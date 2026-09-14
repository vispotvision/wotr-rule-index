---
name: wotr-rules
description: Load the currently-live WOTR craft-law rules for a scene, character sheet, technique design, or naming task from the rule index at /home/oridon/wotr-rule-index. Use before writing any War of the Realms prose, and whenever Isaac asks what the rules say about something.
---

# WOTR rule index

The index at `/home/oridon/wotr-rule-index` holds every rule from the
nineteen amendment packs and the standalone amendments as one YAML row each,
with a `status` that tells you whether it is currently in force. It exists so
you never have to reread the packs: you query it for the tags a task touches,
and you get back only the rules that govern that task.

Path shorthand below: `$IDX` = `/home/oridon/wotr-rule-index`.

## Mode 1 — load rules for a task (the usual case)

1. Work out which `applies_to` tags the task touches (table below). Two to
   four tags is typical. When in doubt, include `prose-law` — it fires on any
   prose at all.
2. Run:
   ```
   python $IDX/build/query.py --applies-to <tag> <tag> ... --format full
   ```
   Rules print newest pack first, so the governing rule appears before the one
   it amended. Read the whole output before writing.
3. Also check whether anything the task touches is still undecided:
   ```
   python $IDX/build/query.py --applies-to <same tags> --status pending proposed --format brief
   ```
   If a pending/proposed rule would materially change the scene, say so to
   Isaac before writing rather than silently picking a side. `proposed` means
   the whole pack was never ratified; `pending` means the pack is ratified but
   that specific item is an open ruling on the docket.
4. Write the prose under the live rules. In your self-review, cite the rule
   ids you were most constrained by — Isaac uses the ids to correct the index
   when a rule reads wrong in practice.

`--format brief` gives id + summary only (good for a first look); `full` adds
the verbatim source text, which is the authoritative wording. `--id R15-2-ONE_TEST`
fetches a single rule. `--pack 12` restricts to one pack.

### Tag vocabulary (closed — `$IDX/schema/applies_to.md` is canonical)

| tag | fires when the task is |
|---|---|
| `prose-law` | any prose output at all: bans, budgets, sentence-level rules |
| `register` | diction, vocabulary level, modern-versus-period, cultural voice |
| `dialogue` | anyone speaks; also prosody, dialect, Isaac's fixed text |
| `pov` | POV lock, psychic distance, dramatic irony, ignorance and misreading |
| `scene-structure` | openings, closings, length bands, turn shape, pacing |
| `combat` | duels and small actions between named characters |
| `mass-combat` | a formation exists |
| `adjudication` | deciding who wins, what a stat gap means, what an action costs |
| `stats` | FOW lines, Bands, Grades, Coherence, Sub-Stats, stat loadouts |
| `magic-mechanism` | how a working is explained on the page |
| `magic-design` | designing a new technique, ability or art |
| `codex` | glyph, Wellspring, Family, Physics Domain, Category assignment |
| `naming` | naming a person, place, technique, house or culture |
| `worldbuilding` | setting texture, technology level, material culture |
| `standing-inventory` | per-culture idiom, recurrence, the elegiac mode |
| `items` | weapons, armour, artefacts, consumables |
| `character-sheet` | sheet template, entry format, technique cards |
| `documents` | in-world documents, deliverable format, .docx production |
| `verification` | wotr_verify.sh, check numbers, the self-review pass |
| `session-protocol` | session start and end, State of Play, Ledger, Fronts |

### Common loadouts

| task | tags |
|---|---|
| duel / small fight between named characters | `prose-law combat adjudication magic-mechanism pov` |
| battle with formations | `prose-law mass-combat adjudication pov scene-structure` |
| council, court, negotiation, any talky scene | `prose-law dialogue register pov naming` |
| quiet / interior / travel scene | `prose-law pov scene-structure standing-inventory register` |
| a working is performed on the page | `prose-law magic-mechanism combat` (+ `codex` if the working is new) |
| designing a new technique or ability | `magic-design codex stats character-sheet` |
| building or revising a character sheet | `character-sheet stats naming codex` |
| naming anyone or anything | `naming register worldbuilding` |
| firearms, armour, gear on the page | `prose-law items combat adjudication` |
| self-review before handing a scene back | `verification prose-law` |
| starting or closing a session | `session-protocol` |

## Mode 2 — a rule seems wrong, contradictory, or missing

Do not quietly write around it. Two things can be true:

- **Two live rules contradict.** Check `$IDX/CONFLICTS.md` — it may already be
  logged (C-001, C-002, ...). If not, tell Isaac the two ids and the two
  verbatim lines. Never decide the winner yourself; that is Isaac's rule for
  reading, not yours (`$IDX/CLAUDE.md`).
- **The rule is unratified.** The three biggest interpretive calls in the index
  are that Pack Six and Pack Twelve are treated as fully live (neither carries a
  status line) and that the Inner World Naming Amendment is entirely
  `proposed`. If a scene hangs on one of these, flag it.

Isaac's rulings get applied to the YAML by whoever is working in `$IDX`, one
commit per ruling batch, followed by `python build/validate.py` and
`python build/resolve.py`. Do not edit `$IDX/rules/*.yaml` from a writing
session — note the ruling and hand it off.

## Mode 3 — a new amendment pack exists

Only do this when working inside `$IDX`, and read `$IDX/CLAUDE.md` and
`$IDX/BRIEF.md` first; they override everything here. In short:

1. The pack goes into `$IDX/sources/` untouched. `sources/` is read-only forever.
2. Extract it to `$IDX/rules/pack-NN-<name>.yaml`, one row per atomic rule,
   `verbatim` an exact quote, `supersedes` naming only what the pack itself
   says it kills in quotable words. Follow the header-comment conventions in
   the neighbouring pack files (ratification reasoning goes in the header).
3. `python build/validate.py` must exit 0. Fix the data, never the checker.
4. `python build/resolve.py` regenerates `out/rules.live.md`, `out/docket.md`
   and `out/rules.resolved.json`. Update `PROGRESS.md`; log anything you could
   not settle in `CONFLICTS.md`.
5. One pack per commit.

## Files worth knowing

- `$IDX/out/rules.live.md` — the whole live rulebook as one document
  (regenerate with `resolve.py`; it is gitignored). Use it when a task is too
  broad for tags, e.g. a full-chapter review.
- `$IDX/out/docket.md` — everything still waiting on Isaac.
- `$IDX/PROGRESS.md` — per-pack ledger and the list of the ten open items most
  likely to change how a scene is written.
- `$IDX/CONFLICTS.md` — logged contradictions, with quotes, awaiting ruling.
