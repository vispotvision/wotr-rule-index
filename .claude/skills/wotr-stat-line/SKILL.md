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

## Where the names may appear

Stat effects on the page as behaviour and physics. Names of stats,
Sub-Stats, Grades, Bands, eta, EU, Aether Class, Category only in a mouth,
an instrument, a document, or a private count. Never in narration.
Sub-Stat names may be spoken the way LitRPG characters talk about stats.
