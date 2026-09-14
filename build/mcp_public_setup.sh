#!/usr/bin/env bash
# Share the WOTR MCP with friends: the read-only server behind a shared secret,
# published through Tailscale Funnel.
#
#   bash build/mcp_public_setup.sh          # set up (idempotent) and print the URLs
#   bash build/mcp_public_setup.sh --off    # stop sharing: funnel off, unit disabled
#
# What it does, idempotently:
#   1. writes build/.mcp_token (the shared secret) if it does not exist
#   2. the server as the systemd user unit wotr-mcp-public.service (was the
#      scheduled task "WOTR MCP public"): installs build/systemd/wotr-mcp-public.service
#      into ~/.config/systemd/user/ if it is not there yet, enables and starts it
#      (the unit's Restart= replaces the task's RestartCount), then waits for
#      127.0.0.1:8765 to listen. The server logs to build/mcp_public.log.
#   3. tailscale funnel --bg 8765: publishes https://<machine>.<tailnet>.ts.net/
#      -> 127.0.0.1:8765 (Tailscale keeps this across reboots)
#   4. prints the URL to hand out
#
# Needs: Tailscale installed and logged in (tailscale status), and Funnel enabled
# for the tailnet (the first `tailscale funnel` prints a one-click link if not).
# Without Tailscale, steps 1 and 2 still run: the server is up on loopback, the
# script prints the install line and exits 0; run it again once Tailscale is up.
#
# The server exposes only the tools that read the repo (READ_ONLY_TOOLS in
# build/mcp_server.py). Nothing a friend does through it can write to the repo,
# the table, Notion, or git. Rotate the secret by deleting build/.mcp_token and
# re-running this script in the same breath (it writes a new one and restarts the
# unit so the server reads it); friends then need the new URL. Do not leave the gap
# open: the server refuses to start without a token, and the unit's Restart= would
# have it retrying every 30 s after a reboot until this script runs again.
#
# Remove with:
#   bash build/mcp_public_setup.sh --off
# which is: tailscale funnel --https=443 off ; systemctl --user disable --now wotr-mcp-public.service

set -eu -o pipefail
. "$(dirname "$0")/env.sh"

port=8765
unit=wotr-mcp-public.service
token_file="$WOTR_REPO/build/.mcp_token"
log="$WOTR_REPO/build/mcp_public.log"
unit_src="$WOTR_REPO/build/systemd/$unit"
unit_dir="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

# true while the unit's own process listens on 127.0.0.1:$port: ss -p names the pid
# behind each socket (-H drops the header) and MainPID is the python the unit started
# (py.sh execs it). Asking about the port alone would call a stray `mcp_server.py
# --public` left in a terminal a success while the unit fails to bind and retries
# every 30 s.
listening() {
    local pid
    pid="$(systemctl --user show -p MainPID --value "$unit" 2>/dev/null)"
    [ "${pid:-0}" != 0 ] && ss -ltnpH "sport = :$port" 2>/dev/null | grep -q "pid=$pid,"
}
# true while anything at all listens on the port (only for the message when it is not the unit)
port_taken() { ss -ltnH "sport = :$port" 2>/dev/null | grep -q .; }

tailscale_up() { command -v tailscale >/dev/null 2>&1 && tailscale status >/dev/null 2>&1; }

# --off: undo steps 3 and 2 (the secret stays; delete build/.mcp_token yourself to rotate)
if [ "${1:-}" = "--off" ]; then
    if tailscale_up; then
        tailscale funnel --https=443 off || true
        echo "funnel off"
    else
        echo "tailscale not running; nothing to turn off there"
    fi
    systemctl --user disable --now "$unit" || true
    echo "$unit disabled and stopped"
    exit 0
fi

# 1. the shared secret (mode 600; never printed here - step 4 is the one place it is)
new_token=0
if [ ! -s "$token_file" ]; then
    ( umask 077; "$WOTR_PYTHON" -c "import secrets; print(secrets.token_urlsafe(24))" > "$token_file" )
    chmod 600 "$token_file"
    new_token=1
    echo "wrote a new shared secret to build/.mcp_token"
fi
token="$(tr -d '[:space:]' < "$token_file")"
if [ "${#token}" -lt 16 ]; then
    echo "build/.mcp_token is too short to be a secret; delete it and re-run" >&2
    exit 1
fi

# 2. the server as a user unit
if [ ! -f "$unit_dir/$unit" ]; then
    if [ ! -f "$unit_src" ]; then
        echo "$unit_src is missing; run build/systemd_setup.sh first" >&2
        exit 1
    fi
    mkdir -p "$unit_dir"
    cp "$unit_src" "$unit_dir/$unit"
    systemctl --user daemon-reload
    echo "installed $unit into $unit_dir"
fi
# a rotated secret only takes effect when the server rereads the file at start, so a
# server that was already running gets a restart; one that `enable --now` starts a
# moment later reads the new file anyway (restarting that one killed it before it bound)
was_active="$(systemctl --user is-active "$unit" 2>/dev/null || true)"
systemctl --user enable --now "$unit" >/dev/null
if [ "$new_token" = 1 ] && [ "$was_active" = active ]; then
    systemctl --user restart "$unit"
fi
i=0
while ! listening && [ "$i" -lt 40 ]; do
    sleep 0.5
    i=$((i + 1))
done
if listening; then
    echo "server listening on 127.0.0.1:$port (unit $unit, log build/mcp_public.log)"
else
    if port_taken; then
        echo "port $port is held by something other than $unit (a server left running in a terminal?):" >&2
        ss -ltnpH "sport = :$port" >&2
        echo "  stop it and re-run" >&2
    fi
    echo "the server did not come up on port $port; see $log" >&2
    echo "  and: journalctl --user -u $unit -n 20 --no-pager" >&2
    exit 1
fi

# 3. the funnel
if ! tailscale_up; then
    echo ""
    echo "Tailscale is not installed or not running, so nothing is published yet."
    echo "The local unit is running; to share it, install and sign in:"
    echo "  sudo pacman -S tailscale; sudo systemctl enable --now tailscaled; sudo tailscale up"
    echo "then enable Funnel once for the tailnet (the first 'tailscale funnel' prints a link)"
    echo "and run this script again."
    exit 0
fi
# the first run on a tailnet without Funnel fails here and prints the one-click link to enable it
if ! out="$(tailscale funnel --bg "$port" 2>&1)"; then
    printf '%s\n' "$out" >&2
    echo "tailscale funnel failed; enable Funnel for the tailnet (link above, once) and re-run" >&2
    exit 1
fi
dns="$(tailscale status --json | "$WOTR_PYTHON" -c 'import json, sys; print(json.load(sys.stdin)["Self"]["DNSName"].rstrip("."))')"

# 4. the URL. The token is printed here on purpose, as the original did: this
# output is the handoff, and the URL is nothing without it. Nowhere else prints it.
echo ""
echo "Give friends this URL (Claude Desktop / claude.ai -> Settings -> Connectors -> Add custom connector):"
echo "  https://$dns/t/$token/mcp"
echo ""
echo "Or, for Claude Code:"
echo "  claude mcp add --transport http wotr https://$dns/mcp --header \"Authorization: Bearer $token\""
if [ "${WOTR_MCP_PUBLIC_URL:-}" != "https://$dns" ]; then
    echo ""
    echo "note: the audio links narration_status hands out use WOTR_MCP_PUBLIC_URL; set it in"
    echo "  ~/.config/wotr/env to https://$dns (then systemctl --user restart $unit)"
fi
