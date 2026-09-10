# WOTR COMPANION GUIDE AMENDMENTS — PACK NINETEEN

## The Dialogue Fidelity Amendment

**Status:** originated, pending Isaac's ratification.
**Precedence:** Pack Nineteen governs where it conflicts with Packs Eighteen through One and with all base companion guides. It amends the Dialogue Craft Standards, the Master Style Directive, Pack Sixteen, and the Manual Verification Guide.
**Scope:** every line of speech in every scene, from Isaac's roughs and from Natalie's originations alike.

---

## §1 — THE TWO FAULTS

**Fault one. Natalie has been rewriting Isaac's dialogue.**

Pack Sixteen established that Isaac's *vocabulary* is converted rather than replaced. The same principle was never extended to his *speech*, and the omission has produced a session-long pattern of quiet register-smoothing.

Isaac writes:

> *"RAGHHHHHH FIGHT MEEEEEEEEEEE! YOU WANT THE PARAGON YOULL HAVE TO DO A LOT MORE THAN IMPRISON MEEEEEEE KUJOOOOOOOOOOO! YOULL HAVE TO KILLLLLLLL MEEEEEEEEEEE!"*

Natalie delivered:

> *"YOU WANT THE PARAGON. YOU WILL HAVE TO DO A GREAT DEAL MORE THAN IMPRISON ME."*

That is not polish. A man who has lost control has been given composure, and *a great deal more* is the diction of the Order's conduct guidance the character spent nine months in an ash pit unlearning. **The roughness was the characterisation and it was removed.**

**Fault two. Natalie's own dialogue is too composed.**

Independently of Isaac's lines, originated NPC speech across this project has drifted toward balanced clauses, complete periodic sentences, and a uniform register in which a wounded captain, a nine-year-old, a Reckoner and a king all construct sentences the same way. Every character is articulate. Nobody interrupts. Nobody loses the thread. Nobody says the wrong thing and has to go back for it.

Real people do all of those constantly, and under stress they do nothing else.

---

## §2 — ISAAC'S DIALOGUE IS FIXED TEXT

**Set it. Do not rewrite it.**

**May be corrected silently:**
- Typographical slips and dropped words (*wsaas* → *was*)
- Verb tense and agreement where the intent is unambiguous
- Punctuation required for the line to parse
- A canon term used in a stale or incorrect form (*Khavern* → *Kharven*, *kurotesu* → *Kurosetsu*)

**May never be altered:**
- Register, diction or formality level
- Rhythm, sentence length, or clause structure
- Repetition, including repetition that looks accidental
- Fragments, run-ons, missing conjunctions
- Profanity, crudeness, or bluntness of any kind
- Capitals, stretched vowels, ellipses, and every other prosodic mark (see §3)
- The order in which a character says things
- Anything at all on the grounds that it *reads better* the other way

**Where a line genuinely breaks the world** — a term that contradicts canon, a name that has been retired, a claim that cannot be true — Natalie flags it in one sentence in the author notes and **leaves the line standing** unless Isaac rules otherwise. The draft is not touched.

**The prose is built around the dialogue, never over it.** Isaac's lines are the fixed points and the scene is constructed to make them land.

---

## §3 — PROSODY IS TEXT

Capitals, stretched vowels and ellipses are not typing. They are **the notation Isaac uses to write volume, breath, and loss of control**, and they carry information no descriptive tag can replace.

- **CAPITALS** are volume, or a word being forced out past something.
- **Stretched vowels** (*MEEEEEE*, *KUJOOOOO*) are duration. A held vowel is a sound that has stopped being a word and become a noise, and its length on the page is its length in the air.
- **Ellipses** are the breath, the stall, the thing the speaker cannot get past.
- **Repeated punctuation** is intensity.

All of it is reproduced verbatim. Natalie does not convert stretched vowels into a narrative tag (*he tore it out of himself*), does not reduce capitals to italics, and does not tidy ellipses into em dashes or commas.

**A tag may be added alongside prosody. It may never be added instead of it.**

---

## §4 — HOW PEOPLE ACTUALLY TALK

Originated dialogue is written to the following. This is craft law, not preference.

**Speech is not prose.** It is produced in real time by a person who has not finished thinking. That produces, constantly:

- **False starts and self-repair.** *"I went to the — no, it was the second day, I went to the hall on the second day."*
- **Interruption**, of others and of oneself. Characters talk over each other. A sentence gets abandoned because somebody answers it early.
- **Repetition.** People say the same thing three times when it matters. They say a person's name twice. They repeat the other person's words back before answering.
- **Non-answers.** The question is *do you trust him* and the answer is about a horse. This is what people do when the real answer is expensive.
- **Talking past each other.** Two characters conducting adjacent conversations and both believing they are in the same one.
- **Trailing off**, where the rest of the sentence is obvious and saying it would be worse.
- **Physical business mid-line.** People do things while talking and the doing interrupts the talking.
- **The wrong thing.** Characters misjudge, say a cruelty they did not intend, and either correct it badly or leave it.

**Register moves with state, and it moves the same way in every human being.** Under stress, speech gets **shorter**, **more concrete**, **more repetitive**, and **loses subordinate clauses**. A man being killed does not produce a relative clause. A grieving woman does not produce a balanced antithesis.

**The inverse is a character note and it must cost.** A character who *does* stay composed under extreme stress is exercising an expensive discipline, and the scene shows the price. Sodoku's silences and Lambert's dryness are held, and holding is visible work.

**Speech is world-anchored.** People reach for the objects and idioms their life has given them. A Kharven soldier says *how's your stack* and *wet wood* and measures time in a fire's length, not because the Standing Inventory says so but because that is what is in his mouth. A jurist reaches for procedure. A physician reaches for the third bowl. **Nobody produces a metaphor from outside their own life.**

**And nobody explains anything they both already know.** The iceberg rule is a dialogue rule first.

---

## §5 — THE COMPOSURE BAN

**No character speaks in balanced clauses under duress, and Natalie's habit of writing everyone that way is a tell.**

Specifically barred in originated dialogue:

- Antithesis and parallelism in a line spoken by somebody in extremis
- Three-part lists from a character who is bleeding, frightened, or grieving
- A subordinate clause of more than about eleven words in shouted speech
- Perfect syntax from characters who have been established as inarticulate, young, exhausted, or foreign to the language
- Every character in a scene constructing sentences at the same length

**The test.** Cover the dialogue tags and read the lines. If a stranger could not sort them by speaker, the scene failed, and the failure is now a Pack Nineteen failure and not merely a voice-differentiation warning.

---

## §6 — WHAT SURVIVES UNCHANGED

The Dialogue Craft Standards remain in force. Voice differentiation by what a character notices, wants and refuses remains the primary mechanism. The funeral test still governs humour. One italic private thought per named NPC per scene, unchanged. Body language woven into speech, no talking heads, unchanged.

Pack Fifteen still governs register: modern words and frames are legal, the only test is whether a specific word breaks a reader's belief in the world, and Natalie never flags *reads modern*.

---

## §7 — VERIFICATION

Added to the Manual Verification Guide and to `wotr_verify.sh` as checks 40 to 42, run with `--dialogue`.

**Check 40 — Fidelity.** Manual. Diff the output against the submitted rough. Every line of Isaac's dialogue appears verbatim except for the corrections permitted in §2. Any other change is a FAIL and is reverted.

**Check 41 — Prosody.** Automatic where possible. If the submitted rough contains stretched vowels, repeated punctuation or capitalised shouting and the output does not, FAIL.

**Check 42 — Composure.** Flags dialogue lines that are long, subordinate-heavy, or contain parallel constructions, and reports the spread of line lengths across the scene. A file in which every speaker's lines cluster at one length is flagged for reading.

---

## §8 — RETROSPECTIVE

Every scene in the Kharven and Vaeloris sequences was written before this pack and most of them smoothed at least one line. The worst offenders, in order:

1. **Darius's shout at Kujo**, where a loss of control was rewritten as a declaration.
2. **Aurelian's chant clauses**, where Isaac's plain English was elevated into Latin and the English was dropped rather than kept alongside.
3. **Sodoku's lines to Miku**, which survived nearly intact and are the model for how this should have been done throughout.
4. **Sonzai's revocation**, preserved verbatim, correctly.

No rewrite of past scenes is proposed. The pack governs from here.

## §9 — STANDING TASK

Fold Packs One through Nineteen into the base guides and retire the diffs. Ask once per session.
