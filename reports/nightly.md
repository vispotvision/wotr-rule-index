# Nightly — 2026-10-13 03:30

## Overnight

Four Naori-versus-Verona arena posts were archived yesterday (Middle of the Thread, Rewinding the Spool, Covenant of the Instant, Returning Water). None is closed yet, so run `/judger` on each.
ChatGPT marked three of them major. In Covenant, Naori's card puts him at Stage III, but the Covenant needs Refraction or higher. In Rewinding and Returning Water, the post explains how the reversal, the feint and the counter work, which hands Verona the answer (R77-2). The fix is to move those explanations into the author notes and leave only the tells and what it costs his body on the page.
The real problem sits under all four: his card still says "no combat training, no techniques, no weapons", while the posts give him childhood sword drilling and named arts. I'd update the card to a tournament loadout before the close, not argue it scene by scene.
Each scene fails verify on one em dash and nothing else. Those four em dashes are four of the five new findings. The fifth is CONTINUITY.md going from 271 to 276 em dashes, so nothing actually cleared.
No page exists for Verona, who is the opponent in all four and has no card, so her 600 EU can't be checked. The same goes for Inzensho, Cymorath, Threadburn, Exuroth, Lethegraal, Senri, Hanuri and Sōma, and for the technique names (Uragaeshi, Kaeri, Kussetsu, Makimodoshi, Awai). I'd card Verona first.
Still waiting on you: 93 Judger proposals across three older scenes, and both books are stopped at their chapter 1 gate.
Validate passes and the docket is empty. The sync pushed twice but logged three "export failed" lines, so check the Notion export before trusting it. The newest backup is still the 10-11 zip, which means the backup didn't run last night.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 42
- findings NEW 5 / CLEARED 1 / STILL OPEN 334

## Scenes archived since the last run

- `covenant_of_the_instant_aetherion_arena` — run `/judger covenant_of_the_instant_aetherion_arena` for the close
- `returning_water_aetherion_arena` — run `/judger returning_water_aetherion_arena` for the close
- `rewinding_the_spool_aetherion_arena` — run `/judger rewinding_the_spool_aetherion_arena` for the close
- `the_middle_of_the_thread_senris_gate_and_the_aetherion_arena` — run `/judger the_middle_of_the_thread_senris_gate_and_the_aetherion_arena` for the close

## ChatGPT review

- `covenant_of_the_instant_aetherion_arena`: major: Reconcile Naori’s Stage III card with the Covenant’s Refraction minimum before treating this exchange as canon.  (reports/reviews/2026-10-13/covenant_of_the_instant_aetherion_arena.md)
- `returning_water_aetherion_arena`: major: Move the combat mechanisms out of the RP prose and into the notes; retain observable effects, tells and bodily cost.  (reports/reviews/2026-10-13/returning_water_aetherion_arena.md)
- `rewinding_the_spool_aetherion_arena`: major: Move the reversal, aura and feint mechanisms into author notes; this combat RP post discloses how to counter Naori.  (reports/reviews/2026-10-13/rewinding_the_spool_aetherion_arena.md)
- `the_middle_of_the_thread_senris_gate_and_the_aetherion_arena`: minor: Track the two wooden swords correctly through the lesson and hand-back.  (reports/reviews/2026-10-13/the_middle_of_the_thread_senris_gate_and_the_aetherion_arena.md)

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

- [prose] CONTINUITY.md: em dashes: 276 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] returning_water_aetherion_arena.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] rewinding_the_spool_aetherion_arena.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] covenant_of_the_instant_aetherion_arena.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_middle_of_the_thread_senris_gate_and_the_aetherion_arena.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)

## Cleared since last night

- [prose] CONTINUITY.md: em dashes: 271 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)

## Still open: 334 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (178 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 2 push(es), 21 quiet run(s), 3 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-11.zip (34.6 MB, 1208 files)
- last run of this digest: 2026-10-12T03:30:00
