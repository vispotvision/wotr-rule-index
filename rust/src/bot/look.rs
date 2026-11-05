//! The bot's view of the repo: pages, cards, scenes and definitions, shaped for Discord. Nothing here
//! writes.
use crate::analysis;
use crate::pages;
use crate::pyyaml;
use crate::re;
use crate::search;
use crate::text::{caps, group, has, rx, split, sub};
use crate::util::{read_lossy, read_page, rglob_md, root, stem};
use crate::writers;
use serde_json::{json, Value};
use std::collections::{BTreeSet, HashSet};
use std::path::{Path, PathBuf};
use std::process::Command;

pub fn commit_hash() -> String {
    Command::new("git").args(["rev-parse", "--short", "HEAD"]).current_dir(root("")).output().ok().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).filter(|s| !s.is_empty()).unwrap_or_else(|| "?".into())
}

fn head(s: &str, n: usize) -> String {
    s.chars().take(n).collect()
}

/// A Markdown fragment as one line of plain text, for a snippet.
pub fn plain(md: &str) -> String {
    let t = sub(re!(r"(?:(?<=\s)|^)#{1,6}\s+"), md, |_| String::new()); // heading marks, even mid-line
    let t = sub(re!(r"(?m)^\s*>\s?"), &t, |_| String::new()); // blockquotes
    let t = sub(re!(r"(\*\*|__|~~|`)"), &t, |_| String::new()); // bold, code
    let t = sub(re!(r"(?<!\w)[*_](?=\S)|(?<=\S)[*_](?!\w)"), &t, |_| String::new()); // italics
    let t = sub(re!(r"\[([^\]]+)\]\([^)]*\)"), &t, |c| group(c, 1).to_string()); // links -> their text
    let t = sub(re!(r"(?m)^\s*[-|:]+\s*$"), &t, |_| String::new()); // table rules
    sub(re!(r"\s+"), &t, |_| " ".to_string()).trim().to_string()
}

/// A whole page as markdown Discord renders: H1-H3 kept, deeper headings bolded, table rows flattened
/// to ' \u{b7} ' lists, blank runs collapsed.
pub fn for_discord(md: &str) -> String {
    let mut out: Vec<String> = Vec::new();
    for line in md.split('\n') {
        if let Some(m) = caps(re!(r"^\s{0,3}#{4,6}\s+(.*)$"), line) {
            out.push(format!("**{}**", group(&m, 1).trim()));
        } else if has(re!(r"^\s*\|[\s:|-]+\|\s*$"), line) {
            continue;
        } else if line.trim().starts_with('|') {
            let cells: Vec<&str> = line.trim().trim_matches('|').split('|').map(str::trim).filter(|c| !c.is_empty()).collect();
            out.push(cells.join(" \u{b7} "));
        } else {
            out.push(line.to_string());
        }
    }
    sub(re!(r"\n{3,}"), &out.join("\n"), |_| "\n\n".to_string()).trim().to_string()
}

fn snippet(text: &str, query: &str, n: usize, width: usize) -> String {
    let lowered = query.to_lowercase();
    let terms: Vec<&str> = re!(r"\w+").find_iter(lowered.as_str()).filter_map(Result::ok).map(|m| m.as_str()).filter(|t| t.chars().count() > 2).collect();
    let mut bits: Vec<String> = Vec::new();
    for b in search::snippets(text, query, n * 3, width) {
        let b = plain(b.trim_matches('.'));
        // the same window found via two terms
        if !b.is_empty() && !bits.iter().any(|x| x.contains(&head(&b, 80)) || b.contains(&head(x, 80))) {
            bits.push(b);
        }
        if bits.len() >= n {
            break;
        }
    }
    let mut s = bits.join(" \u{2026} ");
    for t in terms {
        s = sub(&rx(&format!(r"(?i)(?<!\w)({}\w*)", fancy_regex::escape(t))), &s, |c| format!("**{}**", group(c, 1)));
    }
    if s.is_empty() {
        plain(&head(text, width))
    } else {
        s
    }
}

fn wiki() -> PathBuf {
    root("wiki")
}

fn scenes() -> PathBuf {
    root("scenes")
}

pub fn notion_url(page: &Path) -> Option<String> {
    let rel = crate::util::rel_posix(page, &wiki());
    writers::manifest().iter().find(|(_, v)| v.get("rel").and_then(Value::as_str) == Some(rel.as_str())).map(|(pid, _)| format!("https://www.notion.so/{}", pid.replace('-', "")))
}

fn category(p: &Path) -> String {
    match p.parent() {
        Some(d) if d != wiki() => d.file_name().map_or(String::new(), |n| n.to_string_lossy().into_owned()),
        _ => String::new(),
    }
}

pub fn wiki_hits(query: &str, limit: usize) -> Vec<Value> {
    search::rank(&wiki(), query, limit)
        .into_iter()
        .map(|(score, p, _)| json!({"title": stem(&p), "category": category(&p), "rel": crate::util::rel_posix(&p, &wiki()), "score": score, "snippet": snippet(&read_page(&p), query, 2, 240), "url": notion_url(&p)}))
        .collect()
}

/// (title, text, notion url, category) for a wiki path, else for the best match to a query.
pub fn wiki_page(rel_or_query: &str) -> (String, String, Option<String>, String) {
    let mut p = wiki().join(rel_or_query);
    if !p.is_file() {
        match search::rank(&wiki(), rel_or_query, 5).into_iter().next() {
            Some(h) => p = h.1,
            None => return Default::default(),
        }
    }
    (stem(&p), for_discord(&read_page(&p)), notion_url(&p), category(&p))
}

fn scene_title(text: &str, p: &Path) -> String {
    caps(re!(r"(?m)^#\s+(.+)$"), text).map_or_else(|| stem(p), |m| group(&m, 1).trim().to_string())
}

pub fn scene_hits(query: &str, limit: usize) -> Vec<Value> {
    search::rank(&scenes(), query, limit)
        .into_iter()
        .map(|(score, p, _)| {
            let text = read_page(&p);
            json!({"title": scene_title(&text, &p), "file": p.file_name().map(|n| n.to_string_lossy().into_owned()), "score": score, "snippet": snippet(&text, query, 3, 360)})
        })
        .collect()
}

pub fn scene_text(file: &str) -> (String, String) {
    let p = scenes().join(file);
    if !p.is_file() {
        return Default::default();
    }
    let text = read_page(&p);
    (scene_title(&text, &p), for_discord(&text))
}

/// build/aliases.yaml: names the archive uses that a card title does not carry.
pub fn alias(name: &str) -> String {
    let p = root("build/aliases.yaml");
    if p.exists() {
        if let Ok(doc) = pyyaml::load(&read_lossy(&p)) {
            for (k, v) in doc.as_object().into_iter().flatten() {
                if k.to_lowercase() == name.trim().to_lowercase() {
                    return v.as_str().unwrap_or("").to_string();
                }
            }
        }
    }
    name.to_string()
}

pub struct Page {
    pub path: PathBuf,
    pub title: String,
    pub url: Option<String>,
    pub category: String,
    pub also: Vec<String>,
}

/// The best card for a name. None when there is no card.
pub fn character_page(name: &str) -> Option<Page> {
    let name = alias(name);
    let key = name.trim().to_lowercase();
    let parent = |p: &Path| p.parent().and_then(Path::file_name).map_or(String::new(), |n| n.to_string_lossy().to_lowercase());
    let mut cands: Vec<PathBuf> = rglob_md(&wiki()).into_iter().filter(|p| p.file_name().is_some_and(|n| n != "INDEX.md") && (stem(p).to_lowercase().contains(&key) || parent(p).contains(&key))).collect();
    cands.sort_by_key(|p| (i32::from(key != stem(p).to_lowercase()), i32::from(!parent(p).contains("character")), stem(p).chars().count()));
    let first = cands.first()?.clone();
    Some(Page { title: stem(&first), url: notion_url(&first), category: category(&first), also: cands[1..].iter().take(5).map(|p| stem(p)).collect(), path: first })
}

pub fn timeline() -> Result<String, String> {
    analysis::timeline().map(|t| for_discord(&t))
}

pub fn character_names(prefix: &str, limit: usize) -> Vec<String> {
    let mut names: BTreeSet<String> = BTreeSet::new();
    let cast = read_lossy(&root("scenes/CAST.md"));
    for c in re!(r"(?m)^## (.+?) \(").captures_iter(cast.as_str()).filter_map(Result::ok) {
        names.insert(group(&c, 1).to_string());
    }
    for e in std::fs::read_dir(wiki().join("Characters")).into_iter().flatten().flatten() {
        if e.file_name().to_string_lossy().starts_with("Volume ") {
            for p in std::fs::read_dir(e.path()).into_iter().flatten().flatten().map(|x| x.path()) {
                if p.extension().is_some_and(|x| x == "md") && !stem(&p).starts_with("Volume ") {
                    names.insert(stem(&p));
                }
            }
        }
    }
    let key = prefix.trim().to_lowercase();
    names.into_iter().filter(|n| n.to_lowercase().contains(&key)).take(limit).collect()
}

// ---------------------------------------------------------------- a card, split for display
const KV: &str = r"\*\*([^*\n]{2,48}?)\s*[:\x{ff1a}]?\*\*\s*[:\x{b7}]?\s*(.*?)(?=\s+\*\*[^*\n]{2,48}?\s*[:\x{ff1a}]?\*\*|$)";
const PRIMARIES: [&str; 8] = ["Vitality", "Ardency", "Gnosis", "Dexterity", "Harmonics", "Resilience", "Tempering", "Dominion"];
const STRIP: [char; 3] = [' ', '\u{b7}', ':'];

/// Card markdown for Discord: no H1, no horizontal rules, no empty quote lines.
fn clean(md: &str) -> String {
    let kept: Vec<&str> = md.split('\n').filter(|l| !(has(re!(r"^\s*#\s"), l) || has(re!(r"^\s*([-*_]\s*){3,}$"), l) || has(re!(r"^\s*>\s*$"), l))).collect();
    for_discord(&kept.join("\n"))
}

fn facts_in(text: &str) -> Vec<(String, String)> {
    let mut facts: Vec<(String, String)> = Vec::new();
    for line in text.split('\n') {
        let line = line.trim_start_matches(['>', ' ']).trim();
        for c in re!(KV).captures_iter(line).filter_map(Result::ok) {
            let (k, v) = (group(&c, 1).trim(), group(&c, 2).trim_matches(STRIP));
            if v.chars().next().is_some_and(char::is_alphanumeric) && !k.ends_with('.') && k.chars().count() <= 30 && facts.len() < 9 && !facts.iter().any(|f| f.0 == k) {
                facts.push((k.to_string(), head(&plain(v), 200)));
            }
        }
    }
    facts
}

pub struct Card {
    pub title: String,
    pub url: Option<String>,
    pub category: String,
    pub also: Vec<String>,
    pub overview: String,
    pub facts: Vec<(String, String)>,
    pub sections: Vec<(String, String)>,
}

pub fn card(name: &str) -> Option<Card> {
    let d = character_page(name)?;
    let raw = read_page(&d.path);
    let parts = split(re!(r"(?m)^##\s+"), &raw);
    let (first, rest) = (parts[0], &parts[1..]);
    let mut sections = Vec::new();
    for chunk in rest {
        let (h, body) = chunk.split_once('\n').unwrap_or((chunk, ""));
        let body = clean(body);
        if !body.trim().is_empty() {
            sections.push((h.trim().to_string(), body));
        }
    }
    let facts = facts_in(&format!("{first}\n{}", rest.first().copied().unwrap_or("")));
    Some(Card { title: d.title, url: d.url, category: d.category, also: d.also, overview: clean(first), facts, sections })
}

pub struct FowCard {
    pub title: String,
    pub url: Option<String>,
    pub category: String,
    pub facts: Vec<(String, String)>,
    pub rows: Vec<(String, String, String, String)>,
    pub notes: Vec<String>,
    pub empty: bool,
}

fn cells(line: &str) -> Vec<&str> {
    line.trim().trim_matches('|').split('|').map(str::trim).collect()
}

/// The card's FOW line as structure: facts, one row per Primary, and the card's own notes.
pub fn fow_card(name: &str) -> Option<FowCard> {
    let d = character_page(name)?;
    let raw = pages::fow_line(&alias(name));
    let (mut facts, mut rows, mut notes): (Vec<(String, String)>, Vec<(String, String, String, String)>, Vec<String>) = (Vec::new(), Vec::new(), Vec::new());
    for line in raw.split('\n').skip(1) {
        let s = line.trim();
        if s.is_empty() || s.starts_with('#') || has(re!(r"^\|?\s*-{3,}"), s) {
            continue;
        }
        if s.starts_with('|') {
            let c = cells(s);
            let label = c[0].trim_matches(['*', ' ']);
            if c.len() >= 3 && PRIMARIES.contains(&label) {
                rows.push((label.to_string(), plain(c[1]), plain(c[2]), c.get(3).map_or(String::new(), |x| plain(x))));
            } else if c.len() >= 2 && c[0].starts_with("**") && label != "Stat" {
                let rest: Vec<&str> = c[1..].iter().copied().filter(|x| !x.is_empty()).collect();
                facts.push((c[0].trim_matches(['*', ' ', ':']).to_string(), head(&plain(&rest.join(" \u{b7} ")), 300)));
            }
            continue;
        }
        let body = s.trim_start_matches(['>', ' ']).trim();
        let kv: Vec<(String, String)> = re!(KV)
            .captures_iter(body)
            .filter_map(Result::ok)
            .map(|c| (group(&c, 1).trim_matches([' ', ':']).to_string(), head(&plain(group(&c, 2).trim_matches(STRIP)), 300)))
            .filter(|(k, v)| !v.is_empty() && k.chars().count() <= 30 && k.split_whitespace().count() <= 3 && !k.ends_with('.'))
            .collect();
        if !kv.is_empty() && body.chars().count() < 400 {
            facts.extend(kv);
        } else if s.starts_with('>') && notes.len() < 3 && !plain(body).is_empty() {
            notes.push(head(&plain(body), 400));
        }
    }
    let mut seen = HashSet::new();
    let unique: Vec<(String, String)> = facts.into_iter().filter(|(k, _)| seen.insert(k.clone())).collect();
    let empty = unique.is_empty() && rows.is_empty();
    Some(FowCard { title: d.title, url: d.url, category: d.category, facts: unique.into_iter().take(12).collect(), rows, notes, empty })
}

// ---------------------------------------------------------------- /define
fn after_heading(lines: &[&str], i: usize) -> String {
    let mut out = Vec::new();
    for ln in lines.iter().skip(i + 1).take(18) {
        if ln.starts_with('#') {
            break;
        }
        if !ln.trim().is_empty() {
            out.push(ln.trim());
        }
        if out.len() >= 6 {
            break;
        }
    }
    out.join(" ")
}

/// Where the wiki defines a term (a glossary row, a bold-term line, a heading), verbatim.
pub fn define(term: &str, limit: usize) -> Vec<Value> {
    let term = term.trim().trim_matches(['*', '_', '"', '\'']);
    if term.is_empty() {
        return Vec::new();
    }
    let t = fancy_regex::escape(term);
    let pats = [
        rx(&format!(r"(?i)^\s*(?:[-*\x{{2022}}]\s*)?(?:\*\*|__)\s*{t}\s*(?:\([^)]*\))?\s*(?:\*\*|__)\s*[\x{{2014}}\x{{2013}}:\-\x{{b7}}]\s*(.+)$")),
        rx(&format!(r"(?i)^\s*\|\s*(?:\*\*)?\s*{t}\s*(?:\*\*)?\s*\|\s*(.+?)\s*\|?\s*$")),
        rx(&format!(r"(?i)^\s*(?:[-*\x{{2022}}]\s*)?{t}\s*[\x{{2014}}\x{{2013}}:]\s*(.+)$")),
        rx(&format!(r"(?i)^#{{1,6}}\s*{t}\b.*$")),
    ];
    let lowered = term.to_lowercase();
    let mut hits: Vec<(i64, Value)> = Vec::new();
    for p in rglob_md(&wiki()) {
        if p.file_name().is_some_and(|n| n == "INDEX.md") {
            continue;
        }
        let text = read_page(&p);
        if !text.to_lowercase().contains(&lowered) {
            continue;
        }
        let (st, dir) = (stem(&p), p.parent().and_then(Path::file_name).map_or(String::new(), |n| n.to_string_lossy().into_owned()));
        let lines: Vec<&str> = text.split('\n').collect();
        for (i, ln) in lines.iter().enumerate() {
            for (k, pat) in pats.iter().enumerate() {
                let Some(m) = caps(pat, ln) else { continue };
                let body = if k == 3 { after_heading(&lines, i) } else { group(&m, 1).to_string() };
                let score = if st.to_lowercase() == lowered { 3 } else { 0 } + if has(re!(r"(?i)codex|index|glossary|tongue|terms|lexicon|vocabulary|reference|errata"), &format!("{dir}{st}")) { 2 } else { 0 } + (3 - k as i64) - if dir.contains("Character Cards") { 3 } else { 0 };
                hits.push((score, json!({"page": st, "category": category(&p), "url": notion_url(&p), "text": head(&plain(&body), 700)})));
                break;
            }
        }
    }
    hits.sort_by_key(|h| -h.0);
    let mut seen = HashSet::new();
    let mut out = Vec::new();
    for (_, h) in hits {
        if seen.insert((h["page"].as_str().unwrap_or("").to_string(), head(h["text"].as_str().unwrap_or(""), 60))) {
            out.push(h);
        }
        if out.len() >= limit {
            break;
        }
    }
    out
}

// ---------------------------------------------------------------- a Discord thread as a scene
pub struct Post {
    pub content: String,
    pub speaker: String,
    pub from_bot: bool,
    pub webhook: bool,
    pub ordinary: bool,
}

fn usable(m: &Post) -> bool {
    !(m.content.is_empty() || has(re!(r"^\s*(\(\(|//)"), &m.content) || (m.from_bot && !m.webhook) || !m.ordinary)
}

/// (scene markdown, cast script, speakers) from messages in order. A Tupperbox proxy (a webhook)
/// carries the character's name as its author; out-of-character lines start with "((" or "//".
pub fn compile_scene(title: &str, messages: &[Post]) -> (String, String, Vec<String>) {
    let (mut paras, mut tagged, mut speakers): (Vec<String>, Vec<String>, Vec<String>) = (Vec::new(), Vec::new(), Vec::new());
    let mut last: Option<&str> = None;
    for m in messages.iter().filter(|m| usable(m)) {
        let text = sub(re!(r"[ \t]+"), m.content.trim(), |_| " ".to_string());
        let text = sub(re!(r"\n{3,}"), &text, |_| "\n\n".to_string());
        for para in split(re!(r"\n\s*\n"), &text).into_iter().map(str::trim).filter(|p| !p.is_empty()) {
            paras.push(para.to_string());
            tagged.push(if last == Some(m.speaker.as_str()) { para.to_string() } else { format!("[{}] {para}", m.speaker) });
            last = Some(&m.speaker);
        }
        if !speakers.contains(&m.speaker) {
            speakers.push(m.speaker.clone());
        }
    }
    (format!("# {title}\n\n{}\n", paras.join("\n\n")), format!("# {title}\n\n{}\n", tagged.join("\n\n")), speakers)
}
