//! WOTR Bot: the players' front-end onto the wiki, the scene archive and the table state. Every
//! answer is the index's own text or a refusal: nothing here resolves a conflict, paraphrases a rule
//! or invents a number.
pub mod commands;
pub mod desk;
pub mod embeds;
pub mod fmt;
pub mod fow;
pub mod look;
pub mod names;
pub mod run;
pub mod sheet;

use serde_json::{json, Value};

/// `wotr-mcp bot preview`: JSON lines in, what the bot would say out, with no Discord connection.
pub fn preview() -> i32 {
    for line in std::io::stdin().lines().map_while(Result::ok) {
        let a: Value = match serde_json::from_str(&line) {
            Ok(v) => v,
            Err(e) => {
                println!("{}", json!({"error": e.to_string()}));
                continue;
            }
        };
        let s = |k: &str| a[k].as_str().unwrap_or("");
        let out = match s("cmd") {
            "name" => match names::build(s("culture"), a["seed"].as_u64().unwrap_or(0), s("branch"), s("lineage"), s("sex")) {
                Ok(d) => json!({"data": d, "embed": embeds::name_embed(&d, s("label")).to_json()}),
                Err(e) => json!({"error": e}),
            },
            "stats" => match fow::build(a["level"].as_i64().unwrap_or(1), a["lean"].as_str(), a["seed"].as_u64().unwrap_or(0)) {
                Ok(d) => json!({"embed": embeds::stat_embed(&d).to_json()}),
                Err(e) => json!({"error": e}),
            },
            "plain" => json!(look::plain(s("text"))),
            "for_discord" => json!(look::for_discord(s("text"))),
            "wiki" => {
                let hits = look::wiki_hits(s("query"), 5);
                json!({"hits": hits, "embed": embeds::hits_embed(s("query"), &hits, true, "C").to_json()})
            }
            "wiki_page" => {
                let (title, text, url, cat) = look::wiki_page(s("query"));
                let url = url.as_deref();
                json!({"title": title, "embeds": embeds::pages(&text, 3600, &title, embeds::C_WIKI, url, &format!("wiki mirror{}", if url.is_some() { " \u{b7} title links to Notion" } else { "" }), &cat).iter().map(|e| e.to_json()).collect::<Vec<_>>()})
            }
            "recall" => {
                let hits = look::scene_hits(s("query"), 4);
                json!({"hits": hits, "embed": embeds::hits_embed(s("query"), &hits, false, "C").to_json()})
            }
            "scene_text" => {
                let (title, text) = look::scene_text(s("query"));
                json!({"title": title, "text": text})
            }
            "define" => json!(look::define(s("query"), 5)),
            "character" => match look::card(s("query")) {
                Some(d) => {
                    let sections: Vec<Vec<Value>> = (0..d.sections.len()).map(|n| embeds::card_section(&d, n, 3600).iter().map(|e| e.to_json()).collect()).collect();
                    json!({"overview": embeds::card_overview(&d, 3600).to_json(), "sections": sections})
                }
                None => Value::Null,
            },
            "fow" => look::fow_card(s("query")).map_or(Value::Null, |d| embeds::fow_embed(&d).to_json()),
            "names" => json!(look::character_names(s("query"), 25)),
            "timeline" => json!(look::timeline().unwrap_or_default()),
            "sheet" => {
                let r = sheet::check(s("text"));
                json!({"ok": r.ok, "findings": r.findings, "summary": r.summary, "embed": embeds::sheet_embed(&r, "W").to_json()})
            }
            "commands" => json!(commands::definitions()),
            o => json!({"error": format!("no such preview: {o}")}),
        };
        println!("{out}");
    }
    0
}
