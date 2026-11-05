//! What the bot says, as plain data: embeds, long text as pages, and the shapes of every card. Nothing
//! here talks to Discord, so all of it can be checked without a connection.
use super::fmt::{commas, commas0};
use super::look::{Card, FowCard};
use serde_json::{json, Map, Value};

pub const DESC_MAX: usize = 4096;
pub const FIELD_MAX: usize = 1024;
pub const C_WIKI: u32 = 0x5C6BC0;
pub const C_CARD: u32 = 0x8E24AA;
pub const C_SCENE: u32 = 0x00897B;
pub const C_NAME: u32 = 0xD4A017;
pub const C_STAT: u32 = 0xC0392B;

pub fn clip(s: &str, n: usize) -> String {
    if s.chars().count() <= n {
        return s.to_string();
    }
    let cut: String = s.chars().take(n - 1).collect();
    format!("{}\u{2026}", cut.trim_end())
}

#[derive(Clone, Default)]
pub struct Embed {
    pub title: Option<String>,
    pub description: Option<String>,
    pub color: Option<u32>,
    pub url: Option<String>,
    pub author: Option<String>,
    pub footer: Option<String>,
    pub fields: Vec<(String, String, bool)>,
}

impl Embed {
    pub fn new(title: &str, color: u32) -> Self {
        Embed { title: Some(title.to_string()), color: Some(color), ..Default::default() }
    }

    pub fn field(&mut self, name: &str, value: &str, inline: bool) {
        self.fields.push((name.to_string(), value.to_string(), inline));
    }

    pub fn set_footer(&mut self, text: &str) {
        self.footer = Some(clip(text, 2048));
    }

    pub fn to_json(&self) -> Value {
        let mut m = Map::new();
        let mut put = |k: &str, v: Value| {
            m.insert(k.into(), v);
        };
        if let Some(x) = &self.title {
            put("title", json!(x));
        }
        if let Some(x) = &self.description {
            put("description", json!(x));
        }
        if let Some(x) = self.color {
            put("color", json!(x));
        }
        if let Some(x) = &self.url {
            put("url", json!(x));
        }
        if let Some(x) = &self.author {
            put("author", json!({"name": x}));
        }
        if let Some(x) = &self.footer {
            put("footer", json!({"text": x}));
        }
        if !self.fields.is_empty() {
            put("fields", Value::Array(self.fields.iter().map(|(n, v, i)| json!({"name": n, "value": v, "inline": i})).collect()));
        }
        Value::Object(m)
    }
}

fn some(s: String) -> Option<String> {
    (!s.is_empty()).then_some(s)
}

/// Text split on line boundaries into embeds of at most `size` characters.
pub fn pages(text: &str, size: usize, title: &str, colour: u32, url: Option<&str>, footer_text: &str, author: &str) -> Vec<Embed> {
    let trimmed = text.trim();
    let text = if trimmed.is_empty() { "(nothing)" } else { trimmed };
    let (mut chunks, mut cur): (Vec<String>, String) = (Vec::new(), String::new());
    for line in text.split('\n') {
        let mut line: Vec<char> = line.chars().collect();
        while line.len() > size {
            // a single over-long line is cut hard
            if !cur.is_empty() {
                chunks.push(std::mem::take(&mut cur));
            }
            chunks.push(line[..size].iter().collect());
            line.drain(..size);
        }
        let line: String = line.into_iter().collect();
        if cur.chars().count() + line.chars().count() + 1 > size {
            chunks.push(std::mem::replace(&mut cur, line));
        } else if cur.is_empty() {
            cur = line;
        } else {
            cur = format!("{cur}\n{line}");
        }
    }
    if !cur.is_empty() {
        chunks.push(cur);
    }
    let total = chunks.len();
    chunks
        .into_iter()
        .enumerate()
        .map(|(i, ch)| {
            let mut e = Embed { title: some(clip(title, 256)), description: Some(ch), color: Some(colour), url: url.map(String::from), ..Default::default() };
            if !author.is_empty() {
                e.author = Some(clip(author, 256));
            }
            let tail = if total > 1 { format!("page {}/{total}", i + 1) } else { String::new() };
            let parts: Vec<&str> = [footer_text, tail.as_str()].into_iter().filter(|x| !x.is_empty()).collect();
            e.set_footer(&parts.join(" \u{b7} "));
            e
        })
        .collect()
}

fn text<'a>(v: &'a Value, k: &str) -> &'a str {
    v.get(k).and_then(Value::as_str).unwrap_or("")
}

/// One embed, one field per hit: title, where it lives, a highlighted snippet.
pub fn hits_embed(query: &str, hits: &[Value], wiki: bool, commit: &str) -> Embed {
    let mut e = Embed::new(&clip(&format!("{}: {query}", if wiki { "Wiki" } else { "Scenes" }), 256), if wiki { C_WIKI } else { C_SCENE });
    if hits.is_empty() {
        e.description = Some(format!("Nothing matches **{query}**."));
        return e;
    }
    for (i, h) in hits.iter().enumerate() {
        let where_ = if !text(h, "category").is_empty() { text(h, "category") } else { text(h, "file") };
        let url = text(h, "url");
        let link = if url.is_empty() { String::new() } else { format!(" \u{b7} [Notion]({url})") };
        e.field(&clip(&format!("{}. {}", i + 1, text(h, "title")), 256), &clip(&format!("-# {where_}{link}\n{}", text(h, "snippet")), FIELD_MAX), false);
    }
    e.set_footer(&format!("pick a number below to open it \u{b7} {} \u{b7} @ {commit}", if wiki { "wiki mirror, up to an hour behind Notion" } else { "scene archive" }));
    e
}

pub fn name_embed(d: &Value, label: &str) -> Embed {
    let mut e = Embed { title: Some(clip(text(d, "name"), 256)), description: Some(clip(text(d, "note"), DESC_MAX)), color: Some(C_NAME), author: Some(clip(label, 256)), ..Default::default() };
    for l in d["lines"].as_array().into_iter().flatten() {
        e.field(&clip(l[0].as_str().unwrap_or(""), 256), &clip(l[1].as_str().unwrap_or(""), FIELD_MAX), false);
    }
    let flags: Vec<String> = d["flags"].as_array().into_iter().flatten().map(|f| format!("\u{2022} {}", f.as_str().unwrap_or(""))).collect();
    if !flags.is_empty() {
        e.field("Flags", &clip(&flags.join("\n"), FIELD_MAX), false);
    }
    e.set_footer(&format!("elements from {} \u{b7} Naming Guide 2026-09-12 edition \u{b7} \u{1f3b2} for another", text(d, "rule")));
    e
}

pub fn stat_embed(d: &Value) -> Embed {
    let (st, band) = (&d["stage"], text(d, "band"));
    let int = |k: &str| d[k].as_i64().unwrap_or(0);
    let mut e = Embed::new(&format!("Level {} \u{b7} Stage {} \u{2014} {}", int("level"), text(st, "roman"), text(st, "name")), C_STAT);
    e.author = Some(if text(st, "standing").is_empty() { format!("Band {band}") } else { format!("Band {band} \u{b7} {}", text(st, "standing")) });
    let mut lines = vec![
        format!("Max Grade **{}** \u{2014} a Sub-Stat holds at most **{}** (R39-4); the Stage ceiling of {} is the instability zone", text(st, "max_grade"), commas(int("grade_top")), commas(st["ceiling"].as_i64().unwrap_or(0))),
        format!("Pool **{}** ({} levelling + {} Thresholds) \u{b7} spent **{}** on Sub-Stats", commas(int("pool")), commas(int("lvl_pts")), commas(int("thr_pts")), commas(int("spent"))),
        format!("Leaning **{}**", text(d, "lean")),
    ];
    if int("unheld") != 0 {
        lines.push(format!("\u{26a0} **{}** points the Crystal cannot hold at this Stage; they sit aside", commas(int("unheld"))));
    }
    e.description = Some(clip(&lines.join("\n"), DESC_MAX));
    for r in d["rows"].as_array().into_iter().flatten() {
        let subs: Vec<String> = r["entries"].as_array().into_iter().flatten().map(|x| match x[1].as_i64() {
            Some(v) => format!("{} {}", x[0].as_str().unwrap_or(""), commas(v)),
            None => format!("{} \u{2014}", x[0].as_str().unwrap_or("")),
        }).collect();
        let over = if r["over"].as_bool().unwrap_or(false) { " \u{26a0} above the Stage's grade".to_string() } else { String::new() };
        let shaky: Vec<&str> = r["unstable"].as_array().into_iter().flatten().filter_map(Value::as_str).collect();
        let marks = if shaky.is_empty() { over } else { format!("{over} \u{26a0} unstable: {}", shaky.join(", ")) };
        e.field(&clip(&format!("{} \u{2014} {} \u{b7} mean {} \u{b7} {}-Grade{marks}", text(r, "primary"), commas(r["total"].as_i64().unwrap_or(0)), commas0(r["mean"].as_f64().unwrap_or(0.0)), text(r, "grade")), 256), &clip(&subs.join(" \u{b7} "), FIELD_MAX), false);
    }
    let flags: Vec<String> = d["flags"].as_array().into_iter().flatten().map(|f| format!("\u{2022} {}", f.as_str().unwrap_or(""))).collect();
    if !flags.is_empty() {
        e.field("Flags", &clip(&flags.join("\n"), FIELD_MAX), false);
    }
    e
}

const HEADLINE: [&str; 8] = ["Level", "Level-Band", "Band", "Stage", "Temperance Stage", "Coherence Band", "Aether Class", "Soul Crystal Tier"];

pub fn fow_embed(d: &FowCard) -> Embed {
    let mut e = Embed { title: Some(clip(&format!("FOW line \u{2014} {}", d.title), 256)), url: d.url.clone(), color: Some(C_STAT), ..Default::default() };
    if !d.category.is_empty() {
        e.author = Some(clip(&d.category, 256));
    }
    if d.empty {
        e.description = Some("This card carries no FOW figures. Flag an estimate in a character's mouth or ask Isaac \u{2014} the bot will not invent one.".into());
        e.set_footer("from the card only");
        return e;
    }
    let pair = |(k, v): &(String, String)| format!("**{k}** \u{b7} {v}");
    let (head, rest): (Vec<&(String, String)>, Vec<&(String, String)>) = d.facts.iter().partition(|f| HEADLINE.contains(&f.0.as_str()));
    e.description = some(clip(&head.iter().map(|f| pair(f)).collect::<Vec<_>>().join("\n"), DESC_MAX));
    for (primary, value, grade, peaks) in &d.rows {
        e.field(&clip(&format!("{primary} \u{2014} {value} \u{b7} {grade}"), 256), &clip(if peaks.is_empty() { "\u{2014}" } else { peaks }, FIELD_MAX), true);
    }
    if !rest.is_empty() {
        e.field("Force and flow", &clip(&rest.iter().take(8).map(|f| pair(f)).collect::<Vec<_>>().join("\n"), FIELD_MAX), false);
    }
    if !d.notes.is_empty() {
        e.field("The card's own words", &clip(&d.notes.iter().map(|n| format!("> {n}")).collect::<Vec<_>>().join("\n"), FIELD_MAX), false);
    }
    e.set_footer(&format!("from the card only; the bot never estimates a number{}", if d.url.is_some() { " \u{b7} title links to Notion" } else { "" }));
    e
}

pub fn card_overview(d: &Card, page: usize) -> Embed {
    let mut e = Embed { title: Some(clip(&d.title, 256)), url: d.url.clone(), color: Some(C_CARD), description: some(clip(&d.overview, page.min(1800))), ..Default::default() };
    if !d.category.is_empty() {
        e.author = Some(clip(&d.category, 256));
    }
    for (k, v) in &d.facts {
        e.field(&clip(k, 256), &clip(v, FIELD_MAX), v.chars().count() <= 40);
    }
    if !d.sections.is_empty() {
        let list: Vec<String> = d.sections.iter().enumerate().map(|(i, (h, _))| format!("{}. {h}", i + 1)).collect();
        e.field("Sections", &clip(&list.join("\n"), FIELD_MAX), false);
    }
    let also = if d.also.is_empty() { String::new() } else { format!(" \u{b7} also matched: {}", d.also.join(", ")) };
    e.set_footer(&format!("{} \u{b7} jump to a section below{also}", if d.url.is_some() { "title links to Notion" } else { "wiki mirror" }));
    e
}

pub fn card_section(d: &Card, n: usize, page: usize) -> Vec<Embed> {
    let (h, body) = &d.sections[n];
    pages(body, page, &format!("{} \u{2014} {h}", d.title), C_CARD, d.url.as_deref(), &format!("section {}/{}", n + 1, d.sections.len()), &d.category)
}

pub fn sheet_embed(res: &super::sheet::Report, who: &str) -> Embed {
    let mut e = Embed::new(&format!("Sheet check \u{2014} {}", res.summary), if res.ok { 0x2E7D32 } else { 0xC62828 });
    e.author = Some(who.to_string());
    let body: Vec<String> = res.findings.iter().map(|(l, t)| format!("{} {t}", match *l { "fail" => "\u{274c}", "warn" => "\u{26a0}\u{fe0f}", _ => "\u{2705}" })).collect();
    e.description = Some(clip(if body.is_empty() { "Nothing to check.".to_string() } else { body.join("\n") }.as_str(), DESC_MAX));
    e.set_footer(&format!("canon model R39-1 \u{b7} Dominion \u{f7}7 R39-2 \u{b7} Stage I counts R39-3 \u{b7} Max Grade binds R39-4 \u{b7} struck names R22 \u{b7} terms R14-5{}", if res.ok { "" } else { " \u{b7} fix and repost; nothing reaches the Judger until it passes" }));
    e
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn clip_trims_and_marks() {
        assert_eq!(clip("abc", 3), "abc");
        assert_eq!(clip("ab cdef", 4), "ab\u{2026}");
    }

    #[test]
    fn pages_split_on_lines_and_cut_a_long_one() {
        let p = pages("aaa\nbbb\nccc", 7, "T", C_WIKI, None, "foot", "");
        assert_eq!(p.iter().map(|e| e.description.clone().unwrap()).collect::<Vec<_>>(), ["aaa\nbbb", "ccc"]);
        assert_eq!(p[1].footer.as_deref(), Some("foot \u{b7} page 2/2"));
        let long = pages("xxxxxxxxxx", 4, "", C_WIKI, None, "", "");
        assert_eq!(long.iter().map(|e| e.description.clone().unwrap()).collect::<Vec<_>>(), ["xxxx", "xxxx", "xx"]);
        assert_eq!(pages("", 20, "", C_WIKI, None, "", "")[0].description.as_deref(), Some("(nothing)"));
    }
}
