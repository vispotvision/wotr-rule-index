"""Supertonic 3 (Supertone) as a third narration engine beside Kokoro and Chatterbox.

Used by build/audio_export.py for any speaker whose build/voices.yaml entry says
`engine: supertonic`. Where it sits: the fast, stable tier. It is ONNX on the CPU
(no torch, no ROCm — nothing to fight on the 9070 XT), about 4x real time at
steps=10, 44.1 kHz out, reads back clean (0 % word errors on the audition lines),
and performs three cues written in the line — [laugh] [sigh] [breath] — which a
Kokoro speaker cannot. What it cannot do: a custom voice. The open weights ship ten
fixed presets (M1–M5, F1–F5) and Supertone's Voice Builder, the only official way to
make a style JSON from a clip, closed on 31 Aug 2026; the whole project was archived
on 9 Sep 2026. So: narration and the wider cast from the presets; the leads whose
voices are cast from the card (Darius, Gimbzo …) stay on a cloning engine.

    narrator-fast:
      engine: supertonic
      voice: M2           # M1–M5, F1–F5
      steps: 10           # 5 (rough, fastest) … 12 (best); 8 default
      speed: 0.95         # native, 0.7–2.0 — no resampling needed
    Rubric-st:
      engine: supertonic
      style: build/voices/styles/rubric.json    # any Supertonic voice-style JSON

Runs in its own interpreter, C:\\venvs\\wotr-supertonic, through
build/supertonic_worker.py. Setup: build/supertonic_setup.ps1 (pip install supertonic;
~400 MB of weights on first use). Model licence OpenRAIL-M, code MIT.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
VENV_PY = Path(r"C:\venvs\wotr-supertonic") / "Scripts" / "python.exe"
WORKER = ROOT / "build" / "supertonic_worker.py"
WORKER_LOG = ROOT / "build" / ".supertonic_worker.log"
TARGET_SR = 24000
_proc: subprocess.Popen | None = None

# cast-file cues Supertonic 3 performs; every other [cue] is stripped before synthesis
_CUE_TAGS = {"laugh": "<laugh>", "sigh": "<sigh>", "breath": "<breath>"}


def cues_to_tags(text: str) -> str:
    def swap(m):
        return _CUE_TAGS.get(m.group(1).strip().lower(), "")
    return re.sub(r"\s*\[([^\]]*)\]\s*", lambda m: f" {swap(m)} " if swap(m) else " ", text).strip()


def _worker() -> subprocess.Popen:
    global _proc
    if _proc is None or _proc.poll() is not None:
        if not VENV_PY.exists():
            sys.exit("Supertonic is not set up: run build/supertonic_setup.ps1")
        log = open(WORKER_LOG, "a", encoding="utf-8")
        log.write(f"\n=== worker start {VENV_PY}\n"); log.flush()
        _proc = subprocess.Popen([str(VENV_PY), str(WORKER)], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=log, text=True, encoding="utf-8", bufsize=1)
    return _proc


def _resample(x: np.ndarray, sr: int) -> np.ndarray:
    if sr == TARGET_SR:
        return x
    n = int(len(x) * TARGET_SR / sr)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def synth(cast, sp, text: str, speed: float) -> np.ndarray:
    style = ""
    if sp.ref:
        p = Path(sp.ref) if Path(sp.ref).is_absolute() else ROOT / sp.ref
        if not p.exists():
            sys.exit(f"{sp.name}: voice-style JSON not found: {p}")
        style = str(p)
    w = _worker()
    w.stdin.write(json.dumps({"text": cues_to_tags(text), "voice": sp.style or "M1", "style": style,
                              "steps": int(getattr(sp, "steps", 8)), "speed": float(speed)}) + "\n")
    w.stdin.flush()
    while True:
        line = w.stdout.readline()
        if not line:
            tail = WORKER_LOG.read_text(encoding="utf-8", errors="replace")[-1500:] if WORKER_LOG.exists() else ""
            sys.exit(f"the Supertonic worker died (exit {w.poll()}); the end of its log, {WORKER_LOG.name}:\n{tail}")
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "loaded" in msg:
            print(f"  {msg['loaded']}", flush=True)
            continue
        if "error" in msg:
            sys.exit(f"supertonic: {msg['error']}\n  " + "\n  ".join(msg.get("where", [])))
        x = np.load(msg["path"]).astype(np.float32)
        Path(msg["path"]).unlink(missing_ok=True)
        return _resample(x, int(msg["sr"]))
