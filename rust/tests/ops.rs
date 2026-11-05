//! The gate and the machine's jobs on a scratch repo, through the real binary.
use std::{fs, path::{Path, PathBuf}, process::{Command, Output, Stdio}};
use std::io::Write;

fn scratch(name: &str) -> PathBuf {
    let root = std::env::temp_dir().join(format!("wotr-ops-{name}-{}", std::process::id()));
    let _ = fs::remove_dir_all(&root);
    fs::create_dir_all(root.join("build")).unwrap();
    root
}

fn cmd(root: &Path, args: &[&str]) -> Command {
    let mut c = Command::new(env!("CARGO_BIN_EXE_wotr-mcp"));
    c.args(args).env("WOTR_ROOT", root).env("WOTR_ENV_FILE", "/nonexistent").env_remove("WOTR_DRIVE");
    c
}

fn run(root: &Path, args: &[&str]) -> (Option<i32>, String) {
    let o: Output = cmd(root, args).output().unwrap();
    (o.status.code(), String::from_utf8_lossy(&o.stdout).into_owned())
}

fn index_repo(root: &Path) {
    let repo = Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap();
    fs::create_dir_all(root.join("schema")).unwrap();
    fs::create_dir_all(root.join("rules")).unwrap();
    fs::create_dir_all(root.join("sources")).unwrap();
    fs::copy(repo.join("schema/rule.schema.json"), root.join("schema/rule.schema.json")).unwrap();
    fs::write(root.join("schema/applies_to.md"), "| `combat` | fights |\n| `pov` | heads |\n").unwrap();
    fs::write(root.join("sources/s.md"), "The **blade** speaks\nfirst, always.\n").unwrap();
}

const GOOD: &str = "rules:\n- id: R1-1-GOOD\n  pack: Pack One\n  pack_number: 1\n  section: s\n  title: Good\n  status: live\n  kind: mandate\n  summary: A rule.\n  verbatim: The blade speaks first, always.\n  applies_to: [combat]\n  source: {file: s.md}\n";

#[test]
fn validate_passes_clean_rows_and_names_each_fault() {
    let root = scratch("validate");
    index_repo(&root);
    fs::write(root.join("rules/a.yaml"), GOOD).unwrap();
    let (code, out) = run(&root, &["validate"]);
    assert_eq!(code, Some(0), "{out}");
    assert!(out.contains("1 rules across 1 files") && out.ends_with("PASS\n"), "{out}");

    let bad = "rules:\n- id: R1-1-GOOD\n  pack: P\n  section: s\n  title: t\n  status: live\n  kind: mandate\n  summary: s\n  verbatim: this quote is not in the source file\n  applies_to: [nope]\n  source: {file: s.md}\n  supersedes: [R9-9-GONE]\n";
    fs::write(root.join("rules/b.yaml"), bad).unwrap();
    let (code, out) = run(&root, &["validate"]);
    assert_eq!(code, Some(1), "{out}");
    for want in ["duplicate id R1-1-GOOD", "verbatim quote not found", "applies_to tag 'nope'", "supersedes unknown rule id 'R9-9-GONE'"] {
        assert!(out.contains(want), "{want} in {out}");
    }
    fs::remove_dir_all(&root).unwrap();
}

/// The 1a33d7c defect: a live row citing a ruling nobody logged, with an empty source.
#[test]
fn validate_fails_a_ruling_that_is_on_no_record() {
    let root = scratch("unrecorded");
    index_repo(&root);
    let row = |id: &str, quote: &str| format!("rules:\n- id: {id}\n  pack: P\n  section: s\n  title: t\n  status: live\n  kind: mandate\n  summary: s\n  verbatim: {quote}\n  applies_to: [combat]\n  source: {{file: \"\"}}\n");
    fs::write(root.join("rules/a.yaml"), row("R44-7-INVENTED", "A ruling nobody made.")).unwrap();
    fs::write(root.join("rules/b.yaml"), row("R44-8-LOGGED", "Isaac ruled this one.")).unwrap();
    fs::write(root.join("rules/c.yaml"), row("R44-9-WIKI", "The wiki holds this one.")).unwrap();
    fs::write(root.join("RULINGS.md"), "## Log\n\nIsaac ruled\nthis *one*.\n").unwrap();
    fs::create_dir_all(root.join("wiki/Deep")).unwrap();
    fs::write(root.join("wiki/Deep/Page.md"), "The wiki holds this one.\n").unwrap();
    let (code, out) = run(&root, &["validate"]);
    assert_eq!(code, Some(1), "{out}");
    assert!(out.contains("FAIL (1)") && out.contains("R44-7-INVENTED"), "{out}");
    assert!(!out.contains("R44-8-LOGGED") && !out.contains("R44-9-WIKI"), "{out}");
    fs::remove_dir_all(&root).unwrap();
}

#[test]
fn validate_fails_on_an_empty_index() {
    let root = scratch("empty");
    index_repo(&root);
    let (code, out) = run(&root, &["validate"]);
    assert_eq!(code, Some(1));
    assert!(out.starts_with("no rules found"), "{out}");
    fs::remove_dir_all(&root).unwrap();
}

#[test]
fn resolve_writes_every_output() {
    let root = scratch("resolve");
    index_repo(&root);
    fs::write(root.join("rules/a.yaml"), GOOD).unwrap();
    let (code, out) = run(&root, &["resolve"]);
    assert_eq!(code, Some(0), "{out}");
    assert!(out.contains("resolved 1 rules") && out.contains("live=1 pending=0"), "{out}");
    let live = fs::read_to_string(root.join("out/rules.live.full.md")).unwrap();
    assert!(live.contains("## combat (1)") && live.contains("> The blade speaks first, always."), "{live}");
    let json = fs::read_to_string(root.join("out/rules.resolved.json")).unwrap();
    assert!(json.contains("\"superseded_by\": []"), "{json}");
    assert!(fs::read_to_string(root.join("out/docket.md")).unwrap().contains("0 outstanding."));
    fs::remove_dir_all(&root).unwrap();
}

#[test]
fn backup_zips_the_canon_and_keeps_twelve() {
    let root = scratch("backup");
    let dest = root.join("dest");
    fs::create_dir_all(&dest).unwrap();
    for i in 0..14 {
        fs::write(dest.join(format!("wotr-2020-01-{i:02}.zip")), b"old").unwrap();
    }
    fs::create_dir_all(root.join("wiki/__pycache__")).unwrap();
    fs::write(root.join("wiki/page.md"), "a page").unwrap();
    fs::write(root.join("wiki/__pycache__/x.pyc"), "junk").unwrap();
    fs::write(root.join("RULINGS.md"), "rulings").unwrap();
    let canon = root.join("canon");
    fs::create_dir_all(canon.join("sub")).unwrap();
    fs::write(canon.join("sub/guide.md"), "guide").unwrap();
    let o = cmd(&root, &["backup"]).env("WOTR_BACKUP_DIR", &dest).env("WOTR_TRUE_CANON", &canon).output().unwrap();
    let log = String::from_utf8_lossy(&o.stdout);
    assert_eq!(o.status.code(), Some(0), "{log}");
    assert!(log.contains("3 files") && log.contains("pruned"), "{log}");
    let zips: Vec<PathBuf> = fs::read_dir(&dest).unwrap().flatten().map(|e| e.path()).collect();
    assert_eq!(zips.len(), 12, "{zips:?}");
    let today = zips.iter().find(|p| fs::metadata(p).unwrap().len() > 3).unwrap();
    let mut z = zip::ZipArchive::new(fs::File::open(today).unwrap()).unwrap();
    let mut names: Vec<String> = z.file_names().map(|n| n.unwrap().to_string()).collect();
    names.sort();
    assert_eq!(names, ["RULINGS.md", "canon/sub/guide.md", "wiki/page.md"]);
    let mut text = String::new();
    std::io::Read::read_to_string(&mut z.by_name("wiki/page.md").unwrap(), &mut text).unwrap();
    assert_eq!(text, "a page");
    assert!(fs::read_to_string(root.join("build/backup.log")).unwrap().contains("wrote "));
    fs::remove_dir_all(&root).unwrap();
}

#[test]
fn book_next_blocks_on_an_undecided_gate() {
    let root = scratch("book");
    let b = root.join("book/b");
    fs::create_dir_all(b.join("ch01")).unwrap();
    fs::write(b.join("outline.json"), r#"{"thread":"T","chapters":[{"number":1,"title":"One"},{"number":2,"title":"Two","target_words":900}]}"#).unwrap();
    fs::write(b.join("ch01/final.md"), "x").unwrap();
    let (code, out) = run(&root, &["book-next", "--slug", "b", "--json"]);
    assert_eq!(code, Some(0));
    assert!(out.contains(r#""action": "blocked", "chapter": 1"#), "{out}");
    let (_, out) = run(&root, &["book-next", "--slug", "b", "--approve", "1", "--note", "good"]);
    assert_eq!(out, "chapter 1: approved \u{2014} good\n");
    let (_, out) = run(&root, &["book-next", "--slug", "b", "--json"]);
    assert!(out.contains(r#""action": "write", "chapter": 2"#) && out.contains(r#""target_words": 900"#), "{out}");
    assert!(fs::read_to_string(b.join("GATES.md")).unwrap().contains("| 1 | One | yes | yes | approved |"));
    let (code, out) = run(&root, &["book-next", "--slug", "none"]);
    assert_eq!(code, Some(1));
    assert!(out.starts_with("no outline for 'none'"), "{out}");
    fs::remove_dir_all(&root).unwrap();
}

fn hook(root: &Path, input: &str) -> (Option<i32>, String) {
    let mut c = cmd(root, &["hook"]).stdin(Stdio::piped()).stdout(Stdio::piped()).spawn().unwrap();
    c.stdin.take().unwrap().write_all(input.as_bytes()).unwrap();
    let o = c.wait_with_output().unwrap();
    (o.status.code(), String::from_utf8_lossy(&o.stdout).into_owned())
}

#[test]
fn hook_is_off_without_the_marker_and_blocks_a_fail_with_it() {
    let root = scratch("hook");
    let long = "He walked to the door and opened it. ".repeat(20) + "He looked at her \u{2014} and left.";
    let line = serde_json_line(&long);
    let transcript = root.join("t.jsonl");
    fs::write(&transcript, line).unwrap();
    let stop = format!(r#"{{"hook_event_name":"Stop","transcript_path":"{}"}}"#, transcript.display());
    assert_eq!(hook(&root, &stop), (Some(0), String::new()));

    fs::write(root.join(".natalie"), "").unwrap();
    let (code, out) = hook(&root, &stop);
    assert_eq!(code, Some(0));
    assert!(out.contains(r#""decision": "block""#) && out.contains("em dashes"), "{out}");

    // one enforced revision per reply
    let again = format!(r#"{{"hook_event_name":"Stop","stop_hook_active":true,"transcript_path":"{}"}}"#, transcript.display());
    assert_eq!(hook(&root, &again), (Some(0), String::new()));
    fs::remove_dir_all(&root).unwrap();
}

fn serde_json_line(text: &str) -> String {
    format!(r#"{{"type":"assistant","message":{{"content":[{{"type":"text","text":"{text}"}}]}}}}"#)
}
