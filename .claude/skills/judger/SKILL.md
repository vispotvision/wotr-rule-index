---
name: judger
description: The Judger's assistant for War of the Realms — draft the session close for an archived scene (Ledger lines, Front ticks, NPC wants and lies, rulings, contradictions, a player-safe recap) as proposals Isaac approves one by one, and apply the ones he approves. Use after a Discord scene is archived with /scene save, after any scene lands in scenes/ without a close, or when Isaac says "/judger".
---

# The Judger's assistant

Isaac is the Judger. When a scene is archived — by the Discord bot's `/scene save`
or by Natalie's `archive_scene` — the table still owes a session close: what goes
on the Ledger, which Front ticked, what an NPC now wants or lied about, what was
ruled, what contradicts a card. `session_end` in the MCP drafts that by regex and
logs the session; this skill drafts it by reading, and writes nothing to the table
until Isaac says which lines he approves.

Repo: `/home/oridon/wotr-rule-index`. Run everything from there.

## Mode 1 — draft the close: `/judger <slug|latest>`

Run the workflow:

```
Workflow({ name: "judger-assist", args: { scenes: ["<slug>"], thread: "<thread name, optional>" } })
```

`scenes: "latest"` takes the newest file in `scenes/`. `thread` is a thread name
from `table/fronts.yaml` (`python build/book_tools.py fronts` lists them); leave it
out and the workflow infers it from `scenes/ARCS.md` and says so.

Five stages per scene, no writes: **Gather** (the scene, `scene_context`, verify,
Fronts, Due, Roster, Ledger, timeline, docket, conflicts into
`bot/queue/<slug>.gather.md`) → **Read** (a reader of record extracts every fact
with its verbatim quote; a rules clerk finds rulings made in play, rule questions
raised, contradictions) → **Propose** (each fact becomes the exact MCP call:
`ledger_add`, `advance_front`, `npc_set`, `log_ruling`, `propose_rule`, or a note
for Isaac's hands) → **Check** (a skeptic tries to kill each proposal: quote not in
the scene, inference dressed as fact, already on the Ledger, bad args) → **Note**
(`bot/queue/<slug>.judger.md` for Isaac, `bot/queue/<slug>.judger.json` for the
bot and for Mode 2).

When it returns, show Isaac the "For your approval" section and the path of the
note. Do not apply anything.

## Mode 2 — apply what Isaac approved: `/judger apply <slug> P01 P03 ...`

```
python build/judger_apply.py <slug>             # list proposals and their state
python build/judger_apply.py <slug> P01 P03     # run those ids
python build/judger_apply.py <slug> --all       # run every proposal not yet applied
```

Only on Isaac's word, and only the ids he names (`--all` when he says "all of
it"). The script calls the MCP's own write tools with the proposal's args, commits
the table the way the tools do, and records each id under `applied` in the JSON
so nothing runs twice. `card_note` / `timeline_note` / `inventory_note` /
`conflict_note` are printed for Isaac to act on by hand — they touch Notion pages
or repo files the tools do not own. Report what ran and what failed, verbatim.

## The Discord side (contract with bot/PLAN.md)

`bot/queue/<slug>.judger.json` is the handoff: `{"scene", "thread", "proposals":
[{id, tool, args, quote, why, confidence}], "rejected": [...], "applied": [...]}`.
The bot posts each proposal in `#judger` as a card with approve/reject buttons;
approve runs the same tool with the same args and appends to `applied`. Until the
bot does that, Mode 2 is the approval path.

## Standing rules

- Never call `session_end`, `ledger_add`, `advance_front`, `npc_set`,
  `log_ruling`, `propose_rule` or `archive_scene` in Mode 1. Mode 2 is the only
  writer, and only with ids Isaac gave.
- Every proposal rests on a verbatim quote from the scene. No quote, no proposal.
- Rules are cited by id and quoted; conflicts are recorded, never resolved.
- A "name with no page" in the note is a wiki gap for Isaac, not a licence to
  invent a card.
