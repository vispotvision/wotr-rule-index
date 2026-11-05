//! The rule index's gate: `wotr-mcp validate` must exit 0 before a pack counts as done (fix the data,
//! not the checker), and `wotr-mcp resolve` writes out/ from the supersession graph. Resolve settles
//! nothing the source did not state: a supersession link came from a quotable line in a pack.
use crate::pyjson::dumps_unicode;
use crate::pyyaml;
use crate::rules::vocab;
use crate::util::{read_lossy, rglob_md, root};
use regex::Regex;
use serde_json::{Map, Value};
use std::collections::{BTreeMap, BTreeSet, HashMap};

struct Row {
    file: String,
    v: Map<String, Value>,
}

/// Every rule row in rules/*.yaml with its file, typed by YAML 1.1 as the packs were written.
fn load() -> Result<Vec<Row>, String> {
    let mut files: Vec<_> = std::fs::read_dir(root("rules"))
        .map_err(|e| format!("rules/: {e}"))?
        .flatten()
        .map(|e| e.path())
        .filter(|p| p.extension().is_some_and(|x| x == "yaml"))
        .collect();
    files.sort();
    let mut rows = Vec::new();
    for p in files {
        let doc = pyyaml::load(&read_lossy(&p)).map_err(|e| format!("{}: {e}", p.display()))?;
        let file = p.file_name().unwrap_or_default().to_string_lossy().into_owned();
        for r in doc.get("rules").and_then(Value::as_array).into_iter().flatten() {
            let v = r.as_object().ok_or_else(|| format!("{file}: a rule row is not a mapping"))?.clone();
            rows.push(Row { file: file.clone(), v });
        }
    }
    Ok(rows)
}

fn text<'a>(r: &'a Map<String, Value>, k: &str) -> &'a str {
    r.get(k).and_then(Value::as_str).unwrap_or("")
}

fn list<'a>(r: &'a Map<String, Value>, k: &str) -> impl Iterator<Item = &'a str> {
    r.get(k).and_then(Value::as_array).into_iter().flatten().filter_map(Value::as_str)
}

fn pack(r: &Map<String, Value>) -> i64 {
    r.get("pack_number").and_then(Value::as_i64).unwrap_or(0)
}

/// common.normalise: no emphasis marks, straight quotes, one space, so a quote survives its markdown.
fn normalise(t: &str) -> String {
    let t: String = t
        .chars()
        .filter(|c| !matches!(c, '*' | '_' | '`'))
        .map(|c| match c {
            '\u{2018}' | '\u{2019}' => '\'',
            '\u{201c}' | '\u{201d}' => '"',
            c => c,
        })
        .collect();
    t.split_whitespace().collect::<Vec<_>>().join(" ")
}

fn repr(v: &Value) -> String {
    match v {
        Value::String(s) => format!("'{s}'"),
        Value::Null => "None".into(),
        Value::Bool(b) => if *b { "True" } else { "False" }.into(),
        o => o.to_string(),
    }
}

fn is_type(v: &Value, t: &str) -> bool {
    match t {
        "string" => v.is_string(),
        "object" => v.is_object(),
        "array" => v.is_array(),
        "null" => v.is_null(),
        "boolean" => v.is_boolean(),
        "number" => v.is_number(),
        "integer" => v.is_i64() || v.is_u64() || v.as_f64().is_some_and(|f| f.fract() == 0.0),
        _ => false,
    }
}

/// The draft-7 keywords schema/rule.schema.json uses. A keyword outside them is reported, so a schema
/// edit can never pass rows unchecked here.
fn check(s: &Value, v: &Value, path: &str, rx: &mut HashMap<String, Regex>, errs: &mut Vec<String>) {
    let at = |e: &mut Vec<String>, m: String| e.push(format!("schema: {}: {m}", if path.is_empty() { "<root>" } else { path }));
    let child = |k: &str| if path.is_empty() { k.to_string() } else { format!("{path}.{k}") };
    for (key, want) in s.as_object().into_iter().flatten() {
        match key.as_str() {
            "$schema" | "title" | "description" => {}
            "type" => {
                let names: Vec<&str> = want.as_str().map(|t| vec![t]).unwrap_or_else(|| want.as_array().into_iter().flatten().filter_map(Value::as_str).collect());
                if !names.iter().any(|t| is_type(v, t)) {
                    let quoted: Vec<String> = names.iter().map(|t| format!("'{t}'")).collect();
                    at(errs, format!("{} is not of type {}", repr(v), quoted.join(", ")));
                }
            }
            "required" => {
                if let Some(o) = v.as_object() {
                    for k in want.as_array().into_iter().flatten().filter_map(Value::as_str) {
                        if !o.contains_key(k) {
                            at(errs, format!("'{k}' is a required property"));
                        }
                    }
                }
            }
            "additionalProperties" => {
                if let (Some(o), Some(false)) = (v.as_object(), want.as_bool()) {
                    let props = s.get("properties").and_then(Value::as_object);
                    let extra: Vec<String> = o.keys().filter(|k| !props.is_some_and(|p| p.contains_key(*k))).map(|k| format!("'{k}'")).collect();
                    if !extra.is_empty() {
                        at(errs, format!("Additional properties are not allowed ({} {} unexpected)", extra.join(", "), if extra.len() == 1 { "was" } else { "were" }));
                    }
                }
            }
            "properties" => {
                if let Some(o) = v.as_object() {
                    for (k, sub) in want.as_object().into_iter().flatten() {
                        if let Some(x) = o.get(k) {
                            check(sub, x, &child(k), rx, errs);
                        }
                    }
                }
            }
            "items" => {
                for (i, x) in v.as_array().into_iter().flatten().enumerate() {
                    check(want, x, &child(&i.to_string()), rx, errs);
                }
            }
            "enum" => {
                if !want.as_array().is_some_and(|a| a.contains(v)) {
                    let names: Vec<String> = want.as_array().into_iter().flatten().map(repr).collect();
                    at(errs, format!("{} is not one of [{}]", repr(v), names.join(", ")));
                }
            }
            "pattern" => {
                if let (Some(t), Some(p)) = (v.as_str(), want.as_str()) {
                    match rx.entry(p.to_string()).or_insert_with(|| Regex::new(p).unwrap_or_else(|e| panic!("schema pattern {p}: {e}"))).is_match(t) {
                        true => {}
                        false => at(errs, format!("'{t}' does not match '{p}'")),
                    }
                }
            }
            "minLength" => {
                if let (Some(t), Some(n)) = (v.as_str(), want.as_u64()) {
                    if (t.chars().count() as u64) < n {
                        at(errs, format!("'{t}' is too short"));
                    }
                }
            }
            "minItems" => {
                if let (Some(a), Some(n)) = (v.as_array(), want.as_u64()) {
                    if (a.len() as u64) < n {
                        at(errs, if n == 1 { format!("{v} should be non-empty") } else { format!("{v} is too short") });
                    }
                }
            }
            other => at(errs, format!("schema keyword '{other}' is not supported by wotr-mcp validate")),
        }
    }
}

/// (exit code, report): the same run `wotr-mcp validate` prints.
pub fn validate() -> (i32, String) {
    let rules = match load() {
        Ok(r) => r,
        Err(e) => return (1, e),
    };
    if rules.is_empty() {
        return (1, "no rules found in rules/ \u{2014} nothing to validate".into());
    }
    let schema: Value = match serde_json::from_str(&read_lossy(&root("schema/rule.schema.json"))) {
        Ok(s) => s,
        Err(e) => return (1, format!("schema/rule.schema.json: {e}")),
    };
    let tags = vocab();
    let mut failures: Vec<String> = Vec::new();
    let mut by_id: HashMap<&str, Vec<&Row>> = HashMap::new();
    let mut id_order: Vec<&str> = Vec::new();
    let mut sources: HashMap<String, String> = HashMap::new();
    let mut rx = HashMap::new();
    let fail = |r: &Row, m: String| format!("{} :: {} :: {m}", r.file, r.v.get("id").and_then(Value::as_str).unwrap_or("<no id>"));
    // a live row with no source file quotes a ruling; that ruling has to be on record somewhere
    let on_record = normalise(&std::iter::once(root("RULINGS.md")).chain(rglob_md(&root("wiki"))).map(|p| read_lossy(&p)).collect::<Vec<_>>().join("\n"));

    for r in &rules {
        let mut errs = Vec::new();
        check(&schema, &Value::Object(r.v.clone()), "", &mut rx, &mut errs);
        failures.extend(errs.into_iter().map(|e| fail(r, e)));
        let id = text(&r.v, "id");
        if !id.is_empty() {
            if !by_id.contains_key(id) {
                id_order.push(id);
            }
            by_id.entry(id).or_default().push(r);
        }
        for tag in list(&r.v, "applies_to") {
            if !tags.contains(tag) {
                failures.push(fail(r, format!("applies_to tag '{tag}' is not in schema/applies_to.md")));
            }
        }
        // verbatim must actually exist in the source file
        let src = r.v.get("source").and_then(|s| s.get("file")).and_then(Value::as_str).unwrap_or("");
        let quote = text(&r.v, "verbatim");
        if !src.is_empty() && !quote.is_empty() {
            let path = root("sources").join(src);
            if !path.exists() {
                failures.push(fail(r, format!("source file missing: sources/{src}")));
            } else {
                let body = sources.entry(src.to_string()).or_insert_with(|| normalise(&read_lossy(&path)));
                if !body.contains(&normalise(quote)) {
                    failures.push(fail(r, "verbatim quote not found in source (paraphrase or drift)".into()));
                }
            }
        } else if !quote.is_empty() && text(&r.v, "status") == "live" && !on_record.contains(&normalise(quote)) {
            failures.push(fail(r, "no source file, and the quote is in neither RULINGS.md nor the wiki".into()));
        }
    }
    for id in &id_order {
        let hits = &by_id[id];
        if hits.len() > 1 {
            let files: Vec<&str> = hits.iter().map(|h| h.file.as_str()).collect();
            failures.push(format!("duplicate id {id} in {}", files.join(", ")));
        }
    }
    // supersedes targets must exist, and a superseded rule must not claim to be live
    for r in &rules {
        for target in list(&r.v, "supersedes") {
            let Some(victims) = by_id.get(target) else {
                failures.push(fail(r, format!("supersedes unknown rule id '{target}'")));
                continue;
            };
            if text(&r.v, "status") == "live" {
                for victim in victims {
                    if text(&victim.v, "status") == "live" {
                        failures.push(format!("contradiction: {target} is live but superseded by live {}", text(&r.v, "id")));
                    }
                }
            }
        }
    }
    // an open ruling is never live: once answered it is superseded, the ruling quoted in `ratified`
    let code_rx = Regex::new(r"^R\d{1,2}-[A-Z]$").unwrap();
    for r in &rules {
        if text(&r.v, "kind") == "open_ruling" {
            let status = text(&r.v, "status");
            if !code_rx.is_match(text(&r.v, "id")) {
                failures.push(fail(r, "open_ruling id must look like R15-A".into()));
            }
            if !matches!(status, "pending" | "proposed" | "superseded") {
                failures.push(fail(r, "open_ruling must be pending, proposed or superseded (ruled), not live".into()));
            }
            if status == "superseded" && !r.v.get("ratified").is_some_and(|x| x.as_str().is_some_and(|s| !s.is_empty())) {
                failures.push(fail(r, "a ruled open_ruling must carry the ruling in `ratified`".into()));
            }
        }
    }
    let mut counts: BTreeMap<&str, usize> = BTreeMap::new();
    for r in &rules {
        *counts.entry(r.v.get("status").and_then(Value::as_str).unwrap_or("None")).or_default() += 1;
    }
    let files: BTreeSet<&str> = rules.iter().map(|r| r.file.as_str()).collect();
    let shown: Vec<String> = counts.iter().map(|(k, v)| format!("{k}={v}")).collect();
    let mut out = format!("{} rules across {} files\n  {}\n", rules.len(), files.len(), shown.join("  "));
    if !failures.is_empty() {
        out += &format!("\nFAIL ({})\n", failures.len());
        for f in &failures {
            out += &format!("  {f}\n");
        }
        return (1, out.trim_end().to_string());
    }
    out += "\nPASS";
    (0, out)
}

/// `wotr-mcp resolve`: out/rules.resolved.json, rules.live.md, rules.live.full.md and docket.md.
pub fn resolve() -> Result<String, String> {
    let mut rules: Vec<Map<String, Value>> = load()?.into_iter().map(|r| r.v).collect();
    let mut superseded_by: HashMap<String, Vec<Value>> = HashMap::new();
    let mut targets: BTreeSet<String> = BTreeSet::new();
    for r in &rules {
        for t in list(r, "supersedes") {
            superseded_by.entry(t.to_string()).or_default().push(r.get("id").cloned().unwrap_or(Value::Null));
            targets.insert(t.to_string());
        }
    }
    for r in &mut rules {
        let by = superseded_by.get(text(r, "id")).cloned().unwrap_or_default();
        r.insert("superseded_by".into(), Value::Array(by));
    }
    let known: BTreeSet<&str> = rules.iter().map(|r| text(r, "id")).collect();
    let orphans: Vec<&str> = targets.iter().map(String::as_str).filter(|t| !known.contains(t)).collect();
    let out = root("out");
    std::fs::create_dir_all(&out).map_err(|e| e.to_string())?;
    let write = |name: &str, body: String| std::fs::write(out.join(name), body).map_err(|e| format!("out/{name}: {e}"));

    let mut sorted: Vec<&Map<String, Value>> = rules.iter().collect();
    sorted.sort_by(|a, b| (pack(a), text(a, "id")).cmp(&(pack(b), text(b, "id"))));
    let as_values = Value::Array(sorted.iter().map(|r| Value::Object((*r).clone())).collect());
    write("rules.resolved.json", dumps_unicode(&as_values, Some(2)))?;

    // live rules grouped by applies_to, which is how a scene loads them
    let live: Vec<&Map<String, Value>> = rules.iter().filter(|r| text(r, "status") == "live").collect();
    let mut grouped: HashMap<&str, Vec<&Map<String, Value>>> = HashMap::new();
    for r in &live {
        for tag in list(r, "applies_to") {
            grouped.entry(tag).or_default().push(r);
        }
    }
    let tags = vocab();
    let hits = |tag: &str| {
        let mut h = grouped.get(tag).cloned().unwrap_or_default();
        h.sort_by_key(|r| -pack(r));
        h
    };
    let mut brief: Vec<String> = vec!["# Live rules by domain".into(), String::new(), format!("{} live of {} extracted.", live.len(), rules.len()), String::new()];
    // the same grouping with the source quote, for a session that has the file and no MCP
    let mut full: Vec<String> = vec![
        "# Live rules by domain, with source text".into(),
        String::new(),
        format!("{} live of {} extracted. Newest pack first within each domain; the newer rule governs where two overlap.", live.len(), rules.len()),
        String::new(),
    ];
    for tag in &tags {
        let h = hits(tag);
        if h.is_empty() {
            continue;
        }
        let head = format!("## {tag} ({})", h.len());
        brief.extend([head.clone(), String::new()]);
        full.extend([head, String::new()]);
        for r in h {
            let (id, p, sec) = (text(r, "id"), text(r, "pack"), text(r, "section"));
            brief.push(format!("- **{id}** [{p} {sec}] {}", text(r, "summary").trim()));
            full.extend([
                format!("### {id} [{p} {sec}]"),
                String::new(),
                text(r, "summary").trim().to_string(),
                String::new(),
                format!("> {}", text(r, "verbatim").trim()),
                String::new(),
            ]);
        }
        brief.push(String::new());
    }
    write("rules.live.md", brief.join("\n"))?;
    write("rules.live.full.md", full.join("\n"))?;

    let mut pending: Vec<&Map<String, Value>> = rules.iter().filter(|r| matches!(text(r, "status"), "pending" | "proposed")).collect();
    pending.sort_by(|a, b| (pack(a), text(a, "id")).cmp(&(pack(b), text(b, "id"))));
    let mut dock: Vec<String> = vec!["# The Docket \u{2014} open rulings".into(), String::new(), format!("{} outstanding.", pending.len()), String::new()];
    for r in &pending {
        let blocks: Vec<&str> = list(r, "applies_to").collect();
        dock.extend([
            format!("## {} \u{2014} {}", text(r, "id"), text(r, "title")),
            String::new(),
            format!("*{} {}, blocks: {}*", text(r, "pack"), text(r, "section"), blocks.join(", ")),
            String::new(),
            format!("> {}", text(r, "verbatim").trim()),
            String::new(),
        ]);
        if !text(r, "notes").is_empty() {
            dock.extend([text(r, "notes").trim().to_string(), String::new()]);
        }
    }
    write("docket.md", dock.join("\n"))?;

    let mut report = format!("resolved {} rules -> out/\n  live={} pending={}", rules.len(), live.len(), pending.len());
    if !orphans.is_empty() {
        report += &format!("\n  WARN unknown supersession targets: {}", orphans.join(", "));
    }
    Ok(report)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn errs(s: Value, v: Value) -> Vec<String> {
        let mut e = Vec::new();
        check(&s, &v, "", &mut HashMap::new(), &mut e);
        e
    }

    #[test]
    fn schema_keywords() {
        let s = json!({"type": "object", "required": ["id"], "additionalProperties": false,
            "properties": {"id": {"type": "string", "pattern": "^R\\d$", "minLength": 2}, "n": {"type": ["integer", "null"]},
                           "e": {"enum": ["a", null]}, "l": {"type": "array", "minItems": 1, "items": {"type": "string"}}}});
        assert!(errs(s.clone(), json!({"id": "R1", "n": null, "e": "a", "l": ["x"]})).is_empty());
        let all = errs(s, json!({"n": "x", "e": "b", "l": [], "z": 1})).join("\n");
        for want in ["'id' is a required property", "('z' was unexpected)", "schema: n: 'x' is not of type 'integer', 'null'", "'b' is not one of", "schema: l: [] should be non-empty"] {
            assert!(all.contains(want), "{want} in {all}");
        }
        let bad = errs(json!({"properties": {"id": {"pattern": "^R\\d$", "minLength": 3}}}), json!({"id": "x"})).join("\n");
        assert!(bad.contains("'x' does not match") && bad.contains("'x' is too short"), "{bad}");
    }

    #[test]
    fn unknown_schema_keyword_is_reported() {
        assert!(errs(json!({"maximum": 1}), json!(2))[0].contains("not supported"));
    }

    #[test]
    fn normalise_drops_marks_and_folds_space() {
        assert_eq!(normalise("  a *b*\n\u{2019}c_ \u{201c}d`\u{201d} "), "a b 'c \"d\"");
    }
}
