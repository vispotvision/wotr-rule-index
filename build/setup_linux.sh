#!/usr/bin/env bash
# One-shot bootstrap of the WOTR tooling on a fresh Linux machine. Idempotent: run it
# again after a pull and it only does what is missing. Nothing here needs sudo; the
# steps that do are printed at the end for Isaac's hands. (Arch is assumed only in the
# pacman lines it prints.)
#
#   bash build/setup_linux.sh               # everything
#   bash build/setup_linux.sh --no-systemd  # stop before the units: a machine that only
#                                           # needs the tools, or a first look
#
# What it does:
#   1. ~/.venvs/wotr (WOTR_VENVS/wotr): python3 -m venv if missing, then
#      pip install -r requirements.txt into it, quietly. The narration extras are
#      requirements-audio.txt and are NOT installed here: narration is frozen behind
#      the Gimbzo gate (ROADMAP); install them by hand when that changes.
#   2. ~/.config/wotr/env from build/wotr.env.example if missing, mode 600. The secrets
#      in it are empty until they are pasted in — from the password manager, never
#      from a chat or a commit.
#   3. build/systemd_setup.sh: the four timers and the two services (skipped with
#      --no-systemd).
#   4. prints what is left for Isaac: the secrets, docker, tailscale, ollama, rclone,
#      Claude Desktop.
#
# Remove with: build/systemd_setup.sh --remove; rm -rf ~/.venvs/wotr; the env file is
# yours to keep.

set -uo pipefail
. "$(dirname "$0")/env.sh"

no_systemd=0
case "${1:-}" in
    --no-systemd) no_systemd=1 ;;
    '') ;;
    *) echo "usage: bash build/setup_linux.sh [--no-systemd]"; exit 2 ;;
esac

# 1. the interpreter. env.sh has already looked for it; on a fresh machine it fell back
#    to the system python3, which is why the path is computed here and not taken from
#    $WOTR_PYTHON.
venv="${WOTR_VENVS:-$HOME/.venvs}/wotr"
if [ -x "$venv/bin/python" ]; then
    echo "venv: $venv (exists)"
else
    echo "venv: creating $venv"
    mkdir -p "$(dirname "$venv")"
    python3 -m venv "$venv" || { echo "python3 -m venv failed; is python installed?"; exit 1; }
fi
echo "venv: installing requirements.txt (quiet; a minute the first time)"
if ! "$venv/bin/python" -m pip install -q -r "$WOTR_REPO/requirements.txt"; then
    echo "pip install failed; fix that and re-run (nothing else has been changed yet)"
    exit 1
fi
"$venv/bin/python" -c 'import sys; print("venv: python", sys.version.split()[0], "ready")'

# 2. the env file
cfg="$HOME/.config/wotr/env"
if [ -f "$cfg" ]; then
    echo "env: $cfg (exists; not touched)"
else
    mkdir -p "$(dirname "$cfg")"
    cp "$WOTR_REPO/build/wotr.env.example" "$cfg"
    chmod 600 "$cfg"
    echo "env: wrote $cfg from build/wotr.env.example (mode 600)"
    echo "     fill the secrets in: NOTION_TOKEN, DISCORD_TOKEN, ELEVENLABS_API_KEY, HF_TOKEN"
    echo "     (the sync needs NOTION_TOKEN; the bot needs DISCORD_TOKEN; the others can wait)"
fi

# 3. the units
if [ "$no_systemd" -eq 1 ]; then
    echo "systemd: skipped (--no-systemd); run build/systemd_setup.sh when ready"
else
    echo "systemd: installing the units"
    bash "$WOTR_REPO/build/systemd_setup.sh" || echo "systemd_setup.sh exited $?; see above"
fi

# 4. Isaac's hands
cat <<TXT

Done here. What is left needs you (sudo, logins, secrets):

  1. Secrets: edit $cfg and paste in NOTION_TOKEN (the sync), DISCORD_TOKEN (the bot),
     ELEVENLABS_API_KEY and HF_TOKEN (narration; can wait). Then:
        systemctl --user restart wotr-bot      # picks the token up
        systemctl --user start wotr-sync       # a first sync now

  2. Docker, for n8n (n8n/docker-compose.yml in this repo; network_mode: host, so the
     container reaches the job runner at http://127.0.0.1:8799 like any local process):
        sudo usermod -aG docker "\$USER"       # then log out and in, or: newgrp docker
        sudo systemctl enable --now docker
        cd ~/wotr-rule-index/n8n && docker compose up -d

  3. Tailscale, for the shared MCP:
        sudo pacman -S tailscale
        sudo systemctl enable --now tailscaled
        sudo tailscale up
        bash build/mcp_public_setup.sh        # the secret, the unit, the funnel, the URL

  4. Ollama on the GPU (ROCm), for the cheap passes n8n runs:
        sudo pacman -S ollama-rocm
        sudo systemctl enable --now ollama

  5. Google Drive, if you want the Drive exports and the backup on Drive:
        rclone config                          # a remote named gdrive
        rclone mount gdrive: ~/GoogleDrive     # then WOTR_DRIVE=/home/$USER/GoogleDrive in $cfg
     Left empty, the exports are skipped and the weekly zip goes to WOTR_BACKUP_DIR.

  6. Claude Desktop: bash build/install_mcp.sh registers the MCP with it.
  7. The nightly's Claude step and the book need the CLI signed in: claude /login.
TXT
