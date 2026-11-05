# Wiki rewrite brief: magic pages and the Ages (R83-13, R82-42)

Isaac's order: the whole wiki moves to the Dark Ages setting and the R82 ability feel, section by section. This is the first section. Law: `desktop/NATALIE.md` (ABILITIES AND THE WORLD, The Dark Ages, Cultivation) and rules R82 and R83 (`rules/doc-directions-2026-11-04.yaml`, `rules/doc-directions-2026-11-05.yaml`). Where a page disagrees with that law, the law wins and the page changes.

## Where you work

- Edit ONLY the staged copies under `imports/drafts/wiki-rewrite/library/wiki/`. Never edit `wiki/`, `sources/`, `rules/`, `RULINGS.md` or `CONFLICTS.md`. Never call `wiki_write`, `log_ruling`, `git commit` or any tool that commits. The live `wiki/` autosaves and publishes every 15 minutes, which is why staging exists.
- Keep filenames and folders. Keep frontmatter, adding nothing to it except a changed `title:` if the body's title changes. A page's `private:` line stays as it is.
- Keep every `![[Assets/...]]` embed and every `[[wikilink]]` target working. Keep existing headings where you can, because other pages link to them.

## What each page becomes

**1. It opens on spectacle.** Every page with real content opens on a loud, specific, colorful thing that happened: a famous fight, a disaster, a bet, a blunder, a boast, with named people, a place, a crowd and what it cost. Then the in-world narrator turns to how it works. Scale it: a landing page or short hub gets a line or two, a major page a good paragraph or three. Then the technical detail follows, complete, with dry asides (R82-42).

**2. The narrator stays.** A Guild archivist or Measurewright, with epigraphs, asides and the occasional dry warning. Warm and opinionated and in love with the subject. Measurewrights argue and are sometimes wrong, and the page may say so (R83-11). Keep the existing good jokes.

**3. The tone is dark shonen, bright and loud.** Color, heat, wonder (NATALIE, THE TONE). Fix any passage that is gray, weary or hushed. Practitioners are common, with sects and ranks everyone knows (R83-10). Small powers are everywhere and petty, a trade people do with their hands, costing money, and someone can refuse (R83-8). Schools run like football clubs. Heralds, minstrels, bounties and bookies carry fame (R83-7). Ordinary fighters use street slang for the system, and scholars use the real terms (R82-39). Aura coat, Pressure and sensing are famous shared arts, each culture with its own name and its own argument (R82-19): mention this where those are treated, inventing names by each culture's sound rules.

**4. Nothing is lost.** Every fact, law, number, table, formula, threshold, cost, failure mode, term and definition on a page survives unless this brief retires it. Spectacle is added on top; depth is never cut (NATALIE, DEPTH AND EXPLANATION). A page may come out longer. Never retype a numeric table from memory: edit the cell that needs changing and leave the rest alone.

## Retired, and what replaces it

| Retired | Now |
|---|---|
| the draw, draw-hum, draw main, Draw Boards, Draw Age, drawing Aether | Practitioners PULL Aether from the environment around them, refine it in the Soul Crystal into Essence, and drive it out through the Shell. Where you stand matters: rich ground fills you faster, thin ground starves you. "Aetheric Density" stays as the scholar's term. Ordinary English "draw" (draw a sword, draw near, draw a conclusion) is fine. |
| Draw Age | "the Dark Ages" |
| district mains, standpipes, culverts of Aether, gauge-housings, meters, tariffs on supply, spurs, inspectors, cutters, cells | Gone. City magic is done by living people and their crafts: lamp-wardens, ward-cutters, hedge-workers, Guild craftsmen, paid by the job, who can strike, overcharge or refuse. |
| "cut the main" as a counter | Take the fight off rich ground, onto salted, bled or thin ground. A worked Wellspring site (a Core, in common speech) recharges and has keepers, and its keepers can close it. |
| Wellsprings as only places, or as a current in a pipe | R83-9: Aethers come in different types that affect the Soul Crystal differently, and those types are the Wellsprings: sources of power that also represent alchemical principles and spiritual transformations. There are sixty, fixed. A Wellspring also has sites where its Aether pools, and common speech calls such a site a Core. Well-spawn stays. |
| guns, gunpowder, shot, muskets, pistols, proof-marks against shot | None, in any era. The crossbow bolt is the cheap thing that can kill a high-Stage fighter in a room (R83-5), read by Speed Grade like any projectile. Bows, siege engines and thrown things stay. |
| "Can react to gunfire but cannot outrun it" (Grade D) | "Can read a crossbow bolt loosed across a room and slip it, if they see the loose". Use this exact wording wherever that row appears. |
| "Can engage firearms without significant reactive disadvantage" (Grade B) | "Can stand in a volley of bolts and arrows without significant reactive disadvantage". Use this exact wording wherever that row appears. |
| rail, trams, wire, telegraph, telephone, motorcars, airships, charged cells, factories, draw-engines, newspapers, broadsheets, printing | None. Roads, ships, riders, relays and beacons, workshops and guild halls, heralds and criers, manuscripts, hand-copied bills posted on doors. |
| magitech, patents | Medieval and magical works: guild marks, contraptions that misfire, Runecraft, relics (R82-37). What is built and carried stays medieval. |
| the Imperial Age as the present | The present tense of these pages is the Dark Ages. The Imperial Age is what comes after the turn of the century, a Renaissance of banks and merchant houses, universities and anatomists, full plate, pike and condottieri (R83-4). Name it only as that. |
| old works as city infrastructure | Old works are from the Great Spirit War and the days of the Physical Epochs, when Bara, Ashura and Aegor walked in human form: dead, dangerous battlefields, relics people kill for, and old beings who remember (R83-6). |

Stays exactly: the Soul Crystal, reserve and EU, η, Flux, AU/s, Aether Class, Shell, Core, Layer, Crystal States, Stages, Bands, Tiers, Grades, Sub-Stats, Traits, Releases, Domains, Drafts, tags, Parun and the glyphs, the Eight Families, the Sixty Wellsprings, all their names and failure modes. Mach figures, MJ figures and other modern measures stay in tables and technical sections: modern science may explain anything, and high-Stage practitioners, Measurewrights and scholars know it through the Aether (R83-11). Instruments are medieval: assay forks, water clocks, brass and glass.

## Canon limits

- Never invent or alter what is fixed: the Sixty Wellsprings, the Glyph Index, the Stage, Band and Tier ladders, the Families, the Archons and Titans, cultures and bloodlines, carded people's facts (R79-11).
- You MAY invent the famous stories, minor historical practitioners, duels, schools, nicknames and petty arts that open a page. Use the naming strata in NATALIE and each culture's sound. Comic names are welcome among commons and soldiers. Do not reuse the sample's names, and grep `wiki/` before naming an invented person, so no name collides with one already used. Vary your openings: section one leaned on bookies, Measurewrights proved wrong, and a named commoner who triumphs and then gets a bill. Find other shapes, such as a recipe gone wrong, a lawsuit, a funeral, a smuggler, a child's rhyme, a shipwreck, a guild feud.
- Most of these pages are PUBLIC. Do not use the main cast, sealed secrets or plot of archived scenes. Prefer invented figures of past generations. No events of Arcs One to Three outside the Ages pages. Check facts with the WOTR MCP tools (`wiki`, `character`, `scene_recall`, `codex`, `rule`) or by reading files when you need them.
- Hands off other creators' material: Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai (also Chuluun), the Zettari, Shaka-Al, Dougou, Kushara. Leave what is on the page; add nothing about them.
- `sources/` and the Master Codex outrank wiki pages for numbers, and R83 outranks them for the setting. If a canon source still says guns or the draw, follow this brief and report it.
- Do not settle a contradiction silently. Make the call that lets the writing go on, and report it under `calls` with its grounds. The session that launched you logs it.

## Passages that must not change

The validator requires these exact sentences, so keep each word for word on its page. A retired word inside one stays, and you report it.

- None in your scope.

## THE TEST: nothing machine-age in a costume

Isaac moved WOTR to a medieval world running on old magic because he did not want the 1800s. For any object, trade or institution: is it made by hand, scarce, local and personal, the way things are in a medieval world or in Final Fantasy and Tolkien? Or is it a modern appliance, mass service, network, timetable, product line, factory, bank, newspaper or police force with a fantasy name? If it is the second, it goes, with no renamed successor, and you report it. Real medieval history is the best replacement: guild wars, cloth towns and weavers' revolts, the Venetian Arsenal, carriers and river barges, relay riders and beacon chains, scriveners, sworn notaries, watchmen, reeves, sheriffs, tithe barns, money-changers and factors. Use `mcp__wotr__lookup` (wikipedia) for real detail. Wondrous one-offs, relics, a Guild master's misfiring contraption, fairground wonders and costly hand-made magical things all pass.

Figures tied to a thing that fails the test go with it. Laws about Grades, Tiers, Stages and costs always survive.

**The Grand World.** The present, 715 IC, is before Malakar's split. The Dark Ages open in the Grand World, one landmass, and the split comes about 740 IC. Read Section VI of `wiki/Cosmology & Metaphysics/Ages and Reckoning/The Concordance of Ages.md`. Old World, New World and the Four Quarters read as regions of it. Where a page has an ocean between quarters, or puts a people's history after a split that has not happened, make it fit and report the call. Do not narrate the split or Arc events beyond what Section VI gives.

**C-164.** The Long Reading's "split" is a first blow on the white shelf about 310 IC, which the Moto registers call the split; the Refusal and the Stay fall there, the Long Diminishment follows, the Recension stays two to four generations before Muken. The great split proper comes after Muken and he survives it. Kharven-Seat already stands before Muken, who takes its crown and does not build it. Revise any page you hold to this, and give Muken no death.

**Names.** Filenames stay unless a page's title names a retired thing (The Powers of the Imperial Age, for one); then move it in your folder, give it a new title and report it under rename.

**In-world documents** (the Alftian Codex, papers, letters) are sealed historical texts in old hands: keep their voices, make targeted setting fixes, and keep any opening they already have. They need no spectacle opening.

## The library (R82-9, R82-20 to R82-23)

These are art pages, so the entry shape in `desktop/ABILITY_PIPELINE.md` and the Technique entries paragraph in `desktop/NATALIE.md` govern. Rebuild each page as: the art's new name in caps with its native-language name and kind if its culture is known; the **hook**, one sentence a kid could repeat with no system words; the **named moves**, a line each, saying what it does and looks like in a fight; **How it really works**, the full account, every law and figure of the old page kept and told as one story of metaphysics and physics with the glyph's boundary condition, its failure mode, and how it fights; a one-line **Cost** and a one-line **Counter** on every art; and a **Numbers** block at the bottom with every exact figure from the old page.

Each page keeps its idea and gains a name with swagger, and the old name survives on the page as the scholars' term (R82-9). One wild concept you can say in a breath (R82-14). Names follow the fighter's culture and sound rules; World, God, Fate and Infinite are allowed, and comic names can be lethal (R82-5, R82-10). Take ideas from `mcp__wotr__lookup` (superpower, vsbattles, hxh, jjk, bleach, worm, lotm, reverend-insanity, fma, wikipedia), and borrow no name, move or character. No two pages may end up with the same new name, so grep `wiki/The Disciplines` and the staged copies first.

**Filenames stay, so that cards and scenes keep linking.** Change the frontmatter `title` and the H1. Anything an archived scene has shown stays true, and an old name becomes what people once called it (R82-46, R82-47). Hands off pages belonging to other creators: leave them unchanged and report them. A short spectacle line may sit above the hook where it earns its place, in the page's voice.

No onomatopoeia in prose. An art's signature sound word, if the old page names one, stays as a single plain data line in the Numbers block, labeled "Sound:", because scenes look it up.

## Settled in section one: use these, do not reinvent them

Read `wiki/The Magic System/Practice and Institution/Who Pays for the Lamp The Living Crafts.md` and the shared-art table in `wiki/The Magic System/The Soul and the Climb/The Color of Essence.md` (Part Six) before you write.

- **Dates.** The IC count stands. The Dark Ages run 690 to 800 IC. The present is 715 IC, its twenty-fifth year. The Imperial Age opens at the turn, 800 IC. "The Nth year of the Imperial Age" reads "the Nth year of the Dark Ages". Do not narrate the split or the arcs on these pages.
- **The living crafts.** Lamp-wardens, ward-cutters, hedge-workers, Core keepers, Guild craftsmen, petty folk arts. Assay posts (old gauge-housings), parish stones (old standpipes), searchers (old inspectors), snuffers (old cutters), Core-tenders (old main-men), fee-walkers (old meter-readers), the beacon line (old wire), kept roads and tuned waystones (old rail). Guild marks for patents.
- **Words.** "Pull" for taking Aether from the environment, "drain" and "spend" for what a working costs. Rich and thin ground in scholars' mouths, fat and lean in the street. Salted ground is worked by hedge-workers so Aether will not pool on it; bled ground has been pulled empty. Core means a worked Wellspring site in common speech; the survey keeps "Wellspring Core" for its top density band; the Crystal's Essence Core is the third sense.
- **Arms.** The word is harness, because full plate belongs to the Imperial Age. Proof-marks are proof against a named bow and bolt at a stated range. A crossbow bolt costs about three coppers. An ordinary bolt carries about 100 J and a heavy steel-bowed arbalest about 440 J. Say bolt where old text said round, shot or ball.
- **Prices.** Coin names and the price table are in `wiki/Geography & the Four Quarters/Value, Coin and Trade/What Things Cost.md`, which another agent is rewriting now: do not state new prices for things it covers, and name money in plain coin.

## The page itself

American spelling only (color, gray, armor, harmonized). No em dashes in anything you write, and replace them in prose you touch; a `—` standing as an empty table cell and the em dashes in existing file and page names stay. No hypophora. No "it's not X, it's Y" and none of its cousins. No fragments for fake emphasis, no narrator moral appended to an image. Explain every invented or system word on first use on the page, as the existing parenthetical glosses do; keep those glosses. NO ONOMATOPOEIA, anywhere in a wiki document (Isaac, 2026-11-05): no written sound effects, no stretched noises, no comic word-sounds, in italics, capitals or plain. Say what happened in ordinary words. Every word chosen fresh: do not reuse the sample's images.

## Sample of the method (illustrative, not canon; learn the method, take nothing from it)

> Ask anyone at a Stage bracket what they paid to see and they will say the coat. When Big Hollis Vane of the Tannery Street Rakes took a quarry hammer across the ribs at the midsummer brackets, his aura went from the color of wet clay to the color of an open forge door in the time the hammer took to arrive, and the hammerhead left its haft and went into the third row, where it broke a bench and a bookie's foot. Vane had been six to one. He stood there in a torn yellow shirt, laughing, with four hundred people on their feet, and the Measurewright in the judges' box, who had told everyone the hammer would win, spent the evening explaining why the hammer had been right.
>
> What the crowd saw is called reinforcement on a Guild roll, and in Tannery Street it is called coating up. ...

Then the page's full technical account follows.
