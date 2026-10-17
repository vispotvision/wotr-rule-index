# Coverage audit digest (2026-10-17) — open points still to ask, with ids

## Machinery (pipelines audit)
- Discord 3,500-word delivery: bot /post splitting a .md at paragraphs; /verify bands (bot/cogs/craft.py:80); NATALIE "closes" line.
- Multiplayer Discord: 3,500 + stop at first PC who decides; never another player's PC; R72-36 reply window.
- Nightly (nightly.sh/py, timer 03:30): recurrence, prose_pass, Büri sweep, findings baseline; Overnight note.
- nightly_review.py: unasked ChatGPT cross-read of every archived scene.
- wotr-book.timer blocked nightly since 10-13 (kharven-year ch1, night-watch ch1 gate); book-chapter.js:52 lie+misreading quota, voice_check stats, word 80-150%; BOOK_PIPELINE.md n8n design; wotr-book:201 via wotr-ledger; books read Fronts/Ledger?
- n8n, wotr-jobs (8799), wotr-mcp-local (8766) idle; wotr-mcp-readonly 401 since 10-16.
- Paperclip leftovers: CLAUDE.md "Paperclip docket (Doc Kett...)" + wotr-conflict skill missing; wotr-claude-refresh.timer; desktop/ryoku-wotr/bin/team.sh ask.sh; .paperclip dirs.
- Session reading load: CLAUDE.md makes every session read CONTINUE (2,336 lines), AGENTS, SHARED_MEMORY; phase-stop rules are for extraction.
- Synced claude.ai skill copies (~/.claude/skills/synced/...) diverge from repo skills.
- Skill consolidation: fold wotr-rp into wotr-write; wotr-rules into reference; retire wotr-ledger/judger.
- Orphaned tools: recurrence_report, voice_check, voice_fingerprints (+table/voices.yaml), prose_pass, gap_fill.
- Research plumbing: research (Gemini) vs research_chatgpt (stuck item since 10-06); handoff dead kinds; natalie double-load in Claude Code.
- Tool surface: 61 tools; trello_cards, convert_character, stale_names, cast_index, pack_impact, sync_now, audio set, chatgpt_image, writers' room.
- Sync: header says hourly (15-min); Drive step skipped; push failures; backup read as missing.
- G1-style: wotr-ops Notion/session_end/judger; wotr-stat-line Notion card; wotr-npc lie + npc_set; wotr-chatgpt pass_time/ledger handoffs; CHATGPT_INSTRUCTIONS.md:17,24; NATALIE.gpt.md:85.

## Cards and techniques
- PC kit fallout rows: R47-1, R52-10, R52-09 draft mark; growth R75-29, R75-16, R75-18 (A2 answered: growth stays his).
- Card bookkeeping after no close: R70-98, R75-11, R75-35, R75-41, R75-37, R75-38, R78-10 renown, R14-7.
- Card cap 16,348 (Trello reason) + "all mandatory" sections + R75-25 head, R75-35, R75-32/34/36, R78-10 fields, R58-12/R54-11 As Of, R75-41/42, 64 Sub-Stats.
- Technique required fields: R75-2, R76-3, R47-3, R75-6 triple counter, R17-2 test, R17-3 what nobody knows.
- Retired field formats: R8-13, R8-14, R14-8, R17-3-CODEX_LINE_ORDER, R18-3, R20C-39, R2-6/R1-2 Frontage/Sustain/Re-form, R75-3, character-sheet.md §X.
- Counter scope: R17-3-COUNTER_MANDATORY/R8-13 signature-only vs R12-3/R76-3 always.
- Estimate marks: R75-44 (est.) vs R76-6; R57-07 pending.
- Source order: R20C-32 vs R44-5, R56-5, R58-14, R52-08, R14-2, R14-8 flag; wotr-stat-line.
- 64 Sub-Stats/XP: R75-28, R75-39, R75-41, R38-2.
- Three-rung ladder as gate: R75-26, R75-27.
- Preset figures: R75-11 marks, R75-35, R75-9, R75-12, R71-32, R71-28, R75-10.
- Codex first vs character first: R18-2 vs R7-1, R17-4; R18-7 Check 39; R13-3.
- Explaining bans: R8-11, R10-2 Category default + read.
- Gloss rights field R20C-49.
- Crystal print on first hold R75-5 vs no readouts in fights.
- Voice block slots R52-03, R75-32, R75-34 arc kind, R75-36 comic bank, R75-42 next gate.
- R52-25 stress shortening.
- Sonzai ownership: R20C-16 "Isaac's" vs R79-1 other creator; R1-1 list.
- Card skeleton: desktop/templates/CHARACTER_CARD_TEMPLATE.md (untracked; says English shout) vs character-sheet.md; mcp_server.py:1380 Cozbi reference.
- G1: R75-33, R75-43, R75-45, R75-47, R8-3, R8-4, R7-5; "sixth edition" guide missing (R12-8, R13-9, R14-8, R75-43); Notion R13-9, R18-4, R76-4, R20C-32; R18-6 /mnt/project path; dupes R54-11/R58-12, R1-2/R2-6, R12-3/R17-3/R47-3.

## Stats, items, mass combat
- Drafts refill: R78-10 vs R2-6-REPLENISHMENT_RULE, R61-101, R2-6-MAGAZINE_RULE, R60-03.
- Card outlier vs band: R44-1 vs R54-9, R56-10, R57-13, R78-10.
- Deciding-row notes: R14-3-TRACEABILITY, R71-7, R71-24, R71-19, R71-38, R71-62, R71-67, R74-20, R72-27; TR5.
- Stat Ledger: R14-7, R14-6-CHECK29, R71-6, R71-34, R71-35, R60-03.
- Stacking cap: R78-10, R75-12, R71-32, R71-38, R39-4, R45-3; stack line on card.
- Stage gap vs Grade: R78-10, TR5, R14-3, R71-41, R78-6.
- Estimates: R14-2-ESTIMATE_MARKING, R14-6-NUMBERS_GREP, R71-64, R75-44, R70-99, R20C-34; canon on use vs on archive.
- Ratification: R20C-34 vs R61-103, R71-31, R75-19, R61-104.
- Drain unit: R78-10 duration vs R47-4, R46-4, R14-7, R71-62, R57-25.
- Tell ladder fixed wording (R78-10).
- Faculty read in fight: R71-44 vs R70-79 vs R79-6.
- Items toolbox: R70-48, R71-79, R71-76, R71-73, R71-84; price on page R70-48 vs R70-95, R71-78.
- Ammo tiers: R11-3-AMMO_TIERS, R20C-22 vs R46-2/3, R71-93, R45-3, R46-1, R71-91, R71-50.
- Mass-combat word floors R1-3-WORD_FLOOR, R54-17 (retire under R79-1).
- Fields: R1-2-THREE_FIELDS, R2-6-FRONTAGE, R57-07, R13-9 weapon, R47-5 rung.
- Mass leftovers: R71-59, R3-9-COSTED_OUT, R3-9-BEFORE_AFTER_DURING, R70-106, R1-4 vs R54-20, R71-16 roleplay wounds short.
- Gap-fill pass: R13-5, R71-25, R71-14.
- Discord adjudication cards: R72-37, R72-40.
- Journey clock R72-29; scaling vocab R13-6-SCALING_VOCAB_RESTRICTED vs R15-4.
- G1: R14-5-BUILD_TERMS_LIST, R14-8 orders, R75-30, R75-44, R71-60, R71-77 poison line, R61-104; Notion R14-2, R20C-32, R14-8; R70-56 chain ceiling ref; R71-81 R70-86 ref; R70-30 digits (style default), keep R70-31.

## Worldbuilding, documents, naming
- Canon hierarchy order (RULINGS/directions; archived scenes; "Fifteen governs" stale).
- Stat source by field.
- Never-invent vs estimates canon on use (R76-6, R70-99, R57-07, R75-44).
- Document format (.docx /mnt/user-data/outputs, present_files).
- Author-notes headings at archive (R13-9, R14-7, R13-5, R73-33; keep R74-2 clue list).
- Warm-bond quota: R70-114, R73-36, R73-38, R74-37.
- Arc mandates (R78-7 wording "some die, some do not").
- Crews approval R78-10 vs R72-2/R79-1.
- Malphas kept hidden (unsourced; public pages name him; circle size).
- Death permanence R60-04 vs R78-7, R61-56.
- Mystic register "never as physics" R12-2, R11-2-MEASUREWRIGHTS vs R78-2.
- Invention fence (fixed system canon vs free).
- Inventory required fields R6-8, R70-45, R70-60, R73-22, R74-15, R71-77, R60-21, R53-12, R53-15.
- Per-scene world musts R53-09 weather/date, R53-17, R3-8.
- Something-departs mandates R70-75, R71-70, R12-4 document, R70-23 epigraph.
- Ledger/Front automatic world rules R71-97, R71-20, R71-101, R72-30, R73-31 (A1 silent upkeep answered).
- Fixed document forms R71-97 clause, R74-12, R70-25 glossary, R47-5 rung.
- In-world document voice R20C-37 vs R70-8, R61-65, R70-75.
- Tier numerals R47-7 vs R70-82, R61-106, R46-2, R70-74.
- Technique naming leftovers R8-26, R50-11, R8-22, R8-23, R8-13.
- Names for places etc R50-23, R20C-46, R50-22, R50-24, R50-25, R50-34.
- Büri sweep spent: R20C-3, R20C-5, R21-1, R21-4; Open Rulings page; NATALIE lines.
- Price table approval (imports/drafts/price-table.md).
- G1: Notion R13-9-NOTION_PHYSICS_LINE, R76-4, R20C-32; superseded Codex names R61-13, R61-99, R61-63, R61-3; spent orders R8-27, R20C-40, R8-4, R8-3, R75-44, R75-33, R57-26, R59-16, R61-9, R61-10, R61-127, R70-135, R71-102, R72-41, R73-40, R74-43, R75-43, R20C-59; absent guides; R70-126 Borin's brothers; R54-25 burial vs Kharven sky burial.
