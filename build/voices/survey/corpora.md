# Voice sources: openly licensed, expressive speech corpora for cloning references and voice design

Surveyed 12 September 2026 against the live model cards, READMEs, OpenSLR pages and APIs (not from memory). Everything below was checked this week; corpus pages move, so links are given for re-checking.

**Ground rules applied throughout**

- *Designed or permissioned voices only.* A corpus counts as permissioned when its speakers recorded for release under a stated licence (VCTK, EARS, Expresso, CREMA-D, RAVDESS, EmoV-DB, CMU Arctic, Thorsten, Jenny, OHF/Piper CC0 voices) or when the speaker released the recording into the public domain themselves (LibriVox). "In-the-wild" scrapes of podcasts and video (Emilia, Emilia-YODAS, GigaSpeech's YouTube/podcast portion, VoxBox's Emilia share) are **out**: the speakers never consented to anything and are identifiable real people.
- *Personal listening vs distributed audiobook.* Non-commercial licences (CC BY-NC, CC BY-NC-SA, "research only") are fine for Isaac listening at home; a distributed audiobook, even free, is arguably a "use" that NC clauses restrict once money or a platform is involved, and CC BY-NC-SA additionally demands share-alike on derivatives. Each entry has a `Distribution` line.
- *Hardware note.* None of this needs the GPU. Fetching clips is I/O; the only compute is optional loudness-normalising and trimming a 10 s reference with `ffmpeg`/`sox`. The RX 9070 XT (16 GB) matters only for the engines that consume the references (Chatterbox etc.), which are covered in the sibling survey.

---

## 1. How to fetch one speaker's clips without downloading the corpus

Three mechanisms cover every corpus here.

### 1a. Hugging Face datasets-server `/rows` and `/filter` (tested 12 Sep 2026)

Any dataset with a Parquet export can be paged without cloning. Fields: `dataset`, `config`, `split`, `offset`, `length` (max 100). `/filter` adds `where` (SQL-ish: column names in double quotes, strings in single quotes) and `orderby`.

```
# page rows (works immediately, no index needed)
curl "https://datasets-server.huggingface.co/rows?dataset=ylacombe/expresso&config=read&split=train&offset=0&length=2"

# filter to one speaker + one style
curl "https://datasets-server.huggingface.co/filter?dataset=ylacombe/expresso&config=read&split=train&where=%22speaker_id%22%3D%27ex03%27%20AND%20%22style%22%3D%27whisper%27&length=20"
```

Observed behaviour today:

- `/rows` on `ylacombe/expresso` returned features `['audio','text','speaker_id','style','id']` and rows such as `{'text': 'Why are you beating up my jukebox?', 'speaker_id': 'ex01', 'style': 'confused', 'id': 'ex01_confused_00001'}`. The audio column comes back as a **signed, expiring URL**: `https://datasets-server.huggingface.co/cached-assets/ylacombe/expresso/--/<sha>/--/read/train/0/audio/audio.wav?Expires=1789265651&Signature=...` — download it within the hour.
- `/filter` on a cold dataset answers `{"error": "the dataset index is loading, this can take a minute"}`; in practice every corpus I hit (expresso, libritts_r, hifi-tts, sanchit-gandhi/vctk, badayvedat/VCTK, voxbox) stayed "loading" for the whole session (>30 min). Treat `/filter` as unreliable on first touch; `/rows` and `/statistics` work.
- `/filter` indexing is **partial above 5 GB** ("it only uses the first 5GB"), so on VCTK (11.7 GB) or LibriTTS-R (202 GB of parquet) a filter will silently miss speakers. `/statistics` on `sanchit-gandhi/vctk` reported `partial: true` and only 49 of 110 speakers.
- Script-based datasets have no viewer at all: `CSTR-Edinburgh/vctk` and `keithito/lj_speech` return "The dataset viewer doesn't support this dataset because it runs arbitrary Python code". Use a parquet mirror (`sanchit-gandhi/vctk`, 27 shards, 11.7 GB) or the original tarball.
- Gated sets (`amphion/Emilia-Dataset`, `speechcolab/gigaspeech`) return "not accessible without authentication".

### 1b. DuckDB over `hf://` (reads only the row groups it needs)

From the HF docs (`huggingface.co/docs/hub/en/datasets-duckdb`): DuckDB CLI ≥ 0.10.3 has native `hf://` support, and the auto-converted parquet branch is addressed with `@~parquet`:

```sql
-- one speaker of VCTK, straight from the parquet branch, no clone
SELECT speaker_id, text, age, gender, accent, region, audio
FROM 'hf://datasets/sanchit-gandhi/vctk@~parquet/default/train/*.parquet'
WHERE speaker_id = 'p237' LIMIT 20;
```

or, with the `hf` CLI: `hf datasets sql "FROM 'hf://datasets/ylacombe/expresso@~parquet/read/train/*.parquet' WHERE speaker_id='ex03' AND style='whisper' LIMIT 20" --format json`. Filter pushdown means DuckDB reads the parquet footers and only the matching row groups; on a 12 GB corpus that is typically a few hundred MB, not 12 GB. `/parquet?dataset=...` lists the shard URLs (expresso: 12 shards, 5.8 GB; vctk: 27 shards; libritts_r: 394 shards; hifi-tts: 186 shards, 83.9 GB). DuckDB is not installed on the box (`ModuleNotFoundError: No module named 'duckdb'`); `pip install duckdb` or the single-file CLI.

### 1c. Per-file HTTP (EARS, EmoV-DB, CREMA-D, LibriVox/archive.org)

- **EARS** ships one zip per speaker as a GitHub release asset: `https://github.com/facebookresearch/ears_dataset/releases/download/dataset/p008.zip` (592 MB for p001, 584 MB p002, 652 MB p003 — about 0.6 GB per speaker, 107 assets, plus a 1.38 GB blind test set).
- **EmoV-DB** on OpenSLR 115 is split per speaker per emotion (Bea 102–193 MB per emotion, Sam 55–113 MB, Josh 31–36 MB, Jenie 29–91 MB).
- **CREMA-D** is a Git-LFS repo; `git lfs pull --include "AudioWAV/1034_*"` pulls one actor.
- **LibriVox** is on archive.org, one item per book, one MP3 per section (recipe in section 5).

---

## 2. Corpus-by-corpus

Format: licence · what is in it · speaker metadata · how to get one speaker · best for.

### VCTK (CSTR VCTK Corpus v0.92)
- **Links:** https://datashare.ed.ac.uk/handle/10283/3443 (10.94 GB zip, `license_text.txt`), HF parquet mirror https://huggingface.co/datasets/sanchit-gandhi/vctk
- **Licence:** "This corpus is licensed under the Creative Commons License: Attribution 4.0 International" (README). Commercial OK. **Distribution: OK with attribution.**
- **Content:** 110 English speakers, ~400 read newspaper sentences each, ~44k utterances, studio (anechoic-ish), recorded 96 kHz/24-bit, released 48 kHz/16-bit FLAC, two mics (mic1 DPA 4035, mic2 Sennheiser MKH 800; p280 and p315 have mic2 faults, p315 transcripts lost). Delivery is flat read speech — no emotion, no acting.
- **Metadata:** per-row `age, gender, accent, region` (HF mirror). Accents: English, Scottish, NorthernIrish, Irish, Indian, Welsh. `/statistics` on the (partial) mirror shows ages 19–26 with one 38-year-old (p227, M, Cumbria) — VCTK is a **young-adult** corpus; nobody old, nobody under 18.
- **One speaker:** DuckDB query above, or `/rows` paging; the 12.2 KB HF card is only the README, audio lives in parquet.
- **Best for:** accent variety for a *young* cast (Scottish/Irish/Welsh male voices for soldiers, a Southern-English formal register). Not for giant, old man or child.

### LibriTTS-R (OpenSLR 141)
- **Links:** https://www.openslr.org/141/ ; HF https://huggingface.co/datasets/mythicinfinity/libritts_r
- **Licence:** CC BY 4.0. **Distribution: OK.**
- **Content:** 585 h, 2,456 speakers, 24 kHz, LibriTTS run through Google's speech-restoration (Miipher) — clean but occasionally "restored" artefacts (`libritts_r_failed_speech_restoration_examples.tar.gz` documents the failures). Audiobook read style: a large pool of *narrator* deliveries. Tarballs: dev_clean 1.3 GB, train_clean_100 8.1 GB, train_clean_360 28 GB, train_other_500 46 GB.
- **Metadata:** `speaker_id, chapter_id, text, text_normalized`; **no gender/age in the HF rows**. Gender and LibriVox reader name exist only in the original LibriSpeech/LibriTTS `SPEAKERS.TXT`/`speakers.tsv` inside the tarballs (not exposed on the OpenSLR page; the HF repo tree has only `data/`, `README.md`, `libritts_asr_builder.py`).
- **One speaker:** `dev.clean` is small (1.3 GB, or `/rows` on config `clean`, split `dev.clean`); speaker IDs are LibriSpeech IDs (e.g. 1272), so a LibriVox reader can be mapped back and then fetched directly from archive.org at full MP3 quality instead (see Hi-Fi TTS and LibriVox).
- **Best for:** formal narrator references in bulk; sampling many male voices quickly to shortlist a "deep" one.

### Hi-Fi TTS (OpenSLR 109)
- **Links:** https://www.openslr.org/109/ (41 GB `hi_fi_tts_v0.tar.gz`); HF https://huggingface.co/datasets/MikhailT/hifi-tts (41.9 GB, 648k rows); paper https://arxiv.org/html/2104.01497v3
- **Licence:** CC BY 4.0 (source LibriVox + Gutenberg, public domain). **Distribution: OK.**
- **Content:** 291.6 h, 10 LibriVox readers, 44.1 kHz, ≥17 h each. "Clean" = SNR ≥ 40 dB, "other" = SNR ≥ 32 dB. Speaker table (paper Table 1):

  | ID | Reader | Sex | clean h | other h |
  |---|---|---|---|---|
  | 92 | Cori Samuel | F | 27.3 | — |
  | 6097 | Phil Benson | M | 30.1 | 3.4 |
  | 9017 | John Van Stan | M | 58.0 | — |
  | 6670 | Mike Pelton | M | — | 17.7 |
  | 6671 | Tony Oliva | M | — | 24.1 |
  | 8051 | Maria Kasper | F | — | 30.4 |
  | 9136 | Helen Taylor | F | — | 24.3 |
  | 11614 | Sylviamb | F | — | 22.2 |
  | 11697 | Celine Major | F | — | 26.8 |
  | 12787 | LikeManyWaters | F | — | 27.3 |

- **Metadata:** `speaker, file, duration, text, text_normalized`; sex/name from the table above.
- **One speaker:** `/rows` on config `clean` split `train` (all rows are 6097 or 9017 in the clean config, so paging is enough); or DuckDB `WHERE speaker='9017'`.
- **Best for:** *formal narrator* — 9017 (John Van Stan, 58 h clean) and 6097 (Phil Benson) are the two cleanest long-form male narrators in any open corpus; 92 (Cori Samuel) is the go-to clean female narrator (she is also the `en_GB-cori` Piper voice). Named LibriVox readers: see the consent caveat in §5.

### Expresso (Meta)
- **Links:** https://speechbot.github.io/expresso/ ; HF https://huggingface.co/datasets/ylacombe/expresso (config `read`, 11,615 rows, 12 parquet shards / 5.8 GB)
- **Licence:** "The Expresso dataset is distributed under the CC BY-NC 4.0 license." **Distribution: NO (non-commercial).** Personal listening: yes.
- **Content:** 4 North-American voice actors (2 M, 2 F, ids ex01–ex04; the card does not say which id is which sex — listen to one clip each), 48 kHz/24-bit studio. Read speech in 8 styles (default, confused, enunciated, happy, laughing, sad, whisper, narration) ≈ 11 h; improvised dialogue in 26 styles ≈ 30 h (angry, animal, animal_directed, awe, bored, calm, child, child_directed, confused, default, desire, disgusted, enunciated, fast, fearful, happy, laughing, narration, non_verbal, projected, sad, sarcastic, singing, sleepy, sympathetic, whisper), stereo one-channel-per-actor.
- **Metadata:** `speaker_id, style, text, id` (id encodes speaker and style, e.g. `ex01_confused_00001`).
- **One speaker/style:** `/rows` works now; `/filter` by `"speaker_id"='ex03' AND "style"='whisper'` once its index warms; DuckDB otherwise.
- **Best for:** *style references* — the only open set with acted `whisper`, `projected` (shouting-at-a-distance), `bored`, `sleepy`, `sarcastic`, `awe`, `child`-directed and `narration` from the same voice. Ideal for teaching Chatterbox/other cloners a *manner* (raspy-low giant = male `projected` + `whisper` pair; the priest's formal calm = `narration`/`enunciated`).

### EARS (Meta, Expressive Anechoic Recordings of Speech)
- **Links:** https://github.com/facebookresearch/ears_dataset ; per-speaker zips at `releases/download/dataset/pXXX.zip`; `speaker_statistics.json`, `transcripts.json` in the repo.
- **Licence:** "The code and dataset are released under CC-NC 4.0 International license" (i.e. CC BY-NC 4.0). **Distribution: NO.** Personal: yes.
- **Content:** 107 speakers, 100 h, 48 kHz, anechoic chamber. Per speaker: 18 min freeform monologue; "rainbow passage" sentences in 7 styles (`regular, loud, whisper, high pitch, low pitch, fast, slow`); 22 acted emotions (`emo_adoration … emo_anger, emo_disgust, emo_distress, emo_pain, emo_pride, emo_serenity …`), each as sentences and freeform. File keys look like `rainbow_03_lowpitch`, `emo_anger_sentences`.
- **Metadata:** `speaker_statistics.json`: age band, gender, ethnicity, weight, height, native language. 39 M / 59 F / 1 non-binary / 3 undisclosed; ages 18–25 up to 66–75.
  - Oldest men (56–65): **p008 (British English, 6'–6'3"), p065, p087, p090, p097** (American). The 66–75 band is women only (p021, p084). Men 46–55: p025, p054, p077, p101.
  - Tallest bands cap at 6'–6'3" (p008, p097 among the older men) — no giant-sized speakers, but `lowpitch` + `slow` + `loud` recordings from p008 are the closest thing in any open corpus to a "very low, raspy, slow" acted reference.
  - Young women 18–25 (for a girl's timbre after pitch-shift or design): p011, p028, p035, p041, p043, p045, p052, p053, p056, p062, p067, p068, p073, p075.
- **One speaker:** `curl -L https://github.com/facebookresearch/ears_dataset/releases/download/dataset/p008.zip -o p008.zip` (~0.6 GB), unzip, take `rainbow_*_lowpitch.wav`, `rainbow_*_slow.wav`, `emo_anger_freeform.wav`.
- **Best for:** *giant* (p008 lowpitch/slow/loud), *old man* (p008/p065/p087/p090/p097, 56–65), style-conditioning pairs (same sentence in whisper/loud/low/high).

### EmoV-DB (OpenSLR 115)
- **Links:** https://github.com/numediart/EmoV-DB ; https://openslr.org/115/
- **Licence:** the repo's `LICENSE.md`. [verified 12 Sep 2026, quoted from `numediart/EmoV-DB/LICENSE.md`: "By downloading or using the EmoV-DB Dataset, you are agreeing to the 'Non-commercial Purposes' condition. 'Non-commercial Purposes' means research, teaching, scientific publication and personal experimentation ... Non-commercial Purposes does not include purposes primarily intended for or directed towards commercial advantage or monetary compensation"; commercial use requires contacting Prof. Sarah Ostadabbas.] **Distribution: NO. Personal: yes** ("personal experimentation" is named explicitly).
- **Content:** 4 speakers (Bea F, Jenie F, Sam M, Josh M), 5 styles (neutral, amused, angry, disgusted, sleepy), 16-bit WAV, CMU Arctic sentences; Josh has only 3 styles. "Amused" includes real laughter mid-sentence.
- **One speaker:** per-speaker-per-emotion zips on OpenSLR (e.g. Sam angry 55–113 MB).
- **Best for:** laughter/amused male references (Chatterbox Turbo `[laugh]`), sleepy delivery.

### CREMA-D
- **Links:** https://github.com/CheyneyComputerScience/CREMA-D (Git LFS ~7.55 GB; `VideoDemographics.csv`)
- **Licence:** "Open Database License … Any rights in individual contents are licensed under the Database Contents License" (ODbL 1.0 + DbCL 1.0). Commercial allowed with attribution/share-alike on the *database*; authors ask for a registration form. **Distribution: OK (ODbL attribution).**
- **Content:** 91 actors (52 M / 39 F per the CSV), ages 20–74, 6 emotions × 4 intensities, 7,442 clips of **12 fixed sentences** — clips are 2–3 s, which is short for a 10 s cloning reference (concatenate 4–5 same-emotion clips). 16 kHz-class WAV; quality is lab, not studio.
- **Metadata:** `ActorID, Age, Sex, Race, Ethnicity`. Old men: **1034 (74 M), 1067 (66 M), 1050 (62 M), 1087 (62 M), 1016 (61 M), 1051 (56 M), 1062 (56 M)**.
- **One actor:** `git lfs pull --include "AudioWAV/1034_*"`.
- **Best for:** *old man* timbre with anger/fear/sad variants (1034 at 74 is the oldest male in any open acted set). Not narrator-grade audio.

### RAVDESS
- **Links:** https://zenodo.org/records/1188976
- **Licence:** "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License, CC BY-NC-SA 4.0"; "Commercial licenses for the RAVDESS can be purchased" (ravdess@gmail.com). **Distribution: NO.**
- **Content:** 24 professional actors (12 M / 12 F, odd numbers male), 8 speech emotions × 2 intensities, 2 sentences, 48 kHz/16-bit WAV; audio-only speech zip ≈ 434 MB total. Filename encodes modality-channel-emotion-intensity-statement-repetition-actor, e.g. `03-01-05-02-01-01-01.wav` = audio, speech, angry, strong, actor 01.
- **Metadata:** sex by actor parity; no ages published.
- **Best for:** short, very clean emotional bursts; limited to two sentences so poor as a *timbre* reference.

### ESD (Emotional Speech Database)
- **Links:** https://github.com/HLTSingapore/Emotional-Speech-Data
- **Licence:** signed agreement required, "This database can only be used for research purpose." **Distribution: NO; personal hobby use is also outside "research"** — skip.
- **Content:** 10 English + 10 Mandarin speakers, 5 emotions, 350 parallel utterances each.

### LJSpeech
- **Links:** https://keithito.com/LJ-Speech-Dataset/ (2.6 GB)
- **Licence:** "Public Domain". **Distribution: OK.**
- **Content:** one female (Linda Johnson), 24 h, 13,100 clips, 22.05 kHz, non-fiction. Flat, slightly nasal; the canonical "TTS test voice". Not expressive.

### Common Voice (Mozilla)
- **Links:** now only via Mozilla Data Collective (https://mozilladatacollective.com/); HF mirrors are empty ("Effective October 2025, Mozilla Common Voice datasets are now exclusively available through Mozilla Data Collective"). Version metadata: https://github.com/common-voice/cv-dataset (latest listed v26.0, 2026-06, 42,388 h / 28,893 validated across 294 languages).
- **Licence:** CC0. **Distribution: OK.**
- **Content:** crowdsourced phone/laptop mic MP3s, one sentence per clip. TSV columns `client_id, path, sentence, up_votes, down_votes, age, gender, accents, variant, locale`. Caveats from the release notes: 24.0 (Dec 2025) — "The English dataset will not be released this time again … because of quality issues" and "Demographics data will not be provided for the datasets in this release". So the age/gender buckets that made CV the only open source of *teen* voices are gone in current releases; older archives (e.g. 17.0) still carry them.
- **Best for:** nothing here — mic quality is too poor for a reference and consent covers the clip, not a cloned persona. Only remaining niche: a `teens` bucket in an older release, with a `client_id` filter to gather one speaker, if a young-sounding timbre is needed and the ethics of cloning a minor's crowdsourced voice are acceptable to Isaac (recommendation: no; design the girl's voice instead).

### GigaSpeech
- **Links:** https://huggingface.co/datasets/speechcolab/gigaspeech (gated)
- **Licence:** metadata Apache 2.0; access form binds you to "non-commercial research and educational purposes"; audio is 16 kHz; speaker field is mostly `N/A`. Podcast/YouTube portions are unconsented. **Out.**

### Emilia / Emilia-YODAS and VoxBox
- **Emilia** (https://huggingface.co/datasets/amphion/Emilia-Dataset): CC BY-NC 4.0; Emilia-YODAS CC BY 4.0; 139k h English; gated ("agree to share your contact information"); "in-the-wild speech data" from "video platforms and podcasts". No consent. **Out** on the permissioned-voices rule regardless of licence.
- **VoxBox** (https://huggingface.co/datasets/SparkAudio/voxbox, github.com/SparkAudio/VoxBox): CC BY-NC-SA 4.0 wrapper; 23.76 M rows / 4.84 TB; "Please refer to the original licenses of each sub-corpus." It re-labels VCTK, LibriTTS-R, Hi-Fi TTS, Expresso, EmoV-DB, CREMA-D, RAVDESS, etc. with `age` (Youth/Adult/…), `gender`, `pitch`, `pitch_std`, `speed`, and its metadata is fetched per subset: `hf_hub_download(repo_id="SparkAudio/voxbox", filename="metadata/hifi_tts.jsonl", repo_type="dataset")`. **Use it as an index only**: pull the JSONL, sort by `pitch` ascending within `gender='male'` to find the lowest-pitched consented speakers, then fetch the audio from the *original* corpus under its own licence. Its Emilia-EN (20,298 h) and WenetSpeech4TTS rows are in-the-wild — ignore them.

### MLS (Multilingual LibriSpeech)
- **Links:** https://huggingface.co/datasets/facebook/multilingual_librispeech ; OpenSLR 94
- **Licence:** CC BY 4.0. 16 kHz FLAC, 44,660 h English, `speaker_id, chapter_id`. LibriVox-derived like LibriTTS but 16 kHz — go to archive.org for the same readers at source quality instead.

### LibriVox itself (archive.org) — see §5 for the recipe and the consent discussion.

### Kokoro built-in voice packs (hexgrad/Kokoro-82M v1.0)
- **Links:** https://huggingface.co/hexgrad/Kokoro-82M (VOICES.md)
- **Licence:** Apache 2.0 for weights and voicepacks. **Distribution: OK.**
- **What they are:** 54 style vectors, not audio; no cloning ("custom voice clones" were explicitly excluded from training). Model card: trained on "permissive/non-copyrighted audio data" including "synthetic audio generated by closed TTS models from large providers". Voice names `af_alloy, am_echo, bm_fable, am_onyx, af_nova` match OpenAI's TTS voice names, so several packs are almost certainly distilled from a closed provider's synthetic output — *designed*, not real people, which satisfies the rule, but note the provenance if it ever matters.
- **Grades (VOICES.md):** best `af_heart` (A), `af_bella` (A-, "HH hours"), `bf_emma` (B-); best males `am_michael, am_fenrir, am_puck` (C+), British `bm_fable, bm_george` (C). Duration legend: "10 hours <= HH hours < 100 hours; 1 hour <= H hours < 10 hours; 10 minutes <= MM minutes < 100 minutes; 1 minute <= M minutes < 10 minutes". No male voice is graded above C+, which is why Kokoro sounds flat on male leads.
- **Best for:** fast draft narration (`am_michael`/`bm_george` for a formal narrator; `am_fenrir` the closest to gravel). Not a source of references for other engines.

### Piper / Thorsten and other single-speaker permissioned voices
- **Piper voice cards** (https://huggingface.co/rhasspy/piper-voices/…/MODEL_CARD): each voice carries its own dataset licence —
  - `en_US-joe` (and the other OHF-Voice/voice-datasets voices, e.g. `kathleen`): **CC0** ("These datasets are licensed under CC0 (public domain)"), 27 voices / 15 languages, 22.05 kHz. Distribution OK.
  - `en_US-ryan`: RyanSpeech, **CC BY-NC-SA 4.0**. Personal only.
  - `en_US-hfc_male`/`hfc_female`: NICT Hi-Fi Captain, **CC BY-NC-SA 4.0**. Personal only (NICT site was under maintenance today).
  - `en_GB-alan`: Mycroft `apope` (Alan Pope) — card says "See URL"; that URL's LICENSE reads "Copyright 2022 Mycroft AI, All Rights Reserved". **Not open**; do not use as a reference.
  - `en_GB-northern_english_male`: OpenSLR 83, CC BY-SA 4.0. Distribution OK (share-alike on derivatives).
  - `en_US-lessac`: Blizzard 2013 licence (research agreement). Personal only.
  - `en_GB-cori` = Cori Samuel (Hi-Fi TTS 92), CC BY 4.0.
- **Thorsten-Voice** (https://github.com/thorstenMueller/Thorsten-Voice): **CC0**, German only; 2021.06 emotional set = 300 sentences × 8 emotions, 22.05 kHz, plus a full 44 kHz release on HF; "I contribute my voice as a person believing in a world where all people are equal." Exemplary consent, wrong language for an English audiobook — useful only if an engine's style-transfer is language-agnostic.
- **Jenny (Dioco)** (https://github.com/dioco-group/jenny-tts-dataset): Irish female, ~30 h, 48 kHz, custom attribution licence ("Attribution is required in software/websites/projects/interfaces that generate audio using this dataset"; commercial permitted; credit as "Jenny (Dioco)"). Distribution OK with credit. [verified 12 Sep 2026; the README adds "Attribution is not required when distributing the generated clips (although welcome)" — so the credit obligation sits on the pipeline/tool, not on each audiobook file; crediting anyway costs nothing.]
- **CMU Arctic** (festvox.org/cmu_arctic; mirrors on HF): "Permission to use, copy, modify, and license this software … for any purpose, is hereby granted without fee"; voice talents "signed a waiver"; [verified 12 Sep 2026: festvox.org was reachable and the per-voice `COPYING` file reads "This voice is free for use for any purpose (commercial or otherwise) subject to the pretty light restrictions detailed below" — retain notice, mark modifications, keep authors' names]; 7 core speakers (`bdl` US M, `rms` US M, `awb` Scottish M, `jmk` Canadian M, `ksp` Indian M, `slt` US F, `clb` US F), ~1,150 sentences, 16 kHz. `rms` is the lowest-pitched; `awb` gives a Scottish burr. Old (2003) and 16 kHz, but fully permissioned and commercial-clean.
- **EMNS** (OpenSLR 136, https://openslr.org/136/): Apache 2.0, single British female, 2.3 h, 8 acted emotions with intensity labels, written for "narrative storytelling in games, television and graphic novels". Raw is webm (192 MB). Distribution OK.

### Game / film voice sets that are actually licensed
Short answer: essentially none for real characters. The popular "game voice datasets" (Skyrim, Genshin, Zelda rips) are unlicensed copyrighted performances; public-domain films and old-time radio are public domain as *works* but the actors are named real people, which the project rule excludes. The only game-oriented open set found is **EMNS** above (one actor, consented, Apache 2.0). The LibriVox **dramatic readings** (search `title:"dramatic reading"` in `collection:librivoxaudio`, e.g. `triumphofscarletpimpernel_1407_librivox`, `adventures_of_tom_sawyer_1402_librivox`) are the largest pool of *acted character voices* under a public-domain dedication, with the same reader-consent caveat as all of LibriVox.

---

## 3. Best sources per character type

| Character | Reference audio (clone) | Design / style material | Notes |
|---|---|---|---|
| **Eight-foot giant, very low, raspy, slow** | EARS **p008** (M, 56–65, British, 6'–6'3"): `rainbow_*_lowpitch.wav` + `rainbow_*_slow.wav` + `emo_anger_freeform.wav`; fallback p097. Among Hi-Fi TTS's four men (6097, 9017, 6670, 6671) pick the lowest by measuring: pull 20 clips each via `/rows` and rank by median F0 (`librosa.pyin`), or read `pitch` from VoxBox's `metadata/hifi_tts.jsonl`. CMU Arctic `rms` (US male, 16 kHz). | Expresso male `projected` + `whisper` pair (NC) to teach rasp/effort; then pitch-shift −3 to −5 semitones with formant preserved (`rubberband -p -4 --formant`) | No open corpus has a >6'3" speaker; the rasp will come from the engine's style prompt or a pitched-down, slowed EARS clip, not from a native giant. |
| **Seventy-year-old priest in a young body** | Body = young: Hi-Fi TTS **9017 John Van Stan** (clean, 58 h) or **6097 Phil Benson**; VCTK Southern-England male (p226-type, 22) for a younger timbre | Cadence = old: EARS p008/p065 `slow` + `emo_serenity`, Expresso `narration`/`enunciated`; CREMA-D 1034 (74 M) for the *manner* to imitate in the style prompt | Clone the young timbre; drive the delivery with a slow, formal style reference. |
| **Girl of twelve** | **Do not clone a child.** No consented studio child corpus exists in English; Common Voice `teens` (13–19) is crowdsourced and demographics are now withheld. | Design: youngest EARS women (p011, p028, p035 … all 18–25) `highpitch` + `fast`, then +2–3 semitones formant-preserved; Expresso `child`-style dialogue is an adult *imitating* a child and is exactly the acted reference wanted (NC). Kokoro `af_sky`/`af_river` for a lighter drafting voice. | Voice-design engines (description-conditioned) are the right tool here; the reference is only for manner. |
| **Formal narrator** | Hi-Fi TTS **9017** (M) or **92 Cori Samuel** (F), CC BY 4.0, 44.1 kHz — best in class. LibriTTS-R for breadth. LibriVox Bob Neufeld / Mark F. Smith / Peter Yearsley at source MP3 (public domain, see §5). | Expresso `narration` style; Kokoro `bm_george`/`am_michael` for drafts | Both Hi-Fi TTS narrators are named LibriVox volunteers — public domain, but see §5 before distributing a clone. |

---

## 4. Licence roll-up

| Corpus | Licence | Personal listening | Distributed audiobook |
|---|---|---|---|
| VCTK | CC BY 4.0 | yes | yes (credit CSTR) |
| LibriTTS-R, LibriTTS, LibriSpeech, MLS | CC BY 4.0 | yes | yes |
| Hi-Fi TTS | CC BY 4.0 | yes | yes |
| LJSpeech | Public domain | yes | yes |
| LibriVox recordings | Public domain dedication | yes | legally yes; ethically flagged (§5) |
| Common Voice | CC0 | yes | yes (unsuitable anyway) |
| CREMA-D | ODbL 1.0 + DbCL 1.0 | yes | yes, attribution + share-alike on the database |
| CMU Arctic | CMU permissive ("for any purpose") | yes | yes |
| OHF-Voice / Piper joe, kathleen | CC0 | yes | yes |
| Jenny (Dioco) | custom attribution | yes | yes, credit "Jenny (Dioco)" |
| EMNS | Apache 2.0 | yes | yes |
| Thorsten-Voice | CC0 | yes | yes (German) |
| Kokoro voicepacks | Apache 2.0 | yes | yes |
| Expresso | CC BY-NC 4.0 | yes | **no** |
| EARS | CC BY-NC 4.0 | yes | **no** |
| RAVDESS | CC BY-NC-SA 4.0 | yes | **no** (paid commercial licence exists) |
| RyanSpeech, Hi-Fi Captain (Piper ryan/hfc) | CC BY-NC-SA 4.0 | yes | **no** |
| EmoV-DB | Non-commercial Purposes only (repo LICENSE.md) [verified] | yes | **no** |
| ESD | research-only agreement | **no** | no |
| Emilia, GigaSpeech, VoxBox's wild subsets | NC and/or unconsented | excluded by rule | no |
| Piper en_GB-alan (Mycroft apope) | "All Rights Reserved" | no | no |

Engine licences stack on top: a CC BY reference put through an engine whose weights are CC BY-NC still yields a non-commercial pipeline — check the engine survey.

[verified 12 Sep 2026 against the live licence files: VCTK `license_text.txt` = "Creative Commons License: Attribution 4.0 International"; Hi-Fi TTS OpenSLR 109 "License: CC BY 4.0" and HF mirror tag cc-by-4.0; EARS README "released under CC-NC 4.0 International license" with LICENSE = "Attribution-NonCommercial 4.0 International"; Expresso card and site "CC BY-NC 4.0"; CREMA-D LICENSE.txt = ODbL 1.0 + DbCL 1.0; EMNS OpenSLR 136 "License: Apache 2.0"; Kyutai tts-voices README: voice-donations CC0, VCTK/CML-TTS CC-BY-4.0, Expresso/EARS "Non-commercial use only". No changes needed to those rows.]

---

## 5. LibriVox: finding a deep-voiced reader and pulling one MP3

**Status of the recordings.** LibriVox's wiki page "LibriVox and Artificial Intelligence (AI)": "all LibriVox recordings are released into the public domain. Therefore, it is legal for AI trainers to use them for anything without permission, for free." and "LibriVox has not, does not, and will not sell its recordings to anyone." LibriVox bans AI-*generated* content in its own catalogue but takes no position that binds downstream users. archive.org items carry `licenseurl: http://creativecommons.org/publicdomain/mark/1.0/`.

**The catch for Isaac's rule.** Every LibriVox reader is a named real person. They dedicated *these recordings* to the public domain; they did not, in 2007–2015, contemplate having their voice cloned, and the community has been vocal that "LibriVox recordings are being ingested without permission and used to train commercial voice models" (VoiceProductions summary of the debate). Legally clean, ethically the weakest consent in this list. Recommended handling: use LibriVox readers as *narrator* references for personal listening; for a distributed audiobook prefer Hi-Fi TTS/LibriTTS-R speakers only where the reader is known to be comfortable with synthesis (none have said so publicly), or use designed voices. Bob Neufeld, for what it is worth, has since become a professional narrator (80+ commercial titles) — cloning him for distribution would collide with a working voice actor's livelihood.

**Well-regarded male readers to audition** (names and titles from LearnOutLoud's "Best Librivox Narrators" list and Goodreads/Goodwerks threads; I could not listen from this session, and the web gives almost no timbre descriptions — only Peter Yearsley's "sleepy tone" (Goodwerks) and reviewers calling Neufeld's Jekyll & Hyde "the perfect blend for this story" — so audition each before choosing):
- **Bob Neufeld** — *Jekyll and Hyde* (`jekyll_hyde_1111_librivox`), *Common Sense* (`common_sense_1107_librivox`), *A Christmas Carol* (`christmas_carol_1111_librivox`), *Dorian Gray* (`picture_dorian_gray_1204_librivox`), *Sleepy Hollow* (`sleepyhollow_1206_librivox`). 28 solo items on archive.org. Most-cited "formal narrator" candidate; now a professional narrator (80+ commercial titles).
- **Mark F. Smith** — *White Fang*, *Call of the Wild*, *Treasure Island*, *This Side of Paradise*.
- **Mark Nelson** — *Crime and Punishment*, *Hunchback of Notre Dame*, *Main Street*.
- **Mike Vendetti** — *Red Badge of Courage*, *Benjamin Button*, *Babbitt*.
- **Peter Yearsley** — British; Jerome K. Jerome, Lewis Carroll; "sleepy tone" — audition for a deliberate elderly cadence.
- **David Clarke** (Sherlock Holmes canon), **John Greenman** (Twain), **Phil Chenevert**, **David Barnes** (British).
- Female for comparison: **Cori Samuel** (Hi-Fi TTS 92), **Ruth Golding** (British, *Wuthering Heights*), **Elizabeth Klett**, **Karen Savage**, **Mil Nicholson** (Dickens, character voices).

Audition shortcut: the archive.org `advancedsearch` query in the recipe below, then play `…_64kb.mp3` of section 1 for each — five minutes per reader.

**Recipe (tested today):**

```bash
# 1. solo readings by a named reader (description contains "Read by <name>")
curl -s "https://archive.org/advancedsearch.php?q=collection%3Alibrivoxaudio+AND+description%3A%28%22read+by+Bob+Neufeld%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=runtime&rows=50&output=json"
#   -> 28 hits: common_sense_1107_librivox, christmas_carol_1111_librivox, jekyll_hyde_1111_librivox, ...
#   (a plain "Bob Neufeld" query returns 69 incl. group projects and dramatic readings)

# 2. file list for one item (all MP3s, sizes, durations, licenceurl)
curl -s "https://archive.org/metadata/common_sense_1107_librivox" | python -c "import sys,json;d=json.load(sys.stdin);print(d['metadata']['licenseurl']);[print(f['name'],f['size'],f.get('length')) for f in d['files'] if f['name'].endswith('.mp3')]"
#   -> commonsense_01_paine.mp3 18026684 bytes, 1126.66 s (128 kbps; *_64kb.mp3 variants also present)

# 3. one section, direct
curl -L -o neufeld_ref.mp3 "https://archive.org/download/common_sense_1107_librivox/commonsense_01_paine.mp3"

# 4. cut a clean 10 s reference after the LibriVox disclaimer (first ~20 s), normalise
ffmpeg -ss 45 -t 10 -i neufeld_ref.mp3 -af "loudnorm=I=-20:TP=-2,silenceremove=1:0:-45dB" -ar 24000 -ac 1 neufeld_10s.wav
```

The LibriVox catalogue API (`https://librivox.org/api/feed/audiobooks/?reader=…&extended=1&format=json`) ignored the `reader` filter in testing (returned unrelated Kristin LeMoine titles) but its `extended=1` payload does expose per-section `readers[{reader_id, display_name}]` and `listen_url` (direct archive.org MP3), so it works as a second pass to confirm who read which section of a group project. LibriVox reader pages (`librivox.org/reader/3912`) returned 403 to scripted fetches; use a browser.

---

## 6. Quick decisions

1. **Free, distributable, best quality:** Hi-Fi TTS (CC BY 4.0, 44.1 kHz) is the anchor: 9017/6097 for male narrator, 92 for female. Pull via DuckDB `hf://…@~parquet` or the 41 GB tarball once.
2. **Style/manner references (personal listening only):** EARS per-speaker zips (0.6 GB each; p008 for old/low/slow) and Expresso (`read` config, `/rows` paging) — both CC BY-NC.
3. **Old man:** EARS p008 (56–65, British) and CREMA-D 1034 (74). **Giant:** EARS p008 `lowpitch`+`slow`+`loud`, pitched down. **Girl:** design, don't clone; EARS 18–25 women `highpitch` for manner. **Narrator:** Hi-Fi TTS 9017 / LibriVox Bob Neufeld.
4. **Skip:** Emilia, GigaSpeech, VoxBox-wild, ESD, Piper `alan`, all game rips, Common Voice for references.
5. **Tooling gap on the box:** install `duckdb` (`pip install duckdb`) for hf:// pushdown queries; `ffmpeg` for trimming. Nothing touches the GPU.
