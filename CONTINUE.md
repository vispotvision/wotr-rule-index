# CONTINUE — how to pick this work up cold

Read this first in any new session (scheduled or not). Isaac's standing
direction: inside work he has asked for, make the calls; no "pending" slots.
`ROADMAP.md` is the plan; this file is the live state of the in-flight jobs.

## In flight on 2026-09-12 (session limit hit ~02:30, resets 05:00 America/New_York)

- Inventories: all six landed and reviewed, committed. The reader's codex agent FAILED on the limit: `docs/READERS_CODEX.md` does not exist yet; re-run the codex part (resume workflow `wf_f0f00731-2d0` with its scriptPath; the six inventory agents replay from cache).
- Trello conversion: 41 of 200 converted files existed when the limit hit; the workflow will have died; resume it as described below.
- NATALIE.md's Kharven-only inventory line still needs pointing at desktop/inventories/ (the MCP already reads that folder).

### 1. The Trello conversion (workflow `wf_5988bc5a-45d`)
- 200 cards staged under `imports/trello/<group>/`; agents write
  `imports/converted/<group>/<slug>.md`; batches in `imports/BATCHES.json`.
- Check progress: count files in `imports/converted/*/` (target 200).
  Journal: `~/.claude/projects/C--Users-isaac-Documents-wotr-rule-index/0b7e1af7-86b6-43ae-b4ca-7345be58aff1/subagents/workflows/wf_5988bc5a-45d/journal.jsonl`.
- If the workflow died, resume it: `Workflow({scriptPath: ".../workflows/scripts/wotr-trello-conversion-wf_5988bc5a-45d.js", resumeFromRunId: "wf_5988bc5a-45d"})`
  (completed batches return cached; only unfinished ones re-run).
- **After all 200 exist:** run the resolve pass — a workflow (or a loop of agents,
  ~8 files each) that opens every converted file, replaces every "pending
  Isaac" / "estimate" / "TBD" with a committed value derived from the FOW
  tables in `imports/BRIEFS/common.md` (or the most conservative value
  consistent with the card), and rewrites the migration note to state the
  choices. Then run `python build/verify.py` over the prose sections is
  optional; the reviewers already did prose law.
- **Then publish** with `python build/publish_imports.py` (write it if it does not
  exist yet: for each converted file, create the Notion page under its target —
  characters under "Volume V — Character Cards" / "Volume VI — Character Cards"
  (create Volume VI under Characters `3b158200-eb22-8188-b4d8-d9b195f254dd` if
  missing) / "Volume IV — Character Cards"; everything else under a new
  top-level wiki row **The Iridescent Archive** with sub-pages Techniques,
  Spellcraft, Artifacts, Bestiary Additions — using
  `notion_publish.create_page` and `md_to_blocks`, then `notion_edit.refresh_mirror`
  for each new page so `wiki/` has them, then `git add -A && git commit && git push`).
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

## Owed by Isaac (do not decide these)
- Muken's children (R22-10); Packs Sixteen–Nineteen; Black Agent's and
  Rengai's combat assignments; the four Four Crafts items (R9-1); C-003.

## Every session ends with
`python build/validate.py` (must PASS) → `python build/resolve.py` → commit →
push → tick ROADMAP.md → update this file.
