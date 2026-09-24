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


def quote(file: str, line: int) -> str:
    raw = lines_of(REPO / file)
    if not 1 <= line <= len(raw):
        raise SystemExit(f"{file}:{line} is out of range")
    return raw[line - 1]


def main() -> int:
    if not CANDIDATES.exists():
        raise SystemExit("run extract_anchors.py first")
    swept = json.loads(CANDIDATES.read_text(encoding="utf-8"))

    # One `pages` entry per source page holds what that page states about its
    # own practitioner, so an anchor row carries the figure and a file reference
    # rather than a copy of the card.
    pages: dict[str, dict] = {}
    anchors, costs = [], []
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
        row = {
            "entity": r["page_title"],
            "kind": r["kind"],
            "token": r["token"],
            "value": r["value"],
            "value_low": r["low"],
            "value_high": r["high"],
            "unit": {"eu_reserve": "EU", "eu_cost": "EU", "flux_density": "EU/g",
                     "au_s": "AU/s", "eta": None}[r["kind"]],
            "qualifier": None,
            "origin": "swept",
            "source": {"file": r["file"], "line": r["line"]},
            "verbatim": r["verbatim"],
        }
        (costs if r["kind"] == "eu_cost" else anchors).append(row)

    for s in SUPPLEMENT:
        anchors.append({
            "entity": s["entity"],
            "kind": s["kind"],
            "token": None,
            "value": s["value"],
            "value_low": None,
            "value_high": None,
            "unit": {"eu_reserve": "EU", "flux_density": "EU/g", "au_s": "AU/s"}[s["kind"]],
            "qualifier": s["qualifier"],
            "origin": "hand",
            "source": {"file": s["file"], "line": s["line"]},
            "verbatim": quote(s["file"], s["line"]),
        })

    unquantified = [
        {"entity": e, "kind": k, "source": {"file": f, "line": n}, "verbatim": quote(f, n)}
        for e, k, f, n in UNQUANTIFIED
    ]

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
        "unquantified": unquantified,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by_kind: dict[str, int] = {}
    for a in anchors:
        by_kind[a["kind"]] = by_kind.get(a["kind"], 0) + 1
    print(f"{OUT.relative_to(REPO)}")
    print(f"  anchors       {len(anchors)}  " + "  ".join(f"{k}={v}" for k, v in sorted(by_kind.items())))
    print(f"  costs         {len(costs)}")
    print(f"  unquantified  {len(unquantified)}")
    print(f"  grade bands   {len(doc['system']['grade_bands'])}")
    print(f"  stage gates   {len(doc['system']['stage_gates'])}")
    print(f"  eta tiers     {len(doc['system']['eta_by_tier'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
