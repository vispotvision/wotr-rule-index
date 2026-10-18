#!/usr/bin/env bash
# bash imports/drafts/card-update/run.sh <card path> <out dir>: one card through Codex
set -uo pipefail
cd "$(dirname "$0")/../../.."
card="$1"; out="$2/$(basename "$card")"
[[ -s "$out" ]] && exit 0
bash build/ask_chatgpt.sh "Follow imports/drafts/card-update/BRIEF.md exactly for the card at: $card" > "$out.tmp" 2> "$out.err" && mv "$out.tmp" "$out" && rm -f "$out.err"
echo "done $(basename "$card") rc=$?"
