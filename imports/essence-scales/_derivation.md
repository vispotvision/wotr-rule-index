# The essence scales — EU by Stage, the AU/s ladder, AU to joules, the turn

WAR-161. Every figure in this file is computed by `scales.py` from four quoted
anchors and three ruled constants. Nothing is typed and nothing is invented: the
two ladders below are Part Four and Part Five as they stand, read at the constant
R44-1 fixes, with the set point C-059 already uses. `derive.py` writes this file.

## The three constants

| constant | value | where it is ruled |
|---|---|---|
| 1 EU | 1 MJ | `RULINGS.md`, 2026-09-25, **R44-1-EU_JOULE_ONE_MEGAJOULE** |
| 1 AU | 1 EU, so 1 AU/s = 1 MW | `RULINGS.md`, 2026-09-26, WAR-3 card 1 q3 — "an AU-to-joule rate" |
| one turn | 6 seconds | `RULINGS.md`, 2026-09-26, WAR-3 card 1 q7 — "one turn = 6 seconds" |

The second and third are Isaac's answers to the WAR-3 questionnaire, recorded in
full on that issue's comments of 2026-09-26 and in `RULINGS.md` under
*2026-09-26 — WAR-3 cards 1 and 2 (system accounts, 20 answers)*.

## Anchor one — Part Four, Grade to attack output

`wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`, Part Four. The joule column is the whole basis of the EU ladder, so it
is reproduced here exactly as the page writes it:

| Grade | Sub-Stat value | Attack output |
|---|---|---|
| Hollow | 1–10 | below 60 J |
| F | 11–25 | 60–300 J |
| E | 26–50 | 300 J – 15 kJ |
| D | 51–100 | 15 kJ – 2.092×10^7 J |
| C | 101–175 | 2.092×10^7 – 1.046×10^9 J |
| B | 176–275 | 1.046×10^9 – 4.6024×10^10 J |
| A | 276–400 | 4.6024×10^10 – 4.184×10^12 J |
| S | 401–550 | 4.184×10^12 – 2.42672×10^13 J |
| SS | 551–725 | 4.184×10^13 – 4.184×10^14 J |
| SSS | 726–950 | 4.184×10^14 – 4.184×10^21 J |
| X | 951–1,200 | 4.184×10^21 – 1.24×10^29 J |
| EX | 1,201–1,500 | 1.24×10^29 – 6.906×10^37 J |
| EX+ | 1,501+ | 6.906×10^37 J and above |

## Anchor two — Part Five, Stage to Max Grade and Tier of Standing

The same file, Part Five. Two columns matter: **Max Grade**, which "binds
allocation: a Sub-Stat may not be allocated past the top of the Stage's Max Grade
bracket", and **Sub-Stat ceiling**, which at Stages V, VII, IX and XI sits *above*
that bracket — "the instability zone, reachable only under strain, never by
allocation".

## Anchor three — Part Nineteen, efficiency by Tier of Standing

`wiki/Fracture of Worlds — The Living System/VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md`, Part Nineteen. The η column as it stands after **R44-4**, which
corrects the Tier 5 cell to 0.60–0.70 (applied to the live page under WAR-133;
the mirror lagged when this was written). Tier 9 is "above 1.2, unbounded".

## Anchor four — the Stages whose force is not measured

Part Four, the same file: "At **Zenith, Stage XIV**, speed and attack output are
no longer assessed by conventional metrics." Isaac's WAR-142 answer carries that
upward — "Stage XV keeps its EX+ Grade label, but its force is unmeasured like
Zenith's; the Zenith row sits beside the Grade ladder, not on it" — and Apex
states no Max Grade at all. **Stages XIV, XV and XVI therefore take no derived EU
or AU/s figure.** Every cell for them below reads *unmeasured*, not null: the
absence is ruled, not missing.

## The EU-by-Stage benchmark — the arithmetic, once

For a Stage, Part Five gives the Max Grade *G*; Part Four gives *G*'s
attack-output floor and ceiling in joules. At 1 EU = 1 MJ the band in EU is those
two bounds divided by 10⁶. The benchmark inside the band is **C-059's set point**,
the same one WAR-46 already applies to twelve cards: √(floor × ceiling) ÷ 1 MJ, at
four significant figures — the precision Part Four's own bounds carry.

> Each card whose reserve R44-1 puts outside its Stage's band is scaled by one
> factor: factor = (the band midpoint in decades, the geometric mean of floor and
> ceiling joules / 1 MJ) / (the card's stated reserve).

So this table is not a new scale. It is the band and the set point C-059 names,
written out once per Stage instead of being recomputed per card. Two checks prove
it is the same arithmetic:

- Stage XII's benchmark is **1.323×10^12 EU**, which is exactly
  the set point `reports/eu_card_scaling_2026-09-25.md` computed for the Arctic
  Lion sheet.
- Stage XIII's is **2.278×10^19 EU**, exactly the set point the
  same report computed for Dougou Ozumu Zettari.

Worked once in full, at Stage VIII: Part Five gives Max Grade **S**; Part Four
gives S as 4.184×10^12–2.427×10^13 J; at 1 MJ that is
4.184×10^6–2.427×10^7 EU; the set point is
√(4.184×10^12 × 2.427×10^13) =
1.008×10^13 J ÷ 1 MJ =
**1.008×10^7 EU**.

**The plateaux are real and are not an error.** Stages IV and V share Max Grade B,
VI and VII share A, VIII and IX share S, X and XI share SS, so each pair shares a
band. The second Stage of each pair is the instability Stage, and what rises there
is the Sub-Stat ceiling, not the allocation bracket. Part Four's Sub-Stat column
says which Grade that raised ceiling reaches, and the *Under strain* column below
is that Grade's band: Stage V's ceiling of 350 sits in the
A bracket, so a Stage V practitioner under strain reaches
46,020–4.184×10^6 EU and no further.

**Below Stage III a benchmark reserve is a fraction of one EU.** At 1 EU = 1 MJ
this follows: a Murmuring practitioner's whole attack output is
300–15,000 J, which is
3.000×10^-4–1.500×10^-2 EU. The figures are written as
computed. Whether the unit should carry a floor at the bottom of the ladder is a
question for Isaac, not a number to invent, and it is on the rolling
questionnaire.

## The AU-to-joule equivalence

One AU is one EU, so one AU is 1 MJ and **1 AU/s = 1 MW**. *The Core Vocabulary*
already states which side of η the rate sits on, and this file follows it rather
than offering a second reading: **AU/s is the draw**, power drawn is AU/s × 1 MW,
power delivered is AU/s × η × 1 MW, "and the difference leaves as waste heat. Time
to empty is reserve ÷ AU/s, and that figure does not depend on the conversion at
all." Three identities follow and are used throughout:

- **drawn** by a working of *R* AU/s held for *t* seconds = *R* × *t* EU.
- **delivered** over the same *t* = *R* × *t* × η MJ.
- **time to empty** a reserve of *E* EU at *R* AU/s = *E* ÷ *R* seconds.

## The AU/s progression — the arithmetic, once

The EU ladder is a ladder of reserves, read off the same Part Four column C-059
reads, and a reserve becomes a rate the moment a turn has a length. A Stage's AU/s
band is its EU band spread over one turn: floor and ceiling
÷ 6 s. The benchmark AU/s is the benchmark reserve
÷ 6.

That fixes one plain reading of the whole ladder: **the benchmark reserve is
exactly one turn of draw at the benchmark rate.** Time to empty is E ÷ R, and by
construction E ÷ R = 6 s at every Stage. A practitioner
who opens at their Stage's benchmark rate has six seconds of it and nothing after,
which is why sustained work runs far below the benchmark and why the Starvation
floor at ten percent is reachable inside a single exchange.

**The check that the ladder is the same arithmetic as C-059.** The last column of
the AU/s table is what the benchmark reserve delivers in that turn — reserve × η ×
1 MJ, at the tier's η midpoint — and at every Stage it lands back inside the Part
Four band the reserve was read from. At Stage XIII that figure is
2.449×10^25 J, which is the same
number `reports/eu_card_scaling_2026-09-25.md` prints as its check line for Dougou
Ozumu Zettari. The ladder closes on itself.

**Against the attested cards.** The ladder is checkable and it is not a fit: it
was derived from the tables alone and then read against the cards. Niran Yukari's
16,376 AU/s at Stage VII sits inside
7,671–697,300, and Gimbzo's 6.7×10^14 at
Stage XII sits inside 6.973×10^7–6.973×10^14.
Others sit outside; `reports/essence_scales_2026-09-26.md` reads every one of them
and says which and by how much. **No card figure is moved by this file.** Isaac's
answer to WAR-3 card 1 q2 asks that cards missing the ladder be corrected, and
R44-5's operative sentence — "the card's η governs per character and the tables are
typical ranges" — says an outlier card is lawful. The two do not agree about which
gives way, and until that is answered the published ladder is typical ranges and no
card is overwritten. The question is on the rolling questionnaire.

## η above 1.0

Part Nineteen's Tier 8 row already says what happens there: "Above 1.0 the
Continuum recognizes the expression as law and supplements it with ambient flow;
the environment becomes a co-author." `The Physical Account — Two Sets of Books`
says where the energy is: "a working's energy budget balances at the Aether stratum
and not at the Essence one. The practitioner does not supply the joules. They
supply the boundary condition." Isaac's answer to card 1 q9 makes the reading
explicit and puts it in the Core Vocabulary: η above 1.0 is real, and the surplus
is drawn from the Aether stratum. It is not the Crystal returning more than it
spent; it is the stratum paying the difference, which is why the figure is a ratio
of delivered effect to Essence spent and not a violation of anything.

## The tables

### The EU-by-Stage benchmark

| Stage | Name | Max Grade | EU band | Benchmark reserve (EU) | Under strain |
|---|---|---|---|---|---|
| I | Murmuring | E | 3.000×10^-4–1.500×10^-2 | 2.121×10^-3 | — |
| II | Welling | D | 1.500×10^-2–20.92 | 0.5602 | — |
| III | Ascension | C | 20.92–1,046 | 147.9 | — |
| IV | Flourishing | B | 1,046–46,020 | 6,938 | — |
| V | Splintering | B | 1,046–46,020 | 6,938 | A-Grade reach, 46,020–4.184×10^6 EU |
| VI | Glory | A | 46,020–4.184×10^6 | 438,800 | — |
| VII | Refraction | A | 46,020–4.184×10^6 | 438,800 | S-Grade reach, 4.184×10^6–2.427×10^7 EU |
| VIII | Transcendence | S | 4.184×10^6–2.427×10^7 | 1.008×10^7 | — |
| IX | Invocation | S | 4.184×10^6–2.427×10^7 | 1.008×10^7 | SS-Grade reach, 4.184×10^7–4.184×10^8 EU |
| X | Realization | SS | 4.184×10^7–4.184×10^8 | 1.323×10^8 | — |
| XI | Dissonance | SS | 4.184×10^7–4.184×10^8 | 1.323×10^8 | SSS-Grade reach, 4.184×10^8–4.184×10^15 EU |
| XII | Emanation | SSS | 4.184×10^8–4.184×10^15 | 1.323×10^12 | — |
| XIII | Principality | X | 4.184×10^15–1.240×10^23 | 2.278×10^19 | — |
| XIV | Zenith | EX | unmeasured | unmeasured | not assessed by conventional metrics |
| XV | Revelation | EX+ | unmeasured | unmeasured | not assessed by conventional metrics |
| XVI | Apex | uncapped | unmeasured | unmeasured | not assessed by conventional metrics |

### The AU/s progression by Stage

| Stage | Tier of Standing | η | AU/s band | Benchmark AU/s | Delivered in one turn |
|---|---|---|---|---|---|
| I | 1 · Initiate | 0.30 | 5.000×10^-5–2.500×10^-3 | 3.536×10^-4 | 636.4 J |
| II | 2 · Apprentice | 0.35 | 2.500×10^-3–3.487 | 9.336×10^-2 | 196,100 J |
| III | 3 · Journeyman | 0.40 | 3.487–174.3 | 24.65 | 5.917×10^7 J |
| IV | 4 · Adept | 0.45 | 174.3–7,671 | 1,156 | 3.122×10^9 J |
| V | 5 · Expert | 0.60–0.70 | 174.3–7,671 | 1,156 | 4.510×10^9 J |
| VI | 5 · Expert | 0.60–0.70 | 7,671–697,300 | 73,140 | 2.852×10^11 J |
| VII | 5 · Expert | 0.60–0.70 | 7,671–697,300 | 73,140 | 2.852×10^11 J |
| VIII | 6 · Master | 0.70–0.80 | 697,300–4.045×10^6 | 1.679×10^6 | 7.557×10^12 J |
| IX | 6 · Master | 0.70–0.80 | 697,300–4.045×10^6 | 1.679×10^6 | 7.557×10^12 J |
| X | 6 · Master | 0.70–0.80 | 6.973×10^6–6.973×10^7 | 2.205×10^7 | 9.923×10^13 J |
| XI | 7 · Grandmaster | 0.85–0.90 | 6.973×10^6–6.973×10^7 | 2.205×10^7 | 1.158×10^14 J |
| XII | 7 · Grandmaster | 0.85–0.90 | 6.973×10^7–6.973×10^14 | 2.205×10^11 | 1.158×10^18 J |
| XIII | 8 · Archmaster | 0.95–1.20 | 6.973×10^14–2.067×10^22 | 3.796×10^18 | 2.449×10^25 J |
| XIV | 8 · Archmaster | 0.95–1.20 | unmeasured | unmeasured | unmeasured |
| XV | 9 · Paragon | above 1.2 | unmeasured | unmeasured | unmeasured |
| XVI | 9 · Paragon | above 1.2 | unmeasured | unmeasured | unmeasured |

### The same ladder by Tier of Standing

| Tier | Temperance | η | EU band | AU/s band | Benchmark AU/s |
|---|---|---|---|---|---|
| 1 · Initiate | I–I | ~0.30 | 3.000×10^-4–1.500×10^-2 | 5.000×10^-5–2.500×10^-3 | 3.536×10^-4 |
| 2 · Apprentice | II–II | ~0.35 | 1.500×10^-2–20.92 | 2.500×10^-3–3.487 | 9.336×10^-2 |
| 3 · Journeyman | III–III | ~0.40 | 20.92–1,046 | 3.487–174.3 | 24.65 |
| 4 · Adept | IV–IV | ~0.45 | 1,046–46,020 | 174.3–7,671 | 1,156 |
| 5 · Expert | V–VII | 0.60–0.70 | 1,046–4.184×10^6 | 174.3–697,300 | 11,030 |
| 6 · Master | VIII–X | 0.70–0.80 | 4.184×10^6–4.184×10^8 | 697,300–6.973×10^7 | 6.973×10^6 |
| 7 · Grandmaster | XI–XII | 0.85–0.90 | 4.184×10^7–4.184×10^15 | 6.973×10^6–6.973×10^14 | 6.973×10^10 |
| 8 · Archmaster | XIII–XIV | 0.95–1.20 | 4.184×10^15–1.240×10^23 | 6.973×10^14–2.067×10^22 | 3.796×10^18 (XIV unmeasured) |
| 9 · Paragon | XV–XVI | above 1.2 | unmeasured | unmeasured | unmeasured (XV, XVI unmeasured) |

### The turn

| turns | seconds | delivered by a working of R AU/s | drawn from the reserve at η |
|---|---|---|---|
| 1 | 6 | 6R MJ | 6R ÷ η EU |
| 2 | 12 | 12R MJ | 12R ÷ η EU |
| 3 | 18 | 18R MJ | 18R ÷ η EU |
| 4 | 24 | 24R MJ | 24R ÷ η EU |
| 5 | 30 | 30R MJ | 30R ÷ η EU |
| 6 | 36 | 36R MJ | 36R ÷ η EU |
| 10 | 60 | 60R MJ | 60R ÷ η EU |
| 20 | 120 | 120R MJ | 120R ÷ η EU |
| 100 | 600 | 600R MJ | 600R ÷ η EU |

## Reading a duration in turns

A duration stated in turns is that many times six seconds. Nine technique pages
carried a conversion at **five** seconds a turn and are corrected;
`reports/essence_scales_2026-09-26.md` lists each, with the figure before and
after. A "turn" that is not a combat turn — a lunar turn, a turn of a glass, a
siege turn on a campaign clock, a coil that runs one turn longer — is not a
duration and is left alone; each of those is listed too.
