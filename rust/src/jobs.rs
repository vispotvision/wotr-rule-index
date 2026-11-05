//! The tools that start other programs (mcp_server.py, ported line for line): narration
//! (cast_scene, narrate_scene, narration_status; the render is `wotr-mcp audio`, audio.rs, started
//! detached), research through the agent-reach
//! and agent-browser CLIs, lookup over the reference wikis' APIs (curl), and the build/ask_*.sh calls
//! (ask_chatgpt, ask_claude, research_chatgpt, chatgpt_image). rust/job_parity.py replays them
//! against the Python tools with stub programs.
use crate::analysis::{find_scene, name_of, py_repr, scene_blocks};
use crate::audio::{check_cast, parse_cast};
use crate::pyjson;
use crate::table::{s, t};
use crate::util::{self, audio_dir, chars, head, read_lossy, root, stem, tail, ROOT};
use crate::writers;
use fancy_regex::Regex;
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::process::Stdio;
use std::sync::{LazyLock, Mutex};
use std::time::{Instant, SystemTime};

macro_rules! rx {
    ($p:expr) => {{
        static R: LazyLock<Regex> = LazyLock::new(|| Regex::new($p).unwrap());
        &*R
    }};
}

/// research_chatgpt's threads; `wotr-mcp call` waits for them before it exits, as the worker would live on.
static BACKGROUND: Mutex<Vec<std::thread::JoinHandle<()>>> = Mutex::new(Vec::new());

pub fn join_background() {
    let hs: Vec<_> = BACKGROUND.lock().unwrap().drain(..).collect();
    for h in hs {
        let _ = h.join();
    }
}

type Public<'a> = Option<&'a (String, String)>;

fn home() -> String {
    std::env::var("HOME").unwrap_or_default()
}

/// mcp_server._run: (exit code, stdout+stderr stripped), None for TimeoutExpired. The child runs under
/// `timeout`, which signals its whole process group, TERM then KILL ten seconds on, as _kill_group does.
/// stdin is closed (Python's children inherited the server's).
fn run(prog: &str, args: &[&str], secs: u64, env: &[(&str, &str)]) -> Option<(i32, String)> {
    let t0 = Instant::now();
    let mut c = util::command("timeout");
    c.arg("--kill-after=10").arg(secs.to_string()).arg(prog).args(args).stdin(Stdio::null());
    c.envs(env.iter().copied());
    match c.output() {
        Ok(o) => {
            let code = o.status.code().unwrap_or(-1);
            if matches!(code, 124 | 137) && t0.elapsed().as_secs() >= secs {
                return None;
            }
            Some((code, format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr)).trim().to_string()))
        }
        Err(e) => Some((1, e.to_string())),
    }
}

/// shutil.which(name) or ~/.local/bin/name (the units' PATH may lack ~/.local/bin)
fn which(name: &str) -> String {
    use std::os::unix::fs::PermissionsExt;
    let path = std::env::var_os("PATH").unwrap_or_default();
    std::env::split_paths(&path)
        .map(|d| d.join(name))
        .find(|f| f.is_file() && f.metadata().is_ok_and(|m| m.permissions().mode() & 0o111 != 0))
        .map(|f| f.to_string_lossy().into_owned())
        .unwrap_or_else(|| format!("{}/.local/bin/{name}", home()))
}

pub(crate) fn commas(n: usize) -> String {
    let d = n.to_string();
    let mut out = String::new();
    for (i, c) in d.chars().enumerate() {
        if i > 0 && (d.len() - i) % 3 == 0 {
            out.push(',');
        }
        out.push(c);
    }
    out
}

/// str.splitlines()
fn splitlines(s: &str) -> Vec<&str> {
    let mut out = Vec::new();
    let mut start = 0;
    let mut it = s.char_indices().peekable();
    while let Some((i, c)) = it.next() {
        if matches!(c, '\n' | '\r' | '\u{b}' | '\u{c}' | '\u{1c}' | '\u{1d}' | '\u{1e}' | '\u{85}' | '\u{2028}' | '\u{2029}') {
            out.push(&s[start..i]);
            start = i + c.len_utf8();
            if c == '\r' && it.peek().map(|p| p.1) == Some('\n') {
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

pub fn b64(data: &[u8]) -> String {
    const A: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = String::new();
    for ch in data.chunks(3) {
        let n = ch.iter().enumerate().fold(0u32, |a, (i, b)| a | (*b as u32) << (16 - 8 * i));
        for i in 0..4 {
            out.push(if i <= ch.len() { A[(n >> (18 - 6 * i) & 63) as usize] as char } else { '=' });
        }
    }
    out
}

/// Every file under dir, its subdirectories walked (not those behind a symlink).
fn walk(dir: &Path, out: &mut Vec<PathBuf>) {
    for e in std::fs::read_dir(dir).into_iter().flatten().flatten() {
        if e.file_type().is_ok_and(|t| t.is_dir()) {
            walk(&e.path(), out);
        } else {
            out.push(e.path());
        }
    }
}

fn scene_missing(scene: &str, cands: Vec<String>, more: &str) -> String {
    if cands.is_empty() { format!("No scene matches {}.{more}", py_repr(scene)) } else { format!("More than one scene matches; say which:\n  {}", cands.join("\n  ")) }
}

// ---------------------------------------------------------------- cast files
pub fn cast_scene(scene: &str, script: &str) -> Result<String, String> {
    let (path, cands) = find_scene(scene);
    let Some(path) = path else { return Ok(scene_missing(scene, cands, "")) };
    let blocks = scene_blocks(&read_lossy(&path));
    let cast = match parse_cast(script) {
        Ok(c) => c,
        Err(e) => return Ok(format!("Not saved: {e}")),
    };
    if let Some(problem) = check_cast(&blocks, &cast) {
        return Ok(format!("Not saved \u{2014} {problem}\nRe-read scene_text and tag it without changing the words."));
    }
    let dir = root("scenes/cast");
    let _ = std::fs::create_dir_all(&dir);
    let out = dir.join(format!("{}.cast.md", stem(&path)));
    std::fs::write(&out, script.replace("\r\n", "\n").trim_end().to_string() + "\n").map_err(|e| e.to_string())?;
    let presets = root("build/voices.yaml");
    let voices = if presets.exists() { crate::pyyaml::load(&read_lossy(&presets))? } else { Value::Null };
    let assigned: Vec<String> = voices.as_object().map(|m| m.keys().filter(|k| !k.starts_with('_')).cloned().collect()).unwrap_or_default();
    let mut who: Vec<&str> = Vec::new();
    for (w, _, _) in cast.iter().flat_map(|(_, sp)| sp) {
        if !who.contains(&w.as_str()) {
            who.push(w);
        }
    }
    let missing: Vec<&str> = who.iter().copied().filter(|s| *s != "narrator" && !assigned.iter().any(|a| a == s)).collect();
    let mut lines = vec![format!("Saved {} \u{2014} {} voices: {}.", util::rel_posix(&out, &ROOT), who.len(), who.join(", "))];
    if !missing.is_empty() {
        lines.push(format!("No voice assigned yet (they will get a pool voice until build/voices.yaml names one): {}", missing.join(", ")));
    }
    lines.push("Now narrate_scene to render it; an older single-voice render of this scene is replaced.".into());
    Ok(lines.join("\n"))
}

// ---------------------------------------------------------------- narration jobs
fn jobs_file() -> PathBuf {
    root("build/.narrate_jobs.json")
}

fn jobs() -> Vec<Value> {
    let p = jobs_file();
    if !p.exists() {
        return vec![];
    }
    pyjson::loads(&read_lossy(&p)).ok().and_then(|v| v.as_array().cloned()).unwrap_or_default()
}

/// job[k], or the KeyError
fn key<'a>(j: &'a Value, k: &str) -> Result<&'a Value, String> {
    j.get(k).ok_or_else(|| format!("KeyError: '{k}'"))
}

fn job_state(j: &Value) -> Result<&'static str, String> {
    let log = PathBuf::from(s(Some(key(j, "log")?)));
    if !log.exists() {
        return Ok("starting");
    }
    let text = read_lossy(&log);
    let tail = tail(&text, 4000);
    Ok(if ["Traceback", "unknown voice", "model files missing"].iter().any(|w| tail.contains(w)) {
        "failed"
    } else if rx!(r"(?m)^audio: \d+ written").is_match(tail).unwrap_or(false) {
        "done"
    } else {
        "running"
    })
}

/// A job's state by id, as the bot polls it.
pub(crate) fn job_state_by_id(id: &str) -> String {
    jobs().iter().find(|j| s(j.get("id")) == id).map_or("unknown".to_string(), |j| job_state(j).unwrap_or("unknown").to_string())
}

/// The file a job wrote, read from its log's summary line.
pub(crate) fn job_output(id: &str) -> Option<PathBuf> {
    let jobs = jobs();
    let j = jobs.iter().find(|j| s(j.get("id")) == id)?;
    let text = read_lossy(Path::new(&s(j.get("log"))));
    let name = rx!(r"(?m)^\s+(\S+\.(?:mp3|wav)): [\d,]+ words").captures(tail(&text, 6000)).ok()??.get(1)?.as_str().to_string();
    fn find(dir: &Path, name: &str) -> Option<PathBuf> {
        for e in std::fs::read_dir(dir).ok()?.flatten() {
            let p = e.path();
            let hit = if p.is_dir() { find(&p, name) } else { (e.file_name().to_string_lossy() == name).then(|| p.clone()) };
            if hit.is_some() {
                return hit;
            }
        }
        None
    }
    find(&audio_dir(), &name)
}

fn audio_url(path: &Path, public: Public) -> String {
    let rel = util::rel_posix(path, &audio_dir());
    match public.filter(|(b, t)| !b.is_empty() && !t.is_empty()) {
        Some((b, t)) => format!("{b}/t/{t}/audio/{}", util::quote(&rel, "/", false)),
        None => path.to_string_lossy().into_owned(),
    }
}

/// sys.executable for the render: the venv's interpreter, picked as build/env.sh picks it.
pub(crate) fn python() -> String {
    use std::os::unix::fs::PermissionsExt;
    let exe = |p: &str| Path::new(p).metadata().is_ok_and(|m| m.is_file() && m.permissions().mode() & 0o111 != 0);
    util::env("WOTR_PYTHON").filter(|p| exe(p)).or_else(|| Some(format!("{}/.venvs/wotr/bin/python", home())).filter(|p| exe(p))).unwrap_or_else(|| "python3".into())
}

pub fn narrate_scene(scene: &str, voice: &str, engine: &str, public: Public) -> Result<String, String> {
    let (path, cands) = find_scene(scene);
    let Some(path) = path else { return Ok(scene_missing(scene, cands, " Scene files are listed in scenes/MANIFEST.md (scene_recall searches them).")) };
    let text = read_lossy(&path);
    let words = text.split_whitespace().count();
    let mut est = words as f64 / 18.0; // measured: 3,359 words in 184 s on the 7800X3D
    let dir = audio_dir();
    let _ = std::fs::create_dir_all(&dir);
    let mut jobs = jobs();
    let mut running = 0;
    for j in &jobs {
        running += usize::from(job_state(j)? == "running");
    }
    let job_id = writers::date_fmt("%Y%m%d-%H%M%S");
    let log = root(&format!("build/.narrate-{job_id}.log"));
    let engine = if engine.is_empty() { "local" } else { engine }.trim().to_lowercase();
    if engine != "local" && engine != "elevenlabs" {
        return Ok(format!("engine must be 'local' or 'elevenlabs', not {}.", py_repr(&engine)));
    }
    if engine == "elevenlabs" && public.is_some_and(|(_, t)| !t.is_empty()) {
        // the shared connector may burn Isaac's CPU, not his ElevenLabs plan
        return Ok("The ElevenLabs engine is not available over the shared connector; ask Isaac to render it from his desk.".into());
    }
    let lf = std::fs::File::create(&log).map_err(|e| e.to_string())?;
    // the render is this binary's `audio` (audio_export.py's port); WOTR_AUDIO_BIN is job_parity's stub
    // (a binary rebuilt under a running server reads as "<path> (deleted)"; the new one is at <path>)
    let exe = util::env("WOTR_AUDIO_BIN").map(PathBuf::from)
        .or_else(|| std::env::current_exe().ok().map(|p| PathBuf::from(p.to_string_lossy().trim_end_matches(" (deleted)"))))
        .ok_or("cannot find wotr-mcp")?;
    let mut c = util::command(exe);
    c.arg("audio").args(["--scene", &name_of(&path), "--voice", voice, "--out"]).arg(&dir).args(["--engine", &engine]);
    let mut child = c.stdin(Stdio::null()).stdout(lf.try_clone().map_err(|e| e.to_string())?).stderr(lf).spawn().map_err(|e| e.to_string())?;
    std::thread::spawn(move || child.wait()); // reaped, never waited on
    jobs.push(json!({"id": job_id, "scene": name_of(&path), "voice": voice, "engine": engine, "log": log.to_string_lossy(),
                     "started": writers::now_iso(), "words": words}));
    let keep = jobs.len().saturating_sub(40);
    let _ = std::fs::write(jobs_file(), pyjson::dumps_indent(&Value::Array(jobs.split_off(keep)), 1));
    let note = if running > 0 { format!(" ({running} other render(s) still running; they share the CPU)") } else { String::new() };
    let has_cast = root(&format!("scenes/cast/{}.cast.md", stem(&path))).exists();
    let mut how = if has_cast { format!("with its cast file (narrator voice {})", py_repr(voice)) } else { format!("in one voice, {}", py_repr(voice)) };
    if engine == "elevenlabs" {
        how += &format!(" on ElevenLabs (about {} characters billed to the plan)", commas(chars(&read_lossy(&path))));
        est = words as f64 / 8.0;
    }
    Ok(format!(
        "Rendering {} {how} \u{2014} job {job_id}, about {} words, roughly {:.0} min to render{note}. Output folder: {}. \
         Ask narration_status in a few minutes for the link. An unchanged scene already rendered with the same voices is skipped, not re-made.",
        name_of(&path),
        commas(words),
        est / 60.0,
        dir.display()
    ))
}

pub fn narration_status(job: &str, public: Public) -> Result<String, String> {
    let all = jobs();
    let sel: Vec<&Value> = all.iter().filter(|j| job.is_empty() || j.get("id") == Some(&json!(job))).collect();
    let mut lines = Vec::new();
    for j in sel[sel.len().saturating_sub(12)..].iter().rev() {
        let state = job_state(j)?;
        let mut extra = String::new();
        if state == "done" || state == "failed" {
            let log = read_lossy(Path::new(&s(j.get("log"))));
            extra = format!("  {}", splitlines(log.trim()).last().map_or("", |l| head(l, 200)));
        }
        lines.push(format!("- {}  {}  voice={}  {state}{extra}", s(Some(key(j, "id")?)), s(Some(key(j, "scene")?)), s(Some(key(j, "voice")?))));
    }
    if lines.is_empty() {
        lines.push("- no jobs recorded yet".into());
    }
    let dir = audio_dir();
    let mut files = Vec::new();
    if dir.exists() {
        let mut all = Vec::new();
        walk(&dir, &mut all);
        for ext in [".mp3", ".wav"] {
            let mut f: Vec<PathBuf> = all.iter().filter(|p| name_of(p).ends_with(ext)).cloned().collect();
            f.sort();
            files.extend(f);
        }
    }
    let mut out = vec!["Jobs:".to_string()];
    out.extend(lines);
    out.extend([String::new(), format!("Rendered ({}):", files.len())]);
    for f in &files[files.len().saturating_sub(60)..] {
        let size = f.metadata().map(|m| m.len()).unwrap_or(0) as f64;
        let mins = if name_of(f).ends_with(".mp3") { size / (96_000.0 / 8.0) / 60.0 } else { size / (24000.0 * 2.0) / 60.0 };
        out.push(format!("- {}  (~{mins:.0} min)  {}", util::rel_posix(f, &dir), audio_url(f, public)));
    }
    Ok(out.join("\n"))
}

// ---------------------------------------------------------------- research
fn reach(args: &[&str], secs: u64) -> Value {
    let fail = |code: &str, msg: String| json!({"ok": false, "error": {"code": code, "message": msg}});
    let exe = which("agent-reach");
    if !Path::new(&exe).exists() {
        return fail("NEED_SETUP", "agent-reach is not installed".into());
    }
    match run(&exe, args, secs, &[]) {
        None => fail("TIMEOUT", format!("no answer in {secs} s")),
        Some((_, out)) => match out.find('{') {
            None => fail("NO_OUTPUT", tail(&out, 300).into()),
            Some(i) => pyjson::loads(&out[i..]).unwrap_or_else(|e| fail("BAD_OUTPUT", e)),
        },
    }
}

/// (title, text) of a page through agent-browser; a bot check is reported as blocked; None on failure.
fn browser_read(url: &str) -> Option<(String, String)> {
    let ab = which("agent-browser");
    if !Path::new(&ab).exists() {
        return None;
    }
    const EXE: &str = "AGENT_BROWSER_EXECUTABLE_PATH";
    let env: Vec<(&str, &str)> = if std::env::var_os(EXE).is_none() && util::env(EXE).is_none() { vec![(EXE, "/usr/bin/chromium")] } else { vec![] };
    let go = |a: &[&str]| run(&ab, &[&["--session", "wotr-research"], a].concat(), 60, &env);
    let r = (|| {
        if go(&["open", url])?.0 != 0 {
            return Some(None);
        }
        let title = go(&["get", "title"])?.1.trim().to_string();
        let tl = title.to_lowercase();
        if ["just a moment", "attention required", "access denied"].iter().any(|p| tl.starts_with(p)) {
            return Some(Some((title, "(blocked by the site's bot check)".to_string())));
        }
        let (code, text) = go(&["get", "text", "body"])?;
        Some((code == 0 && !text.trim().is_empty()).then_some((title, text)))
    })();
    let _ = go(&["close"]);
    r.flatten()
}

fn wikitext_plain(t: &str) -> String {
    let mut t = rx!(r"(?s)<ref[^>]*>.*?</ref>|<ref[^>]*/>|<!--.*?-->").replace_all(t, "").into_owned();
    for _ in 0..3 {
        t = rx!(r"\{\{[^{}]*\}\}").replace_all(&t, "").into_owned(); // nested templates
    }
    let t = rx!(r"\[\[(?:File|Image|Category):[^\]]*\]\]").replace_all(&t, "");
    let t = rx!(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]").replace_all(&t, "${1}");
    let t = rx!(r"'{2,}").replace_all(&t, "");
    rx!(r"\n{3,}").replace_all(&t, "\n\n").trim().to_string()
}

fn pytype(v: &Value) -> &'static str {
    match v {
        Value::Null => "NoneType",
        Value::Bool(_) => "bool",
        Value::Number(n) if n.is_f64() => "float",
        Value::Number(_) => "int",
        Value::String(_) => "str",
        Value::Array(_) => "list",
        Value::Object(_) => "dict",
    }
}

/// v[k] as Python raises it
fn idx<'a>(v: &'a Value, k: &str) -> Result<&'a Value, String> {
    match v {
        Value::Object(m) => m.get(k).ok_or_else(|| format!("KeyError: '{k}'")),
        Value::Array(_) => Err("TypeError: list indices must be integers or slices, not str".into()),
        Value::String(_) => Err("TypeError: string indices must be integers, not 'str'".into()),
        o => Err(format!("TypeError: '{}' object is not subscriptable", pytype(o))),
    }
}

// Wikimedia throttles browser-looking agents (429); its policy wants a named tool with a URL
const UA: &str = "WOTR-research/1.0 (https://github.com/vispotvision/wotr-rule-index)";

/// lookup's sources (mcp_server.py's LOOKUP_SOURCES): key, label, site. A site is a MediaWiki host;
/// datamuse, jisho and dnd5e are plain JSON APIs.
const SOURCES: &[(&str, &str, &str)] = &[
    ("superpower", "Superpower Wiki", "https://powerlisting.fandom.com"),
    ("powerscaling", "Power Scaling Wiki", "https://psbattles.fandom.com"),
    ("vsbattles", "VS Battles Wiki", "https://vsbattles.fandom.com"),
    ("hxh", "Hunter x Hunter Wiki", "https://hunterxhunter.fandom.com"),
    ("jjk", "Jujutsu Kaisen Wiki", "https://jujutsu-kaisen.fandom.com"),
    ("bleach", "Bleach Wiki", "https://bleach.fandom.com"),
    ("naruto", "Narutopedia", "https://naruto.fandom.com"),
    ("dragonball", "Dragon Ball Wiki", "https://dragonball.fandom.com"),
    ("onepiece", "One Piece Wiki", "https://onepiece.fandom.com"),
    ("fma", "Fullmetal Alchemist Wiki", "https://fma.fandom.com"),
    ("finalfantasy", "Final Fantasy Wiki", "https://finalfantasy.fandom.com"),
    ("arcane", "Arcane Wiki", "https://arcane.fandom.com"),
    ("lotm", "Lord of the Mysteries Wiki", "https://lordofthemysteries.fandom.com"),
    ("reverend-insanity", "Reverend Insanity Wiki", "https://reverend-insanity.fandom.com"),
    ("worm", "Worm Wiki", "https://worm.fandom.com"),
    ("wiktenauer", "Wiktenauer", "https://wiktenauer.com"),
    ("tolkien", "Tolkien Gateway", "https://tolkiengateway.net"),
    ("wikipedia", "Wikipedia", "https://en.wikipedia.org"),
    ("wiktionary", "Wiktionary", "https://en.wiktionary.org"),
    ("wikisource", "Wikisource", "https://en.wikisource.org"),
    ("datamuse", "Datamuse", "https://api.datamuse.com"),
    ("jisho", "Jisho", "https://jisho.org"),
    ("dnd5e", "D&D 5e SRD", "https://www.dnd5eapi.co"),
];
const W_API: &[&str] = &["en.wikipedia.org", "en.wiktionary.org", "en.wikisource.org", "tolkiengateway.net"];

/// One GET as urllib made it; errors as "Type: message".
fn get_json(url: &str) -> Result<Value, String> {
    let o = util::command("curl")
        .args(["-s", "-L", "--http1.1", "--max-time", "30", "-A", UA, "-D", "/dev/stderr", url])
        .stdin(Stdio::null())
        .output()
        .map_err(|e| format!("FileNotFoundError: {e}"))?;
    // shortcut: curl's failures named as urllib's commonest; the errno text can differ from Python's
    match o.status.code() {
        Some(0) => {}
        Some(28) => return Err("TimeoutError: timed out".into()),
        Some(6) => return Err("URLError: <urlopen error [Errno -3] Temporary failure in name resolution>".into()),
        Some(7) => return Err("URLError: <urlopen error [Errno 111] Connection refused>".into()),
        c => return Err(format!("URLError: <urlopen error curl exit {}>", c.unwrap_or(-1))),
    }
    let heads = String::from_utf8_lossy(&o.stderr);
    let status = heads.lines().filter_map(|l| l.strip_prefix("HTTP/")).last().unwrap_or("").trim_end_matches('\r').to_string();
    let mut sp = status.splitn(3, ' ').skip(1);
    let code: u16 = sp.next().and_then(|c| c.parse().ok()).unwrap_or(0);
    if !(200..300).contains(&code) {
        return Err(format!("HTTPError: HTTP Error {code}: {}", sp.next().unwrap_or("")));
    }
    let body = String::from_utf8(o.stdout).map_err(|e| {
        let i = e.utf8_error().valid_up_to();
        format!("UnicodeDecodeError: 'utf-8' codec can't decode byte 0x{:02x} in position {i}: invalid start byte", e.as_bytes()[i])
    })?;
    pyjson::loads(&body).map_err(|e| format!("JSONDecodeError: {e}"))
}

/// One MediaWiki API call.
fn api_get(api: &str, params: &[(&str, &str)]) -> Result<Value, String> {
    let q: Vec<String> = params.iter().chain(&[("format", "json"), ("formatversion", "2")]).map(|(k, v)| format!("{}={}", util::quote(k, "", true), util::quote(v, "", true))).collect();
    get_json(&format!("{api}{}", q.join("&")))
}

/// `x.get(k)` as Python raises it on a non-dict
fn dict_get(v: &Value, k: &str) -> Result<Value, String> {
    match v {
        Value::Object(m) => Ok(m.get(k).cloned().unwrap_or(Value::Null)),
        o => Err(format!("AttributeError: '{}' object has no attribute 'get'", pytype(o))),
    }
}

/// shortcut: numeric references and the entities wiki HTML uses, not all of html.unescape's; add a name if one shows up raw
fn html_unescape(t: &str) -> String {
    rx!(r"&(?:#(\d+)|#[xX]([0-9a-fA-F]+)|(amp|lt|gt|quot|apos|nbsp));")
        .replace_all(t, |c: &fancy_regex::Captures<'_, str>| {
            let code = c.get(1).and_then(|m| m.as_str().parse().ok()).or_else(|| c.get(2).and_then(|m| u32::from_str_radix(m.as_str(), 16).ok()));
            match (code, c.get(3).map(|m| m.as_str())) {
                (Some(n), _) => char::from_u32(n).unwrap_or('\u{fffd}').to_string(),
                (_, Some("amp")) => "&".to_string(),
                (_, Some("lt")) => "<".to_string(),
                (_, Some("gt")) => ">".to_string(),
                (_, Some("quot")) => "\"".to_string(),
                (_, Some("apos")) => "'".to_string(),
                _ => "\u{a0}".to_string(),
            }
        })
        .into_owned()
}

fn html_plain(h: &str) -> String {
    let h = rx!(r"(?s)<(style|script)[^>]*>.*?</\1>|<!--.*?-->").replace_all(h, "");
    let h = rx!(r"<(?:br|/p|/div|/li|/h\d)[^>]*>").replace_all(&h, "\n");
    let t = html_unescape(&rx!(r"<[^>]+>").replace_all(&h, ""));
    rx!(r"\n\s*\n\s*(?:\n\s*)+").replace_all(&t, "\n\n").trim().to_string()
}

/// A wiki page's title and plain text; None when the wiki has no such page.
fn wiki_page(api: &str, host: &str, title: &str) -> Result<Option<(String, String)>, String> {
    if host == "en.wikipedia.org" || host == "en.wiktionary.org" {
        // TextExtracts: templates rendered, not stripped
        let r = api_get(api, &[("action", "query"), ("prop", "extracts"), ("explaintext", "1"), ("titles", title), ("redirects", "1")])?;
        let pages = idx(idx(&r, "query")?, "pages")?;
        let p = pages.get(0).ok_or("IndexError: list index out of range")?;
        if t(p.get("missing")) || !t(p.get("extract")) {
            return Ok(None);
        }
        return Ok(Some((s(Some(idx(p, "title")?)), s(Some(idx(p, "extract")?)).trim().to_string())));
    }
    // Wikisource's texts are transcluded from scans: only the rendered page holds them
    let prop = if host == "en.wikisource.org" { "text" } else { "wikitext" };
    let p = dict_get(&api_get(api, &[("action", "parse"), ("page", title), ("prop", prop), ("redirects", "1")])?, "parse")?;
    if !t(Some(&p)) {
        return Ok(None);
    }
    let body = s(Some(idx(&p, prop)?));
    Ok(Some((s(Some(idx(&p, "title")?)), if prop == "text" { html_plain(&body) } else { wikitext_plain(&body) })))
}

fn lookup_in(source: &str, label: &str, site: &str, query: &str) -> Result<String, String> {
    let q = |x: &str| util::quote(x, "", false);
    match source {
        "datamuse" => {
            // Datamuse's own parameters pass through (rel_jjb=blood, sl=krang); a bare query means "means like"
            let params = if query.contains('=') { query.to_string() } else { format!("ml={query}") };
            let qs: Vec<String> = params.split('&').filter_map(|p| p.split_once('=')).map(|(k, v)| format!("{}={}", q(k.trim()), q(v.trim()))).collect();
            let got = get_json(&format!("{site}/words?{}&max=60", qs.join("&")))?;
            let words: Vec<String> = got.as_array().into_iter().flatten().map(|w| Ok(s(Some(idx(w, "word")?)))).collect::<Result<_, String>>()?;
            return Ok(format!("## {label}: {params}\n{}", if words.is_empty() { "(no words)".to_string() } else { words.join(", ") }));
        }
        "jisho" => {
            let got = get_json(&format!("{site}/api/v1/search/words?keyword={}", q(query)))?;
            let mut lines = Vec::new();
            for e in idx(&got, "data")?.as_array().into_iter().flatten().take(10) {
                let j = idx(e, "japanese")?.get(0).ok_or("IndexError: list index out of range")?;
                let word = if t(j.get("word")) { s(j.get("word")) } else { s(j.get("reading")) };
                let reading = j.get("reading").map(|r| s(Some(r))).unwrap_or_default();
                let mut senses = Vec::new();
                for sn in idx(e, "senses")?.as_array().into_iter().flatten().take(3) {
                    senses.push(idx(sn, "english_definitions")?.as_array().into_iter().flatten().map(|d| s(Some(d))).collect::<Vec<_>>().join(", "));
                }
                lines.push(format!("- {word} ({reading}): {}", senses.join("; ")));
            }
            return Ok(format!("## {label}: {query}\n{}", if lines.is_empty() { "(no words)".to_string() } else { lines.join("\n") }));
        }
        "dnd5e" => {
            let got = get_json(&format!("{site}/api/2014/spells?name={}", q(query)))?;
            let hits = idx(&got, "results")?.as_array().cloned().unwrap_or_default();
            let Some(first) = hits.first() else {
                return Ok(format!("## {label}: nothing matches '{query}'"));
            };
            let best = hits.iter().position(|h| h.get("name").is_some_and(|n| s(Some(n)).to_lowercase() == query.to_lowercase())).map_or(first, |i| &hits[i]);
            let sp = get_json(&format!("{site}/api/2014/spells/{}", s(Some(idx(best, "index")?))))?;
            let others: Vec<String> = hits.iter().filter(|h| !std::ptr::eq(*h, best)).map(|h| Ok(s(Some(idx(h, "name")?)))).collect::<Result<_, String>>()?;
            let also = if others.is_empty() { String::new() } else { format!("also matched: {}\n", others.join(", ")) };
            let text: Vec<String> = idx(&sp, "desc")?.as_array().into_iter().flatten().chain(sp.get("higher_level").and_then(Value::as_array).into_iter().flatten()).map(|x| s(Some(x))).collect();
            return Ok(format!(
                "## {label}: {} (level {} {}; {}, {})\n{also}\n{}",
                s(Some(idx(&sp, "name")?)),
                s(Some(idx(&sp, "level")?)),
                s(Some(idx(idx(&sp, "school")?, "name")?)),
                s(Some(idx(&sp, "range")?)),
                s(Some(idx(&sp, "duration")?)),
                text.join("\n\n")
            ));
        }
        _ => {}
    }
    let host = site.split("//").nth(1).unwrap_or("");
    let api = format!("{site}{}", if W_API.contains(&host) { "/w/api.php?" } else { "/api.php?" });
    // a site may fence search behind a bot check (Tolkien Gateway) and still serve pages
    let hits = api_get(&api, &[("action", "query"), ("list", "search"), ("srsearch", query), ("srlimit", "5")])
        .ok()
        .and_then(|f| f.get("query")?.get("search")?.as_array().cloned())
        .unwrap_or_default();
    // the page named exactly as asked wins (its redirects followed); search order only breaks ties
    let got = match wiki_page(&api, host, query)? {
        Some(g) => Some(g),
        None => match hits.first() {
            Some(h) => wiki_page(&api, host, &s(Some(idx(h, "title")?)))?,
            None => None,
        },
    };
    let Some((title, text)) = got else {
        return Ok(format!("## {label}: nothing matches '{query}'"));
    };
    let mut others = Vec::new();
    for h in &hits {
        let n = s(Some(idx(h, "title")?));
        if n != title {
            others.push(n);
        }
    }
    let url = format!("{site}/wiki/{}", util::quote(&title.replace(' ', "_"), "/", false));
    let also = if others.is_empty() { String::new() } else { format!("also matched: {}\n", others.join(", ")) };
    Ok(format!("## {label}: {title} ({url})\n{also}\n{}{}", head(&text, 9000), if chars(&text) > 9000 { "\n...[truncated]" } else { "" }))
}

/// One source's best match for `query` as text; a failure is reported, never raised.
pub fn lookup(source: &str, query: &str) -> String {
    let (source, query) = (source.trim().to_lowercase(), query.trim());
    let Some(&(_, label, site)) = SOURCES.iter().find(|x| x.0 == source) else {
        return format!("## lookup: no source '{source}'; sources: {}", SOURCES.iter().map(|x| x.0).collect::<Vec<_>>().join(", "));
    };
    lookup_in(&source, label, site, query).unwrap_or_else(|e| format!("## {label}: lookup failed ({e})"))
}

/// `x.get(k) or {}`, then its .get(k2): the AttributeError when that is not a dict
fn or_get(v: &Value, k: &str, k2: &str) -> Result<Option<Value>, String> {
    match v.get(k).filter(|x| t(Some(x))) {
        None => Ok(None),
        Some(Value::Object(m)) => Ok(m.get(k2).cloned()),
        Some(o) => Err(format!("AttributeError: '{}' object has no attribute 'get'", pytype(o))),
    }
}

fn trunc(text: &str, n: usize) -> String {
    format!("{}{}", head(text.trim(), n), if chars(text) > n { "\n...[truncated]" } else { "" })
}

pub fn research(question: &str, read: i64, urls: &[String], power: &str) -> Result<String, String> {
    let mut out = vec!["[Outside research via Agent Reach; not canon, never a rule source]".to_string()];
    let found = reach(&["web", "search", question, "--limit", "6"], 90);
    let items: Vec<Value> = found.get("items").and_then(Value::as_array).cloned().unwrap_or_default();
    if !t(found.get("ok")) {
        let code = or_get(&found, "error", "code")?;
        let msg = or_get(&found, "error", "message")?.map(|m| s(Some(&m))).unwrap_or_default();
        out.push(format!("## Search failed: {}: {}", s(code.as_ref()), head(&msg, 200)));
    } else {
        let lines: Vec<String> = items
            .iter()
            .map(|i| {
                let title = if t(i.get("title")) { s(i.get("title")) } else { s(i.get("url")) };
                let text = if t(i.get("text")) { s(i.get("text")) } else { String::new() };
                format!("- {title} ({})\n  {}", s(i.get("url")), head(text.trim(), 500).replace('\n', " "))
            })
            .collect();
        out.push(format!("## Search: {question}\n{}", lines.join("\n")));
    }
    let mut pages: Vec<String> = urls.to_vec();
    pages.extend(items.iter().filter(|i| t(i.get("url"))).map(|i| s(i.get("url"))).filter(|u| !u.contains("fandom.com")).take(read.clamp(0, 5) as usize));
    let mut seen: Vec<String> = Vec::new();
    for u in pages {
        if seen.contains(&u) {
            continue;
        }
        seen.push(u.clone());
        let r = reach(&["read", &u], 90);
        if !t(r.get("ok")) {
            match browser_read(&u) {
                Some((title, text)) => out.push(format!("## {} ({u}, read in a browser)\n\n{}", if title.is_empty() { &u } else { &title }, trunc(&text, 7000))),
                None => out.push(format!("## Could not read {u}: {}", s(or_get(&r, "error", "code")?.as_ref()))),
            }
            continue;
        }
        for i in r.get("items").filter(|x| t(Some(x))).and_then(Value::as_array).into_iter().flatten().take(1) {
            let text = if t(i.get("text")) { s(i.get("text")).trim().to_string() } else { String::new() };
            let title = if t(i.get("title")) { s(i.get("title")) } else { u.clone() };
            out.push(format!("## {title} ({u})\n\n{}", trunc(&text, 7000)));
        }
    }
    if !power.trim().is_empty() {
        out.push(lookup("superpower", power));
    }
    Ok(out.join("\n\n"))
}

// ---------------------------------------------------------------- ChatGPT and Claude (build/ask_*.sh)
fn ask(who: &str, script: &str, prompt: &str, minutes: u64) -> String {
    match run("bash", &[&root(&format!("build/{script}")).to_string_lossy(), prompt], minutes * 60, &[]) {
        None => format!("{who} took longer than {minutes} minutes; ask a narrower question"),
        Some((0, out)) => out.trim().to_string(),
        Some((code, out)) => format!("{who} call failed ({code}): {}", tail(out.trim(), 600)),
    }
}

pub fn ask_chatgpt(prompt: &str) -> String {
    ask("ChatGPT", "ask_chatgpt.sh", prompt, 5)
}

pub fn ask_claude(prompt: &str) -> String {
    ask("Claude", "ask_claude.sh", prompt, 5)
}

const RESEARCH_BRIEF: &str = "You are the research desk for War of the Realms, a fantasy setting whose magic is explained with real
science. Research the question below with live web search; you may also read the repo's wotr tools (codex,
load_rules with tags [\"magic-design\", \"magic-mechanism\"]) for the WOTR side, but the research itself is about
the real world. Return markdown with these sections:
## Phenomenon: the real phenomenon, named in scientific terms.
## Governing law: the equations or principles, with real measured figures and units.
## Limits: the boundary conditions, what caps it, at what scale it stops working.
## Failure modes and costs: what breaks, what it does to a body or a material, how fast.
## Precedent: the nearest treatments in anime, games and fiction, so we know what not to copy.
## Sources: every URL you actually opened, numbered; cite them inline as [n] after each figure.
Say where sources disagree. Never invent a figure: an estimate is marked as one. Change no files.

Question:
";

pub fn research_chatgpt(question: &str, thread: &str) -> String {
    let (q, th) = (question.to_string(), thread.to_string());
    let h = std::thread::spawn(move || {
        let answer = ask("ChatGPT", "ask_chatgpt.sh", &format!("{RESEARCH_BRIEF}{q}"), 15);
        let body = format!("[ChatGPT research with live web search; outside source, never a rule source]\n\n**Question:** {q}\n\n{answer}");
        writers::handoff("research", &format!("Research: {}", head(&q, 90)), &body, &th);
    });
    BACKGROUND.lock().unwrap().push(h);
    "ChatGPT is researching; the write-up lands in the inbox as a research item in 2 to 10 minutes.".into()
}

/// The image block (base64, MIME type), if any, and the text.
pub fn chatgpt_image(prompt: &str, name: &str, public: Public) -> Result<(Option<(String, String)>, String), String> {
    let start = SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs_f64() - 1.0;
    let said = ask(
        "ChatGPT",
        "ask_chatgpt.sh",
        &format!("Generate exactly one image with your image generation tool from the brief below, then reply with only the image's file path. Write no other files.\n\n{prompt}"),
        5,
    );
    let mtime = |p: &Path| p.metadata().and_then(|m| m.modified()).map_or(0.0, |t| t.duration_since(SystemTime::UNIX_EPOCH).map_or(0.0, |d| d.as_secs_f64()));
    let suffix = |p: &Path| p.extension().map(|e| format!(".{}", e.to_string_lossy().to_lowercase())).unwrap_or_default();
    let mut made = Vec::new();
    walk(&PathBuf::from(home()).join(".codex/generated_images"), &mut made);
    made.retain(|p| [".png", ".jpg", ".jpeg", ".webp"].contains(&suffix(p).as_str()) && mtime(p) >= start);
    made.sort_by(|a, b| mtime(a).total_cmp(&mtime(b)));
    let Some(src) = made.last() else { return Ok((None, format!("no image came back. ChatGPT said: {}", tail(&said, 600)))) };
    let images = PathBuf::from(home()).join("wotr-drafts/images");
    std::fs::create_dir_all(&images).map_err(|e| e.to_string())?;
    let slug = writers::slug_us(if name.is_empty() { prompt } else { name });
    let out = images.join(format!("{}-{}{}", writers::date_fmt("%Y%m%d-%H%M%S"), head(&slug, 40), suffix(src)));
    std::fs::copy(src, &out).map_err(|e| e.to_string())?;
    if let (Ok(m), Ok(f)) = (src.metadata(), std::fs::File::options().write(true).open(&out)) {
        let _ = f.set_times(std::fs::FileTimes::new().set_accessed(m.accessed().unwrap_or(SystemTime::now())).set_modified(m.modified().unwrap_or(SystemTime::now())));
    }
    // a ~1024 px JPEG for the chat; the full image stays on disk and behind the link
    let preview = util::command("magick")
        .arg(&out)
        .args(["-resize", "1024x1024>", "-quality", "85", "jpg:-"])
        .stdin(Stdio::null())
        .output()
        .map_err(|_| "FileNotFoundError: [Errno 2] No such file or directory: 'magick'".to_string())?
        .stdout;
    let mut text = format!("saved {}", out.display());
    if let Some((b, t)) = public.filter(|(b, t)| !b.is_empty() && !t.is_empty()) {
        text += &format!("\nlink: {b}/t/{t}/images/{}", util::quote(&name_of(&out), "/", false));
    }
    let image = if !preview.is_empty() {
        (b64(&preview), "image/jpeg".to_string())
    } else {
        let mime = match suffix(&out).as_str() {
            ".png" => "image/png",
            ".jpg" | ".jpeg" => "image/jpeg",
            ".webp" => "image/webp",
            _ => "application/octet-stream",
        };
        (b64(&std::fs::read(&out).map_err(|e| e.to_string())?), mime.to_string())
    };
    Ok((Some(image), text))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn helpers() {
        assert_eq!(b64(b""), "");
        assert_eq!(b64(b"f"), "Zg==");
        assert_eq!(b64(b"fo"), "Zm8=");
        assert_eq!(b64(b"foobar"), "Zm9vYmFy");
        assert_eq!(commas(1234567), "1,234,567");
        assert_eq!(commas(999), "999");
        assert_eq!(splitlines("a\r\nb\rc\n\nd\u{2028}"), vec!["a", "b", "c", "", "d"]);
        assert_eq!(format!("{:.0} {:.0} {:.0}", 0.5, 1.5, 2.5), "0 2 2"); // Python's round-half-even
        assert_eq!(util::quote("a b/é~", "/", false), "a%20b/%C3%A9~");
        assert_eq!(util::quote("a b/", "", true), "a+b%2F");
        assert_eq!(wikitext_plain("x<ref>r</ref>{{a{{b}}}}[[File:f.png]][[Link|shown]] '''bold'''\n\n\n\ny"), "xshown bold\n\ny");
    }
}
