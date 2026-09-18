# Nightly — 2026-09-18 03:30

## Overnight

Seventeen scenes archived since last night — the Kharven batch plus the inquisition part 1B, the turtle's boy, the years that were not war. None of them is closed; all seventeen want `/judger`.

Every one of the seventeen fails R6-9-RECURRENCE_RULE at 0 of 5 signature items, including `the_turtles_boy`, `the_years_that_were_not_war` and `the_holy_inquisition_part_1b`, which are not Kharven scenes at all. Seventeen for seventeen with no exception is the check firing on every scene, not seventeen prose failures — I'd read the rule's scene filter before anyone rewrites a line.

The 22 new findings are the usual three: chain ceiling, flat runs, and four 'not X but Y' — twice in `the_field_where_they_picked_them`, once each in `the_empty_place`, `the_terms`, `the_years_that_were_not_war`. `a_name_held_in_common` and `the_circus` carry no prose FAIL at all, only the recurrence line; those two close clean. Names with no page repeat hard across the batch: Rovann in 12 of 17, Xmere, Gorgi and Baraxes in 9 each, Aeldros Korvaeth and Ruvaen Aloreth just behind.

`scenes/the_holy_inquisition_part_1b_the_empty_chair.md` ends on "Verified: PASS, 0 fail, 3 warn" and scene_context now lists "Isaac" among its names with no page — a verifier report was saved into the scene body. That is a scene file, so it is your hand, not mine.

This morning: the 43 proposals on 08_sodoku_recalescence are still waiting and are older than everything above — clear those first, then run the seventeen closes in archive order. kharven-year chapter 1 is gated and nothing else in the book writes until `--approve 1` or `--reject 1`.

validate PASS, docket clear, one conflict open, nothing cleared out of 211. Sync pushed 5 times with 2 export failures, so it is still pushing. The backup is the one that stopped: newest zip is `wotr-2026-09-14.zip`, nothing written in the last 26 hours, four days cold.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 22 / CLEARED 0 / STILL OPEN 211

## Scenes archived since the last run

- `a_name_held_in_common` — run `/judger a_name_held_in_common` for the close
- `on_foot` — run `/judger on_foot` for the close
- `the_brink` — run `/judger the_brink` for the close
- `the_circus` — run `/judger the_circus` for the close
- `the_draught` — run `/judger the_draught` for the close
- `the_empty_place` — run `/judger the_empty_place` for the close
- `the_field_where_they_picked_them` — run `/judger the_field_where_they_picked_them` for the close
- `the_full_match` — run `/judger the_full_match` for the close
- `the_holy_inquisition_part_1b_the_empty_chair` — run `/judger the_holy_inquisition_part_1b_the_empty_chair` for the close
- `the_slow_match` — run `/judger the_slow_match` for the close
- `the_terms` — run `/judger the_terms` for the close
- `the_turtles_boy` — run `/judger the_turtles_boy` for the close
- `the_vey_elarin` — run `/judger the_vey_elarin` for the close
- `the_years_that_were_not_war` — run `/judger the_years_that_were_not_war` for the close
- `what_he_spent` — run `/judger what_he_spent` for the close
- `what_motion_cannot_reach` — run `/judger what_motion_cannot_reach` for the close
- `what_we_did_not_do` — run `/judger what_we_did_not_do` for the close

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- [prose] the_field_where_they_picked_them.md: antithesis 'not X but Y': "it was not a request and it was not a curse, it was" (banned; AI-tells §1)
- [prose] the_field_where_they_picked_them.md: antithesis 'not X but Y': "It is not a technique, it is" (banned; AI-tells §1)
- [prose] the_field_where_they_picked_them.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_field_where_they_picked_them.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_years_that_were_not_war.md: antithesis 'not X but Y': "not merely follow the causal web but" (banned; AI-tells §1)
- [prose] the_years_that_were_not_war.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_years_that_were_not_war.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_empty_place.md: antithesis 'not X but Y': "it is not mercy, it is" (banned; AI-tells §1)
- [prose] the_empty_place.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_empty_place.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_turtles_boy.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_turtles_boy.md: flat runs: 10 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_draught.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] what_motion_cannot_reach.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_full_match.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_brink.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_slow_match.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_terms.md: antithesis 'not X but Y': "which is more levy than he" (banned; AI-tells §1)
- [prose] the_vey_elarin.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] on_foot.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] what_he_spent.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] what_we_did_not_do.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)

## Cleared since last night

- none

## Still open: 211 (see reports/prose_pass.md, reports/reconcile.md; 19 files still carry Büri-register terms (140 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 5 push(es), 20 quiet run(s), 2 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-14.zip (23.7 MB, 1021 files)
- last run of this digest: 2026-09-17T03:30:18
