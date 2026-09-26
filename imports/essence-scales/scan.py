#!/usr/bin/env python3
"""Read every mirrored page against the essence scales, and build the edit plan.

WAR-161. Reads `wiki/` — the hourly Notion mirror, which is what the live pages
say — and reports, page by page:

  * every EU reserve figure against its Stage's EU band
  * every AU/s figure against its Stage's AU/s band, and against AU/s = FD x eta
  * every eta against its Tier of Standing's range
  * every surviving lettered Coherence Band, with the Tier of Standing the page's
    own Stage makes derivable
  * every duration stated in turns, with its length in seconds at 6 s a turn

Nothing is written to `wiki/`. The plan it emits (`_plan.json`) is the list of
Notion edits, each as an exact old_str from the mirror and the new_str that
replaces it.

Run:  python3 imports/essence-scales/scan.py            # the report, as markdown
      python3 imports/essence-scales/scan.py --plan     # write _plan.json
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scales  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI = os.path.join(REPO, "wiki")
HERE = os.path.dirname(os.path.abspath(__file__))

ROMAN = ["XVI", "XV", "XIV", "XIII", "XII", "XI", "X", "IX", "VIII", "VII",
         "VI", "V", "IV", "III", "II", "I"]
STAGE_ROW = {r["stage"]: r for r in scales.rows()}

# A lettered Coherence Band token. The live Level Bands are I to V (Roman), so a
# Band whose token is one of those is left alone; R44-6 confirms that reading.
LETTERED = r"(?:SSS|SS|EX\+|EX|[A-GS])"
BAND_RE = re.compile(r"(?<![A-Za-z])((?:Coherence\s+)?Band)\s+(\*{0,2})(" + LETTERED + r")(\*{0,2})(?![A-Za-z0-9])")

WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
           "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
           "twelve": 12, "fifteen": 15, "twenty": 20, "thirty": 30}
TURN_RE = re.compile(
    r"(?<![\w-])(\d{1,3}(?:[–\-]\d{1,3})?|" + "|".join(WORDNUM) + r")"
    r"(\s+|\-)(turns?)(?![\w])", re.IGNORECASE)

EU_RE = re.compile(r"([\d][\d,\.]*(?:×10\^-?\d+)?|\d+(?:\.\d+)?×10\^-?\d+)\s*EU(?![/a-zA-Z])")
EU_SCI = re.compile(r"(\d+(?:\.\d+)?)×10\^(-?\d+)")
# The value must follow the label directly: a fragment that starts with anything
# but a figure is a sentence about the field, not the field.
RESERVE_RE = re.compile(r"EU\s*Reserve[:\*\s·]*(~?[\d][^·|\n]*)")
AUS_RE = re.compile(r"AU/s[:\*\s]*(~?[\d][^·|\n]*)")
# the other form: the figure first, the unit after ("7,600 AU/s", "6.7×10^14 AU/s")
AUS_PRE = re.compile(r"([\d][\d,\.]*(?:×10\^-?\d+)?|\d+(?:\.\d+)?×10\^-?\d+)\s*(?:million\s*)?AU/s")
FD_RE = re.compile(r"Flux\s*Density[:\*\s·]*(~?[\d][^·|\n]*)")
ETA_RE = re.compile(r"(?:Efficiency\s*\(η\)|\bη\b)[^0-9\n]{0,40}?(\d(?:\.\d+)?)")


def num(s):
    """The first number in a fragment, in either notation, or None."""
    s = s.replace("**", "").replace("*", "").strip()
    m = EU_SCI.search(s)
    if m:
        return float(m.group(1)) * 10 ** int(m.group(2))
    m = re.search(r"\d[\d,]*(?:\.\d+)?", s)
    if not m:
        return None
    return float(m.group(0).replace(",", ""))


R = "|".join(ROMAN)
NAMES = ("Murmuring|Welling|Ascension|Flourishing|Splintering|Glory|Refraction|"
         "Transcendence|Invocation|Realization|Dissonance|Emanation|"
         "Principality|Zenith|Revelation|Apex")
# The subject's own Stage, in the three forms the cards use, most authoritative
# first. A bare "Stage I" anywhere in the page is the weakest reading and is used
# only when nothing better exists: a Catalyst row or a point-economy line names
# Stages that are not the subject's.
FIELD_RE = re.compile(r"(?:Temperance\s+Stage|Level\s*/\s*Stage)")
FIELD_VAL = re.compile(r"Stage[\s*·:,|]*(" + R + r")\b")
NAMED_RE = re.compile(r"\b(" + R + r")\s*[—·,\-]\s*(?:the\s+)?(?:" + NAMES + r")")
BARE_RE = re.compile(r"Stage\s+(" + R + r")\b")


def stage_of(text):
    """The Stage the page states for its subject, as a Roman numeral, or None."""
    for ln in text.split("\n"):
        if FIELD_RE.search(ln):
            m = FIELD_VAL.search(ln)
            if m:
                return m.group(1)
    m = NAMED_RE.search(text)
    if m:
        return m.group(1)
    counts = {}
    for m in BARE_RE.finditer(text):
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    if counts:
        return max(counts, key=lambda k: counts[k])
    return None


def pages():
    for root, _, files in os.walk(WIKI):
        for f in sorted(files):
            if f.endswith(".md"):
                p = os.path.join(root, f)
                yield os.path.relpath(p, REPO), open(p, encoding="utf-8").read()


def in_band(v, lo, hi):
    if v is None or lo is None or hi is None:
        return None
    return lo <= v <= hi


def scan():
    out = []
    for rel, text in pages():
        lines = text.split("\n")
        stage = stage_of(text)
        row = STAGE_ROW.get(stage)
        rec = dict(page=rel, stage=stage, tier=row["tier"] if row else None,
                   eta=None, reserves=[], aus=[], fd=None, bands=[], turns=[])
        m = ETA_RE.search(text)
        if m:
            try:
                rec["eta"] = float(m.group(1))
            except ValueError:
                pass
        for i, ln in enumerate(lines, 1):
            for mm in RESERVE_RE.finditer(ln):
                v = num(mm.group(1))
                if v:
                    rec["reserves"].append(dict(line=i, value=v,
                                                text=mm.group(1).strip()))
            got = False
            for mm in AUS_RE.finditer(ln):
                v = num(mm.group(1))
                if v:
                    rec["aus"].append(dict(line=i, value=v,
                                           text=mm.group(1).strip()))
                    got = True
            if not got:
                for mm in AUS_PRE.finditer(ln):
                    v = num(mm.group(1))
                    if v is None:
                        continue
                    if "million" in ln[mm.start():mm.end()]:
                        v *= 1e6
                    rec["aus"].append(dict(line=i, value=v,
                                           text=mm.group(0).strip()))
            if rec["fd"] is None:
                mm = FD_RE.search(ln)
                if mm and num(mm.group(1)):
                    rec["fd"] = dict(line=i, value=num(mm.group(1)),
                                     text=mm.group(1).strip())
            for mm in BAND_RE.finditer(ln):
                rec["bands"].append(dict(line=i, token=mm.group(0),
                                         label=mm.group(1), letter=mm.group(3)))
            for mm in TURN_RE.finditer(ln):
                raw = mm.group(1)
                if "–" in raw or "-" in raw:
                    parts = re.split(r"[–\-]", raw)
                    secs = [int(p) * 6 for p in parts if p.isdigit()]
                    n = None
                else:
                    n = WORDNUM.get(raw.lower(), None)
                    if n is None and raw.isdigit():
                        n = int(raw)
                    secs = [n * 6] if n else []
                rec["turns"].append(dict(line=i, token=mm.group(0), n=n,
                                         seconds=secs, raw=raw))
        # readings against the ladder
        rec["eu_readings"] = []
        if row:
            for r in rec["reserves"]:
                rec["eu_readings"].append(dict(
                    line=r["line"], value=r["value"],
                    band=(row["eu_floor"], row["eu_ceiling"]),
                    inside=in_band(r["value"], row["eu_floor"], row["eu_ceiling"])))
        rec["aus_readings"] = []
        if row:
            for a in rec["aus"]:
                rec["aus_readings"].append(dict(
                    line=a["line"], value=a["value"],
                    band=(row["aus_floor"], row["aus_ceiling"]),
                    inside=in_band(a["value"], row["aus_floor"], row["aus_ceiling"])))
        rec["formula"] = None
        if rec["fd"] and rec["eta"] and rec["aus"]:
            exp = rec["fd"]["value"] * rec["eta"]
            rec["formula"] = dict(expected=exp, stated=rec["aus"][0]["value"],
                                  holds=abs(exp - rec["aus"][0]["value"]) <=
                                  max(1.0, 0.005 * exp))
        rec["eta_reading"] = None
        if row and rec["eta"] is not None:
            lo, hi = row["eta"]
            if lo == hi:          # Part Nineteen writes these four with a tilde
                lo, hi = lo - 0.05, hi + 0.05
            rec["eta_reading"] = dict(eta=rec["eta"], tier_band=(lo, hi),
                                      inside=(lo <= rec["eta"] <= (hi or 1e9)))
        if (rec["reserves"] or rec["aus"] or rec["bands"] or rec["turns"]
                or rec["eta"] is not None):
            out.append(rec)
    return out


def is_card(rel):
    return ("Volume I — Character Cards" in rel or "/Sodoku Moto/" in rel
            or "Summoned and Bound" in rel or "Called · Summon Register" in rel)


def report(recs):
    L = ["# WAR-161 — every mirrored page read against the essence scales",
         "",
         "Generated by `imports/essence-scales/scan.py` from the `wiki/` mirror; "
         "every figure computed, none typed. The scales themselves are "
         "`imports/essence-scales/_derivation.md`.", ""]
    n_pages = len(recs)
    bands = [r for r in recs if r["bands"]]
    turns = [r for r in recs if r["turns"]]
    eu_out = [(r, x) for r in recs for x in r["eu_readings"] if x["inside"] is False]
    eu_in = [(r, x) for r in recs for x in r["eu_readings"] if x["inside"] is True]
    aus_out = [(r, x) for r in recs for x in r["aus_readings"] if x["inside"] is False]
    aus_in = [(r, x) for r in recs for x in r["aus_readings"] if x["inside"] is True]
    eta_out = [r for r in recs if r["eta_reading"] and not r["eta_reading"]["inside"]]
    f_fail = [r for r in recs if r["formula"] and not r["formula"]["holds"]]
    L += ["| | count |", "|---|---|",
          f"| pages carrying an EU, AU/s, η, Band or turn figure | {n_pages} |",
          f"| EU reserve figures read against a Stage band | {len(eu_in)+len(eu_out)} |",
          f"| — inside the band | {len(eu_in)} |",
          f"| — outside it | {len(eu_out)} |",
          f"| AU/s figures read against a Stage band | {len(aus_in)+len(aus_out)} |",
          f"| — inside the band | {len(aus_in)} |",
          f"| — outside it | {len(aus_out)} |",
          f"| η figures outside their Tier of Standing range | {len(eta_out)} |",
          f"| cards where AU/s ≠ Flux Density × η | {len(f_fail)} |",
          f"| pages carrying a surviving lettered Band | {len(bands)} |",
          f"| lettered Band occurrences | {sum(len(r['bands']) for r in bands)} |",
          f"| pages stating a duration in turns | {len(turns)} |",
          f"| turn durations | {sum(len(r['turns']) for r in turns)} |", ""]
    return "\n".join(L), dict(recs=recs)


def plan(recs):
    """The Notion edit plan: the turn conversions and the lettered Bands."""
    edits = []
    for r in recs:
        page_edits = []
        seen = set()
        for t in r["turns"]:
            if not t["seconds"] or t["n"] is None:
                continue
            key = t["raw"].lower()
            if key in seen:
                continue
            seen.add(key)
            page_edits.append(dict(kind="turn", line=t["line"],
                                   old=t["token"],
                                   new=f"{t['token']} ({t['seconds'][0]} seconds)"))
        for b in r["bands"]:
            if r["stage"]:
                row = STAGE_ROW[r["stage"]]
                page_edits.append(dict(
                    kind="band", line=b["line"], old=b["token"],
                    new=f"Tier of Standing {row['tier']}, {row['tier_name']}",
                    derivable=True, stage=r["stage"]))
            else:
                page_edits.append(dict(kind="band", line=b["line"],
                                       old=b["token"], new=None,
                                       derivable=False, stage=None))
        if page_edits:
            edits.append(dict(page=r["page"], stage=r["stage"], edits=page_edits))
    return edits


if __name__ == "__main__":
    recs = scan()
    if "--plan" in sys.argv:
        p = plan(recs)
        json.dump(dict(pages=p, scan=recs), open(os.path.join(HERE, "_plan.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(f"{len(p)} pages, {sum(len(x['edits']) for x in p)} edits")
    else:
        print(report(recs)[0])
