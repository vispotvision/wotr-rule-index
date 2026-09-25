# WAR-46 — the R44-1 EU-band sweep: every attested EU figure at 1 EU = 1 MJ

Ruling: `RULINGS.md`, 2026-09-25, C-034; `rules/doc-essence-ledger-rulings-2026-09-25.yaml` R44-1.
Input: `imports/essence-ledger/fit.json` (`reserves`, `costs`, `grade_proxy_check`), built for WAR-9 and corrected for WAR-71.
Written by the Stat Keeper, 2026-09-25; regenerated the same day against the corrected fit. **No card figure was changed by this sweep.**

Two defects this sweep found in the fit it reads have since been fixed in the extractor (WAR-71), and this file is the run after that fix. A figure on a table row that states its own gate Stage is now read against that Stage rather than against the page's entry Stage, and the Tier 5 η is R44-4's 0.60–0.70 rather than the mirror's pre-ruling 0.50–0.60. The counts below moved accordingly and the `GATE` reason is gone with the defect that produced it; §"What moved when the fit was corrected" records what changed.

## What the ruling asks for, and what it supplies

> One constant: 1 EU = 1 MJ stands. The Ledger converts at 1 MJ everywhere, and the card figures that then sit outside their Stage's band are the error; each is a card correction in its own issue, not in this ruling batch.

R44-1 settles the constant and names a class of figures as wrong. It does not say what any corrected figure becomes, and no card states a replacement. Under house rule 3.3 a number that is not on a card, in a Magic System table or from `fow_line` is not available to write, so this sweep reads every figure, reports every miss, and sets none of them. Every line below is logged with the reason nothing was set.

## One thing to know before the counts: the draft Part works at a different constant

`imports/essence-ledger/the-essence-ledger.md` — the draft FoW Part Twenty-Three, WAR-12, on master — works at **1 EU = 1 kJ**, three decades below the constant this sweep reads at, and says so at §2.3: "**[draft] 1 EU = 1 kJ of potential. Energy delivered = EU × η × 1 kJ. 1 AU/s = 1 kW.**" It is not a rival ruling and this file does not treat it as one. The Part says of itself, at the C-034 PENDING note: "Every table below is built at 1 kJ and inherits whichever way Isaac rules." R44-1 is that ruling and it went the other way, so the draft owes itself a rebuild at 1 MJ. That is WAR-12's work and is filed separately; nothing in this sweep depends on it, because this sweep reads at the ruled constant and changes nothing either way.

## The reading

Each attested EU figure is converted at 1 EU = 1 MJ, taken through the η that its page states (or the Part Nineteen tier midpoint for its Stage's Tier of Standing where the page states none), and read against the attack-output band that its Stage's Max Grade claims in Part Four. The chain is Part Five's Stage gate table → the Stage's Max Grade → Part Four's joule column.

"Its Stage" is the Stage the figure's own line states where the table it sits in gates its rows one by one, and the Stage the page states otherwise — `stage_basis` on every row of `fit.json` says which was read. Where the η comes off Part Nineteen's Tier 5 row it is the ruled 0.60–0.70, midpoint 0.65: R44-4 corrects that cell and the mirror has not re-exported it yet, so `anchors.json` keeps the mirror's row in `verbatim` and reads the ruling's figures.

> Part Seventeen governs: η reads 0.60 to 0.70 at Stage VI–VII. Part Nineteen's Tier 5 row is corrected to match.

Part Five, `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md:67`:

> | IV | Flourishing | B | 275 | 4 · Adept |

Part Four, the same file `:33`:

> | B | 176–275 | 1.046×10^9 – 4.6024×10^10 J | Mach 1.5–4 |

Two things about that chain are recorded here and decided nowhere. Part Five says what the Max Grade column does, same file `:60`:

> The Max Grade column binds allocation: a Sub-Stat may not be allocated past the top of the Stage's Max Grade bracket.

It binds allocation of a Sub-Stat. Reading it as a ceiling on delivered joules is a proxy, and reading a stored EU reserve against an *attack-output* column is a second proxy on top of it. Both are how WAR-9 fitted the corpus and how this issue words the job; neither is a sentence any page writes. Nothing here rests on choosing otherwise, because no figure is changed.

## What the sweep found

| | count |
|---|---|
| attested EU figures with a band to read against | 155 |
| inside their Stage's band at 1 EU = 1 MJ (delivered, through η) | 27 |
| **outside it** | **128** |
| attested EU figures with no Grade available for the reading | 4 |
| distinct files the misses sit in | 50 |
| distinct entities | 49 |
| misses that read **below** their band | 126 |
| misses that read **above** their band | 2 |

The WAR-11 card put the miss at 137 of 165; this sweep reads 128 of 155, the difference being the figures that carry no band and the duplicate anchors `fit.json` keeps apart. The direction is one-sided: 126 of the 128 misses read below the band their Stage claims, most of them by two decades or more.

## What moved when the fit was corrected

The first run of this sweep, before WAR-71, read 25 of 155 in band and 130 out, six of the misses above their band, and logged the reasons `C-040` 48, `GATE` 4, `NOT-A-CARD-FIGURE` 11, `DERIVED` 2, `NO-TARGET` 65. Two corrections to the fit it reads moved those counts, and neither is a card correction:

- **the Stage a gated row is read against.** `imports/essence-ledger/extract_anchors.py` now carries the Stage a table row states for itself wherever the table gates its rows one by one, and `fit.py` reads that Stage. 4 figures in the corpus carry such a Stage. On `The Disciplines/Rusashin — The Dust That Remembers What It Touched.md` the four Forms the fit had been reading against Stage III, the discipline's entry, are read at the Stages its `Gate` column writes: Form II at IV, Form VII at VII–VIII, Form VIII at VIII–IX, Form IX at IX–X, each taken at the low end of its range, the Stage the row opens at. Form II at 4,000 EU lands inside B-Grade and leaves the log; the other three flip from above their band to below it and are logged `NO-TARGET`. The `GATE` reason existed only to record this misreading and is gone with it.
- **the Tier 5 η.** R44-4 corrects Part Nineteen's Tier 5 row from 0.50–0.60 to 0.60–0.70 and the page edit it names has not come back through the hourly sync, so `build_anchors.py` now reads the ruling's figures and keeps the mirror's row in `verbatim` (`anchors.json`, `system.eta_by_tier`, `corrected_by_ruling`). 16 lines take their η there, one more than the fifteen the first run counted, because Rusashin Form VII moved onto Stage VII and so onto Tier 5 with the first correction. Every delivered figure on them rises 18%. `Spellcraft/Vainglory.md:28` at 75,000 EU was the only row within that distance of a band edge and it is now inside the band, so it leaves the log too.

Nothing else moved: the same 155 figures carry a band, the same 4 carry none, and the twelve cards `C-040` names are the same twelve. No card figure was changed by either correction, and neither touches the constant.

## Why no figure was set

Four reasons, in the order they were applied. Each line in the log carries exactly one.

| reason | lines | what it means |
|---|---|---|
| `C-040` | 48 | The figure sits on one of the twelve cards `CONFLICTS.md` C-040 names, where the Stage-to-Grade chain is measured out by one to seven Grades. The band itself is contested on that card, so the correction depends on C-040 and this issue stops rather than deciding it. |
| `NOT-A-CARD-FIGURE` | 10 | The line says in words that the figure is an estimate, an extrapolation or not stated on the card. R44-1 names *card figures*; extending it to these would extend a ruling to a case it does not name (house rule 3.2). |
| `DERIVED` | 2 | The figure is written as a stated fraction of another figure on the same page — a percentage of a reserve — so it cannot be corrected without first correcting the reserve it is taken from. |
| `NO-TARGET` | 68 | A plain stated figure, outside its band, and the ruling gives no value to put in its place. |

`NO-TARGET` is the reason that would survive every other one being answered, and it is the reason the sweep cannot run at all. "Inside the band" is a range, not a number. Across the 128 misses the in-band window is 0.76 decades wide at its narrowest, 1.96 at the median and 8.75 at its widest — at Stage XII the SSS band runs 4.184×10^14 to 4.184×10^21 J, so a "corrected" figure would be a free choice across seven orders of magnitude. Nothing on any of these cards names a point inside that window, so every replacement value would be invented.

The one place canon prices a working both ways does not supply a target either. Dougou Ozumu Zettari's sheet and `Spellcraft/The Iron Tree.md` state an EU cost and a joule output on the same line three times (`fit.json`, `direct_pairs`), so the EU figure could in principle be re-derived from the stated joules; but those stated joules are themselves seven Grades below his Stage XIII band, which is C-040's largest row. Correcting the EU to agree with them would land the figure further outside the band the ruling reads it against, not inside it.

## The log — 128 lines, nothing set

`dec` is decades (log₁₀) outside the band, delivered through η; negative reads below the band, positive above. `band` is the Stage's Max Grade. A Stage marked *(own gate)* was read off the line's own gate cell rather than off the page.

| entity | file:line | Stage | band | EU | η | J at 1 MJ, delivered | dec | reason |
|---|---|---|---|---|---|---|---|---|
| Amaranth Severance · The Blooming Thorn | `wiki/Artifacts/Amaranth Severance · The Blooming Thorn.md:35` | 7 | A | 60 | 0.65 | 3.9e+07 | -3.07 | `NOT-A-CARD-FIGURE` |
| Chimwala N'Doro | `wiki/Artifacts/Upanga wa Msimu Nne · Blade of the Four Seasons.md:29` | 8 | S | 2,400 | 0.75 | 1.8e+09 | -3.37 | `NOT-A-CARD-FIGURE` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:17` | 12 | SSS | 4.2e+06 | 0.91 | 3.82e+12 | -2.04 | `NO-TARGET` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:56` | 12 | SSS | 45,000 | 0.91 | 4.1e+10 | -4.01 | `NO-TARGET` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:85` | 12 | SSS | 12,000 | 0.91 | 1.09e+10 | -4.58 | `NO-TARGET` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:93` | 12 | SSS | 14,000 | 0.91 | 1.27e+10 | -4.52 | `NO-TARGET` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:107` | 12 | SSS | 180,000 | 0.91 | 1.64e+11 | -3.41 | `NO-TARGET` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:126` | 12 | SSS | 20,000 | 0.91 | 1.82e+10 | -4.36 | `NO-TARGET` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:146` | 12 | SSS | 4,000 | 0.91 | 3.64e+09 | -5.06 | `NO-TARGET` |
| The Arctic Lion — Sovereign Configuration (Level 500) | `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md:150` | 12 | SSS | 8,000 | 0.91 | 7.28e+09 | -4.76 | `NO-TARGET` |
| Edictum | `wiki/Spellcraft/Edictum.md:39` | 7 | A | 70,000 | 0.65 | 4.55e+10 | -0.00 | `NOT-A-CARD-FIGURE` |
| Invert Eidolon | `wiki/Spellcraft/Invert Eidolon.md:28` | 8 | S | 150,000 | 0.75 | 1.12e+11 | -1.57 | `NOT-A-CARD-FIGURE` |
| Muken Moto | `wiki/Spellcraft/Mugen no Hatsurugi.md:20` | 10 | SS | 90,000 | 0.75 | 6.75e+10 | -2.79 | `NO-TARGET` |
| Zeven Halek | `wiki/Spellcraft/Oathrend.md:39` | 9 | S | 130,000 | 0.75 | 9.75e+10 | -1.63 | `NOT-A-CARD-FIGURE` |
| Scission | `wiki/Spellcraft/Scission.md:39` | 6 | A | 60,000 | 0.65 | 3.9e+10 | -0.07 | `NOT-A-CARD-FIGURE` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:20` | 13 | X | 2,800 | 1.07 | 3.01e+09 | -12.14 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:20` | 13 | X | 7,400 | 1.07 | 7.96e+09 | -11.72 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:20` | 13 | X | 8,900 | 1.07 | 9.57e+09 | -11.64 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:20` | 13 | X | 92,000 | 1.07 | 9.89e+10 | -10.63 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:53` | 13 | X | 4,800 | 1.07 | 5.16e+09 | -11.91 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:54` | 13 | X | 6,200 | 1.07 | 6.66e+09 | -11.80 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:55` | 13 | X | 3,600 | 1.07 | 3.87e+09 | -12.03 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:56` | 13 | X | 4,200 | 1.07 | 4.52e+09 | -11.97 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:57` | 13 | X | 5,400 | 1.07 | 5.8e+09 | -11.86 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Spellcraft/The Iron Tree.md:59` | 13 | X | 6,200 | 1.07 | 6.66e+09 | -11.80 | `C-040` |
| Obrenkael · The Mule | `wiki/Summoned and Bound/Obrenkael · The Mule.md:75` | 10 | SS | 8.1e+06 | 0.75 | 6.08e+12 | -0.84 | `DERIVED` |
| Vaelmorn · The Standing Grave | `wiki/Summoned and Bound/Vaelmorn · The Standing Grave.md:80` | 12 | SSS | 4e+07 | 0.88 | 3.5e+13 | -1.08 | `NO-TARGET` |
| Celestial Harmonic Shear | `wiki/Techniques/Celestial Harmonic Shear.md:44` | 12 | SSS | 45,000 | 0.88 | 3.94e+10 | -4.03 | `NOT-A-CARD-FIGURE` |
| Harmonic Null-Ascension | `wiki/Techniques/Harmonic Null-Ascension.md:44` | 12 | SSS | 45,000 | 0.88 | 3.94e+10 | -4.03 | `NOT-A-CARD-FIGURE` |
| Sovereign Parallax Lance | `wiki/Techniques/Sovereign Parallax Lance.md:44` | 12 | SSS | 45,000 | 0.88 | 3.94e+10 | -4.03 | `NOT-A-CARD-FIGURE` |
| The Aether Bastion | `wiki/Techniques/The Aether Bastion.md:44` | 6 | A | 5,000 | 0.65 | 3.25e+09 | -1.15 | `NOT-A-CARD-FIGURE` |
| Rusashin — The Dust That Remembers What It Touched | `wiki/The Disciplines/Rusashin — The Dust That Remembers What It Touched.md:83` | 7 *(own gate)* | A | 12,000 | 0.65 | 7.8e+09 | -0.77 | `NO-TARGET` |
| Rusashin — The Dust That Remembers What It Touched | `wiki/The Disciplines/Rusashin — The Dust That Remembers What It Touched.md:84` | 8 *(own gate)* | S | 40,000 | 0.75 | 3e+10 | -2.14 | `NO-TARGET` |
| Rusashin — The Dust That Remembers What It Touched | `wiki/The Disciplines/Rusashin — The Dust That Remembers What It Touched.md:85` | 9 *(own gate)* | S | 120,000 | 0.75 | 9e+10 | -1.67 | `NO-TARGET` |
| Kwon Mu-jin | `wiki/The Disciplines/The Open Crucible — Kwon Mu-jin's Book of Summons.md:30` | 12 | SSS | 1.28e+08 | 0.88 | 1.12e+14 | -0.57 | `DERIVED` |
| Anryū Ichimonji | `wiki/Volume I — Character Cards/Anryū Ichimonji.md:91` | 7 | A | 18,000 | 1.05 | 1.89e+10 | -0.39 | `NO-TARGET` |
| Anryū Ichimonji | `wiki/Volume I — Character Cards/Anryū Ichimonji.md:92` | 7 | A | 31,000 | 1.05 | 3.26e+10 | -0.15 | `NO-TARGET` |
| Ara Min Mahuo | `wiki/Volume I — Character Cards/Ara Min Mahuo.md:71` | 8 | S | 4.2e+06 | 0.70 | 2.94e+12 | -0.15 | `NO-TARGET` |
| Artemis Amagiri Moto | `wiki/Volume I — Character Cards/Artemis Amagiri Moto.md:56` | 8 | S | 41,800 | 0.84 | 3.51e+10 | -2.08 | `C-040` |
| Artemis Amagiri Moto | `wiki/Volume I — Character Cards/Artemis Amagiri Moto.md:87` | 8 | S | 2,400 | 0.84 | 2.02e+09 | -3.32 | `C-040` |
| Artemis Amagiri Moto | `wiki/Volume I — Character Cards/Artemis Amagiri Moto.md:88` | 8 | S | 1,800 | 0.84 | 1.51e+09 | -3.44 | `C-040` |
| Artemis Amagiri Moto | `wiki/Volume I — Character Cards/Artemis Amagiri Moto.md:89` | 8 | S | 950 | 0.84 | 7.98e+08 | -3.72 | `C-040` |
| Artemis Amagiri Moto | `wiki/Volume I — Character Cards/Artemis Amagiri Moto.md:90` | 8 | S | 3,100 | 0.84 | 2.6e+09 | -3.21 | `C-040` |
| Artemis Amagiri Moto | `wiki/Volume I — Character Cards/Artemis Amagiri Moto.md:91` | 8 | S | 700 | 0.84 | 5.88e+08 | -3.85 | `C-040` |
| Aurelian Prudentius Custos Clausorum · The Primate | `wiki/Volume I — Character Cards/Aurelian Prudentius Custos Clausorum · The Primate.md:85` | 14 | EX | 2.4e+09 | 1.06 | 2.54e+15 | -13.69 | `NO-TARGET` |
| Aurelian Veymont · The Lion of the Dawn | `wiki/Volume I — Character Cards/Aurelian Veymont · The Lion of the Dawn.md:101` | 7 | A | 18,000 | 0.87 | 1.57e+10 | -0.47 | `NO-TARGET` |
| Ayame Yuno | `wiki/Volume I — Character Cards/Ayame Yuno.md:58` | 8 | S | 37,000 | 0.86 | 3.18e+10 | -2.12 | `C-040` |
| Ayame Yuno | `wiki/Volume I — Character Cards/Ayame Yuno.md:88` | 8 | S | 4,800 | 0.86 | 4.13e+09 | -3.01 | `C-040` |
| Borin Ironheart · The Master of the Soul Forge | `wiki/Volume I — Character Cards/Borin Ironheart · The Master of the Soul Forge.md:102` | 12 | SSS | 1.8e+08 | 0.91 | 1.64e+14 | -0.41 | `C-040` |
| Brynja Haldrís · Hammer of the Northroot | `wiki/Volume I — Character Cards/Brynja Haldrís · Hammer of the Northroot.md:100` | 6 | A | 11,000 | 0.82 | 9.02e+09 | -0.71 | `NO-TARGET` |
| Cyranthia Valez · The Gilded Marionette | `wiki/Volume I — Character Cards/Cyranthia Valez · The Gilded Marionette.md:101` | 6 | A | 13,200 | 0.95 | 1.25e+10 | -0.56 | `NO-TARGET` |
| Dougou Ozumu Zettari | `wiki/Volume I — Character Cards/Dougou Ozumu Zettari.md:93` | 13 | X | 4,800 | 0.99 | 4.75e+09 | -11.94 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Volume I — Character Cards/Dougou Ozumu Zettari.md:94` | 13 | X | 6,200 | 0.99 | 6.14e+09 | -11.83 | `C-040` |
| Dougou Ozumu Zettari | `wiki/Volume I — Character Cards/Dougou Ozumu Zettari.md:97` | 13 | X | 14,000 | 0.99 | 1.39e+10 | -11.48 | `C-040` |
| Helki · The Shepherd of Unwilling Paths | `wiki/Volume I — Character Cards/Helki · The Shepherd of Unwilling Paths.md:97` | 7 | A | 40,000 | 0.65 | 2.6e+10 | -0.25 | `NO-TARGET` |
| Ignatius Sanctus Sanctorum Arsenal · The Archpaladin | `wiki/Volume I — Character Cards/Ignatius Sanctus Sanctorum Arsenal · The Archpaladin.md:141` | 12 | SSS | 5.5e+06 | 0.90 | 4.95e+12 | -1.93 | `NO-TARGET` |
| Iracordas | `wiki/Volume I — Character Cards/Iracordas.md:48` | 10 | SS | 16,800 | 0.93 | 1.56e+10 | -3.43 | `C-040` |
| Iracordas | `wiki/Volume I — Character Cards/Iracordas.md:67` | 10 | SS | 1,800 | 0.93 | 1.67e+09 | -4.40 | `C-040` |
| Iracordas | `wiki/Volume I — Character Cards/Iracordas.md:68` | 10 | SS | 3,900 | 0.93 | 3.63e+09 | -4.06 | `C-040` |
| Karo Venrik · The Foolish Magus | `wiki/Volume I — Character Cards/Karo Venrik · The Foolish Magus.md:137` | 5 | B | 1,600 | 0.50 | 8e+08 | -0.12 | `C-040` |
| Krothar Veylshroud — The Chain Without a Master | `wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md:99` | 8 | S | 1.6e+06 | 0.81 | 1.3e+12 | -0.51 | `C-040` |
| Krothar Veylshroud | `wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md:99` | 8 | S | 2.8e+06 | 0.81 | 2.27e+12 | -0.27 | `C-040` |
| Lucius Xenotro | `wiki/Volume I — Character Cards/Lucius Xenotro.md:60` | 8 | S | 2.85e+06 | 0.92 | 2.62e+12 | -0.20 | `NO-TARGET` |
| Lucius Xenotro | `wiki/Volume I — Character Cards/Lucius Xenotro.md:87` | 8 | S | 28,000 | 0.92 | 2.58e+10 | -2.21 | `NO-TARGET` |
| Lucius Xenotro | `wiki/Volume I — Character Cards/Lucius Xenotro.md:88` | 8 | S | 36,000 | 0.92 | 3.31e+10 | -2.10 | `NO-TARGET` |
| Lucius Xenotro | `wiki/Volume I — Character Cards/Lucius Xenotro.md:89` | 8 | S | 18,000 | 0.92 | 1.66e+10 | -2.40 | `NO-TARGET` |
| Lucius Xenotro | `wiki/Volume I — Character Cards/Lucius Xenotro.md:90` | 8 | S | 75,000 | 0.92 | 6.9e+10 | -1.78 | `NO-TARGET` |
| Lucius Xenotro | `wiki/Volume I — Character Cards/Lucius Xenotro.md:91` | 8 | S | 160,000 | 0.92 | 1.47e+11 | -1.45 | `NO-TARGET` |
| Marceline Vireaux · The Crimson Mourner | `wiki/Volume I — Character Cards/Marceline Vireaux · The Crimson Mourner.md:100` | 6 | A | 11,800 | 0.93 | 1.1e+10 | -0.62 | `NO-TARGET` |
| Mizuki Moto | `wiki/Volume I — Character Cards/Mizuki Moto.md:83` | 7 | A | 12,000 | 0.82 | 9.84e+09 | -0.67 | `NO-TARGET` |
| Mizuki Moto | `wiki/Volume I — Character Cards/Mizuki Moto.md:84` | 7 | A | 14,000 | 0.82 | 1.15e+10 | -0.60 | `NO-TARGET` |
| Mizuki Moto | `wiki/Volume I — Character Cards/Mizuki Moto.md:85` | 7 | A | 9,500 | 0.82 | 7.79e+09 | -0.77 | `NO-TARGET` |
| Mizuki Moto | `wiki/Volume I — Character Cards/Mizuki Moto.md:86` | 7 | A | 16,000 | 0.82 | 1.31e+10 | -0.55 | `NO-TARGET` |
| Mizuki Moto | `wiki/Volume I — Character Cards/Mizuki Moto.md:87` | 7 | A | 19,000 | 0.82 | 1.56e+10 | -0.47 | `NO-TARGET` |
| Mizuki Moto | `wiki/Volume I — Character Cards/Mizuki Moto.md:88` | 7 | A | 30,000 | 0.82 | 2.46e+10 | -0.27 | `NO-TARGET` |
| Muken Moto | `wiki/Volume I — Character Cards/Muken Moto.md:60` | 10 | SS | 1.85e+06 | 0.84 | 1.55e+12 | -1.43 | `NO-TARGET` |
| Muken Moto | `wiki/Volume I — Character Cards/Muken Moto.md:101` | 10 | SS | 75,000 | 0.84 | 6.3e+10 | -2.82 | `NO-TARGET` |
| Muken Moto | `wiki/Volume I — Character Cards/Muken Moto.md:108` | 10 | SS | 22,000 | 0.84 | 1.85e+10 | -3.35 | `NO-TARGET` |
| Muken Moto | `wiki/Volume I — Character Cards/Muken Moto.md:108` | 10 | SS | 44,000 | 0.84 | 3.7e+10 | -3.05 | `NO-TARGET` |
| Muken Moto | `wiki/Volume I — Character Cards/Muken Moto.md:115` | 10 | SS | 58,000 | 0.84 | 4.87e+10 | -2.93 | `NO-TARGET` |
| Naevra Yukari | `wiki/Volume I — Character Cards/Naevra Yukari.md:48` | 9 | S | 185,000 | 0.96 | 1.78e+11 | -1.37 | `C-040` |
| Naevra Yukari | `wiki/Volume I — Character Cards/Naevra Yukari.md:76` | 9 | S | 5,400 | 0.96 | 5.18e+09 | -2.91 | `C-040` |
| Naevra Yukari | `wiki/Volume I — Character Cards/Naevra Yukari.md:80` | 9 | S | 8,900 | 0.96 | 8.54e+09 | -2.69 | `C-040` |
| Naevra Yukari | `wiki/Volume I — Character Cards/Naevra Yukari.md:84` | 9 | S | 14,200 | 0.96 | 1.36e+10 | -2.49 | `C-040` |
| Naevra Yukari | `wiki/Volume I — Character Cards/Naevra Yukari.md:88` | 9 | S | 7,300 | 0.96 | 7.01e+09 | -2.78 | `C-040` |
| Naiser Yukari | `wiki/Volume I — Character Cards/Naiser Yukari.md:57` | 6 | A | 2,460 | 0.65 | 1.6e+09 | -1.46 | `NO-TARGET` |
| Naiser Yukari | `wiki/Volume I — Character Cards/Naiser Yukari.md:89` | 6 | A | 320 | 0.65 | 2.08e+08 | -2.34 | `NO-TARGET` |
| Naiser Yukari | `wiki/Volume I — Character Cards/Naiser Yukari.md:95` | 6 | A | 540 | 0.65 | 3.51e+08 | -2.12 | `NO-TARGET` |
| Naiser Yukari | `wiki/Volume I — Character Cards/Naiser Yukari.md:101` | 6 | A | 710 | 0.65 | 4.61e+08 | -2.00 | `NO-TARGET` |
| Naori Yukari | `wiki/Volume I — Character Cards/Naori Yukari.md:54` | 3 | C | 42,000 | 0.40 | 1.68e+10 | +1.21 | `NO-TARGET` |
| Niran Yukari | `wiki/Volume I — Character Cards/Niran Yukari.md:91` | 7 | A | 12,000 | 0.89 | 1.07e+10 | -0.63 | `NO-TARGET` |
| Niran Yukari | `wiki/Volume I — Character Cards/Niran Yukari.md:92` | 7 | A | 14,000 | 0.89 | 1.25e+10 | -0.57 | `NO-TARGET` |
| Niran Yukari | `wiki/Volume I — Character Cards/Niran Yukari.md:94` | 7 | A | 18,000 | 0.89 | 1.6e+10 | -0.46 | `NO-TARGET` |
| Niran Yukari | `wiki/Volume I — Character Cards/Niran Yukari.md:95` | 7 | A | 15,000 | 0.89 | 1.34e+10 | -0.54 | `NO-TARGET` |
| Niran Yukari | `wiki/Volume I — Character Cards/Niran Yukari.md:96` | 7 | A | 22,000 | 0.89 | 1.96e+10 | -0.37 | `NO-TARGET` |
| Niran Yukari | `wiki/Volume I — Character Cards/Niran Yukari.md:97` | 7 | A | 35,000 | 0.89 | 3.12e+10 | -0.17 | `NO-TARGET` |
| Rashani Zettari | `wiki/Volume I — Character Cards/Rashani Zettari.md:90` | 6 | A | 8,000 | 0.81 | 6.48e+09 | -0.85 | `NO-TARGET` |
| Rashani Zettari | `wiki/Volume I — Character Cards/Rashani Zettari.md:91` | 6 | A | 13,000 | 0.81 | 1.05e+10 | -0.64 | `NO-TARGET` |
| Rashani Zettari | `wiki/Volume I — Character Cards/Rashani Zettari.md:92` | 6 | A | 15,000 | 0.81 | 1.22e+10 | -0.58 | `NO-TARGET` |
| Rashani Zettari | `wiki/Volume I — Character Cards/Rashani Zettari.md:93` | 6 | A | 18,000 | 0.81 | 1.46e+10 | -0.50 | `NO-TARGET` |
| Rashani Zettari | `wiki/Volume I — Character Cards/Rashani Zettari.md:94` | 6 | A | 22,000 | 0.81 | 1.78e+10 | -0.41 | `NO-TARGET` |
| Rashani Zettari | `wiki/Volume I — Character Cards/Rashani Zettari.md:95` | 6 | A | 9,500 | 0.81 | 7.7e+09 | -0.78 | `NO-TARGET` |
| Rengai Zettari | `wiki/Volume I — Character Cards/Rengai Zettari.md:84` | 7 | A | 32,000 | 0.78 | 2.5e+10 | -0.27 | `NO-TARGET` |
| Rengai Zettari | `wiki/Volume I — Character Cards/Rengai Zettari.md:85` | 7 | A | 22,000 | 0.78 | 1.72e+10 | -0.43 | `NO-TARGET` |
| Rengai Zettari | `wiki/Volume I — Character Cards/Rengai Zettari.md:86` | 7 | A | 20,000 | 0.78 | 1.56e+10 | -0.47 | `NO-TARGET` |
| Rengai Zettari | `wiki/Volume I — Character Cards/Rengai Zettari.md:87` | 7 | A | 28,000 | 0.78 | 2.18e+10 | -0.32 | `NO-TARGET` |
| Rengai Zettari | `wiki/Volume I — Character Cards/Rengai Zettari.md:88` | 7 | A | 58,000 | 0.78 | 4.52e+10 | -0.01 | `NO-TARGET` |
| Sodoku Moto | `wiki/Volume I — Character Cards/Sodoku Moto.md:109` | 6 | A | 6,000 | 0.84 | 5.04e+09 | -0.96 | `NO-TARGET` |
| Sodoku Moto | `wiki/Volume I — Character Cards/Sodoku Moto.md:110` | 6 | A | 9,500 | 0.84 | 7.98e+09 | -0.76 | `NO-TARGET` |
| Sodoku Moto | `wiki/Volume I — Character Cards/Sodoku Moto.md:111` | 6 | A | 16,000 | 0.84 | 1.34e+10 | -0.53 | `NO-TARGET` |
| Souma Byakuya Moto | `wiki/Volume I — Character Cards/Souma Byakuya Moto.md:88` | 5 | B | 1,200 | 0.65 | 7.8e+08 | -0.13 | `C-040` |
| Souma Byakuya Moto | `wiki/Volume I — Character Cards/Souma Byakuya Moto.md:89` | 5 | B | 460 | 0.65 | 2.99e+08 | -0.54 | `C-040` |
| Vael of Nothing · The Devourer's Index | `wiki/Volume I — Character Cards/Vael of Nothing · The Devourer's Index.md:97` | 9 | S | 2.6e+06 | 0.75 | 1.95e+12 | -0.33 | `NO-TARGET` |
| Vaelthor Ashen-Meridian · The Patient Throne | `wiki/Volume I — Character Cards/Vaelthor Ashen-Meridian · The Patient Throne.md:99` | 10 | SS | 620,000 | 0.97 | 6.01e+11 | -1.84 | `NO-TARGET` |
| Vethraun Ashmaw | `wiki/Volume I — Character Cards/Vethraun Ashmaw.md:64` | 10 | SS | 9,400 | 0.91 | 8.55e+09 | -3.69 | `C-040` |
| Vethraun Ashmaw | `wiki/Volume I — Character Cards/Vethraun Ashmaw.md:93` | 10 | SS | 420 | 0.91 | 3.82e+08 | -5.04 | `C-040` |
| Vethraun Ashmaw | `wiki/Volume I — Character Cards/Vethraun Ashmaw.md:105` | 10 | SS | 800 | 0.91 | 7.28e+08 | -4.76 | `C-040` |
| Vethraun Ashmaw | `wiki/Volume I — Character Cards/Vethraun Ashmaw.md:118` | 10 | SS | 800 | 0.91 | 7.28e+08 | -4.76 | `C-040` |
| Yoko Mishiro | `wiki/Volume I — Character Cards/Yoko Mishiro.md:69` | 5 | B | 185,000 | 0.50 | 9.25e+10 | +0.30 | `NO-TARGET` |
| Yorime Seikai | `wiki/Volume I — Character Cards/Yorime Seikai.md:59` | 12 | SSS | 74,000 | 0.94 | 6.96e+10 | -3.78 | `C-040` |
| Yorime Seikai | `wiki/Volume I — Character Cards/Yorime Seikai.md:92` | 12 | SSS | 2,800 | 0.94 | 2.63e+09 | -5.20 | `C-040` |
| Yorime Seikai | `wiki/Volume I — Character Cards/Yorime Seikai.md:93` | 12 | SSS | 3,600 | 0.94 | 3.38e+09 | -5.09 | `C-040` |
| Yorime Seikai | `wiki/Volume I — Character Cards/Yorime Seikai.md:95` | 12 | SSS | 9,500 | 0.94 | 8.93e+09 | -4.67 | `C-040` |
| Yorime Seikai | `wiki/Volume I — Character Cards/Yorime Seikai.md:96` | 12 | SSS | 6,000 | 0.94 | 5.64e+09 | -4.87 | `C-040` |
| Yorime Seikai | `wiki/Volume I — Character Cards/Yorime Seikai.md:97` | 12 | SSS | 12,000 | 0.94 | 1.13e+10 | -4.57 | `C-040` |
| Yukazuri Moto | `wiki/Volume I — Character Cards/Yukazuri Moto.md:83` | 4 | B | 140 | 0.89 | 1.25e+08 | -0.92 | `C-040` |
| Yukazuri Moto | `wiki/Volume I — Character Cards/Yukazuri Moto.md:84` | 4 | B | 260 | 0.89 | 2.31e+08 | -0.66 | `C-040` |
| Yukazuri Moto | `wiki/Volume I — Character Cards/Yukazuri Moto.md:85` | 4 | B | 390 | 0.89 | 3.47e+08 | -0.48 | `C-040` |

### The 4 figures with no Grade available, read against nothing

| entity | file:line | EU | why |
|---|---|---|---|
| Chimwala N'Doro | `wiki/Artifacts/Kibanda cha Mwanga wa Miti · Lantern of the Grove's Light.md:35` | 60 | no Grade available for this reading |
| The Black Aperture · Void Key | `wiki/Artifacts/The Black Aperture · Void Key.md:36` | 120 | no Grade available for this reading |
| Recarvu — The Body That Builds Over What It Cannot Fix | `wiki/The Disciplines/Recarvu — The Body That Builds Over What It Cannot Fix.md:68` | 8,000 | no Grade available for this reading |
| Recarvu — The Body That Builds Over What It Cannot Fix | `wiki/The Disciplines/Recarvu — The Body That Builds Over What It Cannot Fix.md:70` | 6,000 | no Grade available for this reading |

## Two things found on the way, neither of them a card correction

**One. The sweep's worst residual is a figure the card says is final.** `Volume I — Character Cards/Aurelian Prudentius Custos Clausorum · The Primate.md:85` reads 2,400,000,000 EU at Stage XIV, 13.69 decades below the EX band, the largest miss in the corpus. The line states its own provenance: "Fracture of Worlds specifies no EU table by Stage; this figure was extrapolated from the two attested Band V reserves in project canon, Verinus VII at 620,000,000 and Kwon Mu-jin at 850,000,000, both at Stage XII, and stands as final." It is logged `NO-TARGET`, not `NOT-A-CARD-FIGURE`: the card says the figure stands. What it also says is that the two reserves it was built from are Stage XII figures and his Stage is XIV, and `fit.json` reads Stage XIV's Max Grade as EX off Part Five while Part Eleven's benchmark table declines to give Zenith a figure at all (`fit.json`, `meta.stage_xiv_reading`). Three readings meet on this one line and R44-1 names none of them.

**Two. Once each figure is read against its own Stage, almost every miss reads below its band.** 2 of the 128 misses read above their band and the other 126 below, and the ones above are 2 reserves — Naori Yukari at +1.21, `wiki/Volume I — Character Cards/Naori Yukari.md:54`, Yoko Mishiro at +0.30, `wiki/Volume I — Character Cards/Yoko Mishiro.md:69`. Read that way a stored pool can sit above what its Stage may throw while every attested spend for a working comes in under it, which is a shape and not a correction. Nothing here says which side of the proxy is wrong, and the misses that remain above their band are logged like the rest.

## What would let this sweep run

One further ruling on top of R44-1: what a corrected figure becomes. Under the 2026-09-25 direction in `CLAUDE.md` — "a recorded conflict does not sit waiting for Isaac: it is ruled, openly, by the Paperclip docket" — that is the docket's to make and not the Stat Keeper's, so it is filed to Doc Kett rather than answered here. Three shapes would each be enough, and this file proposes none of them as the answer:

- a rule that puts the figure at a named edge of its band (the floor, the midpoint), which makes every correction arithmetic off Part Four;
- a rule that the figure is correct and the Stage on the card is what moves, which is C-040's other direction and belongs with C-040;
- a rule that an EU reserve is not read against an attack-output band at all, which would take 20 of the 128 out of scope and leave the costs.

Until one of them exists, R44-1 is applied as far as it reaches: the constant is settled, the misses are counted, and every card stands exactly as written.
