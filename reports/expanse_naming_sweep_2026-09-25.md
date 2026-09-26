# The "Expanse" naming sweep — every occurrence, classified (WAR-118)

Date: 2026-09-25. Doc Kett, on WAR-118.

WAR-118 records that the archive names the force besieging Kharven "the Expanse",
that canon's Hobgoblin Expanse is an oceanic parliament that does not make war,
and that Kharven's canonical hobgoblin enemy is the Iron Mandate of Undaar-Keth.
The issue deliberately left the `CONFLICTS.md` row unwritten, on the grounds that
the row needs the sweep first. This is that sweep. It decides nothing. It sorts
every occurrence of the word in the repo into the ones a ruling would move and the
ones it would not, and prices each of the readings that are open.

The question itself is with Isaac, folded into the WAR-3 questionnaire. Everything
below is the part that did not need his answer, and is written so that whichever
way it goes, the file list is already scoped.

---

## 1. What the sweep found that the issue did not

Four things, all of which change the size and the shape of the question.

**1.1 The besieging force and the Keth-Gorrum Front are the same polity, so this
is one question and not two.** Vresk Dokkan is the returned officer whose renaming
the whole Keth-Gorrum Front turns on, and he commanded the breach force.
`scenes/10_wotr_what_the_ground_was_owed.md:366`

> **Vresk Dokkan of Kaadre-Six, Vorruk-Kaan of the Third Ashfold.** He is the one who gave the *Grr-Vaa* speech to 2,200 men on the ash

The 2,200 is the breach force's own count, `scenes/01_wotr_muster_breach_road_north.md:75`:

> They had come through at the second hour and they were still coming through at the fifth, and there were two thousand two hundred of them, and they were the most disciplined thing he had ever seen in his life.

So the body that must coin his new compound is the same body that laid the siege.
A ruling cannot name the besieger without also naming whose parliament sits in the
live Front, and cannot leave the Front alone without leaving the besieger alone.

**1.2 The Keth-Gorrum belongs to the Expanse in every canon page, and the live
Front seats it at the Mandate's capital.** The Front's own id and title are
`the-keth-gorrum-of-undaar-keth` (`table/fronts.yaml:16`, `table/FRONTS.md:9`) —
the Expanse's parliament at the Mandate's seat. Canon does not allow that pairing.

`wiki/The Tongues of the Realms/Old Vaross — The Goblinoid Tongue.md:18`

> **The Keth-Gorrum registers.** Parliamentary record of the Hobgoblin Expanse, continuous since the settlement, held in the Vaross the parliament uses for its own proceedings.

against the next line of the same page, `:19`, which gives the Mandate a different
instrument entirely:

> **The Mandate's decree archive.** Every active decree read daily at every district garrison for the entire history of Undaar-Keth, and every one of them written down.

**1.3 The Third Ashfold — Vresk Dokkan's own command — is filed in canon under a
*Decree*, which is the Mandate's instrument and not the Keth-Gorrum's.**
`wiki/The Tongues of the Realms/Old Vaross — The Goblinoid Tongue.md:154`

> **From the Third Ashfold Decree.**

The same page, `:131`, is explicit that the two bodies produce different objects:

> A decree is a board. A ruling is a post. The Keth-Gorrum's archive is a room full of timber, every entry in it can be destroyed with an axe, this has happened, and the Expanse's law has a hole in it where the year 411 used to be.

This is the one piece of evidence on the page that already points one way, and it
points at the Mandate. It is recorded, not acted on.

**1.4 A previous pass already noticed the conflation and papered over it in a
standing file.** `desktop/inventories/expanse.md:1` and `:3`

> # THE STANDING INVENTORY: THE KETH-GORRUM (UNDAAR-KETH AND THE EXPANSE)
>
> Note: the Fronts page seats the Third Ashfold and Kaadre-Six under the Keth-Gorrum, so this Inventory covers the island parliament and the mainland Mandate as one voice. Items marked (M) are Mandate texture, (B) Bugbear, (O) Ironblood Orc.

That file is loaded by `session_start` and the MCP's `_inventory` by culture name,
so the merged reading is what every scene written since has drawn its texture
from. It is load-bearing, not cosmetic.

---

## 2. The classification

Every "Expanse" in the repo, by whether a ruling on WAR-118 reaches it.

### Class A — the oceanic Hobgoblin Expanse, used correctly. No ruling touches these.

The archipelago, its parliament, its people, its language, its relations with the
Mandate. Sixty-odd occurrences across:

| File | Count |
|---|---|
| `wiki/The Bearing and the Holding/The Hobgoblin Expanse.md` | 14 |
| `wiki/Volume I — Character Cards/Freda Thunn-Gorr — The Caldera Wife.md` | 10 |
| `wiki/The Inner World — The Northern Shield/The Iron Mandate of Undaar-Keth — The Closed Fist.md` | 8 |
| `wiki/The Tongues of the Realms/Old Vaross — The Goblinoid Tongue.md` | 7 (excluding `:154`, which is evidence at 1.3) |
| `wiki/Volume I — Character Cards/Krothar Thunn-Gorr — The Old Chain.md` | 6 |
| `wiki/Volume I — Character Cards/Krothar Veylshroud — The Chain Without a Master.md` | 4 |
| `wiki/Volume I — Character Cards/Torven Greis — The Merchant Lord.md` | 1 |
| `wiki/Reference Table/A Reader's Codex.md:72`, `wiki/Geography/Geography & the Four Quarters.md:71,:77`, `wiki/Geography & the Four Quarters/The Bearing and the Holding.md:116`, `wiki/INDEX.md:294`, `wiki/.manifest.json`, `wiki/Factions, Bloodlines & Institutions/The Bench of Attribution.md:121`, `wiki/The War Cycle/The Rites.md:55` | 1 each |
| `imports/lore/` mirrors of the four cards, and `clusters/c31`, `c15`, `WORLD.md:75,:115` | mirrors of the above |
| `sources/WOTR_Racial_Voice_Guide_Amendment.md:12` | read-only, untouched in any case |

### Class B — a different Expanse entirely. No ruling touches these either.

Two unrelated places whose names happen to carry the common noun.

**The Verath Expanse**, a high-Aether monster wilderness east of Verath township:
`scenes/The_Path_of_Sorrow.md:561,:573,:615,:619`;
`wiki/Volume I — Character Cards/Sodoku Moto.md:192`;
`scenes/TIMELINE.md:21`; `book/night-watch-zombification/ch05/brief.md:1320`.

**The Zafaran Expanse**, Kushara's northern dune ocean:
`wiki/The Bearing and the Holding/Kushara — The Land That Remembers Weight.md:35`;
`wiki/Factions, Bloodlines & Institutions/The Eight Great Houses of Kushara.md:100`.

Flagged because a careless find-and-replace on the string would destroy both.

### Class C — the besieging force named "the Expanse". A ruling reaches all of these.

| File and line | The naming |
|---|---|
| `scenes/01_wotr_muster_breach_road_north.md:117` | "An Expanse man drilled to the count of a horn does not" |
| `scenes/01_wotr_muster_breach_road_north.md:127` | "The men of the Expanse were still coming through at the ninth hour" |
| `scenes/commencement_of_the_curia_kujo_arc.md:2404,:2414` | the same two sentences, in the long arc file |
| `scenes/the_war_in_the_north_v_the_shieldwarden.md:23` | "the Expanse below it breathing green smoke every spring for nine years" |
| `scenes/the_war_in_the_north_v_the_shieldwarden.md:93` | "the green smoke coming up off the Expanse" |
| `scenes/CONTINUITY.md:968` | "while the Expanse breathed green smoke" |
| **`wiki/Volume I — Character Cards/Bram Greymane — The Ridge.md:58`** | "marked for him first, by a horn or a banner or the green smoke off the Expanse" |
| `imports/lore/cards/bram-greymane-the-ridge.md` | the mirror of that card |
| `bot/queue/01_wotr_muster_breach_road_north.judger.md:5,:13,:115` | the session-close draft |
| `bot/queue/01_wotr_muster_breach_road_north.judger.json:284,:523` | the same, structured |
| `bot/queue/01_wotr_muster_breach_road_north.gather.md:123,:133,:551` | the gather artefact |

**Bram Greymane's card is published.** That is the one Class C item that has left
the repo, and it is the reason this sweep is not purely an archive matter.

### Class D — the same polity named by its parliament. A ruling reaches these too.

| File and line | What carries the naming |
|---|---|
| `table/fronts.yaml:16-17` | the Front's id `the-keth-gorrum-of-undaar-keth` and its name |
| `table/fronts.yaml:23,:27,:33,:36,:40` | want, next move and three of five clock ticks |
| `table/FRONTS.md:9,:12,:13,:15,:16,:17` | the same Front, rendered |
| `wiki/The Table — Running Pieces/Fronts, as clocks.md:22,:25,:26,:28,:29,:30` | generated page |
| `wiki/The Table — Running Pieces/Fronts.md:18` | generated page |
| `scenes/10_wotr_what_the_ground_was_owed.md:289,:291,:325,:366,:370` | the Keth-Gorrum coins the compound; "every hobgoblin in the Expanse" |
| `scenes/the_revolution_of_the_inner_world.md:285,:287,:321` | the same passage in the arc file |
| `book/kharven-year/bible.md:13,:23,:39,:64,:88,:99,:125,:128` | the book's premise, its Front table, its ch3/ch7/ch11/ch12 spine |
| `book/kharven-year/outline.json:5,:38,:94,:97,:150,:214,:256` | four chapter beats and two thread texts |
| `book/kharven-year/state.json:70,:148` | two carried facts |
| `book/kharven-year/ch01/brief.md:1060,:1062,:1096` | generated brief |
| `book/night-watch-zombification/ch04/brief.md:1282` | generated brief |
| `desktop/inventories/expanse.md` | the whole file, merged as at 1.4 |
| `desktop/NATALIE.md:118,:194`, `book/kharven-year/ch01/brief.md:84`, `rules/pack-06-six.yaml:599` | the Inventory's culture name, "Expanse", in six places that list the seven Inventories |

`table/ledger.yaml:85-86`, `table/LEDGER.md:21` and the two wiki Ledger pages name
Vresk Dokkan without naming a polity. Untouched under any reading.

---

## 3. What each reading would cost

Not recommendations. The three readings that the evidence leaves open, each priced
in files, so the questionnaire can state a consequence instead of a shrug.

### Reading 1 — the besieger is the Iron Mandate of Undaar-Keth; the archive's "Expanse" is a slip.

The geography and the instruments fit: a continental empire on Kharven's western
flank (`The Iron Mandate … :19`, "A **hobgoblin-led continental empire** occupying
the western reaches of the northern shield"), a land route that a board can be
carried over ("a board the Keth-Gorrum sent over the pass", `outline.json:38`), and
the Third Ashfold *Decree* at 1.3.

Costs: every Class C and Class D name changes — 12 files in Class C including a
published card, 14 in Class D including the live Front. And the Front's engine
breaks: the whole Vresk Dokkan plot needs a body that **votes** to coin a word and
a **hereditary interpreter** of a sealed register, and the Mandate has neither.
`The Iron Mandate … :188` region, Governance:

> Seven operational commanders, one per district, holding **both military and civil authority.** *The Ironfold does not vote in the parliamentary sense. It reaches consensus through assessment*

So Reading 1 is not a rename. It is a rename plus a redesign of a five-tick Front
and four chapters of `book/kharven-year`.

### Reading 2 — the besieger is the Hobgoblin Expanse; the lorebook gains a war.

Costs: nothing in Class C or D moves, and `The Hobgoblin Expanse.md` must absorb a
nine-year continental siege it currently forecloses twice, at `:157`

> **No Hobgoblin or Bugbear soldier draws a weapon.** Recorded in the Rock under the heading *"Resolved by Geography"*

and at `:105`, which puts the archipelago two hundred leagues of open water from
the nearest coast and on the wrong side of it for Kharven. The Mandate page's
Relations entry would also have to explain a four-century peace between the two
goblinoid states surviving one of them prosecuting a war on the other's continent.

### Reading 3 — two polities, and the scenes conflate them.

The tidiest on paper and the one the evidence closes off: it fails at 1.1. Vresk
Dokkan commanded the 2,200 at the breach *and* is the officer the Keth-Gorrum must
rename, so the besieger and the parliament cannot be different bodies without
cutting him in half. Recorded so the questionnaire does not have to rediscover it.

### A fourth thing a ruling could reach for, recorded because canon offers it

`wiki/The Tongues of the Realms/Old Vaross — The Goblinoid Tongue.md:174`

> **A note on Undaar-Keth and Undaar-Gorr.** Under the compounding rule the second element governs, so *Undaar-Keth* is a seal of the standing kind and *Undaar-Gorr* is a mantle-weight of the standing kind. They are not spelling variants of one name. They are two different places, or one place renamed by somebody making a claim.

Canon has already left a door open for a name that is contested between the two
goblinoid states. Whether it opens onto anything is a ruling, not a sweep.

---

## 4. Ruled, and what was applied

Isaac answered in the queue questionnaire the same day, and the answer is Reading 1.
`RULINGS.md`, the WAR-118 line:

> **WAR-118** — Kharven's besiegers are the Iron Mandate: 'Expanse' is corrected to the Mandate across the archive, and the Kharven lorebook's cold peace is updated to the nine-year war.

**Applied on WAR-118, Class C and the relations entries.** Four archive files
(`01_wotr_muster_breach_road_north.md`, `commencement_of_the_curia_kujo_arc.md`,
`the_war_in_the_north_v_the_shieldwarden.md`, `CONTINUITY.md`), the Bram Greymane
card and its `imports/lore` mirror, and both sides of the Kharven–Mandate
relationship: the Ashen Crown's relations row, which the ruling names, and the
Closed Fist's Kharven entry, which stated the same fact the other way round and
would otherwise have gone on denying the war the other page now records. The wiki
pages are a Notion mirror, so the three page edits were made in Notion and reach
`wiki/` on the hourly sync.

**Held, and why.** The parliament naming, Class D. The ruling settles who besieged
Kharven; it does not name the Keth-Gorrum, and §1.2 and §3 above show why the two
cannot simply be renamed together: the Keth-Gorrum is the Expanse's parliament on
every canon page, and the body the Front needs — one that votes to coin a word, and
keeps a hereditary interpreter for a sealed register — is one the Ironfold explicitly
is not. Correcting the word in those files without settling that would put the
Expanse's parliament inside the Mandate, which is a different error rather than a
smaller one. Fourteen files are waiting on it: `scenes/10_wotr_what_the_ground_was_owed.md`,
`scenes/the_revolution_of_the_inner_world.md`, `table/fronts.yaml` and `table/FRONTS.md`
with their two generated wiki pages, all of `book/kharven-year`, the two generated
chapter briefs, and `desktop/inventories/expanse.md`, which merges the two states
into one voice and is loaded by `session_start`.

One thing that will help whoever takes it: the live naming rule
R20-2-UNDAAR_KETH_NAMING gives the Mandate "given name plus genitive patronymic plus
district designation plus, for military personnel, a rank compound that changes with
every promotion or demotion, making a Mandate citizen's name a service record", and
`scenes/10_wotr_what_the_ground_was_owed.md:291` builds Vresk Dokkan on exactly that
convention, sentence for sentence. He is already written as a Mandate officer. It is
the *institution* that renames him, not his name, that has nowhere canonical to sit.

The clash is recorded as **C-075** in `CONFLICTS.md`.
