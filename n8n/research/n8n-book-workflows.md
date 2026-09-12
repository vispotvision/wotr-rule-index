# n8n workflows that write books / novels with LLMs — field notes

Researched 2026-09-12. Every workflow below was either pulled as JSON (n8n template API `api.n8n.io/api/templates/workflows/<id>` or GitHub via `gh api`) and read node-by-node, or read from a fetched page. Raw JSON copies are in this folder (`tpl_*.json`, `gh_*_workflow.json`).

## TL;DR

- The official n8n template library has **no novel/fiction template at all** (template search for "novel" and "manuscript" returns nothing relevant). What it has are five or six "eBook / book" templates, all non-fiction oriented, all built on one of two shapes: (a) one agent writes the whole book in one call, or (b) Outline agent → Split Out → Loop Over Items → per-chapter LLM call → Google Doc. None of them pass previous-chapter context into the next chapter. None have a critique pass on chapters.
- The serious fiction pipelines live on GitHub and in blog write-ups, not the template library. The best three, in ascending order of sophistication: **nagoriktech/E-Book-Generator** (clean loop + assembly, no continuity), **yegisyahrial/n8n-ai-auto-novel-generator** (Sheets story bible + previous-chapter text, one chapter per run), **chi-0518/n8n-novel-generator** (Supabase + Claude Sonnet 4.5 + three-tier context: previous chapter, all summaries, RAG style excerpts).
- The only documented "whole novel, unattended" run is Jon Del Arroz's March 2026 Substack post: an n8n loop (next outline beat → last 2,000 words → scene brief → draft → self-critique → revise → assemble), Claude Sonnet 4.6 via OpenRouter, about **$20 per novel**, three books shipped to Amazon. No JSON shared.
- n8n's own long-execution story in 2026: timeouts are off by default (`EXECUTIONS_TIMEOUT=-1`, self-hosted max settable `EXECUTIONS_TIMEOUT_MAX=3600` s by default, AI HTTP timeout `N8N_AI_TIMEOUT_MAX=3,600,000` ms); Cloud has a per-plan ceiling that staff say "is not published as a number". Memory, not time, is the real limit: the Loop Over Items "done" branch accumulates everything, and the docs' fix is Loop Over Items + Execute Sub-workflow so only the current batch lives in memory. Every working book pipeline found writes each chapter to external storage (Sheets, Docs, Airtable, Supabase) inside the loop and never carries the manuscript in execution data.

---

## 1. Official n8n template library (n8n.io/workflows)

### 1.1 "Create AI-generated books with GPT-4.1-mini, DALL-E, Google Drive and AWS S3" — Trung Tran, template 7482
https://n8n.io/workflows/7482-create-ai-generated-books-with-gpt-41-mini-dall-e-google-drive-and-aws-s3/ (created 2025-08-17, 3,490 views)

- **Shape:** Chat Trigger → `Book Brief Agent` (AI Agent + Structured Output Parser) → `Book Writer Agent` (AI Agent used as orchestrator) with two **AI Agent Tool** sub-nodes (`Designer Agent`, `Content Writer Agent`, type `@n8n/n8n-nodes-langchain.agentTool`, prompt fed by `$fromAI('Prompt__User_Message_')`) → OpenAI image node (`dall-e-2`) → AWS S3 → Set → Markdown node (markdownToHtml) → HTTP upload to Google Drive → convert to PDF → archive to Drive folder.
- **Models:** four `lmChatOpenAi` nodes, all `gpt-4.1-mini`.
- **Prompt shapes:** Book Brief Agent system message: "Your ONLY job in this call: return a single planning JSON object with keys { book_brief, cover_design_brief, writing_brief }" with a full schema (working_title, audience, tone, keywords, `target_word_count`, `chapter_count`, outline[], include_front_matter, citations_policy). User prompt hard-codes "Audience: Kid, Target word count: 10000, Chapter count: 5". Content Writer Agent tool description: "write the entire book in Markdown … ## Chapters (match chapter_count) … Respect language, tone, target_word_count (±15%), and chapter_count."
- **State/memory:** none. No loop. The whole 10,000-word book is expected from **one** tool call.
- **Weaknesses:** a single completion for a 10k-word book (most models cap output well below that, and quality degrades long before); no per-chapter continuity because there is no per-chapter step; no critique; the Markdown node does `replaceAll("---",'/n')` (a typo for `\n`); the "children-friendly" instruction is baked into the orchestrator system prompt. A demo of the AI Agent Tool node, not a book engine.

### 1.2 "Book ghostwriting & research AI agent" — Agniva Mahata, template 2879
https://n8n.io/workflows/2879-book-ghostwriting-and-research-ai-agent/ (created 2025-02-11, 2,376 views)

- **Shape:** an **Airtable-driven state machine**. `Webhook` (path `ai-book`, query `recordId` + `action`) → `Switch` on `$json.query.action` with four branches: `bookDetails`, `generateChapters`, `generateChapterResearch`, `generateChapterContent`. Each branch: Airtable get → LLM → Airtable update, setting `Action` back to `"Idle"`. Airtable automations fire the webhook when a human changes the Action field. Book table fields: Idea, Action, Research, Description, Audience, Chapter. Chapter table: Chapter Name, Description, Action, Research, Chapter Content, Book, Idea, Book Research.
- **Models:** `gemini-2.0-flash-exp` (research agents), `gpt-4o` (chapter list, with Structured Output Parser `{chapters:[{title,description}]}`), `gemini-exp-1206` (chapter prose). Perplexity `sonar` via `toolHttpRequest` with a `{query}` placeholder.
- **Prompt shapes:** chapter list: "You'll give 7-10 chapters for each book, and the chapters should be well thought and connected to the previous one". Research agent: "You have a limited number of uses for the Perplexity tool (maximum 5 times)" broken down as "Max 2 uses" description research, "Max 2 uses" audience, "Max 1 use" general. Chapter prose user prompt: book idea + `Book Research` + chapter name + chapter research + "======= PERFECT NOW WRITE THE CONTENT FOR THE CHAPTER ======"; system: "it should be a long chapter".
- **Long executions:** avoided entirely — every webhook call is one short execution; the human clicking Action in Airtable is the scheduler.
- **Weaknesses:** the chapter-prose prompt never sees previous chapters (no continuity, no summaries); no assembly step (chapters stay in Airtable cells); no word target; tool-use limits are enforced only by prompt text; non-fiction/research framing.

### 1.3 "Create structured eBooks in minutes with Google Gemini Flash 2.0 to Google Docs" — Ranjan Dailata, template 5707
https://n8n.io/workflows/5707-create-structured-ebooks-in-minutes-with-google-gemini-flash-20-to-google-docs/ (created 2025-07-05, **8,560 views — the most-viewed book template**)

- **Shape:** Manual Trigger → Set(`Title` = "Provide me n8n beginners guide with chapters and high-level steps") → Basic LLM Chain + Structured Output Parser (manual JSON schema: `metadata{title,description,audience,author,category}`, `structure.chapters[{chapterNumber,title,objectives[]}]`) → Code (`return $input.first().json.output.structure.chapters`) → **Loop Over Items** → Set(title, objectives) → Basic LLM Chain "Provide a detailed chapter explanation for the following Title: … Objective: …" → Google Docs **create** → Google Docs update (insert text) → back to Loop Over Items.
- **Models:** two `lmChatGoogleGemini` nodes, `models/gemini-2.0-flash-exp`.
- **Weaknesses:** creates a **new Google Doc per chapter** (the create node is inside the loop); the loop's "done" output is connected to nothing, so there is no assembly; the chapter prompt has zero cross-chapter context; no critique; two-line prompts. Popular because it is the smallest possible working example of the Outline → Loop → Chapter shape.

### 1.4 "Generate written content with GPT Recursive Writing & Editing agents" — Matty Reed, template 3503
https://n8n.io/workflows/3503-generate-written-content-with-gpt-recursive-writing-and-editing-agents/ (created 2025-04-09, 1,579 views)

- **Shape (from connections; parameters are stripped in the public JSON):** Chat Trigger → `chatInput` (Set) → `handle edits` (Code: previous edits, defaults to empty string) → `Writing Agent` → `Editing Agent` (with Structured Output Parser, output `{"status": "incomplete|complete", "edits": "..."}`) → `set variables` → `If Status Complete` → true: `chatOutput`; false: back to `handle edits`. One `OpenAI Chat Model` and one `Window Buffer Memory` (Simple Memory) are shared by **both** agents.
- **Worth copying:** the writer/editor loop with an If node feeding back is the idiomatic n8n way to do a critique pass; the editor returning a machine-readable `status` is what makes the loop terminate.
- **Weaknesses:** no visible max-iteration guard (the docs warn "If your termination condition never matches, your workflow execution will get stuck in an infinite loop"); writer and editor share the same memory buffer, so the editor sees its own past critiques as conversation; scoped to a "blurb", not a chapter.

### 1.5 "Generate complete stories with GPT-4o and save them in Google Drive" — Ian Dikhtiar, template 3153
https://n8n.io/workflows/3153-generate-complete-stories-with-gpt-4o-and-save-them-in-google-drive/ (created 2025-03-13, 1,524 views)

- **Shape:** 57 nodes, 10 AI Agents in a straight line, each with its own Structured Output Parser: `story rules` → Sentiment Analysis → seven Set nodes (Connect / Convince / Explain / Impress / Lead / Motivate / Sell — a purpose router based on "PipDeck Storyteller Tactics") → `prompt` → `story baseline` → `characters` → `pick cards` → Split Out → Loop Over Items → `story enhancement` → Aggregate → `story plot` → `story timeline` → `story draft` → `edit notes` (automated critique: "clichés, weak dialogues") → `story_final` → Google Drive create file.
- **Model:** one Azure OpenAI Chat Model (`gpt-4o1`) feeding all agents.
- **Worth copying:** explicit staged decomposition (rules → baseline → characters → plot → timeline → draft → edit notes → final) with a structured parser after every stage; a real critique-then-rewrite pair.
- **Weaknesses:** single short story in one `story draft` call — no chapter loop; prompts are hidden in the published JSON; the loop is only over "cards" (storytelling techniques), not chapters.

### 1.6 "Learn anything, write a book, design a curriculum" — Mohammed Rifad, template 4492 ($75 paid)
https://n8n.io/workflows/4492-learn-anything-write-a-book-design-a-curriculum/ — OpenRouter models, a "SeniorWriter" persona writing per curriculum section, and a `Notion Block Ninja` **sub-workflow** converting Markdown into Notion block JSON. Non-fiction; paid, so nodes not inspected.

### 1.7 Nothing fiction-shaped in the library
n8n template search API (`api.n8n.io/api/templates/search`) on 2026-09-12: "novel" → 1 unrelated result; "manuscript" → 0; "ebook" → 3 (one is 5707 above); "story chapters" → video/bedtime-story templates only.

---

## 2. GitHub repositories (workflow JSON read node by node)

### 2.1 yegisyahrial/n8n-ai-auto-novel-generator — "AI-Powered Auto Novel Generator Assistant"
https://github.com/yegisyahrial/n8n-ai-auto-novel-generator (created 2026-08-07, Indonesian-language web novel, Gemini)

- **Shape (one chapter per execution, 13 nodes):** Manual Trigger → five Google Sheets reads from one spreadsheet "Novel Structure" (tabs `Story_Info`, `Characters`, `Locations`, `Chapters`, `Outline_Chapter`) → Code `Merge & Logic` → Google Docs **get** (previous chapter's doc) → AI Agent → Google Docs create ("BAB N - title") → Google Docs update (insert prose) → Sheets append to `Chapters` (Chapter Number, Chapter Title, Google Doc URL, Created At) → Sheets update `Outline_Chapter` row `Status = Done`.
- **State logic (Code node):** `lastCompletedNum = max(Chapter Number in Chapters)`, `targetNumToWrite = lastCompletedNum + 1`, look that up in `Outline_Chapter`, fall back to the first row with `Status == "planned"`; extract the previous chapter's Doc URL; build `full_story_text` by concatenating text of every earlier chapter row; if none, "Ini adalah Bab 1…".
- **Model:** `lmChatGoogleGemini` `models/gemini-3.1-flash-lite`, `maxOutputTokens: 4096`.
- **Prompt shape (user message, sections in order):** `=== MOST RECENT CHAPTER CONTENT (LAST GENERATED GOOGLE DOC) ===` (full previous chapter) → `=== FULL STORY MANUSCRIPT RECAP ===` → `=== STRICT CONTINUITY & ANTI-DUPLICATION RULES ===` ("Start the opening scene EXACTLY where the Google Doc content above ended", "If an event, item acquisition, or crafting process ALREADY happened … DO NOT WRITE IT AGAIN", strict third person) → `=== DIALOGUE-DRIVEN CHAPTER STRUCTURE (TARGET: 1,000 - 1,200 WORDS) ===` with four phases budgeted at ~250 / ~400 / ~350 / ~200 words and "At least 50% to 60% of this chapter MUST consist of spoken dialogue" → formatting rules (2–4 sentences per paragraph, new paragraph per speaker, no Markdown, no chapter titles) → `=== CURRENT CHAPTER OUTLINE TO WRITE ===` (Chapter Number, Title, Plot Summary, Featured Characters, Location, Goal / Outcome from the outline row) → `=== MANDATORY WRITING STYLE ===` (a `Writing Style` cell in Story_Info) → `=== ACTIVE CHARACTERS CONTEXT ===` and `=== SCENE LOCATION CONTEXT ===` as `JSON.stringify` of the sheet rows. System message repeats: minimum 1,000 words, target 1,200–1,500, "FULL MANUSCRIPT AWARENESS", "NO DUPLICATE OR OVERLAPPING SCENES".
- **Worth copying:** the spreadsheet-as-story-bible layout (Story_Info / Characters / Locations / Outline_Chapter with Status column / Chapters ledger); "next chapter = last done + 1" derived from the ledger so re-running is idempotent; reading the previous chapter's *actual prose* from the doc rather than a summary.
- **Weaknesses:** the `Chapters` sheet stores only number/title/URL/date, so `extractChapterText` returns "" for every row and the "FULL STORY MANUSCRIPT RECAP" section is effectively just headers — only chapter N-1 is really in context. No loop (a human or a Schedule Trigger must re-run per chapter). No critique pass. README's "Dynamic Character Filtering" is not implemented — all characters and locations are dumped as JSON. 4,096 output tokens is tight for 1,500 words of Indonesian with heavy dialogue.

### 2.2 chi-0518/n8n-novel-generator — "AI Novel Generator: 長篇小說自動化創作系統"
https://github.com/chi-0518/n8n-novel-generator (created 2026-02-17, Traditional Chinese horror/mystery web novel)

- **Shape (14 nodes):** Manual Trigger → Supabase `Get many rows` (table `finished_chapter`, returnAll) → Sort by id → Code (`last_content`, `last_title`, `last_chapter_no`, plus `summaries[]` of every row) → AI Agent → Code (JSON extraction) → Set → Supabase `Create a row` (content, metadata, chapter_no, summary, title) → Google Docs update (insert content into one fixed doc) → **Loop Over Items** (`batchSize: 5`) whose loop output goes back to `Get many rows`.
- **Model:** `lmChatAnthropic` `claude-sonnet-4-5-20250929` (Claude Sonnet 4.5); `Supabase Vector Store` in `retrieve-as-tool` mode (table `ref_novel`, `topK: 2`, OpenAI embeddings) attached as a tool.
- **Three-tier context, stated in the system prompt as a priority order:** "1️⃣ 上一章完整內容（主線，必須直接接續）2️⃣ 已完成章節摘要（輔助，僅用於伏筆與設定一致）3️⃣ RAG 搜索結果（風格參考，不得抄襲）" — previous chapter full text (must continue directly), all prior chapter summaries (only for foreshadowing/setting consistency), RAG excerpts from a reference novel for **style only**, with an explicit ban on reusing any character names, place names, game/organisation names or recognisable world settings from the retrieved passages, and "if a RAG fragment conflicts with the current plot, the main plot wins".
- **Output contract:** JSON only `{chapter_no, title, content, summary}`; chapter ≥ 2,000 characters; summary 20–50 characters; "must end on a new hook or pressure point"; "do not rewrite, summarise or recap the previous chapter". The Code node slices from the first `{` to the last `}` and throws if `JSON.parse` fails.
- **Worth copying:** the summary column written at the same time as the chapter so the running recap is free; the priority-ordered context tiers; JSON contract with a defensive extractor.
- **Weaknesses:** loop termination is a hack (Loop Over Items only ever receives one item; the loop is effectively "run until you stop it"); there is no outline — the agent invents the next chapter each time; everything appends to one Google Doc; the "style only" RAG rule is enforced by prompt alone; no critique.

### 2.3 nagoriktech/E-Book-Generator — "AI-Powered Ebook Generator" (ATM-Labs)
https://github.com/nagoriktech/E-Book-Generator (created 2026-01-11; identical copy at nagorik-rashed/E-Book-Generator)

- **Shape (21 nodes):** Manual Trigger → Set (`Topic`, `Tone`, `Clarity Level`, `Target Mindset`, `Framing Style`, `Energy Intensity`) → `Title & Subtitle Generator` (AI Agent + Structured Output Parser) → Google Docs create ("Ebook: {title}") → Set (`Number of Chapters` = 5, `Number of Segments` = "2-4", `Number of Sub-segments` = "2-4") → `Outline Generator` (AI Agent, parser schema = JSON array of `{Chapter Number, Chapter_Name, Chapter_Sections}`, sections formatted "Section X.Y — Title / X.Y.Z: Sub-section") → Split Out → **Loop Over Items** → `Chapter Writer Agent` → Markdown → HTML → Code (strip `<h3>`/`<hr>`, fix links) → Google Sheets **append** (scratch buffer, one column "Chapter Content") → back to loop. Done branch → Limit → Sheets get rows → Aggregate → Code builds a `multipart/related` body (`{"mimeType":"application/vnd.google-apps.document"}` + full HTML with inline CSS) → HTTP Request `PATCH https://www.googleapis.com/upload/drive/v3/files/{id}?uploadType=multipart` → Sheets delete 100 rows.
- **Model:** one `lmChatOpenAi` `gpt-4.1` shared by all three agents.
- **Chapter prompt:** "Write one complete chapter at a time strictly from the outline I provide … Length: 900–1200 words. Structure: Chapter title as H1 … only outline section titles as H2 … Narrative Flow: Hook → original story with tension → transition to core lesson → conversational, research-backed teaching → organic frameworks/metaphors → practical examples & short anecdotes → emotionally uplifting close".
- **Worth copying:** the cleanest instance of the canonical shape (outline as JSON array → Split Out → Loop → write → buffer → assemble → upload); using the Drive multipart upload to replace a Google Doc's body in one call instead of the Docs node's insert-per-chapter.
- **Weaknesses:** chapters are written with **no** knowledge of each other; a shared Google Sheet as the buffer means two concurrent runs collide and the "delete 100 rows" cleanup is brittle; self-help voice ("Blend psychology, neuroscience, and realistic-sounding studies") is hard-coded; no critique.

### 2.4 Jawwad2723/n8n-book-generator — "Automated Book Generation"
https://github.com/Jawwad2723/n8n-book-generator (created 2025-09-23)

- **Intended shape (the most complete *design* found):** Manual Trigger → Set → Supabase insert `books` → If notes exist → `OpenAI - Generate Outline` → Code parse (with a fallback regex for ```json fences) → Supabase update → HTTP notify (Teams webhook) → Code `Prepare Chapter Tasks` (rows with `estimated_pages || 15`, status `pending`) → Supabase insert → **`Wait for Chapter Review`** (Wait node) → separate `Chapter Generation Trigger` webhook (`start-chapter-generation`) → Supabase get all chapters → `Process Chapters One by One` (splitInBatches) → Code `Build Chapter Context` (concatenates **summaries** of all previous chapters: "Chapter N: title\nsummary") → `OpenAI - Generate Chapters` → `OpenAI - Generate Summary` → Supabase update → If `SplitInBatches.isDone` → loop. Third webhook `final-compilation` → get all → Code `Compile Complete Book` (TOC + `# Chapter N: title` + content, computes `word_count`) → Supabase log → write DOCX → notify. Settings: `executionTimeout: -1`.
- **Reality:** never run. All three OpenAI nodes carry the *same* outline prompt; the Wait node has no outgoing connection; `Insert Chapter Records` targets the `books` table; the DOCX node is an empty `readWriteFile`. Looks LLM-generated and unexecuted.
- **Worth copying (as a design):** phases split across three triggers so each execution is short; summaries stored per chapter and re-read for context; a Wait node between outline and drafting for a human to edit the outline in the database.

### 2.5 anansh14/ai-automation-projects → ai-book-generator "The Magic Quill"
https://github.com/anansh14/ai-automation-projects/tree/main/ai-book-generator (created 2026-02-12) — a GET webhook serves an HTML reader; a POST webhook → AI Agent (`lmChatOpenRouter` `openrouter/pony-alpha`) returns one JSON with 4 chapters of 250–350 words. README's own caveat: "Be mindful of n8n.cloud timeouts for very long outputs." Toy scale, but a tidy example of the AI Agent as a strict JSON API behind `Respond to Webhook`.

### 2.6 Not what the name says
namchokGithub/n8n-novel-workflow (May 2026) is Notion→summary/tagging/Markdown export for NotebookLM, not a book writer. chi-0518/n8n-novel-azure is a Flask front-end for 2.2.

---

## 3. Write-ups, videos, forum threads

### 3.1 Jon Del Arroz, "I let AI write three complete novels" (Substack, 2026-03-16)
https://substack.aicentral.blog/p/i-let-ai-write-three-complete-novels

- Fully unattended n8n loop; the only human input was "the genre" (buddy-cop mystery, the *Precinct 99* series, now on Amazon with AI-narrated audiobooks). Generated over one weekend "while sleeping".
- **Loop stages as described:** identify next outline item → retrieve "the last 2,000 words of existing text for continuity" → generate a scene brief → draft the chapter → **self-critique** (the model "identifies weaknesses, and rewrites accordingly" — called "the most interesting part") → revise → assemble into the document.
- **Model/cost:** Claude Sonnet 4.6 via OpenRouter because it "produces the most reliable results"; roughly **$20 per novel** in API credits. Foundation documents (character sheets, world-building, prose style guide, full outline) were generated up front with Grok; covers via Grok descriptions → Nano Banana.
- **Failure modes reported:** POV inconsistencies in early chapters needed manual rewrites; book 2's outline came out "too similar to the first" because the same foundation docs were reused (fixed by having Claude write book 3's outline); a whole-manuscript analysis prompt was run afterwards to catch "continuity errors and plot holes"; the prose is "competent but slightly mechanical". No chapter counts, run times, storage details, retry handling or JSON published.

### 3.2 Kevin Farugia (typeworkflow), 5-part YouTube series "[n8n + DeepSeek] Create AI-Generated Books for Just 7 Cents" (2025-01-29 → 2025-02-03)
Part 1 https://www.youtube.com/watch?v=pKOUgncYr28 (3,359 views) · Part 2 https://www.youtube.com/watch?v=kUxsCklnRIQ · Part 3 https://www.youtube.com/watch?v=h8hlG1znPEI · Part 4 https://www.youtube.com/watch?v=EK96Rl7R-S8 · Part 5 https://www.youtube.com/watch?v=9Vc1jzdJudw

- Non-fiction, Airtable-centred: Reddit scraping for "pain points" → book ideas (Part 1) → book idea → chapters → per-chapter outlines with subtopics, saved to Airtable (Part 2) → "Looping through each chapter to generate content using AI … troubleshooting common issues like API errors and rate limits" (Part 3) → chunk chapter text and convert to cleaned HTML (Part 4) → assemble a "126-page book" into a Google Doc, "about 90-95% done" — but the final assembly is done in **Make.com** with three modules, not n8n (Part 5). Claimed cost "5-7 cents per book" with DeepSeek.

### 3.3 Etsy "One-Click Novel Generator" (commercial; Etsy blocks fetches — details are from the search-result listing text only)
https://www.etsy.com/listing/4449531165/ai-novel-writing-system-n8n-workflow-one — "generates a complete, structured 40-chapter novel by following the same stages real novels are written with: planning, memory, drafting, revision, and assembly"; ships the n8n `.json` plus author templates: Book Bible & Style Guide, Canon & Continuity, Outline Requirements, Writing Samples / Voice Library, Chapter-by-Chapter Plan, and "a glossary of n8n terms". Unverified beyond the listing.

### 3.4 n8n community threads
- "Help me write my book" (2025-03-21) https://community.n8n.io/t/help-me-write-my-book/90870 — Notion pages → HTTP fetch → loop each into an LLM for chapter naming → second LLM consolidates into 10 chapters. Problems: GPT-4 Turbo output quality and "prohibitive costs from repeated token processing during testing iterations". Advice given: switch to GPT-4o mini / Gemini Flash, put a Limit/Filter node in front while testing, consider a vector store.
- "Help building full AI eBook automation workflow (Gemini 2.5 + Drive/Slides/Sheets + FFmpeg)" (2025-09-09) https://community.n8n.io/t/help-building-full-ai-ebook-automation-workflow-gemini-2-5-google-drive-slides-sheets-ffmpeg-video/184594 — 12–15-page eBook + cover + mockups + 30 s promo video; poster stuck on "missing parameters (file names for Drive uploads, disconnected triggers)"; thread closed unresolved after 90 days.

### 3.5 Adjacent, non-n8n but useful numbers
- Entangled Text, "AI Novel Writing Workflow: Outline → Draft → Edit → KDP" (© 2026) https://www.entangledtext.com/ai-novel-writing-workflow — human-in-the-loop studio, not n8n, but its operating numbers are the sanest found: 70–90k-word target, chapter summaries capped at ≤200 words, story bible that "fits on a few screens", review after each chapter or at least every 5–8 chapters; explicit warning that whole-book regeneration without review produces "unpublishable mush" and that "continuity debt compounds faster with AI than human drafting".

---

## 4. How n8n's own machinery gets used (and where it bites)

**Loop Over Items (Split in Batches)** — https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches/
Two outputs: `loop` (current batch) and `done` (everything, combined, after the last batch). `{{$("Loop Over Items").context["noItemsLeft"]}}` and `["currentRunIndex"]` are the exposed counters; the docs warn "If your termination condition never matches, your workflow execution will get stuck in an infinite loop." Every chapter pipeline above uses batch size 1 and wires the last node of the chapter back into the loop node. The `done` output is the trap: a Cloud user on 1.105.4 reported a consistent "Connection Lost" crash exactly when the done branch fired after ~200 items in batches of 20 (https://community.n8n.io/t/memory-issue-with-loop-over-items-node-done-branch/167862, 2025-08-19) — the done branch materialises all processed items at once. Practical rule from the working pipelines: write each chapter to storage *inside* the loop and let `done` carry only ids.

**Sub-workflows (Execute Sub-workflow)** — https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/
Modes "Run once with all items" / "Run once for each item"; "Wait for sub-workflow completion" toggle; input contract defined on the "When Executed by Another Workflow" trigger (fields / JSON example / accept all). The memory doc (https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/fix-memory-issues) prescribes Loop Over Items + Execute Workflow because "the sub-workflow only holds the data for the current batch in memory, after which the memory is free again", and gives the scale hint "instead of processing 10,000 rows per execution, reduce to 200". Caveat from the convert-to-sub-workflow page: "Limited support exists for AI tools within sub-workflows" and new sub-workflows default to v1 execution order. None of the found book workflows use sub-workflows for chapters; the ones that avoid memory problems do it by making each chapter its own *execution* (webhook per action, one chapter per run).

**Wait node / human-in-the-loop** — https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/
Resume modes: after interval, at time, on webhook (`$execution.resumeUrl`), on form submitted; optional "limit wait time". "For wait times less than 65 seconds, the workflow doesn't offload execution data to the database" — above that, the execution is persisted and the process freed, which is what makes a days-long "wait for the author to approve the outline" viable. For agent tool calls, n8n's Human review (https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools) pauses before a tool runs and routes an approve/deny to Chat, Slack, Discord, Telegram, Teams, Gmail, WhatsApp, Google Chat or Outlook, with `$tool.name` / `$tool.parameters` available for the message; the "Send and Wait for Response" operations offer Approval, Free Text or Custom Form replies (blog, 2026-01-16: https://blog.n8n.io/human-in-the-loop-automation/). Only the Jawwad2723 skeleton places a Wait between outline and drafting; Agniva's Airtable Action field is the pragmatic equivalent.

**AI Agent, AI Agent Tool, MCP Client Tool** — https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/ , https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/
All agents are Tools Agents since 1.82 (agent-type selector removed in 3.0). Template 7482 is the only book workflow using `agentTool` (an agent as another agent's tool, prompt via `$fromAI()`); chi-0518 attaches a vector store as a tool. The MCP Client Tool takes an SSE endpoint, bearer/header/multi-header/OAuth2 auth, and tool selection All / Selected / All Except — **no book or novel workflow using MCP Client was found**; the searches surface only generic "n8n as MCP server" guides. Known agent hazard: intermittent infinite tool-calling loops reported on 1.81 (GitHub #13525, closed stale), relevant to any writer/editor loop that lets the agent call tools freely. Prompt caching is exposed on the Anthropic Chat Model node (Disabled / 5 minutes / 1 hour), which matters when the same story bible is resent every chapter.

**State: Data Tables vs external stores** — https://docs.n8n.io/build/work-with-data/data-tables
Data Tables shipped 2025-09-23 (available from 1.113.1 per https://betazeta.dev/blog/n8n-data-tables/): insert/get/update/upsert/delete rows, "if row exists" checks; default cap **200 MiB per instance** (`N8N_DATA_TABLES_MAX_SIZE_BYTES` on self-hosted), project-scoped, "Direct programmatic access to data tables from a Code node isn't supported", meant for "light to moderate data storage". A 90k-word manuscript is under 1 MB of text, so size is not the issue; the Code-node restriction is. Every real pipeline found still uses Google Sheets (yegisyahrial, nagorik), Airtable (Agniva, Farugia), Supabase (chi-0518, Jawwad2723) or Notion.

**Error workflows** — https://docs.n8n.io/build/flow-logic/handle-errors-gracefully
Separate workflow starting with Error Trigger, selected under Options → Settings → Error workflow; receives execution id/url/retry flag/error message/stack/`lastNodeExecuted`/mode plus workflow id and name; `execution.id`/`url` are absent if the trigger itself failed. None of the found book workflows define one; chi-0518's JSON-extractor Code node throws on parse failure, which would be the natural hand-off point.

**Execution time limits** — https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions and https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/configure-workflow-timeouts
Self-hosted: `EXECUTIONS_TIMEOUT` default `-1` (none); `EXECUTIONS_TIMEOUT_MAX` default `3600` s is the ceiling a per-workflow setting may use; `N8N_AI_TIMEOUT_MAX` default `3,600,000` ms for AI/LLM node HTTP calls; `EXECUTIONS_DATA_MAX_AGE` default 336 h with pruning on; on timeout the main process does a "soft timeout (takes effect after the current node finishes)". Cloud: "Cloud caps the maximum value you can pick per plan … env vars are not exposed there" and "The per-plan ceiling is not published as a number" (n8n staff, 2026-07-13, https://community.n8n.io/t/maximum-workflow-execution-timeout-on-n8n-cloud-trial-starter-and-pro/303146); the old 5-minute limit is "outdated" and workflows running 1+ hour on Starter are confirmed (2026-03-13, https://community.n8n.io/t/are-there-workflow-execution-time-limits/276736). Because the timeout is off by default, a 40-chapter sequential run is time-legal; the memory doc's advice for Cloud is simply "upgrade to larger plans".

**Memory and big prompts** — https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/fix-memory-issues
Drivers: JSON volume, binary size, node count, Code nodes, *manual executions* (they copy data to the front end), concurrency; self-hosted fix `NODE_OPTIONS=--max-old-space-size=…`. Community datapoint: ~30,000-token inputs to Basic LLM Chain / AI Agent / Gemini nodes pegged CPU and crashed 6 GB instances on 1.95.1–1.97.1; the workaround that worked was calling the model with a plain HTTP Request node (https://community.n8n.io/t/n8n-workflow-crashing-on-large-text-input-to-llm-node-high-cpu/99788, Apr–Jun 2025). This is directly relevant to "send the whole manuscript so far" prompts.

**Cost** — the two real datapoints are Farugia's "5-7 cents per book" (DeepSeek, non-fiction, early 2025) and Del Arroz's "~$20 per novel" (Claude Sonnet 4.6, with critique + revision passes, 2026). The forum's standard advice for iteration cost is a Limit node before the loop and a cheap model until prompts settle.

---

## 5. Patterns worth copying

1. **Outline as a JSON array → Split Out → Loop Over Items (batch 1) → write → persist inside the loop → assemble from storage.** nagorik's Sheets-buffer + Drive multipart PATCH is the tidiest assembly; Jawwad2723's `Compile Complete Book` Code node (TOC + `# Chapter N` + `---`) is the simplest.
2. **A ledger table with a Status column and "next = last done + 1" logic** (yegisyahrial) so a crashed or timed-out run can be re-fired and resumes at the right chapter with nothing duplicated.
3. **One execution per chapter or per phase, triggered by webhook/schedule** (Agniva, Farugia, Jawwad2723's three webhooks) instead of one giant execution — sidesteps both Cloud ceilings and the done-branch memory pile-up.
4. **Three-tier context with a stated priority** (chi-0518): previous chapter verbatim > all chapter summaries > style exemplars, plus the rule that the main plot wins on conflict.
5. **Write the chapter summary in the same call as the chapter** (chi-0518's `{content, summary}` JSON; Jawwad2723's separate `Generate Summary` node) so the running recap costs nothing extra.
6. **Editor returns machine-readable `status` + `edits`, If node loops back to the writer** (Matty Reed) — add a `currentRunIndex`-style counter or a Set-node iteration cap, which none of the samples do.
7. **Word budgets per beat inside the chapter prompt** (yegisyahrial's ~250/400/350/200 phases) reliably land 1,000–1,500-word chapters on flash-tier models; nagorik's 900–1,200 and anansh14's 250–350 per chapter show the per-call sweet spot most builders converge on.
8. **Structured Output Parser after every planning stage** (Dikhtiar's 10-stage chain, Trung Tran's book_brief/cover_brief/writing_brief) so downstream Set/Code nodes can address fields by name.
9. **Prompt caching on the Anthropic node (5 min / 1 h)** when the same bible + style guide precede every chapter.

## 6. Pitfalls seen in the wild

- Writing the whole book in one completion (7482, anansh14): output caps and quality collapse; the 10,000-word target in 7482 cannot be met by gpt-4.1-mini in one call.
- Chapters generated with no knowledge of each other (5707, 2879, nagorik) — fine for a how-to eBook, fatal for fiction.
- "Full manuscript recap" that is silently empty because the ledger stores URLs, not text (yegisyahrial).
- A new Google Doc per chapter and a `done` output wired to nothing (5707) — no book ever gets assembled.
- Loop Over Items used as a "run forever" switch with no termination condition (chi-0518), and writer/editor loops with no iteration cap (3503).
- Shared Google Sheet as scratch buffer with a blanket "delete 100 rows" (nagorik) — concurrent runs corrupt each other.
- Sending 30k-token contexts through the LangChain nodes on a small instance — CPU/memory crash; use HTTP Request or trim to last chapter + summaries.
- Testing the loop against the full dataset with a frontier model (forum thread 90870) — put a Limit node in front and iterate on a cheap model first.
- Reusing the same foundation docs for sequels produced a near-duplicate outline (Del Arroz) — regenerate the outline with a different model or explicit "differ from book 1" constraints.
- Manual executions copy all execution data to the browser — never drive a 40-chapter run from "Execute workflow" on the canvas; use a production trigger.
- Skeleton repos that look complete but were never run (Jawwad2723: identical prompts in three nodes, disconnected Wait) — read the JSON before trusting a README.

---

## Source list

| # | Source | Type | Fetched as |
|---|---|---|---|
| 1 | https://n8n.io/workflows/7482-… | n8n template | page + `api.n8n.io/api/templates/workflows/7482` JSON |
| 2 | https://n8n.io/workflows/2879-… | n8n template | page + JSON |
| 3 | https://n8n.io/workflows/5707-… | n8n template | page + JSON |
| 4 | https://n8n.io/workflows/3503-… | n8n template | page + JSON (params stripped) |
| 5 | https://n8n.io/workflows/3153-… | n8n template | page + JSON (params stripped) |
| 6 | https://n8n.io/workflows/4492-… | n8n template (paid) | page |
| 7 | https://github.com/yegisyahrial/n8n-ai-auto-novel-generator | GitHub | README + `ai_novel_generator.json` |
| 8 | https://github.com/chi-0518/n8n-novel-generator | GitHub | README + `system_prompt.md` + `AI_novel_generator_v1.json` |
| 9 | https://github.com/nagoriktech/E-Book-Generator | GitHub | README + `Ebook Generator.json` |
| 10 | https://github.com/Jawwad2723/n8n-book-generator | GitHub | `Automated Book Generation.json` |
| 11 | https://github.com/anansh14/ai-automation-projects/tree/main/ai-book-generator | GitHub | README + `workflow.json` |
| 12 | https://substack.aicentral.blog/p/i-let-ai-write-three-complete-novels | blog | page |
| 13 | YouTube pKOUgncYr28, kUxsCklnRIQ, h8hlG1znPEI, EK96Rl7R-S8, 9Vc1jzdJudw | video descriptions | page HTML |
| 14 | https://www.etsy.com/listing/4449531165/… | commercial listing | search-result snippet only (403 on fetch) |
| 15 | https://community.n8n.io/t/help-me-write-my-book/90870 | forum | page |
| 16 | https://community.n8n.io/t/…/184594 | forum | page |
| 17 | https://community.n8n.io/t/memory-issue-with-loop-over-items-node-done-branch/167862 | forum | page |
| 18 | https://community.n8n.io/t/n8n-workflow-crashing-on-large-text-input-to-llm-node-high-cpu/99788 | forum | page |
| 19 | https://community.n8n.io/t/maximum-workflow-execution-timeout-on-n8n-cloud-trial-starter-and-pro/303146 | forum | page |
| 20 | https://community.n8n.io/t/are-there-workflow-execution-time-limits/276736 | forum | page |
| 21 | https://github.com/n8n-io/n8n/issues/13525 | GitHub issue | page |
| 22 | n8n docs: splitinbatches, executeworkflow, wait, human-in-the-loop-for-tools, agent, toolmcp, data-tables, handle-errors-gracefully, executions env vars, configure-workflow-timeouts, fix-memory-issues | docs | pages |
| 23 | https://blog.n8n.io/human-in-the-loop-automation/ | n8n blog | page |
| 24 | https://betazeta.dev/blog/n8n-data-tables/ | blog | page |
| 25 | https://www.entangledtext.com/ai-novel-writing-workflow | blog (non-n8n) | page |
