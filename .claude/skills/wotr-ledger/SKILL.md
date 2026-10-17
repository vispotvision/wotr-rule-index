---
name: wotr-ledger
description: "Silent background upkeep and cost accounting for War of the Realms. Use when a WOTR scene or set piece ends, whenever Isaac says 'wrap', 'log it', 'what did that cost', 'session end', or when a scene has ended and nothing has been recorded yet. Also use mid-session when a scene inflicts a wound, a debt, a witness, a lost object or a reputation change that must persist. It quietly keeps the Ledger, the Fronts and the NPC roster current and archives the scene; nothing is printed to Isaac unless he asks. One pass, nothing forgotten, nothing shown."
---

# wotr-ledger

The world remembers what the PC did to it. Since 2026-10-17 there is no
scene close (R79-2, refined the same day by Isaac's coverage answers): when
a scene ends Natalie keeps the table current in the background and archives
the scene, and none of it is printed, proposed item by item or waited on.
Isaac reads the archive and the wiki when he wants to; "log it" or "what did
that cost" gets him the full account in plain OOC. For a scene already
archived (Discord `/scene save`, or anything in `scenes/` with nothing kept),
run the same silent pass on it; the judger is retired (R79-8).

## 1. At scene end, silently

`session_end(thread, scene_markdown, ledger=..., fronts=..., npcs=...)` in
one call, then `archive_scene`. Pass only what binds:

- **Ledger lines that bind** (`ledger` items, `ledger_add` fields): the dead
  and who saw; wounds that outlast the scene and reserve left low (the tell
  rung reached, Drafts and their crash, R78-10); debts owed and owing; objects
  gained, lost or damaged; renown per audience (public, army, sects, guilds;
  warrants, bounties, epithets, R78-10); what comes due and roughly when.
  Each line carries a thread and a story date or a named trigger (R72-22).
- **Front ticks** (`fronts` items): a Front his acts moved; story days passed
  in the scene go in `days` or `story_date`, which tick the calendar as
  `pass_time` does (R72-20). A new pressure is `add_front` with a four to six
  step clock.
- **Roster** (`npcs` items): doing-now and stands-with for each NPC the scene
  moved (R72-26); a lie only where the NPC's want made them tell one (R79-2).

Leave out what will not matter next scene. A trifle is not a Ledger line.

## 2. Archive

`archive_scene(title, markdown, author_notes)`, titled per
`scenes/MANIFEST.md` (wotr-ops has the ordering for a transcript cut into
several scenes). The full author notes live here and only here (R79-2).
Texture, places, words and minor people invented in the scene stand as canon
once archived, and Isaac may strike them (R79-4); no Standing Inventory entry
is owed. It commits and pushes to the wiki vault; `sync_now` only if he asks.

## 3. Rulings

`log_ruling(rule_id, ruling)` for anything Isaac decided at the table and for
any agent ruling Natalie made, with the rule id; the index takes it in via
`RULINGS.md`, never by editing `rules/` from here. `propose_rule` for a craft
rule you originated. Quietly, like the rest.

## 4. When he asks

"Log it", "what did that cost" or "show me the Ledger": answer OOC at its own
length from `due()`, `fronts`, `roster` and the lines just written. The Stat
Ledger (going in, stressed, spent, coming out, per named practitioner, R14-7)
is written into the archived scene's author notes, and read back on request.

## Not any more

No State of Play rewrite (the wiki State of Play pages are retired and
historical). No proposals item by item. No Inventory entry demand. No OOC foot
or close block under the last turn. No pack-fold question.
