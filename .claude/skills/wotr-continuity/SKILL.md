---
name: wotr-continuity
description: "Use when War of the Realms lore or a person's state must stay consistent across chapters, books and the wiki: before drafting a chapter or scene where a named person, place, object or debt returns; after a book chapter is final, to record what it established as facts with verbatim quotes; when a draft contradicts an earlier page, a card, the wiki or a rule; when Isaac asks 'is X alive', 'what does X know', 'where is X', 'when was that', 'didn't we say...'; before starting a sequel; and at archive, for the R82-1 write-back of the page to the cards. The book's people and professions are wotr-cast; the Ledger, Fronts and roster at scene end are wotr-ledger; archiving order and scene indexes are wotr-ops."
---

# wotr-continuity

Retention is the record of what the pages made true, each item with the
sentence that made it so, kept where the next writer reads it, and checked by
a tool rather than by memory. Three scales, one method:

| Scale | The record | Read with | Checked by |
|---|---|---|---|
| A book | `book/<slug>/state.json` facts, hooks, summaries and the cast register | `wotr-mcp book-memory --slug <slug> --name "<person>"` | `wotr-mcp book-memory --slug <slug>` (exit 1 on any FAIL) |
| A series | the previous book's state.json end state, carried into the sequel's bible | the sequel's bible "## Carried from <previous>" | the same check on the sequel |
| The lore | archived scenes, cards, the roster, the Ledger, the rule index, CONFLICTS.md | `scene_context`, `scene_recall`, `character`, `roster`, `due`, `timeline`, `rule` | the nightly (`validate`, `reconcile`) and the canon critic |

Which source wins is the canon hierarchy in `desktop/NATALIE.md`: Isaac's
word and RULINGS.md, then the canon source documents, the rule index,
archived scenes, cards, the rest of the wiki, internal logic. A book's own
memory is canon for that book; it becomes the lore's only once the chapter is
archived (wotr-book §6).

## Before a draft: the continuity pack

1. `scene_context` on the beat: every name with its card or page, the prior
   scenes on the same ground, and the names with no page (a new name is
   checked here so it does not collide with an existing card).
2. For each person in the scene: in a book, `book-memory --before <chapter>
   --name "<person>"` (the state as of that chapter's start: their register
   entry and every fact from the chapters before it, newest first: look and gear, open
   wounds, moves already used, the sheet, what they know and do not, bonds,
   where they are, alive or dead); at the table, `character` and the roster
   line. That state is fact for the draft until a scene changes it.
3. Time: the previous scene's date line and the real calendar (R85-2; the
   year count is the world's own, Munahi is February 29, Auren's day the
   twelfth of every month). Elapsed time is arithmetic, written in the notes.
4. What is owed: the hooks due soon, `due` on the Ledger, the book's
   `CARRY.md` lines.

## After a final: facts with their sentences

Each durable fact the page establishes becomes one row,
`{"ch", "subject", "kind", "fact", "quote"}`:

- **subject**: a person's register name (or card title at the table), or the
  place's or object's name. One name per person, always the same one.
- **kind**: one of the closed list (`book-memory` enforces it): `fact, time,
  location, object, money, debt, promise, name, look, gear, wound, healed,
  death, move, skill, level, stage, grade, class, title, vow, bond, knows,
  reader_knows, lie, renown, profession`. A lie told is `lie`, never a plain
  fact. What a person now knows is `knows`; what the reader saw and they did
  not is `reader_knows`, and acting on it is a continuity FAIL. A window line
  is the quote for a `grade`, `level`, `skill` or `stage` that moved. A
  `healed` fact names the wound it closes in a `heals` field (the wound
  fact's own words), or it closes nothing; a death that does not hold (a rare
  canon return at its price) is followed by a `returned` fact.
- **quote**: one sentence copied exactly from the accepted final, never from
  an unaccepted draft. No quote, no fact.

A new fact that contradicts an older one is added beside it, never over it,
and both quotes go to Isaac: either a slip (fixed in the chapter by an
instructed round) or a turn the book means. Then run `book-memory` and fix
every FAIL; it also WARNs an open hook whose keywords all appear in a
chapter that logged no event for it. After any later edit to a final (an
instructed round, a spelling sweep), run it again: an edit can strand a
quote.

## When the page and canon disagree

1. Find the governing source by the hierarchy. A draft that contradicts a
   higher source is a slip: fix the draft.
2. Two canon sources that contradict each other are a conflict: write a row
   in CONFLICTS.md with both quotes, never resolving it silently; then rule
   it openly as an agent ruling under the hierarchy with `log_ruling`,
   naming its grounds, and apply it (CLAUDE.md, "Nothing waits on Isaac").
3. A wiki line that contradicts the R82 to R85 law is stale, not canon
   (R83-13): new writing follows the law, and the page goes on the rewrite
   list.

**The retired lore** new writing keeps out: the draw, mains and standpipes;
Essence Typology; Families of Wellsprings; the Büri register and Ajiin
(`stale_names` sweeps them); guns, powder or firearms in any era; the
Imperial Age for any date before 800 IC; Stannvaard, Dawi or Ketsuen as
living states, or the Kingdom of Nalūn; Whitemere or the Stack before they
exist. Archived scenes stay as written (R84-3); a returning old name is what
people once called it.

## A sequel

Before its foundation, read the previous book's state.json and CAST.md and
write into the new bible's "## Carried from <previous>": every hook not
paid (with a new due chapter or a decision to let it lie), each register
person's end state (the newest fact per kind), the debts, vows and promises
still open, and the date the last chapter ended on. The sequel's register
starts from that end state, and its outline names `previous_book`.

## At archive: the write-back

R82-1: what is on the page in an archived scene is written back to the card
at scene end. This skill owns that write-back; the rest of the scene-end
upkeep (the Ledger, the Fronts, the roster) is one `session_end` call by
`wotr-ledger`, and the archiving order and scene indexes are `wotr-ops`. For
each person the scene changed: read `character NAME`, change only the
fields its facts touch (wounds that stay, gear, a move's first use, Level,
Stage, Grades, token, bonds), bump `as_of`, and file it with
`update_character`. When a roster person's `knows` or `lied_about` changes,
remember that `npc_set` replaces those lists whole: pass the merged list,
never only the new item. Other creators' cards are never touched (R82-47).
Isaac's PC follows R81-15: his wounds and their lasting effects are written
and he strikes or changes them; new techniques, Level and Stage are offered,
not written.

## What the night-watch audits showed

The 2026-10 audits of a pre-reset book found fourteen critical
contradictions, and every one came from a way of keeping memory this skill
now closes: free-text kinds and subjects (the checks never matched),
quotes taken from an unaccepted draft, an outline that kept promising what
the pages had already contradicted (now corrected at each audit, CARRY.md),
a draft with a FAIL kept as final (the revise loop now judges FAILs first),
hook events logged from the writer's notes and missed in the text (the
check scans the text), and quotes stranded by a later spelling sweep (run
the check after every edit).
