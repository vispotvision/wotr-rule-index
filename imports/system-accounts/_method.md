# System accounts — the method, and every number the batch is allowed to use

This file is the shared derivation toolkit for `imports/system-accounts/`. Each
account cites it rather than restating it seventy-six times. Every row below is
quoted or read straight off a system page; nothing here is invented.

**Scope note (WAR-7, 2026-09-25).** This file was written for the first
**twenty-eight** accounts and was not revised as the batch grew to **seventy-six**
(56 under `Techniques/`, 20 under `Spellcraft/`). Sections I–IX are general and
hold for all seventy-six. The passages that *enumerate* the batch — the lens list
in §X.1, the conflict counts in §X.3 and the AU/s claim in §VIII — described the
first twenty-eight only, and are corrected or scope-marked below rather than
re-enumerated, since listing 76 lenses is the writing issues' work and not this
review's.

Standard: `wiki/The Magic System/The Physical Account Two Sets of Books.md` —
"The Continuum keeps two sets of books on every working ever performed, and they
balance." Each account carries five sections: the physical half; the stratal
half, closing on a **lens** from philosophy or historical pseudoscience; the
**mechanism, which is the effect**; the ledger in Essence Units; and the
**counterplay and challenge** — a fairness check and a lookup trail. Sections 2,
3 and 5 answer to Isaac's two later rulings, set out in §X below.

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
| V | Splintering | B (stops at 275) | 350; 276–350 under strain | 5 · Expert | 0.50–0.60 *(unruled — see `C-063`)* | Harmonic |
| VI | Glory | A | 400 | 5 · Expert | 0.60–0.70 (**R44-4**) | Harmonic |
| VII | Refraction | A (stops at 400) | 475; 401–475 under strain | 5 · Expert | 0.60–0.70 (**R44-4**) | Resonant |
| VIII | Transcendence | S | 550 | 6 · Master | 0.70–0.80 | Radiant |
| IX | Invocation | S (stops at 550) | 625; 551–625 under strain | 6 · Master | 0.70–0.80 | Sovereign |
| XII | Emanation | SSS | 950 | 7 · Grandmaster | 0.85–0.90 | Sovereign |
| XIV | Zenith | EX | 1,500 | 8 · Archmaster | 0.95–1.2 | Crystallized Soul |

The η column carried the **efficiency conflict the source flags itself**: Part
Seventeen rates Class I Muridic at thirty to forty percent loss (η 0.60–0.70)
while the Tier table put Glory-Stage practitioners at 0.50–0.60, quoted and not
resolved (`Part Nineteen`, the boxed note). **That is CONFLICTS.md C-037 and
R44-4 has closed it** (`RULINGS.md`:704–716, 2026-09-25): *"Part Seventeen
governs: η reads 0.60 to 0.70 at Stage VI–VII. Part Nineteen's Tier 5 row is
corrected to match."* The Stage VI and VII rows above are corrected accordingly
and every account in this batch that reads them has been corrected with them.
**Stage V is not**: the row R44-4 edits spans "V–VII Splintering to Refraction"
with one η cell, while the sentence it rules names Stage VI–VII only, so the
three Stage V accounts keep 0.50–0.60 until that is ruled — `C-063`. The boxed
note on the source page itself is left exactly as written, which R44-4 says to
do, so the mirror still reads the conflict as open.

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
sub-pages that have not been mirrored. Every glyph *proposed* in this batch is drawn
from the thirty, whose fifteen Roots the Index itself describes as naming "a
**kind of limit**, applicable to any law at all" — which is exactly the field
section 3 of an account needs. **No page among the fifty-six `Techniques/` pages
names a glyph.** Each assignment for those is therefore marked *proposed*, made
under the Index's own
Standing Note ("Assignment is decided after the phenomenon, never before, and it
is a filing decision rather than a generative one"), and none is canon until
Isaac rules. See `_conflicts.jsonl`, `SA-GAP-GLYPH-MIRROR`.

**Two `Spellcraft/` pages do name glyphs, and neither set is attested** — a case
this section did not originally allow for. Anointing names **Lo · Wy · Ka**;
Transposition names its own chain. In both, the page's readings disagree with canon
or are absent from it, and **none of the named forms appears among the thirty
mirrored entries**. Those two accounts therefore propose *no* substitute — over a
page-named glyph a proposal would be a third reading rather than a check — and log
the glyphs instead (`SA-UNATT-ANOINTING-GLYPHS`,
`SA-UNATT-TRANSPOSITION-GLYPHS`). The batch thus holds **proposed** glyphs on the
Techniques and **unattested page-named** glyphs on those two, and the two cases
must not be read as one.

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
| Draven Kael Vorrick | VI Glory | 178 | A, ceiling 400 | ~0.55 | 0.60–0.70 ✗ (**R44-4**); card governs (`C-062`) | Refined | null | null |
| Aeldoris Vanthryx | VII Refraction | 195 | A→S, ceiling 475 | ~0.65 | 0.60–0.70 ✓ (**R44-4**) | Refined, residue-heavy | null | null |
| Francis Alexander | XIV Zenith | 470 | EX, ceiling 1,500 | 0.93 | 0.95–1.2 ✗ | "Absolute Crystal" | 2,800,000 (`Dirge Ascension`) | 2,800,000 ÷ 0.93 = **3,010,753 EU/g** |
| Opalis | XII Emanation | 301–400 (Band IV) | SSS, ceiling 950 | no card | 0.85–0.90 | null | null | null |
| Tovain Zethriel | IX Invocation | null | S→SS | no card | 0.70–0.80 | null | null | null |

Three of the five η figures sit outside the Tier of Standing band their Stage
puts them in, and all five cards carry a lettered **Coherence Band**, retired
under R42. Both logged, neither resolved (`SA-NUM-ETA-TIER`,
`SA-UNATT-COHERENCE-BAND`). **R44-4 changed which three**: it corrected Tier 5's
cell to 0.60–0.70, which brought Aeldoris's 0.65 inside his band and put Draven's
~0.55 below his. The count is unchanged at three — Drakvor, Draven, Francis —
and Draven's case was `C-062`, **ruled on 2026-09-25** (agent ruling, Isaac's rung
**I-2**, WAR-132): his card's ~0.55 governs and the corrected Tier 5 row is a
typical range for him, so he sits outside his band **lawfully** and no figure
moves. Drakvor's and Francis's bands are Tier 6 and Tier 8, which R44-4 does not
touch and which that ruling does not name; they stay logged and unruled under
`SA-NUM-ETA-TIER`.

**Six** sourced AU/s figures exist in the batch, across seven Stages, with no
scaling rule between them (`SA-CROSS-AUS-LADDER`). The table above holds the two
the first twenty-eight accounts had; the Spellcraft section added four more, all
stated on cards:

| Practitioner | Stage (card) | Flux Density | η | AU/s | R44-2 closes? |
|---|---|---|---|---|---|
| Niran Yukari | VII | 18,400 EU/g | 0.89 | 16,376 | ✓ 18,400 × 0.89 = 16,376 |
| Muken Moto | X · Realization | 18,600 EU/g | 0.84 | 15,624 | ✓ 18,600 × 0.84 = 15,624 |
| Dougou Ozumu Zettari | XIII · Principality | 18,400 EU/g | 0.99 | 3,900 external | ✗ `CONFLICTS.md` C-054, open |
| Gimbzo | "XII — Zenith" | 9.2×10⁶ EU/g | 0.94 | 6.7×10¹⁴ | ✗ `CONFLICTS.md` C-053, open |

**They are not monotone in Stage.** Niran at Stage VII outputs *more* than Muken
at Stage X, and both of those cards satisfy R44-2 exactly, so neither can be set
aside as an arithmetic slip. Any monotone Stage-to-AU/s ladder is therefore
unfittable to the attested cards without editing one of them
(`SA-CROSS-AUS-NOT-MONOTONE-IN-STAGE`).

## IX · What could not be checked at all

The issue asks that real physics close against "the Aetheric Density ceiling the
system allows at that site." **Aetheric Density has no numeric scale anywhere in
the system.** `The Core Vocabulary` defines it as "the concentration of Aether
present in a given volume. Sets the ceiling on the AU/s output a practitioner can
achieve in that location," and the density scale in `The Eight Families & the
Sixty Wellsprings` runs Ambient Saturation → Active Concentration → Veil-Thin
Nexus → Wellspring Core, which is four named conditions and no units. So the
joules-against-ceiling test the issue asks for cannot be run on any of the
seventy-six. Logged as `SA-GAP-AETHERIC-DENSITY`, the batch's largest gap. No
account in the batch claims to clear or breach a ceiling; each says it cannot be
checked and stops there (verified across all seventy-six under WAR-7).

Each physical account below therefore states its energy budget in SI and says
where those joules were sitting, and stops there. It does not claim the working
clears or breaches a ceiling, because there is no ceiling to clear.

## X · The two later rulings, and what they changed

Isaac widened the format twice after the first seventeen accounts were written.
Both are applied to all **seventy-six**: every account carries the five sections
under their exact titles, every one names a credited lens, every one closes §3 on
what the target sees and feels, and none carries a separate effect description —
the retired heading *"The effect in plain words"* appears in none of the
seventy-six and *"The phenomenon in plain words"* in all of them (verified
mechanically under WAR-7).

### X.1 · Addendum 1 — fair, a challenge, and a wider well

`.claude/skills/wotr-write/references/fair-play.md`. His words: "I want it to be
a 'Challenge' want people to have to think look up stuff thats the whole fun of
this" and "incooperated philosophers different pseudoscientific stuff just
explore a lot of things".

**Section 2 closes on a lens.** One idea from philosophy or historical
pseudoscience, credited by thinker and work, that fits the working: it explains
how the law is *understood or believed*, and it never changes a mechanic or a
number. Every lens in this batch also names the **productive misreading** — the
school that reads the working through the lens wrongly, and what that school gets
killed by. **The first twenty-eight, in page order** (the later forty-eight name
their lenses on the page and are not enumerated here): Aristotle's four causes · alchemical
palingenesis (Kircher) · Leibniz's compossibility · Stoic pneuma and *tonos*
(Chrysippus) · Bergson's *élan vital* · Cusa's *coincidentia oppositorum* ·
Kepler's *Harmonices Mundi* · James's specious present · *solve et coagula*
(Valentine) · Goethe's *Farbenlehre* · *nomos* against *physis* (Antiphon) ·
Lavoisier's caloric · Dionysian theosis · Zhuangzi's butterfly · the *vis
imaginativa* (Avicenna, Agrippa) · Austin's performatives · the tulpa
(David-Néel) · Berkeley's *esse est percipi* · Ficino's musical medicine · Zeno's
dichotomy · Plotinian emanation · Democritus' *eidola* · Mesmer's animal
magnetism · the *Kybalion*'s Hermetic Principles · Plato's wax tablet · Plato's
cave · Paracelsus on signatures · Aristotle on cold as an active quality.

**Section 5 is new.** The **fairness check** — five tests from the brief (a cost
that hurts, stated limits, something beats it, a tell, numbers in band), each
with a pass or fail and its reason. Then the **Counterplay routes that work**,
named against the four in `wiki/The Magic System/Counterplay What Beats a
Practitioner.md` and quoted from it, including routes the technique page omits.
Then the tell, stated plainly. Then the **lookup trail**: the pages a player
would have to read to assemble the counter, as a list of paths. Pieces, never the
solution — no account spells the answer out.

**New conflict kind `fairness`:** the working fails one of the five checks. Eight
are logged. Never nerfed silently.

### X.2 · Addendum 2 — the mechanism IS the effect

Isaac, logged in `RULINGS.md`: "the mechanism in the effect should be the SAME
thing the Mechanism is the Effect or how it works."

- Section 3 is titled **Mechanism (the effect)** and follows the working from the
  glyph's boundary, through the law, to **what the target sees and feels** — which
  is now the closing paragraph of every section 3.
- **There is no separate effect description anywhere in an account.** Section 1's
  lead-in, formerly "The effect in plain words", is now "The phenomenon in plain
  words" and states the physical situation rather than the outcome.
- **New conflict kind `effect-mechanism`:** a wiki page's Effect line describes
  something its Mechanism line does not produce, or the reverse. Thirteen are
  logged.

### X.3 · The questionnaire

`_conflicts.jsonl`, one JSON line per conflict, **397 rows** (104 at the end of
the first twenty-eight accounts), each carrying `id`, `page`, `kind`, both quotes
with their paths, `why`, and two to four `options` with what each would change.
Kinds: `gap` 105 · `cross-page` 83 · `number` 65 · `physics-open` 51 ·
`effect-mechanism` 32 · `fairness` 30 · `unattested` 21 · `off-system` 10.
Every `SA-` identifier cited anywhere in the seventy-six
accounts resolves to a row, and every row is cited by at least one account
(re-checked mechanically under WAR-7).
**Nothing is resolved.** The four largest are `SA-GAP-EU-FORMULA`,
`SA-GAP-AETHERIC-DENSITY`, `SA-GAP-GLYPH-MIRROR` and `SA-GAP-TURN-LENGTH`, and
each of them blocks a check the issue asked for.
