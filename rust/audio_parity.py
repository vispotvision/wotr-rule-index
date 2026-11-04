#!/usr/bin/env python3
"""The Rust narration pipeline (`wotr-mcp audio`: rust/src/audio.rs, kokoro.rs, supertonic.rs) against
build/audio_export.py and its backends.

  bash build/py.sh rust/audio_parity.py [scratch-dir]     # exit 1 on any difference

1. phonemes and token ids, Python (kokoro-onnx + phonemizer + espeak-ng) vs Rust, every paragraph of
   twelve scenes (six from scenes/, six from lore/v1/scenes/);
2. Kokoro samples for short and long passages, voices and blends and speeds: max abs difference;
3. Supertonic samples, both seeded alike (np.random.seed / WOTR_SUPERTONIC_SEED): max abs difference;
4. the pipeline end to end in a scratch clone: --dry-run, --dry-run --plain, --list-voices, one short
   scene rendered by each (MP3 bytes, manifest, log, wall time), the Rust skipping the Python's render
   as unchanged, and a --wav audition cut;
5. a cast file mixing the narrator (Kokoro), a Supertonic speaker and a Chatterbox speaker (Gimbzo,
   whose Qwen entry is locked and falls back to Gimbzo-cb) through both pipelines with the real GPU
   worker and the read-back check: Chatterbox samples, so the requests its worker receives are compared;
6. --engine elevenlabs with the API faked on both sides (a patched _call in Python, a stub curl for
   Rust): the requests and the MP3. The real API is never called.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REAL = Path(__file__).resolve().parent.parent
BIN = REAL / "rust" / "target" / "release" / "wotr-mcp"
S = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wotr-audio-parity").resolve()
HOME = Path.home()
PY = HOME / ".venvs/wotr/bin/python"
ST_PY = HOME / ".venvs/wotr-supertonic/bin/python"
sys.path.insert(0, str(REAL / "build"))
import audio_export as A  # noqa: E402

bad = 0


def fail(msg: str) -> None:
    global bad
    bad += 1
    print("  DIFF " + msg)


class Probe:
    def __init__(self, env=None):
        self.p = subprocess.Popen([str(BIN), "audio-probe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, env={**os.environ, **(env or {})})

    def ask(self, req: dict) -> dict:
        self.p.stdin.write(json.dumps(req) + "\n")
        self.p.stdin.flush()
        r = json.loads(self.p.stdout.readline())
        if "error" in r:
            raise SystemExit(f"probe: {r['error']}")
        return r

    def close(self):
        self.p.stdin.close()
        self.p.wait()


def scene_texts() -> list[str]:
    lex = A.load_lexicon()
    files = sorted(p for p in (REAL / "scenes").glob("*.md") if p.name not in ("ARCS.md", "CAST.md", "TIMELINE.md", "MANIFEST.md"))
    lore = sorted((REAL / "lore/v1/scenes").glob("*.md"))
    pick = files[:: max(1, len(files) // 6)][:6] + lore[:: max(1, len(lore) // 6)][:6]
    out = []
    for p in pick:
        for kind, text in A.scene_blocks(p.read_text(encoding="utf-8", errors="replace")):
            if kind != "divider":
                out.append(A.strip_cues(A.respell(text, lex)))
    return out


def check_phonemes(probe: Probe) -> None:
    from kokoro_onnx import Kokoro
    from kokoro_onnx.tokenizer import Tokenizer
    tok = Tokenizer()
    texts = scene_texts()
    py = []
    for t in texts:
        batches = Kokoro._split_phonemes(None, tok.phonemize(t, "en-us"))
        py.append([[b, tok.tokenize(b[:510])] for b in batches])
    rs = probe.ask({"op": "phonemes", "texts": texts})["batches"]
    diff = [i for i, (a, b) in enumerate(zip(py, rs)) if a != b]
    n_batches = sum(len(b) for b in py)
    print(f"phonemes: {len(texts)} paragraphs, {n_batches} batches, {sum(len(t) for b in py for _, t in b):,} tokens; {len(diff)} differ")
    for i in diff[:5]:
        fail(f"{texts[i][:80]!r}\n    py: {py[i]}\n    rs: {rs[i]}")


def compare(label: str, a: np.ndarray, b: np.ndarray) -> float:
    if len(a) != len(b):
        fail(f"{label}: {len(a)} vs {len(b)} samples")
        return float("inf")
    d = float(np.max(np.abs(a - b))) if len(a) else 0.0
    print(f"  {label}: {len(a):,} samples, max abs diff {d:.3g}")
    if d > 1e-4:
        fail(f"{label}: max abs diff {d}")
    return d


PASSAGES = {
    "short": "He did not look up. \"You will not say that again,\" she said.",
    "long": " ".join(["The ford ran brown with the thaw, and the cart sank to its axles in the silt while the ox bawled "
                      "and the drover cursed it in three languages, none of them his own; on the far bank a Guild clerk "
                      "counted the crates twice, wrote a number, struck it out, and wrote a smaller one."] * 3),
}


def check_kokoro(probe: Probe) -> None:
    eng = A.load_engine()
    print("kokoro samples:")
    for name, text in PASSAGES.items():
        for voice, speed in [("af_heart", 1.0), ("af_heart:0.6,bm_george:0.4", 0.9), ("bm_george", 1.12)]:
            style, pack = A.voice_style(eng, voice)
            py, _ = eng.get(pack).create(text, voice=style, speed=speed, lang="en-us")
            out = S / "k.f32"
            probe.ask({"op": "kokoro", "text": text, "voice": voice, "speed": speed, "out": str(out)})
            compare(f"{name} {voice} x{speed}", py.astype(np.float32), np.fromfile(out, dtype="<f4"))


ST_DRIVER = r'''
import json, sys, numpy as np
from supertonic import TTS
np.random.seed(int(sys.argv[1]))
tts = TTS(auto_download=True)
for req in json.loads(sys.argv[2]):
    wav, _ = tts.synthesize(text=req["text"], voice_style=tts.get_voice_style(voice_name=req["voice"]), total_steps=req["steps"],
                            speed=req["speed"], lang="en", max_chunk_length=300, silence_duration=0.25)
    np.asarray(wav, dtype=np.float32).squeeze().tofile(req["out"])
'''


def check_supertonic() -> None:
    import supertonic_backend as SB
    reqs = [{"text": SB.cues_to_tags(t), "voice": v, "steps": st, "speed": sp} for t, v, st, sp in [
        (PASSAGES["short"], "M2", 10, 0.95), ("[laugh] Ha! You call that a sword? [sigh] Fine.", "F5", 8, 1.0), (PASSAGES["long"], "M1", 5, 1.2)]]
    for i, r in enumerate(reqs):
        r["py"], r["rs"] = str(S / f"st{i}.py.f32"), str(S / f"st{i}.rs.f32")
    subprocess.run([str(ST_PY), "-c", ST_DRIVER, "7", json.dumps([{**r, "out": r["py"]} for r in reqs])], check=True, stderr=subprocess.DEVNULL)
    p = Probe({"WOTR_SUPERTONIC_SEED": "7"})
    for r in reqs:
        p.ask({"op": "supertonic", "text": r["text"], "voice": r["voice"], "steps": r["steps"], "speed": r["speed"], "out": r["rs"]})
    p.close()
    print("supertonic samples (both seeded 7, one stream across the three):")
    for r in reqs:
        compare(f"{r['voice']} steps={r['steps']} x{r['speed']} {r['text'][:30]!r}", np.fromfile(r["py"], dtype="<f4"), np.fromfile(r["rs"], dtype="<f4"))


def clone() -> Path:
    c = S / "clone"
    subprocess.run(["git", "clone", "-q", "--depth", "1", f"file://{REAL}", str(c)], check=True)
    (c / "build/models").mkdir(exist_ok=True)
    for f in (REAL / "build/models").glob("*.onnx"):
        (c / "build/models" / f.name).symlink_to(f)
    for f in (REAL / "build/models").glob("*.bin"):
        (c / "build/models" / f.name).symlink_to(f)
    for f in (REAL / "scenes").glob("*.md"):           # the working tree's scenes (ARCS.md is not tracked)
        shutil.copy(f, c / "scenes" / f.name)
    for f in (REAL / "build/voices/refs").glob("*.wav"):
        shutil.copy(f, c / "build/voices/refs" / f.name)
    return c


def norm_log(t: str, *outs: Path) -> str:
    for o in outs:
        t = t.replace(str(o), "<OUT>")
    t = re.sub(r" in \d+s", " in Ns", t)
    return "\n".join(l for l in t.splitlines() if "WARNING" not in l)


def run_both(c: Path, args: list[str], py_out: Path, rs_out: Path, env: dict | None = None, py_env: dict | None = None) -> tuple:
    e = {**os.environ, "WOTR_ROOT": str(c), **(env or {})}
    t0 = time.time()
    p = subprocess.run([str(PY), str(c / "build/audio_export.py"), *args, "--out", str(py_out)], capture_output=True, text=True, env={**e, **(py_env or {})}, cwd=c)
    t1 = time.time()
    r = subprocess.run([str(BIN), "audio", *args, "--out", str(rs_out)], capture_output=True, text=True, env=e, cwd=c)
    t2 = time.time()
    return p, r, t1 - t0, t2 - t1


def check_e2e(c: Path) -> None:
    print("pipeline:")
    for args in (["--dry-run"], ["--dry-run", "--plain"], ["--list-voices"]):
        p, r, _, _ = run_both(c, args, S / "x", S / "x")
        if (p.stdout, p.returncode) != (r.stdout, r.returncode) or not p.stdout:
            fail(f"{' '.join(args)}: outputs differ ({len(p.stdout)} vs {len(r.stdout)} chars, exit {p.returncode} vs {r.returncode})")
        else:
            print(f"  {' '.join(args)}: identical ({len(p.stdout.splitlines()):,} lines)")
    scene = "naiser_and_seradris_the_courtyard.md"
    py_out, rs_out = S / "e2e/py", S / "e2e/rs"
    p, r, tp, tr = run_both(c, ["--scene", scene], py_out, rs_out)
    print(f"  {scene}, Kokoro only: python {tp:.0f} s, rust {tr:.0f} s")
    mp3 = lambda o: sorted(o.rglob("*.mp3"))  # noqa: E731
    a, b = mp3(py_out), mp3(rs_out)
    if [x.relative_to(py_out) for x in a] != [x.relative_to(rs_out) for x in b] or not a:
        fail(f"files: {a} vs {b}")
    elif a[0].read_bytes() != b[0].read_bytes():
        fail(f"{a[0].name}: MP3 bytes differ ({a[0].stat().st_size} vs {b[0].stat().st_size})")
    else:
        print(f"  {a[0].relative_to(py_out)}: MP3 identical ({a[0].stat().st_size:,} bytes)")
    for f in (".manifest.json",):
        if (py_out / f).read_text() != (rs_out / f).read_text():
            fail(f"{f} differs")
    if norm_log(p.stdout, py_out) != norm_log(r.stdout, rs_out):
        fail(f"log differs:\n{p.stdout}\n---\n{r.stdout}")
    r2 = subprocess.run([str(BIN), "audio", "--scene", scene, "--out", str(py_out)], capture_output=True, text=True, env={**os.environ, "WOTR_ROOT": str(c)}, cwd=c)
    print(f"  rust over the python's output: {r2.stdout.strip().splitlines()[-1].replace(str(py_out), '<OUT>')}")
    if "0 written, 1 unchanged" not in r2.stdout:
        fail("the Rust did not see the Python render as unchanged (manifest hash)")
    p, r, _, _ = run_both(c, ["--scene", scene, "--wav", "--first", "4", "--voice", "narrator-low", "--speed", "0.9"], S / "wav/py", S / "wav/rs")
    a, b = sorted((S / "wav/py").rglob("*.wav")), sorted((S / "wav/rs").rglob("*.wav"))
    if not a or not b or a[0].read_bytes() != b[0].read_bytes():
        fail(f"--wav --first 4: {a} vs {b}")
    else:
        print(f"  --wav --first 4, a blended preset at 0.9: WAV identical ({a[0].stat().st_size:,} bytes)")


SITE = '''import os, sys
if "wotr-supertonic" in sys.executable and os.environ.get("WOTR_SUPERTONIC_SEED"):
    import numpy
    numpy.random.seed(int(os.environ["WOTR_SUPERTONIC_SEED"]))
'''


def check_say(c: Path) -> None:
    """--say on a Supertonic voice, both seeded: the backend's cue tags, the resample to 24 kHz, the
    read-back check (faster-whisper) and soundfile's PCM_16 rounding."""
    text = "The ford ran brown with the thaw. [laugh] Ha! You call that a sword?"
    e = {**os.environ, "WOTR_ROOT": str(c), "WOTR_SUPERTONIC_SEED": "3"}
    args = ["--say", text, "--voice", "narrator-st"]
    subprocess.run([str(PY), str(c / "build/audio_export.py"), *args, "--wav-out", str(S / "say_py.wav")], capture_output=True, env={**e, "PYTHONPATH": str(S / "site")}, cwd=c)
    subprocess.run([str(BIN), "audio", *args, "--wav-out", str(S / "say_rs.wav")], capture_output=True, env=e, cwd=c)
    a, b = (S / "say_py.wav").read_bytes(), (S / "say_rs.wav").read_bytes()
    if a != b:
        fail(f"--say on Supertonic: WAVs differ ({len(a)} vs {len(b)} bytes)")
    else:
        print(f"--say on a Supertonic voice (seeded, read-back on): WAV identical ({len(a):,} bytes)")


def check_gpu(c: Path) -> None:
    scene = c / "scenes/naiser_and_seradris_the_courtyard.md"
    paras = A.plain_text(A.scene_blocks(scene.read_text(encoding="utf-8"))).split("\n\n")
    tagged = []
    for i, t in enumerate(paras):
        if 1 <= i <= 6 and t.strip() != "---":
            t = {1: "[Gimbzo: slow] [sigh] ", 2: "[narrator-st] [laugh] ", 3: "[Gimbzo] ", 4: "[narrator-st: quiet, beat] ",
                 5: "[Hild] ", 6: "[narrator-st] "}[i] + t
        tagged.append(t)
    (c / "scenes/cast").mkdir(exist_ok=True)
    (c / f"scenes/cast/{scene.stem}.cast.md").write_text("\n\n".join(tagged), encoding="utf-8")
    p, r, _, _ = run_both(c, ["--check-cast"], S / "x", S / "x")
    if (p.stdout, p.returncode) != (r.stdout, r.returncode) or "speakers:" not in p.stdout:
        fail(f"--check-cast differs:\n{p.stdout}\n---\n{r.stdout}")
    else:
        print(f"--check-cast: identical ({p.stdout.strip().splitlines()[-1].strip()})")
    venvs = S / "venvs"
    (venvs / "wotr-cb-gpu/bin").mkdir(parents=True)
    for v in ("wotr", "wotr-supertonic"):
        (venvs / v).symlink_to(HOME / ".venvs" / v)
    shim = venvs / "wotr-cb-gpu/bin/python"
    shim.write_text(f'#!/bin/sh\ntee -a "$CB_LOG" | exec {HOME}/.venvs/wotr-cb-gpu/bin/python "$@"\n')
    shim.chmod(0o755)
    logs = {}
    outs = {"py": S / "gpu/py", "rs": S / "gpu/rs"}
    e = {**os.environ, "WOTR_ROOT": str(c), "WOTR_VENVS": str(venvs), "WOTR_SUPERTONIC_SEED": "11"}
    t = {}
    for side in ("py", "rs"):
        e["CB_LOG"] = str(S / f"cb_{side}.jsonl")
        t0 = time.time()
        cmd = [str(PY), str(c / "build/audio_export.py")] if side == "py" else [str(BIN), "audio"]
        extra = {"PYTHONPATH": str(S / "site")} if side == "py" else {}
        logs[side] = subprocess.run(cmd + ["--scene", scene.name, "--first", "7", "--out", str(outs[side])], capture_output=True, text=True, env={**e, **extra}, cwd=c)
        t[side] = time.time() - t0
    print(f"cast file, narrator + Supertonic + Chatterbox (GPU), read-back on: python {t['py']:.0f} s, rust {t['rs']:.0f} s")
    for side in ("py", "rs"):
        if logs[side].returncode:
            fail(f"{side} exit {logs[side].returncode}:\n{logs[side].stdout}\n{logs[side].stderr[-2000:]}")
    reqs = {s: [json.loads(l) for l in (S / f"cb_{s}.jsonl").read_text().splitlines()] for s in ("py", "rs") if (S / f"cb_{s}.jsonl").exists()}
    first = {s: list(dict.fromkeys(json.dumps(r, sort_keys=True) for r in v)) for s, v in reqs.items()}
    raw = {s: (S / f"cb_{s}.jsonl").read_text() for s in reqs}
    if first.get("py") != first.get("rs") or not first.get("py"):
        fail(f"chatterbox requests differ:\n{raw.get('py')}\n---\n{raw.get('rs')}")
    else:
        same_bytes = raw["py"] == raw["rs"]
        print(f"  chatterbox worker requests: {len(first['py'])} distinct, identical (python sent {len(reqs['py'])}, rust {len(reqs['rs'])} with retakes; "
              f"byte-identical lines: {same_bytes})")
    lp, lr = (norm_log(logs[s].stdout, outs[s]) for s in ("py", "rs"))
    strip = lambda t: re.sub(r"read-back check:[\s\S]*?(?=\naudio:)", "<read-back report>", t)  # noqa: E731
    if strip(lp) != strip(lr):
        fail(f"logs differ:\n{lp}\n---\n{lr}")
    else:
        print("  logs identical (the read-back report aside, which depends on Chatterbox's takes):")
        print("    " + lr.replace("\n", "\n    "))
    a, b = sorted(outs["py"].rglob("*.mp3")), sorted(outs["rs"].rglob("*.mp3"))
    if a and b:
        print(f"  MP3s: {a[0].stat().st_size:,} vs {b[0].stat().st_size:,} bytes (Chatterbox takes differ between runs)")


FAKE_CURL = r'''#!PY
import json, math, os, sys, struct
cfg = {}
for line in sys.stdin.read().splitlines():
    k, _, v = line.partition("=")
    v = v.strip()
    cfg[k.strip()] = json.loads(v) if v.startswith('"') else v
url = cfg["url"].replace("https://api.elevenlabs.io/v1", "")
body = json.loads(open(cfg["data-binary"][1:]).read()) if "data-binary" in cfg else None
with open(os.environ["EL_LOG"], "a") as f:
    f.write(json.dumps([cfg.get("request"), url, body]) + "\n")
if url == "/voices":
    data = json.dumps({"voices": [{"voice_id": "JBFqnCBsd6RMkjVDRZzb", "name": "George - Warm, Captivating Storyteller", "category": "premade"}]}).encode()
else:
    n = 2400 + 37 * len(body["text"])
    data = b"".join(struct.pack("<h", int(8000 * math.sin(i / 9))) for i in range(n))
open(cfg["output"], "wb").write(data)
sys.stdout.write("200")
'''

EL_DRIVER = r'''
import json, math, os, struct, sys
sys.path.insert(0, os.path.join(sys.argv[1], "build"))
import elevenlabs_backend as E, audio_export as A
def fake(method, path, body=None, raw=False, tries=4):
    with open(os.environ["EL_LOG"], "a") as f:
        f.write(json.dumps([method, path, body]) + "\n")
    if path == "/voices":
        return {"voices": [{"voice_id": "JBFqnCBsd6RMkjVDRZzb", "name": "George - Warm, Captivating Storyteller", "category": "premade"}]}
    n = 2400 + 37 * len(body["text"])
    return b"".join(struct.pack("<h", int(8000 * math.sin(i / 9))) for i in range(n))
E._call = fake
sys.argv = ["audio_export.py"] + sys.argv[2:]
sys.exit(A.main())
'''


def check_eleven(c: Path) -> None:
    stubs = S / "stubs"
    stubs.mkdir()
    (stubs / "curl").write_text(FAKE_CURL.replace("#!PY", f"#!{PY}"))
    (stubs / "curl").chmod(0o755)
    (c / "scenes/cast").mkdir(exist_ok=True)
    args = ["--scene", "naiser_and_seradris_the_courtyard.md", "--first", "3", "--engine", "elevenlabs", "--no-cast"]
    e = {**os.environ, "WOTR_ROOT": str(c), "ELEVENLABS_API_KEY": "test-key-not-real"}
    p = subprocess.run([str(PY), "-c", EL_DRIVER, str(c), *args, "--out", str(S / "el/py")], capture_output=True, text=True, env={**e, "EL_LOG": str(S / "el_py.jsonl")}, cwd=c)
    r = subprocess.run([str(BIN), "audio", *args, "--out", str(S / "el/rs")], capture_output=True, text=True,
                       env={**e, "EL_LOG": str(S / "el_rs.jsonl"), "PATH": f"{stubs}:{os.environ['PATH']}"}, cwd=c)
    lp, lr = ((S / f"el_{s}.jsonl").read_text() if (S / f"el_{s}.jsonl").exists() else "" for s in ("py", "rs"))
    a, b = sorted((S / "el/py").rglob("*.mp3")), sorted((S / "el/rs").rglob("*.mp3"))
    if lp != lr or not lp:
        fail(f"elevenlabs requests differ:\n{lp}\n---\n{lr}\n{p.stderr[-800:]}\n{r.stderr[-800:]}")
    elif not a or not b or a[0].read_bytes() != b[0].read_bytes():
        fail(f"elevenlabs MP3s differ: {a} {b}")
    elif norm_log(p.stdout, S / "el/py") != norm_log(r.stdout, S / "el/rs"):
        fail(f"elevenlabs logs differ:\n{p.stdout}\n---\n{r.stdout}")
    else:
        print(f"elevenlabs (faked): {len(lp.splitlines())} requests identical, MP3 identical, log identical")


def main() -> int:
    if S.exists():
        shutil.rmtree(S)
    S.mkdir(parents=True)
    probe = Probe()
    check_phonemes(probe)
    check_kokoro(probe)
    probe.close()
    check_supertonic()
    (S / "site").mkdir()
    (S / "site/sitecustomize.py").write_text(SITE)  # seeds the Python's Supertonic worker as WOTR_SUPERTONIC_SEED seeds the Rust
    c = clone()
    check_e2e(c)
    check_say(c)
    check_eleven(c)
    check_gpu(c)
    print("ALL IDENTICAL" if not bad else f"{bad} difference(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
