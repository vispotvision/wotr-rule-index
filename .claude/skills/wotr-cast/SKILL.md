---
name: wotr-cast
description: "Use when a War of the Realms book, novella or series needs its cast register kept: everyone named on the page with their profession, tier and where they stand, and the side characters who come to matter promoted to a full entry like the lead's. Triggers: a book's foundation, after each chapter, Isaac asking 'who's in this book', 'list the characters', 'who is X again', 'what does X do', 'what's X wearing now', and at archive when a promoted person earns a wiki card. For one new table NPC's want, refusal and voice, wotr-npc owns it; for a full card from art, the character pipeline."
---

# wotr-cast

A book keeps one register of its people: `state.json` `cast` is the source,
and `CAST.md` is the same register for reading, written by
`rust/target/release/wotr-mcp book-memory --slug <slug> --render` and never
by hand. Every person the book names is in it with a profession, because
Isaac asked for the whole cast and what each of them does, kept through the
story the way the main character's sheet is kept (2026-11-07). The table's
counterparts are the roster (`npc_set`) and the wiki cards; the register is
the book's own.

## The entry, by tier

Every entry, every tier: `name` (as the page writes it), `aliases` (bynames,
short forms, titles: so "Ned", "Chapman" and "the Warrior Merchant" are one
person; an alias two people share, such as "the Captain", belongs to
neither), `tier`, `profession` (what they do for a living in their world's
words: "toll-reeve of Tollgarth bridge", "Initiate of the Mercers' hall,
peddler"), `age` (whole years at first appearance; the floor check reads it
for every person in an explicit chapter), `role` (one line: who they are to
this story), `culture`, `first_ch`. Each field is one string, so it reads
whole in a brief and in CAST.md; `arc` is the one list.

| Tier | Who | Adds |
|---|---|---|
| `walk-on` | named once | the entry above; their one exact stroke in `look` |
| `recurring` | back in a second chapter | `look` (one exact stroke), `want` (one line), `bonds` (where they stand with the lead) |
| `major` | earned a want on the page, a fight, a stretch of their own or a turn of the plot | the full entry, as the lead has it |
| `lead` | the POV the outline names | the full entry |

The **full entry**: `look` (the full inventory at first sight: hair by
comparison, face, body, marks, then clothes, armor and weapons piece by
piece with material, color, finish, maker's mark, wear and how they are
worn, Grade and Rarity where seen, R85-1, Table Rule 11); `voice` (one
description and one sample line, the verbal fingerprint, culture and rank
first, R79-5); `want`; `refusal` (the line the person will not cross, and
the hinge that can change it); `lie` (where the want makes one, with its
tell); `kit` (the one concept in a breath, its Path and Wellspring, moves by
name with the chapter each was first used, cost and counter, R82-11, R82-12);
`sheet` (the window: Level, Stage, the Grades in use, skills by Grade, guild
token, class once offered, R84-9); `bonds` (who to whom, and how it stands);
`arc` (one `{ch, line}` per chapter that changed them).

## When the register moves

**At a book's foundation.** Natalie invents the cast the plan needs (R79-11):
each person's want, refusal, lie and voice by `wotr-npc`'s method, a major
person by the character pipeline's (`desktop/CHARACTER_PIPELINE.md`),
`scene_context` on every new name so nobody collides with a wiki card, and
canon people (a carded merchant, a named queen) taken from their cards and
pages, never re-invented. Every person gets a profession and a tier; the
lead and the major people get the full entry before chapter 1 is briefed.

**After a chapter** (book-run's memory step, or `wotr-book` §4). From the
notes' "Cast register" and from the text itself:

1. Add each new person, with the tier the page gives them.
2. For each returning person, change the fields the chapter changed (a new
   coat, a cracked pauldron, a dead man's sword, a token, a Grade a window
   moved) and append their `arc` line. The change also goes in as a fact
   with its quote (`wotr-continuity`), so the old state is never lost.
3. Promote what was earned. A walk-on who returns becomes recurring. A
   recurring person who gets a want on the page, a fight, a stretch of their
   own or a turn of the plot becomes major, and their entry is filled to the
   full standard from the pages: what the pages show goes in, what they do
   not show stays empty, nothing is invented after the fact. A major person
   becomes lead only when the outline gives them a POV.
4. Run `book-memory --render` and `book-memory`; fix every FAIL (a missing
   profession, a tier off the list, a fact about someone not in the
   register) and run it again until it prints none.

**Before a chapter.** The brief carries `book-memory --before <chapter>
--name "<person>"` for each person in the chapter's cast: their entry and
every fact about them from the chapters before it, newest first. For the book's own people that block is their card; the
writer keeps them as it says until a scene changes them.

**When Isaac asks** who is in the book, or who someone is: render CAST.md and
send it (`SendUserFile`), or answer from `book-memory --name` for one person.

**At archive** (`wotr-book` §6). A major person who will outlive the book (a
second book, the table, a recurring rival) gets a wiki card as silent
upkeep (R79-8): built by the character pipeline from the register entry,
filed with `create_character`, and listed once in the archive notes so
Isaac can strike it (R79-11). A recurring or walk-on person who matters to
the table gets a roster line with `npc_set`. Other creators' characters get
register entries and never card edits (R82-47). Isaac's PC follows R81-15:
his wounds and their lasting effects are written onto his card and he
strikes or changes them; new techniques, Level and Stage are offered as
window and card lines for him to keep.

## Mistakes the check catches, and the ones it cannot

`book-memory` FAILs a person-kind fact about someone not in the register, a
missing profession, a tier off the list and an alias two people claim, and
WARNs a missing age, a lead or major entry with empty full-entry fields and a
chapter cast name the register lacks; `book-memory --floor N` FAILs an
explicit chapter with anyone in it who has no age or is under eighteen. It
cannot see these, so they are yours:

- One person entered twice under a byname: merge into one entry and put the
  byname in `aliases`.
- A subject written three ways across chapters: facts use the register name.
- A promotion with the entry left thin: fill it the same day, from the pages.
- Detail invented for a promoted walk-on that the pages never showed: leave
  it empty until a scene shows it.
- The register used as the plan for unwritten chapters: the register says
  what is true so far; the outline says what will happen.
