"""/define: where the wiki defines a term — a glossary row, a bold-term line, a heading — not
merely where it is mentioned. Returns the defining text verbatim with its page."""
import re
from pathlib import Path

import wotr as W

GLOSSARY_HINT = re.compile(r"codex|index|glossary|tongue|terms|lexicon|vocabulary|reference|errata", re.I)


def _defining_patterns(term: str) -> list[re.Pattern]:
    t = re.escape(term.strip())
    return [
        re.compile(rf"^\s*(?:[-*•]\s*)?(?:\*\*|__)\s*{t}\s*(?:\([^)]*\))?\s*(?:\*\*|__)\s*[—–:\-·]\s*(.+)$", re.I),  # **Term** — def
        re.compile(rf"^\s*\|\s*(?:\*\*)?\s*{t}\s*(?:\*\*)?\s*\|\s*(.+?)\s*\|?\s*$", re.I),                         # | Term | def |
        re.compile(rf"^\s*(?:[-*•]\s*)?{t}\s*[—–:]\s*(.+)$", re.I),                                              # Term — def
        re.compile(rf"^#{{1,6}}\s*{t}\b.*$", re.I),                                                                # ## Term (heading)
    ]


def _after_heading(lines: list[str], i: int, n: int = 6) -> str:
    out = []
    for ln in lines[i + 1:i + 1 + n * 3]:
        if ln.startswith("#"):
            break
        if ln.strip():
            out.append(ln.strip())
        if len(out) >= n:
            break
    return " ".join(out)


def lookup(term: str, limit: int = 5) -> list[dict]:
    term = term.strip().strip("*_\"'")
    if not term:
        return []
    pats = _defining_patterns(term)
    hits = []
    for p in W.WIKI.rglob("*.md"):
        if p.name == "INDEX.md":
            continue
        text = W.M._read(p)
        if term.lower() not in text.lower():
            continue
        lines = text.split("\n")
        for i, ln in enumerate(lines):
            for k, pat in enumerate(pats):
                m = pat.match(ln)
                if not m:
                    continue
                body = _after_heading(lines, i) if k == 3 else m.group(1)
                score = ((3 if p.stem.lower() == term.lower() else 0) + (2 if GLOSSARY_HINT.search(p.parent.name + p.stem) else 0)
                         + (3 - k) - (3 if "Character Cards" in p.parent.name else 0))
                hits.append({"score": score, "page": p.stem, "category": W._category(p), "url": W.notion_url(p),
                             "text": W.plain(body)[:700], "kind": ["bold", "table", "plain", "heading"][k]})
                break
    hits.sort(key=lambda h: -h["score"])
    seen, out = set(), []
    for h in hits:
        key = (h["page"], h["text"][:60])
        if key not in seen:
            seen.add(key)
            out.append(h)
        if len(out) >= limit:
            break
    return out


def mentions(term: str) -> list[dict]:
    """Fallback: the best pages that merely mention it."""
    return W.wiki_hits(term, limit=3)
