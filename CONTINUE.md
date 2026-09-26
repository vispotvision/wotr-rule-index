# CONTINUE — how to pick this work up cold

Read this first in any new session (scheduled or not). Isaac's standing
direction: inside work he has asked for, make the calls; no "pending" slots.
`ROADMAP.md` is the plan; this file is the live state. Newest block first;
append a dated block, do not rewrite older ones (two sessions write this repo
at once — `git pull` before editing, and commit only your own files).

## State on 2026-09-25 (WAR-46 — WAR-70 applied: 4 EU figures corrected in Notion, 124 held)

WAR-70 (`RULINGS.md`, 2026-09-25) says what an EU figure outside its Stage's band becomes: **the
band's midpoint in decades**, the geometric mean of the Part Four floor and ceiling in joules, divided
by 1 MJ. Every one of the 128 misses is now computed, with the Part Four row it comes from quoted
beside it, in `reports/eu_band_corrections_2026-09-25.md` (generator
`imports/essence-ledger/eu_band_corrections.py`; the script asserts each band against the Part Four
row before it writes a line, so a citation cannot drift from the arithmetic).

- **Four are corrected on the live Notion pages**, one statement each, EU field only: Ara Min Mahuo's
  reserve ~4,200,000 → ~10,080,000; Brynja Haldrís 11,000 → 438,800 EU; Vael of Nothing 2,600,000 →
  10,080,000 EU; Vaelthor Ashen-Meridian 620,000 → 132,300,000 EU. All four verified live afterwards.
- **124 are held**, every one with its set point computed and the reason logged. The big one is
  **`CONFLICTS.md` C-059**: WAR-70's set point is one figure *per band*, and a card's Stage fixes one
  band for every EU figure on it, so on 99 of the misses two or more figures a card states as
  *different* numbers become one number — Dougou Ozumu Zettari's thirteen figures, 2,800 EU to
  92,000 EU, all become 2.278 × 10¹⁹ EU, reserve and cheapest strike alike. **C-060** is the other new
  row: Part Four says Stage XIV is not assessed by attack output, and the chain hands it an EX band
  anyway (one figure, Aurelian Prudentius). Filed to Doc Kett as **WAR-127** (C-059) and **WAR-128**
  (C-060) — parentless, because the board refuses a child of WAR-46 assigned to the agent who filed it.
- Also held, with the arithmetic: 14 self-declared estimates and ranges, 5 figures a card attributes
  to a source by name ("workbook figure", "carry from the legacy sheet" — the wording WAR-48 held four
  cards for), 2 stated fractions of another figure, and 1 set point that lands on a decimal (147.9 EU,
  Naori Yukari), the reason WAR-48 held four cards under R44-2.

**The four edits are in Notion, not in git.** `wiki/` is the mirror and still stale (WAR-29 / WAR-68),
so a grep of `wiki/` returns the old figures until the hourly sync commits.

## State on 2026-09-25 (The Master Codex is in the index)

- **The canon Codex is the 2026-09-24 edition** (`$WOTR_TRUE_CANON/The Master Codex.xlsx`; older copies in
  `true-canon/.superseded/`). It adds Alchemical Index rows 42-61 and, from this session, "Weapon Coating" on the
  Lists AlchType column. The "For ChatGPT" and "For Gemini" bundles are in the system trash; the one file only
  they held is now `true-canon/THE MECHANISM OF THE SIXTY.docx`.
- **`build/codex.py`** (MCP `codex`, `codex_check`) reads the xlsx: `find` for Pack Eighteen 4a, `check` for
  checks 37-39. It flags "Cymorath" in six archived scenes and "Oblatio" in one; the scenes are untouched.
- **The Notion Alchemical Index has the twenty new formulas** (sixty-one rows), drafted from the Codex in
  `imports/alchemy/`. Rows 44, 45, 48, 53 read **Class ?** until **C-058** is ruled; C-055 to C-057 are open
  beside it. Rows 47 and 60 are written Vohrin · Caloria under R27-1 although the Codex still says Crymorath.

## State on 2026-09-25 (WAR-48 — sixteen AU/s figures corrected in Notion under R44-2)

R44-2 (`RULINGS.md`, 2026-09-25, logged by WAR-96) rules that **AU/s = Flux Density x eta** governs and
that a card's stated AU/s is the error. Of the twenty-six cards that miss:

- **Sixteen are corrected on the live Notion pages** (nineteen statements; Mizuki, Muken and Niran
  each state the figure twice and both statements moved together). Only the AU/s field was touched —
  Flux Density and eta stand as written on every card, per R44-2's own scope.
- **Ten are held and not corrected**, all on **WAR-102** (Doc Kett, `canon` + `needs-ruling`):
  Gimbzo (`CONFLICTS.md` **C-053**) and Dougou Ozumu Zettari (**C-054**) because the recomputed figure
  contradicts figures their own cards state elsewhere; Elion Drevas, Ignatius, Borin Ironheart and
  Sodoku Moto because the ruling does not say what their wording becomes; and Artemis, Ayame,
  Vethraun and Yukazuri because the exact product lands on a decimal in a field that has never held
  one, and rounding would invent a number.

**The edits are in Notion, not in git.** `wiki/` is the mirror and it is still stale (WAR-29 /
WAR-68), so a grep of `wiki/` returns the *old* AU/s figures until the hourly sync commits again.
The card-by-card working, with every figure computed from `imports/essence-ledger/fit.json` by script
and none typed, is `reports/au_s_recompute_2026-09-25.md`.

## State on 2026-09-25 (WAR-113 — `wiki/` is stale in git; do not trust an absence found by grep)

**Until the sync commits again, `wiki/` in git is 2026-09-24 17:15 (`c79211a`).**
Notion is 290 files ahead, including the character-lore pass: **5** files in git
carry `Lore · The Life Behind the Card`, **276** carry it in the main checkout's
working tree. Hild Ice's card has `circlet` twice on the live page and zero times
in the committed mirror — which is how WAR-106 came to be filed on an absence that
was not one.

**Before filing any finding whose content is "the card does not say X":**

```bash
git log -1 --format='%ad  %s' --date=iso -- wiki/    # when the sync last committed
grep -m1 last_edited "wiki/<the file>"               # what Notion time that file carries
```

A last `Wiki sync:` commit older than the page's `last_edited` means the absence is
the mirror's, not canon's. `wiki/` is a cache that carries no staleness signal.

**Why, in one line:** the 2026-09-24 18:00 sync exported all 284 changed pages to
disk, was killed by the unit's 30-minute timeout before its commit, and
`wiki/.manifest.json` had already advanced — so every later export correctly says
`0 to export` and no run will ever redo the work. Then nineteen consecutive runs
died at `sync.sh:114-118`, a conflict-marker guard that aborts on `RULINGS.md`, a
file the sync's own path list (`sync.sh:123`) never stages or commits.

Full evidence, with both of WAR-113's suggested causes refuted:
`reports/wiki_mirror_staleness_2026-09-25.md`. The repair is **WAR-29** and
**WAR-68** (Marsha Law); nothing was fixed from here, because every repair is in
`build/*.sh` / `build/*.py` or is a commit of `wiki/`.
## State on 2026-09-25 (WAR-71 — the two defects WAR-46 found in the fit are fixed)

**Both were in the extractor, neither was a card.** WAR-46's sweep logged two
things it could not act on, and WAR-71 fixed them at source in
`imports/essence-ledger/`, rebuilt `anchors.json` and `fit.json`, and regenerated
`reports/eu_band_sweep_2026-09-25.md` from the corrected fit. **No card figure
moved, the constant did not move, and no conflict was resolved.**

**One: a gated table row is read against its own Stage.** `extract_anchors.py`
now carries the Stage a table row states for itself wherever the table gates its
rows one by one (`row_gate` → `anchors.json`'s `stage_on_the_line` → `fit.py`'s
`stage_basis`). The test is mechanical and deliberately narrow: the column has to
be named `Gate` / `Stage` / `Temperance`, and the cell has to be a Stage
statement **and nothing else**. That is what keeps it off Sinclair Mercer's
`Gate` column (Wellspring gates — "Fate VIII") and off Tier Grade, Bands & the
Aether Shell's `Temperance cluster`, which the page itself says binds nothing. A
range cell is read at its low end, the Stage the row opens at, and `stage_high`
keeps the other end. Four figures in the corpus carry one, all four the Rusashin
Forms; the Nadi Forms table has the same shape and its costs are `EU/s` rates the
sweep refuses by design, so nothing there to read.

**Two: Part Nineteen's Tier 5 η is R44-4's.** The ruling corrects that cell to
0.60–0.70 and the Notion edit it names has not come back through the hourly sync,
so the mirror still writes 0.50–0.60. `build_anchors.py` now substitutes the
ruling's figures in one named place (`ETA_TIER_RULINGS`), quoting R44-4 verbatim
and keeping the mirror's row untouched in `verbatim`; the pre-ruling numbers stay
beside them as `*_as_the_mirror_writes_it`, and `fit.json`'s `eta_from` names the
ruling by id on the 16 rows that read there.

**What the numbers did.** In band at 1 EU = 1 MJ: 25 of 155 → **27 of 155**. Best
single constant still 6.2×10⁶ J/EU, in band 65 → **67**. Misses 130 → **128**
(Rusashin Form II at 4,000 EU lands in B-Grade; `Spellcraft/Vainglory.md:28` at
75,000 EU lands in A-Grade at the ruled η). Readings *above* band 6 → **2**, and
both survivors are reserves. The `GATE` reason is gone from the sweep with the
defect it recorded; the other three Rusashin Forms flip to below band and are
logged `NO-TARGET`, which is why `NO-TARGET` went 65 → 68. The Stage III mean
residual went +0.98 → +1.21 because only Naori Yukari is left there.

**What was deliberately not rebuilt.** `ledger_tables.json` and the draft Part
(`the-essence-ledger.md`). Rerunning `ledger_tables.py` against the corrected fit
moves Naiser Yukari's fallback η from 0.55 to 0.65 in four places, and the Part is
written on top of those tables — the two move together or not at all, and that is
WAR-12's work. Filed as a follow-up, not done here.

## State on 2026-09-25 (WAR-96 — R44-1..R44-6 are now in RULINGS.md)

**The record exists.** Six `RULINGS.md` entries, one per row, logged with
`log_ruling`: `## 2026-09-25 — R44-1-EU_JOULE_ONE_MEGAJOULE` through
`## 2026-09-25 — R44-6-BARE_BAND_V_IS_LEVEL_BAND`. Each row's `verbatim` is an
exact substring of its own entry — checked mechanically, all six True — so the
one thing `validate.py` deliberately does not check is now checkable by grep.
**WAR-46 and WAR-48 are unblocked**: R44-1 and R44-2 exist as rulings.

**What each entry carries, and why it is two layers.** Isaac answered the WAR-11
`ask_user_questions` card by *selecting options* — a, a, c, a, a, a on
interaction `364556db-a75a-4e23-ab6a-cc9541ecdbcb`, resolved 17:59:14Z,
`human_only` — and typed no prose. So each entry records the chosen option in
the exact words the card put to him (label and description, block-quoted) and
then the one-sentence form the index row quotes, said to be that. Nobody reading
the entry can mistake the sentence for words Isaac typed, and nothing was
paraphrased into existence that is not shown beside its source. No ruling's
content moved: the constant is 1 EU = 1 MJ, and R44-3's scope is still the
attack-output column only.

**Pointers named precisely, not just "the 2026-09-25 entry".** That phrase was
already ambiguous — RULINGS.md's other 2026-09-25 section is Isaac's seven
precedence-ladder answers on WAR-61. Fixed in two files: the header comment of
`rules/doc-essence-ledger-rulings-2026-09-25.yaml` and line 8 of
`reports/essence_ledger_rulings_2026-09-25.md`.
`imports/essence-ledger/the-essence-ledger.md` was **not** touched: its
references read "the 2026-09-25 entry" / "the 2026-09-25 entries" and are true
now that the entries exist, and it is WAR-12's draft, not this issue's file.

**One real defect found in the tooling, filed as its own issue.** `log_ruling`
resolves its repo from `mcp_server.py`'s own location (`common.ROOT`), so run
from a worktree it appends to *that worktree's* `RULINGS.md`, commits it onto the
worktree branch — the thing `CLAUDE.md` forbids — and then pushes the local
`master` ref, which in a worktree is the main checkout's branch and was 39
commits behind. All six calls returned `push failed: Updates were rejected
because a pushed branch tip is behind its remote counterpart`. That is exactly
how `3215399` became "the unpushed hand-edit of `RULINGS.md`" and vanished on
the next rebase. Here the commits were pushed by hand with
`git push origin HEAD:master` in the same run, so nothing sits unpushed.

**The push carried three commits that are not this issue's**, unavoidably: git
ancestry puts `43b3272` (WAR-22, mine), `90fd356` (WAR-46), `0785443` (WAR-72)
and `067b901` (WAR-48) under the six ruling commits on this shared branch. All
four were finished, committed, reviewed work that WAR-46 and WAR-48 deliberately
withheld *because R44 had no record*; landing the record without them would have
left the branch in the same knot. Named here so their own issues can see it.

`python build/validate.py` PASS. No card, source, wiki, table, `sources/` or
config file changed; `CONFLICTS.md` untouched.

## State on 2026-09-25 (WAR-48 — the 26 AU/s figures recomputed, none applied)

**All twenty-six are recomputed and no card moved.**
`reports/au_s_recompute_2026-09-25.md` is the run: every figure computed from
`imports/essence-ledger/fit.json` `formula_check`, none typed, with each card's
Flux Density, η, stated AU/s, the product, the multiple, and a verdict. Twenty
are arithmetically settled and ready; six are stopped and recorded.

**Nothing was applied because R44-2 does not exist yet, verified two ways.** Its
verbatim is in no `RULINGS.md` — not on this branch, not on `origin/master` —
and the one file it is written in,
`rules/doc-essence-ledger-rulings-2026-09-25.yaml`, is **not on master either**:
`git ls-tree origin/master rules/` has 43 files and none is it. It arrived in
`f335403`, unpushed on this branch. `CLAUDE.md`: *"A ruling exists only if it is
in `RULINGS.md`."* That is **WAR-96**, filed out of WAR-72 to Doc Kett, still
`todo`, and WAR-48 is blocked on it. Nothing about R44-2's *content* is in
question — the issue quotes Isaac's WAR-11 answer — only its record, and
`RULINGS.md` is written through `log_ruling` alone, which is WAR-96's call and
not this issue's task. The moves are too large to ship on an unrecorded ruling:
eight cards move more than 1.89 decades, Gimbzo's by 7.89.

**Six cards need a ruling, not a sweep, and they are the run's real product.**
Two contradict a figure their own card states elsewhere: **Gimbzo** (three
technique costs at 3.2 × 10¹²–1.1 × 10¹⁴ EU that the recomputed 8.648 × 10⁶ AU/s
turns from 4.8–164 ms into 4.3–147 days, i.e. every named Work unusable), and
**Dougou Ozumu Zettari** (`:38` states 3,900 AU/s **external** with internal
cycling immeasurable, so Flux Density × η is a different quantity, not a
correction of that figure). Four are stopped on form, which the ruling does not
reach: **Elion Drevas** (the card's η is the range ~0.72–0.78, so the product is
a range where the field is one figure; `fit.json`'s 0.75 is the extractor's
midpoint, not the card's), **Ignatius** (the figure lives in the card's own
`## X · Open Rulings` section as a record that the legacy sheet's numbers are
unconfirmed — rewriting it would falsify the record), **Borin Ironheart** (all
three fields say `(est.)`, and WAR-46 held a self-declared estimate is not a
figure these rulings name), **Sodoku Moto** (`~3,800 base`, and the product 772.8
is neither approximate nor a base).

**Two further findings.** Four of the twenty land on a decimal (Artemis 1,663.2,
Ayame 438.6, Vethraun 282.1, Yukazuri 258.1) where no AU/s field in the corpus
holds one; the exact product invents nothing but rounding would, so it is the
same question as the backlog's *"what a card figure corrected under R44-1
becomes"*. And **four cards state the AU/s twice** (Mizuki `:30`/`:59`, Muken
`:34`/`:60`, Niran `:28`/`:61`, Yukazuri `:40`/`:61`), so the sweep is thirty
statements across twenty-six cards — twenty-four of them on the ready twenty.
All twenty-six cards are under `wiki/`, the Notion mirror, so the application is
Notion page edits with the mirror returning through the hourly sync, the way
C-030..C-033 went in; that sync is itself blocked right now.

**Not pushed, deliberately, and for the same reason as WAR-46's commit.** This
branch carries three commits that are not mine (`f335403`, `0d60241`,
`7904f76`); `git push origin HEAD:master` would ship them to get one report out,
and `f335403` is the very file WAR-96 is about — putting the R44 index rows on
master while `RULINGS.md` still lacks the entry would deepen the defect rather
than close it. `validate.py` PASS, 697 rules, live=572 superseded=125. No card,
source, rule, `RULINGS.md`, wiki, table or config file changed.

## State on 2026-09-25 (WAR-72 — the Part's rebuild was already on master; audited)

**Read this before the WAR-46 block below, which is stale on one point.** That
block, and the WAR-72 issue filed out of it, both say the draft Part
Twenty-Three still works at 1 EU = 1 kJ and "owes itself a rebuild". It does
not. The rebuild landed on master as `1271ff9`, *"Essence Ledger P2 rebuilt at
the ruled constant, 1 EU = 1 MJ (WAR-12)"*, at 15:14 — thirty-one minutes after
WAR-46's commit was written at 14:43, and WAR-46's commit has been sitting
unpushed on the WAR-22 branch since. WAR-46 read the Part at `e59835f` and was
right at the time; master moved under it. Nothing was wrong with either run.

**WAR-72 therefore changed no figure, and this block is its whole product.**
What it did instead was audit `1271ff9` against its own finish line, because a
commit message is not evidence. All of it holds:

- **The constant lives in one place and the chain is clean at 1 MJ.**
  `ledger_tables.py:642` is `K = 1e6`; `fit.py:67` is `K_TEST = 1e6` and always
  was, so 1e3 only ever lived in `ledger_tables.py`. Re-running
  `ledger_tables.py` reproduces `ledger_tables.json` byte-identically, so the
  committed JSON is the committed script's output and not a stale artifact.
- **The prose follows the JSON, not just the headline.** Spot-checked the nine-
  rung spine (§3), the drain and waste-heat set (§5.3, §6.4) and the Starvation
  floors (§7) row by row against `ledger_tables.json`: every figure matches.
  The arithmetic blocks hand-check too — Dougou's 7,400 EU × 1e6 = 7.40 GJ,
  Kwon Mu-jin's 42.5–127.5 M EU = 42.5–127.5 TJ, Yukazuri Moto's 52.8 MW at
  4,793 K and 18.3 m. The *arguments* were rebuilt with the numbers, not only
  the numbers: §3's bottom-rung note now reads 0.015 EU (it was 15 EU at 1 kJ),
  which is the kind of line a find-and-replace rebuild leaves behind and this
  one did not.
- **§2 records the residuals and reopens nothing**, which is what WAR-72 asked
  for and what `CLAUDE.md` requires. §2.2 states R44-1 as governing, quoted.
  §2.3 carries canon's three self-pricing lines missing the ruled constant by
  **+2.447 to +2.982 decades**, all three the same direction, with the 1 kJ and
  least-squares columns kept beside them as residual rather than argument. §2.4
  carries all four of `physics-check.md`'s brackets, each failed, each in the
  note's own words, with R44-1's own `notes` field quoted to show the ruling was
  made in that knowledge. Nothing is softened and nothing is reconciled.
- **The C-034 PENDING note is out.** The two PENDING blocks left in the Part
  (`:941`, `:1332`) are the AU-identity question and the two recovery
  populations — neither is C-034, and R44-1 settles the constant only. The
  Paragon row's PENDING cells are absent data (`gate_level: null` in the JSON),
  not an unanswered ruling. Tier 7 and Tier 8 printing the same ceiling
  (6.70 × 10⁹ EU) is real and derived — both gate on Level 500, the highest gate
  the ruled anchors reach — not a copy error.

`python build/validate.py` PASS, 697 rules, live=572 superseded=125.

**The audit did turn up one real thing, and it is not about the figures —
it is about the record. Filed as WAR-96 to Doc Kett, `canon`.** R44-1 is not in
`RULINGS.md`. `rules/doc-essence-ledger-rulings-2026-09-25.yaml` says in its own
header *"The record is the 2026-09-25 entry in RULINGS.md; each verbatim quotes
it"*, and all six rows carry `source.file: ''`, the standalone pattern that
`AGENTS.md` says `validate.py` deliberately does not check — "those quotes rest
on your care alone." Grepping `RULINGS.md` for `essence ledger`, `C-034`..`C-037`
or `One constant` returns nothing, on this branch or on `origin/master`.
RULINGS.md's 2026-09-25 section is a different ruling: Isaac's seven
precedence-ladder answers on WAR-61, which mention R44-3 and R44-5 as examples
as though they were already recorded but carry none of the four C-row closures.

That matters because `CLAUDE.md` says a ruling exists only if it is in
`RULINGS.md`, and the Part's §2.2 — **on master** — prints R44-1's text as a
block quote attributed to *"`RULINGS.md`, the 2026-09-25 entry"* and marks it
**[ruled]**. The likely cause is the same split that made WAR-72 look necessary:
the Part's rebuild is on master, the R44 index rows (`48e09d6`) are not, and the
`3215399` hand-edit of `RULINGS.md` that the WAR-46 block below says was
deliberately withheld is no longer in this branch's ancestry after the rebase.
WAR-72 did not touch `RULINGS.md` and did not call `log_ruling`: that file is
written only through the tool, never by hand or from a worktree, and logging the
batch is not what this issue asked for. Nothing about the six rulings' *content*
is in question.

**So WAR-13 and WAR-14 are no longer waiting on this.** WAR-72 named both as
affected and told them to wait for the rebuild rather than the draft; the
rebuild is what is on master now, so the nine-rung spine WAR-13 hangs its
ladders on is the 1 MJ spine in §3, including R44-3's 24.3–41.8 TJ carve-out,
which §3 states deliberately because six of those ladders need it. Neither
issue was touched here. What still blocks WAR-46's card corrections is
unchanged and is not this: the ruling that says what a corrected figure
becomes, with Doc Kett.

## State on 2026-09-25 (WAR-46 — R44-1's card sweep, swept and not applied)

R44-1 settles 1 EU = 1 MJ and names the card figures that then miss their
Stage's band as the error. WAR-46 read all of them and **changed no card
figure.** `reports/eu_band_sweep_2026-09-25.md` is the sweep: 130 of the 155
attested EU figures that have a band miss it — 124 below, 6 above, across 51
files and 50 entities — and every one of the 130 is logged with the reason
nothing was set. 48 sit on the twelve cards C-040 names, where the
Stage-to-Grade chain that *makes* the band is contested, so the issue's own
instruction is to stop; 11 are lines that call themselves estimates, which
R44-1 does not name; 4 are Rusashin Forms whose own Gate cell states a Stage
the fit did not read; 2 are stated fractions of another figure. The remaining
65 are plain card figures that miss, and the reason they stand is the one that
covers all 130: **the ruling names the error and states no corrected value.**
"Inside the band" is a range 0.76 to 8.75 decades wide (median 1.96), nothing
on any card names a point in it, and house rule 3.3 forbids inventing one.

Two findings for whoever owns the fit, neither a card correction:
`build_anchors.py` reads a Discipline page's entry Stage onto every Form in its
cost table (Rusashin's four), and R44-4 has moved the η fifteen lines use —
Part Nineteen Tier 5 is now 0.60–0.70, so the fit's delivered joules are 18%
low on those lines and one row (`Spellcraft/Vainglory.md:28`) changes status.

**What this needs is one more ruling:** what a corrected figure becomes. Under
the 2026-09-25 CLAUDE.md direction that nothing waits on Isaac, that is the
docket's to make, so it is filed to Doc Kett rather than parked. The report
puts three shapes that would each be enough and recommends none. Until one is
ruled, R44-1 is applied as far as it reaches — the constant stands, the misses
are counted, every card stands as written. The AU/s sweep R44-2 hands on
(twenty-six cards, `fit.json` `formula_check`) is a separate issue and
untouched here; unlike this one it has a formula and may well be executable.

**Two notes for the Ledger's own files.** The draft Part Twenty-Three works at
1 EU = 1 kJ and says at its C-034 note that it "inherits whichever way Isaac
rules"; R44-1 ruled 1 MJ, so the Part owes itself a rebuild at the ruled
constant — WAR-12's, filed separately, not touched here. And `build_anchors.py`
reads a Discipline page's entry Stage onto every Form in its cost table
(Rusashin's four), while R44-4 has moved the η fifteen lines use to the Tier 5
range 0.60–0.70, leaving the fit's delivered joules 18% low on those lines.

**Not pushed to master, deliberately.** This commit sits on the WAR-22 branch
behind `3215399`, the unpushed hand-edit of `RULINGS.md` that carries R44-1
itself. Master has neither, and the 2026-09-25 CLAUDE.md says `RULINGS.md` is
written only through `log_ruling` and "never edited by hand or committed from a
worktree", so this run did not ship someone else's commit to get its own out.
The report cites R44-1; it lands on master when R44-1 does.

## State on 2026-09-24 (the agents)

The first full day of the Paperclip team working the repo. Fifteen commits
landed on master under the agents' git identity, between 17:19 and 19:36;
everything earlier in the day under Isaac's name is the book dispatcher, the
lore publish, the hourly wiki sync and the nightly, not this team.

**What shipped.** The Magic System rulings for the day went in first: `16eb7d8`
closed C-030..C-033 as R43-1..4, `10709bf` applied the Coherence Band sweep
across the repo and Notion, and `a71c2f0` was the check pass — 36 pages re-read
straight from Notion, every surviving lettered Band a deliberate leave, all
thirty recorded in `reports/coherence_band_sweep_2026-09-24.md` (WAR-2, done).
Doc Kett then filed C-038 in `CONFLICTS.md` (`db2d9f7`, WAR-16, done): Part
Four's travel-speed column leaves Mach 4 to Mach 5 in no Grade, the same break
repeats in metres per second at `TG&B:58`/`:59`, and Anryū Ichimonji's Ink Gate
transit at Mach 4.8 already lands in the gap. Nothing resolved.

Phenna Menon shipped the first twenty-eight system accounts — Isaac's ask for a
metaphysical, physical and mechanism account in real essence units for every
working — as `9b9ee99`, then applied both addenda in four batches, `d56dde8`,
`a98213a`, `8146db0` and `cd3bc6a`, and filed the questionnaire as `686ed30`:
`imports/system-accounts/_conflicts.jsonl`, 104 rows, 104 unique ids. All 28
carry the five sections with a credited lens and a Counterplay lookup trail,
section 3 is "Mechanism (the effect)" and no account holds a separate effect
description anywhere. Thirteen of the rows are `effect-mechanism` — a page's
stated Effect and its Mechanism describing different workings, Celestial
Harmonic Shear and Dirge Ascension the sharpest — and eight are `fairness`
(WAR-4, done).

The Essence Ledger took the rest of the evening. Etta Band collected every
attested EU, AU/s and η figure in the corpus and fitted the EU-to-joule
constant (`77b298b`), Rhett Konn's review pass added the measured side
(`5891b28`, with `a9f90b7` restoring C-038, which that commit had dropped), and
he approved on round two after checking all 692 anchor rows and 1,066 quoted
lines back to file:line with zero mismatches and no card figure changed
(WAR-9, done). He left one defect standing rather than holding the phase: the
2% band-edge filter matched across measure columns. Etta fixed it the same
evening in `5a0c848` — a figure is now matched only against the ladder for the
measure its own line states, and only against rows of a table, which moved Karo
Venrik's Strike Force and Corona Lunaris's superseded 100 GJ from band citation
to attested (WAR-17, done).

Phenna Menon closed the day with the real-physics check, `9505f80`,
`imports/essence-ledger/physics-check.md`, 848 lines. The verdict is no: 1 EU =
1 MJ does not hold and the failure is structural. At the low end Yukazuri Moto's
Nerve Reading would put 15.4 MJ of waste heat into a body whose whole budget to
a lethal core temperature is 1.225 MJ; requiring only that spending a reserve
not cook the practitioner caps the constant at 3,592 J/EU, which is the top of
the measured band to three figures — two methods that never look at each other
landing on the same number. At the high end the brief's own figure was out by a
factor of a thousand, and corrected it is worse: the largest reserve in canon
cannot pay for one attack at its own Grade's minimum. Two cards break E = mc²
outright. No constant was adopted and no canon figure moved (WAR-10, in review
with Rhett Konn).

**What is blocked, and on whom.** WAR-5, the second twenty-eight Techniques, is
in progress with Phenna Menon and is the live piece of the system-accounts job;
WAR-6 (the twenty Spellcraft pages, Phenna) and WAR-7 (Rhett's review of the
accounts against the system and each other) are queued behind it, and the
parent WAR-3 waits on all three. On the Ledger side WAR-12 (the FoW Part, Etta)
is held by the physics check now in review, WAR-13 (the nine-name ladders,
Etta) by WAR-12, and WAR-14 (publish to wiki and Notion, Cody Wix) by WAR-13;
the parent WAR-8 waits on the lot. WAR-15 — three Yukari cards plus Gimbzo and
Vethraun naming Temperance Stages Fracture of Worlds does not — is in the
backlog with Doc Kett and needs no ruling: Pack Twenty's
`R20C-30-STAGE_NAMES_FROM_FOW` already settles it, the work is applying it.

**What waits on Isaac.** One issue, WAR-11, `blocked-on-isaac` with Doc Kett:
the Essence Ledger questionnaire. On it sit the η conflict (Aether Class I at
0.60–0.70 against Tier of Standing 5 at 0.50–0.60), the card-figure
disagreements Phase 1 surfaced, the stale Coherence Band references the nine
Tiers of Standing replaced, and C-034 through C-040 — six rows after the
rewrite, plus C-038. C-036 and C-038 are the same shape, a Tier Grade column
whose row-pair does not meet, and C-036 now stands in three tables, so a ruling
that closes it has to name all three or the other two keep the old edges.
Whether C-036 and C-038 take one ruling or two is his call and the rows say so.
Nothing else in the repo is waiting on him.

**One environment fault, flagged twice today and still open.** The `wotr` MCP
server will not start: its interpreter under `/tmp/paperclip-ai-…/.venvs/wotr/`
no longer exists, so `load_rules`, `fow_line` and `verify_scene` are
unavailable to every agent, and `build/validate.py` will not run in the default
shell for the same reason (`pyyaml missing`). Phenna worked around it with a
throwaway venv in her run scratch dir and touched nothing in the repo to do it.
If validation is failing for anyone else on this machine, that missing venv is
why. Rebuilding it is Isaac's.

**Tomorrow's first moves.** Rhett Konn reviews WAR-10; the physics check is the
hinge for the whole Ledger, and Phases 2, 3 and 4 unblock in order behind it.
Phenna Menon carries WAR-5 to the end and goes straight into WAR-6. Doc Kett
takes WAR-15, which needs nobody, and keeps WAR-11 ready so the questionnaire
can be answered in one sitting whenever Isaac sits down to it. Someone rebuilds
the `wotr` venv before the first prose run of the day, because nothing written
can be verified without it.

## State on 2026-09-24 (fair play, the challenge, and the system accounts)

**Isaac's standing direction, now in the skills:** use everything WOTR holds
with full metaphysics and essence units; meta knowledge informs the writer,
never a character's omniscience; every ability fair (cost, limits, a
Counterplay route, a tell, in band) and every counter findable by a player
who looks things up; philosophy and historical pseudoscience as lenses, never
mechanics. Text: `.claude/skills/wotr-write/references/fair-play.md`, pointed
to from wotr-write, technique-design, character-sheet, wotr-phenomenon,
wotr-npc, wotr-rp, and in the Paperclip house rules (`WOTR.md`, pushed to
every agent's AGENTS.md). The claude.ai account copies of the skills do not
have it yet. **Paperclip WAR-3..7:** the system accounts for the 56 Techniques
+ 20 Spellcraft pages (physical, stratal, mechanism, essence ledger,
counterplay + lookup trail) into `imports/system-accounts/`, conflicts into
`_conflicts.jsonl`, then Doc Kett's questionnaire; Notion only after rulings.

## State on 2026-09-24 (writing skills in Claude Code)

**The seven claude.ai WOTR skills now live in the repo, adapted for Code.**
`.claude/skills/wotr-write` (+ references: scene-pipeline, technique-design,
character-sheet, prose-law-quickcheck, tools), `wotr-rp`, `wotr-npc`,
`wotr-phenomenon`, `wotr-wound`, `wotr-stat-line`, `wotr-ledger`. Same craft
content as the account skills; what changed: `mcp__wotr__*` names with
`build/book_tools.py` / `build/verify.py` fallbacks, drafts go to
`/tmp/wotr-drafts/`, sources are the `wiki/` mirror (the Stat Sheet workbook
is not in the repo: "workbook, unchecked"), and every writer
(`archive_scene`, `ledger_add`, `npc_set`, ...) is a proposal made on Isaac's
word, per AGENTS.md. The claude.ai account copies are unchanged and still
serve Desktop chat; a craft change should land in both. `~/wotr-natalie`
picks these up on its next pull.

## State on 2026-09-24 (character lore, written and published)

**Published later the same day:** Isaac ran `lore_publish.py --apply` himself;
all 276 sections are on their Notion card pages (checked on three: one
section each, last on the page). `imports/lore/_published.json` holds the
hashes, so a re-run only sends changed files. "The Web of Lives" hub page
was not made (its stage was skipped). The hourly sync mirrors the sections
into wiki/, after which `lore_roster.py` reports has_lore for each card.

**Every card has a Lore section on disk.** Isaac asked
for a character manager that makes the connections and gives every character
a backstory in Notion. `.claude/workflows/character-lore.js` (args `{date,
cards?, rewrite?}`) built the roster (`build/lore_roster.py` →
`imports/lore/_roster.json`), 41 clusters (`_clusters.json`), one shared
history per cluster (`clusters/`), the cross-cluster ties (`WEAVE.md`), and
276 sections "Lore · The Life Behind the Card" (`imports/lore/cards/`, all
verify.py PASS when written; Sodoku Moto's is a record compiled from the
card and archive, nothing new). `LAW.md` and `WORLD.md` are the brief the
writers read; `UNCARDED.md` registers archive characters with no card
(Charles, Kujo, Wren, Ilthára ...). **On Isaac's word the run stopped after
writing:** the canon and craft checks, revisions, tie reconciliation (ties
may be one-sided), the hub page "The Web of Lives" and the audit were
skipped, and he chose to hold publishing. To publish: `bash build/py.sh
build/lore_publish.py` (dry run; 276 would go) then `--apply` on his word;
it appends the section to each card page and replaces it on a re-run. The
skipped stages can be run later by resuming the workflow on the same files.

## State on 2026-09-23 (the Magic System pass)

**Tiers 8/9 renamed and every open Magic System conflict ruled.** Tiers of
Standing 8 and 9 are Archmaster and Paragon; the retired lettered Coherence
Bands are gone from the Magic System pages (Stages read by Tier of Standing).
A cross-check fixed ~14 mechanical errors in Notion (units, speeds, stale
Sub-Stat names, tier slips); the Reader's Codex is current (Kagura Branch,
four Crafts, Level/Bands/Tiers). Isaac's questionnaire closed C-020..C-029
(R42-1..11) plus four follow-ups (R42-12..15), all applied in Notion
including ~75 cards (Dominion Stability → Gravity; Stage I–V cards
Unclassed). The Elven racial trait "Domain Stability" is NOT the Sub-Stat
and keeps its name. **Open:** Ryuka's Crystal field ("Dormant network,
awakening surface"); Kinjiki's η ~1.3 and Absolute Crystal at Stage XIV;
the Color of Essence Revelation cell has a pasted Part Five inside it;
lettered "Coherence Band" still on Technique pages and some cards outside
the Magic System.

## State on 2026-09-18 (the Instructions box)

**`desktop/PROJECT_INSTRUCTIONS.md` rewritten as an order of operations.** The
text in the Claude Desktop project's Instructions box was the pre-MCP version
(before `13171cc`): it named GitHub and Notion and nothing else. The repo copy
now says, in order: WOTR MCP first when present (local `wotr` in Claude
Desktop, all 45 tools; the public read-only connector, 25 tools, from
claude.ai web/phone) with the per-chat sequence (`session_start` → `load_rules`
+ `check_docket` before any prose → `scene_brief`/`scene_context`/`fow_line`
before drafting → `verify_scene` after, twice → the writers at the close, full
server only); then what each GitHub file is for and what lives in the repo but
not in knowledge (`sources/`, `desktop/inventories/`, `scenes/`, `table/`);
then Notion; then the never-skipped list. Header says which files go in
Knowledge. **Waits on Isaac's hands:** paste the text below the rule into the
project's Instructions box and re-sync Knowledge. NATALIE.md unchanged.

**Later the same day, the design inverted.** Isaac: Natalie still writes
without the rules. Cause: project Knowledge is retrieved in chunks, the box is
the only text always in context, and the box held a pointer. The box text now
carries the law itself (turn shape, length bands, the banned constructions,
numbers from `fow_line` only, the four voices, `verify_scene` before posting),
and `build/instructions_box.sh` builds the full paste (the box text plus
NATALIE.md below its first rule, 35 KB) at `~/wotr-instructions-box.md` and
puts it on the clipboard. If the box rejects the length, the box text alone
is the fallback. Still Isaac's hands: the paste, and confirming the `wotr`
tools show in the project chat at all.

**Evening: the enforced surface.** Isaac: "so fix it." The Desktop log
showed the server connected and answering (122 live prose-law rules) and
zero tool calls in the chat that drifted, so the model was simply not
calling. Built the one surface where it cannot skip: `build/natalie_hook.py`
+ `.claude/settings.json` (SessionStart injects NATALIE.md and the prose-law
brief; Stop verifies every reply over 120 words and blocks on FAIL, one
enforced revision per reply), gated on a `.natalie` marker so the coding
checkout is untouched. The clone `~/wotr-natalie` carries the marker; Isaac
opens it in the app's Code tab and that session is the table. Checked with
fake transcripts: no marker → silent; bad reply → block with the FAIL list;
clean reply → silent; `stop_hook_active` → silent. Not yet seen: a real
session in the Code tab (first open will ask to approve the project's
`wotr` MCP server from `.mcp.json`).

**Later: the manual verification.** Isaac asked what happened to it. The
2026-09-12 edition of the guide was in `~/wotr-vault/true-canon` only; the
scripts it names (`wotr_verify.sh` v4, `wotr_beat_check.py`, `wotr_terms.txt`,
`codex_check.py`) are on no disk here and never were in the repo. The guide
is now copied verbatim to `desktop/WOTR_Manual_Verification_Guide (2026-09-12 edition).md`
(vault copy stays the original), listed for project Knowledge, named in the
Instructions box and NATALIE.md with the honest coverage line (verify_scene =
checks 1-8, 10-13, 15-19, 22-23; the rest by reading), and injected by the
Code-tab SessionStart hook. Offered, not done: adding checks 28 and 42 as
FAILs and 9, 14, 41 as WARNs to `build/verify.py`.

## State on 2026-09-15 (Cowork)

**Claude Cowork has its instructions.** `desktop/COWORK.md` is the file: what
Cowork is on this machine (Claude Code run by Claude Desktop, with the app's
connectors and the `WOTR MCP`), where the work is, that it is not Natalie, the
connector rules (read freely; write canon on Isaac's word only and through the
MCP writers; private pages stay private; Drive/Trello/Gmail lines), the lines
that hold everywhere, and that `CLAUDE.md`/`AGENTS.md` are never rewritten as
folder instructions. `~/Claude` (Cowork's default folder, `coworkUserFilesPath`)
now exists with `CLAUDE.md` as a symlink to it; opened on the repo, Cowork reads
the repo's `CLAUDE.md` → `AGENTS.md` (new layout line and a "Claude Cowork"
bullet) → `COWORK.md`. Unverified until Isaac opens a Cowork session: whether
the repo's `.claude/skills` load there, and whether Cowork's own "update folder
instructions" writes through the symlink or replaces it (harmless either way).

## State on 2026-09-14 (midday: ComfyUI and the local TTS, on the card)

**Isaac asked for ComfyUI and the local TTS on Linux; both stand.** The one
unknown behind everything — a ROCm torch that sees the 9070 XT from a 3.12
venv — is settled: AMD's index (`stable.repo.amd.com/rocm/whl-next/`) serves
the exact Linux wheels the setup scripts pin (`torch 2.13.0+rocm10.0.0`,
cp312, `[device-gfx1201]`), and no `render`/`video` group was needed (Arch
ships `/dev/kfd` and `renderD*` mode 666; ROCm 7.2.4 came with
`ollama-rocm`). The card is `cuda:0`, the 7800X3D's iGPU is `cuda:1`.

**ComfyUI** (new on Linux; the Windows installs lost everything but their
metadata, kept in `~/wotr-vault/comfy`): `build/comfy_setup.sh` — clone at
`~/comfy/ComfyUI` (0.35.0), venv `wotr-comfy`, requirements with torch held,
the ten Windows workflows into the UI's list, and `wotr-comfy.service` on
127.0.0.1:8188 with `--cuda-device 0` (without it comfy-aimdo planned against
the iGPU's 31 GB). `--models` fetched what the workflows load and is free:
Z-Image Turbo bf16 + Qwen3-4B encoder + VAE, RealESRGAN x4, BiRefNet (20 GB,
in `models/`, no repo). First render: `text_to_image.json` as posted to
`/prompt`, 1024², 8 steps, 19.6 s cold. Not fetched: FLUX.2 dev (non-
commercial licence), Ideogram 4, Wan 2.2 (the video workflow) — add to
`comfy_models()` in the script if wanted.

**The engines**: every venv rebuilt by its own script as written (three
headers rewritten from UNTESTED to what happened): `wotr-supertonic` answers;
`wotr-cb-gpu` loads Turbo on `cuda:0`; `wotr-qwen` + `wotr-qwen-fast` both see
the card and the fast worker captures HIP graphs; `wotr-cosy` needed one fix
— `setuptools<81` for `pkg_resources` (now in `cosyvoice_setup.sh`) — and
loads Fun-CosyVoice3-0.5B on the card. Kokoro's files re-fetched
(`--fetch-model`), `requirements-audio.txt` installed into the project venv,
the CC-BY reference clips copied back from the vault to `build/voices/refs/`.
Kokoro read scene 02's cast (3 voices, 16.9 min) in 278 s on the CPU.

**One Gimbzo line, three engines, measured** (Whisper read-back clean on all
three; the anchor `line3_deep` is 63.2 Hz median / 57.3 floor): Chatterbox
Turbo on the VCTK clip 131 Hz; Qwen VoiceDesign from the brief 84.7 Hz,
cosine 0.37 to the anchor (anchor self-similarity 0.55), and the best-of-3
draw repeated half the line; CosyVoice cloning the anchor itself 71.6 Hz /
60.0 floor. One line each, not the gate — the freeze stands. Note for the
`cosy_worker`: it chdirs into the clone, so `ref` must be an absolute path.

**Docs**: AGENTS.md (unit row, a "GPU venvs" bullet, the freeze line says
the engines are installed), README (unit count, the engine paragraph, a
ComfyUI paragraph), ROADMAP Phase E (venvs ticked, ComfyUI added),
`systemd_setup.sh` (copies `wotr-comfy.service`, restarts it on change,
does not enable it — `comfy_setup.sh` does). `validate.py` PASS.

## State on 2026-09-14 (later that morning)

**Done since the port block below.** Isaac joined the docker group; n8n is up
from `n8n/docker-compose.yml` (container `n8n`, host networking — proven from
inside it: `wget http://127.0.0.1:8799/health` answers), and `WOTR nightly` is
imported (the CLI import needs an `id` field added to the JSON; the UI import
does not). The journal was purged, so the stray token line is gone everywhere.
The sync ran clean end to end with the new Notion secret at 06:24 (its one
standing note: `scenes/YOKO_MISHIRO.md` cannot be published until its Notion
parent is shared with the `oridon` integration). Headless Claude was proven
from a unit (`systemd-run --user`, 1.6 s, no MCP servers loaded — the
`--strict-mcp-config` flags do their job). The DNS wedge after `tailscale up`
(every lookup hung) was `systemd-resolved`; `sudo systemctl restart
systemd-resolved` cleared it.

**AGENTS.md.** New at the root: the working map for every coding agent (Codex,
OpenCode, Cursor, Copilot, Gemini, Claude Code) — layout, the Linux setup, the
commands, the prose protocol with the table's Docket in it, what the robots
commit, what never leaves the machine. `CLAUDE.md` points at it and is
otherwise unchanged. `build/book_tools.py` run bare now prints its tool list.
Checked by three agents (facts vs the tree, consistency vs the instruction
files, a fresh agent trying four tasks) and rewritten once on their findings.

**Still Isaac's, in n8n's UI** (`localhost:5678`): the owner account, the
`WOTR jobs` Header Auth credential (value: `build/.jobs_token`) on the three
HTTP nodes, the Discord webhook in "Send it to Isaac"; if the workflow is
activated, `systemctl --user disable --now wotr-nightly.timer`. Still owed
from the list below: Tailscale's `ultron` rename + operator flag (then the
public URL), Claude Desktop's `install_mcp.sh` with the app closed, Ollama,
rclone, the render/video groups.

## State on 2026-09-14 (the Linux port)

**The machine.** Windows was wiped overnight for Omarchy (Arch Linux, Hyprland,
systemd 261); the box is still `Ultron`, the user is `oridon`, the repo is
`~/wotr-rule-index`, and everything that lived outside it on Windows is in
`~/wotr-vault` (private repo: `true-canon/` is the old `WOTR True Canon` folder,
`claude/memory/` the old memory, `omarchy/CHECKLIST.md` the plan this session
carried out). Isaac's checklist step 11 was the brief: scripts to shell, tasks to
timers, `C:\` and `G:\` to config.

**What replaced what.** One interpreter, `~/.venvs/wotr/bin/python` (3.14; was
the Store 3.13). One config file, `~/.config/wotr/env` (mode 600; template
`build/wotr.env.example`; fill it with `bash build/secrets.sh`, never by pasting
into a chat) holding the three secrets and the paths — read by `build/env.sh`
(every shell script sources it), `common.load_env()` (every tool; the `winreg`
lookups are gone) and the units (`EnvironmentFile=`). Thirteen `.ps1` files
became `.sh` (same names, same logs, same commit messages, same exit codes) and
the five Windows tasks became systemd *user* units in `build/systemd/`,
installed by `build/systemd_setup.sh`: `wotr-sync.timer` (hourly, now with an
flock so a manual `sync_now` and the timer cannot overlap), `wotr-nightly.timer`
(03:30), `wotr-book.timer` (02:00), `wotr-backup.timer` (Sun 03:00), and the
daemons `wotr-jobs` (127.0.0.1:8799), `wotr-mcp-public` (8765), `wotr-bot`.
Linger is on, so they run without a desktop login. Logs: `journalctl --user -u
wotr-<name>` plus the scripts' own files. `bash build/setup_linux.sh` rebuilds
all of it on a fresh machine. The MCP reaches Claude Code through `.mcp.json`
(project-scoped; approve it once) and Claude Desktop through
`build/install_mcp.sh` (run with the app closed). n8n's compose is
`n8n/docker-compose.yml`, host networking, so it reaches the job runner at
`127.0.0.1:8799`. The TTS venvs are `~/.venvs/wotr-<engine>` and their five
`.sh` setups are untested ports (the narration freeze stands). Backups land in
`~/wotr-backups` until Drive is mounted (rclone; `WOTR_DRIVE`).

**Proven live on 09-14.** The nightly fired as a unit at 03:30 (the timer is
`Persistent=true` and caught up the slot the moment it was installed): checks,
headless Claude note, commit, push — `cfccaa5`. The bot is online
(`WOTR Bot#7139`) and came back on its own after a reboot; the job runner
answers `/health` and ran `book_dry` through n8n's route; the public MCP
answers on 8765 behind its new secret; the first sync with the new Notion
secret read 586 pages, all unchanged, and built the semantic index (11,092
chunks, 9 min once); the first backup zip is 23.7 MB with True Canon inside.
The port went through a 172-agent workflow: seven porters, a static battery, a
live integration run, five skeptics, two refuters per finding, per-unit fixes,
a re-check, a docs sweep (76 findings, 8 refuted, the rest fixed or handed to
this note).

**The secrets.** None were copied off Windows; all three were reissued tonight
(Discord reset, Notion refreshed; ElevenLabs still empty). Two pastes landed in
the chat and one at the shell prompt — the chat ones were reset again, the
shell one left a stray line in the env file that systemd echoed into the
journal 26 times; the line is gone, the journal purge and an optional third
Discord reset are on Isaac's list below.

**Not yet on Linux.** Tailscale is up but this node is `ultron-1` (the dead
Windows node holds `ultron`) and Funnel needs the operator flag — so the
public URL is not published; Docker's group is not joined, so n8n is not
running; Ollama and rclone are not installed; Claude Desktop has no `WOTR MCP`
entry yet. Each is one sudo line, listed under "Owed by Isaac".

## Owed by Isaac (do not decide these) — added 2026-09-14
- `sudo journalctl --rotate && sudo journalctl --vacuum-time=1s` (the stray
  token line in the journal); a third Discord token reset afterwards is
  optional (`bash build/secrets.sh DISCORD_TOKEN`).
- Tailscale: delete the offline Windows node `ultron` in the admin console,
  then `sudo tailscale set --hostname=ultron --operator=oridon`; then
  `bash build/mcp_public_setup.sh` publishes the MCP and prints the URL; put it
  in `WOTR_MCP_PUBLIC_URL` and restart `wotr-mcp-public`.
- Docker: `sudo usermod -aG docker oridon && sudo systemctl enable --now docker`,
  log out and in, then `cd n8n && docker compose up -d`; in n8n paste
  `build/.jobs_token` as the `WOTR jobs` Header Auth credential and import
  `n8n/WOTR_nightly.json`. If that workflow is activated, `systemctl --user
  disable --now wotr-nightly.timer` so nothing runs twice.
- Claude Desktop: quit it, `bash build/install_mcp.sh`, reopen.
- Ollama: `sudo pacman -S ollama-rocm && sudo systemctl enable --now ollama`.
- Drive, if wanted: rclone (`rclone config`, a remote `gdrive`, a mount), then
  `WOTR_DRIVE=` in the env file.
- The GPU engines, when the freeze lifts: `sudo usermod -aG render,video oridon`.
- Everything the 09-13 list below still owes (the Four Crafts items, Darius's
  card, the 43 Judger proposals, chapter 1's gate — `python build/book_next.py
  --approve 1` or `--reject 1 --note "..."`).

## State on 2026-09-13 (night)

**Rules and canon.** validate.py PASS. Docket empty; open conflicts: none
(C-008..C-019 ruled; RULINGS.md 2026-09-13). Pack Twenty extracted
(`rules/pack-20-twenty.yaml`); R20C-24/26/27 superseded on arrival by the
09-12 rulings. R38-2 re-cost applied to the seven sheets with a stated pool
(`build/recost.py`, `reports/recost_2026-09-13_applied.md`). Editions written
today in WOTR True Canon: Combat Craft Guide, Complete Magic System, Mechanism
of the Sixty, Character Template — the Combat guide's next pass owes a note at
the three superseded R20C rows. Six base guides still unfolded (ROADMAP).

**The table and the MCP.** `wiki` and `scene_recall` search by meaning
(`build/embed_index.py`, rebuilt by the sync). `scene_context(draft)` is the
lorebook (`build/lorebook.py`; `build/aliases.yaml` maps Darius → Ignatius's
card — the card should carry the name; Wren, Vaeloris, Ashgate, Cass Holloway
have no page). The Judger's assistant: `/judger <slug>` drafts the close as
proposals in `bot/queue/<slug>.judger.md|json`; `/judger apply <slug> P01 …`
runs only the ids Isaac names. First note written for
`08_sodoku_recalescence` (43 proposals, none applied — Isaac's call).

**The sync and backups.** `WOTR wiki sync` commits and pushes again (the dead
`.git/worktrees/agent-*` entries and ErrorActionPreference=Stop were the
cause; fixed 09-13). Private pages (Notion's "Information not on WIKI" tree,
114 pages) are stamped `private` in `wiki/.manifest.json` and never reach the
Drive shelf; the three documents that had reached it are removed. `WOTR
weekly backup` (Sunday 03:00, `build/backup.py`) now zips the WOTR True Canon
folder too — the one store that is in no git repository. `vault/` is the
Obsidian view (`build/vault_export.py`, hourly) — point Obsidian there.

**The bot** (`bot/`, PLAN.md): F0 lookups, `/scene save`, `/event`, `/verify`,
`/date`, the sheet checker, `/narrate` — 16 commands; the logon task "WOTR
bot" is registered and running. Thread reading and the auto-check wait on the
Message Content intent (Discord developer portal), then
`bot/config.yaml: intents.message_content: true`. Next for the bot: post
`bot/queue/*.judger.json` proposals in `#judger` as approve/set-aside cards
(contract in PLAN.md §9.3). `ELEVENLABS_API_KEY` unset; `/narrate elevenlabs`
cannot run until it is.

**Narration.** Frozen behind one gate (ROADMAP, "Where it stands"): Qwen is
locked behind `--qwen` (drift); nothing new on the voice roadmap until one
engine holds Gimbzo across three renders. CosyVoice is in flight in another
session (`build/cosy_worker.py`, uncommitted).

**The nightly.** `WOTR nightly` (03:30) runs `build/nightly.ps1`; the digest is
`reports/nightly.md`, shown by `session_start` while fresh. Its Claude step
waits on `claude /login` (the CLI is not signed in; Isaac's hands).

**n8n.** Running in Docker (compose at `C:\Users\isaac\Documents\n8n`, port
5678), with Ollama on the host at 11434 and the MCP's HTTP mode on 8765. It
cannot call Claude (no key) and cannot run anything on this machine (Linux
container, no repo mount), so the split is: n8n orchestrates,
`build/jobs_server.py` (logon task `WOTR jobs`, 127.0.0.1:8799) executes
named jobs, Claude Code thinks. `n8n/README.md` has the wiring;
`n8n/WOTR_nightly.json` is the first workflow, ready to import. The shared
secret is `build/.jobs_token` (gitignored, never in chat). **If a workflow is
activated, disable the matching Windows task so nothing runs twice.**

**The book.** `.claude/workflows/book-chapter.js` writes chapters in Claude
Code; the design is `book/design/BOOK_PIPELINE.md` (moved from `n8n/`; its
n8n transport needs an API key that does not exist - do not build toward it).
The dispatcher `WOTR book` (02:00, `build/book_dispatch.ps1`) writes one
chapter a night unattended: `build/book_next.py` decides, headless Claude
Code runs the workflow, the chapter lands under `book/` and is committed.
Gates are chapters 1-3, then every fifth, and the last. **Chapter 1 is
written and waiting: `python build/book_next.py --approve 1` or `--reject 1
--note "..."` - until Isaac answers, the dispatcher writes nothing.**
Two PowerShell traps learned here, and they bind any future script: a .ps1
must be saved UTF-8 **with BOM** or PowerShell 5.1 reads an em dash's third
byte as a smart quote and the file stops parsing; and a prompt must be piped
to `claude -p` on **stdin**, never passed as an argument, or PowerShell
strips its quotes. `Start-Job` also hung after its child exited - both
scripts call `claude` directly and let the task's ExecutionTimeLimit be the
timeout.

**Ideas.** `reports/ideas_2026-09-13.md`: 102 ideas, 66 survived the
skeptics, seven "Do next", the cut list. Done from it today: I03 (True Canon
in the backup), I06 (n8n moved), I08 (audit reports undated; heavy audits off
the public route), I09 (this file), I10 (private pages off the shelf), I12
(the narration freeze). Not done, with reasons: I01/I02 are the sync
session's; deleting `build/.venv-chatterbox` and `chatterbox_setup.ps1` waits
on Isaac. Still on the list: I93+I99 (sweep debt line in `session_start`),
I96 (`natalie_lint`), I13 (constraints as hooks), I23 (`inventory_add`), I54
(loudness master).

**Imports.** Trello conversion: all 200 converted; 196 published to Notion;
four Tovain stubs held by design (`reports/publish_imports_held.md`).

## Owed by Isaac (do not decide these)
- Three of the four Four Crafts items (R9-1): Law III's rewrite, the
  golden-age question, the Latinate/vernacular doublet's scope — the source
  document's Part Four docket text is needed before real options can be put.
- Darius's card: a "Called · Darius" line on Ignatius's card in Notion (or a
  card of his own) — until then `build/aliases.yaml` bridges it.
- The 43 proposals in `bot/queue/08_sodoku_recalescence.judger.md`.
- Whether to delete the CPU Chatterbox venv and its setup script (superseded
  by the GPU one; rebuildable).
- A Zettari forge-culture substrate pitch (Docket 18) is owed FROM Claude,
  not Isaac: he asked for a proposal drafted, mirroring the Dawi's Cask-Oath
  Pitch. Not yet written.

## History, folded
- 2026-09-12: inventories for six cultures landed (`desktop/inventories/`);
  the reader's codex drafted; the Trello conversion workflow ran to 200 with
  its review stage cut at Isaac's word; `build/publish_imports.py` written;
  eleven base guides folded into dated editions; narration built (four
  engines, cast files, the public audio route); the "Information not on WIKI"
  page was re-shared with the integration on 09-13 and the mirror is current.

## Every session ends with
`python build/validate.py` (must PASS) → `python build/resolve.py` → commit →
push → tick ROADMAP.md → append a dated block above.

## State on 2026-09-24 (the last four Magic System items, ruled and applied)

**C-030 to C-033 are closed and the edits are in Notion.** Isaac answered the
WAR-2 questionnaire on 2026-09-24, one ruling per item; `RULINGS.md` carries the
entry, `CONFLICTS.md` the four rows with the evidence, and
`rules/doc-magic-system-rulings-2026-09-24.yaml` rows R43-1..4 the index.

- **C-030.** Ryuka Yukari's Crystal State is `null`, his Crystal Tier is Awakened
  Crystal, and "Dormant network, awakening surface" is off the card. Applied to the
  Notion card and to `imports/converted/characters/the_little_wayfinder.md`.
- **C-031.** Kinjiki's η reads "~1.2, the Archmaster ceiling"; Absolute Crystal
  stays, the pairing Class Ω carries (FoW VII:36).
- **C-032.** The Color of Essence's XV · Revelation cell reads whole again, and the
  block that had been pasted inside it stands as "Part Five · Prose Application"
  after Part Four — the same words, a proper Family / Write it as table.
- **C-033.** The lettered Coherence Band is gone from the cards, the Technique pages
  and the Arctic Lion sheet: **215 Notion pages, 399 occurrences** by script plus
  **28 blocks by hand** (the field-label form, and four cards whose token is split by
  emphasis). 30 occurrences were left as written, all of them *about* the retired
  scale rather than carrying it — its own η ranges, Class and Crystal correlates,
  the dated 2026-09-12 ratification records, and Dorrik's "He is Band F" framing.
  Every one is listed in `reports/coherence_band_sweep_2026-09-24.md`.

The Notion edits return through the hourly sync; the mirror in this worktree was
deliberately not committed. **Open, and small:** Limina has no Part Five line (seven
of eight Families are written, and nothing in the repo supplies the eighth);
Dabney Corvalen Olyss' η is still "pending Isaac"; Aurelian Prudentius' line now
names the Tier twice and wants a reword; the ~115 repo files under `imports/`,
`book/` and `scenes/The_Path_of_Sorrow.md` still carry the lettered Band, which was
outside the sweep's stated scope — `The_Path_of_Sorrow.md` has it in narrative prose,
which is a different decision from a field swap.

## State on 2026-09-25 (the Essence Ledger's Part, and the constant)

**WAR-12, Phase 2 of the Essence Ledger, is drafted and pushed
(`imports/essence-ledger/the-essence-ledger.md`).** It is the draft FoW **Part
Twenty-Three, "The Essence Ledger"** — nothing published to the wiki or Notion,
which is Phase 4 (WAR-14). Every claim in it carries a `[canon]`, `[derived]`
or `[draft]` marker, every quoted fragment was checked against the line it
cites, and every slot a ruling must fill is marked **PENDING** with the
question written so Isaac can answer it in a sentence. `validate.py` PASS.

**The constant is 1 EU = 1 kJ, 1 AU/s = 1 kW — three decades below the brief,
and Isaac's brief authorised exactly that** ("If 1 MJ fits badly, pick the
constant that fits best and say why"). 1 MJ misses canon's only three
self-pricing lines by 2.4 to 3.0 decades, puts Draen Varos's nine-kilogram
Forge-Heart at 7.5 times its own rest-mass energy, and cooks every practitioner
in their own waste heat inside a second. 1 kJ is inside two of the three
measured windows, 0.034 decades outside the third, inside all four physical
brackets `physics-check.md` §6 lists, and **the only power of ten that is.** At
it Dougou Ozumu Zettari's sheet closes end to end: 7,400 EU buys 7.33 MJ, where
The Iron Tree says that working lands, and his reserve holds twelve apex
strikes. His reserve clock (21 s) and his heat clock (33 s) come out within a
factor of 1.6 — which is the mechanic η exists to create, and it does not exist
at 1 MJ.

**The reserve table the cards say does not exist now has a spine, and the
method was already ruled.** `Summoned and Bound/Obrenkael · The Mule.md:215`
(2026-09-12) interpolates log-linearly **on Level**, not on Stage. Fitted to its
own three anchors: **0.012812 decades per Level, ×10 every 78 Levels**, the two
segments agreeing to 1.7%. Put through Part One's four Band gates it gives a
hard reserve ceiling per Stage and a working band per Level-Band cluster —
**29 of 31 attested reserves sit under the ceiling, 22 of 31 within a decade of
the band**, with all 31 characters placed. The Part also carries the nine-rung
spine (joules → Grade → Tier 1–9, derived from Part Four and Part Five with no
name invented) that every WAR-13 ladder will hang on; the tier *names* are
deliberately absent, being WAR-13's.

**New:** `CONFLICTS.md` **C-041** — Sodoku Moto (Level 320, Stage VI) and
Krothar Veylshroud (Level 380, Stage VIII) stand past Band gates their Stage
has not opened, and those gates are the only hard ceiling canon puts on a
reserve. Two further questions are named as PENDING in the Part rather than
filed, because a sentence from Isaac settles either and neither is plainly
canon against canon: **the missing mass** in `AU/s = Flux Density × η` (the
identity is dimensionally short one mass; 21 of 29 cards imply 0.2–10 g and the
three it already fits imply exactly 1 g, but Draen Varos — the one card stating
a Crystal mass — implies 0.00024 g against his own nine kilograms), and **the
two recovery populations** (six cards at 9–28% of reserve a minute, four at
0.025–3.1%, medians 2.15 decades apart).

**No card, page or figure was changed.** C-034 to C-040 stay open and the Part
marks every table that rests on one. `imports/essence-ledger/ledger_tables.py`
reproduces every figure in the Part from `anchors.json` and `fit.json` alone.
**Next:** WAR-11 is the rulings Isaac owes; WAR-13 is the ladders; WAR-14 is
publication.

## State on 2026-09-25 (the Essence Ledger's Part, rebuilt at the ruled constant)

**Supersedes the block above on one point and one only: the constant.** That
block says the Part works at 1 EU = 1 kJ. It does not any more. Isaac answered
C-034 on 2026-09-25 (WAR-11), logged as **R44-1**: *"One constant: 1 EU = 1 MJ
stands. The Ledger converts at 1 MJ everywhere, and the card figures that then
sit outside their Stage's band are the error; each is a card correction in its
own issue, not in this ruling batch."* The ruling is later than the brief
permission the 1 kJ choice rested on, and later than the physics check. Rhett
Konn sent WAR-12 back for it; the Part is rebuilt. **`ledger_tables.py` carries
the constant in one place, `K = 1e6`** — every joule, watt, ton of TNT, drain
figure, waste figure and Starvation floor in the Part follows from it.

**The physics case is not deleted; it is recorded as the residual, which is what
the finish line asked for.** `CLAUDE.md`: a ruling and a physics note
disagreeing is recorded, never resolved. The Part's **§2.4** and **§9.2** are
that record, quoted from `physics-check.md` in its own words: the ruled constant
misses canon's three self-pricing lines by 2.45–2.98 decades in one direction;
it is outside all four of that note's physical brackets, including E = mc² on
Draen Varos and Kaelzar; the EU→J→Grade chain now lands Dougou's apex working at
**B-Grade** where The Iron Tree:41 says D-to-low-C, +2.54 decades; conducted
waste needs ΔT of 10⁵–10⁸ K across three millimetres of skin; and at 1 AU/s =
1 MW **every anchor reaches a lethal core temperature in 0.031 ps to 32.8 ms**,
so Essence Starvation's ten-percent floor is unreachable on the body-heat route.
The Part states each of these and moves the ruling nowhere. The route to revisit
R44-1 is a fresh ruling on WAR-11, and Gemma Nye's independent second opinion on
the note is WAR-59.

**Four further R44 rows are applied, each quoted where used and listed in the
Part's new §9.1.** R44-2 (the AU/s identity governs; the card figures are the
error) rewrites §6's framing and, with it, why the five "sheets their own two
numbers cannot be" stay flagged and unfiled — all five are among the twenty-six
R44-2 already calls errors, and WAR-48 will move them. **R44-3** (the S-to-SS
joule gap, 24.3–41.8 TJ, is ranked by Sub-Stat and not by joules) is now stated
inside the **§3 spine**, because WAR-13 hangs six ladders on that section and
would otherwise inherit the gap silently; the first attested figure to land in
it is Kwon Mu-jin's cheapest summons, 37.0 TJ, worked in §5.2. **R44-4** (η
reads 0.60–0.70 at Stage VI–VII) and **R44-5** (a card's η governs per
character) settle the one η in the Part that came off a table.

**New, and small: WAR-94.** Applying R44-5 turned up that `anchors.json` has no
η for Naiser Yukari although `Naiser Yukari.md:60` states 0.89 — Phase 1's
extractor read his AU/s row and missed the "Aetheric Efficiency" row beneath it,
and the label is the likely cause, so other cards may be affected. Not a canon
conflict and no card touched. `ledger_tables.py` patches it in one named place
(`CARD_ETA_MISSED_BY_PHASE_1`, with the card line quoted) and WAR-94 is the fix
at source.

**Unchanged by the rebuild:** §4's reserve law and every reserve band. The
0.012812-decades-per-Level fit is in EU space off the ruled Obrenkael method, so
the constant does not touch it; only the joule columns beside it moved. C-041
stands as filed, with one correction Rhett caught — its FoW I:18 quote had
carried bold the source does not, now character for character. The two open
questions the block above names (the missing mass, the two recovery populations)
both survive their rulings and are restated as questions against live rulings
rather than as open conflict rows; a third is added, **where the Shell dumps its
waste**, because that is the one thing that decides whether §5.3's body clock or
§6.4's burn radius binds a practitioner at full output.

**No card, page, config or wiki file was changed.** `validate.py` PASS, 691
rules. **Next:** WAR-13 the ladders (the §3 spine is ready and now carries
R44-3's carve-out), WAR-14 publication, WAR-46/WAR-48 the card sweeps R44-1 and
R44-2 order, WAR-94 the extractor gap.

## State on 2026-09-25 (the venv is not missing; the gate works)

**Correcting the 09-24 block's "One environment fault" paragraph. Nothing is
broken and nothing is owed to Isaac there.** That paragraph says the `wotr`
MCP server will not start, that its interpreter "no longer exists", that
`load_rules`, `fow_line` and `verify_scene` are unavailable to every agent, and
that rebuilding the venv is Isaac's. It stays above as written; this block is
the correction. Rhett Konn found it while working WAR-75 and filed WAR-107; the
readings below were re-taken in a fresh agent run today.

**What was actually happening: `$HOME` is redirected inside an agent run.** A
run's `$HOME` is a Paperclip sandbox directory under `/tmp/paperclip-ai-…`, so
`~/.venvs/wotr` — the "one interpreter" `AGENTS.md` names — expands to
`/tmp/paperclip-ai-…/.venvs/wotr/bin/python`, which does not exist and never
did. The venv on this machine is fine, has both packages, and has not moved:

```
/home/oridon/.venvs/wotr/bin/python build/validate.py
  691 rules across 43 files
    live=566  superseded=125
  PASS   (exit 0)
```

The other two interpreters a run can reach both **exit 1**: a bare `python` is
mise's (`/home/oridon/.local/share/mise/installs/python/latest/bin/python`) and
says `pyyaml missing`; `/usr/bin/python3` says `jsonschema missing`. Only the
project venv has both, which is exactly what `AGENTS.md` already says. An agent
that read `pyyaml missing` together with the 09-24 note concluded the machine
was broken, and one (Phenna, 09-24) went to a throwaway venv in a scratch dir —
which rule 1.4 forbids and nobody needed.

**How to run a WOTR tool in an agent run.** Both of these are measured PASS,
exit 0, in a run today:

- `bash build/py.sh build/validate.py` — the form `AGENTS.md` calls safest, and
  it works here because the run environment already exports
  `WOTR_PYTHON=/home/oridon/.venvs/wotr/bin/python` and
  `WOTR_ENV_FILE=/home/oridon/.config/wotr/env`, both absolute into the real
  home, and `env.sh` prefers an exported `WOTR_PYTHON` over `$HOME/.venvs`.
- `/home/oridon/.venvs/wotr/bin/python build/validate.py` — the absolute path,
  which depends on no environment variable at all. Use this if `py.sh` ever
  prints `env.sh: no interpreter at /tmp/paperclip-ai-…`: that line means
  `WOTR_PYTHON` was not exported into the run, `env.sh` fell back through the
  redirected `$HOME` to a package-less `python3`, and the exit code is not the
  gate. **Never** `pip install` into either fallback interpreter, and never
  build a venv of your own; `validate.py`'s own error message suggesting the
  pip line is aimed at a human on the machine, not at a run.

The general form: `~` in any repo document means `/home/oridon`, because the
documents were written on the machine. Inside a run it does not, so type the
absolute path or go through `py.sh`.

**The MCP half of the 09-24 claim is also false today, and was tested.**
`mcp__wotr__load_rules` answered in this run (87 rules for `verification`), so
the server starts and the prose tools are available. The MCP is launched from
`.mcp.json` by the harness per run, not from an agent's shell, so a run that
finds the `wotr` tools genuinely missing is a harness fault to report on the
issue (house rule 1.4) — not this venv, and not something to work around.

**Void, therefore:** the 09-24 block's "Someone rebuilds the `wotr` venv before
the first prose run of the day" and "Rebuilding it is Isaac's". There is nothing
to rebuild. The validation gate (house rule 4.1) has been available the whole
time.

**Not done here, and open for whoever owns it:** whether `AGENTS.md`'s one-
interpreter bullet should give `/home/oridon/.venvs/wotr/bin/python` rather than
`~/.venvs/wotr/bin/python`, since `AGENTS.md` is on the do-not-edit list for
most agents. Rhett raised it; it was not filed and nothing in `AGENTS.md`,
`schema/` or `build/` was touched for this block. No rule, card, page, config or
wiki file changed (WAR-107).

## State on 2026-09-25 (the sweep now reads a card's η written without the η)

**WAR-94 is fixed at source (`8ff44e3`).** Phase 1's extractor read Naiser
Yukari's AU/s row and missed the `| **Aetheric Efficiency** | 0.89 |` row under
it. The cause, exactly: `ETA_LABEL` in `imports/essence-ledger/extract_anchors.py`
hand-rolled its separator instead of using the module's `SEP`, so it accepted
only a literal `(η)` and only `· : |` and a `**` stopped it dead; `ETA_ONE` needs
the literal η character, which that row does not have. `ETA_FIELD` is added and
tried **only after** all three older patterns have failed, so no line that
already yields a figure can have its figure changed — verified, not asserted:
+4 candidate rows, 0 lost, 0 existing value changed. Its separator must carry a
field marker, which is what keeps it off `Verinus VII · The Palatine.md:131`'s
"Transfer efficiency 1.0 by definition" — a technique's transfer ratio inside a
bold span, not a Coherence η.

**The sweep ran wide over all four measures** (every wiki line naming a measure
and carrying a digit that `scan_line` reported nothing for, no distance window)
and found **four figures on four cards**: η **0.89** `Naiser Yukari.md:60`, η
**~0.76** `Krothar Thunn-Gorr — The Old Chain.md:40`, η **0.22** `Torven Greis —
The Merchant Lord.md:39`, AU/s **~420,000** `Krothar Veylshroud …:100`. The two
new η are the same family by a second mechanism — `**η (Coherence Efficiency):**`
puts 26 non-digit characters between the η and the number where `ETA_ONE` allows
18. Veylshroud's is the fourth measure's version: the label `**AU/s Output:**`
was stopped by its own second word, so `AU/s Output` joins the label list.
Thunn-Gorr and Torven Greis had **no anchor row of any kind** before this.
Nothing else is missed by this cause; `flux_density` and `eu_reserve` none.

**What moved, and the half of it that is not WAR-94's.** The fitted constant did
not move, and neither did §4's reserve law or any reserve band. `fit.json` moved
one row: Naiser's η **0.65 → 0.89**, `eta_from` now `page, line 60`, R44-5 read
off the corpus instead of patched around it. He joins `formula_check` as a row
that does not hold (480 × 0.89 = 427.2 against his card's 340 AU/s; under R44-2
the AU/s is the error). `CARD_ETA_MISSED_BY_PHASE_1` is **removed** from
`ledger_tables.py` — it reached `drain()` only, so the four reserve-band cells
that read η off `fit.json` had kept a Tier midpoint and now read 0.89 too; `drain`
gains Krothar Veylshroud. **But rebuilding `anchors.json` from the committed
scripts produced a different file before a line was changed**, because `de43b93`
(`Wiki sync: 290 file(s) changed in Notion`, 18:40) landed **20 card figures**
after WAR-71 committed it: 19 cards' AU/s under R44-2's identity and Kinjiki's η
1.3 → 1.2 under C-031, all verified against the commit as real applied edits
(`Draen Varos` 98,000 → **408,700,000**). A mirror-only baseline was built first
so the two could be told apart, and they are, in the commit message and on the
issue. The consequence is large and sits in `ledger_tables.json` now:
**`flux_eta.holds_exactly` 3 → 19** of 30, `implied_mass_between_0p2_and_10_g`
21 → 28 — the counts the Part's §6 argues the missing mass from.

**`the-essence-ledger.md` is deliberately untouched** and now disagrees with
`ledger_tables.json`. Republishing 20 figures from another issue's card sweep is
not a regex issue's call: **WAR-117** owns the rebuild (its step 1 is done, its
"expect exactly four values, 0.55 to 0.65" is superseded — the four cells read
0.89) and **WAR-13** has been told before it hangs its ladders. §5.3's footnote
can now be shortened to "the card states it". New: **WAR-125**, three attested
figures the sweep found and left because each is data entry rather than an
extractor defect (Veylshroud's second, passive 135,000 AU/s; Wystan Ashmore's
Flux Density labelled just "Flux" in prose; Helki's superseded 1,200,000
capacity). No card, page, config or wiki file changed. `validate.py` PASS.
