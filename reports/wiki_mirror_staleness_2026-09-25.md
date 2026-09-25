# The wiki mirror stalled on 2026-09-24, and why an absence found by grep was not an absence

WAR-113, 2026-09-25. Diagnosis only — no fix is in this report, and none was applied
from it: every repair is in `build/*.sh` / `build/*.py` or is a commit of `wiki/`,
both barred to an extraction agent by `CLAUDE.md` and house rules 2.2, 5.3 and 6.
The repair is carried by **WAR-29** (unstick the sync) and **WAR-68** (the run does
not fit the unit's timeout), both already open and both assigned to Marsha Law.

## The rule this incident produces

**An absence found by grepping `wiki/` is only as good as the mirror's last commit.**
Before filing a finding whose whole content is "the card does not say X", check that
the mirror is current:

```bash
git log -1 --format='%ad  %s' --date=iso -- wiki/    # when the sync last committed
grep -m1 last_edited "wiki/<the file>"               # what Notion time that file carries
```

If the last `Wiki sync:` commit is hours old while the Notion page is newer, the
absence is an artefact of the mirror, not of canon. `wiki/` is a cache with no
staleness signal of its own; nothing in the file says "I am thirteen days behind".

## What happened

The last mirror commit was `c79211a`, **2026-09-24 17:15:14 -0400**, "Wiki sync:
9 file(s) changed in Notion". Nothing has been committed to `wiki/` since.

1. **17:03–17:08 local, the character-lore publish.** `build/lore_publish.py --apply`
   wrote the `Lore · The Life Behind the Card` section into the Notion card pages,
   in `sorted()` order over `imports/lore/cards/*.md` (`lore_publish.py:57`).
2. **17:15 local, the hourly sync.** Its export had read Notion at ~17:03, so it saw
   only the five cards published by then — Aeldoris Vanthryx, Aelum, Aethryn,
   Aren Vallestride, Asaemon, the first five in sort order, all carrying
   `last_edited: "2026-09-24T21:03:00.000Z"`. Committed and pushed as `c79211a`.
   **These are the five that `grep -rl` finds in git, and the alphabetical cut is
   the signature of a publish caught in progress, not of a filter.**
3. **18:00 local, the run that did the work and lost it.** It exported all 284
   changed pages into the main checkout's working tree, wrote `wiki/INDEX.md
   (632 pages)`, reached `embed start` at 18:28:51 — and was killed at 18:30:05 by
   `TimeoutStartSec=30min` on `wotr-sync.service` (WAR-68 has the journal line).
   It never reached the commit at `sync.sh:138-139`. The 284 files were left
   uncommitted.
4. **19:00 local onward, the loss made permanent.** `notion_export.py` writes each
   page file and then stamps `wiki/.manifest.json` with that page's new `edited`
   (`:430-431`), and the manifest is its only idempotence record (`:415-416`). The
   dead run had already written both. So the 19:00 export reported
   `0 to export, 632 unchanged` — correctly, and fatally. **No later run will ever
   re-write those files.** The mirror's real content exists only as uncommitted
   changes in the main checkout's working tree.
5. **19:18 local onward, the commit stage blocked too.** 19 consecutive runs,
   2026-09-24 19:18:09 through 2026-09-25 13:16:29, ended:

   ```
   pull --rebase failed (exit 128); committing on the local branch anyway
   sync failed: conflict markers in 1 file(s) after the pull; nothing committed, resolve by hand: RULINGS.md
   ```

## The measurement, on 2026-09-25 16:30

| | in git (`origin/master`) | in the main checkout's working tree |
|---|---|---|
| files carrying `Lore · The Life Behind the Card` | **5** | **276** |
| Hild's card: occurrences of `circlet` | 0 | **2** |
| Hild's card: `last_edited` | `2026-09-12T05:43:00.000Z` | `2026-09-24T21:06:00.000Z` |
| files modified under the sync's own paths | — | **290** |

So the export was never the problem. It read Notion right, wrote the right bytes,
and put them on disk. Only the commit is missing.

## Both candidates named on WAR-113 are refuted

- *"the export's change detection keys on a `last_edited` it reads from the mirror."*
  No. `notion_export.py:415-416` compares `manifest[id]["edited"]` against
  `x["edited"]`, which is `p.get("last_edited_time")` taken straight off the Notion
  page object (`:406`). The mirror file's frontmatter is never read back.
- *"`lore_publish.py` writes in a way that does not move the property the export
  compares."* No. It moved it. Hild's exported file carries
  `last_edited: "2026-09-24T21:06:00.000Z"` — the lore edit's own timestamp. (The
  REST API truncates `last_edited_time` to the minute, which is why WAR-113's
  `21:06:22Z`, read through a different API, and the file's `21:06:00.000Z` are the
  same edit and not two.)

## A third defect, not previously written down

The guard that blocked 19 runs aborts on a file the sync does not own and could not
have committed.

- `sync.sh:114` tests `git diff --name-only --diff-filter=U` across the **whole**
  working tree, and `:115-118` exits 1 on any hit.
- `sync.sh:123` lists the paths the sync owns — `wiki table scenes/CAST.md
  scenes/TIMELINE.md build/.notion_publish.json` — and the commit at `:139` is
  path-limited (`-- "${paths[@]}"`).

`RULINGS.md` is not in that list. Conflict markers in it could never have reached a
sync commit. An unmerged file in a path the sync neither stages nor commits stopped
the mirror for nineteen hours. The guard's intent (never commit conflict markers) is
right; its scope should be `"${paths[@]}"`, the same list the commit uses. Noted here
for WAR-29; not fixed here, because `build/*.sh` is barred.

Where the `RULINGS.md` conflict came from is already on record: `CONTINUE.md`'s WAR-96
block and WAR-104 / WAR-112 — `log_ruling` run from an agent worktree appends to that
worktree's `RULINGS.md` and pushes a stale local `master`; `--autostash` at
`sync.sh:107` then collided on the restore.

## Two more failures visible in the same log, both already filed

- `notion_publish.py` (the repo → Notion direction) has failed on **every** run since
  at least 2026-09-24: `400 validation_error: body.children[79].table.children.length
  should be ≤ 100, instead was 149`. Non-fatal to the sync by design
  (`sync.sh:85`). That is **WAR-55**, in progress.
- The 2026-09-25 15:00 export died on `TimeoutError: The read operation timed out`
  against the Notion API. Fixed overhead for the crawl alone was 16m18s on the 13:00
  run. That is **WAR-68**.
