# The rule index: loading and reading it

Folded in from the old `wotr-rules` skill (R79-12). The index at
`/home/oridon/wotr-rule-index` holds every rule from the amendment packs,
the standalone laws and Isaac's dated directions as one YAML row each, with
a `status` that says whether it is in force. It exists so nobody rereads the
packs: you load what a task touches and get back only the rules that govern
it.

## Loading, the lean way (R79-2, R79-8)

The same for every model, Claude, ChatGPT and Codex alike:

1. **Once a session, before the first writing:** the whole live rulebook in
   brief, every rule as one line. `load_rules(tags=[], brief=True)`; if the
   header names parts, read `part=1` through the last.
2. **A domain's full text the first time a task touches it:**
   `load_rules(tags)` for the task's tags, `prose-law` always for prose.
   Rules print newest first; the newer governs where two overlap. The
   `verbatim` is the authoritative wording, the summary a gloss.
3. **No re-read after compaction.**

Without the MCP:

```bash
bash build/py.sh build/query.py --format brief                                   # the brief rulebook
bash build/py.sh build/query.py --applies-to <tag> <tag> ... --format full       # a domain in full
bash build/py.sh build/query.py --applies-to <tags> --status pending proposed --format brief   # the docket
bash build/py.sh build/query.py --id R79-6-FIGHTS_ON_THE_PAGE                     # one rule
```

Bare `python build/query.py` prints a missing-pyyaml error; use `build/py.sh`.

## Domain tags (closed list; `schema/applies_to.md` is canonical)

| tag | fires when the task is |
|---|---|
| `prose-law` | any prose output at all |
| `register` | diction, vocabulary, modern versus period, cultural voice |
| `dialogue` | anyone speaks; prosody, dialect, Isaac's fixed text |
| `pov` | POV lock, distance, dramatic irony, ignorance and misreading |
| `scene-structure` | openings, closings, turn shape, pacing |
| `combat` | duels and small actions between named characters |
| `mass-combat` | a formation exists |
| `adjudication` | who wins, what a stat gap means, what an action costs |
| `stats` | FOW lines, Bands, Grades, Sub-Stats, stat loadouts |
| `magic-mechanism` | how a working is explained on the page |
| `magic-design` | designing a technique, ability or art |
| `codex` | glyph, Wellspring, Family, Physics Domain, Category |
| `naming` | naming a person, place, technique, house or culture |
| `worldbuilding` | setting texture, technology level, material culture |
| `standing-inventory` | per-culture idiom and texture |
| `items` | weapons, armor, artifacts, consumables |
| `character-sheet` | the card, entry format, technique entries |
| `documents` | in-world documents, deliverable format |
| `verification` | `verify_scene` / `build/verify.py`, the self-review pass |
| `session-protocol` | session start and scene end, the Ledger, the Fronts |

## Loadouts by task

| task | tags |
|---|---|
| duel or small fight | `prose-law combat adjudication magic-mechanism pov` |
| battle | `prose-law mass-combat adjudication pov scene-structure` |
| council, court, negotiation | `prose-law dialogue register pov naming` |
| quiet, interior, travel | `prose-law pov scene-structure standing-inventory register` |
| explicit scene | `prose-law dialogue pov scene-structure` |
| a working on the page | `prose-law magic-mechanism combat` (+ `codex` if new) |
| technique or ability design | `magic-design codex stats character-sheet` |
| character sheet | `character-sheet stats naming codex` |
| naming | `naming register worldbuilding` |
| gear | `prose-law items combat adjudication` |
| self-review | `verification prose-law` |

## The docket: decided at the table (R79-2)

`check_docket(tags)` lists what is not ratified: `proposed` means the whole
pack was never ratified; `pending` means the pack is ratified but that item
is open. A docket item that would change what you are writing is decided at
the table and the writing goes on; the call is logged with `log_ruling` as
an agent ruling that names its grounds, and Isaac may overturn it. Nothing
waits.

## A rule reads wrong, contradicts another, or is missing

Do not quietly write around it.

- **Two live rules contradict.** Check `CONFLICTS.md` (`list_conflicts()`);
  it may be logged. If not, record it there with both ids and both verbatim
  lines, pick the reading that serves the scene, write under it, and log the
  call as an agent ruling. Never declare a conflict closed by editing the
  rule files; that happens only through `log_ruling` and the index session.
- **A rule reads wrong in practice.** Name the id and the problem to Isaac
  in one line.
- **Standing caveats:** Pack Six and Pack Twelve are treated as live without
  a ratification line; the Inner World Naming Amendment is treated as
  governing.

Isaac's rulings reach the YAML through `RULINGS.md` (`log_ruling`) and an
index session, followed by `build/validate.py` and `build/resolve.py`. A
writing session never edits `rules/*.yaml`.

## A new amendment pack

Only inside the index repo, after `CLAUDE.md` and `BRIEF.md`, which override
this. In short: the pack goes into `sources/` untouched (read-only forever);
extract to `rules/pack-NN-<name>.yaml`, one row per atomic rule, `verbatim`
an exact quote, `supersedes` naming only what the pack itself says it kills;
`build/validate.py` must exit 0 (fix the data, never the checker);
`build/resolve.py` regenerates `out/`; one pack per commit.

## Files worth knowing

- `out/rules.live.full.md`: the whole live rulebook as one document, by
  domain (regenerated by `resolve.py`).
- `out/docket.md`: everything not yet ratified.
- `CONFLICTS.md`: logged contradictions, with quotes.
- `RULINGS.md`: Isaac's rulings and the agent rulings, written only through
  `log_ruling`.
