---
name: wotr-ops
description: "Procedures for running the War of the Realms machine at /home/oridon/wotr-rule-index that no tool returns — turning a transcript or a pasted scene into archived scenes in the right order, adding a character card without making a second one, knowing which wotr MCP call commits and pushes before you make it, and keeping the scene indexes honest. Use when Isaac says 'archive this scene', 'cut this transcript into scenes', 'add this character', 'close out the session', or asks where a rule, a number or a fact lives. Do NOT use for writing prose; that is wotr-write (the craft law, registers, stat tables and loadouts are served live by the wotr MCP, and desktop/NATALIE.md governs the drafting)."
---

# WOTR operations

Procedures that span several tools plus git plus Notion, where **the ordering is
the knowledge** and a silent failure sits at the end of the obvious path.

This skill deliberately contains no craft law. See "The one rule" below.

## 1. The desk, and the one rule

The desk is `/home/oridon/wotr-rule-index`. Read its `CLAUDE.md`, then
`AGENTS.md`, then `CONTINUE.md` newest block first, before WOTR work.

**The one rule: each kind of law has exactly one home, and this file is not it.**

| what you want | where it lives |
|---|---|
| craft law, registers, stat tables | `load_rules` / `check_docket` / `rule` — live, newest pack first |
| a number, a card, a page | `fow_line` / `character` / `wiki` — never recall, always call |
| table protocol, prose standards | `desktop/NATALIE.md` |
| repo constraints | `CLAUDE.md`, `AGENTS.md` |
| Cowork connector etiquette | `desktop/COWORK.md` |

Nothing above is restated here. A second copy drifts from the first and then
degrades output — that is not a hypothetical, it is what happened to
`desktop/PROJECT_INSTRUCTIONS.md`, which grew a condensed duplicate of NATALIE.md's
prose law until the standing prompt was a quarter of what the model was handed.

**The interpreter is not the one on PATH.** Use `bash build/py.sh build/<tool>.py …`
— it sources `build/env.sh` and execs `$WOTR_PYTHON`. Bare `python build/query.py`
prints a missing-pyyaml error; never act on that message.

## 2. Before any write: know that it commits and pushes

Most WOTR MCP writers commit **and push to origin/master** the instant they
return. The split is not guessable from the names, and there is no dry run.

**Derive the list, never carry one:**

```bash
grep -n -A 30 'READ_ONLY_TOOLS = {' build/mcp_server.py
```

A tool not named in that set commits and pushes; several also write Notion.
(At the time of writing: 44 tools, 25 read-only — so 19 writers. Check, don't
trust that count.)

Read-only there means read-only **to git and Notion, not to disk**. Some tools in
the set still write files — `cast_scene`, `voice_fingerprints`, `timeline` (writes
the TIMELINE skeleton on first call), `narrate_scene`.

Three named traps:

- **`archive_scene` does not verify.** It slugs, writes, publishes to Notion,
  commits and pushes, and calls no checker. Get zero FAIL *before* the call:
  `bash build/py.sh build/verify.py <draft>.md --combat --culture <Kharven|…> --band <set-piece|standard>`.
  A WARN is a read; a FAIL is a stop. If a FAIL is wrong, that is a `CONFLICTS.md`
  row or a ruling for Isaac — fix the data, not the checker.
- **`archive_scene` on an existing slug does not refuse.** It writes
  `<slug>_YYYYMMDD_HHMM.md` — a duplicate with a plausible name and nothing
  saying which is canon.
- **`session_end` reads like a report and is not.** It appends to
  `table/sessions.yaml`, commits and pushes, and ages every open Ledger line.
  Call it once per scene and keep the output.

Per `AGENTS.md`, nothing is archived by an agent: Isaac's word comes before any
writer. The session close itself belongs to the `judger` skill.

## 3. Intake: a transcript becomes archived scenes

The most common job, and it has a dependency nothing states.

1. **Stage the raw file anywhere but `scenes/`.** `build/sync.sh` publishes
   `scenes/*.md` from the working tree, committed or not, so a half-cut transcript
   dropped there reaches Notion within the hour.
2. **Cut on the file's own headings, never a byte count.** One part = one
   `archive_scene` call, titled with its part number.
3. **`scene_context` on each part first.** Take its "names with no page" list.
4. **Create the missing cards BEFORE any `cast_index` run.** This is the
   dependency. `cast_index` builds `scenes/CAST.md` by matching names against wiki
   character-card page titles — a character with no card is invisible to it, and
   the scene count silently under-reports. Run the check in §4 first.
5. **`archive_scene` each part in reading order**, then `cast_index(write=True)`.
6. **Place the new scenes in `scenes/TIMELINE.md` and `scenes/CONTINUITY.md` by
   hand.** The `timeline` tool only reads the file back; `build/audit.py` returns
   it untouched once it exists. A scene the text does not locate goes at the end,
   listed with the reason — not guessed at. That is the file's own rule.
7. **Commit `CAST.md` and `TIMELINE.md` promptly** — `build/sync.sh` commits those
   paths wholesale and will otherwise sweep your work into a "Wiki sync" commit.
8. **Sweep the paste at the end:**

```bash
git ls-files --others --exclude-standard -- '*.md'
```

Do **not** use `git status --porcelain | grep '^?? .*\.md$'`. Git quotes names
containing apostrophes or spaces, so that form returns **0** on this tree while
four untracked scenes sit at the root. For each hit decide and say which: it is a
scene (move it in, then run §4) or it is a paste already split (delete it).

## 4. A new character card: check both sides of the em-dash

Stops a duplicate card being born. Card titles carry epithets — `Kirishima
Hae-jin — Kaalabad, the Radiant God of Knights` — and a check that splits on the
em-dash and compares only the first segment will not see "Kaalabad". That exact
miss created a second Kaalabad card.

Before `create_character`, search the **whole** title, both sides:

```bash
find wiki -ipath '*haracter*' -iname '*<name>*'
grep -ril '<name>' wiki --include='*.md' | head
```

If anything comes back, it is `update_character` (which replaces the whole body —
read the card first), or it is Isaac's call which is canon. Never both.

Also worth knowing: several heavily-used names are hard-coded as known cast in
`cast_index` yet have no card at all, so `fow_line` answers "no card exists" for
them. Check before assuming a character is missing from the world rather than
from the wiki.

## 5. After anything lands in `scenes/`: diff the indexes

Index drift is not an accident anyone can remember to avoid — it is the
guaranteed output of the normal archiving path, and it compounds once per scene.
It is why `TIMELINE.md` reached 87 rows against 160 scene files with two rows
pointing at renamed files.

It cannot be automated away on purpose: `build/audit.py` returns `TIMELINE.md`
untouched if it exists, `cast_index` writes `ARCS.md` only if missing, and nothing
writes `MANIFEST.md`. Those are do-not-clobber guards protecting hand-reasoned
content. So: **diff, then append by hand.**

```bash
bash build/py.sh -c "
import os,re
idx={'MANIFEST.md','CAST.md','ARCS.md','TIMELINE.md','CONTINUITY.md'}
files={x for x in os.listdir('scenes') if x.endswith('.md')}-idx
for n in sorted(idx):
    p=os.path.join('scenes',n)
    if not os.path.exists(p): print(f'{n:16} MISSING'); continue
    t=open(p,encoding='utf-8').read()
    listed={m for m in files if m in t}
    print(f'{n:16} {len(listed):3}/{len(files)} listed, {len(files-listed)} missing')
"
```

Anything non-zero in the last column is work. A new index file also needs adding
to `SKIP_NAMES` in `build/embed_index.py`, or it gets embedded and comes back out
of `scene_recall` as though it were a scene.

## 6. Changing what an agent surface is told

The instinct when output degrades is to paste more law into a prompt file. That
is what caused the degradation. Before adding a line to `NATALIE.md`,
`PROJECT_INSTRUCTIONS.md`, `CLAUDE.md` or `AGENTS.md`:

1. **Is it already said somewhere?** If yes, point at that; do not restate.
2. **Which surface actually reads this file?** The Desktop project reads the
   Instructions box and Knowledge. Claude Code reads `CLAUDE.md`/`AGENTS.md` and
   `.claude/skills/`. A skill does not reach a Desktop project chat.
3. **Does it shrink or grow the standing prompt?** `bash build/instructions_box.sh`
   builds the real box; check the size before and after. NATALIE.md must be the
   largest thing in it.
4. **Is the claim still true?** Prompt files rot against the code. `NATALIE.md`
   claims `session_start` "does steps 1 to 7 in one call"; the function performs
   no `wiki`, `character`, `fow_line` or `scene_context` call at all. A prompt
   that overstates a tool teaches the model to skip the work the tool skipped.
