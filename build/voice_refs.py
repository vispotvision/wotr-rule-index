#!/usr/bin/env python3
"""Reference clips for Chatterbox voices, from openly licensed speech corpora.

  python build/voice_refs.py --browse M Scottish          # VCTK speakers matching gender / accent words
  python build/voice_refs.py --browse F                   # every female VCTK speaker
  python build/voice_refs.py --make gimbzo p254 --seconds 12
  python build/voice_refs.py --make kizami p262 --seconds 10
  python build/voice_refs.py --corpus libritts --split train.clean.100 --browse male "very low"
  python build/voice_refs.py --design gimbzo gimbzo-src --pitch -4 --weight 0.5 --grit 0.35 --pace 0.92

--make joins a few of the speaker's sentences into one clip, build/voices/refs/<name>.wav
(24 kHz mono, 6–15 s is what Chatterbox wants), and appends the credit line to
build/voices/refs/CREDITS.md. Point a voices.yaml entry at it:

    Gimbzo:
      engine: chatterbox
      ref: build/voices/refs/gimbzo.wav

Source: the VCTK Corpus (Yamagishi, Veaux, MacDonald; CSTR, University of
Edinburgh), CC BY 4.0, read through the Hugging Face datasets server from the
sanchit-gandhi/vctk mirror. Every speaker recorded for release under that
licence, which is the line Isaac drew: designed or permissioned voices, never
a person who did not agree. Attribution travels with the clip (CREDITS.md); keep
it in any audiobook you distribute. build/voices/*.wav is gitignored — the clips
stay on this PC; re-run --make to rebuild one.
"""
import argparse
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "build" / "voices" / "refs"
API = "https://datasets-server.huggingface.co"
DATASET = "sanchit-gandhi/vctk"
CREDIT = ("VCTK Corpus (Yamagishi, Veaux & MacDonald, CSTR, University of Edinburgh), CC BY 4.0, "
          "https://datashare.ed.ac.uk/handle/10283/3443 — speaker {sid} ({gender}, {age}, {accent}, {region}); "
          "sentences {ids}")
TARGET_SR = 24000


import os
import time

PAUSE = 2.5         # the datasets server rate-limits anonymous callers; pace every request


def get(url: str):
    """One request, paced; on 429 wait a minute and try again (a few times)."""
    headers = {"User-Agent": "wotr-audio/1.0"}
    if os.environ.get("HF_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["HF_TOKEN"]
    for attempt in range(5):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if "datasets-server" in url:
                time.sleep(PAUSE)
            return data
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            code = getattr(e, "code", 0)
            if attempt < 4 and (code == 429 or code >= 500 or not code):
                wait = 60 if code == 429 else 10
                print(f"  {code or 'network'}; waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise


def rows(offset: int = 0, length: int = 100) -> list[dict]:
    q = urllib.parse.urlencode({"dataset": DATASET, "config": "default", "split": "train", "offset": offset, "length": length})
    data = json.loads(get(f"{API}/rows?{q}").decode())
    return [r["row"] for r in data.get("rows", [])]


INDEX = REFS / ".vctk_index.json"
STEP = 400          # the mirror holds ~800 rows per speaker (two microphones), in speaker order


def index() -> dict[str, dict]:
    """speaker_id -> {offset, gender, age, accent, region}; sampled once (paced, resumable), cached."""
    REFS.mkdir(parents=True, exist_ok=True)
    state = json.loads(INDEX.read_text(encoding="utf-8-sig")) if INDEX.exists() else {"_next": 0, "_total": None, "speakers": {}}
    if state.get("_done"):
        return state["speakers"]
    if state["_total"] is None:
        q = urllib.parse.urlencode({"dataset": DATASET, "config": "default", "split": "train", "offset": 0, "length": 1})
        state["_total"] = json.loads(get(f"{API}/rows?{q}").decode())["num_rows_total"]
    total, idx = state["_total"], state["speakers"]
    print(f"  indexing {total:,} rows in steps of {STEP} from {state['_next']:,} (once; ~{PAUSE}s a request)…", flush=True)
    for off in range(state["_next"], total, STEP):
        r = rows(off, 1)[0]
        idx.setdefault(r["speaker_id"], {"offset": off, "gender": r["gender"], "age": r["age"], "accent": r["accent"], "region": r["region"]})
        state["_next"] = off + STEP
        INDEX.write_text(json.dumps(state, indent=1), encoding="utf-8")
    state["_done"] = True
    INDEX.write_text(json.dumps(state, indent=1), encoding="utf-8")
    return idx


def browse(words: list[str]) -> None:
    gender = next((w.upper() for w in words if w.upper() in ("M", "F")), "")
    accents = [w.lower() for w in words if w.upper() not in ("M", "F")]
    n = 0
    for sid, r in sorted(index().items()):
        if gender and r["gender"] != gender:
            continue
        if accents and not any(a in (r["accent"] + " " + r["region"]).lower() for a in accents):
            continue
        print(f"  {sid}  {r['gender']}  age {r['age']:>2}  {r['accent']:<14} {r['region']}")
        n += 1
    print(f"{n} speakers; --make <name> <speaker_id> to build a clip")


def make(name: str, sid: str, seconds: float) -> Path:
    import soundfile as sf
    REFS.mkdir(parents=True, exist_ok=True)
    entry = index().get(sid)
    if not entry:
        sys.exit(f"unknown speaker {sid}; --browse lists them")
    # the sampled offset is somewhere inside the speaker's block; take rows from there on,
    # one microphone only, skipping the two calibration sentences every speaker reads
    picked = [r for r in rows(entry["offset"], 60)
              if r["speaker_id"] == sid and r["text_id"] not in ("001", "002") and "mic2" not in r.get("file", "")]
    if not picked:
        sys.exit(f"no rows for speaker {sid}")
    parts, ids, total = [], [], 0.0
    for r in picked:
        src = r["audio"][0]["src"]
        data, sr = sf.read(io.BytesIO(get(src)), dtype="float32")
        if data.ndim > 1:
            data = data.mean(axis=1)
        if sr != TARGET_SR:
            n = int(len(data) * TARGET_SR / sr)
            data = np.interp(np.linspace(0, len(data) - 1, n), np.arange(len(data)), data).astype(np.float32)
        parts.append(data)
        parts.append(np.zeros(int(TARGET_SR * 0.35), dtype=np.float32))
        ids.append(r["text_id"])
        total += len(data) / TARGET_SR + 0.35
        if total >= seconds:
            break
    clip = np.concatenate(parts)
    peak = float(np.max(np.abs(clip))) or 1.0
    clip = clip / peak * 0.9
    out = REFS / f"{name}.wav"
    sf.write(str(out), clip, TARGET_SR, subtype="PCM_16")
    r0 = picked[0]
    line = f"- `{out.name}`: " + CREDIT.format(sid=sid, gender=r0["gender"], age=r0["age"], accent=r0["accent"], region=r0["region"], ids=", ".join(ids))
    credits = REFS / "CREDITS.md"
    old = credits.read_text(encoding="utf-8") if credits.exists() else "# Reference clips — credits\n\nEach clip below designs a Chatterbox voice. Keep these lines with any audio you share.\n\n"
    old = "\n".join(l for l in old.splitlines() if not l.startswith(f"- `{out.name}`")) + "\n"
    credits.write_text(old + line + "\n", encoding="utf-8")
    print(f"  {out.relative_to(ROOT)}: {total:.1f}s from speaker {sid} ({r0['gender']}, {r0['age']}, {r0['accent']}) — credited in {credits.relative_to(ROOT)}")
    return out


# ---------------------------------------------------------------- LibriTTS-R (audiobook readers)

LTS_DESC = "parler-tts/libritts-r-filtered-speaker-descriptions"   # per-utterance gender / pitch / pace / accent, no audio
LTS_AUDIO = "parler-tts/libritts_r_filtered"                       # the same rows with audio
LTS_SPLITS = {"dev.clean": ("clean", "dev.clean", 120), "train.clean.100": ("clean", "train.clean.100", 300), "train.clean.360": ("clean", "train.clean.360", 400)}
LTS_SPLIT = LTS_SPLITS["dev.clean"][:2]
LTS_STEP = 120


def lts_use(split: str) -> None:
    """Pick which LibriTTS-R split to browse/make from: dev.clean (40 readers), train.clean.100 (247), train.clean.360 (904)."""
    global LTS_SPLIT, LTS_STEP, LTS_INDEX
    c, s, step = LTS_SPLITS[split]
    LTS_SPLIT, LTS_STEP = (c, s), step
    LTS_INDEX = REFS / f".libritts_index_{s}.json"


LTS_INDEX = REFS / ".libritts_index_dev.clean.json"
LTS_CREDIT = ("LibriTTS-R (Koizumi et al., 2023; derived from LibriTTS / LibriVox public-domain readings), CC BY 4.0, "
              "https://www.openslr.org/141/ — reader {sid} ({gender}, {pitch}, {rate}, {accent}); utterances {ids}")


def _rows(dataset: str, config: str, split: str, offset: int, length: int) -> list[dict]:
    q = urllib.parse.urlencode({"dataset": dataset, "config": config, "split": split, "offset": offset, "length": length})
    return [r["row"] for r in json.loads(get(f"{API}/rows?{q}").decode()).get("rows", [])]


def lts_index() -> dict[str, dict]:
    REFS.mkdir(parents=True, exist_ok=True)
    state = json.loads(LTS_INDEX.read_text(encoding="utf-8-sig")) if LTS_INDEX.exists() else {"_next": 0, "_total": None, "speakers": {}}
    if state.get("_done"):
        return state["speakers"]
    c, s = LTS_SPLIT
    if state["_total"] is None:
        q = urllib.parse.urlencode({"dataset": LTS_DESC, "config": c, "split": s, "offset": 0, "length": 1})
        state["_total"] = json.loads(get(f"{API}/rows?{q}").decode())["num_rows_total"]
    print(f"  indexing LibriTTS-R {s}: {state['_total']:,} rows in steps of {LTS_STEP} from {state['_next']:,} (once)…", flush=True)
    for off in range(state["_next"], state["_total"], LTS_STEP):
        r = _rows(LTS_DESC, c, s, off, 1)[0]
        state["speakers"].setdefault(r["speaker_id"], {"offset": off, "gender": r["gender"], "pitch": r["pitch"], "rate": r["speaking_rate"],
                                                        "accent": r.get("accent", ""), "monotony": r["speech_monotony"], "description": r["text_description"]})
        state["_next"] = off + LTS_STEP
        LTS_INDEX.write_text(json.dumps(state, indent=1), encoding="utf-8")
    state["_done"] = True
    LTS_INDEX.write_text(json.dumps(state, indent=1), encoding="utf-8")
    return state["speakers"]


def lts_browse(words: list[str]) -> None:
    words = [w.lower() for w in words]
    n = 0
    for sid, r in sorted(lts_index().items(), key=lambda kv: int(kv[0])):
        blob = " ".join(str(v) for v in r.values()).lower()
        if words and not all(w in blob for w in words):
            continue
        print(f"  {sid:>5}  {r['gender']:<6} {r['pitch']:<18} {r['rate']:<14} {r['accent']:<14} {r['description'][:90]}")
        n += 1
    print(f"{n} readers; --make <name> <speaker_id> --corpus libritts to build a clip")


def lts_make(name: str, sid: str, seconds: float) -> Path:
    import soundfile as sf
    entry = lts_index().get(sid)
    if not entry:
        sys.exit(f"unknown reader {sid}; --browse --corpus libritts lists them")
    c, s = LTS_SPLIT
    picked = [r for r in _rows(LTS_AUDIO, c, s, entry["offset"], 40) if r["speaker_id"] == sid and 2.0 < len(r["text_normalized"].split()) / 2.5]
    if not picked:
        sys.exit(f"no audio rows for reader {sid} at offset {entry['offset']}")
    parts, ids, total = [], [], 0.0
    for r in picked:
        data, sr = sf.read(io.BytesIO(get(r["audio"][0]["src"])), dtype="float32")
        if data.ndim > 1:
            data = data.mean(axis=1)
        if sr != TARGET_SR:
            n = int(len(data) * TARGET_SR / sr)
            data = np.interp(np.linspace(0, len(data) - 1, n), np.arange(len(data)), data).astype(np.float32)
        parts += [data, np.zeros(int(TARGET_SR * 0.35), dtype=np.float32)]
        ids.append(r["id"])
        total += len(data) / TARGET_SR + 0.35
        if total >= seconds:
            break
    clip = np.concatenate(parts)
    clip = clip / (float(np.max(np.abs(clip))) or 1.0) * 0.9
    out = REFS / f"{name}.wav"
    sf.write(str(out), clip, TARGET_SR, subtype="PCM_16")
    line = f"- `{out.name}`: " + LTS_CREDIT.format(sid=sid, gender=entry["gender"], pitch=entry["pitch"], rate=entry["rate"], accent=entry["accent"], ids=", ".join(ids))
    credits = REFS / "CREDITS.md"
    old = credits.read_text(encoding="utf-8") if credits.exists() else "# Reference clips — credits\n\nEach clip below designs a Chatterbox voice. Keep these lines with any audio you share.\n\n"
    old = "\n".join(l for l in old.splitlines() if not l.startswith(f"- `{out.name}`")) + "\n"
    credits.write_text(old + line + "\n", encoding="utf-8")
    print(f"  {out.relative_to(ROOT)}: {total:.1f}s from reader {sid} ({entry['gender']}, {entry['pitch']}, {entry['rate']}) — credited in {credits.relative_to(ROOT)}")
    return out


# ---------------------------------------------------------------- designing a voice

def design(name: str, source: str, pitch: float = 0.0, weight: float = 0.0, grit: float = 0.0, breath: float = 0.0, pace: float = 1.0) -> Path:
    """Build build/voices/refs/<name>.wav from an existing clip, shaped toward a description.

    pitch   semitones, negative = deeper (-3 to -5 turns a baritone into a bass; the clone follows)
    weight  0-1, adds a copy an octave down underneath (chest, size)
    grit    0-1, soft saturation, a rasp that thickens with level
    breath  0-1, a little filtered noise under the voice (worn, tired, whispery)
    pace    stretch factor, 0.9 = slower, unhurried
    The result is a designed voice: nobody's, built from a consenting reader's clip. Credited as such.
    """
    import librosa
    import soundfile as sf
    src = Path(source) if Path(source).is_absolute() else (REFS / f"{source}.wav" if not source.endswith(".wav") else ROOT / source)
    if not src.exists():
        sys.exit(f"no clip at {src}")
    y, sr = sf.read(str(src), dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    if sr != TARGET_SR:
        y = librosa.resample(y, orig_sr=sr, target_sr=TARGET_SR)
        sr = TARGET_SR
    if abs(pace - 1.0) > 0.01:
        y = librosa.effects.time_stretch(y, rate=pace)
    if abs(pitch) > 0.01:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch)
    if weight > 0:
        low = librosa.effects.pitch_shift(y, sr=sr, n_steps=-12)
        y = y + weight * 0.6 * low
    if grit > 0:
        drive = 1.0 + 6.0 * grit
        y = np.tanh(y * drive) / np.tanh(drive) * (0.7 + 0.3 * (1 - grit)) + y * 0.3
    if breath > 0:
        rng = np.random.default_rng(0)
        noise = rng.standard_normal(len(y)).astype(np.float32)
        b, a = _lowpass(sr, 4000.0)
        from scipy.signal import lfilter
        noise = lfilter(b, a, noise).astype(np.float32)
        env = np.abs(librosa.effects.preemphasis(y))
        env = np.convolve(env, np.ones(1200) / 1200, mode="same")
        y = y + breath * 0.25 * noise * (env / (env.max() or 1.0))
    y = y / (float(np.max(np.abs(y))) or 1.0) * 0.9
    out = REFS / f"{name}.wav"
    sf.write(str(out), y.astype(np.float32), sr, subtype="PCM_16")
    line = (f"- `{out.name}`: designed voice — {src.name} shaped with pitch {pitch:+.1f} st, weight {weight}, grit {grit}, breath {breath}, pace {pace}; "
            f"see that clip's line for the source reader's credit")
    credits = REFS / "CREDITS.md"
    old = credits.read_text(encoding="utf-8") if credits.exists() else "# Reference clips — credits\n\n"
    old = "\n".join(l for l in old.splitlines() if not l.startswith(f"- `{out.name}`")) + "\n"
    credits.write_text(old + line + "\n", encoding="utf-8")
    print(f"  {out.relative_to(ROOT)}: {len(y)/sr:.1f}s from {src.name} (pitch {pitch:+.1f}, weight {weight}, grit {grit}, breath {breath}, pace {pace})")
    return out


def _lowpass(sr: int, hz: float):
    from scipy.signal import butter
    return butter(2, hz / (sr / 2), btype="low")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="vctk", choices=["vctk", "libritts"], help="vctk: 110 studio speakers with accent tags; libritts: audiobook readers with pitch/pace descriptions")
    ap.add_argument("--browse", nargs="*", help="words to match: M/F and accents for vctk; gender, pitch, pace, accent words for libritts")
    ap.add_argument("--make", nargs=2, metavar=("NAME", "SPEAKER_ID"))
    ap.add_argument("--seconds", type=float, default=11.0)
    ap.add_argument("--split", default="dev.clean", choices=list(LTS_SPLITS), help="libritts: which split to draw readers from")
    ap.add_argument("--design", nargs=2, metavar=("NAME", "SOURCE"), help="shape an existing clip (a refs/ name or a .wav path) into a new reference")
    ap.add_argument("--pitch", type=float, default=0.0, help="--design: semitones, negative = deeper")
    ap.add_argument("--weight", type=float, default=0.0, help="--design: 0-1 sub-octave weight")
    ap.add_argument("--grit", type=float, default=0.0, help="--design: 0-1 rasp")
    ap.add_argument("--breath", type=float, default=0.0, help="--design: 0-1 breathiness")
    ap.add_argument("--pace", type=float, default=1.0, help="--design: time stretch, 0.9 = slower")
    a = ap.parse_args()
    lts_use(a.split)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.design:
        design(a.design[0], a.design[1], a.pitch, a.weight, a.grit, a.breath, a.pace)
    elif a.browse is not None:
        (lts_browse if a.corpus == "libritts" else browse)(a.browse)
    elif a.make:
        (lts_make if a.corpus == "libritts" else make)(a.make[0], a.make[1], a.seconds)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
