//! The art set over each public page at build time: a plate for an ordinary page, a banner for a
//! section's front page, and the crests. The vault stays plain markdown. The system diagrams are not
//! made here: wiki/Assets/Diagrams/*.svg are the source, inlined by the page builder.
use crate::py::{escape, from_sha1, sha8};
use crate::tables::{Style, CRESTS, DEFAULT, FOLDER_ART, SECTIONS};
use std::f64::consts::PI;
use std::fmt::Write;

pub const GOLD: &str = "#d8ab4f";
pub const INK: &str = "#110d09";

/// The section's style and its name ("" when the page sits outside every section).
pub fn style_for(rel: &str) -> (Style, &str) {
    let top = rel.split('/').next().unwrap_or("");
    match SECTIONS.iter().find(|(k, _)| *k == top) {
        Some((_, s)) => (*s, top),
        None => (DEFAULT, ""),
    }
}

#[allow(clippy::too_many_arguments)]
pub fn crest(key: &str, size: f64, x: f64, y: f64, color: &str, width: f64, opacity: f64) -> String {
    let s = size / 200.0;
    let body = CRESTS.iter().find(|(k, _)| *k == key).map_or("", |(_, b)| b);
    format!(r#"<g transform="translate({x:.1} {y:.1}) scale({s:.3})" fill="none" stroke="{color}" color="{color}" stroke-width="{:.2}" stroke-linejoin="round" stroke-linecap="round" opacity="{opacity:?}">{body}</g>"#, width / s)
}

/// The art behind a page's title: a starfield, a rune wheel and the section crest.
fn plate_svg(title: &str, key: &str, hue: &str, deep: &str, uid: &str) -> String {
    let mut r = from_sha1(title);
    let (cx, cy) = (980 + r.randint(-40, 40), 120i64);
    let (fx, fy) = (cx as f64, cy as f64);
    let mut o = String::new();
    o.push_str(r#"<svg class="wotr-plate-art" viewBox="0 0 1200 240" preserveAspectRatio="xMaxYMid slice" aria-hidden="true">"#);
    let _ = write!(o, r#"<defs><linearGradient id="pg{uid}" x1="0" x2="1"><stop offset="0" stop-color="{INK}"/><stop offset=".55" stop-color="{deep}"/><stop offset="1" stop-color="{INK}"/></linearGradient>"#);
    let _ = write!(o, r#"<radialGradient id="pr{uid}" cx="{:.3}" cy=".5" r=".45"><stop offset="0" stop-color="{hue}" stop-opacity=".55"/><stop offset="1" stop-color="{hue}" stop-opacity="0"/></radialGradient></defs>"#, fx / 1200.0);
    let _ = write!(o, r#"<rect width="1200" height="240" fill="url(#pg{uid})"/><rect width="1200" height="240" fill="url(#pr{uid})"/>"#);
    let stars: Vec<(f64, f64)> = (0..70).map(|_| (r.uniform(0.0, 1200.0), r.uniform(0.0, 240.0))).collect();
    for (x, y) in &stars {
        let size = r.choice(&["0.6", "0.9", "1.2", "1.7"]);
        let _ = write!(o, r##"<circle cx="{x:.0}" cy="{y:.0}" r="{size}" fill="#fff4d6" opacity="{:.2}"/>"##, r.uniform(0.15, 0.8));
    }
    let mut pick = r.sample(&stars[..40], 6);
    pick.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let line: Vec<String> = pick.iter().map(|(x, y)| format!("{x:.0},{y:.0}")).collect();
    let _ = write!(o, r#"<polyline points="{}" fill="none" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1"/>"#, line.join(" "));
    // the rune wheel
    let step = r.choice(&[5i64, 6, 8, 10, 12]);
    for (rad, op) in [(150, ".22"), (118, ".35"), (96, ".18")] {
        let shown = op.replacen('.', "0.", 1);
        let _ = write!(o, r#"<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{GOLD}" stroke-opacity="{shown}" stroke-width="1.2"/>"#);
    }
    for a in (0..360).step_by(step as usize) {
        let t = (a as f64 + r.random() * 0.5) * (PI / 180.0);
        let l = if a % (step * 3) == 0 { 10.0 } else { 5.0 };
        let (c, s) = (t.cos(), t.sin());
        let _ = write!(o, r#"<line x1="{:.1}" y1="{:.1}" x2="{:.1}" y2="{:.1}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1.2"/>"#, fx + 118.0 * c, fy + 118.0 * s, fx + (118.0 + l) * c, fy + (118.0 + l) * s);
    }
    for _ in 0..r.randint(9, 15) {
        // glyph marks between the rings
        let t = r.uniform(0.0, 2.0 * PI);
        let (x, y) = (fx + 134.0 * t.cos(), fy + 134.0 * t.sin());
        let g = r.choice(&["M-5 -5 L5 5 M-5 5 L0 0", "M0 -6 L0 6 M-4 -2 L4 -2", "M-5 4 L0 -6 L5 4", "M-4 -4 L4 -4 L-4 4 L4 4", "M0 -6 A6 6 0 0 1 0 6"]);
        let _ = write!(o, r#"<path d="{g}" transform="translate({x:.1} {y:.1}) rotate({:.0})" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.3"/>"#, t * (180.0 / PI) + 90.0);
    }
    o.push_str(&crest(key, 150.0, fx - 75.0, fy - 75.0, GOLD, 2.4, 0.9));
    let _ = write!(o, r#"<rect x="10" y="10" width="1180" height="220" rx="6" fill="none" stroke="{GOLD}" stroke-opacity=".28"/>"#);
    for (x, y, sx, sy) in [(10, 10, 1, 1), (1190, 10, -1, 1), (10, 230, 1, -1), (1190, 230, -1, -1)] {
        let _ = write!(o, r#"<path d="M{x} {} L{x} {y} L{} {y} M{} {} L{} {}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-opacity=".75"/>"#, y + 26 * sy, x + 26 * sx, x + 6 * sx, y + 6 * sy, x + 14 * sx, y + 6 * sy);
    }
    o.push_str("</svg>");
    o
}

/// Empty spans whose words CSS draws from data-t, so they stay out of search and previews.
fn words(kicker: &str, title: &str, tag: &str) -> String {
    let mut o = String::from(r#"<div class="wotr-words">"#);
    let _ = write!(o, r#"<span class="wk" data-t="{}"></span><span class="wt" data-t="{}"></span>"#, escape(kicker), escape(title));
    if !tag.is_empty() {
        let _ = write!(o, r#"<span class="wg" data-t="{}"></span>"#, escape(tag));
    }
    o.push_str("</div>");
    o
}

/// The raw HTML set at the head of an ordinary page.
pub fn plate(rel: &str, title: &str) -> String {
    let ((key, hue, deep, _, _), _) = style_for(rel);
    let parts: Vec<&str> = rel.split('/').collect();
    let kept: Vec<&str> = parts[..parts.len() - 1].iter().copied().filter(|p| *p != title).collect();
    let kicker = if kept.is_empty() { "War of the Realms".to_string() } else { kept.join(" \u{b7} ") };
    format!(r#"<div class="wotr-plate wotr-s-{key}">{}{}</div>

"#, plate_svg(title, key, hue, deep, &sha8(rel)), words(&kicker, title, ""))
}

/// A section front page: the painted art, the crest, the title and the tagline.
pub fn banner(rel: &str, title: &str, base: &str, painting: Option<&str>) -> String {
    let ((key, hue, _, art, mut tag), top) = style_for(rel);
    let parts: Vec<&str> = rel.split('/').collect();
    let kicker = if !top.is_empty() && top != title {
        tag = ""; // a sub-folder's front page inside a section
        parts[..parts.len().saturating_sub(2)].join(" \u{b7} ")
    } else {
        "War of the Realms".to_string()
    };
    let folder = rel.rsplit_once('/').map_or(rel, |x| x.0);
    let art = painting.or(FOLDER_ART.iter().find(|(k, _)| *k == folder).map(|(_, v)| *v)).unwrap_or(art);
    format!(r#"<div class="wotr-banner wotr-s-{key}" style="background-image:url({base}/assets/{art}.webp);--hue:{hue}"><svg class="wotr-banner-crest" viewBox="0 0 200 200" aria-hidden="true">{}</svg>{}</div>

"#, crest(key, 200.0, 0.0, 0.0, GOLD, 3.0, 1.0), words(&kicker, title, tag))
}
