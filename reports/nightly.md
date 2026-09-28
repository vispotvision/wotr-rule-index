# Nightly — 2026-09-28 03:30

## Overnight

Twenty-one scenes archived since last night: the Geturo and Hiromi Arena run, the five Rovhen pieces, Mujin's
interjection, xanelor_dallae. Thirteen fail verify, most of it small, one em dash each in nine and flat runs
in six. Two want real work: mujins_interjection carries nine em dashes and a chain of three sentences over
25 words, and geturo_the_host_line has that chain fault plus six flat runs.
The Rovhen thread has no cards at all: Edmund Lambert, Agnes Tull, the Alderys, Imogen Pell, Tobin Sallow,
Pryor, Crale and Harrowgate itself all come back with no page, so nothing numeric goes on them yet. Taesyn
is unpaged across six Geturo scenes; Dallae, Zaire, Shiori and the alchemy operation names the same.
This morning: 93 Judger proposals on three scenes, 43 on recalescence alone, the 21 above still needing
/judger, and both books stopped on an unanswered chapter-one gate, night-watch ten chapters deep behind it.
Nothing cleared. 307 findings open, the Büri sweep unmoved at 29 files and 177 hits, validate passing, docket
empty, sync pushing four times through three Notion read timeouts. The one conflict counted open is the
format example in the CONFLICTS.md header, not a live row; the counter should skip the fenced block.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 18 / CLEARED 0 / STILL OPEN 307

## Scenes archived since the last run

- `aftermath_hold_the_wall` — run `/judger aftermath_hold_the_wall` for the close
- `geturo_constrictor` — run `/judger geturo_constrictor` for the close
- `geturo_fire_air` — run `/judger geturo_fire_air` for the close
- `geturo_gypsum` — run `/judger geturo_gypsum` for the close
- `geturo_ignite_tide` — run `/judger geturo_ignite_tide` for the close
- `geturo_the_elbow` — run `/judger geturo_the_elbow` for the close
- `geturo_the_host_line` — run `/judger geturo_the_host_line` for the close
- `geturo_the_other_side` — run `/judger geturo_the_other_side` for the close
- `geturo_the_slip` — run `/judger geturo_the_slip` for the close
- `geturo_the_squeeze` — run `/judger geturo_the_squeeze` for the close
- `geturo_whos_next` — run `/judger geturo_whos_next` for the close
- `hiromi_something_special` — run `/judger hiromi_something_special` for the close
- `hiromi_the_bench` — run `/judger hiromi_the_bench` for the close
- `hiromi_the_picnic` — run `/judger hiromi_the_picnic` for the close
- `mujins_interjection_aetherion_arena` — run `/judger mujins_interjection_aetherion_arena` for the close
- `rovhen_after_the_lecture` — run `/judger rovhen_after_the_lecture` for the close
- `rovhen_the_dispensary` — run `/judger rovhen_the_dispensary` for the close
- `rovhen_the_first_lecture` — run `/judger rovhen_the_first_lecture` for the close
- `rovhen_the_letter` — run `/judger rovhen_the_letter` for the close
- `rovhen_the_sort` — run `/judger rovhen_the_sort` for the close
- `xanelor_dallae` — run `/judger xanelor_dallae` for the close

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

- [prose] geturo_ignite_tide.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] geturo_ignite_tide.md: countdown negation: "No numbers in prose. Never written: no thought, action or reaction. Only the light bending off him and the fifth band reaching his boots." (AI-tells §1)
- [prose] geturo_the_host_line.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] geturo_the_host_line.md: flat runs: 6 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] mujins_interjection_aetherion_arena.md: em dashes: 9 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] mujins_interjection_aetherion_arena.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] rovhen_the_dispensary.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] rovhen_the_dispensary.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] rovhen_the_first_lecture.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] rovhen_the_first_lecture.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] rovhen_the_sort.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] rovhen_after_the_lecture.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] rovhen_the_letter.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] hiromi_the_picnic.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] xanelor_dallae.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] geturo_fire_air.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] geturo_gypsum.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] geturo_whos_next.md: flat runs: 4 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)

## Cleared since last night

- none

## Still open: 307 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (177 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 4 push(es), 19 quiet run(s), 3 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-27.zip (33.4 MB, 1116 files)
- last run of this digest: 2026-09-27T03:30:14
