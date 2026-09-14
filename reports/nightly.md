# Nightly — 2026-09-14 03:30

## Overnight

First night on Linux. The digest ran on time at 03:30 and the index is exactly where the 00:16 run left it: validate passes, docket clear, one conflict open, the same 193 findings, none new, none cleared. No scene was archived since the last run, so there was nothing to verify.

The Notion sync has not pushed since 01:01, the last run on Windows. Three hourly runs here aborted with no NOTION_TOKEN, and the one that found a token (03:16) got 401 "API token is invalid" back from Notion. Until a working secret is in ~/.config/wotr/env, wiki edits do not reach the repo. What I'd do this morning: regenerate the secret at notion.so/my-integrations, paste it in as NOTION_TOKEN, check the wiki database is still shared to that integration, then `systemctl --user start wotr-sync` and look for a push in build/sync.log.

The backup wrote ~/wotr-backups/wotr-2026-09-14.zip (23.7 MB) on this disk only. Nothing carries it to Drive yet, so the newest copy off this machine is still yesterday's wotr-2026-09-13.zip on Google Drive. rclone is the missing piece; it is a sudo step, so it is yours.

Also waiting on you, unchanged since last night: the 43 Judger proposals for 08_sodoku_recalescence (`/judger apply 08_sodoku_recalescence ...`), and chapter 1 of kharven-year at its gate — `python build/book_next.py --approve 1` or `--reject 1 --note "..."`; nothing more gets written until you answer.

Nothing cleared.

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

- sync: 0 push(es), 0 quiet run(s), 1 failure line(s):  export failed (exit 1)
- backup:  wrote /home/oridon/wotr-backups/wotr-2026-09-14.zip (23.7 MB, 1021 files)
- last run of this digest: 2026-09-14T00:16:32
