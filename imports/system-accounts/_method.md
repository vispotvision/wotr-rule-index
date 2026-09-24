# System accounts — the method, and every number the batch is allowed to use

This file is the shared derivation toolkit for `imports/system-accounts/`. Each
account cites it rather than restating it twenty-eight times. Every row below is
quoted or read straight off a system page; nothing here is invented.

Standard: `wiki/The Magic System/The Physical Account Two Sets of Books.md` —
"The Continuum keeps two sets of books on every working ever performed, and they
balance." Each account carries the physical half, the stratal half, the mechanism
as a boundary condition, and the ledger in Essence Units.

---

## I · Grade to real force and energy

`wiki/Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md`,
Part Four. Sub-Stat value, attack output, travel speed.

| Grade | Sub-Stat value | Attack output (J) | Travel speed |
|---|---|---|---|
| B | 176–275 | 1.046×10⁹ – 4.6024×10¹⁰ | Mach 1.5–4 |
| A | 276–400 | 4.6024×10¹⁰ – 4.184×10¹² | Mach 5–25 |
| S | 401–550 | 4.184×10¹² – 2.42672×10¹³ | Mach 25–200 |
| SS | 551–725 | 4.184×10¹³ – 4.184×10¹⁴ | Mach 200–1,000 |
| SSS | 726–950 | 4.184×10¹⁴ – 4.184×10²¹ | 1–10% c |
| X | 951–1,200 | 4.184×10²¹ – 1.24×10²⁹ | 10–50% c |
| EX | 1,201–1,500 | 1.24×10²⁹ – 6.906×10³⁷ | 50–100% c |

Travel/reaction/attack speed by Grade is Part Six of the same file. One full Tier
Grade above an opponent "wins a direct exchange of that stat category without
meaningful contest" (Part Four).

## II · Stage to ceiling, Tier of Standing, Developmental Tier, efficiency

Stage, Max Grade, Sub-Stat ceiling and Tier of Standing: Part Five of the same
file. Efficiency by Tier of Standing: `VII. Aether Class, Essence Typology,
Aether Flow (Parts Seventeen–Nineteen).md`, Part Nineteen. Developmental Tier:
`VIII. Traits, Soul Crystal Tiers, Domains (Parts Twenty–Twenty-Two).md`,
Part Twenty-One.

| Stage | Name | Max Grade | Sub-Stat ceiling | Tier of Standing | η | Developmental Tier |
|---|---|---|---|---|---|---|
| V | Splintering | B (stops at 275) | 350; 276–350 under strain | 5 · Expert | 0.50–0.60 | Harmonic |
| VI | Glory | A | 400 | 5 · Expert | 0.50–0.60 | Harmonic |
| VII | Refraction | A (stops at 400) | 475; 401–475 under strain | 5 · Expert | 0.50–0.60 | Resonant |
| VIII | Transcendence | S | 550 | 6 · Master | 0.70–0.80 | Radiant |
| IX | Invocation | S (stops at 550) | 625; 551–625 under strain | 6 · Master | 0.70–0.80 | Sovereign |
| XII | Emanation | SSS | 950 | 7 · Grandmaster | 0.85–0.90 | Sovereign |
| XIV | Zenith | EX | 1,500 | 8 · Archmaster | 0.95–1.2 | Crystallized Soul |

The η column carries the **efficiency conflict the source flags itself**: Part
Seventeen rates Class I Muridic at thirty to forty percent loss (η 0.60–0.70)
while the Tier table puts Glory-Stage practitioners at 0.50–0.60. Quoted, not
resolved (`Part Nineteen`, the boxed note).

## III · The resource system

`wiki/The Magic System/The Core Vocabulary.md` §V, and Part Nineteen above.

- **EU · Essence Units** — the raw reserve. "Scales with Temperance Stage,
  governed primarily by Tempering Yield." **No formula converts a Stage into an
  EU figure anywhere in the system.** Every EU value in this batch is either
  quoted from a page or `null`. See `_conflicts.jsonl`, `SA-GAP-EU-FORMULA`.
- **Flux Density · EU/g** — compression, Essence per unit Crystal mass.
- **AU/s = Flux Density × η.** The one closed formula the system supplies. Given
  any two of the three, the third is arithmetic. This is how every derived Flux
  Density in the batch is obtained.
- **η · efficiency** — "the ratio of Essence spent to Essence that arrives as
  intended effect." Bleed fraction is therefore **1 − η**, leaving "as heat,
  sound, and structural bleed" (`Two Sets of Books` §III).
- **Essence Starvation** — "Below ten percent EU a practitioner suffers Essence
  Starvation: reduced stat expression, Shell degradation, Trait flickering."
  A starvation margin is only computable where the page states a cost as a
  *fraction of reserve*; where it states absolute EU and the reserve is unknown,
  the margin is `null`.

## IV · The two accounts, and the Four Faults

`Two Sets of Books`: "a working's energy budget balances at the Aether stratum
and not at the Essence one. The practitioner does not supply the joules. They
supply the boundary condition." So each physical account below states where the
joules were (ambient field, chemical store, kinetic store, the target's own
structure) and the stratal account states what the Crystal paid for moving the
boundary. The two are not translations of each other.

Faults, §VII: **Boundary** (condition imprecise, law ran somewhere unintended),
**Field** (room could not supply what the working assumed), **Structural**
(Crystal could not hold what the boundary permitted), **Coherence** (lived
behaviour and stated law drifted apart). Every account names one.

The Four Theories, §IV: **Consent Doctrine** (enforced), **Correspondence**,
**Debt**, **Residue**. An account only names a theory where the page's own
language leans on one.

## V · The glyph is a boundary condition

`wiki/The Magic System/The Master Glyph Index — 136 Attested Forms.md`: "A glyph
creates nothing and carries no power. … **A glyph is a boundary condition imposed
on that law.** It moves a limit, and the law does what it has always done on the
far side of the new limit." And: "A glyph cannot attack a law. Laws are not the
sort of thing that can be opposed."

**The repo mirror of the Index carries 30 of the 136 entries** — the unclassified
thirty, plus the worked examples `[Ur]` Balance and `[Lei]` Binding and the two
amendment entries `[Abys]` Deep and `[Th]` Foundation. The other 106 are Notion
sub-pages that have not been mirrored. Every glyph named in this batch is drawn
from the thirty, whose fifteen Roots the Index itself describes as naming "a
**kind of limit**, applicable to any law at all" — which is exactly the field
section 3 of an account needs. **No technique page in this batch names a glyph.**
Each assignment below is therefore marked *proposed*, made under the Index's own
Standing Note ("Assignment is decided after the phenomenon, never before, and it
is a filing decision rather than a generative one"), and none is canon until
Isaac rules. See `_conflicts.jsonl`, `SA-GAP-GLYPH-MIRROR`.

The thirty available: `[RenB]` Boundary · `[Ath]` Command · `[Ir]` Continuum ·
`[Cal]`/`[Kai]` Craft · `[Dom]` Dominion · `[Al]` Edge · `[AeV]` Era · `[Hael]`
Flame · `[Lh]` Frequency · `[On]` Light · `[Et]` Mirage · `[Ren]`/`[Ps]` Passage ·
`[Ser]` Renewal · `[Kael]` Ruin · `[Ae]` Vastness · `[Eq]` Equivalence · `[Frm]`
Form · `[Tir]` Hour · `[Sa]` Illumination · `[Vel]` Mind · `[Ho]` Order · `[Rv]`
Reverie · `[Ora]` Truth · `[Me]` Measure · `[Rt]` Return · `[Sil]` Silence ·
`[Knt]` Knot (Counter) · `[Lk]` Lock (Counter).

## VI · Reading a retired Sub-Stat name

`IV. The Eight Primaries and the Sixty-Four Sub-Stats (Part Twelve).md`, the
Merge Ledger: "Read a retired name on an older sheet as the entry that absorbed
it." The Wellspring registers and several technique pages use pre-merge names.
The translations this batch relies on, all from that ledger:

Ardency: Saturation/Duality → **Depth** · Radiance → **Compression** · Spectral →
**Cascade** · Detonation/Conversion → **Overchannel** · Inscription → **Density**.
Gnosis: Cartography → **Perception** · Adaptation → **Acuity** · Memorium →
**Retention** · Diagnosis → **Analysis** · Warding → **Cognition**.
Dexterity: Burst → **Celerity** · Equilibrium → **Economy** · Silence → **Feint**.
Harmonics: Memory/Fidelity → **Attunement** · Recovery/Voidance → **Stability** ·
Confluence → **Synergy**.
Resilience: Coherence → **Anchoring** · Insulation → **Fortification** · Nullity →
**Persistence**.
Tempering: Processing/Acceleration/Inheritance → **Maturity** · Conversion/Latency
→ **Yield** · Compression → **Clarity**.
Dominion: Reach → **Sovereignty** · Rift/Acuity → **Sense** · Density/Anchoring →
**Gravity** · Expansion → **Radius**.

A retired name on a page is therefore **not** a conflict. It is a reading.

## VII · Law V, the material anchor

`wiki/The Magic System/The Four Crafts.md`: "Below **Stage VII, Refraction**, a
working requires voice, hand, ink or blood: an external anchor for the boundary.
At Refraction the practitioner can hold the Crystal as an object of study and the
Glyph Roles compress into an internal chain that needs no material anchor at
all." Every account below Stage VII therefore checks that the page supplies an
anchor, and every internalised working checks it sits at Refraction or above.
This is one of the few system gates in the batch that closes cleanly on nearly
every page.

## VIII · The practitioners, and their sheet numbers

Card paths are under `wiki/Volume I — Character Cards/`. Flux Density is derived
from AU/s ÷ η where an AU/s figure exists, and is `null` otherwise.

| Practitioner | Stage | Level | Grade | η (card) | η (Tier table) | Crystal State | AU/s | Flux Density derived |
|---|---|---|---|---|---|---|---|---|
| Serenyra Vaelith | VIII Transcendence | 276 | S, ceiling 550 | ~0.70 | 0.70–0.80 ✓ | Refined | 22 (`Lumen Dissecans`) | 22 ÷ 0.70 = **31.4 EU/g** |
| Drakvor | VIII Transcendence | 295 | S, ceiling 550 | ~0.55 | 0.70–0.80 ✗ | Refined, overbuilt | null | null |
| Draven Kael Vorrick | VI Glory | 178 | A, ceiling 400 | ~0.55 | 0.50–0.60 ✓ | Refined | null | null |
| Aeldoris Vanthryx | VII Refraction | 195 | A→S, ceiling 475 | ~0.65 | 0.50–0.60 ✗ | Refined, residue-heavy | null | null |
| Francis Alexander | XIV Zenith | 470 | EX, ceiling 1,500 | 0.93 | 0.95–1.2 ✗ | "Absolute Crystal" | 2,800,000 (`Dirge Ascension`) | 2,800,000 ÷ 0.93 = **3,010,753 EU/g** |
| Opalis | XII Emanation | 301–400 (Band IV) | SSS, ceiling 950 | no card | 0.85–0.90 | null | null | null |
| Tovain Zethriel | IX Invocation | null | S→SS | no card | 0.70–0.80 | null | null | null |

Three of the five η figures sit outside the Tier of Standing band their Stage
puts them in, and all five cards carry a lettered **Coherence Band**, retired
under R42. Both logged, neither resolved (`SA-NUM-ETA-TIER`,
`SA-UNATT-COHERENCE-BAND`).

Two AU/s figures exist in the whole batch and they sit six Stages and five orders
of magnitude apart with no scaling rule between them (`SA-CROSS-AUS-LADDER`).

## IX · What could not be checked at all

The issue asks that real physics close against "the Aetheric Density ceiling the
system allows at that site." **Aetheric Density has no numeric scale anywhere in
the system.** `The Core Vocabulary` defines it as "the concentration of Aether
present in a given volume. Sets the ceiling on the AU/s output a practitioner can
achieve in that location," and the density scale in `The Eight Families & the
Sixty Wellsprings` runs Ambient Saturation → Active Concentration → Veil-Thin
Nexus → Wellspring Core, which is four named conditions and no units. So the
joules-against-ceiling test the issue asks for cannot be run on any of the
twenty-eight. Logged as `SA-GAP-AETHERIC-DENSITY`, the batch's largest gap.

Each physical account below therefore states its energy budget in SI and says
where those joules were sitting, and stops there. It does not claim the working
clears or breaches a ceiling, because there is no ceiling to clear.
