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
    sf.write(str(out), clip, TARGET_SR)
    r0 = picked[0]
    line = f"- `{out.name}`: " + CREDIT.format(sid=sid, gender=r0["gender"], age=r0["age"], accent=r0["accent"], region=r0["region"], ids=", ".join(ids))
    credits = REFS / "CREDITS.md"
    old = credits.read_text(encoding="utf-8") if credits.exists() else "# Reference clips — credits\n\nEach clip below designs a Chatterbox voice. Keep these lines with any audio you share.\n\n"
    old = "\n".join(l for l in old.splitlines() if not l.startswith(f"- `{out.name}`")) + "\n"
    credits.write_text(old + line + "\n", encoding="utf-8")
    print(f"  {out.relative_to(ROOT)}: {total:.1f}s from speaker {sid} ({r0['gender']}, {r0['age']}, {r0['accent']}) — credited in {credits.relative_to(ROOT)}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--browse", nargs="*", help="gender (M/F) and/or accent words, e.g. M Scottish")
    ap.add_argument("--make", nargs=2, metavar=("NAME", "SPEAKER_ID"))
    ap.add_argument("--seconds", type=float, default=11.0)
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.browse is not None:
        browse(a.browse)
    elif a.make:
        make(a.make[0], a.make[1], a.seconds)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
