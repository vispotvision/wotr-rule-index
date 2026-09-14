# CONTINUE — how to pick this work up cold

Read this first in any new session (scheduled or not). Isaac's standing
direction: inside work he has asked for, make the calls; no "pending" slots.
`ROADMAP.md` is the plan; this file is the live state. Newest block first;
append a dated block, do not rewrite older ones (two sessions write this repo
at once — `git pull` before editing, and commit only your own files).

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
