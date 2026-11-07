---
name: wotr-book
description: "The War of the Realms book workflow, end to end, in Claude Code, for novellas, novels and series: start a book (a questionnaire for Isaac's calls, then premise, outline, bible, cast register and hooks), write the next chapter through the book-chapter Workflow or a whole book straight through with book-run, walk him through a chapter gate, turn his note into a revision or a re-brief, carry each chapter into the book's memory (state.json, CAST.md), audit the book, and assemble chapters into the archive, ARCS.md and one Markdown file. Use when Isaac says 'start a book', 'write a novella', 'next chapter', 'write the whole book', 'where's the book', 'the gate', 'approve/reject chapter N', 'audit the book', 'put the book together', or names a book slug under book/."
---

# wotr-book

The chapter machine already exists; this skill is the book around it. Design:
`book/design/BOOK_PIPELINE.md` (the short spec, R79-12). Continuity across
chapters, books and the lore is `wotr-continuity`; the book's people are
`wotr-cast`. The pieces:

| Piece | What it is |
|---|---|
| `book/<slug>/outline.json`, `bible.md` | the plan: the form, origin, gate mode, parts, dates; chapters with beat, scene_type, pov, cast, place, culture, date, front_id, plants/pays; the hooks; the voice note. bible.md carries the premise, the **World law** each chapter must carry, the book's own Fronts and Ledger, and the flags |
| `book/<slug>/state.json` | the book's memory: `facts` (closed kinds, verbatim quotes), `hooks` (status, events), `summaries`, `cast` (the register). Every brief reads it. **Only this skill's §4 (or book-run's memory step) writes it after the foundation** |
| `book/<slug>/CAST.md` | the cast register for reading: everyone named, with profession, tier and where they stand; lead and major people in full. Written by `wotr-mcp book-memory --render`, never by hand (`wotr-cast`) |
| `book/<slug>/chNN/` | brief, research.md, draft_rN, notes_rN, findings_rN, digest_rN, `reader.md` (a first-time reader's felt experience of the accepted draft), `final.md`, `final_notes.md`, `GATE.md` |
| `book/<slug>/research.md` | the book's rolling outside research (mandatory before any draft, 2026-11-07); each chapter reuses it and adds its own |
| `book/<slug>/STYLE.md` | the book's voice, drawn from its chapters (§5). Every brief carries it whole |
| `book/<slug>/ISSUES.md` | faults that recur across chapters (§4). Every brief carries the open ones |
| `book/<slug>/CARRY.md` | what the audits carry forward: outline rows corrected to fit the pages, and lines later chapters must honor (§5). Every brief carries it whole |
| `book/<slug>/DIGEST.md`, `digest/` | one careful reading per final chapter, for the audits (§5) |
| `.claude/workflows/book-chapter.js` | one chapter: foundation (optional), brief with research, draft, a deterministic check plus six critics, up to 3 revise rounds, the reader, the gate digest. Writes under `book/` only, never commits |
| `.claude/workflows/book-run.js` | a span of chapters straight through: each chapter, then its memory step, then an audit at every fifth chapter, each part's end and the last |
| `wotr-mcp book-next` | what comes next, and the gate record (`gates.json`, `GATES.md`). Gates: the outline's `gates`, else chapters 1-3, every fifth (8, 13, ...) and the last. In `gate_mode: "block"` an undecided written gate blocks everything after it; in `"review"` the book is written straight through and `book-next` answers `review` with the gates that wait |
| `wotr-mcp book-memory` | the memory check (exit 1 on any FAIL; every failure prints a line starting FAIL), `--name "<person>"` (one person's register entry and facts), `--before N` (only the chapters before N count: a brief and a rewrite never see their own or later chapters), `--render` (CAST.md), `--floor N` (an explicit chapter: everyone in its cast has an age, all eighteen or more), `--purge N` (a rewrite starts clean). In review mode it is the only check between chapters |
| `wotr-book.timer` | **disabled** since 2026-10-17 (R79-12), and `build/systemd_setup.sh` no longer enables it: chapters run when Isaac asks. `build/book_dispatch.sh --slug <slug>` exists for a manual run |

Standing: `sources/`, `rules/`, `wiki/`, `table/` are not this skill's to
edit by hand. A chapter is archived on Isaac's word (an approved gate or his
say-so); the table upkeep that follows is silent (§6). Never approve a gate
for him. Natalie writes Isaac's PC in a book only when the outline names him
in `pc` (R79-1). Characters belonging to other creators (Haruki, Dova'Kan,
Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai, also rendered Chuluun) stay hands-off
(R79-1). Commit only the book's files, one chapter's decision per commit,
after `git pull --rebase --autostash` (another session may write here).
Finished work goes to him as a Markdown file (`SendUserFile`, 2026-11-07).

## First: where is it

```bash
rust/target/release/wotr-mcp book-next --slug <slug> --json     # --slug may be left off when only one book has an outline
rust/target/release/wotr-mcp book-memory --slug <slug>          # the memory check
cat book/<slug>/GATES.md book/<slug>/DISPATCH.md 2>/dev/null
systemctl --user is-active wotr-book.service                    # "active" = a manual dispatch is mid-chapter; touch nothing under book/<slug>
```

Say it plainly: chapters written of total, the action and why, the gate or
gates waiting, and whether the memory check is clean. Then pick the move.

## 1. Start a book

**Isaac's calls go to him as a questionnaire** (his direction, 2026-11-07):
AskUserQuestion, four questions a batch, the recommended option first with
"(Recommended)", a sample passage or shape in each preview. Save the
questions to `imports/drafts/<slug>-questionnaire/questions.json` and his
answers to `answers.json` beside it after every batch. Ask only what is
genuinely his and still missing; everything else is Natalie's call, stated
in the bible's flags. The usual calls:

- **Form**: a **novella** (eight to fifteen chapters in three movements, one
  spine, a cast kept tight) or a **novel** (twenty to forty chapters in
  parts, with subplots and a second POV allowed at marked breaks). Form is
  never set by a word count; chapters vary in length on purpose (R80-13).
- **Origin**: a **table** book continues a thread from its archived scenes;
  an **original** book (a new protagonist, or any thread with no archived
  scenes, which since the 2026-10-18 reset is most) is built from the
  premise and canon.
- **Gate mode**: **review** (write it all through, then he reads each gate)
  or **block** (stop at each gate for his word).
- **Series**: the series slug and the book's number; a sequel names the
  `previous_book`.
- The premise's open choices: place and era (the year count and a start
  date in the real calendar, R85-2), the lead's age, name and culture, what
  drives them, their one wild concept, the ending, who is lost and who is won.

The slug is short kebab-case and must not exist under `book/`.

**The foundation is done in this session**, not inside the Workflow, so the
plan is built from his answers and he can read it before or after the
chapters, as his gate mode says. Follow the Foundation prompt in
`book-chapter.js` (it is the spec of the three files and their schema):

1. **Research first** (mandatory, NATALIE.md Outside resources): the trades,
   places, law, money and medicine the premise touches (`lookup wikipedia`,
   `research`), the lead's power (`superpower`, `vsbattles`, the touchstone
   wikis, `pinterest` for how it looks and moves), and a vocabulary pass
   (`datamuse`, `wiktionary`). Findings go to `book/<slug>/research.md`.
2. **Canon reads**: the wiki pages for every place, people and institution
   in the premise, the culture's Standing Inventory, `scene_context` on the
   premise and on every new name (so nobody collides with a card), and the
   live law the loadouts miss (`load_rules` on `worldbuilding items stats
   naming character-sheet`, every part): that becomes bible.md's **World
   law**, each line with its rule id or page, and the outline's `extra_tags`.
3. **The cast register**, built with `wotr-cast`: everyone the plan names,
   each with a profession; the lead and major people in full.
4. **The spine**: every chapter ticks a named Front (the table's, or for an
   original book the book's own, written into bible.md with id, want,
   segments and the tick each chapter makes) and pays what is due; hooks
   carry plant and due chapters with 3-5 keywords; "mention is not
   advancement"; each chapter has a date. A sequel carries the previous
   book's open hooks (new due chapters), the register's end state and the
   facts still in force into bible.md's "## Carried from <previous>".
5. Write `outline.json`, `bible.md`, `state.json`; run `book-memory
   --render` and `book-memory` (it must print no FAIL); show him the chapter
   list with one-line beats, the cast register, the hooks and the voice note
   (as a Markdown file); commit `book/<slug>/` ("Book <slug>: foundation").

Then chapter 1 runs as §2 with `do_foundation: false`.

## 2. Write the next chapter, or the whole book

On demand only (R79-12). Values come from `book-next --json` (slug, thread,
front_thread, culture, target_words) and `outline.json`; do not start a second
run while one is going.

- **One chapter** (block mode, or a rewrite): when `book_next --json` says
  `write` or `rewrite`, invoke
  `Workflow({ name: "book-chapter", args: { slug, chapter, thread, culture, target_words, front_thread, do_foundation: false } })`.
  Then §4 by hand before the next brief.
- **Straight through** (review mode, or when he asks for a span): invoke
  `Workflow({ name: "book-run", args: { slug, thread, culture, front_thread, from, to, total, part_ends, words: {<chapter>: <estimate>} } })`.
  Each chapter runs through book-chapter, then book-run's memory step (§4)
  and, at every fifth chapter, each part's end and the last, the audit (§5).
  It stops at the first chapter that does not pass (an escalation at the
  brief, a crash, or FAILs left after the revise rounds) and says which, so
  nothing is built on a chapter with a FAIL in it. Fix the cause here: a
  docket item decided at the table and logged with `log_ruling` as an agent
  ruling (R79-2); a memory FAIL fixed in state.json; a chapter that kept FAILs
  given an instructed round (§3) with the findings as the note, then carried
  into memory (§4). Then re-run from the next chapter.

Both run an hour or more per chapter in the background. A `rewrite` re-runs
the chapter from a fresh brief, and **the Workflow does not read the reject
note**, so before a rewrite the note must already be in `outline.json` (§3,
re-brief).

## 3. The gate

Read `chNN/GATE.md`, then `chNN/final.md` in full. Send him both as files
(`SendUserFile`). Present: the verdict and FAIL/WARN counts per round; the
reader's first paragraph and any CONVERGES line (a place where the reader
drifted and a critic found a fault: the strongest signal on the page); each
remaining FAIL with its quote and the one-line fix; beat delivered or not;
hooks planted/paid; the Front ticked; the people new to the register; what
he is deciding. In review mode, several gates wait at once: put them to him
as a questionnaire, one question per gate chapter, the four answers below as
its options. His call, one of four:

- **Approve**: `wotr-mcp book-next --slug <slug> --approve N --note "..."` on his word, then §6 when he wants it archived.
- **Instruct** (a prose note: "fix the ears line", "Yoko speaks less"): a
  revise-only pass here, under the reviser's frozen rules from
  `book-chapter.js` (same POV, events, order, ending unless named; no new
  characters; at least 85% of the words, no ceiling; at least 70% of
  dialogue lines and paragraphs kept). His note is the only finding. Save as
  the next `draft_rN.md`/`notes_rN.md`, run
  `rust/target/release/wotr-mcp verify chNN/draft_rN.md --culture <C> --echoes [--combat] [--explicit]`,
  copy to `final.md`/`final_notes.md`, append an "Instructed round" section
  to `GATE.md`, redo §4 for the chapter (facts whose quotes changed), and
  put it back in front of him. Still his gate.
- **Re-brief** (the beat was wrong: "the clerk asks the king, not the
  Bench"): edit that chapter's row in `outline.json` (beat, cast, place,
  plants/pays), show him the diff, then `wotr-mcp book-next --slug <slug> --reject N --note "..."`
  on his word. The next run rewrites from the new row, and its memory step
  starts with `book-memory --purge N` so the rejected version leaves the
  memory; the brief reads only the chapters before N (`--before N`). Once the
  rewrite lands, `book-next` shows the gate as `rewritten` and waiting, and
  the next rejected chapter comes up. If he says the beat
  is wrong but not what is right, offer two or three replacement beats that
  are truly different choices as a questionnaire, each with what it costs
  downstream in its description (hooks moved, the Front tick, what the next
  chapter must now do), and let him pick. Do not recommend one.
- **Drop**: `wotr-mcp book-next --slug <slug> --drop N --note "..."` on his word; the outline row
  stays, the dispatcher moves past it, and `book-memory` stops counting the
  chapter (it WARNs any facts left under it, to remove). Say which hooks that chapter carried,
  so he can move them.

A non-gate chapter needs no decision to continue, but it still goes through
§4 before the next brief is built, or the book forgets it. Check this each
time you are asked for status: `book-memory` FAILs any `final.md` whose
chapter has no summary.

## 4. Carry it into the book's memory (book-run does this per chapter; by hand otherwise)

This is what keeps chapter 9 consistent with chapter 2. From `final.md` and
`final_notes.md`, update `state.json` (edit with `jq` or a load-and-dump,
never by hand-splicing; it stays valid JSON):

- `summaries`: `{"ch": N, "title", "summary"}`, the notes' "Summary for
  continuity" as written (at most 200 words).
- `facts`: each durable fact the chapter establishes, as
  `{"ch": N, "subject", "kind", "fact", "quote"}`. The **subject** is the
  person's register name (state.json `cast`), or the place's or object's
  name. The **kind** is one of the closed list `book-memory` enforces:
  `fact, time, location, object, money, debt, promise, name, look, gear,
  wound, healed, death, move, skill, level, stage, grade, class, title, vow,
  bond, knows, reader_knows, lie, renown, profession`. The **quote** is one
  sentence copied exactly from `final.md`: no quote, no fact. A lie a
  character tells is `lie`, so later chapters do not treat it as true.
  Knowledge splits two ways: `knows` (subject = the character, fact = what
  they now know) and `reader_knows` (the reader saw it, the named character
  did not); the continuity critic fails a character acting on a
  `reader_knows`. A window that moved a Grade, Level, skill or Stage is
  `grade`, `level`, `skill` or `stage`, with the window line as the quote; a
  guild token is `title`; a wound stays open until a `healed` fact names it
  in a `heals` field (the wound fact's own words); a death that does not hold
  is followed by a `returned` fact. A new
  fact that contradicts an older one does not replace it: add it, and put
  both quotes in front of him (a slip to fix by instruct, or a turn the book
  means).
- `cast`: the notes' "Cast register" into the register, by `wotr-cast`:
  new people added with a profession and tier, returning people updated,
  promotions filled to the full entry, one `arc` line per chapter a person
  changed in.
- `hooks`: planted, advanced or paid as the notes' hook lines show **and as
  the text shows** (each open hook's keywords looked for in `final.md`), each
  as an event `{"ch", "kind", "quote"}`; `"paid_ch": N` when paid.

Then `ISSUES.md`: read this chapter's `findings_rN.json` (last round) and
GATE.md against the earlier chapters'. A fault seen in one chapter is a
finding; the same fault in a second chapter is an issue (the same echo word,
the same flat middle, one character's voice drifting, a scene type that keeps
running long). One `## <issue>` per fault: what it is, the evidence (quotes
and chapter numbers), its scope, how badly it hurts the reading, `status:
open`. Add new evidence to an existing entry rather than making a second one.
When a later chapter no longer shows it, set `status: resolved (ch N)` and
keep the entry.

Then `wotr-mcp book-memory --slug <slug> --render` and `wotr-mcp book-memory
--slug <slug>`: fix every FAIL in state.json and run it again until it prints
none. Show him the added rows, new people and promotions, and any new or
resolved issue in one short list; commit ("Book <slug>: ch NN into memory").

## 5. Audit (every fifth chapter, each part's end, and the last; book-run does it)

Reports, and corrects the plan where it contradicts the pages; edits no
chapter. First bring `DIGEST.md` up to date, so no single context has to
hold the whole book: for each `final.md` newer than its digest, one agent in
parallel reads that chapter alone and writes `digest/chNN.md`: the beats
(3-6), time markers, who appears and what each does and wants, places,
relationships that shifted, setups planted and payoffs paid, and two or three
quotes that show the prose at its best and worst. DIGEST.md is those files
in chapter order. The audit reads DIGEST.md, state.json and CAST.md, and
opens a chapter only to check a quote.

Then write `book/<slug>/AUDIT_chNN.md`:

- **Hooks**: overdue (`due_ch` passed, not paid: critical); dormant (no
  event in more than 3 chapters: warn); open hooks over 12 in a novel or 8
  in a novella: warn.
- **Cast**: a register person silent for more than 5 chapters (warn); a
  `death` fact followed by that subject acting (critical); a register entry
  that has drifted from the pages; a person who has earned promotion and
  not got it.
- **Sag**: three chapters in a row with no Front ticked and no hook advanced.
- **Continuity**: read every summary and fact in order; list cross-chapter
  contradictions with both quotes and chapter numbers. Contradictions cluster
  between 35% and 65% of the book: read that band closest. `book-memory`'s
  output goes in as it prints.
- **Voice**: rewrite `STYLE.md` from the chapters: the few principles the
  narration actually runs on (sentence rhythm and how it moves under strain,
  how deep the interiority goes, what the POV notices first, how dialogue
  carries subtext, where the humor lives), each with one or two quoted
  examples and the chapters that show it. Principles, not a checklist: a
  writer should take it in one read. A habit the book would not want copied
  is a tic and goes to ISSUES.md, not STYLE.md. Say where the voice drifted
  or flattened across chapters, with quotes.
- **Carry-forward**: an unwritten chapter whose outline row now contradicts
  the pages (a fact, a count, a place, who knows what) gets that row
  corrected to fit them and nothing else in its beat changed; each edit
  (chapter, before, after, the quote that forced it) goes under "## Outline
  changes" in `CARRY.md` for his review. Everything else later chapters must
  honor goes under "## Carry", one line each with the chapter it binds.
- At the end only: from DIGEST.md, review the whole book once as a critic and
  once as a teacher of fiction, with specific, actionable notes by chapter.
  Then read it once through each lens the law claims: the blend (R70-1, as
  R78-4 leads it with dark shonen and cultivation; R70-3, the POV's culture
  tilting the mix), the tone (THE TONE in NATALIE.md, R80-1 read through
  C-185), the abilities' north star
  (R82-2), the headline feel (R83-1), and The Weak Grade as the prose model:
  where the book keeps that promise and where it doesn't. Then the
  first-time reader from book-chapter.js, over the whole book: where it held
  and where it sagged, the middle closest.

He reopens a chapter by instruct (§3) or re-brief; the audit never does.

## 6. Assemble (on his word, per approved chapter)

1. `archive_scene(title="<chapter title>", markdown=final.md, author_notes=final_notes.md)`:
   writes the scene file under `scenes/`, publishes the Scene Archive page, commits and
   pushes. One chapter per call, in order; wotr-ops has the archiving order.
2. `scenes/ARCS.md`: add the new file under `## <book title>`, in chapter
   order, creating the H2 if missing (hand edit; there is no `arcs_place` tool
   yet). Commit.
3. **The book as one Markdown file**: a title page, the cast list from
   CAST.md, then each final.md in order, saved as
   `book/<slug>/<Title>.md` and sent with `SendUserFile` (2026-11-07). The
   glossary of the book's invented and system words goes at the end
   (R79-11). The epub comes from `build/arcs_export.py`, run when he wants
   it. A .docx only on request (R79-11).
4. Narration (`cast_scene`, `narrate_scene`) is a separate job on his word.
5. The facts the chapter established reach the table as silent upkeep once
   it is archived (R79-8): one `session_end` call for the Ledger lines that
   bind, the Front ticks and the roster for NPCs it moved (`wotr-ledger`),
   and `wotr-continuity`'s R82-1 write-back to the cards, with a wiki card
   for a register person who earned one (`wotr-cast`), listed once in the
   archive notes for him to strike (R79-11). Isaac's PC follows R81-15: his
   wounds and their lasting effects are written and he strikes or changes
   them; new techniques, Level and Stage are offered as window and card lines
   for him to keep. A book chapter is canon only once archived.

## When a chapter goes wrong in the machine

The Workflow's files tell you where it stopped: no `brief.md` = brief stage;
a brief that starts with ESCALATE = a docket item or a memory FAIL;
`draft_r0.md` but no `findings_r0.json` = checks; no `GATE.md` = digest.
Resume with the Workflow's `resumeFromRunId` in the same session, or delete
nothing and let the next run start the chapter over (it overwrites). A
dispatcher failure is in `build/book_dispatch.log` and `journalctl --user -u
wotr-book.service`.
