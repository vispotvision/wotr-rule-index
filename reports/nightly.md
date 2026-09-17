# Nightly — 2026-09-17 03:30

## Overnight

Three scenes landed and none has a close: `in_form`, `nine_hours_of_daylight`, `the_hatch`.
All three break the chain ceiling; `in_form` carries 4 flat runs and `nine_hours_of_daylight` 6.
All three also sit under the Kharven recurrence minimum — `the_hatch` has none of the five — but so does most of the corpus in `reports/recurrence.md`, so that is the standing state, not a break that happened last night.

Every one of the three names Ruvaen Aloreth, and he has no page. He is the POV of all three, so I would put his card up before running any close; Velthaeir, Gorgi and Xmere have no page in all three either.
Thirteen more have none across the set: Harrowbeck, Coldwater, Landward Wall, Hesh Orovain, Neyra Corvenn, Reckoner, Hales, Measurewright, Vaelmarr, Velenn Ithalan, Dova, Rovann, Drow.

"conflicts open 1" is the counter, not a conflict. `build/nightly.py:83` matches the `**Status:** open` line inside the format template at the top of `CONFLICTS.md`; C-001 through C-019 are all closed and nothing waits on a ruling.
That is one regex, but it is the checker, so I have left it for you.

The sync pushed twice and failed one export (exit 1) — the line is in `journalctl --user -u wotr-sync`; it is still pushing, so this is one run, not a stoppage.
Still yours from before: the 43 proposals on `08_sodoku_recalescence`, and chapter 1's gate — nothing more of the book is written until `--approve 1` or `--reject 1`.
validate PASS, docket empty, nothing cleared, 206 still open; the backup is on its Sunday cycle and next runs 09-20.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 5 / CLEARED 0 / STILL OPEN 206

## Scenes archived since the last run

- `in_form` — run `/judger in_form` for the close
- `nine_hours_of_daylight` — run `/judger nine_hours_of_daylight` for the close
- `the_hatch` — run `/judger the_hatch` for the close

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- [prose] in_form.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] in_form.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] nine_hours_of_daylight.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] nine_hours_of_daylight.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_hatch.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)

## Cleared since last night

- none

## Still open: 206 (see reports/prose_pass.md, reports/reconcile.md; 19 files still carry Büri-register terms (140 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 2 push(es), 22 quiet run(s), 1 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-14.zip (23.7 MB, 1021 files)
- last run of this digest: 2026-09-16T03:30:17
