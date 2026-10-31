# Prose law quick check

`verify_scene` or `build/verify.py` is the authority; every finding carries a
rule id or a Table Rule number. One verify_scene a turn: fix every FAIL, read
the WARNs, do not loop (R79-2). The grep list below is a spot check when both
are down or a finding needs locating. The reading pass is for set pieces; a
turn takes the checker and goes. Grep by bash, never by eye. Prose carries no
statistics: any sentence-length, rhythm, paragraph-shape or count finding the
checker still prints is retired law and is ignored (R79-3).

## Grep pass (the draft is already a file: /tmp/wotr-drafts/<slug>.md)

```bash
f=/tmp/wotr-drafts/<slug>.md
wc -w "$f"                                    # every in-fiction reply: about 3,500 (R79-1)
grep -n '—' "$f"                              # em dashes: zero
grep -nE ' like |the way |as if|as though' "$f"      # similes: welcome when earned, read each
grep -nEi "(isn't|wasn't|is not|was not|it's not|not just) .{0,40}(but|it's|it was|,)" "$f"   # "not X, Y" family
grep -nE 'Not [a-z]+\.$|No [a-z]+\. No ' "$f"       # countdown negation
grep -nEi 'now that|as mentioned|as you know|in other words' "$f"   # signposting
grep -nE '\b(Grade|Stage [IVX]+|Band|eta|η|EU|AU/s|Sub-Stat)\b' "$f"  # figures: in a fight, mouths only, never narration, no readout (R79-6); blocks only at milestones (R70-80)
grep -nEi 'cold glint|sucked in a cold breath|killing intent surged|the steel sang|a grim smile|blood ran cold|every fiber of his being|darkness gathered|power surged through|stronger than ever|a wave of power|stats soared' "$f"  # exact cliché phrases banned (R70-35); bare killing intent and qi rising or flaring are genre vocabulary (R79-5)
```

Fights, roleplay and set piece alike, additionally: every blow is body, path,
target, result and what it cost, with what the fighter read and the opening he
found shown as behavior (R79-6); fight jargon, Eastern or Western, free and
never required (R79-6); a technique or release called in English or the
speaker's own tongue (R79-6); wounds plain and anime on the page, clinical
names in the notes and a medic's mouth (R79-6); one clear causal line at a
working's first display, the full three-strata account on the card and in the
notes (R79-6); a stated fault per working; a findable way out (R71-8). The
stats decide out of sight: no Stat Ledger, no deciding-row citations (R79-10).

## Reading pass (after every grep is clean)

- **The Ladder**: two or more clauses of "X was Y and Y was Z" in one sentence,
  or a concrete observation restated as an abstraction next sentence. Cut back
  to the first concrete noun.
- **The Gloss**: a sentence whose only job is to state the significance of the
  one before it. Deletion test: cut it; if the passage means the same, it stays
  cut. Free indirect discourse is not gloss; the test is whose vocabulary.
- **Development**: paragraphs follow the mind's movement, as The Weak Grade
  shows; a revelation may take a short line and its consequence gets room; a
  one-line paragraph stands wherever the movement around it earns it (R79-3).
  No rhythm statistic, no count.
- **Reification** by ear, never at the beat (R49-21).
- **Apparatus**: a perceptive faculty is never the grammatical subject.
- **Meaning**: the POV may interpret, remember and draw meaning in narration;
  only a narrator's moral appended after an image stays banned (R79-4).
  Narration may explain what the trained POV understands, and any voice that
  has earned it may explain (R79-6).
- Fragment-cascade emphasis ("Not slowly."), anaphora and tricolon stacks,
  stacked metaphors, magic adverbs, dead metaphors, hypophora, and a reaction
  shot that replaces showing the event (R79-5; named people react to big power
  with their own words and body, R78-8).
- Third person only outside documents (R70-12). Tense and person of his post
  kept on an improvement unless he asks for a conversion (R79-4).
- POV lock held; narration close by default (R79-4); value turned.
- Every character's lines fail the swap test.
- Texture invented where nothing on file covers it stands as canon once the
  scene is archived (R79-4); no Inventory entry is owed.

## Terminology

Every capitalised system term matched against `wiki/The Magic System/Reference
and Craft/The Lexicon of Magic — Master Terminology.md` and the Codex pages in that section. A near-miss (a Stage renamed, a Wellspring misspelt, a Family
misassigned) is a FAIL, not a warning. A term not in source is originated and
flagged.
