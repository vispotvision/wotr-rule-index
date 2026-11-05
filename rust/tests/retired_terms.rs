//! A retired tool or a reversed direction must not live on where sessions load it: skill
//! descriptions (they decide loading) and the instruction files. Add a term when something retires.
use std::{fs, path::Path};

const RETIRED: &[(&str, &str)] = &[
    ("ask_chatgpt", "2026-10-31, the ChatGPT plan ended"),
    ("chatgpt_image", "2026-10-31, the ChatGPT plan ended"),
    ("ask ChatGPT", "2026-10-31, the ChatGPT plan ended"),
    ("ask Codex", "2026-10-31, the ChatGPT plan ended"),
    ("ChatGPT plan", "2026-10-31, the ChatGPT plan ended"),
    ("ChatGPT and Codex", "2026-11-04, Claude Code only"),
    ("Codex and Antigravity", "2026-11-04, Claude Code only"),
    ("Antigravity", "2026-11-04, Claude Code only"),
    ("build/validate.py", "2026-11-04, the gate is wotr-mcp validate"),
    ("wotr-mcp dump", "2026-11-04, rust/tools.json is kept by hand"),
    ("Draw Age", "2026-11-05, the Dark Ages, R83"),
    ("standpipe", "2026-11-05, no draw and no mains, R83-9"),
    ("draw-hum", "2026-11-05, no draw and no mains, R83-9"),
    ("district main", "2026-11-05, no draw and no mains, R83-9"),
    ("firearm", "2026-11-05, no guns in any era, R83-5"),
];

/// A line that says the thing is gone is the marked notice, not a carrier.
fn hits(text: &str) -> Vec<String> {
    let mut out = Vec::new();
    for line in text.lines() {
        let low = line.to_lowercase();
        if low.contains("retired") || low.contains("no longer") {
            continue;
        }
        for (term, why) in RETIRED {
            if line.contains(term) {
                out.push(format!("'{term}' (retired {why})"));
            }
        }
    }
    out
}

#[test]
fn the_check_can_fail() {
    assert_eq!(hits("Claude Code, Codex and Antigravity share it.").len(), 2);
    assert!(hits("> **Retired, 2026-10-31.** Do not use `ask_chatgpt`.").is_empty());
    assert!(hits("Read the Master Codex and the Glyph Index.").is_empty());
}

#[test]
fn nothing_loaded_names_a_retired_term() {
    let repo = Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap();
    let mut found = Vec::new();
    for f in ["CLAUDE.md", "AGENTS.md", "desktop/NATALIE.md", "desktop/PROJECT_INSTRUCTIONS.md"] {
        let text = fs::read_to_string(repo.join(f)).unwrap();
        found.extend(hits(&text).into_iter().map(|h| format!("{f}: {h}")));
    }
    let skills = fs::read_dir(repo.join(".claude/skills")).unwrap();
    let mut n = 0;
    for dir in skills.flatten() {
        let Ok(text) = fs::read_to_string(dir.path().join("SKILL.md")) else { continue };
        n += 1;
        let description = text.lines().find(|l| l.starts_with("description:")).unwrap_or("");
        found.extend(hits(description).into_iter().map(|h| format!("{} description: {h}", dir.file_name().to_string_lossy())));
    }
    assert!(n > 0, "read no skills");
    assert!(found.is_empty(), "retired terms still loaded:\n{}", found.join("\n"));
}
