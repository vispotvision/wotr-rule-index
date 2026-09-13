# Roadmap

Agreed with Isaac on 2026-09-12. Phases run in order; each item is checked off
with the commit that landed it. Isaac's standing direction (2026-09-12): inside work he has asked for, the calls
are made, not left pending.

## Phase A — finish what the rulings created

- [x] Filemu Agamalu's card without the Ava-name (C-002)
- [x] Taulagi and Afasoa as Yuno retainers with Japonic names (R23-7)
- [x] Stage-name sweep of the cards: Ignition/Temper → Murmuring/Flourishing (R14-A)
- [x] Büri sweep applied to the 11 scenes in the repo; wiki pages swept block by block (R22-9)
- [x] Proposals filed: Northern forms for airag, borts, aaruul, the deel, Tengri (R23-8); a Japonic name for the island (R21-5)

## Phase B — the table

- [x] Fronts as clocks: `table/fronts.yaml`, `fronts()` / `advance_front()`, shown by `session_start`
- [x] The Ledger collects: `due()` returns what comes due tonight
- [x] `session_end(scene)`: drafts State of Play, Ledger appends, Front advance, docket additions from the scene text
- [x] Scene Menu generator from the clocks and the ledger
- [x] NPC roster per thread

## Phase C — canon integrity

- [x] The reconcile: wiki vs live rules vs scenes, contradictions listed
- [x] Timeline: `scenes/TIMELINE.md`, every scene placed; new scenes checked against it
- [x] Card-to-scene consistency: what a scene says about a character vs the card
- [x] Pack impact check: which live rules a new pack's text touches, before extraction

## Phase D — prose

- [x] Ladder / prose-law pass over the archive: `reports/prose_pass.md`
- [x] Voice fingerprints per character; `verify_scene` flags swapped voices
- [ ] Standing Inventory skeletons for the other cultures, drafted from the wiki for pruning
- [x] Recurrence tracking across scenes (which signature items are stale or overused)
- [x] The gap-fill pass (Thirteen §5) as a structured report

## Phase E — readers

- [x] ARCS.md ordered (set by Claude Code from the numbering; move lines freely)
- [x] Arc compilations: one document per arc in Drive
- [ ] A reader's codex: the trimmed version of the wiki
- [x] Epub build

## Folding packs into base guides — eleven done, 2026-09-12

Isaac: "yes — start folding the packs in now." 18 base guides live at
`C:\Users\isaac\Documents\WOTR True Canon\`; each amendment rule names its
target guide in its `amends.guide` field. Eleven guides are done -- each
got a new dated edition alongside the original (never overwritten), with a
changelog listing every rule ID folded in and any judgment call flagged
rather than silently made. Every edition after the first four went through
a write → adversarial check → bounded fix → re-check loop, and the
changelog records each pass. (Drive for Desktop mirrors that folder: rapid
successive edits to one file can be rolled back to a stale snapshot — it
happened once — so write an edition in as few saves as possible and
verify the byte count after.)

- [x] `WOTR_Master_Style_Directive (2026-09-12 edition).md` — 86 amendments folded; 3 judgment calls flagged (a same-day narration-authority supersession applied despite falling outside the strict amends-field filter; a scope-narrowing read reconciling Pack Five vs. Twelve/Sixteen on prose texture; one non-target-guide clarification folded into the chemistry-ban text)
- [x] `WOTR_Ability_Technique_Design_Guide (2026-09-12 edition).md` — 56 amendments folded; 2 flagged (the legacy Corruption Vector field kept as non-mandatory pending a future pack; the naming-strike rule deferred to the Character Naming Guide rather than importing its content)
- [x] `WOTR_Character_Naming_Guide (2026-09-12 edition).md` — 47 amendments folded; reflects today's Ayame Yuno/Yasoshima rulings; C-005/C-006 (Zettai vs. Zettari) correctly left open, not guessed at; both ruled later that day and folded into the edition's changelog addendum (Zettari; the Zettari carved out of the Japonic stratum, R32-1)
- [x] `WOTR_Combat_Craft_Guide (2026-09-12 edition).md` — 29 amendments folded, plus the 7 live named-character combat assignments in the main body and the 2 still-proposed ones (Wren, Edward Lambert) in a clearly marked pending-review appendix

- [x] `WOTR_Scene_Writing_Process_Guide (2026-09-12 edition).md` — 21 rules folded; three review passes; one open tension surfaced and logged as C-008 (the per-NPC italic-thought standard vs. a locked narration distance)
- [x] `WOTR_Racial_Voice_and_Dialect_Guide (2026-09-12 edition).md` — 15 rules folded (the standalone amendment's 14 + Pack Fifteen's 1); new §8
- [x] `WOTR_Visual_Aesthetic_Guide (2026-09-12 edition).md` — 8 rules folded plus the ratified Moto material-culture rows (R34) as §5a; R11-1-REFERENCE_TRIANGLE cross-referenced, not folded (routed to Pack Nine, an index gap)
- [x] `WOTR_Dialogue_Craft_Standards (2026-09-12 edition).md` — 9 rules folded; seven unrouted Pack Nineteen rows listed in Appendix A, not folded
- [x] `WOTR_AI_Writing_Tells_to_Avoid (2026-09-12 edition).md` — 8 rules folded; Tell Bank entries defined only in the defining rules' own words
- [x] `WOTR_Manual_Verification_Guide (2026-09-12 edition).md` — base recovered from Downloads (2026-08-01 export); 23 rules folded as checks 15–42 with a "Script (v4)" line per check saying what `wotr_verify.sh` actually does; the script's own gaps (no checks 18, 19, 22–29; `--codex` failures never reach the summary line) flagged, not fixed
- [x] `WOTR_Mass_Combat_Craft_Guide (2026-09-12 edition).md` — base recovered from Isaac's Google Drive; 18 rules folded as new §12–§15 (naval, siege, cavalry, practitioner POV); §11 rewritten as the gaps page that records the closures

- [x] `WOTR_Item_and_Equipment_Writing_Guide (2026-09-12 reconstruction).md` — the base is lost everywhere (Downloads, Drive, Trello, the session bundle); rebuilt from its nine live rules, Pack Seven's description of what the original held (Amendment 7.10, as testimony, not law), and the 21 artifact pages' practice; four review passes (fidelity ×2, register, a last count check); §13 lists what the original had that nothing can restore. Isaac: "you might have to create it."

Remaining: the six base guides with 1-6 amendments each -- pick up in a
later session the same way (one agent per guide, same prompt shape, then the
check → fix → re-check loop).

## Narration — done 2026-09-12, growing

`build/audio_export.py` reads the scene archive aloud with Kokoro (local,
CPU, ~5× real time) into the Drive folder `Arcs/Audio/`; a cast file per
scene (`scenes/cast/<scene>.cast.md`, speaker tags on the scene's own text,
validated word for word) gives characters and registers their own voices
from `build/voices.yaml`, with delivery words per line (slow, quiet, beat…)
and Chatterbox Turbo cues ([sigh], [laugh]…) for speakers on that engine.
Chatterbox (its own venv, `build/chatterbox_setup.ps1`) is the expressive
engine: Turbo for cues and speed, standard for the exaggeration knob, both
able to design a voice from a reference clip. The MCP has `scene_text` →
`cast_scene` → `narrate_scene` → `narration_status`, and the public server
serves the MP3s at `/t/<secret>/audio/…`, so a phone can ask for a scene and
play it while the PC is on. Next steps, when wanted: cast files for the
whole archive (a workflow: one agent per scene tags speakers, a checker
validates); a voice per named character in `voices.yaml`; RVC as a third
stage for community-made voices (needs a DirectML/ROCm torch on the 9070
XT); the multilingual Chatterbox checkpoint (already downloaded) for the
Latin lines. Chatterbox now runs on the 9070 XT (`build/chatterbox_gpu_setup.ps1`)
with a Whisper read-back on every span.
**Casting rule (Isaac, after the first multi-voice render):** a voice is chosen
from the character's card and the prose — size, age, how the text says they
sound — not from what a corpus offers; Darius and Gimbzo want deep, raspy,
God-of-War-register voices, not the soft studio readers they got.

**The engine decision (Isaac, 12 Sep 2026, late):** Qwen3-TTS-1.7B-VoiceDesign,
pure voice design, for every character — and the job from here is to make
that one model as good and as efficient as it can be. Corpus clips are out;
the brief is the voice. Done the same night: `engine: qwen` in the narrator
(`build/qwen_backend.py`, `build/qwen_worker.py`), faster-qwen3-tts HIP
graphs (2.4–2.8× real time per draw), best-of-N draws scored against an
approved anchor folder per character with a self-calibrated pass mark,
Praat shaping for exact pace/pitch/body (`build/voice_shape.py`), the brief
manual (`build/voices/QWEN_DESIGN_GUIDE.md`) from four verified research
reports, a 41-character casting book (`build/casting.yaml`) with a
"brief a voice actor" paragraph each, and the two locked leads: Gimbzo on a
Yhwach register (the creaky 63 Hz line is the target; "creaky, vocal fry,
low rumble" is the phrase that finds it, "hoarse" pushes pitch up) and Darius
on Piccolo's floor with Vegeta's manner. Real-person references (Sabat,
Epcar) are briefs, not clips, and personal-use only.
Next: Isaac picks the narrator from the N1–N4 audition; write `qwen_instruct`
for the other 39 characters from their casting briefs (a workflow: one agent
per character drafts the 12-field brief from `casting.yaml` + the guide, a
checker rejects untrained words); anchors for each as Isaac approves takes;
`voice_describe.py` (measure a clip → brief words) for "capture the essence"
briefs; speed — the ggml/Vulkan backend of faster-qwen3-tts, `subtalker`
sampling experiments in the plain venv; loudness normalisation and a gentle
master on the final MP3; RVC only if a character's voice must be held tighter
than best-of-N can.

## Deferred until there is a reason

- Character reference art (Isaac, 2026-09-12). Goal: gather artwork for
  characters from artists and boards, not only local AI output. Design
  agreed: gallery-dl fetches a Pinterest board (or an ArtStation/DeviantArt
  gallery — same tool) into a gitignored `refs/<board>/` folder; a scorer
  runs each new image through Claude vision against the wiki page named
  for it (a character's card, a material-culture page) and writes a small
  tracked `refs/index.json` — pin/source link, artist, board, subject,
  score, verdict, and a `reference-only | licensed` flag; matches are
  attached to the Notion page as a link with credit (reference-only) or an
  embedded image (licensed: commissions, CC-with-the-right-terms). Never
  embed reference-only art on the wiki — friends read it through the
  public MCP now, so that would be redistribution. Images stay out of the
  index repo. Rejected routes: the official Pinterest API (needs a
  business account), hand-rolled scraping of the site. First step when
  wanted: test gallery-dl on one of Isaac's boards.

## Still owed by Isaac

- ~~Muken's children (R22-10)~~ ruled 2026-09-12: the wiki's five (Sodoku, Sonzai, Emira, Tomuka, Ezo)
- ~~Packs Sixteen through Nineteen~~ ratified wholesale 2026-09-12
- ~~Black Agent's and Rengai's combat assignments~~ ratified as pitched 2026-09-12
- Three of the four remaining Four Crafts items (R9-1): Law III's rewrite, the golden-age question, the Latinate/vernacular doublet's scope (the Law V gate was ruled: Stage VII, 2026-09-12)
- Ratification of every proposal Phase A files
