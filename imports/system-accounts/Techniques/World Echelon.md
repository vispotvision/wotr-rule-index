---
page: wiki/Techniques/World Echelon.md
section: Techniques
practitioner: Francis Alexander · The Crimson Dirge of Atonement
card: wiki/Volume I — Character Cards/Francis Alexander · The Crimson Dirge of Atonement.md
wellspring: Judicium (primary) · fifty-seven of the Sixty, injured, secondary and unspecified
family: Fulguria (Judicium); the injured secondary spans an unspecified majority of the eight
stage_floor: XIV
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · World Echelon

## 1 · Physical account (physics)

**The phenomenon in plain words.** For forty seconds, inside five kilometres, every mind present is
made to keep the same time as a court. Nobody is struck. What changes is that private feeling stops
being private, because it is now being measured against a common reference that was not there a
minute ago.

**The real phenomenon.** **Phase synchronisation in a network of coupled oscillators** — the
**Kuramoto model**, which the page names by name (`wiki/Techniques/World Echelon.md:38`) and, unlike
most pages in this batch, names correctly. The page gets four things right that fall straight out of
the mathematics, and one thing wrong that the mathematics forbids.

**(a) A synchronisation working is cheap, and that is the whole reason it can be five kilometres
across.** This is the point the page never makes and most needs. Synchronisation does **not** change
the oscillators' amplitudes. It changes only their **phases**. The energy sitting in the population
is the population's own, before and after; the coupling only decides *when* each unit does what it
was already going to do. Huygens saw this in February 1665 with two pendulum clocks on a common
beam — his "odd kind of sympathy" — and the modern reconstruction measured how little the beam has
to carry: the coupling through the support is a small fraction of the energy in either pendulum, and
it still drags both into antiphase within about half an hour
([Bennett, Schatz, Rockwood & Wiesenfeld, *Huygens's clocks*, Proc. R. Soc. Lond. A **458** (2002)
563–579](https://royalsocietypublishing.org/doi/10.1098/rspa.2001.0888);
[Oliveira & Melo, *The sympathy of two pendulum clocks*, Sci. Rep. **6** 23580
(2016)](https://www.nature.com/articles/srep23580)). **A working that only sets phases is the
cheapest large-area working it is possible to design**, and it is exactly what
`The Physical Account Two Sets of Books` §III means: the joules were already in the room, in the
people, in their own emotional and metabolic stores. He supplies a coupling term and nothing else.

**(b) It has a threshold, and below it literally nothing happens.** The Kuramoto order parameter *r*
runs from 0 (incoherent) to 1 (locked), and it stays pinned at **exactly zero** until the coupling
clears a critical value. For a unimodal, symmetric spread of natural frequencies *g*(ω), that value
is

> **K_c = 2 / (π g(0))**

([Dörfler & Bullo, *On the critical coupling for Kuramoto oscillators*, SIAM J. Appl. Dyn. Syst.
(2011), arXiv:1011.3878](https://arxiv.org/abs/1011.3878);
[Chaos **29** 053122 (2019)](https://pubs.aip.org/aip/cha/article/29/5/053122/286744/A-graphical-approach-to-estimate-the-critical)).
Read *g*(0) as the crowd's agreement: **the wider the spread of what the people in the five
kilometres are feeling, the smaller g(0), and the larger the coupling he must pay for.** A court
convened over a homogeneous, frightened district locks almost for free. The same court convened over
a genuinely divided one may not lock at all. **The technique is cheapest against the population that
least needs trying**, and that is a property of the mathematics rather than a moral I have added.

**(c) It cannot let go cleanly, and this is the page's best line arriving with a law behind it.** The
page's Consequence is *"The synchronisation does not release cleanly, hence the local Principle drift
once the working ends; the field takes time to de-phase back to ordinary variance"* (`:41`). That is
**critical slowing down**. Near a synchronisation transition the dominant eigenvalue goes to zero and
the relaxation time **diverges** — the system takes unboundedly long to recover from a perturbation,
and the same divergence has now been measured at abrupt *de*synchronisation as well
([Phys. Rev. E, *Scaling laws and relaxation rate at first order desynchronization*
(2025)](https://journals.aps.org/pre/abstract/10.1103/n74h-sdgj);
[arXiv:1411.4810](https://arxiv.org/pdf/1411.4810)). **The page's after-effect is not a flavour note.
It is the one thing a physicist would have predicted from the mechanism before reading the
Consequence line.** What the page does not supply is the number: a field that took τ to lock takes of
order τ to unlock, and neither τ is stated anywhere. `SA-GAP-ECHELON-DEPHASE-TIME`.

**(d) Five kilometres is not too far, and the arithmetic says so.** The page's Physics Domain is
electromagnetism (`:27`), so the coupling propagates at *c*. Crossing the radius takes
5,000 m ÷ 2.998×10⁸ m s⁻¹ = **1.67×10⁻⁵ s**, about **16.7 microseconds**. Over the stated forty-eight
seconds that is **2.9 million** round trips. Delay-coupled Kuramoto networks only go multistable when
the delay is comparable to the oscillation period; at six orders of magnitude below it, the field is
effectively instantaneous. **The radius is one of the few figures in this batch that survives contact
with real physics untouched.**

**And here is what the mathematics forbids.** **Kuramoto coupling is symmetric.** Oscillator *i*
pulls on *j* through sin(θⱼ − θᵢ) and *j* pulls back on *i* through sin(θᵢ − θⱼ) — the same
coefficient, opposite sign. There is no one-way phase coupling in the model, and the same objection
was already raised in this batch against `Symphonia Ascendens`: **there is no one-way resonant
coupling in linear physics.** But Francis's card describes his Attraction Layer as *"Vast and
one-directional. Fifty-seven Wellsprings under partial siphon and four thousand subjugated spiritual
dominions, every bond pointing inward. **Nothing on it points back**"*
(`wiki/Volume I — Character Cards/Francis Alexander · The Crimson Dirge of Atonement.md:41`).
**A synchronisation mechanism run through a layer on which nothing points back is asking a
bidirectional law to behave unidirectionally**, and the two sentences cannot both be right as
written. `SA-PHYS-ECHELON-ONE-DIRECTIONAL-BOND`.

**Measurable quantities, SI.**
- Radius **5,000 m** (page, as given) ⇒ (4/3)π(5,000 m)³ = **5.236×10¹¹ m³**. That is **125×** the
  volume of `Dirge Ascension`'s kilometre (4.19×10⁹ m³), which is what a cube law does to a factor
  of five.
- Duration **48 s** (page `:39`, eight turns at six seconds each).
- Coupling crossing time **16.7 µs**; **2.4×10⁶** crossings inside the window.
- Threshold **K_c = 2/(π g(0))**, with *g*(0) the density of the population's emotional frequencies
  at the mean. **Not computable here: the system supplies no measure of a crowd's emotional
  variance.**
- Output **null**. See §4 — the one AU/s figure the batch holds for Francis belongs to a state this
  working is forbidden to share. `SA-GAP-ECHELON-AUS`.

**The energy budget, and where the joules were.** In the people and in the ambient field, and almost
none of it moves. This is the cleanest instance in the whole batch of the standard's own claim:
*"The practitioner does not supply the joules. They supply the boundary condition"*
(`wiki/The Magic System/The Physical Account Two Sets of Books.md`, quoted at
`imports/system-accounts/_method.md` §IV). The boundary condition here is a single scalar — the
coupling constant *K* across a sphere — and everything else in the working is the population doing
what a coupled population does. Whether the joules he does spend clear the local ceiling cannot be
tested, because **Aetheric Density has no numeric scale anywhere in the system**
(`SA-GAP-AETHERIC-DENSITY`).

**Precedent we are not copying.** The genre's courtroom-domain is a truth-compeller: Judge Frollo's
tribunal, *Ace Attorney*'s psyche-locks, the Warrant in a dozen CRPGs, and above all the
*Jujutsu Kaisen* Domain Expansion, whose defining property is a **guaranteed hit** inside the
boundary. World Echelon guarantees nothing. It **sets a reference clock** and then reads deviation
off it, which means a participant who happens to sit at the court's own phase is invisible inside it
and a participant far enough off it never couples at all. **The divergence is that this Domain does
not convict anyone. It builds the instrument on which conviction is afterwards legible**, and the
instrument has a documented blind spot at both ends of its own scale.

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** 5.236×10¹¹ m³, drawn thinly, because phase-setting is not amplitude-setting.
The Families table gives Fulguria's environmental coupling as *"Dry air, conductive substrate, clear
line of sight"*, against *"Faraday-caged interiors, heavy ferrous shielding, dense fog"*
(`wiki/The Magic System/The Eight Families & the Sixty Wellsprings.md:148`) — and a five-kilometre
urban radius is the terrain Fulguria is worst in, since the Counterplay register lists *"boiled
leather, fired clay, dense fog and a shielded interior"* as what Fulguria
fails against (`wiki/The Magic System/Counterplay What Beats a Practitioner.md:25`). **A court held
over a tiled, fogged, shuttered quarter is a court running at a discount nobody on the page has
costed.** **Residue:** a district that has been briefly made to keep one time, and whose de-phasing
is the page's own stated Principle drift. **Saturation:** a five-kilometre Zenith field is the
largest saturation candidate in the batch, and the system's consequence for engineered saturation is
*"Crystal Fracture Events in everyone exposed, **including the person who caused it**"*
(`The Core Vocabulary` §II) — which the page does not mention at all.

**Wellspring stratum.** **Judicium · *The Wellspring of Truth*** (primary), Family **Fulguria**,
Physics Domain **electromagnetism**. Its law, verbatim from
`wiki/The Eight Families & the Sixty Wellsprings/Fulguria — Electromagnetism.md:22`:

> "Every element absorbs and emits at wavelengths fixed by its own electron structure, and no
> substance can present another's spectrum. Judicium tunes Gnosis to that principle: the practitioner
> reads the characteristic lines of a Crystal, a technique, or a lie, and identifies composition from
> signature alone. Eddy-current inspection finds the crack under the paint without removing the
> paint."

**And notice what that law is and is not.** Judicium is a **spectroscopic** law: it reads a signature
*against a known reference*. It is a law of **identification**, not of **compulsion** — which is
precisely why it is the right current for the half of this working that weighs, and supplies nothing
at all for the half that synchronises. Judicium's own register failure is *"**Spectral overload.**
Every object in view reports its composition simultaneously and the practitioner loses the ability to
prioritise any of it"*
(`wiki/The Eight Families & the Sixty Wellsprings/Fulguria — Electromagnetism.md:24`) — **which is the exact failure mode of a court that has just made
every emotion inside five kilometres legible at once.** The page's mechanism and the Wellspring's
stated failure are the same event seen from two sides, and the page does not notice.

The secondary is *"fifty-seven of the Sixty Wellsprings, injured per the Heresiology's Wellspring
Injury framework"* (technique page `:25`), which the card corroborates at Dominion 1,480: *"Fifty-seven Wellsprings
and a Tribunal that overlaps the Soul Plane"* (card `:63`). **The Heresiology does carry that
framework, and it says something about this page the page does not say about itself.** Its table
*Wellsprings Most Frequently Injured* names five, and **Judicium is one of them**, with its common
corruptions listed as *"Moralization of extermination · **transformation of review into domination**
· reclassification of cruelty as cleansing"* and its doctrine as *"**Law without mercy becomes
burnished sadism.** … Judicium injury is most visible where either side is used to excuse the other's
absence"* (table at `wiki/Materials, Alchemy & Trade/The Heresiology of Alchemy.md:166`, the Judicium
row at `:172`). **The page cites
the Heresiology as its authority for fifty-seven injured secondaries while performing, on its
primary, the one corruption that same table names for Judicium.** Logged, not resolved:
`SA-CROSS-ECHELON-JUDICIUM-INJURY`. It is the most interesting thing on the page.

*Four Theories.* **The Consent Doctrine, and its breach.** The Accord's enforced position is consent
(`Two Sets of Books` §IV), and this working converts the emotional state of everyone inside five
kilometres into court evidence without any of them being party to the proceeding. The page does not
raise it. **Noted, not resolved.**

**Essence stratum.** Active layer: the **Attraction Layer**, unambiguously — a five-kilometre claim
held as a Domain is what that layer is for — with the **Essence Core** holding the doctrine the court
weighs against. Developmental Tier at Stage XIV: **Crystallized Soul**, *"Self and law correspond
with near-perfect precision. An exact instrument of identity. Thought carries causal weight"*
(Part Twenty-One), which is the prerequisite for a man whose standing claim is itself a tribunal.
Crystal State: the card says **"Absolute Crystal"**, which is a Developmental Tier and not a State;
already logged for this practitioner as `SA-CROSS-FRANCIS-ABSOLUTE-CRYSTAL`. **The invoice:** *"High
soul-heating and a local Principle drift that outlasts the working itself"* (`:18`) — and note that
half of that invoice is billed to the district rather than to him.

**The lens: Quetelet's social physics, and the man who was averaged into existence.** Adolphe
Quetelet, *Sur l'homme et le développement de ses facultés, ou Essai de physique sociale* (Paris,
1835), invented the ***homme moyen*** — a fictitious person carrying the mean of every measurable
human quality — and then did the thing that made him famous and dangerous: he extended it from chests
and heights to conduct. Crime rates held steady year on year, so Quetelet reasoned that the average
man must carry a stable ***penchant au crime***, a propensity, and that **what falls inside the
acceptable limits of variability is normal while what falls outside them is pathological**
([Sposini, *At the borders of the average man*, J. Hist. Behav. Sci. **56** (2020)
](https://onlinelibrary.wiley.com/doi/abs/10.1002/jhbs.22019);
[*Adolphe Quetelet: Social Physics, Determinism, and 'The Average Man'*, in *Victorians and Numbers*,
OUP](https://academic.oup.com/book/38774/chapter/337582254)). That is World Echelon's entire
procedure, four centuries early and in French: **establish a mean, then read distance from it as
guilt.** The Kuramoto order parameter is the *homme moyen* with a phase.

And the lens is wrong in the place that matters, which is why it is worth naming. Quetelet's average
is **descriptive**: it is computed *after* the fact, from a population that went on behaving however
it behaved, and its error is only that he mistook a statistic for a norm. This court does not compute
an average. **It manufactures one**, by driving the population onto a single phase first and reading
deviation second — so the mean it measures against is a mean it imposed. A Measurewright school
reading the Tribunal through social physics will therefore defend it as *observation*, will produce
beautiful tables showing that the Echelon merely records what was always there, and will be wrong by
exactly one step in the causal order. **The productive misreading is that the instrument is
diagnostic. It is constitutive**, and a school that cannot see the difference will certify the court
as impartial for as long as anyone lets it.

---

## 3 · Mechanism (the effect)

**Glyph (proposed; the page names none).** `[Ho]` **Order** · Extension · Valen — a limit on how much
variance a field is permitted to carry, which is the one boundary a synchronisation working actually
moves — laid across `[Ae]` **Vastness** · Root · Zhaeren for the five kilometres, with `[Me]`
**Measure** · Synonym · Urion doing the weighing. All three from the thirty mirrored forms in
`wiki/The Magic System/The Master Glyph Index — 136 Attested Forms.md`.
*Filing decision, not canon — Isaac's ruling.* `SA-GAP-GLYPH-MIRROR`.

**What boundary moves.** Exactly one scalar: **the coupling strength *K* between every Essence-bearing
oscillator inside 5,000 m, for 40 s.** Not their amplitudes, not their contents, not their intentions.
The Index's own statement of what a glyph is could have been written for this working: *"A glyph
creates nothing and carries no power. … A glyph is a boundary condition imposed on that law. It moves
a limit, and the law does what it has always done on the far side of the new limit."*

**What the law then does on its own.** Everything, and every clause on the page is a property of
Kuramoto dynamics rather than a design decision:

- **The lock is all-or-nothing.** *r* sits at zero until *K* clears **2/(π g(0))**, then rises
  continuously. There is no gentle partial court. **This is why the working has no small version**,
  and why the page can state a radius and a duration and nothing in between.
- **It is a phase transition, so it cannot be held indefinitely.** Forty seconds is the page's figure;
  the mathematics only insists the state is maintained, not free.
- **It does not release cleanly**, because relaxation time diverges near the transition. The page's
  Principle drift is the physics' critical slowing down, and neither the page nor the system supplies
  the time constant. `SA-GAP-ECHELON-DEPHASE-TIME`.
- **It cannot coexist with `Dirge Ascension`**, and the page's reason is sound in the physics as well
  as the metaphysics: *"two Domain-scale claims this large do not coexist on one Crystal at once"*
  (`:42`). A renormalisation of a kilometre and a phase-lock of five kilometres are two boundary
  conditions on one field, and a field takes one.
- **The rough seat is a real fault line and the page says so honestly**: *"World Echelon is,
  structurally, two arguments held in one lattice, and an opponent who reads the seam between the
  Spirit half and the Fate half is reading a genuine fault line, not a metaphor"* (`:43`) — which is
  the Four Paths register's own words, *"They are not damaged. They are **two arguments held in one
  lattice**"* (`wiki/The Magic System/The Four Paths Routing, Recognition and the Gate.md:68`). **The
  page quotes canon correctly and applies it correctly.**

**Law V check.** Stage XIV sits far above Refraction, so no material anchor is required
(`wiki/The Magic System/The Four Crafts.md`). The page gives a declaration — *"Francis declares the
merger"* (`:36`) — which is voice, and therefore more anchor than the Stage requires rather than
less. Clean.

**Failure mode — Boundary fault.** *"The condition was imprecise and the law ran somewhere
unintended"* (`Two Sets of Books` §VII). The boundary here is a single coupling constant applied to
every oscillator in a sphere without discrimination, and the law then synchronises **everyone**,
including his own people, including him. There is no clause on the page excluding the caster from his
own court, and under Kuramoto there could not be: a coupled node is coupled.

**And here is the boundary the page cannot supply, because it is asking the wrong plane for it.** The
card says the Tribunal merges with *"the Soul Plane"* (card `:106`); the page says it merges with
*"the local Spirit World"* (`:17`), and **"Spirit World" occurs in exactly one file in the whole
mirror, which is this page** — `grep -rl 'Spirit World' wiki/` returns `wiki/Techniques/World
Echelon.md` and nothing else (`SA-CROSS-ECHELON-SPIRIT-WORLD`). Per `CONTINUE.md`'s staleness
protocol the absence is canon's and not the mirror's: `wiki/` last committed **2026-09-25 18:40**,
after this page's `last_edited` of 2026-09-12 and after the card's of 2026-09-24. Take the card's
term, which is attested, and the cosmology's account of it says three things that this mechanism
cannot survive (`wiki/Cosmology & Metaphysics/The Crossing and the Making of the God Hand.md:21`,
table at `:31`):

> "The Soul Plane does not speak in vibration. It does not carry pressure or temperature or the
> acoustic signatures a Physical Plane sensory Wellspring is built to catalogue."

| Property | On the Physical Plane | On the Soul Plane |
|---|---|---|
| **Light** | Electromagnetic radiation bouncing off surfaces | **Recognition.** … It does not illuminate from outside. It recognises from inside |
| **Organisation** | By distance | **By bond** |

**A Kuramoto field needs oscillators with a phase and a natural frequency — it needs vibration — and
the canon says the plane being merged with does not carry any.** The page's Physics Domain is
*"Electromagnetism, primary"* (`:27`) and the canon says light there is not electromagnetic at all.
And the page states a **five-kilometre radius**, a distance, for a working on a plane the canon
organises **by bond and not by distance**, which means the boundary as written does not name a
well-formed region on the far side of the merge. Three separate contradictions, none of them
explained by anything on the page: `SA-PHYS-ECHELON-SOUL-PLANE-VIBRATION`,
`SA-CROSS-ECHELON-DISTANCE-VS-BOND`.

**What the target sees and feels.** Nothing arrives. That is the first thing, and it is the
frightening one: there is no strike, no pressure, no heat, and for a second or two nothing seems to
have happened at all. Then the interval changes. Whatever a person was feeling — grief, boredom,
the ordinary low hum of a working afternoon — keeps its content and loses its **timing**, and begins
to arrive on a beat that belongs to somebody else's proceeding. Breathing falls in. The crowd in the
street moves like one thing. And a person discovers the specific horror of the working, which is that
their interior life is now **legible from outside as a quantity**: not read, not guessed at, but
*measured*, against a reference they did not set, in a court that convened around them without asking.
Those who happen to lie near the court's own phase feel almost nothing and are recorded as nothing.
Those who lie far outside it never couple, and stay strange, and are conspicuous for it. It is the
people in between — the ones close enough to be caught and far enough to register a deviation — whose
feelings become the evidence. **Forty seconds later the coupling stops and the phases do not, and a
district goes on keeping the court's time for an unstated while afterwards**, which is the Principle
drift, and which is the part nobody inside it can tell from their own mood.

**What bleeds, at the stated efficiency.** The card gives **η = 0.93** (card `:42`). Stage XIV places
him in **Tier 8 · Archmaster**, band **0.95–1.2** (Part Nineteen); 0.93 sits **below the floor by
0.02**, already logged batch-wide as `SA-NUM-ETA-TIER`. At 0.93, **7 %** of the expenditure leaves as
heat, sound and structural bleed — which the page names as *"high soul-heating"*, the one place its
Cost line and the system's efficiency ladder agree. At η above 1.0, which his Tier's band says he
should reach, *"the environment becomes a co-author"* (Part Nineteen) — and **for this working, of all
of them, a co-authoring environment is not a bonus but a category change**, because the thing being
co-authored is a court's reference phase.

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| Radius / volume | **5,000 m** / **5.236×10¹¹ m³** | Page `:17`; (4/3)π(5,000 m)³. **125× `Dirge Ascension`'s kilometre**, by the cube of five. |
| Duration | **48 s** | Page `:39`, eight turns at six seconds each. |
| Coupling crossing time | **16.7 µs** | 5,000 m ÷ c. **2.9×10⁶ crossings in 48 s** — propagation delay is six orders below the window and constrains nothing. |
| Lock threshold | **K_c = 2/(π g(0))** | Kuramoto. *g*(0) is the population's emotional-frequency density at the mean. **Not computable: the system has no measure of crowd variance.** |
| **AU/s** | **`null`** | **And this is the page's sharpest gap.** The only AU/s figure the batch holds for Francis is **2,800,000**, sourced to `wiki/Techniques/Dirge Ascension.md:17` — where it is explicitly the *ascended* output: *"Francis steps into a proto-Archonic state for 45 seconds, shedding his mortal ceiling; local physics inside a one-kilometre radius run on rewritten equations for the duration, and his Aether output spikes to 2,800,000 AU/s"*. **World Echelon cannot run alongside Dirge Ascension** (`:19`), so the one figure is measured in the one state this working forbids. `SA-GAP-ECHELON-AUS`. |
| Flux Density | **`null` for this working** | `_method.md` §VIII carries **3,010,753 EU/g** for Francis, derived as 2.8×10⁶ ÷ 0.93. That derivation treats an ascended figure as a baseline Crystal property; if `Dirge Ascension` raises his output, as its own text says, then 3,010,753 EU/g is the *ascended* Flux Density and his resting figure is unknown. `SA-NUM-FRANCIS-ASCENDED-FLUX`. |
| EU spent | `null` | No page figure, no Stage→EU formula. `SA-GAP-EU-FORMULA`. |
| η | **0.93** (card `:42`) | Tier 8 band **0.95–1.2** (Part Nineteen) — **below the floor by 0.02.** `SA-NUM-ETA-TIER`. |
| Bleed | **7 %** at the card's η | 1 − η. Matches the page's *"high soul-heating"*. **Above η 1.0 the environment co-authors** (Part Nineteen). |
| Cost | **High soul-heating + local Principle drift**, drift duration `null` | Page `:18`. Critical slowing down puts the drift of order the lock time; **neither time is stated anywhere.** `SA-GAP-ECHELON-DEPHASE-TIME`. |
| Minimum Stage | **XIV · Zenith** | Page `:30`. Max Grade EX, ceiling 1,500 (Part Five). |
| Tier of Standing | **8 · Archmaster** | Part Five. |
| Developmental Tier | **Crystallized Soul** | Stage XIV (Part Twenty-One). |
| Crystal State | card says **"Absolute Crystal"** — not a State | Already logged: `SA-CROSS-FRANCIS-ABSOLUTE-CRYSTAL`. |
| Grade required | **EX** (1,201–1,500) | Page `:31`. Card: **Dominion 1,480**, Harmonics 1,380 ✓. |
| EX-Grade band | **1.24×10²⁹ – 6.906×10³⁷ J** | Part Four — **but Part Four also says Zenith output is not assessed by conventional metrics**, and this working delivers no strike to assess. `SA-NUM-ZENITH-CONVENTIONAL-METRICS`. |
| **Path gate — Dominion Radius** | **FAILS: needs Attraction Path** | *"**Radius** requires Attraction Path at Stage V to exceed A, Stage VI to exceed A for partial projection outward, and Stage VII to exceed S for boundary expansion speed"* (Part Seven, `:146`). At EX he is far past S, so all three thresholds bind. **His card reads *"Path · Spirit dominant, Fate secondary, Body tertiary"* (card `:43`) — no Attraction Path at any weight.** `SA-NUM-ECHELON-ATTRACTION-GATE`. |
| **Path gate — Dominion Command** | **FAILS: needs Attraction Path** | *"**Command** requires Attraction Path at Stage VIII to exceed SS"* (Part Seven, `:146`). EX is past SS. Same absence. |
| **Path gate — Harmonics Empathy** | **FAILS: needs Attraction Path** | *"**Empathy** requires Attraction Path at Stage III to exceed C"* (Part Seven, `:134`). The lowest gate on the page and he does not meet it either. |
| Path gate — Dominion Sovereignty | **meets** | *"requires Fate Path at Stage VI to exceed A, and Stage IX to exceed SSS"* (Part Seven, `:146`). Fate secondary ✓. Card: **Dominion Sovereignty 1,500, at ceiling**. |
| Path gate — Harmonics Suppression | **meets** | *"**Suppression** requires Spirit Path at Stage V to exceed A"* (Part Seven, `:134`). Spirit dominant ✓. |
| Sub-Stat data | **Empathy and Suppression carry no card figure** | The card lists Harmonics **Attunement 1,440** and **Stability 1,350** and neither of the two the FOW line names. The page concedes this itself: *"Resonant Pair: None claimed; insufficient Sub-Stat data in the source"* (`:53`). |
| Starvation margin | `null` | No EU figure, no reserve figure. |

**Does the physics close against the stratal account?** **The physics closes better than almost any
page in this batch, and the stratal account does not close at all.**

The physical half is the batch's best-argued: the mechanism is named correctly, the threshold is a
real theorem, the after-effect is *predicted* by the mechanism rather than bolted onto it, the radius
survives a propagation check with six orders of magnitude to spare, and the cheapness of
phase-setting is exactly why a five-kilometre working is affordable at all. Four independent marks in
its favour.

**What does not close is the other set of books, in three places, and they point the same way.**
(i) The category is **Concordia**, the *Spirit-**Attraction*** Apex, which the taxonomy says *"requires
both: Spirit-side precision to align many Essence Cores without flattening any, and **Attraction-side
reach** to hold that alignment as a lasting Domain"*
(`wiki/The Magic System/The Magical Categories — Unified Taxonom.md:206`). (ii) Three of the five
Sub-Stats the FOW line names — Radius, Command, Empathy — **gate on Attraction Path** at Part Seven.
(iii) The plane being merged with is organised *"**By bond**"* and lit by *"**Recognition**"*, and the
Four Paths register says in its own words that *"**Attraction Path routes through bond and
recognition**"* (`The Four Paths Routing, Recognition and the Gate.md:18`). **Three independent
derivations, from three unrelated pages, that World Echelon is an Attraction Path working — and
Francis's card carries no Attraction Path at all.** That is the finding of this account.
`SA-NUM-ECHELON-ATTRACTION-GATE`.

And one more that the taxonomy states and the mechanism contradicts outright: Concordia aligns many
Essence Cores **"without flattening any"**, while Kuramoto coupling drives the whole population onto
one phase, which is flattening in the only sense the word can carry here.
`SA-CROSS-ECHELON-CONCORDIA-FLATTEN`.

**Conflicts logged from this page:** `SA-NUM-ECHELON-ATTRACTION-GATE`,
`SA-PHYS-ECHELON-SOUL-PLANE-VIBRATION`, `SA-PHYS-ECHELON-ONE-DIRECTIONAL-BOND`,
`SA-CROSS-ECHELON-DISTANCE-VS-BOND`, `SA-CROSS-ECHELON-SPIRIT-WORLD`, `SA-CROSS-ECHELON-RADIUS`,
`SA-CROSS-ECHELON-CONCORDIA-FLATTEN`, `SA-CROSS-ECHELON-JUDICIUM-INJURY`,
`SA-EM-ECHELON-EVERY-VS-DEVIATION`, `SA-GAP-ECHELON-AUS`, `SA-GAP-ECHELON-DEPHASE-TIME`,
`SA-NUM-FRANCIS-ASCENDED-FLUX`, `SA-FAIR-ECHELON-NO-SUB-PEER-ROUTE`, and, carried:
`SA-NUM-ETA-TIER`, `SA-CROSS-FRANCIS-ABSOLUTE-CRYSTAL`, `SA-NUM-ZENITH-CONVENTIONAL-METRICS`,
`SA-GAP-TURN-LENGTH`, `SA-GAP-EU-FORMULA`, `SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR`,
`SA-UNATT-COHERENCE-BAND`, `SA-CROSS-AUS-LADDER`.

---

## 5 · Counterplay and the challenge

**The fairness check** (`.claude/skills/wotr-write/references/fair-play.md`).

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **pass, weakly** | *"High soul-heating and a local Principle drift that outlasts the working itself."* The soul-heating is his and reads at 7 % bleed. **But the drift is billed to the district, not to him**, and the page attaches no duration, no figure and no consequence to it. Compare `Dirge Ascension`, which bills one percent of his Crystal per use, permanently. This is the softer of his two Domain-scale workings by a wide margin, and it is the larger one. |
| Stated limits | **pass, and they are good ones** | Five kilometres, forty seconds, **cannot run alongside `Dirge Ascension`** — a real opportunity cost between his two best workings — and the rough seat's seam, which the page names honestly. Unstated but derivable: the lock threshold rises as the population's emotional variance rises, so **a divided district is a harder court than a united one.** |
| Something beats it | **FAIL, on availability** | The page names two counters and both sit at or above his own register: *"A **Sovereign-tier** Spirit Path practitioner, or a **transcendent-grade** Harmonics Empathy field (Catharsis- or Benediction-class)"* (`:20`). Nothing is offered to anyone below that tier — although, as below, the mechanism itself hands a reader at least three sub-peer routes. `SA-FAIR-ECHELON-NO-SUB-PEER-ROUTE`. |
| It has a tell | **pass, and it is a strange one** | *"Francis declares the merger"* (`:36`) — declared, so audible. And then the crowd starts moving together, which is the most visible tell in the batch and the hardest to interpret from inside, because the person noticing it is also in it. |
| Numbers in band | **FAIL** | Grade and Stage agree (EX, Dominion 1,480, ceiling 1,500). But **three of the five governing Sub-Stats gate on a Path his card does not carry** (`SA-NUM-ECHELON-ATTRACTION-GATE`), **η 0.93 is below the Tier 8 floor** (`SA-NUM-ETA-TIER`), the FOW line names two Harmonics Sub-Stats the card does not carry at all, and the working has **no AU/s figure that is not borrowed from a state it forbids** (`SA-GAP-ECHELON-AUS`). |

**The Counterplay routes that work** — including the three the page does not name
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Deny the field — Silence, the named route's honest form.** *"The removal of magical possibility
  from a region, which is not shielding and not counterspelling."* A court cannot convene where
  lawful transformation cannot be authorised. Note the register's field diagnostic, which matters
  here more than usual: *"A soul held in one reports the sensation as **loneliness** rather than
  weakness"* — and loneliness is the exact opposite of what being inside the Echelon feels like.
- **Deny the field — choose the ground by Family, unnamed by the page.** *"Fulguria fails against
  boiled leather, fired clay, dense fog and a shielded interior. **The counter-Fulguria kit has been
  leather and ceramic for four centuries and it is not a secret.**"* Judicium is a Fulguria
  Wellspring and the page's own Physics Domain is electromagnetism. **The cheapest counter to a
  five-kilometre tribunal is the quarter it is held over**, and it costs a tanner's bill.
- **Break the boundary — detune, unnamed by the page and handed over by the mechanism.** Entrainment
  only holds inside the **Arnold tongue**: a driven oscillator locks to a drive only while the
  frequency detuning sits within a range set by the coupling strength, and **outside that range it
  does not lock at all**, however long the drive runs
  ([*Arnold tongue entrainment reveals dynamical principles of the embryonic segmentation clock*,
  eLife **11**:e79575 (2022)](https://elifesciences.org/articles/79575);
  [*How Coupling Determines the Entrainment of Circadian Clocks*,
  arXiv:1107.5137](https://arxiv.org/pdf/1107.5137)). This is the same defence `Symphonia Ascendens`
  already put in the record against Serenyra — *"a chaotic, non-repeating Essence pattern gives the
  sigils nothing consistent to grip"* — and it is stronger here, because a court that cannot couple
  to you records **no deviation at all**, which is to say no evidence.
- **Break the boundary — Knot and Lock.** *"They do not oppose a law, because laws cannot be opposed.
  They condition the conditioning."* **Lock** *"occupies a limit so no other limit can be set there"*,
  and this working's entire boundary is one scalar limit on variance. **Lock is the textbook counter
  to a working whose boundary is a single parameter**, and the page does not mention it.
- **Break the man — Rigidity, and the choice between his own two Domains.** *"A Trait's law is not
  negotiable by its bearer. Present him with the situation his own law handles worst and he will
  handle it that way regardless."* His card carries **Paradox Stasis**: *"Every Celestial, regardless
  of Choir, freezes when presented with two contradictory Oaths of equal metaphysical weight"* (card
  `:89`). **A court is a machine for surfacing contradictory oaths**, run by a man who freezes when he
  meets two of equal weight, across five kilometres, for forty seconds. And because World Echelon and
  `Dirge Ascension` cannot coexist, every second of the court is a second he is not ascended.
- **Wait out the drift, which is not "waiting for the cost."** The register forbids the general plan —
  *"A plan that consists of surviving until he tires is a plan to be killed by a tired man"* — but
  forty seconds is **printed on the page**, the way `Dirge Ascension`'s forty-five is. A counted
  window is not a guess.

**The tell, stated plainly.** He says it out loud, and then a district starts breathing together.

**The lookup trail.**

1. `wiki/Techniques/World Echelon.md` — the radius, the forty seconds, the Kuramoto line, and the
   Weakness naming the Spirit/Fate seam.
2. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — Silence and its loneliness
   diagnostic, the Family-terrain table, and Knot and Lock.
3. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`
   — Part Seven, the Path gates on Dominion Radius, Command and Sovereignty and on Harmonics Empathy
   and Suppression. This is the page that turns the card's Path line into a question.
4. `wiki/The Magic System/The Four Paths Routing, Recognition and the Gate.md` — what Attraction Path
   is, what a rough seat is, and the Tier Four certification cap.
5. `wiki/The Magic System/The Magical Categories — Unified Taxonom.md` §20 — what Concordia requires,
   and the phrase *"without flattening any"*.
6. `wiki/Cosmology & Metaphysics/The Crossing and the Making of the God Hand.md` — the Soul Plane by
   vibration, light and organisation, which is the page a reader needs before any claim about a
   radius on that plane means anything.
7. `wiki/The Eight Families & the Sixty Wellsprings/Fulguria — Electromagnetism.md` — Judicium's law,
   and its Spectral overload failure.
8. `wiki/Materials, Alchemy & Trade/The Heresiology of Alchemy.md` — *Wellsprings Most Frequently
   Injured*, and what the doctrine says happens to Judicium.
9. `wiki/Volume I — Character Cards/Francis Alexander · The Crimson Dirge of Atonement.md` — the Path
   line, the one-directional Attraction Layer, Paradox Stasis, and η 0.93.

**Conflicts added by this section:** `SA-FAIR-ECHELON-NO-SUB-PEER-ROUTE`.
