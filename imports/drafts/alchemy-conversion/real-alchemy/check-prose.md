# The Real Alchemy: prose and publishing check

Page: `/tmp/wotr-drafts/real-alchemy/the-real-alchemy.md` (13,672 words, 417 Notion blocks, 18 tables).

## What was run

- `verify.py --band set-piece`: **PASS, 0 fail, 2 warn.** Both warnings are proper names: the agency "Agency for Toxic Substances..." and Conniff's article title with "May". The info lines (italic beats, last line, length band) are scene rules and do not apply. No action needed.
- Grep for em and en dashes, " -- ", question marks outside titles, rule ids (R..-, C-0..), 2026, "pending", "originat", Isaac, Natalie, docket, ruling, and modern slang: all clean. The one "actually" is in the subtitle.
- `build/notion_publish.py md_to_blocks` run on the page: 1 H1, 9 H2, 80 H3, 258 paragraphs, 37 bullets, 5 numbered items, 18 tables (189 rows), 9 dividers. Every table has its separator line and the same column count in every row. No rich-text array hits the 100-object cap, and no stray `*` or `_` is left in the text. The H1 matches the wiki export style (Alchemetrica.md carries its own H1).
- Quotations: every quoted source phrase is in quotation marks with a citation. The longest are 11 words (Wood and Bache, Fowler's lavender, line 566) and 8 words (Lemery on cohobation, line 91). Both are under the limit. Canon quotes (Alchemetrica, Codex) are marked.

## Findings, most serious first

1. **The publisher corrupts the Persée URL (line 943).** md_to_blocks' INLINE regex reads `_0151-4105_` in `rhs_0151-4105_1996_num_49_2_1254` as italics, so the published URL loses its underscores and breaks. Correction: wrap it as a markdown link, `[persee.fr](https://www.persee.fr/doc/rhs_0151-4105_1996_num_49_2_1254)`. The link pattern matches at the `[` before the underscore pattern gets a chance. Or give the DOI, `doi:10.3406/rhs.1996.1254`.

2. **A policy claim in the page's voice (line 5).** "anything new built on that ground is new canon" states a rule about canon that the canon hierarchy does not grant: invented material is labelled, and an estimate becomes canon only when confirmed. Correction: "Where WOTR has no counterpart, the entry says so, and whatever is built there is WOTR's own."

3. **Process notes left on the page.**
   - Line 139, "The research behind this page found no early modern text that gives it in that order." Correction: "No early modern source for that order has been traced."
   - Line 880, "*(The comparison is made here from the two published translations.)*" Correction: "(Compared from Holmyard 1923 and Steele and Singer 1928.)" or cut it.
   - Lower priority, the "was found" wording at lines 227, 243, 289, 414 and 713 ("no period figure for it was found", "No source found says"). Correction: "no period figure is recorded in these sources", "No source names who mixed the lute".

4. **Cited sources the Sources list does not name.**
   - Line 171, "Stirling Consolidated Boiler Co. (1905)" has no Sources row.
   - Line 324, the Source cell reads "secondary summary", with no author or title.
   - Line 727, "Cornish Mining sources" has no row.
   - Line 496, "a history blog" has no name.

   Correction: give each one a Sources row with author, title, year and URL, or cut the claim. The 15½-year Boerhaave row is the obvious cut, since it is also not in his published *Experiments*.

5. **Line 19 gets its referent and its figure wrong.** "The real bench ran them from ten hours to twelve days": the ten-to-twelve hours is the cementation of gold (line 15), not a calcination, and "them" and "Its" have no clear antecedent. Correction: "Real calcinations ran from thirty-six hours (Lemery's tin in a pan) and four days (the same tin in a crucible) to Lavoisier's twelve days, past the Burning's upper figure."

6. **An unmarked close translation (line 488).** "In the German, all things are poison and none is without it. The dose alone makes a thing no poison." This is a near word-for-word rendering of the Third Defence, set as the page's own prose. Correction: mark it as a rendering, for example "The German says, in this page's plain rendering, that all things are poison...". Or set the rendering in quotation marks and label it as the page's own translation.

7. **"The real" as a verbal tic.** The phrase runs 96 times in all and appears in 52 of the 80 "In WOTR" lines. Two lines double it: line 221 "the real smell of the real bench" and line 245 "the real sound of the real mechanism". Line 293 "That is the real egg's account exactly" and line 35 "matches the real share of bench time exactly" add "exactly". Correction: cut the doubled "real" and the "exactly"s. Vary the verdict with "matches", "is attested", "has its period parallel in", or name the source itself ("is Lemery's fire lute").

8. **Gloss and fragment closers.** Line 225 "The lamp mattered." is manufactured emphasis, so cut it. Line 161 "The trade calibrated by the body." and line 307 "It was the price of seeing." sum up the paragraph after the evidence has already made the point. Cut them or fold them into the sentence before.

9. **Overstatement (line 691).** "Men walk out of the room and drown in their beds that night": the page's own figure is a free interval of three to thirty hours. Correction: "Men walk out of the room and drown in their beds hours later, sometimes the next day."

10. **Empty slot (line 416).** "**The fault.** None recorded." Correction: drop that lead-in for this entry, or fold the gap into the practice line.

11. **The same contrast twice.** Line 17 has "follows how long the fire was kept, far more than how fierce it was" and line 633 has "follows the concentration in the air, far more than years of service". Correction: recast one, for example line 633: "Onset tracks the concentration in the air; years of service matter little."

12. **Low priority, for Notion.** md_to_blocks does not turn bare URLs into links, so the Sources URLs publish as plain text. Wrap them as `[title](url)` if they should be clickable. The subtitle's "actually" ("What the laboratory actually did") can go.
