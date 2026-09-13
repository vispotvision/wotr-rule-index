# What description-driven TTS can and cannot take from text

Survey of the science behind Qwen3-TTS-12Hz-1.7B-VoiceDesign's model class — the training-caption vocabularies such models have literally seen, the benchmark Qwen was scored on, what the inference code actually does with the `instruct`, and the acoustic measurements that voice-director words map to.

Written 12 Sep 2026. Everything quoted was pulled from the primary source that day; where a claim is inference rather than quotation it is marked **[inference]**. Where nobody has published the answer it says **unknown**.

**Skeptic pass, same day.** Every cited source was re-opened and each quote checked. Marks in the text: **[verified]**, **[corrected: …]**, **[unsupported — removed]**, **[added]**; struck text is ~~struck~~. Three "quotations" turned out not to be in their sources, one provenance error (the Qwen blog is about the API model) and one misread finding ("orthogonal capabilities") were the material problems. Full accounting in the **Verification** section at the end.

---

## 0. The three problems, answered up front

| Problem | Short answer | Where the evidence is |
|---|---|---|
| (1) Same brief, different voice every run (105 Hz one take, 145 Hz the next) | This is the *one-to-many problem* that the field named in 2023 and has not solved for description-only models. In VoiceDesign there is **no speaker embedding at all** — the code path is literally commented `# Instruct create speaker` and sets `speaker_embed = None` **[verified]**; sampling runs at `temperature=0.9, top_k=50` on both the main talker and the residual-codebook sub-talker **[verified]**. No `seed` argument exists in the API **[verified]**. That identity is therefore "re-sampled from scratch on every call" is **[inference]** from those code facts, and two community threads complicate it: with a pinned `torch` seed users report identity "reasonably consistent" while *prosody* drifts (#220), and "the fixed seed voice will 'behave' the same" though not byte-identical (#298) — see §3.5. Under the Parler training-caption bins, 105 Hz and 145 Hz for a male voice fall in different word bins ("slightly low pitch" vs "slightly high pitch") **[verified]**, so a brief that says only "deep" is not pinning anything. The official README's documented fix is "Voice Design then Clone" **[verified]**. | §3, §4, §6.1 |
| (2) Per-line delivery direction without the voice changing | The research literature separates *intrinsic* (speaker-level: pitch, texture, age, accent) from *situational* (utterance-level: emotion, speed, volume, whisper, laugh) attributes. InstructTTSEval's line "timbre flexibility and emotional expressiveness remain orthogonal capabilities" **[corrected: this is a remark about the 2025 model landscape — closed models had fixed voices with good emotional control, open models could vary timbre but had weak emotional control — not an acoustic finding that the two are separable inside one model]**. The *mechanism* that keeps intrinsic fixed while situational varies is always a speaker anchor (preset speaker id, clone prompt, or fine-tune). Qwen measured exactly this as "Target Speaker (Editing)" on CustomVoice — not on VoiceDesign **[verified]**. In pure VoiceDesign the only lever is the text, and a text-only lever cannot hold identity constant. | §2.4, §3.3, §6.2 |
| (3) Words that reliably produce rasp, extreme depth, age, neutral accent | There *is* a trained vocabulary and it is small and specific: "very low-pitch / low-pitch", "deep", "resonant", "gravelly", "raspy", "husky", "hoarse", "guttural", "booming", "elderly", "General American English". Extremes are rare in captions (CapSpeech: "very low-pitch" 3.22 %, "elderly" 3.49 %, "very slowly" 0.01 %) **[verified]**. Numbers ("90 Hz"), film characters ("Kratos") and physical descriptions ("eight-foot giant") appear in **no** reviewed caption pipeline **[verified for the four pipelines reviewed]**; Qwen's own caption data is undisclosed **[verified — the tech report never uses the word "caption"]**. **[added]** But Qwen's own VD-Flash blog does showcase a full Chinese *character card* as an instruct — name, backstory, **physical appearance** ("身形挺拔，两鬓斑白"), personality, creed — so a card-shaped brief is demonstrably in-distribution for the API model at least (§3.2). | §5, §7 |

---

## 1. InstructTTSEval — the benchmark Qwen3-TTS-VD was scored on

Paper: [InstructTTSEval: Benchmarking Complex Natural-Language Instruction Following in Text-to-Speech Systems](https://arxiv.org/abs/2506.16381) (Huang et al., Fudan, June 2025). HTML: <https://arxiv.org/html/2506.16381v1>. Dataset: <https://huggingface.co/datasets/CaasiHUANG/InstructTTSEval>.

### 1.1 The three levels

> "We introduce three tasks, namely Acoustic-Parameter Specification, Descriptive-Style Directive, and Role-Play, including English and Chinese subsets, each with 1k test cases (6k in total) paired with reference audio."

- **APS** (Acoustic-Parameter Specification): a structured 12-field caption, one field per attribute. Written by Gemini from a real audio clip: "We leverage the strong spoken language understanding (SLU) capabilities of Gemini to generate a natural language description for each reference audio sample... This caption also serves as the instruction for the APS task."
- **DSD** (Descriptive-Style Directive): "the structured instructions from APS are rewritten by an LLM into free-form descriptions. We further introduce diversity by randomly omitting some attributes in the prompt."
- **RP** (Role-Play): "the prompts describe roles or scenarios (e.g., a teacher scolding a student, a nervous applicant in an interview). The model is expected to infer the corresponding vocal style based on world knowledge".

### 1.2 The 12-attribute taxonomy (four tiers)

> "we integrate 12 features across four tiers: physiological (e.g., gender, pitch, texture), linguistic (e.g., clarity, fluency, speed), social (e.g., accent, age, volume), and psychological or pragmatic (e.g., emotion, tone, personality)"

The APS field order in the released data is: `gender, pitch, speed, volume, age, clarity, fluency, accent, texture, emotion, tone, personality`. A verbatim row (`en_3`) from the HF dataset:

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

**This exact schema shows up in Qwen's own published sample instructs** (see §3.2). That is the strongest available evidence for what the VoiceDesign model was trained to read.

### 1.3 Vocabulary actually used in the 1,000 English APS captions

I downloaded all 1,000 English rows and counted words per field. Top content words (count out of 1,000 captions). **[verified 12 Sep 2026 by re-downloading the `en` split via the HF datasets-server and recounting; the researcher's figures are substring counts, so a few are inflated — e.g. "adult 1237" counts "adults"/"adulthood", "low 303" counts "lower"/"lowering"/"slowing". Word-boundary counts: american 794, general american 191, standard american 244, low (pitch) 213, deep (pitch) 47, deep (texture) 48, gravelly 187, raspy 33, husky 10, hoarse 1, booming 5, elderly 38, child 18. Same picture.]**

| Field | Words the benchmark uses (count) |
|---|---|
| **texture** | bright 467, strained 289, resonant 230, sharp 197, **gravelly 187**, clear 161, tense 91, energetic 76, forceful 66, **deep 48**, nasal 40, **rough 39**, firm 34, **raspy 33**, thin 29, warm 25, crisp 15, reedy 14, harsh 12, **breathy 11**, **husky 10**, smooth 9, **coarse 9**, shrill 8, strident 8, **booming** (3 rows) |
| **pitch** | rising 394, high 353, inflections 215, low 184, upward 181, high-pitched 156, mid-range 136, stable 83, strained 76, elevated 69, **deep 47**, lowering 44, resonant 34 |
| **age** | adult 1237, middle-aged 811, young 578, older 96, **elderly 38**, **child 18**, teenager 16, mature 9, adolescent 3, pre-teen 2, senior 1 |
| **accent** | english 1000, american 804, standard 272, general 192, british 162, received 30, southern 24, cockney 17, estuary 11, aave 6, scottish 4 |
| **volume** | loud 538, conversational 492, forceful 221, shouting 136, projecting 106, elevated 93, softening 21 |
| **speed** | rapid 463, deliberate 209, energetic 179, fast-paced 115, brisk 114, measured 96, slowing 85, urgent 63, rushed 62, slow 57, hurried 33 |
| **clarity** | clear 669, articulation 626, distinct 392, precise 142, crisp 23, blurred 27, clipped 8 |

Verbatim texture strings containing the rough/deep vocabulary:

- `en_423`: "Deep, gravelly, and somewhat hoarse."
- `en_378`: "Deep, booming, resonant, slightly gravelly.."
- `en_562`: "Gravelly and booming vocal texture."
- `en_34`: "Gravelly and rough vocal texture." (pitch field: "Low and deep male pitch.")
- `en_54`: "Gravelly and slightly husky."
- `en_14`: "Firm, somewhat deep, and slightly gravelly texture."
- `en_77`: "Gravelly and coarse, becoming more strained and forceful in moments of assertion."
- `en_9`: "Husky, rich, and soulful vocal texture."
- `en_207` age: "Older adult / Elderly."; `en_18` age: "Middle-aged to elderly, exhibiting a mature vocal quality.."

Only **1** of 1,000 pitch fields (`en_657`) contains "very low" or "very deep" **[verified]**; 47 contain the word "deep", 213 the word "low" **[corrected from 50 / 303 — substring vs word-boundary]**. Extreme depth is under-represented even in the benchmark.

**[added]** Two further counts that matter for casting: the `volume` field is almost never quiet — "loud" 533, "shouting" 151, "conversational" 487 versus "soft" 2, "quiet" 4, "whisper" 1 — so the benchmark barely tests hushed delivery at all; and "neutral" never appears in an `accent` field (it appears 17 times, always as an emotion/tone word).

### 1.4 What the benchmark found models fail at

> "Modern TTS models still struggle to reproduce the paralinguistic sound events that frequently occur in human speech, such as sighs, sudden bursts of laughter, screams, etc."

Case table (Table 7): "NO existing models successfully 'sigh'"; "gemini-flash, gemini-pro and gpt-4o-mini-tts successfully laugh out"; "NO models scream"; "VoxInstruct and Parler-TTS-large generate child-like voices"; "Parler-TTS-large generates a trembling voice of an elderly".

> "This suggests that timbre flexibility and emotional expressiveness remain orthogonal capabilities, and that future TTS research should aim to unify them rather than treat them separately."

**[verified, with context restored]** The sentence immediately before it is "And Parler-TTS-Large successfully synthesizes the voice of the elderly." The paragraph contrasts closed systems (fixed voices, better emotional control) with open ones (flexible timbre, weaker emotional control). "Orthogonal" here describes the *model landscape*, not an acoustic property of speech; it should not be read as evidence that one model can hold timbre fixed while varying emotion.

> "Notably, DSD and RP instructions are generated without feeding in the reference audio, so they may deviate from the original audio. Furthermore, because RP prompts are inherently more subjective, human–Gemini agreement tends to decline."

**[inference]** RP is the level where a brief like "eight-foot ancient giant" lives; it is the level every model scores lowest on (Qwen3-TTS-VD: 68.4 EN vs 82.9 APS — §3.1). **[corrected: the scores are Gemini-as-judge, and the benchmark's own `reference_audio` row — the real human recordings scored by the same judge — gets APS 96.2 / DSD 89.4 / RP 67.2 on EN. So RP has a low ceiling by construction, and Qwen3-TTS-VD's 68.4 RP is at (slightly above) the human-audio reference. "Weakest level" is true of the number, not necessarily of the model's role-play ability.]**

### 1.5 Scores of the systems it evaluated (English)

| System | APS | DSD | RP |
|---|---|---|---|
| Gemini-flash | 92.3 | 93.8 | 80.1 |
| GPT-4o-mini-tts | 76.4 | 74.3 | 54.8 |
| Hume | 83.0 | 75.3 | 54.3 |
| VoxInstruct | 54.9 | 57.0 | 39.3 |
| Parler-TTS-mini | 63.4 | 48.7 | 28.6 |

---

## 2. The caption pipelines — the words these models were literally trained on

### 2.1 Parler-TTS / DataSpeech (Lyth & King 2024; Hugging Face)

Paper: [Natural language guidance of high-fidelity text-to-speech with synthetic annotations](https://arxiv.org/html/2402.01912). Code: <https://github.com/huggingface/dataspeech>. Model card: <https://huggingface.co/parler-tts/parler-tts-mini-v1>.

**How each attribute is measured** (paper §3.1):

> "We compute pitch contours for all utterances using the PENN library ... and then calculate the speaker-level mean and utterance-level standard deviation. The speaker-level mean is used to generate a label for speaker pitch relative to gender, and the standard deviation is used as a proxy for how monotone or animated an individual utterance is."

> "The two proxies we use for labeling recording quality are the estimated signal-to-noise ratio (SNR) and estimated C50. C50 is the ratio of early reflections to late reflections and indicates how reverberant a recording is. For both of these features, we use the Brouhaha library"

> "For each variable, we apply seven bins and then use appropriate short phrases to describe each bin."

**The exact bin words** (from [`scripts/metadata_to_text.py`](https://raw.githubusercontent.com/huggingface/dataspeech/main/scripts/metadata_to_text.py)):

```python
SPEAKER_RATE_BINS = ["very slowly", "quite slowly", "slightly slowly", "moderate speed", "slightly fast", "quite fast", "very fast"]
SNR_BINS = ["very noisy", "quite noisy", "slightly noisy", "moderate ambient sound", "slightly clear", "quite clear", "very clear"]
REVERBERATION_BINS = ["very roomy sounding", "quite roomy sounding", "slightly roomy sounding", "moderate reverberation", "slightly confined sounding", "quite confined sounding", "very confined sounding"]
UTTERANCE_LEVEL_STD = ["very monotone", "quite monotone", "slightly monotone", "moderate intonation", "slightly expressive", "quite expressive", "very expressive"]
SI_SDR_BINS = ["extremely noisy", "very noisy", "noisy", "slightly noisy", "almost no noise", "very clear"]
PESQ_BINS = ["very bad speech quality", "bad speech quality", "slightly bad speech quality", "moderate speech quality", "great speech quality", "wonderful speech quality"]
SPEAKER_LEVEL_PITCH_BINS = ["very low pitch", "quite low pitch", "slightly low pitch", "moderate pitch", "slightly high pitch", "quite high pitch", "very high pitch"]
```

**The bin edges in Hz** — [`examples/tags_to_annotations/v02_bin_edges.json`](https://raw.githubusercontent.com/huggingface/dataspeech/main/examples/tags_to_annotations/v02_bin_edges.json). Male speaker-level mean f0:

| Male mean f0 (Hz) | Caption word |
|---|---|
| 64.7 – 81.7 | very low pitch |
| 81.7 – 98.7 | quite low pitch |
| 98.7 – 115.7 | slightly low pitch |
| 115.7 – 132.7 | moderate pitch |
| 132.7 – 149.7 | slightly high pitch |
| 149.7 – 166.7 | quite high pitch |
| 166.7 – 183.7 | very high pitch |

Female bins run 120.2 → 270.3 Hz in seven equal steps of ≈21.4 Hz. Speaking-rate bins are in phonemes/second: 0–3.8, 3.8–7.7, 7.7–11.5, 11.5–15.3, 15.3–19.1, 19.1–23.0, 23.0–26.8. Monotony bins (utterance f0 std, Hz): 0–20.4, 20.4–40.8, 40.8–70, 70–90, 90–142.7.

**Direct read on Isaac's numbers:** a 105 Hz take is "slightly low pitch"; a 145 Hz take is "slightly high pitch". Gimbzo as briefed ("extremely deep") should be "very low pitch" = **below 82 Hz**, and "quite low pitch" = 82–99 Hz. **[inference]** If Isaac's takes are landing at 105–145 Hz, the description is not being read as an extreme-depth instruction, or the model's own training bins are wider than Parler's. Qwen's bins are undisclosed.

**The prompt that turned bins into captions** (from [`scripts/run_prompt_creation.py`](https://raw.githubusercontent.com/huggingface/dataspeech/main/scripts/run_prompt_creation.py), `NEW_PROMPT`):

> "1. The gender (male, female)
> 2. The level of reverberation (very distant-sounding, distant-sounding, slightly distant-sounding, slightly close-sounding, very close-sounding)
> 3. The amount of noise in the sample (extremely noisy, very noisy, noisy, slightly noisy, almost no noise, very clear)
> 4. The tone of the speaker's voice (very monotone, monotone, slightly expressive and animated, expressive and animated, very expressive and animated)
> 5. The pace of the speaker's delivery (very slowly, slowly, slightly slowly, moderate speed, slightly fast, fast, very fast)
> 6. The pitch of the speaker's voice (very low-pitch, low-pitch, slightly low-pitch, moderate pitch, slightly high-pitch, high-pitch, very high-pitch)
> ... You can randomly omit the following terms, as they are default terms: 'moderate speed' and 'moderate pitch'. Do not add extra details beyond what has been provided above. You can change the order of keywords, and replace synonymous terms."

Worked example: keywords `'female', 'slightly roomy sounding', 'slightly noisy', 'very expressive', 'slightly low pitch', 'very slowly'` → "a woman with a deep voice speaks slowly but has an animated delivery in an echoey room with some background noise". ~~Note: **"deep" is the LLM's synonym for "slightly low pitch"**, i.e. in Parler-style data "deep" was attached to voices only one bin below median.~~ **[corrected: this worked example lives in the legacy `PROMPT` string (line 320–330 of `run_prompt_creation.py`), not in `NEW_PROMPT`. The script selects `NEW_PROMPT` / `NEW_PROMPT_WITH_ACCENT` (lines 562–564), whose worked examples are "A woman speaks very slowly but has a very animated delivery…" and contain no "deep". The LLM was told it may "replace synonymous terms", so "deep" could still have been emitted for any low bin, but there is no evidence it was tied specifically to "slightly low pitch". Claim withdrawn.]**

Model-card guidance: "Include the term 'very clear audio' to generate the highest quality audio, and 'very noisy audio' for high levels of background noise." Controllable set: "gender, background noise, speaking rate, pitch and reverberation." Parler has **no** timbre/texture, age, or emotion vocabulary at all.

Paper's own limitation: "for every attribute other than C50, the model performs fairly well ... We are unsure as to why the model performs poorly at generating audio with the appropriate C50". Accent accuracy only 68 %: "likely to be due to noisy labeling and a very imbalanced distribution of accents in the training set."

### 2.2 CapSpeech (Wang et al., June 2025) — 10 M machine captions

Paper: [CapSpeech: Enabling Downstream Applications in Style-Captioned Text-to-Speech](https://arxiv.org/html/2506.02863). Dataset: <https://huggingface.co/datasets/OpenSound/CapSpeech>.

Attribute set: "intrinsic speaker traits: age (I1), gender (I2), timbre (I3), mean pitch (I4), and accent (I5). E1–E4 represent expressive style traits: speaking rate (E1), emotion (E2), expressiveness of tone (E3), and volume (E4)."

**How rare the extremes are in a 10-million-caption corpus** (paper §III-B):

> "the age category includes "child" (0.15%), "teenager" (0.20%), "young adult" (32.72%), "middle-aged adult" (63.44%), and "elderly" (3.49%); the gender category includes "male" (57.48%) and "female" (42.52%); the pitch category includes "very low-pitch" (3.22%), "low-pitch" (7.19%), "slightly low-pitch" (26.26%), "moderate pitch" (28.05%), "slightly high-pitch" (21.34%), "high-pitch" (12.45%) and "very high-pitch" (1.49%); the expressiveness of tone category includes "very monotone" (10.59%), "monotone" (48.56%), "slightly expressive and animated" (24.58%), "expressive and animated" (8.32%) and "very expressive and animated" (7.96%); the speaking rate category includes "very slowly" (0.01%), "slowly" (1.60%), "slightly slowly" (15.03%), "moderate speed" (59.81%), "slightly fast" (18.98%), "fast" (4.10%) and "very fast" (0.45%)."

Annotated hours per attribute: "30.8k hours for age, 33.5k hours for gender, **0.4k hours for timbre**, 33.5 k hours for pitch, 2.5 k hours for accent, 33.5 k hours for speaking rate, 2.4 k hours for emotion, 33.5 k hours for expressiveness of tone, and 2.7 k hours for volume." — timbre words (the rasp/grit family) have **~1 % of the data** that pitch words have.

Age bins: `"child" (1–12 years), "teenager" (13–19 years), "young adult" (20–39 years), "middle-aged adult" (40–64 years), and "elderly" (65 years and older)`. Age came from a wav2vec2 age/gender estimator, pitch/expressiveness "Following Parler-TTS" with PENN.

The caption-writing LLM prompt (Mistral-7B) lists "Pitch (e.g., very low pitch, quite high pitch, etc.)", "Pace (e.g., very slowly, quite fast, etc.)", "Tone (e.g., very monotone, quite expressive, etc.)" and instructs "Substitute synonymous terms where appropriate". Example output: "A teenage girl speaks with a high-pitched, bright voice that's lively and expressive, delivering her words at a quick pace."

The human-annotated SFT captions (LibriTTS-P, VCTK via DreamVoiceDB) use keyword sets like "teenager, female, bright, smooth, nasal, cute, and quick pace" → "A teenage girl's voice is bright and smooth, with a slight nasal quality, and she speaks at a lively, quick pace." The AgentDB non-speech tag list includes: "Aww, Throat-clearing, Cheering, Contemplation, Gasp, Groan, Laughter, Panting, Scream, Sigh, Sneering laughter, Sob, Yawn" and low-level prosody tags "Default, Monotonous, Deep, Sharp, Gentle, Loud, Mumble, Stutter, Whispering, Crying, Laughing".

### 2.3 ParaSpeechCaps (Diwan et al., March 2025) — the rich-timbre tag set with definitions

Paper: [Scaling Rich Style-Prompted Text-to-Speech Datasets](https://arxiv.org/html/2503.04713).

> "While rich abstract tags (e.g. guttural, nasal, pained) have been explored in small-scale human-annotated datasets, existing large-scale datasets only cover basic tags (e.g. low-pitched, slow, loud)."

Full intrinsic tag list (Appendix A):
- "Pitch: Shrill, Nasal, Deep."
- "Texture: Silky, Husky, Raspy, Guttural, Vocal-fry."
- "Clarity: Crisp, Slurred, Stammering."
- "Volume: Booming, Authoritative, Loud, Soft."
- "Rhythm: Flowing, Monotonous, Punctuated, Hesitant, Singsong."
- "Accent: American, British, Scottish, Canadian, Australian, Irish, Indian, Jamaican."
- Basic: "High-pitched, Medium-pitched, Low-pitched", "Male, Female".

Situational: "Enthusiastic, Happy, Angry, Saddened, Awed, Calm, Anxious, Disgusted, Scared, Confused, Bored, Sleepy, Pained, Guilt, Sarcastic, Sympathetic, Admiring, Desirous" plus "Animated, Laughing, Passive, Whispered, Enunciated" and "Fast, Measured, Slow".

**The definitions annotators were given** (Table 5) — this is the closest thing to a published dictionary of what these words are meant to mean acoustically:

| Tag | Definition (verbatim) |
|---|---|
| Deep | "A low-pitched, resonant, rich voice." |
| Husky | "A slightly rough, low voice that conveys a gritty texture." |
| Raspy | "A rough, grating, somewhat harsh voice." |
| Guttural | "A deep, throaty, gravelly voice." |
| Vocal-fry | "A creaky, breathy voice that occurs when vocal cords flutter and produce a sizzling, popping sound at ends of sentences." |
| Booming | "A loud, resonant, commanding, powerful voice." |
| Authoritative | "A confident, clear voice with a tone that conveys expertise and assurance." |
| Monotonous | "A dull, flat voice whose pitch, tone and speed remains constant throughout." |
| Punctuated | "An engaging voice with clear, deliberate pauses that emphasize key words." |
| Measured speed | "A controlled, deliberate voice that has an even tone and a moderate speed." |
| Whispered | "A breathy, low-volume voice typically used to speak discreetly." |
| Soft | "A gentle, low-volume, calm and soothing voice typically used to convey subtlety." |
| Pained | "A voice characterized by a strained, trembling tone that indicates sorrow or anguish." |
| Laughing | "A voice with intermittent sounds of laughter conveying amusement and joy." |

Findings that matter here:
- "training on basic tags does not generalize to rich styles" (Parler-TTS baseline had "low Consistency MOS and Tag Recalls").
- Intrinsic tag recall after fine-tuning on ParaSpeechCaps: 69.5 %; situational 75.4 %.
- Tags "guttural, vocal-fry, monotonous, punctuated" were skipped in human eval "as they have an insufficient number of speakers".
- "we observed that the shrill tag is overrepresented by female speakers, while the guttural tag is overrepresented among male speakers."
- Celebrity names were used to *find* speakers (GPT-4 was asked which celebrities have a given tag; VoxCeleb is celebrity speech) but names are **not** in the captions: "All annotated style tags are converted to style prompts using a text LLM, Mistral-7B-Instruct-v0.2".

### 2.4 PromptTTS 2 (Microsoft, 2023) — the one-to-many problem named

Paper: [PromptTTS 2: Describing and Generating Voices with Text Prompt](https://arxiv.org/abs/2309.02285v2).

> "TTS approaches based on the text prompt face two main challenges: 1) the one-to-many problem, where not all details about voice variability can be described in the text prompt"

> "a variation network to provide variability information of voice not captured by text prompts ... the variation network predicts the representation extracted from the reference speech (which contains full information about voice variability) based on the text prompt representation."

PromptTTS/PromptTTS 2 attribute set: gender, pitch, speed, volume (four attributes; PromptTTS 2 reports 98.23 % gender, 92.64 % speed, 92.56 % volume, 89.89 % pitch accuracy). No timbre, no age.

**[inference]** This is the formal statement of problem (1). A description is a *region* of voice-space; every sample from it is a valid reading. Qwen3-TTS-VD has no variation network and no reference; the sampler fills the gap.

### 2.5 VoxInstruct, PromptStyle, VoiceSculptor, OV-InstructTTS

- **VoxInstruct** ([arXiv 2408.15676](https://arxiv.org/abs/2408.15676)): unified instruction + content input; scored 54.9/57.0/39.3 on InstructTTSEval-EN. The paper page fetched did not enumerate its attribute set; **unknown** beyond "style and speaker".
- **PromptStyle** (Liu et al. 2023): scored 57.4/46.4/30.9 EN in Qwen's Table 8. InstructTTSEval: "PromptTTS and PromptStyle struggle most with generating expressive speech, yielding relatively flat and unremarkable samples".
- **VoiceSculptor** ([arXiv 2601.10629](https://arxiv.org/html/2601.10629), Jan 2026, 7 days before Qwen3-TTS): controls "pitch, speaking rate, loudness, speaker gender and age, emotional state, paralinguistic characteristics, and contextual attributes"; continuous features "discretized into 5 intervals per dimension, while age is categorized into 4 groups (child, youth, middle-aged, and elderly)". Annotations: "Gemini 2.5 Pro to obtain multi-dimensional annotations", DataSpeech for prosody, VoxProfile for gender/age. Its consistency answer is the same as Qwen's: "The designed voice is rendered into a prompt waveform and fed into a cloning model to enable high-fidelity timbre transfer for downstream speech synthesis."
- **OV-InstructTTS** ([arXiv 2601.01459](https://arxiv.org/abs/2601.01459), Jan 2026): "existing InstructTTS methods mainly rely on a direct combination of audio-related labels or their diverse rephrasings, making it difficult to handle flexible, high-level instructions." **[verified — abstract]** Adds a reasoning chain from high-level instruction → "emotional labels, acoustic descriptions, and paralinguistic tags". Trained on audiobooks (ContextSpeech, 476.8 h) **[not verified — neither figure is in the abstract; full text not checked]**.

### 2.6 What the caption words do inside the model (attribution study)

Paper: [How Do Instructions Shape Speech? Cross-Attention Attribution for Style-Captioned Text-to-Speech](https://arxiv.org/html/2606.20532v1) (June 2026; studied CapSpeech only). **[verified quotes; architecture caveat added: CapSpeech-TTS is a flow-matching diffusion model that reads the caption through T5 *cross-attention* over 24 ODE steps. Qwen3-TTS is an autoregressive LM that reads the instruct as a prepended ChatML turn in the same token stream — there is no cross-attention to the caption and no ODE schedule. "Global modulator" is a statement about that cross-attention mechanism and does not transfer to Qwen3-TTS by any argument in the paper.]**

- Style words "distribute attention uniformly across the utterance, acting as global modulators rather than aligning to specific temporal regions."
- "loud" correlates most strongly with energy (r=+0.64); "confident" showed higher F0 correlation, "consistent with pitch-raising in confident speech."
- Acoustically grounded words like "loud" and "nasal" showed "higher variance, suggesting they partially modulate specific temporal regions," while abstract descriptors like "cheerful" and **"deep" remained "uniformly distributed."**
- "Style conditioning peaks in early ODE steps" — the caption sets the voice at the start, then fades.

**[inference]** "deep" behaves as a global bias, not a hard constraint, in at least one description-TTS model. That is consistent with a "deep" brief producing a 105 Hz take and a 145 Hz take. **[corrected: "uniformly distributed" in the paper means *temporally non-localised* (attention-map variance 1.1 for "deep" vs 6.3 for "loud"); it does not mean weak. The paper reports no attention–F0 correlation for "deep" specifically (Table 3 lists loud, nasal, confident, nervous, robotic, dramatic…). So this study says nothing about whether "deep" pins pitch; the 105/145 Hz observation is not explained by it.]**

---

## 3. Qwen3-TTS specifically

### 3.1 Tech report — what is and is not disclosed

Paper: [Qwen3-TTS Technical Report](https://arxiv.org/html/2601.15621v1) (arXiv 2601.15621, Jan 2026).

Disclosed:
- "Trained on over 5 million hours of speech data spanning 10 languages"
- "All data is formatted in ChatML to standardize inputs and support controllable speech generation."
- "we prepend user-provided instructions containing fine-grained control signals to the input sequences."
- "For voice design, built upon the Qwen3 text model foundation, Qwen3-TTS inherits robust text comprehension capabilities. Additionally, we introduce a probabilistically activated thinking pattern during training to improve instruction following, especially for complex descriptions. Furthermore, based on this strong instruction-following capability, Qwen3-TTS controls predefined voices with desired styles."
- Post-training: DPO on human-preference pairs, then "rule-based rewards and leverage GSPO", then "lightweight speaker fine-tuning on the base model".

**Not disclosed (unknown):** how voice-description captions were produced, by which captioner, with which attribute list or bins, in what proportion, and what the "thinking pattern" content is. The report's data section says nothing about description data at all. **[verified — all five quotes above are in arXiv 2601.15621v1 and the word "caption" does not occur in it.]**

**[added]** The GitHub README states how the InstructTTSEval numbers were produced: "we ran inference for all models with `dtype=torch.bfloat16` and set `max_new_tokens=2048`. All other sampling parameters used the defaults from the checkpoint's `generate_config.json`. For the Seed-Test and InstructTTS-Eval test sets, we set `language="auto"`". `language="auto"` is the code path that prefills `codec_nothink_id` (§3.3) — i.e. the benchmark scores were obtained with the *no-think* prefill, at T=0.9 / top-k 50.

Table 8 (InstructTTSEval) **[verified against the README table; two rows the researcher omitted are restored]**:

| Type | Model | ZH APS | ZH DSD | ZH RP | EN APS | EN DSD | EN RP |
|---|---|---|---|---|---|---|---|
| Target Speaker | Gemini-flash | 88.2 | 90.9 | 77.3 | 92.3 | 93.8 | 80.1 |
| Target Speaker | Gemini-pro | 89.0 | 90.1 | 75.5 | 87.6 | 86.0 | 67.2 |
| Target Speaker | Qwen3TTS-25Hz-1.7B-CustomVoice (unreleased) | 83.1 | 75.0 | 63.0 | 79.0 | 82.8 | 69.3 |
| Target Speaker | Qwen3TTS-12Hz-1.7B-CustomVoice | 83.0 | 77.8 | 61.2 | 77.3 | 77.1 | 63.7 |
| Target Speaker | GPT-4o-mini-tts | 54.9 | 52.3 | 46.0 | 76.4 | 74.3 | 54.8 |
| Voice Design | **Qwen3TTS-12Hz-1.7B-VD** | 85.2 | 81.1 | 65.1 | **82.9** | **82.4** | **68.4** |
| Voice Design | Mimo-Audio-7B-Instruct | 75.7 | 74.3 | 61.5 | 80.6 | 77.6 | 59.5 |
| Voice Design | VoiceSculptor | 75.7 | 64.7 | 61.5 | – | – | – |
| Voice Design | Hume | – | – | – | 83.0 | 75.3 | 54.3 |
| Voice Design | Parler-tts-mini | – | – | – | 63.4 | 48.7 | 28.6 |

> "Target Speaker (Editing): This scenario tests the ability to modify attributes of a reference speaker." — i.e. delivery direction on a fixed voice was measured on **CustomVoice**, and the VD model was measured only on creation.

### 3.2 Official sample instructs — the format the model has seen

From the [GitHub README](https://github.com/QwenLM/Qwen3-TTS) and the [Qwen blog "Qwen3-TTS Steps Up: Voice Cloning and Voice Design!"](https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign):

**[corrected: provenance]** The blog is dated 23 Dec 2025 (its BibTeX `urldate`) and is about **Qwen3-TTS-VD-Flash**, the *API* voice-design model (`target_model: "qwen3-tts-vd-realtime-2025-12-16"`), released a month before the open 12Hz-1.7B-VoiceDesign checkpoint. Every audio sample on that page was generated by the API model, and its InstructTTSEval claim ("surpasses Gemini-2.5-pro-preview-tts on role-playing tests") is the API model's, not the open checkpoint's. The README reuses the blog's "Lucas" instruct (item 2) for the open model, so the phrasing families are shared, but the blog is not direct evidence of what the open checkpoint was trained on. Items 2–7 below are from that blog.

1. `"Speak in an incredulous tone, but with a hint of panic beginning to creep into your voice."` (README, VoiceDesign, EN)
2. `"Male, 17 years old, tenor range, gaining confidence - deeper breath support now, though vowels still tighten when nervous"` (README + blog)
3. `"Female, 16 years old, mezzo-soprano range, softening - lowering register to intimate speaking voice, consonants softening"` (blog)
4. `"Male, middle-aged, booming baritone - hyper-energetic infomercial voice with rapid-fire delivery and exaggerated pitch rises, dripping with salesmanship"` (blog)
5. `"Male, 30s, strained tenor - breathy sobs interrupt speech, pitch swings wildly between whispers and wails"` (blog)
6. `"Playful Homebody Sis"` (blog, RP-style, three words) **[verified; note the paired Chinese instruct is "邪恶女魔头" — "evil female demon lord" — so the EN and ZH instructs for the same sample are not translations of each other]**
6b. **[added — omitted by the researcher]** The blog's "Persona role-play: rich" *Chinese* sample is a full character card, not a voice description: `角色姓名：陈远山 身份背景：某国家重点科研项目首席顾问，年近七十的资深战略科学家。… 外貌特征：身形挺拔，两鬓斑白，眉宇间刻着岁月沉淀的坚毅。… 性格特质：意志如钢，信念坚定… 人生信条：“我们这一代人，不是为了站在光里，而是为了把路铺到光里。”` — i.e. *name / background / physical appearance / personality / creed*, with age given as "nearly seventy". This is the closest thing in any Qwen material to Isaac's cast-card briefs, and it does contain a description of the *body*. The blog also lists a "Background information" control type in which the instruct is a paragraph *about the text* (e.g. a Wikipedia-style note on Dylan Thomas's villanelle) rather than about the voice at all, and states "Users can freely describe acoustic attributes, persona settings, background information, and more".
7. The blog's "Persona role-play: rich" English sample is **verbatim InstructTTSEval APS format** **[verified]**: `role: Mid-level Corporate Project Manager. gender: Male. pitch: Dynamic male pitch, starting mid-high with agitation, transitioning to a lower declarative range, and spiking upwards with intense emphasis such as 'so finished!'. speed: Variable speaking rate; ... volume: Significant dynamic range; initially loud and forceful, ... age: Middle-aged adult. clarity: Consistently clear articulation, ... fluency: Fluent and coherent speech, ... accent: General American English. texture: Predominantly forceful, becoming strained during agitated outbursts and shouting, otherwise resonant and firm during calmer declarations.. emotion: Starts with pronounced frustration ... tone: Begins as agitated and questioning, ... personality: Assertive and emotionally expressive, ...`
8. API example `voice_prompt`: `"A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation, is suitable for news broadcasting or documentary commentary."`
9. CustomVoice instruct examples: `"用特别愤怒的语气说"`, `"Very happy."`
10. Preset speaker descriptions use: "Bright, slightly edgy young female voice", "Seasoned male voice with a low, mellow timbre", "slightly husky brightness", "clear midrange", "strong rhythmic drive". **[verified — these are the README's CustomVoice speaker-table labels, not instructs]**

**[inference, amended]** Four families of phrasing are demonstrably in Qwen's published material: (a) `Gender, age, register — quality; delivery` one-liners with singing-register words (tenor, baritone, mezzo-soprano); (b) the 12-field APS schema with per-field prose; (c) short role labels; (d) a multi-line character card with name, background, appearance, personality and creed (item 6b). "Kratos"/"God of War" is none of these. Families (a)–(d) are attested for the API model; only (a) and the two README instructs (items 1, 2) are attested in the open checkpoint's own documentation.

### 3.3 What the released inference code does with `instruct`

Source: [`qwen_tts/inference/qwen3_tts_model.py`](https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/qwen_tts/inference/qwen3_tts_model.py) and [`qwen_tts/core/models/modeling_qwen3_tts.py`](https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/qwen_tts/core/models/modeling_qwen3_tts.py).

ChatML wrapping:

```python
def _build_instruct_text(self, instruct: str) -> str:
    return f"<|im_start|>user\n{instruct}<|im_end|>\n"
def _build_assistant_text(self, text: str) -> str:
    return f"<|im_start|>assistant\n{text}<|im_end|>\n<|im_start|>assistant\n"
```

So the description is the **user** turn; the line to be spoken is the **assistant** turn. There is no system prompt. **[verified 12 Sep 2026 against `main` (last commit 17 Mar 2026; PyPI `qwen-tts` 0.1.1, 6 Feb 2026; VoiceDesign weights unchanged since 21 Jan 2026 — nothing here is stale). `generate_voice_design` defaults `non_streaming_mode=True`; `generate_voice_clone` defaults it to `False`, which issue #239/#362 identify as the cause of speaking-rate drift in long clone generations.]**

Speaker path in `modeling_qwen3_tts.py`:

```python
if speaker == "" or speaker == None: # Instruct create speaker
    speaker_embed = None
```

VoiceDesign passes no speaker, so **no speaker embedding is injected** **[verified — `modeling_qwen3_tts.py` line 2088]** — the identity is whatever the sampler draws **[inference]**.

The "think" slot at inference carries only the language id:

```python
codec_prefill_list = [[codec_think_id, codec_think_bos_id, language_id, codec_think_eos_id]]
# or, when language == "auto":
codec_prefill_list = [[codec_nothink_id, codec_think_bos_id, codec_think_eos_id]]
```

No attribute tokens (pitch, age, etc.) are exposed in the released think block. Whatever the report's "thinking pattern" reasons over during training is not surfaced or controllable at inference. **[verified — lines 2135–2147 of `modeling_qwen3_tts.py`; the only two prefills are `[nothink, think_bos, think_eos]` for `language="auto"` and `[think, think_bos, <language_id>, think_eos]` otherwise.]**

Sampling defaults ([`generation_config.json`](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/raw/main/generation_config.json) of the VoiceDesign checkpoint):

```json
{"do_sample": true, "repetition_penalty": 1.05, "temperature": 0.9, "top_p": 1.0, "top_k": 50,
 "subtalker_dosample": true, "subtalker_temperature": 0.9, "subtalker_top_p": 1.0, "subtalker_top_k": 50,
 "max_new_tokens": 8192}
```

Documented kwargs of `generate_voice_design`: `text, language, instruct, do_sample, top_k, top_p, temperature, repetition_penalty, subtalker_dosample, subtalker_top_k, subtalker_top_p, subtalker_temperature, max_new_tokens` plus any HF `generate` kwarg. **There is no `seed` parameter**; the file contains no seed handling **[verified — `grep -i seed` over both files returns nothing]**. Determinism has to come from `torch.manual_seed` outside the call ~~(the ComfyUI node wrappers expose one)~~ **[unsupported — not checked against any wrapper's source; removed]**. **[verified]** The `generation_config.json` values quoted above are current, and the sub-talker settings do apply to this checkpoint: the docstring says they are "only valid for qwen3-tts-tokenizer-v2", and the 12Hz tokenizer *is* v2 (`qwen_tts/core/tokenizer_12hz/modeling_qwen3_tts_tokenizer_v2.py`; `config.json` → `"tokenizer_type": "qwen3_tts_tokenizer_12hz"`).

Docstring: "instruct: Instruction(s) describing desired voice/style. Empty string is allowed (treated as no instruction)."

### 3.4 The README's own answer to consistency

> "#### Voice Design then Clone
> If you want a designed voice that you can reuse like a cloned speaker, a practical workflow is: (1) use the **VoiceDesign** model to synthesize a short reference clip that matches your target persona, (2) feed that clip into `create_voice_clone_prompt` to build a reusable prompt, and then (3) call `generate_voice_clone` with `voice_clone_prompt` to generate new content without re-extracting features every time. This is especially useful when you want a consistent character voice across many lines."

The cloud blog says the same thing in API terms: "Users can also persistently store and repeatedly invoke the voices created by Qwen3-TTS" — the API's `qwen-voice-design` call returns a `voice` name that is then used for synthesis; the description is read **once**. **[verified — README §"Voice Design then Clone" and the blog's `qwen-voice-design` / `preferred_name` / `voice_name` snippet.]**

**[added]** A third official anchor the researcher did not name: `finetuning/README.md` in the repo documents single-speaker SFT of the 12Hz Base model on a labelled clip set ("Keeping `ref_audio` identical across the dataset usually improves speaker consistency"). Community pipelines (discussion #220, Finrandojin's "Alexandria") use VoiceDesign to *generate* that clip set and then fine-tune. It is outside Isaac's constraint but it is the only documented route that yields a reusable speaker id with instruct control retained. Also worth recording: the #220 opener's stated cost of design-then-clone — "the cloned version loses emotional range and naturalness. When used purely within Voice Design, it sounds way better."

### 3.5 Community reports (open-weights model)

- [QwenLM/Qwen3-TTS discussion #220](https://github.com/QwenLM/Qwen3-TTS/discussions/220) (opened 21 Feb 2026): "Chunking isn't really an option because the voice changes when you do that." Reply (10 Aug 2026): "The voice identity remains reasonably consistent, but the narrator's baseline cadence, prosody, and emotional delivery drift between chunks" — "with both CustomVoice and VoiceDesign, across multiple seeds". No maintainer reply as of 12 Sep 2026. **[verified via the GitHub GraphQL API; two comments, neither from a Qwen member. Nuance the researcher under-weighted: the 10 Aug report says identity held "reasonably consistent" when "the same voice, instructions, and seed" were used — the drift it complains about is *delivery*, not identity. That is evidence that a pinned seed does anchor identity to some degree in VD, which cuts against §0's "re-sampled from scratch on every call".]**
- **[added]** [QwenLM/Qwen3-TTS issue #298](https://github.com/QwenLM/Qwen3-TTS/issues/298) (Apr–May 2026, CustomVoice under vLLM; no maintainer reply): a user reports timbre and emotion differ on every run with identical input and that "调整了temperature无效" (adjusting temperature had no effect). Reply: "the only stable way I found for us - use the same seed"; and "The fixed seed does not guarantee byte identical output, because it is applied only to one part of the model, but the fixed seed voice will 'behave' the same - same emotional and vocal range, same artifacts… there will be seeds that produce more varying output… And there will more stable seeds". Anecdotal, but it is the most specific published description of what a seed does and does not hold.
- **[added]** [QwenLM/Qwen3-TTS issue #23](https://github.com/QwenLM/Qwen3-TTS/issues/23) (Jan 2026; issue body since removed, comments remain): a Qwen member (`wangxiongts`, 26 Jan 2026) on duration instructions such as "finish within five seconds": "The model currently does not support this kind of control. Our control capabilities are mainly reflected in controlling speaking style, expressiveness, and prosody." So there *is* one maintainer statement on scope: numeric constraints are out, style/expressiveness/prosody are in.
- [koboldcpp discussion #2192](https://github.com/LostRuins/koboldcpp/discussions/2192), maintainer (LostRuins, 7 May 2026): "Qwen3TTS VoiceDesign - this one can create voices with accurate instructions. However, the voice can vary, as it cannot re-use a voice." **[verified; note this describes koboldcpp's own port of the model, not the Python package]**
- [getstream.io guide](https://getstream.io/blog/qwen3-voice-design/) (17 Apr 2026, uses the open 12Hz-1.7B-VoiceDesign checkpoint): "It is not possible to set speaker `ID` or embedding to anchor the voice. This can hinder speech consistency and slightly alter voice characteristics across several generations using the same prompt." **[verified]** Its sample deep-voice prompt: "A powerful male god with an immensely deep, booming, resonant bass voice that reverberates as if echoing through a vast marble temple. The tone is charming, proud, and strong with a theatrical, grandiose delivery." **[verified]** ~~Its "eight dimensions" list (gender, age, pitch, pace, emotion, accent, timbre, personality) is the blog author's, not Qwen's.~~ **[corrected: the page has a *seven*-row layering table — Identity; Pitch & register; Texture & timbre; Emotion & personality; Pacing & cadence; Accent & dialect; Distinguishing details — the word "eight" does not occur. Still the author's, not Qwen's.]** Its elderly example is "An elderly female grandmother, 80 years old, with a high-pitched, thin, croaky old woman's voice…" — this is where the "80 years old" in §5 comes from, not Qwen.
- [ocdevel guide](https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning) (2 Mar 2026): numeric specs like "finish within five seconds" have "no effect whatsoever" **[verified — ocdevel is quoting issue #23 above]**; "most of the voices have too strong a Chinese accent when speaking English" **[corrected: ocdevel is quoting a third blog (mybyways.com, an MLX-on-macOS write-up) and the sentence is not tied to VoiceDesign specifically — it reads as being about the CustomVoice preset speakers]**; recommends design-then-clone because VoiceDesign produces "slightly different voices on each call" **[verified]**.

None of these are controlled measurements. Nobody has published a run-to-run f0 variance study for Qwen3-TTS-VD; **unknown** beyond anecdote plus the code facts in §3.3.

---

## 4. The acoustic side — what a director's words correspond to

| Measurable property | What it is | Director/phonetician words | Source |
|---|---|---|---|
| **f0 median** (speaking pitch) | Adult male typical range ~93–135 Hz, mean ~116 Hz **[verified — voicescience.org wording; the researcher's "≈110–120 Hz" was a rounding]**; Parler male bins: <82 Hz "very low", 82–99 "quite low", 99–116 "slightly low", 116–133 "moderate" **[verified]** | low-pitched, deep, bass, baritone / high-pitched, tenor | DataSpeech bins §2.1; [Voice Science F0 norms](https://www.voicescience.org/lexicon/average-speaking-frequencies/) |
| **f0 std / range** (utterance) | Parler monotony bins: <20 Hz std "very monotone" … >90 Hz "very expressive" | monotone, flat, level / expressive, animated, singsong, "pitch swings wildly" | §2.1 |
| **Formant scale / apparent vocal-tract length** | Lower formant spacing → bigger apparent body. "Men increased their apparent VTLs by as much as 25% to portray a physically larger body size." "Listeners cross-culturally associate both low F0 and low formants with large body size even within sexes." | big, huge, resonant, booming, chesty, "giant" (only via low f0 + low formants — no caption pipeline labels VTL) | [Pisanski et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5043380/) |
| **Jitter / shimmer** (cycle-to-cycle f0 / amplitude perturbation) | ~~"High jitter is perceived as roughness or aperiodicity; high shimmer is associated with breathiness or hoarseness."~~ **[unsupported — this sentence is not in the cited paper (searched for "perceived as", "aperiodic", "hoarse": zero hits); it is textbook lore written from memory and presented as a quotation. Removed.]** What the paper does say **[verified]**: "The strongest significant correlations for acoustic measures were observed between GRBAS ratings of overall voice quality and perturbation measures (jitter% r=.58, shimmer% r=.45, NHR r=.36…)"; NHR was "significantly correlated with GRBAS ratings of overall quality, breathiness, asthenia and strain"; and — a finding the researcher left out — "It was unexpected, however, that NHR was not significantly correlated with roughness". So in this dataset jitter/shimmer track overall dysphonia, and NHR tracks breathiness/strain rather than rasp. | rough, gravelly, raspy, hoarse, harsh, grating, coarse, gritty | [GRBAS / acoustic correlates](https://pmc.ncbi.nlm.nih.gov/articles/PMC8419204/) (a clinical voice-disorder cohort, not actors) |
| **HNR / CPP** (periodicity vs noise) | Low HNR/CPP = noisy, breathy or rough phonation | breathy, airy, husky, hoarse, whispery | same; [Garellek, Phonetics of Voice](https://idiom.ucsd.edu/~mgarellek/files/Garellek_Phonetics_of_Voice_Handbook_final.pdf) |
| **Spectral tilt / H1–H2** | ~~"lower H1-H2 is associated with creaky voice, while higher H1-H2 occurs with breathy voice"~~ **[corrected: not a verbatim quote from Esposito & Khan; the PDF's actual wording is "along the dimension representing H1–H2: the creaky/tense phonations all had negative values, the modal phonations values were between −1 and 0, and the breathy/lax phonations values were all greater than 0". Same direction, now quoted correctly.]** Tilt decreases with glottal constriction / effort **[inference from the same source]** | creaky, fry, pressed, tense, strained, "banked pressure" / breathy, soft | [Esposito & Khan 2020](https://www.reed.edu/linguistics/khan/assets/Esposito%20Khan%202020%20The%20cross-linguistic%20patterns%20of%20phonation%20types.pdf) |
| **Laver phonation settings** | modal; breathy (open glottis, airflow); creaky ~~("very low pitch and often with highly irregular periodicity")~~ **[corrected: page says "Creak phonation (also called vocal fry) is also produced with vibrating vocal folds but at a very low frequency … responsible for the slower and irregular vibration … pulses are produced in a frequency range from 25 to 50 Hz"]**; harsh ("very strong tension of the vocal folds" … "irregular in both cycle duration and amplitude" **[verified, two separate sentences]**); whispery; falsetto | breathy, creaky, harsh, whispery, falsetto | [IMS Stuttgart phonation types](https://www.ims.uni-stuttgart.de/phonetik/EGG/page10.htm) |
| **Speaking rate** (phonemes/s, silence removed) | Parler bins 0–3.8 … 23–26.8 ph/s | very slowly … very fast; deliberate, measured, brisk, rapid | §2.1 |
| **Pause ratio / rhythm** | not binned by any pipeline; ParaSpeechCaps rich tags only | punctuated, hesitant, flowing, clipped, "beat" | §2.3 |
| **Age markers** | Healthy adults 80–89 "produce significantly higher fundamental frequency, jitter percent, shimmer percent, and shimmer in decibels compared to participants aged 60–69" **[verified against the PubMed abstract, PMID 32083980 — Rojas, Kefalianos & Vogel 2020; note the F0 result is for *pooled* participants, and the abstract's only sex-specific line is "males have significantly higher scores on measures of perturbation, including noise-to-harmonic ratio and absolute jitter"]**; "older individuals are perceived to present with higher overall scores of dysphonia and roughness, breathiness, strain, and instability" **[verified]**; ~~reading rate decreases with age~~ **[unsupported — not in the cited abstract; removed]** | elderly, old, aged, trembling, wavering, croaky, thin | [JSLHR 2020 meta-analysis](https://pubs.asha.org/doi/10.1044/2019_JSLHR-19-00099) |
| **Intensity / effort** | "loud" ↔ energy r=+0.64 in CapSpeech attribution | loud, booming, projecting, shouting / soft, quiet, hushed, whispered | §2.6 |

Two things the science says that matter for casting:

1. **"Deep" is two different knobs.** Low f0 (larynx) and long vocal tract (formants) are independent; listeners use both for size. Caption pipelines label only f0 (via PENN) — none labels formant scale. So "deep" in training data means *low f0*, and "big/huge/giant" has no acoustic label behind it at all. **[inference]** Gimbzo's "eight-foot" cannot be asked for directly; the nearest trained proxies are "very low pitch" + "booming, resonant".
2. **Rasp is perturbation + noise, and it is rare in data.** Gravel/rasp/hoarse = high jitter/shimmer, low HNR **[textbook; the cited GRBAS paper supports jitter/shimmer ↔ overall dysphonia but found NHR *not* correlated with roughness — see table]**. The one pipeline with 10 M captions had 0.4k hours of timbre labels; the rich-tag dataset had too few "guttural"/"vocal-fry" speakers to even evaluate **[both verified]**. Old age adds exactly those markers (jitter, shimmer) *and* raises f0 at 80+ **[corrected: the meta-analysis result is pooled across sexes, not "male"; the male-specific F0 rise with age is a well-known finding elsewhere but is not what this source says]**, which pulls against "extremely deep". **[inference]** "ancient" and "extremely deep bass" are mildly contradictory in acoustic terms and in the data; expect the model to trade one off.

---

## 5. The mapping table

Columns: what you want → words the reviewed caption pipelines / benchmark actually contain → words that appear in **none** of them (Qwen's captions are undisclosed, so "not seen" means "not seen in any published description-TTS training or benchmark vocabulary").

| Desired property | Trained vocabulary (with source) | Probably not in vocabulary |
|---|---|---|
| Very low speaking pitch | "very low pitch" / "very low-pitch" (DataSpeech, CapSpeech — 3.2 % of captions); "low-pitched" (ParaSpeechCaps basic); "Low male pitch", "Low and deep male pitch", "Deep and resonant male pitch" (InstructTTSEval APS `pitch:`); "bass", "baritone", "tenor range" (Qwen blog samples) | "sub-bass", "85 Hz", "an octave below", "Kratos", "Darth Vader", "Mufasa" — no caption pipeline includes numbers, note names or proper names |
| Big / large body / resonance | "Deep" = "A low-pitched, resonant, rich voice" (ParaSpeechCaps def.); "Booming" = "A loud, resonant, commanding, powerful voice"; "resonant" (230/1000 APS textures); "booming baritone" (Qwen blog) | "eight-foot", "giant", "huge chest", "cavernous", "reverberates ... marble temple" (community prompt, effect unmeasured); no pipeline labels vocal-tract length |
| Rasp / grit / gravel | "gravelly" (187/1000 APS textures), "raspy" (33), "rough" (39), "coarse" (9), "husky" (10), "hoarse" ("Deep, gravelly, and somewhat hoarse."), "harsh" (12); ParaSpeechCaps "Raspy" = "A rough, grating, somewhat harsh voice", "Husky" = "A slightly rough, low voice that conveys a gritty texture", "Guttural" = "A deep, throaty, gravelly voice", "Vocal-fry" | "sanded", "sandpaper", "whiskey-and-cigarettes", "growl" as a timbre (it appears in APS only as an event: "low growls to frantic shouts"), "gravel-throated" |
| Dryness (little breath, low tilt) | nearest: "firm" (34), "crisp" (15), "clear vocal texture"; "pressed/tense/strained" (289 — but strained is coded as *effort under emotion*, not a resting timbre); opposite pole "breathy" (11), "Whispered" | "dry" as a voice quality does not appear in any reviewed caption vocabulary — it is a director's word, not an annotator's |
| Old age | "elderly" (CapSpeech bin ≥65, 3.49 %; APS 38), "older adult", "Middle-aged to elderly", "mature vocal quality", "senior"; Parler-TTS-large produced "a trembling voice of an elderly"; community prompt words "croaky", "wavers with age" (unmeasured) | "ancient", "centuries old", "seventy-year-old priest in a young body" (a contradiction no dataset contains — **[inference]** the model will resolve it one way or the other per sample) |
| Child / girl | "child" (CapSpeech 0.15 %; APS 18), "Child or early adolescent", "High child pitch", "teenager", "pre-teen"; Qwen README example "撒娇稚嫩的萝莉女声" (coquettish childish loli female voice) | "twelve-year-old" as a number is unverified; age words are bins ("child" 1–12, "teenager" 13–19), so **[inference]** "12" sits on a bin edge — use "child"/"young girl" |
| Slow, level, flat delivery | "very slowly"/"slowly"/"slightly slowly" (DataSpeech; note "very slowly" = 0.01 % of CapSpeech), "deliberate pace", "measured", "Measured speed" = "controlled, deliberate ... even tone"; "very monotone", "monotone", "Monotonous" = "dull, flat voice whose pitch, tone and speed remains constant"; "stable" (83 APS pitch fields) | "level" (as in emotionally level), "unhurried", "glacial", "beat" |
| Precise / clipped articulation | "clear articulation", "distinct pronunciation", "precise" (142), "crisp" (23), "Enunciated", "clipped" (8), "Punctuated" = "clear, deliberate pauses that emphasize key words" | "sanded", "surgical", "military" |
| Contained pressure / cold | "firm", "authoritative" ("confident, clear voice ... expertise and assurance"), "commanding", "calm" ("calm, gentle and serene"), "tone: cold, detached" (InstructTTSEval intro mentions "a cold, detached tone"), "controlled" | "banked", "coiled", "iron", "glacial" |
| Quiet | "soft" ("gentle, low-volume, calm and soothing"), "hushed", "whispered", "low volume", "conversational level", "softening" | "under his breath" (untested), "sotto voce" |
| Urgent | "urgent" (63 APS speed fields), "hurried", "rushed", "rapid", "accelerating", "conveying urgency", emotion "Anxious" ("rapid or jittery speech patterns") | — (well covered) |
| A laugh / bark-laugh | "Laughing" tag ("intermittent sounds of laughter"), "laugh out", "boisterous laugh", CapSpeech AgentDB "Laughter", "Sneering laughter"; InstructTTSEval: only Gemini and GPT-4o-mini-tts "successfully laugh out"; "NO existing models successfully 'sigh'"; "NO models scream" | "one huge bark-laugh"; bracket cues like `[laugh]` `[sigh]` are **undocumented** for Qwen3-TTS (nothing in README, model card or report mentions inline tags) — **unknown** whether they are read as cues or spoken |
| Accent-neutral English | "General American English" (192 APS accent fields), "Standard American English" (272), "American English" (804/1000), "American" (ParaSpeechCaps), "Received Pronunciation"/"RP" (30), "British English" | "accent-neutral", "no accent", "neutral English" — no pipeline has a "neutral" label; nearest trained meaning of neutral is *General American*. Community reports (ocdevel) Chinese-accented English drift in some VD voices |
| Gender | "male"/"female" (every pipeline; gender is the best-controlled attribute in all of them — PromptTTS 2 98.23 % **[verified]**, Parler 94 % **[not checked]**) | "gender-neutral" ~~(getstream claims it; unmeasured)~~ **[unsupported — the getstream page does not contain "neutral" at all; attribution removed]** |
| Register words | "tenor range", "mezzo-soprano range", "booming baritone", "strained tenor" (Qwen blog), "bass voice" (community) | "basso profundo" (untested) |
| Film / game / celebrity comparisons | **none**. ParaSpeechCaps used celebrity names to *find* speakers, then removed them from prompts. VoxCeleb captions carry no names. InstructTTSEval RP uses role nouns ("betrayed warrior", "worn soldier", "villain", "commanding officer"), never named characters. Qwen's data: unknown. | "Kratos", "God of War", "Christopher Judge", "Vader", "Gandalf" |
| Numeric specs | **none**. Every pipeline bins continuous values to words before the LLM ever sees them; VoiceSculptor uses 5 discrete intervals **[verified]**. Duration numbers "no effect whatsoever" — and a Qwen member confirmed the model "does not support this kind of control" (issue #23, §3.5). Age numbers appear in Qwen's own samples ("17 years old", "16 years old", "30s", "年近七十" = nearly seventy) **[corrected: "80 years old" is from the getstream guide, not Qwen]**. | "105 Hz", "90 wpm", "F0 range 20 Hz" |
| Physical description of the body | **none in any caption pipeline** (no pipeline labels VTL/size; captions describe the *voice*, not the *person*). **[corrected]** But Qwen's own VD-Flash blog sample (§3.2 item 6b) is a character card with an 外貌特征 (appearance) line — "身形挺拔，两鬓斑白" (upright build, greying temples) — so body description *is* attested in Qwen's demonstrated instruct format for the API model. Whether it does anything acoustically is unmeasured. | "eight-foot", "barrel-chested", "giant", "child-sized" |

---

## 6. What this implies for the three problems (evidence-led, not a decision)

### 6.1 Consistency across runs

Facts: no speaker embedding (§3.3), sampling at T=0.9/top-k 50 on two samplers (§3.3), no `seed` in the API (§3.3), the one-to-many problem is the field's own name for this (§2.4), ~~"deep" acts as a global bias not a constraint in the one model where it was measured (§2.6)~~ **[struck — §2.6 is a cross-attention study of a diffusion model and reports nothing about "deep" vs pitch; see correction there]**, and the official README, the cloud API, VoiceSculptor and every community guide converge on "read the description once, then anchor" (§3.4, §2.5, §3.5) **[verified]**.

What text alone can do, per the evidence: narrow the region. The APS-format captions (12 explicit fields including `pitch:` with words like "Low and deep male pitch, generally stable") are the most specified thing the model was scored on, and Qwen scores 82.9 on them vs 68.4 on role-play **[verified; but see §1.4 — the human reference audio scores 67.2 on RP under the same judge, so the APS/RP gap is largely the task's, not the model's]**. **[inference]** A fully specified APS-style brief will produce a *tighter* distribution than "eight-foot giant, God-of-War register", but it will still be a distribution; and numbers in Hz will not narrow it because no caption ever contained one. Whether `torch.manual_seed` gives bit-reproducible output on ROCm with the released code is **unknown** (not tested by anyone I could find). **[corrected]** Discussion #220 does *not* report identity drift under a fixed seed — it reports identity "reasonably consistent" and *prosody/emotion* drifting between chunks "across multiple seeds"; issue #298 reports that a fixed seed makes a voice "behave the same" without byte-identical output. The community evidence, such as it is, points to seed-pinning being the one text-free lever that narrows identity in VD, and to "stable seeds" being something people hunt for by ear.

### 6.2 Per-line direction without identity drift

Facts: the literature's intrinsic/situational split (§2.3) and the "orthogonal capabilities" remark (§1.4 — **[corrected]** a comment on which *models* had which strengths in 2025, not a property of speech); Qwen measured direction-on-a-fixed-voice only on CustomVoice (§3.1) **[verified]**; situational tags are the ones data has in bulk (CapSpeech: 33.5k h expressiveness/rate vs 0.4k h timbre) **[verified]**. **[added]** One more lever the report never examines: the *line text itself*. The model reads the spoken text as the assistant turn, and the blog/README describe it "automatically adjusting tone and rhythm according to semantic content". Punctuation, ellipses, capitals and the wording of the line are a delivery channel that does not touch the instruct — untested here, but it is the only per-line lever that leaves the description string byte-identical.

**[inference]** In pure VoiceDesign, every per-line direction is a new description, and a new description is a new draw. The evidence says "cold, quiet" and "urgent" will be *honoured* (situational words are well-trained) and identity will *move* with them, because nothing holds it. There is no published trick that changes this in a description-only model.

### 6.3 Getting rasp, depth, age, neutral accent from words

Use the annotator vocabulary, in the annotator's structure:
- Depth: "very low pitch", "deep", "bass"/"baritone", "resonant", "booming" ~~— and understand that "deep" was attached to voices one bin below median in Parler-style data~~ **[struck — see §2.1 correction; the example was in an unused legacy prompt]**.
- Rasp: "gravelly", "raspy", "hoarse", "rough", "husky", "guttural" — these are the words with the most texture-field occurrences; none is common in data.
- Age: "elderly", "older adult", "mature"; expect it to pull f0 *up* and add tremor, per the acoustics of real ageing.
- Accent: "General American English" / "Standard American English" — that is what the benchmark and data call neutral.
- Structure: the 12-field `gender: … pitch: … texture: …` block is demonstrably in Qwen's own samples.

Do not expect anything from: numbers, character names, physical size, "dry", "banked", "level", "beat", bracket cues (unknown).

---

## 7. Open questions nobody has published

1. Qwen's voice-description caption source, attribute list and bins. Not in the report, model card, README or blog.
2. Whether Qwen3-TTS reads inline non-verbal cues (`[laugh]`, `[sigh]`) — undocumented.
3. Run-to-run f0/formant variance of Qwen3-TTS-VD under a fixed instruct, and the effect of temperature/top-k on that variance — no measurement found.
4. Whether `torch.manual_seed` yields reproducible VoiceDesign output on ROCm — no report found.
5. What the training-time "thinking pattern" contains — only the language id survives in the released think block.

---

## Sources

- InstructTTSEval paper: <https://arxiv.org/abs/2506.16381> · HTML <https://arxiv.org/html/2506.16381v1> · dataset <https://huggingface.co/datasets/CaasiHUANG/InstructTTSEval>
- Qwen3-TTS Technical Report: <https://arxiv.org/html/2601.15621v1>
- Qwen3-TTS GitHub README: <https://github.com/QwenLM/Qwen3-TTS> · inference code <https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/qwen_tts/inference/qwen3_tts_model.py> · modeling <https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/qwen_tts/core/models/modeling_qwen3_tts.py>
- VoiceDesign model card: <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign> · generation_config <https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/raw/main/generation_config.json>
- Qwen blog: <https://qwen.ai/blog?id=qwen3-tts-vc-voicedesign>
- Qwen3-TTS discussion #220: <https://github.com/QwenLM/Qwen3-TTS/discussions/220>
- Qwen3-TTS issue #298 (seed behaviour, CustomVoice/vLLM): <https://github.com/QwenLM/Qwen3-TTS/issues/298> · issue #23 (maintainer on numeric control): <https://github.com/QwenLM/Qwen3-TTS/issues/23> · issue #239 / PR #362 (streaming-mode speaking-rate drift): <https://github.com/QwenLM/Qwen3-TTS/issues/239>
- Qwen3-TTS finetuning README: <https://github.com/QwenLM/Qwen3-TTS/blob/main/finetuning/README.md>
- Ageing meta-analysis abstract (open access): PubMed PMID 32083980 — Rojas, Kefalianos & Vogel, JSLHR 2020
- koboldcpp discussion #2192: <https://github.com/LostRuins/koboldcpp/discussions/2192>
- DataSpeech: <https://github.com/huggingface/dataspeech> · metadata_to_text.py · run_prompt_creation.py · v02_bin_edges.json (raw links above)
- Parler-TTS paper (Lyth & King 2024): <https://arxiv.org/html/2402.01912> · model card <https://huggingface.co/parler-tts/parler-tts-mini-v1>
- CapSpeech: <https://arxiv.org/html/2506.02863> · <https://huggingface.co/datasets/OpenSound/CapSpeech>
- ParaSpeechCaps: <https://arxiv.org/html/2503.04713>
- PromptTTS 2: <https://arxiv.org/abs/2309.02285v2>
- VoxInstruct: <https://arxiv.org/abs/2408.15676>
- VoiceSculptor: <https://arxiv.org/html/2601.10629>
- OV-InstructTTS: <https://arxiv.org/abs/2601.01459>
- Poly-InstructTTS: <https://arxiv.org/abs/2608.20387> **[listed but never cited in the body — a Jun 2026 "open-ended instruction" TTS paper; not read for this survey]**
- Cross-attention attribution for style-captioned TTS: <https://arxiv.org/html/2606.20532v1>
- Pisanski et al. 2016, body-size exaggeration via F0/VTL: <https://pmc.ncbi.nlm.nih.gov/articles/PMC5043380/>
- GRBAS vs acoustic measures: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8419204/>
- Voice ageing meta-analysis (JSLHR 2020): <https://pubs.asha.org/doi/10.1044/2019_JSLHR-19-00099>
- Phonation types / H1–H2 (Esposito & Khan 2020): <https://www.reed.edu/linguistics/khan/assets/Esposito%20Khan%202020%20The%20cross-linguistic%20patterns%20of%20phonation%20types.pdf> · Laver settings: <https://www.ims.uni-stuttgart.de/phonetik/EGG/page10.htm> · Garellek handbook chapter: <https://idiom.ucsd.edu/~mgarellek/files/Garellek_Phonetics_of_Voice_Handbook_final.pdf>
- F0 norms: <https://www.voicescience.org/lexicon/average-speaking-frequencies/>
- Community guides: <https://getstream.io/blog/qwen3-voice-design/> · <https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning>

---

## Verification

Skeptic pass, 12 Sep 2026. Every key finding was checked against its cited source by fetching the source directly (raw code and JSON via curl; arXiv HTML; the HF dataset via the datasets-server API; GitHub threads via the GraphQL/REST API; the Qwen blog rendered in a browser; the ASHA paper via its PubMed abstract because pubs.asha.org returns 403). Inline marks: **[verified]**, **[corrected: …]**, **[unsupported — removed]**, **[added]**.

### Held as written

- Code facts: `speaker_embed = None` on the `# Instruct create speaker` path; `_build_instruct_text` wraps the instruct as the ChatML user turn and the text as the assistant turn; no system prompt; the think prefill carries only the language id (or `nothink` for `auto`); no `seed` anywhere in `qwen3_tts_model.py` or `modeling_qwen3_tts.py`. `generation_config.json` is exactly as quoted, and the sub-talker settings apply because the 12Hz tokenizer is tokenizer-v2. Not stale: last repo commit 17 Mar 2026, PyPI 0.1.1 (6 Feb 2026), VoiceDesign weights untouched since 21 Jan 2026, no newer VoiceDesign checkpoint on the Qwen HF account.
- README "Voice Design then Clone" paragraph and its "consistent character voice across many lines" sentence; both README VoiceDesign instructs; the CustomVoice speaker-table labels; the InstructTTSEval table (VD 85.2/81.1/65.1 ZH, 82.9/82.4/68.4 EN; CustomVoice 77.3/77.1/63.7 EN).
- Tech report: all five quoted sentences, including "probabilistically activated thinking pattern" and "Target Speaker (Editing): This scenario tests the ability to modify attributes of a reference speaker." The word "caption" does not occur in the report.
- InstructTTSEval paper: the 12-features/four-tiers sentence, the three-task definition, the Gemini captioner, "NO existing models successfully 'sigh'", "NO models scream", the laugh/child/elderly case notes, the DSD/RP-without-audio caveat, and the Table 5 EN scores. Dataset: `en_3` APS row is verbatim; all cited row ids (`en_423`, `en_378`, `en_562`, `en_34`, `en_54`, `en_14`, `en_77`, `en_9`, `en_207`, `en_18`) carry the quoted text; the single "very low" pitch row is `en_657`. Word counts reproduce to within substring-vs-word-boundary noise.
- DataSpeech: all seven bin-word lists in `metadata_to_text.py`; every Hz edge in `v02_bin_edges.json` (105 Hz → "slightly low pitch", 145 Hz → "slightly high pitch" is correct arithmetic). Parler paper: PENN, speaker-mean/utterance-std, Brouhaha SNR/C50, seven bins, C50 failure, 68 % accent. Model-card guidance sentences.
- CapSpeech: every percentage, the per-attribute hours, the age bins, "Following Parler-TTS", the Mistral-7B captioner, the AgentDB tag list, both worked caption examples.
- ParaSpeechCaps: 59 tags, the Appendix A tag lists, every Table 5 definition quoted, "training on basic tags does not generalize to rich styles", 69.5 %/75.4 % (Scaled model), the four skipped tags, the shrill/guttural bias sentence, Mistral-7B-Instruct-v0.2 prompt conversion. "Names never placed in captions" is inferred from that pipeline description, not a quoted sentence.
- PromptTTS 2: the one-to-many sentence and variation-network sentence (abstract); the 98.23/92.64/92.56/89.89 row (Table 1).
- Cross-attention paper: "global modulators" sentence, loud r=+0.64, "confident" F0 note, the abstract-vs-grounded split with "deep" in the abstract group, early-ODE-step peak.
- Pisanski 2016: both sentences verbatim. VoiceSculptor: 5 intervals / 4 age groups / Gemini 2.5 Pro / VoxProfile / "prompt waveform … cloning model". OV-InstructTTS abstract sentence. koboldcpp #2192, getstream anchor sentence and Zeus prompt, ocdevel's three claims (as ocdevel's).
- Discussion #220: quotes verbatim, dates right, no maintainer reply.

### Corrected

1. **"Orthogonal capabilities"** was read as an acoustic separability finding; in context it contrasts closed models (fixed voice, good emotion) with open ones (flexible timbre, weak emotion). Affects §0(2), §1.4, §6.2.
2. **RP "weakest level"** lacked the ceiling: the same Gemini judge scores the *human reference audio* at RP 67.2 EN; Qwen VD's 68.4 sits at that ceiling. Also added that the scores are Gemini-as-judge and that Qwen ran the benchmark with `language="auto"` (no-think prefill).
3. **"Deep = slightly low pitch" in DataSpeech**: the worked example is in the legacy `PROMPT` string; the script uses `NEW_PROMPT`, whose examples contain no "deep". Claim withdrawn in §2.1, §6.3 and the §0 table.
4. **The Qwen blog is about Qwen3-TTS-VD-Flash (API, Dec 2025)**, not the open checkpoint; samples and its benchmark claim are the API model's. And the researcher omitted the blog's Chinese *character-card* instruct (name / background / **appearance** / personality / creed) and its "Background information" control type — the one Qwen-published format that resembles a cast card. §0(3), §3.2, §5 updated.
5. **Cross-attention study**: architecture caveat added (flow-matching + T5 cross-attention vs Qwen's AR LM with in-stream ChatML); "uniformly distributed" means temporally non-localised, not weak, and the paper reports no "deep"↔F0 correlation. The §6.1 reliance on it is struck.
6. **Jitter/shimmer "quotation"** is not in PMC8419204 — removed; the paper's actual correlations substituted, plus its finding that NHR was *not* correlated with roughness.
7. **H1–H2 sentence** was a paraphrase presented as a quote — replaced with the PDF's wording. **Laver creaky** description replaced with the page's wording.
8. **Ageing meta-analysis**: F0 rise at 80–89 is for pooled participants, not "male"; "reading rate decreases with age" is not in the abstract — removed.
9. **getstream**: "eight dimensions" → seven layers with different names; "gender-neutral" claim not on the page — removed. "80 years old" moved from "Qwen's own samples" to getstream.
10. **ocdevel** Chinese-accent line is ocdevel quoting a third blog and is not VoiceDesign-specific; the "no effect whatsoever" line is ocdevel quoting Qwen issue #23.
11. **Discussion #220** was cited as showing drift "even with a fixed seed"; it actually reports identity "reasonably consistent" under a fixed seed with *prosody* drifting. §0 and §6.1 amended.
12. "ComfyUI node wrappers expose a seed" — unverified, removed. OV-InstructTTS's 476.8 h / ContextSpeech — not in the abstract, marked unverified. Poly-InstructTTS listed in Sources but never used.
13. F0 norm: voicescience gives adult male ~93–135 Hz, mean ~116 Hz (report said "≈110–120").

### Missing from the report (what the angle asked for and it did not deliver)

- **A maintainer statement does exist** on control scope (issue #23, `wangxiongts`): numeric constraints unsupported; style, expressiveness, prosody are the control surface. Added to §3.5 and §5.
- **Seed behaviour evidence** (issue #298: fixed seed → same "behaviour", not byte-identical; "stable seeds" exist) — the only text-free consistency lever within Isaac's constraint, and the report treated seeds as a pure unknown. Added.
- **The official third anchor** — single-speaker SFT of Base via `finetuning/` — was never named, nor the #220 opener's cost of design-then-clone ("loses emotional range and naturalness"). Added to §3.4.
- **The line text as a delivery channel** (assistant turn; "adjusting tone and rhythm according to semantic content") — the only per-line lever that leaves the instruct string identical. Added to §6.2. Untested.
- **Benchmark volume vocabulary**: InstructTTSEval APS `volume` is 533 "loud" / 151 "shouting" vs 2 "soft", 4 "quiet", 1 "whisper" — hushed delivery is effectively untested by the benchmark Qwen was scored on. Added to §1.3.
- The 25Hz-1.7B-CustomVoice row (unreleased, scores above the 12Hz CustomVoice on EN) and the Gemini-pro row were dropped from Table 8. Restored.
- Not checked at all (left as the researcher wrote them): Garellek handbook chapter; Parler 94 % gender figure; VoxInstruct's attribute set; the Chinese-side InstructTTSEval vocabulary.

### Surviving key findings after this pass

Code path (no speaker embedding, ChatML user/assistant wrapping, language-only think prefill, no seed, T=0.9/top-k 50 on both samplers); README design-then-clone as the documented fix; the tech report's silence on caption data; VD's InstructTTSEval numbers (with the reference-audio ceiling caveat); the InstructTTSEval taxonomy, vocabulary counts, and sigh/scream failures; DataSpeech's bin words and Hz edges and Parler's measurement stack; CapSpeech's rarity percentages, hours and age bins; ParaSpeechCaps's tag dictionary and its basic→rich non-transfer; PromptTTS 2's one-to-many statement; Pisanski's two-knob size result; the ageing meta-analysis (pooled); "General American English" as the trained "neutral"; the community consensus that VD identity varies per call and numeric specs do nothing; and the open questions in §7 — with the addition that seed-pinning has anecdotal support and should be the first thing measured locally.
