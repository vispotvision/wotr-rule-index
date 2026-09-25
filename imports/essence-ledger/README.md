# imports/essence-ledger — the Essence Ledger's working data and draft

Phases 1 to 3 of the Essence Ledger (parent WAR-8): WAR-9 the fit, WAR-10 the
physics check, WAR-12 the draft Part. Nothing here is canon and nothing here
edits canon. It is the collected evidence, the arithmetic done against it, and
the Part drafted on top, so a ruling and Phase 4's publication have something
to stand on.

## What is in here

| file | what it is |
|---|---|
| `anchors.json` | **the deliverable.** Every attested essence figure in the wiki mirror — EU reserve, AU/s, Flux Density, η, **and joules** — with its entity, the Level / Stage / Tier of Standing / Aether Class / Coherence Band / Tier Grades stated on the same page, the exact file and line, and a verbatim quote of the whole line. Plus the system tables the fit reads against, lifted verbatim from FoW Parts Four, Five and Nineteen; the absolute EU costs (`costs`); the joule figures (`joules`, each classed `attested`, `band_edge_quoted`, `system_table` or `withdrawn`); and the figures canon says do not exist (`unquantified`). An entity is read off the line rather than off the page (`entity_basis`), and a row restating a figure already recorded carries `duplicate_of`. |
| `fit.json` | the fit. The measured side first — `direct_pairs` (a working whose EU cost and joule output are both stated), `grade_proxy_check` (the Stage→Grade proxy measured against the attested joules) and `reserve_vs_strike`. Then the proxy: per-anchor residuals at Isaac's 1 EU = 1 MJ, the best single constant, the residual by Stage, and the AU/s = Flux Density × η check card by card. |
| `physics-check.md` | WAR-10, Phase 2. The fitted constant against real physics: the low end (a body's heat capacity against η's waste), the high end (E = mc² against the million-EU/g sheets), the Grade table's joule → TNT → "what it wrecks" chain against cube-root blast scaling, the drain arithmetic, and where the energy η discards goes. Written after Phase 1 and against its two data files; it changes no figure, adopts no constant and files no conflict row. |
| `extract_anchors.py` | the sweep. Walks `wiki/**/*.md`, finds figures carrying one of the four units, writes `_candidates.json`. Parses a number only where the form is unambiguous. |
| `build_anchors.py` | `_candidates.json` + the verbatim system tables + a short hand supplement → `anchors.json`. |
| `fit.py` | `anchors.json` → `fit.json` and the printed report. |
| `_candidates.json` | the raw sweep, written by `extract_anchors.py` and consumed by `build_anchors.py`. A regenerable intermediate; not committed. |
| **`the-essence-ledger.md`** | **WAR-12, Phase 2. The deliverable of this phase: the draft FoW Part Twenty-Three, "The Essence Ledger".** The constant with its residuals, the EU → J → Grade → TNT chain joined to Part Four, reserve bands per Stage and per Tier of Standing with every attested character placed in them, AU/s as power with the drain arithmetic and three worked scales, Flux Density against η stated as an equation with the residual column, and Essence Starvation and recovery in the new units. Nothing in it is published; every claim carries a `[canon]`, `[derived]` or `[draft]` marker and every slot a ruling must fill is marked **PENDING** with the question named. |
| `ledger_tables.py` | WAR-12. Every table the Part prints, from `anchors.json` and `fit.json` only: the constant fit, the reserve law on Level, the bands by Stage and Tier, the nine-rung spine, the drain and waste-heat clocks, the Flux × η residual, and the recovery rates. |
| `ledger_tables.json` | what `ledger_tables.py` writes. The Part's arithmetic, machine-readable. |

## Running it

```bash
python imports/essence-ledger/extract_anchors.py   # sweep  -> _candidates.json
python imports/essence-ledger/build_anchors.py     # build  -> anchors.json
python imports/essence-ledger/fit.py               # fit    -> fit.json + report
python imports/essence-ledger/ledger_tables.py     # tables -> ledger_tables.json + report
```

All four are read-only against `wiki/` and write only inside this folder.

## What the fit found

**Measured.** Canon states an EU cost and a joule output for the same working
three times, all on Dougou Ozumu Zettari's sheet and his Spellcraft page. They
price one EU at **112 to 3,571 joules** — two to four decades below 1 EU = 1 MJ.
The thirteen characters who state both a reserve and a strike put a ceiling on
the same quantity that spans 11.2 decades, 217 to 3.3×10¹³ J/EU.

**By proxy.** Where no joules are stated, an EU figure is read against the band
its Stage's Max Grade claims. At 1 EU = 1 MJ, 25 of 155 figures land in band;
the best single constant, 6.2×10⁶ J/EU, reaches 65. It cannot do better, because
the attested EU figures are not ordered by Stage: Stage XII alone spans 9.8
orders of magnitude, and a Stage XIII reserve (92,000 EU) sits below a Stage V
one (185,000 EU). The residual is Stage-shaped, from +0.98 decades at Stage III
to −13.69 at Stage XIV. The proxy itself is checkable and imperfect: against the
nineteen attested Strike Force figures it agrees seven times and is out by one to
seven Grades on the rest.

Logged as `CONFLICTS.md` C-034 (the measured conversion and the unordered
reserves), C-035 (the AU/s formula fails on 26 of 29 cards), C-036 (the S/SS gap
in the Grade table), C-037 (the η conflict), C-039 (the SSS ceiling written EJ
for ZJ) and C-040 (twelve Strike Force figures against their Stage's Grade). All
are Isaac's to rule. **No card figure was changed.**

## What Phase 2 (WAR-12) found, and what it could not settle

**The constant.** The brief's 1 EU = 1 MJ misses canon's only three self-pricing
lines by 2.4 to 3.0 decades, breaks E = mc² on Draen Varos's nine-kilogram
crystal and on Kaelzar, and kills every practitioner with their own waste heat
inside a second. **The draft works at 1 EU = 1 kJ, 1 AU/s = 1 kW** — inside two
of the three measured windows and 0.034 decades outside the third, inside all
four of the physical brackets `physics-check.md` §6 lists, and the constant at
which Dougou Ozumu Zettari's sheet closes end to end: 7,400 EU buys 7.33 MJ,
which is where The Iron Tree says that working lands, and his reserve holds
twelve apex strikes. C-034 stays open; the draft marks every table that rests
on it.

**The reserve table the cards say does not exist.** The method was already
ruled — `Summoned and Bound/Obrenkael · The Mule.md:215`, 2026-09-12: a
log-linear interpolation on **Level**. Fitted to its own three anchors it gives
**0.012812 decades per Level, a factor of ten every 78 Levels**, and the two
segments of the ruled line agree to 1.7 percent. Put through Part One's four
Band gates it gives a hard reserve ceiling per Stage: **29 of the 31 attested
reserves sit under it, and 22 of 31 within one decade of the working band.**
The two that do not are Gimbzo (inside C-034 already) and Sodoku Moto, whose
Level and Stage are themselves past a Band gate — filed this phase as **C-041**,
with Krothar Veylshroud.

**Two things the draft states and does not file.** `AU/s = Flux Density × η` is
dimensionally short one mass (EU/g on the right, EU/s on the left); solved for
it, 21 of 29 cards imply a mass between 0.2 g and 10 g and the three the
identity already fits imply exactly 1 g — but Draen Varos, the one card that
states a Crystal mass, implies 0.00024 g against his own nine kilograms. And
the attested recovery rates come in two populations two decades apart: six
cards state 9–28% of reserve per minute, four state absolute figures that work
out at 0.025–3.1%. Both are named as PENDING questions in the Part rather than
filed, because a single sentence from Isaac settles either and neither is
plainly a contradiction.

## What `figure_class` means, and what WAR-17 changed

A joule figure is `system_table` where it sits on one of the pages that define
the ladders, `band_edge_quoted` where it is within 2% of a ladder figure — the
line is citing the band, not measuring anything — and `attested` where the page
states it for itself. Two restrictions keep the middle class honest, added under
WAR-17 after the round-2 review of WAR-9:

*   **Same measure.** Part Eleven runs two joule ladders, Strike Force and
    Durability, over the same range of numbers. A figure is matched only against
    the ladder for the measure its own line states — read off the field label
    where there is one, else off the measure named nearest the figure in the
    line, else the attack-output ladder, which is the one Part Four grades. Each
    row carries that reading as `figure_measure` and `figure_measure_basis`.
*   **Ladder rows only.** A number used to illustrate a rule in prose ("A Shell
    rated at 5 TJ absorbs 5 TJ") is not a band edge, so only the rows of the
    tables are matched against.

Two rows changed class and one changed what it matched. Karo Venrik's
**Strike Force** 300 MJ had been read as a citation of the F-Grade *Durability*
row, 0.1–0.3 GJ; it is an `attested` card figure, and it is the nineteenth
strike row in `grade_proxy_check` (C-040). Corona Lunaris's superseded 100 GJ
threshold had been read against the C-Grade Durability row, and is `attested`.
Souma Byakuya Moto's 0.005 PJ Durability keeps its class but now matches the
B-Grade Durability ceiling rather than Part Eleven's prose illustration, the two
being the same 5 TJ. Nothing else moved, and no card figure was changed.
