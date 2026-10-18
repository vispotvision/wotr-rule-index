#!/usr/bin/env bash
# bash imports/drafts/card-update/run.sh <card path> <out dir>: one card through Codex
set -uo pipefail
cd "$(dirname "$0")/../../.."
card="$1"; out="$2/$(basename "$card")"
[[ -s "$out" ]] && exit 0
for try in 1 2; do
  bash build/ask_chatgpt.sh "Follow imports/drafts/card-update/BRIEF.md exactly for the card at: $card" > "$out.tmp" 2> "$out.err"
  if [[ $(head -n1 "$out.tmp") == "---" ]] && grep -q "=== ADDITIONS ===" "$out.tmp"; then mv "$out.tmp" "$out"; rm -f "$out.err"; break; fi
  mv "$out.tmp" "$out.bad"
done
echo "done $(basename "$card") rc=$?"
