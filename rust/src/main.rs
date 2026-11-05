//! WOTR MCP in Rust. The tools listed in NATIVE run here; every other tool in rust/tools.json is
//! answered by one long-lived Python worker (build/mcp_worker.py) until it is ported.
//!
//!   wotr-mcp [--ops] [--read-only]        stdio MCP (what .mcp.json launches); same surfaces as
//!                                         mcp_server.py: core by default, --ops (or WOTR_MCP_OPS=1)
//!                                         for every tool, --read-only narrows either
//!   wotr-mcp call TOOL '{"arg": ...}' [--public BASE TOKEN]
//!                                         run one tool and print its text (parity tests)
//!   wotr-mcp verify FILE [--combat] ...   build/verify.py's command line
//!   wotr-mcp audio [--scene X] ...        build/audio_export.py's command line (audio.rs); audio-probe
//!                                         is rust/audio_parity.py's view of the engines
//!   wotr-mcp http [--port N]... [--dash N] [--log FILE]
//!                                         the public route (default ports 8765 and 8767, the Funnel's
//!                                         / and /ro) gated by the named keys, and the key dashboard on
//!                                         127.0.0.1 (default 8790); see http.rs
//!   wotr-mcp validate | resolve          the rule index gate and out/ (gate.rs)
//!   wotr-mcp backup | nightly | book-next | hook | tool NAME ...
//!                                         the machine's own jobs (ops.rs)
//!   wotr-mcp workshop [--port N] | workshop invite [note]
//!                                         the players' library and Natalie on their own AI
//!   wotr-mcp index [-q]                   build/embed_index.py's build(): build/index/ (index.rs)
//!   wotr-mcp sync                         build/sync.sh: the 15-minute wiki autosave (sync.rs)
//!   wotr-mcp dump                         regenerate rust/tools.json from the Python server
mod analysis;
mod audio;
mod bot;
#[path = "../site/src/rng.rs"]
mod rng;
#[path = "../site/src/text.rs"]
mod text;
mod gate;
mod ops;
mod codex;
mod embed;
mod http;
mod index;
mod jobs;
mod keys;
mod kokoro;
mod pages;
mod pyjson;
mod pyyaml;
mod rules;
mod search;
mod supertonic;
mod sync;
mod table;
mod util;
mod writers;
mod verify;
mod workshop;

use rmcp::model::*;
use rmcp::service::RequestContext;
use rmcp::{ErrorData as McpError, RoleServer, ServerHandler, ServiceExt};
use serde::Deserialize;
use serde_json::{Map, Value};
use std::sync::Arc;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::process::{Child, ChildStdin, ChildStdout, Command};
use tokio::sync::Mutex;
use util::root;

const NATIVE: &[&str] = &[
    "load_rules", "rule", "check_docket", "list_conflicts", "natalie", "natalie_gpt", "skill",
    "character", "fow_line", "verify_scene", "wiki", "scene_recall", "scene_context",
    "fronts", "due", "roster", "scene_menu", "session_start",
    "archive_scene", "wiki_write", "log_ruling", "sync_now", "propose_rule", "handoff", "inbox", "inbox_done",
    "create_character", "update_character", "advance_front", "set_front_clock", "add_front", "pass_time",
    "ledger_add", "ledger_mark", "fire_trigger", "ledger_collect", "npc_set", "session_end",
    "codex", "codex_check", "stale_names", "scene_brief", "gap_fill", "trello_cards", "scene_text", "timeline", "reconcile", "pack_impact",
    "cast_index", "convert_character", "cast_scene", "narrate_scene", "narration_status", "research", "lookup",
    "ask_chatgpt", "ask_claude", "research_chatgpt", "chatgpt_image",
];

#[derive(Deserialize, Clone)]
struct ToolSpec {
    name: String,
    description: String,
    #[serde(rename = "inputSchema")]
    input_schema: Map<String, Value>,
}

#[derive(Deserialize)]
struct Spec {
    instructions: String,
    tools: Vec<ToolSpec>,
    core: Vec<String>,
    read_only: Vec<String>,
    skill_hide: Vec<String>,
    ops_skills: Vec<String>,
    skill_note: String,
}

fn load_spec() -> Spec {
    let p = root("rust/tools.json");
    serde_json::from_str(&util::read_lossy(&p)).unwrap_or_else(|e| panic!("{}: {e} (run `wotr-mcp dump`)", p.display()))
}

// ---------------------------------------------------------------- the Python worker
type Pipe = (Child, ChildStdin, BufReader<ChildStdout>);

#[derive(Default)]
struct Worker(Mutex<Option<Pipe>>);

impl Worker {
    fn spawn() -> std::io::Result<Pipe> {
        let mut c = Command::new("bash")
            .args(["build/py.sh", "build/mcp_worker.py"])
            .current_dir(&*util::ROOT)
            .stdin(std::process::Stdio::piped())
            .stdout(std::process::Stdio::piped())
            .kill_on_drop(true)
            .spawn()?;
        let (i, o) = (c.stdin.take().unwrap(), BufReader::new(c.stdout.take().unwrap()));
        Ok((c, i, o))
    }

    /// Start the worker now so its ~0.5 s import overlaps the client's own startup.
    async fn warm(&self) {
        let mut slot = self.0.lock().await;
        if slot.is_none() {
            *slot = Self::spawn().ok();
        }
    }

    /// One call; a dead worker is respawned once.
    async fn call(&self, tool: &str, args: &Map<String, Value>, public: Option<&(String, String)>) -> Result<String, String> {
        let public = public.map(|(b, t)| serde_json::json!({"base": b, "token": t}));
        let line = serde_json::json!({"tool": tool, "args": args, "public": public}).to_string() + "\n";
        let mut slot = self.0.lock().await;
        for _ in 0..2 {
            if slot.is_none() {
                *slot = Some(Self::spawn().map_err(|e| format!("python worker: {e}"))?);
            }
            let (_, stdin, stdout) = slot.as_mut().unwrap();
            let mut resp = String::new();
            let ok = stdin.write_all(line.as_bytes()).await.is_ok() && stdout.read_line(&mut resp).await.map(|n| n > 0).unwrap_or(false);
            if !ok {
                *slot = None;
                continue;
            }
            let v: Value = serde_json::from_str(&resp).map_err(|e| format!("python worker: bad reply: {e}"))?;
            return match (v.get("ok").and_then(Value::as_str), v.get("err").and_then(Value::as_str)) {
                (Some(t), _) => Ok(t.to_string()),
                (_, Some(e)) => Err(e.to_string()),
                _ => Err("python worker: empty reply".into()),
            };
        }
        Err("python worker died twice".into())
    }
}

// ---------------------------------------------------------------- native dispatch
fn arg_str(a: &Map<String, Value>, k: &str, def: &str) -> String {
    a.get(k).and_then(Value::as_str).unwrap_or(def).to_string()
}
fn arg_req(a: &Map<String, Value>, k: &str) -> Result<String, String> {
    a.get(k).and_then(Value::as_str).map(String::from).ok_or_else(|| format!("missing argument '{k}'"))
}
fn arg_bool(a: &Map<String, Value>, k: &str) -> bool {
    a.get(k).and_then(Value::as_bool).unwrap_or(false)
}
fn arg_int(a: &Map<String, Value>, k: &str, def: i64) -> i64 {
    a.get(k).and_then(Value::as_i64).unwrap_or(def)
}
fn arg_list(a: &Map<String, Value>, k: &str) -> Option<Vec<String>> {
    a.get(k)?.as_array().map(|v| v.iter().filter_map(|x| x.as_str().map(String::from)).collect())
}

/// An exception the Python tool would not have caught, as the MCP error text names it.
fn py_err(r: Result<String, writers::E>) -> Result<String, String> {
    r.map_err(|e| match e {
        writers::E::Key(k) => format!("KeyError: '{k}'"),
        writers::E::Value(m) => format!("ValueError: {m}"),
    })
}

fn native(tool: &str, a: &Map<String, Value>, hide: &[String], note: &str, public: Option<&(String, String)>) -> Result<String, String> {
    Ok(match tool {
        "load_rules" => {
            let tags = arg_list(a, "tags").ok_or("missing argument 'tags'")?;
            rules::load_rules(&tags, arg_list(a, "status"), arg_bool(a, "brief"), a.get("part").and_then(Value::as_i64).unwrap_or(0))?
        }
        "rule" => rules::rule(&arg_req(a, "id")?)?,
        "check_docket" => rules::check_docket(&arg_list(a, "tags").ok_or("missing argument 'tags'")?)?,
        "list_conflicts" => pages::list_conflicts(),
        "natalie" => pages::natalie(&arg_str(a, "section", "")),
        "natalie_gpt" => pages::natalie_gpt(),
        "skill" => pages::skill(&arg_str(a, "name", ""), &arg_str(a, "file", ""), hide, note),
        "character" => pages::character(&arg_req(a, "name")?),
        "fow_line" => pages::fow_line(&arg_req(a, "name")?),
        "wiki" => search::wiki(&arg_req(a, "query")?, a.get("full").and_then(Value::as_bool).unwrap_or(true), arg_int(a, "limit", 6)),
        "scene_recall" => search::scene_recall(&arg_req(a, "query")?, arg_int(a, "limit", 8), arg_bool(a, "old_lore")),
        "scene_context" => search::scene_context(&arg_req(a, "draft")?, arg_int(a, "budget", 24000)),
        "fronts" => table::fronts(&arg_str(a, "thread", ""), arg_bool(a, "include_closed"))?,
        "due" => table::due(arg_int(a, "sessions_old", 2), &arg_str(a, "thread", ""), &arg_str(a, "today", ""))?,
        "roster" => table::roster(&arg_str(a, "thread", ""), arg_bool(a, "public"))?,
        "scene_menu" => table::scene_menu(&arg_req(a, "thread")?, &arg_str(a, "culture", "Kharven"))?,
        "session_start" => table::session_start(&arg_req(a, "thread")?, &arg_str(a, "culture", "Kharven")),
        "archive_scene" => writers::archive_scene(&arg_req(a, "title")?, &arg_req(a, "markdown")?, &arg_str(a, "author_notes", "")),
        "wiki_write" => writers::wiki_write(&arg_req(a, "path")?, &arg_req(a, "markdown")?, &arg_str(a, "message", "")),
        "log_ruling" => writers::log_ruling(&arg_req(a, "rule_id")?, &arg_req(a, "ruling")?, &arg_str(a, "context", "")),
        "sync_now" => writers::sync_now(),
        "propose_rule" => writers::propose_rule(&arg_req(a, "title")?, &arg_req(a, "rule_text")?, &arg_list(a, "applies_to").ok_or("missing argument 'applies_to'")?,
                                                &arg_str(a, "rationale", ""), &arg_str(a, "session", "")),
        "handoff" => writers::handoff(&arg_req(a, "kind")?, &arg_req(a, "title")?, &arg_req(a, "body")?, &arg_str(a, "thread", "")),
        "inbox" => writers::inbox(a.get("full").and_then(Value::as_bool).unwrap_or(true)),
        "inbox_done" => writers::inbox_done(&arg_req(a, "name")?, &arg_req(a, "outcome")?),
        "create_character" => writers::create_character(&arg_req(a, "name")?, &arg_req(a, "markdown")?, &arg_str(a, "volume", "Volume I \u{2014} Character Cards"), arg_list(a, "tags")),
        "update_character" => writers::update_character(&arg_req(a, "name")?, &arg_req(a, "markdown")?),
        "advance_front" => py_err(writers::advance_front(&arg_req(a, "front_id")?, &arg_req(a, "what_happened")?, &arg_str(a, "next_move", "")))?,
        "set_front_clock" => py_err(writers::set_front_clock(&arg_req(a, "front_id")?, arg_list(a, "ticks"), a.get("pace_days").and_then(Value::as_i64)))?,
        "add_front" => py_err(writers::add_front(&arg_req(a, "name")?, &arg_req(a, "thread")?, &arg_req(a, "want")?, arg_list(a, "ticks").ok_or("missing argument 'ticks'")?,
                                                 &arg_str(a, "next_move", ""), a.get("pace_days").and_then(Value::as_i64)))?,
        "pass_time" => py_err(writers::pass_time(&arg_req(a, "thread")?, arg_int(a, "days", 0), &arg_str(a, "story_date", "")))?,
        "ledger_add" => py_err(writers::ledger_add(&arg_req(a, "category")?, &arg_req(a, "who")?, &arg_req(a, "text")?, a.get("due_after_sessions").cloned().unwrap_or(Value::Null),
                                                   &arg_str(a, "due_condition", ""), &arg_str(a, "thread", ""), &arg_str(a, "due_date", ""), &arg_str(a, "due_trigger", ""),
                                                   a.get("ticks").and_then(Value::as_i64), &arg_str(a, "level", "")))?,
        "ledger_mark" => py_err(writers::ledger_mark(&arg_req(a, "entry_id")?, &arg_str(a, "fed", ""), &arg_str(a, "strained", ""), &arg_str(a, "level", ""),
                                                     arg_int(a, "tick", 0), &arg_str(a, "how", "")))?,
        "fire_trigger" => py_err(writers::fire_trigger(&arg_req(a, "trigger")?, &arg_str(a, "thread", "")))?,
        "ledger_collect" => py_err(writers::ledger_collect(&arg_req(a, "entry_id")?, &arg_req(a, "how")?))?,
        "npc_set" => py_err(writers::npc_set(&arg_req(a, "name")?, &arg_req(a, "thread")?, writers::npc_fields(a)))?,
        "session_end" => {
            let objs = |k: &str| a.get(k).and_then(Value::as_array).cloned().unwrap_or_default();
            py_err(writers::session_end(&arg_req(a, "thread")?, &arg_str(a, "scene_markdown", ""), &arg_str(a, "title", ""), &arg_str(a, "author_notes", ""),
                                        arg_list(a, "rulings").unwrap_or_default(), &arg_str(a, "notes", ""), objs("ledger"), objs("fronts"), objs("npcs"), objs("cards"),
                                        arg_list(a, "fired").unwrap_or_default(), arg_int(a, "days", 0), &arg_str(a, "story_date", "")))?
        }
        "codex" => codex::find(&arg_req(a, "query")?, &arg_str(a, "sheet", ""), arg_int(a, "limit", 8))?,
        "codex_check" => codex::check(&arg_req(a, "markdown")?)?,
        "stale_names" => analysis::stale_names(&arg_str(a, "scope", "all"), arg_int(a, "max_files", 60)),
        "scene_brief" => analysis::scene_brief(&arg_req(a, "beat")?, &arg_str(a, "thread", ""), &arg_str(a, "scene_type", "standard"), &arg_list(a, "characters").unwrap_or_default())?,
        "gap_fill" => analysis::gap_fill(&arg_req(a, "markdown")?)?,
        "trello_cards" => analysis::trello_cards(&arg_req(a, "json_path")?, &arg_str(a, "list_name", ""), &arg_str(a, "query", ""))?,
        "scene_text" => analysis::scene_text(&arg_req(a, "scene")?),
        "timeline" => analysis::timeline()?,
        "reconcile" => analysis::reconcile()?,
        "pack_impact" => analysis::pack_impact(&arg_req(a, "markdown")?, &arg_str(a, "name", "new_pack"))?,
        "cast_index" => analysis::cast_index(a.get("write").and_then(Value::as_bool).unwrap_or(true)),
        "convert_character" => analysis::convert_character(&arg_req(a, "source")?, &arg_str(a, "name", ""), &arg_str(a, "json_path", ""),
                                                           &arg_str(a, "target_volume", "Volume I \u{2014} Character Cards"))?,
        "cast_scene" => jobs::cast_scene(&arg_req(a, "scene")?, &arg_req(a, "script")?)?,
        "narrate_scene" => jobs::narrate_scene(&arg_req(a, "scene")?, &arg_str(a, "voice", "narrator"), &arg_str(a, "engine", "local"), public)?,
        "narration_status" => jobs::narration_status(&arg_str(a, "job", ""), public)?,
        "research" => jobs::research(&arg_req(a, "question")?, arg_int(a, "read", 2), &arg_list(a, "urls").unwrap_or_default(), &arg_str(a, "power", ""))?,
        "lookup" => jobs::lookup(&arg_req(a, "source")?, &arg_req(a, "query")?),
        "ask_chatgpt" => jobs::ask_chatgpt(&arg_req(a, "prompt")?),
        "ask_claude" => jobs::ask_claude(&arg_req(a, "prompt")?),
        "research_chatgpt" => jobs::research_chatgpt(&arg_req(a, "question")?, &arg_str(a, "thread", "")),
        "verify_scene" => {
            let (culture, school) = (arg_str(a, "culture", ""), arg_str(a, "school", ""));
            let o = verify::Opts {
                combat: arg_bool(a, "combat"),
                culture: Some(culture.as_str()).filter(|s| !s.is_empty()),
                school: Some(school.as_str()).filter(|s| !s.is_empty()),
                turn: arg_bool(a, "turn"),
                explicit: arg_bool(a, "explicit"),
            };
            verify::report(&verify::run(&arg_req(a, "markdown")?, &o)?)
        }
        _ => return Err(format!("unknown tool {tool}")),
    })
}

// ---------------------------------------------------------------- the MCP server
/// Who a session serves: a fixed surface (stdio, the flags), or a dashboard key whose
/// permissions are read on every request, so an edit or a disable applies at once.
#[derive(Clone)]
enum Access {
    Fixed { ops: bool, read_only: bool, public: Option<(String, String)> },
    Key { reg: Arc<keys::Registry>, id: String },
}

struct Surface {
    tools: Vec<ToolSpec>,
    hide: Vec<String>,
    /// (base URL, token) for audio and image links
    public: Option<(String, String)>,
}

#[derive(Clone)]
struct Wotr {
    spec: Arc<Spec>,
    access: Access,
    worker: Arc<Worker>,
}

impl Wotr {
    fn fixed(ops: bool, read_only: bool) -> Self {
        Wotr { spec: Arc::new(load_spec()), access: Access::Fixed { ops, read_only, public: None }, worker: Arc::default() }
    }

    fn surface(&self) -> Surface {
        let s = &self.spec;
        let (ops, ro, custom, public) = match &self.access {
            Access::Fixed { ops, read_only, public } => (*ops, *read_only, None, public.clone()),
            Access::Key { reg, id } => match reg.get(id).filter(|k| k.enabled) {
                None => return Surface { tools: vec![], hide: vec![], public: None },
                Some(k) => {
                    let public = Some((k.base.clone(), k.token.clone()));
                    match k.preset.as_str() {
                        "full" => (true, false, None, public),
                        "core" => (false, false, None, public),
                        "read-only" => (false, true, None, public),
                        _ => (true, false, Some(k.tools), public),
                    }
                }
            },
        };
        let tools: Vec<ToolSpec> = s
            .tools
            .iter()
            .filter(|t| ops || s.core.contains(&t.name))
            .filter(|t| !ro || s.read_only.contains(&t.name))
            .filter(|t| custom.as_ref().is_none_or(|c| c.contains(&t.name)))
            .cloned()
            .collect();
        let mut hide = s.skill_hide.clone();
        // the ops skills drive writing tools; a surface that cannot write does not see them
        if ro || custom.is_some() && tools.iter().all(|t| s.read_only.contains(&t.name)) {
            hide.extend(s.ops_skills.iter().cloned());
        }
        Surface { tools, hide, public }
    }

    async fn call(&self, tool: &str, args: Map<String, Value>) -> Result<Vec<ContentBlock>, String> {
        let sf = self.surface();
        if !sf.tools.iter().any(|t| t.name == tool) {
            return Err(format!("Unknown tool: {tool}"));
        }
        if tool == "chatgpt_image" {
            // [Image, text] in Python: the JPEG preview (or the file) as an image block, then the text
            let run = move || {
                let (image, text) = jobs::chatgpt_image(&arg_req(&args, "prompt")?, &arg_str(&args, "name", ""), sf.public.as_ref())?;
                Ok(image.map(|(data, mime)| ContentBlock::image(data, mime)).into_iter().chain([ContentBlock::text(text)]).collect())
            };
            return tokio::task::spawn_blocking(run).await.map_err(|e| e.to_string())?;
        }
        if NATIVE.contains(&tool) {
            let (tool, note) = (tool.to_string(), self.spec.skill_note.clone());
            let run = move || native(&tool, &args, &sf.hide, &note, sf.public.as_ref()).map(|t| vec![ContentBlock::text(t)]);
            return tokio::task::spawn_blocking(run).await.map_err(|e| e.to_string())?;
        }
        self.worker.call(tool, &args, sf.public.as_ref()).await.map(|t| vec![ContentBlock::text(t)])
    }
}

impl ServerHandler for Wotr {
    fn get_info(&self) -> ServerConfig {
        ServerConfig::new(ServerCapabilities::builder().enable_tools().enable_prompts().build())
            .with_instructions(self.spec.instructions.clone())
            .with_server_info(Implementation::new("WOTR MCP", env!("CARGO_PKG_VERSION")))
    }

    async fn list_tools(&self, _: Option<PaginatedRequestParams>, _: RequestContext<RoleServer>) -> Result<ListToolsResult, McpError> {
        let tools = self.surface().tools.iter().map(|t| Tool::new(t.name.clone(), t.description.clone(), Arc::new(t.input_schema.clone()))).collect();
        Ok(ListToolsResult::with_all_items(tools))
    }

    async fn call_tool(&self, req: CallToolRequestParams, _: RequestContext<RoleServer>) -> Result<CallToolResponse, McpError> {
        let known = self.surface().tools.iter().any(|t| t.name == req.name);
        Ok(match self.call(&req.name, req.arguments.unwrap_or_default()).await {
            Ok(blocks) => CallToolResult::success(blocks),
            Err(e) if !known => CallToolResult::error(vec![ContentBlock::text(e)]),
            Err(e) => CallToolResult::error(vec![ContentBlock::text(format!("Error executing tool {}: {e}", req.name))]),
        }
        .into())
    }

    async fn list_prompts(&self, _: Option<PaginatedRequestParams>, _: RequestContext<RoleServer>) -> Result<ListPromptsResult, McpError> {
        let prompts = pages::skills(&self.surface().hide).into_iter().map(|(n, d, _)| Prompt::new(n, Some(d), None)).collect();
        Ok(ListPromptsResult::with_all_items(prompts))
    }

    async fn get_prompt(&self, req: GetPromptRequestParams, _: RequestContext<RoleServer>) -> Result<GetPromptResponse, McpError> {
        let skills = pages::skills(&self.surface().hide);
        let (_, d, body) = skills.into_iter().find(|(n, _, _)| *n == req.name).ok_or_else(|| McpError::invalid_params(format!("Unknown prompt: {}", req.name), None))?;
        let mut r = GetPromptResult::new(vec![PromptMessage::new_text(Role::User, format!("{}{body}", self.spec.skill_note))]);
        r.description = Some(d);
        Ok(r.into())
    }
}

/// First-use costs moved off the request path: verify's ~120 regexes, the embedding model and the
/// search index (~60 MB), and the lorebook's alias registry.
fn warm() {
    let _ = verify::run("warm", &verify::Opts { combat: true, explicit: true, ..Default::default() });
    let _ = search::scene_context("warm", 1000);
}

// ---------------------------------------------------------------- command line
fn verify_cli(args: &[String]) -> i32 {
    let flag = |f: &str| args.iter().any(|a| a == f);
    let opt = |f: &str| args.iter().position(|a| a == f).and_then(|i| args.get(i + 1)).map(String::as_str);
    let Some(file) = args.iter().find(|a| !a.starts_with("--") && !["--school", "--culture", "--band"].iter().any(|f| opt(f) == Some(a.as_str()))) else {
        eprintln!("usage: wotr-mcp verify FILE [--combat] [--school S] [--culture C] [--band B] [--echoes] [--turn] [--explicit]");
        return 2;
    };
    let text = util::read_lossy(std::path::Path::new(file));
    let o = verify::Opts { combat: flag("--combat"), culture: opt("--culture"), school: opt("--school"), turn: flag("--turn"), explicit: flag("--explicit") };
    match verify::run(&text, &o) {
        Ok(mut r) => {
            if flag("--echoes") {
                r.warns.extend(verify::echoes(&text));
            }
            println!("{}", verify::report(&r));
            i32::from(!r.fails.is_empty())
        }
        Err(e) => {
            eprintln!("{e}");
            2
        }
    }
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match args.first().map(String::as_str) {
        Some("verify") => std::process::exit(verify_cli(&args[1..])),
        Some("audio") => std::process::exit(audio::main(&args[1..])),
        Some("index") => std::process::exit(index::main(&args[1..])),
        Some("sync") => std::process::exit(sync::main()),
        Some("audio-probe") => std::process::exit(audio::probe()),
        Some("bot") if args.get(1).map(String::as_str) == Some("preview") => std::process::exit(bot::preview()),
        Some("bot") => std::process::exit(bot::run::main(&args[1..]).await),
        Some("workshop") => std::process::exit(workshop::main(&args[1..]).await),
        Some("validate") => {
            let (code, out) = gate::validate();
            println!("{out}");
            std::process::exit(code);
        }
        Some("resolve") => match gate::resolve() {
            Ok(out) => {
                println!("{out}");
                return;
            }
            Err(e) => {
                eprintln!("{e}");
                std::process::exit(1)
            }
        },
        Some("backup") => std::process::exit(ops::backup()),
        Some("book-next") => std::process::exit(ops::book_next(&args[1..])),
        Some("nightly") => std::process::exit(ops::nightly(&args[1..])),
        Some("hook") => std::process::exit(ops::hook()),
        Some("tool") => {
            let (tool, a) = match ops::tool_args(&args[1..]) {
                Ok(Some(call)) => call,
                Ok(None) => {
                    println!("{}", ops::loadout(&args[1..]));
                    return;
                }
                Err(e) => {
                    eprintln!("{e}");
                    std::process::exit(1)
                }
            };
            let r = Wotr::fixed(true, false).call(&tool, a).await;
            jobs::join_background();
            match r {
                Ok(b) => match b.as_slice() {
                    [ContentBlock::Text(t)] => println!("{}", t.text),
                    _ => println!("{}", serde_json::to_string(&b).unwrap()),
                },
                Err(e) => {
                    eprintln!("{e}");
                    std::process::exit(1)
                }
            }
            return;
        }
        Some("dump") => {
            let s = std::process::Command::new("bash").args(["build/py.sh", "build/mcp_worker.py", "--dump"]).current_dir(&*util::ROOT).status();
            std::process::exit(s.map(|s| s.code().unwrap_or(1)).unwrap_or(1));
        }
        Some("embed") => {
            // the query vector as JSON, for checking it against fastembed's
            match embed::embed(args.get(1).map(String::as_str).unwrap_or("")) {
                Ok(v) => println!("{}", serde_json::to_string(&v).unwrap()),
                Err(e) => {
                    eprintln!("{e}");
                    std::process::exit(1)
                }
            }
            return;
        }
        Some("yaml-dump") => {
            // JSON on stdin -> safe_dump's YAML, for rust/yaml_parity.py
            let v: Value = serde_json::from_str(&std::io::read_to_string(std::io::stdin()).expect("stdin")).expect("JSON");
            print!("{}", pyyaml::dump(&v));
            return;
        }
        Some("yaml-load") => {
            // YAML on stdin -> JSON, as table.rs reads it, for rust/yaml_parity.py
            let v = table::parse_yaml(&std::io::read_to_string(std::io::stdin()).expect("stdin")).unwrap_or_else(|e| panic!("{e}"));
            print!("{}", serde_json::to_string(&v).unwrap());
            return;
        }
        Some("call") => {
            let tool = args.get(1).cloned().unwrap_or_default();
            let json = match args.get(2).map(String::as_str) {
                Some("-") => std::io::read_to_string(std::io::stdin()).expect("stdin"), // an argv string caps at 128 KiB
                Some(j) => j.to_string(),
                None => "{}".into(),
            };
            let a: Map<String, Value> = serde_json::from_str(&json).expect("args must be a JSON object");
            let mut server = Wotr::fixed(true, false);
            // --public BASE TOKEN: answer as a dashboard key with that base URL and token would be answered
            if let Some(i) = args.iter().position(|x| x == "--public") {
                let public = Some((args.get(i + 1).cloned().unwrap_or_default(), args.get(i + 2).cloned().unwrap_or_default()));
                server.access = Access::Fixed { ops: true, read_only: false, public };
            }
            let r = server.call(&tool, a).await;
            jobs::join_background();
            match r {
                // one text block prints as its text; anything else as the JSON content list
                Ok(b) => match b.as_slice() {
                    [ContentBlock::Text(t)] => println!("{}", t.text),
                    _ => println!("{}", serde_json::to_string(&b).unwrap()),
                },
                Err(e) => {
                    eprintln!("{e}");
                    std::process::exit(1)
                }
            }
            return;
        }
        _ => {}
    }
    let flag = |f: &str| args.iter().any(|a| a == f);
    let values = |f: &str| args.windows(2).filter(|w| w[0] == f).map(|w| w[1].clone()).collect::<Vec<_>>();
    if args.first().map(String::as_str) == Some("http") {
        let ports: Vec<u16> = values("--port").iter().filter_map(|p| p.parse().ok()).collect();
        let ports = if ports.is_empty() { vec![8765, 8767] } else { ports };
        let dash = values("--dash").first().and_then(|p| p.parse().ok()).unwrap_or(8790);
        let template = Wotr::fixed(true, false);
        std::thread::spawn(warm);
        // the Python worker is only for a tool not yet ported; start it only if there is one
        if template.spec.tools.iter().any(|t| !NATIVE.contains(&t.name.as_str())) {
            let w = template.worker.clone();
            tokio::spawn(async move { w.warm().await });
        }
        http::serve(template, ports, dash, values("--log").first().cloned()).await;
        return;
    }
    let ops = flag("--ops") || matches!(std::env::var("WOTR_MCP_OPS").unwrap_or_default().trim(), "1" | "true" | "yes");
    let server = Wotr::fixed(ops, flag("--read-only"));
    // warm-ups, off the request path: verify's ~120 regexes compile on first use, and the Python
    // worker imports mcp_server once; both would otherwise land on the first call that needs them
    std::thread::spawn(warm);
    let tools = server.surface().tools;
    if tools.iter().any(|t| !NATIVE.contains(&t.name.as_str())) {
        let w = server.worker.clone();
        tokio::spawn(async move { w.warm().await });
    }
    eprintln!("wotr-mcp: {} tools ({} native), stdio", tools.len(), tools.iter().filter(|t| NATIVE.contains(&t.name.as_str())).count());
    let service = server.serve(rmcp::transport::stdio()).await.expect("stdio serve");
    let _ = service.waiting().await;
}
