#!/usr/bin/env python3
"""WAR-14 (Essence Ledger Phase 4). Publish the draft Part to the Notion wiki.

  bash build/py.sh imports/essence-ledger/publish_part.py --dry-run
  bash build/py.sh imports/essence-ledger/publish_part.py --apply

Takes `the-essence-ledger.md` (WAR-12's draft, never edited by this script),
applies the publication patches below in memory, and creates or replaces one
Notion page under "Fracture of Worlds — The Living System", beside volumes I
to VIII. The hourly sync mirrors it back into `wiki/`; nothing here writes
`wiki/`.

The patches are the only difference between the draft on disk and the page,
each is asserted to match exactly once, and the exact body that was published
is written to `_published/the-essence-ledger.notion.md` as the record.

Markdown -> blocks is `build/notion_publish.md_to_blocks`, the converter the
rest of the wiki is published with; the page is created with its `create_page`
and the API door in `build/notion_export`. Nothing in `build/` is changed.

Needs NOTION_TOKEN (build/py.sh loads it from ~/.config/wotr/env).
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, paginate  # noqa: E402
from notion_publish import BATCH, create_page, md_to_blocks  # noqa: E402

HERE = ROOT / "imports" / "essence-ledger"
DRAFT = HERE / "the-essence-ledger.md"
# the clean published edition; when it exists it is published as is, no patches
EDITION = HERE / "the-essence-ledger.edition.md"
RECORD_DIR = HERE / "_published"
STATE = HERE / "_published_pages.json"

# "Fracture of Worlds — The Living System", the section page volumes I-VIII sit under
FOW_PARENT_ID = "3d758200-eb22-8101-bde2-f8eceeaefc7a"
TITLE = "IX. The Essence Ledger (Part Twenty-Three)"

# ---------------------------------------------------------------------------
# The publication patches. (old, new) -- each must match the draft exactly once.
#
# Both are there to meet clean publishing (Isaac, 2026-09-26; the rule is in
# `.claude/skills/wotr-write/references/fair-play.md`): a published page never
# carries his name or role, a ruling, an open question, a conflict or issue id,
# or where its text came from. The draft's header and its closing note on where
# the ruling rows sit are all four of those, so the header becomes a standfirst
# in the page's own register and the note goes. The apparatus the draft keeps
# for the repo -- the [canon]/[ruled]/[derived] markers, the file-and-line
# citations, PENDING, and sections 9 and 10 -- is WAR-12's text and is NOT
# rewritten here: doing that is a published edition of the Part, not a
# publication of it, and it is filed as its own issue.
#
# Both replacements are also written without the draft's wrapping `*...*`. The
# converter's inline regex cannot see an italic span that the source wraps
# across two lines, so such a span reaches Notion with its asterisks printed as
# characters; and joining it onto one line is worse, because an italic run
# swallows the `code` spans inside it and their backticks print instead. The
# draft's own wrapped italics are left exactly as they are: they are WAR-12's
# text, and this issue publishes the Part, it does not restyle it.

OLD_HEAD = """*Fracture of Worlds — The Living System. Draft, WAR-12 (Essence Ledger Phase 2,
parent WAR-8), 2026-09-25. Rebuilt 2026-09-25 (WAR-117) against the
WAR-71/WAR-94-corrected fit and the sixteen card AU/s figures WAR-48 corrected
under R44-2: §5.3's table, §6.2, §6.5's reservoir arithmetic and the counts in
§8 and §9.3. Every figure in it comes from `ledger_tables.json`; none was typed.*

> **Status: draft, not canon.** Nothing here is published to the wiki or to
> Notion; that is Phase 4 (WAR-14). No card, page, table or figure anywhere in
> the project has been changed to make this Part come out. Where canon
> contradicts canon the Part states the equation, shows the break, and leaves
> the conflict open. Where a ruling is pending the slot is marked **PENDING**
> and the question is named in words Isaac can answer in a sentence.
>
> **The constant is ruled.** **[ruled]** *"One constant: 1 EU = 1 MJ stands. The
> Ledger converts at 1 MJ everywhere"* — Isaac on C-034, 2026-09-25, carried as
> **R44-1**. This Part converts at 1 MJ everywhere, and it shows the residual
> against every anchor, measurement and physical bracket the ruled constant
> misses, in the words of the note that found them. **A ruling and a physics
> note disagreeing is recorded, never resolved** (`CLAUDE.md`); §2.4 and §9.2
> are that record, and nothing in them moves the ruling."""

NEW_HEAD = """> Four quantities run through every practitioner in the Continuum — a reserve
> in EU, a compression in EU/g, an output rate in AU/s, an efficiency η — and
> the Grade ladder measures destruction in joules. This Part is the join.
> **One Essence Unit is one megajoule.** What follows is what that buys on the
> ladder, what a reserve costs to spend, how long it lasts at full output, how
> fast it comes back, and what can be done about all of it from the other side
> of a fight."""

OLD_R44_NOTE = """*At the time of writing the R44 rows are in the WAR-22 ruling batch (commit
`3215399`), in review and not yet on master; the 2026-09-25 "new" entry, which is
on master, already cites R44-3 and R44-5 by id.*"""

NEW_R44_NOTE = ""

PATCHES = [(OLD_HEAD, NEW_HEAD), (OLD_R44_NOTE, NEW_R44_NOTE)]


def unwrap(md: str) -> str:
    """Join hard-wrapped lines back into one line per paragraph, list item or quote.

    The sources are wrapped at ~80 columns and Notion keeps every newline inside a
    paragraph, so an unwrapped page reads ragged. Tables, headings, rules and code
    fences are left exactly as they are.
    """
    out, buf, kind = [], [], None
    def flush():
        nonlocal buf, kind
        if buf:
            out.append(("> " if kind == "quote" else "") + " ".join(buf))
        buf, kind = [], None
    fence = False
    lines = md.split("\n")
    # an indented block (aligned arithmetic) becomes a fenced block, kept as written
    fenced, i = [], 0
    while i < len(lines):
        if lines[i].startswith("    ") and lines[i].strip() and (i == 0 or not lines[i - 1].strip()):
            block = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                block.append(lines[i][4:])
                i += 1
            while block and not block[-1].strip():
                block.pop()
            fenced += ["```"] + block + ["```", ""]
            continue
        fenced.append(lines[i])
        i += 1
    for line in fenced:
        st = line.strip()
        if st.startswith("```"):
            flush(); fence = not fence; out.append(line); continue
        if fence or not st or st.startswith(("|", "#", "---")):
            flush(); out.append(line); continue
        if st.startswith(">"):
            body = st[1:].strip()
            if not body:
                flush(); continue
            if kind != "quote":
                flush(); kind = "quote"
            buf.append(body); continue
        if re.match(r"([-*+]|\d+\.)\s", st):
            flush(); kind = "item"; buf.append(line.rstrip()); continue
        if kind == "quote":
            flush()
        if kind is None:
            kind = "para"
        buf.append(st)
    flush()
    return "\n".join(out)


def publication_body() -> str:
    if EDITION.exists():
        return unwrap(EDITION.read_text(encoding="utf-8"))
    md = DRAFT.read_text(encoding="utf-8")
    for old, new in PATCHES:
        n = md.count(old)
        if n != 1:
            raise SystemExit(f"patch matched {n} times, expected 1:\n{old[:120]}...")
        md = md.replace(old, new)
    # the page title carries the H1; every other wiki page's body starts below it
    md = re.sub(r"\A#\s+Part Twenty-Three — The Essence Ledger\n+", "", md, count=1)
    if md.lstrip().startswith("# "):
        raise SystemExit("the H1 was not the one expected")
    return md


def replace_body(page_id: str, blocks: list) -> None:
    for b in list(paginate("GET", f"/blocks/{page_id}/children?page_size=100")):
        api("DELETE", f"/blocks/{b['id']}")
    for i in range(0, len(blocks), BATCH):
        api("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i + BATCH]})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write to Notion")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply:
        args.dry_run = True

    md = publication_body()
    blocks = md_to_blocks(md)
    RECORD_DIR.mkdir(exist_ok=True)
    (RECORD_DIR / "the-essence-ledger.notion.md").write_text(md, encoding="utf-8")

    widest = max((b["table"]["table_width"] for b in blocks if b["type"] == "table"), default=0)
    longest = max((len(b["table"]["children"]) for b in blocks if b["type"] == "table"), default=0)
    print(f"{TITLE}")
    print(f"  {len(md.splitlines())} lines -> {len(blocks)} blocks; "
          f"widest table {widest} columns, longest {longest} rows")

    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    existing = state.get("part_twenty_three", {}).get("page_id")

    if args.dry_run:
        print(f"  dry run: would {'replace the body of ' + existing if existing else 'create it under ' + FOW_PARENT_ID}")
        return 0

    if existing:
        replace_body(existing, blocks)
        pid = existing
        print(f"  replaced the body of {pid}")
    else:
        pid = create_page({"page_id": FOW_PARENT_ID}, TITLE, blocks)
        print(f"  created {pid}")
    state["part_twenty_three"] = {"page_id": pid, "title": TITLE, "issue": "WAR-14",
                                  "source": "imports/essence-ledger/the-essence-ledger.md"}
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
