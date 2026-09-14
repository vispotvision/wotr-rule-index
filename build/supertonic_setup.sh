#!/usr/bin/env bash
# Supertonic 3 (Supertone) for build/supertonic_backend.py — the fast, CPU-only narration tier.
# Makes <WOTR_VENVS>/wotr-supertonic (was C:\venvs\wotr-supertonic) and installs the `supertonic`
# package: onnxruntime, numpy, soundfile, huggingface-hub. The ~400 MB model lands in
# ~/.cache/supertonic3 on first use. No torch, no GPU — so no render-group business here.
# Model licence OpenRAIL-M (personal and commercial use; no deception / impersonation), code MIT.
# Upstream was archived on 9 Sep 2026 (supertone-oss-archive); the package still resolves the weights.
#
#   bash build/supertonic_setup.sh
#
# RUN on this machine 2026-09-14 as written: supertonic 1.3.1 resolved on the 3.12 and answered
# "supertonic-3 ready, 44100 Hz" on the first run.
#
# Remove with: rm -rf ~/.venvs/wotr-supertonic   (or <WOTR_VENVS>/wotr-supertonic if that is set elsewhere)
set -euo pipefail
. "$(dirname "$0")/env.sh"
venv="${WOTR_VENVS:-$HOME/.venvs}/wotr-supertonic"; py="$venv/bin/python"
if [ ! -x "$py" ]; then mise install python@3.12; mkdir -p "$(dirname "$venv")"; "$(mise where python@3.12)/bin/python" -m venv "$venv"; echo "created $venv"; fi
"$py" -m pip install --upgrade pip
"$py" -m pip install "supertonic==1.3.1"
"$py" -c "from supertonic import TTS; t = TTS(auto_download=True); print('supertonic-3 ready,', t.sample_rate, 'Hz')"
