//! The API key registry behind the HTTP route and the dashboard: named keys, each with its own
//! token, base URL and tool permissions. Kept at ~/.config/wotr/mcp_keys.json (0600, never in git).
//! On first run it imports the two tokens the Python units used, so no connector URL changes.
use serde::{Deserialize, Serialize};
use std::io::Read;
use std::path::PathBuf;
use std::sync::RwLock;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Serialize, Deserialize, Clone)]
pub struct Key {
    pub id: String,
    pub name: String,
    pub token: String,
    /// full | core | read-only | custom
    pub preset: String,
    /// the allowed tools when preset is custom
    #[serde(default)]
    pub tools: Vec<String>,
    pub enabled: bool,
    /// where this key's links point (the /ro key keeps its old Funnel path)
    pub base: String,
    pub created: u64,
    #[serde(default)]
    pub last_used: u64,
    #[serde(default)]
    pub last_ip: String,
    #[serde(default)]
    pub calls: u64,
}

pub struct Registry {
    path: PathBuf,
    pub keys: RwLock<Vec<Key>>,
}

pub fn now() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_secs()).unwrap_or(0)
}

/// `n` random bytes as hex, from the kernel.
pub fn random_hex(n: usize) -> String {
    let mut b = vec![0u8; n];
    std::fs::File::open("/dev/urandom").and_then(|mut f| f.read_exact(&mut b)).expect("/dev/urandom");
    b.iter().map(|x| format!("{x:02x}")).collect()
}

/// Constant-time equality, so a token check leaks nothing through timing.
fn same(a: &str, b: &str) -> bool {
    a.len() == b.len() && a.bytes().zip(b.bytes()).fold(0u8, |acc, (x, y)| acc | (x ^ y)) == 0
}

fn env_token() -> String {
    // WOTR_MCP_TOKEN from the environment or ~/.config/wotr/env (the Python loader's two sources)
    if let Ok(t) = std::env::var("WOTR_MCP_TOKEN") {
        if !t.trim().is_empty() {
            return t.trim().to_string();
        }
    }
    let home = std::env::var("HOME").unwrap_or_default();
    let env = std::fs::read_to_string(format!("{home}/.config/wotr/env")).unwrap_or_default();
    env.lines()
        .filter_map(|l| l.trim().strip_prefix("WOTR_MCP_TOKEN="))
        .map(|v| v.trim().trim_matches(|c| c == '"' || c == '\'').to_string())
        .find(|v| !v.is_empty())
        .unwrap_or_default()
}

impl Registry {
    pub fn open(base: &str) -> Self {
        let home = std::env::var("HOME").unwrap_or_default();
        let path = std::env::var_os("WOTR_MCP_KEYS").map(PathBuf::from).unwrap_or_else(|| PathBuf::from(format!("{home}/.config/wotr/mcp_keys.json")));
        let keys = match std::fs::read_to_string(&path) {
            Ok(t) => serde_json::from_str(&t).unwrap_or_else(|e| panic!("{}: {e}", path.display())),
            Err(_) => {
                let read = |rel: &str| std::fs::read_to_string(crate::util::root(rel)).map(|s| s.trim().to_string()).unwrap_or_default();
                let main = Some(env_token()).filter(|t| !t.is_empty()).unwrap_or_else(|| read("build/.mcp_token"));
                let mut v = Vec::new();
                for (name, token, preset, b) in [("Main", main, "full", base.to_string()), ("Read-only (friends)", read("build/.mcp_token_ro"), "read-only", format!("{base}/ro"))] {
                    if token.len() >= 16 {
                        v.push(Key { id: random_hex(4), name: name.into(), token, preset: preset.into(), tools: vec![], enabled: true, base: b, created: now(), last_used: 0, last_ip: String::new(), calls: 0 });
                    }
                }
                v
            }
        };
        let r = Registry { path, keys: RwLock::new(keys) };
        r.save();
        r
    }

    pub fn save(&self) {
        let text = serde_json::to_string_pretty(&*self.keys.read().unwrap()).unwrap();
        let tmp = self.path.with_extension("json.tmp");
        if let Some(d) = self.path.parent() {
            let _ = std::fs::create_dir_all(d);
        }
        // created 0600 so the tokens are never readable by anyone else, then renamed into place
        use std::io::Write;
        use std::os::unix::fs::OpenOptionsExt;
        let _ = std::fs::remove_file(&tmp);
        let ok = std::fs::OpenOptions::new().write(true).create_new(true).mode(0o600).open(&tmp)
            .and_then(|mut f| f.write_all((text + "\n").as_bytes()))
            .and_then(|_| std::fs::rename(&tmp, &self.path))
            .is_ok();
        if !ok {
            eprintln!("could not write {}", self.path.display());
        }
    }

    /// The enabled key holding this token.
    pub fn by_token(&self, token: &str) -> Option<Key> {
        self.keys.read().unwrap().iter().find(|k| k.enabled && same(&k.token, token)).cloned()
    }

    pub fn get(&self, id: &str) -> Option<Key> {
        self.keys.read().unwrap().iter().find(|k| k.id == id).cloned()
    }

    /// Note a request: kept in memory, flushed by the caller's periodic save.
    pub fn touch(&self, id: &str, ip: &str) {
        if let Some(k) = self.keys.write().unwrap().iter_mut().find(|k| k.id == id) {
            k.last_used = now();
            k.last_ip = ip.to_string();
            k.calls += 1;
        }
    }

    pub fn update(&self, id: &str, f: impl FnOnce(&mut Key)) -> Option<Key> {
        let out = self.keys.write().unwrap().iter_mut().find(|k| k.id == id).map(|k| {
            f(k);
            k.clone()
        });
        self.save();
        out
    }

    pub fn add(&self, k: Key) {
        self.keys.write().unwrap().push(k);
        self.save();
    }

    pub fn remove(&self, id: &str) -> bool {
        let mut keys = self.keys.write().unwrap();
        let n = keys.len();
        keys.retain(|k| k.id != id);
        let gone = keys.len() != n;
        drop(keys);
        self.save();
        gone
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn tokens() {
        assert!(super::same("abc", "abc") && !super::same("abc", "abd") && !super::same("abc", "ab"));
        assert_eq!(super::random_hex(24).len(), 48);
    }
}
