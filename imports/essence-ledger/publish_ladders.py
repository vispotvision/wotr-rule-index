#!/usr/bin/env python3
"""Publish the nine-rung tier ladders as one Notion page beside the Essence Ledger.

  bash build/py.sh imports/essence-ledger/publish_ladders.py [--apply]

Same pipeline as publish_part.py (unwrap -> md_to_blocks); state in _published_pages.json.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import publish_part as pp  # noqa: E402

SRC = pp.HERE / "the-tier-ladders.edition.md"
TITLE = "X. The Tier Ladders (Part Twenty-Four)"
KEY = "part_twenty_four"


def main() -> int:
    apply = "--apply" in sys.argv
    md = pp.unwrap(SRC.read_text(encoding="utf-8"))
    blocks = pp.md_to_blocks(md)
    print(f"{TITLE}: {len(md.splitlines())} lines -> {len(blocks)} blocks")
    state = json.loads(pp.STATE.read_text(encoding="utf-8")) if pp.STATE.exists() else {}
    existing = state.get(KEY, {}).get("page_id")
    if not apply:
        print("  dry run:", "replace " + existing if existing else "create under " + pp.FOW_PARENT_ID)
        return 0
    if existing:
        pp.replace_body(existing, blocks); pid = existing
    else:
        pid = pp.create_page({"page_id": pp.FOW_PARENT_ID}, TITLE, blocks)
    state[KEY] = {"page_id": pid, "title": TITLE, "source": str(SRC.relative_to(pp.ROOT))}
    pp.STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  published", pid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
