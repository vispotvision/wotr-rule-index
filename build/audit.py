#!/usr/bin/env python3
"""Archive-wide audits: the prose-law pass, recurrence tracking, the timeline
skeleton, card-to-scene consistency, wiki duplicates, and the pack impact check.

  python build/audit.py prose        -> reports/prose_pass_<date>.md
  python build/audit.py recurrence   -> reports/recurrence_<date>.md
  python build/audit.py timeline     -> scenes/TIMELINE.md (skeleton, kept if present)
  python build/audit.py reconcile    -> reports/reconcile_<date>.md
  python build/audit.py impact <pack.md>   -> which live rules a new pack's text touches
"""
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENES = ROOT / "scenes"
WIKI = ROOT / "wiki"
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "build"))
import verify  # noqa: E402
from common import load_rules  # noqa: E402

SKIP = {"MANIFEST.md", "CAST.md", "ARCS.md", "TIMELINE.md", "00_SUPERSEDED_wrong_names.md", "THE_KINGDOM_OF_KHARVEN_buri.md", "WOTR_AI_Writing_Tells_to_Avoid.md"}


def scenes() -> list[Path]:
    return sorted(p for p in SCENES.glob("*.md") if p.name not in SKIP)


def _read(p: Path) -> str:
    t = p.read_text(encoding="utf-8", errors="replace")
    if t.startswith("---\n"):
        end = t.find("\n---\n", 4)
        if end != -1:
            t = t[end + 5:]
    return t


def report(name: str, lines: list[str]) -> Path:
    REPORTS.mkdir(exist_ok=True)
    p = REPORTS / f"{name}_{date.today().isoformat()}.md"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return p


# --------------------------------------------------------------------------


def prose_pass() -> Path:
    lines = ["# Prose-law pass over the scene archive", "", "Every FAIL is a hard rule; every WARN needs a read. Nothing was edited. Run `verify_scene` on a scene before revising it.", ""]
    totals = Counter()
    rows = []
    for p in scenes():
        text = _read(p)
        combat = bool(re.search(r"\b(?:Vor|Nach|Indes|parry|riposte|blade|cut|thrust|wound)\b", text))
        kharven = bool(re.search(r"\bKharven\b", text))
        res = verify.run(text, combat=combat, culture="Kharven" if kharven else None, band="set-piece" if len(text.split()) >= 2500 else "standard")
        totals["fails"] += len(res["fails"]); totals["warns"] += len(res["warns"])
        rows.append((len(res["fails"]), len(res["warns"]), p.name, res))
    rows.sort(key=lambda r: (-r[0], -r[1]))
    lines.append(f"{len(rows)} scenes: {totals['fails']} FAIL, {totals['warns']} WARN.")
    lines.append("")
    lines.append("| scene | FAIL | WARN |")
    lines.append("|---|---|---|")
    lines += [f"| {n} | {f} | {w} |" for f, w, n, _ in rows]
    lines.append("")
    for f, w, n, res in rows:
        if not res["fails"] and not res["warns"]:
            continue
        lines.append(f"## {n}")
        lines += [f"- FAIL {x}" for x in res["fails"]]
        lines += [f"- WARN {x}" for x in res["warns"]]
        lines.append("")
    return report("prose_pass", lines)


def recurrence() -> Path:
    items = verify.KHARVEN_RECURRENCE
    counts = {k: Counter() for k in items}
    kh = []
    for p in scenes():
        text = _read(p)
        if not re.search(r"\bKharven\b", text):
            continue
        kh.append(p.name)
        for k, rx in items.items():
            n = len(rx.findall(text))
            if n:
                counts[k][p.name] = n
    lines = ["# Recurrence tracking — Kharven signature items across the archive", "",
             f"{len(kh)} scenes mention Kharven. Minimum two items per Kharven scene (R6-9-RECURRENCE_RULE); an item in half the scenes is a signature, an item in one is a stray, an item in none is dead weight.", "",
             "| item | scenes carrying it | total mentions |", "|---|---|---|"]
    for k, c in counts.items():
        lines.append(f"| {k} | {len(c)} / {len(kh)} | {sum(c.values())} |")
    lines.append("")
    lines.append("## Per scene")
    lines.append("")
    for n in kh:
        present = [k for k, c in counts.items() if n in c]
        flag = "" if len(present) >= 2 else "  **← under the minimum**"
        lines.append(f"- {n}: {', '.join(present) or 'none'}{flag}")
    return report("recurrence", lines)


DATE_RX = re.compile(r"\b(?:Year\s+\d{1,4}|the (?:Thin Weeks|ninth hour|eleventh year|first week)|[Ee]leven (?:months|days|years)|[Ff]ourteen(?:th)?|(?:Imperial|Withering|Reconstruction|Voyager)\s+(?:Age|Era|Year)|\d{1,4}\s+(?:days|months|years)\s+(?:after|before|since|later|out))\b")


def timeline() -> Path:
    out = SCENES / "TIMELINE.md"
    if out.exists():
        return out
    arcs = SCENES / "ARCS.md"
    order = re.findall(r"(?m)^-\s+(\S+\.md)", arcs.read_text(encoding="utf-8")) if arcs.exists() else []
    files = sorted(scenes(), key=lambda p: (order.index(p.name) if p.name in order else len(order), p.name))
    lines = ["# Timeline", "", "One line per scene, in reading order, with the in-world moment as far as the text states it. Fill the blanks; a new scene whose events precede something it references is a continuity error.", "",
             "| # | scene | in-world moment (from the text) | placed |", "|---|---|---|---|"]
    for i, p in enumerate(files, 1):
        text = _read(p)
        hits = [m.group(0) for m in DATE_RX.finditer(text)]
        top = ", ".join(dict.fromkeys(hits).keys()) if hits else ""
        title = re.search(r"(?m)^#\s+(.+)$", text)
        sub = re.search(r"(?m)^\*(.{10,140}?)\*\s*$", text)
        moment = (sub.group(1) if sub else "")[:120]
        lines.append(f"| {i} | {p.name} | {moment or top or ''} | ____ |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return out


STAGE_RX = re.compile(r"\bStage\s+([IVX]{1,4})\b")
LEVEL_RX = re.compile(r"\bLevel\s+(\d{1,3})\b")


def reconcile() -> Path:
    lines = ["# Reconcile — wiki vs scenes vs index", "", "Mechanical checks only; each finding is a place for a human read.", ""]
    # 1. duplicate wiki page titles
    m = json.loads((WIKI / ".manifest.json").read_text(encoding="utf-8"))
    titles = Counter(v["title"] for v in m.values())
    dups = [t for t, n in titles.items() if n > 1]
    lines += ["## Duplicate wiki pages (same title twice)", ""] + ([f"- {t} ×{titles[t]}" for t in dups] or ["- none"]) + [""]
    # 2. card Stage/Level vs scene mentions
    cards = {}
    for v in m.values():
        p = WIKI / v["rel"]
        if not p.exists() or "Character Cards" not in v["rel"]:
            continue
        t = _read(p)
        st = STAGE_RX.search(t); lv = LEVEL_RX.search(t)
        name = re.split(r"\s+[·—]\s+", v["title"])[0].strip()
        cards[name] = (st.group(1) if st else None, lv.group(1) if lv else None, v["rel"])
    lines += ["## Card vs scene: Stage or Level stated differently", ""]
    found = 0
    for p in scenes():
        text = _read(p)
        for name, (st, lv, rel) in cards.items():
            first = name.split()[0]
            if len(first) < 4 or not re.search(r"(?<!\w)" + re.escape(first) + r"(?!\w)", text):
                continue
            for mm in re.finditer(re.escape(first) + r"[^.\n]{0,80}?\bStage\s+([IVX]{1,4})\b", text):
                if st and mm.group(1) != st:
                    lines.append(f"- {p.name}: {name} at Stage {mm.group(1)} in the scene, Stage {st} on the card ({rel})"); found += 1
            for mm in re.finditer(re.escape(first) + r"[^.\n]{0,80}?\bLevel\s+(\d{1,3})\b", text):
                if lv and mm.group(1) != lv:
                    lines.append(f"- {p.name}: {name} at Level {mm.group(1)} in the scene, Level {lv} on the card ({rel})"); found += 1
    if not found:
        lines.append("- none found by pattern (Stage/Level within 80 characters of a first name)")
    lines.append("")
    # 3. Wellspring assigned to two Families across the wiki
    fam_pages = list((WIKI / "The Eight Families & the Sixty Wellsprings").glob("*.md"))
    ws_family = {}
    for fp in fam_pages:
        fam = fp.stem.split(" — ")[0]
        for n in re.findall(r"(?m)^###\s+(.+?)\s*·", _read(fp)):
            ws_family[n.strip("* ")] = fam
    lines += ["## Wellsprings named with a Family other than their own", ""]
    bad = 0
    for v in m.values():
        p = WIKI / v["rel"]
        if not p.exists():
            continue
        t = _read(p)
        for ws, fam in ws_family.items():
            for mm in re.finditer(r"\*\*" + re.escape(ws) + r"\*\*\s*·\s*([A-Z][a-z]+)\b", t):
                if mm.group(1) != fam and mm.group(1) in set(ws_family.values()):
                    lines.append(f"- {v['rel']}: {ws} · {mm.group(1)} (Family page says {fam})"); bad += 1
    if not bad:
        lines.append("- none")
    lines.append("")
    # 4. stale names still present anywhere (the sweep's residue)
    lines += ["## Stale-register residue", "", "Run WOTR MCP `stale_names` for the live list; this report does not duplicate it.", ""]
    return report("reconcile", lines)


def impact(pack_path: str) -> Path:
    text = Path(pack_path).read_text(encoding="utf-8", errors="replace")
    words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z\-]{4,}", text))
    stop = set("which there their about would could should these those where being after before while other every under between through against because still never always might".split())
    words -= stop
    hits = []
    for r in load_rules():
        if r.get("status") != "live":
            continue
        rw = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z\-]{4,}", r["summary"] + " " + r["verbatim"]))
        rare = [w for w in (rw & words) if len(w) >= 7]
        if len(rare) >= 4:
            hits.append((len(rare), r["id"], r["title"], sorted(rare)[:8]))
    hits.sort(key=lambda h: -h[0])
    lines = [f"# Pack impact — {Path(pack_path).name}", "", f"{len(hits)} live rules share four or more distinctive terms with this text. Read each against the pack before extraction; a strike or a contradiction needs quotable words.", ""]
    lines += [f"- **{rid}** ({n}) {title} — {', '.join(terms)}" for n, rid, title, terms in hits[:60]]
    return report("impact_" + Path(pack_path).stem, lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prose"
    if cmd == "prose":
        print(prose_pass())
    elif cmd == "recurrence":
        print(recurrence())
    elif cmd == "timeline":
        print(timeline())
    elif cmd == "reconcile":
        print(reconcile())
    elif cmd == "impact":
        print(impact(sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
