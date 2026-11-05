//! Mermaid charts, redrawn as the site's own art. The vault keeps the mermaid source (Obsidian draws
//! it). A chain of steps becomes an illuminated road, a timeline era bands on the same spine, and
//! anything branching SVG plaques and gilt connectors, laid out by Graphviz (dot).
use crate::art::{crest, style_for, GOLD, INK};
use crate::py::{escape, from_str_seed, sha8};
use crate::text::{caps, group, split, sub};
use crate::re;
use serde_json::Value;
use std::collections::{HashMap, HashSet};
use std::fmt::Write as _;
use std::io::Write as _;
use std::process::{Command, Stdio};

const TEXT: &str = "#f1e4c6";
const MUTED: &str = "#b9a583";
const SERIF: &str = "'Cormorant Garamond', Garamond, Georgia, serif";
const BODY: &str = "'Crimson Pro', Georgia, serif";

const NODE: &str = r#"^\s*([\w-]+)\s*(?:(\[\[|\[\(|\(\[|\(\(|\{\{|\[|\(|\{|>)\s*(?:"((?:[^"\\]|\\.)*)"|([^\]\)\}"]*))\s*(?:\]\]|\)\]|\]\)|\)\)|\}\}|\]|\)|\}))?"#;
const LINK: &str = r#"^\s*(-\.->|-\.-|==>|-->|---)\s*(?:\|"?([^|"]*)"?\|)?"#;

fn clean(s: &str) -> Vec<String> {
    let s = s.replace("#quot;", "\"");
    let s = sub(re!(r"\*\*|__|`"), &s, |_| String::new());
    split(re!(r"<br\s*/?>|\\n"), &s).into_iter().map(|l| l.trim().to_string()).filter(|l| !l.is_empty()).collect()
}

struct Group {
    title: String,
    members: Vec<String>,
    parent: Option<usize>,
}

#[derive(Default)]
struct Flow {
    dir: String,
    nodes: HashMap<String, Vec<String>>,
    order: Vec<String>,
    edges: Vec<(String, String, String, &'static str)>,
    groups: Vec<Group>,
}

enum Chart {
    Timeline(String, Vec<(String, Vec<String>)>),
    Flow(Flow),
}

fn parse(src: &str) -> Result<Chart, String> {
    let lines: Vec<&str> = src.trim().lines().map(str::trim).filter(|l| !l.is_empty() && !l.starts_with("%%")).collect();
    let first = lines.first().ok_or("an empty chart")?;
    let head: Vec<&str> = first.split_whitespace().collect();
    if head[0] == "timeline" {
        let (mut title, mut sections) = (String::new(), Vec::<(String, Vec<String>)>::new());
        for l in &lines[1..] {
            if let Some(t) = l.strip_prefix("title ") {
                title = t.trim().to_string();
            } else if let Some(s) = l.strip_prefix("section ") {
                sections.push((s.trim().to_string(), Vec::new()));
            } else {
                if sections.is_empty() {
                    sections.push((String::new(), Vec::new()));
                }
                let parts = l.split(" : ").map(str::trim).filter(|p| !p.is_empty()).map(String::from);
                sections.last_mut().unwrap().1.extend(parts);
            }
        }
        return Ok(Chart::Timeline(title, sections));
    }
    let mut g = Flow { dir: head.get(1).unwrap_or(&"TD").to_uppercase(), ..Default::default() };
    let mut stack: Vec<usize> = Vec::new();
    for l in &lines[1..] {
        let current = stack.last().copied();
        if ["classDef", "class ", "style ", "linkStyle", "click", "direction"].iter().any(|p| l.starts_with(p)) {
            continue;
        }
        if l.starts_with("subgraph") {
            let m = caps(re!(r#"^subgraph\s+([\w-]+)?\s*(?:\[\s*"?([^"\]]*)"?\s*\])?\s*(.*)"#), l).ok_or("an unreadable subgraph")?;
            let name = [group(&m, 2), group(&m, 3), group(&m, 1)].into_iter().find(|s| !s.is_empty()).unwrap_or("");
            g.groups.push(Group { title: name.trim().trim_matches('"').to_string(), members: Vec::new(), parent: current });
            stack.push(g.groups.len() - 1);
            continue;
        }
        if *l == "end" {
            stack.pop();
            continue;
        }
        let (mut pos, mut chain, mut links): (usize, Vec<Vec<String>>, Vec<(String, String)>) = (0, Vec::new(), Vec::new());
        while pos < l.len() {
            let mut ids = Vec::new();
            loop {
                let Some(m) = caps(re!(NODE), &l[pos..]) else { break };
                let id = group(&m, 1).to_string();
                let label = m.get(3).or(m.get(4)).map(|x| x.as_str());
                if !g.nodes.contains_key(&id) {
                    let cleaned = clean(label.unwrap_or(""));
                    g.nodes.insert(id.clone(), if cleaned.is_empty() { vec![id.clone()] } else { cleaned });
                    g.order.push(id.clone());
                } else if let Some(t) = label.filter(|t| !t.is_empty()) {
                    g.nodes.insert(id.clone(), clean(t));
                }
                if let Some(k) = current {
                    if !g.groups[k].members.contains(&id) {
                        g.groups[k].members.push(id.clone());
                    }
                }
                ids.push(id);
                pos += m.get(0).unwrap().end();
                let Some(a) = caps(re!(r"^\s*&"), &l[pos..]) else { break };
                pos += a.get(0).unwrap().end();
            }
            if ids.is_empty() {
                break;
            }
            chain.push(ids);
            let Some(m) = caps(re!(LINK), &l[pos..]) else { break };
            links.push((group(&m, 1).to_string(), clean(group(&m, 2)).join(" ")));
            pos += m.get(0).unwrap().end();
        }
        for (pair, (kind, lab)) in chain.windows(2).zip(&links) {
            for x in &pair[0] {
                for y in &pair[1] {
                    let style = if kind.contains('.') {
                        "dash"
                    } else if kind == "---" {
                        "none"
                    } else {
                        "arrow"
                    };
                    g.edges.push((x.clone(), y.clone(), lab.clone(), style));
                }
            }
        }
    }
    Ok(Chart::Flow(g))
}

fn chain_of(g: &Flow) -> Option<Vec<String>> {
    if !g.groups.is_empty() || g.nodes.len() < 4 || g.edges.len() != g.nodes.len() - 1 {
        return None;
    }
    let (mut next, mut ins): (HashMap<&str, &str>, HashSet<&str>) = (HashMap::new(), HashSet::new());
    for (a, b, _, _) in &g.edges {
        if next.contains_key(a.as_str()) || ins.contains(b.as_str()) {
            return None;
        }
        next.insert(a, b);
        ins.insert(b);
    }
    let starts: Vec<&String> = g.order.iter().filter(|n| !ins.contains(n.as_str())).collect();
    if starts.len() != 1 {
        return None;
    }
    let (mut seq, mut n): (Vec<String>, Option<&str>) = (Vec::new(), Some(starts[0]));
    while let Some(id) = n.filter(|i| !seq.iter().any(|s| s == i)) {
        seq.push(id.to_string());
        n = next.get(id).copied();
    }
    (seq.len() == g.nodes.len()).then_some(seq)
}

fn road(g: &Flow, seq: &[String]) -> Result<String, String> {
    let mut out = String::from(r#"<ol class="wotr-road">"#);
    let mut via: HashMap<&str, &str> = HashMap::new();
    for (_, b, lab, _) in &g.edges {
        if !lab.is_empty() {
            via.insert(b, lab);
        }
    }
    for (i, id) in seq.iter().enumerate() {
        let lines = &g.nodes[id];
        let first = lines.first().ok_or("a node with no text")?;
        let m = caps(re!(r"^((?:\d+|[IVXL]+))\s*(?:·|\.|:)?\s+(.+)$"), first);
        let (num, title) = m.as_ref().map_or(((i + 1).to_string(), first.as_str()), |c| (group(c, 1).to_string(), group(c, 2)));
        let mut rest = String::new();
        if let Some(v) = via.get(id.as_str()) {
            let _ = write!(rest, r#"<span class="rv">{}</span>"#, escape(v));
        }
        for s in &lines[1..] {
            let _ = write!(rest, r#"<span class="rs">{}</span>"#, escape(s));
        }
        let _ = write!(out, r#"<li><span class="rn">{}</span><div class="rc"><span class="rt">{}</span>{rest}</div></li>"#, escape(&num), escape(title));
    }
    out.push_str("</ol>");
    Ok(out)
}

fn timeline(title: &str, sections: &[(String, Vec<String>)]) -> String {
    let mut out = String::from(r#"<div class="wotr-era">"#);
    if !title.is_empty() {
        let _ = write!(out, r#"<div class="et">{}</div>"#, escape(title));
    }
    out.push_str(r#"<ol class="wotr-road wotr-road-era">"#);
    for (i, (name, events)) in sections.iter().enumerate() {
        let m = caps(re!(r"^(.*?)\s*\(([^)]*)\)\s*$"), name);
        let (nm, span) = m.as_ref().map_or((name.as_str(), ""), |c| (group(c, 1), group(c, 2)));
        let ev: String = events.iter().map(|e| format!(r#"<span class="ev">{}</span>"#, escape(e))).collect();
        let dated = if span.is_empty() { String::new() } else { format!(r#"<span class="rd">{}</span>"#, escape(span)) };
        let _ = write!(out, r#"<li><span class="rn">{}</span><div class="rc"><span class="rt">{}</span>{dated}<span class="evs">{ev}</span></div></li>"#, i + 1, escape(nm));
    }
    out.push_str("</ol></div>");
    out
}

/// A node's size and its lines wrapped: (line index, text).
fn measure(lines: &[String]) -> Result<(f64, f64, Vec<(usize, String)>), String> {
    let mut wrapped = Vec::new();
    for (i, l) in lines.iter().enumerate() {
        let lim = if i > 0 { 26 } else { 20 };
        let mut cur = String::new();
        for w in l.split_whitespace() {
            if !cur.is_empty() && cur.chars().count() + 1 + w.chars().count() > lim {
                wrapped.push((i, std::mem::take(&mut cur)));
                cur = w.to_string();
            } else {
                cur = format!("{cur} {w}").trim().to_string();
            }
        }
        wrapped.push((i, cur));
    }
    if wrapped.is_empty() {
        return Err("a node with no text".into());
    }
    let width = wrapped.iter().map(|(i, t)| t.chars().count() as f64 * if *i == 0 { 11.6 } else { 8.3 }).fold(f64::MIN, f64::max) + 48.0;
    let height: f64 = wrapped.iter().map(|(i, _)| if *i == 0 { 27.0 } else { 23.0 }).sum::<f64>() + 32.0;
    Ok((width.max(120.0), height, wrapped))
}

fn dot(src: &str) -> Result<Value, String> {
    let mut c = Command::new("dot").arg("-Tjson").stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().map_err(|e| format!("dot: {e}"))?;
    c.stdin.take().ok_or("dot: no stdin")?.write_all(src.as_bytes()).map_err(|e| e.to_string())?;
    let o = c.wait_with_output().map_err(|e| e.to_string())?;
    if !o.status.success() {
        return Err(format!("dot exited with {}", o.status));
    }
    serde_json::from_slice(&o.stdout).map_err(|e| e.to_string())
}

fn floats(s: &str) -> Result<Vec<f64>, String> {
    s.split(',').map(|x| x.parse::<f64>().map_err(|e| e.to_string())).collect()
}

fn bb(v: &Value) -> Result<Vec<f64>, String> {
    floats(v["bb"].as_str().ok_or("no bounding box")?)
}

fn cluster(g: &Flow, ids: &HashMap<&str, String>, k: usize) -> String {
    let grp = &g.groups[k];
    let members: String = grp.members.iter().map(|m| format!("{}; ", ids[m.as_str()])).collect();
    let kids: Vec<String> = g.groups.iter().enumerate().filter(|(_, x)| x.parent == Some(k)).map(|(j, _)| cluster(g, ids, j)).collect();
    format!(r#"subgraph cluster_{k} {{ label="{}"; fontsize=18; fontname="Georgia"; margin=22; {members}{} }}"#, grp.title.replace('"', ""), kids.join(" "))
}

fn flow_svg(g: &Flow, uid: &str, crest_key: &str) -> Result<String, String> {
    let rank = match g.dir.as_str() {
        "TD" | "TB" => "TB",
        "LR" => "LR",
        "BT" => "BT",
        "RL" => "RL",
        _ => "TB",
    };
    let mut sizes = HashMap::new();
    for n in &g.order {
        sizes.insert(n.as_str(), measure(&g.nodes[n])?);
    }
    let ids: HashMap<&str, String> = g.order.iter().enumerate().map(|(i, n)| (n.as_str(), format!("n{i}"))).collect();
    let mut src = vec![
        format!(r#"digraph G {{ rankdir={rank}; nodesep=0.45; ranksep=0.6; splines=spline; node [shape=box, fixedsize=true, label=""];"#),
        r#"edge [dir=none, fontsize=14, fontname="Georgia"];"#.to_string(),
    ];
    for (k, grp) in g.groups.iter().enumerate() {
        if grp.parent.is_none() {
            src.push(cluster(g, &ids, k));
        }
    }
    for n in &g.order {
        let (w, h, _) = &sizes[n.as_str()];
        src.push(format!("{} [width={:.3}, height={:.3}];", ids[n.as_str()], w / 72.0, h / 72.0));
    }
    for (a, b, lab, _) in &g.edges {
        let l = if lab.is_empty() { String::new() } else { format!(r#"label="{}""#, lab.replace('"', "")) };
        src.push(format!("{} -> {} [{l}];", ids[a.as_str()], ids[b.as_str()]));
    }
    src.push("}".into());
    let src = src.join("\n");
    let mut js = dot(&src)?;
    if rank == "TB" && bb(&js)?[2] > 1000.0 {
        // a wide fan reads better turned on its side
        let side = dot(&src.replacen("rankdir=TB", "rankdir=LR", 1))?;
        if bb(&side)?[2] < bb(&js)?[2] {
            js = side;
        }
    }
    let b = bb(&js)?;
    let (x0, y0, x1, y1) = (b[0], b[1], b[2], b[3]);
    let pad = 40.0;
    let (w_all, h_all) = (x1 - x0 + 2.0 * pad, y1 - y0 + 2.0 * pad);
    let px = |x: f64| x - x0 + pad;
    let py = |y: f64| (y1 - y) + pad;
    let mut r = from_str_seed(uid);
    let mut o = String::new();
    let _ = write!(o, r#"<svg class="wotr-chart" viewBox="0 0 {w_all:.0} {h_all:.0}" style="--mw:{:.0}px" font-family="{SERIF}" role="img">"#, w_all.min(680.0));
    let _ = write!(o, r##"<defs><linearGradient id="pl{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1f12"/><stop offset="1" stop-color="#140f0a"/></linearGradient><linearGradient id="ed{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d58c"/><stop offset="1" stop-color="#b07a24"/></linearGradient><radialGradient id="bg{uid}" cx=".5" cy="0" r="1.1"><stop offset="0" stop-color="#2c2010"/><stop offset="1" stop-color="{INK}"/></radialGradient><filter id="gl{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter><radialGradient id="halo{uid}"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>"##);
    let _ = write!(o, r#"<rect width="{w_all:.0}" height="{h_all:.0}" rx="16" fill="url(#bg{uid})"/>"#);
    for _ in 0..(w_all * h_all / 9000.0) as i64 {
        let (cx, cy) = (r.uniform(0.0, w_all), r.uniform(0.0, h_all));
        let size = r.choice(&["0.6", "0.9", "1.3"]);
        let _ = write!(o, r##"<circle cx="{cx:.0}" cy="{cy:.0}" r="{size}" fill="#fff4d6" opacity="{:.2}"/>"##, r.uniform(0.1, 0.55));
    }
    if !crest_key.is_empty() {
        let cs = w_all.min(h_all) * 0.55;
        o.push_str(&crest(crest_key, cs, w_all - cs * 0.8, h_all - cs * 0.85, GOLD, 2.0, 0.07));
    }
    let _ = write!(o, r#"<rect x="7" y="7" width="{:.0}" height="{:.0}" rx="12" fill="none" stroke="{GOLD}" stroke-opacity=".4"/>"#, w_all - 14.0, h_all - 14.0);
    for (x, y, sx, sy) in [(7.0, 7.0, 1.0, 1.0), (w_all - 7.0, 7.0, -1.0, 1.0), (7.0, h_all - 7.0, 1.0, -1.0), (w_all - 7.0, h_all - 7.0, -1.0, -1.0)] {
        let _ = write!(o, r#"<path d="M{x:.0} {:.0} L{x:.0} {y:.0} L{:.0} {y:.0}" fill="none" stroke="{GOLD}" stroke-width="2"/>"#, y + 22.0 * sy, x + 22.0 * sx);
    }
    let empty = Vec::new();
    let objects = js["objects"].as_array().unwrap_or(&empty);
    let label = |v: &Value, k: &str| v[k].as_str().unwrap_or("").to_string();
    for obj in objects {
        if label(obj, "name").starts_with("cluster") && obj.get("bb").is_some() {
            let c = bb(obj)?;
            let _ = write!(o, r#"<rect x="{:.0}" y="{:.0}" width="{:.0}" height="{:.0}" rx="14" fill="{GOLD}" fill-opacity=".04" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="5 6"/>"#, px(c[0]), py(c[3]), c[2] - c[0], c[3] - c[1]);
            let _ = write!(o, r#"<text x="{:.0}" y="{:.0}" text-anchor="middle" fill="{GOLD}" font-size="16" letter-spacing="2">{}</text>"#, px((c[0] + c[2]) / 2.0), py(c[3]) + 22.0, escape(&label(obj, "label").to_uppercase()));
        }
    }
    let names: HashMap<&str, &str> = ids.iter().map(|(k, v)| (v.as_str(), *k)).collect();
    let by_gvid: HashMap<i64, &Value> = objects.iter().filter_map(|x| Some((x["_gvid"].as_i64()?, x))).collect();
    for e in js["edges"].as_array().unwrap_or(&empty) {
        let end = |k: &str| -> Result<&str, String> {
            let o = by_gvid.get(&e[k].as_i64().ok_or("an edge with no end")?).ok_or("an unknown edge end")?;
            names.get(o["name"].as_str().unwrap_or("")).copied().ok_or_else(|| "an unknown node".to_string())
        };
        let (a, b) = (end("tail")?, end("head")?);
        let style = g.edges.iter().find(|(x, y, _, _)| x == a && y == b).ok_or("an edge not in the chart")?.3;
        let mut pts = Vec::new();
        for p in e["pos"].as_str().unwrap_or("").split_whitespace().filter(|p| !p.starts_with("e,") && !p.starts_with("s,")) {
            let v = floats(p)?;
            pts.push((px(v[0]), py(v[1])));
        }
        let first = pts.first().ok_or("an edge with no points")?;
        let mut d = format!("M{:.1} {:.1} ", first.0, first.1);
        let segs: Vec<String> = (1..pts.len().saturating_sub(2)).step_by(3).map(|i| format!("C{:.1} {:.1} {:.1} {:.1} {:.1} {:.1}", pts[i].0, pts[i].1, pts[i + 1].0, pts[i + 1].1, pts[i + 2].0, pts[i + 2].1)).collect();
        d.push_str(&segs.join(" "));
        let dash = if style == "dash" { r#" stroke-dasharray="6 6""# } else { "" };
        let _ = write!(o, r#"<path d="{d}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="6" filter="url(#gl{uid})"/>"#);
        let _ = write!(o, r#"<path d="{d}" fill="none" stroke="url(#ed{uid})" stroke-width="2"{dash}/>"#);
        if style != "none" {
            let ((ax, ay), (bx, by)) = (pts[pts.len() - 2], pts[pts.len() - 1]);
            let ang = (by - ay).atan2(bx - ax).to_degrees();
            let _ = write!(o, r##"<path d="M0 0 L-11 -6 L-7 0 L-11 6 Z" transform="translate({bx:.1} {by:.1}) rotate({ang:.0})" fill="#f3d58c"/>"##);
        }
        let lab = label(e, "label");
        if let (false, Some(lp)) = (lab.is_empty(), e.get("lp").and_then(Value::as_str)) {
            let p = floats(lp)?;
            let lw = lab.chars().count() as f64 * 8.2 + 20.0;
            let _ = write!(o, r#"<rect x="{:.0}" y="{:.0}" width="{lw:.0}" height="24" rx="12" fill="{INK}" stroke="{GOLD}" stroke-opacity=".5"/>"#, px(p[0]) - lw / 2.0, py(p[1]) - 13.0);
            let _ = write!(o, r#"<text x="{:.0}" y="{:.0}" text-anchor="middle" fill="{MUTED}" font-size="15.5" font-style="italic" font-family="{BODY}">{}</text>"#, px(p[0]), py(p[1]) + 5.0, escape(&lab));
        }
    }
    let has_parent: HashSet<&str> = g.edges.iter().map(|e| e.1.as_str()).collect();
    for obj in objects {
        let Some(n) = names.get(label(obj, "name").as_str()).copied() else { continue };
        let p = floats(obj["pos"].as_str().ok_or("a node with no position")?)?;
        let (cx, cy) = (px(p[0]), py(p[1]));
        let (w, h, wrapped) = &sizes[n];
        let (w, h) = (*w, *h);
        let (x, y) = (cx - w / 2.0, cy - h / 2.0);
        if !has_parent.contains(n) && g.nodes.len() > 2 {
            // the source of the chart wears a halo
            let _ = write!(o, r#"<ellipse cx="{cx:.1}" cy="{cy:.1}" rx="{:.0}" ry="{:.0}" fill="url(#halo{uid})"/>"#, w * 0.85, h * 1.3);
            let _ = write!(o, r#"<rect x="{:.1}" y="{:.1}" width="{:.0}" height="{:.0}" rx="16" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-dasharray="2 5"/>"#, x - 7.0, y - 7.0, w + 14.0, h + 14.0);
        }
        let _ = write!(o, r##"<rect x="{x:.1}" y="{:.1}" width="{w:.0}" height="{h:.0}" rx="11" fill="#000" opacity=".45" filter="url(#gl{uid})"/>"##, y + 4.0);
        let _ = write!(o, r#"<rect x="{x:.1}" y="{y:.1}" width="{w:.0}" height="{h:.0}" rx="11" fill="url(#pl{uid})" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.4"/>"#);
        let _ = write!(o, r#"<rect x="{:.1}" y="{:.1}" width="{:.0}" height="{:.0}" rx="8" fill="none" stroke="{GOLD}" stroke-opacity=".2"/>"#, x + 4.0, y + 4.0, w - 8.0, h - 8.0);
        let _ = write!(o, r#"<polygon points="{cx:.1},{:.1} {:.1},{y:.1} {cx:.1},{:.1} {:.1},{y:.1}" fill="{GOLD}"/>"#, y - 6.0, cx + 6.0, y + 6.0, cx - 6.0);
        let mut ty = y + 15.0;
        for (i, t) in wrapped {
            ty += if *i == 0 { 27.0 } else { 23.0 };
            if *i == 0 {
                let _ = write!(o, r#"<text x="{cx:.1}" y="{:.1}" text-anchor="middle" fill="{GOLD}" font-size="21" font-weight="600" letter-spacing=".5">{}</text>"#, ty - 7.0, escape(t));
            } else {
                let _ = write!(o, r#"<text x="{cx:.1}" y="{:.1}" text-anchor="middle" fill="{TEXT}" font-size="17" font-style="italic" font-family="{BODY}">{}</text>"#, ty - 7.0, escape(t));
            }
        }
    }
    o.push_str("</svg>");
    Ok(format!(r#"<div class="wotr-chart-wrap">{o}</div>"#))
}

/// One mermaid source as raw HTML, or None so the page keeps the mermaid it cannot draw.
pub fn render(src: &str, seed: &str) -> Option<String> {
    let uid = sha8(&format!("{seed}{src}"));
    let drawn = parse(src).and_then(|c| match c {
        Chart::Timeline(title, sections) => Ok(timeline(&title, &sections)),
        Chart::Flow(g) => match chain_of(&g) {
            Some(seq) => road(&g, &seq),
            None => flow_svg(&g, &uid, if seed.is_empty() { "" } else { style_for(seed).0 .0 }),
        },
    });
    match drawn {
        Ok(html) => Some(html),
        Err(e) => {
            println!("  chart left as mermaid ({e})");
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_chain_becomes_a_road_and_keeps_its_labels() {
        let html = render("flowchart TD\nA[\"1 · One\"] --> B[Two] -->|via| C[Three] --> D[\"Four<br/>sub\"]", "").unwrap();
        assert!(html.starts_with(r#"<ol class="wotr-road">"#), "{html}");
        assert!(html.contains(r#"<span class="rn">1</span>"#) && html.contains(r#"<span class="rv">via</span>"#) && html.contains(r#"<span class="rs">sub</span>"#), "{html}");
    }

    #[test]
    fn a_timeline_becomes_era_bands() {
        let html = render("timeline\ntitle The Ages\nsection First (0-10)\nA : B", "").unwrap();
        assert!(html.contains(r#"<div class="et">The Ages</div>"#) && html.contains(r#"<span class="rd">0-10</span>"#) && html.contains(r#"<span class="ev">B</span>"#), "{html}");
    }

    #[test]
    fn an_unreadable_chart_stays_mermaid() {
        assert!(render("", "").is_none());
        assert!(render("flowchart TD\nsubgraph", "").is_none());
    }
}
