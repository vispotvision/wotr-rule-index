#!/usr/bin/env python3
"""Reference clips for Chatterbox voices, from openly licensed speech corpora.

  python build/voice_refs.py --browse M Scottish          # VCTK speakers matching gender / accent words
  python build/voice_refs.py --browse F                   # every female VCTK speaker
  python build/voice_refs.py --make gimbzo p254 --seconds 12
  python build/voice_refs.py --make kizami p262 --seconds 10

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
LTS_SPLIT = ("clean", "dev.clean")                                 # 40 readers; enough to cast a narrator
LTS_INDEX = REFS / ".libritts_index.json"
LTS_STEP = 120
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="vctk", choices=["vctk", "libritts"], help="vctk: 110 studio speakers with accent tags; libritts: audiobook readers with pitch/pace descriptions")
    ap.add_argument("--browse", nargs="*", help="words to match: M/F and accents for vctk; gender, pitch, pace, accent words for libritts")
    ap.add_argument("--make", nargs=2, metavar=("NAME", "SPEAKER_ID"))
    ap.add_argument("--seconds", type=float, default=11.0)
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.browse is not None:
        (lts_browse if a.corpus == "libritts" else browse)(a.browse)
    elif a.make:
        (lts_make if a.corpus == "libritts" else make)(a.make[0], a.make[1], a.seconds)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
