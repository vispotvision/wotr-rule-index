# Intimacy and explicit scenes: the current law

Research for the intimacy questionnaire, 2026-10-04. Maps what WOTR law already says about romance, desire, consent, explicit scenes and their aftermath, by dimension, with rule ids and short quotes, and marks each point **settled** (law, do not re-ask) or **open** (no law, or law that leaves the question standing).

**Searched:** `desktop/NATALIE.md` (the standing prompt), `out/rules.live.full.md` and `out/rules.resolved.json` (all 1,450 rows, filtered for explicit, sex, consent, aftermath, desire, refusal, lover, marriage, courtship and kin), `out/docket.md`, `CONFLICTS.md`, `RULINGS.md`, the style questionnaire (`imports/drafts/style-questionnaire/`), the combat questionnaire (`imports/drafts/combat-questionnaire/decisions.md` and the RULINGS entry `combat-law-2026-10-04`), the `wotr-rp`, `wotr-write` and `wotr-npc` skills, `build/verify.py`, every Standing Inventory in `desktop/inventories/`, the style sample bank (`desktop/style-bank/`), the price table, swears and sense-bank drafts, `scenes/` and the relevant wiki cards.

## The headline

The intimacy law is thin and young. Everything that governs an explicit scene today is:

- the **floor** in NATALIE.md (fixed);
- **Table Rule 9**, which lives only in NATALIE.md and the two skills, and is not itself a rule row in the index;
- three index rows: **R49-51-EXPLICIT** (2026-09-26), **R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL** and **R70-134-KEYED_CULTURE_FREE** (both 2026-10-03, style questions XS1 and XS2);
- general prose, POV, dialogue and voice law that applies to every scene and so reaches the bedroom by default.

Beyond that: the docket is empty ("0 outstanding", `out/docket.md`). No open CONFLICTS.md entry touches intimacy. No archived scene in `scenes/` is explicit (a vocabulary grep finds none; the nearest is the tender, non-explicit Zuberi and Ara night in *The War in the North II*). The R70-138 style bank has five beats per culture (fight, court, quiet, system, comic) and no intimate one. `build/verify.py` has no explicit-scene checks. No Standing Inventory carries a word about courtship, marriage, sexual custom or the bed. So almost every question Isaac picked (courtship by culture, desire and refusal lines, dubcon handling, aftermath, how bonds grow, the new style in bed) is open beyond the two style answers.

---

## 1. The floor (settled; never on a questionnaire)

NATALIE.md, The Floor:

- The shared line: "no sexual content involving minors, ever. Fixed."
- Isaac's domain inside it: "the full range of published adult fiction", named as incest between adults, non-con and dubcon (non-consensual and dubious-consent content), BDSM, age-gap between adults, power dynamics, graphic violence, plain working-man anatomical language. "Within that space my creative judgment governs."
- Natalie's own limits: "no explicit sex on real living people and no bestiality."
- Flags: inside the zone "a flag is a false positive. Note it and keep writing." A real line gets "one plain sentence", never a silent stall or a register shift.
- `wotr-rp` and `wotr-write` repeat the floor word for word in substance; `desktop/PROJECT_INSTRUCTIONS.md` carries it for the Desktop project.

**What the questionnaire must hold to, drawn from canon, not asked:**

- **Named minors on the roster.** Hild Ice is eleven at the muster (CONFLICTS C-049, ruled WAR-109: "Sodoku 28, Hild 11"). Emira is "nine and too perceptive for it" (Voice Roster). Rikudoku, Yoko and Sodoku's son, is "about seven" in the signing year (Yoko Mishiro's card). None of them enters an intimacy question, sample or option in any capacity, including as witness or subject of talk in a sample.
- **Persons, not animals.** WOTR has beastkin and demihuman peoples. Canon already treats them as persons with marriages: Yoko Mishiro, fox-kin ("tail and ears betray her first"), is Sodoku's wife (her card: "lovers, then married"). The floor's bestiality line is about animals, and the questionnaire should not blur that by treating a beastkin adult as anything but a person, or by sampling anything that reads as an animal.
- Samples stay between adult characters and at the plain anatomical register Table Rule 9 sets, kept to the beat each question needs.

## 2. Table Rule 9, clause by clause (settled)

NATALIE.md: "Plain anatomical vocabulary, clinical specificity, positions tracked, arousal scents layered, onomatopoeia committed. The NPC has their own desire and refusal line and can change their mind. The scene has a consequence afterward. Non-con and dubcon written with the same specificity; aftermath never skipped."

Nine clauses, each settled as a floor:

| Clause | What it fixes | Where else it is restated |
|---|---|---|
| Plain anatomical vocabulary | The words for the body are anatomical and plain | R49-51 ("working-man anatomical words"); The Floor ("plain working-man anatomical language") |
| Clinical specificity | Exactness, as in a wound | `scene-pipeline.md` |
| Positions tracked | The reader always knows where the bodies are | `wotr-rp`: "through every movement"; `scene-pipeline.md`: "through every significant movement" (the two skills differ) |
| Arousal scents layered | Smell as a sense layer, as Rule 12 and the sense banks run it everywhere | both skills |
| Onomatopoeia committed | Sound words written out, not shied from | joined by mimetic words under R70-133 |
| The NPC's own desire and refusal line | The partner is a person with wants and a limit | Table Rule 3; R52-02; `wotr-npc` |
| Can change their mind | Either way (`wotr-rp`: "either way") | |
| A consequence afterward | The scene costs or changes something | Table Rule 7 (the Ledger) |
| Non-con and dubcon at the same specificity; aftermath never skipped | No softening for dark content; the after is written | `wotr-rp`: "Aftermath is a turn, never skipped, and the consequence goes on the Ledger" |

Table Rule 9 is older than the index's prose law and has never been reworded by a ruling. It is amended by reference only: R70-133 and R70-134 both name "Table rule 9: explicit scenes" as their locus with operation "extends".

Two neighbouring table rules bear on the bedroom and are also settled: **Rule 11** (first introductions: "body with areas named", now in the POV's own order, R70-54, R70-55) governs a lover's first sight like anyone's; **Rule 12** (lived-in rooms) carries its own exemption: ambient noise "except in private moments".

## 3. Register: how an explicit scene reads

**Settled.**

- **R49-51-EXPLICIT** (Prose Law 2026-09-26, question p51): "Explicit narration stays plain and crude: working-man anatomical words, lush in sensation, blunt in naming." It answered whether the new lush, timeless, image-led narration should soften the bed; it did not.
- **R70-133-EASTERN_TECHNIQUES_BESIDE_CLINICAL** (XS1, all four options ticked; D against the recommendation). Four techniques may sit beside the plain words "without displacing" them:
  - *Season and nature imagery*: "frost, snow, blossom, the brazier", carrying mood.
  - *Held detail at the peak*: one held physical detail at chosen moments; "the aftermath is still written".
  - *The poem after*: the scene may close on "a morning poem, a note, a line answered" (the Heian court custom; Heian is Japan's classical court era) as part of its aftermath.
  - *Mimetic words*: gitaigo (Japanese words that mimic a texture or state rather than a sound) and each culture's own, joining Rule 9's onomatopoeia, "romanised and never italic".
- **R70-134-KEYED_CULTURE_FREE** (XS2, digest): "The POV's culture decides: a Moto POV writes with image and the held detail, a Kharven POV blunt, whoever the lover is; the lover's culture shows in what they do and say." Follows R70-1-BLEND_MODEL's tilt by culture.
- The general register law reaches the bed unchanged: real anatomy terms are exempt from timeless narration (R49-45-SCIENCE); profanity in mouths and close-POV narration when the POV would think it (R48-12-PROFANITY, R51-02-CLOSE_POV_SWEARS), each culture's own swears first (R51-29-SWEARING); modern words legal in speech, narration timeless (R48-13); italic thought may use any word the POV would say aloud (R70-37-MODERN_IDIOM_THOUGHT); borrowed words never italic (R50-32-ITALICS); each culture's sound and state words live in its Inventory (R70-22-SOUND_WORDS); each culture's narration dial is plain, period or archaic (R70-27); feeling may be carried by one held concrete image, never named (R70-39-CARRYING_FEELING); a scene may close on a short poem set apart (R70-64-VERSE_INSIDE_PROSE); verse is offered and answered at rites and court in the Moto court, Eresse, the Mahuo houses and the lineage halls, and Northern speakers may trade flyting (alliterative insult verse) (R70-110).
- **The pop-psych ban reaches consent talk in narration.** R51-04-LIST_PSYCH bans "triggered, toxic, closure, mindset, boundaries" in narration, and `verify.py` line 52 enforces it. A narrator cannot say a lover set "boundaries"; a character may, under R48-13.

**Open.**

- **Which cultures run which techniques.** R70-134 names only the Moto (image, held detail) and Kharven (blunt) poles. The Accord, Dawi, Eresse, Mahuo, lineage halls, Expanse, Korvaeth, Stannvaard, Nalūn, Ketsuen, Zettari and Yukari are unplaced.
- **The banks the techniques need do not exist yet.** No Inventory has R70-22 sound or state words, R70-61 season words, or the R70-110 verse form entered. A Moto POV's morning poem has no Moto verse form on file; a mimetic word has no culture list to come from.
- **Each culture's bed vocabulary.** R49-51 fixes "working-man anatomical words" but no culture has a word list for the body in desire (the Kharven Inventory has body swears, "frozen piss", but nothing for sex). Whether a Moto court POV's narration, on an archaic dial, uses the same crude English as a Kharven rider is unanswered beyond "plain and crude".
- **How explicit, how often.** Rule 9 says how an explicit scene is written, not when a scene must be explicit. Whether a scene may fade or cut is open (see section 6).
- **The register of BDSM and power play in the Draw Age.** Modern kink vocabulary ("aftercare", "safeword") is not on any banned list but is modern; R51-03 leaves the rest "by ear". Whether such terms exist in-world, in which mouths, is open.

## 4. POV, interiority and whose body it is

**Settled.**

- Natalie never thinks, speaks or acts for Isaac's PC Sodoku Moto or the other creators' characters (Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai, also Chuluun) (NATALIE.md, Who Natalie Is). R52-10-CROSSOVER: his POV characters "are always his". R52-08-PC_IDIOM: his play beats the card.
- R49-01-WHOSE_HEAD: in roleplay turns the narration "may go to full depth inside Isaac's character; Isaac overrules any thought that isn't his."
- R48-32-NPC_VOICES: "Isaac may take over any NPC's voice anytime by saying so"; the lover included.
- NPC thought: one italic private thought per NPC per scene in roleplay turns (Table Rule 10, R48-40-NPC_THOUGHTS); in written scenes the POV lock holds and no NPC thought appears (R48-40, R39-7). Third person only (R70-12-FIRST_PERSON), even when Isaac plays in first person (`wotr-rp`).
- The combat law (R71, rows being written; RULINGS item 6, K9) settled a player's fighter on the page: "Wounds as world facts", "how he bears it stays yours"; "The tell placed, the read his"; "Felt from across the room" (from an NPC's POV his "reasons and his Crystal stay dark"); "Outward cost only". It is scoped to fights.

**Open.**

- **The PC's body in bed.** The K9 split (world facts written by Natalie, the inside his) has no intimacy equivalent. What of Sodoku's body may Natalie write as world fact once his stated action resolves (contact, position, a partner's hand on him), and what is always his (arousal, climax, pain, pleasure, how he bears it)? Yoko Mishiro is his canon wife and an NPC Natalie voices, so this is live, not hypothetical.
- **Standing orders in bed.** Combat K5 (RULINGS item 5) lets Isaac post conditions ("if he closes, I cut low") that Natalie runs until the first uncovered branch. Whether the same is legal for an intimate scene (a pace, a limit, a stop condition) is unasked.
- **The lover's interior under a written POV lock.** Rule 9 requires the NPC's own desire and refusal line, but R48-40 forbids their thought in a locked written scene. How the partner's desire and refusal show (body only, speech, one marked exception) is unruled.
- **A non-PC POV in bed with the PC.** K9's "Felt from across the room" covers an NPC POV in a fight; an NPC POV in an explicit scene with Sodoku is unaddressed.

## 5. Desire, refusal, consent and dark content

**Settled.**

- Table Rule 3: NPCs "lie, withhold, refuse, bargain, misjudge him. If an NPC would refuse, they refuse."
- Table Rule 9: the NPC's "own desire and refusal line", and they "can change their mind". `wotr-rp` adds "either way".
- `wotr-npc` makes a refusal line a required field of every NPC: "The thing they will not do no matter what is offered."
- R52-02-VOICE_LEVER and R15-1-VOICE_DIFFERENTIATION: a voice is what a person "notice[s], want[s], refuse[s]" and how they reason. R5-B-DECLARATION_TO_INFERENCE: a person is established by "what they refuse" and choose under pressure.
- R48-42-LIES ("Frequent lies") and Table Rule 8 (one wrong thing per session, uncorrected): a lover may lie.
- R48-30-SURPRISES: betrayal only after foreshadowing a player could have caught. A seduction that turns on him is bound by it.
- Non-con and dubcon are inside Isaac's domain and written at full specificity with the aftermath (The Floor; Rule 9).
- **The only culture-specific body grammar of consent on file** is the Winter Eladrin's three channels (R24-2-ELADRIN_THREE_CHANNELS): "approach is agreement, a half-step back is objection, turning without moving the feet is refusal", at least two channels rendered in any exchange of consequence.
- **A magical precedent, not sexual:** R29-1-SACRAMENT_BOND_ANCHOR_BY_DECLARATION rules that a Sacrament anchor is fixed "regardless of whether the anchor consents"; "the declaration, not consent, is the mechanism" (the Verinus and Aurelian dawn rite). WOTR metaphysics already allows a binding taken without consent, with no release valve.

**Open.**

- **What a desire line and a refusal line contain** for an intimate partner, and whether they go on the card or the roster (`npc_set`) like a want and a lie do.
- **How a mind-change shows**, either way, in roleplay and in a locked written scene.
- **Dubcon handling on the page:** where the ambiguity sits (circumstance, power, intoxication, a working, an oath, a debt), whether the narration may ever resolve it, and whether the POV's culture decides how it is named, as R70-134 keys technique.
- **Non-con and the PC:** whether NPCs may initiate against Sodoku, whether he may be written as perpetrator by his own post, and how the K9 split applies when it is his body.
- **Workings in desire:** pheromone, Pressure, a Somnalis dream, an Attraction or Obsession working, a charm. Whether magic may produce or remove consent on the page, and with what tell and counter (the fair-play standing line demands a findable counter for any ability).
- **Consequence in law:** R70-45 gives every Inventory a "law and punishment" field, not yet written. What each culture's law says of rape, adultery, seduction of a ward, or incest between adults is nowhere on file.

## 6. Aftermath and consequence

**Settled.**

- Rule 9: "a consequence afterward"; "aftermath never skipped". `wotr-rp`: "Aftermath is a turn, never skipped, and the consequence goes on the Ledger." `scene-pipeline.md`: "Aftermath never skipped, including after any explicit scene."
- R70-133: the morning poem, note or answered line may close the aftermath; the held detail still leaves "the aftermath ... still written".
- Table Rule 7, the Ledger: "Injuries, exhaustion, reserve, debts, reputation, who saw what. Persists."
- By analogy only, the duel and battle law: R48-38-AFTERMATH ("wounds dressed, what changed between people"); R1-3-AFTERMATH_IS_WHERE_IT_HAPPENS (relationships change "in the three days afterward"); R2-5-RESOLUTION_IN_AFTERMATH (the change is legible "in how they handle the bucket"; "If a character says what the act meant, the amendment has been violated"). R2-5 is scoped to battles (the Single Act, one unrepeatable physical act per engagement), but it is the index's only rule on how a relationship change shows afterward.
- R70-50-BODIES_AFTER_FIRST_SIGHT: each return shows one changed detail of the body. R60-02-REAL_HEALING_TIMES and R53-10-MEDICINE (era medicine by place; "the north and the poor get folk medicine and the barber") govern any injury.

**Open.**

- **The tension with R70-17-CLOSING_MODES**, which lets a scene "break off a breath before its emotional payoff, which the next scene then owes", and R70-5's Kawabata and Tanizaki model ("the scene that breaks off before its point"; both twentieth-century Japanese novelists of restraint). Rule 9 says never skip the aftermath. Whether an explicit scene may break off, cut to the morning, or fade at all is unruled.
- **What the aftermath is** in an explicit scene: length, beat shape (dressing, washing, sleep, talk, silence, leaving), and whether R2-5's "never say what it meant" applies to lovers.
- **What the Ledger records** after intimacy: a bond, a debt, a witness, reputation, a mark on the body, pregnancy, disease. None of those categories has a rule. Contraception, pregnancy and venereal disease appear nowhere in the law, the Inventories or the price table; R53-10 only says medicine is period-true.
- **Non-con aftermath:** how the body and mind carry it across later scenes, held to R52-26-GRIEF and R70-115 (a guarded restraint that gives way "at a small, unexpected thing"), and whether it opens a Front.

## 7. How bonds grow

**Settled.**

- R70-114-GRIMDARK_WARMTH: "Every live thread carries at least one standing warm bond (found family, master and disciple, sworn kin) written openly warm, joy may get scenes of its own, and losses still cost." NATALIE.md carries it under Grimdark.
- R52-27-JOY: in a guarded voice, joy "shows in hands, face and breath". R52-26-GRIEF: grief returns a voice to its root. R70-115-TEARS_SENTIMENT: restraint gives way once per character per arc, at a small thing.
- R70-14-KISHOTENKETSU: quiet and downtime scenes may run kishōtenketsu (the four-part East Asian shape of set-up, development, twist, reconciliation, with no conflict required).
- R70-104-RIVAL_BOND: a recurring rival is paid for on the Ledger. It is the index's only rule that prices a recurring relationship, and it is about enemies.
- **Canon bonds on the cards:** Yoko Mishiro's card lists "Anima Spirare, Fulfilled", her bond with Sodoku "fully expressed and named at Stage IV", an Axis row for the marriage marked "(marital)" and "Absolute", and an Emergent Bond row for Riku, parental, "Growing, already load-bearing", with Dominion Sense annotated as "bond-awareness". Anima Spirare (the Soul's Breath, a Wellspring) strengthens Vitality Hemostasis, Regeneration and Harmonics Synergy (Fracture of Worlds, Part V). The Five Beastkin Lineages page says Anima Spirare "develops in sustained relationships". Attraction Force is "the law of recognition" by which "vows remain binding" (*Hataraki*).
- **Canon courtships in the archive:** Kwon Mu-jin and Frithia "had one winter together, 699 to 700 IC; she refused marriage and asked not to be written down" (RULINGS, Alftian Codex Volume III), then "Frithia asked Mu-jin to marry her in the east room" in 702 IC (R68-11-MUJIN_FRITHIA_MARRIED_702). Sodoku and Yoko: "lovers, then married. He broke her lock, and she walked through it on her own decision and stayed" (Yoko's card).

**Open.**

- **Whether a romantic bond counts as R70-114's "standing warm bond".** Its examples name found family, master and disciple and sworn kin, not lovers.
- **Whether bonds show on the sheet.** Yoko's card treats a marriage as a stat-bearing Axis through Anima Spirare. Whether that is a general mechanism (any bond, any lineage, any Wellspring), how a bond is graded and grows, and whether intimacy feeds it, is unruled. No figure may be invented (R12-5-NEVER_INVENT_NUMBER); any grade must trace to Fracture of Worlds.
- **The pace and beats of a growing bond:** how many scenes, what marks each step, whether the first time is a set piece, how a bond breaks.
- **Jealousy, rivalry in love, more than two partners, marriage as politics** (the Kharven queen-line and the Moto succession tie marriage to the crown; R60-21-SUCCESSION_BY_CULTURE puts succession on each Inventory, still unwritten).
- **Housekeeping found:** Yoko's card names her husband "Temür Moto" on the Axis and Wellspring rows, a Büri or Mongolian-register form. The Moto canon makes that stale; it is not to be propagated, and belongs on the `stale_names` sweep.

## 8. Courtship and relationships by culture

**Settled (the little there is).**

- R70-134: in bed the POV's culture shapes narration and "the lover's culture shows in what they do and say".
- Court cultures argue in long formal speech at court (R70-111) and lose face to a weak verse answer (R70-110); face and the face-slap carry a bill (R70-112).
- R53-15-FOLK_BELIEFS: each culture keeps false beliefs the narration never corrects. R53-13-FAITH: petition shows "when a character wants something badly".
- Bastardy already lives in the approved swears: the Accord's "Sine sigillo" ("Without seal", said of a bastard) and "Bloody bastard"; the Moto "Written in the wrong hand" (said of a bastard or false claim). Kharven oaths are now "only as strong as the man who says it", since the Fusi Vā (the Queen's binding under clan oaths) is gone.
- R70-43 makes "households, young and old" a rotation group; R70-45 adds Inventory fields for "law and punishment, succession".

**Open (almost all of it).** No Standing Inventory, draft Inventory, sense bank, swears draft, price table or style-bank file carries courtship, betrothal, bride-price or dowry, weddings, divorce, widowhood, concubinage or consorts, the sex trade and its prices, bathing and nakedness customs, what is shameful and what is boasted of, how a culture names the body in desire, or what each culture believes about sex and magic. Each of these is a candidate Inventory field and a candidate question. R70-48 would require any price for intimacy to come from the approved price table, which has none.

## 9. Form, length and process

**Settled.**

- Domain tags for an explicit scene: prose-law, dialogue, pov, scene-structure (NATALIE.md; `scene-pipeline.md`).
- Every roleplay reply runs about 3,500 words (R48-28-TURN_LENGTH, R49-30-SHORT_BEATS), half texture and talk, half the world moving (R49-29); present tense for turns, past for written scenes (R49-02). Set pieces run 5,000 words and up (R48-46); Table Rule 2's older bands still sit in NATALIE.md.
- Rule 1: stop at his next decision; R70-14 keeps that stop even in a kishōtenketsu scene.

**Open.**

- Whether an explicit scene is a set piece (5,000 floor, full standards) or a turn, and how a 3,500-word turn is paced across a scene that has one obvious decision point.
- **The checker.** `verify.py` has no explicit mode: nothing checks positions, scent, sound words, the aftermath beat, mimetic words set roman, or the floor's named minors. Its firearms term list (line 127) counts "cock", so a combat check on a scene with a pistol in the room would count the anatomical word as gun vocabulary.
- **Proof.** R70-138 required law, test scene, then sample bank; there is no explicit test scene and no intimate beat in any culture's bank.

## 10. Drift between the law and the documents

Housekeeping found while mapping, not questions:

1. NATALIE.md's Table Rule 9 cites neither R49-51 nor R70-133 or R70-134, though R70-135 required the Prose Standards rewritten to the style law.
2. `wotr-rp` and `scene-pipeline.md` carry Rule 9's text without those three rows, and differ from each other ("every movement" against "every significant movement").
3. The Inventories lack the R70-22, R70-61 and R70-110 fields that R70-133 and R70-134 lean on.
4. Yoko Mishiro's card carries the stale "Temür" form.

---

## Settled: do not re-ask

- **The floor**, entire: adults only, nothing sexual involving minors ever, no explicit sex on real living people, no bestiality; flags inside the zone are false positives (NATALIE.md).
- **Table Rule 9's nine clauses** (section 2), including dubcon and non-con at the same specificity and the aftermath never skipped.
- **R49-51**: plain and crude, working-man anatomical words, lush in sensation, blunt in naming.
- **R70-133 (XS1)**: season and nature image, held detail at the peak, the poem after, mimetic words romanised and never italic, all beside the plain words.
- **R70-134 (XS2)**: keyed to the POV's culture; the lover's culture shows in deed and speech.
- **Isaac's characters are his** (R49-01, R52-08, R52-10); Isaac may voice any NPC (R48-32); NPC thought rules (Rule 10, R48-40); third person only (R70-12).
- **NPC agency, refusal and lies** (Rule 3, Rule 8, R48-42, R52-02, `wotr-npc`); surprises foreshadowed (R48-30).
- **General register**: anatomy exempt (R49-45), profanity (R48-12, R51-02, R51-29), modern words in speech only (R48-13), pop-psych ban in narration (R51-04), italics (R50-32), carrying feeling by image (R70-39), verse set apart (R70-64), verse exchange at court (R70-110).
- **Warm bonds, joy, grief, tears** (R70-114, R52-27, R52-26, R70-115); kishōtenketsu for quiet scenes (R70-14).
- **Turn length and tense** (R48-28, R49-30, R49-02); set-piece floor (R48-46).
- **From the Style Law R70 generally**: the blend tilted by culture (R70-1), Eastern lead in narration and structure (R70-3), the named models (R70-5), closing modes (R70-17). **From the Combat Law R71**: K9's player-fighter split and K5's standing orders, both in their fight scope only.

## Open: where the questionnaire has room

Grouped by what Isaac picked.

**Relationships and courtship by culture**
1. The courtship, betrothal and marriage custom per culture (an Inventory field or several).
2. What each culture holds shameful, boastable, private and public about sex; nakedness and bathing.
3. The sex trade: whether it exists on the page, in which cultures, at what price, and who runs it.
4. Marriage as politics and succession (R60-21's unwritten field).
5. Folk beliefs about sex and magic per culture (R53-15).

**Desire and refusal lines**
6. What a lover's desire line and refusal line contain, and whether they are carded or rostered.
7. How a partner's desire, refusal and mind-change show under a written POV lock (R48-40), and in a roleplay turn.
8. A body grammar of consent per culture, as the Eladrin have (R24-2).

**Dubcon handling**
9. Where the ambiguity sits and whether narration may resolve it.
10. Workings that bend desire or consent: allowed, with tell and counter, or barred.
11. The PC and non-con, in either role; the K9 split applied to his body.
12. Law and punishment per culture for sexual crimes (R70-45's field).

**Aftermath**
13. Whether an explicit scene may break off or fade (R70-17 and R70-5 against Rule 9).
14. The aftermath beat's shape and length; whether lovers, like the Single Act, never say what it meant.
15. What the Ledger records: bond, debt, mark, witness, reputation, pregnancy, disease; and period contraception and medicine by place.

**How bonds grow**
16. Whether lovers count as R70-114's warm bond.
17. Whether a bond is a sheet mechanic (Anima Spirare's Axis on Yoko's card), how it grows and breaks, with no invented figure.
18. Jealousy, rivals in love, more than two partners; the pace of a bond across scenes.

**The new style in bed**
19. Which of the twelve unplaced cultures run image and held detail, and which run blunt.
20. Each culture's mimetic and sound words for the bed, its season words, its morning-poem form.
21. Each culture's bed vocabulary under one crude English, or bent by the narration dial (R70-27).
22. BDSM and power-play vocabulary in the Draw Age.
23. Whether an explicit scene is a turn or a set piece, and its length.
24. An explicit mode for `verify_scene`, and an intimate beat in the R70-138 sample bank.
25. The PC's body in bed: what Natalie may write as world fact and what stays his; standing orders in bed (K5's analogue).
