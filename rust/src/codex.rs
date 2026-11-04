//! codex and codex_check (build/codex.py find/check): The Master Codex read from the xlsx with
//! calamine, cells as openpyxl gives them (str, int or None), cached by the file's mtime.
use crate::util::chars;
use calamine::{Data, Reader, Xlsx, open_workbook};
use fancy_regex::Regex;
use std::collections::BTreeSet;
use std::path::PathBuf;
use std::sync::{Arc, LazyLock, Mutex};
use std::time::SystemTime;

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

/// A row: column A first (openpyxl's iter_rows starts at column 1), None for an empty cell.
type Row = Vec<Option<String>>;
type Sheets = Vec<(String, Vec<Row>)>;

fn codex_path() -> PathBuf {
    let home = std::env::var("HOME").unwrap_or_default();
    let raw = std::env::var("WOTR_TRUE_CANON").ok().filter(|v| !v.is_empty()).or_else(|| {
        let env = std::fs::read_to_string(format!("{home}/.config/wotr/env")).unwrap_or_default();
        env.lines().filter_map(|l| l.trim().strip_prefix("WOTR_TRUE_CANON=")).map(|v| v.trim().trim_matches(|c| c == '"' || c == '\'').to_string()).find(|v| !v.is_empty())
    });
    let raw = raw.unwrap_or_else(|| "~/wotr-vault/true-canon".into());
    let raw = if raw == "~" || raw.starts_with("~/") { format!("{home}{}", &raw[1..]) } else { raw };
    PathBuf::from(raw).join("The Master Codex.xlsx")
}

fn cell(d: &Data) -> Option<String> {
    match d {
        Data::Empty => None,
        Data::String(s) => Some(s.clone()),
        Data::Float(f) if f.fract() == 0.0 && f.abs() < 1e15 => Some(format!("{}", *f as i64)),
        Data::Float(f) => Some(f.to_string()),
        Data::Int(i) => Some(i.to_string()),
        Data::Bool(b) => Some(if *b { "True" } else { "False" }.into()),
        other => Some(other.to_string()),
    }
}

fn empty(c: &Option<String>) -> bool {
    c.as_deref().is_none_or(str::is_empty)
}

fn sheets() -> Result<Arc<Sheets>, String> {
    static CACHE: Mutex<Option<(SystemTime, Arc<Sheets>)>> = Mutex::new(None);
    let p = codex_path();
    let mtime = std::fs::metadata(&p).and_then(|m| m.modified()).map_err(|e| format!("FileNotFoundError: {e}: '{}'", p.display()))?;
    let mut c = CACHE.lock().unwrap();
    if let Some((_, s)) = c.as_ref().filter(|(t, _)| *t == mtime) {
        return Ok(s.clone());
    }
    let mut wb: Xlsx<_> = open_workbook(&p).map_err(|e| format!("{}: {e}", p.display()))?;
    let mut out = Vec::new();
    for name in wb.sheet_names() {
        let range = wb.worksheet_range(&name).map_err(|e| e.to_string())?;
        let lead = range.start().map(|(_, c)| c as usize).unwrap_or(0);
        let rows = range
            .rows()
            .map(|r| std::iter::repeat_n(None, lead).chain(r.iter().map(cell)).collect::<Row>())
            .filter(|r| r.iter().any(|c| !empty(c)))
            .collect();
        out.push((name, rows));
    }
    let s = Arc::new(out);
    *c = Some((mtime, s.clone()));
    Ok(s)
}

fn at(r: &Row, i: usize) -> Option<&str> {
    r.get(i).and_then(|c| c.as_deref()).filter(|s| !s.is_empty())
}

fn sheet<'a>(s: &'a Sheets, name: &str) -> Result<&'a [Row], String> {
    s.iter().find(|(n, _)| n == name).map(|(_, r)| r.as_slice()).ok_or_else(|| format!("KeyError: '{name}'"))
}

fn row_md(hdr: &Row, r: &Row) -> String {
    hdr.iter()
        .zip(r)
        .filter(|(h, v)| !empty(h) && !empty(v))
        .map(|(h, v)| format!("- **{}:** {}", h.as_deref().unwrap(), v.as_deref().unwrap()))
        .collect::<Vec<_>>()
        .join("\n")
}

pub fn find(query: &str, sheet_name: &str, limit: i64) -> Result<String, String> {
    let q = query.trim().to_lowercase();
    if q.is_empty() {
        return Ok("(empty query)".into());
    }
    let s = sheets()?;
    let mut hits = Vec::new();
    for (name, rows) in s.iter() {
        if !sheet_name.is_empty() && name.to_lowercase() != sheet_name.to_lowercase() {
            continue;
        }
        let Some(hdr) = rows.first() else { continue };
        for r in &rows[1..] {
            let cells: Vec<String> = r.iter().filter(|c| !empty(c)).map(|c| c.as_deref().unwrap().to_lowercase()).collect();
            if !cells.iter().any(|c| c.contains(&q)) {
                continue;
            }
            let exact = cells.iter().take(2).any(|c| *c == q || *c == format!("[{q}]"));
            hits.push((!exact, name.as_str(), hdr, r));
        }
    }
    let names: Vec<&str> = s.iter().map(|(n, _)| n.as_str()).collect();
    if hits.is_empty() {
        let within = if sheet_name.is_empty() { String::new() } else { format!(" in {sheet_name}") };
        return Ok(format!("No Codex row mentions '{query}'{within}. Sheets: {}.", names.join(", ")));
    }
    hits.sort_by_key(|h| h.0);
    let n = hits.len() as i64;
    let mut out = vec![format!(
        "{n} Codex row(s) for '{query}'{} (from The Master Codex.xlsx):",
        if n > limit { format!(", first {limit}") } else { String::new() }
    )];
    // Python's hits[:limit]: a negative limit counts from the end
    let take = if limit < 0 { (n + limit).max(0) } else { limit.min(n) } as usize;
    for (_, name, hdr, r) in &hits[..take] {
        let title = match at(r, 1) {
            Some(t) if *name != "Lists" => t.to_string(),
            _ => r.iter().filter(|c| !empty(c)).map(|c| c.as_deref().unwrap()).find(|c| c.to_lowercase().contains(&q)).unwrap().to_string(),
        };
        out.push(format!("\n### {name}: {title}\n{}", row_md(hdr, r)));
    }
    Ok(out.join("\n"))
}

fn word(t: &str) -> Regex {
    Regex::new(&format!(r"\b{}\b", fancy_regex::escape(t))).unwrap()
}

pub fn check(text: &str) -> Result<String, String> {
    const RULED: [(&str, &str); 1] = [("Crymorath", "Cymorath")];
    const STOP: [&str; 4] = ["Ratio", "Station", "Nation", "Aeon"];
    let body = match rx!(r"(?m)^#{2,3} (?:Notes|Author|Added by the gap-fill)").find(text).ok().flatten() {
        Some(m) => &text[..m.start()],
        None => text,
    };
    let proposed = body.lines().filter(|l| rx!(r"(?i)\bproposed\b").is_match(l).unwrap_or(false)).collect::<Vec<_>>().join(" ");
    let s = sheets()?;
    let lists = sheet(&s, "Lists")?;
    let mut known: BTreeSet<String> = BTreeSet::new();
    if let Some(hdr) = lists.first() {
        for (i, h) in hdr.iter().enumerate() {
            if empty(h) {
                continue;
            }
            known.extend(lists[1..].iter().filter_map(|r| at(r, i)).map(|v| v.trim().to_string()));
        }
    }
    let glyphs: std::collections::HashMap<String, String> = sheet(&s, "Master Glyph Index")?
        .iter()
        .skip(1)
        .filter_map(|r| at(r, 0).map(|g| (g.trim().to_string(), at(r, 1).unwrap_or("").trim().to_string())))
        .collect();
    known.extend(glyphs.values().cloned());
    for (w, canon) in RULED {
        known.remove(w);
        known.insert(canon.to_string());
    }
    let (mut out, mut fails) = (Vec::new(), 0);
    let used: Vec<&String> = known.iter().filter(|t| chars(t) > 3 && body.contains(t.as_str()) && word(t).is_match(body).unwrap_or(false)).collect();
    let unknown: BTreeSet<&str> = rx!(r"\b[A-Z][a-zé]+(?:atio|antia|orath|ivale|thrae|ilithe|aeon)\b")
        .find_iter(body)
        .flatten()
        .map(|m| m.as_str())
        .filter(|w| !known.contains(*w) && !STOP.contains(w) && !proposed.contains(w))
        .collect();
    let ruled: Vec<(&str, &str)> = RULED.iter().copied().filter(|(w, _)| word(w).is_match(body).unwrap_or(false)).collect();
    if !ruled.is_empty() {
        fails += 1;
        out.push(format!("FAIL 37 ruled spelling (RULINGS.md): {}.", ruled.iter().map(|(w, c)| format!("{w} is {c}")).collect::<Vec<_>>().join(", ")));
    }
    let unknown: Vec<&str> = unknown.into_iter().filter(|w| !RULED.iter().any(|(r, _)| r == w)).collect();
    if !unknown.is_empty() {
        fails += 1;
        out.push(format!(
            "FAIL 37 controlled vocabulary (R18-7-CHECK37): not on the Lists sheet: {}. Correct the term or declare it proposed and name the enumeration checked.",
            unknown.join(", ")
        ));
    } else {
        let shown = if used.is_empty() { String::new() } else { format!(" ({})", used.iter().take(12).map(|s| s.as_str()).collect::<Vec<_>>().join(", ")) };
        out.push(format!("PASS 37 controlled vocabulary: {} Lists term(s) used{shown}", used.len()));
    }
    let toks: BTreeSet<String> = rx!(r"\[([A-Z][A-Za-z']{0,5})\](?!\()").captures_iter(body).flatten().map(|c| format!("[{}]", &c[1])).collect();
    let bad: Vec<&str> = toks.iter().filter(|t| !glyphs.contains_key(t.as_str())).map(String::as_str).collect();
    if toks.is_empty() {
        out.push("WARN 38 glyph validity: no bracketed glyph tokens in the body".into());
    } else if !bad.is_empty() {
        fails += 1;
        out.push(format!("FAIL 38 glyph validity (R18-7-CHECK38): unknown to the Master Glyph Index: {}", bad.join(", ")));
    } else {
        out.push(format!("PASS 38 glyph validity: {} token(s), all in the Master Glyph Index", toks.len()));
    }
    let spells: BTreeSet<&str> = sheet(&s, "Spell Index")?.iter().skip(1).filter_map(|r| at(r, 1)).filter(|n| body.contains(n)).collect();
    out.push(format!(
        "WARN 39 precedent (R18-7-CHECK39, manual): {}Name the Spell Index rows checked and say new, derivation of a named row, or duplicate.",
        if spells.is_empty() { String::new() } else { format!("Spell Index rows named: {}. ", spells.into_iter().collect::<Vec<_>>().join(", ")) }
    ));
    out.push(if fails == 0 { "CLEAN".into() } else { format!("{fails} FAIL") });
    Ok(out.join("\n"))
}
