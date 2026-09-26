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
EU_TABLE, AU_TABLE, _ = scales.tables()
T = int(scales.TURN_SECONDS)

PART_NINETEEN = f"""### The Turn, and What a Unit Is Worth

**One turn is {T} seconds.** Every duration the system states in turns is read \
through that figure: a working held three turns is held {3*T} seconds, a field \
that stands eight turns stands {8*T}.

**One EU is one megajoule.** One AU is one EU, so **1 AU/s is 1 MW**. Power drawn \
is AU/s × 1 MW, power delivered is AU/s × η × 1 MW, and the difference leaves as \
heat, sound and structural bleed. A reserve of *E* EU spent at *R* AU/s empties in \
*E* ÷ *R* seconds, and that figure does not depend on the conversion at all.

### The EU Band by Temperance Stage

A reserve is set by Level and capped by Stage, by the law of reserves in Part \
Twenty-Three: log₁₀ EU = {scales.LAW_A} + {scales.LAW_B} × Level. A Stage's \
practitioners usually stand in its Band's cluster of Levels, and that cluster read \
through the law is the Stage's working band. The benchmark inside each band is its \
midpoint in decades, the geometric mean of floor and ceiling. The gate ceiling is \
the reserve at the Level the Stage cannot pass without its next Threshold, and it \
is hard where the working band is only typical.

""" + EU_TABLE + f"""

The floor is not a floor. A reserve below its working band is a practitioner who \
built a precise instrument instead of a large one, and it is lawful at any Stage. \
Above Zenith the Level scale ends, and a Revelation or Apex reserve is known only to \
stand above the highest reserve the scale can hold.

### The AU/s Progression

A reserve becomes a rate the moment a turn has a length. A Stage's AU/s band is \
its working band spread across one turn, and the benchmark rate is the benchmark \
reserve spent inside a single turn. That is the plainest statement of what full \
output costs: **open at your Stage's benchmark rate and you have {T} seconds of \
it, and nothing after.** Sustained work therefore runs far below the benchmark, \
and the ten percent Starvation floor is reachable inside one exchange by anyone \
who forgets it.

""" + AU_TABLE + """

The ladder gives typical rates, not limits. A practitioner's own output is \
Flux Density × η, and a sheet that sits off the ladder is a practitioner who \
built differently. The same bands rolled up by Tier of Standing are in Part \
Twenty-Three.

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
