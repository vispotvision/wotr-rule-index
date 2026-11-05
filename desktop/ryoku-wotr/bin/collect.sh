#!/bin/bash
# Gather everything the WOTR panel shows into one JSON blob on stdout.
# Cheap enough to run every minute: git, systemctl, and a scan of out/rules.resolved.json.
repo="${1:-$HOME/wotr-rule-index}"
repo="${repo/#\~/$HOME}"
cd "$repo" 2>/dev/null || { echo "{\"error\":\"repo not found: $repo\"}"; exit 0; }

python3 - "$repo" <<'PY'
import json, os, re, subprocess, sys, time, collections
repo = sys.argv[1]
out = {"repo": repo, "error": ""}

def run(*cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=8).stdout
    except Exception:
        return ""

def read(path):
    try:
        with open(os.path.join(repo, path), encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""

# --- rules / docket / conflicts / rulings
try:
    rules = json.load(open(os.path.join(repo, "out/rules.resolved.json")))
    c = collections.Counter(r.get("status") for r in rules)
    out["rules"] = {"live": c.get("live", 0), "superseded": c.get("superseded", 0), "total": len(rules)}
except Exception:
    out["rules"] = {"live": 0, "superseded": 0, "total": 0}
m = re.search(r"(\d+)\s+outstanding", read("out/docket.md"))
out["docket"] = int(m.group(1)) if m else 0
conflicts = read("CONFLICTS.md")
out["conflicts"] = {"total": len(re.findall(r"^## C-", conflicts, re.M)),
                    "open": len(re.findall(r"\*\*Status:\*\*\s*open", conflicts))}
out["rulings"] = len(re.findall(r"^## ", read("RULINGS.md"), re.M))

# --- scenes
m = re.search(r"(\d+) files, (\d+) words", read("scenes/MANIFEST.md"))
out["scenes"] = {"count": int(m.group(1)), "words": int(m.group(2))} if m else {"count": 0, "words": 0}

# --- CONTINUE.md: newest dated block headline
m = re.search(r"^## State on (\d{4}-\d\d-\d\d),?\s*(.*)$", read("CONTINUE.md"), re.M)
out["continue"] = {"date": m.group(1) if m else "", "headline": (m.group(2).strip(" ()") if m else "")}

# --- git
last = run("git", "log", "-1", "--format=%h%x1f%s%x1f%cr").strip().split("\x1f")
out["git"] = {
    "branch": run("git", "rev-parse", "--abbrev-ref", "HEAD").strip(),
    "hash": last[0] if len(last) == 3 else "", "subject": last[1] if len(last) == 3 else "",
    "when": last[2] if len(last) == 3 else "",
    "dirty": len([l for l in run("git", "status", "--porcelain").splitlines() if l.strip()]),
}

# --- systemd user units
daemons = []
WOTR_UNITS = (("wotr-mcp-public", "Public MCP"), ("wotr-bot", "Discord bot"), ("wotr-workshop", "Workshop"), ("wotr-jobs", "Job runner"))
for unit, label in WOTR_UNITS:
    state = run("systemctl", "--user", "is-active", unit + ".service").strip() or "unknown"
    # switched off on purpose is not a fault: leave it out rather than raise the bar's alarm
    if state != "active" and run("systemctl", "--user", "is-enabled", unit + ".service").strip() in ("disabled", "not-found", ""):
        continue
    daemons.append({"unit": unit, "label": label, "state": state})
# The private MCP has no unit: each Claude session or Desktop window starts its own over stdio.
# Rust is rust/target/release/wotr-mcp --ops; python is what claude_desktop_config.json still launches.
procs = [p.split(None, 1) for p in run("pgrep", "-af", "wotr-mcp --ops|build/mcp_server.py").splitlines()]
cmds = [c[1] for c in procs if len(c) > 1 and "pgrep" not in c[1] and "disclaimer" not in c[1] and "collect.sh" not in c[1]]
rust_n = sum("wotr-mcp" in c for c in cmds)
py_n = sum("mcp_server.py" in c for c in cmds)
daemons.insert(1, {"unit": "", "label": "Private MCP", "state": "active" if rust_n + py_n else "inactive",
                   "detail": f"{rust_n} Rust session{'' if rust_n == 1 else 's'}" + (f" · {py_n} old Python" if py_n else "") if rust_n + py_n else "no local session open"})
out["daemons"] = daemons

# --- the few other services that matter. A short fixed list: one that is down shows red rather than
# disappearing, which a list of what is running could never do. VPNs have their own bar plugin.
IMPORTANT = (("tailscaled", "Tailscale", "system"), ("ollama", "Ollama", "system"), ("omniroute", "OmniRoute", "user"),
             ("agent-loom", "Agent Loom", "user"), ("jellyfin", "Jellyfin", "system"))
services = []
for unit, label, scope in IMPORTANT:
    flag = ["--user"] if scope == "user" else []
    if "LoadState=loaded" not in run("systemctl", *flag, "show", unit + ".service", "-p", "LoadState"):
        continue
    state = run("systemctl", *flag, "is-active", unit + ".service").strip() or "unknown"
    # a system unit needs root, so only user services get the one-click restart
    services.append({"unit": unit, "label": label, "state": state, "restart": scope == "user"})
out["services"] = services

# --- running docker containers
containers = []
for line in run("docker", "ps", "--format", "{{.Names}}|{{.Status}}|{{.Image}}").splitlines():
    bits = line.split("|")
    if len(bits) == 3:
        containers.append({"name": bits[0], "status": bits[1], "image": bits[2].split("/")[-1], "healthy": "unhealthy" not in bits[1]})
out["containers"] = containers

timers = []
try:
    now = time.time()
    for t in json.loads(run("systemctl", "--user", "list-timers", "wotr-*", "--output=json") or "[]"):
        nxt = t.get("next", 0) / 1e6
        left = max(0, nxt - now)
        if left < 3600: left_s = f"in {int(left // 60)} min"
        elif left < 86400: left_s = f"in {left / 3600:.0f} h"
        else: left_s = f"in {left / 86400:.0f} d"
        timers.append({"unit": t["unit"].replace(".timer", ""),
                       "label": t["unit"].replace("wotr-", "").replace(".timer", ""),
                       "next": time.strftime("%a %H:%M", time.localtime(nxt)) if nxt else "",
                       "left": left_s if nxt else "",
                       "running": run("systemctl", "--user", "is-active", t["activates"]).strip() == "active"})
except Exception:
    pass
out["timers"] = timers
out["generated"] = time.strftime("%H:%M")
print(json.dumps(out))
PY
