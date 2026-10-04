#!/usr/bin/env python3
"""The table's running state as structured data: Fronts as clocks, the Ledger
that comes due, the session log, the NPC roster.

  table/fronts.yaml    one entry per Front: thread, want, clock (ticks), position, last/next move
  table/ledger.yaml    one entry per line that has cost something: category, who, text, opened, due
  table/sessions.yaml  one entry per session: date, thread, what advanced, what came due
  table/npcs.yaml      per-thread roster: want, refusal line, knows, has lied about, last seen,
                       the live lie and its tell, doing now, stands with him, look, role (R72-25, R72-26)
  table/threads.yaml   per thread: the current story date, Y-M-D in the Accord count (R72-20, R72-22)

Ledger lines carry a thread and a due_date (story date) or a due_trigger (named, marked
fired at the close); bonds, heat, projects and roads are categories, the last two with a
clock (ticks, filled). Fronts carry pace_days, story days per tick, and days_banked.

  python build/table.py seed       # first fill, parsed from the Notion Fronts and Ledger pages in wiki/
  python build/table.py render     # writes table/FRONTS.md, LEDGER.md, NPCS.md (published to Notion by sync)

The YAML is the source of truth for clocks and due-dates; the prose pages in
Notion stay Natalie's. Everything seeded here that is not in the source pages
(tick consequences, due windows) is marked "pending Natalie" for her to fill.
"""
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "table"
WIKI = ROOT / "wiki"
RP = WIKI / "The Table — Running Pieces"

FILES = {k: TABLE / f"{k}.yaml" for k in ("fronts", "ledger", "sessions", "npcs", "events", "threads")}

# R72-24, R72-28, R72-29: the new Ledger categories; projects and roads run on clocks of Isaac's sizes
LINE_CATS = {"bond": "bonds", "project": "projects", "road": "roads", "the road": "roads"}
CLOCKS = {"projects": (4, 8), "roads": (4, 6)}
STANDING = {"the dead", "bonds", "heat", "canon conflicts"}  # lines that never come due by date or trigger


def load(kind: str) -> list:
    p = FILES[kind]
    if not p.exists():
        return []
    return yaml.safe_load(p.read_text(encoding="utf-8")) or []


def save(kind: str, rows: list) -> None:
    TABLE.mkdir(exist_ok=True)
    FILES[kind].write_text(yaml.safe_dump(rows, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8", newline="\n")


def _read(p: Path) -> str:
    t = p.read_text(encoding="utf-8", errors="replace")
    if t.startswith("---\n"):
        end = t.find("\n---\n", 4)
        if end != -1:
            t = t[end + 5:]
    return t


def slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U).strip().lower()
    return re.sub(r"[\s_-]+", "-", s)[:50]


def session_count() -> int:
    return len(load("sessions"))


# story dates: "Y-M-D" in the Accord count, thirteen months of twenty-eight days. Munahi is not
# modelled, as in the bot's /date. ponytail: one calendar for every thread; Korvaeth keeps its own
# count, so set its date with pass_time(when=...) rather than trusting the arithmetic there.


def story_days(s) -> int | None:
    m = re.fullmatch(r"\s*(\d+)-(\d+)-(\d+)\s*", str(s or ""))
    if not m or not (1 <= int(m[2]) <= 13 and 1 <= int(m[3]) <= 28):
        return None
    return int(m[1]) * 364 + (int(m[2]) - 1) * 28 + int(m[3]) - 1


def story_date_from(n: int) -> str:
    y, doy = divmod(n, 364)
    return f"{y}-{doy // 28 + 1}-{doy % 28 + 1}"


def same_thread(a, b) -> bool:
    a, b = str(a or "").lower().strip(), str(b or "").lower().strip()
    return bool(a and b) and (a in b or b in a)


def thread_date(thread) -> str | None:
    return next((r.get("story_date") for r in load("threads") if same_thread(r.get("thread"), thread)), None)


# --------------------------------------------------------------------------
# seeding from the prose pages


def seed_fronts() -> list:
    text = _read(RP / "Fronts.md")
    fronts = []
    thread = "unassigned"
    for ln in text.split("\n"):
        h = re.match(r"^##\s+(.+)$", ln)
        if h:
            thread = h.group(1).strip()
            continue
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", ln.strip())
        if not m:
            continue
        name = m.group(1).strip()
        rest = m.group(2)
        closed_in_name = name.rstrip(".").endswith("Closed")
        name = re.sub(r"\.?\s*Closed\.?$", "", name).strip().rstrip(".")
        want = re.search(r"\*Want:\*\s*(.*?)(?=\s*\*(?:Last move|Next move):\*|$)", rest)
        last = re.search(r"\*Last move:\*\s*(.*?)(?=\s*\*(?:Want|Next move):\*|$)", rest)
        nxt = re.search(r"\*Next move:\*\s*(.*?)(?=\s*\*(?:Want|Last move):\*|$)", rest)
        closed = closed_in_name or rest.startswith("Closed") or "Closed." in rest[:12]
        fronts.append({
            "id": slug(name),
            "name": name,
            "thread": thread,
            "status": "closed" if closed else "open",
            "want": (want.group(1).strip() if want else (rest.strip() if not last and not nxt else "")),
            "last_move": last.group(1).strip() if last else "",
            "next_move": nxt.group(1).strip() if nxt else "",
            "clock": [
                {"tick": 1, "consequence": (nxt.group(1).strip() if nxt else "pending Natalie")},
                {"tick": 2, "consequence": "pending Natalie"},
                {"tick": 3, "consequence": "pending Natalie"},
                {"tick": 4, "consequence": "pending Natalie: the Front resolves or breaks"},
            ],
            "position": 0,
            "last_advanced": None,
            "seeded_from": "Fronts page, 2026-09-10 rebuild",
        })
    return fronts


def seed_ledger() -> list:
    text = _read(RP / "The Ledger.md")
    rows = []
    cat = "uncategorised"
    n = 0
    for ln in text.split("\n"):
        h = re.match(r"^##\s+(.+)$", ln)
        if h:
            cat = h.group(1).strip().lower()
            continue
        m = re.match(r"^-\s+(.*)$", ln.strip())
        if not m:
            continue
        body = m.group(1).strip()
        struck = body.startswith("~~")
        who = re.match(r"^\*\*(.+?)\*\*", body)
        n += 1
        rows.append({
            "id": f"L{n:03d}",
            "category": cat,
            "who": (who.group(1).strip().rstrip(",:") if who else ""),
            "text": body.replace("~~", ""),
            "opened": "2026-09-10",
            "opened_session": 0,
            "due": "pending Natalie" if cat in ("debts", "who knows what", "injuries and reserve") else None,
            "status": "collected" if struck else "open",
        })
    return rows


# --------------------------------------------------------------------------
# operations


def fronts_for(thread: str | None = None, include_closed: bool = False) -> list:
    rows = load("fronts")
    if thread:
        rows = [r for r in rows if thread.lower() in r["thread"].lower() or thread.lower() in r["name"].lower()]
    if not include_closed:
        rows = [r for r in rows if r.get("status") != "closed"]
    return rows


def advance(front_id: str, what_happened: str, next_move: str = "", session: str = "") -> dict:
    rows = load("fronts")
    for r in rows:
        if r["id"] == front_id:
            r["position"] = min(int(r.get("position", 0)) + 1, len(r["clock"]))
            r["last_move"] = what_happened
            if next_move:
                r["next_move"] = next_move
                # the next tick's consequence is what she says comes next
                for t in r["clock"]:
                    if t["tick"] == r["position"] + 1:
                        t["consequence"] = next_move
            r["last_advanced"] = session or date.today().isoformat()
            if r["position"] >= len(r["clock"]):
                r["status"] = "resolved"
            save("fronts", rows)
            return r
    raise KeyError(front_id)


def set_clock(front_id: str, ticks: list[str] | None = None, pace_days: int | None = None) -> dict:
    rows = load("fronts")
    for r in rows:
        if r["id"] == front_id:
            if ticks:
                r["clock"] = [{"tick": i + 1, "consequence": t} for i, t in enumerate(ticks)]
            if pace_days is not None:
                r["pace_days"] = pace_days  # 0 stops the calendar clock: his acts can stop it (R72-20)
            save("fronts", rows)
            return r
    raise KeyError(front_id)


def add_front(name: str, thread: str, want: str, ticks: list[str], next_move: str = "", pace_days: int | None = None) -> dict:
    rows = load("fronts")
    r = {"id": slug(name), "name": name, "thread": thread, "status": "open", "want": want, "last_move": "",
         "next_move": next_move or (ticks[0] if ticks else ""), "clock": [{"tick": i + 1, "consequence": t} for i, t in enumerate(ticks)],
         "position": 0, "last_advanced": None, "seeded_from": "added at the table"}
    if pace_days:
        r["pace_days"], r["days_banked"] = pace_days, 0
    rows.append(r)
    save("fronts", rows)
    return r


def pass_time(thread: str, days: int = 0, when: str = "") -> tuple[dict, list]:
    """Story time passes on a thread (R72-20): its date moves, and every open Front of the thread
    with a pace banks the days and ticks offscreen once per pace spent, played or not."""
    if when and story_days(when) is None:
        raise ValueError(f"story date '{when}' is not Y-M-D in the Accord count (month 1 to 13, day 1 to 28)")
    rows = load("threads")
    row = next((r for r in rows if same_thread(r.get("thread"), thread)), None)
    if row is None:
        row = {"thread": thread, "story_date": None}
        rows.append(row)
    old = story_days(row.get("story_date"))
    if when:
        if not days and old is not None:
            days = max(story_days(when) - old, 0)
        row["story_date"] = when
    elif days and old is not None:
        row["story_date"] = story_date_from(old + days)
    save("threads", rows)
    fr = load("fronts")
    owed = []
    for r in fr:
        if days and r.get("status") == "open" and r.get("pace_days") and same_thread(r.get("thread"), thread):
            n, r["days_banked"] = divmod(int(r.get("days_banked", 0)) + days, int(r["pace_days"]))
            owed += [r["id"]] * n
    save("fronts", fr)
    ticks = []
    for fid in owed:
        f = next(x for x in load("fronts") if x["id"] == fid)
        if f.get("status") != "open":
            continue  # resolved by an earlier tick of this same pass
        cons = next((t["consequence"] for t in f["clock"] if t["tick"] == int(f.get("position", 0)) + 1), f.get("next_move", ""))
        ticks.append(advance(fid, f"Offscreen, {row['story_date'] or f'{days} days on'}: {cons}"))
    return row, ticks


def due(sessions_old: int = 2, thread: str | None = None, today: str | None = None) -> list:
    """Open Ledger lines that have come due (R72-22): a story date reached (today, or the line's
    thread date), a trigger marked fired, or a clock filled. A line with neither (every row from
    before R72) keeps the old reading by session age, sorted after; a date that cannot be judged sorts last."""
    rows = load("ledger")
    now = session_count()
    out = []
    for r in rows:
        if r.get("status") != "open" or (thread and r.get("thread") and not same_thread(r["thread"], thread)):
            continue
        age = now - int(r.get("opened_session", 0))
        why, rank = None, 0
        if r.get("ticks") and int(r.get("filled", 0)) >= int(r["ticks"]):
            why = f"clock full, {r['filled']}/{r['ticks']}"
        elif r.get("fired"):
            why = f"fired ({r['fired']}): {r.get('due_trigger', '')}"
        elif r.get("due_date"):
            d, t = story_days(r["due_date"]), story_days(today or thread_date(r.get("thread") or thread))
            if d is None or t is None:
                why, rank = "date not judged: " + ("write it Y-M-D" if d is None else "no story date held for the thread (pass_time)"), 2
            elif d <= t:
                why = f"date came: {r['due_date']}"
        elif not r.get("due_trigger") and not r.get("ticks"):  # no terms (the pre-R72 rows): the old reading by session age
            d, rank = r.get("due"), 1
            if d and d != "pending Natalie":
                if not str(d).isdigit():
                    why = f"no date or trigger yet, a stated condition to judge: {d}"
                elif age >= int(d):
                    why = f"no date or trigger yet, {age} session(s) old"
            elif age >= sessions_old and r["category"] in ("debts", "who knows what", "injuries and reserve", "reputation"):
                why = f"no date or trigger yet, {age} session(s) old"
        if why:
            out.append((rank, age, why, r))
    out.sort(key=lambda x: (x[0], -x[1]))
    return [dict(r, age_sessions=a, why=w) for _, a, w, r in out]


def ledger_add(category: str, who: str, text: str, due_after=None, thread: str = "", due_date: str = "",
               due_trigger: str = "", ticks: int | None = None, level: str = "") -> dict:
    cat = category.strip().lower()
    cat = LINE_CATS.get(cat, cat)
    if due_date and story_days(due_date) is None:
        raise ValueError(f"due_date '{due_date}' is not Y-M-D in the Accord count (month 1 to 13, day 1 to 28)")
    rows = load("ledger")
    if cat in CLOCKS and not (ticks and CLOCKS[cat][0] <= ticks <= CLOCKS[cat][1]):
        raise ValueError(f"a {cat} line runs on a clock of {CLOCKS[cat][0]} to {CLOCKS[cat][1]} ticks (R72-28, R72-29); ticks={ticks}")
    if cat == "heat" and (not thread or any(r["category"] == "heat" and r.get("status") == "open" and same_thread(r.get("thread"), thread) for r in rows)):
        raise ValueError("heat is one standing line per thread (R72-24): name the thread, and raise or cool the open line with ledger_mark")
    n = max([int(r["id"][1:]) for r in rows] + [0]) + 1
    r = {"id": f"L{n:03d}", "category": cat, "who": who, "text": text, "opened": date.today().isoformat(),
         "opened_session": session_count(), "due": due_after, "status": "open"}
    r.update({k: v for k, v in (("thread", thread), ("due_date", due_date), ("due_trigger", due_trigger), ("ticks", ticks), ("level", level)) if v})
    if ticks:
        r["filled"] = 0
    if cat == "bonds":
        r["fed"], r["strained"] = [], []
    rows.append(r)
    save("ledger", rows)
    return r


def ledger_mark(entry_id: str, fed: str = "", strained: str = "", level: str = "", tick: int = 0, how: str = "") -> dict:
    """Feed or strain a bond, raise or cool heat (level in words), or fill a project or road clock."""
    rows = load("ledger")
    for r in rows:
        if r["id"] == entry_id:
            stamp = thread_date(r.get("thread")) or date.today().isoformat()
            note = f" ({how})" if how else ""
            if fed:
                r.setdefault("fed", []).append(fed)
            if strained:
                r.setdefault("strained", []).append(strained)
            if level:
                r.setdefault("marks", []).append(f"{stamp}: {r.get('level') or 'unset'} to {level}{note}")
                r["level"] = level
            if tick:
                if not r.get("ticks"):
                    raise ValueError(f"{entry_id} has no clock")
                r["filled"] = max(0, min(int(r.get("filled", 0)) + tick, int(r["ticks"])))
                r.setdefault("marks", []).append(f"{stamp}: clock {r['filled']}/{r['ticks']}{note}")
            save("ledger", rows)
            return r
    raise KeyError(entry_id)


def fire(trigger: str, thread: str | None = None) -> list:
    """Mark fired every open line whose named trigger contains these words (or whose id this is);
    a line with no thread yet answers to any thread, as in due()."""
    key = trigger.strip().lower()
    if not key:
        return []
    rows = load("ledger")
    hit = []
    for r in rows:
        if (r.get("status") == "open" and r.get("due_trigger") and not r.get("fired")
                and (r["id"].lower() == key or key in r["due_trigger"].lower())
                and (not thread or not r.get("thread") or same_thread(r["thread"], thread))):
            r["fired"] = thread_date(r.get("thread")) or date.today().isoformat()
            hit.append(r)
    if hit:
        save("ledger", rows)
    return hit


def ledger_collect(entry_id: str, how: str) -> dict:
    rows = load("ledger")
    for r in rows:
        if r["id"] == entry_id:
            r["status"] = "collected"
            r["collected"] = {"session": session_count(), "date": date.today().isoformat(), "how": how}
            save("ledger", rows)
            return r
    raise KeyError(entry_id)


def session_log(thread: str, advanced: list[str], came_due: list[str], notes: str = "", when: str = "", rulings: list[str] | None = None) -> dict:
    rows = load("sessions")
    r = {"n": len(rows) + 1, "date": when or date.today().isoformat(), "thread": thread, "advanced": advanced, "came_due": came_due, "notes": notes}
    if rulings:
        r["agent_rulings"] = rulings  # R72-33: each write of the close, a call Isaac may overturn
    rows.append(r)
    save("sessions", rows)
    return r


def roster(thread: str | None = None) -> list:
    rows = load("npcs")
    return [r for r in rows if not thread or thread.lower() in r.get("thread", "").lower()]


def npc_set(name: str, thread: str, **fields) -> dict:
    rows = load("npcs")
    for r in rows:
        if r["name"].lower() == name.lower() and (not thread or same_thread(r.get("thread"), thread)):
            r.update({k: v for k, v in fields.items() if v is not None})
            r["last_updated"] = date.today().isoformat()
            save("npcs", rows)
            return r
    r = {"name": name, "thread": thread, "want": None, "refusal_line": None, "knows": [], "lied_about": [], "last_seen": None, "voice": None}
    r.update({k: v for k, v in fields.items() if v is not None})
    r["last_updated"] = date.today().isoformat()
    rows.append(r)
    save("npcs", rows)
    return r


# R72-40: what a player may see of an NPC. Voice lines written before R72-25 carry the Judger's
# working notes after the voice itself (gloss rights, swap test, the FOW line, counterplay, the
# tell) and asides to Isaac: cut them. Want, lie, tell, knows and lied_about never leave here.
PUBLIC = ("look", "voice", "role")
_NOTES = re.compile(r"\s*\([^)]*\bIsaac\b[^)]*\)|\s*(?:Gloss rights:|Swap test:|LINE NOT SET|Counterplay:|Tell:).*", re.S)


def public_face(r: dict) -> dict:
    return {k: _NOTES.sub("", str(r[k])).strip() for k in PUBLIC if r.get(k)}


# --------------------------------------------------------------------------
# rendering


def _terms(r: dict) -> list[str]:
    """A Ledger line's thread, when it comes due, its clock and level, for LEDGER.md and the tools."""
    t = [r["thread"]] if r.get("thread") else []
    if r.get("due_date"):
        t.append(f"due {r['due_date']}")
    if r.get("due_trigger"):
        t.append(f"when {r['due_trigger']}" + (f", fired {r['fired']}" if r.get("fired") else ""))
    if r.get("ticks"):
        f, n = int(r.get("filled", 0)), int(r["ticks"])
        t.append(f"{'●' * f}{'○' * (n - f)} {f}/{n}")
    if r.get("level"):
        t.append(f"level: {r['level']}")
    if r.get("due"):
        t.append(f"due: {r['due']}")
    return t


def render() -> dict:
    TABLE.mkdir(exist_ok=True)
    out = {}
    fr = load("fronts")
    lines = ["# Fronts, as clocks", ""]
    for thread in dict.fromkeys(r["thread"] for r in fr):
        sd = thread_date(thread)
        lines.append(f"## {thread}" + (f" · story date {sd}" if sd else ""))
        lines.append("")
        for r in [x for x in fr if x["thread"] == thread]:
            pos, n = int(r.get("position", 0)), len(r["clock"])
            bar = "●" * pos + "○" * (n - pos)
            lines.append(f"**{r['name']}** {bar} {pos}/{n} · {r.get('status', 'open')}")
            if r.get("pace_days"):
                lines.append(f"- Pace: a tick every {r['pace_days']} story days, {r.get('days_banked', 0)} spent")
            if r.get("want"):
                lines.append(f"- Want: {r['want']}")
            if r.get("last_move"):
                lines.append(f"- Last move: {r['last_move']}")
            if r.get("next_move"):
                lines.append(f"- Next move: {r['next_move']}")
            for t in r["clock"]:
                mark = "x" if t["tick"] <= pos else " "
                lines.append(f"  - [{mark}] {t['tick']}. {t['consequence']}")
            lines.append("")
    (TABLE / "FRONTS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    out["fronts"] = len(fr)

    lg = load("ledger")
    lines = ["# The Ledger, structured", "", f"{sum(1 for r in lg if r['status'] == 'open')} open lines.", ""]
    for cat in dict.fromkeys(r["category"] for r in lg):
        lines.append(f"## {cat}")
        lines.append("")
        for r in [x for x in lg if x["category"] == cat]:
            flag = "~~" if r["status"] == "collected" else ""
            lines.append(f"- `{r['id']}` {flag}{r['text']}{flag}" + (f"  *({'; '.join(_terms(r))})*" if _terms(r) else ""))
            lines += [f"  - fed: {x}" for x in r.get("fed") or []] + [f"  - strained: {x}" for x in r.get("strained") or []]
        lines.append("")
    (TABLE / "LEDGER.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    out["ledger"] = len(lg)

    np_ = load("npcs")
    lines = ["# NPC roster", ""]
    for thread in dict.fromkeys(r.get("thread", "") for r in np_):
        lines.append(f"## {thread}")
        lines.append("")
        for r in [x for x in np_ if x.get("thread", "") == thread]:
            lines.append(f"**{r['name']}** · wants: {r.get('want') or '—'} · refuses: {r.get('refusal_line') or '—'} · last seen: {r.get('last_seen') or '—'}")
            if r.get("knows"):
                lines.append(f"  - knows: {'; '.join(r['knows'])}")
            if r.get("lied_about"):
                lines.append(f"  - has lied about: {'; '.join(r['lied_about'])}")
            for k, label in (("lie", "live lie"), ("tell", "its tell"), ("doing_now", "doing now"), ("stands_with", "stands with him"), ("look", "look"), ("role", "role")):
                if r.get(k):
                    lines.append(f"  - {label}: {r[k]}")
        lines.append("")
    (TABLE / "NPCS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    out["npcs"] = len(np_)
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "render"
    if cmd == "seed":
        if not FILES["fronts"].exists():
            save("fronts", seed_fronts())
        if not FILES["ledger"].exists():
            save("ledger", seed_ledger())
        if not FILES["sessions"].exists():
            save("sessions", [])
        if not FILES["npcs"].exists():
            save("npcs", [])
        print({k: len(load(k)) for k in FILES})
    print(render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
