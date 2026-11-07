//! The rule index: load_rules, rule, check_docket (mcp_server.py's _fmt, _select, _pack_rank).
//! Read from rules/*.yaml on every call, as the Python did, so an edit is live at once.
use crate::util::{paged, py_list, read_lossy, root};
use fancy_regex::Regex;
use serde::Deserialize;
use std::collections::BTreeSet;
use std::sync::LazyLock;

#[derive(Deserialize, Default)]
pub struct Amend {
    guide: Option<String>,
    locus: Option<String>,
    operation: Option<String>,
}

#[derive(Deserialize, Default)]
#[serde(default)]
pub struct Rule {
    pub id: String,
    pack: String,
    section: String,
    pub status: String,
    pub(crate) summary: String,
    pub(crate) verbatim: String,
    pub(crate) title: String,
    amends: Option<Vec<Amend>>,
    supersedes: Option<Vec<String>>,
    notes: Option<String>,
    applies_to: Option<Vec<String>>,
    pack_number: Option<i64>,
}

#[derive(Deserialize)]
struct Doc {
    rules: Option<Vec<Rule>>,
}

pub fn load() -> Result<Vec<Rule>, String> {
    let mut files: Vec<_> = std::fs::read_dir(root("rules"))
        .map_err(|e| e.to_string())?
        .flatten()
        .map(|e| e.path())
        .filter(|p| p.extension().is_some_and(|x| x == "yaml"))
        .collect();
    files.sort();
    let mut rows = Vec::new();
    for p in files {
        // Through serde_json::Value: its maps keep the last of a repeated key, as PyYAML does
        // (packs 1, 2, 4 and 6 each repeat one key); serde_yaml_ng's own maps refuse the file.
        let v: serde_json::Value = serde_yaml_ng::from_str(&read_lossy(&p)).map_err(|e| format!("{}: {e}", p.display()))?;
        if !v.get("rules").is_some_and(|r| !r.is_null()) {
            continue;
        }
        let doc: Doc = serde_json::from_value(v).map_err(|e| format!("{}: {e}", p.display()))?;
        rows.extend(doc.rules.unwrap_or_default());
    }
    Ok(rows)
}

pub(crate) fn vocab() -> BTreeSet<String> {
    static RX: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"(?m)^\|\s*`([a-z-]+)`").unwrap());
    let body = read_lossy(&root("schema/applies_to.md"));
    RX.captures_iter(body.as_str()).flatten().map(|c| c[1].to_string()).collect()
}

fn pack_rank(r: &Rule) -> i64 {
    static RX: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"^R(\d+)").unwrap());
    r.pack_number.unwrap_or_else(|| {
        RX.captures(r.id.as_str()).ok().flatten().and_then(|c| c[1].parse().ok()).unwrap_or(0)
    })
}

pub fn fmt(r: &Rule, full: bool) -> String {
    if !full {
        return format!("{}: {}", r.id, r.summary.trim());
    }
    let mut lines = vec![
        format!("{}  [{} {}]  {}", r.id, r.pack, r.section, r.status),
        format!("  {}", r.summary.trim()),
        format!("  > {}", r.verbatim.trim()),
    ];
    for a in r.amends.iter().flatten() {
        lines.push(format!(
            "  amends: {} {} ({})",
            a.guide.as_deref().unwrap_or("None"),
            a.locus.as_deref().unwrap_or(""),
            a.operation.as_deref().filter(|s| !s.is_empty()).unwrap_or("?")
        ));
    }
    if let Some(s) = r.supersedes.as_ref().filter(|s| !s.is_empty()) {
        lines.push(format!("  supersedes: {}", s.join(", ")));
    }
    if let Some(n) = r.notes.as_ref().filter(|s| !s.is_empty()) {
        lines.push(format!("  notes: {}", n.trim()));
    }
    lines.join("\n")
}

/// (rules matching any tag with a wanted status, newest pack first; the unknown tags; the known tags sorted)
pub(crate) fn select(tags: &[String], status: &[String]) -> Result<(Vec<Rule>, Vec<String>, Vec<String>), String> {
    let vocab = vocab();
    let bad: Vec<String> = tags.iter().filter(|t| !vocab.contains(*t)).cloned().collect();
    let want: BTreeSet<String> = tags.iter().filter(|t| vocab.contains(*t)).cloned().collect();
    let mut rules: Vec<Rule> = load()?
        .into_iter()
        .filter(|r| status.contains(&r.status))
        .filter(|r| want.is_empty() || r.applies_to.iter().flatten().any(|t| want.contains(t)))
        .collect();
    rules.sort_by(|a, b| pack_rank(b).cmp(&pack_rank(a)).then_with(|| a.id.cmp(&b.id)));
    Ok((rules, bad, want.into_iter().collect()))
}

pub fn load_rules(tags: &[String], status: Option<Vec<String>>, brief: bool, part: i64) -> Result<String, String> {
    let (rules, bad, known) = select(tags, &status.unwrap_or_else(|| vec!["live".into()]))?;
    let out: Vec<String> = rules.iter().map(|r| fmt(r, !brief)).collect();
    let sep = if brief { "\n" } else { "\n\n" };
    let mut head = format!("-- {} rules for tags {}", rules.len(), py_list(&known));
    if !bad.is_empty() {
        head += &format!("  (ignored unknown tags: {})", py_list(&bad));
    }
    let mut pages = paged(out, sep.len());
    if part == 0 && pages.len() == 1 {
        return Ok(head + "\n\n" + &pages.swap_remove(0).join(sep));
    }
    // a load with no part asked starts at part 1, so a client's size limit never silently eats the rulebook
    let p = if part == 0 { 1 } else { part };
    if p < 1 || p as usize > pages.len() {
        return Ok(format!("part {p} out of range: 1 to {}", pages.len()));
    }
    let (p, total) = (p as usize, pages.len());
    let first: usize = pages[..p - 1].iter().map(Vec::len).sum();
    head += &format!("\n-- part {p} of {total}: rules {} to {}", first + 1, first + pages[p - 1].len());
    if p < total {
        head += &format!(". Call load_rules again with the same arguments and part={} and read every part.", p + 1);
    }
    let out = pages.swap_remove(p - 1);
    Ok(head + "\n\n" + &out.join(sep))
}

pub fn rule(id: &str) -> Result<String, String> {
    Ok(load()?.iter().find(|r| r.id == id).map(|r| fmt(r, true)).unwrap_or_else(|| format!("no rule with id {id}")))
}

pub fn check_docket(tags: &[String]) -> Result<String, String> {
    let (rules, _, known) = select(tags, &["pending".into(), "proposed".into()])?;
    let out: Vec<String> = rules.iter().map(|r| fmt(r, false)).collect();
    Ok(format!("-- {} pending/proposed for {}\n\n", rules.len(), py_list(&known)) + &out.join("\n\n"))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::util::{PAGE_CHARS, chars, page_text};

    #[test]
    fn a_long_text_pages_between_lines_and_loses_nothing() {
        let text: String = (0..400).map(|i| format!("Line {i}: {}\n", "y".repeat(500))).collect();
        assert_eq!(page_text("short\n".into(), 0, "t"), "short\n");
        let first = page_text(text.clone(), 0, "natalie");
        assert_eq!(first, page_text(text.clone(), 1, "natalie"));
        assert!(first.starts_with("-- part 1 of 3. Call natalie again with the same arguments and part=2"), "{}", &first[..120]);
        let mut joined = String::new();
        for p in 1..=3 {
            let page = page_text(text.clone(), p, "natalie");
            assert!(chars(&page) < PAGE_CHARS + 200);
            joined += page.split_once("\n\n").unwrap().1;
        }
        assert_eq!(joined, text);
        assert!(page_text(text.clone(), 3, "natalie").starts_with("-- part 3 of 3.\n\n"));
        assert!(page_text(text, 9, "natalie").contains("out of range"));
    }

    #[test]
    fn pages_stay_under_the_limit_and_lose_nothing() {
        let rules: Vec<String> = (0..500).map(|i| format!("R{i}: {}", "x".repeat(600))).collect();
        let pages = paged(rules.clone(), 1);
        assert!(pages.len() > 1);
        for page in &pages {
            assert!(page.iter().map(|r| chars(r) + 1).sum::<usize>() <= PAGE_CHARS);
        }
        assert_eq!(pages.concat(), rules);
    }

    #[test]
    fn a_small_load_is_one_page() {
        assert_eq!(paged(vec!["R1: a", "R2: b"], 1).len(), 1);
        assert_eq!(paged(Vec::<String>::new(), 1).len(), 1);
    }

    #[test]
    fn the_real_rulebook_pages_fit_and_name_the_next_part() {
        let first = load_rules(&[], None, true, 0).unwrap();
        assert_eq!(first, load_rules(&[], None, true, 1).unwrap());
        assert!(first.contains("part=2 and read every part"), "{}", &first[..200]);
        assert!(chars(&first) < PAGE_CHARS + 500);
        assert!(load_rules(&[], None, true, 99).unwrap().contains("out of range"));
    }
}
