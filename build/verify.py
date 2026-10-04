#!/usr/bin/env python3
"""Mechanical prose checks derived from the rule index and the AI-tells guide.

  python build/verify.py draft.md [--combat] [--school blade|japanese|chinese|korean|percussion]
                         [--culture Kharven] [--band standard|set-piece|conversational]

Every check names the rule it enforces. FAIL is a rule with a hard number or an
outright ban; WARN is a pattern that needs a human read (the FID carve-out, the
whose-vocabulary test). Nothing here judges quality; it counts.
"""
import argparse
import re
import statistics
import sys
from pathlib import Path

EM_DASH = re.compile(r"[—–]|(?<!-)--(?!-)")
ANTITHESIS = [
    re.compile(r"\b(?:not|isn['’]t|wasn['’]t|is not|was not|aren['’]t|weren['’]t)\s+(?:just|merely|simply|only|so much)\b[^.!?\n]{0,80}?\b(?:but|it['’]s|it is|as|rather)\b", re.I),
    re.compile(r"\b(?:this|that|it|which|he|she)\s+(?:is|was)\s+(?:less|more)\s+(?:a |an )?\w+\s+than\s+(?:a |an |it was |it is )?\w+", re.I),
    re.compile(r"\b(?:it|this|that)\s+(?:is|was|isn['’]t|wasn['’]t)\s+not\s+(?:a |an |the )?[\w\s]{1,30}?[,;]\s*(?:but|it['’]s|it was|it is)\b", re.I),
]
# R49-40, form 4b: 'Not regret. Recognition.', a Not-fragment corrected by the fragment after it.
# The second is one word, or a determiner and up to two words; a second negation is not a correction.
NOT_FRAG = re.compile(r"(?:^|(?<=[.!?] )|(?<=[.!?][”\"*] )|(?<=[*“\"]))Not(?: [\w'’-]+){1,3}[.!] (?!(?:Not|No|Never|Nor|Nothing|None|Nobody|Neither|Nowhere|Yes|Please)\b)"
                      r"(?:[A-Z][\w'’-]*|(?:A|An|The|His|Her|Their|Its|One)(?: [\w'’-]+){1,2})[.!](?=\s|$|[”\"’*])", re.M)
FRAGMENT = re.compile(r"(?:^|(?<=[.!?]\s))(?:Not|Never|And|Only|Just)\s+\w+(?:\s+\w+)?[.!]", re.M)
LADDER = re.compile(r"\b(?:was|is|became|meant)\s+[a-z]+\s+and\s+the\s+[a-z]+\s+(?:was|is|became|meant)\b", re.I)
FACULTIES = r"(?:Cymorath|Kamigan|Shingan|Meigan|Reigan|Tengan|Ketsumy[oō]gan|Crown Eye|Seeing|Ruling Sight|Revealing Sight|Spirit Sight|Sky Sight)"
APPARATUS_SUBJECT = re.compile(r"\b(?:his|her|the|their)\s+" + FACULTIES + r"\s+(?:saw|read|mapped|noted|caught|found|registered|filed|marked|tracked|perceived|counted|watched|traced|classified|flagged|told|reported)\b")
GLOSS = re.compile(r"\b(?:which meant|which was to say|meaning that|in other words|that is to say|which is to say|what that meant was)\b", re.I)
SIGNPOST = re.compile(r"\b(?:he|she|they|[A-Z][a-z]+)\s+(?:felt|was|were)\s+(?:a\s+(?:wave|surge|flicker|pang|rush|stab)\s+of\s+)?(?:afraid|fear|angry|anger|relief|relieved|dread|terror|terrified|joy|sad|sadness|grief|ashamed|shame|guilt|guilty|nervous|anxious|anxiety|hopeful|hope|despair)\b", re.I)
SIMILE = re.compile(r"\b(?:like an?|like the|as if|as though)\b", re.I)
TIDY_CLOSE = re.compile(r"^(?:Ultimately|In the end|And so|Finally|At last|Perhaps that|Maybe that)\b", re.I)
HYPOPHORA_Q = re.compile(r"\?\s*$")
# R49-21: reification has no count and 'never at the beat' is a read, so no check here.
# R49-17: '-ing' openers and 'As he ..., ' simultaneous action are AI tells, counted.
ING_OPENER = re.compile(r"^(?!(?:During|Nothing|Something|Everything|Anything|King|Morning|Evening|Spring|Thing|String|Wing|Ring|Sing|Bring)\b)[A-Z][a-z]{2,}ing\b[^,.!?]{0,80},")
AS_OPENER = re.compile(r"^As\s+(?:he|she|they|I|we|it|(?!if\b|though\b)[A-Z][a-z]+)\b[^,.!?]{0,80},")
# R49-42: filter verbs, warned above FILTER_RATE per 1,000 narration words. Isaac set no
# number; 5 is the checker's call, raise or lower it here.
FILTER = re.compile(r"\b(?:he|she|they|I|we|(?!The\b|A\b|An\b|It\b)[A-Z][a-z]+)\s+(?:saw|heard|felt|noticed|watched|realised|realized|sensed|smelled|smelt|tasted|wondered|could see|could hear|could feel)\b")
FILTER_RATE = 5.0
# R48-13, R49-44: modern words are free in speech, flagged in narration. Real science and
# anatomy terms are exempt (R49-45): adrenaline, cortisol and the like stay off this list.
# R51-03 slang (okay, OK, vibe, awesome, cool) and R51-04 pop-psych (triggered, toxic, closure,
# mindset, boundaries); R51-04 keeps anxiety and stress, so they and trauma are off the list.
# 'cool' and 'closure' have plain senses too; the WARN asks for a read. Add words here.
# R51-05: tech and office words (deadline, feedback, 'on the main') are legal when the POV's
# culture has the thing; a regex cannot know the POV's culture, so they are not listed.
# 'weekend' lives in CALENDAR below, which covers narration and speech.
MODERN = re.compile(r"\b(?:okay|OK|vibes?|awesome|cool|teenagers?|triggered|toxic|closure|mindset|boundaries)\b", re.I)
# R51-08: Earth day and month names never appear, in narration or speech. Case-sensitive;
# 'May' and 'March' only when capitalised after a lowercase word, so sentence-initial
# 'May he...' and the verb 'march' pass.
CALENDAR = re.compile(r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|April|June|July|August|September|October|November|December|[Ww]eekends?)\b|(?<=[a-z,;] )(?:May|March)\b")
# R51-30: Earth religious swears are replaced in-world; warned in narration and speech.
HOLY_OATH = re.compile(r"\b(?:(?i:god\s*damn\w*|go to hell|for god['’]s sake)|Christ|Jesus)\b")
# R51-10: the hard-ban list, FAIL at first use, narration and dialogue.
SLOP = re.compile(r"\b(?:tapestr(?:y|ies)|testaments?|palpabl[ey]|viscerall?y?|symphony of|a dance of|whispers? of|orbs|ministrations"
                  r"|electric\w*\W+(?:\w+\W+){0,3}?touch\w*|touch\w*\W+(?:\w+\W+){0,3}?electric\w*|velvety? voice"
                  r"|shiver\w* down (?:his|her|their|my|your) spine|breath (?:he|she|they|I) didn['’]t know (?:he|she|they|I) (?:was|were) holding"
                  r"|coppery tang|smell of ozone)\b", re.I)
# R70-35 (VB12 D): three items trimmed to their stock sense; only the stock form fails ('a testament
# to', 'visceral' off the anatomy, orbs for eyes), so a will, the visceral pleura and orbs that are
# lamps, regalia or worked spheres pass.
SLOP_STOCK = {
    "testament": re.compile(r"\btestaments? to\b", re.I),
    "visceral": re.compile(r"\bviscerally\b|\bvisceral\b(?! (?:pleura|peritoneum|pericardium|fat|organs?|layers?|surfaces?|nerves?|afferents?|pain|branch\w*|arter\w*|lymph\w*|cavity|muscle)\b)", re.I),
    "orbs": re.compile(r"\b(?:his|her|their|my|your) (?:[\w-]+ ){0,2}orbs\b|\borbs (?:of (?:his|her|their|my|your) (?:eyes|breasts|bosom)|(?:\w+ )?(?:widen|narrow|blink|squint|flick|fixed on|met (?:his|her|their|mine|yours)\b))", re.I),
}
# R70-35 (VB12 A-C): cultivation-translation, Western fantasy and LitRPG stock join the hard-ban
# list, FAIL at first use in narration only (speech formulas are DL2's). R70-36 (VB13 C): looser
# variants of the same phrases WARN for a read.
_P = r"(?:his|her|their|my|your|its)"
STOCK = re.compile(r"\bqi (?:surge[sd]?|surging)\b|\ba cold glint flash(?:ed|es)?\b|\bsuck(?:ed|s|ing)? in a cold breath\b|\bkilling intent (?:surge[sd]?|surging)\b"
                   r"|\bthe steel (?:sang|sings|singing)\b|\ba grim smile\b|\b" + _P + r" blood (?:ran|runs|running) cold\b|\bevery fib(?:re|er) of " + _P + r" being\b|\bdarkness (?:gathered|gathers|gathering)\b"
                   r"|\bpower surged through (?:him|her|them|me|you)\b|\bstronger than ever\b|\ba wave of power\b|\b" + _P + r" stats (?:soared|soar|soars|soaring)\b", re.I)
STOCK_LOOSE = re.compile(r"\bqi (?:rose|flared|roared|boiled|churned|exploded|erupted)\b|\bcold (?:glint|gleam|light) (?:flash|flicker)\w*|\b(?:drew|took|sucked) (?:in )?a (?:cold|chill) breath\b|\bkilling intent\b"
                         r"|\bsteel (?:sang|sings|singing)\b|\bgrim(?:ly)? smil\w+|\bsmiled grimly\b|\bblood (?:ran|runs|turned|went) (?:cold|to ice)\b|\bfib(?:re|er)s? of " + _P + r" being\b|\bdarkness (?:pooled|coiled|swirled|thickened)\b"
                         r"|\b(?:power|strength|energy) (?:surged|surging|flooded|coursed) through\b|\bsurge of (?:power|strength|energy)\b|\bwave of (?:strength|energy)\b|\bstats? (?:soared|rose|climbed|jumped|skyrocketed)\b", re.I)
# R70-136 (ME2 D): translated web-novel formulas WARN in narration, info in speech, where DL2 keeps
# them. 'this one' only as the self-address formula; the plain pronoun is everywhere in the archive.
FORMULA = re.compile(r"\b(?:(?:you )?court(?:s|ed|ing)? death|seek(?:s|ing)? death|sought death|this junior|this old man|los(?:e|es|ing|t) face"
                     r"|this one (?:humbly|dares|begs|greets|thanks|apologi[sz]es|is grateful|is honou?red|offers|requests|will obey))\b", re.I)
# R70-94 (LR16): gamer slang is free in a mouth and watched in narration: the four words it names,
# plus three with no period sense. buff, tank, grind and proc are left out (leather, a Draw Age
# tank, the mill).
GAMER = re.compile(r"\b(?:min-?max\w*|dump stats?|aggro|cool-?downs?|debuff\w*|nerf\w*|DPS)\b", re.I)
# R70-36 (VB13 D), R49-49: an italicised loanword WARNs. TODO R70-36: add the Words entries of
# desktop/inventories/*.md once the Inventories carry them (none do yet).
LOANWORDS = {"qi", "gi", "ki", "dao", "danjeon", "dantian"}
# R70-30 (VB7): words up to one hundred in narration; digits for big exact counts, system figures
# (Level, EU, AU/s) and sourced figures with a unit (12%, 3 m, 40 Hz). Decimals, times, grouped
# thousands and bracketed readouts are skipped, and so is a numeral after a capitalised label
# (Level 7, Grade: 3, Vials 1, 2 and 4), the labels' own style.
DIGIT = re.compile(r"(?<![\w.,:/-])(\d{1,3})(?![\w.,:/%-]?\d)(?!\s?(?:%|°|(?:EU|AU|Hz|kHz|kg|g|km|cm|mm|m|m/s|s|ms|J|kJ|W|kW|N|Pa|kPa|K|lbs?|ft)\b))")
LABEL_BEFORE = re.compile(r"\b[A-Z][A-Za-z]*[.:]?[ \t]+(?:\d{1,3},?[ \t]+(?:and[ \t]+|or[ \t]+)?)*$")
# R70-80 (LR3), R70-136 (ME2 B): a readout set off as its own line in square brackets is left out
# of the rhythm counts and the word count, as verse set as a '>' block (the verse marker, R70-64)
# and '|' tables already are; the dash and hard-ban checks still read both.
READOUT = re.compile(r"(?m)^[ \t]*\[[^\]\n]+\][ \t]*(?:\n|$)")
QUOTED = re.compile(r"[\"“][^\"“”\n]*[\"”]")
ITALIC = re.compile(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)")
HEMA = re.compile(r"\b(?:Vor|Nach|Indes|Zornhau|Absetzen|Durchwechseln|Winden|Krumphau|Zwerchhau|Schielhau|Scheitelhau|Mutieren|Duplieren|bind|measure|half-sword|halfsword|pommel|guard|ward|thrust|cut|tempo|feint|parry|riposte|void|cross|edge|flat|crossguard|quillon|point|counter-cut)\b")
ANATOMY = re.compile(r"\b(?:femoral|carotid|clavicle|radius|ulna|humerus|tibia|fibula|patella|scapula|sternum|rib|ribs|vertebra|spine|jugular|subclavian|brachial|aorta|lung|liver|kidney|spleen|diaphragm|tendon|ligament|cartilage|orbit|mandible|maxilla|skull|trachea|larynx|hypovol|haemorrh|hemorrh|shock|Class\s+(?:I|II|III|IV))\b", re.I)
# R70-136 (ME2 A), R70-100 (CB1): --combat warns only when a fight carries none of its school's
# terms. The school comes from --school, or from --culture (Ketsuen and the Japonic houses, R8's
# naming register; the Korean houses; the lineage halls); blade (the HEMA list above) otherwise.
SCHOOLS = {
    "blade": HEMA,
    "japanese": re.compile(r"\b(?:maai|ma-ai|kamae|ch[uū]dan|j[oō]dan|gedan|hass[oō]|waki-?gamae|seme|kiai|zanshin|tsuki|kesa-?giri|kiri-?oroshi|nukitsuke|iai\w*|batt[oō]\w*|n[oō]t[oō]|chiburi"
                           r"|tsuba|kissaki|shinogi|monouchi|hasuji|metsuke|kuzushi|irimi|tenkan|atemi|tai-?sabaki|ashi-?sabaki|suriage|nagashi|kaeshi|(?:sen|go)[ -]no[ -]sen|kote|tachi|katana|wakizashi|tant[oō]|naginata|yari|saya)\b", re.I),
    "chinese": re.compile(r"\b(?:jian|dao|qiang|guandao|fa ?jin|fali|qinna|chin na|chan ?si|silk-reeling|tui ?shou|push-?hands|zhan zhuang|ma ?bu|gong ?bu|horse stance|bow stance|dantian|taolu"
                          r"|sanshou|sanda|liuhe|six harmonies|neijia|waijia|qinggong|dianxue|bagua|xingyi|taiji|tai chi|wing chun|chi sao)\b", re.I),
    "korean": re.compile(r"\b(?:taekky[eo]on|ssireum|satba|geomdo|gumdo|kumdo|haidong|ssangsudo|bonguk ?geom\w*|muye ?dobo ?tongji|hwando|jireugi|makgi|chagi|chigi|gyeorugi|pumsae|poomsae"
                         r"|subak|gwonbeop|kwonbeop|baejigi|woldo)\b", re.I),
    "percussion": re.compile(r"\b(?:jab(?:s|bed|bing)?|cross|hooks?|uppercuts?|haymakers?|overhands?|clinch\w*|southpaw|orthodox|teeps?|plum|body shots?|liver shots?|counterpunch\w*|combinations?"
                             r"|footwork|bob(?:bed|bing)?|weav(?:e|ed|ing)|slip(?:s|ped|ping)?|roundhouse|feints?|guard|pivot\w*|(?:elbow|knee) strikes?|straight (?:right|left)|short (?:right|left))\b", re.I),
}
SCHOOL_CULTURES = {"japanese": ("moto", "yukari", "ketsuen", "shirogane", "kokan", "kōkan", "japon"),
                   "korean": ("mahuo", "hon-guk", "honguk", "korea"),
                   "chinese": ("lineage", "chinese")}
# R70-58 (DD7): the description census, a keyword count in narration for each rotation group the
# range rule pulls from (R70-41, R70-42, R70-43; the heavy groups, bodies, rooms and wounds, need no
# push and are not counted). WARN when a scene of standard length or more touches fewer than the
# lead plus two (R70-40) or one group takes over half the hits. Keyword counts are rough ('seal'
# would catch wax and animal, so it is left out).
# TODO R70-58: extend the signature-item count to every Inventory; their Recurrence lines are prose.
CENSUS_MIN = 3
CENSUS = {g: re.compile(r"\b(?:" + w + r")\b", re.I) for g, w in {
    "land, water and sky": r"hills?|mountains?|ridges?|valleys?|rivers?|streams?|lakes?|seas?|shores?|coasts?|plains?|steppe|moors?|forests?|cliffs?|islands?|marsh\w*|tundra|sky|skies|sun|moon|stars?|aurora|horizon|clouds?|dawn|dusk",
    "seasons and weather": r"snow\w*|rain\w*|wind|winds|frost\w*|fog|mist|storms?|thaw\w*|sleet|hail|blizzards?|drizzle|weather|winter|summer|autumn|spring-?time|seasons?",
    "plants and animals": r"trees?|pines?|birch\w*|cedars?|oaks?|grass\w*|moss|flowers?|blossoms?|leaf|leaves|herbs?|crops?|horses?|dogs?|wol(?:f|ves)|birds?|crows?|hawks?|gulls?|fish|cattle|goats?|sheep|rats?|insects?",
    "architecture": r"walls?|gates?|towers?|roofs?|beams?|rafters?|stairs?|doorways?|arch(?:es|way)?|columns?|courtyards?|vaults?|eaves|lintels?|timbers?|masonry|stonework|thresholds?|ornament\w*",
    "dress and adornment": r"coats?|cloaks?|boots?|sleeves?|collars?|gloves?|mittens?|belts?|hats?|hoods?|robes?|silk|wool|woollen|linen|buttons?|cuffs?|scarf|scarves|shawls?|aprons?|trousers|breeches|waistcoats?|jackets?|hems?|jewel\w*|brooch\w*|necklaces?|earrings?",
    "streets, markets, crowds": r"streets?|alleys?|lanes?|squares?|markets?|crowds?|stalls?|carts?|wagons?|hawkers?|vendors?|haggl\w*|arcades?|traffic|townsfolk|cobbles?|cobbled|passers-?by|throngs?",
    "power on show": r"processions?|precedence|thrones?|dais|heralds?|banners?|courtiers?|retinues?|regalia|sceptres?|crowns?|pageant\w*|ranking boards?|guild ?halls?|executions?|gallows|pillory",
    "households": r"servants?|maids?|housekeepers?|nursemaids?|nursery|chores?|cradles?|grand(?:mother|father|child|children)s?|kitchens?|household\w*|widows?|infants?|bab(?:y|ies)",
    "food and taste": r"bread|broth|meat|stew|rice|tea|wine|ale|beer|soup|cheese|porridge|cakes?|butter|honey|fruit|apples?|barley|milk|windmeat|stonecurd|supper|meals?",
    "rites and festivals": r"prayers?|prayed|rites?|rituals?|festivals?|feasts?|funerals?|shrines?|temples?|altars?|incense|vows?|blessings?|offerings?|priests?|ceremon(?:y|ies)|weddings?|sacrament\w*|death-?house|mourn\w*",
    "music, art and play": r"songs?|singing|sang|music|drums?|flutes?|lutes?|fiddles?|harps?|games?|dice|toys?|danc(?:e|es|ed|ing)|tunes?|melod(?:y|ies)|choir|lullab(?:y|ies)|carvings?|paintings?|theatre|storytellers?",
}.items()}
NOTES = re.compile(r"(?im)^##\s+(?:author[\w-]*\s+)?notes\b")  # '## Notes', '## Author notes', '## Author-facing notes'

KHARVEN_RECURRENCE = {
    "the woodpile / how's your stack": re.compile(r"woodpile|how['’]s your stack|your stack", re.I),
    "the night-stone": re.compile(r"night-?stone", re.I),
    "wet wood": re.compile(r"wet wood", re.I),
    "the Thin Weeks": re.compile(r"thin weeks", re.I),
    "the death-house / the Waiting": re.compile(r"death-?house|\bthe Waiting\b"),
}
# R48-28: a roleplay turn runs about 3,500 words; R48-46: set pieces 5,000+.
BANDS = {"conversational": (2500, 4500), "standard": (2500, 4500), "set-piece": (5000, 10**9)}  # every reply is a full ~3,500-word turn (R49-30)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"“‘'A-Z])", text)
    return [p.strip() for p in parts if p.strip()]


def strip_md(text: str) -> str:
    text = re.sub(r"(?m)^#{1,6}\s+.*$", "", text)
    text = re.sub(r"(?m)^---\s*$", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return text


def paired(sen: str) -> bool:
    """A sentence split by one semicolon into two halves of matched length (R70-19)."""
    halves = [len(h.split()) for h in sen.split(";")]
    return len(halves) == 2 and min(halves) >= 3 and max(halves) <= min(halves) * 1.4


def school_for(culture: str | None) -> str:
    c = (culture or "").lower()
    return next((s for s, keys in SCHOOL_CULTURES.items() if any(k in c for k in keys)), "blade")


def run(text: str, combat: bool = False, culture: str | None = None, band: str = "standard", school: str | None = None) -> dict:
    fails, warns, info = [], [], []
    text = NOTES.split(text, maxsplit=1)[0]  # author notes are not measured
    raw = text
    body = strip_md(text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", READOUT.sub("", body)) if p.strip()]
    prose_paras = [p for p in paragraphs if not p.startswith(">") and not p.startswith("|")]
    sentences = [s for p in prose_paras for s in split_sentences(p)]
    words = [len(s.split()) for s in sentences]
    total_words = sum(words)

    # --- bans --------------------------------------------------------------
    n = len(EM_DASH.findall(raw))
    if n:
        fails.append(f"em dashes: {n} (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)")
    hits = [m.group(0) for rx in ANTITHESIS for m in rx.finditer(body)]
    flat = "\n".join(re.sub(r"\s+", " ", p) for p in re.split(r"\n\s*\n", body))
    hits += [m.group(0) for m in NOT_FRAG.finditer(flat)]
    for h in hits[:6]:
        fails.append(f"antithesis 'not X but Y': \"{h.strip()[:90]}\" (R49-40-NOT_X_Y; AI-tells §1)")
    if len(hits) > 6:
        fails.append(f"antithesis: {len(hits) - 6} more")
    for sen in sentences:
        lad = LADDER.findall(sen)
        if len(lad) >= 2:
            fails.append(f"Ladder, two clauses in one sentence: \"{sen[:100]}\" (R6-1-LADDER_BAN, Check 18)")
        elif lad:
            warns.append(f"possible Ladder: \"{lad[0]}\" in \"{sen[:70]}...\" (Check 18: review by reading)")

    # countdown negation: 2+ consecutive short negated sentences resolving into Just/Only
    neg = re.compile(r"\b(?:no|not|never|nothing|none|nor)\b", re.I)
    i = 0
    while i < len(sentences) - 2:
        j = i
        while j < len(sentences) and len(sentences[j].split()) <= 9 and neg.search(sentences[j]):
            j += 1
        if j - i >= 2 and j < len(sentences) and re.match(r"^(?:Just|Only)\b", sentences[j]):
            fails.append(f"countdown negation: \"{' '.join(sentences[i:j + 1])[:140]}\" (AI-tells §1)")
            i = j + 1
        else:
            i += 1
    frags = FRAGMENT.findall(body)
    if len(frags) >= 3:
        warns.append(f"manufactured fragment emphasis: {len(frags)} short Not/Never/And/Only fragments (AI-tells §1)")

    # --- warn-level patterns -----------------------------------------------
    for m in APPARATUS_SUBJECT.finditer(body):
        warns.append(f"faculty as grammatical subject: \"{m.group(0)}\" (R6-2-FACULTY_NEVER_SUBJECT, Check 19)")
    for m in GLOSS.finditer(body):
        s = body[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")
        warns.append(f"gloss watch: \"...{s.strip()}...\" (R4-13-ZERO_BUDGET, Check 15; keep only if it is the POV's own idiom)")
    for m in SIGNPOST.finditer(body):
        warns.append(f"emotional signposting: \"{m.group(0)}\" (AI-tells §4)")
    q = [s for p in prose_paras if not p.startswith("\"") for s in split_sentences(p) if HYPOPHORA_Q.search(s) and not re.search(r"[\"“”]", s)]
    for s in q:
        warns.append(f"question in narration (hypophora?): \"{s[:80]}\" (R49-41-QUESTIONS)")
    for p in prose_paras:
        sm = SIMILE.findall(p)
        if len(sm) >= 2:
            warns.append(f"competing similes in one paragraph ({len(sm)}): \"{p[:70]}...\" (R49-18-SIMILE_COUNT: cut one if they share a beat)")
    if sentences and TIDY_CLOSE.match(sentences[-1]):
        warns.append(f"tidy summary close: \"{sentences[-1][:80]}\" (AI-tells §2; WOTR scenes end on physical action)")

    # --- openers, filter verbs, modern words (narration only) -------------
    narr = QUOTED.sub(" ", body)
    narr_sents = [x for p in prose_paras for x in split_sentences(QUOTED.sub(" ", p)) if x.strip()]
    narr_words = len(narr.split()) or 1
    openers = [x for x in narr_sents if ING_OPENER.match(x) or AS_OPENER.match(x)]
    if len(openers) >= 3:
        warns.append(f"'-ing' / 'As he ...,' openers: {len(openers)} (R49-17-OPENERS, AI tell): "
                     + "; ".join(f"\"{x[:50]}\"" for x in openers[:5]))
    elif openers:
        info.append(f"'-ing' / 'As he ...,' openers: {len(openers)} (R49-17-OPENERS warns at 3)")
    fv = FILTER.findall(narr)
    rate = len(fv) * 1000 / narr_words
    if rate > FILTER_RATE:
        warns.append(f"filter verbs: {len(fv)} ({rate:.1f} per 1,000 narration words, warn above {FILTER_RATE:g}) (R49-42-FILTER_VERBS)")
    elif fv:
        info.append(f"filter verbs: {len(fv)} ({rate:.1f} per 1,000 words)")
    # R70-37 (IN1): italic thought may carry what the POV would say aloud, so it leaves the
    # modern-word, gamer-slang and formula watches with speech.
    narr_plain = ITALIC.sub(" ", narr)
    for m in MODERN.finditer(narr_plain):
        s_ = narr_plain[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        warns.append(f"modern word in narration: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R48-13-PERIOD_FEEL, R49-44-MODERN_FLAGS; science sense is exempt, R49-45)")
    for m in GAMER.finditer(narr_plain):
        s_ = narr_plain[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        warns.append(f"gamer slang in narration: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R70-94-GAMER_SLANG; free in a mouth)")
    for m in FORMULA.finditer(narr_plain):
        s_ = narr_plain[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        warns.append(f"web-novel formula in narration: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R70-136-NEW_CHECKS_VERIFY_SCENE; it belongs in a mouth)")
    n = sum(len(FORMULA.findall(q)) for q in QUOTED.findall(body))
    if n:
        info.append(f"web-novel formulas in speech: {n} (R70-136-NEW_CHECKS_VERIFY_SCENE; free in a mouth)")
    for m in ITALIC.finditer(body):
        if m.group(1).strip(" .,;:!?").lower() in LOANWORDS:
            warns.append(f"italicised loanword: \"*{m.group(1)}*\" (R70-36-CHECKER_ENFORCES, R49-49-FOREIGN: foreign words appear plain)")
    digits = []
    for p in prose_paras:
        p = re.sub(r"\[[^\]\n]*\]", " ", QUOTED.sub(" ", p))
        for m in DIGIT.finditer(p):
            if int(m.group(1)) > 100 or LABEL_BEFORE.search(p, max(0, m.start() - 40), m.start()):
                continue
            if (m.start() == 0 or p[m.start() - 1] == "\n") and p[m.end():m.end() + 2] in (". ", ") "):
                continue  # a numbered list item
            digits.append(p[max(0, m.start() - 25):m.end() + 15].replace("\n", " ").strip())
    if digits:
        warns.append(f"digits for numbers up to one hundred in narration: {len(digits)} (R70-30-NUMBERS_WORDS_DIGITS: words up to one hundred, digits for system figures): "
                     + "; ".join(f"\"...{d}...\"" for d in digits[:4]))
    # R51-34: in-world documents take the modern-word list like narration. verify.py has no
    # flag for 'this is a document'; a document checked as its own file, or set as a > block,
    # is narration here already. A document quoted inside speech marks is stripped with speech.
    for m in CALENDAR.finditer(body):
        s_ = body[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        warns.append(f"Earth calendar word: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R51-08-CALENDAR; use the culture's own span)")
    for m in HOLY_OATH.finditer(body):
        s_ = body[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        warns.append(f"Earth holy swear: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R51-30-HOLY_OATHS; swear by the world's own powers)")
    seen = set()
    for m in SLOP.finditer(body):
        k = m.group(0).lower()
        stock = next((rx for w, rx in SLOP_STOCK.items() if w in k), None)
        if k in seen or (stock and not stock.search(body, max(0, m.start() - 40), m.end() + 40)):
            continue
        seen.add(k)
        s_ = body[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        fails.append(f"hard-ban word: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R51-10-SLOP_WORDS)")
    spans = []
    for m in STOCK.finditer(narr):
        spans.append(m.span())
        k = m.group(0).lower()
        if k in seen:
            continue
        seen.add(k)
        s_ = narr[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        fails.append(f"hard-ban phrase: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R70-35-HARD_BAN_LIST)")
    for m in STOCK_LOOSE.finditer(narr):
        if not any(a < m.end() and m.start() < b for a, b in spans):
            s_ = narr[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
            warns.append(f"near a hard-ban phrase: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R70-36-CHECKER_ENFORCES; read it against R70-35)")

    # --- descent / variance (R4-14, Check 16) ------------------------------
    if len(words) >= 6:
        # R70-19 (RH1 D), set pieces only: once per scene, a long cumulative sentence (three or more
        # 'and') that would make the third in a chain is let past the chain ceiling; a semicolon-split
        # matched pair is exempt from the run rule.
        sp = band == "set-piece"
        pairs = {i for i, s in enumerate(sentences) if sp and paired(s)}
        if pairs:
            info.append(f"matched semicolon pairs exempt from the run rule: {len(pairs)} (R70-19-PAIRED_CUMULATIVE_SENTENCES)")
        chain, licence = [], sp
        for i, w in enumerate(words):
            chain = chain + [i] if w > 25 else []
            if len(chain) == 3:
                cum = next((j for j in chain if licence and len(re.findall(r"\band\b", sentences[j], re.I)) >= 3), None)
                if cum is None:
                    fails.append("three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)")
                    break
                licence = False
                chain.remove(cum)
                info.append(f"cumulative sentence let past the chain ceiling once: \"{sentences[cum][:80]}...\" (R70-19-PAIRED_CUMULATIVE_SENTENCES)")
        flat_runs = 0
        for i in range(len(words) - 2):
            if pairs & {i, i + 1, i + 2}:
                continue
            a, b, c = words[i:i + 3]
            lo, hi = min(a, b, c), max(a, b, c)
            if lo >= 6 and hi <= lo * 1.4:
                flat_runs += 1
        if flat_runs >= 4:
            fails.append(f"flat runs: {flat_runs} stretches of three sentences within 40% of each other (R4-14-RUN_RULE)")
        elif flat_runs:
            info.append(f"flat runs: {flat_runs} (R4-14-RUN_RULE fails at 4)")
        short_share = sum(1 for w in words if w < 8) / len(words)
        if short_share < 0.10:
            fails.append(f"sentences under 8 words: {short_share:.0%} of scene, floor is 18% (R4-14-HARD_CEILINGS)")
        elif short_share < 0.18:
            warns.append(f"sentences under 8 words: {short_share:.0%}, floor is 18% (R4-14-HARD_CEILINGS)")
        lll = 0
        for p in prose_paras:
            ws = [len(s.split()) for s in split_sentences(p)]
            if len(ws) >= 3 and all(w > 18 for w in ws[-3:]):
                lll += 1
        if lll:
            warns.append(f"paragraphs closing on three sentences over 18 words: {lll} (R4-14-HARD_CEILINGS says 0)")
        cv = statistics.pstdev(words) / statistics.mean(words)
        if cv < 0.50:
            warns.append(f"sentence-length CV {cv:.2f}: under 0.50 is the strongest tell; target 0.80 (R49-13-VARIANCE)")
        info.append(f"sentence length: mean {statistics.mean(words):.1f} words, CV {cv:.2f} (target 0.80, R49-13-VARIANCE)")
        pl = [len(p.split()) for p in prose_paras]
        if len(pl) >= 4:
            pcv = statistics.pstdev(pl) / statistics.mean(pl)
            info.append(f"paragraph length: mean {statistics.mean(pl):.0f} words, CV {pcv:.2f}")
            if pcv < 0.35:
                warns.append("paragraphs are uniform blocks (AI-tells §2: break deliberately)")

    # --- table rules ---------------------------------------------------------
    lo, hi = BANDS.get(band, BANDS["standard"])
    if total_words < lo or total_words > hi:
        warns.append(f"length {total_words} words, outside the {band} band {lo}–{hi if hi < 10**9 else '∞'} (Table Rule 2)")
    else:
        info.append(f"length {total_words} words ({band} band)")
    italics = [m.group(1) for m in ITALIC.finditer(raw) if len(m.group(1).split()) >= 3]
    info.append(f"italic interior beats: {len(italics)} (Table Rule 10: one per named NPC per scene)")
    prose_narr = "\n\n".join(QUOTED.sub(" ", p) for p in prose_paras)
    census = sorted(((len(rx.findall(prose_narr)), g) for g, rx in CENSUS.items()), reverse=True)
    touched = [(n, g) for n, g in census if n]
    total = sum(n for n, _ in touched)
    info.append("description census: " + (", ".join(f"{g} {n}" for n, g in touched) or "nothing")
                + f"; untouched: {', '.join(g for n, g in census if not n) or 'none'} (R70-58-CHECKING_RANGE)")
    if total_words >= BANDS["standard"][0]:
        if len(touched) < CENSUS_MIN:
            warns.append(f"description touches {len(touched)} subject groups, fewer than {CENSUS_MIN} (R70-58-CHECKING_RANGE)")
        elif touched[0][0] * 2 > total:
            warns.append(f"description census: {touched[0][1]} takes {touched[0][0]} of {total} hits, over half (R70-58-CHECKING_RANGE)")
    if prose_paras:
        info.append(f"last line: \"{prose_paras[-1][-140:]}\" (must end on physical action, an NPC line, or a thing he can now see)")

    # --- culture recurrence (R6-9) -----------------------------------------
    if culture and culture.lower() == "kharven":
        present = [k for k, rx in KHARVEN_RECURRENCE.items() if rx.search(raw)]
        if len(present) < 2:
            warns.append(f"Kharven recurrence: {len(present)} of the five signature items in this text ({', '.join(present) or 'none'}); two per session, not per turn (R49-54-KHARVEN)")
        else:
            info.append(f"Kharven recurrence: {', '.join(present)}")

    # --- combat density (R13-9 checks 22-23, warn) --------------------------
    if combat:
        school = school or school_for(culture)
        h = len(SCHOOLS[school].findall(raw)); a = len(ANATOMY.findall(raw))
        if h == 0:
            warns.append(f"no {school} school vocabulary found in a combat scene (R70-136-NEW_CHECKS_VERIFY_SCENE, R70-100-MARTIAL_VOCABULARY_NAMES_MOVES, R13-6-HEMA_VOCAB, check 22)")
        if a == 0:
            warns.append("no anatomical/injury vocabulary found in a combat scene (R13-6-ANATOMY_VOCAB, check 23)")
        info.append(f"combat density: {h} {school} school terms, {a} anatomy terms")

    return {"fails": fails, "warns": warns, "info": info}


ECHO_STOP = set("""that this with from have were been they them their there then than when what which while would could should about into over under after before again still just only even very more most some such other each every where here your yours down back through upon onto against between without within being does done said says like made make much many said""".split())


def echoes(text: str, window: int = 60, times: int = 4) -> list[str]:
    """Word echoes in narration (the copy editor's pass, no rule id): one lowercase
    content word 4+ times inside 60 words. Speech and capitalised names are skipped."""
    text = NOTES.split(text, maxsplit=1)[0]
    toks = re.findall(r"[A-Za-z][a-z'’]+", QUOTED.sub(" ", strip_md(text)))
    out, seen = [], set()
    for i, w in enumerate(toks):
        if len(w) < 4 or not w.islower() or w in ECHO_STOP or w in seen:
            continue
        hits = [j for j in range(i, min(i + window, len(toks))) if toks[j] == w]
        if len(hits) >= times:
            seen.add(w)
            out.append(f"word echo: \"{w}\" {len(hits)}× in {window} words, near \"{' '.join(toks[max(0, i - 4):i + 6])}\" (editor's pass; keep it if the echo is deliberate)")
    return out


def report(res: dict) -> str:
    out = []
    out.append(f"{'FAIL' if res['fails'] else 'PASS'}: {len(res['fails'])} fail, {len(res['warns'])} warn")
    for f in res["fails"]:
        out.append(f"  FAIL  {f}")
    for w in res["warns"]:
        out.append(f"  WARN  {w}")
    for i in res["info"]:
        out.append(f"  info  {i}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--combat", action="store_true")
    ap.add_argument("--school", choices=list(SCHOOLS), help="combat school for --combat (default: from --culture, else blade)")
    ap.add_argument("--culture")
    ap.add_argument("--band", default="standard", choices=list(BANDS))
    ap.add_argument("--echoes", action="store_true", help="also warn on word echoes (book chapters)")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    text = Path(a.file).read_text(encoding="utf-8", errors="replace")
    res = run(text, combat=a.combat, culture=a.culture, band=a.band, school=a.school)
    if a.echoes:
        res["warns"] += echoes(text)
    print(report(res))
    return 1 if res["fails"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
