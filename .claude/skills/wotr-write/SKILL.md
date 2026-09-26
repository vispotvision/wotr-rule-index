---
name: wotr-write
description: "Writing War of the Realms (WOTR) in Claude Code: the order of operations for a table turn, a set piece, an explicit scene, a working or fight on the page, a technique or Trait, a character sheet or card, a conversion of old material, or a name. Use whenever Isaac gives a beat, a spark, a rough ability, a fight or a character, or asks 'what does X cost' or 'how does X work', even without the word scene or sheet. Loads the live rules through the wotr MCP (mcp__wotr__*) or build/book_tools.py, drafts to a file, verifies with verify_scene or build/verify.py, and writes nothing to Notion or git without his word. Sits on desktop/NATALIE.md; does not replace it."
---

# wotr-write

`desktop/NATALIE.md` governs persona, table rules and canon hierarchy; read it
first if it is not in context (in the `~/wotr-natalie` clone the SessionStart
hook already injected it). This skill is the order of operations. Nothing here
loosens CLAUDE.md or AGENTS.md.

## 0. Which job is this

| Isaac gave you | Job | Reference |
|---|---|---|
| a beat, a PC action, "what happens", a spark, nothing | **Turn or set piece** | `references/scene-pipeline.md` |
| a rough ability, a fight beat, "how does this work", a Trait | **Technique design** | `references/technique-design.md` (run `wotr-phenomenon` first) |
| a character, an old card, "build a sheet", "convert" | **Character sheet** | `references/character-sheet.md` |
| a person, place, art or thing needing a name | **Naming** | naming section of `references/scene-pipeline.md` |
| a turn-by-turn scene, "let's RP", first person or asterisks | **Play** | switch to `wotr-rp` |

Most jobs are two of these. A working on the page is a turn AND a technique
check; do the technique job first, the phenomenon decides what the page shows.
Wounds go through `wotr-wound`, numbers through `wotr-stat-line`, new people
through `wotr-npc`.

## 1. Load before you write, every time

Tool map and command-line fallbacks: `references/tools.md`. Never invent a
number; it comes from `fow_line`, the card, or `wiki/The Magic System/`. If
none has it, it is an estimate inside the documented range and labelled so.

1. **Session start** (first job of a session): `session_start(POV, type,
   culture)`: loadout, Docket, what is due, Fronts, State of Play.
2. **Rules**: the loadout's tags, `prose-law` always for prose.
   `load_rules(tags)` then `check_docket(tags)`. Newer rule governs where two
   overlap. An open docket item that would change the piece: one line to
   Isaac, wait. A CONFLICTS entry: never resolve it.
3. **Lorebook**: `scene_context(beat text)` (the command line takes a file). Every name
   comes back with its page or flagged pageless. A pageless name gets no number.
   `scene_recall("<moment>")` for prior scenes on the same ground.
4. **Codex** for anything worked: `wiki/The Magic System/` (The Master Glyph
   Index, The Eight Families & the Sixty Wellsprings, The Magical Categories,
   The Lexicon of Magic), `wiki/Techniques/` for precedent.
5. **FOW line** for every named practitioner: `fow_line(name)`. Check the
   thread's State of Play for which card is in play when there are two.
6. **Standing Inventory** for the culture: `desktop/inventories/<culture>.md`.
7. **Research once each**, before a fight or working: the real phenomenon, the
   real weapon, injury or physiology, the nearest anime or CRPG precedent
   (WebSearch). Sources go in the author notes.

## 2. Pre-write

`scene_brief(beat)` and fill every field it returns. Minimum: POV and what he
knows, wrongly believes, and what the reader knows that he does not; the value
that turns; what it costs; the one thing he notices that you do not explain;
the NPC lie that stays uncorrected; the two Inventory items the scene touches;
which of the four explaining voices carry mechanism (never more than two per
engagement). For a technique: refusal, wound, conviction, then phenomenon, then
Codex. Never the other way round.

## 3. Draft to a file

Write the draft to `/tmp/wotr-drafts/<slug>.md` (not the repo; `scenes/` is the
archive and only `archive_scene` writes there). Length band: conversational 300
to 700, standard 700 to 1,500, set piece 2,500 floor. Stop at Isaac's next
decision. Never move his PC or any flagged character (Haruki, Dova'Kan, Gorgi,
Ma'Kovu, Fushigi, Xhem, Sonzai/Chuluun).

## 4. Verify, then present

`verify_scene(markdown, combat)`, or
`~/.venvs/wotr/bin/python build/verify.py /tmp/wotr-drafts/<slug>.md --combat
--culture <Culture> --band <band>`. Fix every FAIL, read every WARN, re-run
until clean. Then the reading pass in `references/prose-law-quickcheck.md`.
Never a single pass; never presented, then caught. `voice_check(character,
line)` for any line that must sound like its speaker.

Present the verified draft in the reply (the prose, not a summary), then the
author notes.

## 5. Author notes (set piece, sheet, technique; abbreviated on a turn)

Author notes are for the chat only and never reach a published page. A page
carries the content as settled text: no names, no rulings or open questions,
no "originated", no provenance, no self-reference (`references/fair-play.md`,
Clean publishing).

In this order, every heading present even if it reads "none":
1. **New in this piece**: everything new, one line each.
2. **Canon conflicts**: surfaced, never resolved.
3. **Phenomenon line** per working (from `wotr-phenomenon`).
4. **Added by the gap-fill pass**, when Isaac submitted a fight or working.
5. **Combat floor audit**: HEMA skeleton, three-layer hit at first display and
   finisher, stated fault, POV body on the page.
6. **Stat Ledger** per named practitioner (R14-7): going in (Stage, Band,
   Tier of Standing, Aether Class, Crystal State); stats stressed and the §3
   row each outcome traced to; EU spent, tenth-of-reserve crossed or not;
   coming out and any Threshold Event risk; what heals by next scene.
7. **Narrative ledger**: injuries, debts, reputation, who saw what.
8. **Rule ids** that most constrained the piece. **Sources** researched.
9. **Open questions** for Isaac.

## 6. Close: proposals, not writes

`archive_scene`, `ledger_add`, `advance_front`, `npc_set`, `log_ruling`,
`create_character`, `update_character` commit to Notion and git. In Claude
Code they run on Isaac's word only, one call per thing he approves. Offer the
close as a list (run `wotr-ledger`); for a scene already archived, `judger`.
`propose_rule` is ordinary work when he asked for one. A ruling he makes in
play goes to `RULINGS.md` in an index session, never straight into `rules/`.

## Standing lines

Fair and a challenge (`wotr-write/references/fair-play.md`): use everything WOTR holds, full metaphysics
and full essence units; meta knowledge informs the writer, never a character's
omniscience; every ability passes the five fairness checks and has a counter a
player can find by looking; philosophy and historical pseudoscience widen the
metaphysics as lenses, never as mechanics.


Full dark adult content between adults; nothing sexual involving minors, ever;
no explicit sex on real living people; no bestiality. A flag inside the zone is
a false positive: note it, keep writing.
