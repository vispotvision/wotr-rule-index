#!/usr/bin/env python3
"""Publish repo markdown into the War of the Realms Notion wiki.

  python build/notion_publish.py            # everything that changed since last run
  python build/notion_publish.py --dry-run  # list what would be created/updated
  python build/notion_publish.py --only sodoku_the_fixed_end   # substring of a path

What goes where (see TARGETS):
  scenes/*.md                 -> pages under the wiki's Scene Archive section
  desktop/NATALIE.md          -> "Natalie — Standing Rules" under The Rule Index
  out/rules.live.full.md      -> "Live Rules (resolved)"   under The Rule Index
  out/docket.md               -> "Docket (index view)"     under The Rule Index
  CONFLICTS.md                -> "Conflicts"               under The Rule Index

"The Rule Index" is a section page this script creates once (as a wiki row if
the integration is allowed to, else under The Table — Running Pieces).

Idempotent: build/.notion_publish.json maps each repo path to the Notion page
it made and the content hash it last pushed. Unchanged files are skipped;
changed files have their page body replaced in place, so page ids and links
stay stable. notion_export.py reads the same map and does not mirror these
pages back, so they never come round twice.

Needs NOTION_TOKEN with insert + update content capabilities.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notion_export import DATABASE_ID, api, paginate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "build" / ".notion_publish.json"

SCENE_ARCHIVE_ID = "3b258200-eb22-8132-a010-ec6fd17e718b"
RUNNING_PIECES_ID = "3d458200-eb22-813a-9148-fb943587f1dc"
RULE_INDEX_TITLE = "The Rule Index"

# repo path -> (parent key, page title or None for "from the file")
TARGETS = {
    "desktop/NATALIE.md": ("rule_index", "Natalie — Standing Rules"),
    "out/rules.live.full.md": ("rule_index", "Live Rules (resolved)"),
    "out/docket.md": ("rule_index", "Docket (index view)"),
    "CONFLICTS.md": ("rule_index", "Conflicts"),
    "table/FRONTS.md": ("running_pieces", "Fronts, as clocks"),
    "table/LEDGER.md": ("running_pieces", "The Ledger, structured"),
    "table/NPCS.md": ("running_pieces", "NPC roster"),
}
SCENE_SKIP = {
    "00_SUPERSEDED_wrong_names.md",       # labels itself superseded
    "WOTR_AI_Writing_Tells_to_Avoid.md",  # a craft guide, not a scene
    "MANIFEST.md",
    # already in the wiki under their own titles
    "THE_YUKARI_BLOODLINE.md",
    "renard_the_left_of_the_door.md",
    "12_mujin_open_crucible.md",
    "THE_KINGDOM_OF_KHARVEN_buri.md",
    "THE_KINGDOM_OF_KHARVEN_corrected.md",
}

TEXT_LIMIT = 2000      # chars per rich_text object
BATCH = 100            # blocks per append request


# --------------------------------------------------------------------------
# markdown -> Notion blocks

INLINE = re.compile(r"(\*\*.+?\*\*|\*(?!\s).+?(?<!\s)\*|_(?!\s).+?(?<!\s)_|`[^`]+`|\[[^\]]+\]\([^)]+\))")


def rich_text(s: str) -> list:
    out = []
    for part in INLINE.split(s):
        if not part:
            continue
        ann = {}
        text, link = part, None
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            text, ann = part[2:-2], {"bold": True}
        elif (part.startswith("*") and part.endswith("*") or part.startswith("_") and part.endswith("_")) and len(part) > 2:
            text, ann = part[1:-1], {"italic": True}
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            text, ann = part[1:-1], {"code": True}
        elif part.startswith("[") and part.endswith(")"):
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part)
            if m and m.group(2).startswith("http"):
                text, link = m.group(1), m.group(2)
            else:
                text = m.group(1) if m else part
        for i in range(0, len(text), TEXT_LIMIT):
            obj = {"type": "text", "text": {"content": text[i:i + TEXT_LIMIT]}}
            if link:
                obj["text"]["link"] = {"url": link}
            if ann:
                obj["annotations"] = ann
            out.append(obj)
    return out[:100] or [{"type": "text", "text": {"content": ""}}]


def _block(kind: str, text: str, **extra) -> dict:
    return {"object": "block", "type": kind, kind: {"rich_text": rich_text(text), **extra}}


def md_to_blocks(md: str) -> list:
    lines = md.replace("\r\n", "\n").split("\n")
    # drop frontmatter
    if lines and lines[0].strip() == "---":
        try:
            end = lines.index("---", 1)
            lines = lines[end + 1:]
        except ValueError:
            pass
    blocks, para, quote = [], [], []
    i = 0

    def flush_para():
        if para:
            blocks.append(_block("paragraph", "\n".join(para)))
            para.clear()

    def flush_quote():
        if quote:
            blocks.append(_block("quote", "\n".join(quote)))
            quote.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            flush_para(); flush_quote(); i += 1; continue
        if s.startswith("```"):
            flush_para(); flush_quote()
            lang = s[3:].strip() or "plain text"
            j = i + 1
            code = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                code.append(lines[j]); j += 1
            blocks.append({"object": "block", "type": "code",
                           "code": {"rich_text": rich_text("\n".join(code)) if code else [{"type": "text", "text": {"content": ""}}],
                                    "language": lang if lang in CODE_LANGS else "plain text"}})
            i = j + 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush_para(); flush_quote()
            level = min(len(m.group(1)), 3)
            blocks.append(_block(f"heading_{level}", m.group(2)))
            i += 1; continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            flush_para(); flush_quote()
            blocks.append({"object": "block", "type": "divider", "divider": {}})
            i += 1; continue
        if s.startswith(">"):
            flush_para()
            quote.append(s[1:].strip())
            i += 1; continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            flush_para(); flush_quote()
            rows = []
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                if not re.match(r"^\|?\s*:?-{2,}", lines[j].strip()):
                    cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    rows.append(cells)
                j += 1
            width = max(len(r) for r in rows) if rows else 1
            blocks.append({"object": "block", "type": "table",
                           "table": {"table_width": width, "has_column_header": True, "has_row_header": False,
                                     "children": [{"object": "block", "type": "table_row",
                                                   "table_row": {"cells": [rich_text(c) for c in (r + [""] * (width - len(r)))]}}
                                                  for r in rows]}})
            i = j; continue
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m:
            flush_para(); flush_quote()
            blocks.append(_block("bulleted_list_item", m.group(1)))
            i += 1; continue
        m = re.match(r"^\d+[.)]\s+(.*)$", s)
        if m:
            flush_para(); flush_quote()
            blocks.append(_block("numbered_list_item", m.group(1)))
            i += 1; continue
        flush_quote()
        para.append(s)
        i += 1
    flush_para(); flush_quote()
    return blocks


CODE_LANGS = {"plain text", "python", "bash", "shell", "yaml", "json", "markdown", "javascript", "powershell", "latex"}


# --------------------------------------------------------------------------
# Notion side


def page_title(p: dict) -> str:
    for prop in p.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    return ""


def create_page(parent: dict, title: str, blocks: list) -> str:
    body = {"parent": parent, "properties": {"title": {"title": [{"type": "text", "text": {"content": title[:2000]}}]}},
            "children": blocks[:BATCH]}
    page = api("POST", "/pages", body)
    for i in range(BATCH, len(blocks), BATCH):
        api("PATCH", f"/blocks/{page['id']}/children", {"children": blocks[i:i + BATCH]})
    return page["id"]


def replace_body(page_id: str, blocks: list) -> None:
    for b in list(paginate("GET", f"/blocks/{page_id}/children?page_size=100")):
        api("DELETE", f"/blocks/{b['id']}")
    for i in range(0, len(blocks), BATCH):
        api("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i + BATCH]})


def ensure_rule_index(m: dict, dry: bool) -> str | None:
    if m.get("_rule_index"):
        return m["_rule_index"]
    if dry:
        return None
    intro = md_to_blocks(
        "Generated pages, mirrored from the GitHub repo vispotvision/wotr-rule-index by "
        "build/notion_publish.py. Edit the repo, not these pages; the next publish overwrites them.\n\n"
        "- Natalie — Standing Rules: the full standing prompt.\n"
        "- Live Rules (resolved): every craft rule currently in force, by domain, with its source quote.\n"
        "- Docket (index view): every pending or proposed rule, with quotes.\n"
        "- Conflicts: live rules that contradict each other, awaiting Isaac.\n"
    )
    try:
        pid = create_page({"database_id": DATABASE_ID}, RULE_INDEX_TITLE, intro)
    except RuntimeError as e:
        print(f"  (wiki root refused a new row: {str(e)[:80]}...; creating under Running Pieces)")
        pid = create_page({"page_id": RUNNING_PIECES_ID}, RULE_INDEX_TITLE, intro)
    m["_rule_index"] = pid
    return pid


def scene_title(path: Path, md: str) -> str:
    m = re.search(r"(?m)^#\s+(.+?)\s*$", md)
    if m:
        return m.group(1).strip().strip("*")
    return path.stem.replace("_", " ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="substring of a repo path")
    ap.add_argument("--force", action="store_true", help="republish even if unchanged")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    m = json.loads(MAP.read_text(encoding="utf-8")) if MAP.exists() else {}

    jobs = []
    for p in sorted((ROOT / "scenes").glob("*.md")):
        if p.name in SCENE_SKIP:
            continue
        jobs.append((p.relative_to(ROOT).as_posix(), "scene_archive", None))
    for rel, (parent_key, title) in TARGETS.items():
        if (ROOT / rel).exists():
            jobs.append((rel, parent_key, title))
    if args.only:
        jobs = [j for j in jobs if args.only.lower() in j[0].lower()]

    todo = []
    for rel, parent_key, title in jobs:
        md = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        h = hashlib.sha256(md.encode("utf-8")).hexdigest()[:16]
        entry = m.get(rel)
        if entry and entry.get("hash") == h and not args.force:
            continue
        todo.append((rel, parent_key, title or scene_title(ROOT / rel, md), md, h, entry))

    print(f"{len(jobs)} tracked files, {len(todo)} to publish")
    if args.dry_run:
        for rel, _, title, _, _, entry in todo:
            print(f"  {'update' if entry else 'create'}  {rel}  ->  {title}")
        return 0

    rule_index_id = ensure_rule_index(m, args.dry_run) if any(j[1] == "rule_index" for j in todo) else m.get("_rule_index")
    MAP.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

    for n, (rel, parent_key, title, md, h, entry) in enumerate(todo, 1):
        blocks = md_to_blocks(md)
        if entry:
            replace_body(entry["page_id"], blocks)
            pid = entry["page_id"]
            print(f"  [{n}/{len(todo)}] updated {rel} ({len(blocks)} blocks)")
        else:
            parent = {"page_id": {"scene_archive": SCENE_ARCHIVE_ID, "running_pieces": RUNNING_PIECES_ID}.get(parent_key, rule_index_id)}
            pid = create_page(parent, title, blocks)
            print(f"  [{n}/{len(todo)}] created {rel} -> {title} ({len(blocks)} blocks)")
        m[rel] = {"page_id": pid, "title": title, "hash": h}
        MAP.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
