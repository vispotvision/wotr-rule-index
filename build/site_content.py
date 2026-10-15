"""Copy the public wiki pages into a Quartz content folder.

  python build/site_content.py <out_dir>

Private = marked private in wiki/.manifest.json (the Notion workroom), `private: true`
in a page's frontmatter, or new in a folder whose every manifest page is private.
"""
import json, re, shutil, sys
from html import escape
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_art import banner, plate
from site_charts import render as chart

WIKI = Path(__file__).resolve().parent.parent / "wiki"


BASE = "/wotr-rule-index"


NONPROSE = re.compile(r"(#|- |\* |\+ |\d+[.)] |\||>|```|~~~|!\[\[|<|---|\$\$|%%)")


def breathe(body: str) -> str:
    """Lines written one paragraph per line get the blank line markdown needs between them."""
    out, fence = [], False
    lines = body.split("\n")
    for a, b in zip(lines, lines[1:] + [""]):
        out.append(a)
        if a.strip().startswith(("```", "~~~")):
            fence = not fence
        prose = lambda l: bool(l.strip()) and not NONPROSE.match(l.strip())
        if not fence and prose(a) and prose(b) and not a.endswith(("  ", "\\")):
            out.append("")
        elif not fence and a.lstrip().startswith(">") and b.strip() and not b.lstrip().startswith(">"):
            out.append("")  # a quote ends before whatever follows it
    return "\n".join(out)


def unquote(m) -> str:
    """A quoted passage six paragraphs long is a section, not a quotation: set it as prose."""
    block = m.group(0)
    paras = [p for p in re.split(r"\n>\s*\n", block) if p.strip("> \n")]
    if len(paras) < 6 or re.match(r">\s*\[!", block):
        return block
    out = re.sub(r"(?m)^>[ \t]?", "", block)
    return re.sub(r"(?m)^\*\*([A-Z][A-Z0-9 ,'’·:—-]{3,})\*\*\s*$", lambda h: "### " + h.group(1).title().replace("’S", "’s").replace("'S", "'s"), out)


def onerow(m) -> str:
    """A table with one row of long prose reads better as cards side by side."""
    rows = [r.strip().strip("|").split("|") for r in m.group(0).strip().split("\n")]
    if len(rows) != 3 or not 2 <= len(rows[0]) <= 4 or sum(len(c) for c in rows[2]) < 160:
        return m.group(0)
    def body(c):
        c = c.strip().replace("<br>", "\n")
        named = re.findall(r"\*\*[^*]+\*\*", c)
        if len(named) >= 2 and c.startswith("**"):  # a run of named abilities: one line each
            parts = re.split(r"\s+(?=\*\*[^*]+\*\*)", c)
            return "\n".join(f"- {p.strip()}" for p in parts if p.strip())
        return c
    blocks = "".join(f'<div class="wotr-pane">\n\n**{h.strip()}**\n\n{body(c)}\n\n</div>\n\n'
                     for h, c in zip(rows[0], rows[2]) if c.strip())
    return f'\n<div class="wotr-panes">\n\n{blocks}</div>\n\n'


def glossary(m) -> str:
    """Short definitions become a grid of small cards; long ones stay as paragraphs."""
    entries = [e for e in m.group(1).strip().split("\n") if e.strip()]
    if sum(map(len, entries)) / len(entries) > 320:
        return m.group(0)
    return ('<div class="wotr-glossary">\n\n' + re.sub(r"(?m)^(\*\*[^*\n]+\*\*)\s*[:—–·-]\s*", r"\1 ", m.group(1).strip())
            + "\n\n</div>\n\n")


PROCESS = re.compile(r"\bIsaac\b(?! Newton)|\bNatalie\b|\bRULED\b|(?:^|[*\s])Ratified(?:\.|\s+(?:20\d\d|as written|against))|"
                     r"Amendment (?:status|applied)|agent ruling|ruling needed|\bR\d{2}[A-Z]?-[0-9A-Z]|\bDocket \d|"
                     r"Proposed canon|Originated, flagged|Echo Elf ratification|Canon ruling|retcon|Aesthetic Guide|⚠️|"
                     r"Closed against|Unratified|has not been altered|has no page|flagged not filled|Answers the open item|dead canon")
PROCESS_HEADING = re.compile(r"(?im)^(#{2,4}) [^\n]*(Open Rulings|Author'?s? Notes|Notes for the Author|Reconciliation note|Amendment status|Flagged Gaps|Open Questions|Discrepancies of Record)[^\n]*$")
REMOVED = []


def scrub(body: str) -> str:
    """The site is the world, not the workshop: rulings, ratifications, rule ids and notes to
    Isaac stay in the vault and come off the published page."""
    # whole process sections
    while True:
        m = PROCESS_HEADING.search(body)
        if not m:
            break
        level = len(m.group(1))
        nxt = re.compile(rf"(?m)^#{{1,{level}}} ").search(body, m.end())
        REMOVED.append(body[m.start():m.end()])
        body = body[:m.start()] + (body[nxt.start():] if nxt else "")
    body = re.sub(r"\s*\((?:R\d{2}[A-Z]?-[\w-]+(?:,\s*|;\s*)?)+\)", "", body)  # (R53-01, R63-2)
    body = re.sub(r"(?im)^\|\s*\**(?:[IVX]+ · )?(?:Open Rulings|Author'?s? Notes|Flagged Gaps)\**\s*\|.*\n", "", body)  # a contents row naming one
    body = re.sub(r"\s*See Open Rulings\.?", "", body)
    out = []
    for block in re.split(r"(\n\s*\n)", body):
        if not PROCESS.search(block) or block.lstrip().startswith(("<", "```")):
            out.append(block)
            continue
        lines = []
        for line in block.split("\n"):
            if not PROCESS.search(line):
                lines.append(line)
                continue
            lead = re.match(r"^(\s*(?:>\s*)*(?:[-*] |\d+\. )?)", line).group(1)
            if line.lstrip().startswith("|"):  # a table row: cut the sentence inside its cell
                cells = line.split("|")
                cells = [" ".join(x for x in re.split(r"(?<=[.!?])\s+", c) if not PROCESS.search(x)) if PROCESS.search(c) else c for c in cells]
                lines.append("|".join(c if c.strip() else " " for c in cells))
                continue
            rest = line[len(lead):]
            kept = [x for x in re.split(r"(?<=[.!?])\s+", rest) if not PROCESS.search(x)]
            REMOVED.append(rest)
            text = " ".join(kept).strip()
            if text and text.count("**") % 2 == 0 and text.count("*") % 2 == 0:
                lines.append(lead + text)
        out.append("\n".join(lines))
    return "".join(out)


def cards(m) -> str:
    """A run of link items becomes a grid of cards; the words after "link:" are the card's line."""
    items = re.sub(r"(?m)^(- \[\[[^\]]*\]\]):\s*(.+)$", r'\1 <span class="wd">\2</span>', m.group(1).rstrip("\n"))
    return f'\n<div class="wotr-entries">\n\n{items}\n\n</div>\n\n'


def pin_fill(svg: str) -> str:
    """Quartz styles every <text> with fill: var(--darkgray), which beats a fill attribute; an inline style does not lose."""
    return re.sub(r'<text([^>]*?) fill="([^"]+)"', r'<text\1 style="fill:\2"', svg)


def dress(rel: str, text: str) -> str:
    """Set the page's artwork where its markdown H1 stood (Quartz prints the title itself)."""
    fm = re.match(r"(?s)^---\n.*?\n---\n", text)
    head, body = (text[:fm.end()], text[fm.end():]) if fm else ("", text)
    t = re.search(r'(?m)^title:\s*"?(.*?)"?\s*$', head)
    stem = rel.rsplit("/", 1)[-1][:-3]
    title = t.group(1).replace('\\"', '"') if t else stem
    body = scrub(breathe(re.sub(r"\A\s*# [^\n]*\n", "\n", body, count=1)))
    first = re.match(r"\s*#{1,6} +(.+?)\s*\n", body)  # the plate already carries the title
    if first and re.sub(r"\W", "", first.group(1)).lower() == re.sub(r"\W", "", title).lower():
        body = body[first.end():]
    body = re.sub(r"(?m)^\|.*\|[ \t]*\n\|[ :|-]+\|[ \t]*\n\|.*\|[ \t]*(?:\n(?![ \t]*\|)|\Z)", onerow, body)
    body = re.sub(r"(?m)(?:^>.*\n?)+", unquote, body)
    body = re.sub(r"!\[\[Assets/Diagrams/([\w-]+)\.svg\]\]",  # inline, so the art draws in the site's own fonts
                  lambda m: '\n\n<figure class="wotr-figure">' + re.sub(r"<svg ", '<svg class="wotr-diagram" role="img" ', pin_fill((WIKI / f"Assets/Diagrams/{m.group(1)}.svg").read_text(encoding="utf-8")), count=1) + "</figure>\n\n", body)
    body = re.sub(r"(?ms)^```mermaid\n(.*?)^```[ \t]*$", lambda m: "\n\n" + pin_fill(chart(m.group(1), rel) or m.group(0)) + "\n\n", body)
    is_hub = "/" in rel and rel.split("/")[-2] == stem
    body = re.sub(r"(?m)((?:^- \[\[[^\n]*\n?){%d,})" % (1 if is_hub else 2), cards, body)
    body = re.sub(r"(?m)((?:^\*\*[^*\n]{1,60}\*\*\s*[:—–·-][^\n]+\n\n?){4,})",  # a run of "**Term**: meaning" lines
                  glossary, body)
    # a divider straight before a heading doubles the heading's own rule
    body = re.sub(r"(?m)^(?:---|\*\*\*|___)[ \t]*\n\s*\n(?=#{2,3} )", "", body)
    # a line that is wholly bold is a lead-in: set it as one
    body = re.sub(r"(?m)^\*\*([^*\n`\[\]]{3,160})\*\*[ \t]*$", lambda m: f'<p class="wotr-lede">{escape(m.group(1))}</p>\n', body)
    # the pronunciation line
    body = re.sub(r"(?m)^\*\*Say it\*\*\s*·\s*(.+)$", lambda m: f'<p class="wotr-sayit"><span>Say it</span>{escape(m.group(1).strip())}</p>\n', body)
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
    lines = ["---", "title: Every Page", "---", "", "Every page on the public wiki, by section and shelf.", ""]
    for section in sorted(kept):
        lines += [f"## {section}", ""]
        shelves = defaultdict(list)
        for r in kept[section]:
            parts = r.split("/")
            shelves[parts[1] if len(parts) > 2 else ""].append(r)
        for shelf in sorted(shelves, key=lambda k: (k != "", k)):
            if shelf:
                lines += [f"### {shelf}", ""]
            lines += [f"- [[{r}|{titles.get(r, r.split('/')[-1])}]]" for r in shelves[shelf]] + [""]
    (out / "Every Page.md").write_text("\n".join(lines), encoding="utf-8")
    # the site's front page is site/landing.html, laid over Quartz's index after the build
    (out / "index.md").write_text("---\ntitle: War of the Realms\n---\n\n[[Start Here]] · [[Every Page]]\n", encoding="utf-8")
    print(f"{sum(map(len, kept.values()))} public pages -> {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
