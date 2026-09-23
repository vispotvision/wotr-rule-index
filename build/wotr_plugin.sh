#!/usr/bin/env bash
# Package the repo's WOTR skills as a Claude Desktop (Cowork) plugin.
#
# The skills in .claude/skills/ are the single source: Claude Code reads them from
# there, and this script assembles a plugin directory around the same files for
# Desktop, which cannot see a repo folder. Nothing is authored here -- if this
# script ever starts containing skill text, the copy has begun to drift and that
# is the failure this whole arrangement exists to avoid.
#
#   bash build/wotr_plugin.sh            -> ~/wotr-plugin/
#   bash build/wotr_plugin.sh /some/dir  -> /some/dir/
#
# Install: Claude Desktop -> Settings -> Capabilities -> add the built folder.
# Rebuild and re-add after changing any SKILL.md; the plugin holds copies by
# necessity (Desktop needs real files), so it is stale the moment the source moves.
set -euo pipefail
cd "$(dirname "$0")/.."

out="${1:-$HOME/wotr-plugin}"
src=".claude/skills"

[ -d "$src" ] || { echo "no $src here -- run this from the repo" >&2; exit 1; }

rm -rf "$out"
mkdir -p "$out/.claude-plugin" "$out/skills"

cat > "$out/.claude-plugin/plugin.json" <<'JSON'
{
  "name": "wotr",
  "version": "1.0.0",
  "description": "War of the Realms: operating procedures for the rule index, the scene archive and the character cards. Built from .claude/skills in vispotvision/wotr-rule-index; the craft law is served live by the wotr MCP and is deliberately not carried here."
}
JSON

n=0
for d in "$src"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    name="$(basename "$d")"
    cp -r "$d" "$out/skills/$name"
    n=$((n + 1))
    printf '  %-14s %6s bytes\n' "$name" "$(wc -c < "$d/SKILL.md")"
done

echo
echo "$n skill(s) -> $out"
echo "add that folder in Claude Desktop -> Settings -> Capabilities"
