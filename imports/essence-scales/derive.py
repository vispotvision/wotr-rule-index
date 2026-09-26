#!/usr/bin/env python3
"""SUPERSEDED 2026-09-26 (C-076): documents the Grade-bracket derivation only; do not re-run.

Write `_derivation.md`: the essence scales with every step of their arithmetic.

WAR-161. The prose is here; every figure comes from `scales.py`, so the document
cannot drift from the computation. Run after any change to an anchor:

    python3 imports/essence-scales/derive.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scales  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FOW2 = ("wiki/Fracture of Worlds — The Living System/"
        "II. Grades, Gates and Thresholds (Parts Four–Ten).md")
FOW7 = ("wiki/Fracture of Worlds — The Living System/"
        "VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen).md")

rows = scales.rows()
tiers = scales.tier_rows(rows)
S = {r["stage"]: r for r in rows}


def f(x):
    return scales.sig(x)


DOC = f"""# The essence scales — EU by Stage, the AU/s ladder, AU to joules, the turn

WAR-161. Every figure in this file is computed by `scales.py` from four quoted
anchors and three ruled constants. Nothing is typed and nothing is invented: the
two ladders below are Part Four and Part Five as they stand, read at the constant
R44-1 fixes, with the set point C-059 already uses. `derive.py` writes this file.

## The three constants

| constant | value | where it is ruled |
|---|---|---|
| 1 EU | 1 MJ | `RULINGS.md`, 2026-09-25, **R44-1-EU_JOULE_ONE_MEGAJOULE** |
| 1 AU | 1 EU, so 1 AU/s = 1 MW | `RULINGS.md`, 2026-09-26, WAR-3 card 1 q3 — "an AU-to-joule rate" |
| one turn | {int(scales.TURN_SECONDS)} seconds | `RULINGS.md`, 2026-09-26, WAR-3 card 1 q7 — "one turn = 6 seconds" |

The second and third are Isaac's answers to the WAR-3 questionnaire, recorded in
full on that issue's comments of 2026-09-26 and in `RULINGS.md` under
*2026-09-26 — WAR-3 cards 1 and 2 (system accounts, 20 answers)*.

## Anchor one — Part Four, Grade to attack output

`{FOW2}`, Part Four. The joule column is the whole basis of the EU ladder, so it
is reproduced here exactly as the page writes it:

| Grade | Sub-Stat value | Attack output |
|---|---|---|
""" + "\n".join(
    f"| {g[0]} | {format(g[1], ',')}{'–' + format(g[2], ',') if g[2] else '+'} | {g[5]} |"
    for g in scales.GRADES) + f"""

## Anchor two — Part Five, Stage to Max Grade and Tier of Standing

The same file, Part Five. Two columns matter: **Max Grade**, which "binds
allocation: a Sub-Stat may not be allocated past the top of the Stage's Max Grade
bracket", and **Sub-Stat ceiling**, which at Stages V, VII, IX and XI sits *above*
that bracket — "the instability zone, reachable only under strain, never by
allocation".

## Anchor three — Part Nineteen, efficiency by Tier of Standing

`{FOW7}`, Part Nineteen. The η column as it stands after **R44-4**, which
corrects the Tier 5 cell to 0.60–0.70 (applied to the live page under WAR-133;
the mirror lagged when this was written). Tier 9 is "above 1.2, unbounded".

## Anchor four — the Stages whose force is not measured

Part Four, the same file: "At **Zenith, Stage XIV**, speed and attack output are
no longer assessed by conventional metrics." Isaac's WAR-142 answer carries that
upward — "Stage XV keeps its EX+ Grade label, but its force is unmeasured like
Zenith's; the Zenith row sits beside the Grade ladder, not on it" — and Apex
states no Max Grade at all. **Stages XIV, XV and XVI therefore take no derived EU
or AU/s figure.** Every cell for them below reads *unmeasured*, not null: the
absence is ruled, not missing.

## The EU-by-Stage benchmark — the arithmetic, once

For a Stage, Part Five gives the Max Grade *G*; Part Four gives *G*'s
attack-output floor and ceiling in joules. At 1 EU = 1 MJ the band in EU is those
two bounds divided by 10⁶. The benchmark inside the band is **C-059's set point**,
the same one WAR-46 already applies to twelve cards: √(floor × ceiling) ÷ 1 MJ, at
four significant figures — the precision Part Four's own bounds carry.

> Each card whose reserve R44-1 puts outside its Stage's band is scaled by one
> factor: factor = (the band midpoint in decades, the geometric mean of floor and
> ceiling joules / 1 MJ) / (the card's stated reserve).

So this table is not a new scale. It is the band and the set point C-059 names,
written out once per Stage instead of being recomputed per card. Two checks prove
it is the same arithmetic:

- Stage XII's benchmark is **{f(S['XII']['eu_benchmark'])} EU**, which is exactly
  the set point `reports/eu_card_scaling_2026-09-25.md` computed for the Arctic
  Lion sheet.
- Stage XIII's is **{f(S['XIII']['eu_benchmark'])} EU**, exactly the set point the
  same report computed for Dougou Ozumu Zettari.

Worked once in full, at Stage VIII: Part Five gives Max Grade **S**; Part Four
gives S as {f(scales.GRADE['S'][3])}–{f(scales.GRADE['S'][4])} J; at 1 MJ that is
{f(S['VIII']['eu_floor'])}–{f(S['VIII']['eu_ceiling'])} EU; the set point is
√({f(scales.GRADE['S'][3])} × {f(scales.GRADE['S'][4])}) =
{f((scales.GRADE['S'][3] * scales.GRADE['S'][4]) ** 0.5)} J ÷ 1 MJ =
**{f(S['VIII']['eu_benchmark'])} EU**.

**The plateaux are real and are not an error.** Stages IV and V share Max Grade B,
VI and VII share A, VIII and IX share S, X and XI share SS, so each pair shares a
band. The second Stage of each pair is the instability Stage, and what rises there
is the Sub-Stat ceiling, not the allocation bracket. Part Four's Sub-Stat column
says which Grade that raised ceiling reaches, and the *Under strain* column below
is that Grade's band: Stage V's ceiling of {S['V']['substat_ceiling']} sits in the
A bracket, so a Stage V practitioner under strain reaches
{f(S['V']['strain_eu_floor'])}–{f(S['V']['strain_eu_ceiling'])} EU and no further.

**Below Stage III a benchmark reserve is a fraction of one EU.** At 1 EU = 1 MJ
this follows: a Murmuring practitioner's whole attack output is
{f(scales.GRADE['E'][3])}–{f(scales.GRADE['E'][4])} J, which is
{f(S['I']['eu_floor'])}–{f(S['I']['eu_ceiling'])} EU. The figures are written as
computed. Whether the unit should carry a floor at the bottom of the ladder is a
question for Isaac, not a number to invent, and it is on the rolling
questionnaire.

## The AU-to-joule equivalence

One AU is one EU, so one AU is 1 MJ and **1 AU/s = 1 MW**. *The Core Vocabulary*
already states which side of η the rate sits on, and this file follows it rather
than offering a second reading: **AU/s is the draw**, power drawn is AU/s × 1 MW,
power delivered is AU/s × η × 1 MW, "and the difference leaves as waste heat. Time
to empty is reserve ÷ AU/s, and that figure does not depend on the conversion at
all." Three identities follow and are used throughout:

- **drawn** by a working of *R* AU/s held for *t* seconds = *R* × *t* EU.
- **delivered** over the same *t* = *R* × *t* × η MJ.
- **time to empty** a reserve of *E* EU at *R* AU/s = *E* ÷ *R* seconds.

## The AU/s progression — the arithmetic, once

The EU ladder is a ladder of reserves, read off the same Part Four column C-059
reads, and a reserve becomes a rate the moment a turn has a length. A Stage's AU/s
band is its EU band spread over one turn: floor and ceiling
÷ {int(scales.TURN_SECONDS)} s. The benchmark AU/s is the benchmark reserve
÷ {int(scales.TURN_SECONDS)}.

That fixes one plain reading of the whole ladder: **the benchmark reserve is
exactly one turn of draw at the benchmark rate.** Time to empty is E ÷ R, and by
construction E ÷ R = {int(scales.TURN_SECONDS)} s at every Stage. A practitioner
who opens at their Stage's benchmark rate has six seconds of it and nothing after,
which is why sustained work runs far below the benchmark and why the Starvation
floor at ten percent is reachable inside a single exchange.

**The check that the ladder is the same arithmetic as C-059.** The last column of
the AU/s table is what the benchmark reserve delivers in that turn — reserve × η ×
1 MJ, at the tier's η midpoint — and at every Stage it lands back inside the Part
Four band the reserve was read from. At Stage XIII that figure is
{f(S['XIII']['eu_benchmark'] * 1.075 * scales.EU_JOULE)} J, which is the same
number `reports/eu_card_scaling_2026-09-25.md` prints as its check line for Dougou
Ozumu Zettari. The ladder closes on itself.

**Against the attested cards.** The ladder is checkable and it is not a fit: it
was derived from the tables alone and then read against the cards. Niran Yukari's
16,376 AU/s at Stage VII sits inside
{f(S['VII']['aus_floor'])}–{f(S['VII']['aus_ceiling'])}, and Gimbzo's 6.7×10^14 at
Stage XII sits inside {f(S['XII']['aus_floor'])}–{f(S['XII']['aus_ceiling'])}.
Others sit outside; `reports/essence_scales_2026-09-26.md` reads every one of them
and says which and by how much. **No card figure is moved by this file.** Isaac's
answer to WAR-3 card 1 q2 asks that cards missing the ladder be corrected, and
R44-5's operative sentence — "the card's η governs per character and the tables are
typical ranges" — says an outlier card is lawful. The two do not agree about which
gives way, and until that is answered the published ladder is typical ranges and no
card is overwritten. The question is on the rolling questionnaire.

## η above 1.0

Part Nineteen's Tier 8 row already says what happens there: "Above 1.0 the
Continuum recognizes the expression as law and supplements it with ambient flow;
the environment becomes a co-author." `The Physical Account — Two Sets of Books`
says where the energy is: "a working's energy budget balances at the Aether stratum
and not at the Essence one. The practitioner does not supply the joules. They
supply the boundary condition." Isaac's answer to card 1 q9 makes the reading
explicit and puts it in the Core Vocabulary: η above 1.0 is real, and the surplus
is drawn from the Aether stratum. It is not the Crystal returning more than it
spent; it is the stratum paying the difference, which is why the figure is a ratio
of delivered effect to Essence spent and not a violation of anything.

## The tables

""" + scales.markdown() + """

## Reading a duration in turns

A duration stated in turns is that many times six seconds. Nine technique pages
carried a conversion at **five** seconds a turn and are corrected;
`reports/essence_scales_2026-09-26.md` lists each, with the figure before and
after. A "turn" that is not a combat turn — a lunar turn, a turn of a glass, a
siege turn on a campaign clock, a coil that runs one turn longer — is not a
duration and is left alone; each of those is listed too.
"""

if __name__ == "__main__":
    out = os.path.join(HERE, "_derivation.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(DOC)
    print(f"wrote {out} ({len(DOC.splitlines())} lines)")
