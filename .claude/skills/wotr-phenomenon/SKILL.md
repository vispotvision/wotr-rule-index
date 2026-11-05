---
name: wotr-phenomenon
description: "Real-physics research for any War of the Realms working, ability, technique, Trait, Wellspring effect or magical phenomenon. Use this the moment Isaac sketches a rough ability, asks how something works, asks what it would cost, or a scene needs a working on the page. It names the real phenomenon in real scientific terms, states the governing law, finds the boundary condition the glyph supplies, derives the failure mode, reads the power on the Superpower Wiki, and locates the nearest anime or CRPG precedent so we know what we are not copying. Run it before wotr-write's technique step, never after."
---

# wotr-phenomenon

Mechanism is on the page in WOTR (Packs Twelve to Fourteen). A working that
cannot name its real phenomenon does not ship. This skill produces the
Phenomenon line and the physics the three-stratum stack is built on.

## Procedure

1. **Strip the ability to its effect.** What does the world do, in one plain
   sentence, with no WOTR terms. "Steel goes brittle where he touches it."
2. **Superpower Wiki (Isaac's direction, 2026-10-30: one of the primary
   sources for abilities).** Find the power type on powerlisting.fandom.com
   and read its Capabilities, Applications, Techniques, Variations,
   Combinations, Limitations and Known Users. Applications and Combinations
   feed inventive uses; Limitations feed the fault and the counter; Known
   Users are the precedent in step 8. `lookup("superpower", "<Power Name>")` on the
   WOTR MCP pulls the page, and the same tool reads the other reference wikis
   (`vsbattles`, `hxh`, `jjk`, `bleach`, `lotm`, `worm`, `wikipedia` and more); by hand, the HTML pages 403, so use the API:
   search `https://powerlisting.fandom.com/api.php?action=query&list=search&srsearch=<words>&format=json`,
   then page text `https://powerlisting.fandom.com/api.php?action=parse&page=<Title>&prop=wikitext&format=json&redirects=1`.
   WOTR canon (Codex, Wellsprings, glyphs, Fracture of Worlds, cards) still
   governs every fact; the wiki shapes what the power can do, never a number.
3. **Name the real phenomenon.** Search once (WebSearch, or the MCP's `research`, which runs
   Agent Reach and reads the pages; Agent Reach also when WebSearch misses the body). The actual physical process
   that produces that effect in the real world, at real scale. Hydrogen
   embrittlement. Cavitation. Joule heating. Bernoulli. Leidenfrost. Prefer
   the mundane law to the exotic one; the reader believes what they half
   remember from school.
4. **State the governing law.** The equation or relation, in words a
   Measurewright could say aloud. This is what the Wellspring's Physics
   Domain from the Codex will be; check `wiki/The Magic System/The Foundations/The Eight Families & the Sixty Wellsprings/The Eight Families & the Sixty Wellsprings.md`
   and `The Master Glyph Index — 136 Attested Forms.md` for the nearest
   Domain and say if none fits.
5. **Find the boundary condition.** What the glyph pins: the variable the
   working holds fixed that nature would not. That is the whole magic. Name
   the one quantity.
6. **Derive the fault.** Push the law to its edge. Every real phenomenon has
   a regime where it stops, reverses, or turns on its user. The fault falls
   out of step 4, or the mechanism is wrong. This becomes Limit and Counter.
7. **Derive the cost.** What the law demands be paid in energy, material or
   time. Route it through the Essence stratum: where does the Crystal pay,
   which Shell property strains, what Crystal State it risks.
8. **Precedent.** Start from the Superpower Wiki Known Users (step 2), then search
   once for the nearest anime, manga, LitRPG or CRPG
   version. Name it so the entry can diverge from it on purpose.
9. **Hand it to wotr-write / technique-design** as the Phenomenon line.
   Before a new art, check `wiki/The Disciplines/Techniques/` and `wiki/The Disciplines/Spellcraft/` for
   precedent inside the setting.

## Output: the Phenomenon line (under 150 words)

Real phenomenon: ___. Law: ___. Boundary condition the glyph pins: ___.
Physics Domain (Codex, or "none fits, pitch: ___"): ___. Fault: ___. Cost
routed to: ___ (Shell property / Crystal State). Superpower Wiki page: ___. Precedent: ___, and how
this diverges. Sources: ___.

## Rules

Alongside the real phenomenon, name one idea from the history of thought
(a philosopher, or superseded science such as alchemy, humours, phlogiston,
the luminiferous aether) that the stratal account can borrow as a lens, and
the Counterplay route the physics hands an opponent. See `wotr-write/references/fair-play.md`.


Never invent a number for a metaphysical quantity. Real-world figures are
fine (Joules, m/s, degrees) and legal in any diagnostic voice; in a fight,
figures live in mouths, never narration (R79-6). Narration shows the physical
effect first, then a trained POV may name it in system and science terms
(R78-3, R79-4); a working's display carries the full account on the page by the
Working Card, physics and metaphysics told as one, every term explained on
first use, and the card and notes keep it too (Isaac, 2026-11-03). Narration may explain what the trained POV understands,
and any voice that has earned it may explain (R79-6).
The elevated Hermetic vocabulary (correspondence, sympathy, essence and
accident, recognition and refusal) belongs to the Attraction-side read and
the document voice, not to this brief.
