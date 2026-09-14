"""/stats: a Fracture of Worlds stat block built the canon way.

Source: the wiki pages of "Fracture of Worlds — The Living System" (the consolidated
64-Sub-Stat system), not the older codex workbook:
  I.  Levels, Experience and Stat Points — points per level and the concentration cap by Band,
      Stage x 100 Threshold bonuses, the ceiling binding each Sub-Stat, Grade read off the mean.
  II. Grades, Gates and Thresholds — the Grade table and the Stage table.
  IV. The Eight Primaries and the Sixty-Four Sub-Stats — the Sub-Stat names.
Points are spent on Sub-Stats only; a Primary is the total of its eight and its Grade is the
mean. Throne carries no ceiling and is excluded from the Dominion total. The only randomness
is which Sub-Stats a build favours and by how much.
"""
import random
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOW_DIR = ROOT / "wiki" / "Fracture of Worlds — The Living System"
PAGE_POINTS = FOW_DIR / "I. Levels, Experience and Stat Points (Parts One–Three).md"
PAGE_GRADES = FOW_DIR / "II. Grades, Gates and Thresholds (Parts Four–Ten).md"
PAGE_SUBS = FOW_DIR / "IV. The Eight Primaries and the Sixty-Four Sub-Stats (Part Twelve).md"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI"]
UNCAPPED = {"Throne"}


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _int(s: str) -> int:
    return int(re.search(r"[\d,]+", s).group().replace(",", ""))


def _read(p: Path) -> str:
    t = p.read_text(encoding="utf-8", errors="replace")
    if t.startswith("---\n"):
        end = t.find("\n---\n", 4)
        if end != -1:
            t = t[end + 5:]
    return t


@lru_cache(maxsize=1)
def canon() -> dict:
    bands, grades, stages, subs = {}, [], [], {}
    # Page I: Band level ranges (the XP table) and the points / concentration-cap table.
    for line in _read(PAGE_POINTS).split("\n"):
        if not line.startswith("|"):
            continue
        c = _cells(line)
        if len(c) >= 3 and c[0] in ROMAN:
            if re.match(r"^\d+[–-]\d+$", c[1]):
                lo, hi = (int(x) for x in re.split(r"[–-]", c[1]))
                bands.setdefault(c[0], {})["lo"], bands[c[0]]["hi"] = lo, hi
            elif c[1].isdigit() and c[2].isdigit():
                bands.setdefault(c[0], {})["pts"], bands[c[0]]["cap"] = int(c[1]), int(c[2])
    # Page II: the Grade table (Sub-Stat value ranges) and the Stage table.
    for line in _read(PAGE_GRADES).split("\n"):
        if not line.startswith("|"):
            continue
        c = _cells(line)
        if len(c) >= 2 and re.match(r"^(Hollow|[A-Z]+\+?)$", c[0]) and c[1] != "Sub-Stat value":
            m = re.match(r"^([\d,]+)(?:[–-]([\d,]+)|\+)", c[1])
            if m and not any(g["grade"] == c[0] for g in grades):
                grades.append({"grade": c[0], "lo": _int(m.group(1)), "hi": _int(m.group(2)) if m.group(2) else 10**9})
        if (len(c) >= 4 and c[0] in ROMAN and re.match(r"^[A-Z][a-z]+$", c[1]) and re.match(r"^([A-Z]+\+?|uncapped)", c[2])
                and re.search(r"\d", c[3]) and not any(s["roman"] == c[0] for s in stages)):
            stages.append({"n": ROMAN.index(c[0]) + 1, "roman": c[0], "name": c[1], "max_grade": c[2],
                           "ceiling": _int(c[3]), "standing": c[4] if len(c) > 4 else ""})
    # Page IV: the sixty-four Sub-Stats under their Primaries.
    prim = None
    for line in _read(PAGE_SUBS).split("\n"):
        m = re.match(r"^###\s+[IVX]+\.\s+(\w+)", line)
        if m:
            prim = m.group(1)
            subs[prim] = []
            continue
        if line.startswith("### "):
            prim = None
        m = re.match(r"^\*\*([A-Z][\w-]+)\*\*\s+[—–-]", line)
        if prim and m and len(subs[prim]) < 8:
            subs[prim].append(m.group(1))
    order = [b for b in ROMAN if b in bands]
    return {"bands": [dict(name=b, **bands[b]) for b in order], "grades": grades,
            "stages": [s for s in stages if s["n"] <= 14], "subs": subs}


def band_for(level: int) -> dict:
    return next(b for b in canon()["bands"] if b["lo"] <= level <= b["hi"])


def natural_stage(level: int) -> int:
    """The Stage a Level usually sits at: the Band's cluster (I-IV, V-VII, VIII-X, XI-XII, XIII-XIV) at the same proportion."""
    clusters = [(1, 4), (5, 7), (8, 10), (11, 12), (13, 14)]
    b = band_for(level)
    lo, hi = clusters[ROMAN.index(b["name"])]
    frac = (level - b["lo"]) / max(1, b["hi"] - b["lo"])
    return min(hi, lo + int(frac * (hi - lo + 1)))


def stage_gate(level: int) -> int:
    """Stage IV before Level 100 is surpassed, VII before 200, X before 300, XII before 400."""
    gates = [4, 7, 10, 12]
    gate = 1
    for b, g in zip(canon()["bands"][:-1], gates):
        if level > b["hi"]:
            gate = g
    return gate


def grade_of(value: float) -> str:
    for g in canon()["grades"]:
        if g["lo"] <= value <= g["hi"]:
            return g["grade"]
    return "Hollow"


def build(level: int, stage: int | None = None, lean: str | None = None, seed: int | None = None) -> dict:
    cx = canon()
    level = max(1, min(level, cx["bands"][-1]["hi"]))
    stage = stage or natural_stage(level)
    st = cx["stages"][stage - 1]
    rng = random.Random(seed)
    flags = []
    gate = stage_gate(level)
    if stage < gate:
        flags.append(f"Level {level} cannot be surpassed below Stage {ROMAN[gate - 1]}; at Stage {st['roman']} this is a forced progression and the Crystal fractures until the Threshold is passed.")
    # Part Three: the pool and the per-Sub-Stat concentration cap.
    lvl_pts = cap_pts = 0
    for b in cx["bands"]:
        n = max(0, min(level, b["hi"]) - b["lo"] + 1)
        lvl_pts += n * b["pts"]
        cap_pts += n * b["cap"]
    thr_pts = sum(s * 100 for s in range(1, stage + 1))
    pool = lvl_pts + thr_pts
    ceiling = st["ceiling"]
    # R39-4 (C-011): the Stage's Max Grade letter binds allocation; the band up to the numeric
    # ceiling is the instability zone, reachable only under strain, never by spending points.
    max_grade = re.match(r"^[A-Z]+\+?", st["max_grade"]).group()
    grade_top = next((g["hi"] for g in cx["grades"] if g["grade"] == max_grade), ceiling)
    sub_max = min(grade_top, ceiling, cap_pts + thr_pts)  # Threshold points are free of the concentration cap
    # The build: a lean Primary, a handful of favoured Sub-Stats, the rest spread thin.
    prim = list(cx["subs"])
    lean = lean if lean in prim else rng.choice(prim)
    spendable = [(p, s) for p in prim for s in cx["subs"][p] if s not in UNCAPPED]
    n_fav = rng.randint(8, 16)
    fav = set(rng.sample([ps for ps in spendable if ps[0] == lean], k=4) + rng.sample(spendable, k=n_fav))
    w = {}
    for ps in spendable:
        base = rng.gammavariate(4.0, 1.0)
        if ps in fav:
            base *= rng.uniform(3.0, 6.0)
        if ps[0] == lean:
            base *= 1.5
        w[ps] = base
    tot = sum(w.values())
    raw = {ps: pool * wi / tot for ps, wi in w.items()}
    for _ in range(12):  # the ceiling binds the Sub-Stat; refused points are re-offered to entries with room
        spill = 0.0
        for ps in spendable:
            if raw[ps] > sub_max:
                spill += raw[ps] - sub_max
                raw[ps] = sub_max
        room = [ps for ps in spendable if raw[ps] < sub_max - 1e-9]
        if spill < 0.5 or not room:
            break
        wsum = sum(w[r] for r in room)
        for ps in room:
            raw[ps] += spill * w[ps] / wsum
    vals = {ps: int(raw[ps]) for ps in spendable}
    left = int(pool) - sum(vals.values())  # rounding remainder, placed one point at a time where there is room
    for ps in sorted(spendable, key=lambda ps: -raw[ps]):
        if left <= 0:
            break
        if vals[ps] < sub_max:
            vals[ps] += 1
            left -= 1
    spent = sum(vals.values())
    unheld = int(pool) - spent
    order = {g["grade"]: i for i, g in enumerate(cx["grades"])}
    unstable = {5: 320, 11: 700}.get(stage)
    rows = []
    for p in prim:
        entries = [(s, vals.get((p, s))) for s in cx["subs"][p]]
        counted = [v for s, v in entries if v is not None]
        total = sum(counted)
        mean = total / max(1, len(counted))
        g = grade_of(mean)
        rows.append({"primary": p, "total": total, "mean": mean, "grade": g, "entries": entries,
                     "over": order.get(g, 0) > order.get(max_grade, 99),
                     "unstable": [s for s, v in entries if v is not None and unstable and v > unstable]})
    rows.sort(key=lambda r: -r["total"])
    return {"level": level, "band": band_for(level), "stage": st, "pool": pool, "lvl_pts": lvl_pts, "thr_pts": thr_pts,
            "sub_max": sub_max, "grade_top": grade_top, "spent": spent, "unheld": unheld, "rows": rows, "lean": lean, "flags": flags,
            "unstable_above": unstable}


def primaries() -> list[str]:
    return list(canon()["subs"])
