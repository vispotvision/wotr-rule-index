---
name: wotr-ask-claude
description: Have Claude check or improve War of the Realms work through the WOTR MCP tool ask_claude. Use ONLY when Isaac asks for it: a cross-read or cross-check of a scene, turn, card or technique, or a second opinion on a ruling, a name, a number or a mechanism ("ask Claude", "have Claude check this", "cross-read", "second opinion").
---

# Asking Claude

The WOTR connector has a tool `ask_claude(prompt)`. It runs Claude, as Natalie with the
full rule index, on Isaac's Claude plan, and returns its answer in 10 to 120 seconds.
Claude works read-only: it can read the repo, the rules, the cards, the wiki and the
scenes, and it cannot save anything. You stay the author of what you post; its answer
is input to weigh, never an order.

Claude cannot see this chat. Every prompt must carry what it needs: the draft text itself
(paste it in full), the thread, the scene type, and anything Isaac said about the beat.
For things already on disk (a card, an archived scene, a rule), give the name or path and
let it look them up.

## The cross-read (scenes, cards, techniques)

1. Draft. Run `verify_scene` and fix every FAIL first: Claude should read a clean draft.
2. Call `ask_claude` with the draft and this brief, adapting the tags to the scene:

   > You are the line editor on a dark shonen cultivation fantasy written as literary prose. First call load_rules with
   > tags ["prose-law", <scene tags>] and use them as the standard. Here is the draft:
   > <full text>. Return, tersely: (1) the five weakest sentences, quoted exactly, each
   > with a rewrite in the same voice and tense; (2) every rule breach, quoted, with its
   > rule id; (3) where the senses, the body or the room went thin, and one concrete detail
   > that would fix each; (4) any line two characters could swap without anyone noticing;
   > (5) the strongest line, quoted, so it is protected. Do not rewrite the scene and do
   > not summarise it.

3. Revise. Take what makes the prose better and truer to the rules. Decline what flattens
   a voice, adds a banned construction, or loses Isaac's intent (improving his post is a
   free rewrite that keeps his intent, R79-8).
4. `verify_scene` again.
5. A set piece gets one more short round on the revision: "What still sags? Five lines at
   most, quoted, with rewrites." Never more than two rounds.
6. Nothing is printed under a turn (R79-2). When the scene is archived, the archive notes
   carry one line: "Cross-read by Claude: kept <what>; declined <what, why>."

This runs only when Isaac asks for it (R79-8, in NATALIE.md); otherwise
post without it and say nothing. One round for a turn or an improvement, two for a set piece.
If `ask_claude` fails or runs past five minutes, post without it and say so in one line.

## Other uses

- **Rival take.** For a beat that will not come right, ask for two or three alternative
  paragraphs of that beat only, then write your own with them in view.
- **Second opinion.** A ruling, a name, a number or a mechanism: state the question, your
  answer and your grounds, and ask Claude to find what is wrong with it.
- **Canon check.** "Does this contradict anything in the cards, the timeline or the
  archived scenes? Quote what it contradicts."

## Rules of use

- One question per call, specific. Broad prompts get slow, vague answers.
- No secrets, tokens or personal data in prompts.
- If `ask_claude` fails or times out, say so in one line and go on without it: never stall
  the table on it.
- Saving stays with you: the cross-read changes the draft; when the scene ends you make
  the silent upkeep and the archive (`session_end`) as NATALIE.md says, once.
