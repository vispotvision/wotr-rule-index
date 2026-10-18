# CONTINUE — how to pick this work up cold

Read this first in any new session (scheduled or not). Isaac's standing
direction: inside work he has asked for, make the calls; no "pending" slots.
`ROADMAP.md` is the plan; this file is the live state. Newest block first;
append a dated block, do not rewrite older ones (two sessions write this repo
at once — `git pull` before editing, and commit only your own files).

## State on 2026-10-18 (lore reset: the old archive is lore/v1)

Isaac is resetting the lore again; the archived scenes go into their own
lore-version. His calls: scenes **and** table state move; old scenes stay
searchable, labelled. Done (commits 22925d7, 4437d17): `scenes/` (243 files with
ARCS/CAST/MANIFEST/TIMELINE/CONTINUITY and cast/), `table/` fronts, ledger, npcs,
sessions, threads (+ their .md views), the vault's `wiki/The Scene Archive/` and
the retired `wiki/The Table — Running Pieces/` pages (the Docket page stays) are
in `lore/v1/` as pure renames (`lore/v1/README.md`). Live `scenes/` and `table/`
start empty (`table/voices.yaml` stays); `session_start` reports no last scene,
`scene_recall` finds nothing until new scenes are archived;
`scene_recall(query, old_lore=True)` searches lore/v1 with every hit tagged
OLD LORE v1. The semantic index carries a `lore-v1` corpus. MCP public/readonly
and the bot restarted. Six uncommitted scene edits (CONTINUITY.md and five
scenes, not this session's) moved with the files and sit unstaged under
`lore/v1/scenes/`.

**Not moved, may still carry old-lore facts:** character cards and the rest of
the wiki, `book/`, RULINGS and the rule index. The reset of those is its own job.

## State on 2026-10-17 (two questionnaires; the table made lean; R79-1 to R79-12)

Isaac ran two questionnaires in one session: prose, conflicts and the table
(`imports/drafts/prose-rp-questionnaire/`, 68 answers, decisions.md maps each to
rule ids) and coverage of everything else (`imports/drafts/coverage-questionnaire/`,
64 answers, audit-digest.md). Law: **R79-1 to R79-12** in
`rules/doc-directions-2026-10-17.yaml`, each verbatim its RULINGS.md paragraph.
The headline: Natalie may write his PC; every in-fiction reply ~3,500 words
(Discord too); no close, no foot, silent upkeep of Ledger/Fronts/roster/cards
at scene end; RP fights show full mechanism; no rhythm or count rules anywhere;
Kharven recurrence gone; NPC thoughts free; anime-big emotion; sources by field;
estimates plain and canon; State of Play retired; judger retired.

Applied: `desktop/NATALIE.md` rewritten clean (no ◆; Kharven Inventory moved to
`desktop/inventories/kharven.md`); verify.py stripped of every statistic and
quota (The Weak Grade passes clean); mcp_server.py core surface of 34 tools with
the rest behind `--ops` / `WOTR_MCP_OPS=1` (units not changed), session_start
lean, session_end = silent upkeep + archive, recurrence_report/voice_*/prose_pass
deleted; wotr-rp and wotr-rules folded into wotr-write; ChatGPT instructions,
NATALIE.gpt.md, PROJECT_INSTRUCTIONS updated; the five style-bank samples
rewritten to the new law; nightly slimmed (review dropped, baseline reset);
book timer, n8n, wotr-jobs and wotr-mcp-local stopped and disabled; CLAUDE.md
splits reading by task; older CONTINUE blocks moved to `CONTINUE_HISTORY.md`.
The long-uncommitted R77-1/R77-2 application (verify.py, skills, five rule
files) was taken over and committed with this pass after a 45-minute mail
notice went unanswered.

**Owed / Isaac's hands:** remove the claude.ai-synced WOTR skills in claude.ai
settings (local deletion re-syncs); the read-only MCP works, so re-share its
current URL with whoever got a 401; add `--ops` to a unit if a surface needs
the audio, Trello or migration tools.

## State on 2026-10-16 (the elevated word bank retired)

Isaac's direction: **R78-11-WORDS_FROM_THE_THING**. No fixed word list; each word
is chosen from what the sentence describes. `desktop/style-bank/elevated-words.md`
is deleted, verify_scene's elevated-density WARN removed (the fight-abstraction
WARN stays), notes on R78-1 and R78-3. Swept: NATALIE.md, the Manual Verification
Guide, BOOK_PIPELINE, SHARED_MEMORY; the skills, ChatGPT skills, Combat Craft
Guide and the wiki carried no bank references. Older blocks below that name the
bank are history. Old chapter briefs under `book/` still cite it; they are records.

## State on 2026-10-15 (system touch-ups and connections; Notion out of blocks)

Isaac ran three more questionnaires (system-touchups, release forms, and a 16-batch
connections questionnaire built from two ask_chatgpt rounds) plus three ChatGPT
digestibility rounds. Law: **R78-9** (enhancement, Drafts, enchantment, training,
concision) and **R78-10** (stacking cap of two Grades, stat Grade decides, Aether Class
sets eta, drain as time from full, the tell ladder, fight Drafts refill, tags, three
roads to each Catalyst, release forms canon, card fields, disciple ranks, renown,
tournaments, Draft prices x3 a Stage, Malphas as the great villain over about ten
numbered lieutenants, Well-spawn masks, crews proposed, skips via pass_time).
R44-3 superseded (the S/SS gap is closed). NATALIE.md, wotr-ledger, wotr-stat-line,
the wotr-write references, the Combat Craft Guide banner and mcp_server/table.py
carry them. The card template (untracked, another session's) has the new fields.

**Notion is blocked:** the workspace hit its free block limit on 2026-10-15 (the
update tool returns entitlement_required). Applied before the stop: The Four Crafts,
The Sixteen Stages, The Ladder and the Draft, The Trait System, The Field Manual.
**Owed when Notion has room**, all in `imports/drafts/system-pages/`:
- `audit/apply.json` pages 5 to 33 (strip a leading "> " from old_str; multi-line
  items need the live page fetched first), `audit/collisions.json` (34 term fixes),
  `audit/maths.json` (91 Grade-table fixes; ripples onto cards listed in the agent
  report: SS floor, speed bands, Peak Force bands, seven carve-out paragraphs in X);
- new pages: primer.md, reinforcement.md, stacking-and-spending.md,
  runes-and-tags.md, training-and-sects.md, release-forms.md, draft-catalogue.md,
  tag-catalogue.md, well-spawn.md (strip each "Notes (not published)" section);
- release-folk-names.md into each Standing Inventory (repo files, not Notion);
- still drafting at close: start-here, power-terms, annotated-exchange, whos-who,
  factions-at-a-glance, newcomer-test.
Conflicts still to fix on pages: The Gate section I ("waking is taught") vs R78-10.

## State on 2026-10-14 (WOTR's identity re-ruled: dark shonen cultivation, physical fights, saturated English)

Isaac ran four questionnaires in one Claude Code session (answers in
`imports/drafts/vocab-clarity-questionnaire/` and
`imports/drafts/page-craft-questionnaire/`, 21 batches) and every answer is law:

- **R78-3** physical clarity and saturated vocabulary: a blow is body, path,
  target, result; no "the line", measure, tempo, vector, geometry or the read in
  narration; elevated English of every root in nearly every sentence, stackable;
  plain body parts; system and science terms free in narration. verify.py WARNs
  on fight abstractions and on bank density under 50% (`build/test_r78_3.py`).
- **R78-4 to R78-8** (`rules/doc-directions-2026-10-14.yaml`): WOTR is a dark
  shonen cultivation fantasy in a magitech world, not grimdark; techniques
  shouted by English name, afterimages, geysers, free flashbacks; coloured auras,
  transformations, open sensing, vows, release forms, fewer readouts; three roads
  to breakthrough, an Aizen-shaped villain over ranked lieutenants, a core crew,
  cliffhangers; anime-big emotion, phonetic accents, anime gags from the
  characters who play that way. Supersedes R9-3, R70-103, R70-113,
  R5-D-HUMOUR_BARRED; notes on 23 more rows. NATALIE.md rewritten to match.
- **Consistency sweep done:** 26 guides, skills, prompts, samples and tool
  docstrings rewritten; the live Combat Craft and Manual Verification guides
  carry a dated amendment block; *The Color of Essence* Prose Application line
  fixed in Notion.
- **Owed:** release forms are a draft (`imports/drafts/release-forms/`, five
  questions for Isaac). `build/verify.py`'s R77-1 region (BLADE_ACTION counting
  measure/tempo, the clinical ANATOMY list, "Eastern terminology unresolved", the
  readout cap) waits on the session holding that open edit; so do
  `build/test_combat_directions.py` (clavicle fixture),
  `desktop/templates/CHARACTER_CARD_TEMPLATE.md` (chant tongue; no aura, sound
  or release fields) and `desktop/style-bank/archive-study.md`, all untracked.
  Turn shape and footers (batch 8) was dismissed by Isaac, not answered.

## State on 2026-10-13 (vocabulary pushed high, modern science, every open conflict ruled)

Isaac: vocabulary isn't reaching past base words; make the rules consistent;
and he retracted the 1900 limit on physics. Done in one Claude Code session:

- **R78-1-VOCABULARY_PUSHED_HIGH** (`rules/doc-directions-2026-10-13.yaml`)
  applies his 2026-10-11 direction, which had never reached the index (load_rules
  kept serving R51-13's "by ear"); supersedes R51-13. The widened elevated bank
  is `desktop/style-bank/elevated-words.md` (by sense domain, glossed, POV reach,
  once per scene); NATALIE.md points to it. A rare-word checker was tried and
  dropped: frequency counts reward "breastbone", not diction.
- **R78-2-MODERN_SCIENCE_IDEAS** (Isaac, 2026-10-13, scope by questionnaire):
  modern science in battle and magical advancement, known through the Aether by
  high-Stage practitioners, Measurewrights and scholars; hardware keeps R53-01
  and R53-03. Closes C-158; NATALIE.md's "nothing after 1900" line struck.
- **Every open conflict ruled** (C-113 to C-162, six read-only drafting agents,
  checked and logged as agent rulings in RULINGS.md; C-160 to C-162 filed and
  ruled the same day). CONFLICTS.md has no open row but the format example.
  Applied: rule notes, repo scenes, and about fifty Notion edits. Owed list:
  `imports/drafts/conflict-rulings-2026-10-13/apply.md` (Malphas lich rebuild,
  Open Crucible dating, the C-129 edits in three files another session holds
  dirty, TIMELINE rows, Scene Archive copies).

`out/` was not regenerated into a commit: it would carry another session's
uncommitted rule edits. load_rules reads `rules/` live.

