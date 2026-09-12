"""Chatterbox (Resemble AI, MIT) as a second narration engine beside Kokoro.

Used by build/audio_export.py for any speaker whose build/voices.yaml entry says
`engine: chatterbox`. What it adds over Kokoro: a voice designed from a short
reference clip (`ref: build/voices/<name>.wav`, 6–15 s of clean speech; with no
`ref` it speaks in its own built-in voice) and delivery. Two models:

  model: turbo      (default) Chatterbox Turbo — faster, and it performs cues
                    written into the line: [laugh] [chuckle] [sigh] [gasp]
                    [cough] [clear throat] [sniff] [groan]. In a cast file those
                    go inside the speaker's span like any word; Kokoro speakers
                    have them stripped.
  model: standard   the original — an `exaggeration` knob (0 flat, 0.5 natural,
                    0.7+ dramatic) and `cfg` (lower = looser, more emotional
                    pacing); slower.

    Verinus:
      engine: chatterbox
      model: turbo
      ref: build/voices/verinus.wav
      speed: 1.0
    Aurelian:
      engine: chatterbox
      model: standard
      exaggeration: 0.65
      cfg: 0.35

Reference clips: your own recordings, a voice you designed, or a consenting
actor. A clip of a real person you did not get permission from is personal-use
only — never for the Drive audiobook or a shared link (Isaac's rule).

The model runs in its own interpreter, build/.venv-chatterbox (its pinned
PyTorch stack stays out of the MCP server's), through build/chatterbox_worker.py.
On this PC that is the CPU unless a ROCm or DirectML torch is installed in that
venv (the RX 9070 XT has no CUDA), so it is several times slower than Kokoro —
use it for the voices that matter and leave narration to Kokoro. Weights
(~1 GB) come from the Hugging Face hub on first use. Setup: build/chatterbox_setup.ps1.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
VENV_PY = ROOT / "build" / ".venv-chatterbox" / "Scripts" / "python.exe"
WORKER = ROOT / "build" / "chatterbox_worker.py"
TARGET_SR = 24000
_proc: subprocess.Popen | None = None


def _worker() -> subprocess.Popen:
    global _proc
    if _proc is None or _proc.poll() is not None:
        if not VENV_PY.exists():
            sys.exit("Chatterbox is not set up: run build/chatterbox_setup.ps1 (creates build/.venv-chatterbox)")
        _proc = subprocess.Popen([str(VENV_PY), str(WORKER)], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1)
    return _proc


def _resample(x: np.ndarray, sr: int) -> np.ndarray:
    if sr == TARGET_SR:
        return x
    n = int(len(x) * TARGET_SR / sr)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def _speed(x: np.ndarray, factor: float) -> np.ndarray:
    """Chatterbox has no pace control; a small stretch is done by resampling, which also
    shifts pitch a little, so only factors within about ±15% are applied."""
    if abs(factor - 1.0) < 0.02:
        return x
    factor = min(max(factor, 0.85), 1.15)
    n = int(len(x) / factor)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def synth(cast, sp, text: str, speed: float) -> np.ndarray:
    ref = ""
    if sp.ref:
        p = Path(sp.ref) if Path(sp.ref).is_absolute() else ROOT / sp.ref
        if not p.exists():
            sys.exit(f"{sp.name}: reference clip not found: {p}")
        ref = str(p)
    w = _worker()
    w.stdin.write(json.dumps({"text": text, "model": sp.model, "ref": ref, "exaggeration": sp.exaggeration, "cfg": sp.cfg}) + "\n")
    w.stdin.flush()
    while True:
        line = w.stdout.readline()
        if not line:
            sys.exit("the Chatterbox worker died; run build/.venv-chatterbox/Scripts/python.exe build/chatterbox_worker.py by hand to see why")
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue            # a library printed on stdout before the worker redirected it
        if "loaded" in msg:
            print(f"  chatterbox loaded on {msg['loaded']}", flush=True)
            continue
        if "error" in msg:
            sys.exit(f"chatterbox: {msg['error']}\n  " + "\n  ".join(msg.get("where", [])))
        x = np.load(msg["path"]).astype(np.float32)
        Path(msg["path"]).unlink(missing_ok=True)
        return _speed(_resample(x, int(msg["sr"])), speed)
