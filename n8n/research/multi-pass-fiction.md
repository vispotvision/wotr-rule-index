# Multi-pass verification for LLM long fiction — what the check passes actually do

Research notes, 2026-09-12. Angle: how practitioners and researchers make chapter-by-chapter LLM fiction hold together, with the focus on the **verification passes** — what they test, what catches real problems vs. theatre, how they gate a chapter, and what still breaks at book length. Every source below was fetched or seen in search results this session; where a summary came from a vendor page it is flagged.

---

## 1. The shape of the problem (measured, not anecdotal)

**ConStory-Bench / "Lost in Stories" (Mar 2026)** — [arXiv 2603.05890](https://arxiv.org/abs/2603.05890), [code](https://github.com/Picrew/ConStory-Bench). The most useful single source for *what goes wrong*.
- 2,000 prompts, stories of 8k–10k words across four tasks (generation 37.5%, continuation 21.6%, expansion 21.1%, completion 19.8%).
- Error taxonomy: **5 categories, 19 subtypes**. Timeline & plot logic (absolute-time, duration, simultaneity contradictions; causeless effects; causal violations; **abandoned plot elements**); characterization (memory, knowledge, skill fluctuation, forgotten abilities); world-building (core rules, social norms, geography); factual detail (appearance, nomenclature, quantities); narrative & style (perspective shift, tone, style variation).
- Where errors live: they **cluster in the 40–60% band of the story** (the middle), sit in text with **+12–19% higher entropy** than the baseline, and **scale roughly linearly with output length**. Factual errors co-occur most with characterization errors (r = 0.304).
- Per-model density (CED = errors per 10k words): GPT-5-Reasoning 0.113, Gemini-2.5-Pro 0.302, Claude-Sonnet-4.5 0.520, GLM-4.6 0.528, MiniMax-M1 3.447.
- **The checker beats humans at finding them.** ConStory-Checker (category-guided extraction → contradiction pairing → evidence chain with quoted spans and positions → JSON report) scored F1 0.678 with 55.0% recall on 1,000 injected errors; human experts managed F1 0.229 / 17.1% recall. Prompts live in `prompts/{characterization,factual_detail,narrative_style,timeline_plot,world_building}.md`. Takeaway: a *category-specific* extraction pass with quoted evidence is a real check; "read this and tell me if anything is inconsistent" is not.

**Magnet + Atlas (Jul 2026)** — [arXiv 2607.00918](https://arxiv.org/html/2607.00918). Same finding from the other direction: Atlas decomposes a story into scene-level event nodes, extracts entities/relations/attributes against a fixed schema (7 node types, 5 edge types), and compares each scene's world state against all prior scenes. F1 0.853 vs 0.805 for vanilla LLM-as-judge. On 100-page stories Magnet drew 24 editorial annotations vs 37 (single model) and 30 (IBSEN); Atlas hallucination counts 6 vs 12 vs 11. At 2 pages the systems are indistinguishable; the gap only opens at 20+ pages.

**Judge reliability caveats** you must design around:
- [LitBench (2025)](https://arxiv.org/abs/2507.00769): best off-the-shelf judge (Claude 3.7 Sonnet) agrees with human story preferences only 73%; GPT-4.1/DeepSeek-R1 70–71%; a trained Bradley-Terry reward model gets 78%. In a human check the LLM judge "performs at chance".
- [StoryAlign / StoryRMB (May 2026)](https://arxiv.org/abs/2605.04831): 1,133 human-verified instances; best existing reward model 66.3% accuracy.
- [Reliability without Validity (Jun 2026)](https://arxiv.org/html/2606.19544v1): raw agreement (83%) masks chance-corrected κ of ~45%; two judges with 99% test-retest consistency had 12–19% position bias. Length bias is now small (<0.011 correlation) on modern models.
- [Rubric artifacts (Sep 2026)](https://arxiv.org/html/2609.02942): rubric *text alone* predicts the verdict at 67–90% accuracy; judges flipped their verdict only 37.7% of the time when the candidate was flipped to violate the rubric. Negation-heavy rubrics bias toward FAIL.
- Practical reading: an aesthetic 1–10 score from one judge is close to noise at the margin; **binary, evidence-quoting, category-scoped checks** are much more reliable than holistic scores.

---

## 2. What the check passes actually test — by system

### Academic plan-write-revise frameworks

| System | Passes | What the pass tests | Loop bound |
|---|---|---|---|
| **Re3** (2022) [arXiv 2210.06774](https://arxiv.org/abs/2210.06774) | Plan → Draft → **Rewrite** (rerank continuations) → **Edit** (factual consistency) | Reranker scores plot coherence + premise relevance; editor fixes contradictions with tracked attributes | one pass per passage |
| **DOC** (2023) [ACL](https://aclanthology.org/2023.acl-long.190.pdf) | Detailed outliner + **detailed controller** | Controller keeps passage aligned to the hierarchical outline node | per passage; +22.5% plot coherence, +28.2% outline relevance over Re3 (human eval) |
| **Dramatron** [README](https://github.com/google-deepmind/dramatron/blob/main/README.md) | Log line → characters → plot → locations → dialogue; human edits at each level | No automated check; "was not conceived or evaluated to be used autonomously"; playwrights called output "formulaic" | human |
| **CritiCS** (EMNLP 2024) [arXiv 2410.02428](https://arxiv.org/html/2410.02428) | CrPlan (3 critics: original theme/setting, unusual structure, unusual ending) → CrText (2 critics: image, voice); a **leader** ranks and picks one critique per round | Creativity/engagement; human "coherent" 77.9% vs 67.3% DOC | **3 rounds** each stage; **more rounds raise creativity but degrade coherence** (Fig. 3); no leader → "noticeable inconsistency" |
| **Agents' Room** (ICLR 2025) [arXiv 2410.02603](https://arxiv.org/html/2410.02603) | 4 planning agents (conflict, character, setting, plot) + 5 writing agents (exposition … resolution), fixed orchestrator | **No critic agent.** Reported failure: high intra- and inter-story trigram repetition, stories 2× too long | n/a |
| **StoryWriter** (CIKM 2025) [arXiv 2506.16445](https://arxiv.org/abs/2506.16445) | Outline → Planning → Writing agent with **dynamic history compression** | Coherence maintained by compressing story-so-far around current events; ~8k-word stories | no explicit critic |
| **LLM Review** (Jan 2026) [arXiv 2601.08003](https://arxiv.org/html/2601.08003) | 3 persona writers **blind-review each other's first drafts**, revise independently (never see peers' revisions) | 5-dim 0–5 rubric (concept integration, speculative logic, character depth, world-building, themes); 3.62 → 3.98 avg | **3 rounds**; gains peak at 3, "decline thereafter" past 4; adding a 4th agent "uniformly degrades all metrics"; ICC with humans 0.58–0.65; risk of **homogenisation** |
| **Plug-and-Play Dramaturge** (Oct 2025) [arXiv 2510.05188](https://arxiv.org/html/2510.05188v3) | Global review (engagement/character/theme/narrative evaluators + integrator) → scene review (dialogue/description/plot/character inspectors + integrator + suggestion router) → coordinated revision (storyline/scene/dialogue editors + polisher) | Four 25-pt dimensions; **Phase 1 structural, Phase 2 detail with storyline locked** | Continue only if script-level score improves ≥ **1.0**; stop after **N_max = 3** non-improving iterations; baselines "exhibit performance drops due to introducing new inconsistencies during revision" |
| **Magnet** (Jul 2026) | Character agents propose actions → **critic** (Gemini 2.5 Flash) accepts/rejects for relevance, specificity, consistency, repetition → narrator (Opus 4.7) selects and writes; rejected actions' state updates never enter the world graph | Consistency vs persona + scene; world state is a typed graph with overwrite resolution | `repeat until r.revise=False or MAX_REVISIONS`; goal replacement after **15 stalled steps**; domain shift every **40 steps** because actions "became increasingly repetitive" |
| **Learning to Reason / VR-CLI** (2025) [arXiv 2503.22828](https://arxiv.org/abs/2503.22828) | Plan the next chapter, reward = how much the plan raises the likelihood of the *real* next chapter | A verifiable signal for plan quality without a judge | training-time only |
| **R2-Write** (Apr 2026) [arXiv 2604.03004](https://arxiv.org/abs/2604.03004), **SuperWriter** (2025) [arXiv 2506.04180](https://arxiv.org/abs/2506.04180) | Reflection/revision baked into the reasoning trace via RL / hierarchical DPO with MCTS | Reasoning models otherwise "achieve limited gains on open-ended writing" | training-time |

### Open-source novel pipelines (the concrete node lists)

**InkOS** (Mar 2026) — [DEV write-up](https://dev.to/dylan_brown_4c803aefcfe51/building-an-autonomous-ai-agent-that-writes-novels-architecture-of-a-10-agent-pipeline-59pf). Ten sequential agents: `Radar → Planner → Composer → Architect → Writer → Observer → Reflector → Normalizer → Auditor → Reviser`.
- Seven "truth files" (now Zod-validated JSON, corrupt data rejected rather than propagated): `current_state`, `particle_ledger` (items/money/stats with quantities), `pending_hooks`, `chapter_summaries`, `subplot_board`, `emotional_arcs`, `character_matrix` (who has met whom; **information boundaries**).
- Observer extracts 9 fact categories; Reflector emits JSON deltas; Auditor checks the draft against all 7 files across **33 dimensions**: characters remembering events they never witnessed, items reappearing after loss, relationship resets, **fake hook advancement** (mentioning a thread without progressing it), knowledge outside witness scope.
- Loop: audit fail → Reviser auto-fixes critical, flags rest for human → re-audit "until all critical issues are resolved" (no documented cap).
- Hook governance: Planner emits a `hookAgenda`; `analyzeHookHealth` audits hook debt, `evaluateHookAdmission` blocks duplicate hooks — built after books accumulated **40+ open threads**.
- Voice: per-genre "fatigue word" lists, banned sentence patterns, a statistical style fingerprint (sentence-length distribution, word frequency, rhythm) injected into later chapters, `revise --mode anti-detect`.
- Cost lesson: before selective retrieval (SQLite temporal memory), stuffing all truth files cost ~$200/chapter and hit token limits by chapter 20.

**Novel-OS** — [GitHub](https://github.com/mrigankad/Novel-OS). Five roles (Architect, Scribe, Editor, Guardian, Curator), each with a machine-parseable OUTPUT CONTRACT block. The interesting part is the **two-layer continuity engine**:
- Layer 1, deterministic, runs before any LLM: `dormant_thread` (idle >3 chapters, warning), `overdue_thread` (past target resolution chapter, **critical**), `unresolved_foreshadowing`, `absent_character` (main cast silent >5 chapters), `never_appeared`, `dead_character_state`, `missing_chapter_file` (critical), `status_drift`, `thin_character`, `relationship_orphan`, `hostile_pair_co_present`, `relationship_since_anachronism`; plus a **sagging-middle detector** (three consecutive chapters with zero plot advance / development / emotional beat / new info).
- Layer 2, LLM Guardian, receives Layer-1 findings as context and returns PASS / WARNING / FAIL. **A chapter cannot be approved while a FAIL is on file.** Humans can mark a finding "this is intentional" with a reason, persisted in `story_state.json` so it is not re-raised — the documented answer to "a checker cannot tell an unreliable narrator, deliberate foreshadowing, or a character who lies from a genuine mistake."

**story-skills** — [GitHub](https://github.com/danjdewhurst/story-skills). Markdown + YAML frontmatter project; the CLI treats the bible "like a compiler treats type errors": `story continuity` catches dead characters walking, payoffs before setup, unfired Chekhov guns, stale scene-cast vs continuity state — **from frontmatter metadata, not prose**. Gate is a PR: `story validate` / `story links` / `story continuity` must pass; word-count and POV mismatches warn, not block. Human review is the final merge.

**Claude-Book** — [GitHub](https://github.com/ThomasHoussin/Claude-Book), [HackerNoon](https://hackernoon.com/claude-book-a-multi-agent-framework-for-writing-novels-with-claude-code). `chapter-planner → chapter-writer → perplexity-improver → style-linter → character-reviewer → continuity-reviewer → state-updater`, "loop if issues found (**max 3 iterations**)". Validators are read-only subagents; only the writer writes. Perplexity gate uses local Ministral-3-8B to find "suspect (too predictable)" sentences and rewrite them (threshold not published). State: permanent `bible/`, versioned `state/chapter-NN/`, append-only `timeline/history.md`. 18-chapter proof of concept.

**AutoNovel (Nous Research)** — [GitHub](https://github.com/NousResearch/autonovel), [ANTI-SLOP.md](https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md). Phase 1 foundation loops until `foundation_score > 7.5`; Phase 2 keeps a chapter only if score **> 6.0**, else retry; Phase 3a adversarial edit → cuts → reader panel → brief → rewrite, stopped by plateau detection; Phase 3b whole-manuscript Opus dual-persona critique until "the reviewer runs out of major items" (example run: 6 automated cycles + 6 Opus rounds). Two evaluators: a **mechanical, no-LLM regex pass** (banned words, clichés, show-don't-tell, sentence uniformity) and an LLM judge (prose, voice adherence, character distinctiveness, beat coverage). Five co-evolving layers (voice → world → characters → outline → chapters, plus `canon.md`) with **propagation debts** recorded in `state.json` when a change in one layer invalidates another.

**AuthorAgent** — [GitHub](https://github.com/Ckokoski/AuthorAgent). "Diffs each chapter against the book's entity database … returns evidence-chained findings — the quote in the chapter vs. the established fact"; each major character critiques *its own* dialogue for off-voice lines, knowledge it couldn't have yet, actions against motivation; GEPA-style judge → diagnose → revise → re-judge that "keeps a candidate only if it measurably improves, never regresses".

**Novel Engine** — [GitHub](https://github.com/john-paul-ruf/novel-engine). Seven named agents (Spark, Verity the only prose writer, Ghostlight cold reader, Lumen dev editor, Forge task master, Sable copy editor, Quill publisher), 15 phases, a **Motif Ledger** for recurring imagery / foreshadowing / overused phrases, series bible. Gate is entirely human: "Nothing advances until *you* confirm it".

**Book-Agent (Level1Techs, local gpt-oss-20b)** — [forum post](https://forum.level1techs.com/t/my-ai-powered-novel-writing-pipeline-book-agent-generating-epistemically-controlled-long-form-fiction/243193). Tracks per-character knowledge state with secrecy classes (public / hidden / delayed / never_explicit) and a revelation schedule; QA engine checks secret leaks, embedding-based repetition vs prior chapters, rotating chapter-opener templates. Notes Qwen3-30B produced excessive "Not X, but Y". 21–48 h per book.

**Barr Group 43-chapter novel** — [blog](https://barrgroup.com/software-expert-witness/blog/ai-agents-finished-decade-old-novel). 3 writers + 3 chapter editors + 4 act-level reviewers with named perspectives (pacing, character, theme/theology, CS accuracy) + publisher. Rule: **A-tier from all four reviewers or the chapter is rewritten.** Panel caught a character age vs timeline mismatch and a wrong location; the human still caught geography, a premise contradiction and an anachronism (a banned fire-suppression system). ~15 min per chapter, 43 chapters in 12 h.

### Commercial tools

- **Sudowrite Chapter Continuity** — [docs](https://docs.sudowrite.com/using-sudowrite/1ow1qkGqof9rtcyGnrWUBS/chapter-continuity/4KL8gFeLZQ6GSBjDWtSbV6), [blog](https://sudowrite.com/blog/how-to-avoid-plot-holes-sudowrites-chapter-continuity-feature-explained/): up to **25 linked documents / 20,000 words of verbatim prior prose** plus 20k words of the current doc, with a published truncation order (worldbuilding drops first, highlighted text last). **Context injection only — no checking pass.** Their own advice for auditing contradictions is "open Chat and ask it".
- **Novelcrafter Codex** — [features](https://www.novelcrafter.com/features/codex): auto-detects Codex entries mentioned in the scene beat and injects them. Again injection, not verification.
- **Novarrium** (vendor, no protocol published) — [test post](https://novarrium.com/blog/ai-writing-tools-keep-contradicting-themselves), [story-bible post](https://novarrium.com/blog/ai-story-bible-structured-memory): claims the four passive-bible tools (ChatGPT, Sudowrite, NovelAI, Novelcrafter) contradict themselves "around chapter 10–15"; pitches auto-extracted typed facts + relevance-weighted injection + **post-generation verification against the whole fact base**. Marketing, but the architecture matches what the papers find works.
- **Inkfluence** (vendor) — [rubric](https://www.inkfluenceai.com/blog/how-to-evaluate-ai-novel-writer-quality-2026): 7 dimensions × 0–5; useful cheap tests: strip dialogue tags from three characters and see if you can still tell who speaks; count summary sentences (>30% = telling); read chapter 12 before chapter 1.

### n8n-shaped loops

- [n8n template 3503 "Recursive Writing & Editing agents"](https://n8n.io/workflows/3503-generate-written-content-with-gpt-recursive-writing-and-editing-agents/): Writing Agent → Editing Agent (Structured Output Parser) → `{"status": "incomplete"|"complete", "edits": "..."}` → **If** node routes `incomplete` back to the writer with the edits. **No iteration cap in the template** — you must add a counter.
- [n8n template 2879 "Book ghostwriting & research"](https://n8n.io/workflows/2879-book-ghostwriting-and-research-ai-agent/): webhook with Book/Chapter record IDs and an action, Switch node per action, writer hands chapter to editor.

---

## 3. What catches real problems vs. theatre

**Real signal (evidence-bearing, narrow, deterministic where possible):**
1. **Typed-fact diff with quoted evidence.** ConStory-Checker, Atlas, AuthorAgent, Novarrium all converge: extract facts per category → pair candidate contradictions → require the checker to quote both spans. This is the one automated check that measurably beats humans (F1 0.68 vs 0.23).
2. **Deterministic ledgers before any LLM.** Novel-OS's 12 checks, story-skills' continuity CLI, InkOS's particle ledger and information-boundary matrix, Book-Agent's secrecy classes. These cannot hallucinate and are free; they catch dead-characters-walking, forgotten threads, knowledge leaks, item reappearances.
3. **Thread/hook accounting with explicit due chapters.** Novel-OS `overdue_thread` (critical) and `dormant_thread` (>3 ch); InkOS hookAgenda + "mention ≠ advance" semantics; story-skills promises/payoffs with planted/paid chapter numbers. This is the only known cure for the "40+ open threads" failure.
4. **Mechanical style tells.** [EQ-Bench Slop Score](https://eqbench.com/slop-score.html) (60% slop words vs wordfreq baseline, 25% "not X, but Y", 15% over-represented trigrams; lists in [slop-score](https://github.com/sam-paech/slop-score)); AutoNovel's regex pass (tiered word lists, sentence-length coefficient of variation, transition clustering, em-dash rate, template-paragraph repetition); InkOS fatigue lists + style fingerprint; Claude-Book perplexity gate. Cheap, reproducible, and they target the actual mechanism of "flattening" (regression to the statistical mean).
5. **Stage separation with a locked skeleton.** Dramaturge's Phase 2 freezes the storyline before detail edits, explicitly to stop later passes reintroducing structural inconsistencies. AutoNovel's layer/propagation-debt model does the same for bible ↔ outline ↔ prose.

**Mostly theatre:**
- A single holistic 1–10 "quality" score used as a gate (LitBench/StoryRMB: 66–73% agreement with humans, chance in some checks; rubric text predicts the verdict).
- Asking the writer model to "check your own chapter for problems" without a fact base — self-critique cannot catch a fact the model already believes, and revision without a locked structure introduces new errors (Dramaturge baselines).
- Unbounded "loop until the editor is satisfied" (the n8n template default). Every measured system plateaus by round 3 (LLM Review, CritiCS, Dramaturge N_max=3, Claude-Book max 3) and degrades after (LLM Review past 4; CritiCS coherence vs rounds).
- Context injection sold as continuity (Sudowrite/Novelcrafter): it reduces errors but nothing *checks*; ConStory shows errors scale linearly with length regardless.

---

## 4. How systems gate a chapter (the actual thresholds seen)

| System | Gate |
|---|---|
| AutoNovel | foundation `> 7.5`; chapter kept iff judge score `> 6.0`, else retry; revision stops on plateau |
| Dramaturge | iterate only if script score gain ≥ 1.0/100; halt after 3 non-improving passes; structural phase before detail phase |
| Novel-OS | deterministic pre-check → Guardian PASS/WARNING/FAIL; **no approval while FAIL**; human "intentional" override persisted |
| story-skills | CI: `validate` + `links` + `continuity` must exit 0 → PR → human merge |
| Claude-Book | three sequential reviewers, loop ≤ 3, then state-update |
| Barr Group | A-tier from all 4 reviewers or rewrite |
| AuthorAgent | accept a revision only if judge score rises (monotone) |
| Magnet | critic `revise=False` or `MAX_REVISIONS`; rejected proposals never touch world state |
| Novel Engine | human confirms every phase |
| LLM Review / CritiCS | fixed 3 rounds, no score gate |

Common pattern across the good ones: **(a)** deterministic checks first, **(b)** an evidence-quoting LLM check scoped by category, **(c)** a hard FAIL class that blocks (continuity, knowledge leak, dead character) vs a soft WARN class that only reports (style, pacing), **(d)** a bounded loop of 2–3 revisions, **(e)** a monotone acceptance rule (never accept a revision that scores lower), **(f)** state written only after the gate passes, **(g)** a human-override channel that records *why* so the checker stops nagging.

---

## 5. What still fails at book length

- **Errors scale linearly with words and pile up in the middle** (ConStory 40–60% band; Novel-OS "sagging middle" detector exists because of this). Plan mid-book checks to be heavier, not lighter.
- **Drift and repetition in agentic loops**: Magnet found actions repetitive after ~15 steps and had to inject domain shifts every 40; Agents' Room reports high trigram repetition; Book-Agent needed embedding-based repetition checks and rotating opener templates.
- **Forgotten setups / hook debt**: the single most-cited practitioner failure (InkOS 40+ threads; Novel-OS overdue/dormant; story-skills unfired guns). Fixes are all ledger-based with due-chapter numbers.
- **Voice flattening / homogenisation**: LLM Review warns extended feedback cycles converge styles; "Towards Human-Level Book-Writing" ([arXiv 2605.17064](https://arxiv.org/abs/2605.17064)) notes generated books are "structurally correct while remaining stylistically generic, overly explanatory"; every revision pass is a regression-to-mean pressure, which is why Claude-Book and AutoNovel put the slop/perplexity pass *inside* the loop rather than at the end.
- **Context bloat**: InkOS hit token limits and ~$200/chapter around chapter 20 before switching to relevance retrieval; Sudowrite caps at 20k words; [Narrative World Model](https://arxiv.org/abs/2607.05577) argues a typed temporal-state graph with query-conditioned retrieval beats Graphiti/Zep-style memory on multi-hop story QA.
- **Checkers cannot read intent**: unreliable narrators, lies, deliberate foreshadowing all read as contradictions (Novel-OS). Human sign-off with a persisted "intentional" flag is the only working answer found.
- **Domain facts**: the Barr Group author still caught geography, an anachronistic device and a premise contradiction the nine-agent panel missed.
- **Revision introducing errors**: Dramaturge baselines got worse when revising without coordination; CritiCS coherence drops with rounds. Freeze structure, then polish.

---

## 6. Sources (all fetched or seen this session)

- Lost in Stories / ConStory-Bench — https://arxiv.org/abs/2603.05890 · https://github.com/Picrew/ConStory-Bench
- Magnet + Atlas — https://arxiv.org/html/2607.00918
- Plug-and-Play Dramaturge — https://arxiv.org/html/2510.05188v3
- LLM Review — https://arxiv.org/html/2601.08003
- CritiCS — https://arxiv.org/html/2410.02428
- Agents' Room — https://arxiv.org/html/2410.02603
- StoryWriter — https://arxiv.org/abs/2506.16445
- Re3 — https://arxiv.org/abs/2210.06774 · DOC — https://aclanthology.org/2023.acl-long.190.pdf · Dramatron — https://github.com/google-deepmind/dramatron/blob/main/README.md
- FACTTRACK — https://arxiv.org/abs/2407.16347 · Narrative World Model — https://arxiv.org/abs/2607.05577
- Learning to Reason / VR-CLI — https://arxiv.org/abs/2503.22828 · R2-Write — https://arxiv.org/abs/2604.03004 · SuperWriter — https://arxiv.org/abs/2506.04180 · Towards Human-Level Book-Writing — https://arxiv.org/abs/2605.17064 · StoryLens — https://arxiv.org/abs/2605.28073
- LitBench — https://arxiv.org/abs/2507.00769 · StoryAlign — https://arxiv.org/abs/2605.04831 · Reliability without Validity — https://arxiv.org/html/2606.19544v1 · Rubric artifacts — https://arxiv.org/html/2609.02942 · LongEval — https://arxiv.org/abs/2502.19103
- InkOS — https://dev.to/dylan_brown_4c803aefcfe51/building-an-autonomous-ai-agent-that-writes-novels-architecture-of-a-10-agent-pipeline-59pf
- Novel-OS — https://github.com/mrigankad/Novel-OS · story-skills — https://github.com/danjdewhurst/story-skills · StoryForge (bootstrap only) — https://github.com/nkchuong1607/storyforge
- Claude-Book — https://github.com/ThomasHoussin/Claude-Book · Claude-Code-Novel-Writer — https://github.com/forsonny/Claude-Code-Novel-Writer
- AutoNovel — https://github.com/NousResearch/autonovel · ANTI-SLOP — https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md
- AuthorAgent — https://github.com/Ckokoski/AuthorAgent · Novel Engine — https://github.com/john-paul-ruf/novel-engine
- Book-Agent — https://forum.level1techs.com/t/my-ai-powered-novel-writing-pipeline-book-agent-generating-epistemically-controlled-long-form-fiction/243193
- Barr Group — https://barrgroup.com/software-expert-witness/blog/ai-agents-finished-decade-old-novel
- EQ-Bench Slop Score — https://eqbench.com/slop-score.html · slop-score — https://github.com/sam-paech/slop-score · awesome-slop — https://github.com/hwajongpark/awesome-slop
- Sudowrite Chapter Continuity — https://docs.sudowrite.com/using-sudowrite/1ow1qkGqof9rtcyGnrWUBS/chapter-continuity/4KL8gFeLZQ6GSBjDWtSbV6 · https://sudowrite.com/blog/how-to-avoid-plot-holes-sudowrites-chapter-continuity-feature-explained/
- Novelcrafter Codex — https://www.novelcrafter.com/features/codex
- Novarrium (vendor) — https://novarrium.com/blog/ai-writing-tools-keep-contradicting-themselves · https://novarrium.com/blog/ai-story-bible-structured-memory
- Inkfluence (vendor) — https://www.inkfluenceai.com/blog/how-to-evaluate-ai-novel-writer-quality-2026
- n8n templates — https://n8n.io/workflows/3503-generate-written-content-with-gpt-recursive-writing-and-editing-agents/ · https://n8n.io/workflows/2879-book-ghostwriting-and-research-ai-agent/
- Curated list — https://github.com/Picrew/awesome-llm-story-generation
