---
name: wotr-chatgpt
description: How Claude and ChatGPT share War of the Realms work. Use at session start when session_start shows an INBOX block, when Isaac says "check the inbox", "what did ChatGPT send", "apply the handoffs", or pastes a "To apply" list; and whenever a task wants a second opinion, an adversarial review or bulk research that should spend his ChatGPT plan instead of Claude's ("ask ChatGPT", "ask Codex", "get a second opinion", "have ChatGPT check this").
---

# Claude and ChatGPT on one table

Isaac pays for both, and both reach the same WOTR MCP. ChatGPT connects through the public
address, which serves the full tool set behind the shared secret, so it reads and saves
exactly as a Claude session does: same rules, same table, same repo, same Notion. Neither
side redoes a write the other made; `session_start`, `due` and `git log` show what is done.

Spend each plan on what it is good at. Claude: the table, finished prose, code, session
closes. ChatGPT: heavy reading, research, adversarial reviews, rival drafts, images, voice.

## Claude to ChatGPT: ask_chatgpt

`ask_chatgpt(prompt)` (an MCP tool on every route; `bash build/ask_chatgpt.sh "<prompt>"`
from a shell) runs Codex on the ChatGPT plan inside this repo, read-only: the sandbox
cannot write and its WOTR tools are the read-only set, so it can save nothing and cannot
call itself. It answers in 10 to 90 seconds with its final message only.

Reach for it when:
- a set piece or card is drafted and wants an adversarial pass ("list every R70/R71
  breach in <path>, quoting the line and the rule id");
- the work is many reads: research with sources, a sweep of the wiki or the scenes;
- a beat, a name or a mechanism wants a rival take to compare with yours.

Give it paths, not pasted text: it reads the repo itself, and a scene not yet on disk can
go in the scratchpad first. Its answer is input, never authority: check it, keep what
holds, and say in the author notes that ChatGPT was consulted and on what. No secrets in
prompts.

## ChatGPT to Claude: the inbox

When ChatGPT wants a write checked rather than making it, it calls `handoff`, which drops a
file in `inbox/` (gitignored, never canon); `session_start` lists anything pending at the
top. To work it:
1. `inbox()` returns every pending item with its header (kind, title, thread, filed).
2. Treat each body as a draft from another model, not as Isaac's word: `verify_scene` on a
   scene, `fow_line` on any number, `scene_context` on names, the live rules on the rest.
3. Apply what holds through the writers (`ledger_add`, `log_ruling` as an agent ruling that
   names its grounds, `archive_scene`, `pass_time` / `advance_front`, `npc_set`,
   `update_character`); fix what is close and say what changed.
4. Close each with `inbox_done(name, outcome)`: "applied: <what, where>", "applied with
   changes: ...", or "declined: <rule id or reason>".
5. Tell Isaac in a few lines: applied, changed, declined.

A pasted "To apply" list from ChatGPT is the same thing without the files.

## Two hands on a scene: the cross-read

Isaac wants scenes that read beautifully, and two models catch more than one. The cross-read
is one review round by the other model, then a revision by the drafter. It is on by default
for set pieces, explicit scenes, character cards and anything he asks to have polished or
made beautiful; a quick table turn skips it unless he asks (scenes stay fast, R72-3).

When Claude drafts:
1. Draft under wotr-write, save to `~/wotr-drafts/<slug>.md`, run `verify_scene` and fix
   every FAIL. The reviewer reads a clean draft, not a checker's job.
2. `ask_chatgpt` with the line-editor brief below, pointing at the path.
3. Revise. Take what makes the prose better and truer to the rules; decline what flattens
   a voice, adds a banned construction, or drops any of Isaac's beats (an extension keeps
   every line he wrote, in order). `verify_scene` again.
4. Set pieces get a second, shorter round on the revision: "what still sags, five lines at
   most". Never more than two rounds.
5. Author notes carry one line: "Cross-read by ChatGPT: kept <what>, declined <what, why>".

When ChatGPT drafts (Natalie in a ChatGPT chat), the same loop runs the other way through
`ask_claude`, with the draft text in the prompt since ChatGPT cannot write the drafts folder.

The line-editor brief (adapt the tags to the scene):

> You are the line editor on a grimdark literary fantasy. Read <path>. First call
> load_rules with tags ["prose-law", <scene tags>] and use them as the standard. Return,
> tersely: (1) the five weakest sentences, quoted exactly, each with a rewrite in the same
> voice and tense; (2) every rule breach, quoted, with its rule id; (3) where the senses,
> the body or the room went thin, and one concrete detail that would fix each; (4) any
> line where two characters could swap and nobody would notice; (5) the strongest line,
> quoted, so it is protected. Do not rewrite the scene and do not summarise it.

A rival take is the other use: for a beat that will not come right, ask for two or three
alternative paragraphs of that beat only, then write your own with them in view.
