"""Supertonic 3 in its own interpreter (C:\\venvs\\wotr-supertonic), driven over stdin/stdout.

Same line protocol as build/chatterbox_worker.py, so build/supertonic_backend.py is a near copy:

  one JSON object per line on stdin
      {"text": ..., "voice": "M1".."M5" | "F1".."F5", "style": "path to a voice-style JSON or empty",
       "steps": 8, "speed": 1.0}
  one JSON object per line on stdout
      {"path": "<npy file of float32 samples>", "sr": 44100}   or   {"error": "..."}
      ({"loaded": "supertonic-3 on CPU"} once, the first time)

Supertonic 3 (Supertone, model OpenRAIL-M, code MIT): 99M parameters, ONNX Runtime on
the CPU — no torch, no ROCm, ~4x real time on the 7800X3D at steps=10 — 44.1 kHz out,
ten preset voices, and it performs <laugh> <breath> <sigh> written in the text. The
project was archived by Supertone on 9 Sep 2026 (weights and code stay available under
the supertone-oss-archive namespace; the `supertonic` pip package still downloads them).

Setup: build/supertonic_setup.ps1. Run this file by hand to see load errors.
"""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

OUT = sys.stdout          # our JSON channel; anything the library prints goes to stderr instead
_tts = None


def say(obj) -> None:
    OUT.write(json.dumps(obj) + "\n")
    OUT.flush()


def load():
    global _tts
    if _tts is None:
        from supertonic import TTS
        _tts = TTS(auto_download=True)      # ~400 MB into ~/.cache/supertonic3 on first use
        say({"loaded": "supertonic-3 on CPU"})
    return _tts


def main() -> int:
    OUT.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout = sys.stderr
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            tts = load()
            if req.get("style"):
                style = tts.get_voice_style_from_path(req["style"])
            else:
                style = tts.get_voice_style(voice_name=str(req.get("voice", "M1")))
            speed = min(max(float(req.get("speed", 1.0)), 0.7), 2.0)
            wav, _dur = tts.synthesize(text=req["text"], voice_style=style, total_steps=int(req.get("steps", 8)),
                                       speed=speed, lang="en", max_chunk_length=300, silence_duration=0.25)
            x = np.asarray(wav, dtype=np.float32).squeeze()
            if x.ndim > 1:
                x = x.mean(axis=0) if x.shape[0] < x.shape[1] else x.mean(axis=1)
            out = Path(tempfile.gettempdir()) / f"wotr_st_{abs(hash(req['text'])) & 0xFFFFFFFF:08x}.npy"
            np.save(out, x)
            say({"path": str(out), "sr": int(getattr(tts, "sample_rate", 44100))})
        except Exception as e:  # noqa: BLE001 — report and keep serving
            import traceback
            tb = traceback.format_exc().strip().splitlines()
            say({"error": f"{type(e).__name__}: {e}", "where": tb[-6:-1]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
