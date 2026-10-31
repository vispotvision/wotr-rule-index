#!/usr/bin/env python3
"""Install finished card drafts that pass the checks; hold the rest.

  python imports/drafts/card-update/install.py            # report only
  python imports/drafts/card-update/install.py --apply    # write passing cards live

Passing: frontmatter first, full head, ADDITIONS block, no number lost, 85%+ of the
original's long sentences kept verbatim. Additions and doubts of every installed card go
to wiki/Author's Workroom/Card Update Review/Card Update Review.md, grouped by culture.
Installed cards are recorded in installed.txt so a rerun skips them.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import check  # noqa: E402

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
DRAFTS, LIST, DONE = HERE / "rest", HERE / "rest.list", HERE / "installed.txt"
REVIEW = ROOT / "wiki/Author's Workroom/Card Update Review/Card Update Review.md"


def serious(probs: list[str]) -> list[str]:
    out = []
    for p in probs:
        if p.startswith("bold labels gone") or p.startswith("em dashes added"):
            continue
        m = re.match(r"sentences kept (\d+)%", p)
        if m and int(m.group(1)) >= 85:
            continue
        out.append(p)
    return out


def main(apply: bool) -> None:
    done = set(DONE.read_text(encoding="utf-8").splitlines()) if DONE.exists() else set()
    entries, held, waiting = [], [], 0
    for line in LIST.read_text(encoding="utf-8").splitlines():
        live = ROOT / line
        draft = DRAFTS / live.name
        if line in done:
            continue
        if not draft.exists():
            waiting += 1
            continue
        probs = serious(check(live, draft))
        if probs:
            held.append((live.stem, probs))
            continue
        text = draft.read_text(encoding="utf-8")
        card, _, rest = text.partition("=== ADDITIONS ===")
        adds, _, doubts = rest.partition("=== DOUBTS ===")
        card = card.strip()
        if "\nprivate:" not in card.split("\n---", 1)[0]:
            card = "---\nprivate: true\n" + card[4:]
        m = re.search(r'(?m)^culture:\s*"?([^"\n]*)"?', card)
        culture = (m.group(1).split(",")[0].strip() if m else "") or "Unplaced"
        entries.append((culture, live, adds.strip(), doubts.strip()))
        if apply:
            live.write_text(card + "\n", encoding="utf-8")
    if apply and entries:
        REVIEW.parent.mkdir(parents=True, exist_ok=True)
        old = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else (
            '---\ntitle: "Card Update Review"\nprivate: true\n---\n\n# Card Update Review\n\n'
            "Every card re-cut to the R79-9 skeleton after the pilot: what was invented or derived "
            "(strike anything) and what the old card contradicts itself on. Grouped by culture.\n")
        add = []
        for culture in sorted({e[0] for e in entries}):
            add += [f"\n## {culture}\n"]
            for c, live, adds, doubts in entries:
                if c != culture:
                    continue
                rel = live.relative_to(ROOT / "wiki").with_suffix("").as_posix()
                add += [f"### [[{rel}|{live.stem}]]\n", "**Added or derived**\n", adds or "- nothing", "",
                        "**Doesn't add up on the old card**\n", doubts or "- nothing flagged", ""]
        REVIEW.write_text(old.rstrip("\n") + "\n" + "\n".join(add) + "\n", encoding="utf-8")
        with DONE.open("a", encoding="utf-8") as f:
            f.writelines(str(e[1].relative_to(ROOT)) + "\n" for e in entries)
    print(f"{'installed' if apply else 'would install'} {len(entries)} · held {len(held)} · not drafted yet {waiting}")
    for name, probs in held:
        print(f"  HELD {name}: " + " | ".join(probs))


if __name__ == "__main__":
    main("--apply" in sys.argv)
