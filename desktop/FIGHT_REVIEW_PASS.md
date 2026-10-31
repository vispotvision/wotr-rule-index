# Fight review pass

Run once after a fight or set piece is drafted and before it is posted. This is the self-correction step: draft, check against criteria, revise. `verify_scene` (combat) runs after this, not instead of it.

Read the draft against the state sheet and answer each line. A "no" is fixed in the prose, not noted.

## Space and body
1. Do the final positions, wounds, weapons and reserve match the recap in `FIGHT_STATE_SHEET.md`? List any floating fighter, ignored obstacle or weapon that came back.
2. Does every wound carry? Find the first exchange after each injury and confirm the body behaves with it.
3. Is every distance change caused by a stated step, lunge, throw or push?

## Blows
4. Does every blow carry its Blow Card parts (set, read, contact or miss, tissue, sound and blood, reaction, next position; a miss takes parts 1, 2, 3 and 7)? Mark any blow that is a bare clause.
5. Is tissue named and specific, never "hurt"? Is the sound and the blood given its own motion and colour?
6. Does the technique ride on the blow, with both damages written, and never replace it?
7. Does the kill or turning point carry the Kill Card (approach, named target, weapon path through named structures, sense detail, reaction, how long the dying takes and what is said, then taunt, vow or silence)?

## Pitch
8. Is the volume map followed? Is exactly one movement at peak?
9. Count the blows followed by a thought or reaction. If it is most of them, cut the thoughts to the turns.
10. Does the rhythm change between the trades and the peak? Read three paragraphs aloud: if they sound alike, rework one.
11. Is the talk constant but individual? Swap two speakers' lines; if nobody would notice, rewrite them.

## Repetition
12. Check the draft against `desktop/style-bank/used-devices.md`. Replace every reused image, simile, beat or sound.
13. Does the fight have its own signature image, one thing the reader has not seen in any other fight?
14. Do the same verbs, sounds or sentence frames recur inside this fight more than the moment earns?

## Clarity of the working
15. Is the technique explained once, in the right voice, with its cost? Is the explanation shorter than the damage it causes?
16. Is the planted clue paid off, and is it visible on a second read?

## After the pass
17. Add the fight's signature image and any new stock device to `used-devices.md`.
18. Run `verify_scene` with combat=True; fix every FAIL.
