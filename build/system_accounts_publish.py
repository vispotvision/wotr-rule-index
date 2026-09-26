#!/usr/bin/env python3
"""Put the system accounts into Notion as a "The Two Accounts" section.

  bash build/py.sh build/system_accounts_publish.py                      # dry run
  bash build/py.sh build/system_accounts_publish.py --apply
  bash build/py.sh build/system_accounts_publish.py --apply --only "World Echelon"
  bash build/py.sh build/system_accounts_publish.py --apply --force      # ignore the hashes
  bash build/py.sh build/system_accounts_publish.py --verify 5           # read N pages back
  bash build/py.sh build/system_accounts_publish.py --audit              # what the scrub leaves
  bash build/py.sh build/system_accounts_publish.py --show "Anointing"   # the text as it will go up

Each imports/system-accounts/{Techniques,Spellcraft}/<Title>.md becomes the
section "The Two Accounts" at the foot of that working's Notion page, carrying
all five sections: the physical account, the stratal account, the mechanism
(the effect), the essence ledger, and counterplay and the challenge.

The page is the one the account's own frontmatter names — `page:`, or
`governing_page:` where the account says the listed page is a retired redirect
(The Veil). The Notion id comes from that wiki mirror file's frontmatter, so no
page id is typed here.

Clean publishing. A published page carries the content and never the process:
no conflict or ruling ids, no "logged", no "open question", no questionnaire, no
ruling or docket reference, no person, agent or tool name, nothing about where
the text came from or what made it. `scrub()` takes that out of the account at
publish time; the account files themselves are the working record and keep
saying all of it. What the scrub does, in the order it does it:

  BLOCKS   The two roll-up paragraphs every account ends its sections with
           ("Conflicts logged from this page:", "Conflicts added by this
           section:"), the "The fairness check" lead-in, and the fairness table
           itself (its header is the give-away, `| Test | Verdict | Why |`) are
           dropped whole. That table is an audit of the write-up — its verdicts
           are "cannot be checked" and "the best route is not on the page" —
           so it is process, not the working. Section 5's substance, the
           Counterplay routes, the tell, the limits and the lookup trail, stays.
  PHRASES  A citation that hangs off a sentence comes out and the sentence
           stays: a parenthetical id, a bare id standing as its own sentence,
           "as corrected by R44-4" and the `RULINGS.md` line it cites, and the
           estimator on a figure ("flagged as an estimate") — the rule is that
           an estimate is published as its figure, without the estimator.
  SENTENCE A sentence still naming the process after that is about how the
           corpus is made, not about the working, and the sentence goes.

The word lists are phrases, never bare words, because the bare words are
content here: "Hooke proposed something startling", "resonance conflict",
"internal conflict", "not a ruling but arithmetic" all stay, and so does
**Isaac Luria**, the Kabbalist the Vorynn lens is built on — the one place a
name that also belongs to a person outside the fiction is in fact the fiction.
`--audit` runs a deliberately wider net over the scrubbed text than the scrub
itself uses and prints every hit, so what the scrub leaves is read, not assumed.

A page that already carries the section has it replaced; nothing above it is
touched and no block this script did not create is deleted. The account's own
headings are demoted one level, so the section is one heading_2 with heading_3
parts under it and both the section boundary and a neighbouring Lore section
stay findable. imports/system-accounts/_published.json remembers what went up,
so an unchanged account is skipped. The hourly sync mirrors the pages back into
wiki/.
"""
import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notion_export import api, paginate  # noqa: E402
from notion_publish import md_to_blocks, rich_text  # noqa: E402
from notion_publish import BATCH  # noqa: E402,F401  (kept for the batching below)

ROOT = Path(__file__).resolve().parent.parent
SA = ROOT / "imports" / "system-accounts"
STATE = SA / "_published.json"
SECTIONS = ("Techniques", "Spellcraft")
HEAD = "The Two Accounts"
# Bumped when the shape of the section changes, so every page is rewritten once.
# 2: clean publishing — the open-question callouts are gone and the account text
#    is scrubbed of the process before it goes up.
FORMAT = 4  # 4: the field-format edition (matches the page's Summary card / Codex line look)


# --------------------------------------------------------------------------
# the repo side


def frontmatter(md: str) -> dict:
    """The account files' frontmatter is one `key: value` per line, no nesting."""
    if not md.startswith("---\n"):
        return {}
    end = md.find("\n---", 4)
    if end < 0:
        return {}
    out = {}
    for ln in md[4:end].split("\n"):
        if ":" in ln and not ln.startswith(" "):
            k, v = ln.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def body(md: str) -> str:
    """The account without its frontmatter and its H1, every heading demoted one."""
    if md.startswith("---\n"):
        end = md.find("\n---", 4)
        if end >= 0:
            md = md[md.find("\n", end + 1) + 1:]
    lines = [ln for ln in md.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(r"^#\s", lines[0]):        # "# System account · X" — the page is titled X
        lines.pop(0)
    out = []
    for ln in lines:
        m = re.match(r"^(#{1,5})(\s.*)$", ln)
        out.append(("#" + m.group(1) + m.group(2)) if m else ln)
    return "\n".join(out).strip("\n")


def wiki_page(md: str, name: str) -> tuple[str | None, str]:
    """(repo path of the wiki mirror file, why) for an account's frontmatter."""
    fm = frontmatter(md)
    page = fm.get("page") or ""
    if (ROOT / page).is_file():
        return page, "page:"
    gov = fm.get("governing_page") or ""
    if (ROOT / gov).is_file():
        return gov, f"governing_page: ({page} is not a file)"
    return None, f"no page on disk (page: {page!r} governing_page: {gov!r})"


def notion_of(wiki_rel: str) -> tuple[str | None, str | None]:
    fm = frontmatter((ROOT / wiki_rel).read_text(encoding="utf-8"))
    return fm.get("notion_id") or None, fm.get("title") or None


def accounts() -> list[Path]:
    return sorted((f for s in SECTIONS for f in (SA / s).glob("*.md")),
                  key=lambda p: (p.parent.name, p.name))


# --------------------------------------------------------------------------
# clean publishing: the page carries the content, never the process

ID = r"(?:SA-[A-Z][A-Z0-9-]*|C-\d{3}|R44-\d+|R20C-\d+|R1[39]-\d+|WAR-\d+)"
_M = r"[`*_]*"          # the emphasis and code ticks an id is usually wrapped in

# Paragraphs whose whole subject is the process. Dropped entire.
DROP_BLOCK = re.compile(
    r"^\**(?:Conflicts logged from this page|Conflicts added by this section|"
    r"Conflicts? (?:logged|added|recorded)\b[^*]*|The fairness check|"
    # An account that opens with an editorial note on its own scope — which page
    # it reads, why its five sections are shaped as they are (The Veil's). The
    # note is the job talking about itself, and it goes whole rather than
    # sentence by sentence, which would leave the tail of its quotation dangling.
    r"A note on which|An? (?:second )?note,? (?:on|because)|And a second note)\b", re.I)
# The fairness table audits the write-up, not the working: "cannot be checked",
# "the best route is not on the page". Its header is how it is known.
DROP_TABLE = re.compile(r"^\|[^\n]*\bVerdict\b", re.I)

# Taken out of a sentence that otherwise stays.
STRIP: list[tuple[re.Pattern, str]] = [
    # "(`SA-GAP-X`)", "(`SA-A`, `SA-B` and its kin)", "(C-053)", "(already `SA-X`)"
    (re.compile(r"[  ]*\((?:already[  ]+)?" + _M + ID + _M
                + r"(?:[  ]*(?:,|and|·|/)[  ]*" + _M + ID + _M + r")*"
                + r"(?:[  ]+and its kin)?\)"), ""),
    # a sentence that is nothing but its id, or a run of them:
    # "… should carry it. `SA-PHYS-X`." / "… none. `SA-A`, `SA-B`."
    (re.compile(r"(?<=[.!?])[  \n]+" + _M + ID + _M
                + r"(?:[  ]*(?:,|and|·|/)[  ]*" + _M + ID + _M + r")*[  ]*\."), ""),
    # The ruling that corrected a figure: the figure stays, the ruling goes. The
    # brackets come off as a pair or not at all — an optional "\)?" eats the
    # closing bracket of the citation the ruling sits *inside*, and
    # "(Part Nineteen as corrected by R44-4)" publishes as "(Part Nineteen".
    (re.compile(r"[  ]*\(as corrected by[  ]+" + _M + r"R44-\d+" + _M + r"\)"), ""),
    (re.compile(r"[  ]*as corrected by[  ]+" + _M + r"R44-\d+" + _M), ""),
    (re.compile(r",?[  ]*" + _M + r"RULINGS\.md" + _M + r":\d+"), ""),
    (re.compile(r",?[  ]*" + _M + r"CONFLICTS\.md" + _M + r"[  ]*"), ""),
    # an estimate is published as its figure, without the estimator
    (re.compile(r",?[  ]*(?:and[  ]+)?flagged[  ]+(?:there[  ]+|by the (?:page|card)"
                r"(?:[  ]+itself)?[  ]+)?as an estimate"), ""),
    (re.compile(r",?[  ]*flagged[  ]+by the (?:page|card)(?:[  ]+itself)?"
                r"(?:[  ]+as unsourced)?"), ""),
    (re.compile(r",?[  ]*(?:as[  ]+)?flagged[  ]+as[  ]+unsourced"), ""),
    (re.compile(r"[  ]*\(" + _M + r"(?:my|our)[  ]+\w+" + _M + r"\)"), ""),
    # A glyph the working's own page does not name. The glyph forms themselves are
    # canon (the Master Glyph Index's attested forms); what is unsettled is which
    # of them this working runs on, and an unsettled point is published as the
    # best-supported reading without a word about its being unsettled.
    (re.compile(r"[  ]*\(proposed[^)]*\)"), ""),
    # The method note is how the batch was made, so a citation of it comes out.
    (re.compile(r"[  ]*\([^()]*" + _M + r"_method\.md" + _M + r"[^()]*\)"), ""),

    # ---- the job talking about itself, phrase by phrase ----
    # These come out of the sentence rather than taking it with them, because the
    # sentence around them is the content: a cost comparison, a Tier-band check,
    # a doctrine. Several sit inside table cells, where losing the sentence loses
    # the cell. STRIP runs before PROCESS, so a phrase taken out here is also a
    # sentence PROCESS no longer matches.
    #
    # "the Spellcraft batch" is the production run and means nothing to a reader
    # of one page; the craft it names means something, so the scope survives as
    # the craft and the claim keeps the reach it was written with.
    (re.compile(r"\bin the (Spellcraft|Techniques) batch\b"), r"in \1"),
    (re.compile(r"\bin the whole batch\b"), ""),
    # Which page best exemplifies the exercise is a judgement about the exercise.
    (re.compile(r",?[  ]*and this is the page the whole batch"
                r"[  ]+should be[  ]+measured against"), ""),
    # The write-up declining to answer. That the source is silent is a fact about
    # the system and stays; the account's own inability to settle it is process.
    # An unsettled point publishes as the best-supported text without comment,
    # and choosing between the readings is not this job's to do.
    (re.compile(r",?[  ]*so the account cannot say whether[^.|]*"), ""),
    (re.compile(r"[  ]*and the account cannot tell whether[^.|]*"), ""),
    (re.compile(r"\bunresolved accounting question\b"), "accounting question"),
    (re.compile(r"[  ]*with no precedent anywhere in the system\b"), ""),
    # The one place the sentence is built round "cannot say … and can say": the
    # silence is the system's, and what follows it is the figure that matters.
    (re.compile(r"The account cannot say this breaches an Aetheric Density"
                r"[  ]+ceiling because the system states no numeric ceiling,"
                r"[  ]+and it can say that[  ]+"),
     "The system states no numeric Aetheric Density ceiling, and "),
]

# A sentence that says any of these is about how the corpus is made. It goes.
# Phrases, never bare words: "proposed", "conflict" and "ruling" are content
# here ("Hooke proposed", "resonance conflict", "not a ruling but arithmetic").
PROCESS = re.compile("|".join([
    ID,
    r"\bfiling decision\b",
    r"\blogged\b", r"\blogs it\b", r"\blog it\b",
    r"\bopen questions?\b",
    r"awaiting[\s-]+ruling", r"held for ruling", r"\bfor ruling\b",
    r"needs[\s-]+ruling", r"until (?:\w+ ){0,3}rules\b", r"when it is ruled",
    r"\bruling still owed\b", r"\bstill owed\b", r"\bre-litigated\b",
    # "ratified" only as a process word: "A ratified blade does not chip" is a
    # line of canon and stays.
    r"pending ratification", r"\bratified by\b",
    r"fairness check", r"questionnaire", r"\bdocket\b",
    r"originated by", r"generated from", r"WOTR MCP", r"\bMCP\b",
    r"RULINGS\.md", r"CONFLICTS\.md", r"\.claude/", r"\bfair-play\.md\b",
    r"\bIsaac\b(?![  ]+Luria)", r"\bNatalie\b", r"\bClaude\b",
    r"\bDoc Kett\b", r"\bRhett Konn\b", r"\bGemma Nye\b", r"\bCody Wix\b",
    r"\bPhenna Menon\b", r"\bLorelei Webb\b",
    r"recorded as (?:a |an )?conflict", r"recorded,? not resolved",
    r"\bnot canon\b", r"\bnot resolved here\b", r"\bnot decided here\b",
    r"this (?:account|section|batch) (?:cannot|does not|refuses)",
    r"\bthis batch\b", r"\bthe batch\b",
    # "the batch" qualified — the production run under its own name. The phrase
    # rules above rewrite the ones whose sentence is worth keeping, so a sentence
    # still saying this after STRIP is one about the job.
    r"\bthe (?:whole|Spellcraft|Techniques) batch\b",
    # A sentence whose subject is that the point is open. The point itself is
    # published as the best-supported reading elsewhere in the section; saying it
    # is open is the process talking, and no page carries it.
    r"\bnothing chooses\b", r"\bunresolved question\b",
    r"single largest unresolved quantity",
    r"\bboth cannot be true as written\b",
    r"the account cannot resolve",
    # net for the account declining to answer in a shape the phrase rules missed
    r"the account (?:cannot|could not|can't|does not)\b",
    r"\bflagged\b", r"\bflags\b",
    r"_method\.md", r"imports/system-accounts",
    # "ruling" is content as often as not here — "a century of correct rulings",
    # "not a ruling but arithmetic", "it cannot rule a thing in by ruling the
    # alternatives out" all stay — so only the phrasings that ask for one go.
    r"worth (?:a|the) ruling", r"worth ruling\b", r"\bis a ruling\b",
    r"\bneeds a ruling\b", r"pending (?:a|that) ruling", r"\bpre-ruling\b",
    r"because of a ruling", r"stays open pending",
    r"before this page can be finished",
    # the account talking about itself, or about the job that made it
    r"this account proposes", r"remain proposed\b",
    r"\bthis account\b", r"the account (?:is|reads|refuses)\b",
    r"\bthe issue (?:lists|names|asks)\b", r"\bsections below\b",
    r"\ba second note\b", r"retired on \d", r"\bis now a redirect\b",
    r"page has been retired",
]), re.I)

# Mask code spans so a period inside one never splits a sentence.
_TICK = re.compile(r"`[^`]*`")
_SPLIT = re.compile(r"(?<=[.!?])(?<!\be\.g)(?<!\bi\.e)(?<!\bcf)"
                    # \x00 is a masked code span: a sentence can begin with one,
                    # and "Page states none. `SA-…`." has to split in two for the
                    # first half to survive the second.
                    r"([`*_\"”’)\]]*)[  ]+(?=[`*_\"“‘(\[]*[\x00A-Z0-9§¶])")


def sentences(text: str) -> list[str]:
    """Split prose into sentences without ever splitting inside a code span."""
    spans: list[str] = []

    def hide(m: re.Match) -> str:
        spans.append(m.group(0))
        return f"\x00{len(spans) - 1}\x00"

    masked = _TICK.sub(hide, text)
    parts = _SPLIT.sub(lambda m: m.group(1) + "\x01", masked).split("\x01")
    return [re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], p) for p in parts]


def tidy(text: str, balance: bool = True) -> str:
    """Close the gaps a removal leaves, without touching anything it did not."""
    text = re.sub(r"\(\s*\)", "", text)                 # an emptied parenthesis
    text = re.sub(r"\[\s*\]", "", text)
    text = re.sub(r"(?<=\S)[  ]+([,.;:!?])", r"\1", text)   # " ," -> ","
    text = re.sub(r"([,;:])(\s*[.!?])", r"\2", text)        # ", ." -> "."
    text = re.sub(r"\.{2,}(?!\.)", ".", text)               # ".." -> "."
    text = re.sub(r"[  ]{2,}", " ", text)
    # Nothing here touches an emphasis marker. The removals above take a marker
    # off with the text it wrapped, so an emptied "****" does not arise, and every
    # rule that tried to clean one up cost more than it paid: "**" before a space
    # is the closing marker of a bold lead-in, and "** **" is that closer next to
    # the opener of the next phrase, not an emphasis wrapping nothing.
    text = re.sub(r"^[  ]*[,;:.][  ]*", "", text)
    # A bold span in the source sometimes opens in one sentence and closes in the
    # next. Drop the second of those and the survivor is left holding one marker,
    # which would bleed bold across the rest of the paragraph. Pairing the markers
    # left to right, the unmatched one is the last, so the last one goes.
    if balance and text.count("**") % 2:
        i = text.rfind("**")
        text = text[:i] + text[i + 2:]
    return tidy_spaces(text)


def tidy_spaces(text: str) -> str:
    return re.sub(r"[  ]{2,}", " ", text).strip()


def scrub_prose(block: str, cell: bool = False) -> str:
    """A prose paragraph with its process taken out.

    `cell` is a table cell rather than a paragraph: it keeps a short one ("≥",
    "ΔG", "0.70" are whole cells and not stubs) and leaves its emphasis markers
    alone, because a cell's bold can open on one side of a pipe and close on the
    other and balancing each side separately would strip both.
    """
    for pat, rep in STRIP:
        block = pat.sub(rep, block)
    kept = [s for s in sentences(block) if not PROCESS.search(s)]
    out = tidy(" ".join(s.strip() for s in kept if s.strip()), balance=not cell)
    if cell:
        return out
    # A paragraph left as a bare emphasis marker or a stub is not a paragraph.
    return "" if len(re.sub(r"[^0-9A-Za-z]", "", out)) < 3 else out


def pipes(row: str) -> str:
    """A table row with the pipes that are not cell separators taken out of the way.

    Three ledgers price a reverse reaction as `**≥ |ΔG| released forward**`, an
    absolute value, and `md_to_blocks` splits a row on every `|` with no notion of
    an escape — so that one cell becomes three, the table is built to the widest
    row, and a three-column ledger renders five columns wide with every other row
    padded blank. A separator here is always a pipe at the row's edge or one with
    whitespace on both sides; an inner `|ΔG|` has whitespace on one side at most.
    The ones that are not separators become U+2223 DIVIDES, which is the character
    the mathematics wanted, reads identically, and does not split a row.

    A second cell quotes a table row off another page —
    `*"| **T8** | Cataclysmic Entity | Hydra · Voidwyrm · Cerberus |"*` — whose
    pipes do have whitespace on both sides and are indistinguishable from
    separators by spacing alone. They are inside quotation marks, and a real
    separator never is, so a pipe within a quoted span is content too. Only
    applied when the row's quotes pair up, since unbalanced ones would invert it.
    """
    n = len(row)
    quoted = row.count('"') % 2 == 0
    out, inside = [], False
    for i, c in enumerate(row):
        if c == '"' and quoted:
            inside = not inside
        if c != "|":
            out.append(c)
            continue
        before, after = row[:i].strip(), row[i + 1:].strip()
        edge = not before or not after
        spaced = (i and row[i - 1] in " \t") and (i + 1 < n and row[i + 1] in " \t")
        out.append("|" if edge or (spaced and not inside) else "∣")
    return "".join(out)


def scrub_row(row: str) -> str:
    """A table row, segment by segment, keeping its pipes exactly as they were.

    The pipes are not split on and re-joined: a cell here can hold a pipe that is
    not a separator at all — `**≥ |ΔG| released forward**`, an absolute value —
    and rebuilding the row from the pieces turns three cells into five and loses
    the arithmetic. Each segment is scrubbed in place instead, so a row comes out
    with the same number of pipes it went in with, whatever they mean.
    """
    if re.fullmatch(r"\|[\s:|-]*\|", row.strip()):      # the |---|---| rule
        return row
    row = pipes(row)
    out = []
    for seg in row.split("|"):
        if not seg.strip():                             # the row's outer edges
            out.append(seg)
            continue
        had = re.search(r"[0-9A-Za-z]", seg)
        s = scrub_prose(seg.strip(), cell=True)
        if s == seg.strip():                 # nothing to take out: leave it alone,
            out.append(seg)                  # padding and all, so "|ΔG|" stays "|ΔG|"
            continue
        if had and not re.search(r"[0-9A-Za-z]", s):    # all of it was process
            s = "—"
        out.append(f" {s} ")
    return "|".join(out)


# A numbered item is "1." and never "1)". The bracket form does not appear in the
# corpus as a list, but a formula wrapped onto a second line does begin with one
# — "√(3.7 × 10⁷ ×" / "413) ≈ 1.2 × 10⁵ Pa**" — and reading that continuation as
# a fresh item cuts the bullet in two, so each half is balanced on its own and a
# bold span that opened in the first half loses both its markers.
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")


def chunks(md: str) -> list[tuple[str, list[str]]]:
    """The account as (kind, lines): heading, rule, quote, table, list, prose.

    A lead-in and the list or table under it are one block in the source, with no
    blank line between them, so splitting on blank lines alone would flatten a
    bulleted list and a blockquote into one run-on paragraph. The kind of each
    line is what groups it.
    """
    out: list[tuple[str, list[str]]] = []
    for ln in md.split("\n"):
        s = ln.strip()
        if not s:
            out.append(("blank", []))
            continue
        if re.match(r"^#{1,6}\s", s):
            kind = "heading"
        elif re.fullmatch(r"(?:-{3,}|\*{3,}|_{3,})", s):
            kind = "rule"
        elif s.startswith(">"):
            kind = "quote"
        elif s.startswith("|"):
            kind = "table"
        elif LIST_ITEM.match(ln):
            kind = "list"
        else:
            kind = "prose"
        # An indented line under a list item is that item continuing.
        if kind == "prose" and out and out[-1][0] == "list" and ln[:1] in " \t":
            out[-1][1].append(ln)
            continue
        if out and out[-1][0] == kind and kind in ("quote", "table", "list", "prose"):
            out[-1][1].append(ln)
        else:
            out.append((kind, [ln]))
    return out


def scrub(md: str) -> str:
    """The account as it is published: the content, with the process gone."""
    kept: list[str] = []
    for kind, lines in chunks(md):
        if kind == "blank":
            continue
        lead = lines[0].strip()
        if kind in ("heading", "rule"):
            kept.append(lead)
        elif kind == "quote":
            # Almost every blockquote here is a quotation of canon and comes
            # through whole. The exception is an account that opens with an
            # editorial note in quote marks (The Veil's, on which page it reads),
            # so a quote is scrubbed sentence by sentence like any other prose —
            # a quoted line of canon holds no process text and is untouched by it.
            inner = " ".join(re.sub(r"^\s*>\s?", "", ln) for ln in lines).strip()
            if DROP_BLOCK.match(inner):
                continue
            q = scrub_prose(inner)
            if q:
                kept.append("> " + q)
        elif kind == "table":
            if DROP_TABLE.match(lead):
                continue
            kept.append("\n".join(scrub_row(r) for r in lines))
        elif kind == "list":
            items: list[str] = []
            for ln in lines:
                if LIST_ITEM.match(ln) or not items:
                    items.append(ln)
                else:
                    items[-1] += " " + ln.strip()
            out = []
            for it in items:
                m = LIST_ITEM.match(it)
                marker = m.group(0) if m else ""
                text = scrub_prose(it[len(marker):])
                if text:
                    out.append(marker + text)
            if out:
                kept.append("\n".join(out))
        else:
            joined = " ".join(ln.strip() for ln in lines)
            if DROP_BLOCK.match(joined):
                continue
            para = scrub_prose(joined)
            if para:
                kept.append(para)
    # A heading with nothing under it, and a divider with nothing after it, go.
    out: list[str] = []
    for i, b in enumerate(kept):
        if re.match(r"^#{1,6}\s", b):
            rest = kept[i + 1:]
            nxt = next((x for x in rest if not re.match(r"^(---|#{1,6}\s)", x)), None)
            same = next((x for x in rest if re.match(r"^#{1,6}\s", x)), None)
            if nxt is None or (same is not None and rest.index(same) < rest.index(nxt)):
                continue
        if b.strip() == "---" and not any(
                not re.match(r"^---$", x) for x in kept[i + 1:]):
            continue
        out.append(b)
    return re.sub(r"\n{3,}", "\n\n", "\n\n".join(out)).strip() + "\n"


# What the page must not say, run over the scrubbed text as the gate.
#
# Wider than the scrub where a word is only ever process, and deliberately
# narrower where the bare word is content in this corpus — every narrowing below
# was made by reading the hits it dropped, not by assuming them:
#   "agent"      a decolourising agent, a dissociative agent, Aristotle's agent
#                that "is not acted on by its own form". Our own agents are
#                named instead, one by one.
#   "awaiting"   a soul in transit, "between, moving, awaiting arrival".
#   "conflicts"  "a norm conflicts with the higher norm", resonance conflict,
#                internal conflict. The ids and CONFLICTS.md carry the real one.
#   "ruling"     "a century of correct rulings nobody wanted", "the immunity is
#                the factor of a hundred in §1(b), not a ruling", "it cannot
#                rule a thing in by ruling the alternatives out".
#   "proposed"   "Hooke proposed something startling for its century".
#   "pending"    "not a synthesis pending. It is a metastable liquid".
#   "the board"  "takes the technique off the board before it is attempted".
#   "the author" the in-world author of a working, and "the author of a
#                nucleation event is not in a position to…".
#   "written /   "written by historians", "a Sealing role that may or may not
#    drafted by"  have been drafted by somebody competent", "the load is
#                generated by the reaction".
#   "Isaac"      Isaac Luria, the Kabbalist the Vorynn lens is built on.
AUDIT = re.compile("|".join([
    ID, r"\bisaac\b(?![  ]+Luria)", r"\bnatalie\b", r"\bclaude\b", r"\bgpt\b",
    r"\bllm\b", r"\bdoc kett\b", r"\brhett konn\b", r"\bgemma nye\b",
    r"\bcody wix\b", r"\bphenna menon\b", r"\blorelei\b", r"\bWOTR MCP\b",
    r"\blogged\b", r"\bopen question", r"awaiting[\s-]+ruling",
    r"\bflagged\b", r"\bflags\b", r"questionnaire", r"\bdocket\b",
    r"pending ratification", r"\bratified by\b", r"originated by", r"generated by WOTR", r"\bdrafted \d",
    r"at the direction of", r"\bmay change\b", r"\bestimator\b",
    r"\b(?:the board|the GM|the author) (?:has |had )?"
    r"(?:ruled|decided|asked|wants|approved)\b",
    r"pending (?:ratification|a ruling|that ruling)",
    r"worth (?:a|the) ruling", r"worth ruling\b", r"\bis a ruling\b",
    r"\bneeds a ruling\b", r"\bpre-ruling\b", r"stays open pending",
    r"\bremain proposed\b", r"this account proposes",
    # The lookup trail of wiki pages stays; a path into how this was made does not.
    r"_method\.md", r"imports/system-accounts", r"\.claude",
    r"RULINGS\.md", r"CONFLICTS\.md", r"\bnot canon\b",
    r"\bthis batch\b", r"\bre-litigated\b", r"\bfairness check\b",
]), re.I)


def ragged(text: str) -> list[str]:
    """Tables whose rows do not all hold the same number of cells.

    `md_to_blocks` builds a table to its widest row and pads the rest blank, so a
    row that splits into more cells than the header silently widens the whole
    table instead of failing. Checked here rather than trusted.
    """
    out, rows = [], []
    for ln in text.split("\n") + [""]:
        if ln.strip().startswith("|"):
            rows.append(ln.strip())
            continue
        if rows:
            counts = {len(r.strip("|").split("|")) for r in rows
                      if not re.match(r"^\|?\s*:?-{2,}", r)}
            if len(counts) > 1:
                out.append(f"ragged table, cells per row {sorted(counts)}: "
                           f"{rows[0][:70]}")
            rows = []
    return out


def audit(text: str) -> list[str]:
    hits = ragged(text)
    for ln in text.split("\n"):
        for m in AUDIT.finditer(ln):
            s = " ".join(ln.strip().split())
            a, b = max(0, m.start() - 55), min(len(ln), m.end() + 45)
            hits.append(f"{m.group(0)!r}: …{' '.join(ln[a:b].split())}…"
                        if len(s) > 110 else f"{m.group(0)!r}: {s}")
    return hits


# --------------------------------------------------------------------------
# the Notion side


EDITION = ROOT / "imports" / "system-accounts" / "_edition"


def rendered(key: str, md: str) -> str:
    """The text that goes up: the clean edition when one exists, else the scrubbed account."""
    ed = EDITION / key
    if ed.exists():
        return ed.read_text(encoding="utf-8").strip() + "\n"
    return scrub(body(md))


def section_blocks(clean: str) -> list[dict]:
    blocks = md_to_blocks(clean)
    if blocks and blocks[0]["type"] == "heading_2":        # field format: starts at "## Physics"
        return [{"object": "block", "type": "divider", "divider": {}}] + blocks
    head = {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": rich_text(HEAD)}}
    return ([{"object": "block", "type": "divider", "divider": {}}, head] + blocks)


def plain(b: dict) -> str:
    return "".join(t.get("plain_text", "") for t in b.get(b["type"], {}).get("rich_text", []))


def old_section(page_id: str) -> list[str]:
    """Block ids of an existing "The Two Accounts" section, and the divider before it."""
    blocks = list(paginate("GET", f"/blocks/{page_id}/children?page_size=100"))
    for i, b in enumerate(blocks):
        t = plain(b).strip() if b["type"].startswith("heading") else ""
        if (b["type"] == "heading_2" and t in (HEAD, "Physics")) or re.match(r"^[1-5] · (Physical|Stratal|Mechanism|Essence|Counterplay)", t):
            start = i - 1 if i and blocks[i - 1]["type"] == "divider" else i
            # the section is always the foot of the page: take it to the end, so no
            # inner heading of an older render can leave a tail behind
            return [x["id"] for x in blocks[start:]]
    return []


def verify(page_id: str) -> tuple[bool, int, list[str]]:
    """(the section is there, blocks in it, what the live text must not say)."""
    blocks = list(paginate("GET", f"/blocks/{page_id}/children?page_size=100"))
    for i, b in enumerate(blocks):
        if b["type"] == "heading_2" and plain(b).strip() in (HEAD, "Physics"):
            sec = blocks[i:]
            live = "\n".join(plain(x) for x in sec
                             if x["type"] not in ("divider", "table", "column_list"))
            return True, len(sec), audit(live)
    return False, 0, []


# --------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", nargs="*", help="substring of Section/Title")
    ap.add_argument("--force", action="store_true", help="republish even if unchanged")
    ap.add_argument("--verify", type=int, default=0, metavar="N",
                    help="after publishing, read N published pages back from Notion")
    ap.add_argument("--audit", action="store_true",
                    help="run the wide net over every scrubbed account and write nothing")
    ap.add_argument("--show", metavar="SUBSTR",
                    help="print one account as it will be published, and write nothing")
    ap.add_argument("--out", metavar="DIR",
                    help="write every scrubbed account to DIR for reading")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    files = accounts()
    texts = {f"{f.parent.name}/{f.name}": f.read_text(encoding="utf-8") for f in files}
    targets, failed = {}, []
    for key, md in texts.items():
        wiki_rel, why = wiki_page(md, key)
        if wiki_rel:
            targets[key] = wiki_rel
        else:
            failed.append((key, why))
            print(f"  NO PAGE   {key}: {why}")

    if a.show:
        for key, md in texts.items():
            if a.show.lower() in key.lower():
                print(f"=== {key} ===\n{scrub(body(md))}")
        return 0

    if a.out:
        d = Path(a.out)
        for key, md in texts.items():
            p = d / key
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(scrub(body(md)), encoding="utf-8")
        print(f"wrote {len(texts)} scrubbed account(s) to {d}")
        return 0

    if a.audit:
        total, dirty = 0, 0
        for key in sorted(texts):
            before, after = body(texts[key]), scrub(body(texts[key]))
            hits = audit(after)
            kept = len(after.split()) / max(1, len(before.split()))
            if hits:
                dirty += 1
                print(f"\n{key}  ({len(hits)} hit(s), {kept:.0%} of the words kept)")
                for h in hits[:12]:
                    print(f"    {h}")
                if len(hits) > 12:
                    print(f"    … {len(hits) - 12} more")
            total += len(hits)
        print(f"\n{total} hit(s) across {dirty} of {len(texts)} account(s)")
        return 1 if total else 0

    if a.only:
        files = [f for f in files
                 if any(s.lower() in f"{f.parent.name}/{f.stem}".lower() for s in a.only)]

    done = skipped = 0
    published: list[tuple[str, str]] = []
    for f in files:
        key = f"{f.parent.name}/{f.name}"
        md = texts[key]
        wiki_rel = targets.get(key)
        if not wiki_rel:
            continue
        pid, title = notion_of(wiki_rel)
        if not pid:
            failed.append((key, f"{wiki_rel} carries no notion_id"))
            print(f"  NO ID     {key}: {wiki_rel} carries no notion_id")
            continue
        clean = rendered(key, md)
        digest = hashlib.sha256(
            json.dumps([FORMAT, clean], ensure_ascii=False).encode("utf-8")
        ).hexdigest()[:16]
        if state.get(key, {}).get("hash") == digest and not a.force:
            skipped += 1
            continue
        if not a.apply:
            print(f"  would publish {key} -> {title or wiki_rel}")
            done += 1
            continue
        try:
            for bid in old_section(pid):
                api("DELETE", f"/blocks/{bid}")
            blocks = section_blocks(clean)
            for i in range(0, len(blocks), BATCH):
                api("PATCH", f"/blocks/{pid}/children", {"children": blocks[i:i + BATCH]})
        except RuntimeError as e:
            failed.append((key, str(e)[:160]))
            print(f"  FAILED    {key}: {str(e)[:160]}")
            continue
        state[key] = {"page": wiki_rel, "notion_id": pid, "hash": digest,
                      "blocks": len(blocks), "format": FORMAT}
        STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False, sort_keys=True) + "\n",
                         encoding="utf-8")
        done += 1
        published.append((key, pid))
        print(f"  published  {key} ({len(blocks)} blocks)")

    print(f"{'published' if a.apply else 'dry run'}: {done}, {skipped} unchanged, "
          f"{len(failed)} failed")
    for key, reason in failed:
        print(f"  failed: {key}: {reason}")

    if a.apply and a.verify and published:
        sample = random.sample(published, min(a.verify, len(published)))
        print(f"\nverifying {len(sample)} page(s) live:")
        for key, pid in sorted(sample):
            there, n, hits = verify(pid)
            print(f"  {'OK  ' if there and not hits else 'BAD '} {key}: "
                  f"section={there} blocks={n} process hits={len(hits)}")
            for h in hits[:6]:
                print(f"      {h}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
