#!/usr/bin/env python3
"""Load the rules a given task needs. This is what the n8n context step calls.

  python build/query.py --applies-to combat adjudication
  python build/query.py --applies-to dialogue --format brief
  python build/query.py --status pending
  python build/query.py --id R15-2-ONE_TEST --format full
"""
import argparse
import json

from common import load_rules


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--applies-to", nargs="*", default=[], help="any of these tags")
    ap.add_argument("--status", nargs="*", default=["live"])
    ap.add_argument("--pack", type=int, default=None)
    ap.add_argument("--id", default=None)
    ap.add_argument("--format", choices=["brief", "full", "json"], default="brief")
    args = ap.parse_args()

    rules = load_rules()
    if args.id:
        rules = [r for r in rules if r.get("id") == args.id]
    else:
        if args.status:
            rules = [r for r in rules if r.get("status") in set(args.status)]
        if args.applies_to:
            want = set(args.applies_to)
            rules = [r for r in rules if want & set(r.get("applies_to") or [])]
        if args.pack is not None:
            rules = [r for r in rules if r.get("pack_number") == args.pack]

    # newest pack first: later beats earlier, so the writer reads the governing
    # rule before the one it amended
    rules.sort(key=lambda r: (-(r.get("pack_number") or 0), r.get("id", "")))

    if args.format == "json":
        print(json.dumps([{k: v for k, v in r.items() if not k.startswith("_")} for r in rules], indent=2, ensure_ascii=False))
        return 0

    for rule in rules:
        print(f"{rule['id']}  [{rule['pack']} {rule['section']}]  {rule['status']}")
        print(f"  {rule['summary'].strip()}")
        if args.format == "full":
            print(f"  > {rule['verbatim'].strip()}")
            if rule.get("amends"):
                for a in rule["amends"]:
                    print(f"  amends: {a.get('guide')} {a.get('locus') or ''} ({a.get('operation') or '?'})")
            if rule.get("supersedes"):
                print(f"  supersedes: {', '.join(rule['supersedes'])}")
        print()

    print(f"-- {len(rules)} rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
