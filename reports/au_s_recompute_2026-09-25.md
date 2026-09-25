# The twenty-six AU/s figures recomputed as Flux Density × η — WAR-48, 2026-09-25

Etta Band. `imports/essence-ledger/fit.json` `formula_check` is the input; every figure below is
computed from it, none typed. `python build/validate.py` PASS, 697 rules, live=572 superseded=125,
before and after — this run changed no rule and no card.

## Applied 2026-09-25, after WAR-96 (second pass)

**Sixteen cards, nineteen statements, are corrected on the live Notion pages.** WAR-96 shipped
R44-1..R44-6 into `RULINGS.md` on `origin/master` (`e1a5cda`), so the record gap this report was first
written around is closed; the section below is kept as the account of why the first pass withheld.
R44-2 was read in both layers of its entry — the option as Isaac was given it and the one-sentence
form the index row quotes — and both say the same thing.

**Applied (16 cards / 19 statements).** Anryū Ichimonji 9,870 · Draen Varos 408,700,000 ·
Garron Vuldane 11,610,000 · Iracordas 8,742 · Kael Serradyn 13,692,000 · Lucius Xenotro 37,720 ·
Mavra Cindrel 3,782,000 · **Mizuki Moto 6,478** (both statements) · **Muken Moto 15,624** (both) ·
Naevra Yukari 2,784 · **Niran Yukari 16,376** (both) · Rashani Zettari 6,642 · Rengai Zettari 14,196 ·
Serai Linthra 7,098,000 · Valthren Odrin 8,442,000 · Yorime Seikai 13,066. Each edit replaced the
AU/s figure alone, by exact-match on the card's own wording, so the field keeps its own form
(comma-grouped integer) and Flux Density and η are untouched on every card. A page whose live text had
drifted from the mirror would have failed the match rather than been overwritten; none did.

**Held (4) — the exact product lands on a decimal.** Artemis Amagiri Moto 1,663.2 · Ayame Yuno 438.6 ·
Vethraun Ashmaw 282.1 · Yukazuri Moto 258.1. No AU/s field in the corpus has ever held a decimal, and
rounding would invent a number. Doc Kett's WAR-96 comment names this as still open and not R44-2's to
answer, so it stays with the six at WAR-102.

**Stopped (6) — unchanged from the first pass**, and now recorded in `CONFLICTS.md`: Gimbzo (**C-053**)
and Dougou Ozumu Zettari (**C-054**) on contradiction; Elion Drevas, Ignatius, Borin Ironheart and
Sodoku Moto on form. The two rows were withheld on the first pass only because R44-2 was not yet
recorded; that reason is gone.

**The contradiction test was run on all sixteen before applying.** No card among them binds a cast
time to its output, and every stated maintenance rate (Anryū 4,800 EU/s, Lucius 34,000, Niran 8,400,
Rengai 6,200, Mizuki 2,800, Rashani 1,800) stays below that card's recomputed AU/s. Anryū's second
AU/s mention at `:83` is a Domain collapse threshold of 1.1 billion, not his own output, and 9,870
sits far below it as 52,000 did.

## What the first pass did and did not do

**It recomputed all twenty-six and changed none of them.** The arithmetic is settled for twenty of
the twenty-six, two are stopped for contradicting a figure their own card states elsewhere, and four
are stopped because the ruling does not say what their form becomes. The twenty that are arithmetically
ready were not applied, and the reason was not arithmetic: **R44-2 was in no `RULINGS.md`, and the file
that carries it was not on master.** `CLAUDE.md`: *"A ruling exists only if it is in `RULINGS.md`
(Isaac's or an agent ruling)."* That is house rule 3.2 and the first pass stopped on it.

## The record gap, verified two ways — closed by WAR-96 on 2026-09-25

1. **R44-2's verbatim is in no `RULINGS.md`.** `grep` for `Flux Density`, `AU/s = `, `C-035` and
   `One constant` over `RULINGS.md` returns nothing, on this branch and on `origin/master`.
   `RULINGS.md`'s 2026-09-25 section is a different ruling — Isaac's seven precedence-ladder answers
   on WAR-61. It *mentions* R44-3 and R44-5 by id in its examples, as though they were already
   recorded, and carries none of the four C-row closures.
2. **The only file R44-2 is written in is not on master.**
   `rules/doc-essence-ledger-rulings-2026-09-25.yaml` was added by `f335403` (*"C-034..C-037 applied:
   the Essence Ledger rulings (WAR-22)"*), which is unpushed on this branch;
   `git ls-tree origin/master rules/` has 43 files and none of them is it. The yaml's own header says
   *"The record is the 2026-09-25 entry in RULINGS.md; each verbatim quotes it"*, and all six rows
   carry `source.file: ''`, the standalone pattern `AGENTS.md` says `validate.py` deliberately does
   not check — *"those quotes rest on your care alone."*

This is **WAR-96** (*"R44-1..R44-6 quote a RULINGS.md entry that is not in RULINGS.md"*), filed out of
WAR-72 to Doc Kett, `canon`, still `todo`. Nothing about R44-2's *content* is in question here: the
issue description quotes Isaac's answer on WAR-11 and this run has no reason to doubt it. What is
missing is the record, and `RULINGS.md` is written only through `log_ruling` — not by hand, not from a
worktree, and not by this issue, whose task is not what that tool does. So WAR-48 blocks on WAR-96
rather than deciding the twenty-six on an unrecorded ruling.

**Why that is not a formality here.** Twenty-six live cards, thirty statements, and the moves are
large: the smallest miss is ×1.049 and the largest is ×7.747 × 10⁷. Eight cards move by more than 1.89
decades — Gimbzo 7.89, Draen Varos 3.62, Serai Linthra 2.08, Garron Vuldane 1.99, Elion Drevas 1.99,
Kael Serradyn 1.98, Valthren Odrin 1.97, Mavra Cindrel 1.90. A figure put on a card under a ruling
that turns out not to exist is worse than a figure left wrong, because the second is recorded as
wrong and the first is not.

## The table

`recomputed` is Flux Density × η, exactly, from the card's own two figures. η is the card's own under
R44-5 in every row. Flux Density and η are untouched throughout: R44-2 names the AU/s figures and
nothing else.

Figures are given as numbers; each card's own wording is quoted in the sections below.

| # | Card | FD | η | stated AU/s | recomputed | ×stated/recomputed | verdict |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | Anryū Ichimonji | 9,400 | 1.05 | 52,000 | 9,870 | 5.268 | arithmetic settled |
| 2 | Artemis Amagiri Moto | 1,980 | 0.84 | 7,600 | 1,663.2 | 4.57 | arithmetic settled |
| 3 | Ayame Yuno | 510 | 0.86 | 1,900 | 438.6 | 4.332 | arithmetic settled |
| 4 | Borin Ironheart · The Master of the Soul Forge | 11,000 | 0.91 | 3,200 | 10,010 | 0.3197 | form not ruled — logged, left |
| 5 | Dougou Ozumu Zettari | 18,400 | 0.99 | 3,900 | 18,216 | 0.2141 | contradiction — stopped |
| 6 | Draen Varos · The Red Forge Sentinel | 670,000,000 | 0.61 | 98,000 | 408,700,000 | 0.0002398 | arithmetic settled |
| 7 | Elion Drevas · The Black Cleric | 9,400,000 | 0.75 | 72,000 | 7,050,000 | 0.01021 | form not ruled — logged, left |
| 8 | Garron Vuldane · Warden of Thaumar | 13,500,000 | 0.86 | 118,000 | 11,610,000 | 0.01016 | arithmetic settled |
| 9 | Gimbzo | 9.2 × 10⁶ | 0.94 | 6.7 × 10¹⁴ | 8,648,000 | 7.747e+07 | contradiction — stopped |
| 10 | Ignatius Sanctus Sanctorum Arsenal · The Archpaladin | 5,400,000 | 0.90 | 5,100,000 | 4,860,000 | 1.049 | form not ruled — logged, left |
| 11 | Iracordas | 9,400 | 0.93 | 5,200 | 8,742 | 0.5948 | arithmetic settled |
| 12 | Kael Serradyn · The Burnmark | 16,300,000 | 0.84 | 145,000 | 13,692,000 | 0.01059 | arithmetic settled |
| 13 | Lucius Xenotro | 41,000 | 0.92 | 118,000 | 37,720 | 3.128 | arithmetic settled |
| 14 | Mavra Cindrel · The Golden Engine | 6,100,000 | 0.62 | 48,000 | 3,782,000 | 0.01269 | arithmetic settled |
| 15 | Mizuki Moto | 7,900 | 0.82 | 26,000 | 6,478 | 4.014 | arithmetic settled |
| 16 | Muken Moto | 18,600 | 0.84 | 72,000 | 15,624 | 4.608 | arithmetic settled |
| 17 | Naevra Yukari | 2,900 | 0.96 | 18,500 | 2,784 | 6.645 | arithmetic settled |
| 18 | Niran Yukari | 18,400 | 0.89 | 38,400 | 16,376 | 2.345 | arithmetic settled |
| 19 | Rashani Zettari | 8,200 | 0.81 | 24,000 | 6,642 | 3.613 | arithmetic settled |
| 20 | Rengai Zettari | 18,200 | 0.78 | 68,000 | 14,196 | 4.79 | arithmetic settled |
| 21 | Serai Linthra · The Serpent Alchemist | 7,800,000 | 0.91 | 59,000 | 7,098,000 | 0.008312 | arithmetic settled |
| 22 | Sodoku Moto | 920 | 0.84 | 3,800 | 772.8 | 4.917 | form not ruled — logged, left |
| 23 | Valthren Odrin · The Lantern Scribe | 12,600,000 | 0.67 | 91,000 | 8,442,000 | 0.01078 | arithmetic settled |
| 24 | Vethraun Ashmaw | 310 | 0.91 | 780 | 282.1 | 2.765 | arithmetic settled |
| 25 | Yorime Seikai | 13,900 | 0.94 | 2,850 | 13,066 | 0.2181 | arithmetic settled |
| 26 | Yukazuri Moto | 290 | 0.89 | 480 | 258.1 | 1.86 | arithmetic settled |

**The `verdict` column is the first pass's reading and is left as written.** For what each row's
figure actually became, read the applied / held / stopped lists at the top of this report: the sixteen
marked *arithmetic settled* whose product is a whole number were applied, and the four marked
*arithmetic settled* whose product lands on a decimal were held.

Twenty-nine cards state all three fields. Three hold exactly and are not in the table — **Ara Min Mahuo** (59,500), **Kwon Mu-jin** (1,566,000), **Yoko Mishiro** (75); each implies a mass of
exactly 1 g in the identity, which is the open question the Essence Ledger Part records and not this
issue's to settle.

## Where each figure is written

All twenty-six cards are under `wiki/Volume I — Character Cards/`. **Four state the AU/s twice**, so
the sweep is thirty statements, not twenty-six:

| Card | lines | note |
|---|---|---|
| Mizuki Moto | `:30`, `:59` | `Aether Index · 26,000 AU/s sustained` and the stat line |
| Muken Moto | `:34`, `:60` | `Aether Index · 72,000 AU/s` and `Output 72,000 AU/s` |
| Niran Yukari | `:28`, `:61` | the Aether row and the stat line |
| Yukazuri Moto | `:40`, `:61` | `Aether Index · 480 AU/s` and `Output 480 AU/s` |

**And `wiki/` is the Notion mirror, not the card.** A card correction is an edit to the Notion page;
the mirror returns through the hourly sync, which is how C-030..C-033 were applied on 2026-09-24
(*"Applied to the Notion card"*, *"the mirror in this worktree was deliberately not committed"*). So
when WAR-96 lands, the work is thirty block edits across twenty-six Notion pages, not twenty-six file
edits — and the sync that carries them back is itself blocked right now (*"Unstick the wiki sync: the
main checkout is mid-rebase with RULINGS.md unresolved"*).

## The two stopped for contradiction

The issue: *"If any recomputed figure would contradict a figure the same card states elsewhere, stop
on that card and record it rather than deciding it."* Two do.

### Gimbzo — ×7.747e+07

`wiki/Volume I — Character Cards/Gimbzo.md:61`

> | **Aether Output** | 6.7 × 10¹⁴ AU/s — **slow casting cadence, but each Work lands with siege weight** |

The card states three technique costs — `:82` **3.2 × 10¹² EU**, `:83` **8.7 × 10¹³ EU**, `:84` **1.1 × 10¹⁴ EU** — and an Essence Capacity of **4.8 × 10¹⁴ EU** at `:58`. At the stated 6.7 × 10¹⁴ AU/s the three pay out in 4.8 ms, 130 ms and 164 ms. At the recomputed 8.648 × 10⁶ they take 3.70 × 10⁵ s (4.3 days), 1.01 × 10⁷ s (116 days) and 1.27 × 10⁷ s (147 days). The recomputed figure makes every named Work on the card unusable, so it contradicts figures the same card states elsewhere and this run stops on it, as the issue instructs.

### Dougou Ozumu Zettari — ×0.2141

`wiki/Volume I — Character Cards/Dougou Ozumu Zettari.md:38`

> **Aether Index** · 3,900 AU/s external · **internal cycling immeasurable** · **η 0.99**

The card does not state an AU/s. It states, at `:38`, **`Aether Index · 3,900 AU/s external · internal cycling immeasurable · η 0.99`** — 3,900 is the *external* figure and the card says in the same breath that the internal figure cannot be measured. Flux Density × η is the whole output, not the external fraction of it, so the recomputed 18,216 is not a correction of the figure the card states; it is a different quantity. R44-2 names the stated AU/s figures as the error and says nothing about a card that splits the figure in two. Stopped and recorded.

## The four stopped on form

The issue: *"Where a card's AU/s is written as a range, a 'base' figure or with a qualifier … the
ruling does not say what the recomputed figure's wording becomes. Keep the card's own form if the
arithmetic fits it; if it does not, log the line and leave it rather than inventing a form."* Four do
not fit.

### Elion Drevas · The Black Cleric — ×0.01021

**The card's η is a range.** `:36` reads **`η · ~0.72–0.78, Band A, fluctuating with emotional resonance`**. `fit.json` carries 0.75, which is the extractor's midpoint and not a figure the card states; under R44-5 the card's η governs, and the card's η is 0.72–0.78. Flux Density × η is therefore **6.768–7.332 million AU/s**, a range, where the card's Aether Output field at `:37` is a single figure. R44-2 does not say what form a recomputed figure takes when the multiplicand is a range. Logged and left.

### Ignatius Sanctus Sanctorum Arsenal · The Archpaladin — ×1.049

**The figure is not in a stat field.** It is item one of the card's own section `## X · Open Rulings`, at `:141`:

> - **Essence Capacity 5.5 million EU, Flux Density 5.4 million EU/g, Output 5.1 million AU/s** carry from the legacy sheet. **I cannot source EU benchmarks by Stage** and have not restated them as confirmed.

The line is a record of what the legacy sheet said and of the fact that it is unconfirmed. Rewriting 5.1 to 4.86 million there would falsify the record rather than correct a figure. The miss is also the smallest of the twenty-six, ×1.049. Logged and left.

### Borin Ironheart · The Master of the Soul Forge — ×0.3197

**All three fields call themselves estimates.** `:103` **`Aether Output (AU/s): ~3,200 AU/s (est.)`**, `:104` **`~11,000 EU/g (est.)`**, `:105` **`η: 0.91 (est.)`**, with `:34` repeating **`0.91 (estimate — …)`**. WAR-46 held that a line calling itself an estimate is not a figure R44-1 names, and R44-2 is worded the same way — "the stated card AU/s figures". Recomputing gives exactly 10,010, a four-figure product, to be written into a field whose own form is `~3,200 … (est.)`. Logged and left.

### Sodoku Moto — ×4.917

**"~3,800 base"**, at `:86`. The issue names this line. `base` says the figure is a floor he rises from; Flux Density × η yields one value, 772.8, and there is no basis on the card for calling it a base rather than the whole. `~772.8 base` is also a tilde and a decimal in one field. R44-2 does not say what the wording becomes. Logged and left.

## One form question the twenty do raise, and it is not settled either

**Four of the twenty land on a decimal** where every AU/s field in the corpus is written as a whole
number:

- **Artemis Amagiri Moto** — 1,980 × 0.84 = **1,663.2** (stated 7,600)
- **Ayame Yuno** — 510 × 0.86 = **438.6** (stated 1,900)
- **Vethraun Ashmaw** — 310 × 0.91 = **282.1** (stated 780)
- **Yukazuri Moto** — 290 × 0.89 = **258.1** (stated 480)

Writing `438.6 AU/s` invents no number — it is the exact product — but it does put a decimal in a
field that has never held one, and rounding it to `439` would invent one, which house rule 3.3
forbids. This run has not decided it, and it is the same question in a different coat as
*"Ruling needed: what a card figure corrected under R44-1 becomes"*, still in the backlog. If the
answer there is "the exact figure, in the field's own form", these four are covered by it and want no
second ruling.

## What is left to do, in order

1. ~~**WAR-96** records R44-1..R44-6 in `RULINGS.md`~~ — **done 2026-09-25**, `e1a5cda` on master.
2. ~~**Twenty cards take the recomputed figure**~~ — **sixteen applied**, listed at the top of this
   report. The remaining four of the twenty are the decimal cases and are held with the six.
3. **Ten cards need a ruling, not a sweep** — Gimbzo (**C-053**) and Dougou (**C-054**) on
   contradiction; Elion Drevas, Ignatius, Borin Ironheart and Sodoku Moto on form; Artemis, Ayame,
   Vethraun and Yukazuri on the decimal. All ten are on **WAR-102** (Doc Kett), each with both sides
   quoted and neither resolved.
4. **The mirror still has to come back.** The nineteen edits are live in Notion; `wiki/` in git will
   not show them until the hourly sync commits again, which is blocked on **WAR-29** / **WAR-68**.
   Until then a grep of `wiki/` returns the old figures, per the standing warning in `CONTINUE.md`.

