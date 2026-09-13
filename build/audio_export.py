#!/usr/bin/env python3
"""Narrate the scene archive with Kokoro, locally, in reading order.

  python build/audio_export.py --fetch-model            # once: the model files (~350 MB) into build/models/
  python build/audio_export.py --fetch-model --pack zh  # the v1.1-zh pack too: 100 Mandarin voices + af_maple, af_sol, bf_vale (~380 MB)
  python build/audio_export.py --list-voices            # the voices the model carries
  python build/audio_export.py --scene 02_verinus_testament_of_the_sixty_fifth.md --voice af_heart
  python build/audio_export.py --out "G:/My Drive/War of the Realms — Documents/Arcs/Audio" --max-minutes 20

One MP3 per scene, grouped by arc (scenes/ARCS.md order), skipping scenes whose
text, voice and lexicon are unchanged since the last run (.manifest.json in the
output folder). The author-facing notes block at the foot of a scene is never
read. Names the engine would mangle are respelled from build/pronounce.json
before synthesis — add to it whenever a name comes out wrong.

Engine: kokoro-onnx (Kokoro 82M, Apache-2.0 weights) on the CPU by default; with
onnxruntime-directml installed in place of onnxruntime it runs on the AMD card.

Voices, --voice:
  af_heart                        one of the model's 54 built-in voices (--list-voices)
  af_heart:0.6,bm_george:0.4      a blend, weights optional
  narrator / Verinus / ...        a preset from build/voices.yaml (name: spec), presets may blend presets
  gravel                          a custom style vector build/voices/gravel.npy — a community-made Kokoro
                                  voice (a [510, 1, 256] float32 array; a .pt from the Kokoro hub converts
                                  with torch.load(...).numpy()); .npz files are read by their first key

Many voices in one scene: a speaker-tagged script at scenes/cast/<scene stem>.cast.md.
It is the scene's cleaned text (what --dry-run --plain prints) with [Name] tags
inserted wherever the voice changes; untagged text is the narrator's. A
paragraph can switch voices mid-line:

    He did not look up. [Aurelian] "You will not say that again." [narrator] The door closed on it.

Each speaker's voice comes from build/voices.yaml (Aurelian: bm_george, or a
mapping with voice / speed / gain); a speaker with no entry gets a stable pick
from the file's _pool list. A tag can carry delivery for that one span, after a
colon: [Verinus: slow] [Aurelian: quiet, beat] — slow / slower / fast / faster
(pace), quiet / loud / whisper (level), beat / long beat (a pause before the
line). A cue inside a line — [sigh] [laugh] [chuckle] [gasp] [cough] [clear
throat] [sniff] [groan] — is performed by a Chatterbox Turbo speaker
(build/chatterbox_backend.py) and silently dropped for a Kokoro one. The
tagged text minus its tags must match the scene exactly (--check-cast says
where it does not), so a cast file can never drop or add words. --no-cast
ignores it.
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SCENES = ROOT / "scenes"
MODELS = ROOT / "build" / "models"
LEXICON = ROOT / "build" / "pronounce.json"

sys.path.insert(0, str(ROOT / "build"))
import docs_export as D  # noqa: E402
from arcs_export import read_arcs, scene_title  # noqa: E402

SAMPLE_RATE = 24000
PARA_PAUSE = 0.55       # seconds of silence between paragraphs
DIVIDER_PAUSE = 1.4     # at a --- section break
TITLE_PAUSE = 1.0       # after the scene title


# ---------------------------------------------------------------- text prep

def load_lexicon() -> dict[str, str]:
    if not LEXICON.exists():
        return {}
    data = json.loads(LEXICON.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def respell(text: str, lexicon: dict[str, str]) -> str:
    """Whole-word, case-sensitive; a possessive or plural tail survives."""
    for name in sorted(lexicon, key=len, reverse=True):
        text = re.sub(rf"(?<![\w-]){re.escape(name)}(?=[\w'’-]*)", lexicon[name], text)
    return text


def scene_blocks(md: str) -> list[tuple[str, str]]:
    """The scene as a list of (kind, text): 'title', 'para', 'divider'.

    Everything from the author-facing notes heading on is dropped, as are the
    scene's frontmatter and any markdown that is not prose.
    """
    md, _ = D.strip_frontmatter(md)
    md = md.replace("\r\n", "\n")
    cut = re.search(r"(?m)^##\s+Notes\b.*$|^##\s+Author.*$|^---\s*\n\s*\*?Author", md)
    if cut:
        md = md[: cut.start()]
    blocks: list[tuple[str, str]] = []
    for raw in re.split(r"\n\s*\n", md):
        b = raw.strip()
        if not b:
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", b):
            blocks.append(("divider", ""))
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", b)
        if h:
            kind = "title" if len(h.group(1)) == 1 and not any(k == "title" for k, _ in blocks) else "para"
            blocks.append((kind, clean_inline(h.group(2))))
            continue
        if b.startswith(">"):
            b = " ".join(l.lstrip("> ").strip() for l in b.split("\n"))
        if re.match(r"^[-*]\s", b):
            b = " ".join(re.sub(r"^[-*]\s+", "", l.strip()) for l in b.split("\n") if l.strip())
        text = clean_inline(b.replace("\n", " "))
        if text:
            blocks.append(("para", text))
    return blocks


def clean_inline(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)           # images
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)        # links -> text
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", s)   # *italic* (thought is read plainly)
    s = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"\1", s)
    s = s.replace("⁂", "").replace("§", "section ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ---------------------------------------------------------------- cast scripts

CAST_DIR = SCENES / "cast"
TAG = re.compile(r"\[([^\[\]\n]{1,80})\]")
SPAN_PAUSE = 0.12       # between two voices inside one paragraph

# Delivery words allowed after the colon in a tag: (speed factor, gain factor, pause before, seconds)
DELIVERY = {
    "slow": (0.9, 1.0, 0.0), "slower": (0.8, 1.0, 0.0), "fast": (1.1, 1.0, 0.0), "faster": (1.2, 1.0, 0.0),
    "quiet": (1.0, 0.7, 0.0), "loud": (1.0, 1.3, 0.0), "whisper": (0.95, 0.5, 0.0),
    "urgent": (1.12, 1.15, 0.0),          # a fight, a chase: quicker and harder, for the narrator too
    "beat": (1.0, 1.0, 0.6), "long beat": (1.0, 1.0, 1.3),
}

# Cues a Chatterbox Turbo speaker performs when they sit inside the line ([sigh] "No."); they
# never change the speaker. A Kokoro speaker cannot perform them, so they are dropped there.
CUES = {"laugh", "chuckle", "sigh", "gasp", "cough", "clear throat", "sniff", "groan", "shush"}
CUE_RE = re.compile(r"\s*\[(" + "|".join(re.escape(c) for c in sorted(CUES, key=len, reverse=True)) + r")\]\s*", re.I)


def parse_tag(inner: str) -> tuple[str, list[str]]:
    """'Verinus: slow, beat' -> ('Verinus', ['slow', 'beat']); unknown words are an error."""
    who, _, mods = inner.partition(":")
    words = [w.strip().lower() for w in mods.split(",") if w.strip()]
    for w in words:
        if w not in DELIVERY:
            sys.exit(f"unknown delivery word {w!r} in tag [{inner}]; known: {', '.join(DELIVERY)}")
    return who.strip(), words


def strip_cues(text: str) -> str:
    return _norm(CUE_RE.sub(" ", text))


def cast_path(scene: Path) -> Path:
    return CAST_DIR / f"{scene.stem}.cast.md"


def plain_text(blocks) -> str:
    """The scene as the cast format without tags: title line, paragraphs, --- dividers."""
    out = []
    for kind, text in blocks:
        out.append("---" if kind == "divider" else (f"# {text}" if kind == "title" else text))
    return "\n\n".join(out) + "\n"


def parse_cast(text: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """Cast file -> [(kind, [(who, text), ...])]; kind is title / para / divider."""
    blocks = []
    for raw in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        b = raw.strip()
        if not b:
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", b):
            blocks.append(("divider", []))
            continue
        kind = "para"
        if b.startswith("# "):
            kind, b = "title", b[2:].strip()
        b = re.sub(r"\s+", " ", b)
        spans, who, mods, pos = [], "narrator", [], 0
        for m in TAG.finditer(b):
            if m.group(1).strip().lower() in CUES:
                continue                      # a performed cue stays in the span's text
            chunk = b[pos:m.start()].strip()
            if chunk:
                spans.append((who, chunk, mods))
            (who, mods), pos = parse_tag(m.group(1)), m.end()
        chunk = b[pos:].strip()
        if chunk:
            spans.append((who, chunk, mods))
        blocks.append((kind, spans))
    return blocks


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def check_cast(scene_blocks_, cast_blocks) -> str | None:
    """None when the cast text (tags removed) is the scene text; else a message saying where they part."""
    want = _norm(" ".join(t for k, t in scene_blocks_ if k != "divider"))
    got = _norm(" ".join(strip_cues(s[1]) for k, spans in cast_blocks if k != "divider" for s in spans))
    if want == got:
        n_scene = sum(1 for k, _ in scene_blocks_ if k == "divider")
        n_cast = sum(1 for k, _ in cast_blocks if k == "divider")
        if n_scene != n_cast:
            return f"the scene has {n_scene} --- dividers, the cast file {n_cast}"
        return None
    i = next((i for i, (a, b) in enumerate(zip(want, got)) if a != b), min(len(want), len(got)))
    return (f"cast text parts from the scene at character {i}:\n  scene: …{want[max(0,i-60):i+80]}…\n"
            f"  cast:  …{got[max(0,i-60):i+80]}…")


def load_cast(scene: Path, scene_blocks_) -> list[tuple[str, list[tuple[str, str]]]] | None:
    p = cast_path(scene)
    if not p.exists():
        return None
    cast = parse_cast(p.read_text(encoding="utf-8"))
    problem = check_cast(scene_blocks_, cast)
    if problem:
        sys.exit(f"{p.name}: {problem}\n(fix the cast file, or run with --no-cast)")
    return cast


def speakers(cast) -> list[str]:
    seen = []
    for _, spans in cast:
        for s in spans:
            if s[0] not in seen:
                seen.append(s[0])
    return seen


# ---------------------------------------------------------------- synthesis

PACKS = {                       # name -> (model file, voices file); a voice is "zh/af_maple" for the second pack
    "v1.0": ("kokoro-v1.0.onnx", "voices-v1.0.bin"),
    "zh": ("kokoro-v1.1-zh.onnx", "voices-v1.1-zh.bin"),   # Kokoro v1.1-zh: 100 Mandarin voices + af_maple, af_sol, bf_vale
}


class Engines:
    """The Kokoro model(s), loaded on first use per pack."""

    def __init__(self):
        self._loaded = {}

    def get(self, pack: str = "v1.0"):
        if pack not in self._loaded:
            try:
                from kokoro_onnx import Kokoro
            except ImportError:
                sys.exit("kokoro-onnx is not installed: pip install kokoro-onnx soundfile lameenc")
            model, voices = (MODELS / f for f in PACKS[pack])
            if not (model.exists() and voices.exists()):
                sys.exit(f"model files for pack {pack!r} missing in {MODELS}: run with --fetch-model" + (" --pack zh" if pack == "zh" else ""))
            self._loaded[pack] = Kokoro(str(model), str(voices))
        return self._loaded[pack]

    def voices(self) -> list[str]:
        out = list(self.get("v1.0").get_voices())
        if all((MODELS / f).exists() for f in PACKS["zh"]):
            out += ["zh/" + v for v in self.get("zh").get_voices()]
        return out


def load_engine():
    return Engines()


VOICES_DIR = ROOT / "build" / "voices"
PRESETS = ROOT / "build" / "voices.yaml"


def load_voices_yaml() -> dict:
    if not PRESETS.exists():
        return {}
    import yaml
    return yaml.safe_load(PRESETS.read_text(encoding="utf-8")) or {}


def load_presets() -> dict[str, str]:
    return {str(k): str(v) for k, v in load_voices_yaml().items() if not str(k).startswith("_")}


def _single_style(engines: Engines, name: str, presets: dict[str, str], depth: int = 0):
    """One term of a voice spec -> (style, pack): a preset, a custom .npy/.npz in build/voices/, or a built-in
    ("zh/af_maple" names a voice of the v1.1-zh pack)."""
    name = name.strip()
    if depth > 8:
        sys.exit(f"voice preset loop at {name!r}")
    if name in presets:
        return voice_style(engines, presets[name], presets, depth + 1)
    for ext in (".npy", ".npz"):
        p = VOICES_DIR / f"{name}{ext}"
        if p.exists():
            arr = np.load(p)
            if ext == ".npz":
                arr = arr[list(arr.keys())[0]]
            return np.asarray(arr, dtype=np.float32), "v1.0"
    pack, _, bare = name.partition("/") if "/" in name else ("v1.0", "", name)
    if pack not in PACKS:
        sys.exit(f"unknown voice pack {pack!r} in {name!r}; packs: {', '.join(PACKS)}")
    try:
        return engines.get(pack).get_voice_style(bare), pack
    except Exception:
        known = ", ".join(sorted(presets)) or "none"
        sys.exit(f"unknown voice {name!r}: not a built-in (--list-voices), a preset ({known}), or a file in {VOICES_DIR}")


def voice_style(engines: Engines, spec: str, presets: dict[str, str] | None = None, depth: int = 0):
    """A voice spec resolved to (style array, pack): term[:weight][,term[:weight]...]; blends stay inside one pack."""
    presets = load_presets() if presets is None else presets
    parts, total, packs = [], 0.0, set()
    for item in spec.split(","):
        name, _, w = item.partition(":")
        w = float(w or 1.0)
        style, pack = _single_style(engines, name, presets, depth)
        parts.append((style, w)); packs.add(pack)
        total += w
    if len(packs) > 1:
        sys.exit(f"voice blend {spec!r} mixes packs {sorted(packs)}; a blend must stay inside one pack")
    if len(parts) == 1:
        return parts[0][0], packs.pop()
    return sum(style * (w / total) for style, w in parts), packs.pop()


def silence(seconds: float):
    return np.zeros(int(SAMPLE_RATE * seconds), dtype=np.float32)


DEFAULT_POOL = ["am_michael", "bf_emma", "am_fenrir", "af_sarah", "bm_lewis", "af_nicole", "am_eric", "bf_alice"]


class Speaker:
    """How one speaker is rendered: which engine (and Chatterbox model), which voice, and their habitual pace and level."""

    def __init__(self, name: str, engine: str, style, speed: float = 1.0, gain: float = 1.0, ref: str = "",
                 exaggeration: float = 0.5, cfg: float = 0.5, model: str = "turbo", pack: str = "v1.0"):
        self.name, self.engine, self.style, self.pack = name, engine, style, pack
        self.speed, self.gain, self.ref, self.exaggeration, self.cfg, self.model = speed, gain, ref, exaggeration, cfg, model


class Cast:
    """Resolves a speaker name to a Speaker: the narrator's --voice, a voices.yaml entry (a voice
    spec string, or a mapping with voice / speed / gain / engine / ref), or a stable pick from
    the pool for a speaker nobody has assigned yet."""

    def __init__(self, engine, narrator_spec: str):
        self.engine = engine
        self.raw = load_voices_yaml()
        self.presets = {k: v for k, v in self.raw.items() if not str(k).startswith("_") and isinstance(v, str)}
        pool = self.raw.get("_pool") or DEFAULT_POOL
        self.pool = [v.strip() for v in pool.split(",")] if isinstance(pool, str) else [str(v) for v in pool]
        # --voice may name a voices.yaml entry (a string or a mapping, e.g. a Chatterbox narrator) or be a bare spec
        self.speakers = {"narrator": self._build("narrator", self.raw.get(narrator_spec, narrator_spec))}
        self.unassigned: list[str] = []
        self.chatterbox = None

    def _build(self, name: str, entry) -> Speaker:
        if isinstance(entry, str):
            style, pack = voice_style(self.engine, entry, self.presets)
            return Speaker(name, "kokoro", style, pack=pack)
        eng = str(entry.get("engine", "kokoro")).lower()
        if eng == "chatterbox":
            return Speaker(name, "chatterbox", None, float(entry.get("speed", 1.0)), float(entry.get("gain", 1.0)),
                           str(entry.get("ref", "")), float(entry.get("exaggeration", 0.5)), float(entry.get("cfg", 0.5)),
                           str(entry.get("model", "turbo")).lower())
        style, pack = voice_style(self.engine, str(entry.get("voice", "af_heart")), self.presets)
        return Speaker(name, "kokoro", style, float(entry.get("speed", 1.0)), float(entry.get("gain", 1.0)), pack=pack)

    def speaker(self, who: str) -> Speaker:
        if who not in self.speakers:
            if who in self.raw and not who.startswith("_"):
                self.speakers[who] = self._build(who, self.raw[who])
            else:
                pick = self.pool[int(hashlib.sha256(who.encode("utf-8")).hexdigest(), 16) % len(self.pool)]
                style, pack = voice_style(self.engine, pick, self.presets)
                self.speakers[who] = Speaker(who, "kokoro", style, pack=pack)
                self.unassigned.append(f"{who} -> {pick}")
        return self.speakers[who]


def render_span(cast: Cast, sp: Speaker, text: str, speed: float) -> np.ndarray:
    if sp.engine == "chatterbox":
        from chatterbox_backend import synth as cb_synth   # build/chatterbox_backend.py
        if sp.model != "turbo":
            text = strip_cues(text)
        return cb_synth(cast, sp, text, speed)
    samples, sr = cast.engine.get(sp.pack).create(strip_cues(text), voice=sp.style, speed=speed, lang="en-us")
    assert sr == SAMPLE_RATE, sr
    return samples.astype(np.float32)


def synth_scene(engine, cast: Cast, blocks, speed: float, lexicon, script=None) -> np.ndarray:
    """One voice for the whole scene, or — with a cast script — a voice per tagged span,
    each span rendered at its speaker's pace and level, adjusted by the tag's delivery words."""
    out = []
    if script is None:
        script = [(kind, [("narrator", text, [])]) for kind, text in blocks]
    for kind, spans in script:
        if kind == "divider":
            out.append(silence(DIVIDER_PAUSE))
            continue
        for i, (who, text, mods) in enumerate(spans):
            sp = cast.speaker(who)
            sp_speed, gain, pause = speed * sp.speed, sp.gain, 0.0
            for w in mods:
                f_speed, f_gain, p = DELIVERY[w]
                sp_speed, gain, pause = sp_speed * f_speed, gain * f_gain, max(pause, p)
            if i or pause:
                out.append(silence(max(SPAN_PAUSE if i else 0.0, pause)))
            samples = render_span(cast, sp, respell(text, lexicon), sp_speed)
            if gain != 1.0:
                samples = np.clip(samples * gain, -1.0, 1.0)
            out.append(samples)
        out.append(silence(TITLE_PAUSE if kind == "title" else PARA_PAUSE))
    return np.concatenate(out) if out else silence(0.1)


def write_audio(samples: np.ndarray, path: Path, mp3: bool) -> Path:
    import soundfile as sf
    if not mp3:
        sf.write(str(path.with_suffix(".wav")), samples, SAMPLE_RATE)
        return path.with_suffix(".wav")
    try:
        import lameenc
    except ImportError:
        sf.write(str(path.with_suffix(".wav")), samples, SAMPLE_RATE)
        print("  (lameenc not installed; wrote WAV)")
        return path.with_suffix(".wav")
    pcm = np.clip(samples, -1.0, 1.0)
    pcm = (pcm * 32767).astype(np.int16).tobytes()
    enc = lameenc.Encoder()
    enc.set_bit_rate(96)
    enc.set_in_sample_rate(SAMPLE_RATE)
    enc.set_channels(1)
    enc.set_quality(2)
    data = enc.encode(pcm) + enc.flush()
    path.with_suffix(".mp3").write_bytes(data)
    return path.with_suffix(".mp3")


# ---------------------------------------------------------------- model files

def fetch_model(pack: str = "v1.0") -> None:
    MODELS.mkdir(parents=True, exist_ok=True)
    release = {"v1.0": "model-files-v1.0", "zh": "model-files-v1.1"}[pack]
    for name in PACKS[pack]:
        dest = MODELS / name
        if dest.exists() and dest.stat().st_size > 1_000_000:
            print(f"  {name}: already here ({dest.stat().st_size:,} bytes)")
            continue
        url = f"https://github.com/thewh1teagle/kokoro-onnx/releases/download/{release}/{name}"
        print(f"  fetching {url}")
        with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
            total, t0 = 0, time.time()
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
                total += len(chunk)
            print(f"  {name}: {total:,} bytes in {time.time()-t0:.0f}s")


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "docs" / "audio"))
    ap.add_argument("--voice", default="narrator", help="built-in voice, preset, custom file, or 'a:0.6,b:0.4' blend")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--scene", action="append", help="only this scene file (repeatable)")
    ap.add_argument("--max-minutes", type=float, default=0, help="stop starting new scenes after this long")
    ap.add_argument("--wav", action="store_true", help="write WAV instead of MP3")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="show the cleaned text, synthesize nothing")
    ap.add_argument("--plain", action="store_true", help="with --dry-run: print the cast-file format (tag it, save as scenes/cast/<stem>.cast.md)")
    ap.add_argument("--check-cast", action="store_true", help="validate the cast files of the selected scenes and list their speakers")
    ap.add_argument("--no-cast", action="store_true", help="ignore cast files; one narrator voice")
    ap.add_argument("--fetch-model", action="store_true")
    ap.add_argument("--pack", default="v1.0", choices=list(PACKS), help="with --fetch-model: which Kokoro pack (zh = v1.1-zh, 103 more voices)")
    ap.add_argument("--list-voices", action="store_true")
    ap.add_argument("--say", help="render this text with --voice to --wav-out and stop (a voice test, or a reference clip for Chatterbox)")
    ap.add_argument("--wav-out", default=str(ROOT / "docs" / "audio" / "say.wav"))
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if a.fetch_model:
        fetch_model(a.pack)
        return 0
    if a.say:
        import soundfile as sf
        engine = load_engine()
        cast = Cast(engine, a.voice)
        samples = render_span(cast, cast.speaker("narrator"), respell(a.say, load_lexicon()), a.speed * cast.speaker("narrator").speed)
        out = Path(a.wav_out); out.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(out), samples, SAMPLE_RATE, subtype="PCM_16")
        print(f"  {out}: {len(samples)/SAMPLE_RATE:.1f}s, voice {a.voice}")
        return 0

    lexicon = load_lexicon()
    arcs = read_arcs()
    filed = {p.name for _, ps in arcs for p in ps}
    unfiled = [p for p in sorted(SCENES.glob("*.md")) if p.name not in filed
               and "SUPERSEDED" not in p.name.upper() and p.name not in ("MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md")]
    if unfiled:
        arcs.append(("Unfiled", unfiled))
    # number every scene from the full reading order, then narrow to --scene if asked, so a
    # scene keeps the same "03-07" prefix whether rendered alone or in the batch
    numbered = [(ai, name, si, p) for ai, (name, files) in enumerate(arcs, 1) for si, p in enumerate(files, 1)]
    if a.scene:
        wanted = {Path(s).name for s in a.scene}
        known = {p.name for _, _, _, p in numbered}
        for w in wanted - known:
            print(f"  no such scene: {w}")
        numbered = [x for x in numbered if x[3].name in wanted]
    arcs = []
    for ai, name, si, p in numbered:
        if not arcs or arcs[-1][0] != name:
            arcs.append((name, []))
        arcs[-1][1].append(p)

    if a.dry_run:
        for name, files in arcs:
            for p in files:
                blocks = scene_blocks(p.read_text(encoding="utf-8", errors="replace"))
                if a.plain:
                    print(plain_text(blocks), end="")
                    continue
                print(f"=== {name} / {p.name}")
                for kind, text in blocks:
                    print(f"[{kind}] {respell(text, lexicon)[:160]}")
        return 0

    if a.check_cast:
        bad = 0
        for name, files in arcs:
            for p in files:
                cp = cast_path(p)
                if not cp.exists():
                    continue
                blocks = scene_blocks(p.read_text(encoding="utf-8", errors="replace"))
                cast = parse_cast(cp.read_text(encoding="utf-8"))
                problem = check_cast(blocks, cast)
                print(f"{cp.name}: {'ok' if not problem else problem}")
                if not problem:
                    assigned = {str(k) for k in load_voices_yaml() if not str(k).startswith("_")}
                    print("  speakers: " + ", ".join(f"{s}{'' if s == 'narrator' or s in assigned else ' (no voice assigned)'}" for s in speakers(cast)))
                bad += bool(problem)
        return 1 if bad else 0

    engine = load_engine()
    if a.list_voices:
        for v in engine.voices():
            print(" ", v)
        return 0
    cast_voices = Cast(engine, a.voice)

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    man_p = out / ".manifest.json"
    manifest = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    lex_hash = hashlib.sha256(json.dumps(lexicon, sort_keys=True).encode()).hexdigest()[:8]

    t_start = time.time()
    written = skipped = 0
    for ai, name, si, p in numbered:
        folder = out / f"{ai:02d} {D.safe_name(name)}"
        md = p.read_text(encoding="utf-8", errors="replace")
        blocks = scene_blocks(md)
        script = None if a.no_cast else load_cast(p, blocks)
        key = f"{ai:02d}-{si:02d} {D.safe_name(scene_title(p, md))}"
        voices_hash = hashlib.sha256(json.dumps(load_voices_yaml(), sort_keys=True, default=str).encode()).hexdigest()[:8]
        h = hashlib.sha256((json.dumps(blocks) + json.dumps(script) + a.voice + str(a.speed) + lex_hash + voices_hash).encode("utf-8")).hexdigest()[:16]
        target = folder / key
        ext = ".wav" if a.wav else ".mp3"
        if not a.force and manifest.get(key) == h and target.with_suffix(ext).exists():
            skipped += 1
            continue
        if a.max_minutes and (time.time() - t_start) / 60 > a.max_minutes:
            print(f"  time budget reached; {key} and later left for next run")
            man_p.write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
            return 0
        folder.mkdir(parents=True, exist_ok=True)
        words = sum(len(t.split()) for _, t in blocks)
        t0 = time.time()
        samples = synth_scene(engine, cast_voices, blocks, a.speed, lexicon, script)
        path = write_audio(samples, target, mp3=not a.wav)
        manifest[key] = h
        man_p.write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
        mins = len(samples) / SAMPLE_RATE / 60
        voices_note = f", {len(speakers(script))} voices" if script else ""
        print(f"  {path.name}: {words:,} words -> {mins:.1f} min audio in {time.time()-t0:.0f}s{voices_note}", flush=True)
        written += 1
    if cast_voices.unassigned:
        print("speakers with no entry in build/voices.yaml, given a pool voice: " + "; ".join(sorted(set(cast_voices.unassigned))))
    print(f"audio: {written} written, {skipped} unchanged -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
