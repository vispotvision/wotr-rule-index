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

### 2026-10-11 — Law reading revised: rulebook digest once a session, full wording per task (Isaac; recorded by Claude Code)

Isaac replaced the same-day "full word-for-word reading before every task"
direction (the note below) after weighing its cost: about 325k tokens a task,
crowding out the card and the scene. Now every model, Claude, Codex, ChatGPT
and Antigravity alike: once a session before the first drafting or revision,
read every live rule as one line, `load_rules(tags=[], brief=True)` (about
82k tokens; `part=1..4` where a client truncates, every part read); then per
task the full wording for its domain tags, `check_docket`, and `rule(id)` for
anything outside them whose line is not enough. Re-read after compaction.
Written into AGENTS.md, desktop/NATALIE.md and desktop/NATALIE.gpt.md.
Logged with log_ruling 2026-10-11.

### 2026-10-11 — Complete indexed law pass finished (Codex; verified coverage)

Completed the requested reading of all 1,742 indexed rules (1,546 live,
196 superseded), with their full indexed wording, statuses and amendment
notes, in 45 bounded batches. All 77 source hashes matched before/after.
Coverage and per-batch comprehension notes are in
`reports/gpt-law-reading-2026-10-11.json`; scope, limitations and the practical
reading are in `reports/gpt-law-reading-2026-10-11.md`. Also read the current
open-labelled conflict sections and selected source tables omitted from
short indexed quotes. This does not claim every entire guide or canon page
was read. Reference tables and scene-specific canon still require consultation.

This completed pass does not replace Isaac's requirement to read the full
current law before each new drafting/revision task. In particular: R49-18/19
allow similes and extended metaphors; R70-21/27 retain the POV culture's
cadence/diction; R4-13-FID and R49-08/43 protect consequential thought;
R52-16 gives Lambert audible counting when shaken, not merely a generic
thumb tell; R74-14 distinguishes deceptive truth from a bodily lie tell.
Do not turn a verifier PASS or a retrieved loadout into a literary-quality
or complete-reading claim. No rule/canon changes were made by this reading.

### 2026-10-11 — Complete rule reading every writing task (Isaac; recorded by Codex)

Isaac directed “read through all of the rules / laws and understand most if
not all of them” and “save in memory to make sure you do this every single
time.” Before each WOTR drafting or revision task, read the complete current
rule/law index, including authoritative wording, statuses, amendment notes and
supersession relationships. Tagged subsets, summaries, truncated previews and
remembered prior reading do not satisfy this direction. Use bounded batches
with explicit source/coverage tracking; after compaction resume actual reading
and do not convert a retrieved response into a claim of comprehension.
Apply the relevant rules against the POV card, culture and Inventory afterward.
This requirement is also in AGENTS.md and desktop/NATALIE.gpt.md. It records a
required process, not a claim that the complete reading has already happened.

Isaac also welcomes metaphor, simile, wit and plot devices; overload is the
problem, not their presence. His latest scene critique qualifies lexical
amplitude by viewpoint: Tabitha's close narration should retain her road work
and Kharven register. Richness must not become an indiscriminate drawing-room
voice, and developed thought must not become repetitive self-diagnosis.

### 2026-10-11 — Greater prose amplitude and vocabulary (Isaac; recorded by Codex)

Isaac additionally objected that GPT is insufficiently verbose and avoids
complicated vocabulary. This is his explicit general WOTR preference, not a
research finding. `desktop/NATALIE.gpt.md`, “Amplitude and vocabulary,” now
requires fuller development of thought, memory, cultural context and aftermath,
with sophisticated precise vocabulary and complex syntax suited to the POV.
Keep apt uncommon words and cumulative clauses; preserve different speakers'
registers. Removing procedural padding must not become a mandate for shorter,
simpler prose. The player's decision boundary still governs length.

### 2026-10-11 — GPT prose corrections after research (Isaac; implemented by Codex)

Isaac requested GPT-specific writing directions informed by research and the
existing Claude guidance. He identified six faults to correct generally:
script-like short paragraphs, perception without developed thought, clipped
interchangeable voices, obscure practical stakes, fragment cascades after a
realization, and repeated document-handling procedure used as padding. His
draft counts and proportions were reported feedback, not independently measured.

`desktop/NATALIE.gpt.md` now directs developed attention and consequential
interiority, distinct professional reasoning and wants, locally understandable
stakes, earned rhythm and recurrence, and compression of routine procedure
without blanket concision. *The Weak Grade* is primary; *The Fourth Letter*
remains a supporting example, preserved byte-for-byte. Audio tags belong only
to an output calling for audio presentation. No gesture/paragraph quotas were
added. Current house law, source lookup, player agency and verifier honesty
remain. These are GPT editorial directions, not new canon or index rules.

Research and limitations: `reports/GPT prose craft research.md`; evidence,
local audit and checks: `research_notes/GPT prose craft research/`. Distinguish
official Astra behavior guidance, studies of other named models, Isaac's
preferences and editorial inference. No controlled generation A/B trial has
proved improvement; a verifier pass or model agreement is not literary proof.
The coordinating Codex session confirmed the new `natalie_gpt` live readback.
Applied locally with pre-existing dirty work preserved; no base Claude prompt,
canon or rule-index changes, and no commit/push in this task.

### 2026-10-11 — Automatic GPT overlay startup (Isaac; recorded by Codex)

Isaac explicitly directed: “always automatically run natalie.gpt.” Every WOTR
chat running on a GPT model must call `natalie`, then `natalie_gpt`, and read
the complete overlay before answering or drafting, even if the first tool
already appended it. Apply its explicit precedence over the base prompt;
do not stop a writing request at a Scene Menu. This is also recorded in
`AGENTS.md`. The dedicated `mcp__wotr__natalie_gpt` tool was called and returned
the full overlay in this chat. The file `desktop/NATALIE.gpt.md` now exists;
the earlier “not found” report describes the earlier session only.

### 2026-10-11 — The Weak Grade as primary prose reference (Isaac; recorded by Codex)

Isaac supplied *The Weak Grade*, said “want something your style to be more like this,”
confirmed “this is the style I want you to write,” and requested inclusion in Natalie's
standing setup. `desktop/NATALIE.md` now embeds the direction and an exact prose
example under PROSE STANDARDS. `desktop/CHATGPT_INSTRUCTIONS.md` points to that
section. The full attachment is preserved unchanged at
`desktop/style-bank/references/the-weak-grade-isaac-reference.md`.
Scope is WOTR drafting and improvement: developed perception, memory, reasoning,
emotion, cultural causality, cumulative rhythm and purposeful recurrence. Do not
reduce this to longer paragraphs or remove meaningful thought as “gloss.” Preserve
POV, agency, current canon and mode-specific disclosure. Audio cues are separate.
The guide Page is https://chatgpt.com/space/page_ef4739666b7c8191944b53bbd76eeb22.
This is an explicit style preference, not adoption of the sample's new canon.

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
