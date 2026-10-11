# Nightly — 2026-10-11 03:30

## Overnight

Quiet night. No scenes were archived and ChatGPT had nothing to review. Validate passes, the docket is empty, and conflicts hold at 42.
The only finding movement is CONTINUITY.md getting longer: em dashes went from 265 to 267 and flat runs from 46 to 49. That's the old file growing, not new prose breaking rules, so it doesn't matter this morning.
The sync timed out talking to Notion three times yesterday (10:09, 20:07, 22:07). It recovered: the 03:20 run was clean with no wiki changes, and the last push was 17:25. Nothing to fix.
One file keeps getting skipped on publish: scenes/YOKO_MISHIRO.md, because its Notion parent isn't shared with the integration. Share that page with the integration once and it'll go up on the next run.
What needs you: three Judger closes are waiting, 93 proposals in all (recalescence 43, muster breach 29, what the sky does not ask 21). I'd start with recalescence because it's the biggest. Both books are stopped at the chapter 1 gate. kharven-year is the quicker call: approve or reject it with `python build/book_next.py --approve 1`.
Backup wrote 34.6 MB.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 42
- findings NEW 3 / CLEARED 3 / STILL OPEN 328

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

- [prose] CONTINUITY.md: em dashes: 267 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] CONTINUITY.md: flat runs: 49 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] CONTINUITY.md: sentences under 8 words: 8% of scene, floor is 18% (R4-14-HARD_CEILINGS)

## Cleared since last night

- [prose] CONTINUITY.md: em dashes: 265 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] CONTINUITY.md: flat runs: 46 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] CONTINUITY.md: sentences under 8 words: 9% of scene, floor is 18% (R4-14-HARD_CEILINGS)

## Still open: 328 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (178 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 3 push(es), 19 quiet run(s), 5 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-11.zip (34.6 MB, 1208 files)
- last run of this digest: 2026-10-10T03:30:00
