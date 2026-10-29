---
name: wotr-lookup
description: "Answer a War of the Realms canon question fast from the WOTR MCP: who someone is, what a Stage, Wellspring, glyph or faction is, what happened in a past scene, when something happened, what a rule says. Use whenever someone asks 'who is', 'what is', 'what happened', 'when did', 'is X canon', 'what do the rules say', or names a person, place or term without context."
---

# wotr-lookup

Pick the tool by what is asked, answer in plain words, and say which page the
answer came from. If nothing on file covers it, say so; do not invent canon to
fill a lookup.

| Asked about | Tool |
|---|---|
| A person | `character(name)`, then `fow_line(name)` for their numbers |
| A place, faction, people, creature, item, term | `wiki(query)` (`limit=` higher to survey what exists) |
| A glyph, Wellspring, Family, Physics Domain | `codex(query)` |
| Every name in a passage at once | `scene_context(text)` |
| What happened, a past scene | `scene_recall(query)` |
| When, in what order | `timeline()` |
| A thread's open business | `fronts(thread)`, `due()`, `roster(thread)` |
| What the rules say | `load_rules(tags)`, `rule(id)`, `check_docket(tags)`, `list_conflicts()` |

Canon order when sources disagree: Isaac's rulings, then Fracture of Worlds
and the Master Codex, then the rule index, archived scenes, character cards,
other wiki pages. A disagreement is reported with both sides, never settled
silently.

Meta knowledge is for the writer; a character knows only what their card and
their life give them.
