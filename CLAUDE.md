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
is ruled, openly, by the Paperclip docket (Doc Kett, reviewed by Rhett Konn and
Gemma Nye) under the precedence ladder in the `wotr-conflict` skill, logged with
`log_ruling` as an **agent ruling** that names its grounds, and applied. Isaac
reads the day's agent rulings in `CONTINUE.md` and may overturn any of them; an
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

## Scope discipline
Read `CONTINUE.md` first: it is the live state, and two sessions often write
this repo at once — commit only your own files. One pack per commit. Stop at
the end of each phase of the job at hand (`BRIEF.md` for a pack extraction,
`ROADMAP.md` otherwise) and report. Do not run ahead into the next phase
because it seems easy.

## Validation gate
`python build/validate.py` must exit 0 before you claim a pack is done. If a
check fails, fix the data, not the checker. If you believe the checker is wrong,
say so and stop.

## The map
`AGENTS.md` is the working map of the repo (layout, commands, the Linux setup,
the MCP, the prose protocol) for every coding agent, this one included. Read it
after this file; it explains, it does not loosen anything above.
