> **Status (2026-09-13).** This is the design of the book pipeline: the ten check
> passes, the book memory, the three-round cap. `.claude/workflows/book-chapter.js`
> implements it in Claude Code, on the subscription. The n8n transport described
> below needs an Anthropic API key that does not exist and is not coming; do not
> build toward it. The research notes are in `research/` beside this file.

# BOOK_PIPELINE.md — the War of the Realms book pipeline on n8n

Design document, 2026-09-12; reviewed against the research notes, `build/mcp_server.py`, `build/verify.py` and `desktop/NATALIE.md` the same day. Written for the builder in the next session. Nothing in this file has been built; the numbers are estimates from the repo inventory and the research notes, and each is marked as such. Anything marked **to verify** is a claim the research does not settle; check it on the first run before relying on it.

Isaac's brief, in his words: "My idea eventually not to just write Roleplay scenes, but to produce entire books. I want to make an n8n thing that pulls from this that has the beauty of being checked multiple times."

What this design was checked against:

- the running n8n (2.38.6, `C:\Users\isaac\Documents\n8n\docker-compose.yml`: n8n, qdrant, open-webui, pipelines; no Postgres; no repo mount inside the container);
- the WOTR MCP (`build/mcp_server.py`, 44 tools) and its `--http` mode, read at source;
- the repo inventory (`scratchpad/n8n_research/repo_inventory.md`);
- four research notes in the same folder: `n8n-book-workflows.md`, `multi-pass-fiction.md`, `claude-orchestration.md`, `open-source-book-agents.md`. Links are given where a choice comes from one of them.

Jargon is glossed at first use. "n8n" is the workflow tool; a "node" is one box on its canvas; an "execution" is one run of a workflow; a "sub-workflow" is a workflow another workflow calls. "MCP" is the Model Context Protocol, the interface the WOTR server speaks; "MCP Client" is the n8n node that calls one of its tools.

---

## 0. The shape

One chapter per execution. Each chapter goes through five stages in order: **brief, draft, check, revise, commit**. The checks are the point. Deterministic passes that cost nothing run first, then five model critics that each hunt one class of fault and must quote their evidence, then a revise loop capped at three rounds, then a human gate on a schedule Isaac sets. Prose reaches `scenes/` through `archive_scene` only after the gate. Book memory (facts with quotes, hooks with due chapters, chapter summaries) lives in n8n Data Tables and is written only after the gate. Assembly is the repo's existing path (`ARCS.md` → `build/arcs_export.py` → docx and epub in Drive) plus narration through `cast_scene` and `narrate_scene`.

```
WF-0 Book Foundation (once)     WF-1 Dispatcher (every 10 min)        WF-3 Book Audit (every 5 ch, every 3 mid-book, and at the end)
  form → planner → outline         next planned chapter?  ──────►  WF-2 Chapter Pipeline (sub-workflow, one chapter)
  → Data Tables → Isaac approves     lock it, fire WF-2                 A BRIEF   MCP: load_rules, check_docket, scene_brief,
WF-0b Planner (revise) (sub-workflow, called by WF-0 and WF-2)                    scene_text (prev tail), character/fow_line,
                                                                                  scene_recall, wiki; Data Tables: summaries,
                                                                                  facts, hooks, overrides
                                                                        B DRAFT   AI Agent (Opus 5, cached system, 5 read tools)
                                                                        C CHECK   verify_scene, gap_fill, voice_check, ledger code,
                                                                                  5 critics (Sonnet 5, evidence-quoting JSON)
                                                                        D REVISE  ≤3 rounds, diff guard, monotone acceptance
                                                                        E GATE    review policy → Gmail approve / instruct / drop
                                                                        F COMMIT  archive_scene → extractor → facts/hooks/summary
                                                                                  → ledger_add, advance_front, session_end,
                                                                                  arcs_place → WF-4 Deliver (epub, docx, audio)
WF-E Error workflow: mark the stage failed, notify Isaac, the dispatcher retries from the last checkpoint
```

Eight principles, each with the reason it is there:

1. **One chapter per execution, never one book per execution.** The Loop Over Items "done" branch materialises every processed item and crashed n8n Cloud at ~200 items ([community, Aug 2025](https://community.n8n.io/t/memory-issue-with-loop-over-items-node-done-branch/167862)); every working book pipeline found persists each chapter inside the loop and makes each chapter or phase its own execution (Agniva's [template 2879](https://n8n.io/workflows/2879-book-ghostwriting-and-research-ai-agent/), Jawwad2723's three webhooks, yegisyahrial's one-chapter-per-run).
2. **Every model call finishes in a few minutes and asks for at most 16k output tokens.** Neither the Anthropic Chat Model node nor the HTTP Request node streams ([issue #23851](https://github.com/n8n-io/n8n/issues/23851)), and Anthropic's SDK refuses non-streaming requests it expects to run past ten minutes ([API errors](https://platform.claude.com/docs/en/api/errors)). The SDK's guard is computed from `max_tokens` alone (an hour per 128k tokens, so the refusal starts at roughly 21,300 tokens; **to verify** against the SDK version the node ships). 16,000 sits under it with room; do not raise it past 20,000. A chapter is one draft call, not one book call.
3. **The static context is sent once and cached.** Prompt caching (Anthropic re-uses a stored prefix at 10% of the input price) is on the Anthropic Chat Model node from node v1.6 / n8n 2.37.0 ([PR #34482](https://github.com/n8n-io/n8n/pull/34482)); the running instance is 2.38.6. The loadout for a scene type is 12–19k tokens and identical for every chapter of that type until a pack changes.
4. **Deterministic checks before any model; model critics are narrow and must quote.** Category-scoped extraction with quoted contradiction pairs scored F1 0.68 against human experts' 0.23 ([ConStory-Bench](https://arxiv.org/abs/2603.05890)); a holistic 1–10 judge agrees with human preference only 66–73% and its rubric wording alone predicts the verdict 67–90% of the time ([LitBench](https://arxiv.org/abs/2507.00769), [rubric artifacts](https://arxiv.org/html/2609.02942)). So: no score gate anywhere. FAIL blocks, WARN reports, both carry a quote.
5. **Revision is bounded at three rounds, accepted only if it does not regress, with structure frozen.** Every measured system plateaus by round three and degrades after four ([LLM Review](https://arxiv.org/html/2601.08003), [Dramaturge](https://arxiv.org/html/2510.05188v3) N_max = 3, [Claude-Book](https://github.com/ThomasHoussin/Claude-Book) max 3); uncoordinated revision introduces new inconsistencies; revisions that score lower are discarded ([AuthorAgent](https://github.com/Ckokoski/AuthorAgent)).
6. **State is written only after the gate; validators are read-only; one writer writes.** ([Claude-Book](https://github.com/ThomasHoussin/Claude-Book), [Magnet](https://arxiv.org/html/2607.00918): rejected proposals never touch world state.)
7. **A human override is persisted with its reason** so a deliberate lie, an unreliable narrator or foreshadowing stops being re-raised ([Novel-OS](https://github.com/mrigankad/Novel-OS)). NATALIE requires a lie per session (Table Rule 8) and a misreading per scene (R6-4), so this is not optional.
8. **Every stage is idempotent** (safe to run twice) and checkpointed by `job_id`, so a crash resumes at the last good stage instead of re-spending tokens ([community pattern for long AI workflows](https://community.n8n.io/t/way-to-handle-long-running-ai-workflows-in-n8n-without-execution-timeouts/295656)).

The unit of prose stays the **scene file**, because that is what `archive_scene`, `ARCS.md`, `arcs_export.py`, `cast_scene` and `narrate_scene` all understand. A chapter is one scene file of 2,500–4,500 words (the archive median is 3,235), titled `Chapter NN — <title>`. In `verify.py`'s terms a chapter is always the `set-piece` band (floor 2,500, no ceiling); the `conversational` and `standard` bands are turn lengths and never describe a chapter. The repo has no chapter concept today; the outline in the Data Tables supplies it.

**What NATALIE was written for and what a book is.** `desktop/NATALIE.md` is a table protocol: Isaac drives his player character, Natalie drives everything else, and Table Rule 1 is a turn-taking rule ("answer what the PC did … never resolve a multi-decision action in one go"). A chapter has no turn to answer and the pipeline will, by construction, write the PC's actions. §7 item 19 states the default this design takes and marks it as Isaac's to overrule; nothing below silently assumes it.

---

## 1. The pipeline as stages, with the n8n nodes

### 1.0 Plumbing that has to exist before any workflow

**A second MCP process.** Port 8765 is the public read-only server (`--public`, 27 tools, bearer token). The pipeline needs the writing tools, so it gets its own process: a scheduled task "WOTR MCP pipeline" running `pythonw.exe build/mcp_server.py --http --port 8766 --log build/mcp_pipeline.log`. That binds 127.0.0.1, no token, all 44 tools. Endpoint from inside the n8n container: `http://host.docker.internal:8766/mcp` (the compose file already sets `extra_hosts: host.docker.internal:host-gateway`).

**The Host-header check, found at source.** In untokened `--http` mode `mcp_server.py` calls `server.run(transport="streamable-http", host="127.0.0.1", ...)` with no `transport_security`, and the MCP SDK then switches on DNS-rebinding protection with `allowed_hosts = ["127.0.0.1:*", "localhost:*", "[::1]:*"]` (the public mode disables it explicitly for the same reason, see the comment above `with_token_gate`). A request from the container carries `Host: host.docker.internal:8766` and is answered **421 "Invalid Host header"** before it reaches the MCP transport. So even when the network hop works, every MCP Client call fails until the server allows that host. The fix is in Appendix A (`allowed_hosts`, four lines) and is needed before anything else; it is not optional.

**Reachability test, first thing.** Nothing in the repo has exercised the container-to-loopback hop; the compose file points `OLLAMA_HOST` at `host.docker.internal:11434`, which is the same hop, but whether that Ollama is bound to loopback or all interfaces is not recorded (**to verify**). Run `docker exec <n8n container name from docker ps> wget -S -O- http://host.docker.internal:8766/mcp` and read the status: **406 or 405** means the hop works and the server is talking (it wants a POST with the MCP `Accept` headers); **421** means the Host check above is still on; **"Connection refused"** means the Docker gateway is not forwarding to loopback, and the fix is a `--bind 0.0.0.0` flag on `mcp_server.py` (six lines) plus a Windows firewall rule limited to the Docker subnet. Do not bind the untokened server to all interfaces without that rule.

**n8n settings.** Leave `EXECUTIONS_TIMEOUT` at its default -1 (no timeout; [executions env vars](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions)). Turn on **Save Execution Progress** in workflow settings only while debugging. Add the Anthropic API key as an n8n credential (never in the compose env). Add a Gmail credential for the human gates (or Telegram; see §7).

**Data Tables** (n8n's built-in tables, project-scoped, 200 MiB per instance, no Code-node access; [docs](https://docs.n8n.io/build/work-with-data/data-tables)): `books`, `chapters`, `stages`, `facts`, `hooks`, `overrides`, `findings`. Schemas in Appendix B. Prose goes into `stages` rows only while a chapter is in flight and is cleared at commit; `scenes/` is the archive. Two limits of the Get node's filters shape the design below: the operators are Equals / Not Equals / Greater / Less / Is Empty with Must Match Any/All, so there is no `in` and no `<=`; and a filter cannot take a list that varies per run (a cast of three today, five tomorrow). Where the text below says "where `subject` is in the cast", the node fetches every row for the book and a Code node filters.

**MCP Client nodes, standing settings.** Transport: HTTP Streamable. If the node keeps sending SSE-style GETs (the [#24967](https://github.com/n8n-io/n8n/issues/24967) bug produced 97.6 million failed requests for one user), set the `serverTransport` parameter as an expression to the literal `httpStreamable` and check `build/mcp_pipeline.log` for POSTs. Retry On Fail: 3 tries × 5,000 ms. On Error: Stop Workflow. Never "Continue", because that silently disables the retries ([issue #10763](https://github.com/n8n-io/n8n/issues/10763)). Timeout: 120,000 ms on read tools, 300,000 ms on the write tools that commit and push, 900,000 ms on `sync_now` (its script has a 900 s ceiling). Build every tool-argument object in a Code node and pass it to the MCP Client node as one JSON expression (`{{ $json.args }}`); never splice a chapter into a JSON template by hand, because the quotes and newlines in 4,000 words of prose break the template.

**Anthropic Chat Model nodes, standing settings.** Enable Prompt Caching: on, Cache TTL: 1 hour (the TTL clock starts at request start, and a chapter run spans 15–20 minutes of hops; [prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)). Thinking Mode: Adaptive, with the Effort dropdown (node v1.5, [PR #29467](https://github.com/n8n-io/n8n/pull/29467)). Maximum Number of Tokens: 16,000 on the writer and reviser, 4,000 on critics. Retry On Fail 3 × 5,000 ms; On Error Stop. The exact option labels come from the two PRs, not from a docs page; **to verify** on the node itself.

**Which root node for a model call.** The AI Agent node is used where tools are attached (planner, writer, Canon critic). For calls with no tools (four critics, the extractor, the caster, the continuity auditor) use the **Basic LLM Chain** node with Require Specific Output Format and a Structured Output Parser; the research notes record that the AI Agent node expects at least one tool sub-node, and the chain node is the documented no-tool shape (template 5707 uses it). **To verify**: if the AI Agent node on 2.38.6 runs with no tool attached, either node works and the choice is cosmetic. Prompt caching lives on the Chat Model sub-node, so it applies under both.

### 1.1 The workflows

| id | name | trigger | what it does | runs |
|---|---|---|---|---|
| WF-0 | Book Foundation | n8n Form Trigger | premise → planner → outline rows → Isaac approves | once per book |
| WF-0b | Planner (revise) | When Executed by Another Workflow | re-plans the remaining chapters from Isaac's notes; called by WF-0's `edit` branch and WF-2's `drop` branch | on demand |
| WF-1 | Chapter Dispatcher | Schedule Trigger, every 10 min | finds the next planned chapter, locks it, fires WF-2; sends the daily reminder when a chapter is waiting on Isaac | continuously while a book is active |
| WF-2 | Chapter Pipeline | When Executed by Another Workflow | brief → draft → check → revise → gate → commit for one chapter | once per chapter, ~15–20 min of machine time |
| WF-3 | Book Audit | Execute Sub-workflow from WF-2 / WF-1 | cross-chapter ledger audit and continuity audit; whole-manuscript review at the end | every 5th chapter (every 3rd in the middle band), and at the end |
| WF-4 | Deliver | Execute Sub-workflow from WF-2 / WF-1 | ARCS placement is done in WF-2; here: cast, narrate, `sync_now` export, digest | per chapter (audio) and per book (epub, docx) |
| WF-E | Error | Error Trigger | mark the stage failed, reset the chapter for retry, notify Isaac | on any failure |

Why a dispatcher on a schedule instead of chaining chapters: the schedule is a production trigger (manual "Execute workflow" copies all execution data to the browser and is a documented memory driver; [fix memory issues](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/fix-memory-issues)); each chapter gets its own execution and its own memory; a crashed chapter is picked up again on the next tick from its last checkpoint; and Isaac can pause the whole book by setting `books.status` to `paused`.

### 1.2 WF-0 Book Foundation

1. **Form Trigger "New book"**: title; thread (dropdown: Sodoku Moto, Hild Ice, Kwon Mu-jin, Ilthára Korvaeth, the four `session_start` accepts); culture (dropdown: Kharven, accord, dawi, eresse, expanse, korvaeth, moto); premise (textarea, Isaac's words, 100–400 words); POV cast (comma list); target chapters (number, default 25); target words per chapter (default 3,500); review mode (dropdown: `every`, `first3_then_5`, `escalations_only`; default `first3_then_5`).
2. **Data Table Insert `books`** (status `planning`).
3. **MCP Client `session_start(thread, "standard", culture)`**: State of Play, Ledger, Fronts as clocks, what comes due, inventory, the standard loadout. ~20–27k tokens, once. → **Code**: split on the `---` separators; store the `# STANDING INVENTORY` block in `books.inventory` (it is the only per-chapter source of the inventory text, since no MCP tool returns it alone; Appendix A proposes one) and a hash of the State of Play block in `books.state_hash` (§7 item 12).
4. **MCP Client `fronts(thread)`**, **`due(1, thread)`**, **`list_conflicts()`**, **`check_docket(["prose-law","pov","scene-structure","dialogue","register"])`**.
5. **Loop Over Items** over the POV cast → **MCP Client `character(name)`** → **Aggregate**.
6. **AI Agent "Planner"** (Anthropic Chat Model `claude-opus-5`, Effort high, prompt caching on; tools: MCP Client Tool with Tools to Include = Selected: `wiki`, `character`, `scene_recall`, `fronts`; Max Iterations 12; Require Specific Output Format → Structured Output Parser). The planner's job is to derive the book's spine from the table, not invent one: each chapter ticks a named Front (Table Rule 4; the twelve Fronts have written tick consequences and all sit at position 0, so the book is what moves them), pays what the Ledger says comes due, and carries hooks with plant and pay chapters ([story-skills](https://github.com/danjdewhurst/story-skills) promises, [InkOS](https://dev.to/dylan_brown_4c803aefcfe51/building-an-autonomous-ai-agent-that-writes-novels-architecture-of-a-10-agent-pipeline-59pf) hook agenda). Output per chapter: `number, title, beat (2–4 sentences), scene_type (one of the seven), culture, band (always set-piece for a chapter), pov, cast[], front_id, plants[], pays[], time_elapsed, target_words`. Output per hook: `hook_id, text, keywords[] (3–5 words the payoff must contain; Pass 4 greps for them), planted_ch, due_ch`. The planner also returns `voice_note`: 150 words on what this book's narration does that the archive does not, with one exemplar paragraph and one anti-exemplar, the way [AutoNovel](https://github.com/NousResearch/autonovel) keeps exemplars and anti-exemplars in `voice.md`.
7. **Code "explode outline"** → one item per chapter.
8. **Data Table Insert `chapters`** (status `planned`) and **Insert `hooks`** (status `planned`, `planted_ch`, `due_ch`, `keywords`).
9. **Data Table Update `books`** (status `outline_review`, `voice_note`, `bible` = premise + cast + voice note).
10. **Gmail "Send and Wait for Response"**, response type Custom Form: `approve` / `edit` (free text) / `reject`. The execution parks in the database until Isaac answers (waits over 65 s are offloaded; [Wait docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)). Limit Wait Time: 14 days (**to verify** that the Send-and-Wait operation exposes the limit the way the Wait node does; if not, follow it with a Wait node).
11. **Switch** on the answer: `approve` → `books.status = active`; `edit` → **Execute Sub-workflow WF-0b** with Isaac's notes, back to step 7, at most twice, then stop and ask again; `reject` → `books.status = dropped`.

WF-0b is the planner call of step 6 with the existing outline, the chapters already `done`, and Isaac's notes as input, returning replacement rows for chapters not yet done. It is its own workflow because a Form-triggered workflow cannot be entered part-way by another workflow.

Del Arroz's second book came out too similar to his first because the same foundation documents were reused ([Substack, Mar 2026](https://substack.aicentral.blog/p/i-let-ai-write-three-complete-novels)); the planner prompt therefore receives the titles and one-line summaries of every earlier book on the same thread with the instruction to differ in spine, not just in surface.

### 1.3 WF-1 Chapter Dispatcher

1. **Schedule Trigger**, cron `5,15,25,35,45,55 * * * *`, so it never coincides with the hourly `WOTR wiki sync` task at the top of the hour (that task does `git pull --rebase` then push; the pipeline's `archive_scene` also pushes; see §7).
2. **Data Table Get `books`** where `status = active`, limit 1. None → stop.
3. **Data Table Get `chapters`** where `book_id` = X and `status = running`. If one exists and `started_at` is older than 120 minutes, it is a stale lock: Update `status = planned`, `retry_count + 1`; if `retry_count > 2`, `status = failed` and notify. If one exists and is fresh → stop (one chapter at a time).
4. **Data Table Get `chapters`** where `status = awaiting_isaac`. Any → if `last_reminder` is empty or older than 24 h, send the reminder mail and set `last_reminder`; then stop (never run ahead of a pending decision; Entangled Text's warning that unreviewed regeneration yields "unpublishable mush" ([link](https://www.entangledtext.com/ai-novel-writing-workflow))).
5. **Data Table Get `chapters`** where `status = planned`, Order By `number` asc, Limit 1. None → `books.status = drafted` → **Execute Sub-workflow WF-3** (final audit) and **WF-4** (book export) → stop.
6. **Data Table Update** that chapter: `status = running`, `started_at = now`, and `job_id = {{$execution.id}}` **only if `job_id` is empty**. On a retry the existing `job_id` is kept; that is what lets WF-2 find its `stages` checkpoints. (A fresh id per attempt would make every retry a full re-spend.)
7. **Execute Sub-workflow WF-2**, Wait For Sub-Workflow Completion **off**, input `{book_id, chapter_no, job_id}`.

"Next = last done + 1" is yegisyahrial's idempotent ledger rule ([repo](https://github.com/yegisyahrial/n8n-ai-auto-novel-generator)); the `running` lock with a stale timeout is what he lacked.

### 1.4 WF-2 Chapter Pipeline

Every stage begins with **Data Table "If Row Exists"** on `stages` where `job_id` and `stage` match and `status = done`; if it exists the stage is skipped and its `output` re-read. Every stage ends with **Data Table Upsert `stages`** `{job_id, stage, status: done, output}`. That is the checkpoint.

**Stage A, BRIEF.** Nodes, in order:

- **Data Table Get** `chapters` (this row), `books` (bible, inventory, voice note, review mode), `chapters` where `book_id` = X and `status = done` (all prior, for summaries, ordered by number), `hooks` where `book_id` = X and (`status = planted` or `status = advanced`, Match Any) and `due_ch < chapter_no + 3` (the hook agenda), `facts` where `book_id` = X (then a Code node keeps rows whose `subject` is in the cast or whose `place` is this chapter's place, newest first, at most 40), `overrides` for this book.
- **Code "loadout tags"**: the seven `LOADOUTS` from `mcp_server.py` as a map from `scene_type` to tags (duel: prose-law combat adjudication magic-mechanism pov; battle: prose-law mass-combat adjudication pov scene-structure; talky: prose-law dialogue register pov naming; quiet: prose-law pov scene-structure standing-inventory register; explicit: prose-law dialogue pov scene-structure; working: prose-law magic-mechanism combat codex; standard: prose-law pov scene-structure dialogue register). Checked against the source on 2026-09-12; re-check if `mcp_server.py` changes.
- **MCP Client `load_rules(tags, brief=true)`**. Deterministic, same input → same text (the header lists the tags sorted, the rules sort newest pack first), which is what makes the cache hit. 12.5–19.4k tokens by type.
- **MCP Client `check_docket(tags)`** → **Code**: if any pending or proposed rule is returned and no `overrides` row names it, set `escalate_before_draft = true` with the docket text. NATALIE: "If one would materially change what you are about to write, ask Isaac before writing."
- **MCP Client `scene_brief(beat, thread, scene_type, culture, characters)`** → **Code**: keep everything from `## Fill before drafting` up to `## Rule loadout` (the blanks and the FOW lines); cut from `## Rule loadout` onward (the loadout is already in the system block, and sending it twice is the triple-send the inventory warns about).
- **MCP Client `scene_text(previous chapter's scene file)`** → **Code "tail"**: drop the two header lines the tool prepends (`scene file: …`, `cast file: …`) and the blank line after them, then keep the last 1,500 words, cut at a paragraph boundary. Raw tail, not a summary, so voice carries ([AutoNovel](https://github.com/NousResearch/autonovel) passes the last ~1,000 words; Del Arroz 2,000). Chapter 1 gets "This is the first chapter."
- **Loop Over Items** over the cast → **If** first appearance in this book (no `facts` row with that subject) → **MCP Client `character(name)`** (full card, capped at 6,000 characters by a Code node) else **MCP Client `fow_line(name)`** → **Aggregate**.
- **MCP Client `scene_recall(beat keywords)`** and **`scene_recall(cast + place)`**; **MCP Client `wiki(term)`** for capitalised terms in the beat that are not cast names (Code extracts them; at most two calls).
- **Code "assemble context"** builds two strings: `system_static` (protocol + inventory + loadout + docket digest + book bible; byte-identical for every chapter of this scene type in this book) and `user_dynamic` (everything that varies). The trimming order when `user_dynamic` passes 40k tokens: drop wiki snippets, then the second `scene_recall`, then full cards down to FOW lines, then collapse summaries older than ten chapters to their first sentence. Never trim the previous tail, the brief blanks, or the hook agenda. (Sudowrite publishes a truncation order and drops worldbuilding first; [docs](https://docs.sudowrite.com/using-sudowrite/1ow1qkGqof9rtcyGnrWUBS/chapter-continuity/4KL8gFeLZQ6GSBjDWtSbV6).)
- If `escalate_before_draft` → jump to Stage E with reason `docket`.

**Stage B, DRAFT.**

- **AI Agent "Writer"**: Anthropic Chat Model `claude-opus-5`, Maximum Number of Tokens 16,000, Thinking Adaptive, Effort high, Enable Prompt Caching on, TTL 1 hour. System Message = `system_static`. Prompt = `user_dynamic`. Tools: **MCP Client Tool**, Tools to Include = Selected: `wiki`, `character`, `rule`, `scene_recall`, `fow_line` (read-only, so the writer can check a place or a number mid-draft, the way NATALIE does; nothing that writes). Max Iterations 6. Require Specific Output Format → **Structured Output Parser** with the Writer schema (§6.4). Prompt in §6.3.
- **Memory watch, first run.** The one community datapoint on large inputs through the LangChain nodes is ~30k-token prompts pegging CPU and crashing 6 GB instances on 1.95–1.97 ([community](https://community.n8n.io/t/n8n-workflow-crashing-on-large-text-input-to-llm-node-high-cpu/99788)). The writer's prompt is 40–70k tokens. The instance is 2.38.6 and its memory ceiling is not recorded, so this is **to verify**: watch `docker stats` on the first real draft; if the container swaps or the run dies, move the writer to an HTTP Request node (§7 item 14) and keep the rest.
- **Code "sanity"**: word count at least 60% of the outline's `target_words`, no markdown fences left in `markdown`, the summary ≤ 200 words, else one re-draft with the shortfall named; then never again (a second failure escalates). A parser failure that survives the parser's own re-ask is treated the same way as a shortfall.
- Checkpoint `draft`, `round = 0`.

**Stage C, CHECK.** The passes are specified in §2. Nodes: **MCP Client `verify_scene(markdown, combat, culture, "set-piece")`** → **Code "parse verify"** (first line is `FAIL: N fail, M warn` or `PASS: 0 fail, M warn`; regex `^(FAIL|PASS): (\d+) fail, (\d+) warn`, then each `  FAIL  ` and `  WARN  ` line becomes a finding with `pass = tell_scan`) → **MCP Client `gap_fill(markdown)`** (only when `scene_type` is duel, battle or working; the tool returns a numbered prose report, so a Code node regexes the counts out of lines 1, 3, 5 and 7) → **Code "ledger checks"** over the `facts`, `hooks`, `chapters` rows already fetched → **Loop Over Items** over up to ten attributed dialogue lines per cast member → **MCP Client `voice_check(name, line)`** → **Code "repetition"** → five critics in sequence (each on `claude-sonnet-5`, Effort medium, caching on, 4,000 max tokens; four as Basic LLM Chain with no tools, the Canon critic as an AI Agent with `character`/`fow_line`/`wiki` and Max Iterations 5; each with the Findings schema, §6.4) → **Code "merge findings"** (dedupe on `chapter_quote`; drop any model finding whose `chapter_quote` is not a substring of the chapter; suppress findings matched by an `overrides` row or by the writer's declared lie and misreading, where "matched" means the finding's `chapter_quote` falls in the same paragraph as the declared sentence; count FAIL and WARN; `verdict = pass | revise | escalate`) → Data Table Insert `findings` (one row per finding, with `round`).

Sequential, not parallel: n8n runs branches of one execution one after another anyway, and five Sonnet calls of about a minute each is five minutes.

**Stage D, REVISE.** Implemented with a `round` counter carried in the item and an **If**, not with Loop Over Items (which has no natural cap; [template 3503](https://n8n.io/workflows/3503-generate-written-content-with-gpt-recursive-writing-and-editing-agents/) shows the shape and the missing cap).

- **If `verdict = revise` and `round < 3`** → **AI Agent "Reviser"** (`claude-opus-5`, the same `system_static`, so the cache hits; Effort medium; prompt in §6.3: the chapter, the findings for this round, and the frozen list) → **Code "diff guard"**: the revision must keep ≥ 85% and ≤ 115% of the previous word count, ≥ 70% of the quoted-dialogue lines, ≥ 70% of the paragraphs, the same first-sentence POV name, and the same last paragraph unless a finding named the ending. A failed guard discards the revision and keeps the previous draft ([KazKozDev](https://github.com/KazKozDev/NovelGenerator): repairs that "silence the chapter's dialogue, fuse its paragraphs or quietly cut a sixth of it" are sent back; the 85% floor is his "a sixth", the 70% figures are this design's starting numbers, not measured). → `round + 1` → checkpoint `draft_r{n}` → back to Stage C, re-running the deterministic passes always, the Continuity critic always (revision is where new inconsistencies come from; Dramaturge), and the other critics only if they raised a FAIL last round.
- **Monotone acceptance**: after re-check, the new draft replaces the old only if `fail_count` did not rise and `warn_count` rose by at most 2. Otherwise the old draft stands and the round is spent.
- **If `round = 3` and FAIL remains** → `verdict = escalate`.

**Stage E, GATE.**

- **Code "review policy"**: human review is required if `verdict = escalate`, or `review_mode = every`, or (`review_mode = first3_then_5` and (`chapter_no <= 3` or `chapter_no % 5 = 0`)). Otherwise auto-approve.
- **Data Table Update `chapters`** `status = awaiting_isaac` → **Gmail "Send and Wait for Response"**, Custom Form with `approve`, `instructions` (free text), `mark_intentional` (free text: which finding, why), `drop`; Limit Wait Time 7 days; the mail body carries the verdict line, every FAIL and WARN with its quotes, the chapter, and the author notes. → **Switch**: `approve` → Stage F (if a Tell-scan FAIL is still open, the archive call passes `verify=False` and the digest says so; see §2); `instructions` → Reviser with Isaac's text as the only finding, `round` reset to 2 (one more round) → Stage C; `mark_intentional` → Data Table Insert `overrides` `{book_id, chapter_no, finding_quote, reason}` → Stage C once more (the override suppresses the finding) → Stage F; `drop` → `chapters.status = dropped`, then **Execute Sub-workflow WF-0b** for the remaining chapters with the note.
- Wait timeout → `chapters.status = awaiting_isaac` stays; the dispatcher keeps stopping at its step 4 and sends the daily reminder from there (the timed-out execution itself ends).

**Stage F, COMMIT.** In this order, each a checkpoint:

1. **MCP Client `archive_scene(title, markdown, author_notes)`**. `title = "Chapter NN — <title>"` (it becomes the H1; the slug strips the dash, so the file is `scenes/chapter_nn_<title>.md`). `author_notes` = the writer's notes (the nine or more filled blanks, rule ids cited) + the ≤200-word summary under a `Summary for continuity` heading + the verify first line + surviving WARNs + a `Pipeline` line (`job_id`, rounds, model ids, cache read tokens where known). The tool writes the file, publishes to the Notion Scene Archive, commits and pushes. With the Appendix A gate it refuses a draft that still has a verify FAIL unless `verify=False`.
2. **Basic LLM Chain "Extractor"** (`claude-sonnet-5`, no tools, Extractor schema §6.4): facts with quotes, each typed `location | knowledge | injury | item | relationship | death | time | number`, with `subject`, `fact`, `quote` (must be a substring of the chapter), and `confidence` (`stated | implied`); hook events (`planted | advanced | paid`, with quote); Ledger candidates in the table's own categories (`the dead | injuries and reserve | debts | who knows what | reputation`); `time_elapsed`; one line of "what happened" for the Front. This is [KazKozDev](https://github.com/KazKozDev/NovelGenerator)'s rule, "Nothing enters the canon that is not backed by a verbatim quotation from accepted prose", and the same evidence-chain shape ConStory's checker uses.
3. **Data Table Insert `facts`** (drop any row whose quote is not in the chapter); **Update `hooks`** (`status`, `last_ch`, and "mention is not advancement": a hook is `advanced` only if the extractor quotes a change in it, [InkOS](https://dev.to/dylan_brown_4c803aefcfe51/building-an-autonomous-ai-agent-that-writes-novels-architecture-of-a-10-agent-pipeline-59pf)); **Update `chapters`** (`status = done`, `summary`, `word_count`, `scene_file`, `rounds`, `fail_final`, `warn_final`, token counts).
4. **MCP Client `ledger_add(category, who, text, due_after_sessions)`** for each Ledger candidate, at most five per chapter; **`advance_front(front_id, what_happened, next_move)`** when the outline row names a Front; **`session_end(thread, scene_markdown, rulings=[], notes)`** (the second parameter is named `scene_markdown` in the tool; the returned drafts are discarded, the call is made for its side effect) so `table/sessions.yaml` grows and `due()` finally ages (today `sessions.yaml` is `[]` and nothing ever comes due). Each of these commits and pushes; three to nine pushes per chapter.
5. **MCP Client `arcs_place(arc, file)`** (new tool, Appendix A): appends the scene under `## <Book title>` in `scenes/ARCS.md` in chapter order. Without it a hand edit is needed before any epub exists.
6. **Code "audit due?"**: WF-3 runs when `chapter_no % 5 = 0`, or every third chapter while `chapter_no / target_chapters` is between 0.35 and 0.65 (§1.5). If due → **Execute Sub-workflow WF-3** (no wait). Always → **Execute Sub-workflow WF-4** (no wait) for narration, and for `sync_now` on the audit chapters.
7. **Data Table Delete `stages`** where `job_id` matches (the in-flight drafts; `findings` rows are kept).

### 1.5 WF-3 Book Audit

Runs every fifth chapter (every third in the middle band) and at the end, and does not edit anything; it reports, and Isaac reopens a chapter if he wants (set `chapters.status = planned` with a `revise_note`; WF-2 then runs with the note as the only finding, which is a revise-only pass).

1. **Data Table Get** all `chapters` summaries, all `facts`, all `hooks`, `findings` for the book.
2. **Code "ledger audit"** (deterministic, [Novel-OS](https://github.com/mrigankad/Novel-OS)'s set with its thresholds where it has them): `overdue_hook` (`due_ch < current` and not paid: critical), `dormant_hook` (no event for > 3 chapters: warn), `absent_cast` (POV cast member with no fact for > 5 chapters: warn), `dead_walking` (a `death` fact and a later fact with the same subject acting: critical), `sagging_middle` (three consecutive chapters where no Front ticked and no hook advanced: warn), `hook_debt` (open hooks > 12: warn; the 12 is a starting number, not from a source; InkOS built hook governance after 40 dangling threads).
3. **Basic LLM Chain "Continuity auditor"** (`claude-sonnet-5`, no tools): all summaries and facts, asked only for cross-chapter contradictions with both quotes and chapter numbers. Findings → `findings` (scope `book`). Errors cluster in the 40–60% band of a story ([ConStory](https://arxiv.org/abs/2603.05890)), which is why WF-2 step 6 runs this every three chapters between 35% and 65% of the outline instead of five.
4. At the end only: **Loop Over Items** over the book's chapters → **MCP Client `scene_text(scene_file)`** → **Aggregate** into the manuscript (the Data Tables do not hold prose after commit, so it is re-read from the archive) → **HTTP Request** `POST https://api.anthropic.com/v1/messages` (predefined Anthropic credential; header `anthropic-version: 2023-06-01`; body `model: claude-opus-5`, `thinking: {"type": "adaptive"}`, `output_config: {"effort": "high"}`, `max_tokens: 8000`; node Timeout ≥ 600,000 ms) with the whole manuscript (25 chapters × 3,500 words ≈ 120k tokens; a 40-chapter book ≈ 190k; the 1M window takes it) and AutoNovel's prompt, "Read the below novel. Review it first as a literary critic and then as a professor of fiction. Give specific, actionable suggestions". One pass, not AutoNovel's loop: AutoNovel revised the manuscript between rounds and stopped on hedging; WF-3 edits nothing, so a second pass on the same text would only re-read the same items. A second pass runs only after Isaac has reopened chapters. HTTP Request rather than the LangChain node because ~30k-token inputs through Basic LLM Chain / AI Agent nodes pegged CPU and crashed 6 GB instances ([community](https://community.n8n.io/t/n8n-workflow-crashing-on-large-text-input-to-llm-node-high-cpu/99788)); this call is six times that.
5. **Gmail** digest to Isaac.

### 1.6 WF-4 Deliver

Specified in §4. Narration per chapter, `sync_now` export on audit chapters and at `drafted`, digest per both.

### 1.7 WF-E Error workflow

Selected as the Error workflow in every other workflow's settings ([handle errors](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully)).

1. **Error Trigger** (receives `execution.id`, `execution.url`, `lastNodeExecuted`, the error message; it does **not** receive the failed execution's input items, so the chapter is found by state, not by `job_id`).
2. **Data Table Get `chapters`** where `status = running` (there is exactly one, by the dispatcher's lock) → **Update `stages`** for that row's `job_id`: `status = failed`, `error`, `node`.
3. **Data Table Update `chapters`**: if `retry_count < 2` → `status = planned`, `retry_count + 1` (the dispatcher re-fires WF-2 with the same `job_id`, which resumes at the last done checkpoint); else `status = failed`.
4. **Gmail** to Isaac with the execution URL and the last node. A 529 "overloaded" from Anthropic surfaces here after the node's own three retries; the dispatcher's next tick is ten minutes later, which is a longer back-off than the node can do on its own (Retry On Fail caps at 5 × 5,000 ms).

---

## 2. The check passes

**Policy.** FAIL blocks, WARN reports. Only a check with a hard number or an outright ban may FAIL; a pattern that needs a human read is a WARN. That is `verify.py`'s own stated policy and it extends to the critics: continuity contradictions, knowledge leaks, canon numbers, dead characters, missing payoffs and stale names FAIL; style, pacing, voice and unsupported new facts WARN. No holistic score exists anywhere in the pipeline. Every model finding carries `chapter_quote`, and the merge node drops any finding whose quote is not in the chapter, which removes most hallucinated findings for free.

**Order.** Free and deterministic first (passes 1–5), then the model critics (6–10), each scoped to one class of fault ([ConStory](https://arxiv.org/abs/2603.05890)'s category-guided prompts; [Atlas](https://arxiv.org/html/2607.00918) F1 0.853 vs 0.805 for a plain judge).

### Pass 1, Tell scan (deterministic, `verify_scene`)

What it catches: the AI tells and the hard prose numbers. The mapping from finding to rule id is `verify.py`'s own (checked against the source):

| level | finding | rule id |
|---|---|---|
| FAIL | em or en dash, ` -- ` | AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE |
| FAIL | antithesis "not X but Y" | AI-tells §1 |
| FAIL / WARN | the Ladder, two / one `was X and the Y was` clauses | R6-1-LADDER_BAN, Check 18 |
| FAIL | countdown negation | AI-tells §1 |
| WARN | 3+ Not/Never/And/Only fragments | AI-tells §1 |
| WARN | a named faculty as grammatical subject | R6-2-FACULTY_NEVER_SUBJECT, Check 19 |
| WARN | gloss phrases | R4-13-ZERO_BUDGET, Check 15 |
| WARN | emotional signposting; question in narration; 2+ similes in a paragraph; tidy close | AI-tells §4 / §1 / §5 / §2 |
| FAIL | reification ≥ 3 per scene or 2 in a paragraph | R4-15-TWO_PER_SCENE_BUDGET, R4-15-ONE_PER_PARAGRAPH, Check 17 |
| FAIL | three consecutive sentences over 25 words | R4-14-CHAIN_CEILING |
| FAIL / info | ≥ 4 flat runs | R4-14-RUN_RULE |
| FAIL / WARN | sentences under 8 words below 10% / 18% | R4-14-HARD_CEILINGS |
| WARN | paragraph closing on three long sentences; paragraph-length CV < 0.35 | R4-14-HARD_CEILINGS, AI-tells §2 |
| WARN | word count outside band (always `set-piece` for a chapter: 2,500 floor, no ceiling) | Table Rule 2 |
| FAIL | Kharven: fewer than 2 of 5 signature items | R6-9-RECURRENCE_RULE |
| WARN | combat: zero HEMA / zero anatomy terms | R13-6-HEMA_VOCAB, R13-6-ANATOMY_VOCAB |

This pass is the same as [EQ-Bench's slop score](https://eqbench.com/slop-score.html) and [AutoNovel's regex pass](https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md) in kind ("not X but Y", sentence-length variation, em-dash rate) but tied to the packs' rule ids, which is why it comes first. Its FAILs are never overridable by the reviser or by an `overrides` row; the only way one reaches the archive is Isaac's `approve` on an escalation, and then `archive_scene` is called with `verify=False` and the digest records it. Known blind spots (inventory §7.10): the HEMA regex counts everyday words (point, cut, guard, cross, edge, void), `split_sentences` skews on dialogue-heavy text, any `*…*` of three words counts as an interior beat; leave them as WARNs.

### Pass 2, Shape (deterministic, Code)

What it catches: a chapter that is not the chapter the outline ordered. `verify.py`'s `set-piece` band has no ceiling, so the size checks use the outline's `target_words`, not the band. FAIL: word count below 80% of `target_words` ([KazKozDev](https://github.com/KazKozDev/NovelGenerator) gates at ≥ 80% of target) or above 150% of it; zero quoted dialogue lines when the cast has two or more people and the type is not `quiet`; a stale name (any struck Büri-register term from `build/renames.yaml`; needs `stale_names_text`, Appendix A, since `stale_names` scans files, not a string). WARN: two consecutive paragraphs sharing more than 60% of their word trigrams (a beat retold in new words); the POV name absent from the first two paragraphs.

### Pass 3, Combat floor (deterministic, `gap_fill`, duel / battle / working only)

What it catches: a fight or a working without its floor. `gap_fill` returns Pack Thirteen §5's eight counts as a prose report. All of it is **WARN**, not FAIL, and the reason is in the tool: an "exchange" is any paragraph matching the HEMA regex or the verbs strike/cut/thrust/hit/drew/swung/closed, and the HEMA regex matches point, cut, guard, cross, edge and void, so "zero exchanges" and "zero HEMA terms" cannot fire on any chapter that contains a fight in ordinary English. A FAIL that cannot fail is theatre; as WARNs the counts are still useful context. WARN: zero exchanges (R12-3-COMBAT_EXCHANGE_OWES); zero anatomy terms (R13-6-ANATOMY_VOCAB, the narrower regex); no Phenomenon line in the author notes (R13-3-PHENOMENON_MANDATE); no stratum named (R13-2-THREE_STRATA_MANDATE, R13-2-STRATUM_TWO_WELLSPRING); no Mechanism Vocabulary term (R13-9-STYLE_DIRECTIVE_MECHANISM_VOCAB); no traceable stat row named in the notes (R14-3-TRACEABILITY). The Rule compliance critic (pass 8) reads these counts as context and is the pass that can FAIL a fight on R12-3.

### Pass 4, Ledger (deterministic, Code over Data Table rows)

What it catches: what a fact table can catch without reading prose, [Novel-OS](https://github.com/mrigankad/Novel-OS)'s layer one. FAIL: a subject with a `death` fact has a speech tag in the chapter (said, asked, and the tag list `build/voices.py` uses); the outline row's `pays` list names a hook and the chapter contains none of that hook's `keywords` (the Beat critic confirms or clears it). WARN: a subject with a `death` fact followed by an action verb (a body can "lie", so this is a read, and the Continuity critic confirms); a cast member with no fact in more than five chapters; a capitalised name in the chapter that is a known character (from `CAST.md` names cached in `books`) but not on the outline's cast; a `location` fact for a cast member that places them elsewhere at the chapter's stated time; an `injury` fact newer than three chapters for a character the chapter has fighting or running.

### Pass 5, Voice and repetition (deterministic, `voice_check` + Code)

What it catches: a line that reads like someone else, and the chapter opening the way the last one did. WARN only. `voice_check(name, line)` for up to ten attributed lines per cast member (attribution by the same speech-tag-within-40-characters heuristic `build/voices.py` uses; characters with fewer than eight archived lines have no fingerprint and are skipped). Repetition: word-trigram overlap of the first paragraph with the first paragraphs of the previous three chapters above 0.3 (Book-Agent's rotating openers; Agents' Room's trigram finding, [survey](https://arxiv.org/html/2410.02603)); the same for the last paragraph.

### Pass 6, Continuity diff (Sonnet 5, no tools)

What it catches: the chapter contradicting what the book has already established. Input: the chapter, the `facts` rows for the cast and place (each with its quote and chapter number), the previous chapter's tail, all summaries. Instruction: extract this chapter's facts in the same eight types, pair each against the table, and report only contradictions, quoting both sides. FAIL: a direct contradiction with a `stated` fact. WARN: contradiction with an `implied` fact; a new fact about a cast member that no earlier chapter supports (passed to the Extractor as `provisional`). The writer's declared lie (brief blank 6) and misreading (blank 4) are given to this critic as known-intentional so they are not raised.

### Pass 7, Knowledge boundary and POV (Sonnet 5, no tools)

What it catches: a character knowing, saying or acting on something outside their witness scope, and the POV discipline the packs demand. Input: the chapter, the `knowledge` facts (who knows what, from the Extractor and from `table/ledger.yaml`'s "who knows what" lines), the brief blanks 1–4 as filled by the writer, the rules R5-C1-WRITE_FROM_LEAST_KNOWING, R5-C1-INFO_TRACKED_PER_POV, R6-3-IGNORANCE_QUOTA, R6-4-MISREADING_BUDGET. FAIL: a character uses a fact the table says they do not know; narration states what the POV cannot perceive or know; the declared misreading is corrected inside the scene. WARN: the ignorance-quota item gets explained; the POV shifts mid-scene without a divider; a "reader knows" item is spoken aloud by someone who should not. [InkOS](https://dev.to/dylan_brown_4c803aefcfe51/building-an-autonomous-ai-agent-that-writes-novels-architecture-of-a-10-agent-pipeline-59pf)'s information-boundary matrix and [Book-Agent](https://forum.level1techs.com/t/my-ai-powered-novel-writing-pipeline-book-agent-generating-epistemically-controlled-long-form-fiction/243193)'s secrecy classes are the models.

### Pass 8, Rule compliance (Sonnet 5, no tools)

What it catches: the packs' rules that regex cannot see. Input: the chapter, the author notes, the same brief loadout the writer had (cached), the `gap_fill` counts for combat types. Instruction: for each finding cite the rule id and quote the span; a rule may FAIL only if its summary carries a number, "never", "always", "must" or "ban"; everything else is WARN. The merge node enforces that rule mechanically: it has the loadout text in the execution data, looks up the cited id, and demotes a FAIL whose summary lacks those words to WARN. Examples that FAIL: a fifth explaining voice or a third voice in one engagement (R12-4-VOICE_MIXING_RULE); a self-derived technique that kills without two exchanges of evidence (R12-3-COMBAT_EXCHANGE_OWES); a Stat name in narration rather than in a mouth (Table Rule 5 ruling); a number for a metaphysical quantity with no source; an ending on a question aimed at the reader (Table Rule 1). Also: every rule id cited in the author notes must exist in the loadout list (the merge node checks the ids; a bad id is a WARN). The rubric is written as neutral criteria, not as a list of negations, because negation-heavy rubrics bias a judge toward FAIL ([rubric artifacts](https://arxiv.org/html/2609.02942)).

### Pass 9, Canon (Sonnet 5, tools: `character`, `fow_line`, `wiki`, Max Iterations 5)

What it catches: what the wiki says differently. FAIL: a Stage, Level, Band, stat, EU or η figure stated for a named practitioner that differs from `fow_line`; a Wellspring with the wrong Family; a technique attributed to the wrong Discipline; a Stage named Ignition/Temper instead of Fracture of Worlds' names (Table Rule 5 ruling). WARN: a claim about a place, an institution or a person's history that the card or the top wiki page does not support; a card that itself lacks the figure (the critic says so rather than inventing, the same rule `fow_line` follows). When the critic judges that the card, not the chapter, is wrong, it says so in `note`, and the finding escalates to Isaac rather than to the reviser (his ruling may become `log_ruling` or `update_character`).

### Pass 10, Beat and hooks (Sonnet 5, no tools)

What it catches: the chapter not doing its job in the book. Input: the outline row (beat, POV, cast, Front, plants, pays, time_elapsed), the hook agenda, the chapter. FAIL: the beat did not happen; a `pays` hook is not paid on the page (a mention is not a payoff); the chapter ends on a question aimed at the reader rather than "an NPC line, a physical action, or a thing he can now see" (Table Rule 1). WARN: a `plants` hook not planted; the Front's tick not visible; `time_elapsed` contradicted by the text; the POV not the least-knowing character present without the notes saying why (R5-C1 is "a default, breakable with reason").

### The revise loop

- **Round 1** gets every FAIL and WARN, grouped by pass, each with its quotes and a one-line fix. Frozen and stated as frozen: the beat, the POV, the cast, the ending's kind, the band, the planted and paid hooks, the declared lie and misreading. "Change only the quoted spans and what they force. Do not summarise, do not add scenes, do not cut a paragraph a finding did not name."
- **Round 2** gets FAILs only.
- **Round 3** gets FAILs only, plus: "If a FAIL cannot be fixed without breaking a frozen element, return `cannot_fix` with the reason instead of a revision."
- After every round: the diff guard, then the re-check (deterministic passes and the Continuity critic always; other critics only if they raised a FAIL), then monotone acceptance.
- Three rounds because every measured system peaks there ([LLM Review](https://arxiv.org/html/2601.08003) 3.62 → 3.98 then decline; [Dramaturge](https://arxiv.org/html/2510.05188v3) N_max = 3; [Claude-Book](https://github.com/ThomasHoussin/Claude-Book) max 3) and because each pass flattens prose ([CritiCS](https://arxiv.org/html/2410.02428) coherence vs rounds; AIStoryWriter ships with `CHAPTER_MAX_REVISIONS = 3` and revisions off by default).

### What escalates to Isaac

| trigger | what he sees | his options |
|---|---|---|
| a FAIL after round 3 | the finding with both quotes, the three attempts' verdict lines | approve as-is; instructions (one more round); mark intentional; drop |
| `cannot_fix` from the reviser | the reason | same |
| a Continuity or Knowledge FAIL the writer's notes flagged as deliberate | the note and the finding | mark intentional (persisted, never re-raised for that quote) |
| a Canon FAIL the critic attributes to the card | the card line and the chapter line | rule for the chapter (override) or for the card (his `log_ruling` / `update_character` later) |
| `check_docket` non-empty for the chapter's tags | the pending rule | proceed as if live / proceed as if absent (both persisted as an override for the book) |
| word count off target by more than 50% after revision | the count | approve; instructions |
| whatever `review_mode` schedules | the full chapter and notes | approve; instructions; drop |

Isaac's replies land in `overrides` with a reason, so a checker that "cannot tell an unreliable narrator, deliberate foreshadowing, or a character who lies from a genuine mistake" ([Novel-OS](https://github.com/mrigankad/Novel-OS)) stops nagging. Every shipping system found keeps a human as the last gate; this one asks him at the outline, the first three chapters, every fifth chapter, and on escalation by default.

---

## 3. Book-level memory

Three layers, three homes.

| layer | contents | where it lives | why there |
|---|---|---|---|
| **Story bible** (static per book) | wiki cards, Standing Inventory, the packs; plus the book's premise, POV cast, voice note with exemplar and anti-exemplar, target words, review mode; the outline | cards and rules in the repo/Notion, read through the MCP (`character`, `fow_line`, `wiki`, `load_rules`); the inventory block captured once from `session_start` into `books.inventory`; the book row and outline in Data Tables `books` and `chapters` | the wiki is already the canon and already mirrored hourly; the outline must be queryable by the dispatcher, which cannot read repo files |
| **Continuity ledger** (dynamic, per chapter) | typed facts with quotes; hooks with plant / due / paid chapters; overrides | Data Tables `facts`, `hooks`, `overrides`; mirrored into the table's own Ledger by `ledger_add` (its five categories), the Fronts by `advance_front`, the session log by `session_end` | typed rows are what deterministic checks and the Continuity critic diff against ([ConStory](https://arxiv.org/abs/2603.05890), [AuthorAgent](https://github.com/Ckokoski/AuthorAgent)); the repo Ledger is one line per commit-and-push and its ageing has never run; Qdrant holds the wiki, not scenes, and embeddings are the wrong tool for contradiction |
| **Chapter summaries** | ≤ 200 words each, written by the writer in the same call as the chapter | `chapters.summary`, and in the scene file under `## Author notes` → `Summary for continuity` | the running recap is free when it is part of the chapter call ([chi-0518](https://github.com/chi-0518/n8n-novel-generator)); the copy in the scene file keeps the archive self-describing and reaches Notion through `archive_scene` |

Not used: a growing conversation transcript across chapters (thinking blocks must be replayed byte-identical or the API returns 400; stage outputs re-prompted are simpler and cache better; [API errors](https://platform.claude.com/docs/en/api/errors), research note `claude-orchestration.md` §6); Postgres Chat Memory (no Postgres in the compose, and the pipeline has no multi-turn agent); the wiki mirror in full (915k words; never loadable whole).

### What one chapter draft is given

Priority order inside the prompt, stated to the writer as a priority order the way [chi-0518](https://github.com/chi-0518/n8n-novel-generator) states it: the previous chapter's tail must be continued directly; the summaries and facts govern foreshadowing and consistency; recall snippets and wiki pages are reference only; on conflict the facts win over the outline's intentions and the outline wins over recall.

| block | source | tokens (estimate) | cached |
|---|---|---|---|
| Protocol: the floor, Table Rules 1–12 as they apply to a chapter (§7 item 19), canon hierarchy, magic frame, prose standards (trimmed from NATALIE.md) | `desktop/NATALIE.md` | ~4k | yes |
| Standing Inventory for the culture | `books.inventory` (from `session_start` in WF-0) | 1–1.7k | yes |
| Loadout, brief, for the scene type | `load_rules(tags, brief=true)` | 12.5–19.4k | yes |
| Book bible: premise, cast, voice note | `books` | 2–3k | yes |
| Docket and conflicts digest for the tags | `check_docket`, `list_conflicts` (a Code node keeps the rows that name a rule id in the loadout) | 1–2k | yes |
| **cached system block** | | **21–30k** | |
| Outline row and hook agenda | `chapters`, `hooks` | ~0.5k | no |
| Brief blanks and FOW lines | `scene_brief` minus its loadout | 1.5–3k | no |
| Summaries of all prior chapters | `chapters.summary` | ch 10 ≈ 2.7k, ch 25 ≈ 6.7k, ch 40 ≈ 10.8k | no |
| Previous chapter tail, 1,500 words | `scene_text` | ~2k | no |
| Cards: full on first appearance, else FOW line + facts | `character` / `fow_line` / `facts` | 3–10k for 3–5 cast | no |
| Facts digest for cast and place, ≤ 40 rows | `facts` | ~1.2k | no |
| `scene_recall` × 2, `wiki` × 1–2 | MCP | 3k + 3.5–7k | no |
| **dynamic user block** | | **17–40k** | |
| Output: chapter 2,500–4,500 words + summary + notes, plus adaptive thinking | | 5–8k + 3–8k (thinking is an unmeasured guess; **to verify** from the first runs' usage) | |

Total input 40–70k tokens, of which 21–30k is read from cache at 10% price when the cache hits. The inventory's uncached estimate was 50–70k; the cache does not shrink the prompt, it shrinks the bill.

### Cache mechanics in n8n

- The Anthropic Chat Model node (v1.6) caches the system prompt, the tool definitions and the history ([PR #34482](https://github.com/n8n-io/n8n/pull/34482)); breakpoints are placed by the node, not by us, so the whole `system_static` string must be **byte-identical** between calls: same `load_rules` call, same order, no timestamps, no job id. Everything that varies goes in the Prompt field. The Structured Output Parser's format instructions are appended to the system message by n8n; they are constant per schema, so they do not break the prefix.
- TTL 1 hour, because the clock starts at request start and the writer, reviser and critics of one chapter are spread over 15–20 minutes; consecutive chapters of the same scene type inside an hour hit the same entry. Seven scene types means at most seven entries per book per model.
- Caches are per model. The Opus writer and reviser share one entry; the Sonnet Rule critic writes and reads its own. Cache write at the 1-hour TTL costs 2× the input price, once; reads cost 0.1×. The minimum cacheable prefix on Opus 5 is 512 tokens and on Sonnet 5 is 1,024; the system block is far above both. Cache reads do not count toward the input-tokens-per-minute limit ([rate limits](https://platform.claude.com/docs/en/api/rate-limits)).
- Where the saving actually is: inside one chapter, not across chapters. The writer's tool iterations (each a fresh request carrying the whole system block), the reviser (up to three calls) and the Rule critic (up to four) all re-read the block; across chapters a hit needs the same scene type within the hour, which the outline does not promise.
- A ratified pack changes `load_rules` output and invalidates the entry. That is the correct behaviour. Changing Effort or the tool list mid-book also invalidates; keep them fixed per node.
- The node's token display sums cache reads into `promptTokens`, so it over-reports cost; the `usage.cache_read_input_tokens` field in the raw response is the truth. **To verify**: whether n8n exposes that raw field anywhere in the execution data (the Chat Model sub-node's log tab is the place to look). If it does not, the Anthropic Console's Usage page shows cache reads per key and is the fallback for the test in §6.5.
- The critics share the same `system_static` as the writer where it helps (the Rule compliance critic) and get a shorter one where it does not (Continuity, Knowledge, Beat: protocol + bible only, ~7k, cached on the Sonnet node separately).

---

## 4. Assembly and delivery

**Chapter → scene file.** `archive_scene(title="Chapter NN — <title>", markdown, author_notes)` writes `scenes/chapter_nn_<title_words>.md` (the slug keeps word characters only) with the title as H1 and the notes under `## Author notes`, publishes a Notion Scene Archive page, commits "Archive scene: …" and pushes. On a slug collision it appends a timestamp; the pipeline avoids collisions by numbering.

**Scene file → the book's arc.** `arcs_place(arc, file)` (Appendix A, ~30 lines in `mcp_server.py`) appends `- chapter_nn_<slug>.md` under `## <Book title>` in `scenes/ARCS.md`, creating the H2 if missing, in chapter order. `ARCS.md` is what `arcs_export.py` reads; today it must be hand-edited for every new scene.

**Arc → epub and docx.** `sync_now()` runs `build/sync.ps1`: Notion export → publish → `docs_export` + `arcs_export` into `G:\My Drive\War of the Realms — Documents` → pull, commit, push. `arcs_export.py` writes one `.docx` and one `.epub` per arc whose scenes changed, plus the complete epub, with headings, emphasis, dividers (`⁂`) and blockquotes converted. WF-4 calls `sync_now` on the audit chapters (every fifth) and WF-1 calls WF-4 once more at `drafted`, so a readable epub of the book so far always exists in Drive. It takes one to two minutes when little has changed and has a 900 s ceiling; it is the only place the pipeline touches Drive, and it does its own `git pull --rebase`, so it must not run while another write tool is pushing (WF-4 runs it after WF-2's COMMIT has finished, never in parallel with it). Front matter: the epub's title is the arc name and its table of contents is the chapter H1s; a book title page and dedication are a later ten-line change to `arcs_export.py`, not needed for the first book.

**Narration (WF-4, per chapter, after COMMIT).**

1. **MCP Client `scene_text(scene)`** → **Code**: drop the two header lines (`scene file: …`, `cast file: …`) and the blank line; what remains is the narration text in cast-file format (`# Title`, paragraphs, `---` dividers, notes and markdown stripped) and is what the byte-for-byte check compares against.
2. **Basic LLM Chain "Caster"** (`claude-sonnet-5`, no tools): insert `[Name]` or `[Name: quiet]` tags where the speaker changes, using the delivery words the tool accepts (`slow slower fast faster quiet loud whisper beat "long beat"`) and the performed cues (`[sigh] [laugh] [chuckle] [gasp] [cough] [clear throat] [sniff] [groan] [shush]`) sparingly; change nothing else. The prompt states the acceptance rule verbatim: the text with tags removed must equal the input character for character.
3. **Code "check cast"**: strip the tags, compare to the header-stripped `scene_text` byte for byte, compare `---` counts. Mismatch → one retry with the first differing line quoted → if it still fails, skip casting and narrate with the narrator voice alone. (`cast_scene` runs the same check itself and refuses on a mismatch; the Code node exists to spend the retry before the MCP call, not instead of the tool's check.)
4. **MCP Client `cast_scene(scene, script)`** → writes `scenes/cast/<stem>.cast.md` and lists speakers with no `build/voices.yaml` entry (they get a stable pool pick).
5. **MCP Client `narrate_scene(scene, "narrator")`** → detached job on Isaac's PC (Kokoro-onnx, CPU, ~18 words per second measured: a 3,500-word chapter renders in about 3.3 minutes and plays for about 23 minutes).
6. **Wait** 60 s → **MCP Client `narration_status(job)`** → **Code** reads the job's line for `done` / `failed` → **If** not done → back to Wait (at most 15 loops) → **Data Table Update `chapters.audio_path`**. Output lands in `G:\My Drive\…\Arcs\Audio` when Drive is mounted, else `docs/audio`.
7. Serial: one narration job at a time, because it is Isaac's CPU. A 25-chapter book renders in about 1.4 hours of CPU and plays for about 10 hours.

**Digest.** Per chapter, one Gmail: file path, Notion page, verify first line, WARN count, rounds, token counts where n8n exposes them, audio path, the speakers still on pool voices (so `build/voices.yaml` grows with the cast). Per book: epub and docx paths in Drive, the audio folder, WF-3's final report.

---

## 5. Cost and time

Prices from the [models overview](https://platform.claude.com/docs/en/models/overview): Opus 5 $5 input / $25 output per million tokens, cache read $0.50, cache write (1 h) $10; Sonnet 5 $2 / $10, cache read $0.20, cache write (1 h) $4. Estimates assume a 3,500-word chapter, 1.5 revise rounds on average, and the token table in §3. Output tokens include thinking, which is the least certain number here.

| call | model | input (uncached / cached) | output incl. thinking | cost |
|---|---|---|---|---|
| Draft | Opus 5 | 30k / 25k (one cache write per chapter, worst case) | 12k | $0.15 + $0.25 + $0.30 = **$0.70** (a cache hit instead of a write makes it $0.46) |
| Reviser × 1.5 | Opus 5 | 17k / 25k read | 9k | ($0.085 + $0.0125 + $0.225) × 1.5 = **$0.48** |
| Critics, first pass × 5 | Sonnet 5 | 12k / 20k read | 2k | 5 × ($0.024 + $0.004 + $0.02) = **$0.24** (+ $0.08 once per scene type for the Sonnet cache write) |
| Critics, re-checks | Sonnet 5 | half the set × 1.5 rounds | | **$0.18** |
| Extractor + Caster | Sonnet 5 | 8k + 6k | 2k + 5k | **$0.10** |
| Planner, WF-3 audits (amortised over 25 chapters) | Opus 5 / Sonnet 5 | | | **$0.15** (a guess; the planner is one long Opus call, the audits are Sonnet) |
| **per chapter** | | | | **≈ $1.85** (range $1.50–3.00 with escalation reruns) |

Per book: 25 chapters (≈ 87k words) ≈ **$45–75**; 40 chapters (≈ 140k words) ≈ **$75–120**, plus the whole-manuscript review on Opus 5 (120–190k tokens in, 8k out ≈ $1–1.2 per pass). Del Arroz reports ~$20 per novel on Sonnet 4.6 with one self-critique and no fact base ([Substack](https://substack.aicentral.blog/p/i-let-ai-write-three-complete-novels)); the difference here is five evidence-quoting critics and Opus as the writer. Without prompt caching the same table comes to roughly $2.20 per chapter, so caching is worth about 15–30% on these numbers, not a multiple; it matters most where one chapter re-reads its own block (the writer's tool iterations, the reviser, the Rule critic), and it is a standing setting because it costs nothing to leave on.

Rate limits: the Start tier allows 1,000 requests and 2M input tokens per minute on Opus 5 and Sonnet 5 with a $500 monthly spend cap ([rate limits](https://platform.claude.com/docs/en/api/rate-limits)). Which tier Isaac's key is on is not recorded (**to verify** in the Console); on any tier the pipeline's one-call-at-a-time shape is far below the per-minute limits, and the monthly cap is what bounds a runaway.

Wall time per chapter, sequential: brief 1 min (eight MCP calls, `wiki` rescans 583 files per call), draft 2–5 min (12k output tokens at Opus 5's non-streaming rate; **to verify**), five critics 4–6 min, revise 1.5 × (2 min + 3 min re-check) ≈ 7 min, extractor and commit with three to nine git pushes 1–2 min: **15–20 minutes** of machine time, in line with the Barr Group's 15 minutes per chapter ([blog](https://barrgroup.com/software-expert-witness/blog/ai-agents-finished-decade-old-novel)). The dispatcher adds up to ten minutes of idle between chapters, so a 25-chapter book with `first3_then_5` is about 8 hours of machine time and 10–12 hours of wall clock plus Isaac's eight decisions, each of which stops the book until he answers; `escalations_only` runs overnight. Narration adds 1.4 CPU-hours off the critical path.

Iteration cost while the prompts settle: run the writer on Sonnet 5 (two-fifths of the price), put a **Limit** node in front of any loop, and test on one chapter, the forum's standard advice after a GPT-4 Turbo bill ([community 90870](https://community.n8n.io/t/help-me-write-my-book/90870)).

---

## 6. The first milestone: "WOTR Chapter v0"

The smallest version worth running: **one chapter, one execution, from a form**, through brief → draft → three checks → revise (≤ 2 rounds) → Isaac approves → archive. No dispatcher, no outline, no extractor, no narration, no Data Tables except an optional `chapters` row at the end. The three checks are the Tell scan (pass 1), the Continuity diff (pass 6, against the previous scene's tail and `scene_recall` hits, since no `facts` table exists yet) and Rule compliance (pass 8). Everything in it is reused unchanged by WF-2.

### 6.1 Prerequisites (about 30 minutes, plus the Appendix A `allowed_hosts` change)

1. The `allowed_hosts` change in `mcp_server.py` (Appendix A, first row) committed; without it every call from the container is a 421.
2. Scheduled task "WOTR MCP pipeline": `pythonw.exe build/mcp_server.py --http --port 8766 --log build/mcp_pipeline.log`, running.
3. `docker exec <n8n container> wget -S -O- http://host.docker.internal:8766/mcp` returns 406 or 405 (not 421, not "connection refused").
4. n8n credentials: Anthropic API key; Gmail (OAuth) for the approval mail.
5. Pick a beat: call `scene_menu("Sodoku Moto")` in Claude Desktop and take the first hook, or take one of Isaac's own. Pick the previous scene by file name from `scenes/MANIFEST.md`.

### 6.2 Node list (31 nodes)

| # | node | type | settings |
|---|---|---|---|
| 1 | Chapter brief | Form Trigger | fields: `book` (text), `chapter_no` (number), `title`, `beat` (textarea), `thread` (dropdown of the four), `scene_type` (dropdown of the seven), `culture` (dropdown), `characters` (text, comma list), `target_words` (number, default 3,200), `previous_scene` (text, scene file name or blank), `combat` (dropdown yes/no), and two test hooks: `draft_override` (textarea; when filled, nodes 15–16 are skipped and this text is the draft) and `tail_override` (textarea; when filled, replaces the previous scene's tail). The two overrides exist so §6.5 steps 3 and 4 can be run without editing an archived scene. |
| 2 | job | Edit Fields (Set) | `job_id = {{$execution.id}}`, `cast = characters.split(',')`, `round = 0`, `band = "set-piece"` |
| 3 | loadout tags | Code | the seven-type map from §1.4; returns `tags` |
| 4 | load_rules | MCP Client | endpoint `http://host.docker.internal:8766/mcp`, tool `load_rules`, JSON `{"tags": <tags>, "brief": true}` built in node 3 |
| 5 | check_docket | MCP Client | `{"tags": <tags>}` |
| 6 | session_start | MCP Client | `{"thread", "scene_type", "culture"}`; only the `# STANDING INVENTORY` block is kept (next node); ~20–27k tokens once per run, acceptable for v0 |
| 7 | inventory | Code | split node 6's output on `\n\n---\n\n`, keep the block starting `# STANDING INVENTORY` → `inventory` |
| 8 | scene_brief | MCP Client | `{"beat", "thread", "scene_type", "culture", "characters": cast}` |
| 9 | trim brief | Code | keep from `## Fill before drafting` to just before `## Rule loadout` |
| 10 | previous text | MCP Client | `scene_text`, `{"scene": previous_scene}`; skipped by an If when blank or when `tail_override` is filled |
| 11 | tail | Code | drop the two header lines; last 1,500 words at a paragraph boundary; `tail_override` wins when filled |
| 12 | cast loop | Loop Over Items | batch 1, over `cast` |
| 13 | character | MCP Client | `character`, `{"name": ...}`; Code after it caps at 6,000 chars |
| 14 | cards | Aggregate | all items → `cards` |
| 15 | recall | MCP Client | `scene_recall`, `{"query": beat's first 12 words + cast}` |
| 16 | assemble | Code | builds `system_static` and `user_dynamic` (§6.3) |
| 17 | Writer | AI Agent | Anthropic Chat Model `claude-opus-5` (for the first runs, `claude-sonnet-5`), max tokens 16,000, Thinking Adaptive / Effort high, Prompt Caching on / 1 h; System Message `{{system_static}}`, Prompt `{{user_dynamic}}`; MCP Client Tool (Selected: `wiki`, `character`, `rule`, `scene_recall`, `fow_line`), Max Iterations 6; Structured Output Parser, Writer schema. Skipped when `draft_override` is filled. |
| 18 | keep draft | Edit Fields | `draft = output.markdown` (or `draft_override`), `notes`, `summary`, `title` |
| 19 | verify_scene | MCP Client | `{"markdown": draft, "combat", "culture", "band": "set-piece"}` |
| 20 | parse verify | Code | regex on the first line; FAIL/WARN lines → findings with `pass: tell_scan` |
| 21 | Continuity critic | Basic LLM Chain | `claude-sonnet-5`, Effort medium, caching on, max tokens 4,000, no tools; System = protocol only; Prompt §6.3; Findings schema |
| 22 | Rule critic | Basic LLM Chain | same model; System = `system_static` (so the loadout is cached once more on Sonnet); Prompt §6.3; Findings schema |
| 23 | merge | Code | drop findings whose `chapter_quote` is not in `draft`; suppress the declared lie and misreading by paragraph; demote Rule FAILs whose cited rule summary has no hard word; `fail_count`, `warn_count`, `verdict` |
| 24 | any FAIL? | If | `fail_count > 0` |
| 25 | round < 2? | If | true → 26; false → 29 |
| 26 | Reviser | AI Agent | `claude-opus-5`, same System as 17 (cache hit), Effort medium; Prompt §6.3; Writer schema |
| 27 | diff guard | Code | the §1.4 thresholds; keeps the old draft on failure; `round + 1` → back to 19 |
| 28 | Approve chapter | Gmail: Send and Wait for Response | Custom Form: `approve` / `instructions` / `drop`; body: verdict line, findings, chapter, notes; Limit Wait Time 7 days |
| 29 | Escalate | Gmail: Send and Wait for Response | same form, subject "needs a decision"; `instructions` → 26 with `round = 1` |
| 30 | archive args | Code | builds `{"title": "Chapter NN — " + title, "markdown": draft, "author_notes": notes + "\n\nSummary for continuity\n" + summary + "\n\nverify_scene: " + first line + "\nPipeline: job " + job_id}` as one object |
| 31 | archive_scene | MCP Client | JSON `{{ $json.args }}` from node 30 |

Plus a two-node error workflow: **Error Trigger → Gmail**. Workflow settings: Error workflow set; timeout off; Save Execution Progress on for the first runs.

### 6.3 Prompts

**Writer, System Message** (`system_static`; the protocol part is fixed text, the rest is spliced in by node 16 and must not change between runs). The protocol below paraphrases NATALIE.md for a chapter rather than a turn; §7 item 19 says what was dropped and why:

```
You write War of the Realms prose for Isaac's table under NATALIE's standing rules. You are the writer; other passes check your work and you will be asked to revise against quoted findings. This is a chapter of a book, not a turn at the table: the approved outline beat is Isaac's decision for his character, and you write what it says he does and nothing he did not decide.

THE FLOOR. Never invent a number for a metaphysical quantity; check the FOW line or put an estimate in a character's mouth and flag it. Never resolve a canon conflict silently. Label anything you originate as pending ruling in the author notes. Naming canon is Moto; the Büri register is dead.

THE TABLE RULES, AS THEY APPLY TO A CHAPTER. 1 Ending: stop on an NPC line, a physical action, or a thing he can now see; never on a question aimed at the reader. 2 Length: a chapter is a set piece, 2,500 words minimum, with full scene standards; hit the target given. 3 NPC agency: they want things, lie, withhold, refuse, bargain, misjudge. 4 The world moves: the named Front advances. 5 Adjudication without dice: Stage gap, whether he read the opponent, what he has spent, what the environment allows; the author notes name the stat row that decided; every action costs something specific and visible. 6 The read is the game: a self-derived technique gets two or three exchanges of evidence before it kills; explanations arrive through the four voices, never narration on its own authority. 7 The ledger persists. 8 Ignorance and lies: one thing per chapter the POV notices and you do not explain; one thing per chapter an NPC says that is wrong and stays uncorrected. 9 Explicit scenes: plain anatomical vocabulary, positions tracked, the NPC's own desire and refusal line, a consequence afterward. 10 Body language over talking heads; one italic private thought per NPC per scene. 11 First introductions: full physical inventory on first sight, then a want and an unswappable voice. 12 Lived-in rooms: ambient noise that is not the plot.

CANON HIERARCHY. Isaac's direction; the project canon documents; the amendment packs, later beats earlier; the Notion wiki; the base craft documents; prior sessions; internal logic.

THE MAGIC FRAME. Mechanism is on the page; power is finite and the spending shows. Four explaining voices, never more than two per engagement. Every working is explained at the Aether, the Wellspring and the Essence; the author notes name its phenomenon, Physics Domain, Wellspring, Category and Mechanism Vocabulary term. The stats decide; effects on the page as behaviour, names only in a mouth, an instrument, a document or a private count.

PROSE STANDARDS. Sensory grounding, texture from the Standing Inventory before anything invented. No em dashes. No hypophora. No "it's not X, it's Y". No countdown negation, no fragment emphasis, no Ladder, no Gloss, no narrator moral adjudication, no reaction-shot cutaway. Varied sentence length inside every paragraph. Reification two per scene. Set pieces: layered sensory opening, end on physical action, HEMA vocabulary as choreography, the combat floor, the three-layer hit, the POV's own body on the page. Register: modern words are legal everywhere; the only test is whether a word breaks belief. Two characters' lines must not be swappable. Iceberg: no "as you know".

CONTEXT PRIORITY. The previous chapter's tail must be continued directly. The summaries and facts govern consistency and foreshadowing. Recall snippets and wiki pages are reference only. On conflict, facts beat the outline's intentions and the outline beats recall.

OUTPUT. Return JSON matching the schema: title; markdown (the chapter, no heading, no fences); author_notes (every numbered blank of the brief filled, with the rule ids that constrained the piece, the stat row that decided each contested action, anything originated marked pending); summary (at most 200 words, past tense, who ended where, what changed, what is now known by whom, what was planted); declared_lie and declared_misreading (the exact sentence from the chapter in each case, so the checks can find and skip it).

=== STANDING INVENTORY ({culture}) ===
{inventory}

=== RULE LOADOUT ({scene_type}: {tags}; live, newest pack first) ===
{load_rules output}

=== DOCKET FOR THESE TAGS ===
{check_docket output, or "none"}
```

**Writer, Prompt** (`user_dynamic`):

```
Book: {book}. Chapter {chapter_no}: {title}. Thread: {thread}. Scene type: {scene_type}. Culture: {culture}. Target {target_words} words. Job {job_id}.

BEAT
{beat}

BRIEF (fill every blank in author_notes before you draft; the prose must obey what you fill)
{scene_brief output, loadout section removed}

PREVIOUS CHAPTER, LAST 1,500 WORDS (continue directly from where this ends; do not recap it)
{tail, or "This is the first chapter."}

CARDS AND FOW LINES
{cards}

CONTINUITY RECALL (reference only)
{scene_recall output}

Write the chapter.
```

**Continuity critic, Prompt** (System = the protocol paragraph and the context-priority paragraph only):

```
You check one chapter for contradictions with what came before. You do not judge quality and you do not rewrite.

Established material, in priority order:
1. The previous chapter's last 1,500 words: {tail}
2. Recall from the archive: {scene_recall output}
3. The writer's declarations, which are intentional and must not be raised: lie = "{declared_lie}"; misreading = "{declared_misreading}".

Method. Extract from the chapter every fact of these types: location, knowledge (who knows what), injury, item, relationship, death, time, number. For each, look for a fact in the established material that contradicts it. Report only contradictions and only with both quotes.

Severity. FAIL when the established fact is stated outright and the chapter contradicts it. WARN when the established fact is implied, or when the chapter asserts a new fact about a named character that nothing supports.

Return JSON matching the schema. If there is nothing to report, return an empty findings list. A finding without an exact chapter_quote will be discarded.

CHAPTER
{draft}
```

**Rule critic, Prompt** (System = `system_static`, the same string the writer had):

```
You check one chapter against the rule loadout in your system prompt and against the author notes. You do not judge taste.

For each finding: the rule id from the loadout, the exact span from the chapter, what the rule requires, and a one-line fix. A rule may FAIL only if its summary carries a number, "never", "always", "must" or "ban"; otherwise the finding is a WARN. Also list any rule id cited in the author notes that is not in the loadout (WARN). Do not report the em-dash, antithesis, ladder, reification or sentence-length rules; a separate mechanical pass covers them.

Return JSON matching the schema. An empty findings list is a valid answer.

AUTHOR NOTES
{notes}

CHAPTER
{draft}
```

**Reviser, Prompt** (System = `system_static`):

```
Revise the chapter below against the findings. Frozen, do not change: the beat, the POV, the cast, the kind of ending, the length, the declared lie ("{declared_lie}") and misreading ("{declared_misreading}"). Change only the quoted spans and what they force. Do not summarise, do not add scenes, do not cut a paragraph no finding names. Keep the word count within 15% of the current {word_count}. Return the full chapter in the same JSON schema, with author_notes updated where a fix changed what they claim and the summary unchanged unless a fix changed an event.

FINDINGS (round {round})
{findings, one per line: [FAIL|WARN] pass | rule_id | "chapter_quote" | "source_quote" | fix}

CHAPTER
{draft}
```

### 6.4 Schemas

These go into n8n's Structured Output Parser ("Define using JSON Schema"). That parser is n8n's own: it appends format instructions to the prompt and parses the model's text; it does not send Anthropic's `output_config.format`, so the API-side guarantees (grammar-constrained output, a schema-valid refusal) do not apply here (§7 item 14). The parser rejects `$ref`; the constraints below are also kept inside Anthropic's [structured outputs rules](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) (no `minLength`/`maximum`, every object with `required` and `additionalProperties: false`) so the same schemas move to an HTTP Request node unchanged if the writer is ever moved there.

Writer and Reviser:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["title", "markdown", "author_notes", "summary", "declared_lie", "declared_misreading", "cannot_fix"],
  "properties": {
    "title": {"type": "string"},
    "markdown": {"type": "string"},
    "author_notes": {"type": "string"},
    "summary": {"type": "string"},
    "declared_lie": {"type": "string", "description": "the exact sentence from the chapter"},
    "declared_misreading": {"type": "string", "description": "the exact sentence from the chapter"},
    "cannot_fix": {"type": "string", "description": "empty unless a FAIL cannot be fixed without breaking a frozen element; then the reason"}
  }
}
```

Findings (the model critics; the deterministic passes build the same shape in Code with `pass` = `tell_scan | shape | combat | ledger | voice`):

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["findings"],
  "properties": {
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["severity", "pass", "category", "rule_id", "chapter_quote", "source_quote", "fix", "note"],
        "properties": {
          "severity": {"type": "string", "enum": ["FAIL", "WARN"]},
          "pass": {"type": "string", "enum": ["continuity", "knowledge", "rule", "canon", "beat"]},
          "category": {"type": "string", "enum": ["location", "knowledge", "injury", "item", "relationship", "death", "time", "number", "pov", "rule", "beat", "hook", "other"]},
          "rule_id": {"type": "string"},
          "chapter_quote": {"type": "string"},
          "source_quote": {"type": "string"},
          "fix": {"type": "string"},
          "note": {"type": "string"}
        }
      }
    }
  }
}
```

Extractor (WF-2 only, not v0): `{facts: [{type, subject, fact, quote, confidence}], hooks: [{hook_id, event, quote}], ledger: [{category, who, text, due_after_sessions}], time_elapsed, front_line}` with the same conventions.

### 6.5 Test plan and acceptance

1. Run once with the writer on `claude-sonnet-5` and `previous_scene` blank; confirm every MCP node returns text and the log at `build/mcp_pipeline.log` shows POSTs to `/mcp` (and no 421 lines).
2. Run again within the hour with the same `scene_type`; confirm the second run read more than 20,000 tokens from cache. Where to read it is **to verify** (§3): the Chat Model sub-node's log tab if n8n exposes `cache_read_input_tokens`, otherwise the Anthropic Console's Usage page for the key. If it is zero, `system_static` differs between runs; diff the two strings.
3. Fill `draft_override` with a draft carrying a deliberate em dash and a deliberate antithesis; confirm `verify_scene` FAILs, the Reviser is called, and the second `verify_scene` passes.
4. Fill `tail_override` with a tail that says the POV's arm is broken and give a beat where he climbs; confirm the Continuity critic returns a FAIL with both quotes. This is ConStory's injected-error method and it is the only way to know a critic is not theatre. Then run the same beat without the injected tail and confirm the critic does **not** FAIL; a critic that fails both ways is also theatre.
5. Switch the writer to `claude-opus-5`, run a real beat, answer the Gmail form, and confirm the file in `scenes/`, the Notion page, and the commit in `git log`.

Acceptance: a chapter in `scenes/` that `verify_scene` passes; author notes carrying the nine filled blanks and rule ids; zero Continuity FAILs against the previous scene; at most two revise rounds; the cache hit confirmed; the run's spend under $3 read from the Console (the pipeline has no cost line of its own until n8n's usage exposure is confirmed).

---

## 7. Risks and open questions, each with a recommendation

Decisions are stated so the builder can start; Isaac overrules any of them by saying so.

1. **The container may not reach the server, for two separate reasons.** (a) The MCP SDK's Host-header check answers 421 to `host.docker.internal` in untokened `--http` mode; found at source, certain, fixed by Appendix A's first row. (b) The Docker gateway may not forward to a 127.0.0.1-bound socket; untested. *Recommendation:* the Appendix A change first, then the reachability test in §6.1; if (b) fails, add `--bind` to `mcp_server.py` and a firewall rule limited to the Docker subnet. Never put the untokened server on all interfaces without the rule.

2. **Every write tool commits and pushes; the hourly sync does `pull --rebase` then push.** Three to nine pushes per chapter can collide with the sync at the top of the hour. *Recommendation:* the dispatcher runs at :05, :15, :25 …; WF-2's COMMIT stage checks the minute and waits until :08 if it is between :58 and :07; later, a `--no-push` batch mode on the write tools with one push at the end of COMMIT (Appendix A).

3. **Test chapters pollute the archive and Notion.** `archive_scene` has no dry run. *Recommendation:* v0 archives only after Isaac's approval mail; test runs stop at the mail and he lets them expire; the first real chapter is the first archive.

4. **Prompt iteration on Opus burns money** ([community 90870](https://community.n8n.io/t/help-me-write-my-book/90870)). *Recommendation:* Sonnet 5 as the writer until the prompts settle; switch to Opus 5 for the first real chapter; the monthly spend cap on the key (Start tier $500, **to verify** which tier) is the backstop.

5. **Critics cannot read intent; NATALIE requires lies and misreadings.** *Recommendation:* the writer declares both in its JSON as the exact chapter sentences, the merge node suppresses findings in those paragraphs, and everything else goes through the persisted `overrides`. Review the `overrides` table at every WF-3 run so it does not become a blanket.

6. **A critic can be theatre.** A judge that flips only 38% of the time when the candidate is flipped is not checking anything. *Recommendation:* the injected-error test (§6.5 step 4, both directions) for each critic before it is trusted, and a `critic_test` workflow later that injects one contradiction, one knowledge leak and one canon number into a passed chapter every ten chapters and confirms three FAILs.

7. **Errors cluster in the middle of a book** (40–60% band). *Recommendation:* WF-3 every three chapters between 35% and 65% of the outline, every five elsewhere; in §1.4 step 6 and §1.5.

8. **Flattening and freshness decay.** Revision homogenises voice; AutoNovel saw chapter scores fall after chapter 6 and rhythms repeat. *Recommendation:* the repetition WARN (pass 5), the voice note with an anti-exemplar in every system block, scene types varied by the planner, and a standing WARN when three consecutive chapters share a scene type. Voice fingerprints (`voice_fingerprints`) rebuilt after every ten chapters and injected as a paragraph in the bible.

9. **Which model writes.** *Recommendation:* Opus 5 for the planner, writer, reviser and the whole-manuscript review; Sonnet 5 for critics, extractor and caster. Per-model consistency-error density differs thirtyfold across models ([ConStory](https://arxiv.org/abs/2603.05890)), so the writer and checker are chosen separately; revisit after three chapters by reading the `findings` table.

10. **Which channel for the gates.** *Recommendation:* Gmail Send and Wait, because it needs no bot and reaches the phone; Telegram if reply latency turns out to matter. The n8n Form alternative gives a nicer editor for `instructions` and can be swapped in without changing the branch logic.

11. **Explicit scenes** (Table Rule 9) may be refused by the model. Through n8n's Structured Output Parser a refusal is not schema-valid JSON; it surfaces as a parser failure and a re-ask, then as an empty or short `markdown`. *Recommendation:* the sanity node treats a parser failure that survives the re-ask, or a chapter under 60% of target, as an escalation, not a retry, and the digest counts them. If refusals are frequent on `explicit` chapters, those chapters are written at the table, not by the pipeline. Isaac's call whether explicit chapters go through the pipeline at all; the default here is that they do, and the digest reports what happened.

12. **The book and the table share a thread.** If Isaac plays a Sodoku session while the pipeline writes Sodoku chapters, State of Play diverges from the outline. *Recommendation:* one thread is either being played or being written at a time; WF-0 records a hash of the **State of Play block only** from `session_start` (not the whole output: the Fronts and Ledger blocks change every time the pipeline itself calls `advance_front` or `ledger_add`, which would pause the book after chapter 1), and the dispatcher pauses the book with a mail if that hash changes.

13. **Data Tables: 200 MiB, no Code-node access, limited filters.** *Recommendation:* prose only in `stages` during a run and cleared at commit; ≤ 40 facts per chapter; ten books fit. Every Code node that needs table rows is preceded by a Data Table Get node, and per-cast filtering happens in the Code node, not the Get.

14. **The Anthropic Chat Model node cannot place cache breakpoints or send `output_config.format`** (as of node v1.6; the research found Thinking, Effort and caching options and nothing else). *Recommendation:* accept the node's own caching (system + tools + history) and n8n's Structured Output Parser for now; move the writer to an HTTP Request node if the cache hit rate falls below 80%, if the parser's re-asks become common, or if the 40–70k-token prompt through the LangChain node proves to be a memory problem (§1.4 Stage B). The whole-manuscript review is already HTTP Request.

15. **`session_end` was built for play sessions.** Calling it per chapter makes a chapter a session for the Ledger's ageing, and it also changes what "one lie per session" means for a book. *Recommendation, Isaac's to overrule:* a chapter counts as a session for Table Rules 7 and 8 and for `due()`; it is the only way `due()` ever fires, and Table Rule 7 says the Ledger persists. Its regex-harvested candidates are ignored in favour of the Extractor's.

16. **The verifier's blind spots** (HEMA regex counts "point" and "cut"; dialogue skews sentence stats). *Recommendation:* leave them WARN; do not tune `verify.py` for the pipeline's convenience, since it is the table's tool too. The same blind spot is why Pass 3 is WARN-only.

17. **Six small MCP additions are asked for** (`allowed_hosts`, `arcs_place`, `stale_names_text`, `inventory`, a verify gate on `archive_scene`, optional `--bind`). Only the first is needed for v0. *Recommendation:* Appendix A, under 100 lines, in one commit before WF-2 is built; the `allowed_hosts` change alone before v0.

18. **Narration voices.** Most speakers will be pool picks. *Recommendation:* the digest lists them; Isaac names two or three voices per book in `build/voices.yaml` as the cast settles; casting is skipped, not failed, when the tag check cannot be satisfied.

19. **The pipeline writes Isaac's player character, which NATALIE forbids at the table.** "What you never do: think, speak, or act for Isaac's PC" is a table rule for a game with a live player; a book in the Sodoku Moto thread has no live player, and the same applies to the other creators' characters NATALIE names (Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai). *Default taken here, Isaac's to overrule:* the outline he approves in WF-0 is his PC's decisions; the writer executes what an approved beat says the PC does and originates no decision for him beyond it; the other creators' characters do not appear as POV or as deciders unless the outline names them, in which case Isaac has approved that use. Table Rule 1's turn-taking half ("answer what the PC did … never resolve a multi-decision action in one go") is dropped from the writer's protocol; its ending rule is kept. Table Rule 2's turn bands are replaced by the chapter target. Rules 7 and 8 are read per chapter (item 15). If Isaac wants the PC kept out of the pipeline's hands altogether, the planner is told to build the book on the non-PC cast and the outline review is where he checks it.

---

## Appendix A. Repo changes the pipeline asks for (proposed, small)

All in `build/mcp_server.py` unless noted; none touches `sources/`, `rules/` or the checker.

| tool / flag | what | size | needed for |
|---|---|---|---|
| `allowed_hosts` in untokened `--http` mode | in `main()`, the `if not args.token:` branch passes `transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=True, allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*", "host.docker.internal:*"], allowed_origins=[...the three loopback origins...])` to `server.run(...)`; keeps the rebinding protection, adds the one host the container uses | ~4 lines | v0 |
| `arcs_place(arc: str, file: str, after: str = "")` | append `- <file>` under `## <arc>` in `scenes/ARCS.md`, creating the H2 at the end if missing; idempotent (no duplicate lines); commit + push like the other write tools | ~30 lines | WF-2 |
| `stale_names_text(markdown: str)` | run the `stale_names` regexes (from `build/renames.yaml` and the Reversion Ledger tables) over a string; return the struck terms with their sentences | ~15 lines, mostly reuse | WF-2 |
| `inventory(culture: str)` | return `_inventory(culture)`; the Standing Inventory block without the 20k-token `session_start` around it | ~4 lines | WF-2 (v0 uses `session_start` and a Code split instead) |
| `archive_scene(..., verify: bool = True, band: str = "set-piece", combat: bool = False)` | refuse with the verify report when `verify.run` has any FAIL, unless `verify=False` | ~10 lines | WF-2 |
| `--bind <addr>` on `--http` | only if the reachability test fails on the network hop | ~6 lines | maybe |
| `--no-push` (later) | write tools commit without pushing; a `push_now()` tool pushes once | ~20 lines | later |

## Appendix B. Data Table schemas

`books`: `book_id`, `title`, `thread`, `culture`, `status` (planning | outline_review | active | paused | drafted | done | dropped), `premise`, `cast` (comma list), `voice_note`, `bible` (text), `inventory` (text, the Standing Inventory block), `target_chapters`, `target_words`, `review_mode`, `state_hash` (State of Play block only), `created_at`.

`chapters`: `book_id`, `number`, `title`, `beat`, `scene_type`, `culture`, `band` (always set-piece), `pov`, `cast`, `front_id`, `plants` (comma list of hook ids), `pays`, `time_elapsed`, `target_words`, `status` (planned | running | awaiting_isaac | done | dropped | failed), `job_id` (kept across retries), `started_at`, `retry_count`, `last_reminder`, `summary`, `word_count`, `scene_file`, `rounds`, `fail_final`, `warn_final`, `tokens_in`, `tokens_cached`, `tokens_out`, `audio_path`, `revise_note`.

`stages`: `job_id`, `stage` (brief | draft | draft_r1 | draft_r2 | draft_r3 | check | gate | archive | extract | commit), `status` (done | failed), `output` (text), `error`, `node`, `updated_at`.

`facts`: `book_id`, `chapter_no`, `type` (location | knowledge | injury | item | relationship | death | time | number), `subject`, `fact`, `quote`, `confidence` (stated | implied | provisional), `place`.

`hooks`: `book_id`, `hook_id`, `text`, `keywords` (comma list, 3–5, from the planner; Pass 4 greps for them), `planted_ch`, `due_ch`, `last_ch`, `paid_ch`, `status` (planned | planted | advanced | paid | dropped).

`overrides`: `book_id`, `chapter_no`, `finding_quote`, `rule_id`, `reason`, `decided_at`.

`findings`: `book_id`, `chapter_no`, `job_id`, `round`, `scope` (chapter | book), `severity`, `pass` (tell_scan | shape | combat | ledger | voice | continuity | knowledge | rule | canon | beat), `category`, `rule_id`, `chapter_quote`, `source_quote`, `fix`, `resolved` (fixed | overridden | open).

## Appendix C. Sources used in this design

n8n mechanics: [Loop Over Items](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches/) · [Execute Sub-workflow](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/) · [Wait](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/) · [Data Tables](https://docs.n8n.io/build/work-with-data/data-tables) · [Data Table rows](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.datatable/rows) · [MCP Client Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/) · [MCP Client core node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcpclient) · [Anthropic Chat Model](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatanthropic) · [Structured Output Parser](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.outputparserstructured.md) · [Human in the loop](https://blog.n8n.io/human-in-the-loop-automation/) · [fix memory issues](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/fix-memory-issues) · [executions env vars](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions) · [handle errors](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully) · issues [#23851](https://github.com/n8n-io/n8n/issues/23851), [#24967](https://github.com/n8n-io/n8n/issues/24967), [#10763](https://github.com/n8n-io/n8n/issues/10763) · PRs [#29467](https://github.com/n8n-io/n8n/pull/29467), [#34482](https://github.com/n8n-io/n8n/pull/34482) · community threads [167862](https://community.n8n.io/t/memory-issue-with-loop-over-items-node-done-branch/167862), [99788](https://community.n8n.io/t/n8n-workflow-crashing-on-large-text-input-to-llm-node-high-cpu/99788), [295656](https://community.n8n.io/t/way-to-handle-long-running-ai-workflows-in-n8n-without-execution-timeouts/295656), [90870](https://community.n8n.io/t/help-me-write-my-book/90870).

Book workflows on n8n: [template 2879](https://n8n.io/workflows/2879-book-ghostwriting-and-research-ai-agent/) · [template 3503](https://n8n.io/workflows/3503-generate-written-content-with-gpt-recursive-writing-and-editing-agents/) · [template 5707](https://n8n.io/workflows/5707-create-structured-ebooks-in-minutes-with-google-gemini-flash-20-to-google-docs/) · [yegisyahrial](https://github.com/yegisyahrial/n8n-ai-auto-novel-generator) · [chi-0518](https://github.com/chi-0518/n8n-novel-generator) · [nagoriktech](https://github.com/nagoriktech/E-Book-Generator) · [Del Arroz](https://substack.aicentral.blog/p/i-let-ai-write-three-complete-novels) · [Entangled Text](https://www.entangledtext.com/ai-novel-writing-workflow).

Verification research: [ConStory-Bench](https://arxiv.org/abs/2603.05890) · [Magnet / Atlas](https://arxiv.org/html/2607.00918) · [Dramaturge](https://arxiv.org/html/2510.05188v3) · [LLM Review](https://arxiv.org/html/2601.08003) · [CritiCS](https://arxiv.org/html/2410.02428) · [LitBench](https://arxiv.org/abs/2507.00769) · [rubric artifacts](https://arxiv.org/html/2609.02942) · [EQ-Bench slop score](https://eqbench.com/slop-score.html) · [Sudowrite continuity](https://docs.sudowrite.com/using-sudowrite/1ow1qkGqof9rtcyGnrWUBS/chapter-continuity/4KL8gFeLZQ6GSBjDWtSbV6) · [Barr Group](https://barrgroup.com/software-expert-witness/blog/ai-agents-finished-decade-old-novel).

Open-source book agents: [AutoNovel](https://github.com/NousResearch/autonovel) and [ANTI-SLOP](https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md) · [Novel-OS](https://github.com/mrigankad/Novel-OS) · [AuthorAgent](https://github.com/Ckokoski/AuthorAgent) · [KazKozDev](https://github.com/KazKozDev/NovelGenerator) · [InkOS](https://dev.to/dylan_brown_4c803aefcfe51/building-an-autonomous-ai-agent-that-writes-novels-architecture-of-a-10-agent-pipeline-59pf) · [Claude-Book](https://github.com/ThomasHoussin/Claude-Book) · [story-skills](https://github.com/danjdewhurst/story-skills) · [Book-Agent](https://forum.level1techs.com/t/my-ai-powered-novel-writing-pipeline-book-agent-generating-epistemically-controlled-long-form-fiction/243193).

Anthropic: [models](https://platform.claude.com/docs/en/models/overview) · [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) · [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) · [API errors](https://platform.claude.com/docs/en/api/errors) · [rate limits](https://platform.claude.com/docs/en/api/rate-limits) · [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector) (not used: the WOTR MCP is local and the connector needs public HTTPS).

Repo, read at source on 2026-09-12: `build/mcp_server.py` (tool signatures, `LOADOUTS`, `_slug`, `main()`'s transport settings), `build/verify.py` (`BANDS`, the HEMA regex, `report()`), `desktop/NATALIE.md` (Table Rules, the floor, canon hierarchy), and the installed MCP SDK's `streamable_http_app` (the auto-enabled Host-header check).
