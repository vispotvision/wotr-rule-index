# House codexes: brief

The author wants every House of the Inner World to have its own detailed codex, in the shape of the two he supplied: `imports/drafts/lineages-2026-11-05/Zettari update 2.md` and `Valorin Family.md`. **Read both first, for shape, voice and density.** Each House gets **its own signature thing**, as the Zettari have the Everlasting Eye and Matla and the Valorin have the Lattice: one idea you can say in a breath, that no other House has, that grows from who this House already is.

## Read before writing
`imports/drafts/connections-audit/FLOW_LAW.md`, which governs. `desktop/NATALIE.md`, sections ABILITIES AND THE WORLD, THE SHEET AND THE CLIMB, and from "**Familiar words" through "**The Wellsprings on the Paths". `wiki/The Magic System/The Soul and the Climb/The Three Paths Routing, Recognition and the Gate.md`, `Classes and the Three Ladders.md`, `wiki/The Magic System/The Foundations/The Sixty Wellsprings/The Sixty Wellsprings.md` and its kind pages. Then everything on file about the House: its section on the group page in `wiki/Factions, Bloodlines & Institutions/Houses and Bloodlines/`, its realm page and Gazetteer section under `wiki/Geography & the Four Quarters/The Bearing and the Holding/The Inner World — The Northern Shield/`, its culture's file in `desktop/inventories/`, its people's page in `wiki/Races & Peoples/`, and every character card from it in `wiki/Characters/Volume I — Character Cards/`. Use `grep -ril` across `wiki/` and `lore/v1/scenes/` for its name.

## Rules
- **Canon binds.** Facts on file, card facts and anything shown in an archived scene stay true (R82-46). A kit on a card must fit the codex: a Stark's cold, a Greymane's shield, and so on. Read the cards, and let the signature explain what they already do. Change no card and no scene. New names follow the culture's sound rules (NATALIE, Naming canon).
- **A House gives four things and never a Path:** an eye if it has one, a grip (one ladder opens early, and its cap never lifts), a stat lean, lens affinities. Only Moto, Zettari and Yukari have an Epoch's instrument behind them; no other House's signature may match them in reach. A signature can be a body trait, a bond, a doctrine, a contract, a craft, a rite or an inheritance. Variety matters: not every House gets an eye, and not every signature is a fighting art. The noodle-seller's scale counts too, since Small powers are everywhere (R82-36).
- **Fair and loud.** Every signature has a mechanism, a cost from its own idea, a limit and a counter within reach. Fate stays ruinously hard, and a Spirit Wellspring gives no fire. Goofy names are welcome on a goofy House (R82-10), and carded Moto stay serious. It should be fun to read: this world is loud, strange and famous.
- **Voice.** Written as Guild archivist or Measurewright, opening on a famous story or spectacle (R82-42). Familiar words beside WOTR's: Aether (mana), Essence (spiritual energy). American spelling, no em dashes in prose (a heading may use one, as the two models do), no onomatopoeia, no author's name, no rule ids, no "upgraded" or how-it-was-made talk. Explain a term at first use. The models carry long tables and lists; so may you, and you also need real paragraphs.
- **Length.** Moto and Yukari run as long as they need. Every other House runs 1,500 to 3,000 words of real content, with no padding.

## The shape (use what the House has; skip what it does not)
1. Frontmatter with `title`, `private: true` and `tags: [Bloodlines]`, then an Overview table: type, origin, founder, seat, anchors, signature, maxim.
2. An opening story, then who they are and what they want, in a few paragraphs. What they hold that everyone needs.
3. **Origin of the House.**
4. **The House on the Crystal:** how the three layers run in them (table), Path lean as a tendency, which ladder usually climbs and what grip they have, what's typical on the rungs.
5. **The signature**, its own section under its own name: what it is, how it works in plain words, its tiers or named forms, what it costs, its limit, who beats it. This is the heart of the page.
6. **Physical Appearance and Dress:** stature, coloring, marks, voice, and how their gear flexes (R85-1): colors, cut, a House's look at fifty paces, what a poor cousin wears.
7. **Lineage Traits:** three to six, each `### [Trait] Name — Subtitle` with bullets and an italic closing line, as the models do.
8. **System Metrics:** Stat lean table by Primary with Signature Sub-Stats and why; Wellspring compatibility by tier, with real names from the Sixty; how they read on the Stages, a short table.
9. **Doctrine and Arts:** the House's fighting or working style and a table of named moves with what each does, in their own tongue with meaning. Technique names shout in the House's culture.
10. **Culture:** language, rites (three to six, specific and strange), who they marry, feud with and owe, what the House's commoners and servants get.
11. **Limitations and Soul-Costs:** two to four `### [Curse] Name — Subtitle`, real costs.
12. **How They Stand Against the Three Paths:** a few lines on how a Body, Spirit and Fate enemy each trouble them.
13. **Final definition,** a paragraph and the House's closing line.

## Filing
New pages go in `wiki/Factions, Bloodlines & Institutions/Houses and Bloodlines/The Houses of the Inner World/`, named `House Stark.md` and so on. Do not create a hub, since one is added after. Leave the group pages' sections in place, adding at the end of the House's section one line: `*The full codex: [[path|House Stark]].*` Run `rust/target/release/wotr-mcp validate`, which must print PASS. Rule-quoted lines survive. Do not edit `sources/`, `rules/`, `RULINGS.md`, `desktop/`, cards or scenes. Do not commit. Scratch work goes in a subfolder of `/tmp/claude-1000/-home-oridon-wotr-rule-index/e30b1f68-e9e0-481d-b086-5bb16a587065/scratchpad/` named for your group.

## Report
For each House: its signature in one line. Then inventions the author may want to strike, conflicts you found with cards or scenes, and anything left undone. Under 300 words.
