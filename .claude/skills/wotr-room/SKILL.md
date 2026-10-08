---
name: wotr-room
description: Run Isaac's WOTR writers' room with Claude as prose author, Codex as rules/physics/prose reviewer and Gemini as continuity/voice reviewer. Use when he asks the three AIs to write together, invokes the writers' room, or requests its setup/status; ordinary solo writing keeps the existing wotr-write workflow.
---

# WOTR writers' room

Read `WRITERS_ROOM.md` for commands, result semantics and recovery. Project
constraints and the live WOTR writing rules still apply.

When Isaac requests a collaborative scene, coordinate it through
`bash build/py.sh build/writers_room.py run <slug> ...`. Choose culture, POV,
scene type and length from his request and current live rules. “Surprise me”
permits fresh cast and a fresh hook, not invented canon mechanics or statistics.

Before dispatch, use the usual `session_start`, rules/docket and lorebook flow
locally. Select the authoritative public cards, State of Play, relevant prior
scenes/timeline, culture/voice pages and researched physical facts as `--source`
files. Use `--codex` for workings. Do not export private pages or secret-bearing
links through an aggregated tool reply. If required context cannot enter the
packet, use the existing interactive process under its privacy constraints.

The runner uses the existing CLI logins, not the identity of a currently open
chat. It freezes one packet for all workers, retains reviews/dispositions, and
stops on failure. One review round is normal; further calls address specific
mechanical failures. Keep Claude's authorship. Read the final scene and notes,
check any remaining warnings and whether the revision created a new continuity
problem, and present the prose and concise author notes to Isaac. Never equate
mechanical PASS with literary quality or canon acceptance.

For interactive Loom coordination, discover live recipients, check inbox at
handoffs, require acknowledgment and distinguish queued/read/completed. Do not
claim automatic idle wakeup from installed reminder hooks. `smoke` tests the
supervised CLI path, not live push. User authorization to use the writers' room
covers its author/reviewer handoffs, not unrelated messages or publishing.

Record Isaac's explicit editorial reactions through `feedback`, with his words
and scene scope by default. Claim `EDITORIAL_FEEDBACK.jsonl` before the append.
Only explicitly general preferences get `--scope wotr`; never label a reviewer's
opinion or an inferred preference as Isaac's. Corrections append with
`--supersedes`. Source laws remain authoritative.
