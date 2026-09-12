# Roadmap

Agreed with Isaac on 2026-09-12. Phases run in order; each item is checked off
with the commit that landed it. Isaac's standing direction (2026-09-12): inside work he has asked for, the calls
are made, not left pending.

## Phase A — finish what the rulings created

- [x] Filemu Agamalu's card without the Ava-name (C-002)
- [x] Taulagi and Afasoa as Yuno retainers with Japonic names (R23-7)
- [x] Stage-name sweep of the cards: Ignition/Temper → Murmuring/Flourishing (R14-A)
- [x] Büri sweep applied to the 11 scenes in the repo; wiki pages swept block by block (R22-9)
- [x] Proposals filed: Northern forms for airag, borts, aaruul, the deel, Tengri (R23-8); a Japonic name for the island (R21-5)

## Phase B — the table

- [x] Fronts as clocks: `table/fronts.yaml`, `fronts()` / `advance_front()`, shown by `session_start`
- [x] The Ledger collects: `due()` returns what comes due tonight
- [x] `session_end(scene)`: drafts State of Play, Ledger appends, Front advance, docket additions from the scene text
- [x] Scene Menu generator from the clocks and the ledger
- [x] NPC roster per thread

## Phase C — canon integrity

- [x] The reconcile: wiki vs live rules vs scenes, contradictions listed
- [x] Timeline: `scenes/TIMELINE.md`, every scene placed; new scenes checked against it
- [x] Card-to-scene consistency: what a scene says about a character vs the card
- [x] Pack impact check: which live rules a new pack's text touches, before extraction

## Phase D — prose

- [x] Ladder / prose-law pass over the archive: `reports/prose_pass.md`
- [x] Voice fingerprints per character; `verify_scene` flags swapped voices
- [ ] Standing Inventory skeletons for the other cultures, drafted from the wiki for pruning
- [x] Recurrence tracking across scenes (which signature items are stale or overused)
- [x] The gap-fill pass (Thirteen §5) as a structured report

## Phase E — readers

- [x] ARCS.md ordered (set by Claude Code from the numbering; move lines freely)
- [x] Arc compilations: one document per arc in Drive
- [ ] A reader's codex: the trimmed version of the wiki
- [x] Epub build

## Deferred until there is a reason

- The WOTR Console (local dashboard); a standalone app; n8n; the pack authoring template
- Backups: weekly dated Notion export to Drive (small; do when convenient)

## Still owed by Isaac

- Muken's children (R22-10)
- Packs Sixteen through Nineteen
- Black Agent's and Rengai's combat assignments
- The four remaining Four Crafts items (R9-1)
- Ratification of every proposal Phase A files
