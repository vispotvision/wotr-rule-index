#!/usr/bin/env bash
# Put the secrets into ~/.config/wotr/env without opening an editor.
#
#   bash build/secrets.sh                 # asks for each of the three, one at a time
#   bash build/secrets.sh DISCORD_TOKEN   # just that one
#
# Paste the value at the prompt (nothing is echoed), press Enter. Enter on an empty
# line keeps whatever is there. The values go only into that file (mode 600); this
# script prints none of them, and nothing here goes anywhere but the file.
#
# Where each one comes from, if it has to be issued again:
#   NOTION_TOKEN        notion.so/profile/integrations -> the "oridon" integration ->
#                       Configuration -> Internal Integration Secret (Show, or Refresh)
#   DISCORD_TOKEN       discord.com/developers/applications -> WOTR Bot -> Bot ->
#                       Reset Token (the old one is gone; the bot keeps its identity)
#   ELEVENLABS_API_KEY  elevenlabs.io -> profile -> API keys -> Create (optional:
#                       only /narrate elevenlabs needs it)
#
# Afterwards: the bot needs a restart to see its token (this script offers to do it);
# the hourly sync reads NOTION_TOKEN on its next run.

set -u
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
FILE="${WOTR_ENV_FILE:-$HOME/.config/wotr/env}"
if [ ! -f "$FILE" ]; then
    mkdir -p "$(dirname "$FILE")"
    cp "$here/wotr.env.example" "$FILE"
    echo "created $FILE from the template"
fi
chmod 600 "$FILE"

keys=("$@")
[ ${#keys[@]} -gt 0 ] || keys=(NOTION_TOKEN DISCORD_TOKEN ELEVENLABS_API_KEY)

# replace (or append) one KEY=value line; python so the value needs no escaping
set_key() {
    python3 - "$FILE" "$1" "$2" <<'PY'
import sys
path, key, val = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(path, encoding="utf-8").read().splitlines()
done = False
for i, line in enumerate(lines):
    if line.startswith(key + "="):
        lines[i] = f"{key}={val}"; done = True; break
if not done:
    lines.append(f"{key}={val}")
open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
PY
}

changed=()
for key in "${keys[@]}"; do
    state="empty"
    if grep -qE "^${key}=.+" "$FILE"; then state="set"; fi
    printf '%s (currently %s) — paste and press Enter, or Enter to keep: ' "$key" "$state"
    IFS= read -rs val; echo
    val="${val//[$'\r\n']/}"
    if [ -n "$val" ]; then
        set_key "$key" "$val"
        changed+=("$key")
        echo "  $key saved"
    fi
done
chmod 600 "$FILE"

[ ${#changed[@]} -gt 0 ] || { echo "nothing changed"; exit 0; }
echo
echo "saved to $FILE: ${changed[*]}"
case " ${changed[*]} " in *" DISCORD_TOKEN "*)
    if systemctl --user cat wotr-bot.service >/dev/null 2>&1; then
        printf 'restart the Discord bot now so it picks the token up? [y/N] '
        read -r yn
        if [ "${yn,,}" = "y" ]; then
            systemctl --user restart wotr-bot.service
            sleep 4
            systemctl --user --no-pager status wotr-bot.service | head -5
            echo "log: tail -f $here/../bot/.bot.log"
        fi
    fi ;;
esac
case " ${changed[*]} " in *" NOTION_TOKEN "*)
    echo "the sync will use NOTION_TOKEN on its next hourly run; to run it now: systemctl --user start wotr-sync.service" ;;
esac
