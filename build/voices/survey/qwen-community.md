# Qwen3-TTS VoiceDesign — community experience survey (Jan–Sep 2026)

Compiled 12 Sep 2026 for the WOTR narration pipeline (pure voice-design mode: `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`, no Base clone, no RVC).

Sources read directly: the QwenLM/Qwen3-TTS issue tracker and Discussions tab (via `gh`), the `qwen_tts` inference source, the checkpoint's `generation_config.json`, the Hugging Face model card and its discussion threads, the official HF "Qwen3-TTS-Voice-Design" Space source, the Alibaba Cloud Model Studio voice-design page, the arXiv tech report, and the source/docs of the main community tools (TTS-Audio-Suite, DarioFT/ComfyUI-Qwen3-TTS, alexandria-audiobook, Castwright, Voice-Clone-Studio, TTS-Story, faster-qwen3-tts, mlx-audio, Rapid-MLX, tts-audiobook-tool) plus the blog guides (ocdevel, getstream, voicecreator.pro, dev.to x2, betterstack, deapi, Habr).

**Gap:** Reddit (r/LocalLLaMA etc.) is blocked from this environment's search, fetch and browser tools — no Reddit threads could be read. YouTube transcripts were not retrievable either. Everything below is from GitHub, Hugging Face, the official docs, and blogs.

---

## 0. Headline findings

1. **Voice drift per run is structural, not a settings problem.** In VoiceDesign mode there is *no speaker embedding at all* — the code path is literally commented `# Instruct create speaker` and sets `speaker_embed = None`; the timbre is sampled token-by-token from the instruct text alone ([modeling_qwen3_tts.py L2088](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/core/models/modeling_qwen3_tts.py)) [verified: line 2088 of the current `main`, last pushed 17 Mar 2026; the pypi `qwen-tts` 0.1.1 of 6 Feb 2026 is the latest release, so this is not stale]. Qwen staff confirm: "voice design需要多Sample几次选择自己想要的音色" (voice design requires sampling several times and picking the timbre you want) — [issue #4](https://github.com/QwenLM/Qwen3-TTS/issues/4) [verified: wangxiongts, "Speech/LLM Algorithm Engineer@Alibaba Qwen Team", COLLABORATOR on the repo]. [corrected: the follow-up in #4 that a designed timbre "seemingly cannot be saved" ("好像不能保存音色") is from an ordinary user, not staff; staff only said to sample repeatedly and pointed at the design-then-clone README recipe.] A community user (not a maintainer — author_association NONE) [corrected: was "community maintainer"]: "the voices are different and randomized each time. I haven't find a way to save a specific voice yet except using the output as the prompt for base model" — [issue #13](https://github.com/QwenLM/Qwen3-TTS/issues/13) [verified].
2. **The only consistency mechanism the community has found is "design then clone"** (pick a good take, use it as a Base-model reference). Every serious tool (TTS-Audio-Suite, alexandria, Castwright, DarioFT node, SwiftVoxAlta, Rapid-MLX request) does this. Isaac has ruled it out; the report still documents it because *nothing else* in the corpus solves identity lock. Within pure design mode the tools that stay there (alexandria "Voice Design Mode") explicitly label it "ideal for minor characters".
3. **Fixed seed + identical text + identical instruct is reproducible** (same bytes) on the HF/PyTorch path; a fixed seed with *different* text does **not** hold the timbre: "As soon as you change the input text—even by a single character—the seed's constraint collapses" — [dev.to, 27 Apr 2026](https://dev.to/lcmd007/from-stochastic-drifting-to-vector-anchors-how-i-solved-voice-consistency-in-qwen-tts-4dff) [verified quote; caveat: the article never names which Qwen3-TTS checkpoint it used, is a 72-hour blog test with no numbers, and its "fix" is a Base-model `.pt` clone. The claim is consistent with the no-speaker-embedding code path above, but it is not a VoiceDesign-specific measurement].
4. **Per-line delivery inside one instruct string is what everyone does**, by concatenating `"{identity description}, {line direction}"` (alexandria) — but there is no evidence anyone achieved a *stable* identity across lines this way. The Qwen team's own answer for identity + per-line instruct is the unreleased 25Hz "VoiceEditing" model, still not released as of 12 Sep 2026 [corrected: was "13 Sep"] (the HF `Qwen` org lists only the five 12Hz model checkpoints — 1.7B Base/CustomVoice/VoiceDesign, 0.6B Base/CustomVoice — plus the 12Hz tokenizer [corrected: was "six 12Hz checkpoints"; six repos, five of them models]; [issue #294](https://github.com/QwenLM/Qwen3-TTS/issues/294) still open [verified]; the staff statement that the 25Hz voice-editing model "will support both cloning and instruct" is [issue #25](https://github.com/QwenLM/Qwen3-TTS/issues/25), wangxiongts, 26 Jan 2026 [verified]).
5. **Age must be written as acoustics, not adjectives.** The most concrete community finding on prompt wording: "Gemini satisfied the rule with psychology ('weary'/'weathered' — which VoiceDesign ignores) plus 'deep-pitched'", which "Qwen3-TTS VoiceDesign reads as a prime-age baritone"; the fix that "audibly fixed it" was to name the age and add "dry rasp, faint tremor, low-to-medium not deep" — [Castwright #830](https://github.com/dudarenok-maker/Castwright/issues/830) [verified: issue of 16 Jun 2026 and docs/features/160 both carry this text. Caveat: this is one developer's listening judgement on one character, with the open 1.7B VoiceDesign checkpoint; no A/B or numbers].
6. **Non-verbal cues (laugh, sigh) are not tags.** Qwen staff: "Our current model does not support explicitly generating non-linguistic signals. It can only produce such sounds implicitly through expressions like 'hahaha' or 'emmm' … this approach involves a certain degree of randomness" — [issue #9](https://github.com/QwenLM/Qwen3-TTS/issues/9) [verified: wangxiongts, 23 Jan 2026]. Bracket tags such as `[laugh]` from other engines have no documented support here [corrected: was "The README's `[laugh]`-style bracket tags" — the Qwen README never mentions such tags; the asker in #9 proposed `<laugh>`/`[laugh]` and staff said neither is supported].
7. **Accent control by description is unreliable**, including for supported languages: "with Voice Design, I often get a noticeable English accent on some words … the result seems very sensitive to the exact wording of the voice description" — [Discussion #315](https://github.com/QwenLM/Qwen3-TTS/discussions/315) (Spanish, 12 May 2026, zero replies) [verified]. For English, ocdevel reports the model "defaults to standard American or Chinese-accented English" [verified quote; ocdevel's own summary, not a test]. Setting `language="English"` explicitly (not `Auto`) is the one documented lever, and it changes the codec prefill (see §2) [verified in code].

---

## 1. Official guidance on writing the description

### 1a. Alibaba Cloud Model Studio voice-design page (same model family, `qwen3-tts-vd-*`)
[alibabacloud.com/help/en/model-studio/qwen-tts-voice-design](https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-design)

[verified 12 Sep 2026: principles, dimension table, four example descriptions, 2,048-char limit, "Chinese and English only", "1,000 custom voices", and the absence of any accent dimension or per-request style field all appear on the page. Caveat: this page documents the cloud `qwen3-tts-vd-*` product, not the open 1.7B checkpoint; same family, but nothing on the page is a test of the open weights.]

Five principles, verbatim: "Be specific, not vague", "Be multi-dimensional, not one-dimensional", "Be objective, not subjective", "Be original, not imitative", "Be concise, not redundant".

Dimension table:

| Dimension | Example words |
|---|---|
| Gender | Male, female, neutral |
| Age | Child (5-12), teenager (13-18), young adult (19-35), middle-aged (36-55), senior (55+) |
| Pitch | High, medium, low, slightly high, slightly low |
| Speed | Fast, medium, slow, slightly fast, slightly slow |
| Emotion | Cheerful, calm, gentle, serious, lively, composed, soothing |
| Characteristics | Resonant, crisp, husky, mellow, sweet, deep, powerful |
| Use case | News broadcast, advertising, audiobook, animation character, voice assistant, documentary narration |

Example descriptions (verbatim):
- "A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation, is suitable for news broadcasting or documentary commentary."
- "Calm, slow-paced middle-aged male voice, deep and resonant, suited for news reading or documentary narration"
- "Cute child's voice, approximately an 8-year-old girl, slightly childish speech, suited for animation character voiceover"
- "Gentle and thoughtful female, around 30 years old, even-toned, suited for audio book reading"

Limits: `voice_prompt` up to 2,048 characters; "Chinese and English only". Note the cloud API is a *two-step* product: a creation call returns a `voice` id that is then reused ("up to 1,000 custom voices" per account) — i.e. Alibaba solved identity lock server-side by persisting the voice; the open checkpoint has no equivalent. No per-request `instructions` field exists on the cloud designed voice either — "styling occurs at description time".

**Note:** accent is absent from the official dimension table (ocdevel: "Accent is conspicuously absent from the official dimensions table").

### 1b. Official HF Space `Qwen/Qwen3-TTS-Voice-Design` — the eight curated example instructs
[huggingface.co/spaces/Qwen/Qwen3-TTS-Voice-Design/blob/main/app.py](https://huggingface.co/spaces/Qwen/Qwen3-TTS-Voice-Design/blob/main/app.py). Placeholder text: "Describe the voice: gender, age, speed, tone, emotion, scenario...". [verified: all eight strings and the placeholder are in `app.py` lines 61–118.] [corrected: this Space does **not** run the open 1.7B VoiceDesign checkpoint. `app.py` posts to `https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization` with `"model": "qwen-voice-design"` and `"target_model": "qwen3-tts-vd-realtime-2025-12-16"` — i.e. it is a front end for the cloud product in §1a. The examples are still Qwen-curated for this model family, but they are not evidence of what the local checkpoint does with them.] These are the closest thing to a Qwen-endorsed prompt style; note that several mix identity with a *delivery arc* in one string:

- "A clear and natural female voice, moderate speed, stable tone, suitable for news broadcasting or daily conversation."
- "Standard pronunciation with a dramatic, sobbing quality. The voice is slightly raspy and tense, conveying deep sorrow and desperate pleading."
- "A loud, powerful male voice exhibiting resilience and authority. The pace is brisk and fluent, slowing down slightly at the end for emphasis and decisiveness."
- "Professional broadcasting style. The pace starts slow and accelerates, with a bright, solid timbre. The tone should be inspiring, passionate, and persuasive."
- "A calm and confident tone. The speed is steady, with very clear articulation. The voice should feel firm and certain, with a slight downward inflection at the end."
- "A young female voice, brave and determined, filled with idealism and warmth. High-mid pitch range, distinct cadence, and transitioning from steady to passionate."
- "Cheerful and extroverted personality. Fast but fluent pace, with the pitch rising at key moments to emphasize excitement and curiosity about the food."
- "A bright, high-pitched young girl's voice. Lively and animated tone that engages the listener, with a loud and clear volume reflecting an active personality."

### 1c. README / examples
- README voice-design example (Chinese): `instruct="体现撒娇稚嫩的萝莉女声，音调偏高且起伏明显，营造出黏人、做作又刻意卖萌的听觉效果。"`; English: `"Speak in an incredulous tone, but with a hint of panic beginning to creep into your voice."` ([README](https://github.com/QwenLM/Qwen3-TTS#voice-design)).
- The "Voice Design then Clone" section's reference instruct: `"Male, 17 years old, tenor range, gaining confidence - deeper breath support now, though vowels still tighten when nervous"` — a terse, attribute-list style ([README](https://github.com/QwenLM/Qwen3-TTS#voice-design-then-clone)).
- README: "This is especially useful when you want a consistent character voice across many lines." — i.e. the authors' own answer to consistency is clone. [verified: all three README quotes in this subsection are present in the current README (lines 221–234, 290, 306).]
- The tech report says only: "we introduce a probabilistically activated thinking pattern during training to improve instruction following, especially for complex descriptions" ([arXiv 2601.15621 §3.3](https://arxiv.org/html/2601.15621)). It gives **no** attribute vocabulary, no caption-construction details, and does not discuss timbre consistency for voice design.

---

## 2. What the code actually does with `instruct` (why runs differ)

From [qwen3_tts_model.py](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/inference/qwen3_tts_model.py) and [modeling_qwen3_tts.py](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/core/models/modeling_qwen3_tts.py):

- The instruct is wrapped as a chat "user" turn and the text as an "assistant" turn:
  `_build_instruct_text` → `f"<|im_start|>user\n{instruct}<|im_end|>\n"`;
  `_build_assistant_text` → `f"<|im_start|>assistant\n{text}<|im_end|>\n<|im_start|>assistant\n"`.
  The instruct embedding is prepended to the talker input (`talker_input_embeds[index].append(text_projection(text_embeddings(instruct_id)))`). Empty instruct is allowed ("treated as no instruction").
- In VoiceDesign there is no speaker vector: `if speaker == "" or speaker == None: # Instruct create speaker` → `speaker_embed = None` [verified, modeling_qwen3_tts.py L2088–2089]. Identity therefore emerges from sampling the first codec frames [researcher's inference from the code, not a sourced statement]; the onset-instability observation in [issue #343](https://github.com/QwenLM/Qwen3-TTS/issues/343) — "the instability is concentrated at generation onset … The generation often 'settles' into the correct voice partway through" [verified quote, 10 Jul 2026, still open, no staff reply] — is *suggestive* only. [corrected: #343 is a LoRA fine-tune of the **Base** model with a baked speaker embedding served on vLLM-Omni under greedy decoding. That is the opposite regime from VoiceDesign (which has no speaker embedding), so "the mechanism is the same head" is the researcher's assumption; nobody in the corpus reports onset instability for VoiceDesign itself.]
- **`language` is not cosmetic.** With `language="Auto"` the codec prefill is `[codec_nothink_id, think_bos, think_eos]`; with an explicit language it is `[codec_think_id, think_bos, <language_id>, think_eos]` [verified, modeling_qwen3_tts.py L2110–2147]. So `language="English"` inserts a language token into the "think" block. README: "Pass `Auto` (or omit) for auto language adaptive; if the target language is known, set it explicitly." [verified; corrected: that comment sits on the **CustomVoice** example (README line 167), not in the voice-design section — but the `language` argument goes through the same prefill code for all three models, and every README voice-design example passes an explicit language.] TTS-Audio-Suite README: "Qwen3-TTS: Use explicit language parameters - language tags directly control output" [verified].
- **Sampling defaults** ([generation_config.json](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/blob/main/generation_config.json)): `do_sample: true, repetition_penalty: 1.05, temperature: 0.9, top_p: 1.0, top_k: 50, subtalker_dosample: true, subtalker_temperature: 0.9, subtalker_top_p: 1.0, subtalker_top_k: 50, max_new_tokens: 8192` [verified byte-for-byte; checkpoint last modified 29 Jan 2026, so current]. Two samplers: the main talker (first codebook / semantic) and the "sub-talker" (acoustic codebooks). All of `temperature, top_k, top_p, repetition_penalty, subtalker_*, max_new_tokens` are accepted as kwargs on `generate_voice_design` [verified: `**kwargs` and the docstring in qwen3_tts_model.py L637–660].
- **There is no seed parameter in the library.** [verified: no `seed` anywhere in `qwen3_tts_model.py` or `modeling_qwen3_tts.py`.] Every tool that offers a seed just calls `torch.manual_seed(seed)` (and `torch.cuda.manual_seed_all`) before `generate_voice_design` — see [alexandria tts.py L767](https://github.com/Finrandojin/alexandria-audiobook/blob/main/app/tts.py) [verified], [TTS-Story worker](https://github.com/Xerophayze/TTS-Story/blob/main/engines/qwen3_voice_design_worker.py) [not re-checked], [TTS-Audio-Suite adapter](https://github.com/diodiogod/TTS-Audio-Suite/blob/main/engines/adapters/qwen3_tts_adapter.py) (`torch.manual_seed(seed)` L297, `cuda.manual_seed_all` L299) [verified].
- No Qwen source, issue or tool documents any effect of lowering `temperature`/`top_k` on *timbre* stability in VoiceDesign. (One CustomVoice user reports "调整了temperature无效" — adjusting temperature had no effect on run-to-run timbre/emotion differences — [issue #298](https://github.com/QwenLM/Qwen3-TTS/issues/298) [verified; CustomVoice on vLLM, not VoiceDesign].)

---

## 3. Controllable vs not-controllable attributes (community consensus)

**Reported as reliably controllable**
- Gender, broad age band, pitch band (high/medium/low), pace, emotional baseline, broad texture words (deep, resonant, husky, raspy, bright, crisp, warm) — the official table plus every guide. ocdevel: use "deep," "crisp," "fast-paced" — "not 'nice'".
- Emotion/prosody instructions on the instruct-capable models: a user test of 12 instructions found "Happy, Sad, Embarrassed, News/Broadcast, Angry, Disgusted, Fearful, Surprised, Whispering" all followed; only dialect switching failed — [issue #248](https://github.com/QwenLM/Qwen3-TTS/issues/248) (CustomVoice preset `vivian`, same instruct mechanism) [verified]. The issue's own author summarised, five minutes after filing [corrected: was "A maintainer summarised" — zhuxiaoxuhit has no association with the repo and nobody from Qwen replied]: "I realized the current instruction tuning focuses on **prosody and emotion**, not **dialect switching**."
- Suppressing unwanted paralinguistics by negation: Qwen staff suggest "very happy but without laughing" — [issue #16](https://github.com/QwenLM/Qwen3-TTS/issues/16) ("Thanks to the model's strong generalization capability, it may be able to follow such nuanced and complex instruct") [verified: wangxiongts, 23 Jan 2026. Caveat: the thread is CustomVoice with preset `Ryan`; staff phrased it as "may be able to"; the reporter never confirmed it worked, and his later attempt at "no laughter or other inflections" still produced a stray "OK". Untested on VoiceDesign.]
- Use-case / archetype anchoring ("BBC documentary narrator", "late-night radio DJ" — deapi guide; "suitable for audiobook narration" — official examples). Castwright adopted a mandatory trailing purpose clause after auditing its prompts against the official format ([Castwright doc 160](https://github.com/dudarenok-maker/Castwright/blob/main/docs/features/160-voicedesign-persona-format.md)).

**Reported as unreliable or ignored**
- **Accent / dialect** (see §5).
- **Numeric duration / rate**: "instructions like 'finish within five seconds' have 'no effect whatsoever'; only vague descriptors like 'fast speaking rate' work" ([ocdevel](https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning)) [verified as present in ocdevel; **but** "no effect whatsoever" is in quotation marks there and ocdevel does not say who said it. It is not on the Alibaba English page and not in any QwenLM/Qwen3-TTS issue (searched). Treat as second-hand and unattributed.]
- **Psychological adjectives without acoustics**: "weary"/"weathered" — "which VoiceDesign ignores" ([Castwright #830](https://github.com/dudarenok-maker/Castwright/issues/830)) [verified; single-developer listening judgement].
- **Conflicting attributes**: "high-pitched deep bass" → "may output unpredictable results by favoring one attribute over the other" ([getstream](https://getstream.io/blog/qwen3-voice-design/), 17 Apr 2026, 1.7B VoiceDesign run locally) [verified quote; stated as general advice, not a reported test].
- **Stacked intensifiers**: "'very, very deep' adds nothing over 'deep'" (ocdevel) [verified quote; ocdevel's own assertion, no test shown].
- **Explicit non-verbal tokens** `[laugh]`, `(sigh)`: unsupported ([issue #9](https://github.com/QwenLM/Qwen3-TTS/issues/9); HF discussion "Are there any in-prompt instructions we can define?" got no answer). Third-party site qwen3tts.net advertises tags like `[serious] [whispers] [laughing] [gasp]` — no primary source supports this; treat as invented.
- **Reading style suppression**: a user asking for flat newscast delivery: "I told it to read the text aloud in the tone of a newscast, no laughter or other inflections, but it doesn't seem to work, it still says 'OK' before reading the text aloud" ([issue #16](https://github.com/QwenLM/Qwen3-TTS/issues/16)); staff: "The speaker 'Ryan' is inherently expressive, non-broadcast in style" and recommend cloning a flat reference instead.
- **Speaking rate on cloned voices** is a known open problem (accelerates over long text — [issue #290](https://github.com/QwenLM/Qwen3-TTS/issues/290), [issue #239](https://github.com/QwenLM/Qwen3-TTS/issues/239), [mlx-audio #910](https://github.com/Blaizzy/mlx-audio/issues/910) with a suspected repetition-penalty mechanism). Not reported for VoiceDesign specifically.

---

## 4. Phrasings people used for deep / gravelly / aged / child voices

Verbatim community and official strings, grouped. None come with a measured pitch (Hz) outcome; nobody in the corpus reports F0 numbers.

**Very deep / bass**
- Official: "A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation" (Alibaba doc).
- getstream (Zeus): "A powerful male god with an immensely deep, booming, resonant bass voice that reverberates..." — with the layered template rows: Pitch `"A deep, booming, resonant bass voice"`, Distinguishing details `"As if echoing through a vast marble temple"`.
- DarioFT node doc: `"A deep, resonant male voice, narrator style, calm and professional."`
- TTS-Audio-Suite README: `"A deep, authoritative male voice with clear articulation"`.
- dev.to (cz): `"Deep male voice with slight rasp"`.
- SwiftVoxAlta: `"Deep, resonant male baritone..."`.
- deapi narrator: `"British male, 70s, warm and authoritative, low-medium pitch, measured pace, rich timbre, documentary-style gravitas, slight RP accent."`

**Rasp / grit / hoarse**
- Official HF Space: "The voice is slightly raspy and tense, conveying deep sorrow and desperate pleading."
- Official table word: "husky"; ocdevel's table also lists "hoarse".
- getstream Texture row: `"Thin, raspy, and cracked with age"`.
- alexandria: `"A warm elderly woman with a gentle raspy voice"`, `"A warm elderly woman with a gentle, raspy voice and a slight Southern drawl"`.
- deapi witch: `"Elderly woman, 80s, raspy and mischievous, medium-low pitch, slow deliberate pace, slight Eastern European accent, gravelly timbre, fairy tale witch energy."`

**Age (the one attribute with a documented failure + fix)**
- Castwright's post-fix prompt rules ([skills/audiobook-voice-style.md](https://github.com/dudarenok-maker/Castwright/blob/main/skills/audiobook-voice-style.md)): "State the apparent age with a concrete word or band ('a child of about eight', 'a man in his seventies', 'an elderly woman') — never leave it implied." / "Elderly / old: pair the explicit age word with aging acoustics — a dry rasp or gravel, a thinner, reedier or breathier edge, and often a faint tremor or quaver — at a slower, more deliberate pace. Do NOT describe an old voice as merely 'deep'; age tends to thin and fray a voice rather than deepen it." / "Middle-aged: fuller and steadier, without the fraying of age."
- Their worked elderly example: `"An elderly man's voice in his seventies, low-to-medium pitch and gravelly, with a dry rasp and a faint tremor; slow and deliberate, carrying worn, unshakable authority, for expressive character dialogue."` [verified: both the rule text and this example are in `skills/audiobook-voice-style.md` on `main`. Note this file is a prompt Castwright feeds to an LLM to *write* instructs; the rules encode one developer's fix, not a community consensus.]
- getstream grandma: `"An elderly female grandmother, 80 years old, with a high-pitched, thin, croaky old woman's voice..."`.
- **Implication for Gimbzo/Darius:** "deep" + "old" pull in opposite directions in this model; the community fix is to state the age explicitly and carry it with rasp/dryness/tremor/pace rather than depth. For a "seventy-year-old priest in a young body" no source addresses the case; the model has only the description, so whatever acoustics are written win.

**Child**
- Official: "Cute child's voice, approximately an 8-year-old girl, slightly childish speech, suited for animation character voiceover"; "A bright, high-pitched young girl's voice. Lively and animated tone…".
- Castwright: "Child / young: brighter, higher, lighter and more energetic." Example teen: `"A bright teenage girl's voice, medium-high pitch and mid-paced, warm and lightly playful with a faintly nervous edge, suited to expressive character dialogue."`
- No source reports a *twelve*-year-old specifically; the official bands are "Child (5-12), teenager (13-18)". No source reports child-voice failure modes.

**Flat / level delivery**
- UChi accent study (CustomVoice): `"Flat, monotone delivery. No emotion."` → "Less dramatic but unnatural"; `"Speak casually and naturally, like a real person making a phone call"` → "Still too dramatic, slow" ([UChi-JCL issue #1](https://github.com/UChi-JCL/Multi-Modal-Semantic-Routing-for-vLLM/issues/1)). Their finding: "Default output is overly dramatic … sounds like TV/movie acting".

---

## 5. The accent problem and the fixes people found

- **Symptom (English):** "most of the voices have too strong a Chinese accent when speaking English" (user quoted by ocdevel); dev.to (cz): "some voices have a slight Asian accent in English"; Habr (Russian): all voices had an "азиатский акцент" and "голоса слабо адаптируются под новый язык". Voicebox #42 "American accent even with Scottish voice" (clone).
- **Symptom (supported non-English):** Spanish VoiceDesign "I often get a noticeable English accent on some words … very sensitive to the exact wording of the voice description, and getting a clean, consistent accent feels like trial and error" — [Discussion #315](https://github.com/QwenLM/Qwen3-TTS/discussions/315), unanswered. Discussion #332: Portuguese carries "a string European Portuguese accent".
- **Dialect by instruction fails**: Sichuan/Cantonese/Shanghainese requests "remain in standard Mandarin" — [issue #248](https://github.com/QwenLM/Qwen3-TTS/issues/248).
- **Fixes reported:**
  1. Set `language="English"` explicitly, never `Auto` (README; TTS-Audio-Suite; and the prefill mechanism in §2). No one quantifies the gain.
  2. Write the accent as a *named locale* in the description ("General American", "RP British" — Voice-Clone-Studio's JSON template field `accent_locale`; getstream: "Specify origin and target language for non-native accents", e.g. `"A thick French accent speaking English"`). Results called "inconsistent" by ocdevel; no controlled test found.
  3. Instruction *language* as a cue: for CustomVoice, "Chinese-language instructions work dramatically better than English ones for controlling Mandarin-accented English output. The model seems to respond to the instruction language as a contextual cue" ([UChi-JCL #1](https://github.com/UChi-JCL/Multi-Modal-Semantic-Routing-for-vLLM/issues/1)) [verified: 11 Apr 2026, CustomVoice presets `vivian`/`dylan` on vLLM-Omni; their goal was to *produce* a Chinese accent, and the winning instruct literally asked for "chinglish的口音". Their to-do list says "Test VoiceDesign mode" — never done]. The converse (English-language instruct → more native English) is an inference, not a reported result.
  4. Everything else is "clone real accented audio" (ocdevel: "Voice cloning with actual British/Australian/etc. reference audio is far more reliable than text descriptions") — out of scope for Isaac.
- **Unknown:** no source reports which English wording ("American English", "neutral English accent", "native English speaker") most reliably removes the Chinese accent in VoiceDesign.

---

## 6. Prompt length, ordering and structure

- Official limit 2,048 chars; official examples are 1–2 sentences. ocdevel: "The official example prompts run 15-40 words (1-3 sentences). This appears to be the sweet spot" [corrected: exact wording; it is ocdevel's reading of the official examples, not a test]. voicecreator.pro: "One to three sentences is the sweet spot … Longer descriptions give more control, but extremely long prompts can sometimes produce inconsistent results". getstream: "2-4 sentences (40-80 words)". qwen3tts.net (third party): "30–80 words". No controlled length experiment exists in the corpus.
- **Ordering** — every guide and tool writes identity first, delivery last: getstream layers = Identity → Pitch → Texture → Emotion → Pacing → Accent → Distinguishing details; qwen3tts.net formula "Age + gender + timbre + rate + emotion + purpose"; Castwright "Describe how the voice SOUNDS, then end with a short purpose clause"; alexandria concatenates `f"{base_desc}, {instruct}"` (identity, then the per-line direction) ([tts.py L807](https://github.com/Finrandojin/alexandria-audiobook/blob/main/app/tts.py)). The official Space examples put pace/arc after timbre. No source tests whether order matters.
- **Structured/JSON instructs**: Voice-Clone-Studio ships an LLM preset "Voice Design (Json)" that emits a JSON object (`age_range, gender_presentation, timbre, pitch, pitch_range, speaking_rate, breathiness, nasality, articulation, warmth, emotional_baseline, accent_locale, prosody_notes, phonetic_cues`) and passes that JSON string straight in as the instruct ([prompt_hub.py](https://github.com/FranckyB/Voice-Clone-Studio/blob/main/modules/core_components/prompt_hub.py)). No evidence offered that it works better than prose.
- **Long text ignored / "text splitting is reportedly ignored"**: ocdevel says only cloning handles long text via chunking. Discussion #220: "Right now we can only create a few minutes of audio at a time. Chunking isn't really an option because the voice changes when you do that."
- **Description language**: Chinese or English only (Alibaba doc; Castwright keeps "instruct stays English").

---

## 7. Keeping one voice across lines and chunks

What is actually reported, ranked by evidence:

1. **Design → clone with Base (`create_voice_clone_prompt` → `generate_voice_clone`)** — the official README recipe and the de-facto community standard: TTS-Audio-Suite's Voice Designer speaks a ~10 s reference text (tooltip: "Use roughly 10 seconds or more with varied intonation, questions, and representative sounds to evaluate and clone the designed voice reliably") [verified in `unified_voice_designer_node.py` L28 and L43; note the tooltip's inclusion of "accent" in the description list is the node author's wish-list, not evidence it works] and saves `name.wav + name.reference.txt`; Castwright caches `voices/qwen/<id>.pt` and uses a "short ~90-char CALIBRATION_TEXT pangram" for the reference clip because "The persona instruct defines the voice identity; the reference text is just a phonetic carrier"; Discussion #279 shows the save/load snippet. **Known cost**: "the cloned version loses emotional range and naturalness. When used purely within Voice Design, it sounds way better" ([Discussion #220](https://github.com/QwenLM/Qwen3-TTS/discussions/220), opening post by GalenMarek14, 21 Feb 2026, no staff reply) [verified]; clone ignores instruct ("Voice cloning (Base) ignores the instruction field entirely" — TTS-Audio-Suite README L932 [verified]; Castwright docs/features/108: "Qwen ignores per-utterance `instruct` on cloned/designed voices today" [verified; "designed" there means design-then-cloned `.pt` voices]). faster-qwen3-tts contradicts slightly: "`instruct` is available on Base voice cloning, but treat it as experimental … behaved much more predictably in ICL mode". Base clone also has its own drift: "sometime it taken random speaker" ([issue #80](https://github.com/QwenLM/Qwen3-TTS/issues/80)), "~20% of requests" diverge on leading words, short lines "sound like a third, different voice" ([SwiftVoxAlta #12](https://github.com/intrusive-memory/SwiftVoxAlta/issues/12)).
2. **Fixed seed** — works only for byte-identical inputs. dev.to (27 Apr 2026): "It ensures that the exact same text produces the exact same audio (even the MD5 hashes will match)" [corrected: exact wording; checkpoint unspecified]; "As soon as you change the input text—even by a single character—the seed's constraint collapses" and "The model's 'vocal cords' drift, and the persona shifts randomly" [verified]. [Rapid-MLX #1338](https://github.com/raullenchai/Rapid-MLX/issues/1338): "Passing the same description across multiple `/v1/audio/speech` calls does not reliably reproduce the same timbre — the voice drifts between utterances." [verified: 30 Jul 2026, filed by the repo owner as a feature request against his own MLX server; closed with no comments, so whether he shipped a `voice_id`/`voice_seed` is unknown — the report's "no implementation exists" in item 8 is not established by this issue]. On vLLM even a fixed seed is not byte-identical: "The fixed seed does not guarantee byte identical output, because it is applied only to one part of the model, but the fixed seed voice will 'behave' the same … there will be seeds that produce more varying output … And there will more stable seeds, without much artifacts. You just need to find one" ([issue #298](https://github.com/QwenLM/Qwen3-TTS/issues/298)) [verified: user BeeegZee, 9 May 2026, who adds "This is based on my experience with proper SFT custom voice, not zero-shot voice cloning" — so a fine-tuned CustomVoice on vLLM-Omni, not VoiceDesign; another user replying said a seed still gave "some voice changes"].
3. **Cherry-pick per line by seed** — alexandria's author on making pure-design outputs match: "This still requires some fidling and re-generating lines with different seeds to make all samples similar enough but with a bit of effort you can get good results" ([Discussion #220](https://github.com/QwenLM/Qwen3-TTS/discussions/220)) [verified: Finrandojin, 14 Mar 2026. Context: he was regenerating VoiceDesign lines to build a *LoRA training set*, i.e. the matched takes then feed a fine-tune — the practice is pure-design regeneration, the end product is not]. TTS-Story added "configurable candidates per speaker, improved bulk candidate generation" for voice casting [not re-checked].
4. **Reuse the exact prompt text** — deapi: "VoiceDesign is not deterministic. The same description produces similar but not identical voices across runs … find a voice you like, then reuse that exact prompt text throughout your project." Necessary, not sufficient.
5. **Batching** — `generate_voice_design` accepts lists, but nothing in the corpus claims batching improves cross-line consistency; alexandria processes design chunks *sequentially* ("Voice Design is sequential") and its batch path is for CustomVoice/Clone/LoRA only.
6. **Delivery drift even with identity held**: "The voice identity remains reasonably consistent, but the narrator's baseline cadence, prosody, and emotional delivery drift between chunks. One chunk may become excited, another dramatic, another melancholy … even though the same voice, instructions, and seed are being used. I observed this behavior with both CustomVoice and VoiceDesign, across multiple seeds" ([Discussion #220, storm-fox, 10 Aug 2026](https://github.com/QwenLM/Qwen3-TTS/discussions/220)) [verified; one user's report, no staff reply]. tts-audiobook-tool offers an "experimental rolling continuation mode" for Qwen3-TTS **Base** (feeding prior output forward) — Base only.
7. **Lower temperature / greedy** — no VoiceDesign report. In the fine-tune case, greedy (`temperature 0, top_k 1`) made onset instability "deterministic per input" but did not remove it ([issue #343](https://github.com/QwenLM/Qwen3-TTS/issues/343)); "tried leading/trailing text padding (leading made it worse)" [verified quotes; Base LoRA fine-tune, not VoiceDesign — see §2].
8. **Not available**: the community-requested `voice_id`/"lock designed voice" handle (Rapid-MLX #1338; HF discussion #3 "Re-use a designed voice" [verified: open, one post, the poster answered himself with "Voice Design then Clone"]; Discussion #220 "store created voices in memory directly within Voice Design" [verified]) — no implementation exists in the Qwen library [corrected: scoped to the Qwen library; Rapid-MLX #1338 is closed without comment, so that server's status is unknown]; the 25Hz VoiceEditing model that "will support both cloning and instruct" ([issue #25](https://github.com/QwenLM/Qwen3-TTS/issues/25), staff) is unreleased [verified: not on HF as of 12 Sep 2026].

---

## 8. Per-line emotion / delivery without changing the voice

- **Method everyone uses:** one string = identity + direction. alexandria: "Set a base voice description (e.g., 'Young strong soldier'). Each line's instruct is appended as delivery/emotion direction" → `f"{base_desc}, {instruct}"`, with line directions like `"Startled and fearful, sharp whispered question, voice cracking with panic."`, `"Menacing confidence, low smug drawl with a dark chuckle, savoring the moment."`, `"Calm, even narration."` — and its own guidance for the LLM: "`instruct` — 2-3 sentence TTS voice direction sent directly to the engine. Set tone, describe delivery, then give specific references. Example: 'Devastated by grief, Sniffing between words and pausing to collect herself, end with a wracking sob.'" ([alexandria README](https://github.com/Finrandojin/alexandria-audiobook)) [verified: README lines 296–298, 437, 440–443 and `app/tts.py` L804–810 (`f"{base_desc}, {instruct}"`); repo last pushed 2 Aug 2026, ~1,000 stars. Note the README calls Voice Design mode "ideal for minor characters" — the author's own signal that he does not trust it for leads]. Its "character style" for CustomVoice is likewise appended: `instruct = f"{instruct_text} {character_style}"` [not re-checked].
- **Delivery arcs inside one line** are in the official examples ("slowing down slightly at the end for emphasis", "transitioning from steady to passionate", "pitch rising at key moments") — so intra-line direction is a trained capability.
- **Cost:** no source demonstrates that changing the appended direction keeps timbre fixed; the dev.to author's characterisation is that tone instructions "are personality modifiers, not identity definitions" that "adjust the 'texture' of the voice but cannot lock the underlying persona across different text inputs". Castwright deliberately gave up: "We bake the character's dominant emotional register into the designed persona and keep the analyzer's per-sentence emotion tags detected + wired but UNUSED at synth".
- **Laughs/sighs/barks:** write them as pronounceable text in the *line*, not the instruct. Staff: "'hahaha' or 'emmm'" ([issue #9](https://github.com/QwenLM/Qwen3-TTS/issues/9)). alexandria: "Vocalizations are written as real pronounceable text that the TTS speaks directly — no bracket tags or special tokens": Gasps "Ah!", "Oh!" (+ instruct "Fearful, sharp gasp."); Sighs "Haah...", "Hff..."; Laughter "Haha!", "Ahaha..."; Crying "Hic... sniff...". Unwanted laughter from an emotional instruct is real ([issue #16](https://github.com/QwenLM/Qwen3-TTS/issues/16): instruct "very happy" produced laughter; fix "very happy but without laughing").
- **Emotion-preset nodes** such as [Dawizzer/ComfyUI-Qwen3TTS-Emotional](https://github.com/Dawizzer/ComfyUI-Qwen3TTS-Emotional) ("80+ emotion presets") do not send emotion to the model at all: "The node adjusts three generation parameters based on emotion: Temperature, Repetition Penalty, Top-p". Not a real control.
- **Cloud contrast:** the Alibaba designed-voice API has no per-request style field either; styling is at description time.

---

## 9. Failure modes and reported fixes

| Failure | Where reported | Fix / note |
|---|---|---|
| Different voice every run | §0; issues #4, #13; Rapid-MLX #1338; deapi | sample & pick; seed only for identical input; clone (rejected) |
| Voice changes at chunk boundaries | Discussion #220 | no in-model fix; clone; cherry-pick seeds |
| Delivery/cadence drift across chunks with same seed | Discussion #220 (Aug 2026) | none; "continuation mode" requested |
| Onset instability, gender flip, whisper in first 1–2 s, worse on short lines | issue #343 (Base LoRA fine-tune, baked speaker embedding); SwiftVoxAlta #12 (clone) — **no VoiceDesign report** [corrected] | longer lines render correctly; "leading padding made it worse"; short standalone lines are the risk — in those regimes |
| Laughter / "OK" / extra words not in text | issue #16 (CustomVoice `Ryan`) | "very happy but without laughing" (staff: "may be able to"; unconfirmed); expressive instructs invite paralinguistics |
| Last one or two words truncated | HF discussion #4 (unanswered); mlx-audio #882 | mlx-audio: even `max_tokens=8192` + terminal punctuation did not fix it; Dawizzer: "seed-dependent … Use longer input text" |
| Garbage / many overlapping voices | issue #78 | unresolved (Windows); DarioFT: "Try a different seed - some seeds may produce more stable results" |
| Infinite loops / very long outputs | ocdevel | cap `max_new_tokens`, retry seed |
| Speech accelerates over long text | issues #239, #290; mlx-audio #910 | Base/clone path; suspected repetition-penalty over accumulated tokens; keep segments short |
| Chinese / Asian accent in English | §5 | explicit `language="English"`; named locale in description; no reliable fix |
| Dialect requests ignored | issue #248 | "instruction tuning focuses on prosody and emotion, not dialect switching" |
| Numbers / dates misread | Habr; issue #265 (cloud) | spell out |
| 0.6B has no VoiceDesign, no instruct | README; code (`if tts_model_size in "0b6": instruct = None`) | 1.7B only |
| Hollow/cracking audio on ComfyUI | issue #307 | packaging/version issue, not prompting |

---

## 10. How the ComfyUI / pipeline tools expose voice design (for reference)

- **TTS-Audio-Suite** ([README](https://github.com/diodiogod/TTS-Audio-Suite)): "The voice-design instruction lives on 🎨 Voice Designer; the engine keeps model, language, and generation settings." Node inputs: `reference_text` (default ~10 s of varied text), `seed` ("0 keeps the provider's random behavior. A fixed nonzero seed also lets Save Character Voice recognize an identical generation safely"), `voice_instruction` (default `"A warm, confident adult voice with natural pacing, clear articulation, and a subtle expressive smile."`, tooltip "Describe the voice identity and delivery to create: age, gender, pitch, texture, accent, pace, emotion, and speaking style"). Output is a `NARRATOR_VOICE` = reference wav + transcript → it is then *cloned* by the Base model for actual lines. Style instructions "only work with CustomVoice and VoiceDesign"; on VoiceDesign the engine's instruction "Supports style instructions alongside the voice description". A user abandoned designers "because of distinct accents" ([TTS-Audio-Suite #313](https://github.com/diodiogod/TTS-Audio-Suite/issues/313)).
- **DarioFT/ComfyUI-Qwen3-TTS**: Voice Design node `instruct` + `text` + `seed`; documented workflow "Voice Design → audio → Prompt Maker → Save Prompt (saves embedding) … Load Prompt → Voice Clone". Troubleshooting: "Try a different seed - some seeds may produce more stable results."
- **alexandria-audiobook**: see §7/§8; also builds LoRA datasets from VoiceDesign output ("Neutral-only training data produces flat voices that resist instruct prompting").
- **Castwright**: persona via LLM prompt (§4), design → `.pt` clone, per-line emotion deliberately unused.
- **Voice-Clone-Studio**: seed (`-1 random`), advanced Qwen sampling sliders per model type, JSON-instruct preset (§6).

---

## 11. Things nobody in the corpus reports (do not assume)

- Any measured F0/pitch outcome of any phrasing (no Hz numbers anywhere).
- Any controlled test of description *length* or *word order*.
- Any effect of `temperature`, `top_k`, `top_p`, or `subtalker_*` on timbre stability in VoiceDesign.
- Any English wording that reliably suppresses the Chinese accent.
- Any way to keep identity fixed while varying the instruct, other than cloning.
- Whether including the *line* in the reference (design once with the whole cue sheet) helps — untested.
- Anything from Reddit/YouTube (inaccessible here).

---

## 12. Distilled, source-backed recommendations for pure-design mode

These are inferences from the material above, not community-verified recipes.

1. **Write identity as acoustics in the official order**: gender → explicit age band → pitch band → texture → pace → emotional baseline → purpose clause; 15–40 words; English; no feelings/backstory; no stacked intensifiers; no conflicting pairs (avoid "deep" + "old" without rasp/thinness carrying the age). Model on the official Space examples.
2. **Always pass `language="English"`**, never `"Auto"` (it changes the prefill).
3. **Per-line direction goes after the identity, comma-joined**, phrased like the official arc examples ("The pace is brisk … slowing down slightly at the end"); put laughs/sighs in the *text* as "Haha.", "Hff…", not as tags; add negations ("without laughing") when a mood instruct over-triggers.
4. **Expect identity variance and budget for it**: generate N candidates per line with different seeds, auto-rank by closeness to a chosen anchor take (e.g. speaker-embedding cosine, median F0) and keep the nearest — this is the only pure-design consistency practice anyone reports (alexandria author, TTS-Story candidates). Record `(instruct, text, seed, sampling params)` per kept take; a kept take is exactly reproducible only with identical inputs.
5. **Prefer longer lines / merge very short cues** — short standalone utterances are where wrong-timbre onsets concentrate in the fine-tune and clone regimes (issue #343, SwiftVoxAlta #12); nobody has reported this for VoiceDesign, so treat it as a cheap precaution, not a documented VoiceDesign fix [corrected].
6. **Keep segments to a few sentences** — long single generations drift in cadence and risk acceleration/truncation.
7. If a stable identity ever becomes non-negotiable, the corpus is unanimous that only design-then-clone (or a LoRA trained on designed takes) delivers it, at the cost of expressiveness and per-line instruct.

---

## Verification

Skeptic pass, 12 Sep 2026. Every GitHub source was re-read through the GitHub API (issue bodies, comment authors and their `author_association`, discussion threads via GraphQL); the Qwen source files, README, `generation_config.json` and the HF Space `app.py` were pulled raw; the Alibaba, ocdevel, getstream and dev.to pages were fetched and grepped. Corrections are marked inline as `[verified]`, `[corrected: …]`. Nothing had to be struck outright — every quote exists at its cited URL — but several were attributed to the wrong kind of person or the wrong model.

### Held (quote present, meaning as stated, about the open VoiceDesign checkpoint or the shared code path)
- No speaker embedding in VoiceDesign (`speaker_embed = None`, modeling_qwen3_tts.py L2088). Code is current: last repo push 17 Mar 2026, pypi `qwen-tts` 0.1.1 (6 Feb 2026), checkpoint last modified 29 Jan 2026.
- Staff (wangxiongts, Qwen team, COLLABORATOR): sample voice design several times and pick (#4); non-verbal cues are not tags, only "hahaha"/"emmm" text with randomness (#9); 25Hz voice-editing model "will support both cloning and instruct" (#25). 25Hz still unreleased: HF `Qwen` org has five 12Hz model repos + the tokenizer, #294 open.
- `language` changes the codec prefill (`nothink` vs `think + language_id`), code L2110–2147; README says set it explicitly (comment is on the CustomVoice example, same argument).
- `generation_config.json` values byte-for-byte; no `seed` anywhere in the library; tools use `torch.manual_seed`.
- Discussion #220: all three quotes (chunk-boundary voice change and clone losing range — GalenMarek14; seed cherry-picking — Finrandojin; cadence drift with same seed on CustomVoice *and* VoiceDesign — storm-fox, 10 Aug 2026). No staff reply in the thread.
- Discussion #315 (Spanish VoiceDesign accent sensitivity): verbatim, unanswered.
- Alibaba Model Studio page: five principles, dimension table, examples, 2,048 chars, Chinese/English only, no accent dimension, no per-request style field, 1,000 voices.
- HF Space: all eight example instructs verbatim.
- Castwright #830 / docs 160 / skill file: the age-as-acoustics finding and the elderly example, verbatim.
- alexandria README and `tts.py`: base description + per-line instruct comma-joined; "ideal for minor characters"; vocalizations as pronounceable text.
- TTS-Audio-Suite node tooltips and README lines; Rapid-MLX #1338 body; UChi-JCL #1 "Chinese-language instructions work dramatically better…"; getstream "high-pitched deep bass"; ocdevel intensifier/duration lines.

### Corrected
- **Wrong attribution:** issue #13's "voices are different and randomized each time" is an ordinary user (Idiotabtcodes, no repo association), not a "community maintainer". Issue #248's "instruction tuning focuses on prosody and emotion" is the issue author's own conclusion, not "a maintainer". The "can't save a designed timbre" line in #4 is a user, not staff.
- **Wrong model/product:** the HF Voice-Design Space calls the DashScope cloud API (`qwen-voice-design`, target `qwen3-tts-vd-realtime-2025-12-16`), not the open checkpoint. Issue #343 (onset instability, gender flip) is a Base LoRA fine-tune with a baked speaker embedding on vLLM-Omni; "same mechanism" was the researcher's inference and no VoiceDesign onset report exists. Issue #16 (negation fix) and #248 (12-emotion test) are CustomVoice presets; #298 (seed "behaves the same", find a stable seed) is an SFT CustomVoice on vLLM. UChi-JCL #1 is CustomVoice and was trying to *produce* a Chinese accent. The dev.to seed article never names its checkpoint.
- **Overstated certainty:** the #16 negation fix was staff's "may be able to" and was never confirmed by the reporter; ocdevel's "no effect whatsoever" is an unattributed second-hand quote (not on the Alibaba English page, not in any Qwen3-TTS issue); Rapid-MLX #1338 is closed without comment, so "no implementation exists" holds for the Qwen library only.
- **Small errors:** "13 Sep 2026" → 12 Sep; "six 12Hz checkpoints" → five model checkpoints plus tokenizer; the README language comment sits on the CustomVoice example; ocdevel's 15–40 words is its reading of the official examples, not a test; "The README's `[laugh]`-style bracket tags" — the README has no such tags.

### Not from any source (researcher inference, now labelled)
- "Identity emerges from sampling the first codec frames" (§2) — plausible from the code, unsourced.
- Recommendation 4's "auto-rank by speaker-embedding cosine / median F0" — nobody in the corpus does this; it is the report's proposal.
- Recommendation 5 (merge short cues) rests on non-VoiceDesign regimes.

### Missing relative to the angle
- **Reddit and YouTube**: confirmed blocked for this environment (`reddit.com` refuses the crawler). r/LocalLLaMA is where most hobbyist VoiceDesign experience will be; this survey has none of it.
- **No VoiceDesign-specific test of anything**: every controlled-ish observation (emotion list, negation, seed stability, onset instability, instruct language) is CustomVoice, fine-tune or clone. For the open VoiceDesign checkpoint the corpus has exactly: staff "sample and pick" (#4), GalenMarek14/storm-fox in #220, cami-sosa in #315, Castwright's one elderly fix, alexandria's design choices, and the code.
- **No staff statement on VoiceDesign consistency in English** beyond #4 (Chinese) and #9/#25.
- **Not re-checked in this pass** (cited but outside the key-findings list): issues #78, #80, #239, #265, #290, #307; SwiftVoxAlta #12; mlx-audio #882/#910; TTS-Story worker; Voicebox #42; Voice-Clone-Studio prompt_hub; faster-qwen3-tts; deapi, voicecreator.pro, betterstack, Habr, qwen3tts.net; HF discussion "Are there any in-prompt instructions we can define?"; arXiv §3.3 quote; Discussion #279 and #332.
- **Nothing on AMD/ROCm**, nothing on pitch measurements, nothing on `subtalker_*` effects — as the report's §11 already says.
