# CHANGELOG — 2026-09-26 EDITION

*The 2026-09-12 edition stays in `desktop/` as history and is not edited. This edition does three things: it follows the seven packs Isaac ruled on 2026-09-26 (R47 Ability Law, R48 Writing Law, R49 Prose Law, R50 Naming Law, R51 Vocabulary Law, R52 Voice Law, R53 World Texture Law; the text is in `RULINGS.md`); it drops every check whose rule is now `status: superseded`; and it is written against the checker that exists, `build/verify.py` (also served as the wotr MCP's `verify_scene`), plus `build/codex.py check` (the MCP's `codex_check`) for the Master Codex checks. `wotr_verify.sh` v4, `wotr_beat_check.py` and `wotr_terms.txt` exist nowhere on this machine; nothing below depends on them. Checks are renumbered 1 to 51 with no gaps and no retired stubs.*

## What changed and why

**The tools.** Every "Script (v4)" line is gone. Each check now says what `build/verify.py` does with it, read from its source on 2026-09-26: **FAIL** (the run exits 1), **WARN** (printed, needs a read), **info** (printed, never blocks) or **not automated**. Checks 46–48 say what `build/codex.py check` does. There are no `--scene`, `--convert`, `--entry`, `--codex`, `--dialogue`, `--register`, `--all` or `--preflight` flags any more; the real flags are `--combat`, `--culture` and `--band` (see Running the Checker).

**Checks changed to the live law.**

- **Word count (1)**: the 2,500-word scene minimum is replaced. Roleplay turns run about 3,500 words (R48-28), every reply included (R49-30); set pieces 5,000+ (R48-46).
- **Simile density (3)**: no rate and no ceiling any more; only two similes competing over one beat are flagged (R49-18-SIMILE_COUNT, R48-03-SIMILES).
- **Not-X-but-Y (4)**: the eleven forms stay; the test is now R49-40-NOT_X_Y's: a second sentence that corrects the first fails, plain negation standing alone is free.
- **Emotional signposting (6)**: the body comes first, then the POV may name the feeling in his own word (R49-07-EMOTIONS).
- **NPC italic thoughts (10)**: roleplay turns keep one thought per NPC; written scenes keep the POV lock, so no NPC thoughts at all (R48-40-NPC_THOUGHTS). The POV's own italic thought is now frequent (R49-05-ITALICS).
- **Scene ending (11)**: an action, a concrete image or a line of dialogue; never a summary or a question (R49-26-ENDINGS). A turn may close on a marked cutaway (R49-09-CUTAWAYS).
- **Paragraph variance (12)** stays as it was (R49-14-PARA_SHAPE).
- **Sentence variance (13)**: target CV 80%, under 50% the strongest tell (R49-13-VARIANCE); the short-sentence floor is scene-wide (R49-12-SHORT_FLOOR); the rhythm law holds (R48-06-RHYTHM_LAW).
- **Gloss watch (15)**: technique names and their translations are now free in narration (R49-48-TECH_NAMES), and narration may explain causes (R49-43-EXPLAINING); the zero gloss budget for new WOTR terms stands (R51-15-FIRST_USE).
- **Reification (17)**: no count. Only "never at the beat" and "object first" are kept (R49-21-REIFICATION). The old two-per-scene and one-per-paragraph budgets and `wotr_beat_check.py` check 17 are superseded.
- **Combat checks (30–34)**: the chemistry ban is lifted for trained POVs (R49-46-CHEMISTRY); a trained POV names his own wound exactly (R49-50-OWN_BODY); bare mechanism terms mid-action are legal (R51-17-MID_ACTION).
- **Terminology audit (35)**: stat names, Grades, Stages, eta, EU figures, Sub-Stat names and Guild words are free in narration (R49-47-STAT_WORDS, R51-16-OLD_BANS_FALL, R53-16-GUILD_WORDS); the check is now about spelling only.
- **Conversion density (37)**: science and anatomy terms are legal in narration and off the modern-word list (R49-45-SCIENCE).
- **Entry checks (41–45)**: new abilities use the field format and the six-line card is retired (R47-2-FIELD_FORMAT); an entry says what the ability is, never how to use it (R47-1-NO_APPLICATIONS); counters are facts (R47-3-COUNTERS_AS_FACTS); tiers and rungs by name (R47-7-NAMES_NOT_NUMBERS, R47-5-LADDER_RUNG); costs off the Ledger (R47-4-LEDGER_COSTS). Checks 41 and 42 still name the Operation line, which the field format does not have: logged as **C-078**.
- **Composure (51)**: triads and parallel clauses are dropped from the check (R52-06-TRIADS); the crafted speech still takes the check (R49-35-SPEECH_CHECK), whose own wording keeps "without balanced parallel clauses": logged as **C-077**. Composure itself is free for people trained into calm (R52-28-COMPOSURE, superseding R19-4-COMPOSURE_COST).

**Checks added (all run by `build/verify.py` unless marked).**

- **20, Manufactured fragments**: negative and Only/Just fragments warned at three per scene; concrete fragments free (R49-15-FRAGMENTS).
- **21, '-ing' and 'As he …,' openers** (R49-17-OPENERS).
- **22, Filter verbs** (R49-42-FILTER_VERBS).
- **23, Modern words in narration and documents** (R48-13-PERIOD_FEEL, R49-44-MODERN_FLAGS, R51-03-LIST_SLANG, R51-04-LIST_PSYCH, R51-05-LIST_TECH, R51-34-DOC_MODERN).
- **24, Earth calendar words** (R51-08-CALENDAR).
- **25, Earth holy swears** (R51-30-HOLY_OATHS).
- **26, The hard-ban list** (R51-10-SLOP_WORDS), a FAIL at first use.
- **27, Collision words** (R51-11-COLLISIONS), not automated.
- **28, Foreign words in italics** (R49-49-FOREIGN, R50-32-ITALICS), not automated.
- **29, Signature items per session**: Kharven two of five per session, not per turn (R49-54-KHARVEN); every culture the same (R53-19-QUOTA).
- **44, What it is, never how to use it** (R47-1, R47-3) and **45, Field format** (R47-2, R47-4, R47-5, R47-7), not automated.

**Checks removed.**

- **Narration leak** (old 28): R14-6-CHECK28 is superseded by R49-47-STAT_WORDS. Nothing replaces it.
- **Mechanism gloss and metaphysical units** (old 20 and 21): retired by R12-8-VERIFY_CHECKS_RETIRED in the last edition; their stubs are gone.
- **The simile rate and the 8-per-scene ceiling** (old 3): superseded by R49-18-SIMILE_COUNT.
- **The reification counts** (old 17): R4-15-TWO_PER_SCENE_BUDGET, R4-15-ONE_PER_PARAGRAPH and R4-ADD-CHECK17 are superseded by R49-21-REIFICATION.
- **The 2,500-word minimum as a pass/fail floor** (old 1): replaced as above.
- **Rules the old edition leaned on, now dead, with no check of their own**: the chemistry ban (R6-2-CHEMISTRY_BAN, R13-6-CHEMISTRY_BAN_SCOPE → R49-46), the body-not-converted rule (R16-7-NOT_CONVERTED → R49-50), the composure cost (R19-4-COMPOSURE_COST → R52-28), the funeral test (R5-D-FUNERAL_TEST → R49-38-FUNERAL_TEST), the not-knowing quotas (R6-3-IGNORANCE_QUOTA, R6-4-MISREADING_BUDGET, R12-7-IGNORANCE_MISREADING_RETAINED → R49-11-NOT_KNOWING), the Technical/Mystic no-mixing rule (R12-2-NO_MIXING → R48-10-MIXING), the sheet-vocabulary tiers (R11-2-VOCABULARY_TIERS, R20C-31-SUBSTAT_NAMES_FACULTY_ONLY → R51-16). A reader who remembers flagging any of these should stop.

**Renumbering.** Old 1–19 keep their numbers. Old 20–21 are gone. Old 22–26 (combat) are now 30–34; old 27 is 35; old 29 is 36; old 30–33 are 37–40; old 34–36 are 41–43; old 37–39 are 46–48; old 40–42 are 49–51.

**Logged, not resolved.** Three rows added to `CONFLICTS.md` in the same commit: **C-077** (R49-35 vs R52-06, parallel clauses in the crafted speech), **C-078** (R17-8-CHECK34/35 name an Operation line that R47-2's field format retired), **C-079** (R49-21 "no count" vs the still-live R4-15-PROCEDURAL_SCENE_BUDGET "one per page"). Each check that touches one says so and quotes both sides.

---

# WOTR Manual Verification Guide

*Companion to `build/verify.py`. Run the checker; read this when a check fails, when it warns, and for every check it cannot run. 2026-09-26 edition.*

Every check below carries five lines: **Catches** (what it is looking for), **Enforces** (the rule ids; the rule text governs, this guide only explains it), **verify.py** (FAIL, WARN, info or not automated, and exactly what it counts), **By hand** (how to run it by reading) and **Fix**. Rule ids are `rules/*.yaml` ids; look any of them up with `python build/book_tools.py rule <id>` or the MCP's `rule`.

---

## 0. The Rule Underneath All the Checks

Stylometric research distinguishes machine prose from human prose on **variance**. Human writing shows dispersion. Machine writing is stable. Every check below is a specific instance of that principle. The correction is always deliberate unevenness.

---

## 1. Word Count

**Catches:** a turn or scene that is too short to have built its senses, its interior and its world moving, or a set piece that has not been let run.

**Enforces:** R48-28-TURN_LENGTH ("Roleplay turns run about 3,500 words"), R49-30-SHORT_BEATS ("Every reply is a full turn of about 3,500 words, even to a quick line or question"), R48-46-WORD_FLOOR (set pieces "5,000+"), R49-29-TURN_FILL (the fill: about half texture and talk, half the world moving). Non-scene prose (entries, letters, documents) has no length rule.

**verify.py:** **WARN** outside the band set by `--band`: `standard` and `conversational` both 2,500–4,500 words, `set-piece` 5,000 and up. Inside the band it prints an info line. The count is of sentence words in prose paragraphs (headings, `>` blockquotes and `|` table rows are not counted), and stops at a `## Notes` heading (see Running the Checker).

**By hand:** count the prose body only, notes excluded. A turn near 3,500; a set piece over 5,000.

**Fix:** build what is missing (the senses at an arrival, the POV's running thought, the world moving) rather than padding. Per-scene budgets do not scale with the longer turn; longer turns run tighter (R49-53-BUDGETS).

---

## 2. Em Dashes

**Catches:** the em dash, the en dash, and a double hyphen standing in for either.

**Enforces:** R48-03-SIMILES ("em dashes stay banned"), R15-1-AI_TELL_CHECKS_SURVIVE.

**verify.py:** **FAIL**, with the count. It matches `—`, `–` and a bare `--` anywhere above a `## Notes` heading, headings included.

**By hand:** search the file for `—`, `–` and `--`.

**Fix:** a comma, a colon, a full stop or a new sentence. No exceptions.

---

## 3. Competing Similes

**Catches:** two similes fighting over the same beat. There is no simile rate and no per-scene ceiling any more.

**Enforces:** R49-18-SIMILE_COUNT ("No simile rate or ceiling: only two similes competing over the same beat get flagged"), R48-03-SIMILES ("a good simile is welcome when it earns its place").

**verify.py:** **WARN** for every paragraph with two or more simile markers (`like a`, `like an`, `like the`, `as if`, `as though`). It cannot tell whether the two serve one beat or two; the WARN is a prompt to read. `the way` is not counted.

**By hand:** in each flagged paragraph, ask whether both similes land on the same moment or image. Two similes on two beats pass.

**Fix:** cut the weaker of two that share a beat. Metaphor is a separate budget, drawn from the POV's own life (R48-04-METAPHORS, R49-19-EXTENDED); never cut a metaphor to manage similes.

---

## 4. Not-X-But-Y (All Forms)

**Catches:** the antithesis construction, the most identifiable machine-prose fingerprint there is, in any of its disguises.

**Enforces:** R49-40-NOT_X_Y ("any pair where the second sentence corrects the first fails; plain negation standing alone is free"), R15-1-AI_TELL_CHECKS_SURVIVE.

**The eleven forms** (the base guide's list, kept):

- **4a. Explicit:** `not X but Y` / `not X, Y` — "the tremor was not damage but adaptation"
- **4b. Two-sentence:** `Not X. Y.` — "Not a judgment. An observation."
- **4c. Negation-correction across sentences:** "The array did not radiate from a direction. It filled the room." Many false positives: "He did not raise his voice" followed by "He had learned…" is plain negation and free. The fail is the second sentence *correcting* the first.
- **4d. Nothing/everything:** `nothing to do with X and everything to do with Y`
- **4e. Formal variants:** `not merely`, `not only`, `not so much X as Y`, `less X than Y`
- **4f. Double/triple negation:** "not wind and not radiation and not any force"
- **4g. "Rather than" as antithesis** (see 14)
- **4h. Countdown negation** (see 8)
- **4i. Split across a comma or semicolon:** "a pump that was losing did not announce itself, it simply became gradually less true"
- **4j. Implicit via structure:** a sentence of what it ISN'T followed by one of what it IS, without the word "not"
- **4k. "Which is to say" / "which meant"** correcting an earlier negation

**verify.py:** **FAIL** on three patterns: `not/isn't/wasn't … just/merely/simply/only/so much … but/it's/as/rather` (4a, 4e), `is/was less|more X than Y` (4e), and `it is/was not X, but/it's…` (4a, 4i). The first six hits are printed, then a count. 4b, 4c, 4d, 4f, 4g, 4j and 4k are **not automated** (4h is check 8).

**By hand:** read every `not`, `never`, `no`, `nothing` in narration and ask whether the next clause or sentence corrects it.

**Fix:** state what the thing IS, directly. If you are writing "not X", ask whether you can just write Y.

---

## 5. Banned Constructions

**Catches:** `it wasn't just` / `it isn't just` / `it's not just` and every tense variant: the antithesis at its most naked.

**Enforces:** R49-40-NOT_X_Y; the base guide (2026-08-01).

**verify.py:** **FAIL** when the construction is followed within 80 characters by its correction (`but`, `it's`, `it is`, `as`, `rather`), through check 4's first pattern. A bare "it wasn't just" with no correction is not caught.

**By hand:** search for `just` after a negated `is`/`was`.

**Fix:** as check 4.

---

## 6. Signposting

**Catches:** two things. (a) Structural signposting: `Now that`, `As mentioned`, `As we know`, `It's worth noting`, `It bears mentioning` — the prose narrating its own structure. (b) Emotional signposting: a feeling named with no body under it.

**Enforces:** (a) the base guide, no index row. (b) R49-07-EMOTIONS ("Emotion: show it in the body first; the POV may then name it in his own word"); R49-08-MEANING (the POV may reflect on what a beat meant in his own idiom; neutral narrator summaries stay banned).

**verify.py:** (a) **not automated**. (b) **WARN** on "he/she/they/[Name] felt/was/were [a wave/surge/flicker/pang/rush/stab of] afraid/fear/angry/relief/dread/terror/joy/sad/grief/ashamed/guilt/nervous/anxious/hopeful/despair…".

**By hand:** (a) search for the five phrases. (b) For each WARN, look at the sentences before it: if the body has already shown the feeling and the word is the POV's own, it passes.

**Fix:** (a) cut the phrase and do the thing. (b) put the body first; name it after, in the POV's word, or not at all.

---

## 7. Hypophora

**Catches:** a question asked in narration in order to answer it.

**Enforces:** R49-41-QUESTIONS ("Every question in narration keeps getting flagged for a read as possible hypophora").

**verify.py:** **WARN** for every sentence ending in `?` that has no quotation marks and is not in a paragraph opening with a quote.

**By hand:** read each flagged question and the sentence after it. Questions in dialogue are free. A question left open (a dramatic question, the POV's own unanswered thought) passes. A question answered by the next sentence is the tell.

**Fix:** state the answer, or leave the question genuinely open.

---

## 8. Countdown Negation

**Catches:** the antithesis spread across short sentences so the hinge is invisible in any one of them.

> *Ruin has no shape. The thing behind it has no shape either. No target. No classification. Just weight.*

**Enforces:** R15-1-AI_TELL_CHECKS_SURVIVE ("countdown negation"); R49-40-NOT_X_Y.

**verify.py:** **FAIL** on two or more consecutive sentences of nine words or fewer that each contain `no/not/never/nothing/none/nor`, followed by a sentence starting `Just` or `Only`.

**By hand:** look for a run of negations resolving into "Just" or "Only", including runs with longer sentences the checker skips.

**Fix:** say the last thing, the one that resolves the run, and cut the negations before it.

---

## 9. Distinctive Word Repetition

**Catches:** the reflex adjective or adverb repeated through a scene.

**Enforces:** R49-55-TIC_WORDS ("The repetition tic-word list stays as it is"). The list: `particular`, `arithmetic`, `specific`, `precisely`, `genuinely`, `honestly`, `actually`, `certainly`, `absolutely`, `essentially`, `fundamental`, `significant`, `remarkable`, `incredible`, `literally`, `basically`, `obviously`, `naturally`, `important`, `beautiful`, `different`, `carefully`, `currently`, `extremely`, `perfectly`, `suddenly`, `entirely`, `generally`, `ultimately`, `straightforward`. Setting nouns and character names are expected repeats and excluded. This list is separate from the hard-ban list (check 26).

**verify.py:** **not automated**.

**By hand:** count every word over six letters that appears four or more times; check the list first.

**Fix:** replace with a concrete alternative, or restructure so the sentence does not need it.

---

## 10. NPC Italic Thoughts

**Catches:** a non-POV character's thought on the page where the job does not allow it, or more of them than it allows.

**Enforces:** R48-40-NPC_THOUGHTS ("roleplay turns keep the one-thought-per-NPC allowance; written scenes keep the POV lock (no NPC thoughts under a lock)"). For the POV himself: R49-05-ITALICS ("Italic direct thought appears often, whenever the POV talks to himself"), R48-39-INTERIORITY.

**verify.py:** **info** only: the count of `*…*` spans of three or more words. It cannot tell whose thought a span is, or whether the span is a thought at all (emphasis, a title). The info line still cites "Table Rule 10"; R48-40 governs.

**By hand:** list each italic thought and its owner. Roleplay turn: at most one per named NPC. Written scene or book chapter: none for anyone but the POV. The POV may have as many as the voice wants.

**Fix:** cut the extra NPC thoughts, or carry them in the NPC's body and speech.

---

## 11. Scene Ending

**Catches:** a scene that ends on a summary, a moral, a question, or the narrator stepping back.

**Enforces:** R49-26-ENDINGS ("Written scenes may end on an action, a concrete image, or a line of dialogue; never a summary or a question"); R49-09-CUTAWAYS (a turn may close with a short, clearly marked cut to something the POV cannot see); R49-29-TURN_FILL (a turn stops at the next decision); R49-08-MEANING (neutral narrator summaries banned).

**verify.py:** **WARN** if the last sentence opens `Ultimately`, `In the end`, `And so`, `Finally`, `At last`, `Perhaps that` or `Maybe that`; **info** prints the last 140 characters of the last paragraph. The info line's wording ("must end on physical action, an NPC line, or a thing he can now see") predates R49-26; the rule governs. The last paragraph is the last one above a `## Notes` heading; notes under any other heading (`## Author`, `### Added by the gap-fill`) are read as prose, and the info line then shows them.

**By hand:** read the last line of the prose. Action, concrete image or spoken line passes. Summary, reflection in the narrator's voice, or a question fails. A roleplay turn that stops on Isaac's decision point passes.

**Fix:** end one beat earlier, on the thing done, seen or said.

---

## 12. Paragraph Length Variance

**Catches:** paragraphs that all run the same length.

**Enforces:** R49-14-PARA_SHAPE ("Paragraph-length spread check stays as is (guide wants 50%+, checker warns under 35%); steady paragraphs vary on purpose"); R48-07-WHITE_SPACE (medium paragraphs, white space used sparingly).

Measured by coefficient of variation (CV = standard deviation / mean):

- CV ≥ 50%: good variance
- CV 35–50%: moderate
- CV < 35%: uniform, a tell

**verify.py:** **WARN** under 0.35; **info** prints mean and CV. Needs at least four prose paragraphs and six sentences.

**By hand:** a one-line paragraph is allowed, a 200-word paragraph is allowed; every paragraph at 60–80 words is the failure.

**Fix:** break deliberately: merge two, split one, give a beat its own line.

---

## 13. Sentence Length Variance and the Rhythm Law

**Catches:** sentences of even length, a payoff that is long or subordinated, a scene short of short sentences, paragraphs that close long-long-long, and a beat sentence clogged with conjunctions.

**Enforces:** R49-13-VARIANCE ("Sentence-length variation targets the guide's 80% (under 50% is the strongest tell)"); R49-12-SHORT_FLOOR ("short sentences cluster at beats and in action so the scene clears 18%"); R48-06-RHYTHM_LAW ("the hit is the shortest sentence and sits last, payoffs under 10 words, at most two long sentences in a row; the checker fails anything else"); R4-14-HARD_CEILINGS; R4-14-CONJUNCTION_AUDIT.

Sentence CV: ≥ 80% good; 50–80% moderate; < 50% uniform, the strongest structural tell there is.

| Metric (R4-14-HARD_CEILINGS) | Ceiling |
|---|---|
| Words in the payoff sentence | **10** |
| Subordinate clauses in the payoff sentence | **0** |
| Sentences under 8 words, share of scene | **18% floor** |
| Paragraphs closing on three consecutive sentences over 18 words | **0** |

**Conjunction audit** (R4-14-CONJUNCTION_AUDIT): count *and, as, while, which, because* per sentence. Two or more inside a sentence carrying a beat is a fail. Outside a beat it is style.

**verify.py:**
- Sentence CV: **WARN** under 0.50; **info** prints mean and CV against the 0.80 target.
- Short-sentence share: **FAIL** under 10%, **WARN** under 18%.
- Paragraphs closing on three sentences over 18 words: **WARN** with the count (the rule's ceiling is 0).
- At most two long sentences in a row: see check 16 (FAIL).
- Payoff sentence length, payoff subordinate clauses, "the hit is the shortest sentence and sits last", the conjunction audit: **not automated**. R48-06 says the checker fails these; `verify.py` does not yet (Appendix A).

**By hand:** find each beat's payoff sentence. Is it the shortest in its run, last, under 10 words, with no subordinate clause? Count the coordinators in the sentence carrying the beat.

**Fix:** fragments at impact beats, long clauses at reads and aftermath. Cut the payoff down and move it to the end; split the clogged beat sentence so it carries at most one coordinator.

---

## 14. "Rather Than"

**Catches:** "rather than" doing the work of "not X but Y" (form 4g), the most-overlooked form of the antithesis.

**Enforces:** R49-40-NOT_X_Y; the base guide ("One instance per scene is acceptable. Two or more is a pattern. Three is a tic").

**verify.py:** **not automated** as a count; the antithesis FAIL of check 4 fires on "not just X … rather".

**By hand:** search `rather than`; read each for correction.

**Fix:** as check 4.

---

## 15. Gloss Watch

**Catches:** an appositive or explanatory gloss of a term: "which meant", "which was to say", "meaning that", "in other words", "that is to say", "which is to say", "what that meant was".

**Enforces:** R4-ADD-CHECK15 (warns rather than fails; "the whose-vocabulary test cannot be automated and the FID carve-out is the whole ruling"); R4-13-ZERO_BUDGET ("Zero glosses per scene"); R51-15-FIRST_USE ("New WOTR terms get meaning from context and use only; no appositive gloss (the zero gloss budget stands)"). What is now free and is not a gloss: a technique's name and its translation in narration (R49-48-TECH_NAMES, R50-08-GLOSS_CLASH); narration explaining causes in the POV's reasoning and vocabulary (R49-43-EXPLAINING).

**verify.py:** **WARN** on each of the seven phrases, with context.

**By hand:** for each WARN, whose words are these? If they are the POV's own idiom (free indirect discourse), it passes. If the narrator is glossing a WOTR term for the reader, it fails.

**Fix:** cut the gloss and let context and use carry the term.

---

## 16. Descent: the Chain and the Run

**Catches:** three long sentences in a row; flat stretches of three sentences of near-equal length.

**Enforces:** R4-ADD-CHECK16 ("Fails any chain of 3+ sentences over 25 words. Fails 4+ flat runs."); R4-14-CHAIN_CEILING ("No more than two consecutive sentences over 25 words"); R4-14-RUN_RULE ("No three consecutive sentences within forty percent of each other's word count"); R48-06-RHYTHM_LAW ("at most two long sentences in a row").

**verify.py:**
- Three consecutive sentences over 25 words: **FAIL**.
- Flat runs (three consecutive sentences, the shortest at least 6 words, the longest no more than 1.4 × the shortest): **FAIL** at 4 or more; **info** below 4. Note the checker fails at four runs as R4-ADD-CHECK16 says, while R4-14-RUN_RULE's text makes one run a flaw; read every run.

**By hand:** mark sentence lengths down the margin in the dense stretches.

**Fix:** break the third long sentence, or the paragraph; in a flat run, cut one sentence hard or join two.

---

## 17. Reification

**Catches:** an abstract noun given a physical verb and handled as an object ("The silence sat between them"; R4-15-REIFICATION_DEFINED) carrying a beat, or standing where an object in the room could have done the work.

**Enforces:** R49-21-REIFICATION ("Reification has no count: judge by ear; keep only 'never at the beat' and 'object first'"), which keeps R4-15-NEVER_AT_BEAT ("The value flips on a body or an object, never on a personified noun") and R4-15-CONCRETE_FIRST ("The object always wins"). Bodies are exempt (R4-15-BODIES_EXEMPT). **C-079:** R4-15-PROCEDURAL_SCENE_BUDGET is still live and still reads "One per page in procedural or ledger scenes", against R49-21's "no count". Both are recorded; this guide does not choose.

**verify.py:** **not automated** (the source says so: "reification has no count and 'never at the beat' is a read").

**By hand:** at each beat, what turns the value? If it is a personified abstraction, it fails. Elsewhere, for each reification, is there an object in the room that could carry it? The watchlist nouns (R4-15-WATCHLIST_NOUNS: silence, weight, arithmetic, governance, permission, distance, authority, refusal, grief, history, patience, the question, the cost, the moment, the space between them) make it greppable.

**Fix:** flip the beat on a body or an object; hand the freight to the object.

---

## 18. The Ladder

**Catches:** the chain in which each clause's predicate becomes the next clause's subject: `was X and the X was`, and the `is`, `became` and `meant` variants.

**Enforces:** R6-11-CHECK18_LADDER ("Flag any sentence containing two or more instances"); R6-1-LADDER_BAN ("an automatic cut, never a rewrite. Cut back to the first concrete noun and stop there").

**verify.py:** **FAIL** on two or more in one sentence; **WARN** on one.

**By hand:** read each WARN; count per sentence.

**Fix:** cut back to the first concrete noun and stop.

---

## 19. Apparatus Subject

**Catches:** a named faculty as the grammatical subject of a perception verb ("his Cymorath mapped the thinning").

**Enforces:** R6-11-CHECK19_APPARATUS_SUBJECT ("High false-positive rate by design; review by reading"); R6-2-FACULTY_NEVER_SUBJECT ("The character perceives. The apparatus does not act on its own behalf"). R12-8-VERIFY_CHECKS_RETIRED orders the check "rewritten off §4" (Pack Twelve §4, the four explaining voices); no pack supplies the rewritten wording, so the Pack Six text stands.

**verify.py:** **WARN** on `his/her/the/their` + a faculty (Cymorath, Kamigan, Shingan, Meigan, Reigan, Tengan, Ketsumyōgan, Crown Eye, Seeing, Ruling Sight, Revealing Sight, Spirit Sight, Sky Sight) + a perception verb (saw, read, mapped, noted, caught, found, registered, filed, marked, tracked, perceived, counted, watched, traced, classified, flagged, told, reported).

**By hand:** read each; also look for faculties the list does not know.

**Fix:** the character perceives, or the thing perceived is the subject ("the fourth layer had thinned").

---

## 20. Manufactured Fragments

**Catches:** emphasis faked with short negative or Only/Just fragments ("Not yet." "Only this.").

**Enforces:** R49-15-FRAGMENTS ("Concrete noun and image fragments are free; negative and 'Only/Just' emphasis fragments stay warned at three per scene").

**verify.py:** **WARN** at three or more fragments of one to two words opening `Not`, `Never`, `And`, `Only` or `Just` and ending `.` or `!`. `And` fragments are counted though the rule names only negative and Only/Just ones.

**By hand:** count the emphasis fragments; concrete ones ("Snow. The gate.") are free.

**Fix:** keep the one that earns it; fold the others into their sentences.

---

## 21. '-ing' Openers and Simultaneous Action

**Catches:** "Turning, he drew the blade"; "As he stepped in, the smell hit him".

**Enforces:** R49-17-OPENERS ("added to the AI tells and counted by the checker").

**verify.py:** **WARN** at three or more narration sentences opening with a capitalised `-ing` word followed by a comma within 80 characters, or `As he/she/they/I/we/it/[Name] …,`; **info** at one or two. Speech is stripped first. `During`, `Nothing`, `Something`, `Morning`, `King` and a few other -ing nouns are excluded.

**By hand:** read each listed opener.

**Fix:** two actions in sequence as two clauses or two sentences; one opener per stretch at most.

---

## 22. Filter Verbs

**Catches:** the perception set between the reader and the thing: he saw, he heard, she felt, noticed, watched, realised, sensed, smelled, tasted, wondered, could see/hear/feel.

**Enforces:** R49-42-FILTER_VERBS ("counted by the checker, which warns above a rate").

**verify.py:** **WARN** above 5 per 1,000 narration words (speech stripped); **info** below. The rate of 5 is the checker's own setting (`FILTER_RATE`); Isaac set no number.

**By hand:** for each "he saw the X", try "the X".

**Fix:** give the reader the thing perceived.

---

## 23. Modern Words in Narration and Documents

**Catches:** modern slang and pop-psych in narration; the same in in-world documents.

**Enforces:** R48-13-PERIOD_FEEL ("Modern words in speech only: characters may talk modern; narration keeps a timeless register"); R49-44-MODERN_FLAGS (a checker word list, checked automatically in narration); R51-03-LIST_SLANG (okay, OK, vibe, awesome, cool); R51-04-LIST_PSYCH (triggered, toxic, closure, mindset, boundaries; "anxiety and stress stay"); R51-05-LIST_TECH (technology and office metaphors legal only if the POV's own culture has the thing); R51-34-DOC_MODERN (documents take the list like narration). Exempt: real science and anatomy terms (R49-45-SCIENCE); seconds and minutes (R51-07-CLOCK_WORDS); Earth-derived words like herculean (R51-06-EARTH_WORDS); lens names (R48-22-LENS_NAMES); profanity in close-POV narration (R48-12-PROFANITY, R51-02-CLOSE_POV_SWEARS). Narration may be more antique by culture (R51-01-TIMELESS).

**verify.py:** **WARN** on each of okay, OK, vibe(s), awesome, cool, teenager(s), triggered, toxic, closure, mindset, boundaries in narration (quoted speech stripped). `cool` and `closure` have plain senses; read. R51-05 words are not listed (the checker cannot know the POV's culture). A document checked as its own file or set as a `>` block is treated as narration; a document quoted inside speech marks is stripped with the speech.

**By hand:** for R51-05, ask whether the POV's culture has the thing (an Accord fitter may think "on the main", a Kharven hunter may not).

**Fix:** the timeless word, or move the word into a mouth.

---

## 24. Earth Calendar Words

**Catches:** Earth day and month names, and "week"/"weekend".

**Enforces:** R51-08-CALENDAR ("Earth day and month names never appear; 'week' becomes the culture's own span (a turn, a quarter-moon)").

**verify.py:** **WARN** on each day name, each month name, `weekend(s)`, in narration and speech. `May` and `March` only when capitalised mid-sentence, so "May he…" and the verb "march" pass. `week` itself is not flagged.

**By hand:** search `week`.

**Fix:** the culture's own span.

---

## 25. Earth Holy Swears

**Catches:** God damn it, Christ, go to hell, Jesus, for God's sake.

**Enforces:** R51-30-HOLY_OATHS ("characters swear by their own powers ('Archons take it', 'By the Sky')"); R51-29-SWEARING (each culture's own oaths first).

**verify.py:** **WARN** on each, narration and speech.

**By hand:** read other oaths for Earth religion the list misses.

**Fix:** the culture's own oath (R51-35-NEW_SWEARS: the starter sets await Isaac's approval).

---

## 26. The Hard-Ban List

**Catches:** the stock phrases of machine prose.

**Enforces:** R51-10-SLOP_WORDS: "tapestry, testament, palpable, visceral, symphony of, a dance of, whisper of, orbs (eyes), ministrations, electric (touch), velvet (voice), shiver down the spine, a breath he didn't know he was holding, the coppery tang of blood, the smell of ozone; each fails the checker at first use, narration and dialogue."

**verify.py:** **FAIL** at first use of each, narration and dialogue. "electric" is caught within three words of "touch" either way round; "orbs" in any sense.

**By hand:** nothing to add; trust the FAIL.

**Fix:** the exact concrete detail (R48-01-BEAUTY).

---

## 27. Collision Words

**Catches:** an ordinary word that is also a WOTR term, used in its plain sense.

**Enforces:** R51-11-COLLISIONS ("Ordinary words that are also WOTR terms (delve, echo, numinous, sovereign, sanctum, weave, ledger) are used only in their WOTR sense; the plain adjective or verb is banned so the term stays sharp").

**verify.py:** **not automated**.

**By hand:** search for delve, echo, numinous, sovereign, sanctum, weave, ledger; each hit must be the WOTR sense.

**Fix:** a plain synonym ("dig", "rang back", "wove" → "plaited").

---

## 28. Foreign Words in Italics

**Catches:** foreign in-world words and borrowed names set in italics.

**Enforces:** R49-49-FOREIGN ("Foreign in-world words appear plain, no italics"); R50-32-ITALICS ("Foreign names and borrowed words are never italic in prose"); R50-31-SCRIPT_SHOWN (romanised only, no real script).

**verify.py:** **not automated** (its italic count, check 10, includes these spans and cannot tell them from thought).

**By hand:** read every italic span; a foreign word or name in one fails. Look for kanji or hangul.

**Fix:** remove the italics; let context carry the meaning.

---

## 29. Signature Items per Session

**Catches:** a session that never touches its culture's signature texture.

**Enforces:** R49-54-KHARVEN ("two of the five per session instead of per turn"); R53-19-QUOTA ("Every culture's signature-item quota is two per session, like Kharven's"); R6-9-RECURRENCE_RULE ("Identity is repetition").

**verify.py:** with `--culture Kharven` only: **WARN** if fewer than two of the five Kharven items appear in the file (the woodpile / "how's your stack", the night-stone, wet wood, the Thin Weeks, the death-house / the Waiting); **info** lists those present. No other culture is known to it.

**By hand:** the rule is per session and the checker sees one file, so a WARN on a single turn is not a fail. Across the session, count two of the culture's items (its Standing Inventory in `desktop/inventories/`).

**Fix:** bring an item in where it belongs in the next turn.

---

## 30–34. The Combat Checks (`--combat`)

Pack Thirteen's five checks, run on any fight: **30 and 31 warn, 32 to 34 fail** (R13-9-VERIFY_CHECKS_22_26, where they were numbered 22–26). The rule gives no thresholds. The live law around them: every duel exchange traced (measure, guard and the move by its fencing name; R48-33-CHOREOGRAPHY); wounds in full clinical detail, anatomy named, blood loss minute by minute (R48-34-WOUNDS); cost in the body (R48-37-COST_SHOWN); a full aftermath beat (R48-38-AFTERMATH); bare mechanism terms legal mid-action (R51-17-MID_ACTION); a trained POV names his own wound exactly, an untrained one in plain words (R49-50-OWN_BODY).

## 30. HEMA Density

**Catches:** a fight with no fencing vocabulary.

**Enforces:** R13-9-VERIFY_CHECKS_22_26 (warn); R13-6-HEMA_VOCAB; R48-33-CHOREOGRAPHY.

**verify.py:** with `--combat`: **WARN** if zero HEMA terms (Vor, Nach, Indes, Zornhau, Krumphau, Zwerchhau, Schielhau, Scheitelhau, Absetzen, Durchwechseln, Winden, Mutieren, Duplieren, bind, measure, half-sword, pommel, guard, ward, thrust, cut, tempo, feint, parry, riposte, void, cross, edge, flat, crossguard, quillon, point, counter-cut); **info** gives the count. Case-sensitive.

**By hand:** every exchange names measure, guard and the move.

**Fix:** trace the exchange.

## 31. Anatomical Density

**Catches:** injury without named anatomy.

**Enforces:** R13-9-VERIFY_CHECKS_22_26 (warn); R13-6-ANATOMY_VOCAB; R48-34-WOUNDS; R49-50-OWN_BODY.

**verify.py:** with `--combat`: **WARN** if zero anatomy terms (femoral, carotid, clavicle, radius, ulna, humerus, tibia, fibula, patella, scapula, sternum, rib(s), vertebra, spine, jugular, subclavian, brachial, aorta, lung, liver, kidney, spleen, diaphragm, tendon, ligament, cartilage, orbit, mandible, maxilla, skull, trachea, larynx, hypovol-, haemorrh-/hemorrh-, shock, Class I–IV); **info** gives the count.

**By hand:** each wound names its structure; blood loss tracked. For an untrained POV's own body, plain words are the rule, not a miss.

**Fix:** run `wotr-wound` for the blow and put the anatomy on the page.

## 32. Causal-Connective Density in Fight Passages

**Catches:** a fight passage that says what happened and never why it worked.

**Enforces:** R13-9-VERIFY_CHECKS_22_26 (fail). Narration may state the cause of any penetration outright (R53-05-PROOF_PLATE) and explain causes anywhere (R49-43-EXPLAINING).

**verify.py:** **not automated**.

**By hand:** in each fight passage, can the reader say why each decisive exchange went the way it did?

**Fix:** give the cause on the page.

## 33. A Stated Fault per Named Technique

**Catches:** a named technique performed with no structural weakness shown.

**Enforces:** R13-9-VERIFY_CHECKS_22_26 (fail); R48-14-DEPTH ("name the real phenomenon and its fault").

**verify.py:** **not automated**.

**By hand:** list the named techniques; each has its fault on the page.

**Fix:** state the fault.

## 34. A Reserve Account per Working

**Catches:** a working with no cost account.

**Enforces:** R13-9-VERIFY_CHECKS_22_26 (fail); R48-37-COST_SHOWN; R48-20-STRATA (the Aether, Wellspring and Essence account at a working's first display and at the finisher); R47-8-WASTE_IS_HEAT; R47-11-TIME_AND_ENERGY (a combat turn is six seconds).

**verify.py:** **not automated**.

**By hand:** each working's draw against the reserve shows on the page (in the body) and in the notes.

**Fix:** write the account, from the stat line (`wotr-stat-line`).

---

## 35. Terminology Audit

**Catches:** a misspelled capitalised system term.

**Enforces:** R14-6-CHECK27 ("Near-misses (edit distance one or two from a canonical term) fail"). The terms themselves are free in narration: R49-47-STAT_WORDS, R51-16-OLD_BANS_FALL, R51-14-NEW_TERMS (no ceiling per page), R53-16-GUILD_WORDS (Guild words in any mouth). So this is a spelling check only.

**verify.py:** **not automated**. `wotr_terms.txt` does not exist. `build/codex.py check` (check 46) catches ruled misspellings (Crymorath → Cymorath) and Latinate coinages not on the Lists sheet, which covers part of this.

**By hand:** check each capitalised system term against the Codex (`codex "<term>"`), the character card and The Core Vocabulary.

**Fix:** the canonical spelling.

---

## 36. The Loadout

**Catches:** a named practitioner in the scene with no Stat Ledger in the notes.

**Enforces:** R14-6-CHECK29 ("The author notes contain a Stat Ledger for every named practitioner … or the run fails"); R48-47-NOTES ("Full author notes go in the scene file (rule ids, stat ledger, research, costs); chat gets a short summary").

**verify.py:** **not automated**.

**By hand:** count the named practitioners; count the ledgers. The numbers match.

**Fix:** write the ledger (`wotr-stat-line`).

---

## 37. Conversion Density

**Catches:** a working, exchange or injury written with no technical vocabulary.

**Enforces:** R16-8-CHECK30 ("at least four terms from the WOTR technical lexicon and at least two correctly-used real scientific or anatomical terms, in the narration, outside italics"). Now legal in narration: science and anatomy terms (R49-45-SCIENCE); science reads by any trained POV, scenery included (R49-46-CHEMISTRY, lifting the chemistry ban); technical words on the narration's own authority (R48-09-TECH_WORDS).

**verify.py:** **not automated** (its `--combat` counts, 30 and 31, are the nearest).

**By hand:** in a scene with a working, exchange or injury, count WOTR terms and real technical terms in narration outside italics: four and two.

**Fix:** convert the mechanism, the read, the wound.

---

## 38. Export

**Catches:** a mechanism term that lives in the author notes and never reaches the prose.

**Enforces:** R16-8-CHECK31.

**verify.py:** **not automated**.

**By hand:** list the mechanism terms in the notes; search the body for each.

**Fix:** the term goes into the body.

---

## 39. Coinage Retention

**Catches:** a distinctive term from Isaac's rough that vanished.

**Enforces:** R16-8-CHECK32 ("Every distinctive term in the submitted rough appears in the output in one of the four routed forms, or is listed as dropped in the notes").

**verify.py:** **not automated** (it has no rough).

**By hand:** list the rough's coinages; find each in the output or in the notes' dropped list.

**Fix:** route it or list it.

---

## 40. Italic Quarantine

**Catches:** technical terms hidden inside italic thought.

**Enforces:** R16-8-CHECK33 ("Fewer than half of a scene's technical terms sit inside italic thought").

**verify.py:** **not automated**.

**By hand:** count technical terms inside italic thought against all of them. Half or more fails.

**Fix:** move terms into narration until fewer than half sit in italics.

---

## 41–45. Entry Checks (abilities, techniques, Traits)

Run on an ability or technique entry, not a scene. `build/verify.py` has no entry mode; run it on an entry only for the prose checks (em dashes, antithesis, hard-ban words) and ignore the length band. Everything in 41–45 is by hand. The live format is R47-2-FIELD_FORMAT: "the card top (Summary card, Codex line, FOW line, Origin) followed by the Physics, Metaphysics, Mechanism, Essence and Counterplay blocks, each a set of one-line **Field** · value entries. The Design Chain and the six-line card are retired as page formats." The template is `.claude/skills/wotr-write/references/technique-design.md`.

## 41. The Four Elements

**Catches:** a mechanism missing its quantity, its law, its operation or its causal chain.

**Enforces:** R17-8-CHECK34 ("Quantity, law, operation and chain all present in the Operation line. Any absence is a FAIL"); R47-6-RESEARCH_STAYS; R48-18-INVENTION (the real law plus one pinned variable); R48-17-NO_CLOSURE (researched pseudoscience or metaphysics where physics cannot close). **C-078:** the "Operation line" belonged to the six-line card (R17-3-SIX_LINE_CARD, superseded), and R47-2 retires that card; a field-format entry has no Operation line. Both rules are live and recorded; this guide does not say where the four elements must now sit. Until ruled, read the entry's Physics and Mechanism blocks for the four and report where each was found.

**verify.py:** **not automated**.

**By hand:** name the quantity, the law, the operation and the chain, each with its line.

**Fix:** write the missing element.

## 42. Derivation

**Catches:** a cost, limit or counter that does not follow from the mechanism.

**Enforces:** R17-8-CHECK35 ("For each of Cost, Limit and Counter, name the sentence in the Operation it follows from. Anything that cannot be traced is decoration and is cut or re-derived"); R47-6-RESEARCH_STAYS ("the cost and the limits are derived from the mechanism"). **C-078** as check 41.

**verify.py:** **not automated**.

**By hand:** for each cost, limit and counter field, name the mechanism line it follows from.

**Fix:** cut or re-derive.

## 43. The Assertion Sweep

**Catches:** a phrase that states an outcome in place of a process.

**Enforces:** R17-8-CHECK36: *is assayed*, *is converted*, *is transferred*, *responds to*, *is affected by*, *is empowered by*, *resonates with*, *attunes to*.

**verify.py:** **not automated**.

**By hand:** `grep -niE "is assayed|are assayed|is converted|are converted|is transferred|are transferred|responds to|is affected by|are affected by|is empowered by|resonates with|attunes to" entry.md`

**Fix:** replace with the operation it stands in for, or delete.

## 44. What It Is, Never How to Use It

**Catches:** tactics, combos, worked fights or advice in an ability entry; counters written as instructions.

**Enforces:** R47-1-NO_APPLICATIONS ("An ability entry describes what the ability is, never how to use it … No tactics, combos, worked fights or lines telling the reader how to use it; the owner invents the applications"); R47-3-COUNTERS_AS_FACTS ("written as facts only: what the ability cannot survive and what gives it away, never an instruction to an opponent"); R47-12-MYSTERY_STAYS_OPEN (a What-nobody-knows question is never answered as fact); R48-35-USES.

**verify.py:** **not automated**.

**By hand:** read for imperatives and second person ("use it to", "pair it with", "an opponent should"), worked examples, and counters phrased as advice.

**Fix:** restate as a fact of the ability or cut.

## 45. Field Format, Costs and Rungs

**Catches:** an entry in a retired format, a cost not read off the Ledger, a missing or numbered rung.

**Enforces:** R47-2-FIELD_FORMAT; R47-4-LEDGER_COSTS ("A new ability's cost is a share of full reserve. Its EU and joule figures are read off the Essence Ledger's bands for its Stage, and its Grade off the joules to Grade to tier spine"); R47-5-LADDER_RUNG (every new item, draught, summon, Domain, Wellspring site, weapon or beast carries its Tier Ladder rung by name); R47-7-NAMES_NOT_NUMBERS; R47-9-INHERITED_FAILURES; R47-10-STATS_ARE_THE_CASTERS.

**verify.py:** **not automated**.

**By hand:** card top present (Summary card, Codex line, FOW line, Origin); the five blocks present as one-line **Field** · value entries; the cost as a share of reserve with EU and joules from the Ledger band; the rung by name; no tier written as a number; inherited Wellspring failures listed.

**Fix:** convert to the field format; read the figures off the Ledger.

---

## 46–48. The Master Codex Checks (`build/codex.py check`)

Pack Eighteen's checks, run by `build/codex.py check draft.md` or the MCP's `codex_check(markdown)`, against `$WOTR_TRUE_CANON/The Master Codex.xlsx`. The body is everything above the first `## Notes`, `## Author` or `### Added by the gap-fill` heading. The run exits 1 on any FAIL and ends `CLEAN` or `N FAIL`. Narration may name Wellsprings and glyphs freely (R48-21-NAMING).

## 46. Controlled Vocabulary

**Catches:** a Wellspring, Family, Physics Domain, Temperance stage, Archon, Titan, Glyph Class, alchemical Tier or Type not on the Lists sheet.

**Enforces:** R18-7-CHECK37 ("Anything absent is a FAIL and must be either corrected or explicitly declared as a proposed new entry with the checked enumeration named").

**codex.py:** **FAIL** on a ruled misspelling (Crymorath); **FAIL** on a capitalised Latinate coinage (ending -atio, -antia, -orath, -ivale, -thrae, -ilithe, -aeon) that is not in any Lists column or the glyph names, unless it sits on a line containing "proposed"; **PASS** lists the Lists terms used. A coinage not Latinate-shaped is invisible to it.

**By hand:** for any other named Wellspring, Family, Archon and so on, `codex "<term>"`.

**Fix:** correct the term, or declare it proposed and name the enumeration checked.

## 47. Glyph Validity

**Catches:** a bracketed glyph token not in the Master Glyph Index.

**Enforces:** R18-7-CHECK38 ("Unknown tokens FAIL").

**codex.py:** **FAIL** on any `[Xx]` token (a capital and up to five letters) not in the Index; **WARN** if there are none; **PASS** with the count.

**Fix:** the canonical token.

## 48. Precedent

**Catches:** a new working written without checking whether it already exists.

**Enforces:** R18-7-CHECK39 ("Manual. For any new working, name the Spell Index rows checked and state whether the working is new, a derivation of a named row, or a duplicate").

**codex.py:** **WARN** always, listing Spell Index names found in the body as a start.

**By hand:** name the rows checked and give the verdict in the notes.

---

## 49–51. The Dialogue Checks

## 49. Fidelity

**Catches:** Isaac's dialogue changed.

**Enforces:** R19-7-CHECK40 ("Every line of Isaac's dialogue appears verbatim except for the corrections permitted in §2. Any other change is a FAIL and is reverted"); R52-08-PC_IDIOM; R52-10-CROSSOVER.

**verify.py:** **not automated** (it has no rough).

**By hand:** diff the output against the rough.

**Fix:** revert.

## 50. Prosody

**Catches:** stretched vowels, repeated punctuation or capitalised shouting in the rough that the output flattened.

**Enforces:** R19-7-CHECK41.

**verify.py:** **not automated**.

**By hand:** search the rough for `aaa`-style stretches, `!!`, `?!`, and capitals in quotes; each survives in the output.

**Fix:** restore it.

## 51. Composure

**Catches:** dialogue lines that are long or subordinate-heavy under duress, and a scene where every speaker's lines cluster at one length.

**Enforces:** R19-7-CHECK42 ("Flags dialogue lines that are long, subordinate-heavy, or contain parallel constructions, and reports the spread of line lengths across the scene"), as narrowed by R52-06-TRIADS ("Triads and parallel clauses are legal in any mouth, under duress included; the composure check drops them"). R49-35-SPEECH_CHECK: "No exemption for the crafted speech: even it must pass the composure check, eloquent without balanced parallel clauses" (the one crafted speech of R48-43-SPEECHES). **C-077:** R52-06 drops parallel clauses from the check; R49-35 keeps "without balanced parallel clauses" for the crafted speech. Both are recorded; this guide does not choose. Until ruled, report any balanced parallel clause in the crafted speech as a C-077 item rather than a pass or a fail. Also: composure is free for people trained into calm and costs only under real strain (R52-28-COMPOSURE); under stress, named humans shorten and the card's stress tell rides on it (R52-25-STRESS_RULE); speaker-swap is by ear, no numbers (R52-07-SWAP_CHECK).

**verify.py:** **not automated**.

**By hand:** list the dialogue lines under duress; flag the long and the subordinate-heavy ones and read them against the speaker's card. Look at the spread of line lengths by speaker. Cover the tags and sort the lines by ear.

**Fix:** shorten under duress unless the card says this person holds; give each speaker their own length.

---

## Running the Checker

The live checker is `build/verify.py`. From the repo, in the project's interpreter:

```bash
# A roleplay turn (default band: standard, 2,500–4,500 words)
bash build/py.sh build/verify.py draft.md

# A set piece (5,000+), a fight, on the Kharven thread
bash build/py.sh build/verify.py draft.md --band set-piece --combat --culture Kharven

# The other band name (same 2,500–4,500 range as standard)
bash build/py.sh build/verify.py draft.md --band conversational

# Checks 46–48 against The Master Codex
bash build/py.sh build/codex.py check draft.md
```

The flags, from its argparse, are all there is:

| Flag | Effect |
|---|---|
| `file` (required) | the draft, read as UTF-8 |
| `--band conversational\|standard\|set-piece` | length band for check 1; default `standard` |
| `--combat` | turns on checks 30 and 31 |
| `--culture X` | only `Kharven` does anything (check 29, case-insensitive) |

It prints `PASS` or `FAIL: n fail, n warn`, then one line per `FAIL`, `WARN` and `info`, each naming its rule. It exits 1 if anything failed, 0 otherwise.

**The same checker through the wotr MCP:** `verify_scene(markdown, combat=False, culture="", band="standard")` takes the draft text, not a path, and returns the same report (it imports `verify.py` and calls it). `codex_check(markdown)` does the same for `codex.py check`. Without the MCP, `python build/book_tools.py verify <file> --band set-piece [--combat] [--culture Kharven]` runs `verify_scene` from the shell.

**What it reads.** Everything from the first line starting `## Notes` down is cut before any check runs; notes under any other heading (`## Author`, `### Added by the gap-fill`, `### Notes`) are checked as prose, so an em dash or a hard-ban word there fails the run. Then Markdown headings and `---` rules are removed and `**bold**` unwrapped; paragraphs opening `>` or `|` are left out of sentence and length statistics but not out of the bans. `codex.py check` cuts at `## Notes`, `## Author` or `### Added by the gap-fill`. Checks 21–23 strip quoted speech first; checks 24–26 run on narration and speech both.

**Where it runs by itself.** In the Natalie clone (`~/wotr-natalie`, `.natalie` marker), the Stop hook (`build/natalie_hook.py`) runs `verify.py` on every reply over 120 words and blocks the reply on any FAIL. The coding checkout has no marker.

**Workflow:**
1. Write the draft to a file.
2. Run `build/verify.py` with the band and flags the draft needs (and `build/codex.py check` if it names Codex terms or glyphs).
3. Fix every FAIL.
4. Read every WARN against its section here.
5. Run the by-hand checks for everything marked **not automated** that applies.
6. Re-run until clean.
7. Present to Isaac.

**No single-pass delivery.** R4-ADD-NO_SINGLE_PASS: "Both scripts run before presenting, failures are fixed, both re-run. No single-pass delivery." The two scripts it names are gone; `build/verify.py` now carries what `wotr_beat_check.py` scripted (gloss watch and descent; reification is a read, check 17). The re-run after fixing is the part of the rule that still binds. **Every roleplay turn takes the full check** (R48-45-CHECKS).

**The checker is a floor, not a ceiling.** It catches the mechanical tells. It does not catch:
- Voice (could the line be moved to another speaker; R52-02-VOICE_LEVER, R52-07-SWAP_CHECK)
- Psychic distance and whose head we are in (R49-01-WHOSE_HEAD, R49-03-BAND_CAPS)
- Value turn (did the scene turn something)
- Overcrowded beats (revelation + threat + philosophy stacked)
- Exposed subtext (a line followed by its own explanation)
- Texture: one detail per beat that could only exist in this world (R53-30-TEXTURE_DENSITY), looked up, not invented (R53-29-LOOK_UP)

Those require reading. A check marked **not automated** is still a check: it runs by reading, in the same pass, and its result is reported with the rest.

---

## Adding New Checks

When a new tell is identified in a session, add it to both this document and `build/verify.py`, citing the rule id in the finding text the way the existing checks do. If a tell survives the checker, the checker is wrong, not the tell. A threshold the rule does not give (like `FILTER_RATE`) is set in the script with a comment saying so.

---

## APPENDIX A — Gaps Between the Rules and the Tools

Carried forward, not fixed here; this guide describes `verify.py`, it does not amend it.

- **R48-06-RHYTHM_LAW says "the checker fails anything else"**; `verify.py` fails only the chain ceiling. Payoff length, payoff subordination and "the hit is the shortest sentence and sits last" are by hand (check 13).
- **Only a `## Notes` heading ends the body for `verify.py`.** Notes under `## Author`, `### Added by the gap-fill` or `### Notes` are checked as prose; `codex.py` cuts at the first two as well.
- **Two info lines carry pre-R48 wording**: the italic count cites "Table Rule 10: one per named NPC per scene" (R48-40 now splits roleplay from written scenes) and the last-line line says "physical action, an NPC line, or a thing he can now see" (R49-26 says action, concrete image or line).
- **The signature-item WARN is per file**; R49-54 and R53-19 are per session. Only Kharven is known to it.
- **Not automated at all**: 4b–4d, 4f, 4g, 4j, 4k, 6a, 9, 13 (payoff rows, conjunctions), 14, 17, 27, 28, 32–45, 49–51. The old flags that ran some of these (`--convert`, `--entry`, `--dialogue`) do not exist.
- **`wotr_terms.txt` does not exist**, so check 35 is by hand.
- **Check 19's rewrite off Pack Twelve §4 is ordered and unwritten** (R12-8-VERIFY_CHECKS_RETIRED).
- **The combat checks have names and severities and no thresholds** (R13-9-VERIFY_CHECKS_22_26); `verify.py` warns only on a count of zero.
- **Open rows touching this guide:** C-077 (check 51), C-078 (checks 41–42), C-079 (check 17).
