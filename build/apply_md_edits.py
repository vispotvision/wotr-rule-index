#!/usr/bin/env python3
"""Apply a plan of markdown edits (written against the wiki mirror) to the live Notion pages.

Plan JSON: [{"page", "notion_id", "edits": [{"old", "new"}], "delete_page", "new_page"?: {"title",
"parent_hint", "body_markdown"}}]. Each page is rendered block by block the way the mirror renders
it; an edit's `old` must match once. The blocks it touches are rewritten: in place when one block
stays one block of the same type, otherwise new blocks go in and the old ones come out. Table
rows are edited cell by cell. Dry run unless --apply.

  bash build/py.sh build/apply_md_edits.py PLAN.json [--apply] [--only SUBSTR]
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, children, block_md  # noqa: E402
from notion_publish import md_to_blocks, rich_text, create_page  # noqa: E402

APPLY = "--apply" in sys.argv


def segments(pid, title):
    """[(text, kind, obj)], kind in title|block|row|fixed; text is the block's mirror markdown."""
    segs = [(f"# {title}", "title", None), ("", "fixed", None)]
    for b in children(pid):
        if b["type"] == "table":
            rows = children(b["id"]) if b.get("has_children") else []
            for i, r in enumerate(rows):
                cells = [rich_rt(c) for c in r["table_row"]["cells"]]
                segs.append(("| " + " | ".join(cells) + " |", "row", (b, r)))
                if i == 0:
                    segs.append(("|" + "---|" * len(cells), "fixed", None))
            segs.append(("", "fixed", None))
        else:
            segs.append(("\n".join(block_md(b)), "block", b))
    return segs


def rich_rt(rt):
    from notion_export import rich
    return rich(rt).replace("|", "\\|").replace("\n", " ")


def shift(md):
    """mirror headings sit one level below Notion's (the page title is H1)."""
    return re.sub(r"(?m)^#(#{1,6}) ", r"\1 ", md)


def apply_edit(pid, segs, old, new):
    text, spans, pos = "", [], 0
    for s, k, o in segs:
        spans.append((len(text), len(text) + len(s)))
        text += s + "\n"
    pat = re.escape(old.strip("\n")).replace(r"\n\n", r"\n{2,}").replace("\\\n\\\n", "\n{2,}")
    ms = list(re.finditer(pat, text))
    if len(ms) != 1:
        return f"MISS ({len(ms)} matches)"
    a, z = ms[0].span()
    hit = [i for i, (s, e) in enumerate(spans) if s < z and e > a or (s == e == a)]
    hit = [i for i in hit if segs[i][1] != "fixed" or segs[i][0]]
    if not hit:
        return "MISS (no block)"
    lo, hi = hit[0], hit[-1]
    base = spans[lo][0]
    region = text[base:spans[hi][1]]
    new_region = region[:a - base] + new.strip("\n") + region[z - base:]
    kinds = {segs[i][1] for i in range(lo, hi + 1)}
    if kinds == {"title"} or (segs[lo][1] == "title"):
        rest = new_region.split("\n", 1)[1].strip() if "\n" in new_region else ""
        blocks = md_to_blocks(shift(rest))
        if APPLY and blocks:
            api("PATCH", f"/blocks/{pid}/children", {"children": blocks, "position": {"type": "start"}})
        return f"prepended {len(blocks)} block(s)"
    if kinds <= {"row", "fixed"}:
        rows = [segs[i][2] for i in range(lo, hi + 1) if segs[i][1] == "row"]
        lines = [ln for ln in new_region.split("\n") if ln.strip() and not re.match(r"^\|?\s*:?-{2,}", ln.strip())]
        table = rows[0][0]
        width = table["table"]["table_width"]
        def cells(ln):
            cs = [c.strip() for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]
            cs = [c.replace("\\|", "|") for c in cs]
            return [rich_text(c) if c else [] for c in (cs + [""] * width)[:width]]
        if APPLY:
            for (t, r), ln in zip(rows, lines):
                api("PATCH", f"/blocks/{r['id']}", {"table_row": {"cells": cells(ln)}})
            for t, r in rows[len(lines):]:
                api("DELETE", f"/blocks/{r['id']}")
            extra = lines[len(rows):]
            if extra:
                api("PATCH", f"/blocks/{table['id']}/children",
                    {"children": [{"object": "block", "type": "table_row", "table_row": {"cells": cells(ln)}} for ln in extra],
                     "after": rows[-1][1]["id"]})
        return f"table: {min(len(rows), len(lines))} row(s) edited, {max(0, len(rows) - len(lines))} deleted, {max(0, len(lines) - len(rows))} added"
    if "row" in kinds:
        return "MISS (edit spans a table and text)"
    olds = [segs[i][2] for i in range(lo, hi + 1) if segs[i][1] == "block"]
    blocks = md_to_blocks(shift(new_region)) if new_region.strip() else []
    if len(olds) == 1 and len(blocks) == 1 and olds[0]["type"] == "callout" and blocks[0]["type"] in ("quote", "paragraph"):
        blocks[0] = {"type": "callout", "callout": {"rich_text": blocks[0][blocks[0]["type"]]["rich_text"]}}
    if len(olds) == 1 and len(blocks) == 1 and blocks[0]["type"] == olds[0]["type"] and "rich_text" in blocks[0][blocks[0]["type"]]:
        t = blocks[0]["type"]
        if APPLY:
            api("PATCH", f"/blocks/{olds[0]['id']}", {t: {"rich_text": blocks[0][t]["rich_text"]}})
        return "edited in place"
    if APPLY:
        if blocks:
            prev = next((segs[i][2] for i in range(lo - 1, -1, -1) if segs[i][1] == "block"), None)
            body = {"children": blocks}
            if prev:
                body["after"] = prev["id"]
            else:
                body["position"] = {"type": "start"}
            api("PATCH", f"/blocks/{pid}/children", body)
        for b in olds:
            api("DELETE", f"/blocks/{b['id']}")
    return f"replaced {len(olds)} block(s) {[b['type'] for b in olds]} with {[b['type'] for b in blocks]}"


def main():
    plan = json.loads(Path(sys.argv[1]).read_text())
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    for x in plan:
        label = x.get("page") or (x.get("new_page") or {}).get("title")
        if only and only not in (label or ""):
            continue
        if x.get("new_page"):
            print("NEW PAGE (handled separately):", label); continue
        pid = x["notion_id"]
        if x.get("delete_page"):
            if APPLY:
                api("PATCH", f"/pages/{pid}", {"archived": True})
            print("archived" if APPLY else "would archive", label); continue
        p = api("GET", f"/pages/{pid}")
        title = "".join(t["plain_text"] for v in p["properties"].values() if v["type"] == "title" for t in v["title"])
        for e in x["edits"]:
            segs = segments(pid, title)          # re-read: earlier edits move blocks
            r = apply_edit(pid, segs, e["old"], e["new"])
            print(f"{label[5:60]:56} {x['answer_ref'][:24]:24} {r}")


if __name__ == "__main__":
    main()
