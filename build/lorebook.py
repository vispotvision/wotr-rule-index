"""The lorebook: what a draft needs from the wiki before another line is written.

`context(draft)` scans a draft for every name the wiki mirror knows — characters,
places, artifacts, disciplines, factions — pulls the matching pages (cards in
full, other pages by their head), finds the prior scenes that touch the same
ground through the semantic index, flags struck Büri-register terms and names
the wiki has no page for. Nothing is written; the wiki is read as it stands.

The registry of names is built from page titles and their aliases (the parts
of "Aurelian Prudentius Custos Clausorum · The Primate", the first name on a
character card) and rebuilt when the mirror changes.
"""
from __future__ import annotations

import re
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
SCENES = ROOT / "scenes"

# sections whose one-word aliases are worth matching (a first name on a card,
# a beast, an artifact); elsewhere a lone word like "Iron" is noise
NAME_SECTIONS = ("Character Cards", "Characters", "Bestiary", "Artifacts", "Natural Beasts",
                 "The Called", "Summoned", "Aberrations", "The Fourteen", "Sodoku Moto")
# page titles that are section labels, not things a draft names
SKIP_TITLES = {"INDEX", "MANIFEST", "Geography", "War", "Misc", "Peoples", "Materials", "Techniques",
               "Characters", "Cosmology", "Disciplines", "Factions", "Spellcraft", "Reference Table",
               "In-World Document", "Information not on WIKI", "Lore & History", "Magic System",
               "Natural Beasts", "Summoned and Bound", "Aberrations", "Artifacts", "Bestiary"}
STOP = {"the", "and", "of", "a", "an", "in", "on", "at", "to", "for", "with", "by", "from", "as", "or",
        "his", "her", "their", "its", "he", "she", "they", "it", "who", "what", "when", "where", "which",
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "first", "last",
        "north", "south", "east", "west", "northern", "southern", "eastern", "western", "inner", "outer",
        "old", "new", "great", "high", "low", "long", "black", "white", "red", "iron", "gold", "silver",
        "king", "queen", "lord", "lady", "house", "hall", "gate", "wall", "road", "river", "sea", "sky",
        "fire", "water", "earth", "air", "stone", "blood", "bone", "night", "day", "world", "plane",
        "fate", "war", "peace", "crown", "sword", "blade", "hand", "fist", "eye", "heart", "voice",
        "state", "play", "table", "scene", "archive", "card", "cards", "volume", "chapter", "part",
        "master", "guide", "ledger", "register", "common", "tongue", "works", "days", "family", "families"}

_lock = threading.Lock()
_registry: dict | None = None


def _frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm = {}
    for ln in text[4:end].splitlines():
        m = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', ln)
        if m:
            fm[m.group(1)] = m.group(2)
    return fm, text[end + 5:]


HONORIFICS = r"^(?:Commander|Captain|General|Lord|Lady|Sir|Dame|Master|Mistress|Brother|Sister|Father|Mother|King|Queen|Prince|Princess|Saint|Doctor|Dr\.?|Emperor|Empress|Archon|Primate|High)\s+"


def _aliases(title: str, section: str) -> set[str]:
    out = set()
    parts = [p.strip(" *_") for p in re.split(r"\s+[·—/]\s+|\s+-\s+", title)]
    is_card = any(s in section for s in ("Character Cards", "Characters"))
    for p in parts:
        p = re.sub(r"^(The|A|An)\s+", "", p).strip()
        if not p or p.lower() in STOP:
            continue
        bare = re.sub(HONORIFICS, "", p).strip()  # "Commander Severin Bale" -> "Severin Bale"
        for q in {p, bare}:
            words = q.split()
            if len(words) >= 2:
                out.add(q)
            elif len(q) >= 4 and any(s in section for s in NAME_SECTIONS):
                out.add(q)
    if is_card:
        first = re.sub(HONORIFICS, "", parts[0]).split()
        if first and len(first[0]) >= 4 and first[0].lower() not in STOP and first[0][0].isupper():
            out.add(first[0].strip(","))
    return out


def _extra_aliases() -> dict[str, str]:
    """build/aliases.yaml: archive name -> exact page title (Darius is Ignatius's card)."""
    p = ROOT / "build" / "aliases.yaml"
    if not p.exists():
        return {}
    try:
        import yaml
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return {str(k): str(v) for k, v in data.items()}
    except Exception:
        return {}


def registry() -> dict:
    """alias -> [(page path, title, section, notion_url)], rebuilt when the mirror changes.
    Also carries the set of words the wiki uses in lowercase (a term, not a name)."""
    global _registry
    files = [p for p in WIKI.rglob("*.md") if p.name not in ("INDEX.md", "MANIFEST.md")]
    extra_p = ROOT / "build" / "aliases.yaml"
    stamp = (len(files), max((p.stat().st_mtime_ns for p in files), default=0),
             extra_p.stat().st_mtime_ns if extra_p.exists() else 0)
    with _lock:
        if _registry and _registry["stamp"] == stamp:
            return _registry
        by_alias: dict[str, list] = {}
        by_title: dict[str, tuple] = {}
        lower_words: set[str] = set()
        for p in files:
            raw = p.read_text(encoding="utf-8", errors="replace")
            fm, body = _frontmatter(raw)
            lower_words.update(re.findall(r"(?<![A-Za-z])[a-z][a-z'’]{3,}", body))
            title = fm.get("title") or p.stem
            if title in SKIP_TITLES:
                continue
            section = fm.get("section") or p.parent.name
            entry = (p, title, section, fm.get("notion_url", ""))
            by_title[title] = entry
            for a in _aliases(title, section):
                by_alias.setdefault(a, []).append(entry)
        for alias, title in _extra_aliases().items():
            if title in by_title:
                by_alias.setdefault(alias, []).append(by_title[title])
        # longest aliases first so "Söröl Ajiin" is tried before "Ajiin"
        order = sorted(by_alias, key=lambda a: (-len(a.split()), -len(a)))
        rx = {a: re.compile(r"(?<![\w\-])" + re.escape(a) + r"(?![\w\-])") for a in order}
        _registry = {"stamp": stamp, "aliases": by_alias, "order": order, "rx": rx, "lower": lower_words}
        return _registry


def _head(text: str, n: int) -> str:
    text = text.strip()
    if len(text) <= n:
        return text
    cut = text.rfind("\n\n", 0, n)
    return text[: cut if cut > n // 2 else n].rstrip() + "\n...[more on the page]"


def _unknown_names(draft: str, matched_aliases: set[str]) -> list[str]:
    """Capitalised words used like names that no page claims — the never-invent guard."""
    reg = registry()
    known = set()
    for a in list(matched_aliases) + reg["order"]:
        known.update(w.lower() for w in a.split())
    # a word the draft or the wiki also uses in lowercase is a term (scale, church), not a name
    lower = reg["lower"] | set(re.findall(r"(?<![A-Za-z])[a-z][a-z'’]{3,}", draft))
    counts: dict[str, int] = {}
    for m in re.finditer(r"(?<![.!?]\s)(?<!^)(?<!\n)\b([A-Z][a-zāēīōūöüáéíóúñ]{3,}(?:\s+[A-Z][a-zāēīōūöüáéíóúñ]{2,})?)\b", draft):
        w = m.group(1)
        first = w.split()[0].lower()
        if first in STOP or first in known or first in lower or first.rstrip("s") in lower:
            continue
        counts[w] = counts.get(w, 0) + 1
    return [w for w, c in sorted(counts.items(), key=lambda kv: -kv[1]) if c >= 2][:12]


def context(draft: str, budget: int = 24000, reversion: list[tuple[str, str]] | None = None) -> str:
    reg = registry()
    hits: dict[Path, dict] = {}
    matched: set[str] = set()
    for a in reg["order"]:
        n = len(reg["rx"][a].findall(draft))
        if not n:
            continue
        matched.add(a)
        weight = 2 if len(a.split()) >= 2 else 1
        for p, title, section, url in reg["aliases"][a]:
            h = hits.setdefault(p, {"title": title, "section": section, "url": url, "score": 0, "via": set()})
            h["score"] += n * weight * (2 if any(s in section for s in ("Character Cards", "Characters")) else 1)
            h["via"].add(a)
    ranked = sorted(hits.items(), key=lambda kv: -kv[1]["score"])

    out = [f"# SCENE CONTEXT — {len(ranked)} page(s) named in the draft"]
    if not ranked:
        out.append("no wiki page is named in this draft; if it introduces new people or places, create_character or a wiki page comes first")
    spent = len(out[0])
    shown = 0
    per_card = 6000 if len(ranked) <= 3 else 3500 if len(ranked) <= 8 else 2200
    per_page = 1800 if len(ranked) <= 8 else 1000
    more = []
    for p, h in ranked:
        is_card = any(s in h["section"] for s in ("Character Cards", "Characters"))
        _, body = _frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        text = _head(body, per_card if is_card else per_page)
        block = (f"\n## {h['title']}  ({h['section']}; named as {', '.join(sorted(h['via']))}; {h['url'] or p.relative_to(ROOT).as_posix()})\n"
                 + text + "\n")
        if spent + len(block) > budget * 0.7 and shown >= 2:
            more.append(f"{h['title']} ({h['section']}, via {', '.join(sorted(h['via']))})")
            continue
        out.append(block)
        spent += len(block)
        shown += 1
    if more:
        out.append("\n## Also named, not shown (call character / wiki for these)\n- " + "\n- ".join(more))

    # prior scenes on the same ground: three windows of the draft through the semantic index
    try:
        import embed_index as E
        windows = [draft[i:i + 1500] for i in (0, max(0, len(draft) // 2 - 750), max(0, len(draft) - 1500))]
        seen: dict[str, dict] = {}
        for w in windows:
            if not w.strip():
                continue
            for s in E.search(w, "scenes", limit=4, per_file=1):
                cur = seen.get(s["path"])
                if not cur or s["score"] > cur["score"]:
                    seen[s["path"]] = s
        prior = sorted(seen.values(), key=lambda s: -s["score"])[:5]
        if prior:
            out.append("\n## Prior scenes on the same ground (scene_recall for more; check TIMELINE.md before contradicting one)")
            for s in prior:
                head, text, _ = s["chunks"][0]
                out.append(f"- **{s['title']}** ({Path(s['path']).name}) — [{head}] " + text[:240].replace("\n", " ") + ("..." if len(text) > 240 else ""))
    except Exception as e:  # index missing or mid-rebuild: the lorebook still answers
        out.append(f"\n(prior-scene search unavailable: {e})")

    if reversion:
        struck = []
        for old, new in reversion:
            n = len(re.findall(r"(?<![\w\-])" + re.escape(old) + r"(?![\w\-])", draft))
            if n:
                struck.append(f"{old} ×{n} → {new}")
        if struck:
            out.append("\n## Struck Büri-register terms in the draft (the ruling is Moto in all new prose)\n- " + "\n- ".join(struck))

    unknown = _unknown_names(draft, matched)
    if unknown:
        out.append("\n## Names with no page (check before writing anything numeric or canonical about them; never invent)\n- " + "\n- ".join(unknown))
    return "\n".join(out)
