//! /stats: a Fracture of Worlds stat block built the canon way, from the wiki pages of "Fracture of
//! Worlds \u{2014} The Living System": points and caps by Band, Stage x 100 Threshold bonuses, the
//! ceiling binding each Sub-Stat, Grade read off the mean. Points are spent on Sub-Stats only; a
//! Primary is the total of its eight and its Grade is the mean. Throne carries no ceiling and is
//! excluded from the Dominion total. The only randomness is which Sub-Stats a build favours.
use crate::rng::Random;
use crate::text::{caps, group, has};
use crate::util::{read_lossy, root};
use crate::re;
use serde_json::{json, Value};
use std::collections::{BTreeMap, HashMap, HashSet};
use std::path::PathBuf;
use std::sync::OnceLock;

pub const ROMAN: [&str; 16] = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI"];

#[derive(Clone, Default)]
pub struct Band {
    pub name: String,
    pub lo: i64,
    pub hi: i64,
    pub pts: i64,
    pub cap: i64,
}

#[derive(Clone)]
pub struct Grade {
    pub grade: String,
    pub lo: i64,
    pub hi: i64,
}

#[derive(Clone)]
pub struct Stage {
    pub n: usize,
    pub roman: String,
    pub name: String,
    pub max_grade: String,
    pub ceiling: i64,
    pub standing: String,
}

pub struct Canon {
    pub bands: Vec<Band>,
    pub grades: Vec<Grade>,
    pub stages: Vec<Stage>,
    pub subs: Vec<(String, Vec<String>)>,
}

fn page(name: &str) -> PathBuf {
    root("wiki/The Magic System/Fracture of Worlds \u{2014} The Living System").join(name)
}

fn read(p: PathBuf) -> String {
    let t = read_lossy(&p);
    if let Some(rest) = t.strip_prefix("---\n") {
        if let Some(end) = rest.find("\n---\n") {
            return rest[end + 5..].to_string();
        }
    }
    t
}

fn cells(line: &str) -> Vec<&str> {
    line.trim().trim_matches('|').split('|').map(str::trim).collect()
}

fn first_int(s: &str) -> i64 {
    caps(re!(r"[\d,]+"), s).map_or(0, |m| group(&m, 0).replace(',', "").parse().unwrap_or(0))
}

fn digits(s: &str) -> bool {
    !s.is_empty() && s.chars().all(|c| c.is_ascii_digit())
}

pub fn canon() -> &'static Canon {
    static C: OnceLock<Canon> = OnceLock::new();
    C.get_or_init(|| {
        let mut bands: BTreeMap<&str, Band> = BTreeMap::new();
        let body = read(page("I. Levels, Experience and Stat Points (Parts One\u{2013}Three).md"));
        for line in body.split('\n').filter(|l| l.starts_with('|')) {
            let c = cells(line);
            if c.len() >= 3 {
                if let Some(rom) = ROMAN.iter().find(|r| **r == c[0]) {
                    if let Some(m) = caps(re!(r"^(\d+)[\x{2013}-](\d+)$"), c[1]) {
                        let b = bands.entry(rom).or_default();
                        (b.lo, b.hi) = (group(&m, 1).parse().unwrap_or(0), group(&m, 2).parse().unwrap_or(0));
                    } else if digits(c[1]) && digits(c[2]) {
                        let b = bands.entry(rom).or_default();
                        (b.pts, b.cap) = (c[1].parse().unwrap_or(0), c[2].parse().unwrap_or(0));
                    }
                }
            }
        }
        let (mut grades, mut stages): (Vec<Grade>, Vec<Stage>) = (Vec::new(), Vec::new());
        let body = read(page("II. Grades, Gates and Thresholds (Parts Four\u{2013}Ten).md"));
        for line in body.split('\n').filter(|l| l.starts_with('|')) {
            let c = cells(line);
            if c.len() >= 2 && has(re!(r"^(Hollow|[A-Z]+\+?)$"), c[0]) && c[1] != "Sub-Stat value" {
                if let Some(m) = caps(re!(r"^([\d,]+)(?:[\x{2013}-]([\d,]+)|\+)"), c[1]) {
                    if !grades.iter().any(|g| g.grade == c[0]) {
                        let hi = m.get(2).map_or(1_000_000_000, |x| first_int(x.as_str()));
                        grades.push(Grade { grade: c[0].to_string(), lo: first_int(group(&m, 1)), hi });
                    }
                }
            }
            if c.len() >= 4 && has(re!(r"^[A-Z][a-z]+$"), c[1]) && has(re!(r"^([A-Z]+\+?|uncapped)"), c[2]) && has(re!(r"\d"), c[3]) && !stages.iter().any(|s| s.roman == c[0]) {
                if let Some(i) = ROMAN.iter().position(|r| *r == c[0]) {
                    stages.push(Stage { n: i + 1, roman: c[0].to_string(), name: c[1].to_string(), max_grade: c[2].to_string(), ceiling: first_int(c[3]), standing: c.get(4).map_or("", |s| s).to_string() });
                }
            }
        }
        let mut subs: Vec<(String, Vec<String>)> = Vec::new();
        let mut prim: Option<usize> = None;
        let body = read(page("IV. The Eight Primaries and the Sixty-Four Sub-Stats (Part Twelve).md"));
        for line in body.split('\n') {
            if let Some(m) = caps(re!(r"^##+\s+[IVX]+\.\s+(\w+)"), line) {
                subs.push((group(&m, 1).to_string(), Vec::new()));
                prim = Some(subs.len() - 1);
                continue;
            }
            if line.starts_with("### ") {
                prim = None;
            }
            if let (Some(p), Some(m)) = (prim, caps(re!(r"^\*\*([A-Z][\w-]+)\*\*\s+[\x{2014}\x{2013}-]"), line)) {
                if subs[p].1.len() < 8 {
                    subs[p].1.push(group(&m, 1).to_string());
                }
            }
        }
        let ordered = ROMAN.iter().filter_map(|r| bands.get(r).map(|b| Band { name: r.to_string(), ..b.clone() })).collect();
        Canon { bands: ordered, grades, stages: stages.into_iter().filter(|s| s.n <= 14).collect(), subs }
    })
}

pub fn band_for(level: i64) -> Option<&'static Band> {
    canon().bands.iter().find(|b| b.lo <= level && level <= b.hi)
}

/// The Stage a Level usually sits at: the Band's cluster at the same proportion.
fn natural_stage(level: i64) -> Result<usize, String> {
    const CLUSTERS: [(usize, usize); 5] = [(1, 4), (5, 7), (8, 10), (11, 12), (13, 14)];
    let b = band_for(level).ok_or("no Band holds that Level")?;
    let i = ROMAN.iter().position(|r| *r == b.name).unwrap_or(0);
    let (lo, hi) = *CLUSTERS.get(i).ok_or("no Stage cluster for that Band")?;
    let frac = (level - b.lo) as f64 / (b.hi - b.lo).max(1) as f64;
    Ok(hi.min(lo + (frac * (hi - lo + 1) as f64) as usize))
}

/// Stage IV before Level 100 is surpassed, VII before 200, X before 300, XII before 400.
pub fn stage_gate(level: i64) -> usize {
    let bands = &canon().bands;
    let mut gate = 1;
    for (b, g) in bands[..bands.len().saturating_sub(1)].iter().zip([4, 7, 10, 12]) {
        if level > b.hi {
            gate = g;
        }
    }
    gate
}

pub fn grade_of(value: f64) -> String {
    canon().grades.iter().find(|g| g.lo as f64 <= value && value <= g.hi as f64).map_or("Hollow".to_string(), |g| g.grade.clone())
}

pub fn max_grade_of(st: &Stage) -> String {
    caps(re!(r"^[A-Z]+\+?"), &st.max_grade).map_or(String::new(), |m| group(&m, 0).to_string())
}

pub fn primaries() -> Vec<String> {
    canon().subs.iter().map(|(p, _)| p.clone()).collect()
}

/// A stat block for a Level, as JSON: the shape the embed reads.
pub fn build(level: i64, lean: Option<&str>, seed: u64) -> Result<Value, String> {
    let cx = canon();
    let last = cx.bands.last().ok_or("no Bands read from the wiki")?;
    let level = level.min(last.hi).max(1);
    let stage = natural_stage(level)?;
    let st = cx.stages.get(stage - 1).ok_or("no such Stage")?;
    let mut r = Random::from_be_bytes(&seed.to_be_bytes());
    let mut flags: Vec<String> = Vec::new();
    let gate = stage_gate(level);
    if stage < gate {
        flags.push(format!("Level {level} cannot be surpassed below Stage {}; at Stage {} this is a forced progression and the Crystal fractures until the Threshold is passed.", ROMAN[gate - 1], st.roman));
    }
    // Part Three: the pool and the per-Sub-Stat concentration cap.
    let (mut lvl_pts, mut cap_pts) = (0, 0);
    for b in &cx.bands {
        let n = (level.min(b.hi) - b.lo + 1).max(0);
        lvl_pts += n * b.pts;
        cap_pts += n * b.cap;
    }
    let thr_pts: i64 = (1..=stage as i64).map(|s| s * 100).sum();
    let pool = lvl_pts + thr_pts;
    // R39-4 (C-011): the Stage's Max Grade letter binds allocation; the band up to the numeric
    // ceiling is the instability zone, reachable only under strain, never by spending points.
    let max_grade = max_grade_of(st);
    let grade_top = cx.grades.iter().find(|g| g.grade == max_grade).map_or(st.ceiling, |g| g.hi);
    let sub_max = grade_top.min(st.ceiling).min(cap_pts + thr_pts); // Threshold points are free of the concentration cap
    let prim = primaries();
    if prim.is_empty() {
        return Err("no Primaries read from the wiki".into());
    }
    let lean = match lean.filter(|l| prim.iter().any(|p| p == l)) {
        Some(l) => l.to_string(),
        None => r.choice(&prim),
    };
    let spendable: Vec<(String, String)> = cx.subs.iter().flat_map(|(p, ss)| ss.iter().filter(|s| *s != "Throne").map(move |s| (p.clone(), s.clone()))).collect();
    let n_fav = r.randint(8, 16) as usize;
    let lean_subs: Vec<(String, String)> = spendable.iter().filter(|ps| ps.0 == lean).cloned().collect();
    let mut fav: HashSet<(String, String)> = r.sample(&lean_subs, 4).into_iter().collect();
    fav.extend(r.sample(&spendable, n_fav));
    let mut w: Vec<f64> = Vec::with_capacity(spendable.len());
    for ps in &spendable {
        let mut base = r.gammavariate(4.0, 1.0);
        if fav.contains(ps) {
            base *= r.uniform(3.0, 6.0);
        }
        if ps.0 == lean {
            base *= 1.5;
        }
        w.push(base);
    }
    let tot: f64 = w.iter().sum();
    let mut raw: Vec<f64> = w.iter().map(|wi| pool as f64 * wi / tot).collect();
    let limit = sub_max as f64;
    for _ in 0..12 {
        // the ceiling binds the Sub-Stat; refused points are re-offered to entries with room
        let mut spill = 0.0;
        for x in raw.iter_mut() {
            if *x > limit {
                spill += *x - limit;
                *x = limit;
            }
        }
        let room: Vec<usize> = (0..raw.len()).filter(|i| raw[*i] < limit - 1e-9).collect();
        if spill < 0.5 || room.is_empty() {
            break;
        }
        let wsum: f64 = room.iter().map(|i| w[*i]).sum();
        for i in room {
            raw[i] += spill * w[i] / wsum;
        }
    }
    let mut vals: Vec<i64> = raw.iter().map(|x| *x as i64).collect();
    let mut left = pool - vals.iter().sum::<i64>(); // the rounding remainder, one point at a time where there is room
    let mut by_raw: Vec<usize> = (0..raw.len()).collect();
    by_raw.sort_by(|a, b| raw[*b].partial_cmp(&raw[*a]).unwrap());
    for i in by_raw {
        if left <= 0 {
            break;
        }
        if vals[i] < sub_max {
            vals[i] += 1;
            left -= 1;
        }
    }
    let spent: i64 = vals.iter().sum();
    let found: HashMap<(&str, &str), i64> = spendable.iter().zip(&vals).map(|(ps, v)| ((ps.0.as_str(), ps.1.as_str()), *v)).collect();
    let order: HashMap<&str, usize> = cx.grades.iter().enumerate().map(|(i, g)| (g.grade.as_str(), i)).collect();
    let unstable = match stage {
        5 => Some(320),
        11 => Some(700),
        _ => None,
    };
    let mut rows: Vec<Value> = Vec::new();
    for (p, ss) in &cx.subs {
        let entries: Vec<(&String, Option<i64>)> = ss.iter().map(|s| (s, found.get(&(p.as_str(), s.as_str())).copied())).collect();
        let counted: Vec<i64> = entries.iter().filter_map(|e| e.1).collect();
        let total: i64 = counted.iter().sum();
        let mean = total as f64 / counted.len().max(1) as f64;
        let g = grade_of(mean);
        let over = order.get(g.as_str()).copied().unwrap_or(0) > order.get(max_grade.as_str()).copied().unwrap_or(99);
        let shaky: Vec<&String> = entries.iter().filter(|e| matches!((e.1, unstable), (Some(v), Some(u)) if v > u)).map(|e| e.0).collect();
        rows.push(json!({"primary": p, "total": total, "mean": mean, "grade": g, "entries": entries.iter().map(|(s, v)| json!([s, v])).collect::<Vec<_>>(), "over": over, "unstable": shaky}));
    }
    rows.sort_by_key(|x| -x["total"].as_i64().unwrap_or(0));
    let band = band_for(level).ok_or("no Band holds that Level")?;
    Ok(json!({"level": level, "band": band.name, "stage": {"roman": st.roman, "name": st.name, "standing": st.standing, "max_grade": st.max_grade, "ceiling": st.ceiling},
        "pool": pool, "lvl_pts": lvl_pts, "thr_pts": thr_pts, "sub_max": sub_max, "grade_top": grade_top, "spent": spent, "unheld": pool - spent, "rows": rows, "lean": lean, "flags": flags}))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_canon_reads_from_the_wiki() {
        let c = canon();
        assert_eq!(c.bands.len(), 5);
        assert_eq!(c.stages.len(), 14);
        assert_eq!(c.subs.len(), 8);
        assert!(c.subs.iter().all(|(_, s)| s.len() == 8));
    }
}
