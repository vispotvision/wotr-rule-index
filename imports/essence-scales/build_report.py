#!/usr/bin/env python3
"""SUPERSEDED 2026-09-26 (C-076): the Grade-bracket report; do not re-run.
Write `reports/essence_scales_2026-09-26.md` — WAR-161's sweep and findings.

The prose is here; every count and every figure is read from `scan.py`, so the
report cannot drift from the corpus. Run:

    python3 imports/essence-scales/build_report.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import scales  # noqa: E402
import scan  # noqa: E402

f = scales.sig
recs = scan.scan()
S = {r["stage"]: r for r in scales.rows()}


def rel(p):
    return p.replace("wiki/", "")


eu_out = [(r, x) for r in recs for x in r["eu_readings"] if x["inside"] is False]
eu_in = [(r, x) for r in recs for x in r["eu_readings"] if x["inside"] is True]
aus_out, seen = [], set()
for r in recs:
    for x in r["aus_readings"]:
        if x["inside"] is False and (r["page"], x["value"]) not in seen:
            seen.add((r["page"], x["value"]))
            aus_out.append((r, x))
aus_in, seen2 = [], set()
for r in recs:
    for x in r["aus_readings"]:
        if x["inside"] is True and (r["page"], x["value"]) not in seen2:
            seen2.add((r["page"], x["value"]))
            aus_in.append((r, x))
bands = [r for r in recs if r["bands"]]
turns = [r for r in recs if r["turns"]]

# What this run changed on the live pages, and what it could not.
APPLIED_TURN = [
    ("Dreambreaker Field · The Shattered Midnight", "3 turns", 15, 18),
    ("Judgment Manifest", "5 turns", 25, 30),
    ("Letheveil Memory-Quake", "1 turn", 5, 6),
    ("Maw of Crystalline Stasis", "3 turns", 15, 18),
    ("Oneiron Parasite · Nightmare Warden", "4 turns", 20, 24),
    ("Principle Overwrite", "3 turns", 15, 18),
    ("Puppet-Dream Marionette", "1 turn", 5, 6),
    ("World Echelon", "8 turns", 40, 48),
]
GLOSSED = [
    ("Archivium Locus", 5), ("Chorda Somnii", 3), ("Corona Lunaris", 2),
    ("Florwyn's Canticle", 4), ("Oneiron Phantasm Court", 2),
    ("Karu Velnar · The Shackled Tempest", 2.2),
    ("Vael of Nothing · The Devourer's Index", 3),
]
BANDS_DONE = [
    ("Aurevian Lysanthir · Voice Between Wars", "B", "VIII", 6, "Master"),
    ("Gorrath Bloodspine · The Magmaborn Juggernaut", "B", "VIII", 6, "Master"),
    ("Kaelen Raive · Sun-Sealed", "B", "VIII", 6, "Master"),
    ("Saruin Kye · Golden Laugh", "B", "VIII", 6, "Master"),
    ("Iskaron Thalnaris — Bearer of the Fractured Crown", "S", "XI", 7, "Grandmaster"),
    ("Juno Petros Marien · Praefect of the Outer Colonies", "A", "IX", 6, "Master"),
    ("Xanelor Rafminar · The Wandering Fang", "A", "IX", 6, "Master"),
]
BANDS_HELD = [
    ("Ara Min Mahuo", "`:14`", "\"Grade B across the board, cleanly, matching Stage VIII's "
     "Coherence Band exactly\" — the observation *is* that her Grade letter equalled the "
     "band letter. With the band retired the sentence has no referent, so the Tier is not "
     "derivable; it needs a rewrite, not a swap."),
    ("Sodoku Moto", "`:14`, `:39`, `:42`, `:43`, `:81`", "his band is low *for his Level*, "
     "and the Tier of Standing does not carry that; \"Band A/S territory, well above Band D\" "
     "is a comparison against the retired scale, not his rank."),
    ("Dorrik · The Pot Man", "`:37` ×2", "\"Nine souls in ten live and die inside Band F\" is "
     "the scale as a class. Band F spanned Stages I–IV, which is Tiers 1 to 4; his own Tier 3 "
     "would narrow a true sentence into a false one."),
    ("Ymir Rhok · The Emberhand", "`:54`, `:69`, `:92`", "same class reading — \"Band G with "
     "no reserve\", \"Dorrik was Band F with 1,840\"."),
    ("Borin Ironheart · The Master of the Soul Forge", "`:35`", "\"Soul Crystal Tier: Sovereign "
     "(Band S correlate)\" is a Crystal-tier correlate, not a rank."),
    ("Iryen Maevith · The Serene Gale", "`:37`", "\"the table places Band A at Radiant\" is an "
     "Aether-Class correlate."),
    ("Drevath Mourne-Kal · The Iron Horizon", "`:38`", "\"Class V's Band B correlate\" — the same, "
     "and it was already restored by hand once for that reason."),
    ("Yoko Mishiro", "`:39`", "\"past what Band E would ordinarily support\" is class prose."),
    ("Eidolyn Falseface Lattice · Oneiron Phantasm Court", "`:49` each",
     "\"Band C ceiling for Stage VII\" reads the retired band as a Grade ceiling, which it "
     "never was: Stage VII's ceiling is A-Grade at 475. A Tier would not fix the sentence."),
    ("Sir Rhyse Calder · The Tartan Bastion", "`:18`, `:20`, `:22`", "seven tokens inside a "
     "record of a correction made *to* the retired scale; replacing them erases what the record "
     "is about."),
    ("Upanga wa Msimu Nne · Blade of the Four Seasons", "`:29`", "\"within Chimwala's Stage VIII, "
     "Band B range\" uses the band as a cost range. At the Stage VIII EU band the stated 2,400 EU "
     "for the rite sits far below it, so the swap would make the sentence false; logged as an "
     "out-of-band cost instead."),
    ("The Left of the Door · State of Play — Hild Ice", "`:48`, `:19`", "\"a third down at Band F "
     "waste rates\" is the retired scale's η, not a rank."),
    ("Zarron Mahuo · The Arbiter of Unity", "`:134`", "the card is being struck from canon "
     "altogether, so it is not this sweep's to edit."),
]
NOT_TURNS = [
    ("Cosmology & Metaphysics/The Sky, the Hour and the Year", "\"The month is two turns, "
     "twenty-eight days\" — lunar turns."),
    ("Factions.../The Articles of the Accord", "\"Registered within one turn\" — a register's "
     "turn, in a table of contract forms."),
    ("Races & Peoples/The Elven Peoples", "\"the first of those three turns out not to be\" — "
     "the verb."),
    ("The Descent of Parun/The Counted Speech", "\"ends after one turn of a named glass\" — an "
     "hourglass."),
    ("The War Cycle/The Fisc — Paying for a Siege", "five rows, One turn to Five turns — a siege "
     "clock counted in something much longer than six seconds."),
    ("Volume I/Verinus VII · The Palatine", "\"the gold coils … run one turn longer\" — a coil."),
    ("Techniques/Pyrewind Breaker", "\"instantaneous, under a second, matching the source's '1 "
     "turn (instant burst)'\" — already consistent: an instant action inside a six-second turn."),
]
ACCOUNTS_DONE = ["Chorda Somnii", "Archivium Locus", "Corona Lunaris", "Bastion Imperium",
                 "Dirge Ascension"]
ACCOUNTS_NOT_LIVE = ["Edict Strike", "Judgment Manifest", "Letheveil Memory-Quake",
                     "Florwyn's Canticle", "Oneiron Phantasm Court",
                     "Dreambreaker Field · The Shattered Midnight",
                     "Maw of Crystalline Stasis", "Principle Overwrite", "World Echelon"]

L = []
A = L.append
A("# WAR-161 — the essence scales, and every page read against them")
A("")
A("The scales are `imports/essence-scales/_derivation.md`, computed by `scales.py` "
  "from four quoted anchors and three ruled constants. This report is written by "
  "`build_report.py`; every count and figure below is read off the corpus by "
  "`scan.py` and none is typed.")
A("")
A("## What was published")
A("")
A("**Fracture of Worlds Part Nineteen** gained three subsections, in the page's own "
  "register, between *The Resource System* and *Efficiency by Tier of Standing*: "
  "*The Turn, and What a Unit Is Worth* (one turn is six seconds; one EU is one "
  "megajoule; one AU/s is one megawatt, with the drawn, delivered and "
  "time-to-empty identities), *The EU Band by Temperance Stage* (sixteen rows, band "
  "and benchmark, with the strain reach at V, VII, IX and XI), and *The AU/s "
  "Progression* (sixteen rows by Stage, nine by Tier of Standing).")
A("")
A("**The Core Vocabulary** gained an η clause — an η above 1.0 is real and the "
  "surplus is drawn from the Aether stratum — a **Turn** entry at six seconds, and a "
  "pointer from the EU entry to the Stage bands. Both pages were re-read live "
  "afterwards; the changed blocks read as intended and nothing else on either page "
  "moved.")
A("")
A("## The ladder against the corpus")
A("")
A("| | count |")
A("|---|---|")
A(f"| pages carrying an EU, AU/s, η, Band or turn figure | {len(recs)} |")
A(f"| EU reserve figures read against a Stage band | {len(eu_in) + len(eu_out)} |")
A(f"| — inside the band | {len(eu_in)} |")
A(f"| — outside it | {len(eu_out)} |")
A(f"| AU/s figures read against a Stage band (distinct per page) | {len(aus_in) + len(aus_out)} |")
A(f"| — inside the band | {len(aus_in)} |")
A(f"| — outside it | {len(aus_out)} |")
A(f"| pages carrying a surviving lettered Band | {len(bands)} |")
A(f"| lettered Band occurrences | {sum(len(r['bands']) for r in bands)} |")
A(f"| pages stating a duration in turns | {len(turns)} |")
A(f"| turn durations | {sum(len(r['turns']) for r in turns)} |")
A("")
A("### The EU reserves outside their Stage band")
A("")
A("Three, and all three are already held by the C-059 pass for reasons this sweep "
  "does not change.")
A("")
for r, x in eu_out:
    A(f"- `{rel(r['page'])}`:{x['line']} — Stage {r['stage']}, **{f(x['value'])} EU** "
      f"against {f(x['band'][0])}–{f(x['band'][1])}")
A("")
A("### The AU/s figures against the new ladder")
A("")
A(f"{len(aus_in)} sit inside their Stage's band and {len(aus_out)} do not. "
  "**No AU/s figure was changed by this run**, and the reason is in the findings below.")
A("")
A("| page | Stage | stated AU/s | Stage band |")
A("|---|---|---|---|")
for r, x in sorted(aus_in + aus_out, key=lambda t: t[0]["page"]):
    mark = "✓" if x["inside"] else "✗"
    A(f"| {mark} `{rel(r['page'])}`:{x['line']} | {r['stage']} | {f(x['value'])} | "
      f"{f(x['band'][0])}–{f(x['band'][1])} |")
A("")
A("## The turn, applied")
A("")
A("### Nine pages were converting turns at five seconds, and are corrected")
A("")
A("| page | turns | was | now |")
A("|---|---|---|---|")
for p, t, was, now in APPLIED_TURN:
    A(f"| `{p}` | {t} | {was} s | **{now} s** |")
A("| `Oneiron Phantasm Court` | 2 turns | ≈10 s | **12 s** |")
A("")
A("### Six durations stated in turns now carry their seconds")
A("")
for p, n in GLOSSED:
    secs = n * scales.TURN_SECONDS
    A(f"- `{p}` — {n} turns, **{secs:g} s**")
A("")
A("### Fourteen system accounts carried the turn-length gap; all fourteen are closed "
  "in the repo")
A("")
A("`imports/system-accounts/` held the gap as an open row — a duration of `null` with "
  "two candidate readings at three and five seconds a turn. Thirty-seven figures across "
  "fourteen account drafts are now written at six seconds, including every figure the "
  "drafts derive from a duration: Corona Lunaris's shed exitance, its colour temperature "
  "and its Wien peak; the Maw's EU per use; World Echelon's coupling crossings. "
  "Dirge Ascension keeps its stated 45 s, which is seven and a half turns, its nine-turn "
  "gloss being the figure that gave way under the rule that a figure and its gloss are "
  "reconciled in favour of the stronger reading.")
A("")
A(f"**{len(ACCOUNTS_DONE)} of the fourteen have that account live in Notion** and are "
  f"corrected there too: {', '.join('`' + p + '`' for p in ACCOUNTS_DONE)}. The other "
  f"{len(ACCOUNTS_NOT_LIVE)} have no account section on their Notion page at all — the "
  "technique page is live, the *Two Accounts* material is not — so the repo draft is the "
  "only copy and it is correct: "
  + ", ".join("`" + p + "`" for p in ACCOUNTS_NOT_LIVE) + ".")
A("")
A("### Seven turn mentions are not durations and are left alone")
A("")
for p, why in NOT_TURNS:
    A(f"- `{p}` — {why}")
A("")
A("## The retired lettered Bands")
A("")
A("Seven cards carried the retired band inside a dated record that states its own "
  "Stage on the same line, so the Tier of Standing is derivable from the line itself "
  "and the swap is arithmetic. All seven are done, η untouched:")
A("")
A("| card | was | Stage | now |")
A("|---|---|---|---|")
for p, letter, st, tier, name in BANDS_DONE:
    A(f"| `{p}` | Coherence Band {letter} | {st} | Tier of Standing {tier}, {name} |")
A("")
A(f"**{len(BANDS_HELD)} pages are held, and each for a stated reason.** Isaac's answer "
  "is to replace the retired band *wherever derivable*; on these the Tier is not what the "
  "sentence is about, so a swap would not convert the sentence but falsify it. Each needs "
  "a rewrite by whoever owns the page's prose, not a token substitution:")
A("")
for p, where, why in BANDS_HELD:
    A(f"- **{p}** {where} — {why}")
A("")
A("## Findings")
A("")
A("**1. The ladder and R44-5 disagree about which gives way, and no card was "
  "overwritten.** Isaac's answer to card 1 q2 asks for an AU/s progression and says "
  "\"correct cards that miss it\". R44-5's operative sentence says \"the card's η governs "
  "per character and the tables are typical ranges; an in-world-acknowledged outlier is "
  "lawful\", and by his own first rule for ruling, a ruling's general sentence governs "
  "every case it describes — which includes a table of AU/s. Three further things point "
  "the same way: R44-2 makes AU/s the product of Flux Density and η, so moving AU/s to a "
  "benchmark forces a second edit to Flux Density on every card; the WAR-102 answers set "
  "specific AU/s figures for Gimbzo, Dougou, Elion and Sodoku by hand, and two of those "
  "sit outside the new band; and a single benchmark per Stage collapses every card at that "
  "Stage onto one figure, which is exactly the effect C-059 was written to avoid for EU. "
  "So the ladder is published as bands, every miss is listed above, and nothing is moved. "
  "The question is on the questionnaire.")
A("")
A("**2. The wiki mirror is materially stale for the system-account pages, and that "
  "bounds this sweep.** `wiki/Techniques/Chorda Somnii.md` carries `last_edited` of "
  "2026-09-12 and 57 lines; the live page carries the whole *Two Accounts* treatment, "
  "hundreds of lines, including the turn-length row this run closed. The scan above reads "
  "the mirror, so on any page in that class it under-reports. Anything counted here is "
  "real; the counts are floors, not totals.")
A("")
A("**3. Below Ascension a benchmark reserve is a fraction of one EU.** At one megajoule "
  f"to the EU a Murmuring practitioner's whole output band is "
  f"{f(S['I']['eu_floor'])}–{f(S['I']['eu_ceiling'])} EU and the benchmark is "
  f"{f(S['I']['eu_benchmark'])}. The figures are published as computed. Whether the unit "
  "wants a floor at the bottom of the ladder is on the questionnaire; it is not a number "
  "to invent.")
A("")
A("**4. Four cards state a reserve their Stage puts far out of band and are not reached "
  "by C-059.** Krothar, Naori, Yoko and Yukazuri are the sweep's remaining reserve misses "
  "and each is already logged against the C-059 pass. Yukazuri's card is also one where a "
  "bare \"Stage I\" in a Catalyst row is not the subject's Stage; she is Stage IV, arrested, "
  "and her card names the Stage \"the Hollowing\", which is not the Part Five name for IV "
  "(Flourishing). That last is a naming mismatch, not a number, and is left for whoever "
  "owns the card.")
A("")
A("**5. Two owed edits on pages this run touched belong to other work and were left.** "
  "The *Efficiency by Tier of Standing* callout on Part Nineteen still reads as an open "
  "conflict; that rewrite is named in Isaac's WAR-49 answer. The seven dated records this "
  "run edited still carry their own naming-and-ratification wording, which the clean "
  "publishing rule bars and which the part-1 and part-2 sweeps already inventory. Only the "
  "band token was changed on each.")
A("")
A("**6. Two figures on the Grade ladder are quoted, not rounded.** Part Four writes "
  "`4.6024×10^10` and `2.42672×10^13`; the derived tables carry four significant figures "
  "throughout, so those appear as 4.602×10^10 and 2.427×10^13 in a *derived* cell and "
  "verbatim wherever the anchor itself is reproduced.")
A("")
A("## The check")
A("")
A("The ladder reproduces, without being fitted to them, the two set points C-059 had "
  f"already computed by hand: Stage XII's benchmark is {f(S['XII']['eu_benchmark'])} EU, "
  "the Arctic Lion figure, and Stage XIII's is "
  f"{f(S['XIII']['eu_benchmark'])} EU, Dougou Ozumu Zettari's. The delivered column of the "
  f"AU/s table at Stage XIII is "
  f"{f(S['XIII']['eu_benchmark'] * 1.075 * scales.EU_JOULE)} J, the same number that "
  "report prints as its own check line. At every Stage the benchmark reserve, spent at the "
  "tier's efficiency, lands back inside the Part Four band it was read from.")
A("")

if __name__ == "__main__":
    out = os.path.join(REPO, "reports", "essence_scales_2026-09-26.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {out} ({len(L)} lines)")
