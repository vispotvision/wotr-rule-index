//! ComfyUI on the 9070 XT (wotr-comfy.service, 127.0.0.1:8188, loopback only): runs one of Isaac's
//! API-format workflows with a new prompt and brings the result back, saved beside chatgpt_image's
//! in ~/wotr-drafts/images so the public route's /images/ link serves it.
use crate::{jobs, util, writers};
use serde_json::{json, Map, Value};
use std::path::{Path, PathBuf};
use std::process::Stdio;
use std::time::{Duration, Instant, SystemTime};

const URL: &str = "http://127.0.0.1:8188";
const WAIT: Duration = Duration::from_secs(20 * 60);

fn workflows() -> PathBuf {
    util::env_path("WOTR_COMFY", None).unwrap_or_else(|| PathBuf::from(std::env::var("HOME").unwrap_or_default()).join("comfy/ComfyUI")).join("user/default/workflows")
}

fn curl(args: &[&str]) -> Result<Vec<u8>, String> {
    let o = util::command("curl").args(["-sS", "--max-time", "120"]).args(args).stdin(Stdio::null()).output().map_err(|e| e.to_string())?;
    if o.status.success() {
        Ok(o.stdout)
    } else {
        Err(format!("ComfyUI did not answer at {URL} ({}). Start it: systemctl --user start wotr-comfy", String::from_utf8_lossy(&o.stderr).trim()))
    }
}

fn get(path: &str) -> Result<Value, String> {
    serde_json::from_slice(&curl(&[&format!("{URL}{path}")])?).map_err(|e| e.to_string())
}

/// The API-format workflows (a UI-format file, with "nodes", cannot be queued as it is).
fn list() -> Vec<(String, Map<String, Value>)> {
    let mut v: Vec<_> = std::fs::read_dir(workflows())
        .into_iter()
        .flatten()
        .flatten()
        .filter_map(|e| {
            let p = e.path();
            let name = p.file_stem()?.to_string_lossy().to_string();
            if p.extension()? != "json" || name.starts_with('_') {
                return None;
            }
            match serde_json::from_str::<Value>(&std::fs::read_to_string(&p).ok()?).ok()? {
                Value::Object(m) if !m.contains_key("nodes") => Some((name, m)),
                _ => None,
            }
        })
        .collect();
    v.sort_by(|a, b| a.0.cmp(&b.0));
    v
}

/// The text encoder wired into the graph's `input` (positive or negative), wherever that input sits.
fn encoder(wf: &Map<String, Value>, input: &str) -> Option<String> {
    wf.values()
        .filter_map(|n| n["inputs"].get(input)?.get(0)?.as_str())
        .find(|id| wf.get(*id).and_then(|t| t["class_type"].as_str()).is_some_and(|c| c.contains("TextEncode")))
        .map(str::to_string)
}

/// Put the call's prompt, size, seed and input image into the graph.
fn fill(wf: &mut Map<String, Value>, prompt: &str, negative: &str, w: i64, h: i64, seed: i64, image: Option<&str>) -> Result<(), String> {
    // a house-style workflow keeps its tag block and marks the subject's place with {prompt} / {negative}
    for (input, text, slot) in [("positive", prompt, "{prompt}"), ("negative", negative, "{negative}")] {
        let Some(id) = encoder(wf, input) else {
            if text.is_empty() {
                continue;
            }
            return Err(format!("this workflow has no text encoder on its {input} input"));
        };
        let t = &mut wf[&id]["inputs"]["text"];
        match t.as_str() {
            Some(s) if s.contains(slot) => *t = json!(if text.is_empty() { s.replace(&format!("{slot}, "), "").replace(slot, "") } else { s.replace(slot, text) }),
            _ if !text.is_empty() => *t = json!(text),
            _ => {}
        }
    }
    let mut loaded = false;
    for n in wf.values_mut().filter_map(|n| n["inputs"].as_object_mut()) {
        for (k, v) in [("width", w), ("height", h)] {
            if v > 0 && n.get(k).is_some_and(Value::is_number) {
                n[k] = json!(v);
            }
        }
        for k in ["seed", "noise_seed"] {
            if n.get(k).is_some_and(Value::is_number) {
                n[k] = json!(seed);
            }
        }
    }
    for n in wf.values_mut().filter(|n| n["class_type"] == "LoadImage") {
        // shortcut: one image fills the first LoadImage only; a mask workflow needs its mask placed by hand
        if let (Some(img), false) = (image, loaded) {
            n["inputs"]["image"] = json!(img);
            loaded = true;
        }
    }
    if !loaded && image.is_none() && wf.values().any(|n| n["class_type"] == "LoadImage") {
        return Err("this workflow starts from an image: pass image (a png, jpg or webp path on this machine)".into());
    }
    Ok(())
}

fn upload(path: &str) -> Result<String, String> {
    let p = Path::new(path);
    let ext = p.extension().map(|e| e.to_string_lossy().to_lowercase()).unwrap_or_default();
    if !["png", "jpg", "jpeg", "webp"].contains(&ext.as_str()) || !p.is_file() {
        return Err(format!("image must be an existing png, jpg or webp file: {path}"));
    }
    let r: Value = serde_json::from_slice(&curl(&["-F", &format!("image=@{}", p.display()), "-F", "overwrite=true", &format!("{URL}/upload/image")])?).map_err(|e| e.to_string())?;
    r["name"].as_str().map(str::to_string).ok_or_else(|| format!("upload refused: {r}"))
}

/// A preview the model can read: a still at ~1024 px, or a video as a strip of frames.
fn preview(out: &Path) -> Option<(String, String)> {
    let video = out.extension().is_some_and(|e| ["webm", "mp4", "gif"].contains(&e.to_string_lossy().as_ref()));
    let o = if video {
        util::command("ffmpeg").args(["-v", "error", "-i"]).arg(out).args(["-vf", "fps=6,scale=320:-1,tile=4x3", "-frames:v", "1", "-f", "image2pipe", "-c:v", "mjpeg", "-"]).stdin(Stdio::null()).output()
    } else {
        util::command("magick").arg(out).args(["-resize", "1024x1024>", "-quality", "85", "jpg:-"]).stdin(Stdio::null()).output()
    };
    o.ok().filter(|o| !o.stdout.is_empty()).map(|o| (jobs::b64(&o.stdout), "image/jpeg".to_string()))
}

#[allow(clippy::too_many_arguments)]
pub fn comfy(workflow: &str, prompt: &str, negative: &str, image: &str, w: i64, h: i64, seed: i64, name: &str, public: Option<&(String, String)>) -> Result<(Option<(String, String)>, String), String> {
    let all = list();
    let Some(mut wf) = all.iter().find(|(n, _)| n == workflow).map(|(_, m)| m.clone()) else {
        let names: Vec<_> = all.iter().map(|(n, _)| n.as_str()).collect();
        return Ok((None, format!("workflows in {}: {}", workflows().display(), names.join(", "))));
    };
    let seed = if seed >= 0 { seed } else { (SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_nanos() % (1 << 48)) as i64 };
    let img = if image.is_empty() { None } else { Some(upload(image)?) };
    fill(&mut wf, prompt, negative, w, h, seed, img.as_deref())?;

    let start = Instant::now();
    let body = json!({"prompt": wf, "client_id": "wotr-mcp"}).to_string();
    let r: Value = serde_json::from_slice(&curl(&["-H", "Content-Type: application/json", "--data-binary", &body, &format!("{URL}/prompt")])?).map_err(|e| e.to_string())?;
    let id = r["prompt_id"].as_str().ok_or_else(|| format!("ComfyUI refused the graph: {}", util::head(&r.to_string(), 1500)))?.to_string();
    let done = loop {
        let h = get(&format!("/history/{id}"))?;
        if let Some(e) = h.get(&id) {
            break e.clone();
        }
        if start.elapsed() > WAIT {
            return Err(format!("still rendering after {} min; it keeps going in ComfyUI (prompt {id})", WAIT.as_secs() / 60));
        }
        std::thread::sleep(Duration::from_secs(1));
    };
    if done["status"]["status_str"] != "success" {
        return Err(format!("the render failed: {}", util::head(&done["status"]["messages"].to_string(), 1500)));
    }

    let dir = PathBuf::from(std::env::var("HOME").unwrap_or_default()).join("wotr-drafts/images");
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let stem = format!("{}-{}", writers::date_fmt("%Y%m%d-%H%M%S"), util::head(&writers::slug_us(if name.is_empty() { workflow } else { name }), 40));
    let mut saved = Vec::new();
    for f in done["outputs"].as_object().into_iter().flat_map(|o| o.values()).filter_map(|o| o.as_object()).flat_map(|o| o.values()).filter_map(Value::as_array).flatten() {
        let (Some(file), Some("output")) = (f["filename"].as_str(), f["type"].as_str()) else { continue };
        let ext = Path::new(file).extension().map(|e| e.to_string_lossy().to_lowercase()).unwrap_or_default();
        let out = dir.join(format!("{stem}{}.{ext}", if saved.is_empty() { String::new() } else { format!("-{}", saved.len() + 1) }));
        let q = |s: &str| util::quote(s, "", false);
        let data = curl(&[&format!("{URL}/view?filename={}&subfolder={}&type=output", q(file), q(f["subfolder"].as_str().unwrap_or("")))])?;
        std::fs::write(&out, data).map_err(|e| e.to_string())?;
        saved.push(out);
    }
    let Some(first) = saved.first() else { return Ok((None, format!("the render finished with no saved output (prompt {id})"))) };
    let mut text = format!("{workflow}, seed {seed}, {:.0} s", start.elapsed().as_secs_f64());
    for p in &saved {
        text += &format!("\nsaved {}", p.display());
        if let Some((b, t)) = public.filter(|(b, t)| !b.is_empty() && !t.is_empty()) {
            text += &format!("\nlink: {b}/t/{t}/images/{}", util::quote(&p.file_name().unwrap().to_string_lossy(), "", false));
        }
    }
    Ok((preview(first), text))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn fill_reaches_the_wired_encoders() {
        // the Wan shape: the encoders feed a conditioning node, not the sampler
        let mut wf = json!({
            "5": {"class_type": "CLIPTextEncode", "inputs": {"text": "old"}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "bad"}},
            "7": {"class_type": "WanImageToVideo", "inputs": {"positive": ["5", 0], "negative": ["6", 0], "width": 512, "height": 288}},
            "8": {"class_type": "KSampler", "inputs": {"positive": ["7", 0], "negative": ["7", 1], "seed": 1}},
        });
        let m = wf.as_object_mut().unwrap();
        fill(m, "new", "", 1024, 0, 99, None).unwrap();
        assert_eq!(m["5"]["inputs"]["text"], "new");
        assert_eq!(m["6"]["inputs"]["text"], "bad");
        assert_eq!(m["7"]["inputs"]["width"], 1024);
        assert_eq!(m["7"]["inputs"]["height"], 288);
        assert_eq!(m["8"]["inputs"]["seed"], 99);
        let mut styled = json!({
            "1": {"class_type": "CLIPTextEncode", "inputs": {"text": "best quality, {prompt}, manga"}},
            "2": {"class_type": "CLIPTextEncode", "inputs": {"text": "{negative}, lowres"}},
            "3": {"class_type": "KSampler", "inputs": {"positive": ["1", 0], "negative": ["2", 0]}},
        });
        let m = styled.as_object_mut().unwrap();
        fill(m, "1boy, red armor", "", 0, 0, 1, None).unwrap();
        assert_eq!(m["1"]["inputs"]["text"], "best quality, 1boy, red armor, manga");
        assert_eq!(m["2"]["inputs"]["text"], "lowres");
        let mut needs = json!({"1": {"class_type": "LoadImage", "inputs": {"image": "x.png"}}});
        assert!(fill(needs.as_object_mut().unwrap(), "", "", 0, 0, 1, None).is_err());
        fill(needs.as_object_mut().unwrap(), "", "", 0, 0, 1, Some("y.png")).unwrap();
        assert_eq!(needs["1"]["inputs"]["image"], "y.png");
    }
}
