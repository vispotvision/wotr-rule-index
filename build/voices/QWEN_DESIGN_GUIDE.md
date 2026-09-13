# Qwen3-TTS VoiceDesign — the WOTR instruct manual

Working manual for writing `qwen_instruct` strings for War of the Realms characters and for
keeping a designed voice stable across a scene. Engine: `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`,
pure voice-design mode (no reference clip, no Base clone, no RVC), driven by
`build/qwen_worker.py` on ROCm. Written 12 Sep 2026 from the four survey reports in
`build/voices/survey/` (`qwen-official.md`, `qwen-community.md`, `qwen-science.md`,
`qwen-consistency.md`) plus the local bakeoff data in `build/voices/bakeoff/`.

Conventions. Every claim that came from a source keeps its link. Where the four reports
disagree, or a report marked its own claim unsupported, this guide says so instead of picking.
"Unmeasured" means nobody has published a test; "local" means one run on Isaac's machine on
12 Sep 2026, which is a single datum, not a finding. Specialist terms are glossed in plain
language the first time they appear.

Three hard facts frame everything below:

1. **VoiceDesign has no identity slot.** The Base and CustomVoice models insert a speaker
   embedding (a fixed numeric fingerprint of one voice) before generation; VoiceDesign's code
   path sets `speaker_embed = None` (`# Instruct create speaker`,
   [modeling_qwen3_tts.py l.2088](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/core/models/modeling_qwen3_tts.py))
   and the checkpoint ships no `speaker_encoder` weights at all (404 tensors, all under
   `talker.`; safetensors header read 12 Sep 2026). The description defines a *region* of
   voice-space; every call draws a fresh member of it. This is the "one-to-many problem"
   named by [PromptTTS 2](https://arxiv.org/abs/2309.02285v2) and never solved for
   description-only models.
2. **There is no seed argument, and a seed reproduces a take, not a voice.** The package never
   calls `torch.manual_seed` ([qwen3_tts_model.py](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/inference/qwen3_tts_model.py),
   grep empty). Seeding outside the call gives bit-identical audio only for identical
   `(instruct, text, kwargs)`; change one character of the text and the draw changes
   ([dev.to, Apr 2026](https://dev.to/lcmd007/from-stochastic-drifting-to-vector-anchors-how-i-solved-voice-consistency-in-qwen-tts-4dff);
   measured on MOSS-VoiceGenerator as 2.2 and 7.6 semitones of median-pitch movement across
   three lines under one seed, [audio.cpp MOSS doc](https://github.com/0xShug0/audio.cpp/blob/main/docs/community_models/moss_voicegen.md)).
   Local confirmation: seed 7, three different Gimbzo lines, median pitch 116 / 82 / 87 Hz
   (`build/voices/bakeoff/qwen3-consistency/scores.json`, rows `A_seed7_L1..L3`).
3. **The only sanctioned consistency path is "design then clone"**, which Isaac has ruled out
   ([README "Voice Design then Clone"](https://github.com/QwenLM/Qwen3-TTS#voice-design-then-clone);
   Qwen collaborator wangxiongts in [issue #16](https://github.com/QwenLM/Qwen3-TTS/issues/16)
   and [issue #4](https://github.com/QwenLM/Qwen3-TTS/issues/4): "voice design需要多Sample几次选择自己想要的音色",
   sample several times and pick). Inside pure VoiceDesign the ceiling is: narrow the region
   with the words, draw as few times as possible, and select draws by similarity to an
   approved anchor. That is what the rest of this manual is for.

---

## 1. How the model reads an instruct

### 1.1 Where the instruct goes

The instruct is the ChatML **user** turn; the line to be spoken is the **assistant** turn; there
is no system prompt. Verbatim from the wrapper
([qwen3_tts_model.py l.269-276](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/inference/qwen3_tts_model.py)):

```
instruct → "<|im_start|>user\n{instruct}<|im_end|>\n"
text     → "<|im_start|>assistant\n{text}<|im_end|>\n<|im_start|>assistant\n"
```

The instruct is embedded as text and **prepended** to the sequence, then a short codec prefix,
then the text. Empty instruct is allowed ("treated as no instruction"). In VoiceDesign's default
`non_streaming_mode=True` the entire target text is laid down before the first audio frame is
sampled, so the very first frame already depends on every word of the line
([modeling l.2199-2232](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/core/models/modeling_qwen3_tts.py)).
Practical consequence: the *line text* is a conditioning input on the voice draw, not just the
words to be spoken. Leave `non_streaming_mode=True`; the official HF Space hard-codes it
([app.py l.156-162](https://huggingface.co/spaces/Qwen/Qwen3-TTS/blob/main/app.py)).

### 1.2 What it was trained on

Officially: almost nothing is disclosed. The technical report says only "All data is formatted
in ChatML", "we prepend user-provided instructions containing fine-grained control signals",
and "we introduce a probabilistically activated thinking pattern during training to improve
instruction following, especially for complex descriptions"
([arXiv 2601.15621 §3.2-3.3](https://arxiv.org/html/2601.15621)). The word "caption" does not
occur in the report; no attribute list, no caption source, no dataset size. Everything below
about the training schema is inference from Qwen's published sample instructs.

The strongest evidence is the **twelve-field caption template** shown in the open checkpoint's
release blog ([qwen.ai, 22 Jan 2026](https://qwen.ai/blog?id=qwen3tts-0115)), which matches
field-for-field, in the same order, the APS (Acoustic-Parameter Specification) captions of the
benchmark Qwen was scored on, [InstructTTSEval](https://arxiv.org/abs/2506.16381) — captions
written by Gemini from real audio clips. Verbatim, the "Age Control" row (the closest official
example to a Darius/Gimbzo register):

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

What the template tells you (observations, not official statements — `qwen-official.md` §4.4):

- The captions describe **the specific clip**, including delivery changes inside it ("slowing
  slightly after the initial exclamation"). The model was trained to map "this description →
  this exact performance", which is why one string carries both timbre and line reading.
- `gender`, `pitch`, `age`, `accent`, `texture` are the stable-identity fields; `speed`,
  `volume`, `emotion`, `tone` are the per-clip delivery fields; `clarity`, `fluency`,
  `personality` sit between.
- Accent is **always named** ("British English", "American English", "General American
  English"). Leaving it out means the model picks.
- Pitch vocabulary never goes past "Low male pitch"; no official instruct says "bass" or
  gives a number. Age never goes past "Middle-aged" / "senior (55+)" / "年近七十" (nearly seventy).

### 1.3 Attribute order

Official order: `gender, pitch, speed, volume, age, clarity, fluency, accent, texture, emotion,
tone, personality`. No source tests whether order matters
([qwen-community.md §6](survey/qwen-community.md)); every guide and tool writes identity first
and delivery last (getstream, Castwright, alexandria's `f"{base_desc}, {instruct}"`). This guide
uses the official order because it is the closest thing to the model's own language, and puts
per-line direction in the delivery fields or in a trailing sentence.

### 1.4 Length

- Official examples run from 4 words ("Playful Homebody Sis", hosted model) through 15–40-word
  sentences to the full 12-field block (~90-110 words) and a multi-paragraph character card.
- DashScope (hosted) caps descriptions at 2,048 characters, Chinese or English only
  ([Alibaba Model Studio](https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-design)).
  The open package enforces **no** length limit on `instruct` or `text`.
- Community "sweet spot" claims (ocdevel 15-40 words; getstream 40-80 words; voicecreator 1-3
  sentences) are readings of the official examples, not tests. **No controlled length
  experiment exists.**
- The five DashScope principles, verbatim: "Be specific, not vague", "Be multi-dimensional, not
  one-dimensional", "Be objective, not subjective", "Be original, not imitative", "Be concise,
  not redundant". Same family, hosted product; the only official prose guidance there is.

### 1.5 What it ignores or handles badly

| Input | Evidence |
|---|---|
| Numbers as constraints ("finish within five seconds") | Qwen collaborator, [issue #23](https://github.com/QwenLM/Qwen3-TTS/issues/23): "The model currently does not support this kind of control. Our control capabilities are mainly reflected in controlling speaking style, expressiveness, and prosody." Hz values: no source shows them honoured; no caption pipeline ever contained one ([qwen-science.md §5](survey/qwen-science.md)). Age in years *does* appear in Qwen's own samples ("17 years old", "30s"). |
| Dialect switching | [issue #248](https://github.com/QwenLM/Qwen3-TTS/issues/248) (CustomVoice): Sichuan/Cantonese requests "remain in standard Mandarin"; the reporter's own conclusion: "instruction tuning focuses on prosody and emotion, not dialect switching". VoiceDesign config has `spk_is_dialect: {}`. |
| Psychological adjectives with no acoustics | Castwright [#830](https://github.com/dudarenok-maker/Castwright/issues/830): "weary"/"weathered" — "which VoiceDesign ignores"; the fix that "audibly fixed it" named the age and added "dry rasp, faint tremor, low-to-medium not deep". One developer's ear, one character. |
| Stacked intensifiers | ocdevel: "'very, very deep' adds nothing over 'deep'" — asserted, not tested. |
| Conflicting attributes | getstream: "high-pitched deep bass" → "may output unpredictable results by favoring one attribute over the other" — author's own limitations note, unmeasured. |
| Film / game / actor comparisons | DashScope principle 4: "The model doesn't support imitation". No reviewed caption pipeline (InstructTTSEval, DataSpeech/Parler, CapSpeech, ParaSpeechCaps) puts a named person in a caption; RP prompts use role nouns ("worn soldier", "commanding officer"), never named characters. Qwen's own data: unknown. |
| Bracket tags `[laugh]` `[sigh]` | wangxiongts, [issue #9](https://github.com/QwenLM/Qwen3-TTS/issues/9): "Our current model does not support explicitly generating non-linguistic signals. It can only produce such sounds implicitly through expressions like 'hahaha' or 'emmm'". Tags will be spoken or treated as noise. |

### 1.6 The "thinking" slot and the language argument

The training-time "thinking pattern" survives at inference only as a language token. With
`language="English"` the codec prefix is `[think, think_bos, <english=2050>, think_eos]`; with
`"Auto"` it is `[nothink, think_bos, think_eos]`
([modeling l.2110-2147](https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/core/models/modeling_qwen3_tts.py)).
So `language` is not cosmetic. The two official usages disagree: the team's InstructTTSEval runs
used `language="auto"` ([README §Evaluation](https://github.com/QwenLM/Qwen3-TTS#evaluation)),
while every README voice-design code example passes an explicit language. No official statement
says which is better for design fidelity. **Decision for WOTR: always `language="English"`** —
it is the one documented lever against accent drift ([qwen-community.md §5](survey/qwen-community.md);
TTS-Audio-Suite README: "language tags directly control output"), and `qwen_worker.py` already
does this.

### 1.7 Instruct formats demonstrably in-distribution

| Format | Example | Attested where |
|---|---|---|
| 12-field caption | above | open-checkpoint release blog; InstructTTSEval APS split |
| Compact comma list | `Male, 17 years old, tenor range, gaining confidence - deeper breath support now, though vowels still tighten when nervous` | README, run through the open checkpoint with `language="English"` — the only compact instruct provably run on these weights |
| Style-only sentence | `Speak in an incredulous tone, but with a hint of panic beginning to creep into your voice.` | README, HF Space default |
| Prose persona | `A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation, is suitable for news broadcasting or documentary commentary.` | DashScope doc / hosted API |
| Character card (name / voice profile / background / presence / personality) | "Marcus Cole" block | open-checkpoint blog "Background Information" rows; the Chinese hosted-model card includes a *physical appearance* line |

Note on scores: on InstructTTSEval EN the open VoiceDesign checkpoint scores APS 82.9 / DSD 82.4
/ RP 68.4. RP (role-play, "eight-foot giant" style briefs) is the lowest for every system, but
the benchmark's own human reference audio scores RP 67.2 under the same Gemini judge — the
ceiling is the task's, not the model's ([qwen-science.md §1.4](survey/qwen-science.md)). Still:
the APS-style block is the most *specified* thing the model was scored on, and a fully specified
block will draw from a tighter region than a persona sentence. That is inference, not a measurement.

---

## 2. Vocabulary

Plain-language glossary for the acoustic terms used in the table:

- **F0 / fundamental frequency** — the speaking pitch, in Hz. Adult male typical range ~93-135 Hz,
  mean ~116 Hz ([voicescience.org](https://www.voicescience.org/lexicon/average-speaking-frequencies/)).
  A **semitone** is one piano key; 12 semitones is an octave. 105 Hz → 145 Hz is 5.6 semitones.
- **Formants** — the resonances of the throat and mouth. Closer-spaced formants read as a longer
  vocal tract, i.e. a bigger body. Listeners use *both* low F0 and low formants to judge size
  ([Pisanski et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5043380/)). No caption
  pipeline labels formants, so "big" has no trained word behind it; only "deep" (= low F0) does.
- **Jitter / shimmer** — cycle-to-cycle wobble in pitch (jitter) and loudness (shimmer). High
  values are what a listener calls rough, gravelly, or old.
- **HNR** (harmonics-to-noise ratio) — how much of the sound is clean tone vs. breath noise. Low
  HNR = breathy, hoarse, husky.
- **Spectral tilt / H1-H2** — how fast the overtones fall off. Pressed/creaky voice has less
  tilt (brighter, tighter); breathy voice has more. "Banked pressure" lives here acoustically,
  but no caption vocabulary names it.
- **Vocal fry / creak** — the slow, popping vibration at the very bottom of the range (25-50 Hz
  pulses). A texture tag in ParaSpeechCaps; rare in data.
- **Speaking rate** — phonemes per second with silences removed. Parler's bins: "very slowly"
  < 3.8 ph/s up to "very fast" > 23 ph/s.

Parler/DataSpeech's caption bins for a male speaker's mean F0
([v02_bin_edges.json](https://raw.githubusercontent.com/huggingface/dataspeech/main/examples/tags_to_annotations/v02_bin_edges.json)),
the only published Hz-to-word mapping in this model class (Qwen's own bins are undisclosed):

| Male mean F0 | Caption word |
|---|---|
| < 82 Hz | very low pitch |
| 82-99 Hz | quite low pitch |
| 99-116 Hz | slightly low pitch |
| 116-133 Hz | moderate pitch |
| 133-150 Hz | slightly high pitch |

So Isaac's 105 Hz take was "slightly low" and the 145 Hz take was "slightly high" in that
vocabulary — a brief that says only "deep" is not pinning anything. Gimbzo as briefed should sit
under 82 Hz.

### 2.1 The table

"Trained words" = attested in Qwen's official instructs, the InstructTTSEval APS captions (counts
out of 1,000 EN captions), DataSpeech/CapSpeech bins, or ParaSpeechCaps tags with their annotator
definitions ([qwen-science.md §2, §5](survey/qwen-science.md)). "Avoid" = appears in no reviewed
caption vocabulary, or is documented as ignored or harmful. Qwen's captions are undisclosed, so
"not seen" means not seen in any *published* description-TTS vocabulary.

| Want | Trained words that work | Avoid | Notes |
|---|---|---|---|
| Very low speaking pitch | "Very low male pitch", "Low and deep male pitch", "Deep and resonant male pitch" (APS `pitch:`); "very low pitch" (DataSpeech bin; 3.2 % of CapSpeech captions); "deep bass", "booming baritone", "tenor range" (Qwen blog register words) | "sub-bass", "85 Hz", "an octave below", "Kratos", "Vader", "Mufasa" | Only 1 of 1,000 APS pitch fields says "very low"; extreme depth is rare even in the benchmark. Local: throat-strain words ("tight", "hoarse") pushed Darius's pitch **up** (Isaac, 12 Sep 2026, `build/casting/Darius.json` `qwen_note`). |
| Big body / resonance | "Deep" = "A low-pitched, resonant, rich voice"; "Booming" = "A loud, resonant, commanding, powerful voice" (ParaSpeechCaps defs); "resonant" (230/1000 APS textures) | "eight-foot", "giant", "huge chest", "cavernous", "as if echoing through a marble temple" (community, unmeasured) | Nothing labels vocal-tract length. Ask for depth + resonance; get body size from `formant` post-processing in `voice_shape.py` if needed. |
| Rasp / grit / gravel | "gravelly" (187/1000), "rough" (39), "raspy" (33), "harsh" (12), "coarse" (9), "husky" (10), "hoarse" ("Deep, gravelly, and somewhat hoarse."); "Guttural" = "A deep, throaty, gravelly voice"; DashScope word "husky" | "sanded", "sandpaper", "whiskey-and-cigarettes", "gravel-throated", "growl" as a timbre (APS has it only as an event) | Timbre words had 0.4k hours of labels in CapSpeech vs 33.5k for pitch — the rarest thing you are asking for. "gravelly" is by far the best-attested rasp word. |
| Dryness (little breath) | nearest: "firm" (34), "crisp" (15), "clear vocal texture"; opposite pole is "breathy"/"Whispered" | "dry" as a voice quality (a director's word, not an annotator's — harmless but inert); "pressed", "tense", "strained" as a *resting* timbre | "strained" (289 APS) is coded as effort under emotion and reads as raised pitch — the local Darius note above. |
| Old age | "elderly" (CapSpeech bin ≥ 65, 3.5 %; APS 38), "older adult", "Middle-aged to elderly", "mature vocal quality", "senior"; Castwright's rule: pair the age word with "a dry rasp or gravel, a thinner, reedier or breathier edge, and often a faint tremor or quaver" at slower pace; "Do NOT describe an old voice as merely 'deep'" | "ancient", "centuries old", "weary", "weathered" (ignored per Castwright) | Real ageing *raises* F0 at 80+ and adds jitter/shimmer ([JSLHR 2020 meta-analysis](https://pubs.asha.org/doi/10.1044/2019_JSLHR-19-00099)), so "elderly" and "extremely deep" pull against each other in the data too. Expect a trade-off; see the Gimbzo recipe for how this guide resolves it. |
| Child / girl | "child" (APS 18; CapSpeech bin 1-12), "Child or early adolescent", "High child pitch", "teenager", "pre-teen"; DashScope: "approximately an 8-year-old girl"; official Space: "A bright, high-pitched young girl's voice" | "twelve-year-old" alone — 12 sits on the child/teen bin edge; no source reports a twelve specifically | Use the bin word *and* the number. Child voices are 0.15 % of CapSpeech; InstructTTSEval found only two open models manage "child-like voices" — expect variance. |
| Slow, level, flat delivery | "slow", "slightly slow" (DashScope), "Deliberate pace", "measured" (96 APS), "Measured speed" = "controlled, deliberate ... even tone"; "very monotone"/"monotone" (DataSpeech), "Monotonous" = "dull, flat voice whose pitch, tone and speed remains constant"; "generally stable" (83 APS pitch fields); "even-toned" (DashScope) | "level" (emotionally), "unhurried", "glacial", "beat" | "very slowly" is 0.01 % of CapSpeech — ask for "slow, deliberate" and let `speed:` post-processing do the exact number. CustomVoice users found "Flat, monotone delivery. No emotion." → "unnatural" ([UChi-JCL #1](https://github.com/UChi-JCL/Multi-Modal-Semantic-Routing-for-vLLM/issues/1)); pair flatness with an emotion word ("composed", "serious"). |
| Precise / clipped articulation | "clear articulation", "distinct pronunciation", "precise" (142), "crisp" (23), "Highly articulate", "clipped" (8), "Punctuated" = "clear, deliberate pauses that emphasize key words" | "surgical", "military", "sanded" | Well covered. Note "clear"/"crisp"/"bright" sit near the *high* end of texture — don't stack them on a bass brief (getstream's conflict warning). |
| Contained pressure / cold | "firm", "authoritative" = "confident, clear voice ... expertise and assurance", "commanding", "composed", "calm", "cold, detached tone" (InstructTTSEval intro), "controlled", "serious", "stern" | "banked", "coiled", "iron", "glacial" | Put pressure in `emotion:`/`tone:`, not in `texture:`. |
| Quiet | "soft" = "gentle, low-volume, calm and soothing", "hushed", "low volume", "conversational level", "softening"; CustomVoice sample "请特别小声的悄悄说" (speak very quietly, in a whisper) | "under his breath", "sotto voce" | The benchmark barely tests quiet: APS `volume` has "loud" 533 / "shouting" 151 vs "soft" 2, "quiet" 4, "whisper" 1. Expect weaker adherence than for loud. |
| Whisper | "Whispered" = "A breathy, low-volume voice typically used to speak discreetly"; "Whispering" was followed in a 12-instruction CustomVoice test ([issue #248](https://github.com/QwenLM/Qwen3-TTS/issues/248)) | — | A whisper has no voicing and therefore no pitch; the speaker-embedding score against the anchor will drop for reasons that are not a wrong voice (reasoning, see §5.5). |
| Urgent | "urgent" (63 APS speed fields), "hurried", "rushed", "rapid", "accelerating", "conveying urgency"; "Anxious" = "rapid or jittery speech patterns" | — | Well covered. |
| Loud | "loud", "projecting", "forceful", "shouting", "booming" | — | Best-covered volume words. "shouting" invites strain and paralinguistics. |
| Laugh / bark-laugh | "Laughing" = "intermittent sounds of laughter", "boisterous laugh", "breaking into genuine, easygoing laughter at moments of embarrassment" (official, paired with "heh"/"ha" written in the text) | `[laugh]`; "one huge bark-laugh" as a tag | See §4.3 and §6. InstructTTSEval: only Gemini and GPT-4o-mini-tts "successfully laugh out"; "NO existing models successfully 'sigh'"; "NO models scream". |
| Accent-neutral English | "General American English" (192 APS), "Standard American English" (272), "American English" (804/1000), "Received Pronunciation" (30), "British English" | "accent-neutral", "no accent", "neutral English" — "neutral" never appears in any APS accent field | The trained meaning of neutral is General American. Always fill the field. |
| Gender | "Male"/"Female" | "gender-neutral" (unmeasured) | Best-controlled attribute in every pipeline; swapping only the gender word moved MOSS median F0 117→190 Hz over 47 designs. |
| Use-case anchor | "audiobook", "documentary narration", "animation character", "news broadcast" (DashScope table); "suited for expressive character dialogue" (Castwright's mandatory trailing clause) | — | Cheap and official; Castwright made it mandatory after auditing prompts. Effect unmeasured. |
| Recording conditions | "very clear audio", "close recording" are Parler caption artefacts; nothing equivalent documented for Qwen | — | Harmless; untested. |

---

## 3. Recipes

Each recipe is one main instruct plus two variants, all single-line strings with no double
quotes inside, so they paste straight into `build/casting/<Name>.json` as `"qwen_instruct"`.
The main version uses the 12-field template (the model's most-attested schema); variant A is
the compact README form; variant B is a prose persona in the DashScope register.

How to read them. In the 12-field form the **identity block** is `gender / pitch / age /
clarity / fluency / accent / texture / personality` and must stay byte-identical for every line
of that character; the **delivery block** is `speed / volume / emotion / tone` and is what
per-line direction swaps (§4). The recipes below hold the character's *default* delivery.

Casting decisions made here (Isaac can overrule, but they are decided, not pending):

- **Giant vs. age.** The data says "elderly" thins and raises a voice; Gimbzo's card says age
  shows as "wear and patience, never frailty". So Gimbzo takes "older adult" (not "elderly"),
  carries age through "gravelly, rough, slightly hoarse", and never asks for tremor or thinness.
  Depth wins where the two conflict.
- **Darius.** Drops "hoarse"/"tight"/"strained" (local note: they raise pitch), keeps
  "slightly gravelly, firm". Middle-aged to older adult, not elderly — he is 56.
- **Old voice in a young body.** The vocal folds belong to the body, the manner to the man.
  Main recipe = young-adult timbre with old-man pacing, phrasing and composure; variant B goes
  the other way (aged timbre) for A/B. The model resolves a contradiction one way per sample
  ([qwen-science.md §5](survey/qwen-science.md)), so the brief must never ask for both.
- **Twelve-year-old girl.** Bin word plus number: "Child or early adolescent, a girl of about
  twelve." Serious by default (WOTR register); lively variant provided.
- **Combat narrator.** Male main, female variant (the pipeline carries `narrator-m` and
  `narrator-f` refs). Urgent but articulate; no "shouting".
- **Liturgical register.** Written as a *delivery block* on Darius's identity, because in the
  prose it is the same man's reading voice. Also given standalone for a generic celebrant.

### 3.1 Extreme depth + gravel — Gimbzo (giant)

Main (12-field):

```
gender: Male. pitch: Very low male pitch, deep bass, generally stable with almost no rise. speed: Slow, deliberate pace, with long pauses between sentences. volume: Conversational and projected from the chest, never loud. age: Older adult. clarity: Clear, distinct pronunciation. fluency: Highly fluent, long unbroken sentences with no hesitations. accent: General American English. texture: Deep, booming, resonant, gravelly and rough, somewhat hoarse with age. emotion: Calm and composed, without heat. tone: Flat, level, authoritative, matter-of-fact. personality: Blunt, patient, plainspoken, unhurried.
```

Variant A (compact, README form):

```
Male, older adult, deep bass, very low pitch - resonant, booming, gravelly and rough, slow and deliberate, calm and level, never loud, long unbroken sentences, General American English, suited for expressive character dialogue.
```

Variant B (prose persona):

```
An older man with an immensely deep, booming, resonant bass voice, very low in pitch and gravelly with age. He speaks slowly and deliberately at a conversational volume, in long unbroken sentences, calm, flat and authoritative, without heat and without theatrics. Clear General American English, suited for audiobook character dialogue.
```

Do not add: "eight-foot", "ancient", "giant", "Yhwach", "God of War", "as low as a human voice
goes" (no caption ever said any of these), "crisp"/"bright" (fights the depth). The current
`qwen_instruct` in `Gimbzo.json` contains "ancient, immense", "as low as a human voice goes"
and "imperious, quietly menacing" — the first two are untrained, the last is fine as `tone:`.

### 3.2 Aged dry baritone — Darius (56, soldier-priest)

Main (12-field):

```
gender: Male. pitch: Low male pitch, generally stable, with no upward inflection at the ends of sentences. speed: Measured, deliberate pace. volume: Conversational, restrained, never raised. age: Middle-aged to older adult. clarity: Highly articulate, precise and distinct pronunciation. fluency: Highly fluent, no hesitations, no fillers. accent: General American English. texture: Resonant and slightly gravelly, firm and dry. emotion: Serious, composed, tightly controlled. tone: Flat, formal, authoritative, cold. personality: Stern, reserved, disciplined, unsentimental.
```

Variant A (compact):

```
Male, middle-aged to older adult, low baritone, generally stable pitch - resonant, slightly gravelly, firm, measured and deliberate, flat and precise with no lift at sentence ends, serious and cold, never raises his voice, General American English, suited for expressive character dialogue.
```

Variant B (prose persona):

```
A stern man in his late fifties with a low, resonant, slightly gravelly baritone, firm and dry. He speaks at a measured, deliberate pace and a restrained conversational volume, flat and precise, formal and cold, with no lift at the ends of sentences and no warmth; a man reading a verdict. Clear General American English, suited for audiobook character dialogue.
```

Do not add: "tight", "hoarse", "strained", "tense" (local: raise pitch), "torn lung",
"sanded", "banked" (untrained). The existing `Darius.json` instruct's "gruff" is not in any
caption vocabulary either — harmless, probably inert.

### 3.3 Old voice in a young body (the seventy-year-old priest)

Main (young timbre, old manner):

```
gender: Male. pitch: Mid-to-low male pitch, generally stable. speed: Slow, deliberate, measured pace with clear pauses between phrases. volume: Conversational, soft-spoken, never raised. age: Young adult voice. clarity: Highly articulate and distinct pronunciation, every word placed with care. fluency: Very fluent, no hesitations, long complete sentences. accent: General American English. texture: Clear, resonant, smooth, with a slightly reedy edge. emotion: Calm, patient, gently weary. tone: Even, thoughtful, unhurried, quietly authoritative, like a much older man speaking through a young voice. personality: Composed, wise, formal, faintly sorrowful.
```

Variant A (compact):

```
Male, young adult, mid-to-low pitch, clear and resonant with a slightly reedy edge - speaks slowly and deliberately with the composed, unhurried, formal manner of a man in his seventies, soft-spoken, patient, General American English, suited for expressive character dialogue.
```

Variant B (aged timbre, for A/B against the main):

```
gender: Male. pitch: Mid-to-low male pitch, generally stable. speed: Slow, deliberate, measured pace. volume: Conversational, soft-spoken. age: Older adult, a man in his seventies. clarity: Highly articulate and distinct pronunciation. fluency: Very fluent, long complete sentences. accent: General American English. texture: Thin, slightly reedy and dry, with a faint tremor. emotion: Calm, patient, gently weary. tone: Even, thoughtful, quietly authoritative. personality: Composed, wise, formal.
```

The phrase "like a much older man speaking through a young voice" in the main `tone:` field is
a persona instruction of the kind the RP benchmark level tests; whether it moves anything is
unmeasured. The identity fields are what actually hold the young timbre.

### 3.4 Twelve-year-old girl

Main (12-field, serious):

```
gender: Female. pitch: High child pitch, light and bright, generally stable. speed: Moderate pace, slightly careful. volume: Conversational, clear. age: Child or early adolescent, a girl of about twelve. clarity: Clear, distinct pronunciation, slightly childish. fluency: Fluent, with short natural pauses. accent: General American English. texture: Bright, thin, light and clear. emotion: Serious, attentive, a little guarded. tone: Direct and earnest. personality: Watchful, brave, matter-of-fact.
```

Variant A (compact):

```
Female, a girl of about twelve, child or early adolescent, high bright light pitch, clear and slightly childish speech, moderate pace, serious and direct, General American English, suited for animation character dialogue.
```

Variant B (lively):

```
gender: Female. pitch: High child pitch, bright, rising at key moments. speed: Slightly fast, energetic. volume: Conversational to loud, clear. age: Child or early adolescent, a girl of about twelve. clarity: Clear, distinct pronunciation, slightly childish. fluency: Fluent and quick. accent: General American English. texture: Bright, thin, light and clear. emotion: Lively, curious, cheerful. tone: Animated and engaging. personality: Outgoing, quick, playful.
```

Do not use the README's "撒娇稚嫩的萝莉女声" register words (coquettish, clingy, cutesy) unless the
character is that. Child voices are the rarest adult-vs-child bin in the data; budget more
best-of-N for this character than for any adult.

### 3.5 Combat narrator

Main (male, 12-field):

```
gender: Male. pitch: Mid-to-low male pitch with controlled rises for emphasis. speed: Brisk, urgent pace, accelerating through action and slowing sharply on the decisive beat. volume: Projected, forceful, rising at moments of impact without shouting. age: Middle-aged adult. clarity: Highly articulate, precise and distinct pronunciation even at speed. fluency: Very fluent, no hesitations, no fillers. accent: General American English. texture: Firm, resonant, slightly gravelly. emotion: Tense, intense, gripping. tone: Urgent, vivid, precise, like a war correspondent reporting live. personality: Focused, unflinching, exact.
```

Variant A (female):

```
gender: Female. pitch: Mid-to-low female pitch with controlled rises for emphasis. speed: Brisk, urgent pace, accelerating through action and slowing sharply on the decisive beat. volume: Projected, forceful, rising at moments of impact without shouting. age: Middle-aged adult. clarity: Highly articulate, precise and distinct pronunciation even at speed. fluency: Very fluent, no hesitations, no fillers. accent: General American English. texture: Firm, resonant, slightly husky. emotion: Tense, intense, gripping. tone: Urgent, vivid, precise, like a war correspondent reporting live. personality: Focused, unflinching, exact.
```

Variant B (compact):

```
Male, middle-aged, mid-to-low pitch, firm resonant slightly gravelly voice - brisk urgent delivery that accelerates through action and lands hard on the decisive beat, projected but never shouting, highly articulate, tense and gripping, General American English, documentary-style combat narration.
```

Official precedent for the arc inside one instruct: the blog's "Gradual Control" row ("Starts
measured, then accelerates rapidly during emotional outburst"). Delivery arcs are a trained
capability ([qwen-official.md §4.4](survey/qwen-official.md)). Expressive briefs invite stray
paralinguistics (§6); if the narrator starts breathing or grunting, add "without any laughter,
sighs or grunts" to `tone:`.

### 3.6 Liturgical register

As Darius's reading voice (identity block byte-identical to §3.2, delivery swapped):

```
gender: Male. pitch: Low male pitch, generally stable, with no upward inflection at the ends of sentences. speed: Slow, measured, even, ceremonial pace with regular pauses at every phrase. volume: Conversational, projected, unvarying. age: Middle-aged to older adult. clarity: Highly articulate, precise and distinct pronunciation. fluency: Highly fluent, no hesitations, no fillers. accent: General American English. texture: Resonant and slightly gravelly, firm and dry. emotion: Solemn, composed, reverent, without any personal feeling. tone: Flat, even, monotone, like a priest reading a funeral office for the thousandth time. personality: Stern, reserved, disciplined, unsentimental.
```

Variant A (generic celebrant, compact):

```
Male, older adult, low resonant voice - slow, even, monotone ceremonial reading with regular pauses at every phrase, solemn and reverent, unvarying volume, no personal feeling, no laughter, General American English, suited for liturgical audiobook reading.
```

Variant B (generic celebrant, prose):

```
An older man with a low, resonant, slightly gravelly voice reading a solemn liturgy at a slow, even, ceremonial pace, pausing at every phrase, monotone and reverent, projected at an unvarying conversational volume with clear articulation and no personal feeling. General American English, suited for audiobook reading.
```

Caveat on Latin: the model's supported languages are `auto, chinese, english, german, italian,
portuguese, spanish, japanese, korean, french, russian` (config `codec_language_id`). Latin is
not among them. How Church-Latin lines read under `language="English"` is **unknown**; expect
English letter-to-sound rules. Spell phonetically in the text if a word misreads.

---

## 4. Per-line delivery

### 4.1 The mechanism and its cost

There is no separate style channel. Timbre and delivery share one string; the caption schema
keeps them in separate fields but the model reads them together. The only field practice for
direction-without-clone is alexandria's `f"{base_desc}, {instruct}"` — frozen identity, then
the line's direction ([alexandria README](https://github.com/Finrandojin/alexandria-audiobook);
the author calls VoiceDesign mode "ideal for minor characters"). Castwright gave up on per-line
direction entirely and bakes "the character's dominant emotional register into the designed
persona" (Castwright docs/features/108, cited in [qwen-community.md §7-8](survey/qwen-community.md); repo https://github.com/dudarenok-maker/Castwright).

**Nobody has measured whether changing the appended direction moves the identity draw more than
re-rolling the seed does.** Both `qwen-community.md` §11 and `qwen-consistency.md` §Missing name
this as the most important unanswered question. The reasoning in `qwen-science.md` §6.2 is that
every new description is a new draw and nothing holds identity; the counter-observation in
[discussion #220](https://github.com/QwenLM/Qwen3-TTS/discussions/220) (storm-fox, Aug 2026) is
that identity held "reasonably consistent" under a fixed seed and instruct while *delivery*
drifted. Treat per-line direction as a cost paid in extra best-of-N draws (§5).

### 4.2 The rule: substitute, do not append contradictions

The current `qwen_backend.py` appends a sentence to the brief ("Speak quietly, almost under the
breath, with the same voice."). That is the alexandria practice and it works, but on a 12-field
brief it can leave `speed: Slow` and `Speak fast and clipped.` in the same string — exactly the
"conflicting attributes" case getstream warns about. This guide's rule:

1. The identity block (`gender, pitch, age, clarity, fluency, accent, texture, personality`)
   is frozen bytes.
2. Per-line direction **replaces** the four delivery fields (`speed, volume, emotion, tone`);
   it does not append after them.
3. Cues that are sounds (a laugh, a sigh) go into **the text** as pronounceable words, and are
   *also* described in `tone:` — the official "Human-likeness" sample does both ("breaking into
   genuine, easygoing laughter" in the instruct; "heh", "huh… ha" in the text).
4. Pauses are not asked for in the instruct at all; the pipeline inserts silence
   (`DELIVERY["beat"]` = 0.6 s, `"long beat"` = 1.3 s in `audio_export.py`).
5. Exact pace and gain are applied after synthesis by `voice_shape.py` (Praat), so the instruct
   only needs the *direction* of the change, not the number — numbers are ignored anyway
   ([issue #23](https://github.com/QwenLM/Qwen3-TTS/issues/23)).

Until `qwen_backend.py` is changed from append to substitute, keep the default delivery fields
in the brief mild enough that an appended sentence does not contradict them (the recipes above
are written that way: "Measured", "Conversational", not "very slow", "never anything but quiet").

### 4.3 Tag and cue mapping

Cast-file tags are `[Name: word, word]` on a span; cues are `[laugh]` etc. inside the line.
`audio_export.py` already applies the numeric column; the instruct column is what this guide adds.

| Cast tag / cue | Pipeline does now | `speed:` / `volume:` / `emotion:` / `tone:` replacement (identity untouched) | Text edit | Strip |
|---|---|---|---|---|
| `slow` | Praat ×0.9 | `speed: Slow, deliberate pace.` | none | tag |
| `slower` | Praat ×0.8 | `speed: Very slow, heavy, deliberate pace, with weight on every word and long pauses.` | optionally break long sentences with commas (Parler documents commas as small breaks; untested on Qwen) | tag |
| `fast` | Praat ×1.1 | `speed: Brisk, fast-paced delivery.` | none | tag |
| `faster` | Praat ×1.2 | `speed: Rapid, hurried, clipped delivery.` | none | tag |
| `quiet` | gain ×0.7 | `volume: Soft, hushed, low volume, conversational level.` + `tone: <default>, subdued.` | none | tag |
| `loud` | gain ×1.3 | `volume: Loud, forceful, projecting.` | keep punctuation plain; exclamation marks invite strain | tag |
| `whisper` | ×0.95, gain ×0.5 | `volume: Whispered, breathy and hushed, very low volume.` + `texture:` **unchanged** | none | tag; exempt the line from the anchor-cosine reject (§5.5) |
| `urgent` | ×1.12, gain ×1.15 | `speed: Urgent, rapid, pressing.` `emotion: Tense, urgent.` `tone: Sharp, pressing, insistent.` | none | tag |
| `beat` | 0.6 s silence | nothing | nothing (do not write "..." — the model may read it as a trailing-off, an untested prosody cue) | tag |
| `long beat` | 1.3 s silence | nothing | nothing | tag |
| `[laugh]` | stripped → "Start with a short, huge bark of a laugh, then the line." | `tone: <default>; one short, loud bark of laughter before the first word, then no more laughter.` | prepend the written laugh as its own sentence: Gimbzo `HOO.`; others `Hah.` / `Ha!` (official sample uses "heh", "ha"; alexandria "Haha!", "Ahaha...") | cue |
| `[chuckle]` | "Start with a low chuckle." | `tone: <default>; a brief, low chuckle before the first word.` | prepend `Heh.` | cue |
| `[sigh]` | "Start with a sigh." | `tone: <default>; begins with an audible sigh.` | prepend `Haah...` (alexandria) | cue; expect failure — "NO existing models successfully 'sigh'" ([InstructTTSEval](https://arxiv.org/html/2506.16381v1)) |
| `[gasp]` | "Start with a sharp gasp." | `emotion: Startled.` `tone: <default>; a sharp gasp before the first word.` | prepend `Ah!` or `Oh!` (alexandria) | cue |
| `[groan]` | "Start with a low groan." | `tone: <default>; a low pained groan before the first word.` | prepend `Hnn.` (untested) | cue |
| `[breath]` | "Start with an audible breath." | `tone: <default>; an audible intake of breath before the first word.` | none | cue |
| `[cough]`, `[clear throat]`, `[sniff]`, `[shush]` | cough/clear throat directed; sniff/shush dropped | as pipeline; expect randomness | `Hff.` for sniff (alexandria); `Shh.` for shush | cue |

Everything in square brackets is stripped before the text reaches the model — the model has no
tag vocabulary and would speak or garble them ([issue #9](https://github.com/QwenLM/Qwen3-TTS/issues/9)).
Third-party sites advertising `[whispers] [laughing] [gasp]` tags for Qwen3-TTS have no primary
source ([qwen-community.md §3](survey/qwen-community.md)).

### 4.4 When a mood over-triggers

Qwen's suggested fix for unwanted laughter from an emotional instruct is negation: "very happy
but without laughing" — offered as "may be able to follow", never confirmed by the reporter,
and on CustomVoice ([issue #16](https://github.com/QwenLM/Qwen3-TTS/issues/16)). Cheap to try:
add "without any laughter or sighs" to `tone:` for a character who should never do them
(Darius). The reverse also holds: a flat, monotone brief on an expressive preset still produced
a stray "OK" before the line in that thread — flat briefs do not fully suppress the model's
expressiveness.

### 4.5 The line text is the one lever that leaves the instruct untouched

The README claims "adaptive control of tone, speaking rate, and emotional expression based on
instructions **and text semantics**" ([README](https://github.com/QwenLM/Qwen3-TTS)). Sentence
shape, punctuation and the words themselves are a delivery channel that keeps the instruct
byte-identical, and because the whole text is prefilled (§1.1) it is *also* a conditioning
input on the draw. Untested by anyone as a deliberate technique
([qwen-science.md §6.2](survey/qwen-science.md)). Prefer it for small shadings (a short flat
sentence for coldness, a comma-broken sentence for a beat) before reaching for a delivery swap.

---

## 5. Consistency protocol

Ordered by expected payoff, following `qwen-consistency.md` §8, with what each step is
documented to do and where the evidence runs out.

### 5.1 Freeze the identity block

Byte-identical identity fields per character, categorical words, accent named, no conflicting
pairs. Basis: the caption schema (§1.2), DashScope's "reuse that exact prompt text" advice
(deapi), MOSS's 117→190 Hz gender-word swap. Effect: narrows the region. Does not remove
per-call draws. Gender / age-band / pitch-band adherence is high (APS 82.9 EN).

### 5.2 Seed

`torch.manual_seed(seed)` immediately before `generate_voice_design`; the worker does
`seed + try_index`. Documented effect:

- Same seed + same instruct + same text + same kwargs → bit-identical audio on HF/torch on one
  machine ([dev.to](https://dev.to/lcmd007/from-stochastic-drifting-to-vector-anchors-how-i-solved-voice-consistency-in-qwen-tts-4dff);
  [MOSS doc](https://github.com/0xShug0/audio.cpp/blob/main/docs/community_models/moss_voicegen.md)).
  Use it to re-render an approved take. Log `(instruct, text, seed, kwargs)` with every kept take.
- Same seed, different text → different draw (local: 116 / 82 / 87 Hz; cosine to anchor
  0.48 / 0.22 / 0.19 for the three separate calls in `scores.json`).
- Under vLLM a seed is not byte-identical but "the fixed seed voice will 'behave' the same";
  "there will more stable seeds ... You just need to find one" ([issue #298](https://github.com/QwenLM/Qwen3-TTS/issues/298),
  user BeeegZee — SFT CustomVoice on vLLM, not VoiceDesign). Seed-hunting by ear is a
  documented practice on a *fixed-identity* model; on VoiceDesign it is anecdote.
- ROCm determinism: **unknown**. PyTorch guarantees nothing across platforms; SDPA forward
  passes are deterministic on documented backends; HIP is not mentioned
  ([PyTorch randomness notes](https://docs.pytorch.org/docs/2.13/notes/randomness.html)).
  `A_seed7_L1` and `A_seed7_L1_again` in `scores.json` carry identical cosine and F0, which is
  one local observation that the box is reproducible.

### 5.3 Decoding kwargs

Shipped defaults ([generation_config.json](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/blob/main/generation_config.json)),
which win over the wrapper's hard defaults unless you pass a value:

| Key | Default | Controls |
|---|---|---|
| `do_sample` | true | talker (codebook 0 — the "what is said and how" stream) |
| `temperature` | 0.9 | talker |
| `top_k` | 50 | talker |
| `top_p` | 1.0 | talker |
| `repetition_penalty` | 1.05 | talker |
| `subtalker_dosample` | true | sub-talker / code predictor (the 15 residual codebooks — timbre detail) |
| `subtalker_temperature` | 0.9 | sub-talker |
| `subtalker_top_k` | 50 | sub-talker |
| `subtalker_top_p` | 1.0 | sub-talker |
| `max_new_tokens` | 8192 | ≈ 655 s of audio at 12.5 frames/s; the team's evals and the HF Space use 2048 (≈ 164 s) |

The two-sampler split is verified in code ([qwen-official.md §2.3](survey/qwen-official.md)):
the paper says "the backbone ingests aggregated codebook features to predict the zeroth codebook,
and an MTP module then generates all residual codebooks", and the tokenizer's "first codebook
layer encodes semantic content, while the subsequent layers capture acoustic details". So
`subtalker_*` is the knob nearest to timbre.

What is documented about changing them: **nothing, for VoiceDesign.** No Qwen statement, no
community measurement. One CustomVoice user: "调整了temperature无效" (temperature had no effect)
on run-to-run timbre ([issue #298](https://github.com/QwenLM/Qwen3-TTS/issues/298)). The C port
defaults `--temperature 0.5`; a DeepWiki summary suggests 0.7-0.8 (secondary, unmeasured).
Greedy: on Parler `do_sample=False` "results in basically noise" ([parler-tts #45](https://github.com/huggingface/parler-tts/issues/45));
on a Qwen Base LoRA fine-tune greedy was deterministic per input yet ~15 % of short lines still
flipped timbre at onset ([issue #343](https://github.com/QwenLM/Qwen3-TTS/issues/343) — a
fine-tune with a suspected training bug, weak evidence). No VoiceDesign report under greedy.

Local single run (`B_seed7_t06_*`, talker `temperature=0.6`): median F0 91 / 66 / 77 Hz, cosine
0.62 / 0.44 / 0.15. Lower pitch and one better line, one worse; n = 3, no conclusion.

**Recommended experiment, not a setting:** A/B `subtalker_temperature` 0.5-0.7 with talker
`temperature` 0.9 on a fixed probe, 8+ draws each, compare the spread of cosine-to-anchor and
median F0. Both `qwen-consistency.md` §2.2 and `qwen-official.md` §2.3 propose it and both say
nobody has measured it. Until measured, run the defaults.

### 5.4 Fewer calls, fewer draws — and an open disagreement about batching

- One long text is one draw. Every long-form complaint in [#220](https://github.com/QwenLM/Qwen3-TTS/discussions/220)
  is about *chunk boundaries* ("the voice changes when you [chunk]"; identity "reasonably
  consistent" inside a chunk, cadence drifting between). `qwen-consistency.md` §3 therefore
  recommends: concatenate a character's lines for a scene into one text, generate once,
  split afterwards. Cost: one bad draw loses the scene, so pair with best-of-N on a short probe.
- `non_streaming_mode=True` (the VoiceDesign default) is the layout that showed flat pacing in
  the one drift measurement ([PR #362](https://github.com/QwenLM/Qwen3-TTS/pull/362), 0.0 % vs
  +16.7 % streaming) — measured on Base clone with a reference clip, so the transfer to
  VoiceDesign is inference. Keep the default.
- **Batching (lists of texts in one call).** Code reading: each item is an independent
  left-padded row; rows do not attend to each other; "Batch = N separate draws that happen to
  run in parallel" ([qwen-consistency.md §3](survey/qwen-consistency.md), modeling l.2236-2254).
  Local measurement in `qwen_worker.py`'s docstring: "three lines batched scored 0.56
  speaker-similarity to each other against 0.37 for the same lines generated separately", and
  in `scores.json` the batched rows score 0.45 / 0.54 / 0.55 to the anchor against 0.48 / 0.22
  / 0.19 for separate calls. **These disagree.** The code says it should not help; one local
  trial says it did. Possible confound: with a fixed seed the batch shares one RNG stream and the
  separate calls each restart it, and the local n is three. The pipeline currently relies on the
  batch behaviour. It needs a proper test (≥ 8 batches vs ≥ 8 separate sets, same seeds) before
  it is treated as a mechanism; until then the whole-scene-in-one-text approach is the one the
  code reading supports.
- Very short standalone lines are where wrong-timbre onsets concentrate in the fine-tune and
  clone regimes ([#343](https://github.com/QwenLM/Qwen3-TTS/issues/343), [SwiftVoxAlta #12](https://github.com/intrusive-memory/SwiftVoxAlta/issues/12));
  nobody reports it for VoiceDesign. Local hint: the two ~8 s lines scored far below the ~16 s
  line. Cheap precaution: merge short cues into a neighbour or into the scene text. A throwaway
  lead-in that is trimmed afterwards is untested ("leading padding made it worse" in the
  fine-tune thread) — if used, use the *same* lead-in on every take so the anchor comparison is
  on equal phonemes.
- Cap per-call length at a few minutes even though 8192 frames allows ~11: long single
  generations are where cadence drift and truncation are reported (§6).

### 5.5 Best-of-N against an anchor

The only pure-design mechanism anyone documents that plausibly converges on a voice, and what
Qwen's hosted product tells its users to do by ear: "Voice Design involves randomness, so the
same description may produce slightly different voices each time. Generate multiple voices,
listen to them, and select the best one" ([DashScope](https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-design)).
Tortoise shipped the automated form in 2022 (`num_autoregressive_samples` re-ranked by a
voice-similarity model, [api.py](https://github.com/neonbjb/tortoise-tts/blob/main/tortoise/api.py)).
The worker already implements it: ECAPA-TDNN cosine to the approved anchor, `tries` batches,
keep the best mean, stop early at `good_enough`.

Protocol (assembled in `qwen-consistency.md` §4.3; effect sizes are the cited ones):

1. **Anchor.** 8-16 takes of a 15-25 s probe paragraph per character with the frozen brief;
   pick by ear; keep the WAV; compute its ECAPA embedding, median F0 and speech rate. Also
   compute the cosine between the *rejected* anchor candidates and the winner — that
   intra-anchor distribution is your "same voice on this model" calibration.
2. **Per line or per scene:** N candidates, vary only the seed. Start N = 4.
3. **Score** = cosine(ECAPA, anchor), tie-break by |Δ median F0| and |Δ speech rate|. Reject
   below a line you set from step 1, not from the literature: SpeakerSleuth uses τ = 0.4 on a
   192-d SpeechBrain ECAPA over human dialogue ([arXiv 2601.04029](https://arxiv.org/pdf/2601.04029));
   Baseten sees ~0.7 pairwise / 0.85+ to centroid on Qwen's own 2048-d encoder
   ([Baseten](https://www.baseten.co/blog/fine-tuning-qwen3-tts-for-high-quality-voice-cloning/));
   the worker's comment says "~0.6+ same person, <0.3 stranger". Numbers do not transfer
   between encoders.
4. **Escalate** N (8, 16) only for lines that fail; log the passing seed.
5. Expect the *spread* to collapse and the mean to move little; the win is removing the 145 Hz
   outliers, not moving the centre (reasoning, no source measures it on a description model).

What the embedding does not see: "speaker embeddings primarily encode static spectral
information (mean pitch, HNR, shimmer, α-ratio)" and "fail to capture dynamic behavioral identity
markers like speech rate, voiced/unvoiced segment durations, variations in pitch, and loudness"
([Carbonneau et al.](https://arxiv.org/html/2507.02176v1)). So cosine will converge timbre and
pitch range but not the cadence drift storm-fox describes — hence the F0/rate tie-break.
Benchmark accuracies (97.8-100 % in SpeakerSleuth) are against an opposite-gender decoy and an
ECAPA-nearest other human; accuracy on ranking same-description draws is **unmeasured**.

Two exemptions: whisper lines (no voicing → the embedding has little to hold; do not reject on
cosine alone), and laugh-led lines (the bark is not speech; score the part after it, or accept
a lower number).

### 5.6 Post-hoc touch-up

`voice_shape.py` already applies `pitch_st`, `formant`, `speed`, `range_factor` via Praat.
Matching median F0 to the anchor will raise measured similarity because the embeddings weight
mean pitch heavily. Limits: no source gives a naturalness-vs-semitones curve for codec-LM TTS;
general practice is ±2-3 st. A 5.6 st gap (105 vs 145 Hz) is a take to reject in §5.5, not to
shift. Formant-shifting to fake a giant's body is uncharted for this codec — unknown.

### 5.7 Untested hypothesis, flagged as such

In `non_streaming_mode=False` the talker is prefilled with only the first text token and the
rest arrives one token per frame; a fixed opening sentence plus a fixed seed would then compute
its first ~1 s from bit-identical inputs — a self-generated prompt to cut off afterwards.
Derived from code by `qwen-consistency.md` §2.3; nobody has tried it; streaming mode carries
the rate-drift bug; bf16 near-ties may diverge anyway. One afternoon's experiment, not a
recommendation.

### 5.8 What no amount of the above delivers

A reusable identity object. Every engine that solved consistency captured a latent (ChatTTS
`spk_emb`, Tortoise conditioning latents, Parler's 34 named training speakers, Qwen
`create_voice_clone_prompt`, DashScope's stored `voice` id). Qwen's answer for identity plus
per-line instruct is the unreleased 25Hz VoiceEditing model ("will support both cloning and
instruct", wangxiongts, [issue #25](https://github.com/QwenLM/Qwen3-TTS/issues/25)), not on HF
as of 12 Sep 2026 ([issue #294](https://github.com/QwenLM/Qwen3-TTS/issues/294) open).

---

## 6. Known failure modes and fixes

| Failure | Reported where | Fix / mitigation | Confidence |
|---|---|---|---|
| Different voice every run | structural (§0); [#4](https://github.com/QwenLM/Qwen3-TTS/issues/4), [#13](https://github.com/QwenLM/Qwen3-TTS/issues/13), [Rapid-MLX #1338](https://github.com/raullenchai/Rapid-MLX/issues/1338) | §5: frozen brief, one call per scene, best-of-N to anchor | mechanism verified; selection accuracy unmeasured |
| Chinese / Asian-accented English | ocdevel (quoting mybyways, probably CustomVoice presets); Habr; [discussion #315](https://github.com/QwenLM/Qwen3-TTS/discussions/315) (Spanish VD: "very sensitive to the exact wording") | `language="English"` (never Auto); `accent: General American English` filled in every brief; write the instruct in English. No wording is documented to remove the accent reliably | partial |
| Mumbling / slurred words | not reported for VoiceDesign in any survey; "Mumble"/"Slurred" exist as tags in CapSpeech/ParaSpeechCaps, so the model class knows the concept | `clarity: Highly articulate and distinct pronunciation.` `fluency: Very fluent, no hesitations.`; avoid "breathy", "soft" and "slow" stacked together (the quiet-and-slow corner is under-represented — APS "soft" 2 / "quiet" 4); re-draw | reasoning only |
| Last one or two words truncated | [HF discussion #4](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/discussions/4) (unanswered); [mlx-audio #882](https://github.com/Blaizzy/mlx-audio/issues/882) | terminal punctuation; longer text ("seed-dependent … Use longer input text" — Dawizzer); add a short trailing sentence and trim it; re-draw. mlx-audio: even `max_tokens=8192` did not fix it | partial |
| Repeats, loops, very long output | ocdevel | cap `max_new_tokens` (2048 for a line batch); keep `repetition_penalty` 1.05; retry seed | anecdotal |
| Garbage / overlapping voices | [#78](https://github.com/QwenLM/Qwen3-TTS/issues/78) (Windows, unresolved) | different seed ("some seeds may produce more stable results" — DarioFT node docs) | anecdotal |
| Speech accelerates over long text | [#239](https://github.com/QwenLM/Qwen3-TTS/issues/239), [#290](https://github.com/QwenLM/Qwen3-TTS/issues/290), [mlx-audio #910](https://github.com/Blaizzy/mlx-audio/issues/910) | Base/clone streaming layout; VoiceDesign defaults to non-streaming; keep calls to a few minutes; `speed:` post-processing corrects small drift | not reported for VD |
| Delivery / cadence drifts between chunks with identity held | [#220](https://github.com/QwenLM/Qwen3-TTS/discussions/220) (storm-fox, both CustomVoice and VD) | no in-model fix; fewer chunks; F0/rate tie-break in selection; `range_factor` post-processing | reported, no fix |
| Wrong timbre / gender flip in the first 1-2 s of a short line | [#343](https://github.com/QwenLM/Qwen3-TTS/issues/343) (Base LoRA fine-tune, suspected training bug); SwiftVoxAlta #12 (clone) | merge short lines into the scene text; same-lead-in trick (untested) | not reported for VD |
| Laughter, "OK", extra words not in the text | [#16](https://github.com/QwenLM/Qwen3-TTS/issues/16) (CustomVoice) | negation in `tone:` ("without laughing"); tone down emotion words; re-draw | staff "may be able to"; unconfirmed |
| The laugh does not come, or comes wrong | [#9](https://github.com/QwenLM/Qwen3-TTS/issues/9) (staff: implicit only, "a certain degree of randomness"); InstructTTSEval (only two closed models laugh reliably) | write it in the text (`HOO.` / `Hah.`) and describe it in `tone:`; give the laugh its own sentence; budget extra draws; if it never lands, render the bark as a separate one-word call and splice | expect randomness |
| Sighs | InstructTTSEval: "NO existing models successfully 'sigh'" | `Haah...` in text; accept failure; splice a Chatterbox sigh if the pipeline has one | expect failure |
| Throat-strain words raise the pitch | local, Isaac 12 Sep 2026 (`Darius.json` `qwen_note`) | never use "tight", "hoarse", "strained", "tense" for a low voice; carry edge as manner ("clipped", "cold") | one session |
| "deep" + "old" cancel | Castwright [#830](https://github.com/dudarenok-maker/Castwright/issues/830); ageing acoustics ([JSLHR 2020](https://pubs.asha.org/doi/10.1044/2019_JSLHR-19-00099)) | decide which wins per character (§3 decisions); never write tremor/thin on a bass brief | one developer + physiology |
| Numbers, dates misread | Habr; [#265](https://github.com/QwenLM/Qwen3-TTS/issues/265) (cloud) | spell out in the text; no normaliser exists in the processor | verified (no normaliser) |
| 0.6B model ignores instruct | code: `if tts_model_size in "0b6": instruct = None` | 1.7B only | verified |

---

## 7. Sources

Survey reports (this folder): [qwen-official.md](survey/qwen-official.md) ·
[qwen-community.md](survey/qwen-community.md) · [qwen-science.md](survey/qwen-science.md) ·
[qwen-consistency.md](survey/qwen-consistency.md). Local data: `build/voices/bakeoff/qwen3-consistency/scores.json`
(columns as written by the bakeoff script: name, [unlabelled], cosine to anchor, median F0 Hz,
[unlabelled]; the anchor row is 1.0 / 105.3 Hz), `build/qwen_worker.py` docstring,
`build/casting/Darius.json` and `Gimbzo.json` `qwen_note`.

Qwen official
- Model card: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign (VoiceDesign-blind: its only code is a CustomVoice call)
- generation_config.json: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/blob/main/generation_config.json
- GitHub README: https://github.com/QwenLM/Qwen3-TTS · voice-design example: https://github.com/QwenLM/Qwen3-TTS/blob/main/examples/test_model_12hz_voice_design.py · finetuning: https://github.com/QwenLM/Qwen3-TTS/blob/main/finetuning/README.md
- Inference wrapper: https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/inference/qwen3_tts_model.py · modeling: https://github.com/QwenLM/Qwen3-TTS/blob/main/qwen_tts/core/models/modeling_qwen3_tts.py
- Technical report: https://arxiv.org/html/2601.15621
- Release blog (open checkpoint, 22 Jan 2026): https://qwen.ai/blog?id=qwen3tts-0115 · hosted VD-Flash blog (23 Dec 2025, API model — same family, not the open weights): https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign
- DashScope voice-design doc (hosted): https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-design
- HF Space app.py: https://huggingface.co/spaces/Qwen/Qwen3-TTS/blob/main/app.py · Voice-Design Space (calls the cloud API, not the open weights): https://huggingface.co/spaces/Qwen/Qwen3-TTS-Voice-Design/blob/main/app.py
- Issues/discussions: #4 https://github.com/QwenLM/Qwen3-TTS/issues/4 · #9 https://github.com/QwenLM/Qwen3-TTS/issues/9 · #13 https://github.com/QwenLM/Qwen3-TTS/issues/13 · #16 https://github.com/QwenLM/Qwen3-TTS/issues/16 · #23 https://github.com/QwenLM/Qwen3-TTS/issues/23 · #25 https://github.com/QwenLM/Qwen3-TTS/issues/25 · #78 https://github.com/QwenLM/Qwen3-TTS/issues/78 · #239 https://github.com/QwenLM/Qwen3-TTS/issues/239 · #248 https://github.com/QwenLM/Qwen3-TTS/issues/248 · #265 https://github.com/QwenLM/Qwen3-TTS/issues/265 · #290 https://github.com/QwenLM/Qwen3-TTS/issues/290 · #294 https://github.com/QwenLM/Qwen3-TTS/issues/294 · #298 https://github.com/QwenLM/Qwen3-TTS/issues/298 · #343 https://github.com/QwenLM/Qwen3-TTS/issues/343 · PR #362 https://github.com/QwenLM/Qwen3-TTS/pull/362 · discussion #220 https://github.com/QwenLM/Qwen3-TTS/discussions/220 · #315 https://github.com/QwenLM/Qwen3-TTS/discussions/315 · HF discussion #3 https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/discussions/3 · HF discussion #4 https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/discussions/4

Benchmarks and caption pipelines
- InstructTTSEval: https://arxiv.org/abs/2506.16381 · https://arxiv.org/html/2506.16381v1 · dataset https://huggingface.co/datasets/CaasiHUANG/InstructTTSEval
- DataSpeech / Parler-TTS: https://github.com/huggingface/dataspeech · bin words https://raw.githubusercontent.com/huggingface/dataspeech/main/scripts/metadata_to_text.py · Hz edges https://raw.githubusercontent.com/huggingface/dataspeech/main/examples/tags_to_annotations/v02_bin_edges.json · paper https://arxiv.org/html/2402.01912 · model card https://huggingface.co/parler-tts/parler-tts-mini-v1 · INFERENCE.md https://github.com/huggingface/parler-tts/blob/main/INFERENCE.md · issues #11 https://github.com/huggingface/parler-tts/issues/11 · #45 https://github.com/huggingface/parler-tts/issues/45 · PR #110 https://github.com/huggingface/parler-tts/pull/110
- CapSpeech: https://arxiv.org/html/2506.02863 · https://huggingface.co/datasets/OpenSound/CapSpeech
- ParaSpeechCaps: https://arxiv.org/html/2503.04713
- PromptTTS 2: https://arxiv.org/abs/2309.02285v2 · VoiceSculptor: https://arxiv.org/html/2601.10629 · OV-InstructTTS: https://arxiv.org/abs/2601.01459 · cross-attention attribution (CapSpeech, diffusion — does not transfer): https://arxiv.org/html/2606.20532v1

Consistency and selection
- SpeakerSleuth: https://arxiv.org/pdf/2601.04029 · Best-of-N with ASR verifier: https://arxiv.org/html/2607.08256v1 · speaker-embedding analysis (Carbonneau et al.): https://arxiv.org/html/2507.02176v1 · Deep Dubbing (text-to-timbre architecture): https://arxiv.org/html/2509.15845v1
- Tortoise api.py: https://github.com/neonbjb/tortoise-tts/blob/main/tortoise/api.py · ChatTTS: https://github.com/2noise/ChatTTS · MOSS-VoiceGenerator doc (measured F0 under seeds): https://github.com/0xShug0/audio.cpp/blob/main/docs/community_models/moss_voicegen.md · VoxCPM README: https://github.com/OpenBMB/VoxCPM/blob/main/README.md
- PyTorch reproducibility: https://docs.pytorch.org/docs/2.13/notes/randomness.html · Baseten Qwen3-TTS fine-tune (cosine figures): https://www.baseten.co/blog/fine-tuning-qwen3-tts-for-high-quality-voice-cloning/

Acoustics
- Body size from F0 + formants, Pisanski et al. 2016: https://pmc.ncbi.nlm.nih.gov/articles/PMC5043380/ · GRBAS vs jitter/shimmer/NHR: https://pmc.ncbi.nlm.nih.gov/articles/PMC8419204/ · ageing meta-analysis, JSLHR 2020: https://pubs.asha.org/doi/10.1044/2019_JSLHR-19-00099 (PubMed PMID 32083980) · phonation types, Esposito & Khan 2020: https://www.reed.edu/linguistics/khan/assets/Esposito%20Khan%202020%20The%20cross-linguistic%20patterns%20of%20phonation%20types.pdf · Laver settings: https://www.ims.uni-stuttgart.de/phonetik/EGG/page10.htm · F0 norms: https://www.voicescience.org/lexicon/average-speaking-frequencies/

Community tools and guides
- alexandria-audiobook: https://github.com/Finrandojin/alexandria-audiobook · Castwright #830: https://github.com/dudarenok-maker/Castwright/issues/830 · docs/features/160: https://github.com/dudarenok-maker/Castwright/blob/main/docs/features/160-voicedesign-persona-format.md · skills/audiobook-voice-style.md: https://github.com/dudarenok-maker/Castwright/blob/main/skills/audiobook-voice-style.md · TTS-Audio-Suite: https://github.com/diodiogod/TTS-Audio-Suite · DarioFT ComfyUI node: https://www.runcomfy.com/comfyui-nodes/ComfyUI-Qwen3-TTS/qwen3-voice-design · Voice-Clone-Studio prompt_hub: https://github.com/FranckyB/Voice-Clone-Studio/blob/main/modules/core_components/prompt_hub.py · C port: https://github.com/gabriele-mastrapasqua/qwen3-tts · koboldcpp #2192: https://github.com/LostRuins/koboldcpp/discussions/2192 · SwiftVoxAlta #12: https://github.com/intrusive-memory/SwiftVoxAlta/issues/12 · mlx-audio #882 https://github.com/Blaizzy/mlx-audio/issues/882 · #910 https://github.com/Blaizzy/mlx-audio/issues/910 · Rapid-MLX #1338: https://github.com/raullenchai/Rapid-MLX/issues/1338 · UChi-JCL #1: https://github.com/UChi-JCL/Multi-Modal-Semantic-Routing-for-vLLM/issues/1
- getstream guide (open checkpoint, 17 Apr 2026): https://getstream.io/blog/qwen3-voice-design/ · ocdevel (2 Mar 2026): https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning · dev.to seed article (27 Apr 2026, checkpoint unnamed): https://dev.to/lcmd007/from-stochastic-drifting-to-vector-anchors-how-i-solved-voice-consistency-in-qwen-tts-4dff

Gaps carried over from the surveys: Reddit and YouTube were unreachable; no controlled test of
description length, word order, `subtalker_temperature`, accent wording, or per-line-direction
identity cost exists for VoiceDesign; nothing ROCm-specific is published. The 105 vs 145 Hz
observation and `scores.json` are the only VoiceDesign measurements in hand.
