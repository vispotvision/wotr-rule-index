# The current WOTR style law, mapped for the style questionnaire

Research note for the Western / Eastern / LitRPG style questionnaire, 2026-10-03. Read in full: rules/doc-prose-law (R49), doc-writing-law (R48), doc-vocabulary-law (R51), doc-voice-law (R52), doc-world-texture-law (R53), doc-naming-law (R50), doc-combat-society-politics-law (R60, prose-facing parts), all dated 2026-09-26; doc-psychic-distance-registers (R35); build/verify.py. Also read: the 2026-09-26 Manual Verification Guide, the AI Writing Tells guide, RULINGS.md 09-26 to 09-28, and every older live row a 09-26 rule leans on or the blend would hit. Every quote is exact text from Isaac's own files. "Live" means `status: live` in rules/ today.

Each entry gives the **rule id**, a short exact quote, and **verify.py**'s treatment: **FAIL** (the run exits 1; in the Natalie clone the Stop hook blocks the reply), **WARN** (printed, needs a read), **info** (printed, never blocks) or **none** (manual only). Each dimension closes with **Blend collision**: where a Western / Eastern / LitRPG mix hits current law or needs a ruling.

Terms, glossed once:
- **LitRPG**: fiction where a game-like system (levels, stats, skills, status screens) is visible on the page. **Progression fantasy**: the wider family where growth in power is the spine. **Cultivation novels** (Chinese *xianxia*, immortal-hero fantasy; *wuxia*, martial-hero fantasy; Korean *murim*, "the martial world"): progression through realms of inner energy. **System novels**: Korean and Chinese web fiction where a "System" speaks to the hero in boxed messages.
- **Status screen** ("blue box", "system window"): a boxed block of stats or messages set off from the prose. **Diegetic**: existing inside the story world (a gauge the character reads). **Non-diegetic**: shown only to the reader.
- **Free indirect discourse (FID)**: third-person narration that slips into a character's own words and judgements without quote marks. **Psychic distance**: how far the narration stands from the character's mind. **POV lock**: the scene never leaves one viewpoint's head.

---

## 0. The doctrine as written: "Eastern skeleton, Western flesh"

The split Isaac wants to change is law, not only a line in NATALIE.md. It lives in Pack Five and was reaffirmed in Pack Eleven.

- **R5-A-SKELETON_UNCHANGED** (live): "WOTR runs an Eastern skeleton under Western flesh. The skeleton stays exactly as it is." Also: "That systematic density is a light-novel and xianxia inheritance and it is the correct engine for this project."
- **R5-A-FLESH_CHANGES** (live): "Prose register, humour, characterisation method, narration authority and tonal architecture now derive from the Western tradition". **Names Martin, Tolkien, Abercrombie.**
- **R5-E-MARTIN_WINS_RULING** (live): "Martin wins on narration authority. Tolkien's elevated and elegiac register is available, his moral voice is not."
- **R11-1-TONAL_SPINE_UNCHANGED** (live): "Pack Eleven widens what the page may look like. It does not reopen what the page may sound like." Also "The Western Register governs characterisation, humour, and narration authority." (It still says "Temür still does not make jokes", a stale Büri-era name.)
- **R5-B-MANHWA_DIRECTIVE_REPEALED** (live): the old Manhwa Energy Directive's items "should be treated as active tells if they appear in a draft." Pack Five §B lists them: personality vomiting (a character being one trait in every line), reaction shots as characterisation, loud opinions as the default register, bizarre or exaggerated minor NPCs, absurdism beside real stakes, humour as the exception to tone, escalation as a prose-level pacing register.
- **R5-G-TELL_BANK_ADDITIONS** (live): "Add as active tells: declarative characterisation, the reaction-shot cutaway, the comedic beat structure, narrator moral adjudication." **R5-B-DECLARATION_TO_INFERENCE**: "Characterisation moves from declaration to inference."
- **R5-F-LIGHT_NOVEL_KEPT** (live): "The chapter as a hard unit with one clear objective and a hook at close." Plus the legible system as reader pleasure, and "Fast entry. Chapters open inside the situation."
- **R5-F-LIGHT_NOVEL_NOT_KEPT** (**superseded** by R51-16): it banned "Status screens, panels, HUD-style rendering", narrator explanation of the system, the isekai commentary register (wry narrator asides about the world's rules; *isekai* is Japanese "other world" fiction) and sheet vocabulary in prose. **The explicit ban on status screens is gone, and nothing licenses them.** That gap is the first LitRPG question.
- **R13-6-ANIME_GRAMMAR_TRANSLATION_AID** (live): "Anime grammar as a translation aid, never as page vocabulary."
- **R23-10-CHINESE_PHONOTACTICS** (live): "Avoid the wuxia register the base guide already warns off: no four-syllable given names, no sect-title constructions, no honorific stacking."

**Already Eastern in law.** R12-2-TECHNICAL_REGISTER_DEF: "It is Naruto. It is exhaustive, tactical, and delivered in-fight." R12-2-MYSTIC_REGISTER_DEF: "It is Lord of the Mysteries" (a Chinese web novel, and the visual reference under R53-28). R12-4-VOICE_TWO_SECOND: "The Kakashi model." R12-4-VOICE_FOUR_DOCUMENT: "The LotM model." R9-3-BODY_UNDER_LOAD (manhwa visual grammar): "WOTR is licensed exactly one splash-panel beat per scene, at the display, never twice" (a *splash panel* is a comic's full-page image at the big moment). R8-24-RELEASE_MECHANIC, the named attack: "An art with a true name may carry a call: an imperative verb plus the name." R51-21: Japanese honorifics in Moto speech. And Isaac's 2026-09-12 ruling on R14-B: "They can be named, but do it like how people talk about stats in LitRPGs like Unbound."

**Blend collision:** a new law has to rewrite or retire R5-A-FLESH_CHANGES, R5-E-MARTIN_WINS_RULING and R11-1-TONAL_SPINE_UNCHANGED, and decide item by item whether the R5-B and R5-G tells stay tells. Every collision below hangs off those rows.

---

## 1. Narrative voice and narrator stance

- **R5-E-NARRATION_NEVER_ADJUDICATES** (live): "Third-person scene narration is POV-locked and never adjudicates." verify: none.
- **R5-C1-NARRATION_NEVER_WINKS** (live): "The narration never winks. No line acknowledging that the reader knows better." verify: none.
- **R49-08-MEANING** (live): the POV may reflect on what a beat meant, but "neutral narrator summaries stay banned." verify: WARN only on a tidy-summary last sentence (Ultimately / In the end / And so / Finally / At last...).
- **R5-E-FREE_INDIRECT_CARVEOUT** (live): "A moral verdict in the POV's own idiom, which could be wrong, is characterisation." The same verdict from the narrator "is Tolkien's voice and gets cut." **R4-13-FID_CARVEOUT**: "Free indirect discourse is not gloss". verify: WARN on seven gloss phrases ("which meant", "in other words"...), read for whose idiom.
- **R48-05-HIGH_STYLE** (live): "High mythic style is allowed freely in narration whenever the moment calls for it". **R49-24-ELEGY**: "at a mythic moment, loss may be sung in full cadence."
- **R51-01-TIMELESS** (live): "plain, undated English by default; some cultures' scenes (Eresse, the Moto court) may take a more antique narration." **R48-13-PERIOD_FEEL**: "Modern words in speech only: characters may talk modern; narration keeps a timeless register." verify: WARN on the modern-word list (§15).
- **Approved, not indexed:** the Moto narration register (imports/drafts/moto-narration-register.md, R51-22, approved to publish in the 09-26 follow-ups). It already reads half-Eastern: verbless sensory fragments, parataxis (clauses side by side with "and", none ranked), everything counted, feeling recorded as absence, judgement closed with "the whole of it".

**Blend collision:** by law the narrator is a Western close-third narrator with no voice of its own. Eastern narrator stances all collide: the Chinese storyteller who addresses the reader and foreshadows (the *zhanghui* chapter-novel, where chapters carry couplet titles and close with "read on to learn what happens"); Lord of the Mysteries' cool asides; the light-novel narrator's commentary; the LitRPG narrator's snark. Each breaks "never winks" and "never adjudicates". Decide: may the narrator have a personality (always, per culture, per document, never), and is "little did he know" foreshadowing legal?

---

## 2. POV and psychic distance

- **R35-1-NARRATION_DISTANCE_BANDS** (live): close, medium ("POV stays with the character and never head-hops") and distant/formal ("An omniscient, epigrammatic narratorial voice describes the character from outside, with only occasional aphoristic italics."). **R35-2** assigns the major cast. verify: none.
- **R49-03-BAND_CAPS** (live): "Lift the per-character depth caps toward deep: every major POV moves closer". **R48-08-NEW_POVS**: "New or minor POVs default to close, deep interior".
- **R49-01-WHOSE_HEAD** (live): roleplay narration may go deep in Isaac's character; "Isaac overrules any thought that isn't his."
- **R49-09-CUTAWAYS** (live): "A turn may close with a short, clearly marked cut to something the POV cannot see". The only licensed break in the lock.
- **R39-7-NO_NPC_THOUGHT_UNDER_POV_LOCK** (live): the NPC-thought carve-out "survives only for scenes with no POV lock (omniscient and mass combat)". So the law knows omniscient scenes exist but sets no rules for them.
- **R1-3-NAME_THREE_RULE** (live): "No more than three characters carry interiority through a battle sequence."
- **R5-C1-WRITE_FROM_LEAST_KNOWING** (live): "write it from whoever knows least about what is coming."

**Blend collision:** wuxia and xianxia often run a roving omniscient camera across a hall or battlefield; Korean system novels are often first person; LitRPG is first person or very tight third with the System as a second voice. "Whoever knows least" fights the Korean regression premise (the hero relives his life knowing the future), where the POV knows most. Decide: omniscience outside mass combat; POV rotation inside a chapter; whether a System voice sits outside the POV lock.

---

## 3. Tense and person

- **R49-02-TENSE** (live): "roleplay turns, and work improved for a roleplay, are written in present tense; written scenes and books are written in past tense." verify: none.
- **Person: no rule.** Question p02 offered "He steps" / "You step" / "He stepped"; the answer set tense only. Third person is practice, not law. R61-9 makes converted in-world texts first person, a document rule.
- The Moto register already drops "into general present tense inside past narration for a law of the world".

**Blend collision:** first person is common in LitRPG, Korean web novels and Japanese light novels. System messages are conventionally present tense inside past narration. Decide: first person (which jobs, which POVs); the tense of a status message in a past-tense chapter; whether the roleplay / book split stands.

---

## 4. Sentence rhythm and paragraphing

- **R48-06-RHYTHM_LAW** (live): "the hit is the shortest sentence and sits last, payoffs under 10 words, at most two long sentences in a row". It says "the checker fails anything else"; verify.py fails only the chain ceiling. Payoff length and position are manual.
- **R4-14-LANDING_RULE** (live): "The emotional hit takes the shortest sentence in its paragraph and sits last." With R4-14-CLAUSE_CAP_AT_BEAT and R4-14-CONJUNCTION_AUDIT. verify: none.
- **R4-14-CHAIN_CEILING** (live): "No more than two consecutive sentences over 25 words." verify: **FAIL**.
- **R4-14-RUN_RULE** (live): "No three consecutive sentences within forty percent of each other's word count." verify: **FAIL** at four such runs; the rule text treats one as a flaw.
- **R49-12-SHORT_FLOOR / R4-14-HARD_CEILINGS** (live): "short sentences cluster at beats and in action so the scene clears 18%." verify: **FAIL** under 10% of sentences under 8 words, **WARN** under 18%; **WARN** on paragraphs closing on three sentences over 18 words.
- **R49-13-VARIANCE** (live): targets 80% sentence-length variation, "under 50% is the strongest tell". (Measured as CV, coefficient of variation: the spread of lengths relative to the average.) verify: **WARN** under 0.50.
- **R48-07-WHITE_SPACE** (live): "Steady paragraphs: medium paragraphs, white space used sparingly so it still means something." **R49-14-PARA_SHAPE**: verify **WARN** when paragraph CV is under 0.35. The AI-tells guide: "A one-line paragraph is allowed to exist."
- **R49-15-FRAGMENTS** (live): "Concrete noun and image fragments are free; negative and 'Only/Just' emphasis fragments stay warned at three per scene." verify: **WARN** at three.
- **R49-23-HIGH_STYLE** (live): "Anaphora and the triad come off the tell list everywhere; always legal." (*Anaphora*: repeated openings across clauses. *Triad*: a three-part list.)

**Blend collision:** the 18% floor, the CV target and the chain ceiling come from AI-detection stylometry, not from any national tradition, and they shape the blend whatever is chosen. Phone-formatted Korean and Chinese web fiction runs on one-line paragraphs: the checker is happy, R48-07 is not. Chinese parallel prose (paired clauses of matched length and grammar, the *duizhang* couplet) makes exactly the even-length runs R4-14-RUN_RULE fails. A climax delivered as one long cumulative sentence breaks the landing rule. Decide: keep the stylometric floors regardless of style; allow web-serial paragraphing; exempt parallel prose and verse from the run rule.

---

## 5. Imagery, metaphor and simile

- **R48-01-BEAUTY** (live): "Beauty comes from exact concrete detail, images and metaphor, and what goes unsaid". verify: none.
- **R49-18-SIMILE_COUNT** (live): "No simile rate or ceiling: only two similes competing over the same beat get flagged." verify: **WARN** on any two simile markers ("like a/an/the", "as if", "as though") in one paragraph, same beat or not.
- **R48-04-METAPHORS** (live): "Metaphors come from the POV's own life: trade, homeland, body; metaphor doubles as characterisation." **R49-19**: extended and stacked metaphors allowed when they come from the POV's life.
- **R49-20-STOCK_PHRASE** (live): "Dead metaphors are always rebuilt from the POV's own life, even when a rough POV would think the cliche." verify: none.
- **R49-21-REIFICATION** (live): no count; only "never at the beat" and "object first". (*Reification*: an abstract noun handled as a thing, "the silence sat between them".) verify: none.
- **R49-22-NATURE** (live): "Avoid personifying weather and landscape: the world is described, not personified." verify: none.
- **R5-C2-ELEGY_CONCRETE_THING** (live): "Elegy attaches to a named concrete thing that is gone." Fed by each Inventory's Gone list (R53-31).
- **R9-3-AURA_AS_FRACTURE** (live): "Aura as fracture, not glow." and "\"It glowed\" stays banned". verify: none.

**Blend collision:** classical Chinese, Japanese and Korean poetics work through shared set images (plum blossom in snow, the autumn moon, the willow at parting) whose force is that they are shared; R49-20 orders every stock image rebuilt. Feeling carried by landscape (Chinese "feeling and scene fused"; Japanese *mono no aware*, the pathos of passing things; *kigo*, the season words of haiku) sits close to R49-22. Cultivation novels' set beauty formulae and glowing qi run into R49-20 and "It glowed". Decide: a per-culture bank of sanctioned set images; whether feeling-in-landscape counts as personification; whether auras may glow.

---

## 6. Description

- **R48-02-DENSITY** (live): "Lush throughout: every scene gets full sensory layering; slower, denser, more immersive." verify: none.
- **R49-28-INTROS** (live): "First introductions get the full physical inventory all at first sight, in one descriptive passage." NATALIE Table Rule 11 sets the inventory (hair by comparison, face, body by area, clothing fit and wear, marks, then a want and a voice). verify: none.
- **R53-30-TEXTURE_DENSITY** (live): "Every beat carries at least one detail that could only exist in this world; sensory layers sit around it." verify: none.
- **R51-31-SENSE_BANK** (live): each Inventory's senses entry; "scenes draw from it first." **R53-23-MIXED_ROOM**: "A mixed room layers every culture present in roughly equal measure."
- **R53-19-QUOTA / R49-54-KHARVEN** (live): two signature items per culture per session. verify: **WARN** with `--culture Kharven` only, per file. **R6-9-RECURRENCE_RULE**: "Identity is repetition. Novelty is its enemy."
- **R53-09** ("every outdoor scene shows the actual weather"), **R53-17** (a working on a main means "somebody notices the cost"), **R60-07** ("Commerce shows on the page as branded goods and advertising").
- **R49-29-TURN_FILL** (live): "about half texture and talk, half the world moving, before the stop at the next decision." **R48-29**: "travel and waiting pass in a line when nothing is at stake".
- **R53-29-LOOK_UP** (live): world facts are looked up; "gaps are flagged, not filled."

**Blend collision:** Isaac wants description to "cover a wide variety of things". The law mandates density, but its required subjects are narrow: senses, bodies at first sight, Inventory items, weather, cost, commerce. Nothing asks for architecture, dress after first sight, cooking, craft processes, landscape at scale, cosmology, treasures or the spectacle of power. Cultivation novels lavish description on treasures, sect grounds, beauty and power display; LitRPG on loot, gear and the inventory screen; light novels describe lightly and move on. Decide: a subject list or rotation; whether density varies by mode (a LitRPG fight lighter on senses, heavier on mechanics); whether item and loot description with stats counts as description.

---

## 7. Exposition and the iceberg

- **NATALIE.md Prose Standards** (no index id): "Iceberg: reader sees ten percent. No \"as you know.\"" Exposition through disagreement, negotiation or a real knowledge gap.
- **R48-25-AWE** (live): "Clarity everywhere: scenes explain Wellsprings, rites, oaths and the Veil as plainly as a sword exchange." **R49-43-EXPLAINING**: "Narration may explain causes anywhere, in the POV's reasoning and vocabulary". verify: none.
- **R51-15-FIRST_USE** (live): "New WOTR terms get meaning from context and use only; no appositive gloss (the zero gloss budget stands)." **R4-13-ZERO_BUDGET**: "Zero glosses per scene. Not rationed. There is no acceptable first instance." verify: **WARN** on the seven gloss phrases.
- **R51-14-NEW_TERMS** (live): "No ceiling on WOTR terms per page; readers learn by immersion." **R8-26-GLOSS_DEPENDENCE_FAILS**: a working that needs a gloss "is a working that failed."
- **R53-15-FOLK_BELIEFS** (live): folk beliefs stand and "the narration never corrects them." **R49-11**: not-knowing quotas optional. **R48-48** (out of scene): the partner explains physics "only when asked".

**Blend collision:** the law now permits causal explanation but forbids the glossary sentence. LitRPG exposition is mostly glossary: a skill tooltip, a tutorial, the System defining a stat. Cultivation novels use the elder's lecture on the realm ladder; Korean system novels have the hero explain what he knows from the "original novel". All are appositive gloss under R51-15 and R4-13. Decide: is there a sanctioned exposition channel (System text, tooltip, elder's lecture, chapter-head document) exempt from the zero-gloss budget, and how much of the ten-percent iceberg survives?

---

## 8. Dialogue and speech register

- **R49-31-TAGS** (live): "Dialogue is mostly untagged: voices sort themselves; tags only when needed." **R49-32**: interruption by ellipsis, since em dashes are banned in speech too (verify **FAIL**).
- **R52-02-VOICE_LEVER** (live): "A voice is mind and sound in equal measure". **R52-03** voice block; **R52-07** swap test by ear. verify: none.
- **R48-43-SPEECHES** (live): "a trained speaker may deliver one crafted, eloquent speech at a big moment." **R52-06-TRIADS**: "Triads and parallel clauses are legal in any mouth, under duress included" (C-077 ruled for this on 09-27).
- **R51-21-MOTO_WORDS** (live): "Moto and other Japonic houses use Japanese honorifics and address forms in speech, in a feudal register, never modern casual." Nothing equivalent for the Korean or Chinese strata. **R52-21**: "Kwon Mu-jin never uses his rank or the old court honorifics to win an argument".
- **R48-41-MAGIC_TALK** (live): "a Measurewright in gauges, a hunter in folk words, a scholar in theory." **R52-05-COUNTING**: exact numbers belong to Lambert, Measurewrights, clerks and instrument readers; "everyone else rounds, guesses or doesn't count."
- **R52-30-PROVERBS** (live): "Every NPC carries one fixed saying from the Standing Inventory".
- **R50-09** (live): "No limit on release calls". **R8-26-NO_SELF_TRANSLATION** (live): "Nobody translates their own technique aloud. Ever."
- verify on speech: em dash, antithesis and hard-ban words **FAIL**; calendar and holy-swear **WARN**; modern words free.

**Blend collision:** honorifics are ruled only for the Japonic register; Korean speech levels and titles and Chinese sect address (Senior Brother, Elder, humble self-reference) have no rule, and R23-10 bans honorific stacking in Chinese names. Stat banter in a mouth is already legal and was asked for (the Unbound ruling), but R52-05 limits exact numbers to a few owners, which cuts against a party arguing builds. The antithesis FAIL applies inside speech, so a rhetorical "not this, but that" couplet fails in a character's mouth. Decide: honorific rules for Korean and Chinese strata; who may talk numbers; whether rhetorical antithesis in speech is exempt.

---

## 9. Interiority and italic thoughts

- **R48-39-INTERIORITY** (live): "POV interiority is deep and running: thoughts, memories and reasoning flow through the narration." **R49-06**: "Memories may run as full flashbacks, a page or more when they matter."
- **R49-05-ITALICS** (live): "Italic direct thought appears often, whenever the POV talks to himself; more voice." verify: info only (a count of italic spans; the line still cites the superseded "one per named NPC").
- **R48-40-NPC_THOUGHTS** (live): "roleplay turns keep the one-thought-per-NPC allowance; written scenes keep the POV lock (no NPC thoughts under a lock)." verify: none.
- **R49-07-EMOTIONS** (live): "Emotion: show it in the body first; the POV may then name it in his own word." verify: **WARN** on signposting ("he felt afraid", "a wave of relief").
- **R49-41-QUESTIONS** (live): "Every question in narration keeps getting flagged for a read as possible hypophora." (*Hypophora*: asking a question to answer it.) verify: **WARN** on every unquoted question, italic thought included.
- **R16-8-CHECK33** (live): "Fewer than half of a scene's technical terms sit inside italic thought". verify: none.
- Italics are forbidden for foreign words (R49-49, R50-32), so italic means thought or emphasis only.

**Blend collision:** LitRPG and Korean web-novel heroes think in a running, joking, modern idiom ("min-maxing", "aggro", "a broken build"). verify.py strips only quoted speech before the modern-word check, so a listed modern word in italic thought WARNs, and R48-13 keeps thought timeless. A System voice needs its own typography (brackets, bold, a box) or it collides with italic thought. Decide: may thought run modern or gamer idiom; how System text is marked; how freely the POV may question himself.

---

## 10. Humour and tone

- **R48-11-HUMOUR** (live): "Humour wherever it's earned: funny characters are funny often; tone flexes with the cast." **R49-38**: funeral test dropped for comic voices. **R52-31**: comic minor NPCs "with no setup-deadpan-reaction beat".
- **R5-D-HUMOUR_BARRED** (live): "Barred: the beat structure of setup, deadpan and reaction." verify: none. **R5-D-HUMOUR_PERMITTED**: "dry understatement, gallows wit from people whose profession earns it, class-inflected contempt" and more.
- **R52-14**: "Sodoku makes jokes only by accident". **R5-B** tells: bizarre minor NPCs; absurdism beside stakes.
- **NATALIE.md** Grimdark: "victories cost. Moral ambiguity over clarity. Hope is small and hard-won." **R48-31**: "Death can happen, if earned". **R60-01**: "most fights end in the first seconds; a wounded man is out of the fight."
- **R48-36** (live): NPCs are veteran-clever, "never omniscient, never dumb." **R5-C1-WELL_REASONED_WRONG_CONCLUSION**: "Irony built on a character being stupid is not irony."

**Blend collision:** the Japanese comic double act (*tsukkomi*, the straight man's retort to the fool's *boke*) and the manhwa gag beat are the setup-deadpan-reaction shape R5-D bars. Chinese web fiction's core pleasure, *shuang* (the gratifying payoff when the underestimated hero humbles an arrogant enemy, "face-slapping"), needs arrogant fools that R48-36 and R5-C1 rule out. Progression fantasy is an optimistic climb; grimdark says hope is small. Decide: setup-reaction comedy; the face-slap and on what terms; how much grimdark survives a progression engine.

---

## 11. Combat on the page

- **R48-33-CHOREOGRAPHY** (live): "Duels: every exchange traced (measure, guard and the move by its fencing name)." **R13-6-HEMA_VOCAB**: "HEMA, extended past the longsword" (*HEMA*: Historical European Martial Arts, the reconstructed medieval and Renaissance fencing systems). verify: with `--combat`, **WARN** on zero terms from a German and English list (Vor, Nach, Indes, Zornhau, bind, measure, guard, parry...).
- **R13-4-COMBAT_FLOOR** (live): every meaningful exchange "puts the following on the page, stated, in one of the four voices": measure, tempo (Vor/Nach/Indes: German fencing terms for before, after and during, who holds the initiative), the read, the fault, the hit, the injury by structure with ATLS-class blood loss (*ATLS*: the trauma-medicine scale of haemorrhage), the three-strata Essence account, what the fighter cannot do next. verify: none.
- **R48-34-WOUNDS** (live): "full clinical gore, anatomy named, blood loss tracked minute by minute, nothing looked away from." verify: with `--combat`, **WARN** on zero anatomy terms.
- **R60-03**: "long fights are won by whoever manages the reserve"; **R47-11**: "One combat turn is six seconds." Plus R48-37 (cost in the body), R48-38 (aftermath).
- **R12-4-VOICE_MIXING_RULE** (live): of the four explaining voices, "Do not run more than two in one engagement." **R12-4-VOICE_THREE_OPPONENT**: the gloating opponent is "barred to anyone who does not have the standing to be arrogant."
- **R12-3-NAMED_INVENTOR_RULE** (live): "A self-derived technique must be read live, in the two or three exchanges before it kills you".
- **R13-6-SCALING_VOCAB_RESTRICTED** (live): powerscaling words (Attack Potency, hax, speed blitz) are "author-notes and adjudication only, never on the page".
- **R9-3** (live): the eyes go first at a Stage display, "Rendered as a fact the room reacts to"; one splash-panel beat per scene.

**Blend collision:** the duel standard is European by name. A Moto swordsman fought in Japanese terms (*kamae*, stance; *ma-ai*, fighting distance; *sen no sen*, taking the initiative as the enemy commits) or a lineage-hall boxer in Chinese forms draws a zero-HEMA WARN and fails R13-4's Vor/Nach/Indes wording. Wuxia stages named forms in sequence with crowd and elder commentary and instant verdicts from a realm gap; LitRPG shows damage numbers, health bars, cooldowns, skill notifications; shōnen fights escalate over chapters. WOTR has one-cut lethality, six-second turns, a hard reserve clock, two explaining voices at most and the reaction shot as a tell. Decide: per-culture combat vocabularies (and checker lists); bystander commentary in fights; reserve and damage as numbers; long escalating duels beside R60-01.

---

## 12. Magic and the system on the page (the LitRPG hinge)

**Already free.**
- **R49-47-STAT_WORDS** (live): "All free: narration may state stat names, Grades, Stages, eta, EU figures and Guild words on its own authority." It superseded R14-4-EFFECTS_CHANNEL, R14-4-DIAGNOSTIC_CHANNEL, R12-5-NUMBERS_DIAGNOSTIC_ONLY and the old narration-leak FAIL (R14-6-CHECK28). verify: none; nothing checks stat words now.
- **R51-16-OLD_BANS_FALL** (live): "All older limits on stat names, Sub-Stat names, Guild words and sheet vocabulary in narration fall; they are free in narration." **R51-17**: "mechanism terms may be bare mid-action; the reader keeps up." Also R48-09 (technical words), R48-21 (Wellspring and glyph names), R48-10 (registers mix), R49-48 (technique names).

**Still framing it.**
- **R48-20-STRATA** (live): "The three-layer account (Aether, Wellspring, Essence) shows at a working's first display and at the finisher; lighter touches between." **R48-37**: cost in the body. **R53-17**: the meter notices.
- **R12-5-NEVER_INVENT_NUMBER** (live): "Never invent a number. Unchanged and absolute." **R14-6-NUMBERS_GREP**: a figure not in Fracture of Worlds "is marked estimate." **R14-6-CHECK29**: a Stat Ledger in the notes for every named practitioner. verify: none.
- **R49-52-MEASURES** (live): "exact minutes and figures come from a trained eye, an instrument, or the notes." **R48-16**: "anyone with an instrument or trained eye states figures as often as they would."
- **R53-14-FOLK_KNOWLEDGE** (live): ordinary people "could not name a Stage and use folk words." **R53-18**: "a ranked practitioner is half a saint to ordinary people."
- **R47-7-NAMES_NOT_NUMBERS** (live): "Tiers of standing and ladder rungs are written by name only, never as numbers." **R47-1**: an entry describes "what the ability is, never how to use it". **R57-26**: usage lines stripped from published write-ups, numbers kept.
- **R10-3** (live): a working may render as "an externalized shape" (beast, guardian), but "Never why the Wellspring resolved as a tiger and not a wolf" on the page. **R12-6-RITUAL_SPECIFICATION**: "A rite has a bill of goods, an order of operations, and a list of ways it goes wrong". **R48-22**: real idea-names (Stoic pneuma, solve et coagula) "may appear anywhere they fit, scenes included."

**Live leftovers that contradict the freedom.** R14-4-SUBSTAT_DIAGNOSTIC_ONLY is still live: "Sub-Stat names are diagnostic-only." (R51-16 superseded R20C-31, not this row.) R13-6-SCALING_VOCAB_RESTRICTED still keeps powerscaling talk off the page. NATALIE.md lags the index: the Magic Frame still says "names only in a mouth, an instrument, a document, or a private count", and Table Rule 5 says Sub-Stat talk goes "in a mouth, never in narration". R49-52 and R49-47 disagree on who may state a figure; no conflict row logged.

**Blend collision:** the words and numbers are already legal; LitRPG adds form and frequency. The questionnaire must put: (a) whether status screens exist, and whether they are diegetic (a Guild identity plate, a Measurewright's gauge, a Crystal registration card, a faculty reading) or a non-diegetic System; (b) who sees them (everyone, practitioners, the POV, the reader only); (c) which fields show (Level, Band, Stage, Grades, Sub-Stats, EU and AU/s, Traits, eta) and how precisely, given that R12-5 and R14-6 make every figure on the page a sourced one; (d) level-up and breakthrough beats: notification, splash-panel display or both, and whether the one-splash-panel cap stands; (e) skill descriptions on the page, against R47-1 and R47-7; (f) cultivation words (qi, dantian, meridians, tribulation) as lens names under R48-22, or kept out under R13-6-ANIME_GRAMMAR; (g) whether commoners' ignorance of the ladder (R53-14) survives visible numbers.

---

## 13. Names, epithets and titles in narration

- **R48-44-NAME_USE** (live): "Narration refers to characters by POV epithets, the way the viewpoint sees them; the naming characterises." **R49-10-EPITHETS**: "One epithet per character per scene: the POV's epithet changes only when the POV's view of them changes". verify: none.
- **R50-27**: a newcomer is "a role (the gate-clerk) until they speak twice or matter". **R50-21**: "The partner may coin a Third Name for one of Isaac's characters through an NPC in a scene" (the world's title for a practitioner).
- **R50-10**: "plain English names for common-tongue fighters, true names for houses with a register." **R50-11**: "New English technique names are short: two words at most, no stacked modifiers." **R50-14**: escalation by suffix "(Kurosetsu becomes Kurosetsu-Kai)". **R8-23**: "An art is spoken once at release and thereafter assumed."
- **R50-31**: "True names are romanised only: no real script (kanji, hangul) on cards, pages or prose." **R49-49 / R50-32**: foreign words and names never italic. **R50-15**: diacritics kept.
- **R23-10** (live): no four-syllable given names, sect-title constructions or honorific stacking in the Chinese stratum.

**Blend collision:** Chinese web fiction rotates descriptive epithets inside a scene ("the youth", "the grey-robed elder") where R49-10 allows one. Sect titles, honorific stacks and grand sobriquets are core cultivation texture, banned for the Chinese stratum by R23-10. LitRPG marks skills and classes typographically ("[Blade Dance]"); nothing covers brackets. Long xianxia-style technique names collide with R50-11. Decide: epithet freedom; whether R23-10 relaxes for sect and hall titles; bracket typography; whether the two-word cap binds translated true names.

---

## 14. Scene structure, openings, endings and length

- **R49-25-OPENINGS** (live): "Openings vary by scene: arrivals open on the senses; tense scenes open in motion." **R1-3** (live): "layered sensory opening". **R5-F-LIGHT_NOVEL_KEPT**: "Chapters open inside the situation." verify: none.
- **R49-26-ENDINGS** (live): "Written scenes may end on an action, a concrete image, or a line of dialogue; never a summary or a question." verify: **WARN** on a tidy-summary close; info prints the last line (pre-R49-26 wording). NATALIE Table Rule 1: a turn stops at the PC's next decision.
- **R49-27-SCENE_BREAKS** (live): a real jump "may be marked with a blank-line break or ornament." R1-3 still lists "no section spacers"; R49-27 supersedes nothing.
- **R49-30** (live): "Every reply is a full turn of about 3,500 words, even to a quick line or question." **R48-46**: set pieces "5,000+". verify: **WARN** outside 2,500 to 4,500, or under 5,000 for a set piece. NATALIE Table Rule 2's 300 to 1,500 bands are stale.
- **R48-30**: surprises "only after foreshadowing a player could have caught." **R48-38 / R1-3**: aftermath beats; for battles "plan the aftermath first".
- **R5-B** (live tell): "Escalation as a prose-level pacing register. It survives as plot architecture only".

**Blend collision:** *kishōtenketsu* (a four-part shape from Chinese and Japanese poetics: set-up, development, twist, reconciliation, with no central conflict required) has no place in a law of value turns, hooks and stops at a decision. Web serials run 2,000 to 3,000-word chapters ending on cliffhangers, often a notification or reveal. Genre arc shapes (tournament, dungeon floor, sect examination, training montage) are untouched except by R48-29's skip of dull stretches. Decide: chapter length and hook rules for book mode; endings on a system message or reveal line; kishōtenketsu chapters; escalation as prose pacing.

---

## 15. Banned constructions and banned words

**FAIL:** em dashes (also "--" and en dashes): R15-1-AI_TELL_CHECKS_SURVIVE ("These are about prose failing, not about period."), R48-03. Antithesis, R49-40-NOT_X_Y: "any pair where the second sentence corrects the first fails; plain negation standing alone is free" (the regex also fails "he was more X than Y"; speech included). Countdown negation (short negations resolving into "Just" or "Only"). The Ladder twice in a sentence, R6-1-LADDER_BAN ("X was Y and the Y was Z"): "an automatic cut, never a rewrite." Hard-ban list, R51-10-SLOP_WORDS (tapestry, testament, palpable, visceral, symphony of, a dance of, whisper of, orbs, ministrations, electric touch, velvet voice, shiver down the spine, the held breath, coppery tang, the smell of ozone): "each fails the checker at first use, narration and dialogue." Rhythm FAILs as §4.

**WARN:** one Ladder; three emphasis fragments; faculty as grammatical subject, R6-2-FACULTY_NEVER_SUBJECT ("The character perceives. The apparatus does not act on its own behalf."); gloss phrases; signposting; any narration question; two simile markers in a paragraph; tidy close; three "-ing" / "As he..." openers; filter verbs ("he saw", "she felt") above 5 per 1,000 narration words (R49-42; the 5 is the checker's own number); the modern list in narration (okay, OK, vibe, awesome, cool, teenager, triggered, toxic, closure, mindset, boundaries: R51-03, R51-04); Earth day and month names and "weekend" (R51-08); Earth holy swears (R51-30).

**Manual only:** the tic-word list (R49-55, thirty words such as "precisely", "suddenly"); collision words (R51-11: delve, echo, numinous, sovereign, sanctum, weave, ledger; "the plain adjective or verb is banned so the term stays sharp"); "rather than"; reification at the beat; structural signposting; the profundity pivot. R51-06 makes Earth-derived words (herculean, Achilles heel) legal; R51-05 allows technology metaphors only where the POV's culture has the thing.

**Blend collision:** most of this list is anti-machine hygiene and style-neutral. Three items are not: the faculty-subject rule forbids the *dōjutsu* convention (Japanese "eye technique" fiction, where the eye itself sees), though WOTR's faculties carry Japanese names (Kamigan, Shingan, Ketsumyōgan); the question WARN catches the Chinese storyteller's rhetorical question; the em dash ban removes the manga and manhwa cut-off shout (ellipses only). "Level up" and game words like "cooldown" are not banned anywhere; only the short modern list WARNs.

---

## 16. Documents and in-world texts

- **R12-4-VOICE_FOUR_DOCUMENT** (live): "An in-world register entry, field manual, or codex line dropped into the narrative at the threshold of a scene." It "Sets a rule the scene then breaks." Explicitly the Lord of the Mysteries model.
- **R51-33-DOC_REGISTER** (live): "In-world documents keep a house style per institution" (Accord chancery Latinate, Dawi Tally terse, Moto records in the old register, letters in the writer's voice).
- **R51-34-DOC_MODERN** (live): "documents are timeless and the checker runs the list on them." verify has no document flag; a `>` block is checked for bans but left out of rhythm statistics.
- **R51-28-CHANT_PAGE** (live): "A chant appears in its own language; a POV who understands it may think the meaning in his own words."
- No rule covers verse inside prose, epigraphs, or chapter-head documents beyond the threshold voice.

**Blend collision:** the document voice is the natural legal home for a LitRPG status screen: an in-world instrument read at a scene's threshold, in a Guild house style, timeless and checked. A non-diegetic System would be a fifth explaining voice the law does not have, and R12-4's two-voice cap would need a ruling. Eastern prose inserts verse at peaks: the chapter-novel's poems and couplets, the Japanese *waka* (31-syllable court poem) and haiku, the Korean *sijo* (three-line verse). None is ruled on; verse in prose paragraphs is currently checked as prose. Decide: verse inserts and epigraphs; whether System text is a document; whether documents may gloss.

---

## 17. Enforcement: what verify.py sees

**What runs.** `build/verify.py draft.md [--combat] [--culture Kharven] [--band standard|conversational|set-piece] [--echoes]`, also the MCP's `verify_scene`. R48-45: "every turn passes the full checker." In ~/wotr-natalie the Stop hook runs it on every reply over 120 words and blocks on any FAIL.

**What it reads.** Everything below the first `## Notes` heading is cut; headings and `---` stripped; bold unwrapped. Paragraphs opening `>` or `|` are out of the sentence, paragraph and word-count statistics but still face the bans. Quoted speech is stripped only for the opener, filter-verb and modern-word checks. Italics are never stripped. Code fences are not recognised and read as prose.

**FAIL and WARN:** as listed in §4 and §15, plus the length band WARN (2,500 to 4,500, or 5,000+ for `--band set-piece`), the Kharven item count (`--culture`), zero HEMA or anatomy terms (`--combat`), and `--echoes` (one word four times in 60).

**Manual only:** payoff rules and the conjunction audit, tic words, reification, collision words, foreign italics, signature items for any culture but Kharven, the combat floor beyond two zero-counts, term spelling (wotr_terms.txt does not exist), the Stat Ledger, voice and swap, psychic distance, value turn, the world-only detail per beat, NPC thought limits, dialogue fidelity and composure.

**What LitRPG material would do to it today.** A status screen as a `|` table or `>` block passes the rhythm checks and is left out of the word count; its words still face the bans. In a code fence it becomes one long unpunctuated "sentence" that can trip the chain ceiling and lower the short-sentence share. Bracketed skill names and numbers trip nothing. A one-line notification ("Level 41.") counts as a short sentence and helps the 18% floor. Listed modern words in italic thought WARN; in speech they pass. No check knows stat words or figures, so R12-5 and R14-6-NUMBERS_GREP stay manual, and a numbers-heavy style multiplies that load. The `--combat` list is European, so an Eastern-vocabulary fight WARNs.

Tool gaps on record are listed in §18 D11.

---

## 18. Flag index

**A. Rules naming a Western model or doctrine:** R5-A-FLESH_CHANGES (Martin, Tolkien, Abercrombie); R5-E-MARTIN_WINS_RULING; R5-E-FREE_INDIRECT_CARVEOUT ("Tolkien's voice and gets cut"); R5-C1-WELL_REASONED_WRONG_CONCLUSION (Martin's Ned Stark as model); R5-B-DECLARATION_TO_INFERENCE (source example from Martin); R5-B-FOIL_FUNCTION_SURVIVES ("It was never Eastern"; source pairs from Tolkien, Martin, Abercrombie); R11-1-TONAL_SPINE_UNCHANGED ("The Western Register governs..."); R13-6-HEMA_VOCAB, R48-33-CHOREOGRAPHY, R13-4-COMBAT_FLOOR (European fencing vocabulary as the standard); NATALIE.md's "Western flesh" line.

**B. Rules that forbid or restrict a common Eastern or LitRPG technique** (checker severity in brackets; detail in the dimension cited):
- Bystander reaction shots: R5-G, R5-B [none]; contradicted by R4-13-WHERE_SIGNIFICANCE_LIVES, R9-3-EYES_AS_TELL, R53-18 (§11).
- Named attacks: legal (R8-24, R50-09) but R8-26-ONE_RELEASE_PER_SCENE still live; R8-26-NO_SELF_TRANSLATION [none] (§8, §13).
- Narrator asides, storyteller voice, foreshadowing: R5-C1, R5-E, R49-08 [tidy-close WARN] (§1).
- Omniscient roving narration and head-hopping: R5-E, R35-1, R48-40 [none] (§2).
- Narrator proverbs and aphorisms: R49-08, R4-13 [gloss WARN] (§1, §7).
- Verse inserts, epigraphs: unruled, checked as prose (§16).
- One-line web-serial paragraphing: R48-07 [checker indifferent] (§4).
- Status screens, System text, visible numbers: unlicensed; R12-5, R14-6, R47-7, R52-05, R53-14, R14-4-SUBSTAT_DIAGNOSTIC_ONLY [none] (§12).
- Tooltip and lecture exposition: R51-15, R4-13-ZERO_BUDGET [WARN] (§7).
- Tsukkomi and gag beats: R5-D-HUMOUR_BARRED, R52-31; face-slapping fools: R48-36, R5-C1, R12-4 [none] (§10).
- Exaggerated NPCs, loud opinions, prose escalation, absurdism: R5-B [none] (§0, §14).
- Shared set imagery, landscape feeling, glowing auras: R49-20, R49-22, R9-3 [none] (§5).
- Sect titles, honorific stacks, rotating epithets, long technique names: R23-10, R49-10, R50-11 [none] (§13).
- Eye-as-subject grammar, rhetorical narration questions: R6-2, R49-41 [WARN] (§15).
- Rhetorical antithesis, parallel couplets: R49-40 [FAIL, speech included], R4-14-RUN_RULE [FAIL at four] (§4, §8).
- Anime or cultivation vocabulary, powerscaling talk: R13-6-ANIME_GRAMMAR, R13-6-SCALING [none] (§12).
- Gamer idiom in narration or thought: R48-13, R51-03 to R51-05 [WARN, short list] (§9).
- Dash shouts and stammers: R48-03, R15-1 [FAIL] (§15).
- Eastern fencing vocabulary: R48-33, R13-4, R13-6 [zero-HEMA WARN] (§11).
- First person: unruled (§3).

**C. Rules that already favour the blend:** the "Already Eastern in law" list in §0, plus R49-47, R51-16, R51-17 (stat words, figures and bare jargon free in narration), R48-05 and R49-24 (mythic high style), R49-23 and R52-06 (anaphora, triads, parallel clauses), R49-05 and R49-06 (frequent italic thought, long flashbacks), R53-25 and R53-27 (real object names; blend real cultures freely), R48-22 and R51-06 (real idea-names, Earth-derived words), R50-21 and R50-14 (Third Names, escalation suffixes), and the approved Moto narration register.

**D. Stale or contradictory rows to clean up in the same pass:**
1. NATALIE.md Magic Frame and Table Rule 5 keep stat names out of narration; R49-47 and R51-16 freed them.
2. NATALIE.md Table Rule 2's length bands vs R48-28 and R49-30.
3. R14-4-SUBSTAT_DIAGNOSTIC_ONLY (live) vs R51-16.
4. R8-26-ONE_RELEASE_PER_SCENE (live) vs R50-09.
5. R1-3-SCENE_STANDARDS_DEFINED still lists "no section spacers" and one NPC thought each; R49-27 and R48-40 / R39-7 govern.
6. R49-52-MEASURES vs R49-47-STAT_WORDS on who may state figures.
7. R11-1-TONAL_SPINE_UNCHANGED names "Temür" (stale Büri name).
8. R9-3-COST_UNCHANGED and R10-3-UNCHANGED_CONSTRAINTS lean on the ignorance quota (optional since R49-11) and the one-read Apparatus Rule (struck by R12-1 and R12-7).
9. R12-4-VOICE_MIXING_RULE's two-voice cap: with R16-5-VOICES_VS_VOCABULARY superseded and R49-43 letting narration explain causes anywhere, what the cap still counts is unclear.
10. R4-13-WHERE_SIGNIFICANCE_LIVES (reaction as a carrier) vs R5-G (reaction-shot cutaway as a tell).
11. verify.py: the italic info line cites "one per named NPC" and the last-line text predates R49-26; R48-06 says the checker fails payoffs and it does not; R4-14-RUN_RULE makes one flat run a flaw while the checker fails at four; signature items are checked per file though the rule is per session.
