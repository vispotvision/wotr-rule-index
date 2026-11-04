//! Kokoro 82M as kokoro-onnx 0.4.7 runs it, ported: espeak-ng (the wotr venv's espeakng_loader copy,
//! loaded as a library) phonemizes as phonemizer 3.3 does for kokoro-onnx (preserve_punctuation,
//! with_stress, the default separator, 'keep-flags'), then the same vocabulary, batching, style row,
//! ONNX graph (the venv's ONNX Runtime, as embed.rs) and librosa-style trim. rust/audio_parity.py
//! checks phonemes, tokens and samples against the Python.
use crate::util::site_packages;
use libloading::{Library, Symbol};
use serde_json::Value;
use std::collections::BTreeMap;
use std::ffi::{c_char, c_int, c_void, CStr, CString};
use std::path::{Path, PathBuf};
use std::sync::{LazyLock, Mutex};

pub const SAMPLE_RATE: usize = 24000;
const MAX_PHONEMES: usize = 510;
const MARKS: &str = ";:,.!?¡¿—…\"«»“”(){}[]"; // phonemizer's Punctuation.default_marks()

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<regex::Regex> = LazyLock::new(|| regex::Regex::new($p).unwrap());
        &*R
    }};
}

/// str.strip() with no argument: str.isspace(), which also counts U+001C..U+001F.
pub fn py_strip(s: &str) -> &str {
    s.trim_matches(|c: char| c.is_whitespace() || ('\u{1c}'..='\u{1f}').contains(&c))
}

#[repr(C)]
struct Voice {
    name: *const c_char,
    languages: *const c_char,
    identifier: *const c_char,
    gender: u8,
    age: u8,
    variant: u8,
    xx1: u8,
    score: c_int,
    spare: *mut c_void,
}

type TextToPhonemes = unsafe extern "C" fn(*mut *const c_void, c_int, c_int) -> *const c_char;

struct Espeak {
    _lib: Library,
    t2p: TextToPhonemes,
}
unsafe impl Send for Espeak {}

fn loader_dir() -> Result<PathBuf, String> {
    site_packages("wotr").map(|d| d.join("espeakng_loader")).filter(|d| d.is_dir()).ok_or_else(|| "espeakng_loader is not installed in the wotr venv (pip install kokoro-onnx)".into())
}

/// EspeakWrapper + set_voice('en-us'). One library for the run: phonemizer loads a fresh copy per
/// phonemize() call, which audio_parity.py shows makes no difference to the phonemes.
fn load_espeak() -> Result<Espeak, String> {
    let dir = loader_dir()?;
    let lib_path = std::env::var("PHONEMIZER_ESPEAK_LIBRARY").map(PathBuf::from).unwrap_or_else(|_| dir.join("libespeak-ng.so"));
    // resolved, as phonemizer does: espeak-ng ignores a data path longer than its buffer
    let data = dir.join("espeak-ng-data").canonicalize().map_err(|e| format!("espeak-ng-data: {e}"))?;
    let data = CString::new(data.to_string_lossy().as_bytes()).unwrap();
    let e = |x: libloading::Error| format!("espeak-ng: {x}");
    unsafe {
        let lib = Library::new(&lib_path).map_err(e)?;
        let init: Symbol<unsafe extern "C" fn(c_int, c_int, *const c_char, c_int) -> c_int> = lib.get(b"espeak_Initialize").map_err(e)?;
        if init(2, 0, data.as_ptr(), 0) <= 0 {
            return Err("failed to initialize espeak shared library".into());
        }
        let list: Symbol<unsafe extern "C" fn(*const Voice) -> *const *const Voice> = lib.get(b"espeak_ListVoices").map_err(e)?;
        let (mut v, mut ident) = (list(std::ptr::null()), None);
        while !(*v).is_null() {
            let voice = &**v;
            // the first byte of `languages` is the priority, then the language, NUL-terminated
            if CStr::from_ptr(voice.languages).to_bytes().get(1..) == Some(b"en-us") {
                ident = Some(CStr::from_ptr(voice.identifier).to_owned());
                break;
            }
            v = v.add(1);
        }
        let ident = ident.ok_or("invalid voice code \"en-us\"")?;
        let set: Symbol<unsafe extern "C" fn(*const c_char) -> c_int> = lib.get(b"espeak_SetVoiceByName").map_err(e)?;
        if set(ident.as_ptr()) != 0 {
            return Err("failed to load voice \"en-us\"".into());
        }
        let t2p = *lib.get::<TextToPhonemes>(b"espeak_TextToPhonemes").map_err(e)?;
        Ok(Espeak { _lib: lib, t2p })
    }
}

static ESPEAK: LazyLock<Mutex<Result<Espeak, String>>> = LazyLock::new(|| Mutex::new(load_espeak()));

/// EspeakWrapper.text_to_phonemes: clause by clause, IPA with '_' between phonemes, joined by spaces.
fn text_to_phonemes(es: &Espeak, text: &str) -> String {
    let c = CString::new(text.split('\0').next().unwrap()).unwrap();
    let mut ptr = c.as_ptr() as *const c_void;
    let mut out = Vec::new();
    while !ptr.is_null() {
        let r = unsafe { (es.t2p)(&mut ptr, 1, ('_' as c_int) << 8 | 2) };
        if !r.is_null() {
            let s = unsafe { CStr::from_ptr(r) }.to_string_lossy().into_owned();
            if !s.is_empty() {
                out.push(s);
            }
        }
    }
    out.join(" ")
}

/// EspeakBackend._postprocess_line with the default separator, stress kept, no tie, strip=False.
fn postprocess(line: &str) -> String {
    let line = py_strip(line).replace('\n', " ").replace("  ", " ");
    let line = rx!("_+").replace_all(&line, "_").replace("_ ", " ");
    if line.is_empty() {
        return String::new();
    }
    line.split(' ').map(|w| py_strip(w).replace('_', "") + " ").collect()
}

struct Mark {
    index: usize,
    mark: String,
    pos: char,
}

/// Punctuation._preserve_line
fn preserve_line(line: &str, num: usize) -> (Vec<String>, Vec<Mark>) {
    static RE: LazyLock<regex::Regex> = LazyLock::new(|| regex::Regex::new(&format!(r"(\s*[{}]+\s*)+", regex::escape(MARKS))).unwrap());
    let ms: Vec<&str> = RE.find_iter(line).map(|m| m.as_str()).collect();
    if ms.is_empty() {
        return (vec![line.to_string()], vec![]);
    }
    if ms.len() == 1 && ms[0] == line {
        return (vec![], vec![Mark { index: num, mark: line.to_string(), pos: 'A' }]);
    }
    let marks: Vec<Mark> = ms.iter().enumerate().map(|(k, m)| {
        let pos = if k == 0 && line.starts_with(m) { 'B' } else if k == ms.len() - 1 && line.ends_with(m) { 'E' } else { 'I' };
        Mark { index: num, mark: m.to_string(), pos }
    }).collect();
    let (mut out, mut rest) = (Vec::new(), line);
    for m in &marks {
        let (prefix, suffix) = rest.split_once(m.mark.as_str()).unwrap_or((rest, ""));
        out.push(prefix.to_string());
        rest = suffix;
    }
    out.push(rest.to_string());
    (out, marks)
}

/// Punctuation.restore with the word separator ' ' and strip=False.
fn restore(text: Vec<String>, marks: Vec<Mark>) -> Vec<String> {
    let (mut text, mut marks) = (std::collections::VecDeque::from(text), std::collections::VecDeque::from(marks));
    let (mut out, mut pos) = (Vec::new(), 0);
    let space = |m: &str| if m.ends_with(' ') { "" } else { " " };
    while !text.is_empty() || !marks.is_empty() {
        if marks.is_empty() {
            out.extend(text.drain(..).map(|l| if l.ends_with(' ') { l } else { l + " " }));
        } else if text.is_empty() {
            out.push(marks.drain(..).map(|m| m.mark).collect());
        } else if marks[0].index == pos {
            let m = marks.pop_front().unwrap();
            if text[0].ends_with(' ') {
                text[0].pop();
            }
            match m.pos {
                'B' => text[0] = format!("{}{}", m.mark, text[0]),
                'E' => {
                    let t = text.pop_front().unwrap();
                    out.push(format!("{t}{}{}", m.mark, space(&m.mark)));
                    pos += 1;
                }
                'A' => {
                    out.push(format!("{}{}", m.mark, space(&m.mark)));
                    pos += 1;
                }
                _ if text.len() == 1 => text[0].push_str(&m.mark),
                _ => {
                    let first = text.pop_front().unwrap();
                    text[0] = format!("{first}{}{}", m.mark, text[0]);
                }
            }
        } else {
            out.push(text.pop_front().unwrap());
            pos += 1;
        }
    }
    out
}

/// The vocabulary of kokoro_onnx/config.json (phoneme char -> token id), read from the venv's copy.
static VOCAB: LazyLock<Result<BTreeMap<char, i64>, String>> = LazyLock::new(|| {
    let p = site_packages("wotr").map(|d| d.join("kokoro_onnx/config.json")).ok_or("kokoro-onnx is not installed: pip install kokoro-onnx soundfile lameenc")?;
    let v: Value = serde_json::from_slice(&std::fs::read(&p).map_err(|e| format!("{}: {e}", p.display()))?).map_err(|e| e.to_string())?;
    let vocab = v["vocab"].as_object().ok_or("config.json has no vocab")?;
    Ok(vocab.iter().filter_map(|(k, id)| Some((k.chars().next()?, id.as_i64()?))).collect())
});

fn vocab() -> Result<&'static BTreeMap<char, i64>, String> {
    VOCAB.as_ref().map_err(Clone::clone)
}

/// Tokenizer.phonemize(text, 'en-us'): phonemizer.phonemize, then only vocabulary characters, stripped.
pub fn phonemize(text: &str) -> Result<String, String> {
    let vocab = vocab()?;
    let guard = ESPEAK.lock().unwrap();
    let es = guard.as_ref().map_err(Clone::clone)?;
    let text = py_strip(text);
    let lines: Vec<&str> = text.trim_matches('\n').split('\n').map(|l| l.trim_matches('\n')).filter(|l| !py_strip(l).is_empty()).collect();
    let (mut chunks, mut marks) = (Vec::new(), Vec::new());
    for (num, line) in lines.iter().enumerate() {
        let (c, m) = preserve_line(line, num);
        chunks.extend(c);
        marks.extend(m);
    }
    chunks.retain(|c| !c.is_empty());
    let phonemized: Vec<String> = chunks.iter().map(|c| postprocess(&text_to_phonemes(es, c))).collect();
    let joined = if lines.is_empty() { String::new() } else { restore(phonemized, marks).join("\n") };
    Ok(py_strip(&joined.chars().filter(|c| vocab.contains_key(c)).collect::<String>()).to_string())
}

/// Kokoro._split_phonemes: batches under MAX_PHONEMES, cut at punctuation.
pub fn split_phonemes(ph: &str) -> Vec<String> {
    let mut parts = Vec::new();
    let mut cur = String::new();
    for c in ph.chars() {
        if ".,!?;".contains(c) {
            parts.push(std::mem::take(&mut cur));
            parts.push(c.to_string());
        } else {
            cur.push(c);
        }
    }
    parts.push(cur);
    let (mut out, mut batch) = (Vec::new(), String::new());
    for part in parts {
        let part = py_strip(&part);
        if part.is_empty() {
            continue;
        }
        if batch.chars().count() + part.chars().count() + 1 >= MAX_PHONEMES {
            out.push(py_strip(&batch).to_string());
            batch = part.to_string();
        } else if ".,!?;".contains(part) {
            batch.push_str(part);
        } else {
            if !batch.is_empty() {
                batch.push(' ');
            }
            batch.push_str(part);
        }
    }
    if !batch.is_empty() {
        out.push(py_strip(&batch).to_string());
    }
    out
}

/// The token ids of one batch, as _create_audio feeds them (before the 0 pads).
pub fn tokens(ph: &str) -> Result<Vec<i64>, String> {
    let vocab = vocab()?;
    Ok(ph.chars().take(MAX_PHONEMES).filter_map(|c| vocab.get(&c).copied()).collect())
}

pub struct Model {
    session: ort::session::Session,
    /// name -> [510, 1, 256] style rows, flattened
    pub voices: BTreeMap<String, Vec<f32>>,
}

const STYLE: usize = 256;

/// np.load of an npz (the voices pack: [510, 1, 256] float32 arrays), in archive order.
pub fn load_npz(path: &Path) -> Result<Vec<(String, Vec<f32>)>, String> {
    let f = std::fs::File::open(path).map_err(|e| format!("{}: {e}", path.display()))?;
    let mut z = zip::ZipArchive::new(f).map_err(|e| e.to_string())?;
    let mut out = Vec::new();
    for i in 0..z.len() {
        let mut e = z.by_index(i).map_err(|e| e.to_string())?;
        let name = e.name().map_err(|e| e.to_string())?.trim_end_matches(".npy").to_string();
        let mut buf = Vec::new();
        std::io::Read::read_to_end(&mut e, &mut buf).map_err(|e| e.to_string())?;
        out.push((name, crate::embed::npy_f32(&buf)?));
    }
    Ok(out)
}

impl Model {
    pub fn load(model: &Path, voices: &Path) -> Result<Model, String> {
        let env = crate::embed::ENV.as_ref().map_err(Clone::clone)?;
        let session = ort::session::Session::builder(env).and_then(|mut b| b.commit_from_file(model)).map_err(|e| e.to_string())?;
        Ok(Model { session, voices: load_npz(voices)?.into_iter().collect() })
    }

    fn create_audio(&mut self, ph: &str, style: &[f32], speed: f32) -> Result<Vec<f32>, String> {
        let toks = tokens(ph)?;
        let row = style.get(toks.len() * STYLE..(toks.len() + 1) * STYLE).ok_or_else(|| format!("IndexError: index {} is out of bounds for axis 0 with size 510", toks.len()))?;
        let mut ids = vec![0i64];
        ids.extend(&toks);
        ids.push(0);
        let t = |e: ort::Error| e.to_string();
        let inputs = ort::inputs![
            "tokens" => ort::value::Tensor::from_array(([1usize, ids.len()], ids)).map_err(t)?,
            "style" => ort::value::Tensor::from_array(([1usize, STYLE], row.to_vec())).map_err(t)?,
            "speed" => ort::value::Tensor::from_array(([1usize], vec![speed])).map_err(t)?,
        ];
        let out = self.session.run(inputs).map_err(t)?;
        Ok(out["audio"].try_extract_tensor::<f32>().map_err(t)?.1.to_vec())
    }

    /// Kokoro.create(text, voice=style, speed, lang='en-us'): the samples at 24 kHz.
    pub fn create(&mut self, text: &str, style: &[f32], speed: f64) -> Result<Vec<f32>, String> {
        if !(0.5..=2.0).contains(&speed) {
            return Err("AssertionError: Speed should be between 0.5 and 2.0".into());
        }
        let mut audio = Vec::new();
        for b in split_phonemes(&phonemize(text)?) {
            let part = self.create_audio(&b, style, speed as f32)?;
            audio.extend_from_slice(trim(&part));
        }
        Ok(audio)
    }
}

/// numpy's pairwise float32 sum (umath's pairwise_sum_FLOAT), which np.mean uses along a contiguous axis.
fn pairwise(a: &[f32]) -> f32 {
    let n = a.len();
    if n < 8 {
        return a.iter().fold(0.0f32, |r, x| r + x);
    }
    if n <= 128 {
        let mut r: [f32; 8] = a[..8].try_into().unwrap();
        let mut i = 8;
        while i < n - n % 8 {
            for j in 0..8 {
                r[j] += a[i + j];
            }
            i += 8;
        }
        let mut res = ((r[0] + r[1]) + (r[2] + r[3])) + ((r[4] + r[5]) + (r[6] + r[7]));
        for x in &a[i..] {
            res += x;
        }
        return res;
    }
    let n2 = n / 2 - (n / 2) % 8;
    pairwise(&a[..n2]) + pairwise(&a[n2..])
}

/// kokoro_onnx.trim.trim(y): top_db 60 against the loudest frame, 2048-sample frames every 512.
pub fn trim(y: &[f32]) -> &[f32] {
    let mut padded = vec![0f32; y.len() + 2048];
    padded[1024..1024 + y.len()].copy_from_slice(y);
    let frames = 1 + y.len() / 512;
    let rms: Vec<f32> = (0..frames).map(|f| {
        let sq: Vec<f32> = padded[f * 512..f * 512 + 2048].iter().map(|x| x * x).collect();
        ((0.0f32 + pairwise(&sq)) / 2048.0).sqrt()
    }).collect();
    let reference = rms.iter().fold(f32::NEG_INFINITY, |m, x| m.max(x.abs()));
    let ref_db = 10.0f32 * (reference * reference).max(1e-10).log10();
    let loud: Vec<usize> = rms.iter().enumerate().filter(|(_, m)| 10.0f32 * (m.abs() * m.abs()).max(1e-10).log10() - ref_db > -60.0).map(|(i, _)| i).collect();
    match (loud.first(), loud.last()) {
        (Some(a), Some(b)) => &y[a * 512..((b + 1) * 512).min(y.len())],
        _ => &y[..0],
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn punctuation_round_trip() {
        let (chunks, marks) = preserve_line("\"Hello, there.\" He left.", 0);
        assert_eq!(chunks, ["", "Hello", "there", "He left", ""]);
        assert_eq!(marks.iter().map(|m| m.pos).collect::<String>(), "BIIE");
        let ph: Vec<String> = ["hə ", "ðɛɹ ", "hi lɛft "].iter().map(|s| s.to_string()).collect();
        assert_eq!(restore(ph, marks), ["\"hə, ðɛɹ.\" hi lɛft. "]);
        assert_eq!(split_phonemes("a, b. c"), ["a, b. c"]);
        assert_eq!(pairwise(&[1.0; 300]), 300.0);
    }
}
