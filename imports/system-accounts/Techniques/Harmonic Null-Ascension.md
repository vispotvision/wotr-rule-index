---
page: wiki/Techniques/Harmonic Null-Ascension.md
section: Techniques
practitioner: Opalis (no card in current canon)
wellspring: Orrenthal (primary) · nine secondaries
family: Fulguria
stage_floor: XII
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · Harmonic Null-Ascension

## 1 · Physical account (physics)

**The phenomenon in plain words.** She plucks a string that is not there. A tone climbs from
nothing, locked to one target's own structural frequency, and at the top of the climb the
target either goes silent or shatters.

**The real phenomenon.** **Forced resonance driven past a structure's damping.** Drive a
lightly damped oscillator at its natural frequency and the steady-state amplitude is the
static response multiplied by the quality factor **Q = 1/(2ζ)**. For a low-loss structure Q
runs into the thousands, so a small sustained drive produces a very large displacement — and
the displacement, not the drive, is what exceeds the material's strain limit.

The canonical demonstration is a wineglass: fundamental mode in the **500–800 Hz** range,
**Q ≈ 10³**, and a sustained drive at resonance of roughly **100–110 dB SPL** is enough to
take it apart. The same acoustic power off-resonance does nothing at all.

**One correction to the page's own example, offered because the distinction matters.** The
page says this is "the same failure mode a bridge or a wineglass shows under sustained
resonant forcing." The wineglass is forced resonance. **The famous bridge case is not.**
Tacoma Narrows failed by **aeroelastic flutter** — a self-excited instability in which the
structure's motion extracts energy from a steady flow, with no external periodic drive at
all. Flutter has no driving frequency to match, which means it is a *different* mechanism and
would be a *different* technique. The distinction is worth keeping because it separates this
working from a working that would need no frequency-lock at all.

**The governing law.** Steady-state amplification = Q at resonance; the locking condition is
that the drive frequency sits inside the resonance bandwidth, Δω = ω₀/Q. **High Q buys
amplification and costs bandwidth** — a Q of 10³ means the drive must sit within one part in a
thousand of the true frequency. That is the whole difficulty of the working and the page names
it: the climb begins only once frequency-lock completes.

**Measurable quantities, SI.**
- Range **500 m**, line-of-sight; single target, with a **15 m** dissonance burst on collapse
  (page).
- Amplification available: **Q ≈ 10³**, so a drive 1,000× below the failure stress suffices.
- **Lock precision required:** Δω/ω₀ = 1/Q = **10⁻³**. To drive a 600 Hz mode she must be
  inside **0.6 Hz**.
- Onset below audibility: human hearing runs **20 Hz – 20 kHz**, so a climb beginning in
  infrasound is inaudible until it crosses **20 Hz**, which is the page's "inaudible at first"
  with a number on it.
- Ringdown after collapse: a Q ≈ 10³ mode decays over roughly Q cycles, so **a few seconds**
  of residual dissonance at audible frequencies — the page's figure, derived.
- **The energy figure has the same two problems as `Celestial Harmonic Shear`.** The page
  gives "on the order of 1 PN peak force and roughly **400 TJ** yield." Part Four's SSS row is
  4.184×10¹⁴ – 4.184×10²¹ J, so **418 TJ is the floor and 400 TJ reads as SS-Grade.** And
  resonant forcing is a mechanism whose entire advantage is that the *drive* is a thousandth
  of the failure load, so quoting a Grade-ceiling energy for the drive contradicts what makes
  the working work. Logged `SA-NUM-NULLASC-400TJ-BELOW-SSS` and
  `SA-PHYS-NULLASC-YIELD-VS-MECHANISM`.

**The energy budget, and where the joules were.** Overwhelmingly in the target. She supplies
a frequency held inside 0.6 Hz for the duration of a climb; the structure supplies a factor of
Q. This is `Two Sets of Books` §III at its most economical: "The energy was in the room. The
structure that let it move in that particular direction was in the person."

**Precedent we are not copying.** Sonic kills are genre-standard — One Piece's
Brook-adjacent tricks, Bleach's Ichigo's resonance feats, the bard's shatter. Those are
**loud**. This one is quiet by construction and then inaudible-to-audible over a climb, and
its counter is **spectral ambiguity** rather than earplugs: a target that can split its own
resonance across several bands never lets one frequency reach the failure point. The
divergence is that the defence is to be *hard to tune*, not hard to hurt.

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** A held line to one target plus a small burst on collapse — a narrow
footprint for a Stage XII working. Fulguria wants "Dry air, conductive substrate, clear line
of sight" and is suppressed by "Faraday-caged interiors, heavy ferrous shielding, dense fog"
(`The Eight Families & the Sixty Wellsprings`, Environmental Coupling). **"Dead air, or a
target with no structural resonance to seize on, gives the tone nothing to climb" is the
page's own Limit, and it is Fulguria's suppression list stated as a mechanism.**
**Residue:** the burst's 15 m of dissonance, plus whatever the target's collapse leaves.
**Saturation:** not a limit; the limit is the lock.

**Wellspring stratum.** **Orrenthal · *The Metallic Heart*** (primary), Family
**Fulguria**, Physics Domain **electromagnetism**. Its law, verbatim from
`wiki/The Eight Families & the Sixty Wellsprings/Fulguria — Electromagnetism.md`:

> "A metal is strong, conductive, and ductile for one reason: its valence electrons belong to
> the lattice rather than to any atom in it. Nothing is individually owned, so the structure
> deforms without fracturing and carries charge without resistance. Orrenthal imposes that
> bonding character on the Crystal. The Measurewrights note without embarrassment that the
> Wellspring's moral reading and its physical reading are the same reading."

Nine secondaries, of which the page assigns three real jobs: **Cataclysm** and **Fractura**
"decide whether the failure resolves as violent over-resolution or as fracture along existing
lines," and **Dissolution** "supplies the alternative failure of reduction to silence rather
than shattering." All three check out. Cataclysm's law is the deflagration-to-detonation
transition — "The mechanism is a change of kind, not degree"
(`Caloria — Thermodynamics.md`) — which is the right current for "violent over-resolution,"
since a resonant failure that couples to a shock is exactly a change of kind. Fractura's is
the Griffith criterion, which is the right current for failure along pre-existing flaws.
Dissolution's is the entropy of mixing, which is the right current for reduction rather than
rupture. **Three secondaries, three correct assignments, and the difference between the
working's two outcomes is a Wellspring choice rather than a die roll.** That is good design
and it deserves crediting.

Register failures in play. Basilithe's "**Resonant catastrophe.** A frequency that cannot be
shifted also cannot be detuned away from a forcing that happens to match it" — **which is the
single most load-bearing sentence for this page and the page takes the wrong side of it.** The
page says "A structure anchored in pure Basilithe resists the collapse through sheer
law-stability." Basilithe's register says the opposite: a Basilithe structure is the *easiest*
thing to drive, because its frequency is fixed and cannot be detuned away from a drive that
matches it. **High stiffness and low loss mean high Q, and high Q means more amplification,
not less.** The resistance the page claims is real only for the *lock* (a stable frequency is
harder to shift) and reverses for the *climb* (a stable frequency is easier to drive). Logged
`SA-CROSS-BASILITHE-RESIST-OR-AMPLIFY`; recorded, not resolved, and it matters because it
inverts a stated counter.

*Four Theories.* **Consent Doctrine** on the page's framing. The page's "What nobody knows" —
"Whether the tone Opalis hears in her own head during the climb is the target's true resonance,
or the one she has decided it deserves" — is the same **Correspondence**-versus-Consent
question `Celestial Harmonic Shear` raises, asked the other way round. **Noted, not
resolved.**

**Essence stratum.** Active layer: the **Aether Shell**, run as a resonant source. Shell
failure states are "Clouding or Rupture" (`The Core Vocabulary` §III); the page's cost —
"a brief harmonic rebound into Opalis's own Essence and a doubled, echoing quality to her
speech and thought for several minutes after" — is Clouding with a very precise signature.
**And it has a physical reading the page does not claim:** a doubled, slightly out-of-phase
self is what a **beat** sounds like, two sources at nearly the same frequency, and running a
Q ≈ 10³ drive through your own Shell leaves that Shell ringing near — but not at — its own
rate. **Her speech doubling is a beat frequency, and that is derivable rather than invented.**
Developmental Tier at Stage XII: **Sovereign** (Part Twenty-One). Crystal State: `null`, no
card. **The invoice:** an estimated **30,000 EU per cast**, plus the rebound.

**The lens: Plotinian emanation, and the return.** Plotinus, *Enneads* V.1–V.2
and VI.9: all things proceed from the One through Intellect and Soul, each level
less unified than the one above it, and the soul's proper motion is *epistrophē*,
the turning back — an ascent in which multiplicity is progressively shed until
form itself is no longer needed. Nothing in this batch is named more accurately
than **Null-Ascension**, because Plotinus gives the page its two outcomes and
tells you which is which: *"the target's form either fails into silence or
shatters outright"*, and those are a successful return to the One and a failed one.
Dissolution supplies the first, reduction to silence; Cataclysm and Fractura
supply the second, a structure that could not hold its own ascent. The lens also
explains why the tone starts inaudible — *"the climb begins below the range
anything but the Essence layer can register"* — because on the emanative scheme
the higher levels are not louder, they are **simpler**, and simplicity registers
last to a sense built for multiplicity. And here the lens turns dangerous in the
best way, because for Plotinus the ascent is **voluntary and good**: a school
reading Null-Ascension as epistrophē will describe what it does to a man as a
liberation and will not think to interfere with it at all. Damping is the entire
counter — *"a true silence field, or an anti-vibrational current such as
Verdantia or Cymorath, damps or redirects the tone entirely"* — and a school that
believes the tone is a blessing does not bring anything to stop it with.

---

## 3 · Mechanism (the effect)

**Glyph (proposed; the page names none).** `[Lh]` **Frequency** · Root · Selhar, as on
`Celestial Harmonic Shear` — the same limit, applied dynamically rather than geometrically —
laid across `[Kael]` **Ruin** · Root · Uurgath, because this working's product is failure
rather than a seam. Both from the thirty unclassified forms in
`wiki/The Magic System/The Master Glyph Index — 136 Attested Forms.md`. **The distinction
from the Shear is worth stating, because it is the whole of what separates the two workings:
the Shear pins `[Lh]` to a line in space (`[Al]` Edge) and the Ascension pins it to a climb in
amplitude (`[Kael]` Ruin).** *Filing decision, not canon — Isaac's ruling.*

**What boundary moves.** One quantity: **the damping of one named mode in one target.**
Not the mode's frequency — she finds that, she does not set it. Not the drive amplitude — that
is small. **Only ζ**, and with ζ pinned low the amplitude climbs on its own until something
gives.

**What the law then does on its own.** All of the climb, and every limit on the page.
Amplitude rises without further input because that is what an underdamped driven oscillator
does. The failure is sudden because a strain limit is a threshold. A target with no structural
resonance cannot be touched because there is no ζ to pin. A being at or above her own
Temperance tier cannot be forced because the lock is contested rather than the climb. The
collapse throws its own shockwave outward because the stored energy in a Q ≈ 10³ mode has to
go somewhere. **And it cannot be sustained past a few breaths without the cost escalating
sharply, which is the page's own Limit, because holding a lock inside 10⁻³ against a target
that is moving is the expensive part.**

**Law V check.** Stage XII sits far above Refraction, so no material anchor is needed
(`wiki/The Magic System/The Four Crafts.md`). The page gives two fingers or a staff brought to
the air — Gestured by choice, and as on the Shear the gesture is plausibly doing aiming work
rather than anchoring work.

**Failure mode — Structural fault.** "The Crystal could not hold what the boundary permitted"
(`Two Sets of Books` §VII). She has made her own Shell a resonant source and it rebounds; the
beat in her speech is the Shell still ringing. A **Field fault** is the counter set: a true
silence field, or an anti-vibrational current, leaves the working correct with no medium to
drive.

**What the target sees and feels.** Almost nothing, at first, which is the worst
part of the page. Opalis brings two fingers or her staff to the air and plucks a
string that is not there; the tone begins *below* what anything but the Essence
layer can register, and it climbs. Frequency-lock is onto the target's **own**
structural resonance, so there is no incoming object to intercept and nothing
arriving from a direction — the thing being driven is the thing that holds him
together. Then, once the lock completes, resolution is instantaneous:
*"resonant frequencies inside the target escalate past stability, producing
fracturing, implosion or soul-pattern distortion as the structure fails."*
Collapse throws a secondary dissonance burst out to fifteen metres, so standing
next to the target is not neutral. Residual dissonance hangs a few seconds
afterward. The limits are the target's whole hope and they are legible: dead air
gives the tone nothing to climb in; something with no structural resonance at all
— true void, pure dreamstuff, an anti-harmonic field — cannot be locked onto; a
being at or above her own Temperance tier cannot be ascended; and holding the
climb open *"for more than a few breaths makes the cost climb faster than it can
be paid"*, which means she is on a clock she set herself.

**What bleeds, at the stated efficiency.** No card for Opalis; the ladder gives Stage XII ⇒
**Tier 7 · Grandmaster**, η **0.85–0.90** (Part Nineteen) ⇒ **10–15 percent** as heat, sound
and structural bleed. On a working whose entire output is a frequency, **the bleed is sound
that is not on the target's mode** — which is inaudible infrasound during the climb and the
page's rebound afterward. At 10–15 % of a drive that is itself a thousandth of the failure
load, the absolute bleed is tiny, and that is why the page can describe a Stage XII killing
working that nobody hears coming. **Part Nineteen's "the highest Bands run quiet" is doing
real work on this page.**

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| EU spent | **≈30,000 per cast** (page's estimate) | Page, against "the 8,000 to 45,000 EU range documented elsewhere for a non-sustained Stage XII working." **No system rule establishes that range.** `SA-GAP-STAGE-XII-EU-BAND`. |
| Flux Density | `null` | No AU/s figure, no card. |
| η | **0.85–0.90** (derived) | Stage XII ⇒ Tier 7 (Part Five) ⇒ η band (Part Nineteen). `SA-GAP-OPALIS-NO-CARD`. |
| AU/s | `null` | Needs Flux Density. |
| Duration | **instantaneous once locked**; climb "a few breaths" | Page. **No turn conversion needed.** |
| Range / burst | **500 m** / **15 m** on collapse | Page. |
| Stated yield | **≈1 PN**, **≈400 TJ** | Page. **Below the SSS floor of 4.184×10¹⁴ J (418 TJ)** — reads as SS. `SA-NUM-NULLASC-400TJ-BELOW-SSS`. And in tension with the mechanism, whose drive is Q⁻¹ of the failure load. `SA-PHYS-NULLASC-YIELD-VS-MECHANISM`. |
| Amplification | **Q ≈ 10³** | Low-loss structure. The drive is ~10⁻³ of the failure load. |
| **Lock precision required** | **Δω/ω₀ = 10⁻³** | 1/Q. For a 600 Hz mode, inside **0.6 Hz**. **This is the working's real difficulty and no system stat is assigned to it.** Harmonics **Attunement** is the closest ("Affinity and synchronisation strength with bound Wellsprings", Part Twelve) and the page cites it. |
| Audibility onset | **20 Hz** | Human hearing floor; the climb starts below it. |
| Ringdown | **a few seconds** | ≈Q cycles at audible frequency. Page's figure, derived. |
| Bleed | **10–15 %**, as off-mode sound | 1 − η at Tier 7. |
| Minimum Stage | **XII · Emanation** | Page. Max Grade SSS, ceiling 950 (Part Five). |
| Tier of Standing | **7 · Grandmaster** | Part Five. |
| Grade required | **SSS** (726–950) | Page. No sheet to check. |
| Path gate | **Spirit** | Page. Ardency Penetration is Body-gated above C and Ardency Depth "requires Attraction Path at Stage IV to exceed B, and Stage VI to exceed A where two Wellspring qualities are held in one working" (Part Seven). **The page's own Sub-Stat list (Flux, Penetration, Depth) carries a Body gate and an Attraction gate, and the declared Path is Spirit.** Same shape as `Celestial Harmonic Shear`. `SA-NUM-NULLASC-PATHGATE`. |
| Wellsprings held | **10** | Requires Harmonics Breadth, Attraction-gated at Stage V for layering (Part Seven). Tempering Capacity for Opalis: `null`. `SA-GAP-OPALIS-TEMPERING-CAPACITY`. |
| Starvation margin | `null` | Estimated EU, no reserve figure. |
| Developmental Tier | **Sovereign** | Stage XII (Part Twenty-One). |
| Crystal State | `null` | No card. |

**Does the physics close against the stratal account?** **The mechanism closes and one stated
counter inverts.** Forced resonance past damping accounts for everything the page claims: the
silent onset, the sudden failure, the outward shockwave, the immunity of anything with no mode,
and the sharp cost of holding a lock. The three secondary Wellsprings that decide *how* the
target fails are each the right current for the job. **What does not close is Basilithe:** the
page lists a pure-Basilithe structure as resistant, and Basilithe's own register says a
frequency that cannot be shifted cannot be detuned away from a drive that matches it — which
makes it the most drivable target on the field once the lock is found. That reverses a counter,
so it goes to Isaac rather than being quietly fixed.

**A cross-page note.** This working and `Celestial Harmonic Shear` are near-twins: same
practitioner, same Stage, same Grade, same Family, same primary and the same nine secondaries,
same Category, same Path gate, both quoting "1 PN and roughly 400 TJ," and EU estimates
30,000 against 35,000 with no stated basis for the 5,000 difference. The mechanisms *are*
genuinely distinct — a mode severed geometrically versus a mode driven past its damping — and
this account and the Shear's each say so. But nothing in the system explains the cost
difference. Logged `SA-CROSS-SHEAR-NULLASCENSION-TWINS`.

**Conflicts logged from this page:** `SA-CROSS-BASILITHE-RESIST-OR-AMPLIFY`,
`SA-NUM-NULLASC-400TJ-BELOW-SSS`, `SA-PHYS-NULLASC-YIELD-VS-MECHANISM`,
`SA-NUM-NULLASC-PATHGATE`, `SA-CROSS-SHEAR-NULLASCENSION-TWINS`,
`SA-GAP-STAGE-XII-EU-BAND`, `SA-GAP-OPALIS-TEMPERING-CAPACITY`, `SA-GAP-OPALIS-NO-CARD`,
`SA-GAP-EU-FORMULA`, `SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR`.

---

## 5 · Counterplay and the challenge

**The fairness check** (`.claude/skills/wotr-write/references/fair-play.md`).

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **pass, on an unsourced figure** | *"An estimated 30,000 EU per cast"*, a harmonic rebound of the same damage into her own Essence, and — the good detail — several minutes afterward in which *"her voice and her own thoughts run doubled, as if two slightly out-of-phase copies of her were speaking at once."* Cognitive impairment that outlasts the exchange is a real cost. But the EU figure rests on an *"8,000 to 45,000 EU range documented elsewhere"* that **no system rule establishes** (`SA-GAP-STAGE-XII-EU-BAND`), and there is no reserve figure, so no Starvation margin (`SA-GAP-OPALIS-NO-CARD`). |
| Stated limits | **pass, and they are the most specific of the three Opalis attack pages** | 500 m, line of sight; primarily single-target with a 15 m collapse burst; **cannot ascend a being at or above her own Temperance tier**; cannot target anything with no structural resonance; **cannot be sustained past a few breaths** without the cost outrunning payment. |
| Something beats it | **pass, and below her Stage** | Damping, silence, or frequency multiplicity. None of these requires a peer, and two of them are terrain. |
| It has a tell | **pass, narrowly** | A raised hand or staff and a plucked string that is not there — a small, quiet, deliberate gesture. The climb itself is **inaudible at the start**, so the gesture is the only warning and it is easy to miss at five hundred metres. This is the thinnest passing tell in the batch and it passes only because the gesture is stated and specific. |
| Numbers in band | **flagged, already logged** | Stage XII ⇒ Max Grade SSS (726–950), ceiling 950, Tier 7, η 0.85–0.90 (Parts Five, Nineteen). The force estimate — *"1 PN peak force and roughly 400 TJ yield"* — sits **below** the SSS floor of 418 TJ (`SA-NUM-NULLASC-400TJ-BELOW-SSS`), the stated yield does not match what the mechanism actually does (`SA-PHYS-NULLASC-YIELD-VS-MECHANISM`), and the Path gate does not fit its own Sub-Stats (`SA-NUM-NULLASC-PATHGATE`). As with `Celestial Harmonic Shear`, these make it **weaker** than its band, not stronger, so none is a new fairness fault. |

**The Counterplay routes that work**
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Deny the field — damping, which is the whole answer.** *"A true silence
  field, or an anti-vibrational current such as Verdantia or Cymorath, damps or
  redirects the tone entirely"*, and dead air *"gives the tone nothing to climb."*
  Resonant forcing only works against a structure whose damping it can outpace, so
  **adding damping is not defence, it is denial**. The register's **Silence** is
  the general form, and Family **Fulguria** supplies the terrain version — *"fails
  against boiled leather, fired clay, dense fog and a shielded interior"* — which
  matters here because the working needs line of sight to 500 m.
- **Break the boundary — split the frequency.** *"A target able to split its own
  resonance across multiple frequencies (a Fractura-dominant being, a dream-form)
  never lets any single frequency climb past stability."* A **Knot**: no single
  path to trace, no single mode to drive. An Oneirion-dominant illusion can
  decouple its own resonance to slip the lock outright, and a structure anchored
  in pure Basilithe resists through law-stability — though whether Basilithe
  resists or *amplifies* is itself contested (`SA-CROSS-BASILITHE-RESIST-OR-AMPLIFY`).
- **Break the man — her own clock.** She cannot hold the climb open past a few
  breaths without the cost outrunning what she can pay. Anything that delays
  frequency-lock — cover breaking line of sight, movement, a decoy resonance — does
  not merely postpone the working, it makes her **pay for the delay**. This is the
  rare case where the register's forbidden plan of waiting is legitimate, because
  the page states that waiting is expensive to her specifically.
- **Break the body — spread, and do not stand together.** Single-target, with a
  fifteen-metre burst on collapse. *"Twenty men who have been drilled to spread,
  to make him choose, and to keep a line of fire open at all times."* One kill per
  cast at 30,000 EU a cast is an economy an army wins.

**The tell, stated plainly.** Two fingers, or a staff, raised to the air, and a
string plucked that is not there. Then silence that is not silence. If you missed
the gesture you will get no second warning, which is logged above as the reason
this check only just passes.

**The lookup trail.**

1. `wiki/Techniques/Harmonic Null-Ascension.md` — the Limitation (no resonance,
   no lock; no peer ascension; cannot be sustained) and the Weakness (Basilithe,
   Oneirion, silence, Verdantia, Cymorath).
2. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — "Silence",
   "Knot and Lock", "Numbers, correctly used", and Fulguria's failure terrain.
3. `wiki/The Eight Families & the Sixty Wellsprings/Fulguria — Electromagnetism.md`
   — Orrenthal's harmonic law, which finds and holds the true frequency.
4. `wiki/The Eight Families & the Sixty Wellsprings/Vitalia — Biochemistry.md` —
   Verdantia as an anti-vibrational current, which is the cheapest damping a party
   is likely to already have.
5. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`
   — Part Four for the SSS band, and therefore for noticing that 400 TJ is under
   it; Part Seven for Ardency Depth's Attraction gate where two Wellspring
   qualities are held in one working.
6. `wiki/Techniques/Celestial Harmonic Shear.md` — the near-twin of this working
   (`SA-CROSS-SHEAR-NULLASCENSION-TWINS`). A reader who compares the two learns
   that both are beaten by the same three things, which is the most useful single
   fact about fighting Opalis.

**Conflicts added by this section:** `SA-GAP-COUNTERPLAY-TERRAIN`. The page's
Effect follows from its Mechanism — resonant forcing driven past a structure's own
damping, with the two named failure outcomes — so no `effect-mechanism` conflict
arises; the yield-versus-mechanism fault was already logged as `physics-open`.
