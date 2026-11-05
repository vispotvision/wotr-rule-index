#!/bin/bash
# Count words in every .md/.txt under the given directories and report today's
# delta against a baseline snapshot taken the first time the counter runs each day.
# Snapshots live in ~/.local/state/quill/<date>.json and are never pruned: the
# words written on day D are the next snapshot's total minus D's, so the whole
# history comes free from the snapshot totals.
#   words.sh <dir> [<dir>...]   → JSON {total, today, files:[{path, delta, words}], date, history:{date: words}}
python3 - "$@" <<'PY'
import json, os, sys, time, re, glob
home = os.path.expanduser("~")
dirs = [os.path.expanduser(d) for d in sys.argv[1:]]
state_dir = os.path.join(os.environ.get("XDG_STATE_HOME", home + "/.local/state"), "quill")
os.makedirs(state_dir, exist_ok=True)
today = time.strftime("%Y-%m-%d")
baseline_path = os.path.join(state_dir, today + ".json")

word_re = re.compile(r"[\w'’-]+", re.UNICODE)
counts = {}
for d in dirs:
    if not os.path.isdir(d):
        continue
    for root, subdirs, files in os.walk(d):
        subdirs[:] = [s for s in subdirs if not s.startswith(".") and s not in ("node_modules", "__pycache__")]
        for f in files:
            if not f.lower().endswith((".md", ".txt", ".markdown")):
                continue
            p = os.path.join(root, f)
            try:
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    counts[p] = len(word_re.findall(fh.read()))
            except OSError:
                pass

total = sum(counts.values())
if os.path.exists(baseline_path):
    try:
        baseline = json.load(open(baseline_path))
    except Exception:
        baseline = {"total": total, "files": counts}
else:
    baseline = {"total": total, "files": counts}
    json.dump(baseline, open(baseline_path, "w"))

bfiles = baseline.get("files", {})
changed = []
for p, n in counts.items():
    delta = n - bfiles.get(p, 0)
    if delta != 0:
        changed.append({"path": p, "name": os.path.relpath(p, home), "delta": delta, "words": n})
# files deleted today count as negative
for p, n in bfiles.items():
    if p not in counts:
        changed.append({"path": p, "name": os.path.relpath(p, home), "delta": -n, "words": 0})
changed.sort(key=lambda c: -abs(c["delta"]))

# Words per day, from the snapshot totals. A day the counter never ran (PC off)
# has no snapshot and is absent here.
# ponytail: words written across a snapshot gap land on the last day before it
snaps = {}
for f in os.listdir(state_dir):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", f):
        try:
            snaps[f[:-5]] = int(json.load(open(os.path.join(state_dir, f)))["total"])
        except Exception:
            pass
snaps[today] = baseline.get("total", total)
dates = sorted(snaps)
history = {a: snaps[b] - snaps[a] for a, b in zip(dates, dates[1:])}
history[today] = total - snaps[today]

print(json.dumps({
    "date": today,
    "total": total,
    "today": total - baseline.get("total", total),
    "files": changed[:12],
    "tracked": len(counts),
    "history": history,
}))
PY
