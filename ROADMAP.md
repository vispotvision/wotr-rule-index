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

## Folding packs into base guides — eleven done, 2026-09-12

Isaac: "yes — start folding the packs in now." 18 base guides live at
`C:\Users\isaac\Documents\WOTR True Canon\` (now `~/wotr-vault/true-canon`;
`WOTR_TRUE_CANON`); each amendment rule names its
target guide in its `amends.guide` field. Eleven guides are done -- each
got a new dated edition alongside the original (never overwritten), with a
changelog listing every rule ID folded in and any judgment call flagged
rather than silently made. Every edition after the first four went through
a write → adversarial check → bounded fix → re-check loop, and the
changelog records each pass. (Drive for Desktop mirrors that folder: rapid
successive edits to one file can be rolled back to a stale snapshot — it
happened once — so write an edition in as few saves as possible and
verify the byte count after.)

- [x] `WOTR_Master_Style_Directive (2026-09-12 edition).md` — 86 amendments folded; 3 judgment calls flagged (a same-day narration-authority supersession applied despite falling outside the strict amends-field filter; a scope-narrowing read reconciling Pack Five vs. Twelve/Sixteen on prose texture; one non-target-guide clarification folded into the chemistry-ban text)
- [x] `WOTR_Ability_Technique_Design_Guide (2026-09-12 edition).md` — 56 amendments folded; 2 flagged (the legacy Corruption Vector field kept as non-mandatory pending a future pack; the naming-strike rule deferred to the Character Naming Guide rather than importing its content)
- [x] `WOTR_Character_Naming_Guide (2026-09-12 edition).md` — 47 amendments folded; reflects today's Ayame Yuno/Yasoshima rulings; C-005/C-006 (Zettai vs. Zettari) correctly left open, not guessed at; both ruled later that day and folded into the edition's changelog addendum (Zettari; the Zettari carved out of the Japonic stratum, R32-1)
- [x] `WOTR_Combat_Craft_Guide (2026-09-12 edition).md` — 29 amendments folded, plus the 7 live named-character combat assignments in the main body and the 2 still-proposed ones (Wren, Edward Lambert) in a clearly marked pending-review appendix

- [x] `WOTR_Scene_Writing_Process_Guide (2026-09-12 edition).md` — 21 rules folded; three review passes; one open tension surfaced and logged as C-008 (the per-NPC italic-thought standard vs. a locked narration distance)
- [x] `WOTR_Racial_Voice_and_Dialect_Guide (2026-09-12 edition).md` — 15 rules folded (the standalone amendment's 14 + Pack Fifteen's 1); new §8
- [x] `WOTR_Visual_Aesthetic_Guide (2026-09-12 edition).md` — 8 rules folded plus the ratified Moto material-culture rows (R34) as §5a; R11-1-REFERENCE_TRIANGLE cross-referenced, not folded (routed to Pack Nine, an index gap)
- [x] `WOTR_Dialogue_Craft_Standards (2026-09-12 edition).md` — 9 rules folded; seven unrouted Pack Nineteen rows listed in Appendix A, not folded
- [x] `WOTR_AI_Writing_Tells_to_Avoid (2026-09-12 edition).md` — 8 rules folded; Tell Bank entries defined only in the defining rules' own words
- [x] `WOTR_Manual_Verification_Guide (2026-09-12 edition).md` — base recovered from Downloads (2026-08-01 export); 23 rules folded as checks 15–42 with a "Script (v4)" line per check saying what `wotr_verify.sh` actually does; the script's own gaps (no checks 18, 19, 22–29; `--codex` failures never reach the summary line) flagged, not fixed
- [x] `WOTR_Mass_Combat_Craft_Guide (2026-09-12 edition).md` — base recovered from Isaac's Google Drive; 18 rules folded as new §12–§15 (naval, siege, cavalry, practitioner POV); §11 rewritten as the gaps page that records the closures

- [x] `WOTR_Item_and_Equipment_Writing_Guide (2026-09-12 reconstruction).md` — the base is lost everywhere (Downloads, Drive, Trello, the session bundle); rebuilt from its nine live rules, Pack Seven's description of what the original held (Amendment 7.10, as testimony, not law), and the 21 artifact pages' practice; four review passes (fidelity ×2, register, a last count check); §13 lists what the original had that nothing can restore. Isaac: "you might have to create it."

Remaining: the six base guides with 1-6 amendments each -- pick up in a
later session the same way (one agent per guide, same prompt shape, then the
check → fix → re-check loop).

## Narration — done 2026-09-12, growing

`build/audio_export.py` reads the scene archive aloud with Kokoro (local,
CPU, ~5× real time) into the Drive folder `Arcs/Audio/`; a cast file per
scene (`scenes/cast/<scene>.cast.md`, speaker tags on the scene's own text,
validated word for word) gives characters and registers their own voices
from `build/voices.yaml`, with delivery words per line (slow, quiet, beat…)
and Chatterbox Turbo cues ([sigh], [laugh]…) for speakers on that engine.
Chatterbox (its own venv, `build/chatterbox_setup.sh`) is the expressive
engine: Turbo for cues and speed, standard for the exaggeration knob, both
able to design a voice from a reference clip. The MCP has `scene_text` →
`cast_scene` → `narrate_scene` → `narration_status`, and the public server
serves the MP3s at `/t/<secret>/audio/…`, so a phone can ask for a scene and
play it while the PC is on. Next steps, when wanted: cast files for the
whole archive (a workflow: one agent per scene tags speakers, a checker
validates); a voice per named character in `voices.yaml`; RVC as a third
stage for community-made voices (needs a DirectML/ROCm torch on the 9070
XT); the multilingual Chatterbox checkpoint (already downloaded) for the
Latin lines. Chatterbox now runs on the 9070 XT (`build/chatterbox_gpu_setup.sh`)
with a Whisper read-back on every span.
**Casting rule (Isaac, after the first multi-voice render):** a voice is chosen
from the character's card and the prose — size, age, how the text says they
sound — not from what a corpus offers; Darius and Gimbzo want deep, raspy,
God-of-War-register voices, not the soft studio readers they got.

**The engine decision (Isaac, 12 Sep 2026, late):** Qwen3-TTS-1.7B-VoiceDesign,
pure voice design, for every character — and the job from here is to make
that one model as good and as efficient as it can be. Corpus clips are out;
the brief is the voice. Done the same night: `engine: qwen` in the narrator
(`build/qwen_backend.py`, `build/qwen_worker.py`), faster-qwen3-tts HIP
graphs (2.4–2.8× real time per draw), best-of-N draws scored against an
approved anchor folder per character with a self-calibrated pass mark,
Praat shaping for exact pace/pitch/body (`build/voice_shape.py`), the brief
manual (`build/voices/QWEN_DESIGN_GUIDE.md`) from four verified research
reports, a 41-character casting book (`build/casting.yaml`) with a
"brief a voice actor" paragraph each, and the two locked leads: Gimbzo on a
Yhwach register (the creaky 63 Hz line is the target; "creaky, vocal fry,
low rumble" is the phrase that finds it, "hoarse" pushes pitch up) and Darius
on Piccolo's floor with Vegeta's manner. Real-person references (Sabat,
Epcar) are briefs, not clips, and personal-use only.
Next: Isaac picks the narrator from the N1–N4 audition; write `qwen_instruct`
for the other 39 characters from their casting briefs (a workflow: one agent
per character drafts the 12-field brief from `casting.yaml` + the guide, a
checker rejects untrained words); anchors for each as Isaac approves takes;
`voice_describe.py` (measure a clip → brief words) for "capture the essence"
briefs; speed — the ggml/Vulkan backend of faster-qwen3-tts, `subtalker`
sampling experiments in the plain venv; loudness normalisation and a gentle
master on the final MP3; RVC only if a character's voice must be held tighter
than best-of-N can.

**Where it stands (2026-09-13, the cutter's pass).** The paragraph above is
the decision; this is the state. Qwen is locked: since `6caf56c` every
`engine: qwen` speaker falls back to its `fallback:` entry or a pool voice
unless `--qwen` is passed on the command line, and `narrate_scene` never
passes it — the design engine still drifts between takes. What is installed:
Kokoro (CPU, `build/models/`), Chatterbox on the GPU (`~/.venvs/wotr-cb-gpu`)
and a CPU copy (`~/.venvs/wotr-cb`, superseded by the GPU one),
Supertonic 3 (`~/.venvs/wotr-supertonic`), Qwen in two venvs
(`~/.venvs/wotr-qwen`, `wotr-qwen-fast`), CosyVoice in flight
(`~/.venvs/wotr-cosy`, `build/cosy_worker.py`) and an ElevenLabs
path in the narrator for a paid voice. Six engines, six venvs, one writer.
(Those are the Linux paths, `<WOTR_VENVS>/wotr-<name>`; the venvs themselves
were built on the Windows machine and none has been rebuilt here yet — the
`.sh` setups are untested ports, see Linux below.)
**The freeze:** nothing new on the voice roadmap until one engine-agnostic
gate is passed — *Gimbzo holds one voice across three consecutive scene
renders* (same pitch floor, same register, by ear and by `voice_shape.py`'s
numbers) — and the gate is measured, not asserted. Whichever engine passes
it is the character engine; the "Next" list that stood here (the 39 briefs,
`voice_describe.py`, the ggml backend, `subtalker`, RVC) moves to Deferred
below with that reason. The loudness master on the final MP3 is the one
exception: it is a mastering step, not an engine, and the ideas report has it
as Do next 7.

## Deferred until there is a reason

- The voice roadmap's "Next" list (moved here 2026-09-13): `qwen_instruct`
  briefs for the other 39 characters; `voice_describe.py` (measure a clip →
  brief words); the ggml/Vulkan backend of faster-qwen3-tts and `subtalker`
  sampling; RVC on ROCm. Reason: the Narration gate above is not passed; each
  of these builds on an engine that may not be the one. When one engine holds
  Gimbzo across three renders, take them up in that order.

- Character reference art (Isaac, 2026-09-12). Goal: gather artwork for
  characters from artists and boards, not only local AI output. Design
  agreed: gallery-dl fetches a Pinterest board (or an ArtStation/DeviantArt
  gallery — same tool) into a gitignored `refs/<board>/` folder; a scorer
  runs each new image through Claude vision against the wiki page named
  for it (a character's card, a material-culture page) and writes a small
  tracked `refs/index.json` — pin/source link, artist, board, subject,
  score, verdict, and a `reference-only | licensed` flag; matches are
  attached to the Notion page as a link with credit (reference-only) or an
  embedded image (licensed: commissions, CC-with-the-right-terms). Never
  embed reference-only art on the wiki — friends read it through the
  public MCP now, so that would be redistribution. Images stay out of the
  index repo. Rejected routes: the official Pinterest API (needs a
  business account), hand-rolled scraping of the site. First step when
  wanted: test gallery-dl on one of Isaac's boards.

## Still owed by Isaac

- ~~Muken's children (R22-10)~~ ruled 2026-09-12: the wiki's five (Sodoku, Sonzai, Emira, Tomuka, Ezo)
- ~~Packs Sixteen through Nineteen~~ ratified wholesale 2026-09-12
- ~~Black Agent's and Rengai's combat assignments~~ ratified as pitched 2026-09-12
- Three of the four remaining Four Crafts items (R9-1): Law III's rewrite, the golden-age question, the Latinate/vernacular doublet's scope (the Law V gate was ruled: Stage VII, 2026-09-12)
- Ratification of every proposal Phase A files

## Search by meaning — done 2026-09-13

Isaac asked whether SillyTavern / Serene Pub would help; the one thing they
would have added is semantic search over the lore, and that belongs in the
MCP, not in a second front-end (both need an API key WOTR does not have).
`build/embed_index.py` cuts wiki/ and scenes/ into passages under their
headings, embeds them with bge-small (ONNX, CPU, no torch; model in
`build/models/fastembed`), and keeps them by content hash so the hourly sync
re-embeds only what changed. `wiki` and `scene_recall` now rank by cosine
spread over the hits plus a keyword share (exact names still win), and show
the passages that matched. The index is gitignored; `sync.sh` rebuilds it.

- [x] `build/embed_index.py`, hybrid `wiki` / `scene_recall`, sync step
- [x] `scene_context(draft)`: the lorebook — every name in a draft to its card or page, the prior scenes on the same ground, struck Büri terms, names with no page (`build/lorebook.py`; `build/aliases.yaml` maps archive names to card titles — Darius is Ignatius's card, and the card should carry that name)
- [x] the Judger's assistant: `/judger <scene>` runs `.claude/workflows/judger-assist.js` — a reader of record, a rules clerk, a table clerk and a skeptic turn an archived scene into proposals (`ledger_add`, `advance_front`, `npc_set`, `log_ruling`, `propose_rule`, notes for Isaac's hands) in `bot/queue/<slug>.judger.md` + `.json`; `/judger apply <scene> P01 ...` (`build/judger_apply.py`) runs only the ids Isaac names. Nothing writes to the table until he does. The bot posts the JSON as cards with buttons (Phase F1/F2)

## The nightly — done 2026-09-13

What n8n was for, without the key. The systemd user timer `wotr-nightly.timer`
(03:30) runs `build/nightly.sh`: `build/nightly.py` (validate, resolve, the three
archive audits, the Büri sweep; every finding hashed by file, check and text
against `build/.nightly_state.json` so `reports/nightly.md` says NEW /
CLEARED / STILL OPEN; the scenes archived since the last run, each a
`/judger <slug>` for the morning; the Judger queue; the sync and backup
logs), then Claude Code headless on the subscription writes the "Overnight"
note at the top (`build/nightly_prompt.md`; tools locked to reading, the
read-only CLI, and editing the digest itself — it can decide nothing), then
the digest and the audit reports are committed and pushed. `session_start`
shows the note while it is under 36 hours old. The Claude step needs the
CLI signed in (`claude /login`; it is, and the first Linux nightly wrote its
note on 2026-09-14); without it the numbers run alone, and
`WOTR_NIGHTLY_NO_CLAUDE=1` in `~/.config/wotr/env` turns the step off on
purpose. The 2 h limit is a `timeout` around the CLI inside the script.

- [x] `build/nightly.py`, `build/nightly.sh`, the `wotr-nightly` unit, the OVERNIGHT block in `session_start`
- [x] the book dispatcher (ideas I29): `wotr-book.timer` (02:00) runs `build/book_dispatch.sh` -> `build/book_next.py` says what the book needs -> Claude Code headless invokes the `book-chapter` workflow for one chapter -> the chapter is committed under `book/`. Gates: the first three chapters, then every fifth, and the last (`build/book_next.py --approve N` / `--reject N --note "..."`); a written, undecided gate chapter blocks the dispatcher, and nothing is archived until Isaac calls `archive_scene`. The 03:30 digest reports where the book stands.
- [ ] the bot posts `bot/queue/*.judger.json` as approve cards in `#judger` (PLAN.md 9.3), and `/scene save` kicks off `/judger` in the background
- [x] n8n as the orchestrator (2026-09-14): `build/jobs_server.py` on 127.0.0.1:8799, the systemd user unit `wotr-jobs.service` (`build/systemd_setup.sh`) — a fixed list of named jobs (nightly, book, book_dry, sync, backup, checks) behind a shared secret in `build/.jobs_token`, never a command and never a prompt. n8n cannot call Claude (no key) and cannot run anything on this machine (a container, no repo mount), so n8n orchestrates and the host executes; the container shares the host network (`n8n/docker-compose.yml`, `network_mode: host`) and reaches the runner at `127.0.0.1:8799` (was Docker Desktop's loopback bridge, verified there; the Linux hop waits on the docker group). `n8n/WOTR_nightly.json` is the first workflow (run the nightly, wait, fetch the digest, send it on) and `n8n/README.md` is the wiring. If the workflow is activated, `systemctl --user disable --now wotr-nightly.timer` so nothing runs twice.
- [ ] the book gate from the phone: n8n posts the gate digest to Discord and the reply drives `book_next.py --approve N`
- [ ] Ollama (`127.0.0.1:11434`, once `ollama-rocm` is installed here; the six models were on the old machine) for the cheap mechanical passes — speaker tags, tell-bank scans — checked by the deterministic tools before anything counts
- [ ] a weekly drift report: what moved in the wiki and the archive this week, what contradicts, what is stale

## Linux — 2026-09-14

Ultron moved from Windows 11 to Arch (Omarchy) overnight and the tooling moved
with it; nothing in the index, the table or the archive changed. What the port
replaced:

- [x] bash for every script (was PowerShell), through one prelude, `build/env.sh`: `build/sync.sh`, `build/nightly.sh`, `build/book_dispatch.sh`, `build/backup.sh`, `build/mcp_public_setup.sh`, `build/install_mcp.sh`, `build/systemd_setup.sh`, `build/setup_linux.sh`, `bot/run.sh`; same logs, same exit codes, same commit messages with the `.sh` name
- [x] seven systemd user units (was seven scheduled tasks) in `build/systemd/`, installed by `build/systemd_setup.sh`: `wotr-sync.timer` (hourly), `wotr-nightly.timer` (03:30), `wotr-book.timer` (02:00), `wotr-backup.timer` (Sunday 03:00), `wotr-jobs.service`, `wotr-mcp-public.service`, `wotr-bot.service`; linger on, so they run without a desktop session; `journalctl --user -u wotr-<name>` beside each script's own log
- [x] the hard-coded paths and the registry token → one file, `~/.config/wotr/env` (template `build/wotr.env.example`), read the same way by the units, `build/env.sh` and `build/common.py`
- [x] the interpreter → `~/.venvs/wotr` (Python 3.14; `requirements.txt`, with `requirements-audio.txt` for the narration extras, not installed)
- [x] the MCP registration → `build/install_mcp.sh` (Claude Desktop) and `.mcp.json` (Claude Code, the project-scoped `wotr` server)
- [x] n8n's compose → `n8n/docker-compose.yml`, one service on the host network
- [x] Drive → `WOTR_DRIVE` when an rclone mount exists, local folders otherwise; the weekly backup always runs (the first Linux zip landed in `~/wotr-backups` on 2026-09-14)
- [x] verified live on 2026-09-14: the job runner, the public server on loopback, the dry-run dispatcher (blocked at chapter 1's gate), the backup, the first nightly under `wotr-nightly.timer` (note written, pushed)

Waits on Isaac's hands (sudo, a secret, a login):

- [ ] secrets in `~/.config/wotr/env` (`bash build/secrets.sh`, a hidden prompt): `NOTION_TOKEN` and `DISCORD_TOKEN` went in on 09-14 (the Discord token then needs a reset and the journal a purge after the mis-paste that day — CONTINUE.md); `ELEVENLABS_API_KEY` and `HF_TOKEN` when wanted; `WOTR_MCP_PUBLIC_URL` once the funnel is up
- [ ] docker: `sudo usermod -aG docker oridon`, re-login, `cd n8n && docker compose up -d`, then the `WOTR jobs` credential and the workflow import (`n8n/README.md`)
- [ ] tailscale: `sudo tailscale set --operator=oridon` once, then `bash build/mcp_public_setup.sh` opens the funnel and prints the URL (this node is `ultron-1` while the retired Windows node still holds `ultron`: remove that node and rename, or set `WOTR_MCP_PUBLIC_URL` to match)
- [ ] `ollama-rocm` for the cheap passes: `sudo pacman -S ollama-rocm; sudo systemctl enable --now ollama`
- [ ] rclone for Drive: `rclone config`, a mount, `WOTR_DRIVE=<mount>` in the env file; the next sync writes the documents there and the next backup lands under it
- [ ] the engine venvs from their `.sh` setups (`chatterbox_gpu_setup.sh`, `qwen_tts_setup.sh`, `supertonic_setup.sh`, `cosyvoice_setup.sh`; `sudo usermod -aG render,video oridon` first), still behind the narration freeze above
- [ ] Claude Desktop: quit it, `bash build/install_mcp.sh`, start it again

## Phase F — the Discord bot

Planned 2026-09-13; the plan is `bot/PLAN.md`. A deterministic,
role-gated bot for the players' server, running on Isaac's PC beside WOTR MCP
and importing its tools directly. No dice in canon channels: Table Rule 5
adjudicates stat-by-stat and every outcome traces to a table row.

- [x] F0 — landed 2026-09-13 (420ad8a) as the players' set: `/wiki`, `/define`, `/character`, `/fow`, `/recall`, `/timeline`, `/name`, `/stats`, `/narrate`; the rule/docket/conflict commands were dropped on Isaac's call (the Judger's desk, not the players'). Runs from `bot/run.sh` as the `wotr-bot.service` unit (installed 2026-09-14; `Restart=on-failure`, and with `DISCORD_TOKEN` empty it exits quietly)
- [ ] F1 — table state: `/fronts`, `/due`, `/ledger`, `/roster`, `/npc`; Judger writes (`/advance`, `/front`, `/ledger add|collect`, `/npc set`, `/menu`); player `/ledger propose` into the Judger queue
- [ ] F2 — scene play: forum per thread, `/bind`, `/scene open|verify|close|archive|text`; transcript → `scenes/<slug>.md` + cast file
- [ ] F3 — mechanics and audio: `/compare`, `/adjudicate` (Table Rule 5 card, no verdict), `/narrate`, `/ruling`, `/propose`; `/roll` off by default, `ooc` only
