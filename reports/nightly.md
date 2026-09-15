# Nightly — 2026-09-15 14:34

## Overnight

Nothing in the index moved: validate passes, docket clear, one conflict open, the same 193 findings, none new, none cleared. No scene was archived, so there was nothing to verify. The three check reports changed only their run date.

The machine was off from about 20:00 last night until 14:33 today, so the 03:30 digest and the 02:00 book dispatch both fired at boot instead. The digest's git pull failed a minute after boot (no network yet); local and origin are level, nothing was lost.

The Notion sync is fixed. The new token worked from 04:03 yesterday morning, and every hourly run since read all 586 pages, found nothing changed and pushed nothing — quiet, not broken. It stopped at 20:04 because the machine did; look for a 15:00 line in build/sync.log to see it resume (the timer check itself was refused here). One page still never publishes: scenes/YOKO_MISHIRO.md, because its parent page is not shared with the integration — one Share click in Notion.

Drive is still unwired: no rclone, WOTR_DRIVE unset, so backups stay on this disk and the sync skips the docs step. The newest copy off this machine is still 09-13 on Google Drive. The next backup is Sunday 09-20 at 03:00; the 09-14 zip was a proof run, not a miss. rclone is a sudo step, so it is yours.

Waiting on you, unchanged: the 43 Judger proposals for 08_sodoku_recalescence (`/judger apply 08_sodoku_recalescence ...`), and chapter 1 of kharven-year at its gate — `python build/book_next.py --approve 1` or `--reject 1 --note "..."`; nothing more gets written until you answer.

Nothing cleared.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 0 / CLEARED 0 / STILL OPEN 193

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- none

## Still open: 193 (see reports/prose_pass.md, reports/reconcile.md; 19 files still carry Büri-register terms (140 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 0 push(es), 8 quiet run(s), 0 failure line(s)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-14.zip (23.7 MB, 1021 files)
- last run of this digest: 2026-09-14T03:30:01
