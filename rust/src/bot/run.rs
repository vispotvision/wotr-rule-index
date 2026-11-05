//! The bot on Discord: the gateway, the commands, and the buttons and menus that keep state for a
//! while after a reply. The answers themselves come from the other modules, which never see Discord.
use super::commands::definitions;
use super::desk;
use super::embeds::{self, clip, Embed, C_CARD, C_NAME, C_SCENE, C_STAT, C_WIKI, DESC_MAX, FIELD_MAX};
use super::fmt::commas;
use super::fow;
use super::look::{self, Card, Post};
use super::names;
use super::sheet;
use crate::analysis;
use crate::pyyaml;
use crate::re;
use crate::table;
use crate::text::{caps, group};
use crate::util::{read_lossy, root};
use crate::writers;
use crate::{ContentBlock, Wotr};
use serde_json::{json, Map, Value};
use serenity::all::*;
use serenity::async_trait;
use std::collections::HashMap;
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

const NARRATE_POLL: u64 = 20;
const NARRATE_MAX: u64 = 3 * 3600;

/// A reply's interactive part, kept here until it times out.
#[derive(Clone)]
enum View {
    Pager { pages: Vec<Embed>, i: usize },
    OpenHit { hits: Vec<Value>, wiki: bool },
    RerollName { culture: String, branch: String, lineage: String, sex: String },
    RerollStats { level: i64 },
    Card { card: Arc<Card>, pages: Vec<Embed>, i: usize },
    Archive { title: String, md: String, script: String, notes: String },
    Engine { path: PathBuf, allow_eleven: bool, words: usize, chars: usize },
    Paste { title: String },
    Verify { combat: bool, culture: String, band: String },
}

impl View {
    fn secs(&self) -> u64 {
        match self {
            View::Archive { .. } => 1800,
            View::Engine { .. } => 300,
            _ => 900,
        }
    }
}

#[derive(Default)]
struct Msg {
    content: Option<String>,
    embed: Option<Embed>,
    ephemeral: bool,
    file: Option<(Vec<u8>, String)>,
    view: Option<View>,
}

impl Msg {
    fn text(t: impl Into<String>) -> Self {
        Msg { content: Some(t.into()), ..Default::default() }
    }
    fn private(t: impl Into<String>) -> Self {
        Msg { content: Some(t.into()), ephemeral: true, ..Default::default() }
    }
    fn embed(e: Embed) -> Self {
        Msg { embed: Some(e), ..Default::default() }
    }
    /// A list of embeds behind \u{25c0} \u{25b6}, or the one embed when there is only one.
    fn paged(pages: Vec<Embed>, ephemeral: bool) -> Self {
        let first = pages.first().cloned();
        let view = (pages.len() > 1).then_some(View::Pager { pages, i: 0 });
        Msg { embed: first, ephemeral, view, ..Default::default() }
    }
}

fn to_embed(e: &Embed) -> CreateEmbed {
    let mut c = CreateEmbed::new();
    if let Some(x) = &e.title {
        c = c.title(x);
    }
    if let Some(x) = &e.description {
        c = c.description(x);
    }
    if let Some(x) = e.color {
        c = c.colour(x);
    }
    if let Some(x) = &e.url {
        c = c.url(x);
    }
    if let Some(x) = &e.author {
        c = c.author(CreateEmbedAuthor::new(x));
    }
    if let Some(x) = &e.footer {
        c = c.footer(CreateEmbedFooter::new(x));
    }
    for (n, v, i) in &e.fields {
        c = c.field(n, v, *i);
    }
    c
}

fn button(id: String, label: &str, style: ButtonStyle) -> CreateButton {
    CreateButton::new(id).label(label).style(style)
}

fn components(id: u64, v: &View) -> Vec<CreateActionRow> {
    let cid = |action: &str| format!("v:{id}:{action}");
    let turn = || vec![button(cid("prev"), "\u{25c0}", ButtonStyle::Secondary), button(cid("next"), "\u{25b6}", ButtonStyle::Secondary)];
    match v {
        View::Pager { .. } => vec![CreateActionRow::Buttons(turn())],
        View::OpenHit { hits, .. } => {
            let options = hits.iter().enumerate().map(|(i, h)| {
                let mut o = CreateSelectMenuOption::new(clip(&format!("{}. {}", i + 1, h["title"].as_str().unwrap_or("")), 100), i.to_string());
                let place = h["category"].as_str().filter(|c| !c.is_empty()).or(h["file"].as_str()).unwrap_or("");
                if !place.is_empty() {
                    o = o.description(clip(place, 100));
                }
                o
            }).collect();
            vec![CreateActionRow::SelectMenu(CreateSelectMenu::new(cid("open"), CreateSelectMenuKind::String { options }).placeholder("Open a result\u{2026}"))]
        }
        View::RerollName { .. } | View::RerollStats { .. } => vec![CreateActionRow::Buttons(vec![button(cid("roll"), "\u{1f3b2} another", ButtonStyle::Primary)])],
        View::Card { card, pages, .. } => {
            let mut options = vec![CreateSelectMenuOption::new("Overview", "-1").emoji('\u{1f0cf}')];
            options.extend(card.sections.iter().take(24).enumerate().map(|(i, (h, _))| CreateSelectMenuOption::new(clip(&format!("{}. {h}", i + 1), 100), i.to_string())));
            let mut rows = vec![CreateActionRow::SelectMenu(CreateSelectMenu::new(cid("jump"), CreateSelectMenuKind::String { options }).placeholder("Jump to a section\u{2026}"))];
            if pages.len() > 1 {
                rows.push(CreateActionRow::Buttons(turn()));
            }
            rows
        }
        View::Archive { .. } => vec![CreateActionRow::Buttons(vec![button(cid("archive"), "\u{2714} Archive", ButtonStyle::Success), button(cid("cancel"), "Cancel", ButtonStyle::Secondary)])],
        View::Engine { allow_eleven, words, chars, .. } => {
            let mut b = vec![button(cid("local"), &format!("Local (free, ~{} min)", (words / 150).max(1)), ButtonStyle::Secondary)];
            if *allow_eleven {
                b.push(button(cid("elevenlabs"), &format!("ElevenLabs (\u{2248} {} characters)", commas(*chars as i64)), ButtonStyle::Primary));
            }
            vec![CreateActionRow::Buttons(b)]
        }
        View::Paste { .. } | View::Verify { .. } => vec![],
    }
}

pub struct Bot {
    cfg: Value,
    page: usize,
    tools: Wotr,
    views: Mutex<HashMap<u64, (Instant, View)>>,
    next_view: AtomicU64,
    lock: tokio::sync::Mutex<()>,
    sync: bool,
}

/// One interaction: its reply path, and whether a first reply has gone out.
struct Itx {
    http: Arc<Http>,
    id: InteractionId,
    token: String,
    done: AtomicBool,
    user: User,
    member: Option<Box<Member>>,
    guild: Option<GuildId>,
    channel: ChannelId,
    channel_name: Option<String>,
    thread: bool,
}

impl Bot {
    fn remember(&self, v: View) -> u64 {
        let id = self.next_view.fetch_add(1, Ordering::Relaxed);
        let mut m = self.views.lock().unwrap();
        let now = Instant::now();
        m.retain(|_, (t, v)| now.duration_since(*t) < Duration::from_secs(v.secs()));
        m.insert(id, (now, v));
        id
    }

    fn view(&self, id: u64) -> Option<View> {
        let m = self.views.lock().unwrap();
        m.get(&id).filter(|(t, v)| t.elapsed() < Duration::from_secs(v.secs())).map(|(_, v)| v.clone())
    }

    fn set_view(&self, id: u64, v: View) {
        if let Some(slot) = self.views.lock().unwrap().get_mut(&id) {
            slot.1 = v;
        }
    }

    fn rows(&self, m: &mut Msg) -> Vec<CreateActionRow> {
        m.view.take().map_or_else(Vec::new, |v| {
            let id = self.remember(v.clone());
            components(id, &v)
        })
    }

    /// judger / scribe / player / reader, from config.yaml's role map.
    async fn role(&self, itx: &Itx) -> &'static str {
        let (Some(member), Some(guild)) = (&itx.member, itx.guild) else { return "reader" };
        let all = match guild.roles(&itx.http).await {
            Ok(all) => all,
            Err(e) => {
                eprintln!("could not read the guild's roles: {e}"); // a member counts as a reader until they can be read
                return "reader";
            }
        };
        let have: Vec<String> = member.roles.iter().filter_map(|r| all.get(r).map(|x| x.name.clone())).collect();
        for level in ["judger", "scribe", "player"] {
            let listed = self.cfg["roles"][level].as_array().cloned().unwrap_or_default();
            if listed.iter().filter_map(Value::as_str).any(|n| have.iter().any(|h| h == n)) {
                return level;
            }
        }
        "reader"
    }

    async fn judge(&self, itx: &Itx) -> bool {
        matches!(self.role(itx).await, "judger" | "scribe")
    }
}

impl Itx {
    fn display_name(&self) -> String {
        self.member.as_ref().map_or_else(|| self.user.display_name().to_string(), |m| m.display_name().to_string())
    }

    async fn defer(&self, ephemeral: bool) -> Result<(), String> {
        CreateInteractionResponse::Defer(CreateInteractionResponseMessage::new().ephemeral(ephemeral)).execute(&self.http, (self.id, &self.token)).await.map_err(|e| e.to_string())?;
        self.done.store(true, Ordering::Relaxed);
        Ok(())
    }

    /// The first reply, or a follow-up once one has gone out.
    async fn send(&self, bot: &Bot, mut m: Msg) -> Result<(), String> {
        let rows = bot.rows(&mut m);
        let files: Vec<CreateAttachment> = m.file.take().map(|(b, n)| CreateAttachment::bytes(b, n)).into_iter().collect();
        if self.done.swap(true, Ordering::Relaxed) {
            let mut f = CreateInteractionResponseFollowup::new().ephemeral(m.ephemeral).components(rows);
            if let Some(c) = m.content {
                f = f.content(c);
            }
            if let Some(e) = &m.embed {
                f = f.embed(to_embed(e));
            }
            f = f.add_files(files);
            f.execute(&self.http, (None, &self.token)).await.map(|_| ()).map_err(|e| e.to_string())
        } else {
            let mut r = CreateInteractionResponseMessage::new().ephemeral(m.ephemeral).components(rows);
            if let Some(c) = m.content {
                r = r.content(c);
            }
            if let Some(e) = &m.embed {
                r = r.embed(to_embed(e));
            }
            r = r.add_files(files);
            CreateInteractionResponse::Message(r).execute(&self.http, (self.id, &self.token)).await.map_err(|e| e.to_string())
        }
    }

    /// Replace the message a button or menu sits on.
    async fn update(&self, bot: &Bot, reuse: Option<u64>, mut m: Msg) -> Result<(), String> {
        let rows = match (reuse, &m.view) {
            (Some(id), Some(v)) => components(id, v),
            _ => bot.rows(&mut m),
        };
        let mut r = CreateInteractionResponseMessage::new().components(rows);
        if let Some(c) = m.content {
            r = r.content(c);
        }
        if let Some(e) = &m.embed {
            r = r.embed(to_embed(e));
        }
        self.done.store(true, Ordering::Relaxed);
        // serenity sends attachments: [], which strips the scene file off an archive report
        let mut body = serde_json::to_value(CreateInteractionResponse::UpdateMessage(r)).map_err(|e| e.to_string())?;
        if let Some(d) = body["data"].as_object_mut() {
            d.remove("attachments");
        }
        self.http.create_interaction_response(self.id, &self.token, &body, vec![]).await.map_err(|e| e.to_string())
    }
}

fn opt_str(o: &[ResolvedOption], k: &str) -> Option<String> {
    o.iter().find(|x| x.name == k).and_then(|x| match x.value {
        ResolvedValue::String(s) => Some(s.to_string()),
        _ => None,
    })
}

fn opt_int(o: &[ResolvedOption], k: &str) -> Option<i64> {
    o.iter().find(|x| x.name == k).and_then(|x| match x.value {
        ResolvedValue::Integer(i) => Some(i),
        _ => None,
    })
}

fn opt_bool(o: &[ResolvedOption], k: &str) -> bool {
    o.iter().any(|x| x.name == k && matches!(x.value, ResolvedValue::Boolean(true)))
}

fn message_link(link: &str) -> Option<(ChannelId, MessageId)> {
    let m = caps(re!(r"/channels/\d+/(\d+)/(\d+)"), link)?;
    Some((ChannelId::new(group(&m, 1).parse().ok()?), MessageId::new(group(&m, 2).parse().ok()?)))
}

fn random_seed() -> u64 {
    let mut b = [0u8; 8];
    let _ = std::fs::File::open("/dev/urandom").and_then(|mut f| std::io::Read::read_exact(&mut f, &mut b));
    u64::from_le_bytes(b) >> 34 // 1 << 30, as random.randrange gave
}

fn today() -> String {
    chrono::Local::now().format("%Y-%m-%d").to_string()
}

/// The blocks a tool answers with, as text.
fn tool_text(blocks: Vec<ContentBlock>) -> String {
    blocks.into_iter().filter_map(|b| match b {
        ContentBlock::Text(t) => Some(t.text.clone()),
        _ => None,
    }).collect::<Vec<_>>().join("\n")
}

async fn message_text(msg: &Message, with_names: bool) -> String {
    let mut text = msg.content.clone();
    if with_names {
        text.push('\n');
        text.push_str(&msg.attachments.iter().map(|a| a.filename.clone()).collect::<Vec<_>>().join("\n"));
    }
    for a in &msg.attachments {
        if (a.filename.ends_with(".md") || a.filename.ends_with(".txt")) && a.size < 200_000 {
            if let Ok(b) = a.download().await {
                text.push('\n');
                text.push_str(&String::from_utf8_lossy(&b));
            }
        }
    }
    text
}

fn speaker(m: &Message) -> String {
    m.member.as_ref().and_then(|x| x.nick.clone()).unwrap_or_else(|| m.author.display_name().to_string())
}

fn name_reply(culture: &str, branch: &str, lineage: &str, sex: &str) -> Result<Embed, String> {
    let label = names::CULTURES.iter().find(|(k, _)| *k == culture).map_or(culture, |(_, v)| v);
    names::build(culture, random_seed(), branch, lineage, sex).map(|d| embeds::name_embed(&d, label))
}

fn stats_reply(level: i64) -> Result<Embed, String> {
    let mut leans: Vec<Option<String>> = fow::primaries().into_iter().map(Some).collect();
    leans.push(None);
    let lean = leans[(random_seed() as usize) % leans.len()].clone();
    fow::build(level, lean.as_deref(), random_seed()).map(|d| embeds::stat_embed(&d))
}

fn open_hit(h: &Value, wiki: bool, page: usize) -> Vec<Embed> {
    if wiki {
        let (title, text, url, cat) = look::wiki_page(h["rel"].as_str().unwrap_or(""));
        let foot = format!("wiki mirror{}", if url.is_some() { " \u{b7} title links to Notion" } else { "" });
        embeds::pages(&text, page, &title, C_WIKI, url.as_deref(), &foot, &cat)
    } else {
        let file = h["file"].as_str().unwrap_or("");
        let (title, text) = look::scene_text(file);
        embeds::pages(&text, page, &title, C_SCENE, None, file, "scene archive")
    }
}

/// Run a blocking read off the gateway's threads, so the heartbeat never waits on disk.
async fn off<T: Send + 'static>(f: impl FnOnce() -> T + Send + 'static) -> Result<T, String> {
    tokio::task::spawn_blocking(f).await.map_err(|e| e.to_string())
}

impl Bot {
    async fn dispatch(&self, itx: &Itx, c: &CommandInteraction) -> Result<(), String> {
        let top = c.data.options();
        let (name, o): (String, Vec<ResolvedOption>) = match top.first().map(|x| &x.value) {
            Some(ResolvedValue::SubCommand(inner)) => (format!("{} {}", c.data.name, top[0].name), inner.clone()),
            _ => (c.data.name.clone(), top.clone()),
        };
        let s = |k: &str| opt_str(&o, k);
        match name.as_str() {
            "wiki" | "recall" => {
                itx.defer(false).await?;
                let wiki = name == "wiki";
                let q = s("query").unwrap_or_default();
                let q2 = q.clone();
                let hits = off(move || if wiki { look::wiki_hits(&q2, 5) } else { look::scene_hits(&q2, 4) }).await?;
                let mut m = Msg::embed(embeds::hits_embed(&q, &hits, wiki, &look::commit_hash()));
                if !hits.is_empty() {
                    m.view = Some(View::OpenHit { hits, wiki });
                }
                itx.send(self, m).await
            }
            "define" => self.define(itx, s("term").unwrap_or_default()).await,
            "character" => {
                itx.defer(false).await?;
                let n = s("name").unwrap_or_default();
                let n2 = n.clone();
                let Some(card) = off(move || look::card(&n2)).await? else {
                    return itx.send(self, Msg::private(format!("No card for **{n}** in the wiki mirror. Check Notion before writing anything numeric about them."))).await;
                };
                let first = embeds::card_overview(&card, self.page);
                let mut m = Msg::embed(first.clone());
                m.view = Some(View::Card { card: Arc::new(card), pages: vec![first], i: 0 });
                itx.send(self, m).await
            }
            "fow" => {
                itx.defer(false).await?;
                let n = s("name").unwrap_or_default();
                let n2 = n.clone();
                match off(move || look::fow_card(&n2)).await? {
                    Some(d) => itx.send(self, Msg::embed(embeds::fow_embed(&d))).await,
                    None => itx.send(self, Msg::private(format!("No card for **{n}** in the wiki mirror."))).await,
                }
            }
            "timeline" => {
                itx.defer(false).await?;
                let text = off(look::timeline).await??;
                itx.send(self, Msg::paged(embeds::pages(&text, self.page, "Timeline", C_SCENE, None, "scenes/TIMELINE.md", ""), false)).await
            }
            "whoami" => {
                let role = self.role(itx).await;
                itx.send(self, Msg::private(format!("{}: table role **{role}** \u{b7} index @ `{}`", itx.user.mention(), look::commit_hash()))).await
            }
            "name" => {
                let (culture, branch, lineage, sex) = (s("culture").unwrap_or_default(), s("branch").unwrap_or_default(), s("lineage").unwrap_or_default(), s("sex").unwrap_or_default());
                let e = name_reply(&culture, &branch, &lineage, &sex)?;
                let mut m = Msg::embed(e);
                m.view = Some(View::RerollName { culture, branch, lineage, sex });
                itx.send(self, m).await
            }
            "name_help" => {
                let mut e = Embed::new("What /name can build", C_NAME);
                e.description = Some(names::CULTURES.iter().map(|(k, v)| format!("\u{2022} **{v}** \u{2014} `{}`", names::BANK[*k]["rule"].as_str().unwrap_or(""))).collect::<Vec<_>>().join("\n"));
                let not: Vec<String> = names::NOT_OFFERED.iter().map(|(k, v)| format!("\u{2022} **{}** \u{2014} {v}", title_word(k))).collect();
                e.field("Not offered (no ratified element bank \u{2014} the bot will not coin one)", &clip(&not.join("\n"), FIELD_MAX), false);
                itx.send(self, Msg { embed: Some(e), ephemeral: true, ..Default::default() }).await
            }
            "stats" => {
                let level = opt_int(&o, "level").unwrap_or(1);
                let mut m = Msg::embed(stats_reply(level)?);
                m.view = Some(View::RerollStats { level });
                itx.send(self, m).await
            }
            "narrate" => self.narrate(itx, s("scene").unwrap_or_default(), s("engine")).await,
            "scene save" => self.scene_save(itx, s("title"), s("source").unwrap_or_else(|| "thread".into()), s("link"), opt_int(&o, "count")).await,
            "event add" => self.event_add(itx, &o).await,
            "event list" => self.event_list(itx).await,
            "event done" => self.event_done(itx, s("id").unwrap_or_default()).await,
            "sheet" => self.sheet_cmd(itx, s("link")).await,
            "verify" => self.verify(itx, s("link"), opt_bool(&o, "combat"), s("culture").unwrap_or_default(), s("band").unwrap_or_else(|| "standard".into())).await,
            "date today" => self.date_today(itx).await,
            "date set" => self.date_set(itx, &o).await,
            "date advance" => self.date_advance(itx, opt_int(&o, "days").unwrap_or(1)).await,
            "date name" => {
                let (month, day, plus) = (opt_int(&o, "month").unwrap_or(1), opt_int(&o, "day").unwrap_or(1), opt_int(&o, "plus").unwrap_or(0));
                let (m2, d2, _) = desk::add_days(month, day, 0, plus);
                let mut text = desk::describe(month, day, None, "");
                if plus != 0 {
                    text += &format!("\n+{plus} days \u{2192} {}", desk::describe(m2, d2, None, ""));
                }
                let mut e = Embed::new("The Sky, the Hour and the Year", C_NAME);
                e.description = Some(text);
                e.field("The turn", &desk::ARCHONS.iter().enumerate().map(|(i, (a, p))| format!("{} {a}'s ({p})", i + 1)).collect::<Vec<_>>().join(" \u{b7} "), false);
                itx.send(self, Msg::embed(e)).await
            }
            "ledger" => self.lines(itx, false).await,
            "due" => self.lines(itx, true).await,
            "roster" => {
                let th = s("thread").unwrap_or_default();
                let th2 = th.clone();
                let rows = off(move || desk::roster(&th2)).await??;
                let (title, miss) = if th.is_empty() { ("Roster".to_string(), "No NPC on the roster.".to_string()) } else { (format!("Roster \u{b7} {th}"), format!("No NPC on the roster for {th}.")) };
                self.faces(itx, rows, &title, miss).await
            }
            "npc" => {
                let n = s("name").unwrap_or_default();
                let key = n.trim().to_lowercase();
                let rows: Vec<Value> = off(|| desk::roster("")).await??.into_iter().filter(|r| !key.is_empty() && table::s(r.get("name")).to_lowercase().contains(&key)).collect();
                self.faces(itx, rows, &n, format!("No NPC on the roster matches **{n}**.")).await
            }
            o => Err(format!("no such command {o}")),
        }
    }

    async fn define(&self, itx: &Itx, term: String) -> Result<(), String> {
        itx.defer(false).await?;
        let t = term.clone();
        let hits = off(move || look::define(&t, 5)).await?;
        let mut e = Embed::new(&clip(&term, 256), C_WIKI);
        let link = |h: &Value| h["url"].as_str().map_or(String::new(), |u| format!(" \u{b7} [Notion]({u})"));
        if !hits.is_empty() {
            for h in &hits {
                e.field(&clip(h["page"].as_str().unwrap_or(""), 256), &clip(&format!("-# {}{}\n{}", h["category"].as_str().unwrap_or(""), link(h), h["text"].as_str().unwrap_or("")), FIELD_MAX), false);
            }
            e.set_footer("the wiki's own defining lines, verbatim \u{b7} /wiki for wider search");
            return itx.send(self, Msg::embed(e)).await;
        }
        let t = term.clone();
        let ment = off(move || look::wiki_hits(&t, 3)).await?;
        if ment.is_empty() {
            return itx.send(self, Msg::private(format!("The wiki neither defines nor mentions **{term}**."))).await;
        }
        e.description = Some(format!("No page defines **{term}** outright. Where it appears:"));
        for h in &ment {
            e.field(&clip(h["title"].as_str().unwrap_or(""), 256), &clip(&format!("-# {}{}\n{}", h["category"].as_str().unwrap_or(""), link(h), h["snippet"].as_str().unwrap_or("")), FIELD_MAX), false);
        }
        e.set_footer("mentions only \u{b7} /wiki to open a page");
        itx.send(self, Msg::embed(e)).await
    }

    async fn lines(&self, itx: &Itx, come_due: bool) -> Result<(), String> {
        itx.defer(true).await?;
        let everyone = self.judge(itx).await;
        let names = desk::owned(&self.cfg, itx.user.id.get());
        if !everyone && names.is_empty() {
            return itx.send(self, Msg::private("No characters are on file for you (bot/config.yaml, players:). Ask the Judger to add yours.")).await;
        }
        let mut rows = off(move || desk::ledger_rows(come_due)).await??;
        if !everyone {
            rows.retain(|r| desk::mine(r, &names));
        }
        let title = if come_due { "Come due" } else { "Ledger" };
        let whose = if everyone { "every line (Judger's view)".to_string() } else { format!("lines about {}", names.join(", ")) };
        if rows.is_empty() {
            return itx.send(self, Msg::private(format!("{title}: nothing open in {whose}."))).await;
        }
        let body = rows.iter().map(desk::ledger_line).collect::<Vec<_>>().join("\n");
        itx.send(self, Msg::paged(embeds::pages(&body, self.page, title, C_STAT, None, &format!("table/ledger.yaml \u{b7} {whose} \u{b7} R72-40"), ""), true)).await
    }

    async fn faces(&self, itx: &Itx, rows: Vec<Value>, title: &str, miss: String) -> Result<(), String> {
        if rows.is_empty() {
            return itx.send(self, Msg::private(miss)).await;
        }
        let body = rows.iter().map(desk::face).collect::<Vec<_>>().join("\n");
        itx.send(self, Msg::paged(embeds::pages(&body, self.page, title, C_CARD, None, "table/npcs.yaml \u{b7} public face only: name, look, voice, role \u{b7} R72-40", ""), false)).await
    }

    async fn sheet_cmd(&self, itx: &Itx, link: Option<String>) -> Result<(), String> {
        itx.defer(false).await?;
        let found = match &link {
            Some(l) => match message_link(l) {
                Some((ch, id)) => Some(ch.message(&itx.http, id).await.map_err(|e| e.to_string())?),
                None => None,
            },
            None if itx.thread => itx.channel.message(&itx.http, MessageId::new(itx.channel.get())).await.ok(),
            None => None,
        };
        let Some(msg) = found else {
            return itx.send(self, Msg::private("Run this inside the sheet's thread, or pass a message link.")).await;
        };
        let text = message_text(&msg, false).await;
        let res = off(move || sheet::check(&text)).await?;
        itx.send(self, Msg::embed(embeds::sheet_embed(&res, &speaker(&msg)))).await
    }

    async fn run_verify(&self, itx: &Itx, md: String, combat: bool, culture: String, band: String) -> Result<(), String> {
        let args = json!({"markdown": md, "combat": combat, "culture": culture, "band": band});
        let report = tool_text(self.tools.call("verify_scene", args.as_object().cloned().unwrap_or_default()).await?);
        let foot = format!("{} words \u{b7} {} \u{b7} {} \u{b7} {band}", commas(md.split_whitespace().count() as i64), if combat { "combat" } else { "standard" }, if culture.is_empty() { "no culture" } else { &culture });
        itx.send(self, Msg::paged(embeds::pages(&report, self.page, "Verification", C_STAT, None, &foot, ""), false)).await
    }

    async fn verify(&self, itx: &Itx, link: Option<String>, combat: bool, culture: String, band: String) -> Result<(), String> {
        let Some(link) = link.filter(|l| !l.is_empty()) else {
            let id = self.remember(View::Verify { combat, culture, band });
            return show_modal(itx, id, "Verify a scene").await;
        };
        let Some((ch, id)) = message_link(&link) else {
            return itx.send(self, Msg::private("That is not a message link.")).await;
        };
        itx.defer(false).await?;
        let msg = ch.message(&itx.http, id).await.map_err(|e| e.to_string())?;
        let text = message_text(&msg, false).await;
        if text.split_whitespace().count() < 20 {
            return itx.send(self, Msg::private("Fewer than twenty words there (if it is someone else's post, the bot needs the Message Content intent to read it).")).await;
        }
        self.run_verify(itx, text, combat, culture, band).await
    }

    async fn present(&self, itx: &Itx, title: String, md: String, script: String, notes: String) -> Result<(), String> {
        let args = json!({"markdown": md});
        let report = tool_text(self.tools.call("verify_scene", args.as_object().cloned().unwrap_or_default()).await?);
        let words = md.split_whitespace().count();
        let mut head = Embed::new(&format!("Scene: {title}"), C_SCENE);
        head.description = Some(clip(&format!("{} words \u{b7} {notes}\n\n**Verification**\n{report}", commas(words as i64)), DESC_MAX));
        let file = (md.clone().into_bytes(), format!("{}.md", writers::slug_us(&title)));
        itx.send(self, Msg { embed: Some(head), file: Some(file), view: Some(View::Archive { title, md, script, notes }), ..Default::default() }).await
    }

    async fn scene_save(&self, itx: &Itx, title: Option<String>, source: String, link: Option<String>, count: Option<i64>) -> Result<(), String> {
        let title = title.or(itx.channel_name.clone()).unwrap_or_default().trim().to_string();
        if title.is_empty() {
            return itx.send(self, Msg::private("Give the scene a title.")).await;
        }
        if source == "paste" {
            let id = self.remember(View::Paste { title });
            return show_modal(itx, id, "Paste the scene").await;
        }
        itx.defer(false).await?;
        let after = if source == "link" {
            let Some(m) = caps(re!(r"https://(?:\w+\.)?discord(?:app)?\.com/channels/(\d+)/(\d+)/(\d+)"), link.as_deref().unwrap_or("")) else {
                return itx.send(self, Msg::private("Give a message link (right-click a message \u{2192} Copy Message Link).")).await;
            };
            Some(group(&m, 3).parse::<u64>().map_err(|e| e.to_string())? - 1)
        } else {
            None
        };
        let msgs = history(&itx.http, itx.channel, after, count.map(|c| c as usize)).await?;
        let posts: Vec<Post> = msgs.iter().map(|m| Post { content: m.content.clone(), speaker: speaker(m), from_bot: m.author.bot, webhook: m.webhook_id.is_some(), ordinary: matches!(m.kind, MessageType::Regular | MessageType::InlineReply) }).collect();
        let (md, script, speakers) = look::compile_scene(&title, &posts);
        if md.split_whitespace().count() < 20 {
            return itx.send(self, Msg::private("Fewer than twenty words of in-character text found here.")).await;
        }
        let notes = format!("Saved from Discord #{} on {} by {}; voices: {}.", itx.channel_name.as_deref().unwrap_or("?"), today(), itx.display_name(), speakers.join(", "));
        self.present(itx, title, md, script, notes).await
    }

    async fn event_add(&self, itx: &Itx, o: &[ResolvedOption<'_>]) -> Result<(), String> {
        if !self.judge(itx).await {
            return itx.send(self, Msg::private("Events are entered by the Judger or a Scribe.")).await;
        }
        itx.defer(false).await?;
        let get = |k: &str| opt_str(o, k).unwrap_or_default();
        let (title, when, where_, who, blurb) = (get("title"), get("when"), get("where"), get("who"), get("blurb"));
        let by = itx.display_name();
        let (id, pushed) = {
            let _g = self.lock.lock().await;
            let (t, wh, wr, w, b) = (title.clone(), when.clone(), where_.clone(), who.clone(), blurb.clone());
            off(move || -> Result<(String, String), String> {
                let mut rows = table::load("events")?;
                let eid = format!("E{:03}", rows.len() + 1);
                rows.push(json!({"id": eid, "title": t, "when": wh, "where": wr, "who": w, "blurb": b, "entered": today(), "by": by, "status": "upcoming"}));
                writers::save("events", &rows);
                let pushed = writers::table_commit(&format!("Event {eid}: {t}")).map_err(|e| e.to_string())?;
                Ok((eid, pushed))
            }).await??
        };
        let mut e = Embed::new(&format!("{id} \u{2014} {title}"), C_NAME);
        e.description = Some(clip(&blurb, DESC_MAX)).filter(|d| !d.is_empty());
        e.field("When", &when, true);
        e.field("Where", &where_, true);
        if !who.is_empty() {
            e.field("Who", &clip(&who, FIELD_MAX), false);
        }
        e.set_footer(&format!("table/events.yaml \u{b7} {pushed}"));
        let log = self.cfg["channels"]["event_log"].as_u64().unwrap_or(0);
        if log != 0 && log != itx.channel.get() {
            let _ = ChannelId::new(log).send_message(&itx.http, CreateMessage::new().embed(to_embed(&e))).await;
        }
        itx.send(self, Msg::embed(e)).await
    }

    async fn event_list(&self, itx: &Itx) -> Result<(), String> {
        let rows: Vec<Value> = off(|| table::load("events")).await??.into_iter().filter(|r| r.get("status").and_then(Value::as_str) == Some("upcoming")).collect();
        if rows.is_empty() {
            return itx.send(self, Msg::private("No upcoming events on the table.")).await;
        }
        let body = rows.iter().map(|r| {
            let who = table::s(r.get("who"));
            format!("**{} \u{2014} {}**\n{} \u{b7} {}{}", table::s(r.get("id")), table::s(r.get("title")), table::s(r.get("when")), table::s(r.get("where")), if who.is_empty() { String::new() } else { format!(" \u{b7} {who}") })
        }).collect::<Vec<_>>().join("\n\n");
        itx.send(self, Msg::paged(embeds::pages(&body, self.page, "Upcoming events", C_NAME, None, "table/events.yaml", ""), false)).await
    }

    async fn event_done(&self, itx: &Itx, id: String) -> Result<(), String> {
        if !self.judge(itx).await {
            return itx.send(self, Msg::private("Events are closed by the Judger or a Scribe.")).await;
        }
        itx.defer(false).await?;
        let key = id.to_uppercase();
        let done = {
            let _g = self.lock.lock().await;
            let key = key.clone();
            off(move || -> Result<Option<(String, String)>, String> {
                let mut rows = table::load("events")?;
                let Some(r) = rows.iter_mut().find(|r| table::s(r.get("id")).to_uppercase() == key) else { return Ok(None) };
                r["status"] = json!("happened");
                let (rid, title) = (table::s(r.get("id")), table::s(r.get("title")));
                writers::save("events", &rows);
                let pushed = writers::table_commit(&format!("Event {rid} happened: {title}")).map_err(|e| e.to_string())?;
                Ok(Some((title, pushed)))
            }).await??
        };
        itx.send(self, Msg::text(match done {
            Some((title, pushed)) => format!("**{key}** \u{2014} {title}: happened \u{b7} {pushed}"),
            None => format!("No event {id}."),
        })).await
    }

    async fn date_today(&self, itx: &Itx) -> Result<(), String> {
        let d = off(desk::calendar).await?;
        if d.is_empty() {
            return itx.send(self, Msg::private("No date is set on the table yet \u{2014} the Judger sets it with `/date set`.")).await;
        }
        let num = |k: &str| d.get(k).and_then(Value::as_i64);
        let mut e = Embed::new("Today", C_NAME);
        e.description = Some(desk::describe(num("month").unwrap_or(1), num("day").unwrap_or(1), num("year"), d.get("era").and_then(Value::as_str).unwrap_or("")));
        let by = d.get("by").and_then(Value::as_str).unwrap_or("?");
        let on = d.get("set_on").map_or("?".to_string(), |v| v.as_str().map_or_else(|| v.to_string(), String::from));
        e.set_footer(&format!("set by {by} on {on} \u{b7} The Sky, the Hour and the Year"));
        itx.send(self, Msg::embed(e)).await
    }

    async fn date_set(&self, itx: &Itx, o: &[ResolvedOption<'_>]) -> Result<(), String> {
        if !self.judge(itx).await {
            return itx.send(self, Msg::private("The Judger or a Scribe sets the date.")).await;
        }
        let (month, year) = (opt_int(o, "month").unwrap_or(1), opt_int(o, "year"));
        let day = if month == 14 { 1 } else { opt_int(o, "day").unwrap_or(1) };
        let era = opt_str(o, "era").unwrap_or_default();
        let mut d = Map::new();
        for (k, v) in [("month", json!(month)), ("day", json!(day)), ("year", json!(year)), ("era", json!(era)), ("by", json!(itx.display_name())), ("set_on", json!(today()))] {
            d.insert(k.into(), v);
        }
        let pushed = off(move || -> Result<String, String> {
            desk::save_calendar(&d)?;
            writers::table_commit("Calendar set").map_err(|e| e.to_string())
        }).await??;
        itx.send(self, Msg::text(format!("Set: {} \u{b7} {pushed}", desk::describe(month, day, year, &era)))).await
    }

    async fn date_advance(&self, itx: &Itx, days: i64) -> Result<(), String> {
        if !self.judge(itx).await {
            return itx.send(self, Msg::private("The Judger or a Scribe advances the date.")).await;
        }
        let mut d = off(desk::calendar).await?;
        let num = |d: &Map<String, Value>, k: &str| d.get(k).and_then(Value::as_i64);
        if d.is_empty() || num(&d, "month") == Some(14) {
            return itx.send(self, Msg::private("Set a calendar date first (`/date set`).")).await;
        }
        let (m, dd, y) = desk::add_days(num(&d, "month").unwrap_or(1), num(&d, "day").unwrap_or(1), num(&d, "year").unwrap_or(0), days);
        let year = (y != 0).then_some(y);
        for (k, v) in [("month", json!(m)), ("day", json!(dd)), ("year", json!(year)), ("by", json!(itx.display_name())), ("set_on", json!(today()))] {
            d.insert(k.into(), v);
        }
        let era = d.get("era").and_then(Value::as_str).unwrap_or("").to_string();
        let pushed = off(move || -> Result<String, String> {
            desk::save_calendar(&d)?;
            writers::table_commit(&format!("Calendar advanced {days} day(s)")).map_err(|e| e.to_string())
        }).await??;
        itx.send(self, Msg::text(format!("Now: {} \u{b7} {pushed}", desk::describe(m, dd, year, &era)))).await
    }

    async fn narrate(&self, itx: &Itx, scene: String, engine: Option<String>) -> Result<(), String> {
        let role = self.role(itx).await;
        if !matches!(role, "judger" | "scribe") {
            return itx.send(self, Msg::private("Narration is for the Judger and Scribes \u{2014} it costs CPU or ElevenLabs credit.")).await;
        }
        let q = scene.clone();
        let (path, cands) = off(move || analysis::find_scene(&q)).await?;
        let Some(path) = path else {
            let msg = if cands.is_empty() { format!("No scene matches **{scene}**.") } else { format!("More than one scene matches:\n{}", cands.iter().take(10).map(|c| format!("\u{2022} {c}")).collect::<Vec<_>>().join("\n")) };
            return itx.send(self, Msg::private(msg)).await;
        };
        let text = read_lossy(&path);
        let (words, chars) = (text.split_whitespace().count(), text.chars().count());
        let st = crate::util::stem(&path);
        if let Some(engine) = engine {
            itx.send(self, Msg::text(format!("Rendering **{st}** on **{engine}**\u{2026}"))).await?;
            return self.render(itx, path, engine).await;
        }
        let mut e = Embed::new(&format!("Narrate {st}?"), C_SCENE);
        e.description = Some(format!("{} words. **Local** is free and takes a few minutes on the PC; **ElevenLabs** bills about {} characters to the plan and is quicker.", commas(words as i64), commas(chars as i64)));
        itx.send(self, Msg { embed: Some(e), view: Some(View::Engine { path, allow_eleven: role == "judger", words, chars }), ..Default::default() }).await
    }

    async fn render(&self, itx: &Itx, path: PathBuf, engine: String) -> Result<(), String> {
        let name = path.file_name().map_or(String::new(), |n| n.to_string_lossy().into_owned());
        let st = crate::util::stem(&path);
        let say = |t: String| {
            let (http, ch) = (itx.http.clone(), itx.channel);
            async move {
                let _ = ch.say(&http, t).await;
            }
        };
        let args = json!({"scene": name, "voice": "narrator", "engine": engine});
        let reply = tool_text(self.tools.call("narrate_scene", args.as_object().cloned().unwrap_or_default()).await?);
        let Some(job) = caps(re!(r"job (\d{8}-\d{6})"), &reply).map(|m| group(&m, 1).to_string()) else {
            say(format!("Could not start the render: {}", clip(&reply, 1500))).await;
            return Ok(());
        };
        say(format!("\u{1f399} {}", reply.split(" Output folder").next().unwrap_or(""))).await;
        let (mut waited, mut state) = (0, "running".to_string());
        while waited < NARRATE_MAX {
            tokio::time::sleep(Duration::from_secs(NARRATE_POLL)).await;
            waited += NARRATE_POLL;
            let j = job.clone();
            state = off(move || crate::jobs::job_state_by_id(&j)).await?;
            if state == "done" || state == "failed" {
                break;
            }
        }
        if state != "done" {
            say(format!("Render **{st}** ({engine}) {state} after {} min \u{2014} see `build/.narrate-{job}.log`.", waited / 60)).await;
            return Ok(());
        }
        let j = job.clone();
        let Some(out) = off(move || crate::jobs::job_output(&j)).await? else {
            say(format!("Render **{st}** finished but the file was not found in the audio folder.")).await;
            return Ok(());
        };
        // the server's limit depends on its boosts: Discord answers for it, and a refusal names the file instead
        let size = std::fs::metadata(&out).map(|m| m.len()).unwrap_or(0);
        let file_name = out.file_name().map_or(String::new(), |n| n.to_string_lossy().into_owned());
        let sent = match std::fs::read(&out) {
            Ok(b) => itx.channel.send_message(&itx.http, CreateMessage::new().content(format!("**{st}** \u{2014} {engine}")).add_file(CreateAttachment::bytes(b, file_name.clone()))).await.is_ok(),
            Err(_) => false,
        };
        if !sent {
            say(format!("**{st}** \u{2014} {engine}: {} MB, over this server's upload limit; it is in the audio folder as `{file_name}`.", size / 1_000_000)).await;
        }
        Ok(())
    }

    async fn component(&self, itx: &Itx, c: &ComponentInteraction) -> Result<(), String> {
        let mut parts = c.data.custom_id.splitn(3, ':');
        let (_, id, action) = (parts.next(), parts.next().and_then(|x| x.parse::<u64>().ok()).unwrap_or(0), parts.next().unwrap_or(""));
        let Some(view) = self.view(id) else {
            return itx.send(self, Msg::private("This has timed out. Run the command again.")).await;
        };
        let value = match &c.data.kind {
            ComponentInteractionDataKind::StringSelect { values } => values.first().cloned().unwrap_or_default(),
            _ => String::new(),
        };
        match view {
            View::Pager { pages, i } => {
                let i = if action == "prev" { (i + pages.len() - 1) % pages.len() } else { (i + 1) % pages.len() };
                let v = View::Pager { pages: pages.clone(), i };
                self.set_view(id, v.clone());
                itx.update(self, Some(id), Msg { embed: Some(pages[i].clone()), view: Some(v), ..Default::default() }).await
            }
            View::OpenHit { hits, wiki } => {
                let h = hits.get(value.parse::<usize>().unwrap_or(0)).cloned().unwrap_or(Value::Null);
                let page = self.page;
                let pages = off(move || open_hit(&h, wiki, page)).await?;
                let mut m = Msg::paged(pages, false);
                m.ephemeral = false;
                itx.update(self, None, m).await
            }
            View::RerollName { culture, branch, lineage, sex } => {
                let e = name_reply(&culture, &branch, &lineage, &sex)?;
                itx.update(self, Some(id), Msg { embed: Some(e), view: Some(View::RerollName { culture, branch, lineage, sex }), ..Default::default() }).await
            }
            View::RerollStats { level } => itx.update(self, Some(id), Msg { embed: Some(stats_reply(level)?), view: Some(View::RerollStats { level }), ..Default::default() }).await,
            View::Card { card, pages, i } => {
                let (pages, i) = if action == "jump" {
                    let n: i64 = value.parse().unwrap_or(-1);
                    (if n < 0 { vec![embeds::card_overview(&card, self.page)] } else { embeds::card_section(&card, n as usize, self.page) }, 0)
                } else if action == "prev" {
                    let i = (i + pages.len() - 1) % pages.len();
                    (pages, i)
                } else {
                    let i = (i + 1) % pages.len();
                    (pages, i)
                };
                let first = pages[i].clone();
                let v = View::Card { card, pages, i };
                self.set_view(id, v.clone());
                itx.update(self, Some(id), Msg { embed: Some(first), view: Some(v), ..Default::default() }).await
            }
            View::Archive { title, md, script, notes } => {
                if action == "cancel" {
                    return itx.update(self, None, Msg::text("Not archived.")).await;
                }
                if !self.judge(itx).await {
                    return itx.send(self, Msg::private("Only the Judger or a Scribe archives.")).await;
                }
                itx.update(self, None, Msg::default()).await?;
                let (reply, note) = {
                    let _g = self.lock.lock().await;
                    let args = json!({"title": title, "markdown": md, "author_notes": notes});
                    let reply = tool_text(self.tools.call("archive_scene", args.as_object().cloned().unwrap_or_default()).await?);
                    let mut note = String::new();
                    if let (Some(m), false) = (caps(re!(r"saved (scenes/\S+\.md)"), &reply), script.is_empty()) {
                        let file = group(&m, 1).rsplit('/').next().unwrap_or("").to_string();
                        let args = json!({"scene": file, "script": script});
                        let out = tool_text(self.tools.call("cast_scene", args.as_object().cloned().unwrap_or_default()).await?);
                        note = format!("\n{}", out.chars().take(400).collect::<String>());
                    }
                    (reply, note)
                };
                itx.send(self, Msg::text(format!("\u{1f4dc} {reply}{note}"))).await
            }
            View::Engine { path, .. } => {
                itx.update(self, None, Msg::default()).await?;
                self.render(itx, path, action.to_string()).await
            }
            View::Paste { .. } | View::Verify { .. } => Ok(()),
        }
    }

    async fn modal(&self, itx: &Itx, m: &ModalInteraction) -> Result<(), String> {
        let text = m.data.components.iter().flat_map(|r| &r.components).find_map(|c| match c {
            ActionRowComponent::InputText(t) => t.value.clone(),
            _ => None,
        }).unwrap_or_default();
        let id = m.data.custom_id.strip_prefix("v:").and_then(|x| x.parse().ok()).unwrap_or(0);
        match self.view(id) {
            Some(View::Verify { combat, culture, band }) => {
                itx.defer(false).await?;
                self.run_verify(itx, text, combat, culture, band).await
            }
            Some(View::Paste { title }) => {
                let md = format!("# {title}\n\n{}\n", text.trim());
                let notes = format!("Pasted into Discord by {} on {}.", itx.display_name(), today());
                self.present(itx, title, md, String::new(), notes).await
            }
            _ => itx.send(self, Msg::private("This has timed out. Run the command again.")).await,
        }
    }
}

fn title_word(s: &str) -> String {
    // str.title(): after any non-letter a capital, so undaar-keth reads Undaar-Keth
    let mut prev = false;
    s.chars().map(|c| {
        let out = if prev { c.to_ascii_lowercase() } else { c.to_ascii_uppercase() };
        prev = c.is_alphabetic();
        out
    }).collect()
}

async fn show_modal(itx: &Itx, id: u64, title: &str) -> Result<(), String> {
    let input = CreateInputText::new(InputTextStyle::Paragraph, "Scene text (markdown)", "text").max_length(4000);
    let form = CreateModal::new(format!("v:{id}"), title).components(vec![CreateActionRow::InputText(input)]);
    itx.done.store(true, Ordering::Relaxed);
    CreateInteractionResponse::Modal(form).execute(&itx.http, (itx.id, &itx.token)).await.map_err(|e| e.to_string())
}

/// Messages in reading order: everything after `after`, or the most recent `limit`, or all of them.
async fn history(http: &Http, ch: ChannelId, after: Option<u64>, limit: Option<usize>) -> Result<Vec<Message>, String> {
    let mut out: Vec<Message> = Vec::new();
    if let Some(mut cursor) = after {
        loop {
            let take = limit.map_or(100, |l| (l - out.len()).min(100)) as u8;
            let mut page = ch.messages(http, GetMessages::new().after(MessageId::new(cursor.max(1))).limit(take)).await.map_err(|e| e.to_string())?;
            if page.is_empty() {
                break;
            }
            page.sort_by_key(|m| m.id);
            cursor = page.last().map_or(cursor, |m| m.id.get());
            out.extend(page);
            if limit.is_some_and(|l| out.len() >= l) {
                break;
            }
        }
        return Ok(out);
    }
    let mut before: Option<MessageId> = None;
    loop {
        let take = limit.map_or(100, |l| (l - out.len()).min(100)) as u8;
        let mut q = GetMessages::new().limit(take);
        if let Some(b) = before {
            q = q.before(b);
        }
        let page = ch.messages(http, q).await.map_err(|e| e.to_string())?;
        if page.is_empty() {
            break;
        }
        before = page.last().map(|m| m.id);
        out.extend(page);
        if limit.is_some_and(|l| out.len() >= l) {
            break;
        }
    }
    out.reverse();
    Ok(out)
}

#[async_trait]
impl EventHandler for Bot {
    async fn ready(&self, ctx: Context, ready: Ready) {
        println!("online as {} ({}) in {} guild(s)", ready.user.name, ready.user.id, ready.guilds.len());
        if self.sync {
            let guild = GuildId::new(self.cfg["guild_id"].as_u64().unwrap_or(1));
            match guild.set_commands(&ctx.http, definitions()).await {
                Ok(c) => println!("synced {} commands to guild {guild}: {}", c.len(), c.iter().map(|x| x.name.as_str()).collect::<Vec<_>>().join(", ")),
                Err(e) => eprintln!("sync failed: {e}"),
            }
        }
    }

    async fn thread_create(&self, ctx: Context, thread: GuildChannel) {
        // a new post in the submission forum: check its opening message
        let forum = self.cfg["channels"]["character_submission"].as_u64().unwrap_or(0);
        if forum == 0 || thread.parent_id.map(|p| p.get()) != Some(forum) {
            return;
        }
        // serenity drops the gateway's newly_created flag; an old thread arriving here is the bot being added to it
        if Timestamp::now().unix_timestamp() - thread.id.created_at().unix_timestamp() > 60 {
            return;
        }
        tokio::time::sleep(Duration::from_secs(2)).await; // the starter message lands just after the thread
        let Ok(starter) = thread.id.message(&ctx.http, MessageId::new(thread.id.get())).await else { return };
        let text = message_text(&starter, true).await;
        let Ok(res) = off(move || sheet::check(&text)).await else { return };
        let _ = thread.id.send_message(&ctx.http, CreateMessage::new().embed(to_embed(&embeds::sheet_embed(&res, &speaker(&starter))))).await;
    }

    async fn interaction_create(&self, ctx: Context, interaction: Interaction) {
        let make = |id: InteractionId, token: &str, user: &User, member: Option<Box<Member>>, guild: Option<GuildId>, channel: ChannelId, name: Option<String>, thread: bool| Itx {
            http: ctx.http.clone(), id, token: token.to_string(), done: AtomicBool::new(false), user: user.clone(), member, guild, channel, channel_name: name, thread,
        };
        let (itx, result) = match &interaction {
            Interaction::Command(c) => {
                let (name, thread) = c.channel.as_ref().map_or((None, false), |p| (p.name.clone(), matches!(p.kind, ChannelType::PublicThread | ChannelType::PrivateThread | ChannelType::NewsThread)));
                let itx = make(c.id, &c.token, &c.user, c.member.clone(), c.guild_id, c.channel_id, name, thread);
                let r = self.dispatch(&itx, c).await;
                (itx, r)
            }
            Interaction::Autocomplete(c) => {
                let focused = c.data.autocomplete().map(|a| a.value.to_string()).unwrap_or_default();
                let names = if c.data.name == "narrate" {
                    scene_choices(&focused)
                } else {
                    off(move || look::character_names(&focused, 25)).await.unwrap_or_default()
                };
                let mut r = CreateAutocompleteResponse::new();
                for n in names {
                    let n: String = n.chars().take(100).collect();
                    r = r.add_string_choice(n.clone(), n);
                }
                let _ = CreateInteractionResponse::Autocomplete(r).execute(&ctx.http, (c.id, &c.token)).await;
                return;
            }
            Interaction::Component(c) => {
                let itx = make(c.id, &c.token, &c.user, c.member.clone().map(Box::new), c.guild_id, c.channel_id, None, false);
                let r = self.component(&itx, c).await;
                (itx, r)
            }
            Interaction::Modal(m) => {
                let itx = make(m.id, &m.token, &m.user, m.member.clone().map(Box::new), m.guild_id, m.channel_id, None, false);
                let r = self.modal(&itx, m).await;
                (itx, r)
            }
            _ => return,
        };
        if let Err(e) = result {
            eprintln!("command failed: {e}");
            let msg: String = format!("That failed: `{e}`").chars().take(1900).collect();
            let _ = itx.send(self, Msg::private(msg)).await;
        }
    }
}

fn scene_choices(current: &str) -> Vec<String> {
    let key = current.to_lowercase();
    let mut names: Vec<String> = std::fs::read_dir(root("scenes")).into_iter().flatten().flatten().map(|e| e.file_name().to_string_lossy().into_owned()).filter(|n| n.ends_with(".md") && n.to_lowercase().contains(&key) && !matches!(n.as_str(), "MANIFEST.md" | "ARCS.md" | "CAST.md" | "TIMELINE.md")).collect();
    names.sort();
    names.truncate(25);
    names
}

/// `wotr-mcp bot [--sync]`: connect and stay connected until the process is stopped.
pub async fn main(args: &[String]) -> i32 {
    let Some(token) = crate::util::env("DISCORD_TOKEN") else {
        eprintln!("DISCORD_TOKEN is not set (see ~/.config/wotr/env).");
        return 1;
    };
    let cfg = match pyyaml::load(&read_lossy(&root("bot/config.yaml"))) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("bot/config.yaml: {e}");
            return 1;
        }
    };
    let mut intents = GatewayIntents::non_privileged();
    if cfg["intents"]["message_content"].as_bool().unwrap_or(false) {
        intents |= GatewayIntents::MESSAGE_CONTENT;
    }
    let bot = Bot { page: cfg["page_size"].as_u64().unwrap_or(3600) as usize, cfg, tools: Wotr::fixed(true, false), views: Mutex::new(HashMap::new()), next_view: AtomicU64::new(1), lock: tokio::sync::Mutex::new(()), sync: args.iter().any(|a| a == "--sync") };
    let mut client = match Client::builder(token.trim(), intents).event_handler(bot).await {
        Ok(c) => c,
        Err(e) => {
            eprintln!("{e}");
            return 1;
        }
    };
    match client.start().await {
        Ok(()) => 0,
        Err(e) => {
            eprintln!("{e}");
            1
        }
    }
}

/// The whole reply path with Discord replaced by a recording server: real interaction payloads go
/// in, and the tests read the REST calls the bot makes. Nothing connects to Discord.
#[cfg(test)]
mod tests {
    use super::*;
    use axum::{body::Bytes, extract::State, http::{Method, Uri}, response::IntoResponse, routing::any, Router};

    type Calls = Arc<Mutex<Vec<(String, String, Vec<u8>)>>>;

    const GUILD: u64 = 1000;

    fn user(id: u64) -> Value {
        json!({"id": id.to_string(), "username": "tester", "discriminator": "0", "global_name": "Tester", "avatar": null, "bot": false})
    }

    fn message(id: u64, content: &str) -> Value {
        json!({"id": id.to_string(), "channel_id": "2000", "author": user(5), "content": content, "timestamp": "2026-11-04T10:00:00Z", "edited_timestamp": null, "tts": false, "mention_everyone": false, "mentions": [], "mention_roles": [], "attachments": [], "embeds": [], "pinned": false, "type": 0})
    }

    async fn stub(State(calls): State<Calls>, method: Method, uri: Uri, body: Bytes) -> impl IntoResponse {
        let path = uri.path().to_string();
        calls.lock().unwrap().push((method.to_string(), path.clone(), body.to_vec()));
        let role = |id: u64, name: &str| json!({"id": id.to_string(), "name": name, "color": 0, "colors": {"primary_color": 0, "secondary_color": null, "tertiary_color": null}, "hoist": false, "position": 1, "permissions": "0", "managed": false, "mentionable": false, "guild_id": GUILD.to_string()});
        let reply = if path.ends_with("/callback") {
            return axum::http::StatusCode::NO_CONTENT.into_response();
        } else if path.ends_with("/roles") {
            json!([role(1, "Archivist"), role(2, "Scribe"), role(3, "wotr noob")])
        } else if path.ends_with("/messages") && method == Method::GET {
            let long = "Sodoku Moto walks the length of the hall and the lamps answer him, brass and gold in the morning, every servant turning to watch the old lord pass by the door.";
            if uri.query().unwrap_or("").contains("before=") { json!([]) } else { json!([message(11, long)]) }
        } else {
            message(99, "ok")
        };
        axum::Json(reply).into_response()
    }

    async fn rig() -> (Bot, Arc<Http>, Calls) {
        let calls: Calls = Arc::default();
        let app = Router::new().fallback(any(stub)).with_state(calls.clone());
        let listener = tokio::net::TcpListener::bind(("127.0.0.1", 0)).await.unwrap();
        let port = listener.local_addr().unwrap().port();
        tokio::spawn(async move { axum::serve(listener, app).await.unwrap() });
        let http = HttpBuilder::new("test-token").proxy(format!("http://127.0.0.1:{port}")).ratelimiter_disabled(true).application_id(ApplicationId::new(7)).build();
        let cfg = json!({"roles": {"judger": ["Archivist"], "scribe": ["Scribe"], "player": ["wotr noob"]}, "channels": {}, "players": {"5": ["Sodoku Moto"]}});
        let bot = Bot { cfg, page: 3600, tools: Wotr::fixed(true, false), views: Mutex::default(), next_view: AtomicU64::new(1), lock: tokio::sync::Mutex::new(()), sync: false };
        (bot, Arc::new(http), calls)
    }

    fn itx(http: &Arc<Http>, roles: &[u64], thread: bool) -> Itx {
        let member: Member = serde_json::from_value(json!({"user": user(5), "roles": roles.iter().map(u64::to_string).collect::<Vec<_>>(), "joined_at": "2026-01-01T00:00:00Z", "deaf": false, "mute": false, "flags": 0, "guild_id": GUILD.to_string()})).unwrap();
        let user: User = serde_json::from_value(self::user(5)).unwrap();
        Itx { http: http.clone(), id: InteractionId::new(50), token: "tok".into(), done: AtomicBool::new(false), user, member: Some(Box::new(member)), guild: Some(GuildId::new(GUILD)), channel: ChannelId::new(2000), channel_name: Some("the-hall".into()), thread }
    }

    fn command(name: &str, options: Value) -> CommandInteraction {
        let member = json!({"user": user(5), "roles": [], "joined_at": "2026-01-01T00:00:00Z", "deaf": false, "mute": false, "flags": 0, "permissions": "0"});
        serde_json::from_value(json!({"id": "50", "application_id": "7", "type": 2, "token": "tok", "version": 1, "guild_id": GUILD.to_string(), "channel_id": "2000", "member": member, "locale": "en-US", "app_permissions": "0", "entitlements": [], "authorizing_integration_owners": {}, "attachment_size_limit": 10485760, "data": {"id": "60", "name": name, "type": 1, "options": options}})).unwrap()
    }

    fn component(custom_id: &str, values: &[&str]) -> ComponentInteraction {
        let data = if values.is_empty() { json!({"custom_id": custom_id, "component_type": 2}) } else { json!({"custom_id": custom_id, "component_type": 3, "values": values}) };
        let member = json!({"user": user(5), "roles": [], "joined_at": "2026-01-01T00:00:00Z", "deaf": false, "mute": false, "flags": 0, "permissions": "0"});
        serde_json::from_value(json!({"id": "51", "application_id": "7", "type": 3, "token": "tok", "version": 1, "guild_id": GUILD.to_string(), "channel_id": "2000", "member": member, "locale": "en-US", "app_permissions": "0", "entitlements": [], "authorizing_integration_owners": {}, "attachment_size_limit": 10485760, "data": data, "message": message(90, "")})).unwrap()
    }

    /// (path, body) of the calls so far that write, the JSON part of a multipart body included.
    fn writes(calls: &Calls) -> Vec<(String, Value)> {
        calls.lock().unwrap().iter().filter(|c| c.0 != "GET").map(|(_, path, body)| {
            let text = String::from_utf8_lossy(body);
            let json = match text.find("{\"") {
                Some(i) if text.starts_with("--") => text[i..].split("\r\n").next().unwrap_or("{}").to_string(),
                _ => text.to_string(),
            };
            (path.clone(), serde_json::from_str(&json).unwrap_or(Value::Null))
        }).collect()
    }

    fn custom_ids(body: &Value) -> Vec<String> {
        let mut out = Vec::new();
        for row in body["components"].as_array().into_iter().flatten() {
            for c in row["components"].as_array().into_iter().flatten() {
                out.push(c["custom_id"].as_str().unwrap_or("").to_string());
            }
        }
        out
    }

    #[tokio::test]
    async fn whoami_reads_the_role_from_the_guild_and_answers_privately() {
        let (bot, http, calls) = rig().await;
        bot.dispatch(&itx(&http, &[2], false), &command("whoami", json!([]))).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w.len(), 1);
        assert!(w[0].0.ends_with("/interactions/50/tok/callback"), "{}", w[0].0);
        assert_eq!(w[0].1["type"], 4);
        assert_eq!(w[0].1["data"]["flags"], 64);
        assert!(w[0].1["data"]["content"].as_str().unwrap().contains("table role **scribe**"));
    }

    #[tokio::test]
    async fn a_reader_is_refused_the_judgers_commands_and_nothing_is_written() {
        let (bot, http, calls) = rig().await;
        for (name, options, expect) in [
            ("event", json!([{"name": "add", "type": 1, "options": [{"name": "title", "type": 3, "value": "x"}, {"name": "when", "type": 3, "value": "y"}, {"name": "where", "type": 3, "value": "z"}]}]), "Events are entered"),
            ("event", json!([{"name": "done", "type": 1, "options": [{"name": "id", "type": 3, "value": "E001"}]}]), "Events are closed"),
            ("date", json!([{"name": "set", "type": 1, "options": [{"name": "month", "type": 4, "value": 3}]}]), "sets the date"),
            ("date", json!([{"name": "advance", "type": 1, "options": [{"name": "days", "type": 4, "value": 3}]}]), "advances the date"),
            ("narrate", json!([{"name": "scene", "type": 3, "value": "x"}]), "Narration is for"),
        ] {
            calls.lock().unwrap().clear();
            bot.dispatch(&itx(&http, &[3], false), &command(name, options)).await.unwrap();
            let w = writes(&calls);
            assert_eq!(w.len(), 1, "{expect}");
            assert_eq!(w[0].1["data"]["flags"], 64);
            assert!(w[0].1["data"]["content"].as_str().unwrap().contains(expect), "{expect}: {}", w[0].1);
        }
    }

    #[tokio::test]
    async fn a_player_with_no_card_sees_no_ledger() {
        let (mut bot, http, calls) = rig().await;
        bot.cfg["players"] = json!({});
        bot.dispatch(&itx(&http, &[3], false), &command("ledger", json!([]))).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["type"], 5, "deferred first");
        assert_eq!(w[0].1["data"]["flags"], 64);
        assert!(w[1].1["content"].as_str().unwrap().contains("No characters are on file for you"));
    }

    #[tokio::test]
    async fn wiki_hits_open_into_a_page_with_page_turns() {
        let (bot, http, calls) = rig().await;
        bot.dispatch(&itx(&http, &[], false), &command("wiki", json!([{"name": "query", "type": 3, "value": "Soul Crystal"}]))).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["type"], 5);
        assert!(w[1].0.ends_with("/webhooks/7/tok"), "{}", w[1].0);
        assert!(w[1].1["embeds"][0]["title"].as_str().unwrap().contains("Soul Crystal"));
        let select = custom_ids(&w[1].1).remove(0);
        calls.lock().unwrap().clear();
        bot.component(&itx(&http, &[], false), &component(&select, &["0"])).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["type"], 7, "the message is replaced in place");
        let first = w[0].1["data"]["embeds"][0]["description"].clone();
        assert!(first.as_str().is_some_and(|d| !d.is_empty()));
        if let Some(next) = custom_ids(&w[0].1["data"]).into_iter().find(|c| c.ends_with(":next")) {
            calls.lock().unwrap().clear();
            bot.component(&itx(&http, &[], false), &component(&next, &[])).await.unwrap();
            let w = writes(&calls);
            assert_ne!(w[0].1["data"]["embeds"][0]["description"], first, "the page turned");
        }
    }

    #[tokio::test]
    async fn a_card_jumps_to_a_section() {
        let (bot, http, calls) = rig().await;
        let name = look::character_names("", 1).remove(0);
        bot.dispatch(&itx(&http, &[], false), &command("character", json!([{"name": "name", "type": 3, "value": name}]))).await.unwrap();
        let w = writes(&calls);
        let jump = custom_ids(&w[1].1).remove(0);
        assert!(jump.ends_with(":jump"));
        calls.lock().unwrap().clear();
        bot.component(&itx(&http, &[], false), &component(&jump, &["0"])).await.unwrap();
        assert_eq!(writes(&calls)[0].1["type"], 7);
    }

    #[tokio::test]
    async fn a_stat_block_rerolls_in_place() {
        let (bot, http, calls) = rig().await;
        bot.dispatch(&itx(&http, &[], false), &command("stats", json!([{"name": "level", "type": 4, "value": 150}]))).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["type"], 4);
        assert!(w[0].1["data"]["embeds"][0]["title"].as_str().unwrap().starts_with("Level 150"));
        assert_eq!(w[0].1["data"]["embeds"][0]["fields"].as_array().unwrap().len(), 8, "eight Primaries");
        let roll = custom_ids(&w[0].1["data"]).remove(0);
        calls.lock().unwrap().clear();
        bot.component(&itx(&http, &[], false), &component(&roll, &[])).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["type"], 7);
        assert_eq!(custom_ids(&w[0].1["data"]), vec![roll], "the same button stays");
    }

    #[tokio::test]
    async fn verify_opens_a_form_and_the_form_keeps_its_options() {
        let (bot, http, calls) = rig().await;
        bot.dispatch(&itx(&http, &[], false), &command("verify", json!([{"name": "combat", "type": 5, "value": true}, {"name": "band", "type": 3, "value": "turn"}]))).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["type"], 9, "a modal");
        let id = w[0].1["data"]["custom_id"].as_str().unwrap().to_string();
        assert_eq!(w[0].1["data"]["components"][0]["components"][0]["max_length"], 4000);
        calls.lock().unwrap().clear();
        let modal: ModalInteraction = serde_json::from_value(json!({"id": "52", "application_id": "7", "type": 5, "token": "tok", "version": 1, "guild_id": GUILD.to_string(), "channel_id": "2000", "member": {"user": user(5), "roles": [], "joined_at": "2026-01-01T00:00:00Z", "deaf": false, "mute": false, "flags": 0, "permissions": "0"}, "locale": "en-US", "app_permissions": "0", "entitlements": [], "authorizing_integration_owners": {}, "attachment_size_limit": 10485760, "data": {"custom_id": id, "components": [{"type": 1, "components": [{"type": 4, "custom_id": "text", "value": "The lamp burned gold over the brass door and Yoko smelled the iron before she saw it."}]}]}})).unwrap();
        bot.modal(&itx(&http, &[], false), &modal).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["type"], 5);
        let foot = w[1].1["embeds"][0]["footer"]["text"].as_str().unwrap();
        assert!(foot.contains("combat") && foot.contains("turn"), "{foot}");
    }

    #[tokio::test]
    async fn scene_save_compiles_the_channel_and_only_a_judge_archives() {
        let (bot, http, calls) = rig().await;
        bot.dispatch(&itx(&http, &[3], false), &command("scene", json!([{"name": "save", "type": 1, "options": [{"name": "title", "type": 3, "value": "The Hall"}]}]))).await.unwrap();
        let w = writes(&calls);
        let up = w.iter().find(|x| x.0.ends_with("/webhooks/7/tok")).expect("the report goes up");
        assert!(up.1["embeds"][0]["title"].as_str().unwrap().contains("The Hall"), "{}", up.1);
        assert!(calls.lock().unwrap().iter().any(|c| String::from_utf8_lossy(&c.2).contains("filename=\"the_hall.md\"")), "the compiled scene is attached");
        let ids = custom_ids(&up.1);
        let archive = ids.iter().find(|c| c.ends_with(":archive")).unwrap();
        calls.lock().unwrap().clear();
        bot.component(&itx(&http, &[3], false), &component(archive, &[])).await.unwrap();
        let w = writes(&calls);
        assert!(w[0].1["data"]["content"].as_str().unwrap().contains("Only the Judger or a Scribe"));
        assert_eq!(w[0].1["data"]["flags"], 64);
        // Cancel clears the buttons and leaves the attachment and the report alone
        let cancel = ids.iter().find(|c| c.ends_with(":cancel")).unwrap();
        calls.lock().unwrap().clear();
        bot.component(&itx(&http, &[3], false), &component(cancel, &[])).await.unwrap();
        let w = writes(&calls);
        assert_eq!(w[0].1["data"]["content"], "Not archived.");
        assert_eq!(w[0].1["data"]["components"], json!([]));
        assert!(w[0].1["data"].get("attachments").is_none(), "{}", w[0].1);
    }

    #[tokio::test]
    async fn a_timed_out_control_says_so() {
        let (bot, http, calls) = rig().await;
        bot.component(&itx(&http, &[], false), &component("v:999:next", &[])).await.unwrap();
        assert!(writes(&calls)[0].1["data"]["content"].as_str().unwrap().contains("timed out"));
    }

    #[test]
    fn views_keep_python_timeouts() {
        assert_eq!(View::Archive { title: String::new(), md: String::new(), script: String::new(), notes: String::new() }.secs(), 1800);
        assert_eq!(View::Engine { path: PathBuf::new(), allow_eleven: false, words: 0, chars: 0 }.secs(), 300);
        assert_eq!(View::RerollStats { level: 1 }.secs(), 900);
    }

    #[test]
    fn a_link_names_its_channel_and_message() {
        let (c, m) = message_link("https://discord.com/channels/1/22/333").unwrap();
        assert_eq!((c.get(), m.get()), (22, 333));
        assert!(message_link("nope").is_none());
    }

    #[test]
    fn title_word_matches_str_title() {
        assert_eq!(title_word("undaar-keth"), "Undaar-Keth");
        assert_eq!(title_word("holy sea"), "Holy Sea");
    }
}
