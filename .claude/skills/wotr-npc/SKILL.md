---
name: wotr-npc
description: "Build a War of the Realms NPC with a real want, a refusal line, a lie, a full physical inventory and an unswappable voice, then propose the roster entry (npc_set on Isaac's word). Use whenever a scene needs a new person (a gate guard, a Measurewright, a widow, a rival), whenever Isaac says 'someone', 'a guy', 'who's there', or names a role without a person, and whenever an existing minor NPC is about to get a second scene and needs to be pinned down. Also use to audit an existing NPC for want, refusal and voice. Never for Isaac's PC or any flagged character."
---

# wotr-npc

NPCs in WOTR want things and pursue them. A character with no want is
furniture. This skill produces a roster entry and the first-sight paragraph.

## Before building

An NPC knows only what it could learn in-world and plays that well; the
writer's meta knowledge never becomes the NPC's omniscience (`wotr-write/references/fair-play.md`).


`roster(thread)` to see who exists; `wiki(query)` and `grep -ril` under
`wiki/` for a name or role already filed. Never duplicate. Load the culture's Standing
Inventory (`desktop/inventories/<culture>.md`): the NPC's food, oaths, time-words and proverbs come from it.
Name through the naming pass (five strata; Büri register dead; roll-name
and carried name for Far-Northern people).

## The seven fields (all mandatory, roster order)

1. **Want.** One concrete thing, this season, that the PC can help or hurt.
   Not "respect": a licence renewed, a son back from the muster, the
   woodpile through the Thin Weeks.
2. **Refusal line.** The thing they will not do no matter what is offered.
   Found by asking what they survived.
3. **Knows.** Three facts, one of which the PC needs.
4. **Lie.** One thing they will say that is wrong, and whether they know it
   is. Stays uncorrected until the PC catches it (table rule 8).
5. **Voice.** What they notice first entering a room; sentence length; one
   discourse marker; one fixed saying from the Inventory; what they never
   say. Gloss rights: never, diagnostic only, or yes. Swap test against
   every other speaker in the scene.
6. **Body.** Full first-sight inventory: hair by comparison (colour, texture,
   length), face shape and one feature, body with shoulders, chest, waist,
   thighs, belly, hands named, clothing with fit and wear, one distinguishing
   mark, one scent.
7. **Line.** If a practitioner: Stage by source name, Path, and the one or
   two stats the scene will stress, via `fow_line` or labelled estimate. If
   not: "no line".

Plus one *italic* private thought, true to their head, for the first scene.

## Output

The roster entry as a proposal (every `npc_set` field filled; the call
commits to git, so it runs on Isaac's word only), then the first-sight paragraph in prose,
under 200 words, layered smell first, from the POV's competence. The want
never stated; shown in what they do with their hands.

## Voice warmup

Before the paragraph, write one throwaway line in their voice and discard
it. Then write. A minor NPC may be a comic voice from the start, with no setup-deadpan-reaction beat (R52-31). Each NPC voice starts from a researched real-world speaker type, credited in the notes (R52-29).
