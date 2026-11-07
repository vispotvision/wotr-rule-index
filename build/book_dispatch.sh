#!/usr/bin/env bash
# The book dispatcher: one chapter a night, while Isaac sleeps.
#
# wotr-mcp book-next says what the book needs (write the next chapter, or stop because a
# gate chapter is written and undecided). If a chapter is due, Claude Code runs headless
# on the subscription (build/book_dispatch_prompt.md) and invokes the book-chapter
# workflow, which does the real work: brief -> draft -> a deterministic check and six critics -> bounded
# revise -> gate digest, all under book/<slug>/ch<NN>/. Then this script commits what
# landed — and, before it decides anything, whatever an earlier run left under book/
# uncommitted (a run killed at the limit, a commit the sync's index.lock refused), so a
# chapter that landed is never stranded in the working tree. Isaac approves or rejects
# at breakfast; the nightly digest (03:30) shows him where the book stands.
#
# One dispatcher at a time: a flock on build/.book.lock (gitignored), so a run started
# by hand never overlaps the 02:00 timer's.
#
# Runs as the systemd user unit wotr-book.service, fired by wotr-book.timer (daily
# 02:00). The unit files live in build/systemd/; build/systemd_setup.sh installs them
# under ~/.config/systemd/user/.
#   bash build/book_dispatch.sh --slug <name>        # by hand, from anywhere
#   systemctl --user start wotr-book.service         # the same, under systemd
#   journalctl --user -u wotr-book.service           # what systemd saw; build/book_dispatch.log has the rest
# Remove with: systemctl --user disable --now wotr-book.timer
# (was the scheduled task "WOTR book", build/book_dispatch.ps1, with a 5 h ExecutionTimeLimit)
#
# Off switch: WOTR_BOOK_OFF=1 (in ~/.config/wotr/env, or the environment); empty, 0,
# no and false all mean on. One chapter per run, always.
#   --slug <name>   the book under book/ (required: there is no default book since 2026-11-07)
#   --dry-run       decide and report; never call Claude

set -uo pipefail   # no -e: the original carried on past every failure and logged it
. "$(dirname "$0")/env.sh"   # cd to the repo; ~/.config/wotr/env; WOTR_PYTHON, WOTR_CLAUDE, wotr_log
WOTR_LOG=build/book_dispatch.log

slug=""
dry_run=""
while [ $# -gt 0 ]; do
    case "$1" in
        --slug) slug="${2:?--slug needs a name}"; shift 2 ;;
        --slug=*) slug="${1#--slug=}"; shift ;;
        --dry-run) dry_run=1; shift ;;
        -h|--help) echo "usage: bash build/book_dispatch.sh [--slug <name>] [--dry-run]"; exit 0 ;;
        *) echo "book_dispatch.sh: unknown option '$1' (--slug <name>, --dry-run)" >&2; exit 2 ;;
    esac
done

# one dispatch at a time (the fd stays open, and the lock held, until the script exits;
# the claude call below closes it for its children, so nothing claude starts can keep it)
exec 9>"$WOTR_REPO/build/.book.lock"
if ! flock -n 9; then wotr_log "another dispatch is running; skipped"; exit 0; fi

case "${WOTR_BOOK_OFF:-}" in
    ''|0|no|false) ;;
    *) wotr_log "WOTR_BOOK_OFF is set; nothing dispatched"; exit 0 ;;
esac

if [ -z "$slug" ]; then wotr_log "book_dispatch.sh: --slug <name> is required (no default book)"; echo "book_dispatch.sh: --slug <name> is required" >&2; exit 2; fi
wotr_log "dispatch start ($slug)"
git pull -q --rebase --autostash origin master >/dev/null 2>&1   # a tracked log churns; autostash keeps the rebase from refusing
code=$?
if [ "$code" -ne 0 ]; then wotr_log "pull --rebase failed (exit $code); running on the local branch"; fi

# commit whatever is under book/ and push. Called before the early exits as well as
# after tonight's chapter, so a chapter that landed but was never committed (the 5 h
# limit, the sync holding .git/index.lock at the wrong second, a refused commit) is
# picked up the next night instead of sitting in the working tree. Returns 1 when
# nothing was committed, and says why.
commit_book() {   # $1: the commit subject
    local n code
    if [ -z "$(git status --porcelain -- book)" ]; then return 1; fi
    git add -- book >/dev/null 2>&1; code=$?
    if [ "$code" -ne 0 ]; then wotr_log "git add failed (exit $code); nothing committed"; return 1; fi
    n="$(git diff --cached --name-only -- book | wc -l)"   # files, not porcelain lines: a new ch<NN>/ is one line there
    git commit -q -m "$1" -m "Automated: build/book_dispatch.sh. Nothing archived; the gate is Isaac's." >/dev/null 2>&1; code=$?
    if [ "$code" -ne 0 ]; then wotr_log "commit failed (exit $code); nothing pushed"; return 1; fi
    if ! git push -q origin master >/dev/null 2>&1; then wotr_log "push failed (the sync will carry it up)"; fi
    wotr_log "committed $n file(s) under book/"
    return 0
}

# what the book needs: action, chapter and why, one to a line.
next="$(rust/target/release/wotr-mcp book-next --slug "$slug" --lines 2>&1)" || { wotr_log "book-next said: $next"; exit 1; }
{ IFS= read -r action; IFS= read -r chapter; IFS= read -r why; } <<< "$next"
wotr_log "  next: $action — $why"

# what an earlier run left under book/ goes up first, on its own — whatever tonight's
# action is — so tonight's chapter (if there is one) gets its own commit. A dry run
# only says so.
if [ -n "$dry_run" ]; then
    left="$(git status --porcelain -- book | wc -l)"
    if [ "$left" -gt 0 ]; then wotr_log "  $left path(s) under book/ uncommitted; a real run commits them first"; fi
elif [ -n "$(git status --porcelain -- book)" ]; then
    wotr_log "  uncommitted work under book/ from an earlier run"
    commit_book "Book $slug: what an earlier run left under book/"
fi

case "$action" in
    write|rewrite) ;;
    *) wotr_log "nothing to write tonight"; exit 0 ;;
esac
if [ -n "$dry_run" ]; then wotr_log "dry run: would write chapter $chapter"; exit 0; fi
# every agent this run spawns loads CLAUDE.md and NATALIE.md from disk: an uncommitted change to
# either rewrites the law of the chapter (2026-11-07, the working CLAUDE.md was found replaced)
if [ -n "$(git status --porcelain -- CLAUDE.md desktop/NATALIE.md)" ]; then
    wotr_log "  CLAUDE.md or desktop/NATALIE.md has uncommitted changes; restore or commit them first"; exit 1
fi

if [ ! -x "$WOTR_CLAUDE" ]; then wotr_log "claude CLI not found at $WOTR_CLAUDE"; exit 1; fi

wotr_log "  chapter $chapter: claude start (this takes an hour or more)"
t0=$(date +%s)
# called directly, never through a background job: the job subsystem on the old machine
# hung after the child had exited (2026-09-13). `timeout 5h` is the timeout now — it
# mirrors the 5 h ExecutionTimeLimit the Windows task had; if it fires mid-chapter,
# claude and everything it started are killed, and this run (and the next night's)
# commits whatever landed and goes on.
# The prompt goes in on stdin, never as an argument: the old shell stripped the quotes
# out of a native exe's arguments before claude ever saw them, and the script inside
# the prompt stopped parsing. The contract stayed.
# No MCP servers: the book-chapter workflow reaches the read-only tools through
# wotr-mcp tool on the command line, and the repo's .mcp.json would otherwise
# start the wotr server (45 tools, unapproved) on every run.
res="$(timeout 5h "$WOTR_CLAUDE" -p --max-turns 120 --permission-mode acceptEdits \
    --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
    --allowedTools "Workflow" "Read" "Write" "Edit" "Glob" "Grep" "TaskOutput" "Bash(rust/target/release/wotr-mcp tool:*)" "Bash(rust/target/release/wotr-mcp book-next:*)" "Bash(rust/target/release/wotr-mcp book-memory:*)" \
    < <(printf 'Slug: %s. Pass --slug %s to every book-next and book-memory call.\n\n' "$slug" "$slug"; cat build/book_dispatch_prompt.md) 2>&1 9>&-)"
code=$?
mins=$(( ($(date +%s) - t0) / 60 ))
if [ "$code" -eq 124 ]; then wotr_log "  claude: killed at the 5 h limit"; fi
tail="$(printf '%s\n' "$res" | tail -n 3 | paste -sd ' ' -)"
wotr_log "  claude done in $mins min: ${tail:0:400}"

# refresh GATES.md from whatever is on disk now, then commit the chapter
while IFS= read -r ln; do wotr_log "  $ln"; done < <(rust/target/release/wotr-mcp book-next --slug "$slug" 2>&1)
if [ -z "$(git status --porcelain -- book)" ]; then wotr_log "nothing new under book/; done"; exit 0; fi
commit_book "Book $slug: chapter $chapter drafted overnight"
