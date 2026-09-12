#!/usr/bin/env python3
"""Integrity gate. Must exit 0 before a pack counts as done.

Fix the data, not the checker.
"""
import re
import sys
from collections import Counter

from common import SOURCES_DIR, load_rules, load_schema, load_vocab, normalise

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("jsonschema missing. run: pip install pyyaml jsonschema")

STATUSES = {"live", "superseded", "repealed", "pending", "proposed"}


def main() -> int:
    rules = load_rules()
    if not rules:
        print("no rules found in rules/ — nothing to validate")
        return 1

    vocab = load_vocab()
    validator = Draft7Validator(load_schema())
    by_id = {}
    failures = []
    source_cache = {}

    def fail(rule, msg):
        failures.append(f"{rule.get('_file','?')} :: {rule.get('id','<no id>')} :: {msg}")

    for rule in rules:
        payload = {k: v for k, v in rule.items() if not k.startswith("_")}

        for err in validator.iter_errors(payload):
            path = ".".join(str(p) for p in err.path) or "<root>"
            fail(rule, f"schema: {path}: {err.message}")

        rid = rule.get("id")
        if rid:
            by_id.setdefault(rid, []).append(rule)

        for tag in rule.get("applies_to") or []:
            if tag not in vocab:
                fail(rule, f"applies_to tag '{tag}' is not in schema/applies_to.md")

        # verbatim must actually exist in the source file
        src = (rule.get("source") or {}).get("file")
        if src and rule.get("verbatim"):
            path = SOURCES_DIR / src
            if not path.exists():
                fail(rule, f"source file missing: sources/{src}")
            else:
                if src not in source_cache:
                    source_cache[src] = normalise(path.read_text(encoding="utf-8"))
                if normalise(rule["verbatim"]) not in source_cache[src]:
                    fail(rule, "verbatim quote not found in source (paraphrase or drift)")

    # ids unique
    for rid, hits in by_id.items():
        if len(hits) > 1:
            files = ", ".join(h["_file"] for h in hits)
            failures.append(f"duplicate id {rid} in {files}")

    # supersedes targets must exist, and a superseded rule must not claim to be live
    for rule in rules:
        for target in rule.get("supersedes") or []:
            if target not in by_id:
                fail(rule, f"supersedes unknown rule id '{target}'")
                continue
            if rule.get("status") == "live":
                for victim in by_id[target]:
                    if victim.get("status") == "live":
                        failures.append(
                            f"contradiction: {victim['id']} is live but superseded by live {rule['id']}"
                        )

    # open rulings carry an R-code and are never live. Once Isaac answers one it
    # is marked superseded (the ruling quoted in `ratified`, the answer in
    # `notes`); it never becomes a live rule itself.
    for rule in rules:
        if rule.get("kind") == "open_ruling":
            if not re.match(r"^R\d{1,2}-[A-Z]$", rule.get("id", "")):
                fail(rule, "open_ruling id must look like R15-A")
            if rule.get("status") not in {"pending", "proposed", "superseded"}:
                fail(rule, "open_ruling must be pending, proposed or superseded (ruled), not live")
            if rule.get("status") == "superseded" and not rule.get("ratified"):
                fail(rule, "a ruled open_ruling must carry the ruling in `ratified`")

    counts = Counter(r.get("status") for r in rules)
    print(f"{len(rules)} rules across {len({r['_file'] for r in rules})} files")
    print("  " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda x: str(x[0]))))

    if failures:
        print(f"\nFAIL ({len(failures)})")
        for line in failures:
            print("  " + line)
        return 1

    print("\nPASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
