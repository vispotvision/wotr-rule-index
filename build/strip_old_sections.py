#!/usr/bin/env python3
"""Remove old renders of the accounts left above the current "The Two Accounts" section.

An old render is recognised by its numbered headings ("1 · Physical account",
"2 · Stratal account", ... "5 · Counterplay"). Everything from the divider before the
first such heading (or the heading itself) up to the current section's divider goes.
Dry run unless --apply.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, paginate  # noqa: E402
from strip_orphans import plain  # noqa: E402

OLD = re.compile(r"^\s*[1-5]\s*·\s*(Physical account|Stratal account|Mechanism|Essence ledger|Counterplay)", re.I)
HEAD = "The Two Accounts"


def main():
    apply = "--apply" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
    state = json.loads((ROOT / "imports/system-accounts/_published.json").read_text())
    total = 0
    for key, v in state.items():
        if only and not any(o in key for o in only):
            continue
        blocks = list(paginate("GET", f"/blocks/{v['notion_id']}/children?page_size=100"))
        heads = [i for i, b in enumerate(blocks) if b["type"] == "heading_2" and plain(b).strip() == HEAD]
        end = (heads[-1] - 1 if heads and blocks[heads[-1] - 1]["type"] == "divider" else heads[-1]) if heads else len(blocks)
        first = next((i for i in range(end) if b_is_old(blocks[i])), None)
        if first is None:
            continue
        start = first - 1 if first and blocks[first - 1]["type"] == "divider" else first
        # an old render may have lost its first heading: walk back over account-style paragraphs to the previous divider
        j = start - 1
        while j >= 0 and blocks[j]["type"] != "divider" and not blocks[j]["type"].startswith("heading"):
            j -= 1
        if j >= 0 and blocks[j]["type"] == "divider" and j < start and re.match(r"(?i)^(the phenomenon|the real phenomenon|aether stratum)", plain(blocks[j + 1]) or ""):
            start = j
        doomed = blocks[start:end]
        total += len(doomed)
        print(f"{key}: {len(doomed)} old blocks ({plain(blocks[first])[:40]!r})" + (" deleting" if apply else ""))
        if apply:
            for b in doomed:
                api("DELETE", f"/blocks/{b['id']}")
    print("total", total)


def b_is_old(b):
    return b["type"].startswith("heading") and bool(OLD.match(plain(b)))


if __name__ == "__main__":
    main()
