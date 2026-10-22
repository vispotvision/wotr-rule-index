# Nightly — 2026-10-22 03:30

## Overnight

Quiet night for the rules: validate passes, docket empty, one conflict open, the same four findings, nothing new archived, backup on schedule from Sunday.

The sync needs you this morning. Its 34 "push failures" are really commit failures: build/sync.sh line 114 still stages scenes/CAST.md and scenes/TIMELINE.md, and the 10-18 lore reset moved both to lore/v1/scenes/. Git refuses the whole add over the missing path, so wiki and table edits have not been committed since then (wiki/INDEX.md is sitting modified right now). The branch is level with origin, so nothing is lost, only stuck. I'd change that line to `lore/v1/scenes/CAST.md lore/v1/scenes/TIMELINE.md` and let the next quarter-hour run carry it up.

Both books are still parked on chapter 1 gates waiting for your approve or reject.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 0 / CLEARED 0 / STILL OPEN 4

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 10/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- none

## Still open: 4 (see reports/reconcile.md)

## The sync (last 26 h) and the weekly backup

- sync: 40 push(es), 0 quiet run(s), 34 push failure(s): push failed
- backup: weekly (Sunday 03:00), last 2026-10-18 (4 day(s) ago, on schedule): wrote /home/oridon/wotr-backups/wotr-2026-10-18.zip (38.1 MB, 1579 files)
- last run of this digest: 2026-10-21T03:40:50
