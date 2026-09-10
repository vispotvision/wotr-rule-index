# WOTR Companion Guide Amendments, Pack Fourteen

## THE STAT SYSTEM AND TERMINOLOGY MANDATE

*Status: originated by Natalie, pending Isaac's ruling. Governs over Thirteen and Twelve where they touch. Fracture of Worlds is the only authority on any number cited here; where this pack paraphrases, the source wins.*

---

## §1. The Fault

Pack Thirteen says a working is explained at three strata and grounded in a real phenomenon. It does not say where the character's side of the explanation comes from, and in practice it has come from nowhere: "Essence" as an undifferentiated fluid, "Stage" as a vague size, cost as tiredness. The Fracture of Worlds system tracks eight Primary Stats with fifteen Sub-Stats each, sixteen Stages with named ceilings, Tier Grades on fixed thresholds, a Coherence Band tracking eta, seven Aether Classes, eight Soul Crystal tiers, four Crystal States, Path gates, Resonant Pairs, Threshold Events, and a full Essence economy. None of that has been doing any work on the page. It is the most precise instrument in the project and it has been sitting in the workbook.

The second fault is drift. Cards say "Stage I Ignition" and "Stage IV Temper." The Codex Lists sheet and Fracture of Worlds say Murmuring and Flourishing. Nobody has ruled. Terminology that drifts is terminology that cannot be adjudicated with.

---

## §2. The Loadout

**Before any scene with a named practitioner, and before any technique is designed, Natalie loads that character's Fracture of Worlds line.** From the character sheet, the Stat Sheet workbook, or the Notion card, in that order of preference, and verified against Fracture_of_Worlds.md by grep or pdftotext. The line:

- Level, Band (I to V), Stage (I to XVI, by name), Path alignment.
- Tier Grade on every stat the scene will lean on, and the Stage's sustainable ceiling for it.
- Coherence Band and eta.
- Aether Class. Aether Index if on the sheet.
- Soul Crystal developmental tier and current Crystal State.
- Essence Typology (one of the eight Families) and the Catalyst it matches.
- Wellspring harmonisations, each with the Sub-Stats it qualitatively alters (Fracture of Worlds Part Thirteen: a Wellspring changes what the number means, never the number).
- EU reserve, Flux Density, AU/s, and the local Aetheric Density that caps AU/s.
- Traits, Domain tier, and Attraction or Obsession sustainment.
- Any Resonant Pair the character has reached (Alacrity and Celerity at B unlocks Reactive Cast; Overflow and Detonation at S unlocks Controlled Detonation; and the rest of Part Nine).

**Where a value is not on any sheet, it is written in the author notes as an estimate inside the documented range for that Stage and Band, and marked as such.** It is never invented to feel right. Memory rule twenty-six governs and this pack restates it because the failure recurs.

---

## §3. The Stats Decide

Table Rule 5 adjudicates from Stage gap, the read, what has been spent, and the environment. This pack names which stat answers each of those, so the adjudication is reconstructible and so the prose can show the right body doing the right thing.

| Question in the scene | What decides it |
|---|---|
| Whose presence bends the room | Stage gap first; Dominion Pressure and Radius for how far |
| Who closes measure first, who reacts in time | Dexterity: Celerity for travel, Reflex for reaction, Burst for the first step; Attack, Reaction, and Travel Speed by Grade per Part Six |
| Whether a working beats an armour tier | Ardency Penetration against the tier's stated behaviour in the Combat Guide; Flux for how much arrives |
| Whether a read lands, and what it costs in tempo | Gnosis Perception for the noticing, Acuity for the interpreting; a faculty read spends a moment per Twelve |
| How long a working holds and how hard it can be pushed | Tempering Compression and Longevity for duration; Overflow and Overchannel for the push, with Crystal Fracture risk above the Stage ceiling |
| What the draw costs in this room | Harmonics Attunement and Depth against local Aetheric Density; Residue and Saturation shift the price |
| How a wound behaves | Vitality: Fortitude for what breaks, Hemostasis for how fast it bleeds, Threshold and Tolerance for when pain arrives; ATLS class on top |
| What a hostile working does to the Crystal | Resilience Integrity and Ward; Anchoring for whether identity holds under pressure |
| Whether a technique is sustained cleanly or by refusal | Attraction Force through Harmonics and Dominion; Obsession Force through the same stats at escalating soul-cost |
| What the character cannot do at all | Path gates. A Body-Path fighter's Spirit-aligned Sub-Stats sit at C until his pattern of use changes, whatever he claims |

**Every outcome in a fight traces to a row in this table**, and the author notes say which.

---

## §4. Two Channels to the Page

**The effects channel, always on.** Every stat that decided an outcome shows on the page as behaviour and physics. B-Grade Celerity is a specific speed of closing measure and a specific breath-count for the opponent to answer it. Poor Hemostasis is a wound that will not stop. High Compression is a working that outlasts the fight. Eta below one half is heat coming off the practitioner, frost on his lips, static in the air, the wasted share arriving as weather. A Crystal Fracture Event is erratic casting, identity leak, a man who does not sound like himself. **Grade letters and stat names never appear in narration. Their consequences always do.**

**The diagnostic channel, rationed per Twelve §5.** Stat names, Sub-Stat names, Grades, Bands, eta, AU/s, EU counts, Aether Class, Crystal State, and Category names reach the page in a mouth, an instrument, a document, or a practitioner's private count. A Measurewright says "Band C, no better, and his Compression is carrying the rest." A Kharven hunter says the same thing in weight and breath. Class-marking by vocabulary per Pack Nine.

**Sub-Stat names are diagnostic-only.** They are the finest grain the system has and they are exactly the words a faculty reading uses. Nobody else reaches for them.

---

## §5. The Terminology Mandate

**Canonical, used exactly, no approximation:** the sixteen Stages by number and source name; the five Bands with Level ranges; the thirteen Tier Grades from Hollow to EX+; the nine Coherence Bands and their eta ranges; the seven Aether Classes from Ø Dormant to Ω Absolute; the eight Soul Crystal developmental tiers; the four Crystal States; the eight Primary Stats and their Sub-Stats; the three speed components; Resonant Pairs and their unlocks; Threshold Events and Crystal Fracture Events; EU, Flux Density, AU/s, eta; Passive Recovery and the rest of the recovery model; the eight Families as Essence Typology; the Sixty Wellsprings by name and House; the twenty-six Categories with alignment tags; the five Crafts; the three Planes and the Veil; Aether, Aetheric Density, Residue, Saturation; Essence, Essence Quality, Signature, Typology; the Soul Crystal's three layers; Lattice Conductivity, Resonant Purity, Continuum Retention; Attraction Force and Obsession Force; the Mechanism Vocabulary; the Domain timeline by Stage; the Trait system including Fusion.

**A term not in the source is originated, and flagged as originated in the notes.** A near-miss (a Stage renamed, a Wellspring misspelt, a Family misassigned, a Category misaligned) is a fail at verification, not a warning.

**The build task.** A canonical term list, `wotr_terms.txt`, extracted from Fracture_of_Worlds.md, the glossary, the Codex Lists sheet, and the Categories page. One term per line with its class. The script checks against it.

---

## §6. Verification

Added to the mandatory pre-delivery run:

- **Check 27, terminology audit.** Every capitalised system term in the draft matched against `wotr_terms.txt`. Unknown terms listed. Near-misses (edit distance one or two from a canonical term) fail.
- **Check 28, narration leak.** Any Grade letter, Stage name, Band, eta, AU/s, EU figure, or Sub-Stat name outside quotation marks, italics, or a marked document block fails.
- **Check 29, the loadout.** The author notes contain a Stat Ledger for every named practitioner (§7) or the run fails.
- **Numbers.** Any figure in the Stat Ledger grepped against Fracture_of_Worlds.md before presenting. If it is not there, it is marked estimate.

---

## §7. The Stat Ledger

Every scene's author notes carry, per named practitioner:

- Stage, Band, Coherence Band, Aether Class, Crystal State going in.
- The stats the scene stressed and the row of §3 each outcome traced to.
- EU spent, as a fraction of reserve if the sheet has no figure, exact if it does. Whether the character crossed below the tenth-of-reserve line Part Nineteen names.
- Crystal State coming out, and any Threshold Event risk incurred.
- What healed by the next scene and what cannot, by the recovery model.

This is the Ledger's mechanical half. The narrative Ledger (injuries, debts, who saw) sits beside it.

---

## §8. Consequential Edits

- **WOTR_Ability_Technique_Design_Guide.md, sixth edition.** Every technique entry carries the FOW line beneath the Codex line: governing Primary Stat and Sub-Stats, Stage floor, Grade required, Path gate if any, Resonant Pair if any.
- **Character sheet template.** Unchanged in sections; §X Techniques gains the FOW line.
- **WOTR_Combat_Craft_Guide.md, third edition.** §3 above becomes its adjudication chapter.
- **The Stat Sheet workbook** becomes a source of truth for numbers alongside the Notion cards, and where they disagree the disagreement is flagged, not resolved.
- **wotr_verify.sh.** Checks 27 to 29. `wotr_terms.txt` built in the same session.

---

## §9. Open Rulings

- **R14-A. Stage names.** Cards use Ignition (I) and Temper (IV); Fracture of Worlds and the Codex use Murmuring and Flourishing. One ruling, then a sweep.
- **R14-B. Sub-Stat names outside a faculty reading.** Recommendation: never.
- **R14-C. Source precedence between the Stat Sheet workbook and the Notion cards** when a number differs.
- **R14-D. Whether Resonant Pair unlocks (Reactive Cast, Seam Sight, Controlled Detonation) may be named on the page in diagnostic voice.** Recommendation: yes, they are exactly what a Measurewright would say.
- **R14-E. Whether an estimate in the Stat Ledger may become canon by default after one session unchallenged.** Recommendation: no; estimates stay estimates until ratified.
