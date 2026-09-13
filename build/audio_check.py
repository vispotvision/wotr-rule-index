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


_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
         "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
_SAME = {"aye": "i", "hoo": "who", "ay": "i", "oh": "o", "mm": "m", "hm": "m", "hmm": "m"}   # spellings Whisper hears differently


def _num_words(n: int) -> list[str]:
    """61 -> ['sixty', 'one']; 400 -> ['four', 'hundred'] — Whisper writes digits, the scene writes words."""
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + ([_ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [_ONES[n // 100], "hundred"] + (_num_words(n % 100) if n % 100 else [])
    if n < 100000:
        return _num_words(n // 1000) + ["thousand"] + (_num_words(n % 1000) if n % 1000 else [])
    return [str(n)]


def _words(s: str) -> list[str]:
    s = s.lower().replace("’", "'")
    s = re.sub(r"\[[^\]]*\]", " ", s)               # cues
    s = re.sub(r"(\d),(\d{3})", r"\1\2", s)         # 1,100 -> 1100
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    out = []
    for w in s.split():
        if w.isdigit():
            out.extend(_num_words(int(w)))
            continue
        w = _SAME.get(w, w)
        out.append(w.replace("'", ""))
    return out


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
    if errors < 2 or (errors == 2 and len(ref) >= 12):
        return 0.0, " ".join(heard)          # a word or two off is a name, a number or Whisper — not a bad take
    return errors / len(ref), " ".join(heard)
