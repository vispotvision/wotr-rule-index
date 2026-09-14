#!/usr/bin/env bash
# Fun-CosyVoice 3 (Alibaba FunAudioLLM, Apache-2.0) on the Radeon RX 9070 XT — the READER in the
# design-then-clone chain: Qwen VoiceDesign makes the voice once, CosyVoice 3 clones that designed take for
# every line with an instruct per line (emotion, pace) and fine-grained tags ([breath] [laughter] <strong>
# and ARPAbet hotfixes like [HH][AA1] for invented names). 0.5B, fast.
#
#   bash build/cosyvoice_setup.sh
#
# RUN on this machine 2026-09-14: built from AMD's index as written (both GPUs listed, the worker picks
# the 9070 XT by name); the one thing the port missed was pkg_resources (the setuptools pin below). No
# render group is needed on Arch (/dev/kfd is mode 666), so the note under it is harmless noise.
#
# The repo is not a pip package: it is cloned under <WOTR_VENVS>/wotr-cosy/src (was C:\venvs\wotr-cosy\src)
# and imported from there by build/cosy_worker.py, which finds it through common.venv_python("cosy"). Its
# requirements pin a 2024 CUDA stack (torch 2.3.1, tensorrt, deepspeed); those are skipped and AMD's ROCm 10
# torch goes on last. The interpreter is a 3.12 from mise (the original pinned py -3.12; the stack predates
# 3.14). Model (~2 GB): FunAudioLLM/Fun-CosyVoice3-0.5B-2512 from the Hugging Face hub into
# src/CosyVoice/pretrained_models — a local_dir download, so it lives with the clone, not in ~/.cache/huggingface.
#
# Remove with: rm -rf ~/.venvs/wotr-cosy   (or <WOTR_VENVS>/wotr-cosy; the clone and the model go with it)
set -euo pipefail
. "$(dirname "$0")/env.sh"
venv="${WOTR_VENVS:-$HOME/.venvs}/wotr-cosy"; py="$venv/bin/python"; src="$venv/src"
amd="https://stable.repo.amd.com/rocm/whl-next/"
if ! id -nG | grep -qw render; then
    echo "note: $(id -un) is not in the render group, so torch will not see the card until" >&2
    echo "      sudo usermod -aG render,video $(id -un)   and a fresh login. Installing anyway." >&2
fi
if [ ! -x "$py" ]; then mise install python@3.12; mkdir -p "$(dirname "$venv")"; "$(mise where python@3.12)/bin/python" -m venv "$venv"; echo "created $venv"; fi
"$py" -m pip install --upgrade pip --quiet
if [ ! -d "$src/CosyVoice" ]; then mkdir -p "$src"; git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git "$src/CosyVoice"; fi
# the requirements minus the CUDA-only and pinned-torch lines
"$py" -m pip install "conformer==0.3.2" "diffusers==0.29.0" "hydra-core==1.3.2" "HyperPyYAML==1.2.3" "inflect" "librosa" \
    "lightning" "matplotlib" "networkx" "numpy<2.3" "omegaconf==2.3.0" "onnx" "onnxruntime" "openai-whisper" "pyarrow" \
    "pydantic" "pyworld" "rich" "soundfile" "x-transformers" "wetext" "wget" "transformers==4.51.3" "huggingface_hub" \
    "speechbrain" "praat-parselmouth" "gdown" "modelscope" "setuptools<81"
# setuptools<81: cosyvoice/dataset/processor.py imports pkg_resources, which setuptools 81 removed
# (found on the first Linux run, 2026-09-14 — the worker died with ModuleNotFoundError at import)
"$py" -m pip install --index-url "$amd" "torch[device-gfx1201]==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
"$py" -m pip install --index-url "$amd" --force-reinstall --no-deps "torch==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
# the model, into the clone (build/cosy_worker.py's MODEL_DIR); the path goes in through the environment, not a quoted literal
WOTR_COSY_MODEL_DIR="$src/CosyVoice/pretrained_models/Fun-CosyVoice3-0.5B" \
    "$py" -c "import os; from huggingface_hub import snapshot_download; snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir=os.environ['WOTR_COSY_MODEL_DIR'])"
"$py" -c "import torch; print('torch', torch.__version__, '| gpus:', [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else '(none)')"
