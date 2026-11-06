# Nightly — 2026-11-06 03:30

## Overnight

Nothing is broken this morning: validate passes, the sync made 31 pushes with no failures, and the backup is on schedule (Sunday's zip, 5 days old).
No scenes were archived since last night, so there are no missing-page names or FAIL lines to report.
It was a heavy canon day: 79 ruling commits, the wiki rewrite passes, the Outer World fold-in, and the R83-14 draw language taken out of the archived scenes, which is the one permitted edit to them.
What matters is that conflicts went from 1 to 5, all four new ones from that work. The count still includes the blank template at line 17 of CONFLICTS.md, so the real number is 4: C-166, C-177, C-179 and C-181.
C-179 and C-181 are marked open for you. C-166 is left for Natalie to rule as scenes touch it, and C-177 leaves card figures standing until it's settled.
On C-179 (battlefield rendering legal against the worst crime in every realm), I'd take R84-15, since the rule index outranks a wiki page, and narrow The Crossing's legal trade to bodies with no practitioner's Crystal cut out.
On C-181, I'd settle Muken first: R83-2 has him surviving and outranks Raizan's card, so the card is what changes. The rest are small mismatches, and scenes already hold for events.
On C-177, I'd keep the figures and move each listed card's Path line to Walked where the fighter really earned it, starting with Hayato, Kiyome and Raizan on Body.
The book gates still need you, same as yesterday: Kharven Year at 1 of 12 and Night Watch at 10 of 80, both waiting on chapter 1. I'd still start with Night Watch, which has nine more chapters stacked behind it: `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."`.
The one cleared finding isn't a real fix: the Wellspring Family check, which already read "none", is gone from the reconcile report. That takes findings from 4 to 3.
The reconcile report names The Veil ×2 and Continuity map ×43 as duplicate titles. No new findings, docket 0.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 5
- findings NEW 0 / CLEARED 1 / STILL OPEN 3

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 10/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `wotr-mcp book-next --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- [reconcile] Wellsprings named with a Family other than their own: none

## Still open: 3 (see reports/reconcile.md)

## The sync (last 26 h) and the weekly backup

- sync: 31 push(es), 83 quiet run(s), 0 push failure(s)
- backup: weekly (Sunday 03:00), last 2026-11-01 (5 day(s) ago, on schedule): wrote /home/oridon/wotr-backups/wotr-2026-11-01.zip (44.3 MB, 962 files)
- last run of this digest: 2026-11-05T03:30:01
