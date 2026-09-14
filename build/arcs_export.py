#!/usr/bin/env python3
"""Reader copies of the scene archive in reading order (scenes/ARCS.md):
one Word document per arc, and one epub per arc plus a complete epub.

  python build/arcs_export.py --out "$WOTR_DRIVE/War of the Realms — Documents/Arcs"   # the Drive mount (build/sync.sh does this when WOTR_DRIVE is set)

Only arcs whose scenes changed since the last run are rewritten (.manifest.json
in the output folder).
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENES = ROOT / "scenes"
sys.path.insert(0, str(ROOT / "build"))
import docs_export as D  # noqa: E402


def read_arcs() -> list[tuple[str, list[Path]]]:
    text = (SCENES / "ARCS.md").read_text(encoding="utf-8")
    arcs, cur = [], None
    for ln in text.split("\n"):
        h = re.match(r"^##\s+(.+)$", ln)
        if h:
            cur = (h.group(1).strip(), [])
            arcs.append(cur)
            continue
        m = re.match(r"^-\s+(\S+\.md)\s*$", ln.strip())
        if m and cur is not None and (SCENES / m.group(1)).exists():
            cur[1].append(SCENES / m.group(1))
    return [a for a in arcs if a[1]]


def scene_title(p: Path, md: str) -> str:
    m = re.search(r"(?m)^#\s+(.+?)\s*$", md)
    return (m.group(1).strip().strip("*") if m else p.stem.replace("_", " "))


def md_to_xhtml(md: str) -> str:
    """Enough markdown for prose: headings, paragraphs, emphasis, dividers, quotes."""
    out = []
    for block in re.split(r"\n\s*\n", md.replace("\r\n", "\n")):
        b = block.strip()
        if not b:
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", b)
        if h:
            lvl = min(len(h.group(1)) + 1, 6)
            out.append(f"<h{lvl}>{esc(h.group(2).strip('*'))}</h{lvl}>")
            continue
        if re.match(r"^(-{3,}|\*{3,})$", b):
            out.append('<p class="sep">⁂</p>')
            continue
        if b.startswith(">"):
            inner = " ".join(l.lstrip("> ").strip() for l in b.split("\n"))
            out.append(f"<blockquote><p>{inline(inner)}</p></blockquote>")
            continue
        if re.match(r"^[-*]\s", b):
            items = [re.sub(r"^[-*]\s+", "", l.strip()) for l in b.split("\n") if l.strip()]
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            continue
        out.append(f"<p>{inline(b.replace(chr(10), ' '))}</p>")
    return "\n".join(out)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


CSS = """body{font-family:Georgia,serif;line-height:1.45;margin:1em}h1,h2,h3{font-weight:normal}h1{font-size:1.6em}h2{font-size:1.25em;margin-top:2em}
p{margin:0 0 0.8em}p.sep{text-align:center;margin:1.4em 0}blockquote{margin:1em 2em;font-style:italic}"""


def build_epub(title: str, chapters: list[tuple[str, str]], out: Path) -> None:
    from ebooklib import epub
    book = epub.EpubBook()
    book.set_identifier(re.sub(r"\W+", "-", title.lower()))
    book.set_title(title)
    book.set_language("en")
    book.add_author("Isaac")
    style = epub.EpubItem(uid="style", file_name="style/main.css", media_type="text/css", content=CSS)
    book.add_item(style)
    items = []
    for i, (ctitle, md) in enumerate(chapters, 1):
        c = epub.EpubHtml(title=ctitle, file_name=f"ch{i:03d}.xhtml", lang="en")
        c.content = f"<h1>{esc(ctitle)}</h1>\n" + md_to_xhtml(re.sub(r"(?m)^#\s+.*$", "", md, count=1))
        c.add_item(style)
        book.add_item(c)
        items.append(c)
    book.toc = tuple(items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + items
    epub.write_epub(str(out), book)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "docs" / "arcs"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    man_p = out / ".manifest.json"
    manifest = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}

    arcs = read_arcs()
    all_chapters = []
    written = 0
    for name, files in arcs:
        chapters = []
        for p in files:
            md, _ = D.strip_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            chapters.append((scene_title(p, md), md))
        all_chapters += chapters
        h = hashlib.sha256("\n".join(t + m for t, m in chapters).encode("utf-8")).hexdigest()[:16]
        base = D.safe_name(name)
        if not a.force and manifest.get(base) == h and (out / f"{base}.docx").exists() and (out / f"{base}.epub").exists():
            continue
        doc = D.new_document(name, f"{len(chapters)} scenes, in reading order", [t for t, _ in chapters])
        for i, (t, md) in enumerate(chapters):
            D.add_page(doc, t, md, page_break=i < len(chapters) - 1)
        doc.save(out / f"{base}.docx")
        build_epub(f"War of the Realms — {name}", chapters, out / f"{base}.epub")
        manifest[base] = h
        written += 1
        print(f"  wrote {base}.docx / .epub ({len(chapters)} scenes)")
    h = hashlib.sha256("\n".join(t + m for t, m in all_chapters).encode("utf-8")).hexdigest()[:16]
    if a.force or manifest.get("_all") != h or not (out / "War of the Realms — The Scene Archive.epub").exists():
        build_epub("War of the Realms — The Scene Archive", all_chapters, out / "War of the Realms — The Scene Archive.epub")
        manifest["_all"] = h
        written += 1
        print(f"  wrote the complete epub ({len(all_chapters)} scenes)")
    man_p.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"{written} written -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
