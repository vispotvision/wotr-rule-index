#!/usr/bin/env python3
"""Put the character-lore pass into Notion.

  python build/lore_publish.py                      # dry run: what would change
  python build/lore_publish.py --apply              # write
  python build/lore_publish.py --apply --only <slug> [<slug> ...]

Each imports/lore/cards/<slug>.md becomes the "Lore · The Life Behind the Card"
section at the foot of that card's Notion page (the page id comes from
imports/lore/_roster.json). A page that already carries the section has it
replaced; nothing above it is touched. imports/lore/THE_WEB.md becomes the page
"The Web of Lives" under Characters. imports/lore/_published.json remembers what
went up, so an unchanged file is skipped. The hourly sync mirrors the pages back
into wiki/.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notion_export import api, paginate  # noqa: E402
from notion_publish import md_to_blocks, create_page, replace_body, BATCH  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LORE = ROOT / "imports" / "lore"
STATE = LORE / "_published.json"
HEAD = "Lore · The Life Behind the Card"
CHARACTERS_PAGE = "3b158200-eb22-8188-b4d8-d9b195f254dd"
WEB_TITLE = "The Web of Lives"


def plain(b: dict) -> str:
    return "".join(t.get("plain_text", "") for t in b.get(b["type"], {}).get("rich_text", []))


def old_section(page_id: str) -> list[str]:
    """Block ids of the existing Lore section (and the divider before it), if any."""
    blocks = list(paginate("GET", f"/blocks/{page_id}/children?page_size=100"))
    for i, b in enumerate(blocks):
        if b["type"].startswith("heading_") and plain(b).strip() == HEAD:
            start = i - 1 if i and blocks[i - 1]["type"] == "divider" else i
            end = next((j for j in range(i + 1, len(blocks))
                        if blocks[j]["type"] in ("heading_1", "heading_2")), len(blocks))
            return [x["id"] for x in blocks[start:end]]
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    roster = {r["slug"]: r for r in json.loads((LORE / "_roster.json").read_text(encoding="utf-8"))}
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    files = sorted((LORE / "cards").glob("*.md"))
    if a.only:
        files = [f for f in files if f.stem in a.only]
    done = skipped = 0
    for f in files:
        md = f.read_text(encoding="utf-8")
        digest = hashlib.sha1(md.encode()).hexdigest()
        row = roster.get(f.stem)
        if not row or not row["notion_id"]:
            print(f"  NO PAGE  {f.stem}")
            continue
        if not md.lstrip().startswith(f"## {HEAD}"):
            print(f"  BAD HEAD {f.stem} (not published)")
            continue
        if state.get(f.stem) == digest:
            skipped += 1
            continue
        pid = row["notion_id"]
        if not a.apply:
            print(f"  would publish {f.stem} -> {row['title']}")
            continue
        for bid in old_section(pid):
            api("DELETE", f"/blocks/{bid}")
        blocks = [{"object": "block", "type": "divider", "divider": {}}] + md_to_blocks(md)
        for i in range(0, len(blocks), BATCH):
            api("PATCH", f"/blocks/{pid}/children", {"children": blocks[i:i + BATCH]})
        state[f.stem] = digest
        STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
        done += 1
        print(f"  published {row['title']}")

    web = LORE / "THE_WEB.md"
    if web.exists() and not a.only:
        md = web.read_text(encoding="utf-8")
        body = md.split("\n", 1)[1] if md.startswith("# ") else md   # the page title carries the H1
        digest = hashlib.sha1(md.encode()).hexdigest()
        if state.get("_web") != digest:
            if not a.apply:
                print(f"  would publish {WEB_TITLE}")
            elif state.get("_web_page"):
                replace_body(state["_web_page"], md_to_blocks(body))
            else:
                state["_web_page"] = create_page({"page_id": CHARACTERS_PAGE}, WEB_TITLE, md_to_blocks(body))
            if a.apply:
                state["_web"] = digest
                STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
                print(f"  published {WEB_TITLE} ({state['_web_page']})")
    print(f"{'published' if a.apply else 'dry run'}: {done} card(s), {skipped} unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
