# Author notes: The Alftian Codex, Volume the First (Kwon Mu-jin edition)

Not part of the document. Draft: `/tmp/wotr-drafts/alftian-codex-vol1.md`. Written 2026-09-28 from `alftian-vol1-brief.md`, `alftian-vol1-names.md`, `alftian-vol1-rules.md`, the source text, `decisions.md` (131 answers), RULINGS.md (alchemy-conversion, open-conflicts and calendar entries of 2026-09-28), fixes.md, Mu-jin's, Ara's and Malphas's cards, and live lookups (`codex`, `wiki`, `scene_context`, `voice_check`, the Tier Ladders, FOW VII Part Nineteen, Alchemetrica, the Heresiology, the Gate, the Sky page, the Ketsuen and Accord inventories, the Descent of Parun, the Colour of Essence, The Crossing).

## 1. Counts and checks

- **Length.** verify.py counts **8,155 prose words** after the review revision (set-piece band; the brief's target is 6,000 to 8,000, so the volume runs 2% over; the growth is the review's additions: the derived Riptide cost, two lens-off figures, five world-only details, the apologies for correcting, the ride's motive). The whole file is 8,785 words; the difference is the three Tablet recitations, the epigraph and the colophon, set as `>` blocks (quoted and archival text, not his prose), plus headings.
- **build/verify.py `--band set-piece`, final run after review:** `PASS: 0 fail, 0 warn`. Info: 1 '-ing'/'As' opener; filter verbs 13 (1.7 per 1,000); flat runs 0; sentence mean 15.7 words, CV 0.72 (target 0.80; under 0.50 is the warn line); paragraph CV 0.71; italics 0; last line "A coffin at Genesio. I have not asked." (the colophon block is not measured).
- **Run history:** draft 1 FAIL (chain of three >25-word sentences; 20 flat runs; 10,391 prose words). Draft 2 FAIL (18 flat runs). Draft 3 FAIL (chain). Draft 4 FAIL (4 flat runs). Then PASS with 1 warn (a paragraph closing on three >18-word sentences, fixed), then PASS clean through every later edit. Review revision: first run FAIL (two chains of three >25-word sentences in the night ride and at Venur's door; 7 flat runs), second run PASS with 2 flat runs, then PASS with 0 flat runs. No single-pass delivery.
- **build/codex.py check (after review):** CLEAN. Check 37 PASS (26 controlled terms). Check 38 PASS (7 glyph tokens, all in the Master Glyph Index). Check 39 (manual precedent): no Spell Index row is worked on the page; the only chains are the Fixatio seal link, Furveus's mediation glyphs and the amulet, none a named spell, so nothing is new, derived or duplicate.
- **--culture Ketsuen** has no effect in verify.py; counted by hand (section 7).
- **voice_check (pre-review):** Ara's "That's asking" line z = +0.4 against her 14-line fingerprint (the line is now shorter and ends on her question); Malphas's title line z = −0.3 against his 8-line fingerprint; Mu-jin has no fingerprint (fewer than eight attributed lines).
- **scene_context** on the draft's names: pages found for Mu-jin (card and both State of Play pages) and Malphas; the only name flagged "no page" is Mortalis, which is a Wellspring (Codex Lists term, check 37 PASS). No figure is printed for it.
- **stale_names:** the tool sweeps the repo, not a draft file. The draft was grepped for every struck Büri-register and Kharven-old-form term (Büri, Ajiin, Altan, Nüdel, Khar Ild, Tengri, airag, borts, aaruul, deel): none present.
- **Hand greps (quickcheck):** zero em or en dashes; no "week"; no "rather than", "not only/just/merely/so much"; no hard-ban words; one simile-marker pair only inside the Tablet recitation block; one "as you know" hit (a simile) rewritten; the only question mark is in dialogue; "Mahuo" appears exactly once; "Ledger-Prince", "Accord" (now absent from the whole file, colophon included), "Division", "Paracelsus", "Noxinus", "Savant", "Voyager", "recovered", "decipher", "dialect", Tat, the cat, Geuk-hon, Kaalabad, Zeraphine Drowl, Pyraeon and The Mother are absent from his text.

## 2. Which decision each chapter serves

- **Title page and Note on the Name:** ST22 (Sum-gol title beside the archive title; glossed only as his house's word for correspondence, never literally, so Volume III's Correction can find the "answering" in it), MJ6 (apology for explaining), MJ7/MJ10 (his name and nothing above it), K9 (clean subheads).
- **Epigraph:** fixes 12 (his, written, not recovered), SE8 (Tempus stands as the Weight's Hermetic name), MJ8.
- **Chapter the First · Of Frost and the First Glass:** MJ2 (mountain, frost, rice valley, sky-watching; house named once, Ledger-Prince never), the Gate's "What Needs No Leave" (the primer's lawfulness given as his own belief, not as law), MJ1 (house thinned before his birth; "Sum-gol went" as the last of the house), C-094 (house's hollow thinned, province not emptied), SE8, the house's two customs (card Lore; C-108), ST18 set-up (Doryun's voice), card Catalyst, fixes 4 (Glory at fourteen), MJ4 seed (Ara in the lower hall, from her card), ML6 (primer as a later unlicensed text passed outside the Gate), ML2 (Malphas at the sealed-stacks gate), ST6, ST9, SE3/SE4, the Gate's "What Needs No Leave".
- **Chapter the Second · The Flat above the Tanner's:** SE3 (tanner's flat at Castlefall), SE1, Malphas card Origin (retting ponds; ML13 candour when glad), MJ11 (failing-seal sense, streets away, free; migraine on every lens-off read), MJ4 (Ara heals beside him; "a passage"), EC2 (no Draft refuels), R52-23 (the one family "we"), ST19 (the astronomer-monk named), SE12 (Antediluvian hall, closed passage, "older than Year Zero"), MJ3 (the Vis coffin, unexplained), SE11/SE5/WS5 (God-Essence, Maelor's gift, Maelor's edict aloud, cut over the Archivum's door), WS2 (clean Riptide), DE3 (plant only), EC13 (figures on both lens-off reads: the illness and the coffin), R51-08 (a quarter-moon, a turn).
- **Chapter the Third · Definitions:** SE6 (Urbis, rail), ST18 (the theft is a court scene: Doryun signs the boy's series into the court's book; the University only uses the series later, credited to Doryun, and Mu-jin corrects the changed link with an apology for correcting; no brawl, no degrees, no sternum strike), MJ5 (claims nothing, files his own matter), MJ10 (leaves before the Licentiate; practises unpaid under Furveus's licence), GW4 (Tria Prima onto Core, Shell, Attraction Layer), GW2 (the Rot), GW3 (Whitening in the Returner, read by colour), Conjunction's Rupture risk and mediation glyphs, EC6 (quicksilver, calomel, white arsenic by name; the dose is the point; crucible palsy and Draft-mark read on sight), GL9 (Furveus's Mortalis), ST7/ST8 (Draycott and Strom at the café), WS3 (the gate correction), DE7 ("necromantic" as the loose word), MJ5 (the café walk-out is gone; he tells Furveus plainly not to).
- **Chapter the Fourth · Corpus Hermeticum:** ML2/ML3/ML4/ML5/ML7 (two visitors, one "goes by a title", the unhealed left hand, the Necrocursica under his own name, the mocked sentence-title), ML1 (the relief: lighter, sleeps, laughs; Mu-jin glad and records it), GW9 (the Aphorism as the old debt doctrine only; no "summons himself"), GW8 (debt and correspondence on facing pages, unjoined), ML6 (Malphas's advice; Mu-jin listens), ST10/SE2/GL11/EC1 (Venur, the border, the Old High Runic amulet read at once and undatable, a Charm, maker paid once), MJ10 (no vow), ST19 (Penn Ralfsohn, the Weight-bred quarry per SE8, the second recitation as his father's words, adaptance, Auren's edict), MJ4/WS4/WS5 ("Death is not the opposite of life" from Ara; "nothing that has been is erased" as his error, sourced in Maelor's edict), ST16/SE11 (Asclepius's quarrel with the order's theology), the dream, the Sacred Discourse.
- **Chapter the Fifth · The Perfect Discourse, and the King Who Would Not Listen:** K2 Case I, ST15 (king and wife unnamed roles, no quoted line), MJ11/EC13 (lens-off read, migraine, η), card "Never says" (no rank to win; pressure held down on principle, tied to the house law), the Tablet whole with its closing in its own speaker's voice, "Hermes Trismegistus" (fixes 6, ST1, R50-05), Stage VII crossing at the hall (proposal), FOW VII Refraction (dual sight), MJ7 ("That is not my name").
- **Appendix · Notes toward the Continuing Work:** K3 (the "passing or departure" line stands), GW1 (double seven; the Great Work is the Temperance path; "the Coagulation of the first round", "round" to keep "turn" for the fourteen-day span), GW4, SE2, EC6, ML4/ML7/GW9, ST7/ST8 renamed, K8 + WS1 + GW5 (the Seven Cacodaemonic Corruptions as the Heresiology's inverted stages, each root current named, Conjunction on Attraction; "the inversion of Calcination" by name), MJ3/MJ5 ("A coffin at Genesio. I have not asked.", now the Appendix's last line; "The work continues" survives as the header's "whoever continues this work").
- **Colophon:** MJ8 (deposited for common use; "Withdrawn under seal" with no agency named, per the brief's colophon and MJ10: the Accord appears only from Volume III), SE4, SE7, EC7 (a named clearance Tier on Lyssara Veyn's pattern), K1 + answer 131 + R63-1 to R63-3 (696 IC, the Withering Era, the sixth year of the Imperial Age).

## 3. New in this piece (Natalie-originated, pending Isaac's ratification)

Everything below is invented for the rebuild under K10 and logged for entry; none of it is canon until Isaac rules.

1. **Title form.** "Gameung-nok" (the naming pass's form) beside THE ALFTIAN CODEX, with no subtitle. "Record of Response" lives in these notes only (section 4, item 1).
2. **The note on the name**: the book named by his house's word for what the Heralds call correspondence, read by him as a mirror; no literal gloss.
3. **Frostbite as his first diagnosis** (the carter off the Uplands road).
4. **The secondhand glass** (cracked second lens), charted from the school wall and a court windowsill; three years of Weight positions (brief proposal) that Neros copies.
5. **The last of the house going at his twelve**: the last grandmother to the ground, the last cousins to the court. "Sum-gol went" is Ara's line; the concrete content of "went" is new.
6. **The two men in the lower hall settling him** (bench, marriage, apology), across a table laid for twelve that the house had not filled in his lifetime: the subject of Ara's canon lower-hall scene is new (brief proposal).
7. **Doryun taught him Draftcraft** at the court bench (GL4 applied to his training).
8. **Ara's smock and plait**; her lines "That's asking" and "Why couldn't you write the word?" (brief proposal, recut on review), and "Correct" as his reply (card pet word) followed by "Come up. They're in the back room."
9. **Malphas's living inventory**: straw-grey-brown hair, narrow face, mended coat. The bench beside the sealed-stacks gate. His suppression felt as the absence of a man above on the ladder (brief proposal, a true plant for Stage VIII). The Heralds' seal on the gate's lock plate worn bright where hands had tried it.
10. **Furveus's inventory**: broad, soft at the middle, hair like wet rope, a physician's black gone brown at the cuffs, started at nine carrying ash, twelve years' bench service (brief's derived figure), grey nail-beds with pale bands (Draft-mark, keyed to quicksilver and arsenic); the laugh that comes first, on the stair.
11. **Neros's inventory**: outward-turned left eye kept shut, thin, dark, coat a size too large.
12. **The baker's room with a shared kitchen** in the archive-town (where the primer is set down).
13. **The primer's cut registration leaf**, his having asked the court for it at thirteen, and the cut stub standing at the spine the next morning (Chapter the First's closing image).
14. **The Castlefall station three winters old** in spring 693 IC, with its sap-weeping cedar platform; carters' "who keeps your posts" on it.
15. **Rent of four silver a month** (draft price table, 4 to 8 silver; pending).
16. **The jar of Uplands herbs working past its term** in Malphas's room, its failing seal felt and resealed (brief optional plant). The young author does not connect it to the illness.
17. **The illness as a burn nobody told the fire was out** (the canon law-fragment burn half-described, never named); "It never touched me."
18. **Mu-jin's Coagulatio suspensions**, brewed by him at the tanner's bench to the court's formula from Uplands stock bought in the archive-town, holding Shells still during the illness.
19. **The "we" slip and its correction** ("It was me.").
20. **The tanner's mother** (a hidden abdominal growth reaching the liver, jaundice) as the patient Ara sits with (brief proposal); at first light the tanner tells the carver who keeps the street's posts (the Ketsuen inventory's frontier custom for the dead, applied to Castlefall).
21. **"Jal gara"** at the carriage door, and the collar inside out.
22. **Penn's inventory**: a square man of fifty or so, nose broken once, beard cut with a knife, robe shiny at the knees. His father Ralf (name from the naming pass), a drake-hunter under a guild licence, gone when Penn was nine; the claw that came back. **"Weight-bred"** as the hunters' folk belief (brief proposal, SE8 recast), left uncorrected.
23. **Castlefall's ground reads Rill** (the brief's Rill is the Northern Shield's; no page places Castlefall's rung). Stated on the page as his lens-off read, so under K4 it becomes fact if ratified.
24. **Genesio's hall as a Spirit-type site** (brief proposal; stated on the page as his read, so it becomes canon under K4 if ratified).
25. **Maelor's edict cut over the Archivum's door** at Genesio.
26. **The migraine on the walk back up the passage** after the coffin read; "A pull answered it at the floor of my Crystal, toward the coffin."
27. **Doryun's seal series**: the fourth-chain link, [Ur] Balance changed to [Flx] Flux in the University's copy by an unnamed hand; Doryun's line "It will serve the court better under a senior hand."
28. **Furveus's line on the stair** ("That was yours. Well, it's better now, isn't it?").
29. **The carver's boy with every third stroke late** (Ketsuen's "third stroke late" put on the page as texture).
30. **Furveus's Wedding** laid with [Wvn] Weave at three points and [Ap] Aperture at the neck (glyph choice mine, verified in the Index).
31. **Gisli Draycott's inventory**: dead front tooth, forty or so, lean, fair going grey, good grey wool, smooth signet. **Ivor Strom's**: about sixty, white beard, wine-coloured birthmark over one ear, stiff knee, oilskin too big.
32. **Malphas's key on a cord** and the open gate at the stair (the bargain shown; Mu-jin does not ask what opened it).
33. **Why he rides**: leaving Furveus alone was the only advice he had, so he goes to take up the Heralds' offer at Urbis; the last ward-post of the valley white on its windward face.
34. **Venur's inventory**: lens-grinder's pitch burn on the right hand, broad brown face, grey in black hair tied at the nape, sheepskin coat, bottle-glass green eyes, the attic under the thatch, the bowl set down before he answered. His witness-clause answer (a voice beat the naming pass offered).
35. **The amulet's chain** [Ma] Recall · [Ir] Continuum · [Lei] Binding (the brief's recommended direction, Maelor's roots) and its rung, **Charm** (brief proposal, R47-5).
36. **Tram-rails going into the high street** at Urbis (brief proposal); the honorific slip toward the Prior; study without the vow (brief proposal); the Monastery behind the great coffee-house on the square.
37. **Asclepius's inventory**: badly set right wrist and the chalk angle, taller than any man, hair the white-gold of a candle flame seen through horn cut at the jaw, long face, elf-lines at the eyes, robe let out badly. Her line "Do it again."
38. **The dream's Herald spheres** pulsing on every shelf.
39. **The king's inventory**: heavy, younger than expected, coat of state buttoned wrong, restless hands, answering each thing with the thing he said before it. **The wife's bruise** (left jaw, yellow edge, plum centre, "four days old or five", his estimate), her hands folded, face to the wall-hangings.
40. **The Stage VII crossing in the king's hall**, with the first Domain seed as Coagulatio nucleation (brief proposal for the timing; the mechanism is mine).
41. **"Penn used it once, kindly, at the refectory door."** and the refusal spoken to him.
42. **The Heralds' Latin name used once**, Ordo Praeconum Maeloris (naming-pass proposal; canon has no Herald order).
43. **"Direction only."** replaces the source's "Direction, not conclusion" (see section 8).
44. **His η readings** (0.61 at the illness, 0.64 at the Wedding, 0.66 at the coffin, 0.62 to 0.67 moving in the king's hall): estimates inside the Tier 5 band (section 5).

## 4. Canon conflicts and tensions surfaced (recorded, not resolved)

1. **The book's title (decided on review).** The brief proposes Sangeungnok (상응록, "Record of Correspondence"); the naming pass returned **Gameung-nok** (감응록 感應錄) with a gloss line, "the Record of Response". The naming pass prescribes the gloss and the brief forbids it (ST22 as briefed: he "does not gloss the characters literally", and Volume III's Correction must be the one to find "answering" in his title). Decision: the naming pass's form, the brief's rule. The title line reads only "Gameung-nok"; the note glosses it as "the word my house uses for what the Heralds call correspondence". "Record of Response" stays in these notes as the literal sense Volume III will use. 感應 is the classical term for heaven and humankind answering each other, so the irony is loaded and unspent. Isaac may swap in Sangeungnok by changing the title line and the note's first sentence.
2. **Calendar stamp (closed).** R63-2 makes 715 IC the twenty-fifth year of the Imperial Age, so year n = IC − 690 and 696 IC is the sixth year. The colophon's "the sixth year of the Imperial Age" is right as stamped. (The earlier note had the counting backwards.) The rules digest's older "no IC" line is superseded by R63-1 to R63-3 and answer 131.
3. **"Older than the count itself" against SE12.** The Antediluvian Calendar (−900 to −450) sits inside the count's negative years (back to −1,400), so the fixes.md wording would contradict the Concordance. The draft uses the brief's resolution: "older than Year Zero and the sealing the years are reckoned from".
4. **[Ir].** The Master Glyph Index gives [Ir] as Continuum (Maelor). The Pantheon sheet lists Irath's glyphs as "[Ir] Will". GL1 puts Index names in chains, so the amulet reads Continuum. Needs a Codex clean-up row.
5. **C-094.** The Ketsuen page still describes Sum-gol as a living province of about 15,000. The draft thins only the house ("The house had thinned before I was born"; the last of the old house went out of the valley) and never describes the province.
6. **C-095.** Mu-jin's card header still reads "Eastern Concord-adjacent enclave"; the draft uses Sum-gol, Ketsuen.
7. **Mu-jin's card harmonisations** still list Distillatio and Calcination (the K6 card fix is planned, not applied). The draft gives him only Fixatio (innate) and Coagulatio (court bench), with Anamnesis beginning unnamed at Genesio.
8. **The title-writ's grade.** His card says the writ "named him S-tier"; at Glory his maximum Grade is A. The draft says only that it "named what I was worth before it named me".
9. **Ara's journey (resolved on review).** "Nine days by the courier road and the line" borrowed the Senri's Gate to Sum-gol courier span and quietly placed the court. It now reads "She came inside the turn" (within fourteen days), which fixes no location.
10. **Aether Class loss against Tier η** (brief section 9): the draft uses the Tier 5 band, 0.60 to 0.70, as his adult card does, and never names his Aether Class.
11. **Doryun and Doyun** sit one letter apart; only Doryun appears in Volume I.
12. **Kwon as a Mahuo cadet branch** (R37-1 open flag): not settled on the page.
13. **ST11 against K3**: not touched here (every Tat beat is gone); the Volume II brief must face it.
14. **Errata C-105** ("not one of" the Alftian codices "cites an Age") must be revised when this volume is published; not this job.
15. **"Turn" in three senses.** The Sky page makes a turn fourteen days; FOW VII makes "one turn" six seconds; GW1's double seven reads as two passes. The volume now uses "turn" only for the fourteen-day span ("the next turns", "three turns in warm dung", "inside the turn") and "round" for the Work's pass. The Sky/FOW collision itself needs a Codex clean-up row.
16. **The Heralds have no canon order.** "Ordo Praeconum Maeloris" and the Herald Monastery are naming-pass and SE5 applications awaiting a Factions page.

## 5. Every figure and its source

| Figure on the page | Source | Note |
|---|---|---|
| eleven miles from a mountain | Mu-jin card, Lore · Origin | canon |
| six hundred years (the house's Vocatia law) | card Lore; brief section 2 | canon |
| twelve / nine; fifteen / twelve; Ara thirteen at the illness | Ara three years younger (Ara card, brief); MJ1, Vaeloris ("She was nine when Sum-gol went") | derived |
| fourteen (catalyst, left the court) | card | canon |
| "nearly five years on" (left the court at fourteen, 691 IC; writing in 696 IC) | K3; K1 (born 677 IC) | derived (was "four years on", corrected on review) |
| a tenth of one circuit | three years of charting ÷ the Weight's ~29-year circuit (Sky page) = 0.10 | derived |
| a man who has seen the Weight come round twice is old | Sky page | canon |
| the road to Castlefall, then a day by rail, then two days mounted | SE3 (the day is from Castlefall) | canon |
| the line two years old (autumn 692 IC); the station three winters old (spring 693 IC) | R63-2 (rail from 690 IC); born 677 IC (C-106, K1), fifteen in 692 | derived |
| four silver a month | draft price table (4 to 8 silver a month) | draft, pending |
| "inside the turn" (Ara's journey) | Sky page (a turn is fourteen days) | canon unit; no route fixed (conflict 9) |
| Riptide, "ground where the Veil has begun to give"; A-grade output to hold one's own law; 4.6 × 10¹⁰ to 4.184 × 10¹² J | Tier Ladders, sites ladder (4.6024 × 10¹⁰ rounded to 4.6; the Veil clause describes the whole rung) | canon |
| a Spirit-type site "speaks to the Crystal and not to the mind, and gives a man seconds before it has him" | Tier Ladders, encounter-type table (Spirit: reports to "the Crystal, and not to the conscious mind"; warning window "seconds" at Millrace and Riptide) | canon wording; the site's Spirit type is a proposal (section 3, item 24) |
| "some seventy thousand units into the act, a seventh of what I carried" | Tier Ladders: an act's joules = EU spent × η × 1 MJ; 4.6024 × 10¹⁰ J ÷ (0.66 × 10⁶) ≈ 69,700 EU; 70,000 ÷ ~500,000 ≈ one seventh; his whole reserve delivers ~3.3 × 10¹¹ J, low in the A band ("the edge of myself") | **derived** |
| own reserve "somewhere past half a million units, high in Glory's band" | band 51,800 to 961,000 EU at VI (FOW VII Part Nineteen); his adult reserve runs above his Stage's band (card) | **estimate** inside the canon band, as the brief permits; label stays |
| η 0.61 (illness), 0.64 (Wedding), 0.66 (coffin), 0.62 to 0.67 moving (king's hall) | Tier 5 Expert band 0.60 to 0.70, FOW VII Part Nineteen | **estimates** inside the canon band, one reading per lens-off read (EC13) |
| Castlefall ground reads Rill, "high and steady, the kind that harms nobody"; the Wedding room "the steady Rill of the ground under a tannery" | Tier Ladders (Rill: "Ambient Saturation, high and steady"; "it harms nobody") | rung wording canon; **Castlefall's rung is a proposal** (no page places it; the brief's Rill is the Northern Shield's) |
| crucible palsy at about nine years of bench service; Furveus has twelve | Alchemetrica ("What it costs the body"); brief's derived service figure | canon + derived |
| the ferment three turns in warm dung | Alchemetrica: the Rot, six to nine weeks in the Bed = three to four and a half turns of fourteen days | derived |
| the Returner for most of a month | Alchemetrica: circulation "for weeks or months" | within canon range |
| a quarter-moon (the elementary ceiling) | fixes 5, R51-08 | canon unit |
| three silver marks, twice what the use was worth | brief proposal on the Value, Coin and Trade scale | proposal |
| Penn's father gone when Penn was nine; Penn "fifty or so" | none | proposal |
| Draycott "forty or so"; Strom twenty years older | brief (Strom about sixty, from his late sixties in Volume III) | derived for Strom, proposal for Draycott |
| the bruise "four days old or five" | his own estimate in the text | proposal |
| 696 IC; the sixth year of the Imperial Age | K1, answer 131, R63-1 to R63-3; brief | derived (conflict 2) |

The benchmark-output sentence (37,200 units a second, a 223,000 reserve empties in six seconds) was cut on review: it was a primer's table figure, not his read, and it did not answer what holding A cost him. No figure is printed for Ara, Furveus, Malphas, Neros, Draycott, Strom, Venur, Penn, Asclepius, the Prior or the king, and none for the amulet, the Drafts or the Wedding (no canon figure exists; EC13 lets him state figures only from canon bands). No dose figure appears anywhere (EC6): the only dose words are "in small measure" and "at a dose".

## 6. Stat Ledger: Kwon Mu-jin (the only practitioner with figures)

- **Stage:** VI Glory at the opening (left the court at Glory, card:147); crosses to **VII Refraction in the king's hall** (proposal): first Domain seed, then dual sight on the step. No first touch of S Grade (that belongs to a later book).
- **Great Work position (GW1):** the Distillation of the first round at the start, the Coagulation of the first round by the end; he says so in the Appendix and corrects "stand" to "setting".
- **Tier of Standing:** Expert (Tier 5), band η 0.60 to 0.70; readings on the page 0.61, 0.64, 0.66 and 0.62 to 0.67 (estimates).
- **Reserve:** estimate "past half a million" EU, inside the VI band and under the VI gate ceiling of 961,000. Holding A-grade at Genesio's floor costs him about 70,000 EU in the act (derived, section 5).
- **Harmonisations shown:** Fixatio (innate seal sense, felt streets away, free), Coagulatio (Drafts at the illness; the Domain seed's law). Anamnesis begins unnamed at the Genesio coffin ("A pull answered it at the floor of my Crystal, toward the coffin"). No Calcination, no Distillation (K6), no Vocatia working (untrained until VIII).
- **Essence:** Fulguria (arc-discharge blue, broken-edged, at the seed); Caloria undertone not shown.
- **Lens-off reads (five), each costed:** the Genesio coffin (rung, reserve, η, the derived cost; migraine on the walk back), the illness (Rill, η 0.61; migraine to the next noon, taste of tin), Furveus's Wedding (Rill, η 0.64; migraine until dark), the king (migraine on the spot, η watched), and the step afterward (lens in his fist, dual sight). No 40-second window, no "Loose Thread", no reserve share per read (the card's ~2% is a Stage XII figure).
- **Other costs on the page:** suppression of his own pressure in the king's hall ("a tiring skill"); Shell heat and a closed throat at the seed; waste leaving as heat (R47-8).
- **Body:** both eyes, both arms; lens on the left eye; white-blond hair; ink to the second knuckle; scholar's coat thin at the elbows; the amulet cold at the sternum from the high road on.

## 7. Workings on the page: Phenomenon lines

- **Ara's healing (Anima Spirare).** Phenomenon: wound re-epithelialisation along the provisional matrix, new tissue migrating over the scaffold the wound's edges leave. Wellspring law as the boundary: "a wound closes because the body remembers being whole" (Ara card). Aether: Castlefall ground, read Rill by him that night (proposal for the rung). Essence: the cost taken at her Shell (hands hot to the wrist). Fault, from the mechanism: it cannot argue with a process still running (the law-fragment burn), which is why the work is divided. Her Stage is left unstated (no higher than Flourishing, brief).
- **Mu-jin's Coagulatio suspensions.** A Draft from stock; steadies the Shell, heals nothing by itself, refills no reserve (EC2, R2-6).
- **Furveus's Wedding (Conjunction).** Phenomenon: coalescence, two drops on a pane running into one as surface tension minimises the shared interface. Governing law: Attraction; Conjunction has no Wellspring mirror (WS1, Alchemetrica). Boundary glyphs: [Wvn] Weave (Index: "foundation glyph for conjunction arrays; locks a third glyph in place"; the page now glosses it in those words) and [Ap] Aperture (Index: "valve control with a safety catch against over-spill"). Aether: Rill ground (proposal for Castlefall); the bench's stock and vein carry it, no reserve drawn (EC1), so no waste heat either (R47-8). Cost: bodily, the strain of holding the pour steady (neck red above the collar) and the tremor returning twice as hard. Fault: Rupture, the vessel first (Alchemetrica). Mechanism Vocabulary: Wedding, Rupture, mediation glyphs, Shell.
- **The amulet (Charm).** Phenomenon: entrainment of coupled oscillators (two pendulum clocks on one shelf falling into step through the wood). Chain: [Ma] Recall (Anamnesis, Limina), [Ir] Continuum (Maelor), [Lei] Binding (Anamnesis, Limina), Maelor's roots. Aether: draws nothing; the maker paid a once-only share of reserve long ago (EC1). Essence: a slow attunement pressed against the wearer's Shell. Rung: Charm ("does one small working reliably and forever... does not tire"). Fault: a Charm never hits hard; it only accumulates, and its maker cannot be traced from an undatable Old High Runic cut. "Wellspring resonance" is left as his own word.
- **The first Domain seed (Coagulatio), the king's hall.** Phenomenon: nucleation in a supersaturated solution, which stays clear until a seed grain gives it a site and then sets all at once. Wellspring: Coagulatio; the boundary is his spoken recitation (below Refraction a working needs voice, hand, ink or blood, R20C-42). Aether: a hall dense with one man's certainty soaked into the Residue, the district main under the floor. Essence: Shell heat, thirst, broken-edged Fulguria blue, hair rising; η watched moving inside its band (Refraction's Tier 5 gift, "real-time observation and correction of waste"). Fault, from the mechanism: nucleation sets whatever is supersaturated, the operator included; he cannot tell whether the words, the field or a slip in his held weight moved the king, and on the step he sees himself set into "something a room would want". Heresiology Case I: correspondence reintroduced between conduct and soul-account, "not by force alone".
- **Lens-off reads.** Gnosis Analysis through the lens; the Fixation Anchor Sense is passive and free. The named technique Sight Through the Glass (Stage XII) is not his and is never named.

**Draft Sub-Stat profile (EC4), for the Drafts made on the page:** Tempering Coherence and Maturity (Core, the Sulphur), Tempering Clarity (Shell, the Salt), Harmonics Attunement (Attraction Layer, the Mercury), Gnosis Analysis and Fluency (reading the chain and the vessel), Vitality Filtration (exposure: Furveus's crucible palsy and Draft-mark). Gnosis Analysis only; never the retired Diagnosis or Sapience. No values printed for Furveus (his FOW line is built later, ST6).

## 8. Rule ids that most constrained the piece

- **R61-10 (K10)** full rebuild; **R61-38 (MJ6)** the Volume I voice (apologies: the title note, the lens at the illness, the bridge, apologising for correcting at the seal lecture and at the café, the Prior; flaw first on every introduction, the announcing frame used once, for Draycott; dry self-correction: "which I called tact. It was pride", "It was me", "I should write that I spoke over him", "I withdraw the word"; lacquer lines cut on review); **R61-34 (MJ2)** and **R52-21** (house named once, no epithet, no rank to win).
- **R61-39 (MJ7)** and **fixes 6**: the Tablet's closing restored to its own speaker ("I am called Hermes Trismegistus"; Hermes is a god name, kept under ST1 and R50-05), the Thrice-Great refused aloud to Penn.
- **R61-40, R61-42 (MJ8, MJ10)**: deposit wording; no Accord, vow, credential or grading in his text.
- **R61-43 (MJ11)**, **R61-112 (EC13)**, **Table Rule 5**: every lens-off read costed; figures only from canon bands.
- **R61-69, R61-70, R61-71 (WS3 to WS5)**: the gate correction; "nothing is erased" as his error sourced in Maelor's edict.
- **R61-79, R61-82, R61-67 (GW1, GW4, WS1)**; **R61-100, R61-101, R61-105 (EC1, EC2, EC6)**; **R61-5, R61-6 (K5, K6)**.
- **R63-1 to R63-3** (calendar) with **R61-1, R61-131**.
- **R48-40 / R39-7** (no other minds: Malphas's wants and gladness rewritten as behaviour; Draycott's motive left as Mu-jin's inference).
- **R49-40** (no antithesis: "Direction, not conclusion" became "Direction only."; "It did not behave like a fever" cut; "The world does not glow when I do that. It goes quiet and specific." became "When I do that the world goes quiet and specific"; the attention aphorism was cut on review).
- **R4-14 CHAIN_CEILING and RUN_RULE, R49-13** (four rewrite passes for rhythm).
- **R13-2 / R48-20 / R16-3** (three strata at each working's display), **R9-3** (shard-edged discharge, eyes first at the threshold).
- **R53-19 / R49-54** (Ketsuen recurrence, counted by hand: Sum-gol scene: cedar weeping sap, the pressure at the temples; Genesio: the pressure at the temples; Castlefall, Chapter the Second: cedar weeping sap, "who keeps your posts", the carver told of the dead (the ward-post custom); Castlefall, Chapter the Third: the mallet on the practice stone, with "third stroke late").
- **R50-32, R49-49** (no italics for names, titles or foreign words; "Gameung-nok" and "Jal gara" roman), **R51-08** (turns, a quarter-moon, a month; no week), **R47-5 / R47-7** (the amulet's rung by name), **R52-23** (one family "we"), **R49-26** (chapter endings after review: an image (the cut stub at the spine), a line ("I told him I would return"), an action ("Furveus did not get up"), an image (dye in water), a spoken line ("That is not my name," I said); the Appendix ends on "A coffin at Genesio. I have not asked."), **R48-27** (credits below).

## 9. Real-world credits (R48-27; notes only)

- **The Emerald Tablet, three English renderings, wording kept from the source per ST1:**
  - Venur's recitation ("Truth. Certainty. That in which there is no doubt..."): E. J. Holmyard's 1923 English translation of the Arabic version (the Tablet as preserved in the Kitāb Sirr al-Khalīqa, attributed to Balinas, and in the Jabirian corpus).
  - Penn's recitation ("It is a certain point full of admiration..."): an English rendering of a later European version of the Tablet, already in Isaac's source text. **Its translator is not identified here; confirm before the credit is published.**
  - Mu-jin's recitation in the king's hall ("True it is, without falsehood..."): Robert Steele and Dorothea Waley Singer's 1928 translation of the Latin Tabula Smaragdina, with the closing's "Hermes Trismegistus" kept as the translators give it (the speaker ST1 keeps; the Monastery's epithet grows from it).
- **Titles:** Corpus Hermeticum (Chapter the Fourth); the Perfect Discourse, the Greek title (Logos Teleios) of the Hermetic Asclepius (Chapter the Fifth); Asclepius as a name (a god, R50-05).
- **Tria Prima and Spagyria:** Paracelsus's three principles (sulphur, salt, mercury) and the spagyric practice of separating a plant's oil, spirit and calcined salt and recombining them.
- **Paracelsus's dose principle** (that the dose makes the poison, Septem Defensiones, 1538): behind "the dose is the point"; not quoted, and Paracelsus is not named in the text (ST1).
- **Iatrochemistry:** calomel (mercurous chloride) as a purgative; white arsenic (arsenic trioxide) as a tonic in small doses; chronic mercury poisoning (tremor, erethism) behind crucible palsy; the pale transverse nail bands of chronic arsenic exposure (Mees' lines) behind the Draft-mark on Furveus's nails.
- **Frostbite:** pallor and numbness, clear and haemorrhagic blisters (the dark ones mark deep injury), dry gangrene and the line of demarcation that guides amputation.
- **Tanning:** liming, dung-bating, oak-bark pits (via the Works and Days page).
- **Physics:** heterogeneous nucleation in supersaturated solutions (the seed); coalescence of droplets under surface tension (the Wedding); Christiaan Huygens's observation of synchronised pendulum clocks, 1665 (the amulet's entrainment).
- **The title:** 感應 (Korean gameung), the classical East Asian term for stimulus and response, as in the Han-dynasty doctrine of heaven and humankind responding to each other (天人感應), via the naming pass.

## 10. Checks against the Heresiology cases (K2, K10)

- **Case I, The Hall of the Unquestioned King.** "A ruler hardened in private certainty": elected, then ungovernable; advisers, court and petition dismissed. "Metaphysically sealed against contradiction": the lens-off read gives Conviction's sign word for word in substance (resonance dry, angular, unmoved by the appeal about his wife). "Not by force alone": the monks remove the courtiers, Mu-jin holds his own pressure down, and the words and the seed do the rest. "By reintroducing correspondence between his conduct and his own soul-account": "What set in that hall was the king's conduct against his own soul's account, held still together long enough for each to be read by the other." The Appendix names the corruption met as the inversion of Calcination. Match holds.
- **Case II, The Compelled Author.** "Pulled by access": the sealed stacks as the bargain, the open gate and the key on the cord. "Manipulated through need": two compellers, the unhealed hand, the mocked sentence-title. "Talented writer": the treatise set on him because of his pen. The footnote belongs to Volume II. Nothing lets Mu-jin connect Malphas to rot-work, cults or later names; Zeraphine Drowl is not named; the second visitor "goes by a title". Match holds as seed.

## 11. Reading pass (prose-law-quickcheck)

- **Ladder:** none (checker and read).
- **Gloss:** "which is the Whitening" (apposition gloss) rewritten so the term is used in context; "Coagulatio is that law" kept as his own reasoning after the image; "The primers call that the first seed of a Domain." kept as his naming; "They are accurate." cut on review; "That is what the words cost." and "He was patient about everything." cut on review.
- **Local burstiness:** no flat runs, no chain; short-sentence share 33%.
- **Reification at the beat:** the two kept payoff lines ("That silence cost me everything." "That is what the words cost.") both failed the deletion test and were cut on review; Chapter the First now ends on the cut leaf's stub, and the rain on the step carries the cost of the king's hall.
- **No other minds:** checked sentence by sentence; motives are behaviour or his marked inference.
- **Knowledge ceiling:** no Accord, Division, Heresiology, Rimward or Frithia in his text; Malphas stays "the alchemist"; the coffin, the jar and Strom's line are left for the reader.
- **Voice swap:** Ara (short, fast, dry), Malphas (command, no contractions), Furveus (genial deflection, contractions, the laugh first), Penn (plain grief), Asclepius (dry challenge), Venur (the witness clause), Draycott (no quoted line; shown by his pleasure), Strom (one oblique line). None swaps.
- **Contractions:** Mu-jin only in family contexts ("I haven't learned it either"; "They're in the back room" to Ara); Ara's "That's asking", "couldn't"; Furveus's "it's", "isn't"; none while Mu-jin corrects or reads a working; Malphas never.
- **Texture:** from the Ketsuen, Accord and Alchemetrica banks; invented texture logged in section 3.

## 12. Deviations from the brief (all small, for Isaac to overrule)

- Title per the naming pass (conflict 1).
- "Year Zero" wording per the brief's section 6 item 8, over fixes.md's "older than the count itself".
- Cut for length (target 6,000 to 8,000): the Castlefall terrace-peaks description, the tanner's wealth line, the shepherd's ward-line folk belief, "thanked him twice", the Prior's "channels I declined to ask about", the Monastery's "stark and permanent", "The Parting" as a named step, the Feeding (GW2's completion), Venur's "structural law" phrasing (kept as "one law in a star and a stone"). All are recoverable.
- Kept line adapted for R49-40: "Direction only."
- Brief-kept lines cut on review (MJ6 lacquer, ML6, R4-13, R49-26): "That silence cost me everything.", "Pride is an unreasonable organ." (now "which I called tact. It was pride."), "the least expensive to lose" (now "It gave no reason, and I asked for none."), "Alchemy does not ask for your ambitions...", "That is what the words cost.", "The work continues." (its sense kept in the Appendix header's "whoever continues this work"). Kept: "remarkable or insufferable depending on the listener's disposition", "I have not read it. I intend to.", "I have not resolved the question of their purpose. It does not feel resolved from the inside."
- ST18 staging: the brief's University exposure is kept only as a later use of the stolen series; the theft itself is the court scene (Doryun signing the pages into the court's book), and the chapter now tells it in that order, which is ST18's letter ("the scene moves to the court").
- Title gloss: the naming pass's "the Record of Response" dropped from the page under the brief's ST22 rule (section 4, item 1).
- The Monastery's formal name Domus Memoriae (naming pass) is not used; the Latin appears once, as the order's name on the Prior's letter.

## 13. Open questions

1. Gameung-nok or Sangeungnok for the title (the draft uses Gameung-nok with no literal gloss; section 4, item 1).
2. Ratify or replace the invented physical inventories (Malphas living, Furveus, Neros, Penn, Venur, Draycott, Strom, Asclepius, the king).
3. Ratify the Stage VII crossing in the king's hall, and Coagulatio nucleation as the first Domain seed's mechanism.
4. Ratify the amulet's chain ([Ma] Recall · [Ir] Continuum · [Lei] Binding) and its rung (Charm); and the [Ir] Index/Pantheon split for the Codex.
5. Identify the translator of the second (Penn's) Tablet rendering for the credit line.
6. Dose and mechanism research for quicksilver, calomel and white arsenic (EC5, EC6) before print; it feeds the planned Real Alchemy page. The text prints no dose.
7. Ratify "Weight-bred" as a hunters' folk belief (SE8 recast of "Tempus-bred") and Penn's father Ralf's guild licence.
8. Ratify Castlefall's rung (Rill) and Genesio's hall as Spirit-type; both are stated as his reads, so both become canon under K4 once ratified.
9. The Sky/FOW "turn" collision (fourteen days against six seconds) needs a Codex clean-up row.


## 14. Review (four reviewers, 2026-09-28): each finding, applied or rejected

Line numbers are the pre-review draft's. "Applied" means the passage was rewritten, not patched, where the finding touched its shape.

### Decisions reviewer

1. **Seasons run past the colophon.** Applied. Urbis is now reached "before the passes closed that autumn" (694 IC); the café falls in the wet snow of winter 694 to 695, "the next thaw" is 695, Asclepius winter 695 to 696, the king spring 696. "for a year" became "for more than two years". The same pass fixed "four years on" to "nearly five years on" (left the court 691, writing 696).
2. **The Accord in the colophon.** Applied: "Withdrawn under seal. Classification: Mortalis-adjacent. Clearance Tier IV Restricted (Hermetic Correspondence)." The word "Accord" is now absent from the file.
3. **Title gloss spends Volume III's irony.** Applied. Subtitle dropped; the note glosses Gameung-nok only as "the word my house uses for what the Heralds call correspondence".
4. **What he took from court.** Applied with canon finding 1: "The only thing I took that was mine"; the suspensions are brewed by him to the court's formula from Uplands stock bought in the archive-town; the horse is paid with "the last silver I had".
5. **Figures missing from two lens-off reads.** Applied: the illness read gives Rill and η 0.61; the Wedding read gives the Rill and η 0.64. No figures for the friends.
6. **ST18's letter.** Applied by restaging: the theft is the court scene, told in full; the University only uses the stolen series afterwards and Mu-jin corrects its changed link. Logged in section 12.
7. **The Tablet's speaker.** Applied: "I am called Hermes Trismegistus". Noted in sections 8 and 9.
8. **Maelor's edict over Sum-gol's doorways.** Applied: the edict is now "cut over the Archivum's door above us" (a Herald house he knows), clear of Sum-gol's breath theology. Logged as section 3, item 25.
9. **Old sentences beyond the keep list.** Applied: the robe is now "gone shiny at the knees"; "between delight and exhaustion" became "the face of a teacher who has been handed the whole syllabus back in one breath".
10. **Two errors in the notes.** Applied: the calendar question is closed (section 4, item 2); Castlefall's Rill is relabelled a proposal (sections 3 and 5).

### Canon reviewer

1. **Things taken from court.** Applied (see decisions 4). The reviewer's "silver I had earned copying at Genesio" was not adopted: it would invent an income; "the last silver I had" makes the same repair with nothing new.
2. **Rill called thin.** Applied: "Rill, high and steady, the kind that harms nobody" and "the steady Rill of the ground under a tannery".
3. **Spirit-type site wording.** Applied: "speaks to the Crystal and not to the mind, and gives a man seconds before it has him"; the Veil clause now describes the whole rung ("Riptide, ground where the Veil has begun to give"). Spirit type logged as a proposal (section 3, item 24).
4. **The reserve figures answer the wrong question.** Applied: the benchmark sentence is gone; "To hold A at the floor I had to put some seventy thousand units into the act, a seventh of what I carried" (derived, section 5). η is now one estimated reading per read (0.66 at the coffin).
5. **Reading the primer stated as lawful.** Applied: "I told myself reading broke no law ... and I let that stand for innocence."
6. **Title gives away the Correction.** Applied (see decisions 3). The naming-pass/brief conflict is recorded and decided in section 4, item 1.
7. **The Wedding costs nothing, then costs Shell heat.** Applied: "at the Shell as heat" cut; the cost is the strain of holding the pour (neck red above the collar) and the tremor returning.
8. **"That is a picture".** Applied: "The river is Sylorin's soulstream, a Pantheon image, and it is no current." "A Pantheon image" is WS3's own wording; the sentence no longer calls the Crossing's soulstream unreal.
9. **Maelor's edict.** Applied (see decisions 8).
10. **Rail geography.** Applied: "I took the road down to Castlefall and the line a day from there"; the station is "three winters old".
11. **Ara's nine days.** Applied: "She came inside the turn." Section 4, item 9 closed.
12. **"Priors".** Applied: "the Prior and the senior teachers".
13. **"Turn" in three senses.** Applied: "the Coagulation of the first round"; "turn" kept only for the fourteen-day span. The Sky/FOW clash is logged (section 4, item 15; section 13, item 9).
14. **Weave gloss.** Applied: "to lock a third glyph in place while the two principles meet".
15. **Notes list things not on the page; section 5 misquotes.** Applied: Ara's cloak, Malphas "ten years older" and the clerk at the closed passage are gone from sections 3 and 5; the Spirit row now quotes canon.

### Voice reviewer

1. **"That silence cost me everything."** Applied: cut; Chapter the First ends on "Malphas never said where he had got it, and I did not ask" and the image of the cut leaf's stub at the spine.
2. **Ara's echo and "Correct".** Applied: the verbatim echo is gone; Ara says "That's asking. Why couldn't you write the word?"; he answers "Correct" and deflects the why ("Come up. They're in the back room.").
3. **Surviving lacquer.** Applied throughout: "Pride is an unreasonable organ" became "which I called tact. It was pride."; "the least expensive to lose" became "It gave no reason, and I asked for none."; "The book does worse" became "I will do it again before the first chapter ends."; the attention aphorism cut; the stubbornness aphorism replaced with the king answering each thing with the thing he said before it; "which felt like a rite I had been assigned" and "I had no words" cut.
4. **He never apologises for correcting.** Applied twice: at the lecture ("I apologised for correcting the book, and then corrected it") and at the café ("I beg your pardon. It is a gate.").
5. **Flaw-first template.** Applied: the announcing frame survives once (Draycott). Malphas opens on his hands at the bench, Furveus on the tremor, Neros on the eye, Venur on the burned hand setting down a bowl, Asclepius on the chalk angle and the crooked wrist.
6. **Benchmark spec-sheet sentence.** Applied (see canon 4). "A is the highest Grade Glory reaches" also cut.
7. **Furveus swappable with Malphas.** Applied: "On the stair Furveus laughed first. 'That was yours,' he said. 'Well, it's better now, isn't it?'"
8. **Contractions.** Applied: "They're in the back room" to Ara; "and it was" added after the collar. Correction and reading passages stay clean.
9. **"The house says 'we' when it is frightened."** Applied: cut.
10. **Attribution inside the quote.** Applied: "'Death is not the opposite of life,' I said. Ara had taught me that on a stair in Castlefall, and then I went further than she had".
11. **Malphas too forthcoming.** Applied in part: "A treatise. They have named it already: the Necrocursica. They wish my name on it." The book's name is kept in his mouth because the Appendix names it and Mu-jin has no other source for the name; the speech is shortened to eleven words and "It is a very long name for a man who copies" stays.

### Prose reviewer

1. **Ladder at the king's stubbornness.** Applied (voice 3).
2. **Not X, Y.** Applied: "When I do that the world goes quiet and specific".
3. **Reaction-shot cutaway at the Discourse.** Applied: "Behind me nobody in the ring moved; I would have heard the robes."
4. **Setup, deadpan, reaction.** Applied through voice 2's fix, and partly rejected: "Correct" stays, because the setup's verbatim echo is gone and the line now answers Ara's harder question and turns the subject, which breaks the three-beat shape; it is his card's pet word, used once.
5. **Glosses at the beat.** Applied: "That is what the words cost", "That silence cost me everything", "It was the one thing in reach I could do anything about", "He was patient about everything" and "They are accurate" all cut.
6. **Endings on narration.** Applied: Chapter the Fifth ends "'That is not my name,' I said." (MJ7's words, now spoken to Penn); the Appendix ends "A coffin at Genesio. I have not asked." and "The work continues." is cut, its sense kept in the header's "whoever continues this work".
7. **Furveus continuity.** Applied: "for more than two years"; "The tremor was what I had known it was since the Archivum: crucible palsy, early." Only the Mortalis is new at the read.
8. **"X before Y" three times.** Applied: two cut; the title-writ line kept; the Glory passage now opens on the lamp ("That year a lamp would gutter when I lost my temper").
9. **Introduction template.** Applied (voice 5).
10. **Competing figures.** Applied: "and the Weave fixed the one place where they could meet"; "a city-state near Urbis ... as cold men stand round a stove".
11. **Stock phrases.** Applied: "I had no words" cut; the wife "with her hands folded at her waist and her face turned to the wall-hangings"; the Prior's look rewritten.
12. **Beats with no world-only detail.** Applied: the tanner's mother (the tanner tells the carver who keeps the street's posts); Malphas's "Leave it" (the Heralds' seal on the lock plate worn bright); the night ride (the last ward-post of the valley white on its windward face); the dream (a Herald sphere pulsing on every shelf); the lower hall (a table laid for twelve that the house had not filled in his lifetime).
13. **Sentence variance.** Applied to the five named paragraphs and others (fragments and long runs; "She promised her nothing." stands alone; the flat runs went from 7 in the first post-review run to 0). Partly unresolved: the whole-text CV reads 0.72 against the 0.80 target (an info line, not a warn); lifting it further would mean chopping the kept recitation-adjacent paragraphs and the appendix labels, and I stopped there.
14. **The figures in the Riptide read do not follow.** Applied (canon 4's derived cost, which answers what holding A costs him from his own reserve).
15. **Unclear referents.** Applied: "He told me not to ride in that weather"; "My eyes blurred first, then cleared on two things at once"; "The same mapping makes the putting-back a Wedding"; "holding a weight of its own", "A pull answered it at the floor of my Crystal, toward the coffin", "a field of my own took the room"; the ride's motive added (leaving Furveus alone was the only advice he had, so he goes to take up the Heralds' offer). "a field" was chosen over "my own weight took the room" because he is holding his weight down in that scene.
16. **Dragon or drake.** Applied: "A drake's claw".
17. **Self-correction pairs.** Applied: "I was not." cut; the remaining four are "It was pride", "It was me", "I should write that I spoke over him", "I withdraw the word".
18. **Echoes.** Applied: "and practised for hire" cut (the fees stay in the next paragraph); Asclepius's hair is now "the white-gold of a candle flame seen through horn"; the third "glad" became "I did not ask what had opened it"; "the way" in narration down from 8 to 2; "offered" down from 4 to 1.
19. **Narrator wink.** Applied: "because it was charming" cut; line 173's dread kept.
20. **Period feel.** Applied: "behind the great coffee-house on the square". The Castlefall "café" (ST7's own word) stays.

### Unresolved after review

- Sentence-length CV 0.72 against the 0.80 target (info only; verify passes).
- Prose length 8,155 words, 2% over the brief's 8,000 target.
- Everything in section 13, chiefly: the title (Gameung-nok without gloss, decided here, open to Isaac); Castlefall's Rill and Genesio's Spirit type as proposals made canon by K4 once ratified; the η readings as labelled estimates; the Sky/FOW "turn" collision for the Codex clean-up; the translator of Penn's Tablet rendering.
