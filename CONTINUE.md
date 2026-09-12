# CONTINUE — how to pick this work up cold

Read this first in any new session (scheduled or not). Isaac's standing
direction: inside work he has asked for, make the calls; no "pending" slots.
`ROADMAP.md` is the plan; this file is the live state of the in-flight jobs.

## In flight on 2026-09-12, resumed after the session-limit reset

- Inventories: all six landed, reviewed, committed. Workflow `wf_f0f00731-2d0` resumed
  (task id `wmp0n8oyi`) to write `docs/READERS_CODEX.md`; it is also re-touching the
  inventories on its review pass (saw a live edit to `desktop/inventories/eresse.md`
  mid-run) -- do not commit the inventories again until this run finishes, then
  review and commit whatever it changed plus the codex.
- Trello conversion: 43 of 200 converted files existed when this resumed; workflow
  `wf_5988bc5a-45d` resumed (task id `wv22tz6jn`) to finish the remaining ~157 and
  their reviews.
- NATALIE.md's inventory line: done. Both the session-start-protocol line and the
  Kharven section's closing line now point at `desktop/inventories/`.
- `build/publish_imports.py`: written and committed. `--dry-run` shows 3 of the 43
  converted-so-far cards are clean and publishable now; 40 are held (unresolved
  "pending Isaac" drafts, or Tovain Zethriel's restriction stub) -- see
  `reports/publish_imports_held.md`. Do not run it for real yet; wait for the
  conversion workflow to finish, then do the resolve pass below, THEN run it.

### 1. The Trello conversion (workflow `wf_5988bc5a-45d`)
- 200 cards staged under `imports/trello/<group>/`; agents write
  `imports/converted/<group>/<slug>.md`; batches in `imports/BATCHES.json`.
- Check progress: count files in `imports/converted/*/` (target 200).
  Journal: `~/.claude/projects/C--Users-isaac-Documents-wotr-rule-index/0b7e1af7-86b6-43ae-b4ca-7345be58aff1/subagents/workflows/wf_5988bc5a-45d/journal.jsonl`.
- If the workflow died, resume it: `Workflow({scriptPath: ".../workflows/scripts/wotr-trello-conversion-wf_5988bc5a-45d.js", resumeFromRunId: "wf_5988bc5a-45d"})`
  (completed batches return cached; only unfinished ones re-run).
- **2026-09-12, later: the Review phase is cut.** Isaac: he'll judge quality
  himself and it was burning usage for no benefit. The script (same path
  above) now has a Convert-only pipeline, no reviewer stage; already-cached
  "convert batch N" calls still replay, so resuming just finishes the
  remaining batches with no review pass. Don't re-add a review stage unless
  Isaac asks for one back.
- **After all 200 exist:** run the resolve pass — a workflow (or a loop of agents,
  ~8 files each) that opens every converted file, replaces every "pending
  Isaac" / "estimate" / "TBD" with a committed value derived from the FOW
  tables in `imports/BRIEFS/common.md` (or the most conservative value
  consistent with the card), and rewrites the migration note to state the
  choices. Since the review pass is cut, `python build/verify.py` over the
  prose sections is no longer "just double-checking a reviewer" — it's the
  only mechanical check these files get before Isaac looks at them himself,
  so run it and fix what it flags.
- **Then publish** with `python build/publish_imports.py` (written; it skips
  anything that still matches "pending Isaac" / TBD / estimate / a restriction
  stub, so the resolve pass above must actually land first or nothing new
  publishes). It creates Volume VI and The Iridescent Archive's four sections
  itself on first use, then runs `notion_export.py` at the end so `wiki/` picks
  up the new pages. Then `git add -A && git commit && git push`. Check
  `reports/publish_imports_held.md` afterward for anything still held.
- Then `python build/docs_export.py --out "G:/My Drive/War of the Realms — Documents" --private-out "G:/My Drive/War of the Realms — Private"`
  so the Drive documents carry the new sections.

### 2. Inventories and the reader's codex (workflow `wf_f0f00731-2d0`)
- Outputs: `desktop/inventories/{accord,dawi,moto,eresse,expanse,korvaeth}.md`,
  `docs/READERS_CODEX.md`. When present: commit, push; add READERS_CODEX to
  `docs_export.py` RULE_INDEX-style targets? No — publish it as a Notion wiki
  row "A Reader's Codex" via `notion_publish` TARGETS (parent `database_id`)
  and add it to the Drive documents (docs_export: a one-page document).
  Point NATALIE.md's "Other cultures have no Inventory yet" line at
  `desktop/inventories/` (the MCP `_inventory` already reads that folder).

### 3. Housekeeping still open on ROADMAP.md
- Fold the packs into the base guides (big; a workflow: one agent per base
  guide in `C:\Users\isaac\Documents\WOTR True Canon\WOTR_*.md`, folding every
  live rule whose `amends.guide` names it, writing a new edition next to the
  old with a change log; never edit `sources/`).
- Standing Inventory skeletons: done by workflow 2 when it lands.
- Weekly Notion export backup to Drive (small).

## Action needed from Isaac: share a Notion page with the integration

Isaac moved "In-World Documents & the Narrative Archive" (Scene Archive,
Running Pieces, every scene) and The Rule Index under a new page,
"Information not on WIKI" (to keep them off the public wiki). That took
them out of the wiki database, and the "oridon" integration was never
connected to the new parent page, so `notion_export.py` gets a 404 trying
to reach it — it now warns and skips the delete-sweep instead of wiping
wiki/ (fixed in build/notion_export.py, commit 02c989c), but the mirror for
that whole subtree is stale until this is fixed. **Isaac: open "Information
not on WIKI" in Notion -> "..." menu -> Connections -> add the "oridon"
integration.** Once shared, the next sync picks it up with no code changes
needed.

## Owed by Isaac (do not decide these)
- Muken's children (R22-10); Packs Sixteen–Nineteen; Black Agent's and
  Rengai's combat assignments; the four Four Crafts items (R9-1); C-003.

## Every session ends with
`python build/validate.py` (must PASS) → `python build/resolve.py` → commit →
push → tick ROADMAP.md → update this file.
