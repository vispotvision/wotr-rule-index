# Character and art-first pipeline (draft, 2026-10-31)

Isaac's direction: he gives art and Natalie builds from it. This file is the working draft of the pipeline from a piece of art, or a spoken sketch, to a filed character card. It becomes law when Isaac approves it. The same art-first path serves places, items, creatures and techniques (the last section). Answers so far: `imports/drafts/character-pipeline-questionnaire/`.

## The steps

1. **Receive.** Isaac sends art (an image) or a sketch in words. Ask only where the image lives (the wiki Assets folder, kept private, or read and not stored); Isaac decides per image.
2. **Read the art.** Read the image and take the four things Isaac named: the full physical inventory (hair by comparison, face, body, clothing with fit and wear, marks and scars); apparent age, culture and place (the Quarter, the naming register); mood, bearing and voice (what they might refuse or want); and power and aura hints (colors, weapons, symbols and effects as clues to Family, hue and kit).
3. **Stay close to the art.** Invent nothing the image does not show. What it leaves open (age, culture, powers) is set to null and logged in the author notes, not guessed. Isaac fills a gap by saying so.
4. **Character first.** What this person refuses, what they survived, what they believe that costs them, drawn from the bearing and detail in the art, and no further than the art supports. Then the want, the refusal line, a lie where the want makes one, and one verbal fingerprint under the culture's grammar.
5. **Numbers.** Derive Level, Band, Stage, Path, Grades, Aether Class (and the eta it sets), Soul Crystal state, Family and the Wellspring harmonizations from the concept and the age, using the Fracture of Worlds tables; state plainly what was derived. Isaac overrules any figure. A missing figure is derived, written plainly, canon on use.
6. **Kit.** Traits and techniques through `desktop/ABILITY_PIPELINE.md`, using the aura and power hints from the art, each with its Wellspring signature.
7. **Voice.** A one-sentence description of the voice and one sample line, approved with the card.
8. **Backstory.** Rich lore with held secrets: public history, private history and sealed facts the page will not state. The sealed facts live in the author notes and are flagged sealed; the card shows only what a character could know.
9. **Card.** The skeleton in `desktop/templates/CHARACTER_CARD_TEMPLATE.md`: the one-screen head, stat line, combat grammar, techniques with tell and counter, the voice line; sections below only where the character has them. A full draft card is handed back first, for Isaac to keep or cut.
10. **File.** The card goes into the vault through `create_character`; the art is stored where Isaac said; a roster entry is kept (`npc_set`); the Ledger and card upkeep stay silent.

## The other pipelines (Isaac's answers, 2026-10-31)

- **Improve my post.** Returns the rewrite alone, with no commentary, in his intent, voice, tense and person; his post still wins. It fixes four things: the body and blows (the Blow Card), magic on the blow (display, signature, cost), voice and heat, and continuity and rules.
- **Locations.** Written only when a scene uses them, and they grow from play.
- **Factions.** A card carries the faction's wants and the splits inside it, its procedures and seals, its money and reach, and a face and a front (a clock and the sign it puts into play).
- **Items.** Driven by art when art exists; otherwise one line (name, Tier, price, wear, one fact).
- **Creatures.** Invented in the scene and filed as a bestiary entry when they recur, biology first.
- **Villains and antagonist circles.** Built by the card, like any character: refusal, want, voice, numbers, backstory, sealed facts. A villain is a person.
- **Arc and session plans.** Hold the Fronts and their clocks, the anchor scenes and the ending, the cast and their wants, and the seeds and plants that will pay off.

## The same path for other things

- **Places and maps.** Read the layout, light, materials, crowd and weather; produce a described location with senses, people and a want that belongs to the place.
- **Items and gear.** Read the object; produce an item with Tier, wear, history and use, priced from the table.
- **Creatures and Well-spawn.** Read the beast; produce a bestiary entry, biology first, then behavior and danger.
- **Techniques and effects.** Read the effect; produce a technique through the ability pipeline, its sensory signature matched to the Wellspring.
