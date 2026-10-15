"""Copy the public wiki pages into a Quartz content folder.

  python build/site_content.py <out_dir>

Private = marked private in wiki/.manifest.json (the Notion workroom), `private: true`
in a page's frontmatter, or new in a folder whose every manifest page is private.
"""
import json, re, shutil, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_art import banner, plate
from site_charts import render as chart

WIKI = Path(__file__).resolve().parent.parent / "wiki"


BASE = "/wotr-rule-index"


def cards(m) -> str:
    """A run of link items becomes a grid of cards; the words after "link:" are the card's line."""
    items = re.sub(r"(?m)^(- \[\[[^\]]*\]\]):\s*(.+)$", r'\1 <span class="wd">\2</span>', m.group(1).rstrip("\n"))
    return f'<div class="wotr-entries">\n\n{items}\n\n</div>\n'


def dress(rel: str, text: str) -> str:
    """Set the page's artwork where its markdown H1 stood (Quartz prints the title itself)."""
    fm = re.match(r"(?s)^---\n.*?\n---\n", text)
    head, body = (text[:fm.end()], text[fm.end():]) if fm else ("", text)
    t = re.search(r'(?m)^title:\s*"?(.*?)"?\s*$', head)
    stem = rel.rsplit("/", 1)[-1][:-3]
    title = t.group(1).replace('\\"', '"') if t else stem
    body = re.sub(r"\A\s*# [^\n]*\n", "\n", body, count=1)
    body = re.sub(r"!\[\[Assets/Diagrams/([\w-]+)\.svg\]\]",  # inline, so the art draws in the site's own fonts
                  lambda m: '<figure class="wotr-figure">' + re.sub(r"<svg ", '<svg class="wotr-diagram" role="img" ', (WIKI / f"Assets/Diagrams/{m.group(1)}.svg").read_text(encoding="utf-8"), count=1) + "</figure>", body)
    body = re.sub(r"(?ms)^```mermaid\n(.*?)^```[ \t]*$", lambda m: "\n" + (chart(m.group(1), rel) or m.group(0)) + "\n", body)
    body = re.sub(r"(?m)((?:^- \[\[[^\n]*\n?){2,})", cards, body)
    hub = "/" in rel and rel.split("/")[-2] == stem
    if hub and "wotr-entries" in body:  # the page lists its own contents; Quartz's folder list would repeat it
        body += '\n<span class="wotr-curated"></span>\n'

    art = banner(rel, title, BASE) if hub else plate(rel, title)
    return head + "\n" + art + body.lstrip("\n")


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
    keep = lambda t: t in names or ("." in t.rsplit("/", 1)[-1] and (WIKI / t).is_file())
    titles = {}
    for r in public:
        t = re.search(r'(?m)^title:\s*"?(.*?)"?\s*$', (WIKI / r).read_text(encoding="utf-8")[:1500])
        titles[r[:-3]] = t.group(1).replace('\\"', '"') if t else r[:-3].split("/")[-1]

    def unlink(m):
        target, alias = m.group(1), m.group(2)
        if not keep(target):
            return alias or target.split("/")[-1]
        if alias or target not in titles:  # embeds and aliased links stand as written
            return m.group(0)
        return m.group(0)[:-2] + "|" + titles[target].replace("|", "-") + "]]"  # a bare link reads as its page's title
    for rel in public:  # a link to a page left off the site reads as plain text
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        text = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]", unlink, (WIKI / rel).read_text(encoding="utf-8"))
        (out / rel).write_text(dress(rel, text), encoding="utf-8")
    shutil.copytree(WIKI / "Assets", out / "Assets")
    lines = ["---", "title: Every Page", "---", "", "Every page on the public wiki, by section.", ""]
    for section in sorted(kept):
        lines += [f"## {section}", ""] + [f"- [[{r}|{r.split('/')[-1]}]]" for r in kept[section]] + [""]
    (out / "Every Page.md").write_text("\n".join(lines), encoding="utf-8")
    # the site's front page is site/landing.html, laid over Quartz's index after the build
    (out / "index.md").write_text("---\ntitle: War of the Realms\n---\n\n[[Start Here]] · [[Every Page]]\n", encoding="utf-8")
    print(f"{sum(map(len, kept.values()))} public pages -> {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
