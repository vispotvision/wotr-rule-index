export const meta = {
  name: 'book-chapter',
  description: 'One chapter of a War of the Realms book, Claude Code as the orchestrator: foundation (once), brief, draft, checks, bounded revise, then the digest for Isaac (nothing is archived here)',
  whenToUse: 'Writing a book chapter through the checked loop from n8n/BOOK_PIPELINE.md without n8n; args {slug, thread, front_thread, culture, chapter, do_foundation, premise, target_chapters, target_words}',
  phases: [{ title: 'Foundation' }, { title: 'Brief' }, { title: 'Draft' }, { title: 'Check' }, { title: 'Revise' }, { title: 'Digest' }],
}
// ------------------------------------------------------------------ setup
const A = Object.assign({ slug: 'kharven-year', thread: 'Sodoku Moto', front_thread: 'Kharven', culture: 'Kharven',
  chapter: 1, do_foundation: false, premise: '', target_chapters: 12, target_words: 3500, max_rounds: 3 }, args || {})
const REPO = 'C:\\Users\\isaac\\Documents\\wotr-rule-index'
const BOOK = `${REPO}\\book\\${A.slug}`
const CH = String(A.chapter).padStart(2, '0')
const DIR = `${BOOK}\\ch${CH}`
const T = `python build/book_tools.py`   // run from ${REPO}
const FINDINGS = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: {
  severity: { type: 'string', enum: ['FAIL', 'WARN'] }, pass: { type: 'string' }, quote: { type: 'string' },
  problem: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['severity', 'pass', 'quote', 'problem'] } } }, required: ['findings'] }
const MERGE = { type: 'object', properties: { fail: { type: 'integer' }, warn: { type: 'integer' }, dropped: { type: 'integer' }, verdict: { type: 'string', enum: ['pass', 'revise', 'escalate'] }, top: { type: 'array', items: { type: 'string' } } }, required: ['fail', 'warn', 'dropped', 'verdict', 'top'] }
const STANDING = `Repo: ${REPO}; run every command from there. sources/ and rules/ are read-only; never commit; never call archive_scene, log_ruling, propose_rule or any MCP tool that writes — this run produces files under book/ only. Read-only WOTR tools are on the command line: ${T} <tool> ... (run it with no arguments to see them; output is UTF-8). Book files live in ${BOOK} (outline.json, bible.md, state.json = {facts:[], hooks:[], summaries:[]}) and this chapter's in ${DIR}.`

// ------------------------------------------------------------------ foundation
phase('Foundation')
if (A.do_foundation) {
  const outline = await agent(`You are the planner for a War of the Realms book written from the table's state, not invented. ${STANDING}
Thread "${A.thread}" (Fronts thread "${A.front_thread}"), culture ${A.culture}, ${A.target_chapters} chapters of ~${A.target_words} words. Isaac's premise, in his words: ${A.premise ? JSON.stringify(A.premise) : '(none given — derive the book from where the table stands)'}.
Read, in this order: ${T} session_start "${A.thread}" standard ${A.culture} (State of Play, Ledger, Fronts, Docket, inventory); ${T} fronts ${A.front_thread}; ${T} due 1 ${A.front_thread}; ${T} list_conflicts; scenes/ARCS.md and the LAST FOUR scenes of the thread's arc in full (the book continues from them); scenes/CAST.md for who appears where; desktop/NATALIE.md for the table's protocol. Then decide the book's spine: each chapter ticks a named Front from the fronts output (its "next tick" is your material), pays what the Ledger says comes due, and carries hooks with plant and pay chapters — "mention is not advancement". Isaac's rule for his player character (Sodoku Moto): the outline's beats state what the PC does and the writer executes exactly that and originates no decision for him beyond it; other creators' characters (Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai) are not POV and decide nothing unless a beat names them.
Write ${BOOK}\\outline.json: {"title","thread","culture","premise","chapters":[{"number","title","beat"(2–4 sentences, concrete, what happens and what changes),"scene_type"(duel|battle|talky|quiet|explicit|working|standard),"pov","cast":[],"place","front_id","plants":[hook ids],"pays":[hook ids],"time_elapsed","target_words"}],"hooks":[{"hook_id","text","keywords":[3–5 words the payoff must contain],"planted_ch","due_ch"}],"voice_note":"150 words on what this book's narration does that the archive does not, with one exemplar paragraph and one anti-exemplar"}. Write ${BOOK}\\bible.md: premise, the cast with one line each (from ${T} fow_line NAME), the voice note, the Fronts and Ledger lines the book will pay. Write ${BOOK}\\state.json as {"facts":[],"hooks":<the hooks with status "planned">,"summaries":[]} unless it exists. Return the outline as a numbered list of chapter titles + one-line beats, and the voice note.`, { phase: 'Foundation', label: 'plan:outline', effort: 'high' })
  log('outline written')
}

// ------------------------------------------------------------------ brief
phase('Brief')
const brief = await agent(`Assemble the brief for chapter ${A.chapter} of the book in ${BOOK}. ${STANDING}
Read ${BOOK}\\outline.json (this chapter's row: beat, scene_type, pov, cast, place, front_id, plants, pays, target_words), ${BOOK}\\bible.md, ${BOOK}\\state.json. Then gather, in this order, and write ONE file ${DIR}\\brief.md with these sections:
1. "## The beat" — the outline row verbatim, plus the hooks it must plant or pay (from state.json / outline hooks, with their keywords) and the Front tick it makes (${T} fronts ${A.front_thread}: that front's want / last / next tick).
2. "## Protocol" — the writer's protocol: desktop/NATALIE.md applies with these chapter adaptations: no turn-taking (Table Rule 1's answer-the-PC half is off; its ending rule stays); the PC does what the beat says and nothing beyond it; length is the target words at the set-piece band; one deliberate lie by an NPC and one misreading by the POV character per chapter, both declared in the notes; the Standing Inventory block from ${T} session_start "${A.thread}" ${'<scene_type>'} ${A.culture} (copy the "# STANDING INVENTORY" section only).
3. "## Rule loadout" — ${T} load_rules <the tags from: ${T} loadout <scene_type>> --brief, whole output.
4. "## Docket" — ${T} check_docket <same tags>; if any pending/proposed rule would change what this chapter must do, say so in one line at the top of the file: "ESCALATE: docket — <why>".
5. "## Scene brief" — ${T} scene_brief "<beat>" --thread "${A.thread}" --type <scene_type> --culture ${A.culture} --cast <cast names>: keep everything from "## Fill before drafting" up to "## Rule loadout" (the blanks and the FOW lines); drop the loadout (already in §3).
6. "## Previous chapter" — for chapter 1: the last 1,500 words of the LAST scene in this thread's arc (scenes/ARCS.md, the arc named for the thread), raw, cut at a paragraph boundary; for later chapters the last 1,500 words of ${BOOK}\\ch${'<previous>'}\\final.md if it exists, else the archived scene named in state.json summaries.
7. "## Cast" — for each cast member: full card (${T} character NAME, capped at 6,000 characters) if state.json has no facts about them yet, else ${T} fow_line NAME. Then ${T} voice_fingerprints for the cast that appear in it.
8. "## Recall" — ${T} scene_recall "<beat keywords>" and ${T} scene_recall "<cast + place>"; ${T} wiki <term> for at most two capitalised terms in the beat that are not cast names.
9. "## Continuity" — state.json facts about the cast or the place (newest first, at most 40, each with its quote), the summaries of all prior chapters, and the hook agenda (planted or advanced hooks due within 3 chapters).
Trim order if the file passes ~40k tokens: wiki snippets, then the second recall, then full cards to FOW lines, then old summaries to one sentence. Never trim the previous chapter tail, the brief blanks, the loadout or the hook agenda. Return: the first line exactly \`scene_type: <type>\`, then the cast, the word count of brief.md, and whether it starts with ESCALATE.`, { phase: 'Brief', label: `brief:ch${CH}` })
if (/starts_with_ESCALATE:\s*yes/i.test(brief || '') || /^ESCALATE:/m.test(brief || '')) return { chapter: A.chapter, stage: 'brief', escalate: brief }
const COMBAT = /scene_type:\s*(duel|battle|working)/i.test(brief || '')

// ------------------------------------------------------------------ draft
phase('Draft')
const writerPrompt = (round, extra) => `You are the writer. ${STANDING}
Read ${DIR}\\brief.md in full — it is the whole brief: the beat, the protocol, the rule loadout, the scene brief's blanks and FOW lines, the previous chapter's tail (match its voice; do not summarise it back), the cast, recall and continuity. ${extra}
Write the chapter as the scene file it will become: an H1 "Chapter ${A.chapter} — <title from the outline>", an italic place/time line, then the prose, ${A.target_words} words ±15%, set-piece band, no author notes inside the prose. Every rule in the loadout binds; the FOW lines are the cast's numbers; the beat is what happens and the PC does what it says and nothing beyond it. Include one deliberate lie by an NPC and one misreading by the POV character. Save the prose as ${DIR}\\draft_r${round}.md and the notes as ${DIR}\\notes_r${round}.md: the scene brief's blanks filled (each with the rule id it serves), the lie and the misreading as the exact sentences from the chapter, a "Summary for continuity" of at most 200 words, and the hooks planted/paid with the sentence that does it. Return the title, the word count, and the two declared sentences.`
let round = 0
await agent(writerPrompt(0, ''), { phase: 'Draft', label: `draft:ch${CH}`, effort: 'high' })

// ------------------------------------------------------------------ check
const critics = [
  { key: 'continuity', prompt: 'CONTINUITY. Compare the draft against the previous chapter tail, the continuity facts and summaries, and the cast cards in the brief. Report every contradiction of a stated fact (place, injury, item, who knows what, who is alive, time elapsed, a number) and every character acting on knowledge they were not shown to have.' },
  { key: 'pov', prompt: 'POV AND KNOWLEDGE. One POV character; the narration knows only what that character perceives or already knows (R5-C1, R6-3, R6-4 in the loadout); no head-hopping; the narration never adjudicates a character morally; free indirect stays inside the POV idiom. Report each breach.' },
  { key: 'rules', prompt: 'RULE COMPLIANCE. Take the rule loadout in the brief rule by rule and report each rule the draft breaks, citing the rule id and quoting the offending span. Do not report rules it keeps. Do not grade prose quality.' },
  { key: 'canon', prompt: `CANON. Every proper noun, number, material, technique, rank and place in the draft is checked against the wiki: ${T} character NAME, ${T} fow_line NAME, ${T} wiki TERM (at most twelve calls). Report each thing the draft states that the wiki contradicts, with the wiki line as evidence; a thing the wiki does not mention is WARN "unattested", not FAIL.` },
  { key: 'beat', prompt: 'BEAT AND HOOKS. Does the chapter deliver the outline beat — every event the beat names happens on the page, the PC does what the beat says and nothing beyond it, the Front is ticked as described? Are the hooks it must plant planted (a reader could notice) and the ones it must pay paid with the keywords present? Mention is not advancement. Report each miss.' },
]
const check = async (r, which) => {
  const det = await agent(`Deterministic checks on ${DIR}\\draft_r${r}.md. ${STANDING}
Run: ${T} verify ${DIR}\\draft_r${r}.md --band set-piece --culture ${A.culture}${COMBAT ? ' --combat' : ''}; ${COMBAT ? `${T} gap_fill ${DIR}\\draft_r${r}.md (WARN only — its regexes count ordinary words); ` : ''}for up to eight attributed dialogue lines per cast member, ${T} voice_check NAME "LINE"; word count against the target ${A.target_words} (FAIL under 80% or over 150%); the two declared sentences in notes_r${r}.md must exist verbatim in the draft (FAIL if not); each hook the beat must pay must contain its keywords (FAIL if not). Write the findings as JSON to ${DIR}\\det_r${r}.json in the schema {findings:[{severity,pass,quote,problem,evidence,fix}]} where quote is a verbatim substring of the draft (for a count-based finding quote the first line of the draft) and pass is tell_scan | shape | combat_floor | voice | hooks. Return the counts and the FAILs.`, { phase: 'Check', label: `det:ch${CH}:r${r}`, effort: 'low' })
  const model = await parallel(critics.filter(c => which.includes(c.key)).map(c => () => agent(`Critic, one job, edit nothing. ${STANDING}
Read ${DIR}\\brief.md and ${DIR}\\draft_r${r}.md and ${DIR}\\notes_r${r}.md. ${c.prompt}
Rules of evidence: every finding quotes the draft verbatim (a substring, 5–40 words) and, where a source exists, quotes the source; a finding you cannot quote is not a finding. FAIL = a contradiction, a broken rule, a missing beat event, a knowledge leak; WARN = a doubt, an unattested thing, a weakness. The notes declare one lie and one misreading — those two sentences are intentional: do not report them. Report nothing about prose quality unless the pass is rules. Return {findings:[]} — empty is a valid answer.`, { phase: 'Check', label: `critic:${c.key}:r${r}`, model: 'sonnet', schema: FINDINGS })))
  const merged = await agent(`Merge the findings for round ${r}. ${STANDING}
Inputs: ${DIR}\\det_r${r}.json and these critic results: ${JSON.stringify(model.filter(Boolean)).slice(0, 60000)}. Read ${DIR}\\draft_r${r}.md and ${DIR}\\notes_r${r}.md. Drop any finding whose quote is not a substring of the draft (whitespace-normalised) — count them as dropped; drop findings that fall in the same paragraph as a declared lie or misreading sentence; dedupe on quote. Write ${DIR}\\findings_r${r}.json {fail, warn, dropped, findings:[...]} and ${DIR}\\digest_r${r}.md (verdict line, then every FAIL and WARN with its quote, pass and fix). Verdict: pass if fail = 0; else revise if ${r} < ${A.max_rounds}; else escalate. Return {fail, warn, dropped, verdict, top} where top lists up to 8 one-line FAIL summaries.`, { phase: 'Check', label: `merge:ch${CH}:r${r}`, schema: MERGE, effort: 'low' })
  // the verdict is arithmetic, not the merge agent's judgment: FAILs remaining + rounds left
  if (merged) merged.verdict = merged.fail === 0 ? 'pass' : (r < A.max_rounds ? 'revise' : 'escalate')
  return merged
}
phase('Check')
let result = await check(0, critics.map(c => c.key))
log(`round 0: ${result.fail} FAIL / ${result.warn} WARN (${result.dropped} unquoted dropped) → ${result.verdict}`)

// ------------------------------------------------------------------ revise loop
phase('Revise')
let failedKeys = critics.map(c => c.key)
while (result.verdict === 'revise' && round < A.max_rounds) {
  const prev = round
  round += 1
  const rev = await agent(`You are the reviser. ${STANDING}
Read ${DIR}\\brief.md, ${DIR}\\draft_r${prev}.md, ${DIR}\\notes_r${prev}.md and ${DIR}\\findings_r${prev}.json. Fix every FAIL and the WARNs you can without harm; a WARN that needs Isaac's ruling (a canon fact the wiki does not settle) is left alone and named in your report. The H1 is the chapter's title alone, "# <title>", with no "Chapter N —" prefix (the number lives in the outline). Change nothing else — structure is frozen: same POV, same events in the same order, the same ending unless a finding names it, no new characters, no new lie or misreading. Keep 85–115% of the word count, at least 70% of the dialogue lines and paragraphs. Save ${DIR}\\draft_r${round}.md and ${DIR}\\notes_r${round}.md (notes updated only where a fix changed a declared sentence or a hook line). Then run the diff guard yourself — word count 85–115%, ≥70% of quoted lines and of paragraphs kept, first sentence's POV name unchanged, last paragraph unchanged unless named — and if the guard fails, restore the previous draft as draft_r${round}.md and say so. Return: what you changed per finding, the word counts before and after, and whether the guard passed.`, { phase: 'Revise', label: `revise:ch${CH}:r${round}`, effort: 'high' })
  const again = await check(round, ['continuity', ...failedKeys.filter(k => k !== 'continuity')])
  // monotone acceptance: keep the revision only if FAILs did not rise and WARNs rose by at most 2
  if (again.fail > result.fail || again.warn > result.warn + 2) {
    log(`round ${round} regressed (${again.fail}/${again.warn} vs ${result.fail}/${result.warn}); keeping round ${prev}`)
    round = prev
    break
  }
  result = again
  failedKeys = critics.map(c => c.key)   // conservative: the next round re-runs all critics
  log(`round ${round}: ${result.fail} FAIL / ${result.warn} WARN → ${result.verdict}`)
}

// ------------------------------------------------------------------ digest
phase('Digest')
const digest = await agent(`Write the gate digest for Isaac. ${STANDING}
The accepted draft is ${DIR}\\draft_r${round}.md (notes ${DIR}\\notes_r${round}.md, findings ${DIR}\\findings_r${round}.json, digest ${DIR}\\digest_r${round}.md). Copy the accepted draft to ${DIR}\\final.md and its notes to ${DIR}\\final_notes.md. Write ${DIR}\\GATE.md: title and word count; verdict (${result.verdict}) with FAIL/WARN counts per round; every remaining FAIL and WARN with its quote; the declared lie and misreading; the beat and whether the critics found it delivered; the hooks planted/paid; the Front ticked; and, in one short paragraph, what Isaac is deciding (approve → archive_scene under the chapter's title; instruct → one more revise round with his note; drop). Return the GATE.md text.`, { phase: 'Digest', label: `gate:ch${CH}`, effort: 'low' })
return { chapter: A.chapter, rounds: round, fail: result.fail, warn: result.warn, verdict: result.verdict, final: `${DIR}\\final.md`, gate: digest }