# Audit after chapter 5: night-watch-zombification

Audited 2026-09-24. I read `outline.json`, `bible.md` (Proposed Fronts, cast and flags), `state.json` (31 facts, 32 hooks and 1 summary) and every chapter's `GATE.md`. Because `state.json` holds only chapter 3, I also read `final.md` and `final_notes.md` for chapters 1, 2, 3 and 5. Nothing else was edited, and no tool that writes was called.

## 0. State of the book (read this first)

| ch | title | POV | text | in state.json | proposed Front ticked | gate |
|---|---|---|---|---|---|---|
| 1 | The Docket Head | Wystan | final.md (r0) | **no** | the-night-register-file s1, push 1/5 | undecided |
| 2 | Twenty-Two Drops | Vesk | final.md (**r0**, though r1 exists) | **no** | project-zombification s1, push 1/3 | undecided (verdict "revise") |
| 3 | The Morning Check | Wystan | final.md (r0) | yes (31 facts, summary) | the-night-register-file s1, push 2/5 | undecided |
| 4 | A Number in the Room | Deming | **none: four rounds wrote no draft** | no | **the-swale-wastage s1: not ticked** | escalate |
| 5 | Who Set the Marker | Wystan | final.md (r0) | **no** | the-night-register-file s1, push 3/5 | undecided |

- **Memory gap (CRITICAL for the next briefs).** `state.json` has no facts, summaries or hook events from chapters 1, 2 or 5. A brief built from `state.json` alone will not see Yinzhi's lie, the tin, the chapter wax, the letter to Tally, anything that happened in the coldhouse, Tally's inventory, the stone, or the Called Late sequence. Hooks H01–H11 and H21 still read `"status": "planned"` even though the text planted them.
- **Chapter 2's final is the wrong round.** `ch02/final.md` is byte-identical to `draft_r0.md`. `draft_r1.md` fixes the r0 FAIL ("twelve days" → "eleven days"), plants the missing H08 line ("The fourth hind I will discuss with Nuvalik separately"), removes the "Wardens of Duty" line and resolves the ambiguous "He" to "Malphas". None of those fixes is in the final text.
- **Chapter 4 does not exist.** H16–H19 are unplanted, and the-swale-wastage has no push. Xu Deming has never appeared on the page.
- `GATES.md` still reads "Chapters 0/80 written". It is stale.

## 1. Hooks

The current chapter is 5. I assessed each hook two ways: against `state.json` as recorded, and against the text as the gates and notes quote it. The text version is the one that governs.

### Overdue (due_ch passed, not paid): CRITICAL
**None.** The earliest due dates are H08 (ch6), H01 (ch7), H21 (ch10), H23 (ch16) and H16 (ch22).

### Due within the next five chapters
- **H08-concealed-contraction, due ch6.** Only half-planted. The canonical ch2 text (r0) never has Malphas promise to discuss it "separately". It does have Vesk hear "The Lord said contraction. Twice, he said.", so Malphas already knows about the contraction. Nuvalik's lie stands: "Everything the fourth hind gave me is written down."
- **H01-far-side-of-the-marker, due ch7.** The hook text says it pays "when the lick-keeper's round is found to end at the marker". Ch5 established that the estate's round does **not** end there: it "met the stone at its south-east corner and bent away west along the foot of the rise." See continuity C8.
- **H21-the-ninth-hind, due ch10.** Planted in ch2 ("The ninth hind is the freshest and she is the one I want.").

### Dormant (no event in more than 3 chapters): WARN
- **H02-quarter-inch-sealed:** planted ch1, with no event in ch2–5.
- **H03-chapter-wax:** planted ch1, with no event in ch2–5.
- **At the threshold** (planted ch2, silent in ch3–5): H07-warm-hands, H09-nuvaliks-three-names, H10-vesks-grafts, H11-the-sky-finishes, H21-the-ninth-hind. They become dormant after ch6 unless ch6 (Nuvalik POV, with Vesk and Malphas in the room) touches them. H08 is paid in ch6.
- **By state.json alone,** nothing is dormant, but only because the ch1/ch2 plants and ch5 events were never recorded.

### Unplanted, because ch4 is missing: WARN, and CRITICAL once ch22 nears
H16-thirty-one-days (due ch22), H17-eleven-weeks (due ch47), H18-the-project-name-is-the-file (due ch57) and H19-the-hollow-shaft-people (due ch58). H16 pays in ch22, and nothing has planted it.

### Open-hook count: WARN
- **By the text: 19 open.** Ch1 planted H01–H06, H23 and H24. Ch2 planted H07–H11 and H21. Ch3 planted H12–H15 and H32. None has been paid. That is more than 12.
- **By state.json: 7 open** (H12, H13, H14, H15, H23, H24, H32).

### Events the text made that state.json lacks
- **ch5 H01:** the stone identified; the sequence stated; *the round.*
- **ch5 H04:** Tally's notebook, "North of the stone. Nothing."
- **ch5 H23:** the margin now reads *the round.*
- **ch5 H05, callback:** "Clerk said you were a person."
- **ch5 H06, callback, including the lapse:** "He had not held it by the edge."
- **ch5 H14:** the brass shown on the palm.
- **ch5 H13:** "which was always him" (see C1).

## 2. Cast

- **POV cast with no fact in state.json** (WARN, at threshold): Qiu Yinzhi (on the page in ch1 and ch5), Vesk, Nuvalik and Ilmar Foss (ch2), Nol Tally (ch5), Xu Deming (never on the page). All of them have gone 5 chapters with no fact. The rule trips at more than 5, so every one of them trips after ch6 unless ch1, ch2 and ch5 are carried in. Wystan has facts (ch3). Osric Salter is not due until ch73.
- **Death followed by acting:** none. There are no death facts. Keld is alive (ch3: "Keld was alive."), and no cast member has died.
- **Standing irony, on track (not an error):** bible item 2 depends on Malphas having pressed the hind. In the ch2 final that sentence reads "He put two fingers against the ninth hind's flank" with an ambiguous "He" (the r0 WARN). Later chapters may rely on it only as the bible does: never pointed at.

## 3. Sag

**No sag.** Ch1 ticks the-night-register-file s1. Ch2 ticks project-zombification s1. Ch3 ticks the-night-register-file s1 and advances H23 and H24. Ch4 has no text, so it ticks nothing and advances nothing. Ch5 ticks the-night-register-file s1 and advances H01, H04 and H23. No three consecutive chapters go without a tick.

- **Watch 1:** the-swale-wastage has zero pushes, and its segment 1 is planned for ch4, 9 and 11.
- **Watch 2:** the bible lists ch8 as a push of project-zombification **segment 2** ("Release": ch8, 13, 17) while segment 1 fills only at ch10. That ordering is out of step (WARN, a bible matter).

## 4. Continuity

The written text is ch1, 2, 3 and 5. I read every summary and fact in order and checked the finals against each other. **The ch28–52 band has no text yet.** Contradictions that reach into that band are marked ⇢.

### Identity (Wystan learns Malphas, or Malphas learns Wystan): CRITICAL if found
**No such line exists.** There are two near misses, and they are why carry-forward line 6 exists:
- **ch2, Malphas:** "The one their Wardens of Duty are issued." This names a rank, not a person. It is WARN-flagged at the gate, and r1 removed it.
- **ch5, Wystan to Tally:** "Ashmore. I keep it." This is the first time the name reaches anyone near the Ferriby round. The carter chain to Foss begins in ch8 ("a man from the Register has asked the Ferriby lick-keeper").

### Contradictions

**C1: CRITICAL ⇢ ch44 (H13, bible "What Wystan believes" 1).** Does Wystan know the residue runs to him?
- ch3: "It was what any shut room did by this hour, with the main running under it and people at work in it all day, and it came down on everybody in the room alike; Lyle had simply never sat a night on the Register, and had nothing on her hands to feel it with."
- ch5: "In a shut room the free residue ran its gradient down to the emptiest thing present, which was always him; in the open there was no room, and what had come off the dead lay where it had come off and went on coming apart."

Ch3's declared misreading is uncorrected on the page, and ch5 has him state the corrected physics as settled knowledge two chapters later. H13 ("paid when he learns he is the sink") and ch44 "Low Ground" assume he does not know. The ch5 notes do not flag this.

**C2: CRITICAL ⇢ ch6 (H20).** Can the field manual be had, and how soon?
- ch2, Foss: "It is a numbered issue. Every copy has a number cut into the board and the number is against a name in an issue book … I will ask a man. He will say no and I will ask a second man. It will be a season." Malphas: "A season is acceptable."
- ch5: "The whole of the chapter's bench had read the field manual, looking for the part about themselves."
- Outline ch6, Day 5 (four days after ch2): "Foss reads the Division field manual aloud, the unsigned paragraph".

**C3: WARN.** Stables and medical house.
- ch3: "The medical house stood two streets over, behind the Division's stables"
- ch5: "The Division's stables stood behind the medical house"

**C4: WARN.** Ch2 contradicts itself, and the gate FAIL was left unfixed in the final. It matters for ch10's "dead twenty-three days".
- ch2: "in twelve days Vesk had watched for the thing that men like him were supposed to have"
- ch2: "Eleven days he had watched for it. The twelfth had started at the second division"

The working count is that Day 1 is the ninth hind's twelfth day, so Day 12 is her twenty-third. That agrees with the outline.

**C5: WARN.** Greyshaft Nine's history, also inside ch2.
- ch2: "the seal broken on a quarterly inspection that had stopped coming nine years ago"
- ch2: "The main under Greyshaft Nine had been capped four years"

Together these leave the main live and uninspected for five years. The bible gives only "a main capped four years".

**C6: CRITICAL ⇢ ch9.** The outline carries the cell's count into Wystan's head.
- ch3: "\"Into eleven hinds and a stag.\"" Lyle says it back, and the clerk writes it down.
- Outline ch9: "the price of third-dilution Verdantia against nine hinds and a stag".
- bible Flags: "Wystan's ch9 arithmetic uses Tally's count." Nine is the rail at Greyshaft Nine (ch2: "nine carcasses signed by nobody"), which Wystan cannot know.

**C7: CRITICAL ⇢ ch12.** The outline repeats what ch3 already did.
- ch3 fact: "*The Register may keep this curiosity open until the quarterly inspection of the gauge-housing, and not a day longer. E. Lyle, Prime Warden.*" The position was copied into her minute in ink under her silver, and Wystan initialled both.
- Outline ch12: "Lyle gives Wystan until the quarterly inspection to produce a purse, and enters the edges memorandum as the Register's position."

**C8: CRITICAL ⇢ ch7 (H01).** Where the round goes.
- ch5: the estate's round "met the stone at its south-east corner and bent away west along the foot of the rise". The Called Late passes "None went on past the place where they stopped, or followed the round where it bent west along the bound."
- H01's text: "Paid when the lick-keeper's round is found to end at the marker". The ch7 outline has "the last [lick] twenty-two paces short of the marker".

**C9: CRITICAL ⇢ ch7.** How recently the carrier walked the round.
- ch5: "The newest were weeks old." The stopping place "lay just inside the birch on the east side, on the estate's round". Wystan stood all night 22 paces from the stone and at dawn looked "a long way down" the round.
- Outline ch7 (Day 7): the lick-keeper Josse is actively setting "the new tonic blocks", one lick every half mile, the last 22 paces short of the marker. Ch8 moves the licks only after ch7.

Ch7 has to explain why Wystan, Yinzhi and Tally saw no block on Day 5, and why no pass is days old. The ch5 notes intend the licks to be "inside the birch, out of sight of the cut".

**C10: WARN ⇢ ch65.** "Disciplinary observation" is used early.
- ch3: "The Division had entered it in his file under a different heading, in the copying hand, as a disciplinary observation."
- bible (l.129): the disciplinary observation belongs to ch65 ("Disciplinary").

**C11: NOTE.** Is Cutler Row a place of exile or the head office?
- ch1: "since the Division wanted a particular officer somewhere else and found him a scullery on Cutler Row"
- ch3 header: "the Arbitration Division's northern office on Cutler Row"

This reads consistently if "somewhere else" means away from a full desk. The bible lists them as separate places, but the text has made them one house (ch1 notes, originated).

**C12: NOTE.** Time units.
- ch2: "It has been in since the eleventh hour". The bible says the book counts divisions, not Guild hours.
- **Clock:** ch5 fixes the eleventh division at dusk and the sixth at first light. On that clock, ch3's ninth-division bell, which rings after Wystan wakes at noon, walks to the medical house, sits his usual time with Keld, and then sees Lyle and Brack, puts the whole of that in about an hour. It is tight, not impossible. Later chapters should not pin divisions to clock hours.

**C13: NOTE ⇢ ch28–52 band.** Ch5's notes originate Tally's lie as helping himself to the estate's set-out salt, and that is what ch37 relies on ("the lick salt he has carried and eaten for two months"). The page does not state the motive. Ch37 must not contradict ch5, where the food in Tally's pack is bread and cheese. The bible's minute count stands at 42 (Josse is the 43rd in ch7, the walked hind the 44th in ch15, the Wicket relief clerk the 45th in ch28).

## 5. Front status (proposed Fronts, bible)

| Front | segment | pushes done | next pushes |
|---|---|---|---|
| the-night-register-file | 1 Exhibit one | ch1, 3, 5 (3/5) | ch7, ch12 (fills) |
| project-zombification | 1 The dose walks | ch2 (1/3) | ch6, ch10 (fills) |
| the-swale-wastage | 1 Diversion | **0/3** (ch4 missing) | ch4, 9, 11 |
| the-quiet-districts | 1 Enforcement asks | 0 (starts ch26) | none yet |

No chapter has written anything to `table/fronts.yaml`. Every `front_id` is still null.

## Carry-forward

1. Ch6+ briefs: state.json holds only ch3, so read ch01, ch02 and ch05 `final_notes.md` directly. Treat `ch02/final.md` (r0) as canon: Malphas never said "separately", and Vesk already heard "The Lord said contraction. Twice." Open ch6's talk as Malphas's own summons over Nuvalik's lie about the book.
2. Ch6: show how Foss has the numbered field manual on Day 5 after ch2's "It will be a season". Use the route ch5 opened ("The whole of the chapter's bench had read the field manual"), a borrowed numbered copy, and let Foss remark that the season came early.
3. From ch6 on, Wystan knows residue in a shut room runs to him (ch5). Never restate ch3's "came down on everybody … alike". Keep his wrong belief (ch25–44) on the dead being *sent* to him. Ch44 pays only that the walking dead lean to him by the same gradient and nobody sent them.
4. Ch7: put the last lick inside the birch at the round's stopping place, out of sight of the cut. Josse's last pass to it must be weeks before Day 5 ("The newest were weeks old"). Pay H01 as "the lick circuit turned home there", because the estate's round goes on west along the bound.
5. Keep "Ashmore" off the salt route. Ch7: Wystan identifies himself to Josse by the brass and "the Register" only. Ch8: the carter and Foss carry only "a man from the Register". Tally, who heard the name in ch5, never passes it to Josse or the estate.
6. Draft ch4 before ch9, planting H16–H19 and ticking the-swale-wastage s1. Until it exists, no chapter treats Deming's thirty-one days, eleven weeks, the Project-name letter or the Hollow Shaft joke as already said.
7. Ch9: Wystan prices the dose against eleven hinds and a stag (his, Lyle's and the clerk's count in ch3), never the outline's "nine hinds and a stag". Nine is the cell's rail count, and he cannot know it.
8. Ch12: Lyle's term (until the quarterly inspection) and the Register's position have been in her minute, under her silver, since ch3. Write ch12's ruling as an addition to that minute (produce a purse by the inspection), not as a first entry.
