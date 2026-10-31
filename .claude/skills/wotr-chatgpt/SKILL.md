---
name: wotr-chatgpt
description: How Claude and ChatGPT share War of the Realms work, including images (chatgpt_image). Use at session start when session_start shows an INBOX block, when Isaac says "check the inbox", "what did ChatGPT send", "apply the handoffs", or pastes a "To apply" list; and whenever a task wants a second opinion, an adversarial review or bulk research that should spend his ChatGPT plan instead of Claude's ("ask ChatGPT", "ask Codex", "get a second opinion", "have ChatGPT check this"), and whenever an image, portrait, map sketch or scene illustration is wanted.
---


> **Superseded in part, 2026-10-31.** Isaac chose to offload only when he asks: Claude does abilities, cards, stats, maps and research in-session, and uses `ask_chatgpt`, Codex or image calls only when he says so. The division of systems to ChatGPT and prose to Claude below no longer governs.

# Claude and ChatGPT on one table

Isaac pays for both, and both reach the same WOTR MCP. ChatGPT connects through the public
address, which serves the full tool set behind the shared secret, so it reads and saves
exactly as a Claude session does: same rules, same table, same repo, same wiki (`wiki/`, the Obsidian vault; Notion is retired). Neither
side redoes a write the other made; `session_start`, `due` and `git log` show what is done.

Spend each plan on what it is good at. Claude: the table, finished prose, code. ChatGPT:
heavy reading, research, adversarial reviews on request, rival drafts, images. Both load
the rulebook the same lean way: the brief rulebook once a session, a domain's full text on
first use, no re-read after compaction (R79-8).

## Claude to ChatGPT: ask_chatgpt

`ask_chatgpt(prompt)` (an MCP tool on every route; `bash build/ask_chatgpt.sh "<prompt>"`
from a shell) runs Codex on the ChatGPT plan inside this repo, read-only: the sandbox
cannot write and its WOTR tools are the read-only set, so it can save nothing and cannot
call itself. It answers in 10 to 90 seconds with its final message only.

Reach for it when:
- Isaac asked for a cross-read or second opinion on a draft, a card or a ruling (R79-8:
  on request only);
- the work is many reads: research with sources, a sweep of the wiki or the scenes;
- a beat, a name or a mechanism wants a rival take to compare with yours.

Give it paths, not pasted text: it reads the repo itself, and a scene not yet on disk can
go in the scratchpad first. Its answer is input, never authority: check it, keep what
holds, and say in the archive notes that ChatGPT was consulted and on what. No secrets in
prompts.

## Research: research_chatgpt

`research_chatgpt(question, thread)` hands a real-world question to ChatGPT with live web
search and returns at once; the cited write-up lands in the inbox as a `research` item in 2
to 10 minutes (phenomenon, governing law with measured figures, limits, failure modes and
costs, fictional precedent, numbered sources it actually opened). Fire it the moment Isaac
sketches an ability or a wound needs real numbers, keep working, and read it with `inbox`
before the mechanism goes on the page. It is outside research: figures from it may enter a
card or the notes with their source, never a rule's verbatim. Close it with `inbox_done`
("used in <card or scene>"). The Gemini `research` tool is the synchronous alternative.

## Images: chatgpt_image

Claude cannot draw; `chatgpt_image(prompt, name)` borrows ChatGPT's image model on the
ChatGPT plan (30 to 120 s). The picture comes back inline, saved to `~/wotr-drafts/images/`,
with a link under the token. Brief it like a painter: subject, setting, light, palette,
medium, framing; WOTR looks like Arcane and Fullmetal Alchemist, the settings of Bleach and Naruto, Final Fantasy and Lord of the Mysteries, vivid and magitech-lit, never muted gray (R53-28, R78-4). It letters signs and
dials with Earth words on its own ("London" on a gauge), so ask for no text or give the
exact WOTR words. Describe a style instead of naming a living artist, and no real
person's likeness (Isaac's rule). Explicit content is refused by OpenAI's model.

## ChatGPT to Claude: the inbox

Since 2026-10-17 `handoff` carries only research and images (R79-12); ChatGPT makes its own
table writes, and its scene ends are silent upkeep like Claude's. `session_start` lists
anything pending in `inbox/` (gitignored, never canon). To work it:
1. `inbox()` returns every pending item with its header (kind, title, thread, filed).
2. Treat each body as another model's work, not Isaac's word: check any figure against
   `fow_line` and the sources by field (R79-10) before it reaches a card or a scene.
3. Use what holds (a research write-up in a card's phenomenon line or the archive notes,
   an image in its page) and close each with `inbox_done(name, outcome)`: "used in
   <card or scene>" or "declined: <reason>".

A pasted "To apply" list from an older ChatGPT chat is worked the same way: verify, apply
what holds as silent upkeep, say in a line what was applied and what declined.

## Two hands on a scene: the cross-read

Isaac wants scenes that read beautifully, and two models catch more than one. The
cross-read runs only when he asks for it ("cross-read", "cross-check", "ask ChatGPT",
"second opinion"; R79-8); otherwise nothing goes to the other model. When asked: one review
round by the other model, then a revision by the drafter. One round for a turn or an
improvement, two for a set piece. If the other model fails or runs past five minutes, post
without it and say so in one line.

When Claude drafts:
1. Draft under wotr-write, save to `~/wotr-drafts/<slug>.md`, run `verify_scene` and fix
   every FAIL. The reviewer reads a clean draft, not a checker's job.
2. `ask_chatgpt` with the line-editor brief below, pointing at the path.
3. Revise. Take what makes the prose better and truer to the rules; decline what flattens
   a voice, adds a banned construction, or loses Isaac's intent (an improvement of his post
   is a free rewrite that keeps his intent, R79-8). `verify_scene` again.
4. Set pieces get a second, shorter round on the revision: "what still sags, five lines at
   most". Never more than two rounds; a turn or an improvement gets one.
5. Nothing is printed under a turn (R79-2); the archive notes carry one line when the scene
   is archived: "Cross-read by ChatGPT: kept <what>, declined <what, why>".

When ChatGPT drafts (Natalie in a ChatGPT chat), the same loop runs the other way through
`ask_claude`, with the draft text in the prompt since ChatGPT cannot write the drafts folder.

The line-editor brief (adapt the tags to the scene):

> You are the line editor on a dark shonen cultivation fantasy written as literary prose. Read <path>. First call
> load_rules with tags ["prose-law", <scene tags>] and use them as the standard. Return,
> tersely: (1) the five weakest sentences, quoted exactly, each with a rewrite in the same
> voice and tense; (2) every rule breach, quoted, with its rule id; (3) where the senses,
> the body or the room went thin, and one concrete detail that would fix each; (4) any
> line where two characters could swap and nobody would notice; (5) the strongest line,
> quoted, so it is protected. Do not rewrite the scene and do not summarise it.

A rival take is the other use: for a beat that will not come right, ask for two or three
alternative paragraphs of that beat only, then write your own with them in view.
