# Character sheets and cards

Tags: character-sheet, stats, naming, codex. **The one skeleton is
`desktop/templates/CHARACTER_CARD_TEMPLATE.md`** (R79-9): copy it, fill the
head, and keep the sections the character actually has. This file is the
procedure around it, not a second template.

New cards go under Volume I Character Cards. `create_character` writes a new
card to the wiki vault and git, on Isaac's word; `update_character` carries
lasting changes as silent upkeep at a scene's end (R79-8: a wound that stays,
Crystal State, Level, Stage, a technique he approved, renown) and design
changes on his word. Check `character(name)` and `grep -ril "<name>" wiki/`
before creating; never duplicate a page (wotr-ops has the no-second-card
procedure).

## Rungs, not gates (R79-9)

Roster entry, short card, full card. A card is made when it is needed, and a
full card when Isaac asks or the character recurs. Nothing waits on a rung.

## Before writing

A card's abilities pass the fairness checks in `references/fair-play.md`;
its vows, failure terrain and tells are written so a player who reads the card
can find them.

1. `character(name)` if a card exists. `convert_character(source)` for old
   material (a Trello export, an old sheet): it returns the conversion brief on
   the current system; work from the brief, not the old text.
2. Naming pass (five strata; Büri register dead; a name only has to sound
   right for its culture, R79-7; see scene-pipeline.md).
3. Numbers by field (R79-10): Fracture of Worlds for system law, tables and
   names (mirrored in `wiki/The Magic System/`: Fracture of Worlds — The Living
   System, The Sixteen Stages, Tier Grade, Bands & the Aether Shell); the Stat
   Sheet for the character's figures; the card for person facts and wherever
   the sheet is silent. Resolve by that order and move on. A missing figure is
   derived from the Fracture of Worlds tables, written plainly with no mark,
   canon on use; a source value beats it on contact. No pending fields.
   Formulas that must compute are recomputed (1 EU = 1 MJ; AU/s = Flux Density
   × η); bands and ladders are typical ranges, and a card's outlier stands.
4. Stage names are Fracture of Worlds' (Murmuring, Welling, Ascension,
   Flourishing, Splintering, Glory, Refraction, Transcendence, Invocation,
   Realization, Dissonance, Emanation, Principality, Zenith, Revelation, Apex),
   never a card's Ignition or Temper.

## Mechanical anchors (memory; confirm against source before use)

- Level max 500, five Bands of 100: I Mortal Foundation (Stages I to IV), II
  Awakened (V to VII), III Sovereign (VIII to X), IV Mythic (XI to XII), V
  Absolute (XIII to XIV).
- Tier Grades on raw stat: Hollow 1 to 10 / F 11 to 25 / E 26 to 50 / D 51 to
  100 / C 101 to 175 / B 176 to 275 / A 276 to 400 / S 401 to 550 / SS 551 to
  725 / SSS 726 to 950 / X 951 to 1200 / EX 1201 to 1500 / EX+ 1501 and up.
- A Primary Stat is the total of its eight Sub-Stats; points buy Sub-Stats
  only; the Primary's Grade is read off the mean. Throne carries no ceiling and
  sits outside the Dominion total.
- Nine Tiers of Standing replace the lettered Coherence Bands as the public
  scale; eta is set by Aether Class (R78-10). Hollow and F confer no rank.
- Eight Essence Families: Caloria, Fulguria, Vectoria, Spatium, Materia,
  Vitalia, Fluxia, Limina.
- Soul Crystal tiers: Dormant, Awakened, Harmonic, Resonant, Radiant,
  Sovereign, Crystallized Soul, Absolute Crystal.
- Domain: seed at VII, first stable Domain at VIII, Realm at IX to X, ambient
  at XI to XII, Continuum-registered at XIII, indistinguishable from the
  character at XIV.

## What the card owes (R79-9)

- **The head, required:** the one-screen block at the top of the template
  (name and moment, stat line, combat grammar, aura and sound, stack, releases
  and bonded weapon, Traits and techniques by name with tell and counter, the
  voice line). Natalie fights from it.
- **The sections below are a menu,** filled with what the character actually
  has, with no character cap. Stats carry the Primaries and the Sub-Stats in
  use; the rest are derived when a scene needs them.
- **The voice block is a menu** with two required slots: a sample line and the
  speaker type. Gloss rights is a voice trait for who explains aloud in
  dialogue, not a gate on narration. Release calls and technique names are
  called in English or the speaker's own tongue, as the character would
  (R79-6).
- **Dropped:** the arc-kind taxonomy. A next-gate line only when the character
  is near a gate.
- **Figures set when play reaches them:** mastery marks, chant cuts, vows,
  Readiness.
- **Abilities** follow `references/technique-design.md`: one name and one
  paragraph each (R76), holding mechanism, cost and one fair counter within
  reach at its own Stage; limit and tell where they exist; the before, during
  and after triad only for signatures. Drain as how long a working lasts from
  full, EU kept on the card as the source of truth (R79-10).

Formatting: bold markdown headers, bold field labels, fields as short prose
lines, not nested bullets.

## Author notes for a sheet

One free block, in the chat (R79-11): what is new, canon conflicts (recorded,
not resolved silently), the phenomenon line per new technique, the estimates
and where each came from. The published card carries the figures as settled
text: no "originated", "pending ruling", estimator, author or process note,
ever.


## Art-first path (Isaac, 2026-10-31)

A character built from Isaac's art follows `desktop/CHARACTER_PIPELINE.md`: read the image
for the physical inventory, age and culture, mood and voice, and power hints; invent nothing
the image does not show; derive the numbers from the concept and state them; a voice is one
description and one sample line; the lore carries sealed secrets; hand back a full draft card.
Abilities on the card go through `desktop/ABILITY_PIPELINE.md`.
