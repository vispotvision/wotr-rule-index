# Fight review pass

Run once after a fight or set piece is drafted and before it is posted. This is the self-correction step: draft, check against criteria, revise. `verify_scene` (combat) runs after this, not instead of it.

Read the draft against the state sheet and answer each line. A "no" is fixed in the prose, not noted.

## Space and body
1. Do the final positions, wounds, weapons and reserve match the recap in `FIGHT_STATE_SHEET.md`? List any floating fighter, ignored obstacle or weapon that came back.
2. Does every wound carry? Find the first exchange after each injury and confirm the body behaves with it.
3. Is every distance change caused by a stated step, lunge, throw or push?

## Blows
4. Does every blow carry its Blow Card parts (set, read, contact or miss, tissue, sound and blood, reaction, next position; a miss takes parts 1, 2, 3 and 7)? Mark any blow that is a bare clause. In a quick trade, are the parts compressed rather than dropped (R81-1)?
5. Is tissue named and specific, never "hurt"? Is the sound and the blood given its own motion and color?
6. Does the technique ride on the blow, with both damages written, and never replace it? Do the two cards interleave (charge and pull with the set, aura and room with the read and contact, mechanism and effect beside the tissue, cost beside the reaction; R81-18)?
7. Does the kill or turning point carry the Kill Card, extending the Blow Card rather than replacing it (R81-18) (approach, named target, weapon path through named structures, sense detail, reaction, how long the dying takes and what is said, then taunt, vow or silence)?

## Pitch
8. Is the volume map followed? Is exactly one movement at peak?
9. Does the thought match each fighter's card (R81-6)? Every blow's read is behavior plus a quick thought; an analyst may think whole exchanges through; a brawler who reasons at length is the fault, not the count.
10. Does the rhythm change between the trades and the peak? Read three paragraphs aloud: if they sound alike, rework one.
11. Is the talk constant but individual? Swap two speakers' lines; if nobody would notice, rewrite them.

## Repetition
12. Check the draft against `desktop/style-bank/used-devices.md`. Replace every reused image, simile, beat or impact sound. Signature sounds of a technique or Wellspring recur and are never replaced (R81-10).
13. Does the fight have its own signature image, one thing the reader has not seen in any other fight?
14. Do the same verbs, sounds or sentence frames recur inside this fight more than the moment earns?

## Depth and clarity (Isaac, 2026-11-03)
15. Do name, hit and awe come first with the account right after? Does a signature's first use, a finisher and each change run the full Working Card (charge, pull, aura, the room, the senses, the mechanism in physics and metaphysics, the effect, the cost), a small move a line, and each ordinary repeat its charge, effect, cost and what differs (R82-24)? Is every move on the page a name someone would remember, called at the volume that character would use (R82-3, R82-25)? Does the aura coat and reinforcement get it once, then show as body tells (R81-17)? Is the real phenomenon named with its law on the page (R81-7)? Is η given as an idea and a proportion, never a figure in narration or a window (R81-3, R84-2)? Is a held card shown by effect first and explained in full at the reveal, the same exchange (R81-5)? Mark any working shown only as light and a name.
16. Is every failure or counter explained as fully as a success, physically and metaphysically?
17. Does the world answer each big moment (the air cracks and ripples, light bends, the ground groans), in vivid language chosen fresh for the moment (no house vocabulary, R80-24), without reusing a device from `used-devices.md`?
18. Is every technical, martial or system term explained on its first use, and set beside the body rather than in place of it?
19. Is every blow placed in space: which foot, which hip, the path of the limb, and where both fighters stand after? Could a reader draw the ring at every exchange?
20. Does the geography hold from first line to last? Does every rule the climax uses appear earlier, uncontradicted? Do the terms of the contest match what the fighters carry?
21. Does any character think in table words (card, row, sheet, rule id) outside his own window? Cut them.
22. Is the planted clue paid off, and is it visible on a second read?

## Windows (R84-1, R84-2, R84-17, R84-21, R84-22, R84-25 to R84-32)
23. Do windows sit on the page often and in detail, for damage, skill gains and reserve? A new fight with none is the fault; archived scenes stay as written (R84-3).
24. Does each window follow the blow or event it reports, with the blow still carded in full? Does the narration stay body first, never turning into numbers and never leaning on a window to do the Blow Card's work?
25. Does each window show only Grades, percentages, bars and levels, with EU, AU/s and η in the notes? Is each line alone in square brackets?
26. Is every window the owner's own, the POV's, apart from the crew's bars a real bond shows and a summon's window its holder reads (R84-25, R84-28)? Does anyone react to a window that is not theirs? Is any read of someone else either a stronger Gnosis Perception over a weaker Resilience Ward or an estimate said aloud?
27. Do the numbers hold? The reserve falls with what was spent and agrees with the body tell at half, a quarter and a tenth; a wound's status line says what it stops him doing, matches the state sheet and stays until treated (R84-29); every figure traces to the card.
28. Does a Release or Domain fill the window with its name and what changed, with a timer bar that drains on the page, its Grades inside the two-Grade cap? Does Pressure show in the room first and the window after? Does a spoken vow show its bargain and terms, and does breaking it land at once (R84-26)? Does a technique show no level, and does a jump take a bigger name? If Limina makes a window lie, is the cost on the page and a Gnosis counter within reach (R84-32)? Is a gain for his PC offered as a window line he can keep or change (R84-23)?

## After the pass
29. Add the fight's signature image and any new stock device to `used-devices.md`.
30. Run `verify_scene` with combat=True; fix every FAIL.
