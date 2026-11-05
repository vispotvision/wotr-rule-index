//! build/sync.sh, build/wiki_index.py and build/vault_export.py as `wotr-mcp sync`: the autosave for
//! the wiki. Commits and pushes what changed in wiki/ (the Obsidian vault, the source since
//! 2026-10-15; Notion is retired and frozen), copies the rendered Fronts, Ledger and NPC roster into
//! the wiki's Running Pieces (never State of Play, retired 2026-10-17), refreshes the search index.
//! The push rebuilds the public site. The Drive step is gone (R79-12). It alerts only on a push
//! failure: that is the one line with "push failed" in build/sync.log and the one non-zero exit;
//! every other step logs "error" and carries on (build/nightly.py counts the "push failed" lines).
//!
//! Safe to run any time; if nothing changed, nothing is committed. Needs git credentials already
//! set up (gh auth login did that). Runs every 15 minutes as the systemd user timer wotr-sync.timer.
//!
//! Two runs never overlap: the run holds build/.sync.lock (flock, the same lock sync.sh took) for
//! its whole length, and a second one (the timer firing during a manual sync, or the other way
//! round) logs "another sync is running; skipped" and exits 0.
//!
//! rust/sync_parity.py replays every path against sync.sh in two scratch clones.
use crate::util::{chars, command, env_path, head, read_text, rel_posix, rglob_md, root, stem};
use crate::writers::{date_fmt, scenes_to_wiki};
use regex::Regex;
use serde_json::Value;
use std::collections::{BTreeSet, HashMap, HashSet};
use std::fs;
use std::io::{Read, Write};
use std::os::unix::fs::PermissionsExt;
use std::os::unix::process::ExitStatusExt;
use std::path::{Path, PathBuf};
use std::process::{ExitStatus, Stdio};
use std::sync::LazyLock;

// ---------------------------------------------------------------- Python's string semantics
/// Python's \s for str patterns (index.rs keeps its own copy, which is left alone).
const WS: &str = r"[\t\n\x0B\x0C\r\x1C-\x1F \x{85}\x{A0}\x{1680}\x{2000}-\x{200A}\x{2028}\x{2029}\x{202F}\x{205F}\x{3000}]";

fn is_space(c: char) -> bool {
    matches!(c, '\t'..='\r' | '\x1c'..='\x1f' | ' ' | '\u{85}' | '\u{a0}' | '\u{1680}' | '\u{2000}'..='\u{200a}' | '\u{2028}' | '\u{2029}' | '\u{202f}' | '\u{205f}' | '\u{3000}')
}

/// Python's \w for str: isalnum() or '_', which is letters and numbers but not marks.
fn is_word(c: char) -> bool {
    static W: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"[\p{L}\p{N}]").unwrap());
    c == '_' || c.is_ascii_alphanumeric() || (!c.is_ascii() && W.is_match(c.encode_utf8(&mut [0; 4])))
}

/// Path.read_text(encoding="utf-8"): invalid UTF-8 is the error that stops the Python tool.
fn read_strict(p: &Path) -> Result<String, String> {
    let bytes = fs::read(p).map_err(|e| format!("{}: {e}", p.display()))?;
    let text = String::from_utf8(bytes).map_err(|e| format!("{}: {e}", p.display()))?;
    Ok(text.replace("\r\n", "\n").replace('\r', "\n"))
}

fn io<T>(r: std::io::Result<T>, p: &Path) -> Result<T, String> {
    r.map_err(|e| format!("{}: {e}", p.display()))
}

/// wiki/.manifest.json's rows, in file order.
fn manifest() -> Result<Vec<Value>, String> {
    let m = crate::pyjson::loads(&read_strict(&root("wiki/.manifest.json"))?)?;
    Ok(m.as_object().ok_or("wiki/.manifest.json is not a mapping")?.values().cloned().collect())
}

fn field<'a>(row: &'a Value, key: &str) -> Result<&'a str, String> {
    row.get(key).and_then(Value::as_str).ok_or(format!("KeyError: '{key}'"))
}

// ---------------------------------------------------------------- build/wiki_index.py
/// wiki_index.title: the frontmatter title (in the first 1500 chars), else the file's stem.
fn page_title(p: &Path) -> Result<String, String> {
    static TITLE: LazyLock<Regex> = LazyLock::new(|| Regex::new(&format!(r#"(?m)^title:{WS}*"?(.*?)"?{WS}*$"#)).unwrap());
    let text = read_strict(p)?;
    Ok(TITLE.captures(head(&text, 1500)).map(|m| m[1].replace("\\\"", "\"")).unwrap_or_else(|| stem(p)))
}

/// Rewrite wiki/INDEX.md: every page in the vault, by section and shelf, as wikilinks.
fn wiki_index() -> Result<String, String> {
    let wiki = root("wiki");
    let mut private = HashSet::new();
    for m in manifest()? {
        if crate::table::t(m.get("private")) {
            private.insert(field(&m, "rel")?.to_string());
        }
    }
    let parts = |p: &Path| -> Vec<String> { p.strip_prefix(&wiki).unwrap_or(p).components().map(|c| c.as_os_str().to_string_lossy().into_owned()).collect() };
    let mut pages: Vec<PathBuf> = rglob_md(&wiki)
        .into_iter()
        .filter(|p| {
            let x = parts(p);
            !x.iter().any(|c| c.starts_with('.')) && x[x.len() - 1] != "INDEX.md" && x[0] != "Assets"
        })
        .collect();
    pages.sort(); // Path order is by component, as sorted() on Paths
    let mut out = vec![
        "# War of the Realms — every page in the vault".to_string(),
        String::new(),
        format!("{} pages. The wiki is this vault (Notion is retired); public pages publish to https://vispotvision.github.io/wotr-rule-index/. Regenerated by `build/wiki_index.py` on each autosave.", pages.len()),
        String::new(),
        "## The front door".to_string(),
        String::new(),
    ];
    for p in pages.iter().filter(|p| parts(p).len() == 1) {
        let rel = rel_posix(p, &wiki);
        out.push(format!("- [[{}|{}]]", &rel[..rel.len() - 3], page_title(p)?));
    }
    out.push(String::new());
    let mut seen = HashSet::new();
    for p in &pages {
        let x = parts(p);
        if x.len() == 1 {
            continue;
        }
        let folders = &x[..x.len() - 1];
        for depth in 1..=folders.len() {
            if seen.insert(folders[..depth].to_vec()) {
                out.extend([String::new(), format!("{} {}", "#".repeat((depth + 1).min(6)), folders[depth - 1]), String::new()]);
            }
        }
        let rel = rel_posix(p, &wiki);
        let lock = if private.contains(&rel) { " · private" } else { "" };
        out.push(format!("- [[{}|{}]]{lock}", &rel[..rel.len() - 3], page_title(p)?));
    }
    let index = wiki.join("INDEX.md");
    io(fs::write(&index, out.join("\n") + "\n"), &index)?;
    Ok(format!("{} pages -> wiki/INDEX.md", pages.len()))
}

// ---------------------------------------------------------------- build/vault_export.py
/// vault_export.short: the part of a title before " · " or " — ", when it stands as a name.
fn short(title: &str) -> Option<String> {
    static SEP: LazyLock<Regex> = LazyLock::new(|| Regex::new(&format!(r"{WS}+[·—]{WS}+")).unwrap());
    let s = SEP.split(title).next().unwrap_or(title).trim_matches(is_space);
    let n = chars(s);
    (s != title && (n >= 4 && s.contains(' ') || n >= 6)).then(|| s.to_string())
}

fn set(map: &mut Vec<(String, String)>, key: String, value: String) {
    match map.iter_mut().find(|(k, _)| *k == key) {
        Some(row) => row.1 = value,
        None => map.push((key, value)),
    }
}

/// vault_export.targets: display name -> vault page (relative, no .md), in insertion order.
fn targets(manifest: &[Value]) -> Result<Vec<(String, String)>, String> {
    static NAME: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"(?m)^## (.+?) \(").unwrap());
    let mut out: Vec<(String, String)> = Vec::new();
    for v in manifest {
        let rel = field(v, "rel")?;
        let rel = rel[..rel.len().saturating_sub(3)].to_string();
        let title = field(v, "title")?.to_string();
        let sh = short(&title);
        if !out.iter().any(|(t, _)| *t == title) {
            out.push((title, rel.clone()));
        }
        if let Some(sh) = sh.filter(|s| !out.iter().any(|(t, _)| t == s)) {
            out.push((sh, rel));
        }
    }
    let cast = root("scenes/CAST.md");
    if cast.exists() {
        for m in NAME.captures_iter(&read_strict(&cast)?) {
            if !out.iter().any(|(t, _)| *t == m[1]) {
                if let Some(hit) = out.iter().find(|(t, _)| t.starts_with(&m[1])).map(|(_, r)| r.clone()) {
                    out.push((m[1].to_string(), hit));
                }
            }
        }
    }
    let al = root("build/aliases.yaml");
    if al.exists() {
        if let Value::Object(aliases) = crate::pyyaml::load(&read_strict(&al)?)? {
            for (k, v) in aliases {
                let hit = v.as_str().and_then(|v| out.iter().find(|(t, _)| t == v)).map(|(_, r)| r.clone());
                if let Some(rel) = hit {
                    set(&mut out, k, rel);
                }
            }
        }
    }
    Ok(out)
}

/// `(?<![\w\[\|/])(name|name|...)(?![\w\]\|])` over names longest first, as a scan: 460 literal
/// alternatives at every word start are slow through a backtracking engine, and this picks the same
/// match (the first name in order that fits and passes both looks).
struct Names(HashMap<char, Vec<(String, String)>>);

impl Names {
    fn new(names: &[(String, String)]) -> Self {
        let mut by_first: HashMap<char, Vec<(String, String)>> = HashMap::new();
        for (n, r) in names {
            if let Some(c) = n.chars().next() {
                by_first.entry(c).or_default().push((n.clone(), r.clone()));
            }
        }
        Names(by_first)
    }

    fn at(&self, text: &str, i: usize, prev: Option<char>) -> Option<&(String, String)> {
        if prev.is_some_and(|c| is_word(c) || matches!(c, '[' | '|' | '/')) {
            return None;
        }
        let rest = &text[i..];
        let cands = self.0.get(&rest.chars().next()?)?;
        cands.iter().find(|(n, _)| rest.strip_prefix(n.as_str()).is_some_and(|after| !after.chars().next().is_some_and(|c| is_word(c) || matches!(c, ']' | '|'))))
    }
}

/// vault_export.link_text: [[rel|name]] for the first mention of each name on the page, outside
/// headings, tables, code and existing links.
fn link_text(md: &str, names: &Names, self_rel: &str) -> String {
    let mut seen: HashSet<&str> = HashSet::new();
    let mut out: Vec<String> = Vec::new();
    for para in md.split("\n\n") {
        let lead = para.trim_start_matches(is_space);
        if ["#", "```", "|", "---"].iter().any(|x| lead.starts_with(x)) {
            out.push(para.to_string());
            continue;
        }
        let (mut linked, mut pos, mut i, mut prev) = (String::new(), 0, 0, None);
        while i < para.len() {
            if let Some((name, rel)) = names.at(para, i, prev) {
                let before = &para[..i];
                let open = before.matches("[[").count() > before.matches("]]").count() || before.matches("](").count() > before.matches(')').count();
                if rel != self_rel && !seen.contains(name.as_str()) && !open {
                    linked.push_str(&para[pos..i]);
                    linked.push_str(&format!("[[{rel}|{name}]]"));
                    pos = i + name.len();
                    seen.insert(name);
                }
                i += name.len();
                prev = name.chars().last();
            } else {
                let c = para[i..].chars().next().unwrap();
                i += c.len_utf8();
                prev = Some(c);
            }
        }
        linked.push_str(&para[pos..]);
        out.push(linked);
    }
    out.join("\n\n")
}

/// `text.split("\n---\n", 1)[1] if text.startswith("---") else text`; a page opening on --- with no
/// closing line stops the export, as the Python's IndexError does.
fn body_of(text: &str) -> Result<&str, String> {
    if !text.starts_with("---") {
        return Ok(text);
    }
    text.split_once("\n---\n").map(|(_, b)| b).ok_or("IndexError: list index out of range".into())
}

/// The Obsidian view: vault/ generated from wiki/ and scenes/ with [[wikilinks]] injected, so the
/// graph and backlinks work. The mirror itself is never touched. Longest name first, first mention
/// per page only. Each scene gets a "Cast" line of links; each card an "Appears in" list from
/// CAST.md; vault/_Index.md lists sections; vault/.obsidian is left to the reader.
fn vault_export() -> Result<String, String> {
    static CAST: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"(?m)^## (.+?) \(\d+ scenes\)\n(.+)$").unwrap());
    static FILES: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"([\p{L}\p{N}_\-.]+\.md) \(\d+\)").unwrap());
    let (wiki, scenes, vault) = (root("wiki"), root("scenes"), root("vault"));
    let man = manifest()?;
    for sub in ["wiki", "scenes"] {
        // regenerate the content; leave the reader's .obsidian settings alone
        let d = vault.join(sub);
        if d.exists() {
            io(fs::remove_dir_all(&d), &d)?;
        }
        io(fs::create_dir_all(&d), &d)?;
    }
    let tg = targets(&man)?;
    let mut sorted: Vec<&(String, String)> = tg.iter().collect();
    sorted.sort_by_key(|(n, _)| std::cmp::Reverse(chars(n))); // stable, as sorted()
    let list: Vec<(String, String)> = sorted.iter().filter(|(n, _)| chars(n) >= 4).map(|(n, r)| (n.clone(), format!("wiki/{r}"))).collect();
    let names = Names::new(&list);
    let mut cast_index: Vec<(String, Vec<String>)> = Vec::new();
    let cast = scenes.join("CAST.md");
    if cast.exists() {
        for m in CAST.captures_iter(&read_strict(&cast)?) {
            let files: Vec<String> = FILES.captures_iter(&m[2]).map(|f| f[1].to_string()).collect();
            match cast_index.iter_mut().find(|(n, _)| *n == m[1]) {
                Some(row) => row.1 = files,
                None => cast_index.push((m[1].to_string(), files)),
            }
        }
    }
    let mut n_pages = 0;
    for p in rglob_md(&wiki) {
        let fname = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        if fname == "INDEX.md" || fname == "MANIFEST.md" {
            continue;
        }
        let rel = rel_posix(&p, &wiki);
        let rel = &rel[..rel.len() - 3];
        let text = read_text(&p);
        let mut body = link_text(body_of(&text)?, &names, &format!("wiki/{rel}"));
        let title = stem(&p);
        let appears: BTreeSet<&String> = cast_index.iter().filter(|(n, _)| title.contains(n.as_str())).flat_map(|(_, files)| files).collect();
        if !appears.is_empty() {
            let lines: Vec<String> = appears.iter().map(|s| format!("- [[scenes/{}]]", &s[..s.len().saturating_sub(3)])).collect();
            body += &format!("\n\n## Appears in\n{}", lines.join("\n"));
        }
        let dest = vault.join("wiki").join(format!("{rel}.md"));
        if let Some(parent) = dest.parent() {
            io(fs::create_dir_all(parent), parent)?;
        }
        io(fs::write(&dest, body), &dest)?;
        n_pages += 1;
    }
    let mut scene_files: Vec<PathBuf> = fs::read_dir(&scenes).into_iter().flatten().flatten().map(|e| e.path()).filter(|p| p.to_string_lossy().ends_with(".md")).collect();
    scene_files.sort();
    let mut n_scenes = 0;
    for p in scene_files {
        let fname = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        if ["MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md"].contains(&fname.as_str()) {
            continue;
        }
        let text = read_text(&p);
        let who: Vec<&String> = cast_index.iter().filter(|(_, files)| files.contains(&fname)).map(|(n, _)| n).collect();
        let cast_line = if who.is_empty() {
            String::new()
        } else {
            let links: Vec<String> = who.iter().filter_map(|n| tg.iter().find(|(t, _)| t.starts_with(n.as_str())).map(|(_, r)| format!("[[wiki/{r}|{n}]]"))).collect();
            format!("\n\n**Cast:** {}", links.join(" · "))
        };
        let body = link_text(body_of(&text)?, &names, &format!("scenes/{}", stem(&p))) + &cast_line;
        let dest = vault.join("scenes").join(&fname);
        io(fs::write(&dest, body), &dest)?;
        n_scenes += 1;
    }
    for extra in ["TIMELINE.md", "ARCS.md", "CAST.md"] {
        let src = scenes.join(extra);
        if src.exists() {
            let dest = vault.join("scenes").join(extra);
            io(fs::copy(&src, &dest), &dest)?;
        }
    }
    let mut sections = BTreeSet::new();
    for v in &man {
        sections.insert(field(v, "rel")?.split('/').next().unwrap_or_default().to_string());
    }
    let lines: Vec<String> = sections.iter().map(|s| format!("- {s}")).collect();
    let index = vault.join("_Index.md");
    let page = format!(
        "# War of the Realms — vault\n\nGenerated from the wiki mirror and the scene archive by build/vault_export.py; read-only, rebuilt by the hourly sync.\n\n## Sections\n{}\n\n## Scenes\n- [[scenes/TIMELINE]] · [[scenes/ARCS]] · [[scenes/CAST]]\n",
        lines.join("\n")
    );
    io(fs::write(&index, page), &index)?;
    Ok(format!("vault: {n_pages} pages, {n_scenes} scenes, {} link targets -> {}", list.len(), vault.display()))
}

// ---------------------------------------------------------------- build/sync.sh
/// wotr_log: one timestamped line to build/sync.log (appended) and to stdout.
fn log(msg: &str) {
    let line = format!("{}  {msg}\n", date_fmt("%Y-%m-%d %H:%M:%S"));
    if let Ok(mut f) = fs::OpenOptions::new().append(true).create(true).open(root("build/sync.log")) {
        let _ = f.write_all(line.as_bytes());
    }
    let _ = std::io::stdout().write_all(line.as_bytes());
}

/// log_tail: the last `n` lines of a step's output into the log, each prefixed.
fn log_tail(out: &str, n: usize, indent: &str) {
    let out = out.trim_end_matches('\n');
    if out.is_empty() {
        return;
    }
    let lines: Vec<&str> = out.split('\n').collect();
    for line in &lines[lines.len().saturating_sub(n)..] {
        log(&format!("{indent}{line}"));
    }
}

/// The interpreter env.sh would pick, for the two log lines that name it; nothing here runs it.
/// shortcut: without the venv this names the venv anyway where env.sh would find python3 on PATH;
/// delete it with the "python:" lines once nothing reads them.
fn python() -> String {
    let set = env_path("WOTR_PYTHON", None).filter(|p| fs::metadata(p).is_ok_and(|m| m.permissions().mode() & 0o111 != 0));
    let picked = set.or_else(|| env_path("HOME", None).map(|h| h.join(".venvs/wotr/bin/python")));
    picked.map(|p| p.display().to_string()).unwrap_or_default()
}

/// The shell's $?: the exit code, 128 + the signal when a signal ended it.
fn code(s: ExitStatus) -> i32 {
    s.code().or(s.signal().map(|n| 128 + n)).unwrap_or(1)
}

/// `git ... >/dev/null 2>&1`: only exit codes are judged. Git writes warnings to stderr (worktree
/// prune failures and the like).
fn git_quiet(args: &[&str]) -> i32 {
    command("git").args(args).stdout(Stdio::null()).stderr(Stdio::null()).status().map(code).unwrap_or(127)
}

/// `$(git ...)`, stderr where `stderr` says: stdout without its trailing newlines.
fn git_out(args: &[&str], stderr: Stdio) -> String {
    let out = command("git").args(args).stderr(stderr).output();
    out.map(|o| String::from_utf8_lossy(&o.stdout).trim_end_matches('\n').to_string()).unwrap_or_default()
}

/// `<args> -- <what the sync owns>`
fn with_paths<'a>(args: &[&'a str]) -> Vec<&'a str> {
    [args, &["--"][..], &["wiki", "table", "scenes/CAST.md", "scenes/TIMELINE.md"][..]].concat()
}

/// A step that fails or panics is one the sync logs and carries on from.
fn step(f: impl FnOnce() -> Result<String, String>) -> Result<String, String> {
    std::panic::catch_unwind(std::panic::AssertUnwindSafe(f)).unwrap_or_else(|_| Err("panicked; see stderr".into()))
}

/// `wotr-mcp index`, both streams in one pipe as `2>&1`. A child, not index::build in this process:
/// ONNX Runtime aborting or the build panicking must never stop the commit and push.
fn embed_child() -> std::io::Result<(i32, String)> {
    let (mut r, w) = std::io::pipe()?;
    let mut c = command("/proc/self/exe");
    c.arg("index").stdout(w.try_clone()?).stderr(w);
    let mut child = c.spawn()?;
    drop(c); // it holds the write ends, and the read below ends only when they close
    let mut out = Vec::new();
    r.read_to_end(&mut out)?;
    Ok((code(child.wait()?), String::from_utf8_lossy(&out).into_owned()))
}

/// `wotr-mcp sync`: build/sync.sh, the exit code its own.
pub fn main() -> i32 {
    // one sync at a time (the file stays open, and the lock held, until this returns)
    let lock_path = root("build/.sync.lock");
    let lock = match fs::File::create(&lock_path) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("{}: {e}", lock_path.display());
            return 1;
        }
    };
    if lock.try_lock().is_err() {
        log("another sync is running; skipped");
        return 0;
    }

    // One interpreter for every step was the Windows run's lesson (it once resolved to a
    // package-less one and failed silently); the line stays so the log reads as it always has.
    log(&format!("python: {}", python()));

    // scenes/ into the vault as private pages (scenes/ stays the source)
    let (Ok(out) | Err(out)) = step(|| Ok(scenes_to_wiki()));
    log_tail(&out, 1, "  ");

    // the vault's page list, by section and shelf
    let (Ok(out) | Err(out)) = step(wiki_index);
    log_tail(&out, 1, "  ");

    // the rendered table (build/table.py render) into the vault's Running Pieces
    for (name, page) in [("FRONTS", "Fronts, as clocks"), ("LEDGER", "The Ledger, structured"), ("NPCS", "NPC roster")] {
        let (src, dst) = (root(&format!("table/{name}.md")), root(&format!("wiki/The Table — Running Pieces/{page}.md")));
        if let Ok(bytes) = fs::read(&src) {
            if fs::read(&dst).ok().as_ref() != Some(&bytes) {
                let _ = fs::write(&dst, bytes);
            }
        }
    }

    // semantic index over wiki/ and scenes/ for the MCP's wiki and scene_recall (build/index/,
    // gitignored; only chunks whose text changed get re-embedded). The index is a convenience; a
    // failure here must never stop the publish, commit and push below.
    log("embed start");
    let (embed_code, out) = embed_child().unwrap_or_else(|e| (127, e.to_string()));
    if embed_code != 0 {
        log(&format!("embed error (exit {embed_code}) with python at {}", python()));
        log_tail(&out, 6, "    ");
    } else {
        log_tail(&out, 1, "  ");
    }

    // the Obsidian view (vault/, gitignored): the mirror with [[wikilinks]] injected
    let done = step(vault_export);
    let (Ok(out) | Err(out)) = &done;
    log_tail(out, 1, "  ");
    if done.is_err() {
        log("vault error (exit 1)");
    }

    // make sure we are not committing on top of a stale checkout.
    // --autostash: the export has just dirtied wiki/, and a plain `pull --rebase` refuses to run
    // over unstaged changes (exit 128, nothing fetched), so without it the push was rejected as
    // non-fast-forward every time origin had moved. The dirty files are stashed, the rebase runs,
    // and they come back; nightly.sh and book_dispatch.sh pull the same way.
    let pulled = git_quiet(&["pull", "-q", "--rebase", "--autostash", "origin", "master"]);
    if pulled != 0 {
        log(&format!("pull --rebase error (exit {pulled}); committing on the local branch anyway"));
    }

    // When a stashed change collides with a commit that came down, git leaves the file with
    // conflict markers and still exits 0 (the stash entry keeps the original). Nothing is committed
    // over those: the export skips pages Notion has not touched since, so the markers would go up
    // to origin and stay. A rebase stopped on a real conflict lands here too.
    let unmerged = git_out(&["diff", "--name-only", "--diff-filter=U"], Stdio::null());
    if !unmerged.is_empty() {
        log(&format!(
            "push failed: conflict markers in {} file(s) after the pull; nothing committed, resolve by hand: {}",
            unmerged.lines().count(),
            unmerged.lines().next().unwrap_or_default()
        ));
        return 1;
    }

    // what the sync owns; nothing outside this list is ever staged or committed here, so whatever
    // another session has left staged (two often write this repo at once) stays out of the sync's
    // commit and n stays honest
    let changes = git_out(&with_paths(&["status", "--porcelain"]), Stdio::inherit());
    if changes.is_empty() {
        // a quiet run still carries up a commit whose push failed earlier: the last run's, or
        // the nightly's ("push failed (the sync will carry it up)")
        let ahead = git_out(&["rev-list", "--count", "origin/master..master"], Stdio::null());
        if !ahead.is_empty() && ahead != "0" {
            if git_quiet(&["push", "-q", "origin", "master"]) != 0 {
                log(&format!("push failed ({ahead} earlier commit(s) still local)"));
                return 1;
            }
            log(&format!("pushed {ahead} earlier commit(s)"));
        }
        log("no wiki changes");
        return 0;
    }

    let n = changes.lines().count();
    let _ = command("git").args(with_paths(&["add"])).status();
    let subject = format!("Wiki: {n} file(s) edited");
    let committed = git_quiet(&with_paths(&["commit", "-q", "-m", &subject, "-m", "Autosave of the Obsidian vault via build/sync.sh."]));
    if committed != 0 {
        log(&format!("commit error (exit {committed})"));
    }
    if git_quiet(&["push", "-q", "origin", "master"]) != 0 {
        log("push failed");
        return 1;
    }
    log(&format!("pushed {n} file(s)"));
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    fn names(rows: &[(&str, &str)]) -> Names {
        Names::new(&rows.iter().map(|(n, r)| (n.to_string(), r.to_string())).collect::<Vec<_>>())
    }

    #[test]
    fn word_is_pythons() {
        for c in ['a', 'Z', '7', '_', 'ō', '²', '漢'] {
            assert!(is_word(c), "{c}");
        }
        for c in [' ', '-', '—', '\u{304}', '\u{200d}', '‿'] {
            assert!(!is_word(c), "{c}");
        }
    }

    #[test]
    fn short_forms() {
        assert_eq!(short("Sodoku Moto · The Kōkan Line").as_deref(), Some("Sodoku Moto"));
        assert_eq!(short("Abcde — x"), None); // five chars, no space
        assert_eq!(short("Abcdef — x").as_deref(), Some("Abcdef"));
        assert_eq!(short("No separator here"), None);
    }

    #[test]
    fn links_first_mention_outside_links_and_headings() {
        let n = names(&[("Sodoku Moto", "wiki/a"), ("Sodoku", "wiki/b")]);
        assert_eq!(link_text("Sodoku Moto and Sodoku Moto.", &n, "x"), "[[wiki/a|Sodoku Moto]] and Sodoku Moto.");
        assert_eq!(link_text("# Sodoku\n\nSodoku!", &n, "x"), "# Sodoku\n\n[[wiki/b|Sodoku]]!");
        assert_eq!(link_text("[[Sodoku Moto", &n, "x"), "[[Sodoku Moto"); // the lookbehind
        assert_eq!(link_text("[[x Sodoku y", &n, "x"), "[[x Sodoku y"); // an open link
        assert_eq!(link_text("Sodoku", &n, "wiki/b"), "Sodoku"); // its own page
    }

    #[test]
    fn a_failed_lookahead_falls_through_to_the_shorter_name() {
        let n = names(&[("Sodoku Moto", "wiki/a"), ("Sodoku", "wiki/b")]);
        assert_eq!(link_text("Sodoku Motos", &n, "x"), "[[wiki/b|Sodoku]] Motos");
        // a skipped match still consumes its text: the scan resumes after it
        let n = names(&[("Abcd efgh", "wiki/a"), ("efgh ijkl", "wiki/c")]);
        assert_eq!(link_text("Abcd efgh ijkl", &n, "wiki/a"), "Abcd efgh ijkl");
    }

    #[test]
    fn frontmatter_with_no_close_stops_the_export() {
        assert_eq!(body_of("---\na: 1\n---\nbody").unwrap(), "body");
        assert_eq!(body_of("plain").unwrap(), "plain");
        assert!(body_of("---\nnever closed").is_err());
    }

    #[test]
    fn title_line_reads_like_the_python() {
        let d = std::env::temp_dir().join(format!("wotr-sync-test-{}", std::process::id()));
        fs::create_dir_all(&d).unwrap();
        for (body, want) in [("---\ntitle: \"A \\\"B\\\"\"\n---\n", "A \"B\""), ("---\ntitle: Plain  \n---\n", "Plain"), ("# no title\n", "page")] {
            let p = d.join("page.md");
            fs::write(&p, body).unwrap();
            assert_eq!(page_title(&p).unwrap(), want);
        }
        let _ = fs::remove_dir_all(&d);
    }
}
