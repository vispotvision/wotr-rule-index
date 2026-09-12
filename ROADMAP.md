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

## Folding packs into base guides — first four done, 2026-09-12

Isaac: "yes — start folding the packs in now." 18 base guides live at
`C:\Users\isaac\Documents\WOTR True Canon\`; each amendment rule names its
target guide in its `amends.guide` field. The four most-amended guides are
done -- each got a new dated edition alongside the original (never
overwritten), with a changelog listing every rule ID folded in and any
judgment call flagged rather than silently made:

- [x] `WOTR_Master_Style_Directive (2026-09-12 edition).md` — 86 amendments folded; 3 judgment calls flagged (a same-day narration-authority supersession applied despite falling outside the strict amends-field filter; a scope-narrowing read reconciling Pack Five vs. Twelve/Sixteen on prose texture; one non-target-guide clarification folded into the chemistry-ban text)
- [x] `WOTR_Ability_Technique_Design_Guide (2026-09-12 edition).md` — 56 amendments folded; 2 flagged (the legacy Corruption Vector field kept as non-mandatory pending a future pack; the naming-strike rule deferred to the Character Naming Guide rather than importing its content)
- [x] `WOTR_Character_Naming_Guide (2026-09-12 edition).md` — 47 amendments folded; reflects today's Ayame Yuno/Yasoshima rulings; C-005/C-006 (Zettai vs. Zettari) correctly left open, not guessed at
- [x] `WOTR_Combat_Craft_Guide (2026-09-12 edition).md` — 29 amendments folded, plus the 7 live named-character combat assignments in the main body and the 2 still-proposed ones (Wren, Edward Lambert) in a clearly marked pending-review appendix

Remaining ~14 guides, by amendment count: Manual Verification Guide (21),
Scene Writing Process Guide (19), Mass Combat Craft Guide (18), Racial
Voice and Dialect Guide (15), Dialogue Craft Standards (9), AI Writing
Tells to Avoid (8), Visual Aesthetic Guide (8, plus the new Moto
material-culture proposal once ratified), Item and Equipment Writing
Guide (7), and the rest with only 1-6 amendments each -- pick up in a
later session the same way (one agent per guide, same prompt shape).

## Deferred until there is a reason

- The WOTR Console (local dashboard); a standalone app; n8n; the pack authoring template
- Backups: weekly dated Notion export to Drive (small; do when convenient)

## Still owed by Isaac

- ~~Muken's children (R22-10)~~ ruled 2026-09-12: the wiki's five (Sodoku, Sonzai, Emira, Tomuka, Ezo)
- ~~Packs Sixteen through Nineteen~~ ratified wholesale 2026-09-12
- ~~Black Agent's and Rengai's combat assignments~~ ratified as pitched 2026-09-12
- Three of the four remaining Four Crafts items (R9-1): Law III's rewrite, the golden-age question, the Latinate/vernacular doublet's scope (the Law V gate was ruled: Stage VII, 2026-09-12)
- Ratification of every proposal Phase A files
