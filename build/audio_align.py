"""Cut one generated take back into its spans, by word-level alignment.

Why: a design-mode engine (Qwen VoiceDesign) draws a fresh voice every call but cannot change
voice inside a call, so the narrator joins a speaker's consecutive spans into one text, has it
spoken once, and needs the audio back as spans. faster-whisper (already the read-back checker)
transcribes with word timestamps; the heard words are aligned to the written words of each span
(difflib on normalised words), and the take is cut in the silence between the last matched
word of one span and the first matched word of the next. A span whose words were not heard at
all (a one-word line the model swallowed, an invented name) gets a boundary interpolated by
character count between its neighbours — never dropped.

    pieces = split(samples, sr, ["First span text.", "Second span.", ...])   # list of arrays, same order
"""
from __future__ import annotations

from difflib import SequenceMatcher

import numpy as np

import audio_check


def _heard_words(samples: np.ndarray, sr: int) -> list[tuple[str, float, float]]:
    """[(normalised word, start s, end s)] from faster-whisper with word timestamps."""
    x = samples.astype(np.float32)
    if sr != 16000:
        n = int(len(x) * 16000 / sr)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    segments, _ = audio_check._load().transcribe(x, language="en", beam_size=1, vad_filter=False,
                                                 condition_on_previous_text=False, word_timestamps=True)
    out = []
    for seg in segments:
        for w in seg.words or []:
            toks = audio_check._words(w.word)
            for t in toks:                       # "sixty-one" may come back as two tokens with one timing
                out.append((t, float(w.start), float(w.end)))
    return out


def split(samples: np.ndarray, sr: int, texts: list[str], pad: float = 0.04) -> list[np.ndarray]:
    if len(texts) == 1:
        return [samples]
    heard = _heard_words(samples, sr)
    written, owner = [], []                       # every written word, and which span it belongs to
    for i, t in enumerate(texts):
        ws = audio_check._words(t)
        written += ws
        owner += [i] * len(ws)
    sm = SequenceMatcher(a=written, b=[h[0] for h in heard], autojunk=False)
    first: dict[int, float] = {}                  # span -> time of its first matched word
    last: dict[int, float] = {}                   # span -> time of its last matched word
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            continue
        for k in range(i2 - i1):
            span, (_, s, e) = owner[i1 + k], heard[j1 + k]
            first.setdefault(span, s)
            last[span] = e
    total = len(samples) / sr
    # a boundary between span i and i+1: midway through the gap between i's last word and i+1's first word
    bounds: list[float | None] = []
    for i in range(len(texts) - 1):
        if i in last and (i + 1) in first and first[i + 1] >= last[i]:
            bounds.append((last[i] + first[i + 1]) / 2)
        elif i in last:
            bounds.append(last[i] + pad)
        elif (i + 1) in first:
            bounds.append(max(0.0, first[i + 1] - pad))
        else:
            bounds.append(None)
    # unknown boundaries: interpolate by character share between the nearest known ones
    chars = np.array([max(1, len(t)) for t in texts], dtype=float)
    cum = np.cumsum(chars)
    known = [(-1, 0.0)] + [(i, b) for i, b in enumerate(bounds) if b is not None] + [(len(texts) - 1, total)]
    for i, b in enumerate(bounds):
        if b is not None:
            continue
        lo = max(k for k in known if k[0] < i)
        hi = min(k for k in known if k[0] > i)
        c_lo = cum[lo[0]] if lo[0] >= 0 else 0.0
        c_hi = cum[hi[0]]
        frac = (cum[i] - c_lo) / max(1e-9, c_hi - c_lo)
        bounds[i] = lo[1] + frac * (hi[1] - lo[1])
    # monotone, inside the take
    cuts = [0.0]
    for b in bounds:
        cuts.append(min(total, max(cuts[-1], float(b))))
    cuts.append(total)
    pieces = []
    for i in range(len(texts)):
        a, b = int(cuts[i] * sr), int(cuts[i + 1] * sr)
        pieces.append(samples[a:b] if b > a else np.zeros(int(0.05 * sr), dtype=np.float32))
    return pieces


def coverage(samples: np.ndarray, sr: int, texts: list[str]) -> float:
    """Share of spans whose words were heard at all — a cheap sanity check before trusting a split."""
    heard = _heard_words(samples, sr)
    written, owner = [], []
    for i, t in enumerate(texts):
        ws = audio_check._words(t); written += ws; owner += [i] * len(ws)
    sm = SequenceMatcher(a=written, b=[h[0] for h in heard], autojunk=False)
    seen = set()
    for tag, i1, i2, _, _ in sm.get_opcodes():
        if tag == "equal":
            seen.update(owner[i1:i2])
    return len(seen) / max(1, len(texts))
