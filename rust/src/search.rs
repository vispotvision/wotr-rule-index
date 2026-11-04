//! wiki, scene_recall and scene_context (mcp_server.py's _rank, _snippets, _hybrid, the wiki and
//! scene_recall tools, _pre_r70_tag, _reversion_map, and build/lorebook.py), ported line for line.
//! One deliberate difference: lorebook.py iterates a Python set of aliases, whose order Python
//! randomizes per process, so pages tied on score come out in any order there; here ties are
//! broken alphabetically and the output is stable.
use crate::embed;
use crate::util::{back, chars, fwd, head, read_lossy, read_page, rel_posix, rglob_md, root, stem, ROOT};
use fancy_regex::Regex;
use std::collections::{BTreeSet, HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::sync::{Arc, LazyLock, Mutex};
use unicode_normalization::UnicodeNormalization;

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

fn terms(query: &str) -> Vec<String> {
    rx!(r"\w+").find_iter(&query.to_lowercase()).flatten().map(|m| m.as_str().to_string()).filter(|t| chars(t) > 2).collect()
}

fn count(hay: &str, needle: &str) -> usize {
    if needle.is_empty() { hay.chars().count() + 1 } else { hay.matches(needle).count() }
}

/// _rank: the keyword ranker. (score, path, lowercased text), best first, ties in walk order.
fn rank(root_dir: &Path, query: &str, limit: usize) -> Vec<(i64, PathBuf, String)> {
    let ts = terms(query);
    if ts.is_empty() {
        return vec![];
    }
    let phrase = query.to_lowercase().trim().to_string();
    let mut hits = Vec::new();
    for p in rglob_md(root_dir) {
        let name = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        if name == "INDEX.md" || name == "MANIFEST.md" {
            continue;
        }
        let low = read_lossy(&p).to_lowercase();
        let st = stem(&p).to_lowercase();
        let title_bonus = 5 * ts.iter().filter(|t| st.contains(t.as_str())).count() as i64;
        let phrase_bonus = if ts.len() > 1 { 10 * count(&low, &phrase).min(5) as i64 } else { 0 };
        let coverage = ts.iter().filter(|t| low.contains(t.as_str())).count() as i64;
        let mut score = title_bonus + phrase_bonus + 3 * coverage + ts.iter().map(|t| count(&low, t).min(10) as i64).sum::<i64>();
        if coverage < 1.max(ts.len() as i64 - 1) {
            score = score.div_euclid(3);
        }
        if score != 0 {
            hits.push((score, p, low));
        }
    }
    hits.sort_by_key(|h| -h.0);
    hits.truncate(limit);
    hits
}

/// _snippets: up to n windows of `width` chars around the query's terms.
fn snippets(text: &str, query: &str, n: usize, width: usize) -> Vec<String> {
    let mut out = Vec::new();
    for t in terms(query) {
        let Ok(r) = Regex::new(&format!("(?i){}", fancy_regex::escape(&t))) else { continue };
        for m in r.find_iter(text).flatten() {
            let (a, b) = (back(text, m.start(), width / 2), fwd(text, m.end(), width / 2));
            out.push(format!("...{}...", text[a..b].replace('\n', " ").trim()));
            if out.len() >= n {
                return out;
            }
        }
    }
    out
}

/// _hybrid: semantic hits merged with the keyword ranker; (score out of 100, path, snippets).
fn hybrid(root_dir: &Path, corpus: &str, query: &str, limit: usize) -> Vec<(i64, PathBuf, Vec<String>)> {
    let kw = rank(root_dir, query, limit * 2);
    let sem = embed::search(query, corpus, limit * 4, 2);
    if sem.is_empty() {
        return kw.into_iter().map(|(sc, p, low)| (sc, p, snippets(&low, query, 3, 220))).collect();
    }
    let kw_max = kw.iter().map(|k| k.0).max().filter(|m| *m != 0).unwrap_or(1) as f64;
    struct M {
        sem: f64,
        kw: f64,
        chunks: Vec<(String, String, f64)>,
    }
    let mut merged: Vec<(PathBuf, M)> = Vec::new();
    for h in sem {
        merged.push((ROOT.join(&h.path), M { sem: h.score, kw: 0.0, chunks: h.chunks }));
    }
    for (sc, p, _) in &kw {
        match merged.iter_mut().find(|(q, _)| q == p) {
            Some((_, m)) => m.kw = *sc as f64 / kw_max,
            None => merged.push((p.clone(), M { sem: 0.0, kw: *sc as f64 / kw_max, chunks: vec![] })),
        }
    }
    let total = |m: &M| m.sem + 1.0 * m.kw;
    merged.sort_by(|a, b| total(&b.1).total_cmp(&total(&a.1)));
    merged.truncate(limit);
    merged
        .into_iter()
        .map(|(p, m)| {
            let mut snips: Vec<String> = m.chunks.iter().take(2).map(|(h, t, _)| format!("[{h}] {}{}", head(t, 320).replace('\n', " "), if chars(t) > 320 { "..." } else { "" })).collect();
            if m.kw != 0.0 {
                let extra: Vec<String> = snippets(&read_page(&p), query, 2, 220)
                    .into_iter()
                    .filter(|x| {
                        let key = x.chars().skip(3).take(57).collect::<String>().to_lowercase();
                        !snips.iter().any(|y| y.to_lowercase().contains(&key))
                    })
                    .collect();
                snips.extend(extra);
            }
            ((100.0 * total(&m) / 1.7).round_ties_even() as i64, p, snips)
        })
        .collect()
}

fn fold(s: &str) -> String {
    s.nfd().filter(|c| !unicode_normalization::char::is_combining_mark(*c)).collect::<String>().to_lowercase()
}

pub fn wiki(query: &str, full: bool, limit: i64) -> String {
    let wiki = root("wiki");
    let hits = hybrid(&wiki, "wiki", query, limit.clamp(1, 25) as usize);
    if hits.is_empty() {
        return format!("nothing in the wiki mirror matches '{query}'");
    }
    let mut out: Vec<String> = hits.iter().map(|(score, p, snips)| format!("## {}  ({}, score {score})\n{}", stem(p), rel_posix(p, &wiki), snips.join("\n"))).collect();
    if full {
        let is_card = |q: &Path| {
            let parts: Vec<String> = q.components().map(|c| c.as_os_str().to_string_lossy().into_owned()).collect();
            let in_cards = parts.iter().any(|x| x.to_lowercase().contains("character cards") || x == "Characters");
            let parent = q.parent().and_then(|d| d.file_name()).map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
            let landing = stem(q).to_lowercase().starts_with("volume") || stem(q) == parent;
            in_cards && !landing
        };
        let qwords: Vec<String> = rx!(r"\W+").split(query).flatten().filter(|w| chars(w) > 2).map(String::from).collect();
        let st = |p: &Path| fold(&stem(p));
        let card = hits.iter().map(|h| &h.1).find(|p| {
            is_card(p) && !qwords.is_empty() && qwords.iter().all(|w| Regex::new(&format!(r"\b{}", fancy_regex::escape(&fold(w)))).ok().is_some_and(|r| r.is_match(&st(p)).unwrap_or(false)))
        });
        let best = card.unwrap_or(&hits[0].1);
        let top = read_page(best);
        out.push(format!("\n---- full text of {} ----\n{}{}", stem(best), head(&top, 14000), if chars(&top) > 14000 { "\n...[truncated]" } else { "" }));
    }
    out.join("\n\n")
}

fn git(args: &[&str]) -> (i32, String) {
    match std::process::Command::new("git").args(args).current_dir(&*ROOT).output() {
        Ok(o) => (o.status.code().unwrap_or(1), format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)).trim().to_string()),
        Err(e) => (1, e.to_string()),
    }
}

/// _pre_r70_tag: a scene written under the style law before 2026-10-03.
fn pre_r70_tag(p: &Path, editions: &HashMap<String, String>) -> &'static str {
    let name = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let ed = editions.get(&name).cloned().unwrap_or_else(|| {
        let rel = rel_posix(p, &ROOT);
        let (code, added) = git(&["log", "--diff-filter=A", "--format=%as", "-1", "--", &rel]);
        if code == 0 && !added.is_empty() && added.as_str() < "2026-10-03" { "pre-R70".into() } else { "R70".into() }
    });
    if ed == "pre-R70" { "  (pre-R70 style: precedent for events, not for prose)" } else { "" }
}

pub fn scene_recall(query: &str, limit: i64, old_lore: bool) -> String {
    let (dir, corpus) = if old_lore { (root("lore/v1/scenes"), "lore-v1") } else { (root("scenes"), "scenes") };
    let hits = hybrid(&dir, corpus, query, limit.clamp(1, 25) as usize);
    if hits.is_empty() {
        return format!("no {}scene matches '{query}'", if old_lore { "old-lore " } else { "" });
    }
    let manifest = dir.join("MANIFEST.md");
    let editions: HashMap<String, String> = if manifest.exists() {
        rx!(r"(?m)^\| (\S+\.md) \| \d+ \| (\S+) \|$").captures_iter(read_lossy(&manifest).as_str()).flatten().map(|c| (c[1].to_string(), c[2].to_string())).collect()
    } else {
        HashMap::new()
    };
    let out: Vec<String> = hits
        .iter()
        .map(|(score, p, snips)| {
            let text = read_page(p);
            let title = rx!(r"(?m)^#\s+(.+)$").captures(text.as_str()).ok().flatten().map(|c| c[1].to_string()).unwrap_or_else(|| stem(p));
            let tag = if old_lore { "  (OLD LORE v1: not canon for events)" } else { pre_r70_tag(p, &editions) };
            let name = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
            format!("## {title}  ({name}, score {score}){tag}\n{}", snips.join("\n"))
        })
        .collect();
    out.join("\n\n")
}

// ---------------------------------------------------------------- the lorebook (lorebook.py)
const NAME_SECTIONS: [&str; 10] = ["Character Cards", "Characters", "Bestiary", "Artifacts", "Natural Beasts", "The Called", "Summoned", "Aberrations", "The Fourteen", "Sodoku Moto"];
const SKIP_TITLES: [&str; 21] = ["INDEX", "MANIFEST", "Geography", "War", "Misc", "Peoples", "Materials", "Techniques", "Characters", "Cosmology", "Disciplines", "Factions", "Spellcraft", "Reference Table", "In-World Document", "Information not on WIKI", "Lore & History", "Magic System", "Natural Beasts", "Summoned and Bound", "Aberrations"];
const SKIP_TITLES2: [&str; 2] = ["Artifacts", "Bestiary"];
const STOP: &str = "the and of a an in on at to for with by from as or his her their its he she they it who what when where which one two three four five six seven eight nine ten first last north south east west northern southern eastern western inner outer old new great high low long black white red iron gold silver king queen lord lady house hall gate wall road river sea sky fire water earth air stone blood bone night day world plane fate war peace crown sword blade hand fist eye heart voice state play table scene archive card cards volume chapter part master guide ledger register common tongue works days family families";
const HONORIFICS: &str = r"^(?:Commander|Captain|General|Lord|Lady|Sir|Dame|Master|Mistress|Brother|Sister|Father|Mother|King|Queen|Prince|Princess|Saint|Doctor|Dr\.?|Emperor|Empress|Archon|Primate|High)\s+";

fn stop() -> &'static HashSet<&'static str> {
    static S: LazyLock<HashSet<&'static str>> = LazyLock::new(|| STOP.split_whitespace().collect());
    &S
}

fn frontmatter(text: &str) -> (HashMap<String, String>, &str) {
    let mut fm = HashMap::new();
    let Some(rest) = text.strip_prefix("---\n") else { return (fm, text) };
    let Some(end) = rest.find("\n---\n") else { return (fm, text) };
    for ln in rest[..end].lines() {
        if let Some(c) = rx!(r#"^(\w+):\s*"?(.*?)"?\s*$"#).captures(ln).ok().flatten() {
            fm.insert(c[1].to_string(), c[2].to_string());
        }
    }
    (fm, &rest[end + 5..])
}

fn is_card_section(section: &str) -> bool {
    section.contains("Character Cards") || section.contains("Characters")
}

fn aliases(title: &str, section: &str) -> BTreeSet<String> {
    let mut out = BTreeSet::new();
    let parts: Vec<String> = rx!(r"\s+[·—/]\s+|\s+-\s+").split(title).flatten().map(|p| p.trim_matches(|c| c == ' ' || c == '*' || c == '_').to_string()).collect();
    let named = NAME_SECTIONS.iter().any(|s| section.contains(s));
    let hon = rx!(HONORIFICS);
    for p in &parts {
        let p = rx!(r"^(The|A|An)\s+").replace(p, "").trim().to_string();
        if p.is_empty() || stop().contains(p.to_lowercase().as_str()) {
            continue;
        }
        let bare = hon.replace(&p, "").trim().to_string();
        for q in [p.clone(), bare] {
            let words = q.split_whitespace().count();
            if words >= 2 || chars(&q) >= 4 && named {
                out.insert(q);
            }
        }
    }
    if is_card_section(section) {
        if let Some(f) = hon.replace(&parts[0], "").split_whitespace().next() {
            if chars(f) >= 4 && !stop().contains(f.to_lowercase().as_str()) && f.chars().next().is_some_and(char::is_uppercase) {
                out.insert(f.trim_matches(',').to_string());
            }
        }
    }
    out
}

#[derive(Clone)]
struct Entry {
    path: PathBuf,
    title: String,
    section: String,
    url: String,
}

struct Registry {
    stamp: (usize, u128, u128),
    aliases: HashMap<String, Vec<Entry>>,
    order: Vec<String>,
    lower: HashSet<String>,
}

fn lower_words(text: &str) -> impl Iterator<Item = String> + '_ {
    rx!(r"(?<![A-Za-z])[a-z][a-z'’]{3,}").find_iter(text).flatten().map(|m| m.as_str().to_string())
}

fn registry() -> Arc<Registry> {
    static REG: LazyLock<Mutex<Option<Arc<Registry>>>> = LazyLock::new(|| Mutex::new(None));
    let mtime = |p: &Path| std::fs::metadata(p).and_then(|m| m.modified()).ok().and_then(|t| t.duration_since(std::time::UNIX_EPOCH).ok()).map(|d| d.as_nanos()).unwrap_or(0);
    let files: Vec<PathBuf> = rglob_md(&root("wiki")).into_iter().filter(|p| p.file_name().is_some_and(|n| n != "INDEX.md" && n != "MANIFEST.md")).collect();
    let extra = root("build/aliases.yaml");
    let stamp = (files.len(), files.iter().map(|p| mtime(p)).max().unwrap_or(0), if extra.exists() { mtime(&extra) } else { 0 });
    let mut slot = REG.lock().unwrap();
    if let Some(r) = slot.as_ref().filter(|r| r.stamp == stamp) {
        return r.clone();
    }
    let mut by_alias: HashMap<String, Vec<Entry>> = HashMap::new();
    let mut first_seen: Vec<String> = Vec::new();
    let mut by_title: HashMap<String, Entry> = HashMap::new();
    let mut lower = HashSet::new();
    for p in &files {
        let raw = read_lossy(p);
        let (fm, body) = frontmatter(&raw);
        lower.extend(lower_words(body));
        let title = fm.get("title").filter(|t| !t.is_empty()).cloned().unwrap_or_else(|| stem(p));
        if SKIP_TITLES.contains(&title.as_str()) || SKIP_TITLES2.contains(&title.as_str()) {
            continue;
        }
        let parent = p.parent().and_then(|d| d.file_name()).map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        let section = fm.get("section").filter(|s| !s.is_empty()).cloned().unwrap_or(parent);
        let e = Entry { path: p.clone(), title: title.clone(), section: section.clone(), url: fm.get("notion_url").cloned().unwrap_or_default() };
        by_title.insert(title.clone(), e.clone());
        for a in aliases(&title, &section) {
            if !by_alias.contains_key(&a) {
                first_seen.push(a.clone());
            }
            by_alias.entry(a).or_default().push(e.clone());
        }
    }
    if let Ok(t) = std::fs::read_to_string(&extra) {
        if let Ok(serde_yaml_ng::Value::Mapping(m)) = serde_yaml_ng::from_str::<serde_yaml_ng::Value>(&t) {
            for (k, v) in m {
                let s = |x: &serde_yaml_ng::Value| x.as_str().map(String::from).or_else(|| serde_yaml_ng::to_string(x).ok().map(|y| y.trim().to_string())).unwrap_or_default();
                let (alias, title) = (s(&k), s(&v));
                if let Some(e) = by_title.get(&title) {
                    if !by_alias.contains_key(&alias) {
                        first_seen.push(alias.clone());
                    }
                    by_alias.entry(alias).or_default().push(e.clone());
                }
            }
        }
    }
    // longest aliases first so "Söröl Ajiin" is tried before "Ajiin"
    let mut order = first_seen;
    order.sort_by_key(|a| (std::cmp::Reverse(a.split_whitespace().count()), std::cmp::Reverse(chars(a))));
    let r = Arc::new(Registry { stamp, aliases: by_alias, order, lower });
    *slot = Some(r.clone());
    r
}

/// Matches of a literal with Python's (?<![\w\-])...(?![\w\-]) around it, non-overlapping, as findall.
fn count_bounded(hay: &str, lit: &str) -> usize {
    let word = |c: Option<char>| c.is_some_and(|c| c.is_alphanumeric() || c == '_' || c == '-');
    let (mut n, mut pos) = (0, 0);
    while let Some(i) = hay[pos..].find(lit).map(|i| i + pos) {
        let end = i + lit.len();
        if !word(hay[..i].chars().next_back()) && !word(hay[end..].chars().next()) {
            n += 1;
            pos = end;
        } else {
            pos = i + hay[i..].chars().next().map(char::len_utf8).unwrap_or(1);
        }
        if lit.is_empty() || pos > hay.len() {
            break;
        }
    }
    n
}

fn head_cut(text: &str, n: usize) -> String {
    let text = text.trim();
    if chars(text) <= n {
        return text.to_string();
    }
    let lim = fwd(text, 0, n);
    let cut = text[..lim].rfind("\n\n").map(|b| chars(&text[..b]));
    let end = match cut {
        Some(c) if c > n / 2 => fwd(text, 0, c),
        _ => lim,
    };
    format!("{}\n...[more on the page]", text[..end].trim_end())
}

fn unknown_names(draft: &str, matched: &HashSet<String>, reg: &Registry) -> Vec<String> {
    let mut known: HashSet<String> = HashSet::new();
    for a in matched.iter().chain(reg.order.iter()) {
        known.extend(a.split_whitespace().map(str::to_lowercase));
    }
    let mut lower: HashSet<String> = lower_words(draft).collect();
    lower.extend(reg.lower.iter().cloned());
    let mut counts: Vec<(String, usize)> = Vec::new();
    // (?<=[\s\S]) is Python's (?<!^): a name at the very start of the draft is skipped and the
    // scan moves on, so "Sodoku Moto" opening a draft still yields "Moto"
    let r = rx!(r"(?<![.!?]\s)(?<=[\s\S])(?<!\n)\b([A-Z][a-zāēīōūöüáéíóúñ]{3,}(?:\s+[A-Z][a-zāēīōūöüáéíóúñ]{2,})?)\b");
    for c in r.captures_iter(draft).flatten() {
        let m = c.get(1).unwrap();
        let w = m.as_str();
        let first = w.split_whitespace().next().unwrap_or("").to_lowercase();
        if stop().contains(first.as_str()) || known.contains(&first) || lower.contains(&first) || lower.contains(first.trim_end_matches('s')) {
            continue;
        }
        match counts.iter_mut().find(|(k, _)| k == w) {
            Some((_, n)) => *n += 1,
            None => counts.push((w.to_string(), 1)),
        }
    }
    counts.sort_by_key(|(_, n)| std::cmp::Reverse(*n));
    counts.into_iter().filter(|(_, n)| *n >= 2).take(12).map(|(w, _)| w).collect()
}

/// _reversion_map: struck -> governing pairs from the Moto Reversion Ledger, the Canon
/// Amendment's strike and build/renames.yaml, longest first.
fn reversion_map() -> Vec<(String, String)> {
    let mut pairs = Vec::new();
    let src = std::fs::read_dir(root("sources")).into_iter().flatten().flatten().map(|e| e.path()).find(|p| p.file_name().is_some_and(|n| n.to_string_lossy().contains("Moto_Reversion")));
    if let Some(src) = src {
        for ln in read_lossy(&src).split('\n') {
            let s = ln.trim();
            if !s.starts_with('|') || rx!(r"^\|\s*-").is_match(s).unwrap_or(false) {
                continue;
            }
            let cells: Vec<String> = s.trim_matches('|').split('|').map(|c| c.trim().trim_matches('*').trim().to_string()).collect();
            if cells.len() >= 2 && !cells[0].is_empty() && cells[0] != "Struck" {
                pairs.push((cells[0].clone(), cells[1].clone()));
            }
        }
    }
    for (a, b) in [("Sātūlagi", "(struck; the Inner World / Kharven)"), ("Satulagi", "(struck)"), ("Buri", "Moto")] {
        pairs.push((a.to_string(), b.to_string()));
    }
    if let Ok(t) = std::fs::read_to_string(root("build/renames.yaml")) {
        if let Ok(serde_yaml_ng::Value::Sequence(v)) = serde_yaml_ng::from_str::<serde_yaml_ng::Value>(&t) {
            for r in v {
                if let (Some(o), Some(n)) = (r.get("old").and_then(|x| x.as_str()), r.get("new").and_then(|x| x.as_str())) {
                    pairs.push((o.to_string(), n.to_string()));
                }
            }
        }
    }
    pairs.sort_by_key(|p| std::cmp::Reverse(chars(&p.0)));
    pairs
}

pub fn scene_context(draft: &str, budget: i64) -> String {
    let reg = registry();
    struct H {
        e: Entry,
        score: i64,
        via: BTreeSet<String>,
    }
    let mut hits: Vec<H> = Vec::new();
    let mut matched: HashSet<String> = HashSet::new();
    for a in &reg.order {
        let n = count_bounded(draft, a) as i64;
        if n == 0 {
            continue;
        }
        matched.insert(a.clone());
        let weight = if a.split_whitespace().count() >= 2 { 2 } else { 1 };
        for e in &reg.aliases[a] {
            let i = match hits.iter().position(|h| h.e.path == e.path) {
                Some(i) => i,
                None => {
                    hits.push(H { e: e.clone(), score: 0, via: BTreeSet::new() });
                    hits.len() - 1
                }
            };
            hits[i].score += n * weight * if is_card_section(&e.section) { 2 } else { 1 };
            hits[i].via.insert(a.clone());
        }
    }
    hits.sort_by_key(|h| std::cmp::Reverse(h.score));
    let mut out = vec![format!("# SCENE CONTEXT — {} page(s) named in the draft", hits.len())];
    if hits.is_empty() {
        out.push("no wiki page is named in this draft; if it introduces new people or places, create_character or a wiki page comes first".into());
    }
    let mut spent = chars(&out[0]);
    let mut shown = 0;
    let n = hits.len();
    let per_card = if n <= 3 { 6000 } else if n <= 8 { 3500 } else { 2200 };
    let per_page = if n <= 8 { 1800 } else { 1000 };
    let mut more = Vec::new();
    for h in &hits {
        let card = is_card_section(&h.e.section);
        let raw = read_lossy(&h.e.path);
        let (_, body) = frontmatter(&raw);
        let via = h.via.iter().cloned().collect::<Vec<_>>().join(", ");
        let loc = if h.e.url.is_empty() { rel_posix(&h.e.path, &ROOT) } else { h.e.url.clone() };
        let block = format!("\n## {}  ({}; named as {via}; {loc})\n{}\n", h.e.title, h.e.section, head_cut(body, if card { per_card } else { per_page }));
        if (spent + chars(&block)) as f64 > budget as f64 * 0.7 && shown >= 2 {
            more.push(format!("{} ({}, via {via})", h.e.title, h.e.section));
            continue;
        }
        spent += chars(&block);
        out.push(block);
        shown += 1;
    }
    if !more.is_empty() {
        out.push(format!("\n## Also named, not shown (call character / wiki for these)\n- {}", more.join("\n- ")));
    }

    // prior scenes on the same ground: three windows of the draft through the semantic index
    let len = chars(draft);
    let window = |i: usize| &draft[fwd(draft, 0, i)..fwd(draft, 0, i + 1500)];
    let mut seen: Vec<embed::Hit> = Vec::new();
    for w in [window(0), window((len / 2).saturating_sub(750)), window(len.saturating_sub(1500))] {
        if w.trim().is_empty() {
            continue;
        }
        for s in embed::search(w, "scenes", 4, 1) {
            match seen.iter().position(|x| x.path == s.path) {
                Some(i) if s.score > seen[i].score => seen[i] = s,
                Some(_) => {}
                None => seen.push(s),
            }
        }
    }
    seen.sort_by(|a, b| b.score.total_cmp(&a.score));
    if !seen.is_empty() {
        out.push("\n## Prior scenes on the same ground (scene_recall for more; check TIMELINE.md before contradicting one)".into());
        for s in seen.iter().take(5) {
            let (h, t, _) = &s.chunks[0];
            let name = Path::new(&s.path).file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
            out.push(format!("- **{}** ({name}) — [{h}] {}{}", s.title, head(t, 240).replace('\n', " "), if chars(t) > 240 { "..." } else { "" }));
        }
    }

    let struck: Vec<String> = reversion_map().iter().filter_map(|(old, new)| {
        let n = count_bounded(draft, old);
        (n > 0).then(|| format!("{old} ×{n} → {new}"))
    }).collect();
    if !struck.is_empty() {
        out.push(format!("\n## Struck Büri-register terms in the draft (the ruling is Moto in all new prose)\n- {}", struck.join("\n- ")));
    }
    let unknown = unknown_names(draft, &matched, &reg);
    if !unknown.is_empty() {
        out.push(format!("\n## Names with no page (check before writing anything numeric or canonical about them; never invent)\n- {}", unknown.join("\n- ")));
    }
    out.join("\n")
}
