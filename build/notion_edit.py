#!/usr/bin/env python3
"""Block-level edits to Notion wiki pages: find-and-replace that keeps everything else.

  python build/notion_edit.py replace "Temür Büri" "Sodoku Moto" --pages "Path of Sorrow" [--apply]
  python build/notion_edit.py sweep [--apply]          # the whole Moto Reversion Ledger table
  python build/notion_edit.py rename <page_id> "New title"

Without --apply nothing is written; the report shows every block that would
change, before and after. With --apply each changed block is PATCHed in place
(annotations, links and mentions preserved; a term split across two formatting
runs is skipped and reported), the page's mirror file is re-exported, and the
report is written to reports/.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notion_export import api, block_md, children, page_tags, page_title, render_page, slug  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
MANIFEST = WIKI / ".manifest.json"
SOURCES = ROOT / "sources"

TEXT_TYPES = {"paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item",
              "to_do", "toggle", "quote", "callout", "code"}


def reversion_pairs() -> list[tuple[str, str]]:
    pairs = []
    src = next(SOURCES.glob("*Moto_Reversion*"), None)
    if src:
        for ln in src.read_text(encoding="utf-8").split("\n"):
            s = ln.strip()
            if not s.startswith("|") or re.match(r"^\|\s*-", s):
                continue
            cells = [c.strip().strip("*").strip() for c in s.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and cells[0] != "Struck":
                pairs.append((cells[0], cells[1]))
    pairs.append(("Buri", "Moto"))
    pairs.sort(key=lambda p: -len(p[0]))
    return pairs


def _rx(term: str) -> re.Pattern:
    return re.compile(r"(?<![\w\-])" + re.escape(term) + r"(?![\w\-])")


def _clean_rt(objs: list) -> list:
    """Rich text as the API accepts it back (drop read-only fields)."""
    out = []
    for o in objs:
        t = o.get("type")
        if t == "text":
            c = {"type": "text", "text": {"content": o["text"]["content"]}}
            if o["text"].get("link"):
                c["text"]["link"] = {"url": o["text"]["link"]["url"]}
            if o.get("annotations"):
                a = {k: v for k, v in o["annotations"].items() if k != "color" or v != "default"}
                if a:
                    c["annotations"] = a
            out.append(c)
        elif t == "mention":
            c = {"type": "mention", "mention": o["mention"]}
            if o.get("annotations"):
                c["annotations"] = o["annotations"]
            out.append(c)
        elif t == "equation":
            out.append({"type": "equation", "equation": o["equation"]})
    return out


def _replace_rt(objs: list, pairs: list[tuple[str, str]]) -> tuple[list, bool, list[str]]:
    """Apply pairs inside each text object. Returns (new objs, changed, skipped-terms)."""
    changed = False
    skipped = []
    full = "".join(o.get("plain_text", "") for o in objs)
    new = []
    for o in objs:
        if o.get("type") != "text":
            new.append(o); continue
        c = o["text"]["content"]
        c2 = c
        for old, rep in pairs:
            c2 = _rx(old).sub(rep, c2)
        if c2 != c:
            changed = True
            o = dict(o); o["text"] = dict(o["text"]); o["text"]["content"] = c2
        new.append(o)
    # a term present in the joined text but in no single object spans runs
    joined_new = "".join(o["text"]["content"] if o.get("type") == "text" else o.get("plain_text", "") for o in new)
    for old, _ in pairs:
        if _rx(old).search(full) and _rx(old).search(joined_new):
            skipped.append(old)
    return new, changed, skipped


def _walk(block_id: str):
    for b in children(block_id):
        yield b
        if b.get("has_children") and b["type"] not in ("child_page", "child_database"):
            yield from _walk(b["id"])


# blocks that talk ABOUT the old names (amendment notes, the docket, the
# reversion itself) must keep them; these phrases mark such blocks
META_PHRASES = ("Amendment note", "renders them as", "definitive ruling", "Reversion Ledger", "the reversion",
                "struck", "Struck", "old register", "Büri register", "Büri/Moto", "Büri / Moto", "formerly", "was called")


def _is_meta(text: str) -> bool:
    return any(p in text for p in META_PHRASES)


def replace_in_page(page_id: str, pairs: list[tuple[str, str]], apply: bool) -> list[dict]:
    """Every block whose text changes; PATCHed when apply=True."""
    hits = []
    for b in _walk(page_id):
        t = b["type"]
        plain = ""
        if t == "table_row":
            plain = " ".join("".join(o.get("plain_text", "") for o in c) for c in b["table_row"]["cells"])
        elif t in TEXT_TYPES:
            plain = "".join(o.get("plain_text", "") for o in b[t].get("rich_text", []))
        if _is_meta(plain):
            continue
        if t == "table_row":
            cells = b["table_row"]["cells"]
            new_cells, changed_any, skipped = [], False, []
            for cell in cells:
                nc, ch, sk = _replace_rt(cell, pairs)
                new_cells.append(nc); changed_any |= ch; skipped += sk
            if changed_any:
                before = " | ".join("".join(o.get("plain_text", "") for o in c) for c in cells)
                after = " | ".join("".join(o["text"]["content"] if o.get("type") == "text" else o.get("plain_text", "") for o in c) for c in new_cells)
                hits.append({"block": b["id"], "type": t, "before": before, "after": after, "skipped": skipped})
                if apply:
                    api("PATCH", f"/blocks/{b['id']}", {"table_row": {"cells": [_clean_rt(c) for c in new_cells]}})
        elif t in TEXT_TYPES:
            rt = b[t].get("rich_text", [])
            nrt, changed, skipped = _replace_rt(rt, pairs)
            if changed:
                before = "".join(o.get("plain_text", "") for o in rt)
                after = "".join(o["text"]["content"] if o.get("type") == "text" else o.get("plain_text", "") for o in nrt)
                hits.append({"block": b["id"], "type": t, "before": before, "after": after, "skipped": skipped})
                if apply:
                    api("PATCH", f"/blocks/{b['id']}", {t: {"rich_text": _clean_rt(nrt)}})
    return hits


def delete_block(block_id: str) -> None:
    api("DELETE", f"/blocks/{block_id}")


def rename_page(page_id: str, title: str) -> None:
    api("PATCH", f"/pages/{page_id}", {"properties": {"title": {"title": [{"type": "text", "text": {"content": title}}]}}})


def refresh_mirror(page_id: str) -> str:
    """Re-export one page into wiki/ after an edit; returns the relative path."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entry = m.get(page_id)
    page = api("GET", f"/pages/{page_id}")
    title = page_title(page)
    if entry:
        rel = entry["rel"]
        section = rel.split("/")[0]
        # keep the folder, retitle the file if the page was renamed
        if Path(rel).stem != slug(title):
            old = WIKI / rel
            rel = f"{section}/{slug(title)}.md"
            if old.exists():
                old.unlink()
    else:
        section = page_tags(page)[0] if page_tags(page) else "Misc"
        rel = f"{slug(section)}/{slug(title)}.md"
    path_for = {k.replace("-", ""): v["rel"] for k, v in m.items()}
    text, _ = render_page(page, section, path_for)
    out = WIKI / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    m[page_id] = {"rel": rel, "edited": page.get("last_edited_time", ""), "title": title}
    MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return rel


def pages_matching(needle: str) -> list[tuple[str, str]]:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if needle in ("", "all"):
        return [(pid, v["title"]) for pid, v in m.items()]
    return [(pid, v["title"]) for pid, v in m.items() if needle.lower() in v["title"].lower() or needle.lower() in v["rel"].lower()]


def pages_containing(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Mirror-side prefilter so a sweep does not walk all 381 pages. The Running
    Pieces (docket, ledger, state of play) refer to the old names on purpose."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out = []
    for pid, v in m.items():
        if v["rel"].startswith("The Table — Running Pieces/"):
            continue
        p = WIKI / v["rel"]
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if any(_rx(old).search(text) for old, _ in pairs):
            out.append((pid, v["title"]))
    return out


def write_report(name: str, lines: list[str]) -> Path:
    rep = ROOT / "reports" / f"{name}_{date.today().isoformat()}.md"
    rep.parent.mkdir(exist_ok=True)
    rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("replace"); r.add_argument("old"); r.add_argument("new"); r.add_argument("--pages", default="all"); r.add_argument("--apply", action="store_true")
    s = sub.add_parser("sweep"); s.add_argument("--apply", action="store_true")
    n = sub.add_parser("rename"); n.add_argument("page_id"); n.add_argument("title")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if a.cmd == "rename":
        rename_page(a.page_id, a.title)
        print("renamed; mirror:", refresh_mirror(a.page_id))
        return 0

    pairs = [(a.old, a.new)] if a.cmd == "replace" else reversion_pairs()
    targets = pages_matching(a.pages) if a.cmd == "replace" else pages_containing(pairs)
    if a.cmd == "replace":
        targets = [t for t in targets if t in pages_containing(pairs)]
    lines = [f"# {'sweep' if a.cmd == 'sweep' else 'replace ' + a.old + ' -> ' + a.new} — {'APPLIED' if a.apply else 'dry run'} {date.today().isoformat()}", ""]
    total = 0
    for pid, title in targets:
        hits = replace_in_page(pid, pairs, a.apply)
        if not hits:
            continue
        total += len(hits)
        lines.append(f"## {title}  ({pid})")
        for h in hits:
            lines.append(f"- [{h['type']}] {h['before'][:160]}")
            lines.append(f"  → {h['after'][:160]}")
            if h["skipped"]:
                lines.append(f"  ! not replaced (term spans formatting runs): {', '.join(sorted(set(h['skipped'])))}")
        if a.apply:
            rel = refresh_mirror(pid)
            lines.append(f"  mirror refreshed: {rel}")
        lines.append("")
        print(f"{title}: {len(hits)} block(s)")
    lines.insert(2, f"{total} block(s) across {sum(1 for _ in targets)} candidate page(s).")
    rep = write_report("notion_" + a.cmd, lines)
    print(f"report: {rep.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
