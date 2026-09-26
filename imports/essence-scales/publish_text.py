#!/usr/bin/env python3
"""The exact text published to Notion, generated so no figure is typed.

WAR-161. Writes two files, which are what goes on the live pages and nothing else:

  _part_nineteen.md   the three subsections inserted into Part Nineteen
  _core_vocabulary.md the replacement strings for The Core Vocabulary, one per line
                      block, as `OLD<<<>>>NEW` pairs

Clean publishing: nothing below names a ruling, a conflict, an issue, a tool, a
person or a process. The pages carry the result as settled text.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scales  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
rows = scales.rows()
tiers = scales.tier_rows(rows)
S = {r["stage"]: r for r in rows}
f = scales.sig
T = int(scales.TURN_SECONDS)


def eta_cell(r):
    lo, hi = r["eta"]
    if hi is None:
        return f"above {lo:.1f}"
    if lo == hi:
        return f"~{lo:.2f}"
    return f"{lo:.2f}–{hi:.2f}"


def rng(a, b):
    if a is None and b is None:
        return "unmeasured"
    if b is None:
        return f"{f(a)} and above"
    return f"{f(a)}–{f(b)}"


eu_rows = []
for r in rows:
    if r["stage"] in scales.UNMEASURED:
        strain = "not assessed by conventional metrics"
    elif r["strain_grade"]:
        strain = (f"{r['strain_grade']}-Grade reach, "
                  f"{rng(r['strain_eu_floor'], r['strain_eu_ceiling'])}")
    else:
        strain = "—"
    eu_rows.append(
        f"| {r['stage']} | {r['name']} | {r['max_grade'] or 'uncapped'} | "
        f"{rng(r['eu_floor'], r['eu_ceiling'])} | "
        f"{f(r['eu_benchmark']) or 'unmeasured'} | {strain} |")

aus_rows = []
for r in rows:
    lo, hi = r["eta"]
    mid = (lo + hi) / 2 if hi else None
    delivered = (f(r["eu_benchmark"] * mid * scales.EU_JOULE) + " J"
                 if (r["eu_benchmark"] and mid) else "unmeasured")
    aus_rows.append(
        f"| {r['stage']} | {r['tier']} · {r['tier_name']} | {eta_cell(r)} | "
        f"{rng(r['aus_floor'], r['aus_ceiling'])} | "
        f"{f(r['aus_benchmark']) or 'unmeasured'} | {delivered} |")

tier_rows_md = []
for t in tiers:
    lo, hi = t["eta"]
    eta = (f"above {lo:.1f}" if hi is None else
           (f"~{lo:.2f}" if lo == hi else f"{lo:.2f}–{hi:.2f}"))
    note = ""
    if t["unmeasured"] and t["aus_benchmark"]:
        note = (" — " + " and ".join(t["unmeasured"]) +
                (" are" if len(t["unmeasured"]) > 1 else " is") + " unmeasured")
    tier_rows_md.append(
        f"| {t['tier']} · {t['tier_name']} | "
        f"{t['stages'][0] if len(t['stages']) == 1 else t['stages'][0] + '–' + t['stages'][-1]} | "
        f"{eta} | {rng(t['eu_floor'], t['eu_ceiling'])} | "
        f"{rng(t['aus_floor'], t['aus_ceiling'])} | "
        f"{(f(t['aus_benchmark']) or 'unmeasured')}{note} |")

PART_NINETEEN = f"""### The Turn, and What a Unit Is Worth

**One turn is {T} seconds.** Every duration the system states in turns is read \
through that figure: a working held three turns is held {3*T} seconds, a field \
that stands eight turns stands {8*T}.

**One EU is one megajoule.** One AU is one EU, so **1 AU/s is 1 MW**. Power drawn \
is AU/s × 1 MW, power delivered is AU/s × η × 1 MW, and the difference leaves as \
heat, sound and structural bleed. A reserve of *E* EU spent at *R* AU/s empties in \
*E* ÷ *R* seconds, and that figure does not depend on the conversion at all.

### The EU Band by Temperance Stage

A Stage's Max Grade fixes the magnitude its practitioners can put into the world, \
and the Grade ladder states that magnitude in joules. At one megajoule to the EU \
those bounds are a reserve band, and the benchmark inside each band is its \
midpoint in decades, the geometric mean of floor and ceiling. A reserve at the \
benchmark, spent at that Stage's efficiency, delivers the middle of the Grade the \
Stage tops out at — which is what makes the benchmark the figure to build a sheet \
around rather than a number chosen for convenience.

| Stage | Name | Max Grade | EU band | Benchmark reserve | Under strain |
|---|---|---|---|---|---|
""" + "\n".join(eu_rows) + f"""

At Stages V, VII, IX and XI the Sub-Stat ceiling sits above the Max Grade bracket, \
and the **Under strain** column is what that raised ceiling reaches. It is not a \
second allocation. It is what the instability zone permits before the Crystal \
answers for it.

At Zenith and above, force is not assessed by conventional metrics, and the ladder \
stops there rather than guessing. At the bottom it runs the other way: below \
Ascension a benchmark reserve is a fraction of one EU, because an Initiate's whole \
output is a few hundred to a few thousand joules. The unit was cut for \
practitioners who move more than that.

### The AU/s Progression

A reserve becomes a rate the moment a turn has a length. A Stage's AU/s band is \
its EU band spread across one turn, and the benchmark rate is the benchmark \
reserve spent inside a single turn. That is the plainest statement of what full \
output costs: **open at your Stage's benchmark rate and you have {T} seconds of \
it, and nothing after.** Sustained work therefore runs far below the benchmark, \
and the ten percent Starvation floor is reachable inside one exchange by anyone \
who forgets it.

| Stage | Tier of Standing | η | AU/s band | Benchmark AU/s | Delivered in one turn |
|---|---|---|---|---|---|
""" + "\n".join(aus_rows) + """

The last column is what the benchmark reserve delivers across that turn at the \
tier's efficiency, and at every Stage it lands back inside the Grade band the \
reserve was read from. The ladder closes on itself, which is the only reason it \
can be trusted at the top, where the figures stop being imaginable.

Read by standing rather than by Stage, the same ladder runs:

| Tier | Temperance | η | EU band | AU/s band | Benchmark AU/s |
|---|---|---|---|---|---|
""" + "\n".join(tier_rows_md) + """

A tier spans every Stage under it, so a tier band is wider than any of its Stages' \
and says less. Where a page names a Stage, the Stage band governs; the tier band \
is for a practitioner whose standing is known and whose Stage is not.

"""

# --- The Core Vocabulary: exact old -> new, one pair per line block -----------
ETA_OLD = ("**Efficiency · Eta · η** · The ratio of Essence spent to Essence that "
           "arrives as intended effect. An η of 0.50 wastes half of every "
           "expenditure as heat, noise, and structural bleed. The single most "
           "important variable in how long a reserve lasts under sustained output.")
ETA_NEW = ETA_OLD + (" **An η above 1.0 is real.** More arrives than the Crystal "
                     "spent because the surplus is drawn from the Aether stratum: "
                     "the practitioner supplies the boundary condition and the "
                     "stratum supplies the joules, and above 1.0 the Continuum "
                     "recognises the expression as law and supplements it with "
                     "ambient flow. It is not a reserve returning more than it "
                     "held, and it is not an error on the sheet.")

EU_OLD = ("**EU · Essence Units** · The raw reserve. Total volume of usable Essence "
          "stored in the Crystal at any given moment, also called Essence Volume. "
          "Scales with Temperance Stage.")
EU_NEW = ("**EU · Essence Units** · The raw reserve. Total volume of usable Essence "
          "stored in the Crystal at any given moment, also called Essence Volume. "
          "Scales with Temperance Stage, and the band and benchmark reserve for "
          "each of the sixteen Stages are set out in Fracture of Worlds Part "
          "Nineteen.")

TURN_OLD = ("**The Essence Ledger** · [Fracture of Worlds Part Twenty-Three]")
TURN_NEW = (f"**Turn** · {T} seconds. The unit every stated duration in turns is "
            f"read through, in a duel and on a campaign clock alike: a working "
            f"held three turns is held {3*T} seconds. A reserve spent at *R* AU/s "
            f"for one turn is {T}*R* EU gone, delivering {T}*R* × η megajoules.\n"
            "**The Essence Ledger** · [Fracture of Worlds Part Twenty-Three]")

PAIRS = [(ETA_OLD, ETA_NEW), (EU_OLD, EU_NEW), (TURN_OLD, TURN_NEW)]

if __name__ == "__main__":
    with open(os.path.join(HERE, "_part_nineteen.md"), "w", encoding="utf-8") as fh:
        fh.write(PART_NINETEEN)
    with open(os.path.join(HERE, "_core_vocabulary.md"), "w", encoding="utf-8") as fh:
        for o, n in PAIRS:
            fh.write(o + "\n<<<>>>\n" + n + "\n===\n")
    print("wrote _part_nineteen.md and _core_vocabulary.md")
