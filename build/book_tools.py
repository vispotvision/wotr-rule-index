#!/usr/bin/env python3
"""The WOTR MCP's read-only tools as a command line, for the book pipeline's agents.

  python build/book_tools.py session_start "Sodoku Moto" standard Kharven
  python build/book_tools.py load_rules prose-law pov scene-structure dialogue register --brief
  python build/book_tools.py check_docket prose-law pov
  python build/book_tools.py scene_brief "the beat, in a sentence" --thread "Sodoku Moto" --type standard --culture Kharven --cast "Sodoku Moto" "Hild Ice"
  python build/book_tools.py character "Sodoku Moto"        fow_line "Sodoku Moto"
  python build/book_tools.py scene_recall "breach road"     wiki "Kharven"
  python build/book_tools.py fronts Kharven                 due 1 Kharven
  python build/book_tools.py scene_menu "Sodoku Moto" --culture Kharven
  python build/book_tools.py verify book/x/ch01/draft_r0.md --band set-piece [--combat] [--culture Kharven]
  python build/book_tools.py gap_fill book/x/ch01/draft_r0.md
  python build/book_tools.py voice_check "Sodoku Moto" "the line as written"
  python build/book_tools.py loadout standard             # the applies_to tags for a scene type

Same functions the MCP serves (build/mcp_server.py), UTF-8 on stdout, nothing that
writes: archiving a chapter is archive_scene through the MCP, on Isaac's approval only.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import mcp_server as M  # noqa: E402


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("tool")
    ap.add_argument("args", nargs="*")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--thread", default="")
    ap.add_argument("--type", default="standard")
    ap.add_argument("--culture", default="Kharven")
    ap.add_argument("--cast", nargs="*", default=None)
    ap.add_argument("--band", default="set-piece")
    ap.add_argument("--combat", action="store_true")
    a = ap.parse_args()
    t, x = a.tool, a.args
    if t == "session_start":
        print(M.session_start(x[0], x[1] if len(x) > 1 else "standard", x[2] if len(x) > 2 else "Kharven"))
    elif t == "load_rules":
        print(M.load_rules_tool(x, None, a.brief))
    elif t == "check_docket":
        print(M.check_docket(x))
    elif t == "scene_brief":
        print(M.scene_brief(x[0], a.thread, a.type, a.culture, a.cast))
    elif t == "character":
        print(M.character(x[0]))
    elif t == "fow_line":
        print(M.fow_line(x[0]))
    elif t == "scene_recall":
        print(M.scene_recall(" ".join(x)))
    elif t == "wiki":
        print(M.wiki(" ".join(x)))
    elif t == "rule":
        print(M.rule(x[0]))
    elif t == "fronts":
        print(M.fronts(x[0] if x else ""))
    elif t == "due":
        print(M.due(int(x[0]) if x else 2, x[1] if len(x) > 1 else ""))
    elif t == "list_conflicts":
        print(M.list_conflicts())
    elif t == "scene_menu":
        print(M.scene_menu(x[0], a.culture))
    elif t == "verify":
        md = Path(x[0]).read_text(encoding="utf-8")
        print(M.verify_scene(md, a.combat, a.culture, a.band))
    elif t == "gap_fill":
        print(M.gap_fill(Path(x[0]).read_text(encoding="utf-8")))
    elif t == "voice_check":
        print(M.voice_check(x[0], x[1]))
    elif t == "voice_fingerprints":
        print(M.voice_fingerprints())
    elif t == "loadout":
        print(" ".join(M.LOADOUTS.get(x[0], M.LOADOUTS["standard"])))
    else:
        sys.exit(f"unknown tool {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
