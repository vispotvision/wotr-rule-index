#!/usr/bin/env python3
"""The roster the character-lore workflow works from (.claude/workflows/character-lore.js).

  python build/lore_roster.py            # writes imports/lore/_roster.json and _graph.json, prints a summary

One row per card in wiki/Volume I — Character Cards (plus the cards that live in a
character's own section): the file, the Notion page id, the affiliation line, the
Relationships text, which other cards it names, who shares its surname, which
archived scenes it appears in (scenes/CAST.md), and whether the card already
carries the Lore section. _graph.json holds the weighted edges and a first-cut
grouping (merge the heaviest edges, nine to a group) for the Cartographer to refine.
Read-only on wiki/ and scenes/.
"""
import collections
import glob
import itertools
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOL = ROOT / "wiki" / "Volume I — Character Cards"
EXTRA = [ROOT / "wiki" / "Hild Ice (Stark) — The Sword Princess" / "Robin Ice — The Bastard Runner.md"]
OUT = ROOT / "imports" / "lore"
LORE_HEAD = "Lore · The Life Behind the Card"
PC = {"Sodoku Moto"}                                  # Isaac's PC: canon-only record, nothing invented
POV = {"Hild Ice (Stark)", "Kwon Mu-jin", "Robin Ice"}  # scene-heavy: the archive outranks invention
STOP = {"The", "Lord", "Sir", "Commander", "Elder", "Dr.", "Lady", "King", "Master"}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main() -> None:
    manifest = json.loads((ROOT / "wiki" / ".manifest.json").read_text(encoding="utf-8"))
    cards = []
    for f in sorted(VOL.glob("*.md")) + [p for p in EXTRA if p.exists()]:
        text = f.read_text(encoding="utf-8")
        head = re.match(r"---\n(.*?)\n---\n", text, re.S)
        meta = dict(re.findall(r'^(\w+): "?(.*?)"?$', head.group(1), re.M)) if head else {}
        title = (meta.get("title") or f.stem).replace('\\"', '"')
        name = re.split(r" · | — |, The ", title)[0].replace('"', "").strip()
        body = text[head.end():] if head else text
        aff = (re.search(r"#### Affiliation\s*\n+(.+)", body) or re.search(r"\*\*Affiliation\*\*\s*·?\s*(.+)", body)
               or re.search(r"\*\*Role\*\*\s*·\s*(.+)", body))
        rel = re.search(r"#+ [^\n]*Relationships\s*\n(.*?)(?=\n#+ |\Z)", body, re.S)
        era = re.search(r"\b(\w+ (?:Era|Age))\b", body)
        pid = meta.get("notion_id", "")
        cards.append(dict(
            slug=slug(f.stem), name=name, title=title, file=str(f.relative_to(ROOT)), notion_id=pid,
            private=bool(manifest.get(pid, {}).get("private")), bytes=len(text), era=era.group(1) if era else "",
            affiliation=aff.group(1).strip()[:300] if aff else "", relationships=rel.group(1).strip()[:1200] if rel else "",
            has_lore=LORE_HEAD in body, mode="record" if name in PC else "pov" if name in POV else "full",
            _body=body))

    toks = {c["slug"]: [t for t in c["name"].split() if t not in STOP] or [c["name"]] for c in cards}
    firsts = collections.Counter(t[0] for t in toks.values())
    for c in cards:
        t = toks[c["slug"]]
        c["_keys"] = {c["name"]} | ({t[0]} if firsts[t[0]] == 1 and len(t[0]) >= 4 else set())
        c["_last"] = t[-1] if len(t) > 1 else None

    cast = (ROOT / "scenes" / "CAST.md").read_text(encoding="utf-8")
    scenes = {re.sub(r" \(a\.k\.a\..*\)$", "", m.group(1)): re.findall(r"([\w.\-]+\.md) \(\d+\)", m.group(2))
              for m in re.finditer(r"^## (.+?) \(\d+ scenes?\)\n(.+)$", cast, re.M)}
    for c in cards:
        c["mentions"] = sorted({o["slug"] for o in cards if o is not c and o["name"] != c["name"] and any(
            re.search(r"(?<![\w'-])" + re.escape(k) + r"(?![\w'-])", c["_body"]) for k in o["_keys"])})
        c["same_surname"] = sorted(o["slug"] for o in cards if o is not c and c["_last"] and o["_last"] == c["_last"])
        c["scenes"] = next((v for k, v in scenes.items() if k == c["name"] or k.startswith(c["name"] + " (")), [])
        c["dupe_of"] = sorted(o["slug"] for o in cards if o is not c and o["name"] == c["name"])
    carded = {c["name"] for c in cards}
    uncarded = [k for k in scenes if k not in carded and not any(k.startswith(n + " (") for n in carded)]

    w = collections.Counter()
    for c in cards:
        for o in c["mentions"] + c["same_surname"]:
            w[tuple(sorted((c["slug"], o)))] += 3
    for a, b in itertools.combinations(cards, 2):
        n = len(set(a["scenes"]) & set(b["scenes"]))
        if n:
            w[(a["slug"], b["slug"]) if a["slug"] < b["slug"] else (b["slug"], a["slug"])] += min(n, 3)
    parent = {c["slug"]: c["slug"] for c in cards}
    size = dict.fromkeys(parent, 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (a, b), _ in sorted(w.items(), key=lambda kv: -kv[1]):
        ra, rb = find(a), find(b)
        if ra != rb and size[ra] + size[rb] <= 9:
            parent[rb], size[ra] = ra, size[ra] + size[rb]
    groups = collections.defaultdict(list)
    for s in parent:
        groups[find(s)].append(s)

    OUT.mkdir(parents=True, exist_ok=True)
    rows = [{k: v for k, v in c.items() if not k.startswith("_")} for c in cards]
    (OUT / "_roster.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "_graph.json").write_text(json.dumps({
        "groups": sorted(groups.values(), key=len, reverse=True),
        "edges": [[a, b, n] for (a, b), n in sorted(w.items(), key=lambda kv: -kv[1])],
        "uncarded_in_scenes": uncarded}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(rows)} cards, {sum(r['has_lore'] for r in rows)} already carry the Lore section, "
          f"{sum(bool(r['scenes']) for r in rows)} appear in scenes; {len(groups)} first-cut groups; "
          f"uncarded names in scenes: {', '.join(uncarded)}")


if __name__ == "__main__":
    main()
