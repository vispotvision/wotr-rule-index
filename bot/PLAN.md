# WOTR Discord bot — plan

Agreed shape (Isaac, 2026-09-13): a bot for a **multi-player roleplay server**,
**fully deterministic** (the rule index and the wiki are the brain; no LLM),
running **on Isaac's PC** beside WOTR MCP, with four surfaces in v1: rule and
lore lookup, table state, scene play and archive, and mechanics.

This document is the plan. Nothing here is built yet. Phases land one at a
time; each is checked off in `ROADMAP.md` (Phase F) with the commit that
landed it.

## 1. What it is, in one paragraph

A second front-end onto what the repo already has. WOTR MCP
(`build/mcp_server.py`) exposes ~45 tools over the rule index, the wiki
mirror, the scene archive and the table state (`table/*.yaml`); the
`@server.tool()` decorator returns the plain function, so the bot imports
`mcp_server` and calls `rule()`, `wiki()`, `fronts()`, `archive_scene()`
directly. The bot adds what Discord is for: several people writing in one
place, roles, threads, and a permanent, searchable transcript that becomes
the scene text.

## 2. Standing constraints (inherited from CLAUDE.md, and they bind the bot)

- **Verbatim only.** A rule answer shows the `verbatim` field, its ID, pack,
  status and source section. The bot never summarises a rule in its own
  words. `summary` may be shown, labelled as summary, under the quote.
- **Never resolve a conflict.** If a rule ID appears in `CONFLICTS.md`, the
  answer carries the conflict row and both sides. The bot never picks.
- **Never invent.** No number the card does not carry (`fow_line` already
  refuses; the bot inherits that). A lookup that finds nothing says so.
- **`sources/` is read-only.** The bot never writes there. Its only writes are
  the ones the MCP already makes: `table/*.yaml`, `scenes/`, `RULINGS.md`,
  `proposals/`, and the Notion Scene Archive via `archive_scene`.
- **Secrets never in chat.** `DISCORD_TOKEN` is a user environment variable,
  read the same way `NOTION_TOKEN` is (`_env()` in the MCP). Never in a file
  in the repo, never in a Discord message.

## 3. Decisions made in this plan

| Decision | Choice | Why |
|---|---|---|
| Language / library | Python 3, `discord.py` 2.x, slash commands (`app_commands`) | Same interpreter and venv as the MCP; direct import, no RPC |
| Where the code lives | `bot/` at the repo root (`bot/main.py`, `bot/cogs/*.py`, `bot/run.ps1`) | Separable from `build/`, which is the index and the narrator |
| Dice | **None in canon channels.** | WOTR resolves contested actions by Table Rule 5 — Stage gap, the read, what has been spent, the environment — stat-by-stat (R14-3-STATS_DECIDE_TABLE), and every outcome traces to a table row (R14-3-TRACEABILITY, R13-8-RECONSTRUCTIBLE_ADJUDICATION). A `/roll` would be a new mechanic the rules don't have; introducing one goes through `propose_rule`, not through a bot. A `/roll` exists only as an out-of-canon toy, off by default, usable in channels tagged `ooc`. |
| Who can write | Role-gated: **Judger** (Isaac; every write), **Scribe** (trusted helper; scene close, ledger, NPC notes), **Player** (post, look up, propose), **Reader** (look up only) | Writes commit to git and touch Notion; players propose, the Judger enters |
| Scene container | Discord **forum channels**, one per story thread; each forum post is one scene; the in-character messages in it are the scene text | Forum posts are threads with titles, tags and a natural close; the message log is already speaker-tagged |
| Attribution | A player's in-character messages are attributed to the character they are **bound** to (`/bind <character>`) — one binding per player per forum | Gives the cast file for free (see §6) |
| Long answers | Embed up to 4096 chars; beyond that, paginate with buttons; a wiki answer always carries the Notion page link from the wiki manifest | Discord limits (embed 6000 total, 25 fields) |
| Hosting | Windows scheduled task at logon, like `WOTR wiki sync`; log to `bot/.bot.log` | Same operating model as the narrator; bot is down when the PC is |
| Audio | `/narrate` attaches the MP3 when under the guild upload limit (10 MB unboosted), otherwise posts the split parts | Never post the `/t/<token>/audio/` route: that leaks the public-MCP secret |

## 4. Server layout (what Isaac builds in Discord; the bot assumes this)

```
#rules-desk           lookups, anyone; bot answers in-channel
#table                fronts, ledger, due, roster; Judger writes here
#judger               private: session_end drafts, proposals queue, ledger candidates
#ooc                  out-of-character; /roll allowed here if enabled
Forum: kharven-thread   one post per scene on the Kharven thread
Forum: <other thread>   one forum per story thread in table/fronts.yaml
#audio                narration drops
```

Forum tags: `open`, `closing`, `archived`, `standard`, `combat`, `mass-combat`
(the last three map to `scene_type` in `session_start` / `verify_scene`).

## 5. Command surface, by phase

### Phase F0 — skeleton and lookups (read-only, no table writes)

| Command | Backs onto | Notes |
|---|---|---|
| `/rule <id>` | `rule(id)` | Embed: title, verbatim (quoted), ID · pack · status · section; conflict rows if any; `summary` below, labelled |
| `/rules <tags…> [status]` | `load_rules_tool(tags, status, brief=True)` | Tags autocomplete from `schema/applies_to.md`; returns IDs and titles, paginated |
| `/docket <tags…>` | `check_docket(tags)` | Pending and proposed |
| `/conflicts` | `list_conflicts()` | Paginated |
| `/wiki <query>` | `wiki(query, full=False)` | Top hits with snippet and Notion link; a button opens the full page paginated |
| `/character <name>` | `character(name)` | Name autocomplete from `scenes/CAST.md` and `wiki/Characters/` |
| `/fow <name>` | `fow_line(name)` | The FOW line; "no FOW figures on this card" verbatim when absent |
| `/recall <query>` | `scene_recall(query)` | Scene archive search |
| `/timeline` | `timeline()` | Paginated |

Also in F0: `bot/main.py`, `bot/run.ps1`, the scheduled task, `DISCORD_TOKEN`
from the environment, the role names in `bot/config.yaml`, and a `/whoami`
that prints the caller's roles and binding. All MCP calls run in
`asyncio.to_thread` so the gateway heartbeat never blocks.

### Phase F1 — table state

| Command | Backs onto | Role |
|---|---|---|
| `/fronts [thread] [closed]` | `fronts()` | anyone |
| `/due [thread]` | `due()` | anyone |
| `/ledger` / `/ledger show <id>` | `T.load("ledger")` | anyone |
| `/roster [thread]` | `roster()` | anyone |
| `/npc <name>` | `roster()` filtered | anyone |
| `/advance <front> <what_happened> [next_move]` | `advance_front()` | Judger |
| `/front add`, `/front clock` | `add_front()`, `set_front_clock()` | Judger |
| `/ledger add <category> <who> <text> [due]` | `ledger_add()` | Judger, Scribe |
| `/ledger collect <id> <how>` | `ledger_collect()` | Judger, Scribe |
| `/ledger propose …` | writes to a queue in `bot/queue/` and posts to `#judger` | Player |
| `/npc set …` | `npc_set()` | Judger, Scribe |
| `/menu <thread>` | `scene_menu()` | Judger |

Every write goes through one `asyncio.Lock`; writes already commit through
`_table_commit`. The bot runs `git pull --ff-only` before a write because
`build/sync.ps1` also commits on the hour (see §8).

### Phase F2 — scene play and archive

| Command | What happens |
|---|---|
| `/bind <character>` | Binds the caller to a character in this forum; stored in `bot/bindings.yaml`. One binding per player per forum; the Judger can bind anyone to anyone (NPCs). |
| `/scene open <title> [type] [culture]` | Creates the forum post, tags it `open`, posts `session_start(thread, type, culture)` as the pinned first message (the loadout, fronts, what's due). |
| in-character messages | Any message in an `open` post from a bound player is scene text. Prefix `((` or `//` marks a line out-of-character; it is excluded. |
| `/scene narrate <text>` | Judger/Scribe: a narrator line (no speaker). Also `/scene say <character> <text>` for NPCs without a binding. |
| `/scene verify` | Compiles the post so far and runs `verify_scene(markdown, combat, culture, band)`; posts the report in the thread. |
| `/scene close` | Tags `closing`. Compiles the transcript (§6), runs `verify_scene`, posts the report, and posts the `session_end` draft to `#judger`. Nothing is archived yet. |
| `/scene archive [title]` | Judger only, on a `closing` post: `archive_scene(title, markdown, author_notes)` — `scenes/<slug>.md`, Notion, one commit — writes the cast file, tags `archived`, locks the post. |
| `/scene text` | The compiled markdown as an attachment, for anyone. |

### Phase F3 — mechanics and audio

| Command | What it does |
|---|---|
| `/compare <a> <b>` | Both FOW lines side by side, the Stage gap named, and the Core Progression / Physical Benchmarks rows that bracket them (from `_fow_tables()`). No verdict. |
| `/adjudicate` | A modal with Table Rule 5's four inputs — Stage gap, the read (landed / not), what has been spent, what the environment allows — plus which stat answers each. Output is an adjudication card naming the rows, posted in the thread and captured into the scene's author notes at archive time so the outcome is reconstructible from the page (R13-8). It records the Judger's decision; it does not make one. |
| `/roll` | Off by default (`bot/config.yaml: ooc_dice: false`); works only in `ooc`-tagged channels when on. |
| `/narrate <scene> [voice]` | `narrate_scene()`; the bot polls `narration_status()` and drops the MP3 in `#audio`. |
| `/ruling <rule_id> <text>` | Judger: `log_ruling()`. |
| `/propose <title> <text> <tags…>` | Player/Judger: `propose_rule()`; the proposal file lands in `proposals/` and a card in `#judger`. |

## 6. The transcript becomes the scene — and the cast file

Compilation of a forum post, in message order:

- bound player message → `**Character:** text` if the message is dialogue-only,
  else the text as written (the character's prose)
- `/scene narrate` → the text, no speaker
- `/scene say` → as a bound message for that character
- `((`/`//` lines, bot messages, reactions, edits after close → dropped
- edits before close → the latest version (Discord keeps the edit; the bot
  reads the message body at compile time, not at receipt)

The same pass writes `scenes/cast/<slug>.cast.md` with the speaker tags,
because every line already knows who said it. That is the file the narrator
wants (`cast_scene` validates it word for word against the scene). Registers
and delivery words are left for a person to add.

Scene text from Discord goes through `verify_scene` before archive. The
verify report is advisory: the Judger archives or does not.

## 7. Files

```
bot/
  main.py           client, intents, cog loading, error handler
  config.yaml       role names, channel/forum ids, ooc_dice flag, page size
  bindings.yaml     player ↔ character per forum
  queue/            proposals and ledger candidates awaiting the Judger
  cogs/
    lookup.py       F0
    table.py        F1
    scene.py        F2
    mechanics.py    F3
    audio.py        F3
  embeds.py         rule / wiki / character / front renderers; paginator
  compile.py        forum post → markdown + cast file
  run.ps1           venv activation, log, restart on crash
  .bot.log          (gitignored)
```

`requirements.txt` gains `discord.py>=2.4`. Nothing under `build/` changes
except, if needed, moving pure helpers the bot shares into `common.py`.

## 8. Risks and how the plan meets them

- **Two writers on one repo.** `build/sync.ps1` commits hourly; the bot commits
  on writes. Both go through git, so the failure is a rejected push, not lost
  data. Bot writes `git pull --ff-only` first, hold the lock across
  write+commit+push, and report the failure in-channel if the push is
  rejected rather than retrying blind.
- **Heartbeat.** Every MCP call is synchronous and some (`reconcile`,
  `narrate_scene`) run for minutes. All of them go through `to_thread`; the
  long ones defer the interaction and follow up.
- **Message Content intent.** Reading in-character messages needs the
  privileged intent. Fine under 100 guilds; enabled in the developer portal.
- **Notion.** `archive_scene` writes Notion; if `NOTION_TOKEN` is missing the
  MCP already says so; the bot surfaces that message and leaves the post at
  `closing`.
- **PC off.** Same trade-off as the audio route. The slash commands stay
  registered; Discord shows "application did not respond". Accepted for v1.
- **Rule drift.** A player quoting `/rule` gets the index as of the last
  sync. The embed footer carries the repo commit hash so a quote is datable.

## 9. What I have not decided (Isaac's calls before F2)

1. Which story threads get a forum at launch — the names in
   `table/fronts.yaml` (`Kharven thread, the year after`, …) or a shorter
   list.
2. Whether players may `/bind` to any card or only to cards on an allowed
   list (PCs), with NPCs reserved to the Judger.
3. Whether `/scene archive` also runs `session_end`'s Ledger candidates into
   the Judger queue automatically or only on request.

## 10. Order of work

F0 → F1 → F2 → F3, one phase per PR, `python build/validate.py` green before
each is called done (the bot does not touch the index, but the gate stands),
and a ROADMAP Phase F line checked per phase.
