//! WOTR MCP in Rust. The tools listed in NATIVE run here; every other tool in rust/tools.json is
//! answered by one long-lived Python worker (build/mcp_worker.py) until it is ported.
//!
//!   wotr-mcp [--ops] [--read-only]        stdio MCP (what .mcp.json launches); same surfaces as
//!                                         mcp_server.py: core by default, --ops (or WOTR_MCP_OPS=1)
//!                                         for every tool, --read-only narrows either
//!   wotr-mcp call TOOL '{"arg": ...}'     run one tool and print its text (parity tests)
//!   wotr-mcp verify FILE [--combat] ...   build/verify.py's command line
//!   wotr-mcp dump                         regenerate rust/tools.json from the Python server
mod pages;
mod rules;
mod util;
mod verify;

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
    "character", "fow_line", "verify_scene",
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
    async fn call(&self, tool: &str, args: &Map<String, Value>) -> Result<String, String> {
        let line = serde_json::json!({"tool": tool, "args": args}).to_string() + "\n";
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
fn arg_list(a: &Map<String, Value>, k: &str) -> Option<Vec<String>> {
    a.get(k)?.as_array().map(|v| v.iter().filter_map(|x| x.as_str().map(String::from)).collect())
}

fn native(tool: &str, a: &Map<String, Value>, hide: &[String], note: &str) -> Result<String, String> {
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
struct Wotr {
    spec: Spec,
    tools: Vec<ToolSpec>,
    hide: Vec<String>,
    worker: Arc<Worker>,
}

impl Wotr {
    fn new(ops: bool, read_only: bool) -> Self {
        let spec = load_spec();
        let tools = spec
            .tools
            .iter()
            .filter(|t| ops || spec.core.contains(&t.name))
            .filter(|t| !read_only || spec.read_only.contains(&t.name))
            .cloned()
            .collect();
        let mut hide = spec.skill_hide.clone();
        if read_only {
            hide.extend(spec.ops_skills.iter().cloned());
        }
        Wotr { spec, tools, hide, worker: Arc::default() }
    }

    async fn call(&self, tool: &str, args: Map<String, Value>) -> Result<String, String> {
        if !self.tools.iter().any(|t| t.name == tool) {
            return Err(format!("Unknown tool: {tool}"));
        }
        if NATIVE.contains(&tool) {
            let (tool, hide, note) = (tool.to_string(), self.hide.clone(), self.spec.skill_note.clone());
            return tokio::task::spawn_blocking(move || native(&tool, &args, &hide, &note)).await.map_err(|e| e.to_string())?;
        }
        self.worker.call(tool, &args).await
    }
}

impl ServerHandler for Wotr {
    fn get_info(&self) -> ServerConfig {
        ServerConfig::new(ServerCapabilities::builder().enable_tools().enable_prompts().build())
            .with_instructions(self.spec.instructions.clone())
            .with_server_info(Implementation::new("WOTR MCP", env!("CARGO_PKG_VERSION")))
    }

    async fn list_tools(&self, _: Option<PaginatedRequestParams>, _: RequestContext<RoleServer>) -> Result<ListToolsResult, McpError> {
        let tools = self.tools.iter().map(|t| Tool::new(t.name.clone(), t.description.clone(), Arc::new(t.input_schema.clone()))).collect();
        Ok(ListToolsResult::with_all_items(tools))
    }

    async fn call_tool(&self, req: CallToolRequestParams, _: RequestContext<RoleServer>) -> Result<CallToolResponse, McpError> {
        let known = self.tools.iter().any(|t| t.name == req.name);
        Ok(match self.call(&req.name, req.arguments.unwrap_or_default()).await {
            Ok(text) => CallToolResult::success(vec![ContentBlock::text(text)]),
            Err(e) if !known => CallToolResult::error(vec![ContentBlock::text(e)]),
            Err(e) => CallToolResult::error(vec![ContentBlock::text(format!("Error executing tool {}: {e}", req.name))]),
        }
        .into())
    }

    async fn list_prompts(&self, _: Option<PaginatedRequestParams>, _: RequestContext<RoleServer>) -> Result<ListPromptsResult, McpError> {
        let prompts = pages::skills(&self.hide).into_iter().map(|(n, d, _)| Prompt::new(n, Some(d), None)).collect();
        Ok(ListPromptsResult::with_all_items(prompts))
    }

    async fn get_prompt(&self, req: GetPromptRequestParams, _: RequestContext<RoleServer>) -> Result<GetPromptResponse, McpError> {
        let skills = pages::skills(&self.hide);
        let (_, d, body) = skills.into_iter().find(|(n, _, _)| *n == req.name).ok_or_else(|| McpError::invalid_params(format!("Unknown prompt: {}", req.name), None))?;
        let mut r = GetPromptResult::new(vec![PromptMessage::new_text(Role::User, format!("{}{body}", self.spec.skill_note))]);
        r.description = Some(d);
        Ok(r.into())
    }
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
        Some("dump") => {
            let s = std::process::Command::new("bash").args(["build/py.sh", "build/mcp_worker.py", "--dump"]).current_dir(&*util::ROOT).status();
            std::process::exit(s.map(|s| s.code().unwrap_or(1)).unwrap_or(1));
        }
        Some("call") => {
            let tool = args.get(1).cloned().unwrap_or_default();
            let json = match args.get(2).map(String::as_str) {
                Some("-") => std::io::read_to_string(std::io::stdin()).expect("stdin"), // an argv string caps at 128 KiB
                Some(j) => j.to_string(),
                None => "{}".into(),
            };
            let a: Map<String, Value> = serde_json::from_str(&json).expect("args must be a JSON object");
            match Wotr::new(true, false).call(&tool, a).await {
                Ok(t) => println!("{t}"),
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
    if flag("--http") || flag("--public") {
        eprintln!("--http is phase 2; serve HTTP with build/mcp_server.py until then");
        std::process::exit(2);
    }
    let ops = flag("--ops") || matches!(std::env::var("WOTR_MCP_OPS").unwrap_or_default().trim(), "1" | "true" | "yes");
    let server = Wotr::new(ops, flag("--read-only"));
    // warm-ups, off the request path: verify's ~120 regexes compile on first use, and the Python
    // worker imports mcp_server once; both would otherwise land on the first call that needs them
    std::thread::spawn(|| verify::run("warm", &verify::Opts { combat: true, explicit: true, ..Default::default() }));
    if server.tools.iter().any(|t| !NATIVE.contains(&t.name.as_str())) {
        let w = server.worker.clone();
        tokio::spawn(async move { w.warm().await });
    }
    eprintln!("wotr-mcp: {} tools ({} native), stdio", server.tools.len(), server.tools.iter().filter(|t| NATIVE.contains(&t.name.as_str())).count());
    let service = server.serve(rmcp::transport::stdio()).await.expect("stdio serve");
    let _ = service.waiting().await;
}
