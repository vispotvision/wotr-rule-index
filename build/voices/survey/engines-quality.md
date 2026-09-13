# Local TTS engines for expressive narration — quality-first survey

Snapshot: 12 September 2026. Target box: Windows 11, Ryzen 7 7800X3D, 64 GB RAM, Radeon RX 9070 XT 16 GB (gfx1201), AMD's native Windows PyTorch (`torch 2.13+rocm10.0.0` from `stable.repo.amd.com/rocm/whl-next/`). Known limits of that stack: MIOpen conv/batch-norm kernels fail to compile (run with `torch.backends.cudnn.enabled = False`), and nothing that needs CUDA-only extensions (flash-attn, bitsandbytes, vLLM, SGLang, mamba-ssm, DeepSpeed) will load. So the test for every engine below is: **does it have a plain-PyTorch/Transformers path, and does it fit in 16 GB without a CUDA quantiser?**

Sources are the model cards, GitHub READMEs and issue trackers linked inline; leaderboard numbers are from Artificial Analysis' Speech Arena (open-weights view) and the July/August 2026 snapshots that quote it. Nothing here is from memory.

---

## 1. Where the field stands (Sept 2026)

**The blind-vote leaderboard.** Artificial Analysis' [open-weights Speech Arena](https://artificialanalysis.ai/text-to-speech/leaderboard/provider-voice/open-weights) currently reads: Breeze TTS 2 (BreezeBlue) 1202 Elo, Fish Audio S2 Pro 1120, Step Audio EditX 1099, Voxtral TTS 1073, Kokoro 82M 1061, Magpie-Multilingual 357M 1060. A July 2026 write-up ([Luke Oliff, 23 Jul 2026](https://dev.to/lukeocodes/open-weights-are-eating-ai-here-are-the-7-best-open-tts-models-and-the-gap-nobody-mentions-13ck)) had Step Audio EditX 1118, Fish S2 Pro 1110, Voxtral 1077, Kokoro 1060, Maya1 1053, Magpie 1048, Chatterbox 1011, and the May 2026 snapshot preserved by [offlinetts](https://offlinetts.com/blog/tts-arena-leaderboard-2026/) puts Zonos at 1000, VibeVoice-7B 960, XTTS-v2 886, StyleTTS2 879. The best open model sits roughly 100–120 Elo below the closed leaders (Qwen-Audio-3.0-TTS-Plus / Speechify Simba ~1235), which that article calls "a clearly audible difference in naturalness and prosody."

**Two caveats that matter for this project.** (1) The arena "does not test voice cloning — it evaluates default voices only" (offlinetts). Several engines that matter most for *designed* voices (Qwen3-TTS, VoxCPM2, IndexTTS-2.5, MOSS-TTS, Higgs v3) are simply not on the board. (2) Elo measures short generic prompts, not a ten-minute fantasy chapter with a giant, a priest and a child talking. Word-error-rate benchmarks (Seed-TTS-eval) are the other public evidence: on the English test, MOSS-TTS 1.84 WER, VoxCPM2 1.84 WER / 75.3 % speaker similarity, Qwen3-TTS-1.7B-Base 1.24, Fun-CosyVoice3-0.5B-RL 1.68 (each from its own README).

**Community consensus, as far as it is visible.** LocalLLaMA feedback on IndexTTS-2 called it "The most realistic and expressive TTS model" and "Speech quality so good you could watch an entire movie or TV show with this dubbing" (quoted via [dev.to review](https://dev.to/czmilo/indextts2-comprehensive-review-in-depth-analysis-of-2025s-most-powerful-emotional-speech-1m9e)). Chatterbox remains "the most popular model on the leaderboard after Kokoro" with 26k stars and a July 2026 commit. Fish S2 Pro is the "quiet favorite among self-hosters." For voice *design* from a description, the engines people actually use are Qwen3-TTS-VoiceDesign, VoxCPM2, Maya1 and now Breeze TTS 2.

**The one-stop shop.** The ComfyUI custom node [TTS Audio Suite v5.8.10](https://github.com/diodiogod/TTS-Audio-Suite) wraps 19 engines (F5-TTS, Chatterbox, VibeVoice, Higgs Audio 2 and v3, IndexTTS 2/2.5, CosyVoice3, Qwen3-TTS, Step Audio EditX, Fish Audio S2 Pro, MOSS-TTS, OmniVoice, …) with `[CharacterName]` switching, `[pause:1s]` tags and per-engine emotion syntax. Isaac already has ComfyUI wired up via MCP, so it is the fastest way to A/B engines — but it is CUDA-first; no AMD notes, and its Fish S2 Pro NF4 option needs bitsandbytes.

---

## 2. The Windows-ROCm filter

What the AMD stack rules out: **Voxtral TTS** (vLLM-Omni only; the Transformers PR is still pending — a [pure-C port](https://github.com/mudler/voxtral-tts.c) exists), **MisoTTS 8B** (24 GB bf16), **Fish S2 Pro unquantised** (docs say "24GB (Inference)"; one tester saw "close to 17 GB" on a 48 GB card; the 12 GB path is bitsandbytes NF4), **VibeVoice-7B** (~19 GB bf16; low-VRAM forks are 4-bit CUDA), **Zonos hybrid** (mamba-ssm), and **Orpheus via vLLM** (use its GGUF/llama.cpp path instead).

What is proven on this exact GPU: **Qwen3-TTS** — a Pinokio package, [Qwen3-TTS-AMD](https://github.com/trevortai/Qwen3-TTS-AMD), lists "AMD Radeon RX 9000 series (RDNA 4)" as supported on Windows 11 with "AMD Adrenalin driver 26.2.2 or later", Python 3.12, and recommends `MIOPEN_GEMM_ENFORCE_BACKEND=hipblaslt` ("~3x speedup"); a YouTube demo runs it on a "9070XT ROCM 7.2 Windows 11" setup. **Chatterbox** is already running here; [Chatterbox-TTS-Server](https://github.com/devnen/Chatterbox-TTS-Server)'s RDNA4 notes add "`ROCBLAS_USE_HIPBLASLT=0` (required for stability on gfx1201)" and "no `HSA_OVERRIDE_GFX_VERSION` needed. Setting it when the GPU is natively detected may cause crashes."

What is plausible but unproven: everything that is pure PyTorch/Transformers and under ~12 GB bf16 (IndexTTS-2.5, VoxCPM2, Maya1, Higgs v3, Breeze TTS 2 eager path, Step-Audio-EditX, VibeVoice-1.5B, Dia2, F5-TTS, Kyutai TTS, MOSS-TTS-Local 4B, MOSS-VoiceGenerator 1.7B, Spark-TTS, CosyVoice3). The one documented failure is IndexTTS [issue #528](https://github.com/index-tts/index-tts/issues/528): a 7900XT user who runs it fine on Ubuntu tried a ROCm nightly on Windows and hit "operator torchvision::nms does not exist" and "No module named 'torch._C._distributed_c10d'" — a mismatched-torchvision problem, not a model problem. [verified: one reply (ljxfstorm, 13 Nov 2025) says transformers must be 4.41.2 or >= 4.56.0 and `torch.distributed` would need to become optional; issue still open.] Expect the same class of issue anywhere a repo pins its own torch: install the repo, then force-reinstall torch/torchaudio/torchvision from the AMD index as a matched set.

---

## 3. Engine by engine

### Tier A — quality ceiling (slow, big, best listening)

**Fish Audio S2 Pro** — [github.com/fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) · [HF](https://huggingface.co/fishaudio/s2-pro)
- What: 5B dual-autoregressive (4B slow AR + 400M fast AR), 10-codebook RVQ at ~21 Hz, 80+ languages, released March 2026. Arena 1120–1129 Elo, #1–2 open-weight.
- Licence: code **and** weights under the "FISH AUDIO RESEARCH LICENSE" — "Research and non-commercial use is permitted free of charge. Commercial use requires a separate license." Personal listening fine; **not** for a distributed audiobook without their licence.
- Voices: cloning from "short reference samples (typically 10-30 seconds)"; "multi-speaker multi-turn generation"; no description-based design.
- Expression: "15,000+ Unique Tags" free-form in brackets — `[whisper in small voice]`, `[professional broadcast tone]`, `[pitch up]`, `[laughing]`, `[singing]`. One local tester: "Voice cloning quality is very high" but tags "sometimes work and sometimes they are missed, including pauses" and "Speed is the main drawback."
- VRAM/speed: docs list "24GB (Inference)"; RTF 0.195 on an H200. Community NF4 gets it to 12 GB but that is bitsandbytes/CUDA. ROCm is supported via `Dockerfile.rocm` on Linux only; "Linux, WSL" are the official OSes.
- Install: `uv sync --python 3.12 --extra cu129` (Linux/WSL).
- Verdict here: **out of reach on a 16 GB Windows-ROCm box** unless someone ships a ROCm-safe 8-bit path; worth re-checking quarterly because it is the quality reference.

**Breeze TTS 2** — [github.com/breezeblue-ai/breeze-tts](https://github.com/breezeblue-ai/breeze-tts) · [HF](https://huggingface.co/BreezeBlue/Breeze-TTS-2)
- What: 3B seq2seq (text encoder, backbone, depth decoder, codec), weights released 25 Aug 2026; now **#1 open-weight at 1202–1215 Elo**, "surpassing Fish Audio S2 Pro by 90 Elo points" (Artificial Analysis). English + Chinese officially, "50 languages" claimed.
- Licence: code Apache-2.0; weights "governed separately by the BreezeBlue Research and Non-Commercial License." Personal fine; distributed audiobook no.
- Voices: three modes — clone (reference wav + exact transcript), **design from a description** (`--instruction "A warm, thoughtful young woman with a clear voice and a calm, reflective delivery." --cfg-scale 4`), and "Voice Direction" (clone plus steer "tone, emotion, pace, and delivery"). Inline paralinguistics like `(sigh)`.
- VRAM/speed: "approximately 7.7 GiB for eager inference or 14.4 GiB with `--fast-all`"; RTF 0.32 on H100. README says "CUDA-capable NVIDIA GPU required" and Linux, but the eager path is plain PyTorch.
- Install: `git clone … && pip install -r requirements.txt`, then `python infer.py ../breeze-tts-2 --text … --instruction …`.
- Verdict: **the current quality leader with real voice design; plausible on ROCm via the eager path** (7.7 GiB). Top candidate to try first among the slow tier.

**Higgs Audio v3 TTS (4B)** — [github.com/boson-ai/higgs-audio](https://github.com/boson-ai/higgs-audio) · [HF](https://huggingface.co/bosonai/higgs-audio-v3-tts-4b)
- What: 4B chat-native TTS released 4 June 2026, 102 languages (85 with WER/CER < 5), "Emergent TTS overall win-rate 53.65 %" vs baselines. Predecessor Higgs Audio v2 (3B base, EmergentTTS-Eval "75.71 %" win on emotions vs gpt-4o-mini-tts) is still up as `higgs-tts-2-3b-base`.
- Licence: code Apache-2.0. **v3 weights**: "Boson Higgs TTS 3 Research and Non-Commercial License"; production/hosted use needs a commercial licence. [verified 12 Sep 2026 against the LICENSE file in `bosonai/higgs-audio-v3-tts-4b`: Section II-A "CREATOR USE GRANT (FREE FOR DIGITAL CREATORS)" explicitly covers "using the Higgs Materials to generate audio for creative works — including podcasts, videos, **audiobooks**, social media posts, and similar creative content — and publishing and monetizing that content on channels You own or control", with one requirement, a "Creator Acknowledgment" of Boson AI's Higgs Audio. What it does *not* cover is hosting the model as a service or redistributing the weights. So a self-published audiobook, free or paid, is allowed under v3 with attribution; the earlier "no" in the table below was wrong.] **v2 weights**: "BOSON HIGGS AUDIO 2 COMMUNITY LICENSE" (Llama-style; commercial OK under 100 000 annual active users, must display "Built with Higgs Materials licensed from Boson AI USA, Inc.") [verified: LICENSE file in `bosonai/higgs-tts-2-3b-base`, the renamed v2 repo] — both are distributable for this use; v3 is the better model.
- Voices: zero-shot cloning ("Supplying the reference transcript materially improves cloning fidelity"); v2 has scene-description prompts ("SPEAKER0: feminine", "Audio is recorded from a quiet room") and `[SPEAKER*]` multi-speaker; v3 has the richest **inline tag grammar** of any engine: `<|category:value|>` mid-utterance — 21 emotions (elation, amusement, contemplation, awe, longing, anger, fear, disgust, bitterness, sadness, shame, helplessness…), style (singing/shouting/whispering), prosody (very_slow…very_fast, pitch low/high, pauses, expressiveness), sfx (cough, laughter, crying, screaming, sigh…). Example: `<|emotion:amusement|><|prosody:expressive_high|>Wait, wait...`.
- VRAM: Boson staff: "weights alone are ~10 GB … roughly 16 GB of VRAM as a practical minimum, and 24 GB for comfortable headroom"; "16 GB cards … work for basic zero-shot synthesis but get tight with cloning — 8-bit quantization helps here." The ComfyUI node reports "roughly 11 GB VRAM … with bf16 on CUDA."
- Install: official is `sgl-omni serve` (SGLang-Omni, "doesn't play nice with consumer GPUs"), but a Transformers pipeline exists (`pip install 'transformers>=5.3.0'`) and the ComfyUI nodes use it.
- Verdict: **best tag-driven expression control; plausible on ROCm via Transformers, tight at 16 GB when cloning.** Use v2 if the output must be distributable.

**Step-Audio-EditX (3B)** — [github.com/stepfun-ai/Step-Audio-EditX](https://github.com/stepfun-ai/Step-Audio-EditX)
- What: 3B LLM-based RL audio *editing* model with zero-shot TTS; open-sourced 12 Nov 2025, updated 29 Jan 2026. Arena 1099–1118 (#2–3 open-weight). Languages: Mandarin, English, Sichuanese, Cantonese, Japanese, Korean.
- Licence: code Apache-2.0. [verified 12 Sep 2026: the README's "License Agreement" section says only "The code in this open-source repository is licensed under the Apache 2.0 License"; the HF model card `stepfun-ai/Step-Audio-EditX` carries **no licence tag and no LICENSE file** — the weights have no stated licence at all. Do not treat them as Apache; treat them as unlicensed until StepFun says otherwise.]
- Voices: clone from a reference prompt, then **iteratively edit** the result: emotion tags (happy, angry, sad, fear, surprised, confusion, empathy, embarrass, excited, depressed, admiration, coldness, disgusted, humour), style tags including **"child", "older", "girl", "whisper", "exaggerated", "ethereal", "recite"** — the closest thing to "seventy-year-old priest in a young body" as a knob — and paralinguistics `[sigh] [inhale] [laugh] [chuckle] [exhale] [clears throat] [breath] [uhm]`. No pure text-to-voice design.
- VRAM: "12 GB" critical, "16GB GPU memory shoule be safer"; NVIDIA/CUDA stated; `uv sync`.
- [verified 12 Sep 2026: the official inference path is **vLLM-only** — `model_loader.py` opens with "Unified model loading utility using vLLM for high-performance inference" and `from vllm import LLM, SamplingParams`; `pyproject.toml` hard-depends on `vllm` pinned to a manylinux wheel URL, plus `torchcodec>=0.9.1`, Python >= 3.12, and the README says "Tested operating system: Linux". There is no transformers loader in the repo. vLLM does not exist for Windows ROCm (see engines-rocm.md §1.4).]
- Verdict: **struck for this box.** Unlicensed weights plus a vLLM-only runtime. The only route would be a third-party reimplementation (TTS-Audio-Suite wraps it; its AMD status is unknown) — not worth an evening. IndexTTS-2.5 covers the "emotion surgery" slot.

### Tier B — designed voices and controllability (the sweet spot for this box)

**Qwen3-TTS (0.6B / 1.7B; Base, CustomVoice, VoiceDesign)** — [github.com/QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)
- What: Alibaba's series released 22 Jan 2026, 10 languages, Apache-2.0 code and weights. Seed test-en WER 1.24 (1.7B-Base).
- Voices: **VoiceDesign** model takes a free-form description ("Speak in an incredulous tone, but with a hint of panic beginning to creep"; the Chinese sample designs a high-pitched childlike girl); **Base** clones from 3 s; **CustomVoice** has 9 presets (Vivian, Serena, Uncle_Fu, Dylan, Eric, Ryan, Aiden, Ono_Anna, Sohee) with instruction-following style control.
- VRAM/speed: ~4.5 GB weights, 6–8 GB in use. Slow: HF discussion #18 reports "RTF of x3", "GPU utilization (~12%)", RTF 4.0 on a 3080M "with super nice quality"; FA2 barely helps.
- Install: `pip install -U qwen-tts`; on this box the Pinokio [Qwen3-TTS-AMD](https://github.com/trevortai/Qwen3-TTS-AMD) package is the proven route.
- Verdict: **the proven-on-9070XT voice-design engine. Start here for the giant / priest / girl trio.** Expect 2–4× slower than real time.

**VoxCPM2 (2B)** — [github.com/OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM) · [HF](https://huggingface.co/openbmb/VoxCPM2)
- What: tokenizer-free, 48 kHz, 30 languages, released April 2026; Apache-2.0 weights and code, "free for commercial use." Seed-TTS-eval EN 1.84 WER / 75.3 % SIM. (VoxCPM1.5, 0.8B, 44.1 kHz, Dec 2025, is the stable fallback.)
- Voices: design "from a natural-language description" with the description in parentheses before the text — `(A young woman, gentle and sweet voice)Hello…`; cloning with style control — `(slightly faster, cheerful tone)This is a cloned voice…`. Card warns "Voice Design and Style Control results may vary between runs; generating 1–3 times is recommended."
- VRAM/speed: "~8 GB"; RTF ~0.30 on a 4090 (0.13 with Nano-vLLM, which is CUDA).
- Install: `pip install voxcpm` (Python 3.10–3.12, PyTorch ≥ 2.5). Pure PyTorch.
- Verdict: **best-licensed voice-design engine, highest sample rate; plausible on ROCm.** Second thing to try.

**IndexTTS-2.5** — [github.com/index-tts/index-tts](https://github.com/index-tts/index-tts) · [HF](https://huggingface.co/IndexTeam/IndexTTS-2.5)
- What: bilibili's zero-shot TTS; 2.0 on 8 Sep 2025, 2.5 on 10 Aug 2026 adding Japanese/Spanish/Arabic, speed control and faster inference (RTF 0.2065 on a 4090 bf16 vs 0.3257 for 2.0).
- Licence: "bilibili Model Use License Agreement" — commercial use allowed unless you exceed 100 M MAU or RMB 1 bn revenue; forbids using it "to improve any AI model" other than non-commercial ones; attribution required. Fine for a hobbyist audiobook.
- Voices: clone from one reference clip; **emotion disentangled from timbre** — steer with a second emotion-reference clip, an 8-float vector `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]`, or a text description via a bundled Qwen3 (`use_qwen_emo=True`); `duration_factor` 0.5–2.0. No description-only voice design.
- VRAM: "roughly 6 GB."
- Install: `uv sync --all-extras` (drop `--all-extras` on Windows to skip DeepSpeed). ROCm-on-Windows attempt failed on torch/torchvision mismatch (#528), fixable in principle. [verified 12 Sep 2026: #528 is still open and *did* get a reply — ljxfstorm, 13 Nov 2025: "it needs to downgrade `transformers` to 4.41.2 or upgrade to >=4.56.0. Furthermore, the `torch.distributed` module needs to be considered as an optional dependency, which needs a lot refactors." The pyproject still pins `transformers==4.52.1`, which is exactly the broken range, so a plain venv with transformers >= 4.56 is mandatory, not optional.]
- Verdict: **the emotion-control engine the community rates highest for drama; 6 GB; try after the torch reinstall trick.**

**Maya1 (3B)** — [HF maya-research/maya1](https://huggingface.co/maya-research/maya1)
- What: Llama-3B backbone + SNAC 24 kHz decoder, Nov 2025, Apache-2.0, English only (multi-accent). Arena 1050–1053.
- Voices: **description-first design** — `<description="40-year-old, warm, low pitch, conversational">` ("as if you were briefing a voice actor": age, accent, pitch, timbre, pacing); 20+ inline emotion tags `<laugh> <sigh> <whisper> <angry> <giggle> <chuckle> <gasp> <cry>`…
- VRAM: card says "16GB+" for the vLLM path; the Transformers path (`pip install torch transformers snac soundfile`) with a 3B bf16 model is ~7 GB.
- Verdict: **simplest pure-Transformers voice-design engine; plausible on ROCm; English-only is fine here.**

**MOSS-TTS family (OpenMOSS)** — [github.com/OpenMOSS/MOSS-TTS](https://github.com/OpenMOSS/MOSS-TTS)
- What: Apache-2.0 family, 31 languages: MOSS-TTS-v1.5 (8B, Seed EN WER 1.84), **MOSS-TTS-Local-Transformer-v1.5 (4B, 18 Jun 2026, native 48 kHz stereo)**, MOSS-TTSD-v1.0 (8B dialogue; the team says it beat "Doubao and Gemini 2.5-pro in subjective evaluations"), **MOSS-VoiceGenerator (1.7B, voice design "directly from text prompts, without any reference speech")**, MOSS-TTS-Realtime (1.7B, 0.51 RTF), MOSS-SoundEffect-v2.0.
- Install: `pip install -e ".[torch-runtime]"` (flash-attn optional), or a torch-free `".[llama-cpp-onnx]"` path.
- Verdict: **the 4B Local model plus VoiceGenerator is a fully Apache, 48 kHz, plain-PyTorch stack that nobody on the arena has scored; worth a test.** The 8B variants are too big for 16 GB in bf16. [verified 12 Sep 2026: repo LICENSE is Apache-2.0 and every HF card checked (`MOSS-VoiceGenerator`, `MOSS-TTS-Local-Transformer-v1.5`) is tagged apache-2.0. VoiceGenerator is listed as **1.7B** in the README model table (the HF card's parameter counter rounds to 2B). README news 2026-03-10: "Significantly optimized the VRAM usage of llama.cpp inference pipeline. Now 8B model fits onto 8GB GPUs!" — so MOSS-TTSD 8B is reachable through the torch-free `".[llama-cpp-onnx]"` path (llama.cpp Vulkan/HIP on this card), not through plain torch. `pyproject` pins `torch==2.9.1+cu128` — install `--no-deps` over the AMD wheel.]

**CosyVoice 3 (Fun-CosyVoice3-0.5B-2512)** — [github.com/FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
- Apache-2.0, Dec 2025, 9 languages + 18 Chinese dialects; instruct strings like `"You are a helpful assistant. 请用尽可能快地语速说一句话.<|endofprompt|>"`; RL variant CER 0.81 % / WER 1.68 %. Small and fast, but Linux-centred (sox, ttsfrd) and the instruction vocabulary is oriented to dialects and speed rather than character. Verdict: capable, lower priority.

**Spark-TTS (0.5B)** — [github.com/SparkAudio/Spark-TTS](https://github.com/SparkAudio/Spark-TTS) — Apache code, Mar 2025, EN/ZH; "creating virtual speakers by adjusting parameters such as gender, pitch, and speaking rate" plus zero-shot cloning. A light, attribute-based designer; no 2026 updates. Verdict: superseded by Qwen3/VoxCPM2.

### Tier C — dialogue and long-form specialists

**VibeVoice (community fork)** — [github.com/vibevoice-community/VibeVoice](https://github.com/vibevoice-community/VibeVoice)
- Microsoft released 25 Aug 2025 under MIT, pulled the repo 4–5 Sep 2025; the fork's issue #4 concludes "The fork is completely legal … since Microsoft released all code and the models under the MIT license." 1.5B: "90 minutes long with up to 4 distinct speakers"; 7B: ~45 min; Streaming-0.5B: presets only, "Voice cloning is not supported for now." Transformers integration landed 27 Aug 2026.
- VRAM: 1.5B ~7 GB; 7B ~19 GB bf16 (4-bit forks are CUDA). Arena 960 for 7B — it is a podcast engine, weaker per-line than Tier A/B. Verdict: **1.5B is viable and MIT; use for multi-voice scene passes, not for hero narration.**

**Dia 1.6B / Dia2 (1B, 2B)** — [github.com/nari-labs/dia](https://github.com/nari-labs/dia) · [Dia2](https://github.com/nari-labs/dia2)
- Apache-2.0, English only, `[S1]`/`[S2]` alternating dialogue, rich non-verbals `(laughs) (clears throat) (sighs) (gasps) (screams) (inhales)`…; Dia 1.6B ~4.4 GB bf16, "x2.1" realtime on a 4090 compiled. Dia2 (19 Nov 2025) is streaming, capped at "up to 2 minutes of generation." Core caveat, verbatim: "you will get different voices every time you run the model … keep speaker consistency by either adding an audio prompt, or fixing the seed." Verdict: fun for two-hander scenes; no stable designed voice.

**Sesame CSM-1B** — Apache-2.0, conversational, "has not been fine-tuned on any specific voice," no cloning by design. Not a narration tool. Skip.

**MisoTTS / Miso One (8B)** — [github.com/MisoLabsAI/MisoTTS](https://github.com/MisoLabsAI/MisoTTS) — June 2026, modified MIT (commercial below 50 M MAU / $10 M MRR), English, audio-context conditioning, "**24 GB**" bf16. Does not fit this card. Skip until quantised.

### Tier D — fast tier and baselines

**Chatterbox (Turbo 350M, Nano 110M, Multilingual V3 500M, original 500M)** — [github.com/resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)
- MIT code and weights; Turbo (Dec 2025) single-step decoder with `[cough] [laugh] [chuckle]` tags; Multilingual V3 (10 Jun 2026) 21 languages + 4 dialects, "Improved speaker similarity, reduced hallucinations"; ~10 s reference; `exaggeration` / `cfg_weight` knobs; Perth watermark on every file. Arena 1006–1011. Already running on this card at ~1.5× real time. Verdict: **keep as the fast cloned-voice tier.**

**Kokoro-82M v1.0** — [github.com/hexgrad/kokoro](https://github.com/hexgrad/kokoro) — Apache-2.0, 54 preset voices in 8 languages, trained on "permissive/non-copyrighted audio data" (public domain, permissive, and synthetic). Arena 1056–1061 — remarkable for 82M — but no cloning, no design, flat delivery. Already installed (kokoro-onnx CPU, 5× real time). **Baseline.**

**Kyutai TTS 1.6B (en/fr)** — [HF kyutai/tts-1.6b-en_fr](https://huggingface.co/kyutai/tts-1.6b-en_fr) — weights CC-BY-4.0, code MIT/Apache, `pip install moshi`. Deliberately **no cloning** ("pre-computed voice embeddings" only; the embedder is not released). The [tts-voices](https://huggingface.co/kyutai/tts-voices) repo is the cleanest *permissioned* voice bank in the field: 228 verified CC0 volunteer voices from the Unmute Voice Donation project (June 2025–Feb 2026), plus VCTK and CML-TTS (CC-BY-4.0), plus Expresso and EARS (CC-BY-NC-4.0 — non-commercial only). Verdict: **the ethics-clean preset library; fast; no design.**

**Pocket-TTS (Kyutai, 100M)** — [github.com/kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) — MIT code, CPU "~6x real-time" on an M4 Air, 6 languages, `--voice` accepts a wav for cloning, training code released Aug 2026. Candidate to replace Kokoro as the draft-pass engine if cloning matters.

**NeuTTS Air (Neuphonic, ~0.5B)** — Apache-2.0, 3–15 s reference, GGUF Q4/Q8, Perth-watermarked, EN/ES/DE/FR. Another fast cloning option; Nano/2E variants carry a "NeuTTS Open License 1.0."

**Orpheus-TTS 3B** — Apache-2.0, 8 presets, `<laugh> <chuckle> <sigh> <cough> <sniffle> <groan> <yawn> <gasp>`, zero-shot cloning. Default stack is vLLM but llama.cpp/GGUF is documented, which runs on this card. Multilingual is a 2025 research preview; no 2026 movement.

**NVIDIA Magpie-TTS Multilingual 357M** — NVIDIA Open Model License (commercial OK), 9 languages, 5 baked speakers, ~120 ms first packet; "removed zero-shot voice-cloning capability for security reasons." Arena 1048–1064. Voice-agent tool, not a narrator.

### Tier E — legacy / skip

**XTTS-v2** (Coqui Public Model License, non-commercial; company defunct; Arena 886; 6 s clone, 17 languages) — superseded. **MaskGCT** (weights CC-BY-NC-4.0, Oct 2024, no updates) — superseded. **F5-TTS** (code MIT, "pre-trained models are licensed under the CC-BY-NC license due to the training data Emilia"; fast diffusion, EN/ZH, `pip install f5-tts`) — still useful as a fast NC cloner but no expression control. **Zonos v0.1** (Apache; transformer variant 6 GB+, 2× realtime on a 4090; 4 emotion sliders + pitch/rate; needs espeak-ng; "experimental windows support" via a fork; no 2026 updates) — a reasonable emotion-slider engine but static since 2025. **Voxtral TTS 4B** (CC-BY-NC-4.0, 9 languages, 20 presets, 2–3 s clone, Arena 1073) — vLLM-Omni only; revisit when the Transformers PR lands.

---

## 4. Licence and provenance summary

| Engine | Code | Weights | Personal listening | Distributed audiobook |
|---|---|---|---|---|
| Breeze TTS 2 | Apache-2.0 | BreezeBlue Research & Non-Commercial | yes | **no** |
| Fish S2 Pro | Fish Research | Fish Research (non-commercial) | yes | **no** |
| Higgs v3 | Apache-2.0 | Boson Higgs TTS 3 Research & Non-Commercial | yes | **yes, under the licence's Creator Use Grant** (self-published creative content incl. "audiobooks", monetised or not, with a Creator Acknowledgment; no hosting/redistribution of the model) [verified: LICENSE §II-A]. v2 Community licence: yes, with attribution |
| Voxtral TTS | — | CC-BY-NC-4.0 | yes | non-commercial only |
| F5-TTS / MaskGCT | MIT | CC-BY-NC | yes | non-commercial only |
| XTTS-v2 | MPL | Coqui CPML | yes | **no** |
| Qwen3-TTS, VoxCPM2, Maya1, MOSS-TTS, CosyVoice3, Dia/Dia2, VibeVoice (MIT), Chatterbox (MIT), Kokoro, Orpheus, NeuTTS Air, Zonos | Apache/MIT | same | yes | yes [verified 12 Sep 2026 via HF API licence tags: Qwen3-TTS, Maya1, MOSS-VoiceGenerator, MOSS-TTS-Local-Transformer-v1.5, Dia-1.6B, Dia2-2B, Kokoro-82M, Zonos-transformer, orpheus-3b, neutts-air, csm-1b = apache-2.0; VibeVoice-1.5B, Chatterbox = mit] |
| Step-Audio-EditX | Apache-2.0 | **none stated** (no HF licence tag, README licence section covers code only) [verified] | unclear | **no** — no grant to rely on |
| Spark-TTS | Apache-2.0 | CC-BY-NC-SA 4.0 [verified: HF tag on `SparkAudio/Spark-TTS-0.5B`] | yes | **no** (moved from the Apache row; it was wrong there) |
| IndexTTS-2.5 | bilibili Model Use License | same | yes | yes (attribution; scale thresholds) |
| Kyutai TTS | MIT/Apache | CC-BY-4.0 | yes | yes — but only with CC0/CC-BY voices; Expresso/EARS voices are NC |

**Voice provenance.** "Designed or permissioned only" is satisfied by: description-designed voices (Qwen3-TTS-VoiceDesign, VoxCPM2, Maya1, Breeze TTS 2, MOSS-VoiceGenerator, Spark-TTS attributes); preset banks with stated consent (Kyutai's 228 CC0 donated voices; Kokoro's synthetic/permissive set; Qwen CustomVoice's 9 presets, Chatterbox/Orpheus presets); and cloning from *Isaac's own* recordings or a CC0 voice. Every cloning engine's card carries some form of "do not mimic real individuals without consent" (CSM, Dia2, VoxCPM2, Chatterbox's "Don't use this model to do bad things"). Chatterbox and NeuTTS embed a Perth watermark in all output; MisoTTS uses SilentCipher.

---

## 5. Recommended menu for this machine

1. **Design pass (slow, designed voices):** Qwen3-TTS-1.7B-VoiceDesign (proven on the 9070 XT) and VoxCPM2 (Apache, 48 kHz, ~8 GB) — generate 3–5 candidates per character from a description, keep the best clip as that character's *reference*.
2. **Hero narration (slow, best quality):** Breeze TTS 2 eager path (7.7 GiB; NC weights, personal use) cloning from the designed reference with `--instruction` direction [verified: `requirements.txt` is `torch==2.9.1, torchaudio==2.9.1, qwen-tts==0.1.1, transformers==4.57.3` — no flash-attn; `infer.py` loads with `attn_implementation="eager"`; it is built on the same `qwen-tts` stack as Qwen3-TTS, so once Qwen3-TTS runs here, Breeze eager very probably does too]; Higgs v3 via Transformers as the alternative when a line needs `<|emotion:…|>` / `<|sfx:…|>` control — and, because of the Creator Use Grant, Higgs v3 is the *distributable* one of the two. Both are unproven on ROCm-Windows: budget an evening each.
3. **Emotion surgery:** IndexTTS-2.5 (6 GB, 8-float emotion vector, duration control). ~~Step-Audio-EditX~~ struck: vLLM-only runtime and no weights licence [verified].
4. **Fast pass:** Chatterbox Turbo (already running, `[laugh]`/`[sigh]`) for drafts; Kokoro or Pocket-TTS on CPU for proofing.
5. **Multi-voice scene render:** VibeVoice-1.5B (MIT, 4 speakers, 90 min) or MOSS-TTSD when the 8B fits.

Re-check in three months: Fish S2 Pro ROCm-safe quantisation, Voxtral Transformers support, MOSS-TTSD 4B variant, and whether Breeze publishes a permissive licence tier.
