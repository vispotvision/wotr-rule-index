# Nightly — 2026-10-17 03:30

## Overnight

Nothing needs you for the machine this morning: validate passes, the sync pushed three times with no failures, and the backup is on schedule (Sunday's zip, six days old). The docket is empty and one conflict is still open.
Four scenes landed: Hibiware, The Chains and the Arm, The Eight Calamities and The Septarch Wakes. All four verify clean, with no FAILs.
Names in them with no wiki page: Sonzai (all four; another creator's character, so that page is theirs to give), Kurosetsu (three), Naifuru and Kamigan (two each), and Malakar, Requiem, Fractura, Asante, Ashura and Verona. The Eight Calamities also names five with no page: Yasomagatsu, Nihiloth, Wazawai, Kegare and Midare. If those five are the Calamities themselves, they're the ones to page first, before anyone writes a number on them.
Four new reconcile findings, and two of them are real. "Continuity map ×43" is Notion-export cruft: the extra copies in The Scene Archive carry hash suffixes like "(3e458200)". I'd delete everything but the plain Continuity map.md. "The Veil ×2" is one page under Cosmology (The Making of the World) and one under The Disciplines/Spellcraft. They may be two different subjects with one title, so I'd rename the Spellcraft one rather than merge them. The other two "findings" are checks that came back "none" and are being counted as new. That's a digest bug, so the real NEW count is 2.
Both books are still stopped at chapter 1, waiting on your approve or reject (book/kharven-year/ch01/GATE.md, book/night-watch-zombification/ch01/GATE.md). Nothing cleared overnight.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 4 / CLEARED 0 / STILL OPEN 0

## Scenes archived since the last run

- `hibiware`
- `the_chains_and_the_arm`
- `the_eight_calamities`
- `the_septarch_wakes`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 10/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- [reconcile] Duplicate wiki pages (same title twice): The Veil ×2
- [reconcile] Duplicate wiki pages (same title twice): Continuity map ×43
- [reconcile] Card vs scene: Stage or Level stated differently: none found by pattern (Stage/Level within 80 characters of a first name)
- [reconcile] Wellsprings named with a Family other than their own: none

## Cleared since last night

- none

## Still open: 0 (see reports/reconcile.md)

## The sync (last 26 h) and the weekly backup

- sync: 3 push(es), 74 quiet run(s), 0 push failure(s)
- backup: weekly (Sunday 03:00), last 2026-10-11 (6 day(s) ago, on schedule): wrote /home/oridon/wotr-backups/wotr-2026-10-11.zip (34.6 MB, 1208 files)
- last run of this digest: never
