# Nightly — 2026-09-24 04:56

## Overnight

Quiet night. No scenes archived, so there is nothing new to verify. The 34 from last night still have no close, and none of them has reached the Judger queue.

The four new findings are the four cleared ones with the volume changed in the path. Azran, Cyrus and Khasir moved from Volumes V and VI into Volume I, still naming Phreatis · Fluxia against a Vitalia Family page. Nothing was fixed. The duplicate Continuity map went from two copies to ten. Still open reads 382 because last night's 131 rolled in; no prose pass ran against them.

Two book gates now instead of one. night-watch-zombification appears tonight at 3/80 with chapter 1 still undecided, so three chapters were written behind a gate you never answered. kharven-year sits where it was at 1/12. Both stop until you run --approve 1 or --reject 1.

The sync pushed 8 times and logged 20 failure lines, against 3 and 8 last night. It is still pushing, export still exits 1, and the failures are growing faster than the pushes. The backup line names the 09-20 zip again, four days old.

Validate passes, the docket is empty, the one conflict is still open, and the 43 proposals on 08_sodoku_recalescence have not moved. Nothing cleared that stayed cleared.

I would answer both gates first, drain the sodoku queue, then take the export exit 1 before it costs another night.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 4 / CLEARED 4 / STILL OPEN 382

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 3/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- [reconcile] Duplicate wiki pages (same title twice): Continuity map ×10
- [reconcile] Wellsprings named with a Family other than their own: Volume I — Character Cards/Azran Nemeir · The Gilded Draft.md: Phreatis · Fluxia (Family page says Vitalia)
- [reconcile] Wellsprings named with a Family other than their own: Volume I — Character Cards/Cyrus Vellhar · The Azure Warden.md: Phreatis · Fluxia (Family page says Vitalia)
- [reconcile] Wellsprings named with a Family other than their own: Volume I — Character Cards/Khasir Aluto · The Isocline Scribe.md: Phreatis · Fluxia (Family page says Vitalia)

## Cleared since last night

- [reconcile] Duplicate wiki pages (same title twice): Continuity map ×2
- [reconcile] Wellsprings named with a Family other than their own: Volume VI — Character Cards/Azran Nemeir · The Gilded Draft.md: Phreatis · Fluxia (Family page says Vitalia)
- [reconcile] Wellsprings named with a Family other than their own: Volume V — Character Cards/Cyrus Vellhar · The Azure Warden.md: Phreatis · Fluxia (Family page says Vitalia)
- [reconcile] Wellsprings named with a Family other than their own: Volume V — Character Cards/Khasir Aluto · The Isocline Scribe.md: Phreatis · Fluxia (Family page says Vitalia)

## Still open: 382 (see reports/prose_pass.md, reports/reconcile.md; 30 files still carry Büri-register terms (178 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 8 push(es), 0 quiet run(s), 20 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-20.zip (24.0 MB, 1077 files)
- last run of this digest: 2026-09-23T17:44:57
