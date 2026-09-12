#!/usr/bin/env python3
"""The table's running state as structured data: Fronts as clocks, the Ledger
that comes due, the session log, the NPC roster.

  table/fronts.yaml    one entry per Front: thread, want, clock (ticks), position, last/next move
  table/ledger.yaml    one entry per line that has cost something: category, who, text, opened, due
  table/sessions.yaml  one entry per session: date, thread, what advanced, what came due
  table/npcs.yaml      per-thread roster: want, refusal line, knows, has lied about, last seen

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

FILES = {k: TABLE / f"{k}.yaml" for k in ("fronts", "ledger", "sessions", "npcs")}


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


def set_clock(front_id: str, ticks: list[str]) -> dict:
    rows = load("fronts")
    for r in rows:
        if r["id"] == front_id:
            r["clock"] = [{"tick": i + 1, "consequence": t} for i, t in enumerate(ticks)]
            save("fronts", rows)
            return r
    raise KeyError(front_id)


def add_front(name: str, thread: str, want: str, ticks: list[str], next_move: str = "") -> dict:
    rows = load("fronts")
    r = {"id": slug(name), "name": name, "thread": thread, "status": "open", "want": want, "last_move": "",
         "next_move": next_move or (ticks[0] if ticks else ""), "clock": [{"tick": i + 1, "consequence": t} for i, t in enumerate(ticks)],
         "position": 0, "last_advanced": None, "seeded_from": "added at the table"}
    rows.append(r)
    save("fronts", rows)
    return r


def due(sessions_old: int = 2, thread: str | None = None) -> list:
    """Open ledger lines that have waited long enough to come due."""
    rows = load("ledger")
    now = session_count()
    out = []
    for r in rows:
        if r.get("status") != "open":
            continue
        age = now - int(r.get("opened_session", 0))
        d = r.get("due")
        if d and d != "pending Natalie":
            if str(d).isdigit() and age >= int(d):
                out.append((age, r))
            elif not str(d).isdigit():
                out.append((age, r))  # a stated condition: surface it, she judges
        elif age >= sessions_old and r["category"] in ("debts", "who knows what", "injuries and reserve", "reputation"):
            out.append((age, r))
    out.sort(key=lambda x: -x[0])
    return [dict(r, age_sessions=a) for a, r in out]


def ledger_add(category: str, who: str, text: str, due_after=None) -> dict:
    rows = load("ledger")
    n = max([int(r["id"][1:]) for r in rows] + [0]) + 1
    r = {"id": f"L{n:03d}", "category": category, "who": who, "text": text, "opened": date.today().isoformat(),
         "opened_session": session_count(), "due": due_after, "status": "open"}
    rows.append(r)
    save("ledger", rows)
    return r


def ledger_collect(entry_id: str, how: str) -> dict:
    rows = load("ledger")
    for r in rows:
        if r["id"] == entry_id:
            r["status"] = "collected"
            r["collected"] = {"session": session_count(), "date": date.today().isoformat(), "how": how}
            save("ledger", rows)
            return r
    raise KeyError(entry_id)


def session_log(thread: str, advanced: list[str], came_due: list[str], notes: str = "", when: str = "") -> dict:
    rows = load("sessions")
    r = {"n": len(rows) + 1, "date": when or date.today().isoformat(), "thread": thread, "advanced": advanced, "came_due": came_due, "notes": notes}
    rows.append(r)
    save("sessions", rows)
    return r


def roster(thread: str | None = None) -> list:
    rows = load("npcs")
    return [r for r in rows if not thread or thread.lower() in r.get("thread", "").lower()]


def npc_set(name: str, thread: str, **fields) -> dict:
    rows = load("npcs")
    for r in rows:
        if r["name"].lower() == name.lower() and (not thread or r.get("thread", "").lower() == thread.lower()):
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


# --------------------------------------------------------------------------
# rendering


def render() -> dict:
    TABLE.mkdir(exist_ok=True)
    out = {}
    fr = load("fronts")
    lines = ["# Fronts, as clocks", "", "Generated from table/fronts.yaml by WOTR MCP. Advance with advance_front; the prose Fronts page in Notion stays Natalie's.", ""]
    for thread in dict.fromkeys(r["thread"] for r in fr):
        lines.append(f"## {thread}")
        lines.append("")
        for r in [x for x in fr if x["thread"] == thread]:
            pos, n = int(r.get("position", 0)), len(r["clock"])
            bar = "●" * pos + "○" * (n - pos)
            lines.append(f"**{r['name']}** {bar} {pos}/{n} · {r.get('status', 'open')}")
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
    lines = ["# The Ledger, structured", "", f"Generated from table/ledger.yaml by WOTR MCP. {sum(1 for r in lg if r['status'] == 'open')} open lines. `due()` says what comes due tonight.", ""]
    for cat in dict.fromkeys(r["category"] for r in lg):
        lines.append(f"## {cat}")
        lines.append("")
        for r in [x for x in lg if x["category"] == cat]:
            flag = "~~" if r["status"] == "collected" else ""
            lines.append(f"- `{r['id']}` {flag}{r['text']}{flag}" + (f"  *(due: {r['due']})*" if r.get("due") else ""))
        lines.append("")
    (TABLE / "LEDGER.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    out["ledger"] = len(lg)

    np_ = load("npcs")
    lines = ["# NPC roster", "", "Generated from table/npcs.yaml by WOTR MCP.", ""]
    for thread in dict.fromkeys(r.get("thread", "") for r in np_):
        lines.append(f"## {thread}")
        lines.append("")
        for r in [x for x in np_ if x.get("thread", "") == thread]:
            lines.append(f"**{r['name']}** · wants: {r.get('want') or '—'} · refuses: {r.get('refusal_line') or '—'} · last seen: {r.get('last_seen') or '—'}")
            if r.get("knows"):
                lines.append(f"  - knows: {'; '.join(r['knows'])}")
            if r.get("lied_about"):
                lines.append(f"  - has lied about: {'; '.join(r['lied_about'])}")
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
