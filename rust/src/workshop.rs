//! WOTR Workshop: each player's own library (characters, techniques, items, lore, places, factions)
//! with images, and Natalie on the player's own AI, wired to the MCP's read tools.
//!
//!   wotr-mcp workshop [--port 8780]           http://127.0.0.1:8780
//!   wotr-mcp workshop invite [note]           print a new invite code
//!   WOTR_APP_DEV=1 wotr-mcp workshop          adds /auth/dev for local testing (never behind Funnel)
//!
//! Sign-in is a key (an invite that becomes the holder's own on first use), or Discord OAuth when
//! DISCORD_CLIENT_ID and DISCORD_CLIENT_SECRET are set. Data lives in WOTR_APP_DATA (default
//! ~/.local/share/wotr-app): app.db and images/. The AI key never reaches this server: the browser
//! calls the provider and comes here only for the tools (POST /api/tool/<name>).
use crate::pyjson::dumps_unicode;
use crate::util::{env, env_path, quote, read_lossy, root};
use crate::{ContentBlock, Wotr};
use axum::body::{Body, Bytes};
use axum::extract::{ConnectInfo, DefaultBodyLimit, Multipart, Path as UrlPath, Query, State};
use axum::http::{header, HeaderMap, Method, StatusCode, Uri};
use axum::response::{IntoResponse, Response};
use axum::routing::{get, post, put};
use axum::Router;
use regex::Regex;
use rusqlite::{params, Connection, OptionalExtension};
use serde_json::{json, Map, Value};
use std::collections::HashMap;
use std::io::{Read, Write};
use std::net::SocketAddr;
use std::path::PathBuf;
use std::process::{Command, Stdio};
use std::sync::Arc;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

const KINDS: [&str; 6] = ["character", "technique", "item", "lore", "place", "faction"];
const COOKIE: &str = "wotr_session";
const SESSION_SECS: i64 = 30 * 86400;
const MAX_IMAGE: usize = 8 * 1024 * 1024;
const MAX_ENTRY: usize = 400_000; // bytes of JSON per entry
const CULTURES: [&str; 12] = ["Kharven", "Accord", "Dawi", "Moto", "Eresse", "Expanse", "Korvaeth", "Stannvaard", "Nal\u{16b}n", "Ketsuen", "Zettari", "Yukari"];
const ITEM_TIERS: [&str; 10] = ["Plain", "Marked", "Proofed", "Tempered", "Instrument", "Hallowed", "Storied", "Found", "Numinous", "Proscribed"];

struct App {
    dev: bool,
    data: PathBuf,
    tools: Wotr,
}

type Shared = State<Arc<App>>;

enum Fail {
    NotFound,
    Bad(String),
    Reply(Response),
    Internal(String),
}

impl From<rusqlite::Error> for Fail {
    fn from(e: rusqlite::Error) -> Self {
        Fail::Internal(e.to_string())
    }
}

impl From<std::io::Error> for Fail {
    fn from(e: std::io::Error) -> Self {
        Fail::Internal(e.to_string())
    }
}

impl IntoResponse for Fail {
    fn into_response(self) -> Response {
        match self {
            Fail::NotFound => reply(StatusCode::NOT_FOUND, json!({"error": "not found"})),
            Fail::Bad(m) => reply(StatusCode::BAD_REQUEST, json!({"error": m})),
            Fail::Reply(r) => r,
            Fail::Internal(m) => {
                eprintln!("workshop: {m}");
                reply(StatusCode::INTERNAL_SERVER_ERROR, json!({"error": "server error"}))
            }
        }
    }
}

type Out = Result<Response, Fail>;

fn reply(status: StatusCode, v: Value) -> Response {
    (status, [(header::CONTENT_TYPE, "application/json")], serde_json::to_string(&v).unwrap_or_default()).into_response()
}

fn ok(v: Value) -> Out {
    Ok(reply(StatusCode::OK, v))
}

fn redirect(to: &str, status: StatusCode) -> Response {
    Response::builder().status(status).header(header::LOCATION, to).body(Body::empty()).unwrap()
}

// ---------- small things ----------
fn random_bytes(n: usize) -> Vec<u8> {
    let mut b = vec![0u8; n];
    std::fs::File::open("/dev/urandom").and_then(|mut f| f.read_exact(&mut b)).expect("/dev/urandom");
    b
}

/// secrets.token_urlsafe(n)
fn token(n: usize) -> String {
    const A: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    let (bytes, mut out) = (random_bytes(n), String::new());
    for c in bytes.chunks(3) {
        let v = (u32::from(c[0]) << 16) | (u32::from(*c.get(1).unwrap_or(&0)) << 8) | u32::from(*c.get(2).unwrap_or(&0));
        for i in 0..=c.len() {
            out.push(A[((v >> (18 - 6 * i)) & 63) as usize] as char);
        }
    }
    out
}

fn now() -> String {
    chrono::Utc::now().format("%Y-%m-%dT%H:%M:%S+00:00").to_string()
}

fn epoch() -> f64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map_or(0.0, |d| d.as_secs_f64())
}

fn take(s: &str, n: usize) -> String {
    s.chars().take(n).collect()
}

fn escape(s: &str) -> String {
    s.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace('\'', "&#x27;")
}

fn same(a: &str, b: &str) -> bool {
    a.len() == b.len() && a.bytes().zip(b.bytes()).fold(0u8, |d, (x, y)| d | (x ^ y)) == 0
}

fn percent_decode(s: &str) -> String {
    let (b, mut out, mut i) = (s.as_bytes(), Vec::new(), 0);
    while i < b.len() {
        let hex = (b[i] == b'%').then(|| s.get(i + 1..i + 3).and_then(|h| u8::from_str_radix(h, 16).ok())).flatten();
        if let Some(v) = hex {
            out.push(v);
            i += 3;
        } else {
            out.push(b[i]);
            i += 1;
        }
    }
    String::from_utf8_lossy(&out).into_owned()
}

fn cookie(headers: &HeaderMap, name: &str) -> Option<String> {
    headers.get_all(header::COOKIE).iter().filter_map(|v| v.to_str().ok()).flat_map(|v| v.split(';')).find_map(|p| {
        let (k, v) = p.trim().split_once('=')?;
        (k == name).then(|| v.to_string())
    })
}

fn wants_write(headers: &HeaderMap) -> bool {
    headers.get("x-wotr").is_some_and(|v| v == "1")
}

fn body_json(b: &[u8]) -> Result<Value, Fail> {
    serde_json::from_slice(b).map_err(|e| Fail::Bad(e.to_string()))
}

fn field(v: &Value, k: &str) -> String {
    match v.get(k) {
        None | Some(Value::Null) => String::new(),
        Some(Value::String(s)) => s.clone(),
        Some(o) => o.to_string(),
    }
}

fn truthy(v: Option<&Value>) -> bool {
    match v {
        None | Some(Value::Null) => false,
        Some(Value::Bool(b)) => *b,
        Some(Value::String(s)) => !s.is_empty(),
        Some(Value::Array(a)) => !a.is_empty(),
        Some(Value::Object(o)) => !o.is_empty(),
        Some(Value::Number(n)) => n.as_f64() != Some(0.0),
    }
}

// ---------- storage ----------
fn data_dir() -> PathBuf {
    env_path("WOTR_APP_DATA", Some("~/.local/share/wotr-app")).expect("a data folder")
}

fn open(data: &std::path::Path) -> Result<Connection, Fail> {
    std::fs::create_dir_all(data)?;
    let con = Connection::open(data.join("app.db"))?;
    con.busy_timeout(Duration::from_secs(5))?;
    con.execute_batch(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, discord_id TEXT UNIQUE, name TEXT, avatar TEXT, created TEXT);
         CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id INTEGER, expires REAL);
         CREATE TABLE IF NOT EXISTS invites(code TEXT PRIMARY KEY, note TEXT, used_by INTEGER, created TEXT);
         CREATE TABLE IF NOT EXISTS entries(id TEXT PRIMARY KEY, owner INTEGER, kind TEXT, title TEXT, data TEXT,
             portrait TEXT, created TEXT, updated TEXT);
         CREATE TABLE IF NOT EXISTS images(id TEXT PRIMARY KEY, owner INTEGER, entry_id TEXT, ext TEXT, created TEXT);",
    )?;
    // sharing, added 2026-10-30: an unguessable token per shared entry, NULL when private
    if con.execute_batch("ALTER TABLE entries ADD COLUMN share TEXT").is_ok() {
        con.execute_batch("CREATE UNIQUE INDEX IF NOT EXISTS entries_share ON entries(share)")?;
    }
    Ok(con)
}

/// Every row as a JSON object under its column names.
fn rows(con: &Connection, sql: &str, args: impl rusqlite::Params) -> Result<Vec<Map<String, Value>>, Fail> {
    use rusqlite::types::ValueRef;
    let mut st = con.prepare(sql)?;
    let names: Vec<String> = st.column_names().iter().map(|s| s.to_string()).collect();
    let mut q = st.query(args)?;
    let mut out = Vec::new();
    while let Some(r) = q.next()? {
        let mut m = Map::new();
        for (i, n) in names.iter().enumerate() {
            let v = match r.get_ref(i)? {
                ValueRef::Null | ValueRef::Blob(_) => Value::Null,
                ValueRef::Integer(x) => json!(x),
                ValueRef::Real(x) => json!(x),
                ValueRef::Text(t) => json!(String::from_utf8_lossy(t)),
            };
            m.insert(n.clone(), v);
        }
        out.push(m);
    }
    Ok(out)
}

fn text(m: &Map<String, Value>, k: &str) -> String {
    m.get(k).and_then(Value::as_str).unwrap_or("").to_string()
}

fn new_invite(data: &std::path::Path, note: &str) -> Result<String, Fail> {
    // 64 bits: it doubles as the sign-in key
    let code = random_bytes(8).chunks(2).map(|c| format!("{:02X}{:02X}", c[0], c[1])).collect::<Vec<_>>().join("-");
    open(data)?.execute("INSERT INTO invites(code, note, created) VALUES(?,?,?)", params![code, note, now()])?;
    Ok(code)
}

// ---------- canon lists, read from the repo so they never drift ----------
fn canon() -> Result<Value, String> {
    let magic = root("wiki/The Magic System");
    let rx = |p: &str| Regex::new(p).map_err(|e| e.to_string());
    let page = read_lossy(&magic.join("Fracture of Worlds \u{2014} The Living System/VI. The Sixteen Temperance Stages (Part Sixteen).md"));
    let stages: Vec<Value> = rx(r"(?m)^### Stage ([IVX]+) \x{2014} (\S+) \(Tier (\d+) \x{b7} (\w+)\)")?
        .captures_iter(&page)
        .map(|m| json!({"numeral": &m[1], "name": &m[2], "tier": m[3].parse::<i64>().unwrap_or(0), "standing": &m[4]}))
        .collect();
    let dir = magic.join("The Foundations/The Eight Families & the Sixty Wellsprings");
    let mut files: Vec<PathBuf> = std::fs::read_dir(&dir)
        .map_err(|e| format!("{}: {e}", dir.display()))?
        .flatten()
        .map(|e| e.path())
        .filter(|p| p.extension().is_some_and(|x| x == "md") && p.file_stem().is_some_and(|s| s.to_string_lossy().contains(" \u{2014} ")))
        .collect();
    files.sort();
    let spring = rx(r"(?m)^## (.+?) \x{b7} \*(.+?)\*")?;
    let mut families = Vec::new();
    for f in files {
        let stem = f.file_stem().unwrap_or_default().to_string_lossy().into_owned();
        let (fam, domain) = stem.split_once(" \u{2014} ").unwrap_or((&stem, ""));
        let body = read_lossy(&f);
        let springs: Vec<Value> = spring.captures_iter(&body).map(|m| json!({"name": m[1].trim(), "gloss": m[2].trim()})).collect();
        families.push(json!({"name": fam, "domain": domain, "wellsprings": springs}));
    }
    let tpl = read_lossy(&root("desktop/templates/CHARACTER_CARD_TEMPLATE.md"));
    let sep = rx(r" \x{b7} | \| ")?;
    let options = |label: &str| -> Result<Vec<String>, String> {
        let re = rx(&format!(r"(?m)^\*\*{}\*\* \x{{b7}} <(.+?)>", regex::escape(label)))?;
        let c = re.captures(&tpl).ok_or_else(|| format!("no {label} in the card template"))?;
        Ok(sep.split(&c[1]).map(|o| o.trim().to_string()).collect())
    };
    Ok(json!({
        "stages": stages, "families": families, "cultures": CULTURES, "item_tiers": ITEM_TIERS,
        "paths": ["Body", "Spirit", "Attraction", "Fate"],
        "aether_classes": options("Aether Class")?, "crystal_tiers": options("Soul Crystal Tier")?,
        "essence": options("Essence Typology")?,
        "combat_grammar": ["Verdict", "Blade", "Percussion", "Expenditure"],
        "trait_kinds": ["Primary Trait", "Secondary Trait", "Inherited Trait", "Passive Trait", "Compound Trait", "Higher-Imprint Trait"],
        "technique_kinds": ["Signature Technique", "School Art", "Bloodline Faculty", "Synergia", "Combined Art", "First Release", "Second Release", "Third Release", "Domain"],
        "kinds": KINDS,
    }))
}

// ---------- auth ----------
fn current_user(app: &App, headers: &HeaderMap) -> Result<Option<Map<String, Value>>, Fail> {
    let Some(t) = cookie(headers, COOKIE) else { return Ok(None) };
    let con = open(&app.data)?;
    Ok(rows(&con, "SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token=? AND s.expires>?", params![t, epoch()])?.into_iter().next())
}

/// The signed-in user, or the reply that says why not. Writes need the X-WOTR header, which a
/// cross-site form cannot send.
fn signed_in(app: &App, headers: &HeaderMap, method: &Method) -> Result<(i64, Map<String, Value>), Fail> {
    let Some(u) = current_user(app, headers)? else {
        return Err(Fail::Reply(reply(StatusCode::UNAUTHORIZED, json!({"error": "sign in"}))));
    };
    if method != Method::GET && method != Method::HEAD && !wants_write(headers) {
        return Err(Fail::Reply(reply(StatusCode::FORBIDDEN, json!({"error": "missing X-WOTR header"}))));
    }
    Ok((u.get("id").and_then(Value::as_i64).unwrap_or(0), u))
}

fn session_cookie(app: &App, user: i64, headers: &HeaderMap) -> Result<String, Fail> {
    let t = token(32);
    open(&app.data)?.execute("INSERT INTO sessions VALUES(?,?,?)", params![t, user, epoch() + SESSION_SECS as f64])?;
    let https = headers.get("x-forwarded-proto").is_some_and(|v| v == "https") || env("WOTR_APP_URL").is_some_and(|u| u.starts_with("https"));
    Ok(format!("{COOKIE}={t}; HttpOnly; Max-Age={SESSION_SECS}; Path=/; SameSite=lax{}", if https { "; Secure" } else { "" }))
}

fn start_session(app: &App, user: i64, headers: &HeaderMap) -> Out {
    let mut r = redirect("/", StatusCode::SEE_OTHER);
    r.headers_mut().insert(header::SET_COOKIE, session_cookie(app, user, headers)?.parse().map_err(|_| Fail::Internal("cookie".into()))?);
    Ok(r)
}

fn base_url(headers: &HeaderMap) -> String {
    env("WOTR_APP_URL").map(|u| u.trim_end_matches('/').to_string()).unwrap_or_else(|| format!("http://{}", headers.get(header::HOST).and_then(|h| h.to_str().ok()).unwrap_or("127.0.0.1")))
}

fn discord_api() -> String {
    std::env::var("WOTR_DISCORD_API").unwrap_or_else(|_| "https://discord.com/api".into())
}

/// curl with its config on stdin, so the client secret and the bearer token stay out of `ps`.
fn curl(config: &str, data: Option<&str>) -> Option<Value> {
    let mut c = Command::new("curl").args(["-sSf", "--max-time", "15", "-K", "-"]).stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().ok()?;
    let body = match data {
        Some(d) => format!("{config}\ndata = \"{d}\"\n"),
        None => format!("{config}\n"),
    };
    c.stdin.take()?.write_all(body.as_bytes()).ok()?;
    let o = c.wait_with_output().ok()?;
    if !o.status.success() {
        return None;
    }
    serde_json::from_slice(&o.stdout).ok()
}

fn upsert_user(app: &App, discord_id: &str, name: &str, avatar: &str, invite: &str) -> Result<Option<i64>, Fail> {
    let mut con = open(&app.data)?;
    let tx = con.transaction()?;
    if let Some(id) = tx.query_row("SELECT id FROM users WHERE discord_id=?", [discord_id], |r| r.get::<_, i64>(0)).optional()? {
        tx.execute("UPDATE users SET name=?, avatar=? WHERE id=?", params![name, avatar, id])?;
        tx.commit()?;
        return Ok(Some(id));
    }
    let code = invite.trim().to_uppercase();
    if tx.query_row("SELECT code FROM invites WHERE code=? AND used_by IS NULL", [&code], |r| r.get::<_, String>(0)).optional()?.is_none() {
        return Ok(None);
    }
    tx.execute("INSERT INTO users(discord_id, name, avatar, created) VALUES(?,?,?,?)", params![discord_id, name, avatar, now()])?;
    let id = tx.last_insert_rowid();
    tx.execute("UPDATE invites SET used_by=? WHERE code=?", params![id, code])?;
    tx.commit()?;
    Ok(Some(id))
}

async fn auth_discord(headers: HeaderMap, Query(q): Query<HashMap<String, String>>) -> Out {
    let Some(cid) = env("DISCORD_CLIENT_ID") else {
        return Ok(reply(StatusCode::SERVICE_UNAVAILABLE, json!({"error": "Discord sign-in is not configured"})));
    };
    let state = token(16);
    let callback = format!("{}/auth/discord/callback", base_url(&headers));
    let url = format!("https://discord.com/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope=identify&state={}&prompt=none", quote(&cid, "", true), quote(&callback, "", true), quote(&state, "", true));
    let saved = json!({"state": state, "invite": q.get("invite").cloned().unwrap_or_default()}).to_string();
    let mut r = redirect(&url, StatusCode::TEMPORARY_REDIRECT);
    let c = format!("wotr_oauth={}; HttpOnly; Max-Age=600; Path=/; SameSite=lax", quote(&saved, "", false));
    r.headers_mut().insert(header::SET_COOKIE, c.parse().map_err(|_| Fail::Internal("cookie".into()))?);
    Ok(r)
}

async fn auth_discord_callback(State(app): Shared, headers: HeaderMap, Query(q): Query<HashMap<String, String>>) -> Out {
    let saved: Value = cookie(&headers, "wotr_oauth").and_then(|c| serde_json::from_str(&percent_decode(&c)).ok()).unwrap_or(json!({}));
    let state = field(&saved, "state");
    let got = q.get("state").map_or("", String::as_str);
    if state.is_empty() || !same(&state, got) {
        return Ok(redirect("/#/signin?error=state", StatusCode::SEE_OTHER));
    }
    let callback = format!("{}/auth/discord/callback", base_url(&headers));
    let form = format!(
        "client_id={}&client_secret={}&grant_type=authorization_code&code={}&redirect_uri={}",
        quote(&env("DISCORD_CLIENT_ID").unwrap_or_default(), "", true),
        quote(&env("DISCORD_CLIENT_SECRET").unwrap_or_default(), "", true),
        quote(q.get("code").map_or("", String::as_str), "", true),
        quote(&callback, "", true)
    );
    let api = discord_api();
    let exchange = tokio::task::spawn_blocking(move || {
        let tok = curl(&format!("url = \"{api}/oauth2/token\""), Some(&form))?;
        let bearer = tok.get("access_token")?.as_str()?.to_string();
        curl(&format!("url = \"{api}/users/@me\"\nheader = \"Authorization: Bearer {bearer}\""), None)
    });
    let Some(me) = exchange.await.map_err(|e| Fail::Internal(e.to_string()))? else {
        return Ok(redirect("/#/signin?error=discord", StatusCode::SEE_OTHER));
    };
    let id = field(&me, "id");
    let avatar = if truthy(me.get("avatar")) { format!("https://cdn.discordapp.com/avatars/{id}/{}.png", field(&me, "avatar")) } else { String::new() };
    let name = if truthy(me.get("global_name")) { field(&me, "global_name") } else { field(&me, "username") };
    let Some(uid) = upsert_user(&app, &id, &name, &avatar, &field(&saved, "invite"))? else {
        return Ok(redirect("/#/signin?error=invite", StatusCode::SEE_OTHER));
    };
    let mut r = start_session(&app, uid, &headers)?;
    r.headers_mut().append(header::SET_COOKIE, "wotr_oauth=; Max-Age=0; Path=/".parse().map_err(|_| Fail::Internal("cookie".into()))?);
    Ok(r)
}

async fn auth_dev(State(app): Shared, ConnectInfo(peer): ConnectInfo<SocketAddr>, headers: HeaderMap, Query(q): Query<HashMap<String, String>>) -> Out {
    if !app.dev || !peer.ip().is_loopback() {
        return Ok((StatusCode::NOT_FOUND, "not found").into_response());
    }
    let name = take(q.get("name").map_or("Dev", String::as_str), 40);
    let con = open(&app.data)?;
    let key = format!("dev:{name}");
    let found = con.query_row("SELECT id FROM users WHERE discord_id=?", [&key], |r| r.get::<_, i64>(0)).optional()?;
    let uid = match found {
        Some(id) => id,
        None => {
            con.execute("INSERT INTO users(discord_id, name, avatar, created) VALUES(?,?,?,?)", params![key, name, "", now()])?;
            con.last_insert_rowid()
        }
    };
    start_session(&app, uid, &headers)
}

/// Sign in with a key. An unused invite becomes the holder's personal key on first use (with a
/// name); after that the same key signs them back in on any device.
async fn auth_key(State(app): Shared, headers: HeaderMap, raw: Bytes) -> Out {
    if !wants_write(&headers) {
        return Ok(reply(StatusCode::FORBIDDEN, json!({"error": "missing X-WOTR header"})));
    }
    let body = body_json(&raw)?;
    let code = field(&body, "key").trim().to_uppercase();
    let name = take(field(&body, "name").trim(), 40);
    let mut con = open(&app.data)?;
    let tx = con.transaction()?;
    let found: Option<Option<i64>> = if code.is_empty() { None } else { tx.query_row("SELECT used_by FROM invites WHERE code=?", [&code], |r| r.get(0)).optional()? };
    let Some(used) = found else {
        return Ok(reply(StatusCode::UNAUTHORIZED, json!({"error": "That key is not valid."})));
    };
    let uid = match used {
        Some(u) => u,
        None => {
            if name.is_empty() {
                return Ok(reply(StatusCode::BAD_REQUEST, json!({"error": "First time with this key: add the name you want to go by.", "need_name": true})));
            }
            tx.execute("INSERT INTO users(discord_id, name, avatar, created) VALUES(?,?,?,?)", params![format!("key:{}", hex(&random_bytes(8))), name, "", now()])?;
            let id = tx.last_insert_rowid();
            tx.execute("UPDATE invites SET used_by=? WHERE code=?", params![id, code])?;
            id
        }
    };
    tx.commit()?;
    let mut r = reply(StatusCode::OK, json!({"ok": true}));
    r.headers_mut().insert(header::SET_COOKIE, session_cookie(&app, uid, &headers)?.parse().map_err(|_| Fail::Internal("cookie".into()))?);
    Ok(r)
}

fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
}

async fn auth_logout(State(app): Shared, headers: HeaderMap) -> Out {
    open(&app.data)?.execute("DELETE FROM sessions WHERE token=?", [cookie(&headers, COOKIE).unwrap_or_default()])?;
    let mut r = redirect("/#/signin", StatusCode::SEE_OTHER);
    r.headers_mut().insert(header::SET_COOKIE, format!("{COOKIE}=; Max-Age=0; Path=/").parse().map_err(|_| Fail::Internal("cookie".into()))?);
    Ok(r)
}

// ---------- the API ----------
fn own_entry(con: &Connection, user: i64, eid: &str) -> Result<Map<String, Value>, Fail> {
    rows(con, "SELECT * FROM entries WHERE id=? AND owner=?", params![eid, user])?.into_iter().next().ok_or(Fail::NotFound)
}

fn entry_out(mut m: Map<String, Value>) -> Value {
    let raw = text(&m, "data");
    let parsed = if raw.is_empty() { json!({}) } else { serde_json::from_str(&raw).unwrap_or(json!({})) };
    m.insert("data".into(), parsed);
    m.remove("owner");
    Value::Object(m)
}

async fn me(State(app): Shared, headers: HeaderMap, method: Method) -> Out {
    let (_, u) = signed_in(&app, &headers, &method)?;
    ok(json!({"name": u.get("name"), "avatar": u.get("avatar"), "discord": env("DISCORD_CLIENT_ID").is_some()}))
}

async fn status(State(app): Shared) -> Out {
    ok(json!({"discord": env("DISCORD_CLIENT_ID").is_some(), "dev": app.dev}))
}

async fn canon_route() -> Out {
    canon().map_err(Fail::Internal).and_then(ok)
}

async fn entries_list(State(app): Shared, headers: HeaderMap, method: Method) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let con = open(&app.data)?;
    let list = rows(&con, "SELECT id, kind, title, portrait, updated, json_extract(data,'$.epithet') AS epithet, json_extract(data,'$.aura') AS aura, json_extract(data,'$.culture') AS culture, json_extract(data,'$.kindOf') AS kindOf, share IS NOT NULL AS shared FROM entries WHERE owner=? ORDER BY updated DESC", [uid])?;
    ok(Value::Array(list.into_iter().map(Value::Object).collect()))
}

fn data_text(body: &Value) -> String {
    dumps_unicode(body.get("data").filter(|d| truthy(Some(d))).unwrap_or(&json!({})), None)
}

async fn entries_create(State(app): Shared, headers: HeaderMap, method: Method, raw: Bytes) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let body = body_json(&raw)?;
    let kind = field(&body, "kind");
    if !KINDS.contains(&kind.as_str()) {
        return Err(Fail::Bad(format!("kind must be one of {}", KINDS.join(", "))));
    }
    let (eid, stamp, con) = (token(9), now(), open(&app.data)?);
    con.execute("INSERT INTO entries(id, owner, kind, title, data, portrait, created, updated) VALUES(?,?,?,?,?,?,?,?)", params![eid, uid, kind, take(&field(&body, "title"), 200), data_text(&body), Option::<String>::None, stamp, stamp])?;
    Ok(reply(StatusCode::CREATED, entry_out(own_entry(&con, uid, &eid)?)))
}

async fn entry_get(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(eid): UrlPath<String>) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    ok(entry_out(own_entry(&open(&app.data)?, uid, &eid)?))
}

async fn entry_put(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(eid): UrlPath<String>, raw: Bytes) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let con = open(&app.data)?;
    let row = own_entry(&con, uid, &eid)?;
    let body = body_json(&raw)?;
    let data = data_text(&body);
    if data.len() > MAX_ENTRY {
        return Err(Fail::Bad("entry too large".into()));
    }
    let portrait: Option<String> = match body.get("portrait") {
        Some(p) => p.as_str().map(String::from),
        None => row.get("portrait").and_then(Value::as_str).map(String::from),
    };
    if let Some(p) = portrait.as_deref().filter(|p| !p.is_empty()) {
        if con.query_row("SELECT 1 FROM images WHERE id=? AND owner=?", params![p, uid], |_| Ok(())).optional()?.is_none() {
            return Err(Fail::Bad("portrait must be one of your images".into()));
        }
    }
    let title = if body.get("title").is_some() { field(&body, "title") } else { text(&row, "title") };
    con.execute("UPDATE entries SET title=?, data=?, portrait=?, updated=? WHERE id=?", params![take(&title, 200), data, portrait, now(), eid])?;
    ok(entry_out(own_entry(&con, uid, &eid)?))
}

async fn entry_delete(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(eid): UrlPath<String>) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let mut con = open(&app.data)?;
    own_entry(&con, uid, &eid)?;
    let images = rows(&con, "SELECT id, ext FROM images WHERE entry_id=? AND owner=?", params![eid, uid])?;
    let tx = con.transaction()?;
    tx.execute("DELETE FROM images WHERE entry_id=? AND owner=?", params![eid, uid])?;
    tx.execute("DELETE FROM entries WHERE id=?", [&eid])?;
    tx.commit()?;
    for i in images {
        let _ = std::fs::remove_file(app.data.join("images").join(format!("{}.{}", text(&i, "id"), text(&i, "ext"))));
    }
    ok(json!({"deleted": eid}))
}

async fn images_list(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(eid): UrlPath<String>) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let con = open(&app.data)?;
    own_entry(&con, uid, &eid)?;
    let list = rows(&con, "SELECT id, ext, created FROM images WHERE entry_id=? AND owner=? ORDER BY created", params![eid, uid])?;
    ok(Value::Array(list.into_iter().map(Value::Object).collect()))
}

/// The extension a file's own bytes prove, whatever it claims to be: files are served under this
/// type only, so a script named .png stays out.
fn image_ext(b: &[u8]) -> Option<&'static str> {
    if b.starts_with(b"\x89PNG\r\n\x1a\n") && b.get(12..16) == Some(b"IHDR") {
        Some("png")
    } else if b.starts_with(b"\xff\xd8\xff") {
        Some("jpg")
    } else if b.starts_with(b"RIFF") && b.get(8..12) == Some(b"WEBP") {
        Some("webp")
    } else if b.starts_with(b"GIF87a") || b.starts_with(b"GIF89a") {
        Some("gif")
    } else {
        None
    }
}

async fn images_upload(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(eid): UrlPath<String>, mut form: Multipart) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let mut con = open(&app.data)?;
    own_entry(&con, uid, &eid)?;
    let mut raw = None;
    while let Some(f) = form.next_field().await.map_err(|e| Fail::Bad(e.to_string()))? {
        if f.name() == Some("file") {
            raw = Some(f.bytes().await.map_err(|e| Fail::Bad(e.to_string()))?);
            break;
        }
    }
    let raw = raw.ok_or_else(|| Fail::Bad("no file".into()))?;
    if raw.len() > MAX_IMAGE {
        return Err(Fail::Bad("image over 8 MB".into()));
    }
    let ext = image_ext(&raw).ok_or_else(|| Fail::Bad("png, jpg, webp or gif only".into()))?;
    let iid = token(12);
    let dir = app.data.join("images");
    std::fs::create_dir_all(&dir)?;
    std::fs::write(dir.join(format!("{iid}.{ext}")), &raw)?;
    let tx = con.transaction()?;
    tx.execute("INSERT INTO images VALUES(?,?,?,?,?)", params![iid, uid, eid, ext, now()])?;
    tx.execute("UPDATE entries SET portrait=? WHERE id=? AND (portrait IS NULL OR portrait='')", params![iid, eid])?;
    tx.commit()?;
    Ok(reply(StatusCode::CREATED, json!({"id": iid, "ext": ext})))
}

fn serve_image(app: &App, id: &str, ext: &str, cache: &'static str) -> Out {
    let bytes = std::fs::read(app.data.join("images").join(format!("{id}.{ext}"))).map_err(|_| Fail::NotFound)?;
    let kind = match ext {
        "png" => "image/png",
        "jpg" => "image/jpeg",
        "webp" => "image/webp",
        _ => "image/gif",
    };
    Ok(([(header::CONTENT_TYPE, kind), (header::CACHE_CONTROL, cache)], bytes).into_response())
}

async fn image_get(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(iid): UrlPath<String>) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let row = rows(&open(&app.data)?, "SELECT ext FROM images WHERE id=? AND owner=?", params![iid, uid])?.into_iter().next().ok_or(Fail::NotFound)?;
    serve_image(&app, &iid, &text(&row, "ext"), "private, max-age=86400")
}

async fn image_delete(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(iid): UrlPath<String>) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let mut con = open(&app.data)?;
    let row = rows(&con, "SELECT ext FROM images WHERE id=? AND owner=?", params![iid, uid])?.into_iter().next().ok_or(Fail::NotFound)?;
    let tx = con.transaction()?;
    tx.execute("DELETE FROM images WHERE id=?", [&iid])?;
    tx.execute("UPDATE entries SET portrait=NULL WHERE portrait=?", [&iid])?;
    tx.commit()?;
    let _ = std::fs::remove_file(app.data.join("images").join(format!("{iid}.{}", text(&row, "ext"))));
    ok(json!({"deleted": iid}))
}

async fn tools(State(app): Shared, headers: HeaderMap, method: Method) -> Out {
    signed_in(&app, &headers, &method)?;
    let list: Vec<Value> = app.tools.surface().tools.iter().map(|t| json!({"name": t.name, "description": t.description, "input_schema": t.input_schema})).collect();
    ok(Value::Array(list))
}

async fn tool(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(name): UrlPath<String>, raw: Bytes) -> Out {
    signed_in(&app, &headers, &method)?;
    let Value::Object(args) = body_json(&raw)? else {
        return Err(Fail::Bad("arguments must be an object".into()));
    };
    match tokio::time::timeout(Duration::from_secs(120), app.tools.call(&name, args)).await {
        Err(_) => ok(json!({"text": format!("{name} timed out after two minutes"), "error": true})),
        // an unknown tool or bad arguments: the model reads the message and retries
        Ok(Err(e)) => ok(json!({"text": format!("{name} failed: {e}"), "error": true})),
        Ok(Ok(blocks)) => {
            let text: Vec<String> = blocks.into_iter().filter_map(|b| match b {
                ContentBlock::Text(t) => Some(t.text.clone()),
                _ => None,
            }).collect();
            ok(json!({"text": text.join("\n"), "error": false}))
        }
    }
}

/// Turn an entry's share link on (a fresh unguessable token) or off.
async fn entry_share(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(eid): UrlPath<String>, raw: Bytes) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let on = truthy(body_json(&raw)?.get("on"));
    let con = open(&app.data)?;
    let row = own_entry(&con, uid, &eid)?;
    let tok = on.then(|| row.get("share").and_then(Value::as_str).map(String::from).unwrap_or_else(|| token(12)));
    con.execute("UPDATE entries SET share=? WHERE id=?", params![tok, eid])?;
    ok(json!({"share": tok}))
}

fn shared_row(con: &Connection, tok: &str) -> Result<Map<String, Value>, Fail> {
    rows(con, "SELECT e.*, u.name AS owner_name FROM entries e JOIN users u ON u.id = e.owner WHERE e.share=?", [tok])?.into_iter().next().ok_or(Fail::NotFound)
}

/// A shared entry, read-only, for anyone holding the link.
async fn shared(State(app): Shared, UrlPath(tok): UrlPath<String>) -> Out {
    let con = open(&app.data)?;
    let Ok(row) = shared_row(&con, &tok) else {
        return Ok(reply(StatusCode::NOT_FOUND, json!({"error": "This link is not shared, or it was turned off."})));
    };
    let images: Vec<Value> = rows(&con, "SELECT id FROM images WHERE entry_id=? ORDER BY created", [text(&row, "id")])?.into_iter().filter_map(|m| m.get("id").cloned()).collect();
    let data = text(&row, "data");
    ok(json!({"kind": row.get("kind"), "title": row.get("title"), "data": serde_json::from_str::<Value>(&data).unwrap_or(json!({})), "portrait": row.get("portrait"), "images": images, "owner": row.get("owner_name"), "updated": row.get("updated")}))
}

async fn shared_image(State(app): Shared, UrlPath((tok, iid)): UrlPath<(String, String)>) -> Out {
    let con = open(&app.data)?;
    let found = match shared_row(&con, &tok) {
        Ok(row) => rows(&con, "SELECT id, ext FROM images WHERE id=? AND entry_id=?", params![iid, text(&row, "id")])?.into_iter().next(),
        Err(_) => None,
    };
    let Some(img) = found else {
        return Ok((StatusCode::NOT_FOUND, "not found").into_response());
    };
    serve_image(&app, &text(&img, "id"), &text(&img, "ext"), "public, max-age=3600")
}

/// Save a copy of a shared entry, with its images, into the signed-in user's own library.
async fn shared_copy(State(app): Shared, headers: HeaderMap, method: Method, UrlPath(tok): UrlPath<String>) -> Out {
    let (uid, _) = signed_in(&app, &headers, &method)?;
    let mut con = open(&app.data)?;
    let row = shared_row(&con, &tok)?;
    let (eid, stamp) = (token(9), now());
    let images = rows(&con, "SELECT id, ext FROM images WHERE entry_id=? ORDER BY created", [text(&row, "id")])?;
    let dir = app.data.join("images");
    std::fs::create_dir_all(&dir)?;
    let tx = con.transaction()?;
    tx.execute("INSERT INTO entries(id, owner, kind, title, data, portrait, created, updated) VALUES(?,?,?,?,?,?,?,?)", params![eid, uid, text(&row, "kind"), text(&row, "title"), text(&row, "data"), Option::<String>::None, stamp, stamp])?;
    for img in images {
        let (id, ext) = (text(&img, "id"), text(&img, "ext"));
        let src = dir.join(format!("{id}.{ext}"));
        if !src.exists() {
            continue;
        }
        let new_id = token(12);
        std::fs::copy(&src, dir.join(format!("{new_id}.{ext}")))?;
        tx.execute("INSERT INTO images VALUES(?,?,?,?,?)", params![new_id, uid, eid, ext, stamp])?;
        if row.get("portrait").and_then(Value::as_str) == Some(id.as_str()) {
            tx.execute("UPDATE entries SET portrait=? WHERE id=?", params![new_id, eid])?;
        }
    }
    tx.commit()?;
    Ok(reply(StatusCode::CREATED, json!({"id": eid})))
}

fn html(status: StatusCode, page: String, cache: Option<&'static str>) -> Response {
    let mut r = (status, [(header::CONTENT_TYPE, "text/html; charset=utf-8")], page).into_response();
    if let Some(c) = cache {
        r.headers_mut().insert(header::CACHE_CONTROL, header::HeaderValue::from_static(c));
    }
    r
}

/// The app shell for /s/<token>, with Open Graph tags so a pasted link unfurls as a card.
async fn share_page(State(app): Shared, headers: HeaderMap, uri: Uri, UrlPath(tok): UrlPath<String>) -> Out {
    let page = read_lossy(&root("app/static/index.html"));
    let Ok(row) = shared_row(&open(&app.data)?, &tok) else {
        return Ok(html(StatusCode::NOT_FOUND, page, None));
    };
    let d: Value = serde_json::from_str(&text(&row, "data")).unwrap_or(json!({}));
    let shown = text(&row, "title");
    let title = format!("{} \u{b7} WOTR Workshop", if shown.is_empty() { "Untitled" } else { &shown });
    let kind = text(&row, "kind");
    let mut kind_title = kind.chars();
    let kind_title: String = kind_title.next().map(|c| c.to_uppercase().chain(kind_title).collect()).unwrap_or_default();
    let by = format!("by {}", text(&row, "owner_name"));
    let (ep, of, cu) = (field(&d, "epithet"), field(&d, "kindOf"), field(&d, "culture"));
    let parts: Vec<&str> = [ep.as_str(), of.as_str(), cu.as_str(), kind_title.as_str(), by.as_str()].into_iter().filter(|x| !x.is_empty()).collect();
    let desc = escape(&parts.join(" \u{b7} "));
    let url = format!("{}{}", base_url(&headers), uri.path());
    let mut tags = vec![
        format!(r#"<meta property="og:title" content="{}">"#, escape(&title)),
        format!(r#"<meta property="og:description" content="{desc}">"#),
        format!(r#"<meta name="description" content="{desc}">"#),
        r#"<meta property="og:type" content="website">"#.to_string(),
        r#"<meta property="og:site_name" content="WOTR Workshop">"#.to_string(),
        "<meta name=\"theme-color\" content=\"#cf3a2b\">".to_string(),
        format!(r#"<meta property="og:url" content="{}">"#, escape(&url)),
    ];
    let portrait = text(&row, "portrait");
    if !portrait.is_empty() {
        tags.push(format!(r#"<meta property="og:image" content="{}/img/{}">"#, escape(&url), escape(&portrait)));
        tags.push(r#"<meta name="twitter:card" content="summary_large_image">"#.to_string());
    }
    let page = page.replace("<title>WOTR Workshop</title>", &format!("<title>{}</title>\n{}", escape(&title), tags.join("\n")));
    Ok(html(StatusCode::OK, page, Some("no-cache")))
}

async fn index() -> Response {
    html(StatusCode::OK, read_lossy(&root("app/static/index.html")), Some("no-cache"))
}

fn router(app: Arc<App>) -> Router {
    Router::new()
        .route("/", get(index))
        .route("/auth/discord", get(auth_discord))
        .route("/auth/discord/callback", get(auth_discord_callback))
        .route("/auth/dev", get(auth_dev))
        .route("/auth/key", post(auth_key))
        .route("/auth/logout", get(auth_logout).post(auth_logout))
        .route("/api/me", get(me))
        .route("/api/status", get(status))
        .route("/api/canon", get(canon_route))
        .route("/api/entries", get(entries_list).post(entries_create))
        .route("/api/entries/{eid}", get(entry_get).put(entry_put).delete(entry_delete))
        .route("/api/entries/{eid}/images", get(images_list).post(images_upload))
        .route("/api/entries/{eid}/share", put(entry_share))
        .route("/api/images/{iid}", get(image_get).delete(image_delete))
        .route("/api/shared/{token}", get(shared))
        .route("/api/shared/{token}/copy", post(shared_copy))
        .route("/s/{token}", get(share_page))
        .route("/s/{token}/img/{iid}", get(shared_image))
        .route("/api/tools", get(tools))
        .route("/api/tool/{name}", post(tool))
        .nest_service("/static", tower_http::services::ServeDir::new(root("app/static")))
        .layer(DefaultBodyLimit::max(MAX_IMAGE * 2))
        .with_state(app)
}

pub async fn main(args: &[String]) -> i32 {
    let data = data_dir();
    if args.first().map(String::as_str) == Some("invite") {
        return match new_invite(&data, &args[1..].join(" ")) {
            Ok(code) => {
                println!("{code}");
                0
            }
            Err(_) => 1,
        };
    }
    let port = args.iter().position(|a| a == "--port").and_then(|i| args.get(i + 1)).and_then(|p| p.parse::<u16>().ok()).unwrap_or(8780);
    let mut dev = env("WOTR_APP_DEV").as_deref() == Some("1");
    if dev && env("WOTR_APP_URL").is_some_and(|u| u.starts_with("https")) {
        // Funnel traffic arrives from 127.0.0.1 too, so a published server never offers /auth/dev
        eprintln!("WOTR_APP_DEV ignored: WOTR_APP_URL is a public https address");
        dev = false;
    }
    if open(&data).is_err() {
        eprintln!("cannot open {}", data.join("app.db").display());
        return 1;
    }
    let app = Arc::new(App { dev, data, tools: Wotr::fixed(false, true) });
    let listener = match tokio::net::TcpListener::bind(("127.0.0.1", port)).await {
        Ok(l) => l,
        Err(e) => {
            eprintln!("127.0.0.1:{port}: {e}");
            return 1;
        }
    };
    println!("WOTR Workshop on http://127.0.0.1:{}", listener.local_addr().map_or(port, |a| a.port()));
    match axum::serve(listener, router(app).into_make_service_with_connect_info::<SocketAddr>()).await {
        Ok(()) => 0,
        Err(e) => {
            eprintln!("{e}");
            1
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn image_bytes_decide_the_type() {
        assert_eq!(image_ext(b"\x89PNG\r\n\x1a\n\0\0\0\rIHDR"), Some("png"));
        assert_eq!(image_ext(b"\xff\xd8\xff\xe0"), Some("jpg"));
        assert_eq!(image_ext(b"RIFF\0\0\0\0WEBPVP8 "), Some("webp"));
        assert_eq!(image_ext(b"GIF89a"), Some("gif"));
        for bad in [&b"<script>"[..], b"\x89PNG\r\n\x1a\n", b"RIFF\0\0\0\0WAVE", b""] {
            assert_eq!(image_ext(bad), None);
        }
    }

    #[test]
    fn token_urlsafe_lengths_match_python() {
        assert_eq!(token(9).len(), 12);
        assert_eq!(token(12).len(), 16);
        assert_eq!(token(16).len(), 22);
        assert_eq!(token(32).len(), 43);
        assert!(token(32).chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_'));
    }

    #[test]
    fn cookie_and_percent_round_trip() {
        let saved = json!({"state": "abc", "invite": "A B&C"}).to_string();
        assert_eq!(percent_decode(&quote(&saved, "", false)), saved);
        let mut h = HeaderMap::new();
        h.insert(header::COOKIE, "a=1; wotr_session=tok; b=2".parse().unwrap());
        assert_eq!(cookie(&h, COOKIE).as_deref(), Some("tok"));
        assert_eq!(cookie(&h, "none"), None);
    }
}
