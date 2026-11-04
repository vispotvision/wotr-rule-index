#!/usr/bin/env python3
"""The Python side of the Rust WOTR MCP (rust/): the tools not yet ported run here.

  python build/mcp_worker.py --dump   # write rust/tools.json: every tool's name, description and
                                      #   input schema, the core and read-only sets, the skill lists
  python build/mcp_worker.py          # serve: one JSON request per stdin line,
                                      #   {"tool": name, "args": {...}} -> {"ok": text} | {"err": text}

The Rust server spawns the serve mode once, on the first call it cannot answer itself, and keeps
it, so mcp_server is imported once a process. Tools print to stdout freely: responses go to the
original stdout fd and sys.stdout is pointed at stderr before anything is imported.
"""
import json
import os
import sys
from pathlib import Path

out = os.fdopen(os.dup(1), "w", encoding="utf-8", buffering=1)
sys.stdout = sys.stderr
sys.argv = sys.argv[:1] + [a for a in sys.argv[1:] if a == "--dump"]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mcp_server as M  # noqa: E402


def dump() -> None:
    tools = [{"name": t.name, "description": t.description or "", "inputSchema": t.parameters}
             for t in M.server._tool_manager._tools.values()]
    spec = {"instructions": M.server.instructions, "tools": tools,
            "core": sorted(M.CORE_TOOLS), "read_only": sorted(M.READ_ONLY_TOOLS),
            "skill_hide": sorted(M.SKILL_HIDE), "ops_skills": sorted(M.OPS_SKILLS), "skill_note": M.SKILL_NOTE}
    path = M.ROOT / "rust" / "tools.json"
    path.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {path} ({len(tools)} tools)")


def serve() -> None:
    tools = M.server._tool_manager._tools
    for line in sys.stdin:
        try:
            req = json.loads(line)
            t = tools[req["tool"]]
            # the caller's key: audio and image links are built with its base URL and token
            pub = req.get("public") or {}
            M.PUBLIC["base"], M.PUBLIC["token"] = pub.get("base", ""), pub.get("token", "")
            res = t.fn(**req.get("args") or {})
            resp = {"ok": res if isinstance(res, str) else str(res)}
        except Exception as e:  # noqa: BLE001 - every failure goes back to the caller as text
            resp = {"err": f"{type(e).__name__}: {e}"}
        out.write(json.dumps(resp, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    dump() if "--dump" in sys.argv else serve()
