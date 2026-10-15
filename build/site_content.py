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
    public = []
    for p in sorted(WIKI.rglob("*.md")):
        rel = p.relative_to(WIKI).as_posix()
        if rel == "INDEX.md" or rel.startswith(".") or rel in private:
            continue
        if any(rel == f or rel.startswith(f + "/") for f in closed):
            continue
        if re.search(r"(?m)^private:\s*true\s*$", p.read_text(encoding="utf-8")[:2000]):
            continue
        public.append(rel)
        kept[rel.split("/")[0] if "/" in rel else "Pages"].append(rel[:-3])
    names = {r[:-3] for r in public}
    unlink = lambda m: m.group(0) if m.group(1) in names else (m.group(2) or m.group(1).split("/")[-1])
    for rel in public:  # a link to a page left off the site reads as plain text
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        text = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]", unlink, (WIKI / rel).read_text(encoding="utf-8"))
        (out / rel).write_text(text, encoding="utf-8")
    lines = ["---", "title: War of the Realms", "---", ""]
    start = WIKI / "Start Here.md"
    if start.exists():
        lines += [re.sub(r"(?s)^---.*?---\n", "", (out / "Start Here.md").read_text(encoding="utf-8")).strip(), "", "# Every page", ""]
    for section in sorted(kept):
        lines += [f"## {section}", ""] + [f"- [[{r}|{r.split('/')[-1]}]]" for r in kept[section]] + [""]
    (out / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{sum(map(len, kept.values()))} public pages -> {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
