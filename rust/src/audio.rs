//! build/audio_export.py ported: `wotr-mcp audio ...` takes its arguments and writes the same files
//! (one MP3 per scene by arc, .manifest.json skipping unchanged scenes, the cast files' voices).
//! Kokoro and Supertonic run here (kokoro.rs, supertonic.rs); Chatterbox stays the Python GPU worker
//! (build/chatterbox_worker.py, same venv, same JSON lines), the read-back check stays faster-whisper
//! (build/audio_check.py in a small worker), MP3s are encoded by the LAME inside the venv's lameenc,
//! and ElevenLabs goes through curl. --qwen runs build/audio_export.py itself: the Qwen engine's
//! takes are joined and cut by Whisper alignment and shaped by Praat (audio_align, voice_shape).
//! rust/audio_parity.py checks it against the Python.
use crate::analysis::{name_of, py_repr, scene_blocks};
use crate::kokoro::{self, py_strip, SAMPLE_RATE};
use crate::util::{self, read_lossy, root, ROOT};
use crate::{pyjson, pyyaml};
use fancy_regex::Regex;
use serde_json::{json, Map, Value};
use std::collections::HashMap;
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};
use std::process::{Child, ChildStdin, ChildStdout, Stdio};
use std::rc::Rc;
use std::sync::LazyLock;
use std::time::Instant;

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

const PARA_PAUSE: f64 = 0.55;
const DIVIDER_PAUSE: f64 = 1.4;
const TITLE_PAUSE: f64 = 1.0;
const SPAN_PAUSE: f64 = 0.12;
/// delivery word -> (speed factor, gain factor, pause before)
const DELIVERY: [(&str, f64, f64, f64); 10] = [
    ("slow", 0.9, 1.0, 0.0), ("slower", 0.8, 1.0, 0.0), ("fast", 1.1, 1.0, 0.0), ("faster", 1.2, 1.0, 0.0),
    ("quiet", 1.0, 0.7, 0.0), ("loud", 1.0, 1.3, 0.0), ("whisper", 0.95, 0.5, 0.0), ("urgent", 1.12, 1.15, 0.0),
    ("beat", 1.0, 1.0, 0.6), ("long beat", 1.0, 1.0, 1.3),
];
const CUES: [&str; 10] = ["laugh", "chuckle", "sigh", "gasp", "cough", "clear throat", "sniff", "groan", "shush", "breath"];
const PACKS: [(&str, &str, &str); 2] = [("v1.0", "kokoro-v1.0.onnx", "voices-v1.0.bin"), ("zh", "kokoro-v1.1-zh.onnx", "voices-v1.1-zh.bin")];
const DEFAULT_POOL: [&str; 8] = ["am_michael", "bf_emma", "am_fenrir", "af_sarah", "bm_lewis", "af_nicole", "am_eric", "bf_alice"];
const THRESHOLD: f64 = 0.25;

// ---------------------------------------------------------------- cast scripts

/// (who, text, delivery words)
pub type Span = (String, String, Vec<String>);
pub type Block = (&'static str, Vec<Span>);

fn norm(s: &str) -> String {
    rx!(r"\s+").replace_all(s, " ").trim().to_string()
}

/// audio_export.parse_tag: who and the delivery words; an unknown word is the SystemExit text.
fn parse_tag(inner: &str) -> Result<(String, Vec<String>), String> {
    let (who, mods) = inner.split_once(':').unwrap_or((inner, ""));
    let words: Vec<String> = mods.split(',').map(|w| w.trim().to_lowercase()).filter(|w| !w.is_empty()).collect();
    for w in &words {
        if !DELIVERY.iter().any(|d| d.0 == w) {
            let known: Vec<&str> = DELIVERY.iter().map(|d| d.0).collect();
            return Err(format!("unknown delivery word {} in tag [{inner}]; known: {}", py_repr(w), known.join(", ")));
        }
    }
    Ok((who.trim().to_string(), words))
}

/// audio_export.parse_cast: [(kind, [(who, text, mods)])]
pub fn parse_cast(text: &str) -> Result<Vec<Block>, String> {
    let text = text.replace("\r\n", "\n");
    let mut blocks = Vec::new();
    for raw in rx!(r"\n\s*\n").split(&text).flatten() {
        let b = raw.trim();
        if b.is_empty() {
            continue;
        }
        if rx!(r"^(-{3,}|\*{3,}|_{3,})\z").is_match(b).unwrap_or(false) {
            blocks.push(("divider", vec![]));
            continue;
        }
        let (kind, b) = match b.strip_prefix("# ") {
            Some(r) => ("title", r.trim()),
            None => ("para", b),
        };
        let b = rx!(r"\s+").replace_all(b, " ").into_owned();
        let (mut spans, mut who, mut mods, mut pos) = (Vec::new(), "narrator".to_string(), vec![], 0);
        for m in rx!(r"\[([^\[\]\n]{1,80})\]").captures_iter(b.as_str()).flatten() {
            let (all, inner) = (m.get(0).unwrap(), &m[1]);
            if CUES.contains(&inner.trim().to_lowercase().as_str()) {
                continue; // a performed cue stays in the span's text
            }
            let chunk = b[pos..all.start()].trim();
            if !chunk.is_empty() {
                spans.push((who.clone(), chunk.to_string(), mods.clone()));
            }
            (who, mods) = parse_tag(inner)?;
            pos = all.end();
        }
        let chunk = b[pos..].trim();
        if !chunk.is_empty() {
            spans.push((who, chunk.to_string(), mods));
        }
        blocks.push((kind, spans));
    }
    Ok(blocks)
}

fn strip_cues(text: &str) -> String {
    norm(&rx!(r"(?i)\s*\[(clear throat|chuckle|laugh|cough|groan|shush|breath|sniff|sigh|gasp)\]\s*").replace_all(text, " "))
}

/// audio_export.check_cast: None when the cast text, tags removed, is the scene's.
pub fn check_cast(scene: &[(&'static str, String)], cast: &[Block]) -> Option<String> {
    let want = norm(&scene.iter().filter(|(k, _)| *k != "divider").map(|(_, t)| t.as_str()).collect::<Vec<_>>().join(" "));
    let got = norm(&cast.iter().filter(|(k, _)| *k != "divider").flat_map(|(_, sp)| sp.iter().map(|s| strip_cues(&s.1))).collect::<Vec<_>>().join(" "));
    if want == got {
        let (ns, nc) = (scene.iter().filter(|(k, _)| *k == "divider").count(), cast.iter().filter(|(k, _)| *k == "divider").count());
        return (ns != nc).then(|| format!("the scene has {ns} --- dividers, the cast file {nc}"));
    }
    let (w, g): (Vec<char>, Vec<char>) = (want.chars().collect(), got.chars().collect());
    let i = w.iter().zip(&g).position(|(a, b)| a != b).unwrap_or(w.len().min(g.len()));
    let cut = |v: &[char]| v[i.saturating_sub(60).min(v.len())..(i + 80).min(v.len())].iter().collect::<String>();
    Some(format!("cast text parts from the scene at character {i}:\n  scene: \u{2026}{}\u{2026}\n  cast:  \u{2026}{}\u{2026}", cut(&w), cut(&g)))
}

/// audio_export.speakers: who speaks, in order of first appearance.
pub fn speakers(cast: &[Block]) -> Vec<String> {
    let mut seen: Vec<String> = Vec::new();
    for s in cast.iter().flat_map(|(_, sp)| sp) {
        if !seen.contains(&s.0) {
            seen.push(s.0.clone());
        }
    }
    seen
}

fn cast_path(scene: &Path) -> PathBuf {
    root("scenes/cast").join(format!("{}.cast.md", util::stem(scene)))
}

// ---------------------------------------------------------------- small Python equivalents

fn sha256_hex(data: &[u8]) -> String {
    const K: [u32; 64] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ];
    let mut h: [u32; 8] = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
    let mut msg = data.to_vec();
    msg.push(0x80);
    while msg.len() % 64 != 56 {
        msg.push(0);
    }
    msg.extend(((data.len() as u64) * 8).to_be_bytes());
    for chunk in msg.chunks(64) {
        let mut w = [0u32; 64];
        for i in 0..64 {
            w[i] = if i < 16 {
                u32::from_be_bytes(chunk[4 * i..4 * i + 4].try_into().unwrap())
            } else {
                let (a, b) = (w[i - 15], w[i - 2]);
                w[i - 16].wrapping_add(a.rotate_right(7) ^ a.rotate_right(18) ^ (a >> 3)).wrapping_add(w[i - 7]).wrapping_add(b.rotate_right(17) ^ b.rotate_right(19) ^ (b >> 10))
            };
        }
        let mut v = h;
        for i in 0..64 {
            let (a, e) = (v[0], v[4]);
            let t1 = v[7].wrapping_add(e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25)).wrapping_add((e & v[5]) ^ (!e & v[6])).wrapping_add(K[i]).wrapping_add(w[i]);
            let t2 = (a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22)).wrapping_add((a & v[1]) ^ (a & v[2]) ^ (v[1] & v[2]));
            v = [t1.wrapping_add(t2), a, v[1], v[2], v[3].wrapping_add(t1), e, v[5], v[6]];
        }
        for (x, y) in h.iter_mut().zip(v) {
            *x = x.wrapping_add(y);
        }
    }
    h.iter().map(|x| format!("{x:08x}")).collect()
}

/// str(v) for a YAML value
fn py_str(v: &Value) -> String {
    match v {
        Value::String(s) => s.clone(),
        Value::Bool(b) => if *b { "True" } else { "False" }.into(),
        Value::Null => "None".into(),
        Value::Number(n) if n.is_f64() => format!("{:?}", n.as_f64().unwrap()),
        o => o.to_string(),
    }
}

/// float(x): a number, or a string Python's float() reads
fn py_float(v: &Value) -> Result<f64, String> {
    match v {
        Value::Number(n) => Ok(n.as_f64().unwrap_or(0.0)),
        Value::Bool(b) => Ok(f64::from(u8::from(*b))),
        Value::String(s) => parse_float(s),
        o => Err(format!("TypeError: float() argument must be a string or a real number, not {}", if o.is_null() { "'NoneType'" } else { "'dict'" })),
    }
}

fn parse_float(s: &str) -> Result<f64, String> {
    py_strip(s).replace('_', "").parse().map_err(|_| format!("ValueError: could not convert string to float: {}", py_repr(s)))
}

fn py_int(v: &Value) -> Result<i64, String> {
    match v {
        Value::Number(n) => Ok(n.as_i64().unwrap_or_else(|| n.as_f64().unwrap_or(0.0).trunc() as i64)),
        Value::Bool(b) => Ok(i64::from(*b)),
        Value::String(s) => py_strip(s).parse().map_err(|_| format!("ValueError: invalid literal for int() with base 10: {}", py_repr(s))),
        _ => Err("TypeError: int() argument must be a string, a bytes-like object or a real number".into()),
    }
}

fn entry<'a>(e: &'a Value, k: &str) -> Option<&'a Value> {
    e.get(k).filter(|_| e.is_object())
}

/// Python truthiness of an optional YAML value
fn truthy(v: Option<&Value>) -> bool {
    match v {
        None | Some(Value::Null) => false,
        Some(Value::Bool(b)) => *b,
        Some(Value::String(s)) => !s.is_empty(),
        Some(Value::Number(n)) => n.as_f64() != Some(0.0),
        Some(Value::Array(a)) => !a.is_empty(),
        Some(Value::Object(o)) => !o.is_empty(),
    }
}

fn silence(seconds: f64) -> Vec<f32> {
    vec![0f32; (SAMPLE_RATE as f64 * seconds) as usize]
}

/// np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
fn interp(x: &[f32], n: usize) -> Vec<f32> {
    if x.is_empty() {
        return vec![];
    }
    let stop = (x.len() - 1) as f64;
    let step = if n > 1 { stop / (n - 1) as f64 } else { 0.0 };
    (0..n).map(|i| {
        let xv = if n > 1 && i == n - 1 { stop } else { i as f64 * step };
        let j = xv.floor() as usize;
        if j >= x.len() - 1 || j as f64 == xv {
            x[j.min(x.len() - 1)]
        } else {
            let (a, b) = (x[j] as f64, x[j + 1] as f64);
            ((b - a) * (xv - j as f64) + a) as f32
        }
    }).collect()
}

/// the backends' _resample to 24 kHz
fn resample(x: Vec<f32>, sr: usize) -> Vec<f32> {
    if sr == SAMPLE_RATE { x } else { interp(&x, (x.len() as f64 * SAMPLE_RATE as f64 / sr as f64) as usize) }
}

fn tail_chars(p: &Path, n: usize) -> String {
    util::tail(&read_lossy(p), n).to_string()
}

/// pathlib's with_suffix on a name that may hold dots ("01-02 St. Mary" -> "01-02 St.mp3")
fn with_suffix(p: &Path, ext: &str) -> PathBuf {
    let name = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let stem = match name.rfind('.') {
        Some(i) if i > 0 && i < name.len() - 1 => &name[..i],
        _ => &name,
    };
    p.with_file_name(format!("{stem}{ext}"))
}

/// docs_export.safe_name
fn safe_name(s: &str) -> String {
    util::head(rx!(r#"[\\/:*?"<>|]+"#).replace_all(s, "").trim(), 120).to_string()
}

/// arcs_export.scene_title
fn scene_title(p: &Path, md: &str) -> String {
    match rx!(r"(?m)^#\s+(.+?)\s*$").captures(md).ok().flatten() {
        Some(m) => m[1].trim().trim_matches('*').to_string(),
        None => util::stem(p).replace('_', " "),
    }
}

/// arcs_export.read_arcs
fn read_arcs() -> Result<Vec<(String, Vec<PathBuf>)>, String> {
    let p = root("scenes/ARCS.md");
    let text = std::fs::read_to_string(&p).map_err(|_| format!("FileNotFoundError: [Errno 2] No such file or directory: {}", py_repr(&p.to_string_lossy())))?;
    let mut arcs: Vec<(String, Vec<PathBuf>)> = Vec::new();
    for ln in text.split('\n') {
        if let Some(h) = rx!(r"^##\s+(.+)$").captures(ln).ok().flatten() {
            arcs.push((py_strip(&h[1]).to_string(), vec![]));
            continue;
        }
        if let Some(m) = rx!(r"^-\s+(\S+\.md)\s*$").captures(py_strip(ln)).ok().flatten() {
            let f = root("scenes").join(&m[1]);
            if let (Some(cur), true) = (arcs.last_mut(), f.exists()) {
                cur.1.push(f);
            }
        }
    }
    arcs.retain(|a| !a.1.is_empty());
    Ok(arcs)
}

fn load_voices_yaml() -> Result<Value, String> {
    let p = root("build/voices.yaml");
    if !p.exists() {
        return Ok(json!({}));
    }
    let v = pyyaml::load(&read_lossy(&p))?;
    Ok(if v.is_null() { json!({}) } else { v })
}

fn load_lexicon() -> Result<Vec<(String, String)>, String> {
    let p = root("build/pronounce.json");
    if !p.exists() {
        return Ok(vec![]);
    }
    let v = pyjson::loads(&read_lossy(&p))?;
    Ok(v.as_object().map(|m| m.iter().filter(|(k, _)| !k.starts_with('_')).map(|(k, v)| (k.clone(), py_str(v))).collect()).unwrap_or_default())
}

/// audio_export.respell: whole-word at the start, case-sensitive, longest names first.
struct Lexicon(Vec<(Regex, String)>);

impl Lexicon {
    fn new(lex: &[(String, String)]) -> Lexicon {
        let mut names: Vec<&(String, String)> = lex.iter().collect();
        names.sort_by_key(|(k, _)| std::cmp::Reverse(k.chars().count()));
        Lexicon(names.into_iter().map(|(k, v)| (Regex::new(&format!(r"(?<![\w-]){}(?=[\w'’-]*)", fancy_regex::escape(k))).unwrap(), v.clone())).collect())
    }

    fn respell(&self, text: &str) -> String {
        let mut t = text.to_string();
        for (re, v) in &self.0 {
            t = re.replace_all(&t, fancy_regex::NoExpand(v)).into_owned();
        }
        t
    }
}

// ---------------------------------------------------------------- the Python workers

/// A long-lived interpreter answering one JSON line per request line, as the backends drive theirs.
struct Worker {
    _child: Child,
    stdin: ChildStdin,
    out: BufReader<ChildStdout>,
    log: Option<PathBuf>,
    label: &'static str,
}

impl Worker {
    fn start(label: &'static str, py: &Path, args: &[&str], log: Option<PathBuf>) -> Result<Worker, String> {
        let mut c = util::command(py);
        c.args(args).stdin(Stdio::piped()).stdout(Stdio::piped());
        if let Some(log) = &log {
            let mut f = std::fs::OpenOptions::new().create(true).append(true).open(log).map_err(|e| e.to_string())?;
            let _ = write!(f, "\n=== worker start {}\n", py.display());
            c.stderr(f);
        }
        let mut child = c.spawn().map_err(|e| format!("{}: {e}", py.display()))?;
        let (stdin, out) = (child.stdin.take().unwrap(), BufReader::new(child.stdout.take().unwrap()));
        Ok(Worker { _child: child, stdin, out, log, label })
    }

    /// The first reply that is not a "loaded" notice (printed with `loaded`'s prefix).
    fn ask(&mut self, req: &Value, loaded: &str) -> Result<Map<String, Value>, String> {
        let died = |w: &mut Worker| {
            let code = w._child.try_wait().ok().flatten().and_then(|s| s.code()).map_or("None".into(), |c| c.to_string());
            match &w.log {
                Some(l) => format!("the {} worker died (exit {code}); the end of its log, {}:\n{}", w.label, name_of(l), tail_chars(l, 1500)),
                None => format!("the {} worker died (exit {code})", w.label),
            }
        };
        if writeln!(self.stdin, "{}", pyjson::dumps(req, false)).and_then(|_| self.stdin.flush()).is_err() {
            return Err(died(self));
        }
        loop {
            let mut line = String::new();
            if self.out.read_line(&mut line).unwrap_or(0) == 0 {
                return Err(died(self));
            }
            let Ok(Value::Object(msg)) = serde_json::from_str::<Value>(&line) else { continue };
            if let Some(l) = msg.get("loaded") {
                println!("  {loaded}{}", py_str(l));
                continue;
            }
            return Ok(msg);
        }
    }
}

/// np.load of a worker's .npy reply, which the backend then deletes.
fn take_npy(msg: &Map<String, Value>) -> Result<Vec<f32>, String> {
    let p = PathBuf::from(py_str(&msg["path"]));
    let x = crate::embed::npy_f32(&std::fs::read(&p).map_err(|e| format!("FileNotFoundError: {e}: {}", p.display()))?)?;
    let _ = std::fs::remove_file(&p);
    let sr = msg.get("sr").and_then(Value::as_u64).unwrap_or(SAMPLE_RATE as u64) as usize;
    Ok(resample(x, sr))
}

fn worker_error(engine: &str, msg: &Map<String, Value>) -> Option<String> {
    let e = msg.get("error")?;
    let where_: Vec<String> = msg.get("where").and_then(Value::as_array).map(|a| a.iter().map(py_str).collect()).unwrap_or_default();
    Some(format!("{engine}: {}\n  {}", py_str(e), where_.join("\n  ")))
}

/// build/audio_check.wer in the wotr venv: faster-whisper, which has no Rust equivalent.
const READBACK: &str = r#"
import json, sys
import numpy as np
sys.path.insert(0, "build")
import audio_check
out, sys.stdout = sys.stdout, sys.stderr
for line in sys.stdin:
    req = json.loads(line)
    try:
        score, heard = audio_check.wer(req["text"], np.fromfile(req["path"], dtype="<f4"))
        rep = {"score": repr(score), "heard": heard}
    except Exception:
        import traceback
        rep = {"error": traceback.format_exc()}
    out.write(json.dumps(rep) + "\n")
    out.flush()
"#;

// ---------------------------------------------------------------- speakers

/// How one speaker is rendered (audio_export.Speaker).
struct Speaker {
    name: String,
    engine: &'static str,
    style: Vec<f32>,
    pack: String,
    voice: String,
    speed: f64,
    gain: f64,
    ref_: String,
    exaggeration: f64,
    cfg: f64,
    model: String,
    steps: i64,
    voice_id: String,
    model_id: String,
    stability: f64,
    similarity: f64,
    style_ex: f64,
}

impl Speaker {
    fn new(name: &str, engine: &'static str) -> Speaker {
        Speaker {
            name: name.into(), engine, style: vec![], pack: "v1.0".into(), voice: String::new(), speed: 1.0, gain: 1.0, ref_: String::new(),
            exaggeration: 0.5, cfg: 0.5, model: "turbo".into(), steps: 8, voice_id: String::new(), model_id: String::new(),
            stability: 0.5, similarity: 0.75, style_ex: 0.0,
        }
    }
}

struct Opts {
    out: String,
    voice: String,
    speed: f64,
    scene: Vec<String>,
    max_minutes: f64,
    wav: bool,
    force: bool,
    dry_run: bool,
    plain: bool,
    check_cast: bool,
    no_cast: bool,
    no_check: bool,
    first: usize,
    qwen: bool,
    engine: String,
    list_eleven: bool,
    single: bool,
    fetch_model: bool,
    pack: String,
    list_voices: bool,
    say: Option<String>,
    wav_out: String,
}

/// The renderer: the loaded engines, the cast (audio_export.Cast) and the run's reports.
struct Narrator {
    kokoro: HashMap<String, kokoro::Model>,
    supertonic: Option<crate::supertonic::Tts>,
    raw: Value,
    presets: HashMap<String, String>,
    pool: Vec<String>,
    speakers: HashMap<String, Rc<Speaker>>,
    unassigned: Vec<String>,
    fallbacks: Vec<String>,
    eleven: bool,
    eleven_used: Vec<String>,
    eleven_names: Option<Vec<(String, String)>>,
    check: bool,
    retakes: usize,
    worst: Vec<(f64, String, String, String)>,
    chatterbox: Option<Worker>,
    readback: Option<Worker>,
}

fn voices_dir() -> PathBuf {
    root("build/voices")
}

impl Narrator {
    fn new(narrator_spec: &str, eleven: bool, check: bool) -> Result<Narrator, String> {
        let raw = load_voices_yaml()?;
        let obj = raw.as_object().cloned().unwrap_or_default();
        let presets = obj.iter().filter(|(k, v)| !k.starts_with('_') && v.is_string()).map(|(k, v)| (k.clone(), py_str(v))).collect();
        let pool = match obj.get("_pool").filter(|p| truthy(Some(p))) {
            Some(Value::String(s)) => s.split(',').map(|v| py_strip(v).to_string()).collect(),
            Some(Value::Array(a)) => a.iter().map(py_str).collect(),
            _ => DEFAULT_POOL.iter().map(|s| s.to_string()).collect(),
        };
        let mut n = Narrator {
            kokoro: HashMap::new(), supertonic: None, raw, presets, pool, speakers: HashMap::new(), unassigned: vec![], fallbacks: vec![],
            eleven, eleven_used: vec![], eleven_names: None, check, retakes: 0, worst: vec![], chatterbox: None, readback: None,
        };
        // --voice may name a voices.yaml entry (a string or a mapping) or be a bare spec
        let e = obj.get(narrator_spec).cloned().unwrap_or_else(|| Value::String(narrator_spec.into()));
        let sp = n.build("narrator", &e)?;
        n.speakers.insert("narrator".into(), Rc::new(sp));
        Ok(n)
    }

    fn kokoro(&mut self, pack: &str) -> Result<&mut kokoro::Model, String> {
        if !self.kokoro.contains_key(pack) {
            if util::site_packages("wotr").is_none_or(|d| !d.join("kokoro_onnx").is_dir()) {
                return Err("kokoro-onnx is not installed: pip install kokoro-onnx soundfile lameenc".into());
            }
            let (_, m, v) = PACKS.iter().find(|p| p.0 == pack).unwrap();
            let (model, voices) = (root("build/models").join(m), root("build/models").join(v));
            if !(model.exists() && voices.exists()) {
                return Err(format!("model files for pack {} missing in {}: run with --fetch-model{}", py_repr(pack), root("build/models").display(), if pack == "zh" { " --pack zh" } else { "" }));
            }
            self.kokoro.insert(pack.into(), kokoro::Model::load(&model, &voices)?);
        }
        Ok(self.kokoro.get_mut(pack).unwrap())
    }

    /// audio_export._single_style: a preset, a custom .npy/.npz in build/voices/, or a built-in.
    fn single_style(&mut self, name: &str, depth: usize) -> Result<(Vec<f32>, String), String> {
        let name = py_strip(name);
        if depth > 8 {
            return Err(format!("voice preset loop at {}", py_repr(name)));
        }
        if let Some(spec) = self.presets.get(name).cloned() {
            return self.voice_style(&spec, depth + 1);
        }
        for ext in [".npy", ".npz"] {
            let p = voices_dir().join(format!("{name}{ext}"));
            if p.exists() {
                let arr = if ext == ".npz" {
                    kokoro::load_npz(&p)?.into_iter().next().map(|(_, a)| a).unwrap_or_default()
                } else {
                    crate::embed::npy_f32(&std::fs::read(&p).map_err(|e| e.to_string())?)?
                };
                return Ok((arr, "v1.0".into()));
            }
        }
        let (pack, bare) = name.split_once('/').unwrap_or(("v1.0", name));
        if !PACKS.iter().any(|p| p.0 == pack) {
            return Err(format!("unknown voice pack {} in {}; packs: v1.0, zh", py_repr(pack), py_repr(name)));
        }
        match self.kokoro(pack)?.voices.get(bare) {
            Some(s) => Ok((s.clone(), pack.into())),
            None => {
                let mut known: Vec<&String> = self.presets.keys().collect();
                known.sort();
                let known = if known.is_empty() { "none".into() } else { known.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", ") };
                Err(format!("unknown voice {}: not a built-in (--list-voices), a preset ({known}), or a file in {}", py_repr(name), voices_dir().display()))
            }
        }
    }

    /// audio_export.voice_style: term[:weight][,term[:weight]...]; blends stay inside one pack.
    fn voice_style(&mut self, spec: &str, depth: usize) -> Result<(Vec<f32>, String), String> {
        let (mut parts, mut total, mut packs) = (Vec::new(), 0.0, Vec::<String>::new());
        for item in spec.split(',') {
            let (name, w) = item.split_once(':').unwrap_or((item, ""));
            let w = if w.is_empty() { 1.0 } else { parse_float(w)? };
            let (style, pack) = self.single_style(name, depth)?;
            if !packs.contains(&pack) {
                packs.push(pack);
            }
            parts.push((style, w));
            total += w;
        }
        packs.sort();
        if packs.len() > 1 {
            return Err(format!("voice blend {} mixes packs {}; a blend must stay inside one pack", py_repr(spec), util::py_list(&packs)));
        }
        if parts.len() == 1 {
            return Ok((parts.pop().unwrap().0, packs.pop().unwrap()));
        }
        // sum(style * (w / total)): each term scaled in float32, added in order
        let mut acc = vec![0f32; parts[0].0.len()];
        for (style, w) in &parts {
            let f = (w / total) as f32;
            acc.iter_mut().zip(style).for_each(|(a, s)| *a += s * f);
        }
        Ok((acc, packs.pop().unwrap()))
    }

    fn build(&mut self, name: &str, e: &Value) -> Result<Speaker, String> {
        if self.eleven {
            if let Some(sp) = self.eleven_for(name, e)? {
                return Ok(sp);
            }
        }
        self.build_engine(name, e) // portray: single-narrator mode only, which is Qwen's (--qwen)
    }

    /// --engine elevenlabs: the speaker's line in `_elevenlabs:` (or their own `eleven:`), else `_default`.
    fn eleven_for(&mut self, name: &str, e: &Value) -> Result<Option<Speaker>, String> {
        let emap = self.raw.get("_elevenlabs").filter(|v| truthy(Some(v))).cloned().unwrap_or(json!({}));
        let own = entry(e, "eleven").filter(|v| truthy(Some(v)));
        let spec = own.or(emap.get(name).filter(|v| truthy(Some(v)))).or(emap.get("_default").filter(|v| truthy(Some(v)))).cloned();
        let Some(spec) = spec else {
            self.eleven_used.push(format!("{name} -> local (no _elevenlabs line, no _default)"));
            return Ok(None);
        };
        let settings = if spec.is_object() { spec } else { json!({"voice_id": spec}) };
        let sp = self.eleven_speaker(name, &settings, &emap)?;
        let pinned = emap.get(name).is_some() || own.is_some();
        self.eleven_used.push(format!("{name} -> {}{}", settings.get("voice_id").map_or("None".into(), py_str), if pinned { "" } else { " (_default)" }));
        Ok(Some(sp))
    }

    fn eleven_speaker(&mut self, name: &str, e: &Value, emap: &Value) -> Result<Speaker, String> {
        let mut sp = Speaker::new(name, "elevenlabs");
        sp.speed = entry(e, "speed").map_or(Ok(1.0), py_float)?;
        sp.gain = entry(e, "gain").map_or(Ok(1.0), py_float)?;
        let v = [entry(e, "voice_id"), entry(e, "voice")].into_iter().flatten().find(|v| truthy(Some(v))).map(py_str).unwrap_or_default();
        sp.voice_id = self.resolve_voice(&v)?;
        sp.model_id = [entry(e, "model"), emap.get("_model")].into_iter().flatten().find(|v| truthy(Some(v))).map(py_str).unwrap_or_default();
        sp.stability = entry(e, "stability").map_or(Ok(0.5), py_float)?;
        sp.similarity = entry(e, "similarity").map_or(Ok(0.75), py_float)?;
        sp.style_ex = entry(e, "style").map_or(Ok(0.0), py_float)?;
        Ok(sp)
    }

    fn build_engine(&mut self, name: &str, e: &Value) -> Result<Speaker, String> {
        if let Value::String(spec) = e {
            let (style, pack) = self.voice_style(spec, 0)?;
            let mut sp = Speaker::new(name, "kokoro");
            (sp.style, sp.pack) = (style, pack);
            return Ok(sp);
        }
        let f = |k: &str, d: f64| entry(e, k).map_or(Ok(d), py_float);
        let s = |k: &str, d: &str| entry(e, k).map_or(d.to_string(), py_str);
        let eng = s("engine", "kokoro").to_lowercase();
        let mut sp = match eng.as_str() {
            "elevenlabs" => {
                let emap = self.raw.get("_elevenlabs").filter(|v| truthy(Some(v))).cloned().unwrap_or(json!({}));
                return self.eleven_speaker(name, e, &emap);
            }
            "chatterbox" => {
                let mut sp = Speaker::new(name, "chatterbox");
                (sp.ref_, sp.exaggeration, sp.cfg, sp.model) = (s("ref", ""), f("exaggeration", 0.5)?, f("cfg", 0.5)?, s("model", "turbo").to_lowercase());
                sp
            }
            "supertonic" => {
                // voice: one of the ten presets (M1-M5, F1-F5); style: a voice-style JSON instead
                let mut sp = Speaker::new(name, "supertonic");
                (sp.voice, sp.ref_, sp.steps) = (s("voice", "M1").to_uppercase(), s("style", ""), entry(e, "steps").map_or(Ok(8), py_int)?);
                sp
            }
            "qwen" => {
                // Isaac, 13 Sep 2026: the design engine still drifts between takes; locked unless --qwen (which runs the Python)
                let fb = entry(e, "fallback").filter(|v| truthy(Some(v))).map(py_str);
                if let Some(fb) = fb.filter(|fb| self.raw.get(fb.as_str()).is_some() && fb != name) {
                    self.fallbacks.push(format!("{name} -> {fb}"));
                    let fe = self.raw[fb.as_str()].clone();
                    return self.build(name, &fe);
                }
                self.fallbacks.push(format!("{name} -> pool"));
                return self.pool_pick(name);
            }
            _ => {
                let (style, pack) = self.voice_style(&s("voice", "af_heart"), 0)?;
                let mut sp = Speaker::new(name, "kokoro");
                (sp.style, sp.pack) = (style, pack);
                sp
            }
        };
        (sp.speed, sp.gain) = (f("speed", 1.0)?, f("gain", 1.0)?);
        Ok(sp)
    }

    fn pool_pick(&mut self, who: &str) -> Result<Speaker, String> {
        // int(sha256(who).hexdigest(), 16) % len(pool)
        let hex = sha256_hex(who.as_bytes());
        let n = self.pool.len() as u64;
        let i = hex.chars().fold(0u64, |acc, c| (acc * 16 + c.to_digit(16).unwrap() as u64) % n) as usize;
        let pick = self.pool[i].clone();
        let (style, pack) = self.voice_style(&pick, 0)?;
        self.unassigned.push(format!("{who} -> {pick}"));
        let mut sp = Speaker::new(who, "kokoro");
        (sp.style, sp.pack) = (style, pack);
        Ok(sp)
    }

    fn speaker(&mut self, who: &str) -> Result<Rc<Speaker>, String> {
        if !self.speakers.contains_key(who) {
            let sp = match self.raw.get(who).cloned().filter(|_| !who.starts_with('_')) {
                Some(e) => self.build(who, &e)?,
                None => match if self.eleven { self.eleven_for(who, &json!({}))? } else { None } {
                    Some(sp) => sp,
                    None => self.pool_pick(who)?,
                },
            };
            self.speakers.insert(who.into(), Rc::new(sp));
        }
        Ok(self.speakers[who].clone())
    }

    // ------------------------------------------------------------ engines

    fn chatterbox_one(&mut self, sp: &Speaker, text: &str, ref_: &str) -> Result<Vec<f32>, String> {
        if self.chatterbox.is_none() {
            let (gpu, cpu) = (util::venv("wotr-cb-gpu").join("bin/python"), util::venv("wotr-cb").join("bin/python"));
            let py = if gpu.exists() { gpu } else { cpu };
            if !py.exists() {
                return Err("Chatterbox is not set up: run build/chatterbox_setup.sh (CPU) or build/chatterbox_gpu_setup.sh (the 9070 XT)".into());
            }
            let worker = root("build/chatterbox_worker.py");
            self.chatterbox = Some(Worker::start("Chatterbox", &py, &[&worker.to_string_lossy()], Some(root("build/.chatterbox_worker.log")))?);
        }
        let req = json!({"text": text, "model": sp.model, "ref": ref_, "exaggeration": sp.exaggeration, "cfg": sp.cfg});
        let msg = self.chatterbox.as_mut().unwrap().ask(&req, "chatterbox loaded on ")?;
        if let Some(e) = worker_error("chatterbox", &msg) {
            return Err(e);
        }
        take_npy(&msg)
    }

    /// chatterbox_backend.synth: sentence chunks, 0.18 s apart, a small pace stretch.
    fn chatterbox(&mut self, sp: &Speaker, text: &str, speed: f64) -> Result<Vec<f32>, String> {
        let ref_ = if sp.ref_.is_empty() { String::new() } else {
            let p = if Path::new(&sp.ref_).is_absolute() { PathBuf::from(&sp.ref_) } else { ROOT.join(&sp.ref_) };
            if !p.exists() {
                return Err(format!("{}: reference clip not found: {}", sp.name, p.display()));
            }
            p.to_string_lossy().into_owned()
        };
        let mut joined = Vec::new();
        for (i, c) in chunks(text).iter().enumerate() {
            if i > 0 {
                joined.extend(vec![0f32; (SAMPLE_RATE as f64 * 0.18) as usize]);
            }
            joined.extend(self.chatterbox_one(sp, c, &ref_)?);
        }
        // Chatterbox has no pace control: a stretch by resampling, within about 15%
        if (speed - 1.0).abs() < 0.02 {
            return Ok(joined);
        }
        let n = (joined.len() as f64 / speed.clamp(0.85, 1.15)) as usize;
        Ok(interp(&joined, n))
    }

    /// supertonic_backend.synth + supertonic_worker, the engine in-process.
    fn supertonic(&mut self, sp: &Speaker, text: &str, speed: f64) -> Result<Vec<f32>, String> {
        let style_path = if sp.ref_.is_empty() { None } else {
            let p = if Path::new(&sp.ref_).is_absolute() { PathBuf::from(&sp.ref_) } else { ROOT.join(&sp.ref_) };
            if !p.exists() {
                return Err(format!("{}: voice-style JSON not found: {}", sp.name, p.display()));
            }
            Some(p)
        };
        if self.supertonic.is_none() {
            self.supertonic = Some(crate::supertonic::Tts::load().map_err(|e| format!("supertonic: {e}\n  "))?);
            println!("  supertonic-3 on CPU");
        }
        let tts = self.supertonic.as_mut().unwrap();
        let fail = |e: String| format!("supertonic: {e}\n  ");
        let style = match &style_path {
            Some(p) => crate::supertonic::style(p),
            None => tts.preset(if sp.voice.is_empty() { "M1" } else { &sp.voice }),
        }.map_err(fail)?;
        let x = tts.synthesize(&cues_to_tags(text), &style, sp.steps, speed.clamp(0.7, 2.0)).map_err(fail)?;
        let sr = tts.sample_rate;
        Ok(resample(x, sr))
    }

    /// audio_check.wer through the read-back worker: (score, transcript).
    fn wer(&mut self, text: &str, samples: &[f32]) -> Result<(f64, String), String> {
        if self.readback.is_none() {
            self.readback = Some(Worker::start("read-back", Path::new(&crate::jobs::python()), &["-c", READBACK], None)?);
        }
        let p = std::env::temp_dir().join(format!("wotr_rb_{}.f32", std::process::id()));
        std::fs::write(&p, samples.iter().flat_map(|x| x.to_le_bytes()).collect::<Vec<u8>>()).map_err(|e| e.to_string())?;
        let msg = self.readback.as_mut().unwrap().ask(&json!({"text": text, "path": p.to_string_lossy()}), "");
        let _ = std::fs::remove_file(&p);
        let msg = msg?;
        if let Some(e) = msg.get("error") {
            return Err(py_str(e).trim_end().to_string());
        }
        Ok((parse_float(&py_str(&msg["score"]))?, py_str(&msg["heard"])))
    }

    /// audio_export.read_back: a generative take that reads back badly is taken again; the better one stays.
    fn read_back(&mut self, sp: &Speaker, text: &str, samples: Vec<f32>, retake: &mut dyn FnMut(&mut Narrator) -> Result<Vec<f32>, String>) -> Result<Vec<f32>, String> {
        if !self.check {
            return Ok(samples);
        }
        let ((mut score, mut heard), mut samples) = (self.wer(text, &samples)?, samples);
        if score > THRESHOLD {
            let again = retake(self)?;
            let (score2, heard2) = self.wer(text, &again)?;
            self.retakes += 1;
            if score2 < score {
                (samples, score, heard) = (again, score2, heard2);
            }
        }
        if score > THRESHOLD {
            self.worst.push((score, sp.name.clone(), util::head(text, 90).into(), util::head(&heard, 90).into()));
        }
        Ok(samples)
    }

    fn render_span(&mut self, sp: &Speaker, text: &str, speed: f64) -> Result<Vec<f32>, String> {
        match sp.engine {
            "elevenlabs" => self.eleven_synth(sp, &strip_cues(text), speed),
            "chatterbox" => {
                let text = if sp.model != "turbo" { strip_cues(text) } else { text.to_string() };
                let x = self.chatterbox(sp, &text, speed)?;
                // both engines sample, so a second take differs: keep whichever reads back better
                self.read_back(sp, &text, x, &mut |n| n.chatterbox(sp, &text, speed))
            }
            "supertonic" => {
                let x = self.supertonic(sp, text, speed)?;
                self.read_back(sp, text, x, &mut |n| n.supertonic(sp, text, speed))
            }
            _ => {
                let pack = sp.pack.clone();
                self.kokoro(&pack)?.create(&strip_cues(text), &sp.style, speed)
            }
        }
    }

    /// audio_export.synth_scene: a voice per tagged span, at its speaker's pace and level.
    fn synth_scene(&mut self, script: &[Block], speed: f64, lex: &Lexicon) -> Result<Vec<f32>, String> {
        let mut out = Vec::new();
        for (kind, spans) in script {
            if *kind == "divider" {
                out.extend(silence(DIVIDER_PAUSE));
                continue;
            }
            for (i, (who, text, mods)) in spans.iter().enumerate() {
                let sp = self.speaker(who)?;
                let (mut sp_speed, mut gain, mut pause) = (speed * sp.speed, sp.gain, 0f64);
                for w in mods {
                    let d = DELIVERY.iter().find(|d| d.0 == w).unwrap();
                    (sp_speed, gain, pause) = (sp_speed * d.1, gain * d.2, pause.max(d.3));
                }
                if i > 0 || pause > 0.0 {
                    out.extend(silence(if i > 0 { SPAN_PAUSE } else { 0.0 }.max(pause)));
                }
                let mut samples = self.render_span(&sp, &lex.respell(text), sp_speed)?;
                if gain != 1.0 {
                    samples.iter_mut().for_each(|x| *x = (*x * gain as f32).clamp(-1.0, 1.0));
                }
                out.extend(samples);
            }
            out.extend(silence(if *kind == "title" { TITLE_PAUSE } else { PARA_PAUSE }));
        }
        Ok(if out.is_empty() { silence(0.1) } else { out })
    }

    // ------------------------------------------------------------ ElevenLabs (build/elevenlabs_backend.py)

    fn resolve_voice(&mut self, spec: &str) -> Result<String, String> {
        let spec = py_strip(spec);
        if spec.chars().count() == 20 && spec.chars().all(char::is_alphanumeric) {
            return Ok(spec.into());
        }
        if self.eleven_names.is_none() {
            self.eleven_names = Some(list_voices()?.into_iter().map(|(id, name, _)| (name.to_lowercase(), id)).collect());
        }
        let names = self.eleven_names.as_ref().unwrap();
        let key = spec.to_lowercase();
        names.iter().find(|(n, _)| *n == key || n.starts_with(&key) || n.split(" - ").next().map(py_strip) == Some(&key)).map(|(_, id)| id.clone())
            .ok_or_else(|| format!("ElevenLabs: no voice named {} in the workspace ({} voices; build/audio_export.py --list-eleven)", py_repr(spec), names.len()))
    }

    fn eleven_synth(&mut self, sp: &Speaker, text: &str, speed: f64) -> Result<Vec<f32>, String> {
        let settings = json!({"stability": sp.stability, "similarity_boost": sp.similarity, "style": sp.style_ex, "use_speaker_boost": true,
                              "speed": (speed * sp.speed).clamp(0.7, 1.2)});
        let model = if sp.model_id.is_empty() { "eleven_multilingual_v2" } else { &sp.model_id };
        let mut out = Vec::new();
        for piece in eleven_split(text) {
            let body = json!({"text": piece, "model_id": model, "voice_settings": settings});
            let pcm = eleven_call("POST", &format!("/text-to-speech/{}?output_format=pcm_24000", sp.voice_id), Some(&body))?;
            out.extend(pcm.chunks_exact(2).map(|b| i16::from_le_bytes([b[0], b[1]]) as f32 / 32768.0));
        }
        Ok(out)
    }
}

/// supertonic_backend.cues_to_tags: [laugh] [sigh] [breath] become its tags, other cues go.
fn cues_to_tags(text: &str) -> String {
    let t = rx!(r"\s*\[([^\]]*)\]\s*").replace_all(text, |c: &fancy_regex::Captures<'_, str>| match py_strip(&c[1]).to_lowercase().as_str() {
        "laugh" => " <laugh> ".to_string(),
        "sigh" => " <sigh> ".to_string(),
        "breath" => " <breath> ".to_string(),
        _ => " ".to_string(),
    });
    py_strip(&t).to_string()
}

/// chatterbox_backend.chunks: sentences up to 280 chars; an over-long one is split at , or ;
fn chunks(text: &str) -> Vec<String> {
    let (mut out, mut cur) = (Vec::new(), String::new());
    for s in rx!(r#"(?<=[.!?…])\s+(?=["“'A-Z\[])"#).split(py_strip(text)).flatten() {
        let parts: Vec<&str> = if s.chars().count() > 280 { rx!(r"(?<=[,;])\s+").split(s).flatten().collect() } else { vec![s] };
        for p in parts {
            if !cur.is_empty() && cur.chars().count() + 1 + p.chars().count() > 280 {
                out.push(std::mem::take(&mut cur));
                cur = p.to_string();
            } else {
                cur = py_strip(&format!("{cur} {p}")).to_string();
            }
        }
    }
    if !cur.is_empty() {
        out.push(cur);
    }
    out
}

fn eleven_key() -> Result<String, String> {
    util::env("ELEVENLABS_API_KEY").map(|k| k.trim().to_string()).filter(|k| !k.is_empty())
        .ok_or_else(|| "ELEVENLABS_API_KEY is not set (see ~/.config/wotr/env); the ElevenLabs engine cannot run.".into())
}

/// elevenlabs_backend._call through curl (the key on curl's stdin, never its command line): the body,
/// with 429/500/502/503 retried after 1, 2, 4 s.
fn eleven_call(method: &str, path: &str, body: Option<&Value>) -> Result<Vec<u8>, String> {
    let key = eleven_key()?;
    let tmp = std::env::temp_dir().join(format!("wotr_el_{}", std::process::id()));
    let (req, resp) = (tmp.with_extension("json"), tmp.with_extension("out"));
    let q = |s: &str| format!("\"{}\"", s.replace('\\', "\\\\").replace('"', "\\\""));
    let mut cfg = format!("silent\nmax-time = 120\nrequest = {method}\nurl = {}\noutput = {}\nwrite-out = \"%{{http_code}}\"\n", q(&format!("https://api.elevenlabs.io/v1{path}")), q(&resp.to_string_lossy()));
    for h in [format!("xi-api-key: {key}"), "Content-Type: application/json".into(), "Accept: */*".into()] {
        cfg += &format!("header = {}\n", q(&h));
    }
    if let Some(b) = body {
        std::fs::write(&req, pyjson::dumps(b, false)).map_err(|e| e.to_string())?;
        cfg += &format!("data-binary = {}\n", q(&format!("@{}", req.display())));
    }
    let result = (|| {
        for attempt in 0..4 {
            let mut c = util::command("curl");
            let mut child = c.args(["-K", "-"]).stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::piped()).spawn().map_err(|e| format!("URLError: <urlopen error {e}>"))?;
            child.stdin.take().unwrap().write_all(cfg.as_bytes()).map_err(|e| e.to_string())?;
            let o = child.wait_with_output().map_err(|e| e.to_string())?;
            let data = std::fs::read(&resp).unwrap_or_default();
            let code: u16 = String::from_utf8_lossy(&o.stdout).trim().parse().unwrap_or(0);
            if !o.status.success() || code == 0 {
                return Err(format!("URLError: <urlopen error curl exit {}: {}>", o.status.code().unwrap_or(-1), String::from_utf8_lossy(&o.stderr).trim()));
            }
            if code < 400 {
                return Ok(data);
            }
            if matches!(code, 429 | 500 | 502 | 503) && attempt < 3 {
                std::thread::sleep(std::time::Duration::from_secs(1 << attempt));
                continue;
            }
            return Err(format!("RuntimeError: ElevenLabs {method} {path} -> {code}: {}", String::from_utf8_lossy(&data[..data.len().min(300)])));
        }
        unreachable!()
    })();
    let _ = (std::fs::remove_file(&req), std::fs::remove_file(&resp));
    result
}

/// elevenlabs_backend.list_voices: (voice_id, name, category) for the workspace.
fn list_voices() -> Result<Vec<(String, String, String)>, String> {
    let v: Value = serde_json::from_slice(&eleven_call("GET", "/voices", None)?).map_err(|e| format!("JSONDecodeError: {e}"))?;
    Ok(v["voices"].as_array().into_iter().flatten().map(|x| (py_str(&x["voice_id"]), x.get("name").map_or(String::new(), py_str), x.get("category").map_or(String::new(), py_str))).collect())
}

/// elevenlabs_backend._split: long spans cut at sentence ends under the API's size cap.
fn eleven_split(text: &str) -> Vec<String> {
    if text.chars().count() <= 4500 {
        return vec![text.into()];
    }
    let (mut parts, mut cur) = (Vec::new(), String::new());
    for sent in text.replace('\n', " ").split(". ") {
        let piece = if sent.ends_with('.') { sent.to_string() } else { format!("{sent}.") };
        if cur.chars().count() + piece.chars().count() + 1 > 4500 && !cur.is_empty() {
            parts.push(py_strip(&cur).to_string());
            cur.clear();
        }
        cur += &format!(" {piece}");
    }
    if !py_strip(&cur).is_empty() {
        parts.push(py_strip(&cur).to_string());
    }
    parts
}

// ---------------------------------------------------------------- output

/// soundfile.write(path, samples, 24000) as PCM_16. libsndfile 1.2 goes through int32 (measured): x * 2^31
/// rounded to even and clipped, then shifted down 16 bits.
fn wav_bytes(samples: &[f32]) -> Vec<u8> {
    let n = samples.len() as u32 * 2;
    let mut b = Vec::with_capacity(44 + n as usize);
    b.extend(b"RIFF");
    b.extend((36 + n).to_le_bytes());
    b.extend(b"WAVEfmt ");
    b.extend(16u32.to_le_bytes());
    b.extend(1u16.to_le_bytes());
    b.extend(1u16.to_le_bytes());
    b.extend((SAMPLE_RATE as u32).to_le_bytes());
    b.extend((SAMPLE_RATE as u32 * 2).to_le_bytes());
    b.extend(2u16.to_le_bytes());
    b.extend(16u16.to_le_bytes());
    b.extend(b"data");
    b.extend(n.to_le_bytes());
    for x in samples {
        let t = (*x as f64 * 2147483648.0).round_ties_even().clamp(-2147483648.0, 2147483647.0) as i32;
        b.extend(((t >> 16) as i16).to_le_bytes());
    }
    b
}

type LameSet = unsafe extern "C" fn(*mut std::ffi::c_void, i32) -> i32;

/// The LAME 3.100 built into the venv's lameenc (Arch's libmp3lame is 4.0, whose frames differ). The
/// extension refers to a few CPython symbols, so libpython is loaded first to provide them; no
/// interpreter is started. None when lameenc is not there.
fn lame() -> Option<&'static libloading::Library> {
    static LIB: LazyLock<Option<libloading::Library>> = LazyLock::new(|| {
        let site = util::site_packages("wotr")?;
        let ext = std::fs::read_dir(&site).ok()?.flatten().map(|e| e.path()).find(|p| name_of(p).starts_with("lameenc.") && name_of(p).ends_with(".so"))?;
        let ver = name_of(site.parent()?).trim_start_matches("python").to_string();
        unsafe {
            let py = libloading::os::unix::Library::open(Some(format!("libpython{ver}.so.1.0")), libloading::os::unix::RTLD_NOW | libloading::os::unix::RTLD_GLOBAL).ok()?;
            std::mem::forget(py);
            libloading::Library::new(ext).ok()
        }
    });
    LIB.as_ref()
}

/// lameenc.Encoder: 96 kb/s, quality 2, mono, 24 kHz (and no Xing frame, as lameenc sets).
fn mp3_bytes(samples: &[f32]) -> Option<Vec<u8>> {
    let lib = lame()?;
    let pcm: Vec<i16> = samples.iter().map(|x| (x.clamp(-1.0, 1.0) * 32767.0) as i16).collect();
    unsafe {
        let init: libloading::Symbol<unsafe extern "C" fn() -> *mut std::ffi::c_void> = lib.get(b"lame_init").ok()?;
        let set = |name: &[u8], v: i32, g| lib.get::<LameSet>(name).map(|f| f(g, v));
        let g = init();
        for (name, v) in [(&b"lame_set_num_channels"[..], 1), (b"lame_set_in_samplerate", SAMPLE_RATE as i32), (b"lame_set_brate", 96), (b"lame_set_quality", 2), (b"lame_set_bWriteVbrTag", 0)] {
            set(name, v, g).ok()?;
        }
        let params: libloading::Symbol<unsafe extern "C" fn(*mut std::ffi::c_void) -> i32> = lib.get(b"lame_init_params").ok()?;
        if params(g) < 0 {
            return None;
        }
        let encode: libloading::Symbol<unsafe extern "C" fn(*mut std::ffi::c_void, *const i16, *const i16, i32, *mut u8, i32) -> i32> = lib.get(b"lame_encode_buffer").ok()?;
        let flush: libloading::Symbol<unsafe extern "C" fn(*mut std::ffi::c_void, *mut u8, i32) -> i32> = lib.get(b"lame_encode_flush").ok()?;
        let close: libloading::Symbol<unsafe extern "C" fn(*mut std::ffi::c_void) -> i32> = lib.get(b"lame_close").ok()?;
        let mut out = vec![0u8; pcm.len() * 5 / 4 + 7200];
        let k = encode(g, pcm.as_ptr(), std::ptr::null(), pcm.len() as i32, out.as_mut_ptr(), out.len() as i32);
        let mut tail = vec![0u8; 7200];
        let k2 = flush(g, tail.as_mut_ptr(), 7200);
        close(g);
        if k < 0 || k2 < 0 {
            return None;
        }
        out.truncate(k as usize);
        out.extend_from_slice(&tail[..k2 as usize]);
        Some(out)
    }
}

fn write_audio(samples: &[f32], path: &Path, mp3: bool) -> Result<PathBuf, String> {
    let w = |p: PathBuf, b: Vec<u8>| std::fs::write(&p, b).map(|_| p).map_err(|e| e.to_string());
    if !mp3 {
        return w(with_suffix(path, ".wav"), wav_bytes(samples));
    }
    match mp3_bytes(samples) {
        Some(b) => w(with_suffix(path, ".mp3"), b),
        None => {
            println!("  (lameenc not installed; wrote WAV)");
            w(with_suffix(path, ".wav"), wav_bytes(samples))
        }
    }
}

fn fetch_model(pack: &str) -> Result<(), String> {
    let dir = root("build/models");
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let release = if pack == "zh" { "model-files-v1.1" } else { "model-files-v1.0" };
    let (_, m, v) = PACKS.iter().find(|p| p.0 == pack).unwrap();
    for name in [m, v] {
        let dest = dir.join(name);
        let size = dest.metadata().map(|m| m.len()).unwrap_or(0);
        if size > 1_000_000 {
            println!("  {name}: already here ({} bytes)", crate::jobs::commas(size as usize));
            continue;
        }
        let url = format!("https://github.com/thewh1teagle/kokoro-onnx/releases/download/{release}/{name}");
        println!("  fetching {url}");
        let t0 = Instant::now();
        let ok = util::command("curl").args(["-fsSL", "-o"]).arg(&dest).arg(&url).status().map_err(|e| e.to_string())?;
        if !ok.success() {
            return Err(format!("urllib.error.HTTPError: {url} (curl exit {})", ok.code().unwrap_or(-1)));
        }
        let total = dest.metadata().map(|m| m.len()).unwrap_or(0);
        println!("  {name}: {} bytes in {:.0}s", crate::jobs::commas(total as usize), t0.elapsed().as_secs_f64());
    }
    Ok(())
}

// ---------------------------------------------------------------- main

fn parse_args(args: &[String]) -> Result<Opts, String> {
    let mut o = Opts {
        out: root("docs/audio").to_string_lossy().into(), voice: "narrator".into(), speed: 1.0, scene: vec![], max_minutes: 0.0, wav: false, force: false,
        dry_run: false, plain: false, check_cast: false, no_cast: false, no_check: false, first: 0, qwen: false, engine: "local".into(),
        list_eleven: false, single: false, fetch_model: false, pack: "v1.0".into(), list_voices: false, say: None,
        wav_out: root("docs/audio/say.wav").to_string_lossy().into(),
    };
    const VALUED: [&str; 9] = ["--out", "--voice", "--speed", "--scene", "--max-minutes", "--first", "--engine", "--pack", "--say"];
    const FLAGS: [&str; 14] = ["--wav", "--force", "--dry-run", "--plain", "--check-cast", "--no-cast", "--no-check", "--qwen", "--list-eleven", "--single",
                               "--fetch-model", "--list-voices", "-h", "--help"];
    let mut i = 0;
    while i < args.len() {
        let (mut flag, mut val) = match args[i].split_once('=').filter(|_| args[i].starts_with("--")) {
            Some((f, v)) => (f.to_string(), Some(v.to_string())),
            None => (args[i].clone(), None),
        };
        // argparse takes an unambiguous prefix of a long option
        let all: Vec<&str> = VALUED.iter().chain(&FLAGS).copied().chain(["--wav-out"]).collect();
        if !all.contains(&flag.as_str()) {
            let m: Vec<&&str> = all.iter().filter(|a| a.starts_with(flag.as_str()) && flag.starts_with("--")).collect();
            if m.len() != 1 {
                return Err(format!("unrecognized arguments: {}", args[i]));
            }
            flag = m[0].to_string();
        }
        if VALUED.contains(&flag.as_str()) || flag == "--wav-out" {
            if val.is_none() {
                i += 1;
                val = Some(args.get(i).cloned().ok_or_else(|| format!("argument {flag}: expected one argument"))?);
            }
            let v = val.unwrap();
            let float = |v: &str| parse_float(v).map_err(|_| format!("argument {flag}: invalid float value: {}", py_repr(v)));
            match flag.as_str() {
                "--out" => o.out = v,
                "--voice" => o.voice = v,
                "--speed" => o.speed = float(&v)?,
                "--scene" => o.scene.push(v),
                "--max-minutes" => o.max_minutes = float(&v)?,
                "--first" => o.first = py_strip(&v).parse().map_err(|_| format!("argument --first: invalid int value: {}", py_repr(&v)))?,
                "--engine" if v == "local" || v == "elevenlabs" => o.engine = v,
                "--engine" => return Err(format!("argument --engine: invalid choice: {} (choose from local, elevenlabs)", py_repr(&v))),
                "--pack" if v == "v1.0" || v == "zh" => o.pack = v,
                "--pack" => return Err(format!("argument --pack: invalid choice: {} (choose from v1.0, zh)", py_repr(&v))),
                "--say" => o.say = Some(v),
                _ => o.wav_out = v,
            }
        } else {
            match flag.as_str() {
                "--wav" => o.wav = true,
                "--force" => o.force = true,
                "--dry-run" => o.dry_run = true,
                "--plain" => o.plain = true,
                "--check-cast" => o.check_cast = true,
                "--no-cast" => o.no_cast = true,
                "--no-check" => o.no_check = true,
                "--qwen" => o.qwen = true,
                "--list-eleven" => o.list_eleven = true,
                "--single" => o.single = true,
                "--fetch-model" => o.fetch_model = true,
                "--list-voices" => o.list_voices = true,
                _ => return Err("help".into()),
            }
        }
        i += 1;
    }
    Ok(o)
}

/// `wotr-mcp audio ARGS`: audio_export.py's main(); the exit code.
pub fn main(args: &[String]) -> i32 {
    let o = match parse_args(args) {
        Ok(o) => o,
        Err(e) if e == "help" => {
            println!("usage: wotr-mcp audio [build/audio_export.py's options; see its docstring]");
            return 0;
        }
        Err(e) => {
            eprintln!("usage: wotr-mcp audio [options]\nwotr-mcp audio: error: {e}");
            return 2;
        }
    };
    if o.qwen {
        // the Qwen design engine joins takes by Whisper word alignment and shapes them with Praat: Python
        use std::os::unix::process::CommandExt;
        let e = util::command(crate::jobs::python()).arg(root("build/audio_export.py")).args(args).exec();
        eprintln!("{e}");
        return 1;
    }
    // the Python's uncaught exceptions print a traceback, which narration_status reads as a failed job;
    // its sys.exit messages (below) do not
    const TRACEBACK: &str = "Traceback (most recent call last):\n  File \"wotr-mcp audio\"";
    let default = std::panic::take_hook();
    std::panic::set_hook(Box::new(move |i| {
        eprintln!("{TRACEBACK}");
        default(i)
    }));
    match run(&o) {
        Ok(code) => code,
        Err(e) => {
            const EXITS: [&str; 12] = ["unknown voice", "voice preset loop", "voice blend", "model files for pack", "kokoro-onnx is not installed",
                                       "Chatterbox is not set up", "the Chatterbox worker died", "chatterbox: ", "supertonic: ", "ElevenLabs: no voice",
                                       "ELEVENLABS_API_KEY", "unknown delivery word"];
            let exit = EXITS.iter().any(|x| e.starts_with(x)) || [": reference clip not found", ": voice-style JSON not found", ".cast.md: "].iter().any(|x| e.contains(x));
            if !exit {
                eprintln!("{TRACEBACK}");
            }
            eprintln!("{e}");
            1
        }
    }
}

fn run(a: &Opts) -> Result<i32, String> {
    if a.fetch_model {
        fetch_model(&a.pack)?;
        return Ok(0);
    }
    let eleven = a.engine == "elevenlabs";
    if a.list_eleven {
        for (id, name, cat) in list_voices()? {
            println!("  {id}  {name}  ({cat})");
        }
        return Ok(0);
    }
    let lex = load_lexicon()?;
    let lexicon = Lexicon::new(&lex);
    if let Some(say) = &a.say {
        let mut n = Narrator::new(&a.voice, eleven, !a.no_check)?;
        let sp = n.speaker("narrator")?;
        let samples = n.render_span(&sp, &lexicon.respell(say), a.speed * sp.speed)?;
        let out = PathBuf::from(&a.wav_out);
        if let Some(d) = out.parent() {
            let _ = std::fs::create_dir_all(d);
        }
        std::fs::write(&out, wav_bytes(&samples)).map_err(|e| e.to_string())?;
        println!("  {}: {:.1}s, voice {}", out.display(), samples.len() as f64 / SAMPLE_RATE as f64, a.voice);
        return Ok(0);
    }
    let mut arcs = read_arcs()?;
    let filed: Vec<String> = arcs.iter().flat_map(|(_, ps)| ps.iter().map(|p| name_of(p))).collect();
    let mut unfiled: Vec<PathBuf> = std::fs::read_dir(root("scenes")).into_iter().flatten().flatten().map(|e| e.path())
        .filter(|p| name_of(p).ends_with(".md")).collect();
    unfiled.sort();
    unfiled.retain(|p| {
        let n = name_of(p);
        !filed.contains(&n) && !n.to_uppercase().contains("SUPERSEDED") && !["MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md"].contains(&n.as_str())
    });
    if !unfiled.is_empty() {
        arcs.push(("Unfiled".into(), unfiled));
    }
    // number every scene from the full reading order, then narrow to --scene, so a scene keeps the
    // same "03-07" prefix whether rendered alone or in the batch
    let mut numbered: Vec<(usize, String, usize, PathBuf)> = arcs.iter().enumerate()
        .flat_map(|(ai, (name, files))| files.iter().enumerate().map(move |(si, p)| (ai + 1, name.clone(), si + 1, p.clone()))).collect();
    if !a.scene.is_empty() {
        let mut wanted: Vec<String> = a.scene.iter().map(|s| name_of(Path::new(s))).collect();
        wanted.dedup();
        for w in wanted.iter().filter(|w| !numbered.iter().any(|x| name_of(&x.3) == **w)) {
            println!("  no such scene: {w}");
        }
        numbered.retain(|x| wanted.contains(&name_of(&x.3)));
    }
    if a.dry_run {
        for (_, name, _, p) in &numbered {
            let blocks = scene_blocks(&read_lossy(p));
            if a.plain {
                let body: Vec<String> = blocks.iter().map(|(k, t)| match *k { "divider" => "---".into(), "title" => format!("# {t}"), _ => t.clone() }).collect();
                print!("{}\n", body.join("\n\n"));
                continue;
            }
            println!("=== {name} / {}", name_of(p));
            for (kind, text) in &blocks {
                println!("[{kind}] {}", util::head(&lexicon.respell(text), 160));
            }
        }
        return Ok(0);
    }
    if a.check_cast {
        let mut bad = 0;
        for (_, _, _, p) in &numbered {
            let cp = cast_path(p);
            if !cp.exists() {
                continue;
            }
            let blocks = scene_blocks(&read_lossy(p));
            let cast = parse_cast(&read_lossy(&cp))?;
            let problem = check_cast(&blocks, &cast);
            println!("{}: {}", name_of(&cp), problem.as_deref().unwrap_or("ok"));
            if problem.is_none() {
                let v = load_voices_yaml()?;
                let assigned: Vec<&String> = v.as_object().map(|m| m.keys().filter(|k| !k.starts_with('_')).collect()).unwrap_or_default();
                let who: Vec<String> = speakers(&cast).iter().map(|s| format!("{s}{}", if s == "narrator" || assigned.contains(&s) { "" } else { " (no voice assigned)" })).collect();
                println!("  speakers: {}", who.join(", "));
            }
            bad += usize::from(problem.is_some());
        }
        return Ok(if bad > 0 { 1 } else { 0 });
    }
    if a.list_voices {
        let models = root("build/models");
        let mut out = Vec::new();
        for (pack, m, v) in PACKS {
            if !(models.join(m).exists() && models.join(v).exists()) {
                if pack == "v1.0" {
                    return Err(format!("model files for pack 'v1.0' missing in {}: run with --fetch-model", models.display()));
                }
                continue;
            }
            let mut names: Vec<String> = kokoro::load_npz(&models.join(v))?.into_iter().map(|(k, _)| if pack == "zh" { format!("zh/{k}") } else { k }).collect();
            names.sort_by(|x, y| x.trim_start_matches("zh/").cmp(y.trim_start_matches("zh/")));
            out.extend(names);
        }
        for v in out {
            println!("  {v}");
        }
        return Ok(0);
    }
    let mut n = Narrator::new(&a.voice, eleven, !a.no_check)?;
    let out = PathBuf::from(&a.out);
    std::fs::create_dir_all(&out).map_err(|e| e.to_string())?;
    let man_p = out.join(".manifest.json");
    let mut manifest: Map<String, Value> = if man_p.exists() { pyjson::loads(&read_lossy(&man_p))?.as_object().cloned().unwrap_or_default() } else { Map::new() };
    let lex_obj = Value::Object(lex.iter().map(|(k, v)| (k.clone(), Value::String(v.clone()))).collect());
    let lex_hash = util::head(&sha256_hex(pyjson::dumps(&lex_obj, true).as_bytes()), 8).to_string();
    let save = |m: &Map<String, Value>| {
        let mut keys: Vec<&String> = m.keys().collect();
        keys.sort();
        let sorted: Map<String, Value> = keys.into_iter().map(|k| (k.clone(), m[k].clone())).collect();
        std::fs::write(&man_p, pyjson::dumps_indent(&Value::Object(sorted), 1)).map_err(|e| e.to_string())
    };
    let t_start = Instant::now();
    let (mut written, mut skipped) = (0, 0);
    for (ai, name, si, p) in &numbered {
        let folder = out.join(format!("{ai:02} {}", safe_name(name)));
        let md = read_lossy(p);
        let mut blocks = scene_blocks(&md);
        let mut script = if a.no_cast { None } else {
            let cp = cast_path(p);
            match cp.exists() {
                false => None,
                true => {
                    let cast = parse_cast(&read_lossy(&cp))?;
                    if let Some(problem) = check_cast(&blocks, &cast) {
                        return Err(format!("{}: {problem}\n(fix the cast file, or run with --no-cast)", name_of(&cp)));
                    }
                    Some(cast)
                }
            }
        };
        let mut key = format!("{ai:02}-{si:02} {}", safe_name(&scene_title(p, &md)));
        if a.first > 0 {
            blocks.truncate(a.first);
            script = script.filter(|s| !s.is_empty()).map(|mut s| {
                s.truncate(a.first);
                s
            });
            key += &format!("-first{}", a.first);
        }
        if eleven {
            key += "-eleven";
        }
        let voices_hash = util::head(&sha256_hex(pyjson::dumps(&load_voices_yaml()?, true).as_bytes()), 8).to_string();
        let blocks_json = Value::Array(blocks.iter().map(|(k, t)| json!([k, t])).collect());
        let script_json = script.as_ref().map_or(Value::Null, |s| Value::Array(s.iter().map(|(k, sp)| json!([k, sp.iter().map(|(w, t, m)| json!([w, t, m])).collect::<Vec<_>>()])).collect()));
        let speed = format!("{:?}", a.speed);
        let h = util::head(&sha256_hex(format!("{}{}{}{speed}{lex_hash}{voices_hash}{}", pyjson::dumps(&blocks_json, false), pyjson::dumps(&script_json, false), a.voice, a.engine).as_bytes()), 16).to_string();
        let target = folder.join(&key);
        let ext = if a.wav { ".wav" } else { ".mp3" };
        if !a.force && manifest.get(&key) == Some(&json!(h)) && with_suffix(&target, ext).exists() {
            skipped += 1;
            continue;
        }
        if a.max_minutes != 0.0 && t_start.elapsed().as_secs_f64() / 60.0 > a.max_minutes {
            println!("  time budget reached; {key} and later left for next run");
            save(&manifest)?;
            return Ok(0);
        }
        std::fs::create_dir_all(&folder).map_err(|e| e.to_string())?;
        let words: usize = blocks.iter().map(|(_, t)| t.split_whitespace().count()).sum();
        let t0 = Instant::now();
        let script = script.filter(|s| !s.is_empty());
        let plan: Vec<Block> = match &script {
            Some(s) => s.clone(),
            None => blocks.iter().map(|(k, t)| (*k, vec![("narrator".to_string(), t.clone(), vec![])])).collect(),
        };
        // every speaker is resolved before the first span renders, as the Python's Qwen check does
        for s in script.as_deref().map(speakers).unwrap_or_else(|| vec!["narrator".into()]) {
            n.speaker(&s)?;
        }
        let samples = n.synth_scene(&plan, a.speed, &lexicon)?;
        let path = write_audio(&samples, &target, !a.wav)?;
        manifest.insert(key.clone(), json!(h));
        save(&manifest)?;
        let note = script.as_ref().map_or(String::new(), |s| format!(", {} voices", speakers(s).len()));
        println!("  {}: {} words -> {:.1} min audio in {:.0}s{note}", name_of(&path), crate::jobs::commas(words), samples.len() as f64 / SAMPLE_RATE as f64 / 60.0, t0.elapsed().as_secs_f64());
        written += 1;
    }
    let sorted_set = |v: &[String]| {
        let mut v = v.to_vec();
        v.sort();
        v.dedup();
        v.join("; ")
    };
    if !n.eleven_used.is_empty() {
        println!("elevenlabs voices: {}", sorted_set(&n.eleven_used));
    }
    if !n.fallbacks.is_empty() {
        println!("qwen engine is locked (--qwen unlocks it); these speakers used their fallback: {}", sorted_set(&n.fallbacks));
    }
    if !n.unassigned.is_empty() {
        println!("speakers with no entry in build/voices.yaml, given a pool voice: {}", sorted_set(&n.unassigned));
    }
    if n.retakes > 0 || !n.worst.is_empty() {
        println!("read-back check: {} span(s) re-taken; {} still above {:.0}% word error:", n.retakes, n.worst.len(), THRESHOLD * 100.0);
        n.worst.sort_by(|x, y| y.0.total_cmp(&x.0).then_with(|| y.1.cmp(&x.1)).then_with(|| y.2.cmp(&x.2)).then_with(|| y.3.cmp(&x.3)));
        for (score, who, text, heard) in n.worst.iter().take(8) {
            println!("  {:.0}% {who}: {} -> heard {}", score * 100.0, py_repr(text), py_repr(heard));
        }
    }
    println!("audio: {written} written, {skipped} unchanged -> {}", out.display());
    Ok(0)
}

/// `wotr-mcp audio-probe`, for rust/audio_parity.py only: one JSON request per stdin line, one reply
/// line each. {"op": "phonemes", "texts": [...]} -> the phoneme batches and token ids per text;
/// {"op": "kokoro"|"supertonic", "text", "voice", "speed", "steps", "out"} -> raw f32 samples in `out`
/// (Supertonic's at its native rate, as its worker returns them).
pub fn probe() -> i32 {
    let mut n: Option<Narrator> = None;
    for line in std::io::stdin().lines().map_while(Result::ok) {
        let req: Value = serde_json::from_str(&line).unwrap_or_default();
        let s = |k: &str| req[k].as_str().unwrap_or_default().to_string();
        let rep = (|| -> Result<Value, String> {
            let n = match &mut n {
                Some(n) => n,
                None => n.insert(Narrator::new("narrator", false, false)?),
            };
            let x = match s("op").as_str() {
                "phonemes" => {
                    let out: Result<Vec<Value>, String> = req["texts"].as_array().into_iter().flatten().map(|t| {
                        let b = kokoro::split_phonemes(&kokoro::phonemize(t.as_str().unwrap_or_default())?);
                        b.into_iter().map(|p| kokoro::tokens(&p).map(|t| json!([p, t]))).collect::<Result<Vec<_>, _>>().map(Value::Array)
                    }).collect();
                    return Ok(json!({"batches": out?}));
                }
                "kokoro" => {
                    let (style, pack) = n.voice_style(&s("voice"), 0)?;
                    n.kokoro(&pack)?.create(&s("text"), &style, req["speed"].as_f64().unwrap_or(1.0))?
                }
                _ => {
                    if n.supertonic.is_none() {
                        n.supertonic = Some(crate::supertonic::Tts::load()?);
                    }
                    let tts = n.supertonic.as_mut().unwrap();
                    let style = tts.preset(&s("voice"))?;
                    tts.synthesize(&s("text"), &style, req["steps"].as_i64().unwrap_or(8), req["speed"].as_f64().unwrap_or(1.0))?
                }
            };
            std::fs::write(s("out"), x.iter().flat_map(|v| v.to_le_bytes()).collect::<Vec<u8>>()).map_err(|e| e.to_string())?;
            Ok(json!({"samples": x.len()}))
        })();
        println!("{}", rep.unwrap_or_else(|e| json!({"error": e})));
    }
    0
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn python_helpers() {
        assert_eq!(sha256_hex(b"abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
        assert_eq!(with_suffix(Path::new("/x/01-02 St. Mary"), ".mp3"), Path::new("/x/01-02 St.mp3"));
        assert_eq!(with_suffix(Path::new("/x/01-02 Plain"), ".mp3"), Path::new("/x/01-02 Plain.mp3"));
        assert_eq!(interp(&[0.0, 1.0, 2.0], 5), [0.0, 0.5, 1.0, 1.5, 2.0]);
        assert_eq!(cues_to_tags("Ha [laugh] no [sniff] way [sigh]"), "Ha <laugh> no way <sigh>");
        assert_eq!(chunks("One. Two! \"Three\""), ["One. Two! \"Three\""]);
        let cast = parse_cast("# T\n\nA line. [Gimbzo: slow, beat] \"No.\" [sigh] [narrator] Done.\n\n---").unwrap();
        assert_eq!(cast[1].1[1], ("Gimbzo".to_string(), "\"No.\" [sigh]".to_string(), vec!["slow".to_string(), "beat".to_string()]));
        assert_eq!(speakers(&cast), ["narrator", "Gimbzo"]);
    }
}
