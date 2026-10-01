# Nightly — 2026-10-01 03:30

## Overnight

Second still day. No scenes archived, nothing new or cleared, docket empty, validate PASS, conflicts still 40, and the Judger queue is the same three at 93 proposals. Nothing moved on its own and nothing broke.

The export leg came back. It timed out reading Notion at 01:00 and 03:00 on the 30th, the same read timeout as the three nights before it, but both runs this morning finished clean on 677 pages with nothing changed. One failure line in the window instead of six. Transient, and I would leave it alone now.

What needs you, in order. Both book gates, a third night stopped: `python build/book_next.py --approve 1` for `kharven-year`, then again for `night-watch-zombification`, or `--reject 1 --note "..."`. Nothing is written behind either until you answer. Then `/judger` on the three closes, oldest first; `08_sodoku_recalescence` holds 43 of the 93.

Two want your hands and nobody else's. `scenes/YOKO_MISHIRO.md` is skipped on every publish because its Notion parent is not shared with the integration, and the backup line still names the 09-27 zip, four nights old.

Still unfixed from the 29th, and CLEARED 0 says nobody went near them: one em dash each in `malphas_on_the_line_the_train_east`, `shioris_findings_aetherion_arena` and `wystans_briefing_aetherion_arena`, and three consecutive sentences over 25 words in `mu_jin_the_old_colleague`. Three characters and one sentence of work.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 40
- findings NEW 0 / CLEARED 0 / STILL OPEN 329

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

## Still open: 329 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 0 push(es), 5 quiet run(s), 1 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-27.zip (33.4 MB, 1116 files)
- last run of this digest: 2026-09-30T03:30:00
