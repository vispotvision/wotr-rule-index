#!/bin/bash
# The MCP tab: the WOTR MCP's named keys, read from and changed through the key dashboard
# (wotr-mcp http, 127.0.0.1:8790, this PC only). The dashboard stays the one writer of the keys.
#   mcp.sh list              one JSON line for the panel, with every token and link left out
#   mcp.sh copy <id>         that key's connector URL to the clipboard (the only path a token takes)
#   mcp.sh enable|disable <id>
url="http://127.0.0.1:8790"
valid_id() { [[ $1 =~ ^[0-9a-f]+$ ]] || { echo "bad key id" >&2; exit 2; }; }
case "${1:-list}" in
list)
  state=$(curl -s -m 4 "$url/api/state")
  [[ -n $state ]] || { echo '{"up":false,"keys":[]}'; exit 0; }
  jq -c '.tools as $t | {up: true, base, now, total: ($t | length), online: ([.keys[] | select(.online)] | length),
    keys: [.keys[] | {id, name, preset, enabled, online, sessions, calls, last_used, last_ip,
      tools: (if .preset == "full" then ($t | length)
              elif .preset == "core" then ([$t[] | select(.core)] | length)
              elif .preset == "read-only" then ([$t[] | select(.core and .read_only)] | length)
              else (.tools | length) end)}]}' <<<"$state" 2>/dev/null || echo '{"up":false,"keys":[]}'
  ;;
copy)
  valid_id "$2"
  row=$(curl -s -m 4 "$url/api/state" | jq -c --arg id "$2" '.keys[] | select(.id == $id) | {name, mcp_url}')
  link=$(jq -r '.mcp_url // empty' <<<"$row")
  [[ -n $link ]] || { notify-send "WOTR MCP" "Could not read that key's link"; exit 1; }
  printf '%s' "$link" | wl-copy
  notify-send "WOTR MCP" "Connector link copied: $(jq -r .name <<<"$row")"
  ;;
enable|disable)
  valid_id "$2"
  on=$([[ $1 == enable ]] && echo true || echo false)
  curl -s -m 6 -o /dev/null -X PATCH "$url/api/keys/$2" -H 'Content-Type: application/json' -d "{\"enabled\":$on}"
  ;;
*) echo "usage: mcp.sh list|copy <id>|enable <id>|disable <id>" >&2; exit 2 ;;
esac
