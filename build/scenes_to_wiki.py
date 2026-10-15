"""Mirror scenes/*.md into the Obsidian vault at wiki/The Scene Archive/Scenes/, one page per
scene titled by its H1, marked private (off the public site). scenes/ stays the source:
edits made to these copies are overwritten on the next run."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "wiki" / "The Scene Archive" / "Scenes"
SKIP = {"MANIFEST.md", "CONTINUITY.md", "CAST.md", "TIMELINE.md", "README.md", "00_SUPERSEDED_wrong_names.md"}


def title_of(p: Path, md: str) -> str:
    m = re.search(r"(?m)^#\s+(.+?)\s*$", md)
    return (m.group(1).strip().strip("*") if m else p.stem.replace("_", " ")).strip()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    made = {}
    for p in sorted((ROOT / "scenes").glob("*.md")):
        if p.name in SKIP or p.name.startswith(("00_", "_")):
            continue
        md = p.read_text(encoding="utf-8", errors="replace")
        name = re.sub(r'[/\\:*?"<>|]', "", title_of(p, md)) or p.stem
        if name in made:
            name = f"{name} ({p.stem})"
        made[name] = p
        body = re.sub(r"(?m)\A#\s+.+\n+", "", md)
        page = (f"---\ntitle: \"{name}\"\nprivate: true\nsource: scenes/{p.name}\n---\n\n"
                f"> Mirrored from `scenes/{p.name}`; edit it there.\n\n{body.strip()}\n")
        dst = OUT / f"{name}.md"
        if not dst.exists() or dst.read_text(encoding="utf-8") != page:
            dst.write_text(page, encoding="utf-8", newline="\n")
    stale = [q for q in OUT.glob("*.md") if q.stem not in made]
    for q in stale:
        q.unlink()
    print(f"{len(made)} scenes mirrored, {len(stale)} stale removed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
