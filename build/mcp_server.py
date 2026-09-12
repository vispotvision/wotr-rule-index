#!/usr/bin/env python3
"""WOTR MCP: the tools Natalie calls from Claude Desktop, over the rule index, the wiki mirror and the scene archive.

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
    "WOTR MCP",
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


# --------------------------------------------------------------------------
# search over the wiki mirror and the scene archive

WIKI = ROOT / "wiki"
NATALIE = ROOT / "desktop" / "NATALIE.md"


def _read(p: Path) -> str:
    t = p.read_text(encoding="utf-8", errors="replace")
    if t.startswith("---\n"):
        end = t.find("\n---\n", 4)
        if end != -1:
            t = t[end + 5:]
    return t


def _rank(root: Path, query: str, limit: int = 5) -> list[tuple[int, Path, str]]:
    terms = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
    if not terms:
        return []
    hits = []
    for p in root.rglob("*.md"):
        if p.name in ("INDEX.md", "MANIFEST.md"):
            continue
        low = p.read_text(encoding="utf-8", errors="replace").lower()
        title_bonus = 5 * sum(1 for t in terms if t in p.stem.lower())
        phrase = query.lower().strip()
        phrase_bonus = 10 * min(low.count(phrase), 5) if len(terms) > 1 else 0
        # every term present counts for more than one term repeated
        coverage = sum(1 for t in terms if t in low)
        score = title_bonus + phrase_bonus + 3 * coverage + sum(min(low.count(t), 10) for t in terms)
        if coverage < max(1, len(terms) - 1):
            score //= 3
        if score:
            hits.append((score, p, low))
    hits.sort(key=lambda x: -x[0])
    return hits[:limit]


def _snippets(text: str, query: str, n: int = 3, width: int = 220) -> list[str]:
    out = []
    for t in [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]:
        for m in re.finditer(re.escape(t), text, re.I):
            a, b = max(0, m.start() - width // 2), min(len(text), m.end() + width // 2)
            out.append("..." + text[a:b].replace("\n", " ").strip() + "...")
            if len(out) >= n:
                return out
    return out


@server.tool()
def wiki(query: str, full: bool = True) -> str:
    """Search the wiki mirror (381 pages) by keywords. Returns the best matches with
    snippets, and the full text of the top page (capped) when full=True. Faster than
    Notion; up to an hour behind it."""
    hits = _rank(WIKI, query)
    if not hits:
        return f"nothing in the wiki mirror matches '{query}'"
    out = []
    for score, p, _ in hits:
        rel = p.relative_to(WIKI).as_posix()
        text = _read(p)
        out.append(f"## {p.stem}  ({rel}, score {score})\n" + "\n".join(_snippets(text, query)))
    if full:
        top = _read(hits[0][1])
        out.append(f"\n---- full text of {hits[0][1].stem} ----\n" + top[:14000] + ("\n...[truncated]" if len(top) > 14000 else ""))
    return "\n\n".join(out)


@server.tool()
def character(name: str) -> str:
    """A character's card from the wiki mirror (the Volume I-V Character Cards and
    single-character sections), full text. Say if none exists rather than inventing."""
    cands = []
    key = name.lower()
    for p in WIKI.rglob("*.md"):
        if p.name == "INDEX.md":
            continue
        if key in p.stem.lower() or key in p.parent.name.lower():
            cands.append(p)
    if not cands:
        return f"no card for '{name}' in the wiki mirror; check Notion before writing anything numeric about them"
    cands.sort(key=lambda p: (0 if key == p.stem.lower() else 1, 0 if "character" in p.parent.name.lower() else 1, len(p.stem)))
    p = cands[0]
    text = _read(p)
    others = [c.relative_to(WIKI).as_posix() for c in cands[1:6]]
    head = f"# {p.stem}  ({p.relative_to(WIKI).as_posix()})\n"
    if others:
        head += "also matched: " + "; ".join(others) + "\n"
    return head + "\n" + text[:24000] + ("\n...[truncated]" if len(text) > 24000 else "")


@server.tool()
def fow_line(name: str) -> str:
    """The Fracture of Worlds line for a named practitioner, pulled from their card:
    Level / Stage / Band, the stat table, force-and-flow figures, EU reserve, eta.
    If the card has no numbers, says so. Never invent a number."""
    card = character(name)
    if card.startswith("no card"):
        return card
    lines = card.split("\n")
    keep = []
    grab = False
    for ln in lines:
        l = ln.strip()
        if re.search(r"\*\*(?:Level|Stage|Band|EU Reserve|Flux Density|AU/s|η|Aether Class|Soul Crystal|Coherence)\b", l) or re.search(r"\b(?:Level|Stage|Band):", l):
            keep.append(l)
        if re.match(r"^##\s+.*(?:Stats|Force and Flow|Force & Flow|Traits and Domain|Fracture of Worlds|Temperance)", l):
            grab = True
            keep.append(l)
            continue
        if grab:
            if l.startswith("## "):
                grab = False
            elif l:
                keep.append(l)
    seen, out = set(), []
    for k in keep:
        if k not in seen:
            seen.add(k)
            out.append(k)
    if not out:
        return f"{lines[0]}\nno FOW figures on this card; flag an estimate in a character's mouth or ask Isaac"
    return lines[0] + "\n" + "\n".join(out)[:12000]


@server.tool()
def scene_recall(query: str) -> str:
    """Search the scene archive (scenes/) for continuity: who said what, what happened
    where. Returns the best-matching scenes with snippets around the matches."""
    hits = _rank(SCENES, query, limit=4)
    if not hits:
        return f"no scene matches '{query}'"
    out = []
    for score, p, _ in hits:
        text = _read(p)
        title = re.search(r"(?m)^#\s+(.+)$", text)
        out.append(f"## {title.group(1) if title else p.stem}  ({p.name}, score {score})\n" + "\n".join(_snippets(text, query, n=4, width=400)))
    return "\n\n".join(out)


# --------------------------------------------------------------------------
# session start, verification, proposals


def _inventory(culture: str) -> str:
    text = NATALIE.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^# THE STANDING INVENTORY: " + re.escape(culture.upper()) + r".*?(?=^# |\Z)", text)
    if m:
        return m.group(0).strip()
    hits = _rank(WIKI, f"standing inventory {culture}", limit=1)
    if hits:
        return f"(no inventory section in NATALIE.md for {culture}; nearest wiki page: {hits[0][1].stem})\n" + _read(hits[0][1])[:6000]
    return f"No Standing Inventory exists for {culture}. Anything invented in play gets entered the same session (R6-9-RECURRENCE_RULE)."


def _running_piece(title_part: str) -> str:
    """A Running Pieces page: live from Notion when the token works, else the mirror."""
    folder = WIKI / "The Table — Running Pieces"
    cands = sorted(folder.glob("*.md")) if folder.exists() else []
    match = [p for p in cands if title_part.lower() in p.stem.lower()]
    if not match:
        return f"(no Running Pieces page matching '{title_part}'; have: {', '.join(p.stem for p in cands)})"
    p = match[0]
    text = p.read_text(encoding="utf-8", errors="replace")
    pid = re.search(r'^notion_id:\s*"?([0-9a-f-]{36})', text, re.M)
    tok = _env().get("NOTION_TOKEN")
    if pid and tok:
        try:
            os.environ.setdefault("NOTION_TOKEN", tok)
            from notion_export import block_md, children
            lines = []
            for b in children(pid.group(1)):
                lines.extend(block_md(b, 0, {}))
            live = "\n".join(lines).strip()
            if live:
                return f"# {p.stem}  (live from Notion)\n\n{live}"
        except Exception:  # noqa: BLE001
            pass
    return f"# {p.stem}  (from the mirror, may be up to an hour old)\n\n{_read(p)}"


LOADOUTS = {
    "duel": ["prose-law", "combat", "adjudication", "magic-mechanism", "pov"],
    "battle": ["prose-law", "mass-combat", "adjudication", "pov", "scene-structure"],
    "talky": ["prose-law", "dialogue", "register", "pov", "naming"],
    "quiet": ["prose-law", "pov", "scene-structure", "standing-inventory", "register"],
    "explicit": ["prose-law", "dialogue", "pov", "scene-structure"],
    "working": ["prose-law", "magic-mechanism", "combat", "codex"],
    "standard": ["prose-law", "pov", "scene-structure", "dialogue", "register"],
}


@server.tool()
def session_start(thread: str, scene_type: str = "standard", culture: str = "Kharven") -> str:
    """Run the session start protocol in one call. thread: 'Sodoku Moto', 'Hild Ice',
    'Kwon Mu-jin' or 'Ilthára Korvaeth' (matched against the State of Play pages).
    scene_type: duel | battle | talky | quiet | explicit | working | standard.
    Returns State of Play, the Ledger, Fronts, the Docket, the Standing Inventory for
    the culture, and the brief rule loadout for the scene type."""
    parts = [_running_piece("State of Play — " + thread.split("/")[0].strip()),
             _running_piece("The Ledger"), _running_piece("Fronts"), _running_piece("Open Rulings")]
    parts.append("# STANDING INVENTORY\n\n" + _inventory(culture))
    tags = LOADOUTS.get(scene_type, LOADOUTS["standard"])
    rules, _ = _select(tags, ["live"])
    parts.append(f"# RULE LOADOUT ({scene_type}: {' '.join(tags)}) — {len(rules)} live rules, brief; call load_rules for the full text\n\n"
                 + "\n\n".join(_fmt(r, full=False) for r in rules))
    pend, _ = _select(tags, ["pending", "proposed"])
    parts.append(f"# STILL UNRATIFIED for these tags: {len(pend)} — call check_docket before writing if any matters")
    parts.append("Next: advance one Front, pick what comes due from the Ledger, load the FOW line for every named practitioner (fow_line), then run Isaac's beat or offer the Scene Menu.")
    return "\n\n---\n\n".join(parts)


@server.tool()
def verify_scene(markdown: str, combat: bool = False, culture: str = "", band: str = "standard") -> str:
    """Mechanical prose checks on a draft before it is posted: em dashes, antithesis,
    countdown negation, the Ladder, apparatus-as-subject, gloss watch, signposting,
    reification budget, sentence and paragraph variance (R4-14), length band,
    interior beats, last line, Kharven recurrence (culture='Kharven'), HEMA and
    anatomy density (combat=True). Fix every FAIL, read every WARN, then post."""
    import verify
    return verify.report(verify.run(markdown, combat=combat, culture=culture or None, band=band))


@server.tool()
def propose_rule(title: str, rule_text: str, applies_to: list[str], rationale: str = "", session: str = "") -> str:
    """File a rule Natalie originated at the table as a proposal (pending Isaac's
    ratification). Appended to proposals/PROPOSED.md and pushed; folded into the next
    amendment pack extraction. rule_text should be the rule as it would read in a pack."""
    vocab = load_vocab()
    bad = [t for t in applies_to if t not in vocab]
    prop = ROOT / "proposals" / "PROPOSED.md"
    prop.parent.mkdir(exist_ok=True)
    if not prop.exists():
        prop.write_text("# Proposed rules, pending Isaac's ratification\n\nFiled from the table via WOTR MCP. Each becomes a row in the next amendment pack, or is struck.\n",
                        encoding="utf-8", newline="\n")
    entry = (f"\n## {date.today().isoformat()} — {title}\n\n**Status:** proposed\n"
             f"**applies_to:** {', '.join(t for t in applies_to if t in vocab)}"
             + (f"  (unknown tags dropped: {bad})" if bad else "") + "\n\n"
             f"{rule_text.strip()}\n")
    if rationale.strip():
        entry += f"\n*Why:* {rationale.strip()}\n"
    if session.strip():
        entry += f"\n*Session:* {session.strip()}\n"
    with prop.open("a", encoding="utf-8", newline="\n") as f:
        f.write(entry)
    _git("add", "--", "proposals/PROPOSED.md")
    _git("commit", "-q", "-m", f"Propose rule: {title}\n\nFiled from Claude Desktop via WOTR MCP; pending ratification.")
    pcode, pout = _git("push", "-q", "origin", "master")
    return f"filed '{title}' as proposed; " + ("pushed" if pcode == 0 else f"push failed: {pout[-300:]}")


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
