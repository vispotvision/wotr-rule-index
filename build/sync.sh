#!/usr/bin/env bash
# Two-way mirror: Notion wiki -> wiki/, then repo scenes and index outputs
# -> Notion, then commit and push whatever changed.
#
#   bash build/sync.sh
#
# This is what turns "Natalie archived a scene in Notion" into "the scene is
# in the repo": her session-end protocol files the scene under the wiki's
# Scene Archive section; this script mirrors it to wiki/The Scene Archive/
# and commits it. Safe to run any time; if nothing changed, nothing is
# committed. Needs NOTION_TOKEN in ~/.config/wotr/env (or the environment)
# and git credentials already set up (gh auth login did that).
#
# Runs hourly as the systemd user timer wotr-sync.timer (the unit files are in
# build/systemd/; build/systemd_setup.sh installs them):
#
#   systemctl --user enable --now wotr-sync.timer
#
# Remove with: systemctl --user disable --now wotr-sync.timer
#
# Two runs never overlap: the script holds build/.sync.lock for its whole run,
# and a second one (the timer firing during a manual sync, or the other way
# round) logs "another sync is running; skipped" and exits 0.
#
# (was build/sync.ps1 and the scheduled task "WOTR wiki sync")

set -euo pipefail
. "$(dirname "$0")/env.sh"

WOTR_LOG="$WOTR_REPO/build/sync.log"

# one sync at a time (the fd stays open, and the lock held, until the script exits)
exec 9>"$WOTR_REPO/build/.sync.lock"
if ! flock -n 9; then wotr_log "another sync is running; skipped"; exit 0; fi

if [ -z "${NOTION_TOKEN:-}" ]; then wotr_log "NOTION_TOKEN not set; aborting"; exit 1; fi

# One interpreter for every step: the venv env.sh picked (and put first on PATH, so a
# bare `python` in anything a tool starts is the same one). The Windows run once
# resolved to a package-less interpreter and failed silently; hence the line.
wotr_log "python: $WOTR_PYTHON"

# run_tool <tool.py> [args...]: runs build/<tool.py> with both streams captured in $out
# and its exit code in $code (never fatal by itself; each step judges $code)
run_tool() {
    local tool="$1"; shift
    out="$("$WOTR_PYTHON" "build/$tool" "$@" 2>&1)" && code=0 || code=$?
}

# log_tail <n> <indent>: the last <n> lines of $out into the log, each prefixed
log_tail() {
    local n="$1" indent="$2" line
    [ -n "$out" ] || return 0
    while IFS= read -r line; do wotr_log "${indent}${line}"; done < <(printf '%s\n' "$out" | tail -n "$n")
}

wotr_log "export start"
run_tool notion_export.py
log_tail 3 "  "
if [ "$code" -ne 0 ]; then wotr_log "export failed (exit $code)"; exit "$code"; fi

# semantic index over wiki/ and scenes/ for the MCP's wiki and scene_recall
# (build/index/, gitignored; only chunks whose text changed get re-embedded)
wotr_log "embed start"
# The index is a convenience; a failure here must never stop the publish, commit and push
# below.
run_tool embed_index.py
if [ "$code" -ne 0 ]; then
    wotr_log "embed failed (exit $code) with python at $WOTR_PYTHON"
    log_tail 6 "    "
else
    log_tail 1 "  "
fi

# the Obsidian view (vault/, gitignored): the mirror with [[wikilinks]] injected
run_tool vault_export.py
log_tail 1 "  "
if [ "$code" -ne 0 ]; then wotr_log "vault failed (exit $code)"; fi

# the other direction: index outputs and scenes that changed in the repo go
# up to Notion (build/notion_publish.py is idempotent; unchanged files are skipped)
wotr_log "publish start"
run_tool notion_publish.py
log_tail 2 "  "
if [ "$code" -ne 0 ]; then wotr_log "publish failed (exit $code)"; fi

# Word documents for the Google Drive folder, when Drive is mounted (WOTR_DRIVE in
# ~/.config/wotr/env names the mount; was G:\My Drive under Drive for Desktop)
if [ -n "${WOTR_DRIVE:-}" ] && [ -d "$WOTR_DRIVE" ]; then
    docs="$WOTR_DRIVE/War of the Realms — Documents"
    wotr_log "docs start"
    run_tool docs_export.py --out "$docs" --private-out "$WOTR_DRIVE/War of the Realms — Private"
    log_tail 1 "  "
    run_tool arcs_export.py --out "$docs/Arcs"
    log_tail 1 "  "
else
    wotr_log "WOTR_DRIVE not set or not mounted; docs skipped"
fi

# make sure we are not committing on top of a stale checkout. Git writes warnings to
# stderr (worktree prune failures and the like); only exit codes are judged from here on.
# --autostash: the export has just dirtied wiki/, and a plain `pull --rebase` refuses to
# run over unstaged changes (exit 128, nothing fetched), so without it the push was
# rejected as non-fast-forward every hour origin had moved. The dirty files are stashed,
# the rebase runs, and they come back; nightly.sh and book_dispatch.sh pull the same way.
set +e
git pull -q --rebase --autostash origin master >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "pull --rebase failed (exit $code); committing on the local branch anyway"; fi

# When a stashed change collides with a commit that came down, git leaves the file with
# conflict markers and still exits 0 (the stash entry keeps the original). Nothing is
# committed over those: the export skips pages Notion has not touched since, so the
# markers would go up to origin and stay. A rebase stopped on a real conflict lands here too.
unmerged="$(git diff --name-only --diff-filter=U 2>/dev/null)"
if [ -n "$unmerged" ]; then
    wotr_log "sync failed: conflict markers in $(printf '%s\n' "$unmerged" | wc -l) file(s) after the pull; nothing committed, resolve by hand: $(printf '%s\n' "$unmerged" | head -n 1)"
    exit 1
fi

# what the sync owns; nothing outside this list is ever staged or committed here, so
# whatever another session has left staged (two often write this repo at once) stays
# out of the sync's commit and $n stays honest
paths=(wiki table scenes/CAST.md scenes/TIMELINE.md build/.notion_publish.json)
changes="$(git status --porcelain -- "${paths[@]}")"
if [ -z "$changes" ]; then
    # a quiet hour still carries up a commit whose push failed earlier: last hour's, or
    # the nightly's ("push failed (the sync will carry it up)")
    ahead="$(git rev-list --count origin/master..master 2>/dev/null)"
    if [ "${ahead:-0}" != 0 ]; then
        git push -q origin master >/dev/null 2>&1; code=$?
        if [ "$code" -ne 0 ]; then wotr_log "push failed ($ahead earlier commit(s) still local)"; exit 1; fi
        wotr_log "pushed $ahead earlier commit(s)"
    fi
    wotr_log "no wiki changes"; exit 0
fi

n="$(printf '%s\n' "$changes" | wc -l)"
git add -- "${paths[@]}"
git commit -q -m "Wiki sync: $n file(s) changed in Notion" -m "Automated mirror of the War of the Realms wiki via build/sync.sh." -- "${paths[@]}" >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "commit failed (exit $code)"; fi
git push -q origin master >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "push failed"; exit 1; fi
wotr_log "pushed $n file(s)"
