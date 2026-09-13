# Chatterbox on the Radeon RX 9070 XT: AMD's native PyTorch-for-Windows wheels (ROCm 10, gfx1201)
# in a second venv at C:\venvs\wotr-cb-gpu. build\chatterbox_backend.py prefers this venv when it
# exists and falls back to the CPU one (build\.venv-chatterbox) otherwise.
#
# Why not under build\: AMD's torch wheel ships licence files nested ten folders deep, and under
# the repo path they pass Windows' 260-character limit and the install dies half-way (no RECORD,
# "torch None", "No module named torchgen"). A short root keeps every path under the limit.
#
#   powershell -ExecutionPolicy Bypass -File build\chatterbox_gpu_setup.ps1
#
# Source: https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html
# (Windows: ROCm 10.0.0 wheels only, Python 3.11–3.14, a current AMD driver). chatterbox-tts
# pins torch 2.6, so it is installed without its pins and its other dependencies by hand;
# if a Chatterbox release ever needs something torch 2.13 no longer has, the CPU venv still works.
#
# Remove with: Remove-Item -Recurse -Force C:\venvs\wotr-cb-gpu

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$venv = "C:\venvs\wotr-cb-gpu"
$py = Join-Path $venv "Scripts\python.exe"

if (-not (Test-Path $py)) {
    New-Item -ItemType Directory -Force (Split-Path $venv) | Out-Null
    python -m venv $venv
    Write-Host "created $venv"
}
& $py -m pip install --upgrade pip --quiet
# 1. Chatterbox without its torch pin, then what it needs (gradio is only for its demo app and is skipped).
#    Some of these depend on torch and would pull PyPI's CPU torch, so AMD's build goes on AFTER them.
& $py -m pip install --no-deps chatterbox-tts
& $py -m pip install "numpy>=2.0" "librosa==0.11.0" s3tokenizer "transformers==5.2.0" "diffusers==0.29.0" `
    "resemble-perth>=1.0.0" "conformer==0.3.2" "safetensors==0.5.3" spacy-pkuseg "pykakasi==2.3.0" pyloudnorm omegaconf "setuptools<81"
# 2. PyTorch for the card (gfx1201 = RX 9070 / 9070 XT), forced over whatever step 1 pulled in
& $py -m pip install --index-url https://stable.repo.amd.com/rocm/whl-next/ `
    "torch[device-gfx1201]==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
& $py -m pip install --index-url https://stable.repo.amd.com/rocm/whl-next/ --force-reinstall --no-deps `
    "torch==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
# 3. does the card show up?
& $py -c "import torch; print('torch', torch.__version__, '| gpu:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '(none)')"
Write-Host ""
Write-Host "Done. Render anything with a Chatterbox voice and the worker reports 'loaded ... on cuda' (ROCm presents the card as cuda)."
