#!/usr/bin/env python3
"""Narrate the scene archive with Kokoro, locally, in reading order.

  python build/audio_export.py --fetch-model            # once: the model files (~350 MB) into build/models/
  python build/audio_export.py --fetch-model --pack zh  # the v1.1-zh pack too: 100 Mandarin voices + af_maple, af_sol, bf_vale (~380 MB)
  python build/audio_export.py --list-voices            # the voices the model carries
  python build/audio_export.py --scene 02_verinus_testament_of_the_sixty_fifth.md --voice af_heart
  python build/audio_export.py --out "$WOTR_DRIVE/War of the Realms — Documents/Arcs/Audio" --max-minutes 20   # the Drive mount; docs/audio when there is none

One MP3 per scene, grouped by arc (scenes/ARCS.md order), skipping scenes whose
text, voice and lexicon are unchanged since the last run (.manifest.json in the
output folder). The author-facing notes block at the foot of a scene is never
read. Names the engine would mangle are respelled from build/pronounce.json
before synthesis — add to it whenever a name comes out wrong.

Engine: kokoro-onnx (Kokoro 82M, Apache-2.0 weights) on the CPU by default (the
extras are requirements-audio.txt); a ROCm build of onnxruntime in place of
onnxruntime would put it on the AMD card, untested here.

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
throat] [sniff] [groan] [breath] — is performed by a Chatterbox Turbo speaker
(build/chatterbox_backend.py), the first three by a Supertonic speaker
(build/supertonic_backend.py), and silently dropped for a Kokoro one. The
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
CUES = {"laugh", "chuckle", "sigh", "gasp", "cough", "clear throat", "sniff", "groan", "shush", "breath"}
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
                 exaggeration: float = 0.5, cfg: float = 0.5, model: str = "turbo", pack: str = "v1.0", steps: int = 8):
        self.name, self.engine, self.style, self.pack = name, engine, style, pack
        self.speed, self.gain, self.ref, self.exaggeration, self.cfg, self.model = speed, gain, ref, exaggeration, cfg, model
        self.steps = steps      # Supertonic only: flow-matching steps, 5 rough … 12 best
        # Qwen only (build/qwen_backend.py): the brief, the approved take, tries per batch, and the exact shaping knobs
        self.instruct, self.anchor, self.tries, self.good_enough, self.batch = "", "", 1, 0.6, 8
        self.pitch_st, self.formant, self.range_factor, self.seed = 0.0, 1.0, 1.0, None
        self.temperature = self.top_k = self.top_p = self.repetition_penalty = self.subtalker_temperature = None
        self.portray: dict = {}     # single-narrator mode: how the narrator's voice is bent for this character (pitch_st, formant, speed, range_factor, gain)


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
        # single-narrator mode: one voice reads everything and portrays the characters (voices.yaml `_single: true`,
        # or --single); only meaningful when the narrator is on the Qwen engine
        self.single = bool(self.raw.get("_single", False)) or SINGLE["on"]

    def _build(self, name: str, entry) -> Speaker:
        if ELEVEN["on"]:
            sp = self._eleven(name, entry)
            if sp is not None:
                return sp
        sp = self._build_engine(name, entry)
        if isinstance(entry, dict) and isinstance(entry.get("portray"), dict):
            sp.portray = {k: float(v) for k, v in entry["portray"].items()}
        return sp

    def _eleven(self, name: str, entry) -> Speaker | None:
        """--engine elevenlabs: the speaker's line in `_elevenlabs:` (or their entry's own `eleven:`),
        else the map's `_default`; a speaker with neither keeps their local voice and is reported."""
        emap = self.raw.get("_elevenlabs") or {}
        spec = (entry.get("eleven") if isinstance(entry, dict) else None) or emap.get(name) or emap.get("_default")
        if not spec:
            ELEVEN["used"].append(f"{name} -> local (no _elevenlabs line, no _default)")
            return None
        settings = spec if isinstance(spec, dict) else {"voice_id": spec}
        sp = self._eleven_speaker(name, settings, emap)
        ELEVEN["used"].append(f"{name} -> {settings.get('voice_id')}" + ("" if name in emap or (isinstance(entry, dict) and entry.get("eleven")) else " (_default)"))
        return sp

    def _eleven_speaker(self, name: str, entry: dict, emap: dict | None = None) -> Speaker:
        from elevenlabs_backend import resolve_voice   # build/elevenlabs_backend.py
        sp = Speaker(name, "elevenlabs", None, float(entry.get("speed", 1.0)), float(entry.get("gain", 1.0)))
        sp.voice_id = resolve_voice(entry.get("voice_id") or entry.get("voice") or "")
        sp.model_id = str(entry.get("model") or (emap or {}).get("_model") or "")
        sp.stability, sp.similarity, sp.style_ex = float(entry.get("stability", 0.5)), float(entry.get("similarity", 0.75)), float(entry.get("style", 0.0))
        return sp

    def _build_engine(self, name: str, entry) -> Speaker:
        if isinstance(entry, str):
            style, pack = voice_style(self.engine, entry, self.presets)
            return Speaker(name, "kokoro", style, pack=pack)
        eng = str(entry.get("engine", "kokoro")).lower()
        if eng == "elevenlabs":
            return self._eleven_speaker(name, entry, self.raw.get("_elevenlabs") or {})
        if eng == "chatterbox":
            return Speaker(name, "chatterbox", None, float(entry.get("speed", 1.0)), float(entry.get("gain", 1.0)),
                           str(entry.get("ref", "")), float(entry.get("exaggeration", 0.5)), float(entry.get("cfg", 0.5)),
                           str(entry.get("model", "turbo")).lower())
        if eng == "supertonic":
            # voice: one of the ten presets (M1–M5, F1–F5); style: a voice-style JSON instead (build/supertonic_backend.py)
            return Speaker(name, "supertonic", str(entry.get("voice", "M1")).upper(), float(entry.get("speed", 1.0)),
                           float(entry.get("gain", 1.0)), str(entry.get("style", "")), steps=int(entry.get("steps", 8)))
        if eng == "qwen" and not QWEN["allowed"]:
            # Isaac, 13 Sep 2026: the design engine still drifts between takes — nobody gets it until it is fixed.
            # Only an explicit --qwen on the command line unlocks it; the MCP's narrate_scene never passes that.
            fb = entry.get("fallback")
            if fb and fb in self.raw and fb != name:
                QWEN["fallbacks"].append(f"{name} -> {fb}")
                return self._build(name, self.raw[fb])
            QWEN["fallbacks"].append(f"{name} -> pool")
            return self._pool_pick(name)
        if eng == "qwen":
            sp = Speaker(name, "qwen", None, float(entry.get("speed", 1.0)), float(entry.get("gain", 1.0)))
            sp.instruct = str(entry.get("instruct", "")).strip()
            if not sp.instruct or entry.get("instruct_from") == "casting":
                sp.instruct = casting_instruct(name) or sp.instruct
            if not sp.instruct:
                sys.exit(f"{name}: engine qwen needs an `instruct` (the voice brief) or a qwen_instruct in build/casting/{name}.json")
            sp.anchor = str(entry.get("anchor", ""))
            sp.tries, sp.good_enough, sp.batch = int(entry.get("tries", 3 if sp.anchor else 1)), float(entry.get("good_enough", 0.6)), int(entry.get("batch", 8))
            sp.pitch_st, sp.formant, sp.range_factor = float(entry.get("pitch_st", 0.0)), float(entry.get("formant", 1.0)), float(entry.get("range_factor", 1.0))
            sp.seed = entry.get("seed")
            for k in ("temperature", "top_k", "top_p", "repetition_penalty", "subtalker_temperature"):
                if k in entry:
                    setattr(sp, k, entry[k])
            return sp
        style, pack = voice_style(self.engine, str(entry.get("voice", "af_heart")), self.presets)
        return Speaker(name, "kokoro", style, float(entry.get("speed", 1.0)), float(entry.get("gain", 1.0)), pack=pack)

    def _pool_pick(self, who: str) -> Speaker:
        pick = self.pool[int(hashlib.sha256(who.encode("utf-8")).hexdigest(), 16) % len(self.pool)]
        style, pack = voice_style(self.engine, pick, self.presets)
        self.unassigned.append(f"{who} -> {pick}")
        return Speaker(who, "kokoro", style, pack=pack)

    def speaker(self, who: str) -> Speaker:
        if who not in self.speakers:
            if who in self.raw and not who.startswith("_"):
                self.speakers[who] = self._build(who, self.raw[who])
            else:
                sp = self._eleven(who, {}) if ELEVEN["on"] else None   # an unassigned speaker still gets the map's _default
                self.speakers[who] = sp or self._pool_pick(who)
        return self.speakers[who]


def casting_instruct(name: str) -> str:
    """The Qwen brief recorded on the character's casting sheet, build/casting/<Name>.json (qwen_instruct)."""
    p = ROOT / "build" / "casting" / (re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_") + ".json")
    if not p.exists():
        return ""
    try:
        return str(json.loads(p.read_text(encoding="utf-8")).get("qwen_instruct", "")).strip()
    except (OSError, ValueError):
        return ""


def shape_span(sp: Speaker, samples: np.ndarray, speed: float, portray: dict | None = None) -> np.ndarray:
    """Exact pace / pitch / body for engines without a knob (Qwen): build/voice_shape.py. In single-narrator
    mode `portray` (the character's entry) is composed on top of the narrator's own shaping."""
    if sp.engine != "qwen":
        return samples
    import voice_shape
    p = portray or {}
    return voice_shape.shape(samples, SAMPLE_RATE, speed=speed * p.get("speed", 1.0), pitch_st=sp.pitch_st + p.get("pitch_st", 0.0),
                             formant=sp.formant * p.get("formant", 1.0), range_factor=sp.range_factor * p.get("range_factor", 1.0))


CHECK = {"on": True, "threshold": 0.25, "retakes": 0, "worst": []}   # read-back check for generative spans
QWEN = {"allowed": False, "fallbacks": []}     # the design engine is off unless --qwen is given on the command line
SINGLE = {"on": False}                          # --single: one narrator voice reads every span and portrays the characters
ELEVEN = {"on": False, "used": []}              # --engine elevenlabs: every speaker goes through voices.yaml's _elevenlabs map


def read_back(sp: Speaker, text: str, samples: np.ndarray, retake) -> np.ndarray:
    """The read-back check on a generative take: transcribe, and if too many words are wrong,
    take it again with `retake()` and keep whichever reads back better."""
    if not CHECK["on"]:
        return samples
    import audio_check
    score, heard = audio_check.wer(text, samples)
    if score > CHECK["threshold"]:
        again = retake()
        score2, heard2 = audio_check.wer(text, again)
        CHECK["retakes"] += 1
        if score2 < score:
            samples, score, heard = again, score2, heard2
    if score > CHECK["threshold"]:
        CHECK["worst"].append((score, sp.name, text[:90], heard[:90]))
    return samples


def render_span(cast: Cast, sp: Speaker, text: str, speed: float, mods: list[str] | None = None) -> np.ndarray:
    if sp.engine == "elevenlabs":
        from elevenlabs_backend import synth as eleven_synth   # build/elevenlabs_backend.py
        return eleven_synth(cast, sp, strip_cues(text), speed)
    if sp.engine == "qwen":
        from qwen_backend import synth as qwen_synth   # build/qwen_backend.py
        samples = qwen_synth(cast, sp, text, speed, mods)
        samples = read_back(sp, strip_cues(text), samples, lambda: qwen_synth(cast, sp, text, speed, mods))
        return shape_span(sp, samples, speed)
    if sp.engine in ("chatterbox", "supertonic"):
        if sp.engine == "chatterbox":
            from chatterbox_backend import synth as gen_synth   # build/chatterbox_backend.py
            if sp.model != "turbo":
                text = strip_cues(text)
        else:
            from supertonic_backend import synth as gen_synth   # build/supertonic_backend.py
        samples = gen_synth(cast, sp, text, speed)
        # both engines sample, so a second take differs — keep whichever reads back better
        return read_back(sp, text, samples, lambda: gen_synth(cast, sp, text, speed))
    samples, sr = cast.engine.get(sp.pack).create(strip_cues(text), voice=sp.style, speed=speed, lang="en-us")
    assert sr == SAMPLE_RATE, sr
    return samples.astype(np.float32)


def synth_scene(engine, cast: Cast, blocks, speed: float, lexicon, script=None) -> np.ndarray:
    """One voice for the whole scene, or — with a cast script — a voice per tagged span,
    each span rendered at its speaker's pace and level, adjusted by the tag's delivery words."""
    out = []
    if script is None:
        script = [(kind, [("narrator", text, [])]) for kind, text in blocks]
    pre = qwen_prepass(cast, script, speed, lexicon)
    for bi, (kind, spans) in enumerate(script):
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
            samples = pre.get((bi, i))
            if samples is None:
                samples = render_span(cast, sp, respell(text, lexicon), sp_speed, mods)
            if gain != 1.0:
                samples = np.clip(samples * gain, -1.0, 1.0)
            out.append(samples)
        out.append(silence(TITLE_PAUSE if kind == "title" else PARA_PAUSE))
    return np.concatenate(out) if out else silence(0.1)


JOIN_CHARS = 900        # a joined take: about a minute of speech; the fast worker's static cache holds ~170 s


def _ends_sentence(t: str) -> str:
    return t if re.search(r"[.!?…\"'”’)]\s*$", t) else t + "."


def qwen_prepass(cast: Cast, script, speed: float, lexicon) -> dict:
    """Qwen draws a fresh voice every call but cannot change voice inside one, so a speaker's
    consecutive spans (same direction, no cue) are joined into ONE take of up to JOIN_CHARS,
    spoken once — best-of-N against the anchor, where a minute of audio scores reliably — then cut
    back into spans by word alignment (build/audio_align.py). A scene of 50 lines becomes a
    handful of draws, and the voice cannot wander between the lines of a take. Spans with a cue,
    a whisper, or a different direction get their own take. Results are handed back to
    synth_scene by (block, span) index, each span shaped afterwards."""
    single = cast.single and cast.speaker("narrator").engine == "qwen"
    rows = []                                          # (bi, i, text, mods, who) in scene order
    for bi, (kind, spans) in enumerate(script):
        if kind == "divider":
            continue
        for i, (who, text, mods) in enumerate(spans):
            sp = cast.speaker(who)
            if sp.engine != "qwen" and not single:
                continue
            rows.append((bi, i, respell(text, lexicon), list(mods), who))
    if not rows:
        return {}
    import qwen_backend as Q
    import audio_align
    # group: a speaker's spans in scene order, same instruct (direction), no exemption, up to JOIN_CHARS per take —
    # whatever other speakers say in between; each piece goes back to its own place afterwards.
    # Single-narrator mode: EVERY span in scene order, one voice, one brief; delivery tags become shaping only,
    # so a take is never broken by a tag, and the dialogue is read in its context like a real narrator reads it.
    takes: list[list] = []
    open_take: dict[tuple, list] = {}
    for bi, i, text, mods, who in rows:
        sp = cast.speaker("narrator") if single else cast.speaker(who)
        instruct, clean, exempt = Q.instruct_for(sp, [] if single else mods, text if not single else strip_cues(text))
        if single:
            exempt = False
        item = (bi, i, text, mods, who, clean, instruct, exempt)
        key = ("*", instruct) if single else (who, instruct)
        cur = None if exempt else open_take.get(key)
        if cur is not None and sum(len(r[5]) + 1 for r in cur) + len(clean) <= JOIN_CHARS:
            cur.append(item)
        else:
            takes.append([item])
            if not exempt:
                open_take[key] = takes[-1]
    done = {}
    for take in takes:
        instruct, exempt = take[0][6], take[0][7]
        gen = cast.speaker("narrator") if single else cast.speaker(take[0][4])
        texts = [_ends_sentence(r[5]) for r in take]
        joined = " ".join(texts)
        x = Q.synth_lines(gen, [joined], instruct, [exempt])[0]
        x = read_back(gen, joined, x, lambda: Q.synth_lines(gen, [joined], instruct, [exempt])[0])
        pieces = audio_align.split(x, SAMPLE_RATE, texts) if len(take) > 1 else [x]
        for (bi, i, text, mods, who, *_), piece in zip(take, pieces):
            sp_speed = speed * gen.speed
            for w in mods:
                sp_speed *= DELIVERY[w][0]
            portray = cast.speaker(who).portray if single and who != "narrator" else None
            done[(bi, i)] = shape_span(gen, piece, sp_speed, portray)
    Q.REPORT["takes"] = Q.REPORT.get("takes", 0) + len(takes)
    return done


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
    ap.add_argument("--no-check", action="store_true", help="skip the read-back check on Chatterbox spans (build/audio_check.py)")
    ap.add_argument("--first", type=int, default=0, metavar="N", help="render only the first N paragraphs of each scene (an audition cut; output named *-first<N>)")
    ap.add_argument("--qwen", action="store_true", help="unlock the Qwen design engine (it still drifts between takes; off for everyone until fixed — "
                                                        "speakers on it fall back to their `fallback:` entry or a pool voice)")
    ap.add_argument("--engine", default="local", choices=["local", "elevenlabs"],
                    help="elevenlabs: every speaker through voices.yaml's _elevenlabs map (build/elevenlabs_backend.py; costs characters); output named *-eleven")
    ap.add_argument("--list-eleven", action="store_true", help="list the ElevenLabs workspace voices and stop")
    ap.add_argument("--single", action="store_true", help="single-narrator mode: --voice reads every span and portrays the characters (their `portray:` shaping)")
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
    CHECK["on"] = not a.no_check
    QWEN["allowed"] = bool(a.qwen)
    SINGLE["on"] = bool(a.single)
    ELEVEN["on"] = a.engine == "elevenlabs"
    if a.list_eleven:
        from elevenlabs_backend import list_voices
        for v in list_voices():
            print(f"  {v['voice_id']}  {v['name']}  ({v['category']})")
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
        if a.first:
            blocks = blocks[:a.first]
            script = script[:a.first] if script else None
            key += f"-first{a.first}"
        if ELEVEN["on"]:
            key += "-eleven"
        voices_hash = hashlib.sha256(json.dumps(load_voices_yaml(), sort_keys=True, default=str).encode()).hexdigest()[:8]
        h = hashlib.sha256((json.dumps(blocks) + json.dumps(script) + a.voice + str(a.speed) + lex_hash + voices_hash + a.engine).encode("utf-8")).hexdigest()[:16]
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
        if "qwen_backend" in sys.modules or any(cast_voices.speaker(s).engine == "qwen" for s in (speakers(script) if script else ["narrator"])):
            import qwen_backend
            qwen_backend.CONTEXT = key
        samples = synth_scene(engine, cast_voices, blocks, a.speed, lexicon, script)
        path = write_audio(samples, target, mp3=not a.wav)
        manifest[key] = h
        man_p.write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
        mins = len(samples) / SAMPLE_RATE / 60
        voices_note = f", {len(speakers(script))} voices" if script else ""
        print(f"  {path.name}: {words:,} words -> {mins:.1f} min audio in {time.time()-t0:.0f}s{voices_note}", flush=True)
        written += 1
    if ELEVEN["used"]:
        print("elevenlabs voices: " + "; ".join(sorted(set(ELEVEN["used"]))))
    if QWEN["fallbacks"]:
        print("qwen engine is locked (--qwen unlocks it); these speakers used their fallback: " + "; ".join(sorted(set(QWEN["fallbacks"]))))
    if cast_voices.unassigned:
        print("speakers with no entry in build/voices.yaml, given a pool voice: " + "; ".join(sorted(set(cast_voices.unassigned))))
    if CHECK["retakes"] or CHECK["worst"]:
        print(f"read-back check: {CHECK['retakes']} span(s) re-taken; {len(CHECK['worst'])} still above {CHECK['threshold']:.0%} word error:")
        for score, who, text, heard in sorted(CHECK["worst"], reverse=True)[:8]:
            print(f"  {score:.0%} {who}: {text!r} -> heard {heard!r}")
    if "qwen_backend" in sys.modules:
        R = sys.modules["qwen_backend"].REPORT
        if R["lines"]:
            print(f"qwen: {R.get('takes', R['lines'])} take(s), {R['draws']} draws; {len(R['low'])} below 0.40 similarity to the anchor" + (":" if R["low"] else ""))
            for c, who, text in sorted(R["low"])[:8]:
                print(f"  {c:.2f} {who}: {text!r}")
    print(f"audio: {written} written, {skipped} unchanged -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
