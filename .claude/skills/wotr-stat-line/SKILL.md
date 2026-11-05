---
name: wotr-stat-line
description: "Pull the Fracture of Worlds loadout for a War of the Realms character: Level, Band, Stage by source name, Path, race and lineage, Tier Grades, the named Aether Class with its tier and the eta it sets, Soul Crystal tier and state, Essence Family, Wellspring harmonisations, EU and AU/s, Traits and their levels, skills by Grade, blessings, Domain, Resonant Pairs. Also holds the window format. Use before ANY scene with a named practitioner, before designing a technique, when Isaac asks 'what Stage is X', 'can X do Y', 'who wins', or any question with a number in it. Sources by field (R79-10): Fracture of Worlds for system law, tables and names; the Stat Sheet for a character's figures; the card for person facts and wherever the sheet is silent. Resolve by that order and move on; a missing figure is derived from the Fracture of Worlds tables, written plainly, canon on use."
---

# wotr-stat-line

The stats decide (Pack Fourteen §3), out of sight (R79-10), and the soul reports
the result to its owner in windows (R84-1). This skill produces the FOW line the
adjudication is decided from, with provenance per figure for Natalie's eyes.

## Sources, by field (R79-10)

Read each field from the source that owns it, resolve by this order and move
on; nothing is flagged and left waiting.

- **System law, tables and names:** Fracture of Worlds, mirrored as
  `wiki/The Magic System/` (Fracture of Worlds — The Living System, The
  Sixteen Stages, Tier Grade, Bands & the Aether Shell); the PDF, if handed
  one, via `pdftotext`.
- **A character's figures:** the Stat Sheet. `fow_line(name)`
  (mcp__wotr__fow_line, or `wotr-mcp call fow_line`) reads what is on
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
- Race and lineage, and what they shape in base stats and what comes easily
  (R84-9)
- Tier Grade per Primary the scene will stress, and the Stage's sustainable
  ceiling (see `references/fow-anchors.md`)
- Guild title and its trade, if any, Initiate through Paragon: it grades trust
  in that trade, and only a fighting guild reads it off the Stage table
- Aether Class: the named class and what it gives, and its tier on the old
  ladder, which sets eta (R78-10, R84-10)
- Stack line: the Grade on the card, the two-Grade cap, and every self-boost
  in use counted against it (vows, releases, Drafts, strain lifts); only
  outside help (allies, arrays, Domains) sits outside it; items work at their
  own Tier (R79-10)
- Releases and bonded weapon, aura color and signature sound
- Soul Crystal tier and Crystal State going in (Refined, Fractured,
  Overgrown, Crystallized)
- Essence Family
- Wellspring harmonisations and the Sub-Stats they alter
- EU reserve (the card's source of truth) and how long each working lasts
  from full, Flux Density, AU/s against the local Aetheric Density (R79-10)
- Traits (each with its level and the Lattice property it alters, R84-7),
  Domain tier, Attraction or Obsession sustainment
- Skills the scene will use, by Grade (R84-8)
- Crew bonds and summons' contracts (R84-25, R84-28)
- Blessings, each its own line as the giver wrote it, and what it really does
  where the line lies (R84-13)
- Resonant Pairs reached
- Path gates: what this character structurally cannot do

Each figure carries its source in brackets for Natalie's eyes: [Stat
Sheet], [card], [FOW p.], [derived]. Where two sources differ, the field's
owner wins and the line says which was used.

## The question map (§3)

Pressure: Stage gap and Dominion. Measure and reaction: Dexterity. Armor:
Ardency Penetration against tier. The read: Gnosis. Duration and push:
Tempering. The draw: Harmonics against Density. Wounds: Vitality, ATLS on
top. Crystal damage: Resilience. Cannot: Path gate. The Grade of the stat in
use decides a contest; the Stage gap governs Pressure and the upset limit;
ties break on the read, then what is left to spend, then the ground (R79-10).
Name the row when Isaac asks "who wins" out of character; on the page and in
the archive notes a row is named only for a contested or turning outcome.

## Where the figures may appear (R84, over the Style Law of R70)

**Windows.** The bearer's soul reports its numbers to its owner in their own
tongue, unseen by anyone else (R84-1). New writing carries windows as text
blocks, often and in detail, fights included, for damage, skill gains and
reserve; archived scenes stay as written (R84-3). A window follows the blow or
event it reports, so the body always comes first and the prose never turns into
numbers. It shows Grades, percentages, bars and levels; EU, AU/s and eta stay in
the notes (R84-2). Each line stands alone in square brackets, which is what
`verify_scene` counts as a window:

```
[Reserve: 41% ▓▓▓▓░░░░░░]
[Wound: two ribs cracked, left. No full breath, no hard twist.]
[Skill: Staff, D to C]
```

A normal look shows the Eight Primaries with Grades, and a Sub-Stat appears when
used or when it moves (R84-9). Traits show levels; techniques show no level and
take a bigger name when they jump (R84-7). A wound is a status line saying what
it stops you doing, and it stays until treated (R84-29). A blessing is its own
line, which the giver wrote and which can lie (R84-13). A spoken vow shows its
bargain and terms, and breaking it lands at once (R84-26). A real crew bond is a
line of its own and shows the crew's bars in a fight (R84-25). A summon is a
contract with its own window, read by its holder (R84-28). A lived breakthrough
lights the window up, a bought one is quiet, and the sheet shows the same Stage
(R84-30). A strong Limina user can make a window lie, show false numbers or hide
a line, at a cost, and Gnosis gives a fair counter (R84-32). A Release or Domain fills the window with
its name and what changed, and a timer bar drains; the two-Grade cap stands
(R84-17):

```
[FIRST RELEASE: <name>]
[Ardency C to B. <what else changed>]
[Timer ▓▓▓▓▓▓▓░░░]
```

Pressure is felt in the room first, and then the window reports it (R84-21). In
roleplay and on Discord windows are plain text blocks, and his PC's gains are
offered as window lines he keeps or changes (R84-23). The percentages agree with
the running-low thresholds (half, a quarter, a tenth), which are world law with
free wording (R79-10).

**Everyone else's numbers.** A stronger Gnosis Perception reads a weaker
Resilience Ward; everything else is an estimate said aloud, and people can hide
or fake it (R84-22). Any practitioner feels another's Band and rough Stage as
such an estimate, Gnosis setting how close. Instruments read everyone else
(R70-78). A monster sits on the same Level and Grade scale, with question marks
for a weak reader (R84-14). An Appraisal skill or an assay instrument reads an
item, and a good forger can beat a weak appraiser (R84-20).

**Narration and mouths.** In a fight narration stays free of figures: they live
in mouths and in windows. Outside a fight, the body first, the figure a line
after in the same beat (R70-89), and narration states the figures the POV holds:
his own last window, a card he has seen, what he was told (R70-83; R14-4-SUBSTAT
retired). Ranked practitioners talk exact numbers and argue builds in dialogue;
commoners round (R70-93), in a fight as in talk. `Stage V, Splintering`, numeral
beside name (R70-82). A derived figure is written plainly, canon on use. Every
figure on the page still comes from this line.
