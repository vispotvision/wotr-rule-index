# Nightly — 2026-09-21 14:40

## Overnight

Nothing moved in the numbers: validate passes, the docket is empty, the one conflict is still open, 255 findings still open with none new and none cleared, and no scene was archived since the last run. Ultron was off from some time after the 23:05 sync until 14:40 today, so this digest ran at boot, not at the timer.

The sync is still not pushing. Every hourly run last evening (19:06 through 23:05) failed at the push, and the 14:40 run at boot died earlier than that — name resolution failed, so the Notion export never started; that one is the network not being up yet, not a new fault. Two nightly commits (12ba485 and adc4829) are still local, so GitHub is two nights behind. My check of the remote was refused, so I can't say from here why the pushes fail: run `git push origin master` by hand and read what git prints. The 15:00 run will show whether the network is back.

No backup this morning: the 03:00 timer fired into a machine that was off, so the newest zip is still yesterday's, wotr-2026-09-20.zip (24 MB, 1,077 files).

Waiting on you, same as last night: 43 Judger proposals on 08_sodoku_recalescence (`/judger apply 08_sodoku_recalescence ...`), and chapter 1 of kharven-year is still gated — `python build/book_next.py --approve 1` or `--reject 1 --note "..."`; nothing more gets written until you answer.

Uncommitted: "The War in The North.md" and "Untitled.md" still sit untracked at the repo root, desktop/ryoku-wotr/ (the bar plugin, since 09-19) is untracked too, and build/mcp_server.py now carries 96 changed lines (cast_index folds short roster names into their full card names). I'd move the two drafts into scenes/ if they're scenes, and commit the plugin and the MCP change or drop them. Standing: scenes/YOKO_MISHIRO.md still isn't publishing (its Notion parent isn't shared with the integration) and the Drive isn't mounted, so docs are skipped.

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

- sync: 0 push(es), 0 quiet run(s), 6 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-20.zip (24.0 MB, 1077 files)
- last run of this digest: 2026-09-20T18:34:57
