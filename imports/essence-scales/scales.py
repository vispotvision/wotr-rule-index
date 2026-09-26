#!/usr/bin/env python3
"""The essence scales — every figure computed from the quoted anchors, none typed.

WAR-161. Builds, from canon tables and the rulings that bind them:

  1. the EU-by-Stage benchmark table          (Part Four x Part Five x R44-1 x C-059)
  2. the AU/s progression by Stage and Tier   (the same, through the 6-second turn)
  3. the AU-to-joule equivalence              (R44-1 + the AU-to-joule rate)
  4. the turn table                           (one turn = 6 seconds)

The three constants and the four answers this file works from are RULINGS.md,
2026-09-25 R44-1 and R44-2, and RULINGS.md, 2026-09-26, "WAR-3 cards 1 and 2
(system accounts, 20 answers)", recorded in full on WAR-3's comments of the
same day.

Every anchor below is quoted in `_derivation.md` with its file and line. Nothing
here is invented: the two tables are Part Four and Part Five as the mirror holds
them, and the three constants are ruled.

Run:  python3 imports/essence-scales/scales.py            # the tables, as markdown
      python3 imports/essence-scales/scales.py --json     # the same, as data
"""

import json
import math
import sys

# --- Anchor 1: Part Four, the Grade table -------------------------------------
# wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds
# (Parts Four–Ten).md:26-39.  (sub-stat floor, sub-stat ceiling, J floor, J ceiling)
# A None bound is a bound the table does not state ("below 60 J", "and above").
# The fifth item on each row is the page's own Attack output cell, character for
# character, so the anchor can be reproduced without being reformatted.
GRADES = [
    ("Hollow", 1, 10, None, 60.0, "below 60 J"),
    ("F", 11, 25, 60.0, 300.0, "60\u2013300 J"),
    ("E", 26, 50, 300.0, 15.0e3, "300 J \u2013 15 kJ"),
    ("D", 51, 100, 15.0e3, 2.092e7, "15 kJ \u2013 2.092\u00d710^7 J"),
    ("C", 101, 175, 2.092e7, 1.046e9, "2.092\u00d710^7 \u2013 1.046\u00d710^9 J"),
    ("B", 176, 275, 1.046e9, 4.6024e10, "1.046\u00d710^9 \u2013 4.6024\u00d710^10 J"),
    ("A", 276, 400, 4.6024e10, 4.184e12, "4.6024\u00d710^10 \u2013 4.184\u00d710^12 J"),
    ("S", 401, 550, 4.184e12, 2.42672e13, "4.184\u00d710^12 \u2013 2.42672\u00d710^13 J"),
    ("SS", 551, 725, 4.184e13, 4.184e14, "4.184\u00d710^13 \u2013 4.184\u00d710^14 J"),
    ("SSS", 726, 950, 4.184e14, 4.184e21, "4.184\u00d710^14 \u2013 4.184\u00d710^21 J"),
    ("X", 951, 1200, 4.184e21, 1.24e29, "4.184\u00d710^21 \u2013 1.24\u00d710^29 J"),
    ("EX", 1201, 1500, 1.24e29, 6.906e37, "1.24\u00d710^29 \u2013 6.906\u00d710^37 J"),
    ("EX+", 1501, None, 6.906e37, None, "6.906\u00d710^37 J and above"),
]
GRADE = {g[0]: g for g in GRADES}

# --- Anchor 2: Part Five, Temperance Gates and Stat Ceilings -------------------
# The same file, :60-77.  (Stage, name, Max Grade, Sub-Stat ceiling, Tier of Standing)
# max_grade None at XVI: the table writes "uncapped".
STAGES = [
    ("I", "Murmuring", "E", 50, 1),
    ("II", "Welling", "D", 100, 2),
    ("III", "Ascension", "C", 175, 3),
    ("IV", "Flourishing", "B", 275, 4),
    ("V", "Splintering", "B", 350, 5),
    ("VI", "Glory", "A", 400, 5),
    ("VII", "Refraction", "A", 475, 5),
    ("VIII", "Transcendence", "S", 550, 6),
    ("IX", "Invocation", "S", 625, 6),
    ("X", "Realization", "SS", 725, 6),
    ("XI", "Dissonance", "SS", 750, 7),
    ("XII", "Emanation", "SSS", 950, 7),
    ("XIII", "Principality", "X", 1200, 8),
    ("XIV", "Zenith", "EX", 1500, 8),
    ("XV", "Revelation", "EX+", 2200, 9),
    ("XVI", "Apex", None, None, 9),
]

TIER_NAME = {
    1: "Initiate", 2: "Apprentice", 3: "Journeyman", 4: "Adept", 5: "Expert",
    6: "Master", 7: "Grandmaster", 8: "Archmaster", 9: "Paragon",
}

# --- Anchor 3: Part Nineteen, efficiency by Tier of Standing -------------------
# wiki/.../VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md:91-101,
# with the Tier 5 cell as R44-4 corrects it (0.60-0.70, applied to Notion under WAR-133).
# None ceiling at Tier 9: the table writes "above 1.2, unbounded".
ETA_BY_TIER = {
    1: (0.30, 0.30), 2: (0.35, 0.35), 3: (0.40, 0.40), 4: (0.45, 0.45),
    5: (0.60, 0.70), 6: (0.70, 0.80), 7: (0.85, 0.90), 8: (0.95, 1.2),
    9: (1.2, None),
}

# --- Anchor 4: the Stages whose force is not measured --------------------------
# Part Four, the same file :51: "At **Zenith, Stage XIV**, speed and attack output
# are no longer assessed by conventional metrics." Isaac's WAR-142 answer
# (RULINGS.md, 2026-09-26, the queue questionnaire) carries that upward: "Stage XV
# keeps its EX+ Grade label, but its force is unmeasured like Zenith's; the Zenith
# row sits beside the Grade ladder, not on it." Apex states no Max Grade at all.
# These Stages therefore take no derived EU or AU/s figure.
UNMEASURED = {"XIV", "XV", "XVI"}

# --- The three constants ------------------------------------------------------
EU_JOULE = 1.0e6          # R44-1: 1 EU = 1 MJ
TURN_SECONDS = 6.0        # WAR-3 card 1 q7: one turn = 6 seconds
AU_WATT = 1.0e6           # WAR-3 card 1 q3: 1 AU = 1 EU = 1 MJ, so 1 AU/s = 1 MW


def sig(x, n=4):
    """Four significant figures, in the notation Part Four itself uses."""
    if x is None:
        return None
    if x == 0:
        return "0"
    e = math.floor(math.log10(abs(x)))
    m = round(x / 10 ** e, n - 1)
    if m >= 10:          # rounding carried
        m, e = m / 10, e + 1
    if -1 <= e < 6:
        v = m * 10 ** e
        if abs(v - round(v)) < 10 ** (e - n + 1) / 2 and abs(v) >= 1:
            return f"{round(v):,}"
        return f"{v:,.{max(0, n - 1 - e)}f}".rstrip("0").rstrip(".")
    return f"{m:.{n-1}f}×10^{e}"


def geomean(a, b):
    if a is None or b is None:
        return None
    return math.sqrt(a * b)


def strain_grade(stage):
    """Part Five: at V, VII, IX and XI the Sub-Stat ceiling sits above the Max
    Grade bracket. Part Four's Sub-Stat column says which Grade that ceiling
    reaches. Returns that Grade, or None where the ceiling tops out the bracket."""
    _, _, mg, ceiling, _ = stage
    if mg is None or ceiling is None:
        return None
    if GRADE[mg][2] is None or ceiling <= GRADE[mg][2]:
        return None
    for name, lo, hi, _, _, _ in GRADES:
        if hi is None or lo <= ceiling <= hi:
            return name if name != mg else None
    return None


def band(grade):
    """(J floor, J ceiling) for a Grade."""
    if grade is None:
        return (None, None)
    return (GRADE[grade][3], GRADE[grade][4])


def rows():
    out = []
    for st in STAGES:
        roman, name, mg, ceiling, tier = st
        jf, jc = (None, None) if roman in UNMEASURED else band(mg)
        eu_f = jf / EU_JOULE if jf else None
        eu_c = jc / EU_JOULE if jc else None
        eu_b = geomean(eu_f, eu_c)
        aus_f = eu_f / TURN_SECONDS if eu_f else None
        aus_c = eu_c / TURN_SECONDS if eu_c else None
        aus_b = eu_b / TURN_SECONDS if eu_b else None
        sg = None if roman in UNMEASURED else strain_grade(st)
        sjf, sjc = band(sg)
        out.append(dict(
            stage=roman, name=name, max_grade=mg, substat_ceiling=ceiling,
            tier=tier, tier_name=TIER_NAME[tier],
            eta=ETA_BY_TIER[tier],
            j_floor=jf, j_ceiling=jc,
            eu_floor=eu_f, eu_ceiling=eu_c, eu_benchmark=eu_b,
            aus_floor=aus_f, aus_ceiling=aus_c, aus_benchmark=aus_b,
            strain_grade=sg,
            strain_eu_floor=sjf / EU_JOULE if sjf else None,
            strain_eu_ceiling=sjc / EU_JOULE if sjc else None,
            strain_eu_benchmark=geomean(sjf, sjc) / EU_JOULE if geomean(sjf, sjc) else None,
        ))
    return out


def tier_rows(rs):
    out = []
    for t in range(1, 10):
        mem = [r for r in rs if r["tier"] == t]
        measured = [r for r in mem if r["stage"] not in UNMEASURED]
        floors = [r["eu_floor"] for r in measured if r["eu_floor"] is not None]
        ceils = [r["eu_ceiling"] for r in measured if r["eu_ceiling"] is not None]
        unbounded = any(r["eu_ceiling"] is None for r in measured
                        if r["eu_floor"] is not None)
        f = min(floors) if floors else None
        c = None if unbounded else (max(ceils) if ceils else None)
        b = geomean(f, c)
        out.append(dict(
            tier=t, tier_name=TIER_NAME[t],
            stages=[r["stage"] for r in mem],
            unmeasured=[r["stage"] for r in mem if r["stage"] in UNMEASURED],
            eta=ETA_BY_TIER[t],
            eu_floor=f, eu_ceiling=c, eu_benchmark=b,
            aus_floor=f / TURN_SECONDS if f else None,
            aus_ceiling=c / TURN_SECONDS if c else None,
            aus_benchmark=b / TURN_SECONDS if b else None,
        ))
    return out


def rng(a, b, unit=""):
    if a is None and b is None:
        return "unmeasured"
    if b is None:
        return f"{sig(a)}{unit} and above"
    if a is None:
        return f"below {sig(b)}{unit}"
    return f"{sig(a)}–{sig(b)}{unit}"


def markdown():
    rs = rows()
    L = []
    L.append("### The EU-by-Stage benchmark\n")
    L.append("| Stage | Name | Max Grade | EU band | Benchmark reserve (EU) | Under strain |")
    L.append("|---|---|---|---|---|---|")
    for r in rs:
        strain = "—"
        if r["stage"] in UNMEASURED:
            strain = "not assessed by conventional metrics"
        elif r["strain_grade"]:
            strain = (f"{r['strain_grade']}-Grade reach, "
                      f"{rng(r['strain_eu_floor'], r['strain_eu_ceiling'])} EU")
        elif r["max_grade"] is None:
            strain = "no ceiling"
        bm = sig(r['eu_benchmark']) or ('unmeasured' if r['stage'] in UNMEASURED
                                        else 'null')
        L.append(f"| {r['stage']} | {r['name']} | {r['max_grade'] or 'uncapped'} | "
                 f"{rng(r['eu_floor'], r['eu_ceiling'])} | {bm} | {strain} |")
    L.append("\n### The AU/s progression by Stage\n")
    L.append("| Stage | Tier of Standing | η | AU/s band | Benchmark AU/s | Delivered in one turn |")
    L.append("|---|---|---|---|---|---|")
    for r in rs:
        eta_lo, eta_hi = r["eta"]
        eta = f"{eta_lo:.2f}" if eta_hi == eta_lo else (
            f"{eta_lo:.2f}–{eta_hi:.2f}" if eta_hi else f"above {eta_lo:.1f}")
        eta_mid = (eta_lo + eta_hi) / 2 if eta_hi else None
        delivered = (sig(r["eu_benchmark"] * eta_mid * EU_JOULE) + " J"
                     if (r["eu_benchmark"] and eta_mid) else "unmeasured")
        L.append(f"| {r['stage']} | {r['tier']} · {r['tier_name']} | {eta} | "
                 f"{rng(r['aus_floor'], r['aus_ceiling'])} | "
                 f"{sig(r['aus_benchmark']) or 'unmeasured'} | {delivered} |")
    L.append("\n### The same ladder by Tier of Standing\n")
    L.append("| Tier | Temperance | η | EU band | AU/s band | Benchmark AU/s |")
    L.append("|---|---|---|---|---|---|")
    for t in tier_rows(rs):
        eta_lo, eta_hi = t["eta"]
        eta = f"~{eta_lo:.2f}" if eta_hi == eta_lo else (
            f"{eta_lo:.2f}–{eta_hi:.2f}" if eta_hi else f"above {eta_lo:.1f}")
        L.append(f"| {t['tier']} · {t['tier_name']} | "
                 f"{t['stages'][0]}–{t['stages'][-1]} | {eta} | "
                 f"{rng(t['eu_floor'], t['eu_ceiling'])} | "
                 f"{rng(t['aus_floor'], t['aus_ceiling'])} | "
                 f"{sig(t['aus_benchmark']) or 'unmeasured'}"
                 f"{' (' + ', '.join(t['unmeasured']) + ' unmeasured)' if t['unmeasured'] else ''} |")
    L.append("\n### The turn\n")
    L.append("| turns | seconds | delivered by a working of R AU/s | drawn from the reserve at η |")
    L.append("|---|---|---|---|")
    for n in (1, 2, 3, 4, 5, 6, 10, 20, 100):
        L.append(f"| {n} | {int(n*TURN_SECONDS)} | {int(n*TURN_SECONDS)}R MJ | "
                 f"{int(n*TURN_SECONDS)}R ÷ η EU |")
    return "\n".join(L)


if __name__ == "__main__":
    if "--json" in sys.argv:
        print(json.dumps({"stages": rows(), "tiers": tier_rows(rows()),
                          "constants": {"eu_joule": EU_JOULE,
                                        "turn_seconds": TURN_SECONDS,
                                        "au_watt": AU_WATT}}, indent=1))
    else:
        print(markdown())
