# Nightly — 2026-10-04 03:30

## Overnight

The Style Law landed at 23:41 and that is the whole night: 138 rows, 82 files, and verify.py took the R70 checks. So the 72 new and 85 cleared findings are the new checker reading the same prose, not prose that moved, and still-open falling from 329 to 244 is the same thing. Only `the_drawing_off` was edited all day. Read none of it as fixes.

The Style Law also opened five conflicts, C-155 to C-159, and the open count went 40 to 43. Two of them bite at the table: C-158 has NATALIE.md capping technology at 1800 to 1900 against R53-01 running the Imperial Age into the mid-1900s, and C-156 leaves it unsaid whether a set-off readout screen may appear on the page. Both are yours to rule.

`the_drawing_off` verifies PASS at standard band, no FAIL. The single warn is the Kharven recurrence check run against a Dawi scene, which reads to me as the check pointed at the wrong culture; I have not touched it. scene_context returns twelve names with no page: Kalrin, Torin, Halfturn, Gorrgorr, Snorin, Valtrin, Varrak, Thur, Welling, Petralon, Halrin, Obadiah Spigot. Snorin is one of Borin's brothers still waiting on your yes (R70-126), and none of the twelve can carry a number until they have a page. The close is `/judger the_drawing_off`.

The sync is exporting clean and then hanging at publish. The 01:00 run sat ninety minutes and systemd killed it at 02:30; the 02:30 run has been in `publish start` since 02:49 and is still there. Two export failures besides, both Notion read timeouts. Borin's card and The Scene Archive are exported and sitting uncommitted in the tree because publish never returns, which is why there was one push in 26 hours. I would stop the service and run the publish step by hand to find where it blocks.

Otherwise, in order: both book gates, a sixth night stopped, `--approve 1` or `--reject 1 --note "..."` for kharven-year then night-watch-zombification; then the three Judger closes, 93 proposals, oldest first. Cleared since the 29th: `mu_jin_the_old_colleague`. Still sitting from it: the em dash in `malphas_on_the_line_the_train_east`, which now carries two antithesis FAILs under the new check, two in `wystans_briefing_aetherion_arena`, one in `shioris_findings_aetherion_arena`. validate PASS, docket empty, backup wrote 34.2 MB.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 43
- findings NEW 72 / CLEARED 85 / STILL OPEN 244

## Scenes archived since the last run

- `the_drawing_off` — run `/judger the_drawing_off` for the close

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

- [prose] commencement_of_the_curia_kujo_arc.md: antithesis: 23 more
- [prose] commencement_of_the_curia_kujo_arc.md: hard-ban phrase: "Darkness gathered" in "...ed one hand beneath the black mantle of Xevorith. Darkness gathered above the tower in an enormou..." (R70-35-HARD_BAN_LIST)
- [prose] commencement_of_the_curia_kujo_arc.md: flat runs: 257 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] The_Path_of_Sorrow.md: antithesis 'not X but Y': "Not destroyed. Taken." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] The_Path_of_Sorrow.md: antithesis 'not X but Y': "Not the content. The physiological signature." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] The_Path_of_Sorrow.md: antithesis 'not X but Y': "Not squeezing. Gathering." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] The_Path_of_Sorrow.md: antithesis 'not X but Y': "Not a prince. A curse." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] The_Path_of_Sorrow.md: antithesis 'not X but Y': "Not a stop. A deceleration." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] The_Path_of_Sorrow.md: antithesis: 2 more
- [prose] the_true_king_of_the_north_part_9.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_9.md: antithesis 'not X but Y': "Not the concept. The substance." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_9.md: antithesis 'not X but Y': "Not a metaphysical principle. A sensation." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_9.md: antithesis 'not X but Y': "Not a weapon held. A sense extended." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_9.md: antithesis 'not X but Y': "Not the ship's. His." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] WOTR_Vaeloris_Sequence.md: antithesis 'not X but Y': "Not appended. Alongside." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] WOTR_Vaeloris_Sequence.md: antithesis 'not X but Y': "Not the resolving. The glass." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_2.md: antithesis 'not X but Y': "Not it. Her." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_2.md: antithesis 'not X but Y': "Not warmer. Broader." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] Niran_Mira_Return_to_the_Enclave.md: antithesis 'not X but Y': "Not grieving. Repairing." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] Niran_Mira_Return_to_the_Enclave.md: antithesis 'not X but Y': "Not asking. Measuring." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] CONTINUITY.md: antithesis 'not X but Y': "Not a patch. A deliberate concealment." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] CONTINUITY.md: flat runs: 44 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_1.md: antithesis 'not X but Y': "Not blockaded. Slowed." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_1.md: antithesis 'not X but Y': "Not flat. Level." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_14.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_14.md: antithesis 'not X but Y': "Not charged. Walked." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_14.md: antithesis 'not X but Y': "Not deference. Recognition." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_14.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] xanelor_the_morning_of_the_first_bell.md: antithesis 'not X but Y': "Not a patch. A deliberate concealment." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] xanelor_the_morning_of_the_first_bell.md: antithesis 'not X but Y': "Not contact. Displacement." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_house_of_abscene_kujo_arc.md: antithesis 'not X but Y': "Not administrative. Dynastic." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_house_of_abscene_kujo_arc.md: antithesis 'not X but Y': "Not all of them. Enough." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_house_of_abscene_kujo_arc.md: flat runs: 116 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_15.md: antithesis 'not X but Y': "Not the same movements. The same weight." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_15.md: antithesis 'not X but Y': "Not proximity. Me." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_years_that_were_not_war.md: antithesis 'not X but Y': "Not just the ground. People." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_years_that_were_not_war.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_8.md: antithesis 'not X but Y': "Not angry-cold. Hurt-cold." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_8.md: antithesis 'not X but Y': "Not you. Us." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_8.md: antithesis 'not X but Y': "Not reforge them. Improve." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_holy_inquisition_part_1_the_kindling.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_holy_inquisition_part_1_the_kindling.md: antithesis 'not X but Y': "Not loud. Present." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_holy_inquisition_part_1_the_kindling.md: antithesis 'not X but Y': "Not gone. Lessened." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] THE_KINGDOM_OF_KHARVEN_corrected.md: flat runs: 17 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_4.md: antithesis 'not X but Y': "Not the war. The holding." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_12.md: antithesis 'not X but Y': "Not warm. Active." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_12.md: antithesis 'not X but Y': "Not the verdict itself. The vision." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_10.md: antithesis 'not X but Y': "Not cruelty. Amusement." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_10.md: antithesis 'not X but Y': "Not estimates. Everything." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_13.md: antithesis 'not X but Y': "Not pain. Recognition." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_war_in_the_north_ii_the_road_two_days_south.md: antithesis 'not X but Y': "Not uncomfortably. Seriously." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] malphas_on_the_line_the_train_east.md: antithesis 'not X but Y': "Not regret. Recognition." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] malphas_on_the_line_the_train_east.md: antithesis 'not X but Y': "Not alarm. Assessment." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_18.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_18.md: antithesis 'not X but Y': "Not timidly. Carefully." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_16.md: antithesis 'not X but Y': "Not the nothing-smile. A warm smile." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_3.md: antithesis 'not X but Y': "Not behind him. Beside." (R49-40-NOT_X_Y; AI-tells §1)
- [prose] nine_hours_of_daylight.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_5.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_war_in_the_north_iii_utopia.md: sentences under 8 words: 5% of scene, floor is 18% (R4-14-HARD_CEILINGS)
- ... and 12 more (reports/prose_pass.md, reports/reconcile.md)

## Cleared since last night

- [prose] commencement_of_the_curia_kujo_arc.md: antithesis: 12 more
- [prose] commencement_of_the_curia_kujo_arc.md: hard-ban word: "testament" in "...emained cold beneath it.  “You wanted to become a testament.”  The black-gold fissure thr..." (R51-10-SLOP_WORDS)
- [prose] commencement_of_the_curia_kujo_arc.md: flat runs: 263 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_21.md: hard-ban word: "testament" in "...Come now, we have work to attend to. The will and testament of the divine judger cannot b..." (R51-10-SLOP_WORDS)
- [prose] CONTINUITY.md: hard-ban word: "testament" in "...ued | File's own dateline 'Charles Lambert's last testament, continued'; quoted 'I paid t..." (R51-10-SLOP_WORDS)
- [prose] CONTINUITY.md: flat runs: 46 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_22.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] YOKO_MISHIRO.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_field_where_they_picked_them.md: antithesis 'not X but Y': "It is not a technique, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_field_where_they_picked_them.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_field_where_they_picked_them.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] THE_KINGDOM_OF_KHARVEN_corrected.md: flat runs: 20 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_12.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_12.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_14.md: em dashes: 2 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_14.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_9.md: em dashes: 2 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_years_that_were_not_war.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_16.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_16.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_empty_place.md: antithesis 'not X but Y': "it is not mercy, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_empty_place.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_empty_place.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_18.md: em dashes: 2 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_18.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] xanelor_juggernauts_fist.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] xanelor_juggernauts_fist.md: flat runs: 8 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_house_of_abscene_kujo_arc.md: flat runs: 122 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_10.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_3.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 07_charles_the_imperceptible_district.md: hard-ban word: "testament" in "...*Kharven. The narrows. Charles Lambert's last testament.*   He got the chain over his..." (R51-10-SLOP_WORDS)
- [prose] 07_charles_the_imperceptible_district.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] no_entry_for_that.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] no_entry_for_that.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_inhale_register.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_8.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] in_form.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] in_form.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] nine_hours_of_daylight.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_5.md: flat runs: 7 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 13_darius_the_holiest_of_holy.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] geturo_ignite_tide.md: countdown negation: "No numbers in prose. Never written: no thought, action or reaction. Only the light bending off him and the fifth band reaching his boots." (AI-tells §1)
- [prose] the_holy_inquisition_part_1_the_kindling.md: em dashes: 7 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] geturo_the_host_line.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] mujins_interjection_aetherion_arena.md: em dashes: 9 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] mujins_interjection_aetherion_arena.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] renard_the_left_of_the_door.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] renard_the_left_of_the_door.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] 08_charles_what_a_hand_is_for.md: hard-ban word: "testament" in "...*The narrows. Charles Lambert's last testament, continued.*   He was still o..." (R51-10-SLOP_WORDS)
- [prose] Cozbi_Pneuma_Unravel_Strike.md: hard-ban word: "orbs" in "...ve accommodated.  "Conjunction. Pneuma."  Massive orbs of Pneumosphera bloomed into..." (R51-10-SLOP_WORDS)
- [prose] rovhen_the_dispensary.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] rovhen_the_first_lecture.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] sodoku_the_count_supply_report.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] xanelor_the_arrow.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_draught.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_blackmatch.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] what_motion_cannot_reach.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 04_sodoku_what_the_sky_does_not_ask.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] 17_darius_ignis.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] mu_jin_the_old_colleague.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)

## Still open: 244 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 1 push(es), 20 quiet run(s), 2 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-04.zip (34.2 MB, 1171 files)
- last run of this digest: 2026-10-03T03:30:00
