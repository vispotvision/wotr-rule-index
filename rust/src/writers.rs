//! Every tool that writes: the table (table.py's advance, set_clock, add_front, pass_time,
//! ledger_add, ledger_mark, fire, ledger_collect, session_log, npc_set, render and mcp_server's
//! wrappers and session_end), archive_scene with scenes_to_wiki.py, wiki_write, log_ruling,
//! propose_rule, create_character, update_character, the inbox and sync_now. Ported line for line;
//! table/*.yaml goes through pyyaml.rs, byte-identical to PyYAML's safe_dump.
//! rust/writer_parity.py replays the same calls through Python and Rust in two scratch clones.
use crate::table::{clock, get_s, int, load, opt_str, s, same_thread, story_days, t};
use crate::util::{chars, head, read_lossy, read_page, root, tail, ROOT};
use chrono::Datelike;
use fancy_regex::Regex;
use serde_json::{json, Map, Value};
use std::path::{Component, Path, PathBuf};
use std::sync::LazyLock;

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

/// Python exceptions the wrappers catch: KeyError prints its argument quoted, ValueError plain.
pub enum E {
    Key(String),
    Value(String),
}

impl std::fmt::Display for E {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            E::Key(k) => write!(f, "'{k}'"),
            E::Value(m) => write!(f, "{m}"),
        }
    }
}

impl From<String> for E {
    fn from(m: String) -> Self {
        E::Value(m)
    }
}

type R<T> = Result<T, E>;

// ---------------------------------------------------------------- small helpers
pub fn git(args: &[&str]) -> (i32, String) {
    match std::process::Command::new("git").args(args).current_dir(&*ROOT).output() {
        Ok(o) => (o.status.code().unwrap_or(1), format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)).trim().to_string()),
        Err(e) => (1, e.to_string()),
    }
}

pub(crate) fn date_fmt(fmt: &str) -> String {
    std::process::Command::new("date").arg(format!("+{fmt}")).output().map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string()).unwrap_or_default()
}

/// date.today().isoformat(), local
pub fn today() -> String {
    date_fmt("%F")
}

pub(crate) fn now_iso() -> String {
    date_fmt("%Y-%m-%dT%H:%M:%S")
}

fn push(tail_chars: usize) -> String {
    let (code, out) = git(&["push", "-q", "origin", "master"]);
    if code == 0 { "pushed".into() } else { format!("push failed: {}", tail(&out, tail_chars)) }
}

fn words(x: &str) -> usize {
    x.split_whitespace().count()
}

/// mcp_server._slug
pub(crate) fn slug_us(title: &str) -> String {
    let x = rx!(r"[^\w\s-]").replace_all(title, "").trim().to_lowercase();
    let x = rx!(r"[\s_-]+").replace_all(&x, "_").to_string();
    let x = head(&x, 80).to_string();
    if x.is_empty() { "untitled".into() } else { x }
}

/// table.slug
fn slug_dash(name: &str) -> String {
    let x = rx!(r"[^\w\s-]").replace_all(name, "").trim().to_lowercase();
    head(&rx!(r"[\s_-]+").replace_all(&x, "-"), 50).to_string()
}

/// mcp_server._safe_name
fn safe_name(title: &str) -> String {
    let x = rx!(r#"[/\\:*?"<>|]"#).replace_all(title, "").trim().to_string();
    if x.is_empty() { "Untitled".into() } else { x }
}

/// json.dumps(v, ensure_ascii=False): Python's separators, ', ' and ': '
fn py_json(v: &Value) -> String {
    match v {
        Value::Array(a) => format!("[{}]", a.iter().map(py_json).collect::<Vec<_>>().join(", ")),
        Value::Object(o) => format!("{{{}}}", o.iter().map(|(k, x)| format!("{}: {}", py_json(&Value::String(k.clone())), py_json(x))).collect::<Vec<_>>().join(", ")),
        o => serde_json::to_string(o).unwrap(),
    }
}

/// json.dumps(m, indent=2, ensure_ascii=False)
fn py_json_indent(v: &Value) -> String {
    serde_json::to_string_pretty(v).unwrap()
}

pub(crate) fn save(kind: &str, rows: &[Value]) {
    let dir = root("table");
    let _ = std::fs::create_dir_all(&dir);
    let _ = std::fs::write(dir.join(format!("{kind}.yaml")), crate::pyyaml::dump(&Value::Array(rows.to_vec())));
}

fn id_of(r: &Value) -> R<String> {
    r.get("id").map(|v| s(Some(v))).ok_or(E::Key("id".into()))
}

fn session_count() -> R<i64> {
    Ok(load("sessions")?.len() as i64)
}

/// thread_date(thread) or date.today()
fn stamp_for(thread: Option<&Value>) -> R<String> {
    let th = if t(thread) { s(thread) } else { String::new() };
    let d = if th.is_empty() && thread.is_none() { None } else { crate::table::thread_date(&th)? };
    Ok(if t(d.as_ref()) { s(d.as_ref()) } else { today() })
}

fn story_date_from(n: i64) -> String {
    chrono::NaiveDate::from_num_days_from_ce_opt(n as i32).map_or_else(String::new, |d| format!("{}-{}-{}", d.year(), d.month(), d.day()))
}

fn obj(r: &mut Value) -> &mut Map<String, Value> {
    r.as_object_mut().expect("table rows are mappings")
}

// ---------------------------------------------------------------- table.py's writers
fn advance(front_id: &str, what: &str, next_move: &str, session: &str) -> R<Value> {
    let mut rows = load("fronts")?;
    for i in 0..rows.len() {
        if id_of(&rows[i])? != front_id {
            continue;
        }
        let r = obj(&mut rows[i]);
        let n = r.get("clock").and_then(Value::as_array).map(Vec::len).ok_or(E::Key("clock".into()))? as i64;
        let pos = (int(Some(r.get("position").unwrap_or(&json!(0))))? + 1).min(n);
        r.insert("position".into(), json!(pos));
        r.insert("last_move".into(), json!(what));
        if !next_move.is_empty() {
            r.insert("next_move".into(), json!(next_move));
            for tk in r.get_mut("clock").and_then(Value::as_array_mut).into_iter().flatten() {
                if tk.get("tick").and_then(Value::as_i64) == Some(pos + 1) {
                    obj(tk).insert("consequence".into(), json!(next_move));
                }
            }
        }
        r.insert("last_advanced".into(), json!(if session.is_empty() { today() } else { session.to_string() }));
        if pos >= n {
            r.insert("status".into(), json!("resolved"));
        }
        let out = rows[i].clone();
        save("fronts", &rows);
        return Ok(out);
    }
    Err(E::Key(front_id.into()))
}

fn ticks_clock(ticks: &[String]) -> Value {
    Value::Array(ticks.iter().enumerate().map(|(i, c)| json!({"tick": i + 1, "consequence": c})).collect())
}

fn set_clock(front_id: &str, ticks: Option<&[String]>, pace_days: Option<i64>) -> R<Value> {
    let mut rows = load("fronts")?;
    for i in 0..rows.len() {
        if id_of(&rows[i])? != front_id {
            continue;
        }
        let r = obj(&mut rows[i]);
        if let Some(tk) = ticks.filter(|x| !x.is_empty()) {
            r.insert("clock".into(), ticks_clock(tk));
        }
        if let Some(p) = pace_days {
            r.insert("pace_days".into(), json!(p)); // 0 stops the calendar clock: his acts can stop it (R72-20)
        }
        let out = rows[i].clone();
        save("fronts", &rows);
        return Ok(out);
    }
    Err(E::Key(front_id.into()))
}

fn add_front_row(name: &str, thread: &str, want: &str, ticks: &[String], next_move: &str, pace_days: Option<i64>) -> R<Value> {
    let mut rows = load("fronts")?;
    let nm = if !next_move.is_empty() { next_move.to_string() } else { ticks.first().cloned().unwrap_or_default() };
    let mut r = json!({"id": slug_dash(name), "name": name, "thread": thread, "status": "open", "want": want, "last_move": "",
        "next_move": nm, "clock": ticks_clock(ticks), "position": 0, "last_advanced": null, "seeded_from": "added at the table"});
    if let Some(p) = pace_days.filter(|p| *p != 0) {
        obj(&mut r).insert("pace_days".into(), json!(p));
        obj(&mut r).insert("days_banked".into(), json!(0));
    }
    rows.push(r.clone());
    save("fronts", &rows);
    Ok(r)
}

fn pass(thread: &str, mut days: i64, when: &str) -> R<(Value, Vec<Value>)> {
    if !when.is_empty() && story_days(when).is_none() {
        return Err(E::Value(format!("story date '{when}' is not a real Y-M-D date (R85-2)")));
    }
    let mut rows = load("threads")?;
    let idx = match rows.iter().position(|r| same_thread(r.get("thread"), thread)) {
        Some(i) => i,
        None => {
            rows.push(json!({"thread": thread, "story_date": null}));
            rows.len() - 1
        }
    };
    let old = story_days(&opt_str(rows[idx].get("story_date")));
    if !when.is_empty() {
        if days == 0 {
            if let Some(o) = old {
                days = (story_days(when).unwrap() - o).max(0);
            }
        }
        obj(&mut rows[idx]).insert("story_date".into(), json!(when));
    } else if days != 0 {
        if let Some(o) = old {
            obj(&mut rows[idx]).insert("story_date".into(), json!(story_date_from(o + days)));
        }
    }
    let row = rows[idx].clone();
    save("threads", &rows);
    let mut fr = load("fronts")?;
    let mut owed = Vec::new();
    for r in fr.iter_mut() {
        if days != 0 && r.get("status").and_then(Value::as_str) == Some("open") && t(r.get("pace_days")) && same_thread(r.get("thread"), thread) {
            let pace = int(r.get("pace_days"))?;
            let total = int(Some(r.get("days_banked").unwrap_or(&json!(0))))? + days;
            obj(r).insert("days_banked".into(), json!(total.rem_euclid(pace)));
            for _ in 0..total.div_euclid(pace) {
                owed.push(id_of(r)?);
            }
        }
    }
    save("fronts", &fr);
    let mut ticks = Vec::new();
    for fid in owed {
        let f = load("fronts")?.into_iter().find(|x| id_of(x).ok().as_deref() == Some(fid.as_str())).ok_or(E::Key(fid.clone()))?;
        if f.get("status").and_then(Value::as_str) != Some("open") {
            continue; // resolved by an earlier tick of this same pass
        }
        let pos = int(Some(f.get("position").unwrap_or(&json!(0))))?;
        let cons = clock(&f).iter().find(|c| c.get("tick").and_then(Value::as_i64) == Some(pos + 1)).map(|c| s(c.get("consequence"))).unwrap_or_else(|| get_s(&f, "next_move"));
        let when_txt = if t(row.get("story_date")) { s(row.get("story_date")) } else { format!("{days} days on") };
        ticks.push(advance(&fid, &format!("Offscreen, {when_txt}: {cons}"), "", "")?);
    }
    Ok((row, ticks))
}

const STANDING: [&str; 4] = ["the dead", "bonds", "heat", "canon conflicts"];

#[allow(clippy::too_many_arguments)]
fn ledger_add_row(category: &str, who: &str, text: &str, due_after: Value, thread: &str, due_date: &str, due_trigger: &str, ticks: Option<i64>, level: &str) -> R<Value> {
    let c = category.trim().to_lowercase();
    let cat = match c.as_str() {
        "bond" => "bonds".to_string(),
        "project" => "projects".into(),
        "road" | "the road" => "roads".into(),
        _ => c,
    };
    if !due_date.is_empty() && story_days(due_date).is_none() {
        return Err(E::Value(format!("due_date '{due_date}' is not a real Y-M-D date (R85-2)")));
    }
    let mut rows = load("ledger")?;
    let clocks = match cat.as_str() {
        "projects" => Some((4, 8)),
        "roads" => Some((4, 6)),
        _ => None,
    };
    if let Some((lo, hi)) = clocks {
        if !ticks.is_some_and(|n| n != 0 && lo <= n && n <= hi) {
            let shown = ticks.map(|n| n.to_string()).unwrap_or("None".into());
            return Err(E::Value(format!("a {cat} line runs on a clock of {lo} to {hi} ticks (R72-28, R72-29); ticks={shown}")));
        }
    }
    if cat == "heat" && (thread.is_empty() || rows.iter().any(|r| s(r.get("category")) == "heat" && r.get("status").and_then(Value::as_str) == Some("open") && same_thread(r.get("thread"), thread))) {
        return Err(E::Value("heat is one standing line per thread (R72-24): name the thread, and raise or cool the open line with ledger_mark".into()));
    }
    let mut n = 0;
    for r in &rows {
        let id = id_of(r)?;
        n = n.max(id.chars().skip(1).collect::<String>().trim().parse::<i64>().map_err(|_| E::Value(format!("invalid literal for int() with base 10: '{}'", id.chars().skip(1).collect::<String>())))?);
    }
    let mut r = json!({"id": format!("L{:03}", n + 1), "category": cat, "who": who, "text": text, "opened": today(),
        "opened_session": session_count()?, "due": due_after, "status": "open"});
    let o = obj(&mut r);
    for (k, v) in [("thread", json!(thread)), ("due_date", json!(due_date)), ("due_trigger", json!(due_trigger)), ("ticks", ticks.map(Value::from).unwrap_or(Value::Null)), ("level", json!(level))] {
        if t(Some(&v)) {
            o.insert(k.into(), v);
        }
    }
    if ticks.is_some_and(|n| n != 0) {
        o.insert("filled".into(), json!(0));
    }
    if cat == "bonds" {
        o.insert("fed".into(), json!([]));
        o.insert("strained".into(), json!([]));
    }
    rows.push(r.clone());
    save("ledger", &rows);
    Ok(r)
}

fn push_list(r: &mut Map<String, Value>, k: &str, v: String) {
    let e = r.entry(k.to_string()).or_insert(json!([]));
    if let Value::Array(a) = e {
        a.push(json!(v));
    }
}

fn ledger_mark_row(entry_id: &str, fed: &str, strained: &str, level: &str, tick: i64, how: &str) -> R<Value> {
    let mut rows = load("ledger")?;
    for i in 0..rows.len() {
        if id_of(&rows[i])? != entry_id {
            continue;
        }
        let stamp = stamp_for(rows[i].get("thread"))?;
        let note = if how.is_empty() { String::new() } else { format!(" ({how})") };
        let r = obj(&mut rows[i]);
        if !fed.is_empty() {
            push_list(r, "fed", fed.into());
        }
        if !strained.is_empty() {
            push_list(r, "strained", strained.into());
        }
        if !level.is_empty() {
            let was = if t(r.get("level")) { s(r.get("level")) } else { "unset".into() };
            push_list(r, "marks", format!("{stamp}: {was} to {level}{note}"));
            r.insert("level".into(), json!(level));
        }
        if tick != 0 {
            if !t(r.get("ticks")) {
                return Err(E::Value(format!("{entry_id} has no clock")));
            }
            let n = int(r.get("ticks"))?;
            let filled = (int(Some(r.get("filled").unwrap_or(&json!(0))))? + tick).min(n).max(0);
            r.insert("filled".into(), json!(filled));
            push_list(r, "marks", format!("{stamp}: clock {filled}/{}{note}", s(r.get("ticks"))));
        }
        let out = rows[i].clone();
        save("ledger", &rows);
        return Ok(out);
    }
    Err(E::Key(entry_id.into()))
}

fn fire_rows(trigger: &str, thread: Option<&str>) -> R<Vec<Value>> {
    let key = trigger.trim().to_lowercase();
    if key.is_empty() {
        return Ok(vec![]);
    }
    let thread = thread.filter(|x| !x.is_empty());
    let mut rows = load("ledger")?;
    let mut hit = Vec::new();
    for i in 0..rows.len() {
        let r = &rows[i];
        let ok = r.get("status").and_then(Value::as_str) == Some("open")
            && t(r.get("due_trigger"))
            && !t(r.get("fired"))
            && (id_of(r)?.to_lowercase() == key || s(r.get("due_trigger")).to_lowercase().contains(&key))
            && thread.is_none_or(|th| !t(r.get("thread")) || same_thread(r.get("thread"), th));
        if ok {
            let stamp = stamp_for(rows[i].get("thread"))?;
            obj(&mut rows[i]).insert("fired".into(), json!(stamp));
            hit.push(rows[i].clone());
        }
    }
    if !hit.is_empty() {
        save("ledger", &rows);
    }
    Ok(hit)
}

fn ledger_collect_row(entry_id: &str, how: &str) -> R<Value> {
    let mut rows = load("ledger")?;
    for i in 0..rows.len() {
        if id_of(&rows[i])? == entry_id {
            let n = session_count()?;
            let r = obj(&mut rows[i]);
            r.insert("status".into(), json!("collected"));
            r.insert("collected".into(), json!({"session": n, "date": today(), "how": how}));
            let out = rows[i].clone();
            save("ledger", &rows);
            return Ok(out);
        }
    }
    Err(E::Key(entry_id.into()))
}

fn session_log(thread: &str, advanced: Vec<String>, came_due: Vec<String>, notes: &str, rulings: Vec<String>) -> R<Value> {
    let mut rows = load("sessions")?;
    let mut r = json!({"n": rows.len() + 1, "date": today(), "thread": thread, "advanced": advanced, "came_due": came_due, "notes": notes});
    if !rulings.is_empty() {
        obj(&mut r).insert("agent_rulings".into(), json!(rulings)); // R72-33: each write of the close, a call Isaac may overturn
    }
    rows.push(r.clone());
    save("sessions", &rows);
    Ok(r)
}

/// table.npc_set: `fields` holds only the fields given (None already dropped)
fn npc_set_row(name: &str, thread: &str, fields: Vec<(String, Value)>) -> R<Value> {
    let mut rows = load("npcs")?;
    for i in 0..rows.len() {
        let r = &rows[i];
        let nm = r.get("name").map(|v| s(Some(v))).ok_or(E::Key("name".into()))?;
        if nm.to_lowercase() == name.to_lowercase() && (thread.is_empty() || same_thread(r.get("thread"), thread)) {
            let o = obj(&mut rows[i]);
            for (k, v) in fields {
                o.insert(k, v);
            }
            o.insert("last_updated".into(), json!(today()));
            let out = rows[i].clone();
            save("npcs", &rows);
            return Ok(out);
        }
    }
    let mut r = json!({"name": name, "thread": thread, "want": null, "refusal_line": null, "knows": [], "lied_about": [], "last_seen": null, "voice": null});
    let o = obj(&mut r);
    for (k, v) in fields {
        o.insert(k, v);
    }
    o.insert("last_updated".into(), json!(today()));
    rows.push(r.clone());
    save("npcs", &rows);
    Ok(r)
}

/// table._terms
pub(crate) fn terms(r: &Value) -> R<Vec<String>> {
    let mut out = Vec::new();
    if t(r.get("thread")) {
        out.push(s(r.get("thread")));
    }
    if t(r.get("due_date")) {
        out.push(format!("due {}", s(r.get("due_date"))));
    }
    if t(r.get("due_trigger")) {
        out.push(format!("when {}{}", s(r.get("due_trigger")), if t(r.get("fired")) { format!(", fired {}", s(r.get("fired"))) } else { String::new() }));
    }
    if t(r.get("ticks")) {
        let (f, n) = (int(Some(r.get("filled").unwrap_or(&json!(0))))?, int(r.get("ticks"))?);
        out.push(format!("{}{} {f}/{n}", "●".repeat(f.max(0) as usize), "○".repeat((n - f).max(0) as usize)));
    }
    if t(r.get("level")) {
        out.push(format!("level: {}", s(r.get("level"))));
    }
    if t(r.get("due")) {
        out.push(format!("due: {}", s(r.get("due"))));
    }
    Ok(out)
}

fn firsts<'a>(rows: &'a [Value], f: impl Fn(&'a Value) -> String) -> Vec<String> {
    let mut seen: Vec<String> = Vec::new();
    for r in rows {
        let k = f(r);
        if !seen.contains(&k) {
            seen.push(k);
        }
    }
    seen
}

/// table.render: FRONTS.md, LEDGER.md and NPCS.md
fn render() -> R<()> {
    let dir = root("table");
    let _ = std::fs::create_dir_all(&dir);
    let fr = load("fronts")?;
    let mut lines = vec!["# Fronts, as clocks".to_string(), String::new()];
    for thread in firsts(&fr, |r| s(r.get("thread"))) {
        let sd = crate::table::thread_date(&thread)?;
        lines.push(format!("## {thread}{}", if t(sd.as_ref()) { format!(" · story date {}", s(sd.as_ref())) } else { String::new() }));
        lines.push(String::new());
        for r in fr.iter().filter(|x| s(x.get("thread")) == thread) {
            let (pos, n) = (int(Some(r.get("position").unwrap_or(&json!(0))))?, clock(r).len() as i64);
            let bar = format!("{}{}", "●".repeat(pos.max(0) as usize), "○".repeat((n - pos).max(0) as usize));
            let status = if r.get("status").is_some() { s(r.get("status")) } else { "open".into() };
            lines.push(format!("**{}** {bar} {pos}/{n} · {status}", s(r.get("name"))));
            if t(r.get("pace_days")) {
                lines.push(format!("- Pace: a tick every {} story days, {} spent", s(r.get("pace_days")), if r.get("days_banked").is_some() { s(r.get("days_banked")) } else { "0".into() }));
            }
            for (k, label) in [("want", "Want"), ("last_move", "Last move"), ("next_move", "Next move")] {
                if t(r.get(k)) {
                    lines.push(format!("- {label}: {}", s(r.get(k))));
                }
            }
            for tk in clock(r) {
                let mark = if int(tk.get("tick"))? <= pos { "x" } else { " " };
                lines.push(format!("  - [{mark}] {}. {}", s(tk.get("tick")), s(tk.get("consequence"))));
            }
            lines.push(String::new());
        }
    }
    let _ = std::fs::write(dir.join("FRONTS.md"), lines.join("\n"));

    let lg = load("ledger")?;
    let open = lg.iter().filter(|r| r.get("status").and_then(Value::as_str) == Some("open")).count();
    let mut lines = vec!["# The Ledger, structured".to_string(), String::new(), format!("{open} open lines."), String::new()];
    for cat in firsts(&lg, |r| s(r.get("category"))) {
        lines.push(format!("## {cat}"));
        lines.push(String::new());
        for r in lg.iter().filter(|x| s(x.get("category")) == cat) {
            let flag = if r.get("status").and_then(Value::as_str) == Some("collected") { "~~" } else { "" };
            let tm = terms(r)?;
            lines.push(format!("- `{}` {flag}{}{flag}{}", s(r.get("id")), s(r.get("text")), if tm.is_empty() { String::new() } else { format!("  *({})*", tm.join("; ")) }));
            for (k, label) in [("fed", "fed"), ("strained", "strained")] {
                for x in r.get(k).and_then(Value::as_array).into_iter().flatten() {
                    lines.push(format!("  - {label}: {}", s(Some(x))));
                }
            }
        }
        lines.push(String::new());
    }
    let _ = std::fs::write(dir.join("LEDGER.md"), lines.join("\n"));

    let np = load("npcs")?;
    let mut lines = vec!["# NPC roster".to_string(), String::new()];
    let th_of = |r: &Value| if r.get("thread").is_some() { s(r.get("thread")) } else { String::new() };
    for thread in firsts(&np, |r| th_of(r)) {
        lines.push(format!("## {thread}"));
        lines.push(String::new());
        for r in np.iter().filter(|x| th_of(x) == thread) {
            let or = |k: &str| if t(r.get(k)) { s(r.get(k)) } else { "—".into() };
            lines.push(format!("**{}** · wants: {} · refuses: {} · last seen: {}", s(r.get("name")), or("want"), or("refusal_line"), or("last_seen")));
            let list = |k: &str| r.get(k).and_then(Value::as_array).map(|a| a.iter().map(|x| s(Some(x))).collect::<Vec<_>>().join("; ")).unwrap_or_default();
            if t(r.get("knows")) {
                lines.push(format!("  - knows: {}", list("knows")));
            }
            if t(r.get("lied_about")) {
                lines.push(format!("  - has lied about: {}", list("lied_about")));
            }
            for (k, label) in [("lie", "live lie"), ("tell", "its tell"), ("doing_now", "doing now"), ("stands_with", "stands with him"), ("look", "look"), ("role", "role")] {
                if t(r.get(k)) {
                    lines.push(format!("  - {label}: {}", s(r.get(k))));
                }
            }
        }
        lines.push(String::new());
    }
    let _ = std::fs::write(dir.join("NPCS.md"), lines.join("\n"));
    Ok(())
}

pub(crate) fn table_commit(msg: &str) -> R<String> {
    render()?;
    git(&["add", "--", "table"]);
    git(&["commit", "-q", "-m", &format!("{msg}\n\nRecorded from the table via WOTR MCP."), "--", "table"]); // only table/, never what another session staged
    Ok(push(200))
}

fn offscreen_lines(ticks: &[Value]) -> Vec<String> {
    ticks
        .iter()
        .map(|r| format!("agent ruling: Front ticked offscreen: [{}] {} {}/{} ({}): {}", s(r.get("id")), s(r.get("name")), s(r.get("position")), clock(r).len(), s(r.get("status")), s(r.get("last_move"))))
        .collect()
}

// ---------------------------------------------------------------- the table tools
pub fn advance_front(front_id: &str, what: &str, next_move: &str) -> R<String> {
    match advance(front_id, what, next_move, "") {
        Err(E::Key(_)) => {
            let ids: Vec<String> = load("fronts")?.iter().map(|x| s(x.get("id"))).collect();
            Ok(format!("no Front with id '{front_id}'; ids: {}", ids.join(", ")))
        }
        Err(e) => Err(e),
        Ok(r) => {
            let n = clock(&r).len();
            let pushed = table_commit(&format!("Front advanced: {} -> {}/{n}", s(r.get("name")), s(r.get("position"))))?;
            let nm = if t(r.get("next_move")) { s(r.get("next_move")) } else { "unset".into() };
            Ok(format!("{} is at {}/{n} ({}); next tick: {nm}; {pushed}", s(r.get("name")), s(r.get("position")), s(r.get("status"))))
        }
    }
}

pub fn set_front_clock(front_id: &str, ticks: Option<Vec<String>>, pace_days: Option<i64>) -> R<String> {
    match set_clock(front_id, ticks.as_deref(), pace_days) {
        Err(E::Key(_)) => Ok(format!("no Front with id '{front_id}'")),
        Err(e) => Err(e),
        Ok(r) => {
            let pace = if t(r.get("pace_days")) { format!("pace {} days", s(r.get("pace_days"))) } else { "no pace".into() };
            Ok(format!("{}: {} ticks, {pace}; {}", s(r.get("name")), clock(&r).len(), table_commit(&format!("Front clock set: {}", s(r.get("name"))))?))
        }
    }
}

pub fn add_front(name: &str, thread: &str, want: &str, ticks: Vec<String>, next_move: &str, pace_days: Option<i64>) -> R<String> {
    let r = add_front_row(name, thread, want, &ticks, next_move, pace_days)?;
    Ok(format!("opened Front [{}] {name} in {thread}; {}", s(r.get("id")), table_commit(&format!("Front opened: {name}"))?))
}

pub fn pass_time(thread: &str, days: i64, story_date: &str) -> R<String> {
    if days < 0 {
        return Ok("time does not run back; to correct a date, pass story_date alone".into());
    }
    let (row, ticks) = match pass(thread, days, story_date) {
        Err(E::Value(e)) => return Ok(format!("not passed: {e}")),
        Err(e) => return Err(e),
        Ok(x) => x,
    };
    let sd = if t(row.get("story_date")) { s(row.get("story_date")) } else { "unset (pass story_date to hold one)".into() };
    let mut lines = vec![format!("{}: story date {sd}", s(row.get("thread")))];
    let off = offscreen_lines(&ticks);
    if off.is_empty() {
        lines.push("no Front's days are spent".into());
    } else {
        lines.extend(off);
    }
    Ok(format!("{}\n{}", lines.join("\n"), table_commit(&format!("Time passes on {}: {} offscreen tick(s)", s(row.get("thread")), ticks.len()))?))
}

#[allow(clippy::too_many_arguments)]
pub fn ledger_add(category: &str, who: &str, text: &str, due_after: Value, due_condition: &str, thread: &str, due_date: &str, due_trigger: &str, ticks: Option<i64>, level: &str) -> R<String> {
    let trig = if due_trigger.is_empty() { due_condition } else { due_trigger };
    let r = match ledger_add_row(category, who, text, due_after, thread, due_date, trig, ticks, level) {
        Err(E::Value(e)) => return Ok(format!("not entered: {e}")),
        Err(e) => return Err(e),
        Ok(r) => r,
    };
    let cat = s(r.get("category"));
    let mut gaps = Vec::new();
    if thread.is_empty() {
        gaps.push("no thread");
    }
    if !(STANDING.contains(&cat.as_str()) || !due_date.is_empty() || !trig.is_empty() || ticks.is_some_and(|n| n != 0)) {
        gaps.push("no story date or trigger");
    }
    let g = if gaps.is_empty() { String::new() } else { format!(" ({}, which R72-22 wants)", gaps.join(", ")) };
    Ok(format!("entered {} under '{cat}'{g}; {}", s(r.get("id")), table_commit(&format!("Ledger: {} {who}", s(r.get("id"))))?))
}

pub fn ledger_mark(entry_id: &str, fed: &str, strained: &str, level: &str, tick: i64, how: &str) -> R<String> {
    let r = match ledger_mark_row(entry_id, fed, strained, level, tick, how) {
        Err(E::Key(_)) => return Ok(format!("no ledger line '{entry_id}'")),
        Err(E::Value(e)) => return Ok(format!("not marked: {e}")),
        Ok(r) => r,
    };
    let tm = terms(&r)?;
    let what = if tm.is_empty() { s(r.get("category")) } else { tm.join("; ") };
    Ok(format!("{}: {what}; {}", s(r.get("id")), table_commit(&format!("Ledger marked: {}", s(r.get("id"))))?))
}

pub fn fire_trigger(trigger: &str, thread: &str) -> R<String> {
    let hit = fire_rows(trigger, Some(thread))?;
    if hit.is_empty() {
        return Ok(format!("no open line waits on '{trigger}'{}", if thread.is_empty() { String::new() } else { format!(" in {thread}") }));
    }
    let lines: Vec<String> = hit.iter().map(|r| format!("fired [{}] {}: {}", s(r.get("id")), s(r.get("due_trigger")), head(&s(r.get("text")), 120))).collect();
    Ok(format!("{}\n{}", lines.join("\n"), table_commit(&format!("Ledger fired: {trigger}"))?))
}

pub fn ledger_collect(entry_id: &str, how: &str) -> R<String> {
    match ledger_collect_row(entry_id, how) {
        Err(E::Key(_)) => Ok(format!("no ledger line '{entry_id}'")),
        Err(e) => Err(e),
        Ok(r) => Ok(format!("{} collected; {}", s(r.get("id")), table_commit(&format!("Ledger collected: {}", s(r.get("id"))))?)),
    }
}

const NPC_KEYS: [&str; 12] = ["want", "refusal_line", "knows", "lied_about", "last_seen", "voice", "lie", "tell", "doing_now", "stands_with", "look", "role"];

/// npc_set's arguments as table.npc_set receives them: strings `or None`, the two lists as given.
pub fn npc_fields(a: &Map<String, Value>) -> Vec<(String, Value)> {
    NPC_KEYS
        .iter()
        .filter_map(|k| {
            let v = a.get(*k)?;
            let keep = if *k == "knows" || *k == "lied_about" { !v.is_null() } else { t(Some(v)) };
            keep.then(|| (k.to_string(), v.clone()))
        })
        .collect()
}

pub fn npc_set(name: &str, thread: &str, fields: Vec<(String, Value)>) -> R<String> {
    let r = npc_set_row(name, thread, fields)?;
    Ok(format!("roster: {} ({thread}) updated; {}", s(r.get("name")), table_commit(&format!("Roster: {name}"))?))
}

// ---------------------------------------------------------------- session_end
fn act(applied: &mut Vec<String>, label: &str, f: impl FnOnce() -> R<String>) {
    match f() {
        Ok(x) => applied.push(format!("agent ruling: {x}")),
        Err(E::Key(k)) => applied.push(format!("not applied: {label}: unknown or missing '{k}'")),
        Err(E::Value(m)) => applied.push(format!("not applied: {label}: {m}")),
    }
}

fn need<'a>(a: &'a Value, k: &str) -> R<&'a Value> {
    a.get(k).ok_or(E::Key(k.into()))
}

/// a.get(k, "") as a str argument
fn arg(a: &Value, k: &str) -> String {
    match a.get(k) {
        None | Some(Value::Null) => String::new(),
        Some(v) => s(Some(v)),
    }
}

#[allow(clippy::too_many_arguments)]
pub fn session_end(thread: &str, scene_markdown: &str, title: &str, author_notes: &str, rulings: Vec<String>, notes: &str,
                   ledger: Vec<Value>, fronts: Vec<Value>, npcs: Vec<Value>, cards: Vec<Value>, fired: Vec<String>, days: i64, story_date: &str) -> R<String> {
    let (mut applied, mut ticked, mut came): (Vec<String>, Vec<String>, Vec<String>) = (vec![], vec![], vec![]);
    if days < 0 {
        applied.push("not applied: story time does not run back".into());
    } else if days != 0 || !story_date.is_empty() {
        match pass(thread, days, story_date) {
            Ok((row, tk)) => {
                let sd = if t(row.get("story_date")) { s(row.get("story_date")) } else { "unset".into() };
                applied.push(format!("agent ruling: story time on {}: date now {sd}", s(row.get("thread"))));
                applied.extend(offscreen_lines(&tk));
                ticked.extend(tk.iter().map(|r| s(r.get("id"))));
            }
            Err(E::Value(e)) => applied.push(format!("not applied: story time: {e}")),
            Err(e) => return Err(e),
        }
    }
    for trig in &fired {
        let hit = fire_rows(trig, Some(thread))?;
        came.extend(hit.iter().map(|r| s(r.get("id"))));
        applied.push(if hit.is_empty() {
            format!("not applied: no open line waits on '{trig}'")
        } else {
            format!("agent ruling: fired '{trig}': {}", hit.iter().map(|r| s(r.get("id"))).collect::<Vec<_>>().join(", "))
        });
    }
    for a in &ledger {
        let label = format!("Ledger line '{}'", head(&if a.get("text").is_some() { s(a.get("text")) } else { String::new() }, 60));
        act(&mut applied, &label, || {
            let th = if t(a.get("thread")) { s(a.get("thread")) } else { thread.to_string() };
            let trig = if t(a.get("due_trigger")) { s(a.get("due_trigger")) } else { arg(a, "due_condition") };
            let ticks = match a.get("ticks") {
                None | Some(Value::Null) => None,
                Some(v) => Some(int(Some(v))?),
            };
            let r = ledger_add_row(&s(Some(need(a, "category")?)), &arg(a, "who"), &s(Some(need(a, "text")?)), a.get("due_after_sessions").cloned().unwrap_or(Value::Null),
                                   &th, &arg(a, "due_date"), &trig, ticks, &arg(a, "level"))?;
            Ok(format!("Ledger {} entered ({}; {}): {}", s(r.get("id")), s(r.get("category")), terms(&r)?.join("; "), head(&s(r.get("text")), 160)))
        });
    }
    for a in &fronts {
        let label = format!("Front '{}'", s(a.get("front_id")));
        let mut tid = None;
        act(&mut applied, &label, || {
            let r = advance(&s(Some(need(a, "front_id")?)), &s(Some(need(a, "what_happened")?)), &arg(a, "next_move"), "")?;
            tid = Some(s(r.get("id")));
            Ok(format!("Front advanced: [{}] {} {}/{} ({}): {}", s(r.get("id")), s(r.get("name")), s(r.get("position")), clock(&r).len(), s(r.get("status")), s(r.get("last_move"))))
        });
        ticked.extend(tid);
    }
    for a in &npcs {
        let label = format!("roster '{}'", s(a.get("name")));
        act(&mut applied, &label, || {
            let f: Vec<(String, Value)> = NPC_KEYS.iter().filter(|k| t(a.get(**k))).map(|k| (k.to_string(), a[*k].clone())).collect();
            let th = if t(a.get("thread")) { s(a.get("thread")) } else { thread.to_string() };
            let r = npc_set_row(&s(Some(need(a, "name")?)), &th, f.clone())?;
            let shown: Vec<String> = f.iter().map(|(k, v)| format!("{k} {}", match v { Value::String(x) => x.clone(), Value::Array(l) => l.iter().map(|x| s(Some(x))).collect::<Vec<_>>().join("; "), o => s(Some(o)) })).collect();
            Ok(format!("roster: {}: {}", s(r.get("name")), shown.join("; ")))
        });
    }
    for a in &cards {
        let label = format!("card '{}'", s(a.get("name")));
        act(&mut applied, &label, || {
            let r = update_character(&s(Some(need(a, "name")?)), &s(Some(need(a, "markdown")?)));
            if r.starts_with("no card") {
                return Err(E::Value(r));
            }
            Ok(format!("card: {r}"))
        });
    }
    let notes = if rulings.is_empty() { notes.to_string() } else { format!("{notes}\nRulings: {}", rulings.join("; ")).trim().to_string() };
    let agent: Vec<String> = applied.iter().filter(|x| x.starts_with("agent ruling")).cloned().collect();
    let log = session_log(thread, ticked, came, &notes, agent)?;
    let pushed = table_commit(&format!("Session {} closed: {thread}, {} write(s)", s(log.get("n")), applied.len()))?;
    let archived = if !title.trim().is_empty() && !scene_markdown.trim().is_empty() {
        format!("; {}", archive_scene(title, scene_markdown, author_notes).split(';').next().unwrap_or(""))
    } else {
        String::new()
    };
    let failed: Vec<&String> = applied.iter().filter(|x| x.starts_with("not applied")).collect();
    let fail_txt = if failed.is_empty() {
        String::new()
    } else {
        format!("; {} not applied: {}", failed.len(), failed.iter().map(|x| x.strip_prefix("not applied: ").unwrap_or(x)).collect::<Vec<_>>().join(" | "))
    };
    Ok(format!("session {} upkeep done: {} write(s), table {pushed}{archived}{fail_txt}", s(log.get("n")), applied.len() - failed.len()))
}

// ---------------------------------------------------------------- scenes, the wiki, rulings
const MIRROR_SKIP: [&str; 6] = ["MANIFEST.md", "CONTINUITY.md", "CAST.md", "TIMELINE.md", "README.md", "00_SUPERSEDED_wrong_names.md"];

/// build/scenes_to_wiki.py: scenes/*.md mirrored as private vault pages; returns the line it prints.
pub(crate) fn scenes_to_wiki() -> String {
    let out = root("wiki/The Scene Archive/Scenes");
    let _ = std::fs::create_dir_all(&out);
    let mut ps: Vec<PathBuf> = std::fs::read_dir(root("scenes")).into_iter().flatten().flatten().map(|e| e.path()).filter(|p| p.extension().is_some_and(|x| x == "md")).collect();
    ps.sort();
    let mut made: Vec<String> = Vec::new();
    for p in ps {
        let fname = p.file_name().unwrap().to_string_lossy().into_owned();
        if MIRROR_SKIP.contains(&fname.as_str()) || fname.starts_with("00_") || fname.starts_with('_') {
            continue;
        }
        let md = crate::util::read_text(&p);
        let st = crate::util::stem(&p);
        let title = rx!(r"(?m)^#\s+(.+?)\s*$").captures(md.as_str()).ok().flatten().map(|c| c[1].trim().trim_matches('*').to_string()).unwrap_or_else(|| st.replace('_', " "));
        let mut name = rx!(r#"[/\\:*?"<>|]"#).replace_all(title.trim(), "").to_string();
        if name.is_empty() {
            name = st.clone();
        }
        if made.contains(&name) {
            name = format!("{name} ({st})");
        }
        made.push(name.clone());
        let body = rx!(r"\A#\s+.+\n+").replace(&md, "").to_string();
        let page = format!("---\ntitle: \"{name}\"\nprivate: true\nsource: scenes/{fname}\n---\n\n> Mirrored from `scenes/{fname}`; edit it there.\n\n{}\n", body.trim());
        let dst = out.join(format!("{name}.md"));
        if !dst.exists() || crate::util::read_text(&dst) != page {
            let _ = std::fs::write(&dst, page);
        }
    }
    let mut stale = 0;
    for e in std::fs::read_dir(&out).into_iter().flatten().flatten() {
        let q = e.path();
        if q.extension().is_some_and(|x| x == "md") && !made.contains(&crate::util::stem(&q)) {
            let _ = std::fs::remove_file(q);
            stale += 1;
        }
    }
    format!("{} scenes mirrored, {stale} stale removed", made.len())
}

pub fn archive_scene(title: &str, markdown: &str, author_notes: &str) -> String {
    let scenes = root("scenes");
    let slug = slug_us(title);
    let mut path = scenes.join(format!("{slug}.md"));
    if path.exists() {
        path = scenes.join(format!("{slug}_{}.md", date_fmt("%Y%m%d_%H%M")));
    }
    let mut body = markdown.trim().to_string();
    if !rx!(r"^#\s").is_match(&body).unwrap_or(false) {
        body = format!("# {title}\n\n{body}");
    }
    if !author_notes.trim().is_empty() {
        body += &format!("\n\n---\n\n## Author notes\n\n{}", author_notes.trim());
    }
    let _ = std::fs::create_dir_all(&scenes);
    let _ = std::fs::write(&path, format!("{body}\n"));
    scenes_to_wiki();
    let rel = crate::util::rel_posix(&path, &ROOT);
    git(&["add", "--", &rel, "wiki/The Scene Archive/Scenes"]);
    git(&["commit", "-q", "-m", &format!("Archive scene: {title}\n\nSaved from Claude Desktop via the wotr MCP server.")]);
    format!("saved {rel} ({} words); mirrored into wiki/The Scene Archive/Scenes; {}", words(&body), push(300).replace("pushed", "pushed to GitHub"))
}

/// Path::resolve() for a path that may not exist yet: '.' and '..' folded lexically.
fn normalize(p: &Path) -> PathBuf {
    let mut out = PathBuf::new();
    for c in p.components() {
        match c {
            Component::ParentDir => {
                out.pop();
            }
            Component::CurDir => {}
            c => out.push(c),
        }
    }
    out
}

pub fn wiki_write(path: &str, markdown: &str, message: &str) -> String {
    let wiki = root("wiki");
    let rel = PathBuf::from(path.trim().trim_start_matches('/'));
    let p = normalize(&wiki.join(&rel));
    let first = rel.components().next().map(|c| c.as_os_str().to_string_lossy().into_owned()).unwrap_or_default();
    if p.extension().is_none_or(|x| x != "md") || !p.starts_with(&wiki) || p == wiki || first.starts_with('.') {
        return "path must be a .md page inside wiki/".into();
    }
    let mut body = markdown.trim().to_string();
    if p.exists() && !body.starts_with("---") {
        if let Some(fm) = rx!(r"(?s)^---\n.*?\n---\n").find(&read_lossy(&p)).ok().flatten() {
            body = format!("{}\n{body}", fm.as_str());
        }
    }
    if let Some(d) = p.parent() {
        let _ = std::fs::create_dir_all(d);
    }
    let _ = std::fs::write(&p, format!("{body}\n"));
    let relp = rel.to_string_lossy().into_owned();
    git(&["add", "--", &crate::util::rel_posix(&p, &ROOT)]);
    let msg = if message.is_empty() { format!("Wiki: {relp}\n\nWritten via the wotr MCP server.") } else { message.to_string() };
    git(&["commit", "-q", "-m", &msg]);
    format!("wrote wiki/{relp} ({} words); {}", words(&body), push(200))
}

pub fn log_ruling(rule_id: &str, ruling: &str, context: &str) -> String {
    use std::io::Write;
    let p = root("RULINGS.md");
    let empty = std::fs::metadata(&p).map(|m| m.len() == 0).unwrap_or(true);
    if empty {
        let _ = std::fs::write(&p, "# Rulings awaiting application to the index\n\nAppended by the wotr MCP server when Isaac rules at the table. Each is applied to rules/*.yaml in Claude Code, then moved to PROGRESS.md.\n");
    }
    let mut entry = format!("\n## {} — {rule_id}\n\n{}\n", today(), ruling.trim());
    if !context.trim().is_empty() {
        entry += &format!("\nContext: {}\n", context.trim());
    }
    if let Ok(mut f) = std::fs::OpenOptions::new().append(true).open(&p) {
        let _ = f.write_all(entry.as_bytes());
    }
    git(&["add", "--", "RULINGS.md"]);
    git(&["commit", "-q", "-m", &format!("Log ruling on {rule_id}\n\nRecorded from Claude Desktop via the wotr MCP server.")]);
    format!("logged ruling on {rule_id}; {}", push(300))
}

pub fn propose_rule(title: &str, rule_text: &str, applies_to: &[String], rationale: &str, session: &str) -> String {
    use std::io::Write;
    let vocab: Vec<String> = {
        let body = read_lossy(&root("schema/applies_to.md"));
        rx!(r"(?m)^\|\s*`([a-z-]+)`").captures_iter(body.as_str()).flatten().map(|c| c[1].to_string()).collect()
    };
    let bad: Vec<String> = applies_to.iter().filter(|x| !vocab.contains(x)).cloned().collect();
    let p = root("proposals/PROPOSED.md");
    let _ = std::fs::create_dir_all(p.parent().unwrap());
    if !p.exists() {
        let _ = std::fs::write(&p, "# Proposed rules, pending Isaac's ratification\n\nFiled from the table via WOTR MCP. Each becomes a row in the next amendment pack, or is struck.\n");
    }
    let good: Vec<&String> = applies_to.iter().filter(|x| vocab.contains(x)).collect();
    let mut entry = format!(
        "\n## {} — {title}\n\n**Status:** proposed\n**applies_to:** {}{}\n\n{}\n",
        today(),
        good.iter().map(|x| x.as_str()).collect::<Vec<_>>().join(", "),
        if bad.is_empty() { String::new() } else { format!("  (unknown tags dropped: {})", crate::util::py_list(&bad)) },
        rule_text.trim()
    );
    if !rationale.trim().is_empty() {
        entry += &format!("\n*Why:* {}\n", rationale.trim());
    }
    if !session.trim().is_empty() {
        entry += &format!("\n*Session:* {}\n", session.trim());
    }
    if let Ok(mut f) = std::fs::OpenOptions::new().append(true).open(&p) {
        let _ = f.write_all(entry.as_bytes());
    }
    git(&["add", "--", "proposals/PROPOSED.md"]);
    git(&["commit", "-q", "-m", &format!("Propose rule: {title}\n\nFiled from Claude Desktop via WOTR MCP; pending ratification.")]);
    format!("filed '{title}' as proposed; {}", push(300))
}

// ---------------------------------------------------------------- character cards
pub(crate) fn manifest() -> Map<String, Value> {
    serde_json::from_str(&read_lossy(&root("wiki/.manifest.json"))).unwrap_or_default()
}

pub(crate) fn find_page(title: &str) -> Option<(String, String)> {
    let m = manifest();
    let tl = title.to_lowercase();
    let title_of = |v: &Value| s(v.get("title")).to_lowercase();
    m.iter()
        .find(|(_, v)| title_of(v) == tl)
        .or_else(|| m.iter().find(|(_, v)| title_of(v).contains(&tl)))
        .map(|(pid, v)| (pid.clone(), s(v.get("rel"))))
}

fn uuid4() -> String {
    let h = crate::keys::random_hex(16);
    let mut b: Vec<char> = h.chars().collect();
    b[12] = '4';
    b[16] = ['8', '9', 'a', 'b'][(b[16].to_digit(16).unwrap() & 3) as usize];
    let h: String = b.into_iter().collect();
    format!("{}-{}-{}-{}-{}", &h[..8], &h[8..12], &h[12..16], &h[16..20], &h[20..])
}

/// A page's text: the markdown replaces only the body. The header stays the one on disk, so tags and
/// `private: true` survive any update, and a header inside the markdown is dropped, never stacked.
fn mirror_text(existing: Option<&str>, title: &str, markdown: &str, tags: &[String], private: bool) -> String {
    let front = |t: &str| rx!(r"(?s)^---\n.*?\n---\n").find(t).ok().flatten().map(|m| m.end());
    let given = markdown.trim();
    let mut body = given[front(given).unwrap_or(0)..].trim().to_string();
    if !rx!(r"^#\s").is_match(&body).unwrap_or(false) {
        body = format!("# {title}\n\n{body}");
    }
    if let Some(old) = existing {
        if let Some(end) = front(old) {
            return format!("{}{body}\n", &old[..end]);
        }
    }
    let mut headl = vec!["---".to_string(), format!("title: {}", py_json(&json!(title)))];
    if !tags.is_empty() {
        headl.push(format!("tags: {}", py_json(&json!(tags))));
    }
    headl.push(format!("private: {}", if private { "true" } else { "false" }));
    headl.push("---".into());
    headl.push(String::new());
    format!("{}{body}\n", headl.join("\n"))
}

fn write_mirror(rel: &str, title: &str, pid: &str, markdown: &str, tags: &[String], private: bool) -> PathBuf {
    let p = root("wiki").join(rel);
    if let Some(d) = p.parent() {
        let _ = std::fs::create_dir_all(d);
    }
    let existing = p.exists().then(|| read_lossy(&p));
    let _ = std::fs::write(&p, mirror_text(existing.as_deref(), title, markdown, tags, private));
    let mut m = manifest();
    m.insert(pid.into(), json!({"rel": rel, "edited": now_iso(), "title": title, "private": private}));
    let _ = std::fs::write(root("wiki/.manifest.json"), py_json_indent(&Value::Object(m)));
    p
}

pub fn create_character(name: &str, markdown: &str, volume: &str, tags: Option<Vec<String>>) -> String {
    if let Some((pid, rel)) = find_page(name) {
        if s(manifest().get(&pid).and_then(|v| v.get("title"))).to_lowercase() == name.to_lowercase() {
            return format!("a card named '{name}' already exists ({rel}); use update_character");
        }
    }
    let Some((vol_id, vol_rel)) = find_page(volume) else {
        return format!("no volume page named '{volume}' in the wiki mirror");
    };
    let pid = uuid4();
    let section = s(manifest().get(&vol_id).and_then(|v| v.get("title")));
    let mut vol_dir = vol_rel.chars().take(chars(&vol_rel).saturating_sub(3)).collect::<String>();
    let parts: Vec<&str> = vol_dir.rsplitn(3, '/').collect(); // reversed: [last, parent, rest]
    if parts.len() >= 2 && parts[1] == parts[0] {
        vol_dir = vol_dir.rsplit_once('/').unwrap().0.to_string(); // the hub page already sits inside its folder
    }
    let rel = format!("{vol_dir}/{}.md", safe_name(name));
    let tags = tags.filter(|t| !t.is_empty()).unwrap_or_else(|| vec!["Characters".into()]);
    let p = write_mirror(&rel, name, &pid, markdown, &tags, true);
    git(&["add", "--", &crate::util::rel_posix(&p, &ROOT), "wiki/.manifest.json"]);
    git(&["commit", "-q", "-m", &format!("Add character card: {name}\n\nCreated from Claude Desktop via WOTR MCP; page {pid} under {section}.")]);
    format!("created '{name}' at wiki/{rel}; {}", push(200))
}

pub fn update_character(name: &str, markdown: &str) -> String {
    let Some((pid, rel)) = find_page(name) else {
        return format!("no card named '{name}' in the wiki mirror; use create_character");
    };
    let m = manifest();
    let title = s(m.get(&pid).and_then(|v| v.get("title")));
    let private = m.get(&pid).and_then(|v| v.get("private")).map(|v| t(Some(v))).unwrap_or(true);
    let path = root("wiki").join(&rel);
    let old = if path.exists() { read_page(&path) } else { String::new() };
    let p = write_mirror(&rel, &title, &pid, markdown, &[], private);
    git(&["add", "--", &crate::util::rel_posix(&p, &ROOT), "wiki/.manifest.json"]);
    git(&["commit", "-q", "-m", &format!("Update character card: {title}\n\nReplaced from Claude Desktop via WOTR MCP; page {pid}.")]);
    format!("updated '{title}' (page {pid}, {} words, was {}); {}", words(markdown), words(&old), push(200))
}

// ---------------------------------------------------------------- the inbox and the sync
fn inbox_pending() -> Vec<PathBuf> {
    let mut v: Vec<PathBuf> = std::fs::read_dir(root("inbox")).into_iter().flatten().flatten().map(|e| e.path()).filter(|p| p.is_file() && p.extension().is_some_and(|x| x == "md")).collect();
    v.sort();
    v
}

pub fn handoff(kind: &str, title: &str, body: &str, thread: &str) -> String {
    if kind != "research" && kind != "image" {
        return format!("unknown kind '{kind}'; use one of: research, image");
    }
    if body.trim().is_empty() || chars(body) > 200_000 {
        return "body must be non-empty and under 200,000 characters".into();
    }
    if inbox_pending().len() >= 200 {
        return "the inbox holds 200 unapplied items; nothing filed until Claude clears some".into();
    }
    let dir = root("inbox");
    let _ = std::fs::create_dir_all(&dir);
    let name = format!("{}-{kind}-{}.md", date_fmt("%Y%m%d-%H%M%S"), head(&slug_us(title), 50));
    let text = format!("---\nkind: {kind}\ntitle: {}\nthread: {}\nfiled: {}\n---\n\n{}\n", py_json(&json!(title)), py_json(&json!(thread)), now_iso(), body.trim());
    let _ = std::fs::write(dir.join(&name), text);
    format!("left in the inbox as {name}; a Claude session applies it next")
}

pub fn inbox(full: bool) -> String {
    let items = inbox_pending();
    if items.is_empty() {
        return "the inbox is empty".into();
    }
    let name = |p: &PathBuf| p.file_name().unwrap().to_string_lossy().into_owned();
    if !full {
        return format!("{} pending:\n{}", items.len(), items.iter().map(|p| format!("- {}", name(p))).collect::<Vec<_>>().join("\n"));
    }
    format!("{} pending\n\n{}", items.len(), items.iter().map(|p| format!("# {}\n\n{}", name(p), read_lossy(p))).collect::<Vec<_>>().join("\n\n---\n\n"))
}

pub fn inbox_done(name: &str, outcome: &str) -> String {
    let base = Path::new(name).file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let p = root("inbox").join(&base);
    if base.is_empty() || !p.is_file() {
        return format!("no pending item named {name}");
    }
    let done = root("inbox/done");
    let _ = std::fs::create_dir_all(&done);
    let _ = std::fs::write(&p, format!("{}\n\n**Outcome ({}):** {}\n", read_lossy(&p).trim_end(), today(), outcome.trim()));
    let _ = std::fs::rename(&p, done.join(&base));
    format!("closed {base}: {}", outcome.trim())
}

pub fn sync_now() -> String {
    // a child, so the embed model and a stuck push stay out of the server; /proc/<pid>/exe still
    // runs this binary after a rebuild has replaced the file on disk
    let exe = format!("/proc/{}/exe", std::process::id());
    let out = std::process::Command::new("timeout").args(["--kill-after=10", "900", exe.as_str(), "sync"]).current_dir(&*ROOT).output();
    match out {
        Ok(o) => {
            let text = format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)).trim().to_string();
            if text.is_empty() { format!("exit {}", o.status.code().unwrap_or(-1)) } else { tail(&text, 2000).to_string() }
        }
        Err(e) => e.to_string(),
    }
}

#[cfg(test)]
mod mirror_tests {
    use super::mirror_text;
    const OLD: &str = "---\ntitle: Cozbi\ntags:\n  - mahuo\nprivate: true\n---\n# Cozbi\n\nold body\n";

    #[test]
    fn a_body_update_keeps_the_header_on_disk() {
        assert_eq!(mirror_text(Some(OLD), "Cozbi", "# Cozbi\n\nnew body", &[], true), "---\ntitle: Cozbi\ntags:\n  - mahuo\nprivate: true\n---\n# Cozbi\n\nnew body\n");
    }

    #[test]
    fn a_header_in_the_markdown_is_dropped_not_stacked() {
        let given = "---\ntitle: Other\nprivate: false\n---\n# Cozbi\n\nnew body\n";
        assert_eq!(mirror_text(Some(OLD), "Cozbi", given, &[], false), "---\ntitle: Cozbi\ntags:\n  - mahuo\nprivate: true\n---\n# Cozbi\n\nnew body\n");
    }

    #[test]
    fn a_new_page_gets_a_built_header_and_a_heading() {
        assert_eq!(mirror_text(None, "Cozbi", "body", &["mahuo".to_string()], true), "---\ntitle: \"Cozbi\"\ntags: [\"mahuo\"]\nprivate: true\n---\n# Cozbi\n\nbody\n");
    }

    #[test]
    fn a_rule_in_the_body_is_not_taken_for_a_header() {
        let t = mirror_text(Some(OLD), "Cozbi", "# Cozbi\n\n---\n\nbelow the rule", &[], true);
        assert!(t.ends_with("# Cozbi\n\n---\n\nbelow the rule\n"), "{t}");
    }
}
