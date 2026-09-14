"""The sheet checker: a character sheet posted in #character-submission, checked against
the canon it must obey. Every check cites its rule. Nothing here judges prose quality;
it checks what can be checked mechanically:

  stats   — the canon model (R39-1): Sub-Stats carry the points, a Primary is their total,
            the Grade is the mean (Dominion over seven, R39-2); no Sub-Stat above the Stage's
            Max Grade top (R39-4); the pool for the Level and Stage (Part Three, Stage I
            counting, R39-3) is not exceeded; Level and Stage present and gated.
  names   — struck names and registers (the Moto Reversion Ledger, R22, R21-1, R23-1).
  terms   — Stage names and Grade letters as the Living System spells them (R14-5).
"""
import re

import fow as F
import wotr as W

M = W.M
ROMAN = F.ROMAN
GRADES = ["Hollow", "F", "E", "D", "C", "B", "A", "S", "SS", "SSS", "X", "EX", "EX+"]
STAT_LINE = re.compile(r"\b([A-Z][a-z]+)\b[^\w\n]{1,6}(\d{1,4})(?!\s*[/%])")


def parse(text: str) -> dict:
    cx = F.canon()
    out = {"level": None, "stage": None, "subs": {}, "primaries_stated": {}}
    m = re.search(r"\bLevel\b[^\d\n]{0,20}(\d{1,3})", text)
    if m:
        out["level"] = int(m.group(1))
    m = re.search(r"\bStage\b[^\S\n]*(?:\*\*)?\s*([IVX]{1,4}|\d{1,2})\b", text)
    if m:
        s = m.group(1)
        out["stage"] = ROMAN.index(s) + 1 if s in ROMAN else int(s)
    owners: dict[str, list[str]] = {}
    for p, subs in cx["subs"].items():
        for sname in subs:
            owners.setdefault(sname, []).append(p)
    current = None  # the Primary whose section we are in (Stability belongs to two)
    for line in text.splitlines():
        for p in cx["subs"]:
            if re.search(r"(?<![A-Za-z])" + p + r"(?![a-z])", line):
                current = p
                break
        # "**Fortitude** 310", "Fortitude: 310", "| Fortitude | 310 |", "Fortitude 310 ·"
        for name, val in STAT_LINE.findall(line):
            if name in owners:
                p = current if current in owners[name] else owners[name][0]
                out["subs"].setdefault((p, name), int(val))
            elif name in cx["subs"] and name not in out["primaries_stated"]:
                out["primaries_stated"][name] = int(val)
    return out


def check(text: str) -> dict:
    """{ok: bool, findings: [(level, text)], summary: str}; level is 'fail' | 'warn' | 'ok'."""
    cx = F.canon()
    d = parse(text)
    f = []
    level, stage = d["level"], d["stage"]
    if level is None:
        f.append(("fail", "No **Level** found on the sheet."))
    if stage is None:
        f.append(("fail", "No **Stage** found (a Temperance Stage, I–XIV)."))
    if level is not None and stage is not None and 1 <= stage <= 14:
        gate = F.stage_gate(level)
        if stage < gate:
            f.append(("fail", f"Level {level} cannot be surpassed below Stage {ROMAN[gate - 1]} (the Band gate); Stage {ROMAN[stage - 1]} is a forced progression."))
        st = cx["stages"][stage - 1]
        max_grade = re.match(r"^[A-Z]+\+?", st["max_grade"]).group()
        grade_top = next((g["hi"] for g in cx["grades"] if g["grade"] == max_grade), st["ceiling"])
        lvl_pts = sum(max(0, min(level, b["hi"]) - b["lo"] + 1) * b["pts"] for b in cx["bands"])
        thr_pts = sum(s * 100 for s in range(1, stage + 1))
        pool = lvl_pts + thr_pts
        subs = d["subs"]
        if not subs:
            f.append(("fail", "No Sub-Stat values found. The canon model (R39-1) spends points on Sub-Stats; a Primary is their total."))
        else:
            spent = sum(v for (p, k), v in subs.items() if k != "Throne")
            missing = [f"{p}/{s}" for p, ss in cx["subs"].items() for s in ss if (p, s) not in subs and s != "Throne"]
            f.append(("ok" if spent <= pool else "fail",
                      f"Points on Sub-Stats: **{spent:,}** of a pool of **{pool:,}** ({lvl_pts:,} levelling + {thr_pts:,} Thresholds, Stage I counting — R39-3)."))
            over = [(s, v) for (p, s), v in subs.items() if s != "Throne" and v > grade_top]
            if over:
                f.append(("fail", f"Above the Stage's Max Grade top of {grade_top:,} (R39-4): " + ", ".join(f"{s} {v}" for s, v in over[:8])))
            if missing:
                f.append(("warn", f"{len(missing)} Sub-Stat(s) not listed (the sheet should carry all sixty-three; Throne aside): "
                                  + ", ".join(missing[:10]) + ("…" if len(missing) > 10 else "")))
            for p, ss in cx["subs"].items():
                vals = [subs[(p, s)] for s in ss if (p, s) in subs and s != "Throne"]
                if not vals:
                    continue
                total, n = sum(vals), (7 if p == "Dominion" else 8)
                mean = total / n
                g = F.grade_of(mean)
                stated = d["primaries_stated"].get(p)
                if stated is not None and abs(stated - total) > 1:
                    f.append(("fail", f"**{p}** is stated as {stated:,} but its Sub-Stats total {total:,}; the Primary is the sum (R39-1)."))
                else:
                    f.append(("ok", f"**{p}** {total:,} · mean {mean:,.0f} · {g}-Grade" + (" (÷7, Throne excluded — R39-2)" if p == "Dominion" else "")))
    # names
    hits = []
    for old, new in M._reversion_map():
        if len(old) >= 4 and re.search(r"(?<!\w)" + re.escape(old) + r"(?!\w)", text):
            hits.append(f"**{old}** → {new}")
    if hits:
        f.append(("fail", "Struck names or terms (the Moto Reversion Ledger; R22, R21-1, R23-1): " + "; ".join(hits[:8])))
    # terms
    canon_stage_names = {s["name"] for s in cx["stages"]}
    for name in re.findall(r"\bStage\s+[IVX\d]+\s*[—–-]\s*([A-Z][a-z]+)", text):
        if name not in canon_stage_names:
            f.append(("fail", f"Stage name **{name}** is not the Living System's (R14-5); the sixteen are {', '.join(sorted(canon_stage_names))}."))
    for g in re.findall(r"\b([A-Z]{1,3}\+?)-Grade\b", text):
        if g not in GRADES:
            f.append(("fail", f"Grade **{g}** is not on the Grade table (R14-5)."))
    fails = [x for x in f if x[0] == "fail"]
    warns = [x for x in f if x[0] == "warn"]
    return {"ok": not fails, "findings": f, "level": level, "stage": stage,
            "summary": ("passes" if not fails else f"{len(fails)} problem(s)") + (f", {len(warns)} warning(s)" if warns else "")}
