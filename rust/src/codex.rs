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
pub type Row = Vec<Option<String>>;
type Sheets = Vec<(String, Vec<Row>)>;

fn codex_path() -> PathBuf {
    crate::util::env_path("WOTR_TRUE_CANON", Some("~/wotr-vault/true-canon")).unwrap().join("The Master Codex.xlsx")
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

/// Python's repr() of a float.
fn py_float(f: f64) -> String {
    if !f.is_finite() {
        return if f.is_nan() { "nan" } else if f > 0.0 { "inf" } else { "-inf" }.into();
    }
    let e = format!("{f:e}");
    let (m, exp) = e.split_once('e').unwrap();
    let exp: i32 = exp.parse().unwrap();
    let (sign, d) = (if m.starts_with('-') { "-" } else { "" }, m.replace(['-', '.'], ""));
    if (-4..16).contains(&exp) {
        let point = exp + 1;
        if point <= 0 {
            return format!("{sign}0.{}{d}", "0".repeat(-point as usize));
        }
        let d = format!("{d:0<w$}", w = point as usize);
        let (i, f) = d.split_at(point as usize);
        return format!("{sign}{i}.{}", if f.is_empty() { "0" } else { f });
    }
    let m = if d.len() > 1 { format!("{}.{}", &d[..1], &d[1..]) } else { d };
    format!("{sign}{m}e{}{:02}", if exp < 0 { '-' } else { '+' }, exp.abs())
}

/// The <v> text of a sheet's number cells by (row, column) from 0, read from the xlsx itself: openpyxl
/// makes a number an int unless that text has a '.' or an exponent, which calamine's f64 cannot say.
fn raw_numbers(p: &std::path::Path, name: &str) -> std::collections::HashMap<(usize, usize), String> {
    use std::io::Read;
    let mut out = std::collections::HashMap::new();
    let Some(mut z) = std::fs::File::open(p).ok().and_then(|f| zip::ZipArchive::new(f).ok()) else { return out };
    let mut read = |f: &str| {
        let mut s = String::new();
        if let Ok(mut e) = z.by_name(f) {
            let _ = e.read_to_string(&mut s);
        }
        s
    };
    let attr = |tag: &str, k: &str| rx!(r#"\s([\w:]+)="([^"]*)""#).captures_iter(tag).flatten().find(|c| &c[1] == k).map(|c| c[2].to_string());
    let esc = name.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;");
    let wb = read("xl/workbook.xml");
    let Some(rid) = rx!(r"<sheet\s[^>]*>").find_iter(&wb).flatten().map(|m| m.as_str()).find(|s| attr(s, "name").as_deref() == Some(&esc)).and_then(|s| attr(s, "r:id")) else { return out };
    let rels = read("xl/_rels/workbook.xml.rels");
    let Some(target) = rx!(r"<Relationship\s[^>]*>").find_iter(&rels).flatten().map(|m| m.as_str()).find(|s| attr(s, "Id").as_deref() == Some(&rid)).and_then(|s| attr(s, "Target")) else { return out };
    let xml = read(&target.strip_prefix('/').map(String::from).unwrap_or_else(|| format!("xl/{target}")));
    for m in rx!(r"<c\s[^>]*>").find_iter(&xml).flatten() {
        let tag = m.as_str();
        if tag.ends_with("/>") || attr(tag, "t").is_some_and(|t| t != "n") {
            continue;
        }
        let body = &xml[m.end()..xml[m.end()..].find("</c>").map_or(m.end(), |i| m.end() + i)];
        let (Some(r), Some(v)) = (attr(tag, "r"), rx!(r"<v>([^<]*)</v>").captures(body).ok().flatten()) else { continue };
        let col = r.chars().take_while(char::is_ascii_alphabetic).fold(0, |a, c| a * 26 + (c as usize - 'A' as usize + 1));
        if let Ok(row) = r.trim_start_matches(|c: char| c.is_ascii_alphabetic()).parse::<usize>() {
            out.insert((row - 1, col - 1), v[1].to_string());
        }
    }
    out
}

/// One sheet of any workbook as openpyxl's read-only iter_rows(values_only=True) gives it: from row 1,
/// a number printed as Python prints the int or float openpyxl made of it.
pub fn sheet_rows(p: &std::path::Path, name: &str) -> Result<Vec<Row>, String> {
    let mut wb: Xlsx<_> = open_workbook(p).map_err(|e| format!("{}: {e}", p.display()))?;
    let range = wb.worksheet_range(name).map_err(|_| format!("KeyError: 'Worksheet {name} does not exist.'"))?;
    let raw = raw_numbers(p, name);
    let (r0, c0) = range.start().map(|(r, c)| (r as usize, c as usize)).unwrap_or((0, 0));
    let num = |r: usize, c: usize, d: &Data| match (d, raw.get(&(r, c))) {
        (Data::Float(f), Some(v)) if v.contains(['.', 'e', 'E']) => Some(py_float(*f)),
        (Data::Float(f), Some(_)) => Some(format!("{}", *f as i64)),
        _ => cell(d),
    };
    let rows = range.rows().enumerate().map(|(i, r)| std::iter::repeat_n(None, c0).chain(r.iter().enumerate().map(|(j, d)| num(r0 + i, c0 + j, d))).collect());
    Ok(std::iter::repeat_n(Row::new(), r0).chain(rows).collect())
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

#[cfg(test)]
mod tests {
    #[test]
    fn float_repr() {
        for (f, s) in [(20.0, "20.0"), (0.5, "0.5"), (-1.25, "-1.25"), (1e16, "1e+16"), (1e15, "1000000000000000.0"), (0.0001, "0.0001"), (1e-5, "1e-05"), (1.5e-7, "1.5e-07"), (0.0, "0.0"), (123456.789, "123456.789")] {
            assert_eq!(super::py_float(f), s);
        }
    }
}
