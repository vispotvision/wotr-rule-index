# Qwen3-TTS-12Hz-1.7B-VoiceDesign — what the OFFICIAL material actually says

Survey date: 12 Sep 2026. Scope: Qwen's own sources only — the HF model card and cached
repo files, the GitHub README / examples / finetuning docs, the technical report
(arXiv 2601.15621), the two qwen.ai blog posts, the DashScope voice-design API docs,
the `qwen-tts` package source (v0.1.1, installed at `C:\venvs\wotr-qwen`), and GitHub
issues where a Qwen collaborator replied. Community folklore is out of scope here and is
flagged as such where it appears.

Everything in quotes is verbatim. Where the official material is silent I say so.

Sources used (short handles used below):

- **[MC]** model card — https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign (README is a 3 KB stub; the CustomVoice example is the only code on it)
- **[CFG]** cached repo files — `C:\Users\isaac\.cache\huggingface\hub\models--Qwen--Qwen3-TTS-12Hz-1.7B-VoiceDesign\snapshots\5ecdb673…\{config.json,generation_config.json}`
- **[GH]** GitHub README — https://github.com/QwenLM/Qwen3-TTS (raw: https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/README.md)
- **[EX]** example script — https://github.com/QwenLM/Qwen3-TTS/blob/main/examples/test_model_12hz_voice_design.py
- **[FT]** finetuning README — https://github.com/QwenLM/Qwen3-TTS/blob/main/finetuning/README.md
- **[PAPER]** technical report, HTML — https://arxiv.org/html/2601.15621
- **[BLOG1]** release blog, 22 Jan 2026 — https://qwen.ai/blog?id=qwen3tts-0115 (JS-rendered; read via browser)
- **[BLOG0]** earlier API blog, 23 Dec 2025 — https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign [corrected: this post is about the **hosted** `Qwen3-TTS-VD-Flash` API model (`target_model: qwen3-tts-vd-realtime-2025-12-16`), released a month before the open weights. Nothing on it is a sample from the open `12Hz-1.7B-VoiceDesign` checkpoint; treat its instruct strings as same-family evidence only]
- **[DS-EN]** DashScope voice-design doc (EN) — https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-design [verified 12 Sep 2026; page shows "Last Updated: Sep 11, 2026" and covers the hosted `qwen3-tts-vd-2026-01-26` / `qwen3-tts-vd-realtime-2026-01-15` models, not the open checkpoint]
- **[DS-ZH]** DashScope voice-design doc (ZH) — https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design
- **[SRC]** package source — `C:\venvs\wotr-qwen\Lib\site-packages\qwen_tts\inference\qwen3_tts_model.py` and `…\core\models\modeling_qwen3_tts.py` (mirrors https://github.com/QwenLM/Qwen3-TTS/tree/main/qwen_tts)
- **[SPACE]** HF Space demo — https://huggingface.co/spaces/Qwen/Qwen3-TTS/blob/main/app.py
- **[I9]** issue #9 (non-verbal cues) — https://github.com/QwenLM/Qwen3-TTS/issues/9
- **[I16]** issue #16 (unwanted laughter) — https://github.com/QwenLM/Qwen3-TTS/issues/16
- **[I298]** issue #298 (same input, same output?) — https://github.com/QwenLM/Qwen3-TTS/issues/298
- **[I239]/[PR362]** speaking-rate drift — https://github.com/QwenLM/Qwen3-TTS/issues/239 , https://github.com/QwenLM/Qwen3-TTS/pull/362
- **[D220]** discussion #220 (keep designed voices) — https://github.com/QwenLM/Qwen3-TTS/discussions/220

---

## 1. Bottom line for Isaac's three problems

| Problem | What the official material says |
|---|---|
| (1) Same brief → different voice each run | Officially acknowledged and *not* fixable with a seed in the shipped package. DashScope doc: "Voice Design involves randomness, so the same description may produce slightly different voices each time. Generate multiple voices, listen to them, and select the best one." [DS-EN]. The package exposes no seed argument at all [SRC]. The **official** consistency mechanism is "Voice Design then Clone": generate one reference clip with VoiceDesign, then drive every line through the Base model's `voice_clone_prompt` [GH]. A collaborator says the same in [I16]. That means Isaac's "pure voice-design, no Base clone" constraint is directly at odds with the only sanctioned consistency path. |
| (2) Per-line delivery without changing the voice | In the VoiceDesign model timbre and delivery live in the *same* instruct string; there is no separate "style" channel. The training-caption schema (§4) keeps them as separate labelled fields (`pitch/texture/age` vs `emotion/tone/speed/volume`), so the least-bad approach inside pure VoiceDesign is to hold the timbre fields byte-identical and vary only the delivery fields. The blog explicitly shows "Gradual Control" examples where a single instruct describes a delivery *arc* within one line ("Starts measured, then accelerates rapidly during emotional outburst") [BLOG1]. The model built for timbre-fixed style control is CustomVoice ~~/Base+instruct~~ [corrected: `generate_voice_clone` on the Base model takes **no** `instruct` argument (SRC line 470 ff.); only `generate_custom_voice` does, and only for its 9 preset speakers. So in the open weights there is no path at all that combines a cloned/designed timbre with a free-text delivery instruct], not VoiceDesign. |
| (3) Reliably getting rasp/depth/age/accent-neutral English | The training captions carry explicit `pitch`, `age`, `accent`, `texture` fields with vocabulary like "Low male pitch", "Resonant and slightly gravelly", "Middle-aged adult", "General American English" [BLOG1]. Accent is a *named field* — "General American English", "British English", "标准普通话" — so leaving it out means the model picks. DashScope's attribute table gives the sanctioned adjective list ("Resonant, crisp, husky, mellow, sweet, deep, powerful") [DS-EN]. Nothing official goes beyond "middle-aged"/"senior" for age or "low"/"slightly low" for pitch; "eight-foot giant" style persona prose is supported in the "Background Information" format but no official example pushes pitch to the extreme. |

---

## 2. Generation kwargs — the exact defaults

### 2.1 `generation_config.json` shipped in the VoiceDesign repo [CFG]

```json
{
  "do_sample": true,
  "repetition_penalty": 1.05,
  "temperature": 0.9,
  "top_p": 1.0,
  "top_k": 50,
  "subtalker_dosample": true,
  "subtalker_temperature": 0.9,
  "subtalker_top_p": 1.0,
  "subtalker_top_k": 50,
  "max_new_tokens": 8192
}
```

### 2.2 How the wrapper resolves them [SRC, `qwen3_tts_model.py` lines 287-352]

`_merge_generate_kwargs` rule, verbatim from the docstring:

> "If the user explicitly passes a value (not None), use it. Otherwise, use the value from generate_config.json if present. Otherwise, fall back to the hard defaults."

Hard defaults in code (only used if the JSON is missing a key): `do_sample=True, top_k=50, top_p=1.0, temperature=0.9, repetition_penalty=1.05, subtalker_dosample=True, subtalker_top_k=50, subtalker_top_p=1.0, subtalker_temperature=0.9, max_new_tokens=2048`.

Note the discrepancy: hard default `max_new_tokens=2048`, but the shipped JSON says `8192`, and the JSON wins. `Qwen3TTSForConditionalGeneration.generate()` itself defaults `max_new_tokens=4096` but is always overridden by the wrapper. Also `min_new_tokens=2` is hard-wired, and `eos_token_id` defaults to `codec_eos_token_id` (2150).

The comment in `from_pretrained` says it loads "`generate_config.json`", but the modeling code actually loads **`generation_config.json`** (`modeling_qwen3_tts.py` line 1924) — the README's Evaluation section also calls it `generate_config.json`. Same file, sloppy naming.

### 2.3 What the two sampler groups control [SRC + CFG]

- `temperature/top_k/top_p/repetition_penalty/do_sample` → the **talker** (28-layer, hidden 2048) predicting codebook 0 (the semantic codebook) each 12.5 Hz frame.
- `subtalker_*` → the **code predictor / MTP module** (5-layer, hidden 1024, `num_code_groups: 16`) that fills in the 15 residual acoustic codebooks for each frame: `max_new_tokens=self.config.num_code_groups - 1` per frame (modeling line 1673). Docstring: "Sampling switch for the sub-talker (only valid for qwen3-tts-tokenizer-v2)" — the 12Hz tokenizer *is* v2, so these are live for this model.
- Paper: "the backbone ingests aggregated codebook features to predict the zeroth codebook, and an MTP (Multi-Token Prediction) module then generates all residual codebooks" [PAPER §3.1]. Tokenizer: "Its first codebook layer encodes semantic content, while the subsequent layers capture acoustic details" [PAPER §1]. So the sub-talker samplers are the ones that touch timbre detail; the official material does not say anything about lowering `subtalker_temperature` for consistency — that is untested inference on my part, not a finding.
- `suppress_tokens` is hard-set to the last 1024 talker vocab entries except EOS (modeling lines 2059-2063) — the control-token range is masked during generation.

### 2.4 Evaluation settings the team used [GH §Evaluation]

> "During evaluation, we ran inference for all models with `dtype=torch.bfloat16` and set `max_new_tokens=2048`. All other sampling parameters used the defaults from the checkpoint's `generate_config.json`. For the Seed-Test and InstructTTS-Eval test sets, we set `language="auto"`, while for all other test sets we explicitly passed the corresponding `language`."

So the InstructTTSEval numbers (the voice-design benchmark) were produced with **`language="auto"`** and `max_new_tokens=2048`.

---

## 3. What `non_streaming_mode` changes

Docstring (identical on all three generate methods) [SRC]:

> "Using non-streaming text input, this option currently only simulates streaming text input when set to `false`, rather than enabling true streaming input or streaming generation."

Defaults: `generate_voice_design(... non_streaming_mode: bool = True)` and `generate_custom_voice(... = True)`; `generate_voice_clone(... = False)`.

Mechanically (modeling lines 2199-2232): with `non_streaming_mode=True` the whole target text (plus `tts_eos`) is laid down in the prefill, summed with `codec_pad` embeddings, and then a `codec_bos`; the trailing text hidden is just `tts_pad`. With `False`, only the first text token is in the prefill and the rest is fed one text token per generated codec frame ("trailing_text_hiddens"). A user-authored PR [PR362] measured that the streaming layout makes the speaking rate climb over long generations ("+16.7%" within one ~25 s clip vs "0.0%" non-streaming) and asks for the Base default to be flipped to `True` — i.e. to what VoiceDesign already does. No maintainer has responded on that PR as of this survey. [verified: PR #362 opened 28 Aug 2026 by `sherifhanna700` (no association), still open/unmerged, only user comments. Caveat the report under-stated: every number in that PR was measured on **1.7B-Base voice clone with a 12.9 s reference clip**, and the PR's own mechanism analysis says the long reference "pre-consumes" the target text and makes the drift "much worse". There is no measurement of the streaming layout on VoiceDesign, which has no reference clip; the transfer to VoiceDesign is inference.] **For Isaac: leave `non_streaming_mode=True` (the default) for VoiceDesign.** The official HF Space also hard-codes `non_streaming_mode=True, max_new_tokens=2048` in its VoiceDesign call [SPACE lines 156-162].

---

## 4. The description schema the model was trained on

### 4.1 What the paper says (almost nothing) [PAPER §3.2-3.3]

> "All data is formatted in ChatML to standardize inputs and support controllable speech generation."

> "Qwen3-TTS supports streaming voice cloning, voice design, and fine-grained control. To achieve this, we prepend user-provided instructions containing fine-grained control signals to the input sequences."

> "For voice design, built upon the Qwen3 text model foundation, Qwen3-TTS inherits robust text comprehension capabilities. Additionally, we introduce a probabilistically activated thinking pattern during training to improve instruction following, especially for complex descriptions. Furthermore, based on this strong instruction-following capability, Qwen3-TTS controls predefined voices with desired styles."

That is the entire description of instruction data. **No attribute list, no caption source, no example instruct, no dataset size** appears in the report. Emotion, laughter and paralinguistic tags are not mentioned anywhere in the paper [verified: zero hits for "emotion", "laugh", "paralinguistic" in the HTML]. ~~The word "accent" does not appear.~~ [corrected: "accent" appears exactly once, in the cross-lingual voice-clone evaluation ("superior content consistency and reduced accent drift"), never in a voice-design context.] The report's Table 1 also lists a `Qwen3-TTS-25Hz-1.7B-VoiceEditing` model (not released) as the one with all four ticks including "Voice Clone" + "Instruction Following".

### 4.2 The prompt format at inference [SRC lines 269-276]

```
instruct → "<|im_start|>user\n{instruct}<|im_end|>\n"
text     → "<|im_start|>assistant\n{text}<|im_end|>\n<|im_start|>assistant\n"
```

The instruct block is embedded with the talker's text embedding + projection and **prepended** to the sequence; then a codec prefix; then the text. Empty instruct is allowed ("Empty string is allowed (treated as no instruction)").

### 4.3 The "thinking pattern" at inference = the language token [SRC lines 2110-2147, CFG]

`config.json` has `codec_think_id: 2154, codec_nothink_id: 2155, codec_think_bos_id: 2156, codec_think_eos_id: 2157` and `codec_language_id: {chinese 2055, english 2050, german 2053, italian 2070, portuguese 2071, spanish 2054, japanese 2058, korean 2064, french 2061, russian 2069}`.

- `language="Auto"` → prefix `[nothink, think_bos, think_eos]` (language_id = None)
- `language="English"` → prefix `[think, think_bos, 2050, think_eos]`

So the only "thought" the released model ever emits is the language tag; the paper's "probabilistically activated thinking pattern" is why both prefixes are valid. The team's own benchmark runs used `"auto"` (§2.4). There is no official statement on whether explicit `"English"` helps or hurts voice-design fidelity; the README code examples pass explicit languages, the HF Space default is `"Auto"` [SPACE line 257].

`spk_id` and `spk_is_dialect` are empty `{}` in the VoiceDesign config — no preset speakers, and the "dialect" branch can never trigger.

### 4.4 The structured caption format — the strongest evidence of the training schema [BLOG1, BLOG0]

The release blog's VoiceDesign sample table shows instructs in a fixed **twelve-field, key: value** template, in the same order in English and Chinese. This is almost certainly the auto-caption format used to label training speech; it is the single most useful thing in the official material.

English instance (verbatim, "Acoustic Attribute Control" row, Gordon-Ramsay-style text):

```
gender: Male.
pitch: Low male pitch with significant upward inflections for emphasis and excitement.
speed: Fast-paced delivery with deliberate pauses for dramatic effect.
volume: Loud and projecting, increasing notably during moments of praise and announcements.
age: Young adult to middle-aged adult.
clarity: Highly articulate and distinct pronunciation.
fluency: Very fluent speech with no hesitations.
accent: British English.
texture: Bright and clear vocal texture.
emotion: Enthusiastic and excited, especially when complimenting.
tone: Upbeat, authoritative, and performative.
personality: Confident, extroverted, and engaging.
```

English instance (verbatim, "Age Control" row — the closest official example to a Darius/Gimbzo register):

```
gender: Male.
pitch: Low male pitch, generally stable.
speed: Deliberate pace, slowing slightly after the initial exclamation.
volume: Starts loud, then transitions to a projected conversational volume.
age: Middle-aged adult.
clarity: High clarity with distinct pronunciation.
fluency: Highly fluent.
accent: American English.
texture: Resonant and slightly gravelly.
emotion: Initially commanding, shifting to narrative amusement.
tone: Authoritative start, moving to an engaging, descriptive tone.
personality: Confident and performative.
```
(text: "Older gentleman, 110, maybe 111 years old, sort of a surly Elvis thing happening with him. He smiles like this. Seen him around?")

English instance (verbatim, "Acoustic Attribute Control", character-voice row):

```
gender: Male.
pitch: Artificially high-pitched, slightly lowering after the initial laugh.
speed: Rapid during the laugh, then slowing to a deliberate pace.
volume: Loud laugh transitioning to a standard conversational level.
age: Young adult to middle-aged, performing a character voice.
clarity: Clear and distinct articulation.
fluency: Fluent delivery without hesitation.
accent: American English.
texture: Slightly strained and somewhat nasal quality.
emotion: Forced amusement shifting to feigned resignation.
tone: Initially playful, then shifts to a slightly put-upon tone.
personality: Theatrical and expressive.
```
(text: "Good one. Okay, fine, I'm just gonna leave this sock monkey here. Goodbye.")

English instance (verbatim, "Gradual Control" row):

```
gender: Female.
pitch: Mid-range female pitch, rising sharply with frustration.
speed: Starts measured, then accelerates rapidly during emotional outburst.
volume: Begins conversational, escalates quickly to loud and forceful.
age: Young adult to middle-aged.
clarity: High clarity and distinct articulation throughout.
fluency: Highly fluent with no significant pauses or fillers.
accent: General American English.
texture: Bright and clear vocal quality.
emotion: Shifts abruptly from neutral acceptance to intense resentment and anger.
tone: Initially accepting, becomes sharply accusatory and confrontational.
personality: Assertive and emotionally expressive when provoked.
```

Chinese instances use the identical field order: `性别 / 音高 / 语速 / 音量 / 年龄 / 清晰度 / 流畅度 / 口音 / 音色质感 / 情绪 / 语调 / 性格`. Example (verbatim, "Age Control"):

```
性别: 男性.
音高: 男性低沉音域，音高稳定.
语速: 语速稍快，节奏紧凑.
音量: 音量洪亮，力度强劲.
年龄: 中老年.
清晰度: 发音清晰，字句有力.
流畅度: 表达流畅，一气呵成.
口音: 标准普通话.
音色质感: 嗓音浑厚，略带沙哑感.
情绪: 严肃告诫，指令明确.
语调: 命令式语调，强调果断.
性格: 权威果断，不容置喙.
```

[BLOG0] adds a 13-field variant with a leading `role:` field, run together on one line (verbatim, truncated) [corrected: this sample is from the hosted VD-Flash API model, not the open checkpoint — it shows the same caption template exists in the family, but it is not evidence of what the 12Hz-1.7B open weights were trained on]:

> "role: Mid-level Corporate Project Manager. gender: Male. pitch: Dynamic male pitch, starting mid-high with agitation, transitioning to a lower declarative range, and spiking upwards with intense emphasis such as 'so finished!'. speed: Variable speaking rate; initially rapid during agitated states ('Damn it!'), slowing for declarative statements like 'I'm done', then accelerating again with strong emotional delivery ('so finished!').. volume: Significant dynamic range; … age: Middle-aged adult. clarity: Consistently clear articulation, maintained even during rapid or loud emotional expressions.. fluency: … accent: General American English. texture: Predominantly forceful, becoming strained during agitated outbursts and shouting, otherwise resonant and firm during calmer declarations.. emotion: Starts with pronounced frustration and exasperation ('Damn it!'), shifts to resolute decisiveness ('I'm done'), culminating in an intensely emphatic declaration of finality ('I am so finished!').. tone: … personality: Assertive and emotionally expressive, demonstrating a build-up of frustration leading to a decisive, forceful resolution.."

Observations from the template (these are observations, not official statements):
- The captions describe *the specific clip*, including delivery changes within it and quoted words from the text. The model was trained to map "this description → this exact performance", which is why one instruct produces both timbre and line reading.
- `pitch`, `age`, `texture`, `accent`, `gender` are the stable-identity fields; `speed`, `volume`, `emotion`, `tone` are the per-clip delivery fields; `clarity`, `fluency`, `personality` sit between.
- Accent is always named ("British English", "American English", "General American English", "标准普通话"). Accent-neutral English is therefore expressible as a field value; no official example uses "neutral", but "General American English" is the recurring default.
- Pitch vocabulary in the official examples never goes beyond "Low male pitch" / "男性低沉音域" / "moderately low pitch". No example says "bass", "subsonic", or gives Hz.

### 4.5 Free-prose and persona formats also shown officially [BLOG1, BLOG0, GH]

Short style-only instructs (the model also accepts *no* timbre information — it invents one):
- `"Speak in an incredulous tone, but with a hint of panic beginning to creep into your voice."` [GH, EX, SPACE default]
- `"Speak as a sarcastic, assertive teenage girl: crisp enunciation, controlled volume, with vocal emphasis that conveys disdain and authority."` [BLOG1]
- `"体现撒娇稚嫩的萝莉女声，音调偏高且起伏明显，营造出黏人、做作又刻意卖萌的听觉效果。"` [GH, EX, BLOG1]
- `"邪恶女魔头"` and `"Playful Homebody Sis"` — 4-word persona-only instructs [BLOG0, "Persona role-play: concise/rich"] [verified, but hosted VD-Flash samples — see BLOG0 note above]

Compact comma-list format (the one the README uses for reuse):
- `"Male, 17 years old, tenor range, gaining confidence - deeper breath support now, though vowels still tighten when nervous"` [GH "Voice Design then Clone"; BLOG1 "Lucas"] [verified — the only compact-format instruct that is demonstrably run through the open checkpoint (README code, with `language="English"` passed explicitly)]
- `"Female, 16 years old, mezzo-soprano range, softening - lowering register to intimate speaking voice, consonants softening"` [BLOG1 "Mia"] [verified; the BLOG1 Lucas/Mia dialogue sits under "Timbre Reuse", i.e. hosted stored-voice generation]
- `"Male, middle-aged, booming baritone - hyper-energetic infomercial voice with rapid-fire delivery and exaggerated pitch rises, dripping with salesmanship"` [BLOG0] [verified; hosted VD-Flash sample]
- `"Male, 30s, strained tenor - breathy sobs interrupt speech, pitch swings wildly between whispers and wails"` [BLOG0] [verified; hosted VD-Flash sample]

Long natural-prose format:
- `"A relaxed, naturally expressive male voice in his late twenties to early thirties, with a moderately low pitch, casual speaking rate, and conversational volume; deliver lines with a light, self-deprecating tone, breaking into genuine, easygoing laughter at moments of embarrassment, while maintaining clear articulation and an overall warm, approachable clarity."` [BLOG1 "Human-likeness"] — paired with a text that *writes the laughs in*: "…Which is—heh—convenient, sure, I guess? … huh… ha Seriously, I sound like a Hallmark card all of a sudden."

"Background Information" / character-card format (verbatim, BLOG1):

```
Character Name: Marcus Cole
Voice Profile: A bright, agile male voice with a natural upward lift, delivering lines at a brisk, energetic pace. Pitch leans high with spark, volume projects clearly—near-shouting at peaks—to convey urgency and excitement. Speech flows seamlessly, fluently, each word sharply defined, riding a current of dynamic rhythm.
Background: Longtime broadcast booth announcer for national television, specializing in live interstitials and public engagement spots. His voice bridges segments, rallies action, and keeps momentum alive—from voter drives to entertainment news.
Presence: Late 50s, neatly groomed, dressed in a crisp shirt under studio lights. Moves with practiced ease, eyes locked on the script, energy coiled and ready.
Personality: Energetic, precise, inherently engaging. He doesn't just read—he propels. Behind the speed is intent: to inform fast, to move people to act. Whether it's "text VOTE to 5703" or a star-studded tease, he makes it feel immediate, vital.
```

Chinese equivalent uses `角色姓名 / 音色信息 / 身份背景 / 外貌特征 / 性格特质 / 人生信条` for a "年近七十的资深战略科学家" (a scientist near seventy) whose 音色信息 is "音量洪亮，音域低沉，力度感强的中年男性声音" — note the *voice* line says "middle-aged male" while the *background* says near seventy. [BLOG1]

[BLOG0] also shows a "Background information" row where the whole instruct is an encyclopaedia paragraph about the Dylan Thomas poem, and another that is a paragraph about 《少年闰土》 — i.e. the model accepts non-voice context as the instruct. [verified, hosted VD-Flash sample; the open-checkpoint blog (BLOG1) shows only the two character-card "Background Information" rows, not the encyclopaedia-paragraph kind.]

Blog statement on what an instruct may contain: "Users can freely input acoustic attributes, persona descriptions, background information, and other free-form descriptions, easily creating their desired voice identities." [BLOG1]

### 4.6 DashScope's official "how to write a description" guidance [DS-EN, DS-ZH]

This is written for the hosted `qwen3-tts-vd-*` models, which are the same family; it is the only official prose guidance on writing prompts.

Five principles (verbatim):

> "1. Be specific, not vague: Use words that describe voice qualities, such as "deep," "crisp," or "fast-paced." Avoid subjective or ambiguous terms like "nice" or "normal." 2. Be multi-dimensional, not one-dimensional: A good description covers multiple dimensions (such as gender, age, and emotion). Describing only "female voice" is too broad to produce a distinctive result. 3. Be objective, not subjective: Focus on the physical and perceptual characteristics of the voice. For example, use "high-pitched with an energetic tone" instead of "my favorite voice." 4. Be original, not imitative: Describe voice qualities instead of requesting imitation of specific individuals (such as celebrities or actors). The model doesn't support imitation, and such requests may raise copyright concerns. 5. Be concise, not redundant: Avoid repeating synonyms or adding meaningless modifiers. Make sure every word serves a clear purpose."

Dimension table (verbatim values):

| Dimension | Examples |
|---|---|
| Gender | "Male, female, neutral" |
| Age | "Child (5-12), teenager (13-18), young adult (19-35), middle-aged (36-55), senior (55+)" |
| Pitch | "High, medium, low, slightly high, slightly low" |
| Speed | "Fast, medium, slow, slightly fast, slightly slow" |
| Emotion | "Cheerful, calm, gentle, serious, lively, composed, soothing" |
| Characteristics | "Resonant, crisp, husky, mellow, sweet, deep, powerful" |
| Use case | "News broadcast, advertising, audiobook, animation character, voice assistant, documentary narration" |

Chinese table: 性别 "男性、女性、中性"; 年龄 "儿童(5-12岁)、青少年、青年、中年、老年"; 音高 "高音、中音、低音、偏高、偏低"; 语速 "快速、中速、缓慢、偏快、偏慢"; 情感 "开朗、沉稳、温柔、严肃、活泼、冷静、治愈"; 特点 "有磁性、清脆、沙哑、圆润、甜美、浑厚、有力"; 用途 "新闻播报、广告配音、有声书、动画角色、语音助手".

Example descriptions (verbatim):
- "Standard broadcast style: clear and precise articulation with perfect enunciation"
- "Young and lively female voice, fast-paced with a noticeable rising intonation, suited for fashion product presentations"
- "Calm, slow-paced middle-aged male voice, deep and resonant, suited for news reading or documentary narration"
- "Gentle and thoughtful female, around 30 years old, even-toned, suited for audio book reading"
- "Cute child's voice, approximately an 8-year-old girl, slightly childish speech, suited for animation character voiceover"
- API sample `voice_prompt`: "A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation, is suitable for news broadcasting or documentary commentary." [BLOG0] [verified; it is the `qwen-voice-design` API request body for `qwen3-tts-vd-realtime-2025-12-16`]

Limits and language: "Up to 500 characters for CosyVoice and up to 2,048 characters for Qwen-TTS." "Voice descriptions support Chinese and English only" — while "the generated voice can synthesize speech in multiple languages." [DS-EN]. (The open-source package has no character limit on `instruct` — see §7.)

### 4.7 CustomVoice instruct examples (style-only, timbre fixed) [GH, BLOG1]

Useful as a vocabulary of *delivery-only* instructs the family was trained on:
`"用特别愤怒的语气说"`, `"Very happy."` [both in GH README code], `"spoke with a very sad and tearful voice."`, `"请特别小声的悄悄说"`, `"Speaking at an extremely slow pace"`, `"音调低沉"` [corrected: these four are BLOG1 "Single Attribute Control" rows only, not in the README], and the HF Space placeholder `"e.g., Speak in a cheerful and energetic tone"` [SPACE line 356, verified]. The blog's CustomVoice "Multi-Attribute Control" rows use the same 12-field template as §4.4 — so the template is shared across VoiceDesign and CustomVoice training.

---

## 5. Emotion, laughter and paralinguistic tags

- **No tag vocabulary exists.** Collaborator `wangxiongts` [I9, 23 Jan 2026]: "Our current model does not support explicitly generating non-linguistic signals. It can only produce such sounds implicitly through expressions like "hahaha" or "emmm", relying on the model to naturally generate these vocalizations based on context. However, this approach involves a certain degree of randomness."
- Laughter is triggered by instruct + text semantics, not markup. Collaborator on unwanted laughter [I16]: "Due to the high expressiveness of our model and your instruct "very happy," the model simulates natural human speech behavior by incorporating laughter. If you prefer the model not to generate laughter, you can try refining the instruction to something like "very happy but without laughing." Thanks to the model's strong generalization capability, it may be able to follow such nuanced and complex instruct."
- The official "Human-likeness" sample writes laughter into the *text* ("heh", "huh… ha") and describes it in the *instruct* ("breaking into genuine, easygoing laughter at moments of embarrassment") [BLOG1].
- ~~Paper's only relevant claim is about the tokenizer:~~ [corrected: the paper never uses the word "paralinguistic"; this sentence is from the blog/README key-features list, not the technical report] "It fully preserves paralinguistic information and acoustic environmental features" [BLOG1 key features, verified]; the tokenizer demo has a "Paralanguage Reconstruction" row [BLOG1, verified].
- README: "the models feature strong contextual understanding, enabling adaptive control of tone, speaking rate, and emotional expression based on instructions and text semantics" [GH].
- **Implication for the cast files' `[laugh]` `[sigh]` tags:** nothing official recognises bracket tags. They would be read as text or (more likely) as noise. The sanctioned route is prose in the instruct + written vocalisation in the line ("Hah." / "Hm.").

---

## 6. Seed / voice-consistency mechanisms

- The package has **no seed argument** and never calls `torch.manual_seed` [SRC grep: no hits]. Any seeding is the caller's `torch.manual_seed(...)` before `generate_voice_design`.
- **No official statement** that a fixed seed reproduces a voice. In [I298] (CustomVoice, "how to get the same output") only users answered; no collaborator reply. User `BeeegZee`: "The fixed seed does not guarantee byte identical output, because it is applied only to one part of the model, but the fixed seed voice will "behave" the same" — user experience, unverified. [verified; two caveats the report omitted: the issue author was serving CustomVoice through **vLLM**, and BeeegZee closes with "This is based on my experience with proper SFT custom voice, not zero-shot voice cloning" — so it is not a VoiceDesign observation at all. BeeegZee also says vLLM-Omni "exposes that parameter" (a seed); that is a third-party serving path, not the `qwen_tts` package.]
- **Official consistency path #1 — design then clone** [GH "Voice Design then Clone"]: "If you want a designed voice that you can reuse like a cloned speaker, a practical workflow is: (1) use the **VoiceDesign** model to synthesize a short reference clip that matches your target persona, (2) feed that clip into `create_voice_clone_prompt` to build a reusable prompt, and then (3) call `generate_voice_clone` with `voice_clone_prompt` to generate new content without re-extracting features every time. This is especially useful when you want a consistent character voice across many lines." Collaborator [I16]: "We also strongly recommend trying the base model for voice cloning—clone audio with the desired style (can be synthesized by other systems) and then generate continuously."
- **Official consistency path #2 — hosted voice ID** [DS-EN/ZH, BLOG0/1 "Timbre Reuse"]: the DashScope API returns a persistent `voice` id: "Users can also persistently store and repeatedly call the timbres created by Qwen3-TTS, generating vivid and natural multi-turn, multi-character long-form dialogues." The multi-character examples ("旁白"/"小林"/"御姐", "Lucas"/"Mia") are produced this way. This is API-only; the open weights have no equivalent.
- **Official consistency path #3 — fine-tune** [FT]: single-speaker SFT of the Base model from a JSONL of `{audio, text, ref_audio}`; "Strongly recommended: use the same `ref_audio` for all samples. Keeping `ref_audio` identical across the dataset usually improves speaker consistency and stability during generation." No instruct/description field in the fine-tune format — you cannot fine-tune VoiceDesign captions with the shipped scripts.
- [D220] (users only, no maintainer reply) confirms the field experience: "Cloned version loses emotional range and naturalness"; drift "between chunks" persists "even though the same voice, instructions, and seed are being used".
- ~~The README's own reuse examples (§4.5 "Lucas"/"Mia") pass the **same short comma-list instruct byte-identical on every line**; that is the closest thing to an official practice for pure-VoiceDesign consistency, and the README still wraps it in clone-from-reference.~~ [unsupported — removed. The README calls `generate_voice_design` exactly **once** (the Lucas reference line) and every subsequent line goes through `generate_voice_clone`; the Lucas/Mia dialogue on BLOG1 sits under "Timbre Reuse", which the blog says is produced by persistently stored voices on the hosted API. No official example generates multiple lines by repeating an instruct through pure VoiceDesign. There is therefore **no** official practice for pure-VoiceDesign consistency, not even an implicit one.]

---

## 7. Language handling for English

- Supported list (config `codec_language_id` + `"auto"`): `auto, chinese, english, german, italian, portuguese, spanish, japanese, korean, french, russian`. Validation is case-insensitive (`str(lang).lower()`); `"English"`, `"english"`, `"Auto"` all pass [SRC].
- `language=None` → `"Auto"` for every item [SRC line 695]. README: "Pass `Auto` (or omit) for auto language adaptive; if the target language is known, set it explicitly." [GH]
- Effect of the choice is only the codec prefix (§4.3). No official guidance on which gives better voice-design adherence; the team benchmarked InstructTTSEval with `"auto"`.
- Dialects: no dialect ids in the VoiceDesign config (`spk_is_dialect: {}`); dialect voice profiles are a CustomVoice feature (Dylan = Beijing, Eric = Sichuan). Accent is controlled only through the instruct text (`accent:` field).
- No text normaliser in the processor; the text is BPE-tokenised as-is (`processing_qwen3_tts.py` has no length/normalisation logic). README robustness claim: handles ~~"pin1 yin1，特殊符号等(◍•͈⌔•͈◍)" and~~ "x = [-b ± √(b²-4ac)] / 2a" [GH] [corrected: the "pin1 yin1" sentence is a BLOG1 "Text Robustness" sample (Base voice-clone row), not in the README; the README's code only carries the equation line, and both are Base/CustomVoice demonstrations, not VoiceDesign].

---

## 8. Max text length per call

- **No character/token limit is enforced on `text` or `instruct`** anywhere in the package [SRC; processor grep empty].
- Practical ceilings: `max_new_tokens=8192` codec frames at 12.5 Hz ≈ **655 s** of audio per call (the README evaluation used 2048 ≈ 164 s); talker `max_position_embeddings: 32768`, `position_id_per_seconds: 13` [CFG]. Paper: "Long-Context Stage (S3): … we increase the maximum token length from 8,192 to 32,768"; "capable of synthesizing over 10 minutes of natural and fluent speech" [PAPER].
- DashScope limits (hosted only): description "up to 2,048 characters for Qwen-TTS" [DS-EN].
- A user-measured caveat (not official): long single calls drift in rate in the streaming layout [PR362]; VoiceDesign's default `non_streaming_mode=True` is the layout that showed 0 % drift in that measurement.

---

## 9. InstructTTSEval — what the benchmark rewards [PAPER §4, GH]

- Three metrics, from the InstructTTSEval paper (Huang et al., 2025, https://arxiv.org/abs/2506.16381): ~~the benchmark "includes three tasks, namely~~ [corrected: the abstract reads "We introduce three tasks, namely] Acoustic-Parameter Specification, Descriptive-Style Directive, and Role-Play, including English and Chinese subsets, each with 1k test cases (6k in total) paired with reference audio." Qwen's tables label them APS / DSD / RP — "Attribute Perception and Synthesis accuracy (APS), Description–Speech Consistency (DSD), and Response Precision (RP)" [PAPER Table 8 caption, verified — note Qwen's expansions of the acronyms do not match the InstructTTSEval task names; the letters line up, the words do not]. The three levels map onto the three instruct styles in §4: parameter list → descriptive prose → persona/role. [This mapping is the surveyor's inference; neither paper states it.]
- VoiceDesign scores (Table 8, EN): APS 82.9, DSD 82.4, RP 68.4; (ZH): 85.2 / 81.1 / 65.1. "Qwen3-TTS-12Hz-1.7B-VD establishes a new state-of-the-art among open-source models." Role-play (RP) is the weakest of the three for every system. [verified against the README table: holds for every row that has all three EN or ZH numbers (Gemini-flash/pro, both CustomVoice rows, GPT-4o-mini-tts, Mimo-Audio, Hume, VoxInstruct, Parler); VoiceDesign's EN APS 82.9 is not bold — Gemini-flash 92.3 and Gemini-pro 87.6 beat it.]
- Paper: "By adopting the ChatML format, Qwen3-TTS treats voice control as a language modeling task, allowing for nuanced manipulation of speech attributes."

---

## 10. Model facts worth having to hand [CFG, MC, GH]

- `tts_model_type: "voice_design"`, `tts_model_size: "1b7"`, `tokenizer_type: "qwen3_tts_tokenizer_12hz"`, `transformers_version: "4.57.3"`, weights 3.83 GB bf16.
- Talker: 28 layers, hidden 2048, 16 heads / 8 KV heads, vocab 3072 (2048 codec + control), MRoPE `mrope_section [24,20,20]` interleaved, `rope_theta 1e6`. Code predictor: 5 layers, hidden 1024, vocab 2048, `num_code_groups 16`.
- Special ids: `tts_bos 151672, tts_eos 151673, tts_pad 151671, codec_bos 2149, codec_eos 2150, codec_pad 2148`.
- Repo has **no** `chat_template`, `tokenizer.json`, `special_tokens_map.json`, `processor_config.json` (all in `.no_exist`); only `config.json, generation_config.json, merges.txt, vocab.json, tokenizer_config.json, preprocessor_config.json, speech_tokenizer/`.
- Package `qwen-tts 0.1.1` (PyPI), depends on `accelerate, einops, gradio, librosa, onnxruntime, soundfile, sox, torchaudio, transformers`. `from_pretrained` forwards kwargs to `AutoModel.from_pretrained`; README uses `attn_implementation="flash_attention_2"` — on ROCm that is Isaac's call, the code path also supports the manual PyTorch attention ("Warning: flash-attn is not installed. Will only run the manual PyTorch version" [I16 log]).
- Web demo: `qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign --ip 0.0.0.0 --port 8000`; the demo makes the instruct **required** for VoiceDesign ("Voice design instruction is required (必须填写音色描述).") [SRC demo.py line 369].

---

## 11. Things the official material does NOT say (so nobody should claim them)

- No pitch-in-Hz vocabulary, no "bass"/"sub-bass" example, no age above "senior (55+)" / "中老年" / "年近七十" in any official instruct.
- No statement on how many training hours carried captions, who/what wrote them, or whether they were LLM-generated (the 12-field template strongly suggests an audio-captioner, but that is inference).
- No seed, no `voice_id`, no speaker-embedding export from VoiceDesign in the open package.
- No documented bracket/angle tags for laughter, sighs, breaths, pauses; no SSML.
- No recommendation about `temperature`/`subtalker_temperature` values other than the shipped defaults; no statement that lowering them stabilises timbre.
- No official guidance on `language="English"` vs `"Auto"` for voice design beyond "if the target language is known, set it explicitly" [GH]; the team's own benchmark used `"auto"`.
- No official reply on drift across chunks [D220, I239, PR362 all unanswered by maintainers as of 12 Sep 2026].

---

## Verification

Skeptic pass, 12 Sep 2026. Every cited source was re-opened: the cached `generation_config.json` / `config.json`, the installed `qwen_tts` 0.1.1 source (PyPI confirms 0.1.1 of 6 Feb 2026 is still the latest; HF snapshot `5ecdb673…` of 29 Jan 2026 is still the head of the VoiceDesign repo — nothing here is stale), the raw GitHub README (last README commit 25 Jan 2026; last repo commit 17 Mar 2026 "fix finetuning bug"), the arXiv HTML, both qwen.ai blog posts rendered in a browser, the DashScope EN doc, the HF Space `app.py`, issues #9 / #16 / #239 / #298, PR #362 and discussion #220 via the GitHub API with author associations.

### Held (all quotes found verbatim, claims mean what the report says)

1. Generation defaults — JSON matches byte for byte; wrapper hard-default `max_new_tokens=2048`, JSON wins; team evals used `max_new_tokens=2048` + `language="auto"` (README §Evaluation, verbatim).
2. Two sampler groups — code at modeling 1668-1677 passes `subtalker_*` into `code_predictor.generate(max_new_tokens=num_code_groups-1)`; paper §3.1 quote verbatim; the package's own module layout (`core/tokenizer_12hz/…tokenizer_v2.py`) settles that "tokenizer-v2" = 12Hz.
3. `non_streaming_mode` docstring verbatim; VoiceDesign default `True`; PR #362 numbers verbatim (with the Base-clone caveat added above).
4. Paper says almost nothing about instruction data — confirmed; §3.3 quote verbatim; `think`/`nothink` prefix code verbatim at modeling 2110-2147; config ids match.
5. ChatML prompt format — `_build_instruct_text` / `_build_assistant_text` verbatim at inference 269-276; "Empty string is allowed" verbatim at line 654.
6. 12-field caption schema — all four English instances and the Chinese one re-read on BLOG1 and match verbatim; the `role:` variant is on BLOG0 (hosted model — see correction).
7. Instruct string inventory — every string found verbatim; four of them (Homebody Sis, 邪恶女魔头, booming baritone, strained tenor) and the `role:` caption are hosted VD-Flash samples, now labelled as such.
8. DashScope five principles, dimension table, 2,048-char limit, Chinese/English-only — verbatim; page updated 11 Sep 2026 and covers hosted `qwen3-tts-vd-2026-01-26`.
9. Randomness acknowledged; no seed in package (grep: zero `manual_seed`/`set_seed` hits); #298 user-only — verbatim.
10. Design-then-Clone is the only sanctioned open-weights consistency path — README verbatim; collaborator `wangxiongts` (COLLABORATOR) in #16 verbatim.
11. Hosted Timbre Reuse quote verbatim on BLOG1; finetuning README verbatim (`{audio,text,ref_audio}`, single-speaker Base only, no instruct field).
12. No paralinguistic tag vocabulary — #9 collaborator reply verbatim (23 Jan 2026); #16 "very happy but without laughing" verbatim; BLOG1 Human-likeness text has "heh" and "huh… ha" in the line.
13. Language handling — config ids, `.lower()` validation, `None → "Auto"` at line 695, `spk_is_dialect: {}` all confirmed.
14. No length limit; 8192 frames / 12.5 Hz ≈ 655 s; `max_position_embeddings 32768`; paper "over 10 minutes" verbatim.
15. Table 8 numbers verbatim; RP weakest for every fully-populated row.
16. Official vocabulary tops out at "Low male pitch" / "senior (55+)" / "中老年" — confirmed after reading every instruct on both blogs and the DashScope table; the only "baritone" is BLOG0's hosted sample, and no official instruct says "bass".

### Corrected

- §1: "CustomVoice/Base+instruct" — Base has no instruct path. Removed.
- §4.1: "accent" does appear once in the paper (cross-lingual "accent drift"), not in a voice-design sense.
- §4.4 / §4.5 / §4.6: BLOG0 is the hosted VD-Flash launch post (Dec 2025); its samples are now marked as hosted-model evidence. Same for the DashScope doc. The report treated them as interchangeable with the open checkpoint; they are the same family but not the same artefact.
- §4.7: four CustomVoice instruct strings were attributed to the README; they are BLOG1-only.
- §5: the "fully preserves paralinguistic information" sentence was attributed to the paper; it is blog/README copy. The paper never says "paralinguistic".
- §6: "same instruct byte-identical on every line is the closest thing to an official practice" — unsupported and removed. The README runs VoiceDesign once, then clones; the blog's multi-line dialogues are hosted stored-voice output.
- §7: "pin1 yin1" is a BLOG1 Base-clone sample, not README text.
- §9: InstructTTSEval abstract misquoted ("includes" → "We introduce"); the level↔instruct-style mapping flagged as inference.
- §3 / §6: PR #362's drift figures are 1.7B-Base voice-clone with a 12.9 s reference; #298's seed anecdote is SFT-CustomVoice-through-vLLM. Neither is a VoiceDesign measurement; both now say so.

### Nothing from memory found

Every claim traced to an opened source. No claims about other models were mislabelled as Qwen3-TTS, but several about the *hosted* Qwen3-TTS-VD-Flash were presented as if about the open checkpoint (now fixed).

### Missing — things the angle asked for that the report does not cover

- **docs/cookbook**: the report cites none because none exist — the repo tree has only `README.md`, `examples/` (4 scripts), `finetuning/` and `qwen_tts/`. The report should have said so outright. (Stated here.)
- **The model card is VoiceDesign-blind**: the 3,214-byte HF README's only code is a `generate_custom_voice` call with `instruct="用特别愤怒的语气说"` — there is no VoiceDesign example on the VoiceDesign model card. Worth saying explicitly for anyone who goes there first.
- **What the official HF Space actually passes**: `non_streaming_mode=True, max_new_tokens=2048`, language default `"Auto"`, description mandatory. The report cites `app.py` for the language default only.
- **The README's own VoiceDesign call passes `language="English"` explicitly** (design-then-clone snippet) while the benchmark used `"auto"` — the two official usages disagree, and the report's §7 only mentions the benchmark side.
- **vLLM-Omni serving path**: a user in #298 says it exposes a seed parameter. Not Qwen-official and unverified here, but it is the only concrete seed-exposing route anyone has named, and the report's "no seed anywhere" framing should carry that footnote.
- **Speaker-embedding / `x_vector_only_mode`**: `create_voice_clone_prompt` has an `x_vector_only_mode` flag (SRC line ~360). Whether a VoiceDesign clip's x-vector alone (no ref text) gives a steadier timbre than full ICL cloning is an official-API question the report does not touch — relevant if Isaac ever relaxes the no-clone rule.
- **DashScope ZH doc** is listed as a source but never independently quoted; every DS quote is from the EN page.
