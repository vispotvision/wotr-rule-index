# Magic lore flow audit

Run 2026-11-05, read-only, against the live `wiki/`. Scratch scans are in the session scratchpad and are not part of the repo.

Paths are relative to `wiki/The Magic System/` unless they start with another top folder. Severity is one of: **LOST** (a reader gets lost or misled), **DEAD** (dead link, orphan or dangling reference), **THIN**, **MINOR**.

## 1. Counts

| Check | Result |
|---|---|
| Pages in scope (Magic System 63, Disciplines 103, Cosmology 27) | 193 |
| Wikilinks whose source is in scope | 402 (365 pages, 37 assets), all resolve |
| Broken links in scope, source or target | 0 inside the three sections; 1 on the road just outside them (`Start Here:53`) |
| Wrong-path links in scope | 0 |
| Broken links in the whole vault | 245, of which 239 are on one page (`In-World Documents & the Narrative Archive/The Scene Archive.md`) |
| Orphans in scope (no inbound link except `INDEX.md`) | 7 |
| Hubs omitting their own children | 3 hubs, 7 children |
| Hubs in scope that link back to their parent | 0 of 20 |
| Duplicate titles | 1 (`The Veil`, one copy a retired stub); 1 art with two full pages (God Fist) |
| Pages missing from `INDEX.md` | 0 (485 listed) |
| Scope pages with no link path from `Start Here` | 114 of 193 (Magic 11, Disciplines 100, Cosmology 3) |
| Reading findings below | 12 LOST, 8 DEAD, 7 THIN, 14 MINOR, plus 6 voice findings (3 THIN, 3 MINOR) |

`reports/reconcile.md` (run 2026-11-05) does not check links. It reports duplicates `The Veil ×2` and `Continuity map ×43`. The second is stale: no `Continuity map` page is left in `wiki/`, they moved to `lore/v1/`. Links were scanned here instead, by a one-off bash and awk scan over every `[[...]]`.

## 2. Mechanical list

### Orphans in scope (7)

| Page | Severity | Fix |
|---|---|---|
| `The Magic System.md` | DEAD, LOST | See L1. Link from `Start Here`. |
| `The Soul and the Climb/The Concordant Crystal.md` | DEAD | Add to the hub if it stays public-facing; it is `private: true`, so either hub it as private or leave it and tell the hub. See V3. |
| `Cosmology & Metaphysics/Ages and Reckoning/Ages and Reckoning.md` | DEAD | Link from the Cosmology hub. |
| `Cosmology & Metaphysics/Faith and the Powers Above/Faith and the Powers Above.md` | DEAD | Link from the Cosmology hub. |
| `Cosmology & Metaphysics/The Making of the World/The Making of the World.md` | DEAD | Link from the Cosmology hub. |
| `The Disciplines/Named Arts/Named Arts.md` | DEAD | Link from `The Disciplines.md`. |
| `The Disciplines/Schools and Bloodline Arts/Schools and Bloodline Arts.md` | DEAD | Link from `The Disciplines.md`. |

`The Disciplines/The Disciplines.md` has a single inbound link, from `Author's Workroom`, which is itself unreachable. `The Magic System.md:263` names it in bold with no link.

### Hubs omitting children (3 hubs, 7 children)

- `Cosmology & Metaphysics/Cosmology & Metaphysics.md` omits the three shelf hubs above and `Cosmology & Metaphysics/Null-Light.md`. It links the shelves' children directly, so the shelf hubs have no purpose as wired.
- `The Disciplines/The Disciplines.md` omits `Named Arts` and `Schools and Bloodline Arts`, same pattern.
- `The Soul and the Climb/The Soul and the Climb.md` omits `The Concordant Crystal`.

### Reachability from `Start Here`

Followed wikilinks only, never through `INDEX.md`. The Obsidian file tree and the site's explorer still show these pages, so unreachable means no road leads there, not that the page cannot be found.

Unreachable in The Magic System (11): `The Magic System.md`, all six shelf hubs (`First Steps`, `The Foundations`, `The Soul and the Climb`, `Power in Use`, `Practice and Institution`, `Reference and Craft`), `Windows and the Sheet`, `Aether Classes`, `Skills and Trait Levels`, `The Concordant Crystal`.

Those three content pages form a closed loop: they link each other, and only the unreachable hubs link in.

Unreachable in The Disciplines: 100 of 103, including the hub. `Hataraki` is reached through `Blessings and Curses`. Unreachable in Cosmology: the three shelf hubs only.

### Road pages with no outbound page links

`The Measures at a Glance`, `One Exchange, Annotated`, `The Sixteen Stages` (10,468 words), `The Color of Essence`, `Reinforcement`, `The Derivation of Practice`, `The Standing and the Title`, `The Master Glyph Index`. Each names other pages in plain text or bold.

### Titles

- `Reference and Craft/The Magical Categories — Unified Taxonom.md:2`: file name and `title:` are truncated, while its own heading reads "Unified Taxonomy". The truncated form shows at `Start Here.md:42` and `The Magic System.md:252`. MINOR. Fix the title and file name.
- `Power in Use/The Four Crafts.md`: the title is now "The Working Trades" but every link path says `The Four Crafts`, against R84-18. MINOR. Rename.
- `The Standing and the Title — The Three Names.md` is titled "...: Guild Titles as Trust". `Start Here.md:40` still shows the old name. MINOR.
- `Cosmology & Metaphysics/Null-Light.md` has no `title:`. MINOR.
- `The Disciplines/Spellcraft/The Veil.md` is a retired stub still listed in the Spellcraft hub. MINOR. Delete or stop listing.
- `The Disciplines/Spellcraft/Kami no Kobushi.md` ("The God Fist: Seven Ways to Refuse") and `The Disciplines/Named Arts/Kami no Kobushi — The God Fist.md` are two full pages for one art, both opening at Ogawara. MINOR. Merge or make one a pointer.
- `The Scene Archive/New Lore — Reading Order.md` holds 29 path-relative links (`Scenes/...`). They resolve in Obsidian. Out of scope, noted only.

## 3. Reading the road

### Reader gets lost or misled

**L1. The hub and its reading order cannot be reached from the front door.** `Start Here.md:25-42`. "The Magic System, in reading order" links single pages and never the section's own hub or any shelf. `The Magic System.md` is the page that explains the shelves, and nothing links it. Fix: link `The Magic System.md` and the five shelves at `Start Here.md:25`.

**L2. The newest pages are off the road, and How Magic Works points past them.** `Start Here.md:40-42` omits nine pages: Windows and the Sheet, Aether Classes, Skills and Trait Levels, Release Forms, Blessings and Curses, Training and Sects, Reinforcement, Stacking and Spending, Runes and Tags. `How Magic Works` has a section on each new concept with the wrong next step:

| Section | Line | Sends you to | Should send you to |
|---|---|---|---|
| Windows | :50 | Measures at a Glance | Windows and the Sheet |
| Traits | :70 | Trait System | also Skills and Trait Levels |
| Skills | :80 | Working Trades | Skills and Trait Levels |
| Aether Class | :112 | Tier Grade | Aether Classes |
| Fate and blessings | :190 | Four Paths, Core Vocabulary | Blessings and Curses |

Fix: change those five read-next lines and add the nine to `Start Here.md:40`.

**L3. Start Here sends a newcomer into the retired lore.** `Start Here.md:46`: "every scene written so far". The target page's 239 scene links are dead because those scenes moved to `lore/v1/` in the 2026-10-18 reset, which `lore/v1/README.md` calls frozen and "not canon for events". All five "first scene for each live thread" entries (`Start Here.md:50-54`) exist only in `lore/v1`, and `:53` is the one broken link on the road. `:56` then sends the reader to that page's reading order. The real live list is `The Scene Archive/Scenes/` (56 files) and `The Scene Archive/New Lore — Reading Order.md`, which has no inbound link. Fix: rebuild the Scene Archive page from live scenes, replace the thread table, and link the new reading order.

**L4. Three reading orders that disagree.** `Start Here.md:19-23` runs How Magic Works, Reader's Codex, Measures, Exchange, Factions. `First Steps.md:9`: "Read these four first", with Core Vocabulary last, while `:14` says of it "Nothing else here is readable without them." `Start Here.md:27`: "read these eight pages in this order. Each one builds on the one before", starting at The Gate (shelf V). `The Magic System.md:190`: "the reading order runs down this list", starting at The Physical Account after First Steps. Fix: name one order and call the others short routes, with Core Vocabulary moved or reworded.

**L5. The Working Trades is still a design document, and it is step 6 of the route.** `Power in Use/The Four Crafts.md`:

- `:24` "standing outside the hall's own voice"
- `:29` "it is not what Tolkien, Martin, Clarke or Le Guin are doing"
- `:59` "Nobody needs to import the Western frame into WOTR."
- `:63-73` The Five Levers, including "remain author-facing"
- `:164, :195, :244` "Prose cues"
- `:191` "Standing rule for prose"
- `:259` "Finrod and Sauron singing at each other"
- `:271-281` What This Changes on the Page
- `:285-295` Settled Positions, ending in a Standing Inventory entry

The page also leans on terms it never explains: "The five-step pipeline" (`:28`), "the Cost Wheel" (`:73, :239`, defined only in the author-facing Field Manual at `:135`), "the Law V question" (`:161`, first defined at `:289`), "Law III" (`:290`). Fix: move the design material to the Field Manual, keep the story and the trade sections in the hall's voice, and define the anchor rule where it is first used.

**L6. Two efficiency ladders with no rule for which to use.** `Tier Grade, Bands & the Aether Shell.md:193-202` gives η by Class; `:277-287` gives η by Tier of Standing; `:291` shrugs: "Both are reproduced as written. Neither has been withdrawn." `The Measures at a Glance.md:25` says "The tier sets η" and `:28` says "About 0.30 at Initiate, rising past 1.0 at Archmaster". They collide on specifics:

- Radiant Crystal is "Class V · Master · Stage VIII" (`Tier Grade:242`), and Class V is 1.00 and up (`Measures:25`), but Master reads 0.70 to 0.80 (`Tier Grade:284`).
- Class II sits at "Early Refraction" at 0.75 to 0.85, but Expert through Refraction reads 0.60 to 0.70.
- Mun Seo-yeon is Class III at Stage VI (`Tier Grade:134`).

`One Exchange:155` quietly uses the Tier figure for an unclassed fighter and the Class figure for a classed one, which may be the intended rule. Fix: say in one sentence that the Stage figure is for the unclassed and the typical, and that a read Class overrides it; if that is not the law, record a conflict and rule it. `CONFLICTS.md` holds no entry for this exact clash that I could find.

**L7. Can a coil tell a bought Stage?** No: `Practice and Institution/The Gate Who May Learn Magic.md:67` "A coil cannot tell a bought Stage from a fought one", `The Derivation of Practice:86`, `Training and Sects:56` "no coil can tell". Yes: `The Sixteen Stages.md:412` "a purchased seat reads differently on the coil from an earned one", `:154` "the instrument shows that too", and `wiki/A Reader's Codex.md:87`. `Mechanica:29` adds that the coil reads a cut-Crystal Draft and a lawful one the same. Fix: separate Stage (reads the same) from seat (reads differently), once, and repeat that wording everywhere.

**L8. Where most practitioners stop.** `The Sixteen Stages.md:88` "Better than nine souls in ten will live and die inside this Band" (Band I, Stages I to IV), with `The Ladder and the Draft:58` and `wiki/A Reader's Codex.md:77` agreeing. `The Trait System:149` "Most practitioners spend the back half of their careers stalled in the high hundred-and-nineties", with `The Sixteen Stages.md:225` close to it. `The Standing and the Title:78` says an opened, untaught Crystal "is the condition most practitioners in the four quarters will die in", while `The Gate:17` says waking is taught. Fix: reword the stall as "most of those who ever reach Band II", and drop or reword the Standing line.

**L9. Domains teach two ways and have no home.** `Tier Grade:299` "a character does not choose to deploy a Domain the way they choose to throw a punch", with no mention of the Second Release anywhere in that section. `Release Forms:43` "The Second Release opens and powers the Domain", and `How Magic Works:178` adds that it forms as it is named. There is also a loop: `The Sixteen Stages:212` makes "first Domain seed activation" the Catalyst for Stage VII, while `Release Forms:33,43` and `Measures:21` make the seed a product of a Second Release available only from Stage VII. The concept's only home is the last fourteen lines of a numbers page, and the hub blurb for that page (`The Soul and the Climb.md:15`) does not mention it. Fix: give Domains their own page on the shelf, reconcile the Catalyst wording, and point `How Magic Works:178` to it.

**L10. Vows have no home, though the world runs on them.** `How Magic Works` has no vow section; `:182` is a passing mention. The real account is scattered: `Windows and the Sheet:135`, `Stacking and Spending:26`, `Blessings and Curses:65`, `Counterplay:88`, `The Four Paths:103` ("the Vow Clause", unlinked), `Mechanica:52` ("Votia", unexplained on the road), `The Magical Categories:310, :366`. The penalty differs: `Counterplay:88` "A vow broken is a Shear Break", `Windows:135` "Breaking it lands at once", and `Core Vocabulary:170` needs repeated denial for a Shear Break. Fix: add a Vows and Oaths page on the Practice shelf and a section in How Magic Works, and state one penalty.

**L11. Two lists of what Fate gates.** `The Four Paths:46, :100` lists Persistence, Continuity, Maturity, Anchoring, Ward, Sovereignty, Throne. `The Magic System.md:117, :120` lists Persistence, Continuity, Ceiling, Stability, Fate, Throne. Fracture II settles it against The Four Paths: `**Maturity** open` and `**Anchoring** open` with Spirit for their gated parts (`Fracture of Worlds — The Living System/II. Grades, Gates and Thresholds (Parts Four–Ten).md:167, :171`), while Ceiling and Fate are Fate-gated, which The Four Paths omits. Fix: correct The Four Paths from the table.

**L12. Where Traits come from is never joined up.** "The body gains Traits" from tempering appears on 12 pages (`How Magic Works:106`, `The Trait System:28`, `The Ladder and the Draft:26`). `The Trait System:36` says "A Trait is survived into existence, never taught", `:54` says "awakening grants a person no new Traits", and `:159` says a Draft seeds "a law that was never survived into existence". No page says whether a melt can create a new Trait or only feeds existing ones. Fix: one plain sentence in Trait System II, and link the gain line to it.

### Dead links and dangling references

**D1.** `Practice and Institution/On Walking Into the Current:19, :88`: "The Mechanism is written for practitioners", "See the Mechanism for compatible and incompatible outcomes". No such page exists; it is a ghost of an older document. Fix: point to The Eight Families' encounter types and density scale.

**D2.** `The Magic System.md:27`: "in twenty-two Parts across eight pages". The Fracture hub says twenty-four Parts, and there are ten pages. Fix: correct both figures.

**D3.** `The Magic System.md:239`: "almost nobody is taught to wake it". `The Gate:7` and the Practice hub say about one in ten. Fix: copy the Practice hub blurb.

**D4.** `The Soul and the Climb.md:11`: "before any of the above touches it", on the first item of the list, so nothing is above it. Blurb copied from the Magic hub. Fix: reword.

**D5.** `Start Here.md:20`: "listed in the wiki as the **Glossary**". INDEX and the hubs list it as A Reader's Codex; no page or build script I checked uses that label. Fix: drop the clause. I did not check the rendered site nav.

**D6.** `The Soul and the Climb/The Color of Essence.md:10`: "the Provenance Doctrine" is named with no link, and only `The Bench of Attribution` carries the term. Fix: link it or cut it.

**D7.** `On Walking Into the Current:76`: "Ketsumōgan", where 41 other uses read Ketsumyōgan. Fix: correct the spelling.

**D8.** `The Magic System.md:122, :159, :263`: "The Four Paths", "The Bestiary" and "The Disciplines" sit in bold unlinked, as do the Apprentice's Primer and Fracture. `The Sixteen Stages`, `The Ladder and the Draft:16, :56, :66` and `The Measures:9, :74` do the same with sibling pages. Fix: turn them into links.

### Thin

**T1. The road has no onward steps.** No shelf hub links back or forward, and none of the 20 sub-hubs links its parent. Only How Magic Works and three new pages use "Read next". The last page on the road, `Mechanica`, ends on "Write all three positions as reasonable". Fix: a one-line next-shelf footer on each hub, and "Read next" on each road page.

**T2. Glossaries miss the road's main words.** `First Steps.md:14` calls Core Vocabulary the page nothing else can be read without, yet it has no entry for Level, Stage, Threshold, Draft, Release, reserve, practitioner, Path, Continuum or coil. `wiki/A Reader's Codex` ("Keep it open in a second tab", `Start Here:20`) has no Release, reserve, practitioner, Pressure, reinforcement or Threat Tier entry, though `:185` uses Release. The Lexicon has no Release, reserve, Path or Continuum entry either. Fix: add those entries to Core Vocabulary and the Codex glossary.

**T3. "Card" is never explained.** `How Magic Works:98`, `One Exchange:103`, `Stacking and Spending:33, :66`, `Reinforcement:41`, `Release Forms:59, :61, :63, :69, :77, :83` use a card as an in-world record, while `Start Here:60` uses Character Cards for wiki pages. Fix: define the registered card once in Measures or Core Vocabulary.

**T4. "Carry" and "Class IV stock".** `The Sixteen Stages:405-407` "carry from four classes and nine sources", `:429, :432` "Class III carry", `:436` "three-mark stock", `:454` "Both Class IV". None is explained or linked to The Standing Index, and on that page "Class III" also means Aether Class. Also `Core Vocabulary:204`, `The Ladder and the Draft:107`, `How Magic Works:132`. Fix: gloss once, say "Index Class IV", and link it.

**T5. Waking Drafts.** `Windows and the Sheet:165` says the rich buy them for their children and they often kill or warp a child. `The Gate:17` says "Waking is taught" and never mentions the Draft; How Magic Works is silent. The Gate is that concept's natural home. Fix: add a paragraph to The Gate and a line to How Magic Works.

**T6. The Third Name's Archetype floats.** `The Standing and the Title:86` "the Archetype under your Aether Class", while `:125` says Stage, Family and Method have no hand in it and it is "produced by Passive Traits". Archetype appears on no other magic page, including Aether Classes, and the "Harmonic" Archetype (`:102`) collides with Class II Harmonic and the Harmonic Crystal. Fix: drop "under your Aether Class" and rename or distinguish it.

**T7. Master Works and Monster Cores sit two links away and are not linked where they are taught.** `How Magic Works:132, :152`, `The Ladder and the Draft:101, :109`, `The Four Crafts:237, :265` all explain them with no link to `Materials, Alchemy & Trade/Alchemy/Monster Cores.md` or `Master Works.md`. Fix: add the links.

### Minor

**M1.** "Outer layer" means two things. The Shell is the outer layer in `How Magic Works:54`, `The Physical Account:43` and `Tier Grade:12`; the Attraction Layer is at `The Ladder and the Draft:76` ("outer layer") and `Blessings and Curses:249` ("the outermost"). Fix: pick one.

**M2.** "Chosen Path" at `The Ladder and the Draft:105, :165` and `Mechanica:55` against `The Four Paths:9` "Nobody chooses a Path" and `The Magic System.md:109`. Fix: say recognized or stated Path.

**M3.** Material Plane in `Core Vocabulary:30` and Physical Plane in `The Eight Families:197` and `The Four Paths:21`; `wiki/A Reader's Codex` uses both (`:21, :51`). Fix: one name, or say they are the same.

**M4.** `wiki/A Reader's Codex.md:39, :121` say Bara and `:151, :235` say Bairos, with no gloss on that page. The gloss exists at `Cosmology & Metaphysics/The Making of the World/The Three Epochs.md:18, :33`. Fix: one clause in the Codex.

**M5.** `The Magic System.md:90` and `Skills and Trait Levels:179` say eight Sub-Stats per Primary with no exception; `Measures:24` and Fracture II `:26, :32` divide Dominion by seven because Throne is excluded. Fix: note the exception once on the hub.

**M6.** Who can level a trade skill: `Skills and Trait Levels:54` "Anyone can level any of them" and `Core Vocabulary:190`, against `Runes and Tags:17` "a skill anyone with a woken Crystal can level" and `The Four Crafts:224`. Fix: say the woken cut and tag, and everyone pours or bakes.

**M7.** `Training and Sects:90`: "a letter from Vane's father". The opponent in that example is Rafe Tressilian. Fix: correct the name.

**M8.** Ibbet Lowe's linen runs "half a century" at `The Trait System:12` and `Skills and Trait Levels:169`, "Forty-one years" at `The Trait System:20` and `Skills and Trait Levels:143`. Fix: pick one.

**M9.** Window format drifts. Path appears on Mun's sheet (`Tier Grade:134`, `Windows:49`, and is listed at `Windows:60`) but not on `How Magic Works:39`, `Measures:62`, `The Magic System.md:131`, or the list at `Core Vocabulary:188`. `Class: Auditor · Tier III, Resonant` against `Class: Hammerhand · Muridic`. `[Damage:` at `Reinforcement:62` against `[Hit:` elsewhere. `→` at `Training and Sects:83` and `The Four Crafts:92` against `to` elsewhere. Fix: settle one format.

**M10.** `Stacking and Spending:27` labels the row "A release call" but defines it as a technique's name shouted, while `Core Vocabulary:112` calls it The Call. Fix: rename the row.

**M11.** The same sentences recur along the road, close to word for word: "opens the door and no more" in 19 files, "the worst crime in every realm" in 12, "wealthy are stronger because they are wealthy" in 11, "because the giver wrote" in 11, "a great giver spends almost nothing" in 10. A reader walking the road meets the bought-Stage paragraph on almost every page. Fix: keep it on The Ladder and the Draft and link there.

**M12.** A mechanical gloss, "one of the sixty types of Aether and the governing idea it carries...", breaks sentences at `The Sixteen Stages:110`, `The Trait System:90`, `The Ladder and the Draft:80` (inside a table cell), `Tier Grade:81` and `The Color of Essence:21`. Fix: shorten the gloss, since the road has already taught the term by then.

**M13.** `The Trait System` VI-a (`:100`) and `The Ladder and the Draft` V-a (`:137`) keep patch-numbered sections, and `The Ladder and the Draft:169` ends on a stray rule. Fix: renumber and remove.

**M14.** `Tier Grade:305` has a Stage VII seed lasting "minutes" against `The Sixteen Stages:222` "often lasting seconds at its first firing". Compatible, but said without reconciling. Fix: one clause.

### Voice: pages that still read as pre-rewrite

Against R82-42. These are the ones that break the scholar's voice or expose the workbench.

**V1. "Writing" sections addressed to the author, on reader pages.** THIN. `The Gate:118-124`, `Who Pays for the Lamp:136-144`, `Mechanica:83-91`, `The Color of Essence:106-118` (Part Five, which also drops the Limina row), `The Four Paths:128-132`. `The Gate:124`: "the reader should never be allowed to forget". Fix: move them to the Field Manual.

**V2. Tier Grade's middle is the old sheet voice.** THIN. `Tier Grade:24-25` "Characters", "The System will simply halt the level counter", `:37` "the file will read as an error", `:40-48`, `:56-119`, `:298-299`, and the emoji at `:79`. Good story at `:14`, good The Sheet at `:125-161`, and a flat rulebook between them. Fix: rewrite in the voice of the page's opening.

**V3. The Concordant Crystal is untouched.** THIN. `The Soul and the Climb/The Concordant Crystal.md:12` uses ` -- ` and "Coherence Band", "Wellspring Houses"; `:20` reads "Ruled by Isaac, 2026-09-12 (R26-1-CONCORDANT_CRYSTAL_MECHANISM)". No opening story and no gloss. Fix: rewrite in voice and take the rule id out.

**V4. Heavier older formatting.** MINOR. `The Derivation of Practice`, `The Standing and the Title` and `On Walking Into the Current` still bold and italicize whole sentences, unlike the clean newer pages beside them. `The Derivation of Practice:128` has raw `<strong>` tags, and its table at `:138-148` has lost its grouping: "Scriptia" and "Alchemia" sit in the Lean column. Fix: strip the emphasis, the HTML and rebuild the table.

**V5. Workbench residue.** MINOR. `The Master Glyph Index:142-144` (Amendments, "a drafter checking a Codex assignment line"). `The Disciplines/Named Arts/Ken — The Fist That Fights the Architecture.md:116` and `The Disciplines/Named Arts/Rusashin — The Dust That Remembers What It Touched.md:109` ("✅ Resolved 2026-09-12"). `The Disciplines/Named Arts/Named Arts.md:12` (Matla's blurb: "Discipline Classification Entry, Second Epoch Archive, Aegorian Reconstruction"). Frontmatter tag `Open Rulings` on `The Magic System.md` and `Cosmology & Metaphysics.md`. Fix: delete or rephrase in voice.

**V6. Named crafts survive against R84-18.** MINOR. 47 Disciplines pages carry a `**Craft** ·` field, mostly Spellcraft (37), Magicraft (6) or Runecraft (2), and Spellcraft is still the folder name under the title "The Spoken Arts". Fix: replace the field with the trade or skill, and rename the folder when convenient.

## 4. Terms from NATALIE: can a reader get there?

Depth is link hops from `Start Here`, never through `INDEX.md`.

| Term | Home | Depth | Note |
|---|---|---|---|
| Windows | `Windows and the Sheet` | none | L2. Taught at `How Magic Works:32`, which does not link it. |
| Aether Class | `Aether Classes` | none | L2. Fuller law on `Tier Grade`, depth 1. |
| Trait levels | `Skills and Trait Levels` | none | `The Trait System:100` covers it, depth 1. |
| Skills | `Skills and Trait Levels` | none | L2. |
| Drafts | `The Ladder and the Draft` | 1 | Fine. `The Common Drafts` is outside the road. |
| Core | no page; `The Eight Families:160`, `Dungeons`, `Who Pays:43`, `Core Vocabulary:89` | 1 | Adequate. Three meanings are flagged well on every page. |
| Dungeons | `The Bestiary/Dungeons` | 1 | Good page, good voice from the head; body only skimmed by heading. |
| Blessings | `Blessings and Curses` | 2 | Only through The Four Paths. L2. |
| Vows | none | n/a | L10. |
| Master Works | `Materials, Alchemy & Trade/Alchemy/Master Works` | 2 | Only through Grade and Rarity. T7. |
| Rarity | `Grade and Rarity` (file `The Item Tiers`) | 1 | Fine. |
| Also: Domains | none; `Tier Grade:295`, `Release Forms:43`, Fracture VIII | 1 | L9. |
| Also: Monster cores | `Materials, Alchemy & Trade/Alchemy/Monster Cores` | 2 | T7. |
| Also: Waking Drafts | `Windows:165` only on the road | none | T5. |

## 5. Could not check

- The rendered public site, its nav, and which links die there because the target is private. Everything above is from the vault's markdown.
- `The Disciplines` and `Cosmology & Metaphysics`: mechanical only, plus hub heads and spot greps. Their prose was not read.
- The Family pages past Caloria's opening, The Master Glyph Index table, The Counted Speech, and the Reference shelf: spot-read or grepped.
- `Dungeons`, `Grade and Rarity`, `Master Works`, `Monster Cores`: heads and section lists only.
- Heading anchors in links: 27 exist in the vault, all outside scope, and were not validated.
- Whether any contradiction above already has a ruling in `RULINGS.md`. I checked `CONFLICTS.md` only for the η and bought-Stage clashes, by grep.
