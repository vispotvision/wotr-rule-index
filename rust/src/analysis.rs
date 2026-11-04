//! stale_names, scene_brief, gap_fill, trello_cards, scene_text (mcp_server.py, with
//! audio_export.py's scene_blocks/clean_inline/plain_text/cast_path) and timeline, reconcile,
//! pack_impact (build/audit.py with its report()), ported line for line.
use crate::util::{chars, head, read_lossy, read_page, rel_posix, rglob_md, root, stem, ROOT};
use crate::{pages, rules, search, verify, writers};
use fancy_regex::Regex;
use serde_json::Value;
use std::collections::{BTreeSet, HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::sync::LazyLock;

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

fn name_of(p: &Path) -> String {
    p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default()
}

fn count(r: &Regex, s: &str) -> usize {
    r.find_iter(s).flatten().count()
}

fn is(r: &Regex, s: &str) -> bool {
    r.is_match(s).unwrap_or(false)
}

/// sorted(dir.glob("*.md")) as Paths sort on POSIX: by the path string.
fn md_files(dir: &Path) -> Vec<PathBuf> {
    let mut v: Vec<PathBuf> = std::fs::read_dir(dir).into_iter().flatten().flatten().map(|e| e.path()).filter(|p| name_of(p).ends_with(".md")).collect();
    v.sort();
    v
}

/// Counter.most_common(n) rendered as "k×v, ...": count descending, ties in first-seen order.
fn most_common(items: impl Iterator<Item = String>, n: usize) -> String {
    let mut c: Vec<(String, usize)> = Vec::new();
    for k in items {
        match c.iter_mut().find(|e| e.0 == k) {
            Some(e) => e.1 += 1,
            None => c.push((k, 1)),
        }
    }
    c.sort_by_key(|e| std::cmp::Reverse(e.1));
    let s: Vec<String> = c.iter().take(n).map(|(k, v)| format!("{k}\u{d7}{v}")).collect();
    if s.is_empty() { "none".into() } else { s.join(", ") }
}

// ---------------------------------------------------------------- stale_names
pub fn stale_names(scope: &str, max_files: i64) -> String {
    let (wiki, scenes) = (root("wiki"), root("scenes"));
    let roots = match scope {
        "wiki" => vec![wiki],
        "scenes" => vec![scenes],
        _ => vec![wiki, scenes],
    };
    let pairs = search::reversion_map();
    let rxs: HashMap<&str, Regex> =
        pairs.iter().map(|(o, _)| (o.as_str(), Regex::new(&format!(r"(?<![\w\-]){}(?![\w\-])", fancy_regex::escape(o))).unwrap())).collect();
    let mut gov: HashMap<&str, &str> = HashMap::new();
    for (o, n) in &pairs {
        gov.insert(o, n);
    }
    let mut results = Vec::new();
    let mut total = 0;
    for r in &roots {
        for p in rglob_md(r) {
            if ["INDEX.md", "MANIFEST.md", "CAST.md", "ARCS.md"].contains(&name_of(&p).as_str()) {
                continue;
            }
            let text = read_page(&p);
            let mut found: Vec<(&str, usize)> = Vec::new();
            for (old, _) in &pairs {
                if !text.contains(old.as_str()) || found.iter().any(|f| f.0 == old) {
                    continue;
                }
                let n = count(&rxs[old.as_str()], &text);
                if n > 0 {
                    found.push((old, n));
                }
            }
            if !found.is_empty() {
                let lines: Vec<String> = text.split('\n').filter(|ln| found.iter().any(|(o, _)| is(&rxs[o], ln))).take(3).map(String::from).collect();
                let cnt: usize = found.iter().map(|f| f.1).sum();
                total += cnt;
                results.push((cnt, rel_posix(&p, &ROOT), found, lines));
            }
        }
    }
    results.sort_by_key(|r| std::cmp::Reverse(r.0));
    let mut out = vec![format!(
        "{} files still carry Büri-register terms ({total} hits) in {scope}. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.",
        results.len()
    )];
    let take = if max_files < 0 { (results.len() as i64 + max_files).max(0) as usize } else { max_files as usize };
    for (cnt, rel, found, lines) in results.iter_mut().take(take) {
        found.sort_by_key(|f| std::cmp::Reverse(f.1));
        let terms: Vec<String> = found.iter().map(|(o, n)| format!("{o}\u{d7}{n} [{}]", gov.get(o).copied().unwrap_or("?"))).collect();
        out.push(format!("\n{rel}  ({cnt})\n  {}", terms.join(", ")));
        for ln in lines.iter() {
            out.push(format!("    > {}", head(ln.trim(), 140)));
        }
    }
    if results.len() as i64 > max_files {
        out.push(format!("\n... {} more files", results.len() as i64 - max_files));
    }
    out.join("\n")
}

// ---------------------------------------------------------------- scene_brief
const LOADOUTS: &[(&str, &[&str])] = &[
    ("duel", &["prose-law", "combat", "adjudication", "magic-mechanism", "pov"]),
    ("battle", &["prose-law", "mass-combat", "adjudication", "pov", "scene-structure"]),
    ("talky", &["prose-law", "dialogue", "register", "pov", "naming"]),
    ("quiet", &["prose-law", "pov", "scene-structure", "standing-inventory", "register"]),
    ("explicit", &["prose-law", "dialogue", "pov", "scene-structure"]),
    ("working", &["prose-law", "magic-mechanism", "combat", "codex"]),
    ("standard", &["prose-law", "pov", "scene-structure", "dialogue", "register"]),
];

pub fn scene_brief(beat: &str, thread: &str, scene_type: &str, characters: &[String]) -> Result<String, String> {
    let tags: Vec<String> = LOADOUTS.iter().find(|(k, _)| *k == scene_type).unwrap_or(&LOADOUTS[6]).1.iter().map(|s| s.to_string()).collect();
    let (live, _, _) = rules::select(&tags, &["live".into()])?;
    let (pend, _, _) = rules::select(&tags, &["pending".into(), "proposed".into()])?;
    let fow: Vec<String> = characters.iter().map(|c| pages::fow_line(c).split('\n').take(12).collect::<Vec<_>>().join("\n")).collect();
    let mut lines: Vec<String> = vec![
        format!("# SCENE BRIEF \u{2014} {scene_type}{}", if thread.is_empty() { String::new() } else { format!(" \u{2014} {thread}") }),
        format!("Beat: {}", beat.trim()),
        String::new(),
        "## Fill before drafting (author notes)".into(),
        "1. POV: ____  (write from whoever knows least about what is coming, R5-C1-WRITE_FROM_LEAST_KNOWING; a default, breakable with reason)".into(),
        "2. This POV knows: ____ | wrongly believes: ____ | the reader knows that they do not: ____  (R5-C1-INFO_TRACKED_PER_POV)".into(),
        "3. What it costs, specific and visible (reserve, body, debt, renown, who saw): ____  (Table Rule 5; R12-1-PACK_SEVEN_SURVIVORS)".into(),
        "4. Closes on: ____  (a chapter or arc on a hook; a scene on any concrete close, a pressing question included; a turn at his next real decision: a risk, a bargain, a fight, a line that matters. R79-1, R79-4)".into(),
        "5. Length: no word count; as long as the beat needs (R80-11)".into(),
        "6. Each named practitioner's kit, read from character(name) once per scene: Traits, techniques, skills by name, with cost and limit. NPCs reach for theirs unprompted and inventively, fresh uses derived from the mechanism and inside its limits; his PC may get inventive new uses of his own abilities, while new techniques, Level points and card changes stay Isaac's (R79-1, 2026-10-17 refinement): ____".into(),
    ];
    if scene_type == "duel" || scene_type == "working" {
        lines.extend([
            "7. Each fighter's combat vocabulary, assigned before the technique (Blade / Verdict / Percussion / Expenditure): ____  (R1-1-THREE_VOCABULARIES_RULING)",
            "8. The read: what evidence the POV gets, over which exchanges, shown as behaviour, before anything kills; the fight has a findable way out (R12-3-COMBAT_EXCHANGE_OWES, R71-8, R79-6): ____",
            "9. The working's one clear causal line at first display, in a mouth or narration; the full mechanism is on the page in roleplay and set piece alike (R79-6): ____",
            "10. Stat that decides each contested action, by row (R14-3-STATS_DECIDE_TABLE, R14-3-TRACEABILITY): ____",
        ].map(String::from));
    }
    if scene_type == "battle" {
        lines.push("7. The lead keeps POV through the battle and may break through or vow mid-fight; the Single Act, name-three and the aftermath stages are optional tools (R79-6): which, if any ____".into());
    }
    if !fow.is_empty() {
        lines.extend([String::new(), "## FOW lines (never invent a number)".into()]);
        for block in fow {
            lines.extend([block, String::new()]);
        }
    }
    lines.extend([String::new(), format!("## Rule loadout ({}) \u{2014} {} live, brief; call load_rules for full text", tags.join(" "), live.len()), String::new()]);
    lines.extend(live.iter().take(60).map(|r| rules::fmt(r, false)));
    if live.len() > 60 {
        lines.push(format!("... {} more; load_rules gives all of them", live.len() - 60));
    }
    lines.extend([
        String::new(),
        format!("## Unratified for these tags: {} (check_docket before writing if one would change the scene)", pend.len()),
        String::new(),
        "Then: draft \u{2192} verify_scene once (fix every FAIL, read the WARNs) \u{2192} post \u{2192} archive_scene when finished (R79-2).".into(),
    ]);
    Ok(lines.join("\n"))
}

// ---------------------------------------------------------------- gap_fill
pub fn gap_fill(md: &str) -> Result<String, String> {
    let sci = rx!(r"(?i)\b(?:pressure differential|gradient|latent heat|phase transition|dielectric|resonance|cavitation|nucleation|entropy|boundary condition|conduction|impedance|friction|momentum|torque|shear|tensile|viscosity|oxidation|combustion|frequency|amplitude|wavelength|density|saturation|diffusion|sintering|spectroscopy|refraction|inertia|kinetic|potential energy|joule|newton|pascal|kelvin|hertz)\b");
    let aether = rx!(r"\b(?:Aether(?:ic)?|Aetheric Density|Residue|Saturation|standpipe|district main|draw)\b");
    let wellspring = rx!(r"\b(?:Wellspring|Family|Physics Domain|glyph|Core Law|Category)\b");
    let essence = rx!(r"\b(?:Essence|Soul Crystal|Essence Core|Aether Shell|Attraction Layer|EU|eta|η|Flux Density|Crystal State|reserve)\b");
    let causal = rx!(r"(?i)\b(?:because|so that|which meant|which is why|therefore|since|as a result|so the|so it|hence)\b");
    let mech = rx!(r"\b(?:coupling|phase-lock|phase lock|resonan\w+|harmonis\w+|harmoniz\w+|conduit|lattice|Attraction|Obsession|Sovereignty|Penetration|Coherence)\b");
    let hit = rx!(r"(?i)\b(?:strike|struck|cut|thrust|parr|blocked|closed|drew|swung|hit)\w*\b");
    let paras: Vec<&str> = rx!(r"\n\s*\n").split(md).flatten().filter(|p| !p.trim().is_empty() && !p.trim().starts_with('#')).collect();
    let exchanges = paras.iter().filter(|p| is(verify::blade_action(), p) || is(hit, p)).count();
    let sci = most_common(sci.find_iter(md).flatten().map(|m| m.as_str().to_lowercase()), 8);
    let mech = most_common(mech.find_iter(md).flatten().map(|m| m.as_str().to_string()), 8);
    let (anat, blade) = (count(verify::anatomy(), md), count(verify::blade_action(), md));
    let prose = verify::run(md, &verify::Opts { combat: true, ..Default::default() })?;
    let out = [
        "# Gap-fill pass (Thirteen \u{a7}5)".to_string(),
        String::new(),
        format!("1. BEAT INVENTORY \u{2014} {} paragraphs, {exchanges} carry a physical exchange. List each exchange as read \u{2192} fault \u{2192} counter \u{2192} cost; any exchange missing one of the four is a gap (R12-3-COMBAT_EXCHANGE_OWES).", paras.len()),
        format!("2. LOGIC AUDIT \u{2014} {} causal connectives in the text (check 24 fails a fight passage with none). For every outcome: which stat row decided it (R14-3-TRACEABILITY)? Name the row in the author notes.", count(causal, md)),
        format!("3. STRATUM AUDIT \u{2014} mentions: Aether {}, Wellspring {}, Essence {}. The page owes one clear causal line at first display; the full three-strata account lives on the card and in the notes (R79-6, superseding R13-2-THREE_STRATA_MANDATE).", count(aether, md), count(wellspring, md), count(essence, md)),
        format!("4. PHYSICS AUDIT \u{2014} real-science terms present: {sci}. Each Wellspring law is stated as the real law with a directional operator (R13-2-STRATUM_TWO_WELLSPRING)."),
        format!("5. BODY AUDIT \u{2014} {anat} anatomy/injury terms, {blade} blade body/action terms (R80-4). Every blow is body, path, target, result and cost; wounds plain and anime on the page, clinical names and ATLS class in the notes and a medic's mouth; the POV's own body on the page. Roleplay fights show the full mechanism like a set piece; figures live in mouths, never narration (R79-6)."),
        "6. PHENOMENON AUDIT \u{2014} for each working: the real phenomenon it runs on, its Physics Domain and Wellspring, Category and alignment tag, and the fault the mechanism creates (R13-3-PHENOMENON_MANDATE). Write the line in the author notes if the text does not carry it.".into(),
        format!("7. VOCABULARY PASS \u{2014} Mechanism Vocabulary present: {mech}. Show the effect first, then name it; system and science terms are free in narration (R78-3, amending R13-9-STYLE_DIRECTIVE_MECHANISM_VOCAB)."),
        "8. PROSE PASS (last) \u{2014}".into(),
        verify::report(&prose),
        String::new(),
        "Log what the pass added under 'Added by the gap-fill pass' in the author notes (R13-5-GAP_FILL_PASS). The pass may change an outcome when no cause fits, and says so (R13-D, ruled 2026-09-12).".into(),
    ];
    Ok(out.join("\n"))
}

// ---------------------------------------------------------------- trello_cards
/// str() of a JSON value as the Python would print it.
fn pystr(v: &Value) -> String {
    match v {
        Value::String(s) => s.clone(),
        Value::Null => "None".into(),
        Value::Bool(b) => if *b { "True" } else { "False" }.into(),
        other => other.to_string(),
    }
}

fn truthy(v: Option<&Value>) -> bool {
    match v {
        None | Some(Value::Null) | Some(Value::Bool(false)) => false,
        Some(Value::Number(n)) => n.as_f64() != Some(0.0),
        Some(Value::String(s)) => !s.is_empty(),
        Some(Value::Array(a)) => !a.is_empty(),
        Some(Value::Object(o)) => !o.is_empty(),
        _ => true,
    }
}

struct Card {
    name: String,
    list: String,
    desc: String,
    labels: Vec<String>,
}

fn get_s(o: &Value, k: &str) -> String {
    o.get(k).map(pystr).unwrap_or_default()
}

fn label_names(c: &Value) -> Vec<String> {
    c.get("labels").and_then(Value::as_array).map(|a| a.iter().map(|l| get_s(l, "name")).collect()).unwrap_or_default()
}

fn trello(obj: &Value) -> Vec<Card> {
    match obj {
        Value::Object(o) if o.contains_key("cards") => {
            let lists: Vec<(&Value, String)> = obj.get("lists").and_then(Value::as_array).map(|a| a.iter().map(|l| (&l["id"], get_s(l, "name"))).collect()).unwrap_or_default();
            obj["cards"]
                .as_array()
                .into_iter()
                .flatten()
                .filter(|c| !truthy(c.get("closed")))
                .map(|c| Card {
                    name: get_s(c, "name"),
                    list: c.get("idList").and_then(|id| lists.iter().rev().find(|(k, _)| *k == id)).map(|(_, n)| n.clone()).unwrap_or_default(),
                    desc: get_s(c, "desc"),
                    labels: label_names(c),
                })
                .collect()
        }
        Value::Array(a) => a
            .iter()
            .filter(|c| c.is_object())
            .map(|c| Card { name: get_s(c, "name"), list: String::new(), desc: get_s(c, "desc"), labels: label_names(c) })
            .collect(),
        Value::Object(_) => {
            let desc = obj.get("desc").or_else(|| obj.get("description")).map(pystr).unwrap_or_default();
            vec![Card { name: get_s(obj, "name"), list: String::new(), desc, labels: vec![] }]
        }
        _ => vec![],
    }
}

pub fn trello_cards(json_path: &str, list_name: &str, query: &str) -> Result<String, String> {
    let p = Path::new(json_path);
    if !p.exists() {
        return Ok(format!("no file at {json_path}"));
    }
    let v: Value = serde_json::from_str(&read_lossy(p)).map_err(|e| format!("JSONDecodeError: {e}"))?;
    let mut cards = trello(&v);
    if !list_name.is_empty() {
        cards.retain(|c| c.list.to_lowercase().contains(&list_name.to_lowercase()));
    }
    if !query.is_empty() {
        cards.retain(|c| format!("{}{}", c.name, c.desc).to_lowercase().contains(&query.to_lowercase()));
    }
    let mut out = vec![format!("{} cards{}", cards.len(), if list_name.is_empty() { String::new() } else { format!(" in list '{list_name}'") })];
    for c in cards.iter().take(200) {
        let labels = if c.labels.is_empty() { String::new() } else { format!("  labels: {}", c.labels.join(", ")) };
        out.push(format!("- {}  [{}]  {} words{labels}", c.name, c.list, c.desc.split_whitespace().count()));
    }
    Ok(out.join("\n"))
}

// ---------------------------------------------------------------- scene_text
/// mcp_server._scene_files: (path, title) for every scene in scenes/.
fn scene_files() -> Vec<(PathBuf, String)> {
    md_files(&root("scenes"))
        .into_iter()
        .filter(|p| {
            let n = name_of(p);
            !n.to_uppercase().contains("SUPERSEDED") && !["MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md"].contains(&n.as_str())
        })
        .map(|p| {
            let text = read_lossy(&p);
            let t = rx!(r"(?m)^#\s+(.+?)\s*$").captures(head(&text, 600)).ok().flatten().map(|c| c[1].trim().trim_matches('*').to_string());
            let t = t.unwrap_or_else(|| stem(&p));
            (p, t)
        })
        .collect()
}

fn find_scene(query: &str) -> (Option<PathBuf>, Vec<String>) {
    let q = query.trim().to_lowercase();
    let files = scene_files();
    if let Some((p, _)) = files.iter().find(|(p, t)| name_of(p).to_lowercase() == q || stem(p).to_lowercase() == q || t.to_lowercase() == q) {
        return (Some(p.clone()), vec![]);
    }
    let loose: Vec<&(PathBuf, String)> = files.iter().filter(|(p, t)| name_of(p).to_lowercase().contains(&q) || t.to_lowercase().contains(&q)).collect();
    if loose.len() == 1 {
        return (Some(loose[0].0.clone()), vec![]);
    }
    (None, loose.iter().take(12).map(|(p, t)| format!("{} \u{2014} {t}", name_of(p))).collect())
}

/// audio_export.clean_inline
fn clean_inline(s: &str) -> String {
    let s = rx!(r"!\[[^\]]*\]\([^)]*\)").replace_all(s, "");
    let s = rx!(r"\[([^\]]+)\]\([^)]*\)").replace_all(&s, "${1}");
    let s = rx!(r"`([^`]+)`").replace_all(&s, "${1}");
    let s = rx!(r"\*\*(.+?)\*\*").replace_all(&s, "${1}");
    let s = rx!(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)").replace_all(&s, "${1}");
    let s = rx!(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)").replace_all(&s, "${1}");
    let s = s.replace('⁂', "").replace('§', "section ");
    rx!(r"\s+").replace_all(&s, " ").trim().to_string()
}

/// audio_export.scene_blocks: ("title" | "para" | "divider", text)
fn scene_blocks(md: &str) -> Vec<(&'static str, String)> {
    let mut md = md.replace("\r\n", "\n");
    if md.starts_with("---\n") {
        if let Some(end) = md[4..].find("\n---\n") {
            md = md[4 + end + 5..].to_string();
        }
    }
    if let Some(m) = rx!(r"(?m)^##\s+Notes\b.*$|^##\s+Author.*$|^---\s*\n\s*\*?Author").find(&md).ok().flatten() {
        md.truncate(m.start());
    }
    let mut blocks: Vec<(&'static str, String)> = Vec::new();
    for raw in rx!(r"\n\s*\n").split(&md).flatten() {
        let mut b = raw.trim().to_string();
        if b.is_empty() {
            continue;
        }
        if is(rx!(r"^(-{3,}|\*{3,}|_{3,})\z"), &b) {
            blocks.push(("divider", String::new()));
            continue;
        }
        if let Some(h) = rx!(r"^(#{1,6})\s+(.*)\z").captures(b.as_str()).ok().flatten() {
            let kind = if h[1].len() == 1 && !blocks.iter().any(|(k, _)| *k == "title") { "title" } else { "para" };
            blocks.push((kind, clean_inline(&h[2])));
            continue;
        }
        if b.starts_with('>') {
            b = b.split('\n').map(|l| l.trim_start_matches(['>', ' ']).trim()).collect::<Vec<_>>().join(" ");
        }
        if is(rx!(r"^[-*]\s"), &b) {
            b = b.split('\n').filter(|l| !l.trim().is_empty()).map(|l| rx!(r"^[-*]\s+").replace(l.trim(), "").into_owned()).collect::<Vec<_>>().join(" ");
        }
        let text = clean_inline(&b.replace('\n', " "));
        if !text.is_empty() {
            blocks.push(("para", text));
        }
    }
    blocks
}

pub fn scene_text(scene: &str) -> String {
    let (path, cands) = find_scene(scene);
    let Some(path) = path else {
        return if cands.is_empty() { format!("No scene matches {}.", py_repr(scene)) } else { format!("More than one scene matches; say which:\n  {}", cands.join("\n  ")) };
    };
    let blocks = scene_blocks(&read_lossy(&path));
    let cast = root("scenes/cast").join(format!("{}.cast.md", stem(&path)));
    let cast_line = if cast.exists() { format!("exists \u{2014} {}", rel_posix(&cast, &ROOT)) } else { "none yet".into() };
    let body: Vec<String> = blocks.into_iter().map(|(k, t)| match k {
        "divider" => "---".into(),
        "title" => format!("# {t}"),
        _ => t,
    }).collect();
    format!("scene file: {}\ncast file: {cast_line}\n\n{}\n", name_of(&path), body.join("\n\n"))
}

/// Python's repr() of a str.
fn py_repr(s: &str) -> String {
    let q = if s.contains('\'') && !s.contains('"') { '"' } else { '\'' };
    let mut out = String::from(q);
    for c in s.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if c == q => {
                out.push('\\');
                out.push(c);
            }
            c if (c as u32) < 0x20 || c as u32 == 0x7f => out.push_str(&format!("\\x{:02x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push(q);
    out
}

// ---------------------------------------------------------------- audit.py
const SKIP: [&str; 7] = ["MANIFEST.md", "CAST.md", "ARCS.md", "TIMELINE.md", "00_SUPERSEDED_wrong_names.md", "THE_KINGDOM_OF_KHARVEN_buri.md", "WOTR_AI_Writing_Tells_to_Avoid.md"];

fn audit_scenes() -> Vec<PathBuf> {
    md_files(&root("scenes")).into_iter().filter(|p| !SKIP.contains(&name_of(p).as_str())).collect()
}

/// audit.report: reports/<name>.md with the run date under the title.
fn report(name: &str, mut lines: Vec<String>) -> Result<PathBuf, String> {
    let dir = root("reports");
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let p = dir.join(format!("{name}.md"));
    if lines.first().is_some_and(|l| l.starts_with("# ")) {
        lines.splice(1..1, [format!("_Run {}_", writers::today()), String::new()]);
    }
    std::fs::write(&p, lines.join("\n") + "\n").map_err(|e| e.to_string())?;
    Ok(p)
}

pub fn timeline() -> Result<String, String> {
    let out = root("scenes/TIMELINE.md");
    if !out.exists() {
        let arcs = root("scenes/ARCS.md");
        let order: Vec<String> = if arcs.exists() { rx!(r"(?m)^-\s+(\S+\.md)").captures_iter(read_lossy(&arcs).as_str()).flatten().map(|c| c[1].to_string()).collect() } else { vec![] };
        let mut files = audit_scenes();
        files.sort_by_key(|p| (order.iter().position(|o| *o == name_of(p)).unwrap_or(order.len()), name_of(p)));
        let date_rx = rx!(r"\b(?:Year\s+\d{1,4}|the (?:Thin Weeks|ninth hour|eleventh year|first week)|[Ee]leven (?:months|days|years)|[Ff]ourteen(?:th)?|(?:Imperial|Withering|Reconstruction|Voyager)\s+(?:Age|Era|Year)|\d{1,4}\s+(?:days|months|years)\s+(?:after|before|since|later|out))\b");
        let mut lines: Vec<String> = vec![
            "# Timeline".into(),
            String::new(),
            "One line per scene, in reading order, with the in-world moment as far as the text states it. Fill the blanks; a new scene whose events precede something it references is a continuity error.".into(),
            String::new(),
            "| # | scene | in-world moment (from the text) | placed |".into(),
            "|---|---|---|---|".into(),
        ];
        for (i, p) in files.iter().enumerate() {
            let text = read_page(p);
            let mut hits: Vec<&str> = Vec::new();
            for m in date_rx.find_iter(&text).flatten() {
                if !hits.contains(&m.as_str()) {
                    hits.push(m.as_str());
                }
            }
            let moment = rx!(r"(?m)^\*(.{10,140}?)\*\s*$").captures(text.as_str()).ok().flatten().map(|c| head(&c[1], 120).to_string()).unwrap_or_default();
            let shown = if moment.is_empty() { hits.join(", ") } else { moment };
            lines.push(format!("| {} | {} | {shown} | ____ |", i + 1, name_of(p)));
        }
        std::fs::write(&out, lines.join("\n") + "\n").map_err(|e| e.to_string())?;
    }
    Ok(head(&read_lossy(&out), 8000).to_string())
}

pub fn reconcile() -> Result<String, String> {
    let wiki = root("wiki");
    let mut lines: Vec<String> = ["# Reconcile \u{2014} wiki vs scenes vs index", "", "Mechanical checks only; each finding is a place for a human read.", ""].map(String::from).into();
    let m: serde_json::Map<String, Value> = serde_json::from_str(&std::fs::read_to_string(wiki.join(".manifest.json")).map_err(|e| e.to_string())?).map_err(|e| e.to_string())?;
    let entries: Vec<(String, String)> = m.values().map(|v| (pystr(&v["title"]), pystr(&v["rel"]))).collect();
    // 1. duplicate wiki page titles
    let mut titles: Vec<(&str, usize)> = Vec::new();
    for (t, _) in &entries {
        match titles.iter_mut().find(|e| e.0 == t) {
            Some(e) => e.1 += 1,
            None => titles.push((t, 1)),
        }
    }
    let dups: Vec<String> = titles.iter().filter(|e| e.1 > 1).map(|(t, n)| format!("- {t} \u{d7}{n}")).collect();
    lines.push("## Duplicate wiki pages (same title twice)".into());
    lines.push(String::new());
    lines.extend(if dups.is_empty() { vec!["- none".into()] } else { dups });
    lines.push(String::new());
    // 2. card Stage/Level vs scene mentions; a repeated name keeps its first place and its last value
    let mut cards: Vec<(String, (Option<String>, Option<String>, String))> = Vec::new();
    for (title, rel) in &entries {
        let p = wiki.join(rel);
        if !p.exists() || !rel.contains("Character Cards") {
            continue;
        }
        let t = read_page(&p);
        let st = rx!(r"\bStage\s+([IVX]{1,4})\b").captures(t.as_str()).ok().flatten().map(|c| c[1].to_string());
        let lv = rx!(r"\bLevel\s+(\d{1,3})\b").captures(t.as_str()).ok().flatten().map(|c| c[1].to_string());
        let name = rx!(r"\s+[·—]\s+").split(title).flatten().next().unwrap_or("").trim().to_string();
        let val = (st, lv, rel.clone());
        match cards.iter_mut().find(|c| c.0 == name) {
            Some(c) => c.1 = val,
            None => cards.push((name, val)),
        }
    }
    lines.extend(["## Card vs scene: Stage or Level stated differently".into(), String::new()]);
    struct Probe {
        first: String,
        word: Regex,
        stage: Regex,
        level: Regex,
    }
    let probes: Vec<Option<Probe>> = cards
        .iter()
        .map(|(name, _)| {
            let first = name.split_whitespace().next().unwrap_or("").to_string();
            if chars(&first) < 4 {
                return None;
            }
            let e = fancy_regex::escape(&first);
            Some(Probe {
                word: Regex::new(&format!(r"(?<!\w){e}(?!\w)")).unwrap(),
                stage: Regex::new(&format!(r"{e}[^.\n]{{0,80}}?\bStage\s+([IVX]{{1,4}})\b")).unwrap(),
                level: Regex::new(&format!(r"{e}[^.\n]{{0,80}}?\bLevel\s+(\d{{1,3}})\b")).unwrap(),
                first,
            })
        })
        .collect();
    let mut found = 0;
    for p in audit_scenes() {
        let text = read_page(&p);
        for ((name, (st, lv, rel)), probe) in cards.iter().zip(&probes) {
            let Some(pr) = probe else { continue };
            if !text.contains(&pr.first) || !is(&pr.word, &text) {
                continue;
            }
            for c in pr.stage.captures_iter(text.as_str()).flatten() {
                if let Some(st) = st.as_ref().filter(|s| c[1] != ***s) {
                    lines.push(format!("- {}: {name} at Stage {} in the scene, Stage {st} on the card ({rel})", name_of(&p), &c[1]));
                    found += 1;
                }
            }
            for c in pr.level.captures_iter(text.as_str()).flatten() {
                if let Some(lv) = lv.as_ref().filter(|s| c[1] != ***s) {
                    lines.push(format!("- {}: {name} at Level {} in the scene, Level {lv} on the card ({rel})", name_of(&p), &c[1]));
                    found += 1;
                }
            }
        }
    }
    if found == 0 {
        lines.push("- none found by pattern (Stage/Level within 80 characters of a first name)".into());
    }
    lines.push(String::new());
    // 3. Wellspring assigned to two Families across the wiki (the Family pages in directory order, as Path.glob gives them)
    let mut ws_family: Vec<(String, String)> = Vec::new();
    let fam_dir = wiki.join("The Magic System").join("The Eight Families & the Sixty Wellsprings");
    for fp in std::fs::read_dir(&fam_dir).into_iter().flatten().flatten().map(|e| e.path()).filter(|p| name_of(p).ends_with(".md")) {
        let st = stem(&fp);
        let fam = st.split(" \u{2014} ").next().unwrap_or("").to_string();
        for c in rx!(r"(?m)^###\s+(.+?)\s*·").captures_iter(read_page(&fp).as_str()).flatten() {
            let n = c[1].trim_matches(['*', ' ']).to_string();
            match ws_family.iter_mut().find(|w| w.0 == n) {
                Some(w) => w.1 = fam.clone(),
                None => ws_family.push((n, fam.clone())),
            }
        }
    }
    let families: HashSet<&str> = ws_family.iter().map(|w| w.1.as_str()).collect();
    let ws_rx: Vec<Regex> = ws_family.iter().map(|(ws, _)| Regex::new(&format!(r"\*\*{}\*\*\s*·\s*([A-Z][a-z]+)\b", fancy_regex::escape(ws))).unwrap()).collect();
    lines.extend(["## Wellsprings named with a Family other than their own".into(), String::new()]);
    let mut bad = 0;
    for (_, rel) in &entries {
        let p = wiki.join(rel);
        if !p.exists() {
            continue;
        }
        let t = read_page(&p);
        for ((ws, fam), r) in ws_family.iter().zip(&ws_rx) {
            if !t.contains(&format!("**{ws}**")) {
                continue;
            }
            for c in r.captures_iter(t.as_str()).flatten() {
                if &c[1] != fam && families.contains(&c[1]) {
                    lines.push(format!("- {rel}: {ws} \u{b7} {} (Family page says {fam})", &c[1]));
                    bad += 1;
                }
            }
        }
    }
    if bad == 0 {
        lines.push("- none".into());
    }
    lines.push(String::new());
    lines.extend(["## Stale-register residue", "", "Run WOTR MCP `stale_names` for the live list; this report does not duplicate it.", ""].map(String::from));
    let p = report("reconcile", lines)?;
    Ok(head(&read_lossy(&p), 6000).to_string())
}

pub fn pack_impact(markdown: &str, name: &str) -> Result<String, String> {
    let wrx = rx!(r"[A-Za-z][A-Za-z\-]{4,}");
    let words_of = |s: &str| -> HashSet<String> { wrx.find_iter(s).flatten().map(|m| m.as_str().to_lowercase()).collect() };
    let stop = "which there their about would could should these those where being after before while other every under between through against because still never always might";
    let mut words = words_of(markdown);
    for w in stop.split(' ') {
        words.remove(w);
    }
    let mut hits = Vec::new();
    for r in rules::load()? {
        if r.status != "live" {
            continue;
        }
        let rare: BTreeSet<String> = words_of(&format!("{} {}", r.summary, r.verbatim)).into_iter().filter(|w| words.contains(w) && w.len() >= 7).collect();
        if rare.len() >= 4 {
            hits.push((rare.len(), r.id.clone(), r.title.clone(), rare.into_iter().take(8).collect::<Vec<_>>()));
        }
    }
    hits.sort_by_key(|h| std::cmp::Reverse(h.0));
    // the tool's input file, which audit.impact names in the report's first line
    let file = format!("_impact_input_{}.md", writers::slug_us(name));
    let mut lines = vec![
        format!("# Pack impact \u{2014} {file}"),
        String::new(),
        format!("{} live rules share four or more distinctive terms with this text. Read each against the pack before extraction; a strike or a contradiction needs quotable words.", hits.len()),
        String::new(),
    ];
    lines.extend(hits.iter().take(60).map(|(n, id, title, terms)| format!("- **{id}** ({n}) {title} \u{2014} {}", terms.join(", "))));
    let p = report("pack_impact", lines)?;
    Ok(head(&read_lossy(&p), 8000).to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn python_shapes() {
        assert_eq!(py_repr("it's"), "\"it's\"");
        assert_eq!(py_repr("a'\"\n\\"), "'a\\'\"\\n\\\\'");
        assert_eq!(most_common(["b", "a", "a", "b", "c"].map(String::from).into_iter(), 2), "b\u{d7}2, a\u{d7}2");
        assert_eq!(clean_inline("**bold** and *it* [link](x) `c` ![i](y) \u{a7}5"), "bold and it link c section 5");
    }
}
