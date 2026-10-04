"""Adversarial revision of draft-2.json (sections CO and ME) into group-2.json.
Run: bash build/py.sh imports/drafts/intimacy-questionnaire/work/revise_group2.py"""
import copy
import json
import pathlib

HERE = pathlib.Path(__file__).parent
d = json.loads((HERE / "draft-2.json").read_text())
Q = {q["id"]: q for s in d["sections"] for q in s["questions"]}


def opt(q, key):
    return next(o for o in Q[q]["options"] if o["key"] == key)


# ---------- section intros
co, me = d["sections"]
co["intro"] = ("How people court, marry, keep, lose and grieve each other, culture by culture, and what love costs "
               "across a Stage gap. The explicit register is settled law (R49-51, R70-133, R70-134); the Ledger, "
               "workings on desire and the coerced body are asked in the first group (K5, SC8, SC9).")

# ---------- CO1: C becomes a real keep-current option; misquote of R70-45 fixed
Q["CO1"]["context"] = ("R70-45 owes every Inventory fields for 'law and punishment' and 'succession' (R60-21), but none "
                       "holds courtship, marriage or widowhood, and no Inventory has a wedding, a bride-price or a word for "
                       "a lover. R70-134 says the lover's culture 'shows in what they do and say', which needs custom on "
                       "file to show.")
Q["CO1"]["options"][2] = {
    "key": "C", "label": "Inside the owed fields",
    "consequence": "No new field. Marriage law goes in R70-45's law and succession fields and a wedding in its festival "
                   "field, written as performed; courtship rides on those and on each scene's notes."}
Q["CO1"]["rec_reason"] = ("R70-134 keys a lover's conduct to culture, and conduct needs a shame line as much as a vow; a "
                          "field of its own is what Natalie loads before a scene, where C scatters custom across three.")
Q["CO1"]["rules_touched"] = ["R70-45-NEW_STANDING_INVENTORY_FIELDS", "R60-21-SUCCESSION_BY_CULTURE",
                             "R70-134-KEYED_CULTURE_FREE"]

# ---------- CO2: adulthood made plain in every sample
opt("CO2", "A")["sample"] = (
    "Halvar had split for Gunnhild's house since the first snow, and nobody had asked him to. Every third day her stack "
    "stood higher, and every third day the old woman said nothing about it. In the Thin Weeks he came in, stamped the "
    "frost off his boots and stood by the fire. \"How's your stack?\" he said. \"Full,\" said Gunnhild. \"Somebody's been "
    "at it.\" Her daughter Sigrun, three winters a widow, ladled the broth and put her own bowl in his hands. The word he "
    "gave her that night was only as strong as he was.")
opt("CO2", "B")["sample"] = (
    "Halvar came in the Thin Weeks with frost in his beard and stood just inside the door, which was as far as a man got "
    "before he was offered anything. Gunnhild looked at him a long while. Then she took the sealskin from its peg and "
    "unstoppered it, and the hut filled with the sour smell of the skin. She handed it to her widowed daughter. Sigrun "
    "drank, wiped the mouth with her thumb and held it out across the fire, and Halvar drank after her with the whole "
    "hearth watching.")
opt("CO2", "C")["sample"] = (
    "On the nameless day Halvar rode to Gunnhild's door with a led horse, and her widowed daughter Sigrun came out in her "
    "hide-coat and got up on it. Nothing bound on that day, so nothing was broken. On the first named morning Gunnhild "
    "walked to his father's fire and named the price: two skins of seal fat, a salt bar, and a winter of splitting. His "
    "father paid it in front of the headman. Whether Sigrun had gone willing was hers to tell, and over the years she "
    "told it two ways.")
Q["CO2"]["rules_touched"] = ["R70-134-KEYED_CULTURE_FREE", "R53-15-FOLK_BELIEFS", "R70-48-MONEY_PRICE_PROVENANCE",
                             "R53-11-JUSTICE"]

# ---------- CO2: Fusi Va glossed
Q["CO2"]["context"] = ("The Fusi Vā (the Queen's binding under clan oaths) is gone, so a northern word is 'only as strong "
                       "as the man who says it'. Canon gives labour-debt, meat-sharing, the skin (fermented milk in "
                       "sealskin; refusing it insults the host) and the nameless day, when 'nothing binds'. Steppe peoples "
                       "on Earth used bride-price and, some, bride-capture. No Kharven courtship is on file.")

# ---------- CO3: Muken's approval added; honorific use fixed by POV (R70-118); 'by the scale' fixed
Q["CO3"]["context"] = ("Moto canon: a thing that matters is 'asked in form, in the old register' and 'entered' in the "
                       "family's own hand, and Muken signed the approval for a match. Clansmen keep their eyes off a "
                       "Moto's because the Moto read through the eyes (a folk belief, R53-15). R70-110 already gives the "
                       "court verse at rites, and R70-133 the poem after the night.")
opt("CO3", "B")["sample"] = (
    "His letter came before the court was swept, folded small, with a sprig of larch through the knot and three lines in "
    "a soldier's square hand. Sayo read it once and laid it face down on the lacquer, and all morning it lay there. A "
    "quick answer would tell the household too much. A slow one would tell him. At the hinge of the day she took the "
    "brush, wrote her three lines beneath his last, and sent it back by the same runner before the bread.")
opt("CO3", "C")["sample"] = (
    "Every retainer at the Seat kept his eyes below the line's, and for a year Masatoki had kept his on Sayo-sama's "
    "collar. This morning, while the scale's beam settled over the ration, he lifted them and let them stay. The outer "
    "ring of her iris flared once. He held still under it and could not tell how far down she went. Neither of them "
    "spoke. When she looked away she said his name and nothing after it, and he understood that she had gone in only as "
    "far as that.")
Q["CO3"]["rec_reason"] = ("The register and the read through the eyes are the Moto's own canon objects; letters would "
                          "double R70-133's poem after and the court verse R70-110 already gives the house.")
Q["CO3"]["rules_touched"] = ["R53-15-FOLK_BELIEFS", "R70-110-VERSE_EXCHANGED_TALK",
                             "R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL", "R70-118-HONORIFICS_NARRATION",
                             "R23-2-JAPONIC_STRATUM"]

# ---------- CO4: Accord canon (Ita spondeo, the almanac) replaces 'only courtship canon'; no jury, no Board seal
Q["CO4"]["context"] = ("The Accord is the Victorian-Edwardian city (R59-07), money and paper on every page (R70-48). Its "
                       "canon has the almanac's marrying days, 'Ita spondeo' (thus I pledge) and 'Sine sigillo' (without "
                       "seal) for a bastard. Victorian England married by settlement (a contract fixing the wife's "
                       "property), courted by calls under a chaperone, and let a jilted party sue for breach of promise.")
opt("CO4", "A")["consequence"] = ("A match is a settlement drawn by an advocate, pledged 'Ita spondeo' and entered in ink, "
                                  "with what stays in her name written in. Courtship is the negotiation, and love shows "
                                  "in the clauses.")
opt("CO4", "A")["sample"] = (
    "Abel Tobin got his answer in Mrs Crane's front parlour, and it came on foolscap. Mr Pruett of Pruett and Vole had "
    "drawn the settlement overnight. Lettice's draw-licence stayed in her own name, and so did the lease on the upper "
    "room, and the clause said so twice. Tobin read it through with his hat on his knee while Lettice watched him read. "
    "At the foot stood Ita spondeo, a space for the attesting clerk's seal and a space beside it for his hand, and the "
    "ink on the stand was fresh.")
opt("CO4", "C")["consequence"] = ("A broken engagement is actionable at the Assize: the letters are read aloud in open "
                                  "court and the Bench prices the jilt. Every love letter in the Accord is also evidence.")
opt("CO4", "C")["sample"] = (
    "Abel Tobin got his answer in Mrs Crane's front parlour, in writing, because Lettice had been told to give it no "
    "other way. Every letter he had sent her lay on the table in a ribboned bundle, numbered by her mother in red ink. "
    "If he cried off now, they would be read aloud at the Assize, every endearment of them, and the Bench would put a "
    "price on her. He knew it. She knew it. The ribbon sat between them with the weight of a seal.")

# ---------- CO5: misquote fixed; 'maru' replaced (no unglossed term in prose)
Q["CO5"]["context"] = ("The Mahuo bank writes 'A verse was owed a verse', turns a sentence in its last clause as a sijo (a "
                       "three-line Korean lyric) does, and writes a drop in speech level as an event (R70-107). Joseon "
                       "houses matched by go-between and exchanged saju, the four pillars of birth hour, day, month and "
                       "year. Nothing on file says how a Mahuo courts.")
opt("CO5", "A")["sample"] = (
    "Widow Pyeon brought the paper into the lower hall folded five times and wrapped in red and blue cloth, the old "
    "houses' way. In it were Do-gyeom's four pillars: the hour, day, month and year of his first breath. The house "
    "elder read them twice. Eun-ha knelt at the far end of the boards and kept her eyes off the cloth. Her grandmother laid "
    "his pillars beside Eun-ha's and counted on her fingers, and the house hummed under them, ung-ung, while she counted.")
opt("CO5", "C")["sample"] = (
    "For two years Do-gyeom had spoken to her in the high forms, as a carver's son speaks to a house with its own "
    "ward-posts, and she had answered him in kind. In the lower hall that evening she poured his tea and said, \"Drink "
    "it before it goes cold,\" in the plain speech a woman keeps for her brothers and her husband. The cousins at the "
    "table went quiet. Do-gyeom set down the cup. He answered her in the same plain speech, and the house took it as "
    "done.")
Q["CO5"]["rules_touched"] = ["R70-107-SPEECH_LEVELS_ADDRESS_KOREAN", "R70-110-VERSE_EXCHANGED_TALK",
                             "R70-118-HONORIFICS_NARRATION", "R23-2-KOREAN_STRATUM"]

# ---------- CO6: 'eight characters' glossed
Q["CO6"]["context"] = ("In the halls the book is the house (R23-2), and verse answered plainly at court costs face "
                       "(R70-110). Value, Coin and Trade makes marriage the way a lineage acquires certified capability. "
                       "Chinese houses wed by go-between and the 'eight characters' (birth hour, day, month and year, two "
                       "characters each), and entered a wife in the husband's genealogy by her family name.")

# ---------- CO7: Kurlo used as canon has it (the bargain-ending 'Kurlo. Ei kurme.'); 'nothing exists' narrowed to trade
Q["CO7"]["context"] = ("The Dawi tongue has no future tense: a Dawi cannot say 'I will', so he swears ('Kurme') or calls a "
                       "thing 'Kurlo', unbegun, and 'Kurlo. Ei kurme.' ends a bargain. Nothing in trade exists until "
                       "entered in the Tally (their record of completed acts), a name's grade shows a broken oath, and "
                       "the Cask-Oath (sworn over a barrel) binds while the brew lives and after.")
Q["CO7"]["options"][2] = {
    "key": "C", "label": "Kurlo, the refusal unsaid",
    "consequence": "Courtship is 'Kurlo' said alone between two people, with the 'Ei kurme' that would end a bargain "
                   "left off: a thing unbegun and not refused, the nearest the tongue comes to hope.",
    "sample": ("Every Dawi knew how a bargain ended: Kurlo. Ei kurme. Unbegun, not undertaken. In the cask-hall, low, "
               "with the brew working in the staves, Haldekk said the first word to Ruutti and stopped there. "
               "\"Kurlo.\" She waited for the second word, and he left it unsaid. She took his beard-ring between finger "
               "and thumb and turned it once. \"Kurlo,\" she said back, and left it off too. The clerk had nothing to "
               "enter. Two unbegun things stood in one dark hall, and neither had refused.")}
Q["CO7"]["rec_reason"] = ("Both fall straight out of the no-future grammar, the Dawi's defining fact. B is strong, but it "
                          "puts every failed marriage on the Oath-Breakers' wall; take it too if you want that cost.")

# ---------- CO8: the question fits all four options; northern 'Ice' added
Q["CO8"]["title"] = "Consorts, concubines, widows"
Q["CO8"]["question"] = "Which marriage laws beyond one spouse for life go into the Inventories?"
Q["CO8"]["context"] = ("No law on file covers concubines or consorts, though the Eressean court keeps a consort "
                       "(Sandalphon). Bastardy already has words: the Accord's 'Sine sigillo', the Moto 'Written in the "
                       "wrong hand', northern law's 'Ice' for a child born before a recognised union. Chinese and Japanese "
                       "lineages entered secondary wives; Victorian law allowed one wife and tolerated the kept woman.")
opt("CO8", "C")["consequence"] = ("A Kharven widow and her stack may pass to her dead man's brother, wife or no wife, if "
                                  "she takes the skin from him, so no hearth goes cold; refusing is her right, and her "
                                  "hunger.")

# ---------- CO9: canon's marriage-as-instrument line and Muken's approval
Q["CO9"]["context"] = ("Canon makes marriage 'the standard instrument by which a lineage acquires certified capability' "
                       "(Value, Coin and Trade), Muken signed the approval for a match, and Obsession Force steered the "
                       "Stannvaard Queen toward one in the Kujo arc. Fronts are the table's threat clocks (Table Rule 4); "
                       "nothing says whether a betrothal is one.")

# ---------- CO10: terms glossed; option C mechanics fixed (no 'Attraction Layer'; a woken rider, not a licence)
Q["CO10"]["context"] = ("R70-39 carries feeling by one held image, and R70-104 makes a recurring rival's survival a "
                        "Ledger debt. Obsession Force (FOW's law of possessive fixation) collapses Breadth (how many "
                        "Wellsprings a soul can hold) and turns "
                        "Empathy into 'a one-directional parasitic channel'. Jin Ping Mei, the Ming household novel, runs "
                        "a whole plot on wives' rivalry, poison included. The archive has no jealous scene.")
opt("CO10", "C")["consequence"] = ("Fed long enough, jealousy turns to Obsession Force: Breadth collapses and Empathy runs "
                                   "one way. An instrument or a good Gnosis read can find it, which is its fair counter.")
opt("CO10", "C")["sample"] = (
    "At the meat-sharing Kolbein cut the widow Asdis the rib piece, and Torunn watched him do it across the fire, and "
    "went on watching. All that winter the rest of her life went thin. Kin, stack and horses fell out of her thoughts one "
    "by one until only the one man was left in them. At the spring muster the Hallenfeld Measurewright put his coil to "
    "her wrist, as to every woken rider's, and frowned at the needle. \"Your Breadth is down,\" he said, \"and your "
    "Empathy runs one way. That is how Obsession starts.\"")
Q["CO10"]["rec_reason"] = ("Grimdark wants jealousy to cost someone, and FOW already supplies its ruin with a price and a "
                           "counter a player can find; A stays open to any quiet scene under R70-39 without a ruling.")
Q["CO10"]["rules_touched"] = ["R70-104-RIVAL_BOND", "R70-39-CARRYING_FEELING", "R25-1-OBSESSION_SATISFIES_ATTRACTION_GATE",
                              "R71-44-FACULTY_READ_MAN", "R53-11-JUSTICE", "R70-85-SCENE_MOMENTS_THAT_EARN"]

# ---------- CO11: the only place conception and the pox are asked (group 1's K5 hands them here)
Q["CO11"]["context"] = ("Table Rule 9 owes 'a consequence afterward' and medicine runs 'by place and purse' (R71-79), but "
                        "contraception, pregnancy and the pox (syphilis) appear nowhere in law, the Inventories or the "
                        "price table. The period had the sheath, the sponge, poisonous herbs such as pennyroyal, and "
                        "mercury for the pox. No pregnancy has ever reached the Ledger.")
opt("CO11", "C")["consequence"] = ("A child comes when a couple decides, on the page or off, and the pox appears only "
                                   "where a scene sets out to put it there.")
Q["CO11"]["rec_reason"] = ("It is Table Rule 5's adjudication without dice brought to the bed: the cost is visible and "
                           "traceable, period medicine decides, and a child or a dose of mercury becomes the bill that "
                           "comes due.")

# ---------- CO12: R71-43 misquote fixed; Yorime's draw is a rare Claim art, never a household craft
Q["CO12"]["context"] = ("Pressure shows in the room first (R70-69); holding it in 'tires him in named places, jaw, collar, "
                        "temper' (R71-43); the unwoken feel a practitioner by the Aura table (R71-41). Canon's one "
                        "precedent is Yorime Seikai's Veil of the Last Hand, a Claim art (drawing Essence out of a target) "
                        "that lets her 'draw off limited pressure' from Dougou. No rule prices a marriage across the gap.")
Q["CO12"]["options"][1] = {
    "key": "B", "label": "Drawn off by an art",
    "consequence": "A partner who holds a draining art, as Yorime does, may take the Pressure off by touch at that art's "
                   "own price, traced to Fracture of Worlds before first use; love alone draws nothing.",
    "sample": ("Hale came down to breakfast with the night's work still on him, and the flame under the kettle leaned "
               "away from his chair. Mary came round the table behind him, peeled off her right glove and laid her bare "
               "palm flat between his shoulder blades. The draining art was the one thing her mother had left her. It "
               "came up her arm cold as well water. Her fingers ached to the second knuckle. The flame stood up "
               "straight. Hale ate his eggs, and Mary sat down to hers and ate them left-handed.")}
Q["CO12"]["rec_reason"] = ("A is R71-43 brought home and costs the stronger partner; B keeps Yorime's art rare and priced, "
                           "a fair counter with canon behind it. C and D would make every such love a tragedy by rule.")

# ---------- CO13: stays (group 1 hands Pressure in bed here); Stage names carry numerals; ambiguity and hyperbole cut
Q["CO13"]["context"] = ("Two Stages up brings sweat and nausea, the room showing it first (R70-69), and holding it in "
                        "costs the holder's body (R71-43). Here she is Stage III, Ascension, he Stage V, Splintering. "
                        "Arousal non-concordance (a body answering what the mind did not choose) is documented in sex "
                        "research. SC9 asks how a coerced body is framed; this asks whether Pressure can cause it.")
opt("CO13", "A")["sample"] = (
    "Lenz was deep in her and holding it in, and Ragnhild, who had buried one husband already, knew that jaw. At the "
    "peak his hold slipped. The blubber lamp lay down flat in its bowl. Frost crossed the inside of the shutter in one "
    "breath. Then it hit her: sweat everywhere at once, her stomach rolling, her cunt gone slack and dry around him. "
    "Whatever she had wanted a moment ago was gone under the weight. She shoved at his chest. He pulled out and got his "
    "hold back, swearing.")
opt("CO13", "B")["sample"] = (
    "Lenz was deep in her and holding it in, and Ragnhild, who had buried one husband already, knew that jaw. At the "
    "peak his hold slipped. The blubber lamp lay down flat in its bowl, and frost crossed the shutter in one breath. "
    "Sweat broke all over her. Her stomach rolled. Her cunt clenched on him, wet, hard, again, and some cold part of her "
    "watched it happen and knew it for the clench of a hand on a knife in the dark. Her body had answered the weight. "
    "She never had.")
opt("CO13", "C")["sample"] = (
    "Lenz was deep in her and holding it in, and Ragnhild, who had buried one husband already, knew that jaw. \"Let it "
    "go,\" she said. He looked down at her. \"All of it.\" He let it go. The blubber lamp lay down flat in its bowl. "
    "Frost crossed the shutter in one breath. Sweat broke over her and her stomach rolled, and she held on through it "
    "with her heels locked in the small of his back, because she had asked for all of him, and this was the part he gave "
    "nobody else.")
Q["CO13"]["depends_on"] = ["CO12", "SC9"]
Q["CO13"]["rec_reason"] = ("It keeps desire honest, which fair play asks of any power, and turns R71-43's suppression into "
                           "something a practitioner can give; B's darker engine stays open through Obsession workings, "
                           "which carry their own tells and counters (SC8).")

# ---------- CO14: R70-114 misquote fixed
Q["CO14"]["context"] = ("R70-114: 'Each live thread carries at least one standing warm bond (found family, master and "
                        "disciple, sworn kin)', written openly warm. Lovers are not named. The archive's love is mostly "
                        "mourned, and FOW warns a bond can rot into Obsession, so a thread whose only warmth is a romance "
                        "can lose all of it at once.")

# ---------- CO15: D grounded in FOW's Flourishing Catalyst and R70-84's breakthrough readout; invented 'tally-wire' gone
Q["CO15"]["context"] = ("The archive grows love by gesture: 'love expressed as maintenance', tokens carried for years. "
                        "Korean jeong is attachment that accrues through shared time and hardship, chosen or not. In "
                        "Fracture of Worlds the Catalyst (the event that completes a breakthrough) for Stage IV, "
                        "Flourishing, is 'formation of the first genuine Spirit Axis bond', a tie between two Crystals with "
                        "mechanical weight. No rule says whether a bond prints.")
opt("CO15", "A")["sample"] = (
    "Corin came back from the Well on the ninth day with his coat in ribbons, and Nell took it off him at the door "
    "without a word and sat down with it under the lamp. She had mended it four times now, and each time the stitches "
    "were smaller. He slept. When he woke the coat hung on the chair, whole, and in the inside pocket where he kept his "
    "half of the split tally she had sewn a square of her own blue flannel, which nobody would ever see but him.")
opt("CO15", "D")["consequence"] = ("The breakthrough readout R70-84 already owes at Flourishing also names its Catalyst, "
                                   "the first Spirit Axis, with no figure (R12-5); no other bond prints, and nothing says "
                                   "whether she loves him.")
opt("CO15", "D")["sample"] = (
    "Corin came back from the Well on the ninth day with the Crystal's line still in him. It had come at the bottom of "
    "the shaft, as the thing in the gallery went past and Nell's hand closed on his over the one lamp: Stage IV, "
    "Flourishing. Tier of Standing: Adept. Catalyst: first Spirit Axis formed. No figure stood beside the bond, and "
    "nothing in it said whether she loved him. That night he sat up by her fire while she slept in the other chair, read "
    "the line again, and looked at her face.")
Q["CO15"]["rec_reason"] = ("A is the house's best habit, B gives grimdark a bond nobody chose, and D puts the LitRPG layer "
                           "exactly where Fracture of Worlds already has it, the Flourishing Catalyst, while leaving the "
                           "read of her heart to the player; C belongs in the culture answers above.")
Q["CO15"]["rules_touched"] = ["R70-84-GROWTH_MOMENTS_THAT_EARN", "R70-78-WHERE_SCREEN_COMES_FROM",
                              "R70-91-BREAKTHROUGH_PAGE", "R70-82-NUMERALS_LADDER_RUNGS", "R12-5-NEVER_INVENT_NUMBER",
                              "R70-114-GRIMDARK_WARMTH"]

# ---------- CO16: C's named feeling replaced by an image (R70-39)
opt("CO16", "C")["sample"] = (
    "The horn comb came back by a carter from the south, tied with her own blue thread, and no word with it. "
    "Bjarke was alive. The whole outer town knew whose fire he sat at now, and that he would not be splitting for this "
    "one again. Inga untied the thread standing in the snow. The teeth were worn smooth on one side. She laid the comb on "
    "the night-stone, where it would stay warm. In the morning she put it out on the woodpile for the cold to have, and "
    "at dark she fetched it back.")

# ---------- CO17: Attraction Force glossed
Q["CO17"]["context"] = ("Fracture of Worlds: through Attraction Force (the law of recognition) 'spiritual relations "
                        "survive time, death, distance and change', and 'grief is the lawful tax on every covenant "
                        "ended'. Obsession keeps 'bonds preserved past death in broken, predatory form', and losing its "
                        "object 'produces fracture events'. No rule says how any of this shows on the page.")
Q["CO17"]["rules_touched"] = ["R12-5-NEVER_INVENT_NUMBER", "R25-1-OBSESSION_SATISFIES_ATTRACTION_GATE",
                              "R52-26-GRIEF", "R71-44-FACULTY_READ_MAN", "R70-85-SCENE_MOMENTS_THAT_EARN"]

# ---------- ME2: the only checks question (group 1 hands euphemism and the floor here); four options, all distinct
Q["ME2"]["context"] = ("verify_scene has no explicit mode: nothing checks scent, sound or mimetic words (words for texture "
                       "and state, roman under R70-133), the consequence Rule 9 owes, or a partner's age, and its firearms list counts 'cock' as "
                       "gun vocabulary. R71-103 watches the archive's tired fight devices; its tired touches (the hand on "
                       "the arm, the jaw held, the kiss on the hair) have no watch.")
Q["ME2"]["options"] = [
    {"key": "A", "label": "An explicit mode",
     "consequence": "verify --explicit WARNs on a scene with no smell word, no sound or mimetic word, an italic mimetic "
                    "word, or notes without a consequence line, and stops counting 'cock' as gun vocabulary."},
    {"key": "B", "label": "A floor guard",
     "consequence": "FAIL when an explicit scene names anyone whose card or roster gives an age under eighteen; WARN when "
                    "a named partner has no age on file. The body's age counts, never a soul's."},
    {"key": "C", "label": "Euphemism bans",
     "consequence": "Bed euphemisms that dodge R49-51 (his member, her sex, manhood, her core) FAIL in narration like the "
                    "hard-ban words; in a mouth they pass, since a character may be coy."},
    {"key": "D", "label": "Stale-touch watch",
     "consequence": "WARN past one a scene on the archive's repeated touches: the hand on the arm, the jaw held, the kiss "
                    "on the hair, as R71-103 does for fight devices."},
]
Q["ME2"]["rec_reason"] = ("B guards the floor itself and costs nothing to run; A and C make Rule 9 and R49-51 visible to a "
                          "script, and D catches the three touches the house survey counted before they become the only "
                          "moves.")
Q["ME2"]["rules_touched"] = ["R70-136-NEW_CHECKS_VERIFY_SCENE", "R71-103-COMBAT_CHECKS_VERIFY_SCENE", "R48-45-CHECKS",
                             "R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL", "R49-51-EXPLICIT"]

# ---------- ME4: A proves both ends of R70-134 by splitting the POV at a break mark
Q["ME4"]["context"] = ("R70-138 and R71-105 ran law and checks, then a test, amendment, then guides and bank. This test must "
                       "prove Rule 9 and R70-134 at both ends, a blunt Kharven POV and an image-led Moto one. A test with "
                       "your character leaves his body and choices to you; a canon couple puts the night into a book "
                       "thread.")
opt("ME4", "A")["consequence"] = ("Log the law and build ME2's checks; write one explicit scene between adult NPCs on your "
                                  "thread's Kharven ground, a Kharven half and a Moto half split by a break mark (R49-27); "
                                  "amend; then guides, Inventories and bank.")
Q["ME4"]["rec_reason"] = ("A proves both ends of R70-134 in one night with nothing canon at stake; a played test proves "
                          "the turn shape only once SC12 and SC13 settle what is yours in bed, and the Blank Seal's stop "
                          "is its point.")
Q["ME4"]["depends_on"] = ["ME2", "SC12"]
Q["ME4"]["rules_touched"] = ["R70-138-PROOF_ORDER_WORK", "R71-105-PROOF_ORDER_WORK", "R70-134-KEYED_CULTURE_FREE",
                             "R49-27-SCENE_BREAKS"]

# ---------- settled: only what this group leans on, deduplicated against group 1's list
d["settled"] = [
    {"point": "The lover's culture shows in what they do and say, whatever the POV's culture does to the narration.",
     "rule_ids": ["R70-134-KEYED_CULTURE_FREE"],
     "why_not_asked": "XS2 of the style law. CO2 to CO7 ask only the customs that give a lover's culture something to do and say."},
    {"point": "The Moto court, Eresse, the Mahuo houses and the lineage halls offer and answer verse at rites and in court, a plain answer costing face; each culture's verse form goes in its Inventory.",
     "rule_ids": ["R70-110-VERSE_EXCHANGED_TALK"],
     "why_not_asked": "Ruled 2026-10-03. CO3, CO5 and CO6 ask only whether verse also courts."},
    {"point": "Native address words and speech-level shifts written as events the room hears; a close POV carries its own culture's honorifics into narration, a Western POV plain names.",
     "rule_ids": ["R70-107-SPEECH_LEVELS_ADDRESS_KOREAN", "R70-118-HONORIFICS_NARRATION"],
     "why_not_asked": "Style law. CO5 C asks only whether such a shift is the Mahuo proposal; the Moto samples follow the POV's honorifics."},
    {"point": "Each Inventory owes fields for law and punishment, succession, and festivals written as performed; succession follows each culture's law.",
     "rule_ids": ["R70-45-NEW_STANDING_INVENTORY_FIELDS", "R60-21-SUCCESSION_BY_CULTURE"],
     "why_not_asked": "Already law. CO1 asks only whether courtship gets a field of its own, CO8 what fills the law field for more than one partner."},
    {"point": "Folk beliefs stand uncorrected by narration; ground-level justice borrows each culture's real analogue (labour-debt in Kharven, fines in Accord cities).",
     "rule_ids": ["R53-15-FOLK_BELIEFS", "R53-11-JUSTICE"],
     "why_not_asked": "World texture law. CO3 C builds on the Moto eye belief and CO10 B on labour-debt without reopening either."},
    {"point": "Every sum on the page is quoted from the approved price table, and payment in kind north of the arrays is named as exactly.",
     "rule_ids": ["R70-48-MONEY_PRICE_PROVENANCE", "R53-07-PRICE_TABLE"],
     "why_not_asked": "Settled. Bride-prices, settlements and allowances in these answers take their sums from the table; no question sets a price."},
    {"point": "Pressure shows in the room before the body; holding it in costs the holder's jaw, collar and temper and leaks; the unwoken feel a practitioner by the Aura table by Grade; commoners hold practitioners in awe.",
     "rule_ids": ["R70-69-PRESSURE_AURA", "R71-43-SUPPRESSION_PAGE", "R71-41-PRESSURE_UNWOKEN", "R53-18-AWE"],
     "why_not_asked": "Style, combat and world law. CO12 asks only what they cost a marriage, CO13 only whether Pressure reaches desire."},
    {"point": "A breakthrough prints a readout naming the new Stage and its Tier of Standing as the Catalyst completes, inside the crisis; the bearer reads only his own Crystal; Stage numerals sit beside the name; no figure is invented.",
     "rule_ids": ["R70-84-GROWTH_MOMENTS_THAT_EARN", "R70-91-BREAKTHROUGH_PAGE", "R70-78-WHERE_SCREEN_COMES_FROM", "R70-82-NUMERALS_LADDER_RUNGS", "R12-5-NEVER_INVENT_NUMBER"],
     "why_not_asked": "LitRPG law. CO15 D asks only whether that readout names a bond as its Catalyst; CO17 is written with no figure."},
    {"point": "Every live thread keeps a standing warm bond written openly warm; joy may have scenes; grief goes back to the root; tears break once per arc at a small thing; death is permanent.",
     "rule_ids": ["R70-114-GRIMDARK_WARMTH", "R52-26-GRIEF", "R52-27-JOY", "R70-115-TEARS_SENTIMENT", "R60-04-DEATH_IS_PERMANENT"],
     "why_not_asked": "Style and voice law. CO14 asks only whether lovers count as the warm bond, CO16 only the balance of lived and mourned."},
    {"point": "Obsession Force satisfies an Attraction gate; a Sacrament anchor is fixed by declaration whether or not the anchor consents.",
     "rule_ids": ["R25-1-OBSESSION_SATISFIES_ATTRACTION_GATE", "R29-1-SACRAMENT_BOND_ANCHOR_BY_DECLARATION"],
     "why_not_asked": "Ruled 2026-09-12. CO10 and CO17 build on them and do not reopen them."},
    {"point": "A recurring rival's survival is paid for on the Ledger with a debt, a scar or a witness.",
     "rule_ids": ["R70-104-RIVAL_BOND"],
     "why_not_asked": "Style law. CO10 B applies it to rivals in love."},
    {"point": "An intimate uses the personal name, and the narrator does not switch names without a reason.",
     "rule_ids": ["R20-5-ON_THE_PAGE"],
     "why_not_asked": "Naming law; a courtship's change of name is already governed by it."},
    {"point": "The order of proof: law and checks, a test scene, amendment, then the guides and the bank.",
     "rule_ids": ["R70-138-PROOF_ORDER_WORK", "R71-105-PROOF_ORDER_WORK"],
     "why_not_asked": "Precedent from both earlier laws. ME4 keeps the order and asks only who is in the test."},
    {"point": "What the Ledger keeps beyond the body, workings that bend desire, the coerced body, and your character in bed.",
     "rule_ids": [],
     "why_not_asked": "Asked in the first group (K5, SC8, SC9, SC12 to SC14). CO13 leans on SC9 and does not ask it twice."},
]

(HERE / "group-2.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("wrote", HERE / "group-2.json")
