#!/usr/bin/env python3
"""WAR-9, step 1 — sweep the wiki mirror for every attested essence figure.

Reads `wiki/**/*.md` and emits one candidate row per figure occurrence with the
exact file, line number and the verbatim line the figure sits in. Values are
parsed only where the form is unambiguous; anything else is emitted with
`value: null` and `parsed: false` so a human fills it or leaves it null.

Nothing here decides anything. It collects. `anchors.json` is the reviewed
output; this script produces `_candidates.json` beside it.

    python imports/essence-ledger/extract_anchors.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WIKI = REPO / "wiki"
OUT = Path(__file__).resolve().parent / "_candidates.json"

# ¹ ² ³ are Latin-1 (U+00B9/B2/B3) and the rest are U+2070.., so the class is
# listed character by character rather than as a range.
SUPS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
SUPER = str.maketrans(SUPS, "0123456789-")

NUM = r"[0-9][0-9,]*(?:\.[0-9]+)?"
SCALE = r"(?:\s*(?:million|billion|trillion|thousand))?"
SCI = rf"[0-9]+(?:\.[0-9]+)?\s*(?:×|x)\s*10[{SUPS}]+"
# what may sit between a field label and its number
SEP = r"[\s:·|*—–-]*(?:is|of|at|approximately|roughly|about|around|estimated|est\.?)?[\s:·*]*"
SCALES = {
    "thousand": 1_000,
    "million": 1_000_000,
    "billion": 1_000_000_000,
    "trillion": 1_000_000_000_000,
}

# joules — the measured side of the conversion. Part Eleven states that Strike
# Force and Durability are recorded in joules, so a card's joule figure is the
# quantity Part Four grades, attested rather than inferred.
JMULT = {"": 1, "k": 1e3, "M": 1e6, "G": 1e9, "T": 1e12,
         "P": 1e15, "E": 1e18, "Z": 1e21}


def to_number(text: str):
    """Parse one numeric token. Returns float or None — never a guess."""
    t = text.strip().strip("*_ ").replace(" ", " ")
    t = t.lstrip("~≈").strip()
    m = re.fullmatch(rf"({NUM})\s*(?:×|x)\s*10([{SUPS}]+)", t)
    if m:
        return float(m.group(1).replace(",", "")) * 10 ** int(m.group(2).translate(SUPER))
    m = re.fullmatch(rf"({NUM})\s*(thousand|million|billion|trillion)", t, re.I)
    if m:
        return float(m.group(1).replace(",", "")) * SCALES[m.group(2).lower()]
    m = re.fullmatch(NUM, t)
    if m:
        return float(t.replace(",", ""))
    return None


def j_mantissa(text: str):
    """One joule mantissa, plain or scientific. Returns float or None."""
    t = text.strip().lstrip("~≈").strip()
    m = re.fullmatch(rf"({J_NUM})\s*(?:×|x)\s*10(?:([{SUPS}]+)|\^(-?[0-9]+))", t)
    if m:
        exp = m.group(2).translate(SUPER) if m.group(2) else m.group(3)
        return float(m.group(1).replace(",", "")) * 10 ** int(exp)
    if re.fullmatch(J_NUM, t):
        return float(t.replace(",", ""))
    return None


def joule_value(token: str):
    """(value, low, high) in joules for one swept joule token."""
    m = JOULE_RANGE.fullmatch(token.strip())
    if m:
        mult = JMULT[m.group("u")]
        lo, hi = j_mantissa(m.group("lo")), j_mantissa(m.group("hi"))
        return None, (lo * mult if lo is not None else None), (hi * mult if hi is not None else None)
    m = JOULE_ONE.fullmatch(token.strip())
    if m:
        v = j_mantissa(m.group("n"))
        return (v * JMULT[m.group("u")] if v is not None else None), None, None
    return None, None, None


# The label a figure sits under, as the page writes it. In a table row it is
# the row's first cell; elsewhere it is the nearest bolded field name before
# the figure — which is what tells `43 PJ shielding` on a Durability run from
# the `88 PJ` earlier in the same Strike Force line. A bold span the figure
# sits inside is not its label. Taken as written and never translated.
LABEL_CELL = re.compile(r"^\|\s*(?P<v>[^|]{1,60})\|")
LABEL_BOLD = re.compile(r"\*\*(?P<v>[^*]{1,60})\*\*")


def label_of(raw: str, token: str | None = None):
    m = LABEL_CELL.match(raw)
    if m:
        return re.sub(r"[*_`]", "", m.group("v")).strip().strip("·:").strip() or None
    at = raw.find(token) if token else -1
    if at < 0:
        at = len(raw)
    best = None
    for m in LABEL_BOLD.finditer(raw):
        if m.end() <= at:
            best = m
    if not best:
        return None
    return re.sub(r"[*_`]", "", best.group("v")).strip().strip("·:").strip() or None


def clean(line: str) -> str:
    return line.rstrip("\n")


# --- figure patterns -------------------------------------------------------
# Each entry: kind, regex over the raw line, group holding the number token.
# Two families: unit-suffixed (the number precedes the unit) and label-led
# (a bolded field name precedes the number).

UNIT_PATTERNS = [
    ("au_s", re.compile(rf"(?P<n>{SCI}|~?{NUM}{SCALE})\s*\*{{0,2}}\s*AU/s", re.I)),
    ("flux_density", re.compile(rf"(?P<n>{SCI}|~?{NUM}{SCALE})\s*\*{{0,2}}\s*EU/g", re.I)),
]

LABEL_PATTERNS = [
    # bare "Output" is deliberately not a label: on several cards it is a
    # Sub-Stat name ("Ardency Crown Breaker Output 420"). An output figure is
    # caught by the AU/s unit pattern instead.
    ("au_s", re.compile(
        rf"(?:\*\*)?(?:AU/s|Aether Output|Aether Index){SEP}(?P<n>{SCI}|~?{NUM}{SCALE})", re.I)),
    ("flux_density", re.compile(
        rf"(?:\*\*)?Flux Density(?:\s*\(EU/g\))?{SEP}(?P<n>{SCI}|~?{NUM}{SCALE})", re.I)),
    ("eu_reserve", re.compile(
        r"(?:\*\*)?(?:EU Reserve|Essence Capacity(?:\s*\(EU Reserve\))?|Essence Reserve)"
        rf"{SEP}(?P<n>{SCI}|~?{NUM}{SCALE})", re.I)),
]

# "…drawn from Dougou's 92,000 EU reserve", "roughly 4,200,000", "850,000,000 EU reserve"
RESERVE_TRAILING = re.compile(rf"(?P<n>{SCI}|~?{NUM}{SCALE})\s*EU\s+reserve", re.I)

# absolute EU costs: a number followed by bare EU (not EU/g, EU/s, EU/min, EU/hour)
EU_COST = re.compile(rf"(?P<n>{SCI}|~?{NUM}{SCALE})\s*\*{{0,2}}\s*EU\b(?!/|\s*(?:per|reserve))", re.I)

J_NUM = r"[0-9][0-9,]*(?:\.[0-9]+)?"
J_SCI = rf"{J_NUM}\s*(?:×|x)\s*10(?:[{SUPS}]+|\^-?[0-9]+)"
# "8 to 20 MJ", "1–5 MJ", "0.12–0.40 PJ" — one unit, shared by both ends.
# A unit letter between the two ends ("46 GJ to 4.184 TJ") stops the match, and
# the two figures are then taken singly by JOULE_ONE.
JOULE_RANGE = re.compile(
    rf"(?P<lo>{J_SCI}|~?{J_NUM})\s*(?:–|—|-|to)\s*(?P<hi>{J_SCI}|~?{J_NUM})\s*(?P<u>[kMGTPEZ]?)J\b")
JOULE_ONE = re.compile(rf"(?P<n>{J_SCI}|~?{J_NUM})\s*(?P<u>[kMGTPEZ]?)J\b")

ETA_RANGE = re.compile(r"η[^0-9\n]{0,18}?(?P<lo>[01]?\.[0-9]+)\s*(?:–|—|-|to)\s*(?P<hi>[01]?\.[0-9]+)")
ETA_ONE = re.compile(r"η[^0-9\n]{0,18}?(?P<n>~?[01](?:\.[0-9]+)?)")
ETA_LABEL = re.compile(r"(?:Efficiency|η)\s*(?:\(η\))?\s*(?:·|:|\|)\s*\*{0,2}(?P<n>~?[01](?:\.[0-9]+)?)", re.I)

# --- page context ----------------------------------------------------------

ROMAN = r"(?:XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)"

# Only labelled fields are read. A bare "Stage VIII" in prose, or a "Grade S"
# from a stat row, is not the card's field and is left null rather than guessed.
CTX = {
    "level": re.compile(r"\*{0,2}Level\s*(?:/\s*Stage\s*)?\*{0,2}\s*(?:\||·|:)\s*\*{0,2}\s*"
                        r"(?P<v>[0-9][0-9,]*(?:\s*/\s*[0-9,]+)?)"),
    # older cards write the Stage in arabic ("Stage 8 — Transcendence"); the
    # arabic form is bounded to 1–16 so a "Level / Stage | 80 / 500" row cannot
    # hand back a Level as a Stage.
    "temperance_stage": re.compile(r"\*{0,2}(?:Temperance )?Stage\*{0,2}[\s,|:·—–-]*\*{0,2}"
                                   rf"(?:Stage\s*)?(?P<v>{ROMAN}|1[0-6]|[1-9])\b"),
    "tier_of_standing": re.compile(r"Tier of Standing:?\s*(?P<v>[0-9](?:\s*,?\s*[A-Za-z]+)?)"),
    # Aether Class holds a Roman class on newer cards and a descriptive name on
    # older ones; both are kept as written and neither is translated.
    "aether_class": re.compile(r"\*{0,2}Aether (?:Class|Shell)\s*\*{0,2}\s*(?:\||·|:)\s*"
                               r"(?P<v>[^|]{1,70})"),
    "coherence_band": re.compile(r"Coherence Band\*{0,2}\s*(?:\||·|:|\s)\s*\*{0,2}(?P<v>[A-Z]{1,3}|Ø)\b"),
    "level_band": re.compile(r"(?:Level Band|Band)\s+(?P<v>I{1,3}|IV|V)\b(?!\w)"),
    # the Grade the card states for itself, taken only off a line that also
    # carries a Stage, a Ceiling or a Coherence Band — never off a stat row
    "stated_grade": re.compile(
        rf"(?=.*(?:Stage\s+(?:{ROMAN}|[0-9])|Ceiling|Coherence Band))"
        r".*?\bGrade\s+\*{0,2}(?P<v>SSS|SS|S|EX\+|EX|X|A|B|C|D|E|F|Hollow)\b"),
}

CTX_LINE = re.compile(
    r"Temperance Stage|\*\*Level\*\*|Coherence Band|Aether Class|Aether Shell|"
    rf"Tier of Standing|\*\*Stage {ROMAN}\b|Stage {ROMAN},?\s*[A-Z]", re.I)


def page_context(lines: list[str]) -> dict:
    """Read labelled fields only. Every value keeps the line it came from."""
    ctx: dict = {}
    for field, pat in CTX.items():
        ctx[field] = None
        ctx[f"{field}_line"] = None
        for i, raw in enumerate(lines, start=1):
            m = pat.search(raw)
            if m:
                ctx[field] = m.group("v").strip().strip("*").strip().rstrip(",.")
                ctx[f"{field}_line"] = i
                break
    # every line that states one of these fields, verbatim, for audit
    ctx["context_lines"] = [
        {"line": i, "verbatim": clean(raw)}
        for i, raw in enumerate(lines, start=1)
        if CTX_LINE.search(raw)
    ][:8]
    ctx["tier_grades"] = tier_grades(lines)
    return ctx


PRIMARIES = ("Ardency", "Dexterity", "Dominion", "Gnosis", "Harmonics",
             "Resilience", "Tempering", "Vitality")
GRADE = r"Hollow|SSS|SS|S|EX\+|EX|X|A|B|C|D|E|F"
STAT_ROWS = (
    # | **Gnosis** | **590** | **SS** | …
    re.compile(rf"^\|\s*\*{{0,2}}(?P<stat>{'|'.join(PRIMARIES)})\*{{0,2}}\s*\|\s*"
               rf"\*{{0,2}}(?P<value>[0-9][0-9,]*)\*{{0,2}}\s*\|\s*"
               rf"\*{{0,2}}(?P<grade>{GRADE})\*{{0,2}}\s*[|\s]"),
    # | **Ardency** | **368 · A** — primary spike | …
    re.compile(rf"^\|\s*\*{{0,2}}(?P<stat>{'|'.join(PRIMARIES)})\*{{0,2}}\s*\|\s*"
               rf"\*{{0,2}}(?P<value>[0-9][0-9,]*)\s*(?:·|—|-|,)\s*(?P<grade>{GRADE})\b"),
)


def tier_grades(lines: list[str]) -> list[dict]:
    """The Primary / value / Grade rows of the card's stat table, as written."""
    out = []
    for i, raw in enumerate(lines, start=1):
        m = next((p.match(raw.strip()) for p in STAT_ROWS if p.match(raw.strip())), None)
        if m:
            out.append({
                "stat": m.group("stat"),
                "value": int(m.group("value").replace(",", "")),
                "grade": m.group("grade"),
                "line": i,
            })
    return out


def scan_line(raw: str):
    """Yield (kind, token) for every figure in one line, de-duplicated by span."""
    found = []
    spans = []

    def take(kind, m):
        for a, b in spans:
            if not (m.end("n") <= a or m.start("n") >= b):
                return
        spans.append((m.start("n"), m.end("n")))
        found.append((kind, m.group("n").strip()))

    for kind, pat in UNIT_PATTERNS:
        for m in pat.finditer(raw):
            take(kind, m)
    for kind, pat in LABEL_PATTERNS:
        for m in pat.finditer(raw):
            take(kind, m)
    for m in RESERVE_TRAILING.finditer(raw):
        take("eu_reserve", m)
    for m in EU_COST.finditer(raw):
        take("eu_cost", m)

    # joules. Ranges first, so "8 to 20 MJ" is one figure with two ends rather
    # than two figures; spans keep JOULE_ONE off what the range already took.
    jspans = []
    for m in JOULE_RANGE.finditer(raw):
        jspans.append((m.start(), m.end()))
        found.append(("joule", m.group(0).strip()))
    for m in JOULE_ONE.finditer(raw):
        if any(not (m.end() <= a or m.start() >= b) for a, b in jspans):
            continue
        jspans.append((m.start(), m.end()))
        found.append(("joule", m.group(0).strip()))

    m = ETA_RANGE.search(raw)
    if m:
        found.append(("eta", f"{m.group('lo')}–{m.group('hi')}"))
    else:
        m = ETA_LABEL.search(raw) or ETA_ONE.search(raw)
        if m:
            found.append(("eta", m.group("n").strip()))
    return found


def main() -> int:
    rows = []
    for path in sorted(WIKI.rglob("*.md")):
        rel = path.relative_to(REPO).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        title = next((l.split(":", 1)[1].strip().strip('"')
                      for l in lines[:8] if l.startswith("title:")), path.stem)
        ctx = None
        for n, raw in enumerate(lines, start=1):
            hits = scan_line(raw)
            if not hits:
                continue
            if ctx is None:
                ctx = page_context(lines)
            for kind, token in hits:
                if kind == "joule":
                    value, low, high = joule_value(token)
                elif kind == "eta" and "–" in token:
                    lo, hi = token.split("–")
                    value, low, high = None, to_number(lo), to_number(hi)
                else:
                    value, low, high = to_number(token), None, None
                rows.append({
                    "page_title": title,
                    "kind": kind,
                    "token": token,
                    "label": label_of(raw, token),
                    "value": value,
                    "low": low,
                    "high": high,
                    "parsed": value is not None or (low is not None and high is not None),
                    "file": rel,
                    "line": n,
                    "verbatim": clean(raw),
                    "context": ctx,
                })
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    by_kind: dict[str, int] = {}
    for r in rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
    print(f"{len(rows)} candidate figures -> {OUT.relative_to(REPO)}")
    for k in sorted(by_kind):
        print(f"  {k:<14} {by_kind[k]}")
    print(f"  unparsed       {sum(1 for r in rows if not r['parsed'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
