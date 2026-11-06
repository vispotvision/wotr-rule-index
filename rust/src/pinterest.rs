//! Isaac's main source for how abilities look and move, as images a model can read from any client.
//! Reads Pinterest signed out through gallery-dl and ffmpeg, and saves nothing past the call.
use crate::{jobs, util};
use std::path::{Path, PathBuf};
use std::process::Stdio;

const PAGE: i64 = 24;
const MAX_FPS: i64 = 8;

fn home() -> PathBuf {
    PathBuf::from(std::env::var("HOME").unwrap_or_default())
}

/// The trust boundary: ffmpeg reads this on a public route, so nothing but Pinterest's own media hosts.
fn media_url(u: &str) -> bool {
    (u.starts_with("https://i.pinimg.com/") || u.starts_with("https://v1.pinimg.com/")) && !u.chars().any(|c| c.is_whitespace() || c.is_control())
}

fn encode(q: &str) -> String {
    q.bytes().map(|b| if b.is_ascii_alphanumeric() || b"-_.~".contains(&b) { (b as char).to_string() } else { format!("%{b:02X}") }).collect()
}

fn board_url(list: &str, name: &str) -> Option<String> {
    list.lines().find_map(|l| {
        let mut p = l.split_whitespace();
        (p.next() == Some(name)).then(|| p.next()).flatten().filter(|u| u.starts_with("https://www.pinterest.com/")).map(str::to_string)
    })
}

fn kind(u: &str) -> &str {
    let path = u.split('?').next().unwrap_or(u);
    path.rsplit('.').next().filter(|e| e.len() <= 5 && !e.contains('/')).unwrap_or("?")
}

fn ffmpeg(input: &str, filter: &str, out: &Path) -> bool {
    util::command("timeout")
        .args(["60", "ffmpeg", "-v", "error", "-y", "-protocol_whitelist", "https,tls,tcp,crypto,data", "-i", input, "-vf", filter, "-frames:v", "1"])
        .arg(out)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|s| s.success())
        && out.is_file()
}

/// One result's frames, or a still at reading size.
fn look(url: &str, fps: i64, dir: &Path) -> Result<((String, String), String), String> {
    if !media_url(url) {
        return Err("url must be an https://i.pinimg.com or v1.pinimg.com result from this tool".into());
    }
    let out = dir.join("look.jpg");
    let moving = !["jpg", "jpeg", "png", "webp"].contains(&kind(url));
    let filter = if moving { format!("fps={},scale=300:-1,tile=6x3", fps.clamp(1, MAX_FPS)) } else { "scale='min(1400,iw)':-2".to_string() };
    if !ffmpeg(url, &filter, &out) {
        return Err(format!("could not read {url}"));
    }
    let text = if moving { "Frames in order, left to right, top to bottom. A slow or long clip reads better at fps=2." } else { "A still, at reading size." };
    Ok(((jobs::b64(&std::fs::read(&out).map_err(|e| e.to_string())?), "image/jpeg".into()), text.into()))
}

/// A page of results as one numbered sheet: position on the sheet is the number in the text.
fn sheet(source: &str, start: i64, dir: &Path) -> Result<((String, String), String), String> {
    let got = util::command("timeout")
        .arg("120")
        .arg(home().join(".local/bin/gallery-dl"))
        .args(["-g", "--range", &format!("{start}-{}", start + PAGE - 1), source])
        .stdin(Stdio::null())
        .output()
        .map_err(|e| format!("gallery-dl did not run: {e}"))?;
    let listed = String::from_utf8_lossy(&got.stdout);
    let urls: Vec<&str> = listed.lines().map(|l| l.trim().trim_start_matches("ytdl:")).filter(|u| media_url(u)).collect();
    if urls.is_empty() {
        let said = String::from_utf8_lossy(&got.stderr);
        return Err(format!("no results for {source} from {start}; a login wall or bot check stays with Isaac. {}", said.lines().last().unwrap_or("")));
    }
    let frames: Vec<PathBuf> = std::thread::scope(|s| {
        let jobs: Vec<_> = urls
            .iter()
            .enumerate()
            .map(|(i, u)| {
                s.spawn(move || {
                    let f = dir.join(format!("{i:03}.jpg"));
                    ffmpeg(u, "scale=300:-1", &f).then_some(f)
                })
            })
            .collect();
        jobs.into_iter().map(|j| j.join().ok().flatten()).collect::<Vec<_>>()
    })
    .into_iter()
    .flatten()
    .collect();
    if frames.is_empty() {
        return Err(format!("{} results listed and none could be read", urls.len()));
    }
    let names = |f: &PathBuf| f.file_stem().and_then(|s| s.to_str()).and_then(|s| s.parse::<usize>().ok());
    let out = dir.join("sheet.jpg");
    let made = util::command("magick")
        .arg("montage")
        .args(&frames)
        .args(["-tile", "6x", "-geometry", "300x380+4+4", "-quality", "85"])
        .arg(&out)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .is_ok_and(|s| s.success());
    if !made {
        return Err("could not build the sheet".into());
    }
    let mut text = String::from("Read the sheet left to right, top to bottom, 6 across; the numbers below are the positions. Call again with url= for a closer look: a gif or m3u8 comes back as frames.\n");
    for (n, f) in frames.iter().enumerate() {
        if let Some(u) = names(f).and_then(|i| urls.get(i)) {
            text += &format!("{} {} {u}\n", n + 1, kind(u));
        }
    }
    if urls.len() as i64 == PAGE {
        text += &format!("More: start={}\n", start + PAGE);
    }
    Ok(((jobs::b64(&std::fs::read(&out).map_err(|e| e.to_string())?), "image/jpeg".into()), text))
}

pub fn pinterest(query: &str, board: &str, url: &str, start: i64, fps: i64) -> Result<((String, String), String), String> {
    let (query, board, url) = (query.trim(), board.trim(), url.trim());
    let dir = std::env::temp_dir().join(format!("wotr-pinterest-{}-{:?}", std::process::id(), std::thread::current().id()).replace(['(', ')'], ""));
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let done = if !url.is_empty() {
        look(url, fps, &dir)
    } else if !board.is_empty() {
        let list = std::fs::read_to_string(home().join("wotr-art-drops/boards.txt")).unwrap_or_default();
        match board_url(&list, board) {
            Some(u) => sheet(&u, start.max(1), &dir),
            None => Err(format!("no board '{board}'; boards: {}", list.lines().filter_map(|l| l.split_whitespace().next()).collect::<Vec<_>>().join(", "))),
        }
    } else if !query.is_empty() && query.len() <= 200 {
        sheet(&format!("https://www.pinterest.com/search/pins/?q={}", encode(query)), start.max(1), &dir)
    } else {
        Err("give one of query (up to 200 characters), board or url".into())
    };
    let _ = std::fs::remove_dir_all(&dir);
    done
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn only_pinterest_media_reaches_ffmpeg() {
        assert!(media_url("https://i.pinimg.com/originals/66/6a/x.gif"));
        assert!(media_url("https://v1.pinimg.com/videos/iht/hls/d2/x.m3u8"));
        for bad in [
            "file:///etc/passwd",
            "http://i.pinimg.com/x.gif",
            "https://i.pinimg.com.evil.test/x.gif",
            "https://evil.test/https://i.pinimg.com/x.gif",
            "concat:https://i.pinimg.com/a|file:///etc/passwd",
            "https://i.pinimg.com/x.gif\n-i file:///etc/passwd",
            "-i",
            "",
        ] {
            assert!(!media_url(bad), "{bad}");
        }
    }

    #[test]
    fn a_query_cannot_leave_the_search_parameter() {
        assert_eq!(encode("fire magic&x=1/é"), "fire%20magic%26x%3D1%2F%C3%A9");
    }

    #[test]
    fn boards_come_only_from_the_list() {
        let list = "wotr-weapons https://www.pinterest.com/me/wotr-weapons/\nbad file:///etc/passwd\n";
        assert_eq!(board_url(list, "wotr-weapons").as_deref(), Some("https://www.pinterest.com/me/wotr-weapons/"));
        assert_eq!(board_url(list, "bad"), None);
        assert_eq!(board_url(list, "https://www.pinterest.com/me/wotr-weapons/"), None);
    }

    #[test]
    fn kinds() {
        assert_eq!(kind("https://i.pinimg.com/a/b.gif"), "gif");
        assert_eq!(kind("https://v1.pinimg.com/a/b.m3u8?x=1"), "m3u8");
    }
}
