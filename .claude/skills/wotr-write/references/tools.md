# WOTR tools in Claude Code

The `wotr` MCP is registered by `.mcp.json`; its tools are `mcp__wotr__<name>`
and may be deferred: `ToolSearch("select:mcp__wotr__load_rules,...")` once,
loading everything the job needs in one call. When the MCP is not connected,
21 read-only tools run as a command line:

```bash
~/.venvs/wotr/bin/python build/book_tools.py            # the list
~/.venvs/wotr/bin/python build/book_tools.py load_rules prose-law combat pov --brief
~/.venvs/wotr/bin/python build/book_tools.py loadout duel
~/.venvs/wotr/bin/python build/verify.py draft.md --combat
```

## Reads (ordinary work)

| Need | MCP tool | Without the MCP |
|---|---|---|
| Start of session | `session_start(thread, scene_type, culture)` | `book_tools.py session_start "<POV>" <type> <culture>` |
| Rules for the job | `load_rules(tags=[], brief=True)` once a session, then `load_rules(tags)` per domain on first use (R79-2; `references/rules.md`) | `book_tools.py load_rules <tags>`, or `out/rules.live.full.md` |
| Open rulings | `check_docket(tags)`, `list_conflicts()`, `rule(id)` | `out/docket.md`, `CONFLICTS.md`, `RULINGS.md` |
| Every name in a beat or draft | `scene_context(draft)` | `book_tools.py scene_context <file>`, `wiki/INDEX.md` |
| One page | `wiki(query)`, `character(name)` | `grep -ril` under `wiki/` |
| Numbers | `fow_line(name)` | the card, then `wiki/The Magic System/` |
| Continuity | `scene_recall(query)`, `timeline()`, `cast_index(write=False)` | `scenes/MANIFEST.md`, `grep` under `scenes/` |
| What comes due | `due()`, `fronts(thread)` | `table/LEDGER.md`, `table/FRONTS.md` |
| Opening with no beat | `scene_menu(thread, culture)` | three hooks from anywhere, one line each (R79-2) |
| NPCs | `roster(thread)` | `table/NPCS.md` |
| Pre-write, set pieces only (R79-2) | `scene_brief(beat, ...)` | the fields in SKILL.md §2 by hand |
| Improve a submitted fight (advisory, unlogged, R79-10) | `gap_fill(markdown)` | the eight steps in technique-design.md |
| Verify a draft, once a turn (R79-2) | `verify_scene(markdown, combat, culture)` | `build/verify.py` |
| Stale Büri names | `stale_names()` | grep the wiki mirror for the old register |
| Scene end, silent upkeep and archive | `session_end(thread, scene_markdown, title, author_notes, ledger, fronts, npcs, cards, days)`: keeps the Ledger, Fronts, roster and lasting card changes current, archives the scene, logs the session, prints one line (R79-8) | fill `wotr-ledger` by hand |

## Writes

Silent background upkeep, no approval asked and nothing printed (R79-8):
`session_end`, `ledger_add`, `advance_front`, `add_front`, `set_front_clock`,
`npc_set`, `log_ruling`, `archive_scene` when a scene ends, and
`update_character` for lasting changes (a wound that stays, Crystal State,
Level, Stage, a technique he approved, renown). On Isaac's word:
`create_character`, card design changes, new techniques and Level points for
his PC, `sync_now`. `handoff` carries only research and images (R79-12).
Each commits to git and writes the wiki vault where it touches a page; Notion
is retired and never written. `propose_rule` files a proposal and is fine when
he asked for one.

## Precedence when copies disagree

Live MCP read, then the `wiki/` vault (the source since 2026-10-15; Notion is
frozen history). The packs beat the rule index if the two ever disagree.
Numbers by field (R79-10): Fracture of Worlds for system law, tables and
names; the Stat Sheet for a character's figures; the card for person facts
and wherever the sheet is silent. Resolve by that order and move on.
