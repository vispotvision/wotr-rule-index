# The MCP's twelve writing tools cannot commit or push from an agent worktree

Verified read-only on 2026-09-25 from the worktree
`/home/oridon/.paperclip/worktrees/wotr/WAR-22-docket-apply-answered-rulings-batch-new-questions`,
for WAR-112 (and WAR-104, the same defect found independently from WAR-62). No
file under `build/` was changed and nothing was pushed: `build/*.py` and
`build/*.sh` are on the extractor's never-edit list, so this report is the
diagnosis and the spec, and the patch is WAR-121's.

`log_ruling` is the named subject of both issues because `CLAUDE.md` house rule
2.2 makes it the only sanctioned writer of `RULINGS.md` — "written ONLY by the
`log_ruling` tool: never edit it by hand, never commit it from your worktree".
It is not the only tool with the defect. **Twelve tools reach a commit and a
push, through six push sites**, and all six are the same two lines.

## The six push sites and the twelve tools

| `build/mcp_server.py` | tools that reach it |
|---|---|
| `:210-212` `archive_scene` | `archive_scene` |
| `:232-234` `log_ruling` | `log_ruling` |
| `:603-605` `propose_rule` | `propose_rule` |
| `:901-903` `create_character` | `create_character` |
| `:925-927` `update_character` | `update_character` |
| `:1071-1073` `_table_commit` | `advance_front` `:1106`, `set_front_clock` `:1118`, `add_front` `:1125`, `ledger_add` `:1145`, `ledger_collect` `:1155`, `npc_set` `:1172`, `session_end` `:1251` |

Every one of the six ends in the identical line:

```python
    pcode, pout = _git("push", "-q", "origin", "master")
```

The extractor's house rules name nine of those tools (`archive_scene`,
`log_ruling`, `propose_rule`, `update_character`, `create_character`,
`ledger_add`, `advance_front`, `session_end`, `npc_set`). **Three commit and
push without being named anywhere**: `set_front_clock`, `add_front` and
`ledger_collect`, all three through `_table_commit`.

## Defect 1 — ROOT is the worktree, not the repo

`build/common.py:8` is

```python
ROOT = Path(__file__).resolve().parent.parent
```

and `mcp_server.py` runs every subprocess with `cwd=ROOT` (`:64`) and resolves
`RULINGS = ROOT / "RULINGS.md"` (`:48`). `.mcp.json` starts the server with
relative paths (`"args": ["build/py.sh", "build/mcp_server.py"]`), and
`build/env.sh` cds to the repo it finds from its own location:

```bash
WOTR_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
export WOTR_REPO
cd "$WOTR_REPO" || exit 1
```

So a session started in a worktree gets a server whose `ROOT` is that worktree.
This is not inference: `mcp_server.py:141` builds the server's own instructions
out of `str(ROOT)`, and the instructions this session was handed read "Tools over
the War of the Realms rule index at
`/home/oridon/.paperclip/worktrees/wotr/WAR-22-docket-apply-answered-rulings-batch-new-questions`".

**A trap for the fix.** `env.sh` sets `WOTR_REPO` from `BASH_SOURCE` *before* it
reads `~/.config/wotr/env`, and its loader only fills a key that is unset or
empty (`_cur="${!_key:-}"; [ -n "$_cur" ] || _cur="$_val"`). The config file's
own `WOTR_REPO` — a key `build/wotr.env.example` documents — is therefore
ignored in a worktree, and cannot be the lever. Resolving the repo from
`$WOTR_REPO` requires changing `env.sh` too.

## Defect 2 — it commits the file onto the issue branch

`:232-233` is `git add -- RULINGS.md` then `git commit`, run with `cwd=ROOT`.
In a worktree that is a commit on the issue branch, which is the exact act
house rule 2.2 forbids. The other five sites do the same for `scenes/`,
`proposals/PROPOSED.md`, `wiki/`, `wiki/.manifest.json` and `table/`.

## Defect 3 — the push cannot reach the commit

`git push origin master` pushes the local `refs/heads/master`. Refs are shared
across a worktree and its main checkout, so `master` is whatever the main
checkout has committed — never the commit just made in the worktree. Reproduced
today, dry run, nothing pushed:

```
$ git push --dry-run origin master
 ! [rejected]        master -> master (non-fast-forward)
hint: Updates were rejected because a pushed branch tip is behind its remote
hint: counterpart.
```

That is the same message all six WAR-96 calls returned. The local `master` was
39 commits behind `origin/master` on the morning of 2026-09-25 and is **64
behind** as this is written; the gap only grows, because nothing in the agent
flow ever advances it.

**The worse case is the one that succeeds.** The rejection is loud. If the main
checkout's `master` were ever ahead of `origin/master` instead of behind, the
same line would exit 0, push the main checkout's commits, and the tool would
report `pushed` for a ruling that is still sitting on an issue branch. The same
false success arrives if the main checkout is on any branch other than `master`:
the commit lands on that branch and `push origin master` reports on a ref that
does not contain it.

## What it has already cost

`3215399` became "the unpushed hand-edit of `RULINGS.md`" (CONTINUE.md, the
WAR-46 block), left the branch's ancestry on the next `git rebase origin/master`,
and left R44-1..R44-6 as index rows quoting an entry that existed nowhere —
WAR-96, at the cost of a run each to WAR-46, WAR-48 and WAR-72. WAR-62 could not
log six reviewer-approved rulings at all (WAR-104).

**Canon is intact as of this report.** `origin/master:RULINGS.md` carries all six
2026-09-25 R44 entries (WAR-96 pushed `HEAD:master` by hand in the same run), and
no branch in the repo holds a `RULINGS.md` commit that is not on `origin/master`:

```
$ for b in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
      git rev-list --count origin/master.."$b" -- RULINGS.md; done
(every branch: 0)
```

## The spec

The recommendation is **operate on the main checkout**, not refuse in a
worktree, on two grounds that are not style preferences:

1. House rule 2.2 forbids committing `RULINGS.md` from a worktree *and* makes
   `log_ruling` its only writer. A `log_ruling` that refuses in a worktree
   leaves an agent ruling with no sanctioned route at all, which is the
   condition WAR-104 calls "every agent ruling is unshippable".
2. The extractor's house rules state as fact that these tools "commit and push
   from the main checkout themselves". That sentence lives in an agent
   instructions file, which no agent may edit. The code has to be made true,
   not the promise weakened.

Against that: the main checkout is not always safe to write into. WAR-29 had it
mid-rebase with `RULINGS.md` unresolved for nineteen consecutive sync runs. So
the main checkout is the target, and the pre-flight is what makes it safe.

1. **Resolve the repo, not the worktree.** `dirname "$(git rev-parse
   --git-common-dir)"` returns `/home/oridon/wotr-rule-index` from here and the
   same path from the main checkout, so it needs no branch on the caller. The
   linked-worktree test itself is `.git` being a file rather than a directory.
   One helper, used by all six sites; `ROOT` keeps meaning "the tree I read".
2. **Pre-flight, and refuse in words if it fails**: the main checkout is on
   `master`, is not mid-rebase or mid-merge (`.git/rebase-merge`,
   `.git/rebase-apply`, `MERGE_HEAD`), and has nothing uncommitted in the paths
   about to be touched. A refusal must name the path and the reason.
3. **Push the commit, not a ref that may be stale.** `git push origin
   <sha>:refs/heads/master` for the sha the commit just produced.
   `HEAD:master` is right only while HEAD is `master`; the sha is right always.
   Fetch and rebase first, or the 64-commit gap rejects every push regardless.
4. **Three outcomes, not two.** `:235` joins a success clause and a failure
   clause with "; " — `logged ruling on C-038; push failed: ...` — so a caller
   reading the first half believes the entry shipped. Written, committed and
   pushed are three steps; say which one stopped, and say plainly that the
   entry is committed-but-unpushed when it is.
5. **Then make the tool lists match the code**: `set_front_clock`, `add_front`
   and `ledger_collect` commit and push and are named nowhere.

Nothing above changes which rulings exist, and nothing above is a canon
decision. Whether to take the recommendation is WAR-121's to make; it touches
all twelve tools and the live units (`wotr-mcp-public`, `wotr-bot`,
`wotr-jobs`) that load the same file.
