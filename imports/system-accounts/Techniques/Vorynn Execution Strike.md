---
page: wiki/Techniques/Vorynn Execution Strike.md
section: Techniques
practitioner: Draven Kael Vorrick
card: wiki/Volume I — Character Cards/Draven Kael Vorrick · The Beast Slayer.md
wellspring: Vohrin (primary) · Tenebra (secondary) · Cinerion (secondary)
family: Caloria (Vohrin, Cinerion) · Limina (Tenebra)
stage_floor: VI
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · Vorynn Execution Strike

## 1 · Physical account (physics)

**The phenomenon in plain words.** A hunter touches something and it goes rigid for a second or two. It is
not knocked down and not cut open; it simply stops being able to answer, and the follow-through happens
to a thing that cannot get out of the way.

**The real phenomenon.** **A contact heat sink**, which the page names correctly, and which cannot do what
the page asks of it in the time the page allows — **thermal diffusion in tissue is a square-root law and
one second of it is half a millimetre deep.** Underneath that sits the effect the working actually has and
the page half-states: **cold destroys a target's ability to yield**, and yielding is most of what a
defence is.

**(a) The heat-sink half is correctly described and correctly limited by the page's own sentence.** The
page: *"that sink pulls thermal energy out of the target's tissue **far faster than the tissue's own
conduction can redistribute it**"* (`:44`). That is exactly right and it is the constraint rather than the
achievement. **A surface sink can only cool what conduction brings to it**, and conduction in soft tissue
is slow. The thermal diffusivity of soft tissue is **α ≈ 1.4 × 10⁻⁷ m²/s**, and the depth a thermal front
reaches in time *t* goes as **L ≈ √(αt)**:

| Contact time | Depth cooled |
|---|---|
| **1 s** | **0.37 mm** |
| **2 s** | **0.53 mm** |
| 1 minute | 2.9 mm |
| **5 hours** | **5 cm** |

**Inverted: to reach a muscle belly 5 cm down takes L²/α = 0.0025 / 1.4 × 10⁻⁷ ≈ 17,900 s, about five
hours.** This is not a theoretical nicety — it is the operating constraint of clinical cryoablation, where
a probe held at −180 °C takes ten to fifteen minutes to grow an iceball a few centimetres across, and the
iceball radius grows as √t for exactly this reason.

**So the page's *"ordered crystallisation blocking Essence pathways at the wound"* is achievable and its
*"locks the local muscle chains"* is not, by two orders of magnitude in depth** — a muscle chain is
centimetres deep and a one-second contact reaches half a millimetre (`SA-PHYS-VORYNN-FREEZE-DEPTH`).
Pulling harder does not help: a sink faster than conduction simply freezes the surface harder while the
interior stays warm, because the bottleneck is the tissue's own transport and not the sink's appetite.

**(b) And the physiology the page wants is real, is fast, and does not require freezing anything.** Two
separate cold effects deliver what the page describes, both within reach of a surface sink:

**Nerve conduction block.** Peripheral nerve conduction velocity falls by roughly **1.5–2 m/s per degree**
of cooling, and myelinated A-fibres **fail outright below about 7–10 °C.** This is established physiology
and the basis of cryoneurolysis. Crucially, **many nerves run shallow** — the ulnar at the elbow is three
to five millimetres deep, the common peroneal at the fibular head similar — so a surface sink can reach
block temperature at a nerve without reaching it at a muscle.

**Cold contracture, which is the better half and explains why the page says rigid rather than limp.**
In muscle, cooling slows *relaxation* far more than it slows *contraction*, because relaxation is active:
it depends on the SERCA pump clearing calcium back into the sarcoplasmic reticulum, and SERCA's activity
has a high temperature coefficient (**Q₁₀ ≈ 2.5–3**), so **relaxation rate roughly halves for every seven
to ten degrees of cooling.** A muscle that can still be activated and cannot let go is a muscle that
locks. **The page's Target Response — *"Kinetic defences seize rigid rather than absorbing or redirecting
the blow"* — is the correct outcome and rigidity rather than flaccidity is the correct sign**, and neither
follows from freezing. It follows from a pump getting slow.

**(c) What that actually does to a fight, which is larger than the page claims for it.** A trained
defender does not absorb an impact by being hard. He absorbs it by **giving** — by lengthening the
deceleration distance, which is the only variable in the impact equation that is free. For a strike
delivering kinetic energy E stopped over a distance d, the mean force is **F = E/d**. A man who yields
30 cm takes half the force of a man who yields 15 cm, and a quarter of the force of one who yields 7.5 cm.

**Cold removes the yielding.** A locked muscle cannot do negative work; a chilled tendon is stiffer; a
cooled limb cannot be steered out of line. **So the same blow, against the same body, delivers two to four
times the force for no extra energy at all**, purely because the stopping distance collapsed. That is a
large, real, cheap effect. It is also exactly what the page's Effect line claims — *"The strike does not
need to be hard to be final"* — and it is not what the page's Numerical Effect gives it.

**(d) The Numerical Effect contradicts the Effect line, by nine orders of magnitude.** *"Strike Force is
Draven's own attested Ardency 320, A-Grade: 20 to 100 GN peak, **46 GJ to 4.184 TJ** yield, city-block
scale, with this technique **run near the top of that sustainable range**"* (`:45`).

**4.184 TJ is one kiloton of TNT.** Delivered by a fist, to one person, in order to hold him still for a
second and a half. Meanwhile the stated cold effect, priced honestly, is tiny: freezing the tissue a
surface sink can actually reach — a fist-sized contact patch of 100 cm² to a depth of 0.5 mm, about
**5 grams** — costs roughly **340 J/g** (sensible heat to 0 °C at c ≈ 3.5 J/(g·K) plus the latent heat of
the water fraction), so **about 1.7 kJ.**

**The page's own two lines are 2.5 × 10⁹ apart**: *"does not need to be hard to be final"* against a
number that is city-block scale by the page's own gloss (`SA-NUM-VORYNN-4TJ-VS-NOT-HARD`). And the
kiloton makes the rest of the page moot — a target that has received 4 TJ is not locked for one to two
seconds, it is weather.

**(e) Where the heat goes, which is a real limit and a findable one.** A heat sink must reject. The page
says where: *"a controlled, directional heat-sink **running through Draven's own ignited musculature**."*
So every joule pulled out of the target arrives in him.

- Freezing **5 g** (the honest figure, §1d) puts **1.7 kJ** into a 100 kg man: **0.005 K.** Nothing.
- Freezing **1 kg** puts **340 kJ** in: **ΔT = 340,000 / (100 × 3,500) ≈ 1 K.**
- Freezing **3 kg** puts **1.0 MJ** in: **≈3 K**, taking a core temperature from 37 °C to **40 °C**, which
  is the threshold of heat illness.

**So the working has a hard ceiling nobody has written down: he can take about three kilograms of another
person to freezing before he cooks himself**, and the ceiling is on *quantity frozen*, not on uses. It is
also the reason the page's stated counter works: *"Reintroduce heat faster than Vohrin can pull it"*
(`:22`) does not overload the sink, **it removes the gradient the sink runs on.**

**Energy budget, stated.** Extracted: **≈1.7 kJ** for the tissue a one-to-two-second contact can actually
reach; **≈340 kJ per kilogram** for anything deeper. Delivered as impact: the page says **46 GJ –
4.184 TJ** and §1(d) says its own Effect line disagrees. Rejected: into the practitioner's own
musculature, at about **1 K of core temperature per kilogram frozen.** Where the joules were: the
target's, for the cold — **this is one of the few workings in the batch where the energy provenance is
unambiguous and the direction of flow is the whole mechanism.** Fault class by `Two Sets of Books` §VII:
**Structural fault** — *"The Crystal could not hold what the boundary permitted… The working succeeds and
the practitioner does not"* — which is the page's own Cost line, *"Every use tears fibre along the
ignition path."*

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** **Caloria**, *"**Spirit** (Fire/Heat/Cold) · **Medium** (Light)"*, favoured by
*"Steep thermal gradients, combustible atmosphere, geothermal ground"*, suppressed by *"**Thermal
equilibrium**, saturated cold, oxygen-poor air"*. **Limina**, *"**Spirit** primary"*, favoured by
*"Darkness, silence, Aether-thin ground, ruins"*, suppressed by *"Saturated Aether, crowd density, active
Domains"* (`wiki/The Magic System/The Eight Families & the Sixty Wellsprings.md`). *"Terrain is not
flavour. It is a modifier on η."*

**Caloria's favoured row is the mechanism restated as weather.** *"Steep thermal gradients"* is what a heat
engine and a heat sink both require, and §1(e) says why: **a sink with nowhere to reject to is not a sink.**
And the suppression row is the page's own counter, printed in the coupling table: *"saturated cold"* — a
room already at the temperature he wants the target to be at offers him nothing to take.

**And there is a second, colder joke in the same row.** The working is a cold technique whose Family fails
in *"saturated cold"*. **The better Draven's previous minute has gone, the worse his next one goes**, in
any enclosed space, because he has been raising the ambient floor toward himself with every use.

**Saturation.** Three currents named on this page, four on the card, plus *"Three additional Wellsprings
networked along predatory lines"* — and the card flags its own arithmetic: *"which would make his
harmonisation total six — **above his Tempering Capacity at this Stage, and worth flagging**"* (card
`:49`).

**Wellspring stratum — Vohrin, and it is not in the register.** The page's primary current, and the card's
(*"**Vohrin** · Caloria. **The cold law.** Heat's absence, held as a discipline rather than suffered as a
condition"*, card `:45`), **is not among the sixty.** It does appear in canon, as a **Titan**
(`SA-UNATT-VOHRIN`). Four technique pages and one card agree with each other and all five disagree with
the register and the Titans page. So this account can quote the card's gloss and cannot quote a Core Law,
because there is not one.

**What can be said is that the gloss is doing real work.** *"Heat's absence, held as a discipline rather
than suffered as a condition"* is a precise statement of the thermodynamic position: cold is not a
substance and cannot be emitted, so a cold working must be an **acceptance** of heat rather than a
projection of anything — which is why §1(e)'s ceiling exists and why it lands on him.

**Wellspring stratum — Cinerion, *The Ash Veil*, Caloria, Thermodynamics.** Core Law, verbatim:

> **Analogue** · Pyrolytic char and its catalytic residue. Particulate optical depth.
> **Mechanism** · What survives a fire is not waste. Char is a high-surface-area carbon scaffold that
> catalyses further reaction… Cinerion retunes the Shell to **metabolize its own combustion products,
> harvesting from expenditure what other practitioners simply vent.**
> **Stat Effect** · Strengthens Tempering Conversion, Harmonics Recovery.
> **Failure** · Fouling. Accumulated residue eventually coats the conduit rather than feeding it, and
> recovery rate collapses precisely when the practitioner has spent the most.

**Cinerion is the answer to §1(e) and the page has it on the sheet without using it.** The working's
binding constraint is that the heat it takes has nowhere to go but him, and Cinerion is the current whose
entire function is *"harvesting from expenditure what other practitioners simply vent."* The page uses
Cinerion only for *"remnants"* and for *"densifying the cold past what Vohrin alone would produce"*
(`:44`) — same-Family compounding, which the card also states. **The load-bearing use is the other one: a
Shell that metabolises its own waste heat is a Shell that can run a sink for longer before its owner
cooks.** And the Failure that comes with it is the correct long-term cost: *"recovery rate collapses
precisely when the practitioner has spent the most."*

**Wellspring stratum — Tenebra, *The Hidden Shadow*, Limina.** Core Law, verbatim:

> **Analogue** · Signal-to-noise reduction. Absorptive coating and faceted return geometry.
> **Stat Effect** · Strengthens Dexterity Silence, Harmonics Suppression, Dominion Sense.
> **Failure** · Aspect dependence.

Its role here is the approach, not the strike — *"closing to contact under Tenebra's signal-reduction
cover"* (`:42`) — which is the Tenebra Ambush Art doing its job one page over, and the account for that
page prices what the closing actually costs in noise.

**The Sub-Stat list is all four the card's own attested peaks, and the page says so.** *"Ardency
Penetration (358), Dexterity Silence (386) and Celerity (344), Vitality Tolerance (400, at ceiling)… All
four are Draven's own attested Sub-Stat Peaks, not freshly assigned"* (`:59`). **Checked against the card:
all four are there, at those numbers.** That is honest sourcing and it is worth recording, because it is
not what most pages in this batch do.

**Which of the Four Theories.** **Debt**, in the plainest form the batch has produced: this is the only
page in twenty-eight that prices its cost as a **fraction of reserve** — *"his own count puts the Essence
toll near a fifth of what he is carrying per use"* (`:20`). A working with a stated draw against a stated
balance is a working with a ledger. **Residue** runs alongside through Cinerion.

**Essence stratum.** Crystal layer: the **Aether Shell**, *"Class III · Resonant. Channels Aether into
hyper-dense muscular ignition and aggressive kinetic force, **using Frost Essence for systematic
slowing**"* (card `:34`) — the working is that clause used at contact range. Developmental Tier
**Harmonic** (Stage VI, Part Twenty-One). Tier of Standing **5 · Expert**, η band **0.60–0.70**
(Part Nineteen as corrected by **R44-4**); card η *"~0.55"* — **0.05 below the floor**, and
lawfully so: `C-062` was **ruled 2026-09-26** (Isaac, rung **I-2**), the card
governing and the corrected row standing as a typical range for him. Crystal State *"Refined"*. **The invoice:** a fifth of the reserve, fibre torn
along the ignition path, and — the part nobody has costed — every joule taken out of the target arriving
in his own musculature.

**The lens: frigorific rays, and the academy that focused cold with a mirror.** Pierre Gassendi,
*Syntagma Philosophicum* (1658), held that cold was a positive thing: **frigorific atoms**, angular and
sluggish, emitted by cold bodies as heat-atoms were emitted by hot ones. The Accademia del Cimento tested
it in Florence and published the result in the *Saggi di naturali esperienze* (1667): they set a block of
ice at the focus of a concave mirror, put a thermometer at the other focus, **and the thermometer fell.**
Cold, apparently, could be reflected and concentrated like light.

**The experiment was sound, the result was real, and the theory was wrong.** Radiative exchange runs both
ways; the thermometer was losing more to the cold block than it gained back, and the mirror was focusing a
*deficit*. It took the recognition that heat flows and cold does not exist as a flow to make sense of an
observation everybody could repeat. **And that distinction is the entire physics of this technique.**
Vohrin's gloss — *"heat's absence, held as a discipline rather than suffered as a condition"* — is the
frigorific doctrine stated in the only form that survives the second law: not something you emit,
something you accept.

**The productive misreading, and what it kills.** Take the Florentine result at face value and the
doctrine is irresistible, because **it works**. Cold can be aimed. So a school trains to project: to reach
further, to cool at a distance, to strike without contact, on the theory that the practitioner who has the
most frigorific capacity has the longest reach. They build focusing rigs. They measure a man by the range
at which he can drop a thermometer.

**The second law kills them and it kills them by promotion.** There is no cold to emit. There is only heat
to accept, and §1(e) prices what accepting it costs: **every kilogram brought to freezing deposits about
340 kJ in whoever pulled it, which is roughly one degree of core temperature.** Three kilograms is three
degrees, and three degrees is forty and heat illness. So the better a frigorific adept becomes — the more
he takes, the further he reaches, the more of a target he claims — **the more heat he has imported into
himself with nowhere to put it.** The school's masters die hot. They die of fever, in winter, at the end
of their best engagements, and every apprentice records it as a mystery because the man was, by every
observation anyone made, the coldest thing in the room.

---

## 3 · Mechanism (the effect)

**The glyph, proposed.** `[RenB]` **Boundary** (Root · Zhaeren) for the thermal condition and `[Lk]`
**Lock** (Counter · Thalen) for the seizure — both from the thirty mirrored entries, both filings under
the Index's Standing Note (*"Assignment is decided after the phenomenon, never before, and it is a filing
decision rather than a generative one"*), neither canon until ruled (`SA-GAP-GLYPH-MIRROR`). `[Lk]` is one
of only two Counter forms in the whole Index and its definition is apt — *"**Lock** occupies a limit so no
other limit can be set there"* — because what this working takes from a defender is his ability to set the
limit himself.

**What boundary moves.** Not the target's heat and not his strength. **The boundary that moves is where
the thermal gradient at the point of contact is permitted to sit.** Two bodies touching already exchange
heat; the direction and rate are set entirely by the difference between them and by the transport
properties of what is in between. The condition moves one end of that difference, and **Fourier's law then
runs without further instruction**, because it always has been running. The Index's formulation is exact:
*"A glyph creates nothing and carries no power… It moves a limit, and the law does what it has always done
on the far side of the new limit."*

**What the law then does on its own — and the first thing it does is refuse to go deep.** The gradient at
the skin can be made as steep as you like; **the depth the cooling reaches is set by the target's own
tissue**, and √(αt) is not negotiable by anybody (§1a). So within the one to two seconds the page allows,
the thermal effect is confined to the outermost half-millimetre and to whatever nerve happens to run
shallow beneath it.

**And that is enough, because what it takes is not the target's strength but his compliance.** Cooled
muscle cannot relax at the rate it contracts — SERCA has a Q₁₀ near three, so the pump slows faster than
anything else does (§1b) — and a muscle that cannot let go cannot lengthen under load. **Lengthening under
load is the whole of a defence.** A guard that yields thirty centimetres halves the force of what it
stops; a guard that has been locked yields nothing, and the same blow arrives two to four times harder
without a single extra joule behind it (§1c). *"Kinetic defences seize rigid rather than absorbing or
redirecting the blow"* is correct, and the operative word in it is **absorbing**.

**The Essence half runs in parallel and the page states it well.** *"Ordered crystallisation blocking
Essence pathways at the wound"* — a lattice forming where a flow was passing, in the depth the cold can
actually reach, which is the depth a wound is anyway.

**The failure modes.** **Depth**, which is §1(a) and which the page's own timing fixes at half a
millimetre. **Reheating**, which is the page's stated counter and which works by removing the gradient
rather than by beating the sink. **Self-loading**, which is §1(e) and which nobody has written down: the
heat has one place to go and it is him. **Fouling**, Cinerion's, for the same reason as on the Reprisal —
*"recovery rate collapses precisely when the practitioner has spent the most."* And **the reserve**, which
is the only cost in this batch stated as a fraction of a balance and which therefore has a computable
floor (§4).

**What the target sees and feels.** Nothing at range, because the approach is Tenebra's and is the other
page's problem. At contact there is a touch that is not a blow — the page is right that the strike *"does
not need to be hard"* — and then a sensation with no precedent in being hit: **the limb stops arguing.**
Not pain, not numbness, not weakness. The arm that was moving to intercept arrives where it was going and
stays there, and the harder the owner tries to withdraw it the more definitely it does not come, because
withdrawal is relaxation and relaxation is what has been taken.

For a practitioner there is a second layer: the pathway at the contact point goes hard and quiet, and
whatever was flowing through it is on the far side of a lattice. For anyone else there is frost on the
skin, a white patch that is not a bruise, and a cold that is not felt as cold because the nerve carrying
that report is on the wrong side of the block.

**One to two seconds later everything comes back**, and that is the cruel part of the design: the target is
not damaged and knows exactly what happened, which means the next exchange is fought by a man who has
learned that the touch is the attack. *"Whatever the target intended to do next does not happen inside the
1-to-2-second lock, which for a hunter closing on a beast at speed is frequently the entire fight."*

**And afterwards there is a large man breathing carefully and running hot**, because every joule that came
out of the quarry is in him now, and the colder the kill the warmer the killer.

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| EU spent | **a fifth of current reserve per use (page `:20`)** | *"his own count puts the Essence toll near a fifth of what he is carrying per use."* **The only page in this batch that prices a cost as a fraction of reserve**, which `_method.md` §III says is the one condition under which a starvation margin can be computed at all. |
| **Starvation margin** | **11 uses, or 5 — the page does not say which** | *"Below ten percent EU a practitioner suffers Essence Starvation"* (`Core Vocabulary`). Read *"a fifth of what he is carrying"* as a fifth of **current** reserve and the sequence is 0.8ⁿ: 80, 64, 51, 41, 33, 26, 21, 17, 13, 10.7, **8.6% — starvation on the eleventh use.** Read it as a fifth of **maximum** and it is linear: 80, 60, 40, 20, **0 — starvation during the fifth** (`SA-GAP-VORYNN-FIFTH-OF-WHAT`). |
| Flux Density | `null` | No AU/s figure on card or page (`_method.md` §VIII). |
| η | **~0.55 (card `:35`)** — **0.05 below band, and it governs** | Tier 5 · Expert is **0.60–0.70** (Part Nineteen as corrected by **R44-4**). `C-062`, **ruled 2026-09-26** (rung **I-2**): the ~0.55 is his own figure and governs; the band is typical. |
| AU/s | `null` | Needs Flux Density. |
| Efficiency and bleed | **45% at η 0.55** | 1 − η, *"as heat, sound, and structural bleed."* **On this working the bleed is thermally in the same direction as the load**: it is heat, and he is already importing heat (§1e). |
| **Thermal diffusivity of tissue** | **α ≈ 1.4 × 10⁻⁷ m²/s** | Standard. |
| **Depth cooled in the stated lock** | **0.37 mm at 1 s · 0.53 mm at 2 s** | L ≈ √(αt). **To reach a muscle belly 5 cm down: t = L²/α ≈ 17,900 s, five hours** (`SA-PHYS-VORYNN-FREEZE-DEPTH`). |
| **Nerve conduction block** | **fails below ≈7–10 °C; ≈1.5–2 m/s lost per °C** | Established physiology. **Shallow nerves are in reach** — ulnar at the elbow 3–5 mm — where muscle bellies are not. |
| **Why rigid and not limp** | **SERCA Q₁₀ ≈ 2.5–3** | Relaxation is active and its rate roughly **halves per 7–10 °C** of cooling, while activation is far less affected. A muscle that cannot let go locks. **The page's stated sign is correct.** |
| **Force multiplier from lost compliance** | **×2 to ×4** | F = E/d. A defender yielding 30 cm halves the force of one yielding 15; 7.5 cm quarters it. **The same blow lands two to four times harder for no extra energy**, which is the page's *"does not need to be hard to be final"* with a number on it. |
| **Energy to freeze tissue** | **≈340 J/g** | Sensible heat to 0 °C at c ≈ 3.5 J/(g·K) plus latent heat of the water fraction (334 J/g × ~0.7). |
| **Cold actually delivered** | **≈1.7 kJ** | 100 cm² contact × 0.5 mm ≈ 5 g × 340 J/g. |
| **Stated Strike Force** | **20–100 GN · 46 GJ – 4.184 TJ**, *"near the top"* | Page `:45`, quoted correctly from Part Eleven and the card. **4.184 TJ is one kiloton.** |
| **Effect line vs Numerical Effect** | **≈2.5 × 10⁹ apart** | *"The strike does not need to be hard to be final"* (`:19`) against a city-block-scale yield at the top of A-Grade (`SA-NUM-VORYNN-4TJ-VS-NOT-HARD`). |
| **Heat rejected into the practitioner** | **≈1 K of core temperature per kg frozen** | 340 kJ/kg ÷ (100 kg × 3,500 J/(kg·K)). **3 kg → ≈3 K → 40 °C, heat illness.** A ceiling on quantity frozen that nobody has written down, and the reason the page's stated counter works. |
| Lock duration | **1–2 s** | Page `:45`, *"kept from the card as given"*. |
| Minimum Stage | **VI · Glory** | Page ✓ Part Five: Max Grade A, ceiling 400, Tier 5 · Expert. |
| Practitioner's Stage | **VI · Glory**, Level 178, Grade A, ceiling 400 | Card `:55`. **At the floor.** |
| Developmental Tier | **Harmonic** | Part Twenty-One, Stage VI. |
| Crystal State | *"Refined"* | Card `:35`. |
| **Ardency Penetration gate** | **✓ passes** | *"**Penetration** requires Body Path at Stage III to exceed C"* (Part Seven). Card: *"Body dominant"* ✓. |
| **Dexterity Celerity gate** | **✓ passes** | *"**Celerity** requires Body Path at Stage II to exceed D, and Stage IV to exceed B for standing acceleration."* Body ✓, Stage VI ✓. |
| **Vitality Tolerance gate** | **✓ open** | *"**Tolerance** open, except that its Aether-dead component requires Fate Path at Stage VII… and its gravitational component requires Attraction Path at Stage VI."* Neither component is claimed here. |
| **Dexterity Feint gate** (ex-Silence, 386) | **the same open question as his other two pages** | *"**Feint** requires **Spirit Path at Stage IV** to exceed B"* (Part Seven). 386 is A-Grade. Card Path: **Body dominant** — but the card also says he **had a Spirit Axis and lost it**, and that *"the power does not fail when the Axis dies"* (`SA-GAP-AXIS-VS-PATH`). |
| **Sub-Stat sourcing** | **✓ all four are the card's own attested peaks** | Ardency Penetration 358, Dexterity Silence 386, Celerity 344, Vitality Tolerance 400 — **all four on the card, at those numbers** (card `:79`). The page says so and the page is right. |
| **Law V and Craft** | **✓ correct, and it is the only Draven page that reasons it** | *"Spellcraft (Bodily: the fist carries the working, and it stops the instant his attention lapses)"* (`:33`). Stage VI is below Refraction and needs an anchor; the Four Crafts supplies exactly this one: *"A fist with combustion on it is Spellcraft with the body as the pen, and the sentence is still ephemeral — **which is why the fist stops burning the moment attention lapses**."* **The page has paraphrased the source's own clause** (`SA-CROSS-DRAVEN-CRAFT-SPLIT`, on which this page is the right side). |
| **Vohrin** | **not among the sixty** | The primary current is on four technique pages and the card and in none of the eight Family registers; it appears in canon as a **Titan** (`SA-UNATT-VOHRIN`). |
| **Cinerion, under-used** | **the current that answers §1(e)** | *"Cinerion retunes the Shell to metabolize its own combustion products, **harvesting from expenditure what other practitioners simply vent**."* The page uses it for remnants and for densifying the cold, not for the waste-heat problem the working actually has. |
| "Coherence Band D" (card `:55`) | **retired** | Lettered Coherence Bands retired under R42 (`SA-UNATT-COHERENCE-BAND`). |
| Aetheric Density check | **cannot be run** | No numeric scale exists (`SA-GAP-AETHERIC-DENSITY`). |

**Does the physics close against the stratal account?** **The mechanism is right, the sign is right, the
sourcing is right, and the two numbers on the page are a factor of a billion apart from each other.**

What closes: the page names a contact heat sink and then writes the correct limiting sentence about it —
*"far faster than the tissue's own conduction can redistribute it"* — which is the real constraint stated
in the right terms. Its stated Target Response is **rigid** rather than limp, and rigidity is what
cooling actually produces in muscle, for a reason (SERCA's temperature coefficient) that the page does not
give and does not contradict. Its stated counter — reintroduce heat — works for the right reason, by
removing the gradient rather than by overwhelming the sink, and Caloria's suppression row says the same
thing in the coupling table. Its four Sub-Stats are all four of the practitioner's own attested peaks and
the page says so. Its Craft line is a paraphrase of the Four Crafts' own sentence about a fist, which makes
it the only one of Draven's four pages that gets Craft and Law V right together. η is 0.05 under band
since **R44-4** and lawful under `C-062`'s ruling, the Stage is the floor, and the cost is priced as a fraction of reserve — **the only page in the batch that gives the
starvation margin anything to work with.**

What does not close: the depth, the yield, and the direction of the waste heat. **One to two seconds of
contact cools half a millimetre**, and the page asks it to lock muscle chains centimetres down; five hours
would do it. The Effect line says the strike *"does not need to be hard to be final"* and the Numerical
Effect hands it a **kiloton**, which is not a lock, it is a crater. And the heat has exactly one place to
go — through his own musculature, by the page's own Mechanism — which puts a ceiling of about three
kilograms of frozen quarry on him before his core temperature reaches forty degrees, a limit no page
states and which the one current already on his sheet, Cinerion, exists to relieve.

**Conflicts logged from this page:** `SA-PHYS-VORYNN-FREEZE-DEPTH`, `SA-NUM-VORYNN-4TJ-VS-NOT-HARD`,
`SA-EM-VORYNN-MOMENTUM-COLLAPSE`, `SA-GAP-VORYNN-FIFTH-OF-WHAT`, `SA-UNATT-VOHRIN`,
`SA-GAP-AXIS-VS-PATH`, `SA-CROSS-DRAVEN-CRAFT-SPLIT`, `SA-UNATT-COHERENCE-BAND`,
`SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR`.

---

## 5 · Counterplay and the challenge

**The fairness check.**

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **pass, and it is the best-costed page in the batch** | Two costs, both real. *"Every use tears fibre along the ignition path. Chained further, the tear compounds"* — structural, cumulative, and it scales with how hard he is pushing. And *"near a fifth of what he is carrying per use"* — a stated fraction of reserve, which makes **Essence Starvation computable for the first time in twenty-eight pages** (§4). The register's usual complaint does not apply here: this cost is due inside the scene. |
| Stated limits | **pass, and it is a hard prerequisite** | *"**Requires Bloodbind ignition.** Without the blood already burning, there is no vector to compress and no strike to throw"*, and *"Draven cannot freeze what the ignition never touches, which in practice means the strike must land, not merely threaten to."* A working that must land, from a man whose card says *"Range · Close. Melee and tracking. **He has no answer at distance and has never needed one.**"* |
| Something beats it | **pass, three named and two more in the registers** | Heat wards, void-momentum declines and airborne pivots are all named. §1(e) adds the self-loading ceiling and Caloria's coupling row adds *"saturated cold"* — a room he has already been working in. |
| It has a tell | **pass, and the tell is the approach rather than the strike** | The strike itself has none worth having: a touch, then rigidity. But the working *"requires Bloodbind ignition already running"*, and the Bloodbind is the card's only Trait, carrying the card's only Risk. Whatever announces the ignition announces this. |
| Numbers in band | **fails on the two that matter to each other** | ✓ η 0.55 is 0.05 below Tier 5's 0.60–0.70 as **R44-4** corrected it, and the card governs there — `C-062` **ruled 2026-09-26** (rung **I-2**), so this is no longer one of the faults. ✓ Stage at the floor, all four Sub-Stats sourced from the card, 1–2 s lock stated, Craft and Law V correct. ✗ The freeze depth is 0.5 mm against muscle chains centimetres deep (`SA-PHYS-VORYNN-FREEZE-DEPTH`). ✗ The Effect line and the Numerical Effect are 2.5 × 10⁹ apart (`SA-NUM-VORYNN-4TJ-VS-NOT-HARD`). |

**The Counterplay routes that work**
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Deny the Field — "Choose the ground by Family," and it has a joke in it.** Caloria fails in *"**Thermal
  equilibrium**, saturated cold, oxygen-poor air."* A sink needs a gradient, so a cold room is not
  atmosphere, it is a disarmament. **And the working manufactures its own suppression**: every joule he
  takes goes into him and then into the room, so in any enclosed space the man is raising the ambient floor
  toward himself with every use.
- **Break the Body — "Armour tiers," read for what a contact working needs.** *"Padded takes bruising and
  not gore. **Mail is immune to cuts, vulnerable to thrusts and blunt trauma, and vibrates under Essence
  shock in a way the wearer feels in the teeth.** Proofed plate turns shot at range and turns most edges
  entirely, leaving joints and grapples."* A heat sink is a **contact** device and half a millimetre deep
  (§1a). **Anything between the fist and the skin is most of a counter** — an air gap, a padded jack, dry
  wool — and the counter is cheap, mundane, and available to a man who has never heard of Vohrin.
- **Break the Body — "Distance," which his own card concedes.** *"Vectoria has to close… **Most
  practitioners are a threat about closing range and are written as though they were not.**"* The card:
  *"He has no answer at distance and has never needed one."* This working is the reason he has never needed
  one, and it reaches as far as his arm.
- **Break the Boundary — "Interrupt the chain," and this page tells you which chain.** *"Break his wrist
  and a gestured chain is finished."* The page's Craft line is *"Bodily: the fist carries the working, and
  **it stops the instant his attention lapses**."* Stage VI is below Refraction, so the anchor is
  required — and the anchor is the hand that has to touch you.
- **Break the Body — "Exhaustion," and it is arithmetic here rather than a hope.** *"Below ten percent
  reserve a practitioner suffers Essence Starvation: reduced stat expression, Shell degradation, Traits
  flickering. **A defender who can afford to spend nothing wins a long engagement against an attacker who
  cannot afford to spend nothing.**"* A fifth of reserve per use is a countable clock, and §4 says it runs
  out somewhere between the fifth use and the eleventh. **Making him spend is the counter and the page
  gives you the exchange rate.**
- **Break the Man — "Rigidity," and his card supplies the law.** *"Present him with the situation his own
  law handles worst and he will handle it that way regardless."* His only Trait is the Vorynn Bloodbind,
  whose Risk is *"an uncontrolled metamorphosis into a Prime Beast form, resulting in permanent loss of
  sapience"* — and this working **requires the Bloodbind to already be running.** A fight that forces him
  to chain it is a fight he wins into something he does not come back from.

**The tell, stated plainly.** The strike has almost none: a touch that does not feel like a blow, and then
a limb that will not come back. The tell is upstream. The Bloodbind has to be lit before the strike
exists, and a man closing under Tenebra cover with his blood already burning has, by his own page's
account, committed to contact. And downstream there is one nobody would look for: **he runs hot
afterwards.** Every joule taken out of the quarry is in him, and it does not leave quickly.

**The lookup trail.** What a player would have to read to assemble any of this. Pieces, not the answer.

1. `wiki/The Eight Families & the Sixty Wellsprings/Caloria — Thermodynamics.md` — read it for **Vohrin**
   and notice what is not there. Then read **Cinerion**, whose Mechanism describes a Shell metabolising its
   own waste and whose Failure describes what that costs later.
2. `wiki/The Magic System/The Eight Families & the Sixty Wellsprings.md` — the **Environmental Coupling**
   row for **Caloria**, both halves. One of the suppressive conditions is a thing this working creates.
3. `wiki/Volume I — Character Cards/Draven Kael Vorrick · The Beast Slayer.md` — his **Sub-Stat Peaks**
   (check all four against the page, they are there), his **Range** line, his one **Trait** and its
   **Risk**, and the note under his Path about an Axis.
4. `wiki/Fracture of Worlds — The Living System/III. Physical Force (Part Eleven).md` — the **A-Grade**
   Strike Force row. Convert the top of it to tonnes of TNT and read it against this page's first sentence.
5. `wiki/The Magic System/The Core Vocabulary.md` — **Essence Starvation**, and the ten percent threshold.
   Then work out how many uses a fifth of reserve buys, and notice that the answer depends on a word the
   page does not define.
6. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md` —
   **Part Seven's Dexterity, Ardency and Vitality Gates**, and Part Five for Stage VI.
7. `wiki/Fracture of Worlds — The Living System/IV. The Eight Primaries and the Sixty-Four Sub-Stats (Part Twelve).md`
   — the **Merge Ledger**, for what the Sub-Stat called Silence is called now.
8. `wiki/The Magic System/The Four Crafts.md` — **Law V** and the **Bodily** delivery vector. This page's
   Craft line is a paraphrase of one sentence in that file, and the sentence contains a limit.
9. `wiki/Techniques/Tenebra Ambush Art.md` — the approach this working's Trigger depends on, which has its
   own account and its own costs.
10. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — **"Choose the ground by Family,"**
    **"Armour tiers"** (read it as a question about what sits between a hand and a body), **"Distance,"**
    **"Interrupt the chain,"** **"Exhaustion,"** and **"Rigidity."**

**Conflicts added by this section:** none beyond those in §4; the fairness check passes on four of five,
and its failure is the two number rows already logged.
