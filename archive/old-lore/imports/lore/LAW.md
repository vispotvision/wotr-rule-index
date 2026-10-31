# LAW · the Lore pass

Binds every Lore section and The Web of Lives. Quotes are the rule index's words; (pass) marks this pass's standard, not a rule.

## 1 The register

A Lore section is a record of a life kept from outside it: third person, past tense, one steady distance, plain exact prose in full sentences, about "the people the systems happened to" (Characters page).

- **Person and tense.** Third person. Past tense for Origin, The Making, The Cost; present tense in Where They Stand, only for what still holds (pass). Use the name the card's title uses and do not switch without a reason (R20-5-ON_THE_PAGE).
- **Distance.** No POV, no italic thought, no free indirect idiom (pass). Narration distances govern scenes (R35-1-NARRATION_DISTANCE_BANDS); their cautions bind a record: "Sodoku never" glosses (R20C-49-GLOSS_RIGHTS_CARD_FIELD), and no interpretive-summary sentence past Sodoku's procedural read (R35-2-NARRATION_DISTANCE_ASSIGNMENTS).
- **Inference, never declaration.** A person is established "by what they choose under pressure, what they refuse, what they notice first" (R5-B-DECLARATION_TO_INFERENCE; R20C-36-CLEARLY_WINS).
- **No verdicts.** A verdict "in the narrator's neutral register is Tolkien's voice and gets cut" (R5-E-FREE_INDIRECT_CARVEOUT). "No line tells the reader what to think of a character's choice" (R5-E-NARRATION_NEVER_ADJUDICATES; R5-E-MARTIN_WINS_RULING). No winks (R5-C1-NARRATION_NEVER_WINKS).
- **A record's register.** The Fracture Log "records the event"; the casebook "records the accommodation" (Characters page); The Cost is written from the casebook's side. "State the loss and move on" (R5-C2-FLAT_DELIVERY). Elegy attaches to "a named concrete thing that is gone" (R5-C2-ELEGY_CONCRETE_THING), one sustained passage at most (R5-C2-ONE_PASSAGE_BUDGET). The elevated register belongs to in-world documents, songs and mythic strata (R5-E-ELEVATED_REGISTER_QUARANTINED); the Lore is the card's record, not an in-world document, and does not use it (pass).
- **Texture.** Material density in full, interpretation at zero (R6-5-MATERIAL_DENSITY_SURVIVES). "Texture comes from the Standing Inventory" (R6-7-GOVERNING_RULE): Kharven in `desktop/NATALIE.md`, the rest in `desktop/inventories/`. New texture must be entered in the Inventory the same session (R6-9-RECURRENCE_RULE), and this pass cannot write it: coin no food, oath, proverb or custom.
- **Words.** Modern words are legal (R15-1-LICENCE). A quoted line is reproduced exactly (R19-2-FIXED_TEXT, R19-3-PROSODY_VERBATIM). Humour passes the funeral test (R5-D-FUNERAL_TEST); "Sodoku does not make jokes" (R5-D-HUMOUR_CASTING).
- **Record mode, other creators.** Sodoku Moto's Lore is compiled, not written; the index's one record card, Sonzai's, holds identity, standing, a dated act, relations and "no interiority" (R20C-16-SONZAI_RECORD_CARD). Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem and Sonzai (Chuluun) appear only as a card or scene records them (`desktop/NATALIE.md`, "What you never do"; R1-1-RESTRICTED_CHARACTERS_EXCLUDED).

## 2 Banned constructions and AI tells

`bash build/py.sh build/verify.py <file> --band standard` FAILs the first eight; a FAIL is never left.

1. An em dash, en dash or double hyphen anywhere, headings and bullets included; a title's em dash is written " · " (R15-1-AI_TELL_CHECKS_SURVIVE).
2. Antithesis in every form: "not just / merely / only X but Y", "less X than Y", "it was not X, it was Y", "Not X. Y.", "rather than" doing that work (R15-1-AI_TELL_CHECKS_SURVIVE; Guide checks 4, 5, 14). State what the thing is.
3. The Ladder: two "was X and the Y was" clauses in one sentence (R6-1-LADDER_BAN, R6-11-CHECK18_LADDER).
4. Countdown negation: short negations resolving into "Just" or "Only" (R15-1-AI_TELL_CHECKS_SURVIVE; Guide check 8).
5. Reification: a watchlist noun (silence, weight, arithmetic, governance, permission, distance, authority, refusal, grief, history, patience, the question, the cost, the moment, the space between them) followed within two words by a physical verb (sat, settled, carried, held, took, stood, left, went, came and more). Three per file or two per paragraph FAIL (R4-15-TWO_PER_SCENE_BUDGET, R4-15-ONE_PER_PARAGRAPH, R4-15-WATCHLIST_NOUNS). The script ignores R4-15-LICENSED_CLASS: "the authority she held" counts.
6. Three consecutive sentences over 25 words (R4-14-CHAIN_CEILING).
7. Four flat runs, three sentences within forty percent of each other's length (R4-14-RUN_RULE).
8. Fewer than one sentence in ten under eight words; under 18% warns (R4-14-HARD_CEILINGS).

The 700-word band WARN does not bind; the pass's length bands do.

WARNs, read and fixed: gloss, budget zero (R4-13-GLOSS_DEFINED, R4-13-ZERO_BUDGET, R4-13-DELETION_TEST); signposting ("felt a wave of grief", "It's worth noting"); hypophora; two similes in a paragraph; a close opening "Ultimately" or "In the end"; stacked fragments; a faculty as subject of a perception verb (R6-2-FACULTY_NEVER_SUBJECT); a paragraph ending on three sentences over 18 words (R4-14-HARD_CEILINGS).

Unscripted, equally banned: declarative characterisation, the reaction-shot cutaway, the comedic beat, narrator moral adjudication (R5-G-TELL_BANK_ADDITIONS); "it glowed" (R9-3-AURA_AS_FRACTURE); grief for abstractions (R5-C2-ELEGY_CONCRETE_THING); narrator explanation of the system (R5-F-LIGHT_NOVEL_NOT_KEPT); check 9's tic words (particular, specific, precisely, genuinely, suddenly); "as you know" (`desktop/NATALIE.md`). No "pending", placeholder or bracketed gap: what cannot be established is left out.

## 3 Names

Names come from the card first; a new name is the last resort, built in the stratum of whoever wrote it down.

| Stratum | Whose names | Shape | Rule |
|---|---|---|---|
| Japonic | archaic bloodlines: Moto, Yukari, Yuno | life-stage slots, name-taboo, compound topographic surnames, renaming at promotion, vow or allegiance | R23-2-JAPONIC_STRATUM |
| Korean | the Mahuo | lineage name first, two-syllable given name with a generation syllable, hollow-seat; "Hyphen means Mahuo" | R23-2-KOREAN_STRATUM, R23-10-TELLING_APART_KOREAN |
| Chinese | houses kept by a record: scholar-physicians, Measurewright, alchemical and trading lineages | one-syllable surname, generation character, courtesy name, studio name | R23-2-CHINESE_STRATUM_SUMMARY, R23-10-CHINESE_SLOTS |
| Northern | whoever the Accord filed: Banner Houses, chartered families, guilds, the muster, the commons | small given-name pool, frozen surname if chartered, live patronymic if not, earned byname | R23-2-NORTHERN_STRATUM |
| Far-Northern | tundra peoples, sealers, timber towns, the Keld, most Kharven commons | no surname; a carried name held by the dead; an Accord roll-name | R23-2-FAR_NORTHERN_STRATUM, R23-11-ROLL_NAMES_FROM_ACCORD |

"Stratum follows institution, never geography and never blood" (R23-3-STRATUM_FOLLOWS_INSTITUTION). Mixed parentage takes one register (R23-4-MIXED_PARENTAGE); renaming at change of allegiance "is Japonic-only" (R23-4-RENAMING_IS_JAPONIC_ONLY); a house name given to a retainer "is an event with a cost attached" (R23-4-SERVICE_TRANSFERS_REGISTER). Outside the five: Zettari (R32-1-ZETTARI_REGISTER_SWAHILI_BANTU_ARABIC); Dawi, Elven, Goblinoid (R23-6-UNTOUCHED_REGISTERS); Holy Sea (R20-2-HOLY_SEA_NAMING); Undaar-Keth (R20-2-UNDAAR_KETH_NAMING); Beastkin (R20-1-BEASTKIN_ANCHOR); Celestial Host (R40-2-CELESTIAL_HOST_NAMING_PASS).

**Banks.** In `wiki/The Tongues of the Realms/`: `Moto Element Inventory — Japonic Stratum.md` (R40-1-MOTO_ELEMENT_INVENTORY), `Element Inventories — Mahuo, Yukari, the Elven Branches, Beastkin.md` (R37-1 to R37-4), `The Celestial Host — Naming.md`, and the Runic Dawi, Eressean and Varrisak, Old Vaross, Accord Latin and Common pages; the Register note in `wiki/The Archaic Bloodlines/The Zettari.md`. Chinese and Far-Northern: `sources/WOTR_Inner_World_Naming_Amendment.md` §X, §XI. The Concord given-name pool and Dawi elements: `sources/WOTR_Naming_Guide_Amendment.docx` Part Three, whose Satulagi/Moto inventory is struck.

**Stale, never written** (`stale_names` lists residue):
- "Büri is dead everywhere, without exception" (R20C-1-BURI_DEAD_EVERYWHERE, R22-1-HOUSE_STRUCK), with every Mongolian-register name and term: Möngke, Sarnai, Temür, Saruul, Chuluun, Enkhtuya are Bara, Mizuki, Sodoku, Yukazuri, Sonzai, Emira (R22-2-NAMED_CHARACTERS_TABLE); Altan, Tsagaan, Ulaan, Khökh, Möngön, Zes, Manan are the Lines Kōkan, Byakuya, Kurenai, Tenrai, Shirogane, Akagane, Amagiri (R22-3-SEVEN_LINES_TABLE); Ajiin is Hataraki, Khar Ild is Kurosetsu, and the other sights, Works and doctrines follow R22-4-SYSTEM_TERMS_TABLE, R22-5-SEVEN_WORKS_TABLE, R22-6-DOCTRINE_COINAGES_TABLE.
- The Polynesian register (R23-1-POLYNESIAN_REGISTER_STRUCK); Sātūlagi "does not exist and never did" (R21-1-SATULAGI_STRUCK). Taulagi is Heisuke, Afasoa is Sadamu, called Futakoto (R23-7-TAULAGI_AFASOA_PENDING, ruled). Muken's queen is Ayame Yuno (R22-2-UNAFFECTED_CHARACTERS, notes). Saishiki is Fusi Vā (R22-7-FUSI_VA_KEPT).
- Airag, borts, aaruul, the deel, Tengri are the skin, windmeat, stonecurd, the hide-coat, the Sky (`desktop/NATALIE.md`, ruled under R23-8-KHARVEN_INVENTORY_DECOUPLED).
- Zettai is Zettari (R32-1, notes). No Tier is "Absolute" or "Chosen"; the title Chosen of the Codex stands (R42-1-TIER_NAMES_ARCHMASTER_PARAGON). The black stones are never "shale" (R28-1-BLACK_STONES_SHALE_ANALOGUE).

**A new minor name** (pass): prefer the role ("his mother"); name only someone who acts; ask who wrote the name down; build from that bank only, a Northern given name from the Concord pool (R20-3-CONCORD_GIVEN_NAMES); coin no outlier, which needs "a reason that exists in the workbook" (R23-5-OUTLIER_BUDGET); avoid long-vowel marks (§6); grep `wiki/` and `scenes/` for a collision; report it in `new_names`.

**Not ethnicity.** "Naming registers are not ethnicity. This ruling is unchanged. A Japonic-sounding name is evidence about a house's linguistic descent, nothing else" (R8-21-REGISTER_NOT_ETHNICITY). No Lore infers race or homeland from a name.

## 4 Numbers and mechanism

A Lore section states no number the card does not state, and in practice states none.

- **Never:** Level, Stage, Band, Grade, Tier number, eta, EU, AU/s, Coherence, Aether Class, Crystal tier or State, stat names or values. They reach the page "in a mouth, an instrument, a document, or a practitioner's private count" (R14-4-DIAGNOSTIC_CHANNEL); "Grade letters and stat names never appear in narration" (R14-4-EFFECTS_CHANNEL; R14-6-CHECK28; R12-5-NUMBERS_DIAGNOSTIC_ONLY).
- **No invented figure** (pass): no age, year, count, distance or duration the card or a scene does not state; copy one exactly or write without it.
- **No apparatus:** no bracketed glyph (R18-4-GLYPH_NAMING_CONTEXTS), Category name (R10-2-CATEGORY_REGISTER_DEFAULT), Family, Physics Domain or Codex line. A true name "never appears in narration"; the gloss "never appears in prose" (R8-26-NAME_NEVER_NARRATED, R8-26-GLOSS_NEVER_IN_PROSE).
- **May:** consequences as behaviour and physics (R14-4-EFFECTS_CHANNEL); the common tongue of the crafts and the draw (R9-2-COMMON_TONGUE_LEGAL, R11-2-VOCABULARY_TIERS); a Wellspring, Archon or Titan the card's Identity or Catalyst Event names, spelled as the card spells it (R14-5-NEAR_MISS_FAIL), Cymorath as motion and cold as Vohrin (R27-1-CYMORATH_AIR_OF_ASCENT_FROST_ON_VOHRIN); a rank the card gives, as the world addresses it (R20-5-FORMAL_ADDRESS).
- **Mechanism stays on the card:** "The sheet explains" (R8-11-SHEET_EXPLAINS). "How it works is required, why it is possible is not" (R17-6-MECHANISM_VS_ORIGIN); origin "stays mythic" (R20C-23-ORIGIN_STAYS_MYTHIC). Epoch-scale powers "never resolve a plot" (R7-2-EPOCH_SCALE_SURVIVES). "No sentence explains why a proofed round defeats a proofed plate" (R11-3-FIREARM_PROSE_LAW). The economy is "finite, spent, visible" (R7-1-THREE_HARD_RAILS): each gift in The Making is paid in The Cost, and "Overuse strains him" is no cost (R8-16-OVERUSE_STRAINS_FAILURE).

## 5 Character first

Before Origin is written, answer three questions from the card: what does this person refuse, what did they survive, what do they believe that costs them.

The order is `desktop/NATALIE.md`'s: these three, "then the phenomenon, then the Codex"; that order "survives untouched" (R12-8-ABILITY_GUIDE_REWRITE).
- **Refusal** is an act the record can point to (R5-B-DECLARATION_TO_INFERENCE).
- **Survival** is a named event and its accommodation; "the unconsolidated ones are the character" (Characters page).
- **The costly belief** shows in the choice it forced and the concrete thing it took.
- **Swap test.** Lines that "could be swapped and nobody noticed" fail (R15-1-VOICE_DIFFERENTIATION): a paragraph that fits another card is cut. Images come from the character's own trade, the principle R19-4-WORLD_ANCHORED_SPEECH sets for speech.
- **Ties bear load:** "the people someone loves are a load-bearing part of what they can survive" (Characters page).

## 6 Open on the docket

`check_docket` for these seven tags returns no pending or proposed row (2026-09-24), and CONFLICTS.md C-001 to C-029 are closed; what stays open lives in live rows and on the cards, and no backstory settles it.

- Every card's Open Rulings.
- R40-1-MOTO_ELEMENT_INVENTORY: glosses of Doku, Muken, Bara, Zuri; Tenrai-marked names after the massacre; Kōkan as a Line name; Artemis and Emira as outliers.
- R40-2-CELESTIAL_HOST_NAMING_PASS: Faisal's and Verantha's Lawbell-names are unassigned; the rank ladder and the Archon-name form are flags.
- R37-1-MAHUO_ELEMENT_INVENTORY: the generational syllable in Ara Min and Mu-jin; Kwon as a Mahuo cadet branch.
- R37-2-YUKARI_ELEMENT_INVENTORY: a second topographic surname beside Yukari.
- R37-3-ELVEN_BRANCH_ELEMENT_INVENTORY: marin unglossed; apostrophe-style names on cards against the inventory.
- R37-4-BEASTKIN_SOUL_NAME_INVENTORY: Name-Keeping outside the Fox lineage; soul-name and held-name as one name or two.
- R23-12-ICE_ROLL_NAME_PENDING (ruled): Hild and Robin Ice carry a name nobody in the south has heard, and "it gets a scene, not a line"; no Lore names it or spends a line on it.
- R23-5-OUTLIER_BUDGET: one in eight is coined, not ratified.
- R4-H1-WREN_ASSIGNED, R4-H2-EDWARD_LAMBERT_ASSIGNED: "pitch only"; their fighting is told as the scenes show it.
- R11-4-WELLS_ORIGIN, R13-3-PHENOMENON_BANK, R8-3-WORKED_EXAMPLES_PENDING: the origin of Wells, the Phenomenon Bank seeds, AUCTORITAS and KŌMYAKU are unratified.
- R20C-9-ANCESTRAL_SEAT_WORKED_CORE: "why that site and no other."
- R28-1-BLACK_STONES_SHALE_ANALOGUE: whether Voidfall Stone acts as Shale does "is not recorded".
- R36-1-YASOSHIMA_SINK_YUNO_SECRET: "no character outside the Kagura officiant line knows it."
- Unruled: Convention Six of `wiki/Races & Peoples/The Tongues of the Realms.md` forbids diacritics, yet R40-1's bank and the cards carry them (Kōkan, Sōhai); attested names keep their card spelling.

## 7 A worked example

One paragraph about no card: Ralf Dunstansohn is a Northern-stratum name built from the Concord pool, and he must never become a character.

> Ralf Dunstansohn was born in a carter's yard beside a post road, to a father who never held a charter, and the muster clerk wrote him down by his father's name. He learned the sword from a sergeant who taught with the flat and would not show a guard twice. The winter the company held the ford, the river ice broke under the sergeant's horse. Ralf went in after him. He dragged the old man out by the collar and kept him breathing on the bank until the carts came back. The sergeant lived. His left hand never closed again, and the company paid him off before the thaw. By spring the men called him Ralf Ford, and the clerk, who had no field for a byname, left it off the roll. He still refuses to cross running water on foot while any bridge stands in reach. He believes the man who taught him is owed a living. He pays it. A share of every wage he draws goes north to the sergeant, and he has never asked whether it arrives.

A live patronymic (R23-2-NORTHERN_STRATUM); a byname the roll cannot file (R20-4-ACCORD_FILING_CONVENTION); `verify.py` passes.
