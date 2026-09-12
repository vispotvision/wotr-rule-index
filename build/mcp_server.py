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
import json
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


# --------------------------------------------------------------------------
# the Büri/Moto sweep, the pre-write brief, the cast index

SOURCES = ROOT / "sources"


def _reversion_map() -> list[tuple[str, str]]:
    """Struck -> governs pairs, read from the Moto Reversion Ledger's tables plus the
    Canon Amendment's Sātūlagi strike. Read at call time so the source stays authoritative."""
    pairs: list[tuple[str, str]] = []
    src = next(SOURCES.glob("*Moto_Reversion*"), None)
    if src:
        for ln in src.read_text(encoding="utf-8").split("\n"):
            s = ln.strip()
            if not s.startswith("|") or re.match(r"^\|\s*-", s):
                continue
            cells = [c.strip().strip("*").strip() for c in s.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and cells[0] != "Struck":
                pairs.append((cells[0], cells[1]))
    pairs += [("Sātūlagi", "(struck; the Inner World / Kharven)"), ("Satulagi", "(struck)"), ("Buri", "Moto")]
    # longest first so "Ajiin Devter" is reported before "Ajiin"
    pairs.sort(key=lambda p: -len(p[0]))
    return pairs


@server.tool()
def stale_names(scope: str = "all", max_files: int = 60) -> str:
    """The Büri/Moto sweep: every wiki page and scene still carrying a struck
    Büri-register term (from the Moto Reversion Ledger's tables: Büri, Ajiin, Altan,
    Nüdel, Khar Ild, the Seven Works, Sātūlagi...). scope: all | wiki | scenes.
    Returns per-file counts with the governing replacement, worst first. Nothing is
    edited; the ruling is Moto in all new prose, old files flagged."""
    roots = {"wiki": [WIKI], "scenes": [SCENES], "all": [WIKI, SCENES]}.get(scope, [WIKI, SCENES])
    pairs = _reversion_map()
    rx = {old: re.compile(r"(?<![\w\-])" + re.escape(old) + r"(?![\w\-])") for old, _ in pairs}
    gov = dict(pairs)
    results = []
    total = 0
    for root in roots:
        for p in root.rglob("*.md"):
            if p.name in ("INDEX.md", "MANIFEST.md", "CAST.md", "ARCS.md"):
                continue
            text = _read(p)
            found = {}
            for old, _ in pairs:
                n = len(rx[old].findall(text))
                if n:
                    found[old] = n
            if found:
                # do not double count "Ajiin" inside "Söröl Ajiin"
                lines = [ln for ln in text.split("\n") if any(rx[o].search(ln) for o in found)][:3]
                cnt = sum(found.values())
                total += cnt
                results.append((cnt, p.relative_to(ROOT).as_posix(), found, lines))
    results.sort(key=lambda r: -r[0])
    out = [f"{len(results)} files still carry Büri-register terms ({total} hits) in {scope}. Ruling 2026-09-12: Moto and Hataraki, not Ajiin. Governing forms in brackets."]
    for cnt, rel, found, lines in results[:max_files]:
        terms = ", ".join(f"{o}×{n} [{gov.get(o, '?')}]" for o, n in sorted(found.items(), key=lambda x: -x[1]))
        out.append(f"\n{rel}  ({cnt})\n  {terms}")
        for ln in lines:
            out.append(f"    > {ln.strip()[:140]}")
    if len(results) > max_files:
        out.append(f"\n... {len(results) - max_files} more files")
    return "\n".join(out)


@server.tool()
def scene_brief(beat: str, thread: str = "", scene_type: str = "standard", culture: str = "Kharven", characters: list[str] | None = None) -> str:
    """The pre-write, assembled from the rules. Give the beat Isaac handed you; get back
    the template you must fill before drafting: POV choice (write from whoever knows
    least, R5-C1), what the POV knows / wrongly believes / the reader knows, the
    ignorance-quota item, the misreading, the Single Act (battles), two Standing
    Inventory items, the cost, the last line; plus FOW lines for the named characters
    and the rule loadout for the scene type. Fill every blank in author notes, then draft."""
    tags = LOADOUTS.get(scene_type, LOADOUTS["standard"])
    rules, _ = _select(tags, ["live"])
    pend, _ = _select(tags, ["pending", "proposed"])
    inv = _inventory(culture)
    recurrence = ""
    m = re.search(r"\*\*Recurrence.*?:\*\*(.*?)(?:\.\s|\n)", inv, re.S)
    if m:
        recurrence = m.group(1).strip()
    fow = []
    for c in characters or []:
        fow.append(fow_line(c).split("\n", 12)[0:12])
    lines = [
        f"# SCENE BRIEF — {scene_type}" + (f" — {thread}" if thread else ""),
        f"Beat: {beat.strip()}",
        "",
        "## Fill before drafting (author notes)",
        "1. POV: ____  (write from whoever knows least about what is coming, R5-C1-WRITE_FROM_LEAST_KNOWING; a default, breakable with reason)",
        "2. This POV knows: ____ | wrongly believes: ____ | the reader knows that they do not: ____  (R5-C1-INFO_TRACKED_PER_POV)",
        "3. Ignorance quota, one thing the POV notices and cannot interpret, unresolved this scene: ____  (R6-3-IGNORANCE_QUOTA)",
        "4. Misreading, one confident inference that is wrong and stays wrong, well-reasoned: ____  (R6-4-MISREADING_BUDGET, R5-C1-WELL_REASONED_WRONG_CONCLUSION)",
        "5. What it costs, specific and visible (reserve, body, debt, reputation, who saw): ____  (Table Rule 5; R12-1-PACK_SEVEN_SURVIVORS)",
        "6. The lie: one thing an NPC says that is wrong and stays uncorrected (once per session): ____  (Table Rule 8)",
        f"7. Standing Inventory, two minimum ({culture}): ____ and ____   (R6-9-RECURRENCE_RULE)" + (f"  — pick from: {recurrence}" if recurrence else ""),
        "8. Ends on: ____  (physical action, an NPC line, or a thing he can now see; never a question at Isaac. Table Rule 1)",
        "9. Length band: ____  (conversational 300–700 / standard 700–1,500 / set piece 2,500+; default the middle. Table Rule 2)",
    ]
    if scene_type in ("duel", "working"):
        lines += [
            "10. Each fighter's combat vocabulary, assigned before the technique (Blade / Verdict / Percussion / Expenditure): ____  (R1-1-THREE_VOCABULARIES_RULING)",
            "11. The read: what evidence the POV gets, over which two or three exchanges, before anything kills (R12-3-COMBAT_EXCHANGE_OWES, R12-3-NAMED_INVENTOR_RULE): ____",
            "12. Which two of the four explaining voices carry the mechanism (R12-4-VOICE_MIXING_RULE): ____",
            "13. Stat that decides each contested action, by row (R14-3-STATS_DECIDE_TABLE, R14-3-TRACEABILITY): ____",
        ]
    if scene_type == "battle":
        lines += [
            "10. The Single Act: physical, unrepeatable, witnessed, ambiguous in the moment (R2-5-SINGLE_ACT_CONDITIONS): ____",
            "11. The three who carry interiority; everyone else exterior (R1-3-NAME_THREE_RULE): ____",
            "12. Practitioner POV closed during the engagement (R3-9-PRACTITIONER_POV_RULING): confirm ____",
        ]
    if fow:
        lines += ["", "## FOW lines (never invent a number)"]
        for block in fow:
            lines += ["\n".join(block), ""]
    lines += ["", f"## Rule loadout ({' '.join(tags)}) — {len(rules)} live, brief; call load_rules for full text", ""]
    lines += [_fmt(r, full=False) for r in rules[:60]]
    if len(rules) > 60:
        lines.append(f"... {len(rules) - 60} more; load_rules gives all of them")
    lines += ["", f"## Unratified for these tags: {len(pend)} (check_docket before writing if one would change the scene)",
              "", "Then: draft → verify_scene (fix every FAIL) → post → archive_scene when finished."]
    return "\n".join(lines)


@server.tool()
def cast_index(write: bool = True) -> str:
    """Who appears in which scene. Matches every wiki character-card name (and the
    voice roster) against scenes/, writes scenes/CAST.md and, if missing, a
    scenes/ARCS.md reading-order skeleton grouped by the numbered prefixes. Returns
    the cast list."""
    names = set()
    for p in WIKI.rglob("*.md"):
        if "character card" in p.parent.name.lower() or p.parent.name in ("Characters", "Sodoku Moto", "Hild Ice (Stark) — The Sword Princess"):
            stem = re.split(r"\s+[—·]\s+", p.stem)[0].strip()
            if 3 <= len(stem) <= 40 and not stem.lower().startswith("volume"):
                names.add(stem)
    for n in ["Sodoku Moto", "Yoko Mishiro", "Emira", "Black Agent", "Cozbi Mahuo", "Lambert", "Pietro", "Hild Ice", "Renard Greymane",
              "Dhaerin", "Rengai", "Niran", "Mira", "Haruki", "Verinus", "Darius", "Aurelian", "Charles", "Wren", "Dabney", "Kwon Mu-jin", "Ilthára", "Brida", "Dougou", "Rashani"]:
        names.add(n)
    scenes = sorted(p for p in SCENES.glob("*.md") if p.name not in ("MANIFEST.md", "CAST.md", "ARCS.md"))
    texts = {p: _read(p) for p in scenes}
    appear: dict[str, list[str]] = {}
    for n in sorted(names):
        first = n.split()[0]
        rx = re.compile(r"(?<!\w)" + re.escape(n) + r"(?!\w)")
        rx_first = re.compile(r"(?<!\w)" + re.escape(first) + r"(?!\w)") if len(first) >= 4 else None
        hits = []
        for p, t in texts.items():
            c = len(rx.findall(t))
            if c == 0 and rx_first:
                c = len(rx_first.findall(t))
            if c >= 2:
                hits.append((c, p.name))
        if hits:
            hits.sort(key=lambda x: -x[0])
            appear[n] = [f"{f} ({c})" for c, f in hits]
    out = ["# Cast index", "", f"{len(appear)} named characters across {len(scenes)} scenes; count is mentions. Generated by WOTR MCP cast_index; regenerate after new scenes.", ""]
    for n, files in sorted(appear.items(), key=lambda kv: -len(kv[1])):
        out.append(f"## {n} ({len(files)} scenes)")
        out.append(", ".join(files))
        out.append("")
    text = "\n".join(out)
    if write:
        (SCENES / "CAST.md").write_text(text, encoding="utf-8", newline="\n")
        arcs = SCENES / "ARCS.md"
        if not arcs.exists():
            groups: dict[str, list[str]] = {}
            loose = []
            for p in scenes:
                m = re.match(r"^(\d+)_([a-z]+)_", p.name)
                if m:
                    groups.setdefault(m.group(2), []).append(p.name)
                else:
                    loose.append(p.name)
            a = ["# Reading order", "", "Edit freely: one heading per arc, scenes in order. docs_export.py compiles The Scene Archive in this order when the file exists.", ""]
            for g, files in sorted(groups.items()):
                a.append(f"## {g.capitalize()} arc")
                a += [f"- {f}" for f in sorted(files)]
                a.append("")
            a.append("## Unplaced")
            a += [f"- {f}" for f in loose]
            arcs.write_text("\n".join(a) + "\n", encoding="utf-8", newline="\n")
    return text


# --------------------------------------------------------------------------
# characters: create and update cards in Notion + the mirror; convert old material

CANON = Path(r"C:\Users\isaac\Documents\WOTR True Canon")
FOW_XLSX = CANON / "FOW_Stat_and_Magic_System_Codex.xlsx"
WIKI_MANIFEST = WIKI / ".manifest.json"
SHEET_SECTIONS = [
    ("I · Identity", "name, house/line and register (Moto canon; five strata), age, origin, affiliation, status, Level / Stage / Band on one line, and the Catalyst Event — everything downstream is its consequence"),
    ("II · Soul Architecture", "Soul Crystal (Essence Core, Aether Shell, Attraction Layer), Crystal State, Aether Class, Essence Typology, Coherence Band and η"),
    ("III · Work Architecture", "Wellspring harmonisations: which of the Sixty answer, Family and Physics Domain from the Master Codex, the Craft (Magicraft / Spellcraft / Runecraft / Draftcraft) and Category of each working"),
    ("IV–V · Stats", "the Eight Primaries with Grade and Sub-Stat peaks: Gnosis, Tempering, Ardency, Resilience, Dexterity, Vitality, Dominion, Harmonics. Grades come off the Tier Grade table; the Stage sets the ceiling"),
    ("VI–VII · Force and Flow", "Strike Force band, Attack Speed, Reaction, Travel, Aura Pressure Field radius, Domain Pressure, EU Reserve, Flux Density, AU/s, η — the part a Measurewright could confirm"),
    ("VIII–IX · Traits and Domain", "each Trait names the Lattice property it alters (R17-5-TRAIT_SCOPE); Domain state by Stage (seed at VII)"),
    ("X · Techniques", "summary card (Effect, Cost, Limit, Counter, What nobody knows) + full Design Chain + Codex line + FOW line per technique; Counter mandatory (R12-3-COUNTER_MANDATORY); every technique statable as 'it does X to Y, which under Z produces W' (R17-2-THE_TEST)"),
    ("XI · Spirit Axes", "who they are bonded to; sited here because the people someone loves are load-bearing"),
    ("XII · Resistances", "what they can take: per-Wellspring / per-Family resistances, Resilience against hostile workings"),
    ("XIII · Physical Description", "full inventory on first sight: hair by comparison, face, body with areas named, clothing with fit and wear, distinguishing marks (Table Rule 11)"),
    ("XIV · Psychology", "what they refuse, what they survived, what they believe that costs them (character first); an unswappable voice"),
    ("XV · Equipment", "weapons with mass, length, point of balance, armour tier beaten/failed (R13-9-ITEM_GUIDE_WEAPON_ENTRY); proof-marks; artefacts with their own Operation line"),
    ("XVI · Temperance Record", "the ladder climbed: each Stage reached, its threshold catalyst, and when"),
    ("XVII · Fracture Log", "every fracture, consolidated or unconsolidated, with its price — the unconsolidated ones are the character"),
]


def _wiki_manifest() -> dict:
    return json.loads(WIKI_MANIFEST.read_text(encoding="utf-8")) if WIKI_MANIFEST.exists() else {}


def _find_page_id_by_title(title: str) -> tuple[str | None, str | None]:
    m = _wiki_manifest()
    for pid, v in m.items():
        if v["title"].lower() == title.lower():
            return pid, v["rel"]
    for pid, v in m.items():
        if title.lower() in v["title"].lower():
            return pid, v["rel"]
    return None, None


def _publish_helpers():
    os.environ.setdefault("NOTION_TOKEN", _env().get("NOTION_TOKEN", ""))
    import notion_publish as npub
    return npub


def _write_mirror(rel: str, title: str, pid: str, section: str, markdown: str, tags: list[str]) -> Path:
    p = WIKI / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    body = markdown.strip()
    if not re.match(r"^#\s", body):
        body = f"# {title}\n\n{body}"
    fm = {"title": title, "notion_id": pid, "notion_url": f"https://www.notion.so/{pid.replace('-', '')}",
          "section": section, "tags": tags, "last_edited": datetime.now().isoformat(timespec="seconds"), "verification": None}
    head = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()] + ["---", ""]
    p.write_text("\n".join(head) + body + "\n", encoding="utf-8", newline="\n")
    m = _wiki_manifest()
    m[pid] = {"rel": rel, "edited": fm["last_edited"], "title": title}
    WIKI_MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


@server.tool()
def create_character(name: str, markdown: str, volume: str = "Volume I — Character Cards", tags: list[str] | None = None) -> str:
    """Add a new character card: creates the Notion page under the given volume
    (Volume I / III / IV / V — Character Cards, or 'Characters'), writes the wiki
    mirror file, commits and pushes. markdown is the full card in the seventeen-section
    format (see convert_character for the skeleton). Refuses a name that already has a
    card; use update_character for those. Numbers must come from the FOW tables or
    Isaac; anything estimated is marked pending in the card."""
    pid_existing, rel_existing = _find_page_id_by_title(name)
    if pid_existing and rel_existing and name.lower() == _wiki_manifest()[pid_existing]["title"].lower():
        return f"a card named '{name}' already exists ({rel_existing}); use update_character"
    vol_id, vol_rel = _find_page_id_by_title(volume)
    if not vol_id:
        return f"no volume page named '{volume}' in the wiki mirror"
    npub = _publish_helpers()
    blocks = npub.md_to_blocks(markdown if re.match(r"^#\s", markdown.strip()) else markdown)
    try:
        pid = npub.create_page({"page_id": vol_id}, name, blocks)
    except Exception as e:  # noqa: BLE001
        return f"Notion refused the page: {str(e)[:300]}"
    section = _wiki_manifest()[vol_id]["title"]
    rel = f"{section}/{name}.md"
    p = _write_mirror(rel, name, pid, section, markdown, tags or ["Characters"])
    _git("add", "--", str(p.relative_to(ROOT)), "wiki/.manifest.json")
    _git("commit", "-q", "-m", f"Add character card: {name}\n\nCreated from Claude Desktop via WOTR MCP; page {pid} under {section}.")
    pcode, pout = _git("push", "-q", "origin", "master")
    return f"created '{name}' in Notion under {section} (page {pid}), mirrored to {rel}; " + ("pushed" if pcode == 0 else f"push failed: {pout[-200:]}")


@server.tool()
def update_character(name: str, markdown: str) -> str:
    """Replace an existing character card's body in Notion (same page id, links
    survive) and in the wiki mirror, then commit and push. markdown is the full
    replacement card, not a diff."""
    pid, rel = _find_page_id_by_title(name)
    if not pid:
        return f"no card named '{name}' in the wiki mirror; use create_character"
    npub = _publish_helpers()
    try:
        npub.replace_body(pid, npub.md_to_blocks(markdown))
    except Exception as e:  # noqa: BLE001
        return f"Notion refused the update: {str(e)[:300]}"
    title = _wiki_manifest()[pid]["title"]
    section = rel.split("/")[0]
    old = _read(WIKI / rel) if (WIKI / rel).exists() else ""
    tags = []
    p = _write_mirror(rel, title, pid, section, markdown, tags)
    _git("add", "--", str(p.relative_to(ROOT)), "wiki/.manifest.json")
    _git("commit", "-q", "-m", f"Update character card: {title}\n\nReplaced from Claude Desktop via WOTR MCP; page {pid}.")
    pcode, pout = _git("push", "-q", "origin", "master")
    return f"updated '{title}' (page {pid}, {len(markdown.split())} words, was {len(old.split())}); " + ("pushed" if pcode == 0 else f"push failed: {pout[-200:]}")


def _fow_tables() -> str:
    if not FOW_XLSX.exists():
        return "(FOW_Stat_and_Magic_System_Codex.xlsx not found; check the canon folder)"
    try:
        import openpyxl
    except ImportError:
        return "(openpyxl missing: pip install openpyxl)"
    wb = openpyxl.load_workbook(FOW_XLSX, read_only=True, data_only=True)
    out = []
    for sheet, first, last in (("Core Progression", 1, 30), ("Physical Benchmarks", 1, 18)):
        ws = wb[sheet]
        out.append(f"### {sheet}")
        for r in list(ws.iter_rows(values_only=True))[first - 1:last]:
            cells = [str(c).strip() for c in r if c is not None and str(c).strip()]
            if cells:
                out.append("| " + " | ".join(cells) + " |")
        out.append("")
    return "\n".join(out)


def _trello_cards(obj) -> list[dict]:
    """Cards out of a Trello export (board JSON, a list of cards, or one card)."""
    if isinstance(obj, dict) and "cards" in obj:
        lists = {l["id"]: l.get("name", "") for l in obj.get("lists", [])}
        cards = []
        for c in obj["cards"]:
            if c.get("closed"):
                continue
            cards.append({"name": c.get("name", ""), "list": lists.get(c.get("idList"), ""), "desc": c.get("desc", ""),
                          "labels": [l.get("name", "") for l in c.get("labels", [])],
                          "checklists": [(cl.get("name", ""), [i.get("name", "") for i in cl.get("checkItems", [])])
                                         for cl in obj.get("checklists", []) if cl.get("idCard") and cl.get("idCard") == c.get("id")],
                          "custom": c.get("customFieldItems", [])})
        return cards
    if isinstance(obj, list):
        return [{"name": c.get("name", ""), "list": "", "desc": c.get("desc", ""), "labels": [l.get("name", "") for l in c.get("labels", [])], "checklists": [], "custom": []} for c in obj if isinstance(c, dict)]
    if isinstance(obj, dict):
        return [{"name": obj.get("name", ""), "list": "", "desc": obj.get("desc", obj.get("description", "")), "labels": [], "checklists": [], "custom": []}]
    return []


@server.tool()
def trello_cards(json_path: str, list_name: str = "", query: str = "") -> str:
    """List the cards in a Trello board export (Trello → Menu → Print and export →
    Export as JSON). Filter by list name or a keyword. Use the card name with
    convert_character(source=<the card's text>) or pass the whole export path."""
    p = Path(json_path)
    if not p.exists():
        return f"no file at {json_path}"
    cards = _trello_cards(json.loads(p.read_text(encoding="utf-8", errors="replace")))
    if list_name:
        cards = [c for c in cards if list_name.lower() in c["list"].lower()]
    if query:
        cards = [c for c in cards if query.lower() in (c["name"] + c["desc"]).lower()]
    out = [f"{len(cards)} cards" + (f" in list '{list_name}'" if list_name else "")]
    for c in cards[:200]:
        out.append(f"- {c['name']}  [{c['list']}]  {len(c['desc'].split())} words" + (f"  labels: {', '.join(c['labels'])}" if c["labels"] else ""))
    return "\n".join(out)


@server.tool()
def convert_character(source: str, name: str = "", json_path: str = "", target_volume: str = "Volume I — Character Cards") -> str:
    """Convert an old character record (a Trello card's JSON or text, an old sheet,
    any prose) into the current system: returns a conversion brief — the source
    material, every old-register name flagged with its Moto-canon form, the
    seventeen-section skeleton with what each section must hold and which rules
    govern it, the FOW Band / Stage / Tier Grade tables so numbers land on the
    real scale, and the rule loadout. You write the card from the brief, then
    create_character saves it. Never invent a number: anything the source does not
    give and the tables do not fix is written as 'pending Isaac' in the card.
    source may be raw text, a JSON string, or a card name when json_path is given."""
    text = source
    cards = []
    if json_path:
        p = Path(json_path)
        if p.exists():
            cards = _trello_cards(json.loads(p.read_text(encoding="utf-8", errors="replace")))
            hit = [c for c in cards if source.lower() in c["name"].lower()] if source else []
            if hit:
                c = hit[0]
                name = name or c["name"]
                text = f"Card: {c['name']}\nList: {c['list']}\nLabels: {', '.join(c['labels'])}\n\n{c['desc']}\n" + "".join(
                    f"\nChecklist {cl}:\n" + "\n".join(f"- {i}" for i in items) for cl, items in c["checklists"])
    else:
        try:
            obj = json.loads(source)
            cs = _trello_cards(obj)
            if cs:
                c = cs[0]
                name = name or c["name"]
                text = f"Card: {c['name']}\nList: {c['list']}\nLabels: {', '.join(c['labels'])}\n\n{c['desc']}\n" + "".join(
                    f"\nChecklist {cl}:\n" + "\n".join(f"- {i}" for i in items) for cl, items in c["checklists"])
        except (json.JSONDecodeError, TypeError):
            pass
    name = name or (re.search(r"(?m)^#\s+(.+)$", text).group(1).strip() if re.search(r"(?m)^#\s+(.+)$", text) else "Unnamed")

    # stale names in the source
    stale = []
    for old, new in _reversion_map():
        n = len(re.findall(r"(?<![\w\-])" + re.escape(old) + r"(?![\w\-])", text))
        if n:
            stale.append(f"{old} ×{n} → {new}")
    existing_pid, existing_rel = _find_page_id_by_title(name)
    numbers = re.findall(r"\b(?:Level|Stage|Band|Grade|EU|η|AU/s)\b[^.\n]{0,40}", text)

    rules_cs, _ = _select(["character-sheet", "stats", "naming", "codex", "magic-design"], ["live"])
    lines = [f"# CONVERSION BRIEF — {name} → {target_volume}", ""]
    if existing_pid:
        lines.append(f"NOTE: a card already exists ({existing_rel}); this is an update, use update_character when done.")
    lines += ["## Source material (verbatim, the only facts you may use)", "", text.strip()[:12000], ""]
    if stale:
        lines += ["## Old-register names in the source — write the governing form", ""] + [f"- {s}" for s in stale] + [""]
    lines += ["## Numbers present in the source (everything else numeric is pending Isaac)", ""] + ([f"- {n.strip()}" for n in numbers[:40]] or ["- none"]) + [""]
    lines += ["## The seventeen-section skeleton — use these exact headings", ""]
    for i, (h, what) in enumerate(SHEET_SECTIONS, 1):
        lines.append(f"## {h}\n  {what}")
    lines += ["", "Format reference: any card in Volume I (character('Cozbi Mahuo')). Under 16,348 characters.", ""]
    lines += ["## FOW scale (from FOW_Stat_and_Magic_System_Codex.xlsx)", "", _fow_tables()]
    lines += ["## Conversion rules", "",
              "- Old stats map to the Tier Grade table by range; a Stage sets the stat ceiling; a Level sets the Band. If the source gives none of these, write 'Level/Stage/Band: pending Isaac' and do not pick.",
              "- Names: Moto register for the Moto bloodline and its lines (Kōkan, Byakuya, Kurenai, Tenrai, Shirogane, Akagane, Amagiri); five strata per the Inner World Naming Amendment; naming register is not ethnicity.",
              "- Every technique: summary card + Design Chain + Codex line (glyphs, Wellspring, Family, Physics Domain, Category, Stage) + FOW line; Counter mandatory; name the real phenomenon (R13-3-PHENOMENON_MANDATE).",
              "- Character first: what they refuse, what they survived, what they believe that costs them; then the phenomenon; then the Codex.",
              "- Anything you originate (a Wellspring assignment, a Trait, a fracture the source never mentioned) is marked 'originated, pending ratification' in the card and filed with propose_rule if it is a rule.",
              "", f"## Rule loadout (character-sheet stats naming codex magic-design) — {len(rules_cs)} live, brief", ""]
    lines += [_fmt(r, full=False) for r in rules_cs[:70]]
    if len(rules_cs) > 70:
        lines.append(f"... {len(rules_cs) - 70} more via load_rules")
    lines += ["", "Then: write the card → verify_scene(markdown) for prose sections → create_character(name, markdown, volume)."]
    return "\n".join(lines)


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
