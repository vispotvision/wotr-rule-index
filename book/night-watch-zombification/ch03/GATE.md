# Gate: Chapter 3, The Morning Check

- **Book:** night-watch-zombification
- **Words:** 3,639 (`wc -w` on the whole file); 3,634 prose words by verify. Target 3,500, set-piece band 2,975 to 4,025.
- **Files:** `final.md` (copied from `draft_r0.md`), `final_notes.md` (copied from `notes_r0.md`)

## Verdict: pass

| Round | FAIL | WARN | Dropped |
|---|---|---|---|
| r0 | 0 | 6 | 1 (the H13 "dead lean" quote is not in the draft) |

`verify --band set-piece --culture Accord`: PASS, 0 fail, 0 warn.

## Open findings (0 FAIL, 6 WARN)

1. **WARN, continuity:** "The Division had entered it in his file under a different heading, in the copying hand, as a disciplinary observation." The phrase is reserved in the bible (l.129) for ch65. Fix: rename this entry, or note that it is a separate, earlier item.
2. **WARN, POV and knowledge:** "The porter knew his face." This states the porter's knowledge as fact under the POV lock. Fix: "The porter seemed to know his face."
3. **WARN, rules:** "as if the air in the room had given up something it had been holding since the morning and let it down on him." This is an "as if" simile at the H13 plant (R15-1). Fix: describe the settling literally.
4. **WARN, canon:** "and it was stale, and he ate all of it because Yinzhi had told him to". This instruction from Qiu Yinzhi appears in no source, though nothing contradicts it. Fix: list it under "Originated in this draft" for sign-off.
5. **WARN, canon:** "in the back room of the old office on the river". The place appears in no source and is already logged as originated in the notes. It needs Isaac's sign-off.
6. **WARN, beat:** "Is that them." Keld is waiting "for a relief that came too late" only by inference, because the relief memory sits apart from the window scene. Fix: tie the memory to Keld at the window in one clause.

## Declared lie and misreading

- **Lie (Elspeth Lyle):** "I did not send for Master Brack." The tell: her eyes stay on the Bureau's green tape, then "She was writing again, and the pen did not stop." Nobody corrects it.
- **Misreading (Wystan):** "It was what any shut room did by this hour, with the main running under it and people at work in it all day, and it came down on everybody in the room alike; Lyle had simply never sat a night on the Register, and had nothing on her hands to feel it with." The residue is actually running to him (H13, corrected in ch44).

## Beat

Wystan wakes at noon with shaking hands and reads Keld's minute against the record. At the medical house, Keld sits at a window, still waiting for a relief that came too late. Lyle reads the edges memorandum and gives the file until the quarterly inspection of the gauge-housing. Brack stands by his classification and hands over the Bureau's raw readings unasked. In Lyle's shut room the residue settles on Wystan and he does not remark it. He tells Brack, "I will get a hand and not a purse."

**Delivered:** yes. The critics found every part on the page. The one soft spot is Keld still waiting for the relief: it is there by inference only (WARN 6).

## Hooks

- **Planted:** H12-kelds-minute, H13-low-ground-sink, H14-brass-token, H15-six-who-know, H32-hand-never-purse. All five are quoted in `final_notes.md`.
- **Paid:** none (the outline's `pays` is empty).
- **Touched, not paid:** H23 (Lyle reads *edges*, and the position goes into her minute) and H24 (Brack: "I'd sign it again this afternoon").

## Proposed Front ticked

**the-night-register-file** (proposed in bible.md; `front_id` null), segment 1 "Exhibit one", push 2 of 5.
- The Prime Warden's minute now carries the term (the quarter) in ink, under her silver, with Wystan's initials.
- The file now holds the Bureau's raw Ferriby field sheets, entered as received unasked.
- The segment is not filled, and nothing was written to `table/fronts.yaml`.

Written in Isaac's unattended run (he asked for the whole book written through); gate not decided

## What Isaac is deciding

**Approve** means `archive_scene` under the title "The Morning Check", after which the chapter goes into the book's memory. **Instruct** means one more revise round carrying his note; the six WARNs above are the obvious candidates, and none blocks the chapter. **Re-brief** means redrafting the chapter from a changed brief. **Drop** means cutting the chapter.
