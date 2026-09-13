# TTS engines on Windows + ROCm (RX 9070 XT, gfx1201) — viability survey

Written 2026-09-12. Angle: what each engine needs under the hood and whether it will run on
this box: Windows 11, Ryzen 7 7800X3D, 64 GB RAM, Radeon RX 9070 XT 16 GB (gfx1201),
AMD native PyTorch `torch==2.13.0+rocm10.0.0` from `https://stable.repo.amd.com/rocm/whl-next/`.
Already installed and working: Kokoro (kokoro-onnx, CPU) and Chatterbox Turbo/standard (~1.5x real time).

Everything below is from model cards, READMEs, pyproject files and issue trackers read today;
links are inline. Where nobody has reported an engine on AMD, it says so.

---

## 1. What the box can and cannot do (cross-cutting)

**What the AMD Windows wheel is.** AMD's ROCm-on-Windows PyTorch (built by [TheRock](https://github.com/ROCm/TheRock/blob/main/RELEASES.md)) ships torch 2.13.0 / 2.12.0 on ROCm 10.0.0 for Python 3.11–3.14, with per-GPU "device extras" (`torch[device-gfx1201]`) ([AMD install docs](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html)). AMD's own limitations page says: "On Windows, only Pytorch is supported, not the entire ROCm stack", "No ML training support", "only LLM batch sizes of 1 are officially supported", and warns that transformers older than 4.55.5 may not work ([limitations](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/limitations/limitationsrad.html)). It also recommends `TORCH_BLAS_PREFER_HIPBLASLT=1` when LLM inference is slow.

**The five things that decide viability here:**

1. **MIOpen (convolutions) is the recurring problem, not the LLM part.** Every TTS engine ends in a neural vocoder / codec decoder built from Conv1d stacks (HiFi-GAN, Vocos, BigVGAN, DAC, iSTFTNet, BiCodec, the Qwen3-TTS 12 Hz decoder). On Windows gfx120X, MIOpen either fails to compile kernels (`HIPRTC_ERROR_COMPILATION (6)` in `naive_conv.cpp`, [MIOpen #3862](https://github.com/ROCm/MIOpen/issues/3862)) or falls back to the naive/GemmFwdRest solver with `workspace = 0`, which is why [TheRock #3077](https://github.com/ROCm/TheRock/issues/3077) measured **Qwen3-TTS at RTF ≈ 12.6 on an RX 9060 XT under Windows** ("FindConvFwdAlgorithm ... workspace = 0" → `ConvDirectNaiveConvFwd`), and why XTTS-v2 ran "3-5x slower on GPU than CPU" on gfx1151 ([TheRock #5105](https://github.com/ROCm/TheRock/issues/5105)), and Kokoro's PyTorch path ran slower than CPU on a 6800 XT ([hexgrad/kokoro #50](https://github.com/hexgrad/kokoro/issues/50)). The workaround that keeps coming back is the one Isaac already uses: `torch.backends.cudnn.enabled = False` (routes conv through PyTorch's own im2col+GEMM path instead of MIOpen; [TheRock #1542](https://github.com/ROCm/TheRock/issues/1542)). Alternatives seen in the threads: `MIOPEN_DEBUG_CONV_DIRECT_NAIVE_CONV_FWD=0`, `MIOPEN_DEBUG_CONV_DIRECT=0`, `MIOPEN_FIND_MODE=2` (the last was reported as ignored on Windows in #3077). Rule of thumb: **put `torch.backends.cudnn.enabled = False` at the top of every engine's entry script, before the model loads.**

2. **Attention: no `flash-attn` wheel, but SDPA may be fine.** The `flash-attn` PyPI package does not build for ROCm on Windows; every engine that lists it must be told to use `attn_implementation="sdpa"` (or `"eager"` as last resort). PyTorch upstream merged AOTriton-backed flash/mem-efficient SDPA for Windows ROCm in Sept 2025 ([pytorch PR #162330](https://github.com/pytorch/pytorch/pull/162330)), and AOTriton 0.10 lists gfx1201 as an *official* (not experimental) target, so the 2.13 wheel should already use it; on gfx1100 people still needed `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1`. The cautionary datapoint is [VibeVoice #185](https://github.com/microsoft/VibeVoice/issues/185): 7900 XTX on Windows, sdpa printed "Mem Efficient attention on Current AMD GPU is still experimental", eager fell to ~1 token/s, 0.5B model ran barely at real time. Check once on this box:
   ```python
   import torch; from torch.nn.attention import sdpa_kernel, SDPBackend
   q=k=v=torch.randn(1,8,512,64,device="cuda",dtype=torch.bfloat16)
   with sdpa_kernel(SDPBackend.FLASH_ATTENTION): torch.nn.functional.scaled_dot_product_attention(q,k,v)
   ```
   If that raises, set `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1` and retry; if it still raises, everything transformer-shaped will be slower but will run on the math backend.

3. **`torch.compile` / Triton.** Official Windows Triton does not exist; the community `triton-windows` (3.6.0.post25 at the time of the [habr write-up](https://habr.com/en/articles/987672)) is reported to work on AMD ROCm Windows for gfx1100 with torch 2.11+rocm7.12. Untested with the 2.13 wheel on gfx1201. Treat `torch.compile` as **off by default** (`optimize=False`, `NO_TORCH_COMPILE=1`, no `--compile` flag) and only try it later.

4. **Definitely unavailable on this box:** `bitsandbytes` CUDA kernels (no Windows ROCm build — so no 8-bit/4-bit loading of the big models), `vLLM` (the only Windows ROCm port, [ThePie88/vLLM-ROCm-Windows](https://github.com/ThePie88/vLLM-ROCm-Windows), is single-GPU text-LLM only, verified on gfx1100 only), `deepspeed`, `mamba-ssm` / `causal-conv1d` (CUDA-only builds), `xformers`, `torchcodec` (no ROCm build — [VoxCPM #203](https://github.com/OpenBMB/VoxCPM/issues/203) monkeypatches around it), `onnxruntime-gpu` CUDA EP (use CPU EP or DirectML EP instead), TensorRT.

5. **Pins that fight the AMD wheel.** Almost every project pins torch to an NVIDIA index or an old exact version. The pattern that works: create the venv, install AMD torch/torchaudio first, then `pip install <engine> --no-deps` and add the remaining requirements by hand. devnen's server README says it plainly: "The --no-deps flag on chatterbox-tts is critical: without it, pip will replace the ROCm torch wheels with CPU-only versions from PyPI" ([Chatterbox-TTS-Server](https://github.com/devnen/Chatterbox-TTS-Server)). Projects that use `uv sync` with a locked `cu128` index (IndexTTS, Dia2, Zonos) need `uv sync --no-install-package torch` or a plain venv instead. Keep **one venv per engine**: Chatterbox wants `transformers==5.2.0`, Qwen3-TTS wants `4.57.3`, IndexTTS wants `4.52.1`.

Two gfx1201-specific env vars seen in the wild: `ROCBLAS_USE_HIPBLASLT=0` ("required for stability on gfx1201", devnen RDNA4 compose file) and `HIP_VISIBLE_DEVICES=<n>` to skip the Ryzen iGPU ([voicebox #918](https://github.com/jamiepine/voicebox/issues/918), the one report of a 9070 XT + Windows + ROCm 7.14 TTS setup: torch 2.12.0+rocm7.14.0, Python 3.12, Qwen3-TTS/Chatterbox/Kokoro app, "GPU usage 20-40%").

---

## 2. Engine by engine

Format: what it is → under the hood → CUDA-only pieces → AMD evidence → pins vs torch 2.13 → the flag/change → verdict. VRAM figures are bf16 unless stated.

### 2.1 Chatterbox (Resemble AI) — already running
- **Under the hood:** Llama-style 0.5B token LM + S3Gen (flow-matching + HiFi-GAN) decoder; plain PyTorch/transformers. Turbo is a 350M variant with `[laugh]`/`[sigh]` tags.
- **CUDA-only:** none.
- **Pins:** `chatterbox-tts 0.1.7` pins `torch==2.6.0`, `torchaudio==2.6.0`, `transformers==5.2.0`, `numpy<2` on Python <3.13 ([pyproject](https://raw.githubusercontent.com/resemble-ai/chatterbox/master/pyproject.toml)) — must be installed `--no-deps` over the AMD wheel.
- **AMD evidence:** Fedora/RX 7600 how-to ([#445](https://github.com/resemble-ai/chatterbox/issues/445)); a 7700 XT container run measured RTF 11.2 *with* "workspace memory warnings" — i.e. the MIOpen fallback ([gist](https://gist.github.com/danielrosehill/33575cb99efb05df801374ceb828731a)). Isaac's 1.5x real time on the 9070 XT with cudnn disabled is better than any public AMD number. devnen's server still says "ROCm only supports Linux - use CPU mode on Windows"; that statement is stale.
- **Licence:** MIT (code and weights). Distribution fine. Outputs carry a Perth watermark.
- **Verdict:** working; keep. Nothing to change.

### 2.2 Qwen3-TTS (Alibaba) — best candidate for voice DESIGN
- **What:** 0.6B and 1.7B models in three flavours: *Base* (3 s clone), *CustomVoice* (9 presets + instructions), *VoiceDesign* (voice from a natural-language description — exactly the "eight-foot giant, low, raspy, slow" use case). 10 languages incl. English. Apache-2.0 ([repo](https://github.com/QwenLM/Qwen3-TTS)).
- **Under the hood:** Qwen3 LM emitting 12 Hz codec tokens + a conv-based codec decoder; the `qwen-tts` package pins `transformers==4.57.3`, `accelerate==1.12.0`, no torch pin, `onnxruntime`, `sox` ([pyproject](https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/pyproject.toml)). Flash-attn is optional: "flash-attn not installed, will only run the manual PyTorch version" ([#41](https://github.com/QwenLM/Qwen3-TTS/issues/41)).
- **AMD evidence:** the strongest of any engine here. Linux 7800 XT: CustomVoice "fully working", Base hung silently in the speaker encoder on torch 2.8+rocm6.4 ([#93](https://github.com/QwenLM/Qwen3-TTS/issues/93), unresolved). **Windows gfx1200:** works but decoder RTF ≈ 12.6 because of the MIOpen naive-conv path ([TheRock #3077](https://github.com/ROCm/TheRock/issues/3077)). **Windows 9070 XT:** runs inside voicebox on torch 2.12+rocm7.14 ([voicebox #918](https://github.com/jamiepine/voicebox/issues/918)); a [Pinokio "Qwen3-TTS (AMD GPU)"](https://beta.pinokio.co/apps/github-com-trevortai-qwen3-tts-amd) package exists. A ROCm docker fork exists for Linux ([antonsokolskyy](https://github.com/antonsokolskyy/Qwen3-TTS-Openai-Fastapi-Rocm)).
- **Fix:** `torch.backends.cudnn.enabled=False` before load; load with `attn_implementation="sdpa"`, `dtype=torch.bfloat16`; `HIP_VISIBLE_DEVICES` if the iGPU is enumerated. Separate venv (transformers 4.57.3 vs Chatterbox's 5.2.0). [verified 12 Sep 2026 via the GitHub API — #3077 is still open with 9 comments and the cudnn trick *is* in the thread: rodial (25 Jan 2026) "reduced the generation time from 40+ seconds to 6 seconds (11-word phrase)"; astrelsky's reply that this "just forces the use of naive solvers which is worst case scenario" — it removes the 30-minute solver search, not the slow kernel; gtherond (31 Mar 2026, **RX 9070 XT**, Linux, Fish Speech DAC) "goes from ConvDirectNaive (7.98s) to GEMM kernels (0.23s)" with imagilux/miopen-conv-fix; Supreme-Commander-droit (13 Jun 2026, **RX 9070 XT**, Fedora) `MIOPEN_FIND_MODE=2` → RTF 0.7–0.9, with the caveat that the Windows reporter saw that variable ignored. Also verified: trevortai/Qwen3-TTS-AMD lists "AMD Radeon RX 9000 series (RDNA 4)", Windows 11, "AMD Adrenalin driver 26.2.2 or later", Python 3.12, `MIOPEN_GEMM_ENFORCE_BACKEND=hipblaslt` "~3x speedup", R9700 (gfx1201) ~67 s cold → ~11–13 s — but it targets the older 7.2.1 "PyTorch on Windows" stack; do not let it replace the torch 2.13+rocm10 wheel. voicebox #918 (19 Jul 2026, closed) is a full Windows 11 + RX 9070 XT + ROCm 7.14 guide with Qwen-TTS running.]
- **VRAM:** ~3 GB (0.6B) / ~6 GB (1.7B). Speed on NVIDIA RTF ≈ 0.9 without flash-attn; expect 1–3x real time here once the conv path is fixed.
- **Verdict:** very likely to run; first thing to install.

### 2.3 VoxCPM2 (OpenBMB) — second candidate for voice DESIGN, and clean licence
- **What:** 2B tokenizer-free diffusion-autoregressive TTS, 48 kHz, 30 languages; "create a brand-new voice from a natural-language description alone" plus cloning with style control. Apache-2.0 ([repo](https://github.com/OpenBMB/VoxCPM)). Also VoxCPM1.5 (0.6B, 44.1 kHz).
- **Under the hood:** pure PyTorch; `torch>=2.5`, `torchaudio>=2.5`, `transformers>=4.36.2`, `torchcodec` ([pyproject](https://raw.githubusercontent.com/OpenBMB/VoxCPM/main/pyproject.toml)); `torch.compile` + CUDA graphs are used when `optimize=True`.
- **CUDA-only:** the `optimize=True` path (CUDA graphs); `torchcodec` has no ROCm build.
- **AMD evidence:** WSL2 + ROCm 7.2.1 on a 7800 XT, torch 2.9.1 — worked with two changes ([#203](https://github.com/OpenBMB/VoxCPM/issues/203)), and the project's own FAQ now documents them: "start by disabling torch.compile first"; "ROCm under WSL2 requires two workarounds: monkey-patching `torchaudio.load_with_torchcodec` ... and disabling `torch.compile` via `optimize=False`" ([FAQ](https://voxcpm.readthedocs.io/en/latest/faq.html)).
- **Fix:** `VoxCPM.from_pretrained("openbmb/VoxCPM2", optimize=False)` (CLI `--no-optimize`); either `torchaudio.set_audio_backend("soundfile")` or the monkeypatch from #203:
  ```python
  import torchaudio
  torchaudio.load_with_torchcodec = lambda p,*a,**k: torchaudio.load(p,*a,**k)
  torchaudio.save_with_torchcodec = lambda p,t,sr,*a,**k: torchaudio.save(p,t,sr,*a,**k)
  ```
  plus the cudnn switch. Python <3.13.
- **VRAM:** ~8 GB (VoxCPM2), ~6 GB (1.5). NVIDIA RTF 0.30 with compile; expect ~1x real time or slower here without compile.
- **Verdict:** likely to run (nobody has tried native Windows ROCm, but the two known blockers are documented and patchable). [verified 12 Sep 2026: README "Weights and code released under the Apache-2.0 license, free for commercial use"; release note "[2026.04] We release VoxCPM2"; requirements "Python ≥ 3.10 (<3.13), PyTorch ≥ 2.5.0, CUDA ≥ 12.0"; #203 (7 Apr 2026, WSL2 + 7800 XT) is the only AMD report and the FAQ calls it "a community-reported path for WSL2 + ROCm ... not one of the project's primary tested environments"; the llama.cpp-omni GGUF path lists "CPU / Metal / CUDA / Vulkan".]

### 2.4 Dia 1.6B / Dia2 (Nari Labs)
- **What:** dialogue TTS with `[S1]/[S2]` tags and non-verbals; cloning from a 5–10 s prompt+transcript; "not fine-tuned on any specific voice" so voices drift between runs. Apache-2.0. Dia2-1B/2B are the streaming successors ([dia](https://github.com/nari-labs/dia), [dia2](https://github.com/nari-labs/dia2)).
- **Under the hood:** plain PyTorch encoder-decoder + DAC codec; Dia 1.6B is also in `transformers` (`DiaForConditionalGeneration`). Dia2 uses `sphn` (Rust audio), optional `--cuda-graph`.
- **CUDA-only:** none hard. Dia README: "GPU-only at present; CPU support is to be added soon"; Dia2 pyproject pins `torch>=2.8.0` from the `cu128` index, `transformers>=4.55.3`, `safetensors==0.5.3` ([dia2 pyproject](https://raw.githubusercontent.com/nari-labs/dia2/main/pyproject.toml)).
- **AMD evidence:** none. [dia #53 "ROCm support?"](https://github.com/nari-labs/dia/issues/53) has zero replies since April 2025.
- **Fix:** install without uv (`pip install git+... --no-deps`), `device="cuda"` works unchanged under HIP, cudnn off, no `--cuda-graph`.
- **VRAM:** 4.4 GB bf16 / 7.9 GB fp32 for Dia 1.6B.
- **Verdict:** plausible, untested by anyone on AMD; low effort to try because it is plain PyTorch.

### 2.5 VibeVoice 1.5B / 7B (Microsoft)
- **What:** long-form multi-speaker (up to 4 speakers, 90 min) with cloning from a reference wav. MIT licence, but the card says "limited to research purpose use" and forbids "voice impersonation without explicit, recorded consent"; an audible disclaimer and inaudible watermark are embedded ([card](https://huggingface.co/microsoft/VibeVoice-1.5B)). Microsoft removed the TTS code from GitHub on 5 Sept 2025; it lives on in `transformers>=5.3` (`AutoModelForTextToWaveform`) and the [vibevoice-community](https://github.com/vibevoice-community/VibeVoice) fork.
- **Under the hood:** Qwen2.5 LLM + diffusion head + acoustic/semantic tokenizers; plain PyTorch. `flash_attention_2` recommended; `sdpa`/`eager` work.
- **AMD evidence (Windows!):** [#185](https://github.com/microsoft/VibeVoice/issues/185) — 7900 XTX, Windows 11, ROCm torch: "taking ~53 seconds to generate 48 seconds of audio" for the 0.5B realtime model, GPU util 15–19 %, "Mem Efficient attention on Current AMD GPU is still experimental", eager ≈ 1 tok/s; no resolution. On Linux ROCm people install the Triton flash-attn with `FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"` ([HF discussion](https://huggingface.co/microsoft/VibeVoice-ASR/discussions/3)).
- **Fix:** `attn_implementation="sdpa"`, bf16, cudnn off, and verify the SDPA flash path (section 1.2). gfx1201 is an official AOTriton target, unlike the gfx1100 in #185, so it may fare better.
- **VRAM:** 1.5B ≈ 7 GB; 7B ≈ 17 GB bf16 — **7B does not fit** without bitsandbytes, which is unavailable here.
- **Verdict:** 1.5B plausible but expect slow; 7B out.

### 2.6 Zonos v0.1 (Zyphra) — transformer variant only
- **What:** 1.6B, cloning from 10–30 s, conditioning sliders for speaking rate, pitch, and emotion vector (happiness/anger/sadness/fear) — a partial "voice design" control set. Apache-2.0. ~2x real time on a 4090 ([repo](https://github.com/Zyphra/Zonos)).
- **Under the hood:** transformer *or* Mamba2 hybrid backbone + DAC-style codec; **needs `espeak-ng`** installed on Windows for phonemisation.
- **CUDA-only:** hybrid requires `mamba-ssm`, `causal-conv1d`, `flash-attn` (`uv sync --extra compile`) — none build here. The pure-PyTorch transformer backbone was merged Feb 2025 ([PR #51](https://github.com/Zyphra/Zonos/pull/51)) "without requiring the mamba-ssm dependency".
- **AMD evidence:** [#81](https://github.com/Zyphra/Zonos/issues/81) unanswered; Zyphra's only comment on HF: "When this [PR #51] is merged you should be able to run on cpu, mlx, amd, and older gpus" ([HF discussion](https://huggingface.co/Zyphra/Zonos-v0.1-hybrid/discussions/10)). No confirmed AMD run.
- **Fix:** `Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", backbone="torch")`, skip `--extra compile`, install espeak-ng and set `PHONEMIZER_ESPEAK_LIBRARY`, cudnn off. Project says Linux/macOS; Windows needs the [loscrossos](https://github.com/loscrossos/core_zonos)-style fixes.
- **VRAM:** ≥6 GB.
- **Verdict:** plausible; the transformer model is plain PyTorch, but Windows + espeak is fiddly and there is no AMD success story.

### 2.7 F5-TTS
- **What:** flow-matching TTS with zero-shot cloning; **weights CC-BY-NC** ("due to the training data Emilia"), so personal use only — no distributed audiobook ([README](https://github.com/SWivid/F5-TTS/blob/main/README.md)).
- **Under the hood:** plain PyTorch DiT + Vocos/BigVGAN vocoder (conv-heavy → MIOpen path). Python ≥3.10.
- **AMD evidence:** README has an official Linux ROCm recipe — `pip install torch==2.9.1+rocm7.2 torchaudio==2.9.1+rocm7.2 --extra-index-url https://download.pytorch.org/whl/rocm7.2` ("RDNA 3.5/4 GPUs require ROCm 7.x"). Windows: a Vega user couldn't get ROCm wheels ([#732](https://github.com/SWivid/F5-TTS/issues/732)); a 7800 XT ZLUDA attempt died on cuFFT ([#415](https://github.com/SWivid/F5-TTS/issues/415)). Also a [F5-TTS-ONNX](https://github.com/DakeQQ/F5-TTS-ONNX) port for onnxruntime (DirectML EP possible).
- **Fix:** `pip install f5-tts --no-deps` over AMD torch, cudnn off; vocoder is the slow bit — try `--vocoder_name vocos` (lighter than bigvgan).
- **VRAM:** ~4–6 GB.
- **Verdict:** likely to run; licence rules it out for distribution.

### 2.8 Fish-Speech / OpenAudio S1-mini
- **What:** 0.5B dual-AR LLM + DAC-style codec, cloning, emotion tags; **weights CC-BY-NC-SA 4.0** — personal only.
- **Under the hood:** plain PyTorch; optional `--compile` (Triton) for the LM; **hardcoded `.cuda()` calls** in `modded_dac.py`, `extract_vq.py`, `model_utils.py`.
- **AMD evidence:** the best gfx1201 datapoint of the whole survey, on Linux: [#1246](https://github.com/fishaudio/fish-speech/issues/1246) author ran it on "RX 9070 (16GB, gfx1201/RDNA4), Ubuntu 24.04 ... ROCm 7.2, PyTorch 2.11.0" after converting `.cuda()` to `.to(device)`, forcing the VQ-GAN decoder to the requested precision and shrinking the always-allocated 32768-token KV cache; issue closed as stale, PR status unknown. A [fish-speech-rocm](https://github.com/moyutegong/fish-speech-rocm) fork (WSL2/docker) and a [fish-speech-zluda](https://github.com/patientx/fish-speech-zluda) Windows fork exist.
- **Fix:** the `.cuda()` calls are harmless on HIP (`cuda` device *is* the ROCm device); the real fixes are half-precision decoder, smaller `max_seq_len`, no `--compile`, cudnn off.
- **VRAM:** ~4 GB in bf16 if the decoder isn't fp32.
- **Verdict:** likely to run (proven on the same silicon under Linux); licence is non-commercial.

### 2.9 Higgs Audio v2 / Higgs TTS 3 (Boson AI)
- **What:** v2 = 3.6B LLM + 2.2B audio dual-FFN (~5.8B total), cloning + "scene" descriptions ("SPEAKER0: feminine", room description) — a weak form of voice design. **Higgs Audio v3 TTS 4B** (June 2026, 102 languages, 21 emotion tokens, cloning) is under a "Research and Non-Commercial License"; "production ... requires a separate commercial license" with a "Free Creator Use Grant" for monetised content with attribution ([v3 card](https://huggingface.co/bosonai/higgs-audio-v3-tts-4b)). [verified 12 Sep 2026, LICENSE file §II-A: the grant names "podcasts, videos, audiobooks, social media posts" published "on channels You own or control, whether personal or commercial, including ad-supported, sponsored, subscription, or otherwise monetized"; the one requirement is a Creator Acknowledgment. A distributed audiobook is therefore **allowed** under v3 — the "non-commercial" label in the ranking table below is corrected.] v2 card now says "License: other — see LICENSE" ([v2 card](https://huggingface.co/bosonai/higgs-audio-v2-generation-3B-base)). [verified: that LICENSE file is the "BOSON HIGGS AUDIO 2 COMMUNITY LICENSE AGREEMENT" (Llama-3-style, expanded licence needed above 100,000 annual active users, attribution string required); the repo has been renamed `bosonai/higgs-tts-2-3b-base`.]
- **Under the hood:** both are in `transformers>=5.3.0` (`HiggsAudioV2ForConditionalGeneration`; v3 via `AutoModelForSeq2SeqLM`) — plain PyTorch. vLLM/SGLang are optional serving paths.
- **AMD evidence:** none in the issue trackers.
- **VRAM:** README recommends "GPU with at least 24GB memory"; community: "16 GB ... works for basic zero-shot synthesis but gets tight with cloning — 8-bit quantization helps" ([higgs-tts-3-4b discussion](https://huggingface.co/bosonai/higgs-tts-3-4b/discussions/3), one user saw 10–11 GB on a 16 GB card). 8-bit needs bitsandbytes → unavailable here; bf16 weights alone are ~10–12 GB, so short prompts only.
- **Fix:** `pip install "transformers>=5.3.0"`, `attn_implementation="sdpa"`, bf16, `device_map="cuda"`, cudnn off, keep reference clips short.
- **Verdict:** possible but marginal on 16 GB and slow; try last.

### 2.10 Kyutai TTS 1.6B and Pocket TTS — cleanest licences, no arbitrary cloning
- **What:** `kyutai/tts-1.6B-en_fr`, CC-BY-4.0. Kyutai **withheld the voice-embedding model**; voices come from [kyutai/tts-voices](https://huggingface.co/kyutai/tts-voices) — pre-made voices CC-BY-4.0 and 228 volunteer-donated voices (Unmute Voice Donation Project, June 2025–Feb 2026) released **CC0** — i.e. a consented corpus, exactly what the brief asks for. [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) (100M, MIT code) *does* clone from a wav and runs ~2.3–6x real time on CPU, six languages.
- **Under the hood:** `pip install moshi` (plain PyTorch, Mimi codec; Rust and MLX ports exist); Pocket TTS needs only CPU torch ≥2.5, Python 3.10–3.14.
- **CUDA-only:** none hard; moshi's CUDA-graph fast path is optional.
- **AMD evidence:** none found either way.
- **Verdict:** Pocket TTS will run today on CPU (no GPU questions at all); TTS-1.6B should run under ROCm but offers no cloning and no design — a voice *library*, not a voice designer. [verified 12 Sep 2026: `kyutai/tts-1.6b-en_fr` HF tag cc-by-4.0; **Pocket TTS weights (`kyutai/pocket-tts`) are CC-BY-4.0 too** — only the code is MIT; `kyutai/tts-voices` README confirms voice-donations CC0 (228 verified voices, 456 WAVs = raw + `_enhanced`), VCTK and CML-TTS CC-BY-4.0, Expresso and EARS "Non-commercial use only".]

### 2.11 Sesame CSM-1B
- **What:** conversational speech model, Apache-2.0, "not fine-tuned on any specific voice"; cloning only by context prompting.
- **Under the hood:** torchtune Llama-3.2-1B backbone + Mimi (moshi); requirements drag in `torchao`, `torchtune`, `silentcipher` (watermark) and `triton` — README: "The triton package cannot be installed in Windows. Instead use pip install triton-windows"; `NO_TORCH_COMPILE=1` is documented ([repo](https://github.com/SesameAILabs/csm)). A `CsmForConditionalGeneration` exists in transformers, which sidesteps torchtune.
- **AMD evidence:** [#86](https://github.com/SesameAILabs/csm/issues/86) is an unanswered request.
- **Verdict:** plausible via the transformers class; low priority — no design, weak cloning, dependency pile.

### 2.12 XTTS-v2 (Coqui, idiap fork)
- **What:** 17-language cloning from 6 s; **CPML 1.0 non-commercial** weights and no one left to sell a commercial licence (Coqui closed Jan 2024). Code MPL-2.0.
- **Under the hood:** GPT-2-style LM + HiFi-GAN; `coqui-tts 0.27.4` tested with "python >= 3.10, < 3.15 and PyTorch 2.2+", torch not pinned ([repo](https://github.com/idiap/coqui-ai-TTS)). DeepSpeed optional.
- **AMD evidence:** the gfx1151 report — "XTTS v2 ... 3-5x slower on GPU than CPU", `Solver <GemmFwdRest>, workspace required: 42172416, provided ptr: 0 size: 0` ([TheRock #5105](https://github.com/ROCm/TheRock/issues/5105)) — the HiFi-GAN conv path again.
- **Fix:** cudnn off, `use_deepspeed=False`.
- **Verdict:** will run; licence forbids distribution; quality is now behind the 2025–26 models.

### 2.13 Spark-TTS 0.5B
- **What:** Qwen2.5-0.5B + BiCodec; zero-shot cloning *and* controllable creation via gender / pitch / speaking-rate labels (coarse voice design). Weights **re-licensed from Apache-2.0 to CC-BY-NC-SA 4.0** "due to the licensing terms of some training data" ([card](https://huggingface.co/SparkAudio/Spark-TTS-0.5B)).
- **Under the hood:** plain PyTorch, torch ≥2.5, Python 3.12 (`unsloth` in requirements is an inference-time nuisance to strip).
- **AMD evidence:** [#53](https://github.com/SparkAudio/Spark-TTS/issues/53) (RX 5500, Windows) unanswered; Windows install corrections in [#5](https://github.com/SparkAudio/Spark-TTS/issues/5).
- **Verdict:** likely to run (small, plain), non-commercial.

### 2.14 IndexTTS-2 / 2.5 (bilibili)
- **What:** cloning with emotion control via reference audio, emotion vectors *or text description*, plus duration control; "bilibili Model Use License Agreement" (restrictive; read before distributing).
- **Under the hood:** uv-locked: `torch 2.8.*` from `cu128`, `transformers==4.52.1`, Python `>=3.10,<3.12`, optional `deepspeed==0.17.1` ([pyproject](https://raw.githubusercontent.com/index-tts/index-tts/main/pyproject.toml)). Everything else is plain PyTorch.
- **AMD evidence:** Linux 7900 XT "runs smoothly"; **Windows ROCm attempt failed** on nightly wheels (`operator torchvision::nms does not exist`, `No module named 'torch._C._distributed_c10d'`) ([#528](https://github.com/index-tts/index-tts/issues/528)). The first error is a torchvision/torch mismatch, the second is transformers 4.52 importing distributed bits that AMD's Windows build omits. [verified 12 Sep 2026: the issue is open and has one substantive reply (ljxfstorm, 13 Nov 2025): "it needs to downgrade `transformers` to 4.41.2 or upgrade to >=4.56.0. Furthermore, the `torch.distributed` module needs to be considered as an optional dependency, which needs a lot refactors." The pyproject still pins `transformers==4.52.1`, `torch==2.8.*`, `python <3.12`.]
- **Fix:** don't use `uv sync`; plain venv with AMD torch 2.13 + matching torchvision, `pip install -e . --no-deps`, newer transformers, no deepspeed, cudnn off. Python 3.11 satisfies `<3.12`.
- **Verdict:** plausible but the only Windows ROCm report is a failure; medium effort.

### 2.15 CosyVoice 2 / 3 (FunAudioLLM)
- **What:** Qwen-based LM + flow-matching + HiFT vocoder; cloning, instruct control (emotion/dialect via text), Apache-2.0.
- **Under the hood:** heavy dependency tree: `pynini`/`WeTextProcessing` (conda-forge only on Windows), `onnxruntime-gpu`, `ttsfrd` binary, optional `deepspeed`, TensorRT/vLLM paths.
- **AMD evidence:** AMD's own engineer published a Linux ROCm recipe (conda env from `cosyvoice-env.yml`, then `conda install -c conda-forge pynini==2.1.5`) ([Medium](https://medium.com/@alexhe.amd/play-cosyvoice-on-amd-rocm-gpu-459c942f7214)); [#839 "Why not supporting AMD?"](https://github.com/FunAudioLLM/CosyVoice/issues/839) is empty and stale.
- **Fix:** conda for pynini, `onnxruntime` CPU instead of `-gpu`, no deepspeed/TRT, `load_jit=False, load_trt=False, load_vllm=False`, cudnn off.
- **Verdict:** possible on Linux, painful on Windows; skip unless the others fail.

### 2.16 Orpheus 3B (Canopy Labs)
- **What:** Llama-3.2-3B emitting SNAC tokens; 8 named voices, `<laugh>`/`<sigh>` tags; zero-shot cloning is weak; Apache-2.0 ([repo](https://github.com/canopyai/Orpheus-TTS)).
- **Under the hood:** `orpheus-speech` requires **vLLM** (pinned `vllm==0.7.3`) — not available here. Alternative: GGUF via llama.cpp/LM Studio plus a small SNAC decoder in torch.
- **AMD evidence:** llama.cpp HIP/Vulkan on the 9070 XT under Windows is well trodden ([ollama-rocm for gfx1201](https://github.com/xnyzer/ollama-rocm)); SNAC is a tiny conv net (MIOpen caveat, cudnn off or run it on CPU).
- **Verdict:** viable only through the llama.cpp path (~8 GB VRAM at Q8); no design, poor cloning — low priority for this use case.

### 2.17 Kokoro 82M — already running
- **Under the hood:** StyleTTS2-derived, iSTFTNet vocoder; PyTorch or ONNX.
- **AMD evidence:** PyTorch-ROCm path slower than CPU on a 6800 XT with the same `GemmFwdRest ... provided ptr: 0` warnings ([hexgrad/kokoro #50](https://github.com/hexgrad/kokoro/issues/50)). kokoro-onnx on CPU at 5x real time is the right choice; DirectML EP is the only GPU route on Windows worth trying and gains little at this size.
- **Licence:** Apache-2.0. No cloning; 50 preset voices only.
- **Verdict:** keep as the fast, flat engine.

---

## 3. Ranking for this box

| # | Engine | Will it run here? | Speed expectation | Design / clone | Licence for a distributed audiobook |
|---|---|---|---|---|---|
| 1 | Chatterbox (Turbo/std) | **Running** | 1.5x RT | clone | MIT — yes |
| 2 | Kokoro (ONNX CPU) | **Running** | 5x RT | neither | Apache — yes |
| 3 | Qwen3-TTS 0.6B/1.7B VoiceDesign + Base | Very likely (Windows ROCm reports exist) | ~1–3x RT after cudnn fix; 12x RTF without | **design + clone** | Apache — yes |
| 4 | VoxCPM2 | Likely (WSL-ROCm recipe, documented flags) | ≤1x RT without compile | **design + clone** | Apache — yes |
| 5 | Dia 1.6B | Plausible, untested on AMD | ~1x RT | clone (unstable voices) | Apache — yes |
| 6 | Fish-Speech / S1-mini | Likely (ran on RX 9070 Linux) | ~1x RT | clone + emotion | CC-BY-NC-SA — personal only |
| 7 | F5-TTS | Likely (official Linux ROCm recipe) | ~1x RT | clone | CC-BY-NC — personal only |
| 8 | Zonos transformer | Plausible (pure-torch backbone) | ~1x RT | clone + emotion/pitch/rate sliders | Apache — yes |
| 9 | VibeVoice 1.5B | Plausible, slow on Windows AMD | <1x RT | clone, long-form | MIT but "research purpose" |
| 10 | Kyutai TTS-1.6B / Pocket TTS | Pocket: yes (CPU); 1.6B: plausible | Pocket 2–6x RT on CPU | Pocket: clone; 1.6B: consented library only | CC-BY-4.0 / CC0 voices — yes |
| 11 | Spark-TTS | Likely | ~2x RT | coarse design (gender/pitch/rate) + clone | CC-BY-NC-SA — personal only |
| 12 | XTTS-v2 | Will run | ~1x RT | clone | CPML — personal only |
| 13 | IndexTTS-2.5 | Plausible; one Windows-ROCm failure on record | ~1x RT | clone + emotion text | bilibili licence — read it |
| 14 | Sesame CSM | Plausible via transformers | ~1x RT | weak | Apache — yes |
| 15 | Higgs Audio v2 / v3 | Marginal on 16 GB, no 8-bit | slow | clone + scene text | v3: yes for a self-published audiobook via the Creator Use Grant (attribution) [verified]; v2: Community licence, yes with attribution |
| 16 | CosyVoice 2/3 | Possible, dependency pain | ~1x RT | clone + instruct | Apache — yes |
| 17 | Orpheus 3B | Only via llama.cpp GGUF | ~1x RT | presets, weak clone | Apache — yes |

**The recipe that makes most of them work** (same three lines every time):
```powershell
python -m venv .venv-<engine>; .\.venv-<engine>\Scripts\activate
python -m pip install --index-url https://stable.repo.amd.com/rocm/whl-next/ "torch[device-gfx1201]==2.13.0+rocm10.0.0" torchaudio
pip install <engine> --no-deps        # then pip install the rest of its requirements minus torch/flash-attn/vllm/deepspeed/bitsandbytes/torchcodec
```
and in the entry script, before any model loads:
```python
import torch
torch.backends.cudnn.enabled = False                 # bypass MIOpen conv path on gfx1201/Windows
# model = X.from_pretrained(..., attn_implementation="sdpa", dtype=torch.bfloat16)
# env: HIP_VISIBLE_DEVICES=0  ROCBLAS_USE_HIPBLASLT=0  (and TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1 only if the SDPA probe fails)
```

**Suggested order of attack:** Qwen3-TTS VoiceDesign (the only engine that does the "describe the giant" job with Apache weights and a Windows-ROCm track record) → VoxCPM2 (second design engine, 48 kHz, clean licence) → Dia (Apache, cheap to test) → Zonos transformer (emotion sliders) → the non-commercial trio (Fish, F5, Spark) for personal-listening comparisons only.
