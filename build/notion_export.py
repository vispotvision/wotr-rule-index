#!/usr/bin/env python3
"""Mirror the War of the Realms Notion wiki into wiki/ as markdown.

  set NOTION_TOKEN=secret_...      (PowerShell: $env:NOTION_TOKEN = "secret_...")
  python build/notion_export.py            # incremental: only pages edited since last run
  python build/notion_export.py --full     # re-export everything
  python build/notion_export.py --dry-run  # list what would change, write nothing

Setup, once:
  1. https://www.notion.so/profile/integrations -> New integration, internal,
     read-only content capability is enough. Copy the secret.
  2. Open the wiki in Notion -> ... -> Connections -> add the integration.
  3. Put the secret in NOTION_TOKEN. Never commit it.

Layout: one file per wiki page at wiki/<Section>/<Title>.md, where Section is
the nearest ancestor page that is itself a wiki row (Characters, Magic System,
...), falling back to the page's first Tag, then "Misc". Each file carries
frontmatter with the Notion id, tags, last-edited time and URL. wiki/INDEX.md
lists everything; wiki/.manifest.json drives the incremental run.

The wiki is read-only from here. Nothing writes back to Notion.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
MANIFEST = WIKI_DIR / ".manifest.json"

DATABASE_ID = "3b158200-eb22-81c6-b008-dcc414a561d0"
DATA_SOURCE_ID = "3b158200-eb22-8044-bc01-000bd63d3f7b"

# Pages Isaac has moved out of the wiki database on purpose (kept off the
# public wiki -- The Rule Index, and everything under "Information not on
# WIKI"). A page moved out of a Notion database stops being a member of it,
# so list_rows() alone can no longer see it or anything nested under it --
# without this, the exporter would read that as "deleted in Notion" and
# wipe the mirror. Walked separately below and merged into `rows`.
PRIVATE_ROOTS = ["3d958200-eb22-80a4-b8f3-cc2c16241f7d"]

API = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"
RATE_SLEEP = 0.35  # Notion allows ~3 req/s


# --------------------------------------------------------------------------
# HTTP


def _token() -> str:
    tok = os.environ.get("NOTION_TOKEN")
    if not tok:
        sys.exit("NOTION_TOKEN is not set. See the docstring at the top of this script.")
    return tok


def api(method: str, path: str, body: dict | None = None, retries: int = 5) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {_token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                time.sleep(RATE_SLEEP)
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = float(e.headers.get("Retry-After", 2 ** attempt))
                time.sleep(wait)
                continue
            detail = e.read().decode("utf-8", "replace")
            raise RuntimeError(f"{method} {path} -> {e.code}: {detail}") from None
    raise RuntimeError(f"{method} {path}: gave up after {retries} retries")


def paginate(method: str, path: str, body: dict | None = None):
    body = dict(body or {})
    cursor = None
    while True:
        if method == "POST":
            if cursor:
                body["start_cursor"] = cursor
            page = api("POST", path, body)
        else:
            url = path + (f"&start_cursor={cursor}" if cursor else "")
            page = api("GET", url)
        yield from page.get("results", [])
        if not page.get("has_more"):
            return
        cursor = page["next_cursor"]


# --------------------------------------------------------------------------
# Rich text and blocks -> markdown


def _wrap(s: str, a: dict, href: str | None) -> str:
    if not s.strip():
        return s
    lead = s[: len(s) - len(s.lstrip())]
    trail = s[len(s.rstrip()):]
    s = s.strip()
    if a.get("code"):
        s = f"`{s}`"
    if a.get("bold"):
        s = f"**{s}**"
    if a.get("italic"):
        s = f"*{s}*"
    if a.get("strikethrough"):
        s = f"~~{s}~~"
    if href:
        s = f"[{s}]({href})"
    return lead + s + trail


def rich(rt: list) -> str:
    out = []
    for t in rt or []:
        s = t.get("plain_text", "")
        if t.get("type") == "equation":
            s = f"${s}$"
        a = t.get("annotations", {})
        href = t.get("href") if t.get("type") != "mention" else None
        # markdown emphasis does not span lines; wrap each line separately
        out.append("\n".join(_wrap(ln, a, href) for ln in s.split("\n")))
    return "".join(out)


def children(block_id: str) -> list:
    return list(paginate("GET", f"/blocks/{block_id}/children?page_size=100"))


def block_md(b: dict, depth: int = 0, ctx: dict | None = None) -> list[str]:
    ctx = ctx or {}
    t = b["type"]
    body = b.get(t, {})
    ind = "  " * depth
    lines: list[str] = []

    def kids(extra_depth: int = 1) -> list[str]:
        if not b.get("has_children"):
            return []
        out = []
        for c in children(b["id"]):
            out.extend(block_md(c, depth + extra_depth, ctx))
        return out

    if t == "paragraph":
        txt = rich(body.get("rich_text"))
        lines.append(f"{ind}{txt}" if txt else "")
        lines.extend(kids())
    elif t in ("heading_1", "heading_2", "heading_3"):
        level = int(t[-1]) + 1  # page title is H1
        lines.append("")
        lines.append(f"{'#' * level} {rich(body.get('rich_text'))}")
        lines.append("")
        lines.extend(kids(0))
    elif t == "bulleted_list_item":
        lines.append(f"{ind}- {rich(body.get('rich_text'))}")
        lines.extend(kids())
    elif t == "numbered_list_item":
        lines.append(f"{ind}1. {rich(body.get('rich_text'))}")
        lines.extend(kids())
    elif t == "to_do":
        box = "[x]" if body.get("checked") else "[ ]"
        lines.append(f"{ind}- {box} {rich(body.get('rich_text'))}")
        lines.extend(kids())
    elif t == "toggle":
        lines.append(f"{ind}- **{rich(body.get('rich_text'))}**")
        lines.extend(kids())
    elif t == "quote":
        txt = rich(body.get("rich_text"))
        lines.extend(f"{ind}> {ln}" for ln in txt.split("\n"))
        for k in kids(0):
            lines.append(f"{ind}> {k}" if k else f"{ind}>")
    elif t == "callout":
        icon = body.get("icon") or {}
        emoji = icon.get("emoji", "") + " " if icon.get("type") == "emoji" else ""
        txt = rich(body.get("rich_text"))
        lines.extend(f"{ind}> {emoji}{ln}" for ln in txt.split("\n"))
        for k in kids(0):
            lines.append(f"{ind}> {k}" if k else f"{ind}>")
    elif t == "code":
        lang = body.get("language", "")
        lines.append(f"{ind}```{lang}")
        lines.extend(f"{ind}{ln}" for ln in rich(body.get("rich_text")).split("\n"))
        lines.append(f"{ind}```")
    elif t == "divider":
        lines.append("")
        lines.append(f"{ind}---")
        lines.append("")
    elif t == "table":
        rows = children(b["id"]) if b.get("has_children") else []
        has_header = body.get("has_column_header", False)
        for i, r in enumerate(rows):
            cells = [rich(c).replace("|", "\\|").replace("\n", " ") for c in r["table_row"]["cells"]]
            lines.append(f"{ind}| " + " | ".join(cells) + " |")
            if i == 0:
                lines.append(f"{ind}|" + "---|" * len(cells))
        if rows and not has_header:
            pass  # markdown needs a header row anyway; first row serves
        lines.append("")
    elif t == "child_page":
        title = body.get("title", "")
        target = ctx.get("path_for", {}).get(b["id"].replace("-", ""))
        lines.append(f"{ind}- [[{title}]]" if not target else f"{ind}- [{title}]({target})")
        ctx.setdefault("child_pages", []).append((b["id"], title))
    elif t == "child_database":
        lines.append(f"{ind}*(embedded database: {body.get('title', '')})*")
    elif t == "image":
        src = (body.get("external") or body.get("file") or {}).get("url", "")
        cap = rich(body.get("caption"))
        lines.append(f"{ind}![{cap}]({src})")
    elif t in ("bookmark", "embed", "link_preview"):
        lines.append(f"{ind}<{body.get('url', '')}>")
    elif t == "equation":
        lines.append(f"{ind}$$ {body.get('expression', '')} $$")
    elif t in ("column_list", "column", "synced_block"):
        lines.extend(kids(0))
    elif t == "link_to_page":
        pid = body.get("page_id") or body.get("database_id") or ""
        lines.append(f"{ind}- [[notion:{pid}]]")
    elif t == "table_of_contents":
        pass
    elif t == "unsupported":
        lines.append(f"{ind}*(unsupported block)*")
    else:
        txt = rich(body.get("rich_text")) if isinstance(body, dict) else ""
        lines.append(f"{ind}{txt}" if txt else f"{ind}*({t})*")
        lines.extend(kids())
    return lines


# --------------------------------------------------------------------------
# Pages


def page_title(p: dict) -> str:
    for prop in p.get("properties", {}).values():
        if prop.get("type") == "title":
            return rich(prop.get("title")) or "Untitled"
    return "Untitled"


def page_tags(p: dict) -> list[str]:
    tags = p.get("properties", {}).get("Tags", {})
    return [o["name"] for o in tags.get("multi_select", [])] if tags else []


def slug(title: str) -> str:
    s = re.sub(r"[\\/:*?\"<>|]+", "", title).strip()
    s = re.sub(r"\s+", " ", s)
    return s[:120] or "Untitled"


def list_rows() -> list[dict]:
    try:
        return list(paginate("POST", f"/data_sources/{DATA_SOURCE_ID}/query", {"page_size": 100}))
    except RuntimeError as e:
        if "404" not in str(e):
            raise
        return list(paginate("POST", f"/databases/{DATABASE_ID}/query", {"page_size": 100}))


def crawl_private_tree(root_id: str) -> list[dict]:
    """Every descendant page under a PRIVATE_ROOTS page, walked by hand.

    A page moved out of the wiki database (Isaac's own move, to keep it off
    the public wiki) stops being a data-source member, so list_rows() can't
    see it or anything nested under it. Walk it the way Notion's own page
    tree does instead: fetch each child_page block, GET the full page (for
    properties/parent/last_edited_time -- block children don't carry those),
    recurse into it, and treat every page found (root included) as if it
    were a row, so section_for()'s "nearest ancestor that is a row" logic
    keeps working unmodified for anything nested under it.
    """
    root = api("GET", f"/pages/{root_id}")
    found = {root_id: root}
    stack = [root_id]
    while stack:
        pid = stack.pop()
        for b in children(pid):
            if b.get("type") == "child_page":
                cid = b["id"]
                if cid in found:
                    continue
                found[cid] = api("GET", f"/pages/{cid}")
                stack.append(cid)
    return list(found.values())


def section_for(p: dict, rows_by_id: dict, cache: dict) -> str:
    """Nearest ancestor that is itself a wiki row; else first tag; else Misc."""
    pid = p["id"]
    if pid in cache:
        return cache[pid]
    parent = p.get("parent", {})
    if parent.get("type") == "page_id":
        anc_id = parent["page_id"]
        if anc_id in rows_by_id:
            cache[pid] = page_title(rows_by_id[anc_id])
            return cache[pid]
        anc = api("GET", f"/pages/{anc_id}")
        cache[pid] = section_for(anc, rows_by_id, cache)
        return cache[pid]
    tags = page_tags(p)
    cache[pid] = tags[0] if tags else "Misc"
    return cache[pid]


def render_page(p: dict, section: str, path_for: dict) -> tuple[str, list]:
    title = page_title(p)
    ctx = {"path_for": path_for}
    body = []
    for b in children(p["id"]):
        body.extend(block_md(b, 0, ctx))
    fm = {
        "title": title,
        "notion_id": p["id"],
        "notion_url": p.get("url", ""),
        "section": section,
        "tags": page_tags(p),
        "last_edited": p.get("last_edited_time", ""),
        "verification": (p.get("properties", {}).get("Verification", {}).get("verification") or {}).get("state"),
    }
    head = ["---"]
    for k, v in fm.items():
        head.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    head.append("---")
    text = "\n".join(head + ["", f"# {title}", ""] + body).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, ctx.get("child_pages", [])


# --------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="ignore the manifest, re-export everything")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="substring of a title, export just matching pages")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    WIKI_DIR.mkdir(exist_ok=True)
    manifest = {} if args.full or not MANIFEST.exists() else json.loads(MANIFEST.read_text(encoding="utf-8"))

    print("listing wiki rows ...")
    rows = list_rows()
    crawl_incomplete = False
    for root_id in PRIVATE_ROOTS:
        try:
            private_pages = crawl_private_tree(root_id)
        except RuntimeError as e:
            crawl_incomplete = True
            print(f"  WARNING: can't reach private root {root_id}: {e}")
            print("  Share this page with the Notion integration (... -> Connections) "
                  "or the exporter can't see it. Skipping the delete-sweep this run so "
                  "nothing under it gets wiped from wiki/ while it's unreachable.")
            continue
        print(f"  {len(private_pages)} pages under the private root {root_id}")
        rows += private_pages
    # pages that notion_publish.py pushed *into* Notion from this repo are not
    # mirrored back, or they would come round twice
    pub = ROOT / "build" / ".notion_publish.json"
    published = set()
    if pub.exists():
        pm = json.loads(pub.read_text(encoding="utf-8"))
        published = {v["page_id"] if isinstance(v, dict) else v for v in pm.values()}
    rows = [r for r in rows if r["id"] not in published]
    rows_by_id = {r["id"]: r for r in rows}
    print(f"  {len(rows)} pages" + (f" ({len(published)} repo-published pages skipped)" if published else ""))

    cache: dict = {}
    plan = []
    for p in rows:
        title = page_title(p)
        if args.only and args.only.lower() not in title.lower():
            continue
        section = section_for(p, rows_by_id, cache)
        rel = f"{slug(section)}/{slug(title)}.md"
        # duplicate titles in one section: disambiguate with a short id
        if any(x["rel"] == rel and x["id"] != p["id"] for x in plan):
            rel = f"{slug(section)}/{slug(title)} ({p['id'][:8]}).md"
        plan.append({"id": p["id"], "title": title, "section": section, "rel": rel,
                     "edited": p.get("last_edited_time", ""), "page": p})

    path_for = {x["id"].replace("-", ""): x["rel"] for x in plan}
    todo = [x for x in plan if manifest.get(x["id"], {}).get("edited") != x["edited"]
            or not (WIKI_DIR / x["rel"]).exists()]
    print(f"  {len(todo)} to export, {len(plan) - len(todo)} unchanged")
    if args.dry_run:
        for x in todo:
            print(f"  would write {x['rel']}")
        return 0

    for i, x in enumerate(todo, 1):
        text, _ = render_page(x["page"], x["section"], path_for)
        out = WIKI_DIR / x["rel"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="\n")
        manifest[x["id"]] = {"rel": x["rel"], "edited": x["edited"], "title": x["title"]}
        print(f"  [{i}/{len(todo)}] {x['rel']}")
        if i % 10 == 0:
            MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # drop files for pages that no longer exist in the wiki
    live_ids = {x["id"] for x in plan}
    if crawl_incomplete:
        print("  crawl was incomplete (see WARNING above); skipping the delete-sweep this run")
    if not args.only and not crawl_incomplete:
        for pid in list(manifest):
            if pid not in live_ids:
                gone = WIKI_DIR / manifest[pid]["rel"]
                if gone.exists():
                    gone.unlink()
                    print(f"  removed {manifest[pid]['rel']} (deleted in Notion)")
                del manifest[pid]

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # index
    by_section = defaultdict(list)
    for x in plan:
        by_section[x["section"]].append(x)
    idx = ["# War of the Realms — Wiki mirror", "",
           f"{len(plan)} pages, mirrored from Notion by build/notion_export.py. Read-only here; edit in Notion and re-run.", ""]
    for section in sorted(by_section):
        idx.append(f"## {section} ({len(by_section[section])})")
        idx.append("")
        for x in sorted(by_section[section], key=lambda y: y["title"].lower()):
            idx.append(f"- [{x['title']}]({x['rel'].replace(' ', '%20')})")
        idx.append("")
    (WIKI_DIR / "INDEX.md").write_text("\n".join(idx), encoding="utf-8", newline="\n")
    print(f"wrote wiki/INDEX.md ({len(plan)} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
