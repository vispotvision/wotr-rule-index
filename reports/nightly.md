# Nightly — 2026-09-16 03:30

## Overnight

Ten scenes archived since the last run and not one has a close; that is the morning's work, `/judger` on each, plus the 43 proposals already waiting on 08_sodoku_recalescence.
The book is the only thing actually stopped: chapter 1 is written and gated, and nothing more gets written until `python build/book_next.py --approve 1` or `--reject 1 --note "..."`.
All ten scenes fail the Kharven recurrence check, nine at zero of five signature items and What the Plate Would Not Take at one, the Thin Weeks.
All ten are Eresse and elven-arc scenes, so the check is firing off its own ground; I would scope R6-9 to Kharven POVs rather than bolt Kharven props onto elven scenes, but I have not touched it and it is yours to call.
Ruvaen Aloreth is POV of seven of the ten and still has no page.
Neither do Aeldros Korvaeth, Sennuvar Vhaeloth or Ithuran Melloran, nor Coldwater, Harrowbeck, Ollavaeth or Vaelmarr, and those four places carry the arc; nothing numeric or canonical about any of them should go on a page until they have one.
The 13 new findings are all prose and all inside these ten scenes. Only two are hard tells, both in The Kindling: seven em dashes, and "it was more a pressure than a sound".
The rest is chain-ceiling and flat-run work, a revision pass rather than a blocker.
Every one of the ten ran 3,100 to 4,300 words against the 700-1500 standard band. These are RP replies, not table scenes, so either they get verified at a band that fits or the length warning is noise from here on.
validate passes, the docket is clear, one conflict open, nothing cleared: 193 still standing, the 140 Büri-register hits among them.
Sync pushed 5 times with no failure lines. The newest backup zip is dated 09-14, so the last two nights did not write, and that is worth a look before anything else gets added to the vault.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 13 / CLEARED 0 / STILL OPEN 193

## Scenes archived since the last run

- `direction_is_not_intention` — run `/judger direction_is_not_intention` for the close
- `no_entry_for_that` — run `/judger no_entry_for_that` for the close
- `spent_not_dead` — run `/judger spent_not_dead` for the close
- `the_blackmatch` — run `/judger the_blackmatch` for the close
- `the_hand_of_the_empress` — run `/judger the_hand_of_the_empress` for the close
- `the_holy_inquisition_part_1_the_kindling` — run `/judger the_holy_inquisition_part_1_the_kindling` for the close
- `the_inhale_register` — run `/judger the_inhale_register` for the close
- `the_overpressure` — run `/judger the_overpressure` for the close
- `the_southern_passing` — run `/judger the_southern_passing` for the close
- `what_the_plate_would_not_take` — run `/judger what_the_plate_would_not_take` for the close

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- [prose] the_inhale_register.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_inhale_register.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] no_entry_for_that.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] no_entry_for_that.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_holy_inquisition_part_1_the_kindling.md: em dashes: 7 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_holy_inquisition_part_1_the_kindling.md: antithesis 'not X but Y': "it was more a pressure than a sound" (banned; AI-tells §1)
- [prose] the_blackmatch.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] what_the_plate_would_not_take.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] direction_is_not_intention.md: antithesis 'not X but Y': "That is not indifference to them, it is" (banned; AI-tells §1)
- [prose] the_hand_of_the_empress.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_southern_passing.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] spent_not_dead.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_overpressure.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)

## Cleared since last night

- none

## Still open: 193 (see reports/prose_pass.md, reports/reconcile.md; 19 files still carry Büri-register terms (140 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 5 push(es), 8 quiet run(s), 0 failure line(s)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-14.zip (23.7 MB, 1021 files)
- last run of this digest: 2026-09-15T14:34:41
