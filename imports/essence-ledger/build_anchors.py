#!/usr/bin/env python3
"""WAR-9, step 1 — assemble `anchors.json` from the sweep plus the hand checks.

Input  : `_candidates.json` (written by `extract_anchors.py`)
Output : `anchors.json`

Three things happen here and nothing else:

1.  The system tables the fit is read against are lifted **verbatim** out of
    the wiki mirror — Part Four's Grade / joule table, Part Five's Stage gates,
    Part Nineteen's efficiency table and its four resource definitions. They are
    located by their header line, not by line number, so an edit upstream moves
    them rather than silently mis-quoting them.
2.  The swept figures are carried through unchanged.
3.  A short hand supplement adds the figures the sweep could not parse — a
    second number on a line that carries two, a number written out in words.
    Every supplement row names the file and line and quotes the whole line;
    nothing is added that is not on the page.

    python imports/essence-ledger/build_anchors.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CANDIDATES = HERE / "_candidates.json"
OUT = HERE / "anchors.json"

FOW_II = REPO / "wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md"
FOW_VII = REPO / "wiki/Fracture of Worlds — The Living System/VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md"

SUPS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
SUPER = str.maketrans(SUPS, "0123456789-")


def lines_of(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def table_after(lines: list[str], header_startswith: str) -> list[tuple[int, str]]:
    """The rows of the markdown table whose header line starts with the given text."""
    for i, raw in enumerate(lines):
        if raw.startswith(header_startswith):
            rows = []
            for j in range(i + 2, len(lines)):  # +2 skips the |---| separator
                if not lines[j].startswith("|"):
                    break
                rows.append((j + 1, lines[j]))
            return rows
    raise SystemExit(f"table header not found: {header_startswith!r}")


def find_line(lines: list[str], startswith: str) -> tuple[int, str]:
    for i, raw in enumerate(lines, start=1):
        if raw.startswith(startswith):
            return i, raw
    raise SystemExit(f"line not found: {startswith!r}")


def cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def strip_md(text: str) -> str:
    return re.sub(r"\*+", "", text).strip()


# --- joule parsing for the Grade table ------------------------------------
# Forms in Part Four: "below 60 J", "60–300 J", "300 J – 15 kJ",
# "15 kJ – 2.092×10^7 J", "6.906×10^37 J and above".
MULT = {"": 1, "k": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}
JOULE = re.compile(r"([0-9][0-9.,]*)\s*(?:×|x)?\s*(?:10\^?([0-9]+))?\s*([kMGT]?)J")


def joules(token: str):
    m = JOULE.search(token)
    if not m:
        return None
    base = float(m.group(1).replace(",", ""))
    if m.group(2):
        base *= 10 ** int(m.group(2))
    return base * MULT[m.group(3)]


def grade_band(cell: str) -> tuple:
    """(low, high) in joules. `None` on an open end."""
    text = strip_md(cell)
    if text.lower().startswith("below"):
        return (None, joules(text))
    if "and above" in text.lower():
        return (joules(text), None)
    parts = re.split(r"\s*[–—]\s*", text)
    if len(parts) == 2:
        lo, hi = parts
        hi_j = joules(hi)
        # "60–300 J" leaves the unit off the low end; borrow the high end's
        lo_j = joules(lo)
        if lo_j is None and hi_j is not None:
            m = re.match(r"\s*([0-9][0-9.,]*)\s*(?:×|x)?\s*(?:10\^?([0-9]+))?", lo)
            if m:
                lo_j = float(m.group(1).replace(",", ""))
                if m.group(2):
                    lo_j *= 10 ** int(m.group(2))
                unit = JOULE.search(hi)
                lo_j *= MULT[unit.group(3)] if unit else 1
        return (lo_j, hi_j)
    return (None, None)


def system_tables() -> dict:
    ii, vii = lines_of(FOW_II), lines_of(FOW_VII)

    grades = []
    for n, row in table_after(ii, "| Grade | Sub-Stat value |"):
        c = cells(row)
        lo, hi = grade_band(c[2])
        grades.append({
            "grade": strip_md(c[0]),
            "substat_value": strip_md(c[1]),
            "attack_output": strip_md(c[2]),
            "attack_output_j_low": lo,
            "attack_output_j_high": hi,
            "travel_speed": strip_md(c[3]),
            "source": {"file": FOW_II.relative_to(REPO).as_posix(), "line": n},
            "verbatim": row,
        })

    stages = []
    for n, row in table_after(ii, "| Stage | Name | Max Grade |"):
        c = cells(row)
        stages.append({
            "stage": strip_md(c[0]),
            "name": strip_md(c[1]),
            "max_grade": strip_md(c[2]),
            "substat_ceiling": strip_md(c[3]),
            "tier_of_standing": strip_md(c[4]),
            "source": {"file": FOW_II.relative_to(REPO).as_posix(), "line": n},
            "verbatim": row,
        })

    etas = []
    for n, row in table_after(vii, "| Tier | Temperance | η |"):
        c = cells(row)
        eta = strip_md(c[2])
        m = re.match(r"~?([0-9.]+)\s*(?:–|—|-)\s*([0-9.]+)$", eta)
        etas.append({
            "tier": strip_md(c[0]),
            "temperance": strip_md(c[1]),
            "eta": eta,
            "eta_low": float(m.group(1)) if m else (
                float(eta.lstrip("~")) if re.fullmatch(r"~?[0-9.]+", eta) else None),
            "eta_high": float(m.group(2)) if m else (
                float(eta.lstrip("~")) if re.fullmatch(r"~?[0-9.]+", eta) else None),
            "note": strip_md(c[3]),
            "source": {"file": FOW_VII.relative_to(REPO).as_posix(), "line": n},
            "verbatim": row,
        })

    defs = []
    for start in ("**EU (Essence Units)**", "**Flux Density (EU/g)**",
                  "**AU/s (Aether Units per second)**", "**Eta (η), Efficiency**"):
        n, raw = find_line(vii, start)
        defs.append({
            "term": strip_md(start),
            "source": {"file": FOW_VII.relative_to(REPO).as_posix(), "line": n},
            "verbatim": raw,
        })

    n, raw = find_line(vii, "> **The efficiency conflict, unresolved.**")
    eta_conflict = {
        "summary": "Part Seventeen's Class I range and the Tier 5 efficiency row disagree; "
                   "flagged on the page itself and reproduced here, unresolved.",
        "source": {"file": FOW_VII.relative_to(REPO).as_posix(), "line": n},
        "verbatim": raw,
    }

    return {
        "grade_bands": grades,
        "stage_gates": stages,
        "eta_by_tier": etas,
        "definitions": defs,
        "eta_conflict": eta_conflict,
    }


# --- the hand supplement ---------------------------------------------------
# Figures the sweep could not take: a second number on a line that carries two,
# or a number written out in words. Each one is checked by eye against the page.
SUPPLEMENT = [
    {
        "entity": "Krothar Veylshroud", "kind": "eu_reserve", "value": 2_800_000,
        "qualifier": "unsuppressed (estimate); the suppressed figure ~1,600,000 is the swept row",
        "file": "wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md",
        "line": 99,
    },
    {
        "entity": "Krothar Veylshroud", "kind": "au_s", "value": 420_000,
        "qualifier": "active",
        "file": "wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md",
        "line": 100,
    },
    {
        "entity": "Krothar Veylshroud", "kind": "au_s", "value": 135_000,
        "qualifier": "passive, chains on",
        "file": "wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md",
        "line": 100,
    },
    {
        "entity": "Sodoku Moto (Arctic Lion, Level 500)", "kind": "au_s", "value": 16_250,
        "qualifier": "with Resonance Circuit; ~12,500 base is the swept row",
        "file": "wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md",
        "line": 17,
    },
    {
        "entity": "Wystan Ashmore", "kind": "flux_density", "value": 20,
        "qualifier": "stated as \"his Flux is 20\"; the card gives no EU/g unit and no AU/s figure",
        "file": "wiki/Volume I — Character Cards/Wystan Ashmore — Late Bell.md",
        "line": 64,
    },
    {
        "entity": "Kwon Hae-ryu", "kind": "eu_reserve", "value": 90_000_000,
        "qualifier": "ruled 2026-09-12; stated on Obrenkael's page, not on a card of his own",
        "file": "wiki/Summoned and Bound/Obrenkael · The Mule.md",
        "line": 75,
    },
]

# Costs the sweep steps over by design: the cost pattern refuses a figure
# written "EU per …", because that form is usually a rate. On The Iron Tree it
# is not a rate, it is the cost of one branch release, and it is half of the
# only EU-to-joule pairing canon states. Added by hand, quoting the line.
COST_SUPPLEMENT = [
    {
        "entity": "Dougou Ozumu Zettari", "value": 2_800,
        "qualifier": "low end of \"2,800 to 8,900 EU per branch\"",
        "file": "wiki/Spellcraft/The Iron Tree.md", "line": 20,
    },
    {
        "entity": "Dougou Ozumu Zettari", "value": 8_900,
        "qualifier": "high end of \"2,800 to 8,900 EU per branch\"",
        "file": "wiki/Spellcraft/The Iron Tree.md", "line": 20,
    },
]

# Figures the page itself withdraws in the same breath as it names them. They
# stay in the file with the quote that withdraws them and are not read as
# attestations. Found by sweeping for a withdrawal word beside a joule figure;
# one line in the corpus matches.
WITHDRAWN = [
    {
        "file": "wiki/Volume I — Character Cards/Serenyra Vaelith · The Archmagus of the Grove-Spired Crown.md",
        "line": 69, "kind": "joule",
        "why": "the line names the figure only to withdraw it: \"Not the 450 PJ the card claimed\"",
    },
]

# Figures canon says are absent, refused or unmeasured. Recorded so a later
# phase does not read the silence as an oversight.
UNQUANTIFIED = [
    ("Aurelian Prudentius Custos Clausorum · The Primate", "au_s",
     "wiki/Volume I — Character Cards/Aurelian Prudentius Custos Clausorum · The Primate.md", 86),
    ("Kinjiki, The Inversion", "flux_density",
     "wiki/Volume I — Character Cards/Kinjiki, The Inversion.md", 85),
    ("Kinjiki, The Inversion", "au_s",
     "wiki/Volume I — Character Cards/Kinjiki, The Inversion.md", 86),
    ("Cozbi Mahuo", "eu_reserve", "wiki/Volume I — Character Cards/Cozbi Mahuo.md", 92),
    ("Corwin Sesk", "all", "wiki/Volume I — Character Cards/Corwin Sesk.md", 45),
    ("Kaalabad", "all", "wiki/Volume I — Character Cards/Kaalabad.md", 51),
    ("Xanelor Rafiminar", "eu_reserve", "wiki/Volume I — Character Cards/Xanelor Rafiminar.md", 74),
    ("Xanelor Rafiminar", "all", "wiki/Volume I — Character Cards/Xanelor Rafiminar.md", 75),
    ("Akira Yukari", "all", "wiki/Volume I — Character Cards/Akira Yukari.md", 28),
    ("Kirishima Hae-jin — Kaalabad", "eu_reserve",
     "wiki/Volume I — Character Cards/Kirishima Hae-jin — Kaalabad, the Radiant God of Knights.md", 60),
    ("Valen Karth · The Breakstorm Vanguard", "flux_density",
     "wiki/Volume I — Character Cards/Valen Karth · The Breakstorm Vanguard.md", 36),
    ("Verinus VII · The Palatine", "au_s",
     "wiki/Volume I — Character Cards/Verinus VII · The Palatine.md", 87),
    ("Speculum Harmoniae", "au_s", "wiki/Techniques/Speculum Harmoniae.md", 49),
    ("Borin Ironheart", "eu_reserve",
     "wiki/Volume I — Character Cards/Borin Ironheart · The Master of the Soul Forge.md", 175),
]


# --- who the figure belongs to --------------------------------------------
# A figure's owner is read off the line, not off the page it sits on. Three
# pages state another practitioner's figure: The Iron Tree carries Dougou's
# reserve, Obrenkael's page carries Kwon Hae-ryu's, and the Open Crucible
# carries Kwon Mu-jin's. The rule is mechanical and its evidence is kept:
# the possessive name nearest before the figure in the same line wins; failing
# that, a possessive name in the page title; failing that, the page title.
POSSESSIVE = re.compile(r"\b(?P<name>(?:[A-ZŌŪĀĒĪ][\wÀ-ɏ'’-]*)(?:\s+[A-ZŌŪĀĒĪ][\wÀ-ɏ'’-]*){0,3})['’]s\b")
NEAR = 60  # characters between the possessive and the figure it governs


def roster() -> tuple[dict, dict]:
    """Every practitioner canon names on a card, plus the names the hand
    supplement already carries. Nothing else is a person: this is what keeps
    "Stage VIII's S-Grade ceiling" and "the Bloom's held force" from being read
    as owners. Card names come from the card file names, cut at the epithet."""
    names = {}
    for p in sorted((REPO / "wiki/Volume I — Character Cards").glob("*.md")):
        names[re.split(r" · | — |, the ", p.stem)[0].strip()] = None
    for s in SUPPLEMENT:
        names[s["entity"]] = None
    canon = {n: n for n in names}
    firsts: dict[str, list[str]] = {}
    for n in canon:
        firsts.setdefault(n.split()[0], []).append(n)
    # a given name is an alias only where exactly one card carries it
    alias = {k: v[0] for k, v in firsts.items() if len(v) == 1 and len(k) >= 4 and k not in canon}
    return canon, alias


CANON_NAMES, ALIASES = {}, {}


def person(name: str):
    return CANON_NAMES.get(name) or ALIASES.get(name)


PAGE_OWNER: dict[str, tuple[str, str] | None] = {}
# Pages about a working rather than about an entity.
WORKING_PAGES = ("wiki/Techniques/", "wiki/Spellcraft/", "wiki/Artifacts/",
                 "wiki/The Disciplines/", "wiki/Hataraki — The Works of the Plane of Fate/")


def page_owner(file: str):
    """A page about a *working* — a technique, a spellcraft system, an artifact
    — that names exactly one practitioner in the possessive belongs to that
    practitioner: The Iron Tree is Dougou's, Winter Rend is Draven's. Pages
    about an entity (a card, a summon, a beast) are never reattributed this
    way, since their figures are their own. Where a working's page names two
    practitioners, nothing is decided here and the page title stands."""
    if file in PAGE_OWNER:
        return PAGE_OWNER[file]
    result = None
    if file.startswith(WORKING_PAGES):
        text = (REPO / file).read_text(encoding="utf-8")
        found = {}
        for m in POSSESSIVE.finditer(text):
            p = person(m.group("name"))
            if p:
                found.setdefault(p, m.group(0))
        if len(found) == 1:
            (name, evidence), = found.items()
            result = (name, evidence)
    PAGE_OWNER[file] = result
    return result


def owner(verbatim: str, token, page_title: str, file: str | None = None) -> tuple[str, str, str | None]:
    """(entity, basis, evidence). Never invents a name: the name returned is
    written in the line or the title it is read from, and it is a name canon
    already carries on a card."""
    if token:
        at = verbatim.find(token)
        if at >= 0:
            best = None
            for m in POSSESSIVE.finditer(verbatim):
                if m.end() <= at and at - m.end() <= NEAR and person(m.group("name")):
                    best = m
            if best:
                return person(best.group("name")), "possessive in the line", best.group(0)
    for m in POSSESSIVE.finditer(page_title):
        if person(m.group("name")):
            return person(m.group("name")), "possessive in the page title", m.group(0)
    if file:
        po = page_owner(file)
        if po:
            return po[0], "the one practitioner the page names in the possessive", po[1]
    return page_title, "page title", None


# --- what a joule figure is ------------------------------------------------
# Part Eleven states that Strike Force and Durability are recorded in joules,
# so a card's joule figure is the measured side of the conversion. Two things
# have to be told apart, and the test is arithmetic rather than judgement:
#
#   system_table       the figure sits on one of the pages that define the
#                      ladder (Part Four, Part Eleven, Tier Grade Bands & the
#                      Aether Shell, the Apprentice's Primer's copy of it);
#   band_edge_quoted   the figure is within 2% of one of those pages' own
#                      figures, i.e. the line is citing the band, not measuring
#                      anything ("at the required SSS-Grade, 418 TJ to 4.184 EJ");
#   attested           neither: a figure the page states for itself.
#
# 2% is wide enough to catch Part Eleven's 46 GJ against Part Four's 4.6024×10^10
# and narrow enough to leave Dougou's 8–20 MJ clear of the 20.92 MJ D/C edge.
SYSTEM_PAGES = (
    "wiki/Fracture of Worlds — The Living System/",
    "wiki/The Magic System/",
    "wiki/In-World Documents & the Narrative Archive/The Apprentice's Primer",
)
EDGE_TOLERANCE = 0.02


def classify_joules(rows: list[dict]) -> None:
    system_values: list[tuple[float, dict]] = []
    for r in rows:
        r["figure_class"] = ("system_table" if r["source"]["file"].startswith(SYSTEM_PAGES)
                             else None)
        if r["figure_class"] == "system_table":
            for v in (r["value"], r["value_low"], r["value_high"]):
                if v:
                    system_values.append((v, r))

    def nearest(v):
        if not v or not system_values:
            return None, None
        sv, src = min(system_values, key=lambda s: abs(math.log10(s[0] / v)))
        return abs(sv - v) / max(sv, v), {"value": sv, "source": src["source"],
                                          "verbatim": src["verbatim"]}

    for r in rows:
        if r["figure_class"]:
            continue
        ends = [v for v in (r["value"], r["value_low"], r["value_high"]) if v]
        diffs = [nearest(v) for v in ends]
        if diffs and all(d is not None and d <= EDGE_TOLERANCE for d, _ in diffs):
            r["figure_class"] = "band_edge_quoted"
            r["nearest_system_figure"] = diffs[0][1]
        else:
            r["figure_class"] = "attested"
            d, near = diffs[0] if diffs else (None, None)
            r["nearest_system_figure"] = near
        r["distance_from_nearest_system_figure"] = diffs[0][0] if diffs else None


# Labels that name a field rather than a working. Everything else in a Cost
# column is the name of the technique the cost belongs to, which is what keeps
# Iron Kick's 6,200 EU and Iron Step's 6,200 EU apart.
GENERIC_LABELS = {"cost", "call cost", "essence cost", "numerical effect",
                  "consequence", "effect", "eu figures ruled", "upkeep",
                  "eu reserve", "essence capacity", "flux density", "strike force",
                  "durability", "crystal state", "η"}


def working(row: dict):
    """The name of the working a figure belongs to, or None where the label
    names a field instead."""
    lbl = (row.get("label") or "").strip()
    if not lbl:
        return None
    norm = re.sub(r"[^a-z0-9 ]", " ", lbl.lower())
    norm = re.sub(r"\s+", " ", norm).strip()
    return None if norm.strip(". ") in GENERIC_LABELS else norm


def mark_duplicates(rows: list[dict]) -> None:
    """One figure, counted once. A row restating a figure already recorded for
    the same entity keeps its place in the file and carries `duplicate_of`, so
    every attestation stays visible and the fit counts each figure once.

    A figure is a restatement when the entity, the kind and the value all match
    and the row does not name a *different* working. Two workings that happen to
    cost the same are two figures, not one, and collapsing them would assert
    they are the same working — which is not this file's call to make.
    `duplicate_of_value_only` records the stricter reading, entity and value
    alone, so the fit can be read both ways."""
    groups: dict[tuple, list[dict]] = {}
    strict: dict[tuple, dict] = {}
    for r in sorted(rows, key=lambda r: (r["source"]["file"], r["source"]["line"])):
        r["duplicate_of"] = None
        r["duplicate_of_value_only"] = None
        if r["value"] is None or r.get("figure_class") == "system_table":
            continue
        key = (r["entity"], r["kind"], round(r["value"], 6))
        first = strict.get(key)
        if first is None:
            strict[key] = r
        else:
            r["duplicate_of_value_only"] = dict(first["source"])
        seen = groups.setdefault(key, [])
        name = working(r)
        named = [s for s in seen if working(s)]
        if not seen:
            seen.append(r)
        elif name is None or not named or any(working(s) == name for s in named):
            r["duplicate_of"] = dict(seen[0]["source"])
        else:
            seen.append(r)


def quote(file: str, line: int) -> str:
    raw = lines_of(REPO / file)
    if not 1 <= line <= len(raw):
        raise SystemExit(f"{file}:{line} is out of range")
    return raw[line - 1]


def main() -> int:
    global CANON_NAMES, ALIASES
    CANON_NAMES, ALIASES = roster()
    if not CANDIDATES.exists():
        raise SystemExit("run extract_anchors.py first")
    swept = json.loads(CANDIDATES.read_text(encoding="utf-8"))

    # One `pages` entry per source page holds what that page states about its
    # own practitioner, so an anchor row carries the figure and a file reference
    # rather than a copy of the card.
    pages: dict[str, dict] = {}
    anchors, costs, joules = [], [], []
    for r in swept:
        ctx = r["context"]
        if r["file"] not in pages:
            pages[r["file"]] = {
                "page_title": r["page_title"],
                "level": ctx["level"],
                "temperance_stage": ctx["temperance_stage"],
                "tier_of_standing": ctx["tier_of_standing"],
                "aether_class": ctx["aether_class"],
                "coherence_band": ctx["coherence_band"],
                "level_band": ctx["level_band"],
                "stated_grade": ctx["stated_grade"],
                "tier_grades": ctx["tier_grades"] or None,
                "context_lines": ctx["context_lines"],
            }
        entity, basis, evidence = owner(r["verbatim"], r["token"], r["page_title"], r["file"])
        row = {
            "entity": entity,
            "entity_basis": basis,
            "entity_evidence": evidence,
            "page_title": r["page_title"],
            "kind": r["kind"],
            "token": r["token"],
            "label": r.get("label"),
            "value": r["value"],
            "value_low": r["low"],
            "value_high": r["high"],
            "unit": {"eu_reserve": "EU", "eu_cost": "EU", "flux_density": "EU/g",
                     "au_s": "AU/s", "eta": None, "joule": "J"}[r["kind"]],
            "qualifier": None,
            "origin": "swept",
            "source": {"file": r["file"], "line": r["line"]},
            "verbatim": r["verbatim"],
        }
        if r["kind"] == "joule":
            joules.append(row)
        elif r["kind"] == "eu_cost":
            costs.append(row)
        else:
            anchors.append(row)

    for s in SUPPLEMENT:
        anchors.append({
            "entity": s["entity"],
            "entity_basis": "hand supplement",
            "entity_evidence": None,
            "page_title": None,
            "kind": s["kind"],
            "token": None,
            "label": None,
            "value": s["value"],
            "value_low": None,
            "value_high": None,
            "unit": {"eu_reserve": "EU", "flux_density": "EU/g", "au_s": "AU/s"}[s["kind"]],
            "qualifier": s["qualifier"],
            "origin": "hand",
            "source": {"file": s["file"], "line": s["line"]},
            "verbatim": quote(s["file"], s["line"]),
        })

    for s in COST_SUPPLEMENT:
        costs.append({
            "entity": s["entity"],
            "entity_basis": "hand supplement",
            "entity_evidence": None,
            "page_title": None,
            "kind": "eu_cost",
            "token": None,
            "label": "Cost",
            "value": s["value"],
            "value_low": None,
            "value_high": None,
            "unit": "EU",
            "qualifier": s["qualifier"],
            "origin": "hand",
            "source": {"file": s["file"], "line": s["line"]},
            "verbatim": quote(s["file"], s["line"]),
        })

    unquantified = [
        {"entity": e, "kind": k, "source": {"file": f, "line": n}, "verbatim": quote(f, n)}
        for e, k, f, n in UNQUANTIFIED
    ]

    classify_joules(joules)
    for w in WITHDRAWN:
        hit = [r for r in joules
               if r["source"]["file"] == w["file"] and r["source"]["line"] == w["line"]]
        if not hit:
            raise SystemExit(f"withdrawn figure not found in the sweep: {w['file']}:{w['line']}")
        for r in hit:
            r["figure_class"] = "withdrawn"
            r["withdrawn_because"] = w["why"]
    mark_duplicates(anchors)
    mark_duplicates(costs)
    mark_duplicates(joules)

    doc = {
        "meta": {
            "issue": "WAR-9",
            "phase": "Essence Ledger Phase 1 — collect and fit",
            "date": "2026-09-24",
            "corpus": "wiki/ (the Notion mirror), swept whole",
            "method": (
                "extract_anchors.py sweeps every wiki page for a figure carrying one of the "
                "four essence units, then build_anchors.py adds the system tables verbatim and "
                "a short hand supplement. No figure here is computed, rounded or inferred: each "
                "row quotes the whole line it came from, with file and line. Where a page "
                "states that a figure does not exist, the row is in `unquantified` rather than "
                "filled in."
            ),
            "caveats": [
                "`joules` holds the measured side of the conversion: every joule figure in "
                "the mirror, with `figure_class` saying which kind it is — `system_table` "
                "(the figure is part of a Grade ladder), `band_edge_quoted` (within 2% of a "
                "ladder figure, so the line cites the band rather than measuring) or "
                "`attested` (the page states it for itself). Part Eleven:30 defines the "
                "quantity: Strike Force is recorded in Newtons and Joules. A card's Strike "
                "Force and Durability rows are therefore the quantity Part Four grades.",
                "`entity` is read off the line, not off the page: the possessive name "
                "nearest before the figure in the same line wins, then a possessive in the "
                "page title, then the page title itself. `entity_basis` and "
                "`entity_evidence` carry which rule fired and the words it fired on. This "
                "is why The Iron Tree's reserve rows say Dougou, Obrenkael's ruling line "
                "says Kwon Hae-ryu and the Open Crucible's cost row says Kwon Mu-jin.",
                "`duplicate_of` marks a row restating a figure already recorded for the "
                "same entity — same entity, same kind, same value. Every attestation stays "
                "in the file; the fit counts each figure once. Two figures for one "
                "character that differ (Krothar suppressed and unsuppressed, Sodoku's card "
                "and his Level 500 configuration) are not duplicates and are not marked.",
                "An anchor's `source.file` is the key into `pages`, which holds what that page "
                "states about its own practitioner. `pages` fields are read from labelled card "
                "fields only: a Stage named in prose, or a Grade from a stat row, is left null "
                "rather than guessed, and `context_lines` quotes the field lines for audit.",
                "`costs` holds absolute EU costs (technique, call, domain upkeep). Where a line "
                "gives a cost range only one end is captured; the verbatim line carries both.",
                "Several cards name a Stage whose name disagrees with FoW Part Five "
                "(Naiser 'Stage 6 — Realization', Vethraun 'Stage 10, Dominion', "
                "Gimbzo 'XII — Zenith'). Recorded as written, not corrected here.",
                "`stated.coherence_band` comes from a mirror that pre-dates the C-033 sweep. "
                "That sweep (ruled 2026-09-24, R43-4) replaced the retired lettered Coherence "
                "Band with the Tier of Standing in Notion; the wiki mirror re-exports on the "
                "hourly sync, so 248 lines here still carry the retired field. The field is "
                "kept because it is what the mirror says, not because it is current.",
                "The 'Band V' in 'a fifth of a Band V reserve' (Raga) and 'low for Band V' "
                "(Verinus VII) is the Level Band of FoW Part One, Levels 401–500, Absolute — "
                "which is live and was never retired. It is not the lettered Coherence Band.",
            ],
        },
        "system": system_tables(),
        "pages": pages,
        "anchors": anchors,
        "costs": costs,
        "joules": joules,
        "unquantified": unquantified,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by_kind: dict[str, int] = {}
    for a in anchors:
        by_kind[a["kind"]] = by_kind.get(a["kind"], 0) + 1
    print(f"{OUT.relative_to(REPO)}")
    print(f"  anchors       {len(anchors)}  " + "  ".join(f"{k}={v}" for k, v in sorted(by_kind.items())))
    print(f"  costs         {len(costs)}")
    jclass: dict[str, int] = {}
    for j in joules:
        jclass[j["figure_class"]] = jclass.get(j["figure_class"], 0) + 1
    print(f"  joules        {len(joules)}  " + "  ".join(f"{k}={v}" for k, v in sorted(jclass.items())))
    dups = sum(1 for r in anchors + costs + joules if r.get("duplicate_of"))
    print(f"  duplicates    {dups} rows restate a figure already recorded")
    print(f"  unquantified  {len(unquantified)}")
    print(f"  grade bands   {len(doc['system']['grade_bands'])}")
    print(f"  stage gates   {len(doc['system']['stage_gates'])}")
    print(f"  eta tiers     {len(doc['system']['eta_by_tier'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
