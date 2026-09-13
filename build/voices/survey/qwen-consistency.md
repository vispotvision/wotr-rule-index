# Keeping one designed voice stable across many lines — description-conditioned AR TTS with no reference clip

Survey date: 12 Sep 2026. Scope: the *consistency* problem for autoregressive, description-conditioned
TTS (Qwen3-TTS-12Hz-1.7B-VoiceDesign first; Parler-TTS, MOSS-VoiceGenerator, VoxCPM2, CosyVoice
instruct, Maya1, Tortoise, ChatTTS for comparison). Constraint honoured throughout: **no reference
clip at generation time, no Base-model clone, no RVC.** Where the only documented answer *is* a clone,
I say so and move on rather than pretend there is another.

Companion report: `qwen-official.md` (same folder) covers Qwen's own material — kwargs, caption
schema, DashScope guidance. I cite it as **[QO §n]** instead of repeating it.

Everything in quotes is verbatim from the linked source. "Unknown" means I looked and found nothing.

Sources (short handles):

- **[SRC-M]** `qwen_tts/core/models/modeling_qwen3_tts.py` @ main — https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/qwen_tts/core/models/modeling_qwen3_tts.py
- **[SRC-W]** `qwen_tts/inference/qwen3_tts_model.py` @ main — https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/qwen_tts/inference/qwen3_tts_model.py
- **[VD-ST]** VoiceDesign checkpoint safetensors header (read via HTTP range request, 12 Sep 2026) — https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/resolve/main/model.safetensors
- **[VD-GC]** https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/raw/main/generation_config.json
- **[GH]** Qwen3-TTS README — https://github.com/QwenLM/Qwen3-TTS
- **[PAPER]** Qwen3-TTS technical report — https://arxiv.org/html/2601.15621v1
- **[D220]** discussion "Voice Design is great, but we need to be able to keep the voices" — https://github.com/QwenLM/Qwen3-TTS/discussions/220
- **[I298]** issue "same input → same output?" (CustomVoice) — https://github.com/QwenLM/Qwen3-TTS/issues/298
- **[I343]** issue "short/opening utterances unstable … while long-form is stable" — https://github.com/QwenLM/Qwen3-TTS/issues/343
- **[I239]** issue "Inconsistent speaking rate in long text generation" — https://github.com/QwenLM/Qwen3-TTS/issues/239
- **[HF-D3]** HF discussion "Re-use a designed voice" — https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/discussions/3
- **[KOBOLD]** koboldcpp discussion "Qwen 3 TTS Voice Design Help" — https://github.com/LostRuins/koboldcpp/discussions/2192
- **[DS-EN]** DashScope Voice Design doc — https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-design
- **[OCDEVEL]** community guide — https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning
- **[DEVTO]** "From Stochastic Drifting to Vector Anchors" — https://dev.to/lcmd007/from-stochastic-drifting-to-vector-anchors-how-i-solved-voice-consistency-in-qwen-tts-4dff
- **[ALEX]** Alexandria audiobook pipeline (VoiceDesign-based) — https://github.com/Finrandojin/alexandria-audiobook
- **[COMFY]** ComfyUI-Qwen3-TTS voice-design node docs — https://www.runcomfy.com/comfyui-nodes/ComfyUI-Qwen3-TTS/qwen3-voice-design
- **[CPORT]** gabriele-mastrapasqua/qwen3-tts (C port) README + `docs/speaker-map.md` — https://github.com/gabriele-mastrapasqua/qwen3-tts
- **[MOSS-DOC]** audio.cpp community doc for MOSS-VoiceGenerator (has measured F0 numbers) — https://github.com/0xShug0/audio.cpp/blob/main/docs/community_models/moss_voicegen.md
- **[MOSS-P]** MOSS-VoiceGenerator paper — https://arxiv.org/html/2603.28086
- **[VOX-R]** VoxCPM README — https://github.com/OpenBMB/VoxCPM/blob/main/README.md
- **[VOX-P]** VoxCPM2 technical report — https://arxiv.org/html/2606.06928v1
- **[PARLER-MC]** parler-tts-mini-v1 model card — https://huggingface.co/parler-tts/parler-tts-mini-v1
- **[PARLER-INF]** parler-tts INFERENCE.md — https://github.com/huggingface/parler-tts/blob/main/INFERENCE.md
- **[P11]** parler-tts issue #11 — https://github.com/huggingface/parler-tts/issues/11
- **[P14]** parler-tts issue #14 — https://github.com/huggingface/parler-tts/issues/14
- **[P45]** parler-tts issue #45 — https://github.com/huggingface/parler-tts/issues/45
- **[P110]** parler-tts PR #110 — https://github.com/huggingface/parler-tts/pull/110
- **[P139]** parler-tts issue #139 — https://github.com/huggingface/parler-tts/issues/139
- **[MAYA]** maya-research/maya1 model card — https://huggingface.co/maya-research/maya1
- **[CHATTTS]** ChatTTS README — https://github.com/2noise/ChatTTS
- **[TORTOISE]** tortoise-tts `api.py` — https://github.com/neonbjb/tortoise-tts/blob/main/tortoise/api.py
- **[SLEUTH]** SpeakerSleuth (Lee et al., Jan 2026) — https://arxiv.org/pdf/2601.04029
- **[BON]** "Best-of-N TTS Evaluation is Confounded by ASR Family Alignment" (Yu & Kang, Jul 2026) — https://arxiv.org/html/2607.08256v1
- **[ASV]** "Analyzing and Improving Speaker Similarity Assessment for Speech Synthesis" — https://arxiv.org/html/2507.02176v1
- **[EXPPRO]** "Expressive Prompting: Improving Emotion Intensity and Speaker Consistency in Zero-Shot TTS" — https://arxiv.org/html/2409.18512
- **[DUB]** "Deep Dubbing: … Text-to-Timbre and Context-Aware Instruct-TTS" — https://arxiv.org/html/2509.15845v1
- **[ITTSE]** InstructTTSEval — https://arxiv.org/html/2506.16381v1
- **[TORCH]** PyTorch reproducibility notes — https://docs.pytorch.org/docs/2.13/notes/randomness.html

---

## 0. Executive summary

1. **Why the voice changes: there is no identity slot in VoiceDesign.** In the Base/CustomVoice models a
   speaker embedding is inserted as one continuous token before the talker; in VoiceDesign the code
   path sets `speaker_embed = None` and the checkpoint ships **no `speaker_encoder` weights at all**
   (404 tensors, all under `talker.`) [SRC-M l.2088-2089, VD-ST]. Identity therefore exists only as the
   codec tokens the talker *samples*, conditioned on the instruct text. The instruct defines a
   distribution over speakers; every call draws a fresh member. This is the same architecture story
   as Parler-TTS, MOSS-VoiceGenerator and VoxCPM2, and all four projects' maintainers or docs say the
   same thing: the description is not a voice ID.
2. **A fixed seed reproduces a take, not a voice.** Same seed + same instruct + same text → identical
   audio (in HF/torch on one machine; not guaranteed in vLLM). Same seed + different text → a
   different draw. Measured on MOSS-VoiceGenerator: median F0 moved **2.2 and 7.6 semitones** across
   three lines under one seed [MOSS-DOC]. Isaac's 105 Hz vs 145 Hz is 5.6 semitones — the same
   phenomenon. Nobody has reported a seed that pins identity across texts on any of these models.
3. **Greedy decoding does not buy identity and can wreck quality.** Parler: `do_sample=False`
   "results in basically noise" [P45, P110] [verified]. Qwen (**LoRA fine-tune of 1.7B-Base**, greedy on
   vLLM-Omni): output is deterministic per input, yet ~15% of short utterances still came out with
   "wrong timbre / gender flip" in the first 1–2 s [I343] [verified — but see caveat: this is a
   fine-tuned CustomVoice-style model, and the one reply on the thread attributes the onset
   instability to a speaker-encoder decay bug in the SFT script (PR #351), so it is weak evidence
   about VoiceDesign]. Greedy removes run-to-run variance for one text; it does not make two texts
   share a speaker.
4. **Identity is settled in the opening ~1–2 s and then held — plausible, thinly evidenced.**
   Evidence: [I343] ("the generation often 'settles' into the correct voice partway through, so the
   instability is concentrated at generation onset") [verified, fine-tuned Base, see 3]; [D220] ("the
   voice changes when you [chunk]"; within one generation the voice holds) [verified]. [corrected: the
   tech report's ">10 minutes" claim is about *content* consistency (WER on an internal long-form set),
   not speaker consistency, and does not support this point.] Practical consequence: **the fewer
   separate calls, the fewer identity draws.** The strongest pure-VoiceDesign lever is to generate a
   character's whole scene in one call and cut it up afterwards (§3).
5. **Batching does nothing for identity.** `generate_voice_design(text=[...])` builds one independent
   left-padded sequence per item; sampling is per row [SRC-M l.2236-2254]. Batch = N separate draws
   that happen to run in parallel.
6. **Best-of-N by speaker-embedding similarity to an anchor is the only documented *pure-design*
   mechanism that plausibly converges on a voice**, and it is exactly what DashScope tells its own
   users to do by ear: "Generate multiple voices, listen to them, and select the best one" [DS-EN]
   [verified; note the DashScope page covers CosyVoice VD and Qwen3-TTS-VD jointly]. Automating the
   ear: ECAPA-TDNN cosine discriminates the same-speaker candidate at **97.8–100 %** accuracy in
   SpeakerSleuth's 3-candidate task [SLEUTH] [verified — but corrected: the two decoys there are an
   *opposite-gender* voice and a *different, voice-converted speaker*; nobody has measured whether
   ECAPA ranks N draws of the *same description* usefully, so "measurably converges" was overstated].
   Tortoise shipped this pattern in 2022 (`num_autoregressive_samples` + CVVP re-ranking) [TORTOISE]
   [verified; note `cvvp_amount` defaults to 0, i.e. CVVP re-ranking is off unless enabled].
7. **Description-level narrowing works for coarse attributes (gender, age band, low/high pitch,
   texture words), and is unmeasured or unsupported for numeric Hz, named accents, or "extreme"
   depth.** Swapping only "male/his"→"female/her" moved median F0 117→190 Hz over 47 MOSS designs
   [MOSS-DOC]; nothing in any Qwen source shows numeric pitch being honoured. Parler's named-speaker
   trick ("Jon") is a *training-time* device (34 named speakers in the captions) and has **no Qwen
   VoiceDesign equivalent** — the VoiceDesign config has `spk_id: {}` [QO §4.3].
8. **Post-hoc F0/formant normalisation to the anchor will raise ASV-measured similarity** because
   the common embeddings "primarily encode static spectral information (mean pitch, HNR, shimmer,
   α-ratio)" [ASV] — but it will not fix cadence/emotional-baseline drift, which is what the
   long-form narrators in [D220] actually complain about, and no source reports a naturalness cost
   curve for shifting TTS output by N semitones. Treat it as a ±2-semitone touch-up, not a fix.

---

## 1. The mechanism: where identity lives, and why it is re-rolled per call

### 1.1 Qwen3-TTS VoiceDesign has no speaker token

`Qwen3TTSForConditionalGeneration.generate()` [SRC-M]:

```python
if voice_clone_spk_embeds is None:
    if speaker == "" or speaker == None: # Instruct create speaker
        speaker_embed = None
```
(l.2087-2089). When `speaker_embed is None` the codec prefix is `[think, think_bos, <lang>, think_eos, pad, bos]`
with **no** identity slot (l.2166-2168); with a speaker it becomes `[…, speaker_embed, pad, bos]` (l.2169-2172).
The instruct is prepended as projected *text* embeddings (l.2076-2080) — it is a prompt, not a latent.

The shipped VoiceDesign `model.safetensors` header lists 404 tensors, every one under `talker.`;
`speaker_encoder.*` does not exist [VD-ST]. So there is nothing to extract, cache or re-inject inside
the VoiceDesign model itself. (The C port's `speaker-map.md` describes the Base/CustomVoice path
where "Timbre/identity is seeded by the x-vector at the input and carried by the codec tokens the
Talker emits" [CPORT] — VoiceDesign has only the second half of that sentence.)

The tech report's own claim — "Qwen3-TTS allows users to create new voices or manipulate fine-grained
attributes of generated speech via natural language descriptions, while also supporting the stable
generation of any content using the created voice" [PAPER §1] [corrected: the earlier version spliced
the abstract's "creation of entirely novel voices" onto this §1 sentence with an ellipsis; this is the
single verbatim sentence] — is, per the README, delivered by cloning the created voice with the Base
model ("If you want a designed voice that you can reuse like a cloned speaker, a practical workflow
is: (1) use the VoiceDesign model to synthesize a short reference clip … (2) feed that clip into
`create_voice_clone_prompt`" [GH]) [verified], not by the VoiceDesign model alone. Qwen's
collaborators have not contradicted users on this in [D220], [HF-D3] or [I298] (no maintainer reply
in any of them, re-checked 12 Sep 2026 via the GitHub API: every commenter is `author_association:
NONE`) [verified].

[verified] Code and checkpoint facts above re-checked 12 Sep 2026 against `main`: the `# Instruct
create speaker` branch is at l.2088-2089 today; the two prefix layouts at l.2166-2172; the safetensors
header lists exactly 404 tensors, all prefixed `talker.`, none matching `speaker`/`spk`;
`generation_config.json` carries `max_new_tokens: 8192` and overrides the wrapper's hard default of
2048 (wrapper `pick()` order: user arg → generation_config → hard default). The repo's last commit
is 2026-03-17 (fine-tuning script only) and PyPI `qwen-tts` stops at 0.1.1 (2026-02-06), so the
code reading is not stale. No newer VoiceDesign weights exist on the Qwen HF org as of today.

### 1.2 Same story, other engines

| Engine | Where identity comes from with no clip | Maintainer/doc statement |
|---|---|---|
| Parler-TTS | sampled codec tokens under a T5-encoded description | "Parler-TTS generate a similar but different voice with same discription but different Transcript text" (user, [P14]); maintainer answer: single-speaker fine-tune, or 34 *named* speakers baked into training captions [P11, PARLER-MC] |
| MOSS-VoiceGenerator | description and text concatenated into the LM [MOSS-P] | "A seed reproduces a take, not a voice." / "The instruction sets a class, the seed picks a member." [MOSS-DOC] |
| VoxCPM2 | "(voice description) text" prefix, diffusion-style with CFG [VOX-P] | "Voice Design and Controllable Voice Cloning results can vary between runs — you may try to generate 1~3 times to obtain the desired voice or style." [VOX-R] |
| CosyVoice instruct (v1) | pre-registered `spk_id` + instruct; not description-designed | identity is a fixed speaker embedding; instruct only changes style — the "CustomVoice" pattern, not "VoiceDesign" |
| Maya1 | `<description="…">` prefix; `voice_id` is a hosted-API concept | no statement on cross-generation consistency of a described voice [MAYA] |
| ChatTTS | **explicit** random speaker latent: `rand_spk = chat.sample_random_speaker()` → `spk_emb=rand_spk` "save it for later timbre recovery" [CHATTTS] | the honest design: sample a speaker once, hold it. Qwen VoiceDesign folds this draw into the codec tokens where you cannot grab it |
| Tortoise | `--voice random` = random conditioning latent; candidates re-ranked by CLVP/CVVP [TORTOISE] | precedent for best-of-N by voice similarity |
| Deep Dubbing (paper) | "Text-to-Timbre" generates one speaker embedding per character from the description, then Instruct-TTS takes "the generated speaker embedding, the current sentence text, and the emotion-scene instruction" [DUB] | the architecture Isaac wants (identity fixed, direction per line) — exists as a research system, not in Qwen VoiceDesign |

---

## 2. Deterministic decoding: seeds, greedy, and what they actually fix

### 2.1 Seeds

- The `qwen_tts` wrapper has no seed argument and never seeds torch [SRC-W grep: no `seed`]. ComfyUI
  nodes and the C port add one (`--seed <n>  Random seed for reproducible output` [CPORT]); it is just
  `torch.manual_seed` before the call.
- **What a seed gives you:** [DEVTO] (Qwen TTS): "It ensures that the exact same text produces the exact
  same audio (even the MD5 hashes will match). Where Seed fails: As soon as you change the input text—even
  by a single character—the seed's constraint collapses." [verified verbatim — but corrected: the
  article never names which Qwen TTS model, checkpoint or runtime it used, gives no measurements, and
  its "vector anchor" fix is a speaker-embedding `.pt` extracted from a saved WAV, i.e. a clone. It is
  a Qwen-family anecdote, not "Qwen VoiceDesign specifically".] [MOSS-DOC] (MOSS): "The same seed,
  instruction and text give a bit-identical WAV. … the same seed on different text does not: median F0
  moved 2.2 and 7.6 semitones across three lines." [verified verbatim; MOSS-VoiceGenerator via
  audio.cpp on ROCm, not Qwen]. The same doc also quantifies chunk-level drift under voice design:
  "47 chunks are 47 independent designs: median F0 spans 13 semitones, and neighbouring chunks jump
  2.3 semitones on median, 9.9 at worst" [MOSS-DOC] [added on verification — the report had omitted
  the strongest number in its best source].
- **vLLM caveat:** [I298] user `BeeegZee`: "The fixed seed does not guarantee byte identical output, because
  it is applied only to one part of the model, but the fixed seed voice will 'behave' the same - same
  emotional and vocal range, same artifacts." (that was SFT CustomVoice on vLLM, not VoiceDesign in HF)
  [verified verbatim via GitHub API; the same commenter adds "there will be seeds that produce more
  varying output … And there will more stable seeds, without much artifacts. You just need to find
  one" — i.e. seed-hunting, on a *fixed-identity* model, for delivery stability only].
- **Why text changes the draw even with a fixed seed:** in `non_streaming_mode=True` (VoiceDesign's
  default, [SRC-W l.642]) the whole target text is prefilled before the first codec frame
  (l.2203-2226), so the logits at frame 0 already depend on every word of the line. The RNG stream is
  the same; the distribution it samples from is not.
- **Torch-level determinism on one machine:** [TORCH] — "Completely reproducible results are not guaranteed
  across PyTorch releases, individual commits, or different platforms." SDPA forward passes are
  deterministic on all backends; only backward is not, so inference with `torch.manual_seed` +
  identical inputs should be bit-stable on Isaac's box. ROCm-specific behaviour: **unknown** (no source
  found; the docs table does not mention HIP).

### 2.2 Greedy / temperature 0

- Parler: "Attempting to set `do_sample=False` for output consistency results in basically noise" [P45];
  PR author: "deterministic sampling by setting `do_sample=False` or `temperatute=0.1` tends to generate
  random noise" [P110]. Maintainer suggested `min_new_tokens=10`; reporter: "No, it doesn't work for me."
- Qwen (fine-tuned Base, greedy `temperature 0, top_k 1`, code-predictor "forced greedy via local patch",
  vLLM-Omni) [I343]: "Behavior is deterministic per input under greedy (identical output across repeats
  of the same text)" *and* "a subset (~15%) of short generations render with wrong timbre / gender flip /
  whisper, concentrated in the first ~1–2 s, sometimes recovering mid-utterance." Long-form was fine.
  So greedy on Qwen is usable (unlike Parler) but it does not stabilise identity across texts.
  [verified — with a caveat the earlier draft under-weighted: the reporter's model is a **LoRA
  fine-tune of 1.7B-Base on ~21 min of one speaker**, and the only reply (user `elaredo8`) points to
  PR #351 "Fix speaker_encoder silent decay under AdamW weight decay in SFT" as the likely cause, plus
  their own hack of re-injecting the Base speaker embedding. The ~15 % onset-flip figure may therefore
  be a fine-tuning artefact rather than a property of the sampler or of VoiceDesign. Still open, no
  maintainer reply, as of 12 Sep 2026.]
- No source reports VoiceDesign specifically under `do_sample=False`. Effect on voice quality: **unknown**.
  Community tuning advice that exists is about the *sampled* regime: Qwen defaults `temperature=0.9,
  top_k=50, top_p=1.0, repetition_penalty=1.05`, subtalker the same [VD-GC]; the C port ships
  `--temperature` default 0.5 [CPORT]; a DeepWiki summary recommends 0.7–0.8 "for stable, formal speech"
  (secondary source, unmeasured).
- **Two samplers:** the talker (codebook 0) and the sub-talker/code predictor (15 residual codebooks)
  are sampled separately (`subtalker_dosample`, `subtalker_temperature`, …) [SRC-W l.319-329]. Timbre
  detail lives largely in the residual codebooks; lowering `subtalker_temperature` while leaving the
  talker alone is the obvious experiment for "same phrasing variety, tighter timbre". **No source has
  measured it.**

### 2.3 Is identity decided in the first tokens, so a seed "locks" it?

Evidence that identity is decided early and then held within a generation:

- [I343]: instability "concentrated at generation onset", "settles into the correct voice partway through".
- [D220] original post: "Chunking isn't really an option because the voice changes when you do that" —
  i.e. within one chunk it does not.
- [D220] `storm-fox`: "The voice identity remains reasonably consistent, but the narrator's baseline
  cadence, prosody, and emotional delivery drift between chunks."
- Codec-LM prompting in general (AudioLM/VALL-E) conditions identity on the first ~3 s of acoustic tokens.

Evidence that a *seed* locks it: **none** — because in non-streaming mode the frame-0 distribution
depends on the whole text (§2.1). A seed reproduces the draw only when the inputs are identical.

**Hypothesis worth one afternoon (derived from code, untested by anyone I can find):** in
`non_streaming_mode=False` the talker is prefilled with only the *first* text token and the remaining
text is fed one token per codec frame (l.2200-2202, l.2228-2232; mechanism confirmed independently in
the [I239] analysis: "the target text is fed one token per codec frame (12.5 tok/s)"). If every line
starts with the same fixed sentence (say 12 tokens) and the same seed, the first ~12 frames (~1 s) are
computed from bit-identical inputs and should be bit-identical audio — a self-generated 1 s prompt
that the model then continues. Cut the fixed sentence off afterwards. Risks: streaming mode has the
rate-drift bug (+16.7 % within 25 s with a long reference; keep calls ≤ ~30 s) [I239]; 1 s may not be
enough (AudioLM/VALL-E use 3 s; [I343] says onset instability lasts 1–2 s); and identical frames only
hold if kernels are deterministic. Flagged as an experiment, not a recommendation. [Verification
note: [MOSS-DOC]'s parity table shows how fragile "identical frames" is in bf16 — "Greedy generation,
bf16 | first 16 rows identical, then diverges on a 0.003 logit gap" (that is C-port vs PyTorch, not
run-to-run, but the same near-tie sensitivity applies to any bf16 sampler once the RNG stream is the
only thing held fixed).]

---

## 3. One call vs many: batching and "whole scene in one generation"

- **Batch ≠ shared identity.** `generate_voice_design` accepts lists, replicates a single instruct across
  items (l.700-701), builds one sequence per item and left-pads them (l.2236-2254). Rows do not attend to
  each other. Batched generation gives N independent draws — the C port notes batched output is
  "bit-identical to single-stream" [CPORT], i.e. batching changes nothing either way.
- **One long text = one draw.** Every long-form complaint in [D220]/[I239] is about *chunk boundaries*.
  VoiceDesign's shipped `max_new_tokens=8192` [VD-GC] at 12.5 frames/s ≈ 10.9 min of audio, matching the
  report's "over 10 minutes" claim [PAPER] [verified]. Non-streaming mode has flat pacing ("0.0 %" drift vs
  "+16.7 %" streaming in [I239]'s table; "this is already the default for CustomVoice/VoiceDesign")
  [verified verbatim via GitHub API — corrected scope: the [I239] measurements (user `sherifhanna700`,
  28 Aug 2026, a comment that is itself footered "Generated with Claude Code") were made on
  **1.7B-Base voice cloning with a 12.9 s reference**, not VoiceDesign; the 0.0 % row is the
  non-streaming *clone* layout. That VoiceDesign defaults to `non_streaming_mode=True` is confirmed in
  [SRC-W l.642]; that VoiceDesign's pacing is flat over 10 minutes is inferred, not measured. PR #362
  (make clone default non-streaming too) is still open, unmerged.]
- So the cheapest pure-VoiceDesign consistency tool is: concatenate all of a character's lines for a scene
  (or a whole chapter) into one text, generate once, split on silences / forced alignment. Delivery
  cues then have to be carried inside the text (punctuation, sentence shape, the "Gradual Control"
  arc style in the instruct [QO §4.5]) rather than by swapping instructs per line. Trade-off: one bad
  draw costs the whole scene → pair with best-of-N on the *scene*, or on a short probe first (§4).

---

## 4. Best-of-N selected by speaker similarity to an anchor

### 4.1 Precedents

- **Tortoise** (2022): "num_autoregressive_samples: Number of samples taken from the autoregressive model,
  all of which are filtered using CLVP. As Tortoise is a probabilistic model, more samples means a higher
  probability of creating something 'great'." / "cvvp_amount: Controls the influence of the CVVP model in
  selecting the best output from the autoregressive model. [0,1]." Presets run 16–256 candidates
  [TORTOISE]. CVVP scores candidate-vs-conditioning-voice similarity.
- **DashScope Voice Design** (Qwen's own hosted product): "The same description may produce slightly
  different voices each time. Generate multiple voices, listen to them, and select the best one." — then
  it returns a persistent `voice` ID [DS-EN]. Human best-of-N, then lock. The open weights give you the
  first half only.
- **VoxCPM2**: "you may try to generate 1~3 times to obtain the desired voice or style" [VOX-R].
- **Alexandria** (VoiceDesign audiobook pipeline): "re-generating lines with different seeds to make all
  samples similar enough" [D220, `Finrandojin`]; the repo exposes a "Batch Seed" and per-line instruct
  appended to a base description, but **no automatic similarity filter** [ALEX].
- **Best-of-N with an ASR verifier** is standard in zero-shot TTS evaluation: "Best-of-N (BoN) inference
  improves content consistency in zero-shot text-to-speech by selecting from N candidates with an
  automatic speech recognition (ASR) verifier"; N ∈ {3, 5, 10}; WER "from 2.06% to 1.72% (−16.5%)" while
  "SIM-o and UTMOS at N=3 stay within ±0.001 and ±0.005" [BON]. Relevant here only as a template: the
  verifier can be a speaker embedding instead of (or as well as) ASR.
- ~~**Expressive Prompting** (prompt selection by speaker similarity, CosyVoice): Resemblyzer SIM 0.683±0.023
  → 0.689±0.012 [EXPPRO] — a small mean gain but roughly halved variance; note the *variance* is what
  Isaac is fighting.~~ [corrected: the numbers are real (Table 2, ESD/CosyVoice, Random vs ExpPro) but
  the method is mischaracterised. ExpPro selects the *reference prompt clip* for zero-shot cloning —
  by pitch statistics, DNSMOS and ChatGPT text-emotion coherence, then text-semantic relevance — and
  "does not generate multiple synthesized candidates for selection"; speaker similarity is only an
  evaluation metric there. It is a clone-regime paper and says nothing about best-of-N over output
  draws or about description-only TTS. Not evidence for §4.]

### 4.2 How well does embedding selection work, and what threshold?

SpeakerSleuth [SLEUTH] frames the exact job: "When an inconsistent turn is identified, TTS systems typically
regenerate multiple candidate outputs and must select the one that best matches the target speaker."
Their embedding baselines:

- Methods: "Pairwise Similarity computes each turn's average cosine similarity to all other turns
  (τ_pair = 0.4). Centroid Distance computes each turn's distance from the centroid of all turns
  (τ_cent = 0.3). Reference Comparison computes similarity between each embedding and a reference speaker
  audio (τ_ref = 0.4)." Backbones: ECAPA-TDNN and WavLM.
- Discrimination (pick the right one of 3 candidates): Pairwise/Centroid (ECAPA) classification accuracy
  **97.8 / 99.0 / 100.0 / 100.0** across the four datasets (avg 99.2), NDCG@2 99.6; WavLM 96.7 / 95.5 /
  79.9 / 100.0. Reference-comparison (ECAPA) 97.8 / 92.0 / 99.4 / 76.2.
- Caveat they report: "ECAPA-TDNN-based methods over-detect changes while under-performing on S1, and
  WavLM-based methods show the opposite pattern." For *selection* (rank N candidates, keep the top)
  over-detection does not matter; for a hard reject threshold it does. [verified verbatim from the PDF]
- [corrected on verification — how the 3 candidates are built:] "Discrimination presents three
  candidates, one from each scenario (S1, S2, S3)": S1 is the original speaker, S2 "Gender Switch" is
  voice-converted "to an opposite-gender voice", S3 "Similar Speaker" is voice-converted to the other
  human speaker "with highest cosine similarity" **selected by ECAPA-TDNN itself**. So the 97.8–100 %
  is "pick the true speaker over a different-gender voice and an ECAPA-nearest other human" — partly
  circular for S3, and much coarser than ranking N same-description draws whose differences are a few
  semitones of median F0. The thresholds (0.4 / 0.3) were "set based on preliminary validation" on
  human multi-turn dialogue, not on TTS draws. Treat the numbers as "ECAPA ranking is the right tool",
  not as an expected accuracy for Isaac's task.
- Threshold calibration is embedding-model-specific. The one Qwen-specific cosine figure found (Baseten,
  fine-tuning Qwen3-TTS-Base with its own 2048-d speaker encoder over 64 clips of one speaker):
  "Per-clip embeddings of the same speaker typically agree at roughly 0.7 cosine similarity with each
  other, but at 0.85+ with their centroid" (https://www.baseten.co/blog/fine-tuning-qwen3-tts-for-high-quality-voice-cloning/;
  encoder not explicitly named in that sentence; nothing to do with VoiceDesign). Same-speaker cosine
  of ~0.7 on one encoder vs a 0.4 reject line on another (SpeechBrain 192-d ECAPA) shows why §4.3
  step 3 must recalibrate on the anchor takes rather than import a number.

What the embeddings do and do not see [ASV]: "speaker embeddings primarily encode static spectral
information (mean pitch, HNR, shimmer, α-ratio) reflecting voice quality and frequency range" and "fail to
capture dynamic behavioral identity markers like speech rate, voiced/unvoiced segment durations,
variations in pitch, and loudness." Also: "X-Vector embeddings encode a wider range of markers, including
more dynamic information, than more recent and better-performing embeddings." Implication: ECAPA
selection will converge timbre and pitch range (Isaac's 105-vs-145 Hz problem) but will *not* catch the
cadence/emotional-baseline drift `storm-fox` describes; add a cheap prosody check (median F0, speech
rate, RMS) alongside cosine.

### 4.3 Concrete recipe (assembled from the above; effect sizes are the cited ones, not mine)

1. **Anchor.** Generate K (8–16) takes of a 15–25 s probe paragraph per character with the frozen
   identity instruct; pick by ear; keep the WAV as the anchor and compute its ECAPA embedding
   (SpeechBrain `spkrec-ecapa-voxceleb`) plus median F0 / speech rate.
2. **Per line (or per scene, §3):** generate N candidates (start N=4; Tortoise-style budgets are 16+
   but Qwen 1.7B at 12.5 fps is far more expensive per candidate). Vary the seed only.
3. **Score** = cosine(ECAPA, anchor), reject below ~0.4 (SpeakerSleuth's τ; recalibrate on your own
   K anchor takes: the intra-anchor cosine distribution tells you what "same voice" scores on this
   model), tie-break by |Δ median F0| and |Δ speech rate|. Optionally also an ASR WER check [BON].
4. **Escalate** N (8, 16) only for lines that fail; log the seed that passed so the take is reproducible.
5. Expect the *mean* similarity to move little and the *spread* to collapse; the win is removing the
   145 Hz outliers, not moving the centre. [corrected: the "[EXPPRO] pattern" citation is withdrawn —
   that paper selects reference clips, not output draws (§4.1). This expectation is now stated as
   reasoning, with no source measuring it on any description-conditioned model.]

---

## 5. Description-level narrowing

What is documented to move the distribution:

- **Categorical, multi-field, objective** — DashScope: "Use words that describe voice qualities, such as
  'deep,' 'crisp,' or 'fast-paced'"; dimensions Gender / Age (child 5-12 … senior 55+) / Pitch (High,
  medium, low, slightly high, slightly low) / Speed / Emotion / Characteristics ("Resonant, crisp, husky,
  mellow, sweet, deep, powerful") / Use case [DS-EN]. The 12-field caption template Qwen's blog shows
  (`gender / pitch / speed / volume / age / clarity / fluency / accent / texture / emotion / tone /
  personality`) matches InstructTTSEval's APS attribute list exactly [QO §4.4, ITTSE]. Writing the
  identity block in that template, in that order, is the closest thing to speaking the model's
  training language.
- **Gender word alone is a huge lever:** "changing only 'male'/'his' to 'female'/'her' moved median F0
  from 117 Hz to 190 Hz across 47 independent designs" [MOSS-DOC] (MOSS, not Qwen — but the same
  caption-vocabulary regime).
- **Conflicting attributes break it:** "The model does not follow instructions correctly when dealing
  with conflicting attributes, such as 'high-pitched deep bass'" (getstream.io guide —
  https://getstream.io/blog/qwen3-voice-design/) [corrected: this sits in the tutorial author's own
  "Limitations" section and is not attributed to any Qwen document; the earlier "quoting Qwen's
  prompting notes" was wrong. Secondary, unmeasured.] For Gimbzo: do not stack "extremely deep" with
  anything the model reads as bright/high (e.g. "clear", "crisp").
- **Numeric attributes ("pitch around 85 Hz", exact age in years):** DashScope allows "specific years
  ('8 years old')" for age [OCDEVEL summarising DS]; **no source shows Hz values being honoured**, and
  the caption vocabulary is categorical ("Low male pitch", "Middle-aged adult"). Untested → do not rely
  on it; if tried, keep the categorical word next to it ("low, around 85 Hz") so nothing is lost if the
  number is ignored.
- **Accent:** the DashScope dimension table has no accent row [verified], and a community guide reports
  "the model defaults toward standard American or Chinese-accented English" and that community accent
  descriptors give "real-world results [that] are inconsistent" [OCDEVEL] [verified; the guide's own
  sourcing is one user quote and one mlx-audio issue about a *cloned* British accent reverting — thin];
  but the blog captions carry `accent: American English` / `accent: British English` [QO §4.4].
  For accent-neutral English the defensible move is to *state* `accent: General American English`
  (a label seen in the captions) rather than leave the field empty.
- **Recording conditions:** Parler's "very clear audio" / "very close recording" phrases are a Parler
  caption artefact [PARLER-MC]; nothing equivalent is documented for Qwen (the caption schema has no
  channel/noise field). Unknown whether "studio recording" helps; harmless to include.
- **Named speakers (Parler's "Jon"):** "To ensure speaker consistency across generations, this checkpoint
  was also trained on 34 speakers, characterized by name (e.g. Jon, Lea, Gary, Jenna, Mike, Laura)"
  [PARLER-MC]; per-speaker similarity 0.84–0.91 (Mini: Jon 0.908) where the score is "the average speaker
  similarity between a random snippet of the person speaking and a randomly Parler-generated snippet"
  [PARLER-INF] [verified: Mini 0.908 (Jon) … 0.839 (Tina); Large 0.906 (Will) … 0.848 (Barbara)]. That
  is a *training-set* fact — and the Parler maintainers' own answer to "consistent voices?" was a
  single-speaker fine-tune ("fine-tuning the model on a single speaker to fix the speaker's voice",
  sanchit-gandhi, [P11]) [verified]. Qwen VoiceDesign: `spk_id: {}` [verified in the checkpoint's
  `config.json` today]; there is no evidence a name in the instruct does anything. Parler's own community still found the named voices
  drifted enough to build audio-prefix "enrolment" on top ([P139], [P110]) — i.e. they ended up cloning too.
- **Persona prose vs field list:** both are shown officially [QO §4.5]. No source measures which is
  tighter. The Alexandria pipeline's convention — a frozen base description with the line's delivery
  "appended as delivery/emotion direction" [ALEX] — is the only field practice for problem (2); no one
  reports how much identity it costs.

---

## 6. Text-level tricks

- **Punctuation for prosody** is documented for Parler ("use commas to add small breaks in speech"
  [PARLER-MC]) and is the model-agnostic lever for delivery inside a single call (§3).
- **A fixed first sentence** does *not* fix identity in Qwen's default non-streaming mode (§2.1); it
  might in streaming mode (§2.3 hypothesis). What a fixed opening sentence *does* do, in any mode, is
  give every take an identical 1–2 s segment for computing the anchor similarity on equal footing
  (same phonemes → cleaner ECAPA comparison), which helps §4.3 step 3.
- **Sentence-initial onset instability** [I343] argues for generating short lines with a throwaway lead-in
  ("Right.") that is trimmed, or — better — not generating short lines separately at all (§3).

---

## 7. Post-hoc unification (pitch / formant to the anchor)

- Rationale: ASV embeddings weight mean pitch and spectral tilt heavily [ASV], so a median-F0 match to
  the anchor (ratio = median(anchor)/median(take), applied as a pitch shift with formant preservation)
  will raise measured similarity and remove the most audible run-to-run difference.
- Tools: Praat/parselmouth (PSOLA `Change gender…`/`Shift pitch`), pyworld (decompose F0/SP/AP, scale F0),
  Rubber Band (formant-preserving shift). Fucci et al. used F0 + formant manipulation as ASR augmentation
  (https://arxiv.org/abs/2310.06590) — proof the operation is routine, but they report no naturalness
  cost.
- Limits: no source gives a "how many semitones before it sounds processed" curve for TTS output;
  general practice is small shifts (±2–3 st). Isaac's 105→145 Hz gap is 5.6 st — too far to hide with
  a shift; that take should be rejected by §4, not corrected. Formant shifting to fake "eight-foot
  giant" depth is also uncharted for these codecs — unknown.
- Grit/rasp: the C port ships a `--roughness` "grit knob" as post-processing [CPORT]; no documentation of
  what it does internally. Rasp from the description is the sanctioned route ("husky", "gravelly",
  `texture: Resonant and slightly gravelly` in the captions [QO §4.4]).

---

## 8. Recommendations, in order of expected payoff

| # | Action | Basis | Expected effect |
|---|---|---|---|
| 1 | Freeze the identity block byte-for-byte per character (12-field template, categorical words, no conflicting attributes); append delivery as a separate trailing sentence. | [DS-EN], [QO §4.4], [ALEX], [MOSS-DOC] | Narrows the class; will not remove per-call draws. Gender/age/pitch-band adherence is high (Qwen APS 82.9 EN [PAPER Tab.8]). |
| 2 | Generate per scene (or chapter) per character in **one** `non_streaming_mode=True` call; split afterwards. | [D220], [I239], [VD-GC], [SRC-M] | Removes identity re-rolls at chunk boundaries entirely; leaves one draw per scene. |
| 3 | Best-of-N with ECAPA cosine to a hand-picked anchor (+ median-F0 / rate tie-break), seed logged. | [SLEUTH], [TORTOISE], [DS-EN] ([EXPPRO] withdrawn, §4.1) | Benchmark accuracy is against different-speaker decoys (§4.2); accuracy on same-description draws is unmeasured. Expect the spread of takes to narrow rather than the mean to move — reasoning, not a cited result. |
| 4 | `torch.manual_seed` per take, stored with the take; treat it as a reproducibility handle only. | [DEVTO], [MOSS-DOC], [TORCH] | Bit-identical re-renders of an approved take; zero cross-text benefit. |
| 5 | Try `subtalker_temperature` 0.5–0.7 with talker `temperature` 0.9 as an A/B; and `do_sample=False` on a probe. | [SRC-W], [I343], [P45] | Unmeasured. Greedy is safe on Qwen (not Parler) but fixes nothing across texts. |
| 6 | Streaming-mode fixed-prefix experiment (§2.3). | code reading only | Unknown; cheap to test; watch rate drift. |
| 7 | ±2 st formant-preserving F0 match to the anchor on accepted takes only. | [ASV] | Raises measured SIM; audible naturalness cost unmeasured. |

What no amount of the above delivers: a *reusable* identity object. Every engine surveyed that actually
solved consistency did so by capturing a latent (ChatTTS `spk_emb`, Tortoise conditioning latents,
Deep Dubbing's Text-to-Timbre embedding, Parler enrolment prefix, Qwen `create_voice_clone_prompt`,
DashScope `voice` ID). Inside the "no clip, no Base, no RVC" boundary the ceiling is "one draw per scene,
selected by similarity", which is what Qwen's own hosted product does before it hands you a voice ID.

---

## 9. Things explicitly not found (so nobody should claim them)

- Any Qwen maintainer statement about seeds, greedy decoding, or per-line consistency for VoiceDesign.
- Any measurement of Qwen VoiceDesign run-to-run speaker similarity (cosine) at any temperature.
- Any evidence that numeric Hz, a speaker *name*, or "recording condition" phrases change Qwen's draw.
- Any published effect size for `subtalker_temperature`.
- Any ROCm-specific determinism statement for SDPA/Qwen inference.
- Any naturalness-vs-semitone curve for pitch-shifting codec-LM TTS output.

---

## Verification

Skeptic pass, 12 Sep 2026. Every key finding was re-checked against its cited source (raw GitHub
files and the safetensors header via HTTP; issue/discussion comments via the GitHub REST API so
that collapsed threads were read in full; arXiv PDFs/HTML; vendor pages via curl). Marks used in the
body: **[verified]**, **[corrected: …]**, strike-through for withdrawn claims.

### Held as written (quote present, meaning as stated)

| Finding | Status |
|---|---|
| No speaker slot in VoiceDesign: `speaker_embed = None` on the instruct path; 404 tensors all under `talker.`; `spk_id: {}` | Verified against `main` (l.2088-2089, 2166-2172) and the live checkpoint header/config. Repo last commit 2026-03-17, PyPI 0.1.1 (Feb 2026), no newer VoiceDesign weights — nothing stale. |
| Seed reproduces a take, not a voice (2.2 / 7.6 st on MOSS) | Verbatim in [MOSS-DOC]. MOSS, not Qwen — the report says so. |
| DashScope "Generate multiple voices, listen to them, and select the best one" | Verbatim, from the page's FAQ ("Voice Design involves randomness, so the same description may produce slightly different voices each time…"). Page covers CosyVoice VD and Qwen3-TTS-VD jointly. |
| [D220] storm-fox drift quote; no maintainer reply in #220 / HF #3 / #298 | Verbatim; every commenter `author_association: NONE`. |
| Parler `do_sample=False` → noise | Verbatim in PR #110 ("temperatute" typo is in the source); #45 confirmed incl. `min_new_tokens=10` suggestion and "No, it doesn't work for me". |
| Batching = independent left-padded rows; VoiceDesign default `non_streaming_mode=True`; `max_new_tokens=8192` from generation_config overrides the wrapper's 2048 | Verified in code. |
| SpeakerSleuth τ values and 97.8/99.0/100/100 (ECAPA pairwise & centroid), WavLM 96.7/95.5/79.9/100, Reference-ECAPA 97.8/92.0/99.4/76.2, NDCG@2 99.6 | Verbatim from Table 2 of the PDF. |
| Tortoise `num_autoregressive_samples` / `cvvp_amount` docstrings | Verbatim; presets 16/96/256/256; `cvvp_amount` default 0.0. |
| [ASV] "static spectral information (mean pitch, HNR, shimmer, α-ratio)" and "fail to capture dynamic behavioral identity markers…" | Verbatim (Carbonneau et al., Ubisoft La Forge); ECAPA-TDNN is among the seven embeddings studied. |
| Parler 34 named speakers; per-speaker SIM 0.84–0.91 | Verbatim on model card and INFERENCE.md. |
| MOSS gender-word swap 117→190 Hz over 47 designs | Verbatim. |
| VoxCPM2 "generate 1~3 times" | Verbatim, in the README's Risks and Limitations, VoxCPM2-specific. |
| ChatTTS `sample_random_speaker` / "save it for later timbre recovery" | Verbatim. |
| Alexandria "Set a base voice description … appended as delivery/emotion direction"; Batch Seed; no similarity filter | Verbatim in the README. |
| PyTorch "not guaranteed across PyTorch releases, individual commits, or different platforms"; SDPA forward deterministic on all backends, backward not | Verbatim on the 2.13 page; no ROCm/HIP mention there (as the report says). |
| README "Voice Design then Clone"; kobold maintainer "cannot re-use a voice … use Q3ttsBase to clone" | Verified. |
| C port `--seed`, `--temperature` default 0.5, `--roughness`, "batch output bit-identical to single-stream"; speaker-map.md x-vector sentence | Verified (the x-vector sentence is in `docs/speaker-map.md` l.23, not the README). |

### Corrected

1. **[I343] 15 % onset-flip under greedy** — real quote, but the model is a LoRA fine-tune of
   1.7B-Base on 21 min of one speaker, and the thread's only reply blames a speaker-encoder decay bug
   in the SFT script (PR #351). Weak evidence for "identity is decided at onset" in VoiceDesign.
2. **Tech-report ">10 minutes" as evidence identity holds within a generation** — that claim is about
   content consistency (WER) on an internal long-form set. Withdrawn as support for §0.4.
3. **[PAPER §1] quote** — was a splice of the abstract and a §1 sentence; replaced with the single
   verbatim sentence.
4. **[I239] "0.0 % vs +16.7 %"** — verbatim, but measured on Base voice-cloning with a 12.9 s
   reference; only the *default* for VoiceDesign is code-verified, not VoiceDesign pacing. The comment
   is itself footered "Generated with Claude Code".
5. **[DEVTO]** — verbatim, but the article names no Qwen model/runtime, has no measurements, and its
   fix is a `.pt` speaker embedding from a saved WAV (a clone). Downgraded from "Qwen-specific
   confirmation" to "Qwen-family anecdote".
6. **[EXPPRO] "prompt selection by speaker similarity … halved variance"** — mischaracterised. ExpPro
   selects reference *prompt clips* for zero-shot cloning by pitch/DNSMOS/emotion-coherence and does
   not generate multiple candidates; SIM is only its evaluation metric. Struck from §4.1, §4.3, §8.
7. **SpeakerSleuth "97.8–100 %"** — verbatim, but the decoys are an opposite-gender voice and an
   ECAPA-nearest *other human*, so the figure does not transfer to ranking same-description draws;
   "measurably converges" softened to "plausibly converges".
8. **getstream "conflicting attributes"** — the tutorial author's own limitation note, not "Qwen's
   prompting notes".
9. **[OCDEVEL] accent wording** — quotes tightened to what the page actually says; its own evidence is
   one user comment and one *clone* issue.

### Unsupported / from memory (flagged, not removed)

- "Codec-LM prompting in general (AudioLM/VALL-E) conditions identity on the first ~3 s of acoustic
  tokens" (§2.3) — no citation; background knowledge. Left as context, carries no weight.
- "DeepWiki summary recommends 0.7–0.8" (§2.2) — labelled secondary/unmeasured in the original;
  not re-checked.
- [P14] user quote "similar but different voice with same discription…" — not re-located (only the
  maintainer replies on #11/#14 were pulled); the maintainers' single-speaker-fine-tune answer is
  verified and is the load-bearing part.
- Table rows for **CosyVoice instruct** and **Maya1** carry no quotes; they are characterisations.

### Missing relative to the angle asked

- **No measurement of Qwen VoiceDesign itself**: nobody (including this report) has run N draws of one
  instruct and reported ECAPA cosine, median-F0 spread or gender-flip rate. Every number in the
  report comes from MOSS, Parler, SpeakerSleuth or a Qwen *fine-tune*. The 105 vs 145 Hz observation
  in the brief is currently the only VoiceDesign datum.
- **Delivery-direction cost (problem 2)**: the angle asked how practitioners direct a line (cold,
  quiet, a laugh) *without* the voice changing. The only field practice found is Alexandria's
  base-description-plus-appended-direction; no one measured whether appending "quiet, cold" moves the
  identity draw more than re-rolling the seed does. This is the most important unanswered question
  for the cast files and is not answerable from sources today.
- **Sampler knobs**: no source at all on `subtalker_temperature`, `top_k`, or `repetition_penalty`
  effects on identity spread for VoiceDesign (DeepWiki-style summaries restate the defaults).
- **Comparison engines in depth**: CosyVoice 3 / Maya1 / MOSS are covered by one quote each;
  MOSS-DOC's chunk-drift figure (13 st span, 2.3 st median neighbour jump) had been omitted and is
  now added to §2.1.
- **Threshold calibration**: the report imported τ=0.4 from a 192-d SpeechBrain ECAPA benchmark on
  human dialogue; the only Qwen-adjacent same-speaker cosine figure (~0.7 pairwise, 0.85+ to
  centroid, Baseten, Qwen's own 2048-d encoder) shows numbers do not transfer between encoders.
  Added to §4.2.
- **ROCm determinism**: explicitly unknown in the report; still unknown after this pass (the one
  ROCm data point, MOSS on a Radeon R9700 via audio.cpp, is a different runtime).
- **vLLM-Omni seed parameter** for Qwen3-TTS is mentioned by [I298] users but its semantics for
  VoiceDesign were not investigated.

### Surviving key findings (post-verification)

1. VoiceDesign has no identity slot; identity is sampled codec tokens per call (code + checkpoint verified).
2. A seed reproduces a take, not a voice (MOSS measured; Qwen anecdotal; mechanism verified in code —
   non-streaming prefill makes frame-0 logits depend on the whole text).
3. DashScope's own guidance is human best-of-N then a stored voice ID; open weights give only the first half.
4. Long-form users report cadence/emotion drift at chunk boundaries with identity mostly holding
   inside one generation; no maintainer response anywhere.
5. Greedy decoding wrecks Parler; on Qwen it is deterministic per input but does nothing across texts
   (and the one Qwen datum is a fine-tune with a suspected training bug).
6. Batching is N independent draws; VoiceDesign's default is one non-streaming prefill with up to
   8192 frames, so one scene per call is one identity draw.
7. ECAPA-based ranking is the standard tool for candidate selection and a reject line must be
   calibrated on your own anchor takes; benchmark accuracies do not transfer.
8. Speaker embeddings encode static spectral identity, not cadence — pair cosine with F0/rate checks.
9. Parler's named-speaker consistency is a training-time device with no Qwen VoiceDesign equivalent.
10. Description wording moves coarse attributes strongly (gender: 117→190 Hz on MOSS); no evidence any
    of these models honour numeric Hz.
11. VoxCPM2 documents the same per-run variance and prescribes retries.
12. Every engine that solved consistency captured a latent; within no-clip constraints the ceiling is
    one draw per scene plus similarity selection.
13. Appending per-line direction to a frozen base description is the only documented field practice
    for direction-without-clone; its identity cost is unmeasured.
14. PyTorch: cross-platform reproducibility not guaranteed; SDPA forward deterministic; ROCm unknown.
