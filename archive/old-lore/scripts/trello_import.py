#!/usr/bin/env python3
"""Stage a Trello board export for conversion: one markdown file per card that
is not already in the wiki, grouped by target, plus the briefs the conversion
agents read.

  python build/trello_import.py "<board export>.json"

Writes imports/trello/<group>/<slug>.md and imports/MANIFEST.json. The briefs
in imports/BRIEFS/ are assembled from the wiki mirror and the rule index by
build/conversion_briefs.py.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
OUT = ROOT / "imports" / "trello"

GROUPS = {
    "[ Volume  IV  ]": ("characters", "Volume I — Character Cards"),
    "[ Volume V ]": ("characters", "Volume I — Character Cards"),
    "[ Volume VI ]": ("characters", "Volume I — Character Cards"),
    "Abilities": ("techniques", "The Iridescent Archive / Techniques"),
    "[ Spellcraft ]": ("spellcraft", "The Iridescent Archive / Spellcraft"),
    "[ Artifacts ]": ("artifacts", "The Iridescent Archive / Artifacts"),
    "[ Bestiary ]": ("beasts", "The Iridescent Archive / Bestiary Additions"),
}


def key_of(name: str) -> str:
    q = re.findall(r"[“”\"]\s*([^“”\"]+?)\s*[”“\"]", name)
    if q:
        return q[-1].strip()
    n = re.sub(r"^\s*[\[<|][^\]>|]*[\]>|]\s*", "", name).strip()
    return re.sub(r"\s*[-–—|].*$", "", n).strip()


def slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U).strip().lower()
    return re.sub(r"[\s_-]+", "_", s)[:70] or "untitled"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    board = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace"))
    lists = {l["id"]: l["name"].strip() for l in board["lists"]}
    checklists = {}
    for cl in board.get("checklists", []):
        checklists.setdefault(cl.get("idCard"), []).append((cl.get("name", ""), [i.get("name", "") for i in cl.get("checkItems", [])]))
    corpus = [p.read_text(encoding="utf-8", errors="replace").lower() for p in WIKI.rglob("*.md")]

    manifest = []
    for c in board["cards"]:
        L = lists.get(c["idList"])
        if L not in GROUPS or c.get("closed"):
            continue
        group, target = GROUPS[L]
        key = key_of(c["name"])
        if len(key) >= 4 and any(key.lower() in t for t in corpus):
            continue  # already in the wiki under some page
        name = c["name"].strip()
        s = slug(key or name)
        d = OUT / group
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{s}.md"
        n = 2
        while path.exists():
            path = d / f"{s}_{n}.md"; n += 1
        body = [f"# {name}", "", f"*Trello list: {L} · labels: {', '.join(l.get('name', '') for l in c.get('labels', []))} · target: {target}*", "", "---", "",
                c.get("desc", "").strip(), ""]
        for cl_name, items in checklists.get(c["id"], []):
            body += [f"### Checklist: {cl_name}"] + [f"- {i}" for i in items] + [""]
        att = [a.get("name", "") for a in c.get("attachments", []) if a.get("name")]
        if att:
            body += ["### Attachments (not imported)"] + [f"- {a}" for a in att] + [""]
        path.write_text("\n".join(body), encoding="utf-8", newline="\n")
        manifest.append({"file": path.relative_to(ROOT).as_posix(), "name": name, "key": key, "group": group, "target": target,
                         "words": len(c.get("desc", "").split()), "labels": [l.get("name", "") for l in c.get("labels", [])]})
    (ROOT / "imports" / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    from collections import Counter
    cnt = Counter(m["group"] for m in manifest)
    print(f"{len(manifest)} cards staged: " + ", ".join(f"{k}={v}" for k, v in cnt.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
