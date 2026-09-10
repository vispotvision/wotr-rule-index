# Pack structure notes

Surveyed 10 September 2026 against `sources/`. Three structural families. Confirm
in Phase 0 before trusting any of it.

## Family C — `## §N` (Packs Eleven through Nineteen, except Eight)

```
# WOTR Companion Guide Amendments, Pack Fifteen
## THE REGISTER REPEAL
*Status: ruled by Isaac in session, 6 September 2026...*
## §1. The Ruling
## §4. Consequential Edits
## §5. Open Rulings
```

The italic line under the title often carries ratification status and date.
Capture it into the pack-level `ratified` field.

`Consequential Edits` is the supersession goldmine: bulleted, each bullet naming
a pack and section or a guide and section, then what happened to it.

`Open Rulings` carries R-codes (`R15-A`, `R15-B`). Every one becomes a row with
`status: pending` and `kind: open_ruling`, and the recommendation, where the pack
offers one, goes in `notes` and never in `verbatim` as though it were settled.

Section counts observed: Eleven 5, Twelve 8, Thirteen 10, Fourteen 9, Fifteen 5,
Sixteen 9, Seventeen 10, Eighteen 9, Nineteen 9.

## Family B — `## PART N` and `### N. TITLE` (Packs Five through Ten)

```
## PART I: OPACITY
### 1. THE LADDER. BUDGET ZERO.
### 2. THE APPARATUS RULE
```

Pack Eight is the outlier: `## SECTION ONE.` with `### 1.1`, `### 1.2` beneath.
Packs Nine and Ten end with a `## RATIFICATION LEDGER`, which tells you the
status of everything above it. Read it first, then extract.

Pack Seven uses `### Amendment 7.1, Section 3.1, ...` which encodes its own IDs
and target loci in the heading. Use them. All of Pack Seven is dead by Twelve §1;
extract it anyway, because rules elsewhere reference it by name.

## Family A — `# AMENDMENT N` + `## Target:` (Packs One through Four)

```
# AMENDMENT ONE
## Target: `WOTR_Combat_Craft_Guide.md` — replaces the open g...
### The per-character pass, and why it cannot be a guard assignment
```

Amendment numbers run continuously across packs One through Four (Pack Four
opens at AMENDMENT THIRTEEN). Use the amendment number in the rule ID, not a
per-pack counter, since the corpus refers to them that way.

The `## Target:` line gives you `amends` for free: the guide filename before the
dash, the operation after it.

Pack One is the file with no number: `WOTR_Companion_Guide_Amendments.md`.
