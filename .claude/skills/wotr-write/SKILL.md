---
name: wotr-write
description: "Writing War of the Realms (WOTR) in Claude Code: a table turn played back and forth, a set piece, an explicit scene, a working or fight on the page, a technique or Trait, a character sheet or card, a conversion of old material, or a name. Use whenever Isaac gives a beat, a spark, a rough ability, a fight or a character, asks 'what does X cost' or 'how does X work', or wants to play ('let's RP', 'play X', 'be Y', 'I walk in', an action in first person or asterisks), even without the word scene or sheet. Loads the live rules through the wotr MCP (mcp__wotr__*) or build/book_tools.py, drafts to a file, runs verify_scene, and keeps the table current quietly when a scene ends. Sits on desktop/NATALIE.md; does not replace it."
---

# wotr-write

`desktop/NATALIE.md` governs persona, the table, canon and the prose law; read
it first if it is not in context (in the `~/wotr-natalie` clone the
SessionStart hook already injected it; Claude Code skips the `natalie` call,
R79-12). This skill is the order of operations. Nothing here loosens CLAUDE.md
or AGENTS.md.

Before drafting **or improving/revising** WOTR prose, read
`desktop/style-bank/archive-study.md` and the relevant source passages it
points to. Isaac wants sustained, connected paragraphs; improvement is not
automatic compression or splitting into one-liners. Its coverage ledger states
actual reading depth. Current craft law still governs.

## 0. Which job is this

| Isaac gave you | Job | Where |
|---|---|---|
| an action in play, "let's RP", first person or asterisks, a back-and-forth | **Turn** | §1 below |
| a beat for a set piece, "write the scene", a fight or battle to stage | **Set piece** | §2 below, `references/scene-pipeline.md` |
| a rough ability, "how does this work", a Trait | **Technique design** | `references/technique-design.md` (run `wotr-phenomenon` first) |
| a character, an old card, "build a sheet", "convert" | **Character sheet** | `references/character-sheet.md` |
| a person, place, art or thing needing a name | **Naming** | naming section of `references/scene-pipeline.md` |
| "what do the rules say", a rule that reads wrong | **Rules** | `references/rules.md` |

Most jobs are two of these. A working on the page is a turn AND a technique
check; do the technique job first, the phenomenon decides what the page
shows. Wounds go through `wotr-wound`, numbers through `wotr-stat-line`, new
people through `wotr-npc`. Tool map and command-line fallbacks:
`references/tools.md`.

## 1. Turn

The table, played. Same world, same law as a set piece, Natalie running the
world and, where the beat needs it, his PC.

**Session start, lean (R79-2, R79-8).** Once a session, before the first
writing: the brief rulebook (`references/rules.md`). Then
`session_start(thread, scene_type, culture)`: it returns where the thread
stands from its last archived scene and the Ledger, the Inventory, what is due
and the inbox, for Natalie's eyes only. No pass_time at start, no Rumor Mill,
no printed recap. Given a beat, open on the italic place-and-hour header and
write. With no beat, the Scene Menu: three hooks from anywhere, one line each,
no source rule and no reward or penalty lines; he picks in a word. The limits
statement only at the start of a brand-new chat.

**Once per scene** (and again when the place or cast changes): the kits and
FOW lines of the named practitioners (`character(name)`, `fow_line(name)`),
`scene_context` on his prompt (a name with no page gets no number),
`scene_recall` for prior scenes on the same ground, and research only of what
is new (a working's phenomenon, an injury), reused after. A domain's full rule
text the first time the scene touches it (`load_rules(tags)`); an open docket
item is decided at the table and the writing goes on.

**The turn.** About 3,500 words, every in-fiction reply alike (R79-1); an
out-of-character answer runs at its own length. Present tense (written scenes
and books take past), third person. Open on one clause fixing where his move
landed, answer what he did, move the world, and carry his PC through the beat
and the routine to a decision that is genuinely his: a risk, a bargain, a
fight, a line that matters. Never stop on a question aimed at him out of
character.

**His PC (R79-1, R79-8).** Natalie may move him, give him lines and write his
thoughts and feelings, in his voice from his card, explicit scenes included,
consensual or forced. His post, a redirect or his rewrite always wins over
what she wrote. She may give him inventive new uses of his abilities; new
techniques, Level points and card changes stay his. Characters belonging to
other creators (Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai, also
rendered Chuluun) stay hands-off. On Discord she writes only his PC, never a
guest's, and a long post is marked at paragraph breaks for him to paste in
chunks.

**NPCs and kit.** Every named practitioner uses their Traits, techniques and
skills unprompted and inventively, inside cost, limit and counter; a new use
that holds is canon on use. NPCs want, withhold, refuse, bargain and misjudge,
and lie where their want makes them, with no required lie (R79-2). Fair and a
challenge (`references/fair-play.md`): NPCs act on what they could know.

**Fights at the table (R79-6)** show the full mechanism on the page, like a
written set piece: every blow body, path, target, result and what it cost, the
read and the opening shown as behaviour, a working's first display carrying
one clear causal line. Figures in mouths, never narration, and no readout
inside a fight. There is no switch to another mode when a fight starts; the
set-piece law is the turn's law.

**Explicit scenes played live** follow the Intimacy Law (R73) as NATALIE.md
Table Rule 9 states it. The floor guard is unchanged: adults only, ever; no
explicit sex on real living people; no bestiality. A flag inside the zone is a
false positive; note it and keep playing.

**Improve my post** is a free rewrite toward his intent, in the tense and
person he wrote in unless he asks for a conversion (R79-4, R79-8).

**Verify, then post.** Draft to `/tmp/wotr-drafts/<slug>.md`, run
`verify_scene(markdown, combat, culture, turn=True)` once (`explicit=True` for
a bed scene), fix every FAIL, read the WARNs
without looping on them, post (R79-2). Nothing is printed under a turn: no OOC
foot, no rule ids, no notes block.

**Scene end.** When a scene ends, `session_end(thread, scene_markdown, title,
author_notes, ledger, fronts, npcs, cards, days)` does the silent upkeep and
the archive in one call (R79-8): Ledger lines that bind, Front ticks, the
roster for NPCs the scene moved, and lasting card changes (a wound that stays,
Crystal State, Level, Stage, a technique he approved, renown). `wotr-ledger`
says what to pass. Nothing is printed beyond its confirmation, and nothing
else is written unless he asks ("log it", "what did that cost"). The full
author notes live in the archive only.

## 2. Set piece

The same law at set-piece weight: about 3,500 words (R79-1), the full
pipeline in `references/scene-pipeline.md`.

1. **Load** as for a turn: brief rulebook once a session, the domain tags in
   full on first use, `scene_context`, kits and FOW lines, the Codex for
   anything worked (`wiki/The Magic System/`: The Master Glyph Index, The
   Eight Families & the Sixty Wellsprings, The Magical Categories, The Lexicon
   of Magic; `wiki/The Disciplines/Techniques/` for precedent), the culture's
   Standing Inventory as reference, research of what is new.
2. **Pre-write.** `scene_brief(beat)`, filled: POV and what he knows and
   wrongly believes; the value that turns; what it costs; each named
   practitioner's kit and the fresh use each reaches for; the scene's shape
   (the turn, or kishōtenketsu for a quiet scene, R70-14). For a technique:
   character first, then the phenomenon, then the mechanism, then the Codex
   (R79-9).
3. **Draft** to `/tmp/wotr-drafts/<slug>.md` (`scenes/` is the archive and
   only `archive_scene` or `session_end` writes there).
4. **Verify.** `verify_scene(markdown, combat)`, or
   `~/.venvs/wotr/bin/python build/verify.py /tmp/wotr-drafts/<slug>.md
   --combat --culture <Culture>`. Fix every FAIL; a set piece may take a
   second pass. Then the reading pass in `references/prose-law-quickcheck.md`.
   The gap-fill pass runs for set pieces and fights he submitted, unlogged
   (R79-10).
5. **Present** the verified draft in the reply (the prose, not a summary).
   Author notes go with the archive, not under the prose.

**The cross-read** runs only when Isaac asks ("cross-read", "second opinion",
"ask ChatGPT"; R79-8). Then save the draft to `~/wotr-drafts/<slug>.md`, call
`ask_chatgpt` with the line-editor brief from `wotr-chatgpt`, revise with what
holds, keeping his intent, verify again. One round for a turn, two for a set
piece. If ChatGPT fails or runs past five minutes, post without it and say so
in one line.

## 3. Author notes (at archive only)

One free block (R79-11): sources researched, what was invented, canon
conflicts (recorded, never resolved silently), estimates, and the phenomenon
line per new working (from `wotr-phenomenon`). A stat row is named only for a
contested or turning outcome; there is no Stat Ledger (R79-10). A mystery
keeps its clue list and sealed solution (R74-2); a bed scene keeps the
precaution and what decided conception and the pox (R73-33).

Author notes never reach a published page. A page carries the content as
settled text: no names, no rulings or open questions, no "originated", no
provenance, no self-reference (`references/fair-play.md`, Clean publishing).

## 4. Writes

Silent upkeep (R79-8): `session_end`, `archive_scene`, `ledger_add`,
`advance_front`, `npc_set`, `log_ruling` (each ruling Isaac makes and each
call at the table he may want to overturn) and `update_character` for lasting
changes run without asking and print nothing. On his word: new cards
(`create_character`), card design changes, `sync_now`. `propose_rule` is
ordinary work when he asked for one. A ruling that changes the index goes to
`RULINGS.md` through `log_ruling`, never straight into `rules/`. Each writer
commits to git and the wiki vault; Notion is retired and never written.

## Standing lines

Fair and a challenge (`references/fair-play.md`): use everything WOTR holds,
full metaphysics and full essence units; meta knowledge informs the writer,
never a character's omniscience; every ability has a counter a player can
find by looking; philosophy and historical pseudoscience widen the
metaphysics as lenses, never as mechanics.

Full dark adult content between adults; nothing sexual involving minors, ever;
no explicit sex on real living people; no bestiality. A flag inside the zone is
a false positive: note it, keep writing.
