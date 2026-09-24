#!/usr/bin/env python3
"""WAR-9, step 2 — fit the EU→joule constant against the collected anchors.

Isaac's conversion to test is **1 EU = 1 MJ of potential**, with energy
delivered = EU × η, so 1 AU/s = 1 MW.

The conversion has two sides and both are read here.

**The measured side.** Part Eleven records Strike Force and Durability in
joules, so a card's joule figure is the quantity Part Four grades, attested
rather than inferred. Three tests use it, and they come first because where a
page states the joules outright the page outranks any proxy:

*   `direct_pairs`    — a working whose EU cost and joule output are both
    stated. This is the conversion itself, measured, with nothing in between.
*   `grade_proxy_check` — every attested joule figure read against the Grade
    the proxy below would have assigned it. This is the proxy's own error bar.
*   `reserve_vs_strike` — for a character with both a reserve and an attested
    strike, the joules per EU that would hold if one strike spent the whole
    reserve. An upper bound per character, and its spread across characters.

**The proxy.** Where no joule figure is stated — which is most of the corpus —
the test asks whether an EU figure, converted and read through η, lands in the
joule band the page's own Grade claims in Part Four. Nothing here edits a card.
Two families of figure are tested separately, because Part Four measures
**attack output**, not stored volume:

*   `cost`  — an absolute EU spend for one working. This is the family Isaac's
    own sanity check uses (Iron Fist, 4,800 EU → about 4.8 GJ → B, "Building").
*   `reserve` — the whole stored pool. Tested as well, and reported apart,
    since a reserve is not a strike.

"Their stated Grade" reads three ways and the test is run under each:
`stage_max`, Part Five's Max Grade for the Stage the page states, the only Grade
nearly every page supplies and the default for the per-anchor tables below;
`card_stated`, a Grade the card writes on its own Stage or Ceiling line; and
`peak_primary`, the highest Primary Grade in the card's stat table, since Part
Four says the fight is decided by the peak.

Residual is reported in **decades** — log10 of how far outside its band a figure
falls, 0.0 meaning inside. The fitted constant is the k that puts the most
figures in band, and among those the k with the smallest sum of squared decades.

Each figure is counted once. A row that restates a figure already recorded for
the same entity carries `duplicate_of` in `anchors.json` and is left out of
every count here; `dedupe` in the report says how many rows that dropped and
what the stricter reading (entity and value alone, ignoring which working is
named) would have dropped instead.

    python imports/essence-ledger/fit.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ANCHORS = HERE / "anchors.json"
REPORT = HERE / "fit.json"

ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
          "XI", "XII", "XIII", "XIV", "XV", "XVI"]
K_TEST = 1e6  # joules per EU — Isaac's 1 EU = 1 MJ


def stage_number(stated) -> int | None:
    if not stated:
        return None
    s = str(stated).strip()
    if s in ROMANS:
        return ROMANS.index(s) + 1
    if s.isdigit() and 1 <= int(s) <= 16:
        return int(s)
    return None


def decades_outside(value: float, lo, hi) -> float:
    if lo is not None and value < lo:
        return -math.log10(lo / value)
    if hi is not None and value > hi:
        return math.log10(value / hi)
    return 0.0


def main() -> int:
    doc = json.loads(ANCHORS.read_text(encoding="utf-8"))
    system = doc["system"]

    grade_band = {g["grade"]: (g["attack_output_j_low"], g["attack_output_j_high"])
                  for g in system["grade_bands"]}

    stage_grade, stage_tier = {}, {}
    for s in system["stage_gates"]:
        n = stage_number(s["stage"])
        if n is None:
            continue
        m = re.match(r"(Hollow|SSS|SS|S|EX\+|EX|X|A|B|C|D|E|F)\b", s["max_grade"])
        stage_grade[n] = m.group(1) if m else None
        t = re.match(r"([0-9])", s["tier_of_standing"])
        stage_tier[n] = int(t.group(1)) if t else None

    tier_eta = {}
    for e in system["eta_by_tier"]:
        t = re.match(r"([0-9])", e["tier"])
        if t and e["eta_low"] is not None:
            tier_eta[int(t.group(1))] = (e["eta_low"], e["eta_high"])

    # η as each page states it. A page can state it more than once (a Tier range
    # in the architecture block, an exact figure on the flow line); the one
    # nearest the figure being read wins, since that is the one written beside it.
    etas_by_file: dict[str, list[dict]] = {}
    for a in doc["anchors"]:
        if a["kind"] != "eta":
            continue
        v = a["value"] if a["value"] is not None else (
            (a["value_low"] + a["value_high"]) / 2
            if a["value_low"] is not None and a["value_high"] is not None else None)
        if v is not None:
            etas_by_file.setdefault(a["source"]["file"], []).append(
                {"eta": v, "line": a["source"]["line"], "verbatim": a["verbatim"]})

    def eta_near(file: str, line: int):
        opts = etas_by_file.get(file)
        if not opts:
            return None
        return min(opts, key=lambda e: abs(e["line"] - line))

    stated_eta = {f: v[0] for f, v in etas_by_file.items()}

    # what each page states about its own practitioner, keyed by file
    pages = doc["pages"]

    def stated(a) -> dict:
        return pages.get(a["source"]["file"], {})

    # peak Primary Grade where the page's stat table parsed
    order = [g["grade"] for g in system["grade_bands"]]
    peak_grade: dict[str, str] = {}
    for f, page in pages.items():
        if page.get("tier_grades"):
            peak_grade[f] = max((r["grade"] for r in page["tier_grades"]),
                                key=lambda g: order.index(g) if g in order else -1)

    def build(rows, family, reading="stage_max"):
        out = []
        for a in rows:
            if a["value"] is None:
                continue
            f = a["source"]["file"]
            n = stage_number(stated(a).get("temperance_stage"))
            if reading == "stage_max":
                grade = stage_grade.get(n) if n else None
            elif reading == "card_stated":
                grade = stated(a).get("stated_grade")
            else:
                grade = peak_grade.get(f)
            if grade is None or grade not in grade_band:
                out.append({**base(a, family), "stage": n, "grade": None,
                            "grade_reading": reading,
                            "skipped": "no Grade available for this reading"})
                continue
            se = eta_near(f, a["source"]["line"])
            if se:
                eta, eta_from = se["eta"], f"page, line {se['line']}"
            else:
                rng = tier_eta.get(stage_tier.get(n))
                if not rng:
                    out.append({**base(a, family), "stage": n, "grade": grade,
                                "skipped": "no η on the page and none for the Stage's Tier"})
                    continue
                eta = (rng[0] + rng[1]) / 2
                eta_from = f"Part Nineteen, Tier {stage_tier[n]} midpoint"
            lo, hi = grade_band[grade]
            # the k that would land this figure on its band's geometric centre —
            # the spread of these across anchors is the whole question
            mid = (math.sqrt(lo * hi) if lo and hi else (lo or hi))
            row = {
                **base(a, family),
                "stage": n,
                "grade": grade,
                "grade_reading": reading,
                "peak_primary_grade": peak_grade.get(f),
                "card_stated_grade": stated(a).get("stated_grade"),
                "eta": eta,
                "eta_from": eta_from,
                "band_j_low": lo,
                "band_j_high": hi,
                "potential_j_at_1MJ": a["value"] * K_TEST,
                "delivered_j_at_1MJ": a["value"] * eta * K_TEST,
                "k_required_j_per_eu": mid / (a["value"] * eta),
                "skipped": None,
            }
            row["decades_potential"] = decades_outside(row["potential_j_at_1MJ"], lo, hi)
            row["decades_delivered"] = decades_outside(row["delivered_j_at_1MJ"], lo, hi)
            out.append(row)
        return out

    def base(a, family):
        return {
            "family": family,
            "entity": a["entity"],
            "kind": a["kind"],
            "eu": a["value"],
            "source": a["source"],
            "verbatim": a["verbatim"],
        }

    # Each figure once. `duplicate_of` marks a row restating a figure already
    # recorded for the same entity; the stricter reading ignores which working
    # a cost names, and both counts are reported.
    def distinct(rows, strict=False):
        field = "duplicate_of_value_only" if strict else "duplicate_of"
        return [r for r in rows if not r.get(field)]

    raw_reserves = distinct([a for a in doc["anchors"] if a["kind"] == "eu_reserve"])
    raw_costs = distinct(doc["costs"])
    dedupe = {
        "note": ("one figure counted once. `duplicate_of` in anchors.json marks the rows "
                 "left out; every attestation stays in that file."),
        "reserves": {"rows": len([a for a in doc["anchors"] if a["kind"] == "eu_reserve"]),
                     "distinct": len(raw_reserves),
                     "distinct_strict": len(distinct([a for a in doc["anchors"]
                                                      if a["kind"] == "eu_reserve"], True))},
        "costs": {"rows": len(doc["costs"]), "distinct": len(raw_costs),
                  "distinct_strict": len(distinct(doc["costs"], True))},
        "kept_apart_because_they_name_different_workings": [
            {"entity": r["entity"], "eu": r["value"], "names": r["label"],
             "source": r["source"], "verbatim": r["verbatim"],
             "same_value_recorded_at": r["duplicate_of_value_only"]}
            for r in doc["costs"] if r.get("duplicate_of_value_only") and not r.get("duplicate_of")
        ],
    }
    readings = {}
    for reading in ("stage_max", "card_stated", "peak_primary"):
        readings[reading] = {
            "reserves": build(raw_reserves, "reserve", reading),
            "costs": build(raw_costs, "cost", reading),
        }
    reserves = readings["stage_max"]["reserves"]
    costs = readings["stage_max"]["costs"]
    tested = [r for r in reserves + costs if not r["skipped"]]

    # --- fit k -------------------------------------------------------------
    # log10(delivered) = log10(EU·η) + log10(k), so the fit is a shift on a log
    # axis. Scanned at 0.01-decade steps from 1 J to 1e12 J per EU.
    def score(logk, rows):
        inband = 0
        sq = 0.0
        for r in rows:
            v = r["eu"] * r["eta"] * (10 ** logk)
            d = decades_outside(v, r["band_j_low"], r["band_j_high"])
            if d == 0.0:
                inband += 1
            sq += d * d
        return inband, sq

    def fit(rows):
        if not rows:
            return None
        best = None
        lk = 0.0
        while lk <= 12.0:
            inband, sq = score(lk, rows)
            key = (-inband, sq)
            if best is None or key < best[0]:
                best = (key, lk, inband, sq)
            lk = round(lk + 0.01, 2)
        _, lk, inband, sq = best
        return {"k_j_per_eu": 10 ** lk, "log10_k": lk, "in_band": inband,
                "of": len(rows), "sum_sq_decades": sq}

    def spread(rows):
        """How far apart the anchors' own required constants sit, in decades."""
        ks = sorted(r["k_required_j_per_eu"] for r in rows)
        if not ks:
            return None
        return {
            "n": len(ks),
            "k_min": ks[0], "k_max": ks[-1],
            "k_median": ks[len(ks) // 2],
            "decades_spanned": math.log10(ks[-1] / ks[0]),
        }

    fits = {
        "costs_only": fit([r for r in costs if not r["skipped"]]),
        "reserves_only": fit([r for r in reserves if not r["skipped"]]),
        "all": fit(tested),
    }
    by_reading = {}
    for reading, sets in readings.items():
        rows = [r for r in sets["reserves"] + sets["costs"] if not r["skipped"]]
        by_reading[reading] = {
            "tested": len(rows),
            "in_band_at_1MJ": sum(1 for r in rows if r["decades_delivered"] == 0.0),
            "best_fit": fit(rows),
            "required_k_spread": spread(rows),
        }
    by_stage: dict[str, dict] = {}
    for r in tested:
        s = by_stage.setdefault(str(r["stage"]), {"n": 0, "sum": 0.0, "ks": []})
        s["n"] += 1
        s["sum"] += r["decades_delivered"]
        s["ks"].append(r["k_required_j_per_eu"])
    for s in by_stage.values():
        s["mean_decades_at_1MJ"] = s.pop("sum") / s["n"]
        ks = sorted(s.pop("ks"))
        s["median_required_k"] = ks[len(ks) // 2]
    at_1mj = {
        name: {
            "in_band_delivered": sum(1 for r in rows if r["decades_delivered"] == 0.0),
            "in_band_potential": sum(1 for r in rows if r["decades_potential"] == 0.0),
            "of": len(rows),
            "sum_sq_decades_delivered": sum(r["decades_delivered"] ** 2 for r in rows),
            "median_decades_delivered": sorted(r["decades_delivered"] for r in rows)[len(rows) // 2] if rows else None,
        }
        for name, rows in (("costs_only", [r for r in costs if not r["skipped"]]),
                           ("reserves_only", [r for r in reserves if not r["skipped"]]),
                           ("all", tested))
    }

    # --- the measured side: canon's own joule figures -----------------------
    # Part Eleven:30 states the quantity. A card's Strike Force row is what
    # Part Four grades, so where a page gives joules the page is read directly
    # and the Stage→Grade proxy is not consulted.
    grade_order = [g["grade"] for g in system["grade_bands"]]

    def grade_of(j):
        """The Grade whose attack-output band holds a figure, as Part Four
        writes it. `None` where a figure falls in the S/SS gap C-036 records."""
        if j is None:
            return None
        for g in system["grade_bands"]:
            lo, hi = g["attack_output_j_low"], g["attack_output_j_high"]
            if (lo is None or j >= lo) and (hi is None or j <= hi):
                return g["grade"]
        return None

    def measure_of(label):
        low = (label or "").lower()
        if low.startswith(("strike force", "strike energy")):
            return "strike"
        if low.startswith("durability"):
            return "durability"
        return "other"

    measured = [j for j in doc["joules"]
                if j["figure_class"] == "attested" and not j.get("duplicate_of")]

    def jfig(j):
        """(low, high) of a joule row; a single figure is both."""
        if j["value"] is not None:
            return j["value"], j["value"]
        return j["value_low"], j["value_high"]

    proxy_check = []
    for j in measured:
        f = j["source"]["file"]
        lo, hi = jfig(j)
        n = stage_number(pages.get(f, {}).get("temperance_stage"))
        proxy = stage_grade.get(n) if n else None
        attested_hi, attested_lo = grade_of(hi), grade_of(lo)
        steps = None
        if proxy in grade_order and attested_hi in grade_order:
            steps = grade_order.index(attested_hi) - grade_order.index(proxy)
        proxy_check.append({
            "entity": j["entity"],
            "measure": measure_of(j["label"]),
            "label": j["label"],
            "joules_low": lo, "joules_high": hi,
            "grade_attested_low": attested_lo,
            "grade_attested_high": attested_hi,
            "stage": n,
            "grade_from_stage_proxy": proxy,
            "card_stated_grade": pages.get(f, {}).get("stated_grade"),
            "peak_primary_grade": peak_grade.get(f),
            "grades_apart": steps,
            "source": j["source"],
            "verbatim": j["verbatim"],
        })
    strikes = [p for p in proxy_check if p["measure"] == "strike" and p["grades_apart"] is not None]
    proxy_summary = {
        "note": ("every attested joule figure read against the Grade the Stage→Part Five→"
                 "Part Four proxy would have assigned it. 0 means the proxy agrees; a "
                 "positive number means the page states an output that many Grades above "
                 "what the proxy assigns, negative that many below. This is the error the "
                 "per-anchor residuals in `reserves` and `costs` inherit before any "
                 "constant is tested."),
        "strike_rows": len(strikes),
        "agree": sum(1 for p in strikes if p["grades_apart"] == 0),
        "mean_grades_apart": (sum(p["grades_apart"] for p in strikes) / len(strikes)
                              if strikes else None),
        "mean_abs_grades_apart": (sum(abs(p["grades_apart"]) for p in strikes) / len(strikes)
                                  if strikes else None),
        "distribution": {},
    }
    for p in strikes:
        k = str(p["grades_apart"])
        proxy_summary["distribution"][k] = proxy_summary["distribution"].get(k, 0) + 1

    # --- direct pairs: one working, an EU cost and a joule output ------------
    # Mechanical first: a cost and a joule figure written on the same line.
    # Then the hand pairs, where the page states the two a few lines apart and
    # names the working in both. Each hand pair carries both quotes; nothing is
    # paired that the page does not put together itself.
    HAND_PAIRS = [
        {
            "why": ("The Iron Tree's apex. The cost line names Kokushin Gyūha and its EU "
                    "figure; the Numerical Effect line gives the output 'at apex'; the "
                    "technique table calls Kokushin Gyūha the 'Apex fruit of the whole system'."),
            "cost": ("wiki/Spellcraft/The Iron Tree.md", 20, 7400),
            "joule": ("wiki/Spellcraft/The Iron Tree.md", 41, None),
            "which_joule": "8 to 20 MJ",
        },
        {
            "why": ("The Iron Tree's branches. Both figures are on the page as ranges for "
                    "the same set of releases: 2,800 to 8,900 EU per branch, and branch "
                    "outputs in the 1 to 10 MJ range."),
            "cost": ("wiki/Spellcraft/The Iron Tree.md", 20, 2800),
            "cost_high": ("wiki/Spellcraft/The Iron Tree.md", 20, 8900),
            "joule": ("wiki/Spellcraft/The Iron Tree.md", 41, None),
            "which_joule": "1 to 10 MJ",
        },
    ]

    def find_row(rows, file, line, value=None, token=None):
        for r in rows:
            if r["source"]["file"] != file or r["source"]["line"] != line:
                continue
            if value is not None and r["value"] != value:
                continue
            if token is not None and r["token"] != token:
                continue
            return r
        return None

    def make_pair(cost, joule, basis, why=None, cost_high=None):
        """One working's EU cost against its joule output. Where either side is
        a range the envelope is taken: the least joules per EU the two ranges
        allow, and the most."""
        lo, hi = jfig(joule)
        eu_lo = cost["value"]
        eu_hi = cost_high["value"] if cost_high else cost["value"]
        eta = eta_near(cost["source"]["file"], cost["source"]["line"])
        e = eta["eta"] if eta else None
        return {
            "entity": cost["entity"],
            "working": cost["label"] or joule["label"],
            "basis": basis,
            "why": why,
            "eu": eu_lo if eu_lo == eu_hi else None,
            "eu_low": eu_lo, "eu_high": eu_hi,
            "joules_low": lo, "joules_high": hi,
            "j_per_eu_low": (lo / eu_hi) if lo and eu_hi else None,
            "j_per_eu_high": (hi / eu_lo) if hi and eu_lo else None,
            "eta": e,
            "j_per_eu_through_eta_low": (lo / (eu_hi * e)) if lo and e and eu_hi else None,
            "j_per_eu_through_eta_high": (hi / (eu_lo * e)) if hi and e and eu_lo else None,
            "joules_at_1MJ_low": eu_lo * K_TEST, "joules_at_1MJ_high": eu_hi * K_TEST,
            # how far 1 EU = 1 MJ overshoots what the page states, in decades
            "decades_from_1MJ_least": (math.log10(eu_lo * K_TEST / hi) if hi and eu_lo else None),
            "decades_from_1MJ_most": (math.log10(eu_hi * K_TEST / lo) if lo and eu_hi else None),
            "cost_source": cost["source"], "cost_verbatim": cost["verbatim"],
            "cost_high_source": cost_high["source"] if cost_high else None,
            "joule_source": joule["source"], "joule_verbatim": joule["verbatim"],
        }

    joules_by_line: dict[tuple, list] = {}
    for j in doc["joules"]:
        if j["figure_class"] in ("system_table", "withdrawn"):
            continue
        joules_by_line.setdefault((j["source"]["file"], j["source"]["line"]), []).append(j)
    direct_pairs = []
    for c in raw_costs:
        for j in joules_by_line.get((c["source"]["file"], c["source"]["line"]), []):
            direct_pairs.append(make_pair(c, j, "the EU cost and the joule output are written on one line"))
    for hp in HAND_PAIRS:
        c = find_row(doc["costs"], hp["cost"][0], hp["cost"][1], value=hp["cost"][2])
        j = find_row(doc["joules"], hp["joule"][0], hp["joule"][1], token=hp["which_joule"])
        ch = (find_row(doc["costs"], *hp["cost_high"][:2], value=hp["cost_high"][2])
              if hp.get("cost_high") else None)
        if not c or not j or (hp.get("cost_high") and not ch):
            raise SystemExit(f"hand pair not found in the data: {hp['why'][:40]}")
        direct_pairs.append(make_pair(c, j, "stated a few lines apart on one page",
                                      hp["why"], ch))

    # --- reserve against attested strike ------------------------------------
    strike_by_entity: dict[str, dict] = {}
    for p in proxy_check:
        if p["measure"] != "strike" or not p["joules_high"]:
            continue
        cur = strike_by_entity.get(p["entity"])
        if cur is None or p["joules_high"] > cur["joules_high"]:
            strike_by_entity[p["entity"]] = p
    reserve_vs_strike = []
    for r in raw_reserves:
        s = strike_by_entity.get(r["entity"])
        if not s or not r["value"]:
            continue
        eta = eta_near(r["source"]["file"], r["source"]["line"])
        e = eta["eta"] if eta else None
        reserve_vs_strike.append({
            "entity": r["entity"],
            "reserve_eu": r["value"],
            "strike_joules": s["joules_high"],
            "j_per_eu_if_one_strike_spent_the_whole_reserve": s["joules_high"] / r["value"],
            "eta": e,
            "j_per_eu_through_eta": (s["joules_high"] / (r["value"] * e)) if e else None,
            "strikes_the_reserve_holds_at_1MJ": (r["value"] * K_TEST) / s["joules_high"],
            "reserve_source": r["source"], "reserve_verbatim": r["verbatim"],
            "strike_source": s["source"], "strike_verbatim": s["verbatim"],
        })
    rvs_ratios = sorted(x["j_per_eu_if_one_strike_spent_the_whole_reserve"]
                        for x in reserve_vs_strike)
    reserve_vs_strike_spread = {
        "note": ("a strike is not a reserve, so this is a ceiling, not the conversion: no "
                 "single strike can deliver more than the pool it draws on. Read that way "
                 "each character sets an upper bound on joules per EU, and the bounds do "
                 "not agree with each other."),
        "n": len(rvs_ratios),
        "min": rvs_ratios[0] if rvs_ratios else None,
        "max": rvs_ratios[-1] if rvs_ratios else None,
        "median": rvs_ratios[len(rvs_ratios) // 2] if rvs_ratios else None,
        "decades_spanned": (math.log10(rvs_ratios[-1] / rvs_ratios[0])
                            if rvs_ratios and rvs_ratios[0] else None),
    }

    # --- which Stage XIV row the proxy reads --------------------------------
    stage_xiv = next((s for s in system["stage_gates"] if s["stage"] == "XIV"), None)
    pe = REPO / "wiki/Fracture of Worlds — The Living System/III. Physical Force (Part Eleven).md"
    pe_lines = pe.read_text(encoding="utf-8").splitlines()
    zenith = next(((i + 1, l) for i, l in enumerate(pe_lines) if l.startswith("| Zenith |")), None)
    stage_xiv_reading = {
        "read": "Part Five's Stage gate table: Stage XIV, Zenith, Max Grade EX.",
        "why": ("the proxy reads a Stage's Max Grade off Part Five for every Stage, and "
                "Part Five gives XIV a Max Grade like every other row. Part Eleven's "
                "benchmark table does not: its Zenith row declines to give a figure. The "
                "two are not reconciled here. Declining to quantify is not a second figure, "
                "so this is recorded rather than filed as a conflict — but the fit's worst "
                "residual, the Primate at Stage XIV, rests on reading EX, and a reader who "
                "takes Part Eleven's row instead has no band to read him against at all."),
        "part_five": {"source": stage_xiv["source"] if stage_xiv else None,
                      "verbatim": stage_xiv["verbatim"] if stage_xiv else None},
        "part_eleven": ({"source": {"file": pe.relative_to(REPO).as_posix(), "line": zenith[0]},
                         "verbatim": zenith[1]} if zenith else None),
    }

    # --- the AU/s = Flux Density × η check ---------------------------------
    by_file: dict[str, dict] = {}
    for a in doc["anchors"]:
        f = a["source"]["file"]
        slot = by_file.setdefault(f, {"entity": a["entity"]})
        if a["kind"] in ("au_s", "flux_density") and a["value"] is not None:
            slot.setdefault(a["kind"], a)
    formula = []
    for f, slot in sorted(by_file.items()):
        if "au_s" not in slot or "flux_density" not in slot:
            continue
        se = eta_near(f, slot["au_s"]["source"]["line"])
        if not se:
            continue
        flux, au = slot["flux_density"]["value"], slot["au_s"]["value"]
        eta = se["eta"]
        expected = flux * eta
        formula.append({
            "entity": slot["entity"],
            "flux_density": flux,
            "eta": eta,
            "expected_au_s": expected,
            "stated_au_s": au,
            "ratio_stated_over_expected": au / expected if expected else None,
            "holds": abs(au - expected) <= 0.005 * max(au, expected),
            "flux_source": slot["flux_density"]["source"],
            "au_s_source": slot["au_s"]["source"],
            "eta_line": se["line"],
            "flux_verbatim": slot["flux_density"]["verbatim"],
            "au_s_verbatim": slot["au_s"]["verbatim"],
            "eta_verbatim": se["verbatim"],
        })

    report = {
        "meta": {
            "issue": "WAR-9",
            "conversion_tested": "1 EU = 1 MJ of potential; delivered = EU × η; 1 AU/s = 1 MW",
            "grade_read_from": ("where the page states joules, the page; otherwise the proxy — "
                                "Part Five's Max Grade for the Stage the page states"),
            "residual_unit": "decades (log10) outside the Grade's joule band; 0.0 = inside",
            "joules_defined_by": {
                "source": {"file": "wiki/Fracture of Worlds — The Living System/"
                                   "III. Physical Force (Part Eleven).md", "line": 30},
                "verbatim": pe_lines[29],
            },
            "stage_xiv_reading": stage_xiv_reading,
        },
        "dedupe": dedupe,
        "direct_pairs": direct_pairs,
        "grade_proxy_check": {"summary": proxy_summary, "rows": proxy_check},
        "reserve_vs_strike": {"summary": reserve_vs_strike_spread, "rows": reserve_vs_strike},
        "at_1_MJ": at_1mj,
        "best_fit": fits,
        "by_grade_reading": by_reading,
        "by_stage": by_stage,
        "required_k_spread_all": spread(tested),
        "formula_check": formula,
        "reserves": reserves,
        "costs": costs,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # --- printed report ----------------------------------------------------
    print("=== the measured side: where canon states both an EU cost and a joule output ===")
    for p in direct_pairs:
        lo = f"{p['j_per_eu_low']:,.0f}" if p["j_per_eu_low"] else "—"
        hi = f"{p['j_per_eu_high']:,.0f}" if p["j_per_eu_high"] else "—"
        eu = (f"{p['eu_low']:,.0f}" if p["eu_low"] == p["eu_high"]
              else f"{p['eu_low']:,.0f}–{p['eu_high']:,.0f}")
        print(f"  {p['entity'][:22]:<23} {p['working'][:26]:<27} {eu:>13} EU  ->  "
              f"{p['joules_low']:.3g} – {p['joules_high']:.3g} J"
              f"   = {lo} – {hi} J/EU"
              f"   (1 MJ overshoots by {p['decades_from_1MJ_least']:+.2f} to "
              f"{p['decades_from_1MJ_most']:+.2f} decades)")

    ps = proxy_summary
    print(f"\n=== the Stage->Grade proxy, checked against those joule figures ===")
    print(f"  strike figures with a Stage to check against: {ps['strike_rows']}"
          f"   proxy agrees on {ps['agree']}"
          f"   mean {ps['mean_grades_apart']:+.2f} Grades, mean absolute {ps['mean_abs_grades_apart']:.2f}")
    for k in sorted(ps["distribution"], key=int):
        print(f"    {k:>3} Grades apart: {ps['distribution'][k]}")
    for p in sorted(strikes, key=lambda p: -abs(p["grades_apart"]))[:10]:
        print(f"    {p['entity'][:26]:<27} {p['joules_high']:.3g} J = {p['grade_attested_high']:<4}"
              f"  proxy says {p['grade_from_stage_proxy']:<4} from Stage {p['stage']}"
              f"   {p['grades_apart']:+d}")

    rs = reserve_vs_strike_spread
    print(f"\n=== reserve against attested strike ({rs['n']} characters state both) ===")
    print(f"  joules per EU if one strike spent the whole reserve: "
          f"{rs['min']:.3g} … {rs['max']:.3g}, median {rs['median']:.3g}"
          f"  — {rs['decades_spanned']:.1f} decades apart")
    for x in sorted(reserve_vs_strike, key=lambda x: -x["j_per_eu_if_one_strike_spent_the_whole_reserve"]):
        print(f"    {x['entity'][:26]:<27} {x['reserve_eu']:>15,.0f} EU  strike {x['strike_joules']:.3g} J"
              f"   {x['j_per_eu_if_one_strike_spent_the_whole_reserve']:>12,.0f} J/EU"
              f"   at 1 MJ the reserve holds {x['strikes_the_reserve_holds_at_1MJ']:.3g} such strikes")

    print(f"\n=== each figure counted once ===")
    print(f"  reserves {dedupe['reserves']['rows']} rows -> {dedupe['reserves']['distinct']} figures"
          f" (strictest reading {dedupe['reserves']['distinct_strict']})")
    print(f"  costs    {dedupe['costs']['rows']} rows -> {dedupe['costs']['distinct']} figures"
          f" (strictest reading {dedupe['costs']['distinct_strict']})")

    print("\n=== at 1 EU = 1 MJ ===")
    for name, s in at_1mj.items():
        print(f"{name:<14} delivered in band {s['in_band_delivered']}/{s['of']}"
              f"   potential in band {s['in_band_potential']}/{s['of']}"
              f"   sum sq decades {s['sum_sq_decades_delivered']:.1f}"
              f"   median {s['median_decades_delivered']:+.2f}")
    print("\n=== best-fit k (joules per EU) ===")
    for name, fv in fits.items():
        if fv:
            print(f"{name:<14} k = {fv['k_j_per_eu']:.3g} J/EU"
                  f"   in band {fv['in_band']}/{fv['of']}"
                  f"   sum sq decades {fv['sum_sq_decades']:.1f}")

    print("\n=== the same test under each reading of \"their stated Grade\" ===")
    for name, s in by_reading.items():
        bf, sp = s["best_fit"], s["required_k_spread"]
        if not bf:
            print(f"{name:<13} no anchors carry a Grade under this reading")
            continue
        print(f"{name:<13} tested {s['tested']:>3}   in band at 1 MJ {s['in_band_at_1MJ']:>3}"
              f"   best k {bf['k_j_per_eu']:.3g} → {bf['in_band']}/{bf['of']}"
              f"   each anchor's own k spans {sp['decades_spanned']:.1f} decades"
              f" ({sp['k_min']:.2g} … {sp['k_max']:.2g})")

    print("\n=== residual by Stage, at 1 EU = 1 MJ (the misfit is not noise) ===")
    for s in sorted(by_stage, key=lambda x: int(x)):
        v = by_stage[s]
        print(f"  Stage {s:>2}  n={v['n']:<4} mean residual {v['mean_decades_at_1MJ']:+6.2f} dec"
              f"   median k this Stage would need: {v['median_required_k']:.3g} J/EU")

    print("\n=== reserves, per anchor, at 1 EU = 1 MJ ===")
    for r in sorted(reserves, key=lambda r: -(r["eu"] or 0)):
        if r["skipped"]:
            print(f"  {r['entity'][:34]:<35} {r['eu']:>16,.0f} EU   — {r['skipped']}")
            continue
        print(f"  {r['entity'][:34]:<35} {r['eu']:>16,.0f} EU  St {r['stage']:>2}"
              f"  Grade {r['grade']:<4} η {r['eta']:.2f}"
              f"  delivered {r['delivered_j_at_1MJ']:.3g} J"
              f"  band {r['band_j_low']:.3g}–{r['band_j_high']:.3g}"
              f"  residual {r['decades_delivered']:+.2f} dec")

    print("\n=== costs, per anchor, at 1 EU = 1 MJ (the family Part Four measures) ===")
    for r in sorted((r for r in costs if not r["skipped"]), key=lambda r: -(r["eu"] or 0)):
        print(f"  {r['entity'][:34]:<35} {r['eu']:>16,.0f} EU  St {r['stage']:>2}"
              f"  Grade {r['grade']:<4} η {r['eta']:.2f}"
              f"  delivered {r['delivered_j_at_1MJ']:.3g} J"
              f"  band {r['band_j_low']:.3g}–{r['band_j_high']:.3g}"
              f"  residual {r['decades_delivered']:+.2f} dec")

    print("\n=== AU/s = Flux Density × η ===")
    for c in formula:
        mark = "holds" if c["holds"] else "BREAKS"
        print(f"  {mark:<7} {c['entity'][:32]:<33} {c['flux_density']:>12,.0f} × {c['eta']:.2f}"
              f" = {c['expected_au_s']:>13,.0f}   card says {c['stated_au_s']:>13,.0f}"
              f"   ×{c['ratio_stated_over_expected']:.2f}")
    print(f"\nwritten: {REPORT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
