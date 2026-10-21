# Nightly — 2026-10-21 03:40

## Overnight

Five scenes went into the archive since last night: The Truth of Muken, and The Uncounted, Chapters Nine to Twelve. Nothing else moved. Validate passes, the docket is empty, one conflict is still open, and the same four findings are still open: none new, none cleared.
The sync pushed 84 times with no failures. The weekly backup ran on Sunday 10-18 and is on schedule.
I couldn't check the five new scenes for names with no page or verify FAILs. The system `python` has no pyyaml, and running the venv interpreter needed an approval this run didn't have. Run `~/.venvs/wotr/bin/python build/book_tools.py verify scenes/<slug>.md --band standard` and `scene_context` on each one when you're up.
This morning both books are waiting on you at the chapter 1 gate: kharven-year and night-watch-zombification. Neither moves until you `--approve 1` or `--reject 1`. I'd read night-watch first, because ten chapters are already sitting behind its gate.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 0 / CLEARED 0 / STILL OPEN 4

## Scenes archived since the last run

- `the_truth_of_muken_20261020_2033`
- `the_uncounted_chapter_eleven_by_my_honour`
- `the_uncounted_chapter_nine_the_queens_will`
- `the_uncounted_chapter_ten_the_red_line`
- `the_uncounted_chapter_twelve_the_woodpile`

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

- sync: 84 push(es), 0 quiet run(s), 0 push failure(s)
- backup: weekly (Sunday 03:00), last 2026-10-18 (3 day(s) ago, on schedule): wrote /home/oridon/wotr-backups/wotr-2026-10-18.zip (38.1 MB, 1579 files)
- last run of this digest: 2026-10-20T03:30:00
