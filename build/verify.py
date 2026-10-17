#!/usr/bin/env python3
"""Mechanical prose checks derived from the rule index and the AI-tells guide.

  python build/verify.py draft.md [--combat] [--school blade|japanese|chinese|korean|percussion|boxing|firearms|kharven]
                         [--culture Kharven] [--band turn|standard|conversational|set-piece|discord] [--turn] [--explicit]

Every check names the rule it enforces. FAIL is a rule with a hard number or an
outright ban; WARN is a pattern that needs a human read (the FID carve-out, the
whose-vocabulary test). Prose carries no statistics (R79-3): no rhythm, sentence-length
or count checks. Nothing here judges quality.
"""
import argparse
import re
import sys
from functools import lru_cache
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
LADDER = re.compile(r"\b(?:was|is|became|meant)\s+[a-z]+\s+and\s+the\s+[a-z]+\s+(?:was|is|became|meant)\b", re.I)
FACULTIES = r"(?:Cymorath|Kamigan|Shingan|Meigan|Reigan|Tengan|Ketsumy[oō]gan|Crown Eye|Seeing|Ruling Sight|Revealing Sight|Spirit Sight|Sky Sight)"
APPARATUS_SUBJECT = re.compile(r"\b(?:his|her|the|their)\s+" + FACULTIES + r"\s+(?:saw|read|mapped|noted|caught|found|registered|filed|marked|tracked|perceived|counted|watched|traced|classified|flagged|told|reported)\b")
GLOSS = re.compile(r"\b(?:which meant|which was to say|meaning that|in other words|that is to say|which is to say|what that meant was)\b", re.I)
SIGNPOST = re.compile(r"\b(?:he|she|they|[A-Z][a-z]+)\s+(?:felt|was|were)\s+(?:a\s+(?:wave|surge|flicker|pang|rush|stab)\s+of\s+)?(?:afraid|fear|angry|anger|relief|relieved|dread|terror|terrified|joy|sad|sadness|grief|ashamed|shame|guilt|guilty|nervous|anxious|anxiety|hopeful|hope|despair)\b", re.I)
TIDY_CLOSE = re.compile(r"^(?:Ultimately|In the end|And so|Finally|At last|Perhaps that|Maybe that)\b", re.I)
HYPOPHORA_Q = re.compile(r"\?\s*$")
# R49-21: reification has no count and 'never at the beat' is a read, so no check here.
# R48-13, R49-44: modern words are free in speech, flagged in narration. Real science and
# anatomy terms are exempt (R49-45): adrenaline, cortisol and the like stay off this list.
# R51-03 slang (okay, OK, vibe, awesome, cool) and R51-04 pop-psych (triggered, toxic, closure,
# mindset, boundaries); R51-04 keeps anxiety and stress, so they and trauma are off the list.
# 'cool' and 'closure' have plain senses too; the WARN asks for a read. Add words here.
# R51-05: tech and office words (deadline, feedback, 'on the main') are legal when the POV's
# culture has the thing; a regex cannot know the POV's culture, so they are not listed.
# 'weekend' lives in CALENDAR below, which covers narration and speech.
MODERN = re.compile(r"\b(?:okay|OK|vibes?|awesome|cool|triggered|toxic|closure|mindset|boundaries)\b", re.I)
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
# variants of the same phrases WARN for a read; bare 'killing intent' and 'qi rose/flared/roared' are free (R79-5).
_P = r"(?:his|her|their|my|your|its)"
STOCK = re.compile(r"\bqi (?:surge[sd]?|surging)\b|\ba cold glint flash(?:ed|es)?\b|\bsuck(?:ed|s|ing)? in a cold breath\b|\bkilling intent (?:surge[sd]?|surging)\b"
                   r"|\bthe steel (?:sang|sings|singing)\b|\ba grim smile\b|\b" + _P + r" blood (?:ran|runs|running) cold\b|\bevery fib(?:re|er) of " + _P + r" being\b|\bdarkness (?:gathered|gathers|gathering)\b"
                   r"|\bpower surged through (?:him|her|them|me|you)\b|\bstronger than ever\b|\ba wave of power\b|\b" + _P + r" stats (?:soared|soar|soars|soaring)\b", re.I)
STOCK_LOOSE = re.compile(r"\bqi (?:boiled|churned|exploded|erupted)\b|\bcold (?:glint|gleam|light) (?:flash|flicker)\w*|\b(?:drew|took|sucked) (?:in )?a (?:cold|chill) breath\b"
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
# of the word count, as verse set as a '>' block (the verse marker, R70-64)
# and '|' tables already are; the dash and hard-ban checks still read both.
READOUT = re.compile(r"(?m)^[ \t]*\[[^\]\n]+\][ \t]*(?:\n|$)")
# R79-6: in a fight, figures live in mouths, never narration; a reserve figure in fight narration WARNs.
RUNNING = re.compile(r"\b\d[\d,.]*\s?(?:EU|AU/s)\b|(?:\bEU|\bAU/s|η|\beta)\s*:?\s*\d")
# R71-103 (ME2 B), R70-86: a '>' block is a readout when it carries a figure (Stage II, Level 100,
# Grade ceiling D, 40 EU); a letter, a contract or verse set as '>' carries none. The figure follows
# the label, and a lone letter before a lowercase word is prose ('the band I rode with', 'Grade A steel').
READOUT_FIG = re.compile(r"(?i:\b(?:stage|level|grade|tier|band|rung|reserve|coherence)(?: ceiling)?\b)\s*:?\s*(?:\d[\d,.]*|(?:[IVX]+|[A-FS][+-]?)(?![\w'’])(?!\s+[a-z]))|"
                         + RUNNING.pattern)
QUOTED = re.compile(r"[\"“][^\"“”\n]*[\"”]")
ITALIC = re.compile(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)")
# R77-1 (Isaac, 2026-10-08): European manual jargon is warned on every surface,
# including dialogue. Body/action words remain evidence of the blade grammar.
# Eastern-school terms are free in narration and never required (R78-5, R79-6).
EUROPEAN_FENCING = re.compile(r"\b(?:Vor|Nach|Indes|Zufechten|Krieg|Vom[ -]Tag|Ochs|Pflug|Alber|Zornhau|Absetzen|Durchwechseln|Winden|Krumphau|Zwerchhau|Schielhau|Scheitelhau|Mutieren|Duplieren)\b", re.I)
BLADE_ACTION = re.compile(r"\b(?:bind|half-sword|halfsword|pommel|guard|ward|thrust|cut|feint|parry|riposte|void|cross|edge|flat|crossguard|quillon|point|counter-cut|blade|sword|weight|heel|heels|foot|feet|stance|step(?:s|ped|ping)?)\b", re.I)
# Compatibility for existing consumers; this now counts plain actions, not jargon.
HEMA = BLADE_ACTION
# R79-6: wounds are written plain on the page, so plain part names count beside the clinical ones.
ANATOMY = re.compile(r"\b(?:jaws?|collarbones?|cheekbones?|throats?|windpipe|necks?|guts?|belly|bellies|groin|knees?|kneecaps?|wrists?|elbows?|shoulders?|hips?|thighs?|shins?|ankles?|teeth|tooth|ribcage|bones?|skulls?|arter(?:y|ies)|veins?|femoral|carotid|clavicle|radius|ulna|humerus|tibia|fibula|patella|scapula|sternum|rib|ribs|vertebra|spine|jugular|subclavian|brachial|aorta|lung|liver|kidney|spleen|diaphragm|tendon|ligament|cartilage|orbit|mandible|maxilla|skull|trachea|larynx|hypovol|haemorrh|hemorrh|shock|Class\s+(?:I|II|III|IV))\b", re.I)
# R70-136 (ME2 A), amended by R77-1: --combat checks blade body/action evidence,
# or the existing other-school vocabulary. --school overrides --culture.
SCHOOLS = {
    "blade": BLADE_ACTION,
    "japanese": re.compile(r"\b(?:maai|ma-ai|kamae|ch[uū]dan|j[oō]dan|gedan|hass[oō]|waki-?gamae|seme|kiai|zanshin|tsuki|kesa-?giri|kiri-?oroshi|nukitsuke|iai\w*|batt[oō]\w*|n[oō]t[oō]|chiburi"
                           r"|tsuba|kissaki|shinogi|monouchi|hasuji|metsuke|kuzushi|irimi|tenkan|atemi|tai-?sabaki|ashi-?sabaki|suriage|nagashi|kaeshi|(?:sen|go)[ -]no[ -]sen|kote|tachi|katana|wakizashi|tant[oō]|naginata|yari|saya)\b", re.I),
    "chinese": re.compile(r"\b(?:jian|dao|qiang|guandao|fa ?jin|fali|qinna|chin na|chan ?si|silk-reeling|tui ?shou|push-?hands|zhan zhuang|ma ?bu|gong ?bu|horse stance|bow stance|dantian|taolu"
                          r"|sanshou|sanda|liuhe|six harmonies|neijia|waijia|qinggong|dianxue|bagua|xingyi|taiji|tai chi|wing chun|chi sao)\b", re.I),
    "korean": re.compile(r"\b(?:taekky[eo]on|ssireum|satba|geomdo|gumdo|kumdo|haidong|ssangsudo|bonguk ?geom\w*|muye ?dobo ?tongji|hwando|jireugi|makgi|chagi|chigi|gyeorugi|pumsae|poomsae"
                         r"|subak|gwonbeop|kwonbeop|baejigi|woldo)\b", re.I),
    # R71-103 (ME2 A): Percussion is hammer and haft (R1-1's four moves); the fist words are boxing's.
    # Words common outside a fight ('heads', 'beard', 'round', 'balls of his feet', 'bore') stay off.
    "percussion": re.compile(r"\b(?:hafts?|hammer-?heads?|rims?|boss|shields?|(?:war-?)?hammers?|mauls?|maces?|flails?|clubs?|cudgels?|axe-?beards?|bearded axes?|hook(?:s|ed)?|shov(?:e|es|ed|ing)"
                             r"|rebound\w*|poll|spikes?|(?-i:the (?:Settling|Sweep|Shove|Return)))\b", re.I),
    "boxing": re.compile(r"\b(?:jab(?:s|bed|bing)?|cross|hooks?|uppercuts?|haymakers?|overhands?|clinch\w*|southpaw|orthodox|teeps?|plum|body shots?|liver shots?|counterpunch\w*|combinations?"
                         r"|footwork|bob(?:bed|bing)?|weav(?:e|ed|ing)|slip(?:s|ped|ping)?|roundhouse|feints?|guard|pivot\w*|(?:elbow|knee) strikes?|straight (?:right|left)|short (?:right|left))\b", re.I),
    # R73-41 (ME2 A): 'cock' is the body's word and stays off this list ('cocked the hammer' counts the hammer).
    "firearms": re.compile(r"\b(?:guns?|gun(?:fire|powder|shots?|smoke)|hammers?|percussion caps?|muzzles?|cylinders?|volleys?|reload\w*|ramrods?|rifle[ds]?|revolvers?|flintlocks?|muskets?|pistols?"
                           r"|carbines?|cartridges?|powder|priming|frizzen|breech\w*|barrels?|wad(?:ding)?|trigger\w*|misfire[ds]?)\b", re.I),
    # The Kharven Standing Inventory (desktop/NATALIE.md) and the hall fights in the archive; R71-53's
    # per-culture wrestling words join here once the Inventories carry them.
    "kharven": re.compile(r"\b(?:belt-?wrestl\w*|belts?|grip(?:s|ped|ping)?|forearm|hip-?throws?|throws?|threw|thrown|trip(?:s|ped|ping)?|axes?|hatchets?|spears?|lances?|harpoons?"
                          r"|knife|knives|(?:horse-?)?bows?|arrows?|saddles?|stirrups?|seal-?clubs?)\b", re.I),
}
SCHOOL_CULTURES = {"japanese": ("moto", "yukari", "ketsuen", "shirogane", "kokan", "kōkan", "japon"),
                   "korean": ("mahuo", "hon-guk", "honguk", "korea"),
                   "chinese": ("lineage", "chinese"),
                   "kharven": ("kharven",)}
NOTES = re.compile(r"(?im)^##\s+(?:author[\w-]*\s+)?notes\b")  # '## Notes', '## Author notes', '## Author-facing notes'

# R71-103 (ME2 D): the archive's tired fight devices (the house survey,
# imports/drafts/combat-questionnaire/work/research-house.md), WARN past one a scene, counted by
# sentence of narration. A year ('Year eleven', 'seven hundred and eleven') is not the device, a
# furrow needs heels driven through the ground (a ploughed field passes), and a nosebleed in a
# sentence with a blow in it is a punch's, not an overdraw's.
STALE = {
    "'eleven' as a count": re.compile(r"(?<!Pack )(?<!Part )(?<!Chapter )(?<!Year )(?<!hundred and )(?<!thousand and )\beleven\b(?! hundred| thousand)", re.I),
    "the knock-back furrow": re.compile(r"\b(?:heels?|boots?|feet)\b[^.!?\n]{0,30}?\b(?:plough|plow|dug|dig|goug|carv|tore|tear|scor)\w*[^.!?\n]{0,30}?\b(?:furrows?|grooves?|trench(?:es)?)\b"
                                        r"|\bgoug(?:e|es|ed|ing) (?:\w+ ){0,2}?(?:furrows?|trench(?:es)?)\b", re.I),
    "the overdraw nosebleed": re.compile(r"^(?!.*\b(?:punch\w*|fists?|knuckles?|jab\w*|elbowed|kneed|head-?butt\w*|pommel|kick\w*|slap\w*|hit|struck|broke|broken|smash\w*)\b)"
                                         r".*?(?:\bnose-?bleeds?\b|\b(?:nose|nostrils?)(?:[ -][\w'’]+){0,3}? (?:bled|bleeds?|bleeding|(?:to|run|ran|running) blood)\b"
                                         r"|\bblood\b[^.!?\n]{0,30}?\b(?:from|out of)\b[^.!?\n]{0,15}?\b(?:nose|nostrils?)\b)", re.I),
    "'without deciding to'": re.compile(r"\bwithout (?:(?:his|her|their|my|its) )?(?:having )?(?:deciding|decided) to\b", re.I),
    "'the particular X of Y'": re.compile(r"\bthe particular (?:[\w'’-]+ ){1,3}?of\b", re.I),
}
# R70-133: a reduplicated romanised mimetic word (nuru-nuru, dugeun-dugeun) is kept roman, never italic.
MIMETIC = re.compile(r"\b([a-z]{2,7})-\1\b|\b(?:kyun|dokun)\b", re.I)
# R73-41 (ME2 C), R49-51: bed euphemisms FAIL in narration; a mouth or an italic thought may be coy.
# 'his length' is on, judged a plain euphemism ('his length of rope' passes). --explicit only:
# 'toward manhood' is age and 'of manhood' passes; 'her core' left the list, Core is the Essence term (R79-7).
EUPHEMISM = re.compile(r"\b[Hh]is member\b|\b[Hh]er sex\b|(?<!into )(?<!toward )(?<!towards )(?<!of )\b[Mm]anhood\b|\b[Hh]is length\b(?! of\b)")
# R73-41 (ME2 B), the floor guard: each card or table roster entry named in an explicit scene, by full
# name or a first name no other shares, and the age its Age field (a roster 'age:' line) gives. The
# roster carries no ages yet, so its people WARN as unaged until it does.
WIKI = Path(__file__).resolve().parent.parent / "wiki"
ROSTER = WIKI.parent / "table" / "npcs.yaml"
CARD_DIRS = ("Volume I \u2014 Character Cards", "Characters")
NAME_TITLES = {"The", "Lord", "Lady", "Sir", "Ser", "Dr.", "Commander", "Elder", "Captain"}
AGE_FIELD = re.compile(r"\*\*Age(?:\s*/\s*\w+)?[:.]?\*\*[ \t]*[:.·|]?[ \t]*([^·|\n]+)|(?:^|\.[ \t])Age (\d{1,4})\.", re.M)
_NUM = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = {w: 10 * i for i, w in enumerate("twenty thirty forty fifty sixty seventy eighty ninety".split(), 2)}
AGE_NUM = (r"(?:(\d[\d,]*)(?![\d,])|\b(" + "|".join(_TENS) + r")(?:-(" + "|".join(_NUM[1:10]) + r"))?(?!-)\b|\b(" + "|".join(_NUM) + r")\b)"
           r"(?:\s+(hundred|thousand))?(?!\s+years?\s+(?:older|younger))")

# R79-3 retired the Kharven recurrence check; the items stay for audit.py's recurrence report.
KHARVEN_RECURRENCE = {
    "the woodpile / how's your stack": re.compile(r"woodpile|how['’]s your stack|your stack", re.I),
    "the night-stone": re.compile(r"night-?stone", re.I),
    "wet wood": re.compile(r"wet wood", re.I),
    "the Thin Weeks": re.compile(r"thin weeks", re.I),
    "the death-house / the Waiting": re.compile(r"death-?house|\bthe Waiting\b"),
}
# R79-1: every in-fiction reply runs about 3,500 words, set pieces and Discord included; reported, never warned.
BANDS = dict.fromkeys(("turn", "standard", "conversational", "set-piece", "discord"), 3500)
# R78-3 (Isaac, 2026-10-14): fight abstractions in narration say what the body did instead; --combat only (R79-6).
# The elevated word bank and its density WARN are retired (R78-11, Isaac 2026-10-16).
FIGHT_ABSTRACT = re.compile(r"\b(?:(?:the|his|her|their|its|off the|on the) line\b(?! of| under)|(?:closed?|closing|in|out of|inside|the|his|her) measure\b|tempo\b|vectors?\b|geometry\b|the read\b)", re.I)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"“‘'A-Z])", text)
    return [p.strip() for p in parts if p.strip()]


def strip_md(text: str) -> str:
    text = re.sub(r"(?m)^#{1,6}\s+.*$", "", text)
    text = re.sub(r"(?m)^---\s*$", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return text


def school_for(culture: str | None) -> str:
    c = (culture or "").lower()
    return next((s for s, keys in SCHOOL_CULTURES.items() if any(k in c for k in keys)), "blade")


def card_age(field: str) -> int | None:
    """The body's age from a card's Age field, never a soul's (R73-41, ME2 B): a figure tagged body or
    vessel first ('body 16', '17 (body)'), else a figure leading the field's first sentence ('Late
    twenties', '~50', 'Roughly 1,600 years') when it names no soul. 'Three years older than his
    brother', '400 (soul)', 'Not recorded' and the like give None."""
    v = re.sub(r"ies\b", "y", field.replace("*", "").split(". ")[0].lower())
    m = (re.search(r"\b(?:body|vessel)\W+(?:age\W+)?" + AGE_NUM, v) or re.search(AGE_NUM + r"\W+(?:body|vessel)\b", v)
         or "soul" not in v and re.match(r"(?:[\s~(-]|\b(?:about|around|roughly|nearly|apparently|appears|looks|indeterminate|early|mid|late)\b)*" + AGE_NUM, v))
    if not m:
        return None
    d, tens, unit, small, mult = m.groups()
    n = int(d.replace(",", "")) if d else _TENS[tens] + _NUM.index(unit or "zero") if tens else _NUM.index(small)
    return n * {"hundred": 100, "thousand": 1000}.get(mult, 1)


@lru_cache(maxsize=None)
def cards() -> tuple:
    """(regex, {name or first name: [(name, age)]}) over the character cards and the table roster, read once a run."""
    found = []
    for d in CARD_DIRS:
        for p in sorted((WIKI / d).glob("*.md")):
            name = re.split(r" · | \u2014 | \(|, ", p.stem)[0].strip()
            if name.split()[0] == "Volume":
                continue
            m = AGE_FIELD.search(p.read_text(encoding="utf-8", errors="replace"))
            found.append((name, None if not m else card_age(m.group(1)) if m.group(1) is not None else int(m.group(2))))
    for e in re.split(r"(?m)^- ", ROSTER.read_text(encoding="utf-8")) if ROSTER.exists() else ():
        if n := re.search(r"(?m)^ *name: *['\"]?(.+?)['\"]? *$", e):
            m = re.search(r"(?m)^ *age: *(.+)$", e)
            found.append((n.group(1), m and card_age(m.group(1))))
    by_key, firsts = {}, {}
    for name, age in found:
        by_key.setdefault(name, []).append((name, age))
        firsts.setdefault(name.split()[0], set()).add(name)
    for f, names in firsts.items():
        if len(names) == 1 and len(f) > 2 and f not in NAME_TITLES and f not in by_key:
            by_key[f] = by_key[next(iter(names))]
    rx = re.compile(r"\b(?:" + "|".join(map(re.escape, sorted(by_key, key=len, reverse=True))) + r")\b") if by_key else None
    return rx, by_key


def readouts(body: str) -> list[str]:
    """One paragraph per readout (R70-86): a whole-line bracket line or a '>' block with a figure in
    it; readout lines split only by blank lines are one readout."""
    out, prev = [], False
    for p in re.split(r"\n\s*\n", body):
        lines = [x for x in p.split("\n") if x.strip()]
        quote = [x.lstrip().startswith(">") for x in lines]
        j = 0
        while j < len(lines):
            e = j + 1
            while quote[j] and e < len(lines) and quote[e]:
                e += 1
            ro = bool(READOUT_FIG.search("\n".join(lines[j:e]))) if quote[j] else bool(READOUT.match(lines[j]))
            if ro and not prev:
                out.append(p)
            prev, j = ro, e
    return out


def run(text: str, combat: bool = False, culture: str | None = None, band: str = "standard", school: str | None = None, turn: bool = False,
        explicit: bool = False) -> dict:
    fails, warns, info = [], [], []
    text = NOTES.split(text, maxsplit=1)[0]  # author notes are not measured
    raw = text
    body = strip_md(text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", READOUT.sub("", body)) if p.strip()]
    prose_paras = [p for p in paragraphs if not p.startswith(">") and not p.startswith("|")]
    sentences = [s for p in prose_paras for s in split_sentences(p)]
    total_words = sum(len(s.split()) for s in sentences)

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
    if sentences and TIDY_CLOSE.match(sentences[-1]):
        warns.append(f"tidy summary close: \"{sentences[-1][:80]}\" (AI-tells §2; R79-4: chapters and arcs close on a hook, scenes on any concrete close, a pressing question included, turns at his next real decision)")

    # --- modern words (narration only) ------------------------------------
    narr = QUOTED.sub(" ", body)
    narr_sents = [x for p in prose_paras for x in split_sentences(QUOTED.sub(" ", p)) if x.strip()]
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
        info.append(f"digits for numbers up to one hundred in narration: {len(digits)} (R70-30-NUMBERS_WORDS_DIGITS: words up to one hundred, digits for system figures): "
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

    # --- R78-3: physical over abstract in fights ------------------------------
    abstract = [m for s in narr_sents for m in FIGHT_ABSTRACT.finditer(s)] if combat else []
    if abstract:
        warns.append(f"fight abstraction in narration: {len(abstract)} ({', '.join(sorted({m.group(0).lower() for m in abstract}))}); "
                     "say what the fist, foot, blade or body did (R78-3-PHYSICAL_AND_SATURATED, R79-6)")

    # --- table rules ---------------------------------------------------------
    info.append(f"length {total_words} words (about {BANDS.get(band, 3500):,} for every in-fiction reply, R79-1-NATALIE_WRITES_HIS_PC)")
    italics = [m.group(1) for m in ITALIC.finditer(raw) if len(m.group(1).split()) >= 3]
    info.append(f"italic interior beats: {len(italics)} (free, no count, R79-4)")
    if prose_paras:
        end = "a turn stops at his next real decision" if turn else "a scene ends on any concrete close, a pressing question included; a chapter or arc on a hook"
        info.append(f"last line: \"{prose_paras[-1][-140:]}\" ({end}, R79-4-INTERIOR_MEANING_WORLD)")

    # --- European jargon (R77-1, check 22, all WOTR prose) ------------------
    jargon = sorted({m.group(0) for m in EUROPEAN_FENCING.finditer(body)}, key=str.casefold)
    if jargon:
        warns.append(f"European fencing jargon: {', '.join(jargon)}; describe body, blade, timing and measure in plain words (R77-1-EUROPEAN_FENCING_ACTIONS, check 22)")

    # --- readouts and stale devices (R71-103, ME2 B and D) --------------------
    ro = readouts(body)
    if ro and combat:
        warns.append(f"readouts: {len(ro)} in a fight; no readouts inside a fight, only at a breakthrough, a re-assay or an arc's end (R79-6-FIGHTS_ON_THE_PAGE)")
    elif ro:
        info.append(f"readouts: {len(ro)} (R70-86-MANY_READOUTS_SCENE_CARRIES, R79-6-FIGHTS_ON_THE_PAGE)")
    for name, rx in STALE.items():
        hits = [(x, m) for x in narr_sents if (m := rx.search(x))]
        if len(hits) > 1:
            x, m = hits[0]
            warns.append(f"stale device: {name} in {len(hits)} sentences of narration, past one a scene, first \"...{x[max(0, m.end() - 70):m.end() + 20]}...\" (R71-103-COMBAT_CHECKS_VERIFY_SCENE)")

    # --- combat density (R13-9 checks 22-23, warn) --------------------------
    if combat:
        school = school or school_for(culture)
        h = len(SCHOOLS[school].findall(raw)); a = len(ANATOMY.findall(raw))
        if h == 0 and school == "blade":
            warns.append("no blade body/action vocabulary found in a combat scene (R77-1-EUROPEAN_FENCING_ACTIONS, R13-9-VERIFY_CHECKS_22_26, check 22)")
        elif h == 0 and school not in ("japanese", "chinese", "korean"):  # Eastern terms are free, never required (R78-5, R79-6)
            warns.append(f"no {school} school vocabulary found in a combat scene (R70-136-NEW_CHECKS_VERIFY_SCENE, R70-100-MARTIAL_VOCABULARY_NAMES_MOVES, check 22)")
        if a == 0:
            warns.append("no injury vocabulary, plain or clinical, found in a combat scene (R13-6-ANATOMY_VOCAB, R79-6, check 23)")
        label = "blade body/action terms" if school == "blade" else f"{school} school terms"
        info.append(f"combat density: {h} {label}, {a} anatomy terms")
        fight_narr = ITALIC.sub(" ", "\n\n".join(QUOTED.sub(" ", p) for p in prose_paras))
        if run_ := list(RUNNING.finditer(fight_narr)):
            s_ = fight_narr[max(0, run_[0].start() - 50):run_[0].end() + 10].replace("\n", " ")
            warns.append(f"figure in fight narration: {len(run_)} reserve figures (EU, AU/s, eta), first \"...{s_.strip()}...\"; in a fight, figures live in mouths, never narration (R79-6-FIGHTS_ON_THE_PAGE)")

    # --- explicit mode (R73-41, ME2 B and C; word-presence checks retired, R79-7) ----
    if explicit:
        for m in ITALIC.finditer(body):
            if MIMETIC.fullmatch(m.group(1).strip(" .,;:!?")):
                warns.append(f"italicised mimetic word: \"*{m.group(1)}*\" (R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL: romanised and never italic, R73-41-INTIMACY_CHECKS_VERIFY)")
        seen = set()
        for m in EUPHEMISM.finditer(narr_plain):
            if m.group(0).lower() not in seen:
                seen.add(m.group(0).lower())
                s_ = narr_plain[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
                fails.append(f"bed euphemism in narration: \"{m.group(0)}\" in \"...{s_.strip()}...\" (R49-51-EXPLICIT, R73-41-INTIMACY_CHECKS_VERIFY; free in a mouth)")
        rx, by_key = cards()
        named = {n: a for k in (set(rx.findall(raw)) if rx else ()) for n, a in by_key[k]}
        for n, a in sorted(named.items()):
            if a is not None and a < 18:
                fails.append(f"floor guard: {n} is {a} on file, under eighteen, named in an explicit scene (R73-41-INTIMACY_CHECKS_VERIFY, NATALIE.md floor)")
        if unaged := sorted(n for n, a in named.items() if a is None):
            warns.append(f"floor guard: no age on file for {', '.join(unaged)}; a partner's card or roster entry needs the body's adult age before drafting (R73-41-INTIMACY_CHECKS_VERIFY)")
        if named:
            info.append("floor guard, named on file: " + ", ".join(f"{n} {'?' if a is None else a}" for n, a in sorted(named.items())))

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
    ap.add_argument("--turn", action="store_true", help="the text is a roleplay turn: the last-line note reads for his next real decision (R79-4)")
    ap.add_argument("--explicit", action="store_true", help="an explicit scene: the floor guard and bed euphemisms (R73-41, R79-7)")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    text = Path(a.file).read_text(encoding="utf-8", errors="replace")
    res = run(text, combat=a.combat, culture=a.culture, band=a.band, school=a.school, turn=a.turn, explicit=a.explicit)
    if a.echoes:
        res["warns"] += echoes(text)
    print(report(res))
    return 1 if res["fails"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
