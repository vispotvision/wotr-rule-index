#!/usr/bin/env python3
"""Diff every native Rust tool against the Python one over the real repo data.

  bash build/py.sh rust/parity.py [tool ...]     # all native tools by default; exit 1 on any mismatch

Each case calls mcp_server's function in-process and `wotr-mcp call` with the same arguments,
then compares the text exactly. The first mismatch per tool prints with a unified diff.
"""
import difflib
import json
import subprocess
import sys
from pathlib import Path

sys.argv, wanted = sys.argv[:1], sys.argv[1:]
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import mcp_server as M  # noqa: E402
import common  # noqa: E402

BIN = ROOT / "rust" / "target" / "release" / "wotr-mcp"
fn = lambda n: M.server._tool_manager._tools[n].fn  # noqa: E731


def rust(tool, args):
    r = subprocess.run([BIN, "call", tool, "-"], input=json.dumps(args), capture_output=True, text=True)
    return r.stdout[:-1] if r.returncode == 0 else f"<<rust error>> {r.stderr.strip()}"


def cases():
    vocab = sorted(common.load_vocab())
    ids = [r["id"] for r in common.load_rules()]
    yield "load_rules", {"tags": [], "brief": True}
    yield "load_rules", {"tags": []}
    yield "load_rules", {"tags": ["combat", "nonsense-tag"]}
    yield "load_rules", {"tags": [], "status": ["superseded"], "brief": True}
    for p in range(0, 6):
        yield "load_rules", {"tags": [], "brief": False, "part": p}
    for t in vocab:
        yield "load_rules", {"tags": [t]}
        yield "check_docket", {"tags": [t]}
    yield "check_docket", {"tags": []}
    for i in ids[::25] + ["R0-NOPE"]:
        yield "rule", {"id": i}
    yield "list_conflicts", {}
    yield "natalie_gpt", {}
    for s in ["", "gpt", "THE FIGHT", "tone", "Voice", "no such heading", "#"]:
        yield "natalie", {"section": s}
    skills = M._skills()
    yield "skill", {}
    for n in list(skills) + ["judger", "nope"]:
        yield "skill", {"name": n}
        root = M.SKILLS / n
        for p in sorted(root.rglob("*.md")) if root.is_dir() else []:
            yield "skill", {"name": n, "file": p.relative_to(root).as_posix()}
        yield "skill", {"name": n, "file": "../wotr-write/SKILL.md"}
    names = set()
    names |= {p.stem.split(" · ")[0].split(" — ")[0] for p in (M.WIKI / "Characters").rglob("*.md")}
    for n in sorted(names) + ["Moto", "Yoko", "zzz-nobody", "a"]:
        yield "character", {"name": n}
        yield "fow_line", {"name": n}
    scenes = sorted(p for p in (ROOT / "scenes").glob("*.md")) + sorted((ROOT / "lore/v1/scenes").glob("*.md")) \
        + sorted((ROOT / "desktop/style-bank").rglob("*.md"))
    for p in scenes:
        md = p.read_text(encoding="utf-8", errors="replace")
        yield "verify_scene", {"markdown": md}
        yield "verify_scene", {"markdown": md, "combat": True, "explicit": True, "turn": True}
        yield "verify_scene", {"markdown": md, "combat": True, "culture": "Moto"}
        yield "verify_scene", {"markdown": md, "combat": True, "school": "boxing"}


def main() -> int:
    bad, seen, total = {}, {}, 0
    for tool, args in cases():
        if wanted and tool not in wanted:
            continue
        total += 1
        seen[tool] = seen.get(tool, 0) + 1
        try:
            py = fn(tool)(**args)
        except Exception as e:  # noqa: BLE001
            py = f"<<python error>> {type(e).__name__}: {e}"
        rs = rust(tool, args)
        if py != rs:
            bad.setdefault(tool, []).append(args)
            if len(bad[tool]) == 1:
                shown = {k: (v[:60] + "...") if isinstance(v, str) and len(v) > 60 else v for k, v in args.items()}
                print(f"\n=== MISMATCH {tool} {shown}")
                print("".join(list(difflib.unified_diff(py.splitlines(True), rs.splitlines(True), "python", "rust", n=1))[:40]))
    for tool, n in seen.items():
        print(f"{tool:15} {n - len(bad.get(tool, [])):5}/{n} match")
    print(f"{total} cases, {sum(map(len, bad.values()))} mismatches")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
