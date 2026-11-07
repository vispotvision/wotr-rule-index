//! `wotr-mcp http`: the public MCP route and the key dashboard, replacing mcp_server.py's
//! --http/--token/--public modes and their two systemd units.
//!
//! The MCP route listens on every --port (8765 and 8767, where Tailscale Funnel points / and /ro)
//! and admits a request only with an enabled key's token: `Authorization: Bearer <token>`, or the
//! path /t/<token>/mcp for connectors that cannot send headers. The key decides the tool surface.
//! /t/<token>/audio/... and /images/... serve rendered narration and saved images, as before.
//! The dashboard listens on 127.0.0.1 only and is never routed through the Funnel.
use crate::keys::{now, random_hex, Key, Registry};
use crate::{Access, Wotr};
use axum::body::Body;
use axum::extract::{ConnectInfo, Path as UrlPath, Request, State};
use axum::http::{header, HeaderMap, Method, StatusCode, Uri};
use axum::response::{Html, IntoResponse, Response};
use axum::routing::{get, post};
use axum::{Json, Router};
use rmcp::transport::streamable_http_server::session::local::LocalSessionManager;
use rmcp::transport::streamable_http_server::session::SessionManager;
use rmcp::transport::streamable_http_server::{StreamableHttpServerConfig, StreamableHttpService};
use serde::Deserialize;
use serde_json::{json, Value};
use std::collections::HashMap;
use std::io::Write;
use std::net::SocketAddr;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};
use tower::ServiceExt;

type Mcp = StreamableHttpService<Wotr, LocalSessionManager>;

pub struct App {
    template: Wotr,
    reg: Arc<Registry>,
    /// one MCP service per key, made on its first request; its session manager counts who is online
    services: Mutex<HashMap<String, (Mcp, Arc<LocalSessionManager>)>>,
    log: Option<Mutex<std::fs::File>>,
    dash_port: u16,
}

impl App {
    fn service(&self, id: &str) -> Mcp {
        let mut map = self.services.lock().unwrap();
        map.entry(id.to_string())
            .or_insert_with(|| {
                let mgr = Arc::new(LocalSessionManager::default());
                let w = Wotr { access: Access::Key { reg: self.reg.clone(), id: id.to_string() }, ..self.template.clone() };
                // the token gate stands in for rmcp's Host check (the Funnel hostname is not loopback),
                // as the Python route did: a page in someone's browser cannot know a token
                let cfg = StreamableHttpServerConfig::default().disable_allowed_hosts();
                (StreamableHttpService::new(move || Ok(w.clone()), mgr.clone(), cfg), mgr)
            })
            .0
            .clone()
    }

    fn manager(&self, id: &str) -> Option<Arc<LocalSessionManager>> {
        self.services.lock().unwrap().get(id).map(|(_, m)| m.clone())
    }

    /// End a key's open sessions (rotate, disable, delete): the next request must re-authenticate.
    async fn drop_sessions(&self, id: &str) {
        let mgr = self.services.lock().unwrap().remove(id).map(|(_, m)| m);
        if let Some(m) = mgr {
            let ids: Vec<_> = m.sessions.read().await.keys().cloned().collect();
            for s in ids {
                let _ = m.close_session(&s).await;
            }
        }
    }

    fn log(&self, line: String) {
        match &self.log {
            Some(f) => {
                let _ = writeln!(f.lock().unwrap(), "{} {line}", iso(now()));
            }
            None => println!("{line}"),
        }
    }
}

/// Seconds since the epoch as an ISO-8601 UTC timestamp (civil-from-days, H. Hinnant).
fn iso(t: u64) -> String {
    let (days, s) = ((t / 86400) as i64, t % 86400);
    let z = days + 719468;
    let era = z.div_euclid(146097);
    let doe = z - era * 146097;
    let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let (d, m) = (doy - (153 * mp + 2) / 5 + 1, if mp < 10 { mp + 3 } else { mp - 9 });
    let y = yoe + era * 400 + i64::from(m <= 2);
    format!("{y:04}-{m:02}-{d:02}T{:02}:{:02}:{:02}Z", s / 3600, s % 3600 / 60, s % 60)
}

fn pct_decode(s: &str) -> String {
    let b = s.as_bytes();
    let mut out = Vec::with_capacity(b.len());
    let mut i = 0;
    while i < b.len() {
        match (b[i], b.get(i + 1..i + 3).and_then(|h| std::str::from_utf8(h).ok()).and_then(|h| u8::from_str_radix(h, 16).ok())) {
            (b'%', Some(x)) => {
                out.push(x);
                i += 3;
            }
            (c, _) => {
                out.push(c);
                i += 1;
            }
        }
    }
    String::from_utf8_lossy(&out).into_owned()
}

fn text(status: StatusCode, body: impl Into<String>) -> Response {
    (status, [(header::CONTENT_TYPE, "text/plain; charset=utf-8")], body.into()).into_response()
}


fn walk(dir: &Path, out: &mut Vec<PathBuf>) {
    for e in std::fs::read_dir(dir).into_iter().flatten().flatten() {
        if e.file_type().is_ok_and(|t| t.is_dir()) {
            walk(&e.path(), out);
        } else {
            out.push(e.path());
        }
    }
}

async fn file(req: Request, target: &Path) -> Response {
    let name = target.file_name().map(|n| n.to_string_lossy().replace('"', "")).unwrap_or_default();
    let mut r = tower_http::services::ServeFile::new(target).oneshot(req).await.map(IntoResponse::into_response).unwrap_or_else(|_| text(StatusCode::NOT_FOUND, "not found\n"));
    if let Ok(v) = format!("inline; filename=\"{name}\"").parse() {
        r.headers_mut().insert(header::CONTENT_DISPOSITION, v);
    }
    r
}

/// /audio/<relative path>: the rendered MP3s, Range-capable for a phone player; /audio/ lists them.
async fn audio(req: Request, tail: &str) -> Response {
    let root = crate::util::audio_dir();
    let rel = pct_decode(tail).replace('\\', "/").trim_matches('/').to_string();
    let real = root.canonicalize().unwrap_or(root.clone());
    if rel.is_empty() {
        let mut all = Vec::new();
        walk(&root, &mut all);
        let rels = |ext: &str| {
            let mut v: Vec<String> = all.iter().filter(|p| p.extension().is_some_and(|x| x == ext)).map(|p| crate::util::rel_posix(p, &root)).collect();
            v.sort();
            v
        };
        let list = [rels("mp3"), rels("wav")].concat();
        let body = if list.is_empty() { "(nothing rendered yet)".to_string() } else { list.join("\n") };
        return text(StatusCode::OK, body + "\n");
    }
    match root.join(&rel).canonicalize() {
        Ok(t) if t.starts_with(&real) && t != real && t.is_file() && t.extension().is_some_and(|x| x.eq_ignore_ascii_case("mp3") || x.eq_ignore_ascii_case("wav")) => file(req, &t).await,
        _ => text(StatusCode::NOT_FOUND, "not found\n"),
    }
}

/// /images/<file>: one image chatgpt_image or comfy saved (a comfy video too); only plain names inside ~/wotr-drafts/images.
async fn image(req: Request, name: &str) -> Response {
    let base = PathBuf::from(std::env::var("HOME").unwrap_or_default()).join("wotr-drafts/images");
    let name = pct_decode(name);
    let Some(n) = Path::new(&name).file_name() else { return text(StatusCode::NOT_FOUND, "not found\n") };
    let t = base.join(n);
    let ok = t.extension().map(|x| x.to_string_lossy().to_lowercase()).is_some_and(|x| ["png", "jpg", "jpeg", "webp", "webm", "mp4", "gif"].contains(&x.as_str()));
    if ok && t.is_file() { file(req, &t).await } else { text(StatusCode::NOT_FOUND, "not found\n") }
}

/// Every request on the MCP ports comes through here.
async fn gate(State(app): State<Arc<App>>, ConnectInfo(peer): ConnectInfo<SocketAddr>, mut req: Request) -> Response {
    let path = req.uri().path().to_string();
    let bearer = req.headers().get(header::AUTHORIZATION).and_then(|v| v.to_str().ok()).filter(|a| a.len() > 7 && a[..7].eq_ignore_ascii_case("bearer ")).map(|a| a[7..].trim().to_string());
    let (key, rest) = match (&bearer, path.strip_prefix("/t/")) {
        (Some(t), _) => (app.reg.by_token(t), path.clone()),
        (None, Some(r)) => {
            let (given, tail) = r.split_once('/').unwrap_or((r, ""));
            (app.reg.by_token(given), format!("/{tail}"))
        }
        _ => (None, path.clone()),
    };
    let shown = match path.strip_prefix("/t/") {
        Some(r) => format!("/t/<token>/{}", r.split_once('/').map(|x| x.1).unwrap_or("")),
        None => path.clone(),
    };
    let ip = req.headers().get("x-forwarded-for").and_then(|v| v.to_str().ok()).and_then(|v| v.split(',').next()).map(|s| s.trim().to_string()).unwrap_or_else(|| peer.ip().to_string());
    let Some(key) = key else {
        app.log(format!("{ip} {} {shown} 401", req.method()));
        return text(StatusCode::UNAUTHORIZED, "unauthorized");
    };
    app.log(format!("{ip} {} {shown} ok [{}]", req.method(), key.name));
    app.reg.touch(&key.id, &ip);
    if let Some(t) = rest.strip_prefix("/audio").filter(|t| t.is_empty() || t.starts_with('/')) {
        return audio(req, &t.to_string()).await;
    }
    if let Some(n) = rest.strip_prefix("/images/") {
        return image(req, &n.to_string()).await;
    }
    if !(rest == "/mcp" || rest.starts_with("/mcp/")) {
        return text(if bearer.is_some() { StatusCode::NOT_FOUND } else { StatusCode::UNAUTHORIZED }, if bearer.is_some() { "not found" } else { "unauthorized" });
    }
    let pq = match req.uri().query() {
        Some(q) => format!("{rest}?{q}"),
        None => rest,
    };
    if let Ok(u) = pq.parse::<Uri>() {
        *req.uri_mut() = u;
    }
    match app.service(&key.id).oneshot(req).await {
        Ok(r) => r.map(Body::new),
        Err(e) => match e {},
    }
}

// ---------------------------------------------------------------- the dashboard
/// Loopback Host only (no DNS rebinding), and writes only as JSON from the dashboard's own
/// origin, so a web page open in the browser cannot drive the API.
fn dash_guard(app: &App, method: &Method, h: &HeaderMap) -> Option<Response> {
    let own = [format!("127.0.0.1:{}", app.dash_port), format!("localhost:{}", app.dash_port)];
    let host = h.get(header::HOST).and_then(|v| v.to_str().ok()).unwrap_or("");
    if !own.iter().any(|o| o == host) {
        return Some(text(StatusCode::FORBIDDEN, "dashboard is loopback-only"));
    }
    if method != Method::GET {
        let json = h.get(header::CONTENT_TYPE).and_then(|v| v.to_str().ok()).is_some_and(|c| c.starts_with("application/json"));
        let origin_ok = h.get(header::ORIGIN).and_then(|v| v.to_str().ok()).is_none_or(|o| own.iter().any(|x| o == format!("http://{x}")));
        if !json || !origin_ok {
            return Some(text(StatusCode::FORBIDDEN, "bad origin"));
        }
    }
    None
}

async fn dash_mw(State(app): State<Arc<App>>, req: Request, next: axum::middleware::Next) -> Response {
    match dash_guard(&app, req.method(), req.headers()) {
        Some(r) => r,
        None => next.run(req).await,
    }
}

const PRESETS: [&str; 4] = ["full", "core", "read-only", "custom"];

async fn state(State(app): State<Arc<App>>) -> Json<Value> {
    let keys = app.reg.keys.read().unwrap().clone();
    let mut out = Vec::new();
    for k in keys {
        let sessions = match app.manager(&k.id) {
            Some(m) => m.sessions.read().await.len(),
            None => 0,
        };
        let recent = now().saturating_sub(k.last_used) < 1800;
        let mut v = serde_json::to_value(&k).unwrap();
        v["sessions"] = json!(sessions);
        v["online"] = json!(k.enabled && sessions > 0 && recent);
        v["mcp_url"] = json!(format!("{}/t/{}/mcp", k.base, k.token));
        v["header_url"] = json!(format!("{}/mcp", k.base));
        v["audio_url"] = json!(format!("{}/t/{}/audio/", k.base, k.token));
        out.push(v);
    }
    let s = &app.template.spec;
    let tools: Vec<Value> = s
        .tools
        .iter()
        .map(|t| json!({"name": t.name, "summary": t.description.lines().next().unwrap_or(""), "core": s.core.contains(&t.name), "read_only": s.read_only.contains(&t.name)}))
        .collect();
    Json(json!({"keys": out, "tools": tools, "presets": PRESETS, "base": app.template_base(), "now": now()}))
}

impl App {
    fn template_base(&self) -> String {
        std::env::var("WOTR_MCP_PUBLIC_URL").unwrap_or_else(|_| "https://ultron.tailf1bfa3.ts.net".into()).trim_end_matches('/').to_string()
    }
}

#[derive(Deserialize)]
struct Edit {
    name: Option<String>,
    preset: Option<String>,
    tools: Option<Vec<String>>,
    enabled: Option<bool>,
    base: Option<String>,
}

fn check(e: &Edit) -> Result<(), Response> {
    if e.preset.as_ref().is_some_and(|p| !PRESETS.contains(&p.as_str())) {
        return Err(text(StatusCode::BAD_REQUEST, "preset must be full, core, read-only or custom"));
    }
    if e.name.as_ref().is_some_and(|n| n.trim().is_empty()) {
        return Err(text(StatusCode::BAD_REQUEST, "name is empty"));
    }
    Ok(())
}

async fn create(State(app): State<Arc<App>>, Json(e): Json<Edit>) -> Response {
    if let Err(r) = check(&e) {
        return r;
    }
    let k = Key {
        id: random_hex(4),
        name: e.name.unwrap_or_else(|| "New key".into()).trim().to_string(),
        token: random_hex(24),
        preset: e.preset.unwrap_or_else(|| "read-only".into()),
        tools: e.tools.unwrap_or_default(),
        enabled: e.enabled.unwrap_or(true),
        base: e.base.unwrap_or_else(|| app.template_base()),
        created: now(),
        last_used: 0,
        last_ip: String::new(),
        calls: 0,
    };
    app.reg.add(k.clone());
    Json(k).into_response()
}

async fn edit(State(app): State<Arc<App>>, UrlPath(id): UrlPath<String>, Json(e): Json<Edit>) -> Response {
    if let Err(r) = check(&e) {
        return r;
    }
    let disabling = e.enabled == Some(false);
    let r = app.reg.update(&id, |k| {
        if let Some(n) = e.name {
            k.name = n.trim().to_string();
        }
        if let Some(p) = e.preset {
            k.preset = p;
        }
        if let Some(t) = e.tools {
            k.tools = t;
        }
        if let Some(b) = e.enabled {
            k.enabled = b;
        }
        if let Some(b) = e.base {
            k.base = b.trim_end_matches('/').to_string();
        }
    });
    if disabling {
        app.drop_sessions(&id).await;
    }
    r.map(|k| Json(k).into_response()).unwrap_or_else(|| text(StatusCode::NOT_FOUND, "no such key"))
}

async fn rotate(State(app): State<Arc<App>>, UrlPath(id): UrlPath<String>) -> Response {
    let r = app.reg.update(&id, |k| k.token = random_hex(24));
    app.drop_sessions(&id).await;
    r.map(|k| Json(k).into_response()).unwrap_or_else(|| text(StatusCode::NOT_FOUND, "no such key"))
}

async fn remove(State(app): State<Arc<App>>, UrlPath(id): UrlPath<String>) -> Response {
    let gone = app.reg.remove(&id);
    app.drop_sessions(&id).await;
    if gone { text(StatusCode::OK, "deleted") } else { text(StatusCode::NOT_FOUND, "no such key") }
}

pub async fn serve(template: Wotr, ports: Vec<u16>, dash_port: u16, log: Option<String>) {
    let base = std::env::var("WOTR_MCP_PUBLIC_URL").unwrap_or_else(|_| "https://ultron.tailf1bfa3.ts.net".into());
    let reg = Arc::new(Registry::open(base.trim_end_matches('/')));
    let log = log.map(|p| Mutex::new(std::fs::OpenOptions::new().create(true).append(true).open(p).expect("--log file")));
    let app = Arc::new(App { template, reg: reg.clone(), services: Mutex::default(), log, dash_port });

    // usage counters live in memory; flush them once a minute
    let r = reg.clone();
    tokio::spawn(async move {
        let mut tick = tokio::time::interval(std::time::Duration::from_secs(60));
        loop {
            tick.tick().await;
            r.save();
        }
    });

    let mcp = Router::new().fallback(gate).with_state(app.clone());
    let dash = Router::new()
        .route("/", get(|| async { Html(include_str!("dash.html")) }))
        .route("/api/state", get(state))
        .route("/api/keys", post(create))
        .route("/api/keys/{id}", axum::routing::patch(edit).delete(remove))
        .route("/api/keys/{id}/rotate", post(rotate))
        .layer(axum::middleware::from_fn_with_state(app.clone(), dash_mw))
        .with_state(app.clone());

    let mut tasks = Vec::new();
    for p in &ports {
        let l = tokio::net::TcpListener::bind(("127.0.0.1", *p)).await.unwrap_or_else(|e| panic!("port {p}: {e}"));
        let svc = mcp.clone().into_make_service_with_connect_info::<SocketAddr>();
        tasks.push(tokio::spawn(async move { axum::serve(l, svc).await }));
    }
    let l = tokio::net::TcpListener::bind(("127.0.0.1", dash_port)).await.unwrap_or_else(|e| panic!("dashboard port {dash_port}: {e}"));
    tasks.push(tokio::spawn(async move { axum::serve(l, dash.into_make_service_with_connect_info::<SocketAddr>()).await }));
    let n = reg.keys.read().unwrap().len();
    app.log(format!("wotr-mcp http: MCP on 127.0.0.1:{ports:?}, {n} keys; dashboard http://127.0.0.1:{dash_port}/"));
    for t in tasks {
        let _ = t.await;
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn helpers() {
        assert_eq!(super::iso(0), "1970-01-01T00:00:00Z");
        assert_eq!(super::iso(1_793_750_400), "2026-11-04T00:00:00Z");
        assert_eq!(super::pct_decode("a%20b%E2%80%94c%zz"), "a b—c%zz");
    }
}
