# Techniques and characters law map, for the techniques questionnaire (2026-10-04)

Sources: `out/rules.resolved.json` and `out/rules.live.full.md` (tags magic-design, character-sheet, stats, naming, codex); `rules/doc-ability-law-2026-09-26.yaml` (R47); Packs Eight, Nine, Ten, Twelve, Thirteen, Fourteen, Seventeen, Eighteen, Twenty; the Style Law (R70); the Combat Law (R71, rows in `imports/drafts/combat-questionnaire/law/rows-*.yaml`); `RULINGS.md`; `CONFLICTS.md`; `build/mcp_server.py` (`convert_character`, `create_character`, `SHEET_SECTIONS`); the skills `wotr-npc`, `wotr-stat-line` and `wotr-write/references/{technique-design,character-sheet}.md`; the wiki's Fracture of Worlds and Trait System pages; the Volume I cards. The docket (`out/docket.md`) reports 0 outstanding; every row in these tags is live or superseded, so "open" below means a gap, a debt the law left owed, or two live texts that disagree.

## Plain glossary (first use)

- **FOW**: Fracture of Worlds, the stat system (Levels, Bands, Stages, Grades, Essence figures).
- **Level / Band / Stage**: Level counts pressure (1 to 500); a Band is 100 Levels; a Stage (I to XVI, Murmuring to Apex) is a structural breakthrough of the Soul Crystal, gated against the Bands.
- **Primary / Sub-Stat / Grade**: eight Primaries, each the total of eight Sub-Stats; a Grade is the letter band (Hollow, F to EX+) read off a value. **Tier of Standing**: the nine named public ranks.
- **EU / eta (η)**: Essence Units (1 EU = 1 MJ, R44-1) and efficiency.
- **Codex line**: a working's filing in the Master Codex: glyphs, Wellspring (one of the Sixty sources of law), Family (one of eight), Physics Domain (the real physics), Category (one of twenty-six kinds), Stage. **FOW line**: the stats a working runs on and what it requires.
- **Craft**: the medium a working comes out of (Magicraft, Spellcraft, Runecraft, Draftcraft, and Chantcraft, see §4).
- **Trait**: a standing law held in a soul's Essence Core.
- **Resonant Pair**: two Sub-Stats from different Primaries at the same Grade, which unlock a passive bonus.
- **Synergia**: the Category for workings that briefly share one Essence structure across several practitioners.
- **Attraction Force / Shear Break**: the clean recognition force of the soul's Attraction Layer; the failure in which a Trait turns on a bearer who denies the truth that formed it.
- **Path gate**: what a character's Path (Body, Spirit, Attraction, Fate) structurally forbids.
- **Catalyst / Threshold / Residual Strain**: the quality of experience a Stage requires; the breakthrough itself; the strain that accrues when a Level hits a Band ceiling without the Threshold.
- **Roster entry vs card**: a short NPC record kept by `npc_set` vs a full character page in the wiki and Notion.

## 0. Settled by R70 and R71: do not re-ask

From the Style Law (R70, 2026-10-03):
- Technique name looks: numbered forms by school and long hall names taken; "Not taken: Brackets inside sentences." (R70-74)
- Readouts: growth at Level gained, Stage breakthrough, New Trait, Wellspring contact (R70-84); in-scene at appraisal, wound, Essence spent (R70-85); caps (R70-86); the bearer reads his own Crystal (R70-78); practitioners feel rank (R70-79); blocks only at milestones (R70-80); Stage and Band numeral beside the name, Tiers of Standing by name only (R70-82); narration states what the POV holds (R70-83); body first (R70-89).
- "Numbers move only for a cause the reader was shown: a FOW XP event on the page, or training named in a downtime turn." (R70-90) Breakthrough inside its Catalyst crisis (R70-91); public re-assay (R70-92); build talk (R70-93); commendations, no stat effect (R70-96); changes block (R70-98); hedged estimates (R70-99).
- Progression models Cradle, Reverend Insanity, Solo Leveling, The Wandering Inn (R70-6); arc shapes tournament, Well delve, training montage, episodic jobs (R70-18).
- Carded comic voices (R70-113); comic names for minors, villains and rivals, never major NPCs (R70-122); sobriquets and hall title ladders (R70-117).

From the Combat Law (R71, 2026-10-04):
- Casting race: "where you fill a card's Readiness, that figure governs" (R71-28). Release "As often as beats allow" (R71-29). Held reveals (R71-30).
- A Family counter chart above "the card's Counter field", which "stays the hard answer. You ratify the chart." (R71-31)
- Vows (R71-32), Traits at first fire (R71-37), Resonant Pairs under strain (R71-38), Synergia (R71-39): see §7.
- Faculty reads exact unless warded (R71-44); "Each card names its grammar; no fifth." (R71-69); the alchemist voice menu (R71-72); weapons by the POV's name (R71-90).

## 1. The technique entry: format and fields

**Settled.**
- R47-1-NO_APPLICATIONS: "An ability entry describes what the ability is, never how to use it". Mechanism, what it acts on, costs, limits, tell, counters; "the owner invents the applications." R48-35-USES: in a fight "each side invents its own".
- R47-2-FIELD_FORMAT (as corrected by the 2026-09-27 audit): field format "in the same look as the card top (Summary card, Codex line, FOW line, Origin)", with Physics, Metaphysics, Mechanism, Essence and Counterplay blocks, "a table for the numbers, and very little prose. The Design Chain and the six-line card are retired as page formats." It supersedes R12-3-CARD_PLUS_CHAIN, R12-3-DESIGN_CHAIN_RETURNS and R17-3-SIX_LINE_CARD.
- The working model is `imports/page-tops/Spellcraft/Fallacy.md` (top) and `imports/system-accounts/_edition/Spellcraft/Fallacy.md` (write-up), named in `wotr-write/references/technique-design.md`. Summary card fields: Effect, Cost, Limit, Counter, What nobody knows.
- R17-3-CODEX_LINE_ORDER: "Codex: [glyphs] / Wellspring / Family / Physics Domain / Category / Stage. Assigned after the phenomenon, never before."
- R14-8-ABILITY_GUIDE_FOW_LINE: "governing Primary Stat and Sub-Stats, Stage floor, Grade required, Path gate if any, Resonant Pair if any". R14-8-CHARACTER_SHEET_FOW_LINE puts it in the sheet's Techniques section.
- R57-11-MECHANISM_IS_EFFECT: "Mechanism and Effect are one thing." No Effect line that could be true of another mechanism.
- R17-2-THE_TEST: state it as "it does X to Y, which under Z produces W".
- R18-3-ENTRY_AS_CANDIDATE_ROW: every new working is written in Spell Index form; "The Codex is a living document and everything originated in play belongs in it or does not exist." R55-9: proposed glyphs stay "provisional".
- R57-26 (audit): published write-ups lose usage lines; a plain "reserve covers N uses" stays "only where it is a number, not advice".
- Other entry kinds (R17-5): a Skill names its cues or mechanics; a bloodline faculty states the quantity it acts on ("The Moto see is not an entry."); an artefact's working carries its own Operation line. Rituals: materials, sequence, errors (R12-6, R70-75). Projected shapes (R10-3); the Craft sets their durability (R13-2).
- R8-11-SHEET_EXPLAINS: "A reader must be able to adjudicate a fight from the sheet alone."

**Open.**
- **Full entry or table row on a card.** R47-2 governs "New abilities". The cards do not follow it: Cozbi Mahuo's Techniques section is a three-column table (Technique, Function and mechanism, Counterplay) with no Codex or FOW line per row, and the Banisher artefact page still runs the older Operation line / Codex line / Counterplay shape. Nothing says whether a card carries each technique's full field-format entry, the summary card only, or a row that links to a technique page. This decides card length (§8).
- **Signature and ordinary.** R17-3-COUNTER_MANDATORY makes Counter mandatory "on Signature techniques"; R12-3-COUNTER_MANDATORY on every entry; R47-3 keeps tells and counters on all. Whether a minor technique on an NPC needs the full block or a one-line card is unset.
- **The two lines overlap.** The Fallacy model's Codex line carries Craft, Stage floor, Grade required and Path gate (repeated in its FOW line) and no glyphs; R17-3 puts glyphs in the Codex line. Small, but every new entry copies the model.

## 2. Design order and derivation

**Settled.**
- R7-1-CHARACTER_FIRST: "Character first, system second." "The Codex is not a generator." R7-5: refuse, survived, believe-that-costs, then check the phenomenon comes out of it. R12-8 keeps character-first "untouched".
- R47-6-RESEARCH_STAYS: "the real phenomenon is researched first, and the cost and the limits are derived from the mechanism." R13-3-PHENOMENON_MANDATE: phenomenon named in the author notes before it ships. R48-14: name "the real phenomenon and its fault".
- R13-3-INVENTION_STEP and R48-18-INVENTION: "the real law plus one pinned variable, easy for a player to reason about." R48-17-NO_CLOSURE: where physics cannot close, "researched pseudoscience, metaphysics or another strange idea first".
- R13-2: every working explained at three strata (Aether, Wellspring, Essence); the Category's alignment tag "names which Plane carries the cost and which Plane the counterplay lives on."
- R17-4: "Cost, Limit and Counter are outputs, not inputs." R17-6: "how it works is required, why it is possible is not".
- R18-2: "The Codex is opened before the working is designed, not after" (for precedent, R18-7-CHECK39), while assignment comes after the phenomenon (R17-3). No new Wellspring, Family, Category or Tier without a demonstrated absence (R18-2-NO_NEW_CATEGORY_WITHOUT_CHECK).
- R48-19-BANK: the Phenomenon Bank is "a growing library"; R20C-28: its seeds become canon "the session someone is derived from it".

**Open.**
- **Who originates a PC's technique.** NATALIE has Natalie supply "how any ability works" once Isaac sketches one. Nothing says how far she fills a PC's technique (cost, limit, counter) before he signs it, or whether his sketched cost stands when the derivation disagrees.
- **Where the Bank lives.** R48-19 makes it a library; no file or page is named.

## 3. Costs, limits, counters, tells and fairness

**Settled.**
- R47-4-LEDGER_COSTS: "A new ability's cost is a share of full reserve." EU and joules from the Essence Ledger's band for its Stage; Grade off the joules to Grade to tier spine.
- R17-3-COST_DERIVED: "If the cost could be swapped for a different cost without changing the mechanism, it is decoration." R8-16: "Overuse strains him" always fails. R7-5-COST_AUDIT: "sixty percent of existing technique entries fail" and the audit stays the largest open job.
- R55-1: costs paid in one's own substance are "permanent and cumulative, with a hard lifetime limit".
- R2-6: costs legible to the user; "no consumable restores a practitioner's magazine"; "no technique holds ground".
- R47-8 waste is heat at the Shell; R47-9 every working inherits its Wellsprings' failures, "and opponents can induce them"; R47-10 governing Sub-Stats are the caster's; R47-11 six-second turn, "Healing and mending always cost more than breaking."
- R17-3-LIMIT_MECHANICAL: "A limit with no mechanical source is a rule the author imposed." R57-27: "A Path gate binds only the component it names".
- R17-3-COUNTER_MANDATORY: "If the counter is hit him harder, the technique has no mechanism." R47-3: counters and tells "written as facts only". R12-3-NAMED_INVENTOR_RULE: "A documented technique is counterable by anyone who studied it"; a self-derived one is read live (R71-23: shown twice, read at the third).
- R47-12 and R17-3-WHAT_NOBODY_KNOWS_SCOPE: the What nobody knows line asks "why the law holds, never about what the working does", and is never answered as fact.
- The skill's fairness pass (`fair-play.md`, Isaac's "fair and a challenge"): a cost that hurts, a findable counter, the lookup trail.

**Open.**
- **The cost audit's order.** Sixty percent of entries fail; the law never says which cards go first or whether an old cost is rewritten silently or as a ruling.
- **The Family chart (R71-31).** Owed, derived from Codex physics, and binding only once ratified. Until then counters come card by card.

## 4. Naming techniques, arts and forms

**Settled.**
- R8-21: "The true name is in the practitioner's own language." Register is not ethnicity.
- R8-22: true name, then a literal gloss, "Flat, literal, no poetry, no interpretation."; the by-name is "where the poetry is allowed to live."
- R8-23: "Art, then technique, then form." R70-74 adds numbered forms at the form level, "mastery reads as forms held".
- R8-24: a release is an optional imperative call; "Speaking it costs a beat and buys a measurable increase in output." R71-29 and R50-09 lift the once-per-scene limit (R8-26-ONE_RELEASE_PER_SCENE superseded).
- R8-25 and R50-14: "New names are for new arts only."; a stronger form takes a suffix "(Kurosetsu becomes Kurosetsu-Kai)".
- R8-26: "Nobody translates their own technique aloud. Ever."; a working that needs its meaning glossed has failed. R49-48 and R50-08: names and translations "free in narration".
- R50-10: "plain English names for common-tongue fighters, true names for houses with a register". R50-11: new English names "two words at most, no stacked modifiers"; R70-74 limits that cap to English. R50-12: "New Latinate names use real, correct Latin." R50-01: borrowed names in correct real grammar. R50-31: romanised only, no script. R50-24: a school takes a true name in the founding culture's tongue. R10-2: Category names stay workbook and Codex line by default.
- People: five strata, stratum follows institution (R23-2, R23-3); outliers free (R50-18); pronunciation line on every card (R50-34); Third Names coined by NPCs stick "only if Isaac keeps it" (R50-21); a dominant Third Name consumes name and rank (R20-5).

**Open.**
- **Chantcraft.** R20C-41 (live): "Chantcraft is the fifth craft, Ars Cantus its medium-home. Not folded." NATALIE.md: "Chantcraft is a delivery of Spellcraft, not a fifth craft." R71-39's note says R20C-41 "is not reached". The Craft field on every chanted technique depends on which holds.
- **Numbered forms in practice.** R70-74 licenses them; nothing says how many forms an art runs, whether each form is its own field entry, or whether a form is learned, unlocked by Stage or bought with points.
- **A fused technique's name.** R71-39 only says the naming law stands. Whose tongue names a Synergia technique shared across two registers is unset.
- **Release and vow together.** The release buys output for a beat (R8-24); a vow buys output by narrowing (R71-32). Whether they stack is unset.

## 5. How a technique and a sheet reach the page

Settled by R70 and R71 (§0), plus R70-71 (rules planted before the fight), R70-73 (one display beat per practitioner), R20C-33 (Pair unlocks named in diagnostic voice) and R20C-49 (gloss rights as a card field). Nothing to ask.

## 6. Traits

**Settled.**
- R17-5-TRAIT_SCOPE: "A Trait that reads he is harder to kill is not a Trait." A Trait names the Lattice property it alters, so which injuries behave differently and which identically.
- Canon (`wiki/The Magic System/The Trait System Law, Function and the Forge.md`, FOW Part Twenty): "A Trait is survived into existence, never taught." It belongs to the soul; awakening "reveals and arms" Traits already present; Class Ø (unwoken) people carry them, and the Weathering hardens them along use. "a Trait edits the body's baseline rather than adding an effect to it". Four Reflections: Primary (Innate), Secondary (Tempered, forged by trauma, revelation, exposure or a choice), Inherited (Lineage), Passive (Resonant), plus Compound and Higher-Imprint Traits. Four offices: Bias, Permission ("A Signature Technique is by definition a working that only one person's Trait architecture permits."), Nucleation at a Threshold, Ceiling.
- R70-84: a readout names a new Trait "when it registers". R71-37: "Narration names the Trait the first time it fires in a scene, then shows it working." R10-3-TRAITUS_SHAPE: a passive, condition-gated visible mark.

**Open.**
- **How a new Trait is gained in play.** Canon gives the causes (trauma, revelation, exposure, a decisive choice) but no rule says when the table grants one, who decides (Isaac for his PC, Natalie for NPCs?), how often, or whether a Trait waits for a Threshold.
- **The Trait entry format.** R47-2 covers abilities; nothing sets a field format for a Trait (Reflection type, Lattice property, bodily signature, trigger, debt after firing, failure state). Cards write Traits as one line each.
- **Shear Break on the card.** Canon makes it "The standing failure mode of a broken vow" and the most common death for a man who changed his mind about who he is. Nothing says whether a card names each Trait's founding truth, so the break is findable.

## 7. Vows, Resonant Pairs and Synergia (R71)

**Vows.** R71-32-VOWS_LIMITS: "A vow that narrows a technique raises its output through Attraction Force, by a figure you set on that card; breaking it is a Shear Break. The vow's terms are its findable counter." Notes: "a vow whose card carries no figure buys nothing yet"; the disclosure option (telling the opponent as a binding) was not taken. Canon beside it: oath XP in FOW Part Two ("An oath that costs nothing earns nothing."); the Votia Category; Mu-jin's carded vows (R68-5, R68-12); broken vows as corruption signs (R61-85).
- **Open:** the size of the figure (a share of output, a Grade step, a fixed multiplier?) and whether there is a scale Isaac ratifies once or a figure per card; what counts as narrowing (target, time, range, a condition on the user, a cost taken on); whether a vow can be added to an existing technique mid-story; whether NPCs vow as freely as PCs; how a vow relates to the Votia Category and to oath XP; where a vow sits on the card.

**Resonant Pairs.** Canon (FOW Part Nine): "These Resonant Pairs generate passive structural bonuses neither stat could produce in isolation." Eight pairs are tabled (Fortitude and Integrity at A to Continuity and Longevity at A, with Reactive Cast, Seam Sight and Sovereign Frequency among the unlocks). R71-38: "Where a Sub-Stat sits at its Stage's cap, strain may lift it level with its partner, and the Pair runs for the crisis, then goes." R39-4 sets the strain-only zone.
- **Open:** whether new Pairs may be designed beyond the eight (R18-2 would demand a demonstrated absence); whether a reached Pair is a card field with its own entry; whether reaching one earns a readout (R70-84 lists four growth moments, not this).

**Synergia.** R71-39: "Allies chain by default; a fusion exists only as a carded Synergia technique the pair learned together, with its own cost split and counter. No improvised fusion." Canon Lexicon: "Synergia field is several Soul Crystals briefly sharing one Essence Core, Shell, and Layer" and requires Attraction Layer compatibility.
- **Open:** how a pair learns one (training time, a shared crisis, a Threshold?); how the cost split is set; whose card holds it (both, or a shared entry); whether Isaac's PC may hold one with an NPC Natalie voices, given that Natalie never acts for the PC; whether three or more may share one.

## 8. The character card: sections, fields, length

**Settled.**
- NATALIE.md: "seventeen sections, Identity through Fracture Log, under 16,348 characters." The 16,348 figure is the Trello card limit (`character-sheet.md`); no rule row in `rules/` carries it.
- R14-8-CHARACTER_SHEET_FOW_LINE: sections "Unchanged"; Techniques gains the FOW line.
- Fields added by ruling: As Of line (R58-12) and headers "at a stated moment" with later events in Lore (R54-11); pronunciation line (R50-34); full voice block with fixed slots "notices first, sentence length, contractions, pet word, never says, stumbles or not, stress shift, grief shift, joy shift, one sample line" (R52-03); gloss rights (R20C-49); combat grammar (R71-69); Readiness (R71-28); vow figures (R71-32); comic voice or double act named on the card (R70-113); the alchemist's "reads first" line (R71-72); voice fingerprint and casting entry for full cards (R61-61).
- Isaac's play beats the card for his PC and the card is updated (R52-08); Sonzai and the other creators' characters get "a record card, not a character card" with no voice or interiority (R20C-16).
- `character-sheet.md`: the published card "carries the figures as settled text: no 'originated', 'pending ruling', estimator, author or process note, ever."

**Open.**
- **Three skeletons.** `SHEET_SECTIONS` in `build/mcp_server.py` has fourteen headings with merged numerals and calls III "Work Architecture"; `character-sheet.md` lists seventeen, III "Wellspring Harmonizations"; Cozbi's card (the named format reference) merges further and adds Voice and Lore; Orin Farrant's runs all seventeen apart. Which is the template, and where each ruled field (As Of, Say it, voice block, gloss rights, grammar, Readiness, vows, Third Name, Lore) sits, is unset.
- **The length cap against the cards.** By file size, about 56 of the 284 Volume I cards exceed 16,348; Cozbi's runs 25,406 bytes and Orin Farrant's 16,582. Lore sections, voice blocks and full field-format techniques all add length. Whether the cap holds (and Lore or technique entries move off the card), rises, or applies only to the stat top is the question.
- **Pressure suppression profile.** `character-sheet.md` lists it as a card field "(docket; pitch one, label it)"; its source, R7-7-PRESSURE_PROFILES_OPEN ("Who can hide, who cannot, and who stopped bothering"), died with Pack Seven unruled, and no docket row exists. R71-43 rules how suppression shows, not who can do it.
- **Estimates on a published card.** `convert_character` tells the writer to put "pending Isaac" in the card; `create_character` says "anything estimated is marked pending in the card"; `character-sheet.md` forbids any such note; R14-2-ESTIMATE_MARKING keeps estimates "in the author notes"; R70-99 lets a readout print a hedged range. Cozbi's card prints constructed stats with a visible flag. Whether a card may print a hedged range, and how, is a real question; the tool text is stale either way (§12).

## 9. NPCs: roster entry, card, record card

**Settled.**
- `wotr-npc`: seven mandatory fields (Want, Refusal line, Knows, Lie, Voice, Body, Line), one italic thought, a first-sight paragraph under 200 words; minor NPCs get one stroke on the page, major ones the full inventory (R70-54); the roster keeps the full Body field either way. `npc_set` commits, so on Isaac's word.
- R52-29: each NPC voice starts from "a researched real-world speaker type"; R52-31 and R70-113: a minor NPC may be comic from the start. R50-27: a person is "a role (the gate-clerk) until they speak twice or matter"; R70-130: a walk-on's comic name lives in another's mouth.
- Case rulings set the tier one person at a time: R61-16 Furveus and R61-23 Cassian Ault get roster entries (Furveus with a FOW line); R61-17 Gillus De Raits gets "A full card with a FOW (Fracture of Worlds) loadout, costs, counters and a Voice block"; R61-61 the Papers' author a full card plus fingerprint and casting.

**Open.**
- **The graduation rule.** No general rule says when a roster NPC becomes a full card (scenes appeared in, a fight, a technique used on the page, Isaac's interest), or when a roster entry needs a FOW line at all (`wotr-npc` field 7 allows "no line").
- **NPC techniques.** Whether a roster NPC's technique needs a field-format entry before it reaches a fight, or a one-line summary card does (ties to §1 and R71-8's planted way out).
- **NPC progression.** NPCs who survive arcs: whether they gain Levels and Traits on the same XP law as the PC, on a Front clock, or only by Natalie's notes.

## 10. Numbers, precedence and the stat line

**Settled.**
- R12-5: "Never invent a number. Unchanged and absolute." R14-2-ESTIMATE_MARKING: an unsheeted value goes in the notes "as an estimate inside the documented range for that Stage and Band, and marked as such". R14-E (ruled 2026-09-12): an estimate becomes canon "Only if that estimate is fully confirmed."
- R39-1: "points are spent on Sub-Stats only"; a Primary is the sum of its eight, its Grade the mean. R39-4: the Stage's Max Grade letter caps a Sub-Stat; above it is the strain-only zone. R38-2: lifetime pool about 18,100 through Stage XIII. R56-4: a Level past its Band gate stands as an outlier with Residual Strain. R47-7 and R70-82: Tiers of Standing by name only.
- R14-8: workbook and card disagreements are "flagged, not resolved".

**Open.**
- **Three precedence orders.** R14-2-LOADOUT_MANDATE: "From the character sheet, the Stat Sheet workbook, or the Notion card, in that order of preference". R20C-32: "Precedence: Fracture of Worlds, then the Stat Sheet workbook, then the Notion card. The card is a rendering and it drifts." `wotr-stat-line` puts `fow_line` (which reads the card) first and the workbook second. The workbook is not in the repo, so in practice the card governs.
- **C-157:** the in-world Apprentice's Primer gives a lifetime pool near 24,100 over twenty stats; R38-2 gives about 18,100 over sixty-three Sub-Stats. Whether the Primer is corrected or read as an old in-world text is open.

## 11. Progression arcs

**Settled.**
- R20C-43: "Progression follows the sixteen Temperance Stages." Canon: "Level counts pressure." and "Stage counts reorganisation."; Band gates at Stages IV, VII, X and XII; Residual Strain at a gate.
- FOW Part Two sets XP by event: repetition decays to ten percent by the fifth engagement ("The Crystal rewards the new sentence, not the repeated word."); zero-risk fighting earns "thirty percent"; Wellspring contact, Gnosis events and oaths pay; Threshold completion is "The largest single XP event available."
- R70-84, R70-90 to R70-92, R70-98 and R70-18 (§0); R71-35 Crisis Recovery decides a fight only if planted.

**Open.**
- **Training yield.** R70-90 lets named training move numbers; nothing says what a week or a season buys, and no number may be invented. The table questionnaire owns how downtime is paced; this one owns the rate.
- **Pace and Level ranges.** C-117: The Sixteen Stages prints a fixed Level span per Stage, while Part Twenty-Three calls the span typical and holds only the Band gate hard. C-121: Mu-jin's own reading puts him near Level 285 a year before his card's Level 430 and Stage XII. No rule says how fast a character may climb, or how many Levels a session or an arc may yield.
- **Who designs a Catalyst.** For Isaac's PC, whether Natalie proposes the Catalyst a Stage requires, Isaac names it, or the world supplies it unseen; for NPCs, whether a Catalyst is planned on a Front.
- **Point allocation at a Level.** Isaac allocates his PC's Sub-Stat points (R47-10 lets anyone allocate into the strain band "at a stated risk"); nothing says whether Natalie allocates NPC points or derives them from what the NPC did.
- **Technique growth.** Whether techniques improve by numbered forms (R70-74), escalation suffixes (R50-14), Grade and Stage floors met, vows, or all of these, and whether a new technique needs a Trait (canon's Permission office) or only a Stage floor.
- **Ledger of gains.** R70-98 lists changes per chapter; no rule says where a PC's growth history lives between the card's Temperance Record and the Ledger.

## 12. Stale text: fix, do not ask

- `convert_character`: "summary card + Design Chain" (R47-2 retired it); "'pending Isaac' in the card" (clashes with `character-sheet.md` and Isaac's direction that he makes the calls); "Coherence Band" (R43-4). `create_character`: "marked pending in the card". `SHEET_SECTIONS` II and X: Coherence Band, Design Chain.
- `technique-design.md`: "Nothing in narration on its own authority" predates R70-83.
- R14-7's quote still lists "Coherence Band"; R43-4 governs.
- Cozbi's header prints "Tier of Standing 8, Archmaster"; R47-7 and R70-82 keep the Tier by name.
- C-159 still reads open; R71-29 closes it. R7-7-VOW_CLAUSE_OPEN, noted as orphaned, is answered by R71-32.

## 13. The gaps in brief (candidate questions)

Card: technique as full entry, summary or link; Signature against minor; one template and where the ruled fields sit; the 16,348 cap; hedged estimates on a card; suppression profiles. Abilities: Chantcraft; numbered forms; release and vow stacking; the vow scale and NPC vows; new Traits and a Trait format; new Resonant Pairs; how Synergia is learned and split. People: roster to card graduation; NPC technique depth and growth; precedence and the missing workbook. Progression: training yield, climb pace, Catalyst authorship, NPC point allocation, technique growth routes; how far Natalie fills a PC's technique. Debts: cost audit order, the Family chart, the Bank's home.

## Boundaries with the other questionnaires

Table keeps NPC behaviour and downtime pacing; this one keeps card content, ability design, progression mechanics and NPC card fields (the line `table-questionnaire/work/research-law.md` draws). Mystery keeps clue and lie craft; Intimacy keeps explicit scenes.
