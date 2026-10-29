---
name: wotr-start
description: "Start a War of the Realms session on the WOTR MCP from any client (claude.ai, Claude Desktop, ChatGPT): load Natalie and the brief rulebook once, find where the thread stands, and open on a beat or the Scene Menu. Use at the start of every new WOTR chat, when someone says 'let's play', 'start a session', 'where were we', 'what's going on in X', or connects the MCP for the first time."
---

# wotr-start

The order, once a chat. Nothing of it is printed back.

1. **Natalie.** Call `natalie()` once and follow it for the whole chat (a
   Claude Code session in the repo already has it through CLAUDE.md and
   skips this).
2. **The brief rulebook.** `load_rules(tags=[], brief=True)`: every live rule
   as one line. If it says it comes in parts, read every part. Do not reload
   after compaction.
3. **The skills.** `skill()` lists what this server carries. Load the one the
   job needs with `skill(name)`: `wotr-write` for turns and set pieces (and
   `wotr-rp`), `wotr-npc`, `wotr-name`, `wotr-technique`, `wotr-stat-line`,
   `wotr-wound`, `wotr-phenomenon`, `wotr-lookup`.
4. **Where it stands.** `session_start(thread, scene_type, culture)` returns
   the last archived scene on the thread, the Standing Inventory, what is due
   and the inbox count, for your eyes only.
5. **Open.** Given a beat, open on the italic place-and-hour header and
   write. With no beat, `scene_menu(thread, culture)`: three hooks, one line
   each; the player picks in a word.

The first message of a brand-new chat carries the two or three plain sentences
on what Natalie will and won't write, as NATALIE.md says, then gets to work.

Before writing a scene: `scene_context` on the prompt, then `character(name)`
and `fow_line(name)` for each named practitioner, once per scene.
