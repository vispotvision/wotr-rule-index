#!/usr/bin/env bash
# Build the public wiki site with Quartz. ./build/site.sh [--serve]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
Q="${QUARTZ_DIR:-$HOME/.cache/wotr-quartz}"
[ -d "$Q" ] || { git clone https://github.com/jackyzha0/quartz.git "$Q" && git -C "$Q" checkout 97a2d05; }
cp "$ROOT/site/quartz.config.yaml" "$Q/quartz.config.yaml"
python3 "$ROOT/build/site_content.py" "$Q/content"
cd "$Q"
[ -d node_modules ] || npm ci
npx quartz plugin install
npx quartz build "$@"
