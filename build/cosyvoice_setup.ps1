# Fun-CosyVoice 3 (Alibaba FunAudioLLM, Apache-2.0) on the Radeon RX 9070 XT — the READER in the
# design-then-clone chain: Qwen VoiceDesign makes the voice once, CosyVoice 3 clones that designed take for
# every line with an instruct per line (emotion, pace) and fine-grained tags ([breath] [laughter] <strong>
# and ARPAbet hotfixes like [HH][AA1] for invented names). 0.5B, fast.
#
# The repo is not a pip package: it is cloned under C:\venvs\wotr-cosy\src (short path — see
# chatterbox_gpu_setup.ps1) and imported from there by build/cosy_worker.py. Its requirements pin a 2024
# CUDA stack (torch 2.3.1, tensorrt, deepspeed); those are skipped and AMD's ROCm 10 torch goes on last.
# Model (~2 GB): FunAudioLLM/Fun-CosyVoice3-0.5B-2512 from the Hugging Face hub into src\pretrained_models.
#
#   powershell -ExecutionPolicy Bypass -File build\cosyvoice_setup.ps1
$ErrorActionPreference = "Stop"
$venv = "C:\venvs\wotr-cosy"; $py = Join-Path $venv "Scripts\python.exe"; $src = Join-Path $venv "src"
if (-not (Test-Path $py)) { py -3.12 -m venv $venv; Write-Host "created $venv" }
& $py -m pip install --upgrade pip --quiet
if (-not (Test-Path "$src\CosyVoice")) { New-Item -ItemType Directory -Force $src | Out-Null; git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git "$src\CosyVoice" }
# the requirements minus the CUDA-only and pinned-torch lines
& $py -m pip install "conformer==0.3.2" "diffusers==0.29.0" "hydra-core==1.3.2" "HyperPyYAML==1.2.3" "inflect" "librosa" `
    "lightning" "matplotlib" "networkx" "numpy<2.3" "omegaconf==2.3.0" "onnx" "onnxruntime" "openai-whisper" "pyarrow" `
    "pydantic" "pyworld" "rich" "soundfile" "x-transformers" "wetext" "wget" "transformers==4.51.3" "huggingface_hub" `
    "speechbrain" "praat-parselmouth" "gdown" "modelscope"
& $py -m pip install --index-url https://stable.repo.amd.com/rocm/whl-next/ "torch[device-gfx1201]==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
& $py -m pip install --index-url https://stable.repo.amd.com/rocm/whl-next/ --force-reinstall --no-deps "torch==2.13.0+rocm10.0.0" "torchaudio==2.11.0.2+rocm10.0.0"
& $py -c "from huggingface_hub import snapshot_download; snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir=r'$src\CosyVoice\pretrained_models\Fun-CosyVoice3-0.5B')"
& $py -c "import torch; print('torch', torch.__version__, '| gpus:', [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else '(none)')"
