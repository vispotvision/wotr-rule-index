# Author notes: The Necrocursica, sealed edition (Malphas)

Not part of the document. Draft: `/home/oridon/wotr-drafts/necrocursica.md`. Written 2026-09-28 from `necro-brief.md` (governing), `necro-names.md` and `necro-voice.md`, checked against Isaac's four answers (RULINGS.md "necrocursica-calls-2026-09-28"), decisions.md ML1 to ML15, the R61 to R68 rulings dated 2026-09-28, the published Volumes I, II and III and The Farrant Papers, Malphas's card (living loadout and Lore), The Crossing, Vitalia (Mortalis), The Heresiology (Cases II to V), the Alchemetrica "Dead at the Bench" draft (`alchemetrica/changes.md` item 52), The Real Alchemy (Calomel; White arsenic), the Arena scene (the Zettari archives), CONFLICTS C-125, C-127 and C-128, and the Volume I rules digest (minus its IC line). **Corrected in review:** `necro-source.md` is present at `/home/oridon/wotr-drafts/necro-source.md` (12:10, before the first draft); the first draft wrongly recorded it absent and ran from the brief's account. The revision checked the front matter, the preface, Category Three, the platform scene and the closing chapter against it (see Review, R-19).

**A gap in the groundwork.** The brief says its "Critic section" and "stratum table E" govern, and cites Critic 1, 2, 3, 6, 7, 9, 10, 11, 13 and 21. **Neither the section nor the table is in the file** (both copies end at §9, line 456). The stratum table below is rebuilt from the brief's §3 ("Critic 1 amends this"), §7 (beats and the register rule), necro-voice §4, and RULINGS "necrocursica-calls" item 4. Where a Critic number is cited inline in the brief, its content was applied as the brief states it.

## 0. The frame call

- First manuscript: winter 694–695 IC to spring 696 IC, at Genesio, at Invocation; brought down and read at the Castlefall table late autumn 696 (Vol II).
- Sealed edition: written at Genesio in 703 IC "by order", sealed at the thaw of 704 IC; stamped "Year 704 IC, the Withering Era; the fourteenth year of the Imperial Age" (brief §1; R63). It cites Volume III (deposited start of winter 702) and the Farrant file (closed late autumn 701).
- Margins: undated on the page; by the brief's call, 704 to after Greyshaft Nine (706), before the Becoming.
- Mu-jin's note: 704 by the brief's call; undated on the page; opens on the four-month echo.
- Reader's copy: made for Halveth's office ("H."), undated, after the last margin.

## 1. Counts and checks

- **Length (after review).** `wc -w` **9,228** (target 9,000 to 10,000). verify.py counts **8,398 prose words**; the difference is headings and the `>` blocks (stamps, epigraph, the five margins, the two "entered" lines, the struck block and Mu-jin's note).
- **build/verify.py `--band set-piece`, final run after review:** `PASS: 0 fail, 0 warn`. Info: one '-ing' opener; filter verbs 2 (0.2 per 1,000); flat runs 0; sentence mean 13.0, **CV 0.71** (target 0.80; info only; Volume III shipped at 0.73); paragraph CV 0.71; short sentences 37%; last line the end stamp.
- **Run history.** Draft 1: `FAIL: 1 fail, 1 warn` (25 flat runs; one paragraph closing long-long-long), 8,359 words. Runs located with a sentence-length script (`scratchpad/flat.py`, imports verify's own splitter); rhythm rewrite plus about 850 words added (preface, the order of reading in Chapter the First, a battlefield paragraph in Category Two, one case each under the Mirror Trace, the Worn Habit and the Incomplete Sealing, Chapter the Sixth's night-sitting paragraph, Appendix II's side-by-side line). Draft 2: PASS, 1 flat run. Draft 3: PASS, 2 flat runs (info), both merged. Final: PASS, 0 flat runs. Review revision: first run `FAIL: 1 fail` (7 flat runs, all introduced by the review edits: Category One's Direction sentence, Category Three's warnings, Chapter the Fifth's head-notes, the Incomplete Sealing's carried-lines line, Appendix I's new head sentence); broken by merges and one shortened sentence; second run PASS with 2 flat runs (info); third and final run PASS, 0 flat runs.
- **build/codex.py check:** `CLEAN`. Check 37 PASS (24 Lists terms). Check 38 PASS: five glyph tokens ([Ie], [Ur], [Flx], [Tp], [Vor]), all in the Master Glyph Index; [Au] Death is not written on the page. Check 39 (manual): **no Spell Index row exists** for any Mortalis Category (EC8 owes them); the text writes the Category One chain from GL1 and GL2 and the Category Three seal from GL3, GL5 and GL7, so each is the source the rows will derive from, not a duplicate.
- **build/codex.py check (after review):** `CLEAN` (37 PASS, 38 PASS, 39 manual as before).
- **voice_check (Malphas, 8-line fingerprint; first draft):** preface bargain line, 30 words, z = −0.1; margin E, 14 words, z = −0.9 (margins run short by design; necro-voice §3).
- **Hand greps above the end stamp:** zero em or en dashes; no "?" anywhere (he never asks); contractions only inside Draycott's and Furveus's quoted speech ("You're", "don't", "won't"); no "week", month or day names, metres; no "rather than", "not merely", "not so much", "less X than", "which is to say"; no R51-10 word; "echo" only as a WOTR term (Noospheric, Parunic, Lawful, held Echo); no "ledger", "sovereign", "weave"; no "Heresiology", "Grade V", "Excepted", "Fermentation" (after review), no ordinal for any Unmooring,, "Cacodaemonic", "unmoored" (the Drift band's participle), "Mother", "Zeraphine", "Pyraeon", "Academy", "Greyshaft", "Thrice-Great", "Gameung-nok", "Monastery", "Nospheric", "Level". "Kwon" appears only as "Kwon Mu-jin" (twelve times after review: first mention in each part, the signature, the transcriber's note and the cross-references; "Mu-jin" after). Category Four is never called impossible or possible.
- **Margins:** five, 68 words in all after review (the brief's ceiling is 70): E 14, F 10, A 16, B 10, C 18. None addresses a reader, none is answered by the core text, none contains "I" or "mine".

## 2. The strata (rebuilt; see the gap above; corrected in review)

| Stratum | Register | Passages |
|---|---|---|
| **First manuscript, 695–696** (candour, at Invocation) | Sincere, confessional, dry; ponds allowed | Epigraph; the preface entire except its entered sentence (the mocked title, from Volume I ch. 4's line, is 696); the Proem's opening paragraphs (Still Gate, Aphorism, Equilibration, the three products, the nine days) except the gloss line; Chapter the Second's three after-window paragraphs (Imprint, Bond Trace, Parunic Echo); the warning sentences in Category Three ("Do not animate a vessel you cannot seal before you sleep" to "the working I am most afraid of"), in the vessel method's own terms, with no Trace vocabulary; the Incomplete Sealing's warning ("Do not leave the last glyph for the morning" to "when a hand stops"); the Averted Regard's confession (the ponds, "I have wanted to know", "treat this document as a confession"); the Misnaming's "I have been told that my own earlier writing carries this"; Chapter the Sixth entire except its entered line, recast in review to the three after-window residues ("the tone they laid into the walls", "the thread that runs from them to whoever grieves", "the mark of every working they made"; "other people's habits and other people's grief") |
| **Sealed edition, 703** (command) | Law then application; no new confession; "I" only as the one who orders, cuts or corrects | Title page; On This Edition; the preface's entered sentence; the Proem's Sublimatio paragraph and the legal-sense lines; Chapters the First, Third and Fourth (residues, credit as a citation of Volume III, order of reading, Tria Prima modified, the Categories and their costs); **Chapter the Second's "Those three paragraphs are the first manuscript's, unchanged" paragraph (moved here in review; the first draft filed it as 696)**, "This edition adds" and "Every record"; the frame sentences that introduce carried text ("I wrote the first manuscript's method before I had seen it done... They stand here beside what replaced it."; "The first manuscript's lines follow."; "I put my own case under this head"); every frame, case, marker and driver line of the Seven Unmoorings, including the stage-current paragraph moved into Chapter the Fifth; the platform recollection, flat, with "I did not go to him" cut in review (see R-19); Chapter the Sixth's entered line; Appendix I; Appendix II (one joy shift at its close) |
| **Margins, later hand** | Command, cooled; the Greyshaft voice | A (Incomplete Sealing), B (Averted Regard), C (Misnaming, now naming the breach: "may say she"), E (Category Three, beside Strom's name), F (Category Four, liches, reworded in review) |
| **Kwon Mu-jin** | Volume III's voice, no apology | One note beside the struck completion steps ("I did not go up", corrected in review) |
| **The Division** | Chancery-plain | Transcriber's note; the struck block's line; the stamps; "H." |

## 3. Which decision each part serves

- **Title page:** K8, ML4, ML5, ML7, EC7, ME1, RULINGS calls item 2 (Tier VI; clearance runs upward), R63.
- **Transcriber's Note:** EC14, ML8, ML9, ST14 ("H."), SE7 (the house line is in the colophon).
- **Epigraph:** ML1, ML13 (necro-voice §5's trimmed wording), signed Malphas (ML4; Critic 6 as the brief states it).
- **On This Edition:** ML7, ML8 (the cut hidden in "Nothing the art requires has been withdrawn"), K7, K8, calls item 1 ("as they bind wherever a circle has signed"; nobody named as drawing or numbering them), calls item 4 (the warnings gathered under new heads), "by order" with no one named (tension 18).
- **Preface:** ML1, ML2 (the bargain), ML3 (the second visitor withheld), ML5 (the imposed title and its mockery, in Volume I ch. 4's own words: "It is a very long name for a man who copies"; added in review), R65-5 (the hand bound in linen, the binder unnamed; instrument undescribed; healed-hand sentence entered in 703; "Between them they held my left hand" cut in review, see §5), Volume I (the bench by the gate, the worn seal, the key on a cord, the thaw, "laughed at Neros's charts", "slept through"), Volume II ("Someone would have written it... with the warning in it"), fourteen months.
- **Proem:** WS3, the Crossing (three products, nine days, "what remains is meat", Trait tissue), Vitalia (Equilibration, quoted in substance), GW9 (Aphorism; gloss credited to Mu-jin), K5, K6, DE7.
- **Chapter the First:** K7, DE1, DE2 (Stage stretches by days, and only by days), DE3, ST21, ST3 and R66-1 (after review, a citation: "as the third volume of Kwon Mu-jin's Codex gives it", then R66-1's four clauses in its own wording, "Kwon Mu-jin" shortened to "Mu-jin" at second mention), MJ13, necro-voice §7 (the ruling on Mu-jin's word).
- **Chapter the Second:** K7, GL10, R62-6 (floor; Mechanica residue never thins), DE3, WS4, EC9, the Papers' quoted Bond Trace sentence kept verbatim.
- **Chapter the Third:** GW4 (canon map stated first, his triad declared modified), DE6, EC11, ST6.
- **Chapter the Fourth:** EC7 to EC10, EC13 (costs as behaviour, no figures; after review, the share of reserve tied to Stage by the law of reserves, with no figure: "a heavier share of a Refraction reserve than of a Realization one"), EC14, GL1 to GL3, GL5 to GL7, GL9, DE4, DE5, EC1, EC2, EC12, R62-7, R62-8, ML11, ML12, ML14, ML8, MJ11 (Mu-jin credited with nothing but the name and the gloss), WS2 and Volume III (Whirlpool to Riptide, the scar, the gauge 26 to 20), SE8 and SE10 (the Weight as debt booked, no EU figure), Volume III (Neros's column), the Papers (Draycott's "closes on Return when the sentence is finished" matched: "ends when the Trace's decision is delivered"; "ended in one breath").
- **Chapter the Fifth:** K8, calls item 3 (the seven names, in that order), GW5 (named, never numbered), GW6 (Volume III's four epithets, exactly as printed), WS1 and K5 (the stage currents, Cinerion and Sublimare, moved here in review from the Proem, where an unmooring names its driver; the Proem keeps only the Sublimatio line K5 says stands), GL6, GL7, GL8 (after review: "the donor is dead", and the regional breach), DE1, ST21, ML9, fixes F3, F5, F12, F16, F20.
- **Chapter the Sixth:** K8 (the verb), ML1, ML13, ST6 (Furveus's line, recast without the Anamnetic fabric: WS5; its second half recast in review to clear R49-40), necro-voice §5 ("I wrote the entire text with myself in mind"; "you come back out").
- **Appendix I:** EC14, EC11, EC15, GL3, GL7, ST6, EC2, EC6, F8 (Preparation Failure: "goes volatile, and it stays volatile"), the Papers (the pair sentence verbatim; withdrawal as a step; after review, a head sentence saying the pair and the withdrawal passed from Furveus's protocol into the field's protocols, so the 701 Papers can quote them), Volume II (Furveus's hand no longer writes small).
- **Appendix II:** GW5 (Separation Perverted first, then the Misnaming in part, then the general scholarly corruption as his opinion), MJ5, GW7 (the vow quoted from Volume III, answered by refusal), ML6, Volume III ("A copy for Malphas... with a letter asking him what he thinks"; "I have written to ask"; "I asked for the Scribe" on the reading floor, and the passes "opened a turn before"; "I named it in myself in the second volume"; the hand worse).
- **Cross-references and colophon:** ME3, PA6 (the Papers cited, not read), MJ8, MJ13, Volume III (the Submission's title and annotations, verbatim), ML15 (the Zettari archives, the Arena's own words), EC7, SE7.

## 4. New in this piece (to be ratified)

1. The transcriber's head-note and the struck block's line ("Struck under redaction. Preservable under redaction. H.").
2. The edition note's wording, including "This edition was made by order" and "with two additions".
3. The preface's additions: the first morning below the gate (drier air, old glue, cold stone, shelves past the lamp); reading by day and writing by night with the jar of Uplands herbs; Draycott coming up "whenever the passes let a mule through" and asking for nothing to be changed; "I let them be glad without telling them the cause".
4. Chapter the First's order of reading (Shell from the threshold with the coil low, held Echo from the doorway, Corporeal Residue with a hand on the slab, Trace last; write each down before the next).
5. The fixed saying "A melted coin does not testify." (necro-voice §3's choice, used once).
6. Chapter the Second's 703 line "A mourner's grief is the thread's living end, and it is the thread the commissions pull." (the first draft's stove and "how many people would one day want to pull on it" cut in review).
7. Chapter the Third's village remedy (dead packed in snow or carried to a cold room), left uncorrected ("They are right, and the body does not care why."; R53 folk beliefs).
8. Category One's four-line forensic return and "It gives no cause of death. That is the physician's."
9. Category Two's battlefield paragraph (drawn from The Crossing's battlefield section, recast as containment worth doing only before the pooling, "Afterward there is nothing to contain", so it never reads as a treatment) and its withdrawal counter.
10. The Boundary rule "paced from the body outward to where the gauge falls back to the room's own reading" (**replaces a number**: the brief's F2 call wanted paces; no figure exists, so the perimeter is a procedure) with the brief's term "one day and a night, or until sealed" (brief call, originated).
11. The five margin lines as worded after review (A 16 words, B 10, C 18, E 14, F 10; 68 in all). C now names its breach ("A master may say she"); F reads "One dead thing stays itself: the lich. Not treated here."
12. The cases: the Mirror Trace (the reader and the shipwright's yard; she struck the separator at the second sitting; a season finishing nothing); the Worn Habit (two Archivum cases; the wife's request; "took his tea the way the dead man of that house had taken it, and would sit in no other chair"); the Incomplete Sealing (Gravemark cut by half with lampblack; the table laid for four, then five); Appendix I's report (standing at the window, asking for a door opened; the rune under the left heel; ended in the fourth division of the night in one breath; the ring-stander grey for a season).
13. The Unmoorings' marker lines where the brief gave none (the Mirror Trace's one tone where two should sound; the Worn Habit's kitchen memory; the Incomplete Sealing's fixed-hour habit (a place laid, a door gone to); the Averted Regard's preference reported as a finding; the False Vocation's uncharged Trace) and the Averted Regard's resolution ("Other people reach it... if they refuse to be read as residue").
14. Appendix I's medicine step: white arsenic 1/10 grain three times a day in pill for a turn ("A bottle of them holds several deaths"); calomel five grains once, never with salt meat or brine, since it turns "partly corrosive". Doses from The Real Alchemy (Wood and Bache 1870).
15. Appendix II's lines: "I leave that where Draycott left it"; "I have sworn nothing myself, and I will not answer a vow with an opinion"; the spring of 702, the reading floor, and "I did not come up"; "It is still the better book."
16. Chapter the Sixth's night-sitting paragraph ("I have never once been bored").
17. The Zettari archives as the second sealed copy's home (ML15, the brief's call, in the Arena's own words).

## 5. Canon conflicts and tensions (recorded; none resolved)

- **C-125 (open).** The title page carries "By Malphas, Scribe to the Genesio Archivum, by order", and every signature reads Malphas (ML4). The preface now also mocks the title (ML5). The text writes nothing addressing the Watch's no-name rule. Not resolved.
- **C-127 (open).** The text states the lawful formula (Gravetide Boundary; Mortalis seal in Gravemark; Expert gate) and the tracing principle (maker's mark, cutter's hand) and never assigns the Ault commission's hands. After review the personal liability reads "the Master of the Circle who seals it" (EC12, R61-111: "the rank that seals"); it names no hand, so C-127 stays open.
- **NEW, owed (drafted below as C-154): DE4 against EC10.** The page says both "Completion is a Greater Summons" (DE4) and "Floor: Refraction, the seventh Stage" (EC10). Not resolved; the text states both rulings as they stand.
- **C-128 (ruled, calls item 1).** The Categories are numbered here in words and stated as binding wherever a circle has signed; nobody is named as drawing or first numbering them. **Flag for Isaac:** the Alchemetrica draft's note on item 52 reads C-128 as "the Categories are unnumbered in the late texts"; this text numbers them, as the brief, the ruling's wording ("No document names who... first numbered them") and ML11's "Category Four" require. If Isaac meant "never numbered anywhere", every head in Chapter the Fourth changes.
- **ML11 against The Crossing.** Category Four: "The Accord does not authorise it, and it will not." Never impossible, never possible. The text is unreliable exactly here; no Category Four mechanic is written.
- **The drivers (a disagreement between groundwork files; changed in review).** The names file (necro-names §1) maps the Averted Regard to "Fermentation Perverted, the Corruption of Catastrophic Germination"; the brief (§7) says "Driver: none named (**Call**: it is Mortalis's own failure, not a stage inverted)", and GW2 (R61-80) keeps Fermentation as "Background for his margins only". Fermentation is also Malphas's own canon corruption (ML2), so naming it as the driver of the case he confesses as his own is a new confession in the 703 driver lines (ML13). The review set the driver to "None. No stage of the Work turned against itself drives it." on GW2 and ML13; the Critic section that would settle the file disagreement is missing. The other five mappings stand as the names file gives them (Mirror Trace: Submission; Incomplete Sealing: Non-Commitment; Open Shell: Instrumental Union; Misnaming: Conviction; False Vocation: Tyrannous Finality; Worn Habit: none). Distillation Perverted (Sanitized Truth) is named by no case: the treatise commits it (the cut footnote). **For Isaac:** Fermentation or none for the Averted Regard; and whether the False Vocation keeps Tyrannous Finality or goes to the brief's "none, and he says why".
- **"Lawfully".** The brief's Category Three line "This is what Gisli Draycott did lawfully" would call the private, unentered, paid commission (EC12) lawful. Written instead: "the working Gisli Draycott built the means for".
- **The hand (corrected in review).** The first draft kept "Between them they held my left hand", and these notes wrongly said the preface "names neither": with Draycott named as one of "them", it answered Volume III ch. 22's open question ("I asked him whether he was one of the two who held Malphas's hand at Genesio... 'Ask Malphas'... I have written to ask"), which Mu-jin could not have asked in 702 had he read it in the 696 preface, and which Appendix II refuses ("I leave that where Draycott left it"). The source's clause ("their method of persuasion left an impression on his left hand", necro-source.md title block) is not carried. The preface now reads "My left hand was bound in linen through that first winter, and the binding was changed by a man who did not know how." Draycott stays named as a visitor (ST7); ML3 (the mark is the second visitor's) stays off the page.
- **Draycott's line against R49-40.** necro-voice.md fixes "'You haven't given them up,' Draycott said. 'You're avoiding them.'" as canon wording; R49-40-NOT_X_Y ("any pair where the second sentence corrects the first fails") is live law and outranks the groundwork. The line is cut to "'You're avoiding them,' Draycott said." (his contraction kept).
- **"Two volumes walked around the obvious"** (brief §7's Appendix II beat, from the source) contradicts Volume II's own self-naming ("Separation Perverted. Recognised in myself.") and Malphas's Volume II margin; cut in review. The charge now falls on the first volume, and on the second only until its page on Separation.
- **The Critic section's absence** (top of these notes; see Review, R-14).

### CONFLICTS row owed (drafted; not written to the repo)

> **C-154 · Category Three's floor against the tier of a Greater Summons.** Source A: DE4, R61-75-IMPRESSION_BODY_GREATER_SUMMONS (live): "A Greater Summons: vessel, Animatria and Vocatia together. Canon's Tier III (Stage IX to XI, 'ancestral echoes'): Arts vessel, the maker's Core as identity, Vocatia contact with the Trace." With it, The Spirit Summoning Arts: "| **III · Greater Summons** | Vocatia + Animatria + Arts | Stage IX – XI | Minutes to hours |". Source B: EC10, R61-109-MORTALIS_CATEGORY_STAGE_FLOORS (live): "Flourishing, Glory, then Refraction with individual review... Category Three sits where the Necrocursica says Trace-compulsion begins. Gillus stands at the floor, lawful by rank and unlawful only by review." The clash: an impression-body is a Tier III working (Stage IX to XI), but the Category that makes it floors at Stage VII, and Draycott at VII is said to stand at that floor. Related text, recorded and not applied: the same Summoning page's Temperance Gate line, "Stage VII (Refraction) for material-anchored constructs · Stage IX (Invocation) for independent Spirit Forge bodies". Where it shows: the Necrocursica, Category Three ("Floor: Refraction, the seventh Stage"; "Completion is a Greater Summons."). Status: open.

The canon reviewer's alternative (describe the build by its parts, "The body is built as a summons is built: a poured vessel, the maker's own Core, Vocatia", and drop the tier name until ruled) is ready if the ruling goes to EC10. It was not applied now because it would drop DE4's live wording from the page, which would be deciding the clash in EC10's favour.

## 6. Every figure and its source

| Figure | Source |
|---|---|
| Winter of 694 to 695 IC (corrected in review to agree with necrocursica-calls item 4, "the first manuscript of 695 to 696 IC"), 696 IC spring, fourteen months | brief §1 (source preface's "fourteen months") |
| 703 IC written, 704 IC sealed, "fourteenth year of the Imperial Age" | brief §1; R63-2 (Age begins 690) |
| Nine days; Stage stretches by days | The Crossing; DE2 |
| Lawful Echo, Class II; Class IV Trait carry | The Crossing |
| Stage floors Flourishing (IV), Glory (VI), Refraction (VII); Adept, Expert, Expert with review; Journeyman gate for Stillgate Ash | EC10, EC11 |
| Clearance Tier VI (treatise), Tier IV (Appendix I) | EC7; calls item 2 |
| Gauge 26 at the thaw of 702 (Dessa Mael's turn reading), 20 on the morning after the last Trace in the hall was spent (corrected in review); Whirlpool to Riptide | Volume III ch. 21 ("At the thaw it stood at twenty-six"; "The next morning Dessa Mael read the gate out of her turn, and the gauge had fallen to twenty") |
| Gravemark: Adept rank, Expert gate, three lawful sources | The Standing Index; the Papers |
| "Several thousand bodies... in one hour"; pits on "the twelfth" | The Crossing (battlefield section) |
| Eleven days, one breath (implied, not restated as eleven) | ST5; the Papers |
| Two years (reconstruction) | K7; R65-2 |
| White arsenic 1/10 grain three times a day; calomel five grains | The Real Alchemy (Wood and Bache 1870) |
| "Thirteen years" (not used); Mu-jin at Genesio in the spring of 702, the passes "opened a turn before"; asked for the Scribe on the reading floor | Volume III ch. 21 |
| Refraction (VII) and Realization (X) as the two reserves compared in the cost paragraph | Stage names R20C-30 (Fracture of Worlds); the law of reserves (a share of reserve is as large as the reserve makes it) |

No figure of any named person (Stage, Level, EU) is on the page (R62-2; brief §1). No reserve share is given as a number. **Corrected in review:** the first draft said no law closes EC13 (brief tension 16); the law of reserves does close its direction, since a reserve grows with Stage, so the text now says the same working is a heavier share of a Refraction reserve than of a Realization one and that the practitioner at a Category's floor pays most. No figure is derived, because no working's absolute cost is set anywhere.

## 7. Stat Ledger

None. Malphas's living loadout (card IV) is withheld by design: he suppresses his field, and the treatise prices Categories, not its author.

## 8. Workings on the page: Phenomenon lines

- **Mortalis (Proem):** Still Gate; real phenomenon: a dissipative structure held far from equilibrium; death as the end of expenditure. Failure: Equilibration (Vitalia). Wellspring Mortalis, Vitalia; Auren.
- **Category One:** Authorization [Ie], Direction [Ur] (draws nothing), Sealing [Flx] sealed by [Tp] on a Fixatio chain; Gravetide Boundary. Fault: an improvised Direction draws, the first step to the Open Shell.
- **Category Three:** Greater Summons (Draft vessel, Animatria identity as Eidolon, Vocatia contact); Mortalis seal in Gravemark closing on [Vor] Return. Fault: short ink (Incomplete Sealing); the Attraction Layer read in at the Authorization (Mirror Trace). Real lens: sublimation and fractional distillation for the Sublimare separations (The Real Alchemy).
- **Anamnesis:** thermal resetting (thermoluminescence of fired ceramic); a read spends the record.
- **The Open Shell:** Mechanica; Statute XXVI; coil and gauge discrepancy as the measure.

## 9. Rule ids that most constrained the piece

R61-53 (ML8) and R65-4 (the footnote verbatim), R61-49/50 (ML4, ML5), R61-54/57/59 (ML9, ML12, ML14), R61-56 (ML11), R61-8 (K8) with necrocursica-calls items 3 and 4, R66-1, R61-12 (ST2, the completion method after 697), R61-75 and R61-109 (DE4, EC10; C-154 owed), R61-80 (GW2), R61-83 (GW5, no ordinals), R61-95 (GL8), R61-111 (EC12), R61-112 (EC13), R49-40-NOT_X_Y, R49-26 (endings), R49-18 (competing comparisons), R4-14-RUN_RULE, R52-04 (no contractions), R51-10, R63-1 to R63-3.

## 10. Real-world credits (notes only)

Paracelsus (tria prima, spagyria, the dose makes the poison); Lemery's *Cours de chymie* (sublimation); Wood and Bache, *Dispensatory* (1870) for the arsenic and calomel doses and calomel's conversion with salt; Le Roy, Teilhard de Chardin and Vernadsky (noosphere, behind "Noospheric"); thermoluminescence dating (Anamnesis); flax retting (the ponds; the card's Lore); Alfred Swaine Taylor's forensic manual and Wellington's dispatches as the register models for the command voice (necro-voice §3).

## 11. Checks against the Heresiology (K2)

- **Case II** ("The warning survived as a footnote"): true. The footnote is cut from the sealed text and survives only in Mu-jin's note; the preface still claims "with the warning in it".
- **Case III** (the Eastern Commission): unnamed; "the likeness" never used with her name; "the commission the fourth chapter touches".
- **Case IV** (the Genesio Activation Sequence; "arrives crowned with achievements"): Strom named as running it at scale; margin E hints the chain was made by another hand.
- **Case V** (the Drift of Tempus): the Weight's steps after clusters of wakings, booked as debt.
- The Heresiology itself, its Grade V and its list name are never cited.

## 12. Reading pass (prose-law-quickcheck)

- Ladder: one near-case removed ("is identity, and the identity is the maker's own").
- Correction pairs removed by hand before the checker saw them: "does not replace his direction. It borrows it"; "The body does not fail. It grows"; "does not go inert; it goes volatile"; "It was not written for anyone... It is only what" (a countdown into "only").
- Gloss (after review): "A melted coin does not testify." folded into the Corporeal Residue paragraph in place of the abstract clause; "One verb serves all seven. The work unmoors them.", "The dose is the point.", "It is about its author as well." and "This is what it is to work honestly with what remains." cut. "Short ink makes a short seal." kept as his verdict line (his idiom, one-line paragraphs, per the voice block's "stumble" and "fixed saying").
- Questions: none anywhere.
- Endings (after review): Chapter the First ends on "Practitioners come apart at the joins between the four." (the signpost cut); Chapter the Third on "So has one who reads the Mercury and calls it the person." (the summary moral cut); Chapter the Sixth on "And then, if the seal holds, you come back out." with no moral before it; the text closes on the stamp.
- Correction pairs cut in review (R49-40): the Proem's hole ("and the hole stays open after the construct is destroyed. / It closes when the residue diffuses."); the revenant ("It has habits and a direction, and nothing that weighs them."); the False Vocation ("The peace was a man..."); Furveus's line ("Be afraid of the living who won't look at them."); Draycott's line (§5). Countdowns eased: "by days, and only by days"; "It has no Bench and no review."
- Residue grammar (the Misnaming's own rule, kept by the main text after review): Sulphur "the part that points"; the Mirror Trace "what the Trace is charged toward"; the Incomplete Sealing's marker a habit at a fixed hour. Only margin C and the household's reported "more like her" break it.
- Swap test: the margins against the core warnings they sit beside (same vocabulary, warmth gone); Mu-jin's note against Malphas (Mu-jin confesses by fact and judges once; Malphas never does); Draycott's single spoken line, four words with his contraction; Malphas never takes over Mu-jin's framing (the credit line is now a citation, not Volume III's own sentence).
- Mother tells, recognisable and unnamed: growth under a sealed lid (margin A beside the Incomplete Sealing); names chosen for the file (margin C); the Open Shell's region and the Mechanica discrepancy; the Boundary as edge.

## 13. Deviations from the brief (small; Isaac may overrule)

1. Order of the front matter follows the brief (title page, transcriber's note, epigraph, On This Edition, preface). The task's summary listed On This Edition before the epigraph; the brief governs.
2. Five drivers from necro-names §1; the Averted Regard's set to none in review, as the brief's §7 and GW2 give it (§5).
3. "Built the means for" in place of "did lawfully" (§5).
4. The perimeter as a procedure, no pace count (§4 item 10).
5. Chapter heads: the brief's six chapters kept; names-file heads used where they agree.
6. Margin D skipped, as the brief allowed; five margins, not six (the epigraph is first-manuscript, per the brief's §3 table).
7. Mu-jin's note reads "at our table in Castlefall" (Volume II has the shared flat's table) in place of "at its author's table".
8. Chapter the Sixth's closing kept necro-voice §5's "I wrote the entire text with myself in mind" and cut the sentence before it instead, which satisfies the Gloss finding and the voice file.
9. The stage currents (Cinerion, Sublimare) moved from the Proem to Chapter the Fifth's head-note (WS1: "Use only where an unmooring names its driving corruption"); the Proem keeps the Sublimatio line (K5).

## 14. Open questions

1. Should the absent Critic section and stratum table E be restored to `necro-brief.md`, so the rebuilt stratum table (§2, corrected in review) can be checked against Isaac's actual table?
3. The Averted Regard's driver: none (as now written; brief §7, GW2, ML13) or Fermentation Perverted (necro-names §1)? And the False Vocation: Tyrannous Finality (as written) or none?
4. C-154 (DE4 against EC10): which governs Category Three's floor, or does the Summoning page's "Stage VII (Refraction) for material-anchored constructs" reconcile them?
2. C-128's reading: numbered in the Necrocursica (as written) or never numbered (the Alchemetrica draft's note)?

## Review (five reviewers: decisions, canon, voice, prose, continuity; applied 2026-09-28)

Tags: D = decisions, C = canon, V = voice, P = prose, K = continuity. Where two reviewers flagged the same line, one fix answers both.

**Applied**

- **R-1 · Category Three's first-manuscript warnings (D1, C3, K3).** The frame no longer dates the completion method to 695–696 (ST2, R61-12; Volume II ch. 9, "There is a fourth. Malphas does not describe it"). Now: "I wrote the first manuscript's method before I had seen it done, and these sentences stood beside it at the same table. They stand here beside what replaced it." The carried warnings use the vessel method's own verb, "Do not animate a vessel you cannot seal before you sleep... Do not animate one for the mourner... Do not animate one in which you hold a stake." The Continuum-at-the-Authorization clause is cut from the 696 lines; the 703 text already states it ("That is the door the Mirror Trace comes through"). Mu-jin's note: "A footnote stood under the method these steps grew from. This is its place."
- **R-2 · ML5's mockery (D2).** Preface: "They gave me a title to sign under as well: Scribe to the Genesio Archivum, by order. It is a very long name for a man who copies." (Volume I ch. 4's line.)
- **R-3 · The Averted Regard's heads (D3, V3, P3, K6).** "The Averted Regard's confession stands as the first manuscript wrote it, under a head that is new, like the other six." The 703 sentence "It is the first of the seven that fails in the one who works" is cut. "I put my own case under this head" states placement, not confession.
- **R-4 · Chapter the Second's look-back (D4, V4, P12, K7, C13).** Now "Those three paragraphs are the first manuscript's, unchanged. A mourner's grief is the thread's living end, and it is the thread the commissions pull." Filed as 703 in §2.
- **R-5 · GL8 (D5, C11, P11).** "It draws finished output from a donor's Crystal, and the donor is dead. The law files that as extraction, which is Mechanica. Statute XXVI says why the boundary stays open: closing needs a warrant, and a working with no Authorization to answer to never had one." This is reworded away from Farrant's sentence in the Papers, which Malphas has not read (PA6). Added to the Resolution: "Of the seven it is the one whose harm does not stay in the room: the ground it opens runs on across a region."
- **R-6 · EC12 (D6, C12).** "the Master of the Circle who seals it, personally." C-127 stays open.
- **R-7 · DE4 against EC10 (D7, C1).** Recorded, not resolved. See §5 and the drafted C-154. The text keeps both rulings. The canon reviewer's parts-only wording is held ready (rejection note below).
- **R-8 · EC13 (D8).** Added to Chapter the Fourth: "A reserve grows with Stage, so the same working is a heavier share of a Refraction reserve than of a Realization one, and the practitioner standing at a Category's floor pays most for it."
- **R-9 · The case count (D9, C6, P4).** "Of the seven I have seen three, and a fourth once, at a distance I kept. One I have from the Archivum's records, and the Misnaming from my own pages." The Averted Regard's confession is the seventh. The three seen are the Mirror Trace (brought to him), the Incomplete Sealing and the Open Shell. "At the bench" is dropped because the Mirror Trace came by her partner.
- **R-10 · Ordinals (D10, P2).** "That is the door the Mirror Trace comes through." The head-note now names the cases: "Four fail in the working: the Mirror Trace, the Worn Habit, the Incomplete Sealing and the Open Shell. The Averted Regard and the False Vocation fail in the one who works. The Misnaming fails in everyone he teaches." That also clears the contradiction with "It afflicts the field and spares the man who starts it."
- **R-11 · Dates (D11).** "the winter of 694 to 695" in On This Edition and the Preface.
- **R-12 · The lich margin (D12, C16).** Now reads *One dead thing stays itself: the lich. Not treated here.* The decisions wording was taken, as it carries no legal "save" or "excepted".
- **R-13 · The credit line (D13, V2).** "The credit stands in layers, as the third volume of Kwon Mu-jin's Codex gives it: Madeleine Ault found it and designed the commission, Ivor Strom found it independently, Gisli Draycott framed the theory and built the mechanism, and Mu-jin named it and set its boundary." These are R66-1's clauses. "Mu-jin" is used at second mention, per brief §5.
- **R-14 · The missing stratum table (D14, V gap).** This cannot be fixed from here. The table in §2 is rebuilt again with the review's corrections, and restoring table E is Open question 1.
- **R-15 · The Proem's stage paragraph (C2, P10).** "Every cure in the fifth chapter is Sublimare-aligned" is cut as false. The Sublimatio line stays in the Proem (K5) behind a lead-in. The Cinerion and Sublimare currents move to Chapter the Fifth's head-note (WS1), ending on "The separation and the cleanse below are Sublimare-aligned."
- **R-16 · Anamnesis spend (C4).** "A careful reading takes a little. A coarse one takes all of it, and leaves nothing for a second." This matches Volume III ch. 23.
- **R-17 · The Shell's window (C7).** "it is the first thing to read, since of what a reader can still find it goes soonest"; the order of reading says "the soonest to go".
- **R-18 · The gauge and the arrival (C8, C10, K5).** The gauge reads "twenty on the morning after the last Trace in the hall was spent". Appendix II: "He came to Genesio in the spring of 702, when the passes had opened, and asked for me on the reading floor. I did not come up."
- **R-19 · Process: the source (C19, K9).** necro-source.md exists. The notes' header is corrected. Checked against it:
  - The source's "Gillus De Raits said... 'You have not retired. You are avoiding.'" is the root of Draycott's line (see R-27).
  - Its title-page clause ("their method of persuasion left an impression on his left hand") is the source of "between them"; it is not carried (R-22).
  - Its platform scene (:365 to :373, "I did not approach him that day. I wrote this chapter instead.") sits in the Seventh Corruption, which call item 4 would allow as first-manuscript text. It stays 703 and flat because its frame (the Continuum presenting Traces) is Trace-era and cannot be 696. The rueful "I did not go to him" is cut (P12).
  - Its Chapter the Fourth has "other people's unfinished wanting". It is recast (R-21) because "unfinished wanting" is the Trace's grammar.
- **R-20 · Appendix II on the corruption (C9, V10, K1).**
  - "The third volume returns to his own corruption, Separation Perverted... which he named in himself in the second." "What that corruption withholds" replaces "forbids".
  - The general-corruption paragraph now reads: "The first volume of the Codex did it. The second did it with me, by name, for its Submission. It was accurate about me, and about him as well, and then it turned, on the page on Separation. The third does not do it at all."
  - "Two volumes walked around the obvious" is cut. "I think" and the second "exact" are gone (V9).
- **R-21 · Chapter the Sixth's residues (C3, K4).** "It holds the tone they laid into the walls by living against them, the thread that runs from them to whoever grieves, and the mark of every working they made." Also: "other people's habits and other people's grief do not replace your own."
- **R-22 · The hand (K2).** "Between them they held my left hand" is cut. The preface now reads "My left hand was bound in linen through that first winter, and the binding was changed by a man who did not know how." (§5)
- **R-23 · Appendix I and the Papers (K8).** Added: "The pair and the withdrawal passed from it into the field's protocols long ago, and are printed here as the field keeps them. The ash, the rune and the medicine are his; the Boundary and the sealing are my modifications."
- **R-24 · The medicine (C17).**
  - "three times a day in pill" (The Real Alchemy: "in pill, usually with opium"; opium is left out)
  - "A bottle of them holds several deaths" (ten to forty-five tenth-grain pills is a fatal dose)
  - "turn partly corrosive"
  - "The dose is the point." is cut (P6).
- **R-25 · Folk belief (C18).** "They are right, and the body does not care why."
- **R-26 · Containment (C14).** "...and it is only worth doing before the pooling. Afterward there is nothing to contain."
- **R-27 · Correction pairs (P1).** Five were cut or recast (§12). Draycott's line becomes "'You're avoiding them,' Draycott said." (§5).
- **R-28 · Held Echo (C15).** "Read a held Echo from the doorway, and do not stand in its room longer than the reading."
- **R-29 · Residue grammar (V1).** Changed: "the part that points"; "What the Trace is charged toward"; the Incomplete Sealing's marker "A habit kept at a fixed hour that nobody poured into it: a place laid, a door gone to, the same hour each day." The Open Shell's "wants a warrant" also became "needs".
- **R-30 · Mu-jin's direction (V5).** "I did not go up to read it for four months."
- **R-31 · No stumble on a word (V6).** "By the third chapter I had stopped counting it as compulsion."
- **R-32 · One "most afraid" (V7, P13).** Category Three keeps it. The Incomplete Sealing now ends "what this method makes possible when a hand stops."
- **R-33 · The formula said once (V8).** Category Three keeps the "I wrote..." frame. The Incomplete Sealing reads "The first manuscript's lines follow." Chapter the Second is handled by R-4.
- **R-34 · The outside tags (V11).** The forearms-on-knees clause and "courteously" are cut.
- **R-35 · Naming slips (V12, P9).** "The second volume of Mu-jin's Codex"; "he is thriving".
- **R-36 · Margin C (V13).** Now reads *The rule is for students. A master may say she, and the file is built on his word.* The margins total 68 words.
- **R-37 · Gloss and endings (P5, P6, P7, P14).** The following were cut:
  - "All seven begin with a practitioner who forgot it."
  - "One verb serves all seven. The work unmoors them."
  - "It is about its author as well."
  - "This is what it is to work honestly with what remains."
  - "Each head of the fifth chapter sits on one of them."

  "A melted coin does not testify." is folded into its paragraph. "You find yourself in it" becomes "You find yourself in what remains", since the sentence that gave "it" its referent is gone.
- **R-38 · Comparisons (P8).** "It sounds like vocation." is cut. Now: "I first entered it in my notes as something close to sanctity. The entry is corrected here. The peace was a man..."
- **R-39 · Countdowns (P15).** "by days, and only by days"; "It has no Bench and no review."
- **R-40 · The Worn Habit's tea (P16).** "took his tea the way the dead man of that house had taken it, and would sit in no other chair."
- **R-41 · Gravetide clause (P17).** "draw it in Gravetide Ink, whose line a residual field can be assayed against."

**Rejected or adjusted, with reasons**

- **V14 (move margin E beside the "stake" warning).** Not moved. The brief places margin E beside Strom's name, so that one line serves ML9 and ML14. The stake warning is now a 696 line in the vessel's terms, and a 703 margin about Genesio's chain beside it would date the chain to the vessel era.
- **C1's page fix (drop "Greater Summons").** Not applied. That would remove DE4's live wording, which decides the clash in EC10's favour. Decisions D7 says the text can stand, provided the clash is recorded. It is recorded (C-154, drafted), and the parts-only wording is ready.
- **C5 (the Averted Regard's driver).** Applied as "None" rather than kept as a disagreement on the page, because GW2 (R61-80) is a ruling ("Background for his margins only") and outranks the names file. The file disagreement still goes to Isaac (Open question 3).
- **P1's Draycott alternative ("keep and log").** Recast instead. R49-40 is live law and necro-voice.md is groundwork.
- **V3 on "Read this chapter back to me from its head".** Kept as 696. The first manuscript had chapters, and "its head" is the chapter's opening, not a case head.
- **K7's "keep 'I have changed nothing in them'".** Voice V4's plainer 703 wording was taken instead: "Those three paragraphs are the first manuscript's, unchanged."
- **P10's destination (Chapter the Fourth).** The stage currents went to Chapter the Fifth instead. WS1 says to use them only where an unmooring names its driver.
- **P13's wording ("is what I have made possible, and I know it").** Not used. V7's wording was taken, since P13's is a fresh confession in a 696 line that already has one superlative.
- **P4's "The Misnaming needs no case; every student is one".** Not used. The Misnaming's source is his own pages, which is D9's and C6's reading and agrees with the 696 "I have been told that my own earlier writing carries this."

**After review:**
- `build/verify.py --band set-piece`: PASS, 0 fail, 0 warn, 0 flat runs, CV 0.71 (info).
- `build/codex.py check`: CLEAN.
- Hand greps are clean:
  - no dashes or "?"
  - no Unmooring ordinal
  - no "Fermentation", "Excepted", "Level", "Cacodaemon", "Monastery" or "Mother"
  - contractions only in Draycott's and Furveus's speech
- Reading pass done a second time, whole.

## For Isaac to ratify

1. The sealed edition as written: 703 IC by order, sealed at the thaw of 704 IC, Tier VI, the Accord's redacted copy made for Halveth's office; the first manuscript begun in the winter of 694 to 695 IC.
2. The front matter order and the transcriber's note, with the struck block's line.
3. The preface as revised: the mocked title in Volume I's words; Draycott's line cut to "You're avoiding them"; the first morning below the gate; Draycott reading and asking for nothing changed; the hand bound in linen with no binder named; the entered healed-hand sentence.
4. The strata as rebuilt in §2, pending table E (Open question 1).
5. The four residues' order of reading and the four-line forensic return.
6. The Categories' costs, tells and counters as written: the Boundary procedure and the term "one day and a night, or until sealed"; the reserve share by Stage without figures; containment only before the pooling; the liability on "the Master of the Circle who seals it".
7. C-154 (DE4 against EC10), drafted in §5, to be entered in CONFLICTS.md and ruled.
8. The drivers: five as the names file gives them, the Averted Regard none, the Worn Habit none, and Sanitized Truth left to the cut footnote (Open question 3).
9. The case tally ("three, and a fourth once... One I have from the Archivum's records, and the Misnaming from my own pages") and the head-note sorting the seven into the working, the one who works, and everyone he teaches.
10. The cases: the shipwright's yard; the two Worn Habit records ("would sit in no other chair"); the lampblack-cut seal and the fifth place laid; Appendix I's report.
11. The Open Shell's regional-breach line and the reworded Mechanica passage.
12. The five margins as worded (68 words), including C's "A master may say she" and F's "One dead thing stays itself: the lich. Not treated here."
13. Mu-jin's note as worded ("I did not go up"; "A footnote stood under the method these steps grew from. This is its place.").
14. Appendix I's head sentence (the pair and the withdrawal passed into the field's protocols), the medicine step and the doses.
15. Appendix II's answer: Separation Perverted, named in himself in the second volume; the Misnaming in part; the vow unanswered; the general corruption charged to the first volume and to the second until its Separation page; the spring of 702, the reading floor, "I did not come up"; "It is still the better book."
16. The second sealed copy in the Zettari archives.
17. The fixed saying "A melted coin does not testify."


## Lead's pass after review

- The Averted Regard's driver set to Fermentation Perverted, the Corruption of Catastrophic Germination ("the rot valued for its yield"), per the groundwork critic's ruling that the names file governs drivers (A.4) and ML2 (Submission first, then Fermentation Perverted as his own corruption). The brief's "none" is overruled.
- Stratum table E recovered from the session transcript and compared with the rebuilt strata in §2: they agree passage by passage.
- The owed row on the Greater Summons tier against Category Three's floor is filed as CONFLICTS C-154 (open).
