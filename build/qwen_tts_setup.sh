#!/usr/bin/env bash
# Qwen3-TTS (Alibaba, Apache-2.0) on the Radeon RX 9070 XT: THE character engine (pure voice design).
# Two venvs under <WOTR_VENVS> (was C:\venvs), each with AMD's ROCm 10 PyTorch forced over the CPU torch
# that pip pulls in:
#   wotr-qwen-fast   faster-qwen3-tts (MIT; static KV cache + HIP graphs, ~2.5x real time per draw)
#                    with transformers 5.15.1 (5.17 breaks its qwen-tts-hf shim: MimiConfig.rope_theta)
#   wotr-qwen        the plain qwen-tts package (transformers 4.57) — the fallback, and batch calls
# Both get speechbrain (ECAPA speaker embeddings for the anchor check) and parselmouth (pitch).
# Model: Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign, ~4.5 GB from the Hugging Face hub (~/.cache/huggingface)
# on first use. Card caveats (in build/qwen_worker.py): pick the discrete GPU by name,
# torch.backends.cudnn.enabled = False (MIOpen's conv path was broken on the Windows gfx1201 build; on
# Linux MIOpen works, but the switch stays until measured), attn_implementation="sdpa" (no flash-attn).
#
#   bash build/qwen_tts_setup.sh
#
# UNTESTED: a line-for-line port of the PowerShell original (was build/qwen_tts_setup.ps1), written while
# narration is frozen (ROADMAP: nothing new until one engine holds Gimbzo across three renders). It has
# not been run on this machine. The two things no script can check from here are spelled out in
# build/chatterbox_gpu_setup.sh: whether AMD's index (https://stable.repo.amd.com/rocm/whl-next/) serves
# Linux wheels for the torch pin — the official fallback is https://download.pytorch.org/whl/rocm<ver>,
# with different version strings — and the group membership without which torch does not see the card:
#     sudo usermod -aG render,video oridon     (once, then log out and in)
# Both interpreters are a 3.12 from mise (the original pinned py -3.12; the stacks predate 3.14).
#
# Remove with: rm -rf ~/.venvs/wotr-qwen-fast ~/.venvs/wotr-qwen   (or the same two under <WOTR_VENVS>)
set -euo pipefail
. "$(dirname "$0")/env.sh"
amd="https://stable.repo.amd.com/rocm/whl-next/"
venvs="${WOTR_VENVS:-$HOME/.venvs}"

install_amd_torch() {   # $1 = the venv's python
    "$1" -m pip install --index-url "$amd" "torch[device-gfx1201]==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
    "$1" -m pip install --index-url "$amd" --force-reinstall --no-deps "torch==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
}
make_venv() {   # $1 = the venv dir; a 3.12 from mise (mise install is a no-op when it is there)
    if [ ! -x "$1/bin/python" ]; then
        mise install python@3.12
        mkdir -p "$(dirname "$1")"
        "$(mise where python@3.12)/bin/python" -m venv "$1"
        echo "created $1"
    fi
}

if ! id -nG | grep -qw render; then
    echo "note: $(id -un) is not in the render group, so torch will not see the card until" >&2
    echo "      sudo usermod -aG render,video $(id -un)   and a fresh login. Installing anyway." >&2
fi

# 1. the fast one
venv="$venvs/wotr-qwen-fast"; py="$venv/bin/python"
make_venv "$venv"
"$py" -m pip install --upgrade pip --quiet
"$py" -m pip install faster-qwen3-tts speechbrain librosa praat-parselmouth soundfile "transformers==5.15.1"
install_amd_torch "$py"
"$py" -c "import torch, faster_qwen3_tts; print('fast venv: torch', torch.__version__, '| gpus:', [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else '(none)')"

# 2. the plain one
venv="$venvs/wotr-qwen"; py="$venv/bin/python"
make_venv "$venv"
"$py" -m pip install --upgrade pip --quiet
"$py" -m pip install qwen-tts speechbrain praat-parselmouth soundfile
install_amd_torch "$py"
"$py" -c "import torch, qwen_tts; print('plain venv: torch', torch.__version__, '| gpu:', torch.cuda.is_available())"
