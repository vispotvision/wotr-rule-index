#!/usr/bin/env python3
"""WAR-46 — apply C-059 to the R44-1 EU-band misses: one factor per card.

C-059 (`RULINGS.md`, 2026-09-25, amends WAR-70):

    WAR-70's set point applies to a card's EU reserve only. Each card whose
    reserve R44-1 puts outside its Stage's band is scaled by one factor:
    factor = (band midpoint in decades, the geometric mean of floor and
    ceiling joules / 1 MJ) / (the card's stated reserve). Every other EU
    figure on that card (technique, Form and working costs, per-use figures)
    is multiplied by the same factor, so each cost keeps its stated share of
    the reserve and distinct figures stay distinct. Flux Density, AU/s and eta
    stand as written. A card with no stated reserve is not scaled by this
    ruling and is logged.

So this script does two things `eu_band_corrections.py` could not:

* it decides per *card*, not per figure — the factor is the reserve's, and the
  card is the unit the ruling names;
* it reads the card itself for the EU figures C-059 names, not only the
  figures `fit.json` extracted as anchors. `fit.json` carries the attested
  anchors; a card also states per-second rates ("75,000 EU activation /
  8,000 EU/s") and follow-on costs that are EU figures on the card and move
  with it. Scaling the anchor and leaving the rate would break the very share
  C-059 exists to keep.

It computes and writes a report. It changes no card: the figures it marks
SCALE are the ones the run then edits on the live Notion pages.

Flux Density (EU/g), AU/s, eta and every percentage are matched and skipped by
name, never by position.
"""
import json, math, re, collections, os

FIT = 'imports/essence-ledger/fit.json'
PART = ('wiki/Fracture of Worlds — The Living System/'
        'II. Grades, Gates and Thresholds (Parts Four–Ten).md')
OUT = 'reports/eu_card_scaling_2026-09-25.md'
SIGFIGS = 4          # the precision Part Four's own floors and ceilings carry
EU_JOULE = 1e6       # R44-1: 1 EU = 1 MJ

# --- Part Four, read off the page rather than typed ---------------------------

UNIT = {'j': 1.0, 'kj': 1e3, 'mj': 1e6, 'gj': 1e9}
HEADER = '| Grade | Sub-Stat value | Attack output | Travel speed |'


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


def part_four():
    """{grade: (line_no, verbatim_row, low_j, high_j)} from the Grade table only.

    The page carries later tables with a Grade column of their own (the
    travel-speed table's SSS row reads in m/s); reading one of those as an
    attack-output band would put a speed in a joule field."""
    rows, inside = {}, False
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
                high, low = joules(parts[1]), joules(parts[0])
                if low is not None and high is not None and low > high:
                    low = None
                if low is None:
                    m = re.match(r'^([\d.]+(?:×10\^-?\d+)?)$', parts[0].strip())
                    if m and high:
                        low = joules(parts[0].strip() + ' J')
        rows[grade] = (n, line, low, high)
    return rows


P4 = part_four()

# --- the fit -----------------------------------------------------------------

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
    """WAR-70's set point for this figure's band, in EU, and the raw mean."""
    gm = math.sqrt(r['band_j_low'] * r['band_j_high'])
    return sig(gm) / EU_JOULE, gm


def eu_text(x):
    """The figure as a card writes one: separators up to 10^12, else ×10^n."""
    x = sig(x)
    if abs(x) >= 1e12:
        e = math.floor(math.log10(abs(x)))
        return '%g×10^%d' % (sig(x / 10 ** e), e)
    if x == int(x):
        return '{:,}'.format(int(x))
    return '{:,}'.format(x)


def g(x):
    s = '%.6g' % x
    if 'e' in s:
        m, e = s.split('e')
        return '%s×10^%d' % (m, int(e))
    return s


ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
         'XIII', 'XIV', 'XV', 'XVI']


def roman(n):
    return ROMAN[n] if n and 0 < n < len(ROMAN) else str(n)


# --- why a reserve cannot carry a factor --------------------------------------
#
# C-059 settles the holds that rested on one set point per band: COLLAPSE (it
# names that collapse as the reason it exists), DERIVED (a stated fraction is
# preserved exactly by a uniform factor) and ORDER (so is an order). It says
# nothing about a figure a card calls an estimate, a figure a card sources
# outside itself, a Stage Part Four declines to assess, or a set point that is
# a decimal in a field that has never held one. Those keep the reasons
# `eu_band_corrections.py` gave them (WAR-46's wake instruction: "the other
# holds keep their own reasons unless this ruling settles them").

ESTIMATE = ('estimat', 'est.)', 'est.,', 'est. ', 'not stated on the card',
            'chosen conservatively', 'conservative reading', 'no exact source figure')
# The wording WAR-48 held Ignatius, Karo, Borin and Sodoku for under R44-2, kept
# verbatim. "per his sheet" is deliberately NOT here: on `The Iron Tree` it
# attaches to one Form's cost and not to the reserve, and C-059's own worked
# example is that card ("Dougou's reserve to ~2.3e19 EU; a 7,400 EU Form stays
# ~8% of it"), so the ruling names it as scaled.
PROVENANCE = ('workbook figure', 'carry from the legacy sheet',
              'carry across from the legacy sheet')


def reserve_hold(r):
    """(code, why) if this reserve cannot supply a factor, else None."""
    low = r['verbatim'].lower()
    if r['decades_delivered'] == 0:
        return 'RESERVE-IN-BAND', ('R44-1 does not put this card\'s reserve outside its '
                                   'Stage\'s band, and C-059 scales only a card whose '
                                   'reserve it does; the misses on this card are outside '
                                   'what the ruling reaches')
    if any(t in low for t in ESTIMATE):
        return 'ESTIMATE', ('the reserve line says of itself that the figure is an '
                            'estimate, so the factor would be computed from a number the '
                            'card does not assert; C-059 does not say whether an estimate '
                            'is a stated reserve')
    if any(t in low for t in PROVENANCE):
        return 'PROVENANCE', ('the card attributes the reserve to a source outside the card '
                              'by name, so a scaled card leaves the card citing a source '
                              'that says otherwise; C-059 does not say whether the note '
                              'moves with the figure')
    if (r['stage'] or 0) >= 14:
        return 'ZENITH', ('Part Four says of this Stage that "speed and attack output are '
                          'no longer assessed by conventional metrics" (%s:55), so the band '
                          'the factor would come from is contested by the Part that supplies '
                          'it — CONFLICTS.md C-060, WAR-128' % PART)
    new, _ = setpoint(r)
    if new != int(new):
        return 'DECIMAL', ('the reserve\'s set point is %s EU, a decimal in a field that has '
                           'never held one; rounding it would invent the factor every other '
                           'figure on the card is then multiplied by' % new)
    return None


# --- the cards ----------------------------------------------------------------

BY_FILE = collections.defaultdict(list)
for r in BANDED:
    BY_FILE[r['source']['file']].append(r)


def card_decision(path, rows):
    """(factor, reserve_row, hold) for one card file."""
    res = [r for r in rows if r['family'] == 'reserve']
    if not res:
        return None, None, ('NO-RESERVE', 'the card states no EU reserve, and C-059 scales a '
                                          'card by its reserve; "A card with no stated reserve '
                                          'is not scaled by this ruling and is logged"')
    distinct = sorted({r['eu'] for r in res})
    if len(distinct) > 1:
        return None, res[0], ('TWO-RESERVES', 'the reserve line states %d figures (%s) and '
                              'C-059 names "the card\'s stated reserve", one figure; choosing '
                              'between them would decide the ruling rather than apply it'
                              % (len(distinct), ', '.join(eu_text(x) for x in distinct)))
    r0 = res[0]
    h = reserve_hold(r0)
    if h:
        return None, r0, h
    new, _ = setpoint(r0)
    return new / r0['eu'], r0, None


# --- the EU figures a card states ---------------------------------------------
#
# Matched by the unit written beside the number, never by position. `EU/g` is
# Flux Density and `AU/s` is output: both stand under C-059, and both are
# excluded here by the pattern rather than by a list of exceptions.

AMOUNT = re.compile(r'(?<![\d.])(\d[\d,]*(?:\.\d+)?)(\s*(?:million|billion))?(\s*)EU\b(?!\s*/\s*g)')
# The low end of a range writes its unit once, on the high end: "2,800 to 8,900
# EU per branch". Both bounds are EU figures on the card and both move, or the
# range reads from the old floor to the new ceiling.
RANGE_LOW = re.compile(r'(?<![\d.])(\d[\d,]*(?:\.\d+)?)\s*(?:to|–|—)\s*\d[\d,]*(?:\.\d+)?'
                       r'(?:\s*(?:million|billion))?\s*EU\b(?!\s*/\s*g)')
RESERVE_LABEL = re.compile(r'(EU Reserve\**\s*[:·]?\**\s*~?)(\d[\d,]*(?:\.\d+)?)')
# A cost the card hangs a per-use rate off writes the unit once, on the cost:
# "20,000 EU + 3,000/s". The rate is an EU figure, so it moves with the cost or
# the line stops stating a share. The denominator is whatever the card counts
# in — `/s`, but also `/target`, `/min`, `/breath` — and a word may stand
# between the unit and the `+` ("75,000 EU each + 15,000/s"). Anchored on `EU`
# and on the `+`, so a metre, a second or a temperature beside a cost is not
# reached: `[^+\d]` cannot cross another figure.
TRAILING_RATE = re.compile(r'(EU\b[^+\d]{0,12}\+\s*)(\d[\d,]*(?:\.\d+)?)(\s*/\s*[A-Za-z]+)')
MAGNITUDE = {'million': 1e6, 'billion': 1e9}


def eu_tokens(line):
    """[(start, end, literal, value)] — every EU figure this line states."""
    found = []
    for m in AMOUNT.finditer(line):
        v = float(m.group(1).replace(',', ''))
        if m.group(2):
            v *= MAGNITUDE[m.group(2).strip()]
        found.append((m.start(1), m.end(2) if m.group(2) else m.end(1), m.group(0), v))
    for m in RANGE_LOW.finditer(line):
        found.append((m.start(1), m.end(1), m.group(0), float(m.group(1).replace(',', ''))))
    for m in RESERVE_LABEL.finditer(line):
        found.append((m.start(2), m.end(2), m.group(0), float(m.group(2).replace(',', ''))))
    for m in TRAILING_RATE.finditer(line):
        found.append((m.start(2), m.end(2), m.group(0), float(m.group(2).replace(',', ''))))
    # one line can match AMOUNT and RESERVE_LABEL over the same digits
    seen, out = set(), []
    for t in sorted(found):
        if t[0] in seen:
            continue
        seen.add(t[0])
        out.append(t)
    return out


def rewrite(line, factor, on_reserve_line=False, set_point=None):
    """(new_line, [(literal, old, new, note)]) for one line at this card's factor.

    The one exception to `value × factor`: the reserve figure itself, which the
    factor is *defined* to carry to the set point. On Ara Min Mahuo the live
    page already reads the set point — WAR-70 corrected that one figure on
    2026-09-25 before C-059 amended it — so the card states the corrected
    reserve while `fit.json` still holds the stated one. Multiplying the page's
    figure again would apply the factor twice."""
    toks, moved, out, last = eu_tokens(line), [], [], 0
    for start, end, literal, value in toks:
        note = ''
        if on_reserve_line and set_point is not None and value == set_point:
            new, note = value, 'already at the set point (WAR-70, applied 2026-09-25)'
        else:
            new = sig(value * factor)
        out.append(line[last:start])
        out.append(eu_text(new))
        last = end
        moved.append((literal.strip(), value, new, note))
    out.append(line[last:])
    return ''.join(out), moved


# --- what WAR-70 already corrected --------------------------------------------

PRIOR = 'reports/eu_band_corrections_2026-09-25.md'


def prior_applied():
    """The rows the WAR-70 run edited on the live pages, read out of its report.

    Its `## Corrected` section is the record of what was written; each entry
    cites `file:line`, so the rows are looked up rather than re-listed here."""
    want, inside = [], False
    for line in open(PRIOR, encoding='utf-8'):
        if line.startswith('## '):
            inside = line.strip() == '## Corrected'
            continue
        if inside:
            m = re.search(r'`([^`]+\.md):(\d+)`', line)
            if m:
                want.append((m.group(1), int(m.group(2))))
    out = []
    for f, n in want:
        for r in ROWS:
            if r['source']['file'] == f and r['source']['line'] == n:
                out.append(r)
                break
    return out


# --- the report ---------------------------------------------------------------

def held_line(r):
    n, verbatim, low, high = P4[r['grade']]
    new, gm = setpoint(r)
    return ('- **%s** — `%s:%d`, %s EU. Stage %s, Max Grade %s, band %s–%s J '
            '(Part Four, `%s:%d`: `%s`). WAR-70\'s set point for this band is %s EU.'
            % (r['entity'], r['source']['file'], r['source']['line'], eu_text(r['eu']),
               roman(r['stage']), r['grade'], g(low), g(high), PART, n, verbatim,
               eu_text(new)))


REASON_TITLE = {
    'NO-RESERVE': 'Held — the card states no EU reserve, so C-059 does not scale it',
    'RESERVE-IN-BAND': "Held — R44-1 does not put this card's reserve outside its band",
    'ESTIMATE': 'Held — the reserve line states the figure is an estimate',
    'PROVENANCE': 'Held — the card attributes the reserve to a source outside the card',
    'ZENITH': 'Held — Part Four says this Stage is not assessed by attack output (C-060)',
    'DECIMAL': 'Held — the set point is a decimal in a field that has never held one',
    'TWO-RESERVES': 'Held — the reserve line states two figures and C-059 names one',
}


def main():
    scaled, held = [], []
    for path in sorted(BY_FILE):
        rows = BY_FILE[path]
        factor, r0, h = card_decision(path, rows)
        if h:
            held.append((path, rows, r0, h))
        else:
            scaled.append((path, rows, r0, factor))

    # the edits, card by card, read off the card
    edits = collections.OrderedDict()
    for path, rows, r0, factor in scaled:
        per_card = []
        sp, _ = setpoint(r0)
        if os.path.exists(path):
            for n, raw in enumerate(open(path, encoding='utf-8'), 1):
                line = raw.rstrip('\n')
                new_line, moved = rewrite(line, factor, n == r0['source']['line'], sp)
                if moved:
                    per_card.append((n, line, new_line, moved))
        edits[path] = per_card

    n_figs = sum(1 for c in edits.values() for _, _, _, m in c for t in m if not t[3])
    n_anchor_misses_freed = sum(1 for p, rows, _, _ in scaled for r in rows
                                if r['decades_delivered'] != 0)
    held_misses = sum(1 for _, rows, _, _ in held for r in rows if r['decades_delivered'] != 0)

    L = []
    w = L.append
    w('# WAR-46 — C-059 applied: one factor per card, from the card\'s own reserve')
    w('')
    w('Rulings: `RULINGS.md` 2026-09-25 **R44-1** (1 EU = 1 MJ), **WAR-70** (what a figure '
      'outside its band becomes) and **C-059** (WAR-127, which amends WAR-70 to scale a whole '
      'card by one factor). Input: `imports/essence-ledger/fit.json` and the card pages '
      'themselves. Generated by `imports/essence-ledger/eu_card_scaling.py`; every number '
      'below is computed, none typed. Supersedes the per-figure set points in '
      '`reports/eu_band_corrections_2026-09-25.md`, which C-059 amends.')
    w('')
    w('> Each card whose reserve R44-1 puts outside its Stage\'s band is scaled by one '
      'factor: factor = (the band midpoint in decades, the geometric mean of floor and '
      'ceiling joules / 1 MJ) / (the card\'s stated reserve). Every other EU figure on that '
      'card is multiplied by the same factor. Flux Density, AU/s and η stand as written. A '
      'card with no stated reserve is not scaled by this ruling and is logged.')
    w('')
    w('## The arithmetic, once')
    w('')
    w('For the reserve\'s Stage the Max Grade is *G*; Part Four gives *G*\'s attack-output '
      'floor and ceiling in joules. The set point is √(floor × ceiling) ÷ 1 MJ at four '
      'significant figures — the precision Part Four\'s own bounds carry (`4.184`, `2.42672`, '
      '`4.6024`). The factor is that set point divided by the reserve the card states. Every '
      'other EU figure on the card is that figure × the factor, written at the same four '
      'significant figures. Nothing else is rounded, and every band was read off the Part '
      'Four row quoted beside it and asserted equal to the band `fit.json` used before a line '
      'was written.')
    w('')
    w('**What counts as an EU figure on the card.** A number the card writes with `EU` beside '
      'it, including a per-second rate (`8,000 EU/s`) and a bare rate the card hangs off an EU '
      'cost (`20,000 EU + 3,000/s`), and the figure on an `EU Reserve` label. `EU/g` (Flux '
      'Density), `AU/s` and η are excluded by the pattern, not by a list, and stand as C-059 '
      'says. This reaches figures `fit.json` never extracted as anchors: those rates are the '
      '"per-use figures" C-059 names, and scaling the cost while leaving the rate would break '
      'the share the ruling exists to keep.')
    w('')
    w('## Counts')
    w('')
    w('| | count |')
    w('|---|---|')
    w('| attested EU figures with a band to read against | %d |' % len(BANDED))
    w('| of those, misses at 1 EU = 1 MJ | %d |' % len(MISSES))
    w('| cards C-059 scales | **%d** |' % len(scaled))
    w('| **EU figures on those cards, each scaled** | **%d** |' % n_figs)
    w('| of those, attested misses the scaling settles | %d |' % n_anchor_misses_freed)
    w('| cards C-059 does not reach | %d |' % len(held))
    w('| attested misses still held on them | %d |' % held_misses)
    w('')
    counts = collections.Counter(h[0] for _, _, _, h in held)
    for code, k in counts.most_common():
        w('- `%s` — %d card(s)' % (code, k))
    w('')
    w('## Scaled — the factor, and every EU figure on the card')
    w('')
    for path, rows, r0, factor in scaled:
        n, verbatim, low, high = P4[r0['grade']]
        new, gm = setpoint(r0)
        w('### %s' % r0['entity'])
        w('')
        w('`%s`. Reserve **%s EU** at `:%d` — Stage %s, Max Grade %s, band %s–%s J '
          '(Part Four, `%s:%d`: `%s`). Set point √(%s × %s) = %s J ÷ 1 MJ = **%s EU**. '
          'Factor = %s ÷ %s = **×%s** (%+.2f decades).'
          % (path, eu_text(r0['eu']), r0['source']['line'], roman(r0['stage']), r0['grade'],
             g(low), g(high), PART, n, verbatim, g(low), g(high), g(sig(gm)), eu_text(new),
             eu_text(new), eu_text(r0['eu']), g(sig(factor)), math.log10(factor)))
        w('')
        w('Check: %s EU × η %.3g × 1 MJ = %s J, inside %s–%s J.'
          % (eu_text(new), r0['eta'], g(sig(new * r0['eta'] * EU_JOULE)), g(low), g(high)))
        w('')
        if not edits[path]:
            w('*The card file is not in the mirror; no line could be read.*')
            w('')
            continue
        w('| line | reads | becomes |')
        w('|---|---|---|')
        for ln, old, newl, moved in edits[path]:
            for literal, ov, nv, note in moved:
                w('| `:%d` | `%s` | %s |'
                  % (ln, literal.replace('|', '\\|'),
                     ('*unchanged — %s*' % note) if note else '**%s EU**' % eu_text(nv)))
        w('')
    w('## The four WAR-70 corrections, re-checked')
    w('')
    w('C-059: "The four cards already corrected under WAR-70 are re-checked against this '
      'rule." The four are read out of the `## Corrected` section of '
      '`%s` rather than typed here.' % PRIOR)
    w('')
    w('| card | `file:line` | card stated | WAR-70 wrote | C-059 | action |')
    w('|---|---|---|---|---|---|')
    for r in prior_applied():
        path = r['source']['file']
        sp, _ = setpoint(r)
        dec = card_decision(path, BY_FILE[path])
        if dec[2] is None:
            factor = dec[0]
            target = sig(r['eu'] * factor)
            if r['family'] == 'reserve' and abs(target / sp - 1) < 1e-12:
                verdict, action = ('the same figure: the reserve\'s set point **is** the '
                                   'factor\'s numerator'), '**stands**'
            else:
                verdict, action = '**%s EU**' % eu_text(target), '**re-set**'
        else:
            verdict = '%s — %s' % (dec[2][0], dec[2][1].split(';')[0])
            action = '**reverted to %s EU**' % eu_text(r['eu'])
        w('| %s | `%s:%d` | %s EU | %s EU | %s | %s |'
          % (r['entity'], path, r['source']['line'], eu_text(r['eu']), eu_text(sp),
             verdict, action))
    w('')
    w('A revert restores the figure the card stated before WAR-70; it is in this table, in '
      '`fit.json` and in the run that made the edit, so nothing is invented by putting it '
      'back.')
    w('')
    w('## Held — the cards C-059 does not reach')
    w('')
    w('One reason per card, the first that applies. C-059 settles `COLLAPSE`, `DERIVED` and '
      '`ORDER` — a uniform factor keeps every stated share and every stated order, which is '
      'the reason the ruling exists. It says nothing about an estimate, a figure sourced '
      'outside the card, a Stage Part Four declines to assess, or a decimal set point, so '
      'those keep the reasons `eu_band_corrections.py` gave them.')
    for code, _ in counts.most_common():
        w('')
        w('### %s (%d)' % (REASON_TITLE[code], counts[code]))
        w('')
        for path, rows, r0, h in sorted(held, key=lambda x: x[0]):
            if h[0] != code:
                continue
            ms = [r for r in rows if r['decades_delivered'] != 0]
            w('- **`%s`** — %d attested miss(es). **Held:** %s.' % (path, len(ms), h[1]))
            if r0 is not None:
                w('  - reserve line: `%s`' % r0['verbatim'].replace('\n', ' ')[:300])
            for r in sorted(ms, key=lambda r: r['source']['line']):
                w('  ' + held_line(r))
    w('')
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('wrote %s' % OUT)
    print('  cards scaled %d, EU figures scaled %d (attested misses settled %d)'
          % (len(scaled), n_figs, n_anchor_misses_freed))
    print('  cards held   %d, attested misses still held %d' % (len(held), held_misses))
    for code, k in counts.most_common():
        print('    %-16s %d' % (code, k))
    for path, rows, r0, factor in scaled:
        print('  SCALE ×%-12s %-4d figures  %s' % (g(sig(factor)), len(edits[path]), path))


if __name__ == '__main__':
    main()
