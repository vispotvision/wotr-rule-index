//! The table's own data as the bot shows it: the in-world calendar, Ledger lines, an NPC's public face
//! and events. R72-40: /ledger and /due show a player only the lines about characters they own, and
//! /roster and /npc show an NPC's public face only. Want, lie, tell, knows and lied_about never leave
//! table/npcs.yaml through here.
use crate::pyyaml;
use crate::re;
use crate::table;
use crate::text::{has, rx, split, sub};
use crate::util::{read_lossy, root};
use serde_json::{json, Map, Value};

pub const ARCHONS: [(&str, &str); 14] = [("Urion", "Balance"), ("Uurgath", "Disruption"), ("Thalen", "Form"), ("Valen", "Time"), ("Maelor", "Memory"), ("Zhaeren", "Space"), ("Irath", "Dominion"), ("Veyra", "Desire"), ("Iesara", "Insight"), ("Kaetra", "Dream"), ("Wyther", "Motion"), ("Auren", "Death"), ("Selhar", "Harmony"), ("Elyndra", "Life")];
const DAYS_IN_MONTH: i64 = 28;
const YEAR: i64 = 364; // Munahi sits after it, eight years in thirteen

/// Month 1-13, day 1-28 (month 14 = Munahi).
pub fn describe(month: i64, day: i64, year: Option<i64>, era: &str) -> String {
    if month == 14 {
        return "**Munahi**, the nameless day \u{2014} no Archon, no Labour, no Work falls due, nothing can be entered, no window opens, no instrument binds.".into();
    }
    let (a, principle) = ARCHONS[((day - 1).rem_euclid(14)) as usize];
    let y = year.filter(|y| *y != 0).map_or(String::new(), |y| format!(" \u{b7} Accord year {y}"));
    let e = if era.is_empty() { String::new() } else { format!(" \u{b7} {era}") };
    format!("**{a}'s day** ({principle}) \u{b7} month {month}, {} turn, day {day}{y}{e}", if day <= 14 { "first" } else { "second" })
}

/// Advance through the calendar; Munahi is not modelled as a step (it is nobody's day).
pub fn add_days(month: i64, day: i64, year: i64, n: i64) -> (i64, i64, i64) {
    let doy = (month - 1) * DAYS_IN_MONTH + day - 1 + n;
    let (year, doy) = (year + doy.div_euclid(YEAR), doy.rem_euclid(YEAR));
    (doy / DAYS_IN_MONTH + 1, doy % DAYS_IN_MONTH + 1, year)
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
    fn the_calendar_turns() {
        assert!(describe(3, 1, Some(715), "Era").starts_with("**Urion's day** (Balance) \u{b7} month 3, first turn, day 1 \u{b7} Accord year 715 \u{b7} Era"));
        assert!(describe(3, 15, None, "").starts_with("**Urion's day** (Balance) \u{b7} month 3, second turn"));
        assert!(describe(14, 1, None, "").starts_with("**Munahi**"));
        assert_eq!(add_days(1, 1, 700, 27), (1, 28, 700));
        assert_eq!(add_days(1, 1, 700, 28), (2, 1, 700));
        assert_eq!(add_days(13, 28, 700, 1), (1, 1, 701));
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
