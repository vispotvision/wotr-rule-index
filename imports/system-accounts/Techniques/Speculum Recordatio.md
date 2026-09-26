---
page: wiki/Techniques/Speculum Recordationis.md
section: Techniques
practitioner: Serenyra Vaelith · The Archmagus of the Grove-Spired Crown
card: wiki/Volume I — Character Cards/Serenyra Vaelith · The Archmagus of the Grove-Spired Crown.md
wellspring: Oneirion (primary) · Mirithane (secondary)
family: Limina
stage_floor: VI
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · Speculum Recordatio

## 1 · Physical account (physics)

**The phenomenon in plain words.** A woman watches a spell being cast at her, copies it while it is
still in the air, and throws the copy into it. The two meet, and what comes out the other side is a
broken-sounding version of the original that goes back the way it came.

**The real phenomenon.** **Feedforward active noise control** — the one real technology that does
exactly this, and the only one whose failure modes are all already on the page. A reference sensor
measures a disturbance upstream, a controller computes its inverse, an actuator emits the inverse, and
superposition does the rest. Every limit the page states is one of ANC's limits, and the question the
page says nobody can answer has a closed-form answer.

**(a) The law is superposition, and the arithmetic of a near-miss is unforgiving.** Take the incoming
working as a wave of amplitude A and the answer as an anti-wave of the same amplitude with a phase
error θ from perfect inversion. The sum is

> |A − A·e^(iθ)| = **2A·|sin(θ/2)|**

and that single expression contains the whole working:

- **θ = 0** — perfect inversion, output zero. Total nullification.
- **θ = 5.7°** — output 0.1 A, which is **20 dB of cancellation**. This is not a derived curiosity: it
  is the working tolerance of real active noise control, where 20 dB of attenuation requires the
  amplitude match to hold within **1 dB** and the phase within **6°**, and the correlation between
  disturbance and anti-signal to exceed 0.995.
- **θ = 60°** — output **equal to the original.** The answer has achieved nothing at all.
- **θ = 120°** — output **1.73 A, +4.8 dB.** The Recordatio has made the incoming working **stronger.**

**So the working has a hidden sign change at sixty degrees**, and above it the technique is an
amplifier pointed at its user. **The page does not have this failure mode**, and it is the sharpest
counterplay route on the page (`SA-PHYS-RECORDATIO-REINFORCEMENT`).

**(b) The page's Counter is the causality condition of feedforward control, stated exactly.** *"A
caster who finishes an effect instantaneously, before the Thesauriel completes its imprint, is never
caught by it"* (`:20`). Feedforward cancellation is **causal**: the reference measurement must reach
the controller, and the controller's output must reach the cancellation point, *before the disturbance
does*. No upstream time, no cancellation — not as a difficulty but as a theorem. Every ANC installation
in the world is a bet on that time budget, and the page has made the same bet and named the same loss.

**And unlike the Nexus on the neighbouring page, this budget closes comfortably.** Range is *"up to a
kilometre"* (`:29`); light crosses it in **3.3 µs**; her reaction floor at the working's **A-Grade** is
**0.2–1 ms** (Part Six). Against an **A-Grade** working travelling at Mach 10–30 (3.4–10 km/s) a
kilometre takes **100–290 ms**; against **S-Grade** Attack Speed at Mach 50–500 (17–170 km/s) it takes
**6–60 ms**. **She has between six and three hundred times the time she needs.** The kilometre is not
decoration — it is the reason the working is causally possible at all, and a Recordatio cast at contact
range would fail on the same theorem its own Counter names.

**(c) The page's "What nobody knows" is answered by the same arithmetic, and the answer is that the
echo is not a copy.** The page asks *"Why the echo comes back fractured and dissonant rather than a
clean copy of the original, when every other part of the recording is exact"* (`:21`). The premise is
the error. **An exact record does not buy an exact inverse, because the inverse has to be *timed* as
well as shaped**, and phase error scales with frequency:

> θ = 2π·f·δt

With δt her own processing latency, the 6° tolerance holds only up to **f = 0.0159/δt**, and the 60°
sign change arrives at **f = 0.167/δt**:

| Her latency δt | 20 dB cancellation up to | Cancellation ceases at | Above that |
|---|---|---|---|
| **200 µs** (A-Grade floor) | **80 Hz** | **833 Hz** | reinforcement |
| **1 ms** (A-Grade ceiling) | **16 Hz** | **167 Hz** | reinforcement |

**So the thing that comes back is the residual**, and a residual has a shape: the low end of the
spectrum subtracted almost to nothing, the middle partly cancelled, the top **doubled and at scrambled
phase**. Broadband content with its fundamentals removed and its upper partials reinforced out of phase
is not a quiet version of the original and it is not a copy of it. **It is the exact acoustic
description of something fractured and dissonant.** The page's open question is its own mechanism
working correctly, and *"every other part of the recording is exact"* is true and irrelevant — the
record is exact and the clock is not.

**(d) And the cancellation is local, which nobody has costed.** Two anti-phase sources cancel only
where the path difference between them is small compared with a wavelength; a step away from that
surface and the same pair reinforces. This is why real ANC produces a **zone of quiet** around its
error sensor rather than a quiet room, and it is why the page is right to say *"the collision is where
the two workings would otherwise have completed themselves"* (`:31`) — a cancellation has a *place*.
**What the page does not say is what happens a few metres outside that place**, where the same two
workings are in phase. Part Eleven gives A-Grade Contact Range at 3–10 m and a Passive Pressure Field
*"Sky hums within 200 m"*, so the geometry of a near-miss matters at exactly the scale a fight happens
at.

**(e) The Limit and the Weakness are one constraint, correctly identified.** *"Only Essence-based or
Aetheric workings leave a signature to record; mundane projectiles and A-Temporal Void effects have
nothing to copy"* (`:19`). Feedforward control cannot act on a disturbance its reference sensor does not
measure — the whole method is *measure, invert, emit*, and an unmeasured disturbance is invisible to
it. A crossbow bolt is not immune because it is humble; it is immune because it is not on the channel.
**This is the same law as the decoy discrimination on the neighbouring page, read from the other end:
there, what you do not measure you cannot reject; here, what you do not measure you cannot cancel.**

**Energy budget, stated.** Not computable and, unusually, not needed: the working supplies no energy of
its own to the collision. Superposition is not a process that consumes anything — the incoming working's
energy is redistributed across the spectrum and the geometry, not destroyed, which is why *"nullifies,
prematurely detonates, or feeds an equivalent working back onto its own caster"* (`:32`) are three
outcomes of one mechanism rather than three effects. **The joules stay the original caster's
throughout**, which is the cleanest illustration in the batch of *"The practitioner does not supply the
joules. They supply the boundary condition"*. What she supplies is a phase. **Fault class:** **Boundary
fault** — *"The condition was established imprecisely and the law ran somewhere unintended"* — and no
page in this batch earns that classification more literally, because an imprecise phase *is* the
imprecise condition and the law then runs as reinforcement.

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** **Limina** for both Wellsprings, *"**Spirit** primary · **Medium** at Veil-Thin
density and above"*, favoured by *"Darkness, silence, Aether-thin ground, ruins"* and suppressed by
*"Saturated Aether, crowd density, **active Domains**"* (`wiki/The Magic System/The Eight Families &
the Sixty Wellsprings.md:154`). *"Terrain is not flavour. It is a modifier on η."* **A counter-working
is used where fighting is, and fighting is where crowds and Domains are**, so this working's Family
fails in its own operating environment — and whether her own Domain is among the suppressors is open
(`SA-GAP-LIMINA-OWN-DOMAIN`).

**Wellspring stratum — Oneirion, *The Wellspring of Dream*, Limina.** Verbatim from
`wiki/The Eight Families & the Sixty Wellsprings/Limina — Entropy, Void and Mind.md:47`:

> **Analogue** · Configuration space. A system's state as a point in an abstract high-dimensional
> manifold.
> **Mechanism** · A mechanical system's every possible arrangement is a coordinate in a space that has
> no physical location, and the system's evolution is a trajectory through it. Oneirion lets a working
> act on that manifold rather than on the room. This is the mechanical reason Oneirion techniques
> reach targets no line of sight connects, and the reason they are so difficult to describe afterward.
> **Failure** · Projection error. The trajectory was correct in the manifold and lands nowhere in
> particular when it is mapped back down into a room.

**Oneirion is the right law for a *record* and the wrong one for a *collision*, and the register says
so in its Failure line.** Acting on the configuration-space trajectory is exactly how you hold a
working's whole structure as one object rather than as a sequence — which is what an imprint has to be.
But the collision happens **in a room**, at a place, at a time, and *"projection error"* is the
register's name for a trajectory that was right in the manifold and lands nowhere in particular when it
comes back down. **That is the phase error of §1c in the register's own vocabulary**, and it means the
fracture is not a defect of this working but the standing failure mode of its primary Wellspring. The
page says the technique *"reach[es] targets no line of sight connects"* nowhere and instead requires
*"cast within her line of sight"* (`:29`), which is the page declining Oneirion's most useful property
in order to keep the causality budget of §1b. That is a good instinct and it goes unremarked.

**Wellspring stratum — Mirithane, *The Wellspring of Reflection*, Limina.** Verbatim, same file `:40`:

> **Analogue** · Specular reflection. The law of reflection; the phase-conjugate mirror.
> **Mechanism** · A true mirror adds nothing. Angle in equals angle out, and fidelity is defined
> entirely by the absence of introduced distortion. A phase-conjugate mirror goes further and returns
> a wavefront that undoes its own aberration on the way back. Mirithane makes the Shell such a
> surface, so what leaves the practitioner is what was in them, with no flattering correction applied
> in transit.
> **Stat Effect** · Strengthens Harmonics Fidelity, Tempering Coherence. Output becomes a more honest
> reflection of internal state.
> **Failure** · The mirror does not discriminate. A practitioner in a state they would rather not
> broadcast broadcasts it perfectly.

**Here the phase-conjugate clause finally earns its keep, and it is worth saying so after the
neighbouring page.** `Speculum Harmoniae` invoked the conjugate mirror to launch an independent double
forward, which is the one thing a conjugate mirror cannot do
(`SA-PHYS-SPECULUM-CONJUGATION-DIRECTION`). **Speculum Recordatio wants precisely what a conjugate
mirror is for:** a wave sent *back* along the incoming path, phase-inverted, aberration-corrected
against the medium it crossed on the way in. *"Aimed back at the original"* (`:30`) is the conjugate
geometry exactly. **Two workings on adjacent pages, the same register cited on both, and only this one
uses it in the direction the physics runs.** The page never mentions Mirithane's law at all — its
Mechanism reaches straight for destructive interference — so this is the register supporting a page
that did not ask it to.

**And Mirithane's Failure is a cost the page has not noticed it is paying.** *"The mirror does not
discriminate."* The Recordatio's answer is built from *her* Shell, phase-inverted; an honest mirror
adds nothing and removes nothing, so what goes back down the line toward the original caster carries
her fidelity along with the inversion. **Every use tells the man she is answering something true about
the state she is in while answering** — which, for a working whose Cost is a blank space in her recent
memory and *"a moment of mental static"*, is a great deal to broadcast at the person best placed to use
it.

**The Sub-Stat list derives from the registers and misses the cost, again.** The page's FOW line is
*"Governing Primary Gnosis (Diagnosis, Perception) and Harmonics (Fidelity)"* (`:42`). Under the Merge
Ledger Diagnosis → **Analysis** and Fidelity → **Attunement**, and Perception stands. Those are
Oneirion's and Mirithane's Stat Effects and nothing else. **But the page states its cost in Retention's
own unit** — *"One memory slot per use"* (`:37`) — against Part Twelve's *"**Retention** — Clarity and
accessibility of the Crystalline Memory structure under pressure, and **the number of complete working
structures held loaded in active cognitive memory** without external inscription"*. A memory slot is a
Retention slot; the system has the stat and the page has the unit and they are not connected
(`SA-CROSS-RECORDATIO-RETENTION-SLOT`). This is the second Serenyra page in a row to charge a Retention
cost without naming Retention (`SA-CROSS-SPECULUM-RETENTION-DENSITY`).

**Which of the Four Theories.** **Correspondence**, and the most literal instance of it in the batch: a
thing is answered by its own likeness, and the likeness has power over it *because* it is a likeness
and to the exact degree that it matches. The page's own arithmetic is a correspondence gradient — 6° of
mismatch is twenty decibels of authority, 60° is none, 120° is help. **Residue** runs underneath, since
what the working leaves behind is a record and a gap in one.

**Essence stratum.** Craft **Runecraft**, and the card agrees: *"**Craft** · **Runecraft first,
Spellcraft second.** *Thesauriel writes lattices directly into reality without verbal incantation*"*
(card `:41`). The substrate is the instrument: *"**Thesauriel, the Mirror Codex** · *Compendium-focus.*
**Writes complex lattices directly into reality without verbal incantation.** *Runecraft in a book*"*
(card `:96`). Crystal State *"Refined"*, η *"~0.70, Band B"*, Developmental Tier **Radiant**, Tier of
Standing **6 · Master**. **The invoice:** a memory slot, a paroxysmal surge, and an instrument held
open in both hands in the middle of a fight.

**The lens: Hooke's *Micrographia* on the memory as a coil, and the mnemonic art it came out of.**
Robert Hooke, *An Hypothetical Explication of Memory* (the Royal Society lecture of 1682, printed in
the *Posthumous Works*, 1705), standing on the *ars memoriae* of Camillo's *L'Idea del Theatro* (1550)
and behind that on the *Ad Herennium*. Hooke proposed something startling for its century and exactly
right for this page: that memory is **a physical store of a finite number of discrete ideas**, laid
down in order like beads on a coil, counted rather than merely felt — he was willing to estimate the
total, which no one had done. Retrieval, for Hooke, is the soul's attention travelling the coil to a
**place**, and remembering is therefore a spatial act with an address and a cost. The mnemonic
tradition he inherited had already built the same picture as a discipline: a memory is a thing put in a
room, and to recall it you go there.

**Speculum Recordatio is that picture used as a weapon.** *"One memory slot per use"* is Hooke's
arithmetic said out loud — a countable store, spent by the unit — and *"she is left with a blank space
in her recent memory"* is what it looks like when you take a bead off the coil and put nothing back.
The Thesauriel is Camillo's theatre in the hand: a place to keep structures so the mind does not have
to, which is why the card calls it *Runecraft in a book* rather than a spell.

**The productive misreading, and what it kills.** A **Theatrist** school reads the coil as *storage*
and draws the natural conclusion: if a slot is a slot, **any slot will do**. So they train to file
aggressively and widely, keeping every working they have ever been shown, on the understanding that a
larger library is a better counter-library — and they treat the blank space the technique leaves as
shelf space rather than as a loss. The doctrine is disciplined, produces prodigious readers, and is
taught with pride.

**What kills them is the clock, and the doctrine has no word for it.** §1c is the whole of it: the
record is exact and the answer still fails, because an inverse must be *timed* and timing is not
stored. A Theatrist with ten thousand filed workings and a two-hundred-microsecond latency can cancel
nothing above eighty hertz and **reinforces** everything above eight hundred, and he will read that as
a filing problem — the wrong structure recalled, the library insufficiently complete — and answer it by
filing harder. **The school's masters are its most comprehensive archivists, and they die facing fast
opponents while reaching for the correct page.** Worse, they die assisting: above the sign change at
sixty degrees the answer adds to what it was sent to stop, so the last thing a Theatrist master does is
make an incoming working brighter, from memory, perfectly.

---

## 3 · Mechanism (the effect)

**The glyphs, proposed.** `[Lk]` **Lock**, `[Me]` **Measure**, `[Rt]` **Return**. The Index is
categorical about what a counter-working can be — *"The only two Counter forms in the index, and they do
not oppose a law, because laws cannot be opposed. They condition the conditioning"* — and **Lock** is
the one that fits to the word: *"**Lock** occupies a limit so no other limit can be set there."* The
page says the collision happens *"where the two workings would otherwise have completed themselves"*
(`:31`), which is Lock's definition with the furniture moved. The page names no glyph, so all three are
filings under the Standing Note and none is canon until ruled (`SA-GAP-GLYPH-MIRROR`).

**What boundary moves.** Not the working, and not its energy. **The boundary that moves is the phase a
copy is permitted to hold relative to its original.** Ordinarily a likeness of a thing is *in phase*
with it — that is what makes it a likeness, and it is why two copies of a working reinforce rather than
cancel, which is the default the system states as Concordia's whole premise on the neighbouring page.
The glyph pins the copy at inversion. Nothing is created and nothing is opposed: *"A glyph creates
nothing and carries no power. … It moves a limit, and the law does what it has always done on the far
side of the new limit."* On the far side of this limit, superposition subtracts.

**What the law then does on its own — and it does not care which way it comes out.** This is the part
the page under-reads. Superposition is not a counter-mechanism; it is an addition, and the only thing
that makes it a *counter* is the sign. Hold the inversion to six degrees and the incoming working goes
to a tenth of itself. Miss by sixty and nothing happened. Miss by a hundred and twenty and **the law
has helped**, at +4.8 dB, with no change of mechanism and no warning, because addition was all it was
ever doing. **The Recordatio does not nullify workings. It adds a phase to them, and nullification is
one of the outcomes of having done that.**

**Then the residual goes back the way the original came.** Mirithane's conjugate geometry is what makes
*"aimed back at the original"* a property rather than an act of aiming: a conjugate return retraces the
incoming path, so the answer finds the caster the way the caster found her, through the same air and
with the same aberrations undone. She does not have to know where he is. She has to have been hit by
him.

**The failure modes, and the page has two of four.** **Overload** and **pass-through** are stated
(`:32`, `:36`): a working two Tiers above her ceiling breaks the recording, and force beyond the
Thesauriel's hold goes through the ward. Not stated: **reinforcement** above the sixty-degree crossover
(§1a), which is a failure that looks like an attack she performed on her own side; and **projection
error**, Oneirion's own, which is the same thing arriving from the register rather than from the
arithmetic. And under all four, **Wards** — the Counterplay register's standing answer to Runecraft:
*"damage the substrate."* The Thesauriel is the substrate, it is a book, and she is holding it.

**What the target sees and feels.** He casts, correctly, at a woman holding a book, and for a moment
nothing is wrong. Then his own working is **in front of him twice** — not blocked, not shielded, not
unmade: answered, by something with his own shape and his own signature that he did not make and
cannot disown. There is no wall and nothing absorbs. The two meet where his working was going to
finish, which is the insult of it: the interception is not defensive, it is *punctual*.

What comes back is worse than a reflection. A reflection would be recognisable. **This is his working
with its bottom taken out of it** — the weight gone, the fundamentals subtracted, and everything sharp
in it doubled and off-key — so that the thing arriving at him is unmistakably his and unmistakably
wrong, the way his own voice is wrong on a recording. If he has misjudged the exchange, he learns it
here: the same mechanism that should have quietened his working has instead handed it back **louder**,
and it is still his, and it is still aimed the way he aimed it. Then a woman across the field loses a
few seconds of her own afternoon and looks, briefly, like someone who has stood up too fast.

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| EU spent | `null` | Page states none; no formula converts a Stage into EU (`SA-GAP-EU-FORMULA`). |
| **Energy supplied by the working** | **zero, and correctly** | Superposition redistributes; it does not consume. The collision's joules are the original caster's throughout, which is why *"nullifies, prematurely detonates, or feeds an equivalent working back"* are one mechanism and not three (`:32`). **The purest instance in this batch of supplying a boundary condition rather than joules.** |
| Flux Density | **31.4 EU/g** | AU/s ÷ η = 22 ÷ 0.70, carried from `Lumen Dissecans` (`_method.md` §VIII); not a figure this page states. |
| η | **~0.70, Band B** (card `:39`) | **In band** — Tier 6 · Master is 0.70–0.80 (Part Nineteen), at its floor. |
| Bleed fraction | **30%** | 1 − η, *"as heat, sound, and structural bleed"* — and on this working the bleed is itself a phase error, so it is not merely waste. |
| **Cancellation tolerance** | **±6° phase, ±1 dB amplitude for 20 dB** | 2A·sin(θ/2) = 0.1A ⇒ θ = 5.7°, which is the working tolerance of real active noise control and its stated correlation requirement of >0.995. |
| **Sign change** | **θ = 60°: no effect · θ = 120°: +4.8 dB** | 2A·sin(θ/2) ≥ A for θ ≥ 60°. **Above 60° the working amplifies what it was cast to stop** (`SA-PHYS-RECORDATIO-REINFORCEMENT`). |
| **Frequency ceiling, derived** | **20 dB up to 16–80 Hz · reinforcement above 167–833 Hz** | θ = 2πf·δt with δt = her A-Grade Reaction Speed, **0.2–1 ms** (Part Six). |
| **Causality budget** | **closes by 6× to 300×** | 1 km in 3.3 µs of light against a 0.2–1 ms reaction floor; an A-Grade working crosses the kilometre in 100–290 ms, an S-Grade one in 6–60 ms. **The range is what makes the working possible**, and the page's Counter is this budget failing. |
| Range | **1 km, and no ladder to check it against** | *"cast within her line of sight, at range up to a kilometre"* (`:29`). This is a sensing and addressing range, not a force envelope, and Part Eleven prices only force (`SA-GAP-RANGE-LADDER`). For scale, A-Grade Projected Force Range is 3–8 km and the A-Grade Passive Pressure Field is *"Sky hums within 200 m"*. |
| Collision locality | **unstated, and it matters at fighting scale** | Anti-phase cancellation holds only where the path difference is small against a wavelength; outside it the same pair reinforces (§1d). A-Grade Contact Range is 3–10 m. |
| **Cost's Sub-Stat** | **Gnosis Retention, and the page uses its unit without naming it** | *"One memory slot per use"* (`:37`) against *"the number of complete working structures held loaded in active cognitive memory without external inscription"* (Part Twelve) (`SA-CROSS-RECORDATIO-RETENTION-SLOT`). |
| **Gnosis Perception gate** | **✓ open** | *"**Perception** open"* (Part Seven). |
| **Gnosis Analysis gate** | **✓ and correctly required** | *"Analysis open, though diagnosis of external fields and living beings requires Spirit Path at Stage IV to exceed B."* Reading a working in flight is diagnosis of an external field; A exceeds B; Spirit is her dominant Path. **The page declares Spirit Path and is right to.** |
| **Harmonics Attunement gate** | **FAIL** | *"Attunement requires **Attraction Path at Stage II to exceed D**"* (Part Seven). A exceeds D. Card: *"Spirit dominant, Fate secondary … The Fate Path routes no force here"* — no Attraction (`SA-CROSS-SPECULUM-ATTRACTION-PATH`, now a fourth working). |
| **Category, Mnemata** | **on her card, and Attraction-side by the taxonomy** | Card `:42` lists Mnemata; the taxonomy makes it *"**Spirit ↔ Attraction**"* and says why — *"memory itself is Soul Plane, but its transmission between souls, generations, or into Domains is Attraction Force at work"* (`SA-CROSS-SERENYRA-CATEGORY-PATHS`). |
| Craft | **Runecraft ✓ and the card agrees first** | Card `:41`: *"Runecraft first, Spellcraft second."* The page picks the card's primary Craft, which is more than most pages in this batch do. |
| Law V, material anchor | **✓ and structurally** | Stage floor **VI**, below Refraction, so an anchor is required — and Runecraft is a Craft that *is* an anchor. The Thesauriel is the substrate. |
| **Thesauriel** | **attested, twice, on her own card** | *"**Thesauriel, the Mirror Codex** · Compendium-focus … Runecraft in a book"* (card `:96`) and card `:41`. **It is an instrument, not an archive**, which is where `Lumen Dissecans` has it wrong and where `SA-UNATT-THESAURIEL` was filed on a false premise; the row is corrected in this batch. |
| **"Cataclysmic-tier casting"** | **not a casting tier** | *"a Cataclysmic-tier casting overloads the recording"* (`:20`). The Tier Grade ladder runs F–EX. **Cataclysmic Entity is T8 on the Bestiary's threat ladder** — *"| **T8** | Cataclysmic Entity | Hydra · Voidwyrm · Cerberus |"* — which prices creatures, not workings (`SA-OFF-RECORDATIO-TIER-VOCABULARY`). |
| **"A-Temporal Void effects"** | **appears nowhere else in the corpus** | `:19`. Same row. |
| **"two or more Tiers above her own ceiling"** | **consistent in spirit, unpriced** | Part Four: *"One full Tier Grade above an opponent wins a direct exchange of that stat category without meaningful contest."* Two full Grades is beyond that, so an overload threshold there is not unreasonable; nothing states what a recording can hold. |
| Minimum Stage | **VI · Glory** | Page ✓ Part Five: Max Grade A, ceiling 400, Tier 5 · Expert. |
| Practitioner's Stage | **VIII · Transcendence**, Level 276, Grade S, ceiling 550 | Card `:59`. Two Stages above the floor, so her latency is better than the A-Grade figures above — Part Six gives S-Grade **0.05–0.2 ms**, which moves the reinforcement crossover up to **833 Hz–3.3 kHz** and does not remove it. |
| "Coherence Band B" (card) | **retired** | Lettered Coherence Bands retired under R42 (`SA-UNATT-COHERENCE-BAND`). |
| Duration | none stated | The working is instantaneous by construction; no turn-length problem arises here, which is rare (`SA-GAP-TURN-LENGTH` not cited for this page's timing). |
| Starvation margin | `null` | Cost is not stated as a fraction of reserve (`SA-GAP-EU-FORMULA`). |
| Aetheric Density check | **cannot be run** | No numeric scale exists (`SA-GAP-AETHERIC-DENSITY`). |

**Does the physics close against the stratal account?** **Better than any page in this batch, and the
one thing the page says is unknowable is the thing the physics settles outright.** Feedforward active
noise control supplies the mechanism, the causality condition, the tolerance, the frequency ceiling and
the sign change; three of those four are already on the page in words, and the fourth is the answer to
its own open question. The Counter is the causality theorem. The Limit and Weakness are the reference-
sensor constraint. The kilometre of range is not scale-inflation but the time budget the method needs,
and it closes by two orders of magnitude. The Craft matches the card's primary Craft, the substrate is
a real instrument named twice on that card, and Law V is satisfied structurally rather than by
assertion. **Mirithane's phase-conjugate clause, misapplied on the neighbouring page, is used here in
the direction the physics actually runs, and the page did not even claim it.**

**What does not close is a sign, a stat and a Path.** The working has an unstated regime above sixty
degrees of phase error in which it **amplifies** what it was cast to stop, which is both its most
interesting failure and its cheapest counter, and neither appears. It charges a cost in Retention's own
unit without naming Retention, for the second Serenyra page running. It borrows a creature threat tier
and an effect class that exist nowhere else as casting vocabulary. And Harmonics Attunement fails the
Attraction gate on a card that denies her Attraction — the fourth working to do so — while three of that
card's four listed Categories are Attraction-side by the taxonomy, which moves the question off the
technique pages entirely and onto the card.

**Conflicts logged from this page:** `SA-PHYS-RECORDATIO-REINFORCEMENT`,
`SA-FAIR-RECORDATIO-NO-TELL`, `SA-CROSS-RECORDATIO-RETENTION-SLOT`, `SA-OFF-RECORDATIO-TIER-VOCABULARY`,
`SA-CROSS-SERENYRA-CATEGORY-PATHS`, `SA-UNATT-THESAURIEL` (corrected in this batch),
`SA-CROSS-SPECULUM-ATTRACTION-PATH` (fourth working), `SA-CROSS-SPECULUM-RETENTION-DENSITY`
(recurrence), `SA-PHYS-SPECULUM-CONJUGATION-DIRECTION` (contrast), `SA-GAP-LIMINA-OWN-DOMAIN`,
`SA-GAP-EU-FORMULA`, `SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR`, `SA-GAP-RANGE-LADDER`,
`SA-UNATT-COHERENCE-BAND`.

---

## 5 · Counterplay and the challenge

**The fairness check.**

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **pass, and it is precise** | *"One memory slot per use, and a paroxysmal Aether surge that leaves her mentally addled for a moment afterward"* (`:37`), with *"a blank space in her recent memory"* (`:18`). A countable resource in the currency she fights with, plus a stated window of incapacity immediately after use — which is the part that makes it cost something *in* the fight rather than after it. |
| Stated limits | **pass, three of them, each load-bearing** | Signature required (`:19`), answers only a working already in flight (`:35`), overloads above two Tiers (`:32`). None is a soft limit and none can be talked around. |
| Something beats it | **pass on the page's two, and the page is missing the free one** | Speed and scale are both correct and both physical (§1b, §1e). **The reinforcement regime above 60° of phase error is a third route and costs the opponent nothing but pace** (`SA-PHYS-RECORDATIO-REINFORCEMENT`). |
| It has a tell | **FAIL, and it is the page's only real omission on this axis** | The page states no tell at all. The working needs a raised instrument and a completed imprint before the incoming working lands — both visible, both takeable — and the aftermath is a woman visibly addled. **The material for a tell is in the page's own Cost and Craft lines and none of it is stated as one** (`SA-FAIR-RECORDATIO-NO-TELL`). |
| Numbers in band | **mixed, with the best record in the batch** | Stage VI, A-Grade, Path gate and Craft all check clean against Part Five, Part Seven and the card. **Harmonics Attunement fails its Attraction gate**; the range has no ladder to check against; and *"Cataclysmic-tier"* and *"A-Temporal Void"* are not system vocabulary (`SA-OFF-RECORDATIO-TIER-VOCABULARY`). |

**The Counterplay routes that work**
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Break the Boundary — "Wards," and here the substrate is a book in her hands.** *"Runecraft standing
  on a substrate, and therefore beaten the way Runecraft is beaten: **damage the substrate.** A ward is
  not argued with. It is chiselled off, or the wall it sits on is brought down."* The page's Craft is
  Runecraft and its instrument is *"Runecraft in a book"*. **The register's standing answer to this
  entire Craft applies, and the page's Counterplay line does not mention it.**
- **Break the Boundary — "Interrupt the chain," which the Stage floor invites.** *"Below Refraction a
  working requires an external anchor: voice, hand, ink or blood. Take the anchor and the sentence does
  not complete."* The floor is **Stage VI**, below Refraction, and the anchor is an object held open.
  Serenyra herself is at Stage VIII and needs none — but she is using one anyway, and the register does
  not ask whether she had to.
- **Break the Body — "Shot," read literally and with the page's blessing.** *"Chemically cheap,
  mechanically simple, and it does not care about Stage."* The page's own Limit: *"mundane projectiles
  … have nothing to copy."* **A counter-magician who has built her defence entirely on the Essence
  channel has no answer to a crossbow**, and the page says so in the Limit line without treating it as
  the conclusion it is.
- **Break the Body — speed, and this is the derived route.** Two tables give it. Part Six's Reaction
  Speed ladder sets her processing floor; the phase arithmetic of §1a turns that floor into a frequency.
  **Fast, sharp, broadband workings are not merely uncancelled — above the crossover they come back
  reinforced**, so the correct answer to a Recordatio is not a bigger working but a quicker one, and the
  opponent who finds this gets her defence to attack for him. A player assembles it from Part Six, Part
  Eleven and the page's own Counter line.
- **Deny the Field — "Choose the ground by Family," and a counter-caster cannot pick her ground.**
  Limina is suppressed by *"Saturated Aether, crowd density, active Domains."* **Those are the
  conditions of any engagement worth countering in**, so this working's terrain penalty is paid every
  time it is used, which is unusual and is not stated.
- **Break the Man — "Read him," inverted, because she is the one who reads.** *"Every thaumaturge has a
  pattern."* Hers is on the page: she answers with a likeness, so **an opponent who casts a working he
  is willing to have returned to him is making her fight his exchange.** A working whose reversal he can
  survive and she cannot is a trap the page's own Consequence line builds for her.
- **Break the Man — "Make him hold Pressure in," against the aftermath.** *"Suppression is a skill and
  it is tiring."* Each use leaves her *"mentally addled for a moment"* with a hole in her recent
  memory, and the register's answer to any cost that lands *in* the scene is to force it repeatedly.
  **Make her spend slots.**

**The tell, stated plainly.** The page gives none, so here is what the page's own lines contain: an
instrument raised and held open before the incoming working arrives — not a gesture but a book, and a
completed imprint takes time she must be seen to spend; then, immediately after the collision, a few
seconds in which she is demonstrably not present, with the specific blankness of somebody who has just
lost the thread of what she was saying. The imprint is the warning and the blankness is the window.

**The lookup trail.** What a player would have to read to assemble any of this. Pieces, not the answer.

1. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`
   — **Part Six's Reaction Speed and Attack Speed rows**, which are the whole of the speed counter, and
   **Part Seven's** Gnosis and Harmonics Gates.
2. `wiki/Fracture of Worlds — The Living System/III. Physical Force (Part Eleven).md` — **Contact
   Range** and the **Passive Pressure Field** column at A-Grade, for the scale a near-miss happens at.
3. `wiki/Fracture of Worlds — The Living System/IV. The Eight Primaries and the Sixty-Four
   Sub-Stats (Part Twelve).md` — **Gnosis Retention**, and the **Merge Ledger** without which this
   page's Diagnosis and Fidelity are not the same list as its registers'.
4. `wiki/The Eight Families & the Sixty Wellsprings/Limina — Entropy, Void and Mind.md` —
   **Oneirion**'s Failure, which is this working's fracture in the register's words, and **Mirithane**
   in full, which is the law the page never cites and most needs.
5. `wiki/The Magic System/The Four Crafts.md` — **Runecraft**, and what it means for a working to stand
   on a substrate rather than on attention.
6. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — **"Wards,"** **"Interrupt the
   chain,"** **"Shot,"** **"Choose the ground by Family,"** **"Read him,"** and **"Make him hold
   Pressure in."**
7. `wiki/Volume I — Character Cards/Serenyra Vaelith · The Archmagus of the Grove-Spired Crown.md` —
   her **Craft** line, her **Categories** line, her **Path** line, and **Thesauriel, the Mirror
   Codex**, which several pages describe as somewhere rather than something.
8. `wiki/The Magic System/The Magical Categories — Unified Taxonom.md` — **§18 Mnemata**, and what it
   says memory costs when it moves between souls.
9. `wiki/Bestiary/The Bestiary.md` — the **threat tier table**, for what *Cataclysmic* actually
   classifies.
10. `wiki/The Magic System/The Master Glyph Index — 136 Attested Forms.md` — the **two Counter forms**,
    and *"They condition the conditioning."*

**Conflicts added by this section:** `SA-FAIR-RECORDATIO-NO-TELL` (also cited in §4).
