# The Papers: the names

Drafted 2026-09-28 for the rebuild of the old Corrant Papers (K10, ME3: the third text in composition order). Nothing here is written to the repo.

**Frame (the lead's dates, carried as given):** the case opens after Volume II is deposited (700 IC) and runs to the hand-delivery of Draycott's intercepted second letter, about 700 to 701 IC, before Volume III. Mu-jin is 24 on the Ashgate road in 701 IC. Greyshaft Nine (706 IC) is five years off.

**Decisions applied:** PA1 to PA6; ST1 to ST5, ST9, ST12 to ST14, ST17; ML4, ML7, ML14; GW5, GW9; GL10, GL12; EC7, EC12, EC15; SE1, SE3, SE4, SE6 to SE9; WS3 to WS5; K2; ME1 to ME3. Rulings: R61 (alchemy conversion), R62, R63 (calendar), R64 and R65 (the two published volumes).

**Rules loaded:** load_rules [naming] (164 rows); [register, worldbuilding] rows as used in the two Codex names files. The rows used here:
- R20-1 (the Concord Human anchor and the class marker), R20-3 (the Concord pool), R20-4 (the filing convention), R20-5 (address, and names on the page).
- R23-2 (the Northern stratum), R23-3 (stratum follows institution), R23-5 (outliers).
- R50-03, -04, -12, -15, -17, -18, -22, -23, -27, -28, -32 and -34.
- R61-11 (ST1), R61-14 (ST4), R61-24 (Halveth), R61-27 (Dessa Mael), R61-62 to R61-66 (PA2 to PA6), R61-83 (GW5), R61-87 (GW9), R61-97 (GL10), R61-99 (GL12), R61-106 (EC7), R61-114 (EC15), R61-115, -117, -118, -120, -121, -122 (SE1, SE3, SE4, SE6 to SE8), R61-128 (ME2).
- R65-3 (Draycott's mark) and R65-10 (the Volitional Trace).
- The Concord pool itself, from sources/WOTR_Naming_Guide_Amendment.docx (read only).

**Docket:** check_docket [naming, register, worldbuilding] shows nothing pending.

**stale_names (scope all):** 29 files still carry struck Büri-register terms. All are Moto or Kharven material, and no Codex page is listed. No name kept or proposed here is a struck term.

**Collision method:**
- `grep -rlw` (and `-rliw`) of every proposed form across wiki/, scenes/ and book/, leaving out .manifest.json and INDEX.md.
- Substring greps for sound-alikes (`farr`, `ferr`, `orin`, `halv`, `kev`, `pell`, `nol`).
- The two Codex names files' checks are not repeated. Their forms are carried as settled.

---

## 1. The new author (PA3)

### Chosen: Niall Farrant

**Form:**
- Niall Farrant. Surname first in any Night Watch filing: "Farrant, N."
- The document becomes **The Farrant Papers**.

**Culture and convention:**
- He is a Concord human, born in Urbis, in the Inner World's Northern stratum (R23-2). Stratum follows institution (R23-3): a crown-chartered Society files him, and the Accord's Division files him beside it.
- **Niall** is in the canon Concord given-name pool (R20-3, male list). It is the only name on that list still unused in canon; see "Rejected on the way".
- **Farrant** is a byname frozen into a surname. A frozen surname reads as urban, chartered and documented, and the tax rolls demanded it (R20-1 class marker). That is an Urbis family.
- It is a **descriptive** byname (the guide's "Aldric the Red" type), frozen the way "Aldric Bram" froze from "Bramsohn".
- It files in two clean fields, given name and family name, so the Accord filing flattens nothing (R20-4; R61-63's reason).

**The Oren Corrant mould:**
- It is two trochees, with the surname ending on -rrant, stressed first.
- "The Farrant Papers" keeps the beat of "The Corrant Papers". The same thing was done when Strom kept Thom's rhyme and Gisli kept Gillus's G-L.
- It contrasts with Mu-jin's Mahuo name, as PA3 asks.

**Meaning:**
- Farrant comes from Old French *ferrant*, "iron-grey". It was a horse-dealer's word for a grey coat before it became a nickname for a grey-haired man, and then a family name. The French farrier, the *maréchal-ferrant*, comes from the same iron.
- Niall is Gaelic, of disputed meaning ("champion" or "cloud"). As a pool name its meaning carries no weight.
- A surname carries no felt meaning for the people who bear it, so the gloss lives in these notes and the page claims nothing.
- For the record: iron-grey suits a Class Ø man who carries no signature and reads the world through iron and brass (PA4).

**Say it:** NEE-ul FARR-unt. The a is the one in "carry", and each word is stressed on its first syllable.

**On the page:**
- **Head:** THE FARRANT PAPERS.
- **Filing line:** "Farrant, N., Urbis chapter, on the crown's warrant". This follows the insert heading "Tally, N., Timberline chapter, North Ferriby walk". A Searcher keeps no fixed walk, so the warrant stands in the walk's slot.
- **Signature on the closing note:** "N. Farrant, Searcher, Urbis chapter".
- **Who calls him what** (R20-5):

| Speaker | Form |
|---|---|
| Halveth, Draycott, Mu-jin | Farrant |
| Dessa Mael, Cassian Ault, the distiller | Searcher |

Never "Master Farrant": Master is a Tier of Standing, and he holds none.

**Collision:**
- Niall, Farrant, Ferrant and Farran each match 0 files.
- Soft sound-alikes, allowed under R50-17 and recorded in flag 5:
  - Tomas **Farren**, Lorn Stark's fellow uncle (2 files, Kharven thread).
  - **Ferriby**, the Night Watch's founding tin (517 hits, a place).
  - **Nol** Tally, a Watch walker (N-L onset).
  - "farrier", which shares the etymology and is harmless.

### Alternate A: Orin Farrant

**Form:** Orin Farrant. This is the same surname with the pool's **female** given name Orin (R20-3, female list).

**Why offer it:**
- Orin is the pool's nearest form to Oren. The source name's own sound survives in the canon pool, and the name is still new.
- It makes the investigator a woman. The rebuilt Volume III's doorway line then reads "the kind of woman who", where the published Volume the Third page has "the kind of man". The Papers' source never genders the narrator except through the name.

**Culture, convention and meaning:** as for Farrant. Orin is a pool name, so its meaning carries no weight.

**Say it:** OR-in FARR-unt

**Collision:**
- Orin matches 0 files.
- Soft rhymes: Borin (Borin Ironheart, 241 hits) and Valorin (63). R50-17 allows both.

### Alternate B: Niall Wakeman

**Form:** Niall Wakeman. The document becomes **The Wakeman Papers**.

**Culture and convention:**
- An **occupational** byname frozen into a surname: an urban, chartered family.

**Meaning:**
- From Middle English *wake-man*, "watchman", a town's night officer. At Ripon the wakeman set the watch each night by horn.
- The family's ancestor kept a city's watch, and the byname froze.

**Why it is second:**
- It says the office out loud. A Night Watch man named Watchman reads as a joke the Society would make, and the page would have to carry it.
- It keeps none of Corrant's shape.

**Say it:** NEE-ul WAKE-mun

**Collision:**
- Wakeman matches 0 files, with no sound-alike in canon.
- Earth echo: Rick Wakeman, a musician. That is soft and allowed under R50-04.

### Rejected on the way

| Candidate | Why not |
|---|---|
| **Wren** (pool) | Wren Greymane, 91 mentions in the Kharven thread. |
| **Tomas**, **Farren** (pool) | Taken together by Tomas Farren. |
| **Dunstan**, **Garret**, **Osric**, **Josse**, **Aldric**, **Edric**, **Ivor**, **Penn**, **Ralf** (pool) | Taken: Dunstan the Brine; Garret Longshore (70 hits); Osric and Osric Salter, who is Malphas's Academy name; Josse Garretsohn, Aldric Harrow and Edric Ashmore; Ivor Strom; Penn and Ralf Ralfsohn. Repetition is legal in the pool, but the author of a published document should be unique. |
| **Haldor** (pool) | H-L-D beside Halveth on every page, and Haldrek already exists. |
| **Durrant** | Its D-R-T skeleton matches Draycott's, and "To Durrant ... G. Draycott" is unreadable. |
| **Sayer** (from assayer) | It echoes Dorothy L. Sayers, a real detective novelist, on a detective's papers (ST1's spirit). |
| **Tallant** | It sits beside Nol Tally in the same Society. |
| **Latimer** | Three syllables, and Hugh Latimer is a known historical person. |
| **Greaves** | Greaves tin is a canon maker (The Apparatus of the Age). |

---

## 2. His office and the frame (PA2, PA5)

### Searcher (replaces "Enforcer-Archivist")

**Form:**
- The Society's title for an investigator sent on the crown's warrant: "Searcher", or "a Searcher of the Night Watch Society".

**Convention:**
- It follows the Society's plain agent nouns: walker, coil-carrier, Searcher.
- It comes from the English parish record, which is the Concord anchor's own ground (Naming Guide Amendment: "medieval English parish records"). The parish **searchers of the dead** viewed a body and reported the cause to the parish clerk. The customs **searcher** went aboard on a warrant.
- For a Class Ø man, the title fits: he looks, and others' senses and his instruments do the reading (PA4).

**Why not the canon words:**
- "Warden of Duty" and "Officer of Attribution" belong to the Night Register and Wystan Ashmore.
- "Field man" is the Society post Wystan takes after the Register folds (bible; outline ch72). Giving it to Farrant would make him Wystan's predecessor in one post and tie the two threads (flag 6).
- "Pursuivant", the Elizabethan warrant officer, is a herald's rank in Earth usage and would read as Maelor's Heralds.

**Say it:** plain English.

**Collision:**
- Searcher matches 0 files.
- Lower-case "searchers" appears three times as a common noun: Rengai's and Dhaerin's cards, and Garu Luneward's. It is not a title in any of them.
- Franchise echo: *The Searchers*, a film. Allowed under R50-04.

### The Urbis chapter, at the Ropewalk

**Form:**
- The Night Watch Society's local body in the city is **the Urbis chapter**.
- It keeps its house and bench in **the Ropewalk**, a disused ropemakers' walk. In the frame it is "the chapter house in the Ropewalk"; in his mouth, "the Ropewalk".

**Convention:**
- Chapters are named for the ground they cover (the Timberline chapter). A city chapter takes the city's name.
- The house follows the Register's own precedent: a working building the Society could afford. The Register sits in a former scullery on Cutler Row, which is a trade street.
- A ropewalk is a real English building and street name (R50-03). It is long, narrow, roofed and cheap once the trade has left it. That suits a Society that prints on the cheapest rag and carries brass where a full desk carries silver.
- It is where men once walked backwards down a line spinning yarn, which is the Society's word, "walk", in a building.

**Doublet:** R50-23 allows an Accord Latin form. None is needed, because the Watch speaks plain.

**Say it:** ROPE-wawk

**Collision:**
- "Ropewalk", "rope-walk" and "Urbis chapter" each match 0 files.

### The Night Watch's name, in the frame and in his mouth

- The frame (chancery style) says **the Night Watch**.
- His entries say **the Night Watch Society**, or **the Society**.
- This follows the canon page: "one body under two names".
- The crown whose warrant it holds stays **the crown**, unnamed, as on every Watch page (flag 2).

### The case's names

| Name | Who uses it | Ground |
|---|---|---|
| **the Castlefall file**; **the Castlefall tin** | The Watch. The first tin sealed on this case is the circle-room scraping, and the Watch names its files by ground ("the Ferriby tin", "the Hollow Shaft file"). | Night Watch page; bible |
| **the Eastern Commission** | The Division's reference for the commission and the Ault interview | Heresiology Case III is "The Eastern Commission of Grief" (K2: the Heresiology is written after, from these files) |
| **the Genesio Activation Sequence** | The Division's reference that replaces "VOLITIONAL TRACE — ANAMNESIS WELLSPRING — ACTIVE" | Heresiology Case IV's title. The file gives the Heresiology its heading. |
| **the Drift of Tempus** | The Division's reference for Neros's readings | Heresiology Case V's title. "Tempus" is Neros's Hermetic word (SE8), so the Division files under it and Farrant writes "the Weight". |

**Collision:** "Castlefall file" and "Castlefall tin" match 0. The three Division references are canon's own case titles, one match each.

### Officers the frame needs

| Officer | Form | Ground |
|---|---|---|
| The opening officer | **Halveth**; in the filing line "Halveth, K., Research and Archives Division, Urbis office" | ST14, PA2 (R61-24, R61-62). Her given name is new: section 4. |
| The Watch officer who enters the warrant | **the Society's secretary**, a role | Already a role in the night-watch bible. R50-27. |
| The Urbis chapter's receiving hand | **the chapter clerk**, a role | R50-27. Receives and dockets; no lines. |
| The assay of record for the Castlefall tin | **Dessa Mael**, at the Genesio Archivum's assay room (recommended) | The Watch writes the assayer's full name at the head of the docket (Night Watch page). This needs no new name; see flag 4. |

---

## 3. Every other name the Papers use, with the verdict

"Keep" means the name passes ST1 and the naming law as it stands.

**ST1 check on the source:** no name in the source that the Codex files have not already handled echoes a real Earth person. Neros's faint echo of Nero stays noted and unacted, as in Volume I, and Cassian and Madeleine were cleared in the Volume II file. No new ST1 rename is owed.

### People

| Source form | Papers form | Verdict and ground | Say it |
|---|---|---|---|
| Oren Corrant; O. Corrant; "Enforcer-Archivist" | **Niall Farrant**; **N. Farrant**; **Searcher** | New (PA3, PA2). Sections 1 and 2. | NEE-ul FARR-unt |
| Halveth | **Halveth** (Keva Halveth on her roster entry) | Keep (ST14, R61-24). She is head of the Division's Urbis office, and the case is joint (R61-62). The given name is new, section 4. | HAL-veth |
| Vis Trismegistus; Trismegistus; "Tell Trismegistus" | **Kwon Mu-jin**, then **Kwon**; "Tell Kwon" | Settled (fixes; R61-128). He knows the Monastery's "the Thrice-Great" and does not use it (R61-39). | KWON moo-JIN |
| Noxinus Ren | **never written**: "the Necrocursica's author" | PA2: no file names Malphas, so the Papers do not either. Flag 1. | none |
| Paracelsus Furveus; Paracelsus | **Furveus** | Settled (ST1, ST6). | FUR-vee-us |
| Gillus De Raits; G. De Raits | **Gisli Draycott**; **Draycott**; "Draycott, G." in a filing; the letter signed **G. Draycott** | Settled (ST1, ST7). | GIS-lee DRAY-kot |
| Vaughaus Thom | **Ivor Strom**; **Strom** | Settled (ST1, ST8). | EYE-vor STROM |
| Neros | **Neros** | Keep (ST9). | NEH-ross |
| the nobleman; Cassian Ault | **Cassian Ault** | Keep (ST13, R61-23). Named here from the case file; Volume II leaves him unnamed. Flag 3 is on "nobleman". | KASS-ee-un AWLT |
| his wife; the woman in the eastern lowlands | **Madeleine Ault** | Keep (ST12, R61-22). | MAD-uh-lin AWLT |
| Archivist Dessa Mael | **Dessa Mael**; "Archivist Mael" | Keep (ST17, R61-27). This is her first appearance on a page. | DESS-uh MAYL (sets R50-34's line; Mael as in Maelor, MAY-lor) |
| the pharmacologist | **Calla, distiller, of Castlefall**; "the distiller" in his entries | New, section 4. | KAL-uh |
| a senior archivist who has since retired | role | R50-27: no lines, and his notes are quoted as notes. | none |
| the Stage VI practitioner who heard Judicium | role | Career texture. Judicium is a canon Wellspring and stays. | none |
| the tanner | role | As in both volumes. | none |
| the Accord's observation post at Naln | **the Measurewrights' instrument chair**, a role | Rename (SE7, R61-121). The chair verifies the drift, and the Guild is canon ("under the Hexagonal Oath"). Unplaced unless the brief needs it; if placed, Nalūn, per the Volume II brief's unused plant. | none |

### Places

| Source form | Papers form | Verdict and ground | Say it |
|---|---|---|---|
| Castlefall; the tanner's workshop; the lower room | **Castlefall**; the flat above the tanner's; the lower room | Keep (SE1, SE3; R61-115, R61-117). | KASS-ul-fawl |
| the Castlefall railway platform; the coffee stand | **the station platform** (Volume II's cedar platform); **the coffee stall**, unnamed | Keep as places without names (R50-27's logic). It is distinct from the café on the square (Volume I). | plain |
| Genesio; the Genesio mountain territory | **Genesio** | Keep (SE1, SE3). | jeh-NEH-zee-oh |
| the Heralds' Archivum, lower stacks (Genesio) | **the Genesio Archivum**; its lower stacks; its sealed stacks | Keep (SE4, R61-118). Maelor's edict is over its door (R64-8). | plain |
| the Accord facility in Genesio | **the Genesio Archivum's assay room** | Rename (a call). Canon has no Accord house at Genesio. An archive that dates hands and inks (GL11) keeps an assay room, and assay rooms are canon ("the shielding of every assay room", The Apparatus of the Age). Flag 4. | plain |
| the Wellspring of Anamnesis (as a place) | **the Anamnesis site at Genesio**; **the site** | Rename (fixes; WS4, R61-70). "Wellspring" stays only where the current is meant. | plain |
| the eastern lowlands; a house with no name on the gate | **the eastern lowlands**, lower case | Keep as a description (Volume II names file, section 3). | plain |
| Urbis | **Urbis** | Keep (SE6, ST21). | OOR-bis |
| the Herald's Archivum (the Urbis anomaly log) | **the Urbis office's anomaly returns** | Rename, descriptive. Halveth grants access, so the register is her Division's, not the Heralds'. The Urbis Archivum in the Monastery's lower floors is where the Codex volumes were deposited and withdrawn under seal. | plain |
| the Trans-Alftian region, highlands and cold; the Alftian terraces | **Trans-Alftian** (his word); **the Alftian country**; **the terraces** | Keep. Volume II makes "Trans-Alftian" other people's word, and an Urbis man is exactly those people. The terraces are Ketsuen's limestone valleys (SE1). | tranz-ALF-tee-un; ALF-tee-un |
| Naln | **Vaultmere, Nalūn**, only if the Silent Archivists are cited | SE7. The macron stays (R50-15). The drift check itself is the Measurewrights'. | VAWLT-meer, nah-LOON |
| Research Archives Division, Guild Accord, Urbis | **the Research and Archives Division, Urbis office**; "the Research Division" as the short form | Fixes (L3, L17 and the rest); SE6 (R61-120). A regional desk; the Archives Eternal stays at the Citadel. | plain |
| Sum-gol (the delivery) | **Sum-gol** | Canon. The intercepted letter is carried to Mu-jin where he teaches in 700 to 701 IC. | SOOM-gol |

### Institutions

| Source form | Papers form | Verdict and ground |
|---|---|---|
| (the author's office) | **the Night Watch** (frame); **the Night Watch Society**, **the Society** (entries); **the Urbis chapter**; **the Ropewalk** | New and canon. Section 2. |
| the Guild Accord | **the Guild Accord**; **the Accord** | Keep: Halveth's side of the joint case. |
| the Heralds | **the Heralds**; **the Archivum of the Heralds** | Settled (SE5). The Latin, Ordo Praeconum Maeloris, has no place in a Watch file. |
| the Accord's observation post | **the Guild of Measurewrights**; the instrument chair | SE7. |
| the crown | **the crown**, unnamed | Night Watch canon never names it. Flag 2. |

### Documents

| Source form | Papers form | Verdict and ground |
|---|---|---|
| The Corrant Papers | **The Farrant Papers** | New. Section 1. As a wiki page under The Alftian Codex (ME1). |
| Alftian Codex Vol. I and Vol. II (restricted) | **The Alftian Codex, Volumes the First and Second, by Kwon Mu-jin**, withdrawn under seal | The archive title stands (ST22; R64-2). Gameung-nok is Mu-jin's own word and not a Concord investigator's. |
| the Necrocursica (sealed) | **the Necrocursica (sealed)**; cited only "as the Codex reports" | Keep (ST21, EC7, PA6; R61-66, R61-106). It is never "by Malphas" in this file (flag 1). |
| the Vaughaus Thom submission | **the Strom Submission** | Settled (Volume I registry). Filed in Genesio's sealed stacks under an anonymous depositor and a Castlefall postal address. |
| one unanswered letter from Gillus De Raits (original, intercepted) | **Draycott's second letter**; "the intercepted letter" | ST4 (R61-14). Its direction reads to Kwon Mu-jin (section 5). It is carried unopened. |
| Neros's astronomical readings | **Neros's readings**, of the Weight | SE8. Neros's own column heads may say "Tempus" (R61-122). |
| the review notes | **the review notes** | Keep, quoted as notes. |
| Ault's account, transcribed into a separate sealed document | **Ault's statement**, sealed | Descriptive, not a proper name. |
| the case file | **the Castlefall file** (Watch); **the Eastern Commission** (Division) | Section 2. |
| VOLITIONAL TRACE — ANAMNESIS WELLSPRING — ACTIVE | **the Genesio Activation Sequence** | Section 2. |

### Instruments (PA4: every reading is an instrument's or someone else's)

| Source form | Papers form | Ground |
|---|---|---|
| a resonance disc | **a field coil** (a reading), and **a Fixatio-anchored evidence tin** under **chapter wax** (the sample) | All canon: the Mancer's kit carries "a small field coil", and the Watch seals samples in Fixatio-anchored tins under the chapter's wax. "Resonance disc" is retired. |
| (none) | **a Clearbeam loupe**, **reference standards** | Canon (the Mancer's kit). Available for the ink. |
| (none) | **a regulation bracelet** | Canon Watch kit: "brass bands wound with fine grey wire", which pulls toward a suppressed practitioner. It is the Class Ø man's one warning at the Draycott meeting. Available, not required. |
| his field journal | **a notebook**; optionally a Sunkwood-boarded book | Sunkwood boards are canon (the Factor's Kit: "Essence-quiet, so entries are not contaminated"). |
| "the glyph associated with Gillus De Raits" | **Draycott's registered craft mark**: a ring crossed by three spokes, the lowest longest, registry letters beneath, in grey wax | R65-3; GL12 (R61-99). It is a mark, not a glyph. The registry has no proper name in canon, and "the register" (Accord Latin "in registro relatum") serves. |
| the ink that catches the light | **Gravetide Ink**, named when the Genesio assay returns | EC15 (R61-114). The circle is the Boundary. Gravemark Ink (GL7) is the Sealing and is not this ink. |

### Terms

| Source form | Papers form | Ground |
|---|---|---|
| Aetheric imprint | **Aetheric Residue** | Canon term (C-107's floor, R62-6). |
| Harmonic Imprint; Sympathetic Bond Trace | kept | K7, DE1. He knows them through the Codex (PA6). |
| Parunic trace | **Parunic Echo** | GL10 (R61-97). |
| Volitional Trace | kept, as Mu-jin's word, "unverified" in the frame | R65-10. The finding is Draycott's; the name and its boundary are Mu-jin's. |
| the Aphorism of Mortalis; "He summons himself ..." | the Aphorism; **Kwon Mu-jin's gloss** of it | GW9 (R61-87): the Papers' author credits the gloss to Mu-jin. |
| the Third Corruption | **Separation Perverted, the Corruption of Non-Commitment** | GW5 (R61-83): by name, never by ordinal. |
| Tempus | **the Weight** | SE8 (R61-122). "Tempus" appears only in Neros's readings and the Division's case title. |
| the Wellspring of Mortalis as threshold or courier | **Mortalis** | WS3: the gate, not a river. Farrant's "courier" metaphor is his own and can stand. |
| activation project; Anamnetic activation | **waking a Trace**, in speech | WS5. "Activation" survives only in the Division's case title. |
| Mortalis-adjacent; impression-body; the Great Work; the Hermetic principle | kept | Canon (K4; ST1). |
| Era of Voyagers | **Year 700 IC, the Withering Era; the tenth year of the Imperial Age** (and 701 IC, the eleventh) | R63-1 to R63-3, in Volume II's colophon form. |
| Level IV Clearance | **Clearance Tier IV Restricted (Mortalis Residue)**, with "Classification: Mortalis-adjacent" | EC7 (R61-106), in the Volume I and II form. The subject label is a call, parallel to Lyssara Veyn's "(Post-Temperance Corpus Studies)". |

---

## 4. Named for the first time

### Keva (Halveth's given name)

**Form:**
- Keva Halveth, given name first, as the Northern stratum writes it.
- Halveth is her **family name**. The source's "a woman named Halveth" is how an Accord colleague speaks: rank plus family name (R20-5).
- On the page she is only "Halveth". "K." appears once, in the frame's filing line.
- She signs margins "H." or not at all. Her order "not a report" is a condition of access (PA2).

**Culture and convention:**
- Keva is from the canon Concord pool (R20-3, female list).
- Halveth fits neither the pool nor a readable byname. It is an outlier and free (R50-18; the Volume II names file says the same).

**Meaning:** pool name, of no weight. Keva is an English spelling of the Irish Caoimhe, "gentle".

**Say it:** KEE-vuh HAL-veth

**Collision:**
- Keva matches 0 files, and the substring "kev" matches 0.
- Halveth matches 2 files, both Codex pages. Soft: Halvren (9), Halvard (2).
- Chosen over Dagna because "Halveth, D." would sit beside "Mael, D." in the same docket.

### Calla, distiller, of Castlefall

**Form:**
- Calla, with a **live** occupational byname and no surname.
- The Watch file lists her as "Calla, distiller, Castlefall"; his entries call her "the distiller".

**Culture and convention:**
- Northern stratum, the rural or small-town side of the class marker. A live byname reads as unchartered and "invisible to the Accord's filing system" (R20-1).
- The Watch file shows it on its face: a witness with no second field.
- Castlefall sits in Ketsuen's valleys toward the heartland (SE1), and a rail town's renting tradeswoman is ordinary there.

**Why a name at all:**
- She speaks twice (R50-27): what the circle means, and that the room has not finished processing.
- The Watch files every witness under a name.
- If the brief prefers her unnamed, nothing breaks.

**Her trade:** "distiller", from the source's own "distillation work". "Pharmacologist" goes as a period word for narration. If the brief makes her pour Drafts, canon's word is "a Drafter" (The Four Crafts).

**Meaning:** pool name, of no weight.

**Say it:** KAL-uh

**Collision:**
- Calla matches 0 files as a name. The substring appears only in "callable" and "recallable".
- Chosen over Pella because of Moros Pellayne (26 hits).

### Searcher, the Urbis chapter, the Ropewalk, the Castlefall file

See section 2.

---

## 5. Address, signature and frame lines

**The head** (Night Watch office style, PA5):

> THE FARRANT PAPERS
> Field notes kept on the crown's warrant by Niall Farrant, Searcher of the Night Watch Society, Urbis chapter
> Farrant, N., Urbis chapter, on the crown's warrant
> Joint case. Opened by Halveth, K., Research and Archives Division, Urbis office. Entered under the Society's warrant by the Society's secretary.
> Classification: Mortalis-adjacent. Clearance Tier IV Restricted (Mortalis Residue).
> Cross-reference: The Alftian Codex, Volumes the First and Second, by Kwon Mu-jin (withdrawn under seal); the Necrocursica (sealed); the Strom Submission (Genesio Archivum, sealed stacks); the Volitional Trace (unverified).

The wording is for the drafter. The name forms are fixed.

**Draycott's second letter, the direction on its outside (unopened):**
- "To Kwon Mu-jin, at the Archivum of the Heralds, Urbis". This is the Volume II names file's fallback form, which would explain where it was intercepted.
- The seal is Draycott's mark in grey wax (R65-3). This is what Farrant matches against the Ault document's seal. It is seen, never broken.

**A letter from Draycott to Farrant, if the brief keeps one:**
- Salutation: "To Niall Farrant, Searcher of the Night Watch Society, care of the Research and Archives Division, Urbis." Then "Farrant,".
- Draycott reaches him through the Division's address, not the Ropewalk. The Watch man has no signature to follow, only paper (PA4).
- Signed "G. Draycott".
- The postscript reads "Tell Kwon ...".
- It never names the Necrocursica's author (flag 1).

**The closing note:**
- Signed "N. Farrant, Searcher, Urbis chapter", dated "Urbis, Year 701 IC, the Withering Era; the eleventh year of the Imperial Age".
- The separate filing reads "the Genesio Activation Sequence (Division reference), open".

**Frame vocabulary (not names, but the frame's style depends on them):**
- **Time:** the Watch counts "divisions" (the Night Watch page). A rail town keeps the Guild hour on the station clock (The Apparatus of the Age). So the source's "at the second bell" becomes "at the second hour by the station clock".
- **Distance:** the Watch measures in miles, paces and inches ("forty miles of timber", "twenty-two paces"). Genesio is a day by rail and two days mounted (SE3). The source's kilometres and metres go.
- **Money:** the fee is three hundred gold marks (R65-2).

---

## 6. Not on the Papers' page

- **Malphas, by name, anywhere.** This covers the frame, the entries, quotations from Volume II that carry the name, and any Draycott letter (PA2's binding rule; flag 1).
- **The Mother**, **Zeraphine Drowl** and **the Pyraeon Forge Academy.** Farrant has no way to know them. The Mother does not yet exist as it will, and a Mother culture finds no signature of his (PA4).
- **Wystan Ashmore**, **the Night Register** and **Cutler Row.** They may exist in 700 IC, since Wystan has "eleven years on the desk" at 706. Keeping them off this page keeps the book's rule simple: nothing noticed across that line.
- **Geuk-hon, Kaalabad, Frithia and Rimward.** They belong to Volume III (MJ3, MJ12).
- **Gameung-nok.** It is Mu-jin's word, not Farrant's.
- **Ordo Praeconum Maeloris.** It has no place in a Watch file.
- **Doyun and Ara** may appear at Sum-gol as roles, or under their canon names if Mu-jin speaks them. No new name is owed.

---

## 7. Flags

1. **"No file names Malphas" against a Codex that names him.**
   - Volume II names Malphas throughout, including Draycott's first letter ("Malphas's manuscript"). Farrant has read it.
   - Proposed office reason, so the silence is the Watch's habit and not a gap: **a Night Watch file names only its parties of record.** Those are a witness met, a payer, and a hand sought. A man who is only the author of a cited document stands under his document, "the Necrocursica's author".
   - This fits the Register's "builds its file off whatever is written down". It is also exactly why no Watch file ever hands Wystan the name.
   - The brief confirms or replaces this reason.
2. **The crown's warrant in Ketsuen.**
   - Castlefall and Genesio are Ketsuen's (R61-115). Ketsuen is a meritocracy with a Council of Threads and no crown.
   - The crown's warrant runs in Urbis, a heartland city. Past the border, Farrant works only on the joint case's access, which is Halveth's Division and the Accord's circles. Her "not a report" order then becomes the price of that access, not a courtesy.
   - The crown stays unnamed. The brief states the mechanism.
3. **"Nobleman" in a meritocracy.**
   - Volume II's "a nobleman in the eastern lowlands" stands as Mu-jin's word.
   - Farrant finds Ault "through land records". If the lowlands are Ketsuen's, he can write "landholder" and let the Codex's word go uncorrected. That quietly catches the Codex, which is the Papers' job.
   - This is the brief's call (Volume II names file, flag 4).
4. **The Genesio assay.**
   - EC15 names the ink "when the Genesio analysis returns", but canon has no Accord house at Genesio.
   - Recommended: the Genesio Archivum's assay room, with **Dessa Mael** as the assay of record, since an archivist who dates hands dates inks. The Watch's rule puts her full name at the head of the docket, so no new name is needed.
   - If the brief wants a separate assayer, that person needs a full name then, in whatever register the Heralds' house uses. Check it against Maelor, Mael'Kara and Dessa Oth-Karreth.
5. **Soft collisions, all allowed under R50-17 and recorded only:**
   - Farrant with Farren (Tomas Farren, the Kharven thread).
   - Farrant with Ferriby (the Watch's founding tin).
   - Niall with Nol Tally, in the same Society.
   - Halveth with Halvren and Halvard.
   - Mael with Maelor: in an archivist of Maelor's order, the echo may be wanted.
   - If Farrant and Tomas Farren ever share a scene, it is a beat (R50-29).
6. **Searcher against "field man".**
   - Canon's existing word for a Society man in the field is "field man", and the book gives Wystan "the Night Watch Society's post as field man" after the Register folds.
   - Using it here would make Farrant the post's earlier holder. That is a live tie between the Papers and the night-watch book, and the book's rule is built to avoid such ties.
   - "Searcher" is a new office word, logged as a coinage (R50-28 logic; R16-6 asks that it be entered for ratification). If Isaac wants the tie, "field man" is a one-word swap.
7. **The investigator's sex.**
   - The chosen name is a man's, which keeps the source name and the published Volume the Third's "the kind of man".
   - Orin Farrant (Alternate A) is the one-word swap if Isaac wants a woman.
8. **"Twelve years" and "four hundred kilometres".**
   - These are dates and distances, not names. The Strom Submission's age is re-dated under ST2 and ML7. The anomaly cluster sits at Genesio itself (SE3), not four hundred kilometres off.
   - Recorded so the drafter does not carry the numbers into a filing line.

---

## 8. Registry pairs for ME2 (the Papers' additions)

These are to be entered when the conversion lands. The Volume I and II lists already cover Gillus De Raits, De Raits, G. De Raits, Vaughaus Thom, Thom Submission, Jabir, Paracelsus, Tat, Noxinus, Path of Silence, V.T., Naln and Herald's Monastery.

| Old | New | Scope |
|---|---|---|
| Oren Corrant | Niall Farrant | Codex pages and Lore & History (the overview :83; Volume the Third :25, :89, :164, :182) |
| O. Corrant | N. Farrant | Codex pages only |
| Corrant | Farrant | Codex pages only. Bare "Corrant" matches only those pages today. |
| The Corrant Papers | The Farrant Papers | Codex pages and Lore & History |
| Enforcer-Archivist | Searcher | The Papers and Volume the Third only |
| Research Archives Division | Research and Archives Division | Global (fixes) |
| Accord facility in Genesio | Genesio Archivum's assay room | The Papers only |
