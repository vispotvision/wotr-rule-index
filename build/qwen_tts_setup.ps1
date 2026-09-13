# Qwen3-TTS (Alibaba, Apache-2.0) on the Radeon RX 9070 XT: THE character engine (pure voice design).
# Two venvs under C:\venvs (short paths — see chatterbox_gpu_setup.ps1 for why), each with AMD's native
# ROCm 10 PyTorch for Windows forced over the CPU torch that pip pulls in:
#   C:\venvs\wotr-qwen-fast   faster-qwen3-tts (MIT; static KV cache + HIP graphs, ~2.5x real time per draw)
#                             with transformers 5.15.1 (5.17 breaks its qwen-tts-hf shim: MimiConfig.rope_theta)
#   C:\venvs\wotr-qwen        the plain qwen-tts package (transformers 4.57) — the fallback, and batch calls
# Both get speechbrain (ECAPA speaker embeddings for the anchor check) and parselmouth (pitch).
# Model: Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign, ~4.5 GB from the Hugging Face hub on first use.
# Card caveats (in build/qwen_worker.py): pick the discrete GPU by name, torch.backends.cudnn.enabled = False
# (MIOpen's conv path is broken on Windows gfx1201), attn_implementation="sdpa" (no flash-attn).
#
#   powershell -ExecutionPolicy Bypass -File build\qwen_tts_setup.ps1
$ErrorActionPreference = "Stop"
$amd = "https://stable.repo.amd.com/rocm/whl-next/"

function Install-AmdTorch($py) {
    & $py -m pip install --index-url $amd "torch[device-gfx1201]==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
    & $py -m pip install --index-url $amd --force-reinstall --no-deps "torch==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
}

# 1. the fast one
$venv = "C:\venvs\wotr-qwen-fast"; $py = Join-Path $venv "Scripts\python.exe"
if (-not (Test-Path $py)) { py -3.12 -m venv $venv; Write-Host "created $venv" }
& $py -m pip install --upgrade pip --quiet
& $py -m pip install faster-qwen3-tts speechbrain librosa praat-parselmouth soundfile "transformers==5.15.1"
Install-AmdTorch $py
& $py -c "import torch, faster_qwen3_tts; print('fast venv: torch', torch.__version__, '| gpus:', [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else '(none)')"

# 2. the plain one
$venv = "C:\venvs\wotr-qwen"; $py = Join-Path $venv "Scripts\python.exe"
if (-not (Test-Path $py)) { py -3.12 -m venv $venv; Write-Host "created $venv" }
& $py -m pip install --upgrade pip --quiet
& $py -m pip install qwen-tts speechbrain praat-parselmouth soundfile
Install-AmdTorch $py
& $py -c "import torch, qwen_tts; print('plain venv: torch', torch.__version__, '| gpu:', torch.cuda.is_available())"
