# Progress

Update at the end of every working session. This job spans sessions and the
supersession graph is only correct once the whole corpus is in.

| phase | scope | status | rules extracted | notes |
|---|---|---|---|---|
| 0 | structure confirmation | done | — | Family B does not parse as one template; see report below |
| 1 | Packs 19 down to 11 | done | 226 | all 9 files validated; 1 CONFLICTS.md row (C-001) |
| 2 | Packs 10 down to 5 | done | 144 | all 6 files validated; Pack Seven's repeal fully backfilled |
| 3 | Packs 4 down to 1 | done | 109 | all 4 files validated; Pack One filed as pack-01-one.yaml |
| 4 | standalone amendments | done | 98 | all 5 files validated; the .docx is plain text, no pandoc needed; 1 new CONFLICTS.md row (C-002) |
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
| Pack Eleven | 33 | 11 | 0 | 5 | 17 | yes |
| **Phase 1 total** | **227** | **68** | **1** | **20** | **138** | **yes** |
| Pack Ten | 11 | 11 | 0 | 0 | 0 | yes |
| Pack Nine | 13 | 12 | 0 | 1 | 0 | yes |
| Pack Eight | 26 | 0 | 0 | 0 | 26 | yes |
| Pack Seven | 37 | 5 | 32 | 0 | 0 | yes |
| Pack Six | 21 | 14 | 3 | 4 | 0 | yes |
| Pack Five | 35 | 27 | 0 | 4 | 4 | yes |
| **Phase 2 total** | **143** | **69** | **35** | **9** | **30** | **yes** |
| Pack Four | 36 | 30 | 0 | 6 | 0 | yes |
| Pack Three | 25 | 24 | 0 | 1 | 0 | yes |
| Pack Two | 18 | 12 | 3 | 3 | 0 | yes |
| Pack One | 30 | 22 | 4 | 4 | 0 | yes |
| **Phase 3 total** | **109** | **88** | **7** | **14** | **0** | **yes** |
| **Corpus total after Phase 3** | **479** | **225** | **43** | **43** | **168** | **yes** |
| Racial Voice and Dialect Guide Amendment | 15 | 15 | 0 | 0 | 0 | yes |
| Naming Guide Amendment | 23 | 18 | 3 | 2 | 0 | yes |
| Canon Amendment, Agamalu and Büri Origin | 15 | 4 | 0 | 6 | 5 | yes |
| Moto Reversion Ledger | 16 | 12 | 0 | 4 | 0 | yes |
| Inner World Naming Amendment | 29 | 0 | 0 | 5 | 24 | yes |
| **Phase 4 total** | **98** | **49** | **3** | **17** | **29** | **yes** |
| **Corpus total after Phase 4** | **577** | **274** | **46** | **60** | **197** | **yes** |

## Backfill queue (supersedes links pointing at not-yet-extracted rules)

Resolved during Phase 1 (kept here only as a record of what got fixed):
R15-1-MYSTIC_REGISTER_NEVER_PHYSICS_STRUCK and R15-4-TWELVE_VOICE_DISCIPLINE_SOFTENED
turned out to be partial strikes/demotions, not full kills — cross-referenced
by id in notes instead of supersedes, once Pack Twelve existed to check
against. R15-4-THIRTEEN_HAX_STRUCK -> R13-6-HAX_DIALOGUE_BAN (full strike,
backfilled). R17-3-SIX_LINE_CARD's five-line predecessor identified as
R12-3-CARD_PLUS_CHAIN (Pack Twelve §3).

Resolved during Phase 2 (kept here as a record):
- R12-1-PACK_SEVEN_REPEALED and its §1/§3/§4/§8 siblings: all backfilled
  against the 40 Pack Seven rows once extracted. Five Pack Seven rows kept
  status:live instead of the superseded default, because Pack Twelve's own
  text explicitly preserves them (the economy/ladder hard rails,
  character-first design order, Titans/Epoch-scale dread, the cost audit
  and the character-first re-derivation pass as ongoing production
  processes rather than prose restrictions).
- R12-1-APPARATUS_CAP_STRUCK, R12-7-APPARATUS_CAP_REPLACED,
  R12-7-LEGIBILITY_BAN_STRUCK -> backfilled against Pack Six.
- R15-1-DICTION_PALETTE -> confirmed no Pack Five target exists (Pack Five
  never mentions the Diction Palette); its true target is the base
  WOTR_Master_Style_Directive.md §8, not present in this corpus, so no id
  to backfill.
- R15-1-REGISTER_BY_CULTURE -> demotes R5-C3-NARRATION_REGISTER_EXTENSION
  (Pack Five §C.3), backfilled.
- R15-4-PACK_NINE_CLASS_MARKING -> demotes R9-2-CLASS_MARKED_CRAFT_WORDS
  (Pack Nine PART TWO), backfilled.

Resolved during Phase 3 (kept here as a record):
- R12-8-SCENE_STANDARDS_BANS_STRUCK checked against Pack One's Amendment
  Three: no match. That row's five listed "Scene Standards" items (word
  count, sensory opening, italic thought, no section spacers,
  physical-action close) contain no mechanism-explanation or
  metaphysical-number bans, so the specific target Pack Twelve struck
  remains unidentified in this corpus. Left unresolved rather than forced.
- R2-6-FRONTAGE_SUSTAIN_REFORM and R3-7-EXPENDITURE_GRAMMAR's "check once
  Pack One is extracted" notes resolved: the origins are
  R1-2-THREE_FIELDS_MANDATORY/R1-2-COUNTERPLAY_THREE_WAYS (Frontage/
  Sustain/Re-form) and R1-1-BLADE_GRAMMAR/R1-1-VERDICT_GRAMMAR/
  R1-1-PERCUSSION_VS_BLADE (the three-vocabulary framework Expenditure
  extends to four).

Still open, carried into Phase 4:
- R7-4-ITEM_TERTIARY_SOURCE and several other Pack Seven rows have no
  specific successor named anywhere yet, even after checking Packs
  One-Four; left pointing at the general R12-1-PACK_SEVEN_REPEALED
  catch-all.
- R1-1-COZBI_TENTATIVE, R2-OP-COZBI_GRAMMAR, R1-OP-COZBI_GRAMMAR and the
  naval/siege/cavalry and practitioner-POV open items across Packs
  One/Two are all marked status:superseded on the editorial-judgment
  basis described below, not a quoted supersedes link — flag to Isaac if
  this reading is wrong.

## Open conflicts (see CONFLICTS.md)

- C-001: R11-3-FIREARM_PROSE_LAW (live) cites Pack Seven's mechanism-explain
  ban as authority for keeping proofed-round mechanics unexplained, but
  R12-1-EXPLAIN_BAN_STRUCK (live) struck exactly that ban. Unresolved,
  Isaac's call.
- C-002: whether Filemu Agamalu's own Ava-name (Canon Amendment) survives
  the Inner World Naming Amendment's strike of "the Agamalu addition"
  (Naming Guide Amendment), given the Moto Reversion Ledger's separate,
  narrower statement that the Agamalu house's naming was never governed
  by the Büri reversion specifically. Three documents, none of which
  settle it directly. Unresolved, Isaac's call.
- Not raised as a formal conflict row, but worth a mention: R7-7-VOW_CLAUSE_OPEN
  (Pack Seven's "vow clause... pitched, unruled") appears to be genuinely
  orphaned — no later pack visibly resolves it, and it isn't itself a
  clash between two live rules, just an abandoned open question.

## Carried notes

- Pack Twelve and Pack Six both carry no pack-level "pending"/"originated"
  status line anywhere, unlike every other pack in Phases 1-2; both treated
  as status:live throughout (see each file's header comment) since their
  content is either explicitly "Confirmed by Isaac's ruling" or treated as
  settled fact by every later pack. Flag to Isaac if this reading is wrong
  for either pack — it would flip ~37 rows for Twelve, ~17 for Six.
- New precedent from Phase 2: where a LATER, already-ratified pack's own
  text explicitly says an earlier, never-formally-ratified pack's content
  "survives" or "stands" in quotable words, that content is marked
  status:live even though its origin pack was never itself ratified. Used
  for five Pack Seven rows (via Pack Twelve) and seventeen Pack Five rows
  in Sections C/D/E (via Pack Fifteen §4's "all stand" line) — see each
  row's own notes. The matching Pack Five §H pending-ruling items are
  deliberately left pending rather than closed, since Pack Fifteen never
  references them by docket item number.
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
- Reference/word-bank style content (a growing table, lexicon, or bank of
  named examples) is not extracted row by row — only the standing rule that
  governs how it's built/used gets a row (e.g. Pack Sixteen's conversion
  lexicon, Pack Thirteen's Phenomenon Bank, Pack Eight's worked entries).
- New precedent from Phase 3: a "Still Open"/pending docket item is marked
  status:superseded (not left pending forever) once a later pack gives a
  substantive answer, even when that later pack's text never quotes the
  specific docket entry by name or number — the alternative (leaving a
  resolved question marked pending) would actively mislead anyone reading
  out/docket.md. This is treated as different in kind from resolving a
  conflict between two contradictory live rules (which CLAUDE.md forbids
  deciding): a question that now has an answer isn't a live contradiction.
  Used repeatedly across Packs One/Two/Three for Cozbi's grammar, naval/
  siege/cavalry prose, and practitioner POV in mass action. Flag to Isaac
  if this reading is wrong — each instance is noted individually on the
  affected rows.
- Pack One is the unnumbered filename (WOTR_Companion_Guide_Amendments.md)
  but is filed as `pack-01-one.yaml`, matching the rest of the numbered
  series — BRIEF's `doc-<slug>.yaml` convention is reserved for the Phase
  4 standalone amendments, not this pack.

## Phase 4 notes

- `WOTR_Naming_Guide_Amendment.docx` is not actually a Word binary — it is
  plain UTF-8 text with a `.docx` extension (confirmed by reading the raw
  bytes: it opens with `**WOTR CHARACTER...`). No pandoc conversion was
  needed, available, or guessed at; the file was read directly.
  `WOTR_Canon_Amendment_Agamalu_and_Büri_Origin.md`'s actual on-disk
  filename contains two mangled box-drawing characters (U+251C, U+255D) in
  place of "ü" — a pre-existing filesystem/transfer encoding artifact, not
  edited per the sources/ read-only rule. `source_file` in that pack's
  rules file references the exact garbled name so validate.py can find it.
- Standalone docs have no pack number for precedence purposes
  (`pack_number: null`, as BRIEF specifies), but the schema's `id` pattern
  requires a numeral. Assigned R20-R24 as mechanical id-numeral buckets in
  rough chronological order for the four-document Büri/Moto naming
  cluster (R20 `Naming Guide Amendment`, oldest; R21 `Canon Amendment,
  Agamalu and Büri Origin`; R22 `Moto Reversion Ledger`; R23 `Inner World
  Naming Amendment`, newest) plus R24 for the unrelated `Racial Voice and
  Dialect Guide Amendment`. These numerals carry no precedence weight of
  their own — pack_number:null already disables that — they exist only so
  ids satisfy the schema's regex.
- As BRIEF anticipated, the Büri/Moto naming reversion cluster lands
  almost entirely as status:proposed/pending rather than live: the
  Canon Amendment's Section I (4 rulings) and the Moto Reversion Ledger
  are live (explicitly "Isaac's own direction" / cited as authoritative
  by later documents), but the Inner World Naming Amendment — the newest
  and most comprehensive of the four, establishing the actual naming
  baseline — says outright "Originated content pending Isaac's
  ratification" and is entirely status:proposed or status:pending. See
  CONFLICTS.md C-002 for the one specific cross-document ambiguity this
  produced (Filemu Agamalu's own naming).
- This phase's documents are far more worldbuilding-lore-heavy than the
  numbered packs, and much of their content (geology, governance detail,
  character-specific flavour) was not extracted, consistent with BRIEF's
  exclusion of rationale and scene-setting description — only rulings,
  definitions later rules depend on, and open items were kept. This is a
  judgment call specific to Phase 4's very different document shape; flag
  to Isaac if more of the lore content should have been indexed.
