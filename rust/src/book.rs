//! `wotr-mcp book-memory`: a book's memory (state.json) checked, read for one person, and its cast
//! register written out as CAST.md. The pipeline runs the check between chapters, where review mode
//! puts no human (2026-11-07): a FAIL means the next brief would be built on bad memory.
use crate::ops::book_slug;
use crate::pyjson::dumps_unicode;
use crate::util::{read_lossy, root};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::PathBuf;

/// The closed list of fact kinds (wotr-book §4); a free-text kind is what let the old checks go blind.
pub const KINDS: &[&str] = &[
    "fact", "time", "location", "object", "money", "debt", "promise", "name", "look", "gear", "wound", "healed", "death", "returned",
    "move", "skill", "level", "stage", "grade", "class", "title", "vow", "bond", "knows", "reader_knows", "lie", "renown", "profession",
];
/// Kinds that are about a person, so the subject must be in the cast register.
const PERSON: &[&str] = &[
    "look", "gear", "wound", "healed", "death", "returned", "move", "skill", "level", "stage", "grade", "class", "title", "vow", "bond",
    "knows", "reader_knows", "lie", "renown", "profession",
];
/// Kinds only the living can have after a death, until a `returned` fact (a corpse can still be moved,
/// described, titled, bonded or lied about).
const ACTS: &[&str] = &["healed", "move", "skill", "level", "stage", "grade", "class", "vow", "knows"];
const TIERS: &[&str] = &["lead", "major", "recurring", "walk-on"];
/// The register fields a lead or major entry carries, the way the main character's does.
const FULL: &[&str] = &["look", "voice", "want", "refusal", "kit", "sheet", "bonds"];

fn s<'a>(v: &'a Value, k: &str) -> &'a str {
    v.get(k).and_then(Value::as_str).unwrap_or("")
}

fn arr<'a>(v: &'a Value, k: &str) -> &'a [Value] {
    v.get(k).and_then(Value::as_array).map(Vec::as_slice).unwrap_or(&[])
}

fn ch(v: &Value) -> i64 {
    v.get("ch").and_then(Value::as_i64).unwrap_or(0)
}

/// A register field as text, whatever shape an agent wrote it in: arrays joined, objects as JSON.
fn field(v: &Value, k: &str) -> String {
    fn text(x: &Value) -> String {
        match x {
            Value::Null => String::new(),
            Value::String(t) => t.clone(),
            Value::Array(items) => items.iter().map(text).filter(|t| !t.is_empty()).collect::<Vec<_>>().join("; "),
            other => other.to_string(),
        }
    }
    v.get(k).map(text).unwrap_or_default().trim().to_string()
}

/// What a quote must survive to be found: curly quotes, italics marks, line breaks and case.
fn norm(t: &str) -> String {
    let t: String = t.chars().filter(|c| !matches!(c, '*' | '_')).map(|c| match c {
        '\u{2018}' | '\u{2019}' => '\'',
        '\u{201C}' | '\u{201D}' => '"',
        c => c,
    }).collect();
    t.split_whitespace().collect::<Vec<_>>().join(" ").to_lowercase()
}

/// A keyword as a whole word or phrase: "stay" does not match "stayed", "wall" not "swallowed".
fn has_word(text: &str, kw: &str) -> bool {
    let word = |c: Option<char>| c.is_some_and(char::is_alphanumeric);
    text.match_indices(kw).any(|(i, m)| !word(text[..i].chars().next_back()) && !word(text[i + m.len()..].chars().next()))
}

fn short(t: &str, n: usize) -> String {
    if t.chars().count() <= n { t.to_string() } else { format!("{}...", t.chars().take(n).collect::<String>()) }
}

struct Book {
    dir: PathBuf,
    outline: Value,
    state: Value,
    /// lowercase name or alias -> the register name
    names: BTreeMap<String, String>,
    /// aliases claimed by two register entries, or colliding with another person's name
    clashes: Vec<String>,
    /// chapter -> normalized final.md, for chapters inside the bound and not dropped
    finals: BTreeMap<i64, String>,
    dropped: BTreeSet<i64>,
    /// only chapters before this one count (a rewrite or a brief must not see its own or later chapters)
    before: Option<i64>,
}

fn load(slug: &str, before: Option<i64>) -> Result<Book, String> {
    let dir = root("book").join(slug);
    let read = |f: &str| -> Result<Value, String> {
        let p = dir.join(f);
        if !p.exists() {
            return Err(format!("book/{slug}/{f} does not exist"));
        }
        serde_json::from_str(&read_lossy(&p)).map_err(|e| format!("book/{slug}/{f}: {e}"))
    };
    let (outline, state) = (read("outline.json")?, read("state.json")?);
    let gates = if dir.join("gates.json").exists() { read("gates.json")? } else { Value::Null };
    let dropped: BTreeSet<i64> = gates.as_object().into_iter().flatten().filter(|(_, d)| s(d, "decision") == "dropped").filter_map(|(n, _)| n.parse().ok()).collect();
    let (mut names, mut clashes) = (BTreeMap::new(), Vec::new());
    let cast = arr(&state, "cast");
    for c in cast {
        let name = s(c, "name");
        if name.is_empty() {
            continue;
        }
        if let Some(prev) = names.insert(name.to_lowercase(), name.to_string()) {
            clashes.push(format!("'{name}' has two register entries ({prev})"));
        }
    }
    for c in cast {
        let name = s(c, "name");
        for a in arr(c, "aliases").iter().filter_map(Value::as_str) {
            match names.get(&a.to_lowercase()) {
                Some(owner) if owner != name => clashes.push(format!("alias '{a}' of '{name}' is already '{owner}'")),
                Some(_) => {}
                None => {
                    names.insert(a.to_lowercase(), name.to_string());
                }
            }
        }
    }
    let mut finals = BTreeMap::new();
    for c in arr(&outline, "chapters") {
        if let Some(n) = c.get("number").and_then(Value::as_i64) {
            let p = dir.join(format!("ch{n:02}/final.md"));
            if p.exists() && !dropped.contains(&n) && before.is_none_or(|b| n < b) {
                finals.insert(n, norm(&read_lossy(&p)));
            }
        }
    }
    Ok(Book { dir, outline, state, names, clashes, finals, dropped, before })
}

impl Book {
    fn canon(&self, subject: &str) -> String {
        self.names.get(&subject.to_lowercase()).cloned().unwrap_or_else(|| subject.to_string())
    }
    fn counts(&self, f: &Value) -> bool {
        self.before.is_none_or(|b| ch(f) < b) && !self.dropped.contains(&ch(f))
    }
    fn facts(&self) -> Vec<&Value> {
        arr(&self.state, "facts").iter().filter(|f| self.counts(f)).collect()
    }
    fn facts_of(&self, name: &str) -> Vec<&Value> {
        self.facts().into_iter().filter(|f| self.canon(s(f, "subject")) == name).collect()
    }
    /// The chapter each person died in, and the chapter they came back in, if they did.
    fn deaths(&self) -> BTreeMap<String, (i64, Option<i64>)> {
        let mut out: BTreeMap<String, (i64, Option<i64>)> = BTreeMap::new();
        for f in self.facts().into_iter().filter(|f| s(f, "kind") == "death") {
            let e = out.entry(self.canon(s(f, "subject"))).or_insert((ch(f), None));
            e.0 = e.0.min(ch(f));
        }
        for f in self.facts().into_iter().filter(|f| s(f, "kind") == "returned") {
            if let Some(e) = out.get_mut(&self.canon(s(f, "subject"))).filter(|e| e.0 <= ch(f)) {
                e.1 = Some(e.1.map_or(ch(f), |r| r.min(ch(f))));
            }
        }
        out
    }
    /// Wounds no later `healed` fact names in its `heals` field; a healed fact that names nothing closes nothing.
    fn open_wounds(&self, name: &str) -> Vec<String> {
        let facts = self.facts_of(name);
        let heals: Vec<(i64, String)> = facts.iter().filter(|f| s(f, "kind") == "healed").map(|f| (ch(f), norm(s(f, "heals")))).filter(|(_, h)| !h.is_empty()).collect();
        facts.iter().filter(|f| s(f, "kind") == "wound").filter(|w| {
            let text = norm(s(w, "fact"));
            !heals.iter().any(|(c, h)| *c >= ch(w) && (text.contains(h.as_str()) || h.contains(text.as_str())))
        }).map(|w| format!("{} (ch {})", s(w, "fact"), ch(w))).collect()
    }
}

/// Every fault in the book's memory, as (FAIL | WARN, message).
fn check(b: &Book) -> Vec<(&'static str, String)> {
    let mut out: Vec<(&'static str, String)> = b.clashes.iter().map(|c| ("FAIL", format!("register: {c}"))).collect();
    for (i, f) in arr(&b.state, "facts").iter().enumerate() {
        let (n, subject, kind, quote) = (ch(f), s(f, "subject"), s(f, "kind"), s(f, "quote"));
        let at = format!("fact {} (ch {n}, {subject}, {kind})", i + 1);
        if b.dropped.contains(&n) {
            out.push(("WARN", format!("{at}: chapter {n} was dropped; remove its facts")));
            continue;
        }
        if !b.counts(f) {
            continue;
        }
        if !KINDS.contains(&kind) {
            out.push(("FAIL", format!("{at}: kind '{kind}' is not one of {}", KINDS.join(", "))));
        }
        if PERSON.contains(&kind) && !b.names.contains_key(&subject.to_lowercase()) {
            out.push(("FAIL", format!("{at}: '{subject}' is not in the cast register; add them to state.json cast or use their register name")));
        }
        match b.finals.get(&n) {
            None => out.push(("FAIL", format!("{at}: chapter {n} has no final.md"))),
            Some(_) if quote.trim().is_empty() => out.push(("FAIL", format!("{at}: no quote (no quote, no fact)"))),
            Some(text) if !text.contains(&norm(quote)) => out.push(("FAIL", format!("{at}: quote not in ch{n:02}/final.md: \"{}\"", short(quote, 90)))),
            _ => {}
        }
    }
    let deaths = b.deaths();
    for f in b.facts() {
        let (n, who, kind) = (ch(f), b.canon(s(f, "subject")), s(f, "kind"));
        if let Some((d, back)) = deaths.get(&who) {
            if *d < n && back.is_none_or(|r| n < r) && ACTS.contains(&kind) {
                out.push(("FAIL", format!("{who} died in ch {d} but has a '{kind}' fact in ch {n} (a `returned` fact marks a return): \"{}\"", short(s(f, "quote"), 90))));
            }
        }
    }
    let summarized: BTreeSet<i64> = arr(&b.state, "summaries").iter().map(ch).collect();
    for n in b.finals.keys().filter(|n| !summarized.contains(n)) {
        out.push(("FAIL", format!("ch {n} has a final.md and no summary: its memory is owed (wotr-book §4)")));
    }
    let last = b.finals.keys().max().copied().unwrap_or(0);
    for h in arr(&b.state, "hooks") {
        let (id, status) = (s(h, "hook_id"), s(h, "status"));
        if status == "paid" || status == "planned" || status.is_empty() {
            continue;
        }
        if let Some(due) = h.get("due_ch").and_then(Value::as_i64).filter(|d| *d < last) {
            out.push(("WARN", format!("hook {id} was due by ch {due} and is {status}")));
        }
        let planted = h.get("planted_ch").and_then(Value::as_i64).unwrap_or(0);
        let mut logged: BTreeSet<i64> = ["planted_ch", "paid_ch"].iter().filter_map(|k| h.get(*k).and_then(Value::as_i64)).collect();
        logged.extend(arr(h, "events").iter().filter_map(|e| e.as_i64().or_else(|| e.get("ch").and_then(Value::as_i64))));
        let kws: Vec<String> = arr(h, "keywords").iter().filter_map(Value::as_str).map(norm).filter(|k| !k.is_empty()).collect();
        if kws.len() >= 2 {
            for (n, text) in b.finals.iter().filter(|(n, _)| **n >= planted && !logged.contains(n)) {
                if kws.iter().all(|k| has_word(text, k)) {
                    out.push(("WARN", format!("hook {id}: all its keywords appear in ch {n}, which logs no event for it")));
                }
            }
        }
    }
    for c in arr(&b.state, "cast") {
        let (name, tier) = (s(c, "name"), s(c, "tier"));
        if !TIERS.contains(&tier) {
            out.push(("FAIL", format!("cast '{name}': tier '{tier}' is not one of {}", TIERS.join(", "))));
        }
        if field(c, "profession").is_empty() {
            out.push(("FAIL", format!("cast '{name}' has no profession")));
        }
        if age(c).is_none() {
            out.push(("WARN", format!("cast '{name}' has no age (an explicit chapter needs one for everyone in it)")));
        }
        if matches!(tier, "lead" | "major") {
            let missing: Vec<&str> = FULL.iter().copied().filter(|k| field(c, k).is_empty()).collect();
            if !missing.is_empty() {
                out.push(("WARN", format!("{tier} '{name}' has no {}", missing.join(", "))));
            }
        }
    }
    for c in arr(&b.outline, "chapters") {
        let n = c.get("number").and_then(Value::as_i64).unwrap_or(0);
        if !b.finals.contains_key(&n) {
            continue;
        }
        for who in arr(c, "cast").iter().filter_map(Value::as_str) {
            let generic = who.chars().next().is_some_and(char::is_lowercase);
            if !generic && !b.names.contains_key(&who.to_lowercase()) {
                out.push(("WARN", format!("ch {n} lists '{who}' in its cast and the register has no entry")));
            }
        }
    }
    out
}

/// A register person's age in years, from a number or the first number in a string ("about 40").
fn age(c: &Value) -> Option<i64> {
    match c.get("age") {
        Some(Value::Number(n)) => n.as_i64(),
        Some(Value::String(t)) => t.split(|ch: char| !ch.is_ascii_digit()).find(|p| !p.is_empty()).and_then(|p| p.parse().ok()),
        _ => None,
    }
}

/// The floor for an explicit chapter (NATALIE.md, The Floor): everyone in its cast has an age on file, and every age is eighteen or more.
fn floor(b: &Book, n: i64) -> Vec<(&'static str, String)> {
    let mut out = Vec::new();
    let row = arr(&b.outline, "chapters").iter().find(|c| c.get("number").and_then(Value::as_i64) == Some(n));
    let Some(row) = row else { return vec![("FAIL", format!("the outline has no chapter {n}"))] };
    for who in arr(row, "cast").iter().filter_map(Value::as_str) {
        let name = b.canon(who);
        match arr(&b.state, "cast").iter().find(|c| s(c, "name") == name) {
            None => out.push(("FAIL", format!("'{who}' in explicit chapter {n} has no register entry, so no age on file"))),
            Some(c) => match age(c) {
                None => out.push(("FAIL", format!("'{name}' in explicit chapter {n} has no age on file"))),
                Some(a) if a < 18 => out.push(("FAIL", format!("'{name}' in explicit chapter {n} is {a}: under eighteen"))),
                _ => {}
            },
        }
    }
    out
}

/// A rewrite starts clean: chapter N's facts, summary, hook events and arc lines leave the memory.
fn purge(b: &mut Book, n: i64) -> String {
    let st = &mut b.state;
    let mut gone = BTreeMap::new();
    for k in ["facts", "summaries"] {
        if let Some(list) = st.get_mut(k).and_then(Value::as_array_mut) {
            let was = list.len();
            list.retain(|x| ch(x) != n);
            gone.insert(k, was - list.len());
        }
    }
    let mut events = 0;
    for h in st.get_mut("hooks").and_then(Value::as_array_mut).into_iter().flatten() {
        if let Some(list) = h.get_mut("events").and_then(Value::as_array_mut) {
            let was = list.len();
            list.retain(|e| e.as_i64().or_else(|| e.get("ch").and_then(Value::as_i64)) != Some(n));
            events += was - list.len();
        }
        if h.get("paid_ch").and_then(Value::as_i64) == Some(n) {
            if let Some(o) = h.as_object_mut() {
                o.remove("paid_ch");
                let left = o.get("events").and_then(Value::as_array).map_or(0, Vec::len);
                o.insert("status".into(), Value::String(if left > 0 { "advanced".into() } else { "planted".into() }));
            }
        }
    }
    let mut arcs = 0;
    for c in st.get_mut("cast").and_then(Value::as_array_mut).into_iter().flatten() {
        if let Some(list) = c.get_mut("arc").and_then(Value::as_array_mut) {
            let was = list.len();
            list.retain(|a| ch(a) != n);
            arcs += was - list.len();
        }
    }
    format!("purged ch {n}: {} facts, {} summaries, {events} hook events, {arcs} arc lines (register entries kept)", gone.get("facts").unwrap_or(&0), gone.get("summaries").unwrap_or(&0))
}

/// One person's state in this book, for the brief: the register entry, open wounds, and the facts
/// newest first with their chapters and quotes.
fn person(b: &Book, asked: &str) -> String {
    let name = b.canon(asked);
    let bound = b.before.map_or(String::new(), |n| format!(" (as of the start of chapter {n})"));
    let mut lines = vec![format!("# {name}{bound}")];
    match arr(&b.state, "cast").iter().find(|c| s(c, "name") == name) {
        Some(c) => {
            for k in ["profession", "tier", "age", "role", "culture", "look", "voice", "want", "refusal", "lie", "kit", "sheet", "bonds"] {
                let v = field(c, k);
                if !v.is_empty() {
                    lines.push(format!("- {k}: {v}"));
                }
            }
            for a in arr(c, "arc").iter().filter(|a| b.counts(a)) {
                lines.push(format!("- arc, ch {}: {}", ch(a), s(a, "line")));
            }
        }
        None => lines.push("- not in the cast register".into()),
    }
    if let Some((d, back)) = b.deaths().get(&name) {
        lines.push(match back {
            Some(r) => format!("- died in ch {d}, returned in ch {r}"),
            None => format!("- DEAD since ch {d}"),
        });
    }
    let open = b.open_wounds(&name);
    if !open.is_empty() {
        lines.push(format!("- open wounds: {}", open.join("; ")));
    }
    lines.push(String::new());
    let mut facts = b.facts_of(&name);
    facts.sort_by_key(|f| std::cmp::Reverse(ch(f)));
    for f in facts {
        lines.push(format!("- ch {} {}: {} (\"{}\")", ch(f), s(f, "kind"), s(f, "fact"), short(s(f, "quote"), 140)));
    }
    lines.join("\n")
}

/// CAST.md: everyone in the register, the lead and major people in full, the rest by line.
fn render(b: &Book) -> String {
    let title = if s(&b.outline, "title").is_empty() { "the book" } else { s(&b.outline, "title") };
    let upto = b.finals.keys().max().map_or("before chapter 1".to_string(), |n| format!("through chapter {n}"));
    let mut out = vec![
        format!("# The cast of {title}"),
        String::new(),
        format!("Everyone the book has named, with their profession and where they stand, {upto}. Written by `wotr-mcp book-memory --render` from state.json: change state.json, not this file."),
    ];
    let span = |c: &Value| -> String {
        let seen: Vec<i64> = b.facts_of(s(c, "name")).iter().map(|f| ch(f)).collect();
        let (lo, hi) = (seen.iter().min().copied().unwrap_or(0), seen.iter().max().copied().unwrap_or(0));
        let first = c.get("first_ch").and_then(Value::as_i64).filter(|n| *n > 0).unwrap_or(lo);
        match (first, hi.max(first)) {
            (0, _) => "not yet on the page".into(),
            (a, z) if a == z => format!("ch {a}"),
            (a, z) => format!("ch {a} to {z}"),
        }
    };
    let cast = arr(&b.state, "cast");
    for (tier, heading) in [("lead", "The lead"), ("major", "Major")] {
        let people: Vec<&Value> = cast.iter().filter(|c| s(c, "tier") == tier).collect();
        if people.is_empty() {
            continue;
        }
        out.extend([String::new(), format!("## {heading}")]);
        for c in people {
            out.extend([String::new(), format!("### {}, {}", s(c, "name"), field(c, "profession")), String::new(), format!("*{}.*", span(c))]);
            for (k, label) in [("age", "Age"), ("role", "Role"), ("culture", "From"), ("look", "Look and kit"), ("voice", "Voice"), ("want", "Wants"), ("refusal", "Refuses"), ("lie", "Lies about"), ("kit", "Power"), ("sheet", "Sheet"), ("bonds", "Bonds")] {
                let v = field(c, k);
                if !v.is_empty() {
                    out.push(format!("- **{label}:** {v}"));
                }
            }
            // the newest fact of each kind, by chapter (file order breaks ties)
            let mut latest: BTreeMap<&str, &Value> = BTreeMap::new();
            for f in b.facts_of(s(c, "name")) {
                let k = s(f, "kind");
                if ["location", "gear", "wound", "healed", "title", "level", "stage", "grade", "skill", "class", "bond", "debt", "vow", "renown", "knows", "death", "returned"].contains(&k)
                    && latest.get(k).is_none_or(|old| ch(old) <= ch(f))
                {
                    latest.insert(k, f);
                }
            }
            if !latest.is_empty() {
                let now: Vec<String> = latest.iter().map(|(k, f)| format!("{k} (ch {}): {}", ch(f), s(f, "fact"))).collect();
                out.push(format!("- **Now:** {}", now.join("; ")));
            }
            let open = b.open_wounds(s(c, "name"));
            if !open.is_empty() {
                out.push(format!("- **Open wounds:** {}", open.join("; ")));
            }
            for a in arr(c, "arc") {
                out.push(format!("- **Ch {}:** {}", ch(a), s(a, "line")));
            }
        }
    }
    for (tier, heading) in [("recurring", "Recurring"), ("walk-on", "Walk-ons")] {
        let people: Vec<&Value> = cast.iter().filter(|c| s(c, "tier") == tier).collect();
        if people.is_empty() {
            continue;
        }
        out.extend([String::new(), format!("## {heading}"), String::new(), "| Name | Profession | Chapters | Who they are |".into(), "|---|---|---|---|".into()]);
        for c in people {
            let who = [field(c, "role"), field(c, "look")].into_iter().filter(|x| !x.is_empty()).collect::<Vec<_>>().join("; ");
            out.push(format!("| {} | {} | {} | {} |", s(c, "name"), field(c, "profession"), span(c), who.replace('|', "/")));
        }
    }
    out.push(String::new());
    out.join("\n")
}

/// `wotr-mcp book-memory [--slug S] [--before N] [--name NAME | --render | --floor N | --purge N]`;
/// with no action flag, the check (exit 1 on any FAIL). Every failure prints a line starting FAIL.
pub fn memory(args: &[String]) -> i32 {
    let opt = |f: &str| args.iter().position(|a| a == f).and_then(|i| args.get(i + 1)).map(String::as_str);
    let num = |f: &str| opt(f).and_then(|v| v.parse::<i64>().ok());
    let run = || -> Result<i32, String> {
        let slug = book_slug(opt("--slug"))?;
        if let Some(n) = num("--purge") {
            let mut b = load(&slug, None)?;
            let said = purge(&mut b, n);
            fs::write(b.dir.join("state.json"), dumps_unicode(&b.state, Some(1)) + "\n").map_err(|e| e.to_string())?;
            println!("{said}");
            return Ok(0);
        }
        let b = load(&slug, num("--before"))?;
        if let Some(name) = opt("--name") {
            println!("{}", person(&b, name));
            return Ok(0);
        }
        if args.iter().any(|a| a == "--render") {
            fs::write(b.dir.join("CAST.md"), render(&b)).map_err(|e| e.to_string())?;
            println!("wrote book/{slug}/CAST.md ({} people)", arr(&b.state, "cast").len());
            return Ok(0);
        }
        let (found, what) = match num("--floor") {
            Some(n) => (floor(&b, n), format!("the floor for chapter {n}")),
            None => (check(&b), format!("{} facts, {} hooks, {} people, {} written chapters", arr(&b.state, "facts").len(), arr(&b.state, "hooks").len(), arr(&b.state, "cast").len(), b.finals.len())),
        };
        let fails = found.iter().filter(|(sev, _)| *sev == "FAIL").count();
        for (sev, m) in &found {
            println!("{sev} {m}");
        }
        println!("{slug}: {fails} FAIL, {} WARN over {what}", found.len() - fails);
        Ok(if fails > 0 { 1 } else { 0 })
    };
    match run() {
        Ok(code) => code,
        Err(e) => {
            println!("FAIL {e}");
            1
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{has_word, norm};

    #[test]
    fn quotes_survive_curly_marks_italics_and_breaks() {
        assert_eq!(norm("He said, \u{201C}Chapman\u{2019}s *here*\u{201D}\n  again."), "he said, \"chapman's here\" again.");
        assert!(norm("The *sword*, he said, had\nbelonged to four men.").contains(&norm("the sword, he said, had belonged")));
    }

    #[test]
    fn keywords_match_whole_words() {
        assert!(has_word("the four lines were refused", "four lines"));
        assert!(!has_word("he swallowed and stayed", "wall"));
        assert!(!has_word("he stayed", "stay"));
        assert!(has_word("stay, he said", "stay"));
    }
}
