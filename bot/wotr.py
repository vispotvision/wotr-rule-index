"""The bot's view of the repo: thin wrappers over WOTR MCP's functions and the index.

Everything here is synchronous and file-bound; the cogs call it through
asyncio.to_thread so the gateway heartbeat never waits on disk. Nothing in this
module writes.
"""
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

BOT_DIR = Path(__file__).resolve().parent
ROOT = BOT_DIR.parent
sys.path.insert(0, str(ROOT / "build"))

import mcp_server as M  # noqa: E402  (the @server.tool() decorator returns the plain function)
from common import load_rules, load_vocab  # noqa: E402

CONFLICTS = ROOT / "CONFLICTS.md"
CAST = ROOT / "scenes" / "CAST.md"
WIKI = ROOT / "wiki"
SCENES = ROOT / "scenes"


def commit_hash() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, timeout=10).stdout.strip() or "?"
    except (OSError, subprocess.TimeoutExpired):
        return "?"


# -- rules ------------------------------------------------------------------

def rule_by_id(rule_id: str) -> dict | None:
    key = rule_id.strip().upper()
    for r in load_rules():
        if r.get("id", "").upper() == key:
            return r
    return None


def rule_ids(prefix: str = "", limit: int = 25) -> list[tuple[str, str]]:
    """(id, title) pairs whose id or title contains the text, for autocomplete."""
    key = prefix.strip().lower()
    out = []
    for r in load_rules():
        if not key or key in r["id"].lower() or key in r.get("title", "").lower():
            out.append((r["id"], r.get("title", "")))
            if len(out) >= limit:
                break
    return out


def vocab() -> list[str]:
    return sorted(load_vocab())


def rules_for(tags: list[str], status: list[str]) -> tuple[list[dict], list[str]]:
    return M._select(tags, status)


def docket_for(tags: list[str]) -> tuple[list[dict], list[str]]:
    return M._select(tags, ["pending", "proposed"])


# -- conflicts --------------------------------------------------------------

@lru_cache(maxsize=1)
def _conflicts_cache(mtime: float) -> list[dict]:
    text = re.sub(r"(?ms)^```.*?^```\s*", "", CONFLICTS.read_text(encoding="utf-8"))  # drop the format example
    out = []
    for m in re.finditer(r"(?ms)^## (C-\d+)\s+[—-]+\s+(.+?)\n(.*?)(?=^## C-|\Z)", text):
        cid, name, body = m.group(1), m.group(2).strip(), m.group(3)
        rules = re.search(r"\*\*Rules:\*\*\s*(.+)", body)
        status = re.search(r"\*\*Status:\*\*\s*(.+)", body)
        clash = re.search(r"(?s)\*\*The clash:\*\*\s*(.+?)(?=\n\*\*|\Z)", body)
        ids = re.findall(r"R\d+-[\w-]+", rules.group(1)) if rules else []
        out.append({"id": cid, "name": name, "rules": ids, "status": (status.group(1).strip() if status else "?"),
                    "clash": re.sub(r"\s+", " ", clash.group(1)).strip() if clash else "", "body": body.strip()})
    return out


def conflicts() -> list[dict]:
    return _conflicts_cache(CONFLICTS.stat().st_mtime) if CONFLICTS.exists() else []


def conflicts_for(rule_id: str) -> list[dict]:
    key = rule_id.upper()
    return [c for c in conflicts() if key in (r.upper() for r in c["rules"])]


# -- markdown for Discord ---------------------------------------------------

def plain(md: str) -> str:
    """Markdown fragment -> one line of plain text, for a snippet."""
    t = re.sub(r"(?:(?<=\s)|^)#{1,6}\s+", "", md)                 # heading marks, even mid-line
    t = re.sub(r"(?m)^\s*>\s?", "", t)                            # blockquotes
    t = re.sub(r"(\*\*|__|~~|`)", "", t)                          # bold, code
    t = re.sub(r"(?<!\w)[*_](?=\S)|(?<=\S)[*_](?!\w)", "", t)      # italics
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)                # links -> their text
    t = re.sub(r"(?m)^\s*[-|:]+\s*$", "", t)                      # table rules
    return re.sub(r"\s+", " ", t).strip()


def for_discord(md: str) -> str:
    """Whole page -> markdown Discord renders: H1-H3 kept, deeper headings bolded,
    table rows flattened to ' · ' lists, blank runs collapsed."""
    out = []
    for line in md.split("\n"):
        m = re.match(r"^\s{0,3}#{4,6}\s+(.*)$", line)
        if m:
            line = f"**{m.group(1).strip()}**"
        elif re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
            continue
        elif line.strip().startswith("|"):
            line = " · ".join(c.strip() for c in line.strip().strip("|").split("|") if c.strip())
        out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def _snippet(text: str, query: str, n: int = 2, width: int = 240) -> str:
    terms = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
    bits: list[str] = []
    for b in M._snippets(text, query, n=n * 3, width=width):
        b = plain(b.strip("."))
        if b and not any(b[:80] in x or x[:80] in b for x in bits):  # the same window found via two terms
            bits.append(b)
        if len(bits) >= n:
            break
    s = " … ".join(bits)
    for t in terms:
        s = re.sub(rf"(?i)(?<!\w)({re.escape(t)}\w*)", r"**\1**", s)
    return s or plain(text[:width])


# -- wiki, cards, scenes ----------------------------------------------------

def notion_url(page: Path) -> str | None:
    rel = page.relative_to(WIKI).as_posix()
    for pid, v in M._wiki_manifest().items():
        if v.get("rel") == rel:
            return "https://www.notion.so/" + pid.replace("-", "")
    return None


def _category(p: Path) -> str:
    return p.parent.name if p.parent != WIKI else ""


def wiki_hits(query: str, limit: int = 5) -> list[dict]:
    hits = []
    for score, p, _ in M._rank(WIKI, query, limit=limit):
        hits.append({"title": p.stem, "category": _category(p), "rel": p.relative_to(WIKI).as_posix(),
                     "score": score, "snippet": _snippet(M._read(p), query), "url": notion_url(p)})
    return hits


def wiki_page(rel_or_query: str) -> tuple[str, str, str | None, str]:
    """(title, text, notion_url, category) for a wiki path, else for the best match to a query."""
    p = WIKI / rel_or_query
    if not p.is_file():
        hits = M._rank(WIKI, rel_or_query)
        if not hits:
            return "", "", None, ""
        p = hits[0][1]
    return p.stem, for_discord(M._read(p)), notion_url(p), _category(p)


def scene_hits(query: str, limit: int = 4) -> list[dict]:
    hits = []
    for score, p, _ in M._rank(SCENES, query, limit=limit):
        text = M._read(p)
        m = re.search(r"(?m)^#\s+(.+)$", text)
        hits.append({"title": m.group(1).strip() if m else p.stem, "file": p.name, "score": score,
                     "snippet": _snippet(text, query, n=3, width=360)})
    return hits


def scene_text(file: str) -> tuple[str, str]:
    p = SCENES / file
    if not p.is_file():
        return "", ""
    text = M._read(p)
    m = re.search(r"(?m)^#\s+(.+)$", text)
    return (m.group(1).strip() if m else p.stem), for_discord(text)


def character(name: str) -> str:
    return for_discord(M.character(name))


def character_page(name: str) -> dict | None:
    """The best card for a name: {title, text, url, category, also}. None when there is no card."""
    key = name.lower().strip()
    cands = [p for p in WIKI.rglob("*.md") if p.name != "INDEX.md" and (key in p.stem.lower() or key in p.parent.name.lower())]
    if not cands:
        return None
    cands.sort(key=lambda p: (0 if key == p.stem.lower() else 1, 0 if "character" in p.parent.name.lower() else 1, len(p.stem)))
    p = cands[0]
    return {"title": p.stem, "text": for_discord(M._read(p)), "url": notion_url(p), "category": _category(p),
            "also": [c.stem for c in cands[1:6]]}


def fow_line(name: str) -> str:
    return for_discord(M.fow_line(name))


def timeline() -> str:
    return for_discord(M.timeline())


@lru_cache(maxsize=1)
def _names_cache(mtime: float) -> list[str]:
    names = set()
    if CAST.exists():
        names.update(re.findall(r"(?m)^## (.+?) \(", CAST.read_text(encoding="utf-8")))
    for d in WIKI.glob("Volume * Character Cards"):
        names.update(p.stem for p in d.glob("*.md"))
    return sorted(names)


def character_names(prefix: str = "", limit: int = 25) -> list[str]:
    mtime = CAST.stat().st_mtime if CAST.exists() else 0.0
    key = prefix.strip().lower()
    return [n for n in _names_cache(mtime) if key in n.lower()][:limit]
