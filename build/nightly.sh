#!/usr/bin/env bash
# The nightly checks: build/nightly.py (validate, resolve, the audits, the Büri sweep,
# the diff against last night -> reports/nightly.md), then Claude Code on the
# subscription writes the "Overnight" note at the top (build/nightly_prompt.md; the
# only file it may edit is reports/nightly.md), then the digest and the audit
# reports are committed and pushed. session_start shows the note next morning.
#
# Runs as the systemd user unit wotr-nightly.service, fired by wotr-nightly.timer
# (daily 03:30). The unit files live in build/systemd/; build/systemd_setup.sh
# installs them under ~/.config/systemd/user/.
#   bash build/nightly.sh                            # by hand, from anywhere
#   systemctl --user start wotr-nightly.service      # the same, under systemd
#   journalctl --user -u wotr-nightly.service        # what systemd saw; build/nightly.log has the rest
# Remove with: systemctl --user disable --now wotr-nightly.timer
# (was the scheduled task "WOTR nightly", build/nightly.ps1, with a 2 h ExecutionTimeLimit)
#
# Set WOTR_NIGHTLY_NO_CLAUDE=1 (in ~/.config/wotr/env, or the environment) to run the
# numbers only; empty, 0, no and false all mean the note is written.

set -uo pipefail   # no -e: the original carried on past every failure and logged it
. "$(dirname "$0")/env.sh"   # cd to the repo; ~/.config/wotr/env; WOTR_PYTHON, WOTR_CLAUDE, wotr_log
WOTR_LOG=build/nightly.log

wotr_log "nightly start"
git pull -q --rebase --autostash origin master >/dev/null 2>&1   # a tracked log churns; autostash keeps the rebase from refusing
code=$?
if [ "$code" -ne 0 ]; then wotr_log "pull --rebase failed (exit $code); running on the local branch"; fi
# the autostash can leave a file unmerged (conflict markers in the tree, pull exit 0);
# git then refuses every commit, so say so here rather than let "committed" lie below
unmerged="$(git diff --name-only --diff-filter=U 2>/dev/null | paste -sd ' ' -)"
if [ -n "$unmerged" ]; then wotr_log "unmerged after the pull (the commit will be refused): $unmerged"; fi

out="$("$WOTR_PYTHON" build/nightly.py 2>&1)"
code=$?
if [ -n "$out" ]; then
    while IFS= read -r ln; do wotr_log "  $ln"; done < <(printf '%s\n' "$out" | tail -n 2)
fi
if [ ! -f reports/nightly.md ]; then wotr_log "no digest written (exit $code); stopping"; exit 1; fi

# the Overnight note: Claude Code, headless, on the subscription; tools locked to reading,
# the read-only CLI, and editing the digest itself. WOTR_NIGHTLY_NO_CLAUDE=0 (or no,
# false, empty) is not the off switch; anything else is.
case "${WOTR_NIGHTLY_NO_CLAUDE:-}" in ''|0|no|false) no_claude="" ;; *) no_claude=1 ;; esac
if [ -z "$no_claude" ] && [ -x "$WOTR_CLAUDE" ]; then
    wotr_log "claude start"
    # called directly, never through a background job: the job subsystem on the old
    # machine hung after the child had exited (2026-09-13: the run sat Running for 20
    # minutes with no child processes). `timeout 2h` is the timeout now — it mirrors the
    # 2 h ExecutionTimeLimit the Windows task had; if it fires, claude and everything it
    # started are killed, the note stays unwritten, and the numbers below still commit.
    # The prompt goes in on stdin, never as an argument (the old shell stripped the
    # quotes out of a native exe's arguments, and the contract stayed).
    # The "python" inside the Bash tool string is the venv's: env.sh put its bin/ first
    # on PATH, so the headless claude's `python build/book_tools.py` is $WOTR_PYTHON.
    # No MCP servers: the note needs only the three tools above, and the repo's .mcp.json
    # would otherwise start the wotr server (45 tools, unapproved) on every run.
    res="$(timeout 2h "$WOTR_CLAUDE" -p --max-turns 40 \
        --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
        --allowedTools "Read" "Edit(reports/nightly.md)" "Bash(python build/book_tools.py:*)" \
        < build/nightly_prompt.md 2>&1)"
    code=$?
    if [ "$code" -eq 124 ]; then wotr_log "  claude: killed at the 2 h limit"; fi
    tail="$(printf '%s\n' "$res" | tail -n 1)"
    wotr_log "  claude: ${tail:0:160}"
    if grep -q "Claude's note goes here" reports/nightly.md; then wotr_log "  claude: note not written"; else wotr_log "  claude: note written"; fi
else
    wotr_log "claude step skipped"
fi

# commit the digest and the audit reports; nothing else
paths=(reports/nightly.md reports/prose_pass.md reports/recurrence.md reports/reconcile.md build/.nightly_state.json out)
changes="$(git status --porcelain -- "${paths[@]}")"
if [ -z "$changes" ]; then wotr_log "nothing to commit"; exit 0; fi
# git add refuses the whole list when one pathspec matches nothing (a report an audit
# has not written yet on a fresh machine), so only the paths on disk or in the index go in
add=(); for p in "${paths[@]}"; do if [ -e "$p" ] || git ls-files --error-unmatch -- "$p" >/dev/null 2>&1; then add+=("$p"); fi; done
git add -- "${add[@]}" >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "git add failed (exit $code); nothing committed"; exit 1; fi
git commit -q -m "Nightly $(date '+%Y-%m-%d'): the checks and the overnight note" -m "Automated: build/nightly.sh." >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "commit failed (exit $code); nothing pushed"; exit 1; fi   # a push with nothing new is 0, so judge the commit itself
if ! git push -q origin master >/dev/null 2>&1; then wotr_log "push failed (the sync will carry it up)"; exit 0; fi
wotr_log "committed and pushed"
