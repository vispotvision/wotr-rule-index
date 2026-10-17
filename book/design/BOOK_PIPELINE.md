# BOOK_PIPELINE.md — how a War of the Realms book gets written

The short spec of the pipeline as it runs (R79-12, 2026-10-17). The original
n8n design it replaced is kept at `book/design/history/BOOK_PIPELINE_n8n_2026-09.md`.
The operating procedure, step by step, is the `wotr-book` skill.

## The shape

A book lives in `book/<slug>/`: `outline.json` (chapters, beats, cast, place,
hooks), `bible.md` (premise, POV cast, voice note), `state.json` (chapter
summaries, typed facts with quotes, hooks planted and paid), `GATES.md`, and one
folder per chapter (`chNN/`: `brief.md`, drafts and notes per round, findings,
`digest_rN.md`, `final.md`). Chapters run **only when Isaac asks**; the nightly
book timer is disabled.

One chapter is one run of the `book-chapter` workflow
(`.claude/workflows/book-chapter.js`), Claude Code orchestrating:

1. **Foundation** (first chapter only): the planner writes the outline from the
   thread's last archived scene, its Inventory and what is due on the Ledger.
2. **Brief**: one file holding the beat and its hooks, the writer's protocol
   (NATALIE.md adapted to a chapter: no turn-taking; the writer may write his PC,
   R79-1), the rule loadout, the docket, the scene brief, the previous chapter's
   tail, the cast cards or FOW lines, recall, and continuity facts.
3. **Draft**: the writer, about 3,500 words (R79-1), past tense, one free notes
   block.
4. **Check**: `build/verify.py --band set-piece --echoes` (plus `--combat` for a
   fight), `gap_fill` as advisory for fights, and five critics (continuity, POV
   and knowledge, rule compliance, canon, beat and hooks). Every finding quotes
   the draft; an unquoted finding is dropped. The verdict is arithmetic: no FAILs
   passes; FAILs with rounds left revise; otherwise escalate.
5. **Revise**: up to three rounds, kept only if FAILs do not rise.
6. **Digest**: a first-time reader's response and the gate digest for Isaac.
   Nothing is archived here.

## The gate

Isaac approves, rejects with a note, or re-briefs (`wotr-book` §3). An approved
chapter's summary, facts and hooks go into `state.json`; the table hears of it
as silent upkeep, never as proposals (R79-8).

## What the checks hold

The same law as every other piece of WOTR prose: verify_scene's FAILs (em
dashes, antithesis, countdown negation, the Ladder, hard bans) and its reading
WARNs. No rhythm, sentence-length, count or quota checks (R79-3); no declared
lie or misreading per chapter; word count is information. Fights show the full
mechanism (R79-6).

## Assembly

On Isaac's word per approved chapter: `archive_scene` files it in `scenes/`
with its notes, the chapter is placed under the book's heading in
`scenes/ARCS.md`, and `build/arcs_export.py` builds the epub. A .docx only when
he asks.

## Audit

After every fifth chapter and at the end, the book is read against its bible,
outline and facts (`wotr-book` §5).
