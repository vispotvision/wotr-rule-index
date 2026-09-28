# Alchemetrica recovery: the recheck

Checked: `plan.json` (23 md edits), `blockops.json` and `status.md` against the live page (a fresh render, `alchemetrica-now.md`, and a fresh GET of the whole block tree taken at this recheck, 285 blocks, `tree.recheck.raw.json`, fetched by `recheck_fetch.py`, which refuses anything but GET), `changes.md`, `check.md` (F1 to F25, R1 to R7), `conflict-rows.md` (drafted C-136 to C-153) and CONFLICTS.md. Nothing was applied: no `--apply`, no PATCH, no DELETE.

**Verdict: two defects found and fixed in the plan files; everything else stands.** plan.json is unchanged byte for byte. blockops.json went from 28 entries to 40.

## Defects found and fixed

**RC1. Items 22b, 58 and 62 would break the callouts in the wiki mirror.** The recovery carried each callout's new closing paragraph inside the patch of its last child, as a second paragraph after a blank line. `notion_export.block_md` renders a callout's children with `lines.append(f"> {k}")`, which prefixes only the first line of a child. A child holding `A\n\nB` renders as `> A`, a blank line and a bare `B`, so the new paragraph falls out of the callout in `wiki/`, the mirror Natalie reads, and every later `apply_md_edits` run segments it wrongly. In Notion it would also be one block posing as two, beside callouts built of separate paragraphs and empty spacers (checked: 9ebe04db, e15aaeb3 and 56adda16 all alternate spacer, paragraph).
Fixed: 22b is now an `append_children` on 9ebe04db after 40517507 (whose text does not change, so its patch is gone); 57+58 split into a patch of a93c8960 (57's text only) and an append on e15aaeb3 after a93c8960 (58); 61+62 split the same way on bd4caa61 and 56adda16. Each append adds an empty spacer paragraph, then the new paragraph, after an anchor that is today the callout's last child (asserted in `build_recovery.py`, re-verified against the fresh tree). The texts are exactly the recovery's, which are changes.md's with no check correction outstanding.

**RC2. Heading colours: layout did not survive the partial apply, and plan.json would lose more.** Every original heading on the page is coloured: the thirteen H1s brown, the five H2s gray. Blocks written through `apply_md_edits` come out default. The partial apply left six default headings, and one of them is The Four Operations, which was brown until item 13 replaced it (its id is now 3e958200-eb22-81b5-...). plan.json's item 63 replaces The Ladder heading (brown, a4bfd379) the same way, and items 52 and 63 add three more default headings.
Fixed: ten colour-only `patch_block` entries, H1 to H10, text unchanged. H1 to H6 carry the known ids of the six headings on the page now (H5 restores The Four Operations). H7 to H10 carry `"run": "after plan.json"`, `"id": null` and a `find` on the top-level heading's exact text, because their blocks do not exist until the md apply (H10 restores The Ladder). Each find text is unique on the page after the apply.

`build_recovery.py` was changed to generate both fixes (new `append`, `colour` and `colour_after` helpers; its prose scan now also covers appended text), and re-run on `tree.now.json`: plan.json came out identical, blockops.json as described. `status.md` is updated: the rows for 22, 57, 58, 61, 62 and 63, the counts line, a heading-colour table, and the applier notes (the three entry kinds, the post-plan finds, the order constraint on H7 to H10).

## Refutation attempts that failed (the plan holds)

**Nothing applied twice.**
- All 26 text patches: the block's live text, rendered by `notion_export.rich`, equals `old` exactly, and differs from `new`. None is half-applied.
- All six deletes: each block is a child of 74001ca2, has no children, and reads exactly its recorded text.
- All 23 md edits matched exactly once in the tool's own dry run against the live page.
- A sequential simulation on the render also held. Each edit was applied in plan order, then each block patch, then the deletes, and every `old` matched once at its turn. No later `old` occurs in an earlier `new`.
- The new section markers occur once afterwards and never before: The Dead at the Bench, Draftcraft and Provenance, Fermentation begins here, never thins, breach sits with the seller. The landed headings keep one occurrence each: What pays for the work, The Great Work, The Tria Prima, Medicine by the dose, The stages at the bench, The Four Operations.

**Every item the check kept is landed or planned.**
- 71 items in all: 30 landed, 18 in plan.json, 23 in blockops.json.
- Sub-parts accounted for: 9a/9b, 11a/11b, 12a/12b, 15 cells 1 and 3, 16 cells 1 and 2, 18 cells 2 to 4, 22a/22b, 43a to c, 46a/b, 48a/b, 49a/b, 53a/b, 64a to c.
- The landed items were read off the live page and agree with changes.md as the check corrected it. Among them: 12's sister lines, 13 with its table and three subsections, 20's flowchart, 26, 28, 30, 32 to 36 and 38.

**Every correction F1 to F24 is honoured.**
- Landed: F1 and F2 (item 6), F3, F4, F5, F6 and F24 (item 13), F7 (19), F8 (16: cell 3 is word for word the pre-update text, checked against the mirror at HEAD), F21 (30), F22 (26).
- Planned:
  - F9 (48b).
  - F10 to F14 (52): "belongs to Animatria and Vocatia"; "a glyph that states when it ends, such as [Vor] Return"; "filed at Grade V, Mechanica Trespass ... crosses into civilizational breach"; "Tier VI clearance, where a higher numeral is the tighter seal"; "Two inks for two roles."
  - F15 (55), F16, F17 and F8 (63), F18 (65), F19 (67), F20 (70, bold-italic as explicit rich_text), F23 (11b).
- F25: drafted C-136 to C-153 carry the corrected T4, T10, T15 and T2 quotes.

**Nothing the check dropped comes back.** None of these is in any new string or on the page:
- R7's callout "separation".
- F2's "No practitioner spends reserve on a Draft".
- F3's walked-it-himself rule.
- F5's "trade calls it the spiral".
- F6's six-Wellsprings sentence.
- F8's Parunic Echo clause (both places).
- F17's dark glass and grey-wax sentences.
- F19's counter count.
- F1's "settled out of sight".

**No open CONFLICTS row is resolved.**
- C-117: no Levels.
- C-123: grain gets no Grade and "shows in the work".
- C-124: untouched.
- C-125: no author for the treatise.
- C-127: no maker, cutter, holder or consignor rule.
- Rows ruled today (C-092, C-093, C-096, C-097, C-098, C-107, C-109, C-126, C-128) are applied as ruled.
- Every Alchemetrica quote in drafted C-136 to C-153 is present on the page both before and after the apply. C-137 already quotes the post-item-37 "heat is a craft skill".

**Layout (apart from RC2).**
- Table edits go cell by cell.
- Column and callout children are patched in place. No md edit touches a callout, column or toggle.
- No block targeted by blockops.json is replaced by plan.json.
- Callout patches send rich_text only, so each callout keeps its background colour: red for ae8ca74f and 0392a06a; purple for 74001ca2 and b62403c2; gray for 9ebe04db; orange for d472b253 and e15aaeb3.
- No target block, md or block, carries a link, mention, inline colour or code run that a rebuild from markdown would lose.
- The only bold-italic target is f89b740f (item 70), which carries explicit rich_text. notion_publish.rich_text would turn `***X***` into a bold run and a stray asterisk (confirmed).
- `[Vor] Return` passes through rich_text as plain text.
- The new sections land as H1 plus divider between the existing section dividers: 52 goes Rupture, divider, The Dead at the Bench ... then the existing divider and Mechanica, and Mechanica keeps its id. 63 does the same before The Ladder.
- Blocks recreated with new ids: the Rupture paragraph (de40eb5d), the italic lines under items 66 and 67 (6652ca2e, c17ca2bf) and The Ladder heading (a4bfd379). No file in wiki/, imports/, rules/, scenes/ or desktop/ cites any of those ids.

**Clean publishing and prose law.** Every `new` string and appended paragraph was scanned. None has:
- an em or en dash, "rather than", "instead", or a question mark;
- a rule id, conflict id, date, "pending" or "originated" (except the live "Strikings originated", which is the page's own);
- a name from the Codex, Papers or Necrocursica (Furveus, Calla, Draycott, Mu-jin, Malphas, Farrant, Doyun, Venur, Castlefall), or Isaac or Natalie;
- "weeks";
- a numeral Tier ("Tier VI clearance" is F13's deliberate clearance numeral);
- a "not ... but" pair, or a hard-banned word.

The three new "not"s are plain negations: "a Crystal that is not the operator's", "will not be when it matters" (live wording) and "the two will not reconcile". After the apply the simulated page has no em dash.

**The Weathering reprint.**
- 74001ca2 has exactly six children today: b2019093, 2b7ad8b6, 4cc44463, c1ef9eb9, b4bccd01 and 10ff30e9. Three are empty spacers, and three are the reprint in the old wording ("there is no organ to melt").
- All six are deleted, once, in one entry.
- The first print is the callout's own rich_text, which carries C-109's "a Crystal that never woke". It is kept and rewritten to item 12's wording by 12a.
- The Tiered Path callout (ae8ca74f) and its four children are separate blocks and are not touched by the delete.

## Every blockops entry, re-read by GET at the recheck

```
3     OK      paragraph cff508ae  in callout 5ab82929
7     OK      paragraph 656c441b  in callout a12b4997 (column)
8     OK      paragraph 22307f63  in callout a12b4997 (column)
9a    OK      paragraph 884b9420  in callout a12b4997 (column)
9b    OK      paragraph a6af102b  in callout a8bc0f7d (column)
10    OK      paragraph d3b7ff5f  in callout a8bc0f7d (column)
11a   OK      callout   ae8ca74f  top level
11b   OK      paragraph 2094e810  in callout ae8ca74f
12a   OK      callout   74001ca2  top level
22a   OK      callout   9ebe04db  top level
22b   APPEND  9ebe04db after its last child 40517507: spacer, "**Fermentation begins here.** ..."
37    OK      callout   0392a06a  top level
39    OK      paragraph 41a241b2  in callout 28ba766d
43a   OK      callout   b62403c2  top level
43b   OK      paragraph 6d50c8f5  in callout b62403c2
43c   OK      paragraph 212d5d8f  in callout b62403c2
46a   OK      callout   d472b253  top level
46b   OK      paragraph eaf051fd  in callout d472b253
50    OK      paragraph ef81d04e  in callout 9640dd07
54    OK      callout   e15aaeb3  top level
55    OK      paragraph a9ea02c1  in callout e15aaeb3
56    OK      paragraph 2d1476dd  in callout e15aaeb3
57    OK      paragraph a93c8960  in callout e15aaeb3
58    APPEND  e15aaeb3 after its last child a93c8960: spacer, "**It leaves a residue that never thins.** ..."
60    OK      paragraph 1d026a6e  in callout 56adda16
61    OK      paragraph bd4caa61  in callout 56adda16
62    APPEND  56adda16 after its last child bd4caa61: spacer, "**The breach sits with the seller.** ..."
71    OK      paragraph ea1256a0  in callout cb516ce8
70    OK      paragraph f89b740f  top level (explicit rich_text)
12b   DEL OK  b2019093 ''  ·  2b7ad8b6 'Which means they do not temper...'  ·  4cc44463 ''
              c1ef9eb9 '*The catalyst network is grain, described...'  ·  b4bccd01 ''
              10ff30e9 '**No instrument in the Accord reads grain.** The gates above Tier Five...'
H1    OK      heading_2 3e958200-eb22-818f  What pays for the work      default -> gray
H2    OK      heading_1 3e958200-eb22-81f2  The Great Work              default -> brown
H3    OK      heading_2 3e958200-eb22-8158  The Tria Prima              default -> gray
H4    OK      heading_2 3e958200-eb22-8192  Medicine by the dose        default -> gray
H5    OK      heading_1 3e958200-eb22-81b5  The Four Operations         default -> brown
H6    OK      heading_2 3e958200-eb22-8115  The stages at the bench     default -> gray
H7    AFTER   heading_1 "The Dead at the Bench" (0 now, 1 after plan.json)         -> brown
H8    AFTER   heading_1 "Draftcraft and Provenance" (0 now, 1 after)               -> brown
H9    AFTER   heading_2 "What the bench can read, and what it cannot" (0 now, 1 after) -> gray
H10   AFTER   heading_1 "The Ladder" (1 now, deleted and remade by 63; 1 after)    -> brown
40 entries, 0 BAD
```

## Final dry run

Command: `cd /home/oridon/wotr-rule-index && bash build/py.sh build/apply_md_edits.py /home/oridon/wotr-drafts/alchemetrica/plan.json` (no `--apply`), exit 0, all 23 matched once, no MISS. Raw output in `dryrun.recheck.txt`, labelled here by item (`dryrun.recheck.items.txt`):

```
41     table: 1 row(s) edited, 0 deleted, 0 added
42     table: 1 row(s) edited, 0 deleted, 0 added
44     edited in place
45     edited in place
47     edited in place
48a    table: 1 row(s) edited, 0 deleted, 0 added
48b    table: 1 row(s) edited, 0 deleted, 0 added
49a    table: 1 row(s) edited, 0 deleted, 0 added
49b    table: 1 row(s) edited, 0 deleted, 0 added
51     edited in place
52     replaced 1 block(s) ['paragraph'] with ['paragraph', 'divider', 'heading_1', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'paragraph']
53a    edited in place
53b    edited in place
59     edited in place
63     replaced 1 block(s) ['heading_1'] with ['heading_1', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'heading_2', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'divider', 'heading_1']
64a    table: 1 row(s) edited, 0 deleted, 0 added
64b    table: 1 row(s) edited, 0 deleted, 0 added
65     table: 1 row(s) edited, 0 deleted, 0 added
64c    table: 1 row(s) edited, 0 deleted, 0 added
66     replaced 1 block(s) ['paragraph'] with ['paragraph', 'paragraph']
67     replaced 1 block(s) ['paragraph'] with ['paragraph', 'paragraph']
68     edited in place
69     edited in place
```

## For the applier

- blockops.json now has three entry kinds, and status.md says how to send each: `patch_block`, which may carry `color` or explicit `rich_text`; `append_children`; and `delete_blocks`.
- H7 to H10 run after plan.json. Everything else can run in either order against plan.json.
- `build_recovery.py` keys `by` on the first eight characters of an id. The 46 blocks the partial apply created all begin `3e958200`, so they collide. No `txt()` or `patch()` call reads one, and `colour()` takes full ids, but any future edit to the script must not look those blocks up by short id.

Files: /home/oridon/wotr-drafts/alchemetrica/recheck.md, /home/oridon/wotr-drafts/alchemetrica/plan.json (unchanged), /home/oridon/wotr-drafts/alchemetrica/blockops.json, /home/oridon/wotr-drafts/alchemetrica/status.md, /home/oridon/wotr-drafts/alchemetrica/build_recovery.py, /home/oridon/wotr-drafts/alchemetrica/recheck_fetch.py, /home/oridon/wotr-drafts/alchemetrica/tree.recheck.raw.json, /home/oridon/wotr-drafts/alchemetrica/dryrun.recheck.txt, /home/oridon/wotr-drafts/alchemetrica/dryrun.recheck.items.txt
