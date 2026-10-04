# Combat law map, for the combat questionnaire (2026-10-04)

What the rule index says today about combat, magical combat, items and firearms, alchemy in scenes, and adjudication, so the questionnaire asks only what is open. Every quote below is an exact substring of the row's `verbatim` (or, where marked "summary", of its `summary` field, because the verbatim is only a header line). Status is the row's `status` in `rules/*.yaml` on 2026-10-04.

**Sources read.** `rules/doc-style-law-2026-10-03.yaml` (R70, combat-facing rows), `doc-combat-society-politics-law-2026-09-26.yaml` (R60), `doc-ability-law-2026-09-26.yaml` (R47), `pack-11` to `pack-14`, `pack-20`, `doc-item-tiers.yaml` (R46), `doc-shot-and-enhanced-weapons.yaml` (R45), `doc-world-texture-law` (R53), `doc-writing-law` (R48), `doc-prose-law` (R49), `doc-vocabulary-law` (R51), `doc-naming-law` (R50), `doc-queue-questionnaire` (R54), `doc-system-accounts-questionnaire` (R55), `doc-magic-docket` (R56), `doc-backfill-rulings` (R57), `doc-era-apparatus-law` (R59), the alchemy rows R61 to R69, `CONFLICTS.md`, `proposals/PROPOSED.md`, `out/docket.md`, the Combat Craft Guide 2026-10-03 edition (`desktop/`), the Mass Combat Craft Guide 2026-10-03 edition and the Item and Equipment Writing Guide 2026-09-12 reconstruction (`~/wotr-vault/true-canon/`), the Manual Verification Guide 2026-09-26 edition, `build/verify.py`, and `imports/drafts/style-questionnaire/decisions.md`.

## Plain glossary (first use)

- **HEMA**: Historical European Martial Arts, the reconstructed medieval and Renaissance fencing manuals (Liechtenauer's German longsword, Fiore's Italian Armizare). The Western school's vocabulary.
- **Measure**: the distance at which a blow can land. **Tempo**: who acts first. **Vor / Nach / Indes**: German fencing words for "before" (taking the initiative), "after" (answering), and "in the instant" (acting inside the other man's action). **The bind**: blades in contact, each fighter feeling the other's pressure through the steel.
- **ATLS class**: the Advanced Trauma Life Support haemorrhage scale, Class I to IV by share of blood volume lost; Class II brings anxiety and a fast pulse, Class III confusion, Class IV collapse.
- **EU / AU/s / η**: Essence Units (the reserve; 1 EU = 1 MJ), Aether Units per second (the draw rate; 1 AU/s = 1 MW), and eta, conversion efficiency.
- **Starvation**: Essence Starvation, the state below ten percent of a practitioner's own reserve, where stats read a Grade lower and Traits flicker.
- **Pressure**: the felt weight of a higher-Stage practitioner's presence. **Dominion**: the Primary Stat that governs it. **Passive Pressure Field (PPF)**: its radius.
- **Draft / Draftcraft**: an alchemical preparation, and the Craft (mode of delivery) that pours rather than speaks, cuts or writes. **Mortalis**: the Wellspring of death-work and the Crossing. **The Crossing**: the nine-day passage of a dead body's residue back to the Wellsprings. **Impression-body**: a summoned likeness built on a dead person's Volitional Trace (an unfinished decision left in the ground). **Stillgate Ash**: the grounding material that lets a stalled body complete its passage.
- **Display beat**: the licensed moment of visible power (a Stage ascension, a Pressure drop, a technique's first display or finisher). **Readout**: a set of figures on the page, from an instrument, a surgeon, or the bearer's own Crystal.

## Three things to know before the dimensions

1. **The docket is empty for these tags.** `book_tools.py check_docket combat magic-mechanism adjudication items mass-combat` returns "0 pending/proposed", and `out/docket.md` reads "0 outstanding." The five `proposed` entries in `proposals/PROPOSED.md` (2026-09-28: Edmund's Sort, the Visitation, muster camps, [Ir] Continuum, Accord Inventory entries) touch none of these tags. Open matter lives in CONFLICTS.md, in rows the style law flagged but never logged, and in debts the guides carry.
2. **Pack status.** Packs Eleven and Twelve carry no ratification line (`ratified: None`) but every row is `live`, as NATALIE.md's caveat says. Packs Thirteen and Fourteen are ratified ("Isaac, 2026-09-11 ... ratified by direction"); NATALIE.md still says the index records them as proposed, which is stale.
3. **The companion guides lag the law in five places** (housekeeping, not questions; the later rows are law and must not be re-asked):
   - The Combat Craft Guide 2026-10-03 edition left §2 and §4 "word for word" because no R70 answer reached them, so it still quotes three rows that were **superseded on arrival** on 2026-09-13 and one ban superseded on 2026-09-26: R20C-26 ("The steel stops the shot, always") at §2 and §4.4, against the live R13-C ruling that the working stops shot; R20C-24 (Joules only in a Measurewright's or Guild officer's mouth) at §6 and §8, against the R13-A ruling that anyone in diagnostic voice may; R20C-27 (gap-fill never changes an outcome) at §9, against the R13-D ruling that it may and says so; and the firearm prose ban (R11-3-FIREARM_PROSE_LAW, `superseded`) at §2 and §4.4, against R53-05. It cites none of R45, R46, R53-03, R53-04, R53-05 or R13-C.
   - The Item and Equipment Writing Guide is the 2026-09-12 reconstruction: it teaches the firearm ban as live (§5, §10) and predates R45 (shot and dodging), R46 (item Tiers), R47 (ability law) and R53 (firearm ceiling, enhanced shot).
   - NATALIE.md's Magic Frame still says "no sentence explains why a proofed round beats proofed plate (C-001)" and "names only in a mouth, an instrument, a document, or a private count"; both are superseded (R53-05; R49-47, R70-83).
   - CONFLICTS.md C-001's status text and R12-1-EXPLAIN_BAN_STRUCK's note still read "Eleven's ban stands"; R53-05 (2026-09-26) lists R11-3-FIREARM_PROSE_LAW in its `supersedes`.
   - The Mass Combat Craft Guide never mentions a firearm, a volley or a gun (a search for musket, rifle, volley, artillery, cannon, gun, powder and shot finds nothing about arms), although the Draw Age runs 1800s hardware (R53-01, R53-03, R59-12).

---

## 1. Exchange tracing and the combat floor

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| R48-33-CHOREOGRAPHY | "Duels: every exchange traced (measure, guard and the move by its fencing name)." | live; amended by R70-100 (the name is the POV's school's) and R70-102 (shape by grammar) |
| R12-3-COMBAT_EXCHANGE_OWES | summary: "the read (evidence named), the fault (structural weakness), the counter and why it works (causal), the cost in body and reserve (both), and what the character cannot do next" | live (Pack Twelve, no ratification line) |
| R13-4-COMBAT_FLOOR | "Every meaningful exchange (a hit that lands, a first display, a counter, a change of measure that decides something) puts the following on the page"; summary lists eight items: measure, tempo (Vor/Nach/Indes), the named read, the fault, the mechanics of the hit, injury by structure with ATLS class, the Essence account at three strata, what he cannot do next | live |
| R13-4-DENSITY_BUDGET | "A duel of 2,500 words carries the full floor at first display and finisher, and items 1 to 4 at every exchange that changes the fight. A turn of 700 to 1,500 carries 1 to 4 once and 8 at close." | live |
| R13-4-THREE_EXPLANATIONS | "Physics, Essence, Hermetic correspondence: at first display and finisher each is a causal sentence beside its image" | live |
| R48-20-STRATA | "The three-layer account (Aether, Wellspring, Essence) shows at a working's first display and at the finisher; lighter touches between." | live |
| R12-8-COMBAT_GUIDE_READ_LENGTH | "The read is now shown at length, no longer summarised." | live |
| R13-8-RECONSTRUCTIBLE_ADJUDICATION | "A fight that resolves because the scene needed it to has failed the pack and is rewritten." | live |
| R49-43-EXPLAINING | "Narration may explain causes anywhere, in the POV's reasoning and vocabulary" | live |
| R51-17-MID_ACTION | "mechanism terms may be bare mid-action; the reader keeps up." | live |
| R48-06-RHYTHM_LAW | "the hit is the shortest sentence and sits last" | live; R70-19 frees one cumulative climax per set piece |
| R70-15-TEMPO_STILLNESS (SP2) | "Jo-ha-kyū tempo. Set pieces and long scenes run slow, breaking, swift" | live |
| R70-57 (DD6) | "Held instant, then outcome." | live |
| R70-71 (MY4) | "A working's rules are planted earlier (training, a document, talk), so the fight's explaining is mostly recall" | live |
| R12-3-NAMED_INVENTOR_RULE | "A self-derived technique must be read live, in the two or three exchanges before it kills you" | live |
| R13-7-RESEARCH_RULE | "A set piece written from memory is a failed set piece." | live |
| R13-5-GAP_FILL_PASS + R13-D ruling | ruling note: "the gap-fill pass may change an outcome Isaac wrote when no cause fits, and says so in the author notes" | live (R13-D row closed by ruling; R20C-27 superseded on arrival) |
| R47-11-TIME_AND_ENERGY | "One combat turn is six seconds." | live |

**Open for the questionnaire**

- **The density budget is keyed to retired lengths.** R13-4-DENSITY_BUDGET counts a 2,500-word duel and a 700 to 1,500 word turn; turns now run about 3,500 words (R48-28) and set pieces 5,000+ (R48-46), and R1-3-WORD_FLOOR_INCLUDES_AFTERMATH still says "The 2,500-word minimum". How the floor scales at the new lengths is unruled.
- **The floor in a roleplay turn where Isaac's PC acts.** Item 3 (the read) and item 8 (what he cannot do next) are interior to the fighter. Which of the eight items Natalie states for Isaac's PC's own exchange, and which she leaves to his post, is unruled. (R49-01-WHOSE_HEAD lets narration go deep inside his character with his overrule; NATALIE.md says never think for him.)
- **Exchanges per turn.** Table Rule 1 says never resolve a multi-decision action in one go, and a turn is six seconds (R47-11); how many six-second turns a ~3,500-word roleplay turn may cover in a fight is unruled.
- **A duel between two grammars** (Verdict against Blade, say): R70-102 is silent, and the Combat Guide says so rather than settle it.

## 2. Combat grammars

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| R1-1-THREE_VOCABULARIES_RULING, extended by R3-7-EXPENDITURE_GRAMMAR | "Assign the vocabulary before assigning the technique."; "Expenditure grammar hunts cost." | live (four grammars: Blade, Verdict, Percussion, Expenditure) |
| R1-1-VERDICT_GRAMMAR | "The prose skeleton is read, rank, commit, and the tension lives in the read rather than in the exchange." | live |
| R1-1-PERCUSSION_VS_BLADE | "Blade grammar hunts openings. Percussion grammar hunts fatigue." | live |
| R1-1-PERCUSSION_MOVES, R3-7-EXPENDITURE_MOVES | the Settling, the Sweep, the Shove, the Return; the Offering, the Standing, the Ledger, the Absence | live |
| R70-102 (CB3) | "Verdict still then one cut, Blade traced passes, Percussion and Expenditure by attrition; practitioners escalate while reserve lasts. R60-01 holds for the unranked." | live |
| R70-100 (CB1) | "Narration names every move in the POV's own training"; "a foreign school's word arrives in a mouth." | live |
| R70-74 (MY9) | "A school's art may run as numbered forms (First Form, Second Form), each named, called and counted" | live |
| R13-6-HEMA_VOCAB | "HEMA, extended past the longsword: spear and staff, poleaxe, dagger and the grappling plays, messer, sword and buckler, mounted lance. A percussion master-strike table built for the hammer, not borrowed." | live |
| R20C-25-PERCUSSION_TABLE_DAWI_AUTHORED | "The Percussion master-strike table is Dawi-authored in-world." | live |
| Assignments | R1-1-SODOKU_ASSIGNED (Isaac's PC; canonical, not to be touched), R1-1-RASHANI, R1-1-RENGAI, R1-1-DOUGOU, R3-7-COZBI, R1-1-YOKO, R1-1-BLACK_AGENT, R4-H1-WREN, R4-H2-EDWARD_LAMBERT; R20C-54 confirms | all live |
| R1-1-RESTRICTED_CHARACTERS_EXCLUDED | "Restricted characters (Ma'Kovu, Fushigi, Haruki, Xhem, Dova'Kan, Gorgi) are excluded entirely" | live |

**Open for the questionnaire**

- **The rest of the cast has no grammar.** R20C-54: "Remaining assignments run with Combat Guide 3e." Nine are assigned; named NPCs on the wiki with no assignment include Renard Greymane, Lorn Stark, Hild Ice, Tōga, Borin Ironheart, Kwon Mu-jin, Hiromi Mahuo (whose Juggernaut's Fist is ruled, R57-03), Malphas. Never Sodoku or the six restricted characters.
- **The Percussion master-strike table** is owed (R13-6) and its in-world author fixed (Dawi, R20C-25); its contents are unwritten.
- **Schools beyond five.** verify carries school lists for blade (HEMA), japanese, chinese, korean and percussion; R70-100 asks for the POV's own school in every culture. Kharven riders, the Dawi, Accord drill, the Zettari, Eresse and the hunting companies have no school vocabulary. Whether each culture gets one, and from which real tradition, is open.
- **A fifth grammar?** Firearms, archery, grappling, area casting and Domain fighting have no grammar of their own; whether one is wanted (a marksman's or a field-caster's grammar) is open.

## 3. Adjudication and the stats that decide

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| R14-3-STATS_DECIDE_TABLE | "This pack names which stat answers each of those, so the adjudication is reconstructible" (the ten-row table is held as reference data, not row by row) | live |
| R14-3-TRACEABILITY | "Every outcome in a fight traces to a row in this table, and the author notes say which." | live |
| R14-2-LOADOUT_MANDATE / R14-2-ESTIMATE_MARKING | "Natalie loads that character's Fracture of Worlds line"; "It is never invented to feel right." | live |
| R12-5-NEVER_INVENT_NUMBER | "Never invent a number. Unchanged and absolute." | live |
| R14-7-STAT_LEDGER_CONTENTS | Stage, Band, Coherence Band, Aether Class, Crystal State in and out; the row each outcome traced to; EU spent (summary) | live |
| R60-01-BRUTAL_LETHALITY | "most fights end in the first seconds; a wounded man is out of the fight." | live |
| R60-03-HARD_RESERVE_CLOCK | "long fights are won by whoever manages the reserve; Starvation hits mid-fight on overspend." | live |
| R57-10-NEVER_RIGGED | "every engagement is built to be fun and a genuine challenge for the PC, never rigged in either direction." | live |
| R48-36-NPC_WITS | "NPCs are veteran-clever with their abilities: use what they could know and have trained, well; never omniscient, never dumb." | live; relaxed by R70-112 before a public reversal |
| R48-35-USES | "each side invents its own; Isaac for his characters, the partner for NPCs within the page's facts." | live |
| R48-31-STAKES / R48-30-SURPRISES | "Death can happen, if earned"; "Big surprises (betrayal, ambush, death) only after foreshadowing a player could have caught." | live |
| R47-3-COUNTERS_AS_FACTS / R17-3-COUNTER_MANDATORY | "Players work out the tactic."; "If the counter is hit him harder, the technique has no mechanism." | live |
| R47-9-INHERITED_FAILURES | "Every working inherits the documented failures of every Wellspring it draws on, and opponents can induce them." | live |
| R45-1-SPEED_DECIDES_THE_DODGE | "Dodging is read off the target's Speed Grade ... and surviving a hit off their Resilience Grade." | live |
| R55-7 / R55-8 | "anyone at the caster's Stage or higher is immune"; "Area workings sort friend from foe by the caster's judgement/attention" | live |
| R54-8, R54-9, R56-1, R56-2 | force "unmeasured" from Zenith up; card Strike Force outliers stand | live |
| R39-1, R39-4, R44-1 | points buy Sub-Stats; Max Grade letter binds; "1 EU = 1 MJ stands." | live |
| R70-79 (LR2) | "Any practitioner feels his own Grades and Stage, and another's Band and rough Stage, with Gnosis setting how close." | live |
| R70-88 (LR11) | "Grades at the read." "no running figures." | live |
| R70-104 (CB5), R70-112 (DL6) | rivals recur only by a mercy paid on the Ledger; the face-slap "with a bill" | live |
| R13-6-SCALING_VOCAB_RESTRICTED | "Scaling vocabulary, author-notes and adjudication only, never on the page" | live |

**Open for the questionnaire**

- **The unwoken against the ranked** (three open conflicts, all live CONFLICTS rows): C-122, the Hollow Grade's strike energy is "below 60 J" in the living pages and "40 to 300 J" in the source table; C-123, Class Ø caps output at Hollow while the Weathering's grain "outperforms a practitioner three Stages up"; C-124, Pressure counts in Stages and the unwoken have none. Together they leave no rule for how an unwoken fighter (Orin Farrant, a commoner with grain) fares against a practitioner.
- **The environment row.** Table Rule 5 names "what the environment allows", and the table's only environment row is Aetheric Density for the draw. Terrain, footing, cold, light and weather have one ruled instance (R54-16, Stone-Blood "about three-quarters of a beat late" in deep cold) and no general row.
- **Near-equal contests without dice.** Nothing says what decides when the rows come out level: the read, the reserve, the POV's side, or a stated tiebreak.
- **One against many.** The table assumes one opponent; several attackers on one fighter (below a formation) is unruled.
- **Wound penalties in later fights.** R60-02 rules healing times; whether a carried wound lowers a Grade or a Sub-Stat in the next fight, and by how much, is unruled.

## 4. Pressure

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| NATALIE.md Magic Frame (standing prompt, not a row) | "One Stage up bends attention; two, sweat and nausea; three or more drops people; a Band gap changes weather." "Suppression is a tiring skill." | standing |
| R12-1-PACK_SEVEN_SURVIVORS | "higher is still felt before it is seen." | live |
| R70-69 (MY2) | "Pressure shows first in the room: smoke, frost, lamp flames, the draw-hum, animals; bodies follow." | live |
| R70-70 (MY3) | "Killing intent becomes Pressure narrowed onto one man through Dominion ... It needs a ruled mechanism before first use." | live (mechanism owed) |
| R53-14-FOLK_KNOWLEDGE | "Pressure is felt as dread" | live |
| R70-85 (LR8) | "Not taken: Pressure." (no readout at Pressure) | live |
| R9-3-SCOPE / R9-3-BODY_UNDER_LOAD / R9-3-SILHOUETTE_ENTRANCE / R9-3-AURA_AS_FRACTURE | a Pressure drop is a display trigger; the body under load; the backlit arrival; discharge as "broken geometry around the body", and It glowed "stays banned" | live |
| R56-12-AUTHORITY_RADIUS_IS_PPF | "the Passive Pressure Field is the authority radius at reference density" | live |
| R70-35 (VB12) | bans "'killing intent surged'" in narration | live |

**Open for the questionnaire**

- **The killing-intent mechanism** (R70-70 says it needs one before first use; the Combat Guide's Appendix A carries it as owed; until ruled it stays off the page).
- **Pressure on the unwoken** (C-124, open).
- **Pressure on a formation.** Pack Seven's pressure-in-the-press exception (a line that breaks before contact because of what it felt) is superseded and "no live rule naming this guide replaces it" (Mass Combat Guide §11).
- **Suppression's cost** (what it spends: reserve, Tempering, attention) has no row.
- **Several practitioners at once**: whether Pressure stacks, and what happens at zero gap, is unruled.

## 5. Magic in a fight: voices, readouts, display beats, named techniques

**Settled: the voices and the register**

| Rule | Exact words | Status |
|---|---|---|
| R12-4-VOICE_MIXING_RULE | "Four carriers. Pick per scene. Do not run more than two in one engagement." | live |
| R12-4-VOICE_ONE_POV | "A wrong technical explanation delivered confidently is now the most valuable tool in the kit" | live |
| R12-4-VOICE_TWO_SECOND / THREE_OPPONENT / FOUR_DOCUMENT | "The Kakashi model."; "Contempt as instruction."; "Sets a rule the scene then breaks." | live |
| R12-2-TECHNICAL_REGISTER_DEF, rewritten by R70-9 (K9) | "It explains the read, the fault, the counter, the reserve, and the reason the answer worked."; "the Technical register draws on LitRPG and wuxia (numbers, named forms, the read)" | live |
| R70-3 (K3) | "Western leads combat, injury and dialogue; LitRPG leads progression." | live |
| R13-2-THREE_STRATA_MANDATE, R13-2-CATEGORY_ACROSS_STRATA | three strata; the alignment tag "names which Plane carries the cost and which Plane the counterplay lives on." | live |
| R13-3-PHENOMENON_MANDATE | the real phenomenon, Physics Domain, Wellspring, Category, Mechanism Vocabulary term and the fault, named in the notes (summary) | live |
| R13-6-ANIME_GRAMMAR_TRANSLATION_AID | "Anime grammar as a translation aid, never as page vocabulary." | live |
| R47-8-WASTE_IS_HEAT, R48-37-COST_SHOWN, R57-24 | "A working's wasted energy radiates as heat at the caster's Shell"; "tremor, heat off the skin, thirst, a Crystal ache"; "the aftermath is the tell" | live |
| R55-1, R55-2 | substance costs "permanent and cumulative"; Overchannel "damage accumulates" | live |
| R20C-35, R20C-42 | "A practitioner chants in their own language."; Law V: below Refraction "a working needs voice, hand, ink or blood." | live |
| R10-3-PROJECTED_FORM_LICENSE / R10-3-CRAFT_DURABILITY_TABLE | workings may render as an externalised shape; "The delivering craft sets how much the shape can be trusted to hold" | live |

**Settled: readouts in a fight (all style law, 2026-10-03)**

R70-2 (K2) "Full LitRPG, screens."; R70-78 (LR22) the bearer reads "his own sheet only, exact, and blind to wounds and to others"; R70-80 (LR3) "Figures inline by default; a set-off block only at a re-assay that moves something, a breakthrough or an arc's end."; R70-81 (LR4) "Clinical, wit in margins."; R70-85 (LR8) appraisal, wound, Essence spent; R70-86 (LR9) "Up to three per scene ... a roleplay turn carries two at most, never two in one exchange."; R70-87 (LR10) readouts "never count" against the two-voice cap; R70-88 (LR11) Grades at the read, no running log; R70-89 (LR12) "Body, then number."; R70-91 (LR23) breakthrough "never mid-exchange"; R70-99 (LR21) "Print the estimate, marked."; R70-84 (LR7) Level, Stage, Trait, Wellspring contact; R70-93 (LR15) ranked practitioners "talk his own and others' numbers exactly and argues builds"; R70-17 a scene may close on "A notice or readout".

**Settled: display beats and the duel's set moments**

R70-73 (MY6) "One per practitioner."; R70-72 (MY5) "Spoken chorus, in hearing."; R70-11 (VO2) marked roll call; R70-101 (CB2) "Full declaration, with a price."; R70-103 (CB4) "Full flashback, POV only."; R70-68 (MY1) "The Crystal as inner map."; R70-75 (MY7) "Numbered rite, set apart."; R70-76 (MY8) "Law stated, reasons kept."

**Settled: named techniques**

R8-23-NAME_HIERARCHY "An art is spoken once at release and thereafter assumed. Techniques are spoken every time they are used."; R8-24-RELEASE_MECHANIC "Speaking it costs a beat and buys a measurable increase in output."; R8-26-NO_SELF_TRANSLATION (nobody translates his own technique aloud); R49-48 "Technique names and their translations are free in narration."; R50-10 "plain English names for common-tongue fighters, true names for houses with a register."; R50-11 "two words at most" (English only, per R70-74); R70-74 long hall names "glossed literally".

**Open for the questionnaire**

- **C-159 (open): how many releases.** R8-26-ONE_RELEASE_PER_SCENE "One release per scene at most. Two men releasing in the same scene is an event, not texture." against R50-09-ONE_RELEASE "No limit on release calls: an art may be called as often as the fight gives a beat". Both serve as live. (The style questionnaire listed "Technique names spoken aloud in a fight" as settled before C-159 was logged.)
- **Faculty appraisal of another man's exact figures**: flagged in R70-85's notes "for the conflict log", never logged as a C-row. R70-85 lists "a faculty" among appraisals; R70-79 says "Another's exact figures need an instrument".
- **How a Crystal line shows an estimate**: flagged in R70-78's notes, never logged. The Crystal's lines are "exact"; R70-99 hedges "with the instrument's own hedge", and the Crystal is no instrument.
- **Whether a closing readout, an item card and a chapter-end changes block sit inside R70-80's "only"** (R70-80's notes: "not settled").
- **Domains in a duel.** Every Domain rule is about formations (R2-6-DOMAINS_BREAK_NOT_KILL, Mass Guide §5). A Domain seated against one opponent has no rule for how it is written or adjudicated.
- **Joint workings in a fight** (allies combining; Synergia exists as a Category) have no combat rule.
- **Mid-fight explanation by the opponent** is settled (voice three), but a technique card set off on the page in a fight (R47-1's field format) is not addressed; R70-95's set-off card is for items only.

## 6. Injury, gore and aftermath

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| R48-34-WOUNDS | "full clinical gore, anatomy named, blood loss tracked minute by minute, nothing looked away from." | live |
| R13-6-ANATOMY_VOCAB | "Anatomy by named structure. Fracture types by name. Neurological consequence by name." | live |
| R49-50-OWN_BODY / R70-28 (VB5) | "A trained POV (medical or fighting training) names his own wound exactly; an untrained POV keeps his own body in plain words." | live |
| R70-85 wound readout | "A diagnostic line in a surgeon's terms: the structure struck, the ATLS class, the minutes left." | live |
| R60-02-REAL_HEALING_TIMES | "weeks for a cut, months for bone"; Vitalia "costs the healer EU and the patient's body pays something (scar tissue, fever, hunger)" | live |
| R60-04-DEATH_IS_PERMANENT | "the only exceptions are liches, the undead and their kind." | live |
| R53-10-MEDICINE | "Medicine is era-appropriate by place"; "the north and the poor get folk medicine and the barber." | live |
| R48-38-AFTERMATH | "Every duel ends with a full aftermath beat: wounds dressed, what changed between people." | live |
| R70-105 (CB6) | "Japonic, Korean and Chinese killers carry the rites; the elegiac image belongs to any POV whose culture mourns that way. The clinical floor holds everywhere." | live |
| R54-20, R1-3-FIVE_STAGE_AFTERMATH, R54-15 | duel-level wound anatomy in battles; touch two of the five aftermath stages; a later named scene may pay a battle's aftermath | live |

**Open for the questionnaire**

- **Wounds carried into later fights** (see section 3): no rule turns a Ledger wound into a stat penalty.
- **Regeneration and healing Traits** against R60-02's real timelines: whether a Trait can shorten healing the way Vitalia does, and at what price, is unruled.
- **Combat's psychological aftermath** (shakes, sleeplessness, the killer's first night) beyond R48-38's "what changed between people" has no rule.
- **Prosthetics and amputation** in the Draw Age (R59-11 materials, R53-10 medicine) are unaddressed.

## 7. Items, armour tiers and firearms

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| R11-3-GUNPOWDER_AND_ARMOUR_CONFIRMED | "gunpowder exists. Magical weapons exist. Armour is not dead." | live |
| R11-3-DUAL_ANSWER_SILHOUETTE | "Inside twenty feet a discharged firearm is a club and the sword is the thing that finishes it." | live |
| R11-3-BALLISTICS_RULING | "They open an engagement, they do not decide one." | live |
| R11-5-COMBAT_GUIDE_RANGE_OPENING | "the HEMA grammar takes over inside roughly twenty feet." | live |
| R11-3-PROOF_MARKS_CANON | "A dented cuirass is certified rather than damaged" | live |
| R11-3-AMMO_TIERS + R20C-22 | summary: common shot, proofed shot, the named round; R20C-22: "ratified, subject to R20C-26" | live (R20C-26 itself superseded) |
| R13-C ruling | "The working stops shot against a worked cuirass, not the steel." | live by ruling (C-018 closed for it) |
| R53-03-FIREARM_CEILING | "up to 1900 hardware: repeating rifles, smokeless powder, even early machine guns exist, rare and state-owned." | live |
| R53-04-ENHANCED_SHOT | "Enhanced shot is standard for elites"; "ordinary infantry do not." | live |
| R53-05-PROOF_PLATE | "Narration may state the cause of any penetration outright, in gunfights as anywhere" | live; supersedes R11-3-FIREARM_PROSE_LAW (closes C-001 the other way) |
| R45-1 to R45-5 | dodge by Speed Grade, survive by Resilience; catch needs Travel floor "at least twice the projectile's velocity"; enhancement capped at the enhancer's Grade; "An enhanced round is dodged at its actual velocity"; "paid for per shot and consumed when fired" | live |
| R46-1 to R46-4 | item Tier is "the lower of what its material can hold and the Tier of Standing its maker stood at"; nine named Tiers (Marked/Signatum to Proscribed/Interdictum); "A strike one Tier above the proof breaks it; a strike two Tiers above passes as if it were not there."; "A practitioner can equip themselves but cannot equip an army." | live |
| R47-5, R47-7, R70-82 | Tier rung by name, never number; "Tiers of Standing and item Tiers keep their names alone." | live |
| R13-9-ITEM_GUIDE_WEAPON_ENTRY | "mass, length, point of balance, and the armour tier it beats and fails against." | live |
| R70-95 (LR17), R70-48 (DS12), R70-56 (DD5) | item card once; "Price whenever money moves"; lineage; catalogue at arming and loot | live |
| R59-12-TRANSITIONAL_MILITARY | "khaki, trenches and rare machine guns later; practitioners change everything anyway." | live |
| R53-25 (real object names), R33-1/R33-2 (Witnessed Temper), R34-1 (Moto material culture), R22-4 (Kurosetsu's scabbard) | as written | live |

**Open for the questionnaire**

- **The three ammunition tiers against the nine item Tiers.** Common, proofed and named shot (R11-3) are not placed on R46's ladder, and "Proofed" is also item Tier 2's name (Probatum, D). Whether "proofed shot" and "proofed plate" mean Tier 2, or a Guild stamp at any Tier, is unruled. R20C-22's condition ("subject to R20C-26") points at a dead row.
- **The armour-type ladder against the item Tier.** Padded, mail, brigandine, plate and ceramic (Combat Guide §4) are physics; R46-3 makes an armour's Tier its proof. How the two combine (a Tempered gambeson against plain plate) is unruled; the Item Guide carries it as a flagged gap ("no rule chooses").
- **How a gunfight is written now.** R53-05 lets narration state the cause of a penetration; the old row's texture clauses went with it ("The gun is furniture, not spectacle", rotten-egg powder smell, wet-weather misfires, the soldier's superstition about his weapon). Whether that texture comes back as law, and how much ballistics a gunfight carries, is open.
- **The firearm ceiling against the age.** R53-03 caps firearms at "up to 1900 hardware"; R53-01 runs the Imperial Age's technology into the mid-1900s, and C-158 (open) sets NATALIE.md's 1900 cap against R53-01. Whether 1900 to 1950 small arms (self-loading pistols, light machine guns) exist is open for firearms in particular.
- **Weapons with no rule**: bows and crossbows outside R45/R46's arrows; artillery, rockets and Essence-engine weapons (R59-01 draw-fed engines); bayonets; grenades and alchemical reactives (Sun-Salt, Therphorus, Combat Guide Appendix A); Aether-Sight visors and Auramancy shielding (Appendix A).
- **A firearms school list** for verify does not exist; R70-100 would need one for a marksman POV.

## 8. Mass combat

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| R1-4-PRECEDENCE_NOTE | "The Mass Combat Craft Guide takes precedence the moment a formation exists." | live |
| R70-106 (CB7) | "A battle cuts between the commander's hill and one man in the press at marked breaks, each section POV-locked" | live |
| R70-11 (VO2) | "one line inside each of several heads, then the lock resumes." | live |
| R1-3-NAME_THREE_RULE | "No more than three characters carry interiority through a battle sequence." | live |
| R1-2-THREE_FIELDS_MANDATORY, R1-2-COUNTERPLAY_THREE_WAYS | Frontage, Sustain, Re-form; counterplay is to exceed Frontage, outlast Sustain, or shorten Re-form | live |
| R2-6-CURRENCY_RULE | "An army converts time into ground. These do not exchange."; "no technique holds ground." | live |
| R2-6-DOMAINS_BREAK_NOT_KILL | "A seated Domain does not kill a formation. It corrodes cohesion, the line breaks, and the killing happens in the rout." | live |
| R2-6-VOIDIC_COUNTER, R2-6-SPEED_RULING | Voidic practitioners priced as suppression; "Speed is Essence, couriers are interdicted first" | live |
| R2-5 Single Act rows | "a battle advances exactly one relationship, and it advances it by a single unrepeatable act." | live |
| R1-3-AFTERMATH_IS_WHERE_IT_HAPPENS, R1-3-PLAN_AFTERMATH_FIRST | "plan the aftermath first and the engagement second." | live |
| R3-8 naval, siege, cavalry rows; R3-9 practitioner POV | "the practitioner POV is available before and after an engagement and is closed during it."; costed-out exception "Spend it once." | live |
| R54-17, R54-20, R57-40 | multi-place scene with a mass section measured as a set piece; duel-level wound anatomy; hobgoblin horn count in deep cold | live |
| R70-56, R70-72, R70-101 | catalogues at muster and loot; the chorus in hearing; declarations at the line | live |

**Open for the questionnaire**

- **Gunpowder battle.** The Mass Combat Guide has no volley, no rifle line, no artillery, no square against cavalry, no black-powder smoke, no skirmish screen, though R53-03 and R59-12 put them in the age. This is the largest uncovered area in the combat law.
- **Skirmish scale.** Between a duel and "the moment a formation exists" sit the hunting company, the ambush on a road, the Night Watch raid (R60-06, R60-12, R60-26). Which guide governs five to thirty fighters with no formation is unruled.
- **Which side of the cut a battle opens on**, and **a commander on the hill who is a high-Stage practitioner** (R70-106 gives the hill a POV section; R3-9 closes a practitioner's POV during an engagement): both listed open in the Mass Guide §11.
- **Pressure on a formation** (section 4 above).
- **Sound and smell at sea; riverine actions as distinct from sea; tells for §12 to §15**: carried open in the Mass Guide.
- **Full-layer scarcity against display beats.** The Mass Guide caps full three-layer rendering at "no more than four or five times" a battle; R70-73 allows "a battle several" display beats, one per named practitioner. They likely agree; how they count together is unstated.
- **Well-spawn and beasts against formations** (R53-06, R58-06, R70-18's Well delve) have no mass-combat rule.
- **Unlogged tension found in this pass.** R54-19-MASS_NPC_THOUGHT: "mass-combat scenes keep the one-thought-per-NPC allowance even when POV-locked" against R1-3-NAME_THREE_RULE ("The one-private-italic-thought-per-named-NPC standard is suspended in mass combat") and the Mass Guide §9, which repeats the suspension. R39-7 sides with R54-19 ("survives only for scenes with no POV lock (omniscient and mass combat)"). No CONFLICTS row names R54-19. It can be asked, or logged.

## 9. Alchemy in scenes

**Settled**

| Rule | Exact words | Status |
|---|---|---|
| R18-5-ALCHEMY_SOURCE_ORDER | "Three sources, consulted in this order, and none of them optional." (Alchemical Index, Alchemetrica, The Real Alchemy) | live |
| R18-5-ALCHEMY_DOCTRINE_BINDING | "the reagents are the nouns, the Wellspring is the verb, Glyphica is the grammar" | live, amended by R61-5, R61-6 |
| R2-6-REPLENISHMENT_RULE, R61-101 | "no consumable restores a practitioner's magazine."; "R2-6 governs: no Draft refills a reserve."; alchemical treatment "reads as speeding Wellspring recovery, not supplying EU" | live (closed C-096) |
| R61-100-ALCHEMY_PAID_BY_STOCK_AND_VEIN | "Drafts stay reserve-free. A Crystal-bearer's standing work (a seal, Jabir's amulet, an impression-body) costs a once-only share of reserve" | live |
| R61-102 | "Pure alchemists hold Tiers of Standing up to Five (Expert) by bench certification, and that Tier caps what they make." | live |
| R61-105 | "The medicine heals at a dose and poisons past it." Paracelsus shows "early crucible palsy and Draft-mark" | live |
| R61-6, R61-5 | "Calcination and Distillation are not Wellsprings; they are bench operations only."; Sublimatio is sublimation, Sublimare distillation | live |
| R61-82 | "Sulphur Core, Salt Shell, Mercury Attraction." | live |
| R61-73, R61-7, R69-3 | after nine days "Only Trait tissue: passive Class IV carry"; four residues inside the nine days, three after | live (closed C-097) |
| R61-77 | "A revenant is a body that spends its nine days where the Wellspring cannot take the residue"; "moving or grounding the body (Stillgate Ash) is the counter." | live |
| R61-108 | "Reserve share, site depletion, waste heat, a Drift Scale tick for Category Two and up, and every Anamnesis read erasing what it takes." | live |
| R61-109 | Mortalis Categories floor at "Flourishing, Glory, then Refraction with individual review." | live |
| R61-110 | "A ring of Stillgate Ash (Journeyman gate) grounds the body's residual charge"; "the counter costs whoever uses it." | live |
| R61-55, R61-85 | the Mother's methods trace to the Necrocursica, "a counter someone can find"; "Every corruption gets a named, findable counter" | live |
| R61-91 | Mu-jin and Malphas "Both Draftcraft"; "their work is traceable through provenance." | live |
| R61-112 | "Each author states figures as their instruments give them." | live |
| R45-3 | an enhancement "enchanted, glyphed or alchemically worked beforehand" is capped at "the maker's Grade at the time of making" (summary) | live |
| R60-07, R70-46, R53-07 | consumer Essence goods sold as products; craft shown as process; prices from the approved table | live |

**Open for the questionnaire**

- **Alchemy as a combat tool has no rule.** Nothing says what a Draft does inside a fight (a stimulant, a clotting salve, a pain-killer, smoke, flash, an incendiary, poison on a blade or in shot), only what it may not do (refill a reserve). Whether a Draft drunk mid-fight can do anything a fight would notice, and what it costs the drinker, is open. The Combat Guide's Appendix A carries "alchemical reactives" (Sun-Salt, Therphorus) as uncovered.
- **Poison.** R61-105 settles dose for medicine; poisoning in a fight (onset, the ATLS-style clock for toxins, who can read it) is unruled.
- **A Draft's readout.** R70-95's item card covers purchase and appraisal; whether a Draft's effect gets a readout at use, and whether it counts against R70-86's cap, is unruled.
- **The alchemist who fights.** No grammar fits a bench practitioner in a fight (Expenditure is the nearest).
- **Open alchemy conflicts that a scene would hit** (all `open`): C-136 (does Draftcraft need a Soul Crystal at manufacture), C-137 (does a 715 IC bench own a thermometer), C-139 (which Crystal layer decides a Draft, and so where its cost and counter live), C-142 (a pure alchemist's product capped at Hollow by Class Ø, or at Expert by bench Tier), C-146 ("Rupture" has three referents), C-147 (what causes Draft Corruption), C-152 ("turn" is fourteen days in alchemy and six seconds in combat; "a reader applying Fracture of Worlds VII to the Bed gets eighteen seconds"), C-153 (calcination and Bed durations against the real record), C-154 (an impression-body is a Greater Summons at Stages IX to XI, yet Category Three floors at Refraction, VII). Also open and narrower: C-138, C-140, C-141, C-143, C-144, C-145, C-148, C-149, C-150, C-151.
- **Owed, not open**: The Real Alchemy page is written and "awaiting Isaac's ratification" (C-110's status line); R61-103's Draft Sub-Stat profile was to be "Filed through propose_rule" and does not appear in `proposals/PROPOSED.md`.

## 10. Enforcement

**What is built**

- `build/verify.py --combat` runs two WARN checks only: the POV school's vocabulary (zero terms of the school warns; schools `blade` = the HEMA list, `japanese`, `chinese`, `korean`, `percussion`, picked by `--school` or by the culture tag: Moto, Yukari, Ketsuen, Shirogane, Kōkan to japanese; Mahuo, Hon-guk to korean; lineage halls to chinese; else blade) and anatomy (zero anatomy terms warns). Both cite R13-9 checks 22 and 23 and R70-136.
- Stock formulas: "killing intent surged", "qi surged" and kin FAIL in narration (R70-35), with looser variants and "killing intent" alone at WARN (R70-36).
- Readouts set off as their own bracketed line are left out of the rhythm counts (R70-80, R70-136); nothing counts them.

**What the law asks and nothing enforces**

- R13-9-VERIFY_CHECKS_22_26 makes checks 24 to 26 FAIL ("causal-connective density in fight passages, a stated fault per named technique, a reserve account per working"); the Manual Verification Guide (renumbered 32 to 34) marks all three "not automated".
- Check 27 terminology audit (R14-6-CHECK27) and R14-5-BUILD_TERMS_LIST: `wotr_terms.txt` "does not exist"; not automated.
- Check 29 / 36, the loadout (a Stat Ledger per named practitioner, R14-6-CHECK29): not automated.
- The readout cap (R70-86), no running figures (R70-88), body before number (R70-89), one display beat per practitioner (R70-73), one flashback per fight (R70-103), the two-voice cap (R12-4): none checked.
- The `percussion` school list in verify is pugilism vocabulary (jab, cross, hook, uppercut, clinch, southpaw), while the Percussion grammar is hammer and haft (the Settling, the Sweep, the Shove, the Return). A hammer fight in the Percussion grammar can pass with no hammer word; whether the list should be the Dawi table's (once written) is open.

---

## SETTLED: do not re-ask

From the style questionnaire (2026-10-03), as the brief lists them:
- CB1 moves named in the POV's own school (R70-100). CB2 full declaration with a price (R70-101). CB3 duel shape follows the grammar (R70-102). CB4 one full flashback, POV only, once per fight (R70-103). CB5 rivals who chose to spare, paid on the Ledger (R70-104). CB6 killing rites and elegiac image by culture (R70-105). CB7 battles cut between hill and ditch (R70-106).
- MY1 the Crystal as inner map (R70-68). MY2 Pressure through the room first (R70-69). MY3 killing intent as aimed Pressure (R70-70; the mechanism itself is open). MY4 rules shown before the fight (R70-71). MY5 the crowd chorus in hearing (R70-72). MY6 one display beat per practitioner (R70-73). MY7 numbered rites (R70-75). MY8 the world's law stated, reasons kept (R70-76). MY9 numbered forms and long hall names (R70-74).
- LR8 readouts at appraisal, wound, Essence spent, never Pressure (R70-85). LR11 Grades at the read, no running figures (R70-88). LR12 body, then number (R70-89). LR23 breakthrough in the crisis, line after (R70-91). Also LR2, LR3, LR4, LR9, LR10, LR15, LR17, LR21, LR22 (R70-79, R70-80, R70-81, R70-86, R70-87, R70-93, R70-95, R70-99, R70-78).
- DD6 one held instant at the deciding exchange (R70-57). VO2 marked roll call (R70-11). K3 Western leads combat, injury and dialogue (R70-3). SP2 jo-ha-kyū tempo (R70-15). DL6 the face-slap with a bill (R70-112). VB12 the stock-phrase bans (R70-35). ME2 verify by school (R70-136).

Settled before the style questionnaire, and listed "settled, not asked" in its decisions file:
- The clinical floor for wounds and exchanges (R48-34, R13-4). Death is permanent (R60-04). Every working costs something visible in the body (R12-1, R48-37). No figure on the page is invented (R12-5, R14-6). Stat names, Grades, Stages and EU in narration (R49-47, R51-16). The three-layer account at first display and finisher (R48-20, R13-2). Damage numbers, reserve readouts and stat talk inside a fight (R49-47, R52-05). Nobody translates his own technique aloud (R8-26-NO_SELF_TRANSLATION). Technique names and translations free in narration; bare mechanism terms mid-action (R49-48, R51-17). A combat turn is six seconds (R47-11). Real object names (a katana is a katana) (R53-25). Unbound as the model for stat talk (R14-B, R70-93). Isaac's characters never thought, voiced or acted for (R49-01).

Settled elsewhere, and not to be re-asked:
- The four grammars and the nine assignments (R1-1, R3-7, R4-H1, R4-H2, R20C-54); Sodoku's is canonical and his.
- Lethality, real healing times, the hard reserve clock, death (R60-01 to R60-04); healing costs more than breaking (R47-11).
- Never rigged, veteran-clever NPCs, each side invents its own uses, death if earned, surprises foreshadowed (R57-10, R48-36, R48-35, R48-31, R48-30).
- Counters as facts, mandatory on Signature techniques, derived from the mechanism; inherited Wellspring failures (R47-3, R12-3, R17-3, R47-9).
- Documented techniques countered by study, self-derived ones read live in two or three exchanges (R12-3).
- Four voices, at most two per engagement; readouts outside the cap (R12-4, R70-87).
- Scaling vocabulary in the notes only (R13-6).
- Research before any set piece (R13-7); the gap-fill pass, which may change an outcome and says so (R13-5, R13-D).
- Anyone in diagnostic voice may speak in Joules and m/s (R13-A ruling; R20C-24 superseded); units by the POV's culture (R70-29).
- Firearms: they exist, open engagements, become clubs inside twenty feet; the silhouette; proof-marks; three ammunition tiers; up-to-1900 hardware; enhanced shot for elites; the working (not the steel) stops shot at a worked cuirass; narration may state the cause of any penetration (R11-3 rows, R11-5, R20C-22, R53-03, R53-04, R13-C, R53-05). C-001 is closed by R53-05; do not ask it again.
- Dodging and catching shot; enhancement ceilings; per-shot cost (R45-1 to R45-5). Item Tiers, armour as proof, item costs (R46-1 to R46-4). Tiers by name only (R47-5, R47-7, R70-82). Weapon entry fields (R13-9).
- Mass combat: precedence, sensory hierarchy, three registers, the Mass Hit Model, Frontage/Sustain/Re-form, Domains break not kill, rout, aftermath-first, gore at scale, name three, naval, siege, cavalry, practitioner POV before and after (R1-2, R1-3, R1-4, R2-5, R2-6, R3-8, R3-9, R54-17, R54-20).
- Alchemy: source order, doctrine binding, no Draft refills a reserve, Drafts reserve-free, bench Tiers to Expert, dose, the Crossing's nine days, revenants, Mortalis cost stack and floors, Stillgate Ash, findable counters for the cult and the corruptions (R18-5, R2-6, R61-100 to R61-110, R61-55, R61-73, R61-77, R61-85).

## Open items, conflicts and debts the questionnaire may take up

**Docket.** Empty for combat, magic-mechanism, adjudication, items and mass-combat (0 pending, 0 proposed).

**Open CONFLICTS.md rows that touch these dimensions**
- C-122 Hollow strike energy (below 60 J against 40 to 300 J).
- C-123 grain against the Class Ø cap.
- C-124 Pressure on the unwoken.
- C-158 the technology ceiling (1900 against the mid-1900s), which reaches firearms through R53-03.
- C-159 one release per scene (R8-26) against no limit (R50-09).
- Alchemy: C-136, C-137, C-139, C-142, C-146, C-147, C-152, C-153, C-154 (scene-facing); C-138, C-140, C-141, C-143, C-144, C-145, C-148, C-149, C-150, C-151 (doctrine and terms).

**Flagged in rule notes, never logged as a C-row**
- Faculty appraisal of another's exact figures (R70-85 against R70-79).
- How a Crystal line shows an estimate (R70-78 against R70-99).
- Whether the other set-off occasions sit inside R70-80's "only".

**Found in this pass, not logged**
- R54-19 (one italic thought per NPC kept in mass combat) against R1-3-NAME_THREE_RULE and the Mass Guide §9 (suspended).
- R13-4-DENSITY_BUDGET and R1-3-WORD_FLOOR_INCLUDES_AFTERMATH keyed to 2,500 words against R48-28 and R48-46.
- R20C-22 ratifies the ammunition tiers "subject to R20C-26", a superseded row.
- "Proofed" names both item Tier 2 (R46-2) and Pack Eleven's Guild-proofed plate and shot.
- verify's `percussion` list is boxing vocabulary, not the hammer grammar's.

**Owed by rule text (debts, not questions, though the questionnaire can collect Isaac's choices for them)**
- The killing-intent mechanism (R70-70).
- The Percussion master-strike table, Dawi-authored (R13-6, R20C-25).
- The remaining named-character grammar assignments (R20C-54).
- The Moto narration register (R20C-58); an untracked draft sits at `imports/drafts/moto-narration-register.md`, "draft for Isaac to rule on", with Bram Greymane and Lorn Stark registers beside it.
- Alchemical reactives and Auramancy; Aether-Sight visors (Combat Guide Appendix A).
- The Real Alchemy's ratification (C-110 status); R61-103's Draft Sub-Stat profile filing.
- Checks 24 to 27 and 29 (R13-9, R14-6) unbuilt; `wotr_terms.txt` (R14-5) unbuilt.

**Uncovered by any rule (the widest open ground)**
- Gunpowder battle: volleys, rifle lines, artillery, squares, smoke.
- Skirmish scale between duel and formation.
- Alchemy inside a fight: Drafts, poisons, reactives, and the alchemist as a fighter.
- Domains in a duel; joint workings between allies.
- Environment as an adjudication row; one against many; near-equal contests without dice; carried wounds as stat penalties.
- Schools for cultures outside the five lists, and whether a marksman's or field-caster's grammar is wanted.
- Firearm texture law, now that R53-05 superseded the row that carried it.
