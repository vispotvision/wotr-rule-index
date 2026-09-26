# Nightly — 2026-09-26 03:30

## Overnight

No scene was archived since the last digest, and that last ran on the 24th, so this covers two nights.
The 96 cleared findings are not fixed prose: yesterday's R49 commit took the reification check out of verify.py altogether and dropped Kharven recurrence to a WARN, and 40 of the 41 new ones are the same antithesis hits re-tagged from "banned" to R49-40. The archive still carries 292 FAIL. Nothing moved on the page.
The one real new finding is that the wiki index now lists "Continuity map" 43 times, with a fresh copy of that page landing on the 23rd and twice on the 25th. It is the page publish was choking on: Notion caps a table at 100 rows, CONTINUITY goes in at 149, and publish died exit 1 three times yesterday midday. I would cut that table in two before the next run; the 43 copies sitting in Notion are a wiki call, so yours.

Sync is pushing — 114 files at 02:45, 96 at 03:13. All 49 failure lines predate 15:10 yesterday: that table cap, and the RULINGS.md conflict markers, which are gone now. One file still will not publish because its Notion page is not shared with the integration.
No backup since the 20th. Six days, nothing in the log since. That is the first thing I would deal with this morning.
Two gates want a word and nothing more is written until they get one: kharven-year ch1 and night-watch-zombification ch1.
Judger queue unchanged, 93 proposals across three scenes (29 / 21 / 43). validate PASS, docket 0 outstanding, conflicts open 10.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 10
- findings NEW 41 / CLEARED 96 / STILL OPEN 290

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

- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not merely push from above but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply a light that could be tangile, but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "was not simply empowerment, this was the freedom of expression, the revelation of nature i" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not just become physical, but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply an evasive measure, but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply erase events that had never occurred, but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "not just physically but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "which was more graceful than the" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "That is not cynicism, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] THE_YUKARI_BLOODLINE.md: antithesis 'not X but Y': "not merely see the threads the way the Moto saw them, as" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] THE_YUKARI_BLOODLINE.md: antithesis 'not X but Y': "not just that it was failing but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] WOTR_Vaeloris_Sequence.md: antithesis 'not X but Y': "It is not a finding, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_field_where_they_picked_them.md: antithesis 'not X but Y': "it was not a request and it was not a curse, it was" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_field_where_they_picked_them.md: antithesis 'not X but Y': "It is not a technique, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_20.md: antithesis 'not X but Y': "it is not a virtue, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_years_that_were_not_war.md: antithesis 'not X but Y': "not merely follow the causal web but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_2.md: antithesis 'not X but Y': "It is not cruelty; it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_7.md: antithesis 'not X but Y': "not just as" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_nights_watch.md: antithesis 'not X but Y': "That is not a mistake, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_nights_watch.md: antithesis 'not X but Y': "It is not a mark he puts on it, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_1.md: antithesis 'not X but Y': "that was more interesting than handsome" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_22.md: antithesis 'not X but Y': "not simply a blade because of the purpose that it brings as" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] Naiser_Death_Cozbi_Genocide_Niran_Fall.md: antithesis 'not X but Y': "not so much break beneath him as" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] YOKO_MISHIRO.md: antithesis 'not X but Y': "not just an animal with a clever face, but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_empty_place.md: antithesis 'not X but Y': "it is not mercy, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] verinus_what_a_thing_weighs.md: antithesis 'not X but Y': "which was more graceful than the" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] verinus_what_a_thing_weighs.md: antithesis 'not X but Y': "That is not cynicism, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_true_king_of_the_north_part_19.md: antithesis 'not X but Y': "that is more work than most" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] 08_charles_what_a_hand_is_for.md: antithesis 'not X but Y': "that is not a trick of language, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] wotr_the_weight_of_a_courier.md: antithesis 'not X but Y': "that is more work than most" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] 18_darius_the_hand_of_the_judger.md: antithesis 'not X but Y': "it is not holding a body still, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_holy_inquisition_part_1_the_kindling.md: antithesis 'not X but Y': "it was more a pressure than a sound" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] Niran_Awakening_Haruki_Reunion.md: antithesis 'not X but Y': "not so much bend as" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] Nisuke_Titan_Dominion_Strike.md: antithesis 'not X but Y': "not so much shake as" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] Cozbi_Dragon_Binding_and_Ashuras_Call.md: antithesis 'not X but Y': "not so much as" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] Cozbi_Pneuma_Unravel_Strike.md: antithesis 'not X but Y': "not merely kill but" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] direction_is_not_intention.md: antithesis 'not X but Y': "That is not indifference to them, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] verinus_weight_of_an_infant.md: antithesis 'not X but Y': "it is not a virtue, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] 04_verinus_the_hand_and_the_print.md: antithesis 'not X but Y': "it is not an insult, it is" (R49-40-NOT_X_Y; AI-tells §1)
- [prose] the_terms.md: antithesis 'not X but Y': "which is more levy than he" (R49-40-NOT_X_Y; AI-tells §1)
- [reconcile] Duplicate wiki pages (same title twice): Continuity map ×43

## Cleared since last night

- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not merely push from above but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply a light that could be tangile, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "was not simply empowerment, this was the freedom of expression, the revelation of nature i" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not just become physical, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply an evasive measure, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply erase events that had never occurred, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: reification: 22 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "weight came"; "the weight came"; "weight he carried"; "The weight pressed"; "the authority he car
- [prose] The_Path_of_Sorrow.md: reification: 6 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "the space between them and sat"; "the silence that followed"; "The question arrived"; "The questio
- [prose] The_Path_of_Sorrow.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "not just physically but" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "which was more graceful than the" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "That is not cynicism, it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: Kharven recurrence: 1 of the five signature items present (the death-house / the Waiting); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] WOTR_Vaeloris_Sequence.md: antithesis 'not X but Y': "It is not a finding, it is" (banned; AI-tells §1)
- [prose] WOTR_Vaeloris_Sequence.md: reification: 5 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "the weight of it came"; "the silence that came"; "grief that had settled"; "The weight went"; "aut
- [prose] the_true_king_of_the_north_part_9.md: reification: 3 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "silence followed"; "the grief came"; "Silence settled"
- [prose] the_true_king_of_the_north_part_9.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] THE_YUKARI_BLOODLINE.md: antithesis 'not X but Y': "not merely see the threads the way the Moto saw them, as" (banned; AI-tells §1)
- [prose] THE_YUKARI_BLOODLINE.md: antithesis 'not X but Y': "not just that it was failing but" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_1.md: antithesis 'not X but Y': "that was more interesting than handsome" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_1.md: reification: 4 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "weight settled"; "the silence that followed"; "the moment arrived"; "The silence that followed"
- [prose] the_true_king_of_the_north_part_1.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_20.md: antithesis 'not X but Y': "it is not a virtue, it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_20.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] 01_the_vacancy_korvaeth_arc.md: reification: 4 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "the moment it went"; "the moment he entered"; "the moment he left"; "silence held"
- [prose] 01_the_vacancy_korvaeth_arc.md: reification: two in one paragraph (R4-15-ONE_PER_PARAGRAPH): "the moment he entered"; "the moment he left"
- [prose] THE_KINGDOM_OF_KHARVEN_corrected.md: reification: 3 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "The question that followed"; "the moment he crossed"; "authority that moved"
- [prose] the_true_king_of_the_north_part_12.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_2.md: antithesis 'not X but Y': "It is not cruelty; it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_2.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_14.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_16.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_7.md: antithesis 'not X but Y': "not just as" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_7.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_3.md: reification: two in one paragraph (R4-15-ONE_PER_PARAGRAPH): "weight settled"; "weight always settled"
- [prose] the_true_king_of_the_north_part_3.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_field_where_they_picked_them.md: antithesis 'not X but Y': "it was not a request and it was not a curse, it was" (banned; AI-tells §1)
- [prose] the_field_where_they_picked_them.md: antithesis 'not X but Y': "It is not a technique, it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_6.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] 15_darius_kill_me_first.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] 21_darius_the_fist_of_god.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] verinus_what_a_thing_weighs.md: antithesis 'not X but Y': "which was more graceful than the" (banned; AI-tells §1)
- [prose] verinus_what_a_thing_weighs.md: antithesis 'not X but Y': "That is not cynicism, it is" (banned; AI-tells §1)
- [prose] verinus_what_a_thing_weighs.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] 10_wotr_what_the_ground_was_owed.md: Kharven recurrence: 1 of the five signature items present (the night-stone); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_house_of_abscene_kujo_arc.md: reification: 6 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "weight arrived"; "the moment he arrived"; "authority sat"; "Silence settled"; "authority she gathe
- [prose] the_true_king_of_the_north_part_17.md: Kharven recurrence: 1 of the five signature items present (wet wood); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_11.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_15.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_years_that_were_not_war.md: antithesis 'not X but Y': "not merely follow the causal web but" (banned; AI-tells §1)
- [prose] the_nights_watch.md: antithesis 'not X but Y': "That is not a mistake, it is" (banned; AI-tells §1)
- [prose] the_nights_watch.md: antithesis 'not X but Y': "It is not a mark he puts on it, it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_10.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] Naiser_Death_Cozbi_Genocide_Niran_Fall.md: antithesis 'not X but Y': "not so much break beneath him as" (banned; AI-tells §1)
- [prose] YOKO_MISHIRO.md: antithesis 'not X but Y': "not just an animal with a clever face, but" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_13.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_4.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_empty_place.md: antithesis 'not X but Y': "it is not mercy, it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_19.md: antithesis 'not X but Y': "that is more work than most" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_22.md: antithesis 'not X but Y': "not simply a blade because of the purpose that it brings as" (banned; AI-tells §1)

## Still open: 290 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 8 push(es), 1 quiet run(s), 49 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-20.zip (24.0 MB, 1077 files)
- last run of this digest: 2026-09-24T04:56:47
