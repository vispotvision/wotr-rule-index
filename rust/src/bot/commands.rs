//! The slash commands as Discord sees them. bot/main.py's tree, option for option.
use super::names;
use serenity::all::{CommandOptionType as T, CreateCommand, CreateCommandOption};

fn opt(kind: T, name: &str, desc: &str, required: bool) -> CreateCommandOption {
    CreateCommandOption::new(kind, name, desc).required(required)
}

fn cmd(name: &str, desc: &str, options: Vec<CreateCommandOption>) -> CreateCommand {
    CreateCommand::new(name).description(desc).set_options(options)
}

fn choices(mut o: CreateCommandOption, items: &[(&str, &str)]) -> CreateCommandOption {
    for (n, v) in items {
        o = o.add_string_choice(*n, *v);
    }
    o
}

fn sub(name: &str, desc: &str, options: Vec<CreateCommandOption>) -> CreateCommandOption {
    let mut c = CreateCommandOption::new(T::SubCommand, name, desc);
    for o in options {
        c = c.add_sub_option(o);
    }
    c
}

pub fn definitions() -> Vec<CreateCommand> {
    let cultures: Vec<(&str, &str)> = names::CULTURES.iter().map(|(k, v)| (*v, *k)).collect();
    let (branches, lineages) = (names::elven_branches(), names::beastkin_lineages());
    let b: Vec<(&str, &str)> = branches.iter().map(|x| (x.as_str(), x.as_str())).collect();
    let l: Vec<(&str, &str)> = lineages.iter().map(|x| (x.as_str(), x.as_str())).collect();
    let bands = [("turn", "turn"), ("standard", "standard"), ("conversational", "conversational"), ("set-piece", "set-piece"), ("discord", "discord")];
    vec![
        cmd("wiki", "Search the lore wiki. Pick a result to read the whole page.", vec![opt(T::String, "query", "What to look for, e.g. Soul Crystal, Kharven, the Accord", true)]),
        cmd("define", "What a word or term means, from where the wiki defines it.", vec![opt(T::String, "term", "The word or phrase, e.g. Soul Crystal, Temperance, the Waiting", true)]),
        cmd("character", "A character's card: overview, key facts, and every section.", vec![opt(T::String, "name", "Character name", true).set_autocomplete(true)]),
        cmd("fow", "A character's Fracture of Worlds line, from their card only.", vec![opt(T::String, "name", "Character name", true).set_autocomplete(true)]),
        cmd("recall", "Search the scene archive: who said what, what happened where.", vec![opt(T::String, "query", "Words or a name", true)]),
        cmd("timeline", "Every archived scene in reading order with its in-world moment.", vec![]),
        cmd("whoami", "Your table role as the bot sees it.", vec![]),
        cmd("name", "Compose a name from a culture's ratified element bank (the Naming Guide).", vec![
            choices(opt(T::String, "culture", "Which register", true), &cultures),
            choices(opt(T::String, "branch", "Elven only: the branch", false), &b),
            choices(opt(T::String, "lineage", "Beastkin only: the lineage", false), &l),
            choices(opt(T::String, "sex", "Concord / Holy Sea only: which given-name pool", false), &[("male", "male"), ("female", "female")]),
        ]),
        cmd("name_help", "Which registers /name can and cannot build, and why.", vec![]),
        cmd("stats", "A Fracture of Worlds stat block for a Level, derived from the codex. Not a card.", vec![opt(T::Integer, "level", "1-500; the Stage follows the Band and the lean is chosen for you", true).min_int_value(1).max_int_value(500)]),
        cmd("narrate", "Render an archived scene to audio: local narrator (free) or ElevenLabs (paid).", vec![
            opt(T::String, "scene", "Scene file or a unique part of its title", true).set_autocomplete(true),
            choices(opt(T::String, "engine", "Leave empty to be asked", false), &[("local (free)", "local"), ("elevenlabs (paid)", "elevenlabs")]),
        ]),
        cmd("scene", "Save what was written here as an archived scene.", vec![sub("save", "Archive this thread, the messages after a link, or a pasted block as a scene.", vec![
            opt(T::String, "title", "The scene's title (default: this thread's name)", false),
            choices(opt(T::String, "source", "Where the text comes from", false), &[("this thread / channel", "thread"), ("from a message link onward", "link"), ("paste a block", "paste")]),
            opt(T::String, "link", "With source=link: the first message to include", false),
            opt(T::Integer, "count", "With source=thread: only the most recent N messages (default: the whole thread)", false).min_int_value(1).max_int_value(10000),
        ])]),
        cmd("event", "Events on the table.", vec![
            sub("add", "Record an event: what, when (in-world), where, who.", vec![
                opt(T::String, "title", "What happens", true),
                opt(T::String, "when", "In-world date or moment", true),
                opt(T::String, "where", "Place (a location channel name works)", true),
                opt(T::String, "who", "Who is involved", false),
                opt(T::String, "blurb", "One paragraph", false),
            ]),
            sub("list", "Upcoming events on the table.", vec![]),
            sub("done", "Mark an event as having happened.", vec![opt(T::String, "id", "The event id, e.g. E003", true)]),
        ]),
        cmd("sheet", "Check a character sheet against the canon: stat model, ceilings, pool, struck names, terms.", vec![opt(T::String, "link", "A message link to the sheet (default: the first message of this thread)", false)]),
        cmd("verify", "The manual-verification checks on a scene: paste it, or point at a message.", vec![
            opt(T::String, "link", "A message link (right-click \u{2192} Copy Message Link); leave empty to paste", false),
            opt(T::Boolean, "combat", "A duel or small action", false),
            opt(T::String, "culture", "Culture the scene sits in", false),
            choices(opt(T::String, "band", "Length band", false), &bands),
        ]),
        cmd("date", "The in-world calendar.", vec![
            sub("today", "The table's current in-world date.", vec![]),
            sub("set", "Judger: set the table's in-world date.", vec![
                opt(T::Integer, "month", "1\u{2013}12", true).min_int_value(1).max_int_value(12),
                opt(T::Integer, "day", "1\u{2013}31", false).min_int_value(1).max_int_value(31),
                opt(T::Integer, "year", "Accord year", false),
                opt(T::String, "era", "The Moto era name, if any", false),
            ]),
            sub("advance", "Judger: move the table's date forward.", vec![opt(T::Integer, "days", "How many days", true).min_int_value(1).max_int_value(3640)]),
            sub("name", "What weekday a date is, and what a span of days lands on.", vec![
                opt(T::Integer, "month", "1\u{2013}12", true).min_int_value(1).max_int_value(12),
                opt(T::Integer, "day", "1\u{2013}31", true).min_int_value(1).max_int_value(31),
                opt(T::Integer, "plus", "Days later (optional)", false),
                opt(T::Integer, "year", "Accord year, for the weekday (optional)", false),
            ]),
        ]),
        cmd("ledger", "The open Ledger lines about your own characters.", vec![]),
        cmd("due", "The Ledger lines about your own characters that have come due.", vec![]),
        cmd("roster", "The NPCs on a thread's roster, as anyone may see them.", vec![opt(T::String, "thread", "The story thread, e.g. Kharven, Mu-jin (default: every thread)", false)]),
        cmd("npc", "One NPC's public face: look, voice, role.", vec![opt(T::String, "name", "The NPC's name, or part of it", true)]),
    ]
}
