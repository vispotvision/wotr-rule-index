# Alchemetrica update: the check

Checked: `changes.md`, `plan.json` (52 markdown edits), `blockops.json` (29 block operations) and the live render `/tmp/wotr-drafts/alchemetrica-live.md`, against decisions.md (K, GW, GL, EC, WS, DE, SE, ML), fixes.md, the 2026-09-28 rulings in RULINGS.md, CONFLICTS.md C-092 to C-134, the published Codex I and II and The Farrant Papers, the sister wiki pages, and the Master Codex workbook (read through `build/codex.py`).

Originals are kept beside the fixed files: `plan.orig.json`, `blockops.orig.json`, `changes.orig.md`, `build_plan.orig.py`, `build_blockops.orig.py`. The fixes were made in `build_plan.py` and `build_blockops.py`, which regenerate `plan.json` and `blockops.json`, and carried into `changes.md` by the same string replacements.

## Findings

### Fixed

**F1. Item 6, the Aphorism of Mortalis was misstated.** The plan had it book "the payment as a debt, owed by the site and by the hands that worked it and settled out of sight". "Settled out of sight" is Mu-jin's Correction (GW8: "given on credit and settled out of sight"). "Debt on the site and the operators" is the Tempus drift's price (SE10). GW9 says the overview "prints doctrine and gloss apart", and the Aphorism itself, as published, is narrower. Codex I L175: "Whoever does it is a debtor: he borrows the current of Mortalis and cannot step back out of it without a cost to his own Crystal." Papers L191: "the old debt doctrine, the Aphorism of Mortalis: whoever raises the dead borrows the current and cannot step back out of it without a cost to his own Crystal."
Now: "*An older doctrine, the Aphorism of Mortalis, reads death-work as a debt: whoever raises the dead borrows the current of Mortalis and cannot step back out of it without a cost to his own Crystal. It is one reading among several of what a working owes, and the schools still argue it.*" This keeps it contested, as GW8 has it: "Still a contested position".

**F2. Item 6, a repeated sentence and an unclear clause.** "No practitioner spends reserve on a Draft." repeated the sentence before it ("the maker's reserve is never drawn on"), so it was cut. "Speeds a Wellspring's own recovery in the patient" became "hurries the recovery a Wellspring gives the patient". EC2 says alchemical treatment "reads as speeding Wellspring recovery, not supplying EU".

**F3. Item 13, an invented rule that contradicts the page.** The plan had "a maker cannot hold a stage steady in the glass until he has walked it himself". No decision says this. It is also false against the page: L316 has a Drafter run Coagulations alone, while Coagulation's first round is Refraction (Stage VII), and a pure alchemist walks no Stage. "All true alchemy" also claimed more than the ground does. Codex II L185 reads: "The Great Work moves through seven stages ... What burns in the crucible burns in the man who tends it."
Now: "The Work moves through seven stages, in one order: ... They are taught as disciplines laid on both at once, and what burns in the crucible burns in the one who tends it."

**F4. Item 13, an invented cause.** The plan had "It belongs to no single Wellspring, which is why a Conjunction bench needs its mediation glyphs". The page's own reason for the glyphs is L94: they are "the structural buffer the Continuum requires before it will permit two laws to occupy one substrate". Codex I L141 gives no cause from the missing current.
Now: "It belongs to no single Wellspring. A Conjunction bench still needs its mediation glyphs, and a Conjunction corrupted injures Attraction itself." The last clause is WS1's: "Conjunction's Corruption injures Attraction itself."

**F5. Item 13, "The Work is the Temperance path" said more than GW1 says.** GW1 maps the stages onto the Stages for the maker and adds "For Class Ø the maker side is read on grain". A pure alchemist walks the Work and never the Temperance path, so the bare identity was false for Class Ø. "The trade calls it the spiral" also named a trade usage that nothing attests. Codex II L373 has only "It proceeds as a spiral".
Now: "**For a Crystal-bearer, the maker's side of the Work is the Temperance path.** ... The Work climbs as a spiral."

**F6. Item 13, a false line in the hinge paragraph.** The plan had "The six Wellsprings that are also operations lend their laws to both maps." That fails for four of them. Transmutatio, Fixatio and Materia Primordia map to no stage, and Sublimatio maps to no stage, since the Distillation stage draws on Sublimare. Only Dissolution and Coagulatio sit on both. The sentence is cut, and the gap stays recorded as T16.

**F7. Item 19, a "week" conversion that doubled the time.** "An apprentice learns the four in a week" had become "in a turn". A turn is fourteen days (The Sky, the Hour and the Year: "**The turn** is fourteen days"). Now: "in half a turn". The other unit changes (items 20, 22, 32, 34, 36, 45) convert weeks to turns correctly or use "turns" loosely where the page said "weeks".

**F8. Items 16 and 63, an ungrounded tie between the Parunic Echo and forensic Distillation.** GL10 and Codex II L127 define the Echo as the Essence Signature in residue, "legible to any reader from Flourishing up". No decision, ruling or published line says forensic Distillation reads the Echo. Item 16's Cell 3 addition was withdrawn, so Cell 3 stays word for word as live, and item 63's sentence "Forensic Distillation reads it back to its root, the same way it reads a corrupted vein or a doubted lot" was cut. Item 16's Cell 1 and Cell 2 changes stand.

**F9. Item 48b, a doubled phrase.** The plan printed "under the nailbeds, **grey nail-beds and pale bands ...**", which spells the same word two ways in one sentence and tied the arsenic bands to every practitioner. Now: "Discolouration in the sclera and under the nailbeds, keyed to what the practitioner has handled most. **A physician's doses leave grey nail-beds and pale bands across the nails.**" Grounds: Papers L201 ("Grey nail-beds, and pale bands across the nails") and Codex I L145 ("The grey was Draft-mark, keyed to what he handled most: quicksilver, calomel ... white arsenic").

**F10. Item 52, the intro contradicted the section.** The intro called the summons "Vocatia's work", but the section itself follows DE4: "A Greater Summons: vessel, Animatria and Vocatia together". Now: "The summons that fills an impression-body belongs to Animatria and Vocatia".

**F11. Item 52, grammar.** "closes on the glyph that states when it ends, [Vor] Return among them" becomes "closes on a glyph that states when it ends, such as [Vor] Return". GL3 applies ("Vor (Return), written as a closing condition"), and [Vor] Return was checked against the Master Glyph Index.

**F12. Item 52, the Open Shell's scale was downgraded and its Grade left unnamed.** The plan said it "breaches a whole region". GL8 says "The one Mortalis failure that crosses into civilizational breach", and the Grade it is filed under is the Heresiology's "V · Mechanica Trespass ... civilizational breach" (Heresiology, Grades of Offense). A bare "Grade V" also reads as a Fracture of Worlds letter Grade. Now: "filed at Grade V, Mechanica Trespass ... the one failure of death-work that crosses into civilizational breach."

**F13. Item 52, an opaque clearance clause.** "Sealed at Tier VI, and clearance runs upward" becomes "sealed at Tier VI clearance, where a higher numeral is the tighter seal". The ground is necrocursica-calls 2: "Clearance runs upward: a higher Tier numeral is more restricted. The treatise is Tier VI". The clause also keeps the clearance numeral apart from the named Tiers of Standing.

**F14. Item 52, "Two inks, two roles, one floor" made one site into doctrine.** Papers L279 is about the one floor at Castlefall ("Two roles of one working, on one floor, in two inks"). EC15 names two roles. Now: "**Two inks for two roles.**"

**F15. Item 55, Mechanica was narrowed to extraction from a Crystal.** The plan made every Mechanica working take output "from a Crystal that is not the operator's". The sister page says otherwise. Mechanica Extraction Without Recognition :18: "The law was conditioned by somebody else, or by a site, or by a thing that was alive at the time." Its :24 treats extraction as one of three practices. Papers L337 defines extraction alone.
Now (blockops item 55): "It skips the process and **takes the output directly**, from whatever did the conditioning: another practitioner, a site, or a thing that was alive at the time. Output taken from a Crystal that is not the operator's is extraction, and the donor may be dead. Mechanica creates structural debt ..."

**F16. Item 63, the grade's location contradicted the page.** The plan had "stamped low on the vessel". That comes from one lot (Papers L163), and the page puts the grade in "the three marks struck into the seal" (L132, The Mark; also L219, "a legitimate three-mark seal"). Now: "struck at the Mark, and the grade is the stamp's." The Papers' "The grade is the stamp's" is kept.

**F17. Item 63, one lot generalised, leaning on open C-127.** "A contracted lot ships in dark glass with a lute of grey wax over the stopper. The consignor's wax goes over the lute, and the maker's mark is in the glass." The glass and the wax describe one lot (Papers L163). The consignor-and-glass rule is the Papers' reading of the exact marks that C-127 leaves open: GL5 has "Maker's mark and cutter's hand both trace De Raits", while the Papers put Furveus in the glass and Draycott in the wax. Printing that reading as general law would take a side, so both sentences are cut. GL12's general rule of the registered craft mark stays.

**F18. Item 65, grammar.** "a Boundary failure first among it" becomes "a Boundary failure above all".

**F19. Item 67, a false count of counters.** The plan had "Each has a counter, and the Heresiology's vows name them." That is untrue now. The Heresiology's seven Vows leave Non-Commitment unguarded (GW7's question: "Conviction and Conjunction take two each and Non-Commitment, the Codex's own, none"), and the eighth vow belongs to Volume III, which is not written. Now: "The Heresiology's vows are sworn against them, and a vow broken is a Shear Break." The ground is the Heresiology's "a vow broken is a Shear Break". No count of vows is given.

**F20. Item 70, formatting lost.** plan.json had turned the page's bold-italic "***Every workshop that has not changed a procedure ...***" into italic. changes.md kept it as it was. The bold-italic is restored in plan.json.

**F21. Item 30, an invented reading of the Yellowing.** "it is the warning before the Reddening" becomes "it is the tincture arriving, on the way to the Reddening", in the page's own words from L144 ("The tincture arriving").

**F22. Item 26, a rule stated for every chain.** "A chain closes on a glyph and runs under Fixatio's law" becomes "A Sealing chain closes on a glyph ...". Fixatio governs the Sealing. GL2 ("sealed by Tp (Topology) on a Fixatio chain") says nothing of other chains.

**F23. Item 11b, the same sentence printed twice.** The italic repeated item 6's sentence word for word ("a pure alchemist's standing work goes out under a Crystal-bearer's seal"). Now: "*The seal is the price of the arrangement: whatever a pure alchemist makes to stand goes out under a Crystal-bearer's seal.*" EC1 is unchanged in substance: "a pure alchemist's needs a Crystal-bearer's seal".

**F24. Item 13, "every" physician-alchemist's cabinet.** This became "the physician-alchemist's cabinet". EC6 grounds the names and the dose, not a universal stock.

**F25. Conflict quotes that were not exact substrings of their files** (the T list in changes.md; corrected below):
- T4, The Four Crafts: "A Draft acts on the Essence Core." is not in the file with a full stop. The exact text is "A Draft acts on the Essence Core, and a Class Ø soul has a Core like anyone else."
- T10, The Alchemical Index: the quote ends "surrounding work with them" with no full stop.
- T15, The Apparatus of the Age: the italic runs on. The exact text is "The Alchemetrica classes both as alchemical products, which they are".
- T2, R53-01: exact in the rule's parsed `verbatim` field. The raw YAML folds the line.

### Checked and rejected (no change)

- **R1. Item 52, "Harmonised work is lawful work" overstates, since the Bench reservation is a second test.** Rejected. GL9's own terms are "Whose Mortalis work is lawfully authorized ... so their death-work is lawful rather than forged Mechanica" and "The commission is lawful work done well". The page's "lawful" is the Mechanica sense ("lawful Wellspring process", L274), and the next paragraph, "Reserved by rank", states the second test.
- **R2. Item 11, Four becomes Adept and Seven becomes Grandmaster.** Kept. This is the faithful numeral conversion under R47-7 (Tiered Path: 4 Adept, 7 Grandmaster). The rulings audit's "Master reads truer" would change the fact, so it is not made.
- **R3. Item 57, "alchemist" becomes "Crystal-bearer" at Master.** Kept. Under EC3 a pure alchemist stops at Expert, so a Master is a Crystal-bearer, and the change adds nothing false. T8 stays recorded.
- **R4. Item 16, Distillation "draws on" Sublimare where K5 says "mirrors".** Kept. It matches this morning's K6 line on the page (L14: "a distillation runs on Sublimare") and does not reverse K5: Sublimare still governs the Distillation operation. K6 makes Distillation a bench operation that no soul harmonises with, and "mirrors" is the table's word for the six Wellspring-operations.
- **R5. Item 63 prints the commission vessel's grade line as a clerk's example.** Kept. No name or provenance goes with it, and the line is ratified (R65-2).
- **R6. Item 29, "and it is not a product".** Kept. It is the live wording with the em dash removed, and it is not a "not X but Y" pair.
- **R7. Item 9, "separate the fused callouts".** No operation is needed. The fusion at L63/L64 and L68/L69 comes from the markdown export, which merges consecutive `>` lines. In Notion they are separate blocks (a6af102b in the column, ae8ca74f the Tiered Path callout), and the blockops dry check reads them as separate ids.

### Verified and standing

- **Great Work Stage names and order** (Sixteen Stages): I Murmuring, II Welling, III Ascension, IV Flourishing, V Splintering, VI Glory, VII Refraction, VIII Transcendence, IX Invocation, X Realization, XI Dissonance, XII Emanation, XIII Principality, XIV Zenith. GW1's four anchors fall correctly (V Fermentation, IX Dissolution, XI Conjunction, XIV Coagulation). EC10's floors (Flourishing, Glory, Refraction) sit at Tier 4 Adept, Tier 5 Expert and Tier 5 Expert, as the reservations read. No Levels are given, so C-117 is untouched.
- **Glyph Index names** (Master Codex, Master Glyph Index sheet): [Ur] Balance, [Ma] Recall, [Th] Foundation, [Ie] Perception, [Flx] Flux, [Xr] Excision, [Vael] Renewal, [Ora] Truth, [Wvn] Weave ("Foundation glyph for conjunction arrays; locks a third glyph in place."), [Ap] Aperture ("Valve control with a safety catch against over-spill."), [Vor] Return. Cinerion, Judicium, Rebirthine, Sublimare, Sublimatio, Coagulatio, Dissolution, Mortalis, Transmutatio, Fixatio and Materia Primordia are all on the Lists sheet.
- **Heresiology epithets**: Catastrophic Germination is Fermentation, Sanitized Truth is Distillation and Tyrannous Finality is Coagulation (Heresiology Appendix I), as GW6 has them.
- **Standing Index**: Gravemark Ink T4, reserved T5, which is Adept rank and the Expert gate (GL7 note; Papers L279). The Standing Index names T1 Household (item 27).
- **Alchemical Index**: Stillgate Ash's and Gravetide Ink's rows agree with items 52 and 63 (the ring grounds a residual charge, and living Essence at the ring bleeds; Gravetide is "the Boundary role made material").
- **The Tiered Path's carve-out** is live ("on the work alone, up to Tier Five, Expert, and no higher ... certified and never read off the Crystal ... caps what its holder makes exactly as a tempered Tier does"), and item 11 repeats it.
- **The Weathering duplicate** is removed once and kept once. Callout 74001ca2 keeps its own rich_text, the first print, which carries C-109's "a Crystal that never woke" and gets item 12's wording. Its six children, the reprint, are deleted: b2019093, 4cc44463 and b4bccd01 are empty spacers; 2b7ad8b6 ("...there is no organ to melt"), c1ef9eb9 and 10ff30e9 are the reprint in the old wording. Every id was re-read by GET and matches its recorded text.
- **Layout.** The column content (items 7 to 10) and the callout children (items 3, 11b, 39, 43b, 43c, 46b, 50, 55 to 57, 60, 61, 71) go through `blockops.json` as in-place block patches, so no column, callout or toggle is flattened. The quote at L36 is replaced by a quote plus the new subsection (dry run: `['quote'] with ['quote', 'heading_2', ...]`). New sections go in at H1 headings, and every table edit is cell by cell.
- **Clean publishing and prose law.** A scan of every `new` string in both files finds no em dash, "rather than", "instead", question mark, rule id, conflict id, date, "pending", "originated", hard-banned word, or name from the Codex, the Papers or the Necrocursica (Furveus, Calla, Draycott, Mu-jin, Malphas, Farrant). The remaining "not" hits are plain negations, with no corrective pair.
- **Open rows untouched**: C-117 (no Levels), C-123 (grain is real, single-axis and unread, and no Grade is given), C-124, C-125 (no author for the treatise), C-127 (no maker, cutter or holder is named, and the consignor rule is now cut too, F17), C-113 to C-116, C-118, C-120 to C-122, C-129 to C-134. Rows ruled today and applied here: C-092, C-093, C-096, C-097, C-098, C-107, C-109, C-128.

## Final dry run

Command: `cd /home/oridon/wotr-rule-index && bash build/py.sh build/apply_md_edits.py /tmp/wotr-drafts/alchemetrica/plan.json` (no `--apply`).

The tool's own dry run, run twice, stopped each time on a Notion read timeout (`TimeoutError: The read operation timed out`, raised in `segments()` while it re-read the page). By then every edit it had reached had matched: edits 1 to 28 in the first run, and edits 29 to 36 in a resume run on `plan.tail.json` (the last 24 edits). Both runs printed no MISS. Those lines are saved as `dryrun.part1.txt` (28 lines) and `dryrun.part2.txt` (8 lines).

To finish, `dryrun_cached.py` imports `apply_md_edits` itself (APPLY False, `--apply` refused), reads the page once with retries, and runs `apply_edit` for all 52 edits against that one read. A dry run writes nothing, so every edit sees the same page the tool re-reads each time. Output (`dryrun.cached.txt`), all 52 edits matched once with no MISS; its first 36 lines agree with the tool's own runs line for line:

```
1      edited in place
2      edited in place
4      edited in place
5+6    replaced 1 block(s) ['quote'] with ['quote', 'heading_2', 'paragraph', 'paragraph', 'paragraph', 'paragraph']
13     replaced 1 block(s) ['heading_1'] with ['heading_1', 'paragraph', 'paragraph', 'paragraph', 'table', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'heading_2', 'paragraph', 'paragraph', 'paragraph', 'heading_2', 'paragraph', 'divider', 'heading_1']
14     edited in place
15     table: 1 row(s) edited, 0 deleted, 0 added
16     table: 1 row(s) edited, 0 deleted, 0 added
17     table: 1 row(s) edited, 0 deleted, 0 added
18     table: 1 row(s) edited, 0 deleted, 0 added
19     edited in place
20     edited in place
21     edited in place
23     edited in place
24     edited in place
25     edited in place
26     edited in place
27     edited in place
28     table: 1 row(s) edited, 0 deleted, 0 added
29+30  replaced 1 block(s) ['paragraph'] with ['paragraph', 'heading_2', 'table', 'paragraph', 'paragraph']
31     edited in place
32     edited in place
33     edited in place
34     table: 1 row(s) edited, 0 deleted, 0 added
35     table: 1 row(s) edited, 0 deleted, 0 added
36     table: 1 row(s) edited, 0 deleted, 0 added
38     edited in place
40     edited in place
41     table: 1 row(s) edited, 0 deleted, 0 added
42     table: 1 row(s) edited, 0 deleted, 0 added
44     edited in place
45     edited in place
47     edited in place
48a    table: 1 row(s) edited, 0 deleted, 0 added
48b    table: 1 row(s) edited, 0 deleted, 0 added
49a    table: 1 row(s) edited, 0 deleted, 0 added
49b    table: 1 row(s) edited, 0 deleted, 0 added
51     edited in place
52     replaced 1 block(s) ['heading_1'] with ['heading_1', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'divider', 'heading_1']
53a    edited in place
53b    edited in place
59     edited in place
63     replaced 1 block(s) ['heading_1'] with ['heading_1', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'heading_2', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'divider', 'heading_1']
64a    table: 1 row(s) edited, 0 deleted, 0 added
64b    table: 1 row(s) edited, 0 deleted, 0 added
65     table: 1 row(s) edited, 0 deleted, 0 added
64c    table: 1 row(s) edited, 0 deleted, 0 added
66     replaced 1 block(s) ['paragraph'] with ['paragraph', 'paragraph']
67     replaced 1 block(s) ['paragraph'] with ['paragraph', 'paragraph']
68     edited in place
69     edited in place
70     edited in place
```

The tool's runs 1 and 2 read the plan before F14's last wording change ("Two inks for two roles."), which changes only item 52's new text. The cached run used the final `plan.json`.

Block operations, re-verified by GET after the fixes (`build_blockops.py`, reads only). All 29 operations and all 37 ids are OK:

```
3     OK   paragraph  cff508ae-9f55-4d87-b1da-5043ee052bd4
7     OK   paragraph  656c441b-e524-4ff9-a736-5f176f46648e
8     OK   paragraph  22307f63-b732-449c-b212-bca7887077af
9a    OK   paragraph  884b9420-a3f7-403f-928d-ea610089f6d0
9b    OK   paragraph  a6af102b-9188-4757-b7f5-155d23e9745d
10    OK   paragraph  d3b7ff5f-cf05-4374-8afe-8b957f8fa9aa
11a   OK   callout    ae8ca74f-495e-430e-930c-9650aeebe05c
11b   OK   paragraph  2094e810-05d4-4382-acc2-476b478ee7d6
12a   OK   callout    74001ca2-c3f1-4730-a5bc-47934892b289
12b   OK   paragraph  b2019093-6829-4de0-a7c7-bb4e9682c5fc
12b   OK   paragraph  2b7ad8b6-73d7-4871-8c27-1f811de1fdb9
12b   OK   paragraph  4cc44463-31a8-464c-b489-5bbfa3084777
12b   OK   paragraph  c1ef9eb9-df84-4cbe-9aa4-cb4a960df0c6
12b   OK   paragraph  b4bccd01-1443-487c-bf2a-1ade3c76c3a5
12b   OK   paragraph  10ff30e9-a56b-427f-b0e2-0b310d5f7eaa
22a   OK   callout    9ebe04db-8711-44de-b9f9-d4e6f499c505
22b   OK   callout    9ebe04db-8711-44de-b9f9-d4e6f499c505
22b   OK   paragraph  40517507-842c-47a0-a32d-08a5b97204cf
37    OK   callout    0392a06a-2f81-41cc-b371-4d16d44f84d3
39    OK   paragraph  41a241b2-efd8-41df-b3f0-5c93c267cd5c
43a   OK   callout    b62403c2-16d0-4795-8ae5-a42d14010f9f
43b   OK   paragraph  6d50c8f5-d891-4364-bcb6-0d796773d32e
43c   OK   paragraph  212d5d8f-8add-4ec4-9428-c98427e91380
46a   OK   callout    d472b253-8ffa-450e-8432-bd7e627f4661
46b   OK   paragraph  eaf051fd-8252-4ca3-aab0-8c139f24ad8c
50    OK   paragraph  ef81d04e-a7d1-4e07-9752-186de5cc0db7
54    OK   callout    e15aaeb3-9c74-4c79-9ccd-41f7df37277f
55    OK   paragraph  a9ea02c1-10e9-4368-9921-e69fdaa5479d
56    OK   paragraph  2d1476dd-09b6-4d81-bc0e-2b0a54890f9a
57    OK   paragraph  a93c8960-f47f-4e0c-b205-52fee1555e57
58    OK   callout    e15aaeb3-9c74-4c79-9ccd-41f7df37277f
58    OK   paragraph  a93c8960-f47f-4e0c-b205-52fee1555e57
60    OK   paragraph  1d026a6e-0d73-4f5c-b6f1-edc173dc6eec
61    OK   paragraph  bd4caa61-70bf-4a47-9784-142315bcdc62
62    OK   callout    56adda16-c6a9-4987-81f3-f0816d08940b
62    OK   paragraph  bd4caa61-70bf-4a47-9784-142315bcdc62
71    OK   paragraph  ea1256a0-51d4-4407-80bd-4baa115f9d3b
29 block operations
```

## Open conflicts to record (owed rows; the page stays as it is on each)

Every quote below was checked as an exact substring of its file.

- **T1. Draftcraft and the Crystal.** The Four Crafts: "Spellcraft, Runecraft and Chantcraft all require a Soul Crystal. **Draftcraft requires one only at the moment of manufacture.**" Against Alchemetrica (live): "*The Law of Alchemical Independence: alchemy requires no Soul Crystal, but remains bound to glyphs and vessels.*" and "A Crystal that never woke, **and works anyway.**"
- **T2. Heat with no instrument, against the Imperial Age's technology.** Alchemetrica: "There is no instrument. There has never been an instrument." · "heat is a craft skill rather than a specification" · "a master will name a temperature off the colour to within a hundred degrees". Against R53-01 (rules/doc-world-texture-law-2026-09-26.yaml, verbatim): "The Imperial Age runs from the 1800s into the middle of the 1900s, and the technology of that whole span exists across it". RULINGS.md calendar-2026-09-28: "The Imperial Age began in Year 690 IC. Its technology span (R53-01), rail included, begins then; the present, Year 715 IC, is its twenty-fifth year."
- **T3. Where the Whitening falls against the Wedding.** RULINGS.md (GW2): "The doctrine counts the stage where it completes". Against Codex I: "the first Wedding I watched" (after the Whitening, L139 to L141). Codex II: "his separating, his Whitening and his Wedding in their order".
- **T4. The decisive variable in a Draft.** The Magical Categories: "classed Spirit-aligned because the decisive variable is how cleanly the Essence Core's intention survives the journey into the crucible". The Four Crafts: "A Draft acts on the Essence Core, and a Class Ø soul has a Core like anyone else." Against Alchemetrica: "**Attraction Layer** · the decisive variable in advanced work."
- **T5. The Wellspring glosses against their Family pages.** Alchemetrica: "Binds and makes permanent" · "Reconfigures identity under catalytic force" · "Crystallises Essence into permanent mineral form". Against the Materia and Spatium Family pages (nucleation and Fixatio's irreversibility; change of basis; allotropy).
- **T6. The operations table's chains against their Wellsprings' attested glyphs.** Alchemetrica: "`Ur` `Ma` `Th`" (and `Ie Ur Flx`, `Xr Vael Ora`). Against the Master Glyph Index: [Plr] Pillar's primary Wellspring is Coagulatio; [Ora] Truth attests Sublimare, not Sublimatio.
- **T7. A pure alchemist's product: the maker's Grade against the bench Tier.** The Tier Ladders: "An enhanced weapon performs no higher than the Grade of whoever put the Essence into it" · "it is the maker's Grade at the time of making". VII. Aether Class: "No stat output above Hollow Grade is possible". Against the Tiered Path: "caps what its holder makes exactly as a tempered Tier does". This borders on C-123.
- **T8. A Master with no harmonisation.** The Tiered Path: "the web vibrates in recognition" · "Wellsprings and Titanic law answer them as co-authors". Against Alchemetrica: a Mechanica-trained practitioner at Master "has never once been recognised by anything".
- **T9. One word on three ladders.** Alchemetrica: "**Drafter** | Journeyman. Runs Coagulations alone". Against The Four Crafts: "a Drafter" (every Draftcraft practitioner). The Standing Index and the Tiered Path use Journeyman for Tier Three.
- **T10. Scribe's Wash against the correction of inscriptions.** Alchemetrica: "Engravers use it to correct a chain before the Sealing". Against The Alchemical Index: "correction is not correction. It is removal by Null-salt or Scribe's Wash, and both take the surrounding work with them".
- **T11. "Rupture" with three referents.** The Crossing: "This is the rupture". Against Alchemetrica's Conjunction Rupture and the Lexicon's Aether Shell Rupture.
- **T12. What produces Draft Corruption.** The Lexicon: "Law-fragments left by a working with a defective Direction role" · "a working that does not happen". Against Alchemetrica: "separates every signature present" (a Distillation without Direction, with no law-fragment) and the general structural-error account at L264.
- **T13. Four centuries or six.** Alchemetrica: "four centuries of practice" against "never been challenged in six centuries".
- **T14. Terms no other page carries.** Alchemetrica: "Paru's First Speech"; "Realm Rot" where the Lexicon's regional-loss word is "Hollowing"; "induced Parunic apertures".
- **T15. The Apparatus cites Alchemetrica for a claim it does not make.** The Apparatus of the Age: "The Alchemetrica classes both as alchemical products, which they are". Alchemetrica says nothing of plastics, and a bench-cured resin postdates the 1900 ceiling.
- **T16. Drafts under Wellsprings that no operation mirrors.** Alchemetrica L88, "Every Draft ever entered in the Standing Index is one of four operations or a composite of them", against the six-row table (Transmutatio, Fixatio, Materia Primordia, Dissolution with no verb-class of their own). F6 keeps the page from claiming otherwise.
- **T17. "Turn" in two senses.** The Sky, the Hour and the Year: "**The turn** is fourteen days". Against VII. Aether Class: "one turn" (a combat turn). Items 19, 20, 22, 32, 34, 36 and 45 now use the fourteen-day sense.

Rows already open and left clear by the page: C-117, C-123, C-124, C-125, C-127 (quotes as printed in CONFLICTS.md; the GL5 quote "Maker's mark and cutter's hand both trace De Raits, who needs both crafts." and the Trait System line "A fisherman weathered by forty years of cold water acquires a cold tolerance that will outperform an unspecialised practitioner three Stages above him." were re-checked as exact).

Seen in passing, and not this page's to fix: The Four Crafts prints its "He also gets no melt" and "The Accord has no category for this" paragraphs three times (Draftcraft section, :163 to :173).

Files: /tmp/wotr-drafts/alchemetrica/check.md, /tmp/wotr-drafts/alchemetrica/plan.json, /tmp/wotr-drafts/alchemetrica/blockops.json, /tmp/wotr-drafts/alchemetrica/changes.md, /tmp/wotr-drafts/alchemetrica/build_plan.py, /tmp/wotr-drafts/alchemetrica/build_blockops.py, /tmp/wotr-drafts/alchemetrica/dryrun_cached.py, /tmp/wotr-drafts/alchemetrica/dryrun.cached.txt, /tmp/wotr-drafts/alchemetrica/dryrun.part1.txt, /tmp/wotr-drafts/alchemetrica/dryrun.part2.txt, /tmp/wotr-drafts/alchemetrica/plan.tail.json