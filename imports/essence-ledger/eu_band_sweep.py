#!/usr/bin/env python3
"""WAR-46 — the R44-1 EU-band sweep. Reads imports/essence-ledger/fit.json and
writes reports/eu_band_sweep_2026-09-25.md. Reads only; changes no card figure.

Regenerated for WAR-71 against the corrected fit: every figure is now read
against the Stage its own line states where its table gates each row, and the
Tier 5 η is R44-4's. The `GATE` reason is gone with the defect it recorded."""
import json, math, re, collections

FIT = json.load(open('imports/essence-ledger/fit.json'))
ROWS = FIT['reserves'] + FIT['costs']

# --- the twelve cards C-040 names, taken from the same file's own strike rows ---
C040 = sorted({r['entity'] for r in FIT['grade_proxy_check']['rows']
               if r.get('measure') == 'strike' and r.get('grades_apart') not in (0, None)})
assert len(C040) == 12, C040

# A line is not a card figure only where it says so of itself. "extrapolated" is
# deliberately not a trigger: Aurelian Prudentius's reserve says how it was arrived at
# and then says it "stands as final", which is a stated card figure.
NOTCARD = ('not stated on the card', 'an estimated', 'estimated ', 'est. ',
           'chosen conservatively', 'conservative reading')
DERIVED = re.compile(r'\d\s*(?:to\s*\d+\s*)?%\s*of\b|% of (?:his|her|their|the)\b')


def classify(r):
    """Why nothing was set on this line. One reason per line, first that applies."""
    ent = r['entity']
    if any(ent.startswith(n.split(' ·')[0].split(' —')[0]) for n in C040):
        return 'C-040', ('the Stage-to-Grade chain that sets this band is contested on '
                         'this card by name')
    low = r['verbatim'].lower()
    if any(t in low for t in NOTCARD):
        return 'NOT-A-CARD-FIGURE', ('the line states the figure is an estimate or is not '
                                     'on the card, so R44-1 does not name it')
    if DERIVED.search(r['verbatim']):
        return 'DERIVED', ('the figure is a stated fraction of another figure on the page '
                           'and cannot move alone')
    return 'NO-TARGET', 'R44-1 names the figure as the error and states no corrected value'


def fmt(x):
    if x is None:
        return '—'
    if x == int(x) and abs(x) < 1e6:
        return '{:,}'.format(int(x))
    return '%.3g' % x


def main():
    banded = [r for r in ROWS if r.get('band_j_low')]
    inband = [r for r in banded if r['decades_delivered'] == 0]
    out = [r for r in banded if r['decades_delivered'] != 0]
    skipped = [r for r in ROWS if r.get('skipped')]
    out.sort(key=lambda r: (r['source']['file'], r['source']['line'], r['eu'] or 0))

    reasons = collections.Counter()
    logged = []
    for r in out:
        code, why = classify(r)
        reasons[code] += 1
        logged.append((r, code, why))

    widths = [math.log10(r['band_j_high'] / r['band_j_low']) for r in out]
    widths.sort()

    L = []
    w = L.append
    w('# WAR-46 — the R44-1 EU-band sweep: every attested EU figure at 1 EU = 1 MJ')
    w('')
    w('Ruling: `RULINGS.md`, 2026-09-25, C-034; '
      '`rules/doc-essence-ledger-rulings-2026-09-25.yaml` R44-1.')
    w('Input: `imports/essence-ledger/fit.json` (`reserves`, `costs`, `grade_proxy_check`), '
      'built for WAR-9 and corrected for WAR-71.')
    w('Written by the Stat Keeper, 2026-09-25; regenerated the same day against the '
      'corrected fit. **No card figure was changed by this sweep.**')
    w('')
    w('Two defects this sweep found in the fit it reads have since been fixed in the '
      'extractor (WAR-71), and this file is the run after that fix. A figure on a table '
      'row that states its own gate Stage is now read against that Stage rather than '
      'against the page\'s entry Stage, and the Tier 5 η is R44-4\'s 0.60–0.70 rather '
      'than the mirror\'s pre-ruling 0.50–0.60. The counts below moved accordingly and '
      'the `GATE` reason is gone with the defect that produced it; §"What moved when the '
      'fit was corrected" records what changed.')
    w('')
    w('## What the ruling asks for, and what it supplies')
    w('')
    w('> One constant: 1 EU = 1 MJ stands. The Ledger converts at 1 MJ everywhere, and the '
      "card figures that then sit outside their Stage's band are the error; each is a card "
      'correction in its own issue, not in this ruling batch.')
    w('')
    w('R44-1 settles the constant and names a class of figures as wrong. It does not say '
      'what any corrected figure becomes, and no card states a replacement. Under house '
      'rule 3.3 a number that is not on a card, in a Magic System table or from `fow_line` '
      'is not available to write, so this sweep reads every figure, reports every miss, and '
      'sets none of them. Every line below is logged with the reason nothing was set.')
    w('')
    w('## One thing to know before the counts: the draft Part works at a different constant')
    w('')
    w('`imports/essence-ledger/the-essence-ledger.md` — the draft FoW Part Twenty-Three, '
      'WAR-12, on master — works at **1 EU = 1 kJ**, three decades below the constant this '
      'sweep reads at, and says so at §2.3: "**[draft] 1 EU = 1 kJ of potential. Energy '
      'delivered = EU × η × 1 kJ. 1 AU/s = 1 kW.**" It is not a rival ruling and this file '
      'does not treat it as one. The Part says of itself, at the C-034 PENDING note: "Every '
      'table below is built at 1 kJ and inherits whichever way Isaac rules." R44-1 is that '
      'ruling and it went the other way, so the draft owes itself a rebuild at 1 MJ. That '
      'is WAR-12\'s work and is filed separately; nothing in this sweep depends on it, '
      'because this sweep reads at the ruled constant and changes nothing either way.')
    w('')
    w('## The reading')
    w('')
    w('Each attested EU figure is converted at 1 EU = 1 MJ, taken through the η that its '
      'page states (or the Part Nineteen tier midpoint for its Stage\'s Tier of Standing '
      'where the page states none), and read against the attack-output band that its '
      'Stage\'s Max Grade claims in Part Four. The chain is Part Five\'s Stage gate table → '
      'the Stage\'s Max Grade → Part Four\'s joule column.')
    w('')
    w('"Its Stage" is the Stage the figure\'s own line states where the table it sits in '
      'gates its rows one by one, and the Stage the page states otherwise — `stage_basis` '
      'on every row of `fit.json` says which was read. Where the η comes off Part '
      'Nineteen\'s Tier 5 row it is the ruled 0.60–0.70, midpoint 0.65: R44-4 corrects that '
      'cell and the mirror has not re-exported it yet, so `anchors.json` keeps the mirror\'s '
      'row in `verbatim` and reads the ruling\'s figures.')
    w('')
    w('> Part Seventeen governs: η reads 0.60 to 0.70 at Stage VI–VII. Part Nineteen\'s '
      'Tier 5 row is corrected to match.')
    w('')
    w('Part Five, `wiki/Fracture of Worlds — The Living System/II. Grades, Gates and '
      'Thresholds (Parts Four–Ten).md:67`:')
    w('')
    w('> | IV | Flourishing | B | 275 | 4 · Adept |')
    w('')
    w('Part Four, the same file `:33`:')
    w('')
    w('> | B | 176–275 | 1.046×10^9 – 4.6024×10^10 J | Mach 1.5–4 |')
    w('')
    w('Two things about that chain are recorded here and decided nowhere. Part Five says '
      'what the Max Grade column does, same file `:60`:')
    w('')
    w('> The Max Grade column binds allocation: a Sub-Stat may not be allocated past the '
      'top of the Stage\'s Max Grade bracket.')
    w('')
    w('It binds allocation of a Sub-Stat. Reading it as a ceiling on delivered joules is a '
      'proxy, and reading a stored EU reserve against an *attack-output* column is a second '
      'proxy on top of it. Both are how WAR-9 fitted the corpus and how this issue words the '
      'job; neither is a sentence any page writes. Nothing here rests on choosing otherwise, '
      'because no figure is changed.')
    w('')
    w('## What the sweep found')
    w('')
    w('| | count |')
    w('|---|---|')
    w('| attested EU figures with a band to read against | %d |' % len(banded))
    w('| inside their Stage\'s band at 1 EU = 1 MJ (delivered, through η) | %d |' % len(inband))
    w('| **outside it** | **%d** |' % len(out))
    w('| attested EU figures with no Grade available for the reading | %d |' % len(skipped))
    w('| distinct files the misses sit in | %d |' %
      len({r['source']['file'] for r in out}))
    w('| distinct entities | %d |' % len({r['entity'] for r in out}))
    w('| misses that read **below** their band | %d |' %
      sum(1 for r in out if r['decades_delivered'] < 0))
    w('| misses that read **above** their band | %d |' %
      sum(1 for r in out if r['decades_delivered'] > 0))
    w('')
    w('The WAR-11 card put the miss at 137 of 165; this sweep reads %d of %d, the '
      'difference being the figures that carry no band and the duplicate anchors '
      '`fit.json` keeps apart. The direction is one-sided: %d of the %d misses read '
      'below the band their Stage claims, most of them by two decades or more.'
      % (len(out), len(banded), sum(1 for r in out if r['decades_delivered'] < 0), len(out)))
    w('')
    w('## What moved when the fit was corrected')
    w('')
    w('The first run of this sweep, before WAR-71, read 25 of 155 in band and 130 out, six '
      'of the misses above their band, and logged the reasons `C-040` 48, `GATE` 4, '
      '`NOT-A-CARD-FIGURE` 11, `DERIVED` 2, `NO-TARGET` 65. Two corrections to the fit it '
      'reads moved those counts, and neither is a card correction:')
    w('')
    w('- **the Stage a gated row is read against.** `imports/essence-ledger/extract_anchors.py` '
      'now carries the Stage a table row states for itself wherever the table gates its rows '
      'one by one, and `fit.py` reads that Stage. %d figures in the corpus carry such a '
      'Stage. On `The Disciplines/'
      'Rusashin — The Dust That Remembers What It Touched.md` the four Forms the fit had been '
      'reading against Stage III, the discipline\'s entry, are read at the Stages its `Gate` '
      'column writes: Form II at IV, Form VII at VII–VIII, Form VIII at VIII–IX, Form IX at '
      'IX–X, each taken at the low end of its range, the Stage the row opens at. Form II at '
      '4,000 EU lands inside B-Grade and leaves the log; the other three flip from above '
      'their band to below it and are logged `NO-TARGET`. The `GATE` reason existed only to '
      'record this misreading and is gone with it.'
      % sum(1 for r in ROWS if r.get('stage_on_the_line')))
    w('- **the Tier 5 η.** R44-4 corrects Part Nineteen\'s Tier 5 row from 0.50–0.60 to '
      '0.60–0.70 and the page edit it names has not come back through the hourly sync, so '
      '`build_anchors.py` now reads the ruling\'s figures and keeps the mirror\'s row in '
      '`verbatim` (`anchors.json`, `system.eta_by_tier`, `corrected_by_ruling`). %d lines '
      'take their η there, one more than the fifteen the first run counted, because Rusashin '
      'Form VII moved onto Stage VII and so onto Tier 5 with the first correction. Every '
      'delivered figure on them rises 18%%. `Spellcraft/Vainglory.md:28` at 75,000 EU was '
      'the only row within that distance of a band edge and it is now inside the band, so it '
      'leaves the log too.' % sum(1 for r in ROWS if 'Tier 5' in (r.get('eta_from') or '')))
    w('')
    w('Nothing else moved: the same 155 figures carry a band, the same %d carry none, and '
      'the twelve cards `C-040` names are the same twelve. No card figure was changed by '
      'either correction, and neither touches the constant.' % len(skipped))
    w('')
    w('## Why no figure was set')
    w('')
    w('Four reasons, in the order they were applied. Each line in the log carries exactly '
      'one.')
    w('')
    w('| reason | lines | what it means |')
    w('|---|---|---|')
    w('| `C-040` | %d | The figure sits on one of the twelve cards `CONFLICTS.md` C-040 '
      'names, where the Stage-to-Grade chain is measured out by one to seven Grades. The '
      'band itself is contested on that card, so the correction depends on C-040 and this '
      'issue stops rather than deciding it. |' % reasons['C-040'])
    w('| `NOT-A-CARD-FIGURE` | %d | The line says in words that the figure is an estimate, '
      'an extrapolation or not stated on the card. R44-1 names *card figures*; extending it '
      'to these would extend a ruling to a case it does not name (house rule 3.2). |'
      % reasons['NOT-A-CARD-FIGURE'])
    w('| `DERIVED` | %d | The figure is written as a stated fraction of another figure on '
      'the same page — a percentage of a reserve — so it cannot be corrected without first '
      'correcting the reserve it is taken from. |' % reasons['DERIVED'])
    w('| `NO-TARGET` | %d | A plain stated figure, outside its band, and the ruling gives no '
      'value to put in its place. |' % reasons['NO-TARGET'])
    w('')
    w('`NO-TARGET` is the reason that would survive every other one being answered, and it '
      'is the reason the sweep cannot run at all. "Inside the band" is a range, not a '
      'number. Across the %d misses the in-band window is %.2f decades wide at its '
      'narrowest, %.2f at the median and %.2f at its widest — at Stage XII the SSS band '
      'runs 4.184×10^14 to 4.184×10^21 J, so a "corrected" figure would be a free choice '
      'across seven orders of magnitude. Nothing on any of these cards names a point inside '
      'that window, so every replacement value would be invented.'
      % (len(out), widths[0], widths[len(widths) // 2], widths[-1]))
    w('')
    w('The one place canon prices a working both ways does not supply a target either. '
      'Dougou Ozumu Zettari\'s sheet and `Spellcraft/The Iron Tree.md` state an EU cost and '
      'a joule output on the same line three times (`fit.json`, `direct_pairs`), so the EU '
      'figure could in principle be re-derived from the stated joules; but those stated '
      'joules are themselves seven Grades below his Stage XIII band, which is C-040\'s '
      'largest row. Correcting the EU to agree with them would land the figure further '
      'outside the band the ruling reads it against, not inside it.')
    w('')
    w('## The log — %d lines, nothing set' % len(out))
    w('')
    w('`dec` is decades (log₁₀) outside the band, delivered through η; negative reads below '
      'the band, positive above. `band` is the Stage\'s Max Grade. A Stage marked *(own '
      'gate)* was read off the line\'s own gate cell rather than off the page.')
    w('')
    w('| entity | file:line | Stage | band | EU | η | J at 1 MJ, delivered | dec | reason |')
    w('|---|---|---|---|---|---|---|---|---|')
    for r, code, why in logged:
        stage = ('%s *(own gate)*' % r['stage'] if r.get('stage_on_the_line')
                 else str(r['stage']))
        w('| %s | `%s:%d` | %s | %s | %s | %.2f | %s | %+.2f | `%s` |' % (
            r['entity'].replace('|', '\\|'),
            r['source']['file'], r['source']['line'],
            stage, r['grade'], fmt(r['eu']), r['eta'],
            '%.3g' % r['delivered_j_at_1MJ'], r['decades_delivered'], code))
    w('')
    w('### The %d figures with no Grade available, read against nothing' % len(skipped))
    w('')
    w('| entity | file:line | EU | why |')
    w('|---|---|---|---|')
    for r in skipped:
        w('| %s | `%s:%d` | %s | %s |' % (r['entity'].replace('|', '\\|'),
                                          r['source']['file'], r['source']['line'],
                                          fmt(r['eu']), r['skipped']))
    w('')
    w('## Two things found on the way, neither of them a card correction')
    w('')
    w('**One. The sweep\'s worst residual is a figure the card says is final.** '
      '`Volume I — Character Cards/Aurelian Prudentius Custos Clausorum · The Primate.md:85` '
      'reads 2,400,000,000 EU at Stage XIV, 13.69 decades below the EX band, the largest '
      'miss in the corpus. The line states its own provenance: "Fracture of Worlds specifies '
      'no EU table by Stage; this figure was extrapolated from the two attested Band V '
      'reserves in project canon, Verinus VII at 620,000,000 and Kwon Mu-jin at 850,000,000, '
      'both at Stage XII, and stands as final." It is logged `NO-TARGET`, not '
      '`NOT-A-CARD-FIGURE`: the card says the figure stands. What it also says is that the '
      'two reserves it was built from are Stage XII figures and his Stage is XIV, and '
      '`fit.json` reads Stage XIV\'s Max Grade as EX off Part Five while Part Eleven\'s '
      'benchmark table declines to give Zenith a figure at all (`fit.json`, '
      '`meta.stage_xiv_reading`). Three readings meet on this one line and R44-1 names none '
      'of them.')
    w('')
    above = [r for r in out if r['decades_delivered'] > 0]
    fams = collections.Counter(r['family'] for r in above)
    w('**Two. Once each figure is read against its own Stage, almost every miss reads '
      '%s its band.** %d of the %d misses read above their band and the other %d below, and '
      'the ones above are %s — %s. Read that way a stored pool can sit above what its Stage '
      'may throw while every attested spend for a working comes in under it, which is a '
      'shape and not a correction. Nothing here says which side of the proxy is wrong, and '
      'the misses that remain above their band are logged like the rest.'
      % ('below' if len(above) * 2 < len(out) else 'above',
         len(above), len(out), len(out) - len(above),
         ' and '.join('%d %s%s' % (n, f, '' if n == 1 else 's')
                      for f, n in sorted(fams.items())),
         ', '.join('%s at %+.2f, `%s:%d`'
                   % (r['entity'], r['decades_delivered'],
                      r['source']['file'], r['source']['line'])
                   for r in sorted(above, key=lambda r: -r['decades_delivered']))))
    w('')
    w('## What would let this sweep run')
    w('')
    w('One further ruling on top of R44-1: what a corrected figure becomes. Under the '
      '2026-09-25 direction in `CLAUDE.md` — "a recorded conflict does not sit waiting for '
      'Isaac: it is ruled, openly, by the Paperclip docket" — that is the docket\'s to make '
      'and not the Stat Keeper\'s, so it is filed to Doc Kett rather than answered here. '
      'Three shapes would each be enough, and this file proposes none of them as the '
      'answer:')
    w('')
    w('- a rule that puts the figure at a named edge of its band (the floor, the midpoint), '
      'which makes every correction arithmetic off Part Four;')
    w('- a rule that the figure is correct and the Stage on the card is what moves, which is '
      'C-040\'s other direction and belongs with C-040;')
    w('- a rule that an EU reserve is not read against an attack-output band at all, which '
      'would take %d of the %d out of scope and leave the costs.'
      % (sum(1 for r in out if r['family'] == 'reserve'), len(out)))
    w('')
    w('Until one of them exists, R44-1 is applied as far as it reaches: the constant is '
      'settled, the misses are counted, and every card stands exactly as written.')
    w('')

    open('reports/eu_band_sweep_2026-09-25.md', 'w').write('\n'.join(L))
    print('reasons:', dict(reasons), 'total', sum(reasons.values()))
    print('wrote reports/eu_band_sweep_2026-09-25.md')


main()
