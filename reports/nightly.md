# Nightly — 2026-10-14 03:30

## Overnight

Two scenes landed overnight, `lions_bane` and `the_last_quiet_room`. Neither has a verify FAIL, and both need `/judger` for the close.
ChatGPT flags `lions_bane` as major under R77-2: the combat RP spells out how the summoning and Cleave work ("The room paid for the body of the summons..."; the glyph and magnetostriction lessons). Move those into the author notes and leave only the tells and the body's cost on the page. It also catches a past-tense RP line (R49-02) and ECHO's "three calls a day", where the card actually says "about three times its first strength".
Kain's numbers couldn't be checked, because the lookup returns Azelra Kaine. `lions_bane` also names Kain, Judicium, Anamnesis, Vocatia, Animatria, Maelor and Fulguria with no page. Give Kain a roster entry before he gets a number. `the_last_quiet_room` has no unpaged names.
Both scenes say the masked boy's duel was six days ago. Hiromi's card and TIMELINE row 143 say seven. I'd make it seven in both scenes during the close.
The three judger queues are still sitting there (29, 21 and 43 proposals), and both books are still stuck at chapter 1 waiting on your approve or reject.
Validate passes, the docket is empty and one conflict is open. The "new" and "cleared" findings are just CONTINUITY.md recounting itself (em dashes went from 276 to 290), so nothing really cleared.
The sync pushed twice but logged two "export failed (exit 1)" lines, so it's worth a look if it keeps happening. The newest backup listed is dated 10-11.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 3 / CLEARED 3 / STILL OPEN 336

## Scenes archived since the last run

- `lions_bane` — run `/judger lions_bane` for the close
- `the_last_quiet_room` — run `/judger the_last_quiet_room` for the close

## ChatGPT review

- `lions_bane`: major: Move the summoning and Cleave mechanisms out of the combat RP and into author notes.  (reports/reviews/2026-10-14/lions_bane.md)
- `the_last_quiet_room`: minor: Correct the duel-to-tournament interval from six days to seven.  (reports/reviews/2026-10-14/the_last_quiet_room.md)

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

- [prose] CONTINUITY.md: em dashes: 290 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] CONTINUITY.md: flat runs: 51 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] CONTINUITY.md: sentences under 8 words: 8% of scene, floor is 18% (R4-14-HARD_CEILINGS)

## Cleared since last night

- [prose] CONTINUITY.md: em dashes: 276 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] CONTINUITY.md: flat runs: 49 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] CONTINUITY.md: sentences under 8 words: 9% of scene, floor is 18% (R4-14-HARD_CEILINGS)

## Still open: 336 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (178 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 2 push(es), 16 quiet run(s), 2 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-11.zip (34.6 MB, 1208 files)
- last run of this digest: 2026-10-13T03:30:00
