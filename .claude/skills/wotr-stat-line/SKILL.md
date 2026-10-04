---
name: wotr-stat-line
description: "Pull the Fracture of Worlds loadout for a War of the Realms character: Level, Band, Stage by source name, Path, Tier Grades, Coherence tier and eta, Aether Class, Soul Crystal tier and state, Essence Family, Wellspring harmonisations, EU and AU/s, Traits, Domain, Resonant Pairs. Use before ANY scene with a named practitioner, before designing a technique, when Isaac asks 'what Stage is X', 'can X do Y', 'who wins', or any question with a number in it. Sources in order: Stat Sheet workbook, character card, Fracture_of_Worlds. Disagreements are flagged, never resolved. Never invent a number."
---

# wotr-stat-line

The stats decide (Pack Fourteen §3). This skill produces the FOW line the
adjudication and the Stat Ledger are written from, with provenance per figure.

## Sources, in order of preference (R14-2, ruling 2026-09-12)

1. `fow_line(name)` (mcp__wotr__fow_line, or `build/book_tools.py fow_line`;
   it reads the card). Where a character has two cards in play, the thread's
   State of Play says which.
2. The Stat Sheet workbook. **Wins over the Notion card when they differ.**
   Not in this repo: a figure only it holds is "workbook, unchecked".
3. The character card (`character(name)`, or its file under `wiki/`).
4. Fracture of Worlds, mirrored as `wiki/The Magic System/` (Fracture of
   Worlds — The Living System, The Sixteen Stages, Tier Grade, Bands & the
   Aether Shell). The PDF, if handed one, via `pdftotext`. This is the
   verification source for every figure regardless of where it
   came from.
5. WOTR_COMPLETE_MAGIC_SYSTEM.docx: derivative, never sole authority.

## The line (every field, "unknown, estimate ___ inside ___" where absent)

- Level / Band / Stage (Fracture of Worlds name only) / Path
- Tier Grade per Primary the scene will stress, and the Stage's sustainable
  ceiling (see `references/fow-anchors.md`)
- Tier of Standing and eta
- Aether Class
- Soul Crystal tier and Crystal State going in (Refined, Fractured,
  Overgrown, Crystallized)
- Essence Family
- Wellspring harmonisations and the Sub-Stats they alter
- EU reserve, Flux Density, AU/s against the local Aetheric Density
- Traits (each with the Lattice property it alters), Domain tier,
  Attraction or Obsession sustainment
- Resonant Pairs reached
- Path gates: what this character structurally cannot do

Each figure carries its source in brackets: [workbook], [card], [FOW p.],
[estimate: range]. A workbook/card disagreement is listed as both figures
and flagged for Isaac.

## The question map (§3)

Pressure: Stage gap and Dominion. Measure and reaction: Dexterity. Armour:
Ardency Penetration against tier. The read: Gnosis. Duration and push:
Tempering. The draw: Harmonics against Density. Wounds: Vitality, ATLS on
top. Crystal damage: Resilience. Cannot: Path gate. Name the row when you
answer "who wins".

## Where the figures may appear (Style Law, R70)

The body first, the figure a line after in the same beat (R70-89).
Narration states the figures the POV holds: his own last reading, a card he
has seen, what he was told (R70-83; R14-4-SUBSTAT retired). The bearer reads
his own sheet in his Soul Crystal at thresholds, exact and blind to wounds and
to others; instruments read everyone else (R70-78), and any practitioner feels
another's Band and rough Stage, Gnosis setting how close (R70-79). Ranked
practitioners talk exact numbers and argue builds in dialogue; commoners round
(R70-93). Inside a fight, Grades and gaps only at the read, as estimates, no
running figures (R70-88). Readouts: inline by default, a set-off block only at
a re-assay that moves something, a breakthrough or an arc's end (R70-80); up to
three a scene, two a roleplay turn (R70-86); `Stage V, Splintering`, numeral
beside name (R70-82); a figure not yet in canon printed with the instrument's
hedge and logged as an estimate (R70-99). Every figure on the page still comes
from this line.
