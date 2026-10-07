#!/usr/bin/env bash
# Ask Claude (Isaac's Claude plan) and print its answer: the mirror of ask_chatgpt.sh,
# so ChatGPT can have Claude check its work the way Claude has ChatGPT check Claude's.
#
#   bash build/ask_claude.sh "Review scenes/drafts/x.md as Natalie; what would you change?"
#
# Read-only: the only tools are Read, Grep, Glob and the WOTR server started with
# --read-only (no saving tool, no ask_* tool, so it cannot call back into itself).
# Runs in the repo, so CLAUDE.md and NATALIE.md load as they do for any session here.
set -euo pipefail
cd "$(dirname "$0")/.."
prompt="${*:-$(cat)}"
claude=$HOME/.local/bin/claude
[[ -x $claude ]] || claude=claude
err=$(mktemp)
trap 'rm -f "$err"' EXIT
mcp=$(printf '{"mcpServers":{"wotr":{"command":"bash","args":["%s/build/py.sh","build/mcp_server.py","--read-only"]}}}' "$PWD")
"$claude" -p "$prompt" --strict-mcp-config --mcp-config "$mcp" \
  --add-dir "$HOME/wotr-drafts" --tools Read Grep Glob --allowedTools Read Grep Glob "mcp__wotr__*" \
  --output-format text 2>"$err" || { tail -20 "$err" >&2; exit 1; }
