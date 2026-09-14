export const meta = {
  name: 'judger-assist',
  description: "The Judger's assistant: read an archived scene (from Discord or the table) and draft the session close for Isaac to approve — Ledger lines, Front ticks, NPC wants and lies, rulings and docket items, contradictions with the cards and the timeline, a player-safe recap. Writes bot/queue/<slug>.judger.md + .json; writes nothing to the table.",
  whenToUse: 'After /scene save archives a Discord scene, or any time a scene lands in scenes/ without a session close; args {scenes: [slugs] | "latest", thread?: "Kharven thread, the year after"}',
  phases: [{ title: 'Gather' }, { title: 'Read' }, { title: 'Propose' }, { title: 'Check' }, { title: 'Note' }],
}
// ------------------------------------------------------------------ setup
const A = Object.assign({ scenes: 'latest', thread: '' }, args || {})
const REPO = 'C:\\Users\\isaac\\Documents\\wotr-rule-index'
const T = 'python build/book_tools.py'
const Q = 'bot\\queue'
const STANDING = `Repo: ${REPO}; run every command from there; output is UTF-8 (set PYTHONIOENCODING=utf-8). sources/, rules/, wiki/, scenes/ and table/ are READ-ONLY for this run: never commit; never call session_end, ledger_add, advance_front, npc_set, log_ruling, propose_rule, archive_scene or any MCP tool that writes. This run produces files under ${Q}\\ only — proposals the Judger (Isaac) approves or rejects one by one. The read-only tools are a command line: ${T} <tool> ... (no arguments lists them). CLAUDE.md binds: rules are quoted verbatim by id, never paraphrased into existence; a conflict is recorded, never resolved; nothing is invented — every claim about the scene carries a verbatim quote from it.`

// which scenes
let slugs = Array.isArray(A.scenes) ? A.scenes : (A.scenes === 'latest' ? [] : String(A.scenes).split(',').map(s => s.trim()).filter(Boolean))
if (!slugs.length) {
  const pick = await agent(`${STANDING}
Find the scene most recently ADDED to the archive: run \`git log --diff-filter=A --name-only --pretty=format: -- "scenes/*.md"\` and take the first path that is a scene (not scenes/cast/, not CAST.md, TIMELINE.md, ARCS.md, MANIFEST.md, INDEX.md). Modification time is not the signal — sweeps touch old files. Return ONLY that file's slug (its name without .md), nothing else.`, { label: 'pick:latest', phase: 'Gather', effort: 'low' })
  slugs = [String(pick || '').trim().split(/\s+/)[0].replace(/\.md$/, '')].filter(Boolean)
}
log(`scenes: ${slugs.join(', ') || '(none)'}`)

const ASSERTIONS = { type: 'object', properties: { thread: { type: 'string' }, pov: { type: 'string' }, place: { type: 'string' }, when: { type: 'string' },
  present: { type: 'array', items: { type: 'string' } },
  facts: { type: 'array', items: { type: 'object', properties: {
    kind: { type: 'string', enum: ['death', 'injury', 'reserve', 'item', 'debt', 'promise', 'knows', 'lie', 'reputation', 'movement', 'number', 'relationship', 'other'] },
    who: { type: 'string' }, fact: { type: 'string' }, quote: { type: 'string', description: 'verbatim from the scene, 8-40 words' } }, required: ['kind', 'who', 'fact', 'quote'] } },
  questions: { type: 'array', items: { type: 'string' }, description: 'what the scene left open, in one line each' },
  last_line: { type: 'string' } }, required: ['thread', 'pov', 'place', 'when', 'present', 'facts', 'questions', 'last_line'] }

const PROPOSALS = { type: 'object', properties: { proposals: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' },
  tool: { type: 'string', enum: ['ledger_add', 'advance_front', 'set_front_clock', 'add_front', 'npc_set', 'log_ruling', 'propose_rule', 'card_note', 'timeline_note', 'inventory_note', 'conflict_note'] },
  args: { type: 'object', description: 'the exact arguments the MCP tool takes (ledger_add: category, who, text, due_after_sessions|due_condition; advance_front: front_id, what_happened, next_move; npc_set: name, thread, want, refusal_line, knows[], lied_about[], last_seen; log_ruling: rule_id, ruling, context; propose_rule: title, rule_text, applies_to[], rationale). For *_note tools: {target, note}.' },
  quote: { type: 'string', description: 'the verbatim sentence(s) from the scene this rests on' },
  why: { type: 'string' },
  confidence: { type: 'string', enum: ['high', 'medium', 'low'] } }, required: ['id', 'tool', 'args', 'quote', 'why', 'confidence'] } } }, required: ['proposals'] }

const VERDICTS = { type: 'object', properties: { verdicts: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, keep: { type: 'boolean' }, reason: { type: 'string' }, fix: { type: 'string', description: 'if keep with a change: the corrected args as JSON text; else empty' } }, required: ['id', 'keep', 'reason', 'fix'] } } }, required: ['verdicts'] }

const results = await pipeline(slugs,
  // ---------------------------------------------------------------- gather
  (slug) => agent(`Gather the Judger's file for the scene scenes/${slug}.md. ${STANDING}
Run, and write the outputs verbatim into ONE file ${Q}\\${slug}.gather.md under these headings, in this order:
1. "## Scene" — the full text of scenes/${slug}.md.
2. "## Thread" — the thread this scene belongs to: ${A.thread ? `Isaac says "${A.thread}"; use it.` : `look the slug up in scenes/ARCS.md (its arc) and match the arc to a thread name in table/fronts.yaml (${T} fronts with no argument lists every thread); state the match as an assumption in one line.`}
3. "## Lorebook" — ${T} scene_context scenes/${slug}.md (cards and pages for every name, prior scenes on the same ground, struck terms, names with no page).
4. "## Verification" — ${T} verify <path> --band standard (add --combat if the scene has a fight).
5. "## Fronts" — ${T} fronts "<thread>"; "## Due" — ${T} due 1 "<thread>"; "## Roster" — ${T} roster "<thread>".
6. "## Timeline" — the rows of scenes/TIMELINE.md for this scene and the four before it in reading order, and the scene's line in scenes/ARCS.md.
7. "## Docket" — ${T} check_docket adjudication scene-structure prose-law; "## Conflicts" — ${T} list_conflicts.
8. "## Ledger" — table/LEDGER.md in full (what already stands, so nothing is proposed twice).
Return the thread you settled on as the first line exactly \`thread: <name>\`, then the word count of the scene and whether verification reported any FAIL.`, { label: `gather:${slug}`, phase: 'Gather', effort: 'low' }).then(r => ({ slug, gather: r, thread: (String(r || '').match(/^thread:\s*(.+)$/m) || [])[1] || A.thread })),

  // ---------------------------------------------------------------- read (two independent readers)
  (g) => parallel([
    () => agent(`You are the reader of record for scene ${g.slug}. ${STANDING}
Read ${Q}\\${g.slug}.gather.md — the "## Scene" section is the text; the "## Lorebook" section is what the wiki says about everyone in it. Extract what the scene ESTABLISHES as fact: deaths, injuries and what they cost, reserve spent, items gained/lost/broken, debts and promises, who now knows what (and who does not), lies told and left uncorrected, reputation (who saw), movement (where everyone ends up), numbers stated, relationships changed. One row per fact, each with a verbatim quote of 8-40 words. Also: the thread, the POV, place, in-world moment as far as the text states it, everyone present, the open questions, and the last line. Do not infer beyond the page; "probably" is not a fact.`, { label: `facts:${g.slug}`, phase: 'Read', schema: ASSERTIONS, effort: 'high' }),
    () => agent(`You are the rules clerk for scene ${g.slug}. ${STANDING}
Read ${Q}\\${g.slug}.gather.md (the scene, its verification report, the docket, the conflicts). Then ${T} load_rules adjudication scene-structure prose-law --brief and, if the scene has a fight, ${T} load_rules combat stats --brief. Report, as plain text under three headings: (1) "Rulings made in play" — any place the scene text itself records a ruling (a Judger's call, an adjudication card, an author note saying "ruling:"), quoting it, with the rule id it touches if one exists; (2) "Rule questions the scene raised" — moments where the live rules do not settle what happened, quoting the moment and the nearest rule by id and verbatim text; (3) "Contradictions" — where the scene contradicts a card in the lorebook section, a timeline row, or a live rule: quote both sides. Nothing else; no prose notes.`, { label: `rules:${g.slug}`, phase: 'Read', effort: 'high' }),
  ]).then(([facts, rules]) => ({ ...g, facts, rules })),

  // ---------------------------------------------------------------- propose
  (r) => agent(`You are the table clerk for scene ${r.slug} on thread "${r.thread}". ${STANDING}
Inputs: ${Q}\\${r.slug}.gather.md (Fronts, Due, Roster, Ledger, Lorebook sections), the reader's facts (JSON below), and the rules clerk's report (below). Draft the proposals the Judger will approve one by one, each as the EXACT MCP call it would become:
- ledger_add for every fact that costs or binds: category one of "the dead" | "injuries and reserve" | "debts" | "who knows what" | "reputation" | "canon conflicts"; who; the line in the Ledger's register (one sentence, present tense, specific); due_after_sessions (a number) or due_condition (a stated condition). Skip anything already on the Ledger.
- advance_front for each Front on the thread the scene moved (Table Rule 4: at least one per session): front_id from the Fronts section, what_happened as the consequence the PC saw, next_move. If nothing moved any Front, say so in one proposal of tool "inventory_note" with target "fronts" explaining why, so the Judger decides.
- npc_set for every NPC whose want, refusal line, knowledge or lies the scene changed: name, thread, and only the fields that changed (knows[] and lied_about[] as short strings; last_seen as the scene slug).
- log_ruling for each ruling the rules clerk found recorded in play; propose_rule for a rule question that needs a rule (title, rule_text as it would read in a pack, applies_to tags from schema/applies_to.md, rationale).
- card_note when the scene asserts something about a character their card does not carry or contradicts (target = card title, note = what and the quote) — Isaac updates cards, not you.
- timeline_note for the scene's row (target = slug, note = the in-world moment as stated); conflict_note when the scene sits on an open conflict (target = C-id).
- inventory_note for anything invented this scene that the Standing Inventory should carry (R6-9-RECURRENCE_RULE).
Every proposal carries the verbatim quote it rests on and a confidence. Do not propose what you cannot quote. Ids: P01, P02...

Reader's facts:
${JSON.stringify(r.facts, null, 1)}

Rules clerk:
${r.rules}`, { label: `propose:${r.slug}`, phase: 'Propose', schema: PROPOSALS, effort: 'high' }).then(p => ({ ...r, proposals: p ? p.proposals : [] })),

  // ---------------------------------------------------------------- check (adversarial)
  (r) => agent(`You are the skeptic for scene ${r.slug}. Try to KILL each proposal below, then say which survive. ${STANDING}
Open ${Q}\\${r.slug}.gather.md. For each proposal: (1) is the quote actually in the "## Scene" section, verbatim? (search for it); (2) does the proposal say more than the quote supports (an inference dressed as a fact, a number the page does not give, a motive the POV could not know)? (3) is it already on the Ledger / already the Front's recorded state / already on the card (check the Ledger, Fronts and Lorebook sections)? (4) are the args well-formed for the tool named (front_id exists in the Fronts section; category is one of the six; applies_to tags exist in schema/applies_to.md)? keep=false if any of (1)-(3) fails; if only (4) fails, keep=true with the corrected args in "fix". Be exact; a wrong Ledger line outlives the session.

Proposals:
${JSON.stringify(r.proposals, null, 1)}`, { label: `check:${r.slug}`, phase: 'Check', schema: VERDICTS, effort: 'high' }).then(v => {
    const vs = new Map((v ? v.verdicts : []).map(x => [x.id, x]))
    const kept = r.proposals.filter(p => vs.get(p.id) && vs.get(p.id).keep).map(p => {
      const fx = vs.get(p.id).fix
      if (fx) { try { return { ...p, args: JSON.parse(fx), fixed: true } } catch (e) { return p } }
      return p
    })
    const killed = r.proposals.filter(p => !vs.get(p.id) || !vs.get(p.id).keep).map(p => ({ ...p, reason: vs.get(p.id) ? vs.get(p.id).reason : 'no verdict' }))
    return { ...r, kept, killed }
  }),

  // ---------------------------------------------------------------- note
  (r) => agent(`Write the Judger's note for scene ${r.slug} (thread "${r.thread}"). ${STANDING}
Write TWO files:
1. ${Q}\\${r.slug}.judger.json — exactly this JSON: {"scene": "${r.slug}", "thread": "${r.thread}", "proposals": <the kept proposals below, verbatim, each with id, tool, args, quote, why, confidence>, "rejected": <the killed proposals: id, tool, reason>}. The Discord bot posts each proposal as a card with approve/reject buttons; approve runs the tool with those args. So the args must be exactly what the tool takes.
2. ${Q}\\${r.slug}.judger.md — for Isaac, in this order, plain and short:
   "# Judger's note — <scene title> — ${r.thread}"
   "## Recap for the players" — five sentences at most, only what was on the page, no numbers the players did not see, no NPC interiors.
   "## What the scene settled" — the reader's facts as a bulleted list, each with its quote in italics.
   "## For your approval" — the kept proposals grouped by tool (Ledger / Fronts / NPCs / Rulings and proposals / Cards / Timeline / Inventory), one line each: [id] the call in words, the quote, confidence. Anything the skeptic corrected says "(args corrected)".
   "## Set aside" — the killed proposals, one line each with the skeptic's reason.
   "## Contradictions and open questions" — from the rules clerk and the reader; and every "name with no page" from the lorebook section of the gather file.
   "## Verification" — FAIL/WARN counts from the gather file's Verification section and the FAIL lines verbatim.
   Last line: "Approve in Claude Desktop (tell Natalie the ids), in Claude Code (/judger apply ${r.slug} P01 P03 ...), or in Discord when the bot posts the cards. Nothing above has been written to the table."
Return the note's "## For your approval" section as text.

Kept proposals:
${JSON.stringify(r.kept, null, 1)}

Killed proposals:
${JSON.stringify(r.killed, null, 1)}

Reader's facts:
${JSON.stringify(r.facts, null, 1)}

Rules clerk:
${r.rules}`, { label: `note:${r.slug}`, phase: 'Note', effort: 'medium' }).then(n => ({ slug: r.slug, thread: r.thread, kept: r.kept.length, killed: r.killed.length, note: `${Q}\\${r.slug}.judger.md`, approval: n })),
)

const done = results.filter(Boolean)
log(`judger notes: ${done.length}/${slugs.length}; ${done.reduce((n, r) => n + r.kept, 0)} proposals for approval, ${done.reduce((n, r) => n + r.killed, 0)} set aside`)
return { scenes: done.map(r => ({ slug: r.slug, thread: r.thread, kept: r.kept, killed: r.killed, note: r.note })), approval: done.map(r => `### ${r.slug}\n${r.approval}`).join('\n\n') }
