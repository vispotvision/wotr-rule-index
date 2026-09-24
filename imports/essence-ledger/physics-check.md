# physics-check.md — the Essence Ledger conversion against real physics

WAR-10, Phase 2 of the Essence Ledger (parent WAR-8). This is a research note, not
canon and not a ruling. It changes no figure, adopts no constant and resolves no
conflict. It answers one question: **does 1 EU = 1 MJ, 1 AU/s = 1 MW survive
contact with real physics, and where does it break?**

Written against `anchors.json` and `fit.json` (WAR-9, Phase 1) and the wiki mirror
as it stood on 2026-09-24. Every canon figure is quoted verbatim with file and
line. Every physical figure carries its working and the law it comes from.

---

## The verdict, first

**No. 1 EU = 1 MJ is too large by three to four orders of magnitude at the low end
and too small by fourteen at the high end, and the failure is not a rounding
problem — it is structural.** Three findings carry it:

1. **The low end fails on thermodynamics, independently of anything canon says.**
   At 1 EU = 1 MJ, the cheapest working on the cheapest attested sheet — Yukazuri
   Moto's Nerve Reading, 140 EU — costs 140 MJ, and her own stated η of 0.89 dumps
   15.4 MJ of waste heat into a 70 kg body whose entire thermal budget to a lethal
   core temperature is 1.2 MJ. She dies twelve times over reading someone's muscle
   tension. The same working at the constant canon actually states on the page
   (112–3,571 J/EU, `fit.json` `direct_pairs`) costs 16 kJ to 500 kJ and raises her
   core temperature by 0.007 K to 0.22 K. **Physics arrives at canon's measured
   number by a route that never looks at canon**, which is the strongest evidence
   in this note.

2. **The high end fails on arithmetic before it reaches physics.** The Primate's
   2,400,000,000 EU at 1 EU = 1 MJ is 2.4 × 10¹⁵ J — **2.4 petajoules, 0.574
   megatons**, not the 2.4 exajoules and half-gigaton the brief states. The brief's
   own high-end figure is out by a factor of 1,000. Corrected, it is worse, not
   better: his Stage's Max Grade is EX, whose floor is 1.24 × 10²⁹ J, so the
   largest named reserve in canon cannot pay for **one** attack at his own Grade's
   minimum. It is short by a factor of 5.2 × 10¹³.

3. **Two cards break the mass–energy limit outright.** At 1 EU = 1 MJ, Draen
   Varos's Forge-Heart holds 6.0 × 10¹⁸ J in a crystal his own card weighs at nine
   kilograms — 7.5 times the rest-mass energy of the crystal. Kaelzar's 3 billion
   EU/g is 33 times c². Nothing made of matter can store more energy than its own
   mass–energy; the contents would outweigh the container. This is not a tuning
   problem and no choice of Grade table fixes it. **Any constant above ≈ 1.5 × 10⁴
   J/EU puts Draen Varos over the limit**, and the brief's constant is 67 times
   that.

**1 AU/s = 1 MW fails harder and fails on its own**, without reference to the EU
constant at all. One megawatt of throughput at any attested η leaks a waste heat
of 37 MW to 4 × 10¹⁹ W into a human body whose combined perfusion and evaporative
capacity is about 2 kW. **Not one attested practitioner survives one second of
their own stated output.** The best case in the whole anchor set, Yoko Mishiro at
75 AU/s, cooks to death in 33 milliseconds.

**What does hold.** The Grade table's joule → TNT arithmetic is exact on every row
but one. The X row's ceiling is the Moon's gravitational binding energy to within
0.2%, which is a real calibration and a good one. Grades S and SS are correct
against real blast scaling. The Ledger has a spine; the spine is about three
decades lower than the brief puts it, and the AU/s axis needs a separate constant
rather than the same one.

---

## Method, and the constants used

Laws named where used. Values fixed once, here:

| quantity | value | why this one |
|---|---|---|
| 1 ton TNT | 4.184 × 10⁹ J | the thermochemical definition (1 g TNT ≡ 1,000 cal ≡ 4,184 J). This is definitional, not measured, so the joule → TNT chain can be checked exactly. |
| body mass | 70 kg | standard reference adult |
| body specific heat | 3.5 kJ·kg⁻¹·K⁻¹ → **245 kJ/K** | the classical figure. The 2023 measurement puts the whole body at 2.98 (range 2.44–3.39) kJ·kg⁻¹·K⁻¹ [1]. Using the *higher* number makes every temperature rise below **smaller**, so every thermal finding here is stated in canon's favour. |
| lethal core rise | +5 K (37 → 42 °C) | thermal budget 5 × 245 kJ = **1.225 MJ** |
| energy to boil a body dry | 1.10 × 10⁸ J | 70 × 3,500 × 63 K to 100 °C, then 42 kg of body water × 2.257 MJ/kg |
| body heat shedding, total | ≈ **2 kW** peak | max evaporative 1.0–1.7 kW at sweat rates of 1.5–2.5 L/h [2], plus perfusion transport 1.6 kW at rest (5 L/min × 3.6 kJ·kg⁻¹·K⁻¹ × 5 K), 8 kW at maximum cardiac output but only as internal redistribution |
| 5 psi (34 kPa) blast radius | R = (0.47 – 0.71) km × Y_kt^⅓ | Hopkinson–Cranz cube-root scaling; 0.71 is the nuclear-weapon FAQ's constant, 0.47 a 1 kt surface burst [3] |
| c² | 8.98755 × 10¹⁶ J/kg | |
| σ (Stefan–Boltzmann) | 5.6704 × 10⁻⁸ W·m⁻²·K⁻⁴ | body radiating area 1.8 m², ε = 0.98 |
| air | ρ = 1.225 kg/m³, c_p = 1,005 J·kg⁻¹·K⁻¹ | sea level, 15 °C |

---

## 1. The constant

### 1.1 What 1 EU = 1 MJ asserts

One EU is 239 grams of TNT. One AU/s is a megawatt — about 400 household kettles
at 2.5 kW each, not a thousand, but the brief's order of magnitude is right.

The two constants together assert something the brief does not say out loud and
that everything in §3 turns on: since 1 MW = 1 MJ/s, **1 AU = 1 EU**. The brief
does not merely scale the two axes, it identifies them.

### 1.2 The low end: Yukazuri Moto

> `wiki/Volume I — Character Cards/Yukazuri Moto.md:61`
> **EU Reserve** · 3,100 EU · **Flux Density** 290 EU/g · **Output** 480 AU/s · **η** 0.89

At 1 EU = 1 MJ her reserve is 3.1 GJ, or 741 kg of TNT, in a woman.

**Energy density.** 3.1 GJ in a 70 kg body is 44 MJ/kg. Gasoline is 46 MJ/kg. TNT
is 4.18 MJ/kg. A lithium-ion cell is 0.9 MJ/kg. The weakest practitioner with an
attested sheet is, by this constant, a tank of petrol that walks.

**Against the body that holds it.** 3.1 GJ is **28 times** the 1.10 × 10⁸ J needed
to heat a 70 kg body to boiling and drive off all of its water. A 3.6% containment
failure vaporises her.

**Against what her card says she does with it.** Her three techniques are the
cleanest test in canon, because the card states cost *and* duration on the same
line:

> `:83` **Nerve Reading** · *Somnalis* · 140 EU — Reads autonomic state, muscle pre-tension and Wellspring signature within 15 ft; **0.3–0.5 s advance notice of physical intent for four seconds.**
>
> `:84` **Coagulatio Seal** · 260 EU — Contact-activated clotting acceleration, or a 90-second Aether-suppression seal on an open channel.
>
> `:85` **Somnalis Drift** · 390 EU — Full-broadcast 25 ft sympathetic suppression, eight-second duration, **risks severe Resonance Saturation bleedback.**

Priced at 1 EU = 1 MJ, and taking her stated η = 0.89, so that 11% of every
expenditure becomes waste (FoW VII:86 names exactly this: "At η 0.50, half of
every expenditure is wasted as heat, noise and structural bleed"):

| working | EU | J | TNT equiv | mean power | waste at η 0.89 | core rise | lethal doses |
|---|---|---|---|---|---|---|---|
| Nerve Reading | 140 | 1.40 × 10⁸ | 33 kg | 35 MW over 4 s | 15.4 MJ | **+63 K** | 12.6 |
| Coagulatio Seal | 260 | 2.60 × 10⁸ | 62 kg | 2.9 MW over 90 s | 28.6 MJ | **+117 K** | 23.4 |
| Somnalis Drift | 390 | 3.90 × 10⁸ | 93 kg | 48.8 MW over 8 s | 42.9 MJ | **+175 K** | 35.0 |

Working, Nerve Reading: 140 EU × 10⁶ J/EU = 1.40 × 10⁸ J; waste = 0.11 × 1.40 ×
10⁸ = 1.54 × 10⁷ J; ΔT = 1.54 × 10⁷ / 2.45 × 10⁵ = 62.9 K; ÷ 5 K = 12.6.

Reading somebody's muscle tension from fifteen feet costs the energy of 33 kg of
TNT and kills the reader thirteen times over in waste heat alone. Canon does not
describe it that way: the line says she uses it, casually, to read intent.

**The same three workings at the measured constant.** `fit.json` `direct_pairs`
prices one EU at 112 to 3,571 J from three lines on Dougou Ozumu Zettari's sheet
and Spellcraft page — the only places canon states an EU cost and a joule output
for one working. At that constant:

| working | at 112 J/EU | at 3,571 J/EU |
|---|---|---|
| Nerve Reading | 15.7 kJ, waste 1.7 kJ, **+0.007 K** | 500 kJ, waste 55 kJ, **+0.22 K** |
| Somnalis Drift | 43.7 kJ, waste 4.8 kJ, **+0.020 K** | 1.39 MJ, waste 153 kJ, **+0.63 K** |

A tenth of a degree to half a degree of core warming for a serious working, over
seconds, shed in minutes. That is what a working *should* cost a body. It is also,
unprompted, the number canon's own page already carries.

**What physics requires of the constant, from the heat side alone.** Require that
spending a reserve does not cook the practitioner: (1 − η) × EU_spent × k ≤ 1.225
MJ. Solving for k per anchor:

| anchor | η | whole-reserve spend | k must be below |
|---|---|---|---|
| Yukazuri Moto | 0.89 | 3,100 EU | 3,592 J/EU |
| Naori Yukari | 0.40 | 42,000 EU | 48.6 J/EU |
| Yoko Mishiro | 0.50 | 185,000 EU | 13.2 J/EU |
| Ara Min Mahuo | 0.70 | 4,200,000 EU | 0.97 J/EU |

The ceiling Yukazuri's own numbers set, 3,592 J/EU, is the top of the measured band
of 112–3,571 J/EU to three significant figures. Two independent methods — canon's
one self-pricing page, and a human body's heat capacity — put the constant in the
same place. The brief's 10⁶ J/EU is 280 to 10⁶ times above every row of that table.

The spread down the column is itself a finding, and it is the same spread C-034
records: the reserves are not ordered, so no single k satisfies all four, and the
disagreement is the cards' rather than the constant's.

### 1.3 The high end: the Primate

> `wiki/Volume I — Character Cards/Aurelian Prudentius Custos Clausorum · The Primate.md:85`
> **EU Reserve:** **2,400,000,000.** Confirmed 2026-09-12. Fracture of Worlds specifies no EU table by Stage; this figure was extrapolated from the two attested Band V reserves in project canon, Verinus VII at 620,000,000 and Kwon Mu-jin at 850,000,000, both at Stage XII, and stands as final.

**Correcting the brief.** 2.4 × 10⁹ EU × 10⁶ J/EU = **2.4 × 10¹⁵ J**. That is 2.4
petajoules. In TNT: 2.4 × 10¹⁵ / 4.184 × 10⁹ = 573,600 tons = **0.574 megatons**.
The issue text says 2.4 exajoules and half a gigaton; both are a factor of 1,000
high. Stated plainly because the brief asks for it plainly.

For scale, 0.574 Mt is about 38 Hiroshimas, or a tenth of the largest weapon ever
detonated. In mass-equivalent, E/c² = 2.4 × 10¹⁵ / 8.988 × 10¹⁶ = **26.7 grams**.
The entire reserve of the largest named practitioner in canon is the rest-mass
energy of a golf ball.

**Against his own Grade.** Read through Part Five, Stage XIV, Zenith, Max Grade EX
(FoW II:77), and Part Four's EX row:

> `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md:39`
> | EX | 1,201–1,500 | 1.24×10^29 – 6.906×10^37 J | 50–100% c |

1.24 × 10²⁹ / 2.4 × 10¹⁵ = **5.2 × 10¹³**, or 13.71 decades short — matching
`fit.json` `by_stage` exactly. To put his reserve at one EX-Grade strike, one EU
would have to be 5.2 × 10¹⁹ J. To put Yukazuri's Nerve Reading inside a body, it
must be under 3.6 × 10³ J. **The two ends of the attested range demand constants
sixteen orders of magnitude apart.** No single k exists. This is the physical
statement of C-034's second half, and physics agrees with it rather than softening
it.

(`fit.json` `meta.stage_xiv_reading` records that Part Eleven declines to quantify
Zenith where Part Five gives it EX. That reading is Phase 1's and is not disturbed
here; the shortfall is 11.75 decades at Stage XIII on the same arithmetic, so the
finding does not rest on the Zenith row.)

### 1.4 The hard ceiling: mass–energy

**The law.** E = mc². No arrangement of matter stores more energy than its own
rest-mass energy; matter–antimatter annihilation, the densest process known,
reaches 1 c² per kilogram of fuel and nothing exceeds it. Rotating black holes are
the general-relativistic maximum for extractable stored energy, at 0.29 c² in spin
(Penrose) and up to 0.42 c² for accretion onto an extremal Kerr hole.

At 1 EU = 1 MJ, a Flux Density of F EU/g stores F × 10⁹ J/kg, so the limit is

    F_max = c² / (10⁶ J/EU × 10³ g/kg) = 8.99 × 10⁷ EU/g.

Measured against the 33 attested Flux Densities in `anchors.json`:

| card | Flux Density | J/kg at 1 EU = 1 MJ | in c² | verdict |
|---|---|---|---|---|
| Kaelzar · The Forge That Roars | 3 × 10⁹ EU/g | 3.0 × 10¹⁸ | **33.4 c²** | impossible |
| Draen Varos · The Red Forge Sentinel | 6.7 × 10⁸ EU/g | 6.7 × 10¹⁷ | **7.46 c²** | impossible |
| Kael Serradyn · The Burnmark | 1.63 × 10⁷ EU/g | 1.63 × 10¹⁶ | 0.181 c² | past the Kerr limit |
| Garron Vuldane | 1.35 × 10⁷ EU/g | 1.35 × 10¹⁶ | 0.150 c² | past the Kerr limit |
| Valthren Odrin | 1.26 × 10⁷ EU/g | 1.26 × 10¹⁶ | 0.140 c² | past the Kerr limit |
| Elion Drevas, Gimbzo, Serai Linthra, Mavra Cindrel, Ignatius | 5.4–9.4 × 10⁶ EU/g | 5.4–9.4 × 10¹⁵ | 0.060–0.105 c² | black-hole-spin density |
| Kwon Mu-jin | 1.8 × 10⁶ EU/g | 1.8 × 10¹⁵ | 0.020 c² | 22 × pure fission |
| Ara Min Mahuo | 8.5 × 10⁴ EU/g | 8.5 × 10¹³ | 9.5 × 10⁻⁴ c² | **exactly U-235 fission** (8.2 × 10¹³ J/kg) |
| the other twenty-one | 20 – 4.1 × 10⁴ EU/g | 2 × 10¹⁰ – 4.1 × 10¹³ | ≤ 4.6 × 10⁻⁴ c² | between chemical and nuclear |

Draen Varos is the decisive one, because his card states the *mass* as well:

> `wiki/Volume I — Character Cards/Draen Varos · The Red Forge Sentinel.md:37`
> **The Forge-Heart Crystal** · Alloyed with tempered slag from the Atlas Mantle, nine kilograms of Crystal and slag that reads as one structure. Flux Density **670 million EU/g.** Aether Output **98,000 AU/s.**

9,000 g × 6.7 × 10⁸ EU/g = 6.03 × 10¹² EU. At 1 EU = 1 MJ that is 6.03 × 10¹⁸ J.
The rest-mass energy of nine kilograms is 9 × 8.988 × 10¹⁶ = 8.09 × 10¹⁷ J. The
crystal holds **7.46 times more energy than it weighs**. There is no material,
field, vacuum state or geometry that does this; the stored energy would itself
gravitate and the object would be far inside its own Schwarzschild radius.

> `wiki/Volume I — Character Cards/Kaelzar · The Forge That Roars.md:106`
> Past the card's 3 billion EU/g line he enters the Silent Forge State: complete immobility until cooled by mantle contact.

**The threshold this sets.** Draen Varos goes over c² at any k above 8.09 × 10¹⁷ /
6.03 × 10¹² = **1.34 × 10⁵ J/EU**, and Kaelzar at any k above 3.0 × 10⁴ J/EU
(taking any crystal mass at all, since his figure is a density). The measured
112–3,571 J/EU clears both by one to two decades. **1 MJ/EU does not.** This is
the one finding in the note that rules out a whole region of constant rather than
merely making it uncomfortable.

---

## 2. The Grade table

> `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md:16`
> Grades use real-world energy equivalents drawn from physical TNT yield benchmarks and speed measurements.

That sentence is a testable claim, so it gets tested.

### 2.1 Joule → TNT: exact on twelve rows of thirteen

Dividing each row's joule figures by 4.184 × 10⁹ J/ton and comparing with the
prose glosses at `:45`–`:54`:

| Grade | joules (`:28`–`:40`) | computed TNT | prose gloss | |
|---|---|---|---|---|
| D | 2.092 × 10⁷ ceiling | 0.005 t | "0.005 tons TNT at the ceiling" | exact |
| C | 2.092 × 10⁷ – 1.046 × 10⁹ | 0.005 – 0.25 t | "0.005 to 0.25 tons TNT" | exact |
| B | 1.046 × 10⁹ – 4.6024 × 10¹⁰ | 0.25 – 11 t | "0.25 to 11 tons TNT" | exact |
| A | 4.6024 × 10¹⁰ – 4.184 × 10¹² | 11 – 1,000 t | "11 to 1,000 tons TNT" | exact |
| S | 4.184 × 10¹² – 2.42672 × 10¹³ | 1 – 5.8 kt | "1 to 5.8 kilotons TNT" | exact |
| SS | 4.184 × 10¹³ – 4.184 × 10¹⁴ | 10 – 100 kt | "10 to 100 kilotons TNT" | exact |
| SSS | 4.184 × 10¹⁴ – 4.184 × 10²¹ | 100 kt – 1 Tt | "100 kilotons to 1 teraton TNT" | exact |
| X | 4.184 × 10²¹ – 1.24 × 10²⁹ | 1 Tt – 29.637 Et | "1 teraton to 29.6 exatons TNT" | exact to 3 s.f. |
| EX | 1.24 × 10²⁹ – 6.906 × 10³⁷ | 29.637 Et – 16.506 Rt | "29.6 exatons to 16.512 ronnatons" | **0.04% out** |

Whoever built this column used the thermochemical ton throughout and did the
arithmetic correctly. The EX ceiling is the single exception: 6.906 × 10³⁷ /
4.184 × 10⁹ = 1.65057 × 10²⁸ tons = 16.506 ronnatons, not 16.512, and 16.512
rounds from neither. It is consistent with an intermediate rounding somewhere in
the original derivation. **Not filed as a conflict** — a fourth-significant-figure
slip in one gloss is noise in `CONFLICTS.md`, and it changes nothing anyone can
read a Grade off. Recorded here so it is not lost.

The gap between S's ceiling and SS's floor (2.42672 × 10¹³ to 4.184 × 10¹³, a
factor of 1.72 in no Grade at all) is already **C-036** and is not re-filed.

### 2.2 TNT → "what it wrecks": the column changes criterion three times without saying so

**The law.** Hopkinson–Cranz cube-root scaling: for a given overpressure, the
radius scales as the cube root of yield, R = Z · W^⅓, because the blast must heat
all the air in a sphere and that air's mass goes as R³ [3]. So a thousandfold
yield buys ten times the radius, and the *area* wrecked goes as W^⅔. Taking
severe structural damage at 5 psi (34 kPa), R = (0.47 – 0.71) km × Y_kt^⅓:

| row ceiling | yield | blast diameter 2R | canon's label | label's real size | |
|---|---|---|---|---|---|
| D | 5 kg | 16 – 24 m | "Wall level" | ~3 m | 6 × conservative |
| C | 250 kg | 59 – 89 m | "Small Building to low Building" | ~20 m | 3–4 × |
| B | 11 t | 209 – 316 m | "Building to Large Building" | ~50 m | 4–6 × |
| A | 1 kt | 0.94 – 1.42 km | "City Block to Multi-City Block" | ~0.3 km | 3–5 × |
| S | 5.8 kt | 1.7 – 2.6 km | "Small Town to Town" | ~2 km | **consistent** |
| SS | 100 kt | 4.4 – 6.6 km | "Town to Large Town" | ~5 km | **consistent** |
| SSS | 1 Tt | 940 – 1,420 km | "Large Town to Small Country" | ~200–350 km | 4–5 × in radius, ~20 × in area |
| X | 29.6 Et | 2.9 – 4.4 × 10⁵ km | "Country to Moon level" | — | criterion breaks |
| EX | 16.5 Rt | 2.4 – 3.6 × 10⁸ km | "Moon to Large Planet" | — | criterion breaks |

Read as one ladder this column is incoherent, and the incoherence has a shape:
**it is three criteria wearing one heading.**

- **D through B are a contact criterion.** Five kilograms of TNT laid against a
  masonry wall holes it; that is what a breaching charge is. As a *radius* it is
  six times short, but as a statement about what the energy does where it lands,
  "Wall level" is right. The same reading carries C and B.
- **S and SS are an area criterion, and they are correct.** 5.8 kt flattens
  2.2 km of town; 100 kt flattens 5.5 km. Both labels land. These two rows are the
  best-calibrated in the table and should be the ones any future revision anchors
  to.
- **A and SSS are the same area criterion, mis-labelled.** 1 kt severely damages a
  circle 1.2 km across — the core of a small town, not "Multi-City Block". 1 Tt
  damages a circle 1,200 km across, an area of 0.7 to 1.6 million km², which is
  one to three Frances; the K-Pg impactor was about 100 Tt. "Small Country" is out
  by an order of magnitude in area and the row is a small continent.
- **X and EX are a disassembly criterion, and the X row is exactly right.** The
  gravitational binding energy of the Moon is U = 3GM²/5R = 3 × 6.674 × 10⁻¹¹ ×
  (7.342 × 10²²)² / (5 × 1.7374 × 10⁶) = **1.2425 × 10²⁹ J**. The X ceiling is
  1.24 × 10²⁹ J. That agrees to 0.2% and is not a coincidence: **whoever wrote
  this row looked up how much energy it takes to blow the Moon apart, and got it
  right.** The EX ceiling, 6.906 × 10³⁷ J, is 33.5 × Jupiter's binding energy
  (2.06 × 10³⁶ J) — "Large Planet" is about 1.5 decades generous, but in the right
  neighbourhood. The EX+ floor is a fifth of a 13-Jupiter-mass brown dwarf's
  binding energy (3.49 × 10³⁸ J), so "Brown Dwarf level and beyond" is right to
  half a decade.

  These rows cannot be read as blast at all: 29.6 exatons as an airburst has a
  5 psi radius of 150,000–220,000 km, most of the way to the Moon, which is not
  what "Moon level" means. The criterion changed and the column did not say so.

**Consistent rows: S, SS, X, EX+ (and EX to 1.5 decades). Inconsistent rows: D, C,
B, A, SSS.** The inconsistency is not a mistake in any one row; it is that the
column changes from contact damage to area damage to gravitational disassembly
across thirteen rows, and a reader who carries one criterion across the table is
wrong by 10² to 10⁵.

### 2.3 The differential rule is not calibrated

> `:17` **One full Tier Grade above** an opponent in the relevant stat wins a direct exchange of that stat category without meaningful contest.

The energy ratio from a Grade's floor to its ceiling, row by row: F 5×, E 50×,
D 1,395×, C 50×, B 44×, A 91×, S 5.8×, SS 10×, SSS 10⁷×, X 3 × 10⁷×, EX 5.6 × 10⁸×.

So "one full Grade above" means a factor of 5.8 at S and a factor of 5.6 × 10⁸ at
EX, while the Sub-Stat column advances in even steps of 150 to 300 points
throughout. A Grade is a constant-width bracket on the Sub-Stat axis and a
bracket varying by a factor of 10⁸ on the energy axis. The rule that decides who
wins is therefore reading two different things depending on where on the ladder it
is applied. This is a design observation, not a contradiction — no page says the
brackets should be equal-width — but any tier ladder built in WAR-8 inherits it.

### 2.4 The travel-speed column against the attack-output column

**The law.** Kinetic energy E = ½mv², and above about 0.1c, E = (γ − 1)mc².

If a practitioner's body is the weapon — and FoW III:30 explicitly contemplates it,
"A body slam distributes enormous total energy across a broad contact zone" — then
an 80 kg body at the travel ceiling of its own row should deliver energy inside
that row's attack band. It does not:

| row | travel ceiling | ½mv² (80 kg) | attack band floor | ratio |
|---|---|---|---|---|
| Hollow | 12.4 m/s | 6.2 kJ | (ceiling 60 J) | **103 × over the ceiling** |
| F | 60 m/s | 144 kJ | 60 J | 2,400 × over |
| E | 150 m/s | 900 kJ | 300 J | 3,000 × over |
| D | 340 m/s | 4.6 MJ | 15 kJ | **inside the band** |
| C | 510 m/s | 10.4 MJ | 20.9 MJ | 0.50 × |
| B | 1,372 m/s | 75.3 MJ | 1.05 GJ | 0.072 × |
| A | 8,575 m/s | 2.94 GJ | 46.0 GJ | 0.064 × |
| S | 68,600 m/s | 188 GJ | 4.18 TJ | 0.045 × |
| SS | 343,000 m/s | 4.71 TJ | 41.8 TJ | 0.11 × |
| SSS | 10% c | 36 PJ | 418 TJ | **inside the band** |
| X | 50% c (γ = 1.155) | 1.11 EJ | 4.18 ZJ | 2.7 × 10⁻⁴ |
| EX | 99% c (γ = 7.09) | 43.7 EJ | 1.24 × 10²⁹ J | 3.5 × 10⁻¹⁰ |

The two columns were calibrated independently and agree on two rows out of twelve.
From C upward the body is always the weaker weapon, by one to ten orders; at the
bottom it is enormously the stronger. **The Hollow row is the sharpest case, and it
needs no practitioner at all: an ordinary 70 kg person walking at 1.4 m/s carries
69 J of kinetic energy, and a 1 m fall delivers 687 J.** Both exceed the Hollow
attack-output ceiling of "below 60 J", and the fall is an E-Grade output. Against
FoW II:16's promise of "real-world energy equivalents", the Hollow and F rows are
set below ordinary human capability: a trained punch (effective mass ~3 kg at
9 m/s) is about 120 J, a war-bow arrow 80–140 J, a 9 mm round about 500 J, a .50
BMG 18 kJ. F-Grade, "no longer fully mortal in potential", tops out below a pistol.

The Part Four / Part Six gap between Mach 4 and Mach 5 is **C-038** and is not
re-filed.

### 2.5 What moving that fast actually costs

**The laws.** Aerodynamic drag power P = ½ρv³C_dA, and stagnation-point convective
heating by Sutton–Graves, q = 1.7415 × 10⁻⁴ √(ρ/R_n) · v³ W/m².

Taking a running human as C_d ≈ 1.0, A = 0.7 m², nose radius 0.1 m, at sea level:

| Grade | travel ceiling | drag power | stagnation heat flux |
|---|---|---|---|
| D | 340 m/s | 16.9 MW | 0.024 MW/m² |
| B | 1,372 m/s | 1.11 GW | 1.57 MW/m² |
| A | 8,575 m/s | **270 GW** | **384 MW/m²** |
| S | 68,600 m/s | **138 TW** | 2.0 × 10⁵ MW/m² |
| SS | 343,000 m/s | 1.7 × 10¹⁶ W | 2.5 × 10⁷ MW/m² |

For comparison, Apollo's peak re-entry heating was about 5 MW/m², at high altitude
where ρ is thousands of times lower.

Canon anticipates this qualitatively and deserves credit for it:

> `:107` At A-Grade movement generates significant environmental effects, heat buildup from air friction, pressure waves, surface disruption, without deliberate technique activation.

It is right, and the magnitude is 384 MW/m² and 270 GW. **The constant cannot
supply it.** At 1 AU/s = 1 MW, Sodoku Moto's ~3,800 AU/s is 3.8 GW, which is 1.4%
of the drag power his own A-Grade travel ceiling demands. Ignatius's 5.1 million
AU/s is 5.1 TW against S-Grade's 138 TW — 3.7%. Every attested output is one to
two orders short of the power needed just to push air out of the way at the speed
the same table grants. Raising the AU/s constant to close that gap makes §4's
thermal problem worse by the same factor.

---

## 3. Power against energy: the drain arithmetic

### 3.1 The identity does the work, not the constant

At 1 EU = 1 MJ and 1 AU/s = 1 MW, time to empty is

    t = EU_reserve × 10⁶ J / (AU/s × 10⁶ W) = EU_reserve / (AU/s) seconds.

The factors of 10⁶ cancel. **Every drain time below is a property of the two card
figures and of the brief's decision to make 1 AU = 1 EU. It does not depend on the
value of the constant at all.** Any ruling that keeps the two axes equal inherits
this table whatever number it picks; a ruling that separates them (1 EU = k J,
1 AU = k′ J) scales every row by k/k′.

### 3.2 Every anchor that states both

| s to empty | entity | EU reserve | AU/s | η | what the card says on the same page |
|---|---|---|---|---|---|
| **0.72** | Gimbzo | 4.8 × 10¹⁴ | 6.7 × 10¹⁴ | 0.94 | "he does not burn essence, he stores it, like a cistern. Endurance fights favour him absolutely" |
| **1.08** | Ignatius / Darius | 5,500,000 | 5,100,000 | 0.90 | legacy sheet, flagged unsourced on the card itself |
| **3.23** | Iracordas | 16,800 | 5,200 | 0.93 | "prolonged exposure to his aura destabilises discipline" |
| **5.50** | Artemis Amagiri Moto | 41,800 | 7,600 | 0.84 | "**Deep reserve** for **sustained** interception, anti-charge fields and **repeated** lane denial" |
| 6.46 | Yukazuri Moto | 3,100 | 480 | 0.89 | |
| 6.67 | Krothar Veylshroud | 2,800,000 | 420,000 | — | |
| 7.24 | Naiser Yukari | 2,460 | 340 | — | |
| 10.00 | Naevra Yukari | 185,000 | 18,500 | 0.96 | |
| 10.00 | Naori Yukari | 42,000 | 4,200 | 0.40 | |
| 12.05 | Vethraun Ashmaw | 9,400 | 780 | 0.91 | |
| 12.63 | Niran Yukari | 485,000 | 38,400 | 0.89 | |
| 15.77 | Anryū Ichimonji | 820,000 | 52,000 | 1.05 | |
| 18.08 | Mizuki Moto | 470,000 | 26,000 | 0.82 | |
| 19.47 | Ayame Yuno | 37,000 | 1,900 | 0.86 | "Optimised for **sustained rites**, mass-oath work and battlefield-scale blessings" |
| 20.59 | Rengai Zettari | 1,400,000 | 68,000 | 0.78 | |
| 22.50 | Rashani Zettari | 540,000 | 24,000 | 0.81 | |
| 23.59 | Dougou Ozumu Zettari | 92,000 | 3,900 | 0.99 | |
| 24.15 | Lucius Xenotro | 2,850,000 | 118,000 | 0.92 | |
| 25.69 | Muken Moto | 1,850,000 | 72,000 | 0.84 | |
| 25.96 | Yorime Seikai | 74,000 | 2,850 | 0.94 | |
| 70.59 | Ara Min Mahuo | 4,200,000 | 59,500 | 0.70 | |
| 336 | Arctic Lion (Level 500) | 4,200,000 | 12,500 | 0.91 | |
| 353 | Sodoku Moto | 1,340,000 | 3,800 | 0.84 | |
| 543 | Kwon Mu-jin | 850,000,000 | 1,566,000 | 0.87 | |
| 2,467 | Yoko Mishiro | 185,000 | 75 | 0.50 | |
| **56,250** | Borin Ironheart | 180,000,000 | 3,200 | 0.91 | "high sustained throughput, optimized for **multi-hour forge operations**" |

Twenty-six anchors, 0.72 s to 15.6 hours — **4.9 decades**. Canon defines the
quantity this table measures:

> `wiki/Fracture of Worlds — The Living System/VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md:86`
> [η is] The single most important variable in sustained combat, because it determines how long the reserve lasts under continuous output.

### 3.3 Flagged: reserves that empty faster than the page they sit on

Five anchors state a duration, or a description of duration, that their own two
numbers contradict:

- **Gimbzo, 0.72 seconds.** `Gimbzo.md:58` calls the reserve a cistern and says
  "Endurance fights favour him absolutely"; `:61` gives "6.7 × 10¹⁴ AU/s". Together
  they say the endurance fighter is dry in under a second. The sharpest case in
  the set, and the one any ruling on the EU↔AU relation should be tested against
  first.
- **Ignatius / Darius, 1.08 seconds.** `scenes/09_dabney_the_undamped_thing.md:111`
  has him holding a working: "his right hand had been open in front of him for the
  last four seconds of it". `scenes/14_darius_two_men_who_would_not_take_the_seat.md:185`
  has a sustained area working — "the Obsession Force went on standing over four
  streets". The scene itself presumes duration: `09:117` "none of the burn of the
  seventh Fist **held too long**". Four seconds of holding against a 1.08 s
  reserve. The card flags its own figures as unsourced (`:141`, "I cannot source EU
  benchmarks by Stage"), which is where the ruling should start.
- **Artemis Amagiri Moto, 5.5 seconds.** The strongest single-line contradiction,
  because one line does both jobs: `:56` "**Deep reserve** for **sustained**
  interception, anti-charge fields and **repeated** lane denial", and `:58` "7,600
  AU/s". Deep, sustained and repeated, for five and a half seconds.
- **Iracordas, 3.23 seconds**, against `:64` "prolonged exposure to his aura".
- **Ayame Yuno, 19.5 seconds**, against `:58` "Optimised for sustained rites,
  mass-oath work and battlefield-scale blessings rather than short violent
  exchanges" — a rite that runs under twenty seconds.

And one that **agrees**, worth recording because it is the only one:
**Borin Ironheart, 15.6 hours** against `:103` "optimized for multi-hour forge
operations rather than combat exchange". His two numbers and his prose describe
the same person.

These are not filed as `CONFLICTS.md` rows. See §5.

### 3.4 How many of their own strikes can they pay for?

A second reading, on the energy axis: a working's cost against the Grade band its
page claims, at 1 EU = 1 MJ and through the stated η.

- **Ara Min Mahuo.** Stage VIII, Max Grade S, floor 4.184 × 10¹² J. Reserve
  4.2 × 10⁶ EU = 4.2 × 10¹² J; through η 0.70, delivered = 2.94 × 10¹² J. He spends
  **his entire reserve and still falls 30% short of one minimum S-Grade blow.** A
  practitioner cannot reach his own Grade's floor once, ever.
- **Yukazuri Moto.** Her card states a 2.1 PJ strike (`:57`). At 1 EU = 1 MJ that
  costs 2.1 × 10⁹ EU against a 3,100 EU reserve — **677,000 times her whole
  reserve.** (The Strike-Force-against-Stage half of this is already **C-040**;
  what is new here is the price in EU.)
- **Artemis Amagiri Moto.** `:62` states 88 PJ. Reserve 41,800 EU = 4.18 × 10¹⁰ J.
  He can afford **1/2,100,000th** of one of his own strikes.
- **Dougou Ozumu Zettari**, the one sheet that prices itself, is the exception:
  92,000 EU against an 8–20 MJ apex gives 4,600 apex strikes at 1 EU = 1 MJ, and
  12 to 33 at the measured constant. Twelve to thirty-three full-power strikes
  from a full reserve is a fightable number. It is also the only anchor in the set
  that produces one.

---

## 4. The thermodynamics of η

> `wiki/Fracture of Worlds — The Living System/VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md:86`
> **Eta (η), Efficiency** — the ratio of Essence spent to Essence that arrives as intended effect. At η 0.50, half of every expenditure is wasted as heat, noise and structural bleed. At η 0.90, ninety percent converts to clean output.

### 4.1 The law, and why the question has only one answer

**First law:** the missing fraction cannot vanish. **Second law:** it cannot come
back as work. **Gouy–Stodola:** the lost work rate equals ambient temperature times
the entropy generation rate, Ẇ_lost = T₀ · Ṡ_gen — so every irreversibility in the
conversion reappears as low-grade heat at ambient temperature. That is the whole
answer to "where does it go": (1 − η) of every expenditure becomes **heat**, at the
lowest useful grade, at the place where the irreversibility happened. Light, sound
and mechanical strain are transport channels out of that place, not alternatives
to it, and each thermalises wherever it is absorbed.

Canon's own wording matches the physics exactly — "heat, noise and structural
bleed" is a correct list of the three channels — and one card names all three and
says they normally leak outward:

> `wiki/Volume I — Character Cards/Anryū Ichimonji.md:29`
> | **Efficiency (η)** | **1.05** — near-zero waste. ***No field pressure, aura warmth, or harmonic noise leaks outward*** |

### 4.2 The real mechanisms, named

The candidate dissipation mechanisms, with the law each obeys, are the ones that
should sit under any in-world account:

1. **Resistive / dielectric loss** — if the carrier behaves like charge or field:
   P = I²R, or per unit volume P = ½ωε₀ε″|E|². Tissue is a lossy dielectric at
   radio frequencies; this is the mechanism a microwave oven uses on a body, and
   it deposits heat volumetrically rather than at the surface.
2. **Viscoelastic / acoustic attenuation** — if the carrier is mechanical: soft
   tissue attenuates at roughly 0.5 dB·cm⁻¹·MHz⁻¹, and the absorbed fraction
   becomes heat where it is absorbed. This is how focused ultrasound ablates, and
   it is canon's "noise" channel with the physics attached.
3. **Radiative loss** — Stefan–Boltzmann, P = εσA(T⁴ − T₀⁴). The light channel,
   and the one that gives a tell (§4.5).
4. **Transport** — Pennes' bioheat equation, ρc ∂T/∂t = ∇·(k∇T) + ω_bρ_bc_b(T_a − T)
   + Q_m + Q_ext. The perfusion term ω_b is the body's only fast internal heat
   mover, and it is small: 1.6 kW at rest, 8 kW at maximum cardiac output, and
   that is redistribution, not disposal.
5. **Damage** — CEM43 thermal dose (Sapareto & Dewey, 1984): t₄₃ = Σ R^(43−T) Δt
   with R = 0.5 above 43 °C and 0.25 below; the common injury threshold is
   CEM43 ≥ 120 minutes [4]. At 45 °C that threshold arrives in 30 min, at 50 °C in
   56 seconds, at 60 °C in 55 milliseconds. Above ~60 °C protein denaturation is
   effectively immediate and CEM43 stops being the binding constraint.
6. **Structural load on the Crystal** — thermal stress, σ = EαΔT/(1 − ν). For a
   brittle crystalline solid (E ≈ 70 GPa, α ≈ 8 × 10⁻⁶ K⁻¹, ν ≈ 0.25, tensile
   strength ≈ 50 MPa) the critical differential is **ΔT ≈ 67 K**. That is a real
   number for Crystal Fracture Events, and it sits within a factor of three of the
   temperature that kills the tissue around it — so under any load that threatens
   one, the other is also in play.

### 4.3 What the waste heat does, at each anchor's scale

Waste power at 1 AU/s = 1 MW, reading AU/s as the spend rate and η as the fraction
delivered: P_waste = (1 − η) × AU/s × 10⁶ W. Body heat capacity 245 kJ/K, lethal
rise +5 K, vaporisation 1.10 × 10⁸ J.

| anchor | AU/s | η | waste | core rise | time to +5 K | time to vaporise |
|---|---|---|---|---|---|---|
| Yoko Mishiro | 75 | 0.50 | 37.5 MW | 153 K/s | **33 ms** | 2.9 s |
| Yukazuri Moto | 480 | 0.89 | 52.8 MW | 216 K/s | **23 ms** | 2.1 s |
| Dougou Ozumu Zettari | 3,900 | 0.99 | 39.0 MW | 159 K/s | **31 ms** | 2.8 s |
| Sodoku Moto | 3,800 | 0.84 | 608 MW | 2,480 K/s | **2.0 ms** | 0.18 s |
| Naori Yukari | 4,200 | 0.40 | 2.52 GW | 10,300 K/s | **0.49 ms** | 44 ms |
| Ara Min Mahuo | 59,500 | 0.70 | 17.9 GW | 72,900 K/s | **69 µs** | 6.2 ms |
| Kwon Mu-jin | 1,566,000 | 0.87 | 204 GW | 8.3 × 10⁵ K/s | **6.0 µs** | 0.54 ms |
| Ignatius / Darius | 5,100,000 | 0.90 | 510 GW | 2.1 × 10⁶ K/s | **2.4 µs** | 0.22 ms |
| Gimbzo | 6.7 × 10¹⁴ | 0.94 | 4.0 × 10¹⁹ W | 1.6 × 10¹⁴ K/s | **30 fs** | 2.7 ps |

**Not one anchor survives one second of their own stated output.** The best case
in canon — the smallest AU/s on any sheet, Yoko Mishiro's 75 — is 37.5 MW of waste
against a body that can shed about 2 kW. That is 18,750 times over capacity, and
she is the *easy* one.

Note the perversity: **η barely matters.** Dougou at η 0.99 dies in 31 ms and Naori
at η 0.40 dies in 0.49 ms. A factor of 60 in waste fraction buys a factor of 60 in
time to death, when the shortfall is a factor of 10⁴ to 10¹⁶. At this constant η
is not "the single most important variable in sustained combat"; it is a rounding
error on an instantaneous death. **That is the clearest statement of why the power
constant is wrong: it destroys the mechanic η exists to create.**

**What the constant would have to be.** For the waste to sit at the body's 2 kW
ceiling: k′ = 2,000 / ((1 − η) × AU/s) J per AU. Yukazuri 37.9, Yoko 53.3, Sodoku
3.3, Naori 0.79, Ara Min 0.11, Ignatius 0.004 J/AU. So sustained full output at a
card's stated AU/s is survivable only at **0.004 to 53 joules per AU** — one to
five decades *below* even the measured 112–3,571 J/EU. Two honest readings follow,
and this note takes neither:

- **AU/s is a peak rate, not a sustained one.** Nothing on any page says a
  practitioner runs at their AU/s continuously; "the output rate ... per second of
  sustained operation" (FoW VII:85) is suggestive but does not say "indefinitely".
  Read as a burst ceiling held for a second or two, the measured constant works.
- **The waste does not land in the body.** Canon's own wording supports this — the
  Anryū line puts field pressure, aura warmth and harmonic noise *outward*. Then
  the constraint moves from the practitioner to the room, and §4.5 is where it
  goes.

### 4.4 Why the waste cannot pass *through* a body: Fourier's law

If the loss is generated inside a Soul Crystal in the chest and must conduct out,
then q = −k∇T binds it. Yukazuri's 52.8 MW through 1.8 m² of skin is 29.3 MW/m²;
across 3 mm of skin at k ≈ 0.4 W·m⁻¹·K⁻¹ that needs a gradient of

    ΔT = qL/k = 2.93 × 10⁷ × 0.003 / 0.4 = 2.2 × 10⁵ K.

Two hundred thousand kelvin across three millimetres of skin, to shed the waste of
the *weakest* sheet in the anchor set. Skin chars at about 200 °C.

**This is a boundary condition, not a failure.** It says the loss cannot be created
inside the body and conducted out — so if the constant is anywhere near the brief's
value, the Soul Crystal cannot be a battery in the chest. It has to be an aperture
whose dissipation happens at or outside the body's surface. That is a real,
findable constraint of exactly the kind a glyph supplies, and Phase 2 can build on
it without inventing anything: it follows from Fourier's law and the card's own
two numbers.

### 4.5 If the waste goes outward: the tell, and the counterplay

Taking Yukazuri's 52.8 MW as radiated from a 1.8 m² surface at ε = 0.98, Stefan–
Boltzmann gives the surface temperature:

    T = (P / εσA)^¼ = (5.28 × 10⁷ / (0.98 × 5.6704 × 10⁻⁸ × 1.8))^¼ = **4,790 K**

The Sun's photosphere is 5,772 K. She glows white, a little cooler than sunlight,
and the whole of her does. Steel melts at 1,810 K.

The flux at range, P/4πr², against real thresholds:

| effect | threshold | radius |
|---|---|---|
| pain on bare skin | 2 kW/m² | 46 m |
| wood ignites (piloted) | 12.5 kW/m² | 18 m |
| rapid burns | 30 kW/m² | 12 m |

And if the same power left as sound instead, the intensity at 1 m is 4.2 MW/m²,
which is **186 dB** re 20 µPa — eardrum rupture is about 160 dB.

**This is the fair-play shape the mechanic wants.** An η loss that leaves the body
is not free: it is a lamp you can see from four hundred metres, a burn radius that
endangers your own side, a sound that deafens the room, and a reason to fight in
rain, in water, in open ground or behind cover. Every one of those is a counter a
player can find by reading a thermal-radiation table, and every one is a tell.

### 4.6 η above 1: not a violation, if the environment pays

Four sheets and one system row put η above 1:

> `VII. Aether Class ... (Parts Seventeen–Nineteen).md:100`
> | 8 · Archmaster | XIII–XIV Principality to Zenith | 0.95–1.2 | Biomes carry the practitioner's doctrine. Above 1.0 the Continuum recognizes the expression as law and supplements it with ambient flow; the environment becomes a co-author. |

**This is physically coherent, and canon got the reasoning right.** An efficiency
above unity violates the first law only for a *closed* system. Open systems exceed
it routinely: a domestic heat pump delivers a coefficient of performance of 3 to 5
precisely because it moves energy from an external reservoir rather than making it.
Canon's clause — "supplements it with ambient flow" — is the correct escape, and it
names the right price: there must be a reservoir, and it must measurably deplete.

Quantified, at Anryū Ichimonji's 52,000 AU/s and η 1.05: of every 1.05 delivered,
0.05 is drawn in, so 4.76% of 5.2 × 10¹⁰ W = **2.48 GW** comes out of the
surroundings. If it comes out as heat from sea-level air, cooling it by 10 K
requires

    V = 2.48 × 10⁹ / (1.225 × 1,005 × 10) = 2.05 × 10⁵ m³ per second,

a sphere 36.6 m in radius, every second. A practitioner running η > 1 in air
produces a rushing inward wind, condensation, frost and a falling barometer in a
seventy-metre bubble. That is measurable with a thermometer, and it is a tell
anyone can be taught to read. It also supplies the counter: **starve the
reservoir** — fight them in still air behind glass, in vacuum, on Aether-dead
ground — and η falls back below 1 by definition.

### 4.7 What Essence Starvation has to sit on

> `VII. Aether Class ... (Parts Seventeen–Nineteen).md:83`
> **EU (Essence Units)** — the raw reserve. ... Operating below **ten percent EU** produces Essence Starvation: reduced stat expression, Shell degradation, Trait flickering.

The physical basis Phase 2 needs, stated as findings rather than as rules:

1. **Starvation and overheating are the same clock, and the constant decides which
   one runs out first.** At 1 AU/s = 1 MW the thermal clock finishes 10⁴ to 10¹⁶
   times sooner than the reserve does, so nobody ever reaches ten percent EU — they
   cook at ninety-nine. The mechanic canon defines cannot occur. At a constant near
   the measured one, the two clocks run at comparable speed, and **that** is what
   makes Essence Starvation a decision at the table rather than a footnote.
2. **The threshold has a physical reading available.** At ten percent reserve, what
   is left has to do the same work through a lower stored density, which in every
   real analogue (a discharging cell's rising internal resistance, a draining
   capacitor's falling drive) means a falling η and therefore a rising waste
   fraction. That gives Starvation a mechanism with a direction: the symptoms
   canon already lists — reduced stat expression, Shell degradation, Trait
   flickering — are what a system does when its efficiency collapses and its waste
   heat climbs at the moment it can least afford either. No page says this; it is
   what the physics would say if asked, and it needs Isaac's word before it is
   anything more.
3. **The tissue-damage and crystal-fracture thresholds are within a factor of three
   of each other** (CEM43 injury at sustained 43–50 °C; thermal fracture at ΔT ≈
   67 K). Whatever hurts the practitioner is close to what cracks the Crystal, so
   Starvation and Crystal Fracture are not independent failure modes — they are two
   readings of one overload, which is how canon already treats them (FoW II:61,
   forced advancement generating "Crystal Fracture Events at an exponentially
   increasing rate").
4. **The tell is thermal, at every scale.** Whatever constant is chosen, the waste
   heat is the observable, and it scales with (1 − η) × output. A practitioner near
   Starvation should be *visibly* hotter, louder and brighter per unit of work
   done, and an opponent who can read that has found the counter by reading a
   table. That is the fair-play property the whole ledger is for.

---

## 5. What is not filed as a conflict, and why

`CLAUDE.md` binds `CONFLICTS.md` to canon contradicting canon, quoted both ways.
Nothing in this note qualifies, and **no new rows were written.** The reasoning,
item by item, so a later session does not have to redo it:

- **Physics contradicting canon is not a conflict row.** §1.2, §1.4, §2.2, §2.4,
  §4.3 and §4.4 are real-world measurement against canon, not page against page.
  They belong here and in a ruling, not in the conflict register.
- **The drain flags in §3.3 depend on the brief's constant.** Gimbzo's cistern
  against his 0.72 seconds is only a contradiction once you accept that 1 AU = 1 EU,
  which no page says. Until a ruling makes that identity canon, the two lines do not
  contradict each other in text. If the ruling adopts it, **these become conflict
  rows at that moment**, and this section is the list to file from.
- **Already registered, not re-filed:** the S/SS joule gap (**C-036**), the B/A
  travel-speed gap (**C-038**), the SSS EJ-for-ZJ ceiling (**C-039**), the Strike
  Force against Stage misses (**C-040**), the measured conversion and the unordered
  reserves (**C-034**), AU/s = Flux Density × η (**C-035**), and the Class I / Tier 5
  efficiency clash (**C-037**). Everything this note found on the canon-versus-canon
  axis was already one of those seven.
- **Deliberately left as a note, not a row:** the EX row's TNT gloss, 16.512
  ronnatons where the joules give 16.506 (§2.1). A fourth-significant-figure
  discrepancy in one gloss, on a row nobody reads a Grade off, is below the
  threshold that makes `CONFLICTS.md` useful.
- **The brief's own arithmetic error** (2.4 exajoules and half a gigaton for
  2.4 petajoules and 0.574 megatons, §1.3) is in the issue text, not in canon, so
  it is corrected here and nowhere else.

**No figure on any card, page or table was changed, and no constant was chosen.**
The choice among C-034's three readings — the measured conversion with the reserves
wrong, a constant near 1 MJ with Dougou's sheet wrong, or no single constant at all
— stays exactly where Phase 1 left it: Isaac's.

---

## 6. If it is useful: where physics says the constant sits

Stated as a range with its working, not as a recommendation, and adopting nothing.
Three independent constraints, each with a direction:

| constraint | law | bound on 1 EU |
|---|---|---|
| canon's three self-pricing lines | — | 112 – 3,571 J |
| a body surviving its own η loss over a working | first law + body heat capacity | ≤ 3,592 J (Yukazuri), lower for lower η |
| Draen Varos's nine-kilogram crystal | E = mc² | ≤ 1.34 × 10⁵ J |
| Kaelzar's 3 billion EU/g | E = mc² | ≤ 3.0 × 10⁴ J |

All four brackets overlap in the range **10² to 3.6 × 10³ J/EU**, and the brief's
10⁶ J/EU lies outside all four. The AU/s axis does not follow from the EU axis and
wants its own constant; the thermal ceiling on sustained full output puts it at
**0.004 to 53 J per AU** if the waste lands in the body, and leaves it unbounded by
thermodynamics if the waste is dissipated outside it — in which case §4.5's
radiance, burn radius and sound pressure become the binding constraints instead,
and they are the interesting ones, because a player can find them.

---

## Sources

Canon, all quoted verbatim above with file and line:
`wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`
lines 16, 17, 28–40, 45–55, 60–79, 107;
`.../III. Physical Force (Part Eleven).md` line 30;
`.../VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md`
lines 83, 85, 86, 100;
`wiki/Volume I — Character Cards/` — Yukazuri Moto 57, 61, 83, 84, 85; Aurelian
Prudentius · The Primate 85; Draen Varos 37; Kaelzar 106; Anryū Ichimonji 29, 63;
Artemis Amagiri Moto 56, 58, 62; Gimbzo 58, 61, 62; Ignatius 141; Iracordas 48,
51, 52, 64; Ara Min Mahuo 71; Borin Ironheart 103; Ayame Yuno 58; Sodoku Moto 86;
Naori Yukari 28; Yoko Mishiro 69; Dougou Ozumu Zettari 58, 62, 93;
`wiki/Spellcraft/The Iron Tree.md` 20, 41;
`scenes/09_dabney_the_undamped_thing.md` 111, 117;
`scenes/14_darius_two_men_who_would_not_take_the_seat.md` 185;
`CONFLICTS.md` C-034 to C-040;
`imports/essence-ledger/anchors.json`, `fit.json` (WAR-9).

Outside sources:

1. Specific heat of the human body — Kenny & Jay et al., *Temperature* 10(2), 2023:
   the classical 3.47 kJ·kg⁻¹·°C⁻¹ was never measured; the calculated whole-body
   value is 2.98 (range 2.44–3.39). https://pmc.ncbi.nlm.nih.gov/articles/PMC10274559/
2. Maximal evaporative heat loss — sweat rates of 1.5–2.5 L/h give 1,000–1,700 W if
   fully evaporated. https://pmc.ncbi.nlm.nih.gov/articles/PMC10687011/
3. Cube-root blast scaling and the 5 psi constant — *Nuclear Weapons Frequently
   Asked Questions* §5, r = Y^0.33 × 0.71 (km, kt);
   https://nuclearweaponarchive.org/Nwfaq/Nfaq5.html — and Glasstone & Dolan,
   *The Effects of Nuclear Weapons*, ch. III, for the scaling law itself:
   https://atomicarchive.com/resources/documents/effects/glasstone-dolan/chapter3.html
4. CEM43 thermal dose — Sapareto & Dewey (1984); R = 0.5 above 43 °C, 0.25 below;
   common injury threshold CEM43 ≥ 120 min.
   https://www.sciencedirect.com/topics/engineering/cumulative-equivalent-minutes

Laws used by name, standard and uncited: conservation of energy; the second law
and the Gouy–Stodola theorem (Ẇ_lost = T₀Ṡ_gen); E = mc²; E = ½mv² and the
relativistic (γ − 1)mc²; Hopkinson–Cranz cube-root blast scaling; the Stefan–
Boltzmann law; Fourier's law of conduction; Pennes' bioheat equation (1948);
Newtonian gravitational binding energy U = 3GM²/5R; aerodynamic drag power
P = ½ρv³C_dA; Sutton–Graves stagnation-point heating; thermoelastic stress
σ = EαΔT/(1 − ν).
