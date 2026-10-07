#!/usr/bin/env bash
# Ask Codex (Isaac's ChatGPT plan) for a second opinion and print its answer.
#
#   bash build/ask_chatgpt.sh "Review scenes/drafts/x.md against R71 and R72; list what breaks."
#   echo "long prompt" | bash build/ask_chatgpt.sh
#
# Read-only all the way down: the sandbox cannot write, and the WOTR server is started
# with --read-only so no saving tool exists, which is what lets its tools run unapproved.
# ChatGPT connectors (Gmail, Notion...) still need approval, so in exec they are refused.
set -euo pipefail
cd "$(dirname "$0")/.."
prompt="${*:-$(cat)}"
# the mise install directly: ~/.local/bin/codex is a mise wrapper that reconciles on every
# call, and systemd units (the MCP servers run this) have neither on PATH
codex=$HOME/.local/share/mise/installs/codex/latest/bin/codex
[[ -x $codex ]] || codex=codex
out=$(mktemp --suffix=.md)
trap 'rm -f "$out" "$out.log"' EXIT
"$codex" exec -s read-only --ephemeral -C "$PWD" \
  -c "mcp_servers.wotr.args=[\"$PWD/build/py.sh\",\"build/mcp_server.py\",\"--read-only\"]" \
  -c 'mcp_servers.wotr.default_tools_approval_mode="approve"' \
  -o "$out" "$prompt" >/dev/null 2>"$out.log" || { tail -20 "$out.log" >&2; exit 1; }
cat "$out"
