#!/usr/bin/env python3
"""The Rust writers against the Python ones, in two scratch clones that push to scratch remotes.

  bash build/py.sh rust/writer_parity.py [scratch-dir]     # exit 1 on any difference

Clone A runs every call through build/mcp_worker.py (Python), clone B through `wotr-mcp call`
(Rust, WOTR_ROOT=B). Each pushes to its own bare repository, so nothing reaches GitHub or the real
checkout. Compared: every reply, every file under the written paths, and the commit messages.
Times, stamps and uuids are normalized; everything else must match byte for byte.
"""
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REAL = Path(__file__).resolve().parent.parent
BIN = REAL / "rust" / "target" / "release" / "wotr-mcp"
S = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wotr-writer-parity").resolve()
WRITTEN = ["table", "scenes", "wiki", "RULINGS.md", "proposals", "inbox"]
NORM = [(re.compile(r"\d{8}_\d{4}"), "<STAMP>"), (re.compile(r"\d{8}-\d{6}"), "<STAMP>"),
        (re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"), "<UUID>"),
        (re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d"), "<NOW>")]


def norm(t: str) -> str:
    for rx, rep in NORM:
        t = rx.sub(rep, t)
    return t


def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True)


def setup() -> tuple[Path, Path]:
    if S.exists():
        shutil.rmtree(S)
    S.mkdir(parents=True)
    head = sh("git", "rev-parse", "HEAD", cwd=REAL).stdout.strip()
    out = []
    for side in "AB":
        bare = S / f"origin{side}.git"
        sh("git", "clone", "-q", "--bare", "--no-hardlinks", str(REAL), str(bare))
        work = S / side
        sh("git", "clone", "-q", str(bare), str(work))
        sh("git", "checkout", "-q", head, cwd=work)
        sh("git", "checkout", "-q", "-B", "master", cwd=work)
        out.append(work)
    return out[0], out[1]


def script(root: Path) -> list[tuple[str, dict]]:
    card = next((p for p in sorted((root / "wiki/Characters/Volume I — Character Cards").glob("*.md"))), None)
    card_name = json.loads((root / "wiki/.manifest.json").read_text())  # a real card title from the manifest
    titled = [v["title"] for v in card_name.values() if "Character Cards/" in v.get("rel", "")]
    existing = titled[0] if titled else (card.stem if card else "nobody")
    long = ("The tithe-collector came down the switchback road with two pikemen and a ledger bound in sealskin, "
            "and the village paid what it owed: salt fish, a lamb, and a promise it could not keep — 'next thaw'. ") * 2
    th = "parity-thread"
    return [
        ("add_front", {"name": "The Salt Tithe: Northern Collectors", "thread": th, "want": "every village pays by thaw",
                       "ticks": ["A collector arrives", "A boat is seized", "A headman is flogged", "The fishing fleet is impounded"], "pace_days": 7}),
        ("add_front", {"name": "Quiet Front", "thread": th, "want": "nothing yet", "ticks": ["one", "two", "three", "four"]}),
        ("set_front_clock", {"front_id": "quiet-front", "ticks": ["a", "b", "c", "d", "e"], "pace_days": 3}),
        ("set_front_clock", {"front_id": "no-such-front", "pace_days": 2}),
        ("advance_front", {"front_id": "the-salt-tithe-northern-collectors", "what_happened": "A collector came", "next_move": "They take the boat 'Gull'"}),
        ("advance_front", {"front_id": "missing", "what_happened": "x"}),
        ("pass_time", {"thread": th, "days": 10}),
        ("pass_time", {"thread": th, "story_date": "715-3-14"}),
        ("pass_time", {"thread": th, "days": 9}),
        ("pass_time", {"thread": th, "story_date": "715-14-2"}),
        ("pass_time", {"thread": th, "days": -1}),
        ("ledger_add", {"category": "debts", "who": "Hild", "text": long, "thread": th, "due_date": "715-4-1"}),
        ("ledger_add", {"category": "bond", "who": "Borin", "text": "Owes him a drink: \"two, actually\"", "thread": th}),
        ("ledger_add", {"category": "projects", "who": "Isaac's PC", "text": "Rebuild the forge", "thread": th, "ticks": 5}),
        ("ledger_add", {"category": "project", "who": "x", "text": "bad clock", "thread": th, "ticks": 2}),
        ("ledger_add", {"category": "heat", "who": "the Guild", "text": "Watched", "thread": th, "level": "warm"}),
        ("ledger_add", {"category": "heat", "who": "the Guild", "text": "again", "thread": th}),
        ("ledger_add", {"category": "debts", "who": "x", "text": "bad date", "due_date": "715-3-40"}),
        ("ledger_add", {"category": "who knows what", "who": "Yoko", "text": "Knows the name: Kōkan — and why", "due_condition": "she is asked", "due_after_sessions": 2}),
        ("ledger_add", {"category": "renown", "who": "public", "text": "yes"}),
        ("ledger_mark", {"entry_id": "L999", "fed": "x"}),
        ("fire_trigger", {"trigger": "she is asked", "thread": th}),
        ("fire_trigger", {"trigger": "nothing waits on this"}),
        ("npc_set", {"name": "Mother Ashby", "thread": th, "want": "her son home", "knows": ["the pass", "the toll: 3 silver"], "voice": "flat, Kharven"}),
        ("npc_set", {"name": "mother ashby", "thread": th, "lie": "he left freely", "tell": "she wipes her hands", "knows": []}),
        ("archive_scene", {"title": "Parity: The Salt Road", "markdown": "The road was **salt** and frost.\n\nIt went on.", "author_notes": "notes: invented the toll"}),
        ("archive_scene", {"title": "Parity: The Salt Road", "markdown": "# Own Heading\n\nSecond copy."}),
        ("wiki_write", {"path": "The Table — Running Pieces/Parity Page.md", "markdown": "# Parity Page\n\nBody: one."}),
        ("wiki_write", {"path": "The Table — Running Pieces/Parity Page.md", "markdown": "Body two, no frontmatter."}),
        ("wiki_write", {"path": "../escape.md", "markdown": "x"}),
        ("wiki_write", {"path": ".obsidian/x.md", "markdown": "x"}),
        ("wiki_write", {"path": "notes.txt", "markdown": "x"}),
        ("log_ruling", {"rule_id": "R81-1-FAST_TRADES_FULL_CARD", "ruling": "  Parity check ruling.  ", "context": "the writer port"}),
        ("log_ruling", {"rule_id": "new", "ruling": "Second."}),
        ("propose_rule", {"title": "Parity proposal", "rule_text": "Every port is replayed.", "applies_to": ["verification", "no-such-tag"], "rationale": "trust", "session": "s1"}),
        ("create_character", {"name": "Parity Testman", "markdown": "**Age:** 30\n\nA test card."}),
        ("create_character", {"name": "Parity Testman", "markdown": "dup"}),
        ("create_character", {"name": "Other", "markdown": "x", "volume": "No Such Volume"}),
        ("update_character", {"name": "Parity Testman", "markdown": "# Parity Testman\n\nUpdated body, longer now."}),
        ("update_character", {"name": "Zzz Nobody Qq", "markdown": "x"}),
        ("handoff", {"kind": "research", "title": "Salt: how it's taxed", "body": "Sources: none.", "thread": th}),
        ("handoff", {"kind": "canon", "title": "x", "body": "y"}),
        ("inbox", {"full": False}),
        ("session_end", {"thread": th, "days": 7, "fired": ["she is asked", "never"],
                         "ledger": [{"category": "injuries and reserve", "who": "PC", "text": "A cracked rib that stays"},
                                    {"category": "projects", "who": "PC", "text": "bad", "ticks": 1}, {"who": "no category"}],
                         "fronts": [{"front_id": "quiet-front", "what_happened": "Nothing, loudly", "next_move": "b again"}, {"front_id": "gone", "what_happened": "x"}],
                         "npcs": [{"name": "Mother Ashby", "doing_now": "waiting at the gate", "stands_with": "owed"}, {"name": "New Face", "want": "coin"}],
                         "cards": [{"name": "Parity Testman", "markdown": "Card after the scene."}, {"name": "Zzz Nobody Qq", "markdown": "x"}],
                         "rulings": ["the toll stands"], "notes": "a long day", "title": "Parity: After the Toll", "scene_markdown": "They paid.", "author_notes": "end"}),
        ("ledger_mark", {"entry_id": "L001", "level": "hot", "how": "the raid"}),
        ("ledger_collect", {"entry_id": "L001", "how": "paid in salt"}),
        ("ledger_collect", {"entry_id": "L777", "how": "x"}),
    ] + ([("update_character", {"name": existing, "markdown": f"# {existing}\n\nReplaced in the parity clone only."})] if existing else [])


def ledger_ids(root: Path) -> list[str]:
    import yaml
    p = root / "table/ledger.yaml"
    return [r["id"] for r in (yaml.safe_load(p.read_text()) or [])] if p.exists() else []


def run_python(root: Path, calls) -> list[str]:
    w = subprocess.Popen(["bash", str(root / "build/py.sh"), str(root / "build/mcp_worker.py")], cwd=root,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    out = []
    for tool, args in calls:
        w.stdin.write(json.dumps({"tool": tool, "args": args}) + "\n")
        w.stdin.flush()
        r = json.loads(w.stdout.readline())
        out.append(r.get("ok", f"<<error>> {r.get('err')}"))
    w.stdin.close()
    w.wait(30)
    return out


def run_rust(root: Path, calls) -> list[str]:
    out = []
    for tool, args in calls:
        r = subprocess.run([str(BIN), "call", tool, "-"], input=json.dumps(args), capture_output=True, text=True,
                           env={**os.environ, "WOTR_ROOT": str(root)})
        out.append(r.stdout[:-1] if r.returncode == 0 else f"<<error>> {r.stderr.strip()}")
    return out


def tree(root: Path) -> dict[str, str]:
    files = {}
    for w in WRITTEN:
        base = root / w
        for p in ([base] if base.is_file() else sorted(base.rglob("*")) if base.exists() else []):
            if p.is_file():
                files[norm(p.relative_to(root).as_posix())] = norm(p.read_text(encoding="utf-8", errors="replace"))
    return files


def main() -> int:
    a, b = setup()
    base = sh("git", "rev-parse", "HEAD", cwd=a).stdout.strip()
    # the bond/project lines' ids depend on what the ledger already holds; both clones start equal
    calls = script(a)
    ids = ledger_ids(a)
    nxt = max([int(i[1:]) for i in ids] + [0])
    calls += [("ledger_mark", {"entry_id": f"L{nxt + 2:03d}", "fed": "a shared meal", "strained": "the lie"}),
              ("ledger_mark", {"entry_id": f"L{nxt + 3:03d}", "tick": 3, "how": "bellows"}),
              ("ledger_mark", {"entry_id": f"L{nxt + 3:03d}", "tick": 10}),
              ("ledger_mark", {"entry_id": f"L{nxt + 1:03d}", "tick": 1}),
              ("inbox", {})]
    py = run_python(a, calls)
    rs = run_rust(b, calls)
    bad = 0
    for (tool, args), p, r in zip(calls, py, rs):
        if norm(p) != norm(r):
            bad += 1
            print(f"=== reply differs: {tool} {json.dumps(args)[:120]}\n  python: {p[:400]!r}\n  rust:   {r[:400]!r}")
    ta, tb = tree(a), tree(b)
    for f in sorted(set(ta) | set(tb)):
        if ta.get(f) != tb.get(f):
            bad += 1
            if f not in ta or f not in tb:
                print(f"=== file only in {'rust' if f in tb else 'python'}: {f}")
            else:
                print(f"=== file differs: {f}")
                print("".join(list(difflib.unified_diff(ta[f].splitlines(True), tb[f].splitlines(True), "python", "rust", n=1))[:30]))
    la = norm(sh("git", "log", "--format=%B%x00", f"{base}..HEAD", cwd=a).stdout)
    lb = norm(sh("git", "log", "--format=%B%x00", f"{base}..HEAD", cwd=b).stdout)
    if la != lb:
        bad += 1
        print("=== commit messages differ\n" + "".join(difflib.unified_diff(la.splitlines(True), lb.splitlines(True), "python", "rust", n=0)))
    n_commits = len([x for x in la.split("\0") if x.strip()])
    pushed = sh("git", "log", "--oneline", "-1", "master", cwd=S / "originB.git").stdout.strip()
    print(f"{len(calls)} calls, {len(ta)} files under {', '.join(WRITTEN)}, {n_commits} commits; "
          f"rust pushed to its scratch remote: {pushed[:60]}")
    print("ALL IDENTICAL" if not bad else f"{bad} difference(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
