# CONTINUE — how to pick this work up cold

Read this first in any new session (scheduled or not). Isaac's standing
direction: inside work he has asked for, make the calls; no "pending" slots.
`ROADMAP.md` is the plan; this file is the live state. Newest block first;
append a dated block, do not rewrite older ones (two sessions write this repo
at once — `git pull` before editing, and commit only your own files).

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

**The book.** `.claude/workflows/book-chapter.js` writes chapters in Claude
Code; the design is `book/design/BOOK_PIPELINE.md` (moved from `n8n/`; its
n8n transport needs an API key that does not exist — do not build toward it).

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
