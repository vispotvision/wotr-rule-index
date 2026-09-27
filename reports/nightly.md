# Nightly — 2026-09-27 03:30

## Overnight

No scene was archived since the last digest, so nothing new waits on `/judger`. The queue is the same 93 proposals across three scenes (29 / 21 / 43).

Almost nothing in the findings moved because prose moved. The 38 that cleared cleared because verify stopped measuring anything below a `## Notes` heading, committed at 04:49 yesterday, an hour after the digest ran. Every em dash and flat run that vanished on those twenty-odd scenes was sitting in the author-facing notes at the foot of the file. The archive still carries 268 FAIL.

The 14 new ones are the same change from the other side. The R51-10 hard-ban word list went into verify at 03:48 yesterday, fourteen minutes after the digest, so tonight is its first count: eight "testament", two "whispers of", one "orbs". The three flat-run rows are recounts on scenes that lost their notes, not new flatness.

Three of the eight "testament" hits are one scene dateline, "Charles Lambert's last testament", in the two Charles scenes and quoted again in CONTINUITY. That is a title, not slop, and I would put the dateline to the docket as a carve-out and reword the other five, which are ordinary prose in Yoko's card, True King parts 21 and 22, the Curia opening and 05_sodoku.

The midnight ruling audit rewrote 16 rules to state exactly what you chose and restored three you chose that were never recorded, R57-26 to R57-28. It is logged in RULINGS.md, but there is no 09-27 block in CONTINUE, which is where you read the day's rulings, so I would write that block first thing.

Conflicts are 15 open, up from 10: C-084 to C-086 and C-088 from the society pass, C-089 to C-091 out of the audit. The last three are the new rule packs contradicting each other rather than canon disagreeing (ozone banned and free, numinous banned and in the free word bank, a Path gate binding one component or the whole Sub-Stat), and all three can be ruled off the packs' own words.

Both book gates have wanted a word since the 24th and nothing more is written until they get one: kharven-year ch1 and night-watch-zombification ch1.

The backup is back. Today's zip is 33.4 MB, 1116 files, the first since the 20th.

Sync is pushing, nine times, last at 01:55 with 119 files. All five failure lines are Notion read timeouts, three publish, one commit and one export at 17:13, and the next hourly run recovered each. The 100-row table cap has not fired since the 25th.

Two things from last night are still yours. YOKO_MISHIRO.md will not publish because its Notion parent is not shared with the integration, and the index still lists Continuity map 43 times.

validate PASS, docket 0 outstanding.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 15
- findings NEW 14 / CLEARED 38 / STILL OPEN 293

## Judger queue (proposals awaiting Isaac)

- 01_wotr_muster_breach_road_north: 29 waiting — `/judger apply 01_wotr_muster_breach_road_north ...`
- 04_sodoku_what_the_sky_does_not_ask: 21 waiting — `/judger apply 04_sodoku_what_the_sky_does_not_ask ...`
- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 10/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- [prose] commencement_of_the_curia_kujo_arc.md: hard-ban word: "testament" in "...emained cold beneath it.  “You wanted to become a testament.”  The black-gold fissure thr..." (R51-10-SLOP_WORDS)
- [prose] commencement_of_the_curia_kujo_arc.md: hard-ban word: "whispers of" in "...ries awakened along their surfaces in overlapping whispers of steel, screams, marching feet..." (R51-10-SLOP_WORDS)
- [prose] the_true_king_of_the_north_part_21.md: hard-ban word: "testament" in "...Come now, we have work to attend to. The will and testament of the divine judger cannot b..." (R51-10-SLOP_WORDS)
- [prose] CONTINUITY.md: hard-ban word: "testament" in "...ued | File's own dateline 'Charles Lambert's last testament, continued'; quoted 'I paid t..." (R51-10-SLOP_WORDS)
- [prose] the_true_king_of_the_north_part_22.md: hard-ban word: "testament" in "...r. Be proud, you stand beside me as a witness and testament to what I am willing to give..." (R51-10-SLOP_WORDS)
- [prose] YOKO_MISHIRO.md: hard-ban word: "testament" in "...ough what she has been through, which is either a testament to how she carries herself or..." (R51-10-SLOP_WORDS)
- [prose] 18_darius_the_hand_of_the_judger.md: hard-ban word: "whispers of" in "...e golden arms and into the head of Ignis, and the whispers of it ran along every filament i..." (R51-10-SLOP_WORDS)
- [prose] 07_charles_the_imperceptible_district.md: hard-ban word: "testament" in "...*Kharven. The narrows. Charles Lambert's last testament.*   He got the chain over his..." (R51-10-SLOP_WORDS)
- [prose] 13_darius_the_holiest_of_holy.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 10_wotr_what_the_ground_was_owed.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 08_charles_what_a_hand_is_for.md: hard-ban word: "testament" in "...*The narrows. Charles Lambert's last testament, continued.*   He was still o..." (R51-10-SLOP_WORDS)
- [prose] Cozbi_Pneuma_Unravel_Strike.md: hard-ban word: "orbs" in "...ve accommodated.  "Conjunction. Pneuma."  Massive orbs of Pneumosphera bloomed into..." (R51-10-SLOP_WORDS)
- [prose] 03_verinus_wall_between_the_safeguarded.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 05_sodoku_the_fixed_end.md: hard-ban word: "testament" in "...ind out how wrong over a period of years, and the testament that man made of him would ta..." (R51-10-SLOP_WORDS)

## Cleared since last night

- [prose] 19_aurelian_five_numbers.md: em dashes: 3 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 19_aurelian_five_numbers.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 19_aurelian_five_numbers.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 15_darius_kill_me_first.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 15_darius_kill_me_first.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 15_darius_kill_me_first.md: flat runs: 7 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 21_darius_the_fist_of_god.md: em dashes: 6 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 21_darius_the_fist_of_god.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 09_dabney_the_undamped_thing.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 09_dabney_the_undamped_thing.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 22_darius_punta.md: em dashes: 5 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 23_darius_the_fist_of_totality.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 23_darius_the_fist_of_totality.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 08_charles_what_a_hand_is_for.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 08_charles_what_a_hand_is_for.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 10_wotr_what_the_ground_was_owed.md: em dashes: 4 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 10_wotr_what_the_ground_was_owed.md: flat runs: 8 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 01_the_vacancy_korvaeth_arc.md: em dashes: 8 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 01_the_vacancy_korvaeth_arc.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 01_the_vacancy_korvaeth_arc.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 13_darius_the_holiest_of_holy.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 14_darius_two_men_who_would_not_take_the_seat.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 14_darius_two_men_who_would_not_take_the_seat.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 20_aurelian_no_signature.md: em dashes: 8 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 20_aurelian_no_signature.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 16_darius_let_nothing_be_sealed.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 02_wren_bulwark.md: em dashes: 10 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] 05_sodoku_the_fixed_end.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 05_sodoku_the_fixed_end.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 11_mujin_second_law_held_open.md: flat runs: 7 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 12_mujin_open_crucible.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 01_verinus_fire_of_the_undeserving.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 01_verinus_fire_of_the_undeserving.md: flat runs: 7 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 05_aurelian_primate_under_the_wrong_stars.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 03_verinus_wall_between_the_safeguarded.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 08_sodoku_recalescence.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 03_wren_three_deliveries.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 06_aurelian_what_the_lamberts_are_for.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)

## Still open: 293 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 9 push(es), 10 quiet run(s), 5 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-27.zip (33.4 MB, 1116 files)
- last run of this digest: 2026-09-26T03:30:00
