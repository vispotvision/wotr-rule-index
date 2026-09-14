#!/usr/bin/env bash
# Runs WOTR Bot. Was bot/run.ps1 (the logon task "WOTR bot"), which looped and restarted
# the bot itself every 30 s; on Linux the restart loop is systemd's — wotr-bot.service
# has Restart=on-failure, RestartSec=30 — so this script starts the bot once and gets out
# of the way (exec: the bot is the unit's main process).
#
#   systemctl --user start wotr-bot   # what the unit runs
#   systemctl --user restart wotr-bot # after a code change
#   systemctl --user stop wotr-bot    # FIRST, before running it by hand:
#   bash bot/run.sh [--sync]          # --sync: (re)register the slash commands with the guild
#
# One bot per token: run by hand while wotr-bot.service is up, this would be a second
# bot online on the same token — --sync included, it syncs and then stays connected —
# and every slash command would be answered twice until one of them is killed. So the
# script refuses while the unit is active, unless it is the unit running it — known
# from the process's own cgroup (/proc/self/cgroup ends in /wotr-bot.service under the
# unit; INVOCATION_ID would not do: a desktop launched as a transient unit hands it
# down to every terminal). On Windows this was the same trap, and stopping the task
# first was the unwritten rule; here it is written and enforced.
#
# No token, no start: with DISCORD_TOKEN empty (see ~/.config/wotr/env) one line goes to
# bot/.bot.log and the script exits 0, which on-failure does not restart — the unit ends
# quietly instead of crash-looping until the secret is filled in. The bot's stdout and
# stderr go to bot/.bot.log (gitignored) as before; the unit's own view is
#   journalctl --user -u wotr-bot
# Remove with: systemctl --user disable --now wotr-bot (or build/systemd_setup.sh --remove).

set -uo pipefail
. "$(dirname "$0")/../build/env.sh"

# by hand, with the unit up: refuse (see the header). Exit 1 and nothing in the log —
# this is a message for the person at the terminal, not a bot event.
if ! grep -qs '/wotr-bot\.service$' /proc/self/cgroup && command -v systemctl >/dev/null 2>&1 \
   && systemctl --user is-active --quiet wotr-bot.service; then
    echo "wotr-bot.service is running; stop it first (systemctl --user stop wotr-bot), or two bots on one token answer every command twice" >&2
    exit 1
fi

log="$WOTR_REPO/bot/.bot.log"
if [ -z "${DISCORD_TOKEN:-}" ]; then
    printf '%s DISCORD_TOKEN not set (see ~/.config/wotr/env); not starting\n' "$(date +%FT%T)" >> "$log"
    exit 0
fi
printf '%s starting\n' "$(date +%FT%T)" >> "$log"
exec "$WOTR_PYTHON" bot/main.py "$@" >> "$log" 2>&1
