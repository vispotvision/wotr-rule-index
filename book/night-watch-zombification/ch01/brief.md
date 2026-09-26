# Brief — Chapter 1: The Docket Head

*The Night Watch — Zombification Arc. Thread: Wystan Ashmore. Culture: Accord. Assembled 2026-09-24 from outline.json, bible.md, state.json and build/book_tools.py (read-only). Docket: 0 pending/proposed for this loadout, so no ESCALATE.*

## The beat

### Outline row (verbatim)

```json
{
 "number": 1,
 "title": "The Docket Head",
 "beat": "Picking up the second she finishes writing her name at the head of the docket, Wystan strikes the fresh tin's wax with his brass, enters the Ferriby wedge as Register exhibit one, and folds the four chapter-wax pieces into a paper he dates on the outside. He writes to Tally for a second dataset and the name of whoever set the marker, and sends Yinzhi home. At the sixth division the main comes back and the hum fills the building; he carries the tin to the day desk, finds Brack's classification entered and closed, and enters his own memorandum beneath it, one word in the margin: edges. The Ferriby filing is now a Register file with an exhibit and a named assay, and nobody on the day desk reads past the classification.",
 "scene_type": "standard",
 "pov": "Wystan Ashmore",
 "cast": [
  "Wystan Ashmore",
  "Qiu Yinzhi"
 ],
 "place": "Cutler Row, the Night Register (the scullery back room) and the day desk at the sixth division",
 "front_id": null,
 "proposed_front": "the-night-register-file",
 "plants": [
  "H01-far-side-of-the-marker",
  "H02-quarter-inch-sealed",
  "H03-chapter-wax",
  "H04-tallys-second-dataset",
  "H05-night-register-a-person",
  "H06-edge-held-cup",
  "H23-edges-in-the-margin",
  "H24-brack-signs-bleed"
 ],
 "pays": [],
 "time_elapsed": "The same night, from the fourth division to the sixth",
 "target_words": 3500
}
```

### Hooks this chapter plants (from state.json; keywords must land on the page)

- **H01-far-side-of-the-marker** (due ch7, status planned). Tally found clean ground on the far side of the parish marker, twenty-two paces past the last carcass, and checked it twice; Wystan writes 'ask Tally who set the marker'. Paid when the lick-keeper's round is found to end at the marker: the carrier turned home there. Keywords: marker, far side, lick, turned.
- **H02-quarter-inch-sealed** (due ch58, status planned). A quarter inch of new growth inside a Fixatio-anchored tin with the seal unbroken; the day book reads 'crown +¼ in sealed, 11d'. Paid at the hearing: Fixatio held what it was given, and what it was given was a running working. Keywords: quarter inch, Fixatio, running, sealed.
- **H03-chapter-wax** (due ch58, status planned). 'They are chapter wax and I will want them later.' Four pieces of the broken seal, dated and kept. Paid at the hearing: the pieces fit the join and prove custody. Keywords: chapter wax, four pieces, join, custody.
- **H04-tallys-second-dataset** (due ch41, status planned). Wystan asks Tally to keep walking and measuring: 'I want a second dataset from the same observer.' Paid when the notebook is taken from Tally's walking body, complete to the night he died. Keywords: second dataset, same observer, notebook, Tally.
- **H05-night-register-a-person** (due ch68, status planned). The bulletin clerk told Tally the Night Register was a person. The cell knows its hunter only as the Night Register. Paid when the Register is folded and Malphas closes the line. Keywords: Night Register, person, folded, somewhere else.
- **H06-edge-held-cup** (due ch78, status planned). Wystan holds everything by the very edge, two-fingered, even a cup. Paid in VI: Salter sees a man holding a cup that way across the quad, notes it, and nothing follows. Keywords: cup, rim, two fingers, window.
- **H23-edges-in-the-margin** (due ch16, status planned). Wystan's margin note: edges. Paid when the walkers erase them and he strikes the word in public. Keywords: edges, margin, struck, bleed.
- **H24-brack-signs-bleed** (due ch67, status planned). Brack's classification: Wellspring bleed, Verdantia, no operator indicated, correct off a true measurement. Paid when the Accord's official classification stays bleed and Brack signs it again. Keywords: Brack, bleed, no operator, signed.

Hooks this chapter pays: none.

### The Front tick: the-night-register-file (proposed; bible.md, Proposed Fronts)

No Front exists in table/fronts.yaml for this thread; `front_id` is null and this proposed Front stands in (nothing is written to the table until Isaac says add_front).

- **Want:** an attribution he can derive, and the purse that Article XV requires.
- **Segments (6):**
  1. **Exhibit one.** The tin entered, the edges memorandum, the round and its intermediary, the theory entered as the Register's position. Ch1, 3, 5, 7, 12.
  2. **The edges fail; the gradient found.** Ch14, 15, 16, 18, 20, 21, 23, 25 (the wrong inference: they are sent to him).
  3. **The sink.** The second dataset complete; Low Ground understood. Ch28, 35, 37, 41, 44.
  4. **The purse built.** Article XV opened, the ledger, the knife, the word. Ch49, 51, 53, 54, 57.
  5. **The hearing and after.** Custody proved, the Stage exposed, the hand reserved. Ch58, 64, 65, 69.
  6. **The file becomes a lesson.** Called Late at Greyshaft Nine, the Register folded, the Society, the tin at Aetherion. Ch71, 72, 74, 76, 77, 79.
- **This chapter's tick:** the first push on segment 1, *Exhibit one* (first of five chapters; ch12 fills it). The world changes and the POV sees it: the Ferriby filing stops being a closed Society insert and becomes a Register file, with the tin struck under Wystan's brass as exhibit one, Yinzhi's full name at the docket head as the named assay, the chapter wax dated and kept for custody, and the *edges* memorandum entered under Brack's closed classification. Mention is not advancement: the tick is the entry in ink at the day desk, and its visible consequence is that nobody there reads past the classification.

## Protocol

`desktop/NATALIE.md` governs the drafting (THE TABLE RULES, PROSE STANDARDS), with these chapter adaptations:

- **No turn-taking.** Table Rule 1's answer-the-PC half is off: this is a chapter, not a turn, and nothing waits on a player's decision. Its ending rule stays: end on a physical action, an NPC line, or a thing the POV can now see; never on a question aimed out of the fiction.
- **There is no PC in this book.** The standing book rule from bible.md applies instead: **neither Wystan nor Malphas ever learns of the other.** Malphas knows his hunter only as "the Night Register" (at most "a desk on Cutler Row with a brass token"); Wystan knows his quarry only as the formulator, "the man who never goes near them." Nothing noticed across that line is ever paid as recognition, and the narration never winks at the reader who knows both. (In this chapter: Malphas does not appear and is not named or implied by the narration.)
- **POV lock (R39-7, bible):** Wystan only thinks in italics; Yinzhi gets no private italic thought, even though the source scene gave NPCs italics.
- **Length:** target 3,500 words at the **set-piece band** (2,500 minimum, full scene standards; verify with `--band set-piece`), though the scene type is standard.
- **One deliberate lie by an NPC and one misreading by the POV character**, both declared in the author notes. (Candidates, the writer's to choose: the misreading is the book's "edges" error, entered as the Register's position, true of the first dose and false of every one after; the lie might be Yinzhi's about her own fitness or her five days, or a day-desk clerk's about the file.)
- **Numbers** reach the page only in a mouth, an instrument, a document or a private count (R14-4, R12-5); the writer invents none. Yinzhi's full name on the docket is never rendered.
- **Voice (bible):** Wystan close and procedural; numbers not adjectives; the division of the hour; the day book's margin; one object handled per chapter; the hum and the moment it stops is the clock; the dead reported flat.

### Standing Inventory (from `session_start "Wystan Ashmore" standard Accord`)

#### STANDING INVENTORY

#### THE STANDING INVENTORY: THE GUILD ACCORD AND THE CONCORD

Note: the sources give no Concord greeting, no everyday swearing and no idiom for the items marked (d); each is derived in one step from an attested fact (the live main, the witness clause, the cased weight, the silver token, the freeman by redemption, the tongue nobody dreams in) and chosen as the plainest option. Everything else is attested in the wiki mirror.

Chartered, metered and entered. A people who did not conquer anybody and are the only layer that works in every court at once, and charge for it. **Food:** the assize loaf (weight fixed against the price of grain; a short loaf is the commonest charge on any market roll), white array-ground bread and dark hand-ground bread, and which one is on the table says what the household could afford, pulse porridge, ale at the fixed price assayed by sworn tasters, the salt bar (money that can be eaten), grounding tea for anyone who has sat too long near an Echo. Meat is a feast-day matter. **Greeting:** title before name, without exception, at any formal occasion (Prime Warden, Upper Bailiff, Master); the silver token shown at a door before the name is given (d); between neighbours the diagnostic is "Still on the main?" (d), and the answer tells you the district's pressure. **Oaths:** "Ita spondeo," thus I pledge, the only first person the chancery permits; "before witnesses" as the everyday emphatic (d); "under the seal"; Measurewrights swear the Hexagonal Oath; Enforcement and Strategic personnel carry three Oaths cut into their bones at initiation, "We see corruption, not race, creed, or kin," "Our lives are weights upon the scale," "We burn only when law demands." **Insults:** "slag," "a small button" (less to him than his reputation), "a blank" (no craft), "corded" (unreliable), "cocked" (cut off, out of the trade), "a dead leg" (on the books, does no work), "a mouth" (a speaker), "potboy" (a Drafter), "assayed" (found out), "cased" (looks solid, rings dull; d), "bought his freedom" (a freeman by redemption; d). **Time:** the Guild hour, fourteen equal hours of sixty counts pushed down the wire from Stannvaard; the turn of fourteen days ("within one turn" for any registration); Auren's day for the dead, Veyra's for markets, Irath's for musters, a court sitting on Uurgath's has chosen it; the quarterly inspection of the gauge-housing; seven years for an indenture; the Lantern's twelve years for a term of service; a man who has seen the Weight return twice is old; the Nameless day, on which nothing binds; maintenance between three and five in the morning; Year 715 of the Imperial Age, and nobody dreams in it. **The dead:** nine days above ground in the house, the sitting in shifts, and the sitting is the rite; the layer-out, who knows within the hour whether the Echo has gone; the parish roll; consecrated parish ground on Auren's day; "In registro relatum," the death entered; the excluded at the crossroads, without the roll; a death-house may not be cut for arrears; those who die in Accord service are sung each solstice, and a soldier who dies defending a Wellspring is not reclaimed. **Objects:** the meter on the wall by the door and the Board's seal on it; the standpipe, iron, waist-high, capped; the gauge-housing, brass, slate-backed, locked; the tundish; the stopcock and the cut plate; the inspector's seal press, gauge and book; the market inspector's small hammer; the silver rank token; the proof-mark, PROB EST; the strike-board; the bronze reach set into the wall at hand height; the split tally; the board in the hall with its green, blue, gold and obsidian wax; the nine-word wire; the letter of credit; the harness that cost two seasons' surplus. **Exchange:** draughts and the bill, monthly, to a chartered Board; the silver mark of twenty-four copper, and copper is the price of being alive; a letter of credit against a factor house; shares, not wages, on a Commission, with the bond posted and the losses on the subscribers; bottomry for a party without a patron; amercement set to the offender's means; fees for attestation; the entry in ink; mine scrip where the copper was melted; the tally between people who cannot read. **Proverbs, fixed wording:** "Balance before Dominion." "One weight, one measure, one reach, through all the land." "No one is measured in his own tongue." "What has been said stands said." "A clause improved is a clause void." "Where coin fades, Merit endures." "Merit spent is memory lost." "The Accord cannot hang you." "A melted coin does not testify." "A solid weight rings when struck." "Nobody dreams in Latin." (d) **Body:** the ear (the hum under a district, the dull note of a cased weight), the hands (ink and wax), sleep (children raised on a main sleep badly off it), the face at a door, which a wire-boy reads before he can read the wire.

**Recurrence, two minimum per Accord scene:** the hum, and the moment it stops; the meter, its seal and the bill; the small hammer and the dull note of a cased weight; the nine-word wire; the roll and the entry in ink.

## Rule loadout

`load_rules prose-law pov scene-structure dialogue register --brief` (tags from `loadout standard`):

```
-- 252 rules for tags ['dialogue', 'pov', 'prose-law', 'register', 'scene-structure']

R41-1-DISTANCE_IS_TWO_AXES  [Distance Two Axes Ruling C-015]  live
  R35-2's register (close, medium, distant/formal) says whose idiom the narration runs in; Pack Twenty's band (1 to 5) says how deep inside the POV it sits. Both assignments stand and neither trades off the other: Cozbi runs distant/formal at band 5.

R40-2-CELESTIAL_HOST_NAMING_PASS  [Naming Banks 2026-09-13 Celestial Host]  live
  The formal pass R20-2 was waiting for. A Celestial's name has three slots: a function-name (a function root and a measure root, coined on the Host's own vocabulary of Vow, Verdict, Boundary, Seal, Record, Tally and Toll), a rank-suffix that changes with promotion and whose loss is a stripping, and a Lawbell-name that is the Archon's own name carried bare, whose loss is the Severance. Obeys the Host's idiom rule. The five working names are kept and read back through the system. Four flags stay open as ratified, two of them canon acts for Isaac.

R39-7-NO_NPC_THOUGHT_UNDER_POV_LOCK  [Stat System and Scene Rulings 2026-09-13 C-008]  live
  The narration-distance rule wins over Pack One's Scene Standards carve-out: a named NPC gets no private italic thought in a scene with a POV lock. The carve-out survives only where there is no lock — omniscient narration and mass combat.

R35-1-NARRATION_DISTANCE_BANDS  [Narration Distances (Psychic Distance by POV) The three registers]  live
  Every POV character carries one of three narration distances — close (narration fuses with the character's own idiom, italicized direct thought available), medium (POV locked, no head-hopping, but emotion arrives by external behaviour or simile, no italicized thought) or distant/formal (an omniscient epigrammatic voice describes the character from outside, occasional aphoristic italics, the one register licensed for more narratorial explanation) — and the field is called "narration register", never "Band", because Band is the unrelated FOW Coherence stat. This supplies the whose-idiom input that R4-13-FID_CARVEOUT depends on.

R35-2-NARRATION_DISTANCE_ASSIGNMENTS  [Narration Distances (Psychic Distance by POV) Close register / Medium register / Distant-formal register / Unassigned]  live
  Close register: Darius, Aurelian, Verinus, Charles, Sodoku Moto, Niran Yukari, Wren, Kwon Mu-jin. Medium register: Rengai. Distant/formal register: Cozbi Mahuo. Each assignment carries a violation caution (never a narratorial verdict Darius does not voice himself; never validate Aurelian's certainty from outside his idiom; no neutral Church register for Verinus; no practitioner's jargon for Charles; no interpretive-summary sentences past Sodoku's procedural read; Niran's feeling only through his clinical vocabulary; Wren laconic and tactical only; Kwon Mu-jin's failing read shown from inside; no retrofitted first-person italics or verdicts for Rengai; Cozbi's explanation stays inside his self-mythologizing frame). Hild Ice and Dabney are unassigned until scenes in their own idiom exist for Isaac to rule on.

R32-1-ZETTARI_REGISTER_SWAHILI_BANTU_ARABIC  [Zettari Naming Register Ruling Standing Ruling]  live
  The Zettari bloodline's names, titles and technique names are built in a Swahili/Bantu/Arabic-flavoured register, and that register stands. The five-strata naming convention's assignment of "archaic bloodlines" to the Japonic stratum does not reach the Zettari: they are their own register, a carve-out, not a repeal. The Japonic assignment continues to govern every other archaic line (Moto, Yukari, Yuno).

R24-1-FLESHSHAPER_GOVERNING_PRINCIPLE  [Racial Voice and Dialect Guide Amendment I]  live
  Fleshshaper Goblin register is governed by the fact that they are surgeons who talk like surgeons never told to be squeamish about it.

R24-1-FLESHSHAPER_IDIOM_AND_MARKERS  [Racial Voice and Dialect Guide Amendment I]  live
  Anatomy applied to everything, not as metaphor but as their actual vocabulary (a seam, badly sutured, swelling, opened, holds under load); exactly two phonetic markers — dropped final -g on gerunds, and "th" hardening to "d" only in unstressed grammatical positions.

R24-1-FLESHSHAPER_SIGNATURES_AND_TELL  [Racial Voice and Dialect Guide Amendment I]  live
  Signature lines "That closes" (anything settled) and "Who holds it?" (their first question about any structure); under stress they become more procedural, not less, shortening to pure sequence with the reasons dropped.

R24-1-FLESHSHAPER_SYNTAX  [Racial Voice and Dialect Guide Amendment I]  live
  Short declarative clauses in working order, sequence first and reason second or not at all; they front the object ("The arm, I open here"), naming the thing being worked on before the working.

R24-2-ELADRIN_GOVERNING_PRINCIPLE  [Racial Voice and Dialect Guide Amendment II]  live
  Winter Eladrin are not silent; speech is the least of what they are doing, and the prose has to carry the rest through distance and stillness.

R24-2-ELADRIN_IDIOM_AND_SIGNATURES  [Racial Voice and Dialect Guide Amendment II]  live
  Idiom draws on weather, season and the behaviour of cold as literal analytical vocabulary (thawing/set, keeps, melted, tracked); signature lines "It keeps" and "You have moved"; under stress stillness increases and the distance grammar stops entirely.

R24-2-ELADRIN_NEVER_BARE_LINE  [Racial Voice and Dialect Guide Amendment II]  live
  Never write an Eladrin line of dialogue without a distance or stillness beat attached; a bare Eladrin line is an incomplete sentence in their language.

R24-2-ELADRIN_SYNTAX_AND_MARKERS  [Racial Voice and Dialect Guide Amendment II]  live
  No contractions ever, present tense for permanent conditions, questions phrased as statements with an expectant pause, no interrupting or overlapping; zero phonetic markers, deliberately — their unaccented perfection is enormous effort read as coldness.

R24-2-ELADRIN_THREE_CHANNELS  [Racial Voice and Dialect Guide Amendment II]  live
  Prose must render at least two of three simultaneous channels in any exchange of consequence — sparse speech that rarely carries the content, distance (approach is agreement, a half-step back is objection, turning without moving the feet is refusal), and stillness (complete stillness is often the loudest thing in the room).

R24-3-HOST_BREAKS_ON_MAXIM  [Racial Voice and Dialect Guide Amendment III]  live
  Any Host line that could appear on a temple wall has failed; if it scans as a maxim, cut it and replace it with a report.

R24-3-HOST_CORE_DEVICE  [Racial Voice and Dialect Guide Amendment III]  live
  A Host gives an answer that is correct and unusable, aware of this and unable to do anything about it — accurate rather than confident, which is what stops them sounding like scripture.

R24-3-HOST_GOVERNING_PRINCIPLE  [Racial Voice and Dialect Guide Amendment III]  live
  The Host is not speaking scripture; they report accurately, and their difficulty is that accuracy in their register does not translate into a mortal one.

R24-3-HOST_IDIOM_AND_SIGNATURES  [Racial Voice and Dialect Guide Amendment III]  live
  Idiom draws on measure, position and law (out of position, standing, no place, release a claim); light/fire/wings are banned as too obvious; signature lines "That is not the question" and "I do not have that"; under stress the Host becomes more precise and slower, with hedges appearing for the first time.

R24-3-HOST_SYNTAX  [Racial Voice and Dialect Guide Amendment III]  live
  Declarative, present tense, unhedged — never "I think" or "perhaps"; short flat subject-verb-object sentences; they answer precisely the question asked, not the question intended, which is where every conversation with the Host goes wrong.

R24-N-OVERRIDE_CAVEAT  [Racial Voice and Dialect Guide Amendment Notes]  live
  All three registers are originations contradicting no existing lore (none existed); if any culture has established speech in an unreached document, these are overridden by it.

R23-10-CHINESE_PHONOTACTICS  [Inner World Naming Amendment X]  live
  Open syllables, permitted nasal codas, no clusters; avoid the wuxia register the base guide already warns off — no four-syllable given names, no sect-title constructions, no honorific stacking.

R23-11-NAME_AVOIDANCE_WAITING  [Inner World Naming Amendment XI]  live
  The name of the recently dead is unsayable until given on; the Waiting is the silence — the body waits in the death-house because the ground is frozen, and the name waits with it, leaving a hole in the household's vocabulary that everyone steers around.

R20-2-HOLY_SEA_NAMING  [Naming Guide Amendment Part Two]  live
  Birth name (Concord Common) plus ordination name (Latin, chosen or assigned at vows) plus locative/title; a documented name in the Testimony archive carries metaphysical weight, and an undocumented person is theologically uncounted.

R20-4-PRONUNCIATION_ADAPTATION  [Naming Guide Amendment Part Four]  live
  When a name crosses cultures, the speaker's own phonology imposes itself (a Concord human flattens Dawi consonant gradation, a Dawi stress-accents a Yukari pitch-accent name); these adaptations should appear in dialogue as characterisation, not be treated as typos.

R20-5-FORMAL_ADDRESS  [Naming Guide Amendment Part Five]  live
  A practitioner's formal address follows the convention of whoever is doing the addressing (rank plus family name for the Accord, ordination name plus title for Sancta Lux, relationship-dependent honorifics at a Ketsuen court); two people in the same room may correctly address the same person by different names.

R20-5-ON_THE_PAGE  [Naming Guide Amendment Part Five]  live
  Introduce a character by whatever name the POV character would use (formal on first meeting, personal for intimates, Third Name or physical description for strangers); the narrator does not switch names without a reason, since a name-switch is a statement about the character's relationship to the reader.

R20C-21-WELL_NAMES_CLASS_MARKED  [Pack Twenty R20C-21]  live
  Both names, class-marked. Guild register a Core Concentration; common tongue a Well; going in is a descent; the people are delvers, or well-rats if you dislike them.

R20C-29-CATEGORY_NAMING_DIAGNOSTIC  [Pack Twenty R20C-29]  live
  Category naming in diagnostic voice: allowed.

R20C-31-SUBSTAT_NAMES_FACULTY_ONLY  [Pack Twenty R20C-31]  live
  Sub-Stat names never appear outside a faculty reading.

R20C-33-RESONANT_PAIRS_DIAGNOSTIC  [Pack Twenty R20C-33]  live
  Resonant Pair unlocks may be named in diagnostic voice.

R20C-35-CHANT_IN_OWN_LANGUAGE  [Pack Twenty R20C-35]  live
  The Latin chant rule folds into the repeal. A practitioner chants in their own language.

R20C-36-CLEARLY_WINS  [Pack Twenty R20C-36]  live
  Clearly wins. Character shows in what a person chooses to explain and what they leave out.

R20C-46-DOUBLET_WIDER_SCOPE  [Pack Twenty R20C-46]  live
  The Latinate/vernacular doublet takes the wider scope — every craft term in WOTR.

R20C-49-GLOSS_RIGHTS_CARD_FIELD  [Pack Twenty R20C-49]  live
  Gloss rights ratified as a card field: Lambert yes, Yoko diagnostic only, Cozbi unlimited, Sodoku never, Emira never.

R20C-50-FLESHSHAPER_VOICE  [Pack Twenty R20C-50]  live
  Fleshshaper Goblin. Old Vaross substrate.

R20C-51-WINTER_ELADRIN_VOICE  [Pack Twenty R20C-51]  live
  Winter Eladrin. Speech is the secondary channel; stillness and the angle of the hands are primary.

R20C-58-REGISTERS_FLAVOUR_NOT_LAW  [Pack Twenty R20C-58]  live
  Per-culture narration registers are flavour, not law (Pack Fifteen §1 stands). Moto register is the exception and gets built with Combat Guide 3e.

R20C-PD-PSYCHIC_DISTANCE_BANDS  [Pack Twenty Psychic-distance bands — assigned]  live
  | POV | Band | Note | |---|---|---| | Sodoku Moto | 3 | To 4 only at the moment of a decision his body has already made. Never 5.

R19-2-BUILT_AROUND  [Pack Nineteen §2]  live
  Scenes are constructed to make Isaac's fixed lines land; the dialogue is never fitted to prose written ahead of it.

R19-2-FIXED_TEXT  [Pack Nineteen §2]  live
  Isaac's submitted dialogue is set as written and never rewritten.

R19-2-NEVER_ALTERED  [Pack Nineteen §2]  live
  Register, rhythm, repetition, fragments, profanity, prosodic marks, line order, and word choice in Isaac's dialogue may never be changed, including for the sake of reading better.

R19-2-PERMITTED_CORRECTIONS  [Pack Nineteen §2]  live
  Only typos, unambiguous verb tense/agreement, required punctuation, and stale canon-term forms may be silently corrected in Isaac's dialogue.

R19-2-WORLD_BREAK_FLAG  [Pack Nineteen §2]  live
  A canon-breaking line in Isaac's dialogue is flagged once in author notes and left standing, untouched, unless Isaac rules otherwise.

R19-3-PROSODY_VERBATIM  [Pack Nineteen §3]  live
  Capitals, stretched vowels, ellipses and repeated punctuation are notation for volume, duration, breath and intensity, and must be reproduced exactly rather than converted into narrative description.

R19-3-TAG_ALONGSIDE  [Pack Nineteen §3]  live
  A narrative tag may be added next to prosodic notation but may never be used instead of it.

R19-4-COMPOSURE_COST  [Pack Nineteen §4]  live
  A character who stays composed under extreme stress is exercising an expensive discipline, and the scene must show that price.

R19-4-ICEBERG_DIALOGUE  [Pack Nineteen §4]  live
  Characters never explain to each other something they both already know.

R19-4-REALISTIC_SPEECH  [Pack Nineteen §4]  live
  Originated dialogue must include false starts and self-repair, interruption, repetition, non-answers, characters talking past each other, trailing off, physical business mid-line, and characters saying the wrong thing, as craft law rather than optional flavour.

R19-4-REGISTER_UNDER_STRESS  [Pack Nineteen §4]  live
  Under stress, a character's speech must get shorter, more concrete, more repetitive, and lose subordinate clauses, uniformly across all characters.

R19-4-WORLD_ANCHORED_SPEECH  [Pack Nineteen §4]  live
  A character's metaphors and idiom must come from their own life and trade, not from an external reference list.

R19-5-COMPOSURE_BAN  [Pack Nineteen §5]  live
  Bars antithesis and parallelism, three-part lists, long subordinate clauses in shouted speech, and perfect syntax from established inarticulate/young/exhausted/foreign characters, and bars every character in a scene from constructing sentences at the same length.

R19-5-SORT_BY_SPEAKER_TEST  [Pack Nineteen §5]  live
  If a stranger could not sort a scene's dialogue lines by speaker with the tags covered, the scene fails as a Pack Nineteen violation, not merely a voice-differentiation warning.

R19-7-CHECK40  [Pack Nineteen §7]  live
  Manual check that every line of Isaac's dialogue matches the submitted rough verbatim except for corrections permitted in §2; any other change fails and is reverted.

R19-7-CHECK41  [Pack Nineteen §7]  live
  Automatic check that fails when the submitted rough has stretched vowels, repeated punctuation or capitalised shouting that the output drops.

R19-7-CHECK42  [Pack Nineteen §7]  live
  Flags long, subordinate-heavy or parallel dialogue lines and reports the spread of line lengths across a scene, flagging files where every speaker clusters at one length.

R19-8-NO_RETROACTIVE  [Pack Nineteen §8]  live
  No rewrite of scenes written before this pack is proposed; the pack governs dialogue written from here forward.

R18-3-CODEX_OVERRIDES_LEXICON  [Pack Eighteen §3]  live
  Pack Sixteen's route-1 rough-prose conversion now means routing to a Codex term, and where the Pack Sixteen §4 conversion lexicon disagrees with the Codex sheet, the sheet wins.

R18-4-GLYPH_NAMING_CONTEXTS  [Pack Eighteen §4]  live
  Glyphs are named only in a document, an instrument, a practitioner's diagnostic voice, or a private count; narration may state what a glyph did without announcing the bracketed form.

R16-1-CONSEQUENCE  [Pack Sixteen §1]  live
  The technical and metaphysical register belongs in the finished narration itself, in Isaac's vocabulary, converted rather than removed or exported to notes.

R16-2-DELETION_REQUIRES_NOTE  [Pack Sixteen §2]  live
  If a rough-draft term does not survive into the finished prose in one of the four routed forms, the author notes must say which term was dropped and why, in one line, or the pass has failed.

R16-2-FOUR_ROUTES  [Pack Sixteen §2]  live
  Every content-bearing noun and verb in Isaac's rough prose is routed to a WOTR system term, a real scientific/technical term, the compound of both, or kept verbatim as a defined WOTR term; nothing is silently dropped.

R16-3-COMPOUND_SENTENCE  [Pack Sixteen §3]  live
  The signature WOTR technical sentence names the real phenomenon, gives the system term as its name/boundary/address, and states the physical consequence, in one sentence or short group; neither element is a gloss on the other.

R16-4-EXTEND_LEXICON  [Pack Sixteen §4]  live
  The rough-to-converted term lexicon is built from Isaac's actual submissions and extended every session; anything converted in play must be entered in it or it does not exist as a settled conversion.

R16-5-NOT_IN_NOTES  [Pack Sixteen §5]  live
  If a mechanism term appears in the author notes but not in the prose, the pass failed and the note is evidence of that failure.

R16-5-REGISTER_IN_NARRATION  [Pack Sixteen §5]  live
  The Technical Register is available to third-person narration for anything a person chooses to do; it is not reserved for italic thought.

R16-5-VOICES_VS_VOCABULARY  [Pack Sixteen §5]  live
  The four explaining voices remain the delivery system for causal explanation only; narration itself may carry technical terms without needing a voice to speak them.

R16-6-COINAGE_COLLISION  [Pack Sixteen §6]  live
  Where a coinage collides with existing canon, the collision is surfaced and both readings are stated, per the standing rule against silent resolution.

R16-6-COINAGE_HANDLING  [Pack Sixteen §6]  live
  A term in Isaac's rough with no canon equivalent is a coinage: it is converted into a defined WOTR term, kept in the prose, given a one-line definition in the author notes, and entered on the Open Rulings Docket for ratification, never silently replaced with a plainer word.

R16-6-SPELLING_VS_VOCABULARY  [Pack Sixteen §6]  live
  Spelling and grammar in Isaac's rough are corrected without comment; vocabulary is never silently corrected.

R16-7-NOT_CONVERTED  [Pack Sixteen §7]  live
  Conversion applies to mechanism, phenomenon, technical read, injury and the physics of an exchange, but never to the body's plain physicality, grief and the elegiac beat, dialogue (outside a practitioner's diagnostic voice or a document), or the ignorance quota.

R16-7-OVERCONVERSION_FAULT  [Pack Sixteen §7]  live
  A scene that converts everything has the same fault as a scene that converts nothing: it has stopped choosing.

R16-8-CHECK30  [Pack Sixteen §8]  live
  A scene with a working, exchange or injury must carry at least four WOTR technical-lexicon terms and at least two correctly-used real scientific/anatomical terms in the narration outside italics; false positives are reviewed by reading.

R16-8-CHECK31  [Pack Sixteen §8]  live
  No mechanism term may appear in the author-notes block that does not also appear in the prose body.

R16-8-CHECK32  [Pack Sixteen §8]  live
  Every distinctive term in the submitted rough must appear in the output in one of the four routed forms, or be listed as dropped in the notes; false positives are reviewed by reading.

R16-8-CHECK33  [Pack Sixteen §8]  live
  Fewer than half of a scene's technical terms may sit inside italic thought.

R15-1-AI_TELL_CHECKS_SURVIVE  [Pack Fifteen §1]  live
  The AI-tell checks (em dashes, similes, not-X-but-Y, countdown negation, gloss, ladder) are about prose failing, not about period, and are unaffected by the register repeal.

R15-1-DICTION_PALETTE  [Pack Fifteen §1]  live
  The one-or-two-elevated-words-per-scene cap is gone; the word bank remains available.

R15-1-ELEVATED_VOCAB_OPTIONAL  [Pack Fifteen §1]  live
  The Elevated Vocabulary Standard stops being a mandate; its words stay available but nobody counts them.

R15-1-LATIN_CHANT_SURVIVES  [Pack Fifteen §1]  live
  Latin for chant-based magic is not a register rule but a texture choice Isaac made, and it stands unless he says otherwise.

R15-1-LICENCE  [Pack Fifteen §1]  live
  Modern words, concepts and frames are legal in every channel of the prose, including narration and in-world documents.

R15-1-MYSTIC_REGISTER_NEVER_PHYSICS_STRUCK  [Pack Fifteen §1]  live
  Pack Twelve §6's clause forbidding a document from explaining mechanism is struck; a document may be as scientific as it wants, and the Mystic Register survives only as an option for documents that want to withhold.

R15-1-RACIAL_VOICE_MENU  [Pack Fifteen §1]  live
  The Racial Voice and Dialect Guide and its Amendment stop being enforced; they become a menu of options a writer may reach for, and no scene fails for ignoring them.

R15-1-READS_MODERN_STRUCK  [Pack Fifteen §1]  live
  Natalie no longer raises, fixes, or notes "reads modern" as a critique on principle.

R15-1-REGISTER_BY_CULTURE  [Pack Fifteen §1]  live
  Per-culture narration registers become optional flavour rather than law.

R15-1-TECHNICAL_REGISTER_SURVIVES  [Pack Fifteen §1]  live
  Packs Twelve, Thirteen and Fourteen's Technical Register for combat and workings is not a register rule in this pack's sense and is unaffected; this pack makes explanation in real terms easier, not harder.

R15-1-VOICE_DIFFERENTIATION  [Pack Fifteen §1]  live
  Characters must remain non-interchangeable, but through what they notice, want and refuse rather than through vocabulary fences.

R15-2-NO_REGISTER_EDIT  [Pack Fifteen §2]  live
  Register is never corrected during editing and alternate less-modern phrasings are never offered.

R15-2-ONE_TEST  [Pack Fifteen §2]  live
  A word is flagged only if it punctures belief in the world, and the flag goes in author notes with the draft left untouched.

R15-4-MEMORY_ENTRIES_SUPERSEDED  [Pack Fifteen §4]  live
  Memory entries thirteen, fourteen, twenty-nine and thirty (accent calibration, phonetic markers, Racial Voice guide, elevated vocabulary) are superseded as mandates and retained only as available technique; flagged for the memory sweep.

R15-4-PACK_FIVE_SCOPE  [Pack Fifteen §4]  live
  Only Pack Five's register-by-culture rule is struck; its dramatic irony through POV lock, the elegiac mode, humour recalibration, and narration authority all stand because none of them are register rules.

R15-4-PACK_NINE_CLASS_MARKING  [Pack Fifteen §4]  live
  Pack Nine's requirement that class show in vocabulary becomes optional.

R15-4-THIRTEEN_HAX_STRUCK  [Pack Fifteen §4]  live
  Pack Thirteen §6's ban on a character saying "hax" is struck; a character may say whatever makes him interesting, though scaling vocabulary stays author-notes-first as adjudication vocabulary, not because it is modern.

R15-4-TWELVE_VOICE_DISCIPLINE_SOFTENED  [Pack Fifteen §4]  live
  Pack Twelve §4's voice discipline clause is softened from a stricter requirement to "may differ."

R15-4-VERIFY_UNCHANGED  [Pack Fifteen §4]  live
  wotr_verify.sh has no check that touches register, and this pack adds none.

R14-4-DIAGNOSTIC_CHANNEL  [Pack Fourteen §4]  live
  Stat names, Sub-Stat names, Grades, Bands, eta, AU/s, EU counts, Aether Class, Crystal State and Category names reach the page only in a mouth, an instrument, a document, or a practitioner's private count, rationed per Pack Twelve §5, and class-marked per Pack Nine.

R14-4-EFFECTS_CHANNEL  [Pack Fourteen §4]  live
  Every stat that decided an outcome must show on the page as behaviour and physics; grade letters and stat names never appear in narration, only their consequences.

R14-4-SUBSTAT_DIAGNOSTIC_ONLY  [Pack Fourteen §4]  live
  Sub-Stat names are the finest grain the system has, and only a faculty reading reaches for them; nobody else does.

R14-6-CHECK28  [Pack Fourteen §6]  live
  Any Grade letter, Stage name, Band, eta, AU/s, EU figure, or Sub-Stat name outside quotation marks, italics, or a marked document block fails.

R13-4-DENSITY_BUDGET  [Pack Thirteen §4]  live
  A 2,500-word duel carries the full eight-item floor at first display and finisher, plus items 1-4 at every fight-changing exchange; a 700-1,500-word turn carries items 1-4 once and item 8 at close.

R13-4-THREE_EXPLANATIONS  [Pack Thirteen §4]  live
  At first display and finisher, physics, Essence and Hermetic correspondence must each appear as a causal sentence beside its image, not as the image alone.

R13-6-ANATOMY_VOCAB  [Pack Thirteen §6]  live
  Anatomy is named by structure, fractures by fracture type, and neurological consequence by name.

R13-6-ANIME_GRAMMAR_TRANSLATION_AID  [Pack Thirteen §6]  live
  Anime shape-vocabulary (Nen's shroud/stop/output/expression, Naruto's shape/nature split, JJK's vow and reversal, Bleach's release) is used only to identify which shape a working needs, then written in WOTR's own words; it never appears as page vocabulary.

R13-6-CHEMISTRY_BAN_SCOPE  [Pack Thirteen §6]  live
  Pack Six's chemistry ban survives, but only for ambient sensory impression; it does not touch a hit, a wound, or a working.

R13-6-HEMA_VOCAB  [Pack Thirteen §6]  live
  Combat vocabulary draws on the full HEMA range (spear/staff, poleaxe, dagger, grappling, messer, sword and buckler, mounted lance) with a percussion master-strike table built for the hammer specifically.

R13-6-METAPHYSICS_VOCAB  [Pack Thirteen §6]  live
  Correspondence, sympathy and contagion, essence and accident, form and actualisation, and recognition and refusal are the vocabulary of stratum two's Attraction-side reads and of the document voice.

R13-6-REAL_SCIENCE_VOCAB  [Pack Thirteen §6]  live
  Real scientific terms (pressure differential, gradient, latent heat, phase transition, dielectric breakdown, resonance, cavitation, nucleation, information entropy, boundary condition, and the rest) are the vocabulary used to explain what a WOTR noun is doing.

R13-6-SCALING_VOCAB_RESTRICTED  [Pack Thirteen §6]  live
  Scaling-comparison vocabulary (Attack Potency, durability, hax as a concept, speed blitz, reaction vs combat speed, striking vs lifting strength, range, outlier, anti-feat) is used only in author notes and adjudication, never on the page, to keep Natalie honest about who wins and why.

R13-6-WOTR_FIRST  [Pack Thirteen §6]  live
  The glossary and Codex's own nouns (the Planes, Aether, Essence, the Soul Crystal and its layers, Crystal States, Attraction/Obsession Force, the Sixty, the Families, the Categories, the Mechanism Vocabulary, EU/Flux Density/AU-s/eta/Band/Grade/Stage) are used in preference to anything borrowed.

R13-9-STYLE_DIRECTIVE_MECHANISM_VOCAB  [Pack Thirteen §9]  live
  Bare jargon mid-action stays banned, but a Mechanism Vocabulary term may now be named in diagnostic voice alongside its dramatisation.

R12-1-PACK_SEVEN_REPEALED  [Pack Twelve §1]  live
  Pack Seven, the Soft Magic Amendment, is repealed in full; six of its specific provisions are individually struck (see the other §1 rows), and where Twelve conflicts with Seven, Seven is struck.

R12-2-MYSTIC_REGISTER_DEF  [Pack Twelve §2]  live
  The Mystic Register governs Wellsprings, sites, rites, oaths, the Veil, and anything the world does regardless of who is watching; it is stated as law, never as physics — imperative rules, prices given as prices, taboos given without justification.

R12-2-NO_MIXING  [Pack Twelve §2]  live
  A passage that mixes the Technical and Mystic registers reads as a textbook and is the pack's primary failure mode.

R12-2-REGISTER_TEST  [Pack Twelve §2]  live
  If a person chose to do a thing, it is Technical Register. If it was already running before anyone noticed, it is Mystic Register.

R12-2-TECHNICAL_REGISTER_DEF  [Pack Twelve §2]  live
  The Technical Register governs combat, craft, injury and anything a practitioner does on purpose; exhaustive, tactical, delivered in-fight, explaining the read, the fault, the counter, the reserve and why the answer worked, in real vocabulary.

R12-3-DESIGN_CHAIN_RETURNS  [Pack Twelve §3]  live
  The Design Chain (Trigger, Function, Mechanism, Numerical Effect, Target Response, Consequence, Limitation, Weakness, Cost, Counterplay) is fully prose-legal, distributed through the scene rather than workbook-only.

R12-4-VOICE_DISCIPLINE  [Pack Twelve §4]  live
  A Measurewright, a Kharven hunter and an Accord officer explain the same phenomenon in three different vocabularies; which words a mouth reaches for remains class-marking per Pack Nine.

R12-4-VOICE_FOUR_DOCUMENT  [Pack Twelve §4]  live
  An in-world register entry, field manual, or codex line dropped in at a scene threshold (the LotM model), using the Mystic Register and setting a rule the scene then breaks.

R12-4-VOICE_MIXING_RULE  [Pack Twelve §4]  live
  Confirmed by Isaac's ruling: the four explaining voices may mix, whoever is in the scene, picked per scene, with no more than two run in one engagement.

R12-4-VOICE_ONE_POV  [Pack Twelve §4]  live
  Free indirect explanation ceilinged at the POV character's actual competence; an out-of-depth character explains wrong, and a confidently wrong technical explanation is now the primary vehicle for the misreading budget.

R12-4-VOICE_THREE_OPPONENT  [Pack Twelve §4]  live
  A practitioner explains exactly what he is doing to his target while doing it, because he does not believe the explanation will help; the most economical and characterful voice, barred to anyone without standing to be arrogant.

R12-4-VOICE_TWO_SECOND  [Pack Twelve §4]  live
  A present observer who understands what the POV does not, narrating the read to a third party or himself (the Kakashi model); requires an actual reason to be present and talking, best carried by teachers, rivals, Measurewrights, or the Research and Archives Division.

R12-5-NUMBERS_DIAGNOSTIC_ONLY  [Pack Twelve §5]  live
  EU, AU/s, eta, Coherence, Grade and Band numbers may not reach third-person narration on the narration's own authority; they are legal only in diagnostic voice (a faculty reading, a practitioner counting reserve, a document, an instrument, or a speaking character).

R12-6-MYSTIC_GRAMMAR  [Pack Twelve §6]  live
  The Mystic Register's grammar: imperative without justification, price stated exactly with no reason given, correspondence in place of causation, attribution to an uncertain institution, and the recorded failure documented in flat administrative prose.

R12-6-RULES_AS_RULES  [Pack Twelve §6]  live
  The Mystic Register states consequences without offering mechanism (the canonical example: do not carry Object Wellsprings into Site Wellsprings, no mechanism given, a stated consequence, the Guild has buried those who tested it); more sentences are written in that shape.

R12-7-AI_TELLS_RETAINED  [Pack Twelve §7]  live
  The Ladder ban, the Gloss budget of zero, local burstiness, the reification budget, and every AI tell in the checklist survive unchanged; explaining a mechanism is no licence to write badly.

R12-7-IGNORANCE_MISREADING_RETAINED  [Pack Twelve §7]  live
  The ignorance quota and misreading budget survive Pack Twelve intact and become more important as dramatic-irony tools now that explanation is the default; the wrong explanation is now the load-bearing device.

R12-7-LEGIBILITY_BAN_STRUCK  [Pack Twelve §7]  live
  Pack Six's total-legibility ban and blanket interpretation-at-zero rule are struck.

R12-8-SCENE_GUIDE_PACK7_STRUCK  [Pack Twelve §8]  live
  The Scene Writing Process Guide's Pack Seven pre-write question and self-review check are struck.

R12-8-SCENE_STANDARDS_BANS_STRUCK  [Pack Twelve §8]  live
  Scene Standards' sentence-level bans on mechanism explanation and metaphysical numbers are struck; everything else in Scene Standards stands.

R11-1-TONAL_SPINE_UNCHANGED  [Pack Eleven §1]  live
  Pack Five stands in full; the Western Register still governs characterisation, humour and narration authority. Pack Eleven widens what the page may look like, not what it may sound like.

R11-2-VOCABULARY_TIERS  [Pack Eleven §2]  live
  "The draw, the hum, a standpipe, a housing, the meter, cut off" are common-tongue and prose-legal under Pack Nine's craft-register carve-out; "concentration, density, coupling, eta" are Guild register and document-only.

R11-3-FIREARM_PROSE_LAW  [Pack Eleven §3]  live
  The gun is furniture, not spectacle; no sentence explains why a proofed round defeats proofed plate — the physical account of the hole stays, the causal account is cut.

R11-4-DESCENT_PROSE_LAW  [Pack Eleven §4]  live
  A descent's sensory opening favours the body (feet, teeth, pack weight) over the room; the ignorance quota becomes the ambient condition rather than a per-scene quota, and a misidentified encounter type is the best-shaped disaster the setting offers.

R11-4-SURVEY_PROTOCOL  [Pack Eleven §4]  live
  Deploy in pairs with one member outside the radius; take Crystal baselines before the march, never after; never carry Object Wellsprings into Site Wellsprings; withdrawal is not retreat; report Medium-type as priority; every rule is one a character can break, and the Guild has buried those who did.

R11-4-WELL_NAMING  [Pack Eleven §4]  live
  Guild register calls it a Core Concentration; common tongue calls it a Well; going in is a descent, and the people who do it are delvers or well-rats.

R10-2-CATEGORY_READ_EXCEPTION  [Pack Ten PART TWO]  live
  A scene's single diagnostic read (the Apparatus Rule's existing budget, not a new one) may be spent naming the category instead of a Wellspring or Family; naming a category doesn't trip Check 20, but it still costs the scene's only read.

R10-2-CATEGORY_REGISTER_DEFAULT  [Pack Ten PART TWO]  live
  Category names sit at Wellspring/Family register, not common tongue, and stay workbook and Codex-line by default.

R10-3-EFFECT_PHYSICAL_ONLY  [Pack Ten PART THREE]  live
  A projected shape's Effect describes only what it looks/does/feels like, never why the Wellspring resolved as that particular shape; if that answer exists at all, it stays workbook, one line, never on the page.

R10-3-UNCHANGED_CONSTRAINTS  [Pack Ten PART THREE]  live
  A projected shape still counts toward the one splash-panel beat per scene (Pack Nine), still costs the one diagnostic read per scene if the category is named, and the ignorance quota/misreading budget are untouched — a POV may see a projected shape and get it wrong.

R9-2-CLASS_MARKED_CRAFT_WORDS  [Pack Nine PART TWO]  live
  Which word a character uses for a craft is characterisation: an Engraver says "the cutting," a Kharven soldier says "a man who can do the writing," and nobody says "Runecraft" aloud except an Accord examiner filling in a form.

R9-2-COMMON_TONGUE_LEGAL  [Pack Nine PART TWO]  live
  A POV may be shown cutting a ward, speaking a working, or pouring a Draft (singing pending Chantcraft's ruling); the common tongue for craft actions is prose-legal, said the way the character would actually say it, while the Accord Latin terms stay document-only.

R9-2-UNTOUCHED_BANS  [Pack Nine PART TWO]  live
  The mechanism gloss ban (Check 20), the metaphysical-units ban (Check 21), the chemistry ban, and the physical-Effect rule are untouched — a line may say a man cut a ward into a doorframe but may not say why the cutting suppressed the Essence.

R9-2-VOCAB_BAN_NARROWED  [Pack Nine PART TWO]  live
  Pack Seven's ban on system vocabulary in prose still binds absolutely against Wellspring names, Family, Physics Domain, Stage/Grade, EU, other metaphysical units, and Codex glyph designations; it no longer binds against the craft register.

R9-3-AURA_AS_FRACTURE  [Pack Nine PART THREE]  live
  Essence discharge reads as broken, shard-edged geometry around the body rather than a soft glow; "it glowed" stays banned, replaced for Stage-display beats specifically, not as a general phenomenon substitute.

R9-3-COST_UNCHANGED  [Pack Nine PART THREE]  live
  The ignorance quota, the misreading budget, and the one-read Apparatus Rule bind a Stage-display beat exactly as hard as any other scene.

R9-3-SILHOUETTE_ENTRANCE  [Pack Nine PART THREE]  live
  A practitioner arriving at an unclassified Pressure is staged backlit, shape before detail, using the existing Section 3 silhouette tool now explicitly licensed for power-arrival rather than rationed to dread generally.

R8-15-DESCRIPTION_STYLE  [Pack Eight 1.5]  live
  The description is written the way a man teaching it would write it: flat operational prose, no mood, no cadence work, no elegiac register — that belongs in scenes.

R8-21-REGISTER_TABLE  [Pack Eight 2.1]  live
  Where a request specifies a register, that register governs and the name is built in it first: Concord/Accord/Guild/Sancta Lux is Latinate; Ketsuen/Japonic houses use Japanese; Korean-register houses use Korean; Büri is Mongolian; Dawi is stressed Germanic-Norse compound; Eresse is Latinate with elvish morphology; Parunic and older strata use Parun etymology.

R8-22-BY_NAME_POETRY  [Pack Eight 2.2]  live
  The by-name, where an art has one, sits after the gloss and is what other characters call it — the one place poetry is allowed.

R8-23-NAME_HIERARCHY  [Pack Eight 2.3]  live
  Naming runs art, then technique, then form; the art carries the character and is spoken once at release then assumed, while individual techniques are spoken every time they are used.

R8-24-RELEASE_MECHANIC  [Pack Eight 2.4]  live
  An art with a true name may carry a release call (imperative verb plus name); it is never required for the art to function, costs a beat for a measurable output increase, and is spoken indistinguishably by a man in real danger or a man showing off.

R8-26-GLOSS_DEPENDENCE_FAILS  [Pack Eight 2.6]  live
  A working whose meaning must be glossed for the scene to land is a working that failed; fix the working, not the gloss.

R8-26-GLOSS_NEVER_IN_PROSE  [Pack Eight 2.6]  live
  The gloss never appears in prose, with no translation apposition; the reader gets it from the sheet or from another character explaining it in dialogue for their own reason.

R8-26-NAME_NEVER_NARRATED  [Pack Eight 2.6]  live
  The true name is spoken by a character; it never appears in narration.

R8-26-NO_SELF_TRANSLATION  [Pack Eight 2.6]  live
  Nobody translates their own technique's name aloud, ever.

R8-26-ONE_RELEASE_PER_SCENE  [Pack Eight 2.6]  live
  One release per scene at most; two men releasing in the same scene is an event, not texture.

R6-1-LADDER_BAN  [Pack Six PART I.1]  live
  Two or more clauses of the form "X was Y and Y was Z" in one sentence is an automatic cut, never a rewrite; cut back to the first concrete noun. Restating a concrete observation as an abstraction in the following sentence is barred the same way.

R6-10-INVENTORY_AND_ELEGY  [Pack Six PART II.10]  live
  Pack Five's elegiac register requires a named concrete thing that is gone, and the Inventory is where those things live; elegy without an Inventory is grief for abstractions, which Pack Five already bars.

R6-11-CHECK18_LADDER  [Pack Six §11]  live
  Flags any sentence containing two or more instances of the "was X and the X was" pattern, including is/became/meant variants.

R6-11-CHECK19_APPARATUS_SUBJECT  [Pack Six §11]  live
  Flags any sentence where a named faculty is the grammatical subject of a perception verb; high false-positive rate by design, reviewed by reading.

R6-12-TELL_BANK_SURVIVING  [Pack Six §12]  live
  Added to the AI tells checklist and retained in full per Pack Twelve §7 — the Ladder in all forms, the apparatus as grammatical subject, scientific vocabulary explaining an ambient sensory impression, and fresh texture invented where Inventory texture exists.

R6-2-CHEMISTRY_BAN  [Pack Six PART I.2]  live
  Real-world scientific vocabulary explaining a sensory impression is barred unless the POV is a practitioner of that specific craft actively diagnosing; the Mechanism Standard governs technique trigger points and nothing else, never a licence for ambient exposition.

R6-2-FACULTY_NEVER_SUBJECT  [Pack Six PART I.2]  live
  A named faculty is never the grammatical subject of a perception verb; the character perceives, the apparatus does not act on its own behalf.

R6-2-READ_DELIVERS_FACT  [Pack Six PART I.2]  live
  A faculty's read delivers a bare fact ("Twenty-three"), never an interpretation woven around it; the faculty is an instrument and instruments produce numbers, not meaning.

R6-3-IGNORANCE_QUOTA  [Pack Six PART I.3]  live
  At least one thing per scene the POV notices and cannot interpret; the narration does not rescue him, and resolution comes in a later scene or chapter.

R6-4-MISREADING_BUDGET  [Pack Six PART I.4]  live
  At least one POV inference per scene is wrong and is not corrected on the page; the misreading must be reasonable, consistent with what the POV knows, and left standing for the reader to find later.

R6-5-MATERIAL_DENSITY_SURVIVES  [Pack Six PART I.5]  live
  Material density (rust, weathering, wear, labour) stays described in full per the Directive; the distinction is that the world is described exhaustively but interpreted at zero — meaning and thematic weight are withheld.

R6-9-RECURRENCE_RULE  [Pack Six PART II.9]  live
  Every scene draws texture from the Inventory before inventing anything; anything newly invented is entered into the Inventory the same session or it does not exist; each culture designates three-to-five high-frequency signature items on the Recurrence Ledger.

R5-A-FLESH_CHANGES  [Pack Five A]  live
  Prose register, humour, characterisation method, narration authority and tonal architecture derive from the Western tradition (Martin's POV discipline, Tolkien's cultural register and elegiac capacity, Abercrombie's dry brutality).

R5-A-OPERATIVE_CONSEQUENCE  [Pack Five A]  live
  The system is author-facing and document-facing — it lives in the Codex, character sheets, in-world treatises and technical-reveal beats; it does not live in prose texture, narrator commentary, or character affect.

R5-A-SKELETON_UNCHANGED  [Pack Five A]  live
  WOTR runs an Eastern skeleton under Western flesh; the systematic density (Stages, Wellsprings, Bands/Grades/Coherence/eta, Codex glyph grammar, Family/Physics Domain, the character sheet, the Design Chain, EU costs) does not get diluted, softened, or made impressionistic.

R5-B-DECLARATION_TO_INFERENCE  [Pack Five B]  live
  A character is established by what they choose under pressure, what they refuse, what they notice first, and what others say about them when absent — not by being vividly themselves in every line; the reader assembles the person.

R5-B-FOIL_FUNCTION_SURVIVES  [Pack Five B]  live
  Deliberate moral and rhythmic contrast between paired characters (Merry/Pippin, Sam/Frodo, Tyrion/Bronn, Jaime/Brienne, Glokta/Severard) is Western-native and remains actively tracked.

R5-B-MANHWA_DIRECTIVE_REPEALED  [Pack Five B]  live
  Personality vomiting, reaction shots as characterisation, loud opinions as a default register, bizarre/exaggerated minor NPCs, absurdist method alongside genuine stakes, humour as a tone exception, and escalation as a prose-level pacing register are no longer craft law and become active tells; escalation survives only as plot architecture (Scene Writing Process Guide §2).

R5-B-YOKO_SODOKU_SURVIVES  [Pack Five B]  live
  Yoko against Sodoku is a precision-versus-instinct foil, not a comedy routine; its humour now arrives through what Yoko declines to say, never a deadpan beat landing on a punchline.

R5-C1-INFO_TRACKED_PER_POV  [Pack Five C.1]  live
  Before a scene, name what this POV knows, what they wrongly believe, and what the reader knows that they do not.

R5-C1-NARRATION_NEVER_WINKS  [Pack Five C.1]  live
  No line acknowledges that the reader knows better than the POV.

R5-C1-WELL_REASONED_WRONG_CONCLUSION  [Pack Five C.1]  live
  Irony built on a character being stupid is not irony; a POV must apply sound reasoning to a corrupted premise, not simply be foolish.

R5-C1-WRITE_FROM_LEAST_KNOWING  [Pack Five C.1]  live
  Where a scene could be written from two POVs, write it from whoever knows least about what is coming; a default, breakable with reason.

R5-C2-ELEGY_CONCRETE_THING  [Pack Five C.2]  live
  Elegy attaches to a named concrete, specific thing that is gone (a road, a dye colour, a lost word, a dying craft), never to abstractions; grief for "the old world" is furniture.

R5-C2-FLAT_DELIVERY  [Pack Five C.2]  live
  Section 1.2's saga restraint governs elegy: state the loss and move on, without raising the prose's voice.

R5-C2-IRREVERSIBLE_NOBODYS_FAULT  [Pack Five C.2]  live
  What distinguishes elegy from grimdark's systemic cruelty is that the loss is often irreversible and often nobody's fault; some things are simply taken, some simply end.

R5-C2-ONE_PASSAGE_BUDGET  [Pack Five C.2]  live
  At most one sustained elegiac passage per scene, which may sit anywhere except the closing beat, which still ends on physical action per Scene Standards.

R5-C3-NARRATION_REGISTER_EXTENSION  [Pack Five C.3]  live
  Free indirect discourse's per-character register licence is raised to a per-culture one: proposed narration registers include Dawi (stressed monosyllables, concrete nouns, sentence-level distrust of abstraction), Eresse (subordination, latinate diction, periodic sentences), Concord human (the house baseline), and Moto (to be built, highest-priority gap).

R5-D-FUNERAL_TEST  [Pack Five D]  live
  Could this line be said at a funeral, by someone who means it, without breaking the room? If the humour needs a comedic frame to work, cut it.

R5-D-HUMOUR_BARRED  [Pack Five D]  live
  The beat structure of setup, deadpan and reaction is barred; humour arrives inside dialogue and narration already in progress and never pauses the scene to land.

R5-D-HUMOUR_CASTING  [Pack Five D]  live
  Lambert carries institutional dryness in the debrief; Pietro carries contempt as wit; Yoko is accidentally funny through literalism; Sodoku does not make jokes and should not start.

R5-D-HUMOUR_PERMITTED  [Pack Five D]  live
  Humour is no longer an exception to tone but a property of specific characters in the Abercrombie register: dry understatement, gallows wit from those whose profession earns it, class-inflected contempt, a character being funny without knowing it, and the joke that is also a threat.

R5-E-ELEGIAC_REGISTER_ALLOWED  [Pack Five E]  live
  The elegiac register is available to scene narration because elegy in the saga mode reports a loss rather than judging it; Section C.2's flat-delivery rule is what keeps it on the correct side of the line.

R5-E-ELEVATED_REGISTER_QUARANTINED  [Pack Five E]  live
  The elevated register (invocation, myth-cadence, high style) is available only to in-world documents, songs, oral-tradition passages, mythic strata, prophetic/Celestial Host material, and the opening/closing frame of a mythic-scale event — not ordinary scene narration.

R5-E-FREE_INDIRECT_CARVEOUT  [Pack Five E]  live
  A moral verdict in the POV's own idiom, which could be wrong, is characterisation; the same verdict in the narrator's neutral register is Tolkien's voice and gets cut, per Pack Four's gloss test.

R5-E-MARTIN_WINS_RULING  [Pack Five E]  live
  Martin wins on narration authority: Tolkien's elevated and elegiac register is available, his moral voice is not.

R5-E-NARRATION_NEVER_ADJUDICATES  [Pack Five E]  live
  Third-person scene narration is POV-locked and never adjudicates; no line tells the reader what to think of a character's choice.

R5-F-LIGHT_NOVEL_KEPT  [Pack Five F]  live
  The chapter as a hard unit with one objective and a hook at close; legibility as reader pleasure (the argument for the Codex); and fast entry, chapters opening inside the situation.

R5-F-LIGHT_NOVEL_NOT_KEPT  [Pack Five F]  live
  Status screens, panels and HUD-style rendering (already banned); narrator explanation of the system to the reader; the isekai commentary register (wry narrator asides about the world's rules); and character-sheet vocabulary (Stage, Grade, eta, Band) surfacing in prose.

R5-G-PROJECT_INSTRUCTIONS_EDIT  [Pack Five G]  live
  The Manhwa Energy Directive block is struck in full from project instructions, "manhwa-cinematic" and "manhwa energy" are struck from tone descriptions, and the genre-intersection statement is amended so only the pacing ambition survives.

R5-G-STYLE_DIRECTIVE_EXCLUDED_LIST  [Pack Five G]  live
  The Master Style Directive's §10 deliberately-excluded list gains the Manhwa Energy Directive.

R5-G-STYLE_DIRECTIVE_HUMOUR_POINTER  [Pack Five G]  live
  The Master Style Directive's §4 final paragraph (the manhwa-energy humour clause) is deleted and replaced with a pointer to Pack Five Section D.

R5-G-TELL_BANK_ADDITIONS  [Pack Five G]  live
  Declarative characterisation and the reaction-shot cutaway (from Section B's confirmed repeal) plus the comedic beat structure and narrator moral adjudication (from Sections D and E, still proposed) are added as active tells.

R4-13-DELETION_TEST  [Pack Four Amendment Thirteen]  live
  Delete the candidate sentence and read the passage; if it means the same thing, it was a gloss and stays deleted; if meaning is genuinely lost, the failure is in the line above and that line is rebuilt, never the gloss restored.

R4-13-FID_CARVEOUT  [Pack Four Amendment Thirteen]  live
  A sentence in the POV's own idiom that could be wrong and reveals the character interpreting is characterisation and is kept; a sentence in the narrator's neutral, authoritative register that reveals nothing about anybody's interior is cut.

R4-13-GLOSS_DEFINED  [Pack Four Amendment Thirteen]  live
  A gloss is any sentence whose only function is to state the significance of the sentence before it, disguised as texture or observant narration.

R4-13-THIRD_RECURRENCE  [Pack Four Amendment Thirteen]  live
  A loaded word gets one physical response on first use and no comment; meaning arrives on the third appearance through change — another character uses it, the usual user withholds it, or register makes earlier uses retroactively legible. Withholding is the strongest of the three.

R4-13-THREE_DISGUISES  [Pack Four Amendment Thirteen]  live
  The etymological gloss explains why a character chose a word; the register gloss explains what a tone signified; the stakes gloss restates in abstract vocabulary an event the reader already watched concretely, usually at paragraph-end.

R4-13-WHERE_SIGNIFICANCE_LIVES  [Pack Four Amendment Thirteen]  live
  Significance may live in a physical tell adjacent to the line, in another character's bodily reaction, or in a governed callback — never in narration itself.

R4-13-ZERO_BUDGET  [Pack Four Amendment Thirteen]  live
  The gloss budget is zero per scene; there is no acceptable first instance.

R4-14-APPROACH_LADDER  [Pack Four Amendment Fourteen]  live
  Decelerate into the hit (long, then medium, then the landing) so the reader's eye slows as it arrives, then expand again afterward since consequence is cumulative and belongs in cumulative syntax.

R4-14-CHAIN_CEILING  [Pack Four Amendment Fourteen]  live
  No more than two consecutive sentences may run over 25 words; the third breaks, or the paragraph does.

R4-14-CLAUSE_CAP_AT_BEAT  [Pack Four Amendment Fourteen]  live
  Within the three sentences bracketing a value turn, no sentence carries more than one subordinate or coordinate clause.

R4-14-CONJUNCTION_AUDIT  [Pack Four Amendment Fourteen]  live
  Count coordinators per sentence (and, as, while, which, because); two or more inside a beat-carrying sentence is a fail, though the same count outside a beat is style and left alone.

R4-14-HARD_CEILINGS  [Pack Four Amendment Fourteen]  live
  A payoff sentence carries at most 10 words and zero subordinate clauses; at least 18% of a scene's sentences run under 8 words; and no paragraph closes on three consecutive sentences over 18 words.

R4-14-LANDING_RULE  [Pack Four Amendment Fourteen]  live
  The emotional hit takes the shortest sentence in its paragraph and sits last; anything trailing it is the paragraph clearing its throat after the point.

R4-14-PARAGRAPH_VARIANCE  [Pack Four Amendment Fourteen]  live
  Sentence-length variance is enforced at the paragraph level, not just the document level; the global CV stays as a floor and stops being sufficient on its own.

R4-14-RUN_RULE  [Pack Four Amendment Fourteen]  live
  No three consecutive sentences may fall within forty percent of each other's word count.

R4-15-BODIES_EXEMPT  [Pack Four Amendment Fifteen]  live
  Concrete nouns doing concrete things (hands shaking, a jaw setting, a tail going still) are not counted against the reification budget.

R4-15-CLERK_TEST  [Pack Four Amendment Fifteen]  live
  If the thing could appear as a line on a ledger, in a writ, or in a Bench finding, reify it freely; if it could not, it costs budget.

R4-15-CONCRETE_FIRST  [Pack Four Amendment Fifteen]  live
  Before reifying, check whether an object already in the room can carry the same freight; the object always wins.

R4-15-DENSITY_PROBLEM  [Pack Four Amendment Fifteen]  live
  Reification is a genuine Hermetic-register instrument and any single instance reads well; the failure is density — ten good instances in a scene leave nothing solid for the reader to stand on.

R4-15-LICENSED_CLASS  [Pack Four Amendment Fifteen]  live
  A debt, claim, verdict, name, standing, bearing, holding, writ, seal, title, warrant, attribution or tally is a closed-class WOTR abstraction the world already treats as a thing that moves between hands; reifying these is description, not device, and is unbudgeted and free.

R4-15-NEVER_AT_BEAT  [Pack Four Amendment Fifteen]  live
  Reification is atmosphere and a poor delivery vehicle for a turn; the value flips on a body or an object, never on a personified noun.

R4-15-ONE_PER_PARAGRAPH  [Pack Four Amendment Fifteen]  live
  Two unlicensed reifications in a single paragraph produces a bogged-down feeling independent of the scene total.

R4-15-PROCEDURAL_SCENE_BUDGET  [Pack Four Amendment Fifteen]  live
  In procedural or ledger scenes, the unlicensed reification budget tightens to one per page, since the Licensed Class is already doing that work there and unlicensed instances would go invisible against it.

R4-15-REIFICATION_DEFINED  [Pack Four Amendment Fifteen]  live
  Reification gives an abstract noun a physical verb, handled by characters as an object in the room; the tell is the verb, not the noun (hand, pass, set, carry, place, take, give, hold, put, return, offer, lift, drop, weigh, lay, arrive, land, sit, settle, drain).

R4-15-TWO_PER_SCENE_BUDGET  [Pack Four Amendment Fifteen]  live
  At most two unlicensed reifications per scene, of different abstractions; a third is a fail regardless of quality, and the same abstraction may be reified only once.

R4-15-WATCHLIST_NOUNS  [Pack Four Amendment Fifteen]  live
  Recurring reification offenders, kept greppable rather than felt: silence, weight, arithmetic, governance, permission, distance, authority, refusal, grief, history, patience, the question, the cost, the moment, the space between them.

R4-ADD-CHECK15  [Pack Four Addendum]  live
  Flags etymological, register and "which meant" constructions; warns rather than fails since the whose-vocabulary test cannot be automated, and every flag gets read.

R4-ADD-CHECK16  [Pack Four Addendum]  live
  Fails any chain of 3+ sentences over 25 words, 4+ flat runs, a short-sentence share under 10% (warns under 18%), and reports every paragraph closing long-long-long.

R4-ADD-CHECK17  [Pack Four Addendum]  live
  Fails at 3+ unlicensed reification instances or any paragraph carrying two; licensed instruments are detected, reported separately, and never counted against budget.

R3-7-COZBI_CRAFT_NOTE  [Pack Three Amendment Seven]  live
  An Expenditure fighter is boring to write badly and terrifying to write correctly; refuse the temptation to give him a spectacular exchange — the scene should feel like the opponent is winning, repeatedly, at increasing cost, until the arithmetic arrives.

R3-8-CAVALRY_FIELD_REGISTER_POV  [Pack Three Amendment Eight §14]  live
  A cavalry POV is the only ordinary soldier who can carry the Field Register honestly, since the rider both sees and moves; use for orientation when needed, aware of the cost paid in intimacy.

R3-8-CAVALRY_PURSUIT_FUNCTION  [Pack Three Amendment Eight §14]  live
  Per Section 6, pursuit is butchery of the unresisting from behind at a canter for as long as the horses last; the honest version does not let the cavalry POV enjoy it and does not let them refuse it either.

R3-8-NAVAL_FIRE_WATER_DEATHS  [Pack Three Amendment Eight §12]  live
  Naval death is written as fire and water, not the blade.

R3-8-NAVAL_SENSORY_HIERARCHY  [Pack Three Amendment Eight §12]  live
  At sea the sensory order runs sight, motion, sound, smell (versus land's sound, pressure, smell, sight), because a ship gives a horizon and takes away footing.

R3-8-NAVAL_SIGHT_HELPLESSNESS  [Pack Three Amendment Eight §12]  live
  A sailor's Field Register is available continuously and is rationed by what the character can do about what they see, not by what they can see; write the helplessness of watching rather than the confusion of not seeing.

R3-8-SIEGE_CLOSE_REGISTER_RESERVED  [Pack Three Amendment Eight §13]  live
  The Close Register is reserved for a sortie, a mine breaking through, and the storm; each arrives without warning and ends faster than the reader wants.

R3-8-SIEGE_LINE_REGISTER_DEFAULT  [Pack Three Amendment Eight §13]  live
  A siege is experienced as a unit condition (camp, food, flux, digging progress) rather than personal action; weeks pass in the Line Register at a paragraph each, correctly.

R3-8-SIEGE_PARLEY_IS_SCENE  [Pack Three Amendment Eight §13]  live
  Everything a siege is about happens in the negotiation, because both commanders know what a storm means; write the parley as the climax and the storm, if it comes, as the failure of the actual drama.

R3-8-SIEGE_TEDIUM_BY_SPECIFICITY  [Pack Three Amendment Eight §13]  live
  One precisely observed repeated detail carries a month — the same gap in the wall, seen from the same place, on a different day, with something small changed.

R3-9-BEFORE_AFTER_DURING  [Pack Three Amendment Nine]  live
  Before covers the costing-out arithmetic and the decision what to spend and on whom; after covers what the practitioner looks at on a field they made and whether they can name anyone; during, use the soldier, with the practitioner appearing only as weather the POV soldier experiences and doesn't understand.

R3-9-COSTED_OUT_EXCEPTION  [Pack Three Amendment Nine]  live
  The single exception to the practitioner-POV ruling: a practitioner who has been costed out inherits every section-1 constraint the moment their magazine empties, so a POV beginning able to see the whole battle and ending able to see twelve feet is the strongest use of the perspective available — spend it once.

R3-9-PRACTITIONER_POV_RULING  [Pack Three Amendment Nine]  live
  A high-Stage practitioner inside a battle experiences none of the constraints the guide is built on; handing the reader that POV mid-engagement dissolves the fog, pressure and helplessness every other section exists to construct, so the POV is open before and after an engagement and closed during it.

R2-5-ONE_PER_ENGAGEMENT  [Pack Two Amendment Five]  live
  One Single Act per engagement — two dilutes both, three is a soap opera in armour; a campaign's several engagements should not all involve the same pairing, or the reader begins to expect the shape.

R2-5-RESOLUTION_IN_AFTERMATH  [Pack Two Amendment Five]  live
  The relationship change is legible in how the two characters handle an unrelated later scene; if a character ever says what the act meant, the amendment has been violated and the scene has been spent.

R2-5-SINGLE_ACT_CONDITIONS  [Pack Two Amendment Five]  live
  The Single Act must be physical (a thing done with the body under load, not a decision or realisation), unrepeatable (the circumstance does not recur), witnessed but not discussed during the engagement, and ambiguous at the moment it happens to witness, reader and actor alike.

R2-5-SINGLE_ACT_RULE  [Pack Two Amendment Five]  live
  A battle cannot hold six relationships the way a duel holds one; a battle advances exactly one relationship, and it advances it by a single unrepeatable act.

R1-3-AFTERMATH_IS_WHERE_IT_HAPPENS  [Pack One Amendment Three]  live
  Whatever an engagement will do to characters' relationships happens in the three days afterward, over the burial detail and the arguments about who should have done what — the fight itself is too loud and too fast for anyone to change during it.

R1-3-FIVE_STAGE_AFTERMATH  [Pack One Amendment Three]  live
  Per the Mass Combat Craft Guide §7: the wounded left where they fell, the stripping, the late and cursory burial, the disease, and the district that does not recover in the season — any aftermath scene should touch at least two.

R1-3-NAME_THREE_RULE  [Pack One Amendment Three]  live
  The one-italic-thought-per-NPC standard is suspended in mass combat; no more than three characters carry interiority through a battle sequence, everyone else is exterior only, and interiority for named characters outside the three is deferred to the aftermath.

R1-3-PLAN_AFTERMATH_FIRST  [Pack One Amendment Three]  live
  When planning a battle scene, plan the aftermath first; the engagement exists to produce the conditions of the aftermath. If you cannot state what the aftermath scene is for before writing the battle, the battle has no reason to be in the book.

R1-3-SCENE_STANDARDS_DEFINED  [Pack One Amendment Three]  live
  The standing Scene Standards (minimum 2,500 words, layered sensory opening, one private italic thought per named NPC, no section spacers, end on physical action) apply in full to all scenes except mass combat sequences, where two provisions are amended.

R1-3-WORD_FLOOR_INCLUDES_AFTERMATH  [Pack One Amendment Three]  live
  The 2,500-word minimum applies to the engagement plus its aftermath treated as one unit, not the fighting alone; a battle that ends when the fighting ends has not met the standard regardless of length.
```

## Docket

`check_docket prose-law pov scene-structure dialogue register`:

```
-- 0 pending/proposed for ['dialogue', 'pov', 'prose-law', 'register', 'scene-structure']
```

Nothing pending or proposed for these tags; nothing changes what this chapter must do.

## Scene brief

`scene_brief` (thread Wystan Ashmore, type standard, culture Accord, cast Wystan Ashmore, Qiu Yinzhi), from "Fill before drafting" up to the loadout:

##### Fill before drafting (author notes)
1. POV: ____  (write from whoever knows least about what is coming, R5-C1-WRITE_FROM_LEAST_KNOWING; a default, breakable with reason)
2. This POV knows: ____ | wrongly believes: ____ | the reader knows that they do not: ____  (R5-C1-INFO_TRACKED_PER_POV)
3. Ignorance quota, one thing the POV notices and cannot interpret, unresolved this scene: ____  (R6-3-IGNORANCE_QUOTA)
4. Misreading, one confident inference that is wrong and stays wrong, well-reasoned: ____  (R6-4-MISREADING_BUDGET, R5-C1-WELL_REASONED_WRONG_CONCLUSION)
5. What it costs, specific and visible (reserve, body, debt, reputation, who saw): ____  (Table Rule 5; R12-1-PACK_SEVEN_SURVIVORS)
6. The lie: one thing an NPC says that is wrong and stays uncorrected (once per session): ____  (Table Rule 8)
7. Standing Inventory, two minimum (Accord): ____ and ____   (R6-9-RECURRENCE_RULE)
8. Ends on: ____  (physical action, an NPC line, or a thing he can now see; never a question at Isaac. Table Rule 1)
9. Length band: ____  (conversational 300–700 / standard 700–1,500 / set piece 2,500+; default the middle. Table Rule 2)

##### FOW lines (never invent a number)
##### Wystan Ashmore — Late Bell  (Volume I — Character Cards/Wystan Ashmore — Late Bell.md)
**Level 300.** Band III, Sovereign. **Stage X, Realization.** Spirit Path, recognised. No Body, Attraction or Fate alignment.
**Soul Crystal tier.** Sovereign Crystal. **State.** Refined, with one unconsolidated fracture (XVII).
**Aether Class.** VI, Voidic. Lateral, Limina-aligned; no loss figure is documented for laterals. His Shell subtracts rather than amplifies, which is why his own workings are nearly silent and why he can hear everyone else's.
**η.** ~0.74. Placed inside the documented Master band of 0.70 to 0.80. No source figure on his sheet.
###### IV. Primary Stats
Pool: 4,500 from leveling, 5,500 from Thresholds I through X. 10,000 total, all of it spent.
**Gnosis** 2,960 / mean 370 / **A** · **Resilience** 1,560 / mean 195 / B · **Harmonics** 1,480 / mean 185 / B · **Tempering** 1,280 / mean 160 / C · **Dominion** 1,160 / mean 166 / C · **Vitality** 760 / mean 95 / D · **Dexterity** 560 / mean 70 / D · **Ardency** 240 / mean 30 / E
###### XVI. Temperance Record
I through VII cleared young and without incident, the Crystal of someone who kept reading. **VIII, Transcendence:** resolving the contradiction between wanting the work to mean something and knowing it arrives too late by definition. **IX, Invocation:** the Realm consolidated, at Keld's bedside, which is not where the Division files it. **X, Realization:** the Continuum accommodated a law that says *nothing here is altered*, an event three Measurewrights have written papers about and he has not read.
**Why he is stalled at 300.** Not the gate; he cleared Stage X. The Crystal Adaptation Rule has classified his casework as Familiar and pays him a tenth, he fights nobody above tier because he fights nobody at all, and he has taken no soul-cost event in four years. A Master-tier practitioner earning experience at the rate of a clerk. He knows, and has made peace with it in a way that worries the two people who like him.

##### Qiu Yinzhi  (Volume I — Character Cards/Qiu Yinzhi.md)
**Level / Stage / Band.** Pending Isaac.
###### IV–V · Stats
Pending Isaac.
###### VI–VII · Force and Flow
###### VIII–IX · Traits and Domain
###### XVI · Temperance Record

## Previous chapter

Last ~1,430 words of `scenes/the_nights_watch.md` (author notes excluded), cut at a paragraph boundary. The chapter picks up the second she finishes writing.

*He is not asking to be kind. He is asking because he has hit the edge of himself and he does not mind saying so.*

"It would have to never be in contact with the hand that made it while it was live," she said. "Inert in the flask. Live in the animal. You would need the synthesis to hold at some threshold and only go over it in the presence of something the body supplies and the bench does not." She had picked the pen up without noticing. "Heat. Or pH. Or the blood. Blood is the obvious one."

"Cost."

"Enormous. Verdantia at any working dilution is metered draw and metered draw is a supply contract." She stopped with the pen down on the paper, and he watched her arrive at the second half of it, and he let her arrive. "Which is a purse."

"Which is mine." He took the book back. "That is Article Fifteen, that is the only jurisdiction this desk has, and it is the first honest reason I have had in four years to be awake at this hour."

He put the forceps down and started on the left glove.

"Master Wystan."

"I am aware of what I am doing."

"You are not aware that I know what it is." She had come round the corner of the bench without his hearing her, which said something about his Perception at four in the morning. "Anamnetic contact off a live residue. My master did it. Off a coil housing out of a foundry fire, against advice, and he was sixty-one and his Anchoring was a C and he spent the last eleven months of his life correcting people who called him by the wrong name and being right about half the time."

"My Anchoring is not a C."

"You have not told me what it is and you are not going to, because you have your whole Stage under suppression and you have been holding it since before I came up the stairs, and I can tell because my bracelet has been pulling toward you since the door." She said it without heat. "I am telling you that I have watched this. That is all. I am not going to stand in front of the bench."

"Good, because I would move you." He got the second glove off and laid them both across the day book, squared, because he liked things squared. "Nine hinds and a stag are dead in a cut in the north and four counties have the same thing and the Grand Mage's office has sent back the weather form. This is the only piece of it I can touch with my hands."

"Then count out loud," she said. "Afterward. Names, if you have them. My master's people made him do that."

He put his bare fingers on the wedge.

It arrived without warning and from the wrong direction, already in progress, like a door opening onto a room where people have been talking for an hour.

Cold in the feet first. Wet ground, and the particular ache of standing in a cut in the ninth hour of a northern morning, and the whole enormous architecture of a body he did not have, four-legged and wrong-jointed and heavy at the front. The light was different. It came in flat and wide and there was too much of it at the edges. He was aware of the others without looking at them, seven or eight, spread along the birch, and the awareness had a texture he had no word for and would not get one.

And underneath all of it, in the gut and the spine and running out along the ribs, something enormously good was happening.

That was the part.

It did not hurt. There was no alarm in it anywhere. Whatever had been introduced into her was making her feel the way an animal feels in the second week of spring, warm through the trunk, heavy and slow and entirely unafraid, and she had stopped walking twenty minutes ago because standing still was better and there had been no reason in the world to do anything else. Her legs had gone at some point. She had not noticed. She was standing because the hide held her up and she did not know the difference and she was, in the last measurable moment of her existence, content.

The ravens came into the birch. She heard them arrive.

They did not come down.

Wystan took his hand off the wedge and made it to the stone sink and was sick until there was nothing left, and then twice more after that, which was the part that hurt.

He stayed bent over the sink with both hands on the cold edge of it and the rain running down the glass eight inches from his face and waited for the grey to come back off the top of his vision. Yinzhi did not touch him and did not speak. The gutter ran. Somewhere off toward the river a bell went for the fourth division, and he counted it, and got five, and let it go.

"Forty-two," he said, when he could.

"What."

"You asked me to count out loud." He straightened up by degrees. His mouth tasted of vinegar and bile and, faintly and impossibly, of green. "I carry forty-one minutes belonging to other people. Now it is forty-two. Thirty-nine of them are men and women whose names are in my files and I could give you every one in order. One of them is my senior officer and he is alive. One of them I have never identified." He wiped his mouth on the back of his wrist. "And one of them is a hind in the North Ferriby cut who was not frightened, and did not suffer, and stood there being warm while her legs came apart under her, and I will have that for the rest of my life and it is the worst thing in the tin."

Yinzhi had gone the colour of the wall.

"It is a kindness," she said. "Whoever did it made it a kindness."

"It is a design." He came back to the bench, unsteady, and sat, and looked at the wedge. "Pain makes an animal run. A hind that runs dies a mile away in a thicket where nobody counts her. He needed them to stay where they were put, so he built it so that stopping felt good, and that is a man who thought about the problem for a long time before he mixed anything."

He wrote it down. The writing took a while.

"There is no hand in this," he said, mostly to the page. "There never was. He does not go near them. He cannot, because the moment his Lattice touches the live formulation it couples and it signs and this whole apparatus falls over, so whatever he is doing he is doing at a distance from the animal and probably at a distance from the ground. He is not walking that line. He has never walked that line." He underscored it twice. "Which means the answer is not in the cut. It is in the water, or the licks, or whatever those animals all put their mouths on, and then it is in the ledger of whoever paid for two myriads of Verdantia."

"And Tally."

"Tally counts deer and has no signature on anything and is of no interest to a man who has arranged never to be within a mile of his own work." He capped the ink. "Write to him tomorrow and tell him to keep walking his line and to measure anything he finds. I want a second dataset from the same observer."

Yinzhi looked at him for a moment longer than the sentence needed. Then she reached past him, took the lid, and seated it back on the tin.

"Wrong tin," Wystan said. "Fresh tin, and I want the wax struck with my brass, not the chapter's, because from tonight this is a Register exhibit and not a Society filing." He found the drawer with the blank forms in it and pulled one out and turned it face up on the bench in front of her. "And I need your full name for the head of the docket. Lineage, generation character and courtesy, in the hand you were taught, because if this ends in a hearing you are the assay and they will come for you first.

She took the pen off the bench and wrote it out.

## Cast

state.json has no facts about either cast member, so both get full cards.

### Wystan Ashmore

#### Wystan Ashmore — Late Bell  (Volume I — Character Cards/Wystan Ashmore — Late Bell.md)


#### Wystan Ashmore — Late Bell

*Guild Accord, Arbitration Division, Night Register. Officer of Attribution.*

###### I. Identity

**Name.** Wystan Ashmore. Northern register, chartered family, third son. The byname *Late Bell* is the Division's, not his.
**Standing.** Tier 6, Master. Title of address **Warden of Duty**. Nobody in the districts he works uses it.
**Level 300.** Band III, Sovereign. **Stage X, Realization.** Spirit Path, recognised. No Body, Attraction or Fate alignment.
**Service.** Eleven years on the desk, four of them after the demotion.
**Catalyst Event.** Nineteen, clerking assay tins in a Measurewright's roll-room. He opened a sealed tin without gloves and received the last minute of a man nine years dead, including the part where the man understood what was happening to him. Anamnesis found him before any instructor did. He filed the tin, went outside, was sick in the yard, then went back in and finished the shelf.
**Why nights.** The district mains go quiet after the eleventh division. An unlicensed draw is inaudible at noon and unmistakable at three. The Night Register exists for signal, not for atmosphere.

###### II. Soul Architecture

**Soul Crystal tier.** Sovereign Crystal. **State.** Refined, with one unconsolidated fracture (XVII).
**Aether Class.** VI, Voidic. Lateral, Limina-aligned; no loss figure is documented for laterals. His Shell subtracts rather than amplifies, which is why his own workings are nearly silent and why he can hear everyone else's.
**Essence Typology Family.** Limina.
**η.** ~0.74. Placed inside the documented Master band of 0.70 to 0.80. No source figure on his sheet.
**EU reserve.** Governed by Tempering Yield at 80, D-Grade. Low for his Stage by a wide margin. No numeric table exists in source for Band III reserves, so the sheet carries none.
**Domain tier.** Realm-consolidated, Stage IX to X band.

###### III. Wellspring Harmonizations

Three held, at shallow Depth. A professional choice, and also all his Attunement will carry.
**Anamnesis**, the Wellspring of Remembrance. Strengthens Retention, Analysis, Anchoring. His three peaks, in order.
**Nihiloth**, the Hollow Law. Strengthens Sovereignty, Persistence, Cognition. The law his Domain runs on, which removes rather than adds.
**Fixatio**, the Binding Flame. Strengthens Fortitude and Anchoring. What is held by Fixatio stays held, including a scene.
**Refused.** Vantabriel, offered twice by the Division. He will not carry a Wellspring that endures by remembering the lost, on the grounds that he already does that for a living.

###### IV. Primary Stats

Pool: 4,500 from leveling, 5,500 from Thresholds I through X. 10,000 total, all of it spent.
**Gnosis** 2,960 / mean 370 / **A** · **Resilience** 1,560 / mean 195 / B · **Harmonics** 1,480 / mean 185 / B · **Tempering** 1,280 / mean 160 / C · **Dominion** 1,160 / mean 166 / C · **Vitality** 760 / mean 95 / D · **Dexterity** 560 / mean 70 / D · **Ardency** 240 / mean 30 / E

###### V. Sub-Stat Peaks

**Gnosis.** Analysis 700 (SS) / Retention 620 (SS) / Perception 560 (SS) / Fluency 480 (S) / Cognition 320 (A) / Acuity 120 (C) / Forecast 80 (D) / Vigilance 80 (D)
**Resilience.** Anchoring 420 (S) / Integrity 260 (B) / Ward 240 (B) / Fortification 200 (B) / Persistence 190 (B) / Hardening 170 (C) / Oath 60 (D) / Continuity 20 (F)
**Harmonics.** Suppression 460 (S) / Stability 440 (S) / Empathy 160 (C) / Breadth 120 (C) / Attunement 100 (D) / Axis 100 (D) / Synergy 60 (D) / Projection 40 (E)
**Tempering.** Coherence 340 (A) / Clarity 300 (A) / Maturity 280 (A) / Ceiling 100 (D) / Capacity 100 (D) / Yield 80 (D) / Overflow 60 (D) / Longevity 20 (F)
**Dominion.** Sense 380 (A) / Gravity 300 (A) / Sovereignty 240 (B) / Command 80 (D) / Fate 80 (D) / Radius 60 (D) / Pressure 20 (F) / **Throne: not registered**
**Vitality.** Fortitude 160 (C) / Filtration 120 (C) / Absorption 100 (D) / Constitution 100 (D) / Hemostasis 100 (D) / Regeneration 100 (D) / Tolerance 60 (D) / Threshold 20 (F)
**Dexterity.** Finesse 140 (C) / Reflex 120 (C) / Economy 80 (D) / Celerity 60 (D) / Evasion 60 (D) / Feint 40 (E) / Sequence 40 (E) / Grapple 20 (F)
**Ardency.** Compression 60 (D) / Depth 60 (D) / Alacrity 40 (E) / Flux 20 (F) / Penetration 20 (F) / Density 20 (F) / Cascade 10 (Hollow) / Overchannel 10 (Hollow)
> **The shape of it.** Every entry sits under the Stage X ceiling of 725 and every Path gate is satisfied by Spirit alone. An assessor reads a modest Dominion, a D-Grade body, and a man who cannot meaningfully hurt anyone. The register is not lying. It has no column for a practitioner whose peak sits at SS in the three entries that decide whether a case closes.

###### VI. Physical Force

D-Grade band. Travel 150 to 340 m/s, reaction 15 to 40 ms, attack speed subsonic to transonic. He can react to a shot. He cannot outrun one, and the Division's field manual says so in the paragraph he wrote.

###### VII. Aether Flow

AU/s is Flux Density against η, and his Flux is 20. Output negligible; draw cost low for the same reason. Harmonics Stability 440 means he holds a clean read on contaminated ground, inside a hostile Domain, or in a district the Accord cut two hours ago.

###### VIII. Traits

**Low Ground.** Passive. His Shell rests at near-zero saturation, so free residue in a closed volume runs its gradient toward him without being called.
**The Quiet Man.** Suppression 460, held continuously, waking and sleeping. It tires him and he does not drop it. Six people alive know what Stage he is.
**Occupational Load.** Filtration 120 against eleven years of ingested residue. His hands shake in the mornings. It is in his file as a disciplinary observation.

###### IX. Domain — STAY


*[card capped at 6,000 characters]*

### Qiu Yinzhi

#### Qiu Yinzhi  (Volume I — Character Cards/Qiu Yinzhi.md)


#### Qiu Yinzhi

##### Qiu Yinzhi

*Night Watch Society, Timberline chapter. Coil-carrier. Scene-derived stub from The Night's Watch; everything not stated in that scene is pending Isaac.*

###### I · Identity

**Name.** Qiu Yinzhi. Lineage-hall register (Chinese stratum): surname Qiu. Generation character, given character and courtesy name not yet on the page; she writes the full form onto Wystan's docket at the close of the scene.
**Age.** Twenty-three. Capped eight months.
**Line.** Measurewright lineage; artificer's apprentice.
**Affiliation.** Night Watch Society, Timberline chapter, carrying coils. Arrives at Cutler Row on the Society's warrant, not the Bureau's. From the close of the scene: the assay of record on a Night Register exhibit.
**Level / Stage / Band.** Pending Isaac.
**Catalyst Event.** Pending Isaac.
**Standing loss.** Her master died two years before the scene, after anamnetic contact off a coil housing pulled from a foundry fire, taken against advice. He was sixty-one, his Anchoring was a C, and he spent his last eleven months correcting people who called him by the wrong name and being right about half the time.

###### II · Soul Architecture

Pending Isaac.

###### III · Work Architecture

Artificer's training out of a Measurewright line. Reads a wall with a coil, sweeps by Signature, Family and Category alignment, and runs gate-open sweeps. Wellspring harmonisations pending Isaac.

###### IV–V · Stats

Pending Isaac.

###### VI–VII · Force and Flow

Pending Isaac.

###### VIII–IX · Traits and Domain

Pending Isaac.

###### X · Techniques

None on the page.

###### XI · Spirit Axes

Her dead master (unnamed). Wystan Ashmore, from the night at Cutler Row onward; the nature of that tie is pending.

###### XII · Resistances

Pending Isaac.

###### XIII · Physical Description

Short, built solid through the shoulders in a way the current cut of coat was designed to hide and did not. Black hair oiled and pinned up off the neck in the double coil the Measurewright lineages wear, with plain iron pins rather than silver. Round face, broad at the cheek; fine dark speckling across nose and forehead from leaning too close to a forge bench too often. Heavy brows. A mouth held hard on purpose. Grey wool coat cut long and narrow to the knee in the season's fashion, tailored with a gap at the left wrist for the bracelet. Body areas below the shoulders (chest, waist, hips, thighs) pending Isaac.

###### XIV · Psychology

Sat five days on a clean return she believed she was not good enough to have read, and still came out in the rain to find the one man who might look. Came with two coils. Holds her hands steady on a bench and her jaw set in a conversation. Has watched anamnetic contact cost a man everything and will say so, then step aside rather than stand in front of the bench. Refusal, wound and conviction in the character-first sense: pending Isaac.

###### XV · Equipment

**Regulation bracelet.** Three brass bands wound with a fine grey wire carrying its own faint sheen, seated against the inside of the left wrist so the coil holds contact with the pulse. Two guild proof-marks on the outer band, one struck badly. Not a cheap device. It pulls toward a suppressed practitioner nearby. Her thumb works the badly struck mark when she is thinking.
**Coils.** At least two carried; one burned on the chapter assay, the spare burned or near-burned on Wystan's bench.
**Sample tin.** The Ferriby tin, Fixatio-anchored, now a Register exhibit under Wystan's brass.

###### XVI · Temperance Record

Pending Isaac.

###### XVII · Fracture Log

Pending Isaac.

---

*Source: The Night's Watch (scenes/the_nights_watch.md). Card created from scene text only; no numbers originated.*

### Voice fingerprints

`voice_fingerprints` lists 30 characters with eight or more attributed lines; **neither Wystan Ashmore nor Qiu Yinzhi appears in it** (too few attributed lines in the archive). Their voices come from the source scene (see Previous chapter) and the cards. R15-1: if their lines could be swapped and nobody noticed, the chapter failed.

## Recall

### scene_recall "Ferriby wedge exhibit chapter wax docket edges Brack classification day desk"

##### The Night's Watch  (the_nights_watch.md, score 95)
[THE THING WITH EDGES] Four counties. That was the part the day-desk kept saying as though it settled the matter rather than opened it. Ferriby in the north, the Swale walks, two chapters out of the eastern timber towns, and one filing from a Society man in the Marches who had sent a sketch instead of a count and whose sketch Wystan had pinn...
[THE THING WITH EDGES] The Lattice Classification Bureau had already had it. Edwyn Brack, whose signature was on half the classifications out of the northern office and who had never in Wystan's experience been wrong in a way that mattered, had returned it inside two days as **Wellspring bleed, Verdantia, tertiary expression, no operator ind...
...bundle of nine and it was the only one he had read twice.  *Filed 14th, Tally, N., Timberline chapter, North Ferriby walk.* The Night Watch Society printed its inserts on the cheapest rag it could buy and the ink bled into the...
...ery week and counted deer for a living. His insert said that on the morning of the ninth he had come down the Ferriby cut and found eleven hinds and a stag inside a quarter mile, all of them dead where they stood rather than wh...

##### Commencement of The Curia. [ Kujo Arc ]  (commencement_of_the_curia_kujo_arc.md, score 44)
[Commencement of The Curia. [ Kujo Arc ]] He had read the taxonomy in a warm room in Altherion and had signed the appendix. Void constructs, assembled and never born, and the assembly is the whole of them: a working folded into a shape, and the shape does the work, and the material it is folded out of is ordinary and inert and could be anything. And a fold can...
[Commencement of The Curia. [ Kujo Arc ]] They were not lighting anything. That was the tell and Darius had it in under a second: an object under a light of that intensity throws a shadow, and nothing in that street was throwing one, because the blooms were not photons and had never been. They were Attraction Force presenting at a wavelength the eye had decide...
...had been the mouth, on the second day, when somebody upstairs still believed this would take an afternoon: a wedge between the back teeth and a pair of drawing pliers, and four molars out of the lower jaw before Sesk arrived...
...“You assumed traffic had one destination.”  Then Kujo selected one.  His left forearm stopped being merely a wedge and became a short horizontal elbow driven across the inside line of Darius’s upper arm, aimed where concentr...

##### WAR OF THE REALMS  (WOTR_Vaeloris_Sequence.md, score 42)
[The Cabin, IV: The Eleven Words] "The instrument." He said it evenly. "That is the part I will not soften. It is not soldiers. Enforcement has a Sealwright detachment and a warded perimeter, and the closure is a sealing operation. They intend to complete the boundary glyph around the marches and then withdraw the authorization glyph from everything st...
[The Witness Schedule] "You are looking at the wrong document and you have been looking at it for six days, and I would not have seen it either if I had spent those six days learning Zettari metaphysics from a sovereign, so do not make that face." She turned the file round and held it flat against the parapet with the heel of her hand and th...
...hold. Verinus had been looking at it for six days and could not have described it to a painter. It occupied a wedge of sky and sea perhaps two fingers wide at arm's length and it did not flicker, did not pulse, did not resolv...
...the doors at the seaward end and the light came in flat and low across forty trestles and made a long bright wedge on the boards, and in the wedge a Zettari dresser was picking through a basket of boiled linen with the delib...

##### The_Path_of_Sorrow  (The_Path_of_Sorrow.md, score 37)
[The_Path_of_Sorrow] The brush moved again. Heavier this time. Closer. The Kamigan read the displacement pattern — the way the branches moved, the timing of the movement, the weight distribution implied by the angle of deflection — and constructed a silhouette: quadrupedal, approximately 400 kilograms, low-slung through the shoulders, wide...
[The_Path_of_Sorrow] *So why. Why keep breathing. Why keep ranking. Why keep the Kamigan running when the Kamigan reads nothing worth reading and ranks nothing worth ranking and the verdicts it produces land on targets that do not change the world's fundamental architecture. Emira. Emira is why. Emira is the only ranking that returns a non...
...dream because you have been reading tactical manuals since you were six and tactical manuals do not contain a chapter on trust. They contain chapters on walls. Walls are easier to draw. Trust is harder to build and impossible t...
...ding tactical manuals since you were six and tactical manuals do not contain a chapter on trust. They contain chapters on walls. Walls are easier to draw. Trust is harder to build and impossible to diagram and it does not photo...

##### Punta  (22_darius_punta.md, score 34)
[Rulings] **Research consulted, per §7.** Floating rib anatomy and the absent anterior attachment. Olecranon as striking surface. Co-contraction reducing net force output and slowing initiation. Over-under clinch mechanics and hip denial via the underhook. Descending diagonal elbow. Repetition into a single location and soft-tis...
[The punta] **The elbow.** *Sok chieng*, the descending diagonal, thrown when the hand is already committed and useless. The olecranon is a lever arm ending in a bone spur with no soft tissue over it — the hardest striking surface a body owns. Into the gap over the floating ribs, which exists because a frame that bends has to leav...

##### The Imperceptible District  (07_charles_the_imperceptible_district.md, score 33)
[Notes (author-facing, not canon)] **Which is why they gave it to the emptiest man in the building.** A practitioner is a man the register holds a great deal of information about, and this working destroys information, so a practitioner would come apart before the second line. Charles is at the bottom of the Accord's file with no output and no faculty, ...
[Notes (author-facing, not canon)] **Research consulted, per §7.** Decoherence and einselection: environmental monitoring destroying interference between alternatives, redundant records in the environment as the reason outcomes are definite, and the pointer basis as what survives the process. Everything else from standing knowledge and flagged as such. ...

##### The Undamped Thing  (09_dabney_the_undamped_thing.md, score 32)
[The Undamped Thing] *A keel north of the Sound. The ash at Sum-gol. The same hour.* ---
[I] A practitioner is a damped instrument. Sixteen Stages of Temperance exist to put resistance into the line, so that what comes out of a soul comes out at a rate the body chose and stops when the body stops driving it. Every hour of training any Moto or any Mahuo or any Court practitioner has ever done is the installatio...

##### The Muster, the Breach, and the Road North  (01_wotr_muster_breach_road_north.md, score 32)
[Notes (author-facing, not canon)] **Open.** Whether Bram's line holds past the ninth hour. Which two of the three false reports the Seat believed. Whether Edward comes back in five days. What is doing the work on the western horizon, since it is ahead of the column and nobody in the column will look at it.
[Notes (author-facing, not canon)] **Mass Combat Guide is in force for section II.** Sensory hierarchy inverted to sound, pressure, smell, sight. Bram never knows how the battle is going: he sees thirty feet, hears Renard on his left, and has no information about his right for eleven minutes that he experiences as either a moment or an afternoon. Three ...

### scene_recall "Wystan Ashmore Qiu Yinzhi Cutler Row Night Register scullery day desk"

##### The Night's Watch  (the_nights_watch.md, score 96)
[Author notes] Isaac's scene, archived as delivered. Three movements: The Thing With Edges (Wystan, Night Register, Cutler Row), What Does Not Smell Dead (Vesk POV, Malphas's cell at the Greyshaft Nine coldhouse; Project Zombification named), Forty-Two (Yinzhi's sub-floor sweep, the hind signature, Wystan's anamnetic contact). New na...
[FORTY-TWO] She broke the wax with her thumbnail and did it badly, in four pieces, and two of them went on the floor. "Leave them," Wystan said. "They are chapter wax and I will want them later. The back room." The back room at Cutler Row had been a scullery before the Division took the building and it still had the drain in the f...
...Row had been off since the eleventh division, and the silence it left had a shape to it. Eleven years in and Wystan still heard the absence as a pressure behind the ears, the way a man who works beside a mill hears the mill s...
...ibre, so a man reading one at the third hour by a single lamp did it with his nose eight inches off the page. Wystan had a scholar's slouch and no scholar's title, whatever the Division put on his door.  Tally walked forty mil...

##### The True King of the North, Part 4  (the_true_king_of_the_north_part_4.md, score 44)
[The True King of the North, Part 4] Ashmore arrived during the exchange, because Ashmore always arrived during someone else's exchange, not from rudeness but from the specific habit of a lord whose power was logistical rather than martial and who understood that the best position in any room was the position adjacent to the conversation that was already ...
[The True King of the North, Part 4] The study was small. Muken had designed it small, the way he had designed everything in Kharven-Seat, with the specific economy of a man who understood that luxury in a cold climate was a vulnerability, because luxury required maintenance and maintenance required resources and resources in the north were the difference...
...bearing nothing, because nothing was the load that preceded collapse, and the Shieldwarden did not collapse.  Ashmore arrived during the exchange, because Ashmore always arrived during someone else's exchange, not from rudeness...
...that preceded collapse, and the Shieldwarden did not collapse.  Ashmore arrived during the exchange, because Ashmore always arrived during someone else's exchange, not from rudeness but from the specific habit of a lord whose...

##### The True King of the North, Part 5  (the_true_king_of_the_north_part_5.md, score 43)
[Author notes] Isaac's manuscript, archived as delivered. Part 5 of 22: Edric Ashmore and Godfrey on grain; Keld and Thornwall in quiet talk; Hallenfeld late; Muken tells Godfrey of the grandchild; Revari and Zuberi enter and greet Muken; the hobgoblin report; Muken tells Revari; Azure Tenrai Moto at the edge of the conversation. Str...
[The True King of the North, Part 5] Edric Ashmore was a different architecture than Godfrey entirely. Where Godfrey was stone, Edric was ledger. A man of middle height and narrow build, clean-shaven, soft-handed, wearing a coat of dark green wool that was the best-made garment in the hall by a margin that was visible to anyone with eyes and that Edric ne...
...ms left as written, pending Isaac: Kokan (without macron). Continuity to check: Edric Ashmore's house against Wystan Ashmore's card (northern register, chartered family)....
...# The True King of the North, Part 5  Edric Ashmore was a different architecture than Godfrey entirely. Where Godfrey was stone, Edric was ledger. A man of middl...

##### The True King of the North, Part 13  (the_true_king_of_the_north_part_13.md, score 42)
[The True King of the North, Part 13] The Ashmore man was brought through the throne room doors with frost in his hair and chains on his wrists and the specific expression of a man who had been dragged rather than escorted, the expression that occurred when the muscles of the face were arranged by indignity rather than by composure, and the indignity was t...
[The True King of the North, Part 13] Pietro Ashmore walked the length of the throne room with the chains pulling at his wrists and the smirk pulling at his mouth, and the smirk was the thing that the room saw before it saw anything else, because the smirk was the weapon, the specific social instrument that men like Pietro Ashmore used when the men like Pi...
...different and the two sounds were the same and the same was the family and the family was walking north.  The Ashmore man was brought through the throne room doors with frost in his hair and chains on his wrists and the specifi...
...that the rebuilding had not yet sealed. A different cold. A cold that had arrived three seconds ago, when the Ashmore man had been pushed through the doors, and that had settled into the stone and the air and the ironwood beams...

##### The Revolution Of The Inner World  (the_revolution_of_the_inner_world.md, score 42)
[The Revolution Of The Inner World] The extraction schedule is the kingdom's sovereign instrument. Everything else is administration. Nobody on that platform said the words *extraction schedule* all morning, and the Ore Council went back down to the Council floor at the ninth hour and set the next quarter's quotas at the number they had already agreed on...
[The Revolution Of The Inner World] The Tinker Goblin quarter of Thane-Gorr had been petitioning the Ore Council for a guild seat for two hundred and six years. They maintained every shaft-lift, every chain-bridge winch, every pump-array gasket and every ventilation fan in the crater. They were not a chartered guild, so they were not represented, so thei...
...oing back to the horses. Three killed by their own kin, entered in a book. Two hundred and ten feet at the narrows, counted in summer under a false name with a cart of salt fish, drawn on the back of a psalter.  The smile a...
...toward a tool that was not there, and both palms the specific slick shine of skin that has been burned and regrown often enough to stop having a print.  She wore a Transport Guild under-coat with the Transport Guild badge c...

##### The True King of the North, Part 16  (the_true_king_of_the_north_part_16.md, score 41)
[The True King of the North, Part 16] Five words. Delivered in the register that was neither the Sword Princess's iron nor the child's smallness but the third register, the register that lived between the two, the register that governance produced in the people who performed it honestly, which was: uncertainty spoken without weakness. The uncertainty was h...
[The True King of the North, Part 16] The correction was the plan. The plan was the architecture. The architecture was inside Kharven-Seat, and the inside was the specific position that Seiji's assets occupied, placed there by Seiji's design over years of patient cultivation, each asset positioned the way a siege engineer positioned charges, inside the wal...
...be calibrated to, and the counter-measure was the thing inside the vial.  The vial was Valdís's work.  Valdís Ashmore. The name was a northern name worn over a function that was not northern. Valdís had arrived in Kharven-Seat...
...ve produced the investigation, and the investigation would have produced the truth, and the truth was: Valdís Ashmore was not an Ashmore. Valdís was the daughter of a Tenrai alchemist whose training had been conducted by Azure...

##### A Silence in the Chord  (00_SUPERSEDED_wrong_names.md, score 34)
[IV. THE ASHKEWE PARLEY] She took Onawa's head eleven days later at Greysalt. Sylvenn Thaeren was not there and read the depositions afterward, all sixty of them, twice, and reads them still. Onawa Ashkewe, Queen of the Tsohanto, She Who Wears the Old Faces, came to Greysalt under parley on the ninth day of the withheld season with a household...
[VI. THE WINDOW] Sylvenn Thaeren, second jurist of Velthaeir, thirty-one years in the office and eleven contour-crimes entered in his hand on the eleventh day of the withheld season, walked back up through the Vaelmarr terraces after the head came off at Greysalt, and stopped where he had stood, and looked at the mark his rail-case had...

##### Nine Hours of Daylight  (nine_hours_of_daylight.md, score 33)
[VI. THE PLATE] "Two reasons, and you should hear both. The first is that no other corps in the four quarters takes a comparable reading and impressions are worth nothing, which is your point and it is correct. The second is that if there is a hand inside Velthaeir, then a Measurewright with a plate out on my frontier taking baselines...
[VI. THE PLATE] "Same method, not impressions. Agreed, and I can give you the method. "Neyra Corvenn of Velthaeir, eleven hundred miles from home, currently at Vaelmarr with a brass plate she has levelled on a dock, on a barge in a swell, and twice inside a dead pocket in the Reach where the needle went flat and stayed flat. She is th...

### wiki Ferriby

##### Nol Tally  (Volume I — Character Cards/Nol Tally.md, score 98)
[XIV · Psychology] The sort of man who measures. On the ninth he found eleven hinds and a stag dead where they stood inside a quarter mile of the Ferriby cut, measured the grey-green mass to nine inches at the tallest, and cut a section with his knife. On the tenth he walked the line north to the Ferriby stones and checked the clean grou...
[Nol Tally] *Night Watch Society, Timberline chapter, North Ferriby walk. Forester and deer-counter. Scene-derived stub from The Night's Watch; everything not stated in that scene is pending Isaac.*
...# Nol Tally  ## Nol Tally  *Night Watch Society, Timberline chapter, North Ferriby walk. Forester and deer-counter. Scene-derived stub from The Night's Watch; everything not stated in that sce...
...mber every week and counts deer for a living. **Affiliation.** Night Watch Society, Timberline chapter, North Ferriby walk. **Level / Stage / Band.** Pending Isaac. Wystan's read: no signature on anything, of no interest to the...

##### Ilmar Foss  (Volume I — Character Cards/Ilmar Foss.md, score 67)
[III · Work Architecture] Coil and instrument work. Understands attribution practice from the inside. He is the one who states why the Ferriby residue reads clean: nothing in the cell ever couples, and the deer's own Lattice runs the working and signs it. Wellspring harmonisations pending Isaac.
[XVII · Fracture Log] Pending Isaac. --- *Source: The Night's Watch (scenes/the_nights_watch.md).*

##### Edwyn Brack  (Volume I — Character Cards/Edwyn Brack.md, score 66)
[XIV · Psychology] In Wystan's experience he has never been wrong in a way that mattered. He returned the Ferriby insert inside two days as *Wellspring bleed, Verdantia, tertiary expression, no operator indicated*, attributed it to a vein surfacing through a drift-geology fault that would exhaust by autumn, and recommended no further act...
[XVII · Fracture Log] Pending Isaac. --- *Source: The Night's Watch (scenes/the_nights_watch.md).*
...### XIV · Psychology  In Wystan's experience he has never been wrong in a way that mattered. He returned the Ferriby insert inside two days as *Wellspring bleed, Verdantia, tertiary expression, no operator indicated*, attribut...

##### The Iron Tree  (Spellcraft/The Iron Tree.md, score 38)
[The Iron Tree] ---
[FOW line] Governing Primary Vitality and Resilience; Sub-Stats Vitality Fortitude, Resilience Anchoring and Hardening, Ardency Compression, Tempering Compression, per the ratified Iron Bison discipline's own stat effects. Stage floor VII (preliminary), IX (sustained), XII (indefinite maintenance); Dougou's personal apex sits at ...

##### Kaelrith Dorne · The Iron Wound  (Volume I — Character Cards/Kaelrith Dorne · The Iron Wound.md, score 36)
[IX · Relationships] **The Enforcement Division** · Deserter. Occasional consultant during Concord clean-ups. **The insignia is still on the mantle, inside-out.** **Seren Valenne, the Grey Adjudicator** · **Unofficial reports claim Seren invoked his aid during the Arbitration of Anguz. Neither spoke to the other throughout the trial, and b...
[Affiliation] ---

##### Aberrations  (The Bestiary/Aberrations.md, score 35)
[Bicorn] ---
[Hellhound] ---


---- full text of Nol Tally ----

#### Nol Tally

##### Nol Tally

*Night Watch Society, Timberline chapter, North Ferriby walk. Forester and deer-counter. Scene-derived stub from The Night's Watch; everything not stated in that scene is pending Isaac.*

###### I · Identity

**Name.** Nol Tally, filed as *Tally, N.* Northern stratum. Whether Tally is a frozen surname or a live byname from the counting is pending Isaac.
**Occupation.** Walks forty miles of timber every week and counts deer for a living.
**Affiliation.** Night Watch Society, Timberline chapter, North Ferriby walk.
**Level / Stage / Band.** Pending Isaac. Wystan's read: no signature on anything, of no interest to the man behind the Ferriby deaths.
**Catalyst Event.** Pending Isaac.

###### II · Soul Architecture

Pending Isaac.

###### III · Work Architecture

None indicated.

###### IV–V · Stats

Pending Isaac.

###### VI–VII · Force and Flow

Pending Isaac.

###### VIII–IX · Traits and Domain

Pending Isaac.

###### X · Techniques

None.

###### XI · Spirit Axes

Pending Isaac.

###### XII · Resistances

Pending Isaac.

###### XIII · Physical Description

Not yet on the page. Full inventory pending his first appearance.

###### XIV · Psychology

The sort of man who measures. On the ninth he found eleven hinds and a stag dead where they stood inside a quarter mile of the Ferriby cut, measured the grey-green mass to nine inches at the tallest, and cut a section with his knife. On the tenth he walked the line north to the Ferriby stones and checked the clean ground on the far side of the parish marker twice. Noted the four ravens that would not come down. Filed his insert on the fourteenth in person at the bulletin office, which he had never done, and asked what happens to a filing after the Bureau closes it, and whether the Night Register was a person. Has not walked his line since the eleventh.

###### XV · Equipment

A knife and a rule. Pending Isaac beyond that.

###### XVI · Temperance Record

Pending Isaac.

###### XVII · Fracture Log

Pending Isaac.

---

*Source: The Night's Watch (scenes/the_nights_watch.md). Known by name to Malphas's cell. Wystan has asked for a second dataset from him.*

### wiki Brack

##### Edwyn Brack  (Volume I — Character Cards/Edwyn Brack.md, score 101)
[XV · Equipment] Pending Isaac.
[IV–V · Stats] Pending Isaac.
...# Edwyn Brack  ## Edwyn Brack  *Lattice Classification Bureau, northern office. Classifier. Scene-derived stub from The Nig...
...# Edwyn Brack  ## Edwyn Brack  *Lattice Classification Bureau, northern office. Classifier. Scene-derived stub from The Night's Watch; ever...

##### II. Grades, Gates and Thresholds (Parts Four–Ten)  (Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md, score 36)
..., Gates and Thresholds (Parts Four–Ten)  ### Part Four — The Tier Grade System  Tier Grade is the qualitative bracket that determines what scale of force, phenomenon, or entity a practitioner can meaningfully engage, resist,...
...my. Because the ceiling sits on the Sub-Stat, a character's Sub-Stats and their Primary Grade sit in the same bracket. A B-Grade practitioner has broadly B-Grade stats. Spread shows what they are good at. It does not move the...

##### Nuvalik  (Volume I — Character Cards/Nuvalik.md, score 35)
[XV · Equipment] Butchering knife; the hook.
[Nuvalik] *Malphas's cell, Greyshaft Nine coldhouse. Butcher and anatomist of the ferment. Scene-derived stub from The Night's Watch; everything not stated in that scene is pending Isaac.*

##### Hide, Horn and Bone  (Materials, Alchemy & Trade/Hide, Horn and Bone.md, score 35)
[Hide, Horn and Bone] ---
[Horn, Claw, Bone and Shell] ---

##### Soren the Mast — The Climb  (Volume I — Character Cards/Soren the Mast — The Climb.md, score 34)
[Soren the Mast — The Climb] *The Climb · Always in the Rigging* > **Full Name:** Soren the Mast > **Age:** 27 · **Origin:** Concord > **Level:** 42 · **Stage:** I Ignition · **Band:** I > **Role:** Rigger, lookout, forward reconnaissance for the Kokan expedition > The climbing IS the oath. The oath IS the climbing. ---
[Soren the Mast — The Climb] > *Soren is not often on the ground. The ground is the place he visits between climbs.*

##### Gonju · The Sage  (Volume I — Character Cards/Gonju · The Sage.md, score 34)
[X · Relationships] **Ascella "Wick" Morwyn** · **Professional respect.** *Her Stillflame pairs with his Bitter Bloom to cleanse Rot seams without panic.* > **Codex** · Vitalia / Biochemistry / Verdantia primary / Stage IV.
[VII · Companion — Mallow] **Young brown bear.** *Bond: Animatria Beast Pact via Honey Truce.* **Sniffs out Rot seams** · **supports wounded bodies during cleansing** · **blocks miasmic gusts with mass** · *provides percussion for Green Lung Draft.* **Quirk** · **Loves daisies and flatbread, and only shares with the penitent.** ---


---- full text of Edwyn Brack ----

#### Edwyn Brack

##### Edwyn Brack

*Lattice Classification Bureau, northern office. Classifier. Scene-derived stub from The Night's Watch; everything not stated in that scene is pending Isaac.*

###### I · Identity

**Name.** Edwyn Brack. Northern stratum.
**Affiliation.** Lattice Classification Bureau, northern office. His signature is on half the classifications that come out of it.
**Level / Stage / Band.** Pending Isaac.
**Catalyst Event.** Pending Isaac.

###### II · Soul Architecture

Pending Isaac.

###### III · Work Architecture

Pending Isaac.

###### IV–V · Stats

Pending Isaac.

###### VI–VII · Force and Flow

Pending Isaac.

###### VIII–IX · Traits and Domain

Pending Isaac.

###### X · Techniques

None on the page.

###### XI · Spirit Axes

Pending Isaac.

###### XII · Resistances

Pending Isaac.

###### XIII · Physical Description

Not yet on the page. Full inventory pending his first appearance.

###### XIV · Psychology

In Wystan's experience he has never been wrong in a way that mattered. He returned the Ferriby insert inside two days as *Wellspring bleed, Verdantia, tertiary expression, no operator indicated*, attributed it to a vein surfacing through a drift-geology fault that would exhaust by autumn, and recommended no further action and no file. Wystan's verdict after the assay: not a fool, not corrupt, and correct off a true measurement. The classification is exactly what Malphas's method is built to produce.

###### XV · Equipment

Pending Isaac.

###### XVI · Temperance Record

Pending Isaac.

###### XVII · Fracture Log

Pending Isaac.

---

*Source: The Night's Watch (scenes/the_nights_watch.md).*

## Continuity

### Facts (state.json)

None yet. state.json holds no facts (this is the first chapter); no lies recorded.

### Prior chapter summaries

None; this is chapter 1. The prior text is the source scene, *The Night's Watch* (see Previous chapter).

### Hook agenda

- **Due within 3 chapters (ch1–4), planted or advanced:** none. All 32 hooks in state.json are status `planned`; nothing has been planted yet. This chapter plants eight (listed under The beat).
- **Overdue:** none.
- **Nearest due among this chapter's plants:** H01-far-side-of-the-marker (due ch7), H23-edges-in-the-margin (due ch16).
