"""Builds draft-2.json (sections CO and ME) for the intimacy questionnaire. Run: bash build/py.sh <this>."""
import json
import pathlib

OUT = pathlib.Path(__file__).with_name("draft-2.json")


def opt(key, label, consequence, sample=None):
    o = {"key": key, "label": label, "consequence": consequence}
    if sample:
        o["sample"] = sample
    return o


def q(id_, title, question, context, options, rec, reason, multi=False, depends=None, rules=None):
    return {"id": id_, "title": title, "question": question, "context": context, "options": options,
            "recommended": rec, "rec_reason": reason, "multi": multi,
            "depends_on": depends or [], "rules_touched": rules or []}


CO = []

CO.append(q(
    "CO1", "Where courtship custom lives",
    "Where does each culture's courtship and marriage custom live?",
    "R70-45 gives every Inventory fields for 'law and punishment, succession', and R60-21 sets succession there, but no field holds courtship, marriage or widowhood, and no Inventory has a wedding, a bride-price or a word for a lover. R70-134 says the lover's culture 'shows in what they do and say', which needs something on file to show.",
    [
        opt("A", "One courtship field",
            "Every Inventory gains a Courtship and Marriage field: the approach, the go-between, the gift or price, the vow, who may refuse, how a match ends, and widowhood. Entered on your word, culture by culture."),
        opt("B", "Courtship field, plus mores",
            "A, plus a Mores field: what the culture holds shameful and what it boasts of, nakedness and bathing, and what its law does to adultery, written beside R70-45's law field."),
        opt("C", "Only cultures in play",
            "The six cultures this section asks about get the field now; the others get it the first time a scene needs it, drafted then and entered on your word."),
    ],
    "B",
    "R70-134 keys a lover's conduct to culture, and conduct needs a shame line as much as a vow; the law field is owed anyway, so adultery costs nothing extra to place.",
    rules=["R70-45-NEW_STANDING_INVENTORY_FIELDS", "R60-21-SUCCESSION_BY_CULTURE", "R70-134-KEYED_CULTURE_FREE", "R53-15-FOLK_BELIEFS"]))

CO.append(q(
    "CO2", "Kharven courtship",
    "Which customs make a Kharven match?",
    "The Fusi Vā is gone, so a word given at the Seat is 'only as strong as the man who says it'. Canon gives the north labour-debt, meat-sharing, the skin (fermented milk in sealskin; refusing it insults the host) and the nameless day, when 'nothing binds'. Steppe peoples on Earth used bride-price and, some of them, bride-capture. No Kharven courtship is on file.",
    [
        opt("A", "The stack proves him",
            "A suitor splits for her household's woodpile unasked, labour-debt run in reverse; the asking comes when the stack is full and her kin say so. Entered in the Kharven field.",
            "Halvar had split for Gunnhild's house since the first snow, and nobody had asked him to. Every third day her stack stood higher, and every third day the old woman said nothing about it. In the Thin Weeks he came in, stamped the frost off his boots and stood by the fire. \"How's your stack?\" he said. \"Full,\" said Gunnhild. \"Somebody's been at it.\" Sigrun ladled the broth and put her own bowl in his hands. The word he gave her before the hearth that night was only as strong as he was."),
        opt("B", "The skin answers",
            "Her household answers at the hearth: she drinks from the sealskin and passes it across the fire, and he drinks after her before everyone. A withheld skin is the no, said without a word.",
            "Halvar came in the Thin Weeks with frost in his beard and stood just inside the door, which was as far as a man got before he was offered anything. Gunnhild looked at him a long while. Then she took the sealskin from its peg and unstoppered it, and the hut filled with the sour smell of the skin. She handed it to Sigrun. Sigrun drank, wiped the mouth with her thumb and held it out across the fire, and Halvar drank after her with the whole hearth watching."),
        opt("C", "Ridden off, priced after",
            "On the nameless day a man may ride off with a woman, and her kin name a price on the first named morning. Whether she went willing is hers to tell; the custom never asks.",
            "On the nameless day Halvar rode to Gunnhild's door with a led horse, and Sigrun came out in her hide-coat and got up on it. Nothing bound on that day, so nothing was broken. On the first named morning Gunnhild walked to his father's fire and named the price: two skins of seal fat, a salt bar, and a winter of splitting. His father paid it in front of the headman. Whether Sigrun had gone willing was hers to tell, and over the years she told it two ways."),
    ],
    "A,B,C",
    "A and B are one custom in two halves, the proof and then the answer, and C is the old road around a withheld skin, built on canon's nameless day; together they make northern courtship cost work, with a dark road beside it.",
    multi=True, depends=["CO1"],
    rules=["R70-45-NEW_STANDING_INVENTORY_FIELDS", "R53-15-FOLK_BELIEFS", "R70-134-KEYED_CULTURE_FREE", "R70-48-MONEY_PRICE_PROVENANCE"]))

CO.append(q(
    "CO3", "Moto courtship",
    "Which customs make a Moto match?",
    "Moto canon: a thing is 'asked in form, in the old register' and 'entered' in the family's own hand, and the clans keep their eyes down because the Moto read through the eyes (a folk belief, R53-15). R70-110 already lets the Moto court trade verse at rites, and R70-133 gives every culture the poem after the night.",
    [
        opt("A", "Asked in form, entered",
            "A match is asked in form at the hinge of the day and is real only when the register holds it in the house's own hand; an unentered lover is nobody to the house.",
            "Masatoki asked for her in form, at the hinge of the day, in the old register, with the steward standing witness and the bread not yet broken. Sayo-sama did not look at him. She watched the register on its stand while the steward wet the brush, and the room listened to it move: her name, his, the line, the day, in the family's own hand. Until the ink took, he had asked for nothing. When it had taken, she went to the table and broke the bread for two."),
        opt("B", "Letters, graded by speed",
            "Courtship runs by three-line letters with a token through the knot, and the speed of an answer is read as regard, as at the Heian court (Japan's classical court era).",
            "His letter came before the court was swept, folded small, with a sprig of larch through the knot and three lines in a soldier's square hand. Sayo-sama read it once and laid it face down on the lacquer, and all morning it lay there. A quick answer would tell the household too much. A slow one would tell him. At the hinge of the day she took the brush, wrote her three lines beneath his last, and sent it back by the same runner before the bread."),
        opt("C", "The eyes offered",
            "A suitor outside the line courts by lifting his eyes to a Moto and leaving them there, offering himself to be read; whether she reads him, and how far, is her answer.",
            "Every retainer at the Seat kept his eyes below the line's, and for a year Masatoki had kept his on Sayo-sama's collar. This morning, by the scale, he lifted them and let them stay. She had been taught from the cradle to read through that door. The outer ring of her iris flared once. She could have gone to the bottom of him then, and he knew it, and he held still and let her. Neither of them spoke. She went in only as far as his name."),
    ],
    "A,C",
    "The register and the read through the eyes are the Moto's own canon objects; letters would double the poem after (R70-133) and the court verse (R70-110) the Moto already have.",
    multi=True, depends=["CO1"],
    rules=["R70-110-VERSE_EXCHANGED_TALK", "R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL", "R53-15-FOLK_BELIEFS", "R23-2-JAPONIC_STRATUM"]))

CO.append(q(
    "CO4", "Accord courtship",
    "Which customs make an Accord match?",
    "The Accord is the Victorian city (R59-07), with money and paper on every page (R70-48). Victorian England married by settlement (a contract fixing the wife's property), courted by calls and cards under a chaperone, and let a jilted party sue for breach of promise. The Accord's only courtship canon is its bastardy swear, 'Sine sigillo', without seal.",
    [
        opt("A", "Terms under seal",
            "A match is a settlement drawn by a solicitor and sealed by the Board, with what stays in her name written in. Courtship is the negotiation, and love shows in the clauses.",
            "Abel Tobin got his answer in Mrs Crane's front parlour, and it came on foolscap. Mr Pruett of Pruett and Vole had drawn the settlement overnight. Lettice's draw-licence stayed in her own name, and so did the lease on the upper room, and the clause said so twice. Tobin read it through with his hat on his knee while Lettice watched him read. At the foot was a space for the Board's seal and a space beside it for his hand, and the ink on the stand was fresh."),
        opt("B", "Calls, cards, a chaperone",
            "Courtship runs by the parlour: calls at set hours, a card left with its corner turned, a chaperone who never leaves the room. A yes is said with the card.",
            "Abel Tobin made his eighth call, and Mrs Crane sat through it with her sewing, as she had sat through the other seven. The parlour clock ticked over the draw-hum from the street. Lettice poured. When he rose to go, the maid brought his card back on the salver with its corner turned down in Lettice's own hand, and under his name, in pencil, the hour of his next call. Mrs Crane bit off her thread. It was as far as a daughter could say yes in a parlour."),
        opt("C", "Breach of promise sued",
            "A broken engagement is actionable before the Bench: the letters are read aloud and a jury prices the jilt. Every love letter in the Accord is also evidence.",
            "Abel Tobin got his answer in Mrs Crane's front parlour, in writing, because Lettice had been told to give it no other way. Every letter he had sent her lay on the table in a ribboned bundle, numbered by her mother in red ink. If he cried off now, they would be read aloud before the Bench, every endearment of them, and a jury would put a price on her. He knew it. She knew it. The ribbon sat between them with the weight of a seal."),
    ],
    "A,C",
    "Money and paper are the Accord's tilt; a settlement and a suit put a price on love, which the city's narration already counts, while the parlour ritual is period dress any culture could wear.",
    multi=True, depends=["CO1"],
    rules=["R59-07-VICTORIAN_EDWARDIAN_CITY", "R70-48-MONEY_PRICE_PROVENANCE", "R53-11-JUSTICE"]))

CO.append(q(
    "CO5", "Mahuo courtship",
    "Which customs make a Mahuo match?",
    "The Mahuo bank has 'a verse is owed a verse', the sijo's turn in its last clause (a sijo is a three-line Korean lyric) and speech levels as events (R70-107). Joseon houses matched by go-between and exchanged saju, the four pillars of birth hour, day, month and year. Nothing on file says how a Mahuo courts.",
    [
        opt("A", "Pillars by go-between",
            "A go-between carries the households' four pillars, and the elders read the match before the pair have a say. Love, if it comes, comes after, as jeong: attachment that grows with shared years.",
            "Widow Pyeon brought the paper into the lower hall folded five times and wrapped in red and blue cloth, the old houses' way. In it were Do-gyeom's four pillars: the hour, day, month and year of his first breath. The elder read them twice. Eun-ha knelt at the far end of the maru and kept her eyes off the cloth. Her grandmother laid his pillars on the boards beside Eun-ha's and counted on her fingers, and the house hummed under them, ung-ung, while she counted."),
        opt("B", "A sijo owed a sijo",
            "Courtship is a verse exchange: the suitor's three lines are answered with three, and the last clause turns. A plain answer costs standing, as R70-110 rules at court.",
            "The verse came up from Do-gyeom's household in his own brush: three lines, the river in the first, the ford in the second, and in the third a turn on a ferryman who would not cross without his fare. The whole lower hall had read it by noon. A verse was owed a verse. Eun-ha took the brush at the recorder's wall and answered in three lines of her own, and her last clause turned on the fare. A ferry, she wrote, is paid on the far bank."),
        opt("C", "The speech level drops",
            "The proposal is a change of speech: one of them drops from the high forms to the plain speech kept for kin and spouses, and the other answering in kind is the yes.",
            "For two years Do-gyeom had spoken to her in the high forms, as a carver's son speaks to a house with its own ward-posts, and she had answered him in kind. On the maru that evening she poured his tea and said, \"Drink it before it goes cold,\" in the plain speech a woman keeps for her brothers and her husband. The cousins on the step went quiet. Do-gyeom set down the cup. He answered her in the same plain speech, and the house took it as done."),
    ],
    "B,C",
    "Both are Mahuo law already, turned to love: the verse owed a verse and speech levels as events. A go-between is real but belongs to every Eastern house; the speech drop belongs to the Korean register alone.",
    multi=True, depends=["CO1"],
    rules=["R70-107-SPEECH_LEVELS_ADDRESS_KOREAN", "R70-110-VERSE_EXCHANGED_TALK", "R23-2-KOREAN_STRATUM"]))

CO.append(q(
    "CO6", "Courtship in the lineage halls",
    "Which customs make a match in the lineage halls?",
    "In the halls the book is the house (R23-2), and a matched couplet traded at court costs face when answered plainly (R70-110). Canon's Value, Coin and Trade names marriage the standard way a lineage acquires certified capability. Chinese houses wed by go-between and the 'eight characters' of birth, and entered a wife in the husband's genealogy by her family name.",
    [
        opt("A", "Entered in the book",
            "A marriage is real when the husband's hall enters her in its book as 'of' her father's hall; a secondary wife is entered lower, and an unentered woman has no standing in the hall.",
            "Nothing was settled until the Fang book said so, and the Fang book lay in the tablet room under the eyes of the Fang dead. The hall elder opened it at his grandson's leaf. Beneath Zhiyuan's line, in a small even hand, he wrote the two characters that meant 'of the Lu', and the date, and blotted them. Qingyan's own name did not go in. She had known since childhood that it would not. She watched the blotter lift from the two characters that would be all of her on that page."),
        opt("B", "A couplet matched",
            "Her hall sets the first line of a couplet on its gate, and the suitor must match it on the spot, in public, or forfeit the match. The halls' court verse turned to courtship.",
            "The Lu set the first line of the couplet on the hall gate: The river owes the sea each drop it carries. Fang Zhiyuan read it from the street with his hands in his sleeves, while the Lu cousins watched from the steps to see the Fang shamed. A plain answer would cost him the match. He asked for a brush and wrote the second line beneath it where he stood: The sea returns each drop as rain, and keeps no book. Behind the screen, Lu Qingyan laughed once."),
        opt("C", "Bought for the book",
            "A hall marries for a skill it lacks, and the bride-gifts come with a schedule of what her children will be taught. Love is a clause, and the halls say so.",
            "The Fang wanted the Lu hand, and they meant it plainly: three generations of Measurewrights who read a gauge to its last division, and a daughter who had learned at her father's bench. The bride-gifts came into the courtyard on carrying poles, and with them came a schedule, in the Fang clerk's hand, of what her children would be taught and by whom. Qingyan read the schedule before she looked at the silk. The schedule was the letter. The silk was its envelope."),
    ],
    "A,C",
    "The book and the purchase of capability are both canon; a couplet at the gate is already legal at court under R70-110, so it needs no ruling to appear.",
    multi=True, depends=["CO1"],
    rules=["R23-2-CHINESE_STRATUM_SUMMARY", "R70-110-VERSE_EXCHANGED_TALK"]))

CO.append(q(
    "CO7", "Dawi courtship",
    "Which customs make a Dawi match?",
    "The Dawi language has no future tense: a Dawi cannot say 'I will', and either swears ('Kurme') or calls a thing 'Kurlo', unbegun. Nothing exists until it is entered in the Tally (their record of completed acts), a name's grade shows a broken oath, and the Cask-Oath binds while the brew lives and after. A promise of love is a sentence they cannot make.",
    [
        opt("A", "Entered, never promised",
            "A Dawi match is made backward: the acts already done for each other are entered in the Tally in metre, and the entry is the marriage. There is no betrothal.",
            "Haldekk could not tell her what he would do, because no Dawi can. So he told the clerk what he had done. He had stood her shifts in the lower gallery through the fever winter, and he had carried her brother's casket home from the Ring unopened. The clerk entered each act in metre while Ruutti listened for the grade in his name. It held strong. When the last line closed on \"on\", she laid her hand flat on the Tally beside his. The entry held, and that was the marriage."),
        opt("B", "A cask laid down",
            "The pair swear the Cask-Oath over a cask they lay down together, binding while the brew lives and after. A broken marriage is a broken cask oath, with its line on the Oath-Breakers' wall.",
            "They laid the cask down together in the deep hall, each with a hand on the stave, and sang the Cask-Oath over it while the pitch was still tacky: Ollu elaa, kaasme elaa. Haldekk drove the bung. Ruutti cut both their names into the head in doubled strokes, the strong grade. Years on, at the Drawing-Off, the cask would go up the shaft with the rest, and the oath would stay down here with them. The brew dies, and the oath does not die."),
        opt("C", "Kurlo, said aloud",
            "Courtship is the one word they have for what is not yet done: each says 'Kurlo' over the two of them. It promises nothing, and it is said only between lovers.",
            "A Dawi has one word for a thing not yet done, and Haldekk said it to her in the cask-hall, low, with the brew working in the staves around them. \"Kurlo.\" Ruutti heard the grade of it, which was neither strong nor weak, because it named nothing yet. She took his beard-ring between finger and thumb and turned it once. \"Kurlo,\" she said back. They were two unbegun things in one dark hall, and the clerk had nothing to enter."),
    ],
    "A,C",
    "Both fall straight out of the no-future grammar, the Dawi's defining fact. B is strong, but it puts every failed marriage on the Oath-Breakers' wall; take it too if you want that cost.",
    multi=True, depends=["CO1"],
    rules=["R70-45-NEW_STANDING_INVENTORY_FIELDS", "R70-134-KEYED_CULTURE_FREE"]))

CO.append(q(
    "CO8", "Consorts, concubines and the law",
    "Where may a person keep more than one partner under law, and how?",
    "No law on file covers concubines or consorts, though the Eressean court keeps a consort (Sandalphon) and bastardy has swears: the Accord's 'Sine sigillo' and the Moto 'Written in the wrong hand'. R70-45 already owes each Inventory a law field. Real houses split: Chinese and Japanese lineages entered secondary wives, and Victorian law allowed one wife and tolerated the kept woman.",
    [
        opt("A", "Entered lower, in book",
            "The lineage halls and the Moto enter a secondary wife or consort below the wife in the book or register; her children's standing is written there, and an unentered child is 'written in the wrong hand'."),
        opt("B", "Accord: off the books",
            "One spouse in Accord law. A kept woman or kept man lives on an allowance quoted from the price table, a scandal with a sum on it, and their children are sine sigillo."),
        opt("C", "Kharven: the brother's widow",
            "A Kharven widow and her stack may pass to her dead man's brother if she takes the skin from him, so no hearth goes cold; refusing is her right, and her hunger."),
        opt("D", "Dawi: one entry only",
            "The Tally holds one marriage entry. A second partner is an act nobody will stand behind, 'kurnur', unentered, and carries that swear in the hold."),
    ],
    "A,B,C,D",
    "Each falls out of a canon object (the book and register, the seal, the stack, the Tally), so each culture's law is its own and the owed law field fills with no invention beyond it.",
    multi=True, depends=["CO1"],
    rules=["R70-45-NEW_STANDING_INVENTORY_FIELDS", "R60-21-SUCCESSION_BY_CULTURE", "R53-11-JUSTICE", "R70-48-MONEY_PRICE_PROVENANCE"]))

CO.append(q(
    "CO9", "Marriage as politics",
    "When a match is political, how does the table run it?",
    "Succession follows each culture's law (R60-21), and canon ties marriage to crowns: the Kharven queen-line, the Moto succession, and the Stannvaard Queen steered toward a match by Obsession Force in the Kujo arc. Fronts are the table's threat clocks (Table Rule 4), and nothing says whether a betrothal is one.",
    [
        opt("A", "A Front with a clock",
            "A political match in play runs as a Front: betrothal, settlement, wedding and first heir are its ticks. A broken match fires the Front, and someone pays."),
        opt("B", "A debt on the Ledger",
            "A match is a debt between houses on the Ledger (Table Rule 7), called in when it comes due: a dowry unpaid, an heir owed, a promise outstanding."),
        opt("C", "News only",
            "Political marriages happen offscreen and reach the table through the Rumor Mill, some of it wrong; only a match your character touches comes onto the page."),
    ],
    "A",
    "A clock makes a match something the world moves on whether or not your character is looking, which Table Rule 4 asks of everything; the debt lives inside the Front anyway.",
    rules=["R60-21-SUCCESSION_BY_CULTURE", "R48-30-SURPRISES"]))

CO.append(q(
    "CO10", "Jealousy and rivals",
    "What does jealousy do in WOTR?",
    "R70-39 already carries feeling by a held image, and R70-104 makes a recurring rival's survival a Ledger debt. Fracture of Worlds Part Fourteen gives jealousy a metaphysics: Obsession Force 'collapses Breadth' and turns Empathy into 'a one-directional parasitic channel'. Jin Ping Mei, the Ming household novel, runs a whole plot on wives' rivalry, poison included. The archive has no jealous scene.",
    [
        opt("A", "Carried, never acted",
            "Jealousy stays in the body and the habits, carried by a held image; it is seldom acted on, and the cost falls on the one who carries it.",
            "At the meat-sharing Kolbein cut the widow Asdis the rib piece, and Torunn watched him do it from across the fire. She said nothing. She finished her bowl. That night she split rounds at the woodpile until the moon was down and stacked them a hand's breadth tighter than she ever had, and in the morning she brought his broth to him the way she always did. The stack stayed tight all winter. Kolbein never asked her why."),
        opt("B", "A feud with a bill",
            "Jealousy acts: slander, theft, a duel, poison. Each act lands on the Ledger as a debt or a witness, and a love rival who recurs is paid for as R70-104 rules.",
            "At the meat-sharing Kolbein cut the widow Asdis the rib piece, and Torunn watched him do it from across the fire. By the Thin Weeks the whole outer town had heard that Asdis was wet wood. Before the thaw her stack went short twice in the night, and nobody could say who had carried it off. Asdis went to the headman. The headman named a labour-debt against Torunn's hearth, a day's splitting for every round, and Torunn paid it round by round and called it cheap."),
        opt("C", "The road to Obsession",
            "Fed long enough, jealousy narrows the Attraction Layer toward one person, the FOW corruption; an instrument or a good Gnosis read can find it, which is its fair counter.",
            "At the meat-sharing Kolbein cut the widow Asdis the rib piece, and Torunn watched him do it across the fire, and went on watching. All that winter the rest of her life went thin. Kin, stack and horses fell out of her thoughts one by one until only the one man was left in them. In the Thin Weeks the Hallenfeld Measurewright put his coil to her wrist for her draw-licence and frowned at the needle. \"Your Breadth is down,\" he said, \"and your Empathy runs one way. That is how Obsession starts.\""),
    ],
    "B,C",
    "Grimdark wants jealousy to cost someone, and FOW already supplies its ruin with a price and a counter a player can find; A is the house default under R70-39 and needs no ruling.",
    multi=True,
    rules=["R70-104-RIVAL_BOND", "R70-39-CARRYING_FEELING", "R25-1-OBSESSION_SATISFIES_ATTRACTION_GATE", "R71-44-FACULTY_READ_MAN"]))

CO.append(q(
    "CO11", "Conception and the pox",
    "Do conception and the pox ride on every bed?",
    "Table Rule 9 owes 'a consequence afterward', and medicine runs 'by place and purse' (R71-79, R53-10), but contraception, pregnancy and venereal disease appear nowhere in law, the Inventories or the price table. The period had the sheath, the sponge, poisonous herbs such as pennyroyal, and mercury for the pox. Yoko Mishiro's two children both arrived offscreen.",
    [
        opt("A", "Ruled openly, every time",
            "Each bed between partners who could conceive records its precaution (sheath, sponge, timing, a Draft, or none) in the notes; Natalie rules conception and the pox by period medicine, names what decided, and a pregnancy opens a Front."),
        opt("B", "Story's call, planted first",
            "No bookkeeping: a pregnancy or the pox arrives when the story wants it, planted in an earlier scene so a reader could have seen it coming (R48-30)."),
        opt("C", "Only by choice",
            "Characters who want no child have none, and the pox never appears; children come when a couple decides, offscreen or on the page."),
    ],
    "A",
    "It is Table Rule 5's adjudication without dice brought to the bed: the cost is visible and traceable, the period's medicine decides, and a child or a dose becomes the bill that comes due.",
    rules=["R53-10-MEDICINE", "R71-79-MEDICINE_PLACE_PURSE", "R48-30-SURPRISES"]))

CO.append(q(
    "CO12", "Love across a Stage gap",
    "What does a Stage gap cost a couple over the years?",
    "Pressure shows in the room first, then in bodies (R70-69); a suppressed man pays 'in named places of his body (jaw, collar, temper)' and leaks (R71-43); the unwoken feel a practitioner by the Aura table, dread up to bent knees (R71-41). Canon's one precedent is Yorime Seikai, who 'drew off his pressure with her hand'. No rule says what a marriage across the gap costs.",
    [
        opt("A", "He holds it, and pays",
            "The higher partner suppresses at home every waking hour; his jaw, collar and temper carry it, and the household learns to read the bill.",
            "Hale came down to breakfast holding it in, as he had every morning of their marriage, and Mary watched what it cost him. His jaw went first, set a shade too hard while he buttered his toast. Then two fingers went to his collar, hooked in it, eased it and let go. The kettle sang. He was short with the maid over nothing. Mary poured his tea and set it at his elbow and said nothing about the jaw, because if he let go to answer her, the lamp would lie down and so would she."),
        opt("B", "She learns to draw it",
            "The lower partner may learn to draw Pressure off by touch, as Yorime did; it costs her hand and arm, and its mechanism is traced to Fracture of Worlds before first use.",
            "Hale came down to breakfast with the night's work still on him, and the flame under the kettle leaned away from his chair. Mary came round the table behind him and laid her palm flat between his shoulder blades, the way the Guild wives taught one another, and breathed slow, and drew. It came up her arm cold as well water. Her fingers ached to the second knuckle. The flame stood up straight. Hale ate his eggs, and Mary sat down to hers and ate them left-handed."),
        opt("C", "The houses forbid it",
            "Houses and the Guild bar or tax a match across a wide gap for the heirs' sake; such marriages run in secret, or pay.",
            "Hale came down to breakfast and found a letter from his House beside his plate, sealed in grey wax. Mary knew the seal. It was the third since the wedding. The House did not object to her, the letter said. It objected to the heirs, who would be born to a man of his Stage from a woman of none, and whom no Measurewright could promise to assay. Hale read it with his jaw set. Mary poured his tea, and the lamp stayed where it was."),
        opt("D", "The awe never leaves",
            "An unwoken spouse keeps the commoner's awe (R53-18) for life: the body stands, bows or flinches before the mind can stop it, and the marriage keeps that distance.",
            "Hale came down to breakfast, and Mary stood up when he came in. She had done it every morning for six years and could not stop. Her knees knew him before she did. Once he had asked her, gently, not to, and she had tried, and her body had stood her up anyway, out of the chair, hands flat on the cloth. He touched her cheek with one knuckle and sat. She sat when he had. Her tea had gone cold by then, and neither of them mentioned it."),
    ],
    "A,B",
    "A is R71-43 brought home and costs the stronger one; B is canon on Yorime's card and gives the weaker partner a craft and a price, which is the fair answer; C and D would make every such love a tragedy by rule.",
    multi=True,
    rules=["R71-43-SUPPRESSION_PAGE", "R71-41-PRESSURE_UNWOKEN", "R70-69-PRESSURE_AURA", "R53-18-AWE"]))

CO.append(q(
    "CO13", "Pressure in bed",
    "Can Pressure reach desire in bed?",
    "Pressure runs on the Stage ladder (NATALIE.md): two Stages up brings sweat and nausea, and the room shows it first (R70-69). In these samples she is Ascension and he is Splintering, two Stages apart. Nothing rules what Pressure does in bed. Arousal non-concordance, a body answering what the mind did not choose, is documented in sex research.",
    [
        opt("A", "Weight, never wanting",
            "Pressure brings weight, sweat and nausea and never desire; any wanting on the page is the person's own, and a slipped hold ends the moment.",
            "Lenz was deep in her and holding it in, and Ragnhild could tell by his jaw. At the peak his hold slipped. The blubber lamp lay down flat in its bowl. Frost crossed the inside of the shutter in one breath. Then it hit her: sweat everywhere at once, her stomach rolling, her cunt gone slack and dry around him. Whatever she had wanted a moment ago was gone under the weight. She shoved at his chest. He pulled out and got it back in, swearing."),
        opt("B", "Weight the body mistakes",
            "Pressure cannot make desire, but a body under it may answer as it answers fear, and the POV knows the difference: a dubcon (dubious consent) engine, the room its tell, distance or suppression its counter.",
            "Lenz was deep in her and holding it in, and Ragnhild could tell by his jaw. At the peak his hold slipped. The blubber lamp lay down flat in its bowl, and frost crossed the shutter in one breath. Sweat broke all over her. Her stomach rolled. Her cunt clenched on him, wet, hard, again, and some cold part of her watched it happen and knew it for the clench of a hand on a knife in the dark. Her body had answered the weight. She never had."),
        opt("C", "Let go, by leave",
            "A, plus: a lover may ask him to stop holding it in. Letting go is the most intimate thing a practitioner can give, and she pays in sweat and nausea she chose.",
            "Lenz was deep in her and holding it in, and Ragnhild could tell by his jaw. \"Let it go,\" she said. He looked down at her. \"All of it.\" He let it go. The blubber lamp lay down flat in its bowl. Frost crossed the shutter in one breath. Sweat broke over her and her stomach rolled, and she held on through it with her heels locked in the small of his back, because she had asked, and nobody else in the north had ever been given this."),
    ],
    "C",
    "It keeps desire honest, which fair play asks of any power, and turns R71-43's suppression into something a practitioner can give; B's dark engine stays open through Obsession workings, which carry their own tells and counters.",
    depends=["CO12"],
    rules=["R70-69-PRESSURE_AURA", "R71-43-SUPPRESSION_PAGE", "R49-51-EXPLICIT"]))

CO.append(q(
    "CO14", "Lovers and the warm bond",
    "Does a romance count as a thread's standing warm bond?",
    "R70-114: 'Every live thread carries at least one standing warm bond (found family, master and disciple, sworn kin)', written openly warm. Lovers are not named. The archive's love is mostly mourned, and FOW warns a bond can rot into Obsession, so a thread whose only warmth is a romance can lose all of it at once.",
    [
        opt("A", "Lovers count",
            "A romance may be a thread's warm bond on its own."),
        opt("B", "Never the only one",
            "Lovers count, but each thread also keeps a warm bond that is not romantic, so a romance that dies, sours or turns to Obsession leaves warmth standing."),
        opt("C", "Lovers never count",
            "The warm bond is found family, master and disciple, or sworn kin; romance comes on top and may run cold."),
    ],
    "B",
    "Grimdark needs love to be losable, and R70-114 exists so that a loss never empties a thread; B lets lovers be warm and still keeps a floor under them.",
    rules=["R70-114-GRIMDARK_WARMTH"]))

CO.append(q(
    "CO15", "How a bond grows",
    "How does a bond show itself growing across scenes?",
    "The archive grows love by gesture: 'love expressed as maintenance', tokens carried for years. Korean jeong is attachment that accrues through shared time and hardship, chosen or not. Fracture of Worlds puts the first genuine Spirit Axis (a bond with mechanical weight) at the threshold into Flourishing, and Axis measures Essence across bonds; no rule says when a bond prints.",
    [
        opt("A", "Tokens and maintenance",
            "A bond grows by what is mended, fed and carried: the coat, the comb, the bowl. Each scene adds one, and the reader counts them.",
            "Corin came back from the Well on the ninth day with his coat in ribbons, and Nell took it off him at the door without a word and sat down with it under the lamp. She had mended it four times now, and each time the stitches were smaller. He slept. When he woke the coat hung on the chair, whole, and in the inside pocket where he kept his tally-wire she had sewn a square of her own blue flannel, which nobody would ever see but him."),
        opt("B", "Jeong through hardship",
            "A bond grows from shared cost, chosen or not: a night in a collapsed gallery, a winter of short rations. Enemies can accrue it, and it binds them anyway.",
            "Corin came back from the Well on the ninth day, and Nell came back with him, because she had gone down too as his lamp-bearer. Neither had much liked the other at the top of the shaft. At the bottom something had come up the gallery, and they had held the one lamp between them, shaking, until it went past. Now they sat in her kitchen with the same cold in their bones and passed one pot of tea back and forth, and neither of them needed to talk."),
        opt("C", "A ladder by culture",
            "Each culture has steps a bond must climb (visits, calls, nights, days at the table), entered in its Courtship field; a step skipped is a scandal or an insult.",
            "Corin came back from the Well on the ninth day and went round to Nell's for the third time. The first time she had let him in and given him the chair and nothing else. The second time she had given him tea, and her name. Tonight, by the custom of the lower wards, the asking was owed, and so was the answer, and both of them knew which step they stood on as well as they knew the steps up to her door. She took his wet coat and hung it on her own peg."),
        opt("D", "Crystal fact, no figure",
            "At a threshold the bearer's own readout may print a Spirit Axis or Axis row with no figure (R12-5); it says the bond exists, never whether she loves him.",
            "Corin came back from the Well on the ninth day and slept the clock round in Nell's bed with her hand on his chest. On the edge of waking the Crystal showed him his own sheet, as it does at a threshold, and there was a row on it that had not been there before. Spirit Axis: formed. No figure stood beside it. It did not say whether she loved him. He lay still under her hand, read it again, and then turned his head to look at her face."),
    ],
    "A,B,D",
    "A is the house's best habit, B gives grimdark a bond nobody chose, and D puts the LitRPG layer where FOW already has it while leaving the read to the player; C belongs in the culture answers above.",
    multi=True,
    rules=["R12-5-NEVER_INVENT_NUMBER", "R70-78-WHERE_SCREEN_COMES_FROM", "R70-114-GRIMDARK_WARMTH"]))

CO.append(q(
    "CO16", "Love mourned or lived",
    "How much of WOTR's love is lived before it is lost?",
    "The house survey found more love mourned than lived: most couples are established offscreen, shown once, and ended by death or duty. R70-114 lets joy have scenes of its own, death is permanent (R60-04), and grief takes a voice back to its roots (R52-26). The question is the balance, not whether loss costs.",
    [
        opt("A", "Mourned more than lived",
            "The house default stands: bonds mostly arrive established, and their scenes are partings, tokens and grief.",
            "The horn comb came back with his horse, tied to the pommel with a bit of her own blue thread. Inga untied it standing in the snow. She had carved it the winter before they were married and had never once seen him use it. The teeth were worn smooth on one side. She went into the death-house to begin the Waiting and took the comb with her, and did not let the other women see it."),
        opt("B", "Lived first, then cost",
            "A bond gets scenes of its own joy before a loss may land on it; a love that dies before the reader has seen it lived is a fault to fix.",
            "The horn comb came back with his horse, tied to the pommel with a bit of her own blue thread. Inga untied it standing in the snow. She had carved it the winter they laughed through at the Seat, when he raced the Thornwall men on the ice and lost his hat and both mittens, and every night since she had watched him comb his beard with it, badly, to please her. The teeth were worn smooth on one side. She went into the death-house to begin the Waiting."),
        opt("C", "Ended by choice",
            "Heartbreak comes more from leaving, refusal and betrayal than from death; fewer lovers die, and more walk away alive.",
            "The horn comb came back by a carter from the south, tied with a bit of her own blue thread, and no word with it. Bjarke was alive. The whole outer town knew whose fire he sat at now, and that he would not be splitting for this one again. Inga untied the thread standing in the snow. The teeth were worn smooth on one side. She went in and laid the comb on the night-stone, where it would stay warm, and hated herself for doing it."),
    ],
    "B",
    "Grimdark costs only what was shown to be worth something; the archive's habit of mourning loves it never lived spends grief it has not earned.",
    rules=["R70-114-GRIMDARK_WARMTH", "R60-04-DEATH_IS_PERMANENT", "R52-26-GRIEF"]))

CO.append(q(
    "CO17", "A bond after death",
    "What does a lover's death do to the survivor's Crystal?",
    "Fracture of Worlds: through Attraction Force 'spiritual relations survive time, death, distance and change', and 'grief is the lawful tax on every covenant ended'. Obsession keeps 'bonds preserved past death in broken, predatory form', and losing its object 'produces fracture events'. No rule says how any of this shows on the page.",
    [
        opt("A", "Carried clean",
            "The bond survives death clean and reciprocal: the survivor's Spirit Axis holds, felt at thresholds and readable by instrument, with no figure, and grief is its tax.",
            "A year after the funeral the Measurewright put his coil to Widow Fenn's wrist for her licence renewal and watched the needle a long while. \"There's a bond on you still,\" he said. \"Spirit Axis, held, and the far end of it quiet. It reads clean.\" She asked him what that meant. \"That he's still recognised,\" he said. \"The Guild calls it a covenant carried. The old women call it grief. It's the same tax.\" He wrote her up fit."),
        opt("B", "Clean or a cage",
            "A, plus the turn: grief fed long enough tips the bond into Obsession, which an instrument or a good Gnosis read can find, and a Crystal grown dependent on the dead risks FOW's fracture events.",
            "A year after the funeral the Measurewright put his coil to Widow Fenn's wrist for her licence renewal and did not like the needle. \"There's a bond on you still,\" he said. \"Spirit Axis, held hard, and everything else on you thinned to make room for it.\" She asked him what that meant. \"That you've kept him the wrong way,\" he said, and he wrote it on the form in plain words, because a Crystal that leans on a dead man can crack, and the Board liked to know first."),
        opt("C", "Human only",
            "A lost love is grief in the body and the life; the Crystal says nothing, and no instrument reads it.",
            "A year after the funeral the Measurewright put his coil to Widow Fenn's wrist for her licence renewal and read her clean, with nothing out of true and nothing held that should not be. He wrote her up fit. On the stair going down she stopped, because the third step still creaked as it had under her husband's weight, and she stood on it a while with her hand on the rail. The coil had nothing to say about that."),
    ],
    "B",
    "It is FOW's own law, both halves, and it gives grief a danger with a tell and a counter a player can find, which is fair; C would leave canon metaphysics unused.",
    depends=["CO15"],
    rules=["R12-5-NEVER_INVENT_NUMBER", "R25-1-OBSESSION_SATISFIES_ATTRACTION_GATE", "R52-26-GRIEF", "R71-44-FACULTY_READ_MAN"]))

ME = []

ME.append(q(
    "ME1", "Where the intimacy law lands",
    "How do your intimacy answers land in the repo?",
    "The style and combat laws each landed as a rule doc plus rewritten guides (R70-135, R71-102). Table Rule 9 lives only in NATALIE.md and two skills, which differ ('every movement' against 'every significant movement') and cite none of R49-51, R70-133 or R70-134. No Inventory has a courtship field.",
    [
        opt("A", "Rule doc only",
            "One dated Intimacy Law doc through log_ruling, served by load_rules. NATALIE.md, the skills and the Inventories stay as they are until a later pass."),
        opt("B", "Rule doc, Rule 9 rewritten",
            "A, plus Table Rule 9 in NATALIE.md rewritten to cite R49-51, R70-133, R70-134 and the new rows, and wotr-rp and the wotr-write scene pipeline brought to one wording."),
        opt("C", "B, plus the Inventories",
            "B, plus the courtship and mores fields drafted for the six cultures from these answers and entered on your word, and an intimacy section in the Dialogue Craft Standards and Scene Writing Process Guide."),
    ],
    "C",
    "Natalie reads NATALIE.md, the skills and the Inventories every session; a culture rule with nowhere to live is a rule nobody loads, which is why R70-135 and R71-102 both went the full distance.",
    depends=["CO1"],
    rules=["R70-135-WHERE_NEW_LAW_LIVES", "R71-102-WHERE_COMBAT_LAW_LANDS", "R70-45-NEW_STANDING_INVENTORY_FIELDS"]))

ME.append(q(
    "ME2", "Intimacy checks in verify_scene",
    "Which checks should verify_scene gain with this law?",
    "verify_scene has no explicit mode. Nothing checks scent, sound or mimetic words (Japanese gitaigo and their kin, which R70-133 bars from italics), the consequence Rule 9 owes, or a partner's age against the floor. R71-103 added a watch on the archive's tired fight devices; the archive's tired touches (the hand on the arm, the jaw held, the kiss on the hair) have none.",
    [
        opt("A", "An explicit mode",
            "verify --explicit WARNs when a scene has no smell word, no sound or mimetic word, or sets a mimetic word in italics (R70-133)."),
        opt("B", "A floor guard",
            "FAIL when an explicit scene names any character whose card gives an age under adulthood; WARN when a named partner has no adult age on card or roster. The floor becomes mechanical as well as absolute."),
        opt("C", "Consequence line owed",
            "WARN when an explicit scene's author notes carry no consequence line (a Ledger entry, a debt, a witness, a precaution ruled), since Table Rule 9 owes one."),
        opt("D", "Stale-touch watch",
            "WARN past one a scene on the archive's repeated touches: the hand on the arm, the jaw held, the kiss on the hair, as R71-103 does for fight devices."),
    ],
    "A,B,C,D",
    "B is the one check that guards the floor itself and costs nothing to run; A and C make Rule 9's clauses mechanical where a word count can see them, and D catches the habits the house survey counted.",
    multi=True,
    rules=["R70-136-NEW_CHECKS_VERIFY_SCENE", "R71-103-COMBAT_CHECKS_VERIFY_SCENE", "R48-45-CHECKS", "R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL"]))

ME.append(q(
    "ME3", "The intimacy sample bank",
    "What should the intimacy sample bank hold?",
    "R70-138 built a style bank of five beats per culture, and R71-104 gave combat a passage per culture plus a bank by fight type. No bank has an intimate beat, and the archive has no explicit scene; the nearest, The Blank Seal, stops at the threshold.",
    [
        opt("A", "An intimate beat per culture",
            "Each of the five style-bank files gains a sixth beat, intimate, in that culture's POV register (R70-134), from courtship to aftermath."),
        opt("B", "A bank by kind",
            "One new file with the kinds the archive has never written: a courtship, a first night, a marriage bed years in, a night across a Stage gap, a dubcon aftermath, a heartbreak."),
        opt("C", "Both",
            "A and B: culture beats where Natalie already loads them, and the kinds the archive lacks; this questionnaire's samples become their first drafts."),
    ],
    "C",
    "It is the answer R71-104 gave combat, for the same reason: the culture files carry register, and the kind bank fills what the archive has never tried.",
    rules=["R70-138-PROOF_ORDER_WORK", "R71-104-COMBAT_SAMPLE_BANK", "R70-134-KEYED_CULTURE_FREE"]))

ME.append(q(
    "ME4", "Proof and the test scene",
    "In what order does the work run, and who is in the test scene?",
    "R70-138 and R71-105 ran law and checks, then a test, amendment, then guides and bank. This test must prove Rule 9 and R70-134 at both ends: a blunt Kharven POV, an image-led Moto one. A test with your character leaves his body and choices to you; a canon couple puts the night into a book thread.",
    [
        opt("A", "Law, checks, NPC test",
            "Log the law and build ME2's checks; write one explicit test scene between adult NPCs on the Kharven ground of your thread, a Kharven POV with a Moto lover; amend; then guides, Inventories and bank."),
        opt("B", "Law, checks, played test",
            "The same order, but the test is played: your character with an NPC partner, Natalie writing only the partner and the room, and you writing him."),
        opt("C", "Law, checks, canon couple",
            "The same order, but the test is the night The Blank Seal broke off, Wren Greymane and Yūgiri Yukari, written in full as a book scene."),
    ],
    "A",
    "A tests both ends of R70-134 in one night with nothing canon at stake; a played test proves the turn shape only once the Keystones settle what is yours in bed, and the Blank Seal's stop is its point.",
    depends=["ME2"],
    rules=["R70-138-PROOF_ORDER_WORK", "R71-105-PROOF_ORDER_WORK", "R70-134-KEYED_CULTURE_FREE"]))

SETTLED = [
    {"point": "The floor: adults only, nothing sexual involving minors ever, no explicit sex on real living people, no bestiality; adult beastkin are people; flags inside the zone are false positives.",
     "rule_ids": [],
     "why_not_asked": "NATALIE.md, The Floor; fixed and never on a questionnaire. Every sample here is between adults, and no named minor appears in any role."},
    {"point": "Table Rule 9's clauses: plain anatomical vocabulary, clinical specificity, positions tracked, arousal scents layered, onomatopoeia committed, the NPC's own desire and refusal line, a consequence afterward, dubcon and non-con at the same specificity, aftermath never skipped.",
     "rule_ids": [],
     "why_not_asked": "Standing table law in NATALIE.md; ME1 asks only where it is rewritten, and ME2 only what verify_scene checks of it."},
    {"point": "Explicit narration is plain and crude: working-man anatomical words, lush in sensation, blunt in naming.",
     "rule_ids": ["R49-51-EXPLICIT"],
     "why_not_asked": "Ruled 2026-09-26 and re-affirmed by the style law; the CO13 samples obey it."},
    {"point": "Season imagery, the held detail at the peak, the poem after, and mimetic words romanised and never italic, beside the plain words.",
     "rule_ids": ["R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL"],
     "why_not_asked": "XS1 of the style law, 2026-10-03. CO3 asks only whether letters also court."},
    {"point": "The POV's culture keys the technique in bed; the lover's culture shows in what they do and say.",
     "rule_ids": ["R70-134-KEYED_CULTURE_FREE"],
     "why_not_asked": "XS2 of the style law. CO2 to CO7 ask only the customs that give the lover's culture something to do and say."},
    {"point": "Courtly cultures offer and answer verse at rites and in court, a plain answer costing face; each culture's verse form goes in its Inventory.",
     "rule_ids": ["R70-110-VERSE_EXCHANGED_TALK"],
     "why_not_asked": "Ruled 2026-10-03. CO3, CO5 and CO6 ask only whether verse also courts."},
    {"point": "Pressure shows in the room before the body; suppression costs the suppressor's body, leaks and sags a gauge; the unwoken feel a practitioner by the Aura table by Grade.",
     "rule_ids": ["R70-69-PRESSURE_AURA", "R71-43-SUPPRESSION_PAGE", "R71-41-PRESSURE_UNWOKEN"],
     "why_not_asked": "Style and combat law. CO12 and CO13 ask only what these mean between lovers."},
    {"point": "Medicine by place and purse: Guild cities have their decade's medicine, the north and the poor the barber and folk remedies.",
     "rule_ids": ["R53-10-MEDICINE", "R71-79-MEDICINE_PLACE_PURSE"],
     "why_not_asked": "Settled; CO11 asks only whether conception and the pox are tracked."},
    {"point": "Every live thread keeps a standing warm bond written openly warm; joy may have scenes; grief goes back to the root; tears break once per arc at a small thing.",
     "rule_ids": ["R70-114-GRIMDARK_WARMTH", "R52-26-GRIEF", "R52-27-JOY", "R70-115-TEARS_SENTIMENT"],
     "why_not_asked": "Style and voice law. CO14 asks only whether lovers count as the warm bond, CO16 only the balance of lived and mourned."},
    {"point": "No invented number; a bond prints no figure until canon holds one.",
     "rule_ids": ["R12-5-NEVER_INVENT_NUMBER"],
     "why_not_asked": "Standing law; CO15 D and CO17 are written with no figure."},
    {"point": "Obsession Force satisfies an Attraction gate; a Sacrament anchor is fixed by declaration whether or not the anchor consents.",
     "rule_ids": ["R25-1-OBSESSION_SATISFIES_ATTRACTION_GATE", "R29-1-SACRAMENT_BOND_ANCHOR_BY_DECLARATION"],
     "why_not_asked": "Ruled 2026-09-12; CO10 and CO17 build on them and do not reopen them."},
    {"point": "A recurring rival's survival is paid for on the Ledger with a debt, a scar or a witness.",
     "rule_ids": ["R70-104-RIVAL_BOND"],
     "why_not_asked": "Style law; CO10 B applies it to rivals in love."},
    {"point": "Each Inventory owes fields for law and punishment and succession; succession follows each culture's law.",
     "rule_ids": ["R70-45-NEW_STANDING_INVENTORY_FIELDS", "R60-21-SUCCESSION_BY_CULTURE"],
     "why_not_asked": "Already law; CO1 adds only the courtship field and CO8 fills the law field for keeping more than one partner."},
    {"point": "Every sum on the page is quoted from the approved price table, payment in kind named exactly.",
     "rule_ids": ["R70-48-MONEY_PRICE_PROVENANCE", "R53-07-PRICE_TABLE"],
     "why_not_asked": "Settled; bride-prices, settlements and allowances in these answers take their sums from the table, and no question sets a price."},
    {"point": "An intimate uses the personal name; the narrator does not switch names without a reason.",
     "rule_ids": ["R20-5-ON_THE_PAGE"],
     "why_not_asked": "Naming law; a courtship's change of name is already governed by it."},
    {"point": "A player's fighter: wounds as world facts, the tell placed and the read his, outward cost only; standing orders run to the first uncovered branch.",
     "rule_ids": ["R71-6-PLAYER_FIGHTER_PAGE", "R71-5-ROLEPLAY_TURNS_AGAINST_WRITTEN"],
     "why_not_asked": "Combat law, fight scope only; this section does not extend them to the bed."},
    {"point": "Roleplay turns in present tense, written scenes in past; third person only.",
     "rule_ids": ["R49-02-TENSE", "R70-12-FIRST_PERSON"],
     "why_not_asked": "Settled; every sample here is a written scene in past tense, third person."},
    {"point": "The order of proof: law, test scene, amendment, then the bank.",
     "rule_ids": ["R70-138-PROOF_ORDER_WORK", "R71-105-PROOF_ORDER_WORK"],
     "why_not_asked": "Precedent from both earlier laws; ME4 keeps the order and asks only who is in the test."},
]

data = {"sections": [
    {"key": "CO", "title": "Courtship and bonds",
     "intro": "How people court, marry, keep, lose and grieve each other, culture by culture, and what love does across a Stage gap or under Pressure. The explicit register itself is settled law (R49-51, R70-133, R70-134); this section gives it customs to show.",
     "questions": CO},
    {"key": "ME", "title": "Method",
     "intro": "How the intimacy answers become law and get proved: where they land, what verify_scene learns to check, what the sample bank holds, and the test scene.",
     "questions": ME},
], "settled": SETTLED}

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(OUT, sum(len(s["questions"]) for s in data["sections"]))
