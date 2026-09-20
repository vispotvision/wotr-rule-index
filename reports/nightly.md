# Nightly — 2026-09-19 22:20

## Overnight

Second run today, nineteen hours after the 03:30 one. Nothing landed in between: no scene archived, no commit since the morning nightly, nothing new and nothing cleared. The 22 findings from this morning have rolled into the open count, 233 to 255. Same findings, one day older.

The ten scenes from this morning still have no close. bot/queue holds nothing for any of them, so that is still ten `/judger` runs, and still the only work that needs your hands.

08_sodoku_recalescence: 43 proposals waiting. Book kharven-year: stopped at the chapter 1 gate until you `--approve 1` or `--reject 1`.

The backup has not written since 09-14 03:24. Five days with no line in build/backup.log; the digest still shows the 09-14 zip only because it looks back eight days. This session could not read the timer, so I'd run `systemctl --user list-timers` first thing and see whether it fired and died or never fired.

Sync: quiet all day, last push 23:06 last night, no failures. It has skipped scenes/YOKO_MISHIRO.md on every run since 09-14 (117 times) because her Notion parent page is not shared with the integration. One share on the Notion side clears it.

Two drafts sit at the repo root, untracked and outside scenes/: "The War in The North.md" (4,114 lines) and "Untitled.md" (6,423 lines, Sodoku at the rail off Satulagi's north), both from last night. Nothing audits or syncs them where they are. I'd move them into scenes/ under real names when they're ready; I have not touched them.

build/mcp_server.py carries an uncommitted cast_index alias change dated 09-15. It is not from the nightly; commit it or drop it.

validate PASS, docket 0, one conflict open.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 0 / CLEARED 0 / STILL OPEN 255

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- none

## Still open: 255 (see reports/prose_pass.md, reports/reconcile.md; 22 files still carry Büri-register terms (156 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 3 push(es), 23 quiet run(s), 0 failure line(s)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-14.zip (23.7 MB, 1021 files)
- last run of this digest: 2026-09-19T03:30:30
