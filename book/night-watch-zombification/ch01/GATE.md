# Gate: Chapter 1, The Docket Head

**Book:** night-watch-zombification · **POV:** Wystan Ashmore · **Words:** 3,413 prose words by verify (3,716 by `wc -w` on the whole file); target 3,500, set-piece band 2,500+.

Files: `final.md` (copied from `draft_r1.md`), `final_notes.md` (from `notes_r1.md`). See **Instructed round (r1)** below.

## Verdict

**Verdict: PASS (r0 0F/0W)**

| Round | FAIL | WARN | Dropped |
|---|---|---|---|
| r0 | 0 | 0 | 0 |

## Remaining FAILs and WARNs

None. The critics returned no findings. The deterministic checks were info-only: verify PASS, the lie and the misreading found verbatim, voice not fingerprintable (fewer than eight archive lines).

## Declared lie and misreading

- **Lie (Qiu Yinzhi):** "It went quiet when you were at the sink." It is false: the bracelet never stopped pulling. Her thumb is on the badly struck mark as she says it. Nobody corrects it.
- **Misreading (Wystan):** "Whatever the formulator had put into those animals had stopped where he stopped putting it, because a man who works at a distance from his own work has to choose the distance, and every site in the four counties would show the same hard margin once somebody walked it with a rule." It is entered as the Register's position ("A dose goes where it is put") and stands until ch15–16.

## Beat

Outline beat: Yinzhi's name at the docket head; the tin struck with his brass and entered as Register exhibit one; the four chapter-wax pieces folded and dated; a letter to Tally asking for a second dataset and who set the marker; Yinzhi sent home; the main returns at the sixth division; Brack's classification found closed at the day desk; the memorandum entered with *edges* in the margin; nobody reads past the classification. The notes' continuity summary covers every element. The critics raised no finding against the beat, so they found it delivered.

## Hooks

- **Planted (8):** H01-far-side-of-the-marker, H02-quarter-inch-sealed, H03-chapter-wax, H04-tallys-second-dataset, H05-night-register-a-person, H06-edge-held-cup, H23-edges-in-the-margin, H24-brack-signs-bleed. The anchoring quotes are in `final_notes.md`.
- **Paid:** none (as the outline planned).

## Front ticked (proposed)

**the-night-register-file**, segment 1 "Exhibit one" (bible, Proposed Fronts; it is not in `table/fronts.yaml` and needs `add_front` on Isaac's word). The world changes: the memorandum is entered in ink under the red rule. The POV sees the consequence: the day clerk says "That's closed, that one" and shelves the book spine out.

## Originated, pending Isaac (from notes)

The day desk sits in the same building, up four steps. The day clerk is unnamed. Also originated: the brass token, brass wax and fresh tins, the grounding tea and the kettle. Flags: the fold carries no rendered date, and the archive attests two different accounts of who cut the wedge, which the exhibit entry no longer chooses between (see the Instructed round below, and `final_notes.md` Flags).

Written in Isaac's unattended run (he asked for the whole book written through); gate not decided.

## Instructed round (r1) — Rhett Konn's note at the gate, 2026-09-25

**The note.** The chain-of-custody line in the day-book exhibit entry put the knife in Tally's hand.
The archive attests two accounts and reconciles neither: `scenes/the_nights_watch.md:13` gives Tally a
cut on the ninth ("He had cut a section with his knife"), and `scenes/the_nights_watch.md:275` gives the
wedge in the tin to Yinzhi ("Under the third lamp he could see that it had grown since she cut it").
Naming Tally either states the wrong one or silently picks a winner between two archive lines inside a
document entered in ink as exhibit one.

**The change.** One clause, `final.md:57`:

- was: *Cut in the cut by Tally, N., and sealed there by the assay under chapter wax, the 9th.*
- now: *Cut in the cut, sealed there by the assay under chapter wax, the 9th.*

True under either reading, decides nothing, and in character for a Register document that records what
it can attest. Nothing else moved: same POV, events, order and ending; no new character; the declared
lie and misreading untouched. Length: 3,413 prose words by `verify` before and after, 3,716 → 3,712 by
`wc -w` on the whole file (three words out of a 3,700-word chapter).

**Bounded-revise compliance.** Frozen rules held: 100% of dialogue lines kept, 100% of paragraphs kept,
word count 100% of round 0, no new characters, no new lie or misreading.

**Checks.** `build/verify.py final.md --band set-piece --culture Accord` → **PASS, 0 fail, 0 warn**,
3,413 words, set-piece band. `build/validate.py` → PASS. `load_rules prose-law` and
`check_docket prose-law` run before the edit; 0 pending or proposed.

**Carried with it.** `final_notes.md` Flags now quotes `:13` and `:275` side by side instead of calling
the question settled; `state.json`'s ch01 custody fact and its anchoring quote are re-cut to the
corrected sentence (the quote has to be verbatim from `final.md`).

**Not decided here.** Which account is right is filed as **WAR-64** for Doc Kett, `needs-ruling`,
`blocked-on-isaac`, and recorded as **C-042** in `CONFLICTS.md` with both lines quoted verbatim and
their file:line. Neither archive line was touched. It does not block this chapter: the corrected line is
true under either answer, and if the ruling names Tally the attribution goes back in one clause.

## What Isaac is deciding

Isaac has four options. **Approve:** the chapter is archived with `archive_scene` under the title "The Docket Head". **Instruct:** one more revise round runs with his note. **Re-brief:** the chapter is redrafted from a changed brief. **Drop:** the chapter is set aside. The originated details above (day-desk location, day clerk, brass token) become canon only if he approves.
