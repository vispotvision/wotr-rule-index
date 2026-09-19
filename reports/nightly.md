# Nightly — 2026-09-19 03:30

## Overnight

Ten scenes landed since last night: the five War in the North parts, the four Xanelor classroom scenes, and the Great Summoner's Morning. None has a close, so that is ten `/judger` runs, and it is the only work this morning that needs your hands.

Nine of the ten fail on one em dash each. Only the Great Summoner's Morning is clean of it. One character per file, cheapest thing on the list.

Heavier: Part I fails the chain ceiling and eight flat runs, Xanelor First Bell fails the chain ceiling and five flat runs, Part II five flat runs. Those are rewrites, not fixes.

The Kharven recurrence check fails on all ten, including the four Xanelor scenes and the Aetherion one, which stand on no Kharven ground. The nightly counts it against Parts II and V only. I read the other eight as the checker's scope rather than a prose debt, and II and V as the real misses.

Names with no page, which block anything numeric or canonical about them: Brackenhold, Foss, Mell, Rannvei (I); Zuberi, Asante, Kujo (II); Emira, Sonzai (III); Marten Hillborn (IV); Josse Hillborn, Ridgewall (V); Frithia, Verona, Taesyn, Zaire, Drogo, Neraveth, Omoro (Xanelor); Aetherion Academy.

Wren has no page either, and he carries a Front sitting at 0 of 4. Emira and Verona now carry scenes with nothing behind them. Those three are the stubs I would write first.

Stale Büri-register terms still stand in three files: Part I (Muken Büri ×2, Büri ×4), Part IV (Möngön ×5, Büri ×4), Part V (Möngön ×1). R19-2 permits the silent correction to Moto and Shirogane. I have not touched them.

Every one of these files ends on its author-note tail, so verify is reading the notes as prose. That is why the last-line check reports a rules list, and why Part II's context lists "Isaac" as a name with no page.

08_sodoku_recalescence still has 43 proposals waiting on you.

Book kharven-year is stopped at the chapter 1 gate. Nothing more is written until `python build/book_next.py --approve 1` or `--reject 1 --note "..."`.

validate PASS, docket 0, one conflict open, 233 findings still open, nothing cleared. Sync pushed six times with no failures. The backup line still points at the 09-14 zip, five days old, so that job has not run.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 22 / CLEARED 0 / STILL OPEN 233

## Scenes archived since the last run

- `the_great_summoners_morning` — run `/judger the_great_summoners_morning` for the close
- `the_war_in_the_north_i_the_kharven_seat` — run `/judger the_war_in_the_north_i_the_kharven_seat` for the close
- `the_war_in_the_north_ii_the_road_two_days_south` — run `/judger the_war_in_the_north_ii_the_road_two_days_south` for the close
- `the_war_in_the_north_iii_utopia` — run `/judger the_war_in_the_north_iii_utopia` for the close
- `the_war_in_the_north_iv_the_blank_seal` — run `/judger the_war_in_the_north_iv_the_blank_seal` for the close
- `the_war_in_the_north_v_the_shieldwarden` — run `/judger the_war_in_the_north_v_the_shieldwarden` for the close
- `xanelor_after_the_crash` — run `/judger xanelor_after_the_crash` for the close
- `xanelor_rikudoku_and_the_address` — run `/judger xanelor_rikudoku_and_the_address` for the close
- `xanelor_the_introductions` — run `/judger xanelor_the_introductions` for the close
- `xanelor_the_morning_of_the_first_bell` — run `/judger xanelor_the_morning_of_the_first_bell` for the close

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- [prose] the_war_in_the_north_i_the_kharven_seat.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_war_in_the_north_i_the_kharven_seat.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_war_in_the_north_i_the_kharven_seat.md: flat runs: 8 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_war_in_the_north_ii_the_road_two_days_south.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_war_in_the_north_ii_the_road_two_days_south.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_war_in_the_north_ii_the_road_two_days_south.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] xanelor_the_morning_of_the_first_bell.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] xanelor_the_morning_of_the_first_bell.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] xanelor_the_morning_of_the_first_bell.md: flat runs: 5 stretches of three sentences within 40% of each other (R4-14-RUN_RULE)
- [prose] the_war_in_the_north_v_the_shieldwarden.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_war_in_the_north_v_the_shieldwarden.md: Kharven recurrence: 0 of the five signature items present (none); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)
- [prose] the_war_in_the_north_iv_the_blank_seal.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] the_great_summoners_morning.md: three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)
- [prose] the_war_in_the_north_iii_utopia.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] xanelor_rikudoku_and_the_address.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] xanelor_after_the_crash.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [prose] xanelor_the_introductions.md: em dashes: 1 (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)
- [stale] scenes/the_war_in_the_north_iv_the_blank_seal.md: Möngön
- [stale] scenes/the_war_in_the_north_iv_the_blank_seal.md: Büri
- [stale] scenes/the_war_in_the_north_i_the_kharven_seat.md: Büri
- [stale] scenes/the_war_in_the_north_i_the_kharven_seat.md: Muken Büri
- [stale] scenes/the_war_in_the_north_v_the_shieldwarden.md: Möngön

## Cleared since last night

- none

## Still open: 233 (see reports/prose_pass.md, reports/reconcile.md; 22 files still carry Büri-register terms (156 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 6 push(es), 20 quiet run(s), 0 failure line(s)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-14.zip (23.7 MB, 1021 files)
- last run of this digest: 2026-09-18T03:30:18
