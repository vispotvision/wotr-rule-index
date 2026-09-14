#!/usr/bin/env bash
# Register WOTR MCP with Claude Desktop.
#
# Claude Desktop rewrites claude_desktop_config.json from memory whenever it
# starts, so the entry has to be added while the app is closed. This script
# refuses to run while the app is up, patches the config, and leaves starting
# the app to you. (The Windows version quit and relaunched Claude itself; on
# Linux, quit it, run this, open it again from the launcher.)
#
#   bash build/install_mcp.sh            # with Claude Desktop closed
#   bash build/install_mcp.sh --dry-run  # print the JSON it would write; changes nothing
#   bash build/install_mcp.sh --force    # patch even while the app runs (it may
#                                        # write the file back without the entry on quit)
#
# The config is ~/.config/Claude/claude_desktop_config.json (was
# %APPDATA%\Claude\..., virtualised into the Store package's LocalCache). The
# previous file is kept next to it as claude_desktop_config.json.bak. The entry
# runs the venv's python on build/mcp_server.py over stdio; the server reads
# ~/.config/wotr/env itself (common.load_env), so nothing else is needed here.

set -eu -o pipefail
. "$(dirname "$0")/env.sh"

mode=write
force=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) mode=dry-run ;;
        --force) force=1 ;;
        -h|--help) sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "unknown option: $arg (use --dry-run or --force)" >&2; exit 2 ;;
    esac
done

cfg="${XDG_CONFIG_HOME:-$HOME/.config}/Claude/claude_desktop_config.json"
if [ ! -f "$cfg" ]; then
    echo "claude_desktop_config.json not found at $cfg" >&2
    echo "  start Claude Desktop once so it writes the file, quit it, then re-run" >&2
    exit 1
fi
echo "config: $cfg"
server="$WOTR_REPO/build/mcp_server.py"

# 1. is Claude Desktop running? The Arch package is /usr/lib/claude-desktop/claude-desktop,
# process name claude-desktop (pgrep -x: exact name, so the Claude Code CLI - process
# name "claude" - and mise's shims never match). The other names cover other packagings:
# the kernel keeps 15 characters of a process name, so the AUR claude-desktop-bin shows
# up as "claude-desktop-" (pgrep -x on the full name can never match, and warns so).
running=""
for name in claude-desktop claude-desktop- Claude; do
    if pgrep -x "$name" >/dev/null 2>&1; then running="$name"; break; fi
done
if [ -n "$running" ]; then
    if [ "$mode" = dry-run ]; then
        echo "Claude Desktop is running (process '$running'); a real run would refuse without --force"
    elif [ "$force" = 1 ]; then
        echo "Claude Desktop is running (process '$running'); patching anyway because of --force."
        echo "  It may write the file back without the entry when it quits; check after a restart."
    else
        echo "Claude Desktop is running (process '$running'). Quit it first, then re-run." >&2
        echo "  The app rewrites its config from memory on start, so a change made while it" >&2
        echo "  runs is lost. Use --force to patch anyway, --dry-run to see the result." >&2
        exit 1
    fi
fi

# 2. add the server entry (a JSON edit that keeps every other key as it is)
if [ "$mode" = write ]; then
    cp -p "$cfg" "$cfg.bak"
    echo "backup: $cfg.bak"
fi
"$WOTR_PYTHON" - "$cfg" "$WOTR_PYTHON" "$server" "$mode" <<'PY'
import json
import sys

cfg, python, server, mode = sys.argv[1:5]
with open(cfg, encoding="utf-8-sig") as f:  # tolerate a BOM if one ever crept in
    data = json.load(f)
if not isinstance(data, dict):
    sys.exit(f"{cfg}: expected a JSON object at the top level")
servers = data.get("mcpServers")
if not isinstance(servers, dict):
    servers = data["mcpServers"] = {}
servers["WOTR MCP"] = {"command": python, "args": [server]}
text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
if mode == "dry-run":
    sys.stdout.write(text)
else:
    with open(cfg, "w", encoding="utf-8", newline="\n") as f:  # UTF-8, no BOM, LF
        f.write(text)
PY

if [ "$mode" = dry-run ]; then
    echo "(dry run: nothing written)"
    exit 0
fi
echo "Added 'WOTR MCP' -> $WOTR_PYTHON $server"

# 3. the app has to start fresh to read it; that is your move, not this script's
echo "Config written. Start Claude Desktop from the launcher; WOTR MCP appears in the tools menu inside a chat."
