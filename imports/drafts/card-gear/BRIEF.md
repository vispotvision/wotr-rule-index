# Card gear pass (R85-1)

Isaac, 2026-11-05: armor, outfits, gear, swords and the rarity of weapons and items are a flex, so characters get them described. He approved a pass over the existing cards. Base commit for checking: 069ba832.

Cards live in `wiki/Characters/Volume I — Character Cards/`. Finished examples, read both first: `Rob Stark.md` (a card that had no Equipment section) and `Muken Moto.md` (one that had a good one, section XV). The law is the "Gear is a flex" paragraph in `desktop/NATALIE.md`; the fields are XV. Equipment in `desktop/templates/CHARACTER_CARD_TEMPLATE.md`.

## Sources, in this order

1. The archived scenes in `scenes/` (grep the name with armor, sword, blade, mail, helm, coat, cloak, robe, ring, belt). A scene wins. Do not use `lore/v1/`: that is old lore.
2. The card itself: its head, Physical Description and Lore, and any existing Equipment.
3. The portrait: open `<Name> — portrait.jpg` beside the card with the Read tool and read every piece on the body. Isaac's art.
4. Where those are silent, invent: a maker, a mark, a repair, a rumor, a price. Inventing gear is allowed and canon on use (R79-11), but no invention may contradict a scene, the card or the art. No character's person, history or kit may change.

## What to write

**Insert only.** Never delete, reword or reorder anything already on a card. Use the Edit tool, one small insert at a time. Change nothing else.

1. **Head.** A `**Kit**` line right before the card's `**Voice**` head line: what they wear and carry at a glance, ending on the piece people talk about first, with its Rarity. One sentence.
2. **Equipment.** If the card has an Equipment section, keep every entry, add ` · Grade <letter> · <Rarity> · rung <rung>` to the end of each worked piece that lacks them, and add a `**Look**` line beneath it covering only what the entry does not already say. If it has none, add `## Equipment` right before `## Lore`, following Rob Stark's card. New sections take the card's own heading style.
3. **Every piece worth a look gets an entry:** armor, outfit, weapons, cloak, rings, belts, a mount's harness, court dress beside field kit. Group small plain things.

An entry's first line: name · what it is · Grade · Rarity · stamp · rung · bonded or not · for a weapon, mass and balance · proof-mark if any · for a weapon, the armor it beats and fails against (R13-9).

A `**Look**` line: material, color and finish, cut and fit, maker's mark, wear, repairs and a flaw; **how they show it off**; **what people say**, past owners included for a famous piece (R82-35); a price where one matters.

## The numbers

- Existing Item Tier converts: Plain/Marked = Hollow-F/E, Sidearm · Proofed = D, Linepiece · Tempered = C, Wallbiter · Instrument = B, Siegepiece · Hallowed = A, Fieldwinner · Storied = S to SS, Kingsarm · Found = SS, Kingsarm, or SSS, Landbreaker · Numinous = X to EX, Moonsplitter · Proscribed = EX+, Unmaker. Never contradict a Tier already on the card.
- A plain item has no working, so no Grade or rung: write `plain`. It still gets a Rarity.
- An item's Tier is the lower of what its material can hold and the Tier of Standing of its maker. Fit the owner: a Stage III soldier does not carry a Kingsarm unless the card says so, and if the card does, that is the story.
- Rarity is scarcity, and it is a ladder that must mean something. Common: any market. Uncommon: a good town smith or tailor. Rare: a commission most people could never pay for. Very Rare: a famous maker or a high monster's parts; a city talks about it. Legendary: a realm knows its name. Mythic: lesser relics, Master Works. Unique: Master Works and true relics only (R84-19, R84-35). True relics read as question marks on Grade. Most characters should own mostly Common to Rare pieces and at most one thing above that.
- Prices follow `wiki/Geography & the Four Quarters/Value, Coin and Trade/What Things Cost.md` (an officer's blade is 4 to 7 gold), by ear above it.

## How it should read

- The person shows in how they treat it. A peacock's entry should strut; a miser's or a killer's may be an anti-flex that people talk about anyway. Fit the card's voice and refusal. Don't make every character vain, and don't repeat a joke shape across cards.
- Color and specifics: WOTR is dark shonen, never gray. Name the actual enamel, thread, metal, hide. Culture sets the style: Moto dress is R34-1 and R34-2 (`mcp__wotr__rule` or grep `rules/`), with each Great Line's own metal and palette.
- Dark Ages setting: medieval arms only. No guns, no gunpowder, no machine-age materials, no draw or mains language.
- Keep it card-register, compact, like the examples. No sound words on cards. American spelling. No em dashes. Pronouns follow the card.
- A dead character's kit is written as of the card's "as of" moment.

## Report back

Per card, one line: pieces added, highest Rarity, and anything you invented that Isaac might want to overturn. Note any scene, card or art contradiction you found instead of resolving it. Do not commit: the wiki autosave handles `wiki/`.
