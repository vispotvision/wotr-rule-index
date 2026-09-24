# Audit after chapter 5: night-watch-zombification

Audited 2026-09-24. This replaces the earlier audit written at 05:06, before chapter 4 was drafted and before chapters 1, 2, 4 and 5 were carried into memory.

I read `outline.json` (80 rows), `bible.md` (Proposed Fronts, cast, flags) and the whole of `state.json`: 5 summaries, 159 facts and 32 hooks. To check the quotes, I also read the chapter `final.md` and `GATE.md` files. I edited nothing except this file, and called no tool that writes.

**About the 28–52 band.** No chapter from 28 to 52 exists yet. I read facts #28–52 of `state.json` most closely instead: they cover the end of ch1 and the start of ch3. Any contradiction that will land inside the ch28–52 band is marked ⇢.

## 0. State of the book

| ch | title | POV | final | proposed Front ticked | gate |
|---|---|---|---|---|---|
| 1 | The Docket Head | Wystan | r0 | the-night-register-file s1, push 1/5 | undecided |
| 2 | Twenty-Two Drops | Vesk | **r0** (r1 exists, not accepted) | project-zombification s1, push 1/3 | undecided ("revise") |
| 3 | The Morning Check | Wystan | r0 | the-night-register-file s1, push 2/5 | undecided |
| 4 | A Number in the Room | Deming | r1 | the-swale-wastage s1, push 1/3 | undecided |
| 5 | Who Set the Marker | Wystan | r0 | the-night-register-file s1, push 3/5 | undecided |

- `ch02/final.md` is byte-identical to `draft_r0.md`. Three things in it matter below:
  - It keeps the FAIL ("in twelve days" against "Eleven days").
  - It keeps the "Wardens of Duty" line.
  - It has no "separately" line. That line exists only in r1.
- Everything in memory comes from an unattended run. No gate has been decided.
- `GATES.md` still reads "Chapters 0/80 written", which is stale.

## 1. Hooks

### Overdue (due_ch passed, not paid): CRITICAL
**None.** The earliest due dates are H08 (ch6), H01 (ch7) and H21 (ch10).

### Due within five chapters
- **H08-concealed-contraction, due ch6.** Status is still "planted", and the hook's own text quotes a line that is not in the canonical text: Malphas "will discuss with her separately". See C3.
- **H01-far-side-of-the-marker, due ch7.** Advanced in ch5. The ch7 outline's placement of the lick contradicts ch5. See C4 and C5.
- **H21-the-ninth-hind, due ch10.** The day count is soft. See C9.

### Dormant (no event in more than 3 chapters): WARN
- **H02-quarter-inch-sealed and H03-chapter-wax.** Last event ch1. Both pay at the ch58 hearing, so the dormancy is by design, but a callback before Movement II would be good.
- **H05-night-register-a-person and H06-edge-held-cup.** Last recorded event ch1. **The text touched both in ch5, and state.json missed the events:**
  - H05: "Clerk said you were a person."
  - H06: "He took it by the edge of the crust, two fingers and a thumb", and the lapse, "He had not held it by the edge."
  - Also missed: H14 in ch5 ("Wystan took the brass out of his waistcoat and showed it on his palm").
- **Trips next chapter unless touched:** H07, H09, H10, H11 and H21, all last touched in ch2.

### Open hooks: WARN
- **23 open** (planted or advanced, none paid): H01–H19, H21, H23, H24 and H32. That is over 12.
- A further 9 are planned but not yet planted: H20, H22 and H25–H31.
- Nothing has been paid in five chapters. The first pays are ch6 (H08), ch7 (H01) and ch10 (H21).

## 2. Cast

- **POV cast with no fact for more than 5 chapters (WARN): none.**
  - Last fact for each: Wystan ch5, Qiu Yinzhi ch5, Nol Tally ch5, Xu Deming ch4, Vesk, Nuvalik and Ilmar Foss ch2.
  - Osric Salter does not come on the page until ch73.
  - Watch: Deming trips at ch10 unless ch10, where he is in the cast, gives him a fact.
- **Death fact followed by the subject acting (CRITICAL): none.** No death facts exist, and Keld is alive ("Keld was alive.", ch3).
- **Subject names are not normalised (WARN).** state.json uses "Wystan", "Deming", "Tally", "Yinzhi" and "Brack" beside "Qiu Yinzhi", "Edwyn Brack" and "Elspeth Lyle". The outline uses "Wystan Ashmore", "Xu Deming" and "Nol Tally". A lookup by the outline name finds no facts for Deming or Tally. Future facts should use the outline's full names.

## 3. Sag

**None.** Every chapter ticks a proposed Front and advances at least one hook:

| ch | Front push | hooks advanced |
|---|---|---|
| 1 | the-night-register-file | plants 8 |
| 2 | project-zombification | plants 6 |
| 3 | the-night-register-file | H23, H24 |
| 4 | the-swale-wastage s1 | plants 4 |
| 5 | the-night-register-file | H01, H04, H23 |

## 4. Continuity

### Identity: Wystan learns Malphas, or Malphas learns Wystan (CRITICAL if found)
**No such line.** I searched all five finals for names from the other side: Wystan-side names in ch2 and ch4, and cell-side names in ch1, ch3 and ch5. There are two hits, and both are allowed:
- ch2, Malphas: "The one their Wardens of Duty are issued." This names a rank, not a person. r1 removed it, but r0 is the canonical text.
- ch1, Wystan: "the formulator". This is his sanctioned term for the unknown hand.

There are three near misses that the next chapters could turn into a CRITICAL:
- **ch5.** "Ashmore. I keep it." Tally now holds the name, and Tally stands one step from the Ferriby round, which leads to Josse, then the carter, then Foss (ch8).
- **ch2, Foss.** Every copy of the field manual "has a number cut into the board and the number is against a name in an issue book", and "Somebody's copy is under a floor with a dead man over it".
- **ch3, Keld.** "Keld's Division coat hangs on a peg in his room with his silver token still in it", and "Nobody had ever come to take it back." Keld's manual may still be out. If a Keld copy reached Foss in ch6, Malphas would hold a name one step from Wystan.

### Contradictions

**C1: CRITICAL ⇢ ch44 (H13; the bible's "What Wystan believes" 1).** Does Wystan know that residue runs to him?
- ch3, the declared misreading: "it came down on everybody in the room alike; Lyle had simply never sat a night on the Register, and had nothing on her hands to feel it with."
- ch5: "In a shut room the free residue ran its gradient down to the emptiest thing present, which was always him".

Ch5 states the corrected physics as something he already knows. H13 ("paid when he learns he is the sink") and ch44 both assume he does not.

**C2: CRITICAL ⇢ ch6 (H20).** When can the field manual be had?
- ch2, Foss: "It will be a season." Malphas: "A season is acceptable."
- ch5: "The whole of the chapter's bench had read the field manual, looking for the part about themselves."
- Outline ch6, Day 5 (four days after ch2): "Foss reads the Division field manual aloud, the unsigned paragraph".

**C3: CRITICAL ⇢ ch6 (H08).** Who knew about the contraction?
- ch2 (canon, r0), Vesk: "The Lord said contraction. Twice, he said." Nuvalik: "Everything the fourth hind gave me is written down."
- H08's text says Malphas "will discuss with her separately". That line is in ch2 r1 only.
- Outline ch6: "Nuvalik says she hid the twitch in the fourth hind's shoulder".

Malphas already knows about the contraction. What Nuvalik concealed can only be the record in the book.

**C4: CRITICAL ⇢ ch7 (H01).** Where the round goes, and where the walker stopped.
- ch5: the stopping place "lay just inside the birch on the east side, on the estate's round". The walker "stopped short of the stone. Well short." "None went on past the place where they stopped, or followed the round where it bent west along the bound."
- ch5: the last hind lies 22 paces from the stone. Wystan stood beside her for eight divisions. The day book reads "Nothing set out, per Tally."
- H01 text: "Paid when the lick-keeper's round is found to end at the marker". Outline ch7: "the last twenty-two paces short of the marker".

**C5: CRITICAL ⇢ ch7.** How recently the carrier walked.
- ch5: "The newest were weeks old." At least some passes "broke ground the dead had already shed on".
- Outline ch7 (Day 7): Josse, who "says the estate steward paid for the new tonic blocks", is actively working the round. Ch8 moves the licks only after that.

**C6: CRITICAL ⇢ ch9.** The outline carries the cell's count into Wystan's head.
- ch1: "Eleven hinds and a stag". ch3: Lyle says it back, and the clerk writes it down.
- ch2: "nine carcasses signed by nobody", which is the rail at Greyshaft Nine.
- Outline ch9: "the price of third-dilution Verdantia against nine hinds and a stag". The bible's flags say "Wystan's ch9 arithmetic uses Tally's count."

**C7: CRITICAL ⇢ ch12.** The outline repeats what ch3 already did.
- ch3: "*The Register may keep this curiosity open until the quarterly inspection of the gauge-housing, and not a day longer. E. Lyle, Prime Warden.*" The position ("a dose goes where it is put") was copied into her minute under her silver seal, and Wystan initialled it.
- Outline ch12: "Lyle gives Wystan until the quarterly inspection to produce a purse, and enters the edges memorandum as the Register's position."

**C8: WARN.** The stables and the medical house.
- ch3: "The medical house stood two streets over, behind the Division's stables".
- ch5: "The Division's stables stood behind the medical house".

**C9: WARN ⇢ ch10 (H21).** The ninth hind's day count.
- ch2 (r0) contradicts itself: "in twelve days Vesk had watched" against "Eleven days he had watched for it. The twelfth had started at the second division".
- The hind has "Eleven days of the ferment" on Day 1. Outline ch10 has her "dead twenty-three days" on Day 12.
- The count works only if Day 1 is her twelfth day. Ch10 should not print a number that fights ch2.

**C10: WARN ⇢ ch22 (H16).** The thirty-first day.
- ch4 (Day 2): "put his finger on today and counted forward, a square to a day … *Thirty-one.*" That lands on Day 32 or 33.
- Outline ch22 is dated "Day 31".

**C11: WARN ⇢ ch47–48 (inside the band; H17).** Eleven weeks.
- ch4: "Eleven weeks from the day the factor took the page away." That was Day 2, so Day 79.
- Outline ch47 and ch48 are dated Day 77, "Eleven weeks to the day". ch4's "near enough that the roads made the difference" gives some slack, but "to the day" does not.

**C12: WARN.** Greyshaft Nine's history, inside ch2.
- "the seal broken on a quarterly inspection that had stopped coming nine years ago"
- "The main under Greyshaft Nine had been capped four years"

Together these leave the main live and uninspected for five years.

**C13: WARN ⇢ ch65.** A disciplinary observation already exists.
- ch3: the tremor was entered "as a disciplinary observation".
- Outline ch65: "Lyle enters a disciplinary observation: a Master concealing his Stage". Ch65's has to be a second, separate entry.

**C14: NOTE.** The carcass counts, a flag the bible records and leaves unresolved.
- Ferriby: eleven hinds and a stag (ch1), still lying in the cut on Day 5 (ch5: "A hind, lying toward the stone").
- The rail: nine (ch2).
- No chapter may say the rail's nine came from Ferriby.

**C15: NOTE ⇢ ch37 (inside the band).** Tally's lie.
- The motive for "Nothing set out on my line, nor near it" is originated in `ch05/final_notes.md` only: he helps himself to what the estate sets out. The page does not state it.
- In ch5, the food in his pack is "a dark hand-ground loaf" and "a heel of hard cheese".
- Ch37's lick salt in his pack has to be reached from that page, not asserted as already shown.

**C16: NOTE.** Units. The outline says "eight hours" and the ch5 text says "Eight divisions" (twelfth to sixth). Ch2 has "since the eleventh hour". Use divisions only.

**C17: NOTE (checked, consistent).** The facts in the #28–52 seam agree:
- ch1: "laid his brass on the lid". ch3: "His brass was lying on a tin lid on Cutler Row, where he had left it at the sixth division".
- ch1: "a scullery on Cutler Row". ch3: "the Arbitration Division's northern office on Cutler Row". These are one house (ch1: the day desk is "up the four steps").

## 5. Front status (proposed, bible)

| Front | segment | pushes done | next |
|---|---|---|---|
| the-night-register-file | 1 Exhibit one | ch1, 3, 5 (3/5) | ch7, ch12 (fills) |
| project-zombification | 1 The dose walks | ch2 (1/3) | ch6, ch10 (fills) |
| the-swale-wastage | 1 Diversion | ch4 (1/3) | ch9, ch11 (fills) |
| the-quiet-districts | 1 Enforcement asks | 0 | ch26 |

Every `front_id` is still null. Nothing has been written to `table/fronts.yaml`.

## Carry-forward

1. Ch6 (H08): canon is ch2 r0, where Malphas never says "separately" and Vesk already heard "The Lord said contraction. Twice, he said." So write Nuvalik's concealment as kept out of the book, not from Malphas, and open on her "Everything the fourth hind gave me is written down."
2. Ch6 (H20): Foss said on Day 1 "It will be a season" and Malphas accepted it. If he reads the manual on Day 5, show on the page how a copy came early (ch5: "The whole of the chapter's bench had read the field manual"), and have Foss remark that the season came short.
3. Ch6–8 (identity): the manual copy Foss reads carries no issue name or number that leads to Wystan, Keld or Cutler Row. In ch7, Wystan gives Josse only the brass and "the Register", never "Ashmore". The carter chain and Foss carry only "a man from the Register", and Tally never passes on the name.
4. Ch7 (H01): put the last lick at the walker's stopping place, just inside the birch on the east side of the estate's round, "well short" of the stone and out of sight of the cut. It is not 22 paces short, where the last hind lies and Wystan stood eight divisions. Pay H01 as the lick circuit turning home there, since the estate's round goes on west along the bound.
5. Ch7: Called Late put the newest passes "weeks old" on Day 5, some of them after the dead were down. Josse has not been to the Ferriby end since. Any "new tonic block" Wystan takes was set weeks back, and Josse's minute shows it being set then.
6. Ch9: Wystan prices the dose against eleven hinds and a stag (ch1 and ch3), never the outline's "nine hinds and a stag". Nine is the cell's rail count, and he cannot know it.
7. Ch12: Lyle's term (until the quarterly inspection) and the Register's position have been in her minute, under her silver, since ch3. Write ch12's ruling as an addition to that minute (produce a purse by the inspection), not as a first entry.
8. Ch6 onward: Wystan already knows that shut-room residue runs "always" to him (ch5). Never restate ch3's "came down on everybody in the room alike". Keep his wrong belief (ch25–44) as the dead being *sent* to him, and have ch44 pay only that nobody sent them.
