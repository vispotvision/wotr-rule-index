# BOOK_PIPELINE.md — how a War of the Realms book gets written

The short spec of the pipeline as it runs (R79-12, 2026-10-17; refit to the
R82-R85 lore, novellas, novels and series on 2026-11-07). The original n8n
design it replaced is kept at `book/design/history/BOOK_PIPELINE_n8n_2026-09.md`.
The operating procedure, step by step, is the `wotr-book` skill; keeping a
book's facts and people straight is `wotr-continuity` and `wotr-cast`.

## The shape

A book lives in `book/<slug>/`: `outline.json` (form, origin, gate mode,
parts, dates; chapters with beat, cast, place, culture, date and hooks),
`bible.md` (premise, the World law each chapter carries, the book's own
Fronts and Ledger, voice note, flags), `state.json` (chapter summaries, facts
of a closed list of kinds with verbatim quotes, hooks planted and paid, and
the cast register), `CAST.md` (the register for reading), `research.md`,
`GATES.md`, and one folder per chapter (`chNN/`: `brief.md`, `research.md`,
drafts and notes per round, findings, `digest_rN.md`, `reader.md`,
`final.md`). Chapters run **only when Isaac asks**; the book timer is
disabled and setup no longer turns it back on.

**Forms.** A novella runs eight to fifteen chapters in three movements; a
novel twenty to forty in parts. Neither is set by a word count, and chapters
vary in length on purpose (R80-13). **Origins.** A table book continues a
thread's archived scenes; an original book is built from the premise and
canon. **Series.** A sequel names its `previous_book` and carries that
book's open hooks, cast end state and live facts into its bible.

**Isaac's calls** go to him as questionnaires (his direction, 2026-11-07);
the foundation is built in session from his answers.

One chapter is one run of the `book-chapter` workflow
(`.claude/workflows/book-chapter.js`), Claude Code orchestrating; a span runs
through `book-run` (`.claude/workflows/book-run.js`), which adds the memory
step and the audits between chapters:

1. **Foundation** (in session, once): research, canon reads, the cast
   register, then outline, bible and state.
2. **Brief**: the memory check (a FAIL escalates), the beat and its hooks
   and Front tick, the writer's protocol (NATALIE.md adapted to a chapter,
   the World law, the window format, precedence lines), the rule loadout
   (part 1, the book's extra tags, pinned older rows), the docket, the scene
   brief, **the mandatory research** (a datamuse pass and every fitting
   source, saved to `research.md`), the previous chapter's tail, each cast
   member's state in this book, recall, continuity, the open issues and the
   audits' carry-forward.
3. **Draft**: the writer, after The Weak Grade (and the fight exemplars,
   lexicon, signatures and state sheet for a fight); past tense, third
   person; notes with Sources, the Cast register, Windows and Dates.
4. **Check**: `wotr-mcp verify --echoes` (plus `--combat` for a fight and
   `--explicit` for an explicit chapter), `gap_fill` as advisory for fights,
   the research and window checks, and six critics (continuity and cast
   state, POV and knowledge, rule compliance, canon with the retired-lore
   list, beat and hooks, prose and fight review). Every finding quotes the
   draft; an unquoted finding is dropped. The verdict is arithmetic: no FAILs
   passes; FAILs with rounds left revise; otherwise escalate.
5. **Revise**: up to three rounds, judged FAILs first: a round whose FAILs
   fell is kept; at least 85% of the words stay, with no ceiling.
6. **Digest**: a first-time reader's response and the gate digest for Isaac.
   Nothing is archived here.
7. **Memory** (book-run, or `wotr-book` §4 by hand): summaries, facts, the
   cast register and hooks into state.json; ISSUES.md; `wotr-mcp book-memory
   --render` writes CAST.md, and `wotr-mcp book-memory` must print no FAIL
   before the next brief.

## The gate

`gate_mode: "block"` stops at each gate chapter for Isaac's word;
`"review"` writes straight through and leaves the gates for him to read
after. He approves, instructs, re-briefs or drops (`wotr-book` §3). The
table hears of an archived chapter as silent upkeep, never as proposals
(R79-8).

## What the checks hold

The same law as every other piece of WOTR prose: verify_scene's FAILs (em
dashes, antithesis, countdown negation, the Ladder, hard bans, British
spelling, the floor in explicit chapters, where `book-memory --floor N` also
checks every register person in the chapter has an age of eighteen or more)
and its reading WARNs; the full
mechanism in fights (the Blow Card and the Working Card, DEPTH AND
EXPLANATION); windows as bracketed blocks (R84-1, R84-2); gear as a flex
(R85-1); the real calendar (R85-2); no retired lore. No rhythm,
sentence-length, count or quota checks (R79-3); word count is information.

## Assembly

On Isaac's word per approved chapter: `archive_scene` files it in `scenes/`
with its notes, the chapter is placed under the book's heading in
`scenes/ARCS.md`, the page is written back to the cards (R82-1), and the
book goes to him as one Markdown file (title page, cast list, chapters,
glossary). `build/arcs_export.py` builds the epub when he wants it; a .docx
only when he asks.

## Audit

At every fifth chapter, each part's end and the last, the book is read
against its bible, outline, facts and register (`wotr-book` §5); an outline
row the pages have contradicted is corrected, and the change is logged in
`CARRY.md` for Isaac.
