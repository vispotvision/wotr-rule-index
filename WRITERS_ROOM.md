# WOTR writers' room

Say **“writers' room: surprise me”** or **“writers' room: [your scene premise]”**
to Claude, Codex or Gemini in this checkout. The project skill is
`.claude/skills/wotr-room/SKILL.md` (Codex discovers it through the existing
`.agents/skills` link). The coordinating agent loads the current WOTR context,
chooses the relevant public sources and runs the room. New sessions pick up the
skill; an existing session can read it explicitly.

Claude authors the prose. Codex reviews rules, physical mechanisms and prose;
Gemini reviews continuity, timeline, POV knowledge and voices. These are working
assignments, not claims that one model is universally best at a task.

## One command

From `/home/oridon/wotr-rule-index`, using the existing CLI logins:

```bash
bash build/py.sh build/writers_room.py run fresh-nalun \
  --culture 'Nalūn' --pov 'Fresh cast' --type quiet \
  --prompt 'Surprise me with a fresh standalone scene and fresh adult characters.' \
  --source 'wiki/The Tongues of the Realms/Common — The Tongue With No Distinctions.md'
```

The coordinating agent selects culture, scene type and length from the request
and current live rules. The CLI's convenience defaults are Nalūn/quiet/standard;
they are not a universal creative preference. Add `--source` for each relevant
card, timeline, prior scene, State of Play or research note; add `--codex TERM`
for every working being used. Complete public source files are snapshotted.
Standing Inventory and public culture-titled wiki pages are included automatically.
Existing cast needs its current authoritative cards and thread context selected
by the coordinating agent. Missing decisive context stops the worker.

`prepare` takes the same scene arguments and makes the packet without calling
models. `run --room /absolute/path/to/room` resumes completed stages. All CLI
models use their configured defaults; no API key or separate service is required.
The runner invokes the installed Claude binary through mise without using the
shell wrapper that auto-updates it. Codex falls back to the desktop app's bundled
binary when it is absent from the shell PATH.

## What the command does

1. Creates a new directory under `/home/oridon/wotr-drafts/rooms/<slug>`.
2. Freezes `packet.json`: the brief, exact live rules and docket, source texts,
   explicit editorial feedback and hashes. Every worker gets the same packet.
3. Runs Claude, then Codex and Gemini concurrently, then one Claude revision
   when findings or mechanical checks call for it. Each review has at most five
   actionable findings and one passage to protect.
4. Requires exact source and draft quotations for factual blockers. Unsupported
   additions and taste suggestions are classified separately. Claude records
   what it kept/declined. A disputed blocker stops for coordinator judgment.
5. Runs the existing WOTR verifier; allows one further mechanical repair by
   default. Saves `final.md`, `notes.md`, reviews, verification and `state.json`.

`ready` means the original draft was cross-read, the author addressed findings,
and the final draft passed mechanical checks. It is not a claim that every final
sentence was independently reread or that Isaac has accepted the scene. The
reviewed and final hashes are recorded separately; warnings remain visible.
The coordinating agent reads the final and presents it to Isaac.

## Delivery and recovery

Supervised workers run to completion independently of whether an interactive
chat is awake. They use the local Claude/Codex/Antigravity CLIs. An acknowledgment
test proves this path; Loom mail and live-session push are separate paths.
Claude's unattended worker has tools/MCP and inbox hooks disabled for that
invocation. Codex uses a read-only sandbox with its hooks and user-configured MCP
servers disabled for that invocation; Gemini uses plan mode. No worker is
launched with permission bypass flags. Workers are instructed to return content,
not to operate tools. These CLIs still apply their own managed policies.

Loom remains the interactive transport: check its inbox at each handoff, require
an acknowledgment, inspect receipts, and distinguish **spooled**, **read**, and
**completed**. Codex has reminder hooks; Antigravity has PreInvocation/Stop
reminders. Those hooks remind a running/resumed session; they do not promise an
idle-session wakeup. Claude's current monitor has acknowledged live mail but is
session-bound. The supervised command does not depend on that monitor.

Optional `recipients.json` in a room maps `claude`, `codex`, `gemini` to freshly
discovered Loom session IDs. The runner sends idempotent, no-Slack observation
mail; those notifications do not dispatch duplicate work or establish completion.

```bash
bash build/py.sh build/writers_room.py smoke
bash build/py.sh build/writers_room.py status /home/oridon/wotr-drafts/rooms/fresh-nalun
bash build/py.sh build/writers_room.py run --room /home/oridon/wotr-drafts/rooms/fresh-nalun
bash build/py.sh build/writers_room.py run --room /home/oridon/wotr-drafts/rooms/fresh-nalun --redo gemini-review
```

Each room is locked against concurrent runners. Valid completed stages are reused.
Invalid responses are retained as `*.rejected.json`; `--redo STAGE` reruns a stage
and discards its downstream outputs. Worker failure, timeout, missing context,
unsubstantiated blocker, disputed blocker or exhausted repairs sets
`needs_attention`, never `ready`. Changing the packet requires a new room.
To add missing facts or change the premise, prepare a new slug with the corrected
source set. There is no infinite retry loop. Default timeout is ten minutes per
worker; `--timeout` changes it. `--repairs 0..3` changes the mechanical budget.

## Isaac's editorial feedback

`EDITORIAL_FEEDBACK.jsonl` is an append-only, WOTR-only record of Isaac's explicit
reactions. It starts empty; reviewers' opinions are never recorded as his taste.
When Isaac says he likes/dislikes a passage or gives a creative direction, the
coordinating agent records his words and any quoted passage. Default scope is
that scene; use `wotr` only for an explicitly general preference. Claim the file
through Loom before editing, following the shared-memory protocol.

```bash
bash build/py.sh build/writers_room.py feedback \
  --scene SCENE-SLUG --kind liked --scope scene --text 'Isaac’s actual words'
```

Kinds: `liked`, `disliked`, `direction`, `correction`. `--quote` stores a passage.
Corrections use `--supersedes ID`; old records remain visible and the newer record
governs. Feedback is frozen into the next packet, not injected into an active run.
It guides craft; it cannot change canon or create rules.

## Boundaries

The workflow neither archives nor publishes scenes, changes the table, amends
rules, restarts live WOTR jobs, nor imports private conversations. Private wiki
pages and secret-bearing source URLs are rejected from packets. Bulk outputs of
`session_start`/`scene_context` may contain private material: the coordinating
agent reads those locally, then selects public source files for the packet.
If the necessary thread context is private, use the interactive workflow locally
under the existing privacy rules instead of exporting it through this runner.
Draft artifacts stay outside the publishing checkout. Only the workflow and
explicit feedback records belong in Git.
