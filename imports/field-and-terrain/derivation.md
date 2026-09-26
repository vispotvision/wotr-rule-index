# Field and terrain — the derivation, with the arithmetic

Repo-facing. This file shows where every figure published under this job comes
from. The published pages carry the results as settled text and cite nothing;
this file carries the sources, the arithmetic and the checks.

Six things are derived here:

1. Numeric ranges for the four Aetheric Density conditions.
2. The saturation threshold, in volume and in rate, and which workings cross it.
3. Absorption: the bank sits in the practitioner's own Crystal, with an overfill
   limit and a stated failure past it.
4. Ambient Resonance as a facet of Aetheric Residue, and why a battlefield
   deafens a Harmonist.
5. Failure terrain for Limina, Spatium, Vectoria and Vitalia.
6. A second Range ladder, for non-force reach, keyed to Grade.

Everything rests on **five constants**, four of which are read off canon and one
of which is derived from canon's own description of the field. Nothing else is
introduced.

---

## The five constants

### C1 · The Aetheric pressure identity

`wiki/The Magic System/The Core Vocabulary.md` §V, the **Joule** entry, live on
the page: *"What one EU is worth outside the Crystal. 1 EU = 1 MJ."* The
**Watt** entry: *"One AU is one EU, so 1 AU/s = 1 MW."*

A density in EU per cubic metre is therefore an energy density in MJ/m³, and
J/m³ and Pa are the same unit:

    1 EU/m³ = 1 MJ/m³ = 10⁶ J/m³ = 10⁶ Pa = 1 MPa

**Aetheric Density read in EU/m³ is the same number in megapascals.** This is
the keystone of the whole job: it is why density *sets a ceiling* rather than
merely correlating with one. A boundary cannot be pushed into a medium at a
pressure the medium does not carry, and the strength of what is standing in the
medium is a pressure too.

### C2 · The relaxation constant: τ = 10³ s, k = 10⁻³ s⁻¹

Canon describes the field as a current running in ground, and says so in
hydrological terms:

- `The Eight Families & the Sixty Wellsprings.md`:49 — *"The way groundwater is
  not stored in a specific container but absolutely collects in aquifers, a
  current concentrates where the substrate is Aether-conductive."*
- ibid.:50 — *"A Wellspring site is the aquifer. The current is the water
  table."*
- ibid.:40 — *"A current pooling in a valley acts on everything standing in the
  valley."*
- ibid.:104 — Wellspring Core is *"The current's origin point. The aquifer's
  source."*

Take the hydrology at its word. Conduit flow in a karst aquifer — the fast case,
the one that behaves like a current in a channel rather than seepage through a
matrix — runs at tracer-measured velocities of roughly 10 to 100 metres per
hour, i.e. 2.8×10⁻³ to 2.8×10⁻² m/s. Take the round figure inside that range:

    v = 1×10⁻² m/s   (36 m/h)

A working's site is the scale of a hall, a courtyard, a drawn circle or a
valley floor:

    L = 10 m

The time for the current to traverse the site, which is the time in which the
site replaces what has been taken out of it and clears what has been put into
it:

    τ = L / v = 10 m ÷ 10⁻² m/s = 1.0×10³ s
    k = 1/τ = 1×10⁻³ s⁻¹

**One constant, three jobs.** A linear reservoir — Darcy flow, Newtonian
cooling, dielectric relaxation, all the same mathematics — has flux proportional
to gradient, so the *same* conductivity governs both directions: what the site
will give up and what it will take in. So k sets

- the **supply ceiling** (a site yields at most k × its stock, per second),
- the **saturation threshold** (injecting faster than k × stock drives the stock
  up), and
- the **decay of Ambient Resonance** (what was put in leaves at k).

That the two directions share one constant is not a convenience; it is what a
linear transport coefficient means.

### C3 · The fracture stress: σ = 10 GPa = 10⁴ EU/m³

A Soul Crystal is a crystal and fails brittle, at a critical stress rather than
at a critical energy. The ideal (flaw-free) tensile strength of a crystal
lattice is about a tenth of its Young's modulus — the standard estimate, of the
same family as Frenkel's ideal shear strength G/2π. For the oxide and silicate
crystals, with E of 70 to 200 GPa, that is 7 to 20 GPa. Take the round figure:

    σ_frac = 1×10¹⁰ Pa = 10 GPa
           = 10⁴ EU/m³              (by C1)

**And this is not a new rung.** 10⁴ EU/m³ falls exactly on the floor of the
third density condition, which canon already describes as the place where
involuntary Soul Drift and Echo Beast manifestation begin
(`The Eight Families`:103). The scale's own third rung is the fracture stress.

### C4 · The 20 dB margin, and what inverse square does with it

A boundary condition must be *imposed*, not merely present: the ordinary
engineering margin for a signal to command a background rather than sit in it is
a factor of 100 in power, 20 dB. Conversely, a coherent narrow-band signature is
*read* well below a broadband background — lock-in detection and matched
filtering recover signals 40 to 60 dB under the noise floor as a matter of
routine, so 20 dB under is conservative.

Canon uses inverse square for field falloff and says so twice:
`Counterplay`:47 — *"Fulguria falls off with the square"*; `Part Eleven`:107 —
*"shockwave energy degrades by the inverse square law."* Under inverse square a
factor of 100 in threshold is a factor of 10 in radius:

    F(r) = P / 4πr²   ⇒   r ∝ threshold^(−1/2)
    100× threshold ⇒ 1/10 × radius

Hence the three non-force reaches of §6 sit one decade apart, and hence every
reach falls as the inverse *root* of the local density (§6, the terrain
multiplier).

### C5 · The pressure-vessel factors: 1.5× and 2.25×

The Crystal is a store held at a pressure (C1), so what bounds it is the same
thing that bounds any vessel: a proof factor and a burst ratio, both real
standards.

- **Proof 1.5×.** Gas cylinders are hydrostatically tested above their service
  rating — the common factors are 1.5 to 1.67 times service pressure. Take 1.5.
- **Burst 2.25×.** The minimum burst ratio required of a composite overwrapped
  pressure vessel is 2.25 times service pressure.

---

## 1 · The four density conditions in numbers

The scale is `The Eight Families & the Sixty Wellsprings.md`:98–104, four named
conditions and no units. Each band below is bounded by a real energy density,
and its supply ceiling is the band times C2.

    s (AU/s per m³) = ρ (EU/m³) × k = ρ × 10⁻³
    in SI:  s × 10⁶ W/m³            (by C1)

| Condition | ρ, EU/m³ | as pressure | s, AU/s per m³ | s in W/m³ |
|---|---|---|---|---|
| Aether-thin ground | 10⁻³ – 10⁻¹ | 1 kPa – 0.1 MPa | 10⁻⁶ – 10⁻⁴ | 1 – 100 |
| **Ambient Saturation** | 0.1 – 10 | 0.1 – 10 MPa | 10⁻⁴ – 10⁻² | 100 – 10⁴ |
| **Active Concentration** | 10 – 10⁴ | 10 MPa – 10 GPa | 10⁻² – 10 | 10⁴ – 10⁷ |
| **Veil-Thin Nexus** | 10⁴ – 10⁸ | 10 GPa – 100 TPa | 10 – 10⁵ | 10⁷ – 10¹¹ |
| **Wellspring Core** | 10⁸ – 7.7×10¹⁸ | 100 TPa – 7.7×10²⁴ Pa | 10⁵ – 7.7×10¹⁵ | 10¹¹ – 7.7×10²¹ |

In a Silence, ρ = 0 and s = 0, which is the whole of why a Silence is not
shielding: there is nothing to draw and nothing to push into.

### Why each boundary sits where it does

**Aether-thin ground.** Below one atmosphere of Aetheric pressure. This is
Limina's favoured terrain (`The Eight Families`:154, *"Aether-thin ground"*) and
the approach to a Silence.

**Ambient Saturation, 0.1 – 10 EU/m³ = 0.1 – 10 MPa.** One atmosphere to a
hundred. The band of the ordinary terrestrial fields, and two real anchors sit
inside it:

- the internal energy of sea-level air:
  1.204 kg/m³ × 718 J/(kg·K) × 293 K = **2.53×10⁵ J/m³ = 0.25 EU/m³**
- the magnetic energy density of a one-tesla field:
  B²/2μ₀ = 1 ÷ (2 × 1.2566×10⁻⁶) = **3.98×10⁵ J/m³ = 0.40 EU/m³**

Supply 100 W/m³ to 10 kW/m³, so a cubic metre of ordinary ground yields about
what a square metre of noon sunlight delivers (1 kW/m²). That is the arithmetic
of *"an ordinary person feels vaguely uneasy or peaceful"* (`The Eight
Families`:101): you are standing in the energy density of the weather.

**The reference density.** The geometric midpoint of Ambient Saturation:

    ρ_ref = √(0.1 × 10) = 1 EU/m³ = 1 MPa

Every figure elsewhere in this job that says "at the reference density" means
this one.

**Active Concentration, 10 – 10⁴ EU/m³ = 10 MPa – 10 GPa.** From a hydraulic
press to the fracture stress itself. Anchors inside the band:

- a lithium cell at 700 Wh/L: 700 × 3600 = 2.52×10⁶ J/L = **2.52×10⁹ J/m³ =
  2,520 EU/m³**
- cast TNT: 4.184 MJ/kg × 1,650 kg/m³ = **6.9×10⁹ J/m³ = 6,900 EU/m³**

Supply 10 kW/m³ to 10 MW/m³. A resting human dissipates about 100 W in about
0.07 m³ of body, which is 1.4 kW/m³. So the field here delivers

    10 kW/m³ ÷ 1.4 kW/m³ = 7×
    10 MW/m³ ÷ 1.4 kW/m³ = 7,100×

seven to seven thousand times the subject's own metabolic power density, into
them, continuously. **That is the arithmetic of Wellspring Baptism being
involuntary** (`The Eight Families`:102: *"A practitioner remaining too long
receives Wellspring Baptism whether they wanted it or not"*) and of :40, which
says the same thing happens to a shepherd. The load is not a choice, because a
body has no way to decline a power density.

**Veil-Thin Nexus, 10⁴ – 10⁸ EU/m³ = 10 GPa – 100 TPa.** The floor is C3, the
fracture stress. The ceiling is planetary-core pressure — Earth's centre is
360 GPa, a gas giant's core a few thousand — the range in which matter itself
changes phase and hydrogen turns metallic. Anchor inside the band: the strongest
magnetic field a laboratory has produced is a destructive pulse of order
10³ T, and at 1,000 T

    B²/2μ₀ = 10⁶ ÷ (2 × 1.2566×10⁻⁶) = 3.98×10¹¹ J/m³ = 4.0×10⁵ EU/m³

Supply 10 MW/m³ to 100 GW/m³, which brackets the power density inside a
lightning channel (order 10¹⁰ W/m³ — roughly 10¹¹ W in a 1.6 m³ channel). The
air is at the power density that makes air glow. *That* is why things not
ordinarily visible are: *"Spiritual entities become visible"*
(`The Eight Families`:103).

**Wellspring Core, 10⁸ – 7.7×10¹⁸ EU/m³.** The ceiling is not chosen. It is the
Schwinger limit: the field at which the vacuum stops behaving as empty space and
begins making electron–positron pairs out of itself.

    E_c = m_e²c³ / (e·ℏ) = 1.323×10¹⁸ V/m
    u   = ½ ε₀ E_c²
        = 0.5 × 8.854×10⁻¹² × (1.323×10¹⁸)²
        = 0.5 × 8.854×10⁻¹² × 1.750×10³⁶
        = 7.75×10²⁴ J/m³
        = 7.75×10¹⁸ EU/m³

Above that there is no physics left to state, which is the literal reading of
*"The physical and metaphysical environments are indistinguishable, and the law
the Wellspring carries is the only law operating"* (`The Eight Families`:104):
the vacuum has stopped being a medium and started being a participant.

### The ceiling on output, and the check against attested figures

`The Core Vocabulary`:39 — Aetheric Density *"sets the ceiling on the AU/s
output a practitioner can achieve in that location."* The ceiling is the supply
rate times the volume the practitioner's field reaches, and the volume the field
reaches is the **authority radius** of §6:

    ceiling = s × (4/3)π r³

At the reference density, s = 10⁻³ AU/s per m³:

| Grade | r (§6) | V = (4/3)πr³, m³ | ceiling, AU/s | attested draw | fraction |
|---|---|---|---|---|---|
| F | 2 m | 33.5 | 0.0335 | — | — |
| B | 50 m | 5.24×10⁵ | 524 | — | — |
| A | 200 m | 3.35×10⁷ | 3.35×10⁴ | 16,376 (Niran Yukari) | 49% |
| S | 1 km | 4.19×10⁹ | 4.19×10⁶ | 22 (Serenyra Vaelith) | 5.3×10⁻⁴ % |
| EX | 12,700 km | 8.58×10²¹ | 8.58×10¹⁸ | 2.8×10⁶ (Francis Alexander) | 3.3×10⁻¹¹ % |

Arithmetic: (4/3)π = 4.18879. 2³ = 8 → 33.5. 50³ = 1.25×10⁵ → 5.24×10⁵.
200³ = 8×10⁶ → 3.351×10⁷. 1000³ = 10⁹ → 4.189×10⁹.
(1.27×10⁷)³ = 2.048×10²¹ → 8.58×10²¹.
16,376 ÷ 33,510 = 0.489. 22 ÷ 4.19×10⁶ = 5.25×10⁻⁶.
2.8×10⁶ ÷ 8.58×10¹⁸ = 3.3×10⁻¹³.

Attested AU/s figures and their Stages are `imports/system-accounts/_method.md`
§VIII. **Nothing attested comes near its ceiling on ordinary ground**, which is
the right result: this is a terrain constraint that bites when the ground is thin
or the working is held small, not a cap on named practitioners. Niran at 49% is
the tightest case in the corpus and the one worth knowing about — an A-Grade
working at half the ambient ceiling has nothing left if the ground gets thinner.

### The ceiling is not the joule budget

`The Physical Account Two Sets of Books.md`:33 — *"The practitioner does not
supply the joules. They supply the boundary condition."* AU/s is the rate at
which a boundary is set. The joules a working moves come from the store the law
is pointed at. An F-Grade's 0.0335 AU/s ceiling is 33.5 kW; an F-Grade strike
delivers 0.1–0.3 GJ (`Part Eleven`, Strike Force). Both are correct. They are
entries in different books, and `_method.md` §IV says so.

---

## 2 · The saturation threshold

`The Core Vocabulary`:41 — *"A danger state in which excessive Essence floods an
area faster than it can disperse. Produces Crystal Fracture Events in everyone
exposed, including the person who caused it."*
`Two Sets of Books`:25 — *"Saturation is the ceiling past which a district stops
accepting further expression and begins returning it."*

Saturation is a **density**, not a total: the density at which what is standing
in the field fractures, which is C3.

### The volume form

A working leaving E EU in a volume V, in a time short against τ, raises the
density by E/V. It saturates when

    E / V ≥ σ_frac = 10⁴ EU/m³
    E ≥ 10⁴ × V          (E in EU, V in m³)

| region | V, m³ | saturating deposit, EU |
|---|---|---|
| one cubic metre (a body) | 1 | 1×10⁴ |
| a 2 m circle | 33.5 | 3.35×10⁵ |
| a 10 m hall | 4.19×10³ | 4.19×10⁷ |
| a 100 m front | 4.19×10⁶ | 4.19×10¹⁰ |
| a 1 km field | 4.19×10⁹ | 4.19×10¹³ |

### The rate form

In steady state the excess leaves across the region's surface at the current's
own speed (C2), so a region of radius r holding an excess ρ_ex sheds
4πr²·v·ρ_ex per second. Injecting at R AU/s gives

    ρ_ex = R / (4πr² v)

and saturation is ρ_ex ≥ σ_frac, i.e.

    R / 4πr² ≥ v · σ_frac = 10⁻² m/s × 10⁴ EU/m³ = 100 AU/s per m²

**More than 100 AU/s through each square metre of the region's boundary.** The
two forms are one statement: the rate form is the volume form times the
current's speed.

| region | 4πr², m² | saturating rate, AU/s |
|---|---|---|
| a 2 m circle | 50.3 | 5.0×10³ |
| a 10 m hall | 1.26×10³ | 1.26×10⁵ |
| a 100 m front | 1.26×10⁵ | 1.26×10⁷ |
| a 1 km field | 1.26×10⁷ | 1.26×10⁹ |

### The consequence: you saturate by confining, not by spending

The threshold rate grows as r²; delivered output does not. **Small volumes
saturate. Large ones swallow.**

### Which workings cross it

Checked against the seventy-six accounts in `imports/system-accounts/`.

**The kilometre-scale Zenith fields do not cross it.** The three are Crimson
Dirge at 1 km, Dirge Ascension at 1 km and Judgment Manifest at 2 km. Dirge
Ascension is the one with a stated rate, 2.8×10⁶ AU/s (`_method.md` §VIII):

    2.8×10⁶ ÷ 1.26×10⁷ m² = 0.22 AU/s per m² = 0.22% of threshold

A kilometre of ground swallows a Zenith working. The same output confined to a
20 m hall (4πr² = 5.03×10³ m²):

    2.8×10⁶ ÷ 5.03×10³ = 557 AU/s per m² = 5.6× threshold

So the answer to *"if a kilometre-wide Zenith field is not saturation, what is"*
is: the same field indoors.

**Coagula Dominium does not cross it.** The working holds 1.41×10⁴ m³; the
volume form puts its saturation deposit at 1.41×10⁸ EU, which is above any
reserve on any card in the corpus. Ordered coagulation at that volume is not
saturation.

**Scission does not cross it, and reaches Active Concentration instead.** It
bleeds 18,000–24,000 EU into one small fixed circle over six to twelve minutes:
25–67 EU/s. Against a 2 m circle's 50.3 m² boundary that is 0.5–1.3 AU/s per m²,
about one per cent of threshold. But accumulated over 720 s against τ = 10³ s,
most of it is still there:

    24,000 EU ÷ 33.5 m³ = 716 EU/m³

716 EU/m³ is **Active Concentration**, held for the length of the rite, in a
room nobody may leave — and the density scale already states what that condition
does to anyone who stays. The Circle step of a Ritus is the thing that keeps it
from climbing further, and an improvised circle is where the risk lives.

**What does cross it is not a working but a fight in a room.** Four S-Grade
practitioners at their reference-density ceiling (4.19×10⁶ AU/s each, §1) for
sixty seconds inside a 20 m hall:

    4 × 4.19×10⁶ × 60 = 1.01×10⁹ EU
    V = (4/3)π(20)³ = 3.35×10⁴ m³
    1.01×10⁹ ÷ 3.35×10⁴ = 3.0×10⁴ EU/m³ = 3.0 × σ_frac

Three times the fracture stress, and every Crystal in the hall is in it.
`Counterplay`:26 says the practical use of saturation *"is the threat rather than
the act"*; this is why. You cannot flood a battlefield. You can flood a
building, and you have to be inside it.

---

## 3 · Absorption: the bank is in the Crystal

The question this answers is where the energy goes in a working that takes an
incoming load and holds it — Cryost Ascendant's arrested force, Kurotana's
Witness Backlash, Solarbound's Strain Lamina, Sovereign's Reprisal, the
Principle Engine's buffer. Canon prices efficiency at the moment of spending and
says nothing about a charge *held* between the spend and the effect.

**The bank sits in the absorber's own Crystal, not in the room.** And what
bounds a store held at a pressure is not its total but its density: a capacitor
fails at a critical field, a vessel at a critical pressure, neither at a
critical energy. The Crystal's rated density is already a system quantity —
**Flux Density, EU per gram** (`The Core Vocabulary`:89).

### The overfill limit is the rated Flux Density

With C5, the failure is graded exactly as a pressure vessel's is, and each rung
lands on a Crystal State canon already has (`The Core Vocabulary`:64).

**To 1.5× rated Flux Density — the proof range. It holds, and it leaks.** The
surplus above rating bleeds at the Crystal's own bleed fraction, 1 − η of itself
per second (`The Core Vocabulary`:91, η is *"the ratio of Essence spent to
Essence that arrives as intended effect"*, so the loss fraction is 1 − η). The
bank's e-folding life is therefore 1/(1 − η) seconds:

    η = 0.70 → 1/0.30 = 3.3 s
    η = 0.90 → 1/0.10 = 10 s
    η = 0.95 → 1/0.05 = 20 s

**A bank is a tempo, not a battery.** And it is visible: 1 − η leaves as heat,
sound and structural bleed, so a man holding a bank is lit up for as long as he
holds it. Crystal State: **Refined**.

**1.5× to 2.25× — permanent set.** Past proof the lattice takes a permanent
deformation and the rated Flux Density itself falls. Crystal State:
**Overgrown** — *"power exceeding architecture, producing involuntary
discharge."*

**At or past 2.25× — burst.** A **Crystal Fracture Event**, in the absorber,
from energy that was aimed at him and that he chose to take. Crystal State:
**Fractured** — *"split by trauma or overload, producing erratic casting and
identity leak."*

### Counterplay, and why absorption is not a free defence

Three routes fall straight out and none of them requires out-hitting him.
**Overfill him** — feed the absorber past 1.5× his rating and the defence
becomes the wound. **Wait him out** — the bank's life is a few seconds to a few
tens of seconds, so a defender who declines to be hit for ten seconds has taken
the bank away without touching him. **Find him** — the bleed is the tell, and it
runs for exactly as long as the bank does.

---

## 4 · Ambient Resonance, a facet of Residue

`The Core Vocabulary`:40 — Aetheric Residue is *"Traces left behind by an Essence
working. A permanent, if often subtle, change to the location where the working
occurred."*

**Ambient Resonance is the part of Residue still ringing** — the same trace,
read while it decays, and therefore not a second quantity and not a second unit.
It is measured in EU/m³, because it *is* density: the excess a working left
behind, on its way out.

### It decays at the one constant

Resonance falls as e^(−t/τ) with τ = 10³ s (C2):

    down 20 dB (a hundredfold):  t = τ ln(10²)  = 1000 × 4.605  = 4.6×10³ s = 77 min
    down 60 dB (a millionfold):  t = τ ln(10⁶)  = 1000 × 13.816 = 1.38×10⁴ s = 3.8 h

**Ground stops ringing about four hours after the working stops.** That is a
reverberation time, and it is measured in hours rather than seconds because the
medium is ground rather than air.

### It limits by raising the floor, not by lowering the ceiling

Density caps what a practitioner can *draw*. Resonance masks what a Harmonist
can *hear*: the work is a signal against a background, and the background is the
ground's ring. By C4, reach goes as the inverse root of the background, so every
non-force reach on rung ground is cut by

    √( (ρ_site + ρ_resonance) / ρ_ref )

### The worked figure

Twenty A-Grade practitioners at their reference-density ceiling, 3.35×10⁴ AU/s
each (§1), for five minutes, over a 200 m radius:

    20 × 3.35×10⁴ × 300 s = 2.01×10⁸ EU
    V = (4/3)π(200)³       = 3.35×10⁷ m³
    ρ_resonance = 2.01×10⁸ ÷ 3.35×10⁷ = 6.0 EU/m³
    total = 1.0 + 6.0 = 7.0 EU/m³
    √(7.0/1.0) = 2.65

**Every Harmonist on that ground hears at 38% of his ordinary range** (1 ÷ 2.65
= 0.378), and is back to ordinary about four hours later. The same fighting in a
hall rather than a field leaves Active Concentration, where the factor is not
2.6 but 18 (§6).

### Which is what Caelmorne bought

`The Disciplines/The Harmonic Arts.md`:127 — Caelmorne Halvrein *"conducting
sessions during lunar Aether tides, when ambient Resonance naturally quiets"*,
and his method *"begins with silence"*, the practitioner dampening their own
Resonant Tone to near-nothing. `Spellcraft/Anima Harmonics.md` — *"a Harmonist
with loud, undisciplined Shell output hears nothing but their own tone."* Those
are one move made twice: he could not raise the signal, so he lowered the
background, his own first and the site's second. The figures above say by how
much.

---

## 5 · Failure terrain for the four Families

`Counterplay`:25 gives four Families their terrain and leaves four without:
Caloria, Fulguria, Materia and Fluxia are there; Limina, Spatium, Vectoria and
Vitalia are not. The suppressive conditions are already canon in
`The Eight Families & the Sixty Wellsprings.md`:145–154, the Environmental
Coupling table. Each line below is that column, with the real reason it
suppresses and the kit that buys it.

**Limina** — *"Saturated Aether, crowd density, active Domains"* (:154). Family
governs *"Entropy, void, mind"*, Physics Domain *"Abstract / entropic"* (:136).
Entropy work needs a gradient, and a medium already at its ceiling has none to
offer — you cannot raise the disorder of something maximally disordered. Void
work needs an absence to work from. Mind work is a signal problem, and a crowd
is noise. Kit: light, company, and somebody else's law over the ground.

**Spatium** — *"Warp scarring, contested Domains, unmapped terrain"* (:150).
Family governs *"Distance and position"*, Physics Domain *"Spatial geometry"*.
A coordinate transform needs a datum: a survey the practitioner can trust to say
where *here* is. Geodesy cannot translate between frames without one. Wreck the
survey and the transform has nothing to solve against. Kit: unmapped ground,
contested ground, scarred ground.

**Vectoria** — *"Loose sediment, free fall, uniform soft ground"* (:149). Family
governs *"Force, motion, gravity"*, Physics Domain *"Mechanics"*. Force needs a
reaction; Newton's third law is not negotiable by a Grade. Sediment shears
before it transmits, soft ground absorbs the brace, and a man in free fall has
no frame to push against. Kit: sand, scree, mud, deep water, and nothing to set
his feet on.

**Vitalia** — *"Sterile ground, extreme cold, Essence-depleted soil"* (:152).
Family governs *"Biology and anatomy"*, Physics Domain *"Biochemistry"*.
Biochemistry is rate-limited: reaction rates fall by roughly half for every ten
degrees of cooling (Q₁₀ of 2 to 3), and no substrate means no reaction at any
temperature. Kit: winter, stone, salted earth.

The page's own closing caution holds for all four (`The Eight Families`:156):
*"None of this is a prohibition… Terrain is not flavour. It is a modifier on
η."*

---

## 6 · The second Range ladder: non-force reach

`Part Eleven` ladders force range against Grade ("Range and Force Coherence",
:104–124) and nothing ladders reach that is not force. Three quantities need
one:

- **Anchor reach** — the greatest distance between the practitioner (or the ink,
  blood, voice or hand that anchors him) and the boundary he sets.
- **Authority radius** — the radius inside which his own law is the operating
  law: a Domain's edge, a ward's jurisdiction, a Seal's writ.
- **Addressing range** — the greatest distance at which he can name a thing
  precisely enough to impose a boundary on it.

### The three are one field at three thresholds

By C4, they differ by the 20 dB margin, and inverse square turns each step into
a factor of ten in radius:

- a boundary must sit **20 dB over** the background to be imposed → anchor reach
- the background itself is where his law stops being the operating one →
  authority radius
- a name, being coherent and narrow, is read **20 dB under** the background →
  addressing range

        anchor reach : authority radius : addressing range = 1 : 10 : 100

### The scale is not a new number either

`Part Eleven`'s range table already ladders a radius against Grade: the
**Passive Pressure Field**, *"the maximum distance…"* at which a practitioner's
presence is felt — which is precisely the radius at which his field still stands
above the ground's. Read at the reference density (§1), **that column is the
authority radius**, and the other two are one decade either side.

| Grade | Part Eleven's Passive Pressure Field | Anchor reach | Authority radius | Addressing range |
|---|---|---|---|---|
| F | Faint static within 2 m | 0.2 m | 2 m | 20 m |
| E | Palpable within 5 m | 0.5 m | 5 m | 50 m |
| D | Air buckles within 10 m | 1 m | 10 m | 100 m |
| C | Distant thunder within 30 m | 3 m | 30 m | 300 m |
| B | Oppressive chorus within 50 m | 5 m | 50 m | 500 m |
| A | Sky hums within 200 m | 20 m | 200 m | 2 km |
| S | Storm reverence within 1 km | 100 m | 1 km | 10 km |
| SS | Worship or panic within 5 km | 500 m | 5 km | 50 km |
| SSS | Metaphysical law within 50 km | 5 km | 50 km | 500 km |
| X | Continental presence | 300 km | 3,000 km | 30,000 km |
| EX | Planetary presence | 1,300 km | 12,700 km | 127,000 km |

Hollow has no passive field and therefore no non-force reach past contact. X and
EX are given as presences rather than figures; read as a continent's span
(3,000 km) and a planet's diameter (12,700 km). Above EX the force ladder stops
giving figures and so does this one.

### Three modifiers, each derived

**Terrain.** By C4 all three fall as the inverse root of the local density
(Ambient Resonance counted in the same sum), against ρ_ref = 1 EU/m³. Band
midpoints, geometric:

    Aether-thin:  √(10⁻³ × 10⁻¹) = 10⁻²      → 1/√(10⁻²)   = ×10
    Ambient:      √(0.1 × 10)    = 1          → ×1
    Active:       √(10 × 10⁴)    = 316        → 1/√316      = ÷17.8  (call it ÷18)
    Veil-Thin:    √(10⁴ × 10⁸)   = 10⁶        → 1/√(10⁶)    = ÷1,000
    Core:         √(10⁸ × 7.75×10¹⁸) = 2.78×10¹³ → 1/√(...)  = ÷5.3×10⁶

**And that is why no one holds a Domain inside a Wellspring Core.** An S-Grade's
kilometre of authority becomes

    1,000 m ÷ 5.3×10⁶ = 1.9×10⁻⁴ m = 0.19 mm

which is the quantitative form of *"the law the Wellspring carries is the only
law operating"* (`The Eight Families`:104). The physics reproduces the sentence.

**A working target is louder.** A target standing above the background by the
same 20 dB margin his own working needs is addressed at **ten times** the range.
Suppression is the converse, and `Counterplay`:57 already prices it: *"A
practitioner who cannot afford to be identified is paying continuously for the
privilege."*

**Below Refraction the anchor is not the body.** `The Four Crafts`:201 — *"Below
Stage VII, Refraction, a working requires voice, hand, ink or blood: an external
anchor for the boundary."* Anchor reach is measured from the anchor, which is why
a drawn circle or an inscribed wall is worth more than a Grade: it moves the
origin to where the boundary is needed.

### The crossover, and the failure modes

Against `Part Eleven`'s Projected Force Range (50% yield):

| Grade | force range | addressing range | further |
|---|---|---|---|
| F | 5–10 m | 20 m | name |
| E | 10–20 m | 50 m | name |
| D | 30–70 m | 100 m | name |
| C | 100–200 m | 300 m | name |
| B | 0.5–1 km | 500 m | level |
| A | 3–8 km | 2 km | strike |
| S | 20–50 km | 10 km | strike |
| SS | 300–800 km | 50 km | strike |

**They cross at B-Grade.** Below it a practitioner can name what he cannot hit;
from B upward he can hit what he cannot name. Artillery outranges authority, and
it starts doing so the moment a man is worth calling dangerous.

The failure modes follow from the thresholds, and two of them are the **Boundary
Fault** already in the register (`_method.md` §IV, `Two Sets of Books` §VII:
*condition imprecise, law ran somewhere unintended*):

- **Past addressing range** the name does not single the target out. Two men are
  one address, and the working lands on both, or on the wrong one.
- **Past anchor reach** the boundary will not hold. It sets and slips.
- **Past authority radius** nothing of yours is operating — and a Seal sworn on
  authority you do not have there closes anyway, *"with the difference deducted
  from the speaker at the moment of closing"* (`Counterplay`:35).

---

## What is published where

| Result | Page |
|---|---|
| Density in EU/m³, the pressure identity, the ceiling formula | The Core Vocabulary (Aetheric Density) |
| Ambient Resonance as a facet, with its decay | The Core Vocabulary (Aetheric Residue; new entry) |
| The saturation threshold, both forms | The Core Vocabulary (Aetheric Saturation) |
| The bank, the overfill limit, the three states | The Core Vocabulary (new entries, §III) |
| The numeric density scale, supply ceilings, anchors, saturation worked | The Eight Families & the Sixty Wellsprings |
| The non-force ladder, modifiers, crossover, failure modes | III. Physical Force (Part Eleven) |
| Failure terrain for the four Families; shrink his authority; overfill him; the saturation threshold | Counterplay: What Beats a Practitioner |
| The ambient floor, the decay, the battlefield figure | The Harmonic Arts |
| The ambient floor as the branch's field limit | Anima Harmonics |
