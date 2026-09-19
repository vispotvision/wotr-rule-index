# CHANGELOG — 2026-09-12 EDITION

*This edition folds every rule in `wotr-rule-index/rules/*.yaml` marked `status: live` whose `amends` block names `WOTR_Manual_Verification_Guide.md` or `Manual Verification Guide` — 23 rules across Packs Four, Six, Twelve, Thirteen, Fourteen, Sixteen, Seventeen, Eighteen, and Nineteen. The original file, `WOTR_Manual_Verification_Guide.md` (dated 2026-08-01, recovered from Downloads today; it predates Pack Four's checks 15 and up), is untouched; this is a new document. Section numbers below refer to the numbering used **in this edition**: the base guide's §1–§14 are its checks 1–14, and from §18 onward the section number is the check number as the packs assign it. The companion script is `wotr_verify.sh` v4 (`Downloads\WOTR_Session_Bundle\WOTR_Session\tools\`, read read-only for this pass); every new section says what v4 actually does with its check, which is not always what the pack ordered.*

## Pack Four (`WOTR_Companion_Guide_Amendments_Pack_Four.md`) — 3 rules

- **R4-14-HARD_CEILINGS** — adds four hard ceilings on payoff sentences and paragraph shape (payoff sentence at most 10 words and 0 subordinate clauses; at least 18% of the scene's sentences under 8 words; no paragraph closing on three consecutive sentences over 18 words) beneath the document-level CV. Two rows are measured at the payoff sentence, one across the scene, one at the paragraph close. §13.
- **R4-14-CONJUNCTION_AUDIT** — adds the conjunction audit: two or more of *and, as, while, which, because* inside a beat-carrying sentence is a fail; outside a beat it is style and left alone. §13.
- **R4-ADD-NO_SINGLE_PASS** — adds the two-script rule: `wotr_verify.sh` and `wotr_beat_check.py` both run before presenting, failures fixed, both re-run, no single-pass delivery. `locus: null` in the index; landed in Running the Script.

## Pack Six (`WOTR_Companion_Guide_Amendments_Pack_Six.md`) — 2 rules

- **R6-11-CHECK18_LADDER** — adds check 18, the Ladder: two or more instances of `was X and the X was` in one sentence, plus the *is / became / meant* variants. §18.
- **R6-11-CHECK19_APPARATUS_SUBJECT** — adds check 19, apparatus subject: a named faculty as the grammatical subject of a perception verb; false-positive by design, cleared by reading. §19 (with Pack Twelve's rewrite directive attached, see below).

## Pack Twelve (`WOTR_Companion_Guide_Amendments_Pack_Twelve.md`) — 1 rule

- **R12-8-VERIFY_CHECKS_RETIRED** — retires checks 20 and 21 (Pack Seven's mechanism gloss and metaphysical units; both `status: superseded` in the index, text not carried here) and directs that check 19 be rewritten off Pack Twelve §4, the four explaining voices. §19; §20 and §21 stand as marked retired stubs.

## Pack Thirteen (`WOTR_Companion_Guide_Amendments_Pack_Thirteen.md`) — 1 rule

- **R13-9-VERIFY_CHECKS_22_26** — adds the `--combat` flag and checks 22 (HEMA density, warn), 23 (anatomical density, warn), 24 (causal-connective density in fight passages, fail), 25 (a stated fault per named technique, fail), 26 (a reserve account per working, fail). §22–§26.

## Pack Fourteen (`WOTR_Companion_Guide_Amendments_Pack_Fourteen.md`) — 3 rules

- **R14-6-CHECK27** — adds check 27, terminology audit: capitalised system terms matched against `wotr_terms.txt`; unknown terms listed; near-misses fail. §27.
- **R14-6-CHECK28** — adds check 28, narration leak: any Grade letter, Stage name, Band, eta, AU/s, EU figure or Sub-Stat name outside quotation marks, italics or a marked document block fails. §28.
- **R14-6-CHECK29** — adds check 29, the loadout: a Stat Ledger in the author notes for every named practitioner, or the run fails. §29.

## Pack Sixteen (`WOTR_Companion_Guide_Amendments_Pack_Sixteen.md`) — 4 rules

- **R16-8-CHECK30** — adds check 30, conversion density: a scene with a working, exchange or injury carries at least four WOTR technical-lexicon terms and at least two real scientific or anatomical terms in narration, outside italics. §30.
- **R16-8-CHECK31** — adds check 31, export: no mechanism term in the author notes that is absent from the prose body. §31.
- **R16-8-CHECK32** — adds check 32, coinage retention: every distinctive term in the submitted rough appears in one of the four routed forms or is listed as dropped. §32.
- **R16-8-CHECK33** — adds check 33, italic quarantine: fewer than half a scene's technical terms inside italic thought. §33.

## Pack Seventeen (`WOTR_Companion_Guide_Amendments_Pack_Seventeen.md`) — 3 rules

- **R17-8-CHECK34** — adds check 34, the four elements: quantity, law, operation and chain all present in the Operation line. §34.
- **R17-8-CHECK35** — adds check 35, derivation: Cost, Limit and Counter each traced to a sentence in the Operation, or cut and re-derived. §35.
- **R17-8-CHECK36** — adds check 36, the assertion sweep: the listed outcome-for-process phrases replaced with the operation or deleted. §36.

## Pack Eighteen (`WOTR_Companion_Guide_Amendments_Pack_Eighteen.md`) — 3 rules

- **R18-7-CHECK37** — adds check 37, controlled vocabulary: every named Wellspring, Family, Physics Domain, Temperance stage, Archon, Titan, Glyph Class, alchemical Tier and alchemical Type validated against the Lists sheet. §37.
- **R18-7-CHECK38** — adds check 38, glyph validity: every bracketed glyph token validated against the Master Glyph Index. §38.
- **R18-7-CHECK39** — adds check 39, precedent (manual): the Spell Index rows checked, and new / derivation / duplicate stated, for any new working. §39.

## Pack Nineteen (`WOTR_Companion_Guide_Amendments_Pack_Nineteen.md`) — 3 rules

- **R19-7-CHECK40** — adds check 40, fidelity (manual): Isaac's dialogue verbatim against the rough except the Pack Nineteen §2 corrections; any other change fails and is reverted. §40.
- **R19-7-CHECK41** — adds check 41, prosody: stretched vowels, repeated punctuation or capitalised shouting present in the rough and absent from the output is a fail. §41.
- **R19-7-CHECK42** — adds check 42, composure: long, subordinate-heavy or parallel dialogue lines flagged; the spread of line lengths reported. §42.

## Judgment calls (every decision flagged; none silent)

1. **Checks 15–17 are cross-referenced, not folded.** Pack Four's Addendum puts the gloss watch, descent and reification checks in `wotr_beat_check.py`, and their index rows (R4-ADD-CHECK15, R4-ADD-CHECK16, R4-ADD-CHECK17) amend that script, not this guide, so they are outside the 23. But R4-ADD-NO_SINGLE_PASS, which *is* one of the 23, makes the second script mandatory, and a guide that runs 14 → 18 with no explanation would be worse than a signpost. §15–17 is a one-paragraph cross-reference naming the three checks, the amendment each enforces, and their home. No substance from those three rules is folded.
2. **R4-ADD-NO_SINGLE_PASS carries `locus: null`.** Placed in Running the Script, the only section that describes the run, directly after the base workflow list. The list itself is preserved unchanged rather than edited to say "scripts".
3. **Checks 20 and 21 stand as retired stubs, name only.** R12-8 retires them. R7-6-CHECK20 and R7-6-CHECK21 are `status: superseded` and their text is not carried (superseded rules are ignored per the brief). "Mark retired in place" is honoured by keeping the numbers, a heading, the retiring rule, and a pointer to the index for the historical wording. This edition says nothing about what those checks did beyond their titles.
4. **Check 19 is folded as Pack Six wrote it, with Pack Twelve's directive attached rather than executed.** R12-8 says "Check 19 rewritten off §4" (Pack Twelve §4, the four explaining voices). No pack in the corpus contains the rewritten wording, and the index row's own note says so. Writing the rewrite here would be inventing a rule. §19 carries the Pack Six text, a marked note that a rewrite is ordered and unwritten, and an observation that v4's check 43 (under `--register`) carries a manual "no more than two explaining voices" warn, named as the nearest thing in the script, explicitly not as the rewrite.
5. **R4-14-HARD_CEILINGS folds four rows, not five.** The Pack Four source table has a fifth ceiling (two consecutive sentences over 25 words). The rule's `verbatim` carries only the four rows listed above, and no other rule in the fold set carries the fifth. Four rows are folded; the fifth is noted here so it is not mistaken for an omission by accident.
6. **Section numbers equal check numbers from §18 on.** The base guide's §1–§14 are also its checks 1–14, so the packs' numbering continues the guide's own. The `## N.` heading form is kept; retired numbers keep their heading with `— RETIRED` appended; 22–26 get one preamble and one heading each.
7. **Every new section carries a "Script (v4)" line, and two paragraphs in Running the Script describe v4's note-stripping and flags.** Those are descriptions of the companion script, written from the script file, not rules. Where v4 does not implement a check the line says so; where v4's implementation is narrower or looser than the rule the line says how. No discrepancy is resolved in either direction: the rule text governs the check, the script line reports the tool. The exception is §13, whose two **Script** lines refer to `wotr_beat_check.py`; that file is not in the bundle, so those lines are written from R4-ADD-CHECK16's published description in Pack Four, not from the script, and they say so. One further editorial sentence, at the end of "floor, not a ceiling", rolls up which checks are manual: it separates the checks whose rule text says *Manual* (39, 40) from those v4 runs as a warn only (32, 35, 40; 34 past its label count) and those v4 lacks (18, 19, 22–29), and asserts nothing beyond the rule text and the Script lines above it.
8. **Checks 18, 19, 22–29 are not in v4 as numbered checks.** Packs Six, Thirteen and Fourteen each say the checks are appended, or will be on Isaac's word; the v4 file in the bundle does not carry them. Each is described from its rule text and marked manual until scripted. v4's check 45 (combat floor counts) and check 46 (numbers attached to system quantities) are named as the nearest script behaviour for 22–23 and 28 respectively, explicitly not as those checks.
9. **The usage block in Running the Script is extended, not replaced.** The base's two command lines are kept byte-for-byte; flag lines for `--combat`, `--convert`, `--entry`, `--codex`, `--dialogue`, `--all` and `--preflight` are added after them from the script's own usage header and the rules' `verification` fields. `--register` (checks 43–49) is named only to say that no rule in the index assigns it to this guide.
10. **Threshold and scope edges between rule and script, reported and left standing.** Check 33: the rule says *fewer than half*; v4 passes at exactly half. Check 34: v4 also demands a Manifestation line, which the rule does not name. Check 36: v4 also greps *is imbued* and *channels the power*, which the rule does not list. Check 37: v4's `codex_check.py` validates five of the rule's nine enumerations and only Latinate-suffixed candidates. Check 41: v4 cannot see the rough, so it warns on absence in the output instead of failing on a dropped mark. Check 42: the rule flags a clustered file for reading; v4 fails it. Each is stated at its section; none is corrected here.
11. **Check 30's "no working performed" exemption is script behaviour, not a folded rule.** v4 warns rather than fails when a scene has under five working-references, citing Pack Sixteen §7. That rule does not amend this guide and is not one of the 23; §30 reports the script behaviour with its citation and folds nothing from Pack Sixteen §7.
12. **The combat checks 22–26 are folded at the level of detail the rule gives.** R13-9 names five checks and their severities and nothing else: no thresholds, no term lists. Each section names the check, its severity, and points at the Combat Craft Guide's technical floor (which the script header itself cites as the checks' source) for what is being measured. The one-line gloss under 24, 25 and 26 says only what the check's own name says; where the name uses a term of art (the fault, the reserve account), the section quotes or points to the Combat Craft Guide §6 for its meaning rather than defining it here.
13. **No conflict among the 23.** Two loci are shared: §13 (two Pack Four rules, both `adds`, building one feature) and check 19 (R6-11-CHECK19_APPARATUS_SUBJECT, locus "check 19", and R12-8-VERIFY_CHECKS_RETIRED, locus "checks 19-21"). The Pack Twelve / Pack Six interaction at check 19 is a directive without a replacement, not a contradiction. Nothing in the body is marked "(conflict — see changelog)".
14. **No proposed rules name this guide.** The index query returned 23 live and 2 superseded rows, nothing `proposed` or `pending`, so there is no Appendix B (proposed items) rather than an empty one.
15. **Base passages no rule touches are preserved byte-for-byte**, including §0–§12, §14, the "floor, not a ceiling" list and Adding New Checks, verified by a script comparison after writing.
16. **Editorial prose beneath the rule text.** Besides the Script lines, this edition adds three kinds of non-rule text, all of it outside the bolded rule sentences and their rule-ID tags: (a) an edition-stamp paragraph under the base title; (b) a one- or two-sentence gloss under the rule in §13, §18, §19, §27, §28, §31 and §33, and pointer sentences in §37 and §39 naming which Master Codex sheet the rule's list lives on; (c) a "**The fix:**" line in §13, §18, §27, §28, §29, §31 and §33. Every gloss restates the rule's own condition in other words and every fix line is the inverse of that condition (the flag is two rungs, so the fix is fewer than two; the flag is a term outside the three containers, so the fix is inside one or cut); none names a remedy, threshold or scope the rule does not. Where a first draft of this edition did (§19's "change the subject", §38's "add the glyph to the Index first", §25's definition of the fault, §28's narrowing of the containers, §13's "and last"), it has been struck; §38 now carries no fix line because R18-7-CHECK38 gives none. §37's fix sentence is the rule's own. These additions are editorial and carry no rule authority; the bolded text is the rule.

## Flagged gaps carried forward

- **`wotr_beat_check.py` is not in the session bundle** (`tools/` holds only `wotr_verify.sh` and `codex_check.py`), and neither is `wotr_terms.txt`, though both are named as mandatory (R4-ADD-NO_SINGLE_PASS; R14-6-CHECK27 and v4's own preflight manifest). Until they are restored, checks 15–17 and 27 are manual.
- **v4 does not implement checks 18, 19, 22, 23, 24, 25, 26, 27, 28, 29.** Its header comment still lists 19 and 20 among the false-positive-by-design checks, and 20 is retired.
- **v4's `--codex` failures do not reach the summary line.** `codex_check.py`'s non-zero exit increments a variable named `FAILURES`; the summary and the "FIX N FAILURE(S)" verdict read `FAIL`. A run can print a glyph or vocabulary failure and still end "CLEAN — READY TO PRESENT". The fix belongs in the script; noted here so nobody trusts the summary line on a `--codex` run.
- **v4's `--all` does not include `--entry`.** It expands to `--scene --combat --convert --codex --dialogue --register`. Checks 34–36 need the flag passed by hand.
- **Check 19's rewrite off Pack Twelve §4 is ordered and unwritten.** Pack Twelve §8 (source line 125) is the only place in the corpus that orders it. The index row R6-11-CHECK19_APPARATUS_SUBJECT's `notes` field attributes the order to Pack Fourteen §6, which contains only checks 27–29 and the Numbers rule; that is a mis-citation in the index, recorded here and in Appendix A as a mis-citation and nowhere repeated as fact.
- **Checks 43–49 (`--register`) exist in v4 with no rule in the index and no section in this guide.**
- **Checks 22–26 have names and severities but no thresholds in any pack.** The rule is folded as given; the thresholds are for whoever writes the checks into the script.

## Second check (2026-09-12, same day)

A second check after the nine corrections found seven residual points, all fixed in this text: (1) judgment call 13 said the only shared locus was §13 — check 19 is shared too (R6-11-CHECK19_APPARATUS_SUBJECT and R12-8-VERIFY_CHECKS_RETIRED), now stated; (2) §22 and §23 read "across the fight passages", a scope R13-9's verbatim attaches only to the causal-connective density — the two now carry the rule's own names, *HEMA density* and *Anatomical density*; (3) §24's gloss "the words that say why a thing worked, not only that it did" defined a term the rule does not define — struck, the section carries the rule's phrase *Causal-connective density in fight passages*; (4) §20 and §21's "do not reuse it" and the §22–26 preamble's "Run on any fight scene alongside `--scene`" were instructions no rule gives — struck; (5) §36's Script line claimed plural forms for all eight phrases — v4 carries plurals for four (*are assayed*, *are converted*, *are transferred*, *are affected by*), now said exactly; (6) §18's manual grep flags any line with one instance while the rule flags a sentence with two or more — the Script line now says to count per sentence; (7) the flagged-gap item above said the Pack Fourteen §6 mis-citation was "not repeated in this guide" while Appendix A records it too — reworded. The file was also found on disk in a state that had lost twelve of the first check's twenty corrections (Drive for Desktop re-created it from an earlier snapshot mid-edit); the corrections were replayed from the edit log and the result matched the corrected file byte for byte before this second check was applied.

---

# WOTR Manual Verification Guide

*Companion to `wotr_verify.sh`. Run the script; read this when a check fails or when adding new checks.*

*2026-09-12 edition. Checks 1–14 are the base guide's. Checks 15–42 arrive from Packs Four through Nineteen; two numbers (20, 21) are retired. The companion scripts are `wotr_verify.sh` v4 and, for checks 15–17, `wotr_beat_check.py`. See the changelog above for the audit trail.*

---

## 0. The Rule Underneath All the Checks

Stylometric research distinguishes machine prose from human prose on **variance**. Human writing shows dispersion. Machine writing is stable. Every check below is a specific instance of that principle. The correction is always deliberate unevenness.

---

## 1. Word Count

**Scene minimum: 2,500 words.** Non-scene prose (codex entries, letters, technique writeups) has no enforced minimum.

**Why it exists:** Scenes that run short are almost always missing their sensory opening, their interior beats, or their physical grounding. The minimum is a proxy for "did you actually build the scene."

---

## 2. Em Dashes

**Banned outright in WOTR prose.** No exceptions, no context where they're acceptable.

**Script:** `grep '—'`

---

## 3. Simile Density

**Target: 1 simile per ~500 words. Hard ceiling around 8 per scene.**

Simile markers: `the way`, `like [noun]`, `as if`, `as though`.

**What the check catches:**
- Raw count (is the scene drowning in similes)
- Competing pairs (two similes fighting for the same beat in close proximity)

**What the check does NOT catch (review manually):**
- Whether two similes within the same paragraph are serving different beats or stepping on each other. The script flags density; the judgment is yours.

**Distinction from metaphor:** Metaphor (X IS Y) is WOTR's native tongue and is used freely. Simile (X is LIKE Y) is rationed. Never cut metaphor to manage simile count. They are separate budgets.

---

## 4. Not-X-But-Y (All Forms)

**The single most important check in this document.** The antithesis construction ("it's not X, it's Y") is the most identifiable machine-prose fingerprint in circulation. It appears in roughly 6% of all chatbot messages. It also appears in eleven disguises, which is why a literal grep for "it wasn't just" catches almost nothing.

### The Eleven Forms

**4a. Explicit:** `not X but Y` / `not X, Y`
> "the tremor was not damage but adaptation"

**4b. Two-sentence:** `Not X. Y.`
> "Not a judgment. An observation."
> "Not in the way tall women are described. Tall in the way pillars are tall."

**4c. Negation-correction across sentences:** `[Subject] did not [verb]. [Subject] [different verb].`
> "The array did not radiate from a direction. It filled the room."
> "Maret was not a forge-tender. Maret was the array-wright."

**Note:** 4c produces many false positives. "He did not raise his voice" followed by "He had learned..." is normal prose. The pattern to catch is when the second sentence *corrects* the negation — when the two sentences together perform the rhetorical move of denying one thing to assert another.

**4d. Nothing/everything:** `nothing to do with X and everything to do with Y`

**4e. Formal variants:** `not merely`, `not only`, `not so much X as Y`, `less X than Y`

**4f. Double/triple negation:** `not X and not Y and not Z`
> "not wind and not radiation and not any force"

**4g. "Rather than" as antithesis:** `X rather than Y`
> When "rather than" is doing the work of "not X but Y." Two or more per scene is a pattern.

**4h. Countdown negation (covered separately in Check 8):**
> "X has no shape. Y has no shape either. Just Z."

**4i. Disguised across clauses:** The negation and correction split across a comma or semicolon rather than a period.
> "a pump that was losing did not announce itself, it simply became gradually less true"

**4j. Implicit via structure:** Two consecutive sentences where the first describes what something ISN'T and the second describes what it IS, even without the word "not."
> "The sound had not changed. The cruelest thing about the situation."

**4k. "Which is to say" / "which meant"** chains that correct an earlier negation.

### Script Coverage

The script catches 4a, 4b, 4d, 4e, 4f explicitly. It flags 4c and 4f as warnings for manual review. **4g through 4k require manual reading.** The script is a net, not a guarantee.

### The Fix

Rewrite the sentence to state what the thing IS, directly, without first saying what it ISN'T. If you find yourself writing "not X," ask: can I just write Y?

---

## 5. Banned Constructions

`"it wasn't just"` / `"it isn't just"` / `"it's not just"` and all tense variants. These are the literal string that kicked off the whole checklist. The antithesis move at its most naked.

---

## 6. Signposting

`"Now that"` / `"As mentioned"` / `"As we know"` / `"It's worth noting"` / `"It bears mentioning"`

Phrases that narrate the structure of the prose rather than the content. They tell the reader what the text is about to do instead of doing it.

---

## 7. Hypophora

Asking a question in order to answer it. The check flags all questions in prose; the manual review is whether the prose immediately answers its own question. Questions in dialogue are fine. Questions in narration that go unanswered (dramatic questions) are fine. Questions followed by their own answer in the next sentence are the tell.

---

## 8. Countdown Negation

The antithesis construction disguised across short sentences so the hinge is invisible in any one of them:

> *Ruin has no shape. The thing behind it has no shape either. No target. No classification. Just weight.*

That is "not X, not Y, just Z" wearing four sentences. Catch it by looking for consecutive negations resolving into "Just" or "Only."

---

## 9. Distinctive Word Repetition

**New check. Added after "arithmetic" appeared 3 times and "particular" appeared 5 times in a single scene without being caught.**

The script counts every word longer than 6 characters that appears 4 or more times, then cross-references against a known tic-word list:

`particular`, `arithmetic`, `specific`, `precisely`, `genuinely`, `honestly`, `actually`, `certainly`, `absolutely`, `essentially`, `fundamental`, `significant`, `remarkable`, `incredible`, `literally`, `basically`, `obviously`, `naturally`, `important`, `beautiful`, `different`, `carefully`, `currently`, `extremely`, `perfectly`, `suddenly`, `entirely`, `generally`, `ultimately`, `straightforward`

**Setting nouns** (gallery, chamber, ladderway) and **character names** are expected repeats and are excluded. The tic-word list catches the adjectives and adverbs that machine prose leans on without noticing.

**The fix:** Find the repeated word. Ask whether every instance earns its place or whether the word has become a reflex. Replace with a concrete alternative or restructure the sentence to not need it.

---

## 10. NPC Italic Thoughts

**One private italic thought per named NPC per scene.** The POV character's interiority is primarily carried by Free Indirect Discourse (narration in their voice); italic thoughts are Level 5 (closest psychic distance) and are used sparingly for the POV character. Every non-POV named NPC gets exactly one, grounded in their actual character.

The script counts italic thought lines and flags for manual verification. It cannot determine which NPC each thought belongs to — that requires reading.

---

## 11. Scene Ending

**End on physical action, never a question.** The last substantive line of the scene must be a character doing something with their body — walking, lifting, closing a hand, setting down an object. A question, a philosophical statement, or a narrative summary as the final beat is a structural failure.

---

## 12. Paragraph Length Variance

**Measured by Coefficient of Variation (CV = standard deviation / mean × 100).**

- CV ≥ 50%: Good variance
- CV 30–50%: Moderate (consider more variation)
- CV < 30%: Uniform — a tell

Human prose has irregular paragraph lengths. A one-line paragraph is allowed. A 200-word paragraph is allowed. The failure is when every paragraph is 60–80 words.

---

## 13. Sentence Length Variance

**Same CV metric applied to sentence length.**

- CV ≥ 80%: Good
- CV 50–80%: Moderate
- CV < 50%: Uniform — the strongest structural tell available

Hard sentence-length variation is the single most effective correction in the entire checklist: fragments at impact beats, long clauses at reads and aftermath.

**Hard ceilings on payoff sentences and paragraph shape.** The CV above measures the scene as a whole. Pack Four adds four hard measures beneath it, two taken at the payoff sentence, one across the scene, one at the paragraph close; they are ceilings and a floor, not targets: *(R4-14-HARD_CEILINGS)*

| Metric | Ceiling |
|---|---|
| Words in the payoff sentence | **10** |
| Subordinate clauses in the payoff sentence | **0** |
| Sentences under 8 words, share of scene | **18% floor** |
| Paragraphs closing on three consecutive sentences over 18 words | **0** |

A scene can post a good CV and still fail every row: variance across the document says nothing about whether the payoff sentence is short and unsubordinated, whether enough of the scene's sentences run under 8 words, or how its paragraphs close.

**Script:** not measured by `wotr_verify.sh` v4, whose check 13 stops at the CV. The nearest scripted ground is `wotr_beat_check.py` check 16 (Descent, R4-ADD-CHECK16; see §15–17), by its published description: it fails a short-sentence share under 10% and warns under 18%, where this table states 18% as a floor, and it reports every paragraph closing long-long-long; it does not measure the payoff sentence's word count or its subordinate clauses, so rows 1 and 2 are manual. That script is not in the bundle, so this line describes Pack Four's account of it, not its behaviour observed.

**Conjunction audit.** Count coordinators per sentence: *and, as, while, which, because.* Two or more inside a sentence carrying a beat is a fail. Outside a beat it is style and left alone. *(R4-14-CONJUNCTION_AUDIT)*

The fix is the count: at most one coordinator in the sentence that carries the beat. The sentences around it are not on this budget.

**Script:** not in `wotr_verify.sh` v4, and check 16's published description does not count coordinators either. Manual: find the beat, count the coordinators in the sentence that delivers it.

---

## 14. "Rather Than"

Tracked separately because it is the most-overlooked form of the antithesis pattern. One instance per scene is acceptable. Two or more is a pattern. Three is a tic.

---

## 15–17. Gloss Watch, Descent, Reification (`wotr_beat_check.py`)

Checks 15, 16 and 17 exist and are mandatory, but they live in the second script, `wotr_beat_check.py`, which Pack Four's Addendum ships beside `wotr_verify.sh`: **15, Gloss watch** (enforces Amendment Thirteen), **16, Descent** (enforces Amendment Fourteen, the ceilings at §13 above), **17, Reification** (enforces Amendment Fifteen). Their rules amend that script, not this guide, so they are not described here; the index rows are R4-ADD-CHECK15, R4-ADD-CHECK16 and R4-ADD-CHECK17. Both scripts run on every draft (see Running the Script). *(Cross-reference only; changelog, judgment call 1.)*

---

## 18. The Ladder

**Flag any sentence containing two or more instances of `was [a-z]+ and the [a-z]+ was`. Also flag the variants using `is`, `became`, and `meant`.** *(R6-11-CHECK18_LADDER)*

The pattern is a chain: each clause's predicate becomes the next clause's subject. One instance in a sentence is not flagged; two or more in the same sentence is the flag.

**The fix:** break the chain so no sentence carries two instances.

**Script (v4):** not implemented. Pack Six says the check was appended to `wotr_verify.sh` beside checks 15 through 17; the v4 file carries no check 18. Until it does, grep by hand: `grep -nP 'was [a-z]+ and the [a-z]+ was'`, then again with `is`, `became` and `meant` in place of `was` — and count per sentence, since the grep prints any line with one instance and the rule flags only a sentence with two or more.

---

## 19. Apparatus Subject

**Flag any sentence where a named faculty is the grammatical subject of a perception verb.** High false-positive rate by design; review by reading. *(R6-11-CHECK19_APPARATUS_SUBJECT)*

The check flags grammar, not meaning: a named faculty as the subject of a perception verb is the pattern, whatever the sentence goes on to say. Every flag is read. The rule gives no remedy beyond the reading.

> **Rewrite ordered, not yet written.** Pack Twelve §8 directs that this check be "rewritten off §4" (Pack Twelve §4, the four explaining voices). No pack supplies the rewritten wording, so Pack Six's text above stands until one does. *(R12-8-VERIFY_CHECKS_RETIRED)*

**Script (v4):** not implemented as check 19, although the v4 header lists 19 among the checks cleared by reading. The nearest thing in v4 is check 43 (under `--register`), which prints a manual warn to confirm no more than two explaining voices per engagement (POV read / knowledgeable second / opponent / document). That is the script's own gesture at Pack Twelve §4, not the rewritten check 19.

---

## 20. The Mechanism Gloss — RETIRED

**Retired by Pack Twelve: "Checks 20 and 21 retired."** *(R12-8-VERIFY_CHECKS_RETIRED)* Pack Seven's check 20 is `status: superseded` in the index (R7-6-CHECK20) and its text is not carried here. The number is kept so this guide's numbering and the script's stay aligned.

**Script (v4):** no check 20 block. The v4 header comment still names 20 among the false-positive-by-design checks; that line is stale.

---

## 21. Metaphysical Units — RETIRED

**Retired by Pack Twelve: "Checks 20 and 21 retired."** *(R12-8-VERIFY_CHECKS_RETIRED)* Pack Seven's check 21 is `status: superseded` in the index (R7-6-CHECK21) and its text is not carried here. The number is kept.

**Script (v4):** no check 21 block.

---

## 22–26. The Combat Checks (`--combat`)

**Pack Thirteen adds a `--combat` flag and five checks. 22 and 23 warn; 24 to 26 fail.** *(R13-9-VERIFY_CHECKS_22_26)* What the five are measuring is the combat technical floor: the Combat Craft Guide (2026-09-12 edition, §6) says what every meaningful exchange owes the page, and these checks are the mechanical side of that floor. The rule names the checks and their severities and gives no thresholds; the thresholds are for whoever writes the checks into the script.

**Script (v4):** no numbered checks 22–26 exist. `--combat` is accepted, and its only effect is to enable check 45 under `--register` (or `--all`), which counts three things in the body and fails below 3 / 3 / 1: anatomy terms (rib, femoral, carotid, sternum, scapula, clavicle, nerve, tendon, artery, pleural, diaphragm, olecranon, patella, hip, shin), measure and technique terms (measure, guard, bind, half-sword, pommel, thrust, parry, void, tempo, plant foot, underhook, clinch, check), and the POV's own body (*his own* / *her own* followed by arm, shoulder, ribs, hip, knee, lungs, breath, hands, neck, back). That is a fail where 22 and 23 are ordered to warn, and it covers nothing of 24 to 26. Until the five are scripted, they are run by reading.

## 22. HEMA Density

**Warn.** HEMA density. *(R13-9-VERIFY_CHECKS_22_26)* The vocabulary itself is the Combat Craft Guide's §3; v4's check 45 term list above is the nearest count the script currently makes.

## 23. Anatomical Density

**Warn.** Anatomical density. *(R13-9-VERIFY_CHECKS_22_26)* The vocabulary is the Combat Craft Guide's §3.6; v4's check 45 anatomy list above is the nearest count the script currently makes.

## 24. Causal-Connective Density in Fight Passages

**Fail.** Causal-connective density in fight passages. *(R13-9-VERIFY_CHECKS_22_26)* Not in v4.

## 25. A Stated Fault per Named Technique

**Fail.** Every named technique in the scene has its fault stated on the page; a named technique with no stated fault fails. *(R13-9-VERIFY_CHECKS_22_26)* What a fault is, the Combat Craft Guide §6 says, and it belongs to the technique performed, not to the opponent: "Every technique has a structural weakness, and the scene says what it is." Not in v4.

## 26. A Reserve Account per Working

**Fail.** Every working in the scene carries a reserve account; a working with no account fails. *(R13-9-VERIFY_CHECKS_22_26)* What the account holds is the Combat Craft Guide §6's business (its cost and Essence-account items), not this check's name. Not in v4.

---

## 27. Terminology Audit

**Every capitalised system term in the draft matched against `wotr_terms.txt`. Unknown terms listed. Near-misses (edit distance one or two from a canonical term) fail.** *(R14-6-CHECK27)*

Two outcomes: an unknown term is listed; a near-miss fails.

**The fix** for a near-miss: the canonical spelling.

**Script (v4):** not implemented. `wotr_terms.txt` is in v4's preflight manifest of mandatory sources and is not in the bundle. Manual until both exist.

---

## 28. Narration Leak

**Any Grade letter, Stage name, Band, eta, AU/s, EU figure, or Sub-Stat name outside quotation marks, italics, or a marked document block fails.** *(R14-6-CHECK28)*

The three containers are the whole rule: quotation marks, italics, a marked document block. The rule does not say what the quotation marks or the italics must be carrying; any of the listed vocabulary outside all three fails.

**The fix:** move it inside one of the three, or cut it.

**Script (v4):** not implemented as 28. Check 46 (under `--register`) is a cousin, not the check: it warns rather than fails, it fires only when a system quantity (Level, Stage, Grade, Band, Coherence, eta, η, Ardency, Dominion, Gnosis, Tempering, Vitality, Resilience, Harmonics) is followed by a digit within 24 characters, and it does not exempt the three containers. Manual until scripted.

---

## 29. The Loadout

**The author notes contain a Stat Ledger for every named practitioner (Pack Fourteen §7) or the run fails.** *(R14-6-CHECK29)*

**The fix:** write the ledger.

**Script (v4):** not implemented. Manual: count the named practitioners in the scene, count the ledgers in the notes, and the two numbers match or the run fails.

---

## 30. Conversion Density (`--convert`)

**A scene containing a working, an exchange, or an injury carries at least four terms from the WOTR technical lexicon and at least two correctly-used real scientific or anatomical terms, in the narration, outside italics.** *(R16-8-CHECK30)* False-positive by design; reviewed by reading.

**Script (v4):** with `--convert`, the body (everything above the first `## Notes`, `## Author` or `### Added by the gap-fill` heading) is taken, lines that are wholly italic are dropped, and two whole-word counts are made. System terms are counted against v4's own list (Wellspring, Essence, Aether, Aetheric, Crystal, Coherence, Dominion, Ardency, Gnosis, Tempering, Vitality, Resilience, Harmonics, Stage, Grade, Pressure, Hataraki, Attraction, Obsession, Oblation, Animatria, Shingan, Asami, Gisei, stratum, strata, Residue, Saturation, Density, Depth, Flux, Compression, Penetration, Cascade, Overchannel, Codex, glyph, Plane); real technical terms against a fixed list of physics, chemistry and anatomy words (latent, deposition, entropy, vasoconstriction, decoherence, femoral, pneumothorax, nucleation, recalescence and so on). Four and two passes. Below that: fewer than five working-references in the narration (working, technique, glyph, invok-, cast, rite, Wellspring, Essence, Aether, Domain, Crystal, Paru) → warn "No working performed — Pack 16 §7 exemption, conversion out of scope" (that citation is the script's; Pack Sixteen §7 does not amend this guide); two and one → warn "Thin conversion — read for flattening"; anything less → fail "Under-converted — register exported or flattened". The lists are the script's, not the rule's: a correctly used term the list doesn't know is invisible to the count, which is why the count is a floor to read against and not a verdict.

---

## 31. Export

**No mechanism term appears in the author-notes block that does not also appear in the prose body.** *(R16-8-CHECK31)*

A mechanism term that appears in the notes and nowhere in the body is the export the check is named for.

**The fix:** the term goes into the body, where the check will find it.

**Script (v4):** the notes block (from the first `## Notes`, `## Author` or `### Added by the gap-fill` heading down) is searched for a fixed list of mechanism terms (wellspring, essence, aether, crystal, coherence, dominion, ardency, gnosis, tempering, harmonics, hataraki, attraction, obsession, oblation, animatria, shingan, asami, gisei, decoherence, deposition, entropy, interference, cardinality, magnetite, reperfusion); each one found is then searched for in the body, case-insensitively, and any term present only in the notes fails with the list printed ("In notes but not in prose"). No notes block → warn and skip.

---

## 32. Coinage Retention

**Every distinctive term in the submitted rough appears in the output in one of the four routed forms, or is listed as dropped in the notes.** *(R16-8-CHECK32)* False-positive by design; reviewed by reading.

**Script (v4):** manual. The script does not have the rough and prints a warn: "Read the submitted rough. Every distinctive term routed (1-4) or listed as dropped."

---

## 33. Italic Quarantine

**Fewer than half of a scene's technical terms sit inside italic thought.** *(R16-8-CHECK33)*

A scene with half or more of its technical terms inside italic thought has quarantined them; that is the check's name.

**The fix:** move terms out of the italic thought until fewer than half sit there.

**Script (v4):** counts a fixed list of technical terms inside `*…*` spans of the body, and passes when that count is no more than half of the total (check 30's two narration counts plus the italic count). Edge: the rule says *fewer than half*; v4 passes at exactly half. Warns instead if no technical terms are found anywhere.

---

## 34. The Four Elements (`--entry`)

**Quantity, law, operation and chain all present in the Operation line. Any absence is a FAIL.** *(R17-8-CHECK34)* Manual. Runs on an entry (an ability or technique writeup), not on a scene.

**Script (v4):** with `--entry`, checks that lines labelled Operation, Manifestation, Cost, Limit and Counter each exist (bold label, or label followed by a period), passing or failing each, then prints a manual warn to confirm the Operation names the quantity, the law, the operation and the causal chain. The Manifestation label is the script's addition; the rule names only the Operation line and its four elements.

---

## 35. Derivation

**For each of Cost, Limit and Counter, name the sentence in the Operation it follows from. Anything that cannot be traced is decoration and is cut or re-derived.** *(R17-8-CHECK35)* Manual.

**Script (v4):** manual warn only: "For Cost, Limit and Counter: name the sentence in Operation each follows from. Untraceable = decoration."

---

## 36. The Assertion Sweep

**Flag every phrase that states an outcome in place of a process: *is assayed*, *is converted*, *is transferred*, *responds to*, *is affected by*, *is empowered by*, *resonates with*, *attunes to*. Each one is either replaced with the operation it is standing in for or deleted.** *(R17-8-CHECK36)*

**Script (v4):** a case-insensitive grep over the whole file for those phrases — with a plural form for four of them (*are assayed*, *are converted*, *are transferred*, *are affected by*) and none for the other four — plus two the rule does not list, *is imbued* and *channels the power*. Any hit fails and the first twelve lines are printed.

---

## 37. Controlled Vocabulary (`--codex`)

**Every Wellspring, Family, Physics Domain, Temperance stage, Archon, Titan, Glyph Class, alchemical Tier and alchemical Type named in the file is validated against the Lists sheet. Anything absent is a FAIL and must be either corrected or explicitly declared as a proposed new entry with the checked enumeration named.** *(R18-7-CHECK37)*

The Lists sheet is in The Master Codex (`The_Master_Codex.xlsx`). The fix is in the rule: correct the term, or declare it as proposed and name which enumeration you checked it against.

**Script (v4):** `--codex` hands the file to `codex_check.py` beside the script, and warns and skips checks 37–39 if that file is missing. `codex_check.py` strips the notes block, reads the Lists sheet's Wellspring, Family, PhysicsDomain, Archon and Titan columns (five of the rule's nine enumerations; Temperance stage, Glyph Class, alchemical Tier and alchemical Type are not yet checked), reports the valid terms the body uses, then hunts capitalised Latinate coinages by suffix (*-atio, -antia, -orath, -ivale, -thrae, -ilithe, -aeon*) minus a stoplist of ordinary English words, and fails on any not in those columns or the glyph index. A coinage that is not Latinate-shaped is invisible to it. **Note:** `codex_check.py`'s failing exit is counted into a variable the summary never reads, so a `--codex` failure prints above a summary that can still say CLEAN. Read the 37 and 38 lines themselves.

---

## 38. Glyph Validity

**Every bracketed glyph token in the file is validated against the Master Glyph Index. Unknown tokens FAIL.** *(R18-7-CHECK38)*

The Master Glyph Index is a sheet of The Master Codex. Unlike check 37, this rule supplies no declared-new-entry path: an unknown token fails, and the rule says nothing further.

**Script (v4):** `codex_check.py` collects every `[Xxxx]` token of one to four letters in the body and checks it against the first column of the Master Glyph Index sheet. No tokens → warn; unknown tokens → fail, listed; all known → pass with the count.

---

## 39. Precedent

**Manual. For any new working, name the Spell Index rows checked and state whether the working is new, a derivation of a named row, or a duplicate.** *(R18-7-CHECK39)*

The Spell Index is a sheet of The Master Codex. The rule does not say where the rows and the verdict are stated.

**Script (v4):** `codex_check.py` prints any Spell Index names it finds in the body as a starting point, then warns with the manual instruction: name the rows checked; new, derivation of a row, or duplicate.

---

## 40. Fidelity (`--dialogue`)

**Manual. Diff the output against the submitted rough. Every line of Isaac's dialogue appears verbatim except for the corrections permitted in Pack Nineteen §2. Any other change is a FAIL and is reverted.** *(R19-7-CHECK40)*

**Script (v4):** manual warn only; the script does not have the rough. "Diff output against the submitted rough. Isaac's lines verbatim except §2 corrections."

---

## 41. Prosody

**Automatic where possible. If the submitted rough contains stretched vowels, repeated punctuation or capitalised shouting and the output does not, FAIL.** *(R19-7-CHECK41)*

**Script (v4):** counts, in the output only, stretched vowels (a vowel three or more times in a row inside a word), shouted lines (four or more consecutive capitals inside a quoted string) and repeated marks (`!!`, `??`, `?!` and longer). Any present → pass "Prosody present in output"; none → warn "No prosody in output — confirm the rough contained none". The script cannot see the rough, so the rule's fail condition (present in the rough, absent from the output) is completed by the reader: on the warn, open the rough.

---

## 42. Composure

**Flags dialogue lines that are long, subordinate-heavy, or contain parallel constructions, and reports the spread of line lengths across the scene.** A file in which every speaker's lines cluster at one length is flagged for reading. *(R19-7-CHECK42)*

**Script (v4):** takes every quoted string of twelve or more characters as a dialogue line and reports the count, mean length in words, standard deviation, lines over 40 words, and parallel constructions (", and … , and", "neither … nor", "both … and … and"). Standard deviation under 6 words → fail "Dialogue lengths cluster — every speaker sounds the same"; long lines more than a quarter of all lines → warn "read for composure under duress"; otherwise pass. No dialogue → warn. Edge: the rule flags a clustered file for reading; v4 fails it outright.

---

## Running the Script

```bash
# Scene prose (enforces 2,500 word minimum)
bash wotr_verify.sh draft.md --scene

# Non-scene prose (codex, letter, technique writeup)
bash wotr_verify.sh draft.md
```

**Flags added since (v4).** Checks 22 onward are gated behind flags. Pass the ones the draft needs; the base run alone stops at check 14.

```bash
# Fight scene: checks 22–26 (Pack Thirteen)
bash wotr_verify.sh draft.md --scene --combat

# Conversion standard: checks 30–33 (Pack Sixteen)
bash wotr_verify.sh draft.md --scene --convert

# Ability or technique entry: checks 34–36 (Pack Seventeen)
bash wotr_verify.sh entry.md --entry

# Master Codex validation: checks 37–39 (Pack Eighteen); needs codex_check.py beside the script
bash wotr_verify.sh draft.md --codex

# Dialogue fidelity: checks 40–42 (Pack Nineteen)
bash wotr_verify.sh draft.md --dialogue

# Every flag at once. In v4 --all expands to --scene --combat --convert --codex --dialogue --register:
# it omits --entry (pass it by hand for an entry) and switches on --register, checks 43–49,
# which no rule in the index assigns to this guide.
bash wotr_verify.sh draft.md --all

# Source manifest and canon hierarchy, no file needed
bash wotr_verify.sh --preflight

# The second script: checks 15–17 (Pack Four)
python3 wotr_beat_check.py draft.md
```

**What v4 does before it checks.** The author-notes block (everything from the first `## Notes`, `## Author` or `### Added by the gap-fill` heading down) is stripped, and checks 1–14 run on the prose body only, because notes legitimately carry em dashes, similes and "rather than" that would fail as prose. The flagged checks re-read the full file, and only some of them split it again: 30–33 (`--convert`) and 43–49 (`--register`) split body from notes in the script, and 37–39 hand the file to `codex_check.py`, which strips the notes block itself; 34–36 (`--entry`) and 40–42 (`--dialogue`) run on the whole file, notes included, so an assertion phrase, a stretched vowel or a quoted line in the author notes counts for those six.

**Workflow:**
1. Write draft to file
2. Run the script
3. Fix all FAILs
4. Review all WARNs manually
5. Re-run until clean
6. Present to Isaac

**Both scripts run before presenting, failures are fixed, both re-run. No single-pass delivery.** *(R4-ADD-NO_SINGLE_PASS)* The workflow above is run for `wotr_verify.sh` and for `wotr_beat_check.py`, and a fix that clears one is re-checked against the other before anything is presented.

**The script is a floor, not a ceiling.** It catches the mechanical tells. It does not catch:
- Voice consistency (are characters unreplaceable)
- Psychic distance control (is the FID consistent)
- Value turn (did the scene turn something)
- Overcrowded beats (revelation + threat + philosophy stacked)
- Exposed subtext (a line followed by its own explanation)
- World detail entering through exposition rather than action

Those require reading. The script handles the checks a machine can do so the reading can focus on the checks only a reader can do.

Of the checks added since the base guide, 39 and 40 say *Manual* in the rule text; 32, 35 and 40 are manual in v4, which prints a warn for each and nothing more, and 34 is manual past its label count; 18, 19 and 22–29 are manual until v4 grows them (each section says which). A manual check is still a check: it runs by reading, in the same pass, and its result is reported with the rest.

---

## Adding New Checks

When a new tell is identified in a session, add it to both this document and the script. The "arithmetic" repetition check was added after a scene passed the script three times with the word appearing uncaught. The checklist is a living document. If a tell survives the script, the script is wrong, not the tell.

---

## APPENDIX A — FLAGGED GAPS CARRIED FORWARD

The base guide had no flagged-gaps page. These are the gaps this edition found between what the packs order and what the tools in the bundle do, carried forward rather than fixed here (the script is read-only for this pass; the guide describes it, it does not amend it):

- **`wotr_beat_check.py` and `wotr_terms.txt` are not in the session bundle.** Both are named as mandatory (R4-ADD-NO_SINGLE_PASS; R14-6-CHECK27 and v4's preflight manifest). Until they are restored, checks 15–17 and 27 are manual.
- **v4 does not implement checks 18, 19, 22–29 as numbered checks**, and its header comment still lists 19 and 20 among the false-positive-by-design checks though 20 is retired.
- **v4's `--codex` failures do not reach the summary line** (`FAILURES` is incremented; `FAIL` is what the summary reads). A `--codex` run can say CLEAN with a failure printed above it.
- **v4's `--all` omits `--entry`.** Checks 34–36 need the flag passed by hand.
- **Check 19's rewrite off Pack Twelve §4 is ordered and unwritten.** Pack Twelve §8 is the only pack that orders it; the index note attributing the order to Pack Fourteen §6 as well is wrong (see the changelog's flagged gaps).
- **Checks 43–49 (`--register`) exist in v4 with no rule in the index and no section here.**
- **Checks 22–26 have names and severities but no thresholds in any pack.**

*No proposed rules name this guide in the index as of 2026-09-12, so there is no Appendix B.*
