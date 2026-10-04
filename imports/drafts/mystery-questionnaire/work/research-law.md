# Mystery, horror and intrigue: the current law

Research for the mystery, horror and intrigue questionnaire, 2026-10-04. It maps what the index already rules on fair clues, how secrets surface, horror pacing, the Night Watch and forensics, courts and jurisdiction, faction intrigue, and lies that stay uncorrected. Each dimension gives the live rows with ids and short quotes, then splits **settled** (do not re-ask) from **open** (a question the questionnaire can put).

Sources: `desktop/NATALIE.md`, `rules/*.yaml`, `RULINGS.md`, both questionnaires' `decisions.md`, `CONFLICTS.md`, `table/`, `out/docket.md`, the wiki page *The Night Watch*, and the Night Watch book bible.

Three facts frame everything below:

- **The docket is empty.** `out/docket.md` reads "0 outstanding", and no rule row is `proposed` or `pending`. Nothing in this territory waits on a ratification.
- **Combat Law R71 is ruled but not yet written as rows.** The RULINGS entry says the rows will be `rules/doc-combat-law-2026-10-04.yaml`, "whose id numerals are the numbers here". This report cites R71 by its RULINGS item number and questionnaire key (for example R71 item 81, AL12), not by a row id, because the row slugs do not exist yet.
- **One open conflict sits in scope:** C-125 (whether a Night Watch file may name Malphas). C-124 (Pressure on the unranked, "felt as dread") is answered in substance by R71 item 41 (MC15) and should close when the rows land.

---

## 0. Settled by the Style Law (R70) and the Combat Law (R71): do not re-ask

These answers touch mystery, horror or intrigue and were given in the last two days. The questionnaire should list them as settled and build on them.

**From R70 (style law, 2026-10-03):**
- The Mystic register draws on "Japanese and Chinese literary craft and the gothic (law, the half-seen)" (R70-9); what the world does is "Law stated, reasons kept" (R70-76).
- The narrator may foreshadow only in a chapter's opening and closing lines (R70-10).
- Openings may be a document or readout "that the scene then tests" (R70-16); chapters may open on an in-world epigraph or case-book (R70-23).
- Closings: the mid-crisis cliffhanger, a notice or readout, the break-off where "the next scene owes what was withheld" (R70-17).
- Document forms include **records of the strange** (the *zhiguai*, a Chinese form that sets down a strange event as plain witness and closes on the recorder's comment), court annals and memorials (R70-67). A rite is a numbered form the scene performs and departs from (R70-75).
- Reasoning may show as stepwise lists, the unsaid, or reasoning from figures (R70-38).
- Comedy may sit "hard against dread"; inside danger, gallows wit only (R70-116).
- The POV's culture misreads the room, and a misread folk belief stays uncorrected (R70-44).
- Every public reversal "opens a Front or a Ledger debt" (R70-112).
- Court speech, ceremony forms, proverb duels and verse contests (R70-108 to R70-111); power on show, courts and punishments in description (R70-42); law as an Inventory field (R70-45); contract hooks with reward and penalty (R70-97); the episodic job and the Well delve as arcs (R70-18).

**From R71 (combat law, 2026-10-04):**
- K6: the deciding fact shows beforehand "in the POV's read or a second's mouth". K7: every fight has "at least one findable line out".
- K9, "The tell placed, the read his": Natalie puts the evidence in the room and never draws the conclusion for his PC.
- CW14: a tell is shown plainly twice "and read at length at the third". MC4: a held reveal acts earlier as evidence; "The notes list each planted sign." MC9, WT5, FT17: a second wind, a stale round, a coming loss each need a planted sign.
- AL11: real poison tests by place (the mirror test, which leaves a metal spot on cold porcelain; the copper test; the iron antidote), not in the north. AL12: a forensic reading plays as action; "The contradiction between the instruments is the scene's turn."
- AL13: corruption signs, "One sign a scene at most." AL15: every forgery "always findable by mark, assay or the Index's own failure". AL14, AL17, AL18: late death by fumes; revenants obey anatomy; an impression-body (a dead person's likeness built from their Trace) leaks "a seam the reader catches".
- CW11 and WT12: killings carry their culture's legal aftermath, "Proof decides", jurisdiction contests open Fronts, an undeclared killing by next dawn is murder. CW13: lies and accusations are moves in a fight.

---

## 1. Table Rule 8: ignorance and lies

**The rule.** NATALIE.md, Table Rule 8: "One thing per turn his PC notices and you don't explain. One thing per session an NPC tells him that is wrong and stays uncorrected until he catches it." It is **not an indexed row**. The table rules live only in the standing prompt; the index carries Rule 5 through R13-8 and R14-3, and nothing for Rule 8.

**Its lineage.** Pack Six's ignorance quota and misreading budget (R6-3-IGNORANCE_QUOTA, R6-4-MISREADING_BUDGET) and Pack Twelve's retention of them (R12-7-IGNORANCE_MISREADING_RETAINED) are all superseded by **R49-11-NOT_KNOWING** (prose law, 2026-09-26): the quotas "become optional; no per-scene minimum." Prose has no quota; the table prompt still states a per-turn and per-session floor. They do not contradict on their face (R49-11 governs scenes, Rule 8 turns), but nothing records whether R49-11 was meant to loosen the table too.

**Live rows that do the work Rule 8 describes:**
- R12-4-VOICE_ONE_POV: a confident wrong explanation "is now the most valuable tool in the kit." R5-C1-WELL_REASONED_WRONG_CONCLUSION: "Irony built on a character being stupid is not irony" (relaxed by R70-112 for the arrogant). R49-08-MEANING: the POV may reflect "and may be wrong".
- R48-42-LIES: "Frequent lies: many NPCs lie for their own reasons; the player has to catch them." R49-36-LIE_TELLS: "Every lie leaves a catchable tell: a body tell, a fact that doesn't fit, or a detail changed later."
- R48-36-NPC_WITS and R57-10-NEVER_RIGGED: NPCs "never omniscient, never dumb".
- R53-15-FOLK_BELIEFS ("the narration never corrects them"); R48-24-4_THEORIES (they "colour reads and mistakes"); R11-4-DESCENT_PROSE_LAW (inside a Well ignorance "is the ambient condition", and the one read "should usually be spent wrong").

**How the table already practises it.** All ten NPCs in `table/npcs.yaml` carry a `lied_about` field. Josse Osricsson's is an honest error, "Uncorrected until someone reads the intake sheet". The Night Watch book bible keeps a "What Wystan believes that is wrong" list; one item is never corrected and is "the book's standing irony".

**Settled.** Lies are frequent, motivated, and tellable. Wrong conclusions must be well reasoned except for the arrogant before a fall. Folk belief is never corrected by narration. The roster records each NPC's lie.

**Open.**
1. Does Rule 8 still bind roleplay turns as a minimum after R49-11, or is it now a target, or retired to match prose?
2. Is "one thing per session" a floor under R48-42's "frequent", or the count of the one **load-bearing** lie per session that the Ledger tracks?
3. What counts as "catching" it: Isaac naming the lie in chat, his PC acting on the truth, or a fact on the page that contradicts it?
4. If he never catches it: does it pay off in the world (a Front ticks on it), stay forever, or get revealed at an arc's end? R48-48-EXPLAIN says the partner explains physics "only when asked"; nothing says whether that extends to lies.
5. Honest error against deliberate lie: both appear in the roster under one field. Are they one budget or two?
6. The unexplained thing per turn: must it pay off later (R6-3 required it; R49-11 dropped the requirement), and is there a ledger of planted mysteries?

---

## 2. Fair clues and foreshadowing

**Live law.**
- R48-30-SURPRISES: "Big surprises (betrayal, ambush, death) only after foreshadowing a player could have caught."
- R48-31-STAKES: death "from real mistakes after clear warning".
- R13-8-RECONSTRUCTIBLE_ADJUDICATION: an outcome must be reconstructible; "A fight that resolves because the scene needed it to has failed".
- R57-09-FULL_KNOWLEDGE and R57-10-NEVER_RIGGED: Natalie draws on everything, meta knowledge included, and never rigs "in either direction".
- R12-3-NAMED_INVENTOR_RULE: a documented technique "is counterable by anyone who studied it"; a self-derived one "must be read live".
- Table Rule 6: "The read is the game. Give him the tells."
- R61-55-MOTHER_TEACHES_NECROCURSICA: the cult's methods trace to the book's protocols, "a counter someone can find". R61-85: "Every corruption gets a named, findable counter."
- R71: K6, K7, K9, CW14, MC4, MC9, WT5, FT17, AL13, AL15, AL18 (listed in section 0). Together they make a fair-clue law for fights and alchemy: plant before, show twice, let the player do the reading, list the planted signs in the notes.

**Settled.** Big surprises need a catchable sign. The player does the deducing for his PC. Corruption, forgery and the cult's work are always findable. The author notes name what was planted (MC4) and what decided (R13-8).

**Open.** Everything above was ruled for fights, items and corruption. Nothing rules a **mystery's** clue economy:
1. How many clues per conclusion (Justin Alexander's Three Clue Rule, from tabletop practice, plants at least three for any conclusion the players must reach)?
2. Where clues live: in the room, in mouths, in documents, in readouts.
3. Whether a mystery's notes carry a clue list (the MC4 practice, extended), so Isaac can audit fairness after.
4. Red herrings: legal, and if so must each be refutable on the page?
5. The fail state: if the clues are missed, does the culprit win, does the world move by Fronts, or does a second route open?
6. Whether CW14's "shown twice, then read" applies to investigative tells as well as fighting tells.

---

## 3. How secrets surface: the iceberg, the voices, the documents

**Live law.**
- NATALIE.md, Iceberg: "reader sees ten percent. No 'as you know.' Exposition through disagreement, negotiation, or a real knowledge gap." R19-4-ICEBERG_DIALOGUE: "nobody explains anything they both already know."
- The four explaining voices, at most two per engagement (R12-4-VOICE_MIXING_RULE): the POV's own read (R12-4-VOICE_ONE_POV), the knowledgeable second with "an actual reason for them to be present and talking" (R12-4-VOICE_TWO_SECOND), the opponent's contempt (R12-4-VOICE_THREE_OPPONENT), and the document, "The LotM model ... Sets a rule the scene then breaks" (R12-4-VOICE_FOUR_DOCUMENT).
- R49-43-EXPLAINING: narration may explain causes "in the POV's reasoning and vocabulary". R48-25-AWE (clarity everywhere) is narrowed by R70-76 to what people do.
- R47-12-MYSTERY_STAYS_OPEN: a "What nobody knows" question "is never answered as fact on the page". Against it, R12-A was ruled 2026-09-12: "nothing is permanently mythic." R7-2-EPOCH_SCALE_SURVIVES: Epoch-scale things "generate problems, dread and awe. They never resolve a plot."
- R5-C1-NARRATION_NEVER_WINKS (with R70-10's threshold exception); R5-E-NARRATION_NEVER_ADJUDICATES; R5-C1-WRITE_FROM_LEAST_KNOWING ("write it from whoever knows least about what is coming").
- R49-09-CUTAWAYS: a turn may close on "a Front advancing, an NPC plotting". R48-48-EXPLAIN: physics explained "only when asked". R71 K9: from an NPC's POV the PC's "reasons and his Crystal stay dark".

**Settled.** Secrets reach the page through the four voices, two per engagement; documents may open a scene and be broken by it; the narrator foreshadows only at thresholds; the world's law is stated and its reasons kept; "what nobody knows" stays open while the Origin layer is explicable in principle.

**Open.**
1. Reveal cadence: how often a thread pays a secret (every session, every arc, at a Front's resolution).
2. Whether R49-09's cutaway to an NPC plotting is legal **inside a mystery**, where it hands the reader the answer the PC is hunting. Dramatic irony (reader ahead of the PC) against shared ignorance (reader beside him) is unruled for roleplay.
3. Whether an NPC investigator (a knowledgeable second) may solve a case in front of the PC, or only supply evidence under K9.
4. R47-12 against the R12-A ruling: which questions are "What nobody knows" (permanently open on the page) and which are merely not yet told.
5. Whether a withheld payoff (R70-17's break-off) creates a debt the State of Play tracks.

---

## 4. The Mystic register and the Lord of the Mysteries model

**Live law.**
- R12-2-MYSTIC_REGISTER_DEF: the Mystic register governs "Wellsprings, sites, rites, oaths, the Veil", stated "as law, never as physics: rules given in the imperative, prices given as prices, taboos given without justification". Its "It is Lord of the Mysteries" label was rewritten by R70-9 to the Eastern literary strands and the gothic; the row stays live, partly amended.
- R12-2-REGISTER_TEST: "if a person chose to do it, Technical. If it was already running before anyone noticed, Mystic." R48-10-MIXING lets the two mix by ear.
- R15-1-MYSTIC_REGISTER_NEVER_PHYSICS_STRUCK: a document "may be as scientific as it wants to be"; the Mystic register "survives as an option for documents that want to withhold".
- R53-28-VISUAL_REFERENCE: "The visual reference is Lord of the Mysteries and Victorian imperial-age fantasy." R70-5's notes keep Lord of the Mysteries a named model.
- R60-13 to R60-17, the Gate: magic knowledge is "gatekept by administration", outlaws learn from hedge-schools and stolen manuals, and "unlicensed high magic is punished like treason". This is WOTR's built-in secret-knowledge economy, its nearest match to Lord of the Mysteries' hidden world of Beyonders (that novel's secret practitioners).

**Settled.** Lord of the Mysteries is the look and a named model; the document voice is its device; the Mystic register's half-seen law is the horror register.

**Open.** Lord of the Mysteries' signature devices beyond the look and the threshold document have no WOTR law:
1. Secret identities, masks and aliases. Malphas is "filed by his title" (R67-8) and the Night Watch book keeps both leads ignorant of each other by Isaac's rule, but nothing general rules on an NPC who is two people.
2. Secret societies meeting under cover. The Mother has cells called cultures (R60-23) but no rule on how a cult appears on the page before it is named.
3. Knowledge as hazard: whether reading a forbidden text or naming a thing costs the reader. WOTR prices contact already (R61-108; the Night Watch page's artificer who spent his last months answering to the wrong name after an Anamnetic contact), but no rule makes knowledge itself dangerous.
4. Whether mental cost (a mind loosening under what it has learned or seen) belongs to horror, and through which existing mechanism, such as the Seven Unmoorings (R69-6) or the Shear Break (AL13, the fall when a vow fails). None is tied to fear today.

---

## 5. Horror: dread, pacing and the dead

**Live law that already produces dread.**
- Pressure as dread: R53-14-FOLK_KNOWLEDGE ("Pressure is felt as dread"); R71 MC15 (the unwoken take the Aura table: "dread from F to D, weight in the room from C, knees bending from A"); NATALIE's Pressure ladder (room first, then bodies).
- R9-3-SILHOUETTE_ENTRANCE: an unclassified Pressure is "staged backlit, shape before detail".
- Wells: R53-06-WELL_SPAWN and R58-06 (spawn breed at Wells only); R11-4-DESCENT_PROSE_LAW (the opening "inverts toward the body"; a misidentified encounter "is the best-shaped disaster available in this setting"); R11-4-SURVEY_PROTOCOL (pairs, "one member outside the radius, because the external observer is the only reliable instrument"); the Well delve as an arc (R70-18).
- The dead: R60-04-DEATH_IS_PERMANENT, except "liches, the undead and their kind"; R61-77 (a revenant is "a Crossing that stalls on its own", the Crossing being the nine-day passage in which a body's residues diffuse back to its Wellspring); R61-56 ("Full resurrection is forbidden on paper ... and secretly Malphas's own path"); R69-8 (the lich as "the one dead thing that stays itself").
- R71 AL14, AL17, AL18 (AL18's base option: "The horror is what the reader knows and she does not").
- R7-2-EPOCH_SCALE_SURVIVES; R48-34-WOUNDS ("nothing looked away from", in fights).
- R70-15 *jo-ha-kyū* tempo (slow opening, quickening, sudden close) for set pieces; R70-14 *kishōtenketsu* (set-up, development, twist, reconciliation, no conflict) for quiet scenes.
- R70-67's records of the strange; R53-15's folk beliefs (the Kharven "cold keeps the dead quiet"); R70-116's farce "then the thing in the dark".
- The Night Watch page: "It fears a working with no author."

**Settled.** Dread arrives through Pressure and the room; Well descents run on ambient ignorance; the dead have mechanisms and counters; comedy may cut against dread; gore is never looked away from in a fight.

**Open.** There is no horror pacing law at all:
1. Slow dread against shock: how long a horror beat builds, and whether a roleplay turn may end on the build without the thing (R70-17's cliffhanger is legal; whether it should be the horror default is not ruled).
2. Show or withhold the monster: R9-3's silhouette covers a practitioner's arrival only. Does a Well-spawn or a revenant get a full first-sight inventory (Table Rule 11) at once, or the half-seen first?
3. Clarity against dread: R48-25 and the R12-A ruling push toward explanation; R70-76 and R47-12 keep reasons back. Where does the explanation of a horror land: never, at its counter, or after the scene?
4. Which horror WOTR is (cosmic, gothic, folk, body, procedural): the Ferriby hinds and the impression-body set a register, but no rule names it.
5. Fear in the PC's body: R71 CW8 owes fear effects for the untrained in fights; whether horror may write fear into Isaac's PC at all, under R49-01 and K9, is unruled.
6. Slow dread across several short turns, against the 2,500-word set-piece floor.

---

## 6. The Night Watch and forensic law

**The institution.**
- R60-22-THE_NIGHT_WATCH: "a pre-Guild-Accord investigation unit on illegal magic and phenomena ... a crown office".
- R60-26-NIGHT_WATCH_SOCIETY (C-087): one body, a crown-chartered society with chapters, "walkers on fixed walks and a bulletin office", keeping the Night Register, "which takes up what the Lattice Classification Bureau (a separate office) closes". C-088 (ruled 2026-09-27): the Register is "the Night Watch Society's own desk, not the Guild Accord's Arbitration Division's".
- R61-62 and R67-1: the Farrant Papers are a Night Watch Searcher's field notes on the crown's warrant, a joint case with the Research and Archives Division. R67-2: Farrant is Class Ø (a Crystal that never woke) and "reads only by instrument or through a named reader". R67-4: "in Ketsuen a Searcher can ask and cannot compel." R61-65: the Papers' frame is in the Watch's office style, the entries in her voice. R61-66: she knows the Necrocursica only "as the Codex reports".
- Wiki canon (published, unindexed): samples go into Fixatio-anchored tins (Fixatio, the Wellspring that holds what it is given, is "why an evidence seal is admissible"); chapter wax makes a filing, the Register's brass an exhibit; the Register sweeps "below the floor" of the Bureau's coil; its only jurisdiction is Article XV, so a case runs from the ground to a contract to "a purse".

**The forensic science.**
- R60-11-TRACE_EVIDENCE_AND_JURISDICTION: a working's crime "is proved by trace examiners reading its traces as evidence".
- R61-7 and R69-3: residues on two clocks. Four inside the Crossing's nine days, read in order (the Corporeal Residue, the Aetheric Shell, the Noospheric Echo, the Volitional Trace); three after (the Harmonic Imprint, the Sympathetic Bond Trace, the Parunic Echo). "A Trace laid in ground that keeps records stays past the nine days."
- R61-73: after nine days a body holds "only passive Trait tissue". R61-97: the Parunic Echo is a practitioner's Essence Signature in residue, "legible from Stage IV".
- R61-70 and R61-108: Anamnesis (the Wellspring that reads the records places keep) "reads and wakes" them; "a Trace can be used once", every read "erasing what it takes". Reading the evidence spends it.
- R61-99, R61-91 and R71 AL15: registered maker's marks and provenance as trails. R61-110: an impression-body "shows a Trace without a Crystal".
- R71 MC17 and MC18: instruments catch a suppressed man "by the sag he leaves on a needle"; a faculty reads exact "unless warded". R59-06-MEDIA: photography for "evidence". R71 AL11 and AL12, as in section 0.

**The Night Watch book** (`book/night-watch-zombification/`) is the archive's long mystery: eighty chapters, Wystan Ashmore against Malphas, under Isaac's rule that "neither man learns of the other", with the case closing on the purse (Xu Deming) and never the hand.

**Open conflict.** C-125: the Night Watch book's rule that no file names Malphas against ML4 (R61-49), which has him sign the Necrocursica in his own name. The Papers take the strict reading. Unruled.

**Settled.** Who the Watch is, whose warrant it holds, where it cannot compel; the residue clocks; reading spends a Trace; marks and provenance are trails; the forensic scene plays as protocol, figures aloud.

**Open.**
1. Forensic scenes beyond residue: the post-mortem, the inquest, the interview, the search of a room. Only the residue reading (AL12) and the poison test (AL11) have a page form.
2. Whether "reading destroys the evidence" becomes a standing scene engine (one read, choose who reads), and whether the nine-day clock is shown as a clock in play.
3. The Night Watch as Isaac's own institution: no live thread carries a Watch PC. Is the Watch a patron, a rival, a quest-giver (R70-97), or a book-only lens?
4. Admissibility: what a Register exhibit proves in a crown court, a guild court, or a Kharven hearing.
5. C-125.

---

## 7. Courts, jurisdiction and the law

**Live law.**
- R60-19-LAYERED_RULE: crown, chartered company and guilds each fight "the others over jurisdiction, and which layer wins differs by place." R60-11: guild and crown courts fight over it.
- R71 WT12: "Proof decides" (a witness or a reading inside the residue clocks, and trace proof reaches blade killings too; "An unread killing sits on the Ledger as a risk"); "Courts fight over it" (every practitioner's killing opens a jurisdiction contest "as a Front"); "Declare it, or murder" (undeclared by next dawn is murder "in every culture that keeps witnesses, Kharven and Korvaeth first"). Not taken: "Standing buys terms."
- R71 CW11: every killing's legal aftermath, "a declaration, a blood-price or labour-debt, outlawry", opens a Front or a Ledger line.
- R53-11-JUSTICE: justice borrows each culture's real analogue ("fines and branding in Accord cities, labour-debt in Kharven, public shaming in Eresse"); R70-45 makes law and punishment an Inventory field; R60-21: succession follows each culture's law.
- R60-16 and R60-17: inspectors, trace examiners, the Inquisition; treason penalties for unlicensed high magic. C-085 (ruled 2026-09-27): the Holy Inquisition "holds legal standing where the crowns and churches that back it rule, and is outlawed where the Accord's circles have signed". Sancta Lux's lawful Inquisitors may "pronounce sentence in the field without an Arbiter" (wiki).
- R60-18: the Accord's Articles bind "where a circle has signed and not yet elsewhere". Kharven texture: with the Fusi Vā gone, "a word in the north is once again only as strong as the man who says it".
- R3-8-SIEGE_PARLEY_IS_SCENE; R70-111 long court speech; R70-67 court annals and memorials (set-form petitions to the throne).

**Settled.** The law is layered and contested by place; proof, witnesses and declarations decide; killings open Fronts; each culture keeps its own justice on its Inventory; court speech runs long in court cultures.

**Open.**
1. The shape of a hearing or trial on the page (the Night Watch book's ch59 to ch60 hearing is the only worked one, and it is a book's invention, not law).
2. Evidentiary weight by culture: confession, torture, oath, compensated witnesses (the Elven naming anchor already uses "compensated witnesses"), the Zettari Stone Witness.
3. Corruption of process: bribed clerks, lost papers, sealed files. The Tallow Street Stair Front already turns on "the papers are shown, withheld, or already missing".
4. Whether the PC can be tried, and how a verdict against him is adjudicated fairly (Table Rule 5 covers contested action, not a court).

---

## 8. Faction intrigue, Fronts and the roster

**Live law and machinery.**
- Table Rule 3: NPCs "lie, withhold, refuse, bargain, misjudge him." Table Rule 4: "Between turns and sessions, Fronts advance."
- **Fronts** (the table's threat clocks) are kept in `table/fronts.yaml` and `table/FRONTS.md` as segmented clocks, mostly five segments, each with a **Want**, a **Last move**, a **Next move** and numbered steps ending in "Resolves". The MCP's `fronts`, `advance_front` and `set_front_clock` run them; the session-start protocol advances at least one per session. R58-07 shows a Front recast by ruling (Wren's grief Front, "ticks driven by who blames whom").
- R60-20-HOW_POWERS_FIGHT: "proxy and company wars, open war, economic war and intrigue; WOTR needs distinct conflicting factions with different interests written out."
- R60-05 to R60-09: company then crown, the scramble, who pays, the Accord forming now. R60-23 to R60-25: The Mother, a cult whose cells are "cultures"; Malphas wants "to obtain the unattainable", "to break the Gate", "profit and power".
- The **roster** (`table/npcs.yaml`, via `npc_set`): want, refusal line, what each knows, `lied_about`, voice. R48-26-INVENTION: NPCs invented mid-scene, logged.
- NATALIE's Rumor Mill: world news in an NPC's mouth, "some wrong, one a hook". The Scene Menu's hooks carry reward and penalty (R70-97). R70-112, CW11 and WT12 open Fronts as consequences.

**Intrigue Fronts already on the table.** The Accord circle, Tabitha Hallenfeld's grain question, Bram Greymane's omission, Thela Ess-Vaelen's validated name, Velthaeir's two registers, The Finding of Cause, and The Tallow Street Stair (a death ruled "a fall in drink" and a stolen daybook). The table already runs paper intrigue and inquest mysteries; the Mu-jin thread's inquiry agent, Rovhen Talvasciel, is the nearest thing to a detective in play.

**Settled.** Factions move by Fronts every session; each faction needs written interests; NPCs carry wants, refusals, knowledge and a lie; a public humiliation or an undeclared killing opens a Front; rumours may be wrong.

**Open.**
1. **Front visibility.** FRONTS.md is readable by Isaac and its "Next move" lines state what is coming. Should mystery and intrigue Fronts be hidden from the player (a sealed Next move), shown as clocks without contents, or stay open as now? R49-09 cutaways raise the same question per turn.
2. Information as currency: spies, informants, blackmail, intercepted letters (the second Gillus letter, R61-14, was "intercepted, held in the case file"), the penny press and the Watch's inserts as public intelligence ("whoever reads the inserts knows where to find him").
3. Faction sheets: R60-20 demands interests "written out" but no format exists beyond a Front's one-line Want.
4. Conspiracy across sessions: how many Fronts one plot may run, and whether a hidden faction may advance with no visible tick.
5. NPC knowledge tracking: `knows` and `lied_about` hold one or a few items. Whether every NPC in an intrigue keeps a running "what they know about the PC" list is unruled.
6. Whether Natalie may stage a betrayal by an NPC the PC trusts, given R48-30's foreshadowing floor and R70-114 (each live thread carries "at least one standing warm bond").

---

## 9. The gaps in brief

The open lists above reduce to nine question areas: Table Rule 8 after R49-11 (coordinate with the table questionnaire, since Rule 8 is a table rule and unindexed); a mystery's clue economy and fail state; reveal cadence and dramatic irony; the Lord of the Mysteries devices not yet ruled; horror pacing; forensics beyond residue; the Night Watch's place at the table and C-125; hearings and evidentiary weight; Front visibility and the information economy. None contradicts a live row, so each can be asked cleanly and logged as a new dated law beside R70 and R71.
