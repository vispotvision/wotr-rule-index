# Part Twenty-Three — The Essence Ledger

*Fracture of Worlds — The Living System. Draft, WAR-12 (Essence Ledger Phase 2,
parent WAR-8), 2026-09-25.*

> **Status: draft, not canon.** Nothing here is published to the wiki or to
> Notion; that is Phase 4 (WAR-14). No card, page, table or figure anywhere in
> the project has been changed to make this Part come out. Where canon
> contradicts canon the Part states the equation, shows the break, and leaves
> the conflict open on Isaac's docket. Where a ruling is pending the slot is
> marked **PENDING** and the question is named in words he can answer in a
> sentence.

---

## What this Part is for, and why it did not exist

Four quantities run through every character card in the project — a reserve in
EU, a compression in EU/g, an output rate in AU/s, an efficiency η — and Part
Nineteen defines all four without ever saying what one of them is worth. The
Grade table in Part Four measures destruction in joules and tons of TNT. The
two systems have never been joined, and the cards say so out loud:

> `wiki/Summoned and Bound/Haelvorn · Housecat.md:236`
> **EU figures unverified, again.** Call cost given as 6% of reserve. **No
> Band-by-Band reserve table exists in FOW** and Mu-jin's 850,000,000 at Level
> 430 remains the only fixed anchor, so no absolute EU number appears anywhere
> in this entry.

> `wiki/Volume I — Character Cards/Ignatius Sanctus Sanctorum Arsenal · The Archpaladin.md:141`
> **I cannot source EU benchmarks by Stage** and have not restated them as
> confirmed.

> `wiki/Volume I — Character Cards/Aurelian Prudentius Custos Clausorum · The Primate.md:85`
> Fracture of Worlds specifies **no EU table by Stage**; this figure was
> extrapolated from the two attested Band V reserves in project canon …

This Part is the missing join. It states what one EU is worth in joules, what
that buys on the Grade ladder, what a reserve costs to spend and how long it
lasts, how fast it comes back, and what the reader can do about all of it from
the other side of the fight.

**How to read the markers.**

| marker | meaning |
|---|---|
| **[canon]** | quoted verbatim from a page, with file and line. Nothing in a `[canon]` block is the draft's words. |
| **[derived]** | arithmetic on `[canon]` figures. The working is shown so it can be checked. |
| **[draft]** | the Part's own statement. Needs Isaac's word before it is anything more. |
| **PENDING** | a slot a ruling must fill. Both readings are stated; the draft chooses neither and names the question. |

---

## §1 · The four quantities, and the fifth

**[canon]** `wiki/Fracture of Worlds — The Living System/VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md:83–86`

> **EU (Essence Units)** — the raw reserve. Total volume of usable Essence
> stored in the Crystal at any moment. Scales with Temperance Stage, governed
> primarily by **Tempering Yield**. Maximum EU is the structural ceiling.
> Operating below **ten percent EU** produces Essence Starvation: reduced stat
> expression, Shell degradation, Trait flickering.
>
> **Flux Density (EU/g)** — the compression ratio, how much Essence is packed
> per unit of Crystal mass. Higher means greater output from the same reserve.
> Governed by **Tempering Clarity** and **Ardency Compression**. This separates
> a practitioner who burns through their reserve in three techniques from one
> who fights for an hour on the same pool.
>
> **AU/s (Aether Units per second)** — the output rate, how much Essence
> converts into active expression per second of sustained operation. Governed
> by **Ardency Flux**, **Ardency Alacrity** and **Tempering Yield**. Formula:
> **AU/s = Flux Density × η**.
>
> **Eta (η), Efficiency** — the ratio of Essence spent to Essence that arrives
> as intended effect. At η 0.50, half of every expenditure is wasted as heat,
> noise and structural bleed. At η 0.90, ninety percent converts to clean
> output. The single most important variable in sustained combat, because it
> determines how long the reserve lasts under continuous output. Governed by
> **Aether Class**, **Tempering Clarity** and **Ardency Compression**.

The fifth quantity is the one Part Eleven already measures, and it is the one
that lets the other four be priced at all:

**[canon]** `wiki/Fracture of Worlds — The Living System/III. Physical Force (Part Eleven).md:30`

> Strike Force is the destructive energy delivered per discrete attack action,
> measured in **Newtons** for peak contact force at the moment of impact and
> **Joules** for total energy yield. Both matter. … The Continuum records both.

So the Continuum already keeps its books in joules. The Ledger is not a new
currency; it is the exchange rate between the two sets of books canon has been
keeping side by side.

**[draft] The direction of the conversion.** EU is *potential* and AU is
*actual* — what the Crystal holds against what leaves it. This is why the two
cannot be the same number even when they are the same size: one is the store,
one is the flow, and η is the loss across the boundary between them.

> **The Aristotelian reading, in-world.** The Collegium tradition that
> descends from the old faculty of Causes reads the Ledger as the doctrine of
> *potency and act*: EU is what a Crystal is able to become, AU is what it has
> become, η is the fraction of the becoming that arrives. Their term for
> Essence Starvation is *the exhausted potency*, and their objection to the
> whole Aether-Flow apparatus is that it measures the act and infers the
> potency, which they hold is backwards. **They are a school, not a
> mechanic.** The numbers below are what happens; the Causes faculty is one of
> several arguments about what the numbers mean, and Part Fifteen's Four
> Theories are the model for how such arguments are carried.

---

## §2 · The constant: what one EU is worth

### 2.1 The evidence, all of it

Canon states an EU cost and a joule output for **one and the same working**
exactly three times. All three are on Dougou Ozumu Zettari's sheet and his
Spellcraft page, and all three are collected in `fit.json` `direct_pairs`
(WAR-9). They are the whole measured evidence; everything else in the corpus
states one side or the other and must be inferred.

**[canon]** `wiki/Volume I — Character Cards/Dougou Ozumu Zettari.md:93`

> | **Ozumu no Katachi** *Form of Accumulated Crush* | 4,800 EU | **Every
> surface becomes a loaded striking point.** 1–5 MJ contact threat | Precision
> strikes into fracture-lines |

**[canon]** `wiki/Spellcraft/The Iron Tree.md:20`

> **Cost** · 2,800 to 8,900 EU per branch, drawn from Dougou's 92,000 EU
> reserve; Kokushin Gyūha costs 7,400 EU exactly per his sheet. The Sevenfold
> Seal cannot be held closed while a branch vents; the two states are mutually
> exclusive.

**[canon]** `wiki/Spellcraft/The Iron Tree.md:41`

> **Numerical Effect** · Per the Physical Benchmarks table and Dougou's own
> sheet, output at apex reaches 12,000,000 N and **8 to 20 MJ**, at the
> boundary between D-Grade and low C-Grade force; branch outputs below apex sit
> in the **1 to 10 MJ** range his sheet's individual techniques already occupy.

### 2.2 The fit, and the residual against each

**[derived]** Each line fixes a window on the constant *k* in joules per EU:
the predicted output *k* × EU must land inside the joule figure the page
states. `ledger_tables.py` §A grid-searches *k* from 10 to 10⁸ J/EU at a
thousandth of a decade and scores the miss in decades.

| working | EU | stated output | *k* window that lands it |
|---|---|---|---|
| Ozumu no Katachi | 4,800 | 1–5 MJ | 208 – 1,042 J/EU |
| Kokushin Gyūha, apex | 7,400 | 8–20 MJ | 1,081 – 2,703 J/EU |
| any branch release | 2,800 – 8,900 | 1–10 MJ | 357 – 1,124 J/EU |

The first and third windows overlap on 357–1,042. The second begins at 1,081.
**No single constant satisfies all three** — they miss each other by 0.016
decades, four percent, which is a rounding seam rather than a disagreement.
The least-squares optimum sits at **1,062 J/EU**, in the seam.

Three constants against the three lines:

| constant | in band | sum of squared residuals (decades) |
|---|---|---|
| the brief's 1 EU = 1 MJ | **0 of 3** | 21.478 |
| **1 EU = 1 kJ** | **2 of 3** | 0.0011 |
| least squares, 1,062 J/EU | 1 of 3 | 0.0001 |

Per working, at each:

| working | at 1 MJ/EU | at **1 kJ/EU** | at 1,062 J/EU |
|---|---|---|---|
| Ozumu no Katachi (1–5 MJ) | 4.8 GJ, **+2.982 dec** | 4.8 MJ, **in band** | 5.10 MJ, +0.008 dec |
| Kokushin Gyūha (8–20 MJ) | 7.4 GJ, **+2.568 dec** | 7.4 MJ, **−0.034 dec** | 7.86 MJ, −0.008 dec |
| branch release (1–10 MJ) | 2.8–8.9 GJ, **+2.447 dec** | 2.8–8.9 MJ, **in band** | 2.97–9.45 MJ, in band |

### 2.3 The constant this Part works at, and why

**[draft] 1 EU = 1 kJ of potential. Energy delivered = EU × η × 1 kJ. 1 AU/s =
1 kW.**

Isaac's brief asked for 1 EU = 1 MJ and said: *"Fit the conversion to the
attested figures and report the residuals. If 1 MJ fits badly, pick the
constant that fits best and say why."* It fits badly. The residuals are above;
the reasons it cannot be rescued are these, in order of how hard they bite.

1. **It misses canon's only self-pricing page by three decades**, on all three
   lines, in the same direction. That is C-034's first half and this Part does
   not settle it — but a constant that reproduces the only measurement is
   better placed than one that does not.

2. **It breaks E = mc² on two cards, and no Grade table fixes that.** The
   physics check (WAR-10, `physics-check.md` §1.4) works it: Draen Varos's
   Forge-Heart is **[canon]** `wiki/Volume I — Character Cards/Draen Varos · The Red Forge Sentinel.md:37`
   *"nine kilograms of Crystal and slag that reads as one structure. Flux
   Density **670 million EU/g.**"* — 6.03 × 10¹² EU. At 1 MJ/EU that is
   6.03 × 10¹⁸ J in an object whose entire rest-mass energy is 8.09 × 10¹⁷ J.
   **The contents outweigh the container, 7.5 to one.** Any constant above
   **1.34 × 10⁵ J/EU** puts him over; Kaelzar's three billion EU/g puts the
   ceiling at **3.0 × 10⁴ J/EU**. 1 kJ clears both by one and a half to two
   decades. 1 MJ clears neither.

3. **It kills the practitioner with her own waste heat before she finishes a
   sentence.** At 1 MJ/EU, Yukazuri Moto's 140 EU Nerve Reading — reading a
   man's muscle tension from fifteen feet — costs 140 MJ, and the eleven
   percent her own η discards is 15.4 MJ into a body whose whole thermal budget
   to a lethal core temperature is 1.225 MJ. She dies twelve times over
   (`physics-check.md` §1.2). At 1 kJ/EU the same working costs 140 kJ, wastes
   15.4 kJ, and warms her by **0.063 K**. That is what a serious working
   *should* cost a body.

4. **It is out by the same factor of a thousand twice.** The brief's own sanity
   check reads the Primate's 2,400,000,000 EU as "2.4 exajoules, half a
   gigaton". At 1 MJ/EU it is 2.4 **peta**joules and 0.574 **mega**tons
   (`physics-check.md` §1.3). A factor of 1,000 went astray in the brief's
   arithmetic, and a factor of 1,000 is exactly the correction the measurement
   asks for. The Ledger is the shape Isaac described; it sits three decades
   lower than he put it.

**Why 1 kJ and not 1,062 J.** 1,062 scores marginally better and is
unmemorable. 1 kJ is inside two of the three windows, misses the third by
**0.034 decades — eight percent**, which is smaller than the rounding in "8 to
20 MJ", and it lets a reader convert at the table without a calculator: *drop
three zeroes and read kilojoules; a thousand EU is a megajoule.* The brief's
own reason for 1 MJ was that it is round. This is the round number that is also
right.

**[derived] The four independent brackets, and where 1 kJ sits in them** (three
from `physics-check.md` §6, one from `fit.json` `direct_pairs`):

| constraint | law | bound on 1 EU | 1 kJ |
|---|---|---|---|
| canon's three self-pricing lines | — | 112 – 3,571 J | inside |
| a body surviving its own η loss over a whole working | first law + 245 kJ/K body heat capacity | ≤ 3,592 J | inside |
| Draen Varos's nine-kilogram crystal | E = mc² | ≤ 1.34 × 10⁵ J | inside |
| Kaelzar's three billion EU/g | E = mc² | ≤ 3.0 × 10⁴ J | inside |

All four overlap on **112 to 3.6 × 10³ J/EU**. **1 kJ is the only power of ten
inside all four** — 100 J falls just outside the measured window's floor of
112 — and the brief's 10⁶ is outside every one of them.

> **PENDING — C-034.** The conflict row is open and this Part does not close
> it. Two readings are live and the draft's constant presumes neither is
> *settled*: **(a)** the conversion is the measured one, in the hundreds to
> low thousands of joules, and the attested reserves are what is out of order;
> **(b)** there is no single constant, and each Stage carries its own (the
> per-Stage medians are in `fit.json` `by_stage`). Every table below is built
> at 1 kJ and inherits whichever way Isaac rules. **The question:** *is one EU
> worth the same number of joules at Stage III as at Stage XIV?*

### 2.4 The chain, end to end

**[derived]** EU → J → Grade → TNT → what it wrecks, with 1 t TNT ≡ 4.184 × 10⁹ J
(the thermochemical definition, so the arithmetic is exact rather than
measured):

    joules delivered = EU spent × η × 1,000
    Grade            = the Part Four row whose attack-output band holds it
    tons TNT         = joules ÷ 4.184 × 10⁹

Worked once, on the line the whole constant rests on. Dougou spends 7,400 EU on
Kokushin Gyūha at his stated η — **[canon]** `wiki/Volume I — Character Cards/Dougou Ozumu Zettari.md:38`
*"**Aether Index** · 3,900 AU/s external · **internal cycling immeasurable** ·
**η 0.99**"*:

    7,400 EU × 1,000 J/EU        = 7.40 MJ of potential
    × η 0.99                     = 7.33 MJ delivered
    Part Four: 15 kJ – 2.092×10⁷ = D-Grade, top of the band
    ÷ 4.184 × 10⁹                = 1.75 kg of TNT
    Part Four's gloss for D      : "Wall level"

**[canon]** The Iron Tree:41 grades that same working *"at the boundary between
D-Grade and low C-Grade force"*. The chain, run forwards from the EU cost,
arrives where the page that states the cost says it arrives. **That is the
whole argument for the constant in one line.**

*(The joule → TNT column of Part Four is exact on twelve rows of thirteen and
the X row's ceiling is the Moon's gravitational binding energy to 0.2%;
`physics-check.md` §2.1–2.2 has the check and the three places the "what it
wrecks" gloss silently changes criterion. Nothing in this Part reads that gloss
as a measurement.)*

---

## §3 · The spine: joules → Grade → a tier from one to nine

Every ladder WAR-13 builds — Bestiary, Drafts, artifacts, Summons, Domains,
Wellspring sites, weapons and armour — hangs on one spine, and the spine is
already in canon twice over. Part Four gives each Grade a joule band. Part Five
gives each Stage a Max Grade and a Tier of Standing. Read the Max Grade column
backwards and the thirteen Grades fall into the nine Tiers without a name being
invented.

**[canon]** `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md:28–40`, the attack-output column; and `:64–79`, the Stage gate table.

**[derived] The nine rungs.** A Grade sits at the lowest Tier of Standing whose
Stages can reach it.

| Tier | Grade(s) | first Stage that reaches it | peak output, joules | tons TNT | EU that buys the ceiling at 1 kJ |
|---|---|---|---|---|---|
| **1 · Initiate** | Hollow, F, E | I Murmuring | below 60 – 1.5 × 10⁴ | ≤ 3.6 × 10⁻⁶ | 15 EU |
| **2 · Apprentice** | D | II Welling | 1.5 × 10⁴ – 2.092 × 10⁷ | 3.6 × 10⁻⁶ – 0.005 | 20,920 EU |
| **3 · Journeyman** | C | III Ascension | 2.092 × 10⁷ – 1.046 × 10⁹ | 0.005 – 0.25 | 1.046 × 10⁶ EU |
| **4 · Adept** | B | IV Flourishing | 1.046 × 10⁹ – 4.6024 × 10¹⁰ | 0.25 – 11 | 4.602 × 10⁷ EU |
| **5 · Expert** | A | VI Glory | 4.6024 × 10¹⁰ – 4.184 × 10¹² | 11 – 1,000 | 4.184 × 10⁹ EU |
| **6 · Master** | S, SS | VIII Transcendence | 4.184 × 10¹² – 4.184 × 10¹⁴ | 1 kt – 100 kt | 4.184 × 10¹¹ EU |
| **7 · Grandmaster** | SSS | XII Emanation | 4.184 × 10¹⁴ – 4.184 × 10²¹ | 100 kt – 1 Tt | 4.184 × 10¹⁸ EU |
| **8 · Archmaster** | X, EX | XIII Principality | 4.184 × 10²¹ – 6.906 × 10³⁷ | 1 Tt – 16.5 Rt | 6.906 × 10³⁴ EU |
| **9 · Paragon** | EX+ | XV Revelation | 6.906 × 10³⁷ and above | 16.5 Rt and above | no ceiling |

**[draft] How to use it.** Take the thing's *peak output in joules* — a beast's
hardest blow, a draught's released energy, an artifact's discharge, a summon's
call cost read through η, a Domain's held energy. Find the row. That row's
number is the thing's tier on every ladder. **Each ladder then adds its own
modifiers** — a beast that is hard to kill rather than hard to be hit by, a
draught that works slowly, an artifact that only fires once — and those
modifiers are WAR-13's business, not this Part's. **The tier names for each
register (Hearth-pest to Sky-eater, Tincture to Stone, Trinket to Covenant)
belong to WAR-13 and are deliberately absent here.**

Two holes in the spine, both already filed, both inherited rather than created:

- **C-036**, the gap between S's ceiling (2.42672 × 10¹³ J) and SS's floor
  (4.184 × 10¹³ J). A figure of 30 TJ sits in Tier 6 but in no Grade. The
  ladder above reads Tier 6 across the whole S-to-SS range because it takes the
  Tier's outer edges, which is a reading and not a repair.
- **C-039**, four Technique pages and Ignatius's card writing the SSS ceiling as
  4.184 EJ where all three ladders write 4.184 ZJ. Anything priced against "the
  SSS ceiling" is priced two ways, a thousandfold apart.

---

## §4 · Reserve bands by Stage and by Tier of Standing

This is the table the cards say does not exist. It turns out the method for
building it was ruled almost two weeks ago and then used exactly once.

### 4.1 The method is already ruled

**[canon]** `wiki/Summoned and Bound/Obrenkael · The Mule.md:215`

> **EU figures ruled.** … Ruled 2026-09-12: Kwon Hae-ryu's EU Reserve is
> 90,000,000 EU, at Level 355, Stage X Realization, Band IV … The figure is a
> **log-linear interpolation on Level** between the project's fixed anchors,
> Ara Min at Level 250, roughly 4,200,000, and Borin Ironheart at Level 378,
> 180,000,000 estimated, and the Borin-to-Mu-jin slope, 850,000,000 at Level
> 430, confirms it. `Fracture_of_Worlds.pdf` establishes that EU scales with
> Temperance Stage and is governed by Tempering Yield and gives no Band-by-Band
> reserve table, **so the interpolation is the method and not a source.**

The ruling names the method, the three anchors and the axis. It is on **Level**,
not on Stage. Fit it and it is startlingly regular:

**[derived]** Between Ara Min (L250, 4.2 × 10⁶) and Borin (L378, 1.8 × 10⁸) the
slope is **0.012750 decades per Level**. Between Borin and Kwon Mu-jin (L430,
8.5 × 10⁸) it is **0.012964**. The two segments agree to 1.7 percent. Across
the whole span:

    log₁₀ EU = 3.4202 + 0.012812 × Level

    — a reserve multiplies by ten every 78.1 Levels,
      and by about 26 across each hundred-Level Band.

> **The Pythagorean reading, in-world.** The Measurewrights' old Harmonic
> faculty never accepted the Level axis and reads the same regularity as a
> ratio: each Band multiplies the reserve by a fixed interval, so the five
> Bands are five octaves of one string and the Crystal is a monochord being
> stopped shorter. They tune reserve gauges to intervals rather than to
> numbers and they are, in practice, no worse at it. **A school, not a
> mechanic** — the gauge reads what the arithmetic above says it reads, and
> the Harmonic faculty's error is in what they think it proves.

### 4.2 The law against every anchor that states a Level

**[derived]** Nineteen of the thirty-one attested reserves sit on a page that
also states a Level. Against the ruled law:

| Level | Stage | entity | stated EU | law | residual |
|---|---|---|---|---|---|
| 80 | III | Naori Yukari | 42,000 | 27,870 | **+0.178** |
| 128 | VII | Mizuki Moto | 470,000 | 114,900 | +0.612 |
| 145 | V | Yoko Mishiro | 185,000 | 189,700 | **−0.011** |
| 156 | V | Karo Venrik | 1,600 | 262,400 | −2.215 |
| 180 | VII | Anryū Ichimonji | 820,000 | 532,600 | **+0.187** |
| 182 | VI | Rashani Zettari | 540,000 | 565,000 | **−0.020** |
| 195 | VII | Niran Yukari | 485,000 | 829,100 | **−0.233** |
| 250 | VIII | Ara Min Mahuo | 4,200,000 | 4,200,000 | **0.000** *(anchor)* |
| 250 | VII | Rengai Zettari | 1,400,000 | 4,200,000 | **−0.477** |
| 320 | VI | Sodoku Moto | 1,340,000 | 33,120,000 | −1.393 |
| 355 | X | Kwon Hae-ryu | 90,000,000 | 93,010,000 | **−0.014** *(ruled by this method)* |
| 378 | XII | Borin Ironheart | 180,000,000 | 183,300,000 | **−0.008** *(anchor)* |
| 380 | VIII | Krothar Veylshroud, suppressed | 1,600,000 | 194,500,000 | −2.085 |
| 380 | VIII | Krothar Veylshroud, unsuppressed | 2,800,000 | 194,500,000 | −1.842 |
| 385 | XII | Ignatius / Darius | 5,500,000 | 225,400,000 | −1.613 |
| 430 | XII | Kwon Mu-jin | 850,000,000 | 850,000,000 | **0.000** *(anchor)* |
| 462 | XII | Verinus VII | 620,000,000 | 2,185,000,000 | **−0.547** |
| 500 | XII | The Arctic Lion (Level 500) | 4,200,000 | 6,703,000,000 | −3.203 |
| 500 | XIV | The Primate | 2,400,000,000 | 6,703,000,000 | **−0.446** |

**Eleven of nineteen inside half a decade; thirteen inside one.** Three of the
six misses are on cards that flag their own figures:

**[canon]** `wiki/Volume I — Character Cards/Karo Venrik · The Foolish Magus.md:137`
> **Essence Capacity 1,600 EU and Flux Density 3.2 × 10² EU/g** carry across
> from the legacy sheet. **I have not been able to source EU benchmarks by
> Stage** and cannot confirm these are in range. Flagged rather than restated.

Ignatius's card says the same thing in the same words (`:141`, quoted at the
head of this Part). The third is the Arctic Lion, which is a Level 500
configuration of a Stage VI character carrying his base sheet's reserve.
Krothar's two figures are a suppressed and an unsuppressed reading of a
practitioner whose chains hold him below his own output. **Sodoku's miss has a
different cause and it is §4.5.**

### 4.3 The bands

**[derived]** Two things bind a Stage's reserve, and they are different in kind.

**The gate ceiling — hard.** Part One sets four gates and states them as
absolutes:

**[canon]** `wiki/Fracture of Worlds — The Living System/I. Levels, Experience and Stat Points (Parts One–Three).md:18`

> **No character can breach a Band ceiling without first passing the Temperance
> Threshold that cluster demands.** The System will simply halt the level
> counter and build pressure, called Residual Strain, until the Threshold is
> passed or the character fractures under the weight.

**[canon]** `:22–25` — *"**Gate:** Stage IV before Level 100 can be
surpassed"*, *"**Gate:** Stage VII before Level 200"*, *"**Gate:** Stage X
before Level 300"*, *"**Gate:** Stage XII before Level 400"*.

Read as their contrapositive: a Stage III practitioner cannot be above Level
100, a Stage VI cannot be above 200, a Stage IX cannot be above 300, a Stage XI
cannot be above 400. Through the ruled law that is a **hard ceiling on the
reserve**.

**The cluster band — typical.** The same four paragraphs give each Band a
*"Temperance cluster"*: Band I (Levels 1–100) is Stages I–IV, Band II
(101–200) Stages V–VII, Band III (201–300) VIII–X, Band IV (301–400) XI–XII,
Band V (401–500) XIII–XIV. That is where a Stage's practitioners usually sit,
not where they must. It gives the working range.

| Tier | Stage | cluster Levels | **working band, EU** | gate Level | **ceiling, EU** |
|---|---|---|---|---|---|
| 1 · Initiate | I Murmuring | 1–100 | 2,710 – 50,300 | 100 | **50,300** |
| 2 · Apprentice | II Welling | 1–100 | 2,710 – 50,300 | 100 | **50,300** |
| 3 · Journeyman | III Ascension | 1–100 | 2,710 – 50,300 | 100 | **50,300** |
| 4 · Adept | IV Flourishing | 1–100 | 2,710 – 50,300 | 200 | **961,000** |
| 5 · Expert | V Splintering | 101–200 | 51,800 – 961,000 | 200 | **961,000** |
| 5 · Expert | VI Glory | 101–200 | 51,800 – 961,000 | 200 | **961,000** |
| 5 · Expert | VII Refraction | 101–200 | 51,800 – 961,000 | 300 | **1.84 × 10⁷** |
| 6 · Master | VIII Transcendence | 201–300 | 9.90 × 10⁵ – 1.84 × 10⁷ | 300 | **1.84 × 10⁷** |
| 6 · Master | IX Invocation | 201–300 | 9.90 × 10⁵ – 1.84 × 10⁷ | 300 | **1.84 × 10⁷** |
| 6 · Master | X Realization | 201–300 | 9.90 × 10⁵ – 1.84 × 10⁷ | 400 | **3.51 × 10⁸** |
| 7 · Grandmaster | XI Dissonance | 301–400 | 1.89 × 10⁷ – 3.51 × 10⁸ | 400 | **3.51 × 10⁸** |
| 7 · Grandmaster | XII Emanation | 301–400 | 1.89 × 10⁷ – 3.51 × 10⁸ | 500 | **6.70 × 10⁹** |
| 8 · Archmaster | XIII Principality | 401–500 | 3.61 × 10⁸ – 6.70 × 10⁹ | 500 | **6.70 × 10⁹** |
| 8 · Archmaster | XIV Zenith | 401–500 | 3.61 × 10⁸ – 6.70 × 10⁹ | none | **6.70 × 10⁹** |
| 9 · Paragon | XV Revelation | — | **PENDING** | none | **PENDING** |
| 9 · Paragon | XVI Apex | — | **PENDING** | none | **PENDING** |

Rolled up to the nine Tiers of Standing, with the attested set beside it:

| Tier | Stages | working band, EU | ceiling, EU | anchors | attested range | under the ceiling |
|---|---|---|---|---|---|---|
| 1 · Initiate | I | 2,710 – 50,300 | 50,300 | 0 | — | — |
| 2 · Apprentice | II | 2,710 – 50,300 | 50,300 | 0 | — | — |
| 3 · Journeyman | III | 2,710 – 50,300 | 50,300 | 1 | 42,000 | **1 / 1** |
| 4 · Adept | IV | 2,710 – 50,300 | 961,000 | 1 | 3,100 | **1 / 1** |
| 5 · Expert | V–VII | 51,800 – 1.84 × 10⁷ | 1.84 × 10⁷ | 9 | 1,600 – 1.4 × 10⁶ | **9 / 9** |
| 6 · Master | VIII–X | 9.90 × 10⁵ – 3.51 × 10⁸ | 3.51 × 10⁸ | 11 | 9,400 – 9.0 × 10⁷ | **11 / 11** |
| 7 · Grandmaster | XI–XII | 1.89 × 10⁷ – 6.70 × 10⁹ | 6.70 × 10⁹ | 7 | 74,000 – 4.8 × 10¹⁴ | 6 / 7 |
| 8 · Archmaster | XIII–XIV | 3.61 × 10⁸ – 6.70 × 10⁹ | 6.70 × 10⁹ | 2 | 92,000 – 2.4 × 10⁹ | **2 / 2** |
| 9 · Paragon | XV–XVI | **PENDING** | **PENDING** | 0 | — | — |

**Twenty-nine of the thirty-one attested reserves sit under the ceiling their
Stage gives. Twenty-two of thirty-one sit within one decade of the working
band.** Two go over, and both are named in §4.5.

### 4.4 Where each attested character sits

**[derived]** Every anchor from `fit.json` `reserves`, against its Stage's
working band.

| Stage | Tier | entity | EU | verdict |
|---|---|---|---|---|
| III | 3 | Naori Yukari | 42,000 | **in the band** |
| IV | 4 | Yukazuri Moto | 3,100 | **in the band** |
| V | 5 | Karo Venrik | 1,600 | −1.51 dec under *(card flags its own figures)* |
| V | 5 | Yoko Mishiro | 185,000 | **in the band** |
| VI | 5 | Naiser Yukari | 2,460 | −1.32 dec under |
| VI | 5 | Rashani Zettari | 540,000 | **in the band** |
| VI | 5 | Sodoku Moto | 1,340,000 | **over the gate ceiling by 0.14 dec** → §4.5 |
| VII | 5 | Mizuki Moto | 470,000 | **in the band** |
| VII | 5 | Niran Yukari | 485,000 | **in the band** |
| VII | 5 | Anryū Ichimonji | 820,000 | **in the band** |
| VII | 5 | Rengai Zettari | 1,400,000 | +0.16 dec over the cluster, under the gate |
| VIII | 6 | Ayame Yuno | 37,000 | −1.43 dec under |
| VIII | 6 | Artemis Amagiri Moto | 41,800 | −1.37 dec under |
| VIII | 6 | Krothar Veylshroud, suppressed | 1,600,000 | **in the band** |
| VIII | 6 | Krothar Veylshroud, unsuppressed | 2,800,000 | **in the band** |
| VIII | 6 | Lucius Xenotro | 2,850,000 | **in the band** |
| VIII | 6 | Ara Min Mahuo | 4,200,000 | **in the band** *(anchor)* |
| IX | 6 | Naevra Yukari | 185,000 | −0.73 dec under |
| X | 6 | Vethraun Ashmaw | 9,400 | −2.02 dec under |
| X | 6 | Iracordas | 16,800 | −1.77 dec under |
| X | 6 | Muken Moto | 1,850,000 | **in the band** |
| X | 6 | Kwon Hae-ryu | 90,000,000 | +0.69 dec over the cluster, under the gate *(ruled)* |
| XII | 7 | Yorime Seikai | 74,000 | −2.41 dec under |
| XII | 7 | The Arctic Lion (Level 500) | 4,200,000 | −0.65 dec under |
| XII | 7 | Ignatius / Darius | 5,500,000 | −0.54 dec under *(card flags its own figures)* |
| XII | 7 | Borin Ironheart | 180,000,000 | **in the band** *(anchor)* |
| XII | 7 | Verinus VII | 620,000,000 | +0.25 dec over the cluster, under the gate |
| XII | 7 | Kwon Mu-jin | 850,000,000 | +0.38 dec over the cluster, under the gate *(anchor)* |
| XII | 7 | Gimbzo | 4.8 × 10¹⁴ | **over the gate ceiling by 4.85 dec** → §4.5 |
| XIII | 8 | Dougou Ozumu Zettari | 92,000 | −3.59 dec under |
| XIV | 8 | The Primate | 2,400,000,000 | **in the band** |

The shape of the misses is worth saying plainly, because it is what a reader of
the cards needs to know: **the band's ceiling holds almost everywhere, and its
floor does not hold at all.** Twelve anchors sit below their Stage's working
band, seven of them by more than a decade, and there is no sign that is an
error — Yorime Seikai's card states the reason on the same line:

**[canon]** `wiki/Volume I — Character Cards/Yorime Seikai.md:59`
> | **Essence Capacity** | **74,000 EU** — vast but carefully rationed. ***She
> does not spend freely because every Claim invites hunger*** |

**[draft]** A small reserve at a high Stage is a character, not a mistake. What
the Stage guarantees is the ceiling; what the practitioner has done with the
room under it is theirs. A Stage XIII practitioner with 92,000 EU is not
mis-statted — he is a man who built a very precise instrument instead of a very
large one, and Dougou's sheet is exactly that.

> **PENDING — C-034, second half.** Part Nineteen says the reserve *"Scales
> with Temperance Stage"*; the ruled method interpolates on **Level**. Both
> are live text and the draft reconciles neither. **The question:** *does
> "scales with Temperance Stage" set the reserve, or set a ceiling on it
> through the Band gates?* On the first reading the table above is wrong and
> the reserves are wrong with it; on the second the table above is right and
> the floor is simply not a rule. Everything in §4.3 is built on the second
> reading and falls with it.

### 4.5 The two that go over the ceiling

Both are canon against canon, both are new, and neither is settled here.

**Sodoku Moto, Level 320 at Stage VI.** Stage VI cannot pass Level 200 without
the Stage VII Threshold, and Level 320 is two gates past that. His card flags
the anomaly in-world rather than hiding it:

**[canon]** `wiki/Volume I — Character Cards/Sodoku Moto.md:36`
> | **Level** | **320 / 500** · Band IV — Mythic (301–400). *Flag: normally
> clusters Stage XI–XII. **He is genuinely Stage VI*** |

**Krothar Veylshroud, Level 380 at Stage VIII.** Stage VIII cannot pass Level
300 without the Stage X Threshold.

**[canon]** `wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md:32–33`
> **Level:** 380 / 500 · **Band:** IV — Warlord (approaching Band V threshold)
> **Temperance Stage:** VIII — Transcendence

Filed as **C-041**. The draft's tables read the gates as written and count both
characters as over the ceiling, which is a reading of the gate rule and not a
claim about either card.

**Gimbzo, 4.8 × 10¹⁴ EU at Stage XII** — 4.85 decades over any Level the gates
allow, and 6.14 over the working band. This is inside C-034 already (his is the
figure that makes Stage XII span 9.8 orders of magnitude on its own) and is not
re-filed. At 1 kJ his reserve is 480 petajoules; his own card calls it a
cistern.

---

## §5 · AU/s as power: how long the output holds

### 5.1 The drain, and the one thing it does not depend on

**[canon]** FoW VII:85 makes AU/s a *rate*: *"how much Essence converts into
active expression per second of sustained operation."* **[canon]** FoW VII:86
says what that rate is for: *"The single most important variable in sustained
combat, because it determines how long the reserve lasts under continuous
output."*

**[draft]** One AU is one EU crossing the boundary. At 1 EU = 1 kJ that makes
1 AU/s = 1 kW, and the time to empty is:

    t_empty       = EU reserve ÷ (AU/s)                 seconds
    t_starvation  = 0.9 × EU reserve ÷ (AU/s)           seconds, to the ten-percent floor
    power drawn   = AU/s × 1 kW
    power delivered = AU/s × η × 1 kW
    waste heat    = (1 − η) × AU/s × 1 kW

**The factor cancels in the first two lines and does not cancel in the last
three.** Every drain time below is a property of the two figures on the card
and of the decision to make one AU one EU; it would be the same at 1 MJ. The
*waste* scales with the constant directly, and that is what the brief's
constant destroyed and this one restores.

### 5.2 Worked, at three scales

**Small — Yukazuri Moto, Stage IV, Tier 4 Adept.**
**[canon]** `wiki/Volume I — Character Cards/Yukazuri Moto.md:61` *"**EU
Reserve** · 3,100 EU · **Flux Density** 290 EU/g · **Output** 480 AU/s · **η**
0.89"*

    reserve        3,100 EU × 1 kJ            = 3.10 MJ potential, 2.76 MJ deliverable
    full output    480 AU/s × 1 kW            = 480 kW drawn, 427 kW delivered
    t_empty        3,100 ÷ 480                = 6.46 s
    t_starvation   0.9 × 6.46                 = 5.81 s
    waste          0.11 × 480 kW              = 52.8 kW
    net of the ~2 kW a body sheds             = 50.8 kW → 0.207 K/s
    +5 K (lethal core rise)                   = 24.1 s

**She runs dry four times before she cooks.** The reserve is the binding clock
and Starvation is the real risk. Her three named workings, priced:

| working | EU | potential | delivered at η 0.89 | Grade | fraction of reserve |
|---|---|---|---|---|---|
| Nerve Reading (`:83`) | 140 | 140 kJ | 125 kJ | D | 4.5% |
| Coagulatio Seal (`:84`) | 260 | 260 kJ | 231 kJ | D | 8.4% |
| Somnalis Drift (`:85`) | 390 | 390 kJ | 347 kJ | D | 12.6% |

Seven full Somnalis Drifts and she is in Starvation (0.9 × 3,100 ÷ 390 = 7.15).
Nineteen Nerve Readings. That is a scene's worth of decisions, and it is the
number a player at her side of the table needs.

**Middle — Dougou Ozumu Zettari, Stage XIII, Tier 8 Archmaster.** The one sheet
in the corpus that prices itself, and therefore the calibration.
**[canon]** `:38` *"3,900 AU/s external … **η 0.99**"*; The Iron Tree:20,
92,000 EU reserve.

    reserve        92,000 EU × 1 kJ           = 92.0 MJ potential, 91.1 MJ deliverable
    full output    3,900 AU/s × 1 kW          = 3.90 MW drawn, 3.86 MW delivered
    t_empty        92,000 ÷ 3,900             = 23.6 s
    t_starvation                              = 21.2 s
    waste          0.01 × 3.90 MW             = 39.0 kW
    net of ~2 kW                              = 37.0 kW → 0.151 K/s
    +5 K                                      = 33.1 s

    apex strike    7,400 EU                   = 7.33 MJ delivered, D-Grade top
    strikes held   92,000 ÷ 7,400             = 12.4 from full, 11.2 before Starvation

**His two clocks are within a factor of 1.6 of each other** — 21 seconds of
reserve against 33 seconds of heat. That is the whole mechanic working: η
matters, the reserve matters, and a fight is decided by which one you spend
first. Twelve apex strikes from a full reserve is a fightable number, and it is
the only one in the corpus that comes out of canon's own arithmetic rather than
out of a choice.

**Large — Kwon Mu-jin, Stage XII, Tier 7 Grandmaster.**
**[canon]** `wiki/Volume I — Character Cards/Kwon Mu-jin.md:73` *"**Flux
Density** 1,800,000 EU/g · **AU/s** **1,566,000** · **η** 0.87"*, reserve
850,000,000 EU.

    reserve        8.5 × 10⁸ EU × 1 kJ        = 850 GJ potential, 740 GJ deliverable
    full output    1,566,000 AU/s × 1 kW      = 1.57 GW drawn, 1.36 GW delivered
    t_empty        8.5 × 10⁸ ÷ 1,566,000      = 542.8 s   (9 min 2 s)
    t_starvation                              = 488.5 s   (8 min 8 s)
    waste          0.13 × 1.57 GW             = 204 MW

Two hundred megawatts cannot be shed by a body — **[derived]** it is a hundred
thousand times what a man can lose, and it is the reason §6.3 exists. What can
be shed is the *reserve*: nine minutes at full draw. Against his own summons:

**[canon]** `wiki/The Disciplines/The Open Crucible — Kwon Mu-jin's Book of Summons.md:30`
> | **Cost** | 5–15% of his 850,000,000 EU reserve per construct, roughly 42.5
> to 127.5 million EU |

**[derived]** 42.5–127.5 GJ potential, 37–111 GJ delivered — **A-Grade, Tier 5
Expert** on the spine in §3, three rungs below his own Tier. And: **six
constructs at the dear end, eighteen at the cheap end, before Starvation.** A
summoner who calls six heavy constructs has spent his afternoon.

### 5.3 The whole attested set

**[derived]** `ledger_tables.py` §E, every anchor that states a reserve and an
AU/s, sorted by how long the reserve holds at full draw. Times to Starvation
are at 90% of reserve spent. Waste and the heat clock are at 1 AU/s = 1 kW,
against 245 kJ/K body heat capacity, a +5 K lethal rise and the ~2 kW a body
can shed (`physics-check.md`, Method).

| t to empty | to Starvation | entity | EU | AU/s | η | waste | +5 K in |
|---|---|---|---|---|---|---|---|
| 0.72 s | 0.65 s | Gimbzo | 4.8 × 10¹⁴ | 6.7 × 10¹⁴ | 0.94 | 4.0 × 10¹⁶ W | 30 ps |
| 1.08 s | 0.97 s | Ignatius / Darius | 5,500,000 | 5,100,000 | 0.90 | 510 MW | 2.4 ms |
| 3.23 s | 2.91 s | Iracordas | 16,800 | 5,200 | 0.93 | 364 kW | 3.4 s |
| 5.50 s | 4.95 s | Artemis Amagiri Moto | 41,800 | 7,600 | 0.84 | 1.22 MW | 1.0 s |
| 6.46 s | 5.81 s | Yukazuri Moto | 3,100 | 480 | 0.89 | 52.8 kW | 24.1 s |
| 6.67 s | 6.00 s | Krothar Veylshroud | 2,800,000 | 420,000 | 0.81 | 79.8 MW | 15 ms |
| 7.24 s | 6.51 s | Naiser Yukari | 2,460 | 340 | 0.55 † | 153 kW | 8.1 s |
| 10.00 s | 9.00 s | Naevra Yukari | 185,000 | 18,500 | 0.96 | 740 kW | 1.7 s |
| 10.00 s | 9.00 s | Naori Yukari | 42,000 | 4,200 | 0.40 | 2.52 MW | 0.49 s |
| 12.05 s | 10.85 s | Vethraun Ashmaw | 9,400 | 780 | 0.91 | 70.2 kW | 18.0 s |
| 12.63 s | 11.37 s | Niran Yukari | 485,000 | 38,400 | 0.89 | 4.22 MW | 0.29 s |
| 15.77 s | 14.19 s | Anryū Ichimonji | 820,000 | 52,000 | 1.05 | none — see §6.5 | never |
| 18.08 s | 16.27 s | Mizuki Moto | 470,000 | 26,000 | 0.82 | 4.68 MW | 0.26 s |
| 19.47 s | 17.53 s | Ayame Yuno | 37,000 | 1,900 | 0.86 | 266 kW | 4.6 s |
| 20.59 s | 18.53 s | Rengai Zettari | 1,400,000 | 68,000 | 0.78 | 15.0 MW | 0.08 s |
| 22.50 s | 20.25 s | Rashani Zettari | 540,000 | 24,000 | 0.81 | 4.56 MW | 0.27 s |
| 23.59 s | 21.23 s | Dougou Ozumu Zettari | 92,000 | 3,900 | 0.99 | 39.0 kW | 33.1 s |
| 24.15 s | 21.74 s | Lucius Xenotro | 2,850,000 | 118,000 | 0.92 | 9.44 MW | 0.13 s |
| 25.69 s | 23.13 s | Muken Moto | 1,850,000 | 72,000 | 0.84 | 11.5 MW | 0.11 s |
| 25.96 s | 23.37 s | Yorime Seikai | 74,000 | 2,850 | 0.94 | 171 kW | 7.3 s |
| 70.59 s | 63.53 s | Ara Min Mahuo | 4,200,000 | 59,500 | 0.70 | 17.9 MW | 0.07 s |
| 5 min 36 s | 5 min 2 s | The Arctic Lion (Level 500) | 4,200,000 | 12,500 | 0.91 | 1.12 MW | 1.1 s |
| 5 min 52 s | 5 min 17 s | Sodoku Moto | 1,340,000 | 3,800 | 0.84 | 608 kW | 2.0 s |
| 9 min 2 s | 8 min 8 s | Kwon Mu-jin | 850,000,000 | 1,566,000 | 0.87 | 204 MW | 6 ms |
| 41 min 6 s | 37 min 0 s | Yoko Mishiro | 185,000 | 75 | 0.50 | 37.5 kW | 34.5 s |
| 15 h 37 m 30 s | 14 h 3 m 45 s | Borin Ironheart | 180,000,000 | 3,200 | 0.91 | 288 kW | 4.3 s |

*† Naiser Yukari's card states no η and Part Nineteen's Tier 5 midpoint stands
in; every other η in this table is the figure that character's own card states,
and `ledger_tables.json` `drain[].eta_from` carries the file and line for each.
(Two reserves are quoted from a Spellcraft or Disciplines page rather than a
card — Dougou's from The Iron Tree, Kwon Mu-jin's from The Open Crucible — and
for those two `fit.json` had fallen back to a Tier midpoint because the page
carrying the reserve states no η. The card wins here.)*

**[derived] What the column says about the cards.** Five sheets describe a
practitioner their own two numbers cannot be:

- **Gimbzo, 0.72 s.** `wiki/Volume I — Character Cards/Gimbzo.md:58`:
  *"He does not burn essence, he stores it, like a cistern. **Endurance fights
  favour him absolutely**"*.
- **Artemis Amagiri Moto, 5.5 s.** `wiki/Volume I — Character Cards/Artemis Amagiri Moto.md:56`:
  *"**Deep reserve** for **sustained interception, anti-charge fields and
  repeated lane denial**"*.
- **Iracordas, 3.2 s.** `wiki/Volume I — Character Cards/Iracordas.md:64`:
  *"prolonged exposure to his aura destabilises discipline"*.
- **Ayame Yuno, 19.5 s.** `wiki/Volume I — Character Cards/Ayame Yuno.md:58`:
  *"Optimised for **sustained rites, mass-oath work and battlefield-scale
  blessings**"*.
- **Ignatius / Darius, 1.08 s**, against scenes that hold a working for four
  seconds (`physics-check.md` §3.3). His card flags its own figures.

One agrees, and it is the only one: **Borin Ironheart, 15 h 37 m**, against
`wiki/Volume I — Character Cards/Borin Ironheart · The Master of the Soul Forge.md:103`:
*"high sustained throughput, optimized for **multi-hour forge operations**"*.
His two numbers and his prose describe the same person.

**These are not filed as conflicts and must not be.** They contradict only once
1 AU = 1 EU is canon, and no page says that. **They become C-rows the moment a
ruling adopts the identity**, and §3.3 of `physics-check.md` is the list to
file from.

> **PENDING.** **The question:** *is one AU one EU — that is, does a second at
> full AU/s cost exactly AU/s worth of EU?* If yes, the table above is the
> Ledger and five cards need their durations reconciled. If no, the two axes
> take separate constants and every row scales by the ratio.

### 5.4 What AU/s is not

**[draft]** AU/s is a **ceiling on the rate**, not a duty cycle. Nothing on any
page says a practitioner runs at their stated AU/s continuously, and every card
above that describes sustained work describes it at a fraction. A working that
costs 390 EU and lasts eight seconds draws 49 AU/s, not 480. **[canon]**
Yukazuri `:85`: *"**Somnalis Drift** · 390 EU — Full-broadcast 25 ft
sympathetic suppression, **eight-second duration**"* — 390 ÷ 8 = 48.75 AU/s,
one tenth of her ceiling. The ceiling is what she can do for a heartbeat; the
tenth is what she does for eight seconds. **Read a card's AU/s as the number
that caps a burst, and read a working's EU ÷ duration as the number that runs a
scene.**

---

## §6 · Flux Density and η

### 6.1 The equation, as canon states it

**[canon]** FoW VII:85, and the same identity twice more at
`wiki/The Magic System/The Core Vocabulary.md:90` and
`wiki/The Magic System/Tier Grade, Bands & the Aether Shell.md:195`:

> Formula: **AU/s = Flux Density × η**.

### 6.2 It is short one mass, and the cards measure the missing one

**[derived] The dimensions do not close.** AU/s is Essence per *second*. Flux
Density is Essence per *gram*. η is a ratio and carries no units. So the right
side of the identity is EU/g and the left is EU/s, and no arrangement of the
two makes them the same quantity. **Something with the dimensions of grams per
second is missing from the written form.**

Solve for it. Writing AU/s = Flux Density × η × *m*, the twenty-nine cards that
state all three figures each imply a value of *m*:

| implied *m* | cards |
|---|---|
| exactly 1 g | Ara Min Mahuo, Kwon Mu-jin, Yoko Mishiro — **the three the formula already holds for** |
| 0.2 – 10 g | 21 of 29, including Dougou 0.21, Borin 0.32, Iracordas 0.59, Ignatius 1.05, Yukazuri 1.86, Niran 2.35, Lucius 3.13, Mizuki 4.01, Artemis 4.57, Muken 4.61, Sodoku 4.92, Anryū 5.27, Naevra 6.65 |
| 0.008 – 0.013 g | the seven "million EU/g" sheets — Serai Linthra, Garron Vuldane, Elion Drevas, Kael Serradyn, Valthren Odrin, Mavra Cindrel |
| 0.00024 g | Draen Varos |
| 7.7 × 10⁷ g | Gimbzo |

**Twenty-one of twenty-nine imply a mass between a fifth of a gram and ten
grams,** and the three the identity already fits imply exactly one gram — which
is what you would expect if the formula was written with a unit gram silently
taken as read. That is a real regularity and it is worth Isaac's attention.

**And it fails on the one card that states a mass.** Draen Varos's Forge-Heart
is **[canon]** *"nine kilograms of Crystal and slag that reads as one
structure"* (`:37`). His implied *m* is 0.00024 g — thirty-seven million times
smaller. **The mass reading is not the whole Crystal.** It could be a working
aperture, a coupled fraction, or nothing at all; the draft asserts none of them.

> **PENDING — C-035.** The conflict row is open: the identity is stated three
> times and fails on twenty-six of twenty-nine cards, and no card states an
> exception. **The question this Part adds, and it is a smaller one:** *does
> AU/s = Flux Density × η carry an implicit mass, and if so, whose — the whole
> Crystal (Draen Varos's nine kilograms), or a working aperture much smaller
> than it?* A ruling on the mass would settle twenty-one of the twenty-six
> misses at once and leave the seven high-Flux sheets and Gimbzo to C-035
> proper. **The Part does not bend to fit any card; the equation above is FoW
> VII:85 as written, and the residual column is what the cards do with it.**

### 6.3 Where the waste goes, and why it cannot go through the body

**[canon]** FoW VII:86 names the channels: *"wasted as **heat, noise and
structural bleed**"*. That list is correct physics. The first law says the
missing fraction cannot vanish; the second says it cannot come back as work;
Gouy–Stodola (Ẇ_lost = T₀ · Ṡ_gen) says it reappears as low-grade heat at the
place the irreversibility happened. Light and sound are ways out of that place,
not alternatives to it, and each thermalises where it is absorbed.

**[derived] It cannot be generated inside the body and conducted out.**
Fourier's law, q = −k∇T. Yukazuri's 52.8 kW through 1.8 m² of skin is
29.3 kW/m²; across 3 mm of skin at k ≈ 0.4 W·m⁻¹·K⁻¹ that needs

    ΔT = qL/k = 2.93 × 10⁴ × 0.003 / 0.4 = 220 K

across three millimetres — and she is the *smallest* output in the set. At
Dougou's 39 kW it is 163 K; at Kwon Mu-jin's 204 MW it is 8.5 × 10⁵ K. Skin
chars at about 200 °C.

**[draft] So the Soul Crystal is not a battery in the chest — it is an
aperture, and the dissipation happens at or outside the body's surface.** This
is not a choice; it is what Fourier's law and two figures off a card require,
and canon's own wording already says it, on the one card that talks about the
channels:

**[canon]** `wiki/Volume I — Character Cards/Anryū Ichimonji.md:29`
> | **Efficiency (η)** | **1.05** — near-zero waste. ***No field pressure, aura
> warmth, or harmonic noise leaks outward*** |

The line is written as a *distinction* — his does not leak outward, which says
everyone else's does.

### 6.4 The tell, priced

**[derived]** If the waste leaves the Shell, Stefan–Boltzmann prices what it
looks like. T = (P / εσA)^¼ over 1.8 m² at ε = 0.98:

| practitioner | waste | surface T | pain on bare skin (2 kW/m²) | wood ignites, piloted (12.5 kW/m²) |
|---|---|---|---|---|
| Yukazuri Moto | 52.8 kW | 852 K | 1.45 m | 0.58 m |
| Dougou Ozumu Zettari | 39.0 kW | 790 K | 1.25 m | 0.50 m |
| Naori Yukari | 2.52 MW | 2,240 K | 10.0 m | 4.0 m |
| Ara Min Mahuo | 17.9 MW | 3,658 K | 26.7 m | 10.7 m |
| Kwon Mu-jin | 204 MW | 6,717 K | 90.0 m | 36.0 m |

*Radius r = √(P / 4π · threshold).* At 852 K Yukazuri glows a dull cherry red
and is painful to stand beside. At 2,240 K Naori is above the melting point of
steel. At 6,717 K Kwon Mu-jin is **hotter than the surface of the Sun** and
sets timber alight at thirty-six metres, **including his own side's.**

**[draft] This is the tell, and it is also the cost.** A practitioner at full
output is a lamp, a furnace and a hazard to everyone within a stated radius,
and the radius is on this table. A low-η practitioner is brighter for the same
work. A high-η one is nearly dark — which is why Anryū's card bothers to say
his does not leak, and why a reader who notices a man working in silence and in
the cold should be more frightened, not less.

### 6.5 η above one

**[canon]** FoW VII:100 — *"Above 1.0 the Continuum recognizes the expression
as law and **supplements it with ambient flow**; the environment becomes a
co-author."*

**[derived] This is physically coherent and canon reasoned it correctly.**
Efficiency above unity breaks the first law only for a closed system; a heat
pump delivers three to five times its input because it moves energy from
outside. Canon's clause is the correct escape and it names the right price:
**there must be a reservoir, and it must measurably deplete.**

Quantified at Anryū Ichimonji's 52,000 AU/s and η 1.05: of every 1.05
delivered, 0.05 is drawn in, so 4.76% of 52.0 MW = **2.48 MW** comes out of the
surroundings. Cooling sea-level air (ρ 1.225 kg/m³, c_p 1,005 J·kg⁻¹·K⁻¹) by
10 K to supply it takes

    V = 2.48 × 10⁶ / (1.225 × 1,005 × 10) = 201 m³ per second

— a sphere 3.6 m in radius, every second. **[draft]** A practitioner running
η > 1 in air stands in a steady inward draught, a ring of condensation and
frost, and a falling barometer. **That is measurable with a thermometer**, and
it is the counter as well as the tell: *starve the reservoir.* Still air behind
glass, vacuum, Aether-dead ground, a Silence Realm — and η falls back below one
by definition, because there is nothing left to supplement it with.

*(At 1 MJ/EU the same figure is 2.48 GW and the bubble is 36.6 m in radius,
which is a weather event rather than a tell. The constant is what makes this
observable instead of theatrical.)*

> **PENDING — C-037.** Part Seventeen rates Class I Muridic at η 0.60–0.70 and
> Part Nineteen puts the same Stages in Tier 5 at η 0.50–0.60. The page flags
> it itself and withdraws neither. Every figure in this Part that reads η off
> a Tier midpoint rather than off a card inherits it. **The question:** *which
> scale governs a Stage VI or VII practitioner's η?*

---

## §7 · Essence Starvation and recovery

### 7.1 The threshold

**[canon]** FoW VII:83, and the same figure at
`wiki/The Magic System/The Core Vocabulary.md:88`,
`The Lexicon of Magic — Master Terminology.md:112` and
`Tier Grade, Bands & the Aether Shell.md:192`:

> Operating below **ten percent EU** produces Essence Starvation: reduced stat
> expression, Shell degradation, Trait flickering.

**[derived] Ten percent of what, in joules, at each Tier's ceiling:**

| Tier | reserve ceiling, EU | Starvation floor, EU | in joules |
|---|---|---|---|
| 3 · Journeyman | 50,300 | 5,030 | 5.03 MJ |
| 4 · Adept | 961,000 | 96,100 | 96.1 MJ |
| 5 · Expert | 1.84 × 10⁷ | 1.84 × 10⁶ | 1.84 GJ |
| 6 · Master | 3.51 × 10⁸ | 3.51 × 10⁷ | 35.1 GJ |
| 7 · Grandmaster | 6.70 × 10⁹ | 6.70 × 10⁸ | 670 GJ |
| 8 · Archmaster | 6.70 × 10⁹ | 6.70 × 10⁸ | 670 GJ |

**[canon]** One card sets its own margin above the floor, and says why that is
allowed: `wiki/Volume I — Character Cards/Hieronymus Cruciferi · The Immortal.md:16`

> **"Flux Sustain — maintains peak output until Essence reserve drops below
> 30%"** is the one percentage figure kept, because **it describes a reserve
> threshold rather than a metaphysical quantity** and Fracture of Worlds names
> ten percent as the Essence Starvation floor. *His thirty percent is a
> personal operating margin, not a law.*

### 7.2 What it costs

**[canon]** The symptoms, three times over: *reduced stat expression, Shell
degradation, Trait flickering.* And the Flicker has a mechanism already
written: `wiki/The Magic System/The Trait System Law, Function and the Forge.md:112`

> **The Flicker.** Traits coming and going without pattern under Essence
> Starvation. A Trait is a standing bias maintained across the Shell, and **a
> Shell below its working reserve cannot maintain a bias**, so the law drops
> out and returns as the reserve moves.

**[draft] The physical reading, and the direction it runs.** A store doing the
same work through a falling density loses efficiency — a discharging cell's
internal resistance rises, a draining capacitor's drive falls. So η should fall
as the reserve falls, which means the waste fraction (1 − η) **rises at exactly
the moment the practitioner can least afford it.** The three symptoms canon
lists are what any system does when its efficiency collapses and its heat
climbs together, and this gives Starvation a direction rather than a line in
the sand: it does not begin at ten percent, it *becomes visible* there.

**[derived] And it makes the two clocks cross.** From §5.3, at 1 kJ the reserve
clock and the heat clock are within a factor of 1.6 on Dougou, a factor of 4 on
Yukazuri, a factor of 1.2 on Yorime. **A practitioner near Starvation is a
practitioner whose heat clock is winning**, because η is falling and the waste
fraction is rising while the reserve that could be spent more slowly is the
thing running out. *(At 1 MJ/EU the heat clock finishes 10⁴ to 10¹⁶ times
sooner than the reserve clock and nobody ever reaches ten percent —
`physics-check.md` §4.7. The mechanic canon defines cannot occur at the brief's
constant. It can at this one.)*

**[canon]** The cost is also permanent in at least one recorded case:
`wiki/Volume I — Character Cards/Borin Ironheart · The Master of the Soul Forge.md:175`

> **Cost:** Borin forfeits a permanent portion of his own EU Reserve for each
> Requiem performed. He has done this seven times. Each one took something from
> him that did not grow back. **His maximum EU Reserve was higher before the
> first.**

### 7.3 How fast it comes back, and on what it depends

**[canon]** FoW VII:109 — the three routes, and what moves each:

> **Passive Recovery** — baseline absorption of ambient Essence without active
> effort. Governed by **Tempering Yield** and **Harmonics Synergy**. **Faster
> near active Wellspring veins, slower in depleted or hostile environments,
> negligible in Silence Realms.**
>
> **Active Recovery** — deliberate absorption through meditation, Wellspring
> communion or alchemical treatment. Significantly faster, but **requires the
> character to stop fighting and concentrate.**
>
> **Crisis Recovery** — surges triggered by soul-cost events, Threshold
> completions or genuine emotional breakthroughs during combat. **Not reliable
> and cannot be manufactured.**

**[derived] The attested rates, and they come in two populations that do not
agree.** Thirteen figures across ten cards:

| entity | kind | as written | % of reserve per minute | EU/min |
|---|---|---|---|---|
| Niran Yukari | passive | 28% EU/min | 28.0% | 135,800 |
| Naori Yukari | passive | 15% EU/min | 15.0% | 6,300 |
| Rashani Zettari | passive | 14% EU/min | 14.0% | 75,600 |
| Mizuki Moto | passive at rest | 12% EU/min | 12.0% | 56,400 |
| Anryū Ichimonji | passive | 11% EU/min | 11.0% | 90,200 |
| Rengai Zettari | passive | 9% EU/min | 9.0% | 126,000 |
| Krothar Veylshroud | passive, chains on | ~18,000 EU/min | 0.64% | 18,000 |
| Krothar Veylshroud | passive, chains off | ~52,000 EU/min | 1.86% | 52,000 |
| Krothar Veylshroud | active, chains off | ~88,000 EU/min | 3.14% | 88,000 |
| Ara Min Mahuo | passive | ~126,000 EU/hour | 0.050% | 2,100 |
| Ara Min Mahuo | active | ~252,000 EU/hour | 0.100% | 4,200 |
| Kwon Mu-jin | passive at rest | ~12,750,000 EU/hour | 0.025% | 212,500 |
| Kwon Mu-jin | active | ~38,250,000 EU/hour | 0.075% | 637,500 |

**The six cards that state a percentage give 9–28% a minute. The four that
state an absolute figure give 0.025–3.1%. The medians are 2.15 decades
apart.** Empty to full is **seven minutes** on the first reading and **sixteen
hours** on the second.

**[draft] The draft's working figures**, for the tables above and for a scene,
pending a ruling:

    Passive recovery, at rest, in ordinary ground   ≈ 10% of maximum reserve per minute
                                                    → empty to full in 10 minutes
                                                    → out of Starvation in ~1 minute
    Active recovery (not fighting, concentrating)    ≈ 2 to 3 × passive
    On an active Wellspring vein                     faster (FoW VII:109; no figure attested)
    In depleted or hostile ground                    slower (ditto)
    In a Silence Realm                               negligible (ditto)
    Crisis recovery                                  cannot be planned for

Ten percent a minute is the bottom of the six-card percentage band (9–28%)
rounded, and it is deliberately the same number Part Nineteen already uses for
the Starvation floor, so one figure serves twice: **a Starved practitioner is
about one minute of rest from being out of Starvation.** Long enough to be a
decision in a fight, short enough not to end one, and slow enough that
`Counterplay:48`'s siege still works — ten percent a minute of a reserve that
empties in twenty seconds does not refill anybody mid-exchange.

> **PENDING.** **The question:** *do the percentage figures and the absolute
> figures measure the same thing?* If yes, ten cards disagree by two decades
> and the absolute ones read as **fractions of a much larger notional
> maximum**. If no, the percentages are a rate on *current* reserve (an
> exponential refill, fast when empty, slow when nearly full) and the
> absolutes are a rate on *maximum* (a linear refill), and the two are
> reconcilable without any card being wrong. The draft takes neither; the
> second is the cheaper repair and the first is what the words say. **This is
> a candidate `CONFLICTS.md` row and is deliberately not filed yet, because
> the two populations may be measuring different quantities rather than
> contradicting each other, and that is a reading a ruling settles in one
> sentence.**

### 7.4 What Starvation is not

**[draft]** It is not unconsciousness and it is not a hit-point track. A
Starved practitioner is still a person with a sword. What they have lost is the
*standing* part of what they were: Traits that were law become weather, the
Shell that was a wall becomes a sheet, stats read one Grade lower than the card
says. **[canon]** `wiki/The Magic System/Counterplay What Beats a Practitioner.md:48` puts the
consequence in the form a commander uses:

> **Exhaustion.** Below ten percent reserve a practitioner suffers Essence
> Starvation: reduced stat expression, Shell degradation, Traits flickering. **A
> defender who can afford to spend nothing wins a long engagement against an
> attacker who cannot afford to spend nothing**, and sieges are decided by this
> more often than by any working.

---

## §8 · What the Ledger gives the other side of the table

Every figure in this Part is a figure someone can use against the person it
describes. Set out in the shape `fair-play.md` asks for, and all of it findable
by reading pages that already exist.

**It costs something that hurts.** §5.2: seven Somnalis Drifts and Yukazuri is
Starved; six constructs and Kwon Mu-jin is. §7.2: Borin's reserve is
permanently smaller seven times over. §6.4: the waste heat is a burn radius
around the practitioner's own position.

**It has stated limits.** §4.3 caps the reserve by Stage. §5.1 caps the
duration at reserve ÷ AU/s. §3 caps the output at the Stage's Max Grade. §5.4
says the AU/s on a card is a burst ceiling, not a duty cycle.

**Something beats it, and it is one of the four routes.**
`wiki/The Magic System/Counterplay What Beats a Practitioner.md:17`:
*"**Deny the field. Break the boundary. Break the body. Break the man.**"* The
Ledger arms the first and the third:

- **Deny the field** — §6.5. A practitioner above η 1.0 is drawing on the room.
  Still air behind glass, vacuum, Aether-dead ground or a Silence Realm takes
  the supplement away and η falls below one by definition. §7.3: the same
  ground stops the refill.
- **Break the body** — §5.3. Every reserve in canon empties in under twenty-six
  seconds at full draw except five. **The whole column is a clock, and making an
  enemy spend is making the clock run.** `Counterplay:48` has been saying this
  without the numbers; this Part supplies them.

**It has a tell.** §6.4 prices it: surface temperature, burn radius, sound
pressure. §6.5 prices the other one: inward draught, condensation, frost,
falling barometer. §7.2: the Flicker is visible before the practitioner admits
to it.

**Its numbers stay in band.** §4.4 shows every attested character against their
Stage's band, including the twelve that sit under it and the two that sit over.

**And it is findable.** A player who reads Part Four gets the Grade ladder. Part
Five gets the Stage gates. Part One gets the Level gates. Part Nineteen gets η
and the Starvation floor. `Counterplay` gets the four routes. This Part joins
them and adds nothing that is not on one of those pages or derivable from them
with a calculator. **Nobody has to be told the answer, and the answer is there
for anyone who looks.**

---

## §9 · What is open

| slot | on | the question |
|---|---|---|
| the constant | **C-034** | is one EU worth the same joules at Stage III as at Stage XIV? |
| the reserve axis | **C-034** | does "scales with Temperance Stage" set the reserve, or cap it through the Band gates? |
| 1 AU = 1 EU | new, §5.3 | does a second at full AU/s cost AU/s worth of EU? Five cards' durations hang on it. |
| the missing mass | **C-035** + §6.2 | does AU/s = Flux Density × η carry an implicit Crystal mass, and whose? |
| η at Stages VI–VII | **C-037** | Class I Muridic's 0.60–0.70 or Tier 5's 0.50–0.60? |
| recovery | new, §7.3 | are the percentage rates and the absolute rates the same quantity? |
| Tier 9 reserve band | — | Part One has no Band for Stages XV–XVI; Part Nineteen has no η figure for Tier 9. Both left null. |
| Stage XIV's Grade | `fit.json` `meta` | Part Five gives Zenith EX; Part Eleven's benchmark row declines to quantify it. |
| the S/SS joule gap | **C-036** | 24.3–41.8 TJ is in Tier 6 and in no Grade. |
| the SSS ceiling | **C-039** | 4.184 EJ or 4.184 ZJ — a thousandfold. |
| Strike Force vs Stage | **C-040** | twelve cards state an output their Stage's Grade does not reach. |
| Level gates vs two cards | **C-041** *(filed by this phase)* | Sodoku at L320/Stage VI and Krothar at L380/Stage VIII are past gates their Stage has not opened. |

**Nothing in this Part resolves any of them.** Where a table had to be built
over an open slot, the reading it used is named in the PENDING block beside it
and the table falls with the reading.

---

## §10 · Sources

**Canon, all quoted verbatim above with file and line.**
`wiki/Fracture of Worlds — The Living System/I. Levels, Experience and Stat Points (Parts One–Three).md` 18, 22–25;
`.../II. Grades, Gates and Thresholds (Parts Four–Ten).md` 16, 17, 28–40, 60, 64–79;
`.../III. Physical Force (Part Eleven).md` 26, 30;
`.../VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md` 83, 84, 85, 86, 96–101, 103, 109;
`wiki/The Magic System/The Core Vocabulary.md` 88, 90;
`.../Counterplay What Beats a Practitioner.md` 17, 48;
`.../The Lexicon of Magic — Master Terminology.md` 112;
`.../Tier Grade, Bands & the Aether Shell.md` 192, 195;
`.../The Trait System Law, Function and the Forge.md` 112;
`wiki/Spellcraft/The Iron Tree.md` 20, 41;
`wiki/The Disciplines/The Open Crucible — Kwon Mu-jin's Book of Summons.md` 30;
`wiki/Summoned and Bound/Obrenkael · The Mule.md` 215; `.../Haelvorn · Housecat.md` 236;
**Cards quoted in the body**, `wiki/Volume I — Character Cards/` — Anryū
Ichimonji 29; Artemis Amagiri Moto 56; Aurelian Prudentius · The Primate 85;
Ayame Yuno 58; Borin Ironheart 103, 175; Dougou Ozumu Zettari 38, 93; Draen
Varos 37; Gimbzo 58; Hieronymus Cruciferi 16; Ignatius Sanctus Sanctorum
Arsenal 141; Iracordas 64; Karo Venrik 137; Krothar Veylshroud 32, 33; Kwon
Mu-jin 73; Sodoku Moto 36, 38; Yorime Seikai 59; Yukazuri Moto 61, 83, 84, 85.

**Cards whose figures populate the tables without being quoted in prose** —
Ara Min Mahuo 38, 71, 72, 74; Ayame Yuno 61; Borin Ironheart 34, 102; Gimbzo
61, 62; Iracordas 48, 52; Krothar Veylshroud 99–103; Kwon Mu-jin 74; Lucius
Xenotro 60, 64; Mizuki Moto 30, 59; Muken Moto 34, 60; Naevra Yukari 48, 51;
Naiser Yukari 57; Naori Yukari 28, 54; Niran Yukari 28, 61; Rashani Zettari 29,
64; Rengai Zettari 29, 60; Sodoku Moto 43, 86; Vethraun Ashmaw 64, 67; Verinus
VII 86; Yoko Mishiro 36, 69; Yorime Seikai 63; Yukazuri Moto 40; Kaelzar 106;
`Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md` 14, 17;
`wiki/Summoned and Bound/Obrenkael · The Mule.md` 75. **Every one of these
carries its own file, line and verbatim line in `anchors.json`**, which is where
a figure in any table above should be checked rather than here.

**Project working files.**
`imports/essence-ledger/anchors.json` and `fit.json` (WAR-9, Phase 1 — every attested figure, with its entity, Stage, Tier, file and line, and the fit against them);
`imports/essence-ledger/physics-check.md` (WAR-10 — the conversion against real physics);
`imports/essence-ledger/ledger_tables.py` and `ledger_tables.json` (this phase — every table above, reproducible);
`CONFLICTS.md` C-034 to C-041; `RULINGS.md` R43.

**Laws used by name, standard and uncited.** Conservation of energy; the second
law and the Gouy–Stodola theorem (Ẇ_lost = T₀Ṡ_gen); E = mc²; Fourier's law of
conduction; the Stefan–Boltzmann law; the thermochemical definition of the ton
of TNT (1 g ≡ 1,000 cal ≡ 4,184 J). Physical constants and body figures are
fixed once in `physics-check.md`, "Method, and the constants used", and are not
restated here.

**Reproducing the arithmetic.**

```bash
python imports/essence-ledger/ledger_tables.py   # -> ledger_tables.json + the report
```

Reads `anchors.json` and `fit.json` only. Writes nothing outside this folder.
