//! build/verify.py and build/american_spelling.py, ported line for line. Every check, pattern and
//! message matches the Python (rust/parity.py diffs the two over the whole scene archive), so the
//! comments that name a rule live in verify.py; this file only notes where Rust differs.
//! Python's `$` without (?m) also matches before a final newline; those patterns end in `\n?\z` here.
use crate::util::{back, fwd, head, read_lossy, root, tail};
use fancy_regex::{Captures, Match, Regex, RegexBuilder};
use std::collections::{BTreeMap, HashMap, HashSet};
use std::sync::LazyLock;

fn build(p: &str) -> Regex {
    RegexBuilder::new(p).backtrack_limit(50_000_000).build().unwrap_or_else(|e| panic!("bad regex {p}: {e}"))
}
macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| build(&$p));
        &*R
    }};
}

fn finds<'a>(r: &Regex, s: &'a str) -> Vec<Match<'a>> {
    r.find_iter(s).flatten().collect()
}
fn first<'a>(r: &Regex, s: &'a str) -> Option<Match<'a>> {
    r.find(s).ok().flatten()
}
fn caps<'a>(r: &Regex, s: &'a str) -> Option<Captures<'a, str>> {
    r.captures(s).ok().flatten()
}
fn has(r: &Regex, s: &str) -> bool {
    r.is_match(s).unwrap_or(false)
}
fn sub(r: &Regex, s: &str, rep: &str) -> String {
    r.replace_all(s, rep).into_owned()
}
/// re.split without groups.
fn split<'a>(r: &Regex, s: &'a str) -> Vec<&'a str> {
    let mut out = Vec::new();
    let mut last = 0;
    for m in finds(r, s) {
        out.push(&s[last..m.start()]);
        last = m.end();
    }
    out.push(&s[last..]);
    out
}
/// `s[max(0, start-b):end+a].replace("\n", " ").strip()`
fn win(s: &str, start: usize, end: usize, b: usize, a: usize) -> String {
    s[back(s, start, b)..fwd(s, end, a)].replace('\n', " ").trim().to_string()
}
/// Python's rx.search(s, pos, endpos) with pos/endpos as char distances around a match.
fn search_around(r: &Regex, s: &str, start: usize, end: usize, b: usize, a: usize) -> bool {
    r.find_from_pos(&s[..fwd(s, end, a)], back(s, start, b)).ok().flatten().is_some()
}
fn words(s: &str) -> usize {
    s.split_whitespace().count()
}

// ---------------------------------------------------------------- american_spelling.py
const PAIRS: &[(&str, &str)] = &[
    (r"colour(s|ed|ing|ful|less|ist|ists|ation|ings)?", r"color\1"),
    (r"favour(s|ed|ing|ite|ites|able|ably)?", r"favor\1"),
    (r"honour(s|ed|ing|able|ably)?", r"honor\1"),
    (r"humour(s|ed|ing|ous|ist|ists)?", r"humor\1"),
    (r"neighbour(s|ed|ing|hood|hoods|ly)?", r"neighbor\1"),
    (r"labour(s|ed|er|ers|ing)?", r"labor\1"),
    (r"flavour(s|ed|ing|ful|some)?", r"flavor\1"),
    (r"harbour(s|ed|ing)?", r"harbor\1"),
    (r"rumour(s|ed)?", r"rumor\1"),
    (r"vapour(s)?", r"vapor\1"),
    (r"odour(s)?", r"odor\1"),
    (r"behaviour(s|al)?", r"behavior\1"),
    (r"savour(s|ed|ing|y)?", r"savor\1"),
    (r"armour(s|ed|er|ers|y)?", r"armor\1"),
    (r"endeavour(s|ed|ing)?", r"endeavor\1"),
    (r"parlour(s)?", r"parlor\1"),
    (r"rigour(s|ous)?", r"rigor\1"),
    (r"vigour(ous|ously)?", r"vigor\1"),
    (r"valour", r"valor"),
    (r"clamour(s|ed|ing|ous)?", r"clamor\1"),
    (r"splendour(s)?", r"splendor\1"),
    (r"candour", r"candor"),
    (r"fervour", r"fervor"),
    (r"saviour(s)?", r"savior\1"),
    (r"arbour(s)?", r"arbor\1"),
    (r"ardour", r"ardor"),
    (r"tumour(s)?", r"tumor\1"),
    (r"demeanour", r"demeanor"),
    (r"grey(s|ed|ing|er|est|ish|ness)?", r"gray\1"),
    (r"defence(s|less)?", r"defense\1"),
    (r"offence(s)?", r"offense\1"),
    (r"pretence(s)?", r"pretense\1"),
    (r"licence(s|d)?", r"license\1"),
    (r"practise(s|d)?", r"practice\1"),
    (r"centre(s|d|piece|pieces)?", r"center\1"),
    (r"metre(s)?", r"meter\1"),
    (r"litre(s)?", r"liter\1"),
    (r"fibre(s)?", r"fiber\1"),
    (r"theatre(s)?", r"theater\1"),
    (r"sabre(s)?", r"saber\1"),
    (r"mould(s|ed|ing|y)?", r"mold\1"),
    (r"moustache(s|d)?", r"mustache\1"),
    (r"plough(s|ed|ing|man|men|share)?", r"plow\1"),
    (r"towards", r"toward"),
    (r"whilst", r"while"),
    (r"amongst", r"among"),
    (r"artefact(s)?", r"artifact\1"),
    (r"sulphur(ous|ic|ates?)?", r"sulfur\1"),
    (r"manoeuvr(e|es|ed|ing)", r"maneuver\1"),
    (r"judgement(s)?", r"judgment\1"),
    (r"ageing", r"aging"),
    (r"catalogue(s|d)?", r"catalog\1"),
    (r"travell(ed|er|ers|ing)", r"travel\1"),
    (r"levell(ed|ing)", r"level\1"),
    (r"fuell(ed|ing)", r"fuel\1"),
    (r"labell(ed|ing)", r"label\1"),
    (r"modell(ed|ing)", r"model\1"),
    (r"signall(ed|ing)", r"signal\1"),
    (r"marvellous(ly)?", r"marvelous\1"),
    (r"jewellery", r"jewelry"),
    (r"counsellor(s)?", r"counselor\1"),
    (r"woollen", r"woolen"),
    (r"burnt", r"burned"),
    (r"learnt", r"learned"),
    (r"spilt", r"spilled"),
    (r"dreamt", r"dreamed"),
    (r"leant", r"leaned"),
    (r"smelt", r"smelled"),
    (r"kerb(s)?", r"curb\1"),
    (r"tyre(s)?", r"tire\1"),
    (r"cheque(s)?", r"check\1"),
    (r"aluminium", r"aluminum"),
    (r"cosy", r"cozy"),
    (r"pyjamas", r"pajamas"),
    (r"plait(s|ed|ing)?", r"braid\1"),
];

static SPELLING: LazyLock<Vec<(Regex, String)>> = LazyLock::new(|| {
    PAIRS.iter().map(|(a, b)| (build(&format!(r"(?i)\b{a}\b")), b.replace(r"\1", "${1}"))).collect()
});

/// american_spelling.british: distinct British spellings as (found, american), lowercased, sorted.
pub fn british(text: &str) -> Vec<(String, String)> {
    let mut seen: BTreeMap<String, String> = BTreeMap::new();
    for (r, rep) in SPELLING.iter() {
        for c in r.captures_iter(text).flatten() {
            let mut out = String::new();
            c.expand(rep, &mut out);
            seen.entry(c[0].to_lowercase()).or_insert(out.to_lowercase());
        }
    }
    seen.into_iter().collect()
}

// ---------------------------------------------------------------- verify.py patterns
const FACULTIES: &str = r"(?:Cymorath|Kamigan|Shingan|Meigan|Reigan|Tengan|Ketsumy[oō]gan|Crown Eye|Seeing|Ruling Sight|Revealing Sight|Spirit Sight|Sky Sight)";
const P: &str = r"(?:his|her|their|my|your|its)";
const RUNNING: &str = r"\b\d[\d,.]*\s?(?:EU|AU/s)\b|(?:\bEU|\bAU/s|η|\beta)\s*:?\s*\d";
const NUM: [&str; 20] = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
    "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
const TENS: [&str; 8] = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
static AGE_NUM: LazyLock<String> = LazyLock::new(|| {
    format!(
        r"(?:(\d[\d,]*)(?![\d,])|\b({})(?:-({}))?(?!-)\b|\b({})\b)(?:\s+(hundred|thousand))?(?!\s+years?\s+(?:older|younger))",
        TENS.join("|"),
        NUM[1..10].join("|"),
        NUM.join("|")
    )
});

fn em_dash() -> &'static Regex { rx!(r"—|(?<!-)--(?!-)") }
fn antithesis() -> [&'static Regex; 3] {
    [
        rx!(r"(?i)\b(?:not|isn['’]t|wasn['’]t|is not|was not|aren['’]t|weren['’]t)\s+(?:just|merely|simply|only|so much)\b[^.!?\n]{0,80}?\b(?:but|it['’]s|it is|as|rather)\b"),
        rx!(r"(?i)\b(?:this|that|it|which|he|she)\s+(?:is|was)\s+(?:less|more)\s+(?:a |an )?\w+\s+than\s+(?:a |an |it was |it is )?\w+"),
        rx!(r"(?i)\b(?:it|this|that)\s+(?:is|was|isn['’]t|wasn['’]t)\s+not\s+(?:a |an |the )?[\w\s]{1,30}?[,;]\s*(?:but|it['’]s|it was|it is)\b"),
    ]
}
fn not_frag() -> &'static Regex {
    rx!(r#"(?m)(?:^|(?<=[.!?] )|(?<=[.!?][”"*] )|(?<=[*“"]))Not(?: [\w'’-]+){1,3}[.!] (?!(?:Not|No|Never|Nor|Nothing|None|Nobody|Neither|Nowhere|Yes|Please)\b)(?:[A-Z][\w'’-]*|(?:A|An|The|His|Her|Their|Its|One)(?: [\w'’-]+){1,2})[.!](?=\s|$|[”"’*])"#)
}
fn ladder() -> &'static Regex { rx!(r"(?i)\b(?:was|is|became|meant)\s+[a-z]+\s+and\s+the\s+[a-z]+\s+(?:was|is|became|meant)\b") }
fn apparatus() -> &'static Regex {
    rx!(format!(r"\b(?:his|her|the|their)\s+{FACULTIES}\s+(?:saw|read|mapped|noted|caught|found|registered|filed|marked|tracked|perceived|counted|watched|traced|classified|flagged|told|reported)\b"))
}
fn tidy_close() -> &'static Regex { rx!(r"(?i)^(?:Ultimately|In the end|And so|Finally|At last|Perhaps that|Maybe that)\b") }
fn hypophora_q() -> &'static Regex { rx!(r"\?\s*\z") }
fn calendar() -> &'static Regex {
    rx!(r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|April|June|July|August|September|October|November|December|[Ww]eekends?)\b|(?<=[a-z,;] )(?:May|March)\b")
}
fn holy_oath() -> &'static Regex { rx!(r"\b(?:(?i:god\s*damn\w*|go to hell|for god['’]s sake)|Christ|Jesus)\b") }
fn slop() -> &'static Regex {
    rx!(r"(?i)\b(?:testaments? to|symphony of|a dance of|orbs|electric\w*\W+(?:\w+\W+){0,3}?touch\w*|touch\w*\W+(?:\w+\W+){0,3}?electric\w*|velvety? voice|shiver\w* down (?:his|her|their|my|your) spine|breath (?:he|she|they|I) didn['’]t know (?:he|she|they|I) (?:was|were) holding|coppery tang)\b")
}
fn slop_stock() -> [(&'static str, &'static Regex); 2] {
    [
        ("testament", rx!(r"(?i)\btestaments? to\b")),
        ("orbs", rx!(r"(?i)\b(?:his|her|their|my|your) (?:[\w-]+ ){0,2}orbs\b|\borbs (?:of (?:his|her|their|my|your) (?:eyes|breasts|bosom)|(?:\w+ )?(?:widen|narrow|blink|squint|flick|fixed on|met (?:his|her|their|mine|yours)\b))")),
    ]
}
fn stock() -> &'static Regex {
    rx!(format!(r"(?i)\bqi (?:surge[sd]?|surging)\b|\ba cold glint flash(?:ed|es)?\b|\bsuck(?:ed|s|ing)? in a cold breath\b|\bkilling intent (?:surge[sd]?|surging)\b|\bthe steel (?:sang|sings|singing)\b|\ba grim smile\b|\b{P} blood (?:ran|runs|running) cold\b|\bevery fib(?:re|er) of {P} being\b|\bdarkness (?:gathered|gathers|gathering)\b|\bpower surged through (?:him|her|them|me|you)\b|\bstronger than ever\b|\ba wave of power\b|\b{P} stats (?:soared|soar|soars|soaring)\b"))
}
fn stock_loose() -> &'static Regex {
    rx!(format!(r"(?i)\bqi (?:boiled|churned|exploded|erupted)\b|\bcold (?:glint|gleam|light) (?:flash|flicker)\w*|\b(?:drew|took|sucked) (?:in )?a (?:cold|chill) breath\b|\bsteel (?:sang|sings|singing)\b|\bgrim(?:ly)? smil\w+|\bsmiled grimly\b|\bblood (?:ran|runs|turned|went) (?:cold|to ice)\b|\bfib(?:re|er)s? of {P} being\b|\bdarkness (?:pooled|coiled|swirled|thickened)\b|\b(?:power|strength|energy) (?:surged|surging|flooded|coursed) through\b|\bsurge of (?:power|strength|energy)\b|\bwave of (?:strength|energy)\b|\bstats? (?:soared|rose|climbed|jumped|skyrocketed)\b"))
}
fn formula() -> &'static Regex {
    rx!(r"(?i)\b(?:(?:you )?court(?:s|ed|ing)? death|seek(?:s|ing)? death|sought death|this junior|this old man|los(?:e|es|ing|t) face|this one (?:humbly|dares|begs|greets|thanks|apologi[sz]es|is grateful|is honou?red|offers|requests|will obey))\b")
}
fn gamer() -> &'static Regex { rx!(r"(?i)\b(?:min-?max\w*|dump stats?|aggro|cool-?downs?|debuff\w*|nerf\w*|DPS)\b") }
const LOANWORDS: [&str; 6] = ["qi", "gi", "ki", "dao", "danjeon", "dantian"];
fn digit() -> &'static Regex {
    rx!(r"(?<![\w.,:/-])(\d{1,3})(?![\w.,:/%-]?\d)(?!\s?(?:%|°|(?:EU|AU|Hz|kHz|kg|g|km|cm|mm|m|m/s|s|ms|J|kJ|W|kW|N|Pa|kPa|K|lbs?|ft)\b))")
}
fn label_before() -> &'static Regex { rx!(r"\b[A-Z][A-Za-z]*[.:]?[ \t]+(?:\d{1,3},?[ \t]+(?:and[ \t]+|or[ \t]+)?)*\n?\z") }
fn readout() -> &'static Regex { rx!(r"(?m)^[ \t]*\[[^\]\n]+\][ \t]*(?:\n|$)") }
fn running() -> &'static Regex { rx!(RUNNING) }
fn readout_fig() -> &'static Regex {
    rx!(format!(r"(?i:\b(?:stage|level|grade|tier|band|rung|reserve|coherence)(?: ceiling)?\b)\s*:?\s*(?:\d[\d,.]*|(?:[IVX]+|[A-FS][+-]?)(?![\w'’])(?!\s+[a-z]))|{RUNNING}"))
}
fn quoted() -> &'static Regex { rx!(r#"["“][^"“”\n]*["”]"#) }
fn italic() -> &'static Regex { rx!(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)") }
pub(crate) fn blade_action() -> &'static Regex {
    rx!(r"(?i)\b(?:bind|half-sword|halfsword|pommel|guard|ward|thrust|cut|feint|parry|riposte|void|cross|edge|flat|crossguard|quillon|point|counter-cut|blade|sword|weight|heel|heels|foot|feet|stance|step(?:s|ped|ping)?)\b")
}
pub(crate) fn anatomy() -> &'static Regex {
    rx!(r"(?i)\b(?:jaws?|collarbones?|cheekbones?|throats?|windpipe|necks?|guts?|belly|bellies|groin|knees?|kneecaps?|wrists?|elbows?|shoulders?|hips?|thighs?|shins?|ankles?|teeth|tooth|ribcage|bones?|skulls?|arter(?:y|ies)|veins?|femoral|carotid|clavicle|radius|ulna|humerus|tibia|fibula|patella|scapula|sternum|rib|ribs|vertebra|spine|jugular|subclavian|brachial|aorta|lung|liver|kidney|spleen|diaphragm|tendon|ligament|cartilage|orbit|mandible|maxilla|skull|trachea|larynx|hypovol|haemorrh|hemorrh|shock|Class\s+(?:I|II|III|IV))\b")
}
fn strike() -> &'static Regex {
    rx!(r"\b(?:(?:hit|hits|struck|strikes|punch(?:ed|es)?|kick(?:ed|s)?|slash(?:ed|es)?|stabb?(?:ed|s)?|chopp?(?:ed|s)?|smash(?:ed|es)?|slamm?(?:ed|s)?|elbowed|kneed|head-?butt(?:ed)?|cut) (?:him|her|them|the (?:Sin|man|woman|boy|girl|arm|leg|head|face|side|shoulder)|[A-Z][a-z]+\b)|took (?:him|her|them) (?:in|on|across|under))")
}
fn mechanics() -> &'static Regex {
    rx!(r"(?i)\b(?:heels?|hips?|shoulders?|foot|feet|toes?|knees?|weight|stance|step(?:s|ped)?|pivot\w*|lunge\w*|torque|momentum|leverage|braced?|planted|drove|wind-?up|swung|swing)\b")
}
fn school(name: &str) -> Option<&'static Regex> {
    Some(match name {
        "blade" => blade_action(),
        "japanese" => rx!(r"(?i)\b(?:maai|ma-ai|kamae|ch[uū]dan|j[oō]dan|gedan|hass[oō]|waki-?gamae|seme|kiai|zanshin|tsuki|kesa-?giri|kiri-?oroshi|nukitsuke|iai\w*|batt[oō]\w*|n[oō]t[oō]|chiburi|tsuba|kissaki|shinogi|monouchi|hasuji|metsuke|kuzushi|irimi|tenkan|atemi|tai-?sabaki|ashi-?sabaki|suriage|nagashi|kaeshi|(?:sen|go)[ -]no[ -]sen|kote|tachi|katana|wakizashi|tant[oō]|naginata|yari|saya)\b"),
        "chinese" => rx!(r"(?i)\b(?:jian|dao|qiang|guandao|fa ?jin|fali|qinna|chin na|chan ?si|silk-reeling|tui ?shou|push-?hands|zhan zhuang|ma ?bu|gong ?bu|horse stance|bow stance|dantian|taolu|sanshou|sanda|liuhe|six harmonies|neijia|waijia|qinggong|dianxue|bagua|xingyi|taiji|tai chi|wing chun|chi sao)\b"),
        "korean" => rx!(r"(?i)\b(?:taekky[eo]on|ssireum|satba|geomdo|gumdo|kumdo|haidong|ssangsudo|bonguk ?geom\w*|muye ?dobo ?tongji|hwando|jireugi|makgi|chagi|chigi|gyeorugi|pumsae|poomsae|subak|gwonbeop|kwonbeop|baejigi|woldo)\b"),
        "percussion" => rx!(r"(?i)\b(?:hafts?|hammer-?heads?|rims?|boss|shields?|(?:war-?)?hammers?|mauls?|maces?|flails?|clubs?|cudgels?|axe-?beards?|bearded axes?|hook(?:s|ed)?|shov(?:e|es|ed|ing)|rebound\w*|poll|spikes?|(?-i:the (?:Settling|Sweep|Shove|Return)))\b"),
        "boxing" => rx!(r"(?i)\b(?:jab(?:s|bed|bing)?|cross|hooks?|uppercuts?|haymakers?|overhands?|clinch\w*|southpaw|orthodox|teeps?|plum|body shots?|liver shots?|counterpunch\w*|combinations?|footwork|bob(?:bed|bing)?|weav(?:e|ed|ing)|slip(?:s|ped|ping)?|roundhouse|feints?|guard|pivot\w*|(?:elbow|knee) strikes?|straight (?:right|left)|short (?:right|left))\b"),
        "firearms" => rx!(r"(?i)\b(?:guns?|gun(?:fire|powder|shots?|smoke)|hammers?|percussion caps?|muzzles?|cylinders?|volleys?|reload\w*|ramrods?|rifle[ds]?|revolvers?|flintlocks?|muskets?|pistols?|carbines?|cartridges?|powder|priming|frizzen|breech\w*|barrels?|wad(?:ding)?|trigger\w*|misfire[ds]?)\b"),
        "kharven" => rx!(r"(?i)\b(?:belt-?wrestl\w*|belts?|grip(?:s|ped|ping)?|forearm|hip-?throws?|throws?|threw|thrown|trip(?:s|ped|ping)?|axes?|hatchets?|spears?|lances?|harpoons?|knife|knives|(?:horse-?)?bows?|arrows?|saddles?|stirrups?|seal-?clubs?)\b"),
        _ => return None,
    })
}
const SCHOOL_CULTURES: [(&str, &[&str]); 4] = [
    ("japanese", &["moto", "yukari", "ketsuen", "shirogane", "kokan", "kōkan", "japon"]),
    ("korean", &["mahuo", "hon-guk", "honguk", "korea"]),
    ("chinese", &["lineage", "chinese"]),
    ("kharven", &["kharven"]),
];
fn notes() -> &'static Regex { rx!(r"(?im)^##\s+(?:author[\w-]*\s+)?notes\b") }
fn stale() -> [(&'static str, &'static Regex); 5] {
    [
        ("'eleven' as a count", rx!(r"(?i)(?<!Pack )(?<!Part )(?<!Chapter )(?<!Year )(?<!hundred and )(?<!thousand and )\beleven\b(?! hundred| thousand)")),
        ("the knock-back furrow", rx!(r"(?i)\b(?:heels?|boots?|feet)\b[^.!?\n]{0,30}?\b(?:plough|plow|dug|dig|goug|carv|tore|tear|scor)\w*[^.!?\n]{0,30}?\b(?:furrows?|grooves?|trench(?:es)?)\b|\bgoug(?:e|es|ed|ing) (?:\w+ ){0,2}?(?:furrows?|trench(?:es)?)\b")),
        ("the overdraw nosebleed", rx!(r"(?i)^(?!.*\b(?:punch\w*|fists?|knuckles?|jab\w*|elbowed|kneed|head-?butt\w*|pommel|kick\w*|slap\w*|hit|struck|broke|broken|smash\w*)\b).*?(?:\bnose-?bleeds?\b|\b(?:nose|nostrils?)(?:[ -][\w'’]+){0,3}? (?:bled|bleeds?|bleeding|(?:to|run|ran|running) blood)\b|\bblood\b[^.!?\n]{0,30}?\b(?:from|out of)\b[^.!?\n]{0,15}?\b(?:nose|nostrils?)\b)")),
        ("'without deciding to'", rx!(r"(?i)\bwithout (?:(?:his|her|their|my|its) )?(?:having )?(?:deciding|decided) to\b")),
        ("'the particular X of Y'", rx!(r"(?i)\bthe particular (?:[\w'’-]+ ){1,3}?of\b")),
    ]
}
fn mimetic_full() -> &'static Regex { rx!(r"(?i)^(?:\b([a-z]{2,7})-\1\b|\b(?:kyun|dokun)\b)\z") }
fn euphemism() -> &'static Regex {
    rx!(r"\b[Hh]is member\b|\b[Hh]er sex\b|(?<!into )(?<!toward )(?<!towards )(?<!of )\b[Mm]anhood\b|\b[Hh]is length\b(?! of\b)")
}
const CARD_DIRS: [&str; 2] = ["Characters/Volume I \u{2014} Character Cards", "Characters"];
const NAME_TITLES: [&str; 9] = ["The", "Lord", "Lady", "Sir", "Ser", "Dr.", "Commander", "Elder", "Captain"];
fn age_field() -> &'static Regex {
    rx!(r"(?m)\*\*Age(?:\s*/\s*\w+)?[:.]?\*\*[ \t]*[:.·|]?[ \t]*([^·|\n]+)|(?:^|\.[ \t])Age (\d{1,4})\.")
}

// ---------------------------------------------------------------- helpers
pub fn split_sentences(text: &str) -> Vec<String> {
    let t = sub(rx!(r"\s+"), text, " ");
    split(rx!(r#"(?<=[.!?])\s+(?=["“‘'A-Z])"#), &t).into_iter().map(str::trim).filter(|s| !s.is_empty()).map(String::from).collect()
}

pub fn strip_md(text: &str) -> String {
    let t = sub(rx!(r"(?m)^#{1,6}\s+.*$"), text, "");
    let t = sub(rx!(r"(?m)^---\s*$"), &t, "");
    sub(rx!(r"\*\*(.+?)\*\*"), &t, "${1}")
}

fn school_for(culture: Option<&str>) -> &'static str {
    let c = culture.unwrap_or("").to_lowercase();
    SCHOOL_CULTURES.iter().find(|(_, keys)| keys.iter().any(|k| c.contains(k))).map(|(s, _)| *s).unwrap_or("blade")
}

/// verify.card_age: the body's age from a card's Age field, never a soul's.
pub fn card_age(field: &str) -> Option<i64> {
    let f = field.replace('*', "");
    let v = sub(rx!(r"ies\b"), &f.split(". ").next().unwrap_or("").to_lowercase(), "y");
    let m = caps(rx!(format!(r"\b(?:body|vessel)\W+(?:age\W+)?{}", &*AGE_NUM)), &v)
        .or_else(|| caps(rx!(format!(r"{}\W+(?:body|vessel)\b", &*AGE_NUM)), &v))
        .or_else(|| {
            if v.contains("soul") {
                return None;
            }
            caps(rx!(format!(r"^(?:[\s~(-]|\b(?:about|around|roughly|nearly|apparently|appears|looks|indeterminate|early|mid|late)\b)*{}", &*AGE_NUM)), &v)
        })?;
    let g = |i| m.get(i).map(|x| x.as_str());
    let idx = |w: &str| NUM.iter().position(|n| *n == w).unwrap_or(0) as i64;
    let n = if let Some(d) = g(1) {
        d.replace(',', "").parse::<i64>().ok()?
    } else if let Some(t) = g(2) {
        (TENS.iter().position(|x| *x == t).unwrap() as i64 + 2) * 10 + idx(g(3).unwrap_or("zero"))
    } else {
        idx(g(4)?)
    };
    Some(n * match g(5) {
        Some("hundred") => 100,
        Some("thousand") => 1000,
        _ => 1,
    })
}

type Cards = (Option<Regex>, HashMap<String, Vec<(String, Option<i64>)>>, usize);

/// verify.cards: every card and table roster name with its age, a regex over the names, and the cards read
/// (plus first names no one else shares). Read on each call; the Python cached it per process.
fn cards() -> Cards {
    let wiki = root("wiki");
    let mut found: Vec<(String, Option<i64>)> = Vec::new();
    for d in CARD_DIRS {
        let mut ps: Vec<_> = std::fs::read_dir(wiki.join(d))
            .into_iter()
            .flatten()
            .flatten()
            .map(|e| e.path())
            .filter(|p| p.extension().is_some_and(|x| x == "md"))
            .collect();
        ps.sort();
        for p in ps {
            let stem = crate::util::stem(&p);
            let name = split(rx!(r" · | \u{2014} | \(|, "), &stem)[0].trim().to_string();
            if matches!(name.split_whitespace().next(), Some("Volume" | "Characters")) {
                continue; // the folders' hub pages, not people
            }
            let age = caps(age_field(), &read_lossy(&p)).and_then(|c| match c.get(1) {
                Some(g) => card_age(g.as_str()),
                None => c.get(2).and_then(|g| g.as_str().parse().ok()),
            });
            found.push((name, age));
        }
    }
    let n_cards = found.len();
    let roster = root("table/npcs.yaml");
    if roster.exists() {
        for e in split(rx!(r"(?m)^- "), &read_lossy(&roster)) {
            if let Some(n) = caps(rx!(r#"(?m)^ *name: *['"]?(.+?)['"]? *$"#), e) {
                let age = caps(rx!(r"(?m)^ *age: *(.+)$"), e).and_then(|m| card_age(&m[1]));
                found.push((n[1].to_string(), age));
            }
        }
    }
    let mut by_key: HashMap<String, Vec<(String, Option<i64>)>> = HashMap::new();
    let mut firsts: Vec<(String, HashSet<String>)> = Vec::new();
    for (name, age) in &found {
        by_key.entry(name.clone()).or_default().push((name.clone(), *age));
        let f = name.split_whitespace().next().unwrap_or("").to_string();
        match firsts.iter_mut().find(|(k, _)| *k == f) {
            Some((_, s)) => {
                s.insert(name.clone());
            }
            None => firsts.push((f, HashSet::from([name.clone()]))),
        }
    }
    for (f, names) in firsts {
        if names.len() == 1 && f.chars().count() > 2 && !NAME_TITLES.contains(&f.as_str()) && !by_key.contains_key(&f) {
            let v = by_key[names.iter().next().unwrap()].clone();
            by_key.insert(f, v);
        }
    }
    if by_key.is_empty() {
        return (None, by_key, n_cards);
    }
    let mut keys: Vec<&String> = by_key.keys().collect();
    keys.sort_by_key(|k| std::cmp::Reverse(k.chars().count()));
    let alt: Vec<String> = keys.iter().map(|k| fancy_regex::escape(k).into_owned()).collect();
    (Some(build(&format!(r"\b(?:{})\b", alt.join("|")))), by_key, n_cards)
}

fn readouts(body: &str) -> usize {
    let mut out = 0;
    let mut prev = false;
    for p in split(rx!(r"\n\s*\n"), body) {
        let lines: Vec<&str> = p.split('\n').filter(|x| !x.trim().is_empty()).collect();
        let quote: Vec<bool> = lines.iter().map(|x| x.trim_start().starts_with('>')).collect();
        let mut j = 0;
        while j < lines.len() {
            let mut e = j + 1;
            while quote[j] && e < lines.len() && quote[e] {
                e += 1;
            }
            let ro = if quote[j] { has(readout_fig(), &lines[j..e].join("\n")) } else { has(readout(), lines[j]) };
            if ro && !prev {
                out += 1;
            }
            prev = ro;
            j = e;
        }
    }
    out
}

pub struct Res {
    pub fails: Vec<String>,
    pub warns: Vec<String>,
    pub info: Vec<String>,
}

#[derive(Default)]
pub struct Opts<'a> {
    pub combat: bool,
    pub culture: Option<&'a str>,
    pub school: Option<&'a str>,
    pub turn: bool,
    pub explicit: bool,
}

fn before_notes(text: &str) -> &str {
    first(notes(), text).map(|m| &text[..m.start()]).unwrap_or(text)
}

pub fn run(text: &str, o: &Opts) -> Result<Res, String> {
    let (mut fails, mut warns, mut info) = (Vec::new(), Vec::new(), Vec::new());
    let raw = before_notes(text);
    let body = strip_md(raw);
    let no_ro = sub(readout(), &body, "");
    let paragraphs: Vec<&str> = split(rx!(r"\n\s*\n"), &no_ro).into_iter().map(str::trim).filter(|p| !p.is_empty()).collect();
    let prose_paras: Vec<&str> = paragraphs.iter().copied().filter(|p| !p.starts_with('>') && !p.starts_with('|')).collect();
    let sentences: Vec<String> = prose_paras.iter().flat_map(|p| split_sentences(p)).collect();
    let total_words: usize = sentences.iter().map(|s| words(s)).sum();

    // --- bans
    let brit = british(raw);
    if !brit.is_empty() {
        let shown: Vec<String> = brit.iter().take(8).map(|(x, y)| format!("{x} -> {y}")).collect();
        let more = if brit.len() > 8 { format!(" (+{} more)", brit.len() - 8) } else { String::new() };
        fails.push(format!("British spelling (American English only, Isaac 2026-10-30): {}{more}", shown.join(", ")));
    }
    let n = finds(em_dash(), raw).len();
    if n > 0 {
        fails.push(format!("em dashes: {n} (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)"));
    }
    let mut hits: Vec<String> = antithesis().iter().flat_map(|r| finds(r, &body).into_iter().map(|m| m.as_str().to_string())).collect();
    let flat: Vec<String> = split(rx!(r"\n\s*\n"), &body).into_iter().map(|p| sub(rx!(r"\s+"), p, " ")).collect();
    let flat = flat.join("\n");
    hits.extend(finds(not_frag(), &flat).into_iter().map(|m| m.as_str().to_string()));
    for h in hits.iter().take(6) {
        fails.push(format!("antithesis 'not X but Y': \"{}\" (R49-40-NOT_X_Y; AI-tells §1)", head(h.trim(), 90)));
    }
    if hits.len() > 6 {
        fails.push(format!("antithesis: {} more", hits.len() - 6));
    }
    for sen in &sentences {
        let lad = finds(ladder(), sen);
        if lad.len() >= 2 {
            fails.push(format!("Ladder, two clauses in one sentence: \"{}\" (R6-1-LADDER_BAN, Check 18)", head(sen, 100)));
        } else if let Some(l) = lad.first() {
            warns.push(format!("possible Ladder: \"{}\" in \"{}...\" (Check 18: review by reading)", l.as_str(), head(sen, 70)));
        }
    }
    let neg = rx!(r"(?i)\b(?:no|not|never|nothing|none|nor)\b");
    let just = rx!(r"^(?:Just|Only)\b");
    let mut i = 0;
    while i + 2 < sentences.len() {
        let mut j = i;
        while j < sentences.len() && words(&sentences[j]) <= 9 && has(neg, &sentences[j]) {
            j += 1;
        }
        if j - i >= 2 && j < sentences.len() && has(just, &sentences[j]) {
            fails.push(format!("countdown negation: \"{}\" (AI-tells §1)", head(&sentences[i..=j].join(" "), 140)));
            i = j + 1;
        } else {
            i += 1;
        }
    }

    // --- warn-level patterns
    for m in finds(apparatus(), &body) {
        warns.push(format!("faculty as grammatical subject: \"{}\" (R6-2-FACULTY_NEVER_SUBJECT, Check 19)", m.as_str()));
    }
    for p in &prose_paras {
        if p.starts_with('"') {
            continue;
        }
        let ss = split_sentences(p);
        for w in ss.windows(2) {
            let (s, nxt) = (&w[0], &w[1]);
            let q = |x: &str| x.contains(['"', '“', '”']);
            if has(hypophora_q(), s) && !q(s) && !q(nxt) && words(nxt) <= 8 {
                warns.push(format!("hypophora (question answered at once): \"{} {}\" (R49-41-QUESTIONS)", head(s, 70), head(nxt, 40)));
            }
        }
    }
    if let Some(last) = sentences.last() {
        if has(tidy_close(), last) {
            warns.push(format!("tidy summary close: \"{}\" (AI-tells §2; R79-4: chapters and arcs close on a hook, scenes on any concrete close, a pressing question included, turns at his next real decision)", head(last, 80)));
        }
    }

    // --- narration
    let narr = sub(quoted(), &body, " ");
    let narr_sents: Vec<String> = prose_paras.iter().flat_map(|p| split_sentences(&sub(quoted(), p, " "))).filter(|x| !x.trim().is_empty()).collect();
    let narr_plain = sub(italic(), &narr, " ");
    for m in finds(gamer(), &narr_plain) {
        warns.push(format!("gamer slang in narration: \"{}\" in \"...{}...\" (R70-94-GAMER_SLANG; free in a mouth)", m.as_str(), win(&narr_plain, m.start(), m.end(), 50, 30)));
    }
    for m in finds(formula(), &narr_plain) {
        warns.push(format!("web-novel formula in narration: \"{}\" in \"...{}...\" (R70-136-NEW_CHECKS_VERIFY_SCENE; it belongs in a mouth)", m.as_str(), win(&narr_plain, m.start(), m.end(), 50, 30)));
    }
    let n: usize = finds(quoted(), &body).iter().map(|q| finds(formula(), q.as_str()).len()).sum();
    if n > 0 {
        info.push(format!("web-novel formulas in speech: {n} (R70-136-NEW_CHECKS_VERIFY_SCENE; free in a mouth)"));
    }
    for c in italic().captures_iter(body.as_str()).flatten() {
        if LOANWORDS.contains(&c[1].trim_matches(|ch| " .,;:!?".contains(ch)).to_lowercase().as_str()) {
            warns.push(format!("italicised loanword: \"*{}*\" (R70-36-CHECKER_ENFORCES, R49-49-FOREIGN: foreign words appear plain)", &c[1]));
        }
    }
    let mut digits = Vec::new();
    for p in &prose_paras {
        let p = sub(rx!(r"\[[^\]\n]*\]"), &sub(quoted(), p, " "), " ");
        for c in digit().captures_iter(p.as_str()).flatten() {
            let (m, g) = (c.get(0).unwrap(), c.get(1).unwrap());
            let labeled = label_before().find_from_pos(&p[..m.start()], back(&p, m.start(), 40)).ok().flatten().is_some();
            if g.as_str().parse::<u32>().unwrap_or(0) > 100 || labeled {
                continue;
            }
            let after = &p[m.end()..fwd(&p, m.end(), 2)];
            if (m.start() == 0 || p[..m.start()].ends_with('\n')) && (after == ". " || after == ") ") {
                continue;
            }
            digits.push(win(&p, m.start(), m.end(), 25, 15));
        }
    }
    if !digits.is_empty() {
        let shown: Vec<String> = digits.iter().take(4).map(|d| format!("\"...{d}...\"")).collect();
        info.push(format!("digits for numbers up to one hundred in narration: {} (R70-30-NUMBERS_WORDS_DIGITS: words up to one hundred, digits for system figures): {}", digits.len(), shown.join("; ")));
    }
    for m in finds(calendar(), &body) {
        warns.push(format!("Earth calendar word: \"{}\" in \"...{}...\" (R51-08-CALENDAR; use the culture's own span)", m.as_str(), win(&body, m.start(), m.end(), 50, 30)));
    }
    for m in finds(holy_oath(), &body) {
        warns.push(format!("Earth holy swear: \"{}\" in \"...{}...\" (R51-30-HOLY_OATHS; swear by the world's own powers)", m.as_str(), win(&body, m.start(), m.end(), 50, 30)));
    }
    let mut seen: HashSet<String> = HashSet::new();
    for m in finds(slop(), &body) {
        let k = m.as_str().to_lowercase();
        let stock_rx = slop_stock().into_iter().find(|(w, _)| k.contains(w)).map(|(_, r)| r);
        if seen.contains(&k) || stock_rx.is_some_and(|r| !search_around(r, &body, m.start(), m.end(), 40, 40)) {
            continue;
        }
        fails.push(format!("hard-ban word: \"{}\" in \"...{}...\" (R51-10-SLOP_WORDS)", m.as_str(), win(&body, m.start(), m.end(), 50, 30)));
        seen.insert(k);
    }
    let mut spans = Vec::new();
    for m in finds(stock(), &narr) {
        spans.push((m.start(), m.end()));
        let k = m.as_str().to_lowercase();
        if seen.contains(&k) {
            continue;
        }
        fails.push(format!("hard-ban phrase: \"{}\" in \"...{}...\" (R70-35-HARD_BAN_LIST)", m.as_str(), win(&narr, m.start(), m.end(), 50, 30)));
        seen.insert(k);
    }
    for m in finds(stock_loose(), &narr) {
        if !spans.iter().any(|&(a, b)| a < m.end() && m.start() < b) {
            warns.push(format!("near a hard-ban phrase: \"{}\" in \"...{}...\" (R70-36-CHECKER_ENFORCES; read it against R70-35)", m.as_str(), win(&narr, m.start(), m.end(), 50, 30)));
        }
    }

    // --- table rules
    info.push(format!("length {total_words} words (no word count, Isaac 2026-10-30)"));
    let italics = italic().captures_iter(raw).flatten().filter(|c| words(&c[1]) >= 3).count();
    info.push(format!("italic interior beats: {italics} (free, no count, R79-4)"));
    if let Some(last) = prose_paras.last() {
        let end = if o.turn { "a turn stops at his next real decision" } else { "a scene ends on any concrete close, a pressing question included; a chapter or arc on a hook" };
        info.push(format!("last line: \"{}\" ({end}, R79-4-INTERIOR_MEANING_WORLD)", tail(last, 140)));
    }

    // --- readouts and stale devices
    let ro = readouts(&body);
    if ro > 0 {
        info.push(format!("windows: {ro} (R84-1-WINDOWS, R84-2-WINDOW_NUMBERS)"));
    }
    for (name, r) in stale() {
        let hits: Vec<(&String, Match)> = narr_sents.iter().filter_map(|x| first(r, x).map(|m| (x, m))).collect();
        if hits.len() > 1 {
            let (x, m) = &hits[0];
            warns.push(format!("stale device: {name} in {} sentences of narration, past one a scene, first \"...{}...\" (R71-103-COMBAT_CHECKS_VERIFY_SCENE)", hits.len(), &x[back(x, m.end(), 70)..fwd(x, m.end(), 20)]));
        }
    }

    // --- combat density
    if o.combat {
        let sch = o.school.unwrap_or_else(|| school_for(o.culture));
        let srx = school(sch).ok_or_else(|| format!("KeyError: '{sch}'"))?;
        let (h, a) = (finds(srx, raw).len(), finds(anatomy(), raw).len());
        if h == 0 && sch == "blade" {
            warns.push("no blade body/action vocabulary found in a combat scene (R80-4-BLOWS_FIRST, R13-9-VERIFY_CHECKS_22_26, check 22)".into());
        } else if h == 0 && !["japanese", "chinese", "korean"].contains(&sch) {
            warns.push(format!("no {sch} school vocabulary found in a combat scene (R70-136-NEW_CHECKS_VERIFY_SCENE, R80-4-BLOWS_FIRST, check 22)"));
        }
        if a == 0 {
            warns.push("no injury vocabulary, plain or clinical, found in a combat scene (R13-6-ANATOMY_VOCAB, R79-6, check 23)".into());
        }
        let label = if sch == "blade" { "blade body/action terms".to_string() } else { format!("{sch} school terms") };
        info.push(format!("combat density: {h} {label}, {a} anatomy terms"));
        let plain = |p: &str| sub(italic(), &sub(quoted(), p, " "), " ");
        let joined: Vec<String> = prose_paras.iter().map(|p| sub(quoted(), p, " ")).collect();
        let fight_narr = sub(italic(), &joined.join("\n\n"), " ");
        let run_ = finds(running(), &fight_narr);
        if let Some(r0) = run_.first() {
            warns.push(format!("figure in fight narration: {} reserve figures (EU, AU/s, eta), first \"...{}...\"; in a fight, eta is an idea and a proportion in narration, figures live in mouths (R79-6, R81-3)", run_.len(), win(&fight_narr, r0.start(), r0.end(), 50, 10)));
        }
        let mut thin: Vec<(String, Vec<&str>)> = Vec::new();
        for (k, p) in prose_paras.iter().enumerate() {
            let pp = plain(p);
            if !has(strike(), &pp) {
                continue;
            }
            let mut ctx = if k + 1 < prose_paras.len() { format!("{pp} {}", plain(prose_paras[k + 1])) } else { pp.clone() };
            ctx = format!("{pp} {} {ctx}", if k > 0 { plain(prose_paras[k - 1]) } else { String::new() });
            let miss: Vec<&str> = [("tissue", anatomy()), ("body mechanics", mechanics())].into_iter().filter(|(_, r)| !has(r, &ctx)).map(|(n, _)| n).collect();
            if !miss.is_empty() {
                thin.push((pp, miss));
            }
        }
        for (pp, miss) in thin.iter().take(3) {
            warns.push(format!("thin blow? a strike with no {} in \"{}...\" (Blow Card, R80-5, R81-1)", miss.join(" or "), head(&pp.replace('\n', " "), 90)));
        }
        if thin.len() > 3 {
            warns.push(format!("thin blow?: {} more paragraphs", thin.len() - 3));
        }
    }

    // --- explicit mode
    if o.explicit {
        for c in italic().captures_iter(body.as_str()).flatten() {
            if has(mimetic_full(), c[1].trim_matches(|ch| " .,;:!?".contains(ch))) {
                warns.push(format!("italicised mimetic word: \"*{}*\" (R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL: romanised and never italic, R73-41-INTIMACY_CHECKS_VERIFY)", &c[1]));
            }
        }
        let mut seen: HashSet<String> = HashSet::new();
        for m in finds(euphemism(), &narr_plain) {
            if seen.insert(m.as_str().to_lowercase()) {
                fails.push(format!("bed euphemism in narration: \"{}\" in \"...{}...\" (R49-51-EXPLICIT, R73-41-INTIMACY_CHECKS_VERIFY; free in a mouth)", m.as_str(), win(&narr_plain, m.start(), m.end(), 50, 30)));
            }
        }
        let (rx_names, by_key, n_cards) = cards();
        if n_cards == 0 {
            // an empty read looks exactly like a clean pass; the roster alone holds no ages yet
            fails.push(format!("floor guard: read no character cards under {}, so no age can be checked; fix the path before posting (R73-41-INTIMACY_CHECKS_VERIFY, NATALIE.md floor)", CARD_DIRS[0]));
        }
        let mut keys: Vec<String> = rx_names.as_ref().map(|r| finds(r, raw).into_iter().map(|m| m.as_str().to_string()).collect()).unwrap_or_default();
        keys.sort();
        keys.dedup();
        let mut named: BTreeMap<String, Option<i64>> = BTreeMap::new();
        for k in &keys {
            for (n, a) in &by_key[k] {
                named.insert(n.clone(), *a);
            }
        }
        for (n, a) in &named {
            if let Some(a) = a.filter(|a| *a < 18) {
                fails.push(format!("floor guard: {n} is {a} on file, under eighteen, named in an explicit scene (R73-41-INTIMACY_CHECKS_VERIFY, NATALIE.md floor)"));
            }
        }
        let unaged: Vec<&str> = named.iter().filter(|(_, a)| a.is_none()).map(|(n, _)| n.as_str()).collect();
        if !unaged.is_empty() {
            warns.push(format!("floor guard: no age on file for {}; a partner's card or roster entry needs the body's adult age before drafting (R73-41-INTIMACY_CHECKS_VERIFY)", unaged.join(", ")));
        }
        if !named.is_empty() {
            let list: Vec<String> = named.iter().map(|(n, a)| format!("{n} {}", a.map(|x| x.to_string()).unwrap_or("?".into()))).collect();
            info.push(format!("floor guard, named on file: {}", list.join(", ")));
        }
    }
    Ok(Res { fails, warns, info })
}

const ECHO_STOP: &str = "that this with from have were been they them their there then than when what which while would could should about into over under after before again still just only even very more most some such other each every where here your yours down back through upon onto against between without within being does done said says like made make much many said";

/// verify.echoes: one lowercase content word 4+ times inside 60 words of narration.
pub fn echoes(text: &str) -> Vec<String> {
    let (window, times) = (60, 4);
    let stop: HashSet<&str> = ECHO_STOP.split_whitespace().collect();
    let cleaned = sub(quoted(), &strip_md(before_notes(text)), " ");
    let toks: Vec<&str> = finds(rx!(r"[A-Za-z][a-z'’]+"), &cleaned).into_iter().map(|m| m.as_str()).collect();
    let (mut out, mut seen) = (Vec::new(), HashSet::new());
    for (i, w) in toks.iter().enumerate() {
        let islower = w.chars().any(char::is_lowercase) && !w.chars().any(char::is_uppercase);
        if w.chars().count() < 4 || !islower || stop.contains(w) || seen.contains(w) {
            continue;
        }
        let hits = toks[i..(i + window).min(toks.len())].iter().filter(|t| *t == w).count();
        if hits >= times {
            seen.insert(*w);
            let near = toks[i.saturating_sub(4)..(i + 6).min(toks.len())].join(" ");
            out.push(format!("word echo: \"{w}\" {hits}× in {window} words, near \"{near}\" (editor's pass; keep it if the echo is deliberate)"));
        }
    }
    out
}

pub fn report(r: &Res) -> String {
    let mut out = vec![format!("{}: {} fail, {} warn", if r.fails.is_empty() { "PASS" } else { "FAIL" }, r.fails.len(), r.warns.len())];
    out.extend(r.fails.iter().map(|f| format!("  FAIL  {f}")));
    out.extend(r.warns.iter().map(|w| format!("  WARN  {w}")));
    out.extend(r.info.iter().map(|i| format!("  info  {i}")));
    out.join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn ages() {
        assert_eq!(card_age("Late twenties"), Some(20));
        assert_eq!(card_age("~50"), Some(50));
        assert_eq!(card_age("Roughly 1,600 years"), Some(1600));
        assert_eq!(card_age("400 (soul)"), None);
        assert_eq!(card_age("body 16, soul 300"), Some(16));
        assert_eq!(card_age("twenty-three"), Some(23));
        assert_eq!(card_age("Three years older than his brother"), None);
    }
    #[test]
    fn bans() {
        let r = run("He looked at her — and it was not just anger, but grief. The colour of it.", &Opts::default()).unwrap();
        let s = report(&r);
        assert!(s.contains("em dashes: 1") && s.contains("colour -> color") && s.contains("antithesis"), "{s}");
    }
}
