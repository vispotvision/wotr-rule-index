#!/usr/bin/env bash
# Chatterbox (Resemble AI's open TTS) as a second narration engine, in its own venv
# so its pinned PyTorch stack never touches the interpreter that runs the MCP server.
#
#   bash build/chatterbox_setup.sh
#
# UNTESTED: a line-for-line port of the PowerShell original (was build/chatterbox_setup.ps1),
# written while narration is frozen (ROADMAP: nothing new until one engine holds Gimbzo
# across three renders). It has not been run on this machine.
#
# Creates <WOTR_VENVS>/wotr-cb (was build/.venv-chatterbox; every engine venv now lives
# under WOTR_VENVS, see build/wotr.env.example) and installs chatterbox-tts into it (about
# 2 GB of packages: torch 2.6 CPU, transformers, diffusers, gradio...). The interpreter is
# a 3.12 from mise rather than the system python3 (3.14): chatterbox-tts pins torch 2.6,
# which predates 3.14 and has no wheel for it. The model weights (~1 GB) are fetched from
# the Hugging Face hub the first time a Chatterbox voice renders, into the usual HF cache
# (~/.cache/huggingface).
#
# GPU: the RX 9070 XT has no CUDA. This venv runs Chatterbox on the CPU (slow — minutes
# per minute of speech). The card goes through build/chatterbox_gpu_setup.sh (AMD's ROCm
# torch in wotr-cb-gpu), which build/chatterbox_backend.py prefers when it exists.
#
# Remove with: rm -rf ~/.venvs/wotr-cb   (or <WOTR_VENVS>/wotr-cb if that is set elsewhere)

set -euo pipefail
. "$(dirname "$0")/env.sh"

venv="${WOTR_VENVS:-$HOME/.venvs}/wotr-cb"
py="$venv/bin/python"

if [ ! -x "$py" ]; then
    # a 3.12 from mise: the pinned stack predates 3.14 (mise install is a no-op when it is there)
    mise install python@3.12
    mkdir -p "$(dirname "$venv")"
    "$(mise where python@3.12)/bin/python" -m venv "$venv"
    echo "created $venv"
fi
"$py" -m pip install --upgrade pip --quiet
"$py" -m pip install chatterbox-tts
# resemble-perth (Chatterbox's audio watermarker) still imports pkg_resources, which
# setuptools removed in 81; without this the watermarker class is None and the model
# fails to construct.
"$py" -m pip install --quiet "setuptools<81"
echo ""
echo "Chatterbox installed. Give a speaker \`engine: chatterbox\` in build/voices.yaml and render;"
echo "the first render downloads the weights (~1 GB) from the Hugging Face hub."
