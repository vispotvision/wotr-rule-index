# The Alftian Codex, Volume I (Mu-jin edition): rules digest

Loaded 2026-09-28. `load_rules` for prose-law, documents, register, pov, naming, magic-mechanism, worldbuilding and standing-inventory; `check_docket` for the same eight tags, which returned 0 pending and 0 proposed. The R61 alchemy-conversion rulings (RULINGS.md, 2026-09-28, the 131 answers) are live but missing from the MCP's `load_rules` index, which predates them. They were read from `out/rules.resolved.json` and confirmed with the `rule` tool. The references read were `.claude/skills/wotr-write/references/prose-law-quickcheck.md` and `fair-play.md`, `desktop/WOTR_Manual_Verification_Guide (2026-09-26 edition).md`, `desktop/NATALIE.md`, the Ketsuen Standing Inventory, Kwon Mu-jin's card (voice block) and `build/verify.py` itself.

The job is about 7,000 words. It is Kwon Mu-jin's own written memoir: first person, past tense, covering his life from about fourteen to about nineteen and written on the road (R61-3). It is a full rebuild, with the old text used only as source notes (R61-10). The length band is set piece (R48-46, 5,000 and up).

---

## The ten that matter most

1. **R48-40-NPC_THOUGHTS, R39-7:** no other minds. He writes what people did, what they said, what they let slip, and his own guess, which may be wrong. He never states another person's thought or motive as fact, and no one's italic thought appears but his.
2. **R61-3, R61-42, R61-51, R61-70, R5-C1-NARRATION_NEVER_WINKS:** he writes at fourteen to nineteen and knows nothing that happens later. That means no Accord rank or Division, no Heresiology, no Rimward and no Frithia. Malphas is only his friend the alchemist. His errors, including 'nothing is erased', stand uncorrected, and no line nods to what the reader knows.
3. **R61-38, R52-21, R61-34, R61-39:** the Volume I voice apologises for explaining. It notices the flaw first and then the child, and it jokes only as dry self-correction. He never uses rank or court honorifics to win an argument. He names the house once and the Ledger-Prince never. To 'the Thrice-Great' he writes 'That is not my name'.
4. **R48-03, R49-40, R4-13-ZERO_BUDGET, R51-10:** use zero em dashes, en dashes or `--`, anywhere including the title and headings. No not-X-but-Y in any form. No sentence whose only job is to explain the one before it. No hard-ban word. The old text had 53 dashes.
5. **R48-06, R4-14-HARD_CEILINGS, R4-14-CHAIN_CEILING, R4-14-RUN_RULE, R49-13:**
   - The hit is the shortest sentence in its paragraph, sits last and runs under ten words.
   - Never three sentences over 25 words in a row.
   - No three neighbouring sentences within 40% of each other's length.
   - At least 18% of sentences run under eight words.
   - Sentence-length CV aims for 0.80.
6. **R49-02, R35-2, R48-13, R51-34, R51-08, R51-30:** past tense, close register and timeless diction.
   - No okay, cool or mindset-type words.
   - No Earth day or month names.
   - No 'week': use a quarter-moon, a turn, a season, a courier's nine days, or distance in stations.
   - No Earth holy swears.
7. **R57-07, R48-16, R61-112, Table Rule 5:** this is a fully metaphysical document.
   - Stages go by their FOW name (he was at Glory at fourteen).
   - EU, η and site density appear when he takes his spectacles off.
   - Every figure comes from `fow_line`, the card or the Codex, or from arithmetic shown in the Notes. With no source there is no figure.
8. **R57-11, R13-2, R13-4, R48-20, R48-37, R61-91, R61-101, R61-6:** the mechanism is the effect.
   - At a working's first display and at its finisher, it is explained at the three strata in causal sentences, and the cost shows in the body.
   - He is a Draftcraft practitioner and writes in terms of price, vessel, seal and ledger.
   - No Draft refills a reserve.
   - Calcination and Distillation are never Wellsprings.
9. **R61-11, R61-16, R61-49, R61-128, R61-35, R14-5, R50-31, R50-32, R61-1, R61-131:**
   - Furveus, never Paracelsus. Malphas, never Noxinus. Kwon Mu-jin, never Vis Trismegistus: 'Vis, Alchemical Astronomer' appears only on the coffin.
   - Every system term is spelled exactly, and a near-miss fails.
   - Names are romanised only and never italic.
   - The volume is dated in the early Imperial Age, never 'Era of Voyagers', 'Withering Era' or 'IC'.
10. **fair-play § Clean publishing, R48-47:** the text carries no rule ids, sources, 'pending', provenance or tool names. All notes go under a `## Notes` heading, where verify.py stops. Run the checker with `--band set-piece`, fix every FAIL, read every WARN and run it again.

---

## 1. Hard bans

- **R48-03-SIMILES, R15-1-AI_TELL_CHECKS_SURVIVE:** no em dash, en dash or bare `--` anywhere above `## Notes`, headings and title included. The checker FAILs on it.
- **R49-40-NOT_X_Y:** no pair where the second part corrects the first. All eleven forms count: 'not X but Y', 'Not X. Y.', 'not merely', 'not so much X as Y', 'less X than Y', 'rather than', and 'which is to say' correcting a negation. Plain negation standing alone is free. The old text failed on 'not so much a giver of life as'.
- **R15-1 (countdown negation):** no run of short negated sentences that resolves into 'Just' or 'Only'.
- **R6-1-LADDER_BAN, R6-11-CHECK18_LADDER:**
  - No 'was X and the X was' chains. Cut back to the first concrete noun.
  - No concrete observation restated as an abstraction in the next sentence.
- **R4-13-GLOSS_DEFINED, R4-13-ZERO_BUDGET, R4-13-DELETION_TEST, R4-13-THREE_DISGUISES:** no sentence whose only job is to state the significance of the one before it. That covers the etymological, register and stakes disguises. Deletion test: if a sentence can be cut without loss, it stays cut.
- **R51-15-FIRST_USE:** never gloss a WOTR term for the reader in apposition. Meaning comes from context and use.
- **R51-10-SLOP_WORDS:** the checker FAILs at first use, in narration or speech, of:
  - tapestry, testament, palpable, visceral
  - symphony of, a dance of, whisper of
  - orbs, ministrations, electric touch, velvet voice, shiver down the spine
  - a breath he didn't know he was holding, the coppery tang of blood, the smell of ozone
  - R57-30: 'ozone' on its own is free.
- **R49-41-QUESTIONS:** no hypophora. A question in narration either stays genuinely open or goes.
- **R5-C1-NARRATION_NEVER_WINKS:** no line acknowledges that the reader knows better than he does.
- **R5-B-MANHWA_DIRECTIVE_REPEALED, R5-G-TELL_BANK_ADDITIONS, R5-D-HUMOUR_BARRED:**
  - No declarative characterisation.
  - No reaction-shot cutaway.
  - No setup-deadpan-reaction beat.
- **R49-22-NATURE:** weather and landscape are described, never personified.
- **R49-20-STOCK_PHRASE:** no dead metaphor, even one he might think. Rebuild it from his own life: the bench, the sky, Sum-gol's fields, the court.
- **R6-12-TELL_BANK_SURVIVING:** no fresh texture invented where the Inventory already has texture. R49-46 lifts the old ban on science vocabulary for scenery for a trained POV like him.
- **Stale quickcheck lines. Ignore these in `prose-law-quickcheck.md`:**
  - the "narration leak" grep, superseded by R49-47
  - "causal connectives only in a mouth", superseded by R49-43
  - "reification two per scene", superseded by R49-21 and R57-42
  - "a faculty speaks once per scene", superseded by R12-7
  - "one italic thought per NPC", superseded by R48-40: none at all in a written document

## 2. Sentence and paragraph shape

- **R48-06-RHYTHM_LAW, R4-14-LANDING_RULE:** the emotional hit is the shortest sentence in its paragraph and sits last. Anything after it is the paragraph clearing its throat.
- **R4-14-HARD_CEILINGS:**
  - A payoff sentence runs 10 words or fewer, with no subordinate clause.
  - At least 18% of sentences run under 8 words. The checker FAILs under 10% and WARNs under 18%.
  - No paragraph closes on three sentences over 18 words.
- **R4-14-CHAIN_CEILING:** never three consecutive sentences over 25 words. The checker FAILs on it, and the old text failed.
- **R4-14-RUN_RULE, R4-ADD-CHECK16:** no three consecutive sentences within 40% of each other's length. The checker FAILs at four such runs; the old text had twelve. Read every run.
- **R49-13-VARIANCE:** sentence-length CV targets 0.80. Under 0.50 is the strongest tell (the old text was at 0.74).
- **R4-14-PARAGRAPH_VARIANCE:** variance is enforced paragraph by paragraph, not only across the whole document.
- **R49-12-SHORT_FLOOR:** description may run long, and short sentences cluster at beats.
- **R4-14-APPROACH_LADDER:** decelerate into the hit (long, then medium, then the landing) and expand again after it.
- **R4-14-CLAUSE_CAP_AT_BEAT:** within the three sentences around a value turn, each sentence carries at most one subordinate or coordinate clause.
- **R4-14-CONJUNCTION_AUDIT:** two or more of and, as, while, which or because in a sentence carrying a beat is a fail.
- **R49-14-PARA_SHAPE, R48-07-WHITE_SPACE:**
  - Paragraph-length CV of 50% or more is wanted; the checker WARNs under 35%.
  - Medium paragraphs, with white space used sparingly so it still means something.
- **R49-15-FRAGMENTS:** concrete noun and image fragments are free. Not, Never, Only, Just and And emphasis fragments draw a WARN at three.
- **R49-17-OPENERS:** '-ing' openers and 'As I ...,' constructions draw a WARN at three. The checker counts 'As I'.
- **R49-42-FILTER_VERBS:** I saw, I heard, I felt, I noticed and I watched are counted, with a WARN above 5 per 1,000 narration words. Give the reader the thing perceived.
- **R49-25-OPENINGS:** arrivals open on the senses; tense passages open in motion.
- **R49-26-ENDINGS:** every chapter, and the volume, ends on an action, a concrete image or a spoken line. Never a summary, a moral or a question.
- **R49-27-SCENE_BREAKS:** real jumps in time or place take a chapter head, a blank line or an ornament.
- **R49-18-SIMILE_COUNT, R48-03:**
  - Similes are welcome when earned.
  - Two competing over one beat: cut the weaker one.
  - The checker WARNs on any paragraph with two simile markers.
- **R48-04-METAPHORS, R49-19-EXTENDED:** metaphors come from his own life (trade, homeland, body). Extended and stacked metaphors are allowed by ear.
- **R48-05-HIGH_STYLE, R49-23-HIGH_STYLE, R49-24-ELEGY:** mythic high style, anaphora, the triad and full elegy are all legal at a mythic moment.
- **R49-21-REIFICATION, R57-42, R4-15-NEVER_AT_BEAT, R4-15-CONCRETE_FIRST, R4-15-LICENSED_CLASS, R4-15-BODIES_EXEMPT:**
  - No count applies.
  - The value never flips on a personified abstraction, and an object in the room always wins.
  - Debts, seals, warrants, tallies and titles are free, and so are bodies.
- **R48-01-BEAUTY, R48-02-DENSITY:** beauty comes from exact concrete detail, image and what goes unsaid, with lush sensory layering throughout.
- **R49-53-BUDGETS:** per-scene budgets don't grow with length. A 7,000-word volume simply runs tighter.

## 3. Register and vocabulary

- **R48-13-PERIOD_FEEL, R51-34-DOC_MODERN, R49-44-MODERN_FLAGS:** the document's narration is timeless; remembered speech may run casual (R51-09).
- **R51-03-LIST_SLANG, R51-04-LIST_PSYCH:**
  - Never: okay, OK, vibe, awesome, cool, teenager.
  - Never: triggered, toxic, closure, mindset, boundaries.
  - Anxiety and stress stay. The checker WARNs on the rest.
- **R51-05-LIST_TECH:** technology metaphors only for things his world has: rail, telegraph, the main, the meter, instruments.
- **R51-07-CLOCK_WORDS:** seconds and minutes are free, and in-world units add flavour.
- **R51-08-CALENDAR:** no Earth day or month names, and no 'week' or 'weekend'.
  - Use the culture's own span: a quarter-moon, a turn, a season, 'last season', a courier's nine days, stations.
  - The old text's 'a matter of weeks' goes.
  - The checker skips 'week' itself, so check it by hand.
- **R51-30-HOLY_OATHS, R51-29-SWEARING, R58-05:** no God damn, Christ, Jesus or go to hell. Swear by the world's powers ('Archons take it') and use the culture's oaths first; Ketsuen's are 'On the record' and 'Before the stones'.
- **R48-12-PROFANITY, R51-02-CLOSE_POV_SWEARS:** profanity is allowed in mouths and in his own prose when he would think it.
- **R51-11-COLLISIONS, R57-31:** delve, echo, numinous, sovereign, sanctum, weave and ledger appear only in their WOTR sense ('Parunic Echo', a Draft ledger). Their plain senses are banned. Check by hand.
- **R51-06-EARTH_WORDS, R48-22-LENS_NAMES, R48-23-LENS_COUNT:** herculean, Stoic pneuma, solve et coagula, the Tria Prima and Hermetic correspondence are legal wherever they fit.
- **R49-45-SCIENCE, R49-46-CHEMISTRY, R13-6-REAL_SCIENCE_VOCAB, R48-09-TECH_WORDS:** real science and anatomy terms are the technical register. As a trained alchemist-physician he may read anything in them, scenery included.
- **R13-6-METAPHYSICS_VOCAB:** correspondence, sympathy and contagion, essence and accident, form and actualisation, recognition and refusal. This is the document voice's own vocabulary.
- **R49-47-STAT_WORDS, R51-16-OLD_BANS_FALL, R53-16-GUILD_WORDS:** stat names, Grades, Stages, η, EU, Sub-Stat names and Guild words are free in his prose.
- **R49-48-TECH_NAMES, R50-08:** technique names and their translations are free in the prose. R8-26: nobody translates his own technique's name aloud in dialogue.
- **R48-10-MIXING, R12-2-REGISTER_TEST:** Technical and Mystic registers mix by ear. A thing a person chose to do is Technical; a thing that was already running is Mystic.
- **R51-01-TIMELESS, R15-1-REGISTER_BY_CULTURE:** plain, undated English by default. Per-culture narration registers are flavour, not law.
- **R15-1-DICTION_PALETTE, R57-31:** the elevated bank is free: eldritch, chthonic, tenebrous, lambent, sepulchral, incarnadine, stygian, empyreal, ineffable.
- **R51-13-WORD_STOCK, R51-14-NEW_TERMS:** word stock is by ear, and there is no ceiling on WOTR terms.
- **R13-6-SCALING_VOCAB_RESTRICTED, R13-6-ANIME_GRAMMAR_TRANSLATION_AID:** none of these ever appear on the page:
  - Attack Potency, hax, speed blitz, outlier, anti-feat
  - Nen, Naruto, JJK or Bleach shape-words
- **R5-D-HUMOUR_PERMITTED, R48-11-HUMOUR, R61-38:** humour arrives as dry self-correction, inside prose that is already moving.
- **R51-28-CHANT_PAGE, R50-26-CHANT_TONGUE, R20C-35:** a chant appears in its own language, and he may think its meaning in his own words.
- **C-111 fix, canon's side (fixes.md):** spoken Latin is the order laid over the Parun Authorization. Never call the Latin 'the authorization'.

## 4. POV in a written first-person document

- **R49-02-TENSE:** books are written in past tense. *Reading:* keep present tense to his rare standing statements at the writing desk.
- **R35-2-NARRATION_DISTANCE_ASSIGNMENTS, R41-1:** Kwon Mu-jin runs in the close register. The card's caution: his failing read is shown from inside.
- **R54-13, R54-14:** he has a register, so he may carry a POV. Everyone else is read through his register rules.
- **R48-40-NPC_THOUGHTS, R39-7-NO_NPC_THOUGHT_UNDER_POV_LOCK:** no other minds.
  - No thought, feeling or motive of another person is stated as fact.
  - No one's italic thought appears but his.
  - Others appear through what they did, said and let slip, plus his inference in his own words, which may be wrong.
- **R49-09-CUTAWAYS:** does not apply here. *Reading:* a first-person document cannot cut away to what he did not see; hearsay arrives as a named report.
- **R5-C1-INFO_TRACKED_PER_POV:** before each chapter, name three things: what he knew then, what he wrongly believed, and what the reader knows that he does not.
- **R61-3, R61-42, R61-2:** the knowledge ceiling. He writes on the road at fourteen to nineteen, outside any institution. There is no Division, no rank, no vow, no Heresiology, no Academy, no Rimward and no Frithia.
- **R61-51:** Malphas is his friend 'Malphas the alchemist'. There is no hint of The Mother, the lich or the cult.
- **R61-70, R12-4-VOICE_ONE_POV, R5-C1-WELL_REASONED_WRONG_CONCLUSION:** his explanations stop at the edge of his competence at the time. 'Nothing is erased' stands as his confident error: sound reasoning on a bad premise, left uncorrected in Volume I.
- **R4-13-FID_CARVEOUT, R5-E-FREE_INDIRECT_CARVEOUT, R49-08-MEANING, R5-E-NARRATION_NEVER_ADJUDICATES:** after a beat he may say what it meant, in his own idiom, and be wrong. A neutral, authoritative verdict gets cut.
- **R49-07-EMOTIONS:** the body comes first, then his own word for the feeling, or none.
- **R48-39-INTERIORITY, R49-05-ITALICS, R49-06-MEMORIES:** interiority runs throughout. Italic self-talk can be frequent, and memories may run as full flashbacks.
- **R48-44-NAME_USE, R49-10-EPITHETS, R20-5-ON_THE_PAGE:** people go by the name or epithet he uses, one epithet per person per scene. A change of epithet is itself the beat.
- **R49-28-INTROS, Table Rule 11:** first sight of a person gets the full physical inventory in one passage: hair by comparison, face, body, the fit and wear of their clothes, distinguishing marks. Then a want and an unswappable voice.
- **R5-B-DECLARATION_TO_INFERENCE:** people are established by what they choose, refuse and notice. The reader assembles them.
- **R49-11-NOT_KNOWING:** the not-knowing quotas are optional.
- **R49-50-OWN_BODY:** he has medical training, so he names his own hurts exactly.
- **R49-52-MEASURES:** he measures in his own units.

## 5. His voice (card and rulings)

- **R61-38-MUJIN_WRITTEN_VOICE_BY_VOLUME:** in Volume I he apologises for explaining. He notices the flaw first, then the child. His jokes are dry self-correction. Keep the length and texture.
- **R52-21-KWON, card 'Never says':** he never uses rank or old court honorifics to win an argument. He gives his name and nothing above it, and never lets an error stand unspoken.
- **R61-34-MUJIN_MAHUO_BOYHOOD:** his boyhood is built from the frost and the mountain, Sum-gol's river-valley fields, and sky-watching. He names the house once and the Ledger-Prince never.
- **R61-39-THRICE_GREAT_REFUSED_EPITHET:** after the king's hall the Monastery calls him the Thrice-Great, and he writes 'That is not my name'. There are no Sage titles.
- **Card voice block (R52-03, R52-04):**
  - Contractions sometimes, but never while correcting an error or reading a working.
  - Pet words: 'Now, now,' when giving ground and 'Correct,' when someone has it right.
  - Now and then a Sum-gol turn drops a word from a short sentence.
  - Outside a Draft or a diagnosis he gives no exact figures, only 'about a second and a half'.
- **R52-25-STRESS_RULE, R19-4-REGISTER_UNDER_STRESS, card:** under strain he writes short, broken bursts that still over-explain. He takes the lens off, goes very still and names the problem aloud.
- **R52-23-MAHUO_WE:** under strain he slips into the family 'we' for himself.
- **R52-26-GRIEF, card:** grief takes him back to Sum-gol's house tongue and the old family sentences.
- **R52-27-JOY, R52-28-COMPOSURE:** joy shows in his hands, face and breath while his speech holds. Trained calm is free.
- **R20C-49, card 'Gloss rights: yes':** he may explain what the room does not know, in his own words. The narrator never glosses a term for the reader.
- **R19-4-WORLD_ANCHORED_SPEECH, R15-1-VOICE_DIFFERENTIATION:** his metaphors come from his trade and home. He differs from others in what he notices, wants and refuses.

## 6. Remembered dialogue

- **R49-31-TAGS:** dialogue is mostly untagged; voices sort themselves.
- **R19-4-REALISTIC_SPEECH:** include false starts, self-repair, interruption, non-answers, people talking past each other, trailing off, business mid-line and wrong things said.
- **R19-5-COMPOSURE_BAN, as amended by R52-06-TRIADS:**
  - Speakers don't all share one sentence length.
  - No perfect syntax from the young, the exhausted or the foreign.
  - Triads and parallel clauses are legal in any mouth.
- **R19-4-ICEBERG_DIALOGUE:** no one explains to another what both already know.
- **R49-32-CUT_OFFS:** interrupted speech ends in an ellipsis and the interrupter's line follows.
- **R48-42-LIES, R49-36-LIE_TELLS:** people lie for their own reasons, and every lie leaves a catchable tell.
- **R48-43-SPEECHES, R49-35, R52-06:** one crafted, eloquent speech is allowed at the big moment (the king's hall). It still has to pass the composure read, and triads are legal in it.
- **R48-41-MAGIC_TALK, R12-4-VOICE_DISCIPLINE:** each person talks about magic by their training: a physician-alchemist in doses, a monk in doctrine, a farmer in folk words.
- **R52-05-COUNTING:** only instrument-readers and clerks speak exact numbers. Everyone else rounds.
- **R52-02, R52-07-SWAP_CHECK:** no two voices could be swapped.
- **R52-29, R52-30:** a voice built for an NPC starts from a researched real type of speaker, and each NPC carries one fixed saying from the Inventory.
- **R20-4-PRONUNCIATION_ADAPTATION, R50-33:** a foreign mouth bends a name, spelled as heard.

## 7. In-world documents

- **R57-07-DOCUMENTS_FULLY_METAPHYSICAL:** in-world documents are fully metaphysical: Stage, Grade, Band, EU, AU/s, η, Crystal State and Category may all appear.
- **R48-16-REAL_FIGURES, R61-112:** anyone with an instrument or a trained eye states figures as often as they would. He reads EU, η and site density whenever he takes off his spectacles.
- **Table Rule 5, R61-112, R53-29-LOOK_UP:** never invent a number.
  - Figures come from `fow_line`, his card, the Codex, or arithmetic from those shown in the Notes.
  - Derived figures (a site's density, a drift) are derived, never invented.
  - No source, no figure.
- **R6-2-READ_DELIVERS_FACT, R12-7-APPARATUS_CAP_REPLACED:** a lens-off read delivers a bare figure first, then his interpretation. Reading costs him tempo on the page.
- **R49-52-MEASURES, card:** figures come only from a trained eye, an instrument or notes. Outside a read he rounds.
- **R61-124:** the Tempus drift is priced as a debt by correspondence, never as an EU figure.
- **R20C-37-DOCUMENTS_OWE_NOTHING, R15-1-MYSTIC_REGISTER_NEVER_PHYSICS_STRUCK, R12-2-MYSTIC_REGISTER_DEF:** a document may be as scientific as it likes. The Mystic Register (law stated, prices as prices, taboos without justification) is an option.
- **R51-33-DOC_REGISTER:** the house style is the writer's own voice, as in a letter. It is not chancery.
- **R51-34, R51-08:** the modern-word list and the calendar ban apply to documents.
- **R61-1, R61-131, R57-36:** the text is stamped in the early years of the Imperial Age and carries Imperial-Age years. The count runs 715 years from the sealing of the Codex. Never 'Era of Voyagers', 'Withering Era' or 'IC'. C-105 and C-112 are ruled, but old pages still read the old way, so do not copy them. See Open items for the year number.
- **fair-play 'Documents give pieces, not solutions':** state law, cost and tell. Never say how to beat someone.
- **R47-12-MYSTERY_STAYS_OPEN, R17-6-MECHANISM_VS_ORIGIN, R20C-23-ORIGIN_STAYS_MYTHIC:**
  - Mechanism is explicable; origin stays mythic.
  - Why a Wellspring answers is at most one school's reading.
- **R61-32-SUMGOL_TITLE_BESIDE_CODEX, R50-01, R50-31:**
  - Volume I is headed by a Sum-gol title in his own words, beside 'The Alftian Codex'.
  - It is correct Korean with a gloss that matches, romanised with no hangul.
- **R58-04:** titles and headings skip the ban list, but an em dash in a heading still FAILs.
- **R61-40-ACCORD_SEALED_MUJINS_JOURNALS:**
  - The frame lines are the archive's, not his.
  - He deposited the volume for common use; the Accord withdrew it under seal as Mortalis-adjacent.
  - 'Recovered' becomes 'withdrawn under seal'.
  - R61-42: the Accord never appears in his own text in Volume I.
- **fixes.md:** the Emerald Tablet recited in the king's hall keeps its own speaker, never the narrator. The Tablet's wording and Trismegistus stay (R61-11), credited in the Notes (R48-27).
- *Layout, verify.py behaviour:* set archive frame lines as headings or `>` blockquotes. Then the length count and the last-line check read his prose, while the bans still run on the frame. The old text's classification line was read as its last line.
- *Reading:* set book titles (the Necrocursica, the Tablet) plain, since foreign words and names are never italic (R50-32, R49-49).

## 8. Magic on the page

- **R7-1-THREE_HARD_RAILS, R12-1-PACK_SEVEN_SURVIVORS:**
  - Power is finite, spent and visible.
  - The ladder is real, felt before it is seen.
  - Everything traces to a source.
  - A fully explained working that costs nothing is worse than an unexplained one.
- **R57-11-MECHANISM_IS_EFFECT:** the effect on the page is the mechanism playing out. Never write what a working does apart from how it does it.
- **R13-2-THREE_STRATA_MANDATE, R48-20-STRATA, R13-4-THREE_EXPLANATIONS:** at a working's first display and its finisher, three causal sentences sit beside the image:
  - the Aether: density, Residue, saturation, the district main
  - the Wellspring: its law as real physics, with the glyph as boundary condition
  - the Essence: Crystal, Shell, Core, Layer, η, Crystal State
  - Between those moments, lighter touches.
- **R16-3-COMPOUND_SENTENCE:** name the real phenomenon, give the system term as its name or boundary, and state the physical consequence, in one sentence or a short group. Neither glosses the other.
- **R49-43-EXPLAINING, R12-4-VOICE_ONE_POV, R12-4-VOICE_MIXING_RULE:**
  - He may explain causes in his own reasoning and vocabulary.
  - Other explaining voices may enter: a knowledgeable second, an opponent's contempt, a quoted document.
  - No more than two voices per engagement.
- **R48-25-AWE, R12-6-RITUAL_SPECIFICATION:**
  - Wellsprings, rites, oaths and the Veil are explained as plainly as a sword exchange.
  - A rite has its bill of goods, its order of operations and its ways of going wrong.
- **R48-24-4_THEORIES, R61-4:**
  - The Four Theories surface through people who hold and argue them.
  - The residues, the Volitional Trace and impression-bodies are system fact.
- **R48-37-COST_SHOWN, R47-8-WASTE_IS_HEAT, R57-24-AFTERMATH_IS_THE_TELL, R47-9-INHERITED_FAILURES:**
  - Cost shows in the body: tremor, heat, thirst, a Crystal ache.
  - Wasted energy leaves as heat at the Shell.
  - What a working leaves behind is its tell, and every working carries its Wellsprings' documented failures.
- **R53-17-THE_BILL:** any working indoors on a main raises the bill, and somebody notices the cost.
- **R61-43, card:**
  - His passive sense of failing seals is free and reaches streets away.
  - A full lens-off read costs a migraine.
  - He diagnoses and warns, and never performs Category Three.
- **R61-91-MUJIN_AND_MALPHAS_DRAFTCRAFT:** both he and Malphas practise Draftcraft. His summons are a spoken call over Draft ground, and his prose talks in price, vessel, seal and ledger.
- **R61-100, R61-101:**
  - Drafts come from stock and vein and cost no reserve.
  - A standing work (a seal, an amulet) costs a once-only share of reserve.
  - No Draft ever refills a reserve.
- **R61-105:** arsenic and mercury are named plainly as medicines that heal at a dose and poison past it. Furveus shows early crucible palsy and Draft-mark, which Mu-jin reads on sight. Research checks every dose before print.
- **R61-6, R61-5:**
  - Calcination and Distillation are bench operations, never Wellsprings.
  - Sublimatio is sublimation; Sublimare is distillation.
- **R61-67:** the Great Work's stages map to currents:
  - Calcination: Cinerion
  - Dissolution: Dissolution
  - Separation: Judicium
  - Fermentation: Rebirthine
  - Distillation: Sublimare
  - Coagulation: Coagulatio
  - Conjunction is driven by Attraction, not a current.
- **R61-79:** the 'double seven' spiral maps the Great Work onto the Stages. Its stated anchors give Glory VI as Distillation, Refraction VII as Coagulation, Invocation IX as Dissolution and Dissonance XI as Conjunction; the pairing for VI and VII is derived from those anchors.
- **R61-82:** the Tria Prima map to Crystal layers: Sulphur to Core, Salt to Shell, Mercury to the Attraction Layer.
- **R61-70, R61-71:**
  - Records live in ground and objects as Mnemata, and Anamnesis reads and wakes them.
  - Never write 'Anamnetic fabric'.
- **R61-97:** 'Parunic Echo' is the trade's word for a practitioner's Essence Signature in Residue, readable from Stage IV. 'Glyph-trace' is retired.
- **R61-125:** God-Essence is the Heralds' belief-word for Wellspring Essence. The humming bridges are ordinary inscribed arrays.
- **R61-122, R61-124:** Tempus is the Hermetic name for the Weight, the 29-year wanderer; it is not a gas giant seen by day. Its drift is moved by correspondence, with no energy.
- **R61-98, fixes.md:**
  - Jabir's copper amulet is cut in Old High Runic, in 'a Parunic hand', not a dialect.
  - Mu-jin reads it at once and cannot date it; Jabir's recited words are his own gloss.
  - R47-5-LADDER_RUNG: name the amulet's Tier Ladder rung by name.
- **R61-88, R18-4-GLYPH_QUOTED_EXACTLY:**
  - Glyph chains use Master Glyph Index names.
  - He may gloss his teacher's older name once per glyph ('Ie, Perception; I was taught Insight').
  - Every chain is quoted exactly.
- **R20C-42-LAW_V_STAGE_GATE_REFRACTION, R42-2-AETHER_CLASS_FROM_GLORY:**
  - Below Refraction (VII), a working needs voice, hand, ink or blood. He is at Glory (VI) at fourteen.
  - Aether Class emerges at Glory.
- **R14-5-CANONICAL_TERMS, R54-1:** system terms are exact, and Stage names are FOW's:
  - Glory VI (left the court)
  - Refraction VII, Transcendence VIII, Invocation IX, Realization X, Dissonance XI (on the road)
  - Never Ignition or Temper.
- **R9-3-AURA_AS_FRACTURE, R9-3-BODY_UNDER_LOAD, R9-3-EYES_AS_TELL, R10-3-EFFECT_PHYSICAL_ONLY:**
  - Essence discharge is shard-edged geometry; 'it glowed' is banned.
  - One splash-panel beat per scene, at the display.
  - At a Stage threshold the eyes go first.
  - A projected shape is shown, never explained.
- **R54-21-FACULTY_AS_SUBJECT and R6-2-FACULTY_NEVER_SUBJECT:** in a close register the faculty may be a sentence's subject. The newer rule governs; check 19 still WARNs, so read each case.
- **R7-2-EPOCH_SCALE_SURVIVES:** Titans, Archons and anything at Epoch scale make dread and awe but never resolve a plot.
- **R61-78:** 'necromantic' is the scholars' loose period word.
- **R61-83:** corruptions are cited by name, never by number.
- **fixes.md:** 'the Archons', 'the Continuum', 'Paru's First Speech' and 'the Veil' are live terms and stay as written.

## 9. World and texture

- **R6-9-RECURRENCE_RULE, R51-31-SENSE_BANK, R58-05, R15-1-STANDING_INVENTORY_SURVIVES:** texture comes from the Standing Inventory and its senses bank first.
  - Ketsuen (`desktop/inventories/ketsuen.md`) covers Sum-gol, the valleys and the Uplands (R61-115). Its Sum-gol lines: river-valley rice, the Mahuo table, and Mahuo rites for the dead.
  - Use the Accord inventory toward Urbis.
- **R53-19-QUOTA, R49-54:** two Ketsuen signature items per session, from these five:
  - the ward-post and 'who keeps your posts'
  - cedar weeping sap
  - the Proving and 'on the record'
  - the pressure at the temples
  - the mallet on the practice stone
- **R53-30-TEXTURE_DENSITY:** every beat carries at least one detail that could only exist in this world.
- **R53-29-LOOK_UP, R53-21-CANON_GATE, R53-22:** look up every world fact. Anything invented is logged in the Notes for entry.
- **R5-C2-ELEGY_CONCRETE_THING, R6-10-INVENTORY_AND_ELEGY, R53-31-GONE_LIST, R5-C2-IRREVERSIBLE_NOBODYS_FAULT:** elegy attaches to a named, concrete thing that is gone, such as Sum-gol's empty roofs (R61-33). Never to abstractions.
- **R53-28-VISUAL_REFERENCE, R11-2-SILHOUETTE, R59-01, R59-02:** the look is Victorian imperial.
  - No smokestacks, coal, steam or electricity.
  - Instead: Essence engines, the main and the meter, standpipes, gauge-housings, brass, slate.
- **R59-04, R61-115, R61-117, R61-120:** rail runs where it runs.
  - Castlefall is a valley rail town.
  - Genesio is a day's rail to its waystation, then two days mounted up the passes.
  - Urbis is a heartland city with trams.
- **R59-05, R59-13, R59-14, R59-06:**
  - The regional gradient is steep.
  - Pocket watches from the middle class up; bells and sun in the country.
  - Heavy bureaucracy.
  - Papers and broadsheets.
- **R60-13-THE_GATE, R60-14, R60-15, R60-16:**
  - Nearly everyone has a Crystal, dormant unless trained.
  - Who may learn magic is locked down by class, licence, exam and bloodline.
  - The lock is enforced by controlled texts, Crystal registration and inspectors.
- **R53-18-AWE, R53-14-FOLK_KNOWLEDGE, R53-15-FOLK_BELIEFS, R53-13-FAITH:**
  - Commoners hold ranked practitioners as half-saints.
  - Folk know the rough ladder only in folk words.
  - Folk beliefs stand uncorrected.
  - Faith shows as petition.
- **R61-119, R61-118:**
  - The Heralds descend from Maelor's heralds.
  - The Monastery is at Urbis, with the Urbis Archivum in its lower floors.
  - Genesio's Archivum is the older outlying house, and there is no Genesio Monastery.
- **R61-126, fixes.md:** Genesio is an Antediluvian site. Write 'older than the count itself', never 'the current Epoch's reckoning'.
- **R61-116:** Jabir's home is the New World border where Eresse's old ground meets the chartered arc. There is no Shaneni empire.
- **R61-33:** he was born to the remnant of a house in a thinned valley. The school and sixty roofs are what remained.
- **R53-25, R53-26, R48-27:**
  - Real object names are allowed where the culture is built on them.
  - Real history is taken exactly, then bent one step, and credited in the Notes.
- **R53-12-LITERACY:** literacy varies by culture; Ketsuen's Proven are highly literate.

## 10. Naming

- **R61-11-RENAME_HISTORICAL_PEOPLE_IN_TEXTS:** real historical people get in-world names.
  - R61-16: Furveus, never 'Paracelsus', and no 'called Paracelsus'.
  - Jabir, Gillus and Thom need in-world names; none are registered yet.
  - Trismegistus, Asclepius, the Tablet's wording and the Tria Prima stay (R50-05), credited in the Notes.
- **R61-49, R61-128:** Malphas, never Noxinus or N. Ren. Kwon Mu-jin, never Vis Trismegistus.
- **fixes.md:** 'My Elfin constitution' becomes a human Mahuo court-line constitution.
- **R61-35:** 'Vis, Alchemical Astronomer' survives only on the Mausoleum coffin, as an earlier life of his soul. *Reading, from the knowledge ceiling:* in Volume I he can't know what it means.
- **R61-25, R61-29, R50-27:**
  - The king and his wife stay unnamed roles.
  - The dragon-claw monk gets a name; the Prior stays a role.
  - Anyone new is a role until they speak twice or matter.
- **R61-21:** Tat becomes Doyun, met as a boy at Sum-gol when Mu-jin is 22 to 24. That falls outside Volume I, so the old Tat scenes do not appear.
- **R23-2-KOREAN_STRATUM, R20-1-MAHUO_ANCHOR, R23-10-TELLING_APART_KOREAN:**
  - The lineage name comes first, then a two-syllable given name carrying a generational syllable.
  - A hyphen means Mahuo.
  - No courtesy names, no wuxia forms, no given-name-first order.
- **R54-36-MAHOU_AND_MAHUO:** Mahou names the line as an institution; Mahuo is the surname. R37-1 leaves Kwon as a Mahuo cadet branch an open flag, so don't settle it on the page.
- **R50-01-REAL_GRAMMAR, R50-12-COINED_LATIN, R8-21-REGISTER_TABLE, R8-22-LITERAL_GLOSS:**
  - Borrowed names are real, correct phrases in their language.
  - New Latin is real Latin, and a gloss is literal.
- **R50-31-SCRIPT_SHOWN, R50-32-ITALICS, R49-49-FOREIGN, R50-15-DIACRITICS:**
  - Names are romanised only, never in hangul or kanji.
  - Never italic.
  - Diacritics stay (Nalūn, Kōkan).
- **R61-121:** 'Naln' is Nalūn.
- **R61-31:** write 'Noospheric'. Anamnetic, Necrocursica and Urbis stay as they are.
- **R50-22-PLACE_STRATA, R50-23-DOUBLETS, R51-18-DOUBLET, R9-2-CLASS_MARKED_CRAFT_WORDS:** a place carries several names and he picks one, and he uses a craft word the way he would say it.
- **R50-10, R50-11, R8-21-NAME_IN_OWN_LANGUAGE:** his arts carry true names in his own tongue. A new English technique name is two words at most.
- **R47-7-NAMES_NOT_NUMBERS, R46-2, R47-5:** Tiers of Standing and item rungs go by name (Marked, Proofed, Tempered, Instrument...), and every item carries its rung by name.
- **R14-5-NEAR_MISS_FAIL, R14-6-CHECK27:** a misspelt Stage, Wellspring or Family fails. Check every capitalised term with `codex "<term>"` or `build/codex.py check`.
- **R16-6-COINAGE_HANDLING, R50-28, R50-30:**
  - A coinage stays in the prose and gets a one-line definition in the Notes.
  - Name by ear mid-draft, then check against the banks at the end.

## 11. Clean publishing

- **fair-play.md § Clean publishing (Isaac 2026-09-26):** the page carries only the content, in its own register. It never carries:
  - Isaac's name or role
  - rule ids, rulings, open questions, 'pending', or conflict or issue ids
  - provenance ('originated', 'drafted by', 'generated from', 'estimates')
  - the names of Claude, Natalie, agents or tools
  - any self-reference
  - In-world attributions stay: the archive's frame lines, the Sum-gol title and the author's own name.
- **R48-47-NOTES, R48-49-CITATIONS, R48-27-REAL_WORLD, R14-7-STAT_LEDGER_CONTENTS:** these go in the draft file under a `## Notes` heading only:
  - rule ids
  - a Stat Ledger for each named practitioner
  - every figure's source and arithmetic
  - real-world credits (the Tablet, thinkers, doses)
  - the source list
  - verify.py cuts at that heading, and the published page drops the whole block.
- **R16-5-NOT_IN_NOTES, R16-8-CHECK31:** every mechanism term in the Notes must also appear in the prose.
- **verify.py:** only a heading starting `## Notes` ends the body. `## Author notes` or `### Notes` is checked as prose.
- **Job brief:** write only under `/tmp/wotr-drafts/`. No repo writes, commits or publishing.

## 12. Verify

```bash
~/.venvs/wotr/bin/python /home/oridon/wotr-rule-index/build/verify.py /tmp/wotr-drafts/<file>.md --band set-piece --culture Ketsuen
# Codex terms and glyph chains, checks 46 to 48:
cd /home/oridon/wotr-rule-index && ~/.venvs/wotr/bin/python build/codex.py check /tmp/wotr-drafts/<file>.md
```

- **`--band set-piece`:** WARNs if the prose body is under 5,000 words; the ~7,000 target clears it. It counts sentence words in prose paragraphs only. Headings, `>` blockquotes and `|` table rows don't count, and counting stops at `## Notes`.
- **`--culture Ketsuen`:** Ketsuen is the right culture (Sum-gol is Ketsuen's Mahuo province, and the valleys and Uplands are Ketsuen per R61-115). The flag is accepted but has no effect, because verify.py only knows Kharven. Count Ketsuen's two signature items by hand.
- **`--combat`:** add it only if the draft puts a fight or a wound on the page. It adds HEMA and anatomy WARNs.
- **Output:** the run prints `PASS` or `FAIL: n fail, n warn`, then one line per finding, each naming its rule. It exits 1 on any FAIL.
- **FAIL:** a hard ban or a hard number was broken. Fix it and run again; a FAIL is never argued away. The FAILs are:
  - em dash, en dash or `--` anywhere above Notes, headings included
  - antithesis patterns (R49-40)
  - two Ladder clauses in one sentence
  - countdown negation
  - a hard-ban word (R51-10)
  - three consecutive sentences over 25 words
  - four or more flat runs
  - fewer than 10% of sentences under eight words
- **WARN:** a pattern that needs a human read against its rule. Fix it, or keep it only if the rule's carve-out covers it. The WARNs are:
  - a single Ladder clause
  - three or more emphasis fragments
  - a faculty as grammatical subject (R54-21 may allow it in close register)
  - gloss phrases ('which meant', 'in other words', 'that is to say'); these pass only if they are his own idiom and not a gloss for the reader
  - a feeling named with no body under it
  - a question in narration (possible hypophora)
  - two simile markers in one paragraph
  - a tidy-close opener on the last sentence
  - three or more '-ing' or 'As I' openers
  - filter verbs above 5 per 1,000 words
  - modern words
  - Earth calendar words
  - Earth holy swears
  - short-sentence share between 10% and 18%
  - paragraphs closing long-long-long
  - sentence CV under 0.50
  - paragraph CV under 0.35
  - length outside the band
- **info:** never blocks. It reports means, CVs, the filter rate, the italic count and the last line.
  - The italic count's 'one per named NPC' wording predates R48-40. Here, only his own thoughts may be italic.
  - The last-line wording predates R49-26. The rule is: an action, a concrete image or a spoken line.
- **Not automated, so read for these by hand:**
  - payoff length and landing, the conjunction audit, 'rather than'
  - collision words, foreign italics, 'week', the tic-word list (R49-55)
  - reification at the beat
  - the no-other-minds lock and the knowledge ceiling
  - voice swap
  - texture and the Ketsuen items
  - term spelling
- **Baseline:** the old Volume I ran FAIL with 4 fails and 3 warns:
  - 53 em dashes
  - one 'not so much X as Y'
  - a chain of three long sentences
  - twelve flat runs
  - sentence CV 0.74
  - `codex.py check` came back CLEAN.
- **R4-ADD-NO_SINGLE_PASS:** fix every FAIL, read every WARN and run again until clean. A single pass is never delivered.

## 13. Open items that touch this volume

The docket has nothing open: `check_docket` for all eight tags returned 0 pending and 0 proposed. These open canon rows and gaps still bear on Volume I. They are recorded here, not resolved.

- **C-106 (open):** Mu-jin is 38 on his pre-Ashgate card (R57-01), against 24 on older pages. This decides his calendar year at fourteen to nineteen, and Ara's age beside him.
  - R61-36 puts Ara in the illness chapter as a healer.
  - Her card says 21 as of 'Before Vaeloris'. If Vaeloris falls when he is 38, she was not yet born in Volume I's years.
  - Safe path: show her as his younger sister with no age stated as a number. The row still needs a ruling.
- **No Imperial-Age year number exists:** R61-131 says 'the texts carry Imperial-Age years', but no ruling gives the Age's first year, and the Concordance page is unchanged (C-112 ruled, pages lag). Any numeral would be invented (Table Rule 5). Keep a numbered stamp out until a year is ruled, and mark the gap in the Notes.
- **C-095 (open):** his card's header says 'Eastern Concord-adjacent enclave'; R61-34 and R61-115 put his boyhood at Sum-gol in Ketsuen. Write Sum-gol and never the enclave phrase.
- **C-094 (ruled by R61-33, page not reconciled):** the Ketsuen page still describes Sum-gol as a living province of about 15,000. Don't use its population or Warden lines against 'emptied before his birth'.
- **C-107 (open):** Aetheric Residue is either permanent or thins on a schedule. State no residue lifetime. Volume I's 'nothing is erased' is his own error anyway (R61-70).
- **C-111 (open), fixes.md applies canon's side:** Latin is the spoken order over the Parun Authorization, never 'the authorization'.
- **Unbuilt records:** Furveus, Neros, Jabir, the dragon-claw monk and Asclepius have no roster entry or FOW line yet (R61-16, R61-19, R61-20, R61-29, R61-26).
  - Put no figures for them on the page.
  - Jabir, Gillus, Thom and the monk have no in-world names yet (R61-11, R61-29).
  - Jabir's amulet has no Tier Ladder rung yet (R47-5).
  - Anything coined is logged in the Notes (R48-26, R50-28).
- **MCP index:** `load_rules` does not serve the R61 rulings yet. Use the `rule` tool or `out/rules.resolved.json` for R61 ids.
