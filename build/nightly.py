#!/usr/bin/env python3
"""The nightly checks, with a diff digest: reports/nightly.md.

  python build/nightly.py            # run everything, write the digest, save the state
  python build/nightly.py --dry-run  # write the digest, do not touch the state

Runs validate, resolve, the three archive audits and the Büri sweep; hashes every
finding by (file, check, text) against build/.nightly_state.json so the digest says
what is NEW since last night, what CLEARED, and only counts what is still open
(prose_pass carries a standing pile from pre-rule scenes). Adds the scenes archived
since the last run (each is a `/judger <slug>` for the morning), the Judger queue,
and the sync and backup logs. Nothing here edits canon; the audits write only under
reports/. build/nightly.ps1 runs this at 03:30, lets Claude write the "Overnight"
note at the top, and commits the digest. session_start shows the note.
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

    # 2. the audits (each writes reports/<kind>.md) and the sweep
    import audit as A
    findings: list[dict] = []
    for fn, check, want in ((A.prose_pass, "prose", "- FAIL "), (A.reconcile, "reconcile", "- ")):
        try:
            path = fn()
            findings += _findings_from_report(path, check, want)
        except Exception as e:  # noqa: BLE001
            lines += [f"## {check} audit failed", "", f"    {e}", ""]
    try:
        A.recurrence()
    except Exception as e:  # noqa: BLE001
        lines += ["## recurrence audit failed", "", f"    {e}", ""]
    try:
        import mcp_server as M
        sweep = M.stale_names("all", max_files=200)
        # "scenes/x.md  (100)" then an indented line of "Büri×34 [Moto], ..." — one finding per term per file
        cur = ""
        for ln in sweep.splitlines():
            mm = re.match(r"^(\S+\.md)\s+\((\d+)\)\s*$", ln)
            if mm:
                cur = mm.group(1)
                continue
            if cur and ln.startswith("  ") and "×" in ln and not ln.lstrip().startswith(">"):
                for term in re.findall(r"([^,\[\]]+?)×\d+ \[", ln):
                    t = term.strip()
                    findings.append({"file": cur, "check": "stale", "text": t, "key": _key(cur, "stale", t)})
                cur = ""
        sweep_head = sweep.splitlines()[0] if sweep else ""
    except Exception as e:  # noqa: BLE001
        sweep_head = f"stale_names failed: {e}"

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

    # 5. the Judger queue
    queue = []
    for q in sorted((ROOT / "bot" / "queue").glob("*.judger.json")):
        try:
            j = json.loads(q.read_text(encoding="utf-8"))
            done = {a["id"] for a in j.get("applied", [])}
            waiting = [p for p in j.get("proposals", []) if p["id"] not in done]
            if waiting:
                queue.append((j.get("scene", q.stem), len(waiting)))
        except Exception:  # noqa: BLE001
            queue.append((q.stem, -1))

    # 6. the sync and the backup
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
    failed = [ln for ln in sync if "failed" in ln.lower()]
    quiet = sum(1 for ln in sync if "no wiki changes" in ln)
    backup = tail_log("backup.log", hours=24 * 8)

    # 7. the digest
    head = [f"# Nightly — {now:%Y-%m-%d %H:%M}", "",
            "## Overnight", "",
            "_(Claude's note goes here; build/nightly.ps1 writes it after these numbers. If this line is still here, the Claude step was off or failed — the numbers below stand on their own.)_", "",
            "## Numbers", "", "- " + "\n- ".join(numbers), ""]
    body = list(lines)
    if new_scenes:
        body += ["## Scenes archived since the last run", ""] + [f"- `{Path(p).stem}` — run `/judger {Path(p).stem}` for the close" for p in new_scenes] + [""]
    if queue:
        body += ["## Judger queue (proposals awaiting Isaac)", ""] + [f"- {s}: {n} waiting — `/judger apply {s} ...`" for s, n in queue] + [""]
    body += ["## New findings since last night", ""]
    body += [f"- [{f['check']}] {f['file']}: {f['text'][:200]}" for f in new[:60]] or ["- none"]
    if len(new) > 60:
        body.append(f"- ... and {len(new) - 60} more (reports/prose_pass.md, reports/reconcile.md)")
    body += ["", "## Cleared since last night", ""]
    body += [f"- [{f['check']}] {f['file']}: {f['text'][:200]}" for f in cleared[:60]] or ["- none"]
    body += ["", f"## Still open: {still} (see reports/prose_pass.md, reports/reconcile.md; {sweep_head})", ""]
    body += ["## The sync and the backup (last 26 h)", "",
             f"- sync: {pushed} push(es), {quiet} quiet run(s), {len(failed)} failure line(s)" + (": " + failed[-1][20:] if failed else ""),
             "- backup: " + (backup[-1][20:] if backup else "no run in the last eight days"),
             f"- last run of this digest: {last_run or 'never'}", ""]
    REPORTS.mkdir(exist_ok=True)
    DIGEST.write_text("\n".join(head + body), encoding="utf-8", newline="\n")
    print(f"nightly: {'; '.join(numbers)}; {len(new_scenes)} new scene(s); queue {sum(n for _, n in queue)}")

    if not dry:
        for f in by_key.values():
            f.setdefault("first_seen", seen.get(f["key"], {}).get("first_seen", now.date().isoformat()))
        STATE.write_text(json.dumps({"run": now.isoformat(timespec="seconds"), "findings": by_key}, ensure_ascii=False, indent=0), encoding="utf-8")
    return 0 if validate == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
