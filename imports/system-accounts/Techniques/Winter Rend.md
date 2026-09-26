---
page: wiki/Techniques/Winter Rend.md
section: Techniques
practitioner: Draven Kael Vorrick
card: wiki/Volume I — Character Cards/Draven Kael Vorrick · The Beast Slayer.md
wellspring: Vohrin (primary) · Tenebra (secondary)
family: Caloria (Vohrin) · Limina (Tenebra)
stage_floor: VI
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · Winter Rend

## 1 · Physical account (physics)

**The phenomenon in plain words.** A man sweeps an arm or a weapon through a two-metre arc and cold comes
with it rather than after it. Things in the arc get colder along the line he drew. Armour cracks. There is
a pale streak in the air for a moment and a sound like something small breaking.

**The real phenomenon.** **Forced convection**, which is the complete answer to the page's own closing
question and is a factor of ten better than the alternative, and **thermal shock**, which is the one
target response on this page whose numbers close exactly — and which closes *because* the cooling is
shallow rather than in spite of it. What does not close is the yield, by six to eight orders of magnitude,
and where the accepted heat is supposed to go.

**(a) The page asks why the cold rides the strike, and heat transfer answers in one line.** *"**What
nobody knows** · Why the cold rides the strike's own kinetic wake rather than radiating from Draven
directly, the way every other cold-law working in the register does"* (`:21`).

**Because a stationary cold surface is a bad heat exchanger and a moving one is not.** Air conducts
appallingly — **k ≈ 0.026 W/(m·K)** — so a cold body sitting still in a room is limited by **natural
convection**, with a heat-transfer coefficient of about **5–10 W/(m²·K)**. Move the same surface and the
boundary layer thins, and the flat-plate correlation **Nu = 0.664 Re^½ Pr^⅓** gives **h ∝ √v.** Run the
numbers for a sword tip:

- Tip speed **30 m/s**, characteristic length 0.1 m, air kinematic viscosity 1.5 × 10⁻⁵ m²/s.
- **Re = vL/ν = 2 × 10⁵**; **Nu = 0.664 × 447 × 0.888 ≈ 264**; **h = Nu·k/L ≈ 69 W/(m²·K).**

**Seven to fourteen times better than standing still, from movement alone.** So the cold rides the wake
because riding the wake is the only configuration in which a cold-law working transfers anything worth
transferring through air. It is not a stylistic choice and it is not a mystery. **It is the difference
between a cold room and a cold wind, and everyone alive already knows which one takes the skin off your
face.**

**(One honest correction while we are here.** The wake itself *does* cool, and it is negligible. The
pressure deficit behind a body at 30 m/s is **½ρv² = 551 Pa**, and the adiabatic drop is
**ΔT = T·[(γ−1)/γ]·Δp/p = 290 × 0.286 × 551/101,325 ≈ 0.45 K.** Half a degree. The wake is the delivery
mechanism, not the cold.)

**(b) The armour claim is correct, the numbers close, and the reason is thermal shock.** *"armor not built
to insulate against a genuine thermal gradient cracks under the sudden contraction"* (`:40`). This is a
real failure mode with a real figure attached. The thermal shock resistance of a material is
**R = σ(1−ν)/(Eα)** — the temperature drop its surface can take instantaneously before the induced tension
reaches its strength:

| Material | σ | E | α | **R** |
|---|---|---|---|---|
| Structural steel | 400 MPa | 200 GPa | 12 × 10⁻⁶/K | **≈117 K** |
| Alumina | 300 MPa | 370 GPa | 8 × 10⁻⁶/K | **≈71 K** |
| Soda-lime glass | 50 MPa | 70 GPa | 9 × 10⁻⁶/K | **≈56 K** |

So cracking a steel plate needs a surface drop of about **120 K** — from a room at 290 K down to roughly
**170 K, or −103 °C** — and the induced stress at that drop is **σ = EαΔT/(1−ν) = 200 × 10⁹ × 12 × 10⁻⁶ ×
120 / 0.7 = 411 MPa**, which is at yield. **The page's claim is right on the number.**

**And here is the part worth pausing on: the shallowness is what makes it work.** Thermal shock is a
*gradient* effect. A plate cooled slowly and uniformly does not crack, because there is no differential
strain; a plate whose outermost skin is dropped a hundred degrees while the interior stays warm is the
worst case there is. **The same 0.1 mm penetration depth that makes the page's other target response
implausible is exactly the configuration that maximises the stress in the armour.**

**One condition attaches and the page satisfies it.** For a thermal shock this severe you need **contact**,
not airflow: the Biot number for a 5 mm steel plate under the convective coefficient in §1(a) is
**Bi = hL/k = 69 × 0.005 / 45 = 0.008**, far too low — the steel would simply equalise. **The sweep has to
touch the plate**, and the page's Trigger is *"A sweeping melee strike, arm or weapon"*. It does.

**(c) What the arc can actually take out of flesh, and it is not much.** Take the page's own geometry: a
**two-metre** arc, swept at a tip speed of 30 m/s, so **ω = 15 rad/s** and a 120° sweep takes **0.14 s**,
with any one point on the target in the cold for perhaps **0.05–0.1 s.**

Thermal diffusion in soft tissue is the same square-root law that governs the Execution Strike:
**L ≈ √(αt)** with **α ≈ 1.4 × 10⁻⁷ m²/s**, so at 0.1 s the cold reaches **0.12 mm.**

Price it. A target presenting about **0.5 m²** to the arc, cooled 0.12 mm deep, is **6 × 10⁻⁵ m³ ≈ 63 g**
of tissue, and taking tissue to freezing costs roughly **340 J/g** (sensible heat plus the latent heat of
its water). **Total: about 21 kilojoules.**

**The page prices this at *"46 GJ–4 TJ yield, city-block scale"*** (`:39`). **That is between 2 × 10⁶ and
2 × 10⁸ times what the described heat extraction requires** (`SA-PHYS-WINTER-ARC-YIELD`). The impact half
of the sweep is a separate matter and the band may be right for it; the page explicitly says *"Heat
extraction **and** impact force **both** land at Draven's A-Grade Ardency band"*, and for the heat
extraction that is a claim about a kiloton of refrigeration delivered across four square metres in a
seventh of a second.

**(d) Where the accepted heat goes, which no page in this practitioner's file answers.** A sink has two
ends. This page prices the cold one precisely — *"Mild numbness through his own arms after the strike"*
(`:44`) — and **numbness at a cooled limb is the correct symptom**: peripheral nerve conduction falls about
1.5–2 m/s per degree and fails below roughly 7–10 °C, so an arm held as the cold end of a sink reports
exactly that.

**But the heat taken out of the target has to arrive somewhere warmer than the arm**, and neither the page
nor the card nor any register says where. At the modest scale of §1(c) it hardly matters — 21 kJ into a
100 kg man is **0.06 K.** At the scale the page's Numerical Effect implies, it is not survivable by
anything. **The system states no rejection path for any Vohrin working**, which is a gap rather than an
error and it lands on every cold page in the corpus (`SA-GAP-WINTER-HOT-END`).

**Energy budget, stated.** Extracted from the target: **≈21 kJ** for what a 0.05–0.1 s exposure can reach
across the arc. Delivered as impact: the page says **46 GJ – 4.184 TJ** and §1(c) says the heat half of
that claim is out by six to eight orders. Moved by the wake: a **0.45 K** adiabatic drop, negligible, and
the wake's real contribution is a **7–14×** rise in transfer coefficient. Rejected: unstated
(`SA-GAP-WINTER-HOT-END`). Where the joules were: the target's. Fault class by `Two Sets of Books` §VII:
**Field fault** — *"The room could not supply what the working assumed"* — because the page's own stated
weakness is a room with heat in it: *"A strong heat vector delivered into the arc before it lands unmakes
the cold faster than Vohrin can hold it there."*

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** **Caloria**, *"**Spirit** (Fire/Heat/Cold) · **Medium** (Light)"*, favoured by
*"**Steep thermal gradients**, combustible atmosphere, geothermal ground"*, suppressed by *"**Thermal
equilibrium**, **saturated cold**, oxygen-poor air"*. **Limina**, *"**Spirit** primary"*, favoured by
*"Darkness, silence, Aether-thin ground, ruins"*, suppressed by *"Saturated Aether, crowd density, active
Domains"* (`wiki/The Magic System/The Eight Families & the Sixty Wellsprings.md`). *"Terrain is not
flavour. It is a modifier on η."*

**Caloria's row is §1 restated as terrain and it is unusually literal here.** *"Steep thermal gradients"*
is the working's input; *"thermal equilibrium"* is its absence; and *"saturated cold"* is the condition a
cold practitioner spends his engagement creating. **A Winter Rend used repeatedly in an enclosed space is
a Winter Rend working toward its own suppression row**, twice over — the room warms as he dumps, and cools
as he takes, until the gradient he needs is gone from both directions.

**Wellspring stratum — Vohrin, and it is not in the register.** The page's primary, and the card's
(*"**Vohrin** · Caloria. **The cold law.** Heat's absence, held as a discipline rather than suffered as a
condition"*, card `:45`), **is not among the sixty.** It appears in canon as a **Titan**
(`SA-UNATT-VOHRIN`). No Core Law can be quoted, so the card's gloss is all there is — and the gloss is
doing correct work: *"held as a discipline rather than suffered as a condition"* is precisely the
statement that cold is not a substance to be emitted but a deficit to be maintained, which is why §1(d)'s
question exists at all.

**Wellspring stratum — Tenebra, *The Hidden Shadow*, Limina, Entropy/Void/Mind.** Core Law, verbatim from
`wiki/The Eight Families & the Sixty Wellsprings/Limina — Entropy, Void and Mind.md`:

> **Analogue** · Signal-to-noise reduction. Absorptive coating and faceted return geometry.
> **Mechanism** · Something is undetectable when its return falls below the noise floor of whatever is
> looking, which is achieved by **absorbing incident energy** and by shaping surfaces so the little that
> reflects goes anywhere except back at the observer. Tenebra applies both to the Shell. Its practitioners
> are not invisible. They are quieter than the background, which is better.
> **Stat Effect** · Strengthens Dexterity Silence, Harmonics Suppression, Dominion Sense.
> **Failure** · Aspect dependence.

**And here the page uses Tenebra to do the opposite of what Tenebra does.** *"The arc lingers a moment as
pale afterimage, **the Tenebra-thinned residue** of the strike's own path"* (`:41`), and the Mechanism line
has Tenebra *"rid[ing] the same arc as afterimage — the same signal-to-noise reduction already documented
on Draven's sheet, applied to the visible strike-path rather than to his own body"* (`:38`). **Tenebra
reduces return.** An afterimage is return — and a *pale* one is bright return, added signal, the single
most visible thing that could be left behind by a man whose entire other discipline is not being seen
(`SA-EM-WINTER-TENEBRA-AFTERIMAGE`).

**The pale streak is real and it is condensation.** Cooling humid air below its dew point precipitates
water; below freezing it nucleates ice crystals; and the result is a white trail that hangs and disperses
— a contrail, or the fog that pours off liquid nitrogen. **A working that drops air temperature sharply
along a two-metre arc will leave exactly the pale afterimage the page describes, by Vohrin alone, with no
second Wellspring needed.** And the chime is real too: *"a faint chime carries where ice forms and
fractures in the same instant"* (`:41`) is differential thermal contraction cracking a thin ice layer, and
it sounds exactly like that.

**So Tenebra's actual job on this page is the one the Consequence line does not claim**: the same
signal-reduction that serves the Ambush Art, applied to the approach rather than to the residue. The page
has the right current doing the wrong thing at the wrong end of the working.

**The Sub-Stat list is the card's own peaks.** *"Ardency (320, A-Grade), Sub-Stat Ardency-Penetration
(358)… Vitality-Tolerance"* (`:49`) — both on the card at those numbers, and **both clear their Part Seven
gates on his declared Body Path** (§4). **This is one of the few pages in the batch with no Path problem
at all.**

**Which of the Four Theories.** **Correspondence**, thinly. The working does not bargain, bill or leave a
mark; it asserts that a line drawn through space can carry a property along it, which is a claim about
relation rather than about transfer. **Consent Doctrine** runs underneath as the standing enforced
position.

**Essence stratum.** Crystal layer: the **Aether Shell**, *"Class III · Resonant. Channels Aether into
hyper-dense muscular ignition and aggressive kinetic force, **using Frost Essence for systematic
slowing**"* (card `:34`) — this working is that clause thrown along an arc instead of applied at a point.
Developmental Tier **Harmonic** (Stage VI, Part Twenty-One). Tier of Standing **5 · Expert**, η band
**0.60–0.70** (Part Nineteen as corrected by **R44-4**); card η *"~0.55"* now **0.05 below the
floor**, and lawfully so: `C-062` was **ruled 2026-09-26** (Isaac, rung **I-2**),
the card governing and the corrected row standing as a typical range for him.
Crystal State *"Refined"*. **The invoice:** an arm held at the
cold end of a sink, and a quantity of somebody else's heat with nowhere stated to put it.

**The lens: *antiperistasis*, and the air that was supposed to push the arrow.** Aristotle, *Physics*
IV.8 (215a14–19) and *De Caelo* III.2, with *Meteorologica* I.12 behind it. ***Antiperistasis*** is the
doctrine that a quality is intensified by the encroachment of its opposite — a well is colder in summer
because the surrounding heat drives the cold inward and concentrates it — and Aristotle extends the same
figure to motion: a thrown spear keeps going because **the air it displaces rushes round behind it and
pushes.** The medium closing in the wake does the work.

**That is Winter Rend's premise stated in the fourth century BC.** The cold does not radiate from the man;
it is carried in the closure behind a moving edge, and the page's own word for the mechanism is *"the
strike's own kinetic wake."* It is also the single most famously wrong thing Aristotle wrote about motion,
and Buridan took it apart in the fourteenth century with the questions that still finish it: if the air
pushes from behind, why does sharpening the *rear* of a projectile not help, and why does the same air not
push it sideways?

**The productive misreading, and what it kills.** A school that takes *antiperistasis* seriously — as
Winter Rend's practitioners have every reason to, since **their working visibly depends on the wake** —
draws the obvious design conclusion. If the medium closing behind the blade is what carries and
concentrates the cold, then **give it more medium to close into.** So they broaden the back of the weapon:
flat, square, deliberately unfaired rear sections, to catch the maximum antiperistatic return. Their
blades look wrong to everybody else and they can explain exactly why they are right.

**Fluid dynamics kills them by the route they thought they were improving.** A broad flat trailing section
is a **bluff body**: drag coefficient rises from something like 0.05 for a faired section to about 1.2 for
a flat plate, form drag multiplies, and the sweep slows. And the cooling they were trying to increase goes
as **h ∝ √v** (§1a). **They have made the blade worse at the one thing that makes the cold work, in order
to improve a mechanism that does not exist** — and they are also, now, slower than the man in front of
them, in an art that is decided at two metres. The school's own records are perfectly consistent: their
masters' weapons are the broadest and their masters die closest to the enemy.

---

## 3 · Mechanism (the effect)

**The glyph, proposed.** `[Al]` **Edge** (Root · Thalen) for the arc and `[RenB]` **Boundary**
(Root · Zhaeren) for the thermal condition — both from the thirty mirrored entries, both filings under the
Index's Standing Note (*"Assignment is decided after the phenomenon, never before, and it is a filing
decision rather than a generative one"*), neither canon until ruled (`SA-GAP-GLYPH-MIRROR`).

**What boundary moves.** Not the air and not the target. **The boundary that moves is where the cold end
of a thermal gradient is permitted to be** — and the novelty of this working, which is the whole of its
"what nobody knows", is that the permission is granted to **a moving locus rather than to a place.** The
condition is attached to the edge, not to the man, and travels with it.

**What the law then does on its own, and it does a great deal more than it would standing still.** A cold
surface in still air is throttled by its own boundary layer, and natural convection is the worst heat
exchange in ordinary experience — **5–10 W/(m²·K)**, which is why a cold room takes hours to chill anything
and a cold wind takes seconds. Move the surface and the boundary layer thins as **h ∝ √v**, and at a sword
tip's speed the transfer coefficient is **an order of magnitude higher** (§1a). **Nothing is being pushed
or projected. A limit has been attached to something that moves, and convection does what convection
always does to a moving cold surface.**

**Two things then happen at once and they land on different materials.** In air, the sweep drops the
temperature past the dew point and past freezing, and the water that was dissolved in the room precipitates
as a white line hanging in the path — the pale arc, which is condensation and not residue. In anything
solid the edge touches, the outer skin goes to the sink's temperature in a hundredth of a second and the
material a millimetre in does not, and **that differential is the attack**: **σ = EαΔT/(1−ν)**, which for
steel at a 120 K surface drop is **411 MPa**, at yield (§1b). Armour does not melt, bend or dent. **It
cracks**, from the surface, in tension, in a plane it was never designed to resist.

**Against flesh the same operation is much less impressive and the page overclaims it.** √(αt) allows
**0.12 mm** in the tenth of a second a point spends in the arc, and half a millimetre of frozen skin is a
serious injury and not a decisive one (§1c).

**The failure modes.** **Reheating**, the page's own: *"A strong heat vector delivered into the arc before
it lands unmakes the cold faster than Vohrin can hold it there"* — a gradient attacked from the far end.
**Insulation**, also the page's, and correct: interpose anything with a low conductivity and the contact
the thermal shock requires never happens. **Reach**, two metres, which the page names as a counter against
itself. And **the hot end**, which is §1(d) and which nobody has written down.

**What the target sees and feels.** The sweep arrives with a smell before it arrives with anything else —
the dry, sharp smell of very cold air, which people describe as clean. Then the arc, drawn in white, and
the white is not the working; it is the room's own water coming out of solution along the line.

For a man in armour the experience is that nothing happens and then his harness is wrong. No impact worth
the name, no heat, no sound of a blow — and a crack, tinking, somewhere in the plate, propagating in the
half-second afterwards while the metal is still deciding. Plates do not fall off. They **split**, along
lines that follow nothing an armourer would recognise, and the next ordinary blow goes through a place
that was proof a moment ago.

For a man without armour it is a burn that is the wrong temperature. The skin along the line whitens and
then hurts later rather than immediately, because the nerve carrying the report is on the cold side of its
own conduction threshold, and what he mostly notices in the moment is that the limb is slow.

And there is a small sound afterwards that nobody expects from a cold working, *"a faint chime… where ice
forms and fractures in the same instant"* — ice laid down in a tenth of a second on a surface that is
still contracting underneath it, breaking as fast as it forms.

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| EU spent | `null` | No page figure; no formula converts a Stage into EU (`SA-GAP-EU-FORMULA`). **Note the sister page does state one** — Vorynn Execution Strike prices its cost at *"a fifth of what he is carrying per use"* — and this page, on the same practitioner and the same current, gives nothing. |
| Flux Density | `null` | No AU/s figure on card or page. |
| η | **~0.55 (card `:35`)** — **0.05 below band, and it governs** | Tier 5 · Expert is **0.60–0.70** (Part Nineteen as corrected by **R44-4**). `C-062`, **ruled 2026-09-26** (rung **I-2**): the ~0.55 is his own figure and governs; the band is typical. |
| AU/s | `null` | Needs Flux Density. |
| Efficiency and bleed | **45% at η 0.55** | 1 − η, *"as heat, sound, and structural bleed."* **The bleed is heat and the working's problem is heat** (§1d). |
| Arc | **2 m** ✓ **in band** | Part Eleven: A-Grade **Contact Range 3–10 m**; a 2 m reach sits below it, which is the conservative direction. |
| **Swept area** | **≈4.19 m²** | A 120° sweep at r = 2 m. |
| **Dwell per point** | **0.05–0.1 s** | Tip at 30 m/s over r = 2 m gives ω = 15 rad/s, so 120° takes 0.14 s. |
| **Depth cooled** | **0.12 mm** | L ≈ √(αt), α ≈ 1.4 × 10⁻⁷ m²/s, t = 0.1 s. |
| **Heat extraction achievable** | **≈21 kJ** | 0.5 m² presented × 0.12 mm ≈ 63 g of tissue × ≈340 J/g. |
| **Heat extraction claimed** | **46 GJ – 4.184 TJ** | Page `:39`, quoted correctly from Part Eleven and the card — but applied to *"Heat extraction **and** impact force **both**"*. |
| **Discrepancy** | **2 × 10⁶ – 2 × 10⁸** | **FAIL on the thermal half** (`SA-PHYS-WINTER-ARC-YIELD`). |
| **Convection coefficient, still** | **5–10 W/(m²·K)** | Natural convection in air. |
| **Convection coefficient, swept** | **≈69 W/(m²·K)** | Nu = 0.664 Re^½ Pr^⅓ at Re = 2 × 10⁵, L = 0.1 m, k = 0.026 W/(m·K). **7–14× better, and h ∝ √v.** This is the answer to the page's *"what nobody knows"*. |
| **Adiabatic wake cooling** | **0.45 K** | Δp = ½ρv² = 551 Pa at 30 m/s; ΔT = T(γ−1)/γ · Δp/p. **Negligible: the wake delivers, it does not cool.** |
| **Thermal shock resistance** | **steel ≈117 K · alumina ≈71 K · glass ≈56 K** | R = σ(1−ν)/(Eα). |
| **Induced stress at 120 K** | **411 MPa, at steel's yield** ✓ | σ = EαΔT/(1−ν) = 200 GPa × 12 × 10⁻⁶ × 120 / 0.7. **The page's armour claim closes exactly.** |
| **Why it needs contact** | **Bi = 0.008 under airflow alone** | hL/k = 69 × 0.005 / 45 for a 5 mm steel plate. Far too low for shock; the plate would equalise. **The page's Trigger supplies the contact** — *"A sweeping melee strike, arm or weapon"*. |
| **The pale arc** | **condensation, not Tenebra** | Cooling humid air below dew point and below freezing nucleates a visible trail. **No second Wellspring is required to produce it, and the one the page credits does the opposite** (`SA-EM-WINTER-TENEBRA-AFTERIMAGE`). |
| **The chime** | ✓ **correct** | Differential thermal contraction cracking a thin ice layer as fast as it forms. |
| **Heat rejection path** | `null` | A sink has two ends. The page prices the cold one (*"mild numbness through his own arms"*, which is the right symptom for a cooled limb — nerve conduction fails below ≈7–10 °C) and **nothing anywhere states where the accepted heat goes** (`SA-GAP-WINTER-HOT-END`). |
| Minimum Stage | **VI · Glory** | Page ✓ Part Five: Max Grade A, ceiling 400, Tier 5 · Expert. |
| Practitioner's Stage | **VI · Glory**, Level 178, Grade A, ceiling 400 | Card `:55`. **At the floor.** |
| Developmental Tier | **Harmonic** | Part Twenty-One, Stage VI. |
| Crystal State | *"Refined"* | Card `:35`. |
| **Ardency Penetration gate** | **✓ passes** | *"**Penetration** requires Body Path at Stage III to exceed C"* (Part Seven). Page and card both declare **Body**. |
| **Vitality Tolerance gate** | **✓ open** | *"**Tolerance** open, except that its Aether-dead component requires Fate Path at Stage VII… and its gravitational component requires Attraction Path at Stage VI."* Neither is claimed. |
| **Path gates overall** | **✓ all pass** | **The page names no Dexterity Sub-Stat, so it escapes the Feint question that binds his other two pages** (`SA-GAP-AXIS-VS-PATH`). One of the few clean Path lines in the batch. |
| **Craft** | **"Magicraft" — the umbrella, not a craft** | Page `:29`. The sister page on the same practitioner gets it right: *"Spellcraft (Bodily: the fist carries the working…)"*. Stage VI is below Refraction, so Law V requires an anchor, and a sweeping strike supplies a perfectly good one — **the page just does not say so** (`SA-CROSS-DRAVEN-CRAFT-SPLIT`). |
| Category | **"Vectra *(judgment call, unverified)*"** | Page `:28`, flagged by the page itself. Recorded as flagged, not as a conflict. |
| **Vohrin** | **not among the sixty** | Primary current absent from all eight Family registers; appears in canon as a **Titan** (`SA-UNATT-VOHRIN`). |
| Cost | *"Mild numbness through his own arms"* | Page `:44`. Physiologically the right symptom and, as a price, not one (`SA-FAIR-WINTER-MILD-COST`). |
| "Coherence Band D" (card `:55`) | **retired** | Retired under R42 (`SA-UNATT-COHERENCE-BAND`). |
| Starvation margin | `null` | No cost stated as a fraction of reserve **on this page** (`SA-GAP-EU-FORMULA`). |
| Aetheric Density check | **cannot be run** | No numeric scale exists (`SA-GAP-AETHERIC-DENSITY`). |

**Does the physics close against the stratal account?** **One half of this page is the best-observed
physics in the batch and the other half is unpriced.**

What closes: the page's own unanswered question has a complete, quantitative, one-line answer — a moving
cold surface transfers heat seven to fourteen times better than a stationary one, because **h ∝ √v**, and
that is why the cold rides the wake rather than radiating. Its armour claim is thermal shock, its number
is **R ≈ 117 K** for steel, the induced stress at that drop is **411 MPa** which is at yield, and the
condition that makes it work — a very shallow, very steep gradient — is supplied by the same diffusion
limit that constrains everything else the working does. The Biot number says the sweep has to touch, and
the page's Trigger says it does. Its stated Limit (insulation) and stated Weakness (heat into the arc) are
both correct and both attack the right variable. Its pale arc and its chime are condensation and
contraction cracking, and both are exactly what would be seen and heard. η is 0.05 under band since
**R44-4** and lawful under `C-062`'s ruling, the Stage is the
floor, the reach is conservative, and **every Path gate passes** — which, with no Dexterity Sub-Stat
claimed, makes this the only one of Draven's three pages in this batch with no gate question at all.

What does not close: the thermal half of the Numerical Effect, by six to eight orders of magnitude —
**21 kJ of achievable extraction priced at a city block** — and the hot end of a heat sink, which no page
and no register anywhere in the corpus locates. And the page credits its pale afterimage to the one
current on its own sheet whose law is the removal of visible return.

**Conflicts logged from this page:** `SA-PHYS-WINTER-ARC-YIELD`, `SA-EM-WINTER-TENEBRA-AFTERIMAGE`,
`SA-GAP-WINTER-HOT-END`, `SA-FAIR-WINTER-MILD-COST`, `SA-UNATT-VOHRIN`,
`SA-CROSS-DRAVEN-CRAFT-SPLIT`, `SA-UNATT-COHERENCE-BAND`, `SA-GAP-EU-FORMULA`,
`SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR`.

---

## 5 · Counterplay and the challenge

**The fairness check.**

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **FAIL** | *"Mild numbness in his own arms afterward."* An A-Grade area attack across two metres that cracks armour, for a sensation that clears. The page's sister technique on the same practitioner and the same current charges *"a fifth of what he is carrying per use"* and *"tears fibre along the ignition path"* — **the corpus knows how to price this working and this page does not** (`SA-FAIR-WINTER-MILD-COST`). The real unstated cost is thermal (`SA-GAP-WINTER-HOT-END`). |
| Stated limits | **pass, and it is material rather than arbitrary** | *"Ineffective against insulated or flame-forged armor built to withstand a genuine thermal swing."* §1(b) gives it a number: raise R = σ(1−ν)/(Eα), or interpose anything with a low conductivity, and the shock never arrives. **A limit a player can shop for.** |
| Something beats it | **pass, and both named routes are correct** | A heat vector into the arc attacks the gradient from the far end; mobility beats two metres. Both are cheap and neither requires a Wellspring. |
| It has a tell | **pass, and it is loud for a cold working** | A white arc hanging in the air, a chime, and the dry smell of very cold air arriving before the strike does. Nothing about this is subtle. |
| Numbers in band | **mostly pass, one large fail** | ✓ 2 m under A-Grade Contact Range. ✓ η 0.55 is 0.05 below the Tier 5 band of 0.60–0.70 as **R44-4** corrected it, and the card governs there — `C-062` **ruled 2026-09-26** (rung **I-2**). ✓ Stage at the floor. ✓ Both Sub-Stats the card's own peaks, both gates clear. ✓ Thermal shock numbers close exactly. ✗ The thermal half of the Numerical Effect is out by 10⁶–10⁸ (`SA-PHYS-WINTER-ARC-YIELD`). |

**The Counterplay routes that work**
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Break the Body — "Armour tiers," and it is the whole fight.** *"Padded takes bruising and not gore…
  **Ceramic and shard are sacrificial and fail on the second hit in the same place.**"* Read as a materials
  question, the register is already answering this working: thermal shock is a stiffness-and-expansion
  problem, so **the counter is anything compliant, low-conductivity and low-modulus between the edge and
  the body.** A padded jack does not crack. Wool, leather and felt have conductivities two orders below
  steel's and cannot sustain the gradient. **The cheapest kit in the register beats the most elegant
  physics on this page.**
- **Break the Body — "Distance," which the page concedes and the card confirms.** *"**Most practitioners
  are a threat about closing range and are written as though they were not.**"* Two metres, and the card:
  *"**Range** · Close. Melee and tracking. **He has no answer at distance and has never needed one.**"*
- **Deny the Field — "Choose the ground by Family," and the working suppresses itself.** Caloria fails in
  *"thermal equilibrium, saturated cold"*, and this technique creates both: every sweep takes heat out of
  the room and puts it back in somewhere, and an enclosed space converges. **He is best in the first
  exchange and worse in every one after it**, in a way the page never states and the coupling table does.
- **Break the Boundary — "Interrupt the chain," and Law V binds at his Stage.** *"Below Refraction a
  working requires an external anchor: voice, hand, ink or blood… **Break his wrist and a gestured chain is
  finished.**"* Stage VI. The anchor is the arm that draws the arc, and this page — unlike its sister —
  does not say which craft it is using, which is the difference between a wrist and a mouth.
- **Break the Man — "Read him," and the register names the category.** *"**Self-derived techniques must be
  read live, in the two or three exchanges before they kill you.**"* The page: *"Draven Kael Vorrick,
  self-derived during the Vorynn Trials."* And the second clause is the counter: *"**Every thaumaturge has
  a pattern.**"* His is a two-metre arc drawn from a closing approach, and it is visible in the air after
  the first one.
- **Break the Man — "Rigidity," via the card's one Trait.** *"Present him with the situation his own law
  handles worst and he will handle it that way regardless."* His card lists one Trait and one Risk: the
  Vorynn Bloodbind, and *"an uncontrolled metamorphosis into a Prime Beast form, resulting in permanent
  loss of sapience."* A fight that must be won by escalation is a fight he escalates.

**The tell, stated plainly.** Cold air smells dry and sharp, and it arrives before he does. The arc is
drawn in white and hangs for a moment — that is the room's own water, not a magical residue, and it tells
you exactly where the edge went and therefore where the next one will go. There is a small ringing sound
that does not belong to a blow. And afterwards he shakes out his arms.

**The lookup trail.** What a player would have to read to assemble any of this. Pieces, not the answer.

1. `wiki/The Eight Families & the Sixty Wellsprings/Limina — Entropy, Void and Mind.md` — **Tenebra**'s
   Mechanism. Read the first clause carefully and then read this page's Consequence line, and ask whether
   a current that removes visible return can be credited with a pale afterimage.
2. `wiki/The Eight Families & the Sixty Wellsprings/Caloria — Thermodynamics.md` — read it for **Vohrin**
   and notice what is not there.
3. `wiki/The Magic System/The Eight Families & the Sixty Wellsprings.md` — the **Environmental Coupling**
   row for **Caloria**, both halves. The working makes one of its own suppressive conditions every time it
   is used.
4. `wiki/Volume I — Character Cards/Draven Kael Vorrick · The Beast Slayer.md` — his **Sub-Stat Peaks**,
   his **Range** line, and his one **Trait** with its **Risk**.
5. `wiki/Techniques/Vorynn Execution Strike.md` — the same practitioner, the same primary current, and a
   **Cost line that prices itself as a fraction of reserve.** Compare it with this page's.
6. `wiki/Fracture of Worlds — The Living System/III. Physical Force (Part Eleven).md` — the **A-Grade**
   Strike Force and Contact Range rows. Note which of this page's two claims that band is plausible for.
7. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md` —
   **Part Seven's Ardency and Vitality Gates**, and Part Five for Stage VI. This page passes them; check
   that it does.
8. `wiki/The Magic System/The Four Crafts.md` — the four crafts and **Law V**. This page names an umbrella
   where its sister names a craft and a delivery vector, and the difference decides which anchor an
   opponent can take.
9. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — **"Armour tiers"** (read as a
   materials list rather than an equipment list), **"Distance,"** **"Choose the ground by Family,"**
   **"Interrupt the chain,"** **"Read him,"** and **"Rigidity."**
10. `wiki/The Magic System/The Physical Account Two Sets of Books.md` — the **Field fault**, which is the
    fault this page's own Weakness line describes.

**Conflicts added by this section:** `SA-FAIR-WINTER-MILD-COST` (also cited in §4).
