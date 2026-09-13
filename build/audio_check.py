"""Read-back check for generated speech: transcribe a rendered span and compare it to its text.

Chatterbox is generative — now and then it drops a clause, doubles a word or garbles a
name. build/audio_export.py calls `wer(text, samples)` on every Chatterbox span and
re-renders the span when the word error rate is above the threshold, keeping the
better of the two takes. Kokoro spans are not checked (it is deterministic).

Transcription: faster-whisper, `base.en`, int8 on the CPU (about 10x real time on the
7800X3D; the model, ~150 MB, comes from the Hugging Face hub on first use). Names the
scenes invent will always "miss" — the score is computed after build/pronounce.json
respellings and with a loose match, so a single strange name costs one word, not the span.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher

import numpy as np

SAMPLE_RATE = 24000
_model = None


def _load():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("base.en", device="cpu", compute_type="int8")
    return _model


def _words(s: str) -> list[str]:
    s = s.lower().replace("’", "'")
    s = re.sub(r"\[[^\]]*\]", " ", s)               # cues
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return [w for w in s.split() if w]


def transcribe(samples: np.ndarray, sr: int = SAMPLE_RATE) -> str:
    x = samples.astype(np.float32)
    if sr != 16000:
        n = int(len(x) * 16000 / sr)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    segments, _ = _load().transcribe(x, language="en", beam_size=1, vad_filter=False, condition_on_previous_text=False)
    return " ".join(seg.text.strip() for seg in segments)


def wer(text: str, samples: np.ndarray, sr: int = SAMPLE_RATE) -> tuple[float, str]:
    """Word error rate of the rendered audio against `text` (0 = perfect), and the transcript."""
    ref, heard = _words(text), _words(transcribe(samples, sr))
    if not ref:
        return 0.0, ""
    sm = SequenceMatcher(a=ref, b=heard, autojunk=False)
    errors = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")
    return errors / len(ref), " ".join(heard)
