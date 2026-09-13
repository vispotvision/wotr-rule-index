# Supertonic 3 (Supertone) for build/supertonic_backend.py — the fast, CPU-only narration tier.
# Makes C:\venvs\wotr-supertonic (a short path on purpose: MAX_PATH bit the Chatterbox venv under
# the repo) and installs the `supertonic` package: onnxruntime, numpy, soundfile, huggingface-hub.
# The ~400 MB model lands in ~\.cache\supertonic3 on first use. No torch, no GPU.
# Model licence OpenRAIL-M (personal and commercial use; no deception / impersonation), code MIT.
# Upstream was archived on 9 Sep 2026 (supertone-oss-archive); the package still resolves the weights.
$ErrorActionPreference = "Stop"
$venv = "C:\venvs\wotr-supertonic"
if (-not (Test-Path $venv)) { py -3.12 -m venv $venv }
& "$venv\Scripts\python.exe" -m pip install --upgrade pip
& "$venv\Scripts\python.exe" -m pip install "supertonic==1.3.1"
& "$venv\Scripts\python.exe" -c "from supertonic import TTS; t = TTS(auto_download=True); print('supertonic-3 ready,', t.sample_rate, 'Hz')"
