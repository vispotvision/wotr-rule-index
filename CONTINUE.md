# CONTINUE — how to pick this work up cold

Read this first in any new session (scheduled or not). Isaac's standing
direction: inside work he has asked for, make the calls; no "pending" slots.
`ROADMAP.md` is the plan; this file is the live state. Newest block first;
append a dated block, do not rewrite older ones (two sessions write this repo
at once — `git pull` before editing, and commit only your own files).

## State on 2026-09-24 (writing skills in Claude Code)

**The seven claude.ai WOTR skills now live in the repo, adapted for Code.**
`.claude/skills/wotr-write` (+ references: scene-pipeline, technique-design,
character-sheet, prose-law-quickcheck, tools), `wotr-rp`, `wotr-npc`,
`wotr-phenomenon`, `wotr-wound`, `wotr-stat-line`, `wotr-ledger`. Same craft
content as the account skills; what changed: `mcp__wotr__*` names with
`build/book_tools.py` / `build/verify.py` fallbacks, drafts go to
`/tmp/wotr-drafts/`, sources are the `wiki/` mirror (the Stat Sheet workbook
is not in the repo: "workbook, unchecked"), and every writer
(`archive_scene`, `ledger_add`, `npc_set`, ...) is a proposal made on Isaac's
word, per AGENTS.md. The claude.ai account copies are unchanged and still
serve Desktop chat; a craft change should land in both. `~/wotr-natalie`
picks these up on its next pull.

## State on 2026-09-23 (the Magic System pass)

**Tiers 8/9 renamed and every open Magic System conflict ruled.** Tiers of
Standing 8 and 9 are Archmaster and Paragon; the retired lettered Coherence
Bands are gone from the Magic System pages (Stages read by Tier of Standing).
A cross-check fixed ~14 mechanical errors in Notion (units, speeds, stale
Sub-Stat names, tier slips); the Reader's Codex is current (Kagura Branch,
four Crafts, Level/Bands/Tiers). Isaac's questionnaire closed C-020..C-029
(R42-1..11) plus four follow-ups (R42-12..15), all applied in Notion
including ~75 cards (Dominion Stability → Gravity; Stage I–V cards
Unclassed). The Elven racial trait "Domain Stability" is NOT the Sub-Stat
and keeps its name. **Open:** Ryuka's Crystal field ("Dormant network,
awakening surface"); Kinjiki's η ~1.3 and Absolute Crystal at Stage XIV;
the Color of Essence Revelation cell has a pasted Part Five inside it;
lettered "Coherence Band" still on Technique pages and some cards outside
the Magic System.

## State on 2026-09-18 (the Instructions box)

**`desktop/PROJECT_INSTRUCTIONS.md` rewritten as an order of operations.** The
text in the Claude Desktop project's Instructions box was the pre-MCP version
(before `13171cc`): it named GitHub and Notion and nothing else. The repo copy
now says, in order: WOTR MCP first when present (local `wotr` in Claude
Desktop, all 45 tools; the public read-only connector, 25 tools, from
claude.ai web/phone) with the per-chat sequence (`session_start` → `load_rules`
+ `check_docket` before any prose → `scene_brief`/`scene_context`/`fow_line`
before drafting → `verify_scene` after, twice → the writers at the close, full
server only); then what each GitHub file is for and what lives in the repo but
not in knowledge (`sources/`, `desktop/inventories/`, `scenes/`, `table/`);
then Notion; then the never-skipped list. Header says which files go in
Knowledge. **Waits on Isaac's hands:** paste the text below the rule into the
project's Instructions box and re-sync Knowledge. NATALIE.md unchanged.

**Later the same day, the design inverted.** Isaac: Natalie still writes
without the rules. Cause: project Knowledge is retrieved in chunks, the box is
the only text always in context, and the box held a pointer. The box text now
carries the law itself (turn shape, length bands, the banned constructions,
numbers from `fow_line` only, the four voices, `verify_scene` before posting),
and `build/instructions_box.sh` builds the full paste (the box text plus
NATALIE.md below its first rule, 35 KB) at `~/wotr-instructions-box.md` and
puts it on the clipboard. If the box rejects the length, the box text alone
is the fallback. Still Isaac's hands: the paste, and confirming the `wotr`
tools show in the project chat at all.

**Evening: the enforced surface.** Isaac: "so fix it." The Desktop log
showed the server connected and answering (122 live prose-law rules) and
zero tool calls in the chat that drifted, so the model was simply not
calling. Built the one surface where it cannot skip: `build/natalie_hook.py`
+ `.claude/settings.json` (SessionStart injects NATALIE.md and the prose-law
brief; Stop verifies every reply over 120 words and blocks on FAIL, one
enforced revision per reply), gated on a `.natalie` marker so the coding
checkout is untouched. The clone `~/wotr-natalie` carries the marker; Isaac
opens it in the app's Code tab and that session is the table. Checked with
fake transcripts: no marker → silent; bad reply → block with the FAIL list;
clean reply → silent; `stop_hook_active` → silent. Not yet seen: a real
session in the Code tab (first open will ask to approve the project's
`wotr` MCP server from `.mcp.json`).

**Later: the manual verification.** Isaac asked what happened to it. The
2026-09-12 edition of the guide was in `~/wotr-vault/true-canon` only; the
scripts it names (`wotr_verify.sh` v4, `wotr_beat_check.py`, `wotr_terms.txt`,
`codex_check.py`) are on no disk here and never were in the repo. The guide
is now copied verbatim to `desktop/WOTR_Manual_Verification_Guide (2026-09-12 edition).md`
(vault copy stays the original), listed for project Knowledge, named in the
Instructions box and NATALIE.md with the honest coverage line (verify_scene =
checks 1-8, 10-13, 15-19, 22-23; the rest by reading), and injected by the
Code-tab SessionStart hook. Offered, not done: adding checks 28 and 42 as
FAILs and 9, 14, 41 as WARNs to `build/verify.py`.

## State on 2026-09-15 (Cowork)

**Claude Cowork has its instructions.** `desktop/COWORK.md` is the file: what
Cowork is on this machine (Claude Code run by Claude Desktop, with the app's
connectors and the `WOTR MCP`), where the work is, that it is not Natalie, the
connector rules (read freely; write canon on Isaac's word only and through the
MCP writers; private pages stay private; Drive/Trello/Gmail lines), the lines
that hold everywhere, and that `CLAUDE.md`/`AGENTS.md` are never rewritten as
folder instructions. `~/Claude` (Cowork's default folder, `coworkUserFilesPath`)
now exists with `CLAUDE.md` as a symlink to it; opened on the repo, Cowork reads
the repo's `CLAUDE.md` → `AGENTS.md` (new layout line and a "Claude Cowork"
bullet) → `COWORK.md`. Unverified until Isaac opens a Cowork session: whether
the repo's `.claude/skills` load there, and whether Cowork's own "update folder
instructions" writes through the symlink or replaces it (harmless either way).

## State on 2026-09-14 (midday: ComfyUI and the local TTS, on the card)

**Isaac asked for ComfyUI and the local TTS on Linux; both stand.** The one
unknown behind everything — a ROCm torch that sees the 9070 XT from a 3.12
venv — is settled: AMD's index (`stable.repo.amd.com/rocm/whl-next/`) serves
the exact Linux wheels the setup scripts pin (`torch 2.13.0+rocm10.0.0`,
cp312, `[device-gfx1201]`), and no `render`/`video` group was needed (Arch
ships `/dev/kfd` and `renderD*` mode 666; ROCm 7.2.4 came with
`ollama-rocm`). The card is `cuda:0`, the 7800X3D's iGPU is `cuda:1`.

**ComfyUI** (new on Linux; the Windows installs lost everything but their
metadata, kept in `~/wotr-vault/comfy`): `build/comfy_setup.sh` — clone at
`~/comfy/ComfyUI` (0.35.0), venv `wotr-comfy`, requirements with torch held,
the ten Windows workflows into the UI's list, and `wotr-comfy.service` on
127.0.0.1:8188 with `--cuda-device 0` (without it comfy-aimdo planned against
the iGPU's 31 GB). `--models` fetched what the workflows load and is free:
Z-Image Turbo bf16 + Qwen3-4B encoder + VAE, RealESRGAN x4, BiRefNet (20 GB,
in `models/`, no repo). First render: `text_to_image.json` as posted to
`/prompt`, 1024², 8 steps, 19.6 s cold. Not fetched: FLUX.2 dev (non-
commercial licence), Ideogram 4, Wan 2.2 (the video workflow) — add to
`comfy_models()` in the script if wanted.

**The engines**: every venv rebuilt by its own script as written (three
headers rewritten from UNTESTED to what happened): `wotr-supertonic` answers;
`wotr-cb-gpu` loads Turbo on `cuda:0`; `wotr-qwen` + `wotr-qwen-fast` both see
the card and the fast worker captures HIP graphs; `wotr-cosy` needed one fix
— `setuptools<81` for `pkg_resources` (now in `cosyvoice_setup.sh`) — and
loads Fun-CosyVoice3-0.5B on the card. Kokoro's files re-fetched
(`--fetch-model`), `requirements-audio.txt` installed into the project venv,
the CC-BY reference clips copied back from the vault to `build/voices/refs/`.
Kokoro read scene 02's cast (3 voices, 16.9 min) in 278 s on the CPU.

**One Gimbzo line, three engines, measured** (Whisper read-back clean on all
three; the anchor `line3_deep` is 63.2 Hz median / 57.3 floor): Chatterbox
Turbo on the VCTK clip 131 Hz; Qwen VoiceDesign from the brief 84.7 Hz,
cosine 0.37 to the anchor (anchor self-similarity 0.55), and the best-of-3
draw repeated half the line; CosyVoice cloning the anchor itself 71.6 Hz /
60.0 floor. One line each, not the gate — the freeze stands. Note for the
`cosy_worker`: it chdirs into the clone, so `ref` must be an absolute path.

**Docs**: AGENTS.md (unit row, a "GPU venvs" bullet, the freeze line says
the engines are installed), README (unit count, the engine paragraph, a
ComfyUI paragraph), ROADMAP Phase E (venvs ticked, ComfyUI added),
`systemd_setup.sh` (copies `wotr-comfy.service`, restarts it on change,
does not enable it — `comfy_setup.sh` does). `validate.py` PASS.

## State on 2026-09-14 (later that morning)

**Done since the port block below.** Isaac joined the docker group; n8n is up
from `n8n/docker-compose.yml` (container `n8n`, host networking — proven from
inside it: `wget http://127.0.0.1:8799/health` answers), and `WOTR nightly` is
imported (the CLI import needs an `id` field added to the JSON; the UI import
does not). The journal was purged, so the stray token line is gone everywhere.
The sync ran clean end to end with the new Notion secret at 06:24 (its one
standing note: `scenes/YOKO_MISHIRO.md` cannot be published until its Notion
parent is shared with the `oridon` integration). Headless Claude was proven
from a unit (`systemd-run --user`, 1.6 s, no MCP servers loaded — the
`--strict-mcp-config` flags do their job). The DNS wedge after `tailscale up`
(every lookup hung) was `systemd-resolved`; `sudo systemctl restart
systemd-resolved` cleared it.

**AGENTS.md.** New at the root: the working map for every coding agent (Codex,
OpenCode, Cursor, Copilot, Gemini, Claude Code) — layout, the Linux setup, the
commands, the prose protocol with the table's Docket in it, what the robots
commit, what never leaves the machine. `CLAUDE.md` points at it and is
otherwise unchanged. `build/book_tools.py` run bare now prints its tool list.
Checked by three agents (facts vs the tree, consistency vs the instruction
files, a fresh agent trying four tasks) and rewritten once on their findings.

**Still Isaac's, in n8n's UI** (`localhost:5678`): the owner account, the
`WOTR jobs` Header Auth credential (value: `build/.jobs_token`) on the three
HTTP nodes, the Discord webhook in "Send it to Isaac"; if the workflow is
activated, `systemctl --user disable --now wotr-nightly.timer`. Still owed
from the list below: Tailscale's `ultron` rename + operator flag (then the
public URL), Claude Desktop's `install_mcp.sh` with the app closed, Ollama,
rclone, the render/video groups.

## State on 2026-09-14 (the Linux port)

**The machine.** Windows was wiped overnight for Omarchy (Arch Linux, Hyprland,
systemd 261); the box is still `Ultron`, the user is `oridon`, the repo is
`~/wotr-rule-index`, and everything that lived outside it on Windows is in
`~/wotr-vault` (private repo: `true-canon/` is the old `WOTR True Canon` folder,
`claude/memory/` the old memory, `omarchy/CHECKLIST.md` the plan this session
carried out). Isaac's checklist step 11 was the brief: scripts to shell, tasks to
timers, `C:\` and `G:\` to config.

**What replaced what.** One interpreter, `~/.venvs/wotr/bin/python` (3.14; was
the Store 3.13). One config file, `~/.config/wotr/env` (mode 600; template
`build/wotr.env.example`; fill it with `bash build/secrets.sh`, never by pasting
into a chat) holding the three secrets and the paths — read by `build/env.sh`
(every shell script sources it), `common.load_env()` (every tool; the `winreg`
lookups are gone) and the units (`EnvironmentFile=`). Thirteen `.ps1` files
became `.sh` (same names, same logs, same commit messages, same exit codes) and
the five Windows tasks became systemd *user* units in `build/systemd/`,
installed by `build/systemd_setup.sh`: `wotr-sync.timer` (hourly, now with an
flock so a manual `sync_now` and the timer cannot overlap), `wotr-nightly.timer`
(03:30), `wotr-book.timer` (02:00), `wotr-backup.timer` (Sun 03:00), and the
daemons `wotr-jobs` (127.0.0.1:8799), `wotr-mcp-public` (8765), `wotr-bot`.
Linger is on, so they run without a desktop login. Logs: `journalctl --user -u
wotr-<name>` plus the scripts' own files. `bash build/setup_linux.sh` rebuilds
all of it on a fresh machine. The MCP reaches Claude Code through `.mcp.json`
(project-scoped; approve it once) and Claude Desktop through
`build/install_mcp.sh` (run with the app closed). n8n's compose is
`n8n/docker-compose.yml`, host networking, so it reaches the job runner at
`127.0.0.1:8799`. The TTS venvs are `~/.venvs/wotr-<engine>` and their five
`.sh` setups are untested ports (the narration freeze stands). Backups land in
`~/wotr-backups` until Drive is mounted (rclone; `WOTR_DRIVE`).

**Proven live on 09-14.** The nightly fired as a unit at 03:30 (the timer is
`Persistent=true` and caught up the slot the moment it was installed): checks,
headless Claude note, commit, push — `cfccaa5`. The bot is online
(`WOTR Bot#7139`) and came back on its own after a reboot; the job runner
answers `/health` and ran `book_dry` through n8n's route; the public MCP
answers on 8765 behind its new secret; the first sync with the new Notion
secret read 586 pages, all unchanged, and built the semantic index (11,092
chunks, 9 min once); the first backup zip is 23.7 MB with True Canon inside.
The port went through a 172-agent workflow: seven porters, a static battery, a
live integration run, five skeptics, two refuters per finding, per-unit fixes,
a re-check, a docs sweep (76 findings, 8 refuted, the rest fixed or handed to
this note).

**The secrets.** None were copied off Windows; all three were reissued tonight
(Discord reset, Notion refreshed; ElevenLabs still empty). Two pastes landed in
the chat and one at the shell prompt — the chat ones were reset again, the
shell one left a stray line in the env file that systemd echoed into the
journal 26 times; the line is gone, the journal purge and an optional third
Discord reset are on Isaac's list below.

**Not yet on Linux.** Tailscale is up but this node is `ultron-1` (the dead
Windows node holds `ultron`) and Funnel needs the operator flag — so the
public URL is not published; Docker's group is not joined, so n8n is not
running; Ollama and rclone are not installed; Claude Desktop has no `WOTR MCP`
entry yet. Each is one sudo line, listed under "Owed by Isaac".

## Owed by Isaac (do not decide these) — added 2026-09-14
- `sudo journalctl --rotate && sudo journalctl --vacuum-time=1s` (the stray
  token line in the journal); a third Discord token reset afterwards is
  optional (`bash build/secrets.sh DISCORD_TOKEN`).
- Tailscale: delete the offline Windows node `ultron` in the admin console,
  then `sudo tailscale set --hostname=ultron --operator=oridon`; then
  `bash build/mcp_public_setup.sh` publishes the MCP and prints the URL; put it
  in `WOTR_MCP_PUBLIC_URL` and restart `wotr-mcp-public`.
- Docker: `sudo usermod -aG docker oridon && sudo systemctl enable --now docker`,
  log out and in, then `cd n8n && docker compose up -d`; in n8n paste
  `build/.jobs_token` as the `WOTR jobs` Header Auth credential and import
  `n8n/WOTR_nightly.json`. If that workflow is activated, `systemctl --user
  disable --now wotr-nightly.timer` so nothing runs twice.
- Claude Desktop: quit it, `bash build/install_mcp.sh`, reopen.
- Ollama: `sudo pacman -S ollama-rocm && sudo systemctl enable --now ollama`.
- Drive, if wanted: rclone (`rclone config`, a remote `gdrive`, a mount), then
  `WOTR_DRIVE=` in the env file.
- The GPU engines, when the freeze lifts: `sudo usermod -aG render,video oridon`.
- Everything the 09-13 list below still owes (the Four Crafts items, Darius's
  card, the 43 Judger proposals, chapter 1's gate — `python build/book_next.py
  --approve 1` or `--reject 1 --note "..."`).

## State on 2026-09-13 (night)

**Rules and canon.** validate.py PASS. Docket empty; open conflicts: none
(C-008..C-019 ruled; RULINGS.md 2026-09-13). Pack Twenty extracted
(`rules/pack-20-twenty.yaml`); R20C-24/26/27 superseded on arrival by the
09-12 rulings. R38-2 re-cost applied to the seven sheets with a stated pool
(`build/recost.py`, `reports/recost_2026-09-13_applied.md`). Editions written
today in WOTR True Canon: Combat Craft Guide, Complete Magic System, Mechanism
of the Sixty, Character Template — the Combat guide's next pass owes a note at
the three superseded R20C rows. Six base guides still unfolded (ROADMAP).

**The table and the MCP.** `wiki` and `scene_recall` search by meaning
(`build/embed_index.py`, rebuilt by the sync). `scene_context(draft)` is the
lorebook (`build/lorebook.py`; `build/aliases.yaml` maps Darius → Ignatius's
card — the card should carry the name; Wren, Vaeloris, Ashgate, Cass Holloway
have no page). The Judger's assistant: `/judger <slug>` drafts the close as
proposals in `bot/queue/<slug>.judger.md|json`; `/judger apply <slug> P01 …`
runs only the ids Isaac names. First note written for
`08_sodoku_recalescence` (43 proposals, none applied — Isaac's call).

**The sync and backups.** `WOTR wiki sync` commits and pushes again (the dead
`.git/worktrees/agent-*` entries and ErrorActionPreference=Stop were the
cause; fixed 09-13). Private pages (Notion's "Information not on WIKI" tree,
114 pages) are stamped `private` in `wiki/.manifest.json` and never reach the
Drive shelf; the three documents that had reached it are removed. `WOTR
weekly backup` (Sunday 03:00, `build/backup.py`) now zips the WOTR True Canon
folder too — the one store that is in no git repository. `vault/` is the
Obsidian view (`build/vault_export.py`, hourly) — point Obsidian there.

**The bot** (`bot/`, PLAN.md): F0 lookups, `/scene save`, `/event`, `/verify`,
`/date`, the sheet checker, `/narrate` — 16 commands; the logon task "WOTR
bot" is registered and running. Thread reading and the auto-check wait on the
Message Content intent (Discord developer portal), then
`bot/config.yaml: intents.message_content: true`. Next for the bot: post
`bot/queue/*.judger.json` proposals in `#judger` as approve/set-aside cards
(contract in PLAN.md §9.3). `ELEVENLABS_API_KEY` unset; `/narrate elevenlabs`
cannot run until it is.

**Narration.** Frozen behind one gate (ROADMAP, "Where it stands"): Qwen is
locked behind `--qwen` (drift); nothing new on the voice roadmap until one
engine holds Gimbzo across three renders. CosyVoice is in flight in another
session (`build/cosy_worker.py`, uncommitted).

**The nightly.** `WOTR nightly` (03:30) runs `build/nightly.ps1`; the digest is
`reports/nightly.md`, shown by `session_start` while fresh. Its Claude step
waits on `claude /login` (the CLI is not signed in; Isaac's hands).

**n8n.** Running in Docker (compose at `C:\Users\isaac\Documents\n8n`, port
5678), with Ollama on the host at 11434 and the MCP's HTTP mode on 8765. It
cannot call Claude (no key) and cannot run anything on this machine (Linux
container, no repo mount), so the split is: n8n orchestrates,
`build/jobs_server.py` (logon task `WOTR jobs`, 127.0.0.1:8799) executes
named jobs, Claude Code thinks. `n8n/README.md` has the wiring;
`n8n/WOTR_nightly.json` is the first workflow, ready to import. The shared
secret is `build/.jobs_token` (gitignored, never in chat). **If a workflow is
activated, disable the matching Windows task so nothing runs twice.**

**The book.** `.claude/workflows/book-chapter.js` writes chapters in Claude
Code; the design is `book/design/BOOK_PIPELINE.md` (moved from `n8n/`; its
n8n transport needs an API key that does not exist - do not build toward it).
The dispatcher `WOTR book` (02:00, `build/book_dispatch.ps1`) writes one
chapter a night unattended: `build/book_next.py` decides, headless Claude
Code runs the workflow, the chapter lands under `book/` and is committed.
Gates are chapters 1-3, then every fifth, and the last. **Chapter 1 is
written and waiting: `python build/book_next.py --approve 1` or `--reject 1
--note "..."` - until Isaac answers, the dispatcher writes nothing.**
Two PowerShell traps learned here, and they bind any future script: a .ps1
must be saved UTF-8 **with BOM** or PowerShell 5.1 reads an em dash's third
byte as a smart quote and the file stops parsing; and a prompt must be piped
to `claude -p` on **stdin**, never passed as an argument, or PowerShell
strips its quotes. `Start-Job` also hung after its child exited - both
scripts call `claude` directly and let the task's ExecutionTimeLimit be the
timeout.

**Ideas.** `reports/ideas_2026-09-13.md`: 102 ideas, 66 survived the
skeptics, seven "Do next", the cut list. Done from it today: I03 (True Canon
in the backup), I06 (n8n moved), I08 (audit reports undated; heavy audits off
the public route), I09 (this file), I10 (private pages off the shelf), I12
(the narration freeze). Not done, with reasons: I01/I02 are the sync
session's; deleting `build/.venv-chatterbox` and `chatterbox_setup.ps1` waits
on Isaac. Still on the list: I93+I99 (sweep debt line in `session_start`),
I96 (`natalie_lint`), I13 (constraints as hooks), I23 (`inventory_add`), I54
(loudness master).

**Imports.** Trello conversion: all 200 converted; 196 published to Notion;
four Tovain stubs held by design (`reports/publish_imports_held.md`).

## Owed by Isaac (do not decide these)
- Three of the four Four Crafts items (R9-1): Law III's rewrite, the
  golden-age question, the Latinate/vernacular doublet's scope — the source
  document's Part Four docket text is needed before real options can be put.
- Darius's card: a "Called · Darius" line on Ignatius's card in Notion (or a
  card of his own) — until then `build/aliases.yaml` bridges it.
- The 43 proposals in `bot/queue/08_sodoku_recalescence.judger.md`.
- Whether to delete the CPU Chatterbox venv and its setup script (superseded
  by the GPU one; rebuildable).
- A Zettari forge-culture substrate pitch (Docket 18) is owed FROM Claude,
  not Isaac: he asked for a proposal drafted, mirroring the Dawi's Cask-Oath
  Pitch. Not yet written.

## History, folded
- 2026-09-12: inventories for six cultures landed (`desktop/inventories/`);
  the reader's codex drafted; the Trello conversion workflow ran to 200 with
  its review stage cut at Isaac's word; `build/publish_imports.py` written;
  eleven base guides folded into dated editions; narration built (four
  engines, cast files, the public audio route); the "Information not on WIKI"
  page was re-shared with the integration on 09-13 and the mirror is current.

## Every session ends with
`python build/validate.py` (must PASS) → `python build/resolve.py` → commit →
push → tick ROADMAP.md → append a dated block above.
