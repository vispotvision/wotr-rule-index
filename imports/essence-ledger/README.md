# imports/essence-ledger — the Essence Ledger's working data

WAR-9, Phase 1 of the Essence Ledger (parent WAR-8). Nothing here is canon and
nothing here edits canon. It is the collected evidence and the arithmetic done
against it, so a later phase and a ruling have something to stand on.

## What is in here

| file | what it is |
|---|---|
| `anchors.json` | **the deliverable.** Every attested essence figure in the wiki mirror — EU reserve, AU/s, Flux Density, η, **and joules** — with its entity, the Level / Stage / Tier of Standing / Aether Class / Coherence Band / Tier Grades stated on the same page, the exact file and line, and a verbatim quote of the whole line. Plus the system tables the fit reads against, lifted verbatim from FoW Parts Four, Five and Nineteen; the absolute EU costs (`costs`); the joule figures (`joules`, each classed `attested`, `band_edge_quoted`, `system_table` or `withdrawn`); and the figures canon says do not exist (`unquantified`). An entity is read off the line rather than off the page (`entity_basis`), and a row restating a figure already recorded carries `duplicate_of`. |
| `fit.json` | the fit. The measured side first — `direct_pairs` (a working whose EU cost and joule output are both stated), `grade_proxy_check` (the Stage→Grade proxy measured against the attested joules) and `reserve_vs_strike`. Then the proxy: per-anchor residuals at Isaac's 1 EU = 1 MJ, the best single constant, the residual by Stage, and the AU/s = Flux Density × η check card by card. |
| `extract_anchors.py` | the sweep. Walks `wiki/**/*.md`, finds figures carrying one of the four units, writes `_candidates.json`. Parses a number only where the form is unambiguous. |
| `build_anchors.py` | `_candidates.json` + the verbatim system tables + a short hand supplement → `anchors.json`. |
| `fit.py` | `anchors.json` → `fit.json` and the printed report. |
| `_candidates.json` | the raw sweep, written by `extract_anchors.py` and consumed by `build_anchors.py`. A regenerable intermediate; not committed. |

## Running it

```bash
bash build/py.sh imports/essence-ledger/extract_anchors.py   # sweep  -> _candidates.json
bash build/py.sh imports/essence-ledger/build_anchors.py     # build  -> anchors.json
bash build/py.sh imports/essence-ledger/fit.py               # fit    -> fit.json + report
```

All three are read-only against `wiki/` and write only inside this folder.

## What the fit found

**Measured.** Canon states an EU cost and a joule output for the same working
three times, all on Dougou Ozumu Zettari's sheet and his Spellcraft page. They
price one EU at **112 to 3,571 joules** — two to four decades below 1 EU = 1 MJ.
The twelve characters who state both a reserve and a strike put a ceiling on the
same quantity that spans 11.2 decades, 217 to 3.3×10¹³ J/EU.

**By proxy.** Where no joules are stated, an EU figure is read against the band
its Stage's Max Grade claims. At 1 EU = 1 MJ, 25 of 155 figures land in band;
the best single constant, 6.2×10⁶ J/EU, reaches 65. It cannot do better, because
the attested EU figures are not ordered by Stage: Stage XII alone spans 9.8
orders of magnitude, and a Stage XIII reserve (92,000 EU) sits below a Stage V
one (185,000 EU). The residual is Stage-shaped, from +0.98 decades at Stage III
to −13.69 at Stage XIV. The proxy itself is checkable and imperfect: against the
eighteen attested Strike Force figures it agrees seven times and is out by one to
seven Grades on the rest.

Logged as `CONFLICTS.md` C-034 (the measured conversion and the unordered
reserves), C-035 (the AU/s formula fails on 26 of 29 cards), C-036 (the S/SS gap
in the Grade table), C-037 (the η conflict), C-039 (the SSS ceiling written EJ
for ZJ) and C-040 (eleven Strike Force figures against their Stage's Grade). All
are Isaac's to rule. **No card figure was changed.**
