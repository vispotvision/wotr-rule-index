# Wiki rewrite brief: three Paths, no Typology, the lens

You are rewriting part of the War of the Realms wiki, an Obsidian vault at `wiki/` in `/home/oridon/wotr-rule-index`, to a new law. Read these first: `desktop/NATALIE.md` from "**Paths, layers and Essence" through the two paragraphs after it; `rules/doc-directions-2026-11-05-paths.yaml`; `imports/drafts/paths-rewrite/DESIGN.md`; and the finished keystone page, `wiki/The Magic System/The Soul and the Climb/The Three Paths Routing, Recognition and the Gate.md`. Match that page's content and voice. The author decided all of this and it is not open for debate; make any small call yourself, and report it.

## The law in short

- Essence Typology is retired everywhere. Nothing is a "Caloria soul". A blow's character comes from Wellspring and Path; compatibility from how a Wellspring's kind sits with the Path; a Primary Trait from origin, first imprint and the lived Path; class trajectory from how the person has lived. The old lens line ("double a person's natural Typology") becomes: the lens reaches double with years of mastery at its home Path, half again at most away from it.
- Three Paths: Body (Physical World, Aether Shell), Spirit (Soul Plane, Essence Core), Fate (Plane of Fate, Attraction Layer). Attraction is the shallow end of Fate. "Attraction Path" becomes "Fate Path" and an Attraction gate becomes a Fate gate at the same Stage and Grade. **Attraction Force, Obsession Force, the Attraction Layer and Harmonics stay as they are.** Avoid leaving "Fate and Fate Path" stutters.
- Mastered, Walked (30 percent of practice or more), Studied. One Path, two (about 2.5 times the time, three-quarter force bonus each, rough seat, the Path behind a Stage late), three (about 6 times, half bonus, two Stages late, high Grades shut, looked down on).
- Wellspring kinds are qualifiers naming a home plane, never a lock. Wild (33), Spirit (15), Fate (6), Medium (6, at home on all three). The list is in R85-17. Spirit Wellsprings usually do little or nothing to the physical world and give no fire. Fate-type ground: luck goes strange, oaths bite, strangers keep meeting.

## House rules for wiki pages

- Written in the in-world scholar's voice: a Guild archivist or Measurewright, dry and enjoying itself. Never mention the author, rule ids, rulings, "retired", questionnaires or how the wiki is made. Say what is true. Where an old idea needs burying, an in-world line is fine ("older books sort souls by an inborn bias; the trade has given that up").
- American spelling. No em dashes in prose. No onomatopoeia in documents. No "it's not X, it's Y". Explain a specialist word at first use, as the pages already do.
- Keep everything else. Never trim a passage just because it is near your edit. Change what the law changes, make the page read as if it was always this way, and leave links working. Do not invent new numbers beyond the law. Sixty names, Families, Codex analogues, Glyph lines, Spirit "Temperance through" lines and Failure names stay.
- Do not touch `sources/`, `RULINGS.md` or `rules/`. Do not commit; an autosave handles the wiki. Do not edit files outside your group, since other agents are working on the rest at the same time. If a page outside your group needs something, report it.

## The gate

`rust/target/release/wotr-mcp validate` must print PASS. Some wiki sentences are quoted word for word by rules, and if you reword one the gate fails with that rule's id. When it does, restore the quoted sentence exactly (`git log -p -- "<file>"` has the old wording) and put the new truth in a sentence beside it. Run it after each page or small batch, and treat a failure you did not cause as another agent's work in progress: re-run it shortly.

## Your report

Under 200 words: pages changed, anything you invented that the author may want to overturn, anything left undone and why. Do not claim what you did not check.
