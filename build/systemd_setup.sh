#!/usr/bin/env bash
# Install the WOTR systemd user units: the four timers (wiki sync hourly, nightly 03:30,
# book 02:00, weekly backup Sunday 03:00) and the long-running services (the job runner
# for n8n, the Discord bot). Was seven Windows scheduled tasks — "WOTR wiki sync",
# "WOTR nightly", "WOTR book", "WOTR weekly backup", "WOTR jobs", "WOTR bot",
# "WOTR MCP public" — each registered from its own script; on Linux they are the files
# in build/systemd/, and this is the one script that puts them in place.
#
#   bash build/systemd_setup.sh            # install (or refresh) and start everything
#   bash build/systemd_setup.sh --status   # the timers and the services; changes nothing
#   bash build/systemd_setup.sh --remove   # stop, disable and delete every installed wotr-* unit
#
# What it does, idempotently:
#   1. copies build/systemd/*.service and *.timer to ~/.config/systemd/user/, noting
#      which copies actually changed
#   2. systemctl --user daemon-reload
#   3. enable --now the four timers, wotr-jobs.service and wotr-bot.service.
#      NOT wotr-mcp-public.service: build/mcp_public_setup.sh enables that one after it
#      has written the shared secret (build/.mcp_token) and opened the funnel, so the
#      public server never comes up without a token. The file is copied here with the
#      rest (that script copies it too if it is missing, so either order works).
#      NOT wotr-comfy.service either: build/comfy_setup.sh enables it once the clone,
#      the venv and the ROCm torch it runs on exist; copied here, enabled there.
#      Then restarts what changed and is running: `enable --now` on a running service
#      is a no-op start, so without this an edited wotr-jobs/wotr-bot/wotr-mcp-public
#      would keep the old process on the old ExecStart until restarted by hand. A
#      changed timer is restarted too (its schedule is re-read). The oneshot services
#      are never restarted — that would run them. And wotr-jobs is left alone while a
#      job it started is still running (the jobs are children in its cgroup; a restart
#      kills them, a chapter mid-write): the script says so and leaves the restart to you.
#   4. loginctl enable-linger, so the user manager — and with it the timers, the job
#      runner and the bot — starts at boot and outlives a logout, not only a desktop
#      session (the old tasks ran "at logon"; these run whenever the machine is up)
#   5. prints the timers and one line per wotr-* unit, inactive ones included
#
# Re-run after editing anything under build/systemd/: the copies are what systemd
# reads, and step 3 applies the change to whatever is running. --remove works from the
# installed copies, not build/systemd/, so a unit renamed or dropped from the repo is
# still found and disabled. Never needs sudo; everything is in the user's own manager.
#
# Logs: journalctl --user -u wotr-<name> (the unit's view: start, exit code, anything
# on stdout/stderr) plus each script's own file — build/sync.log, build/nightly.log,
# build/book_dispatch.log, build/backup.log, build/.jobs_server.log, bot/.bot.log.

set -uo pipefail
. "$(dirname "$0")/env.sh"

src="$WOTR_REPO/build/systemd"
dst="$HOME/.config/systemd/user"
# what --now enables; wotr-mcp-public.service is deliberately not here (see above)
enable=(wotr-sync.timer wotr-nightly.timer wotr-book.timer wotr-backup.timer
        wotr-jobs.service wotr-bot.service)
# what a changed file restarts (see the header); never a oneshot service
restartable=(wotr-sync.timer wotr-nightly.timer wotr-book.timer wotr-backup.timer
             wotr-jobs.service wotr-bot.service wotr-mcp-public.service wotr-comfy.service)

# every unit build/systemd/ ships, by name
units=()
for f in "$src"/*.service "$src"/*.timer; do
    [ -e "$f" ] && units+=("$(basename "$f")")
done

listing() {
    echo
    echo "== timers =="
    systemctl --user list-timers --all 'wotr-*' || true
    echo
    echo "== units: active / enabled (systemctl --user status wotr-<name> for the detail) =="
    # one line per installed file, by name — never `status 'wotr-*'` or `list-units`
    # with a glob: those see only the units the manager has loaded, and a service that
    # exited (the bot without a token), one never started (the public MCP before its
    # setup) or one just disabled is not loaded, so it would be missing from the very
    # list that says what stands. is-active and is-enabled answer for any unit file.
    local f u n=0
    for f in "$dst"/wotr-*.service "$dst"/wotr-*.timer; do
        [ -e "$f" ] || continue
        u="$(basename "$f")"; n=$((n + 1))
        printf '  %-26s %-10s %s\n' "$u" "$(systemctl --user is-active "$u" 2>/dev/null)" "$(systemctl --user is-enabled "$u" 2>/dev/null)"
    done
    [ "$n" -gt 0 ] || echo "  (no wotr-* unit files under $dst)"
}

# true while wotr-jobs.service has more than its own process in its cgroup — a job it
# started (bash + python or claude) is still running there
jobs_busy() {
    local cg procs
    cg="$(systemctl --user show -p ControlGroup --value wotr-jobs.service 2>/dev/null)"
    procs="/sys/fs/cgroup$cg/cgroup.procs"
    [ -n "$cg" ] && [ -r "$procs" ] || return 1
    [ "$(wc -l < "$procs")" -gt 1 ]
}

reminder() {
    cat <<'TXT'

Two things to remember:
  - If an n8n workflow is activated for the nightly or the book, disable the matching
    timer so nothing runs twice:
        systemctl --user disable --now wotr-nightly.timer
        systemctl --user disable --now wotr-book.timer
    (re-enable with `enable --now` when the workflow is switched off again).
  - Logs: journalctl --user -u wotr-<name> for the unit's view, plus the scripts' own
    files: build/sync.log, build/nightly.log, build/book_dispatch.log, build/backup.log,
    build/.jobs_server.log, build/mcp_public.log, bot/.bot.log.
TXT
}

case "${1:-}" in
    --status)
        listing
        exit 0
        ;;
    --remove)
        # from the installed copies, not build/systemd/: a unit renamed or dropped from
        # the repo is still there and still enabled until this finds it
        installed=()
        for f in "$dst"/wotr-*.service "$dst"/wotr-*.timer; do
            [ -e "$f" ] && installed+=("$(basename "$f")")
        done
        if [ "${#installed[@]}" -eq 0 ]; then echo "no wotr-* unit files under $dst; nothing to remove"; exit 0; fi
        for u in "${installed[@]}"; do
            # a unit that was never enabled just says so; carry on
            systemctl --user disable --now "$u" 2>/dev/null || true
            rm -f "$dst/$u"
        done
        systemctl --user daemon-reload
        systemctl --user reset-failed 'wotr-*' 2>/dev/null || true
        echo "removed ${#installed[@]} unit file(s) from $dst and disabled them"
        echo "(the scripts and their logs are untouched; linger is left as it was)"
        exit 0
        ;;
    '')
        ;;
    *)
        echo "usage: bash build/systemd_setup.sh [--status | --remove]"
        exit 2
        ;;
esac

if [ "${#units[@]}" -eq 0 ]; then echo "no unit files under $src"; exit 1; fi

# 1. the files, noting which copies changed (step 3 restarts those that are running)
mkdir -p "$dst"
changed=()
for u in "${units[@]}"; do
    cmp -s "$src/$u" "$dst/$u" || changed+=("$u")
    cp -f "$src/$u" "$dst/$u"
done
echo "installed ${#units[@]} unit file(s) to $dst (${#changed[@]} changed)"

# 2. let systemd read them
systemctl --user daemon-reload

# 3. enable and start (a timer that is already enabled just gets its schedule refreshed)
for u in "${enable[@]}"; do
    if systemctl --user enable --now "$u"; then
        echo "enabled $u"
    else
        echo "could not enable $u; see: systemctl --user status $u"
    fi
done
echo "not enabled: wotr-mcp-public.service (build/mcp_public_setup.sh does that after writing the secret)"
echo "not enabled: wotr-comfy.service (build/comfy_setup.sh does that once ComfyUI and its venv exist)"

# ... and apply a changed file to what is running. is-active first: try-restart would
# also return 0 for an inactive unit and nothing would have happened. An inactive one
# (the public MCP before its setup, the bot without a token) reads the new file when it
# next starts, so it needs nothing here.
for u in "${changed[@]}"; do
    case " ${restartable[*]} " in *" $u "*) ;; *) continue ;; esac
    systemctl --user is-active --quiet "$u" || continue
    if [ "$u" = wotr-jobs.service ] && jobs_busy; then
        echo "$u changed, but a job it started is still running; restart it yourself when GET /jobs shows nothing running:"
        echo "    systemctl --user restart wotr-jobs"
        continue
    fi
    if systemctl --user restart "$u"; then
        echo "restarted $u (its file changed)"
    else
        echo "could not restart $u; see: systemctl --user status $u"
    fi
done

# 4. linger: without it the user manager, and every unit in it, stops at logout and
#    does not exist until the next desktop login. enable-linger for one's own user
#    usually works unprivileged; on a machine where polkit says no, run it once with
#    sudo (sudo loginctl enable-linger "$USER") and re-run this script.
if loginctl enable-linger "$USER" 2>/dev/null; then
    echo "linger enabled for $USER (units run before a desktop login and after logout)"
else
    echo "loginctl enable-linger $USER failed; it may need polkit approval or sudo:"
    echo "    sudo loginctl enable-linger $USER"
    echo "until then the units run only while $USER has a session"
fi

# 5. what stands
listing
reminder
