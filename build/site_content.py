"""Copy the public wiki pages into a Quartz content folder.

  python build/site_content.py <out_dir>

Private = marked private in wiki/.manifest.json (the Notion workroom), `private: true`
in a page's frontmatter, or new in a folder whose every manifest page is private.
"""
import json, re, shutil, sys
from collections import defaultdict
from pathlib import Path

WIKI = Path(__file__).resolve().parent.parent / "wiki"


def main(out: Path) -> None:
    man = json.loads((WIKI / ".manifest.json").read_text(encoding="utf-8")).values()
    private = {m["rel"] for m in man if m.get("private")}
    folders = defaultdict(set)
    for m in man:
        folders[m["rel"].rsplit("/", 1)[0] if "/" in m["rel"] else ""].add(bool(m.get("private")))
    closed = {f for f, flags in folders.items() if f and flags == {True}}
    if out.exists():
        shutil.rmtree(out)
    kept = defaultdict(list)
    for p in sorted(WIKI.rglob("*.md")):
        rel = p.relative_to(WIKI).as_posix()
        if rel == "INDEX.md" or rel.startswith(".") or rel in private:
            continue
        if any(rel == f or rel.startswith(f + "/") for f in closed):
            continue
        if re.search(r"(?m)^private:\s*true\s*$", p.read_text(encoding="utf-8")[:2000]):
            continue
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out / rel)
        kept[rel.split("/")[0] if "/" in rel else "Pages"].append(rel[:-3])
    lines = ["---", "title: War of the Realms", "---", "",
             "A dark shonen cultivation fantasy in a magitech world. Every page below is open to read.", ""]
    for section in sorted(kept):
        lines += [f"## {section}", ""] + [f"- [[{r}|{r.split('/')[-1]}]]" for r in kept[section]] + [""]
    (out / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{sum(map(len, kept.values()))} public pages -> {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
