# Nightly — 2026-09-14 00:07

## Overnight

Nothing moved since last night: validate PASS, docket empty, the one conflict still open, 193 findings still open with none new and none cleared. No scene was archived, so there is nothing to verify and nothing new for the Judger.

Two things wait on you. The 43 proposals for 08_sodoku_recalescence are still sitting in the queue — `/judger apply 08_sodoku_recalescence ...` when you have the morning for it. And chapter 1 of kharven-year is written and gated; nothing more gets written until `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md).

The sync has not pushed since 23:06. Your 23:38 commit (the new nightly) is still local — master is one ahead of origin — because `pull --rebase` fails with exit 128 on the unstaged edits in the working tree (build/nightly.ps1, build/nightly.py, .nightly_state.json, the four reports, bot/.bot.sync.err). I would commit or stash those, then let the next hourly sync rebase and push; until then every run will fail the same way. The 23:51 sync log also ends at "publish start" with no push line after it. The backup is fine: wotr-2026-09-13.zip, 23.6 MB, 1023 files.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 0 / CLEARED 0 / STILL OPEN 193

## Judger queue (proposals awaiting Isaac)

- 08_sodoku_recalescence: 43 waiting — `/judger apply 08_sodoku_recalescence ...`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- none

## Still open: 193 (see reports/prose_pass.md, reports/reconcile.md; 19 files still carry Büri-register terms (140 hits) in all. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets.)

## The sync and the backup (last 26 h)

- sync: 1 push(es), 0 quiet run(s), 2 failure line(s):  pull --rebase failed (exit 128); committing on the local branch anyway
- backup:  wrote G:\My Drive\War of the Realms — Backups\wotr-2026-09-13.zip (23.6 MB, 1023 files)
- last run of this digest: 2026-09-13T23:44:43
