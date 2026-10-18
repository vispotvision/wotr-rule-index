# Card update brief (2026-10-17)

You are converting ONE War of the Realms character card to the current card law. Isaac's
answers are in `imports/drafts/card-update/answers.json`. Do NOT call the `natalie` tool: `desktop/NATALIE.md`
replaces it. If any wotr tool call is refused or unavailable, read the files directly
(desktop/NATALIE.md, rules/*.yaml, wiki/, the card) and carry on; never stop without producing
the card. Read before writing:

1. `desktop/templates/CHARACTER_CARD_TEMPLATE.md` — the one skeleton. The head is required;
   every section after it is a menu (keep what the character has, drop empty sections).
2. `desktop/NATALIE.md`, sections THE MAGIC FRAME (Power on the page, How the systems
   connect, release forms), and COMPANION DOCS (Technique entries, Character sheets).
3. Through the wotr MCP: `load_rules(tags=["character-sheet","stats","magic-design","codex","naming"])`,
   then `fow_line(<name>)` and `character(<name>)` for the figures. Use `codex` to look up any
   Wellspring, Family, Glyph or Physics Domain you name.

## Sources by field (R79-10)
Fracture of Worlds for system law, tables and names; the Stat Sheet (fow_line) for the
character's figures; the card for person facts and wherever the sheet is silent. A missing
figure is derived from the Fracture of Worlds tables and written plainly.

## Keep
- EVERY fact, figure, name, technique, Trait, quote, relationship, fracture and lore paragraph
  on the existing card. Nothing is dropped. Move material into the skeleton's sections; keep
  the existing sentences as written (re-cutting, not rewriting). Lore stays under `## Lore`
  with its sub-headings.
- The `**Say it**` pronunciation (as the Identity Pronunciation line).
- Existing em dashes in names and old text may stay; NEW text you write uses no em dashes.

## Build and fill (canon on use; Isaac strikes what he dislikes)
- The full one-screen HEAD from the template, every line.
- Frontmatter per the template (type, title, subtitle, culture, rung: full, as_of, sources, pc,
  owner). Keep `title` as the card's current title. `pc: true` only for Isaac's own
  characters or other creators' (Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai/Chuluun),
  with `owner:`; otherwise `pc: false` and no owner line. If the card or wiki does not say,
  `pc: false`.
- Missing required pieces, derived from what the card already says about this person:
  Refusal, Conviction, aura colour (Family hue at Stage clarity) and signature sound, combat
  grammar (Verdict | Blade | Percussion | Expenditure), a tell and a counter for every Trait
  and technique (the counter fair and within reach at the technique's own Stage on known law),
  Voice block with speaker type and a sample line (keep an existing sample line), physical
  description if absent (hair by comparison, face, body, clothing with fit and wear, marks).
- RELEASES for Stage IV and above: First Release from Stage IV, Second from VII (opens and
  powers the Domain), Third from IX. Each: a name in caps, folk name in the culture's tongue,
  form, sound, what it does, drain as time from a full reserve, limit, what is lost released
  silently, counter. Built from the character's own Traits and Wellsprings. Bonded weapon line
  (a named weapon on the card may carry part of a release; otherwise "none").
- Never invent: Wellsprings outside the Sixty, Glyphs, Stage/Band/Tier names, Families,
  Archons, Titans, cultures, bloodlines. Never change an existing card fact. For other
  creators' characters: re-cut only, add NOTHING new (no releases, no Refusal), and list what
  is missing instead.
- Plain everyday words in technique entries (R76). Figures inline.

## Output — exactly this, nothing before it
The complete converted card as markdown, starting with the frontmatter `---`. Then a line
containing only `=== ADDITIONS ===`, then a bullet list of every item you invented or derived
(field: value, one line each, and for derived figures the table you used). Then a line
`=== DOUBTS ===` and any fact you could not place or any conflict between card and Stat Sheet
(both values quoted). Do not print anything else.
