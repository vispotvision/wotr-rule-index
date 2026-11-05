//! The table's own data as the bot shows it: the in-world calendar, Ledger lines, an NPC's public face
//! and events. R72-40: /ledger and /due show a player only the lines about characters they own, and
//! /roster and /npc show an NPC's public face only. Want, lie, tell, knows and lied_about never leave
//! table/npcs.yaml through here.
use crate::pyyaml;
use crate::re;
use crate::table;
use crate::text::{has, rx, split, sub};
use crate::util::{read_lossy, root};
use chrono::{Datelike, NaiveDate, TimeDelta};
use serde_json::{json, Map, Value};

/// The real calendar (R85-2). Year 0 stands in when the table has no year; it is a leap year, so February 29 passes.
pub fn date(month: i64, day: i64, year: i64) -> Option<NaiveDate> {
    NaiveDate::from_ymd_opt(i32::try_from(year).ok()?, u32::try_from(month).ok()?, u32::try_from(day).ok()?)
}

/// The weekday needs a year, so a date with no year gives only month and day.
pub fn describe(month: i64, day: i64, year: Option<i64>, era: &str) -> String {
    let year = year.filter(|y| *y != 0);
    let Some(d) = date(month, day, year.unwrap_or(0)) else { return format!("month {month}, day {day}") };
    let name = d.format(if year.is_some() { "%A, %B %-d" } else { "%B %-d" });
    let lore = match (month, day) {
        (2, 29) => " \u{b7} Munahi, the nameless day: no instrument binds",
        (_, 12) => " \u{b7} Auren's day, for the dead",
        _ => "",
    };
    let y = year.map_or(String::new(), |y| format!(" \u{b7} Accord year {y}"));
    let e = if era.is_empty() { String::new() } else { format!(" \u{b7} {era}") };
    format!("**{name}**{lore}{y}{e}")
}

/// Forward through the calendar; an impossible date stays as it is, and /date set refuses those first.
pub fn add_days(month: i64, day: i64, year: i64, n: i64) -> (i64, i64, i64) {
    match date(month, day, year).and_then(|d| d.checked_add_signed(TimeDelta::days(n))) {
        Some(d) => (i64::from(d.month()), i64::from(d.day()), i64::from(d.year())),
        None => (month, day, year),
    }
}

fn calendar_path() -> std::path::PathBuf {
    root("table/calendar.yaml")
}

pub fn calendar() -> Map<String, Value> {
    pyyaml::load(&read_lossy(&calendar_path())).ok().and_then(|v| v.as_object().cloned()).unwrap_or_default()
}

pub fn save_calendar(d: &Map<String, Value>) -> Result<(), String> {
    std::fs::write(calendar_path(), pyyaml::dump(&Value::Object(d.clone()))).map_err(|e| e.to_string())
}

/// The characters a Discord user owns, from bot/config.yaml.
pub fn owned(cfg: &Value, uid: u64) -> Vec<String> {
    let players = cfg.get("players").and_then(Value::as_object);
    let Some(row) = players.and_then(|p| p.get(&uid.to_string())) else { return Vec::new() };
    row.as_array().into_iter().flatten().map(|n| n.as_str().map_or_else(|| n.to_string(), String::from)).collect()
}

/// The line's subject names one of them. The subject is `who` before ' about ': L053, Sodoku Moto
/// about Sonzai, is what Sodoku thinks in his own head, not a line for Sonzai's player.
pub fn mine(r: &Value, names: &[String]) -> bool {
    let who = table::s(r.get("who"));
    let subject = split(re!(r"\s+about\s+"), &who)[0].trim_matches([' ', '.']).to_lowercase();
    if subject.is_empty() {
        return false;
    }
    names.iter().map(|n| n.trim().to_lowercase()).any(|n| {
        !n.is_empty() && (has(&rx(&format!(r"\b{}\b", fancy_regex::escape(&n))), &subject) || has(&rx(&format!(r"\b{}\b", fancy_regex::escape(&subject))), &n))
    })
}

pub fn ledger_line(r: &Value) -> String {
    let terms = crate::writers::terms(r).unwrap_or_default().join("; ");
    let who = table::s(r.get("who"));
    let why = table::s(r.get("why"));
    format!("**{}** \u{b7} {} \u{b7} {}{}{}\n{}\n", table::s(r.get("id")), table::s(r.get("category")), if who.is_empty() { "no one named" } else { &who }, if terms.is_empty() { String::new() } else { format!("\n-# {terms}") }, if why.is_empty() { String::new() } else { format!("\n-# came due: {why}") }, table::s(r.get("text")))
}

/// Open lines, or those come due with why.
pub fn ledger_rows(come_due: bool) -> Result<Vec<Value>, String> {
    if come_due {
        return Ok(table::due_rows(2, None, None)?.into_iter().map(|(mut r, age, why)| {
            r["age"] = json!(age);
            r["why"] = json!(why);
            r
        }).collect());
    }
    Ok(table::load("ledger")?.into_iter().filter(|r| r.get("status").and_then(Value::as_str) == Some("open")).collect())
}

pub fn face(r: &Value) -> String {
    let mut bits = Vec::new();
    for k in ["look", "voice", "role"] {
        if table::t(r.get(k)) {
            let v = sub(re!(r"(?s)\s*\([^)]*\bIsaac\b[^)]*\)|\s*(?:Gloss rights:|Swap test:|LINE NOT SET|Counterplay:|Tell:).*"), &table::s(r.get(k)), |_| String::new());
            bits.push(format!("{k}: {}", v.trim()));
        }
    }
    format!("**{}**\n{}\n", table::s(r.get("name")), if bits.is_empty() { "-# no public face set yet".to_string() } else { bits.join("\n") })
}

pub fn roster(thread: &str) -> Result<Vec<Value>, String> {
    let th = thread.to_lowercase();
    Ok(table::load("npcs")?.into_iter().filter(|r| th.is_empty() || table::s(r.get("thread")).to_lowercase().contains(&th)).collect())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_calendar_is_the_real_one() {
        assert_eq!(describe(3, 1, None, ""), "**March 1**");
        assert!(describe(3, 1, Some(715), "Era").ends_with("\u{b7} Accord year 715 \u{b7} Era"));
        assert!(describe(3, 1, Some(715), "").contains("day, March 1**"));
        assert!(describe(2, 29, None, "").contains("Munahi"));
        assert!(describe(5, 12, None, "").contains("Auren's day"));
        assert_eq!(add_days(1, 31, 700, 1), (2, 1, 700));
        assert_eq!(add_days(12, 31, 700, 1), (1, 1, 701));
        assert_eq!(add_days(2, 28, 716, 1), (2, 29, 716));
        assert_eq!(add_days(2, 28, 715, 1), (3, 1, 715));
        assert!(date(2, 30, 716).is_none() && date(13, 1, 716).is_none());
        assert_eq!(table::story_days("715-3-1").unwrap() - table::story_days("715-2-28").unwrap(), 1);
        assert!(table::story_days("715-13-1").is_none());
    }

    #[test]
    fn a_ledger_line_belongs_to_its_subject_only() {
        let names = vec!["Sodoku Moto".to_string()];
        assert!(mine(&json!({"who": "Sodoku Moto about Sonzai"}), &names));
        assert!(mine(&json!({"who": "Sodoku"}), &names));
        assert!(!mine(&json!({"who": "Sonzai about Sodoku Moto"}), &names));
        assert!(!mine(&json!({"who": ""}), &names));
    }

    #[test]
    fn a_public_face_drops_the_private_notes() {
        let got = face(&json!({"name": "Ana", "look": "tall (Isaac: recast)", "voice": "low. Tell: she blinks", "want": "secret"}));
        assert_eq!(got, "**Ana**\nlook: tall\nvoice: low.\n");
        assert_eq!(face(&json!({"name": "Bo"})), "**Bo**\n-# no public face set yet\n");
    }
}
