# n8n and WOTR

n8n orchestrates; the Windows host executes; Claude Code does the thinking.

## Why it is split that way

n8n runs in Docker (`C:\Users\isaac\Documents\n8n\docker-compose.yml`, port 5678). Two
things it cannot do, and no amount of workflow gets around either:

1. **It cannot call Claude.** Its Anthropic node wants an API key, and there is none.
2. **It cannot run anything here.** The container is Linux, holds no mount of this
   repo, and its Execute Command node runs *inside the container* — so it can reach
   neither `claude.exe` nor the PowerShell scripts nor `G:\My Drive`.

So the schedule → call Claude → call the tools → write files work happens on the
Windows side, and n8n reaches it over HTTP. What n8n is genuinely good at — waiting,
branching, retrying, and fanning out to Discord, mail and a phone — it keeps.

```
n8n container                    Windows host
  Schedule / webhook  ──POST──▶  build/jobs_server.py  (127.0.0.1:8799)
                                   └─▶ build/nightly.ps1 ─▶ claude -p ─▶ the digest
                                   └─▶ build/book_dispatch.ps1 ─▶ the book-chapter workflow
  Fetch the digest    ──GET───▶  /digest
  Send to Discord  ◀────────────┘
```

Docker Desktop lets a container reach the host's loopback as `host.docker.internal`,
so the listener binds to `127.0.0.1` only: n8n gets in, the LAN does not.

## The job runner

`build/jobs_server.py`, registered as the logon task **WOTR jobs** by
`build/jobs_setup.ps1` (`-Remove` to unregister). It takes a **job name**, never a
command and never a prompt — nothing in it executes arbitrary text.

| | |
|---|---|
| `GET /health` | what it is and which jobs exist (no token needed) |
| `POST /run/<job>` | start one; a JSON body may carry `{"slug": "..."}` for the book |
| `GET /status/<job_id>` | state, exit code, the tail of its log |
| `GET /jobs` | the last twenty runs |
| `GET /digest` | `reports/nightly.md`, as markdown |
| `GET /book` | where the book stands (`build/book_next.py --json`) |

Jobs: `nightly`, `book`, `book_dry`, `sync`, `backup`, `checks`.

Every request but `/health` carries the shared secret from `build/.jobs_token` as the
header `X-Job-Token`. That file is gitignored: paste it into n8n once, as a credential,
and never into a chat, a commit or a workflow export.

## Setting it up in n8n, once

1. `powershell -ExecutionPolicy Bypass -File build\jobs_setup.ps1` (already done).
2. In n8n → **Credentials → New → Header Auth**: name `X-Job-Token`, value the string
   in `build/.jobs_token`. Call the credential `WOTR jobs`.
3. **Workflows → Import from File** → `n8n/WOTR_nightly.json`. Open each HTTP Request
   node and pick the `WOTR jobs` credential.
4. In **Send it to Isaac**, paste a Discord channel webhook URL (Channel → Edit →
   Integrations → Webhooks), then enable the node. A Gmail or Telegram node does just
   as well — that is the one place this is a matter of taste.
5. Activate the workflow. It fires at 03:30, runs the nightly on the host, waits,
   fetches the digest and sends you the readable half.

**If you activate it, turn the Windows task off** so the nightly does not run twice:
`Disable-ScheduledTask -TaskName "WOTR nightly"`. The same holds for `WOTR book` if you
move the book dispatcher into n8n. Leave them registered — they are the fallback for
any morning Docker is down.

## Worth building next, in this shape

- **The book, with the gate in the loop.** n8n POSTs `/run/book` at 02:00, then reads
  `/book`; when the answer is `blocked` it sends the gate digest to Discord with two
  buttons, and the reply drives `python build/book_next.py --approve N`. That makes the
  approval something you do from your phone rather than at this desk.
- **Ollama for the cheap mechanical passes.** `host.docker.internal:11434` is up with
  six models. Speaker-tagging a cast file, a tell-bank scan, a first-pass name sweep —
  work that does not touch prose or canon and should not spend subscription tokens.
  Anything it produces is checked by the deterministic tools before it counts.
- **A webhook front door.** `/run/sync` behind an n8n webhook gives a phone shortcut
  that forces a sync without opening anything.

## What not to put in n8n

- **Qdrant under the lore search.** `build/embed_index.py` already indexes the wiki and
  the archive with bge-small and re-embeds only what changed (0.1 s when nothing did).
  A second vector store is a second thing to keep true.
- **The writing itself.** The checked loop lives in `.claude/workflows/book-chapter.js`
  where the rule index, the verifier and the gate are. n8n starts it; it does not
  reimplement it.
