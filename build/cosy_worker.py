"""Fun-CosyVoice 3 in its own interpreter (C:\\venvs\\wotr-cosy), driven over stdin/stdout.

The READER of the design-then-clone chain: Qwen VoiceDesign makes a voice once; this clones that
designed take (`ref` wav + its transcript) for every line, with an instruct per line for
emotion and pace, and CosyVoice's fine-grained tags in the text — [breath] [laughter]
<laughter>…</laughter> <strong>…</strong> [sigh] [cough], and ARPAbet hotfixes such as
[HH][AA1] to force how an invented name is said (cosyvoice/tokenizer/tokenizer.py).

Protocol — one JSON object per line on stdin:
    {"text": "...", "ref": "wav path", "ref_text": "what the ref says", "instruct": "" | "speak slowly and gravely",
     "spk": "optional cached speaker id", "speed": 1.0}
one JSON object per line on stdout:
    {"path": "<npy float32>", "sr": 24000}   or   {"error": "...", "where": [...]};  {"loaded": "..."} once.

Zero-shot (no instruct) uses inference_zero_shot with the reference transcript prefixed by the
CosyVoice 3 system prompt; an instruct uses inference_instruct2 ("You are a helpful assistant.
<instruct><|endofprompt|>"). Card caveats as elsewhere: discrete GPU by name, MIOpen off.
Setup: build/cosyvoice_setup.ps1.
"""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

SRC = Path(r"C:\venvs\wotr-cosy\src\CosyVoice")
MODEL_DIR = SRC / "pretrained_models" / "Fun-CosyVoice3-0.5B"
OUT = sys.stdout
_model = None
_spks: set[str] = set()


def say(obj) -> None:
    OUT.write(json.dumps(obj) + "\n")
    OUT.flush()


def _device_index() -> int:
    import torch
    for i in range(torch.cuda.device_count()):
        if "RX" in torch.cuda.get_device_name(i):
            return i
    return 0


def model():
    global _model
    if _model is None:
        import os, torch
        torch.backends.cudnn.enabled = False
        if torch.cuda.is_available():
            torch.cuda.set_device(_device_index())
        sys.path.insert(0, str(SRC))
        sys.path.insert(0, str(SRC / "third_party" / "Matcha-TTS"))
        os.chdir(SRC)
        # torchaudio 2.9+ routes load/save through torchcodec, which has no ROCm build on Windows; CosyVoice only
        # needs to read a wav, so give it soundfile instead (the same fix VoxCPM #203 uses)
        import torchaudio, soundfile as sf

        def _load(path, *a, **k):
            x, sr = sf.read(str(path), dtype="float32", always_2d=True)
            return torch.from_numpy(x.T.copy()), sr

        def _save(path, tensor, sr, *a, **k):
            sf.write(str(path), tensor.detach().cpu().numpy().T, sr)
        torchaudio.load, torchaudio.save = _load, _save
        from cosyvoice.cli.cosyvoice import AutoModel
        _model = AutoModel(model_dir=str(MODEL_DIR))
        label = f"cuda:{_device_index()} ({torch.cuda.get_device_name(_device_index())})" if torch.cuda.is_available() else "cpu"
        say({"loaded": f"Fun-CosyVoice3-0.5B on {label}, {_model.sample_rate} Hz"})
    return _model


def generate(req: dict) -> dict:
    import torch
    m = model()
    text = str(req["text"])
    ref, ref_text = str(req.get("ref", "")), str(req.get("ref_text", ""))
    instruct = str(req.get("instruct", "")).strip()
    speed = float(req.get("speed", 1.0))
    sys_prefix = "You are a helpful assistant."
    pieces = []
    if instruct:
        gen = m.inference_instruct2(text, f"{sys_prefix} {instruct}<|endofprompt|>", ref, stream=False, speed=speed)
    else:
        gen = m.inference_zero_shot(text, f"{sys_prefix}<|endofprompt|>{ref_text}", ref, stream=False, speed=speed)
    for j in gen:
        pieces.append(j["tts_speech"].squeeze().detach().cpu().numpy().astype(np.float32))
    x = np.concatenate(pieces) if pieces else np.zeros(1, dtype=np.float32)
    p = Path(tempfile.gettempdir()) / f"wotr_cosy_{abs(hash(text)) & 0xFFFFFFFF:08x}.npy"
    np.save(p, x)
    return {"path": str(p), "sr": int(m.sample_rate)}


def main() -> int:
    OUT.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout = sys.stderr
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            say(generate(json.loads(line)))
        except Exception as e:  # noqa: BLE001
            import traceback
            tb = traceback.format_exc().strip().splitlines()
            say({"error": f"{type(e).__name__}: {e}", "where": tb[-8:-1]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
