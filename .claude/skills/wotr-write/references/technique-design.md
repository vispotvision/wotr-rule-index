# Technique and ability design

Tags: magic-design, codex, stats, character-sheet. Load the Ability Technique
Design Guide sixth edition read through Packs Fourteen, Thirteen, Twelve, Ten,
Nine, and whatever `load_rules` returns newer.

## Order of design, never reversed

1. Who is this person: what they refuse, what they survived, what they believe
   that costs them.
2. The phenomenon: the real thing, named in real scientific terms. Research it
   before writing it. Same for the nearest anime or CRPG precedent.
3. The three-stratum stack (Pack Thirteen §2):
   - **Aether**: what was in the room. Density, Residue, Saturation, the
     district main, whether the draw is licensed.
   - **Wellspring**: its Physics Domain from the Codex, stated as a real law,
     the glyph as boundary condition.
   - **Essence**: Soul Crystal (Essence Core, Aether Shell, Attraction Layer),
     EU, eta, Flux Density, Crystal State under strain.
   The Category's alignment tag says where cost and counter live. The fault
   falls out of the mechanism; if it does not, the mechanism is wrong.
4. Only then the Codex line, assigned after the phenomenon: Glyphs, Wellspring,
   Family, Physics Domain, Category, Stage. If no combination fits, say so and
   pitch the new Codex entry in the same pass.
5. The FOW line beneath it: governing Primary Stat and Sub-Stats, Stage floor,
   Grade required, Path gate if any, Resonant Pair if any. Every figure from
   `fow_line` or Fracture_of_Worlds; estimates labelled.

6. The fairness pass (`wotr-write/references/fair-play.md`): the cost that hurts, the stated limits, the
   Counterplay route that beats it, the tell, numbers in band for the Stage.
   Then the lookup trail: which pages a player would have to read to find the
   counter. And the lens: the philosopher or historical theory the stratal
   account draws on, credited in the notes.

The swap test: if two characters exchanged abilities and neither read as
wrong, neither ability is working.

## Entry format

**Summary card, five lines, what the reader sees:**
- **Effect**: two to four sentences. What happens, what it looks like, what the
  target feels, written as the mechanism playing out: the boundary the glyph
  moves, the law doing what it does, and that is the effect. Mechanism and
  Effect are one thing (Isaac, 2026-09-24, RULINGS.md); an Effect that could
  be true of a different mechanism is wrong. Detail is not complexity.
- **Cost**: one line. What it does to the body and what remains after. "Overuse
  strains him" is not a cost. The cost must survive outside the fight.
- **Limit**: one line. What it structurally cannot do.
- **Counter**: one line. Mandatory on Signature techniques.
- **What nobody knows**: one line per art, a question about why the law holds,
  never about what the working does (R17). Mechanism is on the page; origin is
  not.

**Full Design Chain** (workbook, printed in entries and sheets, never surfaced
as explanation in narration): Trigger, Function, Mechanism, Numerical Effect,
Target Response, Consequence, Limitation, Weakness, Cost, Counterplay.

**Codex line.** **FOW line.** **Phenomenon line** (real phenomenon, Physics
Domain, Wellspring, Category, Mechanism Vocabulary term, stated fault) in the
author notes.

## Scope rules for the other entry kinds (Pack Seventeen §5)

- A **Trait** names the Lattice property it alters, and therefore which
  injuries behave differently and which identically. "Harder to kill" is not a
  Trait.
- A **Skill** names its operating principle at the body: for a read, the real
  cognitive cues; for a martial skill, mechanics, measure and tempo.
- A **bloodline faculty** states what quantity it acts on, what it costs to
  hold open, and what it cannot resolve. "The Moto see" is not an entry.

## Metaphysics vocabulary, where it is legal

Correspondence, sympathy and contagion, essence and accident, form and
actualisation, recognition and refusal: the Attraction-side read and the
document voice. Real physics and Mechanism Vocabulary: any diagnostic voice.
Nothing in narration on its own authority.

## The gap-fill pass (when Isaac submits a fight or working to improve)

Before a sentence is polished, eight steps in order: beat inventory, logic
audit, stratum audit, physics audit, body audit, phenomenon audit, vocabulary
pass, prose pass last. `gap_fill` runs it. Log under "Added by the gap-fill
pass." The pass may change an outcome when no cause fits, and says so.

## The cost audit (standing docket)

Roughly sixty percent of existing entries fail the "overuse strains him" test.
Any entry you touch gets its cost rewritten to something specific, bodily, and
present after the fight ends.
