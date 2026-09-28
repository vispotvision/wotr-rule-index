# Author notes: The Farrant Papers (ME3, the rebuilt Corrant Papers)

Not part of the document. Draft: `/tmp/wotr-drafts/papers.md`. Written 2026-09-28 from `papers-brief.md` (source of truth), `papers-names.md`, `vol1/alftian-vol1-rules.md` (minus its "no IC" line, superseded by R63-1 to R63-3), the source `papers-source.md` (notes only, K10), and the PUBLISHED `vol1/alftian-codex-vol1.md` and `vol2/alftian-codex-vol2.md`. Revised the same day against five reviews (decisions, canon, voice, prose, continuity); the Review section below takes every finding in turn. Live lookups: The Night Watch; The Tier Ladders (the sites ladder, the Drafts ladder, "The Index and the ladder", "The unawakened"); On Walking Into the Current (Protocols III, IV, VI, VIII); The Eight Families (density scale in EU/m³); Mechanica: Extraction Without Recognition (§III, §V, §VI, Statute XXVI); The Crossing (the prohibition, the nine days); The Standing Index (Gravemark Ink row); The Alchemical Index (Gravetide Ink row); Alchemetrica (grain); The Sky, the Hour and the Year (fourteen hours of sixty counts); Kwon Mu-jin's card (Lore: the orchard, the Ashgate road); CONFLICTS C-119 to C-124; the Accord and Ketsuen Standing Inventories; the night-watch book bible. `check_docket` for documents, naming, character-sheet, magic-mechanism, worldbuilding, prose-law, stats, pov, register: 0 pending, 0 proposed.

## 0. Timeline as written

The case opens in the autumn of 700 IC, after Volume II's deposit, because Volume II's Appendix (written 700) still has the Weight standing still. Strom's activations begin in the summer of 700 (the Genesio clusters and the gate log both start then); Neros's first new step follows "late", in the autumn. The case closes at the hand-delivery in the late autumn of 701 IC. Volume III's platform then falls four months later, in the winter of 701 to 702 (ST4).

| Entry | Date on the page | IC |
|---|---|---|
| Frame, Preliminary Note | Maelor's day, the second turn of autumn, fourth division | 700 |
| First · Castlefall | Irath's day, early winter; arrival at the eleventh division, readings the next morning (seventh, eighth) | 700 |
| Second · the eastern lowlands | Maelor's day, midwinter | 700 to 701 |
| Third · the line, the University | Auren's day, late winter | 701 |
| Fourth · Genesio | Veyra's day, spring, after the thaw | 701 |
| Fifth · Urbis; Exhibit E arrives | Maelor's day, early summer | 701 |
| Sixth · Castlefall platform | Irath's day, late summer, the morning after the Urbis train | 701 |
| Seventh · the door; Closing Note | Auren's day, late autumn; release at the sixth division, the stair at the seventh | 701 |

Year stamps follow the published colophons: 700 IC is "the tenth year of the Imperial Age" and 701 IC "the eleventh". The brief's timeline column counts 690 as the 1st year, which would make 700 the 11th; that column is off by one against the colophons and was not used. The stamps now sit inside the Division's quoted stamp (frame head and archive line); the Society's own lines carry only day, season and division.

**Time units.** The Society counts in divisions (Guild hours, fourteen to the day, noon at the hinge between the seventh and the eighth). Sleep is now given in divisions (two to four, about three and a half to seven Earth hours), and the Genesio silence in breaths, because a count is a sixtieth of a Guild hour (about 1.7 minutes).

## 1. Counts and checks

- **Length.** verify.py counts **6,491 prose words** (set-piece band). The file has about **7,800 real words** (markdown tokens excluded); `wc -w` gives 7,909. That is about 300 over the brief's 7,500 ceiling; the overage is the review fixes (the bracelet kit line, the rung lines, the assay entered from the sheet, the Night Watch count line, the ranks by name). No canon-required line was cut to meet a budget.
- **build/verify.py `--band set-piece`, final run: `PASS: 0 fail, 0 warn`.** Info: filter verbs 3 (0.4 per 1,000); sentence mean 12.4 words, **CV 0.84**; paragraph CV 0.78; flat runs 0; chains 0; italics 0 (a field book; no NPC italic thoughts, R48-40). Last line: "On his stair I wrote the time: the seventh division."
- **Run history (this revision).** First run after the rewrite: `FAIL: 1 fail` (seven flat runs). The seven triples were listed with a local helper that reuses verify.py's own sentence splitter, each was re-cut by hand, and the next run was `PASS 0/0`. Two later reading-pass edits ("the distiller's words"; "climbed through three") each re-ran `PASS 0/0`.
- **build/codex.py check: CLEAN** (37 PASS, 15 Lists terms; 38 WARN by design, no bracketed glyph; 39 manual, no Spell Index row worked on the page).
- **Hand greps, all zero:** dashes; "week"; metre and kilometre; coal; steam; Malphas; The Mother; Zeraphine; Heresiology; Category with a number; Level; Enforcer; Research Archives; Voyager; Paracelsus; Noxinus; Gillus; De Raits; Vaughaus; Thom; Trismegistus; Vis; Rimward; Kaalabad; Geuk-hon; Frithia; Doyun; Ara; Sum-gol; T-numerals; "(sealed)"; "rather than"; "I record".
- **Hand greps with allowed hits:** "activation" once, in Draycott's mouth (WS5); "Tempus" once, as the Division's reference on Exhibit D (SE8); "Stage" once, read off a file; "Tier" only in the Division's clearance label; every question mark in dialogue; every contraction in speech, apart from Halveth's "don't".
- **"enter" and "entered":** down from 21 to 9. The one-word "Entered." lines are kept where she enters what she did not want to write (Strom's postscript, the letter she did not know of) and at Cassian's lie; "Entered as theirs" marks another's word; the slip keeps "I enter the slip". The registry's "is entered dead" and the bench's "entered me Class Ø" are the office's own verbs.
- **"finish" and "sentence":** Draycott's letter and his mouth own "finishing sentences" and "takes what it reads". Farrant's narration now uses her ledger words (an account left open, closing, business carried to its end); "sentence" appears in her narration only for a quoted sentence of Exhibit B.
- **Ketsuen recurrence:** E1 (who keeps your posts, cedar and sap, the Proving and the station record, the pressure, the practice stone); E4 ("On the record", the pressure); E6 (cedar and amber sap, the pressure).
- **Accord recurrence:** Preliminary (the hum, the gauge and the Board's seal, the bench's roll); E2 (the registry's entry in ink, the meter under the Board's seal by the Ault door, the assize hammer); E5 (the roll of marks, the meter at Neros's door); E7 (the tram on the conduit, the copper, the meter by the street door).

## 2. Which decision each entry serves (R5-C1: knew / wrongly believed / reader knows)

- **Frame head and Case File.** PA5 (the Society's filing line first, times to the division, the Division's stamp set off as a quote); PA2 (joint case, opened by Halveth, condition of access, not for the bulletin office); EC7 and tension 9.3; K1/R63 inside the Division's stamp. Exhibits A and B are "read at the Urbis desk under the Division's access; not copied to this file" (PA2 at the level of the file; see section 4, item 2). ST22 (Gameung-nok once), MJ7 (Thrice-Great on Exhibit C), ST4 (unopened), SE7, SE8. The treatise is "the Necrocursica, first manuscript, kept under seal below the gate" (ML7, ML8: the sealed edition does not yet exist).
- **Preliminary Note.** PA2 and ST14 (the desk, the letter of access, "not a report"); her reading of why, never confirmed. PA4: no roll took her as a child, and the chapter bench entered her Class Ø; the bracelet stated as kit ("the only warning I get"), so the platform and the door can be read. The file-naming rule, and the two volumes kept at the desk "for the same reason". SE7, SE9. Ends on an action (the file up the stair).
- **Entry the First.** SE1, SE3, tension 9.2 (the station record); R64-6 (Rill by the ladder's placement, gauge figure an estimate); EC3 (Calla, grain; "by her certificate" is her source for Calla's being unwoken); the copper on the sill, uncorrected; the lamp-drinking ink checked by eye; R62-6; the two tins (EC15); PA6/K7 (the Bond Trace "as the Codex reports it"); "Traces thin. The floor holds." The Not wanted line is an action: the distiller's words copied where she keeps the readings she cannot check.
  - *Knew:* the room, the Codex. *Wrongly believed:* that the thread runs through Furveus as a point. *Reader knows:* the bench drop is the Sealing ink.
- **Entry the Second.** ST12, ST13, EC12 ("one working, unentered", as vol2:171 has it); K2 Case III in Cassian's account; ST5 (the eleventh day, "Before the eleventh day was out", "in one breath"); PA6/ML8 ("the likeness"; "I do not use her name for it"); the nine days; the likeness poured "by Exhibit B's account" (no narrator mechanism, Table Rule 6); ST7, ST8. R65-2 as the stamp gives it; the coil reads only residue at its floor in the emptied glass (EC9: a finished Trace is spent). GL4 through the roll ("answers to Furveus on the roll; Exhibit B has him pour it"); GL12/R65-3 (the mark over the lute, the same as Exhibit C); Cassian's lie and its tell (Table Rule 8), now entered as two possibilities, not a mind-read. DE3. The grief shift to the assize, the payoff in three short sentences.
- **Entry the Third.** Source L173's order; GW9 (debt doctrine from Exhibit A, the gloss credited to Mu-jin from Exhibit B); WS3; the completion idea in her own words ("close an account its maker had left open"); ST6, EC6 (set against Exhibit A's description, no year count); the laugh on the page; the fee; EC12's order; Halveth "Seen; not referred."; DE7.
  - *Wrongly believed:* only two people knew the paper was there (Strom stood in the doorway).
- **Entry the Fourth.** SE3; the freight book (render stock attested; reserved ink; three winters); R64-8; ST17 (Dessa Mael: tea, the tightening, the fixed saying; she speaks the ink names only); ST2 (the Strom Submission, twelve years, one review); Draycott's Volume II line caught against the catalogue, with the postscript read correctly as Draycott passing on Strom's message; the joy shift ("Twice."); the Scribe's written refusal (ML5's title, "File me by the title"); EC15 (Gravetide the Boundary, Gravemark the Sealing, entered from the reference sheet: Adept rank of the Index, reserved at the Expert gate, the lawful-source shortfall; R47-7 ranks by name); WS4 in Dessa's mouth; Protocol III; WS2 (the gate Freshet, the hall Riptide per Exhibit A, not visited); the gate log climbing from midsummer where drawn ground should fall; Mechanica §V (coil against gauge); the lamps reported by Dessa, not seen; PA4's real risk (the hand, the taste, fifty breaths silent), Protocols VIII and VI; the struck line.
- **Entry the Fifth.** The anomaly returns "since the summer"; the Society's rule on bleeds, credited; the porter hole. Neros (the landlady and the warrant make the room the one she was not invited to); ST9, GW8, SE9, SE10 ("Entered as theirs"). EC10 (the roll confirms Draycott's mark; rank Expert). Her reasoning from her own sources (Exhibit B's Appendix, which does not know whether such a record can be woken; the freight book; Dessa Mael's saying); K2 Cases IV and V; GL8, GL9, Statute XXVI; "I have marked the extraction for it" and "Not yet."; MJ5; the ST14 twist.
- **Exhibit E.** ST3/MJ13 layered credit with no order in time between Madeleine's finding and Strom's ("The finding was hers before it was mine. Ivor found a crude half of it on his own, and the Archivum keeps it in a drawer at Genesio. The name is Kwon's. The framing is mine"); tension 9.9; GL3; EC9 ("Once finished, it is spent; the ground does not keep it twice."); WS4 and WS5; the source-keep lines; the lie; GW5 by name with the cure marked as Draycott's gloss ("I would add that it ends...").
- **Entry the Sixth.** The postscript's source entered as open (Exhibit B's fair copy went out before the seal; no recipient named, ML14/PA2). Protocol III; R64-7; ST7 (the silver first); R53-15 (the token belief now on the page). ST2/ST8's crude activations in Draycott's mouth ("Ivor woke things badly for ten years before he ever saw it done well"); GL7; "tolerable deviation"; the lie caught. The Pressure slip is written as observed effects only, dread first (R53-14), then the knee, sweat, the stomach, a carter down, a child crying; no Stage gap is claimed, because C-124 is open. The coil confirms it. The packet (hook 8).
- **Entry the Seventh.** K3; "By hand. Not by post."; MJ5 read as fact, with Exhibit B's count quoted exactly; the description of record against the card after the Ashgate road (the white left eye behind the lens, the right eye bound, the right arm hanging still in its sleeve, three fingers of the left hand bound and dark at the tips, one side of the chest still), silver first; no cause, Stage, Level or rank; MJ8's wound; ST4; hook 1.
- **Closing Note.** The Society's close line and count line; A and B stay with the Division's deposits; D, E, the statement, the packet held; the tins; pending clearances; Exhibit C released; "The investigation continues."; the archive line with the Division's stamp.

## 3. New in this piece (for ratification; also listed in "For Isaac to ratify")

See the final list. Items added in this revision: the chapter bench's Class Ø entry; the bracelet's kit line; the meter by the Ault door; Neros's landlady; Dessa Mael's two-word naming; the reference sheet's wording; the gate log from midsummer; "fifty breaths"; the Night Watch count and close lines; sleep in divisions; Draycott's "ten years" of crude waking.

## 4. Canon conflicts and tensions (recorded; the calls stand unless Isaac overturns them)

1. **The author's sex and given name.** The brief's CALL 22 makes the investigator a woman; the names file's chosen Niall Farrant is from the male pool and offers Orin Farrant as "the one-word swap if Isaac wants a woman." The page uses Orin. The decisions review notes that Orin Farrant / "O. Farrant" sits close to Oren Corrant / "O. Corrant" (one letter in the given name, a rhyme in the surname, the same initial). That is the Oren Corrant mould PA3 asks for, but it may read as a re-skin. Isaac's call (section 10). To swap: "Orin" and "O." in the frame, Exhibit E's direction and the closing note.
2. **"No file names Malphas" against ML4 and fixes.md** (tension 9.1, CONFLICTS owed; draft below). The page never writes the name. At the level of the file, Exhibits A and B name him (vol1:291 "Malphas's treatise, the Necrocursica"; vol2:197 "Malphas is my example, and I name him"; vol2:215 "Malphas's manuscript"; vol2:375 "A copy for Malphas"). The revision keeps both volumes at the Division's desk, "read ... and not copied to this file", and files only D and E, so the Papers' file carries no page with his name. The Scribe is filed by his title at his own written request.
3. **R65-10 against R61-13** (9.4, CONFLICTS owed; draft below). Draycott's letter carries the layered credit; Strom's half is now "on his own", with no order in time against Madeleine's, so the Papers do not settle Volume III's account either.
4. **GL5 against published Volume II** (9.8, CONFLICTS owed; draft below). The vessel's maker's mark answers to Furveus on the roll (her roll reading, since Exhibit B names no maker's mark and only has him pour and seal it); Draycott's registered mark sits in the consignor's wax over the lute. Related: the Gravemark reservation (Expert gate) and Furveus, who has no roster standing yet; the page asks and does not answer.
5. **Numbered Mortalis Categories** (9.11, CONFLICTS owed, low). None printed.
6. **Rungs for the inks and the vessel (R47-5, cc-05).** The Tier Ladders place a work by the EU one dose holds, and "The Index and the ladder" says the Index rank and the rung are two readings that neither corrects. Canon gives no held figure for Gravetide Ink, Gravemark Ink or the Ault vessel's Field Substrate, so no rung can be read off the spine without inventing a number. The page names what canon does give, by name: Gravemark's Index rank (Adept) and reservation (the Expert gate). The vessel's and both inks' rungs wait for a held figure; Volume III's cost stack (EC9, R61-100) is where the vessel's belongs. The sites carry their rungs: Castlefall Rill, the Genesio gate Freshet, the hall Riptide (Exhibit A, vol1:107). Gravetide's Index rank is not printed because its Alchemical Index row carries no rank on the wiki page; the auditors' "T4" (ae-01) is not a page reading.
7. **C-124 (Pressure with no Stage) and C-123 (grain against the Hollow cap)** are open. The platform beat claims no Stage gap: it gives the body's effects as she observed them and R53-14's dread, and the coil confirms. The card (section 6) must not print a grain Grade or a Pressure resistance until those rows are ruled.
8. **The Division's case references.** "the Eastern Commission" and "the Drift of Tempus" used; "the Genesio Activation Sequence" left out (WS5).
9. **The names file against the brief, where the brief won:** the delivery at Urbis on one lung (K3); "second bell" (CALL 20); the investigator a woman.
10. **Source timing against canon travel.** The line runs all day; Draycott writes "the morning after your train comes in from Urbis". E1's arrival is now at the eleventh division and its readings the next morning, for the same reason.
11. **Madeleine's death date.** The registry reads "the winter of 694"; both 694 and 694 to 695 fit Volume II's "two years ago" in 696.
12. **Clearance labels.** Exhibits A and B keep "(Hermetic Correspondence)"; the file is "(Mortalis Residue)" (CALL 9.3).
13. **C-119 to C-121** left open; nothing numeric or rank-named for Mu-jin reaches the page.
14. **The Volume III brief (forward risk, no change here).** The Exhibit E postscript is addressed to Farrant, who declines to carry it. Volume III should source Mu-jin's "He said so in the postscript" from Exhibit C's own postscript, never from Exhibit E.
15. **Exhibit B's count of midwinters.** Volume II says "two midwinters with the third coming on" at deposit in 700, for a letter received in the spring of 697. The page quotes it exactly as "his own count" and does not recount.

## 5. Every figure and its source

| Figure on the page | Source | Status |
|---|---|---|
| Castlefall gauge "seven and a little" | Eight Families (Ambient 0.1 to 10); Tier Ladders (Rill high and steady); R64-6 | estimate inside the band |
| Genesio reading floor and stair top "nine and a half" | Ambient's top; Vol I pressure | estimate |
| Passage-stair gate "twenty-one, climbing" | Active Concentration at its edge = Freshet; WS2 | estimate |
| Gate log: ten (midsummer), eleven (autumn), fifteen (midwinter), nineteen (thaw) | same bands; a proposal that the Archivum logs the gate | estimate / proposal |
| Riptide (the hall) | Exhibit A, vol1:107 | canon, cited |
| Coil readings | R62-6; Mechanica §V | no number, by design |
| Class II, Field Substrate; Sound; Marked | R65-2, as stamped; the coil reads only residue at its floor in the emptied glass | canon |
| Adept rank of the Index; reserved at the Expert gate; three lawful sources | The Standing Index, Gravemark Ink row ("T4", "reserved T5", "Lawful sources are three") | canon, ranks by name (R47-7) |
| Nine days | The Crossing | canon |
| Eleven days; "a turn at the outside" | ST5; Vol II | canon |
| Two years (death to likeness) | Vol II | canon |
| Three hundred gold marks, half and half | R65-2 | canon |
| About twelve years (Strom paper) | ST2; CALL 9.10 | derived |
| About six years older than the Necrocursica | 689 against 695 to 696 (ML7) | derived |
| Some eight years (paper to Draycott's first letter) | 689 to 697 | derived |
| Six years (the café to 701) | Vol I ch. 3 | derived |
| Ten years of crude waking (Draycott's mouth) | brief §4 planned line; ST2 "crude activations"; about 686 to 696 | proposal, a figure in a mouth |
| Three winters (Strom's ink; the freight book) | GL7 CALL | proposal |
| Ten winters (the platform) | Vol I | derived |
| Twenty-four (Mu-jin) | R62-1 | canon |
| About forty-six (Draycott) | Vol I "forty or so", plus six | derived |
| About sixty (Cassian); past sixty (Halveth); near fifty (Calla); past seventy (Dessa Mael) | source; brief | brief / proposal |
| Screened at seven; nineteen on the survey; eight years walking; twelve on the warrant | brief §1 | proposal |
| Fifty breaths (Dessa's count of the silence) | Protocol VIII; a count of breaths, not the Guild count | proposal |
| Sleep: two to four divisions | the Guild hour (about 1.7 Earth hours) | times only |
| Five stands (coil) | her procedure | proposal |
| Four works of the kind below the gate | source | source |
| Expert (Draycott on the roll) | EC10; FOW Part Five | derived, rank name only |
| One copper (coffee, tram) | Vol II; Accord Inventory | canon |
| Divisions (fourth to eleventh) | Night Watch clock | times only |
| Any EU, η, AU/s, Stage or Level for any person; any drift size; any rung for the vessel or the inks | forbidden or unsourced (PA4, SE10, C-119 to C-121, section 4 item 6) | none printed |

## 6. The author's sheet as the page implies it (for the PA1 card)

- **Name:** Orin Farrant (OR-in FARR-unt). Filing "Farrant, O., Urbis chapter, on the crown's warrant". Title Searcher. "Farrant" to Halveth and Draycott; "Searcher" to Calla, Cassian, Dessa Mael and Furveus.
- **As Of:** Urbis, late autumn 701 IC, the morning she carries Exhibit C up the stair. Age 42 (born 659). Concord human, Urbis native. Searcher, Urbis chapter, the Night Watch Society, on the crown's warrant; joint case with the Research and Archives Division, Urbis office.
- **FOW:** Class Ø (entered by the chapter bench; no screening roll took her); Crystal State Dormant; Shell sealed; no Stage, no Level, Hollow; no Wellsprings; no reserve or output. Path: grain only, and **no Grade printed for it while C-123 is open**. **No Pressure resistance printed while C-124 is open.**
  - Bodily marks on the page: the left hand that has run warm in dense ground since nineteen, uncalibrated; the Genesio onset (hand, taste, fifty breaths silent); the platform (dread, a knee, sweat, the stomach).
- **Kit shown:** pocket density gauge; field coil with scale card; loupe; Fixatio tins; chapter wax; the regulation bracelet (brass bands, grey wire) on the left wrist; field book; the crown's warrant; Halveth's letter of access. No silver token.
- **Voice as used:** pet word "entered" (nine uses, the one-word line kept for what she did not want to write); readings as fragments, time first; a Baseline line per entry; no contractions in the field book; one struck line; stress shift (the numbered order), grief shift (the assize), joy shift (the time twice); metaphors from the meter, the assize, the ledger and the tent poles. Refusal line: "I'll carry the paper. The man can carry himself."
- **Refuses** to carry another's words, and to write a name the file cannot carry. **Survived** the survey load at nineteen. **Believes and pays for it:** that the observer is not evidence.
- **Counterplay:** anyone who lets his weight go drops her; Spirit-type ground keeps its load in her; she carries no trace a follower can use ("nothing of you in the air"; PA4's "no signature to follow", card material).

## 7. Rule ids that most constrained the piece

- **R61:** R61-62, R61-63, R61-64, R61-65, R61-66; R61-12, R61-13, R61-14, R61-15, R61-99; R61-92, R61-94, R61-100, R61-108, R61-111, R61-114; R61-68, R61-69, R61-70, R61-74, R61-87; R61-106, R61-112, R61-117, R61-118, R61-120 to R61-124; R61-23, R61-24, R61-27, R61-49, R61-59.
- **Later rulings the same day:** R62-1, R62-5, R62-6; R63-1 to R63-3; R64-4, R64-6, R64-7, R64-8; R65-1 to R65-4, R65-6, R65-10.
- **NATALIE Table Rules** 5, 6, 8 and 11.
- **Craft law:** R47-5, R47-7; R48-06, R48-11, R48-40; R49-02, R49-13, R49-15, R49-26, R49-38, R49-40; R4-13, R4-14 (run, chain, clause cap, conjunction audit); R5-C1, R5-D, R5-G; R6-1; R52-03, R52-29; R53-14, R53-15, R53-30; R51-08, R51-10.

## 8. Real-world credits (R48-27; notes only)

- **Speaker type.** The Board of Trade railway inspector's accident field book, crossed with the Metropolitan detective's pocketbook of the 1860s.
- **The parish searchers of the dead** give the word "Searcher". The ropewalk is a real English building.
- **Practices borrowed:** the market assize and the sworn weigher's hammer test of a cased weight; the heliometer's split object-glass, from Volume II's own description.
- "Farrant" from Old French *ferrant*, iron-grey (names file).

## 9. Deviations from the brief (small; for Isaac to overrule)

1. **Given name Orin, not the names file's Niall** (section 4, item 1).
2. **Word budget.** About 7,800 real words against a 7,500 ceiling (section 1).
3. **The "Not wanted" labels are `###` subheadings.** They close E1 to E3.
4. **Halveth's "Twice." and "Seen; not referred."** "Twice." is the joy-shift margin the voice block asks for; "Seen" replaces the brief's "Entered", which is Farrant's word.
5. **Optional material cut for length:** SE12, the unnumbered primer, DE6 and Stillgate Ash, the bench by the iron gate.
6. **Cassian's boyhood phrase under grief** not used.
7. **The Codex's "nobleman"** never corrected; she uses his name.
8. **Neros's lodging, his landlady and the meter at his door** added (E5's room and the Accord recurrence).
9. **Exhibit E.** Draycott's want to see Kwon at Genesio stays as "I'll tell it to the one it's for"; the explicit invitation is Volume III's.
10. **Exhibits A and B not copied to the file** (section 4, item 2). The brief had them "held"; the file-level reading of "no file names Malphas" moves them to the Division's deposits.
11. **Mu-jin's description** follows the card after the Ashgate road, which overrides the brief's "right sleeve pinned empty" (section 4 guard: no account of the wounds is given).

## 10. Open questions (short; Isaac makes the calls)

- **Orin or Niall**, and whether Orin Farrant sits too close to Oren Corrant.
- **Furveus's Tier of Standing** against the Gravemark reservation (row 9.8).
- **Rungs for the Ault vessel, Gravetide Ink and Gravemark Ink** (section 4, item 6): each needs a held figure before R47-5 can be met.
- **The Archivum's gate log and the stopped brick-stand lamps**: proposals Volume III can confirm or drop.

## Review

Every finding from the five reviews, applied or rejected. Where two reviews made the same finding it is answered once and cross-referenced.

### Decisions review

1. ST3 / R65-10 broken by "before either of us". **Applied**: "Ivor found a crude half of it on his own, and the Archivum keeps it in a drawer at Genesio." "The finding was hers before it was mine" kept. Row 9.4 drafted below.
2. PA2 at the level of the file. **Applied** (both halves): Exhibits A and B are "read at the Urbis desk under the Division's access; not copied to this file"; the Preliminary Note gives the reason in one line; the Closing Note files only D and E and says A and B stay with the Division's deposits. Recorded in section 4, item 2, and in row 9.1.
3. Rungs (cc-05). **Applied in part.** Added "Exhibit A puts the hall at the passage's far end on Riptide ... I did not go down to it." The vessel's and the inks' rungs are **not printed**: the Tier Ladders place a work by held EU, canon gives none for any of the three, and inventing one breaks "never invent". Gravemark's Index rank and reservation are named by name. Recorded in section 4, item 6, and section 10.
4. R47-7, "the fifth Tier". **Applied**: "reserves it at the Expert gate", entered from the reference sheet.
5. Strom's crude activations missing. **Applied**: "Ivor woke things badly for ten years before he ever saw it done well," in Draycott's mouth on the platform (contracted speech register). "Ten years" is the brief's planned line, logged as a proposal.
6. False citation of a maker's mark in Exhibit B. **Applied**: "The maker's mark in the glass answers to Furveus on the roll. Exhibit B has him pour it." Row 9.8 drafted below.
7. Exhibit B's postscript misquoted. **Applied**: "the letter's postscript carries a message from Strom."
8. EC12 "unentered". **Applied**: "He paid for one working, unentered, done by a Master of the Circle".
9. EC9, a Trace is used once. **Applied** to Exhibit E: "Once finished, it is spent; the ground does not keep it twice."
10. The postscript inference misses the fair copy. **Applied**: "Exhibit B records a fair copy sent out before the seal. Somebody let him read one or the other." No recipient named (ML14, PA2).
11. The name too close to the cut one. **No change**, as the review allows; kept as an open question (section 4 item 1, section 10).

### Canon review

1. Maker's mark citation. **Applied** (see Decisions 6); the reading is now hers, against the roll.
2. "Fifty counts" is 85 minutes. **Applied**: "Fifty breaths. I counted."
3. "six years on from Exhibit A's" for Furveus. **Applied**: "set against Exhibit A's" (no count; the reviews disagreed between eight and nine, and none is needed).
4. Clusters "since the autumn" cannot precede an autumn step. **Applied**: "Since the summer they cluster"; the gate log now starts at midsummer (ten), and the climb is "through three".
5. The coil cannot read the grade of an empty vessel. **Applied**: "The grade is the stamp's. My coil gave residue at its floor inside the glass and nothing to set against the stamp."
6. E5 borrows Exhibit E's wording before it arrives. **Applied**: her reasoning now cites Exhibit B's Appendix ("does not know whether a record of that kind can be woken"), the freight book and Dessa Mael's saying; "finishing sentences" and "takes what it reads" are left to Draycott. No Halveth-leak clue intended, so no proposal.
7. "Residue thins ... This has climbed". **Applied**: "Ground that is drawn on should fall through a season. This has climbed through three."
8. The brick-stand lamps are in the corridor, not at the gate. **Applied**: reported by Dessa Mael, "in the corridor beyond", "I did not see them."
9. Line 461 midwinters; the P.S.'s cure unsourced. **Applied**: Exhibit B's count quoted exactly ("unanswered through two midwinters with the third coming on"); the cure marked "I would add that it ends ...".
10. Low points. **Applied**: sleep in divisions (two to four); "nothing stirred, so no roll took me. The chapter bench read me when I joined the Society and entered me Class Ø"; "By her certificate, she and I were the two in that room with nothing awake in us" (see Continuity 6).

### Voice review

1. Her lines borrow Draycott's wording. **Applied**: E3 "let the impression close an account its maker had left open when she stopped"; E5 "The dead's open accounts may be closing by the score" and "For carrying a dead woman's business to its end the law has no instrument yet."
2. Mu-jin's sentences in her narration. **Applied**: the carriage line recast ("The conduit hum came up through the bench into my back teeth, a note under the tram's"); "between two stations" cut; Neros's eye cut to what she saw, with "Exhibit B says he answers late. He did."; the rule "as Exhibit B has him do with a figure that will not come clean". "damp wool and warm brass" no longer appears on the page. R62-5 is a ban on coal boilers, so it is still honoured (no coal, no steam); the fixes.md carriage-smell line was a patch to the source's "coal smoke", which K10's rebuild no longer carries.
3. "I record it as theirs." **Applied**: "Entered as theirs."
4. Corrant's polish. **Applied** all five: "The registry has no such delicacy." cut; the pun recast ("has no reading to be argued with, and I set it down as a guess"); the coffee verdict removed ("I bought the coffee Exhibit B calls terrible at the stall by the tanner's, one copper."); "None of them wanted a journal." cut; "I compared them at every stand."
5. Frame in chancery style. **Applied**: the filing line leads; "Opened ... at the fourth division"; the Division's stamp set off as a quote carrying the classification and the year; the Closing Note has a Society close line with a division and a count line ("Entries: seven. Tins: two, chapter wax. Exhibits held in this file: two ..."); the release carries "sixth division".
6. Dessa Mael reads like the reference page. **Applied**: she says "Gravetide" and "Gravemark"; the definitions are entered from the reference sheet under her coil.
7. Draycott repeats himself. **Applied**: the P.S. opens "Tell him the second was not rhetorical."
8. "Enter" in other mouths. **Applied**: Halveth "Seen; not referred."; the Scribe "File me by the title."; her reply "Filed by its signature".
9. Furveus's laugh only described. **Applied**: the summary sentence cut; "He laughed, and then said, ...".
10. Kwon's silver last. **Applied**: "At his collar, a ranked man's silver token. Then the man:".
11. The Society's bleed rule as her aphorism. **Applied**: "The Society's rule for it: a bleed has no edge, and a boundary means somebody chose one."
12. "Enforcement takes extraction." staged. **Applied**: folded ("and I have marked the extraction for it").
13. "Withdrawal is not retreat". **Applied**: "The protocols count withdrawal as a step of the procedure. I took it."

### Prose review

1. Swappable with Draycott. **Applied** (Voice 1, Canon 6).
2. The bracelet unexplained. **Applied**: kit line in the Preliminary Note.
3. The token belief not stated. **Applied**: "a token being said to darken beside a lie."
4. Not-X-Y in Exhibit E. **Applied**: "I write because a letter can be read twice."; "What it keeps are records, as it keeps every other record, and there is no soul among them." (WS4's "no souls" kept without the pair).
5. Corrective pair and Ladder at l.199. **Applied**: the two sentences cut; the paragraph opens on "What happened in that house let the impression close an account ...".
6. Clause cap at the pressure beat. **Applied**: short sentences, and "The bracelet pulled again, hard. The weight went off me. I could stand."
7. The onset buries its hit. **Applied**: "It has run warm in dense ground since I was nineteen. Nobody ever calibrated it. I stayed."
8. Gloss. **Applied** all four: the Cassian summary cut; the stillness image cut to "His face went still."; the abstract restatement merged into one sentence with Case V's phrase; the maxim at l.77 cut.
9. Narrator mechanism at l.159. **Applied**: "poured, by Exhibit B's account, from ...".
10. The payoff sentence too long. **Applied**: "He paid three hundred gold marks for eleven days of his wife. What came rang dull. It was a courier." ("What came" for the review's "It", so the dull note belongs to the thing delivered, not the payment.)
11. Endings. **Applied**: the Preliminary ends "I took the file up the stair under my arm."; E1's Not wanted is an action; E6 ends "I took the down train."
12. World-only detail and flat runs. **Applied**: the meter under the Board's seal by the Ault door ticks once; all flat runs re-cut (verify reports none).
13. Setup, deadpan, button. **Applied** for the coffee. **"Twice." kept**: it is the brief's planned joy-shift device, and the review leaves it to Isaac.
14. Manufactured fragments. **Applied in part**: "He drank his wine then, the whole glass." **"Not by much. Enough." kept**: it is a brief Appendix A source-keep line and the Preliminary Note's hinge; with the wine line changed there is one such fragment on the page, which the review allows ("Keep one at most").
15. "Entered" overuse. **Applied**: 21 down to 9 (section 1).
16. Other minds and clarity. **Applied**: Cassian's mark as two possibilities; "as if to let a stranger stand in his doorway"; "I do not use her name for it."; the P.S. doubling cut.
17. Continuity. **Applied**: E1's baseline on arrival, readings next morning; "confirms the ring and three spokes as Gisli Draycott's"; the Entry Five room is Neros's, where his landlady let her in on the warrant (title kept).

### Continuity review

1. Mu-jin's right arm. **Applied**: "the right arm hanging still in its sleeve, the hand not moving".
2. The Ashgate wounds missing. **Applied**: the white left eye behind the lens; three fingers of the left hand bound and dark at the tips; he takes the letter between thumb and forefinger. No cause given. "He held it there a long while" replaces "He looked at the wax", since the card leaves open what the white eye sees.
3. "(sealed)" implies the sealed edition. **Applied**: "the Necrocursica, first manuscript, kept under seal below the gate"; the Scribe's "a text kept under seal"; the Closing Note's "access to the Necrocursica, first manuscript".
4. The credit line against R65-10. **Applied** (Decisions 1); row 9.4 drafted.
5. The Pressure beat settles C-124. **Applied**: the notes now cite C-124 as open and claim no Stage gap; the page adds R53-14's dread first and keeps the rest as observed. Section 6 carries C-123 and C-124 as bars on the card.
6. "the only two on this case". **Applied**: "By her certificate, she and I were the two in that room with nothing awake in us."
7. "he does not know whose mark it is". **Applied**: "Either he does not know whose mark it is, or he would rather I thought so. Entered, and not pressed."
8. The coil on an empty vessel. **Applied** (Canon 5).
9. The maker's mark citation. **Applied** (Decisions 6).
10. Furveus six years on. **Applied** (Canon 3).
11. "from up the line". **Applied**: "from down the line".
12. E1's clock. **Applied** (Prose 17).
13. The unattributed Codex gauge-housing sentence. **Applied**: "Gauge-housing on a post, Guild seal on its door. The hum dropped a note."
14. The postscript "from Strom". **Applied** (Decisions 7).
15. Exhibit E repeats itself. **Applied** (Voice 7).
16. Forward risk from Exhibit E's postscript. **No change to the Papers**, as the review says; recorded for the Volume III brief (section 4, item 14).
17. CONFLICTS rows owed. **Drafted below**; not written to the repo (this job writes only under /tmp/wotr-drafts/).

### Rejected findings

None rejected outright. Three were applied in part, with reasons given above: Decisions 3 (no rung invented for the vessel or the inks), Prose 13 ("Twice." kept as the brief's device) and Prose 14 ("Not by much. Enough." kept as the one allowed fragment).

## CONFLICTS rows owed (drafted; not written to the repo)

**C-1xx. "No file names Malphas" against ML4's signed Necrocursica and the Codex exhibits that name him** (tension 9.1)
**Rules:** `imports/drafts/alchemy-conversion/decisions.md` PA2 (R61-62) vs ML4 (R61-49) and `imports/drafts/alchemy-conversion/fixes.md` (The Papers)
**The clash:** PA2 binds the Papers to the night-watch book's rule that no file names Malphas. ML4 has Malphas sign the Necrocursica in his own name and says every Papers citation changes to it, and fixes.md re-points the old Papers lines at him by name. The published Codex volumes, which are the Papers' Exhibits A and B, name him outright, so a case file that holds them names him.
**Quotes:** decisions.md PA2: "the planned book's rule that no file names Malphas binds the Papers too." · R61-49: "Malphas signs the Necrocursica in his own name, Malphas." · decisions.md ML4: "every Codex and Papers citation changes." · fixes.md: "'Noxinus Ren' at L23, L41, L75, L175 and L255 becomes Malphas" · vol2 (Exhibit B): "Malphas is my example, and I name him" · vol2: "A fair copy of this volume goes to Malphas, who let me read his."
**Consequence if unresolved:** The Papers (and any Night Watch file after them) cannot both obey the rule and cite the Necrocursica by its author, and cannot hold the Codex volumes as exhibits without naming him.
**Draft's call:** the strict reading. No line names him; he is filed by his title at his own request; Exhibits A and B are read at the Division's desk and not copied to the file.
**Recommendation:** none.
**Status:** open

**C-1xx. Who found the Volitional Trace** (tension 9.4)
**Rules:** R65-10 (alftian-vol2-2026-09-28) vs R61-13 (alchemy-conversion-2026-09-28, ST3)
**The clash:** R65-10, the later ruling, gives the finding to Draycott. R61-13 gives it in layers: Madeleine found it and designed the commission, Strom found it independently, Draycott framed the theory and built the mechanism, Mu-jin named it.
**Quotes:** R65-10: "the finding is Draycott's, the name and its boundary are Mu-jin's." · R61-13: "Madeleine found it and designed the commission; Thom found it independently; Gillus framed the theory and built the mechanism; Mu-jin coined the name."
**Consequence if unresolved:** Draycott's letter in the Papers ("The finding was hers before it was mine") can be read as overruling R65-10, and Volume III's layered account has no single rule to follow.
**Draft's call:** R65-10 records the credit as Volume II gives it from Mu-jin's side; the Papers show R61-13's layers in Draycott's own words, with no order in time between Madeleine's finding and Strom's.
**Recommendation:** none.
**Status:** open

**C-1xx. Whose mark is on the Ault vessel, and who could write its Sealing** (tension 9.8)
**Rules:** R61-92 (GL5) vs the published Volume II (vol2:149, vol2:171) and The Standing Index (Gravemark Ink row)
**The clash:** GL5 says the maker's mark and the cutter's hand on a Category Three body both trace De Raits (Draycott). Volume II has Furveus pour the vessel and seal it with his own hand. The Castlefall bench drop is Gravemark Ink, which the Standing Index reserves at T5 (Expert), and Furveus has no Tier of Standing on any roster.
**Quotes:** R61-92: "Maker's mark and cutter's hand both trace De Raits, who needs both crafts." · vol2:171: "It was one working, unentered, done by a Master of the Circle who sealed it with his own hand." · vol2:149: "the vessel went out on the line in a crate packed with straw, with Furveus on one side of it and Strom on the other." · The Standing Index: "Gravemark Ink · T4 | IV / B / 44 · reserved T5".
**Consequence if unresolved:** The Papers must say whose mark is in the glass, and cannot say whether the hand that wrote the Sealing stood at its reservation.
**Draft's call:** the maker's mark answers to Furveus on the roll; Draycott's registered mark is the consignor's wax over the lute; GL5's full trace applies to bodies Draycott makes himself. The reservation question is asked on the page and left open.
**Recommendation:** none.
**Status:** open

**C-1xx. Numbered Mortalis Categories before the framework exists** (tension 9.11, low)
**Rules:** EC8 and EC10 (R61, the Category numbering) vs ST and ME's timeline (the Trace named in 700; the framework designed after Volume III)
**The clash:** The completion Category depends on a residue named only in 700, and Volume III has the framework designed afterward, so a 700 to 701 file cannot cite a Category numeral.
**Quotes:** R61-94 title: "Gravemark Ink seals Category Three" · Volume II Appendix (vol2:361): "I call it the Volitional Trace."
**Consequence if unresolved:** Any document dated before Volume III that numbers a Category contradicts the order in which the framework was made.
**Draft's call:** no Category numerals in the Papers; the law cited is Mechanica and Statute XXVI, and completion has "no instrument yet".
**Recommendation:** none.
**Status:** open

(Not a CONFLICTS row, a gap: rungs for the Ault vessel, Gravetide Ink and Gravemark Ink, section 4, item 6. C-123 and C-124 already exist and are cited, not re-filed.)

## For Isaac to ratify

1. **Orin Farrant** (OR-in FARR-unt), Searcher of the Night Watch Society, Urbis chapter, chapter house the Ropewalk, filing "Farrant, O."; a woman, born 659 IC in Urbis; given name Orin over the names file's Niall.
2. Her history: screened at seven, no roll took her; the chapter bench entered her Class Ø when she joined.
3. Her history: tally-clerk on a Guild survey party at nineteen; the left hand that has run warm in dense ground since, uncalibrated.
4. Her history: eight years on an Urbis walk, twelve on the crown's warrant, three cases in one line each.
5. Her mother, a sworn weigher at the Urbis market assize.
6. Her kit as shown, including the regulation bracelet (brass bands, grey wire) as "the only warning I get".
7. Her refusal line: "I'll carry the paper. The man can carry himself."
8. The Society's file-naming rule as she states it (subjects, witnesses, officers by name; everyone else by post or exhibit).
9. The Urbis chapter of the Night Watch Society and the Ropewalk chapter house.
10. The case references: "the Castlefall file" (the Watch's); "the Eastern Commission" and "the Drift of Tempus" (the Division's).
11. The packet's filing: "Volitional Trace · Genesio · active".
12. The Night Watch filing and count lines of the frame and Closing Note.
13. Halveth's letter of access, her description of record and her margins ("not a report ...", "and find Gisli Draycott", "You are on their record now", "Seen; not referred.", "Stop separating them.", "Twice.", "Keep this.", "Not yet.", "Good. Now write the report.", "He answered the letter.", "By hand. Not by post."); given initial K.
14. Exhibits A and B kept at the Division's desk and not copied to the file.
15. Exhibit C's route: care of the Urbis Archivum after the withdrawal, held unopened with papers touching the deposits.
16. The crown's warrant running in crown land only; in Ketsuen she can ask and cannot compel, and enters herself on the Castlefall station record.
17. Calla, distiller, of Castlefall: description, certificate (bench-certified, pure alchemy), the copper on the sill, "It feels like a room that hasn't finished with something."
18. The dyer's family in the flat above the tanner's.
19. The Castlefall evidence: the second ink drop by the wall and the two Fixatio tins under chapter wax.
20. The crown's registry in Urbis (land records; "In registro relatum") and the Division's copy of the registry's roll of marks.
21. Cassian Ault: description, "In every particular I was able to test", the cough on the first morning, "She asked after her books", the refusal, the lie ("It was a letter to me ... Concerning the two of us."), the cover sheet kept in a drawer.
22. The meter under the Board's seal by the Ault door.
23. The consignor's wax over the lute on a contracted lot (the practice behind row 9.8).
24. Furveus's lines: "Everyone who comes through that door reads me before they say good morning", "Ivor always stays", "Gisli finds people. Let him find you."
25. The Genesio waystation freight book entries (render stock attested; ink, reserved stock; three winters) and the pass-house above the waystation.
26. Dessa Mael's description of record and "He reads in the older hands when he comes in. He has not come in since the thaw."
27. The Strom Submission's review note as worded ("a residue of the dead not in the catalogue").
28. The Scribe's written refusal (text as on the page).
29. The Genesio Archivum's assay of the two inks, Dessa Mael of record, and the reference sheet's wording as entered.
30. The Archivum's gate log (read once a turn: ten, eleven, fifteen, nineteen) and all gauge estimates on the page.
31. The brick-stand lamps stopped at midwinter (reported by Dessa Mael).
32. Farrant's onset at the stair: fifty breaths silent, the taste, the struck line.
33. The Division's anomaly returns and the Bureau's wording ("Wellspring bleed, Anamnesis, no operator indicated").
34. Neros's lodging near the Monastery's platform, his landlady, the meter at his door, ink on the right thumb.
35. Draycott's rank on the roll (Expert) and his three-years-stale address.
36. Draycott's letter, Exhibit E, in full (including "Once finished, it is spent; the ground does not keep it twice." and the P.S.'s gloss).
37. Draycott's description six years on (thin at the crown, a close-cut coat, the signet worn smoother).
38. Draycott's platform lines: "Things people died meaning to do", "He's doing good", "Ivor woke things badly for ten years before he ever saw it done well", "You're restful to stand beside ... There's nothing of you in the air", "I'll tell it to the one it's for".
39. Where Strom is: the hollow below the archive-town by night, a pass-house above the waystation by day.
40. The chapter's coil-carrier at the platform (a role), and the carters' Weight-bred argument.
41. The platform slip as written (dread, one knee, a carter down, a child crying; the coil's needle), pending C-124.
42. Mu-jin's Urbis lodging above the square with an east window, and the three-line exchange at the door.
43. His description at the door as read from the card (no cause given).
