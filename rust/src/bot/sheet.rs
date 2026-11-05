//! The sheet checker: a character sheet checked against the canon it must obey. Every check cites its
//! rule. Nothing here judges prose quality. Stats: the canon model (R39-1), Dominion over seven (R39-2),
//! the Stage's Max Grade top (R39-4), the pool for the Level and Stage (R39-3). Names: struck names
//! and registers (R22, R21-1, R23-1). Terms: Stage names and Grade letters (R14-5).
use super::fmt::{commas, commas0};
use super::fow::{canon, grade_of, max_grade_of, stage_gate, ROMAN};
use crate::re;
use crate::search::reversion_map;
use crate::text::{caps, group, has, rx};
use std::collections::{BTreeSet, HashMap};

const GRADES: [&str; 13] = ["Hollow", "F", "E", "D", "C", "B", "A", "S", "SS", "SSS", "X", "EX", "EX+"];

pub struct Report {
    pub ok: bool,
    pub findings: Vec<(&'static str, String)>,
    pub summary: String,
}

type Subs = Vec<((String, String), i64)>;

fn parse(text: &str) -> (Option<i64>, Option<i64>, Subs, HashMap<String, i64>) {
    let cx = canon();
    let level = caps(re!(r"\bLevel\b[^\d\n]{0,20}(\d{1,3})"), text).and_then(|m| group(&m, 1).parse().ok());
    let stage = caps(re!(r"\bStage\b[^\S\n]*(?:\*\*)?\s*([IVX]{1,4}|\d{1,2})\b"), text).and_then(|m| {
        let s = group(&m, 1);
        ROMAN.iter().position(|r| *r == s).map(|i| i as i64 + 1).or_else(|| s.parse().ok())
    });
    let mut owners: HashMap<&str, Vec<&str>> = HashMap::new();
    for (p, ss) in &cx.subs {
        for s in ss {
            owners.entry(s).or_default().push(p);
        }
    }
    let primaries: Vec<(&str, fancy_regex::Regex)> = cx.subs.iter().map(|(p, _)| (p.as_str(), rx(&format!(r"(?<![A-Za-z]){p}(?![a-z])")))).collect();
    let (mut subs, mut stated): (Subs, HashMap<String, i64>) = (Vec::new(), HashMap::new());
    let mut current: Option<&str> = None; // the Primary whose section we are in (Stability belongs to two)
    for line in text.lines() {
        if let Some((p, _)) = primaries.iter().find(|(_, r)| has(r, line)) {
            current = Some(p);
        }
        // "**Fortitude** 310", "Fortitude: 310", "| Fortitude | 310 |", "Fortitude 310 \u{b7}"
        for c in re!(r"\b([A-Z][a-z]+)\b[^\w\n]{1,6}(\d{1,4})(?!\s*[/%])").captures_iter(line).filter_map(Result::ok) {
            let (name, val) = (group(&c, 1), group(&c, 2).parse().unwrap_or(0));
            if let Some(own) = owners.get(name) {
                let p = current.filter(|x| own.contains(x)).unwrap_or(own[0]).to_string();
                if !subs.iter().any(|(k, _)| k.0 == p && k.1 == name) {
                    subs.push(((p, name.to_string()), val));
                }
            } else if primaries.iter().any(|(p, _)| *p == name) {
                stated.entry(name.to_string()).or_insert(val);
            }
        }
    }
    (level, stage, subs, stated)
}

pub fn check(text: &str) -> Report {
    let cx = canon();
    let (level, stage, subs, stated) = parse(text);
    let mut f: Vec<(&'static str, String)> = Vec::new();
    if level.is_none() {
        f.push(("fail", "No **Level** found on the sheet.".into()));
    }
    if stage.is_none() {
        f.push(("fail", "No **Stage** found (a Temperance Stage, I\u{2013}XIV).".into()));
    }
    if let (Some(level), Some(stage)) = (level, stage.filter(|s| (1..=14).contains(s))) {
        let gate = stage_gate(level);
        if (stage as usize) < gate {
            f.push(("fail", format!("Level {level} cannot be surpassed below Stage {} (the Band gate); Stage {} is a forced progression.", ROMAN[gate - 1], ROMAN[stage as usize - 1])));
        }
        let st = &cx.stages[stage as usize - 1];
        let max_grade = max_grade_of(st);
        let grade_top = cx.grades.iter().find(|g| g.grade == max_grade).map_or(st.ceiling, |g| g.hi);
        let lvl_pts: i64 = cx.bands.iter().map(|b| (level.min(b.hi) - b.lo + 1).max(0) * b.pts).sum();
        let thr_pts: i64 = (1..=stage).map(|s| s * 100).sum();
        let pool = lvl_pts + thr_pts;
        if subs.is_empty() {
            f.push(("fail", "No Sub-Stat values found. The canon model (R39-1) spends points on Sub-Stats; a Primary is their total.".into()));
        } else {
            let get = |p: &str, s: &str| subs.iter().find(|(k, _)| k.0 == p && k.1 == s).map(|x| x.1);
            let spent: i64 = subs.iter().filter(|(k, _)| k.1 != "Throne").map(|x| x.1).sum();
            let missing: Vec<String> = cx.subs.iter().flat_map(|(p, ss)| ss.iter().filter(|s| *s != "Throne" && get(p, s).is_none()).map(move |s| format!("{p}/{s}"))).collect();
            f.push((if spent <= pool { "ok" } else { "fail" }, format!("Points on Sub-Stats: **{}** of a pool of **{}** ({} levelling + {} Thresholds, Stage I counting \u{2014} R39-3).", commas(spent), commas(pool), commas(lvl_pts), commas(thr_pts))));
            let over: Vec<String> = subs.iter().filter(|(k, v)| k.1 != "Throne" && *v > grade_top).take(8).map(|(k, v)| format!("{} {v}", k.1)).collect();
            if !over.is_empty() {
                f.push(("fail", format!("Above the Stage's Max Grade top of {} (R39-4): {}", commas(grade_top), over.join(", "))));
            }
            if !missing.is_empty() {
                let shown: Vec<&str> = missing.iter().take(10).map(String::as_str).collect();
                f.push(("warn", format!("{} Sub-Stat(s) not listed (the sheet should carry all sixty-three; Throne aside): {}{}", missing.len(), shown.join(", "), if missing.len() > 10 { "\u{2026}" } else { "" })));
            }
            for (p, ss) in &cx.subs {
                let vals: Vec<i64> = ss.iter().filter(|s| *s != "Throne").filter_map(|s| get(p, s)).collect();
                if vals.is_empty() {
                    continue;
                }
                let total: i64 = vals.iter().sum();
                let n = if p == "Dominion" { 7.0 } else { 8.0 };
                let mean = total as f64 / n;
                match stated.get(p).filter(|s| (**s - total).abs() > 1) {
                    Some(s) => f.push(("fail", format!("**{p}** is stated as {} but its Sub-Stats total {}; the Primary is the sum (R39-1).", commas(*s), commas(total)))),
                    None => f.push(("ok", format!("**{p}** {} \u{b7} mean {} \u{b7} {}-Grade{}", commas(total), commas0(mean), grade_of(mean), if p == "Dominion" { " (\u{f7}7, Throne excluded \u{2014} R39-2)" } else { "" }))),
                }
            }
        }
    }
    // names
    let hits: Vec<String> = reversion_map().into_iter().filter(|(old, _)| old.chars().count() >= 4 && has(&rx(&format!(r"(?<!\w){}(?!\w)", fancy_regex::escape(old))), text)).map(|(o, n)| format!("**{o}** \u{2192} {n}")).collect();
    if !hits.is_empty() {
        let shown: Vec<&str> = hits.iter().take(8).map(String::as_str).collect();
        f.push(("fail", format!("Struck names or terms (the Moto Reversion Ledger; R22, R21-1, R23-1): {}", shown.join("; "))));
    }
    // terms
    let names: BTreeSet<&str> = cx.stages.iter().map(|s| s.name.as_str()).collect();
    for c in re!(r"\bStage\s+[IVX\d]+\s*[\x{2014}\x{2013}-]\s*([A-Z][a-z]+)").captures_iter(text).filter_map(Result::ok) {
        let name = group(&c, 1);
        if !names.contains(name) {
            f.push(("fail", format!("Stage name **{name}** is not the Living System's (R14-5); the sixteen are {}.", names.iter().copied().collect::<Vec<_>>().join(", "))));
        }
    }
    for c in re!(r"\b([A-Z]{1,3}\+?)-Grade\b").captures_iter(text).filter_map(Result::ok) {
        let g = group(&c, 1);
        if !GRADES.contains(&g) {
            f.push(("fail", format!("Grade **{g}** is not on the Grade table (R14-5).")));
        }
    }
    let (fails, warns) = (f.iter().filter(|x| x.0 == "fail").count(), f.iter().filter(|x| x.0 == "warn").count());
    let summary = format!("{}{}", if fails == 0 { "passes".to_string() } else { format!("{fails} problem(s)") }, if warns > 0 { format!(", {warns} warning(s)") } else { String::new() });
    Report { ok: fails == 0, findings: f, summary }
}
