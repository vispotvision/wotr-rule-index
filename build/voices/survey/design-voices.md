# Voice design without a reference person — survey (12 Sep 2026)

Scope: engines that build a voice from a **text description or attribute sliders** (no reference clip), plus the **reference-shaping** side (making a permissioned clip deeper / bigger / raspier without phase-vocoder smear, and whether Chatterbox will clone the shaped clip). Everything below was read from the model cards, READMEs and issue trackers on 12 Sep 2026; quotes are verbatim. Target box: Windows 11, RX 9070 XT 16 GB (gfx1201), torch 2.13+rocm10.0.0, no CUDA, MIOpen conv path broken (cudnn disabled).

Glossary: *InstructTTSEval* is the standard benchmark for "did the model obey the voice description"; its three columns are APS (acoustic attributes such as pitch/speed/gender), DSD (descriptive style, e.g. "gruff tavern keeper") and RP (role-play, the hardest). *RTF* = real-time factor; 0.5 means 10 s of audio takes 5 s. *Formant* = the resonance peaks of the vocal tract; lowering them makes the body sound bigger, lowering only F0 (pitch) makes the voice deeper but same-sized.

---

## 1. Headline

1. **Description-to-voice is now a solved feature, not a research toy.** Four Apache-2.0 engines released in 2026 do it well: **Qwen3-TTS-1.7B-VoiceDesign** (Jan), **MOSS-VoiceGenerator** (Feb), **VoxCPM2** (Apr) and **OmniVoice** (Apr, weights CC-BY-NC). On InstructTTSEval-EN, Qwen3-VD scores APS 82.9 / DSD 82.4 / RP 68.4 and VoxCPM2 84.2 / 83.2 / 71.4 — against Parler-TTS-mini's 63.4 / 48.7 / 28.6 (the 2024 baseline). The gap between "old" and "new" description engines is not subtle.
2. **The hard part is keeping the voice.** Every description engine draws a *different* voice per run (VoxCPM2 README: "results can vary between runs — you may try to generate 1~3 times"). The working pattern, documented by Qwen users, is **design once → save the best 10–20 s → clone it forever** with the Base/clone model or with Chatterbox. Qwen discussion #220 warns the clone "loses emotional range and naturalness" relative to the pure VoiceDesign output — a real but acceptable cost for a 60-hour audiobook.
3. **On your card, Qwen3-TTS is the one with hard evidence.** RX 9070 XT owners have it running at RTF 0.71–0.94 on Linux once MIOpen's conv search is bypassed; on Windows the same issue (TheRock #3077) still shows the naive-conv fallback, and your existing "disable cudnn" trick is exactly the workaround people report (40 s → 6 s for an 11-word phrase). VoxCPM2, MOSS and OmniVoice are plain-PyTorch so should behave the same way, but nobody has posted Windows-ROCm numbers for them; VoxCPM2 and OmniVoice also have GGUF/C++ ports with **Vulkan** backends, which sidestep ROCm entirely.
4. **Reference shaping: use Praat (parselmouth) or WORLD (pyworld), not a phase vocoder.** Praat's *Change gender* does formant shift by resampling and pitch by PSOLA — no smear. Recipe for "giant": formant ratio 0.80–0.88, new pitch median 70–85 Hz, pitch range factor 0.7, duration 1.10. Rasp is not a pitch-tool job: ask the description engine for it ("hoarse", "gravelly"), or add mild saturation after synthesis.
5. **Licence map for a distributed audiobook:** Apache-2.0 (Qwen3-TTS, VoxCPM2, MOSS, Maya1, Zonos) and MIT (Chatterbox) are fine [verified 12 Sep 2026 via HF licence tags and repo LICENSE files]. **Higgs v3 is also fine** for a self-published audiobook: its "Research and Non-Commercial" licence carries a Creator Use Grant (§II-A) that names "audiobooks" explicitly, monetised or not, on channels you own, with a Creator Acknowledgment [verified: LICENSE file]. **Not fine:** Breeze TTS 2, Fish S2-Pro (research/non-commercial licences, no creator carve-out), Voxtral TTS and OmniVoice weights (CC-BY-NC), Spark-TTS weights (CC-BY-NC-SA — the code is Apache but the checkpoint is not). **Step-Audio-EditX is removed from the Apache list:** its README licenses the *code* under Apache 2.0 and says nothing about the weights; the HF card has no licence tag at all [verified]. Fine for personal listening: all of them except Step-Audio-EditX, whose weights have no stated grant.

---

## 2. Description-driven engines (no reference clip)

### 2.1 Qwen3-TTS-12Hz-1.7B-VoiceDesign — the default choice
- Repo: https://github.com/QwenLM/Qwen3-TTS · card: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign · report: https://arxiv.org/abs/2601.15621
- Released 2026-01-22 ("We have released Qwen3-TTS series (0.6B/1.7B)"), Apache-2.0, 10 languages. Three flavours: **VoiceDesign** ("Performs voice design based on user-provided descriptions"), CustomVoice (9 preset timbres + instruct), Base (3-second clone). VoiceDesign exists only at 1.7B.
- API: `model.generate_voice_design(text=..., language="English", instruct="...")`. Install `pip install -U qwen-tts`; FlashAttention 2 is *recommended*, not required — pass `attn_implementation="sdpa"`.
- Official example descriptions that work: "A calm, middle-aged male voice, with a slow pace and a deep, magnetic tone, suitable for reading news or narrating documentaries." / "A cute child's voice, around 8 years old, speaking with a slightly childish tone". A user guide (ocdevel, Mar 2026) reports gender, exact age, pitch level, pace, emotion and timbre are "reliably controllable"; accents are not ("defaults toward standard American or Chinese-accented English"), and one user complained "most of the voices have too strong a Chinese accent when speaking English."
- Benchmarks (tech report Table 8): InstructTTSEval ZH 85.2/81.1/65.1, EN 82.9/82.4/68.4 — beats GPT-4o-mini-tts (EN 76.4/74.3/54.8) and Mimo-Audio-7B, loses to Gemini-flash (EN 92.3/93.8/80.1).
- VRAM: ~4.2 GB weights at bf16; community guides say plan 6–8 GB. Easily fits 16 GB.
- **Consistency problem (the one that matters for you).** Discussion #220 (Feb 2026, still no maintainer reply): "we can only create a few minutes of audio at a time", "chunking isn't really an option because the voice changes when you do that", and when you clone the designed voice with Base, "the cloned version loses emotional range and naturalness. When used purely within Voice Design, it sounds way better." Aug 2026 follow-up: even with "the same voice, instructions, and seed", cadence and emotional delivery drift between chunks. The design-then-clone workflow:

```python
ref_wavs, sr = design_model.generate_voice_design(
    text="Some reference sentence in your target style.",
    language="English",
    instruct="A very deep, slow, gravelly male voice, an eight-foot giant, chest resonance, unhurried.")
prompt = base_model.create_voice_clone_prompt(ref_audio=(ref_wavs[0], sr),
                                              ref_text="Some reference sentence in your target style.")
wavs, sr = base_model.generate_voice_clone(text="Any new line.", language="English",
                                           voice_clone_prompt=prompt)
```
  Or hand the saved WAV to Chatterbox, which you already run.
- **Your hardware — actual reports.**
  - ROCm/TheRock #3077 (opened 2026-01-24, still open, 9 comments): RX 9060 XT (gfx1200), Windows 11, torch 2.9.1+rocmsdk: "Qwen3-TTS decoder very slow", RTF ≈ 12.6, MIOpen logs `GemmFwdRest ... provided ptr: 0 size: 0` → `ConvDirectNaiveConvFwd`. Reporter set `MIOPEN_FIND_MODE=2` on Windows and it was "not reflected".
  - Comment (rodial, 2026-01-25): "`torch.backends.cudnn.enabled = False` … reduced the generation time from 40+ seconds to 6 seconds (11-word phrase)". Comment (astrelsky): that "just forces the use of naive solvers which is worst case scenario" — i.e. it removes the *search*, not the slow kernel.
  - Comment (Supreme-Commander-droit, 2026-06-13), **RX 9070 XT, Linux**, torch nightly rocm6.4, `attn_implementation="sdpa"`: `export MIOPEN_FIND_MODE=2` + `export TORCH_BLAS_PREFER_HIPBLASLT=0` took Qwen3-TTS from "RTF ~4–57 to ~0.7–0.9 (faster than realtime)"; per-sentence compute "dropped from ~50–75 s to ~1–2 s. Audio quality unchanged." Things that did *not* help: 0.6B model, CPU, perf-DB tuning.
  - Windows one-click: https://github.com/trevortai/qwen3-tts-amd (Pinokio, "Pytorch on Windows release (7.2.1)", Python 3.12 only). On a Radeon AI PRO R9700 (also gfx1201) it reports "~67s" cold baseline → "~11-13s" with `MIOPEN_GEMM_ENFORCE_BACKEND=hipblaslt` ("~3x speedup"), `torch.compile(mode="reduce-overhead")` and a GPU keep-alive thread [verified 12 Sep 2026: README lists "AMD Radeon RX 9000 series (RDNA 4)", "Windows 11 or Linux", "AMD Adrenalin driver 26.2.2 or later (Windows) / ROCm 7.2.1 (Linux)", "Python 3.12 ... ROCm wheels are not available for other versions" — that last line is stale relative to the torch 2.13+rocm10 wheel already on this box; borrow its env vars, not its torch]. Note this contradicts the Linux advice to *disable* hipBLASLt on RDNA4 — try both.
  - gtherond (2026-03-31), RX 9070 XT, Fish Speech DAC decoder: wrote a C++ extension calling MIOpen immediate mode with a real workspace — "goes from ConvDirectNaive (7.98s) to GEMM kernels (0.23s)": https://github.com/imagilux/miopen-conv-fix (updated Jun 2026). This is the general fix for *every* conv-based codec decoder on your card (Qwen's 12 Hz tokenizer, VoxCPM's AudioVAE, SNAC, DAC).
- Verdict: **Install first.** Best-documented design engine, Apache-2.0, proven on gfx1201. Expect to spend an evening on MIOpen env vars.

### 2.2 MOSS-VoiceGenerator (OpenMOSS, Fudan) — best arena scores, fewest independent tests
- Repo: https://github.com/OpenMOSS/MOSS-TTS · card: https://huggingface.co/OpenMOSS-Team/MOSS-VoiceGenerator (Apache-2.0, Chinese + English, family launched 2026-02-10; repo pushed 2026-09-06). [verified 12 Sep 2026: HF tag apache-2.0, repo LICENSE Apache-2.0; the README model table lists MOSS-VoiceGenerator as **1.7B** (`MossTTSDelay`) — the HF parameter counter's "2B" is a rounding; requirements are Transformers 5.0.0, Python 3.12, and a `torch==2.9.1+cu128` pin to override.]
- Card: "an open-source voice design model capable of generating diverse voices and styles directly from text prompts, **without any reference speech**" and positioned "as a design layer for downstream TTS" — i.e. they intend the design-then-clone workflow.
- Example instructions on the card include exactly your kind of brief: `"疲惫沙哑的老年声音缓慢抱怨，带有轻微呻吟。"` (a tired, hoarse elderly voice, slowly complaining, with slight groaning) and `"Hearty, jovial tavern owner's voice, loud and welcoming with a slightly gruff, friendly tone in American English"`.
- Recommended decoding: `audio_temperature 1.5, audio_top_p 0.6, audio_top_k 50, audio_repetition_penalty 1.1`; the card warns it is "sensitive to decoding hyperparameters".
- Evidence: 160-sample blind preference test on Overall / Instruction Following ("gender, age, tone, emotion, accent, speed") / Naturalness — "outperforms all TTS systems that support zero predefined voices" (chart only, no numbers; no third-party InstructTTSEval run found).
- Requirements: **Transformers 5.0.0**, `pyproject` pins `torch==2.9.1+cu128` (you will have to override for ROCm), FlashAttention optional — the README's own loader falls back to SDPA: "CUDA fallback: use PyTorch SDPA kernels." VRAM not stated; 2B bf16 ≈ 4–5 GB plus codec.
- Verdict: **Second install**, specifically for the hoarse/old/tired briefs. No AMD reports at all.

### 2.3 VoxCPM2 (OpenBMB) — best EN instruction numbers, 48 kHz, has a Vulkan escape hatch
- Repo: https://github.com/OpenBMB/VoxCPM (pushed 2026-09-02) · card: https://huggingface.co/openbmb/VoxCPM2 · released 2026-04, 2B, Apache-2.0 ("free for commercial use"), 30 languages, 48 kHz output.
- Design syntax is inline: `text="(A young woman, gentle and sweet voice)Hello, welcome to VoxCPM2!"`, `cfg_value=2.0, inference_timesteps=10`. Same parentheses on top of a reference clip give *controllable cloning*: `"(slightly faster, cheerful tone)This is a cloned voice…"` with `reference_wav_path=`.
- InstructTTSEval (README table): EN **84.2 / 83.2 / 71.4** (best open figure I found), ZH 85.2 / 71.5 / 60.8. Seed-TTS-eval EN WER 1.84 %, SIM 75.3 %.
- README limitation, verbatim: "Voice Design and Controllable Voice Cloning results can vary between runs — you may try to generate 1~3 times to obtain the desired voice or style."
- VRAM "~8 GB"; RTF ~0.30 on an RTX 4090 in plain PyTorch. Stated requirement "CUDA ≥ 12.0", but the device string is just `cuda`, so ROCm torch will be tried as-is; the AudioVAE decoder is convolutional, so expect the MIOpen story again.
- **Non-ROCm route:** GGUF ports — llama.cpp-omni ("CPU / Metal / CUDA / Vulkan"), VoxCPM.cpp ("CPU, CUDA, Vulkan") and audio.cpp. Vulkan runs on your card without ROCm. Reported RTF ~1.76 at Q8_0 on an M4 Pro, so this is a "slow but certain" fallback.
- Verdict: **Third install**; the one to try if Qwen's accent bothers you.

### 2.4 OmniVoice (k2-fsa / Next-gen Kaldi) — attribute tags, tiny, ROCm and Vulkan in C++, but NC weights
- Repo: https://github.com/k2-fsa/OmniVoice (pushed 2026-09-07, 12.8k stars) · card: https://huggingface.co/k2-fsa/OmniVoice (0.6B, paper Apr 2026).
- Design is comma-separated attributes, "freely combinable": gender (male/female), age (child to elderly), pitch (very low to very high), style (whisper), accent, dialect — e.g. `"female, low pitch, british accent"`. Less expressive than free prose but *deterministic vocabulary*.
- Licence: code Apache-2.0, but "The pre-trained model is licensed under the CC-BY-NC due to constraints from its training data (e.g., Emilia)." → personal use yes, distributed audiobook no.
- https://github.com/ServeurpersoCom/omnivoice.cpp: "runs on CPU, CUDA, ROCm, Metal, Vulkan" — the only design engine with a maintained ROCm *and* Vulkan C++ path.
- Verdict: worth a look for quick prototyping of ages/pitches; not for anything you will ship.

### 2.5 Maya1 (Maya Research) — the "brief a voice actor" model, English only
- https://huggingface.co/maya-research/maya1 (Nov 2025, 3B Llama-style + SNAC 24 kHz codec, Apache-2.0, "Currently English with multi-accent support"). Training data claim: "Proprietary curated dataset of studio recordings" with "Human-verified voice descriptions" — the closest any of these comes to a consent statement. [verified 12 Sep 2026: that sentence describes the *supervised fine-tuning* set only; the same card says "Pretraining: Internet-scale English speech corpus", so the base timbres are as unconsented as everyone else's. Licence tag apache-2.0 confirmed; FAQ "Single GPU with 16GB+ VRAM" is the vLLM recommendation.]
- Prompt: `<description="40-year-old, warm, low pitch, conversational"> text` plus 20+ inline tags (`<laugh> <sigh> <whisper> <angry> <gasp> <cry>` …).
- Card says "Single GPU with 16GB+ VRAM" — that figure is for the vLLM path; the plain `AutoModelForCausalLM` path is ~6.5 GB at bf16. Artificial-Analysis arena Elo 1045 (below Kokoro's 1060, which tells you arena voters weigh naturalness over controllability).
- No AMD reports; SNAC decoder is convolutional → MIOpen caveat.
- Verdict: good for English character voices with emotion tags; a tier below Qwen/VoxCPM on instruction following in the benchmark (VoxCPM README does not list it; ocdevel and others place it mid-pack).

### 2.6 Breeze TTS 2 (BreezeBlue) — top of the arena, but NVIDIA-only and non-commercial
- https://huggingface.co/BreezeBlue/Breeze-TTS-2 · https://github.com/breezeblue-ai/breeze-tts. Released 2026-08-25, 3B, EN + ZH. Voice Design (`--instruction "A warm, thoughtful young woman with a clear voice" --cfg-scale 4`), Voice Direction (clone + instruction), inline `(sigh)`/`(clears throat)`.
- Artificial Analysis: #1 open-weight, Elo 1,215, "first open-weight model to outrank ElevenLabs Eleven v3 (1,177)".
- Blockers for you: "A CUDA-capable NVIDIA GPU", "Linux and Python 3.10 or newer" as stated; and the weights are under the "BreezeBlue Research and Non-Commercial License" — "Model weights, checkpoints, adapters, derivative models, and self-hosted outputs" are non-commercial. 7.7 GiB eager / 14.4 GiB `--fast-all`. [verified 12 Sep 2026: the earlier "flash-attn built for sm90" blocker was wrong — flash-attn appears only in `docker/build.sh` (`FLASH_ATTN_CUDA_ARCHS=80`) for the `--fast-all` CUDA-graph path. `requirements.txt` is `torch==2.9.1, torchaudio==2.9.1, qwen-tts==0.1.1, transformers==4.57.3, numpy, soundfile, fastapi, uvicorn` — nothing NVIDIA-specific; `infer.py` loads with `attn_implementation="eager"` and the model class declares `_supports_sdpa = True`. Breeze is built on the `qwen-tts` package, i.e. the same stack as Qwen3-TTS.]
- Verdict: **plausible on this box via the eager path once Qwen3-TTS runs** (same codec-decoder MIOpen story); still personal-listening only because of the weights licence. Worth an evening *after* Qwen3-TTS, not before.

### 2.7 Higgs Audio — v2 has text speaker profiles; v3 dropped them
- v2 (now `bosonai/higgs-tts-2-3b-base`, Llama-3-style community licence, commercial OK under 100k users): `--ref_audio profile:male_en_british` with profiles written as prose, e.g. "Male, American accent, modern speaking rate, moderate-pitch, friendly tone, and very clear audio." plus a `--scene_prompt`. "For optimal performance … GPU with at least 24GB memory" — over your budget, and the design vocabulary is thin (four profiles shipped).
- v3 (`bosonai/higgs-audio-v3-tts-4b`, 2026-06-04): 102 languages, inline tokens `<|emotion:amusement|><|prosody:expressive_high|>`, **no description-to-voice** — cloning plus tags only [verified: card lists emotion/style/prosody/sfx tags and cloning only]. "Boson Higgs TTS 3 Research and Non-Commercial License" [verified: the LICENSE §II-A Creator Use Grant covers self-published "audiobooks", monetised or not, with attribution — so v3 output *is* distributable, unlike Breeze/Fish]. Skip *for voice design*; it stays in the plan as the tag-driven narration engine (see engines-quality.md).

### 2.8 Older / narrower controllable engines
- **Spark-TTS-0.5B** (Mar 2025, repo idle since Apr 2025): `--gender {male,female} --pitch {very_low,low,moderate,high,very_high} --speed {very_low,…,very_high}`. Coarse but *deterministic* — the same flags give the same voice class, which is why it is still used for batch character generation. Weights are **cc-by-nc-sa-4.0** on HF even though the code is Apache. Plain torch (Qwen2.5-0.5B + BiCodec).
- **Zonos-v0.1-transformer** (Feb 2025, idle since Mar 2025, Apache-2.0, "6GB+ VRAM"): sliders, not prose — `emotion` 8-D (Happiness, Sadness, Disgust, Fear, Surprise, Anger, Other, Neutral), `pitch_std` 0–400 ("20-45 normal, 60-150 expressive" — it is pitch *variation*, not absolute pitch), `speaking_rate` 0–40 phonemes/s, `fmax`. The CONDITIONING_README admits emotion "tends to be entangled with various other conditioning inputs". Needs a speaker embedding (reference) for a fixed voice; without one you get a random speaker. The hybrid model needs Mamba CUDA kernels (no); transformer variant is plain torch + eSpeak. Windows via fork only.
- **Parler-TTS** (Mini 880M / Large 2.3B, Aug 2024, repo idle since Dec 2024, Apache-2.0): prose descriptions ("A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch"), trained on "45k hours of audiobook data" with synthetic annotations. InstructTTSEval-EN 63.4/48.7/28.6 (mini) — it will get gender and rough speed, little else. Historical interest only.
- **VoiceSculptor** (ASLP, Jan 2026, Apache-2.0, https://github.com/ASLP-lab/VoiceSculptor): LLaSA + CosyVoice2, RAG-based iterative refinement, ZH-only benchmark (75.7/64.7/61.5). Chinese-first; skip for English narration.

### 2.9 Engines that steer a *reference* rather than design a voice (for completeness)
- **IndexTTS-2.5** (2026-08-10, 0.8B, bilibili licence — royalty-free below 100M MAU / RMB 1bn revenue, so fine for you): `emo_vector=[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]` (each 0–1, sum ≤ 1.5 in the ComfyUI node), `emo_alpha 0–1`, `emo_text`, `use_random` ("reduces the voice cloning fidelity"). Needs `spk_audio_prompt`. Excellent second stage once you own a designed clip.
- **Fun-CosyVoice3-0.5B** (Dec 2025, Apache-2.0): instruct covers "languages, dialects, emotions, speed, volume" — style, not timbre; needs a prompt clip.
- **Step-Audio-EditX** (3B, Elo 1102): edits emotion / speaking style / paralinguistics on an existing clip; "12GB min". [verified 12 Sep 2026: **struck.** Code is Apache-2.0 but the weights carry no licence statement anywhere (README licence section covers code only; HF card has no tag). The shipped inference is vLLM-only — `model_loader.py` imports `from vllm import LLM`, `pyproject.toml` hard-pins a manylinux `vllm` wheel, `torchcodec`, Python >= 3.12, "Tested operating system: Linux". No transformers loader exists in the repo, and vLLM has no Windows ROCm build.]
- **Fish S2-Pro** (Mar 2026, 4B, Elo 1125): cloning + `[whisper]`-style tags; "Fish Audio Research License" — personal use OK ("personal use or evaluation and testing"), any commercial use needs a written licence. Has a `compose.rocm.yml`.
- **Voxtral-4B-TTS-2603** (Mistral, Mar 2026, CC-BY-NC-4.0): 20 presets + 3 s cloning, "visit our AI Studio" for custom voices; vLLM-omni serving. No design.
- **DramaBox** (Resemble, LTX-2 Community licence, "~24 GB VRAM"): screenplay-style stage directions outside quotes; clone from 10 s. Over budget.
- **VibeVoice** (MIT): voice presets from files; no design.
- **Chatterbox** issue #219 (open) shows what people want and are not getting from preset-style engines: one commenter building children's-story voices reports "the current voice design prompts are failing to produce high-pitched, child-like voices, often resembling those of adolescents instead." Expect the twelve-year-old to be the hardest of your three briefs on *every* engine; Qwen's "around 8 years old" example is the strongest counter-evidence.

### 2.10 A permissioned reference bank you can use today
https://huggingface.co/kyutai/tts-voices — Kyutai does not release its voice-embedding model "to ensure people's voices are only cloned consensually", but the repo ships the **raw WAVs**: `voice-donations/` holds 456 WAV files (228 voices, raw + `_enhanced`) from the Unmute Voice Donation Project (Jun 2025–Feb 2026), licensed **CC0**; plus VCTK (CC-BY-4.0), CML-TTS (CC-BY-4.0), Expresso and EARS (CC-BY-NC-4.0, "Non-commercial use only"). Feed the CC0 ones to Chatterbox or to the shaping chain below. This is the cleanest answer to "designed or permissioned voices only".

---

## 3. Shaping a reference clip: deeper, bigger, raspier — without smear

Principle: three independent knobs. **F0 (pitch)** = how deep. **Formant scale** = how big the body. **Rate** = how slow. A phase vocoder pitch-shift without formant preservation moves all three together and smears transients; the tools below keep them separate.

### 3.1 Praat via parselmouth — `Change gender` (resampling + overlap-add, no phase vocoder)
Praat manual: "The shifting of frequencies is done via manipulation of the sampling frequency. Pitch and duration changes are generated with overlap-add synthesis." Parameters: pitch floor (75), pitch ceiling (600), **formant shift ratio** (1.1 ≈ male→female, 1/1.1 ≈ female→male; "0.8 … if the target gender is male" in the ASR-augmentation literature), **new pitch median** Hz (0 = keep), **pitch range factor** (1.0 = keep), **duration factor**.

```python
import parselmouth
from parselmouth.praat import call
snd = parselmouth.Sound("ref.wav")
# giant: body 15 % bigger, median 78 Hz, flatter intonation, 10 % slower
giant = call(snd, "Change gender", 75, 600, 0.85, 78, 0.7, 1.10)
giant.save("ref_giant.wav", "WAV")
# old priest in a young body: keep formants (young tract), lower & flatten pitch, slow a touch
old  = call(snd, "Change gender", 75, 600, 1.00, 95, 0.8, 1.05)
# twelve-year-old from an adult female clip: smaller tract, higher median, livelier
girl = call(snd, "Change gender", 75, 600, 1.12, 240, 1.15, 0.97)
```
Ranges people actually use: formant ratio 0.80–0.90 for "big", 1.08–1.15 for "small"; pitch median 70–85 Hz giant, 85–110 Hz ordinary adult male, 200–260 Hz child; pitch range factor 0.6–0.8 to flatten (menace, age), 1.1–1.3 to enliven. Beyond ratio 0.8 / median < 65 Hz it stops sounding like a person. If you only want pitch, the documented Manipulation route is `To Manipulation` → `Extract pitch tier` → `Multiply frequencies` → `Replace pitch tier` → `Get resynthesis (overlap-add)`.

### 3.2 WORLD vocoder (pyworld) — analysis/resynthesis with explicit F0 and envelope
`pip install pyworld` (or `pyworld-prebuilt` on Windows). Decomposes into f0, spectral envelope `sp` and aperiodicity `ap`; you scale f0 and *warp the frequency axis* of `sp` (formant shift) then resynthesise. Clean for speech; slightly "vocoded" if pushed far.

```python
import numpy as np, soundfile as sf, pyworld as pw
x, fs = sf.read("ref.wav"); x = x.astype(np.float64)
f0, t = pw.harvest(x, fs); sp = pw.cheaptrick(x, f0, t, fs); ap = pw.d4c(x, f0, t, fs)
f0_new = f0 * 2 ** (-5 / 12)                       # -5 semitones
r = 0.87                                            # formants down 13 %
k = np.arange(sp.shape[1])
warp = lambda M: np.array([np.interp(k, k * r, row) for row in M])
y = pw.synthesize(f0_new, warp(sp), warp(ap), fs)
sf.write("ref_giant_world.wav", y, fs)
```
Add breathiness/age by raising `ap` (e.g. `ap = np.clip(ap + 0.15, 0, 1)`) — cheap, believable "seventy-year-old" texture that pitch tools cannot give.

### 3.3 Rubber Band 4.0 (rubberband-cli / pyrubberband) — good phase vocoder with formant control
- `-p X` semitones, `-F/--formant` "Enable formant preservation when pitch shifting", `-3/--fine` = R3 engine ("higher-quality results … especially … vocals"). `OptionFormantPreserved`: "Preserve the spectral envelope of the unshifted signal." Independent formant *scaling* (`setFormantScale`) is "supported only in the R3 … engine" and is **library-API only** — not exposed on the CLI, so pyrubberband cannot reach it.
- Recipes: deeper-same-body `rubberband -3 -p -4 -F ref.wav out.wav`; deeper-and-bigger (formants follow pitch, ≈ −16 % at −3 st) `rubberband -3 -p -3 ref.wav out.wav`. Python: `pyrb.pitch_shift(y, sr, -4, rbargs={'-F': '', '-3': ''})`.
- It is still a phase vocoder; on plosives R3 is far better than librosa/torchaudio's STFT shift but Praat/WORLD are cleaner for speech.

### 3.4 stftPitchShift (MIT) — formant shift without pitch shift
CLI `-p` pitch factor(s), `-q` "optional formant lifter quefrency in milliseconds (default 0.0)", `-t` "fractional timbre shifting factor related to -q (default 1.0)". Start with `-q 1`; e.g. `stftpitchshift -i ref.wav -o out.wav -p 1.0 -q 1 -t 0.85` lowers formants 15 % at unchanged pitch — the "bigger body, same note" move that Rubber Band's CLI cannot do. Applio's RVC fork exposes the same engine as "Formant Shifting … Quefrency (formant scale) and Timbre (formant shift)".

### 3.5 RVC / so-vits as a shaping stage
RVC converts *timbre* onto a trained target model; `f0_up_key` transposes in semitones (negative = deeper), `protect` guards voiceless consonants, `index_rate` "closer to 1.0: The output more closely matches the target speaker's timbre but may introduce artifacts". It only helps if you have a **consented** raspy/deep target to train on (10–30 min of audio); it cannot invent a giant from a description. Do not train on a named actor. As a post-stage after Chatterbox it is stable (`tts-with-rvc`, TTS-Audio-Suite "Voice Changer: RVC + ChatterBox VC").

### 3.6 Rasp / grit
No pitch tool adds rasp. Three honest options: (1) ask the design engine — MOSS's example "hoarse elderly voice", Qwen "deep, gravelly, raspy"; (2) post-synthesis saturation, e.g. Spotify `pedalboard` (GPL-3): `Pedalboard([HighpassFilter(60), Distortion(drive_db=8), LowShelfFilter(cutoff_frequency_hz=160, gain_db=3)])`, optionally mixing an octave-down copy (Praat, factor 0.5) at −12 to −15 dB for "chest"; (3) Step-Audio-EditX / IndexTTS-2.5 emotion vectors for tired/angry deliveries that read as rough. Keep saturation subtle — cloned voices pick up distortion as *identity* and it compounds.

### 3.7 Will Chatterbox clone a shaped clip faithfully?
- No issue in resemble-ai/chatterbox (26k stars, pushed Jul 2026) discusses pitch-shifted or formant-shifted references; nobody has reported it failing *or* working. Mechanically it should: the speaker encoder and S3Gen condition on the clip's spectral envelope, so lowered formants and F0 will be reproduced; PSOLA/WORLD artefacts (buzz, metallic ap) will be reproduced too. That is the argument for Praat/WORLD over a smeary shift — Chatterbox will faithfully clone the smear.
- Test protocol (30 min): take one CC0 Kyutai donation clip → make four variants (raw, Praat giant, WORLD giant, rubberband −4 −F) → run each through `ChatterboxTTS.generate(text, audio_prompt_path=…, exaggeration=0.5, cfg_weight=0.5)` on the same paragraph → measure median F0 with parselmouth (`snd.to_pitch().selected_array['frequency']`) and listen. If Chatterbox "corrects" the giant back toward a normal male range, shape harder (ratio 0.8, median 72 Hz) or move the shaping *after* synthesis instead (shape the Chatterbox output with the same Praat call — cleaner, and it keeps Chatterbox's prosody).
- Alternative that avoids the question: design the giant in Qwen3-VD / MOSS, and clone *that* — no signal processing in the reference at all.

---

## 4. Recommended menu for your three briefs

| Brief | Fast path | Quality path |
|---|---|---|
| Eight-foot giant, very low, raspy, slow | Kyutai CC0 male clip → Praat `Change gender` (0.85, 78 Hz, 0.7, 1.10) → Chatterbox Turbo | Qwen3-VD "An enormous man, extremely deep, slow, gravelly voice, chest resonance, unhurried menace" → best take → Chatterbox / Qwen Base clone; optional WORLD `ap+0.1` and light saturation |
| Seventy-year-old priest in a young body | Young male clip → Praat (1.00, 95 Hz, 0.75, 1.05) + WORLD `ap+0.15` → Chatterbox | MOSS-VoiceGenerator "tired, hoarse elderly voice, slow, breathy, precise diction" → clone; IndexTTS-2.5 `emo_vector` calm/melancholic for delivery |
| Girl of twelve | Female CC0 clip → Praat (1.12, 240 Hz, 1.15, 0.97) → Chatterbox | Qwen3-VD "a girl of about twelve, light clear voice, quick, curious" (the one brief every engine gets wrong most often — audition 5–10 takes) |

Install order on the 9070 XT: Qwen3-TTS (`pip install qwen-tts`, `attn_implementation="sdpa"`, try `MIOPEN_FIND_MODE=2`, then `torch.backends.cudnn.enabled=False`, then `MIOPEN_GEMM_ENFORCE_BACKEND=hipblaslt`; if the decoder is still slow, build imagilux/miopen-conv-fix) → MOSS-VoiceGenerator (override the cu128 torch pin) → VoxCPM2 (PyTorch, fall back to VoxCPM.cpp Vulkan). Shaping stack: `pip install praat-parselmouth pyworld-prebuilt pyrubberband stftpitchshift` plus the rubberband-cli binary.

---

## 5. Sources
- Qwen3-TTS: https://github.com/QwenLM/Qwen3-TTS · https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign · https://arxiv.org/html/2601.15621v1 · https://github.com/QwenLM/Qwen3-TTS/discussions/220 · https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning · https://dev.to/tumf/qwen3-tts-surprised-by-the-quality-of-japanese-on-apple-silicon-m3-creating-rights-free-voices-k1d
- ROCm evidence: https://github.com/ROCm/TheRock/issues/3077 · https://github.com/trevortai/qwen3-tts-amd · https://github.com/imagilux/miopen-conv-fix · https://github.com/Supreme-Commander-droit/qwen3-tts-rocm-rdna4-speedfix
- MOSS: https://github.com/OpenMOSS/MOSS-TTS · https://huggingface.co/OpenMOSS-Team/MOSS-VoiceGenerator
- VoxCPM2: https://github.com/OpenBMB/VoxCPM · https://huggingface.co/openbmb/VoxCPM2
- OmniVoice: https://github.com/k2-fsa/OmniVoice · https://huggingface.co/k2-fsa/OmniVoice · https://github.com/ServeurpersoCom/omnivoice.cpp
- Maya1: https://huggingface.co/maya-research/maya1
- Breeze TTS 2: https://huggingface.co/BreezeBlue/Breeze-TTS-2 · https://github.com/breezeblue-ai/breeze-tts · https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/ (Artificial Analysis Elo table)
- Higgs: https://github.com/boson-ai/higgs-audio · https://huggingface.co/bosonai/higgs-audio-v3-tts-4b · https://huggingface.co/bosonai/higgs-tts-2-3b-base (LICENSE) · examples/voice_prompts/profile.yaml
- Spark-TTS: https://github.com/SparkAudio/Spark-TTS (cli/inference.py) · https://huggingface.co/SparkAudio/Spark-TTS-0.5B (cc-by-nc-sa-4.0)
- Zonos: https://github.com/Zyphra/Zonos/blob/main/CONDITIONING_README.md
- Parler-TTS: https://github.com/huggingface/parler-tts
- VoiceSculptor: https://github.com/ASLP-lab/VoiceSculptor
- IndexTTS: https://github.com/index-tts/index-tts (README + LICENSE)
- CosyVoice: https://github.com/FunAudioLLM/CosyVoice · Step-Audio-EditX: https://github.com/stepfun-ai/Step-Audio-EditX · Fish: https://github.com/fishaudio/fish-speech, https://huggingface.co/fishaudio/s2-pro/blob/main/LICENSE.md · Voxtral: https://huggingface.co/mistralai/Voxtral-4B-TTS-2603 · DramaBox: https://github.com/resemble-ai/DramaBox
- Chatterbox: https://github.com/resemble-ai/chatterbox/issues/219 · https://github.com/petermg/Chatterbox-TTS-Extended · https://github.com/diodiogod/TTS-Audio-Suite
- Kyutai voices: https://huggingface.co/kyutai/tts-voices
- Shaping tools: https://www.fon.hum.uva.nl/praat/manual/Sound__Change_gender___.html · https://parselmouth.readthedocs.io/en/stable/examples/pitch_manipulation.html · https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder · https://breakfastquay.com/rubberband/code-doc/classRubberBand_1_1RubberBandStretcher.html · https://manpages.debian.org/unstable/rubberband-cli/rubberband.1.en.html · https://github.com/bmcfee/pyrubberband · https://github.com/jurihock/stftPitchShift · https://docs.applio.org/reference/architecture/
