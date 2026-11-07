//! The local humanizer pass (Isaac, 2026-11-07): a fine-tuned rewriting model on Ultron's Ollama goes
//! over a draft chunk by chunk, and a guard keeps the draft's own paragraph wherever a rewrite would
//! damage WOTR's law. The model never touches windows, headers or the author notes, and a dead model
//! hands the draft back unchanged, so this pass can never block or lose a scene.
use crate::{util, verify};
use regex::Regex;
use serde_json::{Value, json};
use std::collections::{HashMap, HashSet};
use std::io::Write;
use std::process::Stdio;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{LazyLock, Mutex, mpsc};
use std::time::Duration;

const DEFAULT_MODEL: &str = "hf.co/abacusai/Smaug-Humanizer-GGUF:Q8_0";
const PROMPT: &str = "Rewrite the AI-written text below so that it reads as if a person wrote it, in a person's own voice, wording and rhythm.\n\nKeep every fact, number, name and quote. Keep the structure and the language of the text. Output only the rewritten text.\n\nText:\n";
/// The model card's limit is about 500 words a call.
const CHUNK_WORDS: usize = 450;
/// Chunks at once; the humanizer's Ollama has one slot for each (OLLAMA_NUM_PARALLEL).
const SLOTS: usize = 4;
/// Tokens per slot, the model card's figure. Measured on the 9070 XT: Q8_0 at 4 slots does 104 tokens a
/// second in all against 33 at one, in 13.7 GiB; 6 slots did not finish and filled the card.
const CONTEXT: u32 = 8192;
/// The law says do not shorten, and the fights lose Blow Card parts first.
const MIN_LENGTH: f64 = 0.9;
const MAX_LENGTH: f64 = 1.4;
/// A rewrite keeping more of the draft's words than this changed nothing worth the risk.
const NEAR_COPY: f64 = 0.9;
/// A line this short is a beat the draft placed on purpose (a sound, a turn); it stays as written.
const PINNED_WORDS: usize = 4;

static PROPER: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\b\p{Lu}[\p{L}'’-]+").unwrap());
static QUOTE: LazyLock<Regex> = LazyLock::new(|| Regex::new(r#"["“][^"“”\n]*["”]"#).unwrap());
static ITALIC: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\*+[^*\n]+\*+").unwrap());
static NUMBER: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\d[\d,.]*\d|\d").unwrap());
static WORD: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"[\p{L}\p{N}'’-]+").unwrap());
static BREAK: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"\n[ \t]*\n\s*").unwrap());
/// Plain romanized state words (gogogogo, zawa zawa, doki-doki, shiin), which carry no italics to protect them.
static STATE_WORD: LazyLock<Regex> = LazyLock::new(|| Regex::new(r"(?i)\b(?:shiin|zawa zawa|doki-doki|go(?:go)+|gogogo)\b").unwrap());

fn word_count(s: &str) -> usize {
    s.split_whitespace().count()
}

fn plain_quotes(s: &str) -> String {
    s.replace(['“', '”'], "\"").replace(['‘', '’'], "'")
}

/// A character is at a sentence's start when only opening marks stand between it and the last stop.
fn sentence_start(text: &str, at: usize) -> bool {
    let before = text[..at].trim_end_matches(['"', '“', '‘', '\'', '*', '(', '_', ' ', '\t', '\n']);
    before.is_empty() || before.ends_with(['.', '!', '?', ':', '…', '"', '”', '*'])
}

/// Every capitalized word used mid-sentence anywhere in the scene is a name of something.
fn names(scene: &str) -> HashSet<String> {
    const COMMON: &[&str] = &["The", "He", "She", "It", "They", "We", "You", "His", "Her", "Their", "And", "But", "An", "In", "On", "At", "If", "So", "Then", "There", "This", "That", "What", "Who", "When", "Why", "How", "No", "Yes", "Not"];
    PROPER.find_iter(scene).filter(|m| !sentence_start(scene, m.start()) && !COMMON.contains(&m.as_str())).map(|m| plain_quotes(m.as_str())).collect()
}

fn found(text: &str, r: &Regex) -> Vec<String> {
    r.find_iter(text).map(|m| plain_quotes(m.as_str())).collect()
}

/// Why this rewrite of `old` cannot stand, or None if it can.
fn flaw(old: &str, new: &str, scene_names: &HashSet<String>) -> Option<String> {
    let flat = plain_quotes(new);
    let lost = |what: &str, items: Vec<String>| items.into_iter().find(|i| !flat.contains(i.as_str())).map(|i| format!("lost {what} {}", util_head(&i)));
    let (old_words, new_words) = (word_count(old) as f64, word_count(new) as f64);
    if new_words < old_words * MIN_LENGTH {
        return Some("too short".into());
    }
    if new_words > old_words * MAX_LENGTH {
        return Some("too long".into());
    }
    lost("dialogue", found(old, &QUOTE))
        .or_else(|| lost("italics", found(old, &ITALIC)))
        .or_else(|| lost("number", found(old, &NUMBER)))
        .or_else(|| lost("sound", found(old, &STATE_WORD)))
        .or_else(|| {
            PROPER.find_iter(old).map(|m| plain_quotes(m.as_str())).filter(|n| scene_names.contains(n)).find(|n| !flat.contains(n.as_str())).map(|n| format!("lost name {n}"))
        })
        .or_else(|| {
            let old_flat = plain_quotes(old);
            PROPER.find_iter(new).find(|m| !sentence_start(new, m.start()) && !scene_names.contains(&plain_quotes(m.as_str())) && !old_flat.contains(&plain_quotes(m.as_str()))).map(|m| format!("invented name {}", m.as_str()))
        })
        .or_else(|| match verify::run(new, &verify::Opts::default()) {
            Ok(r) if !r.fails.is_empty() => Some(format!("verify: {}", util_head(&r.fails[0]))),
            _ => None,
        })
}

fn util_head(s: &str) -> String {
    s.chars().take(60).collect()
}

/// How much of the draft's wording survives, 0 to 1.
fn overlap(old: &str, new: &str) -> f64 {
    let lower = |s: &str| found(s, &WORD).into_iter().map(|w| w.to_lowercase()).collect::<Vec<_>>();
    let (a, b) = (lower(old), lower(new));
    let mut pool: HashMap<&str, i32> = HashMap::new();
    for w in &b {
        *pool.entry(w).or_default() += 1;
    }
    let kept = a.iter().filter(|w| pool.get_mut(w.as_str()).is_some_and(|n| { *n -= 1; *n >= 0 })).count();
    kept as f64 / a.len().max(1) as f64
}

#[derive(Clone, Copy, PartialEq)]
enum Kind {
    /// Goes to the model and may be replaced.
    Prose,
    /// Goes to the model for context; the draft's own line stands.
    Pinned,
    /// Never leaves the draft: windows, headers, rules, tables, whole-italic lines, mostly-dialogue paragraphs.
    Fixed,
}

fn kind(p: &str) -> Kind {
    let t = p.trim();
    let line = |f: &dyn Fn(&str) -> bool| t.lines().any(|l| f(l.trim()));
    if t.starts_with(['#', '>', '|']) || t.starts_with("```") || t.starts_with("---") || t.starts_with("***") {
        return Kind::Fixed;
    }
    if line(&|l| l.starts_with('[') && l.ends_with(']')) {
        return Kind::Fixed; // a window (R84-1)
    }
    if t.starts_with('*') && t.ends_with('*') && ITALIC.find(t).is_some_and(|m| m.len() == t.len()) {
        return Kind::Fixed; // a place-and-hour header or a capital sound line
    }
    let spoken: usize = QUOTE.find_iter(t).map(|m| word_count(m.as_str())).sum();
    if spoken as f64 > word_count(t) as f64 * 0.7 {
        return Kind::Fixed; // a voice is built from its card; nothing here reads a card
    }
    if word_count(t) <= PINNED_WORDS { Kind::Pinned } else { Kind::Prose }
}

/// The draft cut into the part the pass may read and the part it leaves alone (frontmatter, author notes).
fn split_body(text: &str) -> (&str, &str, &str) {
    let mut start = 0;
    if text.starts_with("---\n")
        && let Some(end) = text[4..].find("\n---\n")
    {
        start = 4 + end + 5;
    }
    let body = verify::before_notes(&text[start..]);
    (&text[..start], body, &text[start + body.len()..])
}

/// Consecutive paragraphs a call can take together, as indexes.
fn chunks(paras: &[(String, Kind)]) -> Vec<Vec<usize>> {
    let mut out: Vec<Vec<usize>> = Vec::new();
    let mut cur = Vec::new();
    let mut words = 0;
    for (i, (p, k)) in paras.iter().enumerate() {
        if *k == Kind::Fixed || (words > 0 && words + word_count(p) > CHUNK_WORDS) {
            if cur.iter().any(|&j: &usize| paras[j].1 == Kind::Prose) {
                out.push(std::mem::take(&mut cur));
            }
            cur.clear();
            words = 0;
        }
        if *k != Kind::Fixed {
            cur.push(i);
            words += word_count(p);
        }
    }
    if cur.iter().any(|&j| paras[j].1 == Kind::Prose) {
        out.push(cur);
    }
    out
}

struct Pass {
    text: String,
    report: String,
}

/// What one chunk's tries came to: the paragraphs that stand, and why the others keep the draft.
struct Outcome {
    rewrites: Vec<(usize, String)>,
    kept: Vec<String>,
    failure: Option<String>,
}

type Generate<'a> = &'a (dyn Fn(&str) -> Result<String, String> + Sync);

fn rewrite_chunk(chunk: &[usize], paras: &[(String, Kind)], scene_names: &HashSet<String>, tries: usize, generate: Generate) -> Outcome {
    let input = chunk.iter().map(|&i| paras[i].0.as_str()).collect::<Vec<_>>().join("\n\n");
    let mut open: Vec<usize> = chunk.iter().copied().filter(|&i| paras[i].1 == Kind::Prose).collect();
    let mut out = Outcome { rewrites: Vec::new(), kept: Vec::new(), failure: None };
    let mut last_why: HashMap<usize, String> = HashMap::new();
    for _ in 0..tries {
        if open.is_empty() {
            break;
        }
        let reply = match generate(&input) {
            Ok(r) => r,
            Err(e) => {
                out.failure = Some(e);
                break;
            }
        };
        let got: Vec<&str> = BREAK.split(reply.trim()).filter(|p| !p.trim().is_empty()).collect();
        if got.len() != chunk.len() {
            for &i in &open {
                last_why.insert(i, "paragraphs did not line up".into());
            }
            continue;
        }
        open.retain(|&i| {
            let new = got[chunk.iter().position(|&c| c == i).unwrap_or(0)].trim();
            match flaw(&paras[i].0, new, scene_names).or_else(|| (overlap(&paras[i].0, new) > NEAR_COPY).then(|| "near copy".to_string())) {
                None => {
                    out.rewrites.push((i, new.to_string()));
                    false
                }
                Some(w) => {
                    last_why.insert(i, w);
                    true
                }
            }
        });
    }
    for i in open {
        let w = last_why.remove(&i).unwrap_or_else(|| "model unavailable".into());
        out.kept.push(w.split(' ').take(2).collect::<Vec<_>>().join(" "));
    }
    out
}

/// The whole pass, with the model as a function so the tests can stand in for it.
fn run(text: &str, tries: usize, generate: Generate, progress: &(dyn Fn(usize, usize) + Sync)) -> Pass {
    let (head, body, tail) = split_body(text);
    let mut paras: Vec<(String, Kind)> = BREAK.split(body.trim()).filter(|p| !p.trim().is_empty()).map(|p| (p.trim_end().to_string(), kind(p))).collect();
    let mut fence = false;
    for (p, k) in &mut paras {
        if fence || p.trim_start().starts_with("```") {
            *k = Kind::Fixed;
            fence ^= p.matches("```").count() % 2 == 1;
        }
    }
    let prose = paras.iter().filter(|p| p.1 != Kind::Fixed || !p.0.trim_start().starts_with(['#', '[', '|', '`', '-'])).map(|p| p.0.as_str()).collect::<Vec<_>>().join("\n\n");
    let scene_names = names(&prose);
    let work = chunks(&paras);
    let total = paras.iter().filter(|p| p.1 == Kind::Prose).count();
    let (next, finished, stop) = (AtomicUsize::new(0), AtomicUsize::new(0), AtomicBool::new(false));
    let outcomes: Vec<Outcome> = std::thread::scope(|s| {
        let workers: Vec<_> = (0..SLOTS.min(work.len()))
            .map(|_| {
                s.spawn(|| {
                    let mut mine = Vec::new();
                    while !stop.load(Ordering::Relaxed) {
                        let Some(chunk) = work.get(next.fetch_add(1, Ordering::Relaxed)) else { break };
                        let o = rewrite_chunk(chunk, &paras, &scene_names, tries, generate);
                        stop.fetch_or(o.failure.is_some(), Ordering::Relaxed);
                        mine.push(o);
                        progress(finished.fetch_add(1, Ordering::Relaxed) + 1, work.len());
                    }
                    mine
                })
            })
            .collect();
        workers.into_iter().flat_map(|w| w.join().unwrap_or_default()).collect()
    });
    let (mut changed, mut why, mut failure) = (0, HashMap::<String, usize>::new(), None);
    for o in outcomes {
        for (i, new) in o.rewrites {
            paras[i].0 = new;
            changed += 1;
        }
        for w in o.kept {
            *why.entry(w).or_default() += 1;
        }
        failure = failure.or(o.failure);
    }
    let mut reasons: Vec<_> = why.into_iter().map(|(k, v)| format!("{k}: {v}")).collect();
    reasons.sort();
    let mut report = format!("humanize: {changed} of {total} prose paragraphs rewritten");
    if !reasons.is_empty() {
        report += &format!("; the rest keep the draft ({})", reasons.join(", "));
    }
    if let Some(e) = failure {
        report += &format!("\nThe model stopped: {e}. Everything it had not reached is the draft, unchanged.");
    }
    let joined = paras.into_iter().map(|p| p.0).collect::<Vec<_>>().join("\n\n");
    let sep = if tail.is_empty() { "\n" } else { "\n\n" };
    Pass { text: format!("{head}{joined}{sep}{tail}"), report }
}

/// One call to the model, on the humanizer's own Ollama or, with that one down, the system one.
/// keep_alive stays short so the card goes back to ComfyUI and narration.
fn ollama(input: &str) -> Result<String, String> {
    ollama_at("http://127.0.0.1:11435", input).or_else(|e| if e.starts_with("Ollama is not answering") { ollama_at("http://127.0.0.1:11434", input) } else { Err(e) })
}

fn ollama_at(base: &str, input: &str) -> Result<String, String> {
    let model = util::env("WOTR_HUMANIZER_MODEL").unwrap_or_else(|| DEFAULT_MODEL.to_string());
    let body = json!({
        "model": model,
        "messages": [{"role": "user", "content": format!("{PROMPT}{input}")}],
        "stream": false,
        "keep_alive": "3m",
        "options": {"temperature": 1.0, "top_p": 0.95, "top_k": 64, "num_ctx": CONTEXT, "num_gpu": 99, "stop": ["<end_of_turn>"]},
    });
    let mut child = util::command("curl")
        .args(["-sS", "--max-time", "300", &format!("{base}/api/chat"), "-d", "@-"])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| e.to_string())?;
    child.stdin.take().ok_or("no stdin")?.write_all(body.to_string().as_bytes()).map_err(|e| e.to_string())?;
    let o = child.wait_with_output().map_err(|e| e.to_string())?;
    if !o.status.success() {
        return Err(format!("Ollama is not answering ({})", String::from_utf8_lossy(&o.stderr).trim()));
    }
    let v: Value = serde_json::from_slice(&o.stdout).map_err(|e| e.to_string())?;
    if let Some(e) = v.get("error").and_then(Value::as_str) {
        return Err(e.to_string());
    }
    v.pointer("/message/content").and_then(Value::as_str).map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).ok_or_else(|| "an empty reply".to_string())
}

fn finish(p: Pass) -> String {
    format!("{}\n\n===== THE SCENE =====\n{}", p.report, p.text)
}

enum Job {
    Running(String),
    Done(String),
}

static JOBS: LazyLock<Mutex<HashMap<String, Job>>> = LazyLock::new(Default::default);

fn set_job(id: &str, j: Job) {
    if let Ok(mut m) = JOBS.lock() {
        m.insert(id.to_string(), j);
    }
}

/// The MCP tool. A scene that outlasts `wait` seconds keeps running here, and `job` collects it;
/// shortcut: jobs live in this process's memory, so a restart loses a running pass and the draft stands.
pub fn humanize(markdown: &str, job: &str, tries: i64, wait: i64) -> Result<String, String> {
    if !job.is_empty() {
        let mut m = JOBS.lock().map_err(|e| e.to_string())?;
        return match m.get(job) {
            Some(Job::Running(at)) => Ok(format!("Still running: {at}. Call humanize again with job={job}.")),
            Some(Job::Done(_)) => match m.remove(job) {
                Some(Job::Done(out)) => Ok(out),
                _ => Err("job vanished".into()),
            },
            None => Err(format!("no job {job}: it was collected already or the server restarted. The draft stands, or run the pass again.")),
        };
    }
    if markdown.trim().is_empty() {
        return Err("give markdown (the draft) or job".into());
    }
    let id = format!("h{}", std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map(|d| d.as_millis()).unwrap_or(0));
    let (text, tries, thread_id) = (markdown.to_string(), tries.clamp(1, 6) as usize, id.clone());
    set_job(&id, Job::Running("starting".into()));
    let (tx, rx) = mpsc::channel();
    std::thread::spawn(move || {
        let at = |n: usize, of: usize| set_job(&thread_id, Job::Running(format!("{n} of {of} chunks done")));
        let out = finish(run(&text, tries, &ollama, &at));
        set_job(&thread_id, Job::Done(out));
        let _ = tx.send(());
    });
    if rx.recv_timeout(Duration::from_secs(wait.clamp(0, 900) as u64)).is_ok() {
        return humanize("", &id, 0, 0);
    }
    Ok(format!("The pass is still running. Call humanize with job={id} to collect it; a scene takes a few minutes."))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn pass(text: &str, model: Generate) -> Pass {
        run(text, 2, model, &|_, _| {})
    }

    const LONG: &str = "The blade came down from the high line, and Naiser Yukari stepped inside it with his left foot driving hard against the wet stone of the ridge.";
    const REWORD: &str = "Down from the high line came the blade, while Naiser Yukari moved under it, left foot driving hard off wet stone along that ridge's crown.";

    #[test]
    fn a_clean_rewrite_stands() {
        let p = pass(LONG, &|_| Ok(REWORD.into()));
        assert!(p.text.contains("while Naiser Yukari moved"), "{}", p.report);
        assert!(p.report.contains("1 of 1"));
    }

    #[test]
    fn windows_headers_and_notes_never_reach_the_model() {
        let draft = format!("---\ntitle: x\n---\n## I · The Ridge\n\n*The ridge, evening*\n\n{LONG}\n\n[Reserve: 41% ▓▓▓▓░░░░░░]\n\n*KRRAK.*\n\n## Author notes\n\nSources: none.\n");
        let seen = Mutex::new(String::new());
        let p = pass(&draft, &|i| {
            seen.lock().unwrap().push_str(i);
            Ok(REWORD.into())
        });
        let seen = seen.into_inner().unwrap();
        for private in ["Reserve", "KRRAK", "Sources", "title", "The ridge, evening", "The Ridge"] {
            assert!(!seen.contains(private), "{private} reached the model");
            assert!(p.text.contains(private), "{private} lost");
        }
        assert!(p.text.contains("while Naiser Yukari moved"));
        assert!(p.text.starts_with("---\ntitle: x\n---\n## I"));
    }

    #[test]
    fn damage_keeps_the_draft() {
        let cases: &[(&str, &str, &str)] = &[
            ("A long enough line where Sodoku said \"hold the gate\" and he meant every word of it, plainly.", "A long enough line where someone said something like hold your gate and he meant every word of it, plainly.", "dialogue"),
            ("The blade rang, *chiki*, and the collar left the mouth of the scabbard without any hurry at all.", "The blade rang out small and dry and the collar left the mouth of the scabbard without any hurry at all.", "italics"),
            ("He had counted forty-one men and 12 horses along the river road before the bell rang that night.", "He had counted some men and a few horses along that river road before the bell rang that night, again.", "number"),
            ("They walked past Kage no Keifu and the long hill above the water, talking about nothing much.", "They walked past the shadow school and the long hill above the water, talking about nothing much.", "lost name"),
            ("They walked past the long hill above the water, talking about nothing much at all that evening.", "They walked past Halvard Rook and the long hill above that water, talking about nothing much that evening.", "invented"),
            ("They walked past the long hill above the water, talking about nothing much at all that evening.", "They walked past the hill.", "too short"),
        ];
        for (old, bad, reason) in cases {
            let p = pass(old, &|_| Ok(bad.to_string()));
            assert!(p.text.contains(old), "{reason}: {}", p.text);
            assert!(p.report.contains(reason), "{reason}: {}", p.report);
        }
    }

    #[test]
    fn a_near_copy_is_not_a_rewrite() {
        let p = pass(LONG, &|_| Ok(LONG.replace("wet stone", "wet stones")));
        assert!(p.text.contains(LONG));
        assert!(p.report.contains("near copy"));
    }

    #[test]
    fn short_beats_and_mostly_spoken_paragraphs_stay() {
        let draft = format!("{LONG}\n\nThere was one left.\n\n\"Get off my bridge,\" she said, \"or I will put you in the river myself.\"");
        let seen = Mutex::new(0);
        let p = pass(&draft, &|i| {
            *seen.lock().unwrap() += 1;
            assert!(!i.contains("my bridge"));
            Ok(format!("{REWORD}\n\nOne was left, anyway."))
        });
        assert!(p.text.contains("There was one left."));
        assert!(!p.text.contains("One was left"));
        assert!(p.text.contains(REWORD));
    }

    #[test]
    fn a_dead_model_hands_back_the_draft() {
        let draft = format!("{LONG}\n\n{LONG}");
        let p = pass(&draft, &|_| Err("Ollama is not answering".into()));
        assert_eq!(p.text.trim(), draft);
        assert!(p.report.contains("not answering"));
    }

    #[test]
    fn misaligned_paragraphs_are_rejected_then_retried() {
        let tries = Mutex::new(0);
        let draft = format!("{LONG}\n\nThey walked past the long hill above the water, talking about nothing much at all that evening.");
        let p = pass(&draft, &|_| {
            let mut t = tries.lock().unwrap();
            *t += 1;
            Ok(if *t == 1 { REWORD.to_string() } else { format!("{REWORD}\n\nThey went by that long hill over the water, talking of nothing much at all, that whole evening.") })
        });
        assert!(p.report.contains("2 of 2"), "{}", p.report);
    }

    #[test]
    fn long_scenes_are_cut_at_paragraphs() {
        let para = "word ".repeat(200);
        let paras: Vec<(String, Kind)> = (0..5).map(|_| (para.trim().to_string(), Kind::Prose)).collect();
        let c = chunks(&paras);
        assert_eq!(c, vec![vec![0, 1], vec![2, 3], vec![4]]);
    }
}
