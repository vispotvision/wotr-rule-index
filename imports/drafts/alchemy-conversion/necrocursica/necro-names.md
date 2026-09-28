# The Necrocursica, sealed edition: the names

Drafted 2026-09-28 as groundwork for Malphas's Necrocursica, the last of the five texts (ME3). This is the names pass only. The treatise itself is drafted after Volume III exists, and section 7 lists what it needs from that volume. Nothing here is written to the repo.

**Source:** /tmp/wotr-drafts/necro-source.md (the old text, about 6,400 words; K10 full rebuild, so it is notes to rebuild from).

**Decisions applied:** K2, K5 to K8, ST1, ST3, ST4, ST6 to ST8, ST12, ST13, ST21; ML1 to ML15; MJ6, MJ7, MJ9, MJ10, MJ13; GW1, GW4 to GW7, GW9; GL1 to GL3, GL5 to GL8; DE1, DE2, DE6, DE7; EC7, EC8, EC10, EC11, EC14, EC15; WS3, WS5; SE1, SE3, SE4; ME1 to ME3; PA2 and PA6 (for the Papers' side). Later rulings, which govern: open-conflicts-2026-09-28 (C-100, C-101), calendar-2026-09-28 (R63), malphas-living-2026-09-28, alftian-vol1 (R64), alftian-vol2 (R65, especially R65-3, -4, -5), alftian-vol2-credit-correction (R66-1), alftian-vol3-direction.

**Rules loaded:** load_rules [naming] (164 rows), plus [items] for the inks and reservations. The rows used: R50-01, -04, -05, -11, -12, -17, -18, -22, -23, -27, -28, -32, -34; R20-1, R20-4, R20-5; R23-2, R23-3; R14-5, R14-6, R13-6; R16-6; R47-5, R47-7; R61-8, -11, -31, -49, -50, -83, -94, -106, -110, -114, -128; R65-3, R65-4, R65-5; R66-1.

**Docket:** check_docket [naming, register, worldbuilding] shows nothing pending.

**stale_names (scope all):** 29 files, 177 hits, all Moto or Kharven material (Büri, Khökh, Altan, Sātūlagi and the rest). No Codex page, no Necrocursica source and no form kept or proposed here is a struck term.

**Collision method:**
- `grep -rliw` of every proposed and kept form across wiki/, scenes/ and book/, leaving out .manifest.json and INDEX.md. Counts below are files.
- Phrase greps for the source's own names, to find canon terms they already collide with.
- The three earlier names files (alftian-vol1-names.md, alftian-vol2-names.md, papers-names.md) are carried as settled; their forms are not rechecked.

**Three collisions the source names hit, found here:**
1. **"Resonance Lock"** (the Second) is a canon technique: the Sonochoral Conclave's defensive "Resonance Lock zones" (The Harmonic Arts:138).
2. **"Bleed"** (the Aetheric Bleed, the Fourth) is the Accord's filing word for a working with no operator and no edge ("a bleed with no operator indicated": The Night Watch:56, The Powers of the Imperial Age:175, Wystan's card, the_nights_watch.md:211; Papers:317), and the Veil page's **Bleed** field is waste heat off the Shell.
3. **"Unmoored"** is the third band of the Veil's **Drift Scale** (Loosened, Thinned, Unmoored, Adrift, Veil Pilgrim; The Veil:89), and EC9 ticks the Drift Scale for Mortalis Category Two and up. The list name is Isaac's (K8) and stays. Handling is in section 1 and flag 1.

A fourth, structural: **"Category"** is canon's Unified Taxonomy word, and its numbered list puts **3 · Conjunction** and **12 · Mechanica** under the same word the Necrocursica uses for "Category Three". Handling is in section 3.

---

## 1. The Seven Unmoorings

### The list

**Form:** the Seven Unmoorings. Singular: an Unmooring. The verb stays the text's own: "it unmoors them".

**Ground:** K8 (R61-8). The Heresiology keeps "the Seven Cacodaemonic Corruptions". Mu-jin coined that name in Volume I (Volume the First:175) and named three of them in Volume II, so it is his list; this one is Malphas's, and it takes its name from the sentence that closes his chapter four: "The answer, in all seven cases, is: it unmoors them."

**On the page:**
- Title page: "... and the Seven Unmoorings Arising from the Misapplication of Mortalis Law".
- Chapter the Third's head: "The Seven Unmoorings: Case Studies in the Misapplication of Mortalis Law". A colon, not the source's dash.
- Appendix II and the edition note: "the Seven Unmoorings".
- Each case is headed by its name alone. No ordinal, in the heads or in running text (R61-83 extended to this list: GW5 made every corruption a name, and the source's ordinals were what made "the Third Corruption" mean three things, audit gw-09 and gcm-07). The list keeps its order.
- Malphas uses the noun and the verb. He never writes the participle "unmoored" as a patient's state, which stays the Drift Scale's band word (flag 1).
- "Cacodaemon", "Corruption" and "inversion" never name one of the seven. They appear only where a case names the Heresiology stage behind it.

**Say it:** SEV-un un-MOOR-ingz

**Collision:** Unmooring and Unmoorings match 0 files. Unmoored matches 1 (The Veil, the Drift band). Recorded, allowed under R50-17, and handled by the participle rule above.

**Latin doublet:** none coined. R20C-46 allows one, but the obvious Latin, solutio, is also the chemist's word for dissolving and would sit on the Dissolution Wellspring. If the Accord ever files the list in Latin, it is coined then.

### The seven, in the source's order

| # | Source name | Sealed-edition name | Verdict | It unmoors them from | The Heresiology stage it names |
|---|---|---|---|---|---|
| 1 | The Mirror Trace | **the Mirror Trace** | Keep | their own direction | Dissolution Perverted, the Corruption of Submission |
| 2 | The Nospheric Resonance Lock | **the Worn Habit** | Rename | their own character | none; its canon kin is the Crossing's Melancholic Erosion |
| 3 | The Incomplete Sealing | **the Incomplete Sealing** | Keep | the line between what they made and what is making itself | Separation Perverted, the Corruption of Non-Commitment |
| 4 | The Aetheric Bleed | **the Open Shell** | Rename | the present | Conjunction Perverted, the Corruption of Instrumental Union |
| 5 | The Cacodaemon of Inversion | **the Averted Regard** | Rename | the living | Fermentation Perverted, the Corruption of Catastrophic Germination |
| 6 | The Cacodaemon of Nomenclature | **the Misnaming** | Rename | accuracy (the whole field) | Calcination Perverted, the Corruption of Conviction |
| 7 | The Cacodaemon of Completion | **the False Vocation** | Rename | themselves entirely | Coagulation Perverted, the Corruption of Tyrannous Finality |

All seven names match 0 files as phrases. Every one is two words or fewer (R50-11's spirit), plain English in the common tongue Malphas writes in, and none echoes an Earth person (ST1). Say them as plain English.

**Why not a one-to-one nesting.** The source says the first four are mechanical failures and the Fifth is "the first of the Corruptions that crosses from mechanical failure into ... ideological failure" (source:285). K8 says each "may" name the inversion that drives it, and the audit's option B (nest all seven) was rejected because the mechanical four bend under it (gw-08). So each case names the stage whose inversion honestly drives it, and one names none. A tidy seven-for-seven in the Heresiology's order was tried and dropped: it forces the Misnaming onto Distillation, which it contradicts, and makes the Worn Habit a matter of motive when it is a matter of standing in one room too long.

**How the names reach the page.** K2 puts the Heresiology after all five texts, so Malphas cannot cite it by title. He names each stage the way Mu-jin's Codex does: Volume II gives Conviction, Submission and Non-Commitment with their epithets, and the other four by stage name ("Conjunction Perverted"). The four epithets reach print in Volume III's one paragraph (GW6). If Volume III prints them as the Heresiology spells them, the sealed edition may use them; if not, it uses the stage names only. That is dependency D1.

**The one stage none of the seven names: Distillation.** No case is driven by Distillation Perverted, the Corruption of Sanitized Truth. That is the corruption the treatise itself commits. The Heresiology's own common expression for it is "Necromantic manuals whose warnings survive only as footnotes", its Case II is this book, and ML8 has the sealed edition cut the footnote. The absence is not a naming decision; it is left here for the drafter, who may let the older Malphas's margin against the Misnaming step toward it (ML9 puts margins on the Sixth). Nothing needs naming for it.

### Each, in full

**1 · The Mirror Trace** (keep)
- Mechanism: the Trace seeking completion takes the nearest committed intent, the practitioner's own, as its template. GL6 (R61-91) gives it a canon cause: the Continuum reads the practitioner's Attraction Layer into the working at the Authorization. The source's "Volitional Layer" becomes "Attraction Layer" (fixes).
- Why keep: exact, and it already carries "Trace", so a reader places it among the Volitional Trace's failures at once.
- Stage: Dissolution Perverted. The practitioner dissolves "into another will", and the Heresiology's list of wills includes "dead ideal". The audit reached the same pairing (ws-11). The cure the source gives, separation by a third party whom the practitioner resists, stands beside Submission's corrective, removal from the commanding field.
- Collision: 0. "Mirrorwell Prism" (an Artifacts page) shares a syllable only.

**2 · The Worn Habit** (rename from the Nospheric Resonance Lock)
- Why rename: "Resonance Lock" is a Sonochoral Conclave technique (The Harmonic Arts:138), and "Nospheric" goes in any case (ST21 to Noospheric; DE1 then narrows the Noospheric Echo to the held Echo of voice, habit and possession).
- Mechanism: long work in one place leaves the dead's habitual pattern carried on the practitioner's Shell, over their own. Habit is what DE1 leaves in the Echo, and the Shell is the outer layer, worn like a coat. "Worn" is both at once. People who knew the dead see it in the living man.
- Stage: none. This is proximity, not motive. Its canon kin is the Crossing's Lawful Echo, "hazardous by proximity", whose sustained exposure produces Melancholic Erosion and whose remedy is removal from the site (The Crossing:113). The source's own cure is relocation. The text may name Melancholic Erosion as its nearest relative.
- Form: "the Worn Habit". Lower-case "habit" in running text ("the dead man's habit, worn").
- Collision: 0. "Habit" is common prose (132 files) and names no term.
- Considered: the Borrowed Habit (clean, but "borrowed" is the Mortalis loan's word, WS3, and this is taken without a loan); the Second Habit; the Carried Echo (a third Echo on top of the Crossing's and the Noospheric).

**3 · The Incomplete Sealing** (keep)
- Mechanism: the Sealing is not finished. GL5 (R61-92) makes it an unsealed rune, an open wound that ambient pressure completes into a haunting. GL7 (R61-94) gives it a material cause: short or diluted Gravemark Ink.
- Why keep: "Sealing" is the canon Glyph role (Authorization, Boundary, Direction, Sealing), so the name states exactly which step failed.
- Stage: Separation Perverted. The source's third cause, "a failure of nerve at the final step", is Non-Commitment's "perfect diagnosis, absent intervention". Its corrective, decision under witness, is what the two practitioners of the delayed sealing did. ML9 puts one of the older Malphas's margins against this case. Mu-jin's own corruption is also Non-Commitment (MJ5), and he is the Codex's detector of failing seals (MJ11); the sealed edition can let the reader notice that without saying it.
- Collision: 0.

**4 · The Open Shell** (rename from the Aetheric Bleed)
- Why rename: "bleed" is the Accord's filing word for a working with no operator and no edge, the word Malphas's own later method is built to earn (the_nights_watch.md; The Night Watch:56). This failure is the opposite: an operator's Mechanica, with the operator as its edge. Keeping it would put the Night Watch book's key term into Malphas's mouth with a second meaning. The Veil's "Bleed" field (waste heat off the Shell) is a third sense. "Thinned Shell" was the first alternative and is out: Thinned is the Drift Scale's second band.
- Mechanism: GL8 (R61-95) makes it real Mechanica, Extraction from a dead donor. The Heresiology's Grade V says a Mechanica working cannot end, "so the boundary it opened stays open after the practitioner has gone home". The Open Shell is that boundary in the practitioner's own body: the Shell left open in the Mortalis band, so that everything ending anywhere comes in. The afflicted's own phrase, "the weight of all the ends", stays as their phrase, not the name, because "the Weight" is Tempus (SE8).
- Law: Malphas cites **Statute XXVI, Mechanica Irreversibility** (canon: The Magical Categories:132; the Summon Register:126; the Papers:337), not the Heresiology's Grade V, which is later (K2).
- Stage: Conjunction Perverted. Extraction joins a dead donor's law to a living working for use, which is the Heresiology's own Class IV argument under Instrumental Union: "Who bears the cost if the union refuses the joining? The donor, who is by definition dead". GL9 makes Strom's regional scaling the example.
- Collision: 0. No Aether Class or Crystal State is called Open (checked VII. Aether Class).

**5 · The Averted Regard** (rename from the Cacodaemon of Inversion)
- Why rename: "Cacodaemon" belongs to the Heresiology's list, and "Inversion" is its Grade III ("Cacodaemonic Inversion") and its general word for all seven.
- Mechanism: the practitioner's regard, both attention and esteem, turns from the living to the dead, until the living read as drafts of their residue. The source's people "describe them as already gone". Regard names both halves of the loss.
- Stage: Fermentation Perverted, which "begins to value the rot itself". This is Malphas's own canon corruption (card; ML2), ML9 puts a margin against this case, and the source's confession ("if I describe the echoes of the dead as more interesting than the people in the room, treat this document as a confession") is his. The Wellspring-level failure under it is canon's Mortalis failure, **Equilibration** (Vitalia:51: "they cool toward it without noticing"), which the text may name as the current's own tendency, since the Heresiology is not yet written.
- Collision: 0.
- Considered: the Turned Regard (sits on the alchemy's Twelve Turnings, GW2); the Early Crossing (a metaphor Malphas would strike as Misnaming).

**6 · The Misnaming** (rename from the Cacodaemon of Nomenclature)
- Mechanism: describing residues in the grammar of the living: the Echo called a mind, the Trace a will, the Corporeal Residue a body that remembers. It afflicts the field, not the man who starts it.
- Why this name: one word, in the -ing form of the list itself, and exact. It is also the book's central concern in one word: its footnote says "Never give it the name", and Malphas's later rule is "an anchor is a binding, and a binding is a name" (card, Lore).
- Stage: Calcination Perverted. Mu-jin's published Volume II already puts it there: "Every practitioner of Mortalis who insists an impression is the whole person belongs here", and the Heresiology's first common expression for Conviction is "Mortalis practitioners insisting an impression-body is the deceased whole person".
- Appendix II's charge (GW5, R61-83): Malphas calls Mu-jin's corruption Separation Perverted "and partly the Misnaming". That is his opinion of Mu-jin, not a correction of canon.
- Collision: 0. Soft: "The Misnamed Writ", a hook on Severin Bale's card (R50-17).

**7 · The False Vocation** (rename from the Cacodaemon of Completion)
- Why rename: "Completion" is Category Three's own word (Volitional Trace Completion). An Unmooring named for the working it corrupts would make the chapter unreadable.
- Mechanism: the practitioner's Attraction Layer is taken over by the Continuum's Mortalis repair, and it feels like purpose. The source's own line is the ground: "This sounds like vocation. I initially documented it as something close to sanctity." The name records his correction of his own first reading.
- Stage: Coagulation Perverted. The Heresiology's "soul-pattern of terrible stillness" and "practitioners who identify their own perfected state with reality itself" are the man on the platform "with the unhurried quality of something that has no experience of time passing".
- Soft echo, recorded: "vocation" shares its root with Vocatia, canon's calling layer of summons (DE4), and the practitioner here is the one being called. Wanted.
- Collision: 0. Lower-case "vocation" appears in two files as plain prose.
- Considered: the Emptied Will; the Vacant Will.

---

## 2. Title page, labels and signatures

### The title

The treatise's name, **the Necrocursica**, stays (ST21). It is the compellers' name, not his: Volume I has him say "They have named it already: the Necrocursica. They wish my name on it." The signature is his (ML4).

**Say it:** nek-roh-KUR-sih-kuh. Stress on the third syllable, c hard throughout.

**Title page, recast (name forms fixed; the drafter owns the wording):**

> THE NECROCURSICA
>
> Being a Complete Treatise on Cadaverous Alchemy, the Philosophy of the Persistent Dead, and the Seven Unmoorings Arising from the Misapplication of Mortalis Law
>
> Written under compulsion by Malphas, Scribe to the Genesio Archivum, by order, in his confinement at the Archivum of the Heralds, Genesio, by order of persons who will remain unnamed. Their persuasion is on his left hand.
>
> The sealed edition, annotated in a later hand by the same.

- **"Malphas"**, one name, as his card has it (ML4, R61-49). Never "N. Ren" or "Noxinus".
- **"Scribe to the Genesio Archivum, by order"**: the imposed sentence-title (ML5, R61-50), already in print twice: Volume I:109 in his mouth, and the Papers:271 as his written signature. The source's "Alchemist-Scribe of the Trans-Alftian Accord" goes (fixes: no regional Accord).
- **"the Archivum of the Heralds, Genesio"** replaces "the Genesio Monastery" (SE4, R61-118: the Monastery is at Urbis; Genesio's is the older outlying Archivum). Common form: the Genesio Archivum.
- **"Complete"** stays. It is his claim. The Accord's copy the reader holds is redacted (EC14), and the stamp below says so: the irony is left to stand.
- **The hand.** Healed into a small repeating lattice by the sealed edition (R65-5). "Has not yet fully healed" belongs to the first manuscript. The maker stays unnamed (ML3 makes it Zeraphine Drowl's; nobody on any page names her).
- **"Annotated against his will and then with growing enthusiasm"** is a chatty tic ML13 trims. The line becomes a plain edition statement.

### The two editions

| Name | What it is | Ground |
|---|---|---|
| **the first manuscript** | The text Codex I and II read: the three after-window residues and the footnote. Begun at Genesio in Volume I's last years, finished by the winter Volume II records (the Papers' notes derive 695 to 696 IC for the start, and Volume II has it "finished now" after the commission's pour, about 697 IC). Kept under seal below the gate. | ML7; the Papers:25 and :499 use exactly "the Necrocursica, first manuscript" |
| **the sealed edition** | The text this rebuild writes: the four forensic residues, the Mortalis Categories, the Seven Unmoorings, the after-window section (K7), the older Malphas's margins (ML9), no footnote (ML8). | ML7, ME3 |

- **The edition note** is headed **"On This Edition"**, short (ML7).
- In running text Malphas says "the first manuscript" and "this edition". The Accord's stamp says "the sealed edition".

### The sealed labels

The source has four joke-labels ("SEALED — ... — Level VI Clearance — ... this warning has been ignored before ..."). EC7 (R61-106) removes every numbered Level; ML13 trims the jokes and keeps command as his default. Labels split into two hands:

**His own, on the title page and at the close (command register, no contractions):**
> Sealed. Do not distribute. Read it through before you disobey.

The drafter picks the line; the forms fixed are "Sealed" and no Level.

**The Archivum's and the Accord's, as stamps (the house form the Codex volumes and the Papers use):**
> Sealed. The Archivum of the Heralds, Genesio; kept below the gate.
>
> Classification: Mortalis. Clearance Tier VI Restricted (Mortalis Operations).
>
> The Accord's copy. Preservable under redaction: the completion steps of Mortalis Category Three struck.
>
> Year ___ IC, the Withering Era; the ___ year of the Imperial Age.

- **"below the gate"**: the Papers' phrase for Genesio's sealed stacks (Papers:25, :245, :251), from the gate on the stair in Volume II. 1 other file has the words, unrelated (Rikkan Sahr's card).
- **"Classification: Mortalis"**, not the Codex's "Mortalis-adjacent": this book is the thing itself.
- **"Tier VI"** keeps the source's numeral, as the Codex and the Papers carried their "Level IV" across as "Tier IV" (flag 5 on the scale).
- **"(Mortalis Operations)"** is the subject label, parallel to the Codex's "(Hermetic Correspondence)" and the Papers' "(Mortalis Residue)". It is the source's own phrase, "Mortalis Operations".
- **"Preservable under redaction"** is the Accord's seizure class. The Heresiology prints it later, but the Accord's classes are older than that manual, and the stamp is applied whenever the Accord took its copy (EC14). Flag 6.
- **Date line** in R63's colophon form. The year waits on Volume III (D2).
- **The end line** replaces "END OF TEXT — GENESIO ARCHIVUM — SEALED ...": "End of the text. The Archivum of the Heralds, Genesio. Sealed."

### Signatures and margins

| Where | Form |
|---|---|
| Close of the preface, chapter four and Appendix II | **Malphas, Genesio** (the source's "N. Ren, Genesio"); Appendix II **Malphas** |
| The early epigraph ("I began writing this under protest ...") | **Malphas, margin, undated** |
| The older living man's margins (ML9, ML12, ML14) | **In the margin, in the author's later hand:** and no signature. The reader sees the hand change; the page never dates it. |
| Mu-jin's notes in the Genesio Archivum's copy (the four months unopened, which stays as ST4's echo; and the restored footnote, ML8) | **In the Genesio Archivum's copy, in the hand of Kwon Mu-jin:** He signs nothing and holds no title (MJ7). |
| "Internal thought, Noxinus Ren:" (source:369) | cut; the line becomes his first-person recollection (fixes; R48-40) |

The restored footnote is quoted in Mu-jin's note in exactly Volume II's wording (R65-4). The footnote has no name and gets none.

### Chapter and appendix heads

| Source head | Sealed-edition head |
|---|---|
| Preface: A Note on the Circumstances of Composition | keep |
| (none) | **On This Edition** (new, ML7) |
| Proem: The Alchemical Principle That Makes This Possible | keep |
| Chapter the First: On the Tria Prima of the Persistent Dead | keep |
| (none) | **After the Ninth Day** (new section for K7's after-window three; placed after Chapter the First's residues or as its close; 0 collisions as a head) |
| Chapter the Second: Glyphic Syntax in Mortalis Operations — A Practitioner's Compendium | **Chapter the Second: Glyphic Syntax in Mortalis Operations, a Practitioner's Compendium** |
| Chapter the Third: The Seven Cacodaemonic Corruptions — Case Studies ... | **Chapter the Third: The Seven Unmoorings: Case Studies in the Misapplication of Mortalis Law** |
| Chapter the Fourth: The Proper Relationship to What Remains | keep |
| Appendix I: The Stabilization Protocol for Volatile Residue Situations, as Developed by Paracelsus Furveus and Modified for Mortalis Application by Noxinus Ren | **Appendix I: The Stabilisation Protocol for Volatile Residue, as Developed by Furveus and Modified for Mortalis Work by Malphas** (printed in full, EC14; the "Technical Supplement" and its clearance joke go) |
| Appendix II: On the Relationship Between the Necrocursica and the Alftian Codex Trilogy | **Appendix II: On the Necrocursica and the Alftian Codex** |

---

## 3. Residues, Categories and the Noospheric Echo

### The four residues inside the nine days (K7: the forensic reading)

| Source form | Sealed-edition form | Verdict and ground | Say it |
|---|---|---|---|
| the four canonical residue categories | **the four residues** | Rename: "category" is kept for the Mortalis operations alone (below). | plain |
| The Corporeal Residue | **the Corporeal Residue** | Keep. 0 collisions. Distinct from canon's Aetheric Residue (the room) and Temperance residue (the Crossing's product it maps to, DE1). | KOR-por-ee-ul |
| The Aetheric Shell | **the Aetheric Shell** | Keep. It is the living Shell's field, detached, and DE1 and GW4 (Salt) already use the name. 0 collisions as a phrase; canon's living layer is "the Shell" or "Aether Shell". The text must say "detached" at first use. | ee-THEER-ik |
| The Nospheric Echo (13 uses) | **the Noospheric Echo** | Spelling fix (ST21, R61-31). Narrowed to the held Echo, voice, habit, possession (DE1); its place-imprint half moves to the Harmonic Imprint. | noh-uh-SFEER-ik |
| The Volitional Trace | **the Volitional Trace** | Keep. Credit per R66-1 (below). | vo-LISH-un-ul TRAYSS |

**Noospheric:**
- Greek noos, "mind", with sphaira, "sphere", in the adjective English already has from "noosphere". The old spelling dropped an o and meant nothing.
- It is an idea-name, kept under ST1. The coinage (Le Roy, Teilhard de Chardin, Vernadsky, 1920s) is credited in the author notes only (R48-27).
- The Sub-Stats page carries the old spelling once ("Nospheric intrusion", IV. The Eight Primaries:91). ST21 fixes it there too; that is a wiki fix outside this text.
- Collision: Noospheric 0; Nospheric 1 (that page).

**The credit line (source:93).** "Formalized ... through the collaborative work of De Raits, Thom, and Trismegistus" becomes R66-1's layers: Madeleine Ault found the Trace and designed her own commission; Ivor Strom found it independently; Gisli Draycott framed the theory and built the mechanism; Kwon Mu-jin named it and set its boundary (ST3, MJ13). Mu-jin is witness and namer, never co-builder.

### The three after the nine days (K7: what the places and bonds keep)

**Harmonic Imprint, Sympathetic Bond Trace, Parunic Echo**: kept exactly as Volume II prints them from the first manuscript. They go in the new "After the Ninth Day" section, so the Codex and Papers cite the book truly. The Parunic Echo is the Essence Signature in Aetheric Residue (GL10); "glyph-trace" stays retired.

### The Mortalis Categories

| Source form | Sealed-edition form | Reservation (EC10, R61-106) |
|---|---|---|
| Category One: Residue Identification and Forensic Analysis, "Accord Level III" | **Mortalis Category One: Residue Identification and Forensic Analysis** | reserved by the Bench at the **Adept gate** |
| Category Two: Residue Stabilization and Containment, "Level IV" | **Mortalis Category Two: Residue Stabilisation and Containment** | the **Expert gate** |
| Category Three: Volitional Trace Completion, "Level V with individual review" | **Mortalis Category Three: Volitional Trace Completion** | the **Expert gate, with individual review** |
| Category Four: full resurrection, "not authorized" | **Mortalis Category Four: full resurrection** | reserved at **no gate**: the refusal entry (EC8). Forbidden on paper (ML11). |

- **Why "Mortalis Category".** Canon's Unified Taxonomy numbers its Categories, and its 3 is Conjunction and its 12 is Mechanica. A bare "Category Three" beside "Mechanica" in the same chapter reads as the taxonomy's. So: "Mortalis Category One" at the first use in each chapter and in every index row EC8 creates (the R47-2 entries and the Spell Index rows); inside a chapter already about Mortalis operations, "Category Three" may stand. Numerals are written as words, never "I to III".
- **"full resurrection"** stays lower case, the older texts' word. Resurrection appears in 19 files as ordinary prose; no canon term.
- **"Reserved by the Bench"**: the Bench of Attribution (R18-5 names it), in the Papers' form "reserves it at the Expert gate". Rank gates by name, never T-numerals (R47-7; fixes).
- **The source's joke** ("Do not file a Category IV application ... it will go on your record") may survive in his command voice: "Category Four is reserved at no gate. An application goes on the applicant's record and nowhere else."
- **C-128.** The Categories are codified in this book. The sealed edition is the first document that may number them, and it comes after Volume III; no earlier document numbers them (D6).

---

## 4. Every other name the sealed edition uses

"Keep" means the form passes ST1 and the naming law as it stands. Forms settled in the earlier names files are carried without rechecking.

### People

| Source form | Sealed-edition form | Verdict and ground | Say it |
|---|---|---|---|
| Noxinus Ren; N. Ren | **Malphas** | Settled (ML4, R61-49; ME2). | MAL-fas (card) |
| Gillus De Raits | **Gisli Draycott**, then **Draycott** | Settled (ST1, ST7). The preface's joke survives: he agrees to omit the names and then names one. | GIS-lee DRAY-kot |
| the second visitor, who "goes by a title I will not reproduce" | **unnamed; the title not set down** | ML3 makes her Zeraphine Drowl. Canon gives her no Academy-era title, and the source's own line refuses to print one, so nothing is invented. The Pyraeon Forge Academy stays off the page. | none |
| Paracelsus Furveus; Paracelsus | **Furveus** | Settled (ST1, ST6). His quotation in chapter four is Furveus's. His years at the Heralds' Medical University are his own, not "our" (fixes). | FUR-vee-us |
| Vaughaus Thom | **Ivor Strom**, then **Strom** | Settled (ST1, ST8). | EYE-vor STROM |
| Vis Trismegistus; V. Trismegistus; Vis | **Kwon Mu-jin** at first mention, then **Mu-jin** | Settled (fixes; MJ7). Malphas calls him Mu-jin, as in Volume II's address table. Never "K. Mu-jin" (a Korean-stratum name takes no initial), never "the Thrice-Great". | KWON moo-JIN |
| Madeleine Ault; Cassian Ault | **Madeleine Ault**; **Cassian Ault** | Keep (ST12, ST13). A sealed book may name them, as the source does. "Cassian Ault's commission" becomes hers, which he paid for (R66-1; Volume II). | MAD-uh-lin AWLT; KASS-ee-un AWLT |
| O. Corrant | **O. Farrant** (Orin Farrant) | Settled by the Papers draft. Malphas may name her; PA2's rule binds Watch files, not his. The asymmetry, his treatise naming the Searcher whose file will not name him, is left to stand. | OR-in FARR-unt |
| the man on the Genesio platform | role | R50-27. He is the False Vocation's one terminal case and speaks nothing. | none |
| the two Accord practitioners of the delayed sealing | roles | R50-27. Their report goes into Appendix I as the protocol's worked case (EC14 calls the protocol "the defensive counter to a failing seal"), not a new appendix. | none |
| the nearest Guild Accord archivist | role | Keep. | none |
| liches | **lich**, **liches** | The canon word (the Lich page; the card's "lichdom"). ML12's one margin line names them and stops. | LITCH |

### Offices and bodies

| Source form | Sealed-edition form | Ground |
|---|---|---|
| Alchemist-Scribe of the Trans-Alftian Accord | **Scribe to the Genesio Archivum, by order** | ML5 (R61-50); fixes |
| the Guild Accord; Accord investigators | **the Guild Accord**; **the Accord**; Accord investigators | Keep |
| Research Archives Division | **the Research and Archives Division** | Fixes. Its **Mortalis Branch** is canon (Lyssara Veyn's card) and available for whoever holds the Accord's copy. |
| (reservations) | **the Bench of Attribution**, **the Bench** | R18-5; EC7, EC10 |
| the Enforcement Division | **the Enforcement Division** | Canon; it prosecutes extraction (the Papers:337). For the Open Shell. |
| the Heralds | **the Heralds**; **the Archivum of the Heralds, Genesio** | Settled (SE4, SE5). The Latin, Ordo Praeconum Maeloris, stays off: Malphas is not the order. |
| the Night Watch Society | **the Night Watch Society**, in the cross-reference only | Canon; the Papers' office |
| Master of the Circle | **Master of the Circle** | Canon (EC12; Volume II). Furveus's rank, if the commission is mentioned. |

### Documents

| Source form | Sealed-edition form | Ground |
|---|---|---|
| The Alftian Codex, Volumes I–III, authored by Vis Trismegistus | **The Alftian Codex, Volumes the First to the Third, by Kwon Mu-jin** | ST22 and R64-2: the archive title. Gameung-nok is Mu-jin's own word, and Malphas does not use it. |
| The Corrant Papers (O. Corrant, Research Archives Division, Guild Accord) | **The Farrant Papers (O. Farrant, Searcher of the Night Watch Society, Urbis chapter; a joint case with the Research and Archives Division, Urbis office)** | Papers draft; PA2 |
| On the Fourth Residue Category and Its Application to Anamnetic Wellspring Activation (G. De Raits, V. Thom, annotations V. Trismegistus) | **the Strom Submission (the Genesio Archivum, below the gate), with Kwon Mu-jin's annotations** | ST2: the old paper is Strom's. MJ13: Mu-jin annotates it. No co-authored Draycott paper exists, and none is invented. "Anamnetic Wellspring Activation" goes (WS5). When Mu-jin annotates it is D4. |
| Standard Accord Protocols for Mortalis Operations, Categories I–III | cut | This book is where the Categories are first codified (C-128), so no earlier Accord protocol can exist. |
| the collaborative Accord document (source:109) | cut | Same ground. |
| (the Genesio activations) | **the Genesio activations**; the Division's reference **the Genesio Activation Sequence** may be cited | The Papers; Heresiology Case IV. ML14's margin hints at his part; his name stays under Strom's signature. |
| the Aphorism of Mortalis | **the Aphorism of Mortalis**; **Kwon Mu-jin's gloss** of it | GW9 (R61-87) |
| the Technical Supplement | cut | EC14 prints Appendix I in full |
| Heresiology of Alchemy | never cited | K2: written after all five texts |

### Places

| Source form | Sealed-edition form | Ground | Say it |
|---|---|---|---|
| Genesio | **Genesio** | SE1, SE3 | jeh-NEH-zee-oh |
| the Genesio Monastery | **the Archivum of the Heralds, Genesio**; **the Genesio Archivum** | SE4 | plain |
| (the sealed stacks) | **below the gate** | The Papers | plain |
| my apartment in Genesio | **my rooms in the archive-town** | SE3 | plain |
| a Genesio waystation | **the Genesio waystation** | SE3: one railhead waystation (2 files) | plain |
| the mountains | **the mountains**, or **the Uplands** | SE1 | plain |
| the Heralds Medical University | **the Heralds' Medical University** | Volume I's form | plain |
| (Strom's postal address) | **Castlefall** | The Papers | KASS-ul-fawl |
| (the commission's destination) | **the eastern lowlands**, lower case | The Volume II names file | plain |
| (the Codex deposits) | **Urbis** | SE6 | OOR-bis |

### Instruments, inks and reagents

| Form | Use in the sealed edition | Ground |
|---|---|---|
| **Gravemark Ink** | The Sealing ink of the lawful Category Three formula; short or diluted ink as a material cause of the Incomplete Sealing. Entered at the Adept rank of the Index, reserved at the Expert gate (the Standing Index:127; the Papers' reading). | GL7 (R61-94) |
| **Gravetide Ink** | The Boundary ink, where a Category Three circle is drawn (Class III ritual ink, Au and Dr; the Alchemical Index:68). | EC15 (R61-114) |
| **Stillgate Ash** | The ring that grounds an impression-body so it can pass, and bleeds any living Essence at the ring. Journeyman gate. | EC11 (R61-110); Volume II:52 |
| **the Mortalis seal** | Category Three's seal, closing on [Vor] Return as its end condition. Lower-case "seal". | GL3 |
| glyphs | **[Ie] Perception**, **[Ur] Balance**, **[Flx] Flux**, **[Tp] Topology** (Category One's close: "Flx, sealed by Tp on a Fixatio chain"), **[Vor] Return**, **[Au] Death**. Index names only (GL1). Ie, Ur, Flx, Vor and Au are attested on the wiki in these forms; Tp comes from the ruling (GL2) and must be checked against the Master Codex's Glyph Index before print (R18-4). | GL1 to GL3; fixes |
| Glyph roles | **Authorization, Boundary, Direction, Sealing**, in that order | fixes |
| the vessel | **a Field Substrate Draft**, graded by Class, Fidelity and Carry | DE5; R65-2 |
| **the Returner** | Circulation vessel, if Distillation at the bench is mentioned | GW3; Alchemetrica:163 |
| **field coil**, **gauge**, **Fixatio-anchored tin** | Available instruments for Category One | The Papers; canon kit |
| **registered craft mark** | Draycott's: a ring crossed by three spokes, the lowest longest, in grey wax | R65-3 |

### Terms and Wellsprings

| Source form | Sealed-edition form | Ground |
|---|---|---|
| Cadaverous Alchemy; the Persistent Dead; the Persistently Living | keep | His coinages; 0 collisions |
| Tria Prima; Sulphur, Salt, Mercury; Spagyria | keep | ST1; GW4 maps them to Core, Shell, Attraction Layer |
| Iatrochemist | **iatrochemist**, lower case | Idea-word (ST1); 1 file has "iatrochemistry" |
| impression-body; revenant | keep | DE6 makes the revenant a stalled Crossing |
| necromantic | keep, with DE7's one legal note | DE7 |
| Paru's First Speech | keep | Canon: Alchemetrica:23 |
| the Anamnetic fabric | **Mnemata**; "the ground's record" | WS5. Anamnetic survives only as a spelling where a word stays (ST21). |
| Anamnetic Wellspring Activation | **waking a Trace** | WS5 |
| Calcination, Distillation (as Wellsprings) | bench operations | K6 |
| Sublimatio-aligned cleansing | **Sublimare-aligned** | K5 (R61-5) |
| Distillation-aligned glyph chains | **Sublimare-aligned** | K5, K6: Distillation is a bench operation that mirrors Sublimare |
| the constructive-alignment Wellsprings | **Ascensio, Fixatio and Benediction**, three currents from Vectoria, Materia and Vitalia | fixes |
| Wellspring Communion | keep | Canon (4 files) |
| Luminalis; Tenebra | keep | Canon |
| Temperance stage | **Stage** | fixes; capital Stage is only Temperance |
| the Volitional Layer | **the Attraction Layer** | fixes |
| Mechanica impression | **an open boundary** (Category One) | fixes |
| Equilibration | available for the Averted Regard | Canon Mortalis failure (Vitalia:51) |
| Melancholic Erosion | available for the Worn Habit | Canon (The Crossing:113) |

---

## 5. Not on the sealed edition's page

- **The Mother**, **Osric Salter**, **Greyshaft Nine**, **Project Zombification**, the cell: the cult and the lich work under other names (ML6), and the Watch book's rule keeps his work and his names apart.
- **Zeraphine Drowl** and the **Pyraeon Forge Academy**: the second visitor stays unnamed.
- **The Heresiology of Alchemy** by title (K2).
- **Gameung-nok** and **Ordo Praeconum Maeloris**: not his words.
- **Frithia, the children, Doyun, Ara, Geuk-hon, Kaalabad, Rimward**: nothing in this treatise needs them, and the Frithia timeline is being settled separately.
- **Noxinus, Ren, Gillus, De Raits, Vaughaus, Thom, Paracelsus, Trismegistus, Vis, Corrant**: gone everywhere (registry, section 8).

---

## 6. Address

| Speaker in the text | Form |
|---|---|
| Malphas, of Mu-jin | Kwon Mu-jin at first mention, then Mu-jin |
| Malphas, of Draycott, Strom, Furveus | surname: Draycott, Strom, Furveus (Furveus is his only name) |
| Malphas, of himself | "I"; in the title page and signatures, Malphas |
| Mu-jin, in his notes, of Malphas | Malphas |
| The Accord's stamp, of him | the author; the stamp never names him |

---

## 7. What the sealed edition needs from Volume III (dependencies)

Nothing above depends on Volume III's unwritten content. These are the places where the sealed edition must cite or answer it, and what each needs.

- **D1 · The four epithets.** Volume III's one paragraph (GW6, R61-84) must print Instrumental Union, Catastrophic Germination, Sanitized Truth and Tyrannous Finality exactly as the Heresiology spells them, "X Perverted, the Corruption of Y". Otherwise the Open Shell, the Averted Regard and the False Vocation name their stages by stage name only.
- **D2 · Its deposit year.** The sealed edition's date line comes after Volume III's deposit and before the Becoming (the margins are the living man's, ML9). Greyshaft Nine is 706 IC. The window is fixed only when Volume III is dated.
- **D3 · The copy sent.** Appendix II says Mu-jin sent Malphas the third volume "and asked me, in his letter, to tell him what I thought". Volume III must allow that (Volume II already sends Malphas a fair copy of itself). Otherwise Appendix II's opening is recut.
- **D4 · The annotations to the Strom Submission.** MJ13 has Mu-jin annotate it. The cross-reference cites "with Kwon Mu-jin's annotations" only if Volume III, or its years, has him do it.
- **D5 · The eighth vow.** If Appendix II answers Mu-jin's vow against his own corruption (GW7), it quotes Volume III's exact wording.
- **D6 · No numbered Categories in Volume III** (C-128). The sealed edition is where they are codified. If Volume III is made the place instead, the sealed edition cites Volume III's framework and this file's section 3 re-points.
- **D7 · The epigraph.** MJ9 makes Volume III's epigraph a margin note in Malphas's hand in Mu-jin's copy of Volume II. The sealed edition's own margins must not repeat or contradict it; Volume III owns its words.
- **D8 · "Separation Perverted, and partly the Misnaming."** Appendix II's charge answers Volume III's arc (the source: "two volumes avoiding the obvious and a third running toward it"). The charge's name forms are fixed here; what it charges depends on what Volume III shows him doing.
- **D9 · Mu-jin's standing when he writes his note** in the Genesio Archivum's copy (ML8). MJ10 brings the Accord in from Volume III. The note's label carries no title either way.

---

## 8. Flags

1. **The Drift Scale's "Unmoored."** K8's name stands. The text keeps the participle off patients. Recorded: the False Vocation's terminal case, "too thin to remember wanting" in the Veil's words, resembles the Veil Pilgrim at 100, and EC9 ticks the Drift Scale for Category Two and up. Whether the Seven and the Drift Scale are one loosening seen twice is not a naming question; the drafter should not assert it (R16-6: both readings stated).
2. **C-125 stays open.** ML4 (signed "Malphas") and PA2 (no Watch file names him) both hold on their own ground: the rule binds Watch files, and this is his book. The title page carries name and imposed title together, which also squares with the Papers' "File me by the title". Recorded, not ruled.
3. **C-127 stays open.** Whose hand wrote the commission's Sealing (Furveus poured and sealed it, Volume II; GL5 traces Draycott). The sealed edition names Gravemark Ink as the lawful Sealing and does not say whose hand used it.
4. **The Worn Habit and the Aetheric Shell both sit on the Shell,** as does the Open Shell. Three uses of one layer are correct (the Shell is where all three happen) but the drafter must name the layer at each first use.
5. **"Tier VI Restricted."** Lyssara Veyn, a senior Mortalis scholar, holds Tier II Restricted, so the direction of the clearance scale is not settled by canon. The numeral is carried from the source's "Level VI" as the Codex and the Papers carried theirs. If the scale runs the other way, the numeral changes and nothing else does.
6. **"Preservable under redaction"** is the Heresiology's seizure class, and the Heresiology is later (K2). The stamp assumes the Accord's classes predate its manual. If not, the stamp reads "The Accord's copy; the completion steps of Mortalis Category Three struck", without the class.
7. **Sanitized Truth is the one stage none of the seven names** (section 1). A design note, not a naming decision.
8. **The first manuscript's dates** differ slightly between the Papers' derivation (695 to 696 IC) and Volume II's "finished now" after the pour (about 697 IC). Begun and finished, both hold; the edition note should give only "at Genesio" unless the brief fixes a year.

---

## 9. Registry pairs for ME2 (the Necrocursica's additions)

The Volume I, II and Papers lists already cover Noxinus Ren, Noxinus, Gillus De Raits, De Raits, G. De Raits, Vaughaus Thom, Thom Submission, Paracelsus, Vis Trismegistus, V.T., Oren Corrant, O. Corrant, Corrant, The Corrant Papers, Research Archives Division and Herald's Monastery.

| Old | New | Scope |
|---|---|---|
| N. Ren | Malphas | Necrocursica only |
| Nospheric | Noospheric | Necrocursica and the Sub-Stats page (ST21) |
| Seven Cacodaemonic Corruptions | Seven Unmoorings | **Necrocursica only.** Never global: the Heresiology, the Codex and the Crossing page keep the old name for Mu-jin's list. |
| Nospheric Resonance Lock; Resonance Lock | the Worn Habit | Necrocursica only (the Harmonic Arts' Resonance Lock stays) |
| Aetheric Bleed | the Open Shell | Necrocursica only |
| Cacodaemon of Inversion | the Averted Regard | Necrocursica only |
| Cacodaemon of Nomenclature | the Misnaming | Necrocursica only |
| Cacodaemon of Completion | the False Vocation | Necrocursica only |
| Alchemist-Scribe of the Trans-Alftian Accord | Scribe to the Genesio Archivum, by order | Necrocursica and the Codex overview page |
| Genesio Monastery | Genesio Archivum | Necrocursica only (SE4) |
| Heralds Medical University | Heralds' Medical University | Necrocursica only |
| Level VI Clearance | Clearance Tier VI Restricted (Mortalis Operations) | Necrocursica only |
| Alftian Codex Trilogy | the Alftian Codex | Necrocursica only |
