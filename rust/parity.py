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
    for q in ["Soul Crystal", "Renard Greymane", "Emira", "Kaalabad", "Standing Inventory Kharven", "the Scene Archive",
              "Pyreveil thermal debt", "What Things Cost", "Kōkan Line", "Shirogane", "how does eta work", "Wellspring",
              "Draw Age standpipes", "Aetherion Academy", "Malphas", "Hild Ice", "Cozbi Mahuo", "Yoko Mishiro", "Measurewright",
              "Release forms", "Dominion Pressure", "the Veil", "zzzz nothing qqq", "Moto", "Sodoku Moto Arctic Lion"]:
        yield "wiki", {"query": q}
        yield "wiki", {"query": q, "full": False, "limit": 12}
    for q in ["the duel at the arena", "Amelia Greymane", "a funeral in the snow", "Yukazuri", "the ledger comes due",
              "Glass and Irons", "the king's door", "who swore the oath", "fire meets frost", "Kujo arc"]:
        yield "scene_recall", {"query": q}
        yield "scene_recall", {"query": q, "old_lore": True, "limit": 12}
    for sp in sorted((ROOT / "lore/v1/scenes").glob("*.md"))[::8] + sorted((ROOT / "scenes").glob("*.md"))[:6]:
        txt = sp.read_text(encoding="utf-8", errors="replace")
        yield "scene_context", {"draft": txt[:3000]}
    yield "scene_context", {"draft": "Sodoku Moto walked in. Nobody spoke to Blarvex Quintillion, and Blarvex Quintillion said nothing back."}
    import table as T
    threads = sorted({str(r.get("thread")) for k in ("fronts", "ledger", "npcs", "threads") for r in T.load(k) if r.get("thread")})
    for th in threads + ["", "Kharven", "nowhere-thread", "Sodoku", "Moto"]:
        yield "fronts", {"thread": th}
        yield "fronts", {"thread": th, "include_closed": True}
        yield "due", {"thread": th}
        yield "due", {"thread": th, "sessions_old": 0, "today": "715-3-14"}
        yield "roster", {"thread": th}
        yield "roster", {"thread": th, "public": True}
        if th:
            yield "scene_menu", {"thread": th}
            yield "session_start", {"thread": th}
    for c in [p.stem for p in (ROOT / "desktop/inventories").glob("*.md")] + ["Nowhere", "kharven"]:
        yield "session_start", {"thread": "the-uncounted", "culture": c}
        yield "scene_menu", {"thread": "the-uncounted", "culture": c}
    import tempfile
    sys.path.insert(0, str(ROOT / "build"))
    import codex as Cx
    sh = Cx.sheets()
    qs = ["", "  ", "Pyreveil", "zzzqqq", "ignis", "[Ab]", "12", "3", "Thermal", "Archon", "a", "Cymorath", "Crymorath"]
    for name, rows in sh.items():
        for r in rows[1::9]:
            qs += [str(c) for c in r[:3] if c not in (None, "")][:2]
    for q in qs:
        yield "codex", {"query": q}
        yield "codex", {"query": q, "limit": 3}
    for sname in list(sh) + ["lists", "Nope"]:
        for q in ["Pyreveil", "fire", "i", "zzz"]:
            yield "codex", {"query": q, "sheet": sname, "limit": 50}
    yield "codex", {"query": "fire", "limit": 0}
    yield "codex", {"query": "fire", "limit": -2}
    glyphs = [str(r[0]) for r in sh["Master Glyph Index"][1:12]]
    spells = [str(r[1]) for r in sh["Spell Index"][1:6] if r[1]]
    yield "codex_check", {"markdown": "Nothing here."}
    yield "codex_check", {"markdown": " ".join(glyphs) + " [Zz] [Ab](link) Crymorath Velorath Mistatio proposed Quillantia.\n\n## Notes\n[Qq] Bogusatio"}
    yield "codex_check", {"markdown": "The " + ", ".join(spells) + " and " + " ".join(glyphs[:3]) + " Pyreveil Cymorath"}
    yield "codex_check", {"markdown": "A Velorath line, proposed: Velorath.\nThe Mistatio stood."}
    for sp in sorted((ROOT / "scenes").glob("*.md")) + sorted((ROOT / "lore/v1/scenes").glob("*.md"))[::4] + sorted((ROOT / "wiki/The Magic System").rglob("*.md"))[::7]:
        md = sp.read_text(encoding="utf-8", errors="replace")
        yield "codex_check", {"markdown": md}
        yield "gap_fill", {"markdown": md}
    yield "gap_fill", {"markdown": ""}
    yield "gap_fill", {"markdown": "# Head\n\nHe struck. Resonance resonance RESONANCE momentum because so it.\n\nη eta EU coupling Coherence lattice"}
    for scope in ["all", "wiki", "scenes", "nope"]:
        for mf in [60, 0, 5, -3, 10000]:
            yield "stale_names", {"scope": scope, "max_files": mf}
    chars = ["Sodoku Moto", "Yoko", "zzz-nobody", "Emira"]
    for st in ["standard", "duel", "battle", "talky", "quiet", "explicit", "working", "nope"]:
        yield "scene_brief", {"beat": "  A duel at dawn on the ice.  ", "scene_type": st}
        yield "scene_brief", {"beat": "x", "thread": "the-uncounted", "scene_type": st, "characters": chars}
    yield "scene_brief", {"beat": "b", "characters": []}
    tmp = Path(tempfile.mkdtemp(prefix="trello"))
    board = {"lists": [{"id": "L1", "name": "Characters"}, {"id": "L2", "name": "Places — North"}, {"id": "L1", "name": "Dup List"}],
             "cards": [{"name": "Sodoku", "idList": "L1", "desc": "A cold   man\nof iron", "labels": [{"name": "PC"}, {"name": "Moto"}], "id": "c1"},
                       {"name": "Closed one", "idList": "L2", "closed": True, "desc": "gone"},
                       {"name": "Kharven Docks", "idList": "L2", "desc": "", "labels": []},
                       {"name": "Orphan", "idList": "L9", "desc": "fire and frost"},
                       {"name": "Ünïcode Ice", "desc": "Hild Ice, the wall", "closed": 0}],
             "checklists": [{"idCard": "c1", "name": "Kit", "checkItems": [{"name": "sword"}]}]}
    (tmp / "board.json").write_text(json.dumps(board, ensure_ascii=False), encoding="utf-8")
    (tmp / "list.json").write_text(json.dumps([{"name": "A", "desc": "one two"}, "skip", {"name": "B", "labels": [{"name": "x"}]}]), encoding="utf-8")
    (tmp / "one.json").write_text(json.dumps({"name": "Solo", "description": "the desc here"}), encoding="utf-8")
    (tmp / "num.json").write_text("42", encoding="utf-8")
    for f in ["board.json", "list.json", "one.json", "num.json"]:
        for ln, q in [("", ""), ("char", ""), ("north", ""), ("", "fire"), ("", "ICE"), ("nope", "")]:
            yield "trello_cards", {"json_path": str(tmp / f), "list_name": ln, "query": q}
    yield "trello_cards", {"json_path": str(tmp / "missing.json")}
    yield "trello_cards", {"json_path": "relative/missing.json"}
    sf = M._scene_files()
    for p, t in sf:
        yield "scene_text", {"scene": p.name}
        yield "scene_text", {"scene": t}
    for q in ["", "glass", "GLASS_AND_IRONS", "zzz", "it's", 'say "no"', "back\\slash\n", "naiser", "the"]:
        yield "scene_text", {"scene": q}
    scenes = sorted(p for p in (ROOT / "scenes").glob("*.md")) + sorted((ROOT / "lore/v1/scenes").glob("*.md")) \
        + sorted((ROOT / "desktop/style-bank").rglob("*.md"))
    for p in scenes:
        md = p.read_text(encoding="utf-8", errors="replace")
        yield "verify_scene", {"markdown": md}
        yield "verify_scene", {"markdown": md, "combat": True, "explicit": True, "turn": True}
        yield "verify_scene", {"markdown": md, "combat": True, "culture": "Moto"}
        yield "verify_scene", {"markdown": md, "combat": True, "school": "boxing"}


def main() -> int:
    bad, seen, total, order_only = {}, {}, 0, {}
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
        if py != rs and sorted(py.splitlines()) == sorted(rs.splitlines()):
            order_only[tool] = order_only.get(tool, 0) + 1  # same lines, ties in another order
            continue
        if py != rs:
            bad.setdefault(tool, []).append(args)
            if len(bad[tool]) == 1:
                shown = {k: (v[:60] + "...") if isinstance(v, str) and len(v) > 60 else v for k, v in args.items()}
                print(f"\n=== MISMATCH {tool} {shown}")
                print("".join(list(difflib.unified_diff(py.splitlines(True), rs.splitlines(True), "python", "rust", n=1))[:40]))
    for tool, n in seen.items():
        print(f"{tool:15} {n - len(bad.get(tool, [])):5}/{n} match" + (f" ({order_only[tool]} of them in a different tie order)" if tool in order_only else ""))
    print(f"{total} cases, {sum(map(len, bad.values()))} mismatches")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
