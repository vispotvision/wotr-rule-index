---
name: wotr-technique
description: "Design a War of the Realms technique, Trait, art or ability from a rough idea: character first, then the real phenomenon, the mechanism, the cost, a fair counter, then the Codex. Use whenever someone sketches an ability ('what if he could...', 'how would X work', 'make me a technique', 'what does this cost'), or a card needs a technique entry."
---

# wotr-technique

1. **Load.** `load_rules(tags=["magic-design", "codex", "stats", "character-sheet"])`
   the first time. The full method is wotr-write's technique reference:
   `skill("wotr-write", file="references/technique-design.md")` on the MCP,
   `.claude/skills/wotr-write/references/technique-design.md` in Claude Code.
   Fair play: `skill("wotr-write", file="references/fair-play.md")`.
2. **Character first.** `character(name)` and `fow_line(name)`: what this
   person refuses, survived and believes, their Stage, reserve and Aether
   Class. The technique grows from that.
3. **The phenomenon.** Run `wotr-phenomenon` (`skill("wotr-phenomenon")`):
   the real physics, the governing law, the boundary condition the glyph
   supplies, the failure mode.
4. **The mechanism and the price.** Cost in EU against the owner's reserve,
   written as how long it lasts from full; limit and tell; one fair counter
   within reach at the technique's own Stage on known law. A signature's
   counter answers before, during and after contact. A price the player names
   stands; rework the mechanism until it yields that price, or say in one line
   that none can and offer the nearest.
5. **The Codex.** `codex(query)` for precedent, Wellspring, Family and
   Physics Domain. Never invent a Wellspring or glyph.
6. **The entry.** One name in caps, a short gloss where the character has a
   naming register (`wotr-name`), its kind in brackets, then one paragraph in
   plain everyday words with the figures inline.

The whole card comes back at once. Every choice sticks only when the player
keeps it; a PC's new techniques are his call.
