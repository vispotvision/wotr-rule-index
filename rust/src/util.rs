//! Helpers shared by the ported tools: the repo root, Python-compatible file walking, reading
//! and char-indexed slicing. Python slices strings by code point and Rust by byte, so every
//! `text[a:b]` in the Python tools goes through `back`/`fwd`/`head`/`tail` here.
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::LazyLock;

pub static ROOT: LazyLock<PathBuf> = LazyLock::new(|| {
    std::env::var_os("WOTR_ROOT")
        .map(PathBuf::from)
        .unwrap_or_else(|| Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().to_path_buf())
});

pub fn root(rel: &str) -> PathBuf {
    ROOT.join(rel)
}

/// common.load_env(): the env file's KEY=value pairs for the keys this process has unset or empty
/// (the first line for a key wins, as os.environ is set by then).
static ENV_FILE: LazyLock<Vec<(String, String)>> = LazyLock::new(|| {
    let home = std::env::var("HOME").unwrap_or_default();
    let path = std::env::var("WOTR_ENV_FILE").ok().filter(|v| !v.is_empty()).unwrap_or_else(|| format!("{home}/.config/wotr/env"));
    let mut out: Vec<(String, String)> = Vec::new();
    for line in read_lossy(Path::new(&path)).lines() {
        let line = line.trim();
        let Some((k, v)) = line.split_once('=').filter(|_| !line.starts_with('#')) else { continue };
        let (k, mut v) = (k.trim(), v.trim().to_string());
        if v.len() >= 2 && (v.starts_with('"') && v.ends_with('"') || v.starts_with('\'') && v.ends_with('\'')) {
            v = v[1..v.len() - 1].to_string();
        }
        if v == "~" || v.starts_with("~/") {
            v = format!("{home}{}", &v[1..]);
        }
        let ident = k.starts_with(|c: char| c.is_ascii_alphabetic() || c == '_') && k.chars().all(|c| c.is_ascii_alphanumeric() || c == '_');
        if ident && !v.is_empty() && std::env::var(k).unwrap_or_default().is_empty() && !out.iter().any(|(o, _)| o == k) {
            out.push((k.to_string(), v));
        }
    }
    out
});

/// os.environ.get(key) in the Python server, the env file loaded: None when unset or empty.
pub fn env(key: &str) -> Option<String> {
    std::env::var(key).ok().filter(|v| !v.is_empty()).or_else(|| ENV_FILE.iter().find(|(k, _)| k == key).map(|(_, v)| v.clone()))
}

/// common.env_path: the variable (or the default) as a path, a leading ~ expanded.
pub fn env_path(key: &str, default: Option<&str>) -> Option<PathBuf> {
    let raw = env(key).or(default.map(String::from))?;
    let home = std::env::var("HOME").unwrap_or_default();
    Some(PathBuf::from(if raw == "~" || raw.starts_with("~/") { format!("{home}{}", &raw[1..]) } else { raw }))
}

/// A child as mcp_server._env() starts it: this environment, the env file and PYTHONIOENCODING, in the repo.
pub fn command(prog: impl AsRef<std::ffi::OsStr>) -> std::process::Command {
    let mut c = std::process::Command::new(prog);
    c.envs(ENV_FILE.iter().map(|(k, v)| (k, v))).env("PYTHONIOENCODING", "utf-8").current_dir(&*ROOT);
    c
}

/// mcp_server._audio_dir: the Drive folder when WOTR_DRIVE is set and mounted (rclone), else docs/audio.
pub fn audio_dir() -> PathBuf {
    match env_path("WOTR_DRIVE", None).filter(|d| d.is_dir()) {
        Some(d) => d.join("War of the Realms — Documents").join("Arcs").join("Audio"),
        None => root("docs/audio"),
    }
}

/// urllib.parse.quote(s, safe=safe), and quote_plus when `plus`.
pub fn quote(s: &str, safe: &str, plus: bool) -> String {
    let mut out = String::new();
    for b in s.bytes() {
        match b {
            b' ' if plus => out.push('+'),
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'_' | b'.' | b'-' | b'~' => out.push(b as char),
            b if b.is_ascii() && safe.contains(b as char) => out.push(b as char),
            b => out.push_str(&format!("%{b:02X}")),
        }
    }
    out
}

/// A file as text, invalid UTF-8 replaced (Python's errors="replace"); "" when unreadable.
pub fn read_lossy(p: &Path) -> String {
    fs::read(p).map(|b| String::from_utf8_lossy(&b).into_owned()).unwrap_or_default()
}

/// mcp_server._read: the page without its YAML frontmatter.
pub fn read_page(p: &Path) -> String {
    let t = read_lossy(p);
    if let Some(rest) = t.strip_prefix("---\n") {
        if let Some(end) = rest.find("\n---\n") {
            return rest[end + 5..].to_string();
        }
    }
    t
}

fn list_md(dir: &Path, out: &mut Vec<PathBuf>) {
    if let Ok(rd) = fs::read_dir(dir) {
        for e in rd.flatten() {
            if e.file_name().to_string_lossy().ends_with(".md") {
                out.push(e.path());
            }
        }
    }
}

/// Path.rglob("*.md") in Python 3.14's order: a directory's own *.md are listed when its parent's
/// scan first meets it, and its subdirectories are walked later off a LIFO stack. Ties in the
/// tools' sorts fall back on this order, so it is kept exactly. Symlinked dirs are not followed.
pub fn rglob_md(root: &Path) -> Vec<PathBuf> {
    let mut out = Vec::new();
    list_md(root, &mut out);
    let mut stack = vec![root.to_path_buf()];
    while let Some(d) = stack.pop() {
        let Ok(rd) = fs::read_dir(&d) else { continue };
        for e in rd.flatten() {
            if e.file_type().map(|t| t.is_dir()).unwrap_or(false) {
                list_md(&e.path(), &mut out);
                stack.push(e.path());
            }
        }
    }
    out
}

pub fn stem(p: &Path) -> String {
    p.file_stem().map(|s| s.to_string_lossy().into_owned()).unwrap_or_default()
}

pub fn rel_posix(p: &Path, base: &Path) -> String {
    p.strip_prefix(base).unwrap_or(p).to_string_lossy().into_owned()
}

/// The byte offset `n` chars before byte offset `i` (clamped at 0).
pub fn back(s: &str, i: usize, n: usize) -> usize {
    if n == 0 {
        return i;
    }
    s[..i].char_indices().rev().nth(n - 1).map(|(j, _)| j).unwrap_or(0)
}

/// The byte offset `n` chars after byte offset `i` (clamped at the end).
pub fn fwd(s: &str, i: usize, n: usize) -> usize {
    s[i..].char_indices().nth(n).map(|(j, _)| i + j).unwrap_or(s.len())
}

/// s[:n] by chars.
pub fn head(s: &str, n: usize) -> &str {
    &s[..fwd(s, 0, n)]
}

/// s[-n:] by chars.
pub fn tail(s: &str, n: usize) -> &str {
    &s[back(s, s.len(), n)..]
}

pub fn chars(s: &str) -> usize {
    s.chars().count()
}

/// Python's repr() of a list of str, as the tools print tag lists: ['a', 'b'].
pub fn py_list(items: &[String]) -> String {
    let q: Vec<String> = items
        .iter()
        .map(|s| {
            if s.contains('\'') && !s.contains('"') {
                format!("\"{s}\"")
            } else {
                format!("'{}'", s.replace('\\', "\\\\").replace('\'', "\\'"))
            }
        })
        .collect();
    format!("[{}]", q.join(", "))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn slicing_is_by_char() {
        let s = "aé—bc";
        assert_eq!(head(s, 3), "aé—");
        assert_eq!(tail(s, 2), "bc");
        assert_eq!(tail(s, 9), s);
        assert_eq!(&s[back(s, s.len(), 3)..], "—bc");
        assert_eq!(back(s, 3, 0), 3);
        assert_eq!(fwd(s, 1, 1), 3);
        assert_eq!(py_list(&["a".into(), "it's".into()]), "['a', \"it's\"]");
    }
}
