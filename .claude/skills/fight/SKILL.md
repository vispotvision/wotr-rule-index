---
name: fight
description: Write a War of the Realms fight or set piece through the full pipeline. Use when Isaac types /fight or hands over a fight beat; loads the exemplars, fills the state sheet and zoom map, drafts blow by blow with no word count, runs the review passes and verify_scene.
---

# /fight

The fight pipeline, in order. The law is `desktop/NATALIE.md` (Fights on the page, the fight craft block, Magic in combat, Describing a working, Onomatopoeia). This skill only sequences it. Never call ChatGPT or Codex (Isaac has no plan).

1. **Load.** `load_rules(tags=[], brief=True)` once a session; then prose-law, combat, adjudication, magic-mechanism and pov in full the first time. Read the named fighters' cards and `fow_line`; use the wotr-stat-line loadout.
2. **Exemplars.** Read `desktop/style-bank/fight-exemplars/EXEMPLARS.md`, `desktop/style-bank/exemplars/TECHNIQUE_DISPLAY.md` and `desktop/style-bank/sound-lexicon.md`. Learn the density; take no images. Check `desktop/style-bank/used-devices.md` so nothing is reused.
3. **Research.** The wounds that will matter (`wotr-wound`), how each working works (`wotr-phenomenon`, the Superpower Wiki, the Wellspring analogue), crafts and period detail. Notes go to `research_notes/`.
4. **State sheet.** Fill `desktop/templates/FIGHT_STATE_SHEET.md`: ground, positions, distances, weapons, wounds, reserve, the planted clue, the ladder, and the zoom and volume map (one movement at peak). Each working takes its Wellspring signature from `desktop/style-bank/wellspring-signatures.md`.
5. **Brief.** `scene_brief` for a set piece.
6. **Draft** to `~/wotr-drafts/<slug>.md`: probe, reveal, counter, escalate, price; the Blow Card on every blow, landed or not; the Kill Card at the turn; magic riding on the blow; constant banter; sound words per the lexicon; American spelling. No word count: the fight is as long as it needs.
7. **Review.** `desktop/FIGHT_REVIEW_PASS.md` and `desktop/PROSE_REVIEW_PASS.md`, silently, fixing before Isaac sees it. Add the fight's signature image to `used-devices.md`.
8. **Verify.** `verify_scene` with combat=True; fix every FAIL.
9. **Deliver.** The scene alone, no commentary. A set piece waits for his word before it is archived; an ordinary turn archives at scene end. Upkeep (Ledger, Fronts, roster, cards) is silent.
