# Audit after chapter 10: night-watch-zombification

Audited 2026-09-24, after chapter 10 went into memory. I read `outline.json` (80 rows), `bible.md` (Isaac's rule, Cast, Proposed Fronts, What Wystan believes, Flags) and the whole of `state.json`: 10 summaries, 305 facts and 32 hooks. I also read `AUDIT_ch05.md` so its open items could be closed or carried. To check the quotes, I read the chapter `final.md` and `GATE.md` files, and `ch10/draft_r3.md`. I edited nothing except this file, and I called no tool that writes.

**About the 28–52 band.** No chapter from 28 to 52 has been written yet. As in the ch5 audit, I read facts #28–52 of `state.json` closest (the end of ch1 and the start of ch3), and then checked the outline rows for ch28–52 against everything now in memory. An item marked ⇢ lands on a chapter that has not been written.

## 0. State of the book

| ch | title | POV | final | proposed Front ticked | gate |
|---|---|---|---|---|---|
| 6 | Separately | Nuvalik | r1 | project-zombification s1, push 2/3 | pass, undecided |
| 7 | The Lick-Keeper | Wystan | r2 | the-night-register-file s1, push 4/5 | pass, undecided |
| 8 | Rounding | Foss | r0 | project-zombification s2, push 1/3 | pass, undecided |
| 9 | Two Myriads | Wystan | r1 | the-swale-wastage s1, push 2/3 | pass, undecided |
| 10 | The Ninth Hind | Vesk | **r2** | project-zombification s1, push 3/3 (**filled**) | **revise**, undecided |

- **Ch10's memory was built from r2, and r2 is the draft with the gate FAIL.** `ch10/final.md` is byte-identical to `draft_r2.md`. `GATE.md` names r2 as the accepted draft and gives the verdict "revise": 1 FAIL (Foss holds the glass in his hand) and a continuity WARN ("which Vesk had never seen anybody but Nuvalik do").
- **`draft_r3.md` fixes both,** and `digest_r3.md` reads "pass (fail 0, warn 5)". r3 was written at the same minute as the gate but was never accepted. In r3, Foss's glass is "screwed into his eye", and the book line becomes "Foss went to the shelf over the press and took the book down, and Nuvalik watched him do it and said nothing."
  - If Isaac takes r3, fact #302's parenthesis "(only Nuvalik had before)" has to come out of `state.json`.
  - r3's own WARN also stands: the narration line "it went as slowly as it had gone every day since the fifth" confirms Vesk's declared ch6 lie, that sealed tempering works.
- Every chapter in memory still comes from the unattended run, and no gate has been decided.
- `GATES.md` still reads "Chapters 0/80 written", which is stale.

## 1. Hooks

### Overdue (due_ch passed, not paid): CRITICAL
**None.** Three hooks came due by ch10, and all three are paid:
- H08, due ch6, paid ch6
- H01, due ch7, paid ch7
- H21, due ch10, paid ch10

The next due dates are H23 (ch16) and H16 (ch22). **H16 is at risk. See C2.**

### Dormant (no event in more than 3 chapters): WARN
| hook | last event | chapters silent | next outline touch |
|---|---|---|---|
| H11-the-sky-finishes | ch2 | 8 | ch13 (Nuvalik "thinks about the sky") |
| H13-low-ground-sink | ch3 | 7 | ch23 at the earliest. ch5 touched it and no event was logged (see C4) |
| H15-six-who-know | ch3 | 7 | none before ch35 |
| H24-brack-signs-bleed | ch3 | 7 | ch12, ch16 |
| H19-the-hollow-shaft-people | ch4 | 6 | ch20. Ch10 bears on it (see C13), and no event was logged |
| H04-tallys-second-dataset | ch5 | 5 | ch14 |
| H09-nuvaliks-three-names | ch6 | 4 | ch13 |

- **These trip at ch11 unless touched:** H06 (last event ch7), H12 (ch7), H14 (ch7) and H23 (ch7). Ch11 is Deming's POV, so all four will trip. Ch12 is the first chance to touch them again.
- **Events the text carries that memory missed:**
  - The ch5 events flagged last audit are still missing: H05 ("Clerk said you were a person."), H06 (the crust held by the edge, and the lapse at the stone) and H13 ("which was always him").
  - Ch9's brass strike at the registry counter is not logged against H14.

### Open hooks: WARN
- **23 open** (planted or advanced, not paid): H02–H07, H09–H20, H22–H24, H28 and H32. That is over 12.
- **3 paid:** H01, H08 and H21.
- **6 planned, not yet planted:** H25, H26, H27, H29, H30 and H31.
- The count has not come down since ch5. Ch6–10 paid three hooks and planted three (H20, H22, H28).

### Hook texts that no longer match the page: NOTE
- **H01** says it pays when "the lick-keeper's round is found to end at the marker". The ch7 page, and the pay event itself, end the round at the birch, "well short of the stone".
- **H08** still quotes "will discuss with her separately", a line that is only in ch2 r1.

Both are text in the hook rows, not on the page. Nobody should write a later payoff from either hook's text.

## 2. Cast

**POV cast with no fact for more than 5 chapters (WARN): none yet.**

| POV member | last fact | next POV chapter |
|---|---|---|
| Wystan Ashmore | ch9 | ch12 |
| Qiu Yinzhi | ch9 | ch21 |
| **Nol Tally** | **ch5** | ch14 |
| Vesk | ch10 | ch17 |
| Nuvalik | ch10 | ch13 |
| Ilmar Foss | ch10 | ch27 |
| Xu Deming | ch10 | ch11 |
| Osric Salter / Malphas | Malphas ch10 | Salter first on the page ch73 |

- **Tally is at exactly 5 chapters,** and he trips at ch11. He is not in the cast of ch11, ch12 or ch13, so he will be 8 chapters silent by ch14 unless ch12 gives him a fact. Ch9 used his count, but the fact's subject is "Ferriby pour".

**Death fact followed by the subject acting (CRITICAL): none.**
- No person has a death fact.
- The ninth hind stands (ch10) after "Eleven days of the ferment" (ch2). That is the premise, not a breach.
- The fourth hind is "finished now" (ch6) and does not act again.
- Keld is alive (ch3).

**Subject names are still not normalised (WARN).** Memory uses these forms side by side:
- "Foss" (ch6–10) and "Ilmar Foss" (ch2)
- "Yinzhi" (ch5–9) and "Qiu Yinzhi" (ch1)
- "Tally", with "Nol Tally" never used
- "Deming", with "Xu Deming" never used
- "Brack" and "Edwyn Brack"

A lookup by the outline's name finds no facts for Tally or Deming, and only ch2 facts for Foss.

## 3. Sag

**None.** Every chapter ticks a proposed Front and advances at least one hook.

| ch | Front push | hooks |
|---|---|---|
| 1 | the-night-register-file s1 | plants 8 |
| 2 | project-zombification s1 | plants 6 |
| 3 | the-night-register-file s1 | H23, H24, plants 5 |
| 4 | the-swale-wastage s1 | plants 4 |
| 5 | the-night-register-file s1 | H01, H04, H23 |
| 6 | project-zombification s1 | **pays H08**; H07, H09, H10, H21; plants H20, H28 |
| 7 | the-night-register-file s1 | **pays H01**; H05, H06, H12, H14, H23, H32 |
| 8 | project-zombification s2 | H05, H07, H17, H20, H28; plants H22 |
| 9 | the-swale-wastage s1 | H02, H03, H05, H17, H32 |
| 10 | project-zombification s1 | **pays H21**; H07, H10, H16, H18, H28 |

Ch9 ticks Deming's Front from Wystan's POV. It counts, because the world changes (a standing request now lies against the Swale line) and the POV sees the consequence (the refusal).

## 4. Continuity

### Identity: Wystan learns Malphas, or Malphas learns Wystan (CRITICAL if found)
**No such line.** I searched every final sentence by sentence:
- **Cell-side chapters (2, 4, 6, 8, 10)** for Ashmore, Wystan, Cutler, Warden, brass, Register, Timberline, Yinzhi, Tally, Lyle, Keld and Society.
- **Register-side chapters (1, 3, 5, 7, 9)** for Malphas, Lord, Greyshaft, Vesk, Foss, Nuvalik, Ilmar, Deming, Xu, coldhouse, press, Salter, project and Zombification.

What came up:
- **Register side: nothing.**
- **Cell side: only the institution.** "Man from the Register's been at the Ferriby lick-keeper." "Which register." "Somebody the Register sent." (ch8). "The one their Wardens of Duty are issued." (ch2, a rank). The other hits are brass on meters and weights.
- **Ch7 and ch8 held the line.** Josse gets "Register, then." and no name. The carter chain has "no name, no description". Foss's manual print has "no number, name, chapter or mark of origin".

Near misses the next chapters could turn into a CRITICAL:
- **Tally holds "Ashmore"** (ch5), and from ch14 he walks the Swale walks, where the carter and the keepers now set the cell's licks (ch8).
- **Josse has seen Wystan's face,** his hair to the waist and his brass (ch7). He is the head of the chain that reached Foss in one day (ch8). Ch38 sends Nuvalik to the Ferriby cut.
- **⇢ ch34.** Foss asks at inns who the Night Register is. The bible allows at most "a desk on Cutler Row with a brass token". A physical description would arm the ch60 gallery.
- **Ch10 is a structural mirror.** The hind leans to the corner where Malphas sits and he rises and goes to the door. Vesk takes it for courtesy, and the bible allows this once. A second lean that follows him (⇢ ch46, Vesk's own body leaning to the corner while Malphas is in the room) would be the narration winking.

### Resolved since the ch5 audit
- **C2** (the manual a season early): ch6 has "I said a season and I was wrong by a season."
- **C3** (who knew of the contraction): ch6 has "twice is what you said to Vesk and twice is wrong."
- **C4** (where the last lick is): ch7 has it "just inside the birch on the east side … no post on it after this one", well short of the stone.
- **C5** (when the block was set): ch7 has "Set a new one there back before the thaw came in."
- **C6** (the count Wystan prices): ch9 prices eleven hinds and a stag.
- **C9** (the ninth hind's day count): ch10 prints no day count for her.

### Contradictions

**C1: CRITICAL ⇢ ch13–14 (Front project-zombification s2).** The Swale licks cannot be out in time.
- ch8, Foss: "Same night, next turn," which puts his next meeting with the carter on Day 22. Malphas: "Next turn you take the carter the walks."
- ch8 also has "one block to a keeper to begin with", the carter being the only route, and "Nobody from the cell has touched a lick" (outline ch13).
- Outline ch13 (Days 17–18): hinds "that took the dosed licks die standing, then, days later, get up". Ch14 (Days 20–21) has Tally see one walking. Ch17 (Day 25) has "the walks run eleven miles".

Those deaths need blocks on the Swale walks by about Day 13. As ch8 left things, the carter gets the walks on Day 22.

**C2: CRITICAL ⇢ ch19, ch22 (H16, due ch22).** Deming's count of thirty-one days.
- ch4: "put his finger on today and counted forward, a square to a day … *Thirty-one.*" He did the same sum "walking home from the coldhouse", after the ninth division of Day 1. That makes his last useful day Day 32 or 33.
- Outline ch19 (Day 27): "He counts: nineteen days of usefulness left." That arithmetic ends on Day 46.
- Outline ch22 is dated "Day 31".

**C3: CRITICAL ⇢ ch12.** This carries C7 from the ch5 audit.
- ch3: "*The Register may keep this curiosity open until the quarterly inspection of the gauge-housing, and not a day longer.*" The position ("a dose goes where it is put") is in Lyle's minute under her silver, initialled.
- Outline ch12: "Lyle gives Wystan until the quarterly inspection … and enters the edges memorandum as the Register's position."

**C4: CRITICAL ⇢ ch23, 25, 44 (H13).** This carries C1 from the ch5 audit.
- ch3, the declared misreading: "it came down on everybody in the room alike".
- ch5: "In a shut room the free residue ran its gradient down to the emptiest thing present, which was always him".
- Outline ch23: Yinzhi sees the lean shift when he moves, "and he says it is the draught". Ch44 pays "he is the sink".

**C5: CRITICAL ⇢ ch46, and H07 through ch60.** Where Malphas sits, and where the book lives.
- **ch2:** "Malphas was on the gauge bench with his coat folded beside him, in the same place he had been sitting since the first division", and "The press threw its warm air along the east wall and the gauge bench stood in the middle of it, and that was the whole of why the Lord's hands never took the cold." That is Vesk's declared misreading, never corrected.
- **ch6, ch8 and ch10:** Malphas is on "the iron bench under the dead standpipes". Ch10 adds: "The iron bench was the whole width of the room away from the press", and "Foss sat in it, and Foss's hands were pink with it".
- So ch10 puts the refutation of Vesk's misreading in front of Vesk, and he "makes nothing of it". The bible's standing irony survives by one clause.
- **The book (fact #87 against #239):**
  - ch2 has it "on the shelf over the press where it has been since the first night", and ch6 and ch10 agree.
  - ch8 has "The book was under it [the cloth on the gauge bench], where it was always put".
- **Who takes the book down (facts #98, #239 and #282 against #302):**
  - ch2 ends with Vesk himself taking it down: "Then he went to the shelf for the book and wrote the division in the margin."
  - ch8 has Foss write in it and initial "I. F.".
  - ch10 r2 has Foss write in it at the gauge bench earlier the same night.
  - Yet ch10 r2 says "which Vesk had never seen anybody but Nuvalik do". r3 cuts the clause.

**C6: CRITICAL ⇢ ch43.**
- ch6, in Vesk's hearing: house rule three, "nothing comes from a flask to me, or from the substrate to me, without a second pair of hands between". Also "You put your hand on the ninth hind's flank on the first night", which Malphas calls a bad habit that stops now.
- Outline ch43: "Vesk sees for the first time that the Lord never touches anything live."

**C7: CRITICAL ⇢ ch51.** The carter's inn account.
- ch8: "The bars leave no bill", and "Pan salt would not hold a stamp through a wet season". Foss pays only in salt bars, and he and the carter have never had each other's names.
- Outline ch51: Wystan builds the purse file from paper that includes "the carter's inn account".

**C8: WARN.** Foss's asking for the manual.
- ch6: "I was going to ask men in turn. I did not have to ask anybody."
- ch8: "He had spent a season on this road asking for a book", and aloud: "I asked on that road for a season. For the book. I asked a spoon-woman."
- On the page, five days separate ch2's "It will be a season" (Day 1) from ch6 (Day 5). Foss's ch8 misreading (#232) rests on the longer version.

**C9: WARN.** The brass is in two places in ch9.
- Morning: "The Ferriby tin was on the sill under his brass … and left them where they were."
- The eleventh division: "struck his brass into the wax" at the registry counter.
- Then: "The tin was on the sill under his brass where he had left it".

**C10: WARN.** Vesk's ch6 line is stored as fact.
- ch2: the ninth hind's hide "draws up once, a hand's breadth"; Vesk "tells nobody".
- ch6: "I have had nothing like it off any of the others and I have had all nine of them through my hands."
- Fact #190 records this as a plain number. It is his concealment continuing, so treat it as a lie that nobody has corrected.

**C11: WARN.** The eighth hind's reproduction is never reported.
- ch6: "By the eighth division tomorrow I want a shoulder that draws … in the book in both."
- Ch8 (Day 9, at Greyshaft) and ch10 (Day 12) never say whether it drew. Ch10 has only "He had stood at the door just that way through the eighth hind's pours".

**C12: WARN.** Wystan's blood has now met the dose.
- ch7: "The cracks at the nails had gone from stinging to a steady burn" after he gripped a block that is "carrying". Ch9: the skin "still catches the pen".
- ch9, Yinzhi: the compound "crosses over in blood". The bible's Mechanism: those who take the salt "carry it at sub-lethal dose".
- No hook, Ledger proposal or flag records this. It is Isaac's call whether it means anything. Until he makes it, no chapter should show an effect.

**C13: NOTE ⇢ ch20, ch50 and ch66 (H19).** Deming's name is now in the cell's book.
- ch10: "I want it written … that I have heard it," and Foss writes it.
- The man who fears "a name in a private correspondence" (ch4) has put his own name in the project's book. Ch66 burns Greyshaft Nine, and the book's fate is never planned.

**C14: NOTE ⇢ ch17.** "Four to six" days.
- ch2, Foss: "Days. Four to six." The ninth hind was poured on Day 1 and stood on Day 12.
- Outline ch17: "the walks run eleven miles and four to six days, exactly as said."

**C15: NOTE ⇢ ch48 (inside the band).**
- Outline ch22 (Day 31): the last letters are posted.
- Outline ch48 (Day 77): "the letters were posted a turn and a half ago." Forty-six days is more than three turns.

**C16: NOTE ⇢ ch24.** A name Malphas has not yet said.
- Outline ch24: Nuvalik "knows the name Malphas said" for the man with the rule (Tally).
- No page has Malphas say Tally's name. Ch13 or ch17 has to give it to her first, and only as the name on a Society insert.

**Still open from the ch5 audit (unchanged):**
- **C8, WARN.** The stables and the medical house. ch3: "behind the Division's stables". ch5: "The Division's stables stood behind the medical house".
- **C11, WARN ⇢ ch47–48.** Eleven weeks from Day 2 is Day 79, and the outline has "Day 77 … to the day".
- **C12, WARN.** Greyshaft Nine's history: the inspections stopped nine years ago and the main was capped four years ago.
- **C13, WARN ⇢ ch65.** A disciplinary observation is already on file (ch3).
- **C14, NOTE.** The counts: eleven hinds and a stag at Ferriby, and nine on the rail.
- **C15, NOTE ⇢ ch37.** Tally's lick salt appears only in the notes.
- **C16, NOTE.** Divisions, not hours.

**The #28–52 seam, checked:**
- **#28 against #216:** the minute count is consistent. The forty-second is beneath forty-one (ch1). The forty-third is over "forty-one more, forty-two with Keld's" (ch7).
- **#34 and #42–43 against #262:** the brass. See C9.
- **#45** (Keld's silver token, never collected): nothing has touched it. The ch6 print carries no number, so the ch5 near miss is closed.
- **#36** (the disciplinary observation) is still ⇢ ch65.
- **#46** (the stables) is still C8 of the ch5 audit.

## 5. Front status (proposed, bible)

| Front | segment | pushes done | next |
|---|---|---|---|
| project-zombification | 1 The dose walks | ch2, 6, 10: **filled** | — |
| project-zombification | 2 Release | ch8 (1/3) | ch13, ch17 (fills). **Blocked by C1** |
| the-night-register-file | 1 Exhibit one | ch1, 3, 5, 7 (4/5) | ch12 (fills). See C3 |
| the-swale-wastage | 1 Diversion | ch4, 9 (2/3) | ch11 (fills) |
| the-quiet-districts | 1 Enforcement asks | 0 | ch26 |

Every `front_id` is still null. Nothing has been written to `table/fronts.yaml`.

## Carry-forward

1. Ch11–13 (C1): ch8 left the carter's next meeting at "Same night, next turn", which is Day 22. Before ch13, show on the page Foss going to the carter off-turn by about Day 13 and handing him the Swale walks, and say why he broke the turn, so the carter's man has blocks on the walks in time for the Day 17–18 deaths.
2. Ch19 and ch22 (C2, H16): Deming counted thirty-one squares forward from Day 1–2, so in ch19 (Day 27) he counts five or six days left, never "nineteen". Set ch22's dismissal on Day 32 or 33, or print no day number and call it the square his finger stopped on.
3. Ch12 (C3): Lyle's term (to the quarterly inspection) and the Register's position have been in her minute under silver since ch3. Write ch12 as an addition to that minute (produce a purse by the inspection), not as a first entry.
4. Ch23–44 (C4, H13): ch5 has Wystan already knowing that shut-room residue runs "always" to him. In ch23, make "it is the draught" something he says to Yinzhi and does not believe. Keep his wrong belief to the dead being *sent* to him, and pay ch44 as "nobody sent them", never as news that he is the low point.
5. Identity (ch14, 24, 34, 38): Tally speaks "Ashmore" to nobody on the Swale walks. Nuvalik at the Ferriby cut meets nobody from the estate round and hears nothing of Josse's visitor. Foss's ch34 inn report stops at "a desk on Cutler Row with a brass token and a man on nights", with no name and no description (no hair, no eyebrow scar, no edge-held cup).
6. Coldhouse (C5): from now on Malphas sits on the iron bench under the dead standpipes on the west wall, and the book lives on the shelf over the press. Nobody sets the press's warm air against the west bench again, so Vesk's ch2 misreading stays unexamined. In ch46 Malphas stands at the door, out of the lean's line, so no dead thing leans toward him a second time.
7. Ch43 (C6): Vesk heard house rule three and Malphas's "bad habit" admission about the ninth hind's flank on Day 5 (ch6). Write his ch43 realisation as what the rule was for, now that the ferment is in his own grafts, never as seeing "for the first time" that the Lord touches nothing live.
8. Ch51 (C7): salt bars leave "no bill" and Foss and the carter have no names for each other (ch8). The carter thread in Wystan's paper file can only be the inn's own account of the carter's board and his cob on meeting nights. It is never a bill, receipt or entry for salt bars, and never Foss's name.
