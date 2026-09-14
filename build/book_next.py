#!/usr/bin/env python3
"""What the book needs next, and the record of Isaac's gate decisions.

  python build/book_next.py                      # what to do next (human)
  python build/book_next.py --json               # the same, for build/book_dispatch.ps1
  python build/book_next.py --approve 1          # Isaac approved chapter 1's gate
  python build/book_next.py --approve 1 --note "the ears line goes in as written"
  python build/book_next.py --reject 1 --note "re-brief: the clerk asks the king, not the Bench"
  python build/book_next.py --status             # every chapter, its state

A chapter is written when ch<NN>/final.md exists. Isaac's gate (2026-09-12): the
first three chapters are gated, then every fifth after that (8, 13, ...), and the
last chapter always gates. A gated chapter that is written and not yet decided
BLOCKS the dispatcher — nothing is written past a gate Isaac has not answered.
Decisions live in book/<slug>/gates.json and are readable in book/<slug>/GATES.md.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
FIRST_GATES = 3   # chapters 1..3 each gate
EVERY = 5         # then every fifth: 8, 13, ...


def gates_for(total: int) -> set[int]:
    g = set(range(1, min(FIRST_GATES, total) + 1))
    n = FIRST_GATES + EVERY
    while n <= total:
        g.add(n)
        n += EVERY
    g.add(total)  # the last chapter always gates
    return g


def load(slug: str) -> dict:
    d = BOOK / slug
    outline = json.loads((d / "outline.json").read_text(encoding="utf-8"))
    gates_p = d / "gates.json"
    gates = json.loads(gates_p.read_text(encoding="utf-8")) if gates_p.exists() else {}
    return {"dir": d, "outline": outline, "gates": gates, "total": len(outline["chapters"])}


def written(d: Path, n: int) -> bool:
    return (d / f"ch{n:02d}" / "final.md").exists()


def state(slug: str) -> dict:
    b = load(slug)
    d, total = b["dir"], b["total"]
    gated = gates_for(total)
    rows = []
    for c in b["outline"]["chapters"]:
        n = c["number"]
        dec = b["gates"].get(str(n), {})
        rows.append({"n": n, "title": c["title"], "written": written(d, n), "gate": n in gated,
                     "decision": dec.get("decision"), "when": dec.get("when"), "note": dec.get("note", "")})
    blocked = next((r for r in rows if r["gate"] and r["written"] and r["decision"] not in ("approved", "dropped")), None)
    rejected = next((r for r in rows if r["decision"] == "rejected"), None)
    nxt = next((r for r in rows if not r["written"]), None)
    if rejected:
        action, chapter, why = "rewrite", rejected["n"], f"chapter {rejected['n']} was rejected: {rejected['note'] or 'no note'}"
    elif blocked:
        action, chapter, why = "blocked", blocked["n"], f"chapter {blocked['n']} is written and gated; Isaac has not decided (--approve {blocked['n']} / --reject {blocked['n']})"
    elif not nxt:
        action, chapter, why = "done", None, f"all {total} chapters are written and every gate is answered"
    else:
        action, chapter, why = "write", nxt["n"], f"chapter {nxt['n']} — {nxt['title']}" + (" (a gate chapter)" if nxt["gate"] else "")
    return {"slug": slug, "action": action, "chapter": chapter, "why": why, "total": total,
            "written": sum(1 for r in rows if r["written"]), "rows": rows,
            "gated": sorted(gated), "thread": b["outline"].get("thread", ""),
            "culture": b["outline"].get("culture", "Kharven"),
            "target_words": (b["outline"]["chapters"][chapter - 1].get("target_words", 3500) if chapter else 3500)}


def write_gates_md(slug: str) -> None:
    s = state(slug)
    lines = [f"# Gates — {slug}", "",
             f"Chapters {s['written']}/{s['total']} written. Gate chapters: {', '.join(str(n) for n in s['gated'])} "
             f"(the first {FIRST_GATES}, then every {EVERY}th, and the last).", "",
             f"**Next:** {s['action']} — {s['why']}", "",
             "| # | chapter | written | gate | decision | when | note |", "|---|---|---|---|---|---|---|"]
    for r in s["rows"]:
        lines.append(f"| {r['n']} | {r['title']} | {'yes' if r['written'] else '—'} | {'yes' if r['gate'] else '—'} | "
                     f"{r['decision'] or ('waiting' if r['gate'] and r['written'] else '—')} | {r['when'] or ''} | {r['note'][:80]} |")
    lines += ["", "Decide with `python build/book_next.py --approve N` or `--reject N --note \"...\"`. "
                  "Approving does not archive the chapter: `archive_scene` is a separate call Isaac makes.", ""]
    (BOOK / slug / "GATES.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def decide(slug: str, n: int, decision: str, note: str) -> None:
    p = BOOK / slug / "gates.json"
    g = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    g[str(n)] = {"decision": decision, "when": date.today().isoformat(), "note": note}
    p.write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    write_gates_md(slug)
    print(f"chapter {n}: {decision}" + (f" — {note}" if note else ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default="kharven-year")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--approve", type=int)
    ap.add_argument("--reject", type=int)
    ap.add_argument("--drop", type=int, help="the chapter is abandoned; the dispatcher moves past it")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    if not (BOOK / a.slug / "outline.json").exists():
        print(f"no outline for '{a.slug}': run the book-chapter workflow with do_foundation first")
        return 1
    for n, d in ((a.approve, "approved"), (a.reject, "rejected"), (a.drop, "dropped")):
        if n:
            decide(a.slug, n, d, a.note)
            return 0
    s = state(a.slug)
    write_gates_md(a.slug)
    if a.json:
        print(json.dumps({k: s[k] for k in ("slug", "action", "chapter", "why", "total", "written", "thread", "culture", "target_words")}, ensure_ascii=False))
    elif a.status:
        for r in s["rows"]:
            mark = "written" if r["written"] else "—"
            print(f"{r['n']:3}  {mark:8} {'GATE' if r['gate'] else '    '}  {r['decision'] or ''}  {r['title']}")
        print(f"\n{s['action']}: {s['why']}")
    else:
        print(f"{s['action']}: {s['why']}  ({s['written']}/{s['total']} written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
