export const meta = {
  name: 'character-lore',
  description: 'The character manager: map how every card connects, write each character a Lore section (origin, the making, the cost, where they stand, ties) that agrees with the card, the archive and every other character, check it twice, and build The Web of Lives hub. Writes imports/lore/ only; publishing to Notion is build/lore_publish.py.',
  whenToUse: 'When cards lack a Lore section, after new cards land, or to rewrite lore; args {date: "YYYY-MM-DD", cards?: [slugs], rewrite?: false, repo?}',
  phases: [
    { title: 'Roster' }, { title: 'Frame' }, { title: 'Bibles' }, { title: 'Weave' },
    { title: 'Write' }, { title: 'Check' }, { title: 'Revise' }, { title: 'Reconcile' }, { title: 'Web' }, { title: 'Audit' },
  ],
}
// ------------------------------------------------------------------ setup
const A = Object.assign({ repo: '/home/oridon/wotr-rule-index', date: '', cards: null, rewrite: false }, args || {})
const REPO = A.repo
const L = 'imports/lore'
const PY = 'bash build/py.sh'
const HEAD = 'Lore · The Life Behind the Card'
const STANDING = `Repo: ${REPO}; run every command from there. Python tools run as \`${PY} build/<tool>.py ...\` (the read-only command line is \`${PY} build/book_tools.py <tool> ...\`; bare lists the tools). This run writes files under ${L}/ ONLY. wiki/, scenes/, sources/, rules/, table/ are read-only. Never git add/commit/pull/push. Never call a writing MCP tool (update_character, create_character, archive_scene, npc_set, ledger_add, advance_front, log_ruling, propose_rule, sync_now) and never write to Notion by any route. Reading MCP tools (character, wiki, scene_recall, load_rules, check_docket, stale_names, fow_line) are fine; for the archive prefer grep and Read over scene_recall.
The roster is ${L}/_roster.json (one row per card: slug, name, title, file, era, affiliation, relationships, mentions, same_surname, scenes, mode). Canon order: Isaac's direction, then the card's own text, then the archived scenes (scenes/*.md), then wiki pages, then this pass's own records. New lore fills silence; it never contradicts a card or a scene. An "Open Rulings" item on a card, or anything on the docket, stays open: prose does not settle it.
mode "record" = Sodoku Moto, Isaac's player character: nothing invented, no thoughts or choices put in his head; every sentence traces to his card or a scene. mode "pov" = a point-of-view character with a heavy archive: read the archive first; invent only where it is silent. Characters of other creators (Haruki, Dova'Kan, Gorgi, Ma'Kovu, Fushigi, Xhem, Sonzai also rendered Chuluun) get no invented line, thought, act or history.
Never invent a number: no Level, Stage, stat, Grade, EU, eta or tier the card does not state (the card carries them; the lore needs none). No "pending" markers anywhere: what cannot be established is left out. This is War of the Realms prose: the register rules in ${L}/LAW.md bind it; no compressed or telegraphic style.`

const FORMAT = `The file holds exactly this shape and nothing else (no frontmatter, no title line above it):

## ${HEAD}

*<provenance line>*

### Origin
<prose: where and to whom they were born or made, the world that shaped them>

### The Making
<prose: the road to what the card records; it arrives at the card's Catalyst Event (or its equivalent) exactly as the card tells it>

### The Cost
<prose: what it took, what they refuse, what they believe that costs them>

### Where They Stand
<prose: the present as the card and the archive leave them; open threads stay open>

### Ties
- **<Name as their card title gives it (an em dash in a title is written " · "; verify.py FAILs any em or en dash, headings and bullets included), or an archive name>** · <kind of tie>. <one sentence, from this character's side>.

Provenance line: mode full or pov: "Written ${A.date} by the character-lore pass from this card<, the N archived scenes it appears in,> and the record of <cluster name>. What those sources do not state is new here." Mode record: "Compiled ${A.date} from this card and the archived scenes. Nothing here is new."
Length of the four prose sections together: 350-550 words for a card under 3,500 bytes that appears in no scene; 800-1,200 for a card that appears in 5+ scenes or runs over 12,000 bytes; 550-850 otherwise. Ties: every tie your cluster record and WEAVE.md give this character, and any the card or archive already has.`

const WRITTEN = { type: 'object', properties: {
  slug: { type: 'string' }, words: { type: 'number' },
  verify: { type: 'string', description: 'PASS, or FAIL and the remaining fails' },
  ties: { type: 'array', items: { type: 'object', properties: {
    other: { type: 'string', description: 'the other character\'s roster slug, or "archive:<Name>" for an uncarded archive character' },
    kind: { type: 'string' }, line: { type: 'string' } }, required: ['other', 'kind', 'line'] } },
  new_names: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, what: { type: 'string' } }, required: ['name', 'what'] } },
  sources: { type: 'array', items: { type: 'string' }, description: 'files read: the card, scenes, wiki pages' },
}, required: ['slug', 'words', 'verify', 'ties', 'new_names', 'sources'] }

const FINDINGS = { type: 'object', properties: {
  findings: { type: 'array', items: { type: 'object', properties: {
    slug: { type: 'string' }, severity: { type: 'string', enum: ['must-fix', 'should-fix'] },
    issue: { type: 'string' }, evidence: { type: 'string', description: 'quotes from both sides' }, fix: { type: 'string', description: 'the exact change' } },
    required: ['slug', 'severity', 'issue', 'evidence', 'fix'] } },
  clean: { type: 'array', items: { type: 'string' } },
}, required: ['findings', 'clean'] }

const CLUSTERS = { type: 'object', properties: {
  clusters: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, name: { type: 'string' }, theme: { type: 'string' }, era: { type: 'string' },
    hinge: { type: 'string', description: 'what holds these people together, in one sentence' },
    members: { type: 'array', items: { type: 'string' } } }, required: ['id', 'name', 'theme', 'era', 'hinge', 'members'] } },
  notes: { type: 'array', items: { type: 'string' } },
}, required: ['clusters', 'notes'] }

const BIBLE = { type: 'object', properties: {
  id: { type: 'string' }, name: { type: 'string' }, era_span: { type: 'string' },
  members: { type: 'array', items: { type: 'object', properties: { slug: { type: 'string' }, line: { type: 'string' } }, required: ['slug', 'line'] } },
  events: { type: 'array', items: { type: 'object', properties: {
    name: { type: 'string' }, when: { type: 'string' }, where: { type: 'string' }, who: { type: 'array', items: { type: 'string' } }, what: { type: 'string' } },
    required: ['name', 'when', 'where', 'who', 'what'] } },
  ties: { type: 'array', items: { type: 'object', properties: {
    a: { type: 'string' }, b: { type: 'string' }, kind: { type: 'string' }, summary: { type: 'string' }, basis: { type: 'string', enum: ['card', 'scene', 'new'] } },
    required: ['a', 'b', 'kind', 'summary', 'basis'] } },
  outward: { type: 'array', items: { type: 'object', properties: { slug: { type: 'string' }, wants: { type: 'string' } }, required: ['slug', 'wants'] } },
  same_person: { type: 'array', items: { type: 'array', items: { type: 'string' } } },
  card_contradictions: { type: 'array', items: { type: 'string' } },
}, required: ['id', 'name', 'era_span', 'members', 'events', 'ties', 'outward', 'same_person', 'card_contradictions'] }

const WEAVE = { type: 'object', properties: {
  cross_ties: { type: 'array', items: { type: 'object', properties: {
    a: { type: 'string' }, b: { type: 'string' }, kind: { type: 'string' }, summary: { type: 'string' } }, required: ['a', 'b', 'kind', 'summary'] } },
  rulings: { type: 'array', items: { type: 'object', properties: { ids: { type: 'array', items: { type: 'string' } }, issue: { type: 'string' }, ruling: { type: 'string' } }, required: ['ids', 'issue', 'ruling'] } },
}, required: ['cross_ties', 'rulings'] }

const GAPS = { type: 'object', properties: {
  gaps: { type: 'array', items: { type: 'object', properties: { slug: { type: 'string' }, issue: { type: 'string' } }, required: ['slug', 'issue'] } },
  summary: { type: 'string' },
}, required: ['gaps', 'summary'] }

// ------------------------------------------------------------------ roster
phase('Roster')
const R = await agent(`${STANDING}
Run \`${PY} build/lore_roster.py\` (it rebuilds ${L}/_roster.json and ${L}/_graph.json from the wiki mirror). Then read ${L}/_roster.json and return every row's slug with its has_lore flag, in file order, and the tool's printed summary line.`,
  { label: 'roster', phase: 'Roster', effort: 'low', schema: { type: 'object', properties: {
    rows: { type: 'array', items: { type: 'object', properties: { slug: { type: 'string' }, has_lore: { type: 'boolean' } }, required: ['slug', 'has_lore'] } },
    summary: { type: 'string' } }, required: ['rows', 'summary'] } })
if (!R || !R.rows.length) throw new Error('roster came back empty')
const ALL = R.rows.map(r => r.slug)
const ALLSET = new Set(ALL)
const TARGETS = new Set(Array.isArray(A.cards) && A.cards.length ? A.cards.filter(s => ALLSET.has(s))
  : R.rows.filter(r => A.rewrite || !r.has_lore).map(r => r.slug))
log(`${R.summary} | writing ${TARGETS.size} of ${ALL.length}`)
if (Array.isArray(A.cards)) { const bad = A.cards.filter(s => !ALLSET.has(s)); if (bad.length) log(`not in the roster, skipped: ${bad.join(', ')}`) }
if (!TARGETS.size) return { written: 0, note: 'every card already carries the Lore section; pass rewrite: true or cards: [...]' }

// ------------------------------------------------------------------ frame
phase('Frame')
const [law, world, register, carto] = await parallel([
  () => agent(`${STANDING}
You are writing the LAW for a pass that gives every War of the Realms character card a Lore section (a backstory: origin, the making, the cost, where they stand, ties). Every writer reads your file before writing, so it must be complete and short.
Load: \`${PY} build/book_tools.py load_rules prose-law character-sheet worldbuilding naming codex documents register\` (full text; it is long, read all of it) and \`${PY} build/book_tools.py check_docket prose-law character-sheet worldbuilding naming codex documents register\`. Read desktop/NATALIE.md (the canon hierarchy, the naming canon, "Character first", the magic frame), the wiki page "wiki/Information not on WIKI/Characters.md" (how a life is recorded), the head of build/verify.py (what it FAILs), and desktop/WOTR_Manual_Verification_Guide*.md if present.
Write ${L}/LAW.md, at most 2,200 words, in these sections: 1 The register (what a card's Lore section reads like: person, tense, distance, the document register the rules set for a record of a life, with rule ids). 2 Banned constructions and AI tells, each with its rule id (the verify.py FAILs first). 3 Names: the five naming strata and when each applies, where the ratified banks live (page paths), what is stale (the Büri register, struck terms), how a new minor name is chosen, and the rule that naming register is not ethnicity. 4 Numbers and mechanism: what may and may not be stated. 5 Character first: the three questions every life must answer. 6 Open on the docket: anything unratified a backstory must not settle, one line each with its id. 7 A short worked example: one paragraph that obeys all of it (about no real card). Quote rule ids exactly; do not paraphrase a rule into something it does not say. Return the first line of each section.`, { label: 'law', phase: 'Frame' }),

  () => agent(`${STANDING}
You are writing the WORLD frame for a pass that gives every character card a backstory. Writers place lives in it, so it must be right, dense and cited.
Read: wiki/Lore & History/ (all), wiki/Geography & the Four Quarters/ and wiki/Geography/, wiki/Factions, Bloodlines & Institutions/ and wiki/Factions/ (the Guild Accord and its Divisions, the Holy Sea of Alabaster, Sanctum Lux, the Curia, the bloodlines), wiki/The Guild Accord/, wiki/Cosmology & Metaphysics/ (headings and the eras only), wiki/The Moto Bloodline/, wiki/The War Cycle/ (skim), scenes/TIMELINE.md and scenes/ARCS.md, the four "State of Play" pages in wiki/The Table — Running Pieces/, and grep the cards (wiki/Volume I — Character Cards/) for every "... Era" and "... Age" they use.
Write ${L}/WORLD.md, at most 3,000 words: 1 The eras in order, what defines each, and which card eras map to which (flag any card era that fits none). 2 The present: where the table stands now (the year after the ninth hour at Kharven-Seat; the New World war) and what a "where they stand" section may assume. 3 Polities, one line each with the page it comes from; struck or retired polities and terms that must never appear. 4 Institutions and orders (the Accord's Divisions and ranks, the churches, the courts, the guilds), one line each. 5 Places a life can come from, grouped by quarter. 6 Peoples and lifespans (who can live across eras and who cannot). 7 Bloodlines and houses already in canon. Cite the wiki file for every line. Return the section titles and the count of eras.`, { label: 'world', phase: 'Frame' }),

  () => agent(`${STANDING}
You keep the register of archive characters with no card. Read ${L}/_graph.json "uncarded_in_scenes". Skip "Darius" (his card is "Ignatius Sanctus Sanctorum Arsenal · The Archpaladin", see build/aliases.yaml), "The Arctic Lion" and "Tōga (冬牙)" (pages of Sodoku Moto's own section). If a name is an alias of a card (e.g. a surname that is a card's), note it and skip. For Sonzai Moto and Haruki Yuno (and any other creator's character): one line, "belongs to another creator; nothing is written here." For each of the rest: grep scenes/ for the name, read the passages, and compile what the archive establishes: who they are, where they are seen, what they did, who among the carded characters they are bound to, what is left open. 4 to 10 lines each, every claim followed by the scene file in brackets. Nothing invented, no numbers the scenes do not state. Write ${L}/UNCARDED.md with a one-paragraph opening saying these people have no card yet and a card would come through convert_character on Isaac's word. Return one line per name: name, scenes read, carded ties.`, { label: 'register', phase: 'Frame' }),

  () => agent(`${STANDING}
You are the Cartographer. Group all ${ALL.length} cards into clusters of 4 to 9 people who share a life: kin, an order or Division, a campaign, a place, a master and students, rivals, a shared archive thread. The clusters decide who is written in whose company, so coherent beats tidy.
If ${L}/_clusters.json exists and contains every roster slug, return it unchanged. If it exists but some slugs are missing, add each missing slug to the best-fitting cluster (or a new one) and keep the rest as they are. Otherwise build from scratch: start from ${L}/_graph.json "groups" (a first cut from shared surnames, cards naming each other, and shared scenes; its edges are the evidence), split any group that is really two, and place every group of one or two by reading its card (identity, affiliation, era, race, place). Put both cards of a possible same person together (ziyu-pip-inari and ziyu-pip-inari-the-two-tailed-cipher; xanelor-rafiminar and xanelor-rafminar-the-wandering-fang). Keep eras coherent within a cluster where the cards allow; a cross-era cluster needs a hinge that crosses eras (a bloodline, an order, a relic, a record).
Ids c01, c02, ... in order of size. Every roster slug in exactly one cluster; use the slugs exactly as the roster spells them. Write the result to ${L}/_clusters.json (the same JSON you return) and return it.`, { label: 'cartographer', phase: 'Frame', schema: CLUSTERS }),
])
if (!carto) throw new Error('the Cartographer failed')
log(`law: ${law ? 'written' : 'FAILED'}; world: ${world ? 'written' : 'FAILED'}; register: ${register ? 'written' : 'FAILED'}; ${carto.clusters.length} clusters`)

// every slug exactly once
const seen = new Set()
const clusters = carto.clusters.map(c => ({ ...c, members: c.members.filter(s => ALLSET.has(s) && !seen.has(s) && seen.add(s)) }))
const loose = ALL.filter(s => !seen.has(s))
if (loose.length) { clusters.push({ id: `c${String(clusters.length + 1).padStart(2, '0')}`, name: 'The Unplaced', theme: 'cards the Cartographer did not place', era: 'mixed', hinge: 'none yet; the Weaver ties each outward', members: loose }); log(`unplaced by the Cartographer, gathered in one cluster: ${loose.join(', ')}`) }
const work = clusters.filter(c => c.members.some(s => TARGETS.has(s)))
const memberList = c => c.members.map(s => `${s}${TARGETS.has(s) ? '' : ' (already written; read its lore file, do not change it)'}`).join(', ')

// ------------------------------------------------------------------ bibles
const bibles = (await pipeline(work, c => agent(`${STANDING}
You are the Loremaster for cluster ${c.id}, "${c.name}" (${c.theme}; era: ${c.era}; hinge: ${c.hinge}). Members: ${memberList(c)}.
Read ${L}/LAW.md and ${L}/WORLD.md. Read every member's card in full (the roster's "file"). For every member with scenes, grep the listed scenes for the name and read the passages; read in full the two scenes where they appear most. Read the wiki pages for the orders, places and houses they name. If ${L}/clusters/${c.id}.md already exists, build on it and change it only for new members.
Your job is the connections. Work out what binds these people, then write their shared record to ${L}/clusters/${c.id}.md:
1 "Who is here": one paragraph per member, who they are per the card.
2 "What already binds them": every link the cards and scenes already make, each with its quote and file.
3 "The shared history": 2 to 5 events that bind members together, each with when (era, or relative to a canon event), where (a place from WORLD.md), who, what happened, and what each member took from it. Where the sources are silent the events are new, and they must fit every card involved: era, lifespan of the people, affiliation, the Catalyst Event, anything on the card's Psychology or Hooks. People from different eras connect through blood, an order, a relic, a record or a legend, never by meeting.
4 "Ties": every pair that has one: kind (kin, teacher and student, rival, debt, oath, lovers, enemy, comrades, witness, successor ...), one line, basis card/scene/new. Ties are earned by a shared place, order, debt or event; not everyone is tied to everyone, but nobody is left with none.
5 "Outward": for each member, one tie they need beyond this cluster (the kind of person or office), for the Weaver.
6 "Same person?": if two cards here are one person, say so and why; they then share one life.
7 "Where the cards disagree": contradictions between existing cards, quoted, not resolved.
Also write ${L}/clusters/${c.id}.json holding exactly what you return.`, { label: `bible:${c.id}`, phase: 'Bibles', schema: BIBLE }))).filter(Boolean)
log(`${bibles.length}/${work.length} cluster records written`)

// ------------------------------------------------------------------ weave (needs every record at once)
phase('Weave')
const weave = await agent(`${STANDING}
You are the Weaver. Read ${L}/WORLD.md, ${L}/_clusters.json and every ${L}/clusters/*.json (open the matching .md where you need the detail). Clusters were written apart; you make them one world.
1 Cross ties: for each member's "outward" want, find a member of another cluster who fits (same order, same place, same era or an inheritance across eras) and write one tie both ends will agree on. Every cluster gets at least two cross ties; every character ends with at least one tie in total.
2 Contradictions between records: the same event, place or order told two ways; a person in two places at once; an era clash; a house or office described differently. Rule each one (you make the call; a card's text beats any record; the older, better-attested record beats the newer invention).
Write ${L}/WEAVE.md: a section "## <id> · <name>" per cluster listing the cross ties of its members (both slugs, kind, one line) and any ruling that changes that cluster's record; then "## Rulings". Return the cross ties and rulings.`, { label: 'weave', phase: 'Weave', schema: WEAVE })
log(`weave: ${weave ? `${weave.cross_ties.length} cross ties, ${weave.rulings.length} rulings` : 'FAILED; writers work from the cluster records alone'}`)

// ------------------------------------------------------------------ write, check, revise (per cluster, no barrier between clusters)
const writePrompt = (s, c) => `${STANDING}
Write the Lore section for card "${s}" (cluster ${c.id}, "${c.name}"). Read, in this order: ${L}/LAW.md; the card in full (roster "file"); if the roster lists scenes for it, grep them for the name and read the passages (read the three with the most mentions in full); ${L}/WORLD.md; the cluster record ${L}/clusters/${c.id}.md; ${L}/WEAVE.md (the ${c.id} section and every line naming ${s}); the cards of everyone you are tied to (the identity sections at least); and any existing lore file of a tied character in ${L}/cards/ (agree with it).
Character first: what this person refuses, what they survived, what they believe that costs them. Make it specific to this card: a sentence that could sit in another character's lore is a sentence to cut. The shared events are told as the record tells them, from this character's side.
${FORMAT}
Write it to ${L}/cards/${s}.md. Run \`${PY} build/verify.py ${L}/cards/${s}.md --band standard\` and fix every FAIL (a FAIL that only makes sense for a scene, such as a dialogue count, you may leave; say which). Return the result.`

const perCluster = await pipeline(work,
  (c) => parallel(c.members.filter(s => TARGETS.has(s)).map(s => () =>
    agent(writePrompt(s, c), { label: `write:${s}`, phase: 'Write', schema: WRITTEN }))).then(ws => ({ c, ws: ws.filter(Boolean) })),

  (x) => {
    const files = x.ws.map(w => `${L}/cards/${w.slug}.md`).join(', ')
    if (!x.ws.length) return { ...x, findings: [] }
    return parallel([
      () => agent(`${STANDING}
Adversarial canon check, cluster ${x.c.id} "${x.c.name}". Files: ${files}. For each file compare every claim with: the card (identity, race, era, affiliation, the Catalyst Event, relationships, anything under Psychology, Hooks or Open Rulings); the archive for anyone the roster lists in scenes (grep and read the passages); ${L}/clusters/${x.c.id}.md and ${L}/WEAVE.md; and the other files in this cluster (a shared event told two ways, a tie one side forgets or tells differently). Flag: any contradiction; any number the card does not state; a settled open ruling; a tie to a slug not in the roster; anything invented for Sodoku Moto (mode record) or for another creator's character; an era or lifespan broken; a place, order or house that is not in WORLD.md or the wiki. When unsure, flag. Each finding: slug, severity (must-fix for a contradiction or a rule broken), the issue, evidence quoting both sides, the exact fix.`, { label: `canon:${x.c.id}`, phase: 'Check', schema: FINDINGS, effort: 'high' }),
      () => agent(`${STANDING}
Craft check, cluster ${x.c.id} "${x.c.name}". Files: ${files}. Read ${L}/LAW.md. For each file: run \`${PY} build/verify.py <file> --band standard\` (every FAIL is must-fix unless it only makes sense for a scene); check the register LAW.md sets; banned constructions and AI tells; names (a new name outside its stratum, anything in the Büri or Mongolian register, any struck term: must-fix; the stale_names tool helps); the exact format (the heading "## ${HEAD}", the provenance line, the five subsections in order, the Ties bullets); the length band; the character-first test (refusal, survival, costly belief all visible); and the swap test (a paragraph that could belong to another card: should-fix, with the specific material from the card that would replace it). Each finding: slug, severity, issue, evidence, the exact fix.`, { label: `craft:${x.c.id}`, phase: 'Check', schema: FINDINGS, effort: 'high' }),
    ]).then(([k, f]) => ({ ...x, findings: [...(k ? k.findings : []), ...(f ? f.findings : [])] }))
  },

  (x) => {
    const by = {}
    for (const f of x.findings) (by[f.slug] = by[f.slug] || []).push(f)
    const flagged = x.ws.filter(w => by[w.slug])
    if (!flagged.length) return x.ws
    return parallel(flagged.map(w => () => agent(`${STANDING}
Revise ${L}/cards/${w.slug}.md (cluster ${x.c.id}). Two checkers found:
${by[w.slug].map((f, i) => `${i + 1}. [${f.severity}] ${f.issue}\n   evidence: ${f.evidence}\n   fix: ${f.fix}`).join('\n')}
Read the file, the card, ${L}/LAW.md and ${L}/clusters/${x.c.id}.md. Apply every must-fix. Apply every should-fix unless it would break the card, the archive or the record (then leave it and say why). If a fix changes a shared event or a tie, keep it consistent with what the other files in this cluster say. Keep the format:
${FORMAT}
Re-run \`${PY} build/verify.py ${L}/cards/${w.slug}.md --band standard\` until it passes. Return the result.`, { label: `revise:${w.slug}`, phase: 'Revise', schema: WRITTEN })))
      .then(rs => x.ws.map(w => rs.find(r => r && r.slug === w.slug) || w))
  },
)
const finals = perCluster.filter(Boolean).flat().filter(Boolean)
log(`${finals.length}/${TARGETS.size} lore files written and checked`)

// ------------------------------------------------------------------ reconcile: every tie from both ends
phase('Reconcile')
const tieMap = {}
for (const w of finals) tieMap[w.slug] = new Set(w.ties.map(t => t.other))
const owed = {}
for (const w of finals) for (const t of w.ties) {
  if (!ALLSET.has(t.other) || t.other === w.slug) continue
  if (tieMap[t.other] && tieMap[t.other].has(w.slug)) continue
  ;(owed[t.other] = owed[t.other] || []).push({ from: w.slug, kind: t.kind, line: t.line })
}
const owedList = Object.entries(owed)
log(`${owedList.length} characters owe ties back`)
const patched = (await pipeline(owedList, ([b, list]) => agent(`${STANDING}
${L}/cards/${b}.md is missing ties that other lore files claim:
${list.map(o => `- ${o.from} (${o.kind}): "${o.line}"`).join('\n')}
${tieMap[b] ? '' : `There is no lore file for ${b} from this run: if ${L}/cards/${b}.md exists (an earlier run), patch it; if it does not, return slug "${b}" with words 0 and do nothing.`}
Read each claiming file's passages about ${b}, and ${b}'s card. Add each tie to ${b}'s Ties list from ${b}'s side: the same facts, ${b}'s view of them. If the tie is weighty (kin, teacher, sworn enemy, a debt) and the prose never mentions it, add one sentence where it belongs. If a claim contradicts ${b}'s card, do not add it: say so in "verify". Keep the format; re-run \`${PY} build/verify.py ${L}/cards/${b}.md --band standard\` until it passes. Return the result for ${b}.`, { label: `tie:${b}`, phase: 'Reconcile', schema: WRITTEN, effort: 'medium' }))).filter(Boolean)

// ------------------------------------------------------------------ the hub page
phase('Web')
const web = await agent(`${STANDING}
Write ${L}/THE_WEB.md, the hub page that will sit in Notion under Characters as "The Web of Lives". Read ${L}/LAW.md (it binds this page too), ${L}/_clusters.json, every ${L}/clusters/*.md, ${L}/WEAVE.md, the "### Ties" section of every ${L}/cards/*.md, and ${L}/UNCARDED.md.
Shape: "# The Web of Lives", then two short paragraphs in the register of the Characters page on how to read it. "## The Clusters": per cluster a "### <name>" with its members (card titles), the shared history in one paragraph, and the ties that bear weight as bullets. "## Across the Clusters": a table, three columns: | Between | And | The tie |. "## Threads Left Open": what the web makes possible at the table, one bullet each, nothing resolved. "## In the Archive Without a Card": UNCARDED.md condensed, one bullet per name. Names exactly as the card titles give them, with any em dash in a title written " · " (no em or en dashes anywhere on the page); no slugs anywhere; no numbers the cards do not state. Return the section headings and the word count.`, { label: 'web', phase: 'Web' })

// ------------------------------------------------------------------ audit and one repair round
phase('Audit')
const want = [...TARGETS]
const audit = await agent(`${STANDING}
Audit this run. For each of these slugs: ${want.join(', ')}.
Check ${L}/cards/<slug>.md exists; it begins with "## ${HEAD}"; the provenance line follows; the five subsections appear in order (Origin, The Making, The Cost, Where They Stand, Ties); \`${PY} build/verify.py <file> --band standard\` passes; no "pending" anywhere; every Ties bullet names a card title from the roster or a name in ${L}/UNCARDED.md; and each tie to a carded character is answered in that character's file. Also check ${L}/THE_WEB.md exists and names every cluster.
Then write ${L}/REPORT.md for Isaac: what was written (counts), the clusters, the Weaver's rulings (from ${L}/WEAVE.md), every "Where the cards disagree" item from the cluster records (these are contradictions between existing cards, not resolved here), every new proper name the lore introduced (grep the files against the wiki; list name, file, what it names), and what remains open. Return the gaps (one per slug per problem) and a one-line summary.`, { label: 'audit', phase: 'Audit', schema: GAPS, effort: 'high' })

let repaired = []
if (audit && audit.gaps.length) {
  const bySlug = {}
  for (const g of audit.gaps) if (ALLSET.has(g.slug)) (bySlug[g.slug] = bySlug[g.slug] || []).push(g.issue)
  const clusterOf = s => clusters.find(c => c.members.includes(s)) || clusters[0]
  repaired = (await pipeline(Object.entries(bySlug), ([s, issues]) => agent(issues.some(i => /missing|does not exist|no file/i.test(i))
    ? writePrompt(s, clusterOf(s))
    : `${STANDING}
Repair ${L}/cards/${s}.md. The audit found:
${issues.map(i => `- ${i}`).join('\n')}
Fix each without breaking the card, the archive or the cluster record ${L}/clusters/${clusterOf(s).id}.md.
${FORMAT}
Re-run \`${PY} build/verify.py ${L}/cards/${s}.md --band standard\` until it passes. Return the result.`, { label: `repair:${s}`, phase: 'Audit', schema: WRITTEN }))).filter(Boolean)
  log(`repair round: ${repaired.length}/${Object.keys(bySlug).length} fixed; anything left is in ${L}/REPORT.md`)
}

return {
  targets: TARGETS.size, written: finals.length, clusters: clusters.length, cluster_records: bibles.length,
  cross_ties: weave ? weave.cross_ties.length : 0, ties_reconciled: patched.length, repaired: repaired.length,
  audit: audit ? audit.summary : 'audit failed', gaps: audit ? audit.gaps : [],
  missing: want.filter(s => !finals.some(w => w.slug === s) && !repaired.some(w => w.slug === s)),
  files: `${L}/cards/*.md, ${L}/THE_WEB.md, ${L}/UNCARDED.md, ${L}/REPORT.md`, web: web ? String(web).slice(0, 400) : 'web failed',
}
