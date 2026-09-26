#!/usr/bin/env python3
"""Audit the 76 working pages live in Notion. Read-only. Prints one line per page with problems."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import paginate  # noqa: E402
import system_accounts_publish as sap  # noqa: E402
from strip_orphans import plain  # noqa: E402
from page_sweep import PROC  # noqa: E402

OLD = re.compile(r"^\s*[1-5]\s*·\s*(Physical|Stratal|Mechanism|Essence|Counterplay)", re.I)
ACCT = re.compile(r"(?i)^(the phenomenon|the real phenomenon|aether stratum|wellspring stratum|essence stratum|glyph\.|what boundary moves|failure mode|the counterplay routes|the lookup trail|precedent we are not copying|conflicts (logged|added))")
META = re.compile(r"(?i)precedent we are not copying|ichigo|naruto|bleach|jujutsu|anime|jrpg|crpg|we are not copying")


def main():
    rows = []
    for f in sap.accounts():
        key = f"{f.parent.name}/{f.name}"
        rel, _ = sap.wiki_page(f.read_text(encoding="utf-8"), key)
        if not rel:
            rows.append((key, ["no wiki page"])); continue
        pid, _ = sap.notion_of(rel)
        blocks = list(paginate("GET", f"/blocks/{pid}/children?page_size=100"))
        texts = [plain(b) for b in blocks]
        heads = [i for i, b in enumerate(blocks) if b["type"] == "heading_2" and texts[i].strip() == sap.HEAD]
        cut = heads[-1] if heads else len(blocks)
        issues = []
        if len(heads) != 1:
            issues.append(f"{len(heads)} sections")
        old = [texts[i][:30] for i in range(len(blocks)) if blocks[i]["type"].startswith("heading") and OLD.match(texts[i])]
        if old:
            issues.append(f"old headings {old[:2]}")
        stray = [texts[i][:30] for i in range(cut) if ACCT.match(texts[i] or "")]
        if stray:
            issues.append(f"stray account text above section x{len(stray)}")
        proc = sorted({m.group(0).lower() for t in texts for m in PROC.finditer(t)} - {"conflict", "verify", "verified", "retired", "converted"})
        if proc:
            issues.append(f"process words {proc[:6]}")
        meta = sorted({m.group(0).lower() for t in texts for m in META.finditer(t)})
        if meta:
            issues.append(f"meta {meta}")
        if heads:
            sec = texts[cut:]
            hs = [texts[i] for i in range(cut, len(blocks)) if blocks[i]["type"] == "heading_3"]
            if hs[:1] != ["The physical account"]:
                issues.append(f"section not clean ({hs[:1]})")
        rows.append((key, issues))
    bad = [r for r in rows if r[1]]
    for k, i in bad:
        print(f"{k}: " + "; ".join(i))
    print(f"\n{len(rows)} pages, {len(bad)} with problems")


if __name__ == "__main__":
    main()
