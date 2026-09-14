#!/usr/bin/env python3
"""The job runner: n8n orchestrates, this executes on the host.

  python build/jobs_server.py                 # 127.0.0.1:8799
  python build/jobs_server.py --port 8799 --log build/.jobs_server.log
  python build/jobs_server.py --bind 127.0.0.1 --bind 100.64.0.2   # a second address, same port

n8n cannot run anything on this machine — its container is Linux, holds no mount of
the repo, and has no Anthropic key to call Claude with. This closes that gap: a small
HTTP listener on the host that n8n (or a phone, or the bot) POSTs to, which runs one
of a FIXED LIST of named jobs — the nightly, the book dispatcher, the sync, the
backup, the checks. It takes a job name, never a command and never a
prompt: nothing here executes arbitrary text, so a mistake in a workflow cannot turn
into a shell.

Bound to 127.0.0.1 and nowhere else unless --bind says otherwise (repeatable: one
listener per address, all on the same port). n8n runs in Docker with network_mode:
host, so it reaches this at http://127.0.0.1:8799 like any other process on the
machine, and the LAN does not. The systemd user unit is wotr-jobs.service
(build/systemd_setup.sh installs it). Every request carries the shared secret from
build/.jobs_token (generated on first run; gitignored; never in chat) as
`X-Job-Token` or `?token=`.

  GET  /health                 what this is and which jobs exist
  POST /run/<job>              start one; JSON body may carry {"slug": "..."}
  GET  /status/<job_id>        state, exit code, the tail of its log
  GET  /jobs                   the last runs, newest first
  GET  /digest                 reports/nightly.md as markdown (for n8n to deliver)
  GET  /book                   build/book_next.py --json (where the book stands)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import subprocess
import sys
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[1]
JOBS_DIR = ROOT / "build" / ".jobs"
TOKEN_FILE = ROOT / "build" / ".jobs_token"
PY = sys.executable

# the whole allowlist. A job is a name and a fixed command; "slug" is the only
# argument any of them take, and it is checked against the books on disk.
JOBS: dict[str, dict] = {
    "nightly": {"cmd": ["bash", "build/nightly.sh"],
                "what": "the checks, the diff digest and the overnight note (~2 min)"},
    "book": {"cmd": ["bash", "build/book_dispatch.sh"],
             "what": "write the next chapter if one is due and no gate is waiting (an hour or more)",
             "slug_flag": "--slug"},
    "book_dry": {"cmd": ["bash", "build/book_dispatch.sh", "--dry-run"],
                 "what": "say what the book would do tonight; write nothing"},
    "sync": {"cmd": ["bash", "build/sync.sh"],
             "what": "the Notion mirror, the index, the Drive documents, commit and push"},
    "backup": {"cmd": ["bash", "build/backup.sh"],
               "what": "zip the canon and the True Canon folder (to Drive when mounted, else WOTR_BACKUP_DIR)"},
    "checks": {"cmd": [PY, "build/nightly.py"],
               "what": "the nightly numbers only, no Claude, no commit"},
}

_lock = threading.Lock()
_runs: dict[str, dict] = {}


def token() -> str:
    env = os.environ.get("WOTR_JOBS_TOKEN")
    if env:
        return env.strip()
    if not TOKEN_FILE.exists():
        # created 0600 in the same call, not through the umask (0022 under systemd), which
        # left the first Linux token world-readable; build/.mcp_token is written the same way
        fd = os.open(TOKEN_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(secrets.token_urlsafe(32))
        print(f"wrote a new shared secret to {TOKEN_FILE} (gitignored; paste it into n8n once)")
    elif TOKEN_FILE.stat().st_mode & 0o077:
        TOKEN_FILE.chmod(0o600)  # a token from before this check
    return TOKEN_FILE.read_text(encoding="utf-8").strip()


def start(job: str, slug: str = "") -> dict:
    spec = JOBS[job]
    with _lock:
        live = [r for r in _runs.values() if r["job"] == job and r["state"] == "running"]
        if live:
            return {"error": f"{job} is already running", "job_id": live[0]["job_id"]}
        jid = f"{job}-{datetime.now():%Y%m%d-%H%M%S}"
        JOBS_DIR.mkdir(parents=True, exist_ok=True)
        logp = JOBS_DIR / f"{jid}.log"
        cmd = list(spec["cmd"])
        if slug and spec.get("slug_flag"):
            cmd += [spec["slug_flag"], slug]
        f = logp.open("w", encoding="utf-8", buffering=1)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        p = subprocess.Popen(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT, env=env)
        rec = {"job_id": jid, "job": job, "slug": slug, "pid": p.pid, "state": "running",
               "started": datetime.now().isoformat(timespec="seconds"), "finished": None,
               "exit_code": None, "log": str(logp)}
        _runs[jid] = rec

    def wait() -> None:
        code = p.wait()
        f.close()
        with _lock:
            rec["state"] = "done" if code == 0 else "failed"
            rec["exit_code"] = code
            rec["finished"] = datetime.now().isoformat(timespec="seconds")

    threading.Thread(target=wait, daemon=True).start()
    return rec


def tail(rec: dict, n: int = 25) -> list[str]:
    p = Path(rec["log"])
    if not p.exists():
        return []
    return p.read_text(encoding="utf-8", errors="replace").splitlines()[-n:]


class Handler(BaseHTTPRequestHandler):
    server_version = "WOTRJobs/1.0"

    def log_message(self, fmt: str, *a) -> None:  # one line, not two
        # the request line is logged; a client using the ?token= form must not leave the secret in it
        line = re.sub(r"([?&]token=)[^&\s]*", r"\1<token>", fmt % a)
        print(f"{datetime.now():%H:%M:%S} {self.address_string()} {line}", flush=True)

    def _send(self, code: int, body, ctype: str = "application/json") -> None:
        raw = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False, indent=1).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if "json" in ctype or "text" in ctype else ""))
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _authed(self, q: dict) -> bool:
        given = self.headers.get("X-Job-Token") or (q.get("token", [""])[0])
        return secrets.compare_digest(given or "", token())

    def do_GET(self) -> None:  # noqa: N802
        u = urlparse(self.path)
        q = parse_qs(u.query)
        parts = [p for p in u.path.split("/") if p]
        if parts == ["health"]:
            return self._send(200, {"ok": True, "repo": str(ROOT), "auth": "X-Job-Token header or ?token=",
                                    "jobs": {k: v["what"] for k, v in JOBS.items()}})
        if not self._authed(q):
            return self._send(401, {"error": "bad or missing token"})
        if parts == ["jobs"]:
            with _lock:
                return self._send(200, {"runs": sorted(_runs.values(), key=lambda r: r["started"], reverse=True)[:20]})
        if len(parts) == 2 and parts[0] == "status":
            with _lock:
                rec = _runs.get(parts[1])
            if not rec:
                return self._send(404, {"error": "no such job_id"})
            return self._send(200, {**rec, "tail": tail(rec)})
        if parts == ["digest"]:
            p = ROOT / "reports" / "nightly.md"
            if not p.exists():
                return self._send(404, {"error": "no digest yet; run the nightly"})
            return self._send(200, p.read_bytes(), "text/markdown")
        if parts == ["book"]:
            out = subprocess.run([PY, "build/book_next.py", "--json"], cwd=ROOT, capture_output=True,
                                 text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            try:
                return self._send(200, json.loads(out.stdout.strip()))
            except Exception:
                return self._send(500, {"error": (out.stdout + out.stderr)[-500:]})
        return self._send(404, {"error": "unknown path", "try": ["/health", "/run/<job>", "/status/<id>", "/jobs", "/digest", "/book"]})

    def do_POST(self) -> None:  # noqa: N802
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._authed(q):
            return self._send(401, {"error": "bad or missing token"})
        parts = [p for p in u.path.split("/") if p]
        if len(parts) != 2 or parts[0] != "run":
            return self._send(404, {"error": "POST /run/<job>", "jobs": sorted(JOBS)})
        job = parts[1]
        if job not in JOBS:
            return self._send(400, {"error": f"unknown job '{job}'", "jobs": sorted(JOBS)})
        n = int(self.headers.get("Content-Length") or 0)
        body = {}
        if n:
            try:
                body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            except Exception:
                return self._send(400, {"error": "body must be JSON"})
        slug = str(body.get("slug", "") or q.get("slug", [""])[0])
        if slug and not (ROOT / "book" / slug / "outline.json").exists():
            return self._send(400, {"error": f"no book '{slug}' under book/"})
        rec = start(job, slug)
        return self._send(202 if "error" not in rec else 409, rec)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--bind", action="append", metavar="ADDR",
                    help="address to listen on; repeatable, one listener per address on --port (default 127.0.0.1)")
    ap.add_argument("--log", help="append stdout/stderr here (for wotr-jobs.service)")
    a = ap.parse_args()
    if a.log:
        f = open(a.log, "a", encoding="utf-8", buffering=1)
        sys.stdout = sys.stderr = f
    token()  # make sure the secret exists before anything can ask for it
    binds = a.bind or ["127.0.0.1"]
    # one server per address, all on the same port; every one but the last runs on its
    # own thread and the last one holds the main thread, so Ctrl-C and SIGTERM land as before
    servers = [ThreadingHTTPServer((b, a.port), Handler) for b in binds]
    print(f"job runner on {', '.join(f'{b}:{a.port}' for b in binds)} — {len(JOBS)} jobs: {', '.join(sorted(JOBS))}", flush=True)
    print("reachable from the n8n container (network_mode: host) as http://127.0.0.1:%d" % a.port, flush=True)
    for srv in servers[:-1]:
        threading.Thread(target=srv.serve_forever, daemon=True, name=f"listen-{srv.server_address[0]}").start()
    servers[-1].serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
