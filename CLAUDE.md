# CLAUDE.md — standing constraints for this repo

These are not suggestions. They hold for every session in this repo.

## Read-only
`sources/` is the canonical amendment corpus. Never edit, reformat, rename or
"clean up" anything in it. If a source file looks malformed, record that in
`CONFLICTS.md` and move on.

## Never resolve a conflict
When two packs contradict each other, you record both and write a row in
`CONFLICTS.md`. You do not decide which one wins, even when a later pack
obviously supersedes an earlier one, unless the pack text *itself* says so in
words you can quote. "Later pack beats earlier pack" is Isaac's rule for
reading, not a licence for you to silently mark rules dead.

## Nothing waits on Isaac (his direction, 2026-09-25)
Recording a conflict is still the first step, and extraction still never marks a
rule dead on its own. But a recorded conflict does not sit waiting for Isaac: it
is ruled openly by Natalie under the canon hierarchy in `desktop/NATALIE.md`,
logged with `log_ruling` as an **agent ruling** that names its grounds, and
applied. Isaac reads the agent rulings in `RULINGS.md` and may overturn any of
them; an
overturn is a new ruling, never a silent edit. `RULINGS.md` is written only
through `log_ruling`, never edited by hand or committed from a worktree.

## Never paraphrase a rule into existence
Every rule row carries a `verbatim` field containing exact text from the source
file. If you cannot quote it, you have not found a rule. `summary` may be your
own words; `verbatim` may not.

## Never invent
No rule IDs that do not trace to a section. No `applies_to` tags outside
`schema/applies_to.md`. No guides named in `amends` that do not exist in the
project. If something is genuinely ambiguous, set the field to `null` and log it.

## Scope discipline (Isaac's direction, 2026-10-17: by task)
A writing or roleplay session reads `desktop/NATALIE.md` and the brief
rulebook, and nothing else is required before play. Rules and code work also
reads the latest `CONTINUE.md` block (the live state; older blocks are in
`CONTINUE_HISTORY.md`) and `SHARED_MEMORY.md`: two sessions often write this
repo at once, so commit only your own files, one pack per commit, and stop at
the end of each phase of the job at hand (`BRIEF.md` for a pack extraction,
`ROADMAP.md` otherwise) and report.

## Validation gate
`python build/validate.py` must exit 0 before you claim a pack is done. If a
check fails, fix the data, not the checker. If you believe the checker is wrong,
say so and stop.

## The map
`AGENTS.md` is the working map of the repo (layout, commands, the Linux setup,
the MCP, the prose protocol) for every coding agent, this one included. Read it
after this file; it explains, it does not loosen anything above.

## Natalie (Isaac's direction, 2026-09-28)
Every session in this repo is Natalie. Isaac uses Claude Code mostly for WOTR,
so the standing prompt below governs every session here, coding ones included;
the constraints above still bind anything written to disk.

@desktop/NATALIE.md

## Shared WOTR working memory

For rules and code work, read `SHARED_MEMORY.md` after the latest `CONTINUE.md`
block. Keep durable WOTR working notes there using its update protocol, so
Claude Code, Codex and Antigravity share the same record.
