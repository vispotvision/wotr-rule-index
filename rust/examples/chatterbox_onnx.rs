//! Feasibility test, not production: Chatterbox Turbo (Resemble AI's official ONNX export, fp32) in
//! Rust through the system ONNX Runtime (onnxruntime-opt-rocm, /usr/lib/libonnxruntime.so), on the
//! CPU or the RX 9070 XT through MIGraphX. Follows the model card's onnxruntime example
//! (huggingface.co/ResembleAI/chatterbox-turbo-ONNX): speech_encoder on the reference clip,
//! embed_tokens, the GPT-2 language model with its KV cache, conditional_decoder to 24 kHz.
//! A separate binary because one process can load only one ONNX Runtime and wotr-mcp loads the venv's.
//!
//!   cargo run --release --example chatterbox_onnx -- --ep migraphx --jobs jobs.tsv [--greedy] [--seed 7]
//!       [--norm-loudness] [--cpu-graphs language_model,embed_tokens] [--warmup 1] [--device 0] [--decoder x.onnx]
//!   jobs.tsv: one job per line, `ref.wav<TAB>out.wav<TAB>text`; one JSON line of timings per job on stdout.
use ort::ep::{ExecutionProviderDispatch, MIGraphX, CPU};
use ort::session::{Session, SessionInputValue};
use ort::value::{DynValue, Tensor};
use serde_json::json;
use std::borrow::Cow;
use std::path::{Path, PathBuf};
use std::time::Instant;

const SR: u32 = 24000;
const START: i64 = 6561;
const STOP: i64 = 6562;
const SILENCE: i64 = 4299;
const LAYERS: usize = 24;
const HEADS: usize = 16;
const HEAD_DIM: usize = 64;
const MAX_NEW: usize = 1000; // tts_turbo.py's max_gen_len
const GRAPHS: [&str; 4] = ["speech_encoder", "embed_tokens", "language_model", "conditional_decoder"];

type R<T> = Result<T, String>;
fn e<E: std::fmt::Display>(x: E) -> String {
    x.to_string()
}

struct Opts {
    ep: String,
    cpu_graphs: Vec<String>,
    device: i32,
    greedy: bool,
    seed: u64,
    norm_loudness: bool,
    warmup: usize,
    jobs: PathBuf,
    verbose: bool,
    decoder: Option<PathBuf>,
    kv_max: usize,
    iobind: bool,
    prefill: usize,
    lufs: bool,
}

fn parse_args() -> R<Opts> {
    let mut o = Opts { ep: "cpu".into(), cpu_graphs: vec![], device: 0, greedy: false, seed: 0, norm_loudness: false, warmup: 0, jobs: PathBuf::new(), verbose: false, decoder: None, kv_max: 0, iobind: false, prefill: 0, lufs: false };
    let mut a = std::env::args().skip(1);
    while let Some(k) = a.next() {
        let mut v = || a.next().ok_or(format!("{k} needs a value"));
        match k.as_str() {
            "--ep" => o.ep = v()?,
            "--cpu-graphs" => o.cpu_graphs = v()?.split(',').map(String::from).collect(),
            "--device" => o.device = v()?.parse().map_err(e)?,
            "--greedy" => o.greedy = true,
            "--seed" => o.seed = v()?.parse().map_err(e)?,
            "--norm-loudness" => o.norm_loudness = true,
            "--warmup" => o.warmup = v()?.parse().map_err(e)?,
            "--jobs" => o.jobs = v()?.into(),
            "--verbose" => o.verbose = true,
            // fixed-size KV cache (GroupQueryAttention's shared-buffer form): past/present stay [1,16,N,64]
            // and the mask [1,N] marks the filled slots, so every decode step has one shape
            "--iobind" => o.iobind = true,
            "--prefill" => o.prefill = v()?.parse().map_err(e)?, // fixed-KV: one padded prefill length for every line
            "--lufs" => o.lufs = true,                            // print each job's ref loudness and stop
            "--kv-max" => o.kv_max = v()?.parse().map_err(e)?,
            "--decoder" => o.decoder = Some(v()?.into()), // another conditional_decoder.onnx (the seeded copy for parity)
            _ => return Err(format!("unknown argument {k}")),
        }
    }
    if o.jobs.as_os_str().is_empty() {
        return Err("--jobs <file.tsv> is required".into());
    }
    Ok(o)
}

// ---------------------------------------------------------------- audio in and out

/// A PCM16 or float32 WAV as float samples, mono, at 24 kHz (librosa.load(path, sr=24000) for clips
/// already at 24 kHz). shortcut: no resampling; every WOTR ref clip is 24 kHz mono, add it when one is not.
fn read_wav(p: &Path) -> R<Vec<f32>> {
    let b = std::fs::read(p).map_err(|x| format!("{}: {x}", p.display()))?;
    if b.len() < 12 || &b[..4] != b"RIFF" || &b[8..12] != b"WAVE" {
        return Err(format!("{}: not a WAV file", p.display()));
    }
    let (mut i, mut fmt, mut data) = (12, None, None);
    while i + 8 <= b.len() {
        let id = &b[i..i + 4];
        let n = u32::from_le_bytes(b[i + 4..i + 8].try_into().unwrap()) as usize;
        let body = &b[i + 8..(i + 8 + n).min(b.len())];
        if id == b"fmt " {
            fmt = Some((u16::from_le_bytes([body[0], body[1]]), u16::from_le_bytes([body[2], body[3]]), u32::from_le_bytes(body[4..8].try_into().unwrap()), u16::from_le_bytes([body[14], body[15]])));
        } else if id == b"data" {
            data = Some(body);
        }
        i += 8 + n + (n & 1);
    }
    let ((format, ch, sr, bits), data) = (fmt.ok_or("no fmt chunk")?, data.ok_or("no data chunk")?);
    if sr != SR || ch != 1 {
        return Err(format!("{}: {sr} Hz, {ch} channels; this test reads 24 kHz mono only", p.display()));
    }
    match (format, bits) {
        (1, 16) => Ok(data.chunks_exact(2).map(|c| i16::from_le_bytes([c[0], c[1]]) as f32 / 32768.0).collect()),
        (3, 32) => Ok(data.chunks_exact(4).map(|c| f32::from_le_bytes(c.try_into().unwrap())).collect()),
        _ => Err(format!("{}: WAV format {format}/{bits} bits not handled", p.display())),
    }
}

/// soundfile.write(path, x, 24000) as PCM_16 (the same rounding as rust/src/audio.rs).
fn write_wav(p: &Path, x: &[f32]) -> R<()> {
    let n = x.len() as u32 * 2;
    let mut b = Vec::with_capacity(44 + n as usize);
    b.extend(b"RIFF");
    b.extend((36 + n).to_le_bytes());
    b.extend(b"WAVEfmt ");
    for v in [16u32.to_le_bytes(), [1, 0, 1, 0], SR.to_le_bytes(), (SR * 2).to_le_bytes(), [2, 0, 16, 0]] {
        b.extend(v);
    }
    b.extend(b"data");
    b.extend(n.to_le_bytes());
    for s in x {
        let t = (*s as f64 * 2147483648.0).round_ties_even().clamp(-2147483648.0, 2147483647.0) as i32;
        b.extend(((t >> 16) as i16).to_le_bytes());
    }
    if let Some(d) = p.parent() {
        std::fs::create_dir_all(d).map_err(e)?;
    }
    std::fs::write(p, b).map_err(e)
}

/// pyloudnorm Meter(24000).integrated_loudness: BS.1770-4 K-weighting (RBJ high shelf then high pass,
/// lfilter direct form), 400 ms blocks at 75% overlap, -70 LUFS absolute and -10 LU relative gates.
fn integrated_loudness(x: &[f32]) -> f64 {
    let rate = SR as f64;
    let biquad = |g: f64, q: f64, fc: f64, shelf: bool| {
        let a = 10f64.powf(g / 40.0);
        let w0 = 2.0 * std::f64::consts::PI * fc / rate;
        let (c, alpha) = (w0.cos(), w0.sin() / (2.0 * q));
        let (b, aa) = if shelf {
            let s = 2.0 * a.sqrt() * alpha;
            ([a * ((a + 1.0) + (a - 1.0) * c + s), -2.0 * a * ((a - 1.0) + (a + 1.0) * c), a * ((a + 1.0) + (a - 1.0) * c - s)], [(a + 1.0) - (a - 1.0) * c + s, 2.0 * ((a - 1.0) - (a + 1.0) * c), (a + 1.0) - (a - 1.0) * c - s])
        } else {
            ([(1.0 + c) / 2.0, -(1.0 + c), (1.0 + c) / 2.0], [1.0 + alpha, -2.0 * c, 1.0 - alpha])
        };
        (b.map(|v| v / aa[0]), [1.0, aa[1] / aa[0], aa[2] / aa[0]])
    };
    let mut y: Vec<f64> = x.iter().map(|v| *v as f64).collect();
    for (b, a) in [biquad(4.0, 1.0 / 2f64.sqrt(), 1500.0, true), biquad(0.0, 0.5, 38.0, false)] {
        let (mut z1, mut z2) = (0.0, 0.0); // transposed direct form II, as scipy's lfilter
        for v in y.iter_mut() {
            let out = b[0] * *v + z1;
            z1 = b[1] * *v - a[1] * out + z2;
            z2 = b[2] * *v - a[2] * out;
            *v = out;
        }
    }
    let (tg, step) = (0.4, 0.25);
    let t = y.len() as f64 / rate;
    let blocks = (((t - tg) / (tg * step)).round() as i64 + 1).max(0) as usize;
    let z: Vec<f64> = (0..blocks)
        .map(|j| {
            let (l, u) = ((tg * (j as f64 * step) * rate) as usize, ((tg * (j as f64 * step + 1.0) * rate) as usize).min(y.len()));
            y[l..u].iter().map(|v| v * v).sum::<f64>() / (tg * rate)
        })
        .collect();
    let lk = |v: f64| -0.691 + 10.0 * v.log10();
    let mean = |s: &[f64]| if s.is_empty() { 0.0 } else { s.iter().sum::<f64>() / s.len() as f64 };
    let abs: Vec<f64> = z.iter().copied().filter(|v| lk(*v) >= -70.0).collect();
    let gamma_r = lk(mean(&abs)) - 10.0;
    let rel: Vec<f64> = z.iter().copied().filter(|v| lk(*v) > gamma_r && lk(*v) > -70.0).collect();
    lk(mean(&rel))
}

/// ChatterboxTurboTTS.norm_loudness(wav, sr, target_lufs=-27).
fn norm_loudness(x: &mut [f32]) {
    let gain = 10f64.powf((-27.0 - integrated_loudness(x)) / 20.0);
    if gain.is_finite() && gain > 0.0 {
        x.iter_mut().for_each(|v| *v = (*v as f64 * gain) as f32);
    }
}

/// tts_turbo.py's punc_norm.
fn punc_norm(text: &str) -> String {
    if text.is_empty() {
        return "You need to add some text for me to talk.".into();
    }
    let mut t: String = text.split_whitespace().collect::<Vec<_>>().join(" ");
    if let Some(c) = t.chars().next().filter(|c| c.is_lowercase()) {
        t = c.to_uppercase().chain(t.chars().skip(1)).collect();
    }
    for (a, b) in [("…", ", "), (":", ","), ("—", "-"), ("–", "-"), (" ,", ","), ("“", "\""), ("”", "\""), ("‘", "'"), ("’", "'")] {
        t = t.replace(a, b);
    }
    let t = t.trim_end_matches(' ').to_string();
    if [".", "!", "?", "-", ","].iter().any(|p| t.ends_with(p)) { t } else { t + "." }
}

// ---------------------------------------------------------------- sampling

/// splitmix64: a fixed seed gives a fixed run (not torch's generator, so sampled runs differ from PyTorch's).
struct Rng(u64);
impl Rng {
    fn next_f64(&mut self) -> f64 {
        self.0 = self.0.wrapping_add(0x9E3779B97F4A7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
        ((z ^ (z >> 31)) >> 11) as f64 / (1u64 << 53) as f64
    }
}

fn repetition_penalty(logits: &mut [f32], seen: &[i64], p: f32) {
    let mut done = vec![false; logits.len()];
    for &t in seen {
        let t = t as usize;
        if t < logits.len() && !done[t] {
            done[t] = true;
            logits[t] = if logits[t] < 0.0 { logits[t] * p } else { logits[t] / p };
        }
    }
}

fn argmax(x: &[f32]) -> i64 {
    // np.argmax: the first maximum
    x.iter().enumerate().fold((0, f32::NEG_INFINITY), |b, (i, v)| if *v > b.1 { (i, *v) } else { b }).0 as i64
}

/// inference_turbo's processors in its order: temperature 0.8, top_k 1000, top_p 0.95, then the
/// repetition penalty 1.2, softmax, one multinomial draw.
fn sample(logits: &mut [f32], seen: &[i64], rng: &mut Rng) -> i64 {
    logits.iter_mut().for_each(|v| *v /= 0.8);
    let mut sorted: Vec<f32> = logits.to_vec();
    sorted.sort_by(|a, b| b.total_cmp(a));
    let kth = sorted[999.min(sorted.len() - 1)];
    logits.iter_mut().for_each(|v| if *v < kth { *v = f32::NEG_INFINITY });
    // TopPLogitsWarper: drop the low tail whose cumulative probability is <= 1 - top_p, keep at least one
    let mut idx: Vec<usize> = (0..logits.len()).collect();
    idx.sort_by(|a, b| logits[*a].total_cmp(&logits[*b]));
    let m = logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let ex: Vec<f64> = idx.iter().map(|i| ((logits[*i] - m) as f64).exp()).collect();
    let total: f64 = ex.iter().sum();
    let mut cum = 0.0;
    for (k, i) in idx.iter().enumerate() {
        cum += ex[k] / total;
        if cum <= 0.05 && k + 1 < idx.len() {
            logits[*i] = f32::NEG_INFINITY;
        }
    }
    repetition_penalty(logits, seen, 1.2);
    let m = logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let p: Vec<f64> = logits.iter().map(|v| ((v - m) as f64).exp()).collect();
    let mut r = rng.next_f64() * p.iter().sum::<f64>();
    for (i, v) in p.iter().enumerate() {
        r -= v;
        if r < 0.0 {
            return i as i64;
        }
    }
    argmax(logits)
}

// ---------------------------------------------------------------- the pipeline

struct Model {
    enc: Session,
    embed: Session,
    lm: Session,
    lm_dec: Option<Session>,     // --iobind: a second language_model session that only ever sees the decode shape
    _alloc: Option<ort::memory::Allocator>,
    kv: Option<Vec<Tensor<f32>>>, // --iobind: the KV cache on the card, [1,16,kv_max,64] per layer and key/value
    dec: Session,
    tok: tokenizers::Tokenizer,
}

fn f32_tensor(shape: Vec<usize>, v: Vec<f32>) -> R<DynValue> {
    Tensor::from_array((shape, v)).map(|t| t.into_dyn()).map_err(e)
}
fn i64_tensor(shape: Vec<usize>, v: Vec<i64>) -> R<DynValue> {
    Tensor::from_array((shape, v)).map(|t| t.into_dyn()).map_err(e)
}

impl Model {
    fn embed(&mut self, ids: Vec<i64>) -> R<(usize, Vec<f32>)> {
        let n = ids.len();
        let out = self.embed.run(ort::inputs!["input_ids" => i64_tensor(vec![1, n], ids)?]).map_err(e)?;
        let (_, d) = out["inputs_embeds"].try_extract_tensor::<f32>().map_err(e)?;
        Ok((n, d.to_vec()))
    }

    /// One utterance: (waveform, speech tokens, per-stage seconds).
    fn generate(&mut self, text: &str, ref_audio: &[f32], greedy: bool, kv_max: usize, prefill: usize, rng: &mut Rng) -> R<(Vec<f32>, Vec<i64>, serde_json::Value)> {
        let t0 = Instant::now();
        let enc = self.tok.encode(text, true).map_err(e)?;
        let ids: Vec<i64> = enc.get_ids().iter().map(|x| *x as i64).collect();
        let (n_text, text_emb) = self.embed(ids)?;

        let mut out = self.enc.run(ort::inputs!["audio_values" => f32_tensor(vec![1, ref_audio.len()], ref_audio.to_vec())?]).map_err(e)?;
        let (cs, cond) = out["audio_features"].try_extract_tensor::<f32>().map_err(e)?;
        let n_cond = cs[1] as usize;
        let mut emb = cond.to_vec();
        let prompt = out.remove("audio_tokens").ok_or("no audio_tokens")?;
        let spk = out.remove("speaker_embeddings").ok_or("no speaker_embeddings")?;
        let feat = out.remove("speaker_features").ok_or("no speaker_features")?;
        drop(out);
        let t_enc = t0.elapsed().as_secs_f64();
        emb.extend(text_emb);

        let p = n_cond + n_text;
        if kv_max > 0 && p.div_ceil(64).max(prefill.div_ceil(64)) * 64 + MAX_NEW + 1 > kv_max {
            return Err(format!("--kv-max {kv_max} is under the prompt ({p}) plus {MAX_NEW} new tokens"));
        }
        // Fixed-KV mode pads the prefill to a multiple of 64 so MIGraphX compiles a few prefill shapes, not one per
        // line. The pad rows sit causally after the prompt, and the slot each would occupy is written by a generated
        // token before the mask ever reaches it.
        let pre = if kv_max == 0 { p } else if p <= prefill { prefill } else { p.div_ceil(64) * 64 };
        emb.resize(pre * 1024, 0.0);
        let mask = |filled: usize| if kv_max > 0 { i64_tensor(vec![1, kv_max], (0..kv_max).map(|i| (i < filled) as i64).collect()) } else { i64_tensor(vec![1, filled], vec![1; filled]) };
        let name = |i: usize, out: bool| format!("{}.{}.{}", if out { "present" } else { "past_key_values" }, i / 2, if i % 2 == 0 { "key" } else { "value" });
        let pick = |logits: &[f32], row: usize| logits[row * 6563..(row + 1) * 6563].to_vec();

        let t1 = Instant::now();
        let mut inputs: Vec<(Cow<str>, SessionInputValue)> = vec![
            ("inputs_embeds".into(), f32_tensor(vec![1, pre, 1024], emb)?.into()),
            ("attention_mask".into(), mask(pre)?.into()),
            ("position_ids".into(), i64_tensor(vec![1, pre], (0..pre as i64).collect())?.into()),
        ];
        for i in 0..LAYERS * 2 {
            inputs.push((name(i, false).into(), f32_tensor(vec![1, HEADS, kv_max, HEAD_DIM], vec![0.0; HEADS * kv_max * HEAD_DIM])?.into()));
        }
        let mut o = self.lm.run(inputs).map_err(e)?;
        let mut last = pick(o["logits"].try_extract_tensor::<f32>().map_err(e)?.1, p - 1);
        let mut past: Vec<DynValue> = (0..LAYERS * 2).map(|i| o.remove(name(i, true)).ok_or("no present".to_string())).collect::<R<_>>()?;
        drop(o);
        let t_prefill = t1.elapsed().as_secs_f64();

        // io binding (--iobind): the KV cache lives on the card, each present bound onto its own past buffer
        let dec = self.lm_dec.as_mut().unwrap_or(&mut self.lm);
        let mut bind = match self.kv.as_mut() {
            Some(kv) => {
                let mut b = dec.create_binding().map_err(e)?;
                for (i, v) in past.iter().enumerate() {
                    b.bind_input(name(i, false), v).map_err(e)?;
                }
                for (i, t) in kv.iter_mut().enumerate() {
                    b.bind_output(name(i, true), t).map_err(e)?;
                }
                b.bind_output_to_device("logits", &ort::memory::MemoryInfo::default()).map_err(e)?;
                Some(b)
            }
            None => None,
        };
        let mut generated: Vec<i64> = vec![START];
        let (mut t_embed, mut t_run) = (0.0, 0.0);
        for k in 0..MAX_NEW {
            let next = if greedy {
                repetition_penalty(&mut last, &generated, 1.2);
                argmax(&last)
            } else {
                sample(&mut last, &generated, rng)
            };
            generated.push(next);
            if next == STOP {
                break;
            }
            let pos = p + k;
            let te = Instant::now();
            let emb1 = f32_tensor(vec![1, 1, 1024], self.embed.run(ort::inputs!["input_ids" => i64_tensor(vec![1, 1], vec![next])?]).map_err(e)?["inputs_embeds"].try_extract_tensor::<f32>().map_err(e)?.1.to_vec())?;
            t_embed += te.elapsed().as_secs_f64();
            let tr = Instant::now();
            let dec = self.lm_dec.as_mut().unwrap_or(&mut self.lm);
            if let Some(b) = bind.as_mut() {
                b.bind_input("inputs_embeds", &emb1).map_err(e)?;
                b.bind_input("attention_mask", &mask(pos + 1)?).map_err(e)?;
                b.bind_input("position_ids", &i64_tensor(vec![1, 1], vec![pos as i64])?).map_err(e)?;
                let o = dec.run_binding(b).map_err(e)?;
                last = pick(o["logits"].try_extract_tensor::<f32>().map_err(e)?.1, 0);
                drop(o);
                t_run += tr.elapsed().as_secs_f64();
                if k == 0 {
                    for (i, t) in self.kv.as_ref().unwrap().iter().enumerate() {
                        b.bind_input(name(i, false), t).map_err(e)?;
                    }
                }
                continue;
            }
            let mut inputs: Vec<(Cow<str>, SessionInputValue)> = vec![
                ("inputs_embeds".into(), emb1.into()),
                ("attention_mask".into(), mask(pos + 1)?.into()),
                ("position_ids".into(), i64_tensor(vec![1, 1], vec![pos as i64])?.into()),
            ];
            for (i, v) in past.drain(..).enumerate() {
                inputs.push((name(i, false).into(), v.into()));
            }
            let mut o = dec.run(inputs).map_err(e)?;
            last = pick(o["logits"].try_extract_tensor::<f32>().map_err(e)?.1, 0);
            past = (0..LAYERS * 2).map(|i| o.remove(name(i, true)).ok_or("no present".to_string())).collect::<R<_>>()?;
            t_run += tr.elapsed().as_secs_f64();
        }
        let t_lm = t1.elapsed().as_secs_f64();
        let n_steps = generated.len() - 1;

        let t2 = Instant::now();
        let (_, prompt) = prompt.try_extract_tensor::<i64>().map_err(e)?;
        let speech: Vec<i64> = generated[1..].iter().copied().filter(|t| *t < START).collect();
        let mut all = prompt.to_vec();
        all.extend(&speech);
        all.extend([SILENCE; 3]);
        let n = all.len();
        let o = self.dec.run(ort::inputs!["speech_tokens" => i64_tensor(vec![1, n], all)?, "speaker_embeddings" => spk, "speaker_features" => feat]).map_err(e)?;
        let (_, wav) = o["waveform"].try_extract_tensor::<f32>().map_err(e)?;
        let wav = wav.to_vec();
        let t_dec = t2.elapsed().as_secs_f64();
        let stages = json!({"encoder_s": t_enc, "lm_s": t_lm, "lm_steps": n_steps, "ms_per_step": 1000.0 * t_lm / n_steps.max(1) as f64, "decoder_s": t_dec, "prefill_s": t_prefill, "embed_s": t_embed, "lm_run_s": t_run, "cond_len": n_cond, "text_len": n_text});
        Ok((wav, speech, stages))
    }
}

fn session(env: &ort::environment::Environment, dir: &Path, name: &str, label: &str, o: &Opts) -> R<(Session, f64, String)> {
    let gpu = o.ep == "migraphx" && !o.cpu_graphs.iter().any(|g| g == name);
    if gpu {
        // the EP's compiled-program cache, one folder per session and shape set: it names a session's first program
        // <model hash>-0.mxr whatever its shapes and loads that file on the next run without checking them
        let label = if name == "language_model" && o.kv_max > 0 { format!("{label}-kv{}-prefill{}", o.kv_max, o.prefill) } else { label.to_string() };
        let cache = dir.join("migraphx-cache").join(label);
        std::fs::create_dir_all(&cache).map_err(e)?;
        unsafe { std::env::set_var("ORT_MIGRAPHX_MODEL_CACHE_PATH", cache) };
    }
    let eps: Vec<ExecutionProviderDispatch> = if gpu {
        vec![MIGraphX::default().with_device_id(o.device).build().error_on_failure(), CPU::default().build()]
    } else {
        vec![CPU::default().build()]
    };
    let t = Instant::now();
    let mut b = Session::builder(env).map_err(e)?.with_execution_providers(eps).map_err(e)?;
    if o.verbose {
        b = b.with_log_level(ort::logging::LogLevel::Verbose).map_err(e)?;
    }
    let path = match (&o.decoder, name) {
        (Some(p), "conditional_decoder") => p.clone(),
        _ => dir.join(format!("onnx/{name}.onnx")),
    };
    let s = b.commit_from_file(path).map_err(|x| format!("{name}: {x}"))?;
    Ok((s, t.elapsed().as_secs_f64(), if gpu { "migraphx".into() } else { "cpu".into() }))
}

fn main() {
    if let Err(x) = run() {
        eprintln!("chatterbox_onnx: {x}");
        std::process::exit(1);
    }
}

fn run() -> R<()> {
    let o = parse_args()?;
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let dir = root.join("build/models/chatterbox-turbo-onnx");
    // MIGraphX reads a graph's external weights (x.onnx_data) relative to the working directory, not the graph
    let jobs = std::fs::read_to_string(&o.jobs).map_err(e)?;
    let cwd = std::env::current_dir().map_err(e)?;
    std::env::set_current_dir(dir.join("onnx")).map_err(e)?;
    if o.lufs {
        for l in jobs.lines().filter(|l| !l.trim().is_empty()) {
            let r = cwd.join(l.split('\t').next().unwrap_or(""));
            println!("{}\t{}", r.display(), integrated_loudness(&read_wav(&r)?));
        }
        return Ok(());
    }
    let lib = std::env::var("ORT_DYLIB_PATH").unwrap_or_else(|_| "/usr/lib/libonnxruntime.so".into());
    let env = ort::init_from(&lib).map_err(|x| format!("{lib}: {x}"))?.build().map_err(e)?;
    let mut loads = serde_json::Map::new();
    let mut s = vec![];
    for g in GRAPHS {
        let (sess, secs, on) = session(&env, &dir, g, g, &o)?;
        loads.insert(g.into(), json!({"ep": on, "load_s": secs}));
        s.push(sess);
    }
    println!("{}", json!({"loaded": loads, "ort": lib}));
    let mut s = s.into_iter();
    let mut tok = tokenizers::Tokenizer::from_file(dir.join("tokenizer.json")).map_err(e)?;
    tok.with_truncation(None).map_err(e)?;
    tok.with_padding(None);
    let mut m = Model { enc: s.next().unwrap(), embed: s.next().unwrap(), lm: s.next().unwrap(), dec: s.next().unwrap(), tok, lm_dec: None, _alloc: None, kv: None };
    if o.iobind {
        if o.kv_max == 0 || o.ep != "migraphx" {
            return Err("--iobind needs --ep migraphx and --kv-max".into());
        }
        use ort::memory::{AllocationDevice, Allocator, AllocatorType, MemoryInfo, MemoryType};
        let (dec, secs, _) = session(&env, &dir, "language_model", "language_model-decode", &o)?;
        let alloc = Allocator::new(&dec, MemoryInfo::new(AllocationDevice::HIP, o.device, AllocatorType::Device, MemoryType::Default).map_err(e)?).map_err(e)?;
        m.kv = Some((0..LAYERS * 2).map(|_| Tensor::<f32>::new(&alloc, [1usize, HEADS, o.kv_max, HEAD_DIM])).collect::<Result<_, _>>().map_err(e)?);
        m.lm_dec = Some(dec);
        m._alloc = Some(alloc);
        println!("{}", json!({"loaded": {"language_model (decode)": {"ep": "migraphx", "load_s": secs}}}));
    }

    let jobs: Vec<(PathBuf, PathBuf, String)> = jobs.lines().filter(|l| !l.trim().is_empty()).map(|l| {
        let mut p = l.splitn(3, '\t');
        (cwd.join(p.next().unwrap_or("")), cwd.join(p.next().unwrap_or("")), p.next().unwrap_or("").to_string())
    }).collect();
    let mut rng = Rng(o.seed);
    for (k, (r, out, text)) in jobs.iter().enumerate() {
        let reps = if k == 0 { o.warmup + 1 } else { 1 };
        for rep in 0..reps {
            let t = Instant::now();
            let mut audio = read_wav(r)?;
            if o.norm_loudness {
                norm_loudness(&mut audio);
            }
            let text = punc_norm(text);
            let (wav, toks, stages) = m.generate(&text, &audio, o.greedy, o.kv_max, o.prefill, &mut rng)?;
            let secs = t.elapsed().as_secs_f64();
            if rep + 1 < reps {
                eprintln!("warm-up {} s", secs);
                continue;
            }
            write_wav(out, &wav)?;
            std::fs::write(out.with_extension("tokens.txt"), toks.iter().map(|t| t.to_string()).collect::<Vec<_>>().join(" ")).map_err(e)?;
            let audio_s = wav.len() as f64 / SR as f64;
            println!("{}", json!({"out": out, "secs": secs, "audio_s": audio_s, "rtf": secs / audio_s, "tokens": toks.len(), "stages": stages}));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn punc() {
        assert_eq!(super::punc_norm("hello  world: yes…"), "Hello world, yes,");
        assert_eq!(super::punc_norm("“Go”"), "\"Go\".");
    }
}
