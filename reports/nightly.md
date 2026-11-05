# Nightly — 2026-11-05 03:30

## Overnight

Nothing is broken this morning: validate passes, the sync made 50 pushes with no failures, and the backup is on schedule (Sunday's zip, 4 days old).
Two scenes archived since last night, The Second Page and The White Knot. Both verify clean, 0 FAIL.
Names with no page, The Second Page: Hiromi, Itomi, Senna, Seisan, Dari, Kessen, Ketsumyōgan.
Names with no page, The White Knot: Itomi, Kessen, Senna, Hiromi, Cleave, Dari, Kamigan, Hazama, Shikii, Ketsumyōgan.
The tool also listed Isaac, Nothin and Begone; I left those off as not being in-world names. I'd card Senna, Hiromi and Dari first, since all three also run through Glass and Irons.
What needs you is the book gates. Kharven Year sits at 1 of 12 and Night Watch at 10 of 80, and the digest has both waiting on your chapter 1 answer.
I'd start with Night Watch: its chapter 1 gate reads PASS with 0 FAIL and 0 WARN, and nine more chapters are already stacked behind it. `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."`.
"Conflicts open 1" looks like a false count: the only `**Status:** open` line in CONFLICTS.md is the blank format template at line 17, so I'd fix the counter to skip it. It isn't a ruling you owe.
Nothing cleared and nothing new in the findings; the same 4 stay open in reports/reconcile.md, docket 0.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 0 / CLEARED 0 / STILL OPEN 4

## Scenes archived since the last run

- `the_second_page`
- `the_white_knot_20261104_1813`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 10/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- none

## Still open: 4 (see reports/reconcile.md)

## The sync (last 26 h) and the weekly backup

- sync: 50 push(es), 60 quiet run(s), 0 push failure(s)
- backup: weekly (Sunday 03:00), last 2026-11-01 (4 day(s) ago, on schedule): wrote /home/oridon/wotr-backups/wotr-2026-11-01.zip (44.3 MB, 962 files)
- last run of this digest: 2026-11-04T03:30:20
