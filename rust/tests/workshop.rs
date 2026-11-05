//! The Workshop's trust boundaries, through the real binary: sign-in required, write header required,
//! each user sees only their own entries and images, uploads must be real images, dev sign-in only
//! when enabled, key sign-in, sharing, and Discord sign-in against a stub.
use std::io::{BufRead, BufReader, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::time::Duration;

struct Server {
    port: u16,
    child: Child,
    data: PathBuf,
}

impl Drop for Server {
    fn drop(&mut self) {
        let _ = self.child.kill();
        let _ = self.child.wait();
        let _ = std::fs::remove_dir_all(&self.data);
    }
}

fn start(name: &str, extra: &[(&str, &str)]) -> Server {
    let data = std::env::temp_dir().join(format!("wotr-workshop-{name}-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&data);
    let mut c = Command::new(env!("CARGO_BIN_EXE_wotr-mcp"));
    c.args(["workshop", "--port", "0"]).env("WOTR_APP_DATA", &data).env("WOTR_ENV_FILE", "/nonexistent").env_remove("WOTR_APP_URL").env_remove("DISCORD_CLIENT_ID").stdout(Stdio::piped());
    for (k, v) in extra {
        c.env(k, v);
    }
    // the kernel picks the port and the server says which, so parallel tests never share one
    let mut child = c.spawn().unwrap();
    let mut line = String::new();
    BufReader::new(child.stdout.take().unwrap()).read_line(&mut line).unwrap();
    let port = line.trim().rsplit(':').next().unwrap().parse().unwrap_or_else(|_| panic!("the server did not start: {line:?}"));
    Server { port, child, data }
}

struct Res {
    status: u16,
    head: String,
    body: Vec<u8>,
}

impl Res {
    fn json(&self) -> serde_json::Value {
        serde_json::from_slice(&self.body).unwrap_or_else(|e| panic!("{e}: {}", self.text()))
    }
    fn text(&self) -> String {
        String::from_utf8_lossy(&self.body).into_owned()
    }
}

/// One HTTP request; a client is a port and the session cookie it holds.
#[derive(Clone)]
struct Client {
    port: u16,
    cookie: String,
}

impl Client {
    fn new(s: &Server) -> Self {
        Client { port: s.port, cookie: String::new() }
    }

    fn raw(&mut self, method: &str, path: &str, headers: &str, body: &[u8]) -> Res {
        let mut t = TcpStream::connect(("127.0.0.1", self.port)).unwrap();
        let mut req = format!("{method} {path} HTTP/1.1\r\nHost: 127.0.0.1:{}\r\nConnection: close\r\nContent-Length: {}\r\n{headers}", self.port, body.len());
        if !self.cookie.is_empty() {
            req += &format!("Cookie: {}\r\n", self.cookie);
        }
        req += "\r\n";
        t.write_all(req.as_bytes()).unwrap();
        t.write_all(body).unwrap();
        let mut all = Vec::new();
        t.read_to_end(&mut all).unwrap();
        let split = all.windows(4).position(|w| w == b"\r\n\r\n").expect("a response");
        let head = String::from_utf8_lossy(&all[..split]).into_owned();
        let status = head.split_whitespace().nth(1).unwrap().parse().unwrap();
        for line in head.lines() {
            if let Some(v) = line.strip_prefix("set-cookie: ").filter(|v| v.starts_with("wotr_")) {
                let pair = v.split(';').next().unwrap();
                if pair.starts_with("wotr_session=") {
                    self.cookie = pair.to_string();
                }
            }
        }
        Res { status, head, body: all[split + 4..].to_vec() }
    }

    fn get(&mut self, path: &str) -> Res {
        self.raw("GET", path, "", b"")
    }

    fn write(&mut self, method: &str, path: &str, body: &str) -> Res {
        self.raw(method, path, "Content-Type: application/json\r\nX-WOTR: 1\r\n", body.as_bytes())
    }

    fn upload(&mut self, path: &str, file: &[u8], header: bool) -> Res {
        let mut body = b"--BOUND\r\nContent-Disposition: form-data; name=\"file\"; filename=\"x.png\"\r\nContent-Type: image/png\r\n\r\n".to_vec();
        body.extend_from_slice(file);
        body.extend_from_slice(b"\r\n--BOUND--\r\n");
        let write = if header { "X-WOTR: 1\r\n" } else { "" };
        self.raw("POST", path, &format!("Content-Type: multipart/form-data; boundary=BOUND\r\n{write}"), &body)
    }
}

const PNG: &[u8] = b"\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\0\x08\0\0\0\x08\x08\x02\0\0\0";

fn dev(s: &Server, name: &str) -> Client {
    let mut c = Client::new(s);
    assert_eq!(c.get(&format!("/auth/dev?name={name}")).status, 303);
    assert!(!c.cookie.is_empty());
    c
}

fn id(v: &serde_json::Value) -> String {
    v["id"].as_str().unwrap().to_string()
}

fn invite(s: &Server, note: &str) -> String {
    let o = Command::new(env!("CARGO_BIN_EXE_wotr-mcp")).args(["workshop", "invite", note]).env("WOTR_APP_DATA", &s.data).env("WOTR_ENV_FILE", "/nonexistent").output().unwrap();
    String::from_utf8_lossy(&o.stdout).trim().to_string()
}

#[test]
fn entries_images_and_tools_are_private_to_their_owner() {
    let s = start("own", &[("WOTR_APP_DEV", "1")]);
    let mut anon = Client::new(&s);
    assert_eq!(anon.get("/api/entries").status, 401);
    assert_eq!(anon.get("/api/canon").json()["stages"][0]["name"], "Murmuring");
    assert_eq!(anon.get("/api/status").json()["dev"], true);

    let (mut a, mut b) = (dev(&s, "A"), dev(&s, "B"));
    let no_header = a.raw("POST", "/api/entries", "Content-Type: application/json\r\n", br#"{"kind":"character"}"#);
    assert_eq!(no_header.status, 403);
    assert_eq!(a.write("POST", "/api/entries", r#"{"kind":"spell"}"#).status, 400);
    let made = a.write("POST", "/api/entries", r##"{"kind":"character","title":"Naiser","data":{"aura":"#e8b04b"}}"##);
    assert_eq!(made.status, 201);
    let e = made.json();
    assert!(e.get("owner").is_none());
    let path = format!("/api/entries/{}", id(&e));
    assert_eq!(a.write("PUT", &path, r#"{"title":"Naiser","data":{"stage":"IV"}}"#).json()["data"], serde_json::json!({"stage": "IV"}));
    assert_eq!(b.get(&path).status, 404);
    assert_eq!(b.write("PUT", &path, r#"{"data":{}}"#).status, 404);
    assert_eq!(b.get("/api/entries").json(), serde_json::json!([]));
    assert_eq!(a.get("/api/entries").json()[0]["title"], "Naiser");

    assert_eq!(a.upload(&format!("{path}/images"), PNG, false).status, 403);
    let up = a.upload(&format!("{path}/images"), PNG, true);
    assert_eq!(up.status, 201, "{}", up.text());
    let iid = id(&up.json());
    assert_eq!(a.get(&path).json()["portrait"].as_str(), Some(iid.as_str()));
    let img = a.get(&format!("/api/images/{iid}"));
    assert_eq!(img.status, 200);
    assert!(img.head.contains("image/png") && img.body == PNG);
    assert_eq!(b.get(&format!("/api/images/{iid}")).status, 404);
    assert_eq!(a.upload(&format!("{path}/images"), b"<script>", true).status, 400);
    let f = b.write("POST", "/api/entries", r#"{"kind":"item"}"#).json();
    assert_eq!(b.write("PUT", &format!("/api/entries/{}", id(&f)), &format!(r#"{{"data":{{}},"portrait":"{iid}"}}"#)).status, 400); // A's image

    assert!(a.write("POST", "/api/tool/skill", r#"{"name":"wotr-name"}"#).json()["text"].as_str().unwrap().starts_with("(Served by the WOTR MCP."));
    assert_eq!(a.write("POST", "/api/tool/archive_scene", "{}").json()["error"], true); // writers are not exposed
    assert_eq!(a.write("POST", "/api/tool/skill", "[]").status, 400);
    let tools = a.get("/api/tools").json();
    let names: Vec<&str> = tools.as_array().unwrap().iter().map(|t| t["name"].as_str().unwrap()).collect();
    assert!(names.contains(&"load_rules") && !names.contains(&"archive_scene") && tools[0].get("input_schema").is_some(), "{names:?}");

    assert_eq!(a.raw("DELETE", &path, "X-WOTR: 1\r\n", b"").status, 200);
    assert!(!s.data.join("images").join(format!("{iid}.png")).exists());
    assert_eq!(a.get(&path).status, 404);

}

#[test]
fn dev_sign_in_is_off_unless_enabled_and_never_on_a_public_address() {
    let off = start("off", &[]);
    assert_eq!(Client::new(&off).get("/auth/dev?name=X").status, 404);
    let public = start("public", &[("WOTR_APP_DEV", "1"), ("WOTR_APP_URL", "https://example.test:10000")]);
    assert_eq!(Client::new(&public).get("/auth/dev?name=X").status, 404);
}

#[test]
fn logging_out_ends_the_session() {
    let s = start("logout", &[("WOTR_APP_DEV", "1")]);
    let mut a = dev(&s, "A");
    let held = a.cookie.clone();
    assert_eq!(a.get("/api/me").status, 200);
    assert_eq!(a.raw("POST", "/auth/logout", "", b"").status, 303);
    let mut again = Client { port: s.port, cookie: held };
    assert_eq!(again.get("/api/me").status, 401);
}

#[test]
fn an_invite_becomes_the_holders_key() {
    let s = start("keys", &[]);
    let k = invite(&s, "test");
    assert_eq!(k.len(), 19, "{k}");
    let mut c = Client::new(&s);
    let body = |x: &str| format!(r#"{{"key":"{x}"}}"#);
    assert_eq!(c.write("POST", "/auth/key", &body(&k)).json()["need_name"], true);
    assert_eq!(c.write("POST", "/auth/key", &format!(r#"{{"key":"{k}","name":"Kei"}}"#)).status, 200);
    assert_eq!(c.get("/api/me").json()["name"], "Kei");
    let mut c2 = Client::new(&s);
    assert_eq!(c2.write("POST", "/auth/key", &body(&k.to_lowercase())).status, 200);
    assert_eq!(c2.get("/api/me").json()["name"], "Kei");
    assert_eq!(c2.write("POST", "/auth/key", &body("0000-0000-0000-0000")).status, 401);
    assert_eq!(c2.raw("POST", "/auth/key", "Content-Type: application/json\r\n", body(&k).as_bytes()).status, 403);
}

#[test]
fn a_share_link_shows_only_its_entry_and_can_be_turned_off() {
    let s = start("share", &[("WOTR_APP_DEV", "1")]);
    let (mut a, mut b, mut anon) = (dev(&s, "SharerA"), dev(&s, "B"), Client::new(&s));
    let e = a.write("POST", "/api/entries", r#"{"kind":"character","title":"Ka<b>ito","data":{"epithet":"the Ember"}}"#).json();
    let path = format!("/api/entries/{}", id(&e));
    let iid = id(&a.upload(&format!("{path}/images"), PNG, true).json());
    let other = a.write("POST", "/api/entries", r#"{"kind":"lore","title":"secret"}"#).json();
    let secret = id(&a.upload(&format!("/api/entries/{}/images", id(&other)), PNG, true).json());
    assert_eq!(anon.get("/api/shared/nope").status, 404);
    let tok = a.write("PUT", &format!("{path}/share"), r#"{"on":true}"#).json()["share"].as_str().unwrap().to_string();
    assert_eq!(a.write("PUT", &format!("{path}/share"), r#"{"on":true}"#).json()["share"].as_str(), Some(tok.as_str())); // stable
    assert_eq!(b.write("PUT", &format!("{path}/share"), r#"{"on":true}"#).status, 404); // not B's
    let public = anon.get(&format!("/api/shared/{tok}")).json();
    assert_eq!(public["title"], "Ka<b>ito");
    assert_eq!(public["owner"], "SharerA");
    assert_eq!(public["images"], serde_json::json!([iid]));
    assert!(public["data"].get("owner").is_none());
    assert_eq!(anon.get(&format!("/s/{tok}/img/{iid}")).status, 200);
    assert_eq!(anon.get(&format!("/s/{tok}/img/{secret}")).status, 404); // not this entry's
    let page = anon.get(&format!("/s/{tok}")).text();
    assert!(page.contains("og:title\" content=\"Ka&lt;b&gt;ito \u{b7} WOTR Workshop\"") && page.contains("og:image") && !page.contains("<b>ito"), "{page}");
    assert!(page.contains("the Ember \u{b7} Character \u{b7} by SharerA"), "{page}");
    assert_eq!(anon.write("POST", &format!("/api/shared/{tok}/copy"), "").status, 401);
    let copy = id(&b.write("POST", &format!("/api/shared/{tok}/copy"), "").json());
    let mine = b.get(&format!("/api/entries/{copy}")).json();
    assert_eq!(mine["title"], "Ka<b>ito");
    let portrait = mine["portrait"].as_str().unwrap().to_string();
    assert_ne!(portrait, iid);
    assert!(mine["share"].is_null());
    assert_eq!(b.get(&format!("/api/images/{portrait}")).status, 200);
    assert!(a.write("PUT", &format!("{path}/share"), r#"{"on":false}"#).json()["share"].is_null());
    assert_eq!(anon.get(&format!("/api/shared/{tok}")).status, 404);
    assert_eq!(anon.get(&format!("/s/{tok}/img/{iid}")).status, 404);
    assert_eq!(anon.get(&format!("/s/{tok}")).status, 404);
}

/// Answers the two Discord calls once each, then stops.
fn stub_discord(l: TcpListener) -> std::thread::JoinHandle<Vec<String>> {
    std::thread::spawn(move || {
        let mut seen = Vec::new();
        for reply in [r#"{"access_token":"tok123"}"#, r#"{"id":"42","username":"kei","global_name":"Kei","avatar":"abc"}"#] {
            let (mut t, _) = l.accept().unwrap();
            t.set_read_timeout(Some(Duration::from_millis(300))).unwrap();
            let mut buf = [0u8; 4096];
            let mut got = Vec::new();
            while let Ok(n) = t.read(&mut buf) {
                if n == 0 {
                    break;
                }
                got.extend_from_slice(&buf[..n]);
            }
            seen.push(String::from_utf8_lossy(&got).into_owned());
            write!(t, "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{reply}", reply.len()).unwrap();
        }
        seen
    })
}

#[test]
fn discord_sign_in_checks_state_and_needs_an_invite() {
    let stub = TcpListener::bind("127.0.0.1:0").unwrap();
    let api = format!("http://127.0.0.1:{}", stub.local_addr().unwrap().port());
    let s = start("oauth", &[("DISCORD_CLIENT_ID", "cid"), ("DISCORD_CLIENT_SECRET", "shh"), ("WOTR_DISCORD_API", &api)]);
    let mut c = Client::new(&s);
    let bad = c.get("/auth/discord/callback?state=x&code=y");
    assert_eq!(bad.status, 303);
    assert!(bad.head.contains("error=state"), "{}", bad.head);

    let k = invite(&s, "oauth");
    let go = c.get(&format!("/auth/discord?invite={k}"));
    assert_eq!(go.status, 307);
    assert!(go.head.contains("client_id=cid") && go.head.contains("scope=identify"), "{}", go.head);
    let state = go.head.split("state=").nth(1).unwrap().split('&').next().unwrap().to_string();
    let oauth = go.head.lines().find_map(|l| l.strip_prefix("set-cookie: wotr_oauth=")).unwrap().split(';').next().unwrap().to_string();

    let calls = stub_discord(stub);
    let mut back = Client { port: s.port, cookie: format!("wotr_oauth={oauth}") };
    let done = back.get(&format!("/auth/discord/callback?state={state}&code=thecode"));
    assert_eq!(done.status, 303, "{}", done.head);
    assert!(!done.head.contains("error="), "{}", done.head);
    let seen = calls.join().unwrap();
    assert!(seen[0].starts_with("POST /oauth2/token") && seen[0].contains("code=thecode") && seen[0].contains("client_secret=shh"), "{}", seen[0]);
    assert!(seen[1].starts_with("GET /users/@me") && seen[1].contains("Bearer tok123"), "{}", seen[1]);
    let who = back.get("/api/me").json();
    assert_eq!(who["name"], "Kei");
    assert_eq!(who["avatar"], "https://cdn.discordapp.com/avatars/42/abc.png");
}

#[test]
fn the_app_shell_and_static_files_are_served() {
    let s = start("static", &[]);
    let mut c = Client::new(&s);
    let index = c.get("/");
    assert_eq!(index.status, 200);
    assert!(index.head.to_lowercase().contains("cache-control: no-cache") && index.text().contains("WOTR Workshop"));
    assert_eq!(c.get("/static/app.css").status, 200);
    assert_eq!(c.get("/static/../server.py").status, 404);
}
