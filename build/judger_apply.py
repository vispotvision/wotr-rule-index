#!/usr/bin/env python3
"""Apply the proposals Isaac approved from a Judger's note.

  python build/judger_apply.py <slug>                 # list the proposals and their state
  python build/judger_apply.py <slug> P01 P03 ...     # run those, by id
  python build/judger_apply.py <slug> --all           # run every proposal not yet applied

Reads bot/queue/<slug>.judger.json (written by .claude/workflows/judger-assist.js),
calls the MCP's own write tools with the proposal's args, and records what ran
under "applied" so a proposal is never run twice. The *_note proposals (card,
timeline, inventory, conflict) are printed for Isaac to act on by hand — they
touch Notion pages or repo files the tools do not own.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import mcp_server as M  # noqa: E402

QUEUE = ROOT / "bot" / "queue"
WRITERS = {
    "ledger_add": lambda a: M.ledger_add(a["category"], a["who"], a["text"], a.get("due_after_sessions"), a.get("due_condition", "")),
    "advance_front": lambda a: M.advance_front(a["front_id"], a["what_happened"], a.get("next_move", "")),
    "set_front_clock": lambda a: M.set_front_clock(a["front_id"], a["ticks"]),
    "add_front": lambda a: M.add_front(a["name"], a["thread"], a["want"], a["ticks"], a.get("next_move", "")),
    "npc_set": lambda a: M.npc_set(a["name"], a["thread"], a.get("want", ""), a.get("refusal_line", ""), a.get("knows"), a.get("lied_about"), a.get("last_seen", ""), a.get("voice", "")),
    "log_ruling": lambda a: M.log_ruling(a["rule_id"], a["ruling"], a.get("context", "")),
    "propose_rule": lambda a: M.propose_rule(a["title"], a["rule_text"], a["applies_to"], a.get("rationale", ""), a.get("session", "")),
}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    slug = sys.argv[1].replace(".md", "")
    ids = sys.argv[2:]
    p = QUEUE / f"{slug}.judger.json"
    if not p.exists():
        sys.exit(f"no Judger's note for {slug}: run the judger-assist workflow first (bot/queue/{slug}.judger.json)")
    note = json.loads(p.read_text(encoding="utf-8"))
    applied = {a["id"]: a for a in note.get("applied", [])}
    props = {x["id"]: x for x in note.get("proposals", [])}

    if not ids:
        print(f"# {slug} — {note.get('thread', '')}")
        for pid, x in props.items():
            state = "applied " + applied[pid]["result"][:60] if pid in applied else "waiting"
            print(f"{pid}  {x['tool']:14}  {state}\n      {json.dumps(x['args'], ensure_ascii=False)[:160]}")
        for x in note.get("rejected", []):
            print(f"{x['id']}  {x['tool']:14}  set aside: {x.get('reason', '')[:100]}")
        return 0

    if ids == ["--all"]:
        ids = [pid for pid in props if pid not in applied]
    for pid in ids:
        x = props.get(pid)
        if not x:
            print(f"{pid}: not in the note (set aside, or a typo)")
            continue
        if pid in applied:
            print(f"{pid}: already applied on {applied[pid]['when']}: {applied[pid]['result'][:80]}")
            continue
        tool, a = x["tool"], x["args"]
        if tool in WRITERS:
            try:
                result = WRITERS[tool](a)
            except Exception as e:  # a bad arg must not stop the rest
                print(f"{pid} {tool}: FAILED {e}")
                continue
        else:  # a note for Isaac's hands, not a tool call
            result = f"by hand: {a.get('target', '')} — {a.get('note', '')}"
        from datetime import date
        note.setdefault("applied", []).append({"id": pid, "tool": tool, "when": date.today().isoformat(), "result": result})
        print(f"{pid} {tool}: {result}")
    p.write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
