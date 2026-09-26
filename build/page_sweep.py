#!/usr/bin/env python3
"""Collect the page's own blocks (above "The Two Accounts") on the 76 working pages and
flag process wording. Writes a JSON of hits for review; changes nothing.

  bash build/py.sh build/page_sweep.py OUT.json
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import paginate  # noqa: E402
import system_accounts_publish as sap  # noqa: E402
from strip_orphans import last_original, norm, plain  # noqa: E402

PROC = re.compile(r"(?i)\b(the card'?s?|from the card|converted|reassigned|pending|ruling|ruled|unverified|isaac|natalie|claude|"
                  r"C-0\d\d|WAR-\d|R\d\d-\d|flag(ged)?|gap-fill|originated|estimate[sd]?|workbook|trello|the page|"
                  r"\.md\b|wiki/|docket|none documented|not documented|undocumented|legacy|stale|retired|placeholder|TBD|to be (decided|ruled)|"
                  r"conflict|open question|author'?s? note|verif(y|ied))\b")


def main():
    out = []
    for f in sap.accounts():
        key = f"{f.parent.name}/{f.name}"
        md = f.read_text(encoding="utf-8")
        rel, _ = sap.wiki_page(md, key)
        if not rel:
            continue
        pid, title = sap.notion_of(rel)
        tail = last_original(rel)
        blocks = list(paginate("GET", f"/blocks/{pid}/children?page_size=100"))
        o = max((i for i, b in enumerate(blocks) if tail and tail[:30] in norm(plain(b))), default=len(blocks) - 1)
        for b in blocks[:o + 1]:
            t = plain(b)
            hits = sorted({m.group(0).lower() for m in PROC.finditer(t)})
            if hits:
                out.append({"page": key, "page_id": pid, "block_id": b["id"], "type": b["type"],
                            "hits": hits, "text": t})
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(out), "blocks with process wording across", len({x["page"] for x in out}), "pages")


if __name__ == "__main__":
    main()
