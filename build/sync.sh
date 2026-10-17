#!/usr/bin/env bash
# Autosave for the wiki: commits and pushes what changed in wiki/ (the Obsidian
# vault, the source since 2026-10-15; Notion is retired and frozen), copies the
# rendered Fronts, Ledger and NPC roster into the wiki's Running Pieces (never State of
# Play, retired 2026-10-17), refreshes the search index. The push rebuilds the public site.
# The Drive step is gone (R79-12). It alerts only on a push failure: that is the one line
# with "push failed" in build/sync.log and the one non-zero exit; every other step logs
# "error" and carries on (build/nightly.py counts the "push failed" lines).
#
#   bash build/sync.sh
#
# Safe to run any time; if nothing changed, nothing is committed. Needs git
# credentials already set up (gh auth login did that).
#
# Runs every 15 minutes as the systemd user timer wotr-sync.timer (the unit files are in
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

# scenes/ into the vault as private pages (scenes/ stays the source)
run_tool scenes_to_wiki.py
log_tail 1 "  "

# the vault's page list, by section and shelf
run_tool wiki_index.py
log_tail 1 "  "

# the rendered table (build/table.py render) into the vault's Running Pieces
rp="wiki/The Table — Running Pieces"
for pair in "FRONTS:Fronts, as clocks" "LEDGER:The Ledger, structured" "NPCS:NPC roster"; do
    src="table/${pair%%:*}.md"; dst="$rp/${pair#*:}.md"
    { [ -f "$src" ] && ! cmp -s "$src" "$dst" && cp "$src" "$dst"; } || true
done

# semantic index over wiki/ and scenes/ for the MCP's wiki and scene_recall
# (build/index/, gitignored; only chunks whose text changed get re-embedded)
wotr_log "embed start"
# The index is a convenience; a failure here must never stop the publish, commit and push
# below.
run_tool embed_index.py
if [ "$code" -ne 0 ]; then
    wotr_log "embed error (exit $code) with python at $WOTR_PYTHON"
    log_tail 6 "    "
else
    log_tail 1 "  "
fi

# the Obsidian view (vault/, gitignored): the mirror with [[wikilinks]] injected
run_tool vault_export.py
log_tail 1 "  "
if [ "$code" -ne 0 ]; then wotr_log "vault error (exit $code)"; fi


# make sure we are not committing on top of a stale checkout. Git writes warnings to
# stderr (worktree prune failures and the like); only exit codes are judged from here on.
# --autostash: the export has just dirtied wiki/, and a plain `pull --rebase` refuses to
# run over unstaged changes (exit 128, nothing fetched), so without it the push was
# rejected as non-fast-forward every time origin had moved. The dirty files are stashed,
# the rebase runs, and they come back; nightly.sh and book_dispatch.sh pull the same way.
set +e
git pull -q --rebase --autostash origin master >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "pull --rebase error (exit $code); committing on the local branch anyway"; fi

# When a stashed change collides with a commit that came down, git leaves the file with
# conflict markers and still exits 0 (the stash entry keeps the original). Nothing is
# committed over those: the export skips pages Notion has not touched since, so the
# markers would go up to origin and stay. A rebase stopped on a real conflict lands here too.
unmerged="$(git diff --name-only --diff-filter=U 2>/dev/null)"
if [ -n "$unmerged" ]; then
    wotr_log "push failed: conflict markers in $(printf '%s\n' "$unmerged" | wc -l) file(s) after the pull; nothing committed, resolve by hand: $(printf '%s\n' "$unmerged" | head -n 1)"
    exit 1
fi

# what the sync owns; nothing outside this list is ever staged or committed here, so
# whatever another session has left staged (two often write this repo at once) stays
# out of the sync's commit and $n stays honest
paths=(wiki table scenes/CAST.md scenes/TIMELINE.md)
changes="$(git status --porcelain -- "${paths[@]}")"
if [ -z "$changes" ]; then
    # a quiet run still carries up a commit whose push failed earlier: the last run's, or
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
git commit -q -m "Wiki: $n file(s) edited" -m "Autosave of the Obsidian vault via build/sync.sh." -- "${paths[@]}" >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "commit error (exit $code)"; fi
git push -q origin master >/dev/null 2>&1; code=$?
if [ "$code" -ne 0 ]; then wotr_log "push failed"; exit 1; fi
wotr_log "pushed $n file(s)"
