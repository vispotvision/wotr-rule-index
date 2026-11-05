//! Copy the public wiki pages into a Quartz content folder, dressed for the site.
//!
//!   wotr-site <out_dir>
//!
//! Private = marked private in wiki/.manifest.json, `private: true` in a page's frontmatter, or new
//! in a folder whose every manifest page is private. The site is the world, not the workshop: rulings,
//! ratifications, rule ids and notes to Isaac stay in the vault and come off the published page.
mod art;
mod charts;
mod py;
mod rng;
mod tables;
mod text;

use art::{banner, plate};
use charts::render as chart;
use py::{chars, escape, title_case};
use text::{caps, group, has, rx, split, sub};
use serde_json::Value;
use std::collections::{BTreeMap, HashMap, HashSet};
use std::fs;
use std::path::{Path, PathBuf};

const BASE: &str = "/wotr-rule-index";
const PROCESS: &str = r"\bIsaac\b(?! Newton)|\bNatalie\b|\bRULED\b|(?:^|[*\s])Ratified(?:\.|\s+(?:20\d\d|as written|against))|Amendment (?:status|applied)|agent ruling|ruling needed|\bR\d{2}[A-Z]?-[0-9A-Z]|\bDocket \d|Proposed canon|Originated, flagged|Echo Elf ratification|Canon ruling|retcon|Aesthetic Guide|⚠️|Closed against|Unratified|has not been altered|has no page|flagged not filled|Answers the open item|dead canon";
const PROCESS_HEADING: &str = r"(?im)^(#{2,4}) [^\n]*(Open Rulings|Author'?s? Notes|Notes for the Author|Reconciliation note|Amendment status|Flagged Gaps|Open Questions|Discrepancies of Record)[^\n]*$";
const SENTENCE: &str = r"(?<=[.!?])\s+";

fn root() -> PathBuf {
    std::env::var_os("WOTR_ROOT").map_or_else(|| Path::new(env!("CARGO_MANIFEST_DIR")).join("../.."), PathBuf::from)
}

fn read(p: &Path) -> String {
    fs::read_to_string(p).unwrap_or_else(|e| panic!("{}: {e}", p.display()))
}

fn prose(l: &str) -> bool {
    let t = l.trim();
    !t.is_empty() && !has(re!(r"^(?:#|- |\* |\+ |\d+[.)] |\||>|```|~~~|!\[\[|<|---|\$\$|%%)"), t)
}

/// Lines written one paragraph per line get the blank line markdown needs between them.
fn breathe(body: &str) -> String {
    let lines: Vec<&str> = body.split('\n').collect();
    let (mut out, mut fence) = (Vec::with_capacity(lines.len()), false);
    for (i, a) in lines.iter().enumerate() {
        let b = lines.get(i + 1).copied().unwrap_or("");
        out.push(*a);
        let t = a.trim();
        if t.starts_with("```") || t.starts_with("~~~") {
            fence = !fence;
        }
        if !fence && prose(a) && prose(b) && !a.ends_with("  ") && !a.ends_with('\\') {
            out.push("");
        } else if !fence && a.trim_start().starts_with('>') && !b.trim().is_empty() && !b.trim_start().starts_with('>') {
            out.push(""); // a quote ends before whatever follows it
        }
    }
    out.join("\n")
}

/// A quoted passage six paragraphs long is a section, not a quotation: set it as prose.
fn unquote(block: &str) -> String {
    let paras = split(re!(r"\n>\s*\n"), block).into_iter().filter(|p| !p.trim_matches(['>', ' ', '\n']).is_empty()).count();
    if paras < 6 || has(re!(r"^>\s*\[!"), block) {
        return block.to_string();
    }
    let out = sub(re!(r"(?m)^>[ \t]?"), block, |_| String::new());
    sub(re!(r"(?m)^\*\*([A-Z][A-Z0-9 ,'’·:—-]{3,})\*\*\s*$"), &out, |h| format!("### {}", title_case(group(h, 1)).replace("’S", "’s").replace("'S", "'s")))
}

fn pane_body(c: &str) -> String {
    let c = c.trim().replace("<br>", "\n");
    let named = re!(r"\*\*[^*]+\*\*").find_iter(&c).count();
    if named >= 2 && c.starts_with("**") {
        // a run of named abilities: one line each
        let lines: Vec<String> = split(re!(r"\s+(?=\*\*[^*]+\*\*)"), &c).into_iter().filter(|p| !p.trim().is_empty()).map(|p| format!("- {}", p.trim())).collect();
        return lines.join("\n");
    }
    c
}

/// A table with one row of long prose reads better as cards side by side.
fn onerow(whole: &str) -> String {
    let rows: Vec<Vec<&str>> = whole.trim().split('\n').map(|r| r.trim().trim_matches('|').split('|').collect()).collect();
    if rows.len() != 3 || !(2..=4).contains(&rows[0].len()) || rows[2].iter().map(|c| c.chars().count()).sum::<usize>() < 160 {
        return whole.to_string();
    }
    let blocks: String = rows[0].iter().zip(&rows[2]).filter(|(_, c)| !c.trim().is_empty()).map(|(h, c)| format!("<div class=\"wotr-pane\">\n\n**{}**\n\n{}\n\n</div>\n\n", h.trim(), pane_body(c))).collect();
    format!("\n<div class=\"wotr-panes\">\n\n{blocks}</div>\n\n")
}

/// Short definitions become a grid of small cards; long ones stay as paragraphs.
fn glossary(whole: &str, inner: &str) -> String {
    let entries: Vec<&str> = inner.trim().split('\n').filter(|e| !e.trim().is_empty()).collect();
    let total: usize = entries.iter().map(|e| e.chars().count()).sum();
    if total as f64 / entries.len() as f64 > 320.0 {
        return whole.to_string();
    }
    let body = sub(re!(r"(?m)^(\*\*[^*\n]+\*\*)\s*[:—–·-]\s*"), inner.trim(), |c| format!("{} ", group(c, 1)));
    format!("<div class=\"wotr-glossary\">\n\n{body}\n\n</div>\n\n")
}

fn scrub_line(line: &str) -> Option<String> {
    let process = re!(PROCESS);
    if !has(process, line) {
        return Some(line.to_string());
    }
    let lead = caps(re!(r"^(\s*(?:>\s*)*(?:[-*] |\d+\. )?)"), line).map_or("", |c| group(&c, 1));
    if line.trim_start().starts_with('|') {
        // a table row: cut the sentence inside its cell
        let cells: Vec<String> = line
            .split('|')
            .map(|c| {
                let kept = if has(process, c) { split(re!(SENTENCE), c).into_iter().filter(|x| !has(process, x)).collect::<Vec<_>>().join(" ") } else { c.to_string() };
                if kept.trim().is_empty() { " ".to_string() } else { kept }
            })
            .collect();
        return Some(cells.join("|"));
    }
    let rest = &line[lead.len()..];
    let kept: Vec<&str> = split(re!(SENTENCE), rest).into_iter().filter(|x| !has(process, x)).collect();
    let joined = kept.join(" ");
    let text = joined.trim();
    (!text.is_empty() && text.matches("**").count() % 2 == 0 && text.matches('*').count() % 2 == 0).then(|| format!("{lead}{text}"))
}

fn scrub(body: &str) -> String {
    let mut body = body.to_string();
    // whole process sections
    while let Some(m) = caps(re!(PROCESS_HEADING), &body) {
        let (start, end, level) = (m.get(0).unwrap().start(), m.get(0).unwrap().end(), group(&m, 1).len());
        let next = rx(&format!("(?m)^#{{1,{level}}} ")).find_from_pos(&body, end).expect("regex").map(|n| n.start());
        body = format!("{}{}", &body[..start], next.map_or("", |n| &body[n..]));
    }
    let body = sub(re!(r"\s*\((?:R\d{2}[A-Z]?-[\w-]+(?:,\s*|;\s*)?)+\)"), &body, |_| String::new()); // (R53-01, R63-2)
    let body = sub(re!(r"(?im)^\|\s*\**(?:[IVX]+ · )?(?:Open Rulings|Author'?s? Notes|Flagged Gaps)\**\s*\|.*\n"), &body, |_| String::new()); // a contents row naming one
    let body = sub(re!(r"\s*See Open Rulings\.?"), &body, |_| String::new());
    // paragraph by paragraph, the blank lines between them kept as written
    let (mut out, mut last) = (String::with_capacity(body.len()), 0);
    let add = |block: &str, out: &mut String| {
        let start = block.trim_start();
        if !has(re!(PROCESS), block) || start.starts_with('<') || start.starts_with("```") {
            out.push_str(block);
        } else {
            let lines: Vec<String> = block.split('\n').filter_map(scrub_line).collect();
            out.push_str(&lines.join("\n"));
        }
    };
    for m in re!(r"\n\s*\n").find_iter(&body) {
        let m = m.expect("regex");
        add(&body[last..m.start()], &mut out);
        add(m.as_str(), &mut out);
        last = m.end();
    }
    add(&body[last..], &mut out);
    out
}

/// A run of link items becomes a grid of cards; the words after "link:" are the card's line.
fn cards(inner: &str) -> String {
    let items = sub(re!(r"(?m)^(- \[\[[^\]]*\]\]):\s*(.+)$"), inner.trim_end_matches('\n'), |c| format!(r#"{} <span class="wd">{}</span>"#, group(c, 1), group(c, 2)));
    format!("\n<div class=\"wotr-entries\">\n\n{items}\n\n</div>\n\n")
}

/// Quartz styles every <text> with fill: var(--darkgray), which beats a fill attribute; an inline style does not lose.
fn pin_fill(svg: &str) -> String {
    sub(re!(r#"<text([^>]*?) fill="([^"]+)""#), svg, |c| format!(r#"<text{} style="fill:{}""#, group(c, 1), group(c, 2)))
}

fn diagram(wiki: &Path, name: &str) -> String {
    let svg = pin_fill(&read(&wiki.join(format!("Assets/Diagrams/{name}.svg"))));
    format!("\n\n<figure class=\"wotr-figure\">{}</figure>\n\n", svg.replacen("<svg ", r#"<svg class="wotr-diagram" role="img" "#, 1))
}

fn frontmatter_title(head: &str) -> Option<String> {
    caps(re!(r#"(?m)^title:\s*"?(.*?)"?\s*$"#), head).map(|t| group(&t, 1).replace("\\\"", "\""))
}

fn alnum_lower(s: &str) -> String {
    sub(re!(r"\W"), s, |_| String::new()).to_lowercase()
}

/// Set the page's artwork where its markdown H1 stood (Quartz prints the title itself).
fn dress(wiki: &Path, rel: &str, text: &str) -> String {
    let fm_end = caps(re!(r"(?s)^---\n.*?\n---\n"), text).map_or(0, |m| m.get(0).unwrap().end());
    let (head, body) = text.split_at(fm_end);
    let file = rel.rsplit('/').next().unwrap_or(rel);
    let stem = &file[..file.len() - 3];
    let title = frontmatter_title(head).unwrap_or_else(|| stem.to_string());
    // a hub's painting embed (shown in Obsidian) becomes the site banner's art
    let painted = caps(re!(r"(?m)^!\[\[Assets/Paintings/([\w-]+)\.webp(?:\|[^\]]*)?\]\][ \t]*\n?"), body);
    let painting = painted.as_ref().map(|m| group(m, 1));
    let body = match &painted {
        Some(m) => format!("{}{}", &body[..m.get(0).unwrap().start()], &body[m.get(0).unwrap().end()..]),
        None => body.to_string(),
    };
    let no_h1 = match caps(re!(r"^\s*# [^\n]*\n"), &body) {
        Some(m) => format!("\n{}", &body[m.get(0).unwrap().end()..]),
        None => body,
    };
    let mut body = scrub(&breathe(&no_h1));
    // the plate already carries the title
    if let Some(end) = caps(re!(r"^\s*#{1,6} +(.+?)\s*\n"), &body).filter(|f| alnum_lower(group(f, 1)) == alnum_lower(&title)).map(|f| f.get(0).unwrap().end()) {
        body.drain(..end);
    }
    let body = sub(re!(r"(?m)^\|.*\|[ \t]*\n\|[ :|-]+\|[ \t]*\n\|.*\|[ \t]*(?:\n(?![ \t]*\|)|\z)"), &body, |c| onerow(group(c, 0)));
    let body = sub(re!(r"(?m)(?:^>.*\n?)+"), &body, |c| unquote(group(c, 0)));
    // inline, so the art draws in the site's own fonts
    let body = sub(re!(r"!\[\[Assets/Diagrams/([\w-]+)\.svg\]\]"), &body, |c| diagram(wiki, group(c, 1)));
    let body = sub(re!(r"(?ms)^```mermaid\n(.*?)^```[ \t]*$"), &body, |c| format!("\n\n{}\n\n", pin_fill(&chart(group(c, 1), rel).unwrap_or_else(|| group(c, 0).to_string()))));
    let parts: Vec<&str> = rel.split('/').collect();
    let is_hub = parts.len() > 1 && parts[parts.len() - 2] == stem;
    let runs = if is_hub { re!(r"(?m)((?:^- \[\[[^\n]*\n?){1,})") } else { re!(r"(?m)((?:^- \[\[[^\n]*\n?){2,})") };
    let body = sub(runs, &body, |c| cards(group(c, 1)));
    // a run of "**Term**: meaning" lines
    let body = sub(re!(r"(?m)((?:^\*\*[^*\n]{1,60}\*\*\s*[:—–·-][^\n]+\n\n?){4,})"), &body, |c| glossary(group(c, 0), group(c, 1)));
    // a divider straight before a heading doubles the heading's own rule
    let body = sub(re!(r"(?m)^(?:---|\*\*\*|___)[ \t]*\n\s*\n(?=#{2,3} )"), &body, |_| String::new());
    // a line that is wholly bold is a lead-in: set it as one
    let body = sub(re!(r"(?m)^\*\*([^*\n`\[\]]{3,160})\*\*[ \t]*$"), &body, |c| format!("<p class=\"wotr-lede\">{}</p>\n", escape(group(c, 1))));
    // the pronunciation line
    let mut body = sub(re!(r"(?m)^\*\*Say it\*\*\s*·\s*(.+)$"), &body, |c| format!("<p class=\"wotr-sayit\"><span>Say it</span>{}</p>\n", escape(group(c, 1).trim())));
    if is_hub && body.contains("wotr-entries") {
        // the page lists its own contents; Quartz's folder list would repeat it
        body.push_str("\n<span class=\"wotr-curated\"></span>\n");
    }
    let art = if is_hub { banner(rel, &title, BASE, painting) } else { plate(rel, &title) };
    format!("{head}\n{art}{}", body.trim_start_matches('\n'))
}

fn walk(dir: &Path, base: &Path, out: &mut Vec<String>) {
    for e in fs::read_dir(dir).unwrap_or_else(|e| panic!("{}: {e}", dir.display())).flatten() {
        let p = e.path();
        let kind = e.file_type().unwrap_or_else(|e| panic!("{}: {e}", p.display()));
        if kind.is_dir() {
            walk(&p, base, out);
        } else if p.extension().is_some_and(|x| x == "md") {
            out.push(p.strip_prefix(base).unwrap().to_string_lossy().into_owned());
        }
    }
}

/// shutil.copytree without anything named Paintings: banners load those from /assets.
fn copy_assets(from: &Path, to: &Path) {
    fs::create_dir_all(to).unwrap_or_else(|e| panic!("{}: {e}", to.display()));
    for e in fs::read_dir(from).unwrap_or_else(|e| panic!("{}: {e}", from.display())).flatten() {
        if e.file_name() == "Paintings" {
            continue;
        }
        let dest = to.join(e.file_name());
        if e.path().is_dir() {
            copy_assets(&e.path(), &dest);
        } else {
            fs::copy(e.path(), &dest).unwrap_or_else(|x| panic!("{}: {x}", dest.display()));
        }
    }
}

fn build(wiki: &Path, out: &Path) -> usize {
    let manifest: Value = serde_json::from_str(&read(&wiki.join(".manifest.json"))).expect("wiki/.manifest.json");
    let entries: Vec<(&str, bool)> = manifest.as_object().expect("a mapping").values().map(|m| (m["rel"].as_str().expect("rel"), m["private"].as_bool().unwrap_or(false))).collect();
    let private: HashSet<&str> = entries.iter().filter(|e| e.1).map(|e| e.0).collect();
    let mut folders: HashMap<&str, (bool, bool)> = HashMap::new();
    for (rel, flag) in &entries {
        let f = folders.entry(rel.rsplit_once('/').map_or("", |x| x.0)).or_default();
        if *flag {
            f.0 = true;
        } else {
            f.1 = true;
        }
    }
    let closed: Vec<&str> = folders.iter().filter(|(f, v)| !f.is_empty() && v.0 && !v.1).map(|(f, _)| *f).collect();
    if out.exists() {
        fs::remove_dir_all(out).unwrap_or_else(|e| panic!("{}: {e}", out.display()));
    }
    let mut all = Vec::new();
    walk(wiki, wiki, &mut all);
    all.sort_by(|a, b| a.split('/').cmp(b.split('/')));
    let mut kept: BTreeMap<String, Vec<String>> = BTreeMap::new();
    let mut public: Vec<String> = Vec::new();
    for rel in all {
        if rel == "INDEX.md" || rel.starts_with('.') || private.contains(rel.as_str()) {
            continue;
        }
        if closed.iter().any(|f| rel == *f || rel.starts_with(&format!("{f}/"))) {
            continue;
        }
        if has(re!(r"(?m)^private:\s*true\s*$"), chars(&read(&wiki.join(&rel)), 2000)) {
            continue;
        }
        let section = rel.split_once('/').map_or("Pages", |x| x.0).to_string();
        kept.entry(section).or_default().push(rel[..rel.len() - 3].to_string());
        public.push(rel);
    }
    let names: HashSet<&str> = public.iter().map(|r| &r[..r.len() - 3]).collect();
    let mut titles: HashMap<&str, String> = HashMap::new();
    for r in &public {
        let name = &r[..r.len() - 3];
        let text = read(&wiki.join(r));
        titles.insert(name, frontmatter_title(chars(&text, 1500)).unwrap_or_else(|| name.rsplit('/').next().unwrap_or(name).to_string()));
    }
    let keep = |t: &str| names.contains(t) || (t.rsplit('/').next().unwrap_or(t).contains('.') && wiki.join(t).is_file());
    for rel in &public {
        let dest = out.join(rel);
        fs::create_dir_all(dest.parent().unwrap()).unwrap_or_else(|e| panic!("{}: {e}", dest.display()));
        // a link to a page left off the site reads as plain text
        let text = sub(re!(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]"), &read(&wiki.join(rel)), |c| {
            let (whole, target, alias) = (group(c, 0), group(c, 1), c.get(2).map(|a| a.as_str()));
            if !keep(target) {
                return alias.unwrap_or_else(|| target.rsplit('/').next().unwrap_or(target)).to_string();
            }
            match (alias, titles.get(target)) {
                // a bare link reads as its page's title; embeds and aliased links stand as written
                (None, Some(t)) => format!("{}|{}]]", &whole[..whole.len() - 2], t.replace('|', "-")),
                _ => whole.to_string(),
            }
        });
        fs::write(&dest, dress(wiki, rel, &text)).unwrap_or_else(|e| panic!("{}: {e}", dest.display()));
    }
    copy_assets(&wiki.join("Assets"), &out.join("Assets"));
    let mut lines: Vec<String> = ["---", "title: Every Page", "---", "", "Every page on the public wiki, by section and shelf.", ""].map(String::from).to_vec();
    for (section, pages) in &kept {
        lines.extend([format!("## {section}"), String::new()]);
        let mut shelves: BTreeMap<&str, Vec<&String>> = BTreeMap::new();
        for r in pages {
            let parts: Vec<&str> = r.split('/').collect();
            shelves.entry(if parts.len() > 2 { parts[1] } else { "" }).or_default().push(r);
        }
        for (shelf, rs) in &shelves {
            if !shelf.is_empty() {
                lines.extend([format!("### {shelf}"), String::new()]);
            }
            for r in rs {
                lines.push(format!("- [[{r}|{}]]", titles[r.as_str()]));
            }
            lines.push(String::new());
        }
    }
    fs::write(out.join("Every Page.md"), lines.join("\n")).expect("Every Page.md");
    // the site's front page is site/landing.html, laid over Quartz's index after the build
    fs::write(out.join("index.md"), "---\ntitle: War of the Realms\n---\n\n[[Start Here]] · [[Every Page]]\n").expect("index.md");
    public.len()
}

fn main() {
    let Some(out) = std::env::args().nth(1) else {
        eprintln!("usage: wotr-site <out_dir>");
        std::process::exit(2);
    };
    let n = build(&root().join("wiki"), Path::new(&out));
    println!("{n} public pages -> {out}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_workshop_comes_off_the_page() {
        let page = "Keep this.\n\nThe road runs north. Isaac ruled it so. It ends at the sea.\n\n## Author's Notes\n\nGone entirely.\n\n## Next\n\nKept (R53-01, R63-2) here.\n\n- Natalie said so.\n\n| a | Ruled by Isaac. Stays. |\n";
        let got = scrub(page);
        for gone in ["Isaac", "Natalie", "Author's Notes", "Gone entirely", "R53-01"] {
            assert!(!got.contains(gone), "{gone} in {got}");
        }
        for kept in ["Keep this.", "The road runs north. It ends at the sea.", "## Next", "Kept here.", "Stays."] {
            assert!(got.contains(kept), "{kept} in {got}");
        }
    }

    #[test]
    fn isaac_newton_stays() {
        assert_eq!(scrub("Isaac Newton wrote it."), "Isaac Newton wrote it.");
    }

    #[test]
    fn a_page_with_an_unbalanced_mark_after_scrubbing_is_dropped() {
        assert_eq!(scrub("A *bold claim. Isaac said so."), "");
    }

    #[test]
    fn prose_lines_get_blank_lines_outside_fences() {
        assert_eq!(breathe("one\ntwo\n```\nthree\nfour\n```\n> q\nafter"), "one\n\ntwo\n```\nthree\nfour\n```\n> q\n\nafter");
    }

    #[test]
    fn a_long_quote_becomes_prose_and_a_callout_does_not() {
        let long = (0..6).map(|i| format!("> para {i}")).collect::<Vec<_>>().join("\n>\n");
        assert_eq!(unquote(&long), (0..6).map(|i| format!("para {i}")).collect::<Vec<_>>().join("\n\n"));
        let callout = format!("> [!note]\n>\n{long}");
        assert_eq!(unquote(&callout), callout);
    }

    #[test]
    fn a_private_page_never_reaches_the_output() {
        let root = std::env::temp_dir().join(format!("wotr-site-{}", std::process::id()));
        let _ = fs::remove_dir_all(&root);
        let (wiki, out) = (root.join("wiki"), root.join("out"));
        fs::create_dir_all(wiki.join("Assets/Paintings")).unwrap();
        fs::create_dir_all(wiki.join("Lore")).unwrap();
        fs::create_dir_all(wiki.join("Closed")).unwrap();
        fs::write(wiki.join("Assets/Paintings/x.webp"), "art").unwrap();
        fs::write(wiki.join("Assets/keep.txt"), "keep").unwrap();
        fs::write(wiki.join(".manifest.json"), r#"{"a":{"rel":"Secret.md","private":true},"b":{"rel":"Closed/One.md","private":true},"c":{"rel":"Lore/Open.md"}}"#).unwrap();
        fs::write(wiki.join("Secret.md"), "secret").unwrap();
        fs::write(wiki.join("Closed/New.md"), "new in a closed folder").unwrap();
        fs::write(wiki.join("Lore/Hidden.md"), "---\nprivate: true\n---\nhidden").unwrap();
        fs::write(wiki.join("Lore/Open.md"), "---\ntitle: The Open\n---\nSee [[Secret]] and [[Lore/Other]].\n").unwrap();
        fs::write(wiki.join("Lore/Other.md"), "Other.\n").unwrap();
        assert_eq!(build(&wiki, &out), 2);
        for gone in ["Secret.md", "Closed/New.md", "Lore/Hidden.md", "Assets/Paintings"] {
            assert!(!out.join(gone).exists(), "{gone}");
        }
        assert!(out.join("Assets/keep.txt").exists());
        let page = read(&out.join("Lore/Open.md"));
        assert!(page.contains("See Secret and [[Lore/Other|Other]]."), "{page}");
        assert!(read(&out.join("Every Page.md")).contains("- [[Lore/Open|The Open]]"));
        fs::remove_dir_all(&root).unwrap();
    }
}
