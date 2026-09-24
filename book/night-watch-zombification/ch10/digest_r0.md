Verdict: revise (fail 1, warn 1, dropped 0)

## FAIL [CONTINUITY/canon]
Quote: "The gauge over the door said four degrees, which it had said since the first night."
Problem: Gauge fact is attested twice (ch02, ch06, state.json H07) as four degrees 'since the first division'; the corpus keeps 'since the first night' for other facts. Ch10 swaps the formula.
Fix: Change to '...which it had said since the first division'.

## WARN [shape]
Quote: "# The Ninth Hind"
Problem: Word count 3817 (verifier) against target 3500: 109%, within 80-150%. | verify --band set-piece --culture Accord --combat: PASS, 0 fail, 0 warn. | gap_fill (non-set-piece default band) flags length outside standard 700-1500. | gap_fill stratum audit counts Wellspring 0, Essence 0, Aether 2; physics terms none; mechanism vocabulary none. | gap_fill counts 20 HEMA and 6 anatomy terms in a chapter the notes declare has no contest; 18 paragraphs flagged as physical exchange.
Fix: none | none | none; chapter is set-piece band, verify with --band set-piece passes | Confirm in review that the directional law and Essence stratum ('no Crystal in her') read on the page; no change needed if so | Ordinary-word regex hits likely; reviewer to confirm no stray combat vocabulary
