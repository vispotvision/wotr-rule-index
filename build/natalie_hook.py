#!/usr/bin/env python3
"""Claude Code hooks that make a checkout the table. Active only where a `.natalie`
marker file sits at the repo root (gitignored; `touch .natalie` in the Natalie clone,
never in the coding checkout). Wired in .claude/settings.json for two events:

  SessionStart  pulls the clone, then prints NATALIE.md, which Claude Code adds
                to context: the standing prompt is in every turn, not retrieved.
                The rule loadout and the Manual Verification Guide are NOT
                pre-loaded: NATALIE.md's own session start protocol fetches them
                live (session_start, load_rules), and load_rules beats any synced
                copy. Pre-stuffing them buried the standing prompt under four
                times its own weight in reference material.
  Stop          runs build/verify.py over the reply just written; any FAIL blocks
                the reply and hands the FAIL list back, so the second pass is
                mandatory. Replies under 120 words or carrying a code fence pass.

Reads the hook JSON on stdin; stdlib only, plus the repo's own verify.py."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"


def last_reply(transcript: Path) -> str:
    """Text of the assistant turn since the last human prompt (tool results are not prompts)."""
    parts: list[str] = []
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        msg = e.get("message") or {}
        content = msg.get("content")
        if e.get("type") == "user" and isinstance(content, str):
            parts = []
        elif e.get("type") == "assistant" and isinstance(content, list):
            parts += [b.get("text", "") for b in content if b.get("type") == "text"]
    return "\n\n".join(p for p in parts if p.strip())


def band(words: int) -> str:
    return "conversational" if words < 700 else "standard" if words < 1500 else "set-piece"


def main() -> int:
    hook = json.load(sys.stdin)
    if not (ROOT / ".natalie").exists():
        return 0
    event = hook.get("hook_event_name")
    if event == "SessionStart":
        subprocess.run(["git", "-C", str(ROOT), "pull", "-q", "--ff-only"], capture_output=True)
        prompt = (ROOT / "desktop" / "NATALIE.md").read_text(encoding="utf-8").split("\n---\n", 1)[1]
        print("This checkout is the table. You are Natalie for the whole session; the standing prompt follows and governs. "
              "A hook verifies every reply you write; a FAIL comes back to you and you fix it before the reply stands. "
              "The WOTR MCP (`wotr`) is connected: session_start on the first turn, load_rules and check_docket before prose, "
              "fow_line for every number, scene_context on the beat and the draft.\n\n" + prompt)
        return 0
    if event == "Stop":
        if hook.get("stop_hook_active"):
            return 0  # one enforced revision per reply; not a loop
        text = last_reply(Path(hook["transcript_path"]))
        words = len(text.split())
        if words < 120 or "```" in text:
            return 0
        sys.path.insert(0, str(BUILD))
        import verify  # noqa: E402
        res = verify.run(text, band=band(words))
        if res.get("fails"):
            report = verify.report(res)
            print(json.dumps({"decision": "block",
                              "reason": "verify_scene on the reply you just wrote:\n\n" + report
                              + "\n\nFix every FAIL and post the corrected reply in full. Nothing else."}))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
