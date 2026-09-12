#!/usr/bin/env python3
"""MCP server for the WOTR rule index: the tools Natalie calls from Claude Desktop.

  python build/mcp_server.py           # stdio, what claude_desktop_config.json launches
  python build/mcp_server.py --http    # streamable HTTP on :8765, for n8n's MCP Client node
                                       #   (from the n8n container: http://host.docker.internal:8765/mcp)

Tools
  load_rules(tags, status)   the live loadout for a task, same output as build/query.py
  rule(id)                   one rule in full
  check_docket(tags)         pending and proposed rules for the same tags
  list_conflicts()           CONFLICTS.md
  archive_scene(title, markdown)   save a finished scene: scenes/<slug>.md, the
                             Notion Scene Archive, one commit, pushed
  log_ruling(rule_id, ruling)      record a ruling in RULINGS.md so it gets applied
                             to the index next time Claude Code is in the repo
  sync_now()                 run build/sync.ps1 (Notion <-> GitHub <-> Drive docs)

NOTION_TOKEN is read from the environment, falling back to the user-level
variable in the registry (Claude Desktop may have been started before it was set).
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, load_rules, load_vocab  # noqa: E402
from mcp.server.mcpserver import MCPServer  # noqa: E402

PY = sys.executable
SCENES = ROOT / "scenes"
RULINGS = ROOT / "RULINGS.md"


def _env() -> dict:
    env = dict(os.environ)
    if not env.get("NOTION_TOKEN") and sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                env["NOTION_TOKEN"] = winreg.QueryValueEx(k, "NOTION_TOKEN")[0]
        except OSError:
            pass
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _run(cmd: list[str], timeout: int = 600) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, env=_env(), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def _git(*args: str) -> tuple[int, str]:
    return _run(["git", *args], timeout=120)


def _fmt(rule: dict, full: bool = True) -> str:
    lines = [f"{rule['id']}  [{rule['pack']} {rule['section']}]  {rule['status']}",
             f"  {rule['summary'].strip()}"]
    if full:
        lines.append(f"  > {rule['verbatim'].strip()}")
        for a in rule.get("amends") or []:
            lines.append(f"  amends: {a.get('guide')} {a.get('locus') or ''} ({a.get('operation') or '?'})")
        if rule.get("supersedes"):
            lines.append(f"  supersedes: {', '.join(rule['supersedes'])}")
        if rule.get("notes"):
            lines.append(f"  notes: {str(rule['notes']).strip()}")
    return "\n".join(lines)


def _select(tags: list[str], status: list[str]) -> tuple[list[dict], list[str]]:
    vocab = load_vocab()
    bad = [t for t in tags if t not in vocab]
    want = set(tags) - set(bad)
    rules = [r for r in load_rules() if r.get("status") in set(status)]
    if want:
        rules = [r for r in rules if want & set(r.get("applies_to") or [])]
    rules.sort(key=lambda r: (-(r.get("pack_number") or 0), r.get("id", "")))
    return rules, bad


def _slug(title: str) -> str:
    s = re.sub(r"[^\w\s-]", "", title, flags=re.U).strip().lower()
    s = re.sub(r"[\s_-]+", "_", s)
    return s[:80] or "untitled"


server = MCPServer(
    "wotr",
    instructions=(
        "Tools over the War of the Realms rule index at " + str(ROOT) + ". "
        "Before writing prose call load_rules with the task's applies_to tags "
        "(prose-law for any prose; combat, adjudication, magic-mechanism, pov, dialogue, "
        "register, naming, items, scene-structure, mass-combat, stats, magic-design, codex, "
        "worldbuilding, standing-inventory, character-sheet, documents, verification, "
        "session-protocol), then check_docket for the same tags. Rules print newest pack "
        "first; the newer governs where two overlap."
    ),
)


@server.tool(name="load_rules")
def load_rules_tool(tags: list[str], status: list[str] | None = None, brief: bool = False) -> str:
    """Load the rules in force for a task. tags: applies_to tags (see instructions).
    status defaults to ["live"]. brief=True returns id + summary only."""
    rules, bad = _select(tags, status or ["live"])
    out = [_fmt(r, full=not brief) for r in rules]
    head = f"-- {len(rules)} rules for tags {sorted(set(tags) - set(bad))}"
    if bad:
        head += f"  (ignored unknown tags: {bad})"
    return head + "\n\n" + "\n\n".join(out)



@server.tool()
def rule(id: str) -> str:
    """One rule in full by id, e.g. R12-3-COMBAT_EXCHANGE_OWES or R13-C."""
    for r in load_rules():
        if r.get("id") == id:
            return _fmt(r)
    return f"no rule with id {id}"


@server.tool()
def check_docket(tags: list[str]) -> str:
    """Pending open rulings and proposed (never-ratified) rules touching these tags.
    If one would materially change what you are about to write, ask Isaac before writing."""
    rules, bad = _select(tags, ["pending", "proposed"])
    out = [_fmt(r, full=False) for r in rules]
    return f"-- {len(rules)} pending/proposed for {sorted(set(tags) - set(bad))}\n\n" + "\n\n".join(out)


@server.tool()
def list_conflicts() -> str:
    """CONFLICTS.md: live rules that contradict each other, awaiting Isaac's ruling."""
    return (ROOT / "CONFLICTS.md").read_text(encoding="utf-8")


@server.tool()
def archive_scene(title: str, markdown: str, author_notes: str = "") -> str:
    """Save a finished scene. Writes scenes/<slug>.md (title as the H1, author notes
    appended under '## Author notes'), publishes it to the Notion Scene Archive,
    commits and pushes. Returns the file path and the Notion page id."""
    slug = _slug(title)
    path = SCENES / f"{slug}.md"
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M")
        path = SCENES / f"{slug}_{stamp}.md"
    body = markdown.strip()
    if not re.match(r"^#\s", body):
        body = f"# {title}\n\n{body}"
    if author_notes.strip():
        body += f"\n\n---\n\n## Author notes\n\n{author_notes.strip()}"
    SCENES.mkdir(exist_ok=True)
    path.write_text(body + "\n", encoding="utf-8", newline="\n")

    code, pub = _run([PY, str(ROOT / "build" / "notion_publish.py"), "--only", path.name])
    notion = "published to the Notion Scene Archive" if code == 0 else f"Notion publish failed: {pub[-400:]}"

    _git("add", "--", str(path.relative_to(ROOT)), "build/.notion_publish.json")
    _git("commit", "-q", "-m", f"Archive scene: {title}\n\nSaved from Claude Desktop via the wotr MCP server.")
    pcode, pout = _git("push", "-q", "origin", "master")
    pushed = "pushed to GitHub" if pcode == 0 else f"push failed: {pout[-300:]}"
    return f"saved {path.relative_to(ROOT).as_posix()} ({len(body.split())} words); {notion}; {pushed}"


@server.tool()
def log_ruling(rule_id: str, ruling: str, context: str = "") -> str:
    """Record a ruling Isaac made at the table (rule_id may be a rule id, a CONFLICTS id
    like C-001, or 'new'). Appended to RULINGS.md and pushed; applied to the index
    in the next Claude Code session."""
    RULINGS.touch()
    if RULINGS.stat().st_size == 0:
        RULINGS.write_text("# Rulings awaiting application to the index\n\nAppended by the wotr MCP server "
                           "when Isaac rules at the table. Each is applied to rules/*.yaml in Claude Code, "
                           "then moved to PROGRESS.md.\n", encoding="utf-8", newline="\n")
    entry = f"\n## {date.today().isoformat()} — {rule_id}\n\n{ruling.strip()}\n"
    if context.strip():
        entry += f"\nContext: {context.strip()}\n"
    with RULINGS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(entry)
    _git("add", "--", "RULINGS.md")
    _git("commit", "-q", "-m", f"Log ruling on {rule_id}\n\nRecorded from Claude Desktop via the wotr MCP server.")
    pcode, pout = _git("push", "-q", "origin", "master")
    return f"logged ruling on {rule_id}; " + ("pushed" if pcode == 0 else f"push failed: {pout[-300:]}")


@server.tool()
def sync_now() -> str:
    """Run build/sync.ps1: Notion wiki -> repo, repo -> Notion, Drive documents, commit, push.
    Takes a minute or two."""
    code, out = _run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                      str(ROOT / "build" / "sync.ps1")], timeout=900)
    return out[-2000:] or f"exit {code}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--http", action="store_true", help="serve streamable HTTP on --port instead of stdio")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    if args.http:
        server.run(transport="streamable-http", host="127.0.0.1", port=args.port)
    else:
        server.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
