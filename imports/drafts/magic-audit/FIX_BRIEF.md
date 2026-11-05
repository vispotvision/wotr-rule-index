# Magic audit: fix brief

Isaac told Natalie to rule the audit's big questions and fix the rest. The findings are in this folder: `wellsprings.md`, `mechanics.md`, `connections.md`, `flow.md`. Their "Path aliases" and shorthand explain the file names. Line numbers may have drifted; find the quote.

## How to work

Go through all four reports. Fix every finding on a file in your set, following its Fix line. A finding that names files in two sets: fix your side only. Where a Fix line and a ruling below disagree, the ruling wins. Edit live pages in place with the Edit tool, in small changes. The wiki autosave commits `wiki/`, so do not commit.

Before changing a number, recompute it. Change only what a finding calls for: no rewriting for taste, and keep the stories and the scholar's voice. A page that is not in your set stays untouched, even if it is wrong; report it instead.

## The rulings (law, in desktop/NATALIE.md; do not re-argue them)

- **η (R85-3):** from the first class at Glory, the Aether Class tier sets η. The Tier of Standing table is the figure for the unclassed at Stages I to V and a field average above them; a read Class overrides it, and a card's own figure governs its holder.
- **AU/s (R85-4):** AU/s is Flux Density times η, the rate spent at full output, and delivered power is AU/s times η. η counts twice on purpose: once for how much the Shell can move and once for what survives the trip. At full output a higher η empties the reserve faster; for the same delivered effect it lasts longer. No published figure changes.
- **The cap (R85-5):** read from the sustainable Grade on the card. A transient boost passes the Stage's ceiling lawfully inside the cap; only a lasting forced stat takes Part Five's fracture rate. Outside help adds no risk unless it is forced on someone, and a blessing counts as outside help.
- **Domains (R85-6):** a seed as the Catalyst into Stage VII is a one-time flicker of the person's own Trait at the Threshold and needs no Release. The Second Release later lets a seed be called and held; from Stage VIII it is a true Domain, grown by living and called aloud. The Catalyst into Stage IX is a first flicker of a Realm on the same terms; the Third Release makes one. The Stage grants a Domain and a Grade never does. Fields clash by Stage first, a field two Stages up overwriting the lower, and otherwise Dominion holds the ground and a read can flip it.
- **Vohrin (R85-7):** outside the Sixty, which stay fixed. A Titan's power that can be worked at Wellspring level, with a marked note on the Caloria page (analogue, failure, signature) as the register's one exception. A cold site is a Titan-touched site. Frost arts keep the floors their pages state.
- **Spirit lines (R85-8):** every one carries Fracture of Worlds' "Temperance through" name (`~/wotr-vault/true-canon/Fracture of Worlds.md`), with the confessors' reading kept beside it.
- **Stones (R85-9):** a monster's stone and parts are read from the beast's own Grade and Level on the coil. T stays the shorthand for danger and price, and most beasts line up with it.
- **Aura (R85-10):** every woken aura shows its own hue from the first Stage, clouded and smoky low down, clearing as the Stage rises.
- **Vows, Munahi, purse (R85-11):** Munahi (February 29) is the day the law sleeps and Fate does not: no instrument binds, and a vow spoken on it still holds. A broken vow lands at once by its own terms and needs no witness; repeated denial of the truth behind it makes a Shear Break. A purse can buy the Catalyst for any Stage; at Zenith a Hollow Throne must still recognize the buyer, so money buys the attempt and not the seat.
- **Calendar (R85-2):** the real one, with a 24-hour day. Year counts stay. Old papers in The Alftian Codex stay as written.
- **Named crafts are gone (R84-18):** Spellcraft, Runecraft, Magicraft and Chantcraft do not exist as kinds. A page's `**Craft** ·` field becomes `**Skill** ·`, naming the skill and how the working is held.

Pages that already follow the law on something are right. These law sections are the test for everything else: THE SHEET AND THE CLIMB, ABILITIES AND THE WORLD, THE MAGIC FRAME.

## Rules for the pages

- Public pages never mention Isaac, rule ids, R-numbers, the audit or the process. Put the fact in the hall's voice.
- No sound words in documents. American spelling. No em dashes. No guns, no draw or mains language, nothing machine-age.
- Never invent the Sixty, the Glyph Index, the Stage, Band and Tier ladders, the Families, the Archons and Titans, cultures and bloodlines, or carded people's facts. If a fix needs that, leave it and report it. Anything else you may invent when nothing on file covers it, and say so in your report.
- Never touch `sources/`, `scenes/`, `lore/v1/`, `book/`, `RULINGS.md`, `CONFLICTS.md`, `rules/`, `desktop/NATALIE.md`, or any character card.
- New pages being written: `wiki/The Magic System/The Soul and the Climb/Domains.md` and `wiki/The Magic System/Practice and Institution/Vows and Oaths.md`. Link to them by those paths. Natalie renames `The Four Crafts` and `Unified Taxonom` afterward, so keep using the current paths.

## Report back

Under 250 words: counts fixed and skipped, every invention worth overturning, and anything you left open and why. Check your own edits with `git diff --stat` before reporting.
