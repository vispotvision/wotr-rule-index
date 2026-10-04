# Prose law quick check

`verify_scene` or `build/verify.py` is the authority; every finding carries a
rule id or a Table Rule number. The grep list below is a spot check when both
are down or a finding needs locating. The reading pass runs after the checker
either way. Grep by bash, never by eye.

## Grep pass (the draft is already a file: /tmp/wotr-drafts/<slug>.md)

```bash
f=/tmp/wotr-drafts/<slug>.md
wc -w "$f"                                    # set piece: 2,500 minimum
grep -n '—' "$f"                              # em dashes: zero
grep -nE ' like |the way |as if|as though' "$f"      # similes: rationed, read each
grep -nEi "(isn't|wasn't|is not|was not|it's not|not just) .{0,40}(but|it's|it was|,)" "$f"   # "not X, Y" family
grep -nE 'Not [a-z]+\.$|No [a-z]+\. No ' "$f"       # countdown negation
grep -nEi 'now that|as mentioned|as you know|in other words' "$f"   # signposting
grep -nE '\?$' "$f" | tail -1                 # last line must not be a question
grep -c '\*[^*]\{8,\}\*' "$f"                 # italic thoughts: one per named NPC
grep -nE '\b(Grade|Stage [IVX]+|Band|eta|η|EU|AU/s|Sub-Stat)\b' "$f"  # figures: narration only what the POV holds (R70-83), body first (R70-89), blocks only at milestones (R70-80)
grep -nEi 'qi surged|cold glint|sucked in a cold breath|killing intent surged|the steel sang|a grim smile|blood ran cold|every fibre of his being|darkness gathered|power surged through|stronger than ever|a wave of power|stats soared' "$f"  # stock phrases banned in narration (R70-35)
grep -nE '\b(because|since|so that|which is why|as a result)\b' "$f" # causal connectives: legal only in a mouth or a document
```

Combat set pieces additionally: the POV's own school's vocabulary (R70-100;
for a Western blade, HEMA: Zornhau, Krumphau, Zwerchhau, Schielhau,
Scheitelhau, bind, winden, versetzen, nachreisen, abschneiden, measure, tempo,
posta; a Moto POV names a kesa-giri; a foreign school's word arrives in a
mouth), anatomy named where it is cut, a stated fault per
working, the three-stratum account present, a Stat Ledger per named
practitioner in the notes.

## Reading pass (after every grep is clean)

- **The Ladder**: two or more clauses of "X was Y and Y was Z" in one sentence,
  or a concrete observation restated as an abstraction next sentence. Cut back
  to the first concrete noun.
- **The Gloss**: a sentence whose only job is to state the significance of the
  one before it. Deletion test: cut it; if the passage means the same, it stays
  cut. Free indirect discourse is not gloss; the test is whose vocabulary.
- **Local burstiness**, per paragraph: no three consecutive sentences within
  forty percent of each other's word count; the emotional hit is the shortest
  sentence in its paragraph and sits last. Set pieces only: matched pairs are
  exempt, and once a scene the climax may be one long cumulative sentence
  (R70-19).
- **Reification**: two per scene, different abstractions, never at the beat.
  One per page in procedural or ledger scenes.
- **Apparatus**: a perceptive faculty speaks once per scene, delivers a fact
  not an interpretation, is never the grammatical subject.
- **Ignorance quota** met; **misreading budget** spent; no line adjudicates;
  no narration explains why a working worked on its own authority; mechanism
  arrived through at most two of the four voices (a readout sits outside the
  cap, R70-87).
- Fragment-cascade emphasis ("Not slowly."), anaphora and tricolon stacks,
  stacked metaphors, magic adverbs, dead metaphors, hypophora, reaction-shot
  cutaway (a crowd's spoken chorus at a power reveal is legal, R70-72),
  setup-deadpan-reaction beat outside the comic voices and double acts named
  on their cards (R70-113), "rather than" more than once.
- **Paragraphs**: medium is the norm; one-line paragraphs only in a cluster at
  reveals, verdicts, notices and a fight's last beats (R70-20). Third person
  only outside documents (R70-12).
- POV lock held; psychic distance held; no beat overcrowded; value turned.
- Every character's lines fail the swap test.
- Texture came from the Standing Inventory; anything invented is logged for
  entry.

## Terminology

Every capitalised system term matched against `wiki/The Magic System/The
Lexicon of Magic — Master Terminology.md` and the Codex pages beside it. A near-miss (a Stage renamed, a Wellspring misspelt, a Family
misassigned) is a FAIL, not a warning. A term not in source is originated and
flagged.
