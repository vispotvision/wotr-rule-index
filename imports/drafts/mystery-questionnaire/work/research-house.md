# House research: how mystery, horror and intrigue actually read in WOTR

Research for the mystery, horror and intrigue questionnaire, 2026-10-04. Read only; nothing in the archive was changed. Quotes are short and carry their file.

## What was read

- **Isaac's own text, archived verbatim:** `scenes/the_nights_watch.md` ("Isaac's scene, archived as delivered", 8,032 words, three movements); `scenes/the_war_in_the_north_i_the_kharven_seat.md`, `_iv_the_blank_seal.md`, `_v_the_shieldwarden.md`; `scenes/the_true_king_of_the_north_part_15.md`, `_16.md`, `_18.md` (his 22-part manuscript).
- **Night Watch material:** `wiki/Factions, Bloodlines & Institutions/The Night Watch.md`; `wiki/The Alftian Codex/The Farrant Papers.md` (rebuilt 2026-09-28 from Isaac's "Corrant Papers" under his decisions PA1 to PA6 in `imports/drafts/alchemy-conversion/decisions.md`); `book/night-watch-zombification/` (bible, `GATES.md`, `AUDIT_ch10.md`, `state.json` hooks, ch07); `scenes/wystans_briefing_aetherion_arena.md`.
- **Inquiry scenes built from Isaac's beats:** `scenes/rovhen_the_letter.md`, `rovhen_the_sort.md`; draft `~/wotr-drafts/rovhen_the_cuff.md`.
- **Lambert and the Inquisition:** `scenes/the_holy_inquisition_part_1_the_kindling.md`, `_part_1b_the_empty_chair.md`, `scenes/sodoku_true_religion_alabaster.md`.
- **Horror:** `wiki/The Bestiary/Well-spawn.md` (the Lamp-drinker, the Mourning Pike), `wiki/The Alftian Codex/The Necrocursica.md`, `wiki/Factions, Bloodlines & Institutions/The Mother.md`, `scenes/sesk_the_report.md`, `scenes/kaalabad_the_petition.md`, `scenes/malphas_on_the_line_the_train_east.md`, draft `~/wotr-drafts/the-waiting-heisuke.md`.
- **The machinery:** `table/FRONTS.md`, `table/LEDGER.md` (its "who knows what" section), `table/NPCS.md`, the Kharven State of Play page, `book/kharven-year/bible.md`, `scenes/CONTINUITY.md`, and every live rule in `out/rules.resolved.json` that touches lies, ignorance, surprise or secrets.

## Headlines

1. **The house mode is dramatic irony, not the whodunit.** Dramatic irony means the reader knows what a character does not. Isaac's own long work shows the villain's room in full and then lets the investigator find tells. *The Night's Watch* cuts from Wystan's desk to Malphas's coldhouse; *The True King of the North* cuts from Lambert's suspicion to Seiji's desk to the tells in Kharven. The reader is told; the investigator is not.
2. **Paperwork is the clue bed.** Inserts, classifications, tally books, freight books, station records, rolls, seals and wax. Secrets surface because somebody kept an honest record and somebody else read it. Magic supplies the instrument, the record supplies the case.
3. **The archive's best horror is quiet and kind.** No smell, ravens that will not come down, a hind that dies content, a weight that comes on before its cause. Gore is reserved for combat; dread is built from absence.
4. **Horror lives mostly in documents, aftermath and witness.** The Bestiary, the Necrocursica and Sesk's ledger of torture are the strongest horror in the house. The PC's one horror scene, *The Shallow-Seen Unburied*, makes Sodoku watch a past atrocity backward. No archived scene puts him in the dark with an unknown thing and plays it as fear.
5. **Intrigue runs on arithmetic.** The signature move in Isaac's councils is a dated discrepancy: a brother who left fourteen days before the letter, grain bought in the first week for an advance that came in the fourth, a refugee count that fell three hundred.
6. **Lies are tracked better than clues.** The Ledger has a "who knows what" section and the roster has "has lied about" lines. Nothing tracks the clues Isaac himself planted (the oil lamp, the burn-salve, the one-word letter) outside `CONTINUITY.md`.
7. **The rule on not-knowing has drifted.** The per-scene ignorance quota and misreading budget (R6-3, R6-4) are superseded and optional under R49-11, while NATALIE.md table rule 8 still asks for one per turn and one uncorrected lie per session.

## Already settled: do not re-ask

From the **Style Law, R70** (`rules/doc-style-law-2026-10-03.yaml`, `imports/drafts/style-questionnaire/decisions.md`):

- Openings may be a register entry, readout or document that the scene then tests (R70-16). Closings may stop mid-crisis on a reveal or threat, on a notice, or a breath before the payoff (R70-17).
- In-world documents: lists and loose notebooks, records of the strange closed on the recorder's comment, court annals, Guild reference entries (R70-67).
- The narrator foreshadows only in a chapter's opening and closing lines; the body stays POV-locked (R70-10).
- Comedy and dread may sit hard against each other, each played straight (R70-116).
- Court cultures argue in long formal speech; Kharven and soldier speech stays short (R70-111). The public face-slap opens a Front or a Ledger debt (R70-112).
- The POV's culture decides what he makes of a room, misreadings included (R70-44). Narration states only the figures the POV holds (R70-83). Rules are planted before the fight (R70-71). The world's magic is stated law with taboos unexplained (R70-76). Every live thread keeps a warm bond (R70-114).
- Older live law kept by the R70 pass: folk beliefs stand uncorrected (R53-15); a reasoning POV may set out numbered steps (R70-38).

From the **Combat Law, R71** (`imports/drafts/combat-questionnaire/decisions.md`; RULINGS.md "combat-law-2026-10-04"):

- K7, a way out always planted; CW14, the tell shown twice, then read; K6, the deciding fact sits in the read.
- AL12, a forensic reading is written as protocol in action; AL18, the impression-body's voice carries a seam the reader catches.
- WT12, the law turns on proof, courts fight over proof, and the alternative is declare it or murder.
- FT6, a monster fight is the hunt as procedure, in phases at the tie; FT7, a beast is appraised with the gap between guess and truth shown; WT5, the stale pouch fails on a planted tell.

Other live law the questionnaire should treat as standing: R48-30 (big surprises only after foreshadowing a player could have caught), R48-42 (frequent lies), R49-36 (every lie leaves a catchable tell), R47-12 (a "nobody knows" question is never answered as fact), R60-20 (the powers fight by proxy, economy and intrigue), R7-2 (Epoch-scale things make dread and never resolve a plot), R5-C1 (write from whoever knows least), R12-4 (a confidently wrong explanation is the main vehicle), R11-4 (in a descent the ignorance is ambient and an encounter may be misidentified), R49-09 (a turn may close on a short marked cutaway).

## 1. The house mode: suspicion, confirmation to the reader, tell to the investigator

Isaac's own manuscripts run one shape three times.

**The Kharven chain.** In Part 15 Lambert names Valdís Ashmore as the problem by arithmetic: she is the only alchemist, and "sole means unchecked" (`the_true_king_of_the_north_part_15.md`). In Part 16 the reader gets Seiji's desk in full: Valdís was "the face the wards recognized" on the night Muken died, a nine-year-old girl is an unwitting recorder, and a one-word letter goes north. In Part 18 the tells reach Sodoku: an oil lamp in a city that burns tallow, put out by a quick hand, and on a kitchen shelf a properly made burn-salve "In a house with tallow in the lamps." He "could make nothing of it at all."

**The Night Watch chain.** Wystan writes *edges* in his margin; the next movement opens in Malphas's cell and has the villain say the same word ("the work has an edge"); the third movement delivers the hind's memory to Wystan's bare fingers (`the_nights_watch.md`).

**The Wren chain.** Wren writes in a forged hand under a blank seal, says he left "the rat" for Bram (`_iv_the_blank_seal.md`), and the next part shows Bram finding the farrier with a reader who already knows he was placed (`_v_the_shieldwarden.md`).

What this means: the mystery Isaac writes is about *whether and how* the right person catches it, and what it costs them, with the reader one step ahead. The fair-clue puzzle, where the reader solves alongside the detective, appears only in the inquiry threads (Rovhen, Farrant), which hold the villain's room back.

The night-watch book makes the irony a law: "neither man learns of the other," the narration "never winks at the reader who knows both," and its anti-exemplar bans the hunter-and-hunted wink (`book/night-watch-zombification/bible.md`). Its standing irony is a belief Wystan never corrects: that the formulator "never goes near them," when the reader watched Malphas press two fingers into the ninth hind's flank.

## 2. How clues are planted

**The anomaly read through the economy.** The best clues are material and priced: oil where people burn tallow; a nine-hour salve in a poor kitchen; Tally's grey-green mass measured with a rule; Joan Aldery's lamp, "on the third step from the bottom. Standing up," its glass whole (`rovhen_the_letter.md`). This is R53's "money before magic" turned into detection. A reader who knows the Standing Inventory can catch it.

**The edge.** "A bleed has no edge... A boundary means somebody chose one, and a choice means a hand" (`the_nights_watch.md`). The Night Watch page promotes it to the Society's rule and the Farrant Papers reuse it at Genesio. It is the archive's one stated principle of detection.

**The date that does not fit.** Hild asks "How many days between your letter leaving and your brother leaving"; Lambert counts it out and the room learns Charles "left fourteen days before I wrote" (`the_war_in_the_north_i_the_kharven_seat.md`). The same shape drives Tabitha's Front (the grain bought in the first week), Neros's Weight that steps "late," after each Genesio cluster, and Deming's warning that a Logistics return publishes in eleven weeks.

**Seals and hands.** Wax is the master clue object: chapter wax broken in four pieces and kept ("I will want them later"), the Register's brass struck on a fresh tin, Draycott's ring and three spokes on a widow's letter, Wren's blank disc, Rovhen's green wax pressed with a bare thumb. Which seal sits on a thing decides whose case it is. Forged and borrowed hands recur (Wren, Seiji writing in his dead father's hand).

**Shown twice.** The archive likes the second sighting: Tally "checked the far side twice"; Joan's cuff carries three identical cuts, and Rovhen's reasoning is that a nail "does not come back twice more at the same angle" (`~/wotr-drafts/rovhen_the_cuff.md`). This matches CW14.

**The bare fact with no second sentence.** Readers in the house deliver a fact and refuse to interpret it. Yoko: alabaster dust on a satchel's leather, "I am not telling you what it means." Yūgiri: "Two... I do not have a second sentence." R6-2 (the read delivers a bare fact) is the law under it, and Isaac writes it himself.

**The planted absence.** The Empty Chair's lesson is "We're not asking who's here. We're asking who isn't" (`_part_1b_the_empty_chair.md`). The Tsohanto Reach Front is a silence nobody counted for eleven years. The missing daybook is the motive clue: "The lamp is how. The book is why."

## 3. How secrets surface

**Honest records, read by the wrong person.** Josse Hillborn's tally book "had been kept honestly and completely and had never thought to hide"; the finding "had not taken cleverness" (`_v_the_shieldwarden.md`). Farrant is found through "a station record in Castlefall that anyone may read." The Register "builds its file off whatever is written down," which is why Malphas names his project on purpose: "I would prefer the file be built off a word I chose." Secrets leak through bookkeeping, and the cleverest villain in the archive games the bookkeeping.

**Contact at a price.** Anamnetic contact (bare fingers on live residue, which gives the reader what the residue holds) is the archive's revelation with a cost: Wystan carries "forty-one minutes belonging to other people," now forty-two, and is sick at the sink. Farrant's chain of reasoning is labelled "My reasoning" and paid for with what she would rather not record ("Not wanted").

**Letters.** A secret comes as paper: Draycott's letter (Exhibit E), the Exhibit C letter released unopened, the one-word letter for Valdís. The word itself is never printed. That is the archive's single secret withheld from the reader as well as the cast.

**In pieces, never at once.** The night-watch book plants 32 hooks with plant and due chapters (H01 the far side of the marker, H07 the warm hands, H18 the project name as the file) and pays them across 80 chapters. Its audit at ch10 already warns of 23 open hooks and seven dormant ones (`AUDIT_ch10.md`).

**Contradicting the record.** The blank seal turns a man the ridge calls traitor into a deep-cover patriot. Isaac's big reversals overturn what the world's paperwork says rather than what a character said.

## 4. Horror and how dread is paced

**Absence first.** "There was no smell" is a one-line paragraph in Vesk's coldhouse; the main under Cutler Row is off and "the silence it left had a shape"; Sesk's descent opens on "Nothing," and the corridors "smelled of nothing at all" (`sesk_the_report.md`). The Lamp-drinker shows only "as a place the light stops" (`Well-spawn.md`).

**Dread before the cause, and no cause given.** On the Castlefall platform Farrant goes to one knee: "Dread came first, with nothing in front of me to fear." A carter sits down, a child cries, then the weight lifts, and she writes "I enter the slip and nothing about its reason" (`The Farrant Papers.md`). This is R70-69's room-first Pressure (the felt weight of a stronger practitioner) used as horror rather than spectacle.

**The kind design.** The worst thing in the Night's Watch is that the hind did not suffer: "It is a design... he built it so that stopping felt good." The horror is intelligence behind mercy.

**Witness horror.** In `06_sodoku_the_shallow_seen_unburied.md` Sodoku stands outside a boundary and can see "Backward. Only backward": a room with the drain grating lifted, a chair with the arms cut short, Freya in it, and a man he had eaten with who speaks "pleasantly for eleven minutes before he touched anything." The horror is that he must watch and cannot act, which suits a PC who is otherwise the strongest man in the room.

**Ledger horror.** Sesk reports torture "in the order I keep the ledger," molars and strips of thigh counted like stock. Lambert counts chairs. Deming puts "a number in the room." Flat procedure under atrocity is the house's grimdark register.

**The folk rule with a false reason.** Thaloré outflow villages hold no funeral at the water and "the reason given is always something else"; the fishermen's tale ends on "what they found under the jetty when they dragged it." Lamp-drinker delvers whistle on shift: "The noise is not high spirits." Horror is carried by custom and left uncorrected, which is R53-15 working as dread.

**The confession in the document.** The Necrocursica's case "The Averted Regard" is Malphas's own: a boy who left a bundle of flax in the retting pond past the hour to see what the rot did next, a request to read the chapter back to him, and a later margin: "Nobody read it back." It is the strongest horror passage in the house and it is a footnote.

**The unpursued wrongness.** The Heisuke draft carries a dead man two days cold and "the lamp lit tonight," then: "He did not go looking for the hand" (`the-waiting-heisuke.md`). Sesk decides each night "that I do not want to know." The Kindling repeats "Corvinus did not know what that meant." Characters who refuse to look are a recurring dread device.

**Pacing.** Dread scenes in the archive are long and slow and end on a turn of the knife, not a jump: a pen taken up, a hook fetched, a name written at the head of a docket. That is jo-ha-kyū (slow, breaking, swift, R70-15) with the swift beat kept small. No archived scene stages the scare itself.

## 5. Court and faction intrigue

**Councils.** Isaac's kitchen council at the Seat runs on reports, counts and one hard question from the youngest at the table; the room changes when Lambert's thumb stops counting. The Empty Chair has Edward read "the second sentence," catch a legal word ("bequest") in a soldier's mouth, and let a six-year-old answer. Hild keeps a taxonomy of the lies told to her: Osric's kind ones, Pietro's cruel ones, and Edward's truth "built to make me act, which is a third thing" (`sodoku_true_religion_alabaster.md`).

**Methods tied to the faction's metaphysics.** Seiji recruits "circumstances," not agents, because a circumstance "cannot be interrogated," and the Tenrai affinity is convergence. The Mother keeps "the hand and the purse apart" because Article XV (the Accord article that sends liability to whoever paid) can charge only a purse. Sodoku answers Alabaster with sworn testimony because "Their Wellspring is testimony." Intrigue is strongest when the scheme is shaped by the faction's law.

**Fronts as schemes.** Fronts (each faction's clock of moves, `table/FRONTS.md`) carry most of the intrigue: the Accord circle's first test arrives "dressed as housekeeping," Lambert re-entering the 406 refugees under the circle's seal; Seiji's four riders, two of four meant to be believed (L040, L041); the Finding of Cause with a blank beside "Party answerable"; the Tallow Street Stair. Every step is a document signed, refused or read.

**Gaps.** The Night Register case and The Mother have no Front on the table; the book's four proposed Fronts wait on `add_front`. I found no archived scene of the Accord signing itself; it lives in the State of Play and three Fronts.

## 6. Lies that stay uncorrected

**In Isaac's text.** Josse's "I have not sold you, my lord" stands, and the archivist's note calls it "the best misreading in the file." Wren's six hundred spears and the ridge's word "traitor" stand for sixteen months. Seiji's riders mean two lies to be believed.

**In practice at the table.** Author notes carry the rule: "The lie (Rule 8): 'Nail. At the counting-house door.' Uncorrected" (`rovhen_the_letter.md`); "Lies on the table: Malphas's story is that a core took the miller's girl" (`mu_jin_the_card.md`); the Kindling's "Misreading Budget: Corvinus frames the Kindling's cost as something recoverable... The narration does not correct him." About 32 scene files mention a misreading, an ignorance quota or an uncorrected lie.

**The tracking.** `table/NPCS.md` has a "has lied about" line per NPC (Harrowgate: "The ward was proofed at the quarterly"; Joan: the nail). `table/LEDGER.md` has a "who knows what" section with due conditions (L015 Renard's dead man's word, L041 Lorn's three reports, L053 Sodoku crediting the turning to Sonzai "on no evidence the page gives"). The night-watch bible lists five beliefs of Wystan's that are wrong and when each is struck. The Kharven State of Play's matching line reads "What he believes that is wrong. Open. Fill at next session."

**The drift.** R6-3 and R6-4 are superseded; R49-11 made the quotas optional with "no per-scene minimum." NATALIE.md rule 8 still says one unexplained thing per turn and one uncorrected NPC lie per session. Both are live text in the house and they ask different things.

## 7. The Lord of the Mysteries register, as the archive already has it

*Lord of the Mysteries* (a Chinese web novel by Cuttlefish That Loves Diving: a Victorian, steam-and-gaslight occult mystery whose hero works with a church-run night police called the Nighthawks) is the named look of the Draw Age (R53-28). What the archive already shares with that register:

- **A night police in a bureaucracy.** The Night Watch Society, its Register worked "at night while the district main is off," a Warden with a brass token, inserts printed on rag. The investigators are low-status clerks inside a larger state, not heroes.
- **Knowledge with a cost.** Anamnetic contact leaves other people's minutes in the reader; the artificer who took one "spent his last eleven months correcting people who called him by the wrong name." The Necrocursica's taboo is "Never give it the name."
- **Secret cults with method.** The Mother's cultures, inoculation, chosen names, and a founder whose doctrine is "the rot valued for its yield."
- **Newsprint and filings as the world's nervous system.** Bulletins, classification returns, "the standard form, the one they return for weather."

What the register has that the archive does not yet use: the investigator's own double life and secret identity; a gathering of masked members who do not know each other's faces; the danger of speaking a hidden power's name aloud as a live mechanic rather than a footnote; madness that builds in the hero by stages; and cosmic-scale dread on the page (R7-2 allows Titans and Archons to make dread; no scene does it yet).

## 8. What works

- **The edge as a principle a reader can use.** It is stated, applied, inverted by the villain (make the dose walk) and struck in public in the book's plan. Fair, findable, and the counter is planted.
- **Clues priced in the economy.** Oil, salve, salt bars as money that "leaves no bill," grain dates, wastage columns. They need the Standing Inventory and they reward reading it.
- **The bare fact.** Readers who will not supply the second sentence keep the reader working.
- **Two-layer documents.** Farrant's chancery frame around field notes, Halveth's margins ("Stop separating them"), "My reasoning" against "Not wanted." The form shows the investigator's limits as part of the evidence.
- **Folk custom as horror.** The pike rule, the delvers' whistling, "Nobody's down there." Each comes with a fair counter in the same entry.
- **Villains with arguments.** Foss explains why the Bureau is "being correct"; Malphas recites Tally's walk "the way a man reads a bill of lading"; Deming wants it noted he warned them. Nobody in the cell is stupid, which meets R48-36.

## 9. What repeats or goes stale

- **Eleven.** "Eleven" appears about 1,700 times across the scene archive (about one every 600 words); the Night's Watch alone has 22 (eleven years, hinds, days, weeks, months, miles). It is Isaac's own habit too, so it is a question, not a fault.
- **Lamps and wax as the clue object.** Aldery's lamp, the oil lamp, the Register's third lamp, the Lamp-drinker; wax in five different hands. Strong objects, close to a signature, at risk of becoming the only ones.
- **The ignorance formula.** "Could make nothing of it" or "did not know what that meant" in at least eleven scene files, often closing the beat.
- **The regulation bracelet that pulls** toward a suppressed practitioner is the only warning in both the Night's Watch and the Farrant Papers.
- **Ladder-heavy intrigue prose.** The Empty Chair and Seiji's desk explain schemes in long "the X was the Y" chains (R6-1 bans the shape; both predate R70, and Part 16 is Isaac's fixed text).
- **Hand and purse.** The Article XV split carries the Night Watch, the Mother page, the Papers and the book's spine. It is good law and it is used for every case.

## 10. What is missing

1. **A clue ledger across threads.** The night-watch book has one (32 hooks). The Kharven thread does not: the oil lamp, the burn-salve, the one-word letter, the two Hillborns and Lambert's Valdís suspicion appear in no Front, Ledger line or book bible (`book/kharven-year/bible.md` has none of them).
2. **A truth file.** What is actually true behind each open mystery, kept where Natalie can read it and players cannot. Right now truth is scattered across villain-POV scenes, cards and `CONTINUITY.md`.
3. **A fair-play contract for PC-facing mysteries.** R48-30 asks for foreshadowing a player could have caught; CW14 asks for a tell shown twice. Nothing says how many clues a conclusion needs. Tabletop designers use the Three Clue Rule (for every conclusion the players must reach, plant at least three clues, because players miss some) and nothing like it is ruled here.
4. **How much of the villain's room Isaac sees in play.** Written work shows it in full; R49-09 allows only a short marked cutaway at a turn's end in roleplay. The rule for a table where Isaac's PC is not the investigator is unwritten.
5. **Fear on the page in play.** Apart from the vision of the Shallow-Seen Unburied, nothing puts the PC in the dark with the thing: no descent, no Well-spawn encounter, no walking dead (the book's walking chapters, ch14 onward, are unwritten). The Titan Droval on the polar shelf are written as a test of power, not of nerve, and the Tolling draft (`~/wotr-drafts/the-tolling.md`) is framed as a hunt by contract.
6. **Fronts for the Night Register and The Mother.** Proposed in the book bible, never added.
7. **The dead as a question.** Kharven believes "the cold keeps the dead quiet"; the Necrocursica says a revenant walks on Salt, Mercury and Sulphur and to "Do not write it down"; Project Zombification will make carcasses lean toward the quiet districts. No ruling says whether a folk belief about the dead may turn out true, false or half-true on the page.
8. **Reveal cadence.** Nothing rules how often a thread may pay a big secret, how long a lie may stand, or whether a secret may stay unpaid for good (Isaac's one-word letter is the only true withheld secret).
9. **The interrogation scene.** The archive has reports, councils and contact readings, but no question-and-answer interrogation written as a duel of tells (Josse's is summarised in two sentences).
10. **Comic voices in the dark.** R70-116 permits farce then dread; the archive has almost no example in mystery or horror (Sesk's dry asides come closest).

## 11. Targets for the questionnaire

Questions the archive raises and the two laws do not settle:

- **Mode:** dramatic irony (reader sees the villain's room), the fair puzzle (reader solves with the investigator), or each by thread? How much villain-room may a roleplay turn show Isaac when his PC is not the one investigating?
- **Fair play:** how many clues per conclusion; must every clue be catchable by a player who knows the Standing Inventory; are red herrings (false clues planted on purpose) legal, and must they be labelled in author notes?
- **Clue objects:** keep lamps, wax and ledgers as the house signature, or rotate them by culture?
- **Secrets:** a truth file, a clue ledger, or both; who may read them; does every Front carry a secret column?
- **Reveal cadence:** how long may a lie stand; may a secret never be paid; how often may a thread reverse the record (the blank-seal kind of twist)?
- **Rule 8:** restore a per-turn quota, keep R49-11's optional reading, or set a per-session floor? One ruling should make NATALIE.md and the index agree.
- **Horror:** onscreen or offscreen; jump beat allowed or never; how gore in horror differs from combat gore; whether the PC may be frightened in the body (CW8 owes fear for the untrained only); knowledge with a mental cost as a mechanic.
- **The dead:** whether Kharven's beliefs about the dead can be proved or broken on the page, and how walking dead read under the Necrocursica's law.
- **The Lord of the Mysteries register:** which of its absent pieces (a double life, masked gatherings, the spoken name as danger, staged madness, cosmic dread) WOTR should take, and which it should leave.
- **Intrigue:** how intrigue scenes are told (council, letter, ledger, cutaway); whether every scheme must be shaped by its faction's metaphysics; how an interrogation reads; where comedy may enter a dark scene.
- **Investigators as instruments:** what a Night Watch search can and cannot do on the page, what it costs, and the counters (the Watch page's "Where the Seams Are" is the model).
