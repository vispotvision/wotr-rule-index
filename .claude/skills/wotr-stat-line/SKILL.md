---
name: wotr-stat-line
description: "Pull the Fracture of Worlds loadout for a War of the Realms character: Level, Band, Stage by source name, Path, Tier Grades, Aether Class and the eta it sets, Soul Crystal tier and state, Essence Family, Wellspring harmonisations, EU and AU/s, Traits, Domain, Resonant Pairs. Use before ANY scene with a named practitioner, before designing a technique, when Isaac asks 'what Stage is X', 'can X do Y', 'who wins', or any question with a number in it. Sources by field (R79-10): Fracture of Worlds for system law, tables and names; the Stat Sheet for a character's figures; the card for person facts and wherever the sheet is silent. Resolve by that order and move on; a missing figure is derived from the Fracture of Worlds tables, written plainly, canon on use."
---

# wotr-stat-line

The stats decide (Pack Fourteen §3), out of sight (R79-10). This skill
produces the FOW line the adjudication is decided from, with provenance per
figure for Natalie's eyes.

## Sources, by field (R79-10)

Read each field from the source that owns it, resolve by this order and move
on; nothing is flagged and left waiting.

- **System law, tables and names:** Fracture of Worlds, mirrored as
  `wiki/The Magic System/` (Fracture of Worlds — The Living System, The
  Sixteen Stages, Tier Grade, Bands & the Aether Shell); the PDF, if handed
  one, via `pdftotext`.
- **A character's figures:** the Stat Sheet. `fow_line(name)`
  (mcp__wotr__fow_line, or `build/book_tools.py fow_line`) reads what is on
  file. Where a character has two cards in play, the thread's latest archived
  scene says which.
- **Person facts, and wherever the sheet is silent:** the card
  (`character(name)`, or its file under `wiki/`).
- WOTR_COMPLETE_MAGIC_SYSTEM.docx: derivative, never sole authority.

Formulas that must always compute are recomputed (1 EU = 1 MJ; AU/s = Flux
Density × η). Bands and ladders are typical ranges; a card's outlier stands.
A missing figure is derived from the Fracture of Worlds tables, written
plainly with no mark, canon on use; a source value beats it on contact. No
pending fields.

## The line (every field; a derived figure where the sources are silent)

- Level / Band / Stage (Fracture of Worlds name only) / Path
- Tier Grade per Primary the scene will stress, and the Stage's sustainable
  ceiling (see `references/fow-anchors.md`)
- Tier of Standing
- Aether Class and the eta it sets (R78-10)
- Stack line: the Grade on the card, the two-Grade cap, and every self-boost
  in use counted against it (vows, releases, Drafts, strain lifts); only
  outside help (allies, arrays, Domains) sits outside it; items work at their
  own Tier (R79-10)
- Releases and bonded weapon, aura colour and signature sound
- Soul Crystal tier and Crystal State going in (Refined, Fractured,
  Overgrown, Crystallized)
- Essence Family
- Wellspring harmonisations and the Sub-Stats they alter
- EU reserve (the card's source of truth) and how long each working lasts
  from full, Flux Density, AU/s against the local Aetheric Density (R79-10)
- Traits (each with the Lattice property it alters), Domain tier,
  Attraction or Obsession sustainment
- Resonant Pairs reached
- Path gates: what this character structurally cannot do

Each figure carries its source in brackets for Natalie's eyes: [Stat
Sheet], [card], [FOW p.], [derived]. Where two sources differ, the field's
owner wins and the line says which was used.

## The question map (§3)

Pressure: Stage gap and Dominion. Measure and reaction: Dexterity. Armour:
Ardency Penetration against tier. The read: Gnosis. Duration and push:
Tempering. The draw: Harmonics against Density. Wounds: Vitality, ATLS on
top. Crystal damage: Resilience. Cannot: Path gate. The Grade of the stat in
use decides a contest; the Stage gap governs Pressure and the upset limit;
ties break on the read, then what is left to spend, then the ground (R79-10).
Name the row when Isaac asks "who wins" out of character; on the page and in
the archive notes a row is named only for a contested or turning outcome.

## Where the figures may appear (Style Law, R70)

In a fight, figures live in mouths, never narration, and there is no readout
inside a fight (R79-6). Outside a fight, the body first, the figure a line after
in the same beat (R70-89), and narration states the figures the POV holds: his own last reading, a card he
has seen, what he was told (R70-83; R14-4-SUBSTAT retired). The bearer reads
his own sheet in his Soul Crystal at thresholds, exact and blind to wounds and
to others; instruments read everyone else (R70-78), and any practitioner feels
another's Band and rough Stage, Gnosis setting how close (R70-79). Ranked
practitioners talk exact numbers and argue builds in dialogue; commoners round
(R70-93), in a fight as in talk. Readouts: inline by default, a set-off block only at
a re-assay that moves something, a breakthrough or an arc's end (R70-80); none inside a
fight, only at a breakthrough, a re-assay or an arc's end (R78-6); `Stage V, Splintering`, numeral
beside name (R70-82). In a fight a faculty read is an estimate in thought or
speech; exact figures print only outside a fight (R79-10). A derived figure is
written plainly, canon on use. Every figure on the page still comes from this
line. The running-low thresholds (half, a quarter, a tenth) are world law;
their wording is free (R79-10).
