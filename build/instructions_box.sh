#!/usr/bin/env bash
# Build the text for the Claude Desktop project's Instructions box: everything
# below the first rule in desktop/PROJECT_INSTRUCTIONS.md, then everything below
# the first rule in desktop/NATALIE.md. Writes it next to the repo and copies it
# to the clipboard when wl-copy or xclip is present.
set -euo pipefail
cd "$(dirname "$0")/.."
out="${1:-$HOME/wotr-instructions-box.md}"
below_rule() { awk 'f{print} /^---$/ && !f{f=1}' "$1"; }
{ below_rule desktop/PROJECT_INSTRUCTIONS.md; echo; below_rule desktop/NATALIE.md; } > "$out"
if command -v wl-copy >/dev/null; then wl-copy < "$out"; echo "copied to the clipboard (wl-copy)";
elif command -v xclip >/dev/null; then xclip -selection clipboard < "$out"; echo "copied to the clipboard (xclip)"; fi
printf '%s: %s bytes, %s words\n' "$out" "$(wc -c < "$out")" "$(wc -w < "$out")"
