#!/usr/bin/env python3
"""timeline, reconcile and pack_impact (they write reports/ and scenes/TIMELINE.md), Rust against
Python, in writer_parity.py's two scratch clones.

  bash build/py.sh rust/audit_parity.py [scratch-dir]     # exit 1 on any difference
"""
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import writer_parity as W  # noqa: E402  (reads the scratch dir from argv)

WRITTEN = ["reports", "scenes/TIMELINE.md"]


def calls(root: Path) -> list[tuple[str, dict]]:
    rules = sorted((root / "sources").glob("*.md"))
    packs = [p.read_text(encoding="utf-8", errors="replace") for p in rules[::7]]
    return ([("timeline", {}), ("reconcile", {})]
            + [("pack_impact", {"markdown": t, "name": f"Pack {i}: test!"}) for i, t in enumerate(packs)]
            + [("pack_impact", {"markdown": "", "name": ""}), ("pack_impact", {"markdown": "short words only"})])


def tree(root: Path) -> dict[str, str]:
    files = {}
    for w in WRITTEN:
        base = root / w
        for p in ([base] if base.is_file() else sorted(base.rglob("*")) if base.exists() else []):
            if p.is_file():
                files[p.relative_to(root).as_posix()] = p.read_text(encoding="utf-8", errors="replace")
    return files


def plant(root: Path) -> None:
    """Findings for reconcile's two pattern checks: a scene with a carded name at the wrong Stage and
    Level, and a manifest page naming a Wellspring with another Family."""
    import json
    import re
    m = json.loads((root / "wiki/.manifest.json").read_text(encoding="utf-8"))
    cards = [v for v in m.values() if "Character Cards" in v["rel"] and (root / "wiki" / v["rel"]).exists()]
    lines = []
    for v in cards[:40]:
        first = re.split(r"\s+[·—]\s+", v["title"])[0].split()[0]
        lines.append(f"{first} stood there at Stage XIV and Level 999 that day. {first}, Stage I.")
    (root / "scenes/zz_parity_probe.md").write_text("# Probe\n\n*the probe hour, years after the fall*\n\n" + "\n\n".join(lines) + "\n", encoding="utf-8")
    fam_dir = root / "wiki/The Magic System/The Eight Families & the Sixty Wellsprings"  # gone from the wiki; planted
    fam_dir.mkdir(parents=True, exist_ok=True)
    (fam_dir / "Ignara — the Fire Family.md").write_text("### Pyreveil · heat\n\n### **Cymorath** · x\n", encoding="utf-8")
    (fam_dir / "Glacira — Frost.md").write_text("---\nt: 1\n---\n### Exuroth · cold\n### Pyreveil · again\n", encoding="utf-8")
    probe = "**Pyreveil** · Glacira and **Pyreveil** · Ignara, **Cymorath**·Glacira, **Exuroth** · Ignara, **Exuroth** · Nobody"
    page = root / "wiki" / next(v["rel"] for v in m.values() if (root / "wiki" / v["rel"]).exists())
    page.write_text(page.read_text(encoding="utf-8") + "\n\n" + probe + "\n", encoding="utf-8")


def main() -> int:
    a, b = W.setup()
    bad = 0
    for rnd in range(3):
        if rnd:  # later rounds build the timeline skeleton from scratch
            for r in (a, b):
                (r / "scenes/TIMELINE.md").unlink(missing_ok=True)
        if rnd == 2:
            plant(a), plant(b)
        cs = calls(a) if rnd != 1 else [("timeline", {})]
        py, rs = W.run_python(a, cs), W.run_rust(b, cs)
        for (tool, args), p, r in zip(cs, py, rs):
            if p != r:
                bad += 1
                print(f"=== reply differs: {tool} {str(args)[:80]}")
                print("".join(list(difflib.unified_diff(p.splitlines(True), r.splitlines(True), "python", "rust", n=1))[:30]))
        ta, tb = tree(a), tree(b)
        for f in sorted(set(ta) | set(tb)):
            if ta.get(f) != tb.get(f):
                bad += 1
                print(f"=== file differs: {f}")
                print("".join(list(difflib.unified_diff(ta.get(f, "").splitlines(True), tb.get(f, "").splitlines(True), "python", "rust", n=1))[:30]))
        print(f"round {rnd + 1}: {len(cs)} calls, {len(ta)} files compared")
    print("ALL IDENTICAL" if not bad else f"{bad} difference(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
