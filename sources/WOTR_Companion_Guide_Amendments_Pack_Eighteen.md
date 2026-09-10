# WOTR COMPANION GUIDE AMENDMENTS — PACK EIGHTEEN

## The Codex-First Mandate

**Status:** originated, pending Isaac's ratification.
**Precedence:** Pack Eighteen governs where it conflicts with Packs Seventeen through One and with all base companion guides. It amends the Ability and Technique Design Guide, the Master Style Directive, the Session Start Protocol, and the Manual Verification Guide.
**Scope:** every working, spell, technique, art, rite, Domain, Trait, reagent, tincture, oil, chalk, glass, ink, ward and consumable. Everything with a Codex line.

---

## §1 — THE FAULT

`The_Master_Codex.xlsx` is a complete relational reference and it has been treated as a filing cabinet consulted after the fact. It is not. It is a **controlled vocabulary and a worked corpus**, and designing without opening it produces two failures, both of which occurred in the Kharven sequence.

**Inventing inside a closed set.** The Codex fixes sixty Wellsprings, nine Families, nine Physics Domains, sixteen Temperance stages, five Glyph Classes, fourteen Archons, fourteen Titans, eight alchemical Tiers and thirty-six alchemical Types. These are enumerations, not suggestions. In this session Natalie pitched **Cupellatio** as a new Wellspring for Open Crucible while Dissolution, Coagulatio, Catharsis and Absolution sat unread in the list, and pitched **Consonantia** for an entrainment working while the glyph **[Ar] Accord** already existed with the Meaning column reading *unifies vibrations; stabilizes*, under Judicium, Fulguria, Electromagnetism. Both inventions were unnecessary and both were wrong.

**Ignoring 109 worked precedents.** The Spell Index already carries, per entry: Category, Name, Primary Glyphs, Temperance Min, Primary and Secondary Wellspring, Family, Physics Domain, Trigger, Effect, **Mechanism**, Numerical/Physical Effect, Target Response, **Cost/Backlash**, and **Counterplay**. That is Pack Seventeen's six-line card, already populated, one hundred and nine times. Every one of those rows is a solved example of the exact problem being solved from scratch each session.

---

## §2 — THE MANDATE

**The Codex is opened before the working is designed, not after.**

Order of operations, and the order is the point:

1. **Read the sheet.** Before any working is named, pitched, converted or written into prose, query the Master Codex for the phenomenon.
2. **Search the Spell Index first.** 109 entries. If the working already exists, use it. If a near neighbour exists, derive from it and say which row.
3. **Search the Master Glyph Index second.** 136 glyphs, each with Meaning & Use, Primary and Secondary Archon, Primary Wellspring, Family, Physics Domain, and the full attested lists. The glyph usually decides the assignment, because the glyph is where the phenomenon already got named.
4. **Take assignment from the Lists sheet.** Wellspring, Family, Physics Domain, Temperance Min, Category, Glyph Class. **Never from memory and never invented.**
5. **Alchemy goes to the Alchemical Index.** 41 entries with Tier, Type, Glyphs, Wellsprings, Family, Physics Domain, Titan Tie-In, Ingredients, Process, Effect.
6. Only then design, and only then write.

**No new Wellspring, Family, Physics Domain, Archon, Titan, Glyph Class, Tier or alchemical Type may be proposed until the existing enumeration has been read and the absence demonstrated.** A proposal that does not name what was checked and why it failed is not a proposal.

---

## §3 — THE CODEX IS THE DESIGN CHAIN, ALREADY FILLED IN

Pack Seventeen's card and the Spell Index schema are the same object. The mapping is exact and the Codex column governs:

| Pack Seventeen | Spell Index column |
|---|---|
| Operation | Mechanism, plus Trigger |
| Manifestation | Effect, plus Numerical/Physical Effect and Target Response |
| Cost | Cost/Backlash |
| Limit | Temperance Min, plus the constraint stated in Mechanism |
| Counter | Counterplay |
| Codex line | Category, Primary Glyphs, Wellsprings, Family, Physics Domain |

**Consequence.** When a new working is designed, its entry is written in Spell Index form and is a candidate row for the sheet. The Codex is a living document and everything originated in play belongs in it or does not exist.

**And when converting Isaac's rough prose (Pack Sixteen §2), route 1 now means *route to a Codex term*.** The conversion lexicon in Pack Sixteen §4 is subordinate to the Codex: where the two disagree, the sheet wins.

---

## §4 — GLYPHS ON THE PAGE

The Glyph Index gives every glyph a bracketed short form, a name, a class and a meaning. Prose usage rules, unchanged from the base guides and restated because they now have a source:

- Glyphs are named in a **document**, an **instrument**, a **practitioner's diagnostic voice**, or a **private count**. Narration may state what a glyph *did* and does not announce the bracket.
- A glyph in a chant, an inscription or a Wordform Chain is quoted exactly as the Index gives it.
- The **four Glyph Roles** from the Notion Lexicon (Authorization, Boundary, Direction, Sealing) describe *function within a working*. Glyph **Class** from the Codex (Root, and Derivative by Extension, Compound, Synonym or Counter) describes *provenance*. They are orthogonal axes and neither substitutes for the other.

---

## §5 — ALCHEMY

Three sources, consulted in this order, and none of them optional.

**The Alchemical Index** for what exists: 41 entries across eight Tiers and thirty-six Types, each with its glyphs, Wellsprings, Family, Physics Domain, Titan Tie-In, Ingredients, Process and Effect.

**Alchemetrica** for the doctrine, and its governing line is the whole discipline in one sentence: *the reagents are the nouns, the Wellspring is the verb, Glyphica is the grammar that makes the sentence lawful.* It also fixes the eight Wellsprings that are simultaneously Wellspring, cosmic principle and alchemical operation, and any working that touches Calcination, Dissolution, Coagulatio, Distillation, Sublimare or Transmutatio is bound by their entries there.

**The Real Alchemy** for the real-world substrate: the operations were genuine laboratory procedure, the furnaces ran for months, the vessels were luted with dung-and-clay, and the cover-names were deliberate. Anything Natalie invents about process, apparatus or reagent behaviour is checked against it before it reaches the page.

**Companion documents** to load with the above: The Provenance Doctrine, The Standing Index, The Bench of Attribution.

---

## §6 — SESSION START AMENDMENT

Added to the Session Start Protocol, between the current steps four and five:

> **4a. Open the Master Codex for anything the scene will work.** Query the Spell Index for existing precedent, the Glyph Index for the phenomenon, the Alchemical Index for any reagent, and the Lists sheet for every assignment the scene will name. Do this before the FOW line and before the Standing Inventory, because the Codex determines what the working *is* and the others determine what it costs and how it reads.

**Access method:** `openpyxl`, read-only, from `/mnt/project/The_Master_Codex.xlsx`. Never from memory. The sheet is the authority and Natalie's recollection of it is not.

---

## §7 — VERIFICATION

Added to the Manual Verification Guide and to `wotr_verify.sh` as checks 37 to 39, run with `--codex`.

**Check 37 — Controlled vocabulary.** Every Wellspring, Family, Physics Domain, Temperance stage, Archon, Titan, Glyph Class, alchemical Tier and alchemical Type named in the file is validated against the Lists sheet. Anything absent is a FAIL and must be either corrected or explicitly declared as a proposed new entry with the checked enumeration named.

**Check 38 — Glyph validity.** Every bracketed glyph token in the file is validated against the Master Glyph Index. Unknown tokens FAIL.

**Check 39 — Precedent.** Manual. For any new working, name the Spell Index rows checked and state whether the working is new, a derivation of a named row, or a duplicate.

---

## §8 — RETROSPECTIVE

Every technique, Trait and working originated across the Kharven sequence needs a Codex pass it did not get. Priority order:

1. **Open Crucible.** Assignment pending; Cupellatio struck; Dissolution, Coagulatio, Catharsis and Absolution to be evaluated against the Alchemetrica operation entries.
2. **Dōchō.** Consonantia struck; **[Ar] Accord** is almost certainly the glyph, with Judicium, Fulguria, Electromagnetism following from the Index row.
3. **The Trait of Purity**, the **Hammer of Justice** and **Ignis**, which have no Codex line at all.
4. **Bulwark** and **Compact**, same.
5. **The Scale working**, which is Urion's own Designation (Order Magic / Judicaris) and whose glyphs are listed against him in the Pantheon sheet under [Ur] Balance and [Sel] Measure, and which I did not check before writing three scenes with it.

## §9 — STANDING TASK

Fold Packs One through Eighteen into the base guides and retire the diffs. Ask once per session.
