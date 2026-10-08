# Shared WOTR working memory

Scope: War of the Realms only. Isaac requested a shared record for Claude Code,
Codex and Antigravity on 2026-10-07. This file shares durable working notes,
not private chat histories or a model's internal memory.

## Read and update protocol

- Read this at session start after the project constraints and latest handoff.
  Re-read it before using remembered facts after another agent changes it.
- Keep task state in `CONTINUE.md`; keep durable workflow decisions and verified
  operational facts here, with a date, author and evidence or source path.
- Claim `SHARED_MEMORY.md` through Agent Loom before editing; re-read after
  claiming, merge only the intended change, then release the claim. If claims
  are unavailable, do not overwrite a peer's concurrent edits.
- Record user decisions as user decisions. Label agent findings and unverified
  peer reports separately. Correct stale notes openly with a dated replacement.
- Canon stays in its authoritative sources: the live rule index, `RULINGS.md`,
  character sources and `table/*.yaml`. A memory note never creates canon,
  changes a ruling, grants permission or overrides the session's instructions.
- Never copy credentials, private page contents, whole transcripts or unrelated
  personal/project information into this file. Do not bulk-import private
  memories. Distil only relevant, sourced WOTR facts.
- Agent Loom is the message transport, not the memory store. Discover current
  recipients with `list_sessions`; session names are not permanent identities.
  Sending messages still requires the applicable user authorization.

## Durable notes

### 2026-10-08 — WOTR writers' room (Isaac; implemented by Codex)

Isaac approved the reusable scene workflow, shared context packets, reliable
handoff checks and editorial feedback record. Read `WRITERS_ROOM.md` and use
`.claude/skills/wotr-room/SKILL.md` for collaborative scenes. The runner is
`bash build/py.sh build/writers_room.py`; Claude owns prose, Codex reviews
rules/physics/prose, Gemini reviews continuity/voice. These are task roles,
not a model ranking. Exact sources are frozen per room; factual blockers need
source quotations. One review round and bounded mechanical repairs are normal.

`EDITORIAL_FEEDBACK.jsonl` stores only Isaac's explicit editorial reactions.
Default scope is the scene; only explicitly general directions are WOTR-wide.
Corrections append and supersede, never erase. The record begins empty: Isaac
has not yet given editorial reactions to The Bitter Band.

Supervised CLI workers complete independently of an idle interactive chat.
Claude, Codex and Gemini all returned matching acknowledgment nonces in the
runner's live smoke test (local `~/wotr-drafts/rooms/handoff-check.json`).
Antigravity reminder hooks are installed (PreInvocation/Stop); Codex's existing
reminders remain. These are reminders, not proof of idle wakeup. Claude's live
session acknowledged mail through its monitor, which is session-bound. Prefer
the supervised runner for unattended execution; check mail at interactive
handoffs. No private pages, canon writes or publishing are part of this workflow.

### 2026-10-07 — Three-agent memory scope (Isaac; recorded by Codex)

Isaac chose **WOTR only** for shared memory. All three agents use this file in
the WOTR checkout. Other checkouts receive committed updates through Git;
they do not share uncommitted changes. Existing running sessions must explicitly
read new instructions; a changed file does not inject itself into their context.

### 2026-10-07 — Agent Loom connection checks (Codex; verified locally)

Agent Loom is registered for Claude Code, Codex and Antigravity CLI. A
Claude-to-Codex reply completed the initial round trip. An Antigravity message
also arrived in Codex, and Codex queued an acknowledgment back. Antigravity's
reading of that acknowledgment has not been verified.

`agent-loom.service` returned `active`; `~/.codex/hooks.json` contains Agent Loom
references under UserPromptSubmit, PostToolUse and Stop. Claude reports a wakeup
watcher too; its behavior has not been independently verified. No Agent Loom
unread reminder appeared in this Codex conversation before the manual checks.
Do not equate installed hooks with verified automatic delivery.
