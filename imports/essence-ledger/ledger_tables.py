#!/usr/bin/env python3
"""ledger_tables.py — WAR-12, Phase 2 of the Essence Ledger (parent WAR-8).

Reads `anchors.json` and `fit.json` (WAR-9, Phase 1) and produces every table
the draft Part `the-essence-ledger.md` prints, with the residual against each
anchor shown. It invents nothing: every input is a Phase 1 anchor or a verbatim
row of a Magic System / Fracture of Worlds table already collected there.

    python imports/essence-ledger/ledger_tables.py

Writes `ledger_tables.json` beside itself and prints the report.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# A. The constant. Canon prices a working in EU and in joules three times, all
#    on Dougou Ozumu Zettari's sheet and his Spellcraft page (fit.json
#    `direct_pairs`). Those three are the whole measured evidence. Grid-search
#    the constant that puts all three inside the joule band their own page
#    states, scoring in decades.
# --------------------------------------------------------------------------

def residual_decades(pred_lo, pred_hi, band_lo, band_hi):
    """0 if the predicted range sits inside the stated band; else the signed
    distance in decades from the nearer edge to the nearer predicted edge."""
    if pred_lo >= band_lo and pred_hi <= band_hi:
        return 0.0
    if pred_lo > band_hi:
        return math.log10(pred_lo / band_hi)
    if pred_hi < band_lo:
        return math.log10(pred_hi / band_lo)
    # straddles an edge: score the overhang
    if pred_hi > band_hi:
        return math.log10(pred_hi / band_hi)
    return math.log10(pred_lo / band_lo)


def constant_fit(fit):
    pairs = []
    for p in fit["direct_pairs"]:
        eu_lo = p.get("eu_low") or p.get("eu")
        eu_hi = p.get("eu_high") or p.get("eu")
        pairs.append({
            "entity": p["entity"],
            "working": p["working"],
            "why": p.get("why"),
            "eu_low": eu_lo,
            "eu_high": eu_hi,
            "joules_low": p["joules_low"],
            "joules_high": p["joules_high"],
            "k_window_low": p["joules_low"] / eu_hi,
            "k_window_high": p["joules_high"] / eu_lo,
            "k_window_strict_low": p["joules_low"] / eu_lo,
            "k_window_strict_high": p["joules_high"] / eu_hi,
            "cost_source": p["cost_source"],
            "cost_verbatim": p["cost_verbatim"],
            "joule_source": p["joule_source"],
            "joule_verbatim": p["joule_verbatim"],
        })

    def score(k):
        return sum(residual_decades(k * q["eu_low"], k * q["eu_high"],
                                    q["joules_low"], q["joules_high"]) ** 2
                   for q in pairs)

    # grid search, 10^1 .. 10^8, 0.001 decades
    best_k, best_s = None, None
    k = 10.0
    step = 10 ** 0.001
    while k <= 1e8:
        s = score(k)
        if best_s is None or s < best_s - 1e-15:
            best_k, best_s = k, s
        k *= step

    candidates = {}
    for label, k in (("brief, 1 EU = 1 MJ", 1e6),
                     ("1 EU = 1 kJ", 1e3),
                     ("least squares on the three pairs", best_k)):
        rows = []
        for q in pairs:
            r = residual_decades(k * q["eu_low"], k * q["eu_high"],
                                 q["joules_low"], q["joules_high"])
            rows.append({
                "entity": q["entity"],
                "working": q["working"],
                "eu_low": q["eu_low"], "eu_high": q["eu_high"],
                "stated_j_low": q["joules_low"], "stated_j_high": q["joules_high"],
                "predicted_j_low": k * q["eu_low"], "predicted_j_high": k * q["eu_high"],
                "residual_decades": r,
                "in_band": r == 0.0,
            })
        candidates[label] = {
            "k_j_per_eu": k,
            "sum_sq_decades": score(k),
            "in_band": sum(1 for r in rows if r["in_band"]),
            "of": len(rows),
            "rows": rows,
        }
    return {"pairs": pairs, "best_k": best_k, "candidates": candidates}


# --------------------------------------------------------------------------
# B. The reserve law. Isaac ruled a method on 2026-09-12, quoted on
#    `wiki/Summoned and Bound/Obrenkael · The Mule.md:215`: a log-linear
#    interpolation on LEVEL between three fixed anchors. Fit it, then measure
#    every attested reserve that also states a Level against it.
# --------------------------------------------------------------------------

RULED_ANCHORS = [
    # (name, level, EU, where the ruling names it)
    ("Ara Min Mahuo", 250, 4_200_000),
    ("Borin Ironheart", 378, 180_000_000),
    ("Kwon Mu-jin", 430, 850_000_000),
]

# Levels as the anchor pages state them. `pages` in anchors.json carries most;
# the three written "L / 500" and Kwon Hae-ryu's ruled Level are added here so
# the fit reads one dictionary. Every one is quoted in the draft Part.
LEVELS = {
    "Naori Yukari": 80,
    "Yoko Mishiro": 145,
    "Karo Venrik · The Foolish Magus": 156,
    "Mizuki Moto": 128,
    "Anryū Ichimonji": 180,
    "Rashani Zettari": 182,
    "Niran Yukari": 195,
    "Rengai Zettari": 250,
    "Ara Min Mahuo": 250,
    "Sodoku Moto": 320,
    "Kwon Hae-ryu": 355,
    "Borin Ironheart · The Master of the Soul Forge": 378,
    "Krothar Veylshroud": 380,
    "Krothar Veylshroud — The Chain Without a Master": 380,
    "Ignatius Sanctus Sanctorum Arsenal · The Archpaladin": 385,
    "Kwon Mu-jin": 430,
    "Verinus VII · The Palatine": 462,
    "The Arctic Lion — Sovereign Configuration (Level 500)": 500,
    "Aurelian Prudentius Custos Clausorum · The Primate": 500,
}


def reserve_law(fit):
    # slope from the ruled anchors, segment by segment and overall
    segments = []
    for (n1, l1, e1), (n2, l2, e2) in zip(RULED_ANCHORS, RULED_ANCHORS[1:]):
        segments.append({
            "from": n1, "to": n2,
            "levels": [l1, l2],
            "decades_per_level": (math.log10(e2) - math.log10(e1)) / (l2 - l1),
        })
    # one line through the first and last ruled anchor
    (_, la, ea), (_, lb, eb) = RULED_ANCHORS[0], RULED_ANCHORS[-1]
    slope = (math.log10(eb) - math.log10(ea)) / (lb - la)
    intercept = math.log10(ea) - slope * la

    def predict(level):
        return 10 ** (intercept + slope * level)

    rows = []
    for r in fit["reserves"]:
        lvl = LEVELS.get(r["entity"])
        if lvl is None:
            continue
        pred = predict(lvl)
        rows.append({
            "entity": r["entity"],
            "level": lvl,
            "stage": r["stage"],
            "eu_stated": r["eu"],
            "eu_predicted": pred,
            "residual_decades": math.log10(r["eu"] / pred),
            "source": r["source"],
            "verbatim": r["verbatim"],
        })
    rows.sort(key=lambda x: x["level"])
    resid = [abs(r["residual_decades"]) for r in rows]
    resid.sort()
    return {
        "method_source": {
            "file": "wiki/Summoned and Bound/Obrenkael · The Mule.md",
            "line": 215,
        },
        "ruled_anchors": [{"entity": n, "level": l, "eu": e} for n, l, e in RULED_ANCHORS],
        "segments": segments,
        "decades_per_level": slope,
        "log10_eu_at_level_0": intercept,
        "levels_per_decade": 1.0 / slope,
        "rows": rows,
        "n": len(rows),
        "within_half_decade": sum(1 for x in resid if x <= 0.5),
        "within_one_decade": sum(1 for x in resid if x <= 1.0),
        "median_abs_residual": resid[len(resid) // 2],
    }


# --------------------------------------------------------------------------
# C. Reserve bands by Stage and by Tier of Standing, from the attested set.
#    Purely observed: the range the anchors occupy, with who sits at each end.
# --------------------------------------------------------------------------

STAGE_TO_TIER = {
    1: "1 · Initiate", 2: "2 · Apprentice", 3: "3 · Journeyman", 4: "4 · Adept",
    5: "5 · Expert", 6: "5 · Expert", 7: "5 · Expert",
    8: "6 · Master", 9: "6 · Master", 10: "6 · Master",
    11: "7 · Grandmaster", 12: "7 · Grandmaster",
    13: "8 · Archmaster", 14: "8 · Archmaster",
    15: "9 · Paragon", 16: "9 · Paragon",
}

# The GATE CEILING. FoW Part One sets four gates: "Stage IV before Level 100
# can be surpassed", VII before 200, X before 300, XII before 400. Read as the
# contrapositive they are a hard ceiling on Level given Stage — a Stage III
# practitioner cannot be above Level 100 — and nothing more. There is no
# matching floor anywhere in Part One, so the gates cap a reserve; they do not
# set one.
STAGE_LEVEL_CEILING = {
    1: 100, 2: 100, 3: 100,
    4: 200, 5: 200, 6: 200,
    7: 300, 8: 300, 9: 300,
    10: 400, 11: 400,
    12: 500, 13: 500, 14: 500, 15: 500, 16: 500,
}
# The CLUSTER BAND. Part One also gives each of the five Level Bands a
# "Temperance cluster": Band I (Levels 1-100) is Stages I-IV, Band II
# (101-200) Stages V-VII, Band III (201-300) VIII-X, Band IV (301-400) XI-XII,
# Band V (401-500) XIII-XIV, with XV and XVI "lying beyond canonical mortal
# progression". That is where a Stage's practitioners usually sit, not where
# they must; it gives the typical range, and an anchor outside it is at an
# unusual Level for its Stage rather than in breach of anything.
STAGE_CLUSTER_LEVELS = {
    1: (1, 100), 2: (1, 100), 3: (1, 100), 4: (1, 100),
    5: (101, 200), 6: (101, 200), 7: (101, 200),
    8: (201, 300), 9: (201, 300), 10: (201, 300),
    11: (301, 400), 12: (301, 400),
    13: (401, 500), 14: (401, 500),
    # Part One gives Stages XV and XVI no Band: Band V's cluster is XIII-XIV,
    # "with Stage XV Revelation and Stage XVI Apex lying beyond canonical
    # mortal progression", and "There is no Band beyond Band V". A Stage with
    # no Level range has no reserve under a law that reads off Level, so both
    # rows are left null rather than filled by extending Band V upward.
    15: None, 16: None,
}


def bands(fit, law):
    by_stage, by_tier = {}, {}
    for r in fit["reserves"]:
        s = r["stage"]
        if s is None:
            continue
        by_stage.setdefault(s, []).append(r)
        by_tier.setdefault(STAGE_TO_TIER[s], []).append(r)

    def summarise(group):
        eus = sorted(group, key=lambda r: r["eu"])
        return {
            "n": len(eus),
            "low_eu": eus[0]["eu"], "low_entity": eus[0]["entity"],
            "high_eu": eus[-1]["eu"], "high_entity": eus[-1]["entity"],
            "decades_spanned": math.log10(eus[-1]["eu"] / eus[0]["eu"]),
            "geometric_mean": 10 ** (sum(math.log10(r["eu"]) for r in eus) / len(eus)),
            "entities": [{"entity": r["entity"], "eu": r["eu"], "eta": r["eta"]} for r in eus],
        }

    slope, inter = law["decades_per_level"], law["log10_eu_at_level_0"]

    def at_level(l):
        return 10 ** (inter + slope * l)

    def predicted_for_stage(s):
        cluster = STAGE_CLUSTER_LEVELS[s]
        if cluster is None:          # Stages XV-XVI: no Band, so no Level range
            return {"gate_level": None, "gate_ceiling_eu": None,
                    "cluster_levels": None, "cluster_eu_low": None,
                    "cluster_eu_high": None, "pending": "no Level Band in Part One"}
        c_lo, c_hi = cluster
        return {
            "gate_level": STAGE_LEVEL_CEILING[s],
            "gate_ceiling_eu": at_level(STAGE_LEVEL_CEILING[s]),
            "cluster_levels": [c_lo, c_hi],
            "cluster_eu_low": at_level(c_lo),
            "cluster_eu_high": at_level(c_hi),
        }

    def verdicts(group, p):
        out = []
        for r in group:
            eu = r["eu"]
            out.append({
                "entity": r["entity"], "eu": eu, "eta": r["eta"],
                "level": LEVELS.get(r["entity"]),
                "under_gate_ceiling": eu <= p["gate_ceiling_eu"],
                "in_cluster_band": p["cluster_eu_low"] <= eu <= p["cluster_eu_high"],
                "decades_from_cluster": (
                    0.0 if p["cluster_eu_low"] <= eu <= p["cluster_eu_high"]
                    else (math.log10(eu / p["cluster_eu_high"]) if eu > p["cluster_eu_high"]
                          else math.log10(eu / p["cluster_eu_low"]))),
                "decades_over_gate": (math.log10(eu / p["gate_ceiling_eu"])
                                      if eu > p["gate_ceiling_eu"] else 0.0),
                "source": r["source"], "verbatim": r["verbatim"],
            })
        return sorted(out, key=lambda x: x["eu"])

    stage_rows = []
    for s in sorted(by_stage):
        p = predicted_for_stage(s)
        d = summarise(by_stage[s])
        d.update({"stage": s, "tier": STAGE_TO_TIER[s]})
        d.update(p)
        d["anchors"] = verdicts(by_stage[s], p)
        d["under_gate"] = sum(1 for a in d["anchors"] if a["under_gate_ceiling"])
        d["in_cluster"] = sum(1 for a in d["anchors"] if a["in_cluster_band"])
        stage_rows.append(d)

    tier_rows = []
    for t in sorted(by_tier):
        stages = sorted({r["stage"] for r in by_tier[t]})
        ps = [predicted_for_stage(s) for s in stages]
        p = {
            "gate_level": max(STAGE_LEVEL_CEILING[s] for s in stages),
            "gate_ceiling_eu": max(x["gate_ceiling_eu"] for x in ps),
            "cluster_levels": [min(x["cluster_levels"][0] for x in ps),
                               max(x["cluster_levels"][1] for x in ps)],
            "cluster_eu_low": min(x["cluster_eu_low"] for x in ps),
            "cluster_eu_high": max(x["cluster_eu_high"] for x in ps),
        }
        d = summarise(by_tier[t])
        d.update({"tier": t, "stages": stages})
        d.update(p)
        d["anchors"] = verdicts(by_tier[t], p)
        d["under_gate"] = sum(1 for a in d["anchors"] if a["under_gate_ceiling"])
        d["in_cluster"] = sum(1 for a in d["anchors"] if a["in_cluster_band"])
        tier_rows.append(d)

    # the full ladder, every Stage, whether or not an anchor sits there
    full = []
    for s in range(1, 17):
        d = {"stage": s, "tier": STAGE_TO_TIER[s]}
        d.update(predicted_for_stage(s))
        full.append(d)
    for r in full:
        if r.get("pending"):
            print("   note: Stage %d (%s) left null — %s" % (r["stage"], r["tier"], r["pending"]))

    all_anchors = [a for r in stage_rows for a in r["anchors"]]
    return {
        "by_stage": stage_rows, "by_tier": tier_rows, "law_full_ladder": full,
        "totals": {
            "n": len(all_anchors),
            "under_gate_ceiling": sum(1 for a in all_anchors if a["under_gate_ceiling"]),
            "over_gate_ceiling": [
                {"entity": a["entity"], "eu": a["eu"], "decades_over": a["decades_over_gate"]}
                for a in all_anchors if not a["under_gate_ceiling"]],
            "in_cluster_band": sum(1 for a in all_anchors if a["in_cluster_band"]),
            "within_1_decade_of_cluster": sum(
                1 for a in all_anchors if abs(a["decades_from_cluster"]) <= 1.0),
        },
    }


# --------------------------------------------------------------------------
# D. The spine: peak output in joules -> Grade (Part Four) -> Tier of
#    Standing 1..9 (Part Five's Max Grade column read backwards). Every edge
#    is a verbatim Part Four figure; every name is a verbatim Part Five one.
# --------------------------------------------------------------------------

# Part Five, Stage gate table: the lowest Stage whose Max Grade reaches a
# Grade, and the Tier of Standing that Stage carries.
GRADE_TO_TIER = [
    ("Hollow", 1, "I Murmuring"),
    ("F", 1, "I Murmuring"),
    ("E", 1, "I Murmuring"),
    ("D", 2, "II Welling"),
    ("C", 3, "III Ascension"),
    ("B", 4, "IV Flourishing"),
    ("A", 6, "VI Glory"),
    ("S", 8, "VIII Transcendence"),
    ("SS", 10, "X Realization"),
    ("SSS", 12, "XII Emanation"),
    ("X", 13, "XIII Principality"),
    ("EX", 14, "XIV Zenith"),
    ("EX+", 15, "XV Revelation"),
]

TON_TNT_J = 4.184e9


def spine(anchors, k):
    grades = {g["grade"]: g for g in anchors["system"]["grade_bands"]}
    tiers = {}
    for grade, stage, stage_name in GRADE_TO_TIER:
        t = STAGE_TO_TIER[stage]
        g = grades[grade]
        row = tiers.setdefault(t, {
            "tier": t, "grades": [], "stages": [], "stage_names": [],
            "j_low": None, "j_high": None,
        })
        row["grades"].append(grade)
        row["stages"].append(stage)
        row["stage_names"].append(stage_name)
        lo, hi = g["attack_output_j_low"], g["attack_output_j_high"]
        if lo is not None and (row["j_low"] is None or lo < row["j_low"]):
            row["j_low"] = lo
        if hi is not None and (row["j_high"] is None or hi > row["j_high"]):
            row["j_high"] = hi
    out = []
    for t in sorted(tiers):
        r = tiers[t]
        r["tnt_low"] = r["j_low"] / TON_TNT_J if r["j_low"] else None
        r["tnt_high"] = r["j_high"] / TON_TNT_J if r["j_high"] else None
        r["eu_to_buy_ceiling_at_k"] = r["j_high"] / k if r["j_high"] else None
        r["eu_to_buy_floor_at_k"] = r["j_low"] / k if r["j_low"] else None
        out.append(r)
    return out


# --------------------------------------------------------------------------
# E. The drain. At 1 AU = 1 EU the constant cancels and t = EU / (AU/s); the
#    table is reproduced here so the Part can show the arithmetic beside the
#    waste-heat clock, which does NOT cancel.
# --------------------------------------------------------------------------

BODY_HEAT_CAPACITY_J_PER_K = 245_000.0   # 70 kg x 3.5 kJ/kg/K, physics-check.md
LETHAL_RISE_K = 5.0
BODY_SHED_W = 2_000.0


def drain(fit, anchors, k):
    au, card_eta = {}, {}
    for a in anchors["anchors"]:
        if a.get("value") is None or a.get("duplicate_of"):
            continue
        if a["kind"] == "au_s":
            au.setdefault(a["entity"], a)
        elif a["kind"] == "eta":
            card_eta.setdefault(a["entity"], a)
    rows = []
    for r in fit["reserves"]:
        a = au.get(r["entity"])
        if not a:
            continue
        # The card's own eta governs. `fit.json` reads eta off the page that
        # carries the RESERVE, which for Dougou (The Iron Tree) and Kwon Mu-jin
        # (The Open Crucible) is not the card, so it falls back to Part
        # Nineteen's Tier midpoint. Here the character's own sheet wins where
        # it states a figure.
        ce = card_eta.get(r["entity"])
        if ce:
            aus, eta = a["value"], ce["value"]
            r = dict(r, eta=eta, eta_from="card, %s:%d" % (
                ce["source"]["file"].rsplit("/", 1)[-1], ce["source"]["line"]))
        else:
            aus, eta = a["value"], r["eta"]
        waste_w = (1 - eta) * aus * k if eta is not None and eta < 1 else 0.0
        rows.append({
            "entity": r["entity"],
            "stage": r["stage"],
            "tier": STAGE_TO_TIER[r["stage"]] if r["stage"] else None,
            "eu": r["eu"], "au_s": aus, "eta": eta, "eta_from": r.get("eta_from"),
            "reserve_j": r["eu"] * k,
            "power_w": aus * k,
            "seconds_to_empty": r["eu"] / aus,
            "seconds_to_starvation": 0.9 * r["eu"] / aus,
            "waste_w": waste_w,
            "seconds_to_lethal_rise": (BODY_HEAT_CAPACITY_J_PER_K * LETHAL_RISE_K /
                                       (waste_w - BODY_SHED_W)) if waste_w > BODY_SHED_W else None,
            "shed_fraction": BODY_SHED_W / waste_w if waste_w else None,
            "au_s_source": a["source"],
            "au_s_verbatim": a["verbatim"],
        })
    rows.sort(key=lambda x: x["seconds_to_empty"])
    return rows


# --------------------------------------------------------------------------
# F. Flux Density against eta. Canon states AU/s = Flux Density x eta. The
#    left side is EU/s, the right EU/g: the identity is short one mass. Solve
#    for the mass it would need and report it, without asserting it.
# --------------------------------------------------------------------------

def flux_eta(fit):
    rows = []
    for r in fit["formula_check"]:
        implied_g = r["stated_au_s"] / (r["flux_density"] * r["eta"])
        rows.append({
            "entity": r["entity"],
            "flux_density": r["flux_density"],
            "eta": r["eta"],
            "stated_au_s": r["stated_au_s"],
            "expected_au_s": r["expected_au_s"],
            "ratio": r["ratio_stated_over_expected"],
            "implied_crystal_mass_g": implied_g,
            "residual_decades": math.log10(r["ratio_stated_over_expected"]),
            "holds": r["holds"],
            "flux_source": r["flux_source"],
            "flux_verbatim": r["flux_verbatim"],
        })
    rows.sort(key=lambda x: x["implied_crystal_mass_g"])
    inside = [r for r in rows if 0.2 <= r["implied_crystal_mass_g"] <= 10]
    return {
        "rows": rows,
        "n": len(rows),
        "holds_exactly": sum(1 for r in rows if r["holds"]),
        "implied_mass_between_0p2_and_10_g": len(inside),
        "implied_mass_names": [r["entity"] for r in inside],
    }


# --------------------------------------------------------------------------
# G. Starvation and recovery, in the attested recovery figures.
# --------------------------------------------------------------------------

RECOVERY = [
    # entity, kind, figure as written, per-minute fraction of reserve or absolute
    ("Niran Yukari", "passive", "28% EU/min", 0.28, None,
     "wiki/Volume I — Character Cards/Niran Yukari.md", 61),
    ("Naori Yukari", "passive", "15% EU/min", 0.15, None,
     "wiki/Volume I — Character Cards/Naori Yukari.md", 54),
    ("Rashani Zettari", "passive", "14% EU/min", 0.14, None,
     "wiki/Volume I — Character Cards/Rashani Zettari.md", 64),
    ("Mizuki Moto", "passive", "12% EU/min at rest", 0.12, None,
     "wiki/Volume I — Character Cards/Mizuki Moto.md", 59),
    ("Anryū Ichimonji", "passive", "11% EU/min", 0.11, None,
     "wiki/Volume I — Character Cards/Anryū Ichimonji.md", 63),
    ("Rengai Zettari", "passive", "9% EU/min", 0.09, None,
     "wiki/Volume I — Character Cards/Rengai Zettari.md", 60),
    ("Krothar Veylshroud", "passive, chains on", "~18,000 EU/min", None, 18_000.0,
     "wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md", 102),
    ("Krothar Veylshroud", "passive, chains off", "~52,000 EU/min", None, 52_000.0,
     "wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md", 102),
    ("Krothar Veylshroud", "active, chains off", "~88,000 EU/min", None, 88_000.0,
     "wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md", 103),
    ("Ara Min Mahuo", "passive", "~126,000 EU/hour", None, 126_000.0 / 60,
     "wiki/Volume I — Character Cards/Ara Min Mahuo.md", 72),
    ("Ara Min Mahuo", "active", "~252,000 EU/hour", None, 252_000.0 / 60,
     "wiki/Volume I — Character Cards/Ara Min Mahuo.md", 74),
    ("Kwon Mu-jin", "passive", "~12,750,000 EU/hour at rest", None, 12_750_000.0 / 60,
     "wiki/Volume I — Character Cards/Kwon Mu-jin.md", 74),
    ("Kwon Mu-jin", "active", "~38,250,000 EU/hour", None, 38_250_000.0 / 60,
     "wiki/Volume I — Character Cards/Kwon Mu-jin.md", 74),
]


def recovery(fit):
    reserves = {r["entity"]: r["eu"] for r in fit["reserves"]}
    rows = []
    for ent, kind, written, frac, absolute, f, line in RECOVERY:
        res = reserves.get(ent)
        if frac is None and res:
            frac = absolute / res
        if absolute is None and res:
            absolute = frac * res
        rows.append({
            "entity": ent, "kind": kind, "as_written": written,
            "reserve_eu": res,
            "fraction_per_min": frac,
            "eu_per_min": absolute,
            "minutes_empty_to_full": (1.0 / frac) if frac else None,
            "minutes_to_clear_starvation": (0.9 / frac) if frac else None,
            "source": {"file": f, "line": line},
        })
    # Two populations, and they do not agree. Six cards state recovery as a
    # PERCENTAGE of reserve per minute; four state an ABSOLUTE EU figure per
    # minute or hour. Converted to the same units the two groups sit one to
    # three decades apart, so they are reported apart.
    def group(pred):
        g = sorted((r for r in rows if pred(r) and r["fraction_per_min"]),
                   key=lambda r: r["fraction_per_min"])
        return {
            "n": len(g),
            "low": g[0]["fraction_per_min"], "low_entity": g[0]["entity"],
            "high": g[-1]["fraction_per_min"], "high_entity": g[-1]["entity"],
            "median": g[len(g) // 2]["fraction_per_min"],
            "minutes_empty_to_full_at_median": 1.0 / g[len(g) // 2]["fraction_per_min"],
            "minutes_empty_to_full_at_low": 1.0 / g[0]["fraction_per_min"],
            "minutes_empty_to_full_at_high": 1.0 / g[-1]["fraction_per_min"],
        }

    pct = group(lambda r: "%" in r["as_written"])
    absolute = group(lambda r: "%" not in r["as_written"])
    return {
        "rows": rows,
        "stated_as_percentage": pct,
        "stated_as_absolute": absolute,
        "decades_between_the_two_medians": math.log10(pct["median"] / absolute["median"]),
    }


# --------------------------------------------------------------------------

def main():
    anchors, fit = load("anchors.json"), load("fit.json")
    cf = constant_fit(fit)
    K = 1e3  # the draft's working constant; see the Part, §2
    law = reserve_law(fit)
    out = {
        "meta": {
            "issue": "WAR-12",
            "phase": "Essence Ledger Phase 2 — the system",
            "date": "2026-09-25",
            "inputs": ["imports/essence-ledger/anchors.json",
                       "imports/essence-ledger/fit.json"],
            "working_constant_j_per_eu": K,
            "note": "the working constant is the draft's, not a ruling. C-034 is open and chooses none of the readings; every table here is marked pending on it in the Part.",
        },
        "constant_fit": cf,
        "reserve_law": law,
        "bands": bands(fit, law),
        "spine": spine(anchors, K),
        "drain": drain(fit, anchors, K),
        "flux_eta": flux_eta(fit),
        "recovery": recovery(fit),
    }
    with open(os.path.join(HERE, "ledger_tables.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    # ---- report ----
    print("A. THE CONSTANT — the three lines where canon prices a working both ways")
    for label, c in cf["candidates"].items():
        print("  %-36s k = %-12.4g  in band %d/%d  sum sq %.4f"
              % (label, c["k_j_per_eu"], c["in_band"], c["of"], c["sum_sq_decades"]))
        for r in c["rows"]:
            print("      %-34s %9.3g-%-9.3g J vs stated %9.3g-%-9.3g  resid %+.3f dec"
                  % (r["working"][:34], r["predicted_j_low"], r["predicted_j_high"],
                     r["stated_j_low"], r["stated_j_high"], r["residual_decades"]))

    print("\nB. THE RESERVE LAW — log-linear on Level, the method Isaac ruled 2026-09-12")
    print("   %.6f decades per Level  (x10 every %.1f Levels);  log10 EU = %.4f + %.6f L"
          % (law["decades_per_level"], law["levels_per_decade"],
             law["log10_eu_at_level_0"], law["decades_per_level"]))
    for s in law["segments"]:
        print("   segment %-18s -> %-18s %.6f dec/Level" % (s["from"], s["to"], s["decades_per_level"]))
    print("   %d anchors state a Level; %d within +/-0.5 decades, %d within +/-1.0; median |resid| %.3f"
          % (law["n"], law["within_half_decade"], law["within_one_decade"], law["median_abs_residual"]))
    for r in law["rows"]:
        print("     L%-4d St %-3s %-44s stated %-12.4g law %-12.4g  %+.3f dec"
              % (r["level"], r["stage"], r["entity"][:44], r["eu_stated"],
                 r["eu_predicted"], r["residual_decades"]))

    print("\nC. RESERVE BANDS BY STAGE — gate ceiling (hard), cluster band (typical), attested")
    for r in out["bands"]["by_stage"]:
        print("   Stage %-4s %-16s n=%-2d  gate L%-3d <= %-9.3g EU | cluster L%d-%d %9.3g - %-9.3g | attested %9.3g - %-9.3g (%.2f dec)  under gate %d/%d, in cluster %d/%d"
              % (r["stage"], r["tier"], r["n"], r["gate_level"], r["gate_ceiling_eu"],
                 r["cluster_levels"][0], r["cluster_levels"][1],
                 r["cluster_eu_low"], r["cluster_eu_high"],
                 r["low_eu"], r["high_eu"], r["decades_spanned"],
                 r["under_gate"], r["n"], r["in_cluster"], r["n"]))
        for a in r["anchors"]:
            print("        %-46s %-11.4g  %s%s"
                  % (a["entity"][:46], a["eu"],
                     "under gate" if a["under_gate_ceiling"] else "OVER GATE by %.2f dec" % a["decades_over_gate"],
                     ", in cluster band" if a["in_cluster_band"] else ", %+.2f dec from cluster" % a["decades_from_cluster"]))

    print("\nC2. RESERVE BANDS BY TIER OF STANDING")
    for r in out["bands"]["by_tier"]:
        print("   %-16s stages %-14s n=%-2d gate <= %-9.3g | cluster %9.3g - %-9.3g | attested %9.3g - %-9.3g  under gate %d/%d"
              % (r["tier"], str(r["stages"]), r["n"], r["gate_ceiling_eu"],
                 r["cluster_eu_low"], r["cluster_eu_high"],
                 r["low_eu"], r["high_eu"], r["under_gate"], r["n"]))
    t = out["bands"]["totals"]
    print("   TOTAL: %d of %d attested reserves sit under the gate ceiling their Stage gives; %d in the cluster band, %d within one decade of it"
          % (t["under_gate_ceiling"], t["n"], t["in_cluster_band"], t["within_1_decade_of_cluster"]))
    for o in t["over_gate_ceiling"]:
        print("     over the gate: %-46s %-11.4g by %.2f decades" % (o["entity"][:46], o["eu"], o["decades_over"]))

    print("\nD. THE SPINE — joules -> Grade -> Tier 1..9, and the EU that buys the ceiling at 1 kJ")
    for r in out["spine"]:
        hi = ("%9.3g" % r["j_high"]) if r["j_high"] else "  and up"
        tnthi = ("%9.3g" % r["tnt_high"]) if r["tnt_high"] else "  and up"
        eu = ("%.4g EU" % r["eu_to_buy_ceiling_at_k"]) if r["eu_to_buy_ceiling_at_k"] else "no ceiling"
        print("   %-16s %-10s %9.3g - %-9s J   %9.3g - %-9s t TNT   ceiling costs %s"
              % (r["tier"], "/".join(r["grades"]), r["j_low"], hi, r["tnt_low"], tnthi, eu))

    print("\nE. THE DRAIN — t = EU / (AU/s), and the waste-heat clock at 1 AU/s = 1 kW")
    for r in out["drain"]:
        print("   %-44s %8.1f s to empty, %8.1f s to Starvation, waste %9.3g W, +5K in %-10s (eta %s from %s)"
              % (r["entity"][:44], r["seconds_to_empty"], r["seconds_to_starvation"],
                 r["waste_w"],
                 ("%.2f s" % r["seconds_to_lethal_rise"]) if r["seconds_to_lethal_rise"] else "never",
                 r["eta"], r["eta_from"]))

    print("\nF. AU/s = FLUX DENSITY x eta — the missing mass, in grams")
    fe = out["flux_eta"]
    print("   holds exactly on %d of %d; implied mass between 0.2 g and 10 g on %d"
          % (fe["holds_exactly"], fe["n"], fe["implied_mass_between_0p2_and_10_g"]))
    for r in fe["rows"]:
        print("     %-44s implied %10.4g g   resid %+.3f dec" %
              (r["entity"][:44], r["implied_crystal_mass_g"], r["residual_decades"]))

    print("\nG. RECOVERY — two populations, one to three decades apart")
    rc = out["recovery"]
    for label, g in (("stated as a percentage", rc["stated_as_percentage"]),
                     ("stated as an absolute figure", rc["stated_as_absolute"])):
        print("   %-30s n=%d  %.3f%%/min (%s) to %.3f%%/min (%s), median %.3f%%/min; empty to full %.1f min at the median"
              % (label, g["n"], g["low"] * 100, g["low_entity"], g["high"] * 100,
                 g["high_entity"], g["median"] * 100, g["minutes_empty_to_full_at_median"]))
    print("   the two medians are %.2f decades apart" % rc["decades_between_the_two_medians"])
    for r in rc["rows"]:
        print("     %-22s %-20s %-28s %s%%/min, %s EU/min"
              % (r["entity"][:22], r["kind"], r["as_written"],
                 ("%.1f" % (r["fraction_per_min"] * 100)) if r["fraction_per_min"] else "?",
                 ("%.4g" % r["eu_per_min"]) if r["eu_per_min"] else "?"))

    print("\nwrote ledger_tables.json")


if __name__ == "__main__":
    main()
