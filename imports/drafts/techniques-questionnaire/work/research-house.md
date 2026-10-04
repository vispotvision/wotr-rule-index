# Techniques and characters: how the cards and technique entries actually read

House research for the techniques-and-characters questionnaire, 2026-10-04. Read-only: nothing in the archive was changed.

## 0. What was read, and how to read the references

Card paths sit in the Volume I cards folder, whose name carries a dash, so they are written here as a glob: `wiki/Volume I*/<name>*.md`. The Fracture of Worlds mirror is `wiki/Fracture of Worlds*/`.

- **Eight cards, read whole:** Borin Ironheart (`Borin*.md`), Yoko Mishiro, Renard Greymane, Cozbi Mahuo, Kwon Mu-jin, Malphas (`Malphas*.md`), Muken Moto as the Moto card (Sodoku Moto's and Emira Moto's read for structure only, nothing voiced), and the NPC roster `table/npcs.yaml` (Lei Yanshu and Registrar Anselm Pike as its rich and thin ends). For comparison: Aelor Vaelith (the commonest shape), Gorvan Aldric Voss, Dougou Ozumu Zettari, and the Kharven cast headers.
- **Technique entries:** `wiki/Techniques/` (56 pages): Bloodbind Surge, Hunter's Breath, Final Mercy, Sigillum Fixationis, Obelisk of the Eclipsed Dawn.
- **The template:** `SHEET_SECTIONS` at `build/mcp_server.py:940` to `955`; `convert_character` at `:1109` to `1180`; `create_character` at `:996`; `build/recost.py` (the stat re-coster); the Ability and Technique Design Guide, 2026-09-12 edition (`~/wotr-vault/true-canon/`); the Ability Law rows R47-1 to R47-5 (`rules/doc-ability-law-2026-09-26.yaml`).
- **Census figures** are grep counts over all 284 Volume I cards: close, not exact.

Glossary. **EU** (Essence Units): reserve, one EU to the megajoule (R44-1). **AU/s**: output rate. **η** (eta): efficiency, the share of spent Essence that becomes work, not heat. **Level** (1 to 500) sits in five **Bands**; **Stage** (I to XVI) sets the stat ceiling. Eight **Primaries**, each with eight **Sub-Stats**. **Grade**: the letter band a value falls in. **Pool**: the stat points a Level and Stage have earned. **Codex line**: a working's catalogue entry (Wellspring, Family, Physics Domain, Category, Stage). **FOW line**: its stat requirement (governing stat, Stage floor, Grade, **Path gate**, a cap lifted only by walking a Path, and **Resonant Pair**, two Sub-Stats whose joint height unlocks an effect). **Readout**: the LitRPG status text the Crystal or an instrument prints. **Catalyst Event**: the crisis that opened a Stage. **Starvation**: the reserve floor below which a practitioner collapses.

## 1. Settled: what the questionnaire must not re-ask

The Style Law (R70, answered 2026-10-03) and the Combat Law (R71, answered 2026-10-04) already rule most of what a card or technique shows on the page. Listed so the questionnaire asks how these become card fields, never whether they exist.

**Readouts and progression (R70).** The Crystal is the screen, the bearer reads only his own sheet, instruments read others (R70-77, R70-78). Figures inline, a block only at a re-assay that moves something, a breakthrough or an arc's end (R70-80); clinical voice (R70-81); numeral beside Stage name (R70-82); narration states what the POV holds (R70-83). Growth readouts at a Level, a Stage, a new Trait, first Wellspring contact (R70-84); in-scene at appraisal, wound and Essence spent, three a scene, outside the two-voice cap, Grades at the read, body first (R70-85 to R70-89). Numbers climb only for a seen cause (R70-90); breakthrough inside its crisis, confirmed at a public re-assay (R70-91, R70-92); build talk (R70-93); item card once (R70-95); Guild commendations (R70-96); contract boards (R70-97); sheet changes at chapter end (R70-98); estimates printed, marked (R70-99).

**Technique and character names (R70).** Numbered forms by school; four-syllable true names for the lineage halls and Korean stratum (R70-74); numbered rites (R70-75); the world's law stated, reasons kept (R70-76); the release call costs a beat, nobody translates his own art (R8-24, R8-26). Comic names, their banks and who carries one, never Isaac's or the other creators' characters (R70-119 to R70-132, R52-14); Borin's brothers done (R70-126).

**Combat Law (R71).** A narrowing vow raises output through Attraction Force by a figure set on that card; breaking it is a Shear Break (the bond turning on its bearer); its terms are its counter (R71-32). A card's **Readiness** figure overrides the Alacrity row (the default casting-speed row) in a casting race (R71-28). Fusion only as a carded Synergia technique (R71-39). Each card names its grammar: Verdict, Blade, Percussion or Expenditure (R71-69). Traits named at first fire (MC11). Alchemists get a "reads first" voice line (R71-72). A Draft gets one card (AL9).

**Ability Law (R47).** The field format: Summary card, Codex line, FOW line, Origin, then Physics, Metaphysics, Mechanism, Essence, Counterplay; Design Chain and six-line card retired as page formats (R47-2). Counters and tells as facts (R47-3). Cost as a share of reserve off the Essence Ledger (R47-4). Tier Ladder rung (the named step on the joules-to-Grade spine) on every item, summon, Domain, beast (R47-5). Never how to use it (R47-1).

**Numbers.** Fracture of Worlds, then the workbook, then the card (R20C-32); Fracture of Worlds' Stage names (R20C-30); never invent (R12-5).

## 2. The template on paper

`SHEET_SECTIONS` (`build/mcp_server.py:940`) lists fourteen entries covering seventeen sections: Identity; Soul Architecture; Work Architecture; Stats (IV and V merged); Force and Flow (VI and VII merged); Traits and Domain; Techniques; Spirit Axes; Resistances; Physical Description; Psychology; Equipment; Temperance Record; Fracture Log. `convert_character` hands a writer this skeleton with the Fracture of Worlds tables, stale-name flags, the source's numbers and seventy rules.

Three things in it have fallen behind the law:

1. **The technique brief is pre-R47.** Line 952 asks for "summary card + full Design Chain"; R47-2 retired the Design Chain as a page format on 2026-09-26, and the 56 Techniques pages already follow R47-2. The vault guide is the 2026-09-12 edition and still teaches the six-line card (Operation, Manifestation, Cost, Limit, Counter, What nobody knows), which R47-2 also retired. A writer following the converter, the guide and the Techniques pages would produce three formats.
2. **"Pending Isaac" placeholders.** Lines 1122, 1165 and 1172 tell the writer to enter "pending Isaac" for any missing number, and line 1176 "originated, pending ratification". R70-99 now says print the estimate, marked; the standing direction of 2026-09-25 is that nothing waits on Isaac. The converter is the one tool that still manufactures placeholders.
3. **Fields the skeleton never names**, though the archive or the law has them: the pronunciation line (R50-34; present on 276 of 284 cards); the dated "As Of" header (187 cards); the voice block (R52-03); the Lore section (282 cards, added by a later pass); combat grammar (R71-69); Readiness (R71-28); vows (R71-32); a readout or status block; any record of XP or progress toward the next Level; commendations and Third Names (R70-96); a comic-voice flag (R70-113).

Two structural facts sit under the template. `build/recost.py`'s docstring keeps cards in a "two-layer shape (Primaries and listed peaks)" and states that the sixty-four-entry table is not invented. And the Stat Sheet workbook (`FOW_Stat_and_Magic_System_Codex.xlsx`) has eight tabs, all system tables, none per character: despite the precedence ladder, the card is the only per-character numeric record that exists.

## 3. Five shapes of card in practice

The 284 cards do not share one template. Heading counts sort them into five shapes.

| Shape | Examples | Roughly how many | What it carries | What it lacks |
|---|---|---|---|---|
| **A. Full seventeen, roman headings** | Borin | 14 to 20 | Every section as its own heading; techniques in the old Design Chain (Wellsprings, Trigger, Function, Mechanism, Numerical Effect, Target Response, Cost, Counterplay) | Codex and FOW lines per technique; Phenomenon; readout shape |
| **B. Merged "Card N" layout** | Yoko (Card 20), Kwon (Card 21), Cozbi (Card 24), Sodoku | about 25 | Paired headings (IV and V, VI and VII...), tables for stats with Sub-Stat peaks, techniques as a three-column table, bold-italic pull quotes, a Core Wound / Flaw / Desire / Loop table | Per-technique Codex and FOW lines; Cost column on some tables |
| **C. Compact re-costed card** | Aelor Vaelith, Gorvan | 100 to 180 | Identity, Soul Architecture, Wellspring Harmonizations, Primary Stats with Pool and Allocated, fourteen Sub-Stat peaks, Traits, Kit, Signature summary card, Limits and Counters, a Codex line at the foot | Psychology, Description as a section, Temperance Record, Fracture Log, voice block |
| **D. Table-cast header card** | Renard, Bram, Brida, Lambert, Hild, Lorn, Osric, Heisuke, Nella, Soren, Garret | about a dozen | A boxed header (Level, Stage, Band, Role), Description, sometimes a Voice block, a long Lore | No stats, no Traits, no techniques, no Force and Flow |
| **E. One-offs** | Malphas (two sheets, living and lich); Muken (dead king, with an "Incomplete in the Record" section) | a handful | Malphas: the only full sixty-four Sub-Stat array, Pool arithmetic, reserve to a tenth of an EU, turns to Starvation, Resonant Pairs, a Counter in plain words | Malphas: a voice block |

Over all five sit two later passes: the **Lore** section (282 cards, dated 2026-09-24, five fixed parts: Origin, The Making, The Cost, Where They Stand, Ties) and the **voice block** (28 cards).

The sharpest finding is shape D. The live Kharven thread's cast are the thinnest cards in the archive. Renard's card is 2,336 characters before its Lore; its FOW line, as `fow_line` returns it, is one header line. NATALIE's Table Rule 5 adjudicates fights from Pack Fourteen §3 stat rows, and for these people there are no rows to read.

## 4. Section by section: rich and thin

**Identity: rich.** The Catalyst Event is the strongest field in the archive, a story beat rather than a stat: Borin's (`Borin*.md:26`) ends "permanence is a gift offered, not a sentence imposed." The "As Of" line anchors a card to a moment. The pronunciation line is near-universal.

**Soul Architecture: rich, uneven vocabulary.** Crystal State is often the best prose on a card ("Borin calls them the invoice"). Aether Class is a number on some cards and a job description on Muken's.

**Stats: the least settled section** (§6).

**Force and Flow: specific, often unanchored.** Borin's lifting strength, "est. 100 to 500 billion tonnes" (`Borin*.md:100`), has no row behind it; Muken gives petajoule strikes with no Level at all.

**Traits: good on mechanism, short of the R17-5 test.** R17-5 asks each Trait to name the Lattice property it alters. Borin's Ironheart and Kwon's "Loose Thread" read well but name a Wellspring or a stat, not the Lattice property. Muken's Traits give percentages ("+300 to 500% standing load tolerance short-term") without source.

**Domain: rich where present.** Borin's Adamant Forge has Name, Stage, Principle, Environmental Signature and Limitation, the limitation in plain words ("a man who must be visited"). No Domain carries the Tier Ladder rung R47-5 now asks for.

**Techniques:** see §5.

**Spirit Axes: rich and load-bearing.** Weight words (Absolute, Heavy, Growing) are consistent across shapes A and B. Cozbi's son as an unconsenting axis is the archive at its darkest and best.

**Resistances: thin and generic** except where a vulnerability is written as a fact ("A combat-focused practitioner of equivalent Stage can outmaneuver him").

**Physical Description: rich on major cards** (Borin's beard "thick enough to insulate a chimney"), absent on shape C, partial on Muken ("Clothing and scent are unrecorded").

**Psychology: strong.** Desire, Loop, Core Wound, Flaw, Foil, Stress Default. The Loop is the archive's best field: Kwon's "Sees the truth clearly, states it plainly, gets punished".

**Equipment: thin against the law.** No item carries R70-95's Tier, Latin form, Grade band, maker, stamp and price, or R47-5's ladder rung. Borin's Ur-Maul has a Wellspring and an effect, no mass or point of balance (R13-9). Yoko's card states plainly that no gear is catalogued "rather than filled with invented items", a good honest gap.

**Temperance Record: prose on old cards, a list on new ones.** Borin's is a story per Stage band ("The Eight Silent Years"); Kwon's is one line a Stage. Neither records Levels, XP events or dates.

**Fracture Log: the best bridge between mechanism and feeling.** Its template (fracture, Layer, Status, "Feature: yes/no") is worth keeping.

## 5. How techniques are written

### On the cards: five formats

1. **Design Chain blocks** (Borin): Wellsprings, Trigger, Function, Mechanism, Numerical Effect, Target Response, Cost, Counterplay. Mechanisms are real chains ("Exuroth quench-temper cycle applied to Soul Crystal lattice", with martensitic hardening, steel's quench hardening, named). Costs are the best in the archive because they are permanent and personal: each Adamant Requiem took a slice of his reserve that "did not grow back."
2. **Three-column tables** (Yoko, Kwon, Cozbi, Sodoku): Technique, Function (and mechanism or cost), Counterplay. Kwon's mixes trigger, figures and cost into one cell: "~1400°C at the face", "~2% of reserve per use". Yoko's table has no cost column at all.
3. **Bulleted Trigger / Function / Mechanism / Cost / Counterplay** (Muken), with romanised Japanese true names and English glosses ("Hametsu Kessan, Ruined Account Settlement"), costs in absolute EU.
4. **Summary card** (Effect, Cost, Limit, Counter, What nobody knows) on 145 cards, mostly shape C's "Signature".
5. **Malphas's Signature**: Effect, Cost, Limit, Counter, and a "What nobody knows" set off as a quote.

None of the five carries a per-technique Codex line and FOW line together. A "FOW line" heading appears on two cards; "Physics Domain" on eight; "Path gate" on six; "Resonant Pair" on one (Malphas). No card carries Readiness, combat grammar, a vow field, a tell field (the word "Tell" appears on five cards) or a numbered form.

### On the Techniques pages: the law already met

The 56 pages in `wiki/Techniques/` follow R47-2 to the letter. Bloodbind Surge runs: Summary card; Codex line (Wellsprings, Family, Physics Domain, Category, Craft, Stage floor, Grade, Path gate); FOW line (governing Sub-Stat with figure, Trait invoked, Resonant Pair); Origin; Physics (Phenomenon, Law, Limit, Energy, with a worked table: Achilles tendon failure at 4 to 6 kN, bone 1.36 times stronger in compression); Metaphysics (Aether, Wellspring, Trait, Terrain, Inherited failures, Theory, School); Mechanism (Glyph, Boundary, Effect, Hold, Ceiling, Failure, Bleed); Essence (cost table, duration in six-second turns, uses before Starvation); Counterplay (Tell, Limits, Fails against, Look up). Obelisk of the Eclipsed Dawn prices a reversal with Landauer's principle (the energy cost of erasing information). Real figures, counters as facts.

Two gaps between the pages and the cards:

- **No link either way.** Zero cards link to a Techniques page. The pages are anonymised ("Self-derived by its author during the Vorynn Trials"); Bloodbind Surge belongs to the Vorynn Bloodbind carried on Draven Kael Vorrick's and Kael Serradyn's cards, but neither page nor card says so. R12-3's named-inventor rule (a documented technique is counterable by anyone who studied it, a self-derived one must be read live) depends on knowing whose it is.
- **Practitioner bands, not people.** Each page's Essence block reads a Stage band ("Glory, Expert, reserve 51,800 to 961,000 EU"), so its cost table fits any holder. That is correct for a school art and wrong for a signature: a card's own Level fixes its reserve exactly under the Level law.

### Mechanism, cost and counter in practice

- **Mechanism** is strongest where a real process is named (Borin's metallurgy, Kwon's calcination, Bloodbind's compression routing) and weakest where a Wellspring is listed as the mechanism ("Fractura tracks, Judicium ranks, Coagulatio compresses").
- **Cost** comes in four currencies: share of reserve (Kwon, the Techniques pages, R47-4's rule); absolute EU (Muken, Sodoku); body and Crystal damage (Borin, Muken's "torn fibres, scar rupture"); and vague ("negligible EU", "Massive EU drain"). Share-of-reserve billing at high Level produces large joules: Kwon's Vocatia at 5 to 15 percent of 850 million EU is 4 to 13 × 10¹³ J a summons. The Techniques pages answer this ("the joules are ambient"); the cards do not.
- **Counter** is present on 197 cards but sometimes absent in substance. Cozbi's Root Severance reads "None documented once contact is made" (`Cozbi*.md:119`); Yoko's Threat Assessment Scan reads "None confirmed". R12-3 and R47-3 require a counter that falls out of the mechanism.
- **What nobody knows** has drifted. R17-3 scopes it to a question about why the law holds. On shape C cards it often becomes a character note: Gorvan's asks whether his patience is strength. Malphas's ("What the Black Star Core is a pseudo-organ of") and Final Mercy's (why the collapse runs Soul, memory, Principle in that order) keep the rule.
- **Chants.** Borin's techniques call for "Latin incantation" and "Latin liturgy" (`Borin*.md:147`, `:173`); R15-A folded the Latin requirement and the chant now follows the practitioner's own tongue (R50-26, R51-28), so a Dawi smith in Latin reads as a leftover. Kwon chants in Latin ("Falsum ardeat, verum maneat"); as a Guild Accord Archmagus that may be his learned tongue (style law VB3), but his card does not say which.

## 6. Numbers: where they come from, and how estimates are marked

### Three stat economies on one shelf

- **Single value per Primary near the Stage ceiling, peaks beside it** (Borin, Kwon, Yoko, Sodoku, Cozbi, Aelor).
- **Primary as the total of its eight Sub-Stats, Grade read off the mean** (Malphas living: Ardency 2,100 total, mean 262.5, Grade B; the totals sum exactly to his allocated 11,000).
- **Primary as a single value again, on the same card** (Malphas's lich table, Ardency 1,500): its eight values sum to 9,799 against an "Allocated 23,095".

### Pools that do not match today's formula

`recost.py`'s `current_pool` (12, 15, 18, 21, 24 points a Level by Band, plus Stage × 100 per Threshold, Stage I counting, R39-3) gives:

| Card | Level, Stage | Pool on the card | Pool by formula |
|---|---|---|---|
| Malphas (living) | 350, X | 11,050 | 11,050 |
| Malphas (lich) | 475, XIV | 23,100 | 18,900 |
| Kwon | 430, XII | 18,800 ("verified") | 15,120 |
| Borin | 378, XII | about 18,000 | 13,938 |
| Aelor | 246, VIII | 9,480 | 7,128 |
| Yoko | 145, V | about 4,100 | 3,375 |

Only Malphas's living sheet is on the current economy. Kwon's and Yoko's both claim to be verified against their Level's "real point economy" and are not.

### Reserves that do match

The Essence Ledger's Level law (log₁₀ EU = 3.4202 + 0.012812 × Level, ruled governing in C-076, 2026-09-26) has been applied: Yoko 185,000 against 189,644; Borin 180,000,000 against 183,288,830; Kwon 850,000,000 against 849,884,679; Malphas 80,241,677.6 exactly. Yet Borin and Yoko still mark these "(est.)" and "(estimate, no exact source figure exists)": the flags outlived the fix. Sodoku's 1,340,000 sits far under the law because his card states Residual Strain (what a Crystal builds when its Level outruns a Stage gate), which is coherent.

### Sub-Stat names from before the merge

Part Twelve consolidated 120 Sub-Stats into 64 and kept a Merge Ledger (Diagnosis into Analysis, Endurance into Constitution, Inscription into Density, Confluence into Synergy, Memorium into Retention, Conversion into Yield). Retired names still appear on many cards: Diagnosis 60, Fidelity 46, Inscription 39, Endurance 37, Saturation 25, Detonation 24. Kwon's Gnosis peaks include Diagnosis and Sapience; Borin's include "Gnosis Diagnosis" and "Dominion Density" (Density is now an Ardency Sub-Stat); the lich half of Malphas lists Saturation, Severance, Spectral, Detonation, Adaptation and Voidance, none of them in the sixty-four, while his living half uses only the sixty-four. Readouts (R70-83) print Sub-Stat names, so this drift will reach the page.

### Stage names and gates on the table cast

Thirteen cards, every one a table-cast header card, still print the old Stage names (Ignition, Hold, Temper, Surge) against R20C-30. And four Kharven cast cards pair a Level with a Stage that Part One's gates forbid (Stage IV before Level 100, VII before 200, X before 300, XII before 400): Lorn Stark 168 at Stage III, Edward Lambert 142 at III, Bram Greymane 224 at IV, Heisuke 278 at V. None states Residual Strain, the gate's own consequence. R14-F (Renard, 198 at IV) was closed as legal; these four were never put.

### How estimates are marked

At least six styles: "~850" (Borin's table), "(est.)", "(estimate, no exact source figure exists at Level 145)" (Yoko), "No source figure" and "placed at the floor of his Stage's band" (Malphas, the clearest), "constructed to fit Stage XIV's real ceiling" (Cozbi), and a whole-section confession ("No numeric stat block exists for Cozbi in canon", `Cozbi*.md:68`; "Incomplete in the Record", `Muken*.md:202`). R70-99 settled that estimates print, marked; nothing settles one marking.

## 7. Voice blocks

Twenty-eight cards carry the fixed block R52-03 asks of every major card: Notices first, Sentence length, Contractions, Pet word, Never says, Stumbles, Gloss rights, Under stress, In grief, In joy, Sample line. Where present it is the most usable part of a card at the table. Borin "never" contracts and never says "I will"; Yoko's pet word is "Exact"; Muken's is "Tell me". The grief slot is consistently strong because it sends each voice back to a root tongue (Runic Dawi, the fox-register, the Sum-gol house tongue, a Nalūn trader's talk).

Gaps: Renard, in NATALIE's Voice Roster, has no block; nor does Malphas, though R69-10 rules his saying. Shape B cards keep a one-cell "Voice" in the psychology table beside the new block, so two voice descriptions can disagree. No block carries R71-72's alchemist "reads first" line yet (Kwon is the obvious first case). The NPC roster's voice field runs on a different, freer pattern (§9).

## 8. Lore sections

Two hundred and eighty-two cards carry "Lore · The Life Behind the Card", written 2026-09-24 by the character-lore pass from the card plus archived scenes, each opening with a provenance line. They are often the best prose on the card and frequently longer than the card above them: 53 cards exceed the 16,348-character cap with Lore, 10 without it.

The Lore can contradict its own card. Yoko's body still names her husband "Temür" and her son "Riku" (`Yoko*.md:26`, `:61`, `:86`), a stale Büri-register form, while her Lore and Ties say Sodoku Moto and Rikudoku: the Lore was written in Moto canon over a body nobody swept. Garret Longshore's and Osric of Hallenfeld's descriptions carry the same "Temür".

## 9. The NPC roster

`table/npcs.yaml` holds ten entries, all on the Mu-jin thread; the Kharven thread has none. The schema (`build/table.py:253`) is name, thread, want, refusal_line, knows, lied_about, last_seen, voice, last_updated. Two depths:

- **Rich** (Josse Osricsson, Lei Yanshu, 2026-09-25): a want with a mechanism, a refusal line with its scar ("I will not write a figure I did not take"), knowledge tagged to Ledger lines (L031, L032), a lie that stays uncorrected until a named check, naming logic cited to the Inner World Naming Amendment, and a voice field that has absorbed a swap test, gloss rights, and for Lei Yanshu a partial FOW line ("LINE NOT SET: Band I"), a tell and a counterplay.
- **Thin** (the 2026-09-28 batch): one-line wants, empty knows, voice as a single image ("Wide nib, round broad hand", Anselm Pike).

The schema has no field for physical inventory (Table Rule 11 asks for it on first sight), FOW line, comic name, culture, or card link. Two entries still say "flagged for Isaac", and Maud Harrowgate's "since Monday" breaks R51-08's ban on Earth day names.

## 10. What repeats

- **Catalyst Event, Loop, Fracture Feature**: a wound, the behaviour it locks in, the scar as architecture. The archive's signature move.
- **The cost that does not grow back** (Borin's Requiems, Malphas's frozen Conversion, Cozbi's "Pure loss"). The grimdark lives in the costs.
- **Bold, bold-italic and boxed pull quotes** on shape B cards, heavy enough that emphasis stops meaning anything.
- **Dashes in card bodies**: the prose bans (R48-03, R15-1) bind the page, not the sheet, and the cards are full of them.
- **Duplicated header blocks** left by machine passes: Renard's and Brida's Level line twice, Bram's three times; Dougou's technique table repeats "(4,800 EU at η 0.99), B-Grade" inside one cell.
- **A Codex line at the foot** of shape C cards, with no FOW line under it.

## 11. What is missing for the new LitRPG and Style Law

1. **A screen.** R70-78, R70-80 and R70-84 say where and when readouts appear. No card says what the screen shows: fields, order, precision. Malphas's living sheet is closest.
2. **Progress toward the next Level.** Fracture of Worlds Part One prices XP events (repetition decays to ten percent by the fifth engagement; zero-risk fights earn thirty percent; first Wellspring contact is a one-time surge). R70-90 binds every climb to a seen cause. No card records XP held, XP to next Level, or the event that moved the last number.
3. **One stat economy.** Two layers or sixty-four; Primary as value or as total; the current Pool; Sub-Stat names from the sixty-four only.
4. **A technique card that is the Techniques page.** Readiness (R71-28), combat grammar (R71-69), vow terms and figure (R71-32), Synergia partner and cost split (R71-39), numbered form or true name (R70-74), Tier Ladder rung (R47-5), tell and counter as facts (R47-3), and the named inventor (R12-3).
5. **Item cards** with Tier, Latin form, Grade band, maker, stamp, price, lore (R70-95).
6. **Commendations and Third Names** (R70-96) as a card line.
7. **Comic standing**: whether a character is a carded comic voice or double act (R70-113), and the comic name's bank.
8. **The table cast built out.** Renard, Bram, Lambert, Hild and the rest need stats, Traits and techniques before Table Rule 5 can name a deciding row.
9. **A converter that matches the law**: R47-2 field format, R70-99 estimates, and the missing fields of §2.
10. **NPC roster parity**: physical inventory, FOW line, comic flag, culture.

## 12. Questions the archive raises

Candidate topics, each on ground the two laws left open.

- **The screen:** what the Crystal shows (fields, order, exact figure or Grade), and whether it differs by Path or culture.
- **Stat economy:** two layers or the full sixty-four for major cards; Primary as value or total; bringing old Pools onto R39-3.
- **XP on the card:** XP held, XP to next Level, a log of each Level and its cause.
- **Technique format on cards:** the full R47-2 page on the card, or a short card entry linked to a Techniques page.
- **Signature against school art:** owner's exact reserve for a signature, the Stage band for a school art.
- **Vows:** where a vow lives, how its figure is set, whether others can see it.
- **Readiness and grammar:** who gets Readiness first; grammar per character or per technique.
- **Numbered forms:** which schools (Moto Hataraki, the Greymane sword, Dawi forge-rites), how many, what holding a form means on the sheet.
- **Technique names:** owner's tongue, a learned tongue, or both; whether Borin's and Kwon's Latin stays.
- **Progression arcs:** prose record, Level log, or breakthrough list with Catalysts.
- **Card building:** the minimum before a major card's first play, an NPC's second scene, and an NPC's promotion to a card.
- **Estimates:** one house marking.
- **The table cast:** the order Renard, Bram, Lambert, Hild, Lorn, Osric and Heisuke get sheets, and how the four gate breaches read (Residual Strain like Sodoku's, or a corrected Stage).
- **Traits and equipment:** the Lattice property and first-fire beat on every Trait; an R70-95 card and ladder rung on every carried weapon.
