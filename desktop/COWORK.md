# COWORK.md — what Claude Cowork reads

Cowork is Claude Desktop's folder mode. On this machine it is Claude Code run
by the desktop app (`~/.config/Claude/claude-code/`), with the app's
connectors (Notion, Google Drive, Trello, Gmail, …) and the `WOTR MCP`
registered by `build/install_mcp.sh`. It reads the `CLAUDE.md` of whatever
folder the session is opened on, and its default folder is `~/Claude`
(`coworkUserFilesPath`), where `CLAUDE.md` is a link to this file. Opened on
the repo, it reads the repo's `CLAUDE.md` instead, which leads through
`AGENTS.md` back here. Either way this file binds.

## Where the work is

Isaac's War of the Realms work is `~/wotr-rule-index`. For anything WOTR, that
folder is the desk: its `CLAUDE.md` (the constraints), then `AGENTS.md` (the
map — layout, commands, the prose protocol, what the robots commit), then
`CONTINUE.md` (the live state, newest block first). If the session was opened
on `~/Claude` and the task is WOTR, say so and work in the repo by path; if the
tools will not reach it, ask him to reopen the session on the repo folder.
Deliverables he asks for outside the repo land in `~/Claude`; inside it, where
`AGENTS.md`'s layout puts them.

You are not Natalie. `desktop/NATALIE.md` is the standing prompt of the Claude
Desktop *chat* project — the game master who runs the table. Cowork is the
desk beside the table: files, connectors, checks, conversions, drafts, closes.
A turn at the table is a Natalie chat, not a Cowork session. When Isaac asks
for prose here anyway, `AGENTS.md` "Before writing any WOTR prose" governs:
`session_start`, `load_rules` with the loadout's tags, `check_docket`, the
cards, `verify_scene` after — never from memory of "how WOTR works".

## The connectors — what Cowork has that Claude Code does not

The repo's own paths win. The `WOTR MCP` tools (`AGENTS.md` lists them; the
read-only ones are also `python build/book_tools.py <tool>`) already read Notion,
Trello and the archive the way the repo expects; reach for a raw connector only
for what no tool covers.

- **Notion** is where canon is edited, and the hourly sync mirrors it into
  `wiki/`, so a page edit through the connector *is* a canon edit. Reading is
  free. Writing to the wiki database, The Table — Running Pieces, a character
  card or The Rule Index pages happens on Isaac's word only, and through the
  MCP writer where one exists (`archive_scene`, `log_ruling`, `ledger_add`,
  `advance_front`, `npc_set`, `create_character` / `update_character`) rather
  than the connector, so git and Notion move together. Pages flagged `private`
  in `wiki/.manifest.json` stay private: never copied, exported or quoted onto
  a public page.
- **Google Drive** is the export shelf and the backup target when it is
  mounted (`WOTR_DRIVE`; `build/docs_export.py`, `build/backup.py`). Nothing
  private goes there, no wiki or scene dumps outside those scripts, and the
  base craft guides (`~/wotr-vault/true-canon`) are never overwritten — a
  change is a new dated edition beside the original, with a changelog.
- **Trello** holds the old material that the conversions came from
  (`trello_cards`, `convert_character`). Read it; do not reorganise, archive
  or relabel boards and cards.
- **Gmail** and any other connector are not WOTR surfaces. Send nothing; draft
  only what he asked for, and show it before it goes anywhere.

## The lines that hold everywhere

- `sources/` is read-only. `verbatim` is exact source text. Conflicts are
  recorded in `CONFLICTS.md`, never resolved. Nothing invented. The gate is
  `python build/validate.py` exiting 0 — `python` meaning the venv,
  `bash build/py.sh build/validate.py` in the safest form.
- Secrets: never in this window, never printed, never written for him. He fills
  `~/.config/wotr/env` with `bash build/secrets.sh` in a terminal. The `/t/…`
  MCP URL and the two token files are never posted or committed. Anything
  needing `sudo` is his to run — give the line in a `bash` block.
- The robots (hourly sync, 03:30 nightly, 02:00 book dispatcher) commit their
  own paths and `git pull --rebase --autostash` first. `git pull --rebase`
  before editing; commit only your own files, promptly; one pack per commit.
- Never rewrite the repo's `CLAUDE.md` or `AGENTS.md` as "folder
  instructions": they are Isaac's constraints and the map. Anything the next
  session must know is a dated block at the top of `CONTINUE.md`; a note about
  Cowork itself goes in this file, under Notes.
- Inside work he asked for, make the calls and say which; the only "pending"
  is the *Owed by Isaac* list in `CONTINUE.md`. Plain language, a specialist
  term glossed at first use. Close with what was done, what was not, and why.

## Notes

(Cowork may add dated lines here — what it learned about working from Claude
Desktop on this machine. Nothing about canon; that has its own files.)
