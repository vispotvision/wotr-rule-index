"""Qwen3-TTS VoiceDesign in its own interpreter, driven over stdin/stdout.

Two interpreters can run this file; build/qwen_backend.py prefers the first that exists:
  C:\\venvs\\wotr-qwen-fast   faster-qwen3-tts (MIT): static KV cache + CUDA graphs, which PyTorch
                            runs as HIP graphs on the 9070 XT — measured 2.4-2.8x real time per
                            line against 0.5x for the plain package (12 Sep 2026). One line per call.
  C:\\venvs\\wotr-qwen        the plain qwen-tts package (transformers 4.57); batch calls allowed.

Protocol — one JSON object per line on stdin:
    {"texts": ["line", ...], "instruct": "the brief", "anchor": "wav path or empty",
     "tries": 3, "good_enough": 0.6, "exempt": [false, ...], "seed": null,
     "temperature": 0.9, "top_k": 50, "subtalker_temperature": null}
one JSON object per line on stdout:
    {"paths": ["<npy float32>", ...], "sr": 24000, "cos": [0.61, ...], "tries": [2, ...]}
    or {"error": "...", "where": [...]};  {"loaded": "..."} once per model.

Why best-of-N: VoiceDesign has no identity slot — the brief names a region of voice-space and
every call draws a fresh member of it (build/voices/QWEN_DESIGN_GUIDE.md). So each line is
drawn up to `tries` times and scored against the anchor (the take Isaac approved) with an
ECAPA speaker embedding — cosine ~0.6+ reads as the same person, under 0.3 a stranger — and
the closest draw is kept; a draw at or above `good_enough` stops early. Lines marked exempt
(a whisper, a laugh-led line) take the first clean draw. Card caveats: the discrete GPU is
picked by name (ROCm lists the iGPU first); MIOpen is off (its conv kernels do not compile on
Windows gfx1201). Setup: build/qwen_tts_setup.ps1 (both venvs).
"""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

OUT = sys.stdout
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign"
_model = None
_fast = False
_ecapa = None
_anchor_cache: dict[str, np.ndarray] = {}
SR_EMB = 16000


def say(obj) -> None:
    OUT.write(json.dumps(obj) + "\n")
    OUT.flush()


def _device():
    import torch
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            if "RX" in torch.cuda.get_device_name(i):
                return f"cuda:{i}"
        return "cuda:0"
    return "cpu"


def model():
    global _model, _fast
    if _model is None:
        import torch
        torch.backends.cudnn.enabled = False
        dev = _device()
        label = dev if dev == "cpu" else f"{dev} ({torch.cuda.get_device_name(int(dev.split(':')[-1]))})"
        try:
            from faster_qwen3_tts import FasterQwen3TTS
            _model = FasterQwen3TTS.from_pretrained(MODEL_ID, device=dev, dtype=torch.bfloat16, attn_implementation="sdpa")
            _fast = True
            say({"loaded": f"qwen3-tts 1.7B VoiceDesign, HIP graphs, on {label}"})
        except ImportError:
            from qwen_tts import Qwen3TTSModel
            _model = Qwen3TTSModel.from_pretrained(MODEL_ID, device_map=dev, dtype=torch.bfloat16, attn_implementation="sdpa")
            say({"loaded": f"qwen3-tts 1.7B VoiceDesign on {label}"})
    return _model


def embed(x: np.ndarray, sr: int) -> np.ndarray:
    global _ecapa
    import torch, librosa
    if _ecapa is None:
        from speechbrain.inference.speaker import EncoderClassifier
        _ecapa = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", run_opts={"device": "cpu"})
        say({"loaded": "ECAPA speaker encoder (cpu)"})
    y = librosa.resample(x.astype(np.float32), orig_sr=sr, target_sr=SR_EMB) if sr != SR_EMB else x.astype(np.float32)
    with torch.no_grad():
        e = _ecapa.encode_batch(torch.from_numpy(y).unsqueeze(0)).squeeze().numpy()
    return e / (np.linalg.norm(e) + 1e-9)


_anchor_self: dict[str, float] = {}
_anchor_f0: dict[str, float] = {}
SHORT_S = 1.6           # under this length a speaker embedding is noise; a fragment is judged by pitch instead


def median_f0(x: np.ndarray, sr: int) -> float:
    import parselmouth
    snd = parselmouth.Sound(x.astype(np.float64), sampling_frequency=sr)
    f0 = snd.to_pitch(pitch_floor=50, pitch_ceiling=500).selected_array["frequency"]
    f0 = f0[f0 > 0]
    return float(np.median(f0)) if len(f0) else 0.0


def anchor_embedding(path: str) -> np.ndarray:
    """The anchor is a wav, or a folder of wavs (one per approved line): the mean of the line
    embeddings, so a draw is compared with the voice rather than with one performance. The
    folder's own line-to-line similarity is kept as the ceiling for `good_enough`."""
    if path not in _anchor_cache:
        import soundfile as sf, itertools
        p = Path(path)
        files = sorted(p.glob("*.wav")) if p.is_dir() else [p]
        es, f0s = [], []
        for f in files:
            x, sr = sf.read(str(f), dtype="float32")
            if x.ndim > 1:
                x = x.mean(axis=1)
            es.append(embed(x, sr))
            f0s.append(median_f0(x, sr))
        mean = np.mean(es, axis=0)
        _anchor_cache[path] = mean / (np.linalg.norm(mean) + 1e-9)
        pairs = [float(np.dot(a, b)) for a, b in itertools.combinations(es, 2)]
        _anchor_self[path] = float(np.mean(pairs)) if pairs else 1.0
        _anchor_f0[path] = float(np.median([f for f in f0s if f]) or 0.0)
        say({"loaded": f"anchor {p.name}: {len(files)} line(s), self-similarity {_anchor_self[path]:.2f}, pitch {_anchor_f0[path]:.0f} Hz"})
    return _anchor_cache[path]


def score(x: np.ndarray, sr: int, anchor: str, a_emb: np.ndarray) -> float:
    """Similarity of a draw to the anchor: speaker-embedding cosine, or for a fragment too short to
    embed, closeness of median pitch (1.0 = same pitch, 0.5 = 25 % off) — scaled to the same range."""
    if len(x) < sr * SHORT_S:
        af = _anchor_f0.get(anchor, 0.0)
        f = median_f0(x, sr)
        if not af or not f:
            return 0.5
        return max(0.0, 1.0 - 2.0 * abs(f - af) / af)
    return float(np.dot(a_emb, embed(x, sr)))


def _draw(text: str, instruct: str, kwargs: dict):
    """One line, one draw -> (float32 samples, sr)."""
    m = model()
    if _fast:
        wavs, sr = m.generate_voice_design(text=text, instruct=instruct, language="English", **kwargs)
    else:
        wavs, sr = m.generate_voice_design(text=text, instruct=instruct, language="English", **kwargs)
    return np.asarray(wavs[0], dtype=np.float32).squeeze(), int(sr)


def generate(req: dict) -> dict:
    import torch
    texts = [str(t) for t in req["texts"]]
    instruct = str(req.get("instruct", ""))
    anchor = req.get("anchor") or ""
    tries = max(1, int(req.get("tries", 1))) if anchor else 1
    good = float(req.get("good_enough", 0.6))
    exempt = list(req.get("exempt") or [False] * len(texts))
    kwargs = {k: req[k] for k in ("temperature", "top_k") if req.get(k) is not None}
    if not _fast:
        for k in ("top_p", "repetition_penalty", "subtalker_temperature", "subtalker_top_k"):
            if req.get(k) is not None:
                kwargs[k] = req[k]
    a_emb = anchor_embedding(anchor) if anchor else None
    if a_emb is not None:
        good = min(good, _anchor_self.get(anchor, 1.0))    # never demand more than the anchor's lines give each other
    paths, cos_out, tries_out, sr = [], [], [], 24000
    for i, text in enumerate(texts):
        best = None
        n = 1 if exempt[i] else tries
        for t in range(n):
            if req.get("seed") is not None:
                torch.manual_seed(int(req["seed"]) + 1000 * i + t)
            x, sr = _draw(text, instruct, kwargs)
            c = score(x, sr, anchor, a_emb) if a_emb is not None else 1.0
            if best is None or c > best[1]:
                best = (x, c, t + 1)
            if c >= good:
                break
        x, c, used = best
        p = Path(tempfile.gettempdir()) / f"wotr_qwen_{abs(hash(text)) & 0xFFFFFFFF:08x}_{i}.npy"
        np.save(p, x)
        paths.append(str(p)); cos_out.append(c); tries_out.append(used)
    return {"paths": paths, "sr": sr, "cos": cos_out, "tries": tries_out}


def main() -> int:
    OUT.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout = sys.stderr          # library chatter stays off the JSON channel
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            say(generate(json.loads(line)))
        except Exception as e:  # noqa: BLE001 — report and keep serving
            import traceback
            tb = traceback.format_exc().strip().splitlines()
            say({"error": f"{type(e).__name__}: {e}", "where": tb[-6:-1]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
