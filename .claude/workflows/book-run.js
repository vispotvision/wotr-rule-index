export const meta = {
  name: 'book-run',
  description: "Write a War of the Realms book straight through: each chapter through book-chapter, then into the book's memory (state.json, the cast register, ISSUES.md), with an audit at every fifth chapter, each part's end and the last",
  whenToUse: 'Isaac asked for several chapters or a whole book in one go (outline gate_mode "review"); args {slug, thread, culture, front_thread?, from, to, total, part_ends?, words?:{chapter: estimate}, target_words?}',
  phases: [{ title: 'Chapter' }, { title: 'Memory' }, { title: 'Audit' }],
}
// the script cannot read files: the bounds and the per-chapter estimates come in args, from book-next --json and outline.json
const A = Object.assign({ repo: '/home/oridon/wotr-rule-index', front_thread: '', from: 1, to: 0, total: 0, part_ends: [], words: {}, target_words: 3500 }, args || {})
const MISSING = ['slug', 'thread', 'culture', 'to', 'total'].filter(k => !A[k])
if (MISSING.length) return { error: `book-run needs ${MISSING.join(', ')}` }
const REPO = A.repo
const BOOK = `${REPO}/book/${A.slug}`
const M = `rust/target/release/wotr-mcp book-memory --slug ${A.slug}`
const STANDING = `Repo: ${REPO}; run every command from there. sources/, rules/, wiki/, scenes/ and table/ are read-only for this run; never commit; never call archive_scene or any MCP tool that writes. Edit JSON with jq (/usr/bin/jq) or a load-and-dump, never by hand-splicing, and keep it valid.`
const KINDS = 'fact, time, location, object, money, debt, promise, name, look, gear, wound, healed, death, returned, move, skill, level, stage, grade, class, title, vow, bond, knows, reader_knows, lie, renown, profession'
const auditAt = new Set([...A.part_ends, A.total, ...Array.from({ length: Math.floor(A.total / 5) }, (_, i) => (i + 1) * 5)])
const STALE = { type: 'object', properties: { chapters: { type: 'array', items: { type: 'integer' } } }, required: ['chapters'] }
const out = []

const audit = async (ch, last) => {
  const CH = String(ch).padStart(2, '0')
  // one careful reading per chapter whose digest is missing or older than its final.md (a rewrite, an instructed round,
  // a chapter written outside this run), each to its own file, so no single context holds the book
  const stale = await agent(`List the chapters 1 to ${ch} of ${BOOK} that have a chNN/final.md and whose ${BOOK}/digest/chNN.md is missing or older than that final.md (compare modification times with stat or ls -l --time-style=+%s). ${STANDING} Return {chapters:[numbers]}.`, { phase: 'Audit', label: `digest-list:ch${CH}`, schema: STALE, effort: 'low' })
  const fresh = (stale && stale.chapters) || []
  await parallel(fresh.map(n => () => agent(`Read ${BOOK}/ch${String(n).padStart(2, '0')}/final.md alone, once, and write ${BOOK}/digest/ch${String(n).padStart(2, '0')}.md: "## ch ${n} <title>", then the beats (3-6), time and date markers, who appears and what each does and wants, places, relationships that shifted, setups planted and payoffs paid, and two or three quotes that show the prose at its best and worst. ${STANDING}`, { phase: 'Audit', label: `digest:ch${String(n).padStart(2, '0')}`, effort: 'low' })))
  return agent(`Audit the book after chapter ${ch}. ${STANDING}
Assemble ${BOOK}/DIGEST.md from ${BOOK}/digest/ch*.md in chapter order. Then follow .claude/skills/wotr-book/SKILL.md §5 exactly, reading DIGEST.md, state.json, CAST.md, outline.json and bible.md (open a chapter only to check a quote), and write ${BOOK}/AUDIT_ch${CH}.md: hooks (overdue, dormant, too many open), cast (a register person silent too long, a death followed by acting, an entry that drifted from the pages, a person who has earned promotion and not got it), sag, continuity (cross-chapter contradictions with both quotes; read the 35-65% band closest), and voice (rewrite ${BOOK}/STYLE.md from the chapters; tics go to ISSUES.md). Run ${M} and list what it prints. Carry-forward: for each unwritten chapter whose outline row now contradicts the pages (a fact, a count, a place, who knows what), edit that row in outline.json so it fits the pages, changing nothing else in the beat, and record each edit (chapter, before, after, the quote that forced it) under "## Outline changes" in ${BOOK}/CARRY.md for Isaac's review; everything else the later chapters must carry goes under "## Carry" in CARRY.md, one line each with the chapter it binds. ${last ? `This is the end of the book: also review the whole book once as a critic and once as a teacher of fiction, with specific notes by chapter; read it through the lenses §5 names; and read it once as the first-time reader of book-chapter.js over the whole book (where it held and where it sagged, the middle closest). ` : ''}Return the audit's critical and warn counts, the outline rows changed, and the carry lines added.`, { phase: 'Audit', label: `audit:ch${CH}`, effort: 'high' })
}

for (let ch = A.from; ch <= A.to; ch++) {
  const CH = String(ch).padStart(2, '0')
  phase('Chapter')
  let r
  try {
    r = await workflow('book-chapter', { repo: REPO, slug: A.slug, thread: A.thread, culture: A.culture, front_thread: A.front_thread, chapter: ch, target_words: A.words[ch] || A.target_words, do_foundation: false })
  } catch (e) {
    r = { error: `book-chapter threw: ${String(e).slice(0, 300)}` }
  }
  // stop at a chapter that did not pass: an escalation at the brief, a crash, or FAILs left after the revise rounds;
  // the next chapter would be briefed on it, so it is fixed (and re-run from here) before the run goes on
  if (!r || r.error || r.escalate || r.verdict !== 'pass') {
    out.push({ chapter: ch, stopped: r })
    log(`ch ${ch} stopped: ${JSON.stringify(r).slice(0, 300)}`)
    break
  }
  log(`ch ${ch}: ${r.verdict}, ${r.fail} FAIL / ${r.warn} WARN after ${r.rounds} revise round(s)`)
  phase('Memory')
  const mem = await agent(`You are the book's memory keeper for chapter ${ch}. ${STANDING}
If state.json already holds a summary for chapter ${ch} (this chapter is a rewrite), first run ${M} --purge ${ch} so its old facts, summary, hook events and arc lines leave the memory. Read ${BOOK}/ch${CH}/final.md and final_notes.md, ${BOOK}/state.json, ${BOOK}/outline.json and .claude/skills/wotr-book/SKILL.md §4, then update state.json:
- summaries: {ch, title, summary}, the notes' "Summary for continuity" as written (at most 200 words).
- facts: each durable fact the chapter establishes, as {ch, subject, kind, fact, quote}. subject is the person's register name (state.json cast) or the place's or object's name; kind is one of: ${KINDS}; quote is one sentence copied exactly from final.md (no quote, no fact). A lie a character tells is kind lie; what a character now knows is knows; what the reader saw and the character did not is reader_knows; money and debts are money and debt; a guild token is title; a window that moved a Grade, Level, skill or Stage is grade, level, skill or stage, with the window line as the quote; a wound is wound, and a healed fact names the wound it closes in a "heals" field (the wound fact's own words); a death that does not hold is followed by a returned fact. A new fact that contradicts an older one does not replace it: add it.
- cast: from the notes' "Cast register", add each new person {name, aliases, tier, profession, age, role, culture, first_ch: ${ch}} and, at lead or major, the full entry (look and gear, voice, want, refusal, lie, kit, sheet, bonds, each one string) from the pages, inventing nothing they do not show; for returning people change the fields the chapter changed and append {ch: ${ch}, line} to their arc, one line of what this chapter did to them. Promote when it is earned: a walk-on who returns becomes recurring; a recurring person who gets a want on the page, a fight, a stretch of their own or a turn of the plot becomes major, with the full entry filled. Every person has a profession and an age.
- hooks: planted, advanced or paid as the notes' Hooks lines show and as the text shows (look for each open hook's keywords in final.md); each as an event {ch, kind, quote}; status, and paid_ch when paid.
Then ${BOOK}/ISSUES.md: this chapter's accepted-round findings (${BOOK}/ch${CH}/findings_r${r.rounds}.json) and GATE.md against the earlier chapters'; a fault seen in a second chapter is an issue, in the §4 format; new evidence goes onto the existing entry; an issue a later chapter no longer shows is resolved and kept.
Then run ${M} --render and ${M}. Fix every FAIL it prints in state.json (a quote not found: copy the sentence exactly; a subject not in the register: add the person or use their register name; a kind off the list: the right kind) and run ${M} again until it prints no FAIL. Write your report to ${BOOK}/ch${CH}/memory.md: rows added per kind, new people and promotions, hooks moved, new or resolved issues, every new fact that contradicts an older one with both quotes (for Isaac), and the last line ${M} printed. Return the same report.`, { phase: 'Memory', label: `memory:ch${CH}` })
  out.push({ chapter: ch, verdict: r.verdict, fail: r.fail, warn: r.warn, rounds: r.rounds, final: r.final, memory: `${BOOK}/ch${CH}/memory.md`, memory_tail: String(mem || '').slice(-600) })
  if (auditAt.has(ch)) {
    phase('Audit')
    const a = await audit(ch, ch === A.total)
    log(`audit after ch ${ch}: ${String(a || '').slice(0, 200)}`)
    out[out.length - 1].audit = String(a || '').slice(0, 1500)
  }
}
return out
