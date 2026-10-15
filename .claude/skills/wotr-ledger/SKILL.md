---
name: wotr-ledger
description: "Session close and cost accounting for War of the Realms. Use at the end of any WOTR session or set piece, whenever Isaac says 'wrap', 'log it', 'what did that cost', 'session end', or when a scene has ended and nothing has been recorded yet. Also use mid-session when a scene inflicts a wound, a debt, a witness, a lost object or a reputation change that must persist. It fills the narrative Ledger and the Stat Ledger, advances a Front, rewrites State of Play, files rulings and proposals, enters new Inventory texture and archives the scene, every write as a proposal Isaac approves item by item. One pass, nothing forgotten."
---

# wotr-ledger

The world remembers what the PC did to it. This skill is the close, run as a
form so nothing is left to memory. In Claude Code the close is a list of
proposals: draft every field below, show Isaac, and make each write call only
for the items he approves, by name. `session_end(thread, scene_markdown)`
drafts candidates and logs the session (the Ledger ages from it): call it
once, at a real close. For a scene already archived (Discord `/scene save`,
or anything in `scenes/` with no close), use `judger` instead.

## 1. Narrative Ledger (`ledger_add` on approval, one line per category)

- **The dead**: name, how, who saw.
- **Injuries and reserve**: per character, the wound brief's Ledger line;
  EU spent, the lowest tell rung reached (half, quarter, tenth: R78-10), any maxing out, Drafts drunk and their crash, stack layers run; what heals by
  next scene and what does not.
- **Debts**: owed and owing, to whom, in what (coin, labour, salt, meat).
- **Objects**: gained, lost, damaged. A damaged Inventory signature item is
  a plot event; say so.
- **Renown**, per audience (public, army, sects, guilds; R78-10): who now knows what about him, what they will say, warrants and bounties posted, epithets given.
- **Witnesses**: who saw a working, and what they could read of it.
- **Due**: what comes due and roughly when (a fire's length, the Thin Weeks).

## 2. Stat Ledger (R14-7, per named practitioner)

Going in: Stage, Band, Tier of Standing, Aether Class, Crystal State.
Stressed: the stats the scene used and the §3 row each outcome traced to.
Spent: EU, lowest tell rung reached, Drafts and crash, stack layers. Coming out: Crystal State and any
Threshold Event risk. Healed by next scene: ___. Every figure sourced or
marked estimate.

## 3. Fronts (`pass_time` for story days, R72-20; `advance_front` only for a move his acts sped, on approval)

Which Front moved, which consequence fired, the PC's part in it or none.
If a new pressure appeared, propose `add_front` with a four to six step clock.

## 4. State of Play (a full rewrite, proposed, not appended)

Where he is, what he holds, who is with him, what he believes that is wrong,
the open threads in one line each, the last physical image of the scene.
Written so a cold session can start from it alone.

## 5. Rulings and proposals

`log_ruling(rule_id, ruling)` for anything Isaac decided at the table, with
the rule id; the index takes it in via `RULINGS.md` in a later index
session, never by editing `rules/` from here. `propose_rule` for anything you
originated, marked pending, no author name. Docket page updated.

## 6. Inventory

Every piece of texture invented in play entered into its culture's Standing
Inventory now, or it does not exist. Any rough-to-converted term into the
lexicon (R16-4).

## 7. Archive

`archive_scene(title, markdown, author_notes)` on his word, titled per
`scenes/MANIFEST.md` (wotr-ops has the ordering for a transcript cut into
several scenes). It commits and pushes; the hourly sync carries Notion, so
`sync_now` only if he asks.

## 8. Ask once

Whether to fold a pack this session. Once. Then stop.
