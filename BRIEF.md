# BRIEF — Build the WOTR Rule Index

## What this is for

War of the Realms has nineteen amendment packs plus several standalone
amendment documents. They amend a set of base craft guides. Precedence is
"later pack beats earlier pack," which is unreadable at this volume, so in
practice nobody can say with confidence which rules are live when writing a
scene.

Your job is to convert that pile of prose into a queryable index of discrete
rulings, so that a scene about combat can load the eleven live rules that touch
combat instead of nineteen documents.

You are not folding the packs into the base guides. You are not rewriting
anything. You are extracting, tagging and linking.

## Output

For each source document, one YAML file in `rules/` named `pack-NN-name.yaml`
(or `doc-<slug>.yaml` for standalone amendments), containing a list of rule
rows conforming to `schema/rule.schema.json`.

Then `build/resolve.py` produces:
- `out/rules.resolved.json` — every rule with supersession links walked
- `out/rules.live.md` — human-readable, grouped by `applies_to`
- `out/docket.md` — every row with `status: pending`, which is Isaac's Docket

`CONFLICTS.md` accumulates everything you could not resolve without a ruling.

## What counts as one rule

A rule row is **one enforceable proposition**. Not a section, not a paragraph.

Split when a section contains several independently checkable things. Pack
Fifteen §1 is not one rule; it is a licence, seven repeals and five survivals,
and each of those is separately true or false about a given draft.

Do extract:
- mandates, bans, budgets, floors, caps, procedures
- repeals and supersessions of earlier rules
- definitions that later rules depend on
- open rulings (anything with an R-code, or marked pending, proposed, or
  awaiting Isaac)
- consequential edits that name a target guide

Do not extract:
- worked examples, before/after prose demonstrations, rationale, diagnosis of
  what went wrong in some past draft

Rationale is often the bulk of a pack. It is context, not rule. If a paragraph
explains *why*, skip it. If it says *do* or *never*, extract it.

## Fields that matter most

- `verbatim` — exact quoted text from the source, whitespace-normalised. This is
  the integrity anchor and `validate.py` checks it appears in the file.
- `amends` — which base guide and where. Packs One through Four state this
  explicitly in a `## Target:` heading; use it. Later packs usually name targets
  in a "Consequential Edits" section; use that. If a pack names no target, set
  `amends: null` rather than guessing.
- `supersedes` — list of rule IDs this kills. Only populate when the source says
  so in quotable words: "struck," "repealed," "replaced," "demoted," "no longer,"
  or a named pack and section. Pack Fifteen §4 and Pack Twelve §1 are dense with
  these and are the highest-value extractions in the corpus.
- `applies_to` — closed vocabulary in `schema/applies_to.md`. This is the query
  key the pipeline uses. Tag generously but only from the list.
- `verification` — if the rule names a check number or a `wotr_verify.sh` flag,
  record it. This is how mechanical enforcement gets wired later.

## Phases — stop and report after each

**Phase 0.** Read `schema/pack_structure.md`. Open one pack from each of the
three structural families and confirm the heading conventions still hold. Write
nothing except a short report of what you found. If a family does not parse the
way the notes claim, say so before proceeding.

**Phase 1.** Packs Nineteen down to Eleven, newest first. These use `## §N`
headings and are the packs that actually fire during a scene. Newest first
matters: later packs name what they kill, which seeds the supersession graph
before you meet the victims.

**Phase 2.** Packs Ten down to Five.

**Phase 3.** Packs Four down to One, including `WOTR_Companion_Guide_Amendments.md`
which is Pack One and has no number in its filename. These use
`# AMENDMENT N` + `## Target:` and are the easiest to extract but the most
likely to be already dead.

**Phase 4.** The standalone amendments in `sources/`: Racial Voice Guide
Amendment, Inner World Naming Amendment, Moto Reversion Ledger, the Agamalu and
Büri origin amendment, and `WOTR_Naming_Guide_Amendment.docx` (convert with
`pandoc -t plain`, do not guess at its contents).

**Phase 5.** Run `build/resolve.py`. Produce the conflict report. Summarise:
how many rules total, how many live, how many superseded, how many pending, and
the ten conflicts you think are most likely to change how a scene gets written.

## Known live-fire cases to get right

- **Pack Twelve §1 repeals Pack Seven in full.** Every Pack Seven rule should
  end up `status: superseded` with `superseded_by` pointing at the Twelve §1 row.
  If your extraction does not produce that, your supersession logic is wrong.
- **Pack Fifteen repeals the register rules** across Packs Five, Nine, Twelve and
  the Racial Voice guide. Its §4 lists targets by pack and section. This is the
  single densest supersession node in the corpus.
- **The Büri/Moto naming reversion** spans the Moto Reversion Ledger, the Inner
  World Naming Amendment and the Agamalu amendment, and Isaac's definitive
  ruling is still outstanding. Expect these to land as `status: pending` with a
  conflict row, not as live rules.
- **Pack Eight** has no `§` sections; it uses `## SECTION ONE` and `### 1.1`.
  Do not skip it because the parser misses it.

## Style of work

Commit per pack with the pack name in the message. Keep `PROGRESS.md` current as
you go, since this job will span sessions. When you hit something that needs
Isaac, write the row in `CONFLICTS.md` in the format already there and keep
moving; do not stall the whole extraction on one ambiguity.
