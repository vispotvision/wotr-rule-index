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

### 2026-10-29 — Volume I culled to the new lore (Isaac's decision; recorded by Claude Code)

Isaac's scope for the New Lore: the Great Conflict of the North (The
Uncounted), the Sin of Wrath material, and Amelia and Muken's love. Every
Volume I card outside it was deleted the same day, about 285 in all, old
voice-roster and villain cards included (Malphas, Yoko, Cozbi, Emira, Charles
Lambert, Verinus, Sodoku). Retconned out by his ruling: Hild Ice, and for now
Ayame Yuno, Sodoku, Edward Lambert and Fern Stark. Also cut: Dougou (no longer
his to run), Naevra Yukari, Borin and Raizan; Naiser was cut and restored the same
hour, since he is still Isaac's character. Kept: Naiser, Muken, Yukazuri, Gimbzo, Lorn, Godfrey, Shōki and
Vaashuuk. Rashani and Rengai (Zettari, no longer his to run) and Renard (does
not exist yet) were cut too. The cards carry no frontmatter properties (Isaac's
direction); the Volume I folder's private manifest entries keep them off the site. Many cut characters will
be recreated; old text is in git history. `character()` misses on cut names,
and NATALIE.md's voice roster still names cut characters.

### 2026-10-18 — Lore reset: the old archive is `lore/v1/` (Isaac's decision; recorded by Claude Code)

Archived scenes and table state from before the reset live in `lore/v1/`
(scenes, table yaml, the vault's Scene Archive and retired Table pages). They
are not canon for events in the new lore. Live `scenes/` and `table/` began
empty on 2026-10-18. Search the old archive only with
`scene_recall(query, old_lore=True)`; its hits are labelled old lore. Never
archive into or edit `lore/v1/`. Evidence: commits 22925d7, 4437d17;
`lore/v1/README.md`.

### 2026-10-17 — R79: the table made lean (Isaac's decisions; recorded by Claude Code)

Two questionnaires (`imports/drafts/prose-rp-questionnaire/`,
`imports/drafts/coverage-questionnaire/`) became R79-1 to R79-12
(`rules/doc-directions-2026-10-17.yaml`). For every model: load the brief
rulebook once, a domain on first use, no re-read after compaction; Natalie may
write Isaac's PC (never other creators' characters, never a guest's on Discord);
~3,500 words every in-fiction reply; nothing printed under a turn; scene end is
`session_end` (silent upkeep of Ledger, Fronts, roster and cards, plus archive);
no rhythm, length or count rules; State of Play pages and the judger are
retired; improving his post is a free rewrite toward his intent. Older notes
here about keep-every-beat, tells-only roleplay fights, the OOC foot or the
close are superseded.

### 2026-10-16 — The elevated word bank is retired (Isaac's decision; recorded by Claude Code)

R78-11-WORDS_FROM_THE_THING (`RULINGS.md` 2026-10-16): no fixed word list.
Words are chosen from what the sentence describes, exact and resonant where
earned, plain where plain is truer; no no-repeat rule, no density count.
`desktop/style-bank/elevated-words.md` is deleted and verify_scene's
elevated-density WARN removed. The 2026-10-13 note below that says to read the
bank before drafting is stale on that point; R78-3's physical clarity and
fight-abstraction WARN stand.

### 2026-10-15 — The wiki left Notion; it is the Obsidian vault, published as a designed site (Isaac's decisions; recorded by Claude Code)

Isaac's decisions: Notion hit its free block limit and he would not pay, so the wiki
moved to Obsidian + Quartz the same day. `wiki/` in this repo is the source and the
vault; Notion is retired and frozen and is never written again. The public site is
https://vispotvision.github.io/wotr-rule-index/ (every page except the Author's
Workroom and anything private), rebuilt on each push to `wiki/**`. He asked for it to
be beautiful and in order, and checked it section by section: every page has art
(plates, painted banners, SVG diagrams), mermaid charts are redrawn as art on the site,
every section is filed into shelves, tables and spacing were reworked. The character
cards are personal to him: never reorganize, restyle or publish them.

Working facts for any agent (evidence: `AGENTS.md` "The wiki and the public site",
`build/site_content.py`, `build/site_art.py`, `build/site_charts.py`):
- Write wiki pages with `wiki_write`, `create_character`, `update_character`,
  `archive_scene`; links are `[[full/vault/path|Title]]`.
- Shelves: a section's pages sit in sub-folders, each with its own front page
  `X/X.md`; a hub page lives inside its folder. New pages go on their shelf; a new
  shelf gets a front page and a name in the sidebar `sortFn` list
  (`site/quartz.config.yaml`).
- Markdown: a blank line between paragraphs, sections as `##`, a blank line before a
  table. The Notion export wrote one paragraph per line without blank lines, which the
  site ran together; that was fixed in 603 pages and the build now adds the breaks.
- Art: diagrams are `wiki/Assets/Diagrams/*.svg` from `build/site_art.py`, embedded
  with `![[Assets/Diagrams/name.svg]]`; paintings for shelves are ChatGPT images in
  `wiki/Assets/Paintings/*.webp` (embedded at the top of each hub so Obsidian shows them), mapped in `FOLDER_ART`.
- The autosave (`wotr-sync.timer`, every 15 minutes) commits and pushes `wiki/`.


### 2026-10-13 — Vocabulary bank, modern science, conflicts ruled (Isaac's directions; recorded by Claude Code)

Isaac's decisions: (1) vocabulary is pushed high, and his 2026-10-11 direction is
now live in the index as R78-1-VOCABULARY_PUSHED_HIGH (it had stayed out of
`rules/`, so `load_rules` served R51-13's "by ear"). Before drafting, read
`desktop/style-bank/elevated-words.md`, the widened elevated bank: glossed by
sense domain; since 2026-10-14 (R78-3) saturated, stackable, English of every
root, no word twice on a page, the POV's reach choosing which words.
(2) He retracted the 1900 limit on scientific ideas: R78-2-MODERN_SCIENCE_IDEAS.
Modern science may explain workings and fights and drive magical research; it is
known through the Aether by high-Stage practitioners, Measurewrights and
scholars, never by commoners; built hardware keeps R53-01 and the R53-03 firearm
ceiling (his answers to a three-question questionnaire). Agent finding: a
word-frequency checker for rare vocabulary was tried and rejected, as it
rewards concrete compounds, not elevated diction. (3) Every open CONFLICTS row
(C-113 to C-162) was ruled as an agent ruling in RULINGS.md; owed application
items are in `imports/drafts/conflict-rulings-2026-10-13/apply.md`.

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

### 2026-11-03 — Combat and magic fix, R81 (Claude Code; Isaac's decisions)

Isaac answered a 20-question combat and magic questionnaire
(`imports/drafts/combat-magic-fix-questionnaire/answers.json`), logged in
RULINGS.md and indexed as R81-1 to R81-19 (`rules/doc-directions-2026-11-03b.yaml`).
Key decisions: every Blow Card part in every blow, quick trades compressed; full
Working Card at first display, finisher and change, repeats by what changed; η as
an idea and proportion in narration; narration explains in any POV; held cards
explained at the reveal; physics named on the page; signature sounds never
retire; own Domain inside the two-Grade cap; on "continue" the PC's choice is
carried by card and flagged; PC past invented freely; PC wounds onto the card at
scene end; technique entries in the Hiromi layout with no Applications list.
verify.py now FAILs only exact stock phrases (canon Wellspring signatures
exempt), allows en dashes, drops the emotion-signpost WARN, narrows hypophora to
a question answered at once, and adds a "thin blow?" WARN in combat (a strike
with no tissue or body mechanics in its paragraph and neighbors; a read, not a
gate). Evidence: commits d558966 to fadc822.

### 2026-11-04 — The WOTR MCP moves to Rust (Isaac's decision; recorded by Claude Code)

Isaac asked for the MCP, verify and most of the architecture in Rust, for speed.
Measured first: the slowness was PyYAML's pure-Python loader (load_rules 1.6 s,
now 0.16 s via CSafeLoader in `build/common.py`) and a quadratic loop in
`build/embed_index.py` search; both fixed in Python. Phase 1 of the port is
done: `rust/` serves stdio MCP (`.mcp.json`), ten tools native, the rest via
`build/mcp_worker.py`; `rust/parity.py` shows all 1,539 cases byte-identical
(every scene through verify with four flag sets). Startup 1 ms vs 476 ms.
Found on the way: verify's floor guard read no character cards (stale path,
fixed in `build/verify.py`; it now sees 55 names, two under eighteen), and
rules packs 1, 2, 4 and 6 each repeat one YAML key (the first value is
silently dropped by both loaders; reported to Isaac, not edited). Next phases:
HTTP + token gate + a key dashboard (named API keys, permissions, which are
online; localhost only), then wiki/scene search, then the writing tools.
Isaac no longer uses Codex or Antigravity.

### 2026-11-04 — The public MCP route is Rust, gated by named keys (Isaac's decision; recorded by Claude Code)

Phase 2 is live: `wotr-mcp-public` runs `rust/target/release/wotr-mcp http` on
8765 and 8767 (the Funnel's `/` and `/ro`); `wotr-mcp-readonly` is retired.
Every request needs an enabled key's token; each key has a preset (full, core,
read-only, custom tool list) applied live. Keys are in
`~/.config/wotr/mcp_keys.json` (0600); the old two secrets were imported as
"Main" (full) and "Read-only (friends)", so no URL changed. Isaac makes,
renames, rotates, disables and watches keys (online = open sessions and a call
in the last 30 min) at http://127.0.0.1:8790/, loopback only. Verified through
the Funnel: Main 58 tools, friends 20, no token 401. Also fixed:
`WOTR_MCP_PUBLIC_URL` in `~/.config/wotr/env` named a dead host (ultron-1), so
audio links from the old route did not resolve; it is ultron now.

### 2026-11-04 — Search tools in Rust; research on Agent Reach (Isaac's decisions; recorded by Claude Code)

`wiki`, `scene_recall` and `scene_context` run natively in `rust/` (phase 3):
the query is embedded with the same bge-small ONNX model and the wotr venv's ONNX
Runtime 1.30 (bit-identical vectors; the system 1.29 differs in the fourth
decimal), against `build/index/` as the sync builds it. Parity: 108 cases
identical; ten differ only in the order of tied results, which Python itself
randomizes (alias sets, numpy's unstable argsort). About twice as fast warm.
`session_start` moved to phase 4 with the table (it needs `table.due`).
`research` no longer uses Antigravity: Agent Reach web search and page reads,
agent-browser (installed at Isaac's request, on the system Chromium) for pages
Agent Reach cannot read, the Superpower Wiki through its MediaWiki API; a bot
check is reported, never passed.

### 2026-11-04 — Table reads in Rust; the writers stay Python (Claude Code's call; Isaac may overturn)

Phase 4: `fronts`, `due`, `roster`, `scene_menu` and `session_start` run natively
in `rust/`, reading `table/*.yaml`. The full parity suite is 1,737 cases with no
mismatch. Every tool that writes (the Ledger, Fronts, roster and session tools,
archive_scene, wiki_write, log_ruling, propose_rule, the character writes) stays
in Python behind the Rust server: a Rust YAML emitter would reformat the data
files, each writer is bound by its git push, and `log_ruling` is the one path into
`RULINGS.md`. Audio and TTS stay in Python (their models are Python-only).

### 2026-11-04 — The writers are Rust too (Isaac's decision; replaces the same day's "writers stay Python")

Isaac asked for the writers to be ported, overturning my call above. Every table
writer, session_end, archive_scene (scenes_to_wiki.py ported in), wiki_write,
log_ruling, propose_rule, create_character, update_character, the inbox tools and
sync_now run natively; 38 of 58 tools. `rust/src/pyyaml.rs` writes table/*.yaml
byte-identically to PyYAML (15,738 awkward rows checked both ways by
`rust/yaml_parity.py`) and reads it with YAML 1.1 typing. `rust/writer_parity.py`
replays 53 writer calls through Python and Rust in two scratch clones pushing to
scratch remotes: replies, 625 files and 34 commit messages identical. Still in
Python: codex lookups (xlsx), audio and narration, the archive audits
(reconcile, pack_impact, timeline, gap_fill, stale_names, cast_index,
scene_brief), the Trello import, and the retired ChatGPT tools.

### 2026-11-04 — All 58 MCP tools run in Rust (Isaac's decision; recorded by Claude Code)

The rest is ported: codex and codex_check (calamine, openpyxl's rows), the audits
(stale_names, scene_brief, gap_fill, timeline, reconcile, pack_impact, cast_index),
trello_cards, convert_character, scene_text, cast_scene, narrate_scene and
narration_status (orchestration only; the TTS engines stay Python programs),
research, and the retired ChatGPT wrappers (stub-tested, never run for real).
Checks on the final build: parity.py 2,425 cases identical; writer, audit and job
replays in scratch clones all identical; a live stdio session over every new tool.

### 2026-11-04 — Narration in Rust (Isaac's decision; recorded by Claude Code)

Isaac chose: Kokoro, Supertonic and the pipeline in Rust; Chatterbox, Qwen3-TTS
and CosyVoice stay Python GPU workers (no Rust path to the AMD card). `wotr-mcp
audio` takes audio_export.py's arguments; narrate_scene starts it. Checked by
`rust/audio_parity.py`: phonemes and tokens identical over 1,442 paragraphs,
Kokoro and Supertonic samples max difference 0, a full scene's MP3 byte-identical,
Chatterbox requests byte-identical (its audio differs run to run in Python too).
Speed is the same (156 s vs 156 s for a scene): inference dominates. MP3 encoding
uses the venv lameenc's LAME 3.100 via libpython3.14; a Python upgrade breaks that
path and narration falls back to WAV.

### 2026-11-04 — Chatterbox Turbo on ONNX + MIGraphX: tested, not ported (Claude Code's finding; Isaac kept PyTorch)

Isaac installed onnxruntime-opt-rocm (MIGraphX) and the official fp32 export
`ResembleAI/chatterbox-turbo-ONNX` (build/models/chatterbox-turbo-onnx/). The Rust
runner `rust/examples/chatterbox_onnx.rs` is correct (speech tokens identical to
the model card's Python example) but slower than the PyTorch worker: RTF 1.16
with the language model on MIGraphX, 1.48 on CPU, 0.71 for PyTorch; read-back WER
equal (0.092). Only the language model runs on MIGraphX (fixed KV cache, io
binding, MIGRAPHX_DISABLE_MLIR=1); the speech encoder (NonZero), decoder
(MultiHeadAttention with bias) and embeddings fail on the EP. Recheck when
MIGraphX gains fp32/fp16 MLIR attention for gfx1201. Chatterbox, Qwen and
CosyVoice stay on PyTorch. Samples: ~/wotr-drafts/chatterbox-onnx-test/.

