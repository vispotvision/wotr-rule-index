# The current style law, mapped for the style questionnaire

Working research for the Western / Eastern / LitRPG style questionnaire. Read 2026-10-03 from `rules/*.yaml` (the source of `out/rules.live.full.md`), `desktop/NATALIE.md`, Packs Five, Nine, Eleven, Twelve, Thirteen and Fifteen in `sources/`, the companion guides and `CONFLICTS.md`. Statuses are the index's own: **live**, **superseded** (struck or replaced; "repealed" below means struck in words), **proposed**, **pending**. The index today has no proposed or pending style rows and `out/docket.md` reads "0 outstanding": every style question ever asked has been ruled. Quotes are Isaac's own files.

Plain-language glossary for terms used below, at first use:
- **LitRPG**: fiction where a game-like system (levels, stats, skills, status screens) is visible on the page. **Status screen / blue box**: a boxed panel of game text dropped into the prose ("[Skill acquired]"). **GameLit**: the lighter cousin. **Progression fantasy**: the hero's measurable climb is the plot.
- **Cultivation / xianxia / wuxia**: Chinese web-fiction traditions; xianxia is immortal-cultivation (realms climbed by refining the self), wuxia is martial-arts chivalry (sects, masters, techniques with names). **Manhwa**: Korean comics; **light novel**: Japanese serial prose, often first person with status screens; **isekai**: transported-to-another-world fiction.
- **Free indirect discourse (FID)**: third-person narration that slips into a character's own words and judgements without quote marks. **Psychic distance**: how close the narration stands to a character's mind.
- **Gloss**: a sentence whose only job is to state the significance of the sentence before it. **The Ladder**: "X was Y and Y was Z" chains. **Reification**: giving an abstract noun a physical verb ("he set the silence down"). **Hypophora**: asking a question in order to answer it. **Anaphora**: repeating a sentence opening for cadence. **Triad / tricolon**: a three-part list or rhythm.
- **HEMA**: Historical European Martial Arts (Liechtenauer, Fiore), the fencing vocabulary the combat law uses. **ATLS class**: the trauma-medicine scale for blood loss (Class I to IV).
- **Kishōtenketsu**: a four-part story shape from Chinese and Japanese poetics (set-up, development, twist, reconciliation) that does not need conflict to drive it.

---

## Headline findings for the questionnaire

1. **Stat words in narration are already legal, and most of the prose-facing documents have not caught up.** R49-47-STAT_WORDS (live, 2026-09-26): "All free: narration may state stat names, Grades, Stages, eta, EU figures and Guild words on its own authority." R51-16-OLD_BANS_FALL (live) says the same and supersedes the Sub-Stat and light-novel bans. Still saying the opposite: NATALIE.md Table Rule 5 (Sub-Stat names "in a mouth, never in narration") and the Magic Frame ("names only in a mouth, an instrument, a document, or a private count"); the wotr-write skill (`references/scene-pipeline.md` lines 42 to 44, and `prose-law-quickcheck.md`'s "narration leak" grep); the Master Style Directive's 2026-09-12 edition §1, §4.6 and §6.1; and R14-4-SUBSTAT_DIAGNOSTIC_ONLY, still marked live in the index though R49-47 overtakes it. The computed brief's premise that "current law keeps the numbers off the page" is the *older* law. The questionnaire should start from R49-47, not from NATALIE.md.
2. **Status screens were never re-ruled.** The only ban, R5-F-LIGHT_NOVEL_NOT_KEPT ("Status screens, panels, HUD-style rendering. Already banned"), was marked superseded wholesale by R51-16 on 2026-09-26, but R51-16's text speaks only of vocabulary. Meanwhile the Master Style Directive §4.6 still bans status screens and the Dialogue Craft Standards §3.H says "LitRPG/system text stays minimal and earned". Status screens sit in limbo: the questionnaire has to rule them in words.
3. **A visible game-system is a world fact, not only a style.** R53-14-FOLK_KNOWLEDGE: ordinary people "could not name a Stage and use folk words"; R53-18-AWE: "a ranked practitioner is half a saint to ordinary people"; R47-12-MYSTERY_STAYS_OPEN; R48-48-EXPLAIN (the partner explains physics and metaphysics "only when asked"). A LitRPG system that everyone sees, or that speaks in boxes, collides with these. The questionnaire must say whether the "system" is diegetic (exists in the world: a Guild instrument, a Measurewright's slate, a Crystal sense) or a reader-only convention.
4. **"Western flesh" is still written into live law.** R5-A-FLESH_CHANGES, R5-E-MARTIN_WINS_RULING, R11-1-TONAL_SPINE_UNCHANGED and the repeal of the Manhwa Energy Directive (R5-B-MANHWA_DIRECTIVE_REPEALED, which turns several East Asian web-fiction moves into "active tells") all stand. A real blend needs these named and either kept, narrowed or struck.
5. **The tools would fail a LitRPG page as written.** `build/codex.py`'s glyph pattern `\[([A-Z][A-Za-z']{0,5})\]` catches `[Skill]`, `[Status]`, `[Title]`, `[Class]` and fails them as unknown glyphs (check 47); `verify.py` fails every em dash and reads a `>` blockquote as narration or document (so the modern-word list runs on it); tables and blockquotes do not count toward word count. Any box format needs a checker decision.

---

## 1. Narrative voice and narrator stance

- **R5-E-NARRATION_NEVER_ADJUDICATES** (live): "Third-person scene narration is POV-locked and never adjudicates. No line tells the reader what to think of a character's choice."
- **R5-E-MARTIN_WINS_RULING** (live; ruled 2026-09-12): "Martin wins on narration authority. Tolkien's elevated and elegiac register is available, his moral voice is not."
- **R5-E-FREE_INDIRECT_CARVEOUT** (live): a moral verdict "in the POV's own idiom, which could be wrong, is characterisation." The same in a neutral narrator's voice is cut.
- **R5-C1-NARRATION_NEVER_WINKS** (live): "No line acknowledging that the reader knows better."
- **R48-05-HIGH_STYLE** (live): "High mythic style is allowed freely in narration whenever the moment calls for it." Supersedes the quarantine R5-E-ELEVATED_REGISTER_QUARANTINED (superseded).
- **R51-01-TIMELESS** (live): "plain, undated English by default; some cultures' scenes (Eresse, the Moto court) may take a more antique narration."
- **R5-F-LIGHT_NOVEL_NOT_KEPT** (superseded by R51-16): had barred "the isekai commentary register. Wry narrator asides about the world's rules." Nothing live now bans the wry aside by name, but R5-C1 (never winks) and R5-E (never adjudicates) cover most of it.

**Blend collisions.** Chinese and Korean web fiction often uses a commenting narrator (the storyteller's "little did he know", a narrator who rates a technique's grandeur); classical Chinese fiction has the storyteller frame; LitRPG often has an ironic, gamer-literate narrator. All three collide with R5-C1 and R5-E. Japanese light novels are frequently first person; current law assumes third person throughout (no rule bans first person, but R5-E, R35-1 and R16-5 are all written for third). Decision needed: is a storyteller or system-voice narrator ever allowed, and does first person become legal for scenes (it already is for in-world documents; the alchemy texts were converted "in first person throughout", R61).

## 2. POV and psychic distance

- **R35-1-NARRATION_DISTANCE_BANDS** (live): three distances, close, medium, distant/formal; "Every POV character carries a narration distance." Distant/formal is "an omniscient epigrammatic voice", assigned only to Cozbi Mahuo (R35-2).
- **R41-1-DISTANCE_IS_TWO_AXES** (live): register says whose idiom; band (1 to 5) says how deep.
- **R49-03-BAND_CAPS** (live): "Lift the per-character depth caps toward deep: every major POV moves closer."
- **R48-08-NEW_POVS** (live): new or minor POVs "default to close, deep interior".
- **R54-13-NO_POV_WITHOUT_REGISTER** (live): a character carries a POV only once a narration register exists. **R58-05** (live) approved "the Moto, Bram Greymane and Lorn Stark narration registers" (the draft file `imports/drafts/moto-narration-register.md` still says "Not canon" in its header: stale).
- **R20C-58-REGISTERS_FLAVOUR_NOT_LAW** (live): per-culture registers are flavour, "Moto register is the exception".
- **R5-C1-INFO_TRACKED_PER_POV**, **R5-C1-WRITE_FROM_LEAST_KNOWING** (live): dramatic irony through POV lock.
- **R49-11-NOT_KNOWING** (live): the ignorance and misreading quotas "become optional; no per-scene minimum". NATALIE.md Table Rule 8 still states them as per-turn and per-session duties (stale against R49-11).
- **R49-09-CUTAWAYS** (live): "a short, clearly marked cut to something the POV cannot see". **R39-7** and **R48-40** (live): no NPC italic thought under a POV lock in written scenes; roleplay keeps one per NPC.
- **R3-9-PRACTITIONER_POV_RULING** (live): a high-Stage practitioner's POV during a battle "dissolves the fog, the pressure and the helplessness".

**Blend collisions.** Martin's POV discipline (one locked head per chapter) is the Western spine here. Wuxia and xianxia commonly head-hop and cut to bystanders gasping at the hero; the manhwa "reaction shot" was struck as a tell (R5-B). LitRPG is usually deep single POV with the system as a second voice inside the head, which fits the close distance but raises a question R35-1 never asked: is a system voice a narration register of its own? The Moto register is the only built Japonic one; Korean (Mahuo, Hon-guk, Ketsuen, Sum-gol) and Chinese lineage-hall POVs have none, so under R54-13 no Korean or Chinese-stratum character can carry a POV until one is built. R3-9 also cuts against progression fantasy's pleasure of the overpowered POV at a battle.

## 3. Tense (and person)

- **R49-02-TENSE** (live): "roleplay turns, and work improved for a roleplay, are written in present tense; written scenes and books are written in past tense."
- Person: no rule names it; every narration rule assumes third person (R5-E, R16-5 "available to third-person narration").

**Blend collisions.** Present tense is common in Korean web novels and some LitRPG; first-person past is the light-novel default. Decision: whether books stay third-past, whether a first-person mode exists for some threads, and whether status screens are tenseless.

## 4. Rhythm and paragraphing

- **R48-06-RHYTHM_LAW** (live): "the hit is the shortest sentence and sits last, payoffs under 10 words, at most two long sentences in a row".
- **R4-14-LANDING_RULE** (live): "The emotional hit takes the shortest sentence in its paragraph and sits last."
- **R4-14-HARD_CEILINGS** (live): payoff 10 words, 0 subordinate clauses; 18% of sentences under 8 words; no paragraph closing on three sentences over 18 words.
- **R4-14-RUN_RULE**, **R4-14-CHAIN_CEILING**, **R4-14-CONJUNCTION_AUDIT** (live).
- **R49-12-SHORT_FLOOR**, **R49-13-VARIANCE** (live): sentence-length variation target 80%, "under 50% is the strongest tell".
- **R48-07-WHITE_SPACE** (live): "Steady paragraphs: medium paragraphs, white space used sparingly so it still means something." **R49-14-PARA_SHAPE** (live) keeps the checker warning anyway.
- **R49-15-FRAGMENTS** (live): image fragments free; "negative and 'Only/Just' emphasis fragments stay warned at three per scene".
- **R49-16-MODIFIERS** (live): adjective stacking by ear.

**Blend collisions.** Korean and Chinese web fiction runs one-sentence paragraphs and heavy white space for phone reading; LitRPG punctuates with stat blocks. Both collide with R48-07. The landing rule and the payoff ceiling are a Western cadence (end the paragraph on the short blow); Japanese prose often lets the paragraph end on an image or a seasonal detail rather than a hit (closer to R49-26's "concrete image" ending, which is allowed for scenes but not paragraphs). The variance law is the anti-AI foundation (AI Tells guide §0) and is the hardest thing to touch.

## 5. Imagery and metaphor

- **R48-01-BEAUTY** (live): "exact concrete detail, images and metaphor, and what goes unsaid".
- **R48-03-SIMILES**, **R49-18-SIMILE_COUNT** (live): no simile ceiling, only two similes "competing over the same beat get flagged"; em dashes stay banned.
- **R48-04-METAPHORS** (live): "Metaphors come from the POV's own life: trade, homeland, body". **R49-19**, **R49-20** (live): extended metaphors allowed; dead metaphors always rebuilt.
- **R49-21-REIFICATION**, **R57-42** (live): no count; keep "never at the beat" (R4-15-NEVER_AT_BEAT: "The value flips on a body or an object, never on a personified noun") and "object first".
- **R49-22-NATURE** (live): "Avoid personifying weather and landscape: the world is described, not personified."
- **R49-23-HIGH_STYLE** (live): "Anaphora and the triad come off the tell list everywhere; always legal." **R49-24-ELEGY** (live): "loss may be sung in full cadence."
- **R6-1-LADDER_BAN** (live): "an automatic cut, never a rewrite."
- Master Style Directive §5 (2026-09-12 ed.): metaphor is "WOTR's native tongue", Hermetic correspondence available.

**Blend collisions.** R49-22 directly blocks a core East Asian move: landscape that feels (the mountain that broods, the river that mourns), the seasonal word (kigo, the season-marker of Japanese poetry) that carries emotion by association, mono no aware (the gentle ache at things passing) carried by falling blossom or first frost. Chinese poetic imagery works by paired images and parallelism (duizhang, matched couplets), which R49-23 now allows but the AI Tells guide (`scenes/` second edition) still lists as "excessive tricolon" and "anaphora abuse" (stale). The anime "aura" glow is already constrained: R9-3-AURA_AS_FRACTURE replaces "it glowed" with broken geometry at a Stage display.

## 6. Description

- **R48-02-DENSITY** (live): "Lush throughout: every scene gets full sensory layering; slower, denser, more immersive."
- **R53-30-TEXTURE_DENSITY** (live): "Every beat carries at least one detail that could only exist in this world".
- **R49-28-INTROS** (live): full physical inventory "all at first sight, in one descriptive passage". NATALIE Table Rule 11 carries the same.
- **R51-31-SENSE_BANK**, **R6-9-RECURRENCE_RULE** (live): scenes draw texture from the culture's Standing Inventory first; "Identity is repetition. Novelty is its enemy."
- **R53-19-QUOTA**, **R49-54** (live): two signature items per culture per session.
- **R53-23-MIXED_ROOM** (live): a mixed room layers every culture present equally. **R53-24** (live): texture and mechanism mix freely.
- **R53-28-VISUAL_REFERENCE** (live): "Lord of the Mysteries and Victorian imperial-age fantasy; the Berserk and Vinland Saga references are retired everywhere."
- **R9-3-*** (live, Pack Nine): manhwa power-display grammar for Stage ascension, Pressure drop, first display and finisher: eyes as the tell, aura as fracture, body under load ("exactly one splash-panel beat per scene"), silhouette entrance.
- **R11-1-REFERENCE_TRIANGLE** (superseded): had widened the manhwa grammar "to the general visual register"; now superseded, so the narrow Pack Nine scope stands.
- Visual Aesthetic Guide (2026-09-12 ed.) §2 and §3: desaturated default palette; magic as "Weather, Not Fireworks"; "Anti-pattern to kill on sight: describing a working like a UI or a light show".
- **R8-15-DESCRIPTION_STYLE** (live): an ability entry's description is "flat operational prose, no mood, no cadence work".

**Blend collisions.** Isaac's "descriptions should cover a wide variety of things" pulls against R6-9's "Novelty is its enemy" and the inventory-first rule; the questionnaire needs a range list (food, craft, law, money, weather, architecture, ritual, clothing, the body, animals, music, smell) and whether range comes from more inventory entries or from free invention (R48-26 already allows logged invention). The Visual Aesthetic Guide's "kill on sight" UI anti-pattern is the opposite of LitRPG's on-screen notifications. Manhwa splash panels are rationed to one per scene; cultivation breakthroughs (heaven-shaking ascensions) want more. The guide still cites the Berserk/Vinland split in §4a (stale against R53-28).

## 7. Exposition and the iceberg

- NATALIE.md Prose Standards: "Iceberg: reader sees ten percent. No 'as you know.' Exposition through disagreement, negotiation, or a real knowledge gap."
- **R19-4-ICEBERG_DIALOGUE** (live): "nobody explains anything they both already know. The iceberg rule is a dialogue rule first."
- **R4-13-ZERO_BUDGET** (live): "Zero glosses per scene. Not rationed. There is no acceptable first instance."
- **R51-15-FIRST_USE** (live): new terms "get meaning from context and use only; no appositive gloss". **R51-14** (live): "No ceiling on WOTR terms per page; readers learn by immersion."
- **R49-43-EXPLAINING** (live): "Narration may explain causes anywhere, in the POV's reasoning and vocabulary; the mouth-only rules for the why of a working are struck."
- **R48-25-AWE** (live): "scenes explain Wellsprings, rites, oaths and the Veil as plainly as a sword exchange."
- **R5-F-LIGHT_NOVEL_KEPT** (live): "Legibility as reader pleasure. The satisfaction of a system the reader can reason inside."
- **R48-48-EXPLAIN** (live): the partner explains "only when asked; working it out is part of the challenge" (a table rule, but it governs the out-of-character channel).
- **R47-12-MYSTERY_STAYS_OPEN** (live), against **R12-A** (ruled 2026-09-12: "The Origin layer is explicable too; nothing is permanently mythic").

**Blend collisions.** LitRPG explains its system openly in skill descriptions and tooltips, which is a gloss by R4-13's definition and an appositive gloss by R51-15. Cultivation novels open with realm ladders explained by a master to a disciple, and the disciple's "as you know" is the genre's teaching scene. The law already allows explaining causes in narration (R49-43) but still bans glossing; the line between a system description box and a gloss needs drawing.

## 8. Dialogue and register

- **Pack Fifteen §1, R15-1-*** (live, the Register Repeal, 6 September): "Interesting beats consistent." Repealed: the Diction Palette cap, register by culture in narration ("Available as flavour. Not law"), the Racial Voice guide as enforcement, the Elevated Vocabulary mandate, class-marking by vocabulary, the Mystic Register's "never physics" clause for documents, and "reads modern" as a critique. Survives: **R15-1-VOICE_DIFFERENTIATION** ("If two characters' lines could be swapped and nobody noticed, the scene has still failed"), the Technical Register, the AI-tell checks, the Standing Inventory. **R15-1-LICENCE** (modern words everywhere) is now superseded by **R48-13-PERIOD_FEEL** (live): "Modern words in speech only: characters may talk modern; narration keeps a timeless register."
- **R19-4-REALISTIC_SPEECH** (live): false starts, interruption, non-answers, talking past each other "as craft law". **R19-4-REGISTER_UNDER_STRESS** (live): speech gets shorter, more concrete, more repetitive. **R19-4-WORLD_ANCHORED_SPEECH** (live): idiom from "their own life and trade".
- **R19-5-COMPOSURE_BAN** (live): "No character speaks in balanced clauses under duress". Narrowed by **R52-06-TRIADS** (live): "Triads and parallel clauses are legal in any mouth, under duress included".
- **R19-2-FIXED_TEXT**, **R19-2-NEVER_ALTERED**, **R19-3-PROSODY_VERBATIM** (live): Isaac's dialogue is set as written; **R57-04** (live) improves it only when he asks for an RP post to be made better.
- **R52-02-VOICE_LEVER** (live): "A voice is mind and sound in equal measure". **R52-03** (live): a full voice block on every major card. **R52-05** (live): exact-number speech belongs to Lambert, Measurewrights, clerks and instrument readers.
- **R51-21-MOTO_WORDS** (live): Moto "use Japanese honorifics and address forms in speech, in a feudal register, never modern casual." **R52-21** (live): Kwon Mu-jin never uses rank or old court honorifics to win an argument. **R52-23** (live): the Mahuo "we" under strain. **R52-20** (live): Aurelian's Sum-gol dropped copula.
- **R51-27-DIALECT**, **R49-37** (live): full phonetic dialect allowed. **R51-29**, **R51-30** (live): culture swears first; Earth holy swears replaced. **R51-09** (live): modern-speech level set per card, default "casual, not current".
- **R49-31** (live): dialogue mostly untagged. **R49-39** (live): dialogue and description "about even".
- **R48-43-SPEECHES** (live): one crafted eloquent speech at a big moment.
- **R14-B** (ruled 2026-09-12, Isaac's words): Sub-Stat names "can be named, but do it like how people talk about stats in LitRPGs like Unbound." Now widened by R49-47 and R51-16.

**Blend collisions.** Wuxia and xianxia dialogue carries formal address chains (senior brother, young master, this venerable one), boasts and declared challenges, and the arrogant young master's set speech; R23-10 (below) bans "honorific stacking" in names, and Pack Five struck "loud opinions as a default register". LitRPG characters talk about builds, levels and drops openly; R52-05 restricts exact numbers to counting trades, and R53-14 says commoners cannot name a Stage. Korean honorific levels (speech styles that mark rank) have no rule of their own; R52-21 gives Mu-jin a refusal of them, so they exist in-world.

## 9. Interiority

- **R48-39-INTERIORITY** (live): "deep and running: thoughts, memories and reasoning flow through the narration."
- **R49-05-ITALICS** (live): italic direct thought "often". **R49-06** (live): full flashbacks "a page or more when they matter".
- **R49-07-EMOTIONS** (live): "show it in the body first; the POV may then name it in his own word."
- **R49-08-MEANING** (live): "the POV may reflect on what it meant in his own idiom, and may be wrong; neutral narrator summaries stay banned."
- **R49-01-WHOSE_HEAD** (live): roleplay narration may go deep inside Isaac's character; he overrules any thought not his. NATALIE.md: never "think, speak, or act for Isaac's PC" (in tension; R49-01 is the later and narrower rule).
- **R16-8-CHECK33** (live): "Fewer than half of a scene's technical terms may sit inside italic thought."
- **R6-2-READ_DELIVERS_FACT** (live): a faculty's read delivers "a bare fact ('Twenty-three')". **R6-2-FACULTY_NEVER_SUBJECT** (live) against **R54-21-FACULTY_AS_SUBJECT** (live): inside a close register the faculty may be the subject.
- **R20C-49-GLOSS_RIGHTS_CARD_FIELD** (live): "Lambert yes, Yoko diagnostic only, Cozbi unlimited, Sodoku never, Emira never."

**Blend collisions.** LitRPG interiority is often the protagonist reading his own screen and planning a build; R6-2's "bare fact" read is the nearest legal form. Japanese interior monologue (the light-novel tsukkomi, a character's sharp inner retort to absurdity) is a comic form close to the struck setup-deadpan-reaction. R52-27 ("Joy in a guarded voice ... shows in hands, face and breath") and the Moto register's "never names its own pleasure, triumph or grief outright" are restraint rules that fit Japanese reticence well.

## 10. Humour and tone

- **R5-D-HUMOUR_PERMITTED** (live): "dry understatement, gallows wit ... class-inflected contempt, a character being funny without knowing it, and the joke that is also a threat."
- **R5-D-HUMOUR_BARRED** (live): "the beat structure of setup, deadpan and reaction."
- **R48-11-HUMOUR** (live): "funny characters are funny often". **R49-38** (live) drops the funeral test for comic voices; **R52-31** (live) allows comic minor NPCs from the start. **R52-14** (live): Sodoku jokes "only by accident".
- **R5-B-MANHWA_DIRECTIVE_REPEALED** (live): struck and to be "treated as active tells": personality vomiting, reaction shots as characterisation, loud opinions as default, "bizarre or exaggerated minor NPCs", "absurdist method coexisting with genuine stakes", humour as tone exception, escalation as prose-level pacing. Master Style Directive §14 lists the Manhwa Energy Directive as "deliberately excluded".
- **R5-B-DECLARATION_TO_INFERENCE** (live): "Characterisation moves from declaration to inference."
- **R5-C2-IRREVERSIBLE_NOBODYS_FAULT**, **R5-C2-ELEGY_CONCRETE_THING** (live): elegy attaches to "a named concrete thing that is gone"; **R53-31** (live): every Inventory carries a Gone list.
- **R11-1-TONAL_SPINE_UNCHANGED** (live): "Pack Eleven widens what the page may look like. It does not reopen what the page may sound like."
- NATALIE.md: "Grimdark: victories cost. Moral ambiguity over clarity. Hope is small and hard-won."

**Blend collisions.** This is where the blend bites hardest. Shōnen, manhwa and cultivation tone (face-slapping arrogant rivals, onlookers' shock, comic overreaction, the hype beat before a power reveal) is exactly what R5-B struck. LitRPG humour often lives in the system's snark. Korean han (a collective, unresolved grief) and Japanese mono no aware are elegiac modes that fit R5-C2 and R49-24 better than the Western "long defeat" does, and could be named as the Eastern contribution to tone. The 2026-09-12 Scene Writing Process Guide §2 still recommends "Manhwa-energy beats" as an escalation tool, with an editorial note that the repeal was never routed to that guide (stale).

## 11. Combat on the page

- **R12-3-COMBAT_EXCHANGE_OWES** (live): across an engagement, the read, the fault, the counter and why it works, the cost in body and reserve, what the character cannot do next.
- **R13-4-COMBAT_FLOOR** (live): every meaningful exchange states measure, tempo (Vor, Nach, Indes: the before, after and during of HEMA timing), the named read, the fault, the mechanics of the hit, injury by structure with ATLS-class blood loss, the Essence account at three strata, what the character cannot do next. **R13-4-DENSITY_BUDGET** (live) scales it by length.
- **R13-4-THREE_EXPLANATIONS** (live): "Physics, Essence, Hermetic correspondence: at first display and finisher each is a causal sentence beside its image".
- **R48-33-CHOREOGRAPHY** (live): "every exchange traced (measure, guard and the move by its fencing name)." **R13-6-HEMA_VOCAB** (live). **R48-34-WOUNDS** (live): "full clinical gore ... blood loss tracked minute by minute". **R48-37-COST_SHOWN**, **R48-38-AFTERMATH** (live).
- **R13-6-SCALING_VOCAB_RESTRICTED** (live): power-scaling words (Attack Potency, hax, speed blitz, outlier) "author-notes and adjudication only, never on the page". **R15-4-THIRTEEN_HAX_STRUCK** (live) struck only the "never says hax" clause.
- **R13-8-RECONSTRUCTIBLE_ADJUDICATION** (live): the outcome must be reconstructible from the page. **R14-3-TRACEABILITY** (live): every outcome traces to a row in Pack Fourteen §3.
- **R8-24-RELEASE_MECHANIC** (live): an art may carry a release call (an imperative plus its name), never required, costs a beat. **R8-26-ONE_RELEASE_PER_SCENE** (live) against **R50-09-ONE_RELEASE** (live): "No limit on release calls". R50-09 lists no supersession, so the index carries both (an index fault; R50-09 is the later).
- Combat Craft Guide 3e (`desktop/`, 2026-09-26 ed.) §1: four combat grammars, Blade (Liechtenauer/Fiore), Verdict (Sodoku's Shinken-ryū: "read, rank, commit"), Percussion, Expenditure.
- Mass combat: R1-3, R2-5, R3-8, R3-9 (live), the Single Act and aftermath-first.

**Blend collisions.** Shouted technique names are a shōnen and wuxia staple; R8-24 and R50-09 already legalise them with a cost. Wuxia lightness skill (qinggong), qi deviation and sect formation arrays have no grammar; Verdict Grammar is the only Eastern-rooted one, and there is no kenjutsu, Korean or Chinese martial vocabulary rule to sit beside HEMA. LitRPG combat narrates damage numbers, cooldowns and procs; R13-6 bans scaling vocabulary on the page and the Dialogue Craft Standards §3.H lists "aggro, threat level, burst window, cooldown" as vocabulary to be absorbed into WOTR's own terms.

## 12. Magic and the system on the page

**The four explaining voices (Pack Twelve §4).**
- **R12-4-VOICE_MIXING_RULE** (live): "Four carriers. Pick per scene. Do not run more than two in one engagement."
- **R12-4-VOICE_ONE_POV** (live): "a character who is out of his depth explains wrong."
- **R12-4-VOICE_TWO_SECOND** (live): "the Kakashi model", a knowledgeable onlooker narrating the read.
- **R12-4-VOICE_THREE_OPPONENT** (live): "contempt as instruction", barred to anyone without standing to be arrogant.
- **R12-4-VOICE_FOUR_DOCUMENT** (live): "The LotM model. An in-world register entry, field manual, or codex line dropped into the narrative at the threshold of a scene."
- **R15-B** (ruled 2026-09-12) and **R20C-36** (live): "Clearly wins. Character shows in what a person chooses to explain and what they leave out."
- **R16-5-REGISTER_IN_NARRATION** (live) and **R49-43** (live): narration itself may carry technical terms and explain causes, so the four voices are no longer the only channel. NATALIE.md Table Rule 6 ("Explanations arrive through the four voices, never narration on its own authority") is stale against R49-43.

**The three-stratum stack (Pack Thirteen §2).**
- **R13-2-THREE_STRATA_MANDATE** (live): "Every working explained on the page is explained at three strata" (Aether, Wellspring, Essence). **R48-20-STRATA** (live): at first display and finisher, "lighter touches between."
- **R16-3-COMPOUND_SENTENCE** (live): the signature sentence carries "the real mechanism and the system term in the same breath".
- **R13-6-WOTR_FIRST**, **R13-6-REAL_SCIENCE_VOCAB** (live). **R13-6-ANIME_GRAMMAR_TRANSLATION_AID** (live): Nen, Naruto's shape and nature, JJK's vows, Bleach's release "never as page vocabulary".

**The two registers (Pack Twelve §2).**
- **R12-2-TECHNICAL_REGISTER_DEF** (live): "It is Naruto. It is exhaustive, tactical, and delivered in-fight."
- **R12-2-MYSTIC_REGISTER_DEF** (live): "It is Lord of the Mysteries. It is stated as law, never as physics". Softened by Pack Fifteen (documents may be scientific; R15-C ruled "No obligation") and **R48-10-MIXING** (live): "Drop the Technical/Mystic no-mixing rule: registers mix freely by ear." **R12-2-NO_MIXING** (superseded). **R12-6-RITUAL_SPECIFICATION** (live): a rite has "a bill of goods, an order of operations, and a list of ways it goes wrong".

**Stats on the page.**
- **R49-47-STAT_WORDS** (live), **R51-16-OLD_BANS_FALL** (live), **R51-17-MID_ACTION** (live: bare jargon mid-action allowed), **R49-48-TECH_NAMES** (live: technique names and translations free), **R48-21-NAMING** (live: narration names Wellsprings and glyphs freely), **R48-16-REAL_FIGURES** (live).
- Superseded on the way: R12-5-NUMBERS_DIAGNOSTIC_ONLY, R14-4-EFFECTS_CHANNEL ("Grade letters and stat names never appear in narration"), R14-4-DIAGNOSTIC_CHANNEL, R14-6-CHECK28 (the "narration leak" check), R20C-31, R5-F-LIGHT_NOVEL_NOT_KEPT, R5-A-OPERATIVE_CONSEQUENCE ("the system is author-facing and document-facing").
- Still live and now contradicting: **R14-4-SUBSTAT_DIAGNOSTIC_ONLY**, **R10-2-CATEGORY_READ_EXCEPTION** (Category naming costs "the scene's only read"), **R10-3-EFFECT_PHYSICAL_ONLY** ("Never why the Wellspring resolved as a tiger and not a wolf"), **R10-3-UNCHANGED_CONSTRAINTS**. These read against R49-43, R49-47 and R12-7-APPARATUS_CAP_REPLACED.
- **R12-5-NEVER_INVENT_NUMBER**, **R14-2-ESTIMATE_MARKING** (live): every metaphysical figure checked against source.
- **R47-3**, **R47-1** (live): abilities written as what they are, never how to use them; counters as facts.
- Pressure on the page: NATALIE Magic Frame ("One Stage up bends attention ... Felt in the body"); **R53-14**: commoners feel Pressure "as dread"; **C-124** (open, below).

**Blend collisions.** This is the LitRPG crux. Already legal: stat names and figures in narration, technique names and their translations, bare jargon mid-action, Wellspring and glyph names, exact figures from a trained eye. Not ruled: the box itself (status screens, skill-acquired notices, level-up announcements), a system voice, a stat sheet shown mid-chapter, damage numbers, and whether the "system" exists in-world. Cultivation adds realm-breakthrough set pieces (tribulation, the bottleneck, the dantian), which WOTR already has in its Stages and Threshold Events, and xianxia's "heavenly dao" is a natural fit for the Mystic Register. Anime shape-vocabulary stays author-only under R13-6; the questionnaire should ask whether genre vocabulary (sect, realm, dantian, qi, aura, mana, level, class) is admitted or always translated into WOTR nouns (R13-6-WOTR_FIRST says translate).

## 13. Names and epithets

- **R48-44-NAME_USE** (live): narration uses "POV epithets, the way the viewpoint sees them". **R49-10-EPITHETS** (live): "One epithet per character per scene".
- **R50-01-REAL_GRAMMAR** (live): borrowed names must be "real, correct phrases in that language". **R50-31** (live): romanised only, no kanji or hangul. **R50-32**, **R49-49** (live): foreign words never italic. **R50-15** (live): macrons stay. **R50-34** (live): pronunciation line on every card.
- **R50-10-NAME_STYLE** (live): plain English technique names for common-tongue fighters, "true names for houses with a register". **R50-11** (live): new English technique names two words at most. **R50-14-ESCALATION** (live): a stronger form takes a suffix in the art's own language ("Kurosetsu becomes Kurosetsu-Kai"). **R50-24** (live): schools take true names in the founding tongue.
- **R8-26-NO_SELF_TRANSLATION** (live): "Nobody translates their own technique's name aloud, ever." **R8-22-BY_NAME_POETRY** (live): the by-name is "the one place poetry is allowed".
- **R23-10-CHINESE_PHONOTACTICS** (live): "Avoid the wuxia register the base guide already warns off: no four-syllable given names, no sect-title constructions, no honorific stacking."
- Naming Guide Amendment, Mahuo (R20-*, live): "Avoid Chinese wuxia conventions and given-name-first Japanese conventions."
- **R50-04-POP_CULTURE** (live): franchise echoes (Stark, Greymane, the Night's Watch) allowed. **R53-25** (live): "a katana a katana".
- Moto canon (NATALIE.md, Moto Reversion Ledger): Büri register dead; five naming strata.

**Blend collisions.** Cultivation fiction lives on sect titles (the Azure Cloud Sect, Elder of the Third Peak) and epithet chains ("the Sword Saint of the Northern Waste"); R23-10 bans sect-title constructions for the Chinese stratum. LitRPG gives every skill a bracketed title and rank ([Shadow Step Lv. 3]); R50-11's two-word cap and R47-7 ("Tiers of standing and ladder rungs are written by name only, never numbered") both bear on that. R49-10's single epithet per scene clashes with web-fiction's rotating epithets (the youth, the young master, the trash, the genius).

## 14. Scene structure and length

- **R49-25-OPENINGS** (live): "arrivals open on the senses; tense scenes open in motion." **R49-26-ENDINGS** (live): "an action, a concrete image, or a line of dialogue; never a summary or a question." **R49-27** (live): a break mark for a real jump.
- **R5-F-LIGHT_NOVEL_KEPT** (live): "The chapter as a hard unit with one clear objective and a hook at close" and "Fast entry".
- **R48-28-TURN_LENGTH** (live): about 3,500 words. **R49-30-SHORT_BEATS** (live): "Every reply is a full turn of about 3,500 words, even to a quick line or question." **R49-29-TURN_FILL** (live): half texture and talk, half the world moving. **R48-46-WORD_FLOOR** (live): set pieces 5,000+.
- **R1-3-SCENE_STANDARDS_DEFINED** (live): "minimum 2,500 words, layered sensory opening, one private italic thought per named NPC, no section spacers, end on physical action" (partly overtaken by R49-26, R49-27, R48-40).
- NATALIE.md Table Rule 2 ("Conversational 300 to 700. Standard 700 to 1,500. Set piece 2,500 minimum") and "Length discipline ... Over-delivery is the standing complaint" are stale against R48-28, R49-30 and R48-46. NATALIE's Prose Standards section already says 5,000+ for set pieces, so the file contradicts itself.
- Scene Writing Process Guide §1: the three-pass process (pre-write, draft, silent self-review); one dramatic job per scene.
- Book pipeline (`book/design/BOOK_PIPELINE.md`): 3,500 words per chapter default, hooks planted and paid by chapter.

**Blend collisions.** Web serials run shorter chapters (2,000 to 3,000 words in Korean and Chinese platforms) with a cliffhanger every chapter; R49-26 bans ending on a question, and the cliffhanger is often one. Kishōtenketsu (set-up, development, twist, reconciliation, with no central conflict required) is an alternative to the conflict-escalation-landing spine the Scene Writing guide assumes. LitRPG chapter rhythm alternates action with downtime and loot or stat review; R48-29 already lets dull stretches pass in a line.

## 15. Banned constructions

Live, enforced by `verify.py` or by hand:
- Em dashes (**R48-03**, **R15-1-AI_TELL_CHECKS_SURVIVE**: "Em dashes, similes, not-X-but-Y, countdown negation, gloss, ladder. These are about prose failing, not about period.")
- **R49-40-NOT_X_Y**: "any pair where the second sentence corrects the first fails". Countdown negation (AI Tells guide §1). NATALIE: "No 'it's not X, it's Y.'"
- **R49-41-QUESTIONS**: every narration question flagged as possible hypophora.
- **R49-42-FILTER_VERBS** (he saw, he heard) counted. **R49-17-OPENERS**: "'Turning, he drew the blade'" constructions are AI tells.
- **R6-1-LADDER_BAN**; **R4-13** gloss, zero budget; **R4-15** reification never at the beat.
- **R51-10-SLOP_WORDS**: tapestry, testament, palpable, visceral, symphony of, orbs, ministrations, "a breath he didn't know", and the rest; **R57-30** keeps "the smell of ozone" banned.
- **R51-11-COLLISIONS**: delve, echo, numinous, sovereign, sanctum, weave, ledger used only in their WOTR sense.
- **R51-03**, **R51-04**: okay, OK, vibe, awesome, cool; triggered, toxic, closure, mindset, boundaries banned in narration. **R51-08**: no Earth day or month names. **R51-30**: no Earth holy swears.
- **R5-G-TELL_BANK_ADDITIONS** (live): "declarative characterisation, the reaction-shot cutaway, the comedic beat structure, narrator moral adjudication."
- **R49-22** personified landscape (avoid).

Stale in the guides: the repo's AI Tells second edition (`scenes/WOTR_AI_Writing_Tells_to_Avoid.md`) still lists "Excessive tricolon", "Anaphora abuse" (both made legal by R49-23) and "The Elevated Vocabulary standard is one per paragraph, maximum" (repealed by Pack Fifteen).

**Blend collisions.** "Not X, but Y" correction pairs are a staple of translated Chinese web fiction's emphatic style; "-ing" openers and simultaneous-action constructions are common in LitRPG action; system prompts are often questions ("Accept? Yes / No"), which R49-41 flags; LitRPG uses dashes and brackets in stat lines. Each needs a carve-out or a ban.

## 16. Documents

- **R12-4-VOICE_FOUR_DOCUMENT** (live): the LotM-model threshold document that "Sets a rule the scene then breaks".
- **R20C-37-DOCUMENTS_OWE_NOTHING** (live): "In-world documents owe nothing to sounding in-world." **R15-C** (ruled 2026-09-12): "a Guild proofing report may read like a lab report".
- **R51-33-DOC_REGISTER** (live): "a house style per institution: Accord chancery formal and Latinate, the Dawi Tally terse entries, Moto records in the old register, letters in the writer's voice."
- **R51-34-DOC_MODERN** (live): the modern-word list applies to documents.
- **R57-07-DOCUMENTS_FULLY_METAPHYSICAL** (live): cards, entries, items, lore, in-world documents and exports print stats, Grades, Bands, Stage, EU, AU/s, eta, Crystal State and Category.
- **R47-2-FIELD_FORMAT** (live): new abilities use the field format ("**Field** · value").
- **R8-15-DESCRIPTION_STYLE** (live): flat operational prose in an entry.
- docket/questions.jsonl, WAR-162 (open): whether the em-dash ban governs system-page documentation as well as scene prose.

**Blend collisions.** The status screen is a document by another name. Two live paths could carry it without new law: R12-4's threshold document and R57-07's fully metaphysical documents, rendered by a diegetic instrument (a Measurewright's slate, a Guild assessment, the Crystal's own read under R6-2). The questionnaire should offer that as an option against a non-diegetic system box.

## 17. Enforcement

- **R48-45-CHECKS** (live): "every turn passes the full checker." `build/verify.py` (and the MCP's `verify_scene`); `build/codex.py check` for checks 46 to 48.
- **WOTR_Manual_Verification_Guide (2026-09-26 edition)** (`desktop/`): 51 checks. FAILs: em dashes (2), not-X-but-Y (4, 5), the chain ceiling (16), short-sentence share under 10% (13), the hard-ban list (26), terminology near-misses (35), glyph validity (47) and others. Not automated: payoff length, conjunction audit, reification, collision words, italics, most combat thresholds, the dialogue checks 49 to 51 (Appendix A).
- **R12-7-AI_TELLS_RETAINED** (live): "Explaining a mechanism is no licence to write badly."
- **R14-5-NEAR_MISS_FAIL**, **R18-7-CHECK37**, **R18-7-CHECK38** (live): every capitalised system term and bracketed glyph token validated; unknown fails.
- **R16-8-CHECK30** (live): a scene with a working, exchange or injury carries at least four WOTR technical-lexicon terms and two real scientific terms in narration.
- **R54-12** (live): checks stop at the author-notes heading. **R58-04** (live): titles exempt from the ban list.
- `.claude/skills/wotr-write/references/prose-law-quickcheck.md` still greps for "narration leak" of Grade, Stage, Band, eta, EU, AU/s, Sub-Stat and for causal connectives "legal only in a mouth or a document": both stale against R49-47 and R49-43.

**Blend collisions.** `codex.py`'s `GLYPH` pattern fails `[Skill]`, `[Status]`, `[Title]`, `[Class]`; em dashes fail anywhere above `## Notes`; a `>` block is checked as a document; word count ignores blockquotes and tables, so a box-heavy LitRPG chapter would read short. Any style law that admits boxes needs the checker told how to read them.

---

## Every place the current law names its models

- **Pack Five §A** (R5-A-SKELETON_UNCHANGED, R5-A-FLESH_CHANGES, live): "Eastern skeleton under Western flesh"; the skeleton "a light-novel and xianxia inheritance"; the flesh "Martin's POV discipline, Tolkien's cultural register and elegiac capacity, Abercrombie's dry brutality."
- **Pack Five §B** (live): the Manhwa Energy Directive struck; the Foil Function kept because "It was never Eastern", with Western pairs as the models (Merry and Pippin, Sam and Frodo, Tyrion and Bronn, Jaime and Brienne, Glokta and Severard); Martin's Stannis as the model for inference.
- **Pack Five §C.1** and **Pack Six** (R6-4, superseded; R5-C1-WELL_REASONED_WRONG_CONCLUSION, live): Ned Stark as "the whole Ned Stark instrument".
- **Pack Five §C.2, §E**: Tolkien's long defeat for elegy; Tolkien's per-people narration shift for register by culture (now flavour); "Martin wins" on narration authority.
- **Pack Five §D**: humour "in the Abercrombie register".
- **Pack Five §F** (R5-F-LIGHT_NOVEL_KEPT, live): the light novel keeps chapter unit, legibility, fast entry; R5-F-LIGHT_NOVEL_NOT_KEPT (superseded) had dropped status screens and isekai asides.
- **Pack Six PART II** (source line 86): "Tolkien's fingerprint is roads, food, songs, trees and leaving. Martin's is what is on the table and who sits where."
- **Pack Seven** (superseded): objects are "the Tolkien half of the system".
- **Pack Eight §1**: technique Class (Offensive, Defensive, Supplementary) is "Naruto's three-way split, retained because it is the fastest legibility tool in the genre."
- **Pack Nine** (R9-3-*, live): "the manhwa power-panel reference Isaac supplied"; the Berserk density / Vinland restraint split (retired by Pack Eleven and R53-28, still cited in the Visual Aesthetic Guide §4a).
- **Pack Eleven §1**: Berserk / Vinland North Star retired; reference triangle (superseded): Warhammer 40,000 for bureaucracy, late-Victorian industrial imperialism for texture, manhwa for power display.
- **Pack Twelve §2, §4** (live): Technical Register "is Naruto"; Mystic Register "is Lord of the Mysteries"; voice two "the Kakashi model"; voice four "the LotM model"; ritual's bill of goods "is LotM's actual engine"; R12-A cites Naruto's unexplained chakra origin (ruled against).
- **Pack Thirteen §6, §7** (live): Nen, Naruto, JJK, Bleach as author-only shape vocabulary; research "the nearest anime or CRP precedent".
- **R14-B** (ruled 2026-09-12): Sub-Stats spoken "like how people talk about stats in LitRPGs like Unbound."
- **R53-28** (live): "Lord of the Mysteries and Victorian imperial-age fantasy"; Berserk and Vinland retired "everywhere".
- **NATALIE.md, WHO NATALIE IS**: "Eastern skeleton (sixteen Stages, sixty Wellsprings, the Codex, the Design Chain, the Fracture of Worlds stat system) under Western flesh (Martin's POV discipline, Abercrombie's brutality, Tolkien's elegiac reach, Naruto's tactical read, Lord of the Mysteries' mystic register)". Note: NATALIE moves Naruto and LotM into the flesh, where Pack Five kept the Eastern half to the skeleton.
- **NATALIE.md Pack Eleven line**: "Look: Lord of the Mysteries / Victorian imperial fantasy, never Berserk or Vinland (R53-28)."
- **Master Style Directive** (2026-09-12 ed.) §1 "PROSE LINEAGE: WESTERN FLESH, EASTERN SKELETON"; §3 the Western foil pairs; §9.2 anime shape-vocabulary; §14 the Manhwa Energy Directive "deliberately excluded".
- **Dialogue Craft Standards** (2026-09-12 ed.) §3.H "LitRPG/system text stays minimal and earned"; §3.I "Light novel / published-book admissibility check".
- **Combat Craft Guide 3e**: HEMA (Liechtenauer, Fiore) for Blade Grammar; Sodoku's Shinken-ryū for Verdict Grammar.
- **R23-10** and the Naming Guide Amendment: the wuxia register named as a thing to avoid.
- **CRP.docx** (`~/wotr-vault/true-canon/`, the original house style): "battle as a ritual; conversation as a small metaphysical negotiation; travel as a pilgrimage"; "The narration must not read like a glossary, combat log, wiki entry, or system breakdown"; and "ranged characters shouldn't spam shots like anime machine guns".

## Open docket items and CONFLICTS rows touching prose style

The index docket is empty (`out/docket.md`: "0 outstanding"). Touching style:
- **C-124** (open): Pressure is counted in Stage gaps, but a person with no Stage has no gap; canon gives only the Grade-keyed Aura table and "felt as dread" (NATALIE Magic Frame against Fracture of Worlds Part Eleven and R53-14). Bears on how Pressure is shown to commoners on the page.
- **C-118** (open): Doyun, a Korean-stratum boy, is spelled without a hyphen, which R23-10 reads as a Chinese-stratum name. Bears on Korean naming in prose.
- **C-152** (open): "turn" means fourteen days on the Sky page and six seconds in Fracture of Worlds VII. Bears on in-world time words in narration (R51-08 makes "turn" a culture's week).
- **docket/questions.jsonl, WAR-162** (open, outside the index): whether the em-dash ban covers system-page documentation.
- Closed but load-bearing: **C-001** (proofed round explanation; ruled "Eleven's ban stands" on 2026-09-12, then superseded by R53-05: "the old firearm ban on explaining why a proofed round beats proofed plate is superseded"; NATALIE.md still cites the ban, stale). **C-003** (Twelve wins: a sentence may explain why a working worked). **C-007**, **C-015** (narration register and distance are two axes, R41-1). **C-008** (no NPC italic thought under a POV lock, R39-7). **C-090** (ozone, R57-30). **C-091** (numinous, R57-31). **C-111** (Latin is not the authorization; R62-8).

## Stale or self-contradicting places the questionnaire should fix while it is open

- NATALIE.md: Table Rule 2 length bands and "Length discipline" (vs R48-28, R49-30); Table Rule 5 Sub-Stat names (vs R49-47, R51-16); Table Rule 6 "never narration on its own authority" (vs R49-43); Table Rule 8 quotas (vs R49-11); Table Rule 10 NPC thought (vs R48-40); Magic Frame "names only in a mouth" (vs R49-47); Pack Eleven line on C-001 (vs R53-05); the "Packs Thirteen and Fourteen are recorded as proposed" caveat (both ratified 2026-09-11); the OPEN DOCKET list (R13-A to F, R14-B to E, R15-A to C all ruled 2026-09-12).
- Index rows still live against later law: R14-4-SUBSTAT_DIAGNOSTIC_ONLY, R10-2-CATEGORY_READ_EXCEPTION, R10-3-EFFECT_PHYSICAL_ONLY, R10-3-UNCHANGED_CONSTRAINTS, R8-26-ONE_RELEASE_PER_SCENE, R6-5-MATERIAL_DENSITY_SURVIVES ("interpreted at zero", vs R12-7-LEGIBILITY_BAN_STRUCK), R6-2-FACULTY_NEVER_SUBJECT (vs R54-21), R19-5-COMPOSURE_BAN (vs R52-06), R12-2-MYSTIC_REGISTER_DEF ("never as physics", vs Pack Fifteen and R48-10).
- Guides: all five base craft guides are 2026-09-12 editions and predate the 2026-09-26 Writing, Prose, Vocabulary, Voice, World Texture and Naming Law. The wotr-write skill references carry the pre-R49-47 narration-leak rule.

## Where the companion guides live

- **Master Style Directive**: `~/wotr-vault/true-canon/WOTR_Master_Style_Directive.md` (base) and `... (2026-09-12 edition).md` (folds Packs One to Sixteen). Outside the repo.
- **Scene Writing Process Guide**: `~/wotr-vault/true-canon/WOTR_Scene_Writing_Process_Guide.md` and its 2026-09-12 edition.
- **AI Writing Tells to Avoid**: `~/wotr-vault/true-canon/WOTR_AI_Writing_Tells_to_Avoid.md` and its 2026-09-12 edition; a differing "Second edition" copy sits in the repo at `scenes/WOTR_AI_Writing_Tells_to_Avoid.md`.
- **Dialogue Craft Standards**: `~/wotr-vault/true-canon/WOTR_Dialogue_Craft_Standards.md` and its 2026-09-12 edition (folds Pack Nineteen).
- **Visual Aesthetic Guide**: `~/wotr-vault/true-canon/WOTR_Visual_Aesthetic_Guide.md` and its 2026-09-12 edition (folds Packs Nine and Eleven, Moto material culture).
- **CRP.docx** (the original house style the Dialogue Standards quote): `~/wotr-vault/true-canon/CRP.docx`.
- In the repo: `desktop/WOTR_Manual_Verification_Guide (2026-09-26 edition).md`, `desktop/WOTR_Combat_Craft_Guide (2026-09-26 edition).md`, `desktop/NATALIE.md`, `desktop/inventories/`, and the approved narration registers as drafts in `imports/drafts/` (`moto-`, `bram-greymane-`, `lorn-stark-narration-register.md`).
- None of the five craft guides is in `wiki/`, `vault/`, `docs/`, `imports/` or `sources/`.
