"""ElevenLabs as a narration engine for build/audio_export.py.

    voices.yaml:
      _elevenlabs:                       # used when the render is asked for engine elevenlabs
        _default: JBFqnCBsd6RMkjVDRZzb   # George — every speaker without a line below
        _model: eleven_multilingual_v2
        Darius: <voice_id>               # a speaker's ElevenLabs voice (id, or a name from the workspace)
      Sodoku Moto:
        engine: elevenlabs               # or: a speaker pinned to ElevenLabs in every render
        voice_id: <voice_id>
        stability: 0.5  similarity: 0.75  style: 0.0  speed: 1.0

The key is ELEVENLABS_API_KEY (a user environment variable; never in a file in the repo).
Output is PCM at the narrator's 24 kHz so it splices with the local engines. Every call
costs characters on the ElevenLabs plan; `chars()` says how many a text will cost.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

import numpy as np

API = "https://api.elevenlabs.io/v1"
SAMPLE_RATE = 24000
DEFAULT_MODEL = "eleven_multilingual_v2"
CHUNK = 4500  # characters per request; the API caps a request at 5,000 for multilingual_v2


def api_key() -> str:
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not k and sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg:
                k = str(winreg.QueryValueEx(reg, "ELEVENLABS_API_KEY")[0]).strip()
        except OSError:
            pass
    if not k:
        sys.exit("ELEVENLABS_API_KEY is not set (user environment variable); the ElevenLabs engine cannot run.")
    return k


def _call(method: str, path: str, body: dict | None = None, raw: bool = False, tries: int = 4):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"xi-api-key": api_key(), "Content-Type": "application/json", "Accept": "*/*"})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read() if raw else json.load(r)
        except urllib.error.HTTPError as e:
            detail = e.read()[:300].decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503) and attempt < tries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"ElevenLabs {method} {path} -> {e.code}: {detail}") from None


def list_voices() -> list[dict]:
    """[{voice_id, name, category}] for the workspace, so a name in voices.yaml can be resolved."""
    out = []
    for v in _call("GET", "/voices").get("voices", []):
        out.append({"voice_id": v["voice_id"], "name": v.get("name", ""), "category": v.get("category", "")})
    return out


_NAMES: dict[str, str] | None = None


def resolve_voice(spec: str) -> str:
    """A voice id passes through; a name (or the start of one, case-insensitive) is looked up once."""
    global _NAMES
    spec = str(spec).strip()
    if len(spec) == 20 and spec.isalnum():
        return spec
    if _NAMES is None:
        _NAMES = {v["name"].lower(): v["voice_id"] for v in list_voices()}
    key = spec.lower()
    for name, vid in _NAMES.items():
        if name == key or name.startswith(key) or name.split(" - ")[0].strip() == key:
            return vid
    sys.exit(f"ElevenLabs: no voice named {spec!r} in the workspace ({len(_NAMES)} voices; build/audio_export.py --list-eleven)")


def chars(text: str) -> int:
    return len(text)


def _split(text: str) -> list[str]:
    """Long spans are split on sentence ends so no request exceeds the API's size cap."""
    if len(text) <= CHUNK:
        return [text]
    parts, cur = [], ""
    for sent in text.replace("\n", " ").split(". "):
        piece = sent if sent.endswith(".") else sent + "."
        if len(cur) + len(piece) + 1 > CHUNK and cur:
            parts.append(cur.strip())
            cur = ""
        cur += " " + piece
    if cur.strip():
        parts.append(cur.strip())
    return parts


def synth(cast, sp, text: str, speed: float) -> np.ndarray:
    """Text -> float32 samples at 24 kHz for one speaker. `sp` carries voice_id, model_id and the
    voice settings; `speed` multiplies the speaker's own pace (the API accepts 0.7–1.2)."""
    settings = {"stability": float(getattr(sp, "stability", 0.5)), "similarity_boost": float(getattr(sp, "similarity", 0.75)),
                "style": float(getattr(sp, "style_ex", 0.0)), "use_speaker_boost": True,
                "speed": max(0.7, min(1.2, float(speed) * float(getattr(sp, "speed", 1.0))))}
    model = getattr(sp, "model_id", "") or DEFAULT_MODEL
    out = []
    for piece in _split(text):
        pcm = _call("POST", f"/text-to-speech/{sp.voice_id}?output_format=pcm_24000",
                    {"text": piece, "model_id": model, "voice_settings": settings}, raw=True)
        out.append(np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0)
    return np.concatenate(out) if out else np.zeros(0, dtype=np.float32)
