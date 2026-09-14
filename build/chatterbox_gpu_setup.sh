#!/usr/bin/env bash
# Chatterbox on the Radeon RX 9070 XT: AMD's ROCm 10 PyTorch wheels (gfx1201) in a second venv at
# <WOTR_VENVS>/wotr-cb-gpu (was C:\venvs\wotr-cb-gpu). build/chatterbox_backend.py prefers this venv
# when it exists and falls back to the CPU one (wotr-cb, build/chatterbox_setup.sh) otherwise.
#
#   bash build/chatterbox_gpu_setup.sh
#
# UNTESTED: a line-for-line port of the PowerShell original (was build/chatterbox_gpu_setup.ps1),
# written while narration is frozen (ROADMAP: nothing new until one engine holds Gimbzo across
# three renders). It has not been run on this machine, and two things cannot be checked from here:
#
#   - Whether AMD's index, https://stable.repo.amd.com/rocm/whl-next/, serves Linux wheels for
#     the pins below (torch 2.13.0+rocm10.0.0 / torchaudio 2.11.0.2+rocm10.0.0 were verified on
#     Windows only). The official fallback is PyTorch's own ROCm index,
#     https://download.pytorch.org/whl/rocm<ver> (rocm7.0 at the time of writing), whose version
#     strings differ (torch==2.x.y+rocmN.N, no [device-gfx1201] extra) — change $amd and the pins
#     together if AMD's index refuses. Neither index was reachable from the porting session.
#   - The card is only visible to a user in the render and video groups. Once, then log out and in:
#         sudo usermod -aG render,video oridon
#     Until then torch.cuda.is_available() is False and the check at the end says so.
#
# Source: https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html
# chatterbox-tts pins torch 2.6, so it is installed without its pins and its other dependencies by
# hand; if a Chatterbox release ever needs something torch 2.13 no longer has, the CPU venv still
# works. The interpreter is a 3.12 from mise, not the system python3 (3.14): the original took
# whatever `python` was, but here that would be the wotr venv's 3.14 and the pinned stack
# (transformers 5.2.0, diffusers 0.29.0, safetensors 0.5.3, spacy-pkuseg) predates it; the other
# ROCm venvs are 3.12 too. Weights (~1 GB) land in ~/.cache/huggingface on first use.
#
# Remove with: rm -rf ~/.venvs/wotr-cb-gpu   (or <WOTR_VENVS>/wotr-cb-gpu if that is set elsewhere)

set -euo pipefail
. "$(dirname "$0")/env.sh"

venv="${WOTR_VENVS:-$HOME/.venvs}/wotr-cb-gpu"
py="$venv/bin/python"
amd="https://stable.repo.amd.com/rocm/whl-next/"

if ! id -nG | grep -qw render; then
    echo "note: $(id -un) is not in the render group, so torch will not see the card until" >&2
    echo "      sudo usermod -aG render,video $(id -un)   and a fresh login. Installing anyway." >&2
fi

if [ ! -x "$py" ]; then
    # a 3.12 from mise: the pinned stack predates 3.14 (mise install is a no-op when it is there)
    mise install python@3.12
    mkdir -p "$(dirname "$venv")"
    "$(mise where python@3.12)/bin/python" -m venv "$venv"
    echo "created $venv"
fi
"$py" -m pip install --upgrade pip --quiet
# 1. Chatterbox without its torch pin, then what it needs (gradio is only for its demo app and is skipped).
#    Some of these depend on torch and would pull PyPI's CPU torch, so AMD's build goes on AFTER them.
"$py" -m pip install --no-deps chatterbox-tts
"$py" -m pip install "numpy>=2.0" "librosa==0.11.0" s3tokenizer "transformers==5.2.0" "diffusers==0.29.0" \
    "resemble-perth>=1.0.0" "conformer==0.3.2" "safetensors==0.5.3" spacy-pkuseg "pykakasi==2.3.0" pyloudnorm omegaconf "setuptools<81"
# 2. PyTorch for the card (gfx1201 = RX 9070 / 9070 XT), forced over whatever step 1 pulled in
"$py" -m pip install --index-url "$amd" \
    "torch[device-gfx1201]==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
"$py" -m pip install --index-url "$amd" --force-reinstall --no-deps \
    "torch==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
# 3. does the card show up?
"$py" -c "import torch; print('torch', torch.__version__, '| gpu:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '(none)')"
echo ""
echo "Done. Render anything with a Chatterbox voice and the worker reports 'loaded ... on cuda' (ROCm presents the card as cuda)."
