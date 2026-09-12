# Chatterbox (Resemble AI's open TTS) as a second narration engine, in its own venv
# so its pinned PyTorch stack never touches the interpreter that runs the MCP server.
#
#   powershell -ExecutionPolicy Bypass -File build\chatterbox_setup.ps1
#
# Creates build\.venv-chatterbox and installs chatterbox-tts into it (about 2 GB of
# packages: torch 2.6 CPU, transformers, diffusers, gradio...). The model weights
# (~1 GB) are fetched from the Hugging Face hub the first time a Chatterbox voice
# renders, into the usual HF cache (%USERPROFILE%\.cache\huggingface).
#
# GPU: the RX 9070 XT has no CUDA. Chatterbox runs on the CPU here (slow — minutes
# per minute of speech). If a ROCm or DirectML build of torch that matches the
# pin becomes available, install it into this venv and the worker picks it up.
#
# Remove with: Remove-Item -Recurse -Force build\.venv-chatterbox

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$venv = Join-Path $repo "build\.venv-chatterbox"

if (-not (Test-Path (Join-Path $venv "Scripts\python.exe"))) {
    python -m venv $venv
    Write-Host "created $venv"
}
& (Join-Path $venv "Scripts\python.exe") -m pip install --upgrade pip --quiet
& (Join-Path $venv "Scripts\python.exe") -m pip install chatterbox-tts
# resemble-perth (Chatterbox's audio watermarker) still imports pkg_resources, which
# setuptools removed in 81; without this the watermarker class is None and the model
# fails to construct.
& (Join-Path $venv "Scripts\python.exe") -m pip install --quiet "setuptools<81"
Write-Host ""
Write-Host "Chatterbox installed. Give a speaker `engine: chatterbox` in build\voices.yaml and render;"
Write-Host "the first render downloads the weights (~1 GB) from the Hugging Face hub."
