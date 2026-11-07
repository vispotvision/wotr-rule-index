# AGENTS.md — working in wotr-rule-index

You are reading the map. Before doing anything read `CLAUDE.md` (the
constraints; they bind whatever tool you are) and then `CONTINUE.md` (the live
state, newest block first — it says what is in flight and what only Isaac may
decide). Isaac's standing direction: inside work he has asked for, make the
calls and state them; no "pending Isaac" placeholders.

## Shared WOTR memory

### GPT startup (Isaac's standing direction, 2026-10-11)

In every WOTR chat running on a GPT model, automatically call `natalie`, then
immediately call `natalie_gpt` (`mcp__wotr__natalie_gpt`). Read the complete GPT
overlay before answering or drafting. Do this even when `natalie` already
appends the overlay; never wait for Isaac to remind you. On matters it names,
`desktop/NATALIE.gpt.md` overrides the base Natalie prompt, including its
direction to act on writing requests instead of stopping at a Scene Menu.
Isaac's current direction remains first. If the connector is unreachable,
report that and stop; never substitute remembered WOTR instructions.

### Law reading before prose (Isaac, 2026-10-17, R79-2; the same for every model)

Every model loads the law the same lean way. Once a session,
before the first WOTR drafting or revision, read the whole live rulebook in
brief, one line per rule: `load_rules(tags=[], brief=True)`. Where a client
truncates long results, take it as `part=1` through the last part the header
names and read every part. A domain's full text is loaded the first time a
task touches it (`load_rules(tags=[...])`), and `rule(id)` pulls any rule whose
one line is not enough. The rulebook is never re-read after compaction. An
open docket item that touches the work is decided at the table and the writing
goes on (R79-2). A fetch is not a read; never claim coverage you have not done,
or a literary pass from the verifier.

After `CLAUDE.md` and the newest `CONTINUE.md` block, read `SHARED_MEMORY.md`.
Every session uses this same file for durable WOTR working
notes. Follow its update protocol; model-private memory is not the shared record.

## What this is

War of the Realms (WOTR) is Isaac's fiction world; this repo is its desk.

- **The rule index.** Every craft rule from the twenty amendment packs and the
  standalone amendments as one YAML row each under `rules/`, `verbatim` quoted
  from `sources/` (read-only canon), each with a `status`. Rulings Isaac made
  directly (`rules/doc-*-ruling.yaml`) have `source.file: ""` and quote the
  wiki page or the `RULINGS.md` entry that recorded them; `wotr-mcp validate` accepts
  that and skips the quote-matches-source check for such rows (1,171 rows in 17
  files on 2026-11-04). It fails a live one whose quote is in neither
  `RULINGS.md` nor the wiki, so editing a quoted wiki passage means updating the row. `rules/` is the work;
  `sources/` is untouchable.
- **The wiki** (`wiki/`, the Obsidian vault and the source since 2026-10-15; Notion
  is retired and frozen, never written) and **the scene
  archive** (`scenes/`, 87 scene files, one marked superseded; `MANIFEST.md`,
  `ARCS.md`, `CAST.md`, `TIMELINE.md`).
- **The table** (`table/`): Fronts as clocks, the Ledger, the NPC roster, the
  session log. `table/*.yaml` is the source of truth; the "Running
  Pieces" pages (files under `wiki/The Table — Running Pieces/`) are
  Natalie's prose copies, and that folder also holds the table's **Docket**
  (`Open Rulings — The Docket.md`) — the rulings Isaac still owes.
  Four POVs have a State of Play page: Sodoku Moto (Kharven), Hild Ice
  (Kharven-Seat), Kwon Mu-jin (Hon-guk), Ilthára Korvaeth (New World); those
  pages are retired since 2026-10-17, historical and no longer maintained, and
  the archived scenes are the current state.
  `table/fronts.yaml` knows two thread strings, "Kharven thread, the year
  after" and "New World, the Korvaeth War". `session_start` takes the POV
  name; `fronts`, `due`, `roster` take the culture word. Some characters have
  more than one card in play (Sodoku Moto: the Volume I card and the Level-500
  "Arctic Lion" page); the thread's latest archived scene says which; check
  before you trust `fow_line`.
- **WOTR MCP** (`rust/`, binary `rust/target/release/wotr-mcp`) — what `.mcp.json`, Claude
  Desktop (`build/install_mcp.sh`) and the public route run; every tool is native. All new
  code, fixes and tests go in Rust (`CLAUDE.md`). Tool names, descriptions and schemas live in
  `rust/tools.json`, kept by hand (Isaac, 2026-11-04); nothing generates it. Any tool runs without
  an MCP client: `wotr-mcp call TOOL '{json args}'`. `table/*.yaml` is written by
  `rust/src/pyyaml.rs`, byte-identical to PyYAML. The semantic search embeds queries with the
  bge-small ONNX model on the venv's ONNX Runtime and reads `build/index/`. Narration runs
  through `wotr-mcp audio`: Kokoro and Supertonic in-process, MP3s through the venv's lameenc
  LAME (it loads libpython3.14 for that library's symbols, so a Python upgrade drops narration
  to WAV until fixed). The public route is `wotr-mcp http` (the `wotr-mcp-public` unit): named
  API keys, each with its own token and tool permissions, made and watched at the dashboard
  http://127.0.0.1:8790/ (this PC only, never funneled); keys in `~/.config/wotr/mcp_keys.json`.
  **The check after a change:** `cargo test --release --bins --tests` in `rust/`. The
  `rust/*_parity.py` harnesses compare Rust against the old Python tools, so a Rust-only fix
  shows there as an expected difference: read the diff, and don't port the fix back.
  The rule index gate (`wotr-mcp validate`, `resolve`) and the machine's jobs (`wotr-mcp backup`,
  `nightly`, `book-next`, `hook`, and `tool NAME args`, the positional command line for the book
  pipeline's agents) run here too.
  So does the Discord bot (`wotr-mcp bot [--sync]`, `rust/src/bot/`, on serenity); it reads
  `bot/config.yaml` and `bot/namebank.yaml`, and `bot/run.sh` starts it.
- **Not ported yet, still Python: run it, don't extend it.** `build/sync.sh` with `embed_index.py`;
  the Chatterbox and Qwen GPU workers, the Whisper read-back check and `--qwen` runs.
  Research also calls external CLIs (Agent Reach, agent-browser).
- **The automation:** the wiki autosave every 15 minutes, 03:30 nightly checks, 02:00 book
  dispatcher, Sunday backup, the Discord bot, a public
  read-only MCP behind a shared secret. All systemd user units (below).

## The wiki and the public site (since 2026-10-15)

- **Source:** `wiki/` is the Obsidian vault. Links are `[[vault/path|Title]]` by full
  vault path. Every section is filed into **shelves**: sub-folders with a front page
  named after the folder (`X/X.md`), and a hub page always sits inside its own folder,
  never beside it. A new page goes on the shelf it belongs to; a new shelf gets a front
  page with a one-line intro and a card list (`- [[path|Title]]: one line`).
- **Write it as markdown that breathes:** a blank line between paragraphs, sections as
  `##`, a blank line before a table, no Notion-style one-paragraph-per-line blocks.
  Mermaid charts are fine in the vault; the site redraws them as its own art.
- **The site** (https://vispotvision.github.io/wotr-rule-index/) is Quartz, built by
  `.github/workflows/site.yml` on any push to `wiki/**`, `site/**` or `rust/site/**`. The
  builder is its own crate, `rust/site/` (`wotr-site <out_dir>`), so CI skips the MCP's dependencies:
  - `src/main.rs` copies public pages only (manifest `private`, frontmatter
    `private: true`, or an all-private folder; character cards, scenes, techniques and
    the Table never publish) and dresses them: a plate per page, a painted banner per
    section and shelf front page, card grids for link lists, glossary cards for runs
    of `**Term**: meaning`, paragraph breaks, long quotes set as prose;
  - `src/art.rs` draws the plates and banners, and `src/tables.rs` holds the crests,
    section styles and `FOLDER_ART` (painting per shelf, from `wiki/Assets/Paintings/*.webp`,
    embedded at the top of each hub page);
  - the diagrams are hand-kept SVG: edit or add `wiki/Assets/Diagrams/*.svg` directly and
    embed one with `![[Assets/Diagrams/name.svg]]`;
  - `src/charts.rs` redraws mermaid: a chain becomes a gilt road, a timeline era
    bands, anything branching gilt plaques laid out by Graphviz;
  - the sidebar order is the `sortFn` list in `site/quartz.config.yaml`: add a new
    shelf's name there.
- **Local preview:** `./build/site.sh` (Quartz clone in `~/.cache/wotr-quartz`).
- **Isaac's own:** the character cards are personal to him; never reorganize, restyle
  or publish them.

## Layout

```
sources/      the amendment corpus. READ-ONLY. never edit, reformat or rename.
rules/        one YAML per pack, standalone document or standing ruling — the index
schema/       rule.schema.json, applies_to.md (the closed tag vocabulary), pack notes
out/          wotr-mcp resolve output: rules.resolved.json, rules.live.md, rules.live.full.md, docket.md
wiki/         the wiki, an Obsidian vault (the source); .manifest.json flags private pages;
              wiki/Assets/Diagrams = the SVG art. Public pages build to the site (below)
site/         the public site: quartz.config.yaml, custom.scss, landing.html, assets/ (paintings)
scenes/       the archive; scenes/cast/ = speaker-tagged cast files for narration
table/        fronts.yaml ledger.yaml npcs.yaml sessions.yaml (+ FRONTS.md LEDGER.md NPCS.md rendered);
              voices.yaml here = voice fingerprints for voice_check (narration presets are build/voices.yaml)
build/        the Python not yet ported, the shell scripts, build/systemd/ (the units), casting/, voices/
app/          the WOTR Workshop's front end (static/; the server is `wotr-mcp workshop`): each player's own library
              of characters, techniques, items, lore, places, factions with images; Natalie runs
              on the player's own AI (key stays in their browser) with the MCP's read tools wired in
bot/          the Discord bot — deterministic, no LLM, no dice in canon channels, writes
              role-gated to the Judger (bot/PLAN.md); the rule/docket/conflict commands were
              dropped on Isaac's call (ROADMAP.md, Phase F0). bot/queue/ = Judger proposals
book/         the book pipeline: book/design/BOOK_PIPELINE.md; one folder per book (kharven-year/)
proposals/    proposed rules awaiting a pack   reports/  audits, digests   imports/  conversions
desktop/      NATALIE.md — what the Claude Desktop project reads; COWORK.md — what Claude
              Cowork (Desktop's folder mode) reads (~/Claude/CLAUDE.md links to it)
.claude/      skills (wotr-rules, wotr-ops, judger; the writing set: wotr-write, wotr-rp,
              wotr-npc, wotr-phenomenon, wotr-wound, wotr-stat-line, wotr-ledger, wotr-name,
              wotr-technique, wotr-lookup, wotr-start; wotr-book drives the book pipeline; the MCP
              serves them all through skill() and as prompts); Workflow scripts (book-chapter.js, judger-assist.js)
              — the Workflow scripts run only in Claude Code; other agents use wotr-mcp tool
.mcp.json     registers WOTR MCP for Claude Code sessions here (the Rust binary)
rust/         the WOTR MCP and all new code: src/, tests/, tools.json, *_parity.py
CLAUDE.md CONTINUE.md ROADMAP.md CONFLICTS.md RULINGS.md PROGRESS.md BRIEF.md README.md
```

Gitignored but real: `build/index/` (semantic search), `build/models/`,
`vault/` (the Obsidian view), `build/.mcp_token`, the logs.

## This machine (Linux since 2026-09-14)

Host `Ultron`, user `oridon`, Arch Linux (Omarchy); repo at `~/wotr-rule-index`;
what lived outside it on Windows is in the private `~/wotr-vault`
(`true-canon/` = the base craft guides and their dated editions).

- **One interpreter, for the Python not yet ported:** `~/.venvs/wotr/bin/python` (3.14). `python` in this
  file means that one; the system `python` has none of the packages.
  Safest form: `bash build/py.sh build/<tool>.py …` (sources the config, runs
  the venv). `. build/env.sh` also puts it first on `PATH` but exports the
  secrets into your shell — use `py.sh` when you don't need them.
- **The GPU venvs** are separate, one per engine, on a mise Python 3.12 with
  AMD's ROCm 10 torch (`torch 2.13.0+rocm10.0.0`, index
  `stable.repo.amd.com/rocm/whl-next/`, `[device-gfx1201]`): `wotr-comfy`
  (ComfyUI), `wotr-cb-gpu` (Chatterbox), `wotr-qwen` / `wotr-qwen-fast`
  (Qwen3-TTS VoiceDesign), `wotr-cosy` (CosyVoice), `wotr-supertonic` (ONNX,
  CPU). Each has a `build/<engine>_setup.sh`; each is reached through
  `common.venv_python("<name>")` by its worker, never imported into the
  project venv. ROCm presents the card as `cuda:0`; the 7800X3D's iGPU is
  `cuda:1`, so anything that picks a device picks by name or pins device 0.
  No render/video group is needed on Arch (`/dev/kfd` is mode 666).
- **One config file:** `~/.config/wotr/env` (mode 600; template
  `build/wotr.env.example` lists every key: the three secrets, `HF_TOKEN`,
  `WOTR_REPO` / `WOTR_PYTHON`, the paths `WOTR_TRUE_CANON` / `WOTR_VENVS` /
  `WOTR_DRIVE` / `WOTR_BACKUP_DIR`, `WOTR_MCP_PUBLIC_URL`, the switches
  `WOTR_BOOK_OFF` / `WOTR_NIGHTLY_NO_CLAUDE`). Shell scripts read it
  via `build/env.sh`, Python via `common.load_env()`, units via
  `EnvironmentFile=`. Isaac fills it with `bash build/secrets.sh`. Never print
  it, never write a secret into it for him, never paste a secret into a chat.
- **Units** (`build/systemd/`; `bash build/systemd_setup.sh` installs,
  `--status` is read-only, `--remove` uninstalls):

  | unit | when | runs |
  |---|---|---|
  | `wotr-sync.timer` | every 15 min | `build/sync.sh` — the wiki autosave: mirrors `scenes/` into `wiki/The Scene Archive/Scenes`, copies `table/` pages in, commits `wiki/` `table/` `scenes/CAST.md` `scenes/TIMELINE.md` and pushes **only if something changed** (a push to `wiki/**` republishes the site) |
  | `wotr-nightly.timer` | 03:30 | `build/nightly.sh` — checks, headless Claude note, commit |
  | `wotr-book.timer` | 02:00 | `build/book_dispatch.sh` — one chapter if no gate waits |
  | `wotr-backup.timer` | Sun 03:00 | `build/backup.sh` — zip to Drive or `~/wotr-backups` |
  | `wotr-mcp-public.service` | always | `rust/target/release/wotr-mcp http` on 8765 and 8767 (the Funnel's `/` and `/ro`), every request gated by a dashboard key; the dashboard on 127.0.0.1:8790 (enabled by `build/mcp_public_setup.sh`, not the installer; replaced wotr-mcp-readonly 2026-11-04) |
  | `wotr-bot.service` | always | `bot/run.sh` → `wotr-mcp bot` |
  | `wotr-comfy.service` | always | ComfyUI (`~/comfy/ComfyUI`, venv `wotr-comfy`) on 127.0.0.1:8188, the 9070 XT only (`--cuda-device 0`); enabled by `build/comfy_setup.sh`, not the installer |

  Did something run? `systemctl --user list-timers 'wotr-*'` and
  `journalctl --user -u wotr-<name>.service -u wotr-<name>.timer --since -3h`,
  plus the scripts' own files: `build/sync.log`, `nightly.log`,
  `book_dispatch.log`, `backup.log`, `mcp_public.log`,
  `bot/.bot.log`. A quiet hour leaves no sync commit; the journal is the proof.
- Anything needing `sudo` (pacman, docker, tailscale, groups) is Isaac's to
  run: give him the command in a `bash` block.

## Commands

```bash
# the index — the validation gate must PASS before any pack is "done"
rust/target/release/wotr-mcp validate
rust/target/release/wotr-mcp resolve                     # regenerates out/
rust/target/release/wotr-mcp call load_rules '{"tags":["combat","adjudication"]}'
rust/target/release/wotr-mcp call rule '{"id":"R15-2-ONE_TEST"}'

# any tool without an MCP client, JSON arguments; plain text search is grep over rules/ or out/rules.live.full.md
rust/target/release/wotr-mcp call session_start '{"thread":"Sodoku Moto","scene_type":"duel","culture":"Kharven"}'
rust/target/release/wotr-mcp call load_rules '{"tags":["prose-law","combat","pov"],"brief":true}'
rust/target/release/wotr-mcp call character '{"name":"Amelia Greymane"}'
rust/target/release/wotr-mcp call due '{"culture":"Kharven"}'
rust/target/release/wotr-mcp call scene_context '{"draft":"the text of a draft or a beat"}'   # the lorebook
rust/target/release/wotr-mcp verify draft.md --combat
rust/target/release/wotr-mcp tool loadout duel                # the tags for a scene type
rust/target/release/wotr-mcp book-next --json                      # where the book stands (read-only)

# these do the real thing — sync commits and pushes the wiki, nightly runs headless
# Claude and commits, book_dispatch pulls --rebase --autostash even with --dry-run,
# backup writes a zip. To check on them, read the journal and logs above; don't run them.
bash build/sync.sh   bash build/nightly.sh   bash build/book_dispatch.sh [--dry-run]   bash build/backup.sh

# Isaac's decisions — run only on his word
rust/target/release/wotr-mcp book-next --approve 1              # or --reject 1 --note "..."
python build/judger_apply.py <scene-slug>          # list proposals; then P01 P03 ... to apply the ids he names

# the MCP itself
(cd rust && cargo build --release)        # build the Rust MCP; .mcp.json runs rust/target/release/wotr-mcp --ops
rust/target/release/wotr-mcp verify draft.md --combat
(cd rust && cargo test --release --bins --tests)   # the check after a change; must pass
bash build/py.sh rust/parity.py           # Rust vs the old Python; a Rust-only fix shows as an expected difference
rust/target/release/wotr-mcp http        # the public route + key dashboard, what the unit runs

# operations — Isaac's, or on his word: they (re)install and restart the live units
bash build/setup_linux.sh                 # fresh machine: venv, config, units
bash build/systemd_setup.sh               # (re)install the units; --status is the read-only form
bash build/install_mcp.sh                 # register with Claude Desktop (app closed)
bash build/mcp_public_setup.sh            # secret + unit + Tailscale Funnel + the URL
```

## Before writing any WOTR prose

The rules are the point of this repo; never write a scene, sheet, technique or
name from memory of "how WOTR works". Scene types: `duel | battle | talky |
quiet | explicit | working | standard` (`loadout <type>` prints the tags; an
unknown type silently returns `standard`). The closed tag vocabulary and what
each tag means is `schema/applies_to.md`.

1. `session_start "<POV>" <type> <culture>` — the loadout, the Docket, what
   comes due, the Fronts and the thread's last (historical) State of Play, in
   one call, for the model's eyes only: nothing from it is printed as a recap
   (R79-2).
2. `load_rules` with the loadout's tags (`prose-law` for any prose; rules
   print newest first, standing rulings included, and the newer governs where
   two overlap), the full text of a domain on its first use, then
   `check_docket` with the same tags. **The index's docket
   (`check_docket`, `out/docket.md`) is the current open list.** The wiki's
   "Open Rulings — The Docket" page is Natalie's copy and lags: a letter there
   that a later pack ratifies (Pack Twenty did for several) or that
   `RULINGS.md` closes is not open. What is genuinely open and touches the
   scene is decided at the table and the writing goes on (R79-2).
3. `character` and `fow_line` for anyone named, once per scene; `scene_brief`
   for the fill-in template, set pieces only (R79-2); `scene_context <file>` (or `scene_recall "<moment>"`) for the
   cards and the prior scenes on the same ground. `codex "<term>"` for any
   glyph, spell, formula or Wellspring the
   scene will work: The Master Codex read from the xlsx (Pack Eighteen 4a).
4. After drafting: one `verify_scene` / `wotr-mcp verify` a turn, every FAIL
   fixed, WARNs read but not looped (R79-2); every finding carries a
   rule id or a Table Rule number; `codex_check` for
   Pack Eighteen checks 37-39; `voice_check` for a line that must sound
   like its speaker.
5. At the table, when a scene ends Natalie archives it with `archive_scene`
   and keeps the Ledger, Fronts and NPC roster current in the background
   (`session_end`, `ledger_add`, `advance_front`, `npc_set`), nothing printed
   unless he asks (R79-2 as refined 2026-10-17); there is no State of Play
   rewrite. `log_ruling` records Isaac's rulings and agent rulings.
   `create/update_character` (card changes, new techniques, Level points) run
   on Isaac's word only; the Judger's queue still goes through
   `build/judger_apply.py` with the ids he names. `propose_rule` files a
   proposal for a later pack and is ordinary work when he has asked for one.
6. A ruling made in play goes to `RULINGS.md` and is applied to `rules/*.yaml`
   later, in an index session, one commit per ruling batch, then `wotr-mcp validate`
   and `wotr-mcp resolve`. Never edit `rules/` from a prose session.

Stats, items and techniques come from ratified tables (the wiki's Living
System pages, `RULINGS.md`), never invented; an ambiguous source means `null`
and a log line, not a guess. A name only has to sound right for its culture,
the element banks are reference (R79-7), and in play Natalie invents texture,
places, words and minor people where nothing on file covers them, canon once
in an archived scene (R79-4). An NPC with no card gets a roster entry
(`npc_set`, kept quietly), not a card you make up; a beat that would reopen a
closed Front is Isaac's call.

## Rules of the road

`CLAUDE.md`'s constraints hold as written (read-only `sources/`; `verbatim` is
exact source text; conflicts recorded in `CONFLICTS.md`, never resolved — a
`supersedes` link is set only where the pack text itself says so in quotable
words; nothing invented; stop at phase ends; the validation gate). In addition:

- **Two writers, and three robots.** The sync (hourly) commits `wiki/`,
  `table/`, `scenes/CAST.md` and `scenes/TIMELINE.md`
  wholesale; the nightly commits `reports/nightly.md`, `prose_pass.md`,
  `recurrence.md`, `reconcile.md`, `build/.nightly_state.json` and `out/`; the
  dispatcher commits `book/`. All three `git pull --rebase --autostash` first,
  so uncommitted edits in those paths get swept into their commits: `git pull
  --rebase` before you edit, commit your own files promptly, one pack per
  commit, and don't commit changes in their paths that you didn't make.
- **What never leaves this machine.** Pages flagged `private` in
  `wiki/.manifest.json` stay off every export and shelf. The `/t/<secret>/…`
  URLs and the two token files are never printed, posted or committed.
  Art Isaac selects goes on the wiki as chosen, credited (RULINGS.md, 2026-11-05;
  the `art-drop` skill and `~/wotr-art-drops/`); a voice modelled on a real
  person is for Isaac's own listening only (`ROADMAP.md`, the casting rule).
  The base craft guides in `~/wotr-vault/true-canon` are never overwritten:
  a change is a new dated edition beside the original, with a changelog.
- **Claude Cowork** is Claude Code run by Claude Desktop, with the app's
  connectors (Drive, Trello, Gmail; Notion is frozen and never written) beside the MCP. `desktop/COWORK.md`
  binds it: a connector reads freely and writes canon on Isaac's word only,
  through the MCP writer where one exists; `CLAUDE.md` and this file are never
  rewritten as "folder instructions".
- **Natalie in Claude Code** is the clone at `~/wotr-natalie` opened in the
  app's Code tab. Its `.natalie` marker (gitignored) turns on the two hooks in
  `.claude/settings.json` (`wotr-mcp hook`): SessionStart pulls, then
  puts NATALIE.md in context; Stop runs
  the Rust verify on every reply over 120 words and blocks it with the FAIL list
  until it is fixed. The coding checkout has no marker, so the hooks exit at
  once here. This is the one surface where the rules are enforced rather than
  requested; the Desktop project (`desktop/PROJECT_INSTRUCTIONS.md`) still
  only asks.
- **Frozen:** the narration engines (nothing new until one engine holds Gimbzo
  across three renders — `ROADMAP.md`). Don't build toward it. The engines themselves are installed
  and proven on this machine since 2026-09-14 (`~/.venvs/wotr-{cb-gpu,qwen,
  qwen-fast,supertonic,cosy}`, Kokoro's files in `build/models/`, the
  reference clips in `build/voices/refs/`); the freeze is on new voice work,
  not on rendering a scene with what stands.
- **End of session:** `wotr-mcp validate` → `wotr-mcp resolve` → commit → push → tick
  `ROADMAP.md` (and `PROGRESS.md` after a pack) → append a dated block at the
  top of `CONTINUE.md`; never rewrite an older block.
