# WOTR tools in Claude Code

The `wotr` MCP is registered by `.mcp.json`; its tools are `mcp__wotr__<name>`
and may be deferred: `ToolSearch("select:mcp__wotr__load_rules,...")` once,
loading everything the job needs in one call. When the MCP is not connected,
21 read-only tools run as a command line:

```bash
~/.venvs/wotr/bin/python build/book_tools.py            # the list
~/.venvs/wotr/bin/python build/book_tools.py load_rules prose-law combat pov --brief
~/.venvs/wotr/bin/python build/book_tools.py loadout duel
~/.venvs/wotr/bin/python build/verify.py draft.md --combat --culture Kharven --band set-piece
```

## Reads (ordinary work)

| Need | MCP tool | Without the MCP |
|---|---|---|
| Start of session | `session_start(thread, scene_type, culture)` | `book_tools.py session_start "<POV>" <type> <culture>` |
| Rules for the job | `load_rules(tags)` | `book_tools.py load_rules <tags>`, or `out/rules.live.full.md` |
| Open rulings | `check_docket(tags)`, `list_conflicts()`, `rule(id)` | `out/docket.md`, `CONFLICTS.md`, `RULINGS.md` |
| Every name in a beat or draft | `scene_context(draft)` | `book_tools.py scene_context <file>`, `wiki/INDEX.md` |
| One page | `wiki(query)`, `character(name)` | `grep -ril` under `wiki/` |
| Numbers | `fow_line(name)` | the card, then `wiki/The Magic System/` |
| Continuity | `scene_recall(query)`, `timeline()`, `cast_index(write=False)` | `scenes/MANIFEST.md`, `grep` under `scenes/` |
| What comes due | `due()`, `fronts(thread)` | `table/LEDGER.md`, `table/FRONTS.md` |
| Opening with no beat | `scene_menu(thread, culture)` | three hooks by hand: Front, Ledger, fresh |
| NPCs | `roster(thread)` | `table/NPCS.md` |
| Pre-write | `scene_brief(beat, ...)` | the fields in SKILL.md §2 by hand |
| Improve a submitted fight | `gap_fill(markdown)` | the eight steps in technique-design.md |
| Voice | `voice_check(name, line)` | swap test by reading; `table/voices.yaml` |
| Verify a draft | `verify_scene(markdown, combat, culture, band)` | `build/verify.py` |
| Stale Büri names | `stale_names()` | grep the wiki mirror for the old register |
| Session close draft | `session_end(thread, scene_markdown)`: drafts, and logs the session (ages the Ledger) | fill `wotr-ledger` by hand |

## Writes (Isaac's word, one call per approved item)

`archive_scene`, `ledger_add`, `advance_front`, `add_front`, `set_front_clock`,
`npc_set`, `log_ruling`, `create_character`, `update_character`,
`voice_fingerprints` (rebuilds `table/voices.yaml`), `sync_now`. Each
commits to git and/or writes Notion. `propose_rule` files a proposal and is
fine when he asked for one. `session_end` logs a session: call it once, at a
real close.

## Precedence when copies disagree

Live MCP read, then Notion, then the `wiki/` mirror. The packs beat the rule
index if the two ever disagree; the Stat Sheet workbook beats a card (R14-2).
