# The Essence Ledger rulings, 2026-09-25 — what was applied and what follows

Isaac answered the WAR-11 questionnaire on 2026-09-25. Six calls, six answers,
each his choice among stated options. This file records what each answer
changed in the repo, what it deliberately did not change, and the one page edit
that is still owed.

Record: six `RULINGS.md` entries dated 2026-09-25, one per row, each headed by
that row's id — `## 2026-09-25 — R44-1-EU_JOULE_ONE_MEGAJOULE` through
`R44-6-BARE_BAND_V_IS_LEVEL_BAND`. They were logged with `log_ruling` under
WAR-96, after WAR-72 found that the single entry this line first pointed at did
not exist.
Index: `rules/doc-essence-ledger-rulings-2026-09-25.yaml`, rows R44-1 to R44-6.
Closed: `CONFLICTS.md` C-034, C-035, C-036, C-037.

## The six answers

| call | answer | what it changes in the repo |
|---|---|---|
| C-034, EU to joules | one constant, 1 EU = 1 MJ stands | R44-1. No card figure touched here; the figures that miss their Stage's band become a card-correction issue of their own. |
| C-035, the AU/s formula | the formula governs, the card figures are the error | R44-2. No card figure touched here; the twenty-six that miss become a card-correction issue of their own. |
| C-036, the S/SS energy gap | the gap is deliberate, rank that range by Sub-Stat | R44-3. Nothing edited. All three tables that carry the break stand as written. |
| C-037, the efficiency conflict | Part Seventeen governs, η 0.60–0.70 at Stage VI–VII | R44-4. One page cell is owed, below. |
| the Stage VI card η figures | the card's η governs per character | R44-5. Nothing edited. Sodoku 0.84, Rashani 0.81, Naiser as written. |
| the bare "Band V" | confirmed, it is the live Level Band | R44-6. Nothing edited. |

## The page edit C-037 names, still owed

The ruling names one cell. Page edits go to Notion and return through the
hourly sync, so this is not a repo diff; it is applied to the Notion page after
review and lands in `wiki/` on the next sync.

Page: **Fracture of Worlds — The Living System / VII. Aether Class, Essence
Typology, Aether Flow (Parts Seventeen–Nineteen)**, the "Efficiency by Tier of
Standing" table, the Tier 5 row (mirror line 97).

As written:

> | 5 · Expert | V–VII Splintering to Refraction | 0.50–0.60 | First genuine efficiency; the Crystal has learned to stop leaking. Dual sight at Refraction allows real-time observation and correction of waste. |

After the edit, the η cell only:

> | 5 · Expert | V–VII Splintering to Refraction | 0.60–0.70 | First genuine efficiency; the Crystal has learned to stop leaking. Dual sight at Refraction allows real-time observation and correction of waste. |

Nothing else on the row moves, and no other row moves. The ladder stays
monotone: Tier 4 ~0.45, Tier 5 0.60–0.70, Tier 6 0.70–0.80.

**Not done, deliberately.** The same page carries its own callout at mirror
line 103 — "**The efficiency conflict, unresolved.** … A ruling is needed on
which scale governs" — which the ruling does not name. It is now false on its
face, but rewriting it means writing words Isaac has not approved, so it is
left exactly as written and asked as its own question on the 2026-09-25
questionnaire.

## What the rulings hand on

Both card-correction sweeps are follow-up issues by the terms of the answers
themselves ("a follow-up issue, not this one"), assigned to the Stat Keeper:

- **C-034's sweep.** Every attested EU figure read at 1 EU = 1 MJ against its
  Stage's Grade band; the misses are card errors. Counts and per-figure
  residuals: `imports/essence-ledger/fit.json`, `reserves` and `costs`.
- **C-035's sweep.** The twenty-six cards whose stated AU/s is not Flux
  Density × η, recomputed. Card-by-card table: `imports/essence-ledger/fit.json`,
  `formula_check`.

## What this does not settle

`imports/essence-ledger/physics-check.md` (WAR-10, in review) reports that
1 EU = 1 MJ fails against real physics and that the failure is structural.
The ruling is dated later than that report and is recorded as made. Nothing
here reconciles the two, and nothing here is a reading of which one the Ledger
Part should print; that sits with WAR-10 and WAR-12.

C-038, C-039 and C-040 were not on the WAR-11 card and stay open. C-038 is the
same shape as C-036 one column over, and R44-3's wording is scoped to the
attack-output column, so it does not reach the travel-speed gap.
