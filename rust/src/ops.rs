//! The machine's own jobs: `wotr-mcp backup`, `book-next`, `nightly`, `hook` and `tool`.
use crate::analysis;
use crate::gate;
use crate::pyjson::{dumps, dumps_unicode};
use crate::util::{env_path, read_lossy, rel_posix, root, stem};
use crate::verify;
use chrono::{Datelike, Local, NaiveDateTime, TimeDelta, Timelike};
use regex::Regex;
use serde_json::{json, Map, Value};
use std::collections::BTreeSet;
use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::Command;

fn stamp() -> String {
    Local::now().format("%Y-%m-%d %H:%M:%S").to_string()
}

fn take(s: &str, n: usize) -> String {
    s.chars().take(n).collect()
}

fn drop_chars(s: &str, n: usize) -> String {
    s.chars().skip(n).collect()
}

// ---------------------------------------------------------------- backup
const BACKUP_ITEMS: [&str; 13] = ["wiki", "scenes", "table", "rules", "sources", "proposals", "reports", "docs", "RULINGS.md", "CONFLICTS.md", "ROADMAP.md", "CONTINUE.md", "README.md"];
const BACKUP_KEEP: usize = 12;

fn walk(dir: &Path, out: &mut Vec<PathBuf>) {
    for e in fs::read_dir(dir).into_iter().flatten().flatten() {
        let p = e.path();
        // a symlinked file is copied; a symlinked folder is not walked
        let is_link = e.file_type().is_ok_and(|t| t.is_symlink());
        if p.is_dir() {
            if !is_link {
                walk(&p, out);
            }
        } else if p.is_file() {
            out.push(p);
        }
    }
}

/// Adds one file; an error names what another process held open, and the zip carries on.
fn add_to_zip<W: Write + std::io::Seek>(z: &mut zip::ZipWriter<W>, file: &Path, name: &str) -> Result<(), String> {
    use std::os::unix::fs::PermissionsExt;
    let mut f = fs::File::open(file).map_err(|e| e.to_string())?;
    let meta = f.metadata().map_err(|e| e.to_string())?;
    let mut o = zip::write::SimpleFileOptions::default()
        .compression_method(zip::CompressionMethod::Deflated)
        .large_file(meta.len() >= 0xFFFF_FFFF)
        .unix_permissions(meta.permissions().mode());
    if let Ok(m) = meta.modified() {
        let t: chrono::DateTime<Local> = m.into();
        if let Ok(d) = zip::DateTime::from_date_and_time(t.year() as u16, t.month() as u8, t.day() as u8, t.hour() as u8, t.minute() as u8, t.second() as u8) {
            o = o.last_modified_time(d);
        }
    }
    z.start_file(name, o).map_err(|e| e.to_string())?;
    if let Err(e) = std::io::copy(&mut f, z) {
        let _ = z.abort_file();
        return Err(e.to_string());
    }
    Ok(())
}

/// One zip of the canon and the True Canon folder, which lives in no git repository, into Drive when
/// it is mounted and WOTR_BACKUP_DIR otherwise, keeping the last twelve. Run by build/backup.sh.
pub fn backup() -> i32 {
    let log = |m: String| {
        let line = format!("{}  {m}", stamp());
        println!("{line}");
        if let Ok(mut f) = fs::OpenOptions::new().create(true).append(true).open(root("build/backup.log")) {
            let _ = writeln!(f, "{line}");
        }
    };
    let drive = env_path("WOTR_DRIVE", None).filter(|d| d.is_dir()).map(|d| d.join("War of the Realms \u{2014} Backups"));
    let Some(dest) = drive.clone().or_else(|| env_path("WOTR_BACKUP_DIR", Some("~/wotr-backups"))) else {
        return 1;
    };
    if drive.is_none() {
        log(format!("Drive not mounted; writing to {}", dest.display()));
    }
    if let Err(e) = fs::create_dir_all(&dest) {
        log(format!("cannot create {}: {e}", dest.display()));
        return 1;
    }
    let out = dest.join(format!("wotr-{}.zip", Local::now().format("%Y-%m-%d")));
    let file = match fs::File::create(&out) {
        Ok(f) => f,
        Err(e) => {
            log(format!("cannot write {}: {e}", out.display()));
            return 1;
        }
    };
    let mut z = zip::ZipWriter::new(file);
    let (mut n, mut skipped) = (0, Vec::new());
    let repo = root("");
    for item in BACKUP_ITEMS {
        let p = root(item);
        if !p.exists() {
            continue;
        }
        let mut files = Vec::new();
        if p.is_file() {
            files.push(p);
        } else {
            walk(&p, &mut files);
        }
        for f in files.iter().filter(|f| !f.components().any(|c| c.as_os_str() == "__pycache__")) {
            let name = rel_posix(f, &repo);
            match add_to_zip(&mut z, f, &name) {
                Ok(()) => n += 1,
                Err(e) => skipped.push(format!("{name} ({e})")),
            }
        }
    }
    if let Some(folder) = env_path("WOTR_TRUE_CANON", Some("~/wotr-vault/true-canon")) {
        if folder.exists() {
            let base = folder.file_name().unwrap_or_default().to_string_lossy().into_owned();
            let mut files = Vec::new();
            walk(&folder, &mut files);
            for f in files {
                let name = format!("{base}/{}", rel_posix(&f, &folder));
                match add_to_zip(&mut z, &f, &name) {
                    Ok(()) => n += 1,
                    Err(e) => skipped.push(format!("{name} ({e})")),
                }
            }
        } else {
            log(format!("{} not found; skipped", folder.display()));
        }
    }
    if let Err(e) = z.finish() {
        log(format!("could not finish {}: {e}", out.display()));
        return 1;
    }
    let mb = fs::metadata(&out).map(|m| m.len() as f64 / 1e6).unwrap_or(0.0);
    let skip = if skipped.is_empty() { String::new() } else { format!("; skipped {}: {}", skipped.len(), skipped.iter().take(5).cloned().collect::<Vec<_>>().join("; ")) };
    log(format!("wrote {} ({mb:.1} MB, {n} files){skip}", out.display()));
    let mut old: Vec<(std::time::SystemTime, PathBuf)> = fs::read_dir(&dest)
        .into_iter()
        .flatten()
        .flatten()
        .map(|e| e.path())
        .filter(|p| p.file_name().is_some_and(|f| f.to_string_lossy().starts_with("wotr-") && f.to_string_lossy().ends_with(".zip")))
        .filter_map(|p| Some((fs::metadata(&p).ok()?.modified().ok()?, p)))
        .collect();
    old.sort_by(|a, b| b.0.cmp(&a.0));
    for (_, p) in old.into_iter().skip(BACKUP_KEEP) {
        if fs::remove_file(&p).is_ok() {
            log(format!("pruned {}", p.file_name().unwrap_or_default().to_string_lossy()));
        }
    }
    0
}

// ---------------------------------------------------------------- book-next
const FIRST_GATES: i64 = 3; // chapters 1..3 each gate
const EVERY: i64 = 5; // then every fifth: 8, 13, ...

fn gates_for(total: i64) -> BTreeSet<i64> {
    let mut g: BTreeSet<i64> = (1..=FIRST_GATES.min(total)).collect();
    let mut n = FIRST_GATES + EVERY;
    while n <= total {
        g.insert(n);
        n += EVERY;
    }
    g.insert(total); // the last chapter always gates
    g
}

fn s<'a>(v: &'a Value, k: &str) -> &'a str {
    v.get(k).and_then(Value::as_str).unwrap_or("")
}

/// What the book needs next: a chapter is written when ch<NN>/final.md exists, and a gated chapter
/// written and not decided blocks everything after it.
pub fn book_state(slug: &str) -> Result<Value, String> {
    let d = root("book").join(slug);
    let read = |p: PathBuf| -> Result<Value, String> { serde_json::from_str(&read_lossy(&p)).map_err(|e| format!("{}: {e}", p.display())) };
    let outline = read(d.join("outline.json"))?;
    let gates_path = d.join("gates.json");
    let gates = if gates_path.exists() { read(gates_path)? } else { json!({}) };
    let chapters = outline.get("chapters").and_then(Value::as_array).ok_or("outline.json has no chapters")?;
    let total = chapters.len() as i64;
    let gated = gates_for(total);
    let mut rows = Vec::new();
    for c in chapters {
        let n = c.get("number").and_then(Value::as_i64).ok_or("a chapter has no number")?;
        let dec = gates.get(n.to_string()).cloned().unwrap_or(json!({}));
        rows.push(json!({"n": n, "title": s(c, "title"), "written": d.join(format!("ch{n:02}/final.md")).exists(), "gate": gated.contains(&n),
            "decision": dec.get("decision").cloned().unwrap_or(Value::Null), "when": dec.get("when").cloned().unwrap_or(Value::Null), "note": s(&dec, "note")}));
    }
    let flag = |r: &Value, k: &str| r[k].as_bool().unwrap_or(false);
    let blocked = rows.iter().find(|r| flag(r, "gate") && flag(r, "written") && !matches!(r["decision"].as_str(), Some("approved" | "dropped")));
    let rejected = rows.iter().find(|r| r["decision"].as_str() == Some("rejected"));
    let next = rows.iter().find(|r| !flag(r, "written"));
    let (action, chapter, why) = if let Some(r) = rejected {
        let note = if s(r, "note").is_empty() { "no note" } else { s(r, "note") };
        ("rewrite", r["n"].clone(), format!("chapter {} was rejected: {note}", r["n"]))
    } else if let Some(r) = blocked {
        ("blocked", r["n"].clone(), format!("chapter {0} is written and gated; Isaac has not decided (--approve {0} / --reject {0})", r["n"]))
    } else if let Some(r) = next {
        let tail = if flag(r, "gate") { " (a gate chapter)" } else { "" };
        ("write", r["n"].clone(), format!("chapter {} \u{2014} {}{tail}", r["n"], s(r, "title")))
    } else {
        ("done", Value::Null, format!("all {total} chapters are written and every gate is answered"))
    };
    let target = chapter.as_i64().and_then(|c| chapters.get((c - 1) as usize)).and_then(|c| c.get("target_words").cloned()).unwrap_or(json!(3500));
    let written = rows.iter().filter(|r| flag(r, "written")).count();
    let culture = outline.get("culture").cloned().unwrap_or(json!("Kharven"));
    Ok(json!({"slug": slug, "action": action, "chapter": chapter, "why": why, "total": total, "written": written, "thread": s(&outline, "thread"),
        "culture": culture, "target_words": target, "rows": rows, "gated": gated.iter().collect::<Vec<_>>()}))
}

fn write_gates_md(slug: &str) -> Result<(), String> {
    let st = book_state(slug)?;
    let gated: Vec<String> = st["gated"].as_array().into_iter().flatten().map(Value::to_string).collect();
    let mut lines = vec![
        format!("# Gates \u{2014} {slug}"),
        String::new(),
        format!("Chapters {}/{} written. Gate chapters: {} (the first {FIRST_GATES}, then every {EVERY}th, and the last).", st["written"], st["total"], gated.join(", ")),
        String::new(),
        format!("**Next:** {} \u{2014} {}", s(&st, "action"), s(&st, "why")),
        String::new(),
        "| # | chapter | written | gate | decision | when | note |".into(),
        "|---|---|---|---|---|---|---|".into(),
    ];
    for r in st["rows"].as_array().into_iter().flatten() {
        let (w, g) = (r["written"].as_bool().unwrap_or(false), r["gate"].as_bool().unwrap_or(false));
        let dec = match r["decision"].as_str().filter(|d| !d.is_empty()) {
            Some(d) => d,
            None if g && w => "waiting",
            None => "\u{2014}",
        };
        lines.push(format!("| {} | {} | {} | {} | {dec} | {} | {} |", r["n"], s(r, "title"), if w { "yes" } else { "\u{2014}" }, if g { "yes" } else { "\u{2014}" }, s(r, "when"), take(s(r, "note"), 80)));
    }
    lines.extend([
        String::new(),
        "Decide with `wotr-mcp book-next --approve N` or `--reject N --note \"...\"`. Approving does not archive the chapter: `archive_scene` is a separate call Isaac makes.".into(),
        String::new(),
    ]);
    fs::write(root("book").join(slug).join("GATES.md"), lines.join("\n")).map_err(|e| e.to_string())
}

fn decide(slug: &str, n: i64, decision: &str, note: &str) -> Result<(), String> {
    let p = root("book").join(slug).join("gates.json");
    let mut g: Map<String, Value> = if p.exists() { serde_json::from_str(&read_lossy(&p)).map_err(|e| e.to_string())? } else { Map::new() };
    g.insert(n.to_string(), json!({"decision": decision, "when": Local::now().format("%Y-%m-%d").to_string(), "note": note}));
    fs::write(&p, dumps_unicode(&Value::Object(g), Some(1))).map_err(|e| e.to_string())?;
    write_gates_md(slug)?;
    println!("chapter {n}: {decision}{}", if note.is_empty() { String::new() } else { format!(" \u{2014} {note}") });
    Ok(())
}

pub fn book_next(args: &[String]) -> i32 {
    let opt = |f: &str| args.iter().position(|a| a == f).and_then(|i| args.get(i + 1)).map(String::as_str);
    let num = |f: &str| opt(f).and_then(|v| v.parse::<i64>().ok()).filter(|n| *n != 0);
    let slug = opt("--slug").unwrap_or("kharven-year");
    if !root("book").join(slug).join("outline.json").exists() {
        println!("no outline for '{slug}': run the book-chapter workflow with do_foundation first");
        return 1;
    }
    let run = || -> Result<(), String> {
        for (f, d) in [("--approve", "approved"), ("--reject", "rejected"), ("--drop", "dropped")] {
            if let Some(n) = num(f) {
                return decide(slug, n, d, opt("--note").unwrap_or(""));
            }
        }
        let st = book_state(slug)?;
        write_gates_md(slug)?;
        if args.iter().any(|a| a == "--lines") {
            // action, chapter, why on three lines, for build/book_dispatch.sh to `read`
            let chapter = st["chapter"].as_i64().map(|c| c.to_string()).unwrap_or_default();
            println!("{}\n{chapter}\n{}", s(&st, "action"), s(&st, "why").replace('\n', " "));
        } else if args.iter().any(|a| a == "--json") {
            let mut m = Map::new();
            for k in ["slug", "action", "chapter", "why", "total", "written", "thread", "culture", "target_words"] {
                m.insert(k.into(), st[k].clone());
            }
            println!("{}", dumps_unicode(&Value::Object(m), None));
        } else if args.iter().any(|a| a == "--status") {
            for r in st["rows"].as_array().into_iter().flatten() {
                let mark = if r["written"].as_bool().unwrap_or(false) { "written" } else { "\u{2014}" };
                let gate = if r["gate"].as_bool().unwrap_or(false) { "GATE" } else { "    " };
                println!("{:3}  {mark:8} {gate}  {}  {}", r["n"].as_i64().unwrap_or(0), s(r, "decision"), s(r, "title"));
            }
            println!("\n{}: {}", s(&st, "action"), s(&st, "why"));
        } else {
            println!("{}: {}  ({}/{} written)", s(&st, "action"), s(&st, "why"), st["written"], st["total"]);
        }
        Ok(())
    };
    match run() {
        Ok(()) => 0,
        Err(e) => {
            eprintln!("{e}");
            1
        }
    }
}

// ---------------------------------------------------------------- nightly
/// SHA-1, only to keep the finding keys already stored in build/.nightly_state.json.
fn sha1_hex(data: &[u8]) -> String {
    let mut h: [u32; 5] = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0];
    let mut m = data.to_vec();
    m.push(0x80);
    while m.len() % 64 != 56 {
        m.push(0);
    }
    m.extend_from_slice(&((data.len() as u64) * 8).to_be_bytes());
    for block in m.chunks(64) {
        let mut w = [0u32; 80];
        for (i, b) in block.chunks(4).enumerate() {
            w[i] = u32::from_be_bytes([b[0], b[1], b[2], b[3]]);
        }
        for i in 16..80 {
            w[i] = (w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]).rotate_left(1);
        }
        let [mut a, mut b, mut c, mut d, mut e] = h;
        for (i, wi) in w.iter().enumerate() {
            let (f, k) = match i {
                0..=19 => ((b & c) | (!b & d), 0x5A827999),
                20..=39 => (b ^ c ^ d, 0x6ED9EBA1),
                40..=59 => ((b & c) | (b & d) | (c & d), 0x8F1BBCDC),
                _ => (b ^ c ^ d, 0xCA62C1D6u32),
            };
            let t = a.rotate_left(5).wrapping_add(f).wrapping_add(e).wrapping_add(k).wrapping_add(*wi);
            (e, d, c, b, a) = (d, c, b.rotate_left(30), a, t);
        }
        for (x, y) in h.iter_mut().zip([a, b, c, d, e]) {
            *x = x.wrapping_add(y);
        }
    }
    h.iter().map(|x| format!("{x:08x}")).collect()
}

fn finding_key(file: &str, check: &str, text: &str) -> String {
    take(&sha1_hex(format!("{file}|{check}|{}", text.trim()).as_bytes()), 12)
}

/// (file, check, text) rows: the '## <file>' heading above each bullet of a report.
fn findings(report: &str, check: &str) -> Vec<Value> {
    let (mut out, mut cur) = (Vec::new(), String::new());
    for ln in report.lines() {
        if let Some(h) = ln.strip_prefix("## ") {
            cur = h.trim().to_string();
        } else if let Some(t) = ln.strip_prefix("- ").filter(|_| !cur.is_empty()) {
            let text = t.trim();
            out.push(json!({"file": cur, "check": check, "text": text, "key": finding_key(&cur, check, text)}));
        }
    }
    out
}

fn git_out(args: &[&str]) -> String {
    Command::new("git").args(args).current_dir(root("")).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default()
}

fn log_lines(name: &str, cutoff: NaiveDateTime) -> Vec<String> {
    let p = root("build").join(name);
    if !p.exists() {
        return vec![format!("{name}: no log")];
    }
    read_lossy(&p).lines().filter(|l| NaiveDateTime::parse_from_str(&take(l, 19), "%Y-%m-%d %H:%M:%S").is_ok_and(|t| t >= cutoff)).map(String::from).collect()
}

fn finding_line(f: &Value) -> String {
    format!("- [{}] {}: {}", s(f, "check"), s(f, "file"), take(s(f, "text"), 200))
}

/// The nightly checks with a diff digest (reports/nightly.md): validate, resolve and the reconcile
/// audit, each finding hashed against build/.nightly_state.json so the digest says what is NEW, what
/// CLEARED and only counts what stays open; then new scenes, the books, the sync and the backup.
/// Edits no canon. build/nightly.sh runs it at 03:30. `--dry-run` leaves the state alone.
pub fn nightly(args: &[String]) -> i32 {
    let dry = args.iter().any(|a| a == "--dry-run");
    let now = Local::now().naive_local();
    let state_path = root("build/.nightly_state.json");
    let state: Value = if state_path.exists() { serde_json::from_str(&read_lossy(&state_path)).unwrap_or(json!({"run": null, "findings": {}})) } else { json!({"run": null, "findings": {}}) };
    let last_run = state.get("run").and_then(Value::as_str).map(String::from);
    let (mut lines, mut numbers): (Vec<String>, Vec<String>) = (Vec::new(), Vec::new());

    // 1. the gates
    let (code, out) = gate::validate();
    let validate = if code == 0 { "PASS" } else { "FAIL" };
    numbers.push(format!("validate {validate}"));
    if code != 0 {
        let n = out.chars().count();
        lines.extend(["## validate FAILED".into(), String::new(), "```".into(), drop_chars(&out, n.saturating_sub(2500)), "```".into(), String::new()]);
    }
    let _ = gate::resolve();
    let docket = root("out/docket.md");
    let m = docket.exists().then(|| read_lossy(&docket)).and_then(|t| Regex::new(r"(\d+) outstanding").unwrap().captures(&t).map(|c| c[1].to_string()));
    numbers.push(format!("docket {} outstanding", m.as_deref().unwrap_or("?")));
    let conflicts = root("CONFLICTS.md");
    let open = if conflicts.exists() { Regex::new(r"(?m)^\*\*Status:\*\*\s*open").unwrap().find_iter(&read_lossy(&conflicts)).count() } else { 0 };
    numbers.push(format!("conflicts open {open}"));

    // 2. the reconcile audit (writes reports/reconcile.md)
    let mut found = Vec::new();
    match analysis::reconcile() {
        Ok(_) => found = findings(&read_lossy(&root("reports/reconcile.md")), "reconcile"),
        Err(e) => lines.extend(["## reconcile audit failed".into(), String::new(), format!("    {e}"), String::new()]),
    }
    // 3. the diff against last night
    let empty = Map::new();
    let seen = state.get("findings").and_then(Value::as_object).unwrap_or(&empty);
    let mut by_key = Map::new();
    for f in found {
        by_key.insert(s(&f, "key").to_string(), f);
    }
    let new: Vec<&Value> = by_key.iter().filter(|(k, _)| !seen.contains_key(*k)).map(|(_, f)| f).collect();
    let cleared: Vec<&Value> = seen.iter().filter(|(k, _)| !by_key.contains_key(*k)).map(|(_, f)| f).collect();
    let still = by_key.len() - new.len();
    numbers.push(format!("findings NEW {} / CLEARED {} / STILL OPEN {still}", new.len(), cleared.len()));

    // 4. scenes archived since the last run
    let since = last_run.clone().unwrap_or_else(|| (now - TimeDelta::days(1)).format("%Y-%m-%dT%H:%M:%S%.6f").to_string());
    let added = git_out(&["log", &format!("--since={since}"), "--diff-filter=A", "--name-only", "--pretty=format:", "--", "scenes/*.md"]);
    let indexes = ["CAST.md", "TIMELINE.md", "ARCS.md", "MANIFEST.md", "INDEX.md"];
    let new_scenes: BTreeSet<&str> = added
        .lines()
        .filter(|p| p.starts_with("scenes/") && !p.contains("/cast/") && !Path::new(p).file_name().is_some_and(|n| indexes.iter().any(|i| *i == n)))
        .collect();

    // 5. where the book stands
    let mut slugs: Vec<String> = fs::read_dir(root("book")).into_iter().flatten().flatten().filter(|e| e.path().join("outline.json").is_file()).map(|e| e.file_name().to_string_lossy().into_owned()).collect();
    slugs.sort();

    // 6. the sync and the backup. The backup is weekly: show the newest "wrote" line with its date
    // and age, and call it missing only past eight days.
    let sync = log_lines("sync.log", now - TimeDelta::hours(26));
    let pushed = sync.iter().filter(|l| l.contains("pushed")).count();
    let failed: Vec<&String> = sync.iter().filter(|l| l.contains("push failed")).collect();
    let quiet = sync.iter().filter(|l| l.contains("no wiki changes")).count();
    let wrote: Vec<String> = log_lines("backup.log", now - TimeDelta::hours(24 * 8)).into_iter().filter(|l| l.contains("  wrote ")).collect();
    let backup_line = match wrote.last() {
        Some(w) => {
            let age = NaiveDateTime::parse_from_str(&take(w, 19), "%Y-%m-%d %H:%M:%S").map(|t| (now - t).num_days()).unwrap_or(0);
            format!("weekly (Sunday 03:00), last {} ({age} day(s) ago, on schedule): {}", take(w, 10), drop_chars(w, 21))
        }
        None => "weekly (Sunday 03:00): MISSING, no zip written in the last eight days (build/backup.log)".to_string(),
    };

    // 7. the digest
    let mut digest: Vec<String> = vec![
        format!("# Nightly \u{2014} {}", now.format("%Y-%m-%d %H:%M")),
        String::new(),
        "## Overnight".into(),
        String::new(),
        "_(Claude's note goes here; build/nightly.sh writes it after these numbers. If this line is still here, the Claude step was off or failed \u{2014} the numbers below stand on their own.)_".into(),
        String::new(),
        "## Numbers".into(),
        String::new(),
        format!("- {}", numbers.join("\n- ")),
        String::new(),
    ];
    digest.extend(lines);
    if !new_scenes.is_empty() {
        digest.extend(["## Scenes archived since the last run".into(), String::new()]);
        digest.extend(new_scenes.iter().map(|p| format!("- `{}`", stem(Path::new(p)))));
        digest.push(String::new());
    }
    if !slugs.is_empty() {
        digest.extend(["## The book".into(), String::new()]);
        for slug in &slugs {
            match book_state(slug) {
                Ok(st) => {
                    digest.push(format!("- **{slug}**: {}/{} chapters written. Next: {} \u{2014} {}", st["written"], st["total"], s(&st, "action"), s(&st, "why")));
                    if s(&st, "action") == "blocked" {
                        let c = st["chapter"].as_i64().unwrap_or(0);
                        digest.push(format!("  - nothing more is written until you answer: `wotr-mcp book-next --approve {c}` or `--reject {c} --note \"...\"` (book/{slug}/ch{c:02}/GATE.md)"));
                    }
                }
                Err(e) => digest.push(format!("- **{slug}**: book-next failed: {e}")),
            }
        }
        digest.push(String::new());
    }
    digest.extend(["## New findings since last night".into(), String::new()]);
    if new.is_empty() {
        digest.push("- none".into());
    }
    digest.extend(new.iter().take(60).map(|f| finding_line(f)));
    if new.len() > 60 {
        digest.push(format!("- ... and {} more (reports/reconcile.md)", new.len() - 60));
    }
    digest.extend([String::new(), "## Cleared since last night".into(), String::new()]);
    if cleared.is_empty() {
        digest.push("- none".into());
    }
    digest.extend(cleared.iter().take(60).map(|f| finding_line(f)));
    let fail_tail = failed.last().map(|l| format!(": {}", drop_chars(l, 21))).unwrap_or_default();
    digest.extend([
        String::new(),
        format!("## Still open: {still} (see reports/reconcile.md)"),
        String::new(),
        "## The sync (last 26 h) and the weekly backup".into(),
        String::new(),
        format!("- sync: {pushed} push(es), {quiet} quiet run(s), {} push failure(s){fail_tail}", failed.len()),
        format!("- backup: {backup_line}"),
        format!("- last run of this digest: {}", last_run.as_deref().unwrap_or("never")),
        String::new(),
    ]);
    let _ = fs::create_dir_all(root("reports"));
    if let Err(e) = fs::write(root("reports/nightly.md"), digest.join("\n")) {
        eprintln!("reports/nightly.md: {e}");
        return 1;
    }
    println!("nightly: {}; {} new scene(s)", numbers.join("; "), new_scenes.len());

    if !dry {
        let today = now.format("%Y-%m-%d").to_string();
        for (k, f) in by_key.iter_mut() {
            let first = seen.get(k).and_then(|o| o.get("first_seen")).cloned().unwrap_or(json!(today));
            f["first_seen"] = first;
        }
        let saved = json!({"run": now.format("%Y-%m-%dT%H:%M:%S").to_string(), "findings": by_key});
        if let Err(e) = fs::write(&state_path, dumps_unicode(&saved, Some(0))) {
            eprintln!("{}: {e}", state_path.display());
            return 1;
        }
    }
    i32::from(validate != "PASS")
}

// ---------------------------------------------------------------- hook
/// The assistant's text since the last human prompt; tool results are not prompts.
fn last_reply(transcript: &str) -> String {
    let mut parts: Vec<String> = Vec::new();
    for line in transcript.lines() {
        let Ok(e) = serde_json::from_str::<Value>(line) else { continue };
        let content = e.get("message").and_then(|m| m.get("content"));
        match (e.get("type").and_then(Value::as_str), content) {
            (Some("user"), Some(Value::String(_))) => parts.clear(),
            (Some("assistant"), Some(Value::Array(blocks))) => parts.extend(blocks.iter().filter(|b| s(b, "type") == "text").map(|b| s(b, "text").to_string())),
            _ => {}
        }
    }
    parts.retain(|p| !p.trim().is_empty());
    parts.join("\n\n")
}

/// The Claude Code hooks that make a checkout the table, active only where a `.natalie` marker sits at
/// the repo root. SessionStart pulls and prints NATALIE.md; Stop verifies the reply just written and
/// blocks it on any FAIL, once per reply. Replies under 120 words or carrying a code fence pass.
pub fn hook() -> i32 {
    let Ok(input) = std::io::read_to_string(std::io::stdin()) else { return 1 };
    let Ok(h) = serde_json::from_str::<Value>(&input) else { return 1 };
    if !root(".natalie").exists() {
        return 0;
    }
    match s(&h, "hook_event_name") {
        "SessionStart" => {
            let _ = Command::new("git").arg("-C").arg(root("")).args(["pull", "-q", "--ff-only"]).output();
            let natalie = read_lossy(&root("desktop/NATALIE.md"));
            let prompt = natalie.split_once("\n---\n").map(|x| x.1).unwrap_or(&natalie);
            println!("This checkout is the table. You are Natalie for the whole session; the standing prompt follows and governs. A hook verifies every reply you write; a FAIL comes back to you and you fix it before the reply stands. The WOTR MCP (`wotr`) is connected: session_start on the first turn, load_rules and check_docket before prose, fow_line for every number, scene_context on the beat and the draft.\n\n{prompt}");
        }
        "Stop" => {
            if h.get("stop_hook_active").and_then(Value::as_bool).unwrap_or(false) {
                return 0; // one enforced revision per reply; not a loop
            }
            let text = last_reply(&read_lossy(Path::new(s(&h, "transcript_path"))));
            if text.split_whitespace().count() < 120 || text.contains("```") {
                return 0;
            }
            if let Ok(r) = verify::run(&text, &verify::Opts::default()) {
                if !r.fails.is_empty() {
                    let reason = format!("verify_scene on the reply you just wrote:\n\n{}\n\nFix every FAIL and post the corrected reply in full. Nothing else.", verify::report(&r));
                    println!("{}", dumps(&json!({"decision": "block", "reason": reason}), false));
                }
            }
        }
        _ => {}
    }
    0
}

// ---------------------------------------------------------------- tool
/// `wotr-mcp tool NAME [args] [--flags]`: the positional command line the book pipeline's agents use,
/// as (MCP tool name, its arguments). None for `loadout`, which `tool_main` answers itself.
pub fn tool_args(args: &[String]) -> Result<Option<(String, Map<String, Value>)>, String> {
    const VALUED: [&str; 5] = ["--thread", "--type", "--culture", "--band", "--cast"];
    let (mut x, mut cast, mut i): (Vec<&str>, Vec<&str>, usize) = (Vec::new(), Vec::new(), 1);
    let (mut brief, mut combat, mut thread, mut kind, mut culture) = (false, false, "", "standard", "Kharven");
    while i < args.len() {
        match args[i].as_str() {
            "--brief" => brief = true,
            "--combat" => combat = true,
            "--band" => i += 1, // length is not checked any more (R79-1); accepted for old callers
            "--thread" => {
                i += 1;
                thread = args.get(i).map_or("", String::as_str);
            }
            "--type" => {
                i += 1;
                kind = args.get(i).map_or("standard", String::as_str);
            }
            "--culture" => {
                i += 1;
                culture = args.get(i).map_or("Kharven", String::as_str);
            }
            "--cast" => {
                while args.get(i + 1).is_some_and(|a| !VALUED.contains(&a.as_str()) && !a.starts_with("--")) {
                    i += 1;
                    cast.push(&args[i]);
                }
            }
            a => x.push(a),
        }
        i += 1;
    }
    let tool = args.first().map_or("", String::as_str);
    let first = || x.first().copied().ok_or_else(|| format!("{tool} needs an argument"));
    let file = || -> Result<String, String> { fs::read_to_string(first()?).map_err(|e| e.to_string()) };
    let v = match tool {
        "loadout" => return Ok(None),
        "session_start" => json!({"thread": first()?, "scene_type": x.get(1).copied().unwrap_or("standard"), "culture": x.get(2).copied().unwrap_or("Kharven")}),
        "load_rules" => json!({"tags": x, "brief": brief}),
        "check_docket" => json!({"tags": x}),
        "scene_brief" => json!({"beat": first()?, "thread": thread, "scene_type": kind, "culture": culture, "characters": if cast.is_empty() { Value::Null } else { json!(cast) }}),
        "character" | "fow_line" => json!({"name": first()?}),
        "scene_recall" | "wiki" => json!({"query": x.join(" ")}),
        "rule" => json!({"id": first()?}),
        "fronts" | "roster" => json!({"thread": x.first().copied().unwrap_or("")}),
        "due" => json!({"sessions_old": x.first().and_then(|n| n.parse::<i64>().ok()).unwrap_or(2), "thread": x.get(1).copied().unwrap_or("")}),
        "list_conflicts" | "timeline" => json!({}),
        "scene_menu" => json!({"thread": first()?, "culture": culture}),
        "verify" => json!({"markdown": file()?, "combat": combat, "culture": culture}),
        "gap_fill" => json!({"markdown": file()?}),
        "scene_context" => json!({"draft": file()?}),
        "" | "help" | "list" => return Err("tools: session_start load_rules check_docket scene_brief character fow_line scene_recall wiki rule fronts due list_conflicts scene_menu verify gap_fill loadout scene_context roster timeline".into()),
        t => return Err(format!("unknown tool {t}")),
    };
    let name = if tool == "verify" { "verify_scene" } else { tool };
    Ok(Some((name.to_string(), v.as_object().cloned().unwrap_or_default())))
}

pub fn loadout(args: &[String]) -> String {
    analysis::loadout_tags(args.get(1).map_or("standard", String::as_str)).join(" ")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sha1_vectors() {
        assert_eq!(sha1_hex(b"abc"), "a9993e364706816aba3e25717850c26c9cd0d89d");
        assert_eq!(sha1_hex(b""), "da39a3ee5e6b4b0d3255bfef95601890afd80709");
    }

    #[test]
    fn gate_chapters() {
        let g: Vec<i64> = gates_for(14).into_iter().collect();
        assert_eq!(g, [1, 2, 3, 8, 13, 14]);
        assert_eq!(gates_for(2).into_iter().collect::<Vec<_>>(), [1, 2]);
    }

    #[test]
    fn findings_read_the_heading_above() {
        let f = findings("# t\n- early\n## page\n- a thing \nplain\n## next\n- b\n", "reconcile");
        assert_eq!(f.len(), 2);
        assert_eq!((s(&f[0], "file"), s(&f[0], "text")), ("page", "a thing"));
        assert_eq!(s(&f[1], "file"), "next");
    }

    #[test]
    fn reply_starts_after_the_last_human_prompt() {
        let t = r#"{"type":"assistant","message":{"content":[{"type":"text","text":"old"}]}}
{"type":"user","message":{"content":"new prompt"}}
{"type":"assistant","message":{"content":[{"type":"text","text":"one"},{"type":"tool_use"}]}}
{"type":"user","message":{"content":[{"type":"tool_result"}]}}
not json
{"type":"assistant","message":{"content":[{"type":"text","text":"two"}]}}"#;
        assert_eq!(last_reply(t), "one\n\ntwo");
    }

    #[test]
    fn tool_args_map_to_mcp_names() {
        let a = |v: &[&str]| tool_args(&v.iter().map(|s| s.to_string()).collect::<Vec<_>>()).unwrap().unwrap();
        let (n, m) = a(&["load_rules", "combat", "pov", "--brief"]);
        assert_eq!((n.as_str(), m["tags"].as_array().unwrap().len(), m["brief"].as_bool()), ("load_rules", 2, Some(true)));
        let (_, m) = a(&["scene_brief", "the beat", "--thread", "T", "--cast", "A", "B", "--culture", "Moto"]);
        assert_eq!((m["beat"].as_str(), m["characters"].as_array().unwrap().len(), m["culture"].as_str()), (Some("the beat"), 2, Some("Moto")));
        assert!(tool_args(&["archive_scene".to_string()]).is_err());
        assert!(tool_args(&["loadout".to_string(), "duel".to_string()]).unwrap().is_none());
    }
}
