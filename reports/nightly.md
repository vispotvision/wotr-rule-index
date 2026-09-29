# Nightly — 2026-09-29 03:30

## Overnight

Seven scenes landed since last night and not one of them has a close yet. Four carry a FAIL: a single em dash each in `malphas_on_the_line_the_train_east`, `shioris_findings_aetherion_arena` and `wystans_briefing_aetherion_arena`, and three consecutive sentences over 25 words in `mu_jin_the_old_colleague`. `mu_jin_the_card`, `mu_jin_the_readers_oath` and `the_leveller` verify clean.

Those four FAILs are the four new findings, so nothing turned up overnight that the scenes did not bring in themselves. Nothing cleared: still 325 open, 40 conflicts, docket empty, validate PASS. The rest of the index sat still.

Names with no page, by how often they recur: Xhem in four of the seven scenes, Velder in three, Shiori and Zaire in two. Then Ossery Cut, Dunnock, Frithia, Kovu, Taesyn, and the whole of `the_leveller`'s cast: Haldor Ivor, Penn Lister, Thea, Willa, Southbank, Wellow, Chainsalt. Mortalis comes back with no page too, and it is a Wellspring rather than a person, so that one looks like a wiki mirror gap and not a naming gap. The bare "Madam", "Seol", "Penn", "Ivor" and "Lister" entries are the checker cutting one name into pieces.

What needs you: both books are stopped dead at the chapter-one gate, and nothing further is written until you answer, `python build/book_next.py --approve 1` or `--reject 1 --note "..."`, once for `kharven-year` and once for `night-watch-zombification`. Behind that, 93 Judger proposals wait across three scenes, 43 on `08_sodoku_recalescence`, 29 on `01_wotr_muster_breach_road_north`, 21 on `04_sodoku_what_the_sky_does_not_ask`. Sync pushed five times but logged seven failures, every one of them `export failed (exit 1)`, so the push leg is alive and the export leg is not. The backup line still names the 09-27 zip, which is a day behind.

In your place I would clear the two gates first, since everything downstream of them is idle, then fix the three em dashes and the one sentence chain, which are a character and a sentence of work, then take the Judger backlog oldest first and the seven new closes after it.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 40
- findings NEW 4 / CLEARED 0 / STILL OPEN 325

## Scenes archived since the last run

- `malphas_on_the_line_the_train_east` — run `/judger malphas_on_the_line_the_train_east` for the close
- `mu_jin_the_card` — run `/judger mu_jin_the_card` for the close
- `mu_jin_the_old_colleague` — run `/judger mu_jin_the_old_colleague` for the close
- `mu_jin_the_readers_oath` — run `/judger mu_jin_the_readers_oath` for the close
- `shioris_findings_aetherion_arena` — run `/judger shioris_findings_aetherion_arena` for the close
- `the_leveller` — run `/judger the_leveller` for the close
- `wystans_briefing_aetherion_arena` — run `/judger wystans_briefing_aetherion_arena` for the close

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

- [prose] mu_jin_the_old_colleague.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] malphas_on_the_line_the_train_east.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] wystans_briefing_aetherion_arena.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] shioris_findings_aetherion_arena.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)

## Cleared since last night

- none

## Still open: 325 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 5 push(es), 10 quiet run(s), 7 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-27.zip (33.4 MB, 1116 files)
- last run of this digest: 2026-09-28T03:30:00
