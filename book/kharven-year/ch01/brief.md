# Chapter 1 brief — The Week After

scene_type: talky

## The beat

Outline row, verbatim (book/kharven-year/outline.json, chapters[0]):

```json
{
  "number": 1,
  "title": "The Week After",
  "beat": "Seven days after the signing the instrument has to be entered somewhere, and Nalūn's factor asks the table for a fair copy for Vaultmere while the Bench's clerk asks Yoko Mishiro for her record of the signing night and is refused in one sentence. Sodoku orders the copy made and names Tabitha Hallenfeld to carry it, knowing exactly where the four factors sit, and says in front of Lambert that the road is hers. In the passage behind the hall Brida, on her stick, tells him what a man who has not slept a full night in a year is spending and that it comes due in the Thin Weeks; he answers by asking after her stack and goes back to the grain returns. Miku Tenrai Moto holds his chair through all of it and watches the king's hands rather than his face.",
  "scene_type": "talky",
  "pov": "Sodoku Moto",
  "cast": [
    "Sodoku Moto",
    "Yoko Mishiro",
    "Edward Lambert",
    "Tabitha Hallenfeld",
    "Brida Ashwell",
    "Miku Tenrai Moto",
    "a clerk of the Bench",
    "a factor of the Council of Links"
  ],
  "place": "Kharven-Seat, the lower hall and the passage behind it",
  "front_id": "the-accord-circle-unnamed",
  "plants": [
    "H01-yoko-lines",
    "H02-copy-road",
    "H03-miku-chair",
    "H04-price-of-standing"
  ],
  "pays": [],
  "time_elapsed": "Seven days after the signing; Ice-out",
  "target_words": 3500
}
```

### Hooks this chapter must plant

- **H01-yoko-lines** (planted ch1, due ch12, status planned) — keywords: four lines, Yoko, refused, Bench
  Yoko's four lines about the signing night exist in her own record and the Bench has never been permitted to see them. The Bench's clerk asks and is refused; by the anniversary the king asks and is refused the same way, and does not press.
- **H02-copy-road** (planted ch1, due ch6, status planned) — keywords: Vaultmere, copy, first week, factor
  Sodoku sends Tabitha Hallenfeld south with the fair copy of the instrument for Vaultmere, knowing the four factors sit there. The copy goes into the salt and the road gives her the first order's date.
- **H03-miku-chair** (planted ch1, due ch5, status planned) — keywords: Miku, clause, three hundred, by name
  Miku Tenrai Moto, fourteen, holds a chair at the table by right of a forfeiture and watches the king's hands. The first test of the refugee clause comes from that chair, not from outside: he asks for the three hundred by name.
- **H04-price-of-standing** (planted ch1, due ch12, status planned) — keywords: sat down, Brida, full night
  Brida names what a man who has not slept a full night in a year is spending and says it comes due in the Thin Weeks. Bram would not sit at the signing. At the anniversary Bram sits in the hall and Sodoku sits on the ground by the smallest stone.

### Hooks this chapter pays

None (outline `pays: []`).

### The Front tick

From `python build/book_tools.py fronts Kharven`, the front named in the outline row (`front_id: the-accord-circle-unnamed`):

```
[the-accord-circle-unnamed] The Accord circle, unnamed — ○○○○○ 0/5
  want: four constituents with every reason to hate each other each want the instrument read their way.
  last: signed, Sodoku's hand last.
  next tick: The first test of the refugee clause, by someone who signed it.
```
Bible spine, ch1: the copy leaves the hall. The front ticks when the world moves and the king sees the consequence (bible, "The spine"); the next tick on the Fronts page (the first test of the refugee clause, by someone who signed it) is ch5's, not this chapter's — ch1 makes the instrument leave the hall and the four factors' city receive it.

## Protocol

`desktop/NATALIE.md` applies in full, with these chapter adaptations:

- **No turn-taking.** Table Rule 1's answer-the-PC half is off: nobody is waiting for Isaac's next move. Its ending rule stays: the chapter ends on an NPC line, a physical action, or a thing he can now see; never on a question aimed at him out of character. The bible adds: no chapter closes on the king choosing, because his choices are the outline's.
- **The PC does what the beat says and nothing beyond it.** Sodoku Moto's actions in this chapter (bible, "Isaac's rule for the PC", item 1): orders the fair copy for Vaultmere; names Tabitha to carry it; says in front of Lambert that the road is hers; answers Brida with "how's your stack" and goes back to the grain returns. The writer originates no decision for him beyond those.
- **Length.** The target is the outline's `target_words` (3,500) at the set-piece band (Table Rule 2: set piece 2,500 minimum with full scene standards).
- **One deliberate lie by an NPC** (Table Rule 8; scene-brief blank 6) and **one misreading by the POV character** (R6-4-MISREADING_BUDGET; scene-brief blank 4) per chapter, both declared in the author notes.
- **Standing Inventory**, two recurrences minimum (R6-9-RECURRENCE_RULE). The block below is copied from `python build/book_tools.py session_start "Sodoku Moto" talky Kharven`, the `# STANDING INVENTORY` section only.
- **Previous-scene choice** (recorded here so the writer does not re-derive it): ARCS.md lists the Sodoku Moto arc in filename order and ends on `kaalabad_star_crusher.md`, which the bible places off this book's map; the bible's chronology note names *What the Ground Was Owed* (scene 10) as the latest point in story time and the point the book continues from. §6 below carries the tail of scene 10.

### STANDING INVENTORY

### THE STANDING INVENTORY: KHARVEN (LIVE)

Steppe-riders who stopped riding because the land became permafrost. Food: windmeat, bone broth, the skin (fermented milk carried in sealskin; refusing the skin is an insult), seal fat, the root cache, stonecurd. Greeting: forearm grip, diagnostic. "How's your stack?" Oaths: "By the sky that covers us." "By the fire." Insults: "wet wood," "empty saddle," "cracked bowl." Time: a fire's length, a broth, the Thin Weeks, "when the grass comes." The dead: the death-house, the Waiting, sky burial, "gone to the sky." Objects: the night-stone, the woodpile, the hide-coat, the belt, the blubber lamp. Exchange: meat-sharing, labour-debt, salt. Proverbs, fixed wording: "The sky does not ask whether you are ready." "A full stack speaks louder than a full mouth." "The first bowl goes to the one who cannot fill it themselves." "Wet wood burns eventually. A liar never dries." "The night-stone remembers the fire." "Don't saddle a horse you cannot feed." "The dead can wait. The cold cannot." "Under the sky, everything balances." Body: hands, breath-plume, weight, scent. **Recurrence, two minimum per Kharven scene:** the woodpile and "how's your stack"; the night-stone; "wet wood"; the Thin Weeks; the death-house and the Waiting. Pending entry: "the third bowl" (Brida's shorthand for Class III haemorrhage).

The Accord, Dawi, Moto, Eresse, Expanse and Korvaeth Standing Inventories live at `desktop/inventories/` in the repo (session_start and the MCP's `_inventory` load them by culture automatically; open the file directly if working without the MCP). Anything invented in play gets entered the same session, in the Inventory it belongs to. ◆ Ruled 2026-09-12 (R23-8) and applied: airag is the skin, borts is windmeat, aaruul is stonecurd, the deel is the hide-coat, and the sky-name Tengri is simply the Sky, capitalised and unnamed, as the oaths already have it. The old forms are stale in new prose.

## Rule loadout

`python build/book_tools.py loadout talky` → `prose-law dialogue register pov naming`

`python build/book_tools.py load_rules prose-law dialogue register pov naming --brief`, whole output:

-- 286 rules for tags ['dialogue', 'naming', 'pov', 'prose-law', 'register']

R19-2-BUILT_AROUND  [Pack Nineteen §2]  live
  Scenes are constructed to make Isaac's fixed lines land; the dialogue is never fitted to prose written ahead of it.

R19-2-FIXED_TEXT  [Pack Nineteen §2]  live
  Isaac's submitted dialogue is set as written and never rewritten.

R19-2-NEVER_ALTERED  [Pack Nineteen §2]  live
  Register, rhythm, repetition, fragments, profanity, prosodic marks, line order, and word choice in Isaac's dialogue may never be changed, including for the sake of reading better.

R19-2-PERMITTED_CORRECTIONS  [Pack Nineteen §2]  live
  Only typos, unambiguous verb tense/agreement, required punctuation, and stale canon-term forms may be silently corrected in Isaac's dialogue.

R19-2-WORLD_BREAK_FLAG  [Pack Nineteen §2]  live
  A canon-breaking line in Isaac's dialogue is flagged once in author notes and left standing, untouched, unless Isaac rules otherwise.

R19-3-PROSODY_VERBATIM  [Pack Nineteen §3]  live
  Capitals, stretched vowels, ellipses and repeated punctuation are notation for volume, duration, breath and intensity, and must be reproduced exactly rather than converted into narrative description.

R19-3-TAG_ALONGSIDE  [Pack Nineteen §3]  live
  A narrative tag may be added next to prosodic notation but may never be used instead of it.

R19-4-COMPOSURE_COST  [Pack Nineteen §4]  live
  A character who stays composed under extreme stress is exercising an expensive discipline, and the scene must show that price.

R19-4-ICEBERG_DIALOGUE  [Pack Nineteen §4]  live
  Characters never explain to each other something they both already know.

R19-4-REALISTIC_SPEECH  [Pack Nineteen §4]  live
  Originated dialogue must include false starts and self-repair, interruption, repetition, non-answers, characters talking past each other, trailing off, physical business mid-line, and characters saying the wrong thing, as craft law rather than optional flavour.

R19-4-REGISTER_UNDER_STRESS  [Pack Nineteen §4]  live
  Under stress, a character's speech must get shorter, more concrete, more repetitive, and lose subordinate clauses, uniformly across all characters.

R19-4-WORLD_ANCHORED_SPEECH  [Pack Nineteen §4]  live
  A character's metaphors and idiom must come from their own life and trade, not from an external reference list.

R19-5-COMPOSURE_BAN  [Pack Nineteen §5]  live
  Bars antithesis and parallelism, three-part lists, long subordinate clauses in shouted speech, and perfect syntax from established inarticulate/young/exhausted/foreign characters, and bars every character in a scene from constructing sentences at the same length.

R19-5-SORT_BY_SPEAKER_TEST  [Pack Nineteen §5]  live
  If a stranger could not sort a scene's dialogue lines by speaker with the tags covered, the scene fails as a Pack Nineteen violation, not merely a voice-differentiation warning.

R19-7-CHECK40  [Pack Nineteen §7]  live
  Manual check that every line of Isaac's dialogue matches the submitted rough verbatim except for corrections permitted in §2; any other change fails and is reverted.

R19-7-CHECK41  [Pack Nineteen §7]  live
  Automatic check that fails when the submitted rough has stretched vowels, repeated punctuation or capitalised shouting that the output drops.

R19-7-CHECK42  [Pack Nineteen §7]  live
  Flags long, subordinate-heavy or parallel dialogue lines and reports the spread of line lengths across a scene, flagging files where every speaker clusters at one length.

R19-8-NO_RETROACTIVE  [Pack Nineteen §8]  live
  No rewrite of scenes written before this pack is proposed; the pack governs dialogue written from here forward.

R18-3-CODEX_OVERRIDES_LEXICON  [Pack Eighteen §3]  live
  Pack Sixteen's route-1 rough-prose conversion now means routing to a Codex term, and where the Pack Sixteen §4 conversion lexicon disagrees with the Codex sheet, the sheet wins.

R18-4-GLYPH_NAMING_CONTEXTS  [Pack Eighteen §4]  live
  Glyphs are named only in a document, an instrument, a practitioner's diagnostic voice, or a private count; narration may state what a glyph did without announcing the bracketed form.

R16-1-CONSEQUENCE  [Pack Sixteen §1]  live
  The technical and metaphysical register belongs in the finished narration itself, in Isaac's vocabulary, converted rather than removed or exported to notes.

R16-2-DELETION_REQUIRES_NOTE  [Pack Sixteen §2]  live
  If a rough-draft term does not survive into the finished prose in one of the four routed forms, the author notes must say which term was dropped and why, in one line, or the pass has failed.

R16-2-FOUR_ROUTES  [Pack Sixteen §2]  live
  Every content-bearing noun and verb in Isaac's rough prose is routed to a WOTR system term, a real scientific/technical term, the compound of both, or kept verbatim as a defined WOTR term; nothing is silently dropped.

R16-3-COMPOUND_SENTENCE  [Pack Sixteen §3]  live
  The signature WOTR technical sentence names the real phenomenon, gives the system term as its name/boundary/address, and states the physical consequence, in one sentence or short group; neither element is a gloss on the other.

R16-4-EXTEND_LEXICON  [Pack Sixteen §4]  live
  The rough-to-converted term lexicon is built from Isaac's actual submissions and extended every session; anything converted in play must be entered in it or it does not exist as a settled conversion.

R16-5-NOT_IN_NOTES  [Pack Sixteen §5]  live
  If a mechanism term appears in the author notes but not in the prose, the pass failed and the note is evidence of that failure.

R16-5-REGISTER_IN_NARRATION  [Pack Sixteen §5]  live
  The Technical Register is available to third-person narration for anything a person chooses to do; it is not reserved for italic thought.

R16-5-VOICES_VS_VOCABULARY  [Pack Sixteen §5]  live
  The four explaining voices remain the delivery system for causal explanation only; narration itself may carry technical terms without needing a voice to speak them.

R16-6-COINAGE_COLLISION  [Pack Sixteen §6]  live
  Where a coinage collides with existing canon, the collision is surfaced and both readings are stated, per the standing rule against silent resolution.

R16-6-COINAGE_HANDLING  [Pack Sixteen §6]  live
  A term in Isaac's rough with no canon equivalent is a coinage: it is converted into a defined WOTR term, kept in the prose, given a one-line definition in the author notes, and entered on the Open Rulings Docket for ratification, never silently replaced with a plainer word.

R16-6-SPELLING_VS_VOCABULARY  [Pack Sixteen §6]  live
  Spelling and grammar in Isaac's rough are corrected without comment; vocabulary is never silently corrected.

R16-7-NOT_CONVERTED  [Pack Sixteen §7]  live
  Conversion applies to mechanism, phenomenon, technical read, injury and the physics of an exchange, but never to the body's plain physicality, grief and the elegiac beat, dialogue (outside a practitioner's diagnostic voice or a document), or the ignorance quota.

R16-7-OVERCONVERSION_FAULT  [Pack Sixteen §7]  live
  A scene that converts everything has the same fault as a scene that converts nothing: it has stopped choosing.

R16-8-CHECK30  [Pack Sixteen §8]  live
  A scene with a working, exchange or injury must carry at least four WOTR technical-lexicon terms and at least two correctly-used real scientific/anatomical terms in the narration outside italics; false positives are reviewed by reading.

R16-8-CHECK31  [Pack Sixteen §8]  live
  No mechanism term may appear in the author-notes block that does not also appear in the prose body.

R16-8-CHECK32  [Pack Sixteen §8]  live
  Every distinctive term in the submitted rough must appear in the output in one of the four routed forms, or be listed as dropped in the notes; false positives are reviewed by reading.

R16-8-CHECK33  [Pack Sixteen §8]  live
  Fewer than half of a scene's technical terms may sit inside italic thought.

R15-1-AI_TELL_CHECKS_SURVIVE  [Pack Fifteen §1]  live
  The AI-tell checks (em dashes, similes, not-X-but-Y, countdown negation, gloss, ladder) are about prose failing, not about period, and are unaffected by the register repeal.

R15-1-DICTION_PALETTE  [Pack Fifteen §1]  live
  The one-or-two-elevated-words-per-scene cap is gone; the word bank remains available.

R15-1-ELEVATED_VOCAB_OPTIONAL  [Pack Fifteen §1]  live
  The Elevated Vocabulary Standard stops being a mandate; its words stay available but nobody counts them.

R15-1-LATIN_CHANT_SURVIVES  [Pack Fifteen §1]  live
  Latin for chant-based magic is not a register rule but a texture choice Isaac made, and it stands unless he says otherwise.

R15-1-LICENCE  [Pack Fifteen §1]  live
  Modern words, concepts and frames are legal in every channel of the prose, including narration and in-world documents.

R15-1-MYSTIC_REGISTER_NEVER_PHYSICS_STRUCK  [Pack Fifteen §1]  live
  Pack Twelve §6's clause forbidding a document from explaining mechanism is struck; a document may be as scientific as it wants, and the Mystic Register survives only as an option for documents that want to withhold.

R15-1-RACIAL_VOICE_MENU  [Pack Fifteen §1]  live
  The Racial Voice and Dialect Guide and its Amendment stop being enforced; they become a menu of options a writer may reach for, and no scene fails for ignoring them.

R15-1-READS_MODERN_STRUCK  [Pack Fifteen §1]  live
  Natalie no longer raises, fixes, or notes "reads modern" as a critique on principle.

R15-1-REGISTER_BY_CULTURE  [Pack Fifteen §1]  live
  Per-culture narration registers become optional flavour rather than law.

R15-1-TECHNICAL_REGISTER_SURVIVES  [Pack Fifteen §1]  live
  Packs Twelve, Thirteen and Fourteen's Technical Register for combat and workings is not a register rule in this pack's sense and is unaffected; this pack makes explanation in real terms easier, not harder.

R15-1-VOICE_DIFFERENTIATION  [Pack Fifteen §1]  live
  Characters must remain non-interchangeable, but through what they notice, want and refuse rather than through vocabulary fences.

R15-2-NO_REGISTER_EDIT  [Pack Fifteen §2]  live
  Register is never corrected during editing and alternate less-modern phrasings are never offered.

R15-2-ONE_TEST  [Pack Fifteen §2]  live
  A word is flagged only if it punctures belief in the world, and the flag goes in author notes with the draft left untouched.

R15-4-MEMORY_ENTRIES_SUPERSEDED  [Pack Fifteen §4]  live
  Memory entries thirteen, fourteen, twenty-nine and thirty (accent calibration, phonetic markers, Racial Voice guide, elevated vocabulary) are superseded as mandates and retained only as available technique; flagged for the memory sweep.

R15-4-PACK_FIVE_SCOPE  [Pack Fifteen §4]  live
  Only Pack Five's register-by-culture rule is struck; its dramatic irony through POV lock, the elegiac mode, humour recalibration, and narration authority all stand because none of them are register rules.

R15-4-PACK_NINE_CLASS_MARKING  [Pack Fifteen §4]  live
  Pack Nine's requirement that class show in vocabulary becomes optional.

R15-4-THIRTEEN_HAX_STRUCK  [Pack Fifteen §4]  live
  Pack Thirteen §6's ban on a character saying "hax" is struck; a character may say whatever makes him interesting, though scaling vocabulary stays author-notes-first as adjudication vocabulary, not because it is modern.

R15-4-TWELVE_VOICE_DISCIPLINE_SOFTENED  [Pack Fifteen §4]  live
  Pack Twelve §4's voice discipline clause is softened from a stricter requirement to "may differ."

R15-4-VERIFY_UNCHANGED  [Pack Fifteen §4]  live
  wotr_verify.sh has no check that touches register, and this pack adds none.

R14-4-DIAGNOSTIC_CHANNEL  [Pack Fourteen §4]  live
  Stat names, Sub-Stat names, Grades, Bands, eta, AU/s, EU counts, Aether Class, Crystal State and Category names reach the page only in a mouth, an instrument, a document, or a practitioner's private count, rationed per Pack Twelve §5, and class-marked per Pack Nine.

R14-4-EFFECTS_CHANNEL  [Pack Fourteen §4]  live
  Every stat that decided an outcome must show on the page as behaviour and physics; grade letters and stat names never appear in narration, only their consequences.

R14-4-SUBSTAT_DIAGNOSTIC_ONLY  [Pack Fourteen §4]  live
  Sub-Stat names are the finest grain the system has, and only a faculty reading reaches for them; nobody else does.

R14-5-CANONICAL_TERMS  [Pack Fourteen §5]  live
  The full Fracture of Worlds terminology (Stages, Bands, Tier Grades, Coherence Bands, Aether Classes, Soul Crystal tiers/states, Primary Stats/Sub-Stats, speed components, Resonant Pairs, Threshold/Fracture Events, EU/Flux/AU-s/eta, the recovery model, Families, Wellsprings, Categories, Crafts, Planes, Aether/Residue/Saturation, Essence terms, Soul Crystal layers, Attraction/Obsession Force, Mechanism Vocabulary, the Domain timeline, and the Trait system) is used exactly, with no approximation.

R14-5-NEAR_MISS_FAIL  [Pack Fourteen §5]  live
  A term not in the source is flagged as originated; a near-miss (a renamed Stage, a misspelt Wellspring, a misassigned Family, a misaligned Category) fails verification outright rather than warning.

R14-6-CHECK27  [Pack Fourteen §6]  live
  Every capitalised system term in the draft is matched against wotr_terms.txt; unknown terms are listed, and near-misses (edit distance one or two from a canonical term) fail.

R14-6-CHECK28  [Pack Fourteen §6]  live
  Any Grade letter, Stage name, Band, eta, AU/s, EU figure, or Sub-Stat name outside quotation marks, italics, or a marked document block fails.

R13-4-THREE_EXPLANATIONS  [Pack Thirteen §4]  live
  At first display and finisher, physics, Essence and Hermetic correspondence must each appear as a causal sentence beside its image, not as the image alone.

R13-6-ANATOMY_VOCAB  [Pack Thirteen §6]  live
  Anatomy is named by structure, fractures by fracture type, and neurological consequence by name.

R13-6-ANIME_GRAMMAR_TRANSLATION_AID  [Pack Thirteen §6]  live
  Anime shape-vocabulary (Nen's shroud/stop/output/expression, Naruto's shape/nature split, JJK's vow and reversal, Bleach's release) is used only to identify which shape a working needs, then written in WOTR's own words; it never appears as page vocabulary.

R13-6-CHEMISTRY_BAN_SCOPE  [Pack Thirteen §6]  live
  Pack Six's chemistry ban survives, but only for ambient sensory impression; it does not touch a hit, a wound, or a working.

R13-6-HEMA_VOCAB  [Pack Thirteen §6]  live
  Combat vocabulary draws on the full HEMA range (spear/staff, poleaxe, dagger, grappling, messer, sword and buckler, mounted lance) with a percussion master-strike table built for the hammer specifically.

R13-6-METAPHYSICS_VOCAB  [Pack Thirteen §6]  live
  Correspondence, sympathy and contagion, essence and accident, form and actualisation, and recognition and refusal are the vocabulary of stratum two's Attraction-side reads and of the document voice.

R13-6-REAL_SCIENCE_VOCAB  [Pack Thirteen §6]  live
  Real scientific terms (pressure differential, gradient, latent heat, phase transition, dielectric breakdown, resonance, cavitation, nucleation, information entropy, boundary condition, and the rest) are the vocabulary used to explain what a WOTR noun is doing.

R13-6-SCALING_VOCAB_RESTRICTED  [Pack Thirteen §6]  live
  Scaling-comparison vocabulary (Attack Potency, durability, hax as a concept, speed blitz, reaction vs combat speed, striking vs lifting strength, range, outlier, anti-feat) is used only in author notes and adjudication, never on the page, to keep Natalie honest about who wins and why.

R13-6-WOTR_FIRST  [Pack Thirteen §6]  live
  The glossary and Codex's own nouns (the Planes, Aether, Essence, the Soul Crystal and its layers, Crystal States, Attraction/Obsession Force, the Sixty, the Families, the Categories, the Mechanism Vocabulary, EU/Flux Density/AU-s/eta/Band/Grade/Stage) are used in preference to anything borrowed.

R13-9-STYLE_DIRECTIVE_MECHANISM_VOCAB  [Pack Thirteen §9]  live
  Bare jargon mid-action stays banned, but a Mechanism Vocabulary term may now be named in diagnostic voice alongside its dramatisation.

R12-1-PACK_SEVEN_REPEALED  [Pack Twelve §1]  live
  Pack Seven, the Soft Magic Amendment, is repealed in full; six of its specific provisions are individually struck (see the other §1 rows), and where Twelve conflicts with Seven, Seven is struck.

R12-2-MYSTIC_REGISTER_DEF  [Pack Twelve §2]  live
  The Mystic Register governs Wellsprings, sites, rites, oaths, the Veil, and anything the world does regardless of who is watching; it is stated as law, never as physics — imperative rules, prices given as prices, taboos given without justification.

R12-2-NO_MIXING  [Pack Twelve §2]  live
  A passage that mixes the Technical and Mystic registers reads as a textbook and is the pack's primary failure mode.

R12-2-REGISTER_TEST  [Pack Twelve §2]  live
  If a person chose to do a thing, it is Technical Register. If it was already running before anyone noticed, it is Mystic Register.

R12-2-TECHNICAL_REGISTER_DEF  [Pack Twelve §2]  live
  The Technical Register governs combat, craft, injury and anything a practitioner does on purpose; exhaustive, tactical, delivered in-fight, explaining the read, the fault, the counter, the reserve and why the answer worked, in real vocabulary.

R12-3-DESIGN_CHAIN_RETURNS  [Pack Twelve §3]  live
  The Design Chain (Trigger, Function, Mechanism, Numerical Effect, Target Response, Consequence, Limitation, Weakness, Cost, Counterplay) is fully prose-legal, distributed through the scene rather than workbook-only.

R12-4-VOICE_DISCIPLINE  [Pack Twelve §4]  live
  A Measurewright, a Kharven hunter and an Accord officer explain the same phenomenon in three different vocabularies; which words a mouth reaches for remains class-marking per Pack Nine.

R12-4-VOICE_FOUR_DOCUMENT  [Pack Twelve §4]  live
  An in-world register entry, field manual, or codex line dropped in at a scene threshold (the LotM model), using the Mystic Register and setting a rule the scene then breaks.

R12-4-VOICE_MIXING_RULE  [Pack Twelve §4]  live
  Confirmed by Isaac's ruling: the four explaining voices may mix, whoever is in the scene, picked per scene, with no more than two run in one engagement.

R12-4-VOICE_ONE_POV  [Pack Twelve §4]  live
  Free indirect explanation ceilinged at the POV character's actual competence; an out-of-depth character explains wrong, and a confidently wrong technical explanation is now the primary vehicle for the misreading budget.

R12-4-VOICE_THREE_OPPONENT  [Pack Twelve §4]  live
  A practitioner explains exactly what he is doing to his target while doing it, because he does not believe the explanation will help; the most economical and characterful voice, barred to anyone without standing to be arrogant.

R12-4-VOICE_TWO_SECOND  [Pack Twelve §4]  live
  A present observer who understands what the POV does not, narrating the read to a third party or himself (the Kakashi model); requires an actual reason to be present and talking, best carried by teachers, rivals, Measurewrights, or the Research and Archives Division.

R12-5-NUMBERS_DIAGNOSTIC_ONLY  [Pack Twelve §5]  live
  EU, AU/s, eta, Coherence, Grade and Band numbers may not reach third-person narration on the narration's own authority; they are legal only in diagnostic voice (a faculty reading, a practitioner counting reserve, a document, an instrument, or a speaking character).

R12-6-MYSTIC_GRAMMAR  [Pack Twelve §6]  live
  The Mystic Register's grammar: imperative without justification, price stated exactly with no reason given, correspondence in place of causation, attribution to an uncertain institution, and the recorded failure documented in flat administrative prose.

R12-6-RULES_AS_RULES  [Pack Twelve §6]  live
  The Mystic Register states consequences without offering mechanism (the canonical example: do not carry Object Wellsprings into Site Wellsprings, no mechanism given, a stated consequence, the Guild has buried those who tested it); more sentences are written in that shape.

R12-7-AI_TELLS_RETAINED  [Pack Twelve §7]  live
  The Ladder ban, the Gloss budget of zero, local burstiness, the reification budget, and every AI tell in the checklist survive unchanged; explaining a mechanism is no licence to write badly.

R12-7-IGNORANCE_MISREADING_RETAINED  [Pack Twelve §7]  live
  The ignorance quota and misreading budget survive Pack Twelve intact and become more important as dramatic-irony tools now that explanation is the default; the wrong explanation is now the load-bearing device.

R12-7-LEGIBILITY_BAN_STRUCK  [Pack Twelve §7]  live
  Pack Six's total-legibility ban and blanket interpretation-at-zero rule are struck.

R11-1-TONAL_SPINE_UNCHANGED  [Pack Eleven §1]  live
  Pack Five stands in full; the Western Register still governs characterisation, humour and narration authority. Pack Eleven widens what the page may look like, not what it may sound like.

R11-2-VOCABULARY_TIERS  [Pack Eleven §2]  live
  "The draw, the hum, a standpipe, a housing, the meter, cut off" are common-tongue and prose-legal under Pack Nine's craft-register carve-out; "concentration, density, coupling, eta" are Guild register and document-only.

R11-3-FIREARM_PROSE_LAW  [Pack Eleven §3]  live
  The gun is furniture, not spectacle; no sentence explains why a proofed round defeats proofed plate — the physical account of the hole stays, the causal account is cut.

R11-4-DESCENT_PROSE_LAW  [Pack Eleven §4]  live
  A descent's sensory opening favours the body (feet, teeth, pack weight) over the room; the ignorance quota becomes the ambient condition rather than a per-scene quota, and a misidentified encounter type is the best-shaped disaster the setting offers.

R11-4-WELL_NAMING  [Pack Eleven §4]  live
  Guild register calls it a Core Concentration; common tongue calls it a Well; going in is a descent, and the people who do it are delvers or well-rats.

R10-2-CATEGORY_READ_EXCEPTION  [Pack Ten PART TWO]  live
  A scene's single diagnostic read (the Apparatus Rule's existing budget, not a new one) may be spent naming the category instead of a Wellspring or Family; naming a category doesn't trip Check 20, but it still costs the scene's only read.

R10-2-CATEGORY_REGISTER_DEFAULT  [Pack Ten PART TWO]  live
  Category names sit at Wellspring/Family register, not common tongue, and stay workbook and Codex-line by default.

R10-3-EFFECT_PHYSICAL_ONLY  [Pack Ten PART THREE]  live
  A projected shape's Effect describes only what it looks/does/feels like, never why the Wellspring resolved as that particular shape; if that answer exists at all, it stays workbook, one line, never on the page.

R10-3-UNCHANGED_CONSTRAINTS  [Pack Ten PART THREE]  live
  A projected shape still counts toward the one splash-panel beat per scene (Pack Nine), still costs the one diagnostic read per scene if the category is named, and the ignorance quota/misreading budget are untouched — a POV may see a projected shape and get it wrong.

R9-2-CLASS_MARKED_CRAFT_WORDS  [Pack Nine PART TWO]  live
  Which word a character uses for a craft is characterisation: an Engraver says "the cutting," a Kharven soldier says "a man who can do the writing," and nobody says "Runecraft" aloud except an Accord examiner filling in a form.

R9-2-COMMON_TONGUE_LEGAL  [Pack Nine PART TWO]  live
  A POV may be shown cutting a ward, speaking a working, or pouring a Draft (singing pending Chantcraft's ruling); the common tongue for craft actions is prose-legal, said the way the character would actually say it, while the Accord Latin terms stay document-only.

R9-2-UNTOUCHED_BANS  [Pack Nine PART TWO]  live
  The mechanism gloss ban (Check 20), the metaphysical-units ban (Check 21), the chemistry ban, and the physical-Effect rule are untouched — a line may say a man cut a ward into a doorframe but may not say why the cutting suppressed the Essence.

R9-2-VOCAB_BAN_NARROWED  [Pack Nine PART TWO]  live
  Pack Seven's ban on system vocabulary in prose still binds absolutely against Wellspring names, Family, Physics Domain, Stage/Grade, EU, other metaphysical units, and Codex glyph designations; it no longer binds against the craft register.

R9-3-AURA_AS_FRACTURE  [Pack Nine PART THREE]  live
  Essence discharge reads as broken, shard-edged geometry around the body rather than a soft glow; "it glowed" stays banned, replaced for Stage-display beats specifically, not as a general phenomenon substitute.

R9-3-COST_UNCHANGED  [Pack Nine PART THREE]  live
  The ignorance quota, the misreading budget, and the one-read Apparatus Rule bind a Stage-display beat exactly as hard as any other scene.

R8-12-NAMING_EQUALS_PHENOMENON_STRUCK  [Pack Eight 1.2]  live
  The Ability Guide line "ability naming equals the phenomenon itself, Ruin is Ruin" is repealed by this pack's Section Two.

R8-13-ENTRY_STRUCTURE  [Pack Eight 1.3]  live
  An entry runs, in order: true name and gloss, classification block, release (where carried), description (2-6 sentences), techniques (1-3 functional lines each), cost, limit, counter (mandatory on Signature), what nobody knows, and Codex (one line at the foot).

R8-15-DESCRIPTION_STYLE  [Pack Eight 1.5]  live
  The description is written the way a man teaching it would write it: flat operational prose, no mood, no cadence work, no elegiac register — that belongs in scenes.

R8-21-FIRST_DRAFT_REPEALED  [Pack Eight 2.1]  live
  Pack Eight Section Two's first draft, which set the naming language by filing body, is repealed by the version in this file.

R8-21-NAME_IN_OWN_LANGUAGE  [Pack Eight 2.1]  live
  The true name is in the practitioner's own language; neither the Accord, the Guild, nor the Family has a claim on it, and a register's Latin gloss never appears in the practitioner's own mouth.

R8-21-REGISTER_NOT_ETHNICITY  [Pack Eight 2.1]  live
  A Japonic-sounding name is evidence about a house's linguistic descent and nothing else; this ruling is unchanged from elsewhere.

R8-21-REGISTER_TABLE  [Pack Eight 2.1]  live
  Where a request specifies a register, that register governs and the name is built in it first: Concord/Accord/Guild/Sancta Lux is Latinate; Ketsuen/Japonic houses use Japanese; Korean-register houses use Korean; Büri is Mongolian; Dawi is stressed Germanic-Norse compound; Eresse is Latinate with elvish morphology; Parunic and older strata use Parun etymology.

R8-22-BY_NAME_POETRY  [Pack Eight 2.2]  live
  The by-name, where an art has one, sits after the gloss and is what other characters call it — the one place poetry is allowed.

R8-22-LITERAL_GLOSS  [Pack Eight 2.2]  live
  The gloss is the true name's plain English meaning, flat and literal, no poetry or interpretation; if the literal meaning is dull, the name is wrong and gets rebuilt rather than dressed up.

R8-23-NAME_HIERARCHY  [Pack Eight 2.3]  live
  Naming runs art, then technique, then form; the art carries the character and is spoken once at release then assumed, while individual techniques are spoken every time they are used.

R8-24-RELEASE_MECHANIC  [Pack Eight 2.4]  live
  An art with a true name may carry a release call (imperative verb plus name); it is never required for the art to function, costs a beat for a measurable output increase, and is spoken indistinguishably by a man in real danger or a man showing off.

R8-25-ESCALATION_SUFFIX  [Pack Eight 2.5]  live
  A stronger expression of a known art takes a modifier on the existing true name; new names are reserved for genuinely new arts.

R8-26-GLOSS_DEPENDENCE_FAILS  [Pack Eight 2.6]  live
  A working whose meaning must be glossed for the scene to land is a working that failed; fix the working, not the gloss.

R8-26-GLOSS_NEVER_IN_PROSE  [Pack Eight 2.6]  live
  The gloss never appears in prose, with no translation apposition; the reader gets it from the sheet or from another character explaining it in dialogue for their own reason.

R8-26-NAME_NEVER_NARRATED  [Pack Eight 2.6]  live
  The true name is spoken by a character; it never appears in narration.

R8-26-NO_SELF_TRANSLATION  [Pack Eight 2.6]  live
  Nobody translates their own technique's name aloud, ever.

R8-27-STANDING_TASK  [Pack Eight 2.7]  live
  A naming pass runs per culture; existing techniques already established in prose are flagged, not renamed, cashing the release-and-true-name mechanic pitched since the fifth edition and requiring rewritten first displays across the major cast.

R8-3-WORKED_EXAMPLES_PENDING  [Pack Eight 3]  live
  Two full worked entries (AUCTORITAS in Latin register, KŌMYAKU in Japanese register) demonstrate the new entry format; per the Ratification Ledger, nothing in them is canon until Isaac rules, and the Division's "four hundred and six" catalogued errata count is explicitly self-flagged as an invented, unsized figure.

R8-4-RETROACTIVE_TASKS  [Pack Eight 4]  live
  Folded into the cost audit: re-cut every existing technique entry into the §1.3 structure; add a classification block to every entry from live taxonomy only, flagging any entry with no legal Codex combination; run the §2.1 naming pass per culture, flagging prose-established names rather than renaming; run a drawback pass checking every Cost line against the overuse-strains-him test and the metaphysical-units ban; write Counter lines onto every Signature technique that lacks one.

R6-1-LADDER_BAN  [Pack Six PART I.1]  live
  Two or more clauses of the form "X was Y and Y was Z" in one sentence is an automatic cut, never a rewrite; cut back to the first concrete noun. Restating a concrete observation as an abstraction in the following sentence is barred the same way.

R6-10-INVENTORY_AND_ELEGY  [Pack Six PART II.10]  live
  Pack Five's elegiac register requires a named concrete thing that is gone, and the Inventory is where those things live; elegy without an Inventory is grief for abstractions, which Pack Five already bars.

R6-11-CHECK18_LADDER  [Pack Six §11]  live
  Flags any sentence containing two or more instances of the "was X and the X was" pattern, including is/became/meant variants.

R6-11-CHECK19_APPARATUS_SUBJECT  [Pack Six §11]  live
  Flags any sentence where a named faculty is the grammatical subject of a perception verb; high false-positive rate by design, reviewed by reading.

R6-12-TELL_BANK_SURVIVING  [Pack Six §12]  live
  Added to the AI tells checklist and retained in full per Pack Twelve §7 — the Ladder in all forms, the apparatus as grammatical subject, scientific vocabulary explaining an ambient sensory impression, and fresh texture invented where Inventory texture exists.

R6-2-CHEMISTRY_BAN  [Pack Six PART I.2]  live
  Real-world scientific vocabulary explaining a sensory impression is barred unless the POV is a practitioner of that specific craft actively diagnosing; the Mechanism Standard governs technique trigger points and nothing else, never a licence for ambient exposition.

R6-2-FACULTY_NEVER_SUBJECT  [Pack Six PART I.2]  live
  A named faculty is never the grammatical subject of a perception verb; the character perceives, the apparatus does not act on its own behalf.

R6-2-READ_DELIVERS_FACT  [Pack Six PART I.2]  live
  A faculty's read delivers a bare fact ("Twenty-three"), never an interpretation woven around it; the faculty is an instrument and instruments produce numbers, not meaning.

R6-3-IGNORANCE_QUOTA  [Pack Six PART I.3]  live
  At least one thing per scene the POV notices and cannot interpret; the narration does not rescue him, and resolution comes in a later scene or chapter.

R6-4-MISREADING_BUDGET  [Pack Six PART I.4]  live
  At least one POV inference per scene is wrong and is not corrected on the page; the misreading must be reasonable, consistent with what the POV knows, and left standing for the reader to find later.

R6-5-MATERIAL_DENSITY_SURVIVES  [Pack Six PART I.5]  live
  Material density (rust, weathering, wear, labour) stays described in full per the Directive; the distinction is that the world is described exhaustively but interpreted at zero — meaning and thematic weight are withheld.

R6-9-RECURRENCE_RULE  [Pack Six PART II.9]  live
  Every scene draws texture from the Inventory before inventing anything; anything newly invented is entered into the Inventory the same session or it does not exist; each culture designates three-to-five high-frequency signature items on the Recurrence Ledger.

R5-A-FLESH_CHANGES  [Pack Five A]  live
  Prose register, humour, characterisation method, narration authority and tonal architecture derive from the Western tradition (Martin's POV discipline, Tolkien's cultural register and elegiac capacity, Abercrombie's dry brutality).

R5-A-OPERATIVE_CONSEQUENCE  [Pack Five A]  live
  The system is author-facing and document-facing — it lives in the Codex, character sheets, in-world treatises and technical-reveal beats; it does not live in prose texture, narrator commentary, or character affect.

R5-A-SKELETON_UNCHANGED  [Pack Five A]  live
  WOTR runs an Eastern skeleton under Western flesh; the systematic density (Stages, Wellsprings, Bands/Grades/Coherence/eta, Codex glyph grammar, Family/Physics Domain, the character sheet, the Design Chain, EU costs) does not get diluted, softened, or made impressionistic.

R5-B-DECLARATION_TO_INFERENCE  [Pack Five B]  live
  A character is established by what they choose under pressure, what they refuse, what they notice first, and what others say about them when absent — not by being vividly themselves in every line; the reader assembles the person.

R5-B-FOIL_FUNCTION_SURVIVES  [Pack Five B]  live
  Deliberate moral and rhythmic contrast between paired characters (Merry/Pippin, Sam/Frodo, Tyrion/Bronn, Jaime/Brienne, Glokta/Severard) is Western-native and remains actively tracked.

R5-B-MANHWA_DIRECTIVE_REPEALED  [Pack Five B]  live
  Personality vomiting, reaction shots as characterisation, loud opinions as a default register, bizarre/exaggerated minor NPCs, absurdist method alongside genuine stakes, humour as a tone exception, and escalation as a prose-level pacing register are no longer craft law and become active tells; escalation survives only as plot architecture (Scene Writing Process Guide §2).

R5-B-YOKO_SODOKU_SURVIVES  [Pack Five B]  live
  Yoko against Sodoku is a precision-versus-instinct foil, not a comedy routine; its humour now arrives through what Yoko declines to say, never a deadpan beat landing on a punchline.

R5-C1-INFO_TRACKED_PER_POV  [Pack Five C.1]  live
  Before a scene, name what this POV knows, what they wrongly believe, and what the reader knows that they do not.

R5-C1-NARRATION_NEVER_WINKS  [Pack Five C.1]  live
  No line acknowledges that the reader knows better than the POV.

R5-C1-WELL_REASONED_WRONG_CONCLUSION  [Pack Five C.1]  live
  Irony built on a character being stupid is not irony; a POV must apply sound reasoning to a corrupted premise, not simply be foolish.

R5-C1-WRITE_FROM_LEAST_KNOWING  [Pack Five C.1]  live
  Where a scene could be written from two POVs, write it from whoever knows least about what is coming; a default, breakable with reason.

R5-C2-ELEGY_CONCRETE_THING  [Pack Five C.2]  live
  Elegy attaches to a named concrete, specific thing that is gone (a road, a dye colour, a lost word, a dying craft), never to abstractions; grief for "the old world" is furniture.

R5-C2-FLAT_DELIVERY  [Pack Five C.2]  live
  Section 1.2's saga restraint governs elegy: state the loss and move on, without raising the prose's voice.

R5-C2-IRREVERSIBLE_NOBODYS_FAULT  [Pack Five C.2]  live
  What distinguishes elegy from grimdark's systemic cruelty is that the loss is often irreversible and often nobody's fault; some things are simply taken, some simply end.

R5-C2-ONE_PASSAGE_BUDGET  [Pack Five C.2]  live
  At most one sustained elegiac passage per scene, which may sit anywhere except the closing beat, which still ends on physical action per Scene Standards.

R5-C3-NARRATION_REGISTER_EXTENSION  [Pack Five C.3]  live
  Free indirect discourse's per-character register licence is raised to a per-culture one: proposed narration registers include Dawi (stressed monosyllables, concrete nouns, sentence-level distrust of abstraction), Eresse (subordination, latinate diction, periodic sentences), Concord human (the house baseline), and Moto (to be built, highest-priority gap).

R5-D-FUNERAL_TEST  [Pack Five D]  live
  Could this line be said at a funeral, by someone who means it, without breaking the room? If the humour needs a comedic frame to work, cut it.

R5-D-HUMOUR_BARRED  [Pack Five D]  live
  The beat structure of setup, deadpan and reaction is barred; humour arrives inside dialogue and narration already in progress and never pauses the scene to land.

R5-D-HUMOUR_CASTING  [Pack Five D]  live
  Lambert carries institutional dryness in the debrief; Pietro carries contempt as wit; Yoko is accidentally funny through literalism; Sodoku does not make jokes and should not start.

R5-D-HUMOUR_PERMITTED  [Pack Five D]  live
  Humour is no longer an exception to tone but a property of specific characters in the Abercrombie register: dry understatement, gallows wit from those whose profession earns it, class-inflected contempt, a character being funny without knowing it, and the joke that is also a threat.

R5-E-ELEGIAC_REGISTER_ALLOWED  [Pack Five E]  live
  The elegiac register is available to scene narration because elegy in the saga mode reports a loss rather than judging it; Section C.2's flat-delivery rule is what keeps it on the correct side of the line.

R5-E-ELEVATED_REGISTER_QUARANTINED  [Pack Five E]  live
  The elevated register (invocation, myth-cadence, high style) is available only to in-world documents, songs, oral-tradition passages, mythic strata, prophetic/Celestial Host material, and the opening/closing frame of a mythic-scale event — not ordinary scene narration.

R5-E-FREE_INDIRECT_CARVEOUT  [Pack Five E]  live
  A moral verdict in the POV's own idiom, which could be wrong, is characterisation; the same verdict in the narrator's neutral register is Tolkien's voice and gets cut, per Pack Four's gloss test.

R5-E-MARTIN_WINS_RULING  [Pack Five E]  live
  Martin wins on narration authority: Tolkien's elevated and elegiac register is available, his moral voice is not.

R5-E-NARRATION_NEVER_ADJUDICATES  [Pack Five E]  live
  Third-person scene narration is POV-locked and never adjudicates; no line tells the reader what to think of a character's choice.

R5-F-LIGHT_NOVEL_NOT_KEPT  [Pack Five F]  live
  Status screens, panels and HUD-style rendering (already banned); narrator explanation of the system to the reader; the isekai commentary register (wry narrator asides about the world's rules); and character-sheet vocabulary (Stage, Grade, eta, Band) surfacing in prose.

R5-G-PROJECT_INSTRUCTIONS_EDIT  [Pack Five G]  live
  The Manhwa Energy Directive block is struck in full from project instructions, "manhwa-cinematic" and "manhwa energy" are struck from tone descriptions, and the genre-intersection statement is amended so only the pacing ambition survives.

R5-G-STYLE_DIRECTIVE_EXCLUDED_LIST  [Pack Five G]  live
  The Master Style Directive's §10 deliberately-excluded list gains the Manhwa Energy Directive.

R5-G-STYLE_DIRECTIVE_HUMOUR_POINTER  [Pack Five G]  live
  The Master Style Directive's §4 final paragraph (the manhwa-energy humour clause) is deleted and replaced with a pointer to Pack Five Section D.

R5-G-TELL_BANK_ADDITIONS  [Pack Five G]  live
  Declarative characterisation and the reaction-shot cutaway (from Section B's confirmed repeal) plus the comedic beat structure and narrator moral adjudication (from Sections D and E, still proposed) are added as active tells.

R4-13-DELETION_TEST  [Pack Four Amendment Thirteen]  live
  Delete the candidate sentence and read the passage; if it means the same thing, it was a gloss and stays deleted; if meaning is genuinely lost, the failure is in the line above and that line is rebuilt, never the gloss restored.

R4-13-FID_CARVEOUT  [Pack Four Amendment Thirteen]  live
  A sentence in the POV's own idiom that could be wrong and reveals the character interpreting is characterisation and is kept; a sentence in the narrator's neutral, authoritative register that reveals nothing about anybody's interior is cut.

R4-13-GLOSS_DEFINED  [Pack Four Amendment Thirteen]  live
  A gloss is any sentence whose only function is to state the significance of the sentence before it, disguised as texture or observant narration.

R4-13-THIRD_RECURRENCE  [Pack Four Amendment Thirteen]  live
  A loaded word gets one physical response on first use and no comment; meaning arrives on the third appearance through change — another character uses it, the usual user withholds it, or register makes earlier uses retroactively legible. Withholding is the strongest of the three.

R4-13-THREE_DISGUISES  [Pack Four Amendment Thirteen]  live
  The etymological gloss explains why a character chose a word; the register gloss explains what a tone signified; the stakes gloss restates in abstract vocabulary an event the reader already watched concretely, usually at paragraph-end.

R4-13-WHERE_SIGNIFICANCE_LIVES  [Pack Four Amendment Thirteen]  live
  Significance may live in a physical tell adjacent to the line, in another character's bodily reaction, or in a governed callback — never in narration itself.

R4-13-ZERO_BUDGET  [Pack Four Amendment Thirteen]  live
  The gloss budget is zero per scene; there is no acceptable first instance.

R4-14-APPROACH_LADDER  [Pack Four Amendment Fourteen]  live
  Decelerate into the hit (long, then medium, then the landing) so the reader's eye slows as it arrives, then expand again afterward since consequence is cumulative and belongs in cumulative syntax.

R4-14-CHAIN_CEILING  [Pack Four Amendment Fourteen]  live
  No more than two consecutive sentences may run over 25 words; the third breaks, or the paragraph does.

R4-14-CLAUSE_CAP_AT_BEAT  [Pack Four Amendment Fourteen]  live
  Within the three sentences bracketing a value turn, no sentence carries more than one subordinate or coordinate clause.

R4-14-CONJUNCTION_AUDIT  [Pack Four Amendment Fourteen]  live
  Count coordinators per sentence (and, as, while, which, because); two or more inside a beat-carrying sentence is a fail, though the same count outside a beat is style and left alone.

R4-14-HARD_CEILINGS  [Pack Four Amendment Fourteen]  live
  A payoff sentence carries at most 10 words and zero subordinate clauses; at least 18% of a scene's sentences run under 8 words; and no paragraph closes on three consecutive sentences over 18 words.

R4-14-LANDING_RULE  [Pack Four Amendment Fourteen]  live
  The emotional hit takes the shortest sentence in its paragraph and sits last; anything trailing it is the paragraph clearing its throat after the point.

R4-14-PARAGRAPH_VARIANCE  [Pack Four Amendment Fourteen]  live
  Sentence-length variance is enforced at the paragraph level, not just the document level; the global CV stays as a floor and stops being sufficient on its own.

R4-14-RUN_RULE  [Pack Four Amendment Fourteen]  live
  No three consecutive sentences may fall within forty percent of each other's word count.

R4-15-BODIES_EXEMPT  [Pack Four Amendment Fifteen]  live
  Concrete nouns doing concrete things (hands shaking, a jaw setting, a tail going still) are not counted against the reification budget.

R4-15-CLERK_TEST  [Pack Four Amendment Fifteen]  live
  If the thing could appear as a line on a ledger, in a writ, or in a Bench finding, reify it freely; if it could not, it costs budget.

R4-15-CONCRETE_FIRST  [Pack Four Amendment Fifteen]  live
  Before reifying, check whether an object already in the room can carry the same freight; the object always wins.

R4-15-DENSITY_PROBLEM  [Pack Four Amendment Fifteen]  live
  Reification is a genuine Hermetic-register instrument and any single instance reads well; the failure is density — ten good instances in a scene leave nothing solid for the reader to stand on.

R4-15-LICENSED_CLASS  [Pack Four Amendment Fifteen]  live
  A debt, claim, verdict, name, standing, bearing, holding, writ, seal, title, warrant, attribution or tally is a closed-class WOTR abstraction the world already treats as a thing that moves between hands; reifying these is description, not device, and is unbudgeted and free.

R4-15-NEVER_AT_BEAT  [Pack Four Amendment Fifteen]  live
  Reification is atmosphere and a poor delivery vehicle for a turn; the value flips on a body or an object, never on a personified noun.

R4-15-ONE_PER_PARAGRAPH  [Pack Four Amendment Fifteen]  live
  Two unlicensed reifications in a single paragraph produces a bogged-down feeling independent of the scene total.

R4-15-PROCEDURAL_SCENE_BUDGET  [Pack Four Amendment Fifteen]  live
  In procedural or ledger scenes, the unlicensed reification budget tightens to one per page, since the Licensed Class is already doing that work there and unlicensed instances would go invisible against it.

R4-15-REIFICATION_DEFINED  [Pack Four Amendment Fifteen]  live
  Reification gives an abstract noun a physical verb, handled by characters as an object in the room; the tell is the verb, not the noun (hand, pass, set, carry, place, take, give, hold, put, return, offer, lift, drop, weigh, lay, arrive, land, sit, settle, drain).

R4-15-TWO_PER_SCENE_BUDGET  [Pack Four Amendment Fifteen]  live
  At most two unlicensed reifications per scene, of different abstractions; a third is a fail regardless of quality, and the same abstraction may be reified only once.

R4-15-WATCHLIST_NOUNS  [Pack Four Amendment Fifteen]  live
  Recurring reification offenders, kept greppable rather than felt: silence, weight, arithmetic, governance, permission, distance, authority, refusal, grief, history, patience, the question, the cost, the moment, the space between them.

R4-ADD-CHECK15  [Pack Four Addendum]  live
  Flags etymological, register and "which meant" constructions; warns rather than fails since the whose-vocabulary test cannot be automated, and every flag gets read.

R4-ADD-CHECK16  [Pack Four Addendum]  live
  Fails any chain of 3+ sentences over 25 words, 4+ flat runs, a short-sentence share under 10% (warns under 18%), and reports every paragraph closing long-long-long.

R4-ADD-CHECK17  [Pack Four Addendum]  live
  Fails at 3+ unlicensed reification instances or any paragraph carrying two; licensed instruments are detected, reported separately, and never counted against budget.

R3-7-COZBI_CRAFT_NOTE  [Pack Three Amendment Seven]  live
  An Expenditure fighter is boring to write badly and terrifying to write correctly; refuse the temptation to give him a spectacular exchange — the scene should feel like the opponent is winning, repeatedly, at increasing cost, until the arithmetic arrives.

R3-8-CAVALRY_FIELD_REGISTER_POV  [Pack Three Amendment Eight §14]  live
  A cavalry POV is the only ordinary soldier who can carry the Field Register honestly, since the rider both sees and moves; use for orientation when needed, aware of the cost paid in intimacy.

R3-8-CAVALRY_PURSUIT_FUNCTION  [Pack Three Amendment Eight §14]  live
  Per Section 6, pursuit is butchery of the unresisting from behind at a canter for as long as the horses last; the honest version does not let the cavalry POV enjoy it and does not let them refuse it either.

R3-8-NAVAL_FIRE_WATER_DEATHS  [Pack Three Amendment Eight §12]  live
  Naval death is written as fire and water, not the blade.

R3-8-NAVAL_SENSORY_HIERARCHY  [Pack Three Amendment Eight §12]  live
  At sea the sensory order runs sight, motion, sound, smell (versus land's sound, pressure, smell, sight), because a ship gives a horizon and takes away footing.

R3-8-NAVAL_SIGHT_HELPLESSNESS  [Pack Three Amendment Eight §12]  live
  A sailor's Field Register is available continuously and is rationed by what the character can do about what they see, not by what they can see; write the helplessness of watching rather than the confusion of not seeing.

R3-8-SIEGE_TEDIUM_BY_SPECIFICITY  [Pack Three Amendment Eight §13]  live
  One precisely observed repeated detail carries a month — the same gap in the wall, seen from the same place, on a different day, with something small changed.

R3-9-BEFORE_AFTER_DURING  [Pack Three Amendment Nine]  live
  Before covers the costing-out arithmetic and the decision what to spend and on whom; after covers what the practitioner looks at on a field they made and whether they can name anyone; during, use the soldier, with the practitioner appearing only as weather the POV soldier experiences and doesn't understand.

R3-9-COSTED_OUT_EXCEPTION  [Pack Three Amendment Nine]  live
  The single exception to the practitioner-POV ruling: a practitioner who has been costed out inherits every section-1 constraint the moment their magazine empties, so a POV beginning able to see the whole battle and ending able to see twelve feet is the strongest use of the perspective available — spend it once.

R3-9-PRACTITIONER_POV_RULING  [Pack Three Amendment Nine]  live
  A high-Stage practitioner inside a battle experiences none of the constraints the guide is built on; handing the reader that POV mid-engagement dissolves the fog, pressure and helplessness every other section exists to construct, so the POV is open before and after an engagement and closed during it.

R2-5-RESOLUTION_IN_AFTERMATH  [Pack Two Amendment Five]  live
  The relationship change is legible in how the two characters handle an unrelated later scene; if a character ever says what the act meant, the amendment has been violated and the scene has been spent.

R2-5-SINGLE_ACT_CONDITIONS  [Pack Two Amendment Five]  live
  The Single Act must be physical (a thing done with the body under load, not a decision or realisation), unrepeatable (the circumstance does not recur), witnessed but not discussed during the engagement, and ambiguous at the moment it happens to witness, reader and actor alike.

R1-3-NAME_THREE_RULE  [Pack One Amendment Three]  live
  The one-italic-thought-per-NPC standard is suspended in mass combat; no more than three characters carry interiority through a battle sequence, everyone else is exterior only, and interiority for named characters outside the three is deferred to the aftermath.

R20-1-BEASTKIN_ANCHOR  [Naming Guide Amendment Part One]  live
  Real anchor is Akan day-naming plus the Name-Keeping tradition: a soul-name by birth circumstance, a held name as the last thing that cannot be taken; the soul-name carries an attribute the bearer is expected to embody, and failing it is a strong source of internal shame.

R20-1-CONCORD_HUMAN_ANCHOR  [Naming Guide Amendment Part One]  live
  Real anchor is medieval European byname freezing: a small given-name pool, byname disambiguation, some bynames frozen into surnames, some still live. Frozen surnames read as urban and chartered; live patronymics read as rural and unchartered.

R20-1-DAWI_ANCHOR  [Naming Guide Amendment Part One]  live
  Real anchor is Norse dithematic compounding with Finnish phonology: two-element compound given names from a fixed inventory, patronymic, earned byname. The oath-name is a Dawi-specific fourth slot, audible in the full name or audible in its absence.

R20-1-ELVEN_ANCHOR  [Naming Guide Amendment Part One]  live
  Real anchor is Northwest Coast Indigenous institutional logic: names as heritable property, publicly validated, requiring compensated witnesses, ranked name-holding, names as offices. Content is entirely original; no specific crest, ceremonial or sacred terms from living traditions appear. Avoid generic fantasy Elf naming and Tolkien's specific Quenya/Sindarin phonology.

R20-1-GOBLINOID_ANCHOR  [Naming Guide Amendment Part One]  live
  Real anchor is Germanic compounding with heavy phonotactics: a short given name plus a compound byname describing the force that made the person; the compounding follows rules and bynames may be inherited past the point anyone remembers the original event.

R20-1-MAHUO_ANCHOR  [Naming Guide Amendment Part One]  live
  Real anchor is Korean generational syllables (dollimja): family name first, a two-syllable given name sharing a generation syllable across the cohort, a clan seat distinguishing unrelated families sharing a surname. Avoid Chinese wuxia conventions and given-name-first Japanese conventions.

R20-1-YUKARI_ANCHOR  [Naming Guide Amendment Part One]  live
  Real anchor is Japanese life-stage renaming: childhood name, adult name at coming-of-age, calling name for intimates, true name taboo to speak, posthumous name at death. Avoid modern Japanese casual naming; carry feudal-era court weight.

R20-2-HOLY_SEA_NAMING  [Naming Guide Amendment Part Two]  live
  Birth name (Concord Common) plus ordination name (Latin, chosen or assigned at vows) plus locative/title; a documented name in the Testimony archive carries metaphysical weight, and an undocumented person is theologically uncounted.

R20-2-UNDAAR_KETH_NAMING  [Naming Guide Amendment Part Two]  live
  Given name plus genitive patronymic plus district designation plus, for military personnel, a rank compound that changes with every promotion or demotion, making a Mandate citizen's name a service record; Ironblood Orc citizens carry a hybrid orc-personal-name plus Old Vaross patronymic/district name.

R20-3-CONCORD_GIVEN_NAMES  [Naming Guide Amendment Part Three]  live
  A deliberately small pool of 30 given names (20 male, 20 female) — repetition is the feature, not the bug — combined with patronymic, occupational, locative or descriptive bynames; in a village of two hundred there will be three of the same given name, and the byname is more real than the given name.

R20-3-DAWI_ELEMENTS  [Naming Guide Amendment Part Three]  live
  Thirty fixed-meaning morphemes (endurance, craft, stone/metal, virtue, nature) across five categories, combined two-element with consonant gradation at the join, plus patronymic and earned-byname construction, so a compliant name can be generated in under a minute.

R20-4-ACCORD_FILING_CONVENTION  [Naming Guide Amendment Part Four]  live
  The Accord files every practitioner under given name, family or patronymic, culture of origin, rank designation — a bureaucratic act that is also a cultural act, reducing a five-slot Yukari name to three fields or stripping a Dawi oath-name for lack of a slot.

R20-4-PRONUNCIATION_ADAPTATION  [Naming Guide Amendment Part Four]  live
  When a name crosses cultures, the speaker's own phonology imposes itself (a Concord human flattens Dawi consonant gradation, a Dawi stress-accents a Yukari pitch-accent name); these adaptations should appear in dialogue as characterisation, not be treated as typos.

R20-4-THIRD_NAME_PROBLEM  [Naming Guide Amendment Part Four]  live
  The earned Third Name (documented in The Standing and the Title) is conferred in whatever language the naming community speaks and has no equivalent in the bearer's own register; carrying one means one's identity now belongs to the people who named you rather than the people who bore you.

R20-4-WHEN_NAMES_CHANGE  [Naming Guide Amendment Part Four]  live
  Yukari rename at life-stage; Dawi add the oath-name at oath-taking; Elven validate or strip names publicly; Concord freezes bynames into surnames over generations; Beastkin hold name-keeping as a last resort. Which rule applies when a character moves between cultures is always specific to the characters involved and never clean.

R20-5-FORMAL_ADDRESS  [Naming Guide Amendment Part Five]  live
  A practitioner's formal address follows the convention of whoever is doing the addressing (rank plus family name for the Accord, ordination name plus title for Sancta Lux, relationship-dependent honorifics at a Ketsuen court); two people in the same room may correctly address the same person by different names.

R20-5-ON_THE_PAGE  [Naming Guide Amendment Part Five]  live
  Introduce a character by whatever name the POV character would use (formal on first meeting, personal for intimates, Third Name or physical description for strangers); the narrator does not switch names without a reason, since a name-switch is a statement about the character's relationship to the reader.

R20-5-THIRD_NAME_SUPERSEDING  [Naming Guide Amendment Part Five]  live
  When a Third Name becomes dominant, both the personal name and institutional rank recede — the title becomes the person, and the birth name is what the family uses and nobody else remembers.

R21-1-SATULAGI_STRUCK  [Canon Amendment, Agamalu and Büri Origin I]  live
  The Malō of Sātūlagi does not exist and never did; the Büri hold one seat and it is Kharven.

R22-1-HOUSE_STRUCK  [Moto Reversion Ledger I]  live
  "Büri" and "the Büri bloodline" are struck; "Moto" and "the Moto bloodline" govern.

R22-2-NAMED_CHARACTERS_TABLE  [Moto Reversion Ledger II]  live
  Möngke→Bara, Sarnai→Mizuki, Temür→Sodoku, Muken→Muken (given name was never converted), Saruul→Yukazuri, Chuluun→Sonzai (originated name dissolved, not translated), Enkhtuya→Emira (originated name dissolved), Souma Tsagaan→Souma Byakuya, Artemis Amagiri Büri→ Artemis Amagiri Moto (Amagiri was already Japonic and survives intact) — all with the Moto surname/bloodline where applicable.

R22-2-UNAFFECTED_CHARACTERS  [Moto Reversion Ledger II]  live
  Hild Ice and Robin Ice keep the Stark maternal register; Filemu Agamalu and the whole Agamalu house keep Polynesian register, which the amendment never governed; Tomuka, Ezo, Kuroyuki and Mizuyi were never converted and stay as they are.

R22-3-MONGON_DISPUTE_DEAD  [Moto Reversion Ledger III]  live
  The Möngön against Mönggön spelling dispute is struck from the docket, since it was an argument about a name that no longer exists.

R22-3-SEVEN_LINES_TABLE  [Moto Reversion Ledger III]  live
  Altan→Kōkan (Crown, sovereignty/judgment), Tsagaan→Byakuya (revelation/exposure), Ulaan→Kurenai (punishment/severance), Khökh→Tenrai (convergence/turning points), Möngön→Shirogane (silver), Zes→Akagane (copper), Manan→Amagiri (heaven-mist).

R22-4-KUROSETSU_SCABBARD_SURVIVES  [Moto Reversion Ledger IV]  live
  Kurosetsu keeps the belt scabbard; that was an equipment ruling, not a naming one, and it survives the reversion.

R22-4-SYSTEM_TERMS_TABLE  [Moto Reversion Ledger IV]  live
  Ajiin→Hataraki (the Working), Nüdel→Shingan (the Seeing), Zasag→Kamigan (the Ruling Sight), Iltgel→Meigan (the Revealing Sight), Süldiin→Reigan (the Spirit Sight), Tengeriin→Tengan (the Sky Sight), Khar Ild→Kurosetsu (Black Blade), Ünen→Asami (Truth), Takhil→Gisei (Offering).

R22-5-SEVEN_WORKS_TABLE  [Moto Reversion Ledger V]  live
  Söröl Ajiin→Hametsu no Gō (Ruin), Ariun Ajiin→Junketsu no Gō (Purity), Süld Ajiin→Seirei no Gō (Spirit), Tsagiin Ajiin→Jikan no Shigoto (Time), Mergen Ajiin→Chishiki no Shigoto (Wisdom), Tegsh Ajiin→Shigoto no Baransu (Balance), Bükhel Ajiin→Zentai-sei no Hataraki (Totality).

R22-6-DOCTRINE_COINAGES_TABLE  [Moto Reversion Ledger VI]  live
  Ar Nutag→Okuchi, Bükhel Mörgöl→Sōhai, Ajiin Devter→Hataraki no Sho.

R22-6-SOHAI_LOSES_WORDPLAY  [Moto Reversion Ledger VI]  live
  Bükhel Mörgöl shared its root with the crown Work and the house name, so religion/Work-of-Totality/family were one word and the charge of Singling was levelled in a term that said so; Sōhai does not do that — the one genuine cost of the reversion.

R22-7-FUSI_VA_KEPT  [Moto Reversion Ledger VII]  live
  Fusi Vā, the Agamalu binding rite, replaced Saishiki (a Japonic word on a rite that is Agamalu in origin and Vāimoana in provenance, wrong for both registers on its own terms); the Büri amendment isn't what made that change correct, so it stays kept.

R23-1-POLYNESIAN_REGISTER_STRUCK  [Inner World Naming Amendment I]  live
  Samoan phonotactics, the fa'amatai title system, the aiga, the Ava-name slot, the gafa, and every Moto name built from them are dead; the Polynesian register survives nowhere in the Inner World naming baseline (the Agamalu house's own naming is a separate question, not an Inner World register — see notes).

R23-10-CHINESE_CONTACT  [Inner World Naming Amendment X]  live
  A hall child fostered into a Banner House keeps the surname and drops the generation character, and the hall records the omission — a small, quiet, permanent thing to do to somebody.

R23-10-CHINESE_PHONOTACTICS  [Inner World Naming Amendment X]  live
  Open syllables, permitted nasal codas, no clusters; avoid the wuxia register the base guide already warns off — no four-syllable given names, no sect-title constructions, no honorific stacking.

R23-10-CHINESE_SLOTS  [Inner World Naming Amendment X]  live
  Surname (one syllable), generation character (fixed decades in advance by a lineage-hall poem, revealing relative seniority on first exchange), given character (the individual half), courtesy name (taken at capping, adult use — using someone's given name past that point is a superior's privilege or a deliberate insult), studio name (optional, self-chosen, for scholars/physicians/ alchemists), and posthumous name (conferred by the hall, occasionally an insult).

R23-10-TELLING_APART_KOREAN  [Inner World Naming Amendment X]  live
  A hyphen means Mahuo (Korean); no hyphen means the lineage halls (Chinese). A hollow-seat means Mahuo; the halls use the book instead. A courtesy name means the halls; no Mahuo character has one. A two-syllable surname means neither register — that's Japonic.

R23-11-CARRIED_NAME_MECHANISM  [Inner World Naming Amendment XI]  live
  A name is not a label but a person; when someone dies the name is held unspoken until given on to a child, who carries the same name, not a memory or tribute, and is treated accordingly by everyone who loved it.

R23-11-CONTACT_RULES  [Inner World Naming Amendment XI]  live
  A Far-Northern child fostered south keeps the carried name but simply stops hearing it used, and the kin-turns lapse; giving a carried name to an outsider makes them a specific dead person, with all the kin-turns, binding the household without individual consent.

R23-11-KIN_TURN  [Inner World Naming Amendment XI]  live
  A woman whose mother's name is given to her newborn daughter calls that infant "mother," and means it, and the settlement uses the term with her; names are not gendered, and a person may carry several, each bringing its own kin-turn.

R23-11-NAME_AVOIDANCE_WAITING  [Inner World Naming Amendment XI]  live
  The name of the recently dead is unsayable until given on; the Waiting is the silence — the body waits in the death-house because the ground is frozen, and the name waits with it, leaving a hole in the household's vocabulary that everyone steers around.

R23-11-PHONOTACTICS  [Inner World Naming Amendment XI]  live
  Three vowels (a i u) with phonemic length, uvulars as the signature (q where another register takes k), velar/uvular fricatives, geminate consonants across syllable boundaries, no onset clusters, heavily suffixing with meaningful morphemes, light and late stress.

R23-11-ROLL_NAMES_FROM_ACCORD  [Inner World Naming Amendment XI]  live
  There never was an inherited surname; the Accord's registers assigned a frozen surname off the nearest legible thing (Ice, Foss), so a Far-Northern character has a roll-name the Accord/muster/tax survey use and a separate carried name the household uses.

R23-2-CHINESE_STRATUM_SUMMARY  [Inner World Naming Amendment II]  live
  One-syllable surname, a generation character from a poem fixed centuries in advance, a courtesy name taken at capping for adult use, and an optional studio name for scholars.

R23-2-FAR_NORTHERN_STRATUM_SUMMARY  [Inner World Naming Amendment II]  live
  No inherited surname at all; a name is a person, held by the dead and given on to the living, with kinship terms following the name instead of the blood.

R23-2-JAPONIC_STRATUM  [Inner World Naming Amendment II]  live
  Full life-stage slots, name-taboo on the living, compound topographic surnames, renaming at promotion or vow or change of allegiance (Sodoku Moto, Ayame Yuno, Niran, Jinmu Yukari).

R23-2-KOREAN_STRATUM  [Inner World Naming Amendment II]  live
  Lineage name first, a two-syllable given name carrying a generational syllable shared across a cohort, plus a hollow-seat subdividing the lineage (Kwon Mu-jin, Cozbi Mahuo, Ara Min Mahuo).

R23-2-NORTHERN_STRATUM  [Inner World Naming Amendment II]  live
  A small given-name pool producing constant disambiguation by trade, a frozen surname if the family is chartered and a live patronymic if not, plus an earned byname available to anyone (Bram Greymane, Edward Lambert, Hild Ice).

R23-3-STRATUM_FOLLOWS_INSTITUTION  [Inner World Naming Amendment III]  live
  Which stratum a character's name belongs to is decided by institution (archaic bloodline, record-keeping house, Accord filing, or the dead) — never by geography and never by blood; the rule retcons nothing, since every existing name already obeys it.

R23-4-MIXED_PARENTAGE  [Inner World Naming Amendment IV]  live
  A character of mixed parentage takes one naming register rather than blending; Hild Ice is the model — a Moto father, a Stark mother, a maternal Northern name carried openly, needing no explanation.

R23-4-RENAMING_IS_JAPONIC_ONLY  [Inner World Naming Amendment IV]  live
  Renaming at change of allegiance does not travel into the Northern stratum, where a man who changes sides keeps his name; this is why the Greymane split has no naming event and the Moto exile does.

R23-4-SERVICE_TRANSFERS_REGISTER  [Inner World Naming Amendment IV]  live
  A retainer raised inside a bloodline house may be given a house-register name, and the giving is an event with a cost attached.

R23-5-OUTLIER_BUDGET  [Inner World Naming Amendment V]  live
  Roughly one outlier in eight named characters, each with a reason that exists in the workbook whether or not it reaches prose; above that ratio the registers stop reading as systems and start reading as an author picking names he liked.

R23-5-OUTLIER_DEFINED  [Inner World Naming Amendment V]  live
  A name is an outlier when it fits no stratum (foreign fostering, a mother's whim, a bought name, an insult or shield name); Bram is the standing example and needs no justification on the page.

R23-6-UNTOUCHED_REGISTERS  [Inner World Naming Amendment VI]  live
  Dawi (Norse dithematic/Finnic), Elven Peoples (Northwest Coast institutional logic, the Eressean/Varrisak transfer schism), and Goblinoid (Germanic compounding) are none of them Inner World registers, and none are affected by this amendment.

R24-1-FLESHSHAPER_GOVERNING_PRINCIPLE  [Racial Voice and Dialect Guide Amendment I]  live
  Fleshshaper Goblin register is governed by the fact that they are surgeons who talk like surgeons never told to be squeamish about it.

R24-1-FLESHSHAPER_IDIOM_AND_MARKERS  [Racial Voice and Dialect Guide Amendment I]  live
  Anatomy applied to everything, not as metaphor but as their actual vocabulary (a seam, badly sutured, swelling, opened, holds under load); exactly two phonetic markers — dropped final -g on gerunds, and "th" hardening to "d" only in unstressed grammatical positions.

R24-1-FLESHSHAPER_SIGNATURES_AND_TELL  [Racial Voice and Dialect Guide Amendment I]  live
  Signature lines "That closes" (anything settled) and "Who holds it?" (their first question about any structure); under stress they become more procedural, not less, shortening to pure sequence with the reasons dropped.

R24-1-FLESHSHAPER_SYNTAX  [Racial Voice and Dialect Guide Amendment I]  live
  Short declarative clauses in working order, sequence first and reason second or not at all; they front the object ("The arm, I open here"), naming the thing being worked on before the working.

R24-2-ELADRIN_GOVERNING_PRINCIPLE  [Racial Voice and Dialect Guide Amendment II]  live
  Winter Eladrin are not silent; speech is the least of what they are doing, and the prose has to carry the rest through distance and stillness.

R24-2-ELADRIN_IDIOM_AND_SIGNATURES  [Racial Voice and Dialect Guide Amendment II]  live
  Idiom draws on weather, season and the behaviour of cold as literal analytical vocabulary (thawing/set, keeps, melted, tracked); signature lines "It keeps" and "You have moved"; under stress stillness increases and the distance grammar stops entirely.

R24-2-ELADRIN_NEVER_BARE_LINE  [Racial Voice and Dialect Guide Amendment II]  live
  Never write an Eladrin line of dialogue without a distance or stillness beat attached; a bare Eladrin line is an incomplete sentence in their language.

R24-2-ELADRIN_SYNTAX_AND_MARKERS  [Racial Voice and Dialect Guide Amendment II]  live
  No contractions ever, present tense for permanent conditions, questions phrased as statements with an expectant pause, no interrupting or overlapping; zero phonetic markers, deliberately — their unaccented perfection is enormous effort read as coldness.

R24-2-ELADRIN_THREE_CHANNELS  [Racial Voice and Dialect Guide Amendment II]  live
  Prose must render at least two of three simultaneous channels in any exchange of consequence — sparse speech that rarely carries the content, distance (approach is agreement, a half-step back is objection, turning without moving the feet is refusal), and stillness (complete stillness is often the loudest thing in the room).

R24-3-HOST_BREAKS_ON_MAXIM  [Racial Voice and Dialect Guide Amendment III]  live
  Any Host line that could appear on a temple wall has failed; if it scans as a maxim, cut it and replace it with a report.

R24-3-HOST_CORE_DEVICE  [Racial Voice and Dialect Guide Amendment III]  live
  A Host gives an answer that is correct and unusable, aware of this and unable to do anything about it — accurate rather than confident, which is what stops them sounding like scripture.

R24-3-HOST_GOVERNING_PRINCIPLE  [Racial Voice and Dialect Guide Amendment III]  live
  The Host is not speaking scripture; they report accurately, and their difficulty is that accuracy in their register does not translate into a mortal one.

R24-3-HOST_IDIOM_AND_SIGNATURES  [Racial Voice and Dialect Guide Amendment III]  live
  Idiom draws on measure, position and law (out of position, standing, no place, release a claim); light/fire/wings are banned as too obvious; signature lines "That is not the question" and "I do not have that"; under stress the Host becomes more precise and slower, with hedges appearing for the first time.

R24-3-HOST_SYNTAX  [Racial Voice and Dialect Guide Amendment III]  live
  Declarative, present tense, unhedged — never "I think" or "perhaps"; short flat subject-verb-object sentences; they answer precisely the question asked, not the question intended, which is where every conversation with the Host goes wrong.

R24-N-OVERRIDE_CAVEAT  [Racial Voice and Dialect Guide Amendment Notes]  live
  All three registers are originations contradicting no existing lore (none existed); if any culture has established speech in an unreached document, these are overridden by it.

R32-1-ZETTARI_REGISTER_SWAHILI_BANTU_ARABIC  [Zettari Naming Register Ruling Standing Ruling]  live
  The Zettari bloodline's names, titles and technique names are built in a Swahili/Bantu/Arabic-flavoured register, and that register stands. The five-strata naming convention's assignment of "archaic bloodlines" to the Japonic stratum does not reach the Zettari: they are their own register, a carve-out, not a repeal. The Japonic assignment continues to govern every other archaic line (Moto, Yukari, Yuno).

R33-1-ZETTARI_AGANO_SAND_WITNESSED_TEMPER  [Zettari Forge Culture Ruling Standing Ruling]  live
  The Zettari forge culture answers "what makes a thing trustworthy?" with witness and inheritance, not time: a Zettari-forged object is declared reliable once, before a witness older than the speaker, and the bloodline's Material Covenant Resonance holds the declaration in place. The substrate is Agano Sand ("covenant", Swahili-derived, inside the Zettari's own register), a working measure of the Paths' sand -- condensed lineage memory -- folded into the quench. It is access-gated rather than time-gated: it must come from, or through, someone the Paths already recognize. The rite is the Witnessed Temper, a Vow Clause working and not new magic: at the quench the smith or the sovereign the piece is for speaks a bound claim over the object before a Stone Witness (a ruin, an ancestral hall, a Path-linked relic), and the claim becomes a standing law the object runs. Write it as witnessed law, set against the Dawi's brewed endurance; the cross-culture parallel slot is deliberately left open.

R33-2-ZETTARI_WITNESSED_TEMPER_ITEM_BEHAVIOUR  [Zettari Forge Culture Ruling Standing Ruling]  live
  A Witnessed-Tempered piece inherits a scaled-down Ancestral Dominion Frame: every significant strain it survives in the hands of whoever it was sworn to makes it measurably more resistant to that same kind of stress thereafter, and the hardening plateaus the way the bloodline's own combat maturity does. If the piece changes hands outside the terms of the oath its accrued memory does not transfer -- the cost falls on the object's recognition of the new holder, not on the oath-breaker's Crystal Coherence as with the Dawi -- and in the worst documented cases Physical Plane Authority's "hold shape" reverses for that bearer alone, making the piece more failure-prone in their hands than an ordinary equivalent. Trade entry, Standing Index format: Agano Sand, T4, provenance restricted, Class III / Fidelity A / Carry 26, price 26.0; sourcing requires a lineage-acknowledged Zettari's sponsorship, and no smith outside Kushara has explained why the sand only "listens" to a claim spoken over stone older than the speaker.

R35-1-NARRATION_DISTANCE_BANDS  [Narration Distances (Psychic Distance by POV) The three registers]  live
  Every POV character carries one of three narration distances — close (narration fuses with the character's own idiom, italicized direct thought available), medium (POV locked, no head-hopping, but emotion arrives by external behaviour or simile, no italicized thought) or distant/formal (an omniscient epigrammatic voice describes the character from outside, occasional aphoristic italics, the one register licensed for more narratorial explanation) — and the field is called "narration register", never "Band", because Band is the unrelated FOW Coherence stat. This supplies the whose-idiom input that R4-13-FID_CARVEOUT depends on.

R35-2-NARRATION_DISTANCE_ASSIGNMENTS  [Narration Distances (Psychic Distance by POV) Close register / Medium register / Distant-formal register / Unassigned]  live
  Close register: Darius, Aurelian, Verinus, Charles, Sodoku Moto, Niran Yukari, Wren, Kwon Mu-jin. Medium register: Rengai. Distant/formal register: Cozbi Mahuo. Each assignment carries a violation caution (never a narratorial verdict Darius does not voice himself; never validate Aurelian's certainty from outside his idiom; no neutral Church register for Verinus; no practitioner's jargon for Charles; no interpretive-summary sentences past Sodoku's procedural read; Niran's feeling only through his clinical vocabulary; Wren laconic and tactical only; Kwon Mu-jin's failing read shown from inside; no retrofitted first-person italics or verdicts for Rengai; Cozbi's explanation stays inside his self-mythologizing frame). Hild Ice and Dabney are unassigned until scenes in their own idiom exist for Isaac to rule on.

R37-1-MAHUO_ELEMENT_INVENTORY  [Naming Guide Amendment / Element Inventories I. Mahuo]  live
  A Mahuo given name is two syllables drawn from a fixed thirty-element inventory in five categories (breath and soul, Ledger and record, house and clan-seat, precision and correction, care and healing); one syllable is the generation-syllable shared across a cohort, the other is personal, either may take either position, and the family name may precede or follow since canon attests both orders. Which syllable is generational in the attested pairs, and whether Kwon is a Mahuo cadet branch, stay open flags.

R37-2-YUKARI_ELEMENT_INVENTORY  [Naming Guide Amendment / Element Inventories II. Yukari]  live
  A Yukari name is a two-element compound drawn from a thirty-element inventory in five categories (thread and fate, crow and silence, divine and dream, water/stone/grief, weight and office), and a full name carries up to five life-stage forms: childhood name, adult name taken at the Telling, calling-name, taboo true name, posthumous name. Only Ketsu, En, Jin and Mu are canon-attested; the rest are coined to the register. Whether individuals carry a second topographic surname beside "Yukari" stays an open flag.

R37-3-ELVEN_BRANCH_ELEMENT_INVENTORY  [Naming Guide Amendment / Element Inventories III. The Elven Branches]  live
  The five elven branches (Eressean, Varrisak, Drow, Eladrin, Echo Elves) share one root inventory and one affix inventory drawn from the Vey-Elarin grammar, plus one new branch-specific root each (kalen, sova, morel, faelo, verath); roots are disyllabic and open with restricted codas and every element carries a pitch contour. Branch divergence is shown on the same root, not by five separate lists. The root marin stays unglossed, and the clash with already published apostrophe-style Eressean-adjacent names stays an open flag.

R37-4-BEASTKIN_SOUL_NAME_INVENTORY  [Naming Guide Amendment / Element Inventories IV. Beastkin]  live
  A Beastkin soul-name is a circumstance-element (how the birth went, Akan-day-name style) spoken together with an expectation-element (the attribute the child is charged to grow into, flavoured by lineage stat), and the held-name is whichever fragment survives when home, rank and kin are gone; a third layer supplies the Name-Keeping ritual vocabulary. Whether the four non-Fox lineages actually practise Name-Keeping, and whether soul-name and held-name are one name or two, stay open flags.

## Docket

`python build/book_tools.py check_docket prose-law dialogue register pov naming`:

```
-- 1 pending/proposed for ['dialogue', 'naming', 'pov', 'prose-law', 'register']

R20-2-CELESTIAL_HOST_NAMING  [Naming Guide Amendment Part Two]  pending
  Proposed structure is a function-name plus a rank-suffix plus a permanent Lawbell-name declaring which Archonic principle the Celestial serves; current working names are placeholders pending a full naming pass.
```

Assessment: the one pending item (R20-2, Celestial Host naming) concerns Celestial name structure and touches nothing in a Kharven table chapter with no Celestial in it. Nothing on the docket changes what this chapter must do. No ESCALATE.

Standing flags the writer must still respect (bible, "Flags"): the circle has no name in prose; Hild's roll-name is an open ruling (her stone reads *Hild Ice, twelve years old*, nothing more); the Lambert postern line is blocking on the Docket and is never raised; R14-A (no Stage names on the page) and R14-F (Renard, off-page this chapter) are open conflicts; Robin Ice's age stays off the page; Miku's temporal is never written from inside.

## Scene brief

`python build/book_tools.py scene_brief "<beat>" --thread "Sodoku Moto" --type talky --culture Kharven --cast ...` — header, then everything from "## Fill before drafting" to the loadout (the loadout itself is §3):

### SCENE BRIEF — talky — Sodoku Moto
Beat: Seven days after the signing the instrument has to be entered somewhere, and Nalūn's factor asks the table for a fair copy for Vaultmere while the Bench's clerk asks Yoko Mishiro for her record of the signing night and is refused in one sentence. Sodoku orders the copy made and names Tabitha Hallenfeld to carry it, knowing exactly where the four factors sit, and says in front of Lambert that the road is hers. In the passage behind the hall Brida, on her stick, tells him what a man who has not slept a full night in a year is spending and that it comes due in the Thin Weeks; he answers by asking after her stack and goes back to the grain returns. Miku Tenrai Moto holds his chair through all of it and watches the king's hands rather than his face.

#### Fill before drafting (author notes)
1. POV: ____  (write from whoever knows least about what is coming, R5-C1-WRITE_FROM_LEAST_KNOWING; a default, breakable with reason)
2. This POV knows: ____ | wrongly believes: ____ | the reader knows that they do not: ____  (R5-C1-INFO_TRACKED_PER_POV)
3. Ignorance quota, one thing the POV notices and cannot interpret, unresolved this scene: ____  (R6-3-IGNORANCE_QUOTA)
4. Misreading, one confident inference that is wrong and stays wrong, well-reasoned: ____  (R6-4-MISREADING_BUDGET, R5-C1-WELL_REASONED_WRONG_CONCLUSION)
5. What it costs, specific and visible (reserve, body, debt, reputation, who saw): ____  (Table Rule 5; R12-1-PACK_SEVEN_SURVIVORS)
6. The lie: one thing an NPC says that is wrong and stays uncorrected (once per session): ____  (Table Rule 8)
7. Standing Inventory, two minimum (Kharven): ____ and ____   (R6-9-RECURRENCE_RULE)  — pick from: the woodpile and "how's your stack"; the night-stone; "wet wood"; the Thin Weeks; the death-house and the Waiting
8. Ends on: ____  (physical action, an NPC line, or a thing he can now see; never a question at Isaac. Table Rule 1)
9. Length band: ____  (conversational 300–700 / standard 700–1,500 / set piece 2,500+; default the middle. Table Rule 2)

#### FOW lines (never invent a number)
### Sodoku Moto  (Volume I — Character Cards/Sodoku Moto.md)
> **Level 320 in a Stage VI body.** Two to four Grade brackets past what his Crystal has certified, and a Coherence Band of **D**, which is what that costs.
| **Level** | **320 / 500** · Band IV — Mythic (301–400). *Flag: normally clusters Stage XI–XII. He is genuinely Stage VI* |
| **Coherence Band** | **D** — *his Aether Class and η read higher than Band D typically supports. Same outpacing anomaly, not a separate error* |
| **Aether Class** | **II — Harmonic** (Band D, ~15–25% loss) |
#### IV–V · Stats
> Every Grade below is recomputed against the universal Tier Grade table **and lands several brackets above both the codex's original letters and the nominal Stage VI ceiling of 400.**
>
> *Not a transcription error. The named tension of his arc — bloodline-compounding and five years of forced survival growth outpacing formal Temperance advancement.*
| Stat | Value | Grade | Peaks |
|---|---|---|---|
| **Gnosis** | **1,050** | **X** *(codex: S)* | Acuity 1,080 · Analysis 1,065 · Retention 1,020 · Sapience 990 |

### Yoko Mishiro  (Volume I — Character Cards/Yoko Mishiro.md)
| **Level** | **145 / 500** · Band II — Awakened. *Gated on reaching Stage VII to pass Level 200* |
| **Tier of Standing** | **5, Expert** · η ≈ 0.60 — *"the Crystal has learned to stop leaking"* |
| **Soul Crystal Tier** | **Resonant**, progressed from Harmonic. *In-world shorthand among those who knew her before is still Kindled* |
#### IV–V · Stats
*Verified against Level 145's real point economy — roughly 2,800 held across seven stats at a B-Grade floor, and roughly 1,300 concentrated into the Harmonics family: the fox-spirit anomaly that has never once tracked with her Level.*
| Stat | Value | Grade | Peaks |
|---|---|---|---|
| **Harmonics** | **345** | **A** — ANOMALOUS | Attunement 350 · Memory 346 · Confluence 342 · Fidelity 335 · Stability 330 |
| **Gnosis** | 260 | B | Perception 275 · Analysis 268 · Retention 258 · Forecast 250 |
| **Dexterity** | 245 | B | Celerity 255 · Economy 248 · Reflex 240 · Evasion 235 |
| **Vitality** | 210 | B | Constitution 220 · Fortitude 208 · Endurance 205 · Threshold 200 |

### Edward Lambert — The Arithmetic  (Volume I — Character Cards/Edward Lambert — The Arithmetic.md)
> **Level:** 142 · **Stage:** III Hold · **Band:** II
Edward Lambert is a **Level 142, Stage III Hold** practitioner. This is not impressive. This is the ceiling of a man who trained daily because the training was the requirement and who reached the level that competent daily training produced and who never pushed past the level because pushing past the level required the specific obsession with power that Lambert did not possess, because Lambert's obsession was not power. Lambert's obsession was the count.

### Tabitha Hallenfeld — The Road Woman  (Volume I — Character Cards/Tabitha Hallenfeld — The Road Woman.md)
> **Level:** 28 · **Stage:** 0 (unpracticed) · **Band:** 0

### Brida Ashwell — The Warm Diagnosis  (Volume I — Character Cards/Brida Ashwell — The Warm Diagnosis.md)
> **Level:** 45 · **Stage:** I Ignition · **Band:** I

no card for 'Miku Tenrai Moto' in the wiki mirror; check Notion before writing anything numeric about them

no card for 'a clerk of the Bench' in the wiki mirror; check Notion before writing anything numeric about them

no card for 'a factor of the Council of Links' in the wiki mirror; check Notion before writing anything numeric about them

## Previous chapter

Chapter 1 has no `final.md` behind it. The tail below is the last 1,490 words of the prose body of `scenes/10_wotr_what_the_ground_was_owed.md` (*What the Ground Was Owed* — "Kharven. The year after."), raw, cut at a paragraph boundary, author notes excluded. This is the last scene in story time for the Sodoku Moto arc (bible chronology note); the book continues from it.

---

Robin Ice stood on that path for what he later put at four seconds.

Then he said "Aye," and turned his horse, and rode, and did it, and has never once said in any hall that he questioned the order, and has told two people privately that he did not, and both of them believe him, and the reason they believe him is that Robin Ice is a runner and a runner who begins weighing the traffic stops being one.

Brida Ashwell watched the boy go down the path.

"Edward."

"No."

"I have not said anything."

"You have been standing beside me for a quarter of an hour and I have heard all of it."

She let a moment go past.

"Your brother would have."

"My brother," said Edward Lambert, "is a hole in an ordination roll." He was still looking down the path. "And he did whatever it was he did, and nobody knows what it was, and there is no version of the man left that anybody can appeal to. Not by me, not by you, and not by the four hundred and six."

"And if there were."

"Then I would still have given the order," he said, "and I would have had to look at him afterward, and I have been spared that, and I would like it noted that I am aware of what I just said."

He put his gloves on properly and went down to the hall and sat the afternoon council and asked the correct questions about grain.

Bram Greymane stood over the commander of the Third Ashfold in the lower yard of the Stormfold hall on the eleventh day of the tenth month with a cup of something hot in his good hand.

Vresk Dokkan of Kaadre-Six had been Vorruk-Kaan for eleven years. In Old Vaross a name is a service record: given name, patronymic, district, and the rank compound, and only the compound changes in a lifetime, and it changes at every promotion and every demotion, so that any hobgoblin in the Expanse hearing a man's name hears exactly what the institution currently thinks of him. *Vorruk*, ground that tried to move and was stopped. *Kaan*, the hand set to a thing.

The officer whose function is holding ground. Eleven years, and never once given a compound that meant taking any, and he had been sent north to take some, and he had broken forty feet of the Kharven wall in four nights of patient work under a shed roof of his own making, and had then met three hundred men in a gap twenty-two feet wide.

Bram crouched so their faces were level, which took him a while now because of the hip.

"Remember when your men took my fingers."

He held up the left hand. Three stumps at the second joint, healed hard and shiny, the skin over them still bright pink at eleven months.

"You might be asking why I've taken my time to mutilate every bit of you."

He had. He had taken eleven days. It had begun with a fingertip and had gone on from there in a specific order, and the order had a document behind it, and the document was a roll.

"I've taken a fingertip, then all of your toes, for each of my comrades who died during this war."

There were more names on the roll than there were extremities on a hobgoblin, and Bram Greymane had known that on the first morning and had gone ahead anyway, and had moved to other things when he ran out, and had entered each one against a name, and the roll is in the Stormfold book with a mark beside every entry in a hand with three fingers missing from it.

Egil Vald is on it. Cass Holloway is on it, from the depositions, entered by a man who never met him.

Wren Greymane is not on it, and the omission is deliberate, and Bram has never explained it.

"I don't want to kill you."

He said it without heat. That is the thing everyone who was in that yard has said since: there was no heat in any part of it, at any point, on any of the eleven days.

"I am going to return you back to the Hobgoblin Imperials, so they'll see what I've made of their commander."

And that is the cruelty, and it is not the mutilation, and Bram Greymane knew exactly what he was doing because Lambert had briefed him on Old Vaross naming in the fourth month and Bram had listened.

A hobgoblin's name is his record. Vresk Dokkan was going back alive, and the Keth-Gorrum would have to look at what came through the gate, and would have to give him a compound, because a returning officer is renamed and there is no provision anywhere for declining to.

And there is no compound in four hundred years of Old Vaross for what he now was.

It could not be *vorruk*, because he had not held, and it could not be any of the taking compounds, because he had not taken. He was not dead and could not be entered as dead. He was not a captive, because he had been returned. Whatever the Keth-Gorrum wrote beside his name would be a new word, coined for him, and every hobgoblin in the Expanse would hear it and would know it was new, and would know why, for as long as the man lived and afterward.

Bram Greymane had not maimed a commander. He had made a nation invent a word.

"I want you to remember the name of the person who took your virginity."

He put his hand on the man's chin, which had very little left on it, and moved the head so the eyes came round, and smacked it twice, lightly, the way you rouse a drunk.

"Don't die now."

And then he stood up, on the hip, with the cup still in his good hand, and gave the order to load him into the cart, and went inside out of the rain, and drank the rest of it sitting by the fire in the Stormfold hall under a shield with a boss cracked in two directions, and did not say another word for the rest of the evening to anybody.

And in the spring, under a sky that four countries had agreed to describe with the same word, the instrument was drawn.

Kharven, and the Holy Sea of Alabaster, and the Kingdom of Nalūn, and the stretches from the Brine crossing east to the marches of Sum-gol, under one seal and one body of law, with the Moto lines seated as the royal house and a fourteen-year-old boy with the temporal running behind his eyes holding a chair at the table by right of a forfeiture he made at nine years old in eleven men's blood.

The first Accord circle. The thing Muken Moto had wanted and had died four years short of asking for.

They signed it in the lower hall at Kharven-Seat with three thousand and eleven names read out beforehand by a man in gloves who would not delegate one of them, and a woman with a stick standing at the back who should not have been on her feet, and a man with three fingers who had walked in from the Stormfold road and would not sit down, and a king who had lost his daughter and had built a country out of the passion that came after and had still not slept a full night since the ninth hour.

Sodoku Moto put his hand to it last.

And Yoko Mishiro, who had been chained once and had been unchained by that man and had spent nine years finding out what he was, wrote in her own record that night, in the plain form she uses for everything, four lines that the Bench has never been permitted to see.

*He built it for her. Every clause. The refugee clause, the royal house clause, the one about children of the defeated lines. All of it is a twelve-year-old girl in a doorway and none of it says so and none of it ever will.*

*He will not say it because saying it would make her the reason, and he does not want her to be a reason. He wants her to be a person who was killed.*

*I have been beside this man for nine years and this is the first thing he has done that I do not think I could have done.*

*And it is going to hold. That is the part nobody has understood yet. It is going to hold, because a thing built out of grief that refuses to name the grief has no argument in it that anybody can get a grip on, and there is nothing in that instrument for a future council to repeal.*

---

## Cast

state.json has no facts yet, so every cast member gets the full card (`python build/book_tools.py character NAME`), capped at 6,000 characters.

### Sodoku Moto  (Volume I — Character Cards/Sodoku Moto.md)
also matched: Sodoku Moto/Tōga (冬牙) — Winter Fang.md; The Table — Running Pieces/State of Play — Sodoku Moto Kharven.md; Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md


### Sodoku Moto

*The Exiled Lion · The Kōkan Butcher · Card 19*
> **Level 320 in a Stage VI body.** Two to four Grade brackets past what his Crystal has certified, and a Coherence Band of **D**, which is what that costs.
>
> *His own codex names it rather than smoothing it: he moves like Level 320 now, despite a Crystal that has crossed six of sixteen Stages.*

---

#### I · Identity

**Also known as** The Scourge of the Moto · The Kōkan Prince
**Race / Lineage** Human — Archaic Bloodline, Moto. **Kōkan Line. Former Crown Heir**
**Age** 22 · **Sex** Male
**Standing** Exiled by High Council decree, wanted across multiple territories, **charged with the massacre of the Tenrai main-branch settlement.** Travelling the Scourge of Hell with Yoko and Emira
> **Catalyst Event.** A Tenrai-commissioned corridor assassination took his father Muken, his mother, and his brother Nergüi **in one night.**
>
> He and Sonzai answered by burning the Tenrai main-branch settlement to the ground, **women and children included.**
>
> ***The High Council's charge isn't entirely wrong. It isn't entirely complete either.***

---

#### II · Soul Architecture

| **Level** | **320 / 500** · Band IV — Mythic (301–400). *Flag: normally clusters Stage XI–XII. He is genuinely Stage VI* |
|---|---|
| **Temperance Stage** | **VI — Glory**, active. Universal ceiling 400, max Grade A, Coherence Band D |
| **Coherence Band** | **D** — *his Aether Class and η read higher than Band D typically supports. Same outpacing anomaly, not a separate error* |
| **Path** | Spirit 62% · Attraction 28% · Body 10% |
| **Essence Typology** | **Limina**, primary — endings, dissolution. *Catalyst "accepting that something is over, and meaning it" maps the Ruins Work far more precisely than the codex's Eldritch/Fate-adjacent label.* **Fulguria**, undertone — matches the Kamigan's revelation function |
| **Aether Class** | **II — Harmonic** (Band D, ~15–25% loss) |
| **Efficiency (η)** | **0.84** — Band A/S territory, well above Band D. *The codex itself calls this the highest rating at Stage VI, so the anomaly is in-world acknowledged, not introduced here* |
| **Crystal State** | **The Stage V fracture is closed, not healed — a load-bearing seam** |
| **Attraction / Obsession** | Clean, recognition-sustained |

---

#### III · Work Architecture

> *The Kōkan Line does not harmonize with Wellsprings in the standard sense. It carries native bloodline intimacy with Hataraki, the governing function of the Plane of Fate.*
**Techniques administer rather than explode: reveal, rank, condemn, stabilize, sever, complete.**
**Totality — Zentai-sei no Hataraki** · Primary Work inheritance. The Crown judgment at full expression.
**Ruins — Hametsu no Gō** · Active in Kurosetsu's Mandate Weave inscription. Collapse, severance, terminal pressure.
**Judicium** · The Kamigan's analytical substrate. Threat-reading, Essence-signature assessment, probability-vector ranking.

---

#### IV–V · Stats

> Every Grade below is recomputed against the universal Tier Grade table **and lands several brackets above both the codex's original letters and the nominal Stage VI ceiling of 400.**
>
> *Not a transcription error. The named tension of his arc — bloodline-compounding and five years of forced survival growth outpacing formal Temperance advancement.*
| Stat | Value | Grade | Peaks |
|---|---|---|---|
| **Gnosis** | **1,050** | **X** *(codex: S)* | Acuity 1,080 · Analysis 1,065 · Retention 1,020 · Sapience 990 |
| **Tempering** | 940 | SSS *(codex: S)* | Clarity 955 · Coherence 945 · Maturity 920 |
| **Ardency** | 880 | SSS *(codex: A)* | Inscription 895 · Compression 885 · Depth 860 |
| **Resilience** | 810 | SSS *(codex: A)* | Scarring 835 · Threshold 825 · Hardening 805 |
| **Dexterity** | 760 | SSS *(codex: A)* | Economy 785 · Finesse 770 · Celerity 745 |
| **Vitality** | 720 | SS *(codex: B+)* | Filtration 740 · Threshold 730 · Constitution 715 |
| **Dominion** | 580 | SS *(codex: B+)* | Sovereignty 600 · Density 590 · Radius 560 — *small, steep trajectory* |
| **Harmonics** | 560 | SS *(codex: B)* | Fidelity 575 · Attunement 555, **rising via Yoko's presence** · Memory 540 |

> **Harmonics reverses the pattern** — genuinely his weakest stat relative to bloodline projection. *The Kōkan Line's isolation architecture working against him exactly where Yoko's presence is slowly working against it.*

---

#### VI–VII · Force and Flow

*Raw stats suggest SS–X territory, but Aether Class II caps deliverable output at Band D conversion. Figures below are actual current battlefield output, with the SSS-territory raw numbers as unrealized headroom.*
**Strike Force** · A-Grade band, city-block to multi-city-block equivalence at full Kurosetsu delivery — **the Mandate Weave routes Ardency into verdict rather than raw force**, so strikes read above the blade's physical weight class.
**Attack Speed** Mach 10–30 · **Reaction** 0.2–1ms · **Travel** Mach 5–25, 1,715–8,575 m/s
**Aura Pressure Field** · **38m passive, 80m+ under full Crown Judgment** — sourced directly, not estimated
**Domain Pressure** · Minimal. The Totality Domain is still seed-stage
**EU Reserve** 1,340,000 · **Flux Density** 920 EU/g · **AU/s** ~3,800 base · **η** 0.84

---

#### VIII–IX · Traits and Domain

> **The Kamigan, Crown Eye** · Innate · Judicium
>
> **A continuous, unclosable system.** Classifies everything by threat level, Essence signature, combat capability, intent, and verdict status. **No off switch.** At Stage VI it reads authority gradients in social spaces as readily as combat geometry.

*[card capped at 6,000 characters; 13,309 in full — `python build/book_tools.py character "Sodoku Moto"`]*

### Yoko Mishiro  (Volume I — Character Cards/Yoko Mishiro.md)


### Yoko Mishiro

*The One Who Stayed · Fox-Spirit of the Mishiro Line · Card 20*
> **A settled B-Grade profile everywhere she was always going to sit, built underneath one stat that was never going to behave.**
>
> Harmonics at **345** — sixteen points shy of her Stage's hard ceiling, **past the 320 instability line**, and Grade A in a Stage V body. *The same anomaly flagged at Level 72, just denser now.*

---

#### I · Identity

**Race / Lineage** Beastkin — Fox-Spirit variant, **Mishiro lineage. Spirit-adjacent; predates formal beastkin taxonomy**
**Age** 29 · **Sex** Female
**Standing** Unaffiliated, settled — **a cabin on the Scourge's edge, with Temür, their son Riku, and a second child on the way**
> **Catalyst Event. The lock on the pen.**
>
> She walked through it **on her own decision**, past a man who had already stopped waiting for her, ***because the choosing had to be hers and not a rescue she owed anyone.***

---

#### II · Soul Architecture

| **Level** | **145 / 500** · Band II — Awakened. *Gated on reaching Stage VII to pass Level 200* |
|---|---|
| **Temperance Stage** | **V — Splintering**, active. Ceiling 350, sustainable max Grade B, **instability risk above 320** |
| **Tier of Standing** | **5, Expert** · η ≈ 0.60 — *"the Crystal has learned to stop leaking"* |
| **Path** | Spirit 65% · Attraction 30% · Body 5% |
| **Essence Typology** | **Vitalia**, primary — growth, generosity, rhythm, **discovered through accumulation rather than rupture.** *Catalyst: "giving without counting, and finding the count was always in your favour."* **Fluxia**, undertone — the capacity to feel a thing again without being destroyed by the repetition |
| **Aether Index** | **Unusually clean for her Class** — fed directly by the Harmonics anomaly, *which inflates her Lattice Conductivity past what Band E would ordinarily support* |
| **Soul Crystal Tier** | **Resonant**, progressed from Harmonic. *In-world shorthand among those who knew her before is still Kindled* |
| **Crystal State** | Refined, stable. **The first genuinely settled stretch of her life** — no active fracture, no suppression pressure |

**Wellspring Harmonizations** · **Somnalis** primary, native, **requires no harmonization ritual.** **Anima Spirare** secondary, now fully expressed — *the bond with Temür, named and load-bearing.* **Verdantia** tertiary, lineage-access. **Manganthra** peripheral, **residual harmonization from the Scourge years.**

---

#### IV–V · Stats

*Verified against Level 145's real point economy — roughly 2,800 held across seven stats at a B-Grade floor, and roughly 1,300 concentrated into the Harmonics family: the fox-spirit anomaly that has never once tracked with her Level.*
| Stat | Value | Grade | Peaks |
|---|---|---|---|
| **Harmonics** | **345** | **A** — ANOMALOUS | Attunement 350 · Memory 346 · Confluence 342 · Fidelity 335 · Stability 330 |
| **Gnosis** | 260 | B | Perception 275 · Analysis 268 · Retention 258 · Forecast 250 |
| **Dexterity** | 245 | B | Celerity 255 · Economy 248 · Reflex 240 · Evasion 235 |
| **Vitality** | 210 | B | Constitution 220 · Fortitude 208 · Endurance 205 · Threshold 200 |
| **Resilience** | 195 | B | Integrity 205 · Persistence 198 · Ward 190 · Anchoring 185 |
| **Tempering** | 180 | B | Clarity 190 · Coherence 178 · Maturity 172 · Ceiling 168 |
| **Ardency** | 155 | C | Flux 162 · Depth 158 · Alacrity 150 · Compression 145 |
| **Dominion** | 150 | C | **Sense 165** — *bond-awareness, Riku and the coming child* · Radius 148 · Sovereignty 142 · Pressure 138 |

> **Ardency and Dominion stay her floor. She was never a fighter or a sovereign, and motherhood didn't change that.**

---

#### VI–VII · Force and Flow

*Non-combat architecture by design.*
**Strike Force** below 300 Joules unaided · **Durability** low-B · **Attack Speed** Mach 2.0–5.0 · **Reaction** 1–5ms · **Travel** Mach 1.5–4 · **Aura Pressure** faint, *just crossing into passive-pressure territory* · **Domain Pressure** none
**EU Reserve** ~185,000 *(estimate — no exact source figure exists at Level 145)* · **Flux Density** ~150 EU/g *(estimate)* · **AU/s** ~90 · **η** 0.60 *(sourced)*

---

#### VIII · Traits

> **The Aetheric Nose** · Innate Reflection · Somnalis-adjacent
>
> **Continuous, involuntary, unsuppressible.** Forty metres passive threat horizon, seventy active.
>
> ***Now tuned as much to a home and two children as to a war zone.***
**Fox-Fire, Splintering Expression** · Tempered · Verdantia-adjacent — **the projected Stage V escalation has arrived.** No longer a four-minute palm-light: **a sustained, shapeable cold-amber flame, held for minutes rather than seconds, still carrying no offensive force behind it.**
**Somnalis Native Access** · Lineage — accurate, non-symbolic dream-navigation, **present since birth.**
> **Anima Spirare, Fulfilled** · Resonant
>
> The bond with Temür, **fully expressed and named at Stage IV as projected.** A second, distinct thread now runs to Riku — **parental rather than romantic, same Wellspring, different weight.**
**Domain** · None. *Formation begins at Stage VII; she is two Stages short.*

---

#### X · Techniques

| Technique | Function | Counterplay |
|---|---|---|
| **Intent-Frequency Reading** | Passive, continuous. Reads the directional Essence-signature of **a forming decision** — olfactory-Essence pattern against autonomic emotional output. **Undetectable by the subject** | Trained affect suppression · *heavily scent-saturated environments degrade resolution* |
| **Wellspring Proximity Read** | Detects and types Wellspring nodes at 20m+, scaling with node strength | Signature-masking wards · **a wholly novel signature returns blank rather than a false negative** |

*[card capped at 6,000 characters; 9,921 in full — `python build/book_tools.py character "Yoko Mishiro"`]*

### Edward Lambert — The Arithmetic  (Volume I — Character Cards/Edward Lambert — The Arithmetic.md)


### Edward Lambert — The Arithmetic

*The Lambert · The Arithmetic · Hild's Right Hand*
> **Affiliation:** Kingdom of Kharven (loyalist) · The Sword Princess's Council
> **Status:** Active · Right-Hand Advisor to Hild Stark-Moto
> **Level:** 142 · **Stage:** III Hold · **Band:** II
> Not powerful. Never was. Never needed to be.

---

#### I · Overview

Edward Lambert is the man who taught an eleven-year-old girl how to hold a kingdom.
He did not teach her the sword. Lorn did that. He did not teach her the standing. The blood did that. He did not teach her the cold, or the jaw, or the cadence, or the specific quality of silence that the Kokan inheritance provided without instruction. Those things were architecture. Edward taught her the arithmetic.
The arithmetic of governance. Who holds what. Who needs what. Who fears what. How the three interact to produce the outcome you want. How the outcome you want differs from the outcome you need, and why the difference is the space where rulers are made or broken. How a granary's inventory is a weapon. How a road's condition is an intelligence report. How a man's second sentence tells you more than his first because the first sentence is the one he rehearsed and the second is the one that fell out.
Edward Lambert is not a great warrior. He is not a powerful practitioner. He is not a legendary commander or a storied knight or any of the things that songs are made about. He is a man who counts things. He counts grain stores and troop dispositions and the specific number of days between a lord's promise and a lord's delivery, and the counting is the thing he taught Hild, and the counting is the reason Hild governs rather than merely rules, because ruling is the sitting and governing is the counting, and the counting is the thing that keeps the sitting from collapsing.

---

#### II · Physical Description

Edward Lambert is fifty-three years old and looks sixty because the last eleven years added the decade that the previous forty-two had not. He is of middling height, neither tall enough to command a room by stature nor short enough to be overlooked by it, the specific build of a man who has spent his life occupying the space between notice and invisibility and who has found that the space between the two is where the most useful work gets done.
His frame is lean but not gaunt. A body that was once solidly built in the northern frontier manner, broad enough through the chest and shoulders to carry armour and swing a blade with the competence of a man who trained daily because training was the requirement, not the passion. The body has thinned with age and with the specific weight-loss that sustained stress produced in men who processed stress through the mind rather than through the body, the metabolism burning through reserves that the appetite was not replacing because the appetite was not interested in food. The appetite was interested in the problem, and the problem was the kingdom, and the kingdom had been the appetite's only subject for eleven years.
His face is long and angular, weathered to the texture of old leather by decades of northern wind and the specific indoor weathering that lamplight and sleeplessness produced in men who spent their nights reading dispatches by inadequate illumination. The cheekbones are prominent, the jaw narrow but set, the mouth a line that curves neither up nor down at rest, the specific neutral expression of a man who decided early that the face was a surface and that surfaces were for other people to project onto, and that the projection told him more about the projector than any direct question would. His eyes are grey. Not the pale grey of the Stark bloodline or the malachite grey of Dawi mineral. The grey of iron. Small eyes, set deep beneath a brow that produces permanent shadow across the upper face, and the shadow is the thing that most people see first, because the shadow makes the eyes harder to read, and the hardness is the point.
His hair is grey-brown, thinning at the crown, cut close to the skull in the northern military style that he adopted during his service and never abandoned because the style required no maintenance and maintenance was time and time was the thing Edward Lambert did not spend on anything that did not produce a return. He is clean-shaven, always, because a beard in the north was a vulnerability (it froze, it could be grabbed, it concealed the jaw's tells from people who were reading his face the way he read theirs) and because the daily shaving was the discipline, and the discipline was the man.
He wears dark wool. Always dark wool. A long coat over a quilted tunic, the coat's cut plain and functional, the fabric good but not ostentatious, the specific quality of clothing that communicated: this man has means but does not display them, and the not-displaying is the statement, and the statement is: I am not here to be seen. I am here to see.
He carries no visible weapon. A short knife lives inside the coat, accessible through a slit in the lining, and the knife has not been drawn in four years, and the four years is the proof that the knife's presence is sufficient and the knife's use is not required, because a man who needs to draw a knife has already failed at the thing the knife was supposed to prevent, which is: the situation reaching the point where knives are relevant.

---

#### III · History

##### Before the Fall

*[card capped at 6,000 characters; 24,141 in full — `python build/book_tools.py character "Edward Lambert"`]*

### Tabitha Hallenfeld — The Road Woman  (Volume I — Character Cards/Tabitha Hallenfeld — The Road Woman.md)


### Tabitha Hallenfeld — The Road Woman

*The Road Woman · The Kingdom's Nervous System*
> **Full Name:** Tabitha Hallenfeld
> **Age:** 42 · **House:** Hallenfeld (river corridors)
> **Level:** 28 · **Stage:** 0 (unpracticed) · **Band:** 0
> **Role:** Logistics officer, road intelligence, coalition supply coordinator
> Carries route manifests as weapons. Reads roads the way generals read battlefields.

---

Broad through the shoulders and thick through the waist, built with the solidity of a body that has spent its life on roads. Sun-darkened face, wind-roughened, crow's feet around the eyes. Hair brown streaked with grey, pulled back with two wooden pins. Traveling coat of heavy wool, road-stained at the hem, belted with a leather strap holding a knife and a sheaf of route manifests rolled into a cylinder.
She reminds Hild of her mother. Not physically — Fern was lean and angular. The reminding is in how Tabitha reads rooms: for what they can carry and what they cannot, and how long the carrying will last before the surface fails. Fern read rooms that way.
Tabitha walked three days through compromised territory to reach Kharven-Seat and tell Hild that the roads are talking and the roads are saying the Tenrai know where she is. The walking was the loyalty. The loyalty was the function. The function was the roads.
*Gods. She is a baby. She is a baby with a sword and a jaw that belongs on a grown woman. I will be damned if I let the roads die before this child has a chance to walk them.*

---

> *The Hallenfelds arrive late to everything because the roads do not pause for assemblies. The lateness is the function.*

### Brida Ashwell — The Warm Diagnosis  (Volume I — Character Cards/Brida Ashwell — The Warm Diagnosis.md)


### Brida Ashwell — The Warm Diagnosis

*The Warm Diagnosis · The Physician Who Sees the Child*
> **Full Name:** Brida Ashwell
> **Age:** 31 · **Origin:** Concord (frontier settlement, frozen locative surname)
> **Level:** 45 · **Stage:** I Ignition · **Band:** I
> **Role:** Personal physician to Hild Ice, medical authority of the Kokan Loyalist Coalition
> The only person who tells Hild to eat and means it.

---

#### Description

Short and dense through the torso, built close to the ground in the specific way women are built when their mothers and grandmothers all worked standing up. Round face, wind-chapped, permanently flushed across the cheeks and nose. Hair a colour that cannot decide between brown and red, settling on russet like autumn bracken, pinned in a twist at the skull's base with two bone pins that are not decorative and that she has used for field suturing on one occasion she mentions at meals with cheerful specificity.
Her eyes are hazel, green-brown, and they move across bodies performing assessment before performing greeting. She wears a leather satchel whose buckles have been re-set so many times the leather around the hardware has gone soft and shapeless. She brings willowbark when she has diagnosed something the patient has not noticed yet.
**Her function:** The warmth. In a court defined by Lambert's arithmetic and Osric's strategy and Lorn's honour, Brida is the person who sees the eleven-year-old underneath the Sword Princess. She is the one who reads the jaw-tension on the left side and knows it means the child is holding something too heavy. She is the one who tells Hild to eat and means it and follows up and checks.
**Her voice:** Firm and warm simultaneously. The voice of a thousand delivered instructions, each one as though it were the first, because the recipient needs to hear it as the first. *"The treatment is not negotiable."*

---

> *She does not treat the Sword Princess. She treats Hild. The distinction is the medicine.*

### Miku Tenrai Moto

no card for 'Miku Tenrai Moto' in the wiki mirror; check Notion before writing anything numeric about them

### a clerk of the Bench

no card for 'a clerk of the Bench' in the wiki mirror; check Notion before writing anything numeric about them

### a factor of the Council of Links

no card for 'a factor of the Council of Links' in the wiki mirror; check Notion before writing anything numeric about them

### Voice fingerprints (`python build/book_tools.py voice_fingerprints`, rows for the ch1 cast that appear in it: Sodoku Moto and Lambert; Yoko, Tabitha, Brida and Miku have fewer than eight attributed lines and no row)


12 characters with eight or more attributed lines (heuristic attribution; treat as measurement, not verdict). Rule: if two characters' lines could be swapped and nobody noticed, the scene failed (R15-1-VOICE_DIFFERENTIATION).

| character | lines | mean words | short share | questions | contractions | first person | imperatives | favourite words |
|---|---|---|---|---|---|---|---|---|
| Lambert | 20 | 35.3 ±25.5 | 0.25 | 0.0 | 0.1 | 0.45 | 0.0 | years, three, eleven, grain, four, because |
| Sodoku Moto | 13 | 45.6 ±21.7 | 0.0 | 0.0 | 0.08 | 0.46 | 0.08 | through, years, hand, tell, every, because |

#### Closest pairs (most swappable by the numbers)

- Hild Ice / Lambert (distance 0.45)
- Verinus VII / Lambert (distance 0.57)

## Recall

### `scene_recall "fair copy Vaultmere factor Bench clerk signing night refused grain returns"` (beat keywords)

Note for the writer: the Vaeloris, Path of Sorrow and Vacancy hits are keyword noise (other threads); the *What the Ground Was Owed* hits are the ones that bear — the four factors, the Vaultmere houses, and the first-week question.

#### WAR OF THE REALMS  (WOTR_Vaeloris_Sequence.md, score 22)
...You have carried a thing up ninety-one steps that you were not senior enough to be given. Somebody in that chapter hold decided that the news should be delivered by whoever could be spared. Is that a fair reading."  A long silence.  "Yes, sire."  "Then you have been treated poorly and you have done it well, and I will say so in writing to Altherion, and it will do you no good whatsoever." He turned ba...
...nked him for it, and the worst part is that he is right about the two hundred, and the second worst part is that I am about to go and choose six people, and there is no version of that where I choose fairly, because a fair choice would be a lottery and I am not going to run a lottery, I am going to pick the ones I can spare.*  She was still standing there when the side door banged.  "Commander." The v...
...nd the worst part is that he is right about the two hundred, and the second worst part is that I am about to go and choose six people, and there is no version of that where I choose fairly, because a fair choice would be a lottery and I am not going to run a lottery, I am going to pick the ones I can spare.*  She was still standing there when the side door banged.  "Commander." The voice arrived befor...
...six paces off with his boots at the edge of the ash and his weight back on his heels. "Sire, permission to say a thing."  "You do not need permission and you have never once waited for it."  "That is fair." Fend swallowed. "I have been trying to work out what is wrong with the light. It is not the light. It is that everything is casting the wrong shadow, and I have been looking at it for a quarter of...

#### What the Ground Was Owed  (10_wotr_what_the_ground_was_owed.md, score 18)
...and Lambert had done nothing about the holding at all. What he did was buy grain. He bought it in Nalūn through four factors who did not know about each other and he bought it at prices that made the Vaultmere houses laugh at him, and he shipped it north, and he did not distribute one bushel of it to any settlement in the southern reach. He let those settlements empty. He let them walk north with what they...
...hen and nobody has answered since.  *"Why did you buy the grain in the first week?"*  Because the advance came in the fourth. Because on the day Edward Lambert placed his first order with a factor in Vaultmere, no orc had crossed the wall, and no council had been called, and no threat assessment existed in any file in the Seat that would have justified the expenditure, and he spent eleven thousand in Kharv...
...ven miles past the wall in the first month and had held, and holding is expensive, and Lambert had done nothing about the holding at all. What he did was buy grain. He bought it in Nalūn through four factors who did not know about each other and he bought it at prices that made the Vaultmere houses laugh at him, and he shipped it north, and he did not distribute one bushel of it to any settlement in the...
...answered then and nobody has answered since.  *"Why did you buy the grain in the first week?"*  Because the advance came in the fourth. Because on the day Edward Lambert placed his first order with a factor in Vaultmere, no orc had crossed the wall, and no council had been called, and no threat assessment existed in any file in the Seat that would have justified the expenditure, and he spent eleven thou...

#### The_Path_of_Sorrow  (The_Path_of_Sorrow.md, score 17)
...ther and the strap bit into the muscle beneath, and the muscle accepted it the way it accepted everything: without complaint, without adjustment, without the luxury of deciding whether the weight was fair.  The inn's door opened one more time. Smaller hands. Smaller weight. The sound of bare feet on the planking and then the sound of a nine-year-old's breathing, morning-thick and sleep-warm, and behin...
...tch her frame.  "Fuck — one thing after the OTHER, WHAT THE FUCK!" Kroathar's voice cracked out, more fury than pain, fury at the tail, at the chains still binding half his strength, at the general unfairness of getting backhanded by something he'd just put four spears through.  "Mreow, that's the spirit," Saiya said, not even trying to hide the grin, hauling him fully to his feet by the collar of his...
...tification for the exile they had been engineering since before Father's body was cold. Every step we took was a step they had already mapped. Every verdict I delivered was a verdict they had already factored into the probability model. We were not fighting them. We were performing their choreography and calling it war.*  He did not cry. The observation was not new. He had arrived at it months ago, duri...
...tification for the exile they had been engineering since before Father's body was cold. Every step we took was a step they had already mapped. Every verdict I delivered was a verdict they had already factored into the probability model. We were not fighting them. We were performing their choreography and calling it war.*  He did not cry. The observation was not new. He had arrived at it months ago, duri...

#### The Vacancy  (01_the_vacancy_korvaeth_arc.md, score 14)
...-uren Thela Ess-Vaelen. Ie-sae. Ureth zo. Uren, uren, uren."*  The three-fold witness word again. The Elareth closing. The consecration form, in a frozen field, over a prisoner.  Nobody has ever satisfactorily explained it.  The Regency's own jurists spent six weeks on it and concluded that it accomplished nothing legally, cost Korvaeth eleven hundred witness-fees, and gave a hostile house a validated n...
...ter and it has not been used outside a rite in four Eons because there has been no occasion."  "So what is it doing in a yard."  "It is making it permanent."  Aeren Lyth sat down on the reading-floor bench, which is not permitted.  ---  The finding took nine days to draft and eleven words to state, and Sylvenn Thaeren wrote the second half of it, and the argument in the drafting chamber went on for six...
...e-en, elar-uren, uren, uren.*  The two of them stood on either side of a lectern in a floating city with eleven Eons of law under their feet and did nothing at all for a length of time that the floor-clerk later entered as *considerable*.  "She said the witness word three times," said Aeren Lyth.  "Yes."  "Once is the form. Twice is emphasis. Three times is."  "Three times is the Elareth construction,"...
...the bottom of it. Tell me it was for the empire. Tell me it was for the record, or for the Under-Houses, or for the war. Give me a reason with a number in it and I will go and sell it to six houses tonight and I will make them believe it."  "There is no number in it."  "Ilthára."  "She was fourteen," said Ilthára Korvaeth.  Her brother stopped.  "She was fourteen and I was fourteen and we were in the V...

### `scene_recall "Sodoku Yoko Lambert Tabitha Brida Miku lower hall Kharven-Seat passage"` (cast + place)

#### What the Ground Was Owed  (10_wotr_what_the_ground_was_owed.md, score 105)
...e had lost his daughter and there was no arrangement of the world in which that was survivable, and he survived it, and both of those were true at the same time for eleven months and are true still.  Sodoku Moto did not grieve in any manner the Seat could recognise. There was no shutting of a door and no drinking and no long silence in a cold room, and there was nothing anybody could point at afterward...
...apart was very little and it came north in pieces over the sixth and seventh months, and Kharven took them in as refugees, which is the single most contested decision of the entire post-war and which Sodoku Moto made alone and against the advice of every officer in his service.  They came in wagons and on foot and eleven of them came in a boat that should not have floated. They came having eaten what th...
...losed around him and went to a knee with their weapons out and their faces up, which is the Tenrai posture for a household guard that intends to die where it is standing and wishes the fact entered.  Sodoku Moto rode into the middle of that on Tōga with the frost coming off the animal in a front and eleven hundred men behind him.  He asked once.  He asked in form, in the old register, which is a courtes...
...said, in Common so the boy would understand, that the Tenrai household did not hand its heir to the man who had done the Tenrai settlement, and that they would be obliged if he would get on with it.  Sodoku Moto got down off the Droval.  He killed all eleven and it took him under a minute and he did it with Kurosetsu and he did not use the cold, and Yoko, who was there, entered afterward in her own hand...

#### Cast index  (CAST.md, score 23)
...nd_the_print.md (7), 07_charles_the_imperceptible_district.md (5), verinus_sword_and_scale.md (4), verinus_what_a_thing_weighs.md (4)  ## Lambert (19 scenes) 10_wotr_what_the_ground_was_owed.md (19), sodoku_the_count_supply_report.md (13), 05_aurelian_primate_under_the_wrong_stars.md (10), verinus_weight_of_an_infant.md (10), 07_charles_the_imperceptible_district.md (9), 08_charles_what_a_hand_is_for.md...
...ount_supply_report.md (13), 05_aurelian_primate_under_the_wrong_stars.md (10), verinus_weight_of_an_infant.md (10), 07_charles_the_imperceptible_district.md (9), 08_charles_what_a_hand_is_for.md (9), sodoku_fourteenth_bow_table.md (9), 06_aurelian_what_the_lamberts_are_for.md (8), wotr_the_weight_of_a_courier.md (8), renard_the_left_of_the_door.md (6), sodoku_gate_reunion_lambert.md (6), sodoku_true_rel...
...d (9), 08_charles_what_a_hand_is_for.md (9), sodoku_fourteenth_bow_table.md (9), 06_aurelian_what_the_lamberts_are_for.md (8), wotr_the_weight_of_a_courier.md (8), renard_the_left_of_the_door.md (6), sodoku_gate_reunion_lambert.md (6), sodoku_true_religion_alabaster.md (6), temur_true_religion_alabaster.md (6), 01_wotr_muster_breach_road_north.md (3), 04_sodoku_what_the_sky_does_not_ask.md (3), 05_sodok...
....md (9), sodoku_fourteenth_bow_table.md (9), 06_aurelian_what_the_lamberts_are_for.md (8), wotr_the_weight_of_a_courier.md (8), renard_the_left_of_the_door.md (6), sodoku_gate_reunion_lambert.md (6), sodoku_true_religion_alabaster.md (6), temur_true_religion_alabaster.md (6), 01_wotr_muster_breach_road_north.md (3), 04_sodoku_what_the_sky_does_not_ask.md (3), 05_sodoku_the_fixed_end.md (3), 09_dabney_th...

#### The Weight of a Courier  (wotr_the_weight_of_a_courier.md, score 22)
...The fire had burned down to the stage where it gave more smell than heat, resin and old ash and the particular sourness of green wood that has been forced. Somebody had banked it wrong. The heel of Sodoku's boot found a nailhead standing proud of the flagstone and he pressed on it twice without deciding to, and out in the passage a woman was telling a man that four ricks of green would not see him to...
...d not want to be talked out of it.*  "I have an answer. The answer costs an evening, and we have a courier nine days out, and I would sooner spend the evening on the thing that can still be changed." Sodoku pulled the plank of bread toward himself and then pushed it away again, untouched. "And because my brother is right, and he has been right for the length of this meal, and everyone in this room has b...
...two hundred years, and no theology I have ever been furious about has moved one wagon."  "Then why have you spent four minutes being furious about it," Lambert said.  "Because I am capable of both." Sodoku did not look up. "Write it down if you like. Under acceptable losses."  Yoko's ear flicked once and settled.  "Consider what the pattern actually is," Sodoku said. "Grain cut by three quarters over t...
...rt said.  "Because I am capable of both." Sodoku did not look up. "Write it down if you like. Under acceptable losses."  Yoko's ear flicked once and settled.  "Consider what the pattern actually is," Sodoku said. "Grain cut by three quarters over two years. Inscription substrate delivered in full, on schedule, every quarter, for eleven years, through the collapse, through two winters when the corridor w...

#### The Left of the Door  (renard_the_left_of_the_door.md, score 21)
...lse, a pressure in the sinuses, the weight of a sky before snow. It had been like that since the girl claimed her name in front of the court and the temperature of the whole room fell four fingers on Lambert's glass. Something had stayed behind after. Renard did not have the words for what and had never asked for them.  The lamp by the throne went sideways.  Sideways, toward the arch, and there was no dr...
..."Greymane," the man said. His Concord was clean and unaccented and dead flat, and the voice was pitched not to carry. "Which one. The cousin."  Renard said nothing. The sword was already speaking.  "Lambert opened the west postern for me," the man said. "In case you were wondering how. I'm telling you because it won't help you."  It went into him past the skin before he felt it, a splinter. He did not b...
...er the Pressure scale). Wellspring Exuroth, Caloria, Thermodynamics. Category Arts, Body-aligned, delivered through Magicraft. Working: *the Held Boil*, the latent-heat seed from Pack Thirteen §3. - "Lambert opened the west postern." The session's lie. Uncorrected on the page. Whether it is a lie is Isaac's to rule; the man believed he was buying time with it, which is not the same as it being false. - T...
...ned yet. - The wax-sealed packet. Unopened. Contents unassigned. - "The third bowl" as Brida's shorthand for Class III haemorrhage. New Kharven Standing Inventory entry under the dead, if ratified. - Lambert's glass (a thermometer at court) and the "four fingers" it fell on the night of the Bastard Speech. Pack Eleven instrument texture in a Kharven hall; pending.  **Phenomenon line (Pack Thirteen §3)**...

### `wiki Bench` — trimmed to "What the Bench Is" and "Crown and Bench"

Reading recorded here: the wiki has one Bench, the Bench of Attribution (a standing joint instrument of three Accord Divisions, with a Record); the State of Play uses "the Bench" for the body that has never been permitted to see Yoko's four lines, and the outline uses it again in ch10 ("the Bench under the instrument") and ch12. The brief reads the ch1 clerk as that body's clerk. The prose never expands or explains the name; if Isaac means a court of the instrument instead, he says so in a sentence and nothing on the page changes.

Source: Factions, Bloodlines & Institutions/The Bench of Attribution.md

#### What the Bench Is

The Bench of Attribution **is not a Division and has never been one.** It is a standing joint instrument of three Divisions that could not agree to give the function to any one of them, **and its entire procedure is the machinery of that disagreement operating at scale.**
It rules on what a formula is, whether it may lawfully exist in commerce, what class of material a given lot actually contains, and who is permitted to hold the result.
> Those four questions govern the alchemical economy, and the alchemical economy governs everything the Crown does not own outright.
>
> The Bench is therefore **the most consequential body in the four quarters and the only one with no seat on the Concord Council** — which is not an oversight, and has been proposed for correction eleven times.

##### The three chairs

| Chair | Question | Its position |
|---|---|---|
| **Doctrine** *Research and Archives* | Whether the glyph chain constitutes lawful Parunic syntax. Whether Authorization, Boundary, Direction and Sealing are properly filled. **Whether the Wellspring invoked would recognise the invoker as an authorized channel** | That attribution is fundamentally a question of **law**, and the instrument is a convenience of the modern era |
| **Instrument** *The Measurewrights* | What the coil reads. Class, Fidelity, Carry, and the reference figures against which every subsequent lot in the world is measured | That attribution is fundamentally a question of **measurement**, and doctrine is what a party appeals to when the needle has disagreed with them |
| **Ruling** *Arbitration* | The Attribution is an adjudication. Enforceable, appealable at the appellant's cost, backed by Enforcement | That attribution is fundamentally a question of **who can be sued** — and Arbitration is the only chair that has ever stated its position aloud, in session, on the record, **and declined to withdraw it** |

> **A session requires all three. Two chairs cannot rule.**
>
> This has produced four documented deadlocks lasting longer than a year, **one of which is ongoing** — and the ongoing one concerns a formula that **eleven thousand people are currently taking.**

#### Crown and Bench

The Crown holds the land, the law, the levy, the tax and the right to hang. The Accord holds the assay, the rank, the credit, the writ and the arrays. Neither can abolish the other and both have costed it.
> **The Bench is where that arrangement is actually administered, and it is administered by not being discussed.**
>
> A crown that quarrels with the Bench does not lose a war. **It loses entry on the formulas its own arsenals are built around** — quietly, over two or three sittings, on grounds that are every time doctrinally impeccable.
Two crowns have tried. One withdrew the quarrel. **The other is Kaetran**, and the Kaetran arsenals are still supplied, and the terms on which they are supplied are not published, **and the Bench's Kaetran rulings since have been notably swift and notably favourable** — and the Measurewrights have entered a note observing this **and have not been asked to remove it.**

### `wiki Vaultmere` — the page returned is *The Kingdom of Nalūn — The Chain-Cities*; trimmed to Overview, the Seven Chain-Cities, the Six Provinces, the Wellsprings and the Oath, and Governance (the Council of Links, whose factor sits at the table in this chapter)

Source: The Inner World — The Northern Shield/The Kingdom of Nalūn — The Chain-Cities.md

#### Overview

A **subterranean merchant oligarchy** carved into a sealed evaporite basin on the southeastern margin of the northern shield. Its cities are cut from salt two hundred fathoms thick, **the preserved floor of an ancient sea that dried out in an era nobody alive can date with confidence.**
> Its wealth is not the tunnels. **It is what the tunnels are made of, and what the Wellsprings beneath them can do to a promise spoken inside their resonance.**
> A bill of exchange drawn on Ironlink Hold is accepted in the Ring smelters, in the Old World's western ports, and in trade posts across the frontier — **not because those places respect the Kingdom of Nalūn but because the instrument enforces itself.**
>
> *The distinction is the whole of the explanation, and it is the reason the chain-cities have endured as a sovereign power for longer than most of the kingdoms that regard them as a curiosity.*
Seven subterranean cities, a surface port, six administrative provinces. **Roughly forty-five thousand souls underground**, with a further eight thousand in surface settlements and corridor way-stations that depend on the chain-cities for their economic existence.

#### The Seven Chain-Cities

> Together they form a single organism: **a creature made of salt and contract and the accumulated weight of seven centuries of people who discovered that the most durable thing in the world is a promise made inside a mountain.**
| City | Character |
|---|---|
| **Ironlink Hold** *the capital* | Largest and oldest, where three salt horizons intersect a fault that channelled Wellspring energy upward from the deep. Seat of the Council of Links; **where the most significant Parun-bound contracts in the four quarters are sealed.** Five levels, shaft-lifts, the Great Chain Hall holding three thousand under lanterns casting warm light across walls of translucent amber salt. *The air smells of mineral warmth, lamp oil, dried ink,* *and the ozone sharpness of active resonance that visitors feel as low pressure behind the eyes.* *The oldest walls glow faintly during contract-sealing —* *the Chain Light* |
| **Vaultmere** *the counting city* | Where the salt is exceptionally dense and dry — **ideal for long-term storage of Parun-bound instruments.** Sealed chambers holding the physical record of every significant agreement in the kingdom's history, **climate-regulated by the salt itself.** Roughly three thousand: archivists, contract scribes, and the calibrators who verify authenticity. *Quiet, deliberate, and slightly oppressive in the way of any place where every surface contains the weight of promises that cannot be unmade.* *Visiting factors describe it as the place where you can feel the kingdom's memory pressing against your skin* |
| **Deepvein** *the Wellspring floor* | Lowest of the seven, where the beds are thickest and Contraxis concentration is most intense. **Contracts sealed here hold tighter, last longer, and enforce with a specificity instruments sealed elsewhere do not match — and the difference is measurable.** Roughly two thousand: the kingdom's most senior contract specialists, the Measurewright station, and the handful of scholars studying the Contraxis–Fixatio interaction. *Warm, quiet, and glowing.* *The Chain Light is constant here**, a faint amber radiance that does not flicker and does not need fuel, and the oldest residents claim they can feel the Wellspring the way other people feel weather* |
| **Rimward** *the eastern frontier* | Newest and most vulnerable, founded ~140 years ago to service corridor trade. Thinner salt, weaker resonance, **and contracts sealed here carry a slight but measurable reduction in enforcement strength.** **The factor houses regard this as a quality-control problem. The Rimward merchants regard it as a competitive advantage** — *because a contract that enforces slightly less rigidly allows slightly more flexibility, and flexibility is what frontier commerce requires* |

*(rows for Halcrest, Cutwall and Bridgemarch trimmed; `python build/book_tools.py wiki Vaultmere` for the full table)*

#### The Six Provinces

*Each governed by a Provincial Chainwarden, appointed by the Council and bound by Parun-sealed terms specifying their authority, obligations, and the conditions of recall.*
| Province · Capital | Character |
|---|---|
| **The Ironward** *Ironlink Hold* | Political and financial core. Provincial and kingdom governance are in practice the same thing, **and the Ironward's Chainwarden is traditionally the most junior Council member, given the post as a formality because the Council governs the province directly** |
| **The Vaultlands** *Vaultmere* | Archival. **Deliberate, precise, and suspicious of haste in any form.** Home to the kingdom's largest concentration of trained scribes, each of whom completed **a seven-year apprenticeship before being permitted to draft an instrument that would be sealed.** *A factor without a scribe is a man with opinions.* *A scribe without a factor is a scribe with a full calendar* |
| **The Eastern Reach** *Rimward* | Frontier. **Bears the full weight of the corridor closures** — supply disruptions, stranded convoys, and the mountain settlements that have received nothing for months. *The Chainwarden's dispatches are reported to be* *increasingly direct in their assessment that the kingdom's policy of waiting for external authority to restore itself is not a policy but an absence of one* Deepvein sits inside its borders as a special zone under direct Council authority, administered by a Council-appointed Steward — producing exactly the friction one would expect between a frontier province and a carve-out in its middle |

*(rows for the Upper Basin, the Cuttings and the Span trimmed)*

#### The Wellsprings and the Oath

> Nalūn sits on **Contract-aspected Wellsprings**, which are uniquely among the sixty **able to seal an agreement into metaphysical law.** This is the single fact upon which the entire kingdom is built.
**Contraxis** · *Contract / Agreement.* Does not produce practitioners in the conventional sense. **What it produces is an ambient field in which spoken and written agreements, properly sealed, acquire metaphysical weight.** A Parun-bound contract executed under Contraxis resonance is not a promise backed by a court. **It is a working**, and breaking it has consequences that arrive **without anyone needing to be convinced, subpoenaed, or bribed.**
> The consequences are structural. The breaker's Essence becomes unreliable, their instruments fail to seal, **their credit becomes physically unreadable to anyone attuned to the field.**
> ***The punishment for breaking a Nalūn contract is that Nalūn stops working for you** — and in a world where Nalūn's instruments are the backbone of long-distance credit, that is a punishment worse than any court could impose.*
**Fixatio** · Concentrated in the salt itself, making Chainsalt **an Essence dielectric of exceptional quality**: it will not conduct, will not retain, and will not degrade under sustained potential. *The interaction is what gives the chain-cities their character — agreements made inside the salt are simultaneously bound by the Wellspring and insulated from tampering by the substrate.*
**Parun-bound instruments** · A document inscribed with specific glyph sequences, sealed in a linked token, executed inside the resonance field. **Each party holds a token — small iron or bronze discs that resonate while the contract is sound and go inert when it is breached.**

#### Governance · The Council of Links

> Nalūn is not a monarchy in any functional sense, **though it retains the title in its diplomatic instruments because the Concord Codex's recognition framework requires a sovereign signatory and the Council refused to invent a new category.**
**The Council of Links** · The senior partners of the fourteen recognised factor houses, sworn in by Parun-bound contracts specifying obligations, term, authority, and the consequences of exceeding any of the three.
> **Four Council members in the kingdom's recorded history have been removed by the mechanism of their own oath** — their tokens going inert mid-session when the Wellspring determined they had breached the terms under which they held their seat.
**The High Chainlord** · Head of state, chosen by **the Trial of Ten Deals**: ten days, ten increasingly complex commercial problems, judged by retired factors, active Measurewrights, and one representative of the Accord's Arbitration Division. **The candidate who resolves the most without breaching any existing contract, creating any new liability, or insulting any party whose goodwill the kingdom requires** takes the office. *Held for life, or until the holder's oath-token goes inert, whichever arrives first.*
**The factor houses** · Fourteen recognised, each a commercial partnership bound by Parun-sealed articles of association. **The articles are public documents and anyone may read them.**

## Continuity

### Facts about the cast or the place (state.json, newest first, at most 40)

None yet: `state.json` `facts` is empty. This is chapter 1; the only continuity is the archive, carried in §6 and §8, and the bible's cast lines (one each, from fow_line):

- **Sodoku Moto** — Level 320 in a Stage VI body, Band IV Mythic, Coherence Band D, Aether Class II Harmonic; Gnosis 1,050. Kōkan Line. Kurosetsu, Black Verdict, Ruins-inscribed. The card is from the exile years; on the page he is a king in solace who has not slept a full night in a year, works eighteen hours, makes no jokes, and gloss rights never.
- **Yoko Mishiro** — Level 145, Band II Awakened, Tier of Standing 5 Expert, η about 0.60, Resonant tier; Harmonics 345, anomalous. Nine years beside him. Exactly what is accurate and nothing more; nose before eyes; ears and tail betray her first. Gloss rights diagnostic only. Her four lines exist and the Bench has never seen them.
- **Edward Lambert** — Level 142, Stage III Hold, Band II. Fifty-three, gloves indoors, collar to the throat, the count. Read three thousand and eleven names and would not delegate one. His seal is on the four hundred and six. His brother is a hole in an ordination roll. Gloss rights yes.
- **Tabitha Hallenfeld** — Level 28, Stage 0, Band 0. The road woman. Has the question, written and dated, and two refusals.
- **Brida Ashwell** — Level 45, Stage I, Band I (card says Ignition; Fracture of Worlds says Murmuring; R14-A open; no Stage name reaches the page). On a stick for a year, colour wrong for longer. Says the true thing. "The third bowl" is hers.
- **Miku Tenrai Moto** — no card in the wiki mirror; nothing numeric on the page. Fourteen, the temporal running behind his eyes, a chair by right of a forfeiture at nine. Asked eleven times what he saw; four words: "I saw him mean it."
- Unnamed, invented for the book and to be entered in the Inventory of whichever culture owns them if they survive the draft: a clerk of the Bench; a factor of the Council of Links at the Seat; the Chainwarden of the Eastern Reach's clerk; the four Vaultmere factors; the Chainwarden of the Vaultlands; an envoy of the Keth-Gorrum (Bugbear, carries a stone); a hereditary interpreter of Kethaal Vaross; the lord of House Thornwall (the wiki leaves the head unnamed); the Council Chair of the Ore Council (the wiki says he needs a name; the book does not give him one); the Coldbeck cooper who reads the names.

Place, from the bible: Kharven-Seat: the lower hall where the instrument was signed, the pillar (the board hangs there from ch3), the passage behind the throne hall, the altar-room, the upper burying ground with four stones cut to one depth.

### Summaries of prior chapters

None: this is chapter 1.

### Hook agenda

No hook is yet planted or advanced (all twelve are `planned`), so nothing is due within three chapters. The four this chapter plants, with the chapter each comes due:

- **H01-yoko-lines** — due ch12 (11 chapters out). Keywords: four lines, Yoko, refused, Bench.
  Plant in ch1: Yoko's four lines about the signing night exist in her own record and the Bench has never been permitted to see them. The Bench's clerk asks and is refused; by the anniversary the king asks and is refused the same way, and does not press.
- **H02-copy-road** — due ch6 (5 chapters out). Keywords: Vaultmere, copy, first week, factor.
  Plant in ch1: Sodoku sends Tabitha Hallenfeld south with the fair copy of the instrument for Vaultmere, knowing the four factors sit there. The copy goes into the salt and the road gives her the first order's date.
- **H03-miku-chair** — due ch5 (4 chapters out). Keywords: Miku, clause, three hundred, by name.
  Plant in ch1: Miku Tenrai Moto, fourteen, holds a chair at the table by right of a forfeiture and watches the king's hands. The first test of the refugee clause comes from that chair, not from outside: he asks for the three hundred by name.
- **H04-price-of-standing** — due ch12 (11 chapters out). Keywords: sat down, Brida, full night.
  Plant in ch1: Brida names what a man who has not slept a full night in a year is spending and says it comes due in the Thin Weeks. Bram would not sit at the signing. At the anniversary Bram sits in the hall and Sodoku sits on the ground by the smallest stone.

Nearest payments after this chapter: H03-miku-chair pays in ch5 (Miku asks for the three hundred by name; the chair and the watching of hands must be on the page here so ch5 has something to pay); H02-copy-road pays in ch6 (the copy in the salt, the first factor's date arriving via ch2). H01 and H04 run the length of the book to ch12.

Ledger line paid this chapter (bible spine): Sodoku, no full night since the ninth hour — Brida prices it in the passage behind the hall. What the PC wrongly believes, left uncorrected until ch5: that the first test of the instrument will come from outside (Nalūn, the Holy Sea, the Ore Council). Grief's one named object for the chapter is the writer's to pick and to leave without an adjective; the circle is never named; Hild is never named as the reason.
