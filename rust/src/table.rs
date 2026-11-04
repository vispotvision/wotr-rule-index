//! The table's read side: fronts, due, roster, scene_menu and session_start (build/table.py and
//! mcp_server.py, same names). table/*.yaml is read, never written here: the writers stay in Python,
//! whose PyYAML dump is the files' format. The rows are loose (an int here, a string there), so the
//! helpers below copy Python's str(), int() and truthiness exactly.
use crate::search;
use crate::util::{read_lossy, read_page, root, stem, ROOT};
use fancy_regex::Regex;
use serde_json::Value;
use std::collections::{BTreeSet, HashMap};
use std::path::{Path, PathBuf};
use std::sync::LazyLock;

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

/// Python's str() of a YAML value.
fn s(v: Option<&Value>) -> String {
    match v {
        None | Some(Value::Null) => "None".into(),
        Some(Value::Bool(b)) => if *b { "True" } else { "False" }.into(),
        Some(Value::Number(n)) => n.as_f64().filter(|_| n.is_f64()).map(|f| if f.fract() == 0.0 { format!("{f:.1}") } else { f.to_string() }).unwrap_or_else(|| n.to_string()),
        Some(Value::String(t)) => t.clone(),
        Some(Value::Array(a)) => format!("[{}]", a.iter().map(|x| match x { Value::String(t) => format!("'{t}'"), o => s(Some(o)) }).collect::<Vec<_>>().join(", ")),
        Some(o) => o.to_string(),
    }
}

/// Python truthiness.
fn t(v: Option<&Value>) -> bool {
    match v {
        None | Some(Value::Null) => false,
        Some(Value::Bool(b)) => *b,
        Some(Value::Number(n)) => n.as_f64() != Some(0.0),
        Some(Value::String(x)) => !x.is_empty(),
        Some(Value::Array(a)) => !a.is_empty(),
        Some(Value::Object(o)) => !o.is_empty(),
    }
}

/// Python's int(): ints, digit strings (spaces allowed), bools; anything else is the ValueError.
fn int(v: Option<&Value>) -> Result<i64, String> {
    match v {
        Some(Value::Number(n)) => n.as_i64().or_else(|| n.as_f64().map(|f| f.trunc() as i64)).ok_or("int(): bad number".into()),
        Some(Value::Bool(b)) => Ok(*b as i64),
        Some(Value::String(x)) => x.trim().parse().map_err(|_| format!("ValueError: invalid literal for int() with base 10: '{x}'")),
        _ => Err("TypeError: int() argument must be a string or a number, not 'NoneType'".into()),
    }
}

/// get with a default, as r.get(k, default)
fn g<'a>(r: &'a Value, k: &str) -> Option<&'a Value> {
    r.get(k)
}

/// s() of r.get(k) or `or_` when the value is falsy: f"{r.get(k) or 'x'}"
fn or(r: &Value, k: &str, or_: &str) -> String {
    if t(g(r, k)) { s(g(r, k)) } else { or_.into() }
}

/// f"{r.get(k, '')}": the default only when the key is absent
fn get_s(r: &Value, k: &str) -> String {
    if r.get(k).is_some() { s(r.get(k)) } else { String::new() }
}

pub fn load(kind: &str) -> Result<Vec<Value>, String> {
    let p = root(&format!("table/{kind}.yaml"));
    if !p.exists() {
        return Ok(vec![]);
    }
    let v: Value = serde_yaml_ng::from_str(&read_lossy(&p)).map_err(|e| format!("{}: {e}", p.display()))?;
    Ok(match v {
        Value::Array(a) => a,
        _ => vec![],
    })
}

fn same_thread(a: Option<&Value>, b: &str) -> bool {
    let a = if t(a) { s(a).to_lowercase().trim().to_string() } else { String::new() };
    let b = b.to_lowercase().trim().to_string();
    !a.is_empty() && !b.is_empty() && (b.contains(&a) || a.contains(&b))
}

fn story_days(v: &str) -> Option<i64> {
    let c = rx!(r"^\s*(\d+)-(\d+)-(\d+)\s*$").captures(v).ok().flatten()?;
    let (y, m, d): (i64, i64, i64) = (c[1].parse().ok()?, c[2].parse().ok()?, c[3].parse().ok()?);
    ((1..=13).contains(&m) && (1..=28).contains(&d)).then(|| y * 364 + (m - 1) * 28 + d - 1)
}

/// str(s or "") for story_days
fn opt_str(v: Option<&Value>) -> String {
    if t(v) { s(v) } else { String::new() }
}

pub fn thread_date(thread: &str) -> Result<Option<Value>, String> {
    Ok(load("threads")?.into_iter().find(|r| same_thread(r.get("thread"), thread)).map(|r| r.get("story_date").cloned().unwrap_or(Value::Null)))
}

pub fn fronts_for(thread: Option<&str>, include_closed: bool) -> Result<Vec<Value>, String> {
    let mut rows = load("fronts")?;
    if let Some(th) = thread {
        let th = th.to_lowercase();
        rows.retain(|r| s(r.get("thread")).to_lowercase().contains(&th) || s(r.get("name")).to_lowercase().contains(&th));
    }
    if !include_closed {
        rows.retain(|r| r.get("status").and_then(Value::as_str) != Some("closed"));
    }
    Ok(rows)
}

fn clock(r: &Value) -> Vec<Value> {
    r.get("clock").and_then(Value::as_array).cloned().unwrap_or_default()
}

/// The consequence of the tick after `pos`, else the Front's next_move.
fn next_tick(r: &Value, pos: i64) -> String {
    clock(r).iter().find(|c| c.get("tick").and_then(Value::as_i64) == Some(pos + 1)).map(|c| s(c.get("consequence"))).unwrap_or_else(|| get_s(r, "next_move"))
}

fn fronts_text(thread: Option<&str>) -> Result<String, String> {
    let rows = fronts_for(thread, false)?;
    if rows.is_empty() {
        return Ok(format!("no open Fronts{}", thread.map(|t| format!(" for '{t}'")).unwrap_or_default()));
    }
    let mut out = Vec::new();
    for r in &rows {
        let (pos, n) = (int(Some(r.get("position").unwrap_or(&Value::from(0))))?, clock(r).len() as i64);
        let pace = if t(r.get("pace_days")) {
            format!("a tick every {} story days, {} spent", s(r.get("pace_days")), r.get("days_banked").map(|v| s(Some(v))).unwrap_or("0".into()))
        } else {
            "none set, so the calendar never ticks it (R72-20)".into()
        };
        out.push(format!(
            "[{}] {} · {}{} {pos}/{n}\n  want: {}\n  last: {}\n  next tick: {}\n  pace: {pace}",
            s(r.get("id")), s(r.get("name")), "●".repeat(pos.max(0) as usize), "○".repeat((n - pos).max(0) as usize),
            get_s(r, "want"), get_s(r, "last_move"), next_tick(r, pos)
        ));
    }
    Ok(out.join("\n\n"))
}

pub fn fronts(thread: &str, include_closed: bool) -> Result<String, String> {
    let th = Some(thread).filter(|x| !x.is_empty());
    if fronts_for(th, include_closed)?.is_empty() {
        return Ok(format!("no Fronts match '{thread}'"));
    }
    fronts_text(th)
}

const SESSION_CATS: [&str; 5] = ["debts", "who knows what", "injuries and reserve", "reputation", "renown"];

/// table.due: open Ledger lines come due, each with its age and why.
pub fn due_rows(sessions_old: i64, thread: Option<&str>, today: Option<&str>) -> Result<Vec<(Value, i64, String)>, String> {
    let thread = thread.filter(|x| !x.is_empty()); // Python: an empty thread is no filter
    let rows = load("ledger")?;
    let now = load("sessions")?.len() as i64;
    let mut out = Vec::new();
    for r in rows {
        if r.get("status").and_then(Value::as_str) != Some("open") || thread.is_some_and(|th| t(r.get("thread")) && !same_thread(r.get("thread"), th)) {
            continue;
        }
        let age = now - int(Some(r.get("opened_session").unwrap_or(&Value::from(0))))?;
        let (mut why, mut rank) = (None, 0);
        let ticks = r.get("ticks");
        if t(ticks) && int(Some(r.get("filled").unwrap_or(&Value::from(0))))? >= int(ticks)? {
            why = Some(format!("clock full, {}/{}", s(r.get("filled")), s(ticks)));
        } else if t(r.get("fired")) {
            why = Some(format!("fired ({}): {}", s(r.get("fired")), get_s(&r, "due_trigger")));
        } else if t(r.get("due_date")) {
            let d = story_days(&s(r.get("due_date")));
            let today_v = match today {
                Some(x) => Some(x.to_string()),
                None => {
                    let th_key = if t(r.get("thread")) { s(r.get("thread")) } else { thread.unwrap_or("").to_string() };
                    thread_date(&th_key)?.map(|v| opt_str(Some(&v)))
                }
            };
            let tt = story_days(&today_v.unwrap_or_default());
            match (d, tt) {
                (None, _) | (_, None) => {
                    why = Some(format!("date not judged: {}", if d.is_none() { "write it Y-M-D" } else { "no story date held for the thread (pass_time)" }));
                    rank = 2;
                }
                (Some(d), Some(tt)) if d <= tt => why = Some(format!("date came: {}", s(r.get("due_date")))),
                _ => {}
            }
        } else if !t(r.get("due_trigger")) && !t(ticks) {
            let d = r.get("due");
            rank = 1;
            if t(d) && d.and_then(Value::as_str) != Some("pending Natalie") {
                let ds = s(d);
                if !(!ds.is_empty() && ds.chars().all(|c| c.is_numeric())) {
                    why = Some(format!("no date or trigger yet, a stated condition to judge: {ds}"));
                } else if age >= int(d)? {
                    why = Some(format!("no date or trigger yet, {age} session(s) old"));
                }
            } else if age >= sessions_old && SESSION_CATS.contains(&s(r.get("category")).as_str()) {
                why = Some(format!("no date or trigger yet, {age} session(s) old"));
            }
        }
        if let Some(w) = why {
            out.push((rank, age, w, r));
        }
    }
    out.sort_by_key(|x| (x.0, -x.1));
    Ok(out.into_iter().map(|(_, a, w, r)| (r, a, w)).collect())
}

pub fn due(sessions_old: i64, thread: &str, today: &str) -> Result<String, String> {
    let th = Some(thread).filter(|x| !x.is_empty());
    let rows = due_rows(sessions_old, th, Some(today).filter(|x| !x.is_empty()))?;
    if rows.is_empty() {
        let held = if th.is_some() { thread_date(thread)? } else { None };
        let when = match (&held, th) {
            (Some(h), _) if t(Some(h)) => format!("; story date {}", s(Some(h))),
            (_, Some(_)) => "; no story date held for this thread (pass_time sets it)".into(),
            _ => String::new(),
        };
        let open = load("ledger")?.iter().filter(|r| r.get("status").and_then(Value::as_str) == Some("open")).count();
        return Ok(format!("nothing has come due; {open} lines open{when}"));
    }
    Ok(rows.iter().take(12).map(|(r, _, why)| format!("[{}] ({}, {}) {}\n  why: {why}", s(r.get("id")), s(r.get("category")), or(r, "thread", "no thread"), s(r.get("text")))).collect::<Vec<_>>().join("\n"))
}

const PUBLIC: [&str; 3] = ["look", "voice", "role"];

pub fn roster(thread: &str, public: bool) -> Result<String, String> {
    let th = thread.to_lowercase();
    let rows: Vec<Value> = load("npcs")?.into_iter().filter(|r| th.is_empty() || get_s(r, "thread").to_lowercase().contains(&th)).collect();
    if rows.is_empty() {
        return Ok(format!("roster empty{}; use npc_set after a session to fill it", if thread.is_empty() { String::new() } else { format!(" for '{thread}'") }));
    }
    let notes = rx!(r"(?s)\s*\([^)]*\bIsaac\b[^)]*\)|\s*(?:Gloss rights:|Swap test:|LINE NOT SET|Counterplay:|Tell:).*");
    let list = |r: &Value, k: &str| r.get(k).and_then(Value::as_array).map(|a| a.iter().map(|x| s(Some(x))).collect::<Vec<_>>().join("; ")).unwrap_or_default();
    let out: Vec<String> = rows
        .iter()
        .map(|r| {
            if public {
                let face: Vec<String> = PUBLIC.iter().filter(|k| t(r.get(**k))).map(|k| format!("{k} {}", notes.replace_all(&s(r.get(*k)), "").trim())).collect();
                return format!("{}: {}", s(r.get("name")), if face.is_empty() { "no public face set".to_string() } else { face.join("; ") });
            }
            let knows = Some(list(r, "knows")).filter(|x| !x.is_empty()).unwrap_or("nothing logged".into());
            let lied = Some(list(r, "lied_about")).filter(|x| !x.is_empty()).unwrap_or("nothing logged".into());
            let line = format!(
                "{} ({}): wants {}; refuses {}; knows {knows}; live lie {} (tell: {}); lied about {lied}; doing now {}; stands with him {}; last seen {}",
                s(r.get("name")), get_s(r, "thread"), or(r, "want", "unset"), or(r, "refusal_line", "unset"), or(r, "lie", "unset"),
                or(r, "tell", "unset"), or(r, "doing_now", "unset"), or(r, "stands_with", "unset"), or(r, "last_seen", "unset")
            );
            let gap = if t(r.get("want")) && !t(r.get("lie")) { "a want and no live lie" } else if t(r.get("lie")) && !t(r.get("tell")) { "a live lie and no tell" } else { "" };
            if gap.is_empty() { line } else { format!("{line}\n  R72-25: {gap}") }
        })
        .collect();
    Ok(out.join("\n"))
}

/// mcp_server._inventory: the culture's Standing Inventory.
fn inventory(culture: &str) -> String {
    let key = culture.to_lowercase();
    for e in std::fs::read_dir(root("desktop/inventories")).into_iter().flatten().flatten() {
        let p = e.path();
        if p.extension().is_none_or(|x| x != "md") {
            continue;
        }
        let text = read_lossy(&p);
        let headl = text.split('\n').next().unwrap_or("").to_lowercase();
        if stem(&p).to_lowercase().contains(&key) || headl.contains(&key) {
            return text.trim().to_string();
        }
    }
    let nat = read_lossy(&root("desktop/NATALIE.md"));
    if let Ok(r) = Regex::new(&format!(r"(?ms)^# THE STANDING INVENTORY: {}.*?(?=^# |\z)", fancy_regex::escape(&culture.to_uppercase()))) {
        if let Some(m) = r.find(&nat).ok().flatten() {
            return m.as_str().trim().to_string();
        }
    }
    if let Some((_, p, _)) = search::rank(&root("wiki"), &format!("standing inventory {culture}"), 1).into_iter().next() {
        return format!("(no inventory section in NATALIE.md for {culture}; nearest wiki page: {})\n{}", stem(&p), crate::util::head(&read_page(&p), 6000));
    }
    format!("No Standing Inventory exists for {culture}. Write it from the wiki and the cards straight away; anything invented stands as canon once in an archived scene (R79-4).")
}

const NOT_SCENES: [&str; 6] = ["MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md", "INDEX.md", "CONTINUITY.md"];

fn local_date(ts: f64) -> String {
    // datetime.fromtimestamp(ts).date(): the local calendar day, as `date` prints it
    std::process::Command::new("date").args(["-d", &format!("@{}", ts as i64), "+%F"]).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default()
}

/// mcp_server._last_scene: the newest archived scene for a thread and its last `words` words.
fn last_scene(thread: &str, words: usize) -> String {
    let key = { let k = thread.split('/').next().unwrap_or("").trim(); if k.is_empty() { thread.trim() } else { k } }.to_string();
    let words_in: Vec<String> = rx!(r"\w[\w'-]+").find_iter(&key).flatten().map(|m| m.as_str().to_string()).filter(|w| w.chars().count() > 2).collect();
    let scenes = root("scenes");
    let mut names: Vec<PathBuf> = std::fs::read_dir(&scenes).into_iter().flatten().flatten().map(|e| e.path()).filter(|p| p.extension().is_some_and(|x| x == "md")).collect();
    names.sort();
    let files: HashMap<String, PathBuf> = names
        .into_iter()
        .filter_map(|p| {
            let n = p.file_name()?.to_string_lossy().into_owned();
            let skip = n.to_uppercase().contains("SUPERSEDED") || n.ends_with(".cast.md") || NOT_SCENES.contains(&n.as_str());
            (!skip).then_some((n, p))
        })
        .collect();
    let mut cands: BTreeSet<String> = BTreeSet::new();
    let arcs = scenes.join("ARCS.md");
    if arcs.exists() {
        let text = read_lossy(&arcs);
        for block in rx!(r"(?m)^## ").split(&text).flatten().skip(1) {
            let headl = block.split('\n').next().unwrap_or("").to_lowercase();
            if words_in.iter().any(|w| headl.contains(&w.to_lowercase())) {
                cands.extend(rx!(r"(?m)^- (\S+\.md)").captures_iter(block).flatten().map(|c| c[1].to_string()).filter(|n| files.contains_key(n)));
            }
        }
    }
    if !words_in.is_empty() {
        let alt: Vec<String> = words_in.iter().map(|w| fancy_regex::escape(w).into_owned()).collect();
        if let Ok(r) = Regex::new(&format!(r"(?<!\w)(?:{})(?!\w)", alt.join("|"))) {
            for (n, p) in &files {
                let text = read_lossy(p);
                let found: Vec<String> = r.find_iter(&text).flatten().map(|m| m.as_str().to_string()).collect();
                let set: BTreeSet<&String> = found.iter().collect();
                if found.len() >= 10 && words_in.iter().all(|w| set.contains(w)) {
                    cands.insert(n.clone());
                }
            }
        }
    }
    if cands.is_empty() {
        let hit = search::rank(&scenes, &key, 5).into_iter().find(|(_, p, low)| {
            let n = p.file_name().map(|x| x.to_string_lossy().into_owned()).unwrap_or_default();
            files.contains_key(&n) && !words_in.is_empty() && words_in.iter().all(|w| low.contains(&w.to_lowercase()))
        });
        match hit {
            Some((_, p, _)) => {
                cands.insert(p.file_name().unwrap().to_string_lossy().into_owned());
            }
            None => return format!("(no archived scene matches '{key}')"),
        }
    }
    // when git first added each scene (the log runs newest first, so the last stamp seen wins)
    let mut added: HashMap<String, f64> = HashMap::new();
    if let Ok(o) = std::process::Command::new("git").args(["log", "--diff-filter=A", "--format=@%at", "--name-only", "--", "scenes"]).current_dir(&*ROOT).output() {
        let mut stamp = 0.0;
        for ln in String::from_utf8_lossy(&o.stdout).lines() {
            if let Some(x) = ln.strip_prefix('@') {
                stamp = x.parse().unwrap_or(0.0);
            } else if !ln.trim().is_empty() {
                added.insert(Path::new(ln.trim()).file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default(), stamp);
            }
        }
    }
    let when_of = |n: &str| {
        added.get(n).copied().unwrap_or_else(|| {
            std::fs::metadata(&files[n]).and_then(|m| m.modified()).ok().and_then(|t| t.duration_since(std::time::UNIX_EPOCH).ok()).map(|d| d.as_secs_f64()).unwrap_or(0.0)
        })
    };
    // max() keeps the first of a tie; Python's set order is random there, sorted names are not
    let mut best: Option<(String, f64)> = None;
    for n in &cands {
        let w = when_of(n);
        if best.as_ref().is_none_or(|(_, bw)| w > *bw) {
            best = Some((n.clone(), w));
        }
    }
    let (name, w) = best.unwrap();
    let p = &files[&name];
    let text = read_page(p);
    let title = rx!(r"(?m)^#\s+(.+)$").captures(text.as_str()).ok().flatten().map(|c| c[1].trim().to_string()).unwrap_or_else(|| stem(p));
    let body = rx!(r"(?m)^#{1,3}\s+Author notes\b").split(&text).flatten().next().unwrap_or("").to_string();
    let tail: Vec<&str> = body.split_whitespace().collect();
    let excerpt = tail[tail.len().saturating_sub(words)..].join(" ");
    format!("## {title}  ({name}, archived {}, {} words)\n\n{}{excerpt}", local_date(w), tail.len(), if tail.len() > words { "..." } else { "" })
}

pub fn session_start(thread: &str, culture: &str) -> String {
    let mut parts = vec![format!("# LAST ARCHIVED SCENE\n\n{}", last_scene(thread, 1500))];
    parts.push(format!("# STANDING INVENTORY\n\n{}", inventory(culture)));
    let th = { let k = thread.split('/').next().unwrap_or("").trim(); if k.is_empty() { None } else { Some(k) } };
    parts.push(match due_rows(2, th, None) {
        Ok(d) if d.is_empty() => "# COMES DUE\n\nnothing has come due".into(),
        Ok(d) => format!("# COMES DUE\n\n{}", d.iter().take(8).map(|(r, _, why)| format!("[{}] ({}) {}  why: {why}", s(r.get("id")), s(r.get("category")), s(r.get("text")))).collect::<Vec<_>>().join("\n")),
        Err(e) => format!("# COMES DUE\n\n(table unavailable: {e})"),
    });
    let inbox = std::fs::read_dir(root("inbox")).into_iter().flatten().flatten().filter(|e| e.path().extension().is_some_and(|x| x == "md")).count();
    parts.push(format!("# INBOX: {inbox} pending"));
    parts.join("\n\n---\n\n")
}

pub fn scene_menu(thread: &str, culture: &str) -> Result<String, String> {
    let mut fr = fronts_for(Some(thread), false)?;
    let mut keyed = Vec::new();
    for r in fr.drain(..) {
        let pos = int(Some(r.get("position").unwrap_or(&Value::from(0))))?;
        keyed.push((-pos, opt_str(r.get("last_advanced")), r));
    }
    keyed.sort_by(|a, b| (a.0, &a.1).cmp(&(b.0, &b.1)));
    let f = keyed.into_iter().next().map(|x| x.2);
    let d = due_rows(1, Some(thread), None)?;
    let dl = d.first();
    let cast = root("scenes/CAST.md");
    let stale = if cast.exists() {
        let text = read_lossy(&cast);
        let few: Vec<String> = rx!(r"(?m)^## (.+?) \((\d+) scenes\)").captures_iter(text.as_str()).flatten().filter(|c| c[2].parse::<i64>().unwrap_or(99) <= 2).map(|c| c[1].to_string()).take(6).collect();
        few.join(", ")
    } else {
        String::new()
    };
    let inv = inventory(culture);
    let rec = rx!(r"(?s)\*\*Recurrence.*?:\*\*(.*?)(?:\.\s|\n)").captures(inv.as_str()).ok().flatten().map(|c| c[1].trim().to_string()).unwrap_or_default();
    let hook1 = match &f {
        Some(f) => {
            let pos = int(Some(f.get("position").unwrap_or(&Value::from(0))))?;
            let nxt = next_tick(f, pos);
            let when = if t(f.get("pace_days")) {
                format!("within {} story days", int(f.get("pace_days"))? - int(Some(f.get("days_banked").unwrap_or(&Value::from(0))))?)
            } else {
                "the next time story time passes".into()
            };
            format!("(a Front, {}; for Natalie: ticks offscreen {when}) {}.", s(f.get("name")), nxt.trim_end_matches('.'))
        }
        None => "(a Front) no open Front on this thread".into(),
    };
    let hook2 = match dl {
        Some((r, _, why)) => format!("(a Ledger line, [{}], {why}) {}.", s(r.get("id")), s(r.get("text")).trim_end_matches('.')),
        None => "(a Ledger line) nothing has come due".into(),
    };
    let fresh = format!("- (fresh) a character the archive has barely seen ({}){}.", if stale.is_empty() { "run cast_index" } else { &stale }, if rec.is_empty() { String::new() } else { format!(", through one of: {rec}") });
    Ok([
        format!("# Scene Menu seeds: {thread} (OOC; offer three hooks from anywhere, one line each, no reward or penalty lines, R79-2)"),
        String::new(),
        format!("- {hook1}"),
        format!("- {hook2}"),
        fresh,
        String::new(),
        "He picks in a word; the turn opens on that hook in the world.".into(),
    ]
    .join("\n"))
}
