#!/usr/bin/env python3
"""R38-2: re-cost the originated character sheets to Part Three's current allotment.

  python build/recost.py                # dry run: reports/recost_<date>.md, nothing written
  python build/recost.py --apply        # edit the Notion cards block by block, refresh the mirror
  python build/recost.py --only Gorrath # one card

What it does to a card that states its pool on the old figures (a "Total lifetime pool" line,
"Band III at 30 per level"):
  1. reads Level and Stage; computes the current pool: 12/15/18/21/24 a Level by Band plus
     Stage x 100 per Threshold, Stage I counting (R39-3); ratio = current / stated.
  2. scales every stat number that follows a Primary or Sub-Stat name (tables, peaks, prose)
     by the ratio, rounded; caps a Sub-Stat, and a Primary's mean-scale figure, at the top of
     the Stage's Max Grade bracket (R39-4); re-derives the Grade letter that follows a value.
  3. rewrites the pool line and the "point economy, worked" paragraph to the current figures,
     marking the re-cost, and recomputes Allocated / Unspent from the scaled listed numbers.
  The card keeps its two-layer shape (Primaries and listed peaks) for verification, as the
  C-014 record proposed; the sixty-four-entry table is not invented. R38-1's Path gates need
  a Path commitment the cards do not state; they are listed in the report, not applied.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
sys.path.insert(0, str(ROOT / "bot"))
import notion_edit as NE  # noqa: E402
from notion_export import api  # noqa: E402
import fow as F  # noqa: E402  (bot/fow.py: the Living System's tables)

WIKI = ROOT / "wiki"
MANIFEST = json.loads((WIKI / ".manifest.json").read_text(encoding="utf-8"))
ROMAN = F.ROMAN
CARD_DIRS = [d for d in WIKI.glob("Volume * Character Cards")]
GRADE_RX = r"(?:Hollow|EX\+|EX|SSS|SS|S|X|A|B|C|D|E|F)"


def candidates(only: str | None) -> list[Path]:
    out = []
    for d in CARD_DIRS:
        for p in sorted(d.glob("*.md")):
            t = p.read_text(encoding="utf-8", errors="replace")
            if re.search(r"Total lifetime pool", t) and (only is None or only.lower() in p.stem.lower()):
                out.append(p)
    return out


def merge_ledger() -> dict[str, str]:
    """Part Twelve's Merge Ledger: retired Sub-Stat name -> the entry that absorbed it."""
    page = WIKI / "Fracture of Worlds — The Living System" / "IV. The Eight Primaries and the Sixty-Four Sub-Stats (Part Twelve).md"
    out = {}
    for line in page.read_text(encoding="utf-8", errors="replace").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 3 and c[0] in F.canon()["subs"] and c[1] not in ("Retired", "---") and not c[1].startswith("-"):
            for r in c[1].split(","):
                out.setdefault(r.strip(), []).append(f"{c[0]} {c[2]}")
    current = {x for ss in F.canon()["subs"].values() for x in ss}
    return {k: v for k, v in out.items() if k not in current}   # a name still current (Ardency Density) is not retired


def stat_names() -> tuple[list[str], set[str]]:
    cx = F.canon()
    return list(cx["subs"]), {s for ss in cx["subs"].values() for s in ss} | set(merge_ledger())


def current_pool(level: int, stage: int) -> tuple[int, int, int, str]:
    cx = F.canon()
    lvl = sum(max(0, min(level, b["hi"]) - b["lo"] + 1) * b["pts"] for b in cx["bands"])
    thr = sum(s * 100 for s in range(1, stage + 1))
    parts = []
    for b in cx["bands"]:
        n = max(0, min(level, b["hi"]) - b["lo"] + 1)
        if n:
            parts.append(f"Band {b['name']} at {b['pts']} a Level across {b['lo']}–{min(level, b['hi'])} contributes {n * b['pts']:,}")
    worked = ". ".join(parts) + f". Threshold bonuses for Stages I through {ROMAN[stage - 1]} contribute {thr:,}, Stage I counting (R39-3)."
    return lvl + thr, lvl, thr, worked


def grade_top(stage: int) -> int:
    cx = F.canon()
    st = cx["stages"][stage - 1]
    letter = re.match(r"^[A-Z]+\+?", st["max_grade"]).group()
    return next((g["hi"] for g in cx["grades"] if g["grade"] == letter), st["ceiling"])


def block_md(b: dict) -> str:
    t = b["type"]
    out = ""
    for o in b[t].get("rich_text", []):
        txt = o.get("plain_text", "")
        a = o.get("annotations", {})
        if a.get("bold") and a.get("italic"):
            txt = f"***{txt}***"
        elif a.get("bold"):
            txt = f"**{txt}**"
        elif a.get("italic"):
            txt = f"*{txt}*"
        out += txt
    return out


def rich_text(md: str) -> list:
    out = []
    for tok in re.split(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*.+?\*)", md):
        if not tok:
            continue
        ann = {}
        if tok.startswith("***") and tok.endswith("***") and len(tok) > 6:
            tok, ann = tok[3:-3], {"bold": True, "italic": True}
        elif tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            tok, ann = tok[2:-2], {"bold": True}
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            tok, ann = tok[1:-1], {"italic": True}
        run = {"type": "text", "text": {"content": tok}}
        if ann:
            run["annotations"] = ann
        out.append(run)
    return out


class Recost:
    def __init__(self, level: int, stage: int, stated_pool: int):
        self.level, self.stage, self.stated = level, stage, stated_pool
        self.pool, self.lvl_pts, self.thr_pts, self.worked = current_pool(level, stage)
        self.ratio = self.pool / stated_pool
        self.cap = grade_top(stage)
        self.prim, self.subs = stat_names()
        self.names = set(self.prim) | self.subs
        self.retired = merge_ledger()
        self.changes: list[tuple[str, int, int, str]] = []   # (name, old, new, where)
        self.listed_new: list[int] = []
        self.first: dict[str, int] = {}   # name -> new value, first sighting (the table, then peaks); the allocation
        self.alloc: int | None = None

    def scale(self, v: int) -> int:
        return min(int(round(v * self.ratio)), self.cap)

    def _num_after_name(self, m: re.Match, where: str) -> str:
        name, sep, num, tail = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        old = int(num.replace(",", ""))
        new = self.scale(old)
        self.changes.append((name, old, new, where))
        self.listed_new.append(new)
        self.first.setdefault(name, new)
        out = f"{name}{sep}{new:,}"
        # a Grade letter riding on the number: "| 542 | S |", "358, A-Grade", "542 (S)"
        g = F.grade_of(new)
        tail2 = re.sub(rf"^(\s*\|\s*\**)({GRADE_RX})(\**\s*\|)", lambda mm: mm.group(1) + g + mm.group(3), tail)
        tail2 = re.sub(rf"^(,\s*){GRADE_RX}(-Grade)", lambda mm: mm.group(1) + g + mm.group(2), tail2)
        tail2 = re.sub(rf"^(\s*\(){GRADE_RX}(\))", lambda mm: mm.group(1) + g + mm.group(2), tail2)
        return out + tail2

    def rewrite(self, md: str, where: str) -> str:
        if "Temperance Stage" in md or "Coherence Band" in md:
            # the card's header line: Level, Band, Grade and the Stage ceiling live here, not stats
            return md
        names = "|".join(sorted(self.names, key=len, reverse=True))
        rx = re.compile(rf"\b({names})\b(\**\s*[:·|]?\s*\**)(\d{{1,3}}(?:,\d{{3}})?|\d{{2,4}})(?!\s*[/%–-]\d)(?!\s*(?:EU|m/s|kJ|MJ|GJ|TJ|J|kg|km|kt|m|%|Hz))(\s*\|\s*\**{GRADE_RX}\**\s*\||,\s*{GRADE_RX}-Grade|\s*\({GRADE_RX}\))?")
        md2 = rx.sub(lambda m: self._num_after_name(m, where), md)
        return md2

    def pool_line(self, md: str) -> str | None:
        m = re.search(r"Total lifetime pool:\s*\**\s*([\d,]+)", md)
        if not m:
            return None
        alloc = self.alloc if self.alloc is not None else sum(self.first.values())
        unspent = max(0, self.pool - alloc)
        new = re.sub(r"(Total lifetime pool:\s*\**\s*)[\d,]+", lambda mm: mm.group(1) + f"{self.pool:,}", md, count=1)
        new = re.sub(r"(Allocated(?: below)?:\s*\**\s*)[\d,]+", lambda mm: mm.group(1) + f"{alloc:,}", new, count=1)
        new = re.sub(r"(Unspent:\s*\**\s*)[\d,]+", lambda mm: mm.group(1) + f"{unspent:,}", new, count=1)
        if "re-costed" not in new:
            new = new.rstrip() + f" *Re-costed to Part Three's current allotment (R38-2, 2026-09-13; the sheet's pool was {self.stated:,}).*"
        return new

    def worked_line(self, md: str) -> str | None:
        if "point economy, worked" not in md.lower() and "per level" not in md.lower():
            return None
        head = re.match(r"^(.*?point economy, worked\.\*\*\s*)", md, re.S)
        prefix = head.group(1) if head else ""
        return prefix + self.worked + f" Total: {self.pool:,}."


def process_card(path: Path, apply: bool, report: list[str]) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    m_lvl = re.search(r"\*\*Level\*\*\s*·\s*(\d+)", text) or re.search(r"\bLevel\b[^\d\n]{0,12}(\d{1,3})", text)
    m_stg = re.search(r"Temperance Stage\*\*\s*·\s*\**\s*([IVX]+)", text) or re.search(r"\bStage\s+([IVX]{1,4})\b", text)
    m_pool = re.search(r"Total lifetime pool:\s*\**\s*([\d,]+)", text)
    if not (m_lvl and m_stg and m_pool):
        report.append(f"## {path.stem}\n\n- skipped: could not read Level / Stage / pool ({bool(m_lvl)}, {bool(m_stg)}, {bool(m_pool)})\n")
        return
    level, stage, stated = int(m_lvl.group(1)), ROMAN.index(m_stg.group(1)) + 1, int(m_pool.group(1).replace(",", ""))
    rc = Recost(level, stage, stated)
    if abs(rc.ratio - 1) < 0.01:
        report.append(f"## {path.stem}\n\n- already on the current allotment (pool {stated:,}); nothing to do\n")
        return
    rel = path.relative_to(WIKI).as_posix()
    pid = next((k for k, v in MANIFEST.items() if v["rel"] == rel), None)
    if not pid:
        report.append(f"## {path.stem}\n\n- skipped: no Notion page id in the manifest\n")
        return
    lines = [f"## {path.stem}", "", f"- Level {level}, Stage {ROMAN[stage-1]}; stated pool **{stated:,}** → current pool **{rc.pool:,}** ({rc.lvl_pts:,} levelling + {rc.thr_pts:,} Thresholds); ratio {rc.ratio:.3f}; Sub-Stat cap {rc.cap:,} (R39-4)", ""]
    blocks = list(NE._walk(pid))
    edits = []
    for _pass in (1, 2):
      if _pass == 2:
        rc.alloc = sum(rc.first.values())
        rc.changes, rc.listed_new, edits = [], [], []
      for b in blocks:
          t = b["type"]
          if t == "table_row":
              cells = b["table_row"]["cells"]
              plain_cells = ["".join(o.get("plain_text", "") for o in c) for c in cells]
              row_md = " | ".join(plain_cells)
              words = re.sub(r"[*]", "", plain_cells[0]).split() if plain_cells else []
              name = words[-1] if words and words[-1] in rc.names else (words[0] if words and words[0] in rc.names else "")
              if name in rc.names and len(cells) >= 2 and re.fullmatch(r"[*\s]*[\d,]+[*\s]*", plain_cells[1] or ""):
                  old = int(re.sub(r"[^\d]", "", plain_cells[1]))
                  new = rc.scale(old)
                  rc.changes.append((name, old, new, "table"))
                  rc.listed_new.append(new)
                  rc.first.setdefault(name, new)
                  bold = any(o.get("annotations", {}).get("bold") for o in cells[1])
                  new_cells = list(cells)
                  new_cells[1] = rich_text(f"**{new:,}**" if bold else f"{new:,}")
                  if len(cells) >= 3 and re.fullmatch(rf"[*\s]*{GRADE_RX}[*\s]*", plain_cells[2] or ""):
                      gb = any(o.get("annotations", {}).get("bold") for o in cells[2])
                      g = F.grade_of(new)
                      new_cells[2] = rich_text(f"**{g}**" if gb else g)
                  # peaks or notes in later cells: scale any "Name 1,080" pairs
                  for j in range(3, len(cells)):
                      cmd = "".join((f"**{o['plain_text']}**" if o.get("annotations", {}).get("bold") else o.get("plain_text", "")) for o in cells[j])
                      cmd2 = rc.rewrite(cmd, "table peaks")
                      if cmd2 != cmd:
                          new_cells[j] = rich_text(cmd2)
                  edits.append((b, {"table_row": {"cells": [NE._clean_rt(c) if c is not cells[j] else c for j, c in enumerate(new_cells)]}}, row_md))
              else:
                  changed = False
                  new_cells = []
                  for c in cells:
                      cmd = "".join((f"**{o['plain_text']}**" if o.get("annotations", {}).get("bold") else o.get("plain_text", "")) for o in c)
                      cmd2 = rc.rewrite(cmd, "table")
                      new_cells.append(rich_text(cmd2) if cmd2 != cmd else c)
                      changed |= cmd2 != cmd
                  if changed:
                      edits.append((b, {"table_row": {"cells": [NE._clean_rt(c) if c is not cells[j] else c for j, c in enumerate(new_cells)]}}, row_md))
          elif t in NE.TEXT_TYPES:
              md = block_md(b)
              md2 = rc.rewrite(md, t)
              pl = rc.pool_line(md2)
              if pl:
                  md2 = pl
              wl = rc.worked_line(md2) if "point economy" in md2.lower() else None
              if wl:
                  md2 = wl
              if md2 != md:
                  edits.append((b, {t: {"rich_text": rich_text(md2)}}, md))
    for name, old, new, where in rc.changes:
        retired = f" — retired name; read as {' or '.join(rc.retired[name])} (Merge Ledger)" if name in rc.retired else ""
        lines.append(f"- {name}: {old:,} → {new:,}" + (" (capped)" if new == rc.cap and round(old * rc.ratio) > rc.cap else "") + f"  [{where}]{retired}")
    alloc = sum(rc.first.values())
    lines.append(f"- allocation (each stat once, table then peaks): {alloc:,} against the pool of {rc.pool:,}; unspent {max(0, rc.pool - alloc):,}")
    if alloc > rc.pool:
        lines.append(f"- ⚠ the listed numbers exceed the pool by {alloc - rc.pool:,}: the sheet's own Allocated line did not count every listed stat, or a peak sits above its Primary's scale — for the Judger")
    lines.append(f"- blocks to edit: {len(edits)}")
    lines.append("- R38-1 Path gates: not applied (the card states no Path commitment); listed for the Judger")
    report.append("\n".join(lines) + "\n")
    if apply and edits:
        for b, body, _ in edits:
            api("PATCH", f"/blocks/{b['id']}", body)
        NE.refresh_mirror(pid)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    report = [f"# Re-cost pass (R38-2) — {date.today().isoformat()} — {'APPLIED' if a.apply else 'dry run'}", ""]
    cards = candidates(a.only)
    report.append(f"{len(cards)} card(s) state a lifetime pool.\n")
    for p in cards:
        print("…", p.stem, flush=True)
        process_card(p, a.apply, report)
    out = ROOT / "reports" / f"recost_{date.today().isoformat()}{'_applied' if a.apply else ''}.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
