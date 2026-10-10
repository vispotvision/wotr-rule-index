# Nightly — 2026-10-10 03:30

## Overnight

Quiet night. No scenes were archived, so there was no ChatGPT review and nothing to verify. Validate passes, the docket is empty, and no findings were added or cleared (331 still open, 42 conflicts).
What needs you this morning:
- Two sync runs logged "export failed (exit 1)". One push still went through, so it hasn't stopped. If tonight's line still shows the failures, check the sync unit's journal.
- The backup line still names wotr-2026-10-04.zip, so no new backup has been written in six days. Check the backup timer. I couldn't see the backups folder from here.
- 93 Judger proposals are waiting across three scenes (Muster Breach 29, What the Sky Does Not Ask 21, Recalescence 43). I'd clear Recalescence first because it has the most.
- Both books are stuck at the chapter 1 gate (kharven-year, night-watch-zombification). Nothing more gets written until you approve or reject chapter 1.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 42
- findings NEW 0 / CLEARED 0 / STILL OPEN 331

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

## Still open: 331 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (178 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 1 push(es), 20 quiet run(s), 2 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-04.zip (34.2 MB, 1171 files)
- last run of this digest: 2026-10-09T03:30:00
