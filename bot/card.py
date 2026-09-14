"""A character card split for display: overview, key facts, and its sections."""
import re

import wotr as W

KV_RX = re.compile(r"\*\*([^*\n]{2,48}?)\s*[:：]?\*\*\s*[:·]?\s*(.*?)(?=\s+\*\*[^*\n]{2,48}?\s*[:：]?\*\*|$)")
FACT_LIMIT = 9


def clean(md: str) -> str:
    """Card markdown -> Discord: no H1, no horizontal rules, no empty quote lines."""
    out = []
    for line in md.split("\n"):
        if re.match(r"^\s*#\s", line) or re.match(r"^\s*([-*_]\s*){3,}$", line) or re.match(r"^\s*>\s*$", line):
            continue
        out.append(line)
    return W.for_discord("\n".join(out))


def facts_in(text: str) -> list[tuple[str, str]]:
    facts: list[tuple[str, str]] = []
    for line in text.split("\n"):
        line = line.lstrip("> ").strip()
        for k, v in KV_RX.findall(line):
            k, v = k.strip(), v.strip(" ·:")
            if (v and v[0].isalnum() and not k.endswith(".") and len(k) <= 30 and len(facts) < FACT_LIMIT
                    and k not in {f[0] for f in facts}):
                facts.append((k, W.plain(v)[:200]))
    return facts


PRIMARIES = ("Vitality", "Ardency", "Gnosis", "Dexterity", "Harmonics", "Resilience", "Tempering", "Dominion")


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def fow(name: str) -> dict | None:
    """The card's FOW line as structure: facts, one row per Primary, and the card's own notes."""
    d = W.character_page(name)
    if not d:
        return None
    raw = W.M.fow_line(name)
    facts: list[tuple[str, str]] = []
    rows: list[dict] = []
    notes: list[str] = []
    for line in raw.split("\n")[1:]:
        s = line.strip()
        if not s or s.startswith("#") or re.match(r"^\|?\s*-{3,}", s):
            continue
        if s.startswith("|"):
            c = _cells(s)
            if len(c) >= 3 and c[0].strip("* ") in PRIMARIES:
                rows.append({"primary": c[0].strip("* "), "value": W.plain(c[1]), "grade": W.plain(c[2]),
                             "peaks": W.plain(c[3]) if len(c) > 3 else ""})
            elif len(c) >= 2 and c[0].startswith("**") and c[0].strip("* ") not in ("Stat",):
                facts.append((c[0].strip("* :"), W.plain(" · ".join(x for x in c[1:] if x))[:300]))
            continue
        body = s.lstrip("> ").strip()
        kv = [(k.strip(" :"), W.plain(v.strip(" ·:"))[:300]) for k, v in KV_RX.findall(body)]
        kv = [(k, v) for k, v in kv if v and len(k) <= 30 and len(k.split()) <= 3 and not k.endswith(".")]
        if kv and len(body) < 400:
            facts.extend(kv)
        elif s.startswith(">") and len(notes) < 3 and W.plain(body):
            notes.append(W.plain(body)[:400])
    seen, uniq = set(), []
    for k, v in facts:
        if k not in seen:
            seen.add(k)
            uniq.append((k, v))
    d.update({"facts": uniq[:12], "rows": rows, "notes": notes, "empty": not (uniq or rows)})
    return d


def load(name: str) -> dict | None:
    d = W.character_page(name)
    if not d:
        return None
    path = next(p for p in W.WIKI.rglob(d["title"] + ".md"))
    raw = W.M._read(path)
    parts = re.split(r"(?m)^##\s+", raw)
    head, rest = parts[0], parts[1:]
    sections = []
    for chunk in rest:
        h, _, body = chunk.partition("\n")
        body = clean(body)
        if body.strip():
            sections.append((h.strip(), body))
    d.update({"overview": clean(head), "facts": facts_in(head + "\n" + (rest[0] if rest else "")), "sections": sections})
    return d
