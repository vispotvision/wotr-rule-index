# Nightly — 2026-10-09 03:30

## Overnight

Two Aetherion scenes came in overnight. Validate passes, the docket is empty, and 42 conflicts are still open. Both scenes need a fix before you run `/judger` on them.
The Medlar Tree: ChatGPT rates it major. Madeleine Ault's voice is credited to Draycott and Strom, but Furveus sealed her commission, and her attempt is mixed up with the 694 Necrocursica commission. Its arithmetic also says Malphas could raise "about eleven thousand", when Starvation starts at about 10,316. I'd put Furveus back as her maker and change the count to "ten thousand" before closing it.
The Stands Before the Bell: ChatGPT rates it major. The point of view drifts into Kaiyo's head and Lance's. Kaiyo has no card, so they can't hold a section. Neraveth is called "he" but she is Naori's sister. Yoko's ears are red-gold but her card says ash-grey. The notes say Dabney has no card, and he does. I'd fix the pronouns and the ears first, then cut the Kaiyo section down to what Rikudoku can see.
verify: each scene has one FAIL, the same one: a single em dash, nothing else. Medlar is also 6,300 words, over the standard band.
Names with no page. Medlar: Aegon, Nuvilak, Genesio, Draycott, Gisli Draycott, Maren, Strom, Madeleine Ault, Greyshaft, Nihiloth, Mortalis, Necrocursica. The last three are terms, not people, and their pages need aliases. Stands: Kaiyo, Mira, Taesyn, Neraveth, Whitemere, Sonzai, Xhem. Sonzai and Xhem are other creators' characters, so leave them without pages. Ignore "Natalie": it only matches the author notes.
Still waiting on you: the Judger queue has 93 proposals across three scenes (08_sodoku_recalescence alone has 43). Both books are stuck at the chapter 1 gate.
Sync: Notion publishing timed out once at 22:39. Git kept pushing and the 03:19 run was clean, apart from scenes/YOKO_MISHIRO.md, whose Notion parent isn't shared with the integration. Share that page when you're next in Notion. The backup is weekly and the last one was 10-04, so it's on schedule.
Cleared: nothing real. The only "cleared" lines are CONTINUITY.md's own em-dash and short-sentence counts going up by two and one point.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 42
- findings NEW 4 / CLEARED 2 / STILL OPEN 327

## Scenes archived since the last run

- `the_medlar_tree_aetherion_academy` — run `/judger the_medlar_tree_aetherion_academy` for the close
- `the_stands_before_the_bell_aetherion_arena` — run `/judger the_stands_before_the_bell_aetherion_arena` for the close

## ChatGPT review

- `the_medlar_tree_aetherion_academy`: major: Restore Furveus as Madeleine Ault’s maker and separate her commission from the earlier Necrocursica commission.  (reports/reviews/2026-10-09/the_medlar_tree_aetherion_academy.md)
- `the_stands_before_the_bell_aetherion_arena`: major: Restore one viewpoint per section; the breaks do not prevent access to other characters’ private thoughts.  (reports/reviews/2026-10-09/the_stands_before_the_bell_aetherion_arena.md)

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

- [prose] CONTINUITY.md: em dashes: 265 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] CONTINUITY.md: sentences under 8 words: 9% of scene, floor is 18% (R4-14-HARD_CEILINGS)
- [prose] the_stands_before_the_bell_aetherion_arena.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_medlar_tree_aetherion_academy.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)

## Cleared since last night

- [prose] CONTINUITY.md: em dashes: 263 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] CONTINUITY.md: sentences under 8 words: 8% of scene, floor is 18% (R4-14-HARD_CEILINGS)

## Still open: 327 (see reports/prose_pass.md, reports/reconcile.md; 29 files still carry Büri-register terms (178 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 5 push(es), 17 quiet run(s), 5 failure line(s):  publish failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-10-04.zip (34.2 MB, 1171 files)
- last run of this digest: 2026-10-08T03:30:00
