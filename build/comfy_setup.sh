#!/usr/bin/env bash
# ComfyUI on the Radeon RX 9070 XT: the image/video/audio graph runner the Windows box had at
# C:\Users\isaac\Documents\comfy\ComfyUI (two installs, both lost with Windows — only their
# metadata came over in ~/wotr-vault/comfy). On Linux it is one clone at ~/comfy/ComfyUI with its
# own venv, <WOTR_VENVS>/wotr-comfy, on AMD's ROCm 10 PyTorch (the same wheels the TTS venvs use),
# and it runs as the systemd user unit wotr-comfy on 127.0.0.1:8188 — loopback only; n8n reaches it
# there (network_mode: host) and nothing else does.
#
#   bash build/comfy_setup.sh            # clone or update, venv, torch, requirements, the workflows, the unit
#   bash build/comfy_setup.sh --models   # the same, then the model files the workflows in agent_workflows/ name
#
# What it does, idempotently:
#   1. clones github.com/comfyanonymous/ComfyUI into $WOTR_COMFY (default ~/comfy/ComfyUI), or pulls
#   2. makes the venv on a 3.12 from mise (ComfyUI's pins predate 3.14) and installs AMD's torch for
#      gfx1201 — torch 2.13.0+rocm10.0.0 / torchaudio 2.11.0.2 / torchvision — from
#      https://stable.repo.amd.com/rocm/whl-next/ (verified to serve these Linux wheels on 2026-09-14),
#      then ComfyUI's requirements.txt with torch held (pip would otherwise swap in the CPU build)
#   3. copies the workflow JSONs the Windows install had (~/wotr-vault/comfy/ComfyUI/agent_workflows/)
#      into the clone's user/default/workflows/ so they show in the UI's workflow list; never overwrites
#      a file that is already there
#   4. installs and starts the wotr-comfy user unit (build/systemd/wotr-comfy.service)
#   5. --models: downloads, with the venv's huggingface-hub, the checkpoints those workflows reference
#      that are freely licensed and fit the card (the list is in comfy_models(); ~20 GB; skips what exists)
#
# The card: ROCm presents it as "cuda" to torch. On Arch /dev/kfd and /dev/dri/renderD* are mode 666,
# so no render-group membership is needed (the TTS setup scripts warn about it; the warning is harmless
# here). If torch.cuda.is_available() is False after this, check `rocminfo` lists gfx1201 first.
#
# Remove with: systemctl --user disable --now wotr-comfy; rm -rf ~/.venvs/wotr-comfy ~/comfy/ComfyUI
set -euo pipefail
. "$(dirname "$0")/env.sh"

amd="https://stable.repo.amd.com/rocm/whl-next/"
venvs="${WOTR_VENVS:-$HOME/.venvs}"
venv="$venvs/wotr-comfy"; py="$venv/bin/python"
comfy="${WOTR_COMFY:-$HOME/comfy/ComfyUI}"
vault_wf="$HOME/wotr-vault/comfy/ComfyUI/agent_workflows"

# 1. the clone
if [ -d "$comfy/.git" ]; then
    git -C "$comfy" pull --ff-only --quiet && echo "updated $comfy ($(git -C "$comfy" log --oneline -1))"
else
    mkdir -p "$(dirname "$comfy")"
    git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git "$comfy"
    echo "cloned $comfy"
fi

# 2. the venv and torch
if [ ! -x "$py" ]; then
    mise install python@3.12
    mkdir -p "$venvs"
    "$(mise where python@3.12)/bin/python" -m venv "$venv"
    echo "created $venv"
fi
"$py" -m pip install --upgrade pip --quiet
if ! "$py" -c "import torch; assert '+rocm' in torch.__version__" 2>/dev/null; then
    "$py" -m pip install --index-url "$amd" "torch[device-gfx1201]==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0" torchvision
fi
# ComfyUI's requirements name torch/torchvision/torchaudio unpinned; with the ROCm builds already
# satisfying them pip leaves them alone, and the constraint file makes sure of it
constraints="$(mktemp)"; trap 'rm -f "$constraints"' EXIT
"$py" -m pip freeze | grep -E '^(torch|torchaudio|torchvision)==' > "$constraints"
"$py" -m pip install -r "$comfy/requirements.txt" -c "$constraints" --quiet
"$py" -m pip install huggingface-hub --quiet
"$py" -c "import torch; print('torch', torch.__version__, '| gpu:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '(none)')"

# 3. the workflows from the Windows install
if [ -d "$vault_wf" ]; then
    dst="$comfy/user/default/workflows"; mkdir -p "$dst"; n=0
    for f in "$vault_wf"/*.json; do
        [ -e "$f" ] || continue
        [ -e "$dst/$(basename "$f")" ] && continue
        cp "$f" "$dst/"; n=$((n + 1))
    done
    echo "workflows: $n copied from the vault into $dst"
fi

# 4. the unit
mkdir -p "$HOME/.config/systemd/user"
cp -f "$WOTR_REPO/build/systemd/wotr-comfy.service" "$HOME/.config/systemd/user/"
systemctl --user daemon-reload
systemctl --user enable --now wotr-comfy.service
echo "wotr-comfy: $(systemctl --user is-active wotr-comfy.service) — http://127.0.0.1:8188 (journalctl --user -u wotr-comfy)"

# 5. the models, on request
comfy_models() {   # repo  file-in-repo  models-subfolder   (what agent_workflows/*.json load)
    cat <<'LIST'
Comfy-Org/z_image_turbo               split_files/diffusion_models/z_image_turbo_bf16.safetensors   diffusion_models
Comfy-Org/z_image_turbo               split_files/text_encoders/qwen_3_4b.safetensors               text_encoders
Comfy-Org/z_image_turbo               split_files/vae/ae.safetensors                                vae
Comfy-Org/Real-ESRGAN_repackaged      RealESRGAN_x4plus.safetensors                                 upscale_models
Comfy-Org/BiRefNet                    background_removal/birefnet.safetensors                       background_removal
LIST
}
if [ "${1:-}" = "--models" ]; then
    while read -r repo file sub; do
        [ -n "$repo" ] || continue
        dest="$comfy/models/$sub/$(basename "$file")"
        if [ -e "$dest" ]; then echo "have $dest"; continue; fi
        mkdir -p "$comfy/models/$sub"
        echo "fetching $repo/$file"
        "$py" -c "
import sys, shutil
from huggingface_hub import hf_hub_download
p = hf_hub_download(sys.argv[1], sys.argv[2])
shutil.copy(p, sys.argv[3])
" "$repo" "$file" "$dest"
    done < <(comfy_models)
    echo "models: $(du -sh "$comfy/models" | cut -f1) under $comfy/models"
fi
