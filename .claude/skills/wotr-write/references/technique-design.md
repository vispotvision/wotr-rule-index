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

## Entry format (Ability Law R47, 2026-09-26)

**Describe what the ability is, never how to use it.** Mechanism, what it can
act on, costs, limits, tell and counters. No tactics, combos, worked fights,
"use it to…" lines or fight counts written as advice: Isaac invents the
applications. Counters and tells are facts ("fails in a warm room", "the air
shimmers"), never instructions to an opponent.

The page is the **field format**, one `**Field** · value` line per field, 1–2
short plain sentences, tables only for numbers. Model:
`imports/system-accounts/_edition/Spellcraft/Fallacy.md` (write-up) and
`imports/page-tops/Spellcraft/Fallacy.md` (top).

**Card top:** `## Summary card` (Effect, Cost, Limit, Counter, What nobody
knows) · `## Codex line` (Wellspring, Family, Physics Domain, Category, Craft,
Stage floor, Grade required, Path gate) · `## FOW line` (Governing Primary,
Stage floor, Grade required, Path gate, Resonant Pair) · `## Origin` (Origin,
Practitioners).

**Write-up:** `## Physics` (Phenomenon, Law, Limit, a Quantity | Working |
Result table) · `## Metaphysics` (Aether, Wellspring per Wellspring, Inherited
failures, Essence, School) · `## Mechanism` (Glyph, Boundary, Effect, Failure,
Bleed) · `## Essence` (Practitioner, a cost table, Cost, Duration) ·
`## Counterplay` (Tell, Limits, Beats it, Look up).

Rules that bind the fields:
- The Effect is the mechanism playing out (mechanism and effect are one thing).
- **Costs** are a share of full reserve; EU and joules come off the Essence
  Ledger's band for the Stage (Fracture of Worlds Part Twenty-Three), and the
  Grade off the joules → Grade → tier spine.
- **Things** (items, draughts, summons, Domains, sites, weapons, beasts) carry
  their Tier Ladder rung by name (Part Twenty-Four).
- Tiers and rungs by **name**, never number; Stages by name.
- Waste radiates as heat at the Shell; every working inherits its Wellsprings'
  failures; governing Sub-Stats are the caster's; one turn is 6 seconds;
  mending costs more than breaking.
- **What nobody knows** is never answered as fact; a proposed answer is one
  in-world school's reading.
- Research stays: the real phenomenon first, cost and limits derived from the
  mechanism. The Design Chain and six-line card are retired as page formats.

**Phenomenon line** (real phenomenon, Physics Domain, Wellspring, Category,
stated fault) stays in the author notes, which never reach the page.

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
