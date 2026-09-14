# wotr-rule-index: inventory for an automated book pipeline

Read-only survey, 2026-09-12. Repo: `C:\Users\isaac\Documents\wotr-rule-index`.
Token figures are estimates: chars/4 for rule text, words x 1.35 for prose.

## 0. Infrastructure facts that shape the pipeline

**MCP server** `build/mcp_server.py` (1,556 lines, 44 tools via `@server.tool`, `MCPServer("WOTR MCP")`).

| mode | command | transport | auth | tools |
|---|---|---|---|---|
| stdio (Claude Desktop) | `python build/mcp_server.py` | stdio | none | all 44 |
| HTTP for n8n | `python build/mcp_server.py --http [--port 8765]` | streamable HTTP, binds **127.0.0.1**, path `/mcp` | none | all 44 |
| public | `--public` (= `--http --read-only --token`) | same, wrapped in `with_token_gate` | `Authorization: Bearer <secret>` or path `/t/<secret>/mcp`; secret from `WOTR_MCP_TOKEN` or `build/.mcp_token` (>=16 chars) | 27 `READ_ONLY_TOOLS`; the 17 writing tools are removed via `server.remove_tool` before serving; `/t/<secret>/audio/<arc>/<scene>.mp3` serves narration with Range support |

Flags: `--port` (default 8765), `--read-only`, `--token`, `--base-url` (default `https://ultron.tailf1bfa3.ts.net`, used only to build audio links), `--log <file>`. DNS-rebinding protection is disabled in token mode. `NOTION_TOKEN` is read from env, falling back to HKCU\Environment.

**Right now port 8765 is taken by the public server**, not the plain `--http` one: scheduled task `WOTR MCP public` (Running) = `pythonw.exe build/mcp_server.py --public --port 8765 --log build/mcp_public.log`. So an n8n MCP Client node pointed at `http://host.docker.internal:8765/mcp` today gets 401 without the secret, and with the secret gets only the 27 read-only tools (no `archive_scene`, no table writes, no `sync_now`). A full-tool HTTP server for the pipeline needs `--http --port <other>` as a second process, or the writing done outside the MCP (CLI scripts / git). `--http` binds loopback; from the n8n container `host.docker.internal` works on Docker Desktop for Windows (`extra_hosts: host-gateway` is set in the compose), but this has not been tested against the repo — the README claims it, nothing in the repo has exercised it.

**n8n instance** — exists, outside the repo:
- `C:\Users\isaac\Documents\n8n\docker-compose.yml`: services `n8n` (n8nio/n8n:latest, :5678, `N8N_HOST=localhost`), `qdrant` (:6333), `open-webui` (:3000), `pipelines` (:9099). Env in the n8n container: `COMFYUI_HOST=host.docker.internal:8188`, `OLLAMA_HOST=host.docker.internal:11434`, `QDRANT_HOST=qdrant`. Nothing there references the MCP server or the repo.
- `docker ps`: all four containers Up 18 hours. Host is listening on :5678 (n8n), :11434 (Ollama), 127.0.0.1:8765 (public MCP).
- Existing n8n workflows live in `C:\Users\isaac\Documents\ComfyUI-n8n-Automation\`: `ingest_workflow.json` ("WOTR - Ingest Page to Qdrant"), `query_workflow.json` ("WOTR - Ask the Wiki"), `crawl_workflow.json` ("WOTR - Full Wiki Crawl and Ingest") — webhook -> code -> httpRequest chains doing RAG over the Notion wiki with Qdrant + Ollama (`nomic-embed-text`, `dolphin-llama3`). Two open-webui Pipelines: `wotr_rag_pipeline.py` ("WOTR Lore Assistant"), `wotr_creative_pipeline.py` ("WOTR Creative Writer", with a ComfyUI portrait step). None of it touches the rule index, the verifier, or the scene archive.
- Inside the repo n8n is mentioned only in `README.md:150-151`, the `mcp_server.py` docstring, `build/query.py:2` ("This is what the n8n context step calls"), and `PROGRESS.md:240` (an encoding bug flagged "for whoever wires up the n8n pipeline"; `query.py` now does `sys.stdout.reconfigure(encoding="utf-8")`, so that one is patched). No `n8n/` folder, no workflow JSON, no launch config.

**Rule index shape** (`build/common.py`, `schema/`): one YAML per pack in `rules/`; rule keys `id, title, pack, pack_number, section, source, kind, status, ratified, summary, verbatim, applies_to, amends, supersedes, notes, verification`. `applies_to` is a closed vocabulary of 20 tags (`schema/applies_to.md`). Totals now: **599 rules, 487 live, 4 pending, 2 proposed**, rest superseded. `build/validate.py` (verbatim must appear in `sources/`), `build/resolve.py` (writes `out/`), `build/query.py --applies-to ... --format brief|full|json`.

---

## 1. Tools grouped by pipeline stage

### Stage: BRIEF (assemble the context for a chapter)

| tool | signature | reads | returns / size |
|---|---|---|---|
| `session_start` | `(thread, scene_type="standard", culture="Kharven")` — thread matched against State of Play page titles: 'Sodoku Moto', 'Hild Ice', 'Kwon Mu-jin', 'Ilthára Korvaeth'; scene_type one of `duel battle talky quiet explicit working standard` | `wiki/The Table — Running Pieces/*.md` (State of Play, The Ledger, Fronts, Open Rulings — live from Notion when the token works, else the mirror), `table/fronts.yaml`, `table/ledger.yaml` via `table.due(2)`, `desktop/inventories/<culture>.md` or the Kharven block in `desktop/NATALIE.md`, `rules/` | 7 blocks joined by `---`; Running Pieces are 142–727 words each (~0.2–1k tok), Fronts-as-clocks ~2.8k tok, inventory ~0.7–1.7k tok, then the **brief loadout for the scene type (12–19k tok)** and an unratified count. Whole thing ~20–27k tok. |
| `scene_brief` | `(beat, thread="", scene_type="standard", culture="Kharven", characters=[])` | rules, inventory (pulls the `**Recurrence…:**` line), `fow_line()` per character (first 12 lines) | The pre-write template: 9 numbered blanks (POV = least-knowing R5-C1; knows/wrongly believes/reader knows; ignorance quota R6-3; misreading R6-4; the cost; the lie; two Standing Inventory items R6-9; the ending; length band) + 4 duel/working blanks (vocabularies R1-1, the read R12-3, two explaining voices R12-4, deciding stat R14-3) or 3 battle blanks (Single Act R2-5, name-three R1-3, practitioner POV R3-9); FOW lines; first 60 brief rules; unratified count; the loop instruction "draft → verify_scene → post → archive_scene". ~5–8k tok. |
| `scene_menu` | `(thread, culture="Kharven")` | fronts (closest to ticking), `due(1)`, `scenes/CAST.md` (characters in <=2 scenes), inventory recurrence line | Three hooks; the third is left for the model to write. <0.5k tok. |
| `load_rules` | `(tags: list[str], status=["live"], brief=False)` | `rules/*.yaml` live | Rules sorted newest pack first; unknown tags ignored and named. Sizes below. |
| `rule` | `(id)` | rules | One rule full. |
| `check_docket` | `(tags)` | rules with status pending/proposed | Only 6 such rules exist now; <1k tok. |
| `list_conflicts` | `()` | `CONFLICTS.md` | 3,778 words (~6.3k tok), whole file. |
| `wiki` | `(query, full=True)` | `wiki/**/*.md` (583 pages, 915k words), keyword rank (`_rank`: title bonus, phrase bonus, coverage) | Top 5 with 3 snippets of 220 chars each, plus full text of the top page capped at 14,000 chars (~3.5k tok). Mirror is up to an hour behind Notion. |
| `character` | `(name)` | wiki, stem/parent match, prefers Character Cards | Card text capped 24,000 chars (~6k tok). 257 cards, median 1,214 words (~1.6k tok), max 6,265 (~8.5k). Key ones: Sodoku 2,037 w; Yoko 1,587; Lambert 4,333; Verinus 5,814; Cozbi 2,239; Hild 1,121. |
| `fow_line` | `(name)` | `character()` | Only the numeric lines (Level/Stage/Band, stat table, Force and Flow, EU, η), capped 12,000 chars; says "no FOW figures" rather than inventing. |
| `scene_recall` | `(query)` | `scenes/*.md` keyword rank | Top 4 scenes, 4 snippets of 400 chars each (~1.5k tok). No embeddings, no entity index. |
| `fronts` / `due` / `roster` | `(thread="", include_closed=False)` / `(sessions_old=2, thread="")` / `(thread="")` | `table/*.yaml` | Read-only views of the table. `due()` depends on `sessions.yaml` count — currently `[]`, so nothing ever ages. `roster` is empty (`npcs.yaml` = `[]`). |
| `stale_names` | `(scope="all", max_files=60)` | Moto Reversion Ledger tables in `sources/`, `build/renames.yaml`, wiki + scenes | The Büri sweep, per file counts; nothing edited. |
| `timeline` | `()` | `scenes/TIMELINE.md` (exists, 90 lines; `placed` column is all `____`) | Returns the file; only creates a skeleton if missing. |
| CLI equivalents | `python build/query.py --applies-to combat pov --format full\|brief\|json` | rules | Same selection as `load_rules`; `--format json` is the machine-readable path for an n8n Code node. |

### Stage: DRAFT

**Nothing in the repo calls a model.** The draft is written by Claude in Claude Desktop under `desktop/NATALIE.md` (4,167 words, ~7k tok) or by Claude Code with the `wotr-rules` skill. The protocol NATALIE.md fixes: table rules 1–12 (turn shape, length bands conversational 300–700 / standard 700–1,500 / set piece 2,500+, NPC agency, adjudication without dice by named stat row, the read, the ledger, ignorance and lies, explicit scenes, body language, first-introduction inventory, lived-in rooms); tag picking (2–4 tags, always `prose-law`); read `rules.live.full.md` sections + `docket.md`; write; cite rule ids in author notes; canon hierarchy (Isaac > canon docs > packs, later beats earlier > Notion wiki > base guides > prior sessions); never invent numbers; label originated content pending. Author notes are expected to carry: originated content, canon conflicts, Phenomenon line, combat floor audit, Stat Ledger, narrative ledger, open questions, and the rule ids that constrained the piece. Only **36 of 87** archived scenes actually carry an author-notes heading.

An n8n pipeline therefore needs its own LLM node (Anthropic API, or Ollama at `host.docker.internal:11434` which is already running) with the loadout as system context; the MCP only supplies context and checks.

### Stage: VERIFY (mechanical)

`verify_scene(markdown, combat=False, culture="", band="standard")` → `build/verify.py` `run()` + `report()`. `python build/verify.py draft.md --combat --culture Kharven --band set-piece` exits 1 on any FAIL. "Nothing here judges quality; it counts." Checks, by the rule id each names:

| level | check | rule id |
|---|---|---|
| FAIL | any em/en dash or ` -- ` | AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE |
| FAIL | antithesis "not X but Y" (3 regexes), first 6 quoted | AI-tells §1 |
| FAIL / WARN | Ladder: two `was X and the Y was` clauses in one sentence / one | R6-1-LADDER_BAN, Check 18 |
| FAIL | countdown negation: 2+ short negated sentences then a `Just`/`Only` sentence | AI-tells §1 |
| WARN | 3+ Not/Never/And/Only fragments | AI-tells §1 |
| WARN | a named faculty (Cymorath, Kamigan, Shingan…) as grammatical subject of saw/read/mapped… | R6-2-FACULTY_NEVER_SUBJECT, Check 19 |
| WARN | gloss phrases ("which meant", "in other words"…) | R4-13-ZERO_BUDGET, Check 15 |
| WARN | emotional signposting ("he felt afraid") | AI-tells §4 |
| WARN | question in narration outside quotes | AI-tells §1 (hypophora) |
| WARN | 2+ similes in one paragraph | AI-tells §5 |
| WARN | tidy summary close (Ultimately/In the end/…) | AI-tells §2 |
| FAIL | reification (watchlist noun + motion verb) >=3 per scene; 2 in one paragraph | R4-15-TWO_PER_SCENE_BUDGET, R4-15-ONE_PER_PARAGRAPH, Check 17 |
| FAIL | three consecutive sentences >25 words | R4-14-CHAIN_CEILING |
| FAIL / info | >=4 "flat runs" (three sentences within 40% of each other) | R4-14-RUN_RULE |
| FAIL / WARN | sentences under 8 words <10% / <18% | R4-14-HARD_CEILINGS |
| WARN | paragraphs closing on three sentences >18 words | R4-14-HARD_CEILINGS |
| info / WARN | sentence-length CV; paragraph-length CV <0.35 = uniform blocks | R4-14, AI-tells §2 |
| WARN | word count outside band | Table Rule 2 |
| info | italic interior beats count; last line echoed | Table Rule 10; Table Rule 1 |
| FAIL | Kharven only: fewer than 2 of the 5 signature items (woodpile/stack, night-stone, wet wood, Thin Weeks, death-house/Waiting) | R6-9-RECURRENCE_RULE |
| WARN | combat=True: zero HEMA terms / zero anatomy terms | R13-6-HEMA_VOCAB check 22, R13-6-ANATOMY_VOCAB check 23 |

Caveats: recurrence regexes exist for Kharven only (the six other inventories in `desktop/inventories/` have no checks); the HEMA regex includes common words (point, cut, guard, cross, edge, void) so density is inflated; `prose_pass` auto-detects combat by `Vor|Nach|Indes|parry|riposte|blade|cut|thrust|wound`.

Other verify-stage tools:
- `gap_fill(markdown)` — Pack Thirteen §5's eight steps as a report: counts paragraphs with exchanges, causal connectives, Aether/Wellspring/Essence mentions, real-science terms, anatomy/HEMA counts, Mechanism Vocabulary; then the prose pass. Asks the question each step exists to ask (R12-3-COMBAT_EXCHANGE_OWES, R14-3-TRACEABILITY, R13-2-THREE_STRATA_MANDATE, R13-2-STRATUM_TWO_WELLSPRING, R13-4-COMBAT_FLOOR, R13-3-PHENOMENON_MANDATE, R13-9-STYLE_DIRECTIVE_MECHANISM_VOCAB, R13-5-GAP_FILL_PASS). Counts, not judgement.
- `voice_check(name, line)` / `voice_fingerprints()` — `build/voices.py`: per-character dialogue fingerprint (length, questions, contractions, first person) from the archive into `table/voices.yaml`; attribution heuristic (speech tag within 40 chars, else last name in the paragraph); characters with <8 lines are not fingerprinted.
- Archive-wide (`build/audit.py`, written to `reports/`): `prose_pass()` (verify over every scene, summary table), `recurrence_report()` (Kharven items per scene), `reconcile()` (duplicate wiki titles; Stage/Level within 80 chars of a first name vs the card; Wellspring named with the wrong Family), `pack_impact(markdown, name)` (live rules sharing 4+ distinctive 7+-letter words with new pack text), `timeline()`.

### Stage: REVISE

No tool. The loop in NATALIE.md and `scene_brief` is "fix every FAIL, read every WARN, never a single pass", done by the model by hand. There is no draft versioning (`archive_scene` appends a `_YYYYMMDD_HHMM` stamp on a slug collision; nothing tracks draft/revision state), no apply-findings step, no diff between passes.

### Stage: ARCHIVE (and the table)

| tool | signature | writes | side effects |
|---|---|---|---|
| `archive_scene` | `(title, markdown, author_notes="")` | `scenes/<slug>.md` (H1 added if missing; notes under `## Author notes` after `---`) | `notion_publish.py --only <file>` to the Notion Scene Archive; `git add` + commit "Archive scene: <title>" + `push origin master`. Returns path, word count, publish and push status. Not idempotent, no dry run. |
| `session_end` | `(thread, scene_markdown, rulings=[], notes="")` | `table/sessions.yaml` (+render, commit, push) | Regex-harvested candidate Ledger lines (injuries, debts, who-knows-what, reputation, lies), State of Play skeleton (last paragraph, questions, cast names from CAST.md), Front list, docket additions. Writes nothing to Notion pages. |
| `advance_front` / `set_front_clock` / `add_front` | `(front_id, what_happened, next_move="")` / `(front_id, ticks[])` / `(name, thread, want, ticks[], next_move="")` | `table/fronts.yaml`, `table/FRONTS.md` | each call = commit + push |
| `ledger_add` / `ledger_collect` | `(category, who, text, due_after_sessions=None, due_condition="")` / `(entry_id, how)` | `table/ledger.yaml`, `LEDGER.md` | commit + push |
| `npc_set` | `(name, thread, want, refusal_line, knows[], lied_about[], last_seen, voice)` | `table/npcs.yaml` | commit + push |
| `log_ruling` | `(rule_id, ruling, context="")` | `RULINGS.md` | commit + push; applied to YAML in a later Claude Code session |
| `propose_rule` | `(title, rule_text, applies_to[], rationale="", session="")` | `proposals/PROPOSED.md` | commit + push |
| `cast_index` | `(write=True)` | `scenes/CAST.md`; `scenes/ARCS.md` only if missing | no commit |
| `create_character` / `update_character` | `(name, markdown, volume, tags)` / `(name, markdown)` | Notion page + `wiki/<section>/<name>.md` + `wiki/.manifest.json` | commit + push |
| `sync_now` | `()` | runs `build/sync.ps1` (timeout 900 s) | Notion export → notion_publish → docs_export + arcs_export to `G:\My Drive\War of the Realms — Documents` → `git pull --rebase` → commit `wiki table scenes/CAST.md scenes/TIMELINE.md build/.notion_publish.json` → push. Scheduled task `WOTR wiki sync` (hourly, Ready). |

**Assembly** (not MCP tools; CLI only, or via `sync_now`):
- `build/arcs_export.py --out <dir>`: reads `scenes/ARCS.md` (H2 = arc, `- file.md` lines in order), writes one `.docx` and one `.epub` per arc plus a complete epub; only arcs whose scenes changed (`.manifest.json` in the output folder). Markdown → XHTML covers headings, paragraphs, emphasis, dividers (`⁂`), blockquotes.
- `build/docs_export.py`: one Word document per wiki section plus The Scene Archive and The Rule Index, title page + contents, into Drive.
- `scenes/ARCS.md` must be edited by hand to place a new scene; nothing appends to it after `cast_index` creates the skeleton. There is no "chapter" concept anywhere — the unit is the scene file.

### Stage: NARRATE

| tool | signature | does |
|---|---|---|
| `scene_text` | `(scene)` — file name, title, or unique substring (`_find_scene`; ambiguity returns candidates) | `audio_export.scene_blocks` → `plain_text`: `# Title`, paragraphs, `---` dividers; frontmatter, author/Notes block, images, links, emphasis stripped. Reports whether a cast file exists. |
| `cast_scene` | `(scene, script)` | Parses `[Name]` / `[Name: slow, beat]` tags (delivery words `slow slower fast faster quiet loud whisper beat "long beat"`; performed cues `[sigh] [laugh] [chuckle] [gasp] [cough] [clear throat] [sniff] [groan] [shush]` kept in-line), `check_cast` requires the tag-stripped text to equal the scene text character for character and the divider counts to match; saves `scenes/cast/<stem>.cast.md`; lists speakers with no `build/voices.yaml` entry (they get a stable `_pool` pick). |
| `narrate_scene` | `(scene, voice="narrator")` | `subprocess.Popen(python build/audio_export.py --scene <file> --voice <voice> --out <dir>)`, detached; job appended to `build/.narrate_jobs.json` (last 40), log `build/.narrate-<id>.log`. Output dir `G:\My Drive\War of the Realms — Documents\Arcs\Audio` if Drive is mounted else `docs/audio`. Estimate 18 words/s (~5x real time on the 7800X3D). Unchanged scene+voice is skipped. |
| `narration_status` | `(job="")` | Job states (starting/running/done/failed from the log tail) and every rendered `.mp3`/`.wav` with a path, or a `/t/<secret>/audio/...` URL in public mode. |

`build/audio_export.py` (572 lines): Kokoro-onnx 82M (model files ~350 MB in `build/models/`, `--fetch-model`), CPU by default (DirectML optional); `build/pronounce.json` respelling lexicon; `build/voices.yaml` presets (`narrator: af_heart`, blends `a:0.6,b:0.4`, `.npy` style vectors in `build/voices/`, or `engine: chatterbox` entries with `speed/gain/ref/exaggeration/cfg/model`); Chatterbox via `build/chatterbox_backend.py` + `chatterbox_worker.py` in its own venv (`chatterbox_setup.ps1`). Pauses: 0.55 s paragraph, 1.4 s divider, 1.0 s after title, 0.12 s between voices in a paragraph. Flags: `--fetch-model --list-voices --dry-run --plain --check-cast --scene --voice --out --max-minutes --no-cast`. Processes the archive in `ARCS.md` order. **Only one cast file exists** (`scenes/cast/02_verinus_testament_of_the_sixty_fifth.cast.md`). `table/voices.yaml` is the fingerprint file, a different thing from `build/voices.yaml`.

---

## 2. The table (`table/`)

- `fronts.yaml`: 12 Fronts (11 open, 1 closed) in 2 threads, "Kharven thread, the year after" and "New World, the Korvaeth War"; each has `id, name, thread, status, want, last_move, next_move, clock[{tick, consequence}] (4–5 ticks), position (all 0), last_advanced (None)`. 2,092 words. Rendered `FRONTS.md`.
- `ledger.yaml`: 29 lines, 28 open, categories `the dead | injuries and reserve | debts | who knows what | reputation | canon conflicts on the ledger (blocking)`; `due` is a session count (1–3) or a condition. 1,149 words. Rendered `LEDGER.md`. Four blocking canon items on it (R14-A Stage names — since ruled; the Accord circle's name; the Onawa collision; whether Ilthára said the name).
- `npcs.yaml`: `[]`. `sessions.yaml`: `[]` → `session_count()` = 0, so `due()` returns "nothing older than N sessions" until `session_end` has logged sessions.
- `voices.yaml`: dialogue fingerprints (416 words).
- `build/table.py`: `load/save/render`, `seed` (parses the Notion Fronts/Ledger prose pages), `fronts_for`, `advance`, `set_clock`, `add_front`, `due`, `ledger_add`, `ledger_collect`, `roster`, `npc_set`, `session_log`.

## 3. The scene archive (`scenes/`)

- `MANIFEST.md`: 87 files, 343,191 words. Includes non-scenes: `00_SUPERSEDED_wrong_names.md` (4,230), `THE_KINGDOM_OF_KHARVEN_buri.md` (9,556, the stale twin of `_corrected`), `WOTR_AI_Writing_Tells_to_Avoid.md` (1,044); `audit.py`/`voices.py` skip these. Two long-form pieces dominate: `WOTR_Vaeloris_Sequence.md` 42,130 and `The_Path_of_Sorrow.md` 38,063. Median scene 3,235 words (~4.4k tok); the numbered Sodoku/Verinus/Aurelian/Darius/Mu-jin/Charles/Dabney scenes sit at 3,100–4,500; the Cozbi/Niran/Six Crows cluster at 600–2,600.
- `ARCS.md`: 9 arcs in reading order — The Kharven year (Sodoku Moto, 21 scenes), The Kharven-Seat (Hild/Wren/Charles/Dabney, 5), Verinus (7), Aurelian (5), Kwon Mu-jin (3), Darius (9), The New World — Ilthára Korvaeth (1), Cozbi/Niran/the Enclave (22), The Six Crows (5), Long-form and bloodline pieces (6). Set on 2026-09-12 from filenames; hand-edited thereafter.
- `CAST.md` exists (who appears where, mention counts). `TIMELINE.md` exists as a skeleton with the `placed` column entirely blank.
- 36/87 scenes carry an author-notes block (`## Notes (author-facing, not canon)` or `## Author notes`); the block is free prose, not a fixed schema.
- `scenes/cast/`: one file.

## 4. Live rule loadout sizes

Files in `out/` (regenerated by `build/resolve.py`; gitignored per PROGRESS but currently tracked-modified in git status):

| file | words | ~tokens |
|---|---|---|
| `out/rules.live.md` (id + summary, grouped by tag, rules repeated across tags) | 45,016 | ~78k |
| `out/rules.live.full.md` (+ verbatim quote) | 89,649 | ~145k |
| `out/rules.resolved.json` | 89,818 | ~192k |
| `out/docket.md` | 633 | ~1k |
| `CONFLICTS.md` | 3,778 | ~6.3k |
| `desktop/NATALIE.md` | 4,167 | ~7k |

Per tag, as `load_rules` returns them (live only, sorted newest pack first):

| tag | live rules | brief (id+summary) | full (+verbatim, amends, supersedes, notes) |
|---|---|---|---|
| prose-law | 117 | ~7.3k tok | ~17.9k tok (10,386 words) |
| combat | 59 | ~4.0k | ~8.9k (5,199 w) |
| pov | 38 | ~2.7k | ~7.7k (4,489 w) |
| dialogue | 66 | ~4.0k | ~9.0k (5,210 w) |
| scene-structure | 25 | ~1.5k | ~4.0k (2,351 w) |
| **union of those five** | **248** | **9,022 w ≈ 15.8k tok** | **21,734 w ≈ 37k tok** |

The seven built-in `LOADOUTS` (deduplicated across their tags):

| scene_type | tags | rules | brief | full |
|---|---|---|---|---|
| duel | prose-law combat adjudication magic-mechanism pov | 266 | ~18k | ~45k |
| battle | prose-law mass-combat adjudication pov scene-structure | 191 | ~12.5k | ~31k |
| talky | prose-law dialogue register pov naming | 286 | ~19.4k | ~45k |
| quiet | prose-law pov scene-structure standing-inventory register | 226 | ~14.4k | ~35k |
| explicit | prose-law dialogue pov scene-structure | 197 | ~12.3k | ~29.5k |
| working | prose-law magic-mechanism combat codex | 265 | ~17.8k | ~44.4k |
| standard | prose-law pov scene-structure dialogue register | 237 | ~14.9k | ~36k |

Other tags for reference (brief, rules-live.md section sizes): worldbuilding 112 rules ~9.1k; naming 86 ~7k; register 101 ~6.5k; magic-mechanism 96 ~6.7k; magic-design 72 ~4.9k; character-sheet 59 ~4.4k; verification 84 ~4.7k; stats 36 ~2.8k; mass-combat 38 ~2.6k; codex 35 ~2.5k; items 23 ~2.3k; adjudication 25 ~2k; documents 19 ~1.1k; standing-inventory 14 ~0.9k; session-protocol 10 ~0.6k.

## 5. Wiki mirror (`wiki/`)

583 pages, 915,601 words (~1.24M tok) — never loadable whole. Biggest sections: Volume V Character Cards 89 pages/118k words, Volume IV 96/103k, Volume I 49/82k, The Magic System 23/62k, The Disciplines 21/50k, Techniques 56/42k, Cosmology 12/31k. 257 character cards, median 1,214 words. Standing inventories in `desktop/inventories/`: accord 861 w, dawi 982, eresse 553, expanse 835, korvaeth 895, moto 1,255; Kharven inline in NATALIE.md (~330 w). Running Pieces pages: State of Play 142–680 w, Fronts 619, Ledger 727, Docket 427. Search is keyword ranking in Python (`_rank`), no index; each `wiki()` call rescans 583 files.

## 6. Context budget for one chapter draft (estimate)

| component | source | tokens |
|---|---|---|
| Protocol (NATALIE.md, or a trimmed pipeline system prompt) | `desktop/NATALIE.md` | 3–7k |
| Rule loadout, brief, five tags | `load_rules(brief=True)` | ~16k |
| — or full with verbatim | `load_rules()` | ~37k |
| Docket for the tags + relevant conflicts | `check_docket`, `list_conflicts` | 1–7k |
| Standing Inventory for the culture | `session_start` / inventories | 1–2k |
| Cards for 3–5 named characters (full) | `character()` | 5–15k |
| — or FOW lines only | `fow_line()` | 1–3k each |
| Setting lookups, 2–3 calls | `wiki()` | 7–10k |
| Continuity lookups, 2–3 calls | `scene_recall()` | 3–5k |
| Previous chapter(s) verbatim (median scene 4.4k) | scenes/ | 4–13k |
| State of Play + Fronts as clocks + Ledger due | `session_start` | 3–4k |
| Pre-write template | `scene_brief` (overlaps the loadout) | 2–3k without the rules |
| Output: standard turn / set piece / chapter at archive median | — | 1–2k / 3.5k+ / ~4.4k |
| **Total input, brief loadout** | | **~50–70k** |
| **Total input, full loadout** | | **~75–95k** |

The loadout is static per scene_type and the single largest block; it belongs in a cached system prompt, not re-sent per call. `session_start` alone is ~20–27k because it embeds the brief loadout; calling it and `scene_brief` and `load_rules` in one chapter triple-sends the same rules.

## 7. What is missing for a book-length run

1. **No planner / orchestrator.** Nothing produces a chapter outline, a book brief, or "the next chapter's beat". `scene_brief` requires a beat; `scene_menu` offers three hooks and leaves one to the model. Fronts have clocks with written tick consequences (a usable skeleton for a plot engine), but `position` is 0 on all twelve and nothing derives a chapter from a tick.
2. **No chapter-level continuity memory.** `scene_recall` is keyword search over the 87 files (Qdrant + `nomic-embed-text` exist in the n8n stack but hold the wiki, not the scenes, and the repo does not know about them). No entity/fact store per chapter (who is where, who knows what, injuries, time elapsed). `session_end` harvests candidates by regex only and writes nothing to the Ledger itself; `ledger_add` is one line per call, by hand. `TIMELINE.md` has every `placed` cell blank; `reconcile` catches only "Stage X"/"Level N" within 80 chars of a first name. NPC roster empty; sessions log empty, so the Ledger's ageing mechanism has never run.
3. **No critic pass.** `verify.py` counts patterns; `gap_fill` counts and asks questions; `voice_check` measures four statistics. There is no model-based judge for canon consistency, rule compliance beyond regex (author notes cite rule ids but nothing checks the citation), POV discipline (R5-C1, R6-3/6-4 blanks are filled in notes, never verified), the Single Act, the three-layer hit, or whether the scene's cost landed. The recurrence check exists for Kharven only.
4. **No revise step.** Findings are returned as text; there is no apply-fix loop, no draft versioning, no diff, no pass counter. NATALIE's "never a single pass" is a habit of the model, not a tool.
5. **No draft step in the repo.** No model call anywhere; the pipeline supplies its own LLM node. `build/query.py --format json` and the MCP over HTTP are the two ways to feed it context.
6. **No assembly for a book.** `arcs_export.py` compiles docx/epub by `ARCS.md` order, but only via CLI or `sync_now`, only into `G:\My Drive`, and only if someone has added the new scene's line to `ARCS.md` by hand. No chapter numbering, no front matter, no per-chapter manifest, no book-level word budget, no cross-chapter repetition or pacing check (`prose_pass` is per scene).
7. **Write tools are not pipeline-safe.** Every writing tool commits and pushes on each call (`archive_scene`, six table tools, `log_ruling`, `propose_rule`, `create/update_character`); a failed push is reported in the return string, not raised; no dry-run or batch mode; `archive_scene` does not check the draft against `verify_scene` first.
8. **Transport gap.** The plain `--http` server is not running; :8765 is the read-only public one. A pipeline that archives needs a second process on another port (`--http --port 8766`), untokened and loopback-only, reached from the n8n container via `host.docker.internal` (untested from the repo's side). The n8n MCP Client node exposes the tool list to an AI Agent node; 44 tools is a wide surface — a pipeline would pick per stage.
9. **Narration at book scale.** One cast file in 87; the whole archive is ~343k words ≈ 5.3 CPU-hours to render at 18 w/s and ~38 hours of audio; `pronounce.json` grows only as mangled names are noticed; voices for most named speakers are pool picks until `build/voices.yaml` names them.
10. **Verifier blind spots** that a pipeline will hit: HEMA regex counts everyday words; combat auto-detect in `prose_pass` is crude; `split_sentences` splits only before a capital/quote so dialogue-heavy scenes skew the variance stats; italics regex takes any `*…*` of 3+ words as an interior beat.
