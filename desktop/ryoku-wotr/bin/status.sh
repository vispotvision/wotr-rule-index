#!/bin/bash
# Server state for the bar widget, as one JSON line. Never blocks for long:
# docker inspect is instant and rcon-cli gets a short timeout.
dir="${1:-$HOME/minecraft}"; dir="${dir/#\~/$HOME}"
cd "$dir" 2>/dev/null || { echo '{"state":"missing","players":[],"max":0}'; exit 0; }
name=$(grep -E '^\s*container_name:' docker-compose.yml 2>/dev/null | head -1 | awk '{print $2}'); name=${name:-mc}
inspect=$(docker inspect -f '{{.State.Running}} {{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}} {{.State.StartedAt}}' "$name" 2>/dev/null)
if [[ -z $inspect ]]; then state=stopped; health=none; started=""
else read -r running health started <<<"$inspect"; state=$([[ $running == true ]] && echo running || echo stopped); fi
players=(); max=0; online=0; motd=$(grep -E '^MOTD=' .env 2>/dev/null | cut -d= -f2- | tr -d '"'); version=$(grep -E "^VERSION=" .env 2>/dev/null | cut -d= -f2- | sed "s/[[:space:]]*#.*//"); type=$(grep -E "^TYPE=" .env 2>/dev/null | cut -d= -f2- | sed "s/[[:space:]]*#.*//"); pack=$(grep -E "^(MODRINTH_MODPACK|CF_SLUG|GENERIC_PACK)=" .env 2>/dev/null | head -1 | cut -d= -f2- | sed "s/[[:space:]]*#.*//; s|.*/||")
if [[ $state == running && $health == healthy ]]; then
  list=$(timeout 3 docker exec "$name" rcon-cli list 2>/dev/null | head -1)
  # "There are 2 of a max of 20 players online: Steve, Alex"
  if [[ $list =~ There\ are\ ([0-9]+)\ of\ a\ max\ of\ ([0-9]+) ]]; then online=${BASH_REMATCH[1]}; max=${BASH_REMATCH[2]}; fi
  names=${list#*online:}; [[ $names == "$list" ]] && names=""
  IFS=',' read -r -a players <<<"$(echo "$names" | tr -d ' ')"
fi
python3 - "$state" "$health" "$started" "$online" "$max" "$motd" "$version" "$type" "$pack" "${players[@]}" <<'PY'
import json, sys, datetime
state, health, started, online, mx, motd, version, typ, pack = sys.argv[1:10]
players = [p for p in sys.argv[10:] if p]
uptime = ""
if started and state == "running":
    try:
        t = datetime.datetime.fromisoformat(started.replace("Z", "+00:00"))
        s = int((datetime.datetime.now(datetime.timezone.utc) - t).total_seconds())
        uptime = f"{s // 3600}h {s % 3600 // 60}m" if s >= 3600 else f"{s // 60}m"
    except Exception:
        pass
print(json.dumps({"state": state, "health": health, "uptime": uptime, "online": int(online or 0), "max": int(mx or 0),
                  "players": players, "motd": motd, "version": version, "type": typ, "pack": pack}))
PY
