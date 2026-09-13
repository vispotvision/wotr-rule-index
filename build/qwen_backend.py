"""Qwen3-TTS VoiceDesign (Alibaba, Apache-2.0) — THE character engine: every line of a designed
voice is generated from a written brief, no reference clip. The manual for writing briefs is
build/voices/QWEN_DESIGN_GUIDE.md; this module is its mechanics.

A speaker whose build/voices.yaml entry says `engine: qwen`:

    Gimbzo:
      engine: qwen
      instruct: "gender: Male. pitch: Very low male pitch, deep bass ... personality: Blunt, patient."
      anchor: build/voices/anchors/Gimbzo.wav   # the take Isaac approved; every draw is scored against it
      tries: 3            # draws per line; the one closest to the anchor is kept
      good_enough: 0.6    # a draw at or above this similarity stops early
      speed: 0.95         # exact, applied after synthesis by build/voice_shape.py (Praat)
      pitch_st: -1        # semitones, same
      formant: 0.95       # body size, same (1.0 = as designed)
      range_factor: 0.85  # intonation range (0.7 flatter … 1.3 livelier)

The brief. Two forms are accepted. The 12-field caption the model was trained on —
`gender, pitch, speed, volume, age, clarity, fluency, accent, texture, emotion, tone,
personality` — is the one to use: the identity fields are frozen bytes for the character, and a
span's delivery tags ([Gimbzo: quiet, slower]) REPLACE the four delivery fields (speed, volume,
emotion, tone) instead of contradicting them. A plain prose brief still works; direction is
then appended as a sentence (the alexandria practice), which is weaker.

Cues. Qwen has no tag vocabulary, so [laugh] [sigh] … are stripped from the text; a laugh is
written into the text as its own word (Gimbzo's "HOO." is already in the prose) and described
in `tone:`; sighs mostly fail on every model. Whisper and laugh-led lines are exempt from the
anchor check (their embedding is not comparable). Beats are silence the narrator inserts.

Consistency. VoiceDesign has no identity slot: the brief names a region of voice-space and every
call draws a fresh member. So each line is drawn up to `tries` times in build/qwen_worker.py and
the draw closest to the anchor (ECAPA speaker-embedding cosine) is kept; low scores are
reported at the end of the render. With faster-qwen3-tts (HIP graphs) a draw runs ~2.5x real
time, so three draws still beat the plain package's single draw.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
VENVS = [Path(r"C:\venvs\wotr-qwen-fast") / "Scripts" / "python.exe",   # faster-qwen3-tts, HIP graphs (preferred)
         Path(r"C:\venvs\wotr-qwen") / "Scripts" / "python.exe"]         # plain qwen-tts
WORKER = ROOT / "build" / "qwen_worker.py"
WORKER_LOG = ROOT / "build" / ".qwen_worker.log"
TARGET_SR = 24000
_proc: subprocess.Popen | None = None
REPORT = {"lines": 0, "draws": 0, "low": []}      # filled in as a scene renders; printed by the narrator
CONTEXT = ""                                       # the scene being rendered; kept takes are scored for coherence within it

FIELDS = ["gender", "pitch", "speed", "volume", "age", "clarity", "fluency", "accent", "texture", "emotion", "tone", "personality"]
_FIELD_RE = re.compile(r"\b(" + "|".join(FIELDS) + r")\s*:\s*", re.I)

# delivery tag -> replacement delivery fields (QWEN_DESIGN_GUIDE.md §4.3); exact pace/gain are applied after synthesis
DELIVERY_FIELDS = {
    "slow":      {"speed": "Slow, deliberate pace."},
    "slower":    {"speed": "Very slow, heavy, deliberate pace, with weight on every word and long pauses."},
    "fast":      {"speed": "Brisk, fast-paced delivery."},
    "faster":    {"speed": "Rapid, hurried, clipped delivery."},
    "quiet":     {"volume": "Soft, hushed, low volume, conversational level.", "tone+": "subdued"},
    "loud":      {"volume": "Loud, forceful, projecting."},
    "whisper":   {"volume": "Whispered, breathy and hushed, very low volume."},
    "urgent":    {"speed": "Urgent, rapid, pressing.", "emotion": "Tense, urgent.", "tone": "Sharp, pressing, insistent."},
    "beat": {}, "long beat": {},
}
# cue -> (word written into the text before the line, addition to tone:)
CUE_TEXT = {
    "laugh": ("", "one short, loud bark of laughter before the first word, then no more laughter"),
    "chuckle": ("Heh.", "a brief, low chuckle before the first word"),
    "sigh": ("Haah...", "begins with an audible sigh"),
    "gasp": ("Ah!", "a sharp gasp before the first word"),
    "groan": ("Hnn.", "a low pained groan before the first word"),
    "breath": ("", "an audible intake of breath before the first word"),
    "cough": ("", "a cough before the first word"),
    "clear throat": ("", "clears the throat before the first word"),
    "sniff": ("Hff.", ""), "shush": ("Shh.", ""),
}
EXEMPT_TAGS = {"whisper"}
EXEMPT_CUES = {"laugh", "chuckle", "gasp", "groan", "cough"}
_CUE = re.compile(r"\s*\[([^\]]*)\]\s*")
# the legacy prose-brief direction (appended), for entries that are not in the 12-field form
DIRECTION = {
    "slow": "Speak slowly.", "slower": "Speak very slowly, with weight on every word.",
    "fast": "Speak quickly.", "faster": "Speak fast and clipped.",
    "quiet": "Speak quietly, almost under the breath, with the same voice.",
    "loud": "Raise the voice: loud, forceful, carrying.", "whisper": "Whisper, breathy and hushed.",
    "urgent": "Urgent and pressing, fast, tense.", "beat": "", "long beat": "",
}


def parse_fields(brief: str) -> dict[str, str] | None:
    """'gender: Male. pitch: Low ...' -> ordered dict, or None when the brief is prose."""
    parts = _FIELD_RE.split(brief.strip())
    if len(parts) < 7:          # fewer than three fields: treat as prose
        return None
    out: dict[str, str] = {}
    for i in range(1, len(parts) - 1, 2):
        out[parts[i].lower()] = parts[i + 1].strip().rstrip(".").strip() + "."
    return out if len(out) >= 3 else None


def render_fields(fields: dict[str, str]) -> str:
    return " ".join(f"{k}: {fields[k]}" for k in FIELDS if k in fields) + \
        "".join(f" {k}: {v}" for k, v in fields.items() if k not in FIELDS)


def instruct_for(sp, mods: list[str], text: str) -> tuple[str, str, bool]:
    """(brief with this span's direction, text with cues turned into words, exempt-from-anchor-check)."""
    cues = [c.strip().lower() for c in _CUE.findall(text)]
    clean = re.sub(r"\s+", " ", _CUE.sub(" ", text)).strip()
    lead = " ".join(CUE_TEXT[c][0] for c in cues if c in CUE_TEXT and CUE_TEXT[c][0])
    if lead:
        clean = f"{lead} {clean}".strip()
    exempt = any(m in EXEMPT_TAGS for m in mods) or any(c in EXEMPT_CUES for c in cues)
    fields = parse_fields(sp.instruct)
    if fields is None:
        parts = [sp.instruct.strip()] + [DIRECTION[m] for m in mods if DIRECTION.get(m)]
        parts += [f"Start with {CUE_TEXT[c][1]}." for c in cues if c in CUE_TEXT and CUE_TEXT[c][1]]
        return " ".join(p for p in parts if p), clean, exempt
    f = dict(fields)
    tone_add = []
    for m in mods:
        for k, v in DELIVERY_FIELDS.get(m, {}).items():
            if k == "tone+":
                tone_add.append(v)
            else:
                f[k] = v
    for c in cues:
        if c in CUE_TEXT and CUE_TEXT[c][1]:
            tone_add.append(CUE_TEXT[c][1])
    if tone_add:
        f["tone"] = f.get("tone", "").rstrip(".") + "; " + "; ".join(tone_add) + "."
    return render_fields(f), clean, exempt


def _worker() -> subprocess.Popen:
    global _proc
    if _proc is None or _proc.poll() is not None:
        py = next((p for p in VENVS if p.exists()), None)
        if py is None:
            sys.exit("Qwen3-TTS is not set up: run build/qwen_tts_setup.ps1")
        log = open(WORKER_LOG, "a", encoding="utf-8")
        log.write(f"\n=== worker start {py}\n"); log.flush()
        _proc = subprocess.Popen([str(py), str(WORKER)], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=log, text=True, encoding="utf-8", bufsize=1)
    return _proc


def _resample(x: np.ndarray, sr: int) -> np.ndarray:
    if sr == TARGET_SR:
        return x
    n = int(len(x) * TARGET_SR / sr)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def _anchor_path(sp) -> str:
    if not sp.anchor:
        return ""
    p = Path(sp.anchor) if Path(sp.anchor).is_absolute() else ROOT / sp.anchor
    if not p.exists():
        sys.exit(f"{sp.name}: anchor clip not found: {p}")
    return str(p)


def synth_lines(sp, texts: list[str], instruct: str, exempt: list[bool]) -> list[np.ndarray]:
    """One worker call for several lines sharing a brief: each line is drawn up to sp.tries times
    and the draw closest to the anchor is kept."""
    w = _worker()
    req = {"texts": texts, "instruct": instruct, "anchor": _anchor_path(sp), "tries": int(getattr(sp, "tries", 1)),
           "good_enough": float(getattr(sp, "good_enough", 0.6)), "exempt": exempt, "seed": getattr(sp, "seed", None),
           "context": CONTEXT}
    for k in ("temperature", "top_k", "top_p", "repetition_penalty", "subtalker_temperature"):
        v = getattr(sp, k, None)
        if v is not None:
            req[k] = v
    w.stdin.write(json.dumps(req) + "\n")
    w.stdin.flush()
    while True:
        line = w.stdout.readline()
        if not line:
            tail = WORKER_LOG.read_text(encoding="utf-8", errors="replace")[-1500:] if WORKER_LOG.exists() else ""
            sys.exit(f"the Qwen worker died (exit {w.poll()}); the end of its log, {WORKER_LOG.name}:\n{tail}")
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "loaded" in msg:
            print(f"  {msg['loaded']}", flush=True)
            continue
        if "error" in msg:
            sys.exit(f"qwen: {msg['error']}\n  " + "\n  ".join(msg.get("where", [])))
        break
    REPORT["lines"] += len(texts)
    REPORT["draws"] += sum(msg.get("tries", [1] * len(texts)))
    if req["anchor"]:
        for t, c, ex in zip(texts, msg["cos"], exempt):
            if c < 0.4 and not ex:
                REPORT["low"].append((c, sp.name, t[:80]))
    out = []
    for p in msg["paths"]:
        x = np.load(p).astype(np.float32)
        Path(p).unlink(missing_ok=True)
        out.append(_resample(x, int(msg["sr"])))
    return out


def synth(cast, sp, text: str, speed: float, mods: list[str] | None = None) -> np.ndarray:
    """Single-span path (the --say test, a retake, or a span that missed the pre-pass)."""
    instruct, clean, exempt = instruct_for(sp, mods or [], text)
    return synth_lines(sp, [clean], instruct, [exempt])[0]
