# AGENTS.md — working in wotr-rule-index

You are reading the map. Before doing anything read `CLAUDE.md` (the
constraints; they bind whatever tool you are) and then `CONTINUE.md` (the live
state, newest block first — it says what is in flight and what only Isaac may
decide). Isaac's standing direction: inside work he has asked for, make the
calls and state them; no "pending Isaac" placeholders.

## What this is

War of the Realms (WOTR) is Isaac's fiction world; this repo is its desk.

- **The rule index.** Every craft rule from the twenty amendment packs and the
  standalone amendments as one YAML row each under `rules/`, `verbatim` quoted
  from `sources/` (read-only canon), each with a `status`. Rulings Isaac made
  directly (`rules/doc-*-ruling.yaml`) have `source.file: ""` and quote the
  wiki page or the `RULINGS.md` entry that recorded them; `validate.py` accepts
  that and skips the quote-matches-source check for such rows (33 rows in 17
  files), so those quotes rest on your care alone. `rules/` is the work;
  `sources/` is untouchable.
- **The wiki mirror** (`wiki/`, ~590 pages from Notion) and **the scene
  archive** (`scenes/`, 87 scene files, one marked superseded; `MANIFEST.md`,
  `ARCS.md`, `CAST.md`, `TIMELINE.md`).
- **The table** (`table/`): Fronts as clocks, the Ledger, the NPC roster, the
  session log. `table/*.yaml` is the source of truth; the Notion "Running
  Pieces" pages (mirrored under `wiki/The Table — Running Pieces/`) are
  Natalie's prose copies, and that folder also holds the table's **Docket**
  (`Open Rulings — The Docket.md`) — the rulings Isaac still owes.
  Four POVs have a State of Play page: Sodoku Moto (Kharven), Hild Ice
  (Kharven-Seat), Kwon Mu-jin (Hon-guk), Ilthára Korvaeth (New World).
  `table/fronts.yaml` knows two thread strings, "Kharven thread, the year
  after" and "New World, the Korvaeth War". `session_start` takes the POV
  name; `fronts`, `due`, `roster` take the culture word. Some characters have
  more than one card in play (Sodoku Moto: the Volume I card and the Level-500
  "Arctic Lion" page); the thread's State of Play says which — check before
  you trust `fow_line`.
- **WOTR MCP** (`build/mcp_server.py`, 45 tools) — what Claude Desktop
  ("Natalie"), Claude Code (`.mcp.json`), the Discord bot and the book pipeline
  use. **Without an MCP client, 21 of the read-only tools are a command line:**
  `python build/book_tools.py <tool> …` (bare = the list; `verify_scene` is
  `verify` there). `stale_names`, `scene_text`, `cast_index`, `pack_impact`,
  `narration_status`, `trello_cards` and every writer need the MCP. One
  command-line tool writes: `voice_fingerprints` rebuilds `table/voices.yaml`,
  which the sync commits — don't run it idly.
- **The automation:** hourly Notion sync, 03:30 nightly checks, 02:00 book
  dispatcher, Sunday backup, the Discord bot, a job runner n8n calls, a public
  read-only MCP behind a shared secret. All systemd user units (below).

## Layout

```
sources/      the amendment corpus. READ-ONLY. never edit, reformat or rename.
rules/        one YAML per pack, standalone document or standing ruling — the index
schema/       rule.schema.json, applies_to.md (the closed tag vocabulary), pack notes
out/          build/resolve.py output: rules.resolved.json, rules.live.md, rules.live.full.md, docket.md
wiki/         Notion mirror (build/notion_export.py); .manifest.json flags private pages
scenes/       the archive; scenes/cast/ = speaker-tagged cast files for narration
table/        fronts.yaml ledger.yaml npcs.yaml sessions.yaml (+ FRONTS.md LEDGER.md NPCS.md rendered);
              voices.yaml here = voice fingerprints for voice_check (narration presets are build/voices.yaml)
build/        every tool, the shell scripts, build/systemd/ (the units), casting/, voices/
bot/          the Discord bot — deterministic, no LLM, no dice in canon channels, writes
              role-gated to the Judger (bot/PLAN.md); the rule/docket/conflict commands were
              dropped on Isaac's call (ROADMAP.md, Phase F0). bot/queue/ = Judger proposals
book/         the book pipeline: book/design/BOOK_PIPELINE.md; one folder per book (kharven-year/)
n8n/          docker-compose.yml (host networking), WOTR_nightly.json, README.md
proposals/    proposed rules awaiting a pack   reports/  audits, digests   imports/  conversions
desktop/      NATALIE.md — what the Claude Desktop project reads; COWORK.md — what Claude
              Cowork (Desktop's folder mode) reads (~/Claude/CLAUDE.md links to it)
.claude/      skills (wotr-rules, wotr-ops, judger; the writing set: wotr-write, wotr-rp,
              wotr-npc, wotr-phenomenon, wotr-wound, wotr-stat-line, wotr-ledger; wotr-book drives
              the book pipeline); Workflow scripts (book-chapter.js, judger-assist.js)
              — the Workflow scripts run only in Claude Code; other agents use book_tools.py
.mcp.json     registers WOTR MCP for Claude Code sessions here
CLAUDE.md CONTINUE.md ROADMAP.md CONFLICTS.md RULINGS.md PROGRESS.md BRIEF.md README.md
```

Gitignored but real: `build/index/` (semantic search), `build/models/`,
`vault/` (the Obsidian view), `build/.jobs_token`, `build/.mcp_token`, the logs.

## This machine (Linux since 2026-09-14)

Host `Ultron`, user `oridon`, Arch Linux (Omarchy); repo at `~/wotr-rule-index`;
what lived outside it on Windows is in the private `~/wotr-vault`
(`true-canon/` = the base craft guides and their dated editions).

- **One interpreter:** `~/.venvs/wotr/bin/python` (3.14). `python` in this
  file means that one; the system `python` has none of the packages (and
  `validate.py`'s own error would tell you to pip-install into it — don't).
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
  | `wotr-sync.timer` | hourly | `build/sync.sh` — Notion → `wiki/`, index, vault, publish (it publishes `scenes/*.md` from the working tree, committed or not); commit+push **only if something changed** |
  | `wotr-nightly.timer` | 03:30 | `build/nightly.sh` — checks, headless Claude note, commit |
  | `wotr-book.timer` | 02:00 | `build/book_dispatch.sh` — one chapter if no gate waits |
  | `wotr-backup.timer` | Sun 03:00 | `build/backup.sh` — zip to Drive or `~/wotr-backups` |
  | `wotr-jobs.service` | always | `build/jobs_server.py` on 127.0.0.1:8799 (n8n's door) |
  | `wotr-mcp-public.service` | always | `mcp_server.py --public` on 8765 (read-only, token; enabled by `build/mcp_public_setup.sh`, not the installer) |
  | `wotr-bot.service` | always | `bot/run.sh` → `bot/main.py` |
  | `wotr-comfy.service` | always | ComfyUI (`~/comfy/ComfyUI`, venv `wotr-comfy`) on 127.0.0.1:8188, the 9070 XT only (`--cuda-device 0`); enabled by `build/comfy_setup.sh`, not the installer |

  Did something run? `systemctl --user list-timers 'wotr-*'` and
  `journalctl --user -u wotr-<name>.service -u wotr-<name>.timer --since -3h`,
  plus the scripts' own files: `build/sync.log`, `nightly.log`,
  `book_dispatch.log`, `backup.log`, `.jobs_server.log`, `mcp_public.log`,
  `bot/.bot.log`. A quiet hour leaves no sync commit; the journal is the proof.
- **n8n** runs from `n8n/docker-compose.yml` (`cd n8n && docker compose up -d`;
  UI `localhost:5678`; host networking so it reaches the job runner directly).
  If `WOTR_nightly.json` is ever activated there, `systemctl --user disable
  --now wotr-nightly.timer` so the nightly does not run twice.
- Anything needing `sudo` (pacman, docker, tailscale, groups) is Isaac's to
  run: give him the command in a `bash` block.

## Commands

```bash
# the index — the validation gate must PASS before any pack is "done"
python build/validate.py
python build/resolve.py                     # regenerates out/
python build/query.py --applies-to combat adjudication --format full
python build/query.py --id R15-2-ONE_TEST --format full

# read-only tools without the MCP (bare = the list); plain text search is grep over rules/ or out/rules.live.full.md
python build/book_tools.py
python build/book_tools.py session_start "Sodoku Moto" duel Kharven    # loadout + docket + ledger + fronts
python build/book_tools.py load_rules prose-law combat pov --brief
python build/book_tools.py loadout duel                                # the tags for a scene type
python build/book_tools.py character "Sodoku Moto"     due 1 Kharven     fronts Kharven
python build/book_tools.py scene_context beat.md       # the lorebook for a draft or a beat — write it to a file first
python build/verify.py draft.md --combat --culture Kharven --band set-piece
python build/book_next.py --json                      # where the book stands (read-only)

# these do the real thing — sync publishes to Notion and pushes, nightly runs headless
# Claude and commits, book_dispatch pulls --rebase --autostash even with --dry-run,
# backup writes a zip. To check on them, read the journal and logs above; don't run them.
bash build/sync.sh   bash build/nightly.sh   bash build/book_dispatch.sh [--dry-run]   bash build/backup.sh

# Isaac's decisions — run only on his word
python build/book_next.py --approve 1              # or --reject 1 --note "..."
python build/judger_apply.py <scene-slug>          # list proposals; then P01 P03 ... to apply the ids he names

# the MCP itself
python build/mcp_server.py                # stdio, all 45 tools (what .mcp.json registers)
python build/mcp_server.py --public       # read-only + token, what the unit runs

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
   comes due, the Fronts, the State of Play, in one call.
2. `load_rules` with the loadout's tags (`prose-law` for any prose; rules
   print newest first, standing rulings included, and the newer governs where
   two overlap), then `check_docket` with the same tags. **The index's docket
   (`check_docket`, `out/docket.md`) is the current open list.** The wiki's
   "Open Rulings — The Docket" page is Natalie's copy and lags: a letter there
   that a later pack ratifies (Pack Twenty did for several) or that
   `RULINGS.md` closes is not open. What is genuinely open and touches the
   scene is Isaac's before you draft.
3. `character` and `fow_line` for anyone named; `scene_brief` for the fill-in
   template; `scene_context <file>` (or `scene_recall "<moment>"`) for the
   cards and the prior scenes on the same ground.
4. After drafting: `verify_scene` / `build/verify.py` — every finding carries a
   rule id or a Table Rule number; `voice_check` for a line that must sound
   like its speaker.
5. Nothing is archived by an agent. `archive_scene`, `log_ruling`,
   `ledger_add`, `advance_front`, `npc_set`, `create/update_character` write
   to Notion and git on Isaac's word only — through Claude Desktop, the bot, or
   `build/judger_apply.py` with the ids he names. `propose_rule` files a
   proposal for a later pack and is ordinary work when he has asked for one.
6. A ruling made in play goes to `RULINGS.md` and is applied to `rules/*.yaml`
   later, in an index session, one commit per ruling batch, then `validate.py`
   and `resolve.py`. Never edit `rules/` from a prose session.

Names, stats, items and techniques come from ratified banks and tables (the
wiki's Living System pages, `RULINGS.md`), never invented; an ambiguous source
means `null` and a log line, not a guess. An NPC with no card gets an
`npc_set` proposal through the Judger's assistant, not a card you make up; a
beat that would reopen a closed Front is Isaac's call.

## Rules of the road

`CLAUDE.md`'s constraints hold as written (read-only `sources/`; `verbatim` is
exact source text; conflicts recorded in `CONFLICTS.md`, never resolved — a
`supersedes` link is set only where the pack text itself says so in quotable
words; nothing invented; stop at phase ends; the validation gate). In addition:

- **Two writers, and three robots.** The sync (hourly) commits `wiki/`,
  `table/`, `scenes/CAST.md`, `scenes/TIMELINE.md` and `build/.notion_publish.json`
  wholesale; the nightly commits `reports/nightly.md`, `prose_pass.md`,
  `recurrence.md`, `reconcile.md`, `build/.nightly_state.json` and `out/`; the
  dispatcher commits `book/`. All three `git pull --rebase --autostash` first,
  so uncommitted edits in those paths get swept into their commits: `git pull
  --rebase` before you edit, commit your own files promptly, one pack per
  commit, and don't commit changes in their paths that you didn't make.
- **What never leaves this machine.** Pages flagged `private` in
  `wiki/.manifest.json` stay off every export and shelf. The `/t/<secret>/…`
  URLs and the two token files are never printed, posted or committed.
  Reference-only art is never embedded on the wiki; a voice modelled on a real
  person is for Isaac's own listening only (`ROADMAP.md`, the casting rule).
  The base craft guides in `~/wotr-vault/true-canon` are never overwritten:
  a change is a new dated edition beside the original, with a changelog.
- **Claude Cowork** is Claude Code run by Claude Desktop, with the app's
  connectors (Notion, Drive, Trello, Gmail) beside the MCP. `desktop/COWORK.md`
  binds it: a connector reads freely and writes canon on Isaac's word only,
  through the MCP writer where one exists; `CLAUDE.md` and this file are never
  rewritten as "folder instructions".
- **Natalie in Claude Code** is the clone at `~/wotr-natalie` opened in the
  app's Code tab. Its `.natalie` marker (gitignored) turns on the two hooks in
  `.claude/settings.json` (`build/natalie_hook.py`): SessionStart pulls, then
  puts NATALIE.md and the brief prose-law loadout in context; Stop runs
  `verify.py` on every reply over 120 words and blocks it with the FAIL list
  until it is fixed. The coding checkout has no marker, so the hooks exit at
  once here. This is the one surface where the rules are enforced rather than
  requested; the Desktop project (`desktop/PROJECT_INSTRUCTIONS.md`) still
  only asks.
- **Frozen:** the narration engines (nothing new until one engine holds Gimbzo
  across three renders — `ROADMAP.md`) and any design where n8n calls Claude
  itself (needs an API key that doesn't exist; n8n triggers the host's jobs
  instead). Don't build toward either. The engines themselves are installed
  and proven on this machine since 2026-09-14 (`~/.venvs/wotr-{cb-gpu,qwen,
  qwen-fast,supertonic,cosy}`, Kokoro's files in `build/models/`, the
  reference clips in `build/voices/refs/`); the freeze is on new voice work,
  not on rendering a scene with what stands.
- **End of session:** `validate.py` → `resolve.py` → commit → push → tick
  `ROADMAP.md` (and `PROGRESS.md` after a pack) → append a dated block at the
  top of `CONTINUE.md`; never rewrite an older block.
