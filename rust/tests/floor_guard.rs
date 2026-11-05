//! The explicit-scene floor guard on a scratch repo, through the real binary.
use std::{fs, path::Path, process::Command};

const READ_NOTHING: &str = "floor guard: read no character cards";
const CARDS: &str = "wiki/Characters/Volume I \u{2014} Character Cards";

fn verify(root: &Path) -> String {
    let scene = root.join("scene.md");
    fs::write(&scene, "Mira kissed him.").unwrap();
    let out = Command::new(env!("CARGO_BIN_EXE_wotr-mcp")).arg("verify").arg(&scene).arg("--explicit").env("WOTR_ROOT", root).output().unwrap();
    String::from_utf8_lossy(&out.stdout).into_owned()
}

#[test]
fn floor_guard() {
    let root = std::env::temp_dir().join(format!("wotr-floor-guard-{}", std::process::id()));
    let _ = fs::remove_dir_all(&root);
    fs::create_dir_all(&root).unwrap();

    // No folder at all: the guard cannot run, so the scene does not pass.
    let out = verify(&root);
    assert!(out.contains(READ_NOTHING), "{out}");

    // A hub page and a roster entry are not cards: the shape of the 2026-10-15 stale path.
    fs::create_dir_all(root.join("wiki/Characters")).unwrap();
    fs::write(root.join("wiki/Characters/Characters.md"), "The hub.\n").unwrap();
    fs::create_dir_all(root.join("table")).unwrap();
    fs::write(root.join("table/npcs.yaml"), "- name: Oskar Vane\n  age: 40\n").unwrap();
    let out = verify(&root);
    assert!(out.contains(READ_NOTHING), "{out}");

    // A card under eighteen, named in the scene, FAILs by name.
    let cards = root.join(CARDS);
    fs::create_dir_all(&cards).unwrap();
    fs::write(cards.join("Mira Sol.md"), "**Age:** 16\n").unwrap();
    let out = verify(&root);
    assert!(out.contains("floor guard: Mira Sol is 16") && !out.contains(READ_NOTHING), "{out}");

    // An adult card passes the guard, and the info line proves it was read.
    fs::write(cards.join("Mira Sol.md"), "**Age:** 30\n").unwrap();
    let out = verify(&root);
    assert!(!out.contains("floor guard:") && out.contains("floor guard, named on file: Mira Sol 30"), "{out}");

    fs::remove_dir_all(&root).unwrap();
}
