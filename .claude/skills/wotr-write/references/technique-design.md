# Technique and ability design

Tags: magic-design, codex, stats, character-sheet. Load the Ability Technique
Design Guide read through Packs Fourteen, Thirteen, Twelve, Ten, Nine, and
whatever `load_rules` returns newer (R79-9 governs the required fields).

**What a technique requires (R79-9):** its mechanism, its cost, and one fair
counter within reach at its own Stage. Limit and tell where they exist. The
before, during and after counter triad only for signatures. Every ability has
a counter.

## Entry shape and the full path (Isaac, 2026-10-31)

An entry is written in Isaac's own layout (Reitori, Hiromi; R81-16), drawing
on the Superpower Wiki for design, application, variation and limitation but
never copying its lists: there is no Applications, Variations, Associations or
Limits list, and the physics lives on the entry beside the metaphysics (R80-25).
The path from a rough sketch to a filed card is in
`desktop/ABILITY_PIPELINE.md`:`desktop/ABILITY_PIPELINE.md`: research (Superpower Wiki is a primary source,
physics, the Wellspring's analogue), design, the Wellspring signature from
`desktop/style-bank/wellspring-signatures.md`, a sample display for
signatures and releases, one best name, an overlap check surfaced to Isaac,
then filing.

## Order of design, never reversed (R79-9)

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
4. Only then the Codex lookup, for precedent and assignment: Glyphs,
   Wellspring, kind, Titan, Form, Stage. Name what was checked
   only when proposing a new Codex entry; if no combination fits, pitch the
   entry in the same pass.
5. The FOW line beneath it: governing Primary Stat and Sub-Stats, Stage floor,
   Grade required, Path gate if any, Resonant Pair if any. Figures by field
   (R79-10); a missing one derived from the Fracture of Worlds tables, written
   plainly, canon on use.

6. The fairness pass (`wotr-write/references/fair-play.md`): the cost that hurts, the stated limits, the
   Counterplay route that beats it, the tell, numbers in band for the Stage.
   Then the lookup trail: which pages a player would have to read to find the
   counter. And the lens: the philosopher or historical theory the stratal
   account draws on, credited in the notes.

The swap test: if two characters exchanged abilities and neither read as
wrong, neither ability is working.

## Entry format (R82-20 to R82-23, Isaac 2026-11-04)

One wild concept, then named moves (R82-11). Every art, assumed to be used in
battle unless the card says otherwise, is written: its name in caps with its
native-language name (script and romanization) and its kind (a release form's
kind is *First*, *Second* or *Third Release*); the **hook**, one sentence a kid
could repeat, no system words; the **named moves**, a line each saying what it
does and looks like in a fight; **How it really works**, the full account with
the metaphysics and the physics as one story, the glyph's boundary condition,
for a Trait the aura's color, and for a signature or release how it plays
against a higher Stage; one short **Cost** line and one short **Counter** line
(individual moves may skip them); and a **Numbers** block with the exact figures
and the art's signature sound word as a plain `Sound:` data line, the only place
an entry spells a sound, because documents carry no onomatopoeia and sound words
belong to scenes (Isaac, 2026-11-05). Counters and tells are facts ("fails in a warm room",
"the air shimmers"), never instructions to an opponent. Names follow
ABILITIES AND THE WORLD in `desktop/NATALIE.md`. An old entry is rewritten into
this shape the next time it is edited or used, keeping what scenes have shown
(R82-46) and listing its old name (R82-47). For his PC, new names are offered
and he keeps or cuts them (R82-28).

- Any words that make it clearest, chosen fresh; technical terms welcome when
  explained on first use. Explaining fully beats concision (DEPTH AND
  EXPLANATION in desktop/NATALIE.md, Isaac 2026-11-03).
- Full figures inline (EU, time from full, Grade, m/s, joules), written plainly
  with no (est.) mark (R76-6); estimates are listed in the author notes only.
  Never a number where a source has one.
- Always mechanism, cost and counter; limit and tell where they exist
  (R79-9). The bearer's belief is left
  implied, never quoted. Offices, Lattice property and nucleation only where
  they read naturally; they are still designed.
- Model: Isaac's FERMENT (Primary Trait) for Malphas: "Anything that enters
  Malphas's reach, he rots. ... A blade still can."

The design work above (phenomenon, three strata, Codex, FOW, fairness) still
happens in full; it feeds the entry and the author notes in chat. When
Isaac sketches an ability out of character, supply how it works without being
asked (R79-2). For his PC, inventive new uses of his abilities are Natalie's to
write in play; new techniques, Level points and card changes stay his.

Rules that bind the content:
- The Effect is the mechanism playing out (mechanism and effect are one thing).
- **Drain** is written as how long the working lasts from a full reserve (R78-10); EU and joules come off the Essence
  Ledger's band for the Stage (Fracture of Worlds Part Twenty-Three), and the
  Grade off the joules → Grade → tier spine.
- **Things** (items, draughts, summons, Domains, sites, weapons, beasts) carry
  their Tier Ladder rung by name (Part Twenty-Four).
- Tiers and rungs by **name**, never number; Stages and Bands by name with
  the numeral beside it (Stage V, Splintering; R70-82).
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
  Trait. It has its own level, which rises with use and grows with overall Level
  and skill (R84-7).
- A **Skill** names its operating principle at the body: for a read, the real
  cognitive cues; for a martial skill, mechanics, measure and tempo. It rises
  with use and shows as a Grade on the sheet; a technique is a named thing done
  with it, shows no level and takes a bigger name when it jumps (R84-7, R84-8).
  Drafts, runes, tags and chants are skills and trades anyone can level, with no
  named craft above them (R84-18).
- A **class ability** comes from the named class the soul was offered and evolves
  with it; the one wild concept stays the person's own (R84-10).
- A **bloodline faculty** states what quantity it acts on, what it costs to
  hold open, and what it cannot resolve. "The Moto see" is not an entry.

## Metaphysics vocabulary, where it is legal

Correspondence, sympathy and contagion, essence and accident, form and
actualisation, recognition and refusal: the Attraction-side read and the
document voice. Real physics and Mechanism Vocabulary: any voice, and narration in any POV
when explained, an untrained POV in plainer, more wondering words (R81-4). On
the page the name, hit and awe come first, then the account, scaled by the
move's size (R82-24): at a signature's first use the full Working Card (DEPTH AND
EXPLANATION in desktop/NATALIE.md), the real phenomenon and its law named and
explained, the math in the notes (R81-7).

## The gap-fill pass (when Isaac submits a fight or working to improve)

Before a sentence is polished, eight steps in order: beat inventory, logic
audit, stratum audit, physics audit, body audit, phenomenon audit, vocabulary
pass, prose pass last. `gap_fill` runs it as an advisory, for set pieces and
fights he submitted only, unlogged (R79-10). The pass may change an outcome
when no cause fits, and says so.

## The cost audit (standing docket)

Roughly sixty percent of existing entries fail the "overuse strains him" test.
Any entry you touch gets its cost rewritten to something specific, bodily, and
present after the fight ends.
