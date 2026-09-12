#!/usr/bin/env python3
"""Voice fingerprints: what each named character's dialogue actually does across
the scene archive, so a swapped line can be caught by measurement.

  python build/voices.py            -> table/voices.yaml, reports/voice_fingerprints_<date>.md
  python build/voices.py check "<name>" "<line of dialogue>"   -> how far the line sits from the fingerprint

Attribution is heuristic: a quoted span is credited to a name that appears in a
speech tag within forty characters ("..." Lambert said / said Lambert / Lambert:)
or, failing that, to the last name mentioned in the paragraph before the quote.
Characters with fewer than eight attributed lines are not fingerprinted.
"""
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCENES = ROOT / "scenes"
TABLE = ROOT / "table"
SKIP = {"MANIFEST.md", "CAST.md", "ARCS.md", "TIMELINE.md", "00_SUPERSEDED_wrong_names.md", "THE_KINGDOM_OF_KHARVEN_buri.md", "WOTR_AI_Writing_Tells_to_Avoid.md"}
QUOTE = re.compile(r"[\"“]([^\"“”]{3,400})[\"”]")
TAG = re.compile(r"(?:[\"”]\s*,?\s*(?:said|asked|answered|replied|murmured|called|went on|added|breathed)\s+([A-Z][\w'’-]+(?:\s+[A-Z][\w'’-]+)?))|(?:([A-Z][\w'’-]+(?:\s+[A-Z][\w'’-]+)?)\s+(?:said|asked|answered|replied|murmured|called|went on|added|breathed)\s*[,:]?\s*[\"“])")
NAME = re.compile(r"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?)\b")
CONTRACTION = re.compile(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", re.I)


def cast_names() -> set[str]:
    cast = SCENES / "CAST.md"
    names = set()
    if cast.exists():
        names = set(re.findall(r"(?m)^## (.+?) \(", cast.read_text(encoding="utf-8")))
    return names


def _read(p: Path) -> str:
    t = p.read_text(encoding="utf-8", errors="replace")
    if t.startswith("---\n"):
        end = t.find("\n---\n", 4)
        if end != -1:
            t = t[end + 5:]
    return t


def attribute(text: str, known: set[str]) -> list[tuple[str, str]]:
    """(speaker, line) pairs."""
    first_to_full = {n.split()[0]: n for n in known}
    out = []
    for para in re.split(r"\n\s*\n", text):
        last_name = None
        pos = 0
        for m in QUOTE.finditer(para):
            line = m.group(1).strip()
            before = para[max(0, m.start() - 80):m.start()]
            after = para[m.end():m.end() + 80]
            spk = None
            t = TAG.search(after[:60]) or TAG.search(before[-60:])
            if t:
                spk = t.group(1) or t.group(2)
            if not spk:
                names = [n for n in NAME.findall(para[pos:m.start()]) if n.split()[0] in first_to_full]
                if names:
                    last_name = names[-1]
                spk = last_name
            if spk:
                spk = first_to_full.get(spk.split()[0], spk)
                if spk in known:
                    out.append((spk, line))
            pos = m.end()
    return out


def fingerprint(lines: list[str]) -> dict:
    wc = [len(l.split()) for l in lines]
    words = [w.lower() for l in lines for w in re.findall(r"[A-Za-z']+", l)]
    return {
        "lines": len(lines),
        "mean_words": round(statistics.mean(wc), 1),
        "sd_words": round(statistics.pstdev(wc), 1) if len(wc) > 1 else 0.0,
        "short_share": round(sum(1 for w in wc if w <= 4) / len(wc), 2),
        "question_rate": round(sum(1 for l in lines if "?" in l) / len(lines), 2),
        "contraction_rate": round(sum(1 for l in lines if CONTRACTION.search(l)) / len(lines), 2),
        "first_person_rate": round(sum(1 for l in lines if re.search(r"\b(I|I'm|I've|my|me)\b", l)) / len(lines), 2),
        "imperative_rate": round(sum(1 for l in lines if re.match(r"^(?:Do|Don't|Stop|Go|Come|Tell|Bring|Leave|Sit|Stand|Look|Listen|Wait|Take|Put|Give)\b", l)) / len(lines), 2),
        "favourite_words": [w for w, _ in Counter(w for w in words if len(w) > 3 and w not in STOP).most_common(8)],
    }


STOP = set("that this with have from they were what when there your will would could about into then them than been said were which their there here just only over very".split())


def build() -> tuple[dict, Path]:
    known = cast_names()
    by = defaultdict(list)
    for p in sorted(SCENES.glob("*.md")):
        if p.name in SKIP:
            continue
        for spk, line in attribute(_read(p), known):
            by[spk].append(line)
    fps = {n: fingerprint(ls) for n, ls in by.items() if len(ls) >= 8}
    TABLE.mkdir(exist_ok=True)
    (TABLE / "voices.yaml").write_text(yaml.safe_dump(fps, allow_unicode=True, sort_keys=True, width=100), encoding="utf-8", newline="\n")
    rep = ROOT / "reports" / f"voice_fingerprints_{date.today().isoformat()}.md"
    rep.parent.mkdir(exist_ok=True)
    lines = ["# Voice fingerprints", "", f"{len(fps)} characters with eight or more attributed lines (heuristic attribution; treat as measurement, not verdict). Rule: if two characters' lines could be swapped and nobody noticed, the scene failed (R15-1-VOICE_DIFFERENTIATION).", "",
             "| character | lines | mean words | short share | questions | contractions | first person | imperatives | favourite words |", "|---|---|---|---|---|---|---|---|---|"]
    for n, f in sorted(fps.items(), key=lambda kv: -kv[1]["lines"]):
        lines.append(f"| {n} | {f['lines']} | {f['mean_words']} ±{f['sd_words']} | {f['short_share']} | {f['question_rate']} | {f['contraction_rate']} | {f['first_person_rate']} | {f['imperative_rate']} | {', '.join(f['favourite_words'][:6])} |")
    # nearest neighbours: who could be swapped
    lines += ["", "## Closest pairs (most swappable by the numbers)", ""]
    keys = ["mean_words", "short_share", "question_rate", "contraction_rate", "first_person_rate", "imperative_rate"]
    names = list(fps)
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = fps[names[i]], fps[names[j]]
            d = sum(((a[k] - b[k]) / (10 if k == "mean_words" else 1)) ** 2 for k in keys) ** 0.5
            pairs.append((d, names[i], names[j]))
    pairs.sort()
    lines += [f"- {a} / {b} (distance {d:.2f})" for d, a, b in pairs[:8]]
    rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return fps, rep


def check(name: str, line: str) -> str:
    fps = yaml.safe_load((TABLE / "voices.yaml").read_text(encoding="utf-8")) if (TABLE / "voices.yaml").exists() else {}
    f = fps.get(name) or next((v for k, v in fps.items() if name.lower() in k.lower()), None)
    if not f:
        return f"no fingerprint for {name} (fewer than eight attributed lines in the archive)"
    wc = len(line.split())
    z = (wc - f["mean_words"]) / max(f["sd_words"], 1)
    notes = [f"{name}: {f['lines']} lines, mean {f['mean_words']} words (this line: {wc}, z={z:+.1f})"]
    if abs(z) > 2:
        notes.append("length is far outside this voice")
    if "?" in line and f["question_rate"] < 0.1:
        notes.append("a question from a voice that almost never asks")
    if CONTRACTION.search(line) and f["contraction_rate"] < 0.15:
        notes.append("a contraction from a voice that does not contract")
    if not CONTRACTION.search(line) and f["contraction_rate"] > 0.6 and wc > 6:
        notes.append("no contraction from a voice that always contracts")
    # who does it sound like instead
    best = None
    for k, v in fps.items():
        if k == name:
            continue
        zz = abs((wc - v["mean_words"]) / max(v["sd_words"], 1))
        if best is None or zz < best[0]:
            best = (zz, k)
    if best and abs(z) > 1.5 and best[0] < 1:
        notes.append(f"by length alone it reads more like {best[1]}")
    return "; ".join(notes)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 2 and sys.argv[1] == "check":
        print(check(sys.argv[2], sys.argv[3]))
        return 0
    fps, rep = build()
    print(f"{len(fps)} fingerprints -> {rep}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
