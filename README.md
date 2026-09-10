# WOTR Rule Index

Nineteen amendment packs and a handful of standalone amendments, converted from
prose into a queryable index of discrete rulings.

The point: a combat scene should load the eleven live rules that touch combat,
not nineteen documents. And a ruling Isaac makes should flip one field, not
require anyone to remember which pack it lived in.

## Start here

1. `CLAUDE.md` — hard constraints. Read first, they are not optional.
2. `BRIEF.md` — the actual job, in five phases.
3. `schema/pack_structure.md` — how the three families of pack are laid out.
4. `rules/pack-15-fifteen.yaml` — a real worked example against real source text.

```
pip install -r requirements.txt
cd build && python3 validate.py    # PASS on the example as shipped
python3 resolve.py
python3 query.py --applies-to combat adjudication --format full
```

## Layout

```
sources/    the amendment corpus. read-only. never edit.
rules/      one yaml per source document. this is the work.
schema/     rule schema, closed tag vocabulary, pack structure notes
build/      validate, resolve, query
out/        generated. rules.resolved.json, rules.live.md, docket.md
CONFLICTS.md  things needing Isaac. the extraction never decides these itself.
PROGRESS.md   phase tracker. this job spans sessions.
```

## The two properties that matter

**Every rule carries its source quote.** `validate.py` checks that the
`verbatim` field appears in the source file after stripping markdown and
collapsing whitespace. A paraphrase that drifts fails the build. This is what
stops the index quietly becoming a different rulebook than the packs.

**Supersession is quoted, never assumed.** "Later pack beats earlier pack" is
how Isaac reads the corpus. It is not licence for the extraction to mark rules
dead. A `supersedes` link exists only where a pack says so in words you can
point at, usually in a Consequential Edits section. Everything else goes to
`CONFLICTS.md`.

## What this feeds

`out/rules.resolved.json` is the context source for the drafting pipeline: query
by task tags, get the live loadout, ship that to the writing step instead of the
whole corpus. `out/docket.md` regenerates the Open Rulings page.
