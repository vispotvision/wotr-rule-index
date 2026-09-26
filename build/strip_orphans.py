#!/usr/bin/env python3
"""Remove leftovers of earlier "The Two Accounts" sections from the 76 working pages.

A page's own content is taken from the wiki mirror as it stood at c79211a (before any
account was published). Everything between the page's last original block and the
current "The Two Accounts" divider is a leftover and is deleted. Dry run by default.

  bash build/py.sh build/strip_orphans.py [--apply] [--only NAME ...]
"""
import json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, paginate  # noqa: E402

BASE = "c79211a"
HEAD = "The Two Accounts"


def plain(b):
    t = b.get(b["type"], {})
    return "".join(r.get("plain_text", "") for r in t.get("rich_text", []))


def norm(s):
    s = re.sub(r"[*_`>#\[\]()]|\s+", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def last_original(rel):
    try:
        md = subprocess.run(["git", "show", f"{BASE}:{rel}"], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    body = md.split("---", 2)[2] if md.startswith("---") else md
    lines = [l for l in body.splitlines() if norm(l) and not re.fullmatch(r"[-| :]+", l.strip())]
    return norm(lines[-1])[:50] if lines else None


def main():
    apply = "--apply" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
    state = json.loads((ROOT / "imports/system-accounts/_published.json").read_text())
    for key, v in state.items():
        if only and not any(o in key for o in only):
            continue
        rel, pid = v["page"], v["notion_id"]
        tail = last_original(rel)
        blocks = list(paginate("GET", f"/blocks/{pid}/children?page_size=100"))
        heads = [i for i, b in enumerate(blocks) if b["type"] == "heading_2" and plain(b).strip() == HEAD]
        if not tail or not heads:
            print(f"SKIP {key}: {'no base text' if not tail else 'no section'}"); continue
        h = heads[-1]
        d = h - 1 if blocks[h - 1]["type"] == "divider" else h
        o = max((i for i in range(d) if tail[:30] in norm(plain(blocks[i]))), default=None)
        if o is None:
            print(f"SKIP {key}: original tail not found"); continue
        # an older section left whole (its own heading) also goes
        doomed = blocks[o + 1:d] + [b for i in heads[:-1] for b in []]
        print(f"{key}: {len(doomed)} leftover blocks" + (" (deleting)" if apply and doomed else ""))
        if apply:
            for b in doomed:
                api("DELETE", f"/blocks/{b['id']}")


if __name__ == "__main__":
    main()
