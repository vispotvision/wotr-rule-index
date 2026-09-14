# n8n and WOTR

n8n orchestrates; the host executes; Claude Code does the thinking.

## Why it is split that way

n8n runs in Docker (`n8n/docker-compose.yml` in this repo, port 5678). Two things it
cannot do, and no amount of workflow gets around either:

1. **It cannot call Claude.** Its Anthropic node wants an API key, and there is none.
2. **It cannot run anything here.** The container holds no mount of this repo, and its
   Execute Command node runs *inside the container* — so it can reach neither the
   `claude` CLI nor the scripts under `build/` nor the Drive mount.

So the schedule → call Claude → call the tools → write files work happens on the
host, and n8n reaches it over HTTP. What n8n is genuinely good at — waiting,
branching, retrying, and fanning out to Discord, mail and a phone — it keeps.

```
n8n container                    the host
  Schedule / webhook  ──POST──▶  build/jobs_server.py  (127.0.0.1:8799)
                                   └─▶ build/nightly.sh ─▶ claude -p ─▶ the digest
                                   └─▶ build/book_dispatch.sh ─▶ the book-chapter workflow
  Fetch the digest    ──GET───▶  /digest
  Send to Discord  ◀────────────┘
```

The compose runs n8n with `network_mode: host`: on Linux Docker there is no bridge
from a container to the host's loopback (that was a Docker Desktop convenience, and
`extra_hosts` lands on the LAN address, not 127.0.0.1), so the container shares the
host's network instead. From inside it, `http://127.0.0.1:8799` is the job runner,
`127.0.0.1:11434` is Ollama and `127.0.0.1:8765` is the MCP's HTTP mode. The
listener still binds `127.0.0.1` only: n8n gets in, the LAN does not. With host
networking there is no `ports:` line; n8n listens on 5678 as before.

## The job runner

`build/jobs_server.py`, the systemd user unit **wotr-jobs.service** (installed and
enabled by `build/systemd_setup.sh` with the rest; `journalctl --user -u wotr-jobs`
and `build/.jobs_server.log`). It takes a **job name**, never a command and never a
prompt — nothing in it executes arbitrary text.

| | |
|---|---|
| `GET /health` | what it is and which jobs exist (no token needed) |
| `POST /run/<job>` | start one; a JSON body may carry `{"slug": "..."}` for the book |
| `GET /status/<job_id>` | state, exit code, the tail of its log |
| `GET /jobs` | the last twenty runs |
| `GET /digest` | `reports/nightly.md`, as markdown |
| `GET /book` | where the book stands (`build/book_next.py --json`) |

Jobs: `nightly` (`bash build/nightly.sh`), `book` (`bash build/book_dispatch.sh`),
`book_dry` (the same with `--dry-run`), `sync` (`bash build/sync.sh`), `backup`
(`bash build/backup.sh`), `checks` (`build/nightly.py` alone: the numbers, no
Claude, no commit).

Every request but `/health` carries the shared secret from `build/.jobs_token` as the
header `X-Job-Token`. The runner writes that file on its first start; it is
gitignored: paste it into n8n once, as a credential, and never into a chat, a commit
or a workflow export. (`--bind ADDR`, repeatable, adds a listener on another
address; the unit passes none, so it is loopback only.)

## Setting it up in n8n, once

1. Join the docker group (`sudo usermod -aG docker oridon`, then log out and in),
   then `cd ~/wotr-rule-index/n8n && docker compose up -d` and open
   http://localhost:5678. `docker compose down` stops it and keeps the `n8n_data`
   volume (credentials, workflows); `down -v` drops the volume too. Do not run the
   old four-service compose at the same time — both name their container `n8n`.
2. The job runner is already up: `systemctl --user status wotr-jobs` (or
   `bash build/systemd_setup.sh` if it is not).
3. In n8n → **Credentials → New → Header Auth**: name `X-Job-Token`, value the string
   in `build/.jobs_token` (`cat` it in your own terminal). Call the credential
   `WOTR jobs`.
4. **Workflows → Import from File** → `n8n/WOTR_nightly.json`. Its three HTTP Request
   nodes already point at `http://127.0.0.1:8799/...`; open each and pick the
   `WOTR jobs` credential.
5. In **Send it to Isaac**, paste a Discord channel webhook URL (Channel → Edit →
   Integrations → Webhooks), then enable the node. A Gmail or Telegram node does just
   as well — that is the one place this is a matter of taste.
6. Activate the workflow. It fires at 03:30 (the container's clock is
   `GENERIC_TIMEZONE`, the machine's zone), runs the nightly on the host, waits,
   fetches the digest and sends you the readable half.

**If you activate it, turn the timer off** so the nightly does not run twice:
`systemctl --user disable --now wotr-nightly.timer`. The same holds for
`wotr-book.timer` if you move the book dispatcher into n8n. Leave the unit files
installed — `systemctl --user enable --now wotr-nightly.timer` brings the fallback
back for any morning Docker is down.

## Worth building next, in this shape

- **The book, with the gate in the loop.** n8n POSTs `/run/book` at 02:00, then reads
  `/book`; when the answer is `blocked` it sends the gate digest to Discord with two
  buttons, and the reply drives `python build/book_next.py --approve N`. That makes the
  approval something you do from your phone rather than at this desk.
- **Ollama for the cheap mechanical passes.** `127.0.0.1:11434` once `ollama-rocm` is
  installed on this machine (the compose already sets `OLLAMA_HOST` to it). Speaker-tagging
  a cast file, a tell-bank scan, a first-pass name sweep — work that does not touch
  prose or canon and should not spend subscription tokens. Anything it produces is
  checked by the deterministic tools before it counts.
- **A webhook front door.** `/run/sync` behind an n8n webhook gives a phone shortcut
  that forces a sync without opening anything.

## What not to put in n8n

- **Qdrant under the lore search.** `build/embed_index.py` already indexes the wiki and
  the archive with bge-small and re-embeds only what changed (0.1 s when nothing did).
  A second vector store is a second thing to keep true.
- **The writing itself.** The checked loop lives in `.claude/workflows/book-chapter.js`
  where the rule index, the verifier and the gate are. n8n starts it; it does not
  reimplement it.
