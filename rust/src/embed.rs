//! build/embed_index.py's search side: embed a query with the same bge-small ONNX model the index
//! was built with (the system ONNX Runtime, loaded at run time) and rank build/index's chunks by
//! cosine. Building the index stays in Python (the hourly sync runs it); this only reads it.
use crate::util::root;
use serde::Deserialize;
use std::path::PathBuf;
use std::sync::{Arc, LazyLock, Mutex};
use std::time::SystemTime;

#[derive(Deserialize)]
pub struct Chunk {
    pub corpus: String,
    pub path: String,
    pub title: String,
    pub heading: String,
    pub text: String,
}

#[derive(Deserialize)]
struct Meta {
    chunks: Vec<Chunk>,
}

struct Index {
    stamp: SystemTime,
    chunks: Vec<Chunk>,
    vecs: Vec<f32>, // row-major, len = chunks * 384
}

const DIM: usize = 384;

fn model_dir() -> Option<PathBuf> {
    let snaps = root("build/models/fastembed/models--qdrant--bge-small-en-v1.5-onnx-q/snapshots");
    std::fs::read_dir(snaps).ok()?.flatten().map(|e| e.path()).find(|p| p.join("model_optimized.onnx").is_file())
}

struct Model {
    session: ort::session::Session,
    tok: tokenizers::Tokenizer,
}

static MODEL: LazyLock<Mutex<Option<Model>>> = LazyLock::new(|| Mutex::new(None));
static INDEX: LazyLock<Mutex<Option<Arc<Index>>>> = LazyLock::new(|| Mutex::new(None));
pub(crate) static ENV: LazyLock<Result<ort::environment::Environment, String>> = LazyLock::new(|| {
    // the ONNX Runtime the index was built with (the wotr venv's) gives bit-identical query vectors;
    // the system onnxruntime-cpu differs in the fourth decimal and is the fallback
    let own = crate::util::site_packages("wotr").map(|d| d.join("onnxruntime/capi"))
        .into_iter().flat_map(|d| std::fs::read_dir(d).into_iter().flatten().flatten().map(|e| e.path()))
        .find(|p| p.file_name().is_some_and(|n| n.to_string_lossy().starts_with("libonnxruntime.so.")));
    let lib = std::env::var("ORT_DYLIB_PATH").ok().or(own.map(|p| p.to_string_lossy().into_owned())).unwrap_or_else(|| "/usr/lib/libonnxruntime.so".into());
    ort::init_from(&lib).map_err(|e| format!("{lib}: {e}"))?.build().map_err(|e| e.to_string())
});

fn load_model() -> Result<Model, String> {
    let dir = model_dir().ok_or("embedding model missing (build/models/fastembed); run build/embed_index.py once")?;
    let env = ENV.as_ref().map_err(Clone::clone)?;
    let session = ort::session::Session::builder(env)
        .and_then(|mut b| b.commit_from_file(dir.join("model_optimized.onnx")))
        .map_err(|e| e.to_string())?;
    let mut tok = tokenizers::Tokenizer::from_file(dir.join("tokenizer.json")).map_err(|e| e.to_string())?;
    // fastembed's preprocessing: truncate at model_max_length (512); one query needs no padding
    tok.with_truncation(Some(tokenizers::TruncationParams { max_length: 512, ..Default::default() })).map_err(|e| e.to_string())?;
    tok.with_padding(None);
    Ok(Model { session, tok })
}

/// The query's unit vector: CLS pooling, then L2 normalization, as fastembed does for bge.
pub fn embed(text: &str) -> Result<Vec<f32>, String> {
    let mut slot = MODEL.lock().unwrap();
    if slot.is_none() {
        *slot = Some(load_model()?);
    }
    let m = slot.as_mut().unwrap();
    let enc = m.tok.encode(text, true).map_err(|e| e.to_string())?;
    let n = enc.get_ids().len();
    let as_i64 = |v: &[u32]| v.iter().map(|x| *x as i64).collect::<Vec<i64>>();
    let t = |v: Vec<i64>| ort::value::Tensor::from_array(([1usize, n], v)).map_err(|e| e.to_string());
    let inputs = ort::inputs![
        "input_ids" => t(as_i64(enc.get_ids()))?,
        "attention_mask" => t(as_i64(enc.get_attention_mask()))?,
        "token_type_ids" => t(as_i64(enc.get_type_ids()))?,
    ];
    let out = m.session.run(inputs).map_err(|e| e.to_string())?;
    let (_, data) = out["last_hidden_state"].try_extract_tensor::<f32>().map_err(|e| e.to_string())?;
    let mut v = data[..DIM].to_vec(); // token 0 of sequence 0: the CLS vector
    let norm = v.iter().map(|x| x * x).sum::<f32>().sqrt().max(1e-12);
    v.iter_mut().for_each(|x| *x /= norm);
    Ok(v)
}

/// An .npy file's float data as f32 (np.asarray(x, dtype=np.float32)): '<f4' or '<f8', C order.
pub(crate) fn npy_f32(bytes: &[u8]) -> Result<Vec<f32>, String> {
    // NPY v1/v2: magic, version, header length, a dict header, then raw data
    if bytes.len() < 10 || &bytes[..6] != b"\x93NUMPY" {
        return Err("not an npy file".into());
    }
    let (hlen, start) = if bytes[6] == 1 { (u16::from_le_bytes([bytes[8], bytes[9]]) as usize, 10) } else { (u32::from_le_bytes(bytes[8..12].try_into().unwrap()) as usize, 12) };
    let header = String::from_utf8_lossy(&bytes[start..start + hlen]);
    let data = &bytes[start + hlen..];
    if header.contains("'fortran_order': True") {
        return Err(format!("unexpected npy header {header}"));
    }
    if header.contains("'<f8'") {
        return Ok(data.chunks_exact(8).map(|b| f64::from_le_bytes(b.try_into().unwrap()) as f32).collect());
    }
    if !header.contains("'<f4'") {
        return Err(format!("unexpected npy header {header}"));
    }
    Ok(data.chunks_exact(4).map(|b| f32::from_le_bytes(b.try_into().unwrap())).collect())
}

/// The index, reloaded when the sync rebuilt it (vectors.npy's mtime), as embed_index._load does.
fn index() -> Result<Arc<Index>, String> {
    let vp = root("build/index/vectors.npy");
    let stamp = std::fs::metadata(&vp).and_then(|m| m.modified()).map_err(|e| e.to_string())?;
    let mut slot = INDEX.lock().unwrap();
    if let Some(ix) = slot.as_ref().filter(|ix| ix.stamp == stamp) {
        return Ok(ix.clone());
    }
    let meta: Meta = serde_json::from_slice(&std::fs::read(root("build/index/chunks.json")).map_err(|e| e.to_string())?).map_err(|e| e.to_string())?;
    let vecs = npy_f32(&std::fs::read(&vp).map_err(|e| e.to_string())?).map_err(|e| format!("vectors.npy: {e}"))?;
    if vecs.len() != meta.chunks.len() * DIM {
        return Err("index is mid-rebuild; try again".into());
    }
    let ix = Arc::new(Index { stamp, chunks: meta.chunks, vecs });
    *slot = Some(ix.clone());
    Ok(ix)
}

pub struct Hit {
    pub path: String,
    pub title: String,
    pub score: f64,
    pub chunks: Vec<(String, String, f64)>,
}

/// embed_index.search: best files for a query in one corpus ('wiki' | 'scenes' | 'lore-v1'), each
/// with its best-matching passages. Empty when the index or the model is unavailable, so the
/// caller falls back to the keyword ranker, as the Python does.
pub fn search(query: &str, corpus: &str, limit: usize, per_file: usize) -> Vec<Hit> {
    let (Ok(ix), Ok(q)) = (index(), embed(query)) else { return vec![] };
    let sims: Vec<f32> = ix.vecs.chunks_exact(DIM).map(|row| row.iter().zip(&q).map(|(a, b)| a * b).sum()).collect();
    let mut order: Vec<usize> = (0..sims.len()).collect();
    order.sort_by(|&a, &b| sims[b].total_cmp(&sims[a]));
    let mut by_file: Vec<Hit> = Vec::new();
    let mut pos: std::collections::HashMap<&str, usize> = std::collections::HashMap::new();
    let mut unfilled = 0usize;
    for i in order {
        let c = &ix.chunks[i];
        if c.corpus != corpus {
            continue;
        }
        let k = *pos.entry(c.path.as_str()).or_insert_with(|| {
            by_file.push(Hit { path: c.path.clone(), title: c.title.clone(), score: sims[i] as f64, chunks: vec![] });
            unfilled += 1;
            by_file.len() - 1
        });
        let h = &mut by_file[k];
        if h.chunks.len() < per_file {
            h.chunks.push((c.heading.clone(), c.text.clone(), sims[i] as f64));
            if h.chunks.len() == per_file {
                unfilled -= 1;
            }
        }
        if by_file.len() > limit * 4 && unfilled == 0 {
            break;
        }
    }
    by_file.sort_by(|a, b| b.score.total_cmp(&a.score));
    by_file.truncate(limit);
    by_file
}
