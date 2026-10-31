#!/usr/bin/env python3
"""Check converted cards against their originals.

  python imports/drafts/card-update/check.py <draft dir> <list file>

Per card: head lines present, output delimiters present, how much of the original
survives (sentences of 8+ words found verbatim, every number, every short bold label),
and the em-dash count (new text must add none). Prints what is missing.
"""
import re
import sys
from pathlib import Path

HEAD = ["**Stat line**", "**Combat grammar**", "**Aura and sound**", "**Traits**", "**Voice**"]


def body(t: str) -> str:
    return re.sub(r"(?s)^---\n.*?\n---\n", "", t)


def norm(s: str) -> str:
    return re.sub(r"[\s*_>#|]+", " ", s).strip().lower()


def check(orig: Path, draft: Path) -> list[str]:
    o, d = body(orig.read_text(encoding="utf-8")), draft.read_text(encoding="utf-8")
    probs = []
    if "=== ADDITIONS ===" not in d:
        probs.append("no ADDITIONS block")
    card = d.split("=== ADDITIONS ===")[0]
    if not card.startswith("---\n"):
        probs.append("does not start with frontmatter")
    probs += [f"head missing {h}" for h in HEAD if h not in card]
    nd = norm(card)
    sents = [s for s in re.split(r"(?<=[.!?])\s+|\n", o) if len(s.split()) >= 8]
    lost = [s.strip() for s in sents if norm(s) not in nd]
    if sents and len(lost) / len(sents) > 0.10:
        probs.append(f"sentences kept {100 - 100 * len(lost) // len(sents)}% ({len(lost)} of {len(sents)} not verbatim)")
    nums = set(re.findall(r"\d[\d,.]*\d|\d", o)) - set(re.findall(r"\d[\d,.]*\d|\d", card))
    if nums:
        probs.append("numbers gone: " + ", ".join(sorted(nums)[:15]))
    labels = {m.strip() for m in re.findall(r"\*\*([^*\n]{3,40})\*\*", o)}
    gone = [l for l in labels if norm(l) not in nd]
    if gone:
        probs.append("bold labels gone: " + "; ".join(sorted(gone)[:12]))
    if card.count("—") > o.count("—"):
        probs.append(f"em dashes added: {card.count('—') - o.count('—')}")
    return probs


if __name__ == "__main__":
    out, lst = Path(sys.argv[1]), Path(sys.argv[2])
    for line in lst.read_text(encoding="utf-8").splitlines():
        orig = Path(line)
        draft = out / orig.name
        if not draft.exists():
            print(f"-- {orig.stem}: no draft yet")
            continue
        probs = check(orig, draft)
        print(f"{'OK' if not probs else '!!'} {orig.stem}")
        for p in probs:
            print("    " + p)
