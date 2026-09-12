#!/usr/bin/env python3
"""Walk the supersession graph and emit the resolved index.

Writes out/rules.resolved.json, out/rules.live.md, out/rules.live.full.md and out/docket.md.
Resolves nothing that the source text did not state. Where a rule is superseded
by something, that link came from a quotable line in a pack, not from an
assumption about pack ordering.
"""
import json
from collections import defaultdict

from common import OUT_DIR, load_rules, load_vocab


def main() -> int:
    rules = load_rules()
    by_id = {r["id"]: r for r in rules if "id" in r}

    superseded_by = defaultdict(list)
    for rule in rules:
        for target in rule.get("supersedes") or []:
            superseded_by[target].append(rule["id"])

    for rule in rules:
        rule["superseded_by"] = superseded_by.get(rule["id"], [])
        rule.pop("_file", None)

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "rules.resolved.json").write_text(
        json.dumps(sorted(rules, key=lambda r: (r.get("pack_number") or 0, r["id"])), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # live rules grouped by applies_to, which is how a scene loads them
    live = [r for r in rules if r.get("status") == "live"]
    grouped = defaultdict(list)
    for rule in live:
        for tag in rule.get("applies_to") or []:
            grouped[tag].append(rule)

    lines = ["# Live rules by domain", ""]
    lines.append(f"{len(live)} live of {len(rules)} extracted.")
    lines.append("")
    for tag in sorted(load_vocab()):
        hits = sorted(grouped.get(tag, []), key=lambda r: -(r.get("pack_number") or 0))
        if not hits:
            continue
        lines.append(f"## {tag} ({len(hits)})")
        lines.append("")
        for rule in hits:
            lines.append(f"- **{rule['id']}** [{rule['pack']} {rule['section']}] {rule['summary'].strip()}")
        lines.append("")
    (OUT_DIR / "rules.live.md").write_text("\n".join(lines), encoding="utf-8")

    # same grouping with the source quote under each rule, for a writing
    # session that has the file but not query.py (Claude Desktop project knowledge)
    full = ["# Live rules by domain, with source text", ""]
    full.append(
        f"{len(live)} live of {len(rules)} extracted. Newest pack first within each domain; "
        "the newer rule governs where two overlap."
    )
    full.append("")
    for tag in sorted(load_vocab()):
        hits = sorted(grouped.get(tag, []), key=lambda r: -(r.get("pack_number") or 0))
        if not hits:
            continue
        full.append(f"## {tag} ({len(hits)})")
        full.append("")
        for rule in hits:
            full.append(f"### {rule['id']} [{rule['pack']} {rule['section']}]")
            full.append("")
            full.append(rule["summary"].strip())
            full.append("")
            full.append(f"> {rule['verbatim'].strip()}")
            full.append("")
    (OUT_DIR / "rules.live.full.md").write_text("\n".join(full), encoding="utf-8")

    # the docket
    pending = sorted(
        [r for r in rules if r.get("status") in {"pending", "proposed"}],
        key=lambda r: (r.get("pack_number") or 0, r["id"]),
    )
    dock = ["# The Docket — open rulings", "", f"{len(pending)} outstanding.", ""]
    for rule in pending:
        dock.append(f"## {rule['id']} — {rule['title']}")
        dock.append("")
        dock.append(f"*{rule['pack']} {rule['section']}, blocks: {', '.join(rule.get('applies_to') or [])}*")
        dock.append("")
        dock.append(f"> {rule['verbatim'].strip()}")
        dock.append("")
        if rule.get("notes"):
            dock.append(rule["notes"].strip())
            dock.append("")
    (OUT_DIR / "docket.md").write_text("\n".join(dock), encoding="utf-8")

    orphans = [t for t in superseded_by if t not in by_id]
    print(f"resolved {len(rules)} rules -> out/")
    print(f"  live={len(live)} pending={len(pending)}")
    if orphans:
        print(f"  WARN unknown supersession targets: {', '.join(sorted(orphans))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
