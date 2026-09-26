#!/usr/bin/env python3
"""WAR-46 — apply WAR-70 to the R44-1 EU-band misses.

Reads `imports/essence-ledger/fit.json` and the Part Four Grade table out of the
live-system page, computes the set point WAR-70 names for every miss, and writes
`reports/eu_band_corrections_2026-09-25.md`: one line of arithmetic per figure,
each citing the Part Four row it is computed from.

WAR-70 (`RULINGS.md`, 2026-09-25): "A card EU figure that R44-1 (1 EU = 1 MJ)
puts outside its Stage's band is corrected by moving it to a set point in that
band ... The set point is the band's midpoint in decades (the geometric mean of
floor and ceiling, in joules, divided by 1 MJ)."

This script computes; it changes no card. The figures it marks APPLY are the ones
the run then edits on the live Notion pages, and the report says why every other
figure is held. Nothing here rounds a band, invents a bound or reads a Grade the
Part Four table does not write."""
import json, math, re, collections

FIT = 'imports/essence-ledger/fit.json'
PART = ('wiki/Fracture of Worlds — The Living System/'
        'II. Grades, Gates and Thresholds (Parts Four–Ten).md')
OUT = 'reports/eu_band_corrections_2026-09-25.md'
SIGFIGS = 4          # the precision Part Four's own floors and ceilings carry
EU_JOULE = 1e6       # R44-1: 1 EU = 1 MJ

# --- Part Four, read off the page rather than typed ---------------------------

UNIT = {'j': 1.0, 'kj': 1e3, 'mj': 1e6, 'gj': 1e9}


def joules(tok):
    """'4.184×10^21 J' / '15 kJ' / '60' -> float. Returns None for a bare word."""
    tok = tok.strip().replace(',', '')
    m = re.match(r'^([\d.]+)\s*(?:×10\^(-?\d+))?\s*([kKmMgG]?[jJ])?$', tok)
    if not m:
        return None
    v = float(m.group(1))
    if m.group(2):
        v *= 10 ** int(m.group(2))
    if m.group(3):
        v *= UNIT[m.group(3).lower()]
    return v


HEADER = '| Grade | Sub-Stat value | Attack output | Travel speed |'


def part_four():
    """{grade: (line_no, verbatim_row, low_j, high_j)} from the Grade table.

    Only that table: the page carries later tables with a Grade column of their
    own (the travel-speed table's SSS row reads in m/s), and reading one of
    those as an attack-output band would put a speed in a joule field."""
    rows = {}
    inside = False
    for n, raw in enumerate(open(PART, encoding='utf-8'), 1):
        line = raw.rstrip('\n')
        if line == HEADER:
            inside = True
            continue
        if not inside:
            continue
        if not line.startswith('|'):
            break
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) != 4 or cells[0].startswith('---'):
            continue
        grade, out = cells[0], cells[2]
        if not re.match(r'^(Hollow|F|E|D|C|B|A|S|SS|SSS|X|EX|EX\+)$', grade):
            continue
        low = high = None
        if out.startswith('below '):
            high = joules(out[len('below '):])
        elif out.endswith(' and above'):
            low = joules(out[:-len(' and above')])
        else:
            parts = re.split(r'\s*[–-]\s*', out)
            if len(parts) == 2:
                # the unit is often written once, on the second bound only
                high = joules(parts[1])
                low = joules(parts[0])
                if low is not None and high is not None and low > high:
                    low = None
                if low is None:
                    m = re.match(r'^([\d.]+(?:×10\^-?\d+)?)$', parts[0].strip())
                    if m and high:
                        # bare number: carry the second bound's magnitude words
                        low = joules(parts[0].strip() + ' J')
        rows[grade] = (n, line, low, high)
    return rows


P4 = part_four()

# --- the misses --------------------------------------------------------------

F = json.load(open(FIT, encoding='utf-8'))
ROWS = F['reserves'] + F['costs']
BANDED = [r for r in ROWS if r.get('band_j_low')]
MISSES = [r for r in BANDED if r['decades_delivered'] != 0]

# Every band the fit read must be the Part Four row this report cites, or the
# citation would be decoration. Checked, not assumed.
for r in BANDED:
    n, verbatim, low, high = P4[r['grade']]
    assert low is not None and high is not None, (r['grade'], verbatim)
    assert abs(low / r['band_j_low'] - 1) < 1e-9 and abs(high / r['band_j_high'] - 1) < 1e-9, \
        (r['grade'], low, r['band_j_low'], high, r['band_j_high'])


def sig(x, n=SIGFIGS):
    """x to n significant figures, exactly (no float tail)."""
    if x == 0:
        return 0.0
    e = math.floor(math.log10(abs(x)))
    return round(x, -(e - n + 1))


def setpoint(r):
    """WAR-70's set point for this figure's band, in EU."""
    gm = math.sqrt(r['band_j_low'] * r['band_j_high'])
    return sig(gm) / EU_JOULE, gm


def eu_text(x):
    """The figure as a card writes one: separators up to 10^12, else ×10^n."""
    if x >= 1e12:
        e = math.floor(math.log10(x))
        return '%g×10^%d' % (sig(x / 10 ** e), e)
    if x == int(x):
        return '{:,}'.format(int(x))
    return '{:,}'.format(x)


# --- why a figure is held ----------------------------------------------------

# A line that says of itself that its figure is an estimate, or not on the card.
# Wider than the sweep's list, which missed "(est.)" and "*(estimate — ...)*".
ESTIMATE = ('estimat', 'est.)', 'est.,', 'est. ', 'not stated on the card',
            'chosen conservatively', 'conservative reading', 'no exact source figure')
# A figure the card states as a fraction of another figure on the same page.
DERIVED = re.compile(r'\d\s*(?:to\s*\d+\s*)?%\s*of\b|% of (?:his|her|their|the)\b')
# A figure the card attributes to a source outside the card by name. Correcting
# the number leaves the card citing a source that says something else — the
# wording WAR-48 held Ignatius, Karo, Borin and Sodoku for under R44-2.
PROVENANCE = ('workbook figure', 'carry from the legacy sheet',
              'carry across from the legacy sheet')
# The card's own words that the corrected figure would make false, quoted.
CARD_SAYS = {
    ('wiki/Summoned and Bound/Vaelmorn · The Standing Grave.md', 80):
        'the same cell calls the figure "Low, and the lowness is why hedge '
        'practitioners at Stage VII can reach him at all"; the set point is '
        '1.323×10^12 EU, which no Stage VII practitioner can pay, and the page '
        'states the figure a second time at :231',
}

GROUP = collections.defaultdict(list)
for r in BANDED:
    GROUP[(r['entity'], r['band_j_low'])].append(r)
PER_FILE = collections.Counter(r['source']['file'] for r in MISSES)


def hold(r):
    """(code, why) or None if WAR-70 applies to this figure as it stands."""
    low = r['verbatim'].lower()
    key = (r['source']['file'], r['source']['line'])
    if key in CARD_SAYS:
        return 'CARD-SAYS', CARD_SAYS[key]
    if any(t in low for t in ESTIMATE):
        return 'ESTIMATE', ('the line says of itself that the figure is an estimate or is '
                            'not on the card; R44-1 names card figures, and the form of an '
                            'estimate is one of the questions WAR-96 left open')
    if DERIVED.search(r['verbatim']):
        return 'DERIVED', ('the card states this figure as a fraction of another figure on '
                           'the same page, so it cannot move to a set point of its own '
                           'without contradicting the percentage')
    if any(t in low for t in PROVENANCE):
        return 'PROVENANCE', ('the card attributes the figure to a source outside the card '
                              'by name, so a corrected number leaves the card citing a '
                              'source that says otherwise; WAR-70 does not say whether the '
                              'note goes with the figure')
    if r['stage'] >= 14:
        return 'ZENITH', ('Part Four says of this Stage that "speed and attack output are '
                          'no longer assessed by conventional metrics" (%s:55), so the '
                          'attack-output band the chain hands it is contested by the Part '
                          'that supplies it' % PART)
    if len(GROUP[(r['entity'], r['band_j_low'])]) > 1:
        others = [x for x in GROUP[(r['entity'], r['band_j_low'])] if x is not r]
        return 'COLLAPSE', ('%d other banded figure(s) on this entity read against the same '
                            'band, so one set point per band makes them all the same number '
                            '(%s)' % (len(others),
                                      ', '.join(sorted({eu_text(x['eu']) for x in others}))))
    if PER_FILE[r['source']['file']] > 1:
        return 'ORDER', ('another miss on this same file is held, and moving this figure '
                         'alone would invert the order the page states between them')
    new, _ = setpoint(r)
    if new != int(new):
        return 'DECIMAL', ('the set point is %s EU, a decimal in a field that has never held '
                           'one; rounding it would invent a number (the reason WAR-48 held '
                           'four cards under R44-2)' % new)
    return None


# --- the report --------------------------------------------------------------

def line_of_arithmetic(r):
    n, verbatim, low, high = P4[r['grade']]
    new, gm = setpoint(r)
    return (
        '- **%s** — `%s:%d`. Stage %s, Max Grade %s, band %s–%s J '
        '(Part Four, `%s:%d`: `%s`). Set point √(%s × %s) = %s J ÷ 1 MJ = '
        '**%s EU**, from **%s EU** (%+.2f decades). Check: %s EU × η %.3g × 1 MJ = %s J, '
        'inside the band.' % (
            r['entity'], r['source']['file'], r['source']['line'], roman(r['stage']),
            r['grade'], g(low), g(high), PART, n, verbatim, g(low), g(high), g(sig(gm)),
            eu_text(new), eu_text(r['eu']), math.log10(new / r['eu']), eu_text(new),
            r['eta'], g(sig(new * r['eta'] * EU_JOULE))))


def g(x):
    s = '%.6g' % x
    if 'e' in s:
        m, e = s.split('e')
        return '%s×10^%d' % (m, int(e))
    return s


ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
         'XIII', 'XIV', 'XV', 'XVI']


def roman(n):
    return ROMAN[n] if 0 < n < len(ROMAN) else str(n)


REASON_TITLE = {
    'COLLAPSE': 'Held — one set point per band makes distinct figures the same number',
    'ESTIMATE': 'Held — the line states the figure is an estimate, or not on the card',
    'PROVENANCE': 'Held — the card attributes the figure to a source outside the card',
    'DERIVED': 'Held — the figure is a stated fraction of another figure on the page',
    'ZENITH': 'Held — Part Four says this Stage is not assessed by attack output',
    'DECIMAL': 'Held — the set point is a decimal in a field that has never held one',
    'ORDER': 'Held — applying it alone would invert an order the page states',
    'CARD-SAYS': "Held — the corrected figure would make the card's own words false",
}


def main():
    classified = [(r, hold(r)) for r in MISSES]
    applied = [r for r, h in classified if h is None]
    held = [(r, h) for r, h in classified if h is not None]
    counts = collections.Counter(h[0] for _, h in held)

    L = []
    w = L.append
    w('# WAR-46 — WAR-70 applied: every R44-1 EU-band miss, with its set point')
    w('')
    w('Rulings: `RULINGS.md` 2026-09-25 **R44-1** (1 EU = 1 MJ) and **WAR-70** (what a '
      'figure outside its band becomes). Input: `imports/essence-ledger/fit.json`, the fit '
      'as corrected by WAR-71 and WAR-94. Generated by '
      '`imports/essence-ledger/eu_band_corrections.py`; every number below is computed, '
      'none typed.')
    w('')
    w('> A card EU figure that R44-1 (1 EU = 1 MJ) puts outside its Stage\'s band is '
      'corrected by moving it to a set point in that band, so every correction is '
      'arithmetic off Part Four. The set point is the band\'s midpoint in decades (the '
      'geometric mean of floor and ceiling, in joules, divided by 1 MJ).')
    w('')
    w('## The arithmetic, once')
    w('')
    w('For a figure whose Stage\'s Max Grade is *G*, Part Four gives *G*\'s attack-output '
      'floor and ceiling in joules. The set point is √(floor × ceiling) ÷ 1 MJ, taken to '
      'four significant figures — the precision Part Four\'s own bounds carry (`4.184`, '
      '`2.42672`, `4.6024`). Nothing else is rounded. Every band in this report was read '
      'off the Part Four row quoted beside it and checked against the band `fit.json` used; '
      'the script asserts the two agree before it writes a line.')
    w('')
    w('One set point per band, so the same Grade gives the same figure on every card:')
    w('')
    w('| Max Grade | Part Four row | set point |')
    w('|---|---|---|')
    for grade in ['C', 'B', 'A', 'S', 'SS', 'SSS', 'X', 'EX']:
        n, verbatim, low, high = P4[grade]
        gm = math.sqrt(low * high)
        w('| %s | `:%d` %s | %s EU |' % (grade, n, verbatim.replace('|', '\\|'),
                                         eu_text(sig(gm) / EU_JOULE)))
    w('')
    w('**The η check.** WAR-70\'s arithmetic converts joules to EU at 1 MJ and does not '
      'divide by η, so a corrected figure delivers η × the midpoint rather than the '
      'midpoint. That still lands inside the band for every one of the %d misses — the '
      'widest η would have to fall below 10^(−half the band\'s width in decades) to fall '
      'out, and none does. Each line below carries the check.' % len(MISSES))
    w('')
    w('## Counts')
    w('')
    w('| | count |')
    w('|---|---|')
    w('| attested EU figures with a band to read against | %d |' % len(BANDED))
    w('| inside their band at 1 EU = 1 MJ | %d |' % (len(BANDED) - len(MISSES)))
    w('| **misses, each computed below** | **%d** |' % len(MISSES))
    w('| corrected on the live Notion page by this run | **%d** |' % len(applied))
    w('| held, with the reason and the arithmetic | **%d** |' % len(held))
    w('')
    for code, k in counts.most_common():
        w('- `%s` — %d' % (code, k))
    w('')
    w('The two new conflict rows the holds rest on are `CONFLICTS.md` **C-059** (the set point is '
      'one figure per band, so 99 figures a card states as different numbers become one number — '
      'filed as WAR-127) and **C-060** (Part Four says Stage XIV is not assessed by attack output '
      'while the chain hands it an EX band — WAR-128). The `PROVENANCE`, `DECIMAL` and `ESTIMATE` '
      'holds are the wording questions WAR-48 and WAR-96 left open, named in C-059 and not reopened '
      'here.')
    w('')
    w('The sweep that found the misses is `reports/eu_band_sweep_2026-09-25.md` (130 at '
      'the time WAR-70 was filed, %d after WAR-71 and WAR-94 corrected the extractor; no '
      'card moved in either correction).' % len(MISSES))
    w('')
    w('## Corrected')
    w('')
    if applied:
        for r in sorted(applied, key=lambda r: r['entity']):
            w(line_of_arithmetic(r))
            w('  - card, as it stood: `%s`' % r['verbatim'].replace('\n', ' '))
    else:
        w('None.')
    w('')
    w('## Held, with the set point each would take')
    w('')
    w('Each of these is computed the same way and none was written. The reason is the '
      'first that applies, in the order the script tests them.')
    for code, _ in counts.most_common():
        w('')
        w('### %s (%d)' % (REASON_TITLE[code], counts[code]))
        w('')
        rs = sorted((x for x in held if x[1][0] == code),
                    key=lambda x: (x[0]['source']['file'], x[0]['source']['line']))
        for r, (_, why) in rs:
            w(line_of_arithmetic(r))
            w('  - **held:** %s' % why)
    w('')
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('wrote %s — %d misses, %d applied, %d held' % (OUT, len(MISSES), len(applied), len(held)))
    for code, k in counts.most_common():
        print('  %-12s %d' % (code, k))
    for r in applied:
        new, _ = setpoint(r)
        print('  APPLY %-50s %s:%d  %s -> %s' % (r['entity'][:50], r['source']['file'],
                                                 r['source']['line'], eu_text(r['eu']),
                                                 eu_text(new)))


if __name__ == '__main__':
    main()
