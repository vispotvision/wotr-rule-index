---
name: wotr-book
description: "The War of the Realms book workflow, end to end, in Claude Code: start a book (premise, outline, bible, hooks) and put the outline in front of Isaac, write the next chapter through the book-chapter Workflow, walk him through a chapter gate, turn his note into a revision or a re-brief, carry each approved chapter into the book's memory (state.json summaries, facts, hooks), audit the book every fifth chapter and at the end, and assemble approved chapters into the archive, ARCS.md and the epub. Use when Isaac says 'start a book', 'next chapter', 'where's the book', 'the gate', 'approve/reject chapter N', 'audit the book', 'put the book together', or names a book slug under book/."
---

# wotr-book

The chapter machine already exists; this skill is the book around it. Design:
`book/design/BOOK_PIPELINE.md` (the n8n version; this repo runs the Claude
Code version). The pieces:

| Piece | What it is |
|---|---|
| `book/<slug>/outline.json`, `bible.md` | the plan: chapters with beat, scene_type, pov, cast, place, front_id, plants/pays; the hooks; the voice note |
| `book/<slug>/state.json` | the book's memory: `facts`, `hooks` (status), `summaries`. Every brief reads it. **Nothing but this skill writes it after the foundation.** |
| `book/<slug>/chNN/` | brief, draft_rN, notes_rN, findings_rN, digest_rN, `reader.md` (a first-time reader's felt experience of the accepted draft), `final.md`, `final_notes.md`, `GATE.md` |
| `book/<slug>/STYLE.md` | the book's voice, drawn from its approved chapters (§5). Every brief carries it whole |
| `book/<slug>/ISSUES.md` | faults that recur across chapters (§4). Every brief carries the open ones |
| `book/<slug>/DIGEST.md` | one careful reading per final chapter, for the audits (§5) |
| `.claude/workflows/book-chapter.js` | one chapter: foundation (optional), brief, draft, 10 checks, up to 3 revise rounds, gate digest. Writes under `book/` only, never commits |
| `build/book_next.py` | what comes next, and the gate record (`gates.json`, `GATES.md`). Gates: chapters 1-3, then every fifth (8, 13, ...), and the last. An undecided written gate blocks everything after it |
| `wotr-book.timer` (02:00) | `build/book_dispatch.sh`: headless Claude runs `book_next --json` and, on write/rewrite, the Workflow; leaves `book/<slug>/DISPATCH.md`; commits `book/` |

Standing: `sources/`, `rules/`, `wiki/`, `table/` are not this skill's to
edit. No `archive_scene`, `ledger_add`, `advance_front`, `npc_set`,
`log_ruling` except on Isaac's word, one call per thing he approves. Never
approve a gate for him. The PC (Sodoku Moto in kharven-year) does what the beat
says and nothing beyond it; flagged characters decide nothing a beat does not
name. Commit only the book's files, one chapter's decision per commit, after
`git pull --rebase --autostash` (another session and the 02:00 run write here).

## First: where is it

```bash
~/.venvs/wotr/bin/python build/book_next.py --json            # add --slug <slug> for a second book
cat book/<slug>/GATES.md book/<slug>/DISPATCH.md 2>/dev/null
systemctl --user is-active wotr-book.service                 # "active" = the dispatcher is mid-chapter; touch nothing under book/<slug>
```

Say it plainly: chapters written of total, the action and why, the gate
waiting if any, when the timer next fires. Then pick the move.

## 1. Start a book

Ask only what is missing: thread (POV name), Fronts thread (culture word),
culture, premise in his words (or "from where the table stands"), chapter
count, words per chapter (3,500 default). The slug is short kebab-case and
must not exist under `book/`.

Do the foundation **in this session**, not inside the Workflow, so the outline
reaches Isaac before a chapter is written (the design's first gate). Follow the
Foundation prompt in `book-chapter.js` exactly (read it there, it is the
spec): the reads, the spine rules (every chapter ticks a named Front; pays
what the Ledger says is due; hooks carry plant and due chapters with 3-5
keywords; "mention is not advancement"), and the three files it writes. Then
show him: the chapter list with one-line beats, the hooks with plant/due
chapters, the voice note. Revise on his notes until he says go. Commit
`book/<slug>/` ("Book <slug>: foundation").

Chapter 1 then runs as in §2 with `do_foundation: false`.

## 2. Write the next chapter

Only when `book_next --json` says `write` or `rewrite` and the service is not
active. Two ways; ask which if he did not say:

- **Tonight**: nothing to do; the 02:00 run takes it.
- **Now**: invoke the Workflow tool (this skill is his opt-in):
  `Workflow({ name: "book-chapter", args: { slug, chapter, thread, culture, target_words, front_thread, do_foundation: false } })`,
  values from `book_next --json` and `outline.json`. It runs an hour or more
  in the background; do not start a second. If it returns `escalate` at the
  brief stage, that is a docket item: show it, stop.

A `rewrite` re-runs the whole chapter from a fresh brief, and **the Workflow
does not read the reject note.** So before a rewrite, the note must already
be in `outline.json` (see §3, re-brief).

## 3. The gate

Read `chNN/GATE.md`, then `chNN/final.md` in full. Present:
the verdict and FAIL/WARN counts per round; the reader's first paragraph and any CONVERGES line (a place where the reader drifted and a critic found a fault: the strongest signal on the page); each remaining FAIL with its quote
and the one-line fix; the declared lie and misreading; beat delivered or not;
hooks planted/paid; the Front ticked; what he is deciding. Offer the prose
itself if he wants to read it here. Then his call, one of four:

- **Approve**: `book_next.py --approve N --note "..."` on his word, then §4.
- **Instruct** (a prose note: "fix the ears line", "Yoko speaks less"): a
  revise-only pass here, under the reviser's frozen rules from
  `book-chapter.js` (same POV, events, order, ending unless named; no new
  characters, lie or misreading; 85-115% words; at least 70% of dialogue lines
  and paragraphs kept). His note is the only finding. Save as the next
  `draft_rN.md`/`notes_rN.md`, run
  `build/verify.py chNN/draft_rN.md --band set-piece --culture <C> --echoes [--combat]`,
  copy to `final.md`/`final_notes.md`, append an "Instructed round" section to
  `GATE.md`, and put it back in front of him. Still his gate.
- **Re-brief** (the beat was wrong: "the clerk asks the king, not the
  Bench"): edit that chapter's row in `outline.json` (beat, cast, place,
  plants/pays), show him the diff, then `book_next.py --reject N --note "..."`
  on his word. The next run rewrites from the new row. If he says the beat is
  wrong but not what is right, offer two or three replacement beats that are
  truly different choices, each with what it costs downstream (hooks moved,
  the Front tick, what the next chapter must now do), and let him pick. Do not
  recommend one.
- **Drop**: `book_next.py --drop N --note "..."` on his word; the outline row
  stays, the dispatcher moves past it. Say which hooks that chapter carried,
  so he can move them.

A non-gate chapter needs no decision to continue, but it still goes through
§4 before the next brief is built, or the book forgets it. Check this each time
you are asked for status: any `final.md` whose chapter has no entry in
`state.json` summaries is owed §4.

## 4. Carry it into the book's memory (after approve, and for every non-gate chapter)

This is what keeps chapter 9 consistent with chapter 2. From `final.md` and
`final_notes.md`, update `state.json`:

- `summaries`: `{"ch": N, "title", "summary"}`, the notes' "Summary for
  continuity" as written (at most 200 words).
- `facts`: each durable fact the chapter establishes (an injury, who knows
  what, an object moved, a death, a promise, time elapsed, a number) as
  `{"ch": N, "subject", "kind", "fact", "quote"}`; the quote is a verbatim
  sentence from `final.md`. No quote, no fact. The declared lie is recorded
  with kind `lie` so later chapters do not treat it as true. Knowledge splits
  two ways: kind `knows` (subject = the character, fact = what they now know)
  and kind `reader_knows` (the reader saw it, the named character did not).
  The continuity critic fails a character acting on a `reader_knows`.
  A new fact that contradicts an older one does not replace it: add it, and
  put both quotes in front of him (a slip to fix by instruct, or a turn the
  book means).
- `hooks`: planted, advanced or paid as the notes' hook lines show, with the
  sentence; `"paid_ch": N` when paid.

Then `ISSUES.md`: read this chapter's `findings_rN.json` (last round) and
GATE.md against the earlier chapters'. A fault seen in one chapter is a
finding; the same fault in a second chapter is an issue (the same echo word,
the same flat middle, one character's voice drifting, a scene type that keeps
running long). One `## <issue>` per fault: what it is, the evidence (quotes
and chapter numbers), its scope, how badly it hurts the reading, `status:
open`. Add new evidence to an existing entry rather than making a second one.
When a later chapter no longer shows it, set `status: resolved (ch N)` and
keep the entry.

Show him the added rows and any new or resolved issue in one short list;
commit ("Book <slug>: ch NN into memory"). JSON stays valid: load and dump with Python, never hand-splice.

## 5. Audit (after every fifth chapter, the middle third every third, and the end)

Reports; edits no chapter. First bring `DIGEST.md` up to date, so no single
context has to hold the whole book: for each `final.md` newer than its
DIGEST.md section (or missing from it), spawn one Agent in parallel that reads
that chapter alone and returns a careful reading: the beats (3-6), time
markers, who appears and what each does and wants, places, relationships that
shifted, setups planted and payoffs paid, and two or three quotes that show
the prose at its best and worst. Replace those sections in DIGEST.md, in
chapter order. The audit reads DIGEST.md and state.json, and opens a chapter
only to check a quote.

Then write `book/<slug>/AUDIT_chNN.md`:

- **Hooks**: overdue (`due_ch` passed, not paid: critical); dormant (no
  event in more than 3 chapters: warn); open hooks over 12: warn.
- **Cast**: a POV-cast member with no fact for more than 5 chapters (warn); a
  `death` fact followed by that subject acting (critical).
- **Sag**: three chapters in a row with no Front ticked and no hook advanced.
- **Continuity**: read every summary and fact in order; list cross-chapter
  contradictions with both quotes and chapter numbers. Contradictions cluster
  between 35% and 65% of the book: read that band closest.
- **Voice**: rewrite `STYLE.md` from the approved chapters: the few
  principles the narration actually runs on (sentence rhythm and how it
  moves under strain, how deep the interiority goes, what the POV notices
  first, how dialogue carries subtext, where the humour lives), each with one
  or two quoted examples and the chapters that show it. Principles, not a
  checklist: a writer should take it in one read. A habit the book would not
  want copied is a tic and goes to ISSUES.md, not STYLE.md. Say where the
  voice drifted or flattened across chapters, with quotes.
- At the end only: from DIGEST.md, review the whole book once as a critic and
  once as a teacher of fiction, with specific, actionable notes by chapter.
  Then read it once through each lens the table claims (Martin's POV
  discipline, Abercrombie's brutality and cost, Tolkien's elegiac reach, Lord
  of the Mysteries' mystic register): where the book keeps that promise and
  where it doesn't. Then the first-time reader from book-chapter.js, over the
  whole book: where it held and where it sagged, the middle closest.

He reopens a chapter by instruct (§3) or re-brief; the audit never does.

## 6. Assemble (on his word, per approved chapter)

1. `archive_scene(title="<chapter title>", markdown=final.md, author_notes=final_notes.md)`:
   writes the scene file under `scenes/`, publishes the Scene Archive page, commits and
   pushes. One chapter per call, in order; wotr-ops has the archiving order.
2. `scenes/ARCS.md`: add the new file under `## <book title>`, in chapter
   order, creating the H2 if missing (hand edit; there is no `arcs_place` tool
   yet). Commit.
3. The epub and docx come from `build/arcs_export.py`, which the hourly sync
   runs into Drive. `sync_now` only if he wants it now.
4. Narration (`cast_scene`, `narrate_scene`) is a separate job on his word.
5. The table's own Ledger and Fronts (`ledger_add`, `advance_front`) for what
   the chapter changed: propose them through `wotr-ledger`; a book chapter is
   canon only once archived.

## When a chapter goes wrong in the machine

The Workflow's files tell you where it stopped: no `brief.md` = brief stage;
`draft_r0.md` but no `findings_r0.json` = checks; no `GATE.md` = digest. Resume
with the Workflow's `resumeFromRunId` in the same session, or delete nothing
and let the next run start the chapter over (it overwrites). A dispatcher
failure is in `build/book_dispatch.log` and `journalctl --user -u
wotr-book.service`.
