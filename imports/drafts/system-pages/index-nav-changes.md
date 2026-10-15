# Index and navigation changes for newcomers

*Concrete edits to the Notion wiki and to the mirror's wiki/INDEX.md, to go with Start Here. Nothing here has been applied. Each item says where the change is made: in Notion by hand, or in the repo.*

## 1. Put Start Here at the top

- **Notion.** Create Start Here as a top-level page of the wiki (parent: the wiki page `3b158200-eb22-81c6-b008-dcc414a561d0`, never a sub-page), and add one line at the very top of the wiki's home page: "New here? Read **Start Here** first." Its Tags: leave empty, or add a new option "Start Here" (see the next bullet).
- **Notion, the default view.** The only views are "All pages" and "Pages I own", both sorted by last edited time, so a newcomer opening the database lands on whatever was touched most recently. Add a third view, "Read first", filtered to Tags contains Start Here or Glossary, and make it the first tab. Tag Start Here, How Magic Works, A Reader's Codex, The Measures at a Glance, Who's Who: the Starting Threads and Factions at a Glance with it.
- **Repo.** wiki/INDEX.md sorts sections alphabetically, so a newcomer reading the mirror meets "Aberrations (1)" first. In `build/notion_export.py`, where it writes INDEX.md (the `by_section` loop near line 454), write a pinned block before the first section:

  ```
  **New here?** Start with [Start Here](<path>), then the [Glossary](Glossary/A%20Reader's%20Codex.md).
  ```

## 2. Rename "Reference Table" to "Glossary"

"Reference Table" is not a page: it is an option of the wiki database's **Tags** property, and A Reader's Codex is the only page carrying it. The mirror files a top-level page under its first tag, which is why INDEX.md shows a section "Reference Table (1)" holding "A Reader's Codex".

- **Notion.** Database → Tags property → edit the option "Reference Table" → rename it **Glossary**. Renaming the option (rather than adding a new one) retags the page in one move and leaves no orphan option. Keep the page title "A Reader's Codex"; its own glossary section ("A Short Glossary of Forty Terms") is what earns the label.
- **Repo, after the next export.** The page moves from `wiki/Reference Table/A Reader's Codex.md` to `wiki/Glossary/A Reader's Codex.md`. Two things read the old name:
  - `build/lorebook.py` line 29, `SKIP_TITLES`: add `"Glossary"` beside `"Reference Table"` (keep both until the old folder is gone).
  - `CONFLICTS.md` (line ~597) cites `Reference Table/A Reader's Codex.md`. That file is a record; leave the old path standing and do not rewrite it. Book briefs under `book/` are generated and will pick up the new path on their next build.

## 3. Take "Information not on WIKI" off the newcomer route

**What it is.** "Information not on WIKI" (`3d958200-eb22-80a4-b8f3-cc2c16241f7d`) is a private page that was deliberately moved out of the wiki database. The exporter crawls it by hand (`PRIVATE_ROOTS` in `build/notion_export.py`), and because it has no Tags it lands in the mirror under "Misc", while its children appear as a section of their own, "Information not on WIKI (8)", early in the alphabet.

**The snag.** It is not only author files. Four of its eight children are wiki content a newcomer needs:

| Child | What hangs under it |
|---|---|
| Characters `3b158200-eb22-8188-b4d8-d9b195f254dd` | Volume I — Character Cards (every card) and Mara Venn |
| In-World Documents & the Narrative Archive `3b258200-eb22-8131-9fac-d195197bddc3` | **The Scene Archive** (every scene, the reading order, cast index, timeline), the Accord, the letters, the memoir, the Apprentice's Primer |
| The Disciplines `3b158200-eb22-810f-a709-d122245d7ab8` | The 21 discipline pages (Spellcraft, Kami no Kobushi, Hataraki and the rest) |
| Artifacts `3d958200-eb22-8135-aecf-cee1b6c2cd65` | The artifact pages |

The other four are working files that belong off the route: Bram Greymane's Narration Register, Lorn Stark's Narration Register, The Moto Narration Register, Pack Twenty — The Clearance (plus the link to The Rule Index).

**The edit (recommended).**
1. In Notion, move Characters, In-World Documents & the Narrative Archive, The Disciplines and Artifacts back into the wiki: drag each onto the wiki page (`3b158200-eb22-81c6-b008-dcc414a561d0`) so it becomes a database row again, then set Tags: Characters → `Characters`; The Disciplines → `Disciplines`; In-World Documents & the Narrative Archive → `In-World Document`; Artifacts → `Lore & History` (no Artifacts option exists; adding one is fine too). Their sub-pages move with them, links do not break (Notion links by id), and every id in NATALIE.md stays valid.
2. Leave "Information not on WIKI" holding only the three narration registers, Pack Twenty and the Rule Index link. Rename it **Author's Workroom** so nobody mistakes it for content, and keep it outside the wiki (private, not shared with guests).
3. Never link it from Start Here, the wiki home or any published page.
4. In the repo, have the exporter list private-root sections last in INDEX.md under a heading "Not part of the wiki", instead of sorting them in with everything else: in `notion_export.py`, sort sections with `key=lambda s: (s in private_sections, s)`, where `private_sections` is the set of sections whose pages came from `private_ids`. Also give pages under a private root the section name of the root rather than "Misc".

**Why this needs a yes before anyone acts.** Moving those four pages out of the wiki was a deliberate choice (the exporter's comment records it as done "to keep it off the public wiki"). Step 1 reverses it. If the cards and scenes are meant to stay private, skip step 1, do steps 2 to 4, and Start Here must drop its Scene Archive and character card links, because a friend outside the workspace cannot open them.

## 4. The "Continuity map" links in the Scene Archive

**They are not scenes.** All forty-four pages titled "Continuity map" under The Scene Archive are copies of one page: the repo's `scenes/CONTINUITY.md`. Between 2026-09-22 and 09-25 the hourly sync created the page, then failed on a table longer than Notion's 100-row limit (`build/sync.log`: "body.children[79].table.children.length should be ≤ 100, instead was 149"), and the next hour created another. Each failed copy stops partway (the four in the mirror are identical, 6,820 bytes against 245 KB for the full map). The nightly reconcile already lists it as "Continuity map ×43". The live copy is the one `build/.notion_publish.json` updates: `3e658200-eb22-81f3-b54f-ec54cb058ff8` (the mirror skips repo-published pages, which is why INDEX.md shows 43, not 44).

So a "thread + number + scene title" label cannot be given to them: none of them belongs to a thread. The edit is one rename and forty-three removals:

- **Rename the live page** to **Continuity Map: How the Scenes Connect**. The publisher only replaces the body on update (`replace_body` in `build/notion_publish.py`), so a title set in Notion stays.
- **Move the other forty-three to the Notion trash** (recoverable for thirty days; nothing links to them, and the repo holds the full text). Do this by hand in Notion.
- Optional: change the H1 of `scenes/CONTINUITY.md` to match, so a future re-creation gets the same name.

| # | Notion id | Old label | New label / action |
|---|---|---|---|
| 1 | `3e358200-eb22-813f-988c-cfe973b55fee` | Continuity map | trash (stale partial copy) |
| 2 | `3e458200-eb22-81dd-981b-f73430ece0b7` | Continuity map | trash (stale partial copy) |
| 3 | `3e458200-eb22-81b5-b608-e58e81694c3e` | Continuity map | trash (stale partial copy) |
| 4 | `3e458200-eb22-81b7-a383-d31b23e09b56` | Continuity map | trash (stale partial copy) |
| 5 | `3e458200-eb22-8112-abe3-f60f8443ee96` | Continuity map | trash (stale partial copy) |
| 6 | `3e558200-eb22-8127-b8b1-eba89a6fb293` | Continuity map | trash (stale partial copy) |
| 7 | `3e558200-eb22-811b-9453-e0b5455edbb5` | Continuity map | trash (stale partial copy) |
| 8 | `3e558200-eb22-81ea-b65b-f45cc25e14d0` | Continuity map | trash (stale partial copy) |
| 9 | `3e558200-eb22-81c9-ac86-dbbedb075f72` | Continuity map | trash (stale partial copy) |
| 10 | `3e558200-eb22-8143-84d2-cd6d87366e1f` | Continuity map | trash (stale partial copy) |
| 11 | `3e558200-eb22-8127-ace5-ca402dc6af2b` | Continuity map | trash (stale partial copy) |
| 12 | `3e558200-eb22-81c0-a58a-ee77beb92f63` | Continuity map | trash (stale partial copy) |
| 13 | `3e558200-eb22-81b2-ab6d-cb283653048f` | Continuity map | trash (stale partial copy) |
| 14 | `3e558200-eb22-81e7-b9cf-e4552c83479c` | Continuity map | trash (stale partial copy) |
| 15 | `3e558200-eb22-81b3-a429-c7a47c8a7f6c` | Continuity map | trash (stale partial copy) |
| 16 | `3e558200-eb22-81d1-99e0-d950ebf03759` | Continuity map | trash (stale partial copy) |
| 17 | `3e558200-eb22-81c7-b65c-f1af1608f07a` | Continuity map | trash (stale partial copy) |
| 18 | `3e558200-eb22-815c-bf6a-cce24cbd3ba7` | Continuity map | trash (stale partial copy) |
| 19 | `3e558200-eb22-81ad-815e-c566aca0bbbe` | Continuity map | trash (stale partial copy) |
| 20 | `3e558200-eb22-8139-9500-c265943dfc2c` | Continuity map | trash (stale partial copy) |
| 21 | `3e558200-eb22-81a3-8c2c-f7f84422c9f9` | Continuity map | trash (stale partial copy) |
| 22 | `3e558200-eb22-81f6-80cb-c72be6326062` | Continuity map | trash (stale partial copy) |
| 23 | `3e558200-eb22-810e-a6a2-e4b019927429` | Continuity map | trash (stale partial copy) |
| 24 | `3e558200-eb22-8171-bf1d-ca897bd86747` | Continuity map | trash (stale partial copy) |
| 25 | `3e558200-eb22-8100-ab32-e5047cc54521` | Continuity map | trash (stale partial copy) |
| 26 | `3e658200-eb22-8135-8b46-e76bacf75065` | Continuity map | trash (stale partial copy) |
| 27 | `3e658200-eb22-8132-ab76-f4da4a35cc4b` | Continuity map | trash (stale partial copy) |
| 28 | `3e658200-eb22-8156-89d2-e546e4209878` | Continuity map | trash (stale partial copy) |
| 29 | `3e658200-eb22-8175-850f-dcb5899b825a` | Continuity map | trash (stale partial copy) |
| 30 | `3e658200-eb22-816c-88f8-d6e246059ea2` | Continuity map | trash (stale partial copy) |
| 31 | `3e658200-eb22-8151-821f-d5c0c79335b5` | Continuity map | trash (stale partial copy) |
| 32 | `3e658200-eb22-8143-8fbd-dbb3bf65c595` | Continuity map | trash (stale partial copy) |
| 33 | `3e658200-eb22-81e0-8c2e-eeadb2d2fd5b` | Continuity map | trash (stale partial copy) |
| 34 | `3e658200-eb22-8133-a81f-dc50e8372323` | Continuity map | trash (stale partial copy) |
| 35 | `3e658200-eb22-81df-ae07-de818e753bbf` | Continuity map | trash (stale partial copy) |
| 36 | `3e658200-eb22-8107-bc15-fbef696bf84a` | Continuity map | trash (stale partial copy) |
| 37 | `3e658200-eb22-81dd-a290-db5374d187ce` | Continuity map | trash (stale partial copy) |
| 38 | `3e658200-eb22-81e8-a279-c51da58b1987` | Continuity map | trash (stale partial copy) |
| 39 | `3e658200-eb22-8106-9c7a-e8c8fec24d57` | Continuity map | trash (stale partial copy) |
| 40 | `3e658200-eb22-812c-a0f3-e43a771f93b0` | Continuity map | trash (stale partial copy) |
| 41 | `3e658200-eb22-8187-8c00-d6217b8784ed` | Continuity map | trash (stale partial copy) |
| 42 | `3e658200-eb22-81df-9249-c90a00009943` | Continuity map | trash (stale partial copy) |
| 43 | `3e658200-eb22-81a0-bb0b-e54ca83d700f` | Continuity map | trash (stale partial copy) |
| 44 | `3e658200-eb22-81f3-b54f-ec54cb058ff8` | Continuity map | **Continuity Map: How the Scenes Connect** (keep; the live page) |

### The scene links in that section that do need new labels

The rest of the mirror's Scene Archive section is real scenes, and here the same title appears twice or three times, so a reader cannot tell which to open. Label scheme: **thread · number in the placed order · scene title**, where the thread is the scene's thread in `scenes/CONTINUITY.md` (shortened) and the number is its row in that file's "Every scene, in placed order" tables (1 to 148). The copy the repo publishes (`build/.notion_publish.json`) keeps the clean label; a hand-made copy beside it is compared with it first and, if it says nothing the published copy does not, trashed; if it differs, it is kept and marked as an earlier draft.

| Old label | Notion id | Which copy | New label / action |
|---|---|---|---|
| The Turtle's Boy | `3df58200-eb22-81d5-8dd4-df31fc48ec62` | repo-published | **Aetherion Academy · 137 · The Turtle's Boy** |
| The Turtle's Boy | `3df58200-eb22-8125-8b54-edd0ada0056d` | hand-made | compare; trash, or **Aetherion Academy · 137 · The Turtle's Boy (earlier draft)** |
| The Years That Were Not War | `3df58200-eb22-812c-9524-ffc275f92411` | repo-published | **Cozbi and the Six Crows · 8 · The Years That Were Not War** |
| The Years That Were Not War | `3de58200-eb22-81ec-87c4-eb31db90fc8d` | hand-made | compare; trash, or **Cozbi and the Six Crows · 8 · The Years That Were Not War (earlier draft)** |
| The Holy Inquisition, Part 1B: The Empty Chair | `3df58200-eb22-8173-a989-d29de96df36d` | repo-published | **Lambert Inquisition · 135 · The Empty Chair (Part 1B)** |
| The Holy Inquisition, Part 1B: The Empty Chair | `3df58200-eb22-8163-ac24-e2b417882d9e` | hand-made | compare; trash, or **Lambert Inquisition · 135 · The Empty Chair (Part 1B, earlier draft)** |
| `The Holy Inquisition — Part 1B: The Empty Chair` | `3dd58200-eb22-819c-b51d-f81b068151ee` | hand-made | compare; trash, or **Lambert Inquisition · 135 · The Empty Chair (Part 1B, first draft)** |
| The True Religion | `3d958200-eb22-8131-8181-d0c2e426af3d` | repo-published (`sodoku_` file) | **Kharven Return · 49 · The True Religion** |
| The True Religion | `3d958200-eb22-81ba-921a-ef1e86ea5984` | repo-published (`temur_` file) | **Kharven Return · 50 · The True Religion (old Temür names)**. Keep: the map records it as the same scene in the struck name-state, kept as history |
| The Petition | `3da58200-eb22-8112-9ae9-de64f60e8744` | repo-published | **Altherion · 71 · The Petition** |
| The Petition | `3d958200-eb22-8146-bdae-f17bc9bdf8bb` | older copy | compare; trash, or **Altherion · 71 · The Petition (earlier draft)** |
| Star Crusher | `3da58200-eb22-8199-8aaa-cd3b9e472a03` | repo-published | **Altherion · 72 · Star Crusher** |
| Star Crusher | `3d958200-eb22-8138-a949-e51ec20ca83e` | older copy | compare; trash, or **Altherion · 72 · Star Crusher (earlier draft)** |

Rename these in Notion by hand. The publisher keeps a page's title on update, so the new labels survive the next sync. The scheme can be rolled out to every scene page later; these are the only titles that collide today.

## 5. Smaller fixes on the same route

- **"The Magical Categories — Unified Taxonom"** (`3c758200-eb22-819e-8385-c81cd92f8d13`): the title is cut off. Rename to **The Magical Categories: Unified Taxonomy**. NATALIE.md lists the id, not the title, so nothing breaks; update the Start Here mention after.
- **Reading order** (`3d958200-eb22-8105-8af2-fbde5728de07`, under The Scene Archive): last edited 2026-09-13, so it misses every scene since (the Aetherion Academy, Rovhen, Geturo, Hiromi and Class X Open pages among them), and its file names render broken because the underscores were read as italics (`01*wotr*muster...`). For a newcomer, replace the list with scene titles (Notion page mentions) in the thread order of `scenes/CONTINUITY.md`, or put a line at its top pointing to the Continuity Map until it is rebuilt.
- **Single-page sections in the mirror** ("Magic System (1)" holding The Magic System, "Cosmology (1)", "Factions (1)", "Geography (1)", "Peoples (1)", "Materials (1)", "War (1)", "Bestiary (1)"): these are the top-level hub pages, filed under their own tag. Harmless, but in the pinned block (item 1) list the hubs by name so a newcomer does not have to find them in the alphabet: The Magic System, Cosmology & Metaphysics, Factions, Bloodlines & Institutions, Geography & the Four Quarters, Races & Peoples, Materials, Alchemy & Trade, The Bestiary.

---

## Notes (not published)

### Calls made
- **Continuity map labels.** The task asked for thread + number + title for each "Continuity map" link. None of them is a scene (all forty-four are copies of the continuity map, forty-three of them failed partial copies), so the scheme is applied to the scene titles that actually collide, and the copies get one rename and forty-three removals. Evidence: `build/sync.log` 2026-09-24 20:29 to 09-25 16:29, `build/.notion_publish.json` (`scenes/CONTINUITY.md` → `3e658200-eb22-81f3-...`), the four identical mirror files, and the live Scene Archive child list read from Notion on 2026-10-15.
- **Information not on WIKI.** Recommended moving the four content pages back into the wiki, flagged as reversing a deliberate earlier move, with the alternative spelled out. Not applied.
- **Thread short names** in the scene labels are shortened from the CONTINUITY.md thread headings: "Omoro and the Aetherion Academy" → Aetherion Academy; "Cozbi, the Yukari and the Six Crows" → Cozbi and the Six Crows; "The Lambert inquisition (Dabney's sixth year)" → Lambert Inquisition; "Kharven — the return (the eleventh year)" → Kharven Return; "Altherion — the Word of Judger on the frame" → Altherion.
- **Em dashes.** None in this file's own prose. Exact existing titles quoted as old labels or ids keep theirs, since they must match.

### New figures set here
None.
