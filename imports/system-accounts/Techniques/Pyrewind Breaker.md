---
page: wiki/Techniques/Pyrewind Breaker.md
section: Techniques
practitioner: null (generic Codex entry, no named hand)
card: null
wellspring: Exuroth (primary) · Cataclysm (secondary)
family: Caloria
stage_floor: VI
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · Pyrewind Breaker

## 1 · Physical account (physics)

**The phenomenon in plain words.** Fire spirals outward from the caster to twenty metres and burns
everything standing in it, and a blunt pressure wave follows the fire out — sometimes ahead of it.

**The real phenomenon.** **A deflagration that may or may not complete the transition to
detonation**, and this page is unusual in the batch: its Wellspring's own analogue answers the
question the page says nobody knows the answer to.

**(a) The deflagration-to-detonation transition, with its real numbers.** Cataclysm's stated
analogue. A subsonic flame front — laminar burning velocity for hydrocarbon–air is only about
**0.4 m/s**, rising to a few metres per second with turbulence — accelerates when confinement and
turbulence feed back into it, and past a threshold the reaction zone couples to a shock and the whole
thing propagates **supersonically**. A stoichiometric hydrocarbon–air detonation runs at a
Chapman–Jouguet velocity of roughly **1,800 m/s** with a CJ overpressure near **18 bar**. The
register is precise about the character of it: *"The mechanism is a change of kind, not degree."*

**(b) And that answers the page's open question completely.** *"Why the shockwave sometimes outruns
the flame it came from instead of arriving with it."* Because in a **deflagration** the flame front
moves at metres per second while the pressure disturbance it drives moves at the local sound speed,
**343 m/s** — three orders of magnitude faster — so the shock always arrives first. In a **detonation**
the reaction zone is *locked to* the shock by definition, so they arrive together. **The shock
outruns the flame whenever the burst is a deflagration and arrives with it whenever DDT has
completed**, and whether DDT completes depends on confinement and turbulence, which change from room
to room. **The page's "What nobody knows" is the textbook distinction between its own Wellspring's two
regimes, and the Families page states the law in the entry the Codex line already cites.** This is
the best lookup in the batch.

**(c) But DDT needs the one thing an open burst does not have.** The register: *"A subsonic flame
front that meets **sufficient confinement and turbulence** accelerates until the reaction couples to
a shock wave."* The page's working *"detonates outward to a 20-metre radius"* in the open. **An open
outward burst is precisely the condition in which DDT does not occur**, so the technique's default
mode is a deflagration — which is consistent with the shock outrunning the flame, and inconsistent
with the word *detonates* in the Effect line.

**(d) Blast scaling, and the radius does not match the yield.** Blast obeys the **Hopkinson–Cranz
cube-root law**: at scaled distance Z = R/W^(1/3) the overpressure is the same for any charge. Anchor
it on a figure everybody uses: **1 kg of TNT produces roughly 34 kPa (5 psi, severe structural
damage) at about 4 m**, so Z ≈ 4 m·kg^(−1/3) for that overpressure. Now run the page's own numbers.

- The page states an A-Grade yield, **46 GJ to 4.184 TJ, 11 to 1,000 tonnes of TNT** (Part Eleven's A
  row, quoted exactly).
- At the **floor**, 11 t = 11,000 kg: R = 4 × 11,000^(1/3) = 4 × 22.2 = **89 m.**
- At the **ceiling**, 1,000 t = 10⁶ kg: R = 4 × 100 = **400 m.**
- Working backwards from the stated **20 m** radius: W^(1/3) = 5, so **W = 125 kg of TNT = 5.2×10⁸ J**
  — which is **C-Grade** (0.005–0.25 t), two whole Grades below the page's requirement.

**So the twenty-metre radius is a C-Grade blast and the stated yield is an A-Grade one, and the two
disagree by a factor of between four and twenty in radius and by three orders of magnitude in
energy.** Logged.

**(e) The thermal half, which closes beautifully.** Take the 20 m radius seriously and price the
fire instead of the blast.

- Sphere: (4/3)π(20 m)³ = **3.35×10⁴ m³**; air mass **4.1×10⁴ kg.**
- Raising that to flame temperature, ΔT ≈ 1,500 K: 4.1×10⁴ × 1,005 × 1,500 = **6.2×10¹⁰ J = 62 GJ.**
- **A-Grade's floor is 46 GJ.** **The thermal content of a 20 m fire-filled sphere sits just inside
  the bottom of the band the page claims.**
- And there is a hard chemical cap the page does not state. Air is 23 % oxygen by mass, so the sphere
  holds **9.4×10³ kg of O₂**; hydrocarbon combustion needs about 3.4 kg O₂ per kg fuel, so at most
  **2,800 kg of fuel** can burn in it, releasing 2,800 × 43 MJ/kg = **1.2×10¹¹ J = 120 GJ.**
  **One hundred and twenty gigajoules is the ceiling on any chemical fire in a 20 m sphere of ordinary
  air, and it is 2.9 % of the A-Grade band's top.**

**The fire closes at the bottom of A-Grade. The blast does not close at 20 m at all.** That is the
page's central numeric problem stated as precisely as it can be stated.

**(f) Exuroth, and why the caster survives it.** Quench and temper: a steel quenched past its
martensite-start temperature is hard and brittle to the point of uselessness, and tempering at
**200–650 °C** restores toughness by permitting controlled carbide diffusion, taking a part from
roughly **65 HRC** to the low forties. The register: Exuroth *"runs the Crystal on that cycle …
so the lattice arrives at a hardness the same material could never have reached by slow cooling."*
Its failure is the caster's real risk: *"Quench cracking. Cycle too fast without the tempering
interval and the lattice arrives hard, brittle, and split along its own thermal gradients."*
**That is the page's *"genuine risk of internal overheating … worse with repeated use in a short
span"*, and the register names the mechanism the page only gestures at: it is not overheating, it is
cycling without the interval.**

**The governing law, and the page's worst exposure.** Part Eleven's **Aether-Physics Fusion Rule**:
*"magical combat must obey physical law and Aetheric law simultaneously … The Continuum measures the
energy that arrived."* A blast radius is not a design decision. It is W^(1/3).

**Measurable quantities, SI.**
- Radius **20 m** (page); sphere **3.35×10⁴ m³**; air mass **4.1×10⁴ kg.**
- Duration: **under 1 s** (page, "1 turn (instant burst)").
- Laminar burning velocity, hydrocarbon–air: **≈0.4 m/s.** CJ detonation velocity: **≈1,800 m/s.**
  CJ overpressure: **≈18 bar.** Sound speed: **343 m/s.**
- Hopkinson–Cranz: **Z = R/W^(1/3)**; 34 kPa at **Z ≈ 4 m·kg^(−1/3).**
- A-Grade band (Part Eleven): **20–100 GN · 46 GJ – 4.184 TJ · 11–1,000 t TNT.**
- Radius implied by the A-Grade floor: **89 m.** By the ceiling: **400 m.**
- Yield implied by the stated 20 m radius: **125 kg TNT = 5.2×10⁸ J = C-Grade.**
- Thermal content of the stated sphere: **≈62 GJ.** Chemical ceiling from available O₂: **≈120 GJ.**
- Reflected-shock amplification in confinement: **up to ~8×** the incident overpressure in the ideal
  strong-shock limit, ~2.4× at weak shocks.
- Exuroth's tempering window: **200–650 °C**; hardness **65 → low 40s HRC.**

**The energy budget, and where the joules were.** **In the air's oxygen, and nowhere else.** That is
the finding, and it is a hard ceiling rather than a soft one: 120 GJ is all the chemistry a 20 m
sphere of ordinary air can supply, which is 2.6× the A-Grade floor and 0.029× the A-Grade top. So the
working can reach the bottom of its stated band and cannot approach the middle of it **in air**, and
the Families page's suppressive condition for Caloria — *"oxygen-poor air"* — is the same sentence
said from the other side. Anything above 120 GJ has to come from a store the page does not name.

**Precedent we are not copying.** The expanding fire-blast is the most crowded slot in the genre:
Bakugō's Howitzer Impact, every Explosion spell, Fire Emblem's Bolganone, Dragon Ball's Kamehameha,
the standard MMO nova. Those are **yield without a radius argument**. This one has a radius, a
duration and a Grade, which means it can be checked — and being checkable is what makes the
discrepancy interesting rather than invisible. The divergence worth keeping is the page's own honest
Limitation: *"Once released, the burst cannot be steered, throttled or called back."* A nova with an
undo is a genre convention; a deflagration is a chemical process with a stopping condition written
into how much oxygen is in the room.

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** A single burst across **3.35×10⁴ m³**, under a second. Caloria is favoured by
*"Steep thermal gradients, combustible atmosphere, geothermal ground"* and suppressed by
*"Thermal equilibrium, saturated cold, oxygen-poor air"* (Families page, Environmental Coupling), and
the Counterplay register repeats it as doctrine: *"Caloria fails in thermal equilibrium, saturated
cold, and oxygen-poor air."* **This is one of the few workings in the batch whose terrain counter is
in the register rather than having to be assembled** — and the oxygen clause is not only a modifier
on η here, it is a hard cap on the chemistry, which the account has priced above. *"Terrain is not
flavour. It is a modifier on η."*

**Residue:** heavy, physical, and the page's own counter is made of it. *"Aetheric Residue · Traces
left behind by an Essence working. A permanent, if often subtle, change to the location where the
working occurred"* (`Core Vocabulary` §II) — and after a Pyrewind Breaker nothing is subtle. Note that
the working's **own products** are the thing Cinerion metabolises (*"What survives a fire is not
waste"*), which is why the page reaches for a Cinerion barrier as a counter; the register's Cinerion
is char and ash, not rust, of which more below.

**Saturation:** the danger the page does not name, and it is close here. *"Aetheric Saturation · A
danger state in which excessive Essence floods an area faster than it can disperse. Produces Crystal
Fracture Events in everyone exposed, **including the person who caused it**"* (`Core Vocabulary` §II).
A repeated burst in the same twenty metres — which the page's Cost explicitly warns against — is that
state arriving, and the Counterplay register prices it as *"a weapon of last resort and a real one."*

**Wellspring stratum.** **Exuroth · *The Trial Flame*** (primary), Family **Caloria**, Physics Domain
**Thermodynamics**. Its law, verbatim from
`wiki/The Eight Families & the Sixty Wellsprings/Caloria — Thermodynamics.md`:

> "A steel quenched from austenite is hard and useless, brittle to the point of shattering. Tempering
> restores toughness by permitting controlled diffusion. Exuroth runs the Crystal on that cycle:
> repeated thermal shock followed by controlled recovery, so the lattice arrives at a hardness the
> same material could never have reached by slow cooling."
>
> **Failure** · "Quench cracking. Cycle too fast without the tempering interval and the lattice
> arrives hard, brittle, and split along its own thermal gradients."

**Cataclysm · *The Shattered Law*** (secondary), same Family:

> "A subsonic flame front that meets sufficient confinement and turbulence accelerates until the
> reaction couples to a shock wave and begins propagating faster than sound in the unreacted medium.
> The mechanism is a change of kind, not degree. Cataclysm makes that transition available to Essence
> expression, and blast radius thereafter scales with the cube root of yield, which is why the
> Wellspring's area effects widen coherently rather than merely spilling."
>
> **Failure** · "Reflected overpressure. In confinement the shock returns along its own path, and the
> practitioner standing at the origin receives the sum of the wave and its reflection."

**Two things follow that the page does not say.** First: *"blast radius thereafter scales with the
cube root of yield"* is written into the Core Law itself, so the radius-versus-yield mismatch is not a
quibble about real-world ballistics — **the working's own Wellspring states the scaling rule the page
breaks.** Second: **Cataclysm's failure is the caster standing at the origin of a reflected shock.**
A normally reflected shock can return up to roughly **eight times** the incident overpressure, and the
page's Counterplay invites exactly the geometry that produces it — *"accept the shockwave's
redirection through a Cinerion barrier"* — without noticing that a redirecting barrier is a reflecting
surface and the caster is twenty metres from it in the middle.

Same-Family harmonisation, which *"compounds"* (Families page), and the page reads the compounding
correctly: both currents strengthen **Ardency Overchannel** (from Detonation, via the Merge Ledger),
*"which is why the technique reads as volatile even though its Family is a straightforward
thermodynamic one."* Part Seven adds the teeth: Overchannel carries *"inherent Overflow risk above
D-Grade and Backlash risk above C, **with no Path providing structural protection**."* At A-Grade that
is unavoidable Backlash risk, and **that is the mechanical derivation of the page's Cost.**

*Four Theories.* **Consent Doctrine**, entirely. A flame front is offered no intention, and the page
is the most doctrinally uncomplicated in the batch. The only place another theory could get a footing
is the page's own unanswerable — and the physics answers that, so no theory is needed.

**Essence stratum.** Active layer: the **Aether Shell**, projected outward — Spellcraft's ephemeral
sentence, and the page files the Craft with unusual care: *"Spellcraft (Ars Vocis; declared, with a
chant carrying the working when the caster wants the extra output a release call buys)."* **That
chant clause sits on a fault line**, because `The Four Crafts` ratifies **Chantcraft** as its own
craft — *"Ars Cantus … Neither ephemeral nor permanent. It holds for as long as it is sung"* — and
*"It scales with throats. Everything above trivial requires more than one voice."* A single caster's
release call is a shout, not a chant, and reading it as a chant would move the working into a craft
that cannot be practised alone. Developmental Tier at Stage VI: **Harmonic** (Part Twenty-One).
Crystal State: `null` — no practitioner. **The invoice:** *"High Aether burn and a genuine risk of
internal overheating in the caster, worse with repeated use in a short span"* — which is Overchannel
Backlash with no Path protection, plus Exuroth's quench cracking when the tempering interval is
skipped.

**The lens: Plutonism against Neptunism.** James Hutton, *Theory of the Earth* (1788, expanded 1795),
against Abraham Gottlob Werner's Neptunism. The question was whether the rocks of the world were laid
down by **water** — precipitated from a universal ocean, in order, as Werner's Freiberg school taught
— or raised by **fire**, as Hutton argued from the granite veins at Glen Tilt and the unconformity at
Siccar Point, concluding that the earth was an engine of subterranean heat with *"no vestige of a
beginning, no prospect of an end."* It was the defining controversy of late-eighteenth-century geology
and it was fought, at bottom, over which of two agents is primary.

**The Pyrewind Breaker is a Vulcanist argument and its counter is a Neptunist one.** *"Thaloré-worked
water blunts the blast outright."* The page's own Weakness and Counterplay put fire and water on
opposite sides of the question, and the practitioner who uses this working is asserting, with a
twenty-metre demonstration, which agent is primary.

**The productive misreading.** A Vulcanist school reads the Breaker as settling it: fire raises,
water merely lies about. They will teach that the Thaloré counter is a **suppression** rather than a
defeat — a temporary damping to be pushed through with more output — and they will train repeated
bursts on the reasoning that the fire is the primary agent and will win on the second attempt.

**What kills them is arithmetic that Neptunism happens to own.** Water's specific heat is
**4.18 kJ/(kg·K)** and its latent heat of vaporisation **2,260 kJ/kg**, so absorbing the whole 62 GJ
thermal content of the sphere takes about **25 tonnes** of water boiled — a modest quantity for a
current whose Family is fluid dynamics, and nothing at all next to a river. Meanwhile the fire's
ceiling is fixed by the **oxygen in the room** at about 120 GJ, and no amount of conviction adds
oxygen. And the repeated bursts the school prescribes are the exact behaviour Exuroth's register
forbids: *"Cycle too fast without the tempering interval and the lattice arrives hard, brittle, and
split along its own thermal gradients."* **Hutton won the general question and Werner's students win
this particular fight**, which is the most enjoyable shape a wrong school can have.

---

## 3 · Mechanism (the effect)

**Glyph (proposed; the page names none).** `[Hael]` **Flame** · Root · Urion as the governing form —
the Index lists it among the fifteen unclassified Roots and says why that matters: *"None of these
names a law. Each names a **kind of limit**, applicable to any law at all."* Laid across `[Ae]`
**Vastness** · Root · Zhaeren for the twenty metres. `[Kael]` **Ruin** · Root · Uurgath is the
alternative and would file the working under *what may be brought down* rather than under *where the
flame front is allowed to be*; the page's own emphasis on an unsteerable, unrecallable release argues
for it. All from the thirty unclassified forms in
`wiki/The Magic System/The Master Glyph Index — 136 Attested Forms.md`.
*Filing decision, not canon — Isaac's ruling.*

**What boundary moves.** **Where the reaction front is permitted to be, and how fast it is permitted
to run.** Not the fuel, not the oxygen, not the pressure: the front's position and velocity. Pin those
and Cataclysm's ordinary law takes over — a front that is permitted to accelerate accelerates, and
past threshold it couples to a shock, and thereafter the radius goes as the cube root of the yield
because that is what blast does. **Nobody decides the shock.** The Index's rule: *"It moves a limit,
and the law does what it has always done on the far side of the new limit."*

**What the law then does on its own.** All of it, and every limit on the page falls out — including
the ones the page states and the ones it does not.

It cannot be steered, throttled or called back, because a reaction front carrying its own oxidiser has
no throttle; the register says so of Tarturon and it is truer still of a front already propagating.
It cannot be aimed finer than its radius, because a sphere has no aim. The shock outruns the flame in
the open and arrives with it under confinement, because those are the two regimes DDT sits between.
It overloads weak shields **on contact** rather than at range, because overpressure falls with
distance and a reflected pulse at a surface is worse than the incident one. It is blunted by water,
because water's heat capacity and latent heat are enormous against the sphere's 62 GJ. It is blunted
by oxygen-poor air, because 120 GJ is all the chemistry available. And **it hurts the caster**,
because Overchannel at A-Grade carries Backlash risk that *"no Path"* protects against, and because a
caster standing at the origin of a confined burst receives *"the sum of the wave and its
reflection."*

**The Four Glyph Roles** (`wiki/The Magic System/The Four Crafts.md`). Authorization: the declaration,
or the release call. Boundary: twenty metres. Direction: outward. **Sealing: nothing.** The page says
so plainly — *"committing to a burst with no further input once it starts"* — and the Craft page's
warning is the page's own Limitation restated: *"Sealing failing produces a working that does not
stop, because the law goes on obeying itself after the operator's attention has left the room."*
**A Pyrewind Breaker has no Seal by design, which is why it cannot be recalled, and the working's
honesty about that is its best feature.**

**Law V check, and it closes with the vector named.** Stage VI sits below Refraction, so an external
anchor is required: *"Below Stage VII, Refraction, a working requires voice, hand, ink or blood."* The
page supplies the **Spoken** vector explicitly and in the Accord register — *"Ars Vocis; declared"* —
so the gate closes, **and the consequence attaches**: *"Spoken · Voice into air. The default. Loud,
legible, and it tells everyone within earshot exactly which Wellspring you just invoked."* The
Counterplay route *"Put a hand over his mouth"* is therefore live against this working and not against
most of the others in this batch. **That is a real and unusual vulnerability and it is the price of a
Stage VI ceiling.**

**Failure mode — Structural fault, with a Boundary fault as its second.** *"The Crystal could not hold
what the boundary permitted. Overchannel, Backlash, Fracture. The working succeeds and the
practitioner does not"* (`Two Sets of Books` §VII). Overchannel at A-Grade, no Path protection, and
Exuroth's quench cracking when the interval is skipped: this is the page's Cost with the fault named.
The **Boundary** fault is the reflected shock — the condition established imprecisely in a confined
room, the law running somewhere unintended, and the unintended place is where the caster is standing.

**What the target sees and feels.** *"A vortex of white-orange flame coils like a living serpent
before it bursts. A tearing roar follows."* And then, in order, three things that do not arrive
together.

First the warning, and it is physical rather than visual: *"Anyone caught near it reports hair rising,
chest pressure and the taste of metal in the air, just before impact."* Hair rising is a static
field; chest pressure is a pressure gradient arriving ahead of the front; the taste of metal is what
ozone and hot oxides taste like. **All three are real precursors of a fast-rising overpressure and all
three are perceptible before anything is felt as heat.**

Then the shock, because in the open it travels at 343 m/s and the flame does not. Twenty metres is
**58 milliseconds** of transit for the shock and, at a few metres per second of flame speed, **seconds**
for the fire. Bodies are knocked back or down and weak shields *"overloaded on contact"* before the
burning begins.

Then the fire, filling the volume it is allowed to fill, consuming whatever oxygen is in reach and
stopping when that runs out.

And the caster is at the centre of all three, with no way to stop any of it, in a room whose walls
decide whether the shock comes back.

**What bleeds, at the stated efficiency.** No practitioner, so η is read off the Stage: Stage VI ⇒
Tier of Standing 5 · Expert (Part Five) ⇒ **η 0.50–0.60** (Part Nineteen). **Forty to fifty percent of
every expenditure leaves as heat, sound and structural bleed** — and on this working the bleed is not a
loss, it is the second half of the effect: heat and sound *are* what the technique delivers. **The
Pyrewind Breaker is the one working in the batch whose inefficiency is indistinguishable from its
output**, which is a genuinely useful observation and the reason a low-efficiency practitioner is a
better candidate for it than a high-efficiency one.

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| EU spent | `null` | No page figure; no formula converts a Stage into EU. `SA-GAP-EU-FORMULA`. |
| Cost in kind | **high Aether burn** + **risk of internal overheating, worse on repetition** | Page. **Mechanically: Overchannel Backlash risk above C-Grade with "no Path providing structural protection" (Part Seven), plus Exuroth's quench cracking when the tempering interval is skipped.** |
| Flux Density | `null` | No AU/s figure, no card, no named practitioner. |
| η | **0.50–0.60** (derived) | Stage VI ⇒ Tier 5 · Expert (Part Five) ⇒ η band (Part Nineteen). |
| AU/s | `null` | Needs Flux Density. |
| Duration | **under 1 s** | Page, "1 turn (instant burst)". **One of only two pages in the batch that does not need the turn-length ruling.** |
| Radius | **20 m** | Page. Sphere **3.35×10⁴ m³**; air mass **4.1×10⁴ kg.** |
| Stated yield | **20–100 GN · 46 GJ – 4.184 TJ · 11–1,000 t TNT** | Page, quoting Part Eleven's A row exactly. |
| **Radius implied by that yield** | **89 m** at the floor · **400 m** at the ceiling | Hopkinson–Cranz, Z ≈ 4 m·kg^(−1/3) for 34 kPa. **Four to twenty times the stated radius.** `SA-NUM-PYREWIND-RADIUS-VS-YIELD`. |
| **Yield implied by the stated radius** | **125 kg TNT = 5.2×10⁸ J = C-Grade** | W = (20/4)³. **Two Grades below the requirement.** |
| **Thermal content of the sphere** | **≈62 GJ** | 4.1×10⁴ kg × 1,005 J/(kg·K) × 1,500 K. **Just inside A-Grade's 46 GJ floor — the fire closes.** |
| **Chemical ceiling from available O₂** | **≈120 GJ** | 9.4×10³ kg O₂ ÷ 3.4 kg O₂ per kg fuel × 43 MJ/kg. **A hard cap at 2.9 % of the A-Grade top, and the physical content of Caloria's "oxygen-poor air" suppression.** |
| Flame vs shock transit over 20 m | shock **58 ms** · flame **seconds** | 20 m ÷ 343 m/s; 20 m ÷ a few m/s. **This is the page's "What nobody knows", answered.** |
| DDT figures | laminar burning velocity **≈0.4 m/s** · CJ velocity **≈1,800 m/s** · CJ overpressure **≈18 bar** | Cataclysm's stated analogue. **DDT requires confinement and turbulence, which an open outward burst does not supply.** `SA-EM-PYREWIND-DETONATES-IN-THE-OPEN`. |
| Reflected-shock amplification | **up to ≈8×** incident overpressure | Cataclysm's own register failure, with the caster at the origin. **Not on the page, and the page's Cinerion counter creates the geometry.** |
| Water needed to absorb the thermal load | **≈25 tonnes boiled** | 62 GJ ÷ (4.18 kJ/(kg·K) × 80 K + 2,260 kJ/kg). **Why the Thaloré counter works and how much of it is needed.** |
| Bleed | **40–50 %** | 1 − η. **Indistinguishable from the output, since the output is heat and sound.** |
| Minimum Stage | **VI · Glory** | Page. Max Grade A, ceiling 400 (Part Five). |
| Tier of Standing | **5 · Expert** | Part Five. |
| Grade required | **A** (276–400) | Page. **At Stage VI's Max Grade exactly, so the working sits at its own ceiling with no headroom.** |
| Ardency **Overchannel** | **✓ open, with unavoidable risk** | "open, carrying inherent Overflow risk above D-Grade and Backlash risk above C, **with no Path providing structural protection**; recovery of rebound as usable output requires Body Path at Stage V to exceed B" (Part Seven). A-Grade exceeds C. **The risk is the Cost.** |
| Ardency **Cascade** | **✗ FAIL** | "requires **Attraction Path at Stage IV to exceed B for spread**, Spirit Path at Stage V to exceed S for range" (Part Seven). A exceeds B, and the whole working is spread. **The page's Path gate is "Spirit, Body" — no Attraction.** `SA-NUM-PYREWIND-PATHGATE`. |
| Dominion **Radius** (page: Cataclysm's "Expansion") | **✓ on the line** | Merge Ledger: Expansion → Radius. "requires Attraction Path at Stage V to exceed A, **Stage VI to exceed A for partial projection outward**" (Part Seven). At exactly A neither threshold is crossed, so it closes — **by one Grade bracket and no more.** |
| Tempering **Overflow** | **✓ open, with risk** | "open, with inherent structural risk above B" (Part Seven). |
| Vitality **Threshold** | **✓ closes** | "requires Body Path at Stage IV to exceed B" (Part Seven). Body declared. |
| Path gate | **Spirit, Body** | Page. Carries Threshold and the Overchannel risk; **fails Cascade's Attraction gate**, which is the Sub-Stat that makes it a burst rather than a jet. |
| Craft, and a fault line | **Spellcraft, *Ars Vocis*, declared or chanted** | Page. The Spoken vector closes Law V at Stage VI ✓. **But `The Four Crafts` ratifies Chantcraft as its own craft and says "It scales with throats. Everything above trivial requires more than one voice."** A solo release call is a shout, not *Ars Cantus*. `SA-CROSS-PYREWIND-CHANT-OR-SHOUT`. |
| Counter currents, as named | **Thaloré as water, Cinerion as rust** | Page. **The register's Thaloré is hydrostatic pressure and emotional weight, not water; the register's Cinerion is char and ash, not rust.** `SA-CROSS-PYREWIND-COUNTER-CURRENTS`. |
| Starvation margin | `null` | No cost figure and no reserve figure. `SA-GAP-EU-FORMULA`. |
| Developmental Tier | **Harmonic** | Stage VI (Part Twenty-One). |
| Crystal State | `null` | No practitioner named. |
| Aetheric Density check | **cannot be run** | No numeric scale exists. `SA-GAP-AETHERIC-DENSITY`. |

**Does the physics close against the stratal account?** **The fire closes and the blast does not.** The
thermal content of the stated sphere is 62 GJ against an A-Grade floor of 46 GJ, which is as neat a
match as anything in this batch, and the oxygen in the room supplies a hard 120 GJ ceiling the page
could have used as a stated limit. The caster's cost is derivable from Part Seven rather than asserted:
Overchannel above C carries Backlash risk that no Path protects against. The page's own open question
is answered by its own Wellspring's Core Law. **But the radius and the yield are not compatible.**
Blast scales as the cube root of yield — a rule written into Cataclysm's Core Law, not merely into
real-world ballistics — and 11 tonnes of TNT reaches 89 metres while the page claims 20. Either the
radius is a C-Grade radius or the yield is an A-Grade yield; both cannot stand.

**Conflicts logged from this page:** `SA-NUM-PYREWIND-RADIUS-VS-YIELD`,
`SA-EM-PYREWIND-DETONATES-IN-THE-OPEN`, `SA-CROSS-PYREWIND-COUNTER-CURRENTS`,
`SA-NUM-PYREWIND-PATHGATE`, `SA-CROSS-PYREWIND-CHANT-OR-SHOUT`, `SA-GAP-EU-FORMULA`,
`SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR`.

---

## 5 · Counterplay and the challenge

**The fairness check** (`.claude/skills/wotr-write/references/fair-play.md`).

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **pass, and it is derivable rather than asserted** | *"A heavy Aether burn in the caster, with a real risk of internal overheating if the working is pushed or repeated too soon."* Part Seven supplies the mechanism: Ardency Overchannel above C-Grade carries Backlash risk with **"no Path providing structural protection"**, and Exuroth's register failure names the repetition clause exactly — cycle without the tempering interval and the lattice splits along its own gradients. Unpriced in EU (`SA-GAP-EU-FORMULA`). |
| Stated limits | **pass, and unusually honestly** | 20 m; under a second; **it cannot be steered, throttled, aimed finer than its radius, or called back once declared.** A working with no Seal is a working that has told you its worst property. |
| Something beats it | **pass, four routes and none of them requires a peer** | Thaloré-worked water; a Cinerion barrier that redirects; a Verdantia ward that muffles spread; and the Family terrain answer. Abyssal-aligned entities take the fire and not the shock, which is a partial. |
| It has a tell | **pass, and it is the best-written tell in the batch** | It is **spoken** (*Ars Vocis*), so everyone in earshot learns which Wellspring was invoked; then *"a vortex of white-orange flame coils like a living serpent before it bursts"*; then **hair rising, chest pressure and the taste of metal**, which are real overpressure precursors perceptible before any heat. Three tells in ascending order of lateness. |
| Numbers in band | **FAIL, and by orders of magnitude** | The 20 m radius and the 11–1,000 t yield are incompatible: the floor of the stated band reaches 89 m and the top reaches 400 m, while 20 m corresponds to 125 kg of TNT, which is C-Grade (`SA-NUM-PYREWIND-RADIUS-VS-YIELD`). **Ardency Cascade needs Attraction Path for spread** and the page declares Spirit and Body (`SA-NUM-PYREWIND-PATHGATE`). The thermal half, by contrast, closes at 62 GJ against a 46 GJ floor. |

**The Counterplay routes that work**
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Deny the field — and the register names this one outright.** *"Choose the ground by Family …
  **Caloria fails in thermal equilibrium, saturated cold, and oxygen-poor air.**"* For this working
  the oxygen clause is not a modifier, it is a hard cap: 120 GJ is everything a 20 m sphere of air can
  burn, and less air means proportionally less. A cellar, a flooded street, a snowfield, a sealed
  vault. **This is a counter a commander can pick off a single line of doctrine without reading any
  other page.**
- **Break the boundary — put a hand over his mouth, and this is the rare working where that is
  live.** *"Below Refraction a working requires an external anchor: voice, hand, ink or blood. Take
  the anchor and the sentence does not complete … **Put a hand over his mouth and a spoken one
  is.**"* The page files the Craft as *Ars Vocis, declared*, at Stage VI, which is below Refraction.
  **Of the four Stage VI–VII workings in this batch, this is the only one whose anchor is explicitly
  a voice**, and that makes a grapple a complete answer.
- **Deny the field — water, and the quantity is knowable.** *"Thaloré-worked water blunts the blast
  outright."* Absorbing the sphere's 62 GJ takes about twenty-five tonnes of water boiled, which is
  nothing to a river and a great deal to a bucket. **A player who works that out knows the difference
  between standing behind a Thaloré working and standing in the rain.**
- **Break the man — Rigidity, and the burst's own Limitation is the handle.** *"Present him with the
  situation his own law handles worst and he will handle it that way regardless."* His law handles
  everything the same way: a twenty-metre sphere he cannot steer, throttle or recall, centred on
  himself. **Put something he needs to keep inside twenty metres** — a hostage, a wounded man, a
  standard, a door he must not bring down — and he either does not fire or fires and pays for it.
- **Break the boundary — make the room reflect.** Cataclysm's own failure: *"In confinement the shock
  returns along its own path, and the practitioner standing at the origin receives the sum of the wave
  and its reflection."* Up to eight times the incident overpressure in the strong-shock limit. **Fight
  him in a corridor and let him fire.** The page does not know this about itself, and its own
  suggested Cinerion counter — a barrier that *redirects* — is the geometry that produces it.
- **Break the man — Exhaustion, with the register's caveat noted.** *"Waiting for the cost"* is
  normally a plan to be killed by a tired man. Here the cost has a stated repetition clause and a
  register-level mechanism (the tempering interval), which makes forcing a second burst inside the
  interval a real move rather than a hope.

**The tell, stated plainly.** He says it aloud, and everybody who has studied knows what Caloria
sounds like. A vortex of white-orange flame coils on itself like something alive. Then hair stands up,
the chest tightens, and the air tastes of metal — and those three arrive **before** the heat, because
the pressure front is travelling at three hundred and forty-three metres a second and the fire is not.

**The lookup trail.**

1. `wiki/Techniques/Pyrewind Breaker.md` — the Limit (*"cannot be steered, throttled or called
   back"*), the Weakness (Thaloré, a Cinerion rust-barrier), the Counterplay (Verdantia, the Abyssal
   partial), and the *"What nobody knows"* about the shockwave outrunning the flame.
2. `wiki/The Eight Families & the Sixty Wellsprings/Caloria — Thermodynamics.md` — **Cataclysm's Core
   Law**, which answers the page's own open question in one sentence (*"faster than sound in the
   unreacted medium"*) and states the cube-root scaling the page's radius breaks; and **Cataclysm's
   failure**, which is the caster receiving his own reflected shock. **Exuroth's failure** is the
   repetition clause. Also **Cinerion**, which is char and ash and not rust.
3. `wiki/The Eight Families & the Sixty Wellsprings/Fluxia — Fluid Dynamics.md` — **Thaloré**, which
   is hydrostatic pressure and emotional weight rather than a water current, so a reader checking the
   page's own counter finds the counter mis-named.
4. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — **"Choose the ground by Family"**
   (the oxygen clause), and **"Interrupt the chain"** (*"Put a hand over his mouth"*), which is live
   here and dead on most of this batch.
5. `wiki/The Magic System/The Four Crafts.md` — **Settled Position I (Law V)** and the **Spoken
   vector**, for why the mouth is a target at Stage VI; and **Chantcraft**, for why *"a chant carrying
   the working"* is a claim with a craft attached that requires more than one throat.
6. `wiki/Fracture of Worlds — The Living System/III. Physical Force (Part Eleven).md` — the A-Grade
   Strike Force row, and the **Aether-Physics Fusion Rule**. **A reader who takes 11 tonnes of TNT and
   asks how far a 5 psi overpressure reaches has found the page's central problem with one cube
   root.**
7. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`
   — **Part Seven**, for Ardency Overchannel's unprotectable Backlash risk (which is the Cost) and
   Ardency Cascade's Attraction gate (which the page's Path line misses).
8. `wiki/The Magic System/The Core Vocabulary.md` §II — **Aetheric Saturation**, for what repeating
   this inside the same twenty metres does to *"everyone exposed, including the person who caused
   it."*

**Conflicts added by this section:** none beyond those above. `SA-GAP-COUNTERPLAY-TERRAIN` does
**not** apply: Caloria has a failure-terrain line in the Counterplay register, and for this working it
is not merely a modifier on η but a hard ceiling on the chemistry.
