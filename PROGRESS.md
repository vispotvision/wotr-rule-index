# Progress

Update at the end of every working session. This job spans sessions and the
supersession graph is only correct once the whole corpus is in.

| phase | scope | status | rules extracted | notes |
|---|---|---|---|---|
| 0 | structure confirmation | done | — | Family B does not parse as one template; see report below |
| 1 | Packs 19 down to 11 | in progress | 19 so far | Pack Nineteen done; Eighteen down to Eleven remain, plus finishing Fifteen |
| 2 | Packs 10 down to 5 | not started | — | Pack Eight has no § headings |
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
| Pack Fifteen | 8 (partial) | 7 | 0 | 1 | 0 | yes |
| Pack Nineteen | 19 | 0 | 0 | 0 | 19 | yes |

## Carried notes

- Pack Fifteen §1 has seven repeals and five survivals; only a sample is
  extracted so far. Finish it in Phase 1.
- Several Pack Fifteen rows have empty `supersedes` with a note, because their
  targets live in Packs Five, Nine and Twelve and have not been extracted yet.
  Backfill those links at the end of Phase 2, not before.
- Pack Nineteen is entirely `status: proposed` — the pack's own header says
  "originated, pending Isaac's ratification" with no section marked
  confirmed. It supersedes nothing; it only extends Pack Sixteen's
  vocabulary-conversion principle to speech (noted on R19-2-FIXED_TEXT, not a
  supersedes link since nothing is struck) and escalates the severity of the
  existing voice-differentiation test (R19-5-SORT_BY_SPEAKER_TEST).
- Policy adopted for `amends.guide`: use the exact name/filename the source
  text itself gives (e.g. `WOTR_Master_Style_Directive.md` when a pack spells
  out the filename, or the plain prose name like "Manual Verification Guide"
  when it doesn't). Never invent a `.md` suffix a pack doesn't use.
