#!/usr/bin/env python3
"""The Obsidian view: vault/ generated from wiki/ and scenes/ with [[wikilinks]] injected, so
the graph and backlinks work. The mirror itself is never touched.

  python build/vault_export.py          # rebuild vault/ (gitignored); the sync runs it hourly

What gets linked, longest name first, first mention per page only, never inside a
heading, a link, code, or the page's own title:
  - every wiki page title (and the short form before " · " or " — ", e.g. "Sodoku Moto")
  - every character in scenes/CAST.md, and the aliases in build/aliases.yaml
Each scene gets a "Cast" line of links; each card gets an "Appears in" list from CAST.md;
vault/_Index.md lists sections; vault/.obsidian is left to the reader.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI, SCENES, VAULT = ROOT / "wiki", ROOT / "scenes", ROOT / "vault"
MANIFEST = json.loads((WIKI / ".manifest.json").read_text(encoding="utf-8"))


def short(title: str) -> str | None:
    s = re.split(r"\s+[·—]\s+", title)[0].strip()
    return s if s != title and len(s) >= 4 and " " in s or (s != title and len(s) >= 6) else None


def targets() -> dict[str, str]:
    """display name -> vault page (relative, without .md). Longest names first when applied."""
    out = {}
    for v in MANIFEST.values():
        rel = v["rel"][:-3]
        title = v["title"]
        out.setdefault(title, rel)
        sh = short(title)
        if sh:
            out.setdefault(sh, rel)
    cast = SCENES / "CAST.md"
    if cast.exists():
        for name in re.findall(r"(?m)^## (.+?) \(", cast.read_text(encoding="utf-8")):
            if name not in out:
                hit = next((rel for t, rel in out.items() if t.startswith(name)), None)
                if hit:
                    out[name] = hit
    al = ROOT / "build" / "aliases.yaml"
    if al.exists():
        import yaml
        for k, v in (yaml.safe_load(al.read_text(encoding="utf-8")) or {}).items():
            rel = next((r for t, r in out.items() if t == v), None)
            if rel:
                out[str(k)] = rel
    return out


_RX_CACHE: dict[int, "re.Pattern"] = {}


def _combined(names: list[tuple[str, str]]) -> "re.Pattern":
    key = id(names)
    if key not in _RX_CACHE:
        alt = "|".join(re.escape(n) for n, _ in names)  # longest first already
        _RX_CACHE[key] = re.compile(r"(?<![\w\[\|/])(" + alt + r")(?![\w\]\|])")
    return _RX_CACHE[key]


def link_text(md: str, names: list[tuple[str, str]], self_rel: str) -> str:
    """Inject [[rel|name]] for the first mention of each name on the page, outside headings,
    tables, code, and existing links. One combined pattern, one pass per paragraph."""
    lookup = dict(names)
    rx = _combined(names)
    out = []
    seen = set()  # one link per page: the first mention
    for para in md.split("\n\n"):
        if para.lstrip().startswith(("#", "```", "|", "---")):
            out.append(para)
            continue
        pieces, pos = [], 0
        for m in rx.finditer(para):
            name = m.group(1)
            rel = lookup.get(name)
            if not rel or rel == self_rel or name in seen:
                continue
            before = para[:m.start()]
            if before.count("[[") > before.count("]]") or before.count("](") > before.count(")"):
                continue
            pieces.append(para[pos:m.start()])
            pieces.append(f"[[{rel}|{name}]]")
            pos = m.end()
            seen.add(name)
        pieces.append(para[pos:])
        out.append("".join(pieces))
    return "\n\n".join(out)


def main() -> int:
    if VAULT.exists():
        shutil.rmtree(VAULT)
    (VAULT / "wiki").mkdir(parents=True)
    (VAULT / "scenes").mkdir(parents=True)
    tg = targets()
    names = sorted(tg.items(), key=lambda kv: -len(kv[0]))
    names = [(n, "wiki/" + r) for n, r in names if len(n) >= 4]
    cast_index = {}
    cast = SCENES / "CAST.md"
    if cast.exists():
        for m in re.finditer(r"(?m)^## (.+?) \(\d+ scenes\)\n(.+)$", cast.read_text(encoding="utf-8")):
            cast_index[m.group(1)] = re.findall(r"([\w\-.]+\.md) \(\d+\)", m.group(2))
    n_pages = 0
    for p in WIKI.rglob("*.md"):
        if p.name in ("INDEX.md", "MANIFEST.md"):
            continue
        rel = p.relative_to(WIKI).as_posix()[:-3]
        text = p.read_text(encoding="utf-8", errors="replace")
        body = text.split("\n---\n", 1)[1] if text.startswith("---") else text
        body = link_text(body, names, "wiki/" + rel)
        title = p.stem
        appears = [s for n, files in cast_index.items() if n in title or title.startswith(n) for s in files]
        if appears:
            body += "\n\n## Appears in\n" + "\n".join(f"- [[scenes/{s[:-3]}]]" for s in sorted(set(appears)))
        dest = VAULT / "wiki" / (rel + ".md")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8", newline="\n")
        n_pages += 1
    n_scenes = 0
    for p in sorted(SCENES.glob("*.md")):
        if p.name in ("MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        body = text.split("\n---\n", 1)[1] if text.startswith("---") else text
        who = [n for n, files in cast_index.items() if p.name in files]
        cast_line = ("\n\n**Cast:** " + " · ".join(f"[[{tg_rel}|{n}]]" for n in who for tg_rel in [next(("wiki/" + r for t, r in tg.items() if t.startswith(n)), None)] if tg_rel)) if who else ""
        body = link_text(body, names, "scenes/" + p.stem) + cast_line
        (VAULT / "scenes" / p.name).write_text(body, encoding="utf-8", newline="\n")
        n_scenes += 1
    for extra in ("TIMELINE.md", "ARCS.md", "CAST.md"):
        if (SCENES / extra).exists():
            shutil.copy(SCENES / extra, VAULT / "scenes" / extra)
    sections = sorted({v["rel"].split("/")[0] for v in MANIFEST.values()})
    (VAULT / "_Index.md").write_text("# War of the Realms — vault\n\nGenerated from the wiki mirror and the scene archive by build/vault_export.py; read-only, rebuilt by the hourly sync.\n\n## Sections\n"
                                     + "\n".join(f"- {s}" for s in sections) + "\n\n## Scenes\n- [[scenes/TIMELINE]] · [[scenes/ARCS]] · [[scenes/CAST]]\n", encoding="utf-8", newline="\n")
    print(f"vault: {n_pages} pages, {n_scenes} scenes, {len(names)} link targets -> {VAULT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
