#!/usr/bin/env python3
"""Replace a working page's own top (between its title and the write-up) with a card-style
top from imports/page-tops/<Section>/<Title>.md. Dry run unless --apply.

  bash build/py.sh build/replace_tops.py [--apply] [--only NAME ...]
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, paginate  # noqa: E402
from notion_publish import BATCH, md_to_blocks  # noqa: E402
from strip_orphans import plain  # noqa: E402

TOPS = ROOT / "imports" / "page-tops"
SECTION = ("Physics", "The Two Accounts")


def main():
    apply = "--apply" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
    state = json.loads((ROOT / "imports/system-accounts/_published.json").read_text())
    for f in sorted(TOPS.glob("*/*.md")):
        key = f"{f.parent.name}/{f.name}"
        if only and not any(o in key for o in only):
            continue
        pid = state[key]["notion_id"]
        blocks = list(paginate("GET", f"/blocks/{pid}/children?page_size=100"))
        t = next((i for i, b in enumerate(blocks) if b["type"] == "heading_1"), None)
        s = next((i for i, b in enumerate(blocks) if b["type"] == "heading_2" and plain(b).strip() in SECTION), None)
        if t is None or s is None:
            print(f"SKIP {key}: title {t} section {s}"); continue
        if blocks[s - 1]["type"] == "divider":
            s -= 1
        old = blocks[t + 1:s]
        new = md_to_blocks(f.read_text(encoding="utf-8"))
        print(f"{key}: replace {len(old)} blocks with {len(new)}" + (" (applying)" if apply else ""))
        if not apply:
            continue
        for b in old:
            api("DELETE", f"/blocks/{b['id']}")
        after = blocks[t]["id"]
        for i in range(0, len(new), BATCH):
            r = api("PATCH", f"/blocks/{pid}/children", {"children": new[i:i + BATCH], "after": after})
            after = r["results"][-1]["id"]


if __name__ == "__main__":
    main()
