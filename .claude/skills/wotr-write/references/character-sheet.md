# Character sheets and cards

Tags: character-sheet, stats, naming, codex. Under 16,348 characters (Trello
card limit). New cards go under Volume I Character Cards. `create_character` /
`update_character` write to Notion and git in one call, so they run on Isaac's
word only; until then the sheet is a file he reads. Check `character(name)` and
`grep -ril "<name>" wiki/` before creating; never duplicate a page (wotr-ops
has the no-second-card procedure).

## Before writing

1. `character(name)` if a card exists. `convert_character(source)` for old
   material (a Trello export, an old sheet): it returns the conversion brief on
   the current system; work from the brief, not the old text.
2. Naming pass (five strata; Büri register dead; see scene-pipeline.md).
3. Every number checked: Stat Sheet workbook wins over a Notion card when they
   differ; flag the disagreement, never resolve it. The workbook and
   Fracture_of_Worlds are not in this repo; the mirror of the system is
   `wiki/The Magic System/` (Fracture of Worlds — The Living System, The
   Sixteen Stages, Tier Grade, Bands & the Aether Shell). A figure only the
   workbook holds is marked "workbook, unchecked" and asked for.
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
  scale; eta survives underneath. Hollow and F confer no rank.
- Eight Essence Families: Caloria, Fulguria, Vectoria, Spatium, Materia,
  Vitalia, Fluxia, Limina.
- Soul Crystal tiers: Dormant, Awakened, Harmonic, Resonant, Radiant,
  Sovereign, Crystallized Soul, Absolute Crystal.
- Domain: seed at VII, first stable Domain at VIII, Realm at IX to X, ambient
  at XI to XII, Continuum-registered at XIII, indistinguishable from the
  character at XIV.

## The seventeen sections, in order, all mandatory

I. Identity (including the Catalyst Event)
II. Soul Architecture
III. Wellspring Harmonizations
IV. Primary Stats
V. Sub-Stat Peaks
VI. Physical Force
VII. Aether Flow
VIII. Traits (each names the Lattice property altered)
IX. Domain
X. Techniques (five-line card, Design Chain, Codex line, FOW line; Counterplay
   mandatory; see technique-design.md)
XI. Spirit Axes
XII. Resistances
XIII. Physical Description (full inventory: hair by comparison, face, body with
   areas named, clothing with fit and wear, marks)
XIV. Psychology (refusal, wound, conviction; what they notice first in a room)
XV. Equipment (Item and Equipment Guide; mass and balance per weapon,
   proof-marks where relevant)
XVI. Temperance Record
XVII. Fracture Log

Formatting: bold markdown headers, bold field labels, fields as short prose
lines not nested bullets, Traits/Techniques/Equipment as inline "/"-delimited
fields.

## Card fields added by ruling

- Gloss rights (yes / diagnostic only / unlimited / never).
- Combat grammar assignment (Blade, Verdict, Percussion, Expenditure), marked
  ratified or pitched.
- Pressure suppression profile (docket; pitch one, label it).

## Author notes for a sheet

Originated pending ruling; canon conflicts (card vs workbook); Phenomenon line
per technique; Stat Ledger of the figures used and where each came from;
estimates listed with their range; open questions. On the wiki, attributions
read "originated, pending ruling" with no author name attached, ever.
