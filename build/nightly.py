#!/usr/bin/env python3
"""The nightly checks, with a diff digest: reports/nightly.md.

  python build/nightly.py            # run everything, write the digest, save the state
  python build/nightly.py --dry-run  # write the digest, do not touch the state

Runs validate, resolve and the reconcile audit; hashes every finding by (file, check,
text) against build/.nightly_state.json so the digest says what is NEW since last night,
what CLEARED, and only counts what is still open. Adds the scenes archived since the
last run, where the books stand, and the sync (push health) and weekly backup lines.
The recurrence report, the prose pass, the Büri sweep and the ChatGPT review are gone
(R79-12). Nothing here edits canon; the audit writes only under reports/. build/nightly.sh runs this at 03:30, lets Claude write the "Overnight"
note at the top, and commits the digest. The note is read in reports/nightly.md.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
REPORTS = ROOT / "reports"
STATE = ROOT / "build" / ".nightly_state.json"
DIGEST = REPORTS / "nightly.md"
PY = sys.executable


def _run(*args: str, timeout: int = 900) -> tuple[int, str]:
    p = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def _git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout.strip()


def _key(file: str, check: str, text: str) -> str:
    return hashlib.sha1(f"{file}|{check}|{text.strip()}".encode("utf-8")).hexdigest()[:12]


def _findings_from_report(path: Path, check: str, want: str = "- FAIL ") -> list[dict]:
    """(file, check, text) rows: the '## <file>' heading above each matching bullet."""
    out, cur = [], ""
    if not path.exists():
        return out
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            cur = ln[3:].strip()
        elif ln.startswith(want) and cur:
            text = ln[len(want):].strip()
            out.append({"file": cur, "check": check, "text": text, "key": _key(cur, check, text)})
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    dry = "--dry-run" in sys.argv
    now = datetime.now()
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"run": None, "findings": {}}
    last_run = state.get("run")
    lines: list[str] = []
    numbers: list[str] = []

    # 1. the gates
    code, out = _run("build/validate.py")
    validate = "PASS" if code == 0 else "FAIL"
    numbers.append(f"validate {validate}")
    if code != 0:
        lines += ["## validate.py FAILED", "", "```", out[-2500:], "```", ""]
    _run("build/resolve.py")
    docket = ROOT / "out" / "docket.md"
    m = re.search(r"(\d+) outstanding", docket.read_text(encoding="utf-8")) if docket.exists() else None
    numbers.append(f"docket {m.group(1) if m else '?'} outstanding")
    conflicts = ROOT / "CONFLICTS.md"
    open_c = len(re.findall(r"(?m)^\*\*Status:\*\*\s*open", conflicts.read_text(encoding="utf-8"))) if conflicts.exists() else 0
    numbers.append(f"conflicts open {open_c}")

    # 2. the reconcile audit (writes reports/reconcile.md)
    import audit as A
    findings: list[dict] = []
    try:
        findings += _findings_from_report(A.reconcile(), "reconcile", "- ")
    except Exception as e:  # noqa: BLE001
        lines += ["## reconcile audit failed", "", f"    {e}", ""]
    # 3. the diff against last night
    seen = state.get("findings", {})
    by_key = {f["key"]: f for f in findings}
    new = [f for k, f in by_key.items() if k not in seen]
    cleared = [seen[k] for k in seen if k not in by_key]
    still = len(by_key) - len(new)
    numbers.append(f"findings NEW {len(new)} / CLEARED {len(cleared)} / STILL OPEN {still}")

    # 4. scenes archived since the last run
    since = last_run or (now - timedelta(days=1)).isoformat()
    added = _git("log", f"--since={since}", "--diff-filter=A", "--name-only", "--pretty=format:", "--", "scenes/*.md")
    new_scenes = sorted({p for p in added.splitlines() if p.startswith("scenes/") and "/cast/" not in p
                         and Path(p).name not in ("CAST.md", "TIMELINE.md", "ARCS.md", "MANIFEST.md", "INDEX.md")})

    # 6. where the book stands (the dispatcher ran at 02:00)
    books = []
    for outline in sorted((ROOT / "book").glob("*/outline.json")):
        slug = outline.parent.name
        try:
            import book_next as B
            s = B.state(slug)
            disp = outline.parent / "DISPATCH.md"
            last = disp.read_text(encoding="utf-8").strip().splitlines()[:1] if disp.exists() else []
            books.append((slug, s, last[0] if last else ""))
        except Exception as e:  # noqa: BLE001
            books.append((slug, None, f"book_next failed: {e}"))

    # 7. the sync and the backup
    def tail_log(name: str, hours: int = 26) -> list[str]:
        p = ROOT / "build" / name
        if not p.exists():
            return [f"{name}: no log"]
        cutoff = now - timedelta(hours=hours)
        keep = []
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                if datetime.strptime(ln[:19], "%Y-%m-%d %H:%M:%S") >= cutoff:
                    keep.append(ln)
            except ValueError:
                continue
        return keep
    sync = tail_log("sync.log")
    pushed = sum(1 for ln in sync if "pushed" in ln)
    failed = [ln for ln in sync if "push failed" in ln]  # build/sync.sh alerts only on a failed push
    quiet = sum(1 for ln in sync if "no wiki changes" in ln)
    # The backup is WEEKLY (wotr-backup.timer, Sunday 03:00). The old line printed the last
    # log line with its date cut off under a "last 26 h" heading, so a six-day-old zip read
    # as a missed nightly run, and once the twelve-zip limit is hit the last line is a
    # "pruned ..." line, not the zip. Show the newest "wrote" line with its date and age,
    # and call it missing only past eight days.
    wrote = [ln for ln in tail_log("backup.log", hours=24 * 8) if "  wrote " in ln]
    if wrote:
        age = (now - datetime.strptime(wrote[-1][:19], "%Y-%m-%d %H:%M:%S")).days
        backup_line = f"weekly (Sunday 03:00), last {wrote[-1][:10]} ({age} day(s) ago, on schedule): {wrote[-1][21:]}"
    else:
        backup_line = "weekly (Sunday 03:00): MISSING, no zip written in the last eight days (build/backup.log)"

    # 8. the digest
    head = [f"# Nightly — {now:%Y-%m-%d %H:%M}", "",
            "## Overnight", "",
            "_(Claude's note goes here; build/nightly.sh writes it after these numbers. If this line is still here, the Claude step was off or failed — the numbers below stand on their own.)_", "",
            "## Numbers", "", "- " + "\n- ".join(numbers), ""]
    body = list(lines)
    if new_scenes:
        body += ["## Scenes archived since the last run", ""] + [f"- `{Path(p).stem}`" for p in new_scenes] + [""]
    if books:
        body += ["## The book", ""]
        for slug, s, note in books:
            if s:
                body.append(f"- **{slug}**: {s['written']}/{s['total']} chapters written. Next: {s['action']} — {s['why']}")
                if s["action"] == "blocked":
                    body.append(f"  - nothing more is written until you answer: `python build/book_next.py --approve {s['chapter']}` or `--reject {s['chapter']} --note \"...\"` (book/{slug}/ch{s['chapter']:02d}/GATE.md)")
            else:
                body.append(f"- **{slug}**: {note}")
        body.append("")
    body += ["## New findings since last night", ""]
    body += [f"- [{f['check']}] {f['file']}: {f['text'][:200]}" for f in new[:60]] or ["- none"]
    if len(new) > 60:
        body.append(f"- ... and {len(new) - 60} more (reports/reconcile.md)")
    body += ["", "## Cleared since last night", ""]
    body += [f"- [{f['check']}] {f['file']}: {f['text'][:200]}" for f in cleared[:60]] or ["- none"]
    body += ["", f"## Still open: {still} (see reports/reconcile.md)", ""]
    body += ["## The sync (last 26 h) and the weekly backup", "",
             f"- sync: {pushed} push(es), {quiet} quiet run(s), {len(failed)} push failure(s)" + (": " + failed[-1][21:] if failed else ""),
             "- backup: " + backup_line,
             f"- last run of this digest: {last_run or 'never'}", ""]
    REPORTS.mkdir(exist_ok=True)
    DIGEST.write_text("\n".join(head + body), encoding="utf-8", newline="\n")
    print(f"nightly: {'; '.join(numbers)}; {len(new_scenes)} new scene(s)")

    if not dry:
        for f in by_key.values():
            f.setdefault("first_seen", seen.get(f["key"], {}).get("first_seen", now.date().isoformat()))
        STATE.write_text(json.dumps({"run": now.isoformat(timespec="seconds"), "findings": by_key}, ensure_ascii=False, indent=0), encoding="utf-8")
    return 0 if validate == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
