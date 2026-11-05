//! Tools that read pages: character, fow_line, natalie, natalie_gpt, list_conflicts, skill
//! (mcp_server.py, same names). Read from disk on every call so edits are live.
use crate::util::{chars, head, read_lossy, read_page, rel_posix, rglob_md, root, stem};
use fancy_regex::Regex;
use std::path::{Path, PathBuf};
use std::sync::LazyLock;

pub fn character(name: &str) -> String {
    let wiki = root("wiki");
    let key = name.to_lowercase();
    let parent = |p: &Path| p.parent().and_then(|d| d.file_name()).map(|s| s.to_string_lossy().to_lowercase()).unwrap_or_default();
    let mut cands: Vec<PathBuf> = rglob_md(&wiki)
        .into_iter()
        .filter(|p| p.file_name().is_some_and(|n| n != "INDEX.md"))
        .filter(|p| stem(p).to_lowercase().contains(&key) || parent(p).contains(&key))
        .collect();
    if cands.is_empty() {
        return format!("no card for '{name}' in the wiki mirror; check the Stat Sheet before writing anything numeric about them");
    }
    cands.sort_by_key(|p| (key != stem(p).to_lowercase(), !parent(p).contains("character"), chars(&stem(p))));
    let p = &cands[0];
    let text = read_page(p);
    let others: Vec<String> = cands[1..cands.len().min(6)].iter().map(|c| rel_posix(c, &wiki)).collect();
    let mut out = format!("# {}  ({})\n", stem(p), rel_posix(p, &wiki));
    if !others.is_empty() {
        out += &format!("also matched: {}\n", others.join("; "));
    }
    out += "\n";
    out += head(&text, 24000);
    if chars(&text) > 24000 {
        out += "\n...[truncated]";
    }
    out
}

pub fn fow_line(name: &str) -> String {
    static FIG: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\*\*(?:Level|Stage|Band|EU Reserve|Flux Density|AU/s|η|Stat line|Path|Aether Class|Essence Class|Thread Class|Soul Crystal|Coherence)\b").unwrap());
    static LBL: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\b(?:Level|Stage|Band):").unwrap());
    static SEC: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"^(#{2,3})\s+.*(?:Stats|Force and Flow|Force & Flow|Traits and Domain|Fracture of Worlds|Temperance)").unwrap());
    static ANY: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"^(#{1,6})\s").unwrap());
    let card = character(name);
    if card.starts_with("no card") {
        return card;
    }
    let lines: Vec<&str> = card.split('\n').collect();
    let (mut keep, mut grab, mut level) = (Vec::new(), false, 2);
    for ln in &lines {
        let l = ln.trim();
        let is = |r: &Regex| r.is_match(l).unwrap_or(false);
        if is(&FIG) || is(&LBL) {
            keep.push(l);
        }
        if let Some(c) = SEC.captures(l).ok().flatten() {
            grab = true;
            level = c[1].len();
            keep.push(l);
            continue;
        }
        if grab {
            match ANY.captures(l).ok().flatten() {
                Some(c) if c[1].len() <= level => grab = false,
                _ if !l.is_empty() => keep.push(l),
                _ => {}
            }
        }
    }
    let mut seen = std::collections::HashSet::new();
    let out: Vec<&str> = keep.into_iter().filter(|k| seen.insert(*k)).collect();
    if out.is_empty() {
        return format!("{}\nno FOW figures on this card; flag an estimate in a character's mouth or ask Isaac", lines[0]);
    }
    format!("{}\n{}", lines[0], head(&out.join("\n"), 12000))
}

pub fn natalie(section: &str) -> String {
    let gpt = root("desktop/NATALIE.gpt.md");
    let s = section.trim().to_lowercase();
    if s == "chatgpt" || s == "gpt" {
        return read_lossy(&gpt);
    }
    let text = read_lossy(&root("desktop/NATALIE.md"));
    if s.is_empty() {
        if !gpt.exists() {
            return text;
        }
        return text
            + "\n\n---\n\n# FOR CHATGPT SESSIONS: NATALIE.gpt.md\n\nClaude sessions skip everything from here to the end. A GPT model reads all of it now: it is your overlay on everything above, and its last section is the worked example of the prose Isaac wants.\n\n"
            + &read_lossy(&gpt);
    }
    // re.split(r"(?m)^(?=#{1,3} )", text): cut before every line that opens with 1-3 '#' and a space
    let is_head = |l: &str| {
        let n = l.bytes().take_while(|b| *b == b'#').count();
        (1..=3).contains(&n) && l.as_bytes().get(n) == Some(&b' ')
    };
    let mut cuts = vec![0];
    let mut pos = 0;
    for line in text.split_inclusive('\n') {
        if is_head(line) {
            // a heading on the first line cuts at 0 too, giving Python's leading '' part
            cuts.push(pos);
        }
        pos += line.len();
    }
    cuts.push(text.len());
    let parts: Vec<&str> = cuts.windows(2).map(|w| &text[w[0]..w[1]]).collect();
    let first_line = |p: &str| p.split('\n').next().unwrap_or("").to_string();
    let want = section.to_lowercase();
    let hits: Vec<&str> = parts.iter().copied().filter(|p| first_line(p).to_lowercase().contains(&want)).collect();
    if !hits.is_empty() {
        return hits.join("\n");
    }
    let heads: Vec<String> = parts.iter().filter(|p| p.starts_with('#')).map(|p| first_line(p)).collect();
    format!("no heading matches '{section}'. Headings:\n{}", heads.join("\n"))
}

pub fn natalie_gpt() -> String {
    read_lossy(&root("desktop/NATALIE.gpt.md"))
}

pub fn list_conflicts() -> String {
    read_lossy(&root("CONFLICTS.md"))
}

/// name -> (description, body) for every served skill, in directory order.
pub fn skills(hide: &[String]) -> Vec<(String, String, String)> {
    let dir = root(".claude/skills");
    let mut names: Vec<String> = std::fs::read_dir(&dir)
        .into_iter()
        .flatten()
        .flatten()
        .filter(|e| e.path().join("SKILL.md").is_file())
        .map(|e| e.file_name().to_string_lossy().into_owned())
        .filter(|n| !hide.contains(n))
        .collect();
    names.sort();
    names
        .into_iter()
        .filter_map(|n| {
            let text = read_lossy(&dir.join(&n).join("SKILL.md"));
            let mut it = text.splitn(3, "---");
            let (_, front, body) = (it.next()?, it.next()?, it.next()?);
            let meta: serde_yaml_ng::Value = serde_yaml_ng::from_str(front).unwrap_or_default();
            let desc = meta.get("description").and_then(|d| d.as_str()).unwrap_or("").to_string();
            Some((n, desc, body.trim().to_string()))
        })
        .collect()
}

pub fn skill(name: &str, file: &str, hide: &[String], note: &str) -> String {
    let all = skills(hide);
    if name.is_empty() {
        return all.iter().map(|(n, d, _)| format!("- {n}: {d}")).collect::<Vec<_>>().join("\n");
    }
    let Some((_, _, body)) = all.iter().find(|(n, _, _)| n == name) else {
        return format!("no skill '{name}'; skill() lists them");
    };
    let dir = root(".claude/skills").join(name).canonicalize().unwrap_or_default();
    if file.is_empty() {
        let mut refs: Vec<String> = rglob_md(&dir).iter().filter(|p| p.file_name().is_some_and(|n| n != "SKILL.md")).map(|p| rel_posix(p, &dir)).collect();
        refs.sort();
        let foot = if refs.is_empty() { String::new() } else { format!("\n\nReference files: {}", refs.join(", ")) };
        return format!("{note}{body}{foot}");
    }
    match dir.join(file).canonicalize() {
        Ok(t) if t.starts_with(&dir) && t != dir && t.extension().is_some_and(|x| x == "md") && t.is_file() => read_lossy(&t),
        _ => format!("no file '{file}' in {name}; skill('{name}') lists its reference files"),
    }
}
