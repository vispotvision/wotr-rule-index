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
# Two outputs, because Desktop has two different doors and they are easy to confuse:
#
#   <out>/                a plugin folder -- the shape Claude Code and the Cowork
#                         skills store use.
#   <out>/../<name>.zip   one zip per skill, which is what a USER skill is uploaded
#                         as. Desktop's own user skills arrive by syncing down from
#                         the account (wotr-write on this machine is creatorType
#                         "user" with a backingPluginId), NOT from a local folder.
#                         The Extensions menu is a different mechanism again -- it
#                         wants a root manifest.json and is for MCP/DXT extensions.
#
# Rebuild and re-upload after changing any SKILL.md; these are copies by necessity,
# so they are stale the moment the source moves.
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

# one uploadable zip per skill, beside the plugin folder
for d in "$src"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    name="$(basename "$d")"
    z="$(dirname "$out")/$name.zip"
    rm -f "$z"
    ( cd "$src" && zip -qr "$z" "$name" )
    printf '  %-14s -> %s\n' "$name" "$z"
done

echo
echo "plugin folder : $out          (Claude Code / Cowork skills store shape)"
echo "skill zips    : $(dirname "$out")/<name>.zip   (upload a user skill this way)"
