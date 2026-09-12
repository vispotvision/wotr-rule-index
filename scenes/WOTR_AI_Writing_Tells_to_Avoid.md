# WOTR — AI Writing Tells to Avoid
*Second edition. Rebuilt on stylometric research rather than accumulated suspicion.*

---

## 0. Why the List Works

The first edition was a list of things that felt wrong. There is now actual research underneath it, and it explains the whole list with one finding.

Peer-reviewed stylometry (O'Sullivan, *Humanities & Social Sciences Communications*, 2025; Zhu & Lei, *Digital Scholarship in the Humanities*, 2025) finds machine-generated prose remains statistically identifiable, with classifiers exceeding eighty percent accuracy on passages as short as a hundred words. The distinguishing feature is not vocabulary. It is **variance**.

Human writing shows substantial dispersion and individual variation. Machine writing is comparatively stable — evenly weighted sentences, uniform paragraph blocks, smoothed emotional register, frictionless transitions. **Uniformity is the fingerprint.**

Two consequences for how this guide is used:

1. **Sentence structure is a more reliable tell than any word list.** Vocabulary tells drift and die. Structural tells persist. Weight the checks accordingly.
2. **The correction is deliberate unevenness.** Not the absence of tics but the presence of variance, applied on purpose.

---

## 1. Sentence-Level Tics

**The antithesis construction. Banned outright.**

"It isn't just X, it's Y." "Not merely X but Y." "This is less X than Y."

This is the single most identifiable machine construction in circulation. A *Washington Post* analysis of 328,744 chatbot messages found variations of "not just X, but Y" in roughly six percent of all messages — an extraordinary share for one rhetorical move. It has also been tracked climbing in corporate filings, from 49 instances in 2023 to 208 in 2025. When a construction is that concentrated, using it once is a signature.

**Countdown negation.** The same move disguised across short sentences so the hinge is not visible in any one of them:

> *Ruin has no shape. The thing behind it has no shape either. No target. No classification. Just weight.*

That is "not X, not Y, just Z" wearing four sentences. It reads as atmospheric and is the tell in its most-evolved form. Catch it by looking for consecutive negations resolving into a "just."

**Manufactured fragment emphasis.** "Not slowly." "Never again." "And it held." A fragment deployed to manufacture weight the preceding sentence did not earn.

**Hypophora.** Asking a question in order to answer it.

**Em dashes.** Banned in WOTR prose regardless of provenance.

---

## 2. Rhythm and Structure

The highest-value section, per the research.

- **Uniform sentence length.** Measurable and damning. Vary hard: fragments at impact, long clauses at reads and aftermath.
- **Uniform paragraph blocks.** If every paragraph is four to six lines, the page has a machine's shape. Break deliberately. A one-line paragraph is allowed to exist.
- **Repeated sentence architecture across paragraphs.** Subject-verb-object, subject-verb-object, subject-verb-object.
- **Excessive tricolon.** Three-item lists as a default rhythm rather than a chosen one.
- **Anaphora abuse.** Repeated openings deployed for cadence.
- **Frictionless transitions.** Every paragraph flowing smoothly into the next. Real prose lurches sometimes.
- **The tidy summary close.** "Ultimately," "In the end," a closing sentence that restates and resolves. WOTR scenes end on physical action.

---

## 3. Word Choice

Lower-value than structure, and the specific words drift, so treat this as indicative rather than definitive.

- **Vague abstraction and nominalization.** Framework, dynamic, ecosystem, landscape, tapestry. Concrete noun or nothing.
- **Overused verbs.** Navigate, leverage, unlock, delve, weave, underscore.
- **Hedging.** "Something like," "a kind of," "almost as if" stacked where a direct assertion belongs.
- **Elevated-word stacking.** More than one advanced word per paragraph reads as a thesaurus pass. The Elevated Vocabulary standard is one per paragraph, maximum, and it is a hard ceiling.
- **Dead metaphors and magic adverbs.**

---

## 4. Tone-Level Tics

Fiction-specific, and the ones that survive a mechanical check.

- **Emotional over-signposting.** Naming the feeling the scene already delivered. If the reader watched the hands shake, do not say he was afraid.
- **Exposed subtext.** A line followed by a sentence explaining its implication. Delete the explanation, never the line.
- **Characters narrating their own meaning.** People do not annotate themselves.
- **Smoothed emotional register.** Uniform sentiment with no abrupt modulation. Real distress is uneven, lurches, and does not resolve on schedule.
- **Overcrowded beats.** Revelation plus threat plus philosophy in one exchange. Cut two.
- **Cliché metaphor clusters.** Multiple stacked figures in a row, each individually acceptable.
- **World detail entering through explanation** rather than action or observation.
- **The generic profundity pivot.** A concrete scene turning, in its last line, into a universal statement about the human condition.

---

## 5. What This Guide Does Not Ban

Worth stating, because over-correction produces its own flatness.

- **Metaphor.** WOTR's native tongue, including the full Hermetic correspondence register. Metaphor asserts identity and is used freely.
- **Simile.** Rationed, not banned. Cut only when two compete for the same beat. Never cut metaphor to manage simile count.
- **Telling.** Narrative summary is correct for transitions, elapsed time, and connective tissue. See the Scene Writing Process Guide.
- **Long sentences.** The problem is uniformity, not length.
- **Formality.** A codex document should sound like a codex document.

---

## 6. Pre-Output Scan

Mechanical, via bash, never by eye.

1. grep the antithesis construction and every variant
2. scan for countdown negation — consecutive negations resolving into "just"
3. grep for em dashes
4. grep for signposting
5. **sentence-length variance** — compute it, do not estimate it
6. **paragraph-length variance** — same
7. grep simile markers, checking for competing pairs
8. confirm one interior beat per named NPC
9. confirm the scene ends on physical action
10. read the final line and ask whether it pivoted to profundity

Items 5 and 6 are new and, per the research, they are the two that matter most.

---

## 7. The Underlying Rule

Everything above reduces to one instruction: **variance is voice.**

Machine prose is stable, balanced, smooth, and even. Human prose is uneven, lurches, over-commits in one place and under-commits in another, and carries the individual dispersion that stylometry measures and cannot fake. The corrections in this guide are not about avoiding forbidden words. They are about restoring unevenness on purpose.

Write the sentence that is the wrong length for the paragraph it is in, when that is the sentence the moment wants.
