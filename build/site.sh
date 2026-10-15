#!/usr/bin/env bash
# Build the public wiki site with Quartz. ./build/site.sh [--serve]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
Q="${QUARTZ_DIR:-$HOME/.cache/wotr-quartz}"
[ -d "$Q" ] || { git clone https://github.com/jackyzha0/quartz.git "$Q" && git -C "$Q" checkout 97a2d05; }
cp "$ROOT/site/quartz.config.yaml" "$Q/quartz.config.yaml"
cp "$ROOT/site/custom.scss" "$Q/quartz/styles/custom.scss"
python3 "$ROOT/build/site_content.py" "$Q/content"
cd "$Q"
[ -d node_modules ] || npm ci
npx quartz plugin install
if [ "${1:-}" = "--serve" ]; then npx quartz build "$@"; exit; fi
npx quartz build "$@"
cp "$ROOT/site/landing.html" public/index.html && cp -r "$ROOT/site/assets" public/
