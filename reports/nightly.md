# Nightly — 2026-11-07 03:30

## Overnight

One scene went into the archive since last night, The Line Written (Naiser on the ridge above the Aerne mouth). Validate passes, no findings came or cleared, and the 3 open findings and 5 open conflicts are unchanged.
Verify gives it one FAIL, the new research line, and that FAIL is the gate misreading this check rather than a fault in the scene. The gate remembers lookups only inside the running process, so a fresh `wotr-mcp tool verify` has none to find. The prose checks came back 0 fail, 0 warn.
It will say the same about every scene this note checks from now on. I'd stop the gate firing on the `tool` route, the way it already stands down for quick lines, so a real FAIL can still be seen here.
Names with no page: Isaac, Measurewrights, Sengaki, Senri, Mimamori, Muen. Senri matters most, since Naiser's card leans on him as father and teacher, so I'd write his page first. Isaac is you, and I didn't look at where the scene names you.
What needs you this morning is the two books, and only if you want them moving. kharven-year (1/12) and night-watch-zombification (10/80) are both stopped at the chapter 1 gate, so `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."` on each starts them again.
The sync made 5 pushes with no failures, and the backup is on schedule (last 2026-11-01, next Sunday 03:00). Nothing cleared overnight.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 5
- findings NEW 0 / CLEARED 0 / STILL OPEN 3

## Scenes archived since the last run

- `the_line_written`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 10/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- none

## Still open: 3 (see reports/reconcile.md)

## The sync (last 26 h) and the weekly backup

- sync: 5 push(es), 101 quiet run(s), 0 push failure(s)
- backup: weekly (Sunday 03:00), last 2026-11-01 (6 day(s) ago, on schedule): wrote /home/oridon/wotr-backups/wotr-2026-11-01.zip (44.3 MB, 962 files)
- last run of this digest: 2026-11-06T03:30:00
