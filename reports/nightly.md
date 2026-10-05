# Nightly — 2026-10-05 03:30

## Overnight

Nothing moved in the index overnight: validate passes, the docket is clear, no findings new or cleared, the same 316 open and 42 conflicts still sitting.
No scenes were archived since the last run, so there was nothing to verify. The newest file in `scenes/` is still `the_drawing_off`, from the night before.
What wants you this morning is all decision and no work.
The Judger queue holds 93 proposals across three scenes: 43 on `08_sodoku_recalescence`, 29 on `01_wotr_muster_breach_road_north`, 21 on `04_sodoku_what_the_sky_does_not_ask`.
I would take Recalescence first. It is the largest, and nothing is waiting behind the other two.
Both books are stopped at the same gate, chapter 1 written and your call unmade, and nothing further is written for either until you answer.
That is two readings: `book/kharven-year/ch01/GATE.md` and `book/night-watch-zombification/ch01/GATE.md`, then approve or reject each. Eighty-one chapters of runway sit behind them.
The sync did not stop pushing. One Notion read timed out at 22:07, the hourly run after it went clean, and so did the five since, 677 pages unchanged each time.
Backup wrote `wotr-2026-10-04.zip`, 34.2 MB, 1171 files.
Nothing cleared.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 42
- findings NEW 0 / CLEARED 0 / STILL OPEN 316

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

- none

## Cleared since last night

- none

## Still open: 316 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 3 push(es), 19 quiet run(s), 1 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-04.zip (34.2 MB, 1171 files)
- last run of this digest: 2026-10-04T03:30:00
