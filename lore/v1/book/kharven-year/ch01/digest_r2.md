# Digest r2

**Verdict: escalate** (fail 4, warn 8, dropped 0)

## 1. FAIL [continuity]

> A voice that had not once, in three days, risen above the level of the water coming off the roof.

**Problem:** Time-elapsed contradiction: the clerk of the Bench is introduced as having "arrived on the third day," and the chapter's own dateline is "Seven days after the signing" (confirmed again mid-scene: "He had asked for nothing in seven days"). Day 7 minus day 3 is four days, not three, so her own paragraph's "in three days" undercounts her stay by one day against the chapter's day-numbering (the same convention that puts Tabitha's arrival on "the sixth day").

**Fix:** Change "in three days" to "in four days" (or move her arrival to "the fourth day") so the elapsed count matches the chapter's day-numbering.

## 2. FAIL [POV and knowledge]

> Her left ear went back once and came forward. The tail did not move. She did not open the book.

**Problem:** Head-hop / knowledge leak: the narration reports a precise visual read of Yoko's ear and tail immediately after the draft itself states the POV's line of sight does not reach her.

**Fix:** Cut the ear/tail detail from this beat, or relocate it to a moment with an established line of sight (the scene's opening survey, or a stated glance/turn) — the same relocate-to-a-perceivable-channel fix the r1 round already applied to the Yoko-nose and Brida-gait head-hops.

## 3. FAIL [canon]

> and did not enter them, and the Bench asks that she enter them now.

**Problem:** The draft's only institution named "the Bench" is written as a treaty-witness registrar — it keeps "the Record of the signing" and can compel a signatory to "enter" her account of a political signing. The wiki's only Bench is the Bench of Attribution, whose charter is warrant/culpability for workings, formulas and strikings ("who did this, and by what warrant"), not treaty witness records.

**Fix:** None stated.

## 4. FAIL [beat and hooks — PC does what the beat says and nothing beyond it]

> Sodoku said nothing. It was his hall and the Bench had been refused in it, and he let it stand, and the water came down the walls.

**Problem:** The brief limits Sodoku's actions this chapter to exactly four items and states the writer originates no decision for him beyond those. Yoko's refusal of the Bench is the beat's event, not Sodoku's; the beat never gives him a fifth act of choosing whether to let it stand. Narrating his silence as a sovereign choice ('he let it stand') originates a decision for the PC that isn't one of the four licensed actions and isn't in the outline beat.

**Fix:** Cut the interpretive clause so the sentence reports only the fact (his silence, the refusal standing) without framing it as something he chose — e.g. end the sentence after 'refused in it' and let the water-down-the-walls beat carry the scene forward, or move the observation into Yoko's or the clerk's action rather than Sodoku's agency.

## 5. WARN [voice]

> "How's your stack?"

**Problem:** Sodoku Moto's archive fingerprint (13 lines, mean 45.6 words) is a long, uncontracted, non-asking voice. All six of his lines here are short (1 to 22 words, z between -1.1 and -2.1); two single-word lines ('Vaultmere.', 'Good,') are 'far outside this voice'; 'How's your stack?' is flagged as a question from a voice that almost never asks and a contraction from a voice that does not contract.

**Fix:** WARN, not FAIL: the greeting is the Kharven Standing Inventory's fixed wording (R6-9-RECURRENCE_RULE, notes_r2.md item 7) and the brief prescribes imperatives for Sodoku in this scene (R19-5-SORT_BY_SPEAKER_TEST). The archive's long mean comes from council speech; the short register is a deliberate choice here. Isaac to confirm the short register is acceptable for ch01, or lengthen one non-greeting line.

## 6. WARN [continuity]

> Mistress Mishiro wrote at this table on the night of the signing, after the seal, four lines, and did not enter them, and the Bench asks that she enter them now.

**Problem:** The clerk states precise circumstantial details of a private act — location ("at this table"), timing ("after the seal"), and exact length ("four lines") — of Yoko's writing in her own record, even though she "had arrived on the third day," days after the signing night. The draft frames that act as something Sodoku alone witnessed ("He had seen her write them. He had not seen them"), and never shows how the clerk, arriving later, came to know these specifics rather than just "an entry is missing."

**Fix:** Either add a line showing the clerk's source for the detail (testimony, the Record's witness log noting time/place), or soften her claim to what an official Record would actually show — that Mishiro's entry is outstanding — without the precise at-the-table/after-the-seal/four-lines specificity.

## 7. WARN [POV and knowledge]

> On the bench, Yoko's nose moved. Once, toward Lambert, and back.

**Problem:** Same channel doubt as the FAIL above: Yoko is behind Sodoku's left shoulder and no glance or turn is narrated at this moment, yet the draft gives a directional read of her nose.

**Fix:** If kept, ground it with a one-clause anchor (a half-turn, or 'in the edge of his eye') so the perception channel is stated rather than assumed.

## 8. WARN [POV and knowledge]

> Nobody in front of him looked past him at the bench.

**Problem:** A comprehensive negative claim about the simultaneous gaze of every person seated in front of Sodoku, asserted as settled fact rather than a perception in progress.

**Fix:** Narrow further to the one or two people whose faces he is actually shown reading in this beat, or reframe as his own inference from the room's stillness rather than a flat claim about others' attention.

## 9. WARN [POV and knowledge]

> Her ears were up. Her tail lay along the bench and did not move.

**Problem:** Part of the opening cast-introduction block: precise visual detail of Yoko, seated behind Sodoku's left shoulder, with no stated glance or turn establishing he is looking at her at this point (he has just been placed standing at the head of the table over his grain returns).

**Fix:** No action needed if the opening block is read as a pre-settling survey; if tightened, anchor it with an explicit look ('he had marked her on the way in') to match the rigor applied elsewhere in the draft.

## 10. WARN [rules]

> It was his hall and the Bench had been refused in it, and he let it stand, and the water came down the walls.

**Problem:** Possible break of R4-14-CLAUSE_CAP_AT_BEAT and R4-14-CONJUNCTION_AUDIT. This sentence sits at the H01 value-turn (the king lets the Bench's refusal of Yoko stand, per the brief's own gloss: '(Refused in one sentence; the Bench notes it; the king does not press.)'), one beat before the next turn ('"Make the copy," he said.'). It carries three coordinating 'and' clauses in one sentence, exceeding CLAUSE_CAP_AT_BEAT's cap of one subordinate-or-coordinate clause within the three sentences bracketing a value turn, and clearing CONJUNCTION_AUDIT's two-coordinator fail threshold for a beat-carrying sentence. The doubt, not certainty: the draft uses equally conjunction-heavy 'and'-chained sentences throughout as general connective/descriptive texture (e.g. the vellum paragraph, the death-house paragraph, Tabitha's coat description), which CONJUNCTION_AUDIT explicitly exempts as 'style... left alone' when a sentence is outside a beat — so whether this particular instance counts as beat-carrying rather than the piece's ordinary connective style is a judgment call for a human read, not a mechanical count.

**Fix:** If this is judged to be the beat, break it: 'It was his hall. The Bench had been refused in it. He let it stand.' and move 'the water came down the walls' to its own sentence or the next paragraph's atmosphere.

## 11. WARN [canon]

> where she had sat, or stood, or crouched, for nine years, whenever there had been a wall

**Problem:** Yoko Mishiro's only wiki card gives her current standing as settled and domestic elsewhere, not as a nine-year fixture of Sodoku's court. Unlike Sodoku's card, which the bible explicitly marks as superseded ("the card is from the exile years"), nothing in the bible or notes says the same of Yoko's card, so the tension between the two pictures of her is unattested/unreconciled rather than resolved.

**Fix:** None stated.

## 12. WARN [canon]

> Greymane stood through it, and that is his hip and his business

**Problem:** Brida attributes Bram Greymane's standing through the signing to his hip. The only wiki record of that fact (State of Play) gives him a different, unrelated physical detail and no stated cause for standing — the hip is an unattested addition.

**Fix:** None stated.
