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
actor. A clip of a real person you did not get permission from is for personal
audiobooks and stories only — never published, never on a shared link or the
wiki (Isaac's rule).

The model runs in its own interpreter (its pinned PyTorch stack stays out of
the MCP server's), through build/chatterbox_worker.py. Two venvs under
WOTR_VENVS (common.venv_python; was C:\\venvs and build/.venv-chatterbox):
wotr-cb-gpu carries AMD's ROCm torch for the RX 9070 XT (no CUDA) and is
preferred when it exists; wotr-cb is the CPU copy, several times slower than
Kokoro — use it for the voices that matter and leave narration to Kokoro.
Weights (~1 GB) come from the Hugging Face hub on first use. Setup:
build/chatterbox_gpu_setup.sh (the card) or build/chatterbox_setup.sh (CPU).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, venv_python  # noqa: E402

VENV_GPU = venv_python("cb-gpu")   # AMD ROCm torch (build/chatterbox_gpu_setup.sh)
VENV_CPU = venv_python("cb")       # CPU torch (build/chatterbox_setup.sh; was build/.venv-chatterbox)
VENV_PY = VENV_GPU if VENV_GPU.exists() else VENV_CPU
WORKER = ROOT / "build" / "chatterbox_worker.py"
WORKER_LOG = ROOT / "build" / ".chatterbox_worker.log"   # the worker's stderr: model chatter, and the reason if it dies
TARGET_SR = 24000
_proc: subprocess.Popen | None = None


def _worker() -> subprocess.Popen:
    global _proc
    if _proc is None or _proc.poll() is not None:
        if not VENV_PY.exists():
            sys.exit("Chatterbox is not set up: run build/chatterbox_setup.sh (CPU) or build/chatterbox_gpu_setup.sh (the 9070 XT)")
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


def _speed(x: np.ndarray, factor: float) -> np.ndarray:
    """Chatterbox has no pace control; a small stretch is done by resampling, which also
    shifts pitch a little, so only factors within about ±15% are applied."""
    if abs(factor - 1.0) < 0.02:
        return x
    factor = min(max(factor, 0.85), 1.15)
    n = int(len(x) / factor)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


MAX_CHARS = 280          # Chatterbox is happiest on a sentence or two; longer inputs garble or truncate
_SENT = re.compile(r"(?<=[.!?…])\s+(?=[\"“'A-Z\[])")


def chunks(text: str) -> list[str]:
    """Sentences grouped up to MAX_CHARS; a single over-long sentence is split at a comma or semicolon."""
    out, cur = [], ""
    for s in _SENT.split(text.strip()):
        if len(s) > MAX_CHARS:
            parts = re.split(r"(?<=[,;])\s+", s)
        else:
            parts = [s]
        for p in parts:
            if cur and len(cur) + 1 + len(p) > MAX_CHARS:
                out.append(cur)
                cur = p
            else:
                cur = f"{cur} {p}".strip()
    if cur:
        out.append(cur)
    return out


def synth(cast, sp, text: str, speed: float) -> np.ndarray:
    ref = ""
    if sp.ref:
        p = Path(sp.ref) if Path(sp.ref).is_absolute() else ROOT / sp.ref
        if not p.exists():
            sys.exit(f"{sp.name}: reference clip not found: {p}")
        ref = str(p)
    pieces = [_one(sp, c, ref) for c in chunks(text)]
    gap = np.zeros(int(TARGET_SR * 0.18), dtype=np.float32)
    joined = pieces[0] if len(pieces) == 1 else np.concatenate([x for piece in pieces for x in (piece, gap)][:-1])
    return _speed(joined, speed)


def _one(sp, text: str, ref: str) -> np.ndarray:
    w = _worker()
    w.stdin.write(json.dumps({"text": text, "model": sp.model, "ref": ref, "exaggeration": sp.exaggeration, "cfg": sp.cfg}) + "\n")
    w.stdin.flush()
    while True:
        line = w.stdout.readline()
        if not line:
            tail = WORKER_LOG.read_text(encoding="utf-8", errors="replace")[-1500:] if WORKER_LOG.exists() else ""
            sys.exit(f"the Chatterbox worker died (exit {w.poll()}); the end of its log, {WORKER_LOG.name}:\n{tail}")
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
        return _resample(x, int(msg["sr"]))
