# Driving Claude from n8n for a long multi-step writing job

Research notes, 12 Sept 2026. Every claim below traces to a page fetched or a search result seen during this session; links are at the point of use and collected at the end. "n8n" version numbers are the n8n release; "node vX.Y" is the node's own version inside n8n.

---

## 0. The shape that falls out of the research

An 8-15 minute writing job (load rules + story bible, draft, check, revise, file) should **not** be one Claude call and should **not** be one n8n execution that blocks on the API for 15 minutes. It should be a **chain of 4-8 calls of 1-4 minutes each**, orchestrated by n8n, with:

- the big stable context (rulebook, story bible, tool list) placed first in the request and **prompt-cached** (read cost 10% of base, and cache reads don't count against rate limits);
- each stage's result **checkpointed** to a Data Table or Postgres row keyed by `job_id`, so a retry resumes at the last good stage instead of re-spending tokens;
- the job started from a Webhook that **responds immediately** and hands off to a sub-workflow (or several) that run without a client waiting;
- structured JSON demanded from Claude with `output_config.format` (GA) or n8n's Structured Output Parser, so downstream nodes never parse prose.

The rest of this document is the evidence and the numbers.

---

## 1. Which n8n node to call Claude with

There are three ways in; they expose very different subsets of the API.

### 1a. Anthropic node (the "app" node, `n8n-nodes-langchain.anthropic`)

Operations, per the [Anthropic node docs](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.anthropic): Document > Analyze Document; File > Upload / Get Metadata / List / Delete; Image > Analyze; Prompt > Generate / Improve / Templatize; Text > **Message a Model**.

From the operation source ([message.operation.ts](https://github.com/n8n-io/n8n/blob/master/packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/text/message.operation.ts)), Message a Model exposes: `Messages` (role user/assistant + content), `Simplify Output` (default true), `Add Attachments` (URL or binary), and Options: `System Message`, `Maximum Tokens` (**default 1024** - far too low for prose), `Temperature` (default 1), `Top P` (0.7), `Top K` (5), `Web Search` (+ `Max Uses` default 5, allowed/blocked domains), `Code Execution`, `Include Merged Response`, `Max Tool Calls Iterations` (default 15). The body it builds is `model, messages, tools, max_tokens, system, temperature, top_p, top_k`. I could not find thinking/effort, `output_config`, or `cache_control` in that file; a PR to add prompt caching to this node ([#22318](https://github.com/n8n-io/n8n/pull/22318)) was closed unmerged in May 2026.

**Verdict:** fine for one-shot "Analyze Document" or file upload steps; not the node for the main writing calls.

### 1b. Anthropic Chat Model sub-node + AI Agent root node (LangChain cluster)

This is the pair that has been getting the Claude-specific work.

- **Thinking Mode / Effort** (node v1.5, shipped in n8n 2.20.0, May 2026, [PR #29467](https://github.com/n8n-io/n8n/pull/29467); motivated by [issue #28635](https://github.com/n8n-io/n8n/issues/28635) where the old `thinking: {type:"enabled", budget_tokens}` payload got a 400 from Opus 4.7). Options: `Thinking Mode` = Disabled / Adaptive (Recommended) / Manual (Deprecated); `Effort` dropdown appears under Adaptive. Sampling params are stripped for models that reject them. Manual mode + Opus 4.7+ throws a `NodeOperationError`.
- **Prompt caching** (node v1.6, shipped in n8n 2.37.0, 25 Aug 2026, [PR #34482](https://github.com/n8n-io/n8n/pull/34482), [release notes](https://docs.n8n.io/changelog/release-notes)): Options `Enable Prompt Caching` (off by default) and `Cache TTL` = 5 minutes (default) / 1 hour. The PR says system prompt, tool definitions and conversation history are cached. Caveat from the PR: cache-creation and cache-read tokens are summed into the reported `promptTokens`/`totalTokens`, so n8n's token display is only an approximation of billable usage.
- Other documented options ([docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatanthropic)): `Maximum Number of Tokens`, `Sampling Temperature`, `Top K`, `Top P`.
- **Open problem - no streaming to the API.** [Issue #23851](https://github.com/n8n-io/n8n/issues/23851) (n8n 2.0.3, still open/stale): the sub-node doesn't pass `stream` to the Anthropic SDK, so a large `max_tokens` trips the SDK guard "Streaming is required for operations that may take longer than 10 minutes." The practical fix is to keep each call's `max_tokens` at a size the SDK accepts (see section 4) rather than asking for 64k+ tokens in one node.
- `N8N_AI_TIMEOUT_MAX` (default 3,600,000 ms) is the HTTP timeout for AI/LLM nodes ([executions env vars](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions)).

**AI Agent node** ([Tools Agent docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/tools-agent.md), [AI Agent docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/)): the agent-type selector is deprecated since n8n 1.82.0; everything is the Tools Agent, and v1 is removed in n8n 3.0. Parameters: `Prompt` (from Chat Trigger `chatInput`, or Define below), `Require Specific Output Format` (connect Auto-fixing / Item List / Structured Output Parser), Options: `System Message`, `Max Iterations` (**default 10**), `Return Intermediate Steps`, `Automatically Passthrough Binary Images`, `Enable Streaming` (on by default), and `Batch Processing` with `Batch Size` and `Delay Between Batches` (ms) ([AI Agent Tool docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolaiagent), [issue #19592](https://github.com/n8n-io/n8n/issues/19592)). At least one tool sub-node must be connected.

**What this means for cost:** every agent iteration is a fresh Messages request carrying the full system prompt + tool list + history. Ten iterations over a 60k-token rulebook is 600k input tokens without caching, ~60k-equivalent with it. Turn caching on in the Chat Model node before anything else.

### 1c. HTTP Request node straight at `POST /v1/messages`

Use this when you need a request field the nodes don't expose: `output_config.format` (JSON schema), `output_config.effort`, explicit `cache_control` breakpoints, `mcp_servers`, Files API `file_id` documents, `thinking.display`, task budgets, or the Batches API. [HTTP Request docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest): Options include `Timeout` (ms, waits for response headers), `Batching` (`Items per Batch`, `Batch Interval` ms), `Response Format` Autodetect/JSON/Text/File, pagination. It does **not** consume SSE streams; a community package `n8n-nodes-streaming-http-request` exists for that ([npmx](https://npmx.dev/package/n8n-nodes-streaming-http-request)), but the simpler answer is to size each call so the non-streaming path is safe.

---

## 2. Tools via MCP

### 2a. n8n MCP Client Tool (sub-node for the AI Agent)

[Docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp). Auth: Bearer, Generic header, **Multiple Headers Auth** ("when your MCP server requires more than one header, for example an API key and a username"), OAuth2, None. `Tools to Include`: All / Selected / All Except.

Transport: HTTP Streamable support landed in **n8n 1.104.0 (21 Jul 2025)** via [PR #15454](https://github.com/n8n-io/n8n/pull/15454), which added a transport selector (HTTP Streamable vs deprecated SSE), endpoint fields and custom headers. Third-party guides variously cite 1.112.0; trust the PR.

Two bugs worth knowing:
- [Issue #24967](https://github.com/n8n-io/n8n/issues/24967): the dropdown showed HTTP Streamable but the node kept sending SSE-style GETs; combined with immediate retries this produced ~97.6 million failed requests over 8 days (~47 req/s per workflow). Workaround was to set the `serverTransport` parameter as an expression to the literal string `httpStreamable` and restart; closed with a linked fix PR #34397. Lesson: cap retries on the MCP path and watch server logs after upgrades.
- [Community: "MCP Client Tool times out with HTTP Streamable, but works with SSE"](https://community.n8n.io/t/mcp-client-tool-times-out-with-http-streamable-but-works-with-sse/313086) - some servers still behave better on SSE; keep both endpoints available on your MCP server while testing.

### 2b. n8n MCP Client (core node, runs a tool as a normal step)

[Docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcpclient): `MCP Endpoint URL` (example `https://mcp.notion.com/mcp`), same auth menu, `Server Transport` parameter, Manual or JSON input for tool parameters, `Timeout` (ms), `Convert to Binary`. This is the right node for **deterministic** steps - e.g. call `load_rules` with fixed tags at the start of a job and put the result in the cached system block - rather than letting the agent decide whether to load rules.

### 2c. Let Anthropic run the MCP loop instead: the MCP connector

[MCP connector docs](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector) (beta header `mcp-client-2025-11-20`): put `mcp_servers: [{type:"url", url, name, authorization_token}]` in the request and a matching `tools: [{type:"mcp_toolset", mcp_server_name}]` entry (both halves are required). Claude calls the tools **inside one Messages request**; results come back as `mcp_tool_use` / `mcp_tool_result` blocks. Only tool calls are supported (no prompts/resources); the server must be publicly reachable over HTTPS (Streamable HTTP or SSE); `mcp_toolset` accepts `cache_control`; per-tool allow/deny via `default_config` and `configs`; works in the Batches API; not ZDR-eligible.

For the WOTR MCP, which is local, this route needs a public HTTPS tunnel with a bearer token; the n8n sub-node can reach it over the LAN without that. The trade: connector = fewer n8n iterations and one API call per stage; n8n sub-node = you see every tool call in the execution log.

---

## 3. Prompt caching and cost control for repeated large contexts

Numbers from [prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and [models overview](https://platform.claude.com/docs/en/models/overview):

| Item | Value |
|---|---|
| Cache write, 5-min TTL | 1.25x base input |
| Cache write, 1-hour TTL | 2x base input |
| Cache read | 0.1x base input (Opus 5: $0.50/MTok vs $5 base) |
| Minimum cacheable prefix | 512 tokens Opus 5 / Fable 5.x; 1,024 Sonnet 5, Sonnet 4.6, Opus 4.8; 4,096 Haiku 4.5 |
| Breakpoints per request | max 4 |
| Prefix order | `tools` -> `system` -> `messages`; a change invalidates that level and everything after |
| Lookback | up to 20 blocks back from a breakpoint |
| TTL clock | starts at **request start**, not response end; a 4-minute generation leaves ~1 minute of a 5-minute TTL |
| Verify | `usage.cache_read_input_tokens` > 0; `input_tokens` counts only tokens after the last breakpoint |
| Top-level shortcut | `"cache_control": {"type":"ephemeral"}` at the request root auto-caches the last cacheable block |
| Rate-limit bonus | cache reads do **not** count toward ITPM ([rate limits](https://platform.claude.com/docs/en/api/rate-limits)) |

Invalidators that matter in a writing pipeline: changing `output_config.effort` or thinking settings (model-specific), toggling web search, changing tool definitions or order, editing the system prompt, and - reported by n8n users - thinking-block signatures in tool-loop history that differ run to run ([community thread](https://community.n8n.io/t/anthropic-prompt-caching-for-tool-heavy-agents-in-n8n/299640); the same thread measured ~75% cut in input tokens from caching the system prompt alone). Changing `output_config.format` also invalidates ([structured outputs docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)).

**Prompt shape for a chapter job** (HTTP Request body; the same layering applies inside the Chat Model node, which puts system + tools first):

```json
{
  "model": "claude-opus-5",
  "max_tokens": 12000,
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "high"},
  "system": [
    {"type": "text", "text": "<house style + hard constraints; never changes>"},
    {"type": "text", "text": "<live rules dump from load_rules, regenerated only when packs change>",
     "cache_control": {"type": "ephemeral", "ttl": "1h"}},
    {"type": "text", "text": "<story bible / character cards for this arc>",
     "cache_control": {"type": "ephemeral", "ttl": "1h"}}
  ],
  "messages": [
    {"role": "user", "content": "<prior chapter summaries + this scene brief + job_id>"}
  ]
}
```

Keep timestamps, job IDs and the varying brief **after** the last breakpoint. Use the 1-hour TTL because a multi-stage job with 2-4 minute calls and n8n hops between them will blow past 5 minutes.

Other levers:
- **1M context is the default** on Opus 5 / Sonnet 5 / Fable 5.x, no beta header, standard pricing; max output 128k per request ([context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)). Context rot is real, so curate rather than dump.
- **Files API** ([docs](https://platform.claude.com/docs/en/build-with-claude/files)): upload the rulebook/bible once (`text/plain` or PDF, 500 MB per file, 1 TB per org, no beta header, uploads are free, content billed as input tokens), reference as `{"type":"document","source":{"type":"file","file_id":...}}`; document blocks can be cached. The n8n Anthropic node has the Upload File operation.
- **Batches API** ([docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing)): 50% off everything; 100,000 requests or 256 MB per batch; most finish under 1 hour, hard 24-hour expiry, results kept 29 days; pair with the 1-hour cache TTL; `max_tokens: 0` pre-warm not allowed inside a batch; up to 300k output tokens with beta `output-300k-2026-03-24`. Good for overnight drafts of many scenes or parallel continuity checks; useless for a job someone is waiting on.
- **Rate limits** ([docs](https://platform.claude.com/docs/en/api/rate-limits)): Start tier Opus 5 and Sonnet 5 = 1,000 RPM / 2,000,000 ITPM / 400,000 OTPM; Fable 5.x = 1,000 / 500,000 / 100,000. Monthly spend caps: Start $500, Build $1,000. A tier-cap 429 has no `retry-after`.
- **Model prices** ([models overview](https://platform.claude.com/docs/en/models/overview)): Fable 5.1 $10/$50; Opus 5 $5/$25; Sonnet 5 $2/$10; Haiku 4.5 $1/$5 per MTok. Thinking is adaptive on the 5-series with effort default `high`; `budget_tokens` is rejected on 4.7+.

---

## 4. Handling 8-15 minute runs inside n8n

### 4a. The two clocks

1. **Anthropic's clock.** [API errors docs](https://platform.claude.com/docs/en/api/errors): "Consider using the streaming Messages API or Message Batches API for long-running requests, especially those over 10 minutes"; the SDKs refuse non-streaming requests they expect to exceed 10 minutes; 504 `timeout_error` is the failure mode. Since neither the n8n Chat Model node (issue #23851) nor the HTTP Request node streams, **size each call so it finishes well inside 10 minutes** - in practice `max_tokens` of roughly 8k-16k per call and one scene or one revision pass per call, not a whole chapter in one request.
2. **n8n's clock.** [Executions env vars](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions): `EXECUTIONS_TIMEOUT` default **-1** (no timeout); `EXECUTIONS_TIMEOUT_MAX` default **3600 s** (ceiling for the per-workflow "Timeout Workflow After" setting, [workflow settings](https://docs.n8n.io/build/manage-workflows/configure-workflow-settings)). On n8n Cloud the per-plan ceiling is not published; staff say to ask help@n8n.io ([community](https://community.n8n.io/t/maximum-workflow-execution-timeout-on-n8n-cloud-trial-starter-and-pro/303146)). Self-hosted with the default -1, a 15-minute execution is legal; the risk is the process being restarted mid-run, which is what queue mode and checkpoints address.

### 4b. Queue mode (self-hosted)

[Enable queue mode](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode): `EXECUTIONS_MODE=queue`; Redis (`QUEUE_BULL_REDIS_HOST/PORT/DB/PASSWORD`, `QUEUE_BULL_REDIS_TIMEOUT_THRESHOLD=10000` ms); Postgres, not SQLite; `N8N_ENCRYPTION_KEY` shared by main + workers; worker default concurrency **10** (`n8n worker --concurrency=5` recommended minimum to spare the DB pool); `N8N_GRACEFUL_SHUTDOWN_TIMEOUT=30` s - **raise this** (e.g. 900) or a redeploy will kill a 12-minute run; `N8N_CONCURRENCY_PRODUCTION_LIMIT` default -1. `N8N_WORKFLOW_AUTODEACTIVATION_ENABLED` (default false) would unpublish a workflow after 3 crashed runs - leave it off while tuning.

### 4c. Splitting the job so nothing waits 15 minutes

The pattern recommended in the [community thread on long-running AI workflows](https://community.n8n.io/t/way-to-handle-long-running-ai-workflows-in-n8n-without-execution-timeouts/295656):

1. **Webhook** node with Respond = *Immediately* (HTTP 200 back before any Claude call).
2. **Execute Sub-workflow** with `Wait For Sub-Workflow Completion` **off** ([docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow)) - the sub-workflow gets its own execution and its own timeout clock.
3. Inside, one stage per Claude call: `load context -> draft -> continuity check -> revise -> file`. After each stage, **Upsert** a Data Table / Postgres row `{job_id, stage, status, output_ref}`; at the start of each stage, **If Row Exists** with `status = done` -> skip. Make each stage idempotent so a retry does not double-spend.
4. For human review or an external callback mid-job, use the **Wait** node with Resume = *On Webhook Call* and send `$execution.resumeUrl` to wherever the approval happens; set `Limit Wait Time` so the job doesn't hang forever ([Wait docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait)). Waits over 65 seconds offload execution data to the database, which is what makes them survive restarts; n8n 2.0 fixed Wait-in-sub-workflow return data ([blog](https://blog.nocodecreative.io/n8n-v2-wait-node-hitl-sub-workflows/), [issue #13135](https://github.com/n8n-io/n8n/issues/13135)).
5. For fan-out (several scenes at once), the template [Run multiple tasks in parallel with asynchronous processing and webhooks](https://n8n.io/workflows/8578-run-multiple-tasks-in-parallel-with-asynchronous-processing-and-webhooks/) uses Execute Sub-workflow (no wait) + a Wait node that each child calls back to; or use **Loop Over Items** (`Batch Size`, `loop`/`done` outputs, [docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches)) with the AI Agent's `Batch Processing` option to throttle.

Payload hygiene: `N8N_PAYLOAD_SIZE_MAX` defaults to 16 MB ([community](https://community.n8n.io/t/existing-execution-data-is-too-large/256344)); do not pass a 60k-token rulebook from node to node as item JSON - fetch it inside the stage (MCP Client core node, or Files API `file_id`) and let caching absorb the cost. Enable `Save Execution Progress` in workflow settings only while debugging (it adds latency).

---

## 5. Retries and structured output

**n8n node settings** ([Handle rate limits](https://docs.n8n.io/integrations/builtin/handle-rate-limits), [HTTP Request common issues](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/common-issues), [issue #10763](https://github.com/n8n-io/n8n/issues/10763)): `Retry On Fail` with `Max. Tries` (capped at 5) and `Wait Between Tries` (ms, capped at 5,000); `On Error` = Stop Workflow (default) / Continue / Continue (using error output). **If On Error is either Continue option, the retry settings are ignored** - the node continues on the first failure. Workflow-level: Error Workflow + Error Trigger node, and the Stop And Error node to force a failure ([Handle errors gracefully](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully)).

**Anthropic side** ([errors](https://platform.claude.com/docs/en/api/errors)): retry 429 (honour `retry-after`), 500, 504, 529 overloaded; don't retry 400/401/403/413. Request size cap 32 MB on Messages. Because n8n's per-node retry maxes at 5 tries x 5 s, put a longer back-off in a Wait node on the error branch (e.g. 60-120 s) for 529s.

**Structured output** ([structured outputs docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), GA, no beta header): `output_config: {format: {type:"json_schema", schema:{...}}}` (the old `output_format` is deprecated). Schema rules: every object needs `additionalProperties: false` and `required`; no external `$ref`, no `minimum/maximum/minLength/maxLength`, arrays only `minItems: 0|1`; enums of primitives only. The SDKs strip unsupported constraints and validate locally; a raw HTTP Request node does not, so keep the schema legal. First use of a schema compiles a grammar (extra latency), cached 24 h; name/description changes don't invalidate it. A refusal still returns schema-valid JSON. `strict: true` on tool definitions gives the same guarantee for tool inputs. Assistant prefill is a 400 on 4.6+ models, so JSON-by-prefill is dead - use `output_config.format`.

In n8n: enable `Require Specific Output Format` on the AI Agent and attach a **Structured Output Parser** ([docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.outputparserstructured.md)) with `Generate From JSON Example` (all fields required) or `Define using JSON Schema` (`$ref` not supported); an Auto-fixing Output Parser variant will re-ask the model on a parse failure. For stage outputs that feed a Data Table, a small schema like `{chapter_id, scene_id, status, word_count, rule_ids_applied[], text}` keeps the rest of the workflow expression-safe.

---

## 6. Keeping state between runs

| Store | What it's good for | Concrete facts |
|---|---|---|
| **n8n Data Tables** | job/stage checkpoints, per-scene status, small metadata | Project-scoped, built in, no external DB. Operations: Get, Insert, Update, Upsert, Delete, If Row Exists / If Row Does Not Exist, Clear (added n8n 2.31); filters Equals / Not Equals / Greater / Less / Is Empty; `Must Match` Any/All; Dry Run on writes; Order By + Limit on Get ([rows docs](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.datatable/rows)). Storage cap is instance-wide: the Build docs page says 200 MiB default, an older page/search says 50 MB; both cite `N8N_DATA_TABLES_MAX_SIZE_BYTES` for self-hosted, warning at 80% ([data tables docs](https://docs.n8n.io/build/work-with-data/data-tables)). Not for the prose itself. |
| **Postgres** | the prose, run logs, anything you want to query later; agent memory | Postgres node for a `jobs` / `stages` table; **Postgres Chat Memory** sub-node (`Session Key`, `Table Name`, `Context Window Length`) if you want the AI Agent to remember prior turns across executions - multiple memory nodes share one store unless you vary the session ID ([docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorypostgreschat)). Queue mode already requires Postgres. |
| **Notion** | human-facing state (docket, rulings, chapter pages) | Reachable from n8n via the Notion node or the MCP Client core node; this repo already mirrors to Notion hourly, so write finished output there and keep machine state in Data Tables/Postgres. |
| **Files** | the corpus | Anthropic Files API `file_id` for rulebook/bible (see section 3); n8n binary data on disk via `N8N_DEFAULT_BINARY_DATA_MODE=filesystem` for drafts/exports. |

Two cautions on carrying **conversation transcripts** (rather than outputs) between runs: thinking blocks must be passed back byte-identical with their signatures or the API returns a 400 ([errors](https://platform.claude.com/docs/en/api/errors)), and on Fable 5.1 replayed thinking blocks are bound to an unchanged prefix. Storing stage *outputs* and re-prompting is simpler and cache-friendlier than persisting the agent's message array.

---

## 7. What current Claude models offer that matters here

From [models overview](https://platform.claude.com/docs/en/models/overview) and [context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows):

- Opus 5 (`claude-opus-5`), Sonnet 5, Fable 5.1: **1M context, 128k max output**, adaptive thinking (effort `low`..`max`, default `high`), structured outputs GA, strict tool use, MCP connector (beta), Files API (GA), Batches (GA, 50% off), prompt caching (GA, min 512 tokens on Opus 5). Sonnet 5 also has "context awareness" (the API tells it its remaining token budget after each tool call); Opus 5 and Fable don't, but support task budgets (beta).
- Server-side **compaction** (beta) summarises earlier turns when a session approaches the window; **context editing** clears old tool results - both only matter if you keep a single conversation running for the whole job, which section 4 argues against.
- 200k-window models (Haiku 4.5) are fine for cheap continuity checks against the cached bible.

---

## 8. Pitfalls checklist

1. Anthropic node `Maximum Tokens` default 1024 - raise it or prose gets truncated.
2. Chat Model node does not stream; asking for 64k+ tokens in one call trips the SDK's 10-minute guard (#23851). Split calls.
3. Turn `Enable Prompt Caching` (node v1.6, n8n >= 2.37.0) on; keep the varying brief last; use the 1-hour TTL for multi-stage jobs.
4. Changing effort, tools, output schema or the system prompt mid-job invalidates the cache.
5. MCP Client Tool transport bugs (#24967): verify with server logs that POSTs arrive; cap retries on that path.
6. `On Error: Continue` silently disables `Retry On Fail`.
7. `N8N_GRACEFUL_SHUTDOWN_TIMEOUT` default 30 s kills long runs on redeploy - raise it in queue mode.
8. n8n Cloud publishes no timeout ceiling; self-hosted `EXECUTIONS_TIMEOUT=-1` means no limit unless you set one per workflow (max 3600 s by default).
9. Don't shuttle the rulebook through item JSON (16 MB payload default, DB bloat); fetch it inside the stage.
10. Structured-output schemas cannot use `minLength`/`maximum`/external `$ref`; n8n's Structured Output Parser rejects `$ref` outright.
11. Prefill is gone on 4.6+; use `output_config.format`.
12. Batches expire at 24 h and are not for anything interactive.

---

## Sources

Anthropic docs
- Models overview: https://platform.claude.com/docs/en/models/overview
- Context windows: https://platform.claude.com/docs/en/build-with-claude/context-windows
- Prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Batch processing: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- MCP connector: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
- Files API: https://platform.claude.com/docs/en/build-with-claude/files
- Errors / long requests: https://platform.claude.com/docs/en/api/errors
- Rate limits: https://platform.claude.com/docs/en/api/rate-limits
- Streaming: https://platform.claude.com/docs/en/build-with-claude/streaming

n8n docs
- Anthropic node: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.anthropic
- Anthropic Chat Model: https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatanthropic
- AI Agent: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/ and Tools Agent: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/tools-agent.md
- AI Agent Tool (batch options): https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolaiagent
- Structured Output Parser: https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.outputparserstructured.md
- MCP Client Tool: https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp
- MCP Client (core): https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcpclient
- HTTP Request: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest
- Wait: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait
- Execute Sub-workflow: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow
- Loop Over Items: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches
- Data tables: https://docs.n8n.io/build/work-with-data/data-tables and row operations: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.datatable/rows
- Postgres Chat Memory: https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorypostgreschat
- Executions env vars: https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/executions
- Enable queue mode: https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode
- Workflow settings: https://docs.n8n.io/build/manage-workflows/configure-workflow-settings
- Handle errors gracefully: https://docs.n8n.io/build/flow-logic/handle-errors-gracefully
- Handle rate limits: https://docs.n8n.io/integrations/builtin/handle-rate-limits
- Release notes: https://docs.n8n.io/changelog/release-notes

GitHub / community
- PR #15454 HTTP Streamable for MCP Client Tool: https://github.com/n8n-io/n8n/pull/15454
- Issue #24967 transport dropdown ignored: https://github.com/n8n-io/n8n/issues/24967
- Issue #23851 Chat Model doesn't stream: https://github.com/n8n-io/n8n/issues/23851
- Issue #28635 legacy thinking payload vs Opus 4.7: https://github.com/n8n-io/n8n/issues/28635
- PR #29467 Thinking Mode / Effort: https://github.com/n8n-io/n8n/pull/29467
- PR #34482 prompt caching in Chat Model v1.6: https://github.com/n8n-io/n8n/pull/34482
- PR #22318 (closed) caching for Anthropic app node: https://github.com/n8n-io/n8n/pull/22318
- Issue #10763 Retry On Fail vs On Error Continue: https://github.com/n8n-io/n8n/issues/10763
- Issue #19592 AI Agent batch processing bug: https://github.com/n8n-io/n8n/issues/19592
- Community: long-running AI workflows without timeouts: https://community.n8n.io/t/way-to-handle-long-running-ai-workflows-in-n8n-without-execution-timeouts/295656
- Community: Cloud timeout ceilings: https://community.n8n.io/t/maximum-workflow-execution-timeout-on-n8n-cloud-trial-starter-and-pro/303146
- Community: prompt caching for tool-heavy agents: https://community.n8n.io/t/anthropic-prompt-caching-for-tool-heavy-agents-in-n8n/299640
- Community: does n8n support Anthropic prompt caching: https://community.n8n.io/t/does-n8n-support-anthropic-prompt-caching-in-the-ai-agent-node/301467
- Community: MCP Client Tool times out on HTTP Streamable: https://community.n8n.io/t/mcp-client-tool-times-out-with-http-streamable-but-works-with-sse/313086
- Community: payload size: https://community.n8n.io/t/existing-execution-data-is-too-large/256344
- Template: parallel tasks with async sub-workflows + webhooks: https://n8n.io/workflows/8578-run-multiple-tasks-in-parallel-with-asynchronous-processing-and-webhooks/
- Blog: n8n 2.0 Wait node fix in sub-workflows: https://blog.nocodecreative.io/n8n-v2-wait-node-hitl-sub-workflows/
- Community node for streaming HTTP: https://npmx.dev/package/n8n-nodes-streaming-http-request
