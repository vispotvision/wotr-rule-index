//! Supertonic 3 as the `supertonic` 1.3.1 package runs it in build/supertonic_worker.py, ported: the
//! UnicodeProcessor's text cleaning and indexing, chunk_text, the four ONNX graphs (duration, text
//! encoder, the flow-matching vector estimator stepped `steps` times, vocoder) and the noise it
//! starts from: numpy's legacy np.random.randn (MT19937, polar Gauss), so a seeded run reproduces
//! the Python sample for sample (WOTR_SUPERTONIC_SEED, which rust/audio_parity.py also gives the
//! Python worker). Unseeded, like the worker, every take draws fresh noise.
use crate::util::env_path;
use fancy_regex::Regex;
use serde_json::Value;
use std::path::{Path, PathBuf};
use std::sync::LazyLock;
use unicode_normalization::UnicodeNormalization;

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

/// numpy.random.RandomState: MT19937 and legacy_gauss.
struct Mt {
    key: [u32; 624],
    pos: usize,
    gauss: Option<f64>,
}

impl Mt {
    /// mt19937_seed (np.random.seed(int))
    fn new(mut seed: u32) -> Mt {
        let mut key = [0u32; 624];
        for (pos, k) in key.iter_mut().enumerate() {
            *k = seed;
            seed = 1812433253u32.wrapping_mul(seed ^ (seed >> 30)).wrapping_add(pos as u32 + 1);
        }
        Mt { key, pos: 624, gauss: None }
    }

    fn next(&mut self) -> u32 {
        if self.pos == 624 {
            let k = &mut self.key;
            for i in 0..624 {
                let y = (k[i] & 0x8000_0000) | (k[(i + 1) % 624] & 0x7fff_ffff);
                k[i] = k[(i + 397) % 624] ^ (y >> 1) ^ if y & 1 == 1 { 0x9908_b0df } else { 0 };
            }
            self.pos = 0;
        }
        let mut y = self.key[self.pos];
        self.pos += 1;
        y ^= y >> 11;
        y ^= (y << 7) & 0x9d2c_5680;
        y ^= (y << 15) & 0xefc6_0000;
        y ^ (y >> 18)
    }

    fn double(&mut self) -> f64 {
        let (a, b) = ((self.next() >> 5) as f64, (self.next() >> 6) as f64);
        (a * 67108864.0 + b) / 9007199254740992.0
    }

    fn gauss(&mut self) -> f64 {
        if let Some(g) = self.gauss.take() {
            return g;
        }
        loop {
            let (x1, x2) = (2.0 * self.double() - 1.0, 2.0 * self.double() - 1.0);
            let r2 = x1 * x1 + x2 * x2;
            if r2 < 1.0 && r2 != 0.0 {
                let f = (-2.0 * r2.ln() / r2).sqrt();
                self.gauss = Some(f * x1);
                return f * x2;
            }
        }
    }
}

pub struct Tts {
    dp: ort::session::Session,
    enc: ort::session::Session,
    est: ort::session::Session,
    voc: ort::session::Session,
    indexer: Vec<i64>,
    pub sample_rate: usize,
    chunk: usize,
    ccf: usize,
    ldim: usize,
    dir: PathBuf,
    rng: Mt,
}

pub struct Style {
    ttl: (Vec<i64>, Vec<f32>),
    dp: (Vec<i64>, Vec<f32>),
}

fn flat(v: &Value, out: &mut Vec<f32>) {
    match v {
        Value::Array(a) => a.iter().for_each(|x| flat(x, out)),
        x => out.push(x.as_f64().unwrap_or(f64::NAN) as f32),
    }
}

/// load_voice_style_from_json_file
pub fn style(path: &Path) -> Result<Style, String> {
    let v: Value = serde_json::from_slice(&std::fs::read(path).map_err(|_| format!("FileNotFoundError: Voice style file not found: {}", path.display()))?)
        .map_err(|_| format!("ValueError: Voice style file is malformed at {}. Please check the file format.", path.display()))?;
    let part = |k: &str| -> Result<(Vec<i64>, Vec<f32>), String> {
        let (dims, data) = (v[k]["dims"].as_array(), &v[k]["data"]);
        let dims: Vec<i64> = dims.ok_or_else(|| format!("ValueError: Invalid voice style format in {}. Expected 'style_ttl' and 'style_dp' with 'dims' and 'data' fields.", path.display()))?
            .iter().map(|d| d.as_i64().unwrap_or(0)).collect();
        let mut out = Vec::new();
        flat(data, &mut out);
        Ok((dims, out))
    };
    Ok(Style { ttl: part("style_ttl")?, dp: part("style_dp")? })
}

impl Tts {
    /// TTS(auto_download=True) on the cached supertonic-3 files (~/.cache/supertonic3, SUPERTONIC_CACHE_DIR).
    pub fn load() -> Result<Tts, String> {
        let dir = env_path("SUPERTONIC_CACHE_DIR", Some("~/.cache/supertonic3")).unwrap();
        let onnx = dir.join("onnx");
        if !["duration_predictor", "text_encoder", "vector_estimator", "vocoder"].iter().all(|m| onnx.join(format!("{m}.onnx")).exists()) {
            // shortcut: the Python package downloads them from the hub; here build/supertonic_setup.sh does it once
            return Err(format!("Supertonic model files missing in {}: run build/supertonic_setup.sh", dir.display()));
        }
        let env = crate::embed::ENV.as_ref().map_err(Clone::clone)?;
        let open = |m: &str| ort::session::Session::builder(env).and_then(|mut b| b.commit_from_file(onnx.join(format!("{m}.onnx")))).map_err(|e| e.to_string());
        let cfg: Value = serde_json::from_slice(&std::fs::read(onnx.join("tts.json")).map_err(|e| e.to_string())?).map_err(|e| e.to_string())?;
        let idx: Value = serde_json::from_slice(&std::fs::read(onnx.join("unicode_indexer.json")).map_err(|e| e.to_string())?).map_err(|e| e.to_string())?;
        let n = |v: &Value| v.as_u64().unwrap_or(0) as usize;
        let seed = std::env::var("WOTR_SUPERTONIC_SEED").ok().and_then(|s| s.trim().parse().ok()).unwrap_or_else(|| {
            let t = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default();
            t.as_nanos() as u32 ^ std::process::id().rotate_left(16)
        });
        Ok(Tts {
            dp: open("duration_predictor")?,
            enc: open("text_encoder")?,
            est: open("vector_estimator")?,
            voc: open("vocoder")?,
            indexer: idx.as_array().ok_or("unicode_indexer.json is not a list")?.iter().map(|x| x.as_i64().unwrap_or(-1)).collect(),
            sample_rate: n(&cfg["ae"]["sample_rate"]),
            chunk: n(&cfg["ae"]["base_chunk_size"]),
            ccf: n(&cfg["ttl"]["chunk_compress_factor"]),
            ldim: n(&cfg["ttl"]["latent_dim"]),
            dir,
            rng: Mt::new(seed),
        })
    }

    pub fn preset(&self, name: &str) -> Result<Style, String> {
        let p = self.dir.join("voice_styles").join(format!("{name}.json"));
        if !p.exists() {
            let mut names: Vec<String> = std::fs::read_dir(self.dir.join("voice_styles")).into_iter().flatten().flatten()
                .filter_map(|e| e.file_name().to_string_lossy().strip_suffix(".json").map(String::from)).collect();
            names.sort();
            return Err(format!("FileNotFoundError: Voice style '{name}' not found. Available voice styles: {}", names.join(", ")));
        }
        style(&p)
    }

    fn supported(&self, c: char) -> bool {
        self.indexer.get(c as usize).is_some_and(|&i| i != -1)
    }

    /// TTS.synthesize(text, style, steps, speed, lang='en', max_chunk_length=300, silence_duration=0.25)
    /// as the worker calls it (speed already clamped to 0.7..2.0): float32 samples at sample_rate.
    pub fn synthesize(&mut self, text: &str, style: &Style, steps: i64, speed: f64) -> Result<Vec<f32>, String> {
        if crate::kokoro::py_strip(text).is_empty() {
            return Err("ValueError: Text cannot be empty".into());
        }
        if text.chars().count() > 100000 {
            return Err(format!("ValueError: Text length ({}) exceeds maximum allowed length (100000). Please split your text into smaller chunks.", text.chars().count()));
        }
        if !(1..=100).contains(&steps) {
            return Err(format!("ValueError: total_steps must be between 1 and 100, got {steps}. Higher values = better quality but slower."));
        }
        let mut bad: Vec<char> = Vec::new();
        for c in text.chars() {
            if !bad.contains(&c) && preprocess(&c.to_string(), None).chars().any(|p| !self.supported(p)) {
                bad.push(c);
            }
        }
        if !bad.is_empty() {
            bad.sort();
            let list: Vec<String> = bad.iter().map(|c| crate::analysis::py_repr(&c.to_string())).collect();
            return Err(format!("ValueError: Found {} unsupported character(s): [{}]", bad.len(), list.join(", ")));
        }
        let silence = (0.25 * self.sample_rate as f64) as usize;
        let mut wav = Vec::new();
        for (i, chunk) in chunk_text(text, 300).iter().enumerate() {
            if i > 0 {
                wav.extend(std::iter::repeat_n(0f32, silence));
            }
            wav.extend(self.infer(chunk, style, steps, speed)?);
        }
        Ok(wav)
    }

    /// Supertonic.__call__ for one chunk.
    fn infer(&mut self, chunk: &str, style: &Style, steps: i64, speed: f64) -> Result<Vec<f32>, String> {
        let text = preprocess(chunk, Some("en"));
        let ids: Vec<i64> = text.chars().map(|c| self.indexer.get(c as u32 as u16 as usize).copied().unwrap_or(-1)).collect();
        let n = ids.len();
        let t = |e: ort::Error| e.to_string();
        use ort::value::Tensor;
        let tensor = |shape: Vec<i64>, v: Vec<f32>| Tensor::from_array((shape, v)).map_err(t);
        let ids_t = || Tensor::from_array(([1usize, n], ids.clone())).map_err(t);
        let mask_t = || Tensor::from_array(([1usize, 1, n], vec![1f32; n])).map_err(t);
        let dur = {
            let out = self.dp.run(ort::inputs!["text_ids" => ids_t()?, "style_dp" => tensor(style.dp.0.clone(), style.dp.1.clone())?, "text_mask" => mask_t()?]).map_err(t)?;
            out["duration"].try_extract_tensor::<f32>().map_err(t)?.1[0] / speed as f32
        };
        let (emb_shape, emb) = {
            let out = self.enc.run(ort::inputs!["text_ids" => ids_t()?, "style_ttl" => tensor(style.ttl.0.clone(), style.ttl.1.clone())?, "text_mask" => mask_t()?]).map_err(t)?;
            let (s, d) = out["text_emb"].try_extract_tensor::<f32>().map_err(t)?;
            (s.to_vec(), d.to_vec())
        };
        // sample_noisy_latent, in numpy's float32 arithmetic
        let sr = self.sample_rate as f32;
        let chunk_size = self.chunk * self.ccf;
        let wav_len = (dur * sr) as i64;
        let latent_len = ((dur * sr + (chunk_size - 1) as f32) / chunk_size as f32) as usize;
        let mask_len = ((wav_len + chunk_size as i64 - 1) / chunk_size as i64) as usize;
        if mask_len != latent_len && mask_len != 1 {
            return Err(format!("ValueError: operands could not be broadcast together with shapes (1,{},{latent_len}) (1,1,{mask_len})", self.ldim * self.ccf));
        }
        let dim = self.ldim * self.ccf;
        let mut xt: Vec<f32> = (0..dim * latent_len).map(|_| self.rng.gauss() as f32).collect();
        let mask = vec![1f32; mask_len];
        for (i, x) in xt.iter_mut().enumerate() {
            *x *= mask[if mask_len == 1 { 0 } else { i % latent_len }];
        }
        let total = vec![steps as f32];
        for step in 0..steps {
            let out = self.est.run(ort::inputs![
                "noisy_latent" => tensor(vec![1, dim as i64, latent_len as i64], xt)?,
                "text_emb" => tensor(emb_shape.clone(), emb.clone())?,
                "style_ttl" => tensor(style.ttl.0.clone(), style.ttl.1.clone())?,
                "text_mask" => mask_t()?,
                "latent_mask" => tensor(vec![1, 1, mask_len as i64], mask.clone())?,
                "current_step" => tensor(vec![1], vec![step as f32])?,
                "total_step" => tensor(vec![1], total.clone())?,
            ]).map_err(t)?;
            xt = out["denoised_latent"].try_extract_tensor::<f32>().map_err(t)?.1.to_vec();
        }
        let out = self.voc.run(ort::inputs!["latent" => tensor(vec![1, dim as i64, latent_len as i64], xt)?]).map_err(t)?;
        Ok(out["wav_tts"].try_extract_tensor::<f32>().map_err(t)?.1.to_vec())
    }
}

/// UnicodeProcessor._preprocess_text
pub fn preprocess(text: &str, lang: Option<&str>) -> String {
    let mut s: String = text.nfkd().collect();
    s = rx!("[\u{1f600}-\u{1f64f}\u{1f300}-\u{1f5ff}\u{1f680}-\u{1f6ff}\u{1f700}-\u{1f77f}\u{1f780}-\u{1f7ff}\u{1f800}-\u{1f8ff}\u{1f900}-\u{1f9ff}\u{1fa00}-\u{1fa6f}\u{1fa70}-\u{1faff}\u{2600}-\u{26ff}\u{2700}-\u{27bf}\u{1f1e6}-\u{1f1ff}]+")
        .replace_all(&s, "").into_owned();
    for (a, b) in [("–", "-"), ("‑", "-"), ("—", "-"), ("¯", " "), ("_", " "), ("“", "\""), ("”", "\""), ("‘", "'"), ("’", "'"), ("´", "'"), ("`", "'"),
                   ("[", " "), ("]", " "), ("|", " "), ("/", " "), ("#", " "), ("→", " "), ("←", " ")] {
        s = s.replace(a, b);
    }
    s = rx!(r"[♥☆♡©\\]").replace_all(&s, "").into_owned();
    for (a, b) in [("@", " at "), ("e.g.,", "for example, "), ("i.e.,", "that is, ")] {
        s = s.replace(a, b);
    }
    for (a, b) in [(" ,", ","), (" .", "."), (" !", "!"), (" ?", "?"), (" ;", ";"), (" :", ":"), (" '", "'")] {
        s = s.replace(a, b);
    }
    s = rx!(r#"(["'`])\1+"#).replace_all(&s, "$1").into_owned();
    s = crate::kokoro::py_strip(&rx!(r"\s+").replace_all(&s, " ")).to_string();
    if !rx!(r#"[.!?;:,'"')\]}…。」』】〉》›»]$"#).is_match(&s).unwrap_or(false) {
        s.push('.');
    }
    match lang {
        Some(l) => format!("<{l}>{s}</{l}>"),
        None => s,
    }
}

/// utils.chunk_text: paragraphs, then sentences (not after a common abbreviation) packed to max_len.
pub fn chunk_text(text: &str, max_len: usize) -> Vec<String> {
    let sent = rx!(r"(?<!Mr\.)(?<!Mrs\.)(?<!Ms\.)(?<!Dr\.)(?<!Prof\.)(?<!Sr\.)(?<!Jr\.)(?<!Ph\.D\.)(?<!etc\.)(?<!e\.g\.)(?<!i\.e\.)(?<!vs\.)(?<!Inc\.)(?<!Ltd\.)(?<!Co\.)(?<!Corp\.)(?<!St\.)(?<!Ave\.)(?<!Blvd\.)(?<!\b[A-Z]\.)(?<=[.!?])\s+");
    let mut chunks = Vec::new();
    for para in rx!(r"\n\s*\n+").split(crate::kokoro::py_strip(text)).flatten() {
        let para = crate::kokoro::py_strip(para);
        if para.is_empty() {
            continue;
        }
        let mut cur = String::new();
        for s in sent.split(para).flatten() {
            let s = crate::kokoro::py_strip(s);
            if s.is_empty() {
                continue;
            }
            if cur.chars().count() + s.chars().count() + 1 <= max_len {
                if !cur.is_empty() {
                    cur.push(' ');
                }
                cur.push_str(s);
            } else {
                if !cur.is_empty() {
                    chunks.push(crate::kokoro::py_strip(&cur).to_string());
                }
                cur = s.to_string();
            }
        }
        if !crate::kokoro::py_strip(&cur).is_empty() {
            chunks.push(crate::kokoro::py_strip(&cur).to_string());
        }
    }
    chunks
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn numpy_randn_and_text() {
        // np.random.seed(7); np.random.randn(3)
        let mut m = Mt::new(7);
        let g: Vec<f64> = (0..3).map(|_| m.gauss()).collect();
        assert_eq!(g, [1.690525703800356, -0.4659373705408328, 0.0328201636785844]);
        assert_eq!(preprocess("“Hi” — e.g., you…", Some("en")), "<en>\"Hi\" - for example, you...</en>");
        assert_eq!(chunk_text("Mr. Smith ran. It rained! Done", 20), ["Mr. Smith ran.", "It rained! Done"]);
    }
}
