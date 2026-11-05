//! /name: compose a name from a culture's ratified element bank (bot/namebank.yaml). Each builder
//! gives the headline, labelled lines, the rule, a note, and flags that say where the output leans
//! on filler or where the rule left something open.
use crate::pyyaml;
use crate::rng::Random;
use crate::util::{read_lossy, root};
use serde_json::{json, Value};
use std::sync::LazyLock;

pub const CULTURES: [(&str, &str); 10] = [
    ("mahuo", "Mahuo (Korean stratum)"),
    ("yukari", "Yukari (Japonic stratum)"),
    ("dawi", "Dawi (Barrel Dwarves)"),
    ("concord", "Concord Human (Northern stratum)"),
    ("holy_sea", "Holy Sea of Alabaster (Latin ordination)"),
    ("elven", "Elven \u{2014} pick a branch"),
    ("beastkin", "Beastkin \u{2014} pick a lineage"),
    ("far_northern", "Far-Northern carried name"),
    ("moto", "Moto (Japonic stratum)"),
    ("celestial", "Celestial Host"),
];

pub const NOT_OFFERED: [(&str, &str); 4] = [
    ("zettari", "The Zettari register is Swahili/Bantu/Arabic in flavour (R32-1) with attested names but no element bank. Nothing to draw from."),
    ("chinese", "The Chinese stratum has its six slots (R23-10-CHINESE_SLOTS) but no syllable bank. Nothing to draw from."),
    ("goblinoid", "R20-1-GOBLINOID_ANCHOR names the pattern, not the elements. Nothing to draw from."),
    ("undaar-keth", "R20-2-UNDAAR_KETH_NAMING refers to a hobgoblin element inventory that is not in the index. Nothing to draw from."),
];

pub static BANK: LazyLock<Value> = LazyLock::new(|| pyyaml::load(&read_lossy(&root("bot/namebank.yaml"))).expect("bot/namebank.yaml"));

fn txt(v: &Value) -> String {
    match v {
        Value::String(s) => s.clone(),
        Value::Null => String::new(),
        o => o.to_string(),
    }
}

fn st(b: &Value, k: &str) -> String {
    txt(&b[k])
}

fn strings(v: &Value) -> Vec<String> {
    v.as_array().into_iter().flatten().map(txt).collect()
}

fn items(v: &Value) -> Vec<(String, String)> {
    v.as_object().into_iter().flatten().map(|(k, x)| (k.clone(), txt(x))).collect()
}

pub fn elven_branches() -> Vec<String> {
    BANK["elven"]["branches"].as_object().map(|m| m.keys().cloned().collect()).unwrap_or_default()
}

pub fn beastkin_lineages() -> Vec<String> {
    BANK["beastkin"]["expectation"].as_object().map(|m| m.keys().filter(|k| *k != "any").cloned().collect()).unwrap_or_default()
}

type El = (String, String, String);

fn flat(groups: &Value) -> Vec<El> {
    let mut out = Vec::new();
    for (grp, els) in groups.as_object().into_iter().flatten() {
        for (el, gloss) in els.as_object().into_iter().flatten() {
            out.push((el.clone(), txt(gloss), grp.clone()));
        }
    }
    out
}

fn pick2(groups: &Value, r: &mut Random) -> (El, El) {
    let s = r.sample(&flat(groups), 2);
    (s[0].clone(), s[1].clone())
}

/// a + b.lower()
fn join(a: &str, b: &str) -> String {
    format!("{a}{}", b.to_lowercase())
}

/// str.capitalize()
fn capitalize(s: &str) -> String {
    let mut c = s.chars();
    c.next().map_or(String::new(), |f| f.to_uppercase().chain(c.as_str().to_lowercase().chars()).collect())
}

fn done(name: String, b: &Value, flags: Vec<String>, lines: Vec<(&str, String)>) -> Value {
    let lines: Vec<Value> = lines.into_iter().map(|(l, t)| json!([l, t])).collect();
    json!({"name": name, "rule": st(b, "rule"), "note": st(b, "note"), "flags": flags, "lines": lines})
}

fn mahuo(r: &mut Random) -> Value {
    let b = &BANK["mahuo"];
    let (gn, per) = pick2(&b["elements"], r);
    let given = if r.random() < 0.5 { join(&gn.0, &per.0) } else { join(&per.0, &gn.0) };
    let fam = r.choice(&strings(&b["families"]));
    let full = if r.random() < 0.5 { format!("{fam} {given}") } else { format!("{given} {fam}") };
    let others: Vec<El> = flat(&b["elements"]).into_iter().filter(|e| e.0 != gn.0 && e.0 != per.0).collect();
    let sib = r.choice(&others);
    let sibling = if r.random() < 0.5 { join(&gn.0, &sib.0) } else { join(&sib.0, &gn.0) };
    done(full, b, vec!["Which syllable is generational in the attested pairs is not fixed by canon; the inventory leaves it flexible.".into()], vec![
        ("Generation-syllable", format!("**{}** \u{2014} {} ({})", gn.0, gn.1, gn.2)),
        ("Personal syllable", format!("**{}** \u{2014} {} ({})", per.0, per.1, per.2)),
        ("Reads as", format!("\u{201c}{}\u{201d} + \u{201c}{}\u{201d}", gn.1, per.1)),
        ("A cohort sibling", format!("{sibling} (shares **{}**)", gn.0)),
    ])
}

fn yukari(r: &mut Random) -> Value {
    let b = &BANK["yukari"];
    let els = flat(&b["elements"]);
    let child = r.sample(&els, 2);
    let rest: Vec<El> = els.iter().filter(|e| !child.contains(e)).cloned().collect();
    let adult = r.sample(&rest, 2);
    let rest: Vec<El> = els.iter().filter(|e| !child.contains(e) && !adult.contains(e)).cloned().collect();
    let post = r.sample(&rest, 2);
    let (c, a, p) = (join(&child[0].0, &child[1].0), join(&adult[0].0, &adult[1].0), join(&post[0].0, &post[1].0));
    done(format!("{a} Yukari"), b, vec!["Whether a Yukari carries a second topographic surname beside \u{201c}Yukari\u{201d} is left open by the inventory.".into()], vec![
        ("Childhood name", format!("**{c}** \u{2014} {} + {}", child[0].1, child[1].1)),
        ("Adult name (at the Telling)", format!("**{a}** \u{2014} {} + {}", adult[0].1, adult[1].1)),
        ("Calling-name (intimates)", format!("**{}**", adult[0].0)),
        ("True name (taboo)", format!("**{a} Yukari** \u{2014} family, Council, a Proving, or before Senri's stone only")),
        ("Posthumous name", format!("**{p}** \u{2014} {} + {}", post[0].1, post[1].1)),
    ])
}

fn dawi(r: &mut Random) -> Value {
    let b = &BANK["dawi"];
    let (x, y) = pick2(&b["elements"], r);
    let given = join(&x.0, &y.0);
    let (fa, fb) = pick2(&b["elements"], r);
    let father = join(&fa.0, &fb.0);
    done(format!("{given} {father}sson"), b, vec![
        "Consonant gradation at the join: named by the rule, no table given \u{2014} left plain.".into(),
        "Byname and oath-name are earned in play; the bot does not invent them. An absent oath-name is audible.".into(),
    ], vec![
        ("Given name", format!("**{given}** \u{2014} {} ({}) + {} ({})", x.0, x.1, y.0, y.1)),
        ("Patronymic", format!("**{father}sson** \u{2014} son/daughter of {father} ({}-{})", fa.1, fb.1)),
        ("Earned byname", "\u{2014} (earned; e.g. *the Immovable*, for holding a doorway during a collapse)".into()),
        ("Oath-name", "absent \u{2014} not yet sworn".into()),
    ])
}

fn concord_pool(c: &Value, sex: &str) -> Vec<String> {
    match sex {
        "male" => strings(&c["male"]),
        "female" => strings(&c["female"]),
        _ => strings(&c["male"]).into_iter().chain(strings(&c["female"])).collect(),
    }
}

fn concord(r: &mut Random, sex: &str) -> Value {
    let b = &BANK["concord"];
    let given = r.choice(&concord_pool(b, sex));
    let father = r.choice(&strings(&b["male"]));
    let kind = r.choice(&["patronymic", "occupational", "locative", "descriptive"]);
    let mut flags = vec!["Three people in the village share this given name; the byname is the real identifier.".to_string()];
    let (byname, how) = if kind == "patronymic" {
        let rural = r.random() < 0.5;
        (if rural { format!("{father}sohn") } else { father.clone() }, format!("patronymic, {} \u{2014} father {father}", if rural { "live (rural, one generation)" } else { "frozen (urban, chartered)" }))
    } else {
        flags.push(format!("The {kind} list is bot-supplied plain-register filler; the guide gives that type by example only."));
        (r.choice(&strings(&b[kind]["list"])), format!("{kind} byname"))
    };
    done(format!("{given} {byname}"), b, flags, vec![
        ("Given name", format!("**{given}** \u{2014} from the thirty-name pool")),
        ("Byname", format!("**{byname}** \u{2014} {how}")),
    ])
}

fn holy_sea(r: &mut Random, sex: &str) -> Value {
    let (b, c) = (&BANK["holy_sea"], &BANK["concord"]);
    let birth_a = r.choice(&concord_pool(c, sex));
    let birth = format!("{birth_a} {}", r.choice(&strings(&c["male"])));
    let ordination = r.choice(&strings(&b["ordination"]["list"]));
    let title = r.choice(&strings(&b["titles"]["list"]));
    done(format!("{ordination} {title}"), b, vec![
        "The Latin ordination and title pools are bot-supplied filler in the attested register (Aurelian Prudentius Custos Clausorum; Verinus VII), not canon.".into(),
        "Which name a speaker uses declares whether the conversation is secular or sacred.".into(),
    ], vec![
        ("Birth name (Concord Common)", format!("**{birth}**")),
        ("Ordination name (Latin, at vows)", format!("**{ordination}**")),
        ("Title / locative", format!("**{title}** \u{2014} add the locative of the seat, e.g. *{title} of \u{2026}*")),
    ])
}

fn elven(r: &mut Random, branch: &str) -> Value {
    let b = &BANK["elven"];
    let branch = if b["branches"].get(branch).is_some() { branch.to_string() } else { r.choice(&elven_branches()) };
    let br = &b["branches"][&branch];
    let roots: Vec<(String, String)> = items(&b["roots"]).into_iter().filter(|(k, _)| !matches!(k.as_str(), "ma" | "ur" | "ie")).collect();
    let own = r.random() < 0.5;
    let (root, gloss) = if own { (st(br, "root"), st(br, "gloss")) } else { r.choice(&roots) };
    let suffix = st(br, "suffix");
    let cap = capitalize(&root);
    let name = format!("{cap}{}", suffix.trim_start_matches('-'));
    let alt = format!("{cap}{}", st(br, "alt_suffix").trim_start_matches('-'));
    let byname = format!("{cap}ith");
    let form = st(br, "form").replace("{name}", &name).replace("{alt}", &alt);
    let affix = b["affixes"].get(&suffix).map_or("none; the branch marks assent another way".to_string(), txt);
    let lines = vec![
        ("Branch", format!("**{branch}**")),
        ("Root", format!("**{root}** \u{2014} {gloss}{}", if own { " (the branch's own root)" } else { "" })),
        ("Suffix", if suffix.is_empty() { "none \u{2014} see the form".to_string() } else { format!("**{suffix}** \u{2014} {affix}") }),
        ("On the page", form),
        ("Small name / by-name", format!("**{byname}** (-ith)")),
    ];
    done(name, b, vec!["Roots carry a pitch contour (level/rising/falling) the text does not spell per root; not rendered here.".into()], lines)
}

fn beastkin(r: &mut Random, lineage: &str) -> Value {
    let b = &BANK["beastkin"];
    let lineage = if lineage != "any" && b["expectation"].get(lineage).is_some() { lineage.to_string() } else { r.choice(&beastkin_lineages()) };
    let circ = r.choice(&items(&b["circumstance"]));
    let own = items(&b["expectation"][&lineage])[0].clone();
    let exp = if r.random() < 0.75 { own } else { items(&b["expectation"]["any"])[0].clone() };
    let soul = format!("{}-{}", circ.0, exp.0.to_lowercase());
    let k = &b["keeping"];
    done(soul.clone(), b, vec![
        "Name-Keeping is documented for the Fox-Spirit lineage; the inventory generalises it to the others and flags that.".into(),
        "The daily use-name is separate and ordinary \u{2014} not generated here.".into(),
    ], vec![
        ("Lineage", format!("**{lineage}**")),
        ("Circumstance", format!("**{}** \u{2014} {}", circ.0, circ.1)),
        ("Expectation", format!("**{}** \u{2014} {}", exp.0, exp.1)),
        ("Soul-name", format!("**{soul}** \u{2014} recorded, not used daily")),
        ("Name-Keeping", format!("*\u{201c}Fen {soul}, Baru\u{201d}* ({}; {}) \u{2014} the witness answers *\u{201c}Ashe\u{201d}* ({})", st(k, "Fen"), st(k, "Baru"), st(k, "Ashe"))),
    ])
}

fn far_northern(r: &mut Random) -> Value {
    let b = &BANK["far_northern"];
    let (vowels, onsets, codas) = (strings(&b["vowels"]), strings(&b["onsets"]), strings(&b["codas"]));
    let n = r.choice(&[2usize, 2, 3]);
    let mut syl: Vec<(String, String, String)> = Vec::new();
    for i in 0..n {
        let on = if i > 0 || r.random() < 0.8 { r.choice(&onsets) } else { String::new() };
        let v = r.choice(&vowels);
        let co = if i < n - 1 && r.random() < 0.45 { r.choice(&codas) } else { String::new() };
        syl.push((on, v, co));
    }
    // geminate across a boundary: double the next onset when the previous syllable has no coda
    let mut name = String::new();
    for i in 0..syl.len() {
        let (on, v, co) = syl[i].clone();
        let on = if i > 0 && syl[i - 1].2.is_empty() && on.chars().count() == 1 && r.random() < 0.35 { on.repeat(2) } else { on };
        name += &format!("{on}{v}{co}");
    }
    if r.random() < 0.6 {
        name += r.choice(&strings(&b["suffixes"])).trim_start_matches('-');
    }
    let name = capitalize(&name);
    let roll = r.choice(&strings(&b["roll_names"]["list"]));
    let c = &BANK["concord"];
    let given = r.choice(&strings(&c["male"]).into_iter().chain(strings(&c["female"])).collect::<Vec<_>>());
    done(name.clone(), b, vec![
        "Sound-shape only: R23-11-PHONOTACTICS gives the phonology, not a morpheme list. Assign the meaning, and remember the name is a specific dead person given on.".into(),
        "The roll-name list is bot-supplied filler (a trade or landmark, per R23-11-ROLL_NAMES_FROM_ACCORD).".into(),
    ], vec![
        ("Carried name (household)", format!("**{name}** \u{2014} the kin-turn comes with it")),
        ("Roll-name (the Accord's ledger)", format!("**{given} {roll}** \u{2014} what the muster and the tax survey use")),
        ("Unspoken", "while the person it belonged to lies in the death-house, through the Waiting".into()),
    ])
}

fn moto(r: &mut Random) -> Value {
    let b = &BANK["moto"];
    let (mut x, mut y, mut given) = (Default::default(), El::default(), String::new());
    for _ in 0..30 {
        // two to four syllables (Naming Guide 5.1): re-pick while the compound runs long
        (x, y) = pick2(&b["elements"], r);
        given = join(&x.0, &y.0);
        if given.to_lowercase().chars().filter(|c| "aeiou\u{101}\u{12b}\u{16b}\u{113}\u{14d}".contains(*c)).count() <= 4 {
            break;
        }
    }
    let x: El = x;
    let kokan = r.random() < 0.3;
    let line = if kokan { None } else { Some(r.choice(&strings(&b["lines"]))) };
    let full = match &line {
        None => format!("{given} Moto"),
        Some(l) => format!("{given} {l} Moto"),
    };
    done(full, b, vec![
        "Glosses on Doku, Muken, Bara and Zuri are coined and ratified as flags.".into(),
        "Whether Kokan is ever carried as a Line name is open; the bank omits it, as every attested Kokan name does.".into(),
    ], vec![
        ("Given name", format!("**{given}** \u{2014} {} ({}, {}) + {} ({}, {})", x.0, x.1, x.2, y.0, y.1, y.2)),
        ("Line", line.map_or("**K\u{14d}kan** \u{2014} the seat; no Line name is carried".to_string(), |l| format!("**{l}**"))),
        ("Reads as", format!("\u{201c}{}\u{201d} + \u{201c}{}\u{201d}", x.1, y.1)),
        ("Renaming", "at promotion, vow or change of allegiance \u{2014} a feature of this stratum".into()),
    ])
}

fn celestial(r: &mut Random) -> Value {
    let b = &BANK["celestial"];
    let f = r.choice(&items(&b["functions"]));
    let m = r.choice(&items(&b["measures"]));
    let rank = r.choice(&items(&b["ranks"]));
    let arch = r.choice(&items(&b["archons"]));
    let choir = r.choice(&strings(&b["choirs"]));
    let fun = format!("{}{}", f.0, m.0);
    let full = format!("{fun}-{} {}", rank.0, arch.0);
    done(fun.clone(), b, vec![
        "Function and measure roots are coined on the Host's own vocabulary; the Archon names are attested.".into(),
        "The Lawbell-name is carried bare; a Parunic genitive form was left open.".into(),
    ], vec![
        ("Function-name", format!("**{fun}** \u{2014} {} ({}) + -{} ({})", f.0, f.1, m.0, m.1)),
        ("Rank-suffix", format!("**-{}** \u{2014} {}", rank.0, rank.1)),
        ("Lawbell-name", format!("**{}** \u{2014} the Archon of {}; its loss is the Severance", arch.0, arch.1)),
        ("Choir", format!("**{choir}**")),
        ("In the Host's register", format!("**{full}** \u{2014} \u{201c}{fun}, {}, of {}\u{201d}; mortals hear only **{fun}**", rank.1, arch.1)),
    ])
}

pub fn build(culture: &str, seed: u64, branch: &str, lineage: &str, sex: &str) -> Result<Value, String> {
    let r = &mut Random::from_be_bytes(&seed.to_be_bytes());
    Ok(match culture {
        "mahuo" => mahuo(r),
        "moto" => moto(r),
        "celestial" => celestial(r),
        "yukari" => yukari(r),
        "dawi" => dawi(r),
        "concord" => concord(r, sex),
        "holy_sea" => holy_sea(r, sex),
        "elven" => elven(r, branch),
        "beastkin" => beastkin(r, lineage),
        "far_northern" => far_northern(r),
        o => return Err(format!("no culture {o}")),
    })
}
