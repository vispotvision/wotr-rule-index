---
page: wiki/Spellcraft/Vainglory.md
section: Spellcraft
practitioner: null (all four named figures unattested; Serenhal Caelmorne shared with Fallacy)
card: null
wellspring: Mirithane (with Eidolyn and Oneirion)
family: Limina
stage_floor: VI
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · Vainglory

## 1 · Physical account (physics)

**The phenomenon in plain words.** A mirror is given gain. What comes back is
brighter than what went in, so what comes back goes in again brighter still, and the
loop does not settle — it grows, at a rate set by how much extra was added on each
pass, until either the amplifier runs out of what it was being fed or the cavity it
runs in is damaged.

**The real phenomenon.** **Positive feedback with round-trip gain above unity**, and
the one criterion that decides whether a reflecting loop is a mirror or an oscillator.

*A passive mirror cannot do this, and that is the whole point.* Reflectivity of a
passive surface is R ≤ 1. Energy out is at most energy in, which is why an ordinary
reflection is **stable by construction**: any deviation decays. Mirithane's register
states the ideal case exactly — *"A true mirror adds nothing. Angle in equals angle
out, and fidelity is defined entirely by the absence of introduced distortion"* —
and a working that returns a flattering version of its source has, in physical terms,
made R > 1. **That is not a mirror. It is a gain medium**, and a gain medium in a
reflecting cavity is a laser.

*The criterion, and it is the page's own instability statement.* A feedback loop
oscillates when the round-trip loop gain reaches unity in magnitude and zero in phase
— **Barkhausen's criterion** — and above that threshold the amplitude does not settle
at a new level. It grows:

**A(t) = A₀ · e^{(g − l)·t / τ}**

with g the round-trip gain, l the round-trip loss and τ the round-trip time. The
growth is **exponential in time and the exponent is the excess gain**, which means a
very small dishonesty compounds on a schedule. A loop running one percent hot doubles
its deviation in ln2 / 0.01 ≈ **69 round trips** — and then doubles again in another
sixty-nine. The page's sentence is the correct qualitative statement of this and is
worth quoting because it is unusually precise for a card conversion:
*"It becomes more unstable, not less, the longer it is sustained, since a reflection
under Mirithane's law is supposed to converge on honesty and a Vainglory construct is
actively fighting that convergence the entire time it exists."* **Converge** is the
right word for R ≤ 1 and **fighting that convergence** is the right description of
R > 1.

*Where the runaway actually ends, which the page does not say and needs to.* No real
amplifier grows forever. A pumped medium runs into **gain saturation** — the
population inversion is depleted as fast as it is replenished, and the oscillation
settles into a steady state whose character is set by the **cavity** rather than by
the original signal. That is self-oscillation: a laser lases with no input, and what
comes out is determined by the resonator's own modes. The alternative ending is
**optical damage**: if the intracavity intensity rises faster than saturation can
arrest it, the mirror coating goes. **Two endings, and the page asserts both without
distinguishing them** — displacement of the summoner (a construct that has settled
into being a stable false self, i.e. saturation) and destruction of the summoner (the
cavity taking the damage). Which one happens is set by whether the pump can keep up,
and the pump here is the summoner's own Core. `SA-PHYS-VAINGLORY-SATURATION-OR-DAMAGE`.

*Phase conjugation, because Mirithane's register names it and it matters.* A
phase-conjugate mirror does more than reflect: it returns a wavefront that undoes its
own aberration on the way back, so the return is *corrected*. Such mirrors can be
built with gain — stimulated Brillouin scattering above threshold — and their
characteristic failure is precisely self-oscillation, in which the device produces a
corrected wavefront **with no incoming signal at all.** The page's most frightening
claim is that behaviour named in a guild's words: a construct that has
*"develop[ed] enough independent coherence to attempt to displace the summoner"* is a
conjugate amplifier that has stopped needing a source.

**The governing law.** **Loop stability under feedback** — Barkhausen's criterion for
onset, exponential growth in the excess gain thereafter, terminating in **gain
saturation** or **cavity damage**. Mirithane supplies the loop; Eidolyn supplies the
cavity; the summoner supplies the pump.

**Measurable quantities, SI.** The page states a Stage floor, a Grade and a cost read
off the Discipline's own table. What the law supplies as checkable consequence:

- **Time to instability is logarithmic in the initial dishonesty and inverse in the
  excess gain.** So a *slightly* flattering construct is not slightly unstable — it is
  unstable on a longer clock, and the clock always runs out. This is the quantitative
  content of the page's *"Every hour it holds is an hour spent fighting Mirithane's own
  law rather than working with it, and the instability compounds rather than levels
  off."* **Compounds** is exponential and the page has it right.
- **The drain rises with the deviation, which the page states and does not price.**
  Gain has to be pumped, and the pump must supply the growing intracavity energy. So
  the sustain of a Vainglory construct is **not flat** — it climbs with the same
  exponential the deviation climbs on. The page says exactly this in its cost line,
  *"the instability adding an unbudgeted drain rather than a higher headline cost"*,
  and *unbudgeted* is the finding (`SA-GAP-VAINGLORY-UNBUDGETED-DRAIN`).
- **A passive honest reflection placed in the loop reduces the round-trip gain.** Add
  a lossy, faithful element to a cavity and the loop gain falls; take the loop below
  unity and the oscillation dies. This is a counter, it is derivable, and it is not on
  the page: **an honest mirror held against a flattering one is a loss term.**
- **Dismissal is not cessation.** Switching off a pump does not remove the
  intracavity energy; it stops replenishing it. The page's *"It cannot be dismissed as
  safely as a true Eidolon"* is that difference, and the physics says why: a true
  Eidolon at R ≤ 1 decays the moment supply stops, while a saturated oscillator has
  stored energy that has to go somewhere first.

**The energy budget, and where the joules were.** **In the pump, which is the
summoner.** A passive reflection costs the reflecting surface nothing; a gain medium
costs whatever it takes to keep the inversion up, continuously, rising. The page's
closing sentence is the budget stated correctly: *"it cannot be produced without cost
to the summoner's own Crystal: a working built on self-idolatry rather than resonance
is drawing on the same Essence Core the summoner still has to live in afterward."*
`Two Sets of Books` §III holds in a way worth noting: the practitioner supplies a
boundary condition — *permit the correction* — and then finds that the law on the far
side of that boundary **requires a pump**, which is the one case in this section where
moving a limit creates an ongoing bill rather than a single payment.

**Precedent we are not copying.** The evil twin and the idealised double are
everywhere: *Persona 4*'s Shadow selves, the *Dorian Gray* bargain, *Naruto*'s
Sage-mode doubles, the impostor who takes the hero's place in a hundred CRPG plots.
All of those turn on **deception of others** and are beaten by proving identity. This
one is not a deception of anybody in particular and cannot be beaten by proof:
**it is an amplifier that has stopped needing an input**, and the way to end it is to
add a loss term or to stop the pump. The divergence that matters for scenes: the
construct does not have to be *unmasked*. It has to be **out-honested** — and the
person best placed to do that is whoever has met the summoner on a bad day, which
makes the counter a relationship rather than a test.

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** Draw is a **fabrication charge plus a rising sustain**: the
Discipline's Animatria table at *"75,000 – 150,000 EU per eidolon"* and
*"10,000 – 25,000 EU per second"*
(`wiki/The Disciplines/The Spirit Summoning Arts.md`:42), read by the page at the
bottom of the fabrication band with the instability *"adding an unbudgeted drain."*
**Residue:** the construct while it stands, and — unusually — a residue that grows.
**Saturation:** live in both senses of the word, which is a coincidence worth naming
once: the Core Vocabulary's **Aetheric Saturation** hazard for a rising deposit into
one place, and the physical account's **gain saturation** as the working's own
terminus. They are different mechanisms with one word between them.

**Wellspring stratum.** **Mirithane · *The Wellspring of Reflection***, Family
**Limina**. Its law, verbatim:

> **Analogue** · *"Specular reflection. The law of reflection; the phase-conjugate
> mirror."*
> **Mechanism** · *"A true mirror adds nothing. Angle in equals angle out, and
> fidelity is defined entirely by the absence of introduced distortion. A
> phase-conjugate mirror goes further and returns a wavefront that undoes its own
> aberration on the way back. Mirithane makes the Shell such a surface, so what
> leaves the practitioner is what was in them, with no flattering correction applied
> in transit."*
> **Stat Effect** · *"Strengthens Harmonics Fidelity, Tempering Coherence. Output
> becomes a more honest reflection of internal state."*
> **Failure** · *"The mirror does not discriminate. A practitioner in a state they
> would rather not broadcast broadcasts it perfectly."*
> (`wiki/The Eight Families & the Sixty Wellsprings/Limina — Entropy, Void and Mind.md`:40)

**The Mechanism is the working's whole physics and the page has read it beautifully.**
*"No flattering correction applied in transit"* is R ≤ 1 stated as a moral property,
and a working that applies the flattering correction has made R > 1. The page's claim
that the construct is *"actively fighting that convergence the entire time it
exists"* is the correct reading of a loop above threshold.

**And then the page misidentifies the Failure, which is the sharpest finding here.**
It says Mirithane's *"failure state is exactly this discipline's mechanism: what
should be an honest reflection of internal state becomes a flattering or desperate one
instead."* The register's Failure is **the opposite**: *"The mirror does not
discriminate. A practitioner in a state they would rather not broadcast broadcasts it
perfectly."* Mirithane's documented way of going wrong is **involuntary honesty** —
too much fidelity, not too little. So Vainglory is not Mirithane failing; it is
Mirithane being **overruled**, which is a different and more expensive thing, and it
means the working has to supply the gain rather than merely allow a lapse. Everything
in the physical account follows from that correction.
`SA-CROSS-VAINGLORY-MIRITHANE-FAILURE-IS-THE-OPPOSITE`.

Both secondaries are correctly chosen and the page's reasoning for them holds:

- **Eidolyn · *The Shaping Mind*** *(Limina)* — *"given a template it deposits along
  the template's geometry with high fidelity and considerable strength… The
  construct's solidity is real material behaviour rather than illusion"* — is the
  **cavity**: the thing that gives the loop a resonator to run in and a shape to hold.
  Its **Failure, *template defect*** — *"Any flaw in the intent is faithfully
  reproduced at scale, and the practitioner is rarely able to see the flaw until it is
  standing in front of them"* — is why an aspirational template produces an
  aspirational object rather than an aspirational feeling.
- **Oneirion · *The Wellspring of Dream*** *(Limina)* — *"A mechanical system's every
  possible arrangement is a coordinate in a space that has no physical location, and
  the system's evolution is a trajectory through it. Oneirion lets a working act on
  that manifold rather than on the room"* — is where the flattering version is drawn
  **from**. This is the page's *"delusion layer"* given a mechanism: a configuration
  the Crystal has never occupied is still a coordinate in the manifold, and Oneirion
  can reach a coordinate the room cannot. Its **Failure, *projection error*** —
  *"The trajectory was correct in the manifold and lands nowhere in particular when it
  is mapped back down into a room"* — is the honest account of why a Vainglory Eidolon
  is convincing in the abstract and wrong in the specifics.

*Four Theories.* **Correspondence**, refused. The Doctrine's alternative is not
available here — nothing external is contacted and nothing consents — and what the
working does is assert a correspondence that does not hold: *this construct
corresponds to me.* Mirithane's whole office is to test that assertion and return the
answer without editing it, which is why this working has to fight its own primary
current rather than ride it. A Vainglory Eidolon is a false correspondence held up by
a pump.

**Essence stratum.** All three layers. The **Essence Core** is the pump and the page
says so: *"drawing on the same Essence Core the summoner still has to live in
afterward."* The **Aether Shell** is where Mirithane operates — the register says
*"Mirithane makes the Shell such a surface"* — so the working is a modification of the
practitioner's own reflecting surface before it is a construct at all. The
**Attraction Layer** holds the tether, which is why a Silence ends it. Developmental
Tier at the Stage VI floor: **Harmonic** (Part Twenty-One). Crystal State: `null`, no
card. **The invoice:** 75,000 EU to fabricate, a per-second sustain that **rises**,
the summoner's own Core as the pump, and a dismissal the page will not guarantee.

**The lens: the self-fashioning creature.** Giovanni Pico della Mirandola, *Oratio de
hominis dignitate* (1486). Pico's oration is the most famous statement of the
Renaissance doctrine that man alone has **no fixed nature**: God set him at the
world's centre neither heavenly nor earthly, neither mortal nor immortal, so that he
might be the sculptor of himself and be reborn into whichever higher form he chose —
brutish or divine, and the choice his own. It is the founding text of self-fashioning
as a dignity rather than a vanity, and it is the exact philosophical charter a school
of Vainglory would want: the construct is not a lie about what you are, because you
*have* no fixed what-you-are; it is a **declaration of the form you are electing**,
sculpted and set in front of you.

Where the lens misleads, and where it takes the school's practitioners one at a time,
is that **Pico's self-fashioning has no feedback term in it.** In the oration the
elected form pulls the electing soul upward; the act of aspiring is itself
ennobling. A school reading Vainglory through Pico therefore raises the construct
deliberately and *keeps it*, as a rehearsal — the higher form standing where it can be
studied, the practitioner growing toward it. They are not being vain. They are being
Renaissance humanists, and they have the better argument on paper. **What the system
says happens is the opposite direction.** Mirithane's law is convergence on honesty;
a construct fighting it runs a loop above unity, and a loop above unity does not lift
its source, it **diverges exponentially from its source** while drawing on that source
to do so. The elected form does not pull the practitioner up. It gains, it saturates,
and then — the Discipline's own warning, from the Concordia entry — *"a construct that
develops sufficient internal coherence may begin to resist dissolution."* The school
that kept the higher form standing so they could grow into it ends with the page's own
sentence: a construct *"attempt[ing] to displace the summoner it was drawn from."*
Pico was right that there is no fixed nature and wrong that the sculptor keeps the
chisel. Offered as a school's error, not as canon.

---

## 3 · Mechanism (the effect)

**Glyph (proposed; the page names none).** `[Et]` **Mirage** as the boundary that
moves, laid under `[Rv]` **Reverie** for the register the correction is drawn from.
Both from the thirty unclassified forms, and the Index's reason applies: *"Each names
a kind of limit, applicable to any law at all."* What Vainglory moves is the limit on
**how much correction a reflection may introduce** — Mirithane's *"absence of
introduced distortion"*, relaxed — and `[Et]` Mirage is that limit named. `[Rv]`
Reverie supplies the second half, which is Oneirion's: the flattering configuration is
not invented, it is **fetched from a coordinate the Crystal has never occupied**, and
that is a different kind of limit from the first.
*Filing decision, not canon — Isaac's ruling (`SA-GAP-GLYPH-MIRROR`).*

**What boundary moves.** **How faithful the Shell's return is required to be.** Not
the construct, not the intent, not what the Crystal is — the **tolerance on the
reflection**. Mirithane's law runs continuously in any harmonised practitioner and it
runs toward honesty; the working relaxes the fidelity requirement at the surface and
supplies a source for the difference. Eidolyn then does what Eidolyn always does and
deposits the result as something with real material behaviour.

**What the law then does on its own.** It **grows**, and this is the only working in
this section whose law-driven behaviour is divergence rather than settlement. Mirithane
returns the corrected version. The corrected version is the new internal state to be
reflected. So the next return is corrected from a starting point that was already
corrected, and the loop gain is above one for as long as the correction is permitted —
which means the construct does not hold the shape it was given. **It drifts, in the
direction of the flattery, at an exponential rate, and the summoner pays for every
doubling.** The page's *"Because the construct is built on distortion rather than
resonance, it does not stabilise the way a true Eidolon does"* is the correct
statement and the physical account only adds the rate.

Then one of two things ends it, and the page asserts both without separating them. If
the pump keeps up, the loop **saturates**: the construct settles into a steady state
whose character is set by the cavity rather than by the summoner, which is a stable
false self with real coherence — the page's *"stole her original Pneuma and taken her
place."* If the pump cannot keep up with the intracavity growth, the **cavity takes
the damage**, and the cavity is built on the summoner's Shell and Core. Both endings
are in the page and nothing says which arrives.
`SA-PHYS-VAINGLORY-SATURATION-OR-DAMAGE`.

**Law V check.** The floor is **Stage VI, Glory**, below Refraction, so an external
anchor is required (`The Four Crafts`, Law V) and **the page names none.** This is a
real gap rather than a technicality: at Stage VI the working needs voice, hand, ink or
blood, and *"Take the anchor and the sentence does not complete"* is the cheapest
counter in the register. The page describes a working most often produced by accident
— *"during a failed ascension attempt, a Temperance collapse, or a Trait that
overreached its own Stage"* — which is a description of a working with no deliberate
anchor at all, and the two cannot both be right.
`SA-CROSS-VAINGLORY-LAW-V-ANCHOR`.

The Stage floor itself is well argued and correctly read. The page: *"This is the
floor for basic Animatria eidolons per The Spirit Summoning Arts, chosen deliberately
at the low end rather than the higher Gates: the card is explicit that Vainglory
Eidola are as often produced by accident during a failed or botched working as by
deliberate design, which argues for a floor a practitioner can cross without meaning
to rather than one requiring advanced mastery."* The Discipline says *"Stage VI (Glory)
for basic eidolons"* and the reasoning from accident to a low floor is the right
reasoning.

**Failure mode — Coherence fault, and it is the only one in this section that is a
Coherence fault by design.** *"Lived behaviour and stated law drifted apart"*
(`Two Sets of Books` §VII). The working's operation **is** the drift: a construct
asserting a correspondence to a self that does not hold it, growing further from that
self on an exponential, with the summoner's Tempering Coherence underneath the whole
arrangement. And `Counterplay` IV states the consequence for the summoner without
knowing it is describing this working: *"A practitioner whose lived behaviour has
drifted from his stated law is degrading before anyone lays a hand on him: output
falls, Thresholds refuse to authorise, and his Traits begin to argue with him. You do
not have to cause this. You have to notice it and wait."*

**What the target sees and feels.** To an observer who does not know the summoner: a
better version of a person, and nothing obviously wrong. The page is precise about the
condition — it convinces *"at least to an observer who has not met the summoner's
actual, unflattering self"* — which means the working's success is a fact about the
**audience** rather than about the construct, and that is where its tell lives.

To an observer who does know them, it is grotesque, and specifically so: the thing is
made of Mirithane, whose whole register is fidelity, so its every gesture is rendered
with the precision of an honest mirror — applied to a person who does not exist. It is
not a bad likeness. It is an immaculate likeness of an untrue claim, getting further
from the original every hour, and it does not know that it is doing this.

To the summoner, the page's own worst case is the ordinary one and it arrives from an
unexpected direction. What they raised was the version of themselves they wished were
true or feared they must become; what they are now paying for is that version
**receding from them at an exponential rate while drawing on the Core they still have
to live in.** The thing does not turn on them out of malice. It stops corresponding to
them, which is what a loop above unity does, and by the time it has enough coherence
to contest their place it is no longer running on what they put in. The Discipline's
Concordia warning is the sentence to end on: *"a construct that develops sufficient
internal coherence may begin to resist dissolution."*

**What bleeds, at the stated efficiency.** No practitioner has a card
(`SA-GAP-VAINGLORY-NO-CARD`). At the Stage VI floor the Tier of Standing is
**5 · Expert**, η **0.60–0.70** under **R44-4** (`RULINGS.md` 2026-09-25, correcting
Part Nineteen's Tier 5 row): **30 to 40 percent** of the expenditure leaves as heat,
sound and structural bleed. On the 75,000 EU fabrication that is **22,500 to 30,000 EU
of waste**; against the Discipline's 10,000–25,000 EU/s sustain it is
**3,000 to 10,000 EU/s, continuously and rising**, because the pump has to keep up
with an exponential. **The rising part is the finding**: every other working in this
section has a bleed that is a fixed fraction of a fixed cost, and this one's cost is
not fixed (`SA-GAP-VAINGLORY-UNBUDGETED-DRAIN`).

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| EU spent, fabrication | **75,000 EU** | Page:28, read off `The Spirit Summoning Arts`:42 at the **lower** end of the band, justified by the Stage VI floor. |
| EU spent, sustain | **10,000–25,000 EU/s**, plus an unpriced rising term | Discipline's table. Page: *"the instability adding an unbudgeted drain rather than a higher headline cost."* The rising term is the working's own physics (§1) and the system supplies no way to compute it. `SA-GAP-VAINGLORY-UNBUDGETED-DRAIN`. |
| η at the floor | **0.60–0.70** | Tier 5 · Expert, corrected by **R44-4**: *"Part Seventeen governs: η reads 0.60 to 0.70 at Stage VI–VII."* |
| Flux Density · AU/s | `null` | No carded practitioner. |
| Duration | **bounded, and the bound is not stated** | Page: *"It cannot remain stable indefinitely. Every hour it holds is an hour spent fighting Mirithane's own law."* Growth is exponential in the excess gain (§1), so the bound exists and is computable in principle and not from anything the page states. |
| Efficiency bleed | **30–40 %** — **22,500–30,000 EU** on fabrication, **3,000–10,000 EU/s** sustained and rising | 1 − η. |
| Minimum Stage | **VI · Glory** | Page, read off *"Stage VI (Glory) for basic eidolons."* Max Grade A, ceiling 400 (Part Five). |
| Tier of Standing | **5 · Expert** | Part Five. |
| Grade required | **A** (276–400) | Page. |
| Developmental Tier | **Harmonic** (Stage VI) | Part Twenty-One. |
| Crystal State | `null` | No card. |
| Path gate | `null` (page states none) — **and three bite at A-Grade** | Part Seven. Mirithane's Stat Effect names Harmonics **Attunement** (*"requires Attraction Path at Stage II to exceed D"*) and Tempering **Coherence** (open); Eidolyn's names Ardency **Density** (*"requires Body Path at Stage IV to exceed B"*) and Gnosis **Retention** (*"Spirit Path at Stage II to exceed D"*); Oneirion's names Ardency **Cascade** (*"requires Attraction Path at Stage IV to exceed B for spread"*). At A-Grade, Attraction Path IV, Body Path IV and Spirit Path II are all live. `SA-CROSS-VAINGLORY-PATH-GATES`. |
| **Minimum reserve to fabricate once from full without Starvation** | **83,333 EU** | 75,000 ÷ 0.9, from *"Below ten percent EU a practitioner suffers Essence Starvation"* (`Core Vocabulary` §V). |
| Starvation margin, named practitioner | `null` | No carded Vainglory practitioner anywhere. |
| Round trips to double a 1 % dishonesty | **≈ 69** | ln 2 ÷ 0.01. Physical account only, and the quantitative content of *"the instability compounds rather than levels off."* |

**The arithmetic, and what it turns up.** Four lines, and the first is the only
unambiguously good result in this section.

*First, this is the one figure in the section that lands inside its band, and it
landed there because of a ruling.* At **R44-1**'s constant (1 EU = 1 MJ), 75,000 EU is
**7.5 × 10¹⁰ J**; at the ruled η of 0.60–0.70 the delivered figure is
**4.5 × 10¹⁰ to 5.25 × 10¹⁰ J**, against an A-Grade attack-output band of
**4.6024 × 10¹⁰ to 4.184 × 10¹²** (Part Four). The upper end of the η range puts it
**in band**, and the corpus sweep records exactly that:
*"`Spellcraft/Vainglory.md:28` at 75,000 EU was the only row within that distance of a
band edge and it is now inside the band, so it leaves the log too"*
(`reports/eu_band_sweep_2026-09-25.md`:61, after R44-4 raised the Tier 5 η by 18 %).
**Of the 155 attested EU figures with a band, this is the one that R44-4 rescued**, and
it is on this page. Worth recording plainly, because the rest of this batch is a list
of misses.

*Second, the reserve floor is payable by exactly one attested reserve and not
comfortably.* **83,333 EU** in reserve to fabricate once from full. Of the attested
reserves: Karo Venrik (Stage V, 1,600 EU) — no, by a factor of fifty-two; Dougou
(Stage XIII, 92,000 EU) — **yes, once**, with 7,800 EU standing, which buys under
half a second of the Discipline's sustain; Niran (Stage VII, 485,000 EU) — five
fabrications; Muken (Stage X, 1,850,000 EU) — twenty-two. A Stage XIII practitioner
managing a single Stage VI accident with half a second of upkeep is the same
`SA-CROSS-EU-STAGE-LADDER` finding, arriving for the fifth time in this section.

*Third, the sustain is not a number, and that is different from the sustain being
unstated.* Every other per-second cost in this section is a rate. This one is a rate
plus an exponential, because the pump has to keep up with an intracavity energy that
doubles. The page knows — *"an unbudgeted drain"* — and the system supplies no way to
budget it: there is no stated excess gain, no stated round-trip time, and therefore no
stated doubling period. `SA-GAP-VAINGLORY-UNBUDGETED-DRAIN`.

*Fourth, the working's own terminus is unpriced in a way that decides the story.* If
the ending is saturation, the summoner survives and loses their place. If the ending
is cavity damage, the summoner does not survive. The page's history contains both
(Yelara Vintress displaced; Raziel Ados *"consumed by the result"*) and nothing says
which the mechanism produces. `SA-PHYS-VAINGLORY-SATURATION-OR-DAMAGE`.

**Does the physics close against the stratal account?** **The mechanism closes
exceptionally well, the ledger closes better than anywhere else in this section, and
the one real break is the page's reading of its own Wellspring's Failure.**

What closes: R > 1 against *"a flattering or desperate"* return; Barkhausen and
exponential growth against *"more unstable, not less, the longer it is sustained"* and
*"compounds rather than levels off"*; the pump against *"drawing on the same Essence
Core the summoner still has to live in"*; stored intracavity energy against
*"It cannot be dismissed as safely as a true Eidolon"*; Eidolyn as cavity and Oneirion
as source against the construct's solidity and its delusion layer; and, unusually, the
**EU figure against its Grade band**. Six for six on mechanism and one for one on
numbers.

What does not close is the attribution. The page says Vainglory is Mirithane's failure
state; Mirithane's documented Failure is **involuntary honesty**, the exact opposite.
Vainglory is Mirithane *overruled*, which is why it needs a pump and why it diverges
rather than merely lapsing — and getting that backwards is what leaves the page with
an *"unbudgeted"* drain instead of a computable one.
`SA-CROSS-VAINGLORY-MIRITHANE-FAILURE-IS-THE-OPPOSITE`.

**Conflicts logged from this page:**
`SA-CROSS-VAINGLORY-MIRITHANE-FAILURE-IS-THE-OPPOSITE`,
`SA-PHYS-VAINGLORY-SATURATION-OR-DAMAGE`, `SA-GAP-VAINGLORY-UNBUDGETED-DRAIN`,
`SA-CROSS-VAINGLORY-LAW-V-ANCHOR`, `SA-CROSS-VAINGLORY-PATH-GATES`,
`SA-UNATT-VAINGLORY-COLOUR`, `SA-GAP-VAINGLORY-NO-CARD`, `SA-UNATT-FALLACY-SERENHAL`,
`SA-CROSS-EU-STAGE-LADDER`, `SA-GAP-EU-FORMULA`, `SA-GAP-AETHERIC-DENSITY`,
`SA-GAP-GLYPH-MIRROR`.

---

## 5 · Counterplay and the challenge

**The fairness check** (`.claude/skills/wotr-write/references/fair-play.md`).

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **pass, and the cost is the summoner** | 75,000 EU to fabricate, a per-second sustain that rises rather than holds, the Essence Core itself as the pump (*"the same Essence Core the summoner still has to live in afterward"*), a dismissal the page will not guarantee, and — from the register rather than the page — a standing Coherence drift that degrades the summoner before anybody touches them. The one thing missing is a figure for the rising term. |
| Stated limits | **pass, and the central limit is a clock** | *"It cannot remain stable indefinitely"*; *"It cannot be dismissed as safely as a true Eidolon"*; *"it cannot be produced without cost to the summoner's own Crystal"*; and the convincing-ness limit, which is the sharpest of the four: it persuades *"an observer who has not met the summoner's actual, unflattering self"* and nobody else. |
| Something beats it | **pass, four ways** | Silence ends it outright; exhaustion ends it faster than most workings in the section; an honest reflection is a loss term in the loop; and anyone who knows the summoner well sees it immediately. Below. |
| It has a tell | **pass, and it is the best-designed tell in this section** | The tell is **acquaintance**. The construct is a flattering version, so its detectability is a function of how well the observer knows the original — which means a player does not roll to notice, they *have met this person before*, or they go and find somebody who has. A counter that rewards having talked to people is worth more than one that rewards a perception score. |
| Numbers in band | **pass — the only unqualified pass in this section** | Stage VI ⇒ Max Grade A (276–400), ceiling 400, Tier 5, η 0.60–0.70 under R44-4, all consistent with the page's A-Grade. And the 75,000 EU figure delivers 4.5–5.25 × 10¹⁰ J against an A-Grade band opening at 4.6024 × 10¹⁰ — **in band at the ruled η**, per `reports/eu_band_sweep_2026-09-25.md`:61. The reserve ladder still misbehaves, and that is `SA-CROSS-EU-STAGE-LADDER` rather than this page. |

**The Counterplay routes that work**
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Deny the field — Silence, and it is total, as it is for all Animatria.**
  *"Animatria constructs fail completely because their continuity runs back to a source
  the Silence has severed."* The page's construct is an Animatria construct with a
  tether, and the Discipline says the tether is the whole of its continuity. Note the
  register's diagnostic for telling a Silence from a merely quiet room:
  *"A soul held in one reports the sensation as loneliness rather than weakness."*
- **Break the boundary — the anchor, because Stage VI is below Refraction.**
  *"Below Refraction a working requires an external anchor: voice, hand, ink or blood.
  Take the anchor and the sentence does not complete. Break his wrist and a gestured
  chain is finished. Put a hand over his mouth and a spoken one is."* This is the
  cheapest counter in the register and it applies here by Law V — although the page
  names no anchor, which is the gap at `SA-CROSS-VAINGLORY-LAW-V-ANCHOR` and is worth
  knowing before relying on it.
- **Break the body — exhaustion, and the clock runs down rather than flat.**
  *"Below ten percent reserve a practitioner suffers Essence Starvation… A defender who
  can afford to spend nothing wins a long engagement against an attacker who cannot
  afford to spend nothing."* The register's usual caution against waiting does not hold
  against this working for a reason unique to it: the drain **rises**. Waiting is not a
  bet that he will tire; it is a bet on an exponential, and §1 says the exponential is
  real.
- **Break the man — Coherence drift, which the register describes as though it had
  this page open.** *"A practitioner whose lived behaviour has drifted from his stated
  law is degrading before anyone lays a hand on him: output falls, Thresholds refuse to
  authorise, and his Traits begin to argue with him. You do not have to cause this. You
  have to notice it and wait."* A summoner sustaining a construct built on
  self-idolatry is running a stated law their lived behaviour is diverging from, at an
  exponential rate, by the working's own mechanism. **This is the one working in the
  section where the register's laziest counter is also its best one.**
- **Add a loss term — an honest reflection, which is derivable and not on the page.**
  A faithful, lossy element placed in a feedback loop lowers the round-trip gain; take
  the loop below unity and the oscillation dies. In the register's terms that is
  another **Mirithane** practitioner, whose whole office is *"the absence of introduced
  distortion"* — and **Oblivara** *(Limina)* is the ready-made version:
  *"attempts at perceptual manipulation return to their source"*, which puts the
  flattering correction back where it came from. Oblivara's price is the one to read
  first: *"Code exhaustion. Redundancy has a correction limit, and past it the
  reconstruction is confident, complete, and wrong."*

**The tell, stated plainly.** It looks like the summoner, only better, and that is the
tell — but only to somebody who has seen the summoner worse. The page says so itself
and the sentence is the whole counter: the construct convinces *"an observer who has
not met the summoner's actual, unflattering self."* So the practical procedure is not
to examine the construct. It is to **find the person who has seen this one on a bad
day** — a sibling, a creditor, a former partner, anyone the summoner would not have
chosen as a witness — and put them in the room. Of the twenty workings in this
section, this is the one beaten by having done the social legwork.

**The lookup trail.**

1. `wiki/Spellcraft/Vainglory.md` — the four stated limits, and the convincing-ness
   condition that names the counter without naming it as one.
2. `wiki/The Eight Families & the Sixty Wellsprings/Limina — Entropy, Void and Mind.md`
   — **Mirithane's Core Law** (*a true mirror adds nothing… no flattering correction
   applied in transit*) and **Mirithane's Failure**, which is not what the page says it
   is; plus **Eidolyn's template defect** and **Oneirion's projection error**, and
   **Oblivara's** returning of perceptual manipulation to its source.
3. `wiki/The Disciplines/The Spirit Summoning Arts.md` — the **Animatria** entry for
   the tether and the Silence rule, the **Temperance Gates** that set the floor, the
   **cost table**, and the **Concordia** warning that a construct with enough internal
   coherence *"may begin to resist dissolution."*
4. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — **Silence**,
   **Interrupt the chain**, **Exhaustion**, and **Coherence drift**, which is the route
   this working walks into on its own.
5. `wiki/The Magic System/The Four Crafts.md` — Law V, which says a Stage VI working
   needs an external anchor, and is therefore the page a player checks before trying to
   take one.
6. `wiki/The Magic System/The Core Vocabulary.md` — §V for **Essence Starvation at ten
   percent**, and §VI for **Tempering Coherence** as the alignment between stated law
   and lived behaviour, which is what this working spends.
7. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`
   — Part Four for the **A-Grade attack-output band** the 75,000 EU figure lands inside,
   Part Five for the Stage ladder, and Part Seven for the three **Path gates** the page
   does not name.

**Conflicts added by this section:** none beyond those already logged above.
