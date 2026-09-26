#!/usr/bin/env python3
"""Put each carded character's ## Voice block on its Notion card (R52), just before the
Temperance section (or the Lore section, or the page end). Skips cards that already have one.

  bash build/py.sh build/add_voice_sections.py [--apply] [--only NAME ...]
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, paginate  # noqa: E402
from notion_publish import md_to_blocks  # noqa: E402
from strip_orphans import plain  # noqa: E402
from system_accounts_publish import notion_of  # noqa: E402

BLOCKS = ROOT / "imports/drafts/voice-blocks"
CARDS = "wiki/Volume I — Character Cards"


def main():
    apply = "--apply" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
    for f in sorted(BLOCKS.glob("*.md")):
        if f.name.startswith("_") or (only and not any(o in f.name for o in only)):
            continue
        card = f"{CARDS}/{f.name}"
        if not (ROOT / card).is_file():
            print("no card ", f.name); continue
        pid, _ = notion_of(card)
        blocks = list(paginate("GET", f"/blocks/{pid}/children?page_size=100"))
        texts = [plain(b).strip() for b in blocks]
        heads = [i for i, b in enumerate(blocks) if b["type"].startswith("heading")]
        old = next((i for i in heads if texts[i] == "Voice"), None)
        if old is not None:                  # an older prose Voice section: replace its body
            end = next((j for j in range(old + 1, len(blocks))
                        if blocks[j]["type"] in ("divider",) or j in heads), len(blocks))
            if apply:
                for b in blocks[old + 1:end]:
                    api("DELETE", f"/blocks/{b['id']}")
                lines = f.read_text(encoding="utf-8").strip().split("\n", 1)[1].strip()
                api("PATCH", f"/blocks/{pid}/children", {"children": md_to_blocks(lines), "after": blocks[old]["id"]})
            print(("replaced " if apply else "would replace ") + f"{f.name} ({end - old - 1} old blocks)")
            continue
        at = next((i for i in heads if texts[i].startswith("XVI")), None)
        if at is None:
            at = next((i for i in heads if texts[i].startswith("Lore")), None)
        body = {"children": md_to_blocks(f.read_text(encoding="utf-8").strip())}
        where = "end"
        if at:
            body["after"] = blocks[at - 1]["id"]
            where = f"before '{texts[at][:30]}'"
        if apply:
            api("PATCH", f"/blocks/{pid}/children", body)
        print(("added   " if apply else "would add ") + f"{f.name} {where}")


if __name__ == "__main__":
    main()
