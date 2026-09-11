# Progress

Update at the end of every working session. This job spans sessions and the
supersession graph is only correct once the whole corpus is in.

| phase | scope | status | rules extracted | notes |
|---|---|---|---|---|
| 0 | structure confirmation | done | — | Family B does not parse as one template; see report below |
| 1 | Packs 19 down to 11 | done | 226 | all 9 files validated; 1 CONFLICTS.md row (C-001) |
| 2 | Packs 10 down to 5 | not started | — | Pack Eight has no § headings; Pack Five uses lettered headings |
| 3 | Packs 4 down to 1 | not started | — | Pack One is the unnumbered filename |
| 4 | standalone amendments | not started | — | one is .docx, needs pandoc |
| 5 | resolve and conflict report | not started | — | |

## Phase 0 findings (2026-09-10)

Section counts in `schema/pack_structure.md` for Family C (Packs 11-19) are
accurate. The "italic line carries ratification status and date" claim is
not: status/date live in a bold `**Status:**` line, not an italic one, and
often carry no date at all (unratified packs). Family B (Packs 5-10) is not
one template — each pack has its own heading scheme (Pack Five uses lettered
`## A./B./...` headings, not `## PART N`; Pack Six has three top-level `##`
sections outside any PART; Pack Nine/Ten have no numbered `###` subsections
at all, just bold lead-ins). Treating each Five-Ten source individually
rather than assuming a shared template.

## Per-pack ledger

| source | rules | live | superseded | pending | proposed | validated |
|---|---|---|---|---|---|---|
| Pack Nineteen | 19 | 0 | 0 | 0 | 19 | yes |
| Pack Eighteen | 16 | 0 | 0 | 0 | 16 | yes |
| Pack Seventeen | 19 | 0 | 0 | 0 | 19 | yes |
| Pack Sixteen | 18 | 0 | 0 | 0 | 18 | yes |
| Pack Fifteen | 23 | 20 | 0 | 3 | 0 | yes |
| Pack Fourteen | 24 | 0 | 0 | 5 | 19 | yes |
| Pack Thirteen | 37 | 0 | 1 | 6 | 30 | yes |
| Pack Twelve | 37 | 37 | 0 | 1 | 0 | yes |
| Pack Eleven | 33 | 10 | 0 | 5 | 18 | yes |
| **Phase 1 total** | **226** | **67** | **1** | **20** | **138** | **yes** |

## Backfill queue (supersedes links pointing at not-yet-extracted rules)

Resolved during Phase 1 (kept here only as a record of what got fixed):
R15-1-MYSTIC_REGISTER_NEVER_PHYSICS_STRUCK and R15-4-TWELVE_VOICE_DISCIPLINE_SOFTENED
turned out to be partial strikes/demotions, not full kills — cross-referenced
by id in notes instead of supersedes, once Pack Twelve existed to check
against. R15-4-THIRTEEN_HAX_STRUCK -> R13-6-HAX_DIALOGUE_BAN (full strike,
backfilled). R17-3-SIX_LINE_CARD's five-line predecessor identified as
R12-3-CARD_PLUS_CHAIN (Pack Twelve §3).

Still open, carried into Phase 2/3:
- R15-1-DICTION_PALETTE, R15-1-REGISTER_BY_CULTURE -> Pack Five rows
- R15-4-PACK_NINE_CLASS_MARKING -> Pack Nine row
- R12-1-PACK_SEVEN_REPEALED and its six sibling §1 rows -> every Pack Seven
  rule, once extracted (mark each Pack Seven row status:superseded directly
  with a note pointing back here, per BRIEF's known live-fire case — this is
  the single densest backfill in the corpus)
- R12-7-APPARATUS_CAP_REPLACED, R12-7-LEGIBILITY_BAN_STRUCK -> Pack Six rows
- R12-8-SCENE_GUIDE_PACK7_STRUCK -> Pack Seven's pre-write-question/self-review rows
- R12-8-SCENE_STANDARDS_BANS_STRUCK -> confirm against Amendment Three
  (WOTR_Companion_Guide_Amendments.md, Phase 3) once extracted

## Open conflicts (see CONFLICTS.md)

- C-001: R11-3-FIREARM_PROSE_LAW (live) cites Pack Seven's mechanism-explain
  ban as authority for keeping proofed-round mechanics unexplained, but
  R12-1-EXPLAIN_BAN_STRUCK (live) struck exactly that ban. Unresolved,
  Isaac's call.

## Carried notes

- Pack Twelve carries no pack-level "pending"/"originated" status line
  anywhere, unlike every other pack in Phase 1; treated as status:live
  throughout (see that file's header comment) since §1/§4 are explicitly
  "Confirmed by Isaac's ruling" and every later pack treats it as settled.
  Flag to Isaac if this reading is wrong — it would flip ~37 rows.
- Policy adopted for `amends.guide`: use the exact name/filename the source
  text itself gives (e.g. `WOTR_Master_Style_Directive.md` when a pack spells
  out the filename, or the plain prose name like "Manual Verification Guide"
  when it doesn't). Never invent a `.md` suffix a pack doesn't use. Where a
  later-extracted pack gives a filename for a guide an earlier pack only
  named in prose, backfilled the earlier pack to the attested filename
  (done for WOTR_Ability_Technique_Design_Guide.md on Pack Eighteen and
  WOTR_Item_and_Equipment_Writing_Guide.md on Pack Seventeen).
- Partial strikes and demotions (a pack narrows or softens an earlier rule
  without fully killing it) are never recorded in `supersedes` — that field
  is reserved for full kills, since validate.py's contradiction check would
  otherwise force a still-live rule to be marked dead. Cross-reference these
  by rule id in `notes` on both sides instead.
