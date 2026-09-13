"""Exact speed and pitch control for engines that have none (Qwen3-TTS VoiceDesign, Chatterbox).

Qwen3-TTS takes pace and pitch only as words in its brief ("slow", "slightly low pitch");
there is no number to set (QwenLM/Qwen3-TTS discussion #241, issue #290 — still open). So
the narrator applies them AFTER synthesis, with Praat (parselmouth), which changes duration
and pitch by overlap-add on the actual glottal periods instead of a phase vocoder — no
smear on consonants, and the voice's formants (the resonances that say how big the body
is) stay where they were unless you move them on purpose.

    shape(samples, sr, speed=0.9)                  10 % slower, same pitch, same body
    shape(samples, sr, pitch_st=-2)                two semitones deeper, same body
    shape(samples, sr, formant=0.9)                a bigger body, same note
    shape(samples, sr, range_factor=0.7)           flatter intonation (menace, age)

Keep it small: beyond about ±3 semitones, formant 0.85, or speed 0.8 it starts to sound
processed, and a designed voice should get its depth from the brief, not from here.
"""
from __future__ import annotations

import numpy as np


def shape(samples: np.ndarray, sr: int, speed: float = 1.0, pitch_st: float = 0.0, formant: float = 1.0,
          range_factor: float = 1.0) -> np.ndarray:
    if abs(speed - 1.0) < 0.01 and abs(pitch_st) < 0.05 and abs(formant - 1.0) < 0.005 and abs(range_factor - 1.0) < 0.01:
        return samples
    import parselmouth
    from parselmouth.praat import call
    snd = parselmouth.Sound(samples.astype(np.float64), sampling_frequency=sr)
    floor, ceiling = 60, 500
    # median pitch of the take, so the shift is relative to what the engine gave us
    pitch = snd.to_pitch(pitch_floor=floor, pitch_ceiling=ceiling)
    f0 = pitch.selected_array["frequency"]
    f0 = f0[f0 > 0]
    median = float(np.median(f0)) if len(f0) else 0.0
    new_median = median * (2.0 ** (pitch_st / 12.0)) if median and abs(pitch_st) >= 0.05 else 0.0   # 0 keeps Praat's default (no change)
    # Change gender: pitch floor, ceiling, formant shift ratio, new pitch median (0 = keep), pitch range factor, duration factor
    out = call(snd, "Change gender", floor, ceiling, float(formant), float(new_median), float(range_factor), float(1.0 / speed))
    y = out.values[0].astype(np.float32)
    peak = float(np.max(np.abs(y))) if len(y) else 0.0
    if peak > 0.99:
        y = y / peak * 0.99
    return y
