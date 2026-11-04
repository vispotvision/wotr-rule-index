#!/usr/bin/env python3
"""Rust's PyYAML emitter (rust/src/pyyaml.rs) against PyYAML itself.

  bash build/py.sh rust/yaml_parity.py      # exit 1 on any difference

Dumps the table files and a few thousand awkward values (every wiki and scene paragraph, YAML
look-alikes, quotes, control and astral characters, lines long enough to fold, long keys) with
yaml.safe_dump(allow_unicode=True, sort_keys=False, width=100) and with `wotr-mcp yaml-dump`.
"""
import glob
import json
import random
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "rust" / "target" / "release" / "wotr-mcp"


def py(v):
    return yaml.safe_dump(v, allow_unicode=True, sort_keys=False, width=100)


def rs(v):
    return subprocess.run([BIN, "yaml-dump"], input=json.dumps(v), capture_output=True, text=True).stdout


def values():
    out = ["", " ", "yes", "No", "on", "OFF", "true", "null", "~", "Null", "1", "-1", "+1", "0x1F", "0o7", "017", "1_000",
           "1:30", "1.5", "1e3", "1.0e+3", ".5", ".inf", "-.Inf", ".NaN", "2026-11-04", "2026-11-04 10:00:00", "2026-1-4T1:00:00Z",
           "<<", "=", "!", "&", "*", "- x", "-x", "-", "? q", "?q", ": v", "a: b", "a:b", "a #b", "a#b", "#x", "x #", "[a]", "{a}", "a, b",
           "it's", "'quoted'", '"dq"', "\\back", "%x", "@x", "`x", "|x", ">x", "...", "---", "--- x", "...x",
           " lead", "trail ", "two  spaces", "tab\there", "line\nbreak", "\nlead break", "trail break\n", "a \nb", "a\n b",
           "a\n\nb", "a\r\nb", "nel\x85x", "ls x", "nbsp\xa0x", "bom﻿x", "ctrl\x01x", "esc\x1bx", "del\x7fx",
           "emoji 🐉 here", "ā ē ō Kōkan", "—em", "“curly”", "x" * 150, ("word " * 60).strip(), ("w" * 99 + " ") * 3,
           ("a " * 120), "'" * 5, ("it's a " * 30), ("tab\t" * 40), ("'x' " * 40), ("é" * 120 + " z"), "\\" * 3, "\x00"]
    for f in sorted(glob.glob(str(ROOT / "wiki/**/*.md"), recursive=True))[::4] + sorted(glob.glob(str(ROOT / "scenes/*.md"))):
        t = Path(f).read_text(encoding="utf-8", errors="replace")
        out += [p.strip() for p in t.split("\n\n") if p.strip()][:40]
        out += [ln for ln in t.splitlines() if ln][:40]
    rnd = random.Random(7)
    alphabet = list("ab :#-'\"\\\n\t,?[]{}&*!|>%@`") + ["é", "—", "🐉", "\x85", " ", "\xa0", "\x07"]
    out += ["".join(rnd.choice(alphabet) for _ in range(rnd.randint(1, 60))) for _ in range(3000)]
    return out


def main() -> int:
    bad = 0
    for f in sorted(glob.glob(str(ROOT / "table/*.yaml"))):
        data = yaml.safe_load(Path(f).read_text(encoding="utf-8"))
        same = rs(data) == Path(f).read_text(encoding="utf-8")
        bad += not same
        print(f"{Path(f).name:16} {'identical' if same else 'DIFFERS'}")
    vals = values()
    rows = [{"text": v, "list": [v, {"k": v}], "nested": {"deep": [v]}} for v in vals]
    rows += [{v[:200] or "empty": 1} for v in vals[:400] if "\n" not in v]  # values as keys, long ones taking '?'
    rows += [{"k" * n: "v"} for n in (120, 122, 123, 124, 127, 130)]
    rows += [[], {}, [[]], [{}], {"a": []}, {"a": {}}, [1, 2.5, None, True, False, 1e17, 1e-05, -0.0, 3.14159, 123456789012]]
    for chunk in range(0, len(rows), 500):
        part = rows[chunk:chunk + 500]
        if py(part) == rs(part):
            continue
        for r in part:  # find the culprits
            if py([r]) != rs([r]):
                bad += 1
                if bad <= 8:
                    print("DIFF for", repr(r)[:160], "\n  python:", repr(py([r]))[:300], "\n  rust:  ", repr(rs([r]))[:300])
    print(f"{len(rows)} rows of awkward values: {'all identical' if not bad else f'{bad} differ'}")
    # and back: what PyYAML wrote must read as the same values in Rust (YAML 1.1 vs 1.2 typing)
    misread = 0
    for chunk in range(0, len(rows), 500):
        text = py(rows[chunk:chunk + 500])
        got = json.loads(subprocess.run([BIN, "yaml-load"], input=text, capture_output=True, text=True).stdout or "null")
        if got != json.loads(json.dumps(yaml.safe_load(text))):
            for r in rows[chunk:chunk + 500]:
                t = py([r])
                g = json.loads(subprocess.run([BIN, "yaml-load"], input=t, capture_output=True, text=True).stdout or "null")
                if g != json.loads(json.dumps(yaml.safe_load(t))):
                    misread += 1
                    if misread <= 8:
                        print("MISREAD", repr(t)[:200], "->", repr(g)[:120])
    print(f"read back: {'all identical' if not misread else f'{misread} rows misread'}")
    bad += misread
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
