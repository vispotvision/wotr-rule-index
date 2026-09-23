# Nightly — 2026-09-23 17:44

## Overnight

Thirty-four scenes archived since the last digest: the whole True King of the North run (parts 1 to 22), the three Kujo/Curia scenes, CONTINUITY, and seven Xanelor. None of them has a close. That is the morning.

All 34 fail verify at standard band, and the same two faults account for most of it, flat runs and the 25-word chain ceiling, so treat this as two passes over the set rather than 34 separate jobs. Em dashes survived in ten files; CONTINUITY has 263 and reads like it never went through the strip at all. commencement_of_the_curia_kujo_arc is the outlier at 15 fails: eighteen "not X but Y", five countdown negations, 22 reifications. Kharven recurrence is 0 of 5 in roughly two dozen scenes.

Names with no page, the same ones over and over: Tenrai, Kokan/Kōkan, Selvara, Zaehaerys, Saishiki, Kamigan, Godfrey, Fern, Vaeloris, Kurosetsu, Thornwall. Those need cards before anyone writes a number about them. Your own name is listed as a no-page character in five scenes, which is transcript speaker labels that never got stripped.

Needs you: the kharven-year gate, where nothing more gets written until you run --approve 1 or --reject 1; the 43 proposals sitting on 08_sodoku_recalescence; and the sync, where 3 pushes landed but there are 8 failure lines and export exits 1.

Nothing cleared, 0 against 131 new and 255 still open. Validate passes, the docket is empty, the one conflict is still open, and the backup line still names the 09-20 zip.

I would answer the book gate first, drain the sodoku queue, then take the scenes in story order and leave the Kujo arc for last, since it needs the most rewriting.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 131 / CLEARED 0 / STILL OPEN 255

## Scenes archived since the last run

- `CONTINUITY` — run `/judger CONTINUITY` for the close
- `commencement_of_the_curia_kujo_arc` — run `/judger commencement_of_the_curia_kujo_arc` for the close
- `the_house_of_abscene_kujo_arc` — run `/judger the_house_of_abscene_kujo_arc` for the close
- `the_nights_watch` — run `/judger the_nights_watch` for the close
- `the_revolution_of_the_inner_world` — run `/judger the_revolution_of_the_inner_world` for the close
- `the_true_king_of_the_north_part_1` — run `/judger the_true_king_of_the_north_part_1` for the close
- `the_true_king_of_the_north_part_10` — run `/judger the_true_king_of_the_north_part_10` for the close
- `the_true_king_of_the_north_part_11` — run `/judger the_true_king_of_the_north_part_11` for the close
- `the_true_king_of_the_north_part_12` — run `/judger the_true_king_of_the_north_part_12` for the close
- `the_true_king_of_the_north_part_13` — run `/judger the_true_king_of_the_north_part_13` for the close
- `the_true_king_of_the_north_part_14` — run `/judger the_true_king_of_the_north_part_14` for the close
- `the_true_king_of_the_north_part_15` — run `/judger the_true_king_of_the_north_part_15` for the close
- `the_true_king_of_the_north_part_16` — run `/judger the_true_king_of_the_north_part_16` for the close
- `the_true_king_of_the_north_part_17` — run `/judger the_true_king_of_the_north_part_17` for the close
- `the_true_king_of_the_north_part_18` — run `/judger the_true_king_of_the_north_part_18` for the close
- `the_true_king_of_the_north_part_19` — run `/judger the_true_king_of_the_north_part_19` for the close
- `the_true_king_of_the_north_part_2` — run `/judger the_true_king_of_the_north_part_2` for the close
- `the_true_king_of_the_north_part_20` — run `/judger the_true_king_of_the_north_part_20` for the close
- `the_true_king_of_the_north_part_21` — run `/judger the_true_king_of_the_north_part_21` for the close
- `the_true_king_of_the_north_part_22` — run `/judger the_true_king_of_the_north_part_22` for the close
- `the_true_king_of_the_north_part_3` — run `/judger the_true_king_of_the_north_part_3` for the close
- `the_true_king_of_the_north_part_4` — run `/judger the_true_king_of_the_north_part_4` for the close
- `the_true_king_of_the_north_part_5` — run `/judger the_true_king_of_the_north_part_5` for the close
- `the_true_king_of_the_north_part_6` — run `/judger the_true_king_of_the_north_part_6` for the close
- `the_true_king_of_the_north_part_7` — run `/judger the_true_king_of_the_north_part_7` for the close
- `the_true_king_of_the_north_part_8` — run `/judger the_true_king_of_the_north_part_8` for the close
- `the_true_king_of_the_north_part_9` — run `/judger the_true_king_of_the_north_part_9` for the close
- `xanelor_juggernauts_fist` — run `/judger xanelor_juggernauts_fist` for the close
- `xanelor_seven_days` — run `/judger xanelor_seven_days` for the close
- `xanelor_the_arrow` — run `/judger xanelor_the_arrow` for the close
- `xanelor_the_bullet_train` — run `/judger xanelor_the_bullet_train` for the close
- `xanelor_the_challenge` — run `/judger xanelor_the_challenge` for the close
- `xanelor_the_constellations` — run `/judger xanelor_the_constellations` for the close
- `xanelor_the_dorms` — run `/judger xanelor_the_dorms` for the close

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not merely push from above but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply a light that could be tangile, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "was not simply empowerment, this was the freedom of expression, the revelation of nature i" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not just become physical, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply an evasive measure, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis 'not X but Y': "not simply erase events that had never occurred, but" (banned; AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: antithesis: 12 more
- [prose] commencement_of_the_curia_kujo_arc.md: countdown negation: "“No sermons. No cathedral. No witnesses telling you what your suffering means. Just pressure, darkness, and the body discovering that convic" (AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: countdown negation: "No bodies. No Names. No histories. No relationships. Only consciousness suspended over an absolute absence that provided nothing for conscio" (AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: countdown negation: "No corruption. Nothing offered to the maw. Only metal." (AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: countdown negation: "There was no second shield. No sword technique. No Aspect calculation. Only the child behind him." (AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: countdown negation: "No courtesy. No disguise. No attempt at civilization. Only Kujo." (AI-tells §1)
- [prose] commencement_of_the_curia_kujo_arc.md: reification: 22 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "weight came"; "the weight came"; "weight he carried"; "The weight pressed"; "the authority he car
- [prose] commencement_of_the_curia_kujo_arc.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] commencement_of_the_curia_kujo_arc.md: flat runs: 263 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "not just physically but" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "which was more graceful than the" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: antithesis 'not X but Y': "That is not cynicism, it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: countdown negation: "“Not enough to kill you. Not yet. Just enough that every promise starts costing something.”" (AI-tells §1)
- [prose] the_true_king_of_the_north_part_21.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_21.md: flat runs: 23 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_21.md: Kharven recurrence: 1 of the five signature items present (the death-house / the Waiting); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_9.md: em dashes: 2 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_9.md: reification: 3 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "silence followed"; "the grief came"; "Silence settled"
- [prose] the_true_king_of_the_north_part_9.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_9.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_9.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_1.md: antithesis 'not X but Y': "that was more interesting than handsome" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_1.md: reification: 4 unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "weight settled"; "the silence that followed"; "the moment arrived"; "The silence that followed"
- [prose] the_true_king_of_the_north_part_1.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_1.md: flat runs: 26 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_1.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_20.md: antithesis 'not X but Y': "it is not a virtue, it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_20.md: countdown negation: "It was not ceremonial. Not sovereign. Just Zuberi." (AI-tells §1)
- [prose] the_true_king_of_the_north_part_20.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_20.md: flat runs: 11 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_20.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_12.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_12.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_12.md: flat runs: 12 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_12.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_2.md: antithesis 'not X but Y': "It is not cruelty; it is" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_2.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_2.md: flat runs: 12 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_2.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_14.md: em dashes: 2 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_14.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_14.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_14.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_16.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_true_king_of_the_north_part_16.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_16.md: flat runs: 11 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_16.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_7.md: antithesis 'not X but Y': "not just as" (banned; AI-tells §1)
- [prose] the_true_king_of_the_north_part_7.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_7.md: flat runs: 20 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_true_king_of_the_north_part_7.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_true_king_of_the_north_part_3.md: reification: two in one paragraph (R4-15-ONE_PER_PARAGRAPH): "weight settled"; "weight always settled"
- [prose] the_true_king_of_the_north_part_3.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_true_king_of_the_north_part_3.md: flat runs: 14 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- ... and 71 more (reports/prose_pass.md, reports/reconcile.md)

## Cleared since last night

- none

## Still open: 255 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 3 push(es), 0 quiet run(s), 8 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-20.zip (24.0 MB, 1077 files)
- last run of this digest: 2026-09-22T05:35:29
