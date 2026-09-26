#!/usr/bin/env python3
"""Put each page's pronunciation line under its title (R50-34). Skips pages that already have one.

  bash build/py.sh build/add_say_lines.py PRONUNCIATIONS.json [--apply]
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, paginate  # noqa: E402
from notion_publish import md_to_blocks  # noqa: E402
from strip_orphans import plain  # noqa: E402


def main():
    rows = json.loads(Path(sys.argv[1]).read_text())
    apply = "--apply" in sys.argv
    done = skipped = failed = 0
    for r in rows:
        try:
            first = list(paginate("GET", f"/blocks/{r['notion_id']}/children?page_size=10"))[:6]
        except Exception as e:
            print("FAIL", r["page"], e); failed += 1; continue
        if any(plain(b).startswith("Say it") for b in first):
            skipped += 1; continue
        t = next((b for b in first[:2] if b["type"] == "heading_1"), None)
        body = {"children": md_to_blocks(r["line"])}
        if t:
            body["after"] = t["id"]           # under the page's own title heading
        else:
            body["position"] = {"type": "start"}   # top of the page
        if apply:
            api("PATCH", f"/blocks/{r['notion_id']}/children", body)
        done += 1
    print(f"added {done}, already had one {skipped}, failed {failed}{'' if apply else ' (dry run)'}")


if __name__ == "__main__":
    main()
