#!/usr/bin/env python3
"""The Master Codex, read from the file (R18-6: openpyxl, read-only, never from memory).

  python build/codex.py find <query> [--sheet "Spell Index"] [--limit 8]
  python build/codex.py check draft.md          # checks 37-39 (Pack Eighteen)

The workbook is $WOTR_TRUE_CANON/The Master Codex.xlsx. Sheets: The Pantheon,
Master Glyph Index, Spell Index, Alchemical Index, Lists.
"""
import argparse
import re
import sys
from functools import lru_cache

from common import TRUE_CANON

CODEX = TRUE_CANON / "The Master Codex.xlsx"
NOTES = re.compile(r"^#{2,3} (?:Notes|Author|Added by the gap-fill)", re.M)
GLYPH = re.compile(r"\[([A-Z][A-Za-z']{0,5})\](?!\()")
# v4's coinage hunt: capitalised Latinate shapes a Lists column should know.
COINAGE = re.compile(r"\b[A-Z][a-zé]+(?:atio|antia|orath|ivale|thrae|ilithe|aeon)\b")
STOP = {"Ratio", "Station", "Nation", "Aeon"}


@lru_cache(maxsize=1)
def sheets() -> dict[str, list[tuple]]:
    """{sheet: [header, *rows]}, blank rows dropped. Raises if the file is missing."""
    import openpyxl
    wb = openpyxl.load_workbook(CODEX, read_only=True, data_only=True)
    try:
        return {ws.title: [r for r in ws.iter_rows(values_only=True) if any(c not in (None, "") for c in r)]
                for ws in wb.worksheets}
    finally:
        wb.close()


def lists() -> dict[str, set[str]]:
    rows = sheets()["Lists"]
    hdr = rows[0]
    return {h: {str(r[i]).strip() for r in rows[1:] if i < len(r) and r[i] not in (None, "")}
            for i, h in enumerate(hdr) if h}


def glyphs() -> dict[str, str]:
    """{'[Ab]': name} from the Master Glyph Index."""
    return {str(r[0]).strip(): str(r[1] or "").strip() for r in sheets()["Master Glyph Index"][1:] if r and r[0]}


def _row(hdr: tuple, r: tuple) -> str:
    return "\n".join(f"- **{h}:** {v}" for h, v in zip(hdr, r) if h and v not in (None, ""))


def find(query: str, sheet: str = "", limit: int = 8) -> str:
    q = query.strip().lower()
    if not q:
        return "(empty query)"
    hits = []
    for name, rows in sheets().items():
        if sheet and name.lower() != sheet.lower():
            continue
        hdr = rows[0]
        for r in rows[1:]:
            cells = [str(c).lower() for c in r if c not in (None, "")]
            if not any(q in c for c in cells):
                continue
            exact = any(c == q or c == f"[{q}]" for c in cells[:2])
            hits.append((not exact, name, hdr, r))
    if not hits:
        return f"No Codex row mentions '{query}'" + (f" in {sheet}" if sheet else "") + f". Sheets: {', '.join(sheets())}."
    hits.sort(key=lambda h: h[0])
    out = [f"{len(hits)} Codex row(s) for '{query}'" + (f", first {limit}" if len(hits) > limit else "") + f" (from {CODEX.name}):"]
    for _, name, hdr, r in hits[:limit]:
        title = r[1] if name != "Lists" and len(r) > 1 and r[1] else next(c for c in r if c not in (None, "") and q in str(c).lower())
        out.append(f"\n### {name}: {title}\n{_row(hdr, r)}")
    return "\n".join(out)


def check(text: str) -> str:
    """Checks 37 (controlled vocabulary), 38 (glyph validity), 39 (precedent)."""
    m = NOTES.search(text)
    body = text[:m.start()] if m else text
    proposed = " ".join(l for l in body.splitlines() if re.search(r"\bproposed\b", l, re.I))
    L = lists()
    known = set().union(*L.values())
    G = glyphs()
    known |= set(G.values())
    out, fails = [], 0

    used = sorted({t for t in known if len(t) > 3 and re.search(rf"\b{re.escape(t)}\b", body)})
    unknown = sorted({w for w in COINAGE.findall(body) if w not in known and w not in STOP and w not in proposed})
    if unknown:
        fails += 1
        out.append(f"FAIL 37 controlled vocabulary (R18-7-CHECK37): not on the Lists sheet: {', '.join(unknown)}. "
                   "Correct the term or declare it proposed and name the enumeration checked.")
    else:
        out.append(f"PASS 37 controlled vocabulary: {len(used)} Lists term(s) used" + (f" ({', '.join(used[:12])})" if used else ""))

    toks = sorted({f"[{t}]" for t in GLYPH.findall(body)})
    bad = [t for t in toks if t not in G]
    if not toks:
        out.append("WARN 38 glyph validity: no bracketed glyph tokens in the body")
    elif bad:
        fails += 1
        out.append(f"FAIL 38 glyph validity (R18-7-CHECK38): unknown to the Master Glyph Index: {', '.join(bad)}")
    else:
        out.append(f"PASS 38 glyph validity: {len(toks)} token(s), all in the Master Glyph Index")

    spells = sorted({str(r[1]) for r in sheets()["Spell Index"][1:] if len(r) > 1 and r[1] and str(r[1]) in body})
    out.append("WARN 39 precedent (R18-7-CHECK39, manual): " + (f"Spell Index rows named: {', '.join(spells)}. " if spells else "")
               + "Name the Spell Index rows checked and say new, derivation of a named row, or duplicate.")
    out.append("CLEAN" if not fails else f"{fails} FAIL")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("query")
    f.add_argument("--sheet", default="")
    f.add_argument("--limit", type=int, default=8)
    c = sub.add_parser("check")
    c.add_argument("file")
    a = ap.parse_args()
    if a.cmd == "find":
        print(find(a.query, a.sheet, a.limit))
        return 0
    res = check(open(a.file, encoding="utf-8").read())
    print(res)
    return 1 if res.endswith("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main())
