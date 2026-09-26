---
page: wiki/Techniques/Edict Strike.md
section: Techniques
practitioner: Drakvor · The Black-Crowned Bastion
card: wiki/Volume I — Character Cards/Drakvor · The Black-Crowned Bastion.md
wellspring: Judicium (primary) · Coagula (secondary)
family: Fulguria / Materia
stage_floor: VIII
status: awaiting-ruling
method: imports/system-accounts/_method.md
---

# System account · Edict Strike

## 1 · Physical account (physics)

**The phenomenon in plain words.** A slow downward sword-cut that lands heavier the more
the person it is aimed at is hesitating, and doubles against someone fully unsure.

**The real phenomenon.** **Impulse transfer and effective mass**, with a
**dimensionless spectroscopic ratio** as the multiplier.

*The impulse side.* Force delivered by a strike is F = dp/dt. For a fixed contact
duration, the force scales with the momentum delivered, and the momentum scales with the
**effective mass** coupled into the striking body — not the blade's rest mass. Coagula's
contribution on the page is exactly this: gathering borrowed weight "into the blade
itself rather than letting it disperse on the swing," which is a statement about
effective mass.

*The measurement side, and this is the page's own open question answered.* The page asks:
"Why Judicium can price a target's hesitation at all, in exactly the units a blade needs
to grow heavier by." **Because a spectroscopic read does not return units.** Absorption
spectroscopy returns a *ratio* — line depth against continuum, an absorbance
A = log₁₀(I₀/I) — and a ratio is **dimensionless**. A dimensionless quantity multiplies
anything at all, including a mass. **There is no unit conversion problem because there
was never a unit.** That falls straight out of Judicium's register analogue and it is the
cleanest answer to any "What nobody knows" line in the batch.

**The governing law.** F = dp/dt for the delivery; Beer–Lambert, A = ε·c·l, for the read;
and the multiplier is the dimensionless absorbance, capped at 2 by the page's own
statement ("Against a fully hesitant target the impact doubles").

**Measurable quantities, SI.**
- Baseline: **0.5–2 TN** peak force, **4.184×10¹² – 2.42672×10¹³ J** — the S-Grade row
  from Part Four, correctly quoted by the page.
- Doubled: **1–4 TN**, **8.37×10¹² – 4.85×10¹³ J**. The upper end crosses into
  **SS-Grade** (4.184×10¹³ – 4.184×10¹⁴ J), and the page addresses this itself: Stage
  VIII's "own late push runs toward SS-Grade before any Overchannel risk applies."
  Checking that against Part Five: Stage VIII's Max Grade is S with ceiling 550 and
  **no instability zone** — the zones sit at Stages V, VII, IX and XI. **Stage IX is the
  Stage with the "late push toward SS entry," not Stage VIII.** Logged
  `SA-NUM-EDICT-SS-PUSH`; recorded, not resolved.
- Armour defeat: the page says armour rated below **B-Grade** buckles. B-Grade's ceiling
  is 4.6024×10¹⁰ J, so an S-Grade baseline strike exceeds it by **91× to 528×**.
  "Buckles outright" is an understatement by two orders of magnitude and the page is
  conservative, not wrong.
- Windup: **6 s** (page, "the source's single old-count turn"), at six seconds to
  the turn.
- **The contact-area problem.** A sword edge is roughly 10 mm of engaged length by
  0.1 mm of edge thickness — **1×10⁻⁷ m²**. Delivering 5×10¹¹ N through that footprint
  is a contact stress of **5×10¹⁸ Pa**. Diamond, the hardest material known, fails in
  compression near **1.1×10¹¹ Pa**. The required stress is therefore **≈4.5×10⁷ times**
  what any material can carry, and the minimum contact area for 0.5 TN even *against
  diamond* is 5×10¹¹ ÷ 1.1×10¹¹ = **4.5 m²**. **A blade cannot be the force-transfer
  path for a 0.5 TN peak.** The blade vaporises long before the target registers the
  hit. Logged `SA-PHYS-TN-THROUGH-A-BLADE`; this is a batch-wide issue, since the same
  0.5–2 TN figures appear on `Bastion Imperium` (where a 314 m² footprint resolves it)
  and `Cryost Ascendant` (where a 6–18 m field resolves it). **Edict Strike is the one
  page where the force has nowhere to go.**

**The energy budget, and where the joules were.** Not in his arms. 4.184×10¹² J is
roughly a kiloton of TNT and no musculature delivers it; the system's answer stands — he
supplies the boundary, the field supplies the joules, and structure is what fails. The
structure that fails on this page is his wrists and shoulders, and the page bills them.

**Precedent we are not copying.** Conviction-scaling strikes are a genre staple —
Berserk, Fire Emblem's weapon triangle, every "damage scales with enemy fear" mechanic.
Those read a **status**. This reads a **spectrum** and multiplies by a ratio, which is
why the counter is not courage-as-a-buff but a **Resolve-aligned Wellspring that keeps
the doubt from registering at all** — the read returns nothing, so the multiplier is 1.
The divergence is that immunity here means being *unreadable*, not being brave.

---

## 2 · Stratal account (metaphysics)

**Aether stratum.** Small draw, melee range, single target. Fulguria wants "Dry air,
conductive substrate, clear line of sight" and is suppressed by "Faraday-caged
interiors, heavy ferrous shielding, dense fog"; Materia wants "Mineral-rich rock, worked
stone, deep foundation" (`The Eight Families & the Sixty Wellsprings`, Environmental
Coupling). **Heavy ferrous shielding is the interesting one: a target in full plate is
partly Faraday-caged against the read, which would suppress the multiplier rather than
the blow.** The page does not say this and it is a consequence of its own Family
assignment. Offered as texture. **Residue:** minimal — one strike, one target, no
field. **Saturation:** not a factor.

**Wellspring stratum.** **Judicium · *The Wellspring of Truth*** (primary), Family
**Fulguria**, Physics Domain **electromagnetism**. Its law, verbatim from
`wiki/The Eight Families & the Sixty Wellsprings/Fulguria — Electromagnetism.md`:

> "Every element absorbs and emits at wavelengths fixed by its own electron structure,
> and no substance can present another's spectrum. Judicium tunes Gnosis to that
> principle: the practitioner reads the characteristic lines of a Crystal, a technique,
> or a lie, and identifies composition from signature alone. Eddy-current inspection
> finds the crack under the paint without removing the paint."

**"No substance can present another's spectrum" is why the strike cannot be bluffed.**
A target who performs confidence still presents their own lines. That is a harder and
better counter-immunity condition than the page states, and it is in the register
already.

**Coagula · *The Unifying Pulse*** (secondary), Family **Materia** — law quoted in full
in the `Bastion Imperium` account — gathering the read into the blade.

Register Stat Effects, through the Merge Ledger: Judicium gives Gnosis **Acuity** and
**Analysis** (from Diagnosis); Coagula gives Resilience **Integrity** and Tempering
**Coherence**. The page cites all four and adds Ardency **Flux** as the delivery stat,
which is correct — Flux is "Raw destructive and constructive output of active
expressions. The damage ceiling" (Part Twelve).

Register failures in play. Judicium's "**Spectral overload.** Every object in view
reports its composition simultaneously and the practitioner loses the ability to
prioritise any of it" — which is the mechanical reason the windup is slow and read-heavy.
Coagula's "**Residual porosity**" — the gathered weight is not fully dense, so the
delivered impulse has voids in it, which is a candidate reading for why a *partially*
hesitant target gets less than the doubling and not a proportional share of it.

*Four Theories.* **Consent Doctrine**, cleanly. A spectrum is read; nothing is asked.

**Essence stratum.** Active layer: the **Essence Core** for the read (Gnosis is Core
work), the **Aether Shell** for the delivery. Shell failure states, "Clouding or
Rupture" (`The Core Vocabulary` §III) — and the page's cost is "Aether strain through
his wrists and shoulders with every full swing," which is Clouding localised to the
conduit's delivery end. **That the cost lands on wrists and shoulders rather than
anywhere else is the physical account's contact-area problem showing up in the invoice,
whether the page intended it or not: the narrower the transfer path, the more of the load
the practitioner's own joints see.** Developmental Tier at Stage VIII: **Radiant**.
Crystal State: **Refined, overbuilt by design** (card). **The invoice:** per swing, not
per second — the correct shape for an instantaneous working, and this is one of the few
pages in the batch whose cost cadence matches its duration.

**The lens: the *vis imaginativa*.** Avicenna, *De anima* IV.4, developed by
Marsilio Ficino and set out at length in Agrippa's *De occulta philosophia*
(1533) I.lxiv: a sufficiently intense imagination acts on bodies, first on its
own and then on others — the terrified man who marks his own flesh, the pregnant
woman whose fright is held to shape the child. It was the standard learned
explanation for centuries of how fear could do physical work, and it is the exact
shape of this working's claim: the target's own hesitation contributes to what
arrives. Judicium's half of the mechanism fits the lens precisely, because the
*vis imaginativa* tradition always held that the imagination had to be **read**
before it could be used, which is why the doctrine travelled with physiognomy and
the reading of faces. What the lens gets wrong is the direction of the loan. On
Avicenna's account the power sits in the **imaginer** — the fear does the wounding
— and a school that reads Edict Strike that way concludes that a fearless target
cannot be hurt by it, and will send its bravest man forward on that theory. The
page says the baseline strike still lands at the S-Grade band, 0.5–2 TN,
regardless of what anyone believes. Fearlessness halves the blow; it does not
remove it. Where the doubled weight comes from, in joules, is the question this
account logs rather than answers (`SA-PHYS-TN-THROUGH-A-BLADE`,
`SA-EM-EDICT-DOUBT-AS-MASS`).

---

## 3 · Mechanism (the effect)

**Glyph (proposed; the page names none).** `[Me]` **Measure** · Synonym · Urion —
because the working *is* a measurement, and the strike is the measurement made heavy —
laid across `[Al]` **Edge** · Root · Thalen. Both from the thirty unclassified forms in
`wiki/The Magic System/The Master Glyph Index — 136 Attested Forms.md`. The Index's
worked example is instructive beside this: `[Ur]` **Balance**, the Urion root, carries
Judicium among its seven attested Wellsprings, and the Index calls a root that broad
"a load-bearing member." `[Me]` is the Urion synonym in the measurement family and the
better fit for a working whose content is a reading.
*Filing decision, not canon — Isaac's ruling.*

**What boundary moves.** One quantity: **the effective mass coupled into a falling
blade, set equal to a dimensionless read of the target.** That is the whole
imposition, and it is unusually elegant: the boundary condition is *itself* a
measurement, which is why it costs a slow windup — you cannot read fast.

**What the law then does on its own.** Everything after, including both of the page's
weaknesses. The blow lands heavy because momentum is mass times velocity and the mass
went up. The windup telegraphs because **the read is the windup** — an integration time
is not optional for a measurement, and the same seconds that buy the absorbance buy the
target a warning. A fearless target denies it because the multiplier is a read and an
absent line reads as 1. A fast target denies it because the read is complete before the
blade is, and the blade is the slow part. **The page lists two weaknesses and they are
the same fact: measuring takes time.**

**Law V check, and a choice.** Stage VIII sits above Refraction, so no material anchor
is needed (`wiki/The Magic System/The Four Crafts.md`). He declares — Spellcraft,
*Ars Vocis*, "declared" — as on both his other pages. **Consistent across all three of
Drakvor's techniques and consistent with the doctrine the card gives him: a king
commands out loud.**

**Failure mode — Boundary fault.** "The condition was established imprecisely and the
law ran somewhere unintended" (`Two Sets of Books` §VII). The boundary is a read with a
finite integration time, and the imprecision is temporal: during the window the strike is
read-heavy and legible. The page's Limitation names it exactly — "the same mechanism that
reads the target's doubt also telegraphing the strike itself." Behind it sits a
**Structural fault** in the physical account that the page does not reach: a 0.5–2 TN
peak through a 10⁻⁷ m² edge is not a fault the Crystal fails at, it is a fault the
*blade* fails at, and nothing in the system covers a sword's material limit.
`SA-PHYS-TN-THROUGH-A-BLADE`.

**What the target sees and feels.** He is given time to understand it, which is
the working's design and its flaw at once. The blade *"darkens into geometric
iron-black facets as the strike builds"*, the air pulls inward just before it
falls, and the windup and strike together run about three seconds — long enough
for a competent opponent to do almost anything else. Then it lands with what the
page calls *"a verdict-like thud"*, and armour rated for less than B-Grade force
buckles rather than turning it. Against a target holding no doubt it is a heavy
downward blow at the S band. Against a target holding a great deal, it is twice
that, and the target has no way to tell from outside which one he has just been
hit by. The cruelty of the thing is in the coupling: **the reading that finds his
hesitation is the same reading that telegraphs the strike**, so the more carefully
Drakvor measures the man, the longer the man has to leave. That is the page's own
Limitation, in the page's own words — *"the same mechanism that reads the
target's doubt also telegraphing the strike itself."*

**What bleeds, at the stated efficiency.** η ≈ 0.55 (card): **45 percent** of every
expenditure as heat, sound and structural bleed. On an instantaneous working that bleed
arrives all at once and locally, which is the honest physical reading of the page's own
Target Response — "The air pulls inward just before it falls. The impact lands with a
verdict-like thud." A 45 % bleed on a kiloton-class delivery is not a thud. It is the
loudest thing on the field, and `Two Sets of Books` §III says so: "a low-efficiency
practitioner is loud, warm, and easy to find." As on his other two pages, 0.55 sits
**below Tier 6 · Master's 0.70–0.80 floor** (`SA-NUM-ETA-TIER`), and the card's tuned-
bastion escape clause does not apply to a sword swing.

---

## 4 · Essence ledger (units)

| Quantity | Value | Derivation |
|---|---|---|
| EU spent | `null` | No page figure; no Stage→EU formula. `SA-GAP-EU-FORMULA`. |
| Cost shape | **per full swing** | Page. Correct cadence for an instantaneous working. |
| Flux Density | `null` | No AU/s figure for Drakvor. |
| η | **0.55** (card) | Card line 42. Tier 6 band 0.70–0.80 — **below the floor**; the tuned-bastion clause does not cover this. `SA-NUM-ETA-TIER`. |
| AU/s | `null` | Needs Flux Density. |
| Duration | **6 s** windup-and-strike | Page, "the source's single old-count turn," at six seconds to the turn. |
| Baseline output | **4.184×10¹² – 2.42672×10¹³ J**, **0.5–2 TN** | S-Grade row, Part Four. Page's citation correct. |
| Doubled output | **8.37×10¹² – 4.85×10¹³ J**, **1–4 TN** | ×2. Upper end crosses into SS-Grade (4.184×10¹³ – 4.184×10¹⁴ J). |
| Stage VIII headroom | **none by allocation** | Part Five: Stage VIII is Max Grade S, ceiling 550, **no instability zone**. The "late push toward SS entry" belongs to **Stage IX**. `SA-NUM-EDICT-SS-PUSH`. |
| Multiplier | **1 to 2**, dimensionless | Page. Dimensionless because a spectroscopic absorbance is a ratio — which is the page's own open question, answered. |
| Armour defeat margin | **91× to 528×** over B-Grade | S-Grade band ÷ B-Grade ceiling 4.6024×10¹⁰ J. |
| **Edge contact stress at 0.5 TN** | **5×10¹⁸ Pa** | 5×10¹¹ N ÷ 1×10⁻⁷ m². Against diamond's ≈1.1×10¹¹ Pa limit: **≈4.5×10⁷ × over.** Minimum viable contact area: **4.5 m².** `SA-PHYS-TN-THROUGH-A-BLADE`. |
| Bleed | **45 %** | 1 − 0.55, delivered instantaneously and locally. |
| Minimum Stage | **VIII · Transcendence** | Page. Part Five. |
| Tier of Standing | **6 · Master** | Part Five. |
| Grade required | **S** (401–550) | Page. Card: Gnosis 430, Ardency 415 both S ✓. Meets at grade; Ardency 415 is near the S floor, which the card itself glosses — "Enough to end a siege engine, not to overwhelm a city." |
| Path gate | **Body** | Page. Ardency Penetration "requires Body Path at Stage III to exceed C" and Ardency Density "requires Body Path at Stage IV to exceed B" (Part Seven) — both open at Stage VIII. **Closes cleanly.** |
| Starvation margin | `null` | No cost figure, no reserve figure. |
| Developmental Tier | **Radiant** | Stage VIII (Part Twenty-One). |
| Crystal State | **Refined, overbuilt by design** | Card. |

**Does the physics close against the stratal account?** **Partly.** The read-and-
multiply mechanism closes beautifully and answers the page's own open question from the
register: a dimensionless absorbance needs no unit conversion, which is why a spectrum
can price a blade. The two accounts also agree on why the technique telegraphs, which no
rule had to state. **What does not close is the delivery.** Half a teranewton cannot pass
through a sword edge; it needs 4.5 m² of contact even against diamond. The other two
pages carrying the same S-Grade force figures have somewhere to put it — a 314 m²
footprint, a 6–18 m field. This one has a blade, and the system has no rule for what a
blade can carry. That is the sharpest physics-open item in Drakvor's three and it is put
to Isaac as `SA-PHYS-TN-THROUGH-A-BLADE`.

**Conflicts logged from this page:** `SA-PHYS-TN-THROUGH-A-BLADE`,
`SA-NUM-EDICT-SS-PUSH`, `SA-NUM-ETA-TIER`, `SA-GAP-TURN-LENGTH`,
`SA-GAP-EU-FORMULA`, `SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR`,
`SA-UNATT-COHERENCE-BAND`.

---

## 5 · Counterplay and the challenge

**The fairness check** (`.claude/skills/wotr-write/references/fair-play.md`).

| Test | Verdict | Why |
|---|---|---|
| Costs something that hurts | **pass, weakly** | *"Aether strain through his wrists and shoulders with every full swing."* It is located in tissue, it is per-use rather than per-scene, and it accumulates in the joints the working depends on — but there is no figure, no fraction of reserve, and no stated point at which the arm stops answering (`SA-GAP-EU-FORMULA`). For a technique that doubles its own output, this is the thinnest cost in the batch after `Dreambreaker Field`. |
| Stated limits | **pass** | Melee range, one named target, a single committed downward strike; **the windup is slow and telegraphs itself**; roughly three seconds from commitment to landing; the doubling requires doubt that is actually there. |
| Something beats it | **pass, three ways** | Resolve, speed, or evasion — all named, all available below his Stage. |
| It has a tell | **pass, the strongest on any offensive page here** | Facets darkening across the blade, then the air drawing inward. The page treats the tell as a design feature rather than an oversight, which is the right instinct. |
| Numbers in band | **flagged, already logged** | Stage VIII ⇒ Max Grade S (401–550), ceiling 550, Tier 6 (Part Five); card Gnosis 430 and Ardency 415 both S ✓. But the doubled impact leaves the S band — the page defends it by appeal to *"Stage VIII's own late push … toward SS-Grade"*, which is a reading of Part Five rather than a rule it states (`SA-NUM-EDICT-SS-PUSH`). η 0.55 against the Tier 6 floor of 0.70 (`SA-NUM-ETA-TIER`). |

**The Counterplay routes that work**
(`wiki/The Magic System/Counterplay What Beats a Practitioner.md`).

- **Break the man — by not being readable, which is the page's own Counter.** A
  Resolve-aligned Wellspring keeps a target's doubt *"from registering at all"*,
  and the doubling is gone. This is the register's **Rigidity** inverted: instead
  of presenting him with the situation his law handles worst, deny his law its
  input. The interesting consequence for a player is that the counter is a state
  of mind with a Wellspring behind it, so *being* fearless is not enough — it has
  to be fearlessness the reading cannot find a seam in.
- **Break the body — three seconds and a straight line down.** *"Distance. …
  Most practitioners are a threat about closing range."* This one is melee-only
  with a telegraphed windup. High-speed repositioning or a sublimation-type
  evasion gets a body out from under it before it lands, and the page says so.
  Compare *"Armour tiers"*: nothing under proofed plate is relevant here, since
  the strike buckles anything rated below B-Grade, so the answer is not to wear
  more but to not be there.
- **Break the boundary — the commitment, not the blade.** The strike is
  *committed to* against a named target. Interrupt the commitment — a second
  threat appearing inside the three seconds, a grapple, an ally stepping in — and
  the working is not weakened, it is **not performed**, because it exists only as
  a completed downward swing.
- **Deny the field — marginal.** Families **Fulguria / Materia**: *"Fulguria
  fails against boiled leather, fired clay, dense fog and a shielded interior"*,
  which reaches Judicium's reading half. In fog he can still swing; he cannot
  read as well what he is swinging at.

**The tell, stated plainly.** Facets crawl black across the blade, the air draws
in, and then it comes straight down. Three seconds, every time, and the better he
has read you the longer you have had.

**The lookup trail.**

1. `wiki/Techniques/Edict Strike.md` — the Limitation (the reading telegraphs the
   strike) and the Weakness (agile or genuinely fearless targets).
2. `wiki/The Magic System/Counterplay What Beats a Practitioner.md` — "Rigidity",
   "Distance", "Armour tiers".
3. `wiki/Fracture of Worlds — The Living System/III. Physical Force (Part Eleven).md`
   — the force bands, so a reader can work out what 0.5–2 TN does to what they are
   wearing, and what doubling it would mean.
4. `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`
   — Part Four for the S band and the standing differential rule; Part Five for
   whether an SS "late push" at Stage VIII is a thing the system actually grants.
5. `wiki/The Eight Families & the Sixty Wellsprings/Fulguria — Electromagnetism.md`
   — Judicium's law of discernment, which is what is reading the hesitation.
6. `wiki/Volume I — Character Cards/Drakvor · The Black-Crowned Bastion.md` —
   Ardency 415, glossed on the card as *"enough to end a siege engine, not to
   overwhelm a city"*, and Dexterity 355, which is how fast the windup is not.

**Conflicts added by this section:** `SA-EM-EDICT-DOUBT-AS-MASS`,
`SA-GAP-COUNTERPLAY-TERRAIN`.
