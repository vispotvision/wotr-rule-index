#!/usr/bin/env python3
"""WAR-9, step 2 — fit the EU→joule constant against the collected anchors.

Isaac's conversion to test is **1 EU = 1 MJ of potential**, with energy
delivered = EU × η, so 1 AU/s = 1 MW.

The test asks whether a figure, converted to joules and read through η, lands in
the joule band the page's own Grade claims in FoW Part Four. Nothing here edits a
card. Two families of figure are tested separately, because Part Four measures
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

    raw_reserves = [a for a in doc["anchors"] if a["kind"] == "eu_reserve"]
    readings = {}
    for reading in ("stage_max", "card_stated", "peak_primary"):
        readings[reading] = {
            "reserves": build(raw_reserves, "reserve", reading),
            "costs": build(doc["costs"], "cost", reading),
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
            "grade_read_from": "Part Five's Max Grade for the Stage the page states",
            "residual_unit": "decades (log10) outside the Grade's joule band; 0.0 = inside",
        },
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
    print("=== at 1 EU = 1 MJ ===")
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
