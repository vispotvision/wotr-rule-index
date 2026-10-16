# Nightly — 2026-10-16 03:30

## Overnight

Quiet night. Validate passes, the docket is empty, one conflict is still open, and no scenes were archived, so there was nothing new to check.
The one real change: CONTINUITY.md went from 295 em dashes to 305. That means something wrote ten more into it yesterday. It's a scenes index, not prose, so it doesn't matter for the table, but whatever writes it is still putting them in.
Cleared: the three cards (Azran Nemeir, Cyrus Vellhar, Khasir Aluto) that put Phreatis under Fluxia no longer show the mismatch.
What needs you this morning, in this order. First, the sync: 5 push failures in the last 26 hours, and one commit is still sitting local. I'd run `git status` and `git push` by hand and see what it says before the wiki drifts further from the site.
Second, the Judger queue: 93 proposals across three scenes. Recalescence is the biggest at 43, so I'd start with `/judger 08_sodoku_recalescence`.
Third, both books are stopped at their chapter 1 gate, kharven-year and night-watch-zombification. Nothing more gets written on either until you approve or reject.
The backup line still points at the 10-11 zip. If it's meant to run nightly, it hasn't run for five days.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 2 / CLEARED 4 / STILL OPEN 335

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

- [prose] CONTINUITY.md: em dashes: 305 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [reconcile] Wellsprings named with a Family other than their own: none

## Cleared since last night

- [prose] CONTINUITY.md: em dashes: 295 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [reconcile] Wellsprings named with a Family other than their own: Volume I — Character Cards/Azran Nemeir · The Gilded Draft.md: Phreatis · Fluxia (Family page says Vitalia)
- [reconcile] Wellsprings named with a Family other than their own: Volume I — Character Cards/Cyrus Vellhar · The Azure Warden.md: Phreatis · Fluxia (Family page says Vitalia)
- [reconcile] Wellsprings named with a Family other than their own: Volume I — Character Cards/Khasir Aluto · The Isocline Scribe.md: Phreatis · Fluxia (Family page says Vitalia)

## Still open: 335 (see reports/prose_pass.md, reports/reconcile.md; 40 files still carry Büri-register terms (312 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 6 push(es), 31 quiet run(s), 5 failure line(s):  push failed (1 earlier commit(s) still local)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-11.zip (34.6 MB, 1208 files)
- last run of this digest: 2026-10-15T03:30:00
