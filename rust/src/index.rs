//! build/embed_index.py's build(), as `wotr-mcp index [-q]`: every wiki page and scene cut into
//! chunks under its nearest heading, each chunk embedded once with bge-small and kept by content
//! hash, written as build/index/chunks.json and vectors.npy byte for byte as the Python writes them.
//! Python's string semantics are kept where they show: str.isspace for \s and strip, splitlines'
//! boundaries, lengths and slices by code point, Path.read_text's universal newlines, sorted() of
//! paths by component, and numpy's float32 norm (embed::normalize).
use crate::embed::{embed_docs, normalize, npy_f32};
use crate::util::{fwd, rglob_md, rel_posix, root, ROOT};
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::sync::LazyLock;
use std::time::Instant;

const MODEL: &str = "BAAI/bge-small-en-v1.5";
const CHUNK_CHARS: usize = 900;
const DIM: usize = 384;
const SKIP_NAMES: [&str; 6] = ["INDEX.md", "MANIFEST.md", "CAST.md", "ARCS.md", "TIMELINE.md", "CONTINUITY.md"];

/// Python's \s for str patterns: exactly the characters for which str.isspace() is true
/// (Unicode White_Space plus \x1c-\x1f).
const WS: &str = r"[\t\n\x0B\x0C\r\x1C-\x1F \x{85}\x{A0}\x{1680}\x{2000}-\x{200A}\x{2028}\x{2029}\x{202F}\x{205F}\x{3000}]";
static PARA: LazyLock<Regex> = LazyLock::new(|| Regex::new(&format!(r"\n{WS}*\n")).unwrap());
static HEADING: LazyLock<Regex> = LazyLock::new(|| Regex::new(&format!(r"^(#{{1,6}}){WS}+(.+)$")).unwrap());
static TITLE: LazyLock<Regex> = LazyLock::new(|| Regex::new(&format!(r"(?m)^#{WS}+(.+)$")).unwrap());

fn is_space(c: char) -> bool {
    matches!(c, '\t'..='\r' | '\x1c'..='\x1f' | ' ' | '\u{85}' | '\u{a0}' | '\u{1680}' | '\u{2000}'..='\u{200a}' | '\u{2028}' | '\u{2029}' | '\u{202f}' | '\u{205f}' | '\u{3000}')
}

/// str.strip()
fn strip(s: &str) -> &str {
    s.trim_matches(is_space)
}

/// str.splitlines(): \n, \r, \r\n, \v, \f, \x1c-\x1e, \x85,  ,  ; no trailing empty line.
fn splitlines(s: &str) -> Vec<&str> {
    let (mut out, mut start) = (Vec::new(), 0);
    let mut it = s.char_indices().peekable();
    while let Some((i, c)) = it.next() {
        if matches!(c, '\n' | '\r' | '\x0b' | '\x0c' | '\x1c' | '\x1d' | '\x1e' | '\u{85}' | '\u{2028}' | '\u{2029}') {
            out.push(&s[start..i]);
            start = i + c.len_utf8();
            if c == '\r' && it.peek().is_some_and(|p| p.1 == '\n') {
                it.next();
                start += 1;
            }
        }
    }
    if start < s.len() {
        out.push(&s[start..]);
    }
    out
}

fn nchars(s: &str) -> usize {
    s.chars().count()
}

/// embed_index.chunk: (heading, chunk text) pairs, split on headings, then on paragraphs to size.
pub fn chunk(text: &str, title: &str) -> Vec<(String, String)> {
    let mut out: Vec<(String, String)> = Vec::new();
    let mut heading = title.to_string();
    let mut buf: Vec<String> = Vec::new();
    let flush = |buf: &mut Vec<String>, heading: &str, out: &mut Vec<(String, String)>| {
        let body = strip(&buf.join("\n")).to_string();
        if !body.is_empty() {
            out.push((heading.to_string(), body));
        }
        buf.clear();
    };
    for para in PARA.split(text) {
        let mut para = strip(para).to_string();
        if para.is_empty() {
            continue;
        }
        let lines = splitlines(&para);
        if let Some(m) = HEADING.captures(lines[0]) {
            flush(&mut buf, &heading, &mut out);
            heading = strip(&m[2]).to_string();
            let rest = strip(&lines[1..].join("\n")).to_string();
            if !rest.is_empty() {
                buf.push(rest);
            }
            continue;
        }
        if buf.iter().map(|b| nchars(b)).sum::<usize>() + nchars(&para) > CHUNK_CHARS && !buf.is_empty() {
            flush(&mut buf, &heading, &mut out);
        }
        while nchars(&para) > CHUNK_CHARS * 2 {
            // a single huge paragraph: cut after the last ". " inside the first CHUNK_CHARS chars
            let lim = fwd(&para, 0, CHUNK_CHARS);
            let cut = match para[..lim].rfind(". ").map(|b| nchars(&para[..b])) {
                Some(c) if c > CHUNK_CHARS / 2 => c + 1,
                _ => CHUNK_CHARS,
            };
            let cb = fwd(&para, 0, cut);
            buf.push(strip(&para[..cb]).to_string());
            flush(&mut buf, &heading, &mut out);
            para = strip(&para[cb..]).to_string();
        }
        buf.push(para);
    }
    flush(&mut buf, &heading, &mut out);
    out
}

/// embed_index._read: Path.read_text(errors="replace") (universal newlines), frontmatter cut.
fn read(p: &Path) -> Result<String, String> {
    let b = std::fs::read(p).map_err(|e| format!("{}: {e}", p.display()))?;
    let t = String::from_utf8_lossy(&b).replace("\r\n", "\n").replace('\r', "\n");
    if let Some(rest) = t.strip_prefix("---\n") {
        if let Some(end) = rest.find("\n---\n") {
            return Ok(rest[end + 5..].to_string());
        }
    }
    Ok(t)
}

/// PurePath.stem in Python 3.14: the name minus its last suffix, unless that leaves only dots.
fn py_stem(p: &Path) -> String {
    let name = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    match name.rfind('.') {
        Some(i) if !name[..i].trim_start_matches('.').is_empty() => name[..i].to_string(),
        _ => name,
    }
}

/// embed_index._files: sorted(root.rglob("*.md")) (Path order is by component), SKIP_NAMES out,
/// and in the scene roots anything under a cast/ folder.
fn files(dir: &Path, scenes: bool) -> Vec<PathBuf> {
    let mut v = rglob_md(dir);
    v.sort();
    v.retain(|p| {
        let name = p.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        !SKIP_NAMES.contains(&name.as_str()) && !(scenes && p.strip_prefix(dir).unwrap_or(p).components().any(|c| c.as_os_str() == "cast"))
    });
    v
}

/// hashlib.sha1(s.encode()).hexdigest()
fn sha1_hex(data: &[u8]) -> String {
    let mut h: [u32; 5] = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0];
    let mut msg = data.to_vec();
    msg.push(0x80);
    while msg.len() % 64 != 56 {
        msg.push(0);
    }
    msg.extend(((data.len() as u64) * 8).to_be_bytes());
    for block in msg.chunks_exact(64) {
        let mut w = [0u32; 80];
        for i in 0..16 {
            w[i] = u32::from_be_bytes(block[i * 4..i * 4 + 4].try_into().unwrap());
        }
        for i in 16..80 {
            w[i] = (w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]).rotate_left(1);
        }
        let [mut a, mut b, mut c, mut d, mut e] = h;
        for (i, wi) in w.iter().enumerate() {
            let (f, k) = match i {
                0..20 => ((b & c) | (!b & d), 0x5A827999),
                20..40 => (b ^ c ^ d, 0x6ED9EBA1),
                40..60 => ((b & c) | (b & d) | (c & d), 0x8F1BBCDC),
                _ => (b ^ c ^ d, 0xCA62C1D6u32),
            };
            let t = a.rotate_left(5).wrapping_add(f).wrapping_add(e).wrapping_add(k).wrapping_add(*wi);
            (e, d, c, b, a) = (d, c, b.rotate_left(30), a, t);
        }
        for (x, y) in h.iter_mut().zip([a, b, c, d, e]) {
            *x = x.wrapping_add(y);
        }
    }
    h.iter().map(|x| format!("{x:08x}")).collect()
}

/// np.save of a C-order float32 (n, DIM) array: NPY 1.0, the dict header with numpy's growth
/// spaces (21 digits for the first axis), space padded to 64 bytes, a newline, the data.
fn npy_bytes(vecs: &[f32]) -> Vec<u8> {
    let n = vecs.len() / DIM;
    let mut h = format!("{{'descr': '<f4', 'fortran_order': False, 'shape': ({n}, {DIM}), }}");
    h.push_str(&" ".repeat(21usize.saturating_sub(n.to_string().len())));
    let hlen = h.len() + 1;
    let pad = 64 - (8 + 2 + hlen) % 64;
    let mut out = b"\x93NUMPY\x01\x00".to_vec();
    out.extend(((hlen + pad) as u16).to_le_bytes());
    out.extend(h.as_bytes());
    out.extend(std::iter::repeat_n(b' ', pad));
    out.push(b'\n');
    out.extend(vecs.iter().flat_map(|x| x.to_le_bytes()));
    out
}

/// The old index's vectors by chunk hash (the last row wins), or nothing when it cannot be read
/// or its row count does not match its chunks, as build() falls back to a full embed.
fn old_vectors(meta_p: &Path, vec_p: &Path) -> HashMap<String, Vec<f32>> {
    let mut out = HashMap::new();
    if !(meta_p.exists() && vec_p.exists()) {
        return out;
    }
    let Ok(meta) = std::fs::read(meta_p).map_err(|_| ()).and_then(|b| serde_json::from_slice::<serde_json::Value>(&b).map_err(|_| ())) else { return out };
    let Some(chunks) = meta.get("chunks").and_then(|c| c.as_array()) else { return out };
    let Ok(bytes) = std::fs::read(vec_p) else { return out };
    // only what this writer writes ('<f4', (n, 384)); anything else is rebuilt from scratch
    let header = String::from_utf8_lossy(&bytes[..bytes.len().min(128)]).into_owned();
    if !header.contains("'<f4'") || !header.contains(&format!(", {DIM}), }}")) {
        return out;
    }
    let Ok(vecs) = npy_f32(&bytes) else { return out };
    if vecs.len() % DIM != 0 || vecs.len() / DIM != chunks.len() || chunks.iter().any(|c| c.get("hash").is_none()) {
        return out;
    }
    for (c, row) in chunks.iter().zip(vecs.chunks_exact(DIM)) {
        if let Some(h) = c["hash"].as_str() {
            out.insert(h.to_string(), row.to_vec());
        }
    }
    out
}

struct Chunk {
    corpus: &'static str,
    path: String,
    title: String,
    heading: String,
    text: String,
    hash: String,
    passage: String,
}

fn js(s: &str) -> String {
    serde_json::to_string(s).unwrap() // json.dumps(s, ensure_ascii=False)
}

pub fn build(verbose: bool) -> Result<(), String> {
    let index_dir = root("build/index");
    std::fs::create_dir_all(&index_dir).map_err(|e| format!("{}: {e}", index_dir.display()))?;
    let (meta_p, vec_p) = (index_dir.join("chunks.json"), index_dir.join("vectors.npy"));
    let mut old = old_vectors(&meta_p, &vec_p);

    let mut chunks: Vec<Chunk> = Vec::new();
    for (corpus, rel, scenes) in [("wiki", "wiki", false), ("scenes", "scenes", true), ("lore-v1", "lore/v1/scenes", true)] {
        for p in files(&root(rel), scenes) {
            let text = read(&p)?;
            let title = TITLE.captures(&text).map(|m| strip(&m[1]).to_string()).unwrap_or_else(|| py_stem(&p));
            let path = rel_posix(&p, &ROOT);
            for (heading, body) in chunk(&text, &title) {
                let passage = if heading != title { format!("{title} — {heading}\n{body}") } else { format!("{title}\n{body}") };
                let hash = sha1_hex(passage.as_bytes());
                chunks.push(Chunk { corpus, path: path.clone(), title: title.clone(), heading, text: body, hash, passage });
            }
        }
    }

    let todo: Vec<&Chunk> = chunks.iter().filter(|c| !old.contains_key(&c.hash)).collect();
    let t0 = Instant::now();
    if !todo.is_empty() {
        let passages: Vec<&str> = todo.iter().map(|c| c.passage.as_str()).collect();
        let new = embed_docs(&passages, 64)?;
        for (c, v) in todo.iter().zip(new.chunks_exact(DIM)) {
            old.insert(c.hash.clone(), v.to_vec());
        }
    }
    let mut vecs: Vec<f32> = Vec::with_capacity(chunks.len() * DIM);
    for c in &chunks {
        vecs.extend_from_slice(&old[&c.hash]);
    }
    vecs.chunks_exact_mut(DIM).for_each(|row| normalize(row, 1e-9));

    let mut meta = format!("{{\"model\": {}, \"built\": {}, \"chunks\": [", js(MODEL), js(&crate::writers::date_fmt("%Y-%m-%d %H:%M:%S")));
    for (i, c) in chunks.iter().enumerate() {
        meta.push_str(if i > 0 { ", " } else { "" });
        meta.push_str(&format!(
            "{{\"corpus\": {}, \"path\": {}, \"title\": {}, \"heading\": {}, \"text\": {}, \"hash\": {}}}",
            js(c.corpus), js(&c.path), js(&c.title), js(&c.heading), js(&c.text), js(&c.hash)
        ));
    }
    meta.push_str("]}");
    let (tmp_v, tmp_m) = (index_dir.join("vectors.tmp.npy"), index_dir.join("chunks.tmp.json"));
    let io = |r: std::io::Result<()>, p: &Path| r.map_err(|e| format!("{}: {e}", p.display()));
    io(std::fs::write(&tmp_v, npy_bytes(&vecs)), &tmp_v)?;
    io(std::fs::write(&tmp_m, meta), &tmp_m)?;
    io(std::fs::rename(&tmp_m, &meta_p), &meta_p)?;
    io(std::fs::rename(&tmp_v, &vec_p), &vec_p)?; // last: its mtime is the stamp readers watch
    if verbose {
        let files: HashSet<&str> = chunks.iter().map(|c| c.path.as_str()).collect();
        println!(
            "index: {} files, {} chunks, {} newly embedded in {:.1}s -> {}",
            files.len(), chunks.len(), todo.len(), t0.elapsed().as_secs_f64(), index_dir.display()
        );
    }
    Ok(())
}

/// `wotr-mcp index [-q]`: embed_index.py's __main__.
pub fn main(args: &[String]) -> i32 {
    match build(!args.iter().any(|a| a == "-q")) {
        Ok(()) => 0,
        Err(e) => {
            eprintln!("index: {e}");
            1
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sha1_matches_hashlib() {
        assert_eq!(sha1_hex(b""), "da39a3ee5e6b4b0d3255bfef95601890afd80709");
        assert_eq!(sha1_hex("Soul Crystal — Shell\nthe draw".as_bytes()).len(), 40);
        assert_eq!(sha1_hex(&[b'a'; 1000]), "291e9a6c66994949b57ba5e650361e98fc36b1ba");
    }

    #[test]
    fn npy_header_is_numpys() {
        // np.save(f, np.zeros((23034, 384), np.float32)): a 128-byte header
        let b = npy_bytes(&vec![0.0; 23034 * DIM]);
        assert_eq!(b.len(), 128 + 23034 * DIM * 4);
        assert_eq!(&b[10..75], b"{'descr': '<f4', 'fortran_order': False, 'shape': (23034, 384), }".as_slice());
        assert_eq!(b[127], b'\n');
        assert_eq!(npy_bytes(&[]).len(), 128);
    }

    #[test]
    fn python_string_semantics() {
        assert_eq!(splitlines("a\x1cb\x1fc\r\nd\n"), vec!["a", "b\x1fc", "d"]);
        assert_eq!(strip("\x1f\u{a0} x \u{3000}"), "x");
        assert_eq!(py_stem(Path::new("..md")), "..md");
        assert_eq!(py_stem(Path::new("a.b.md")), "a.b");
        let c = chunk("# T\n\nintro\n\n## H\n\n\n\nbody", "T");
        assert_eq!(c, [("T", "intro"), ("H", "body")].map(|(h, b)| (h.to_string(), b.to_string())));
    }
}
