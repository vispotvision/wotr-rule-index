"""Chatterbox in its own interpreter (build/.venv-chatterbox), driven over stdin/stdout.

chatterbox-tts pins torch 2.6, transformers 5.2, gradio 6.8 and friends, which
do not belong in the interpreter that runs the MCP server and Kokoro, so it
lives in a venv and build/chatterbox_backend.py talks to this worker:

  one JSON object per line on stdin
      {"text": ..., "model": "turbo" | "standard", "ref": "path or empty",
       "exaggeration": 0.5, "cfg": 0.5}
  one JSON object per line on stdout
      {"path": "<npy file of float32 samples>", "sr": 24000}   or   {"error": "..."}
      ({"loaded": "<model> on <device>"} once per model, the first time it is used)

Two models, both from Resemble AI (MIT):
  turbo     ResembleAI/chatterbox-turbo — 350M, a one-step decoder, several times
            faster; reads paralinguistic cues written in the text: [laugh] [chuckle]
            [sigh] [gasp] [cough] [clear throat] [sniff] [groan]. No exaggeration knob.
  standard  ResembleAI/chatterbox — 500M; the exaggeration (0 flat … 0.7+ dramatic)
            and cfg (lower = looser, more emotional pacing) knobs. Slower.
Both design a voice from a reference clip (audio_prompt_path) or use a built-in one.

Setup: build/chatterbox_setup.ps1. Run this file by hand to see load errors.
"""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

_models: dict = {}
OUT = sys.stdout          # our JSON channel; libraries that print go to stderr instead


def say(obj) -> None:
    OUT.write(json.dumps(obj) + "\n")
    OUT.flush()


def _device():
    import torch
    if torch.cuda.is_available():
        return "cuda"
    try:
        import torch_directml
        return torch_directml.device()
    except ImportError:
        return "cpu"


def load(name: str):
    if name not in _models:
        device = _device()
        if name == "turbo":
            from chatterbox.tts_turbo import ChatterboxTurboTTS
            _models[name] = ChatterboxTurboTTS.from_pretrained(device=device)
        else:
            from chatterbox.tts import ChatterboxTTS
            _models[name] = ChatterboxTTS.from_pretrained(device=device)
        say({"loaded": f"{name} on {device}"})
    return _models[name]


def main() -> int:
    OUT.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout = sys.stderr      # anything the model libraries print stays off the JSON channel
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            name = "turbo" if str(req.get("model", "turbo")).lower() == "turbo" else "standard"
            model = load(name)
            kwargs = {}
            if name == "standard":
                kwargs = {"exaggeration": float(req.get("exaggeration", 0.5)), "cfg_weight": float(req.get("cfg", 0.5))}
            if req.get("ref"):
                kwargs["audio_prompt_path"] = req["ref"]
            wav = model.generate(req["text"], **kwargs)
            x = wav.squeeze().detach().cpu().numpy().astype(np.float32)
            out = Path(tempfile.gettempdir()) / f"wotr_cb_{abs(hash(req['text'])) & 0xFFFFFFFF:08x}.npy"
            np.save(out, x)
            say({"path": str(out), "sr": int(model.sr)})
        except Exception as e:  # noqa: BLE001 — report and keep serving
            import traceback
            tb = traceback.format_exc().strip().splitlines()
            say({"error": f"{type(e).__name__}: {e}", "where": tb[-6:-1]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
