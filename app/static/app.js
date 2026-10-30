// WOTR Workshop front end. No build step: one file, hash routes, plain DOM.
// The AI key stays in this browser (localStorage); the server only runs the WOTR tools.
'use strict';

const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const view = () => $('#view');
const S = { me: null, canon: null, list: [], filter: 'all', entry: null, step: 0, images: [], chat: [], convo: null, busy: false, saving: null, tools: null, natalie: null };

const KIND = {
  character: { label: 'Character', color: '#e8b04b', glyph: 'C', blurb: 'A person: Crystal, kit, look and voice.' },
  technique: { label: 'Technique', color: '#86f4ff', glyph: 'T', blurb: 'An art or Trait: phenomenon, cost, counter.' },
  item: { label: 'Weapon or item', color: '#ff6a55', glyph: 'W', blurb: 'Blades, armour, Drafts, relics, by item Tier.' },
  lore: { label: 'Lore', color: '#c79bff', glyph: 'L', blurb: 'History, legends, documents, rumours.' },
  place: { label: 'Place', color: '#2fd1b2', glyph: 'P', blurb: 'Cities, Cores, ruins, roads.' },
  faction: { label: 'Faction', color: '#6f9bff', glyph: 'F', blurb: 'Houses, sects, guilds, orders.' },
};
const AURAS = [['Brass gold', '#e8b04b'], ['Ember', '#ff6a3d'], ['Vermilion', '#ff3b5c'], ['Tide jade', '#2fd1b2'], ['Draw-light', '#86f4ff'],
  ['Cobalt', '#5b7cff'], ['Violet', '#b77bff'], ['Frost', '#cfe8ff'], ['Verdant', '#7be05a'], ['Void', '#8a6bff']];

// ---------- plumbing ----------

async function api(url, opts = {}) {
  const o = { credentials: 'same-origin', ...opts, headers: { ...(opts.headers || {}) } };
  if (o.method && o.method !== 'GET') o.headers['X-WOTR'] = '1';
  if (o.json !== undefined) { o.body = JSON.stringify(o.json); o.headers['Content-Type'] = 'application/json'; delete o.json; }
  const r = await fetch(url, o);
  if (r.status === 401) { location.hash = '#/signin'; throw new Error('sign in'); }
  const body = r.headers.get('content-type')?.includes('json') ? await r.json() : await r.text();
  if (!r.ok) throw new Error(body.error || r.statusText);
  return body;
}
function toast(msg) {
  const t = document.createElement('div'); t.className = 'toast'; t.setAttribute('role', 'status'); t.textContent = msg;
  document.body.append(t); setTimeout(() => t.remove(), 2600);
}
function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k) || 'null'); localStorage.setItem(k, JSON.stringify(v)); } catch { return null; } }
const ai = () => store('wotr.ai') || {};
const img = (id) => `/api/images/${encodeURIComponent(id)}`;

// ---------- schemas: what each kind of entry holds ----------

function schema(kind) {
  const C = S.canon;
  const stageOpts = C.stages.map((s) => `${s.numeral} · ${s.name}`);
  const springs = C.families.flatMap((f) => f.wellsprings.map((w) => w.name));
  const mine = (k) => S.list.filter((e) => e.kind === k).map((e) => e.title);
  const look = { id: 'look', label: 'Look', fields: [{ k: 'aura', label: 'Aura colour', type: 'color' }, { k: '_gallery', type: 'gallery', label: 'Images' }] };
  const card = { id: 'card', label: 'The card', fields: [{ k: '_card', type: 'card' }] };
  if (kind === 'character') return [
    { id: 'origin', label: 'Origin', intro: 'Who they are and where they come from. A name only has to sound right for its culture.', fields: [
      { k: 'title', label: 'Name', type: 'text' }, { k: 'epithet', label: 'Title or by-name', type: 'text', help: 'The Doom Breaker, the Wandering Fang' },
      { k: 'culture', label: 'Culture', type: 'select', opts: C.cultures }, { k: 'lineage', label: 'Race or lineage', type: 'text' },
      { k: 'pronunciation', label: 'Pronunciation', type: 'text' }, { k: 'age', label: 'Age', type: 'text', help: 'Adults only for anything explicit.' },
      { k: 'faction', label: 'Realm or faction', type: 'text' }, { k: 'school', label: 'School and rank', type: 'text', help: 'outer, inner or core disciple; or the guild ladder' },
      { k: 'catalyst', label: 'Catalyst event', type: 'area', wide: true, help: 'The event that opened or broke the Crystal.' }] },
    { id: 'crystal', label: 'Crystal', intro: 'The soul architecture: the Stage they stand at and what the Crystal draws on.', fields: [
      { k: 'stage', label: 'Temperance Stage', type: 'stage', wide: true },
      { k: 'path', label: 'Path', type: 'select', opts: C.paths, help: 'Recognised, not declared.' }, { k: 'band', label: 'Band', type: 'select', opts: ['I', 'II', 'III', 'IV', 'V'] },
      { k: 'aetherClass', label: 'Aether Class', type: 'select', opts: C.aether_classes }, { k: 'crystalTier', label: 'Soul Crystal Tier', type: 'select', opts: C.crystal_tiers },
      { k: 'crystalState', label: 'Crystal State', type: 'text' }, { k: 'essence', label: 'Essence Typology', type: 'select', opts: C.essence },
      { k: 'combatGrammar', label: 'Combat grammar', type: 'select', opts: C.combat_grammar }, { k: 'reserve', label: 'EU reserve', type: 'text', help: 'Natalie can derive it from the tables.' },
      { k: 'wellsprings', label: 'Wellspring harmonisations', type: 'springs', wide: true }] },
    { id: 'kit', label: 'Kit', intro: 'Traits, techniques and releases. Every one carries a cost, a tell and a fair counter.', fields: [
      { k: 'traits', label: 'Traits', type: 'list', add: 'Add a Trait', sub: [{ k: 'name', label: 'Name' }, { k: 'kind', label: 'Reflection', type: 'select', opts: C.trait_kinds },
        { k: 'gloss', label: 'Gloss' }, { k: 'text', label: 'What it does, its cost and limit', type: 'area' }, { k: 'tell', label: 'Tell' }, { k: 'counter', label: 'Counter' }] },
      { k: '_techniques', type: 'linked', label: 'Techniques' },
      { k: 'releases', label: 'Releases', type: 'list', add: 'Add a release', help: 'First from Stage IV, Second from VII, Third from IX.', sub: [{ k: 'name', label: 'Name' },
        { k: 'kind', label: 'Release', type: 'select', opts: ['First Release', 'Second Release', 'Third Release'] }, { k: 'text', label: 'The form it takes, the sound, the drain', type: 'area' }] },
      { k: 'weapon', label: 'Bonded weapon', type: 'text' }, { k: 'vows', label: 'Vows in force', type: 'area', wide: true }] },
    { ...look, fields: [look.fields[0], { k: 'auraSound', label: 'Aura sound', type: 'text', help: 'gogogogo, a low thrum under the floorboards, krrrRRAK' }, look.fields[1],
      { k: 'hair', label: 'Hair', type: 'area', help: 'By comparison.' }, { k: 'face', label: 'Face', type: 'area' }, { k: 'body', label: 'Body', type: 'area' },
      { k: 'clothing', label: 'Clothing, fit and wear', type: 'area' }, { k: 'marks', label: 'Marks', type: 'area' }] },
    { id: 'voice', label: 'Voice & lore', intro: 'What do they refuse, what did they survive, what do they believe that costs them.', fields: [
      { k: 'voiceLine', label: 'A line only they would say', type: 'text', wide: true }, { k: 'speakerType', label: 'Speaker type', type: 'text', help: 'The real-world model for how they talk.' },
      { k: 'refusal', label: 'Refusal', type: 'text' }, { k: 'conviction', label: 'Conviction', type: 'text' }, { k: 'wound', label: 'Core wound', type: 'text' },
      { k: 'desire', label: 'Desire', type: 'text' }, { k: 'flaw', label: 'Flaw', type: 'text' }, { k: 'lore', label: 'Lore', type: 'area', wide: true, rows: 10 }] },
    card,
  ];
  if (kind === 'technique') return [
    { id: 'concept', label: 'Concept', intro: 'Character first, then the phenomenon, then the mechanism, then the Codex.', fields: [
      { k: 'title', label: 'Name, in caps on the card', type: 'text' }, { k: 'gloss', label: 'Gloss', type: 'text' },
      { k: 'kindOf', label: 'Kind', type: 'select', opts: [...C.technique_kinds, ...C.trait_kinds] }, { k: 'owner', label: 'Whose it is', type: 'select', opts: mine('character') },
      { k: 'family', label: 'Family', type: 'select', opts: C.families.map((f) => f.name) }, { k: 'wellspring', label: 'Wellspring', type: 'select', opts: springs },
      { k: 'sound', label: 'Its sound', type: 'text', help: 'Every technique fires with its own sound.' },
      { k: 'idea', label: 'The idea, in your words', type: 'area', wide: true }] },
    { id: 'mechanism', label: 'Mechanism', intro: 'Power is finite and the spending shows. A technique that costs nothing is worse than one left unexplained.', fields: [
      { k: 'phenomenon', label: 'The real phenomenon', type: 'area', help: 'The physics or biology it rides on.' }, { k: 'mechanism', label: 'Mechanism', type: 'area' },
      { k: 'cost', label: 'Cost', type: 'area', help: 'EU against the owner’s reserve, as how long it lasts from full.' }, { k: 'limit', label: 'Limit', type: 'area' },
      { k: 'tell', label: 'Tell', type: 'area' }, { k: 'counter', label: 'A fair counter', type: 'area', help: 'Within reach at its own Stage, on known law.' }] },
    { id: 'entry', label: 'Entry', fields: [{ k: 'entry', label: 'The entry paragraph', type: 'area', wide: true, rows: 9, help: 'Plain everyday words, full figures inline.' }] },
    look, card,
  ];
  if (kind === 'item') return [
    { id: 'concept', label: 'Concept', fields: [
      { k: 'title', label: 'Name', type: 'text' }, { k: 'kindOf', label: 'Kind', type: 'select', opts: ['Blade', 'Polearm', 'Firearm', 'Shot', 'Armour', 'Shield', 'Focus', 'Draft', 'Tool', 'Relic'] },
      { k: 'tier', label: 'Item Tier', type: 'select', opts: C.item_tiers, help: 'The lower of what the material holds and the maker’s standing.' },
      { k: 'owner', label: 'Carried by', type: 'select', opts: mine('character') }, { k: 'maker', label: 'Maker', type: 'text' }, { k: 'material', label: 'Material', type: 'text' },
      { k: 'trueName', label: 'True name', type: 'text' }, { k: 'price', label: 'Price', type: 'text' }] },
    { id: 'working', label: 'Working', fields: [{ k: 'mechanism', label: 'The working in it', type: 'area' }, { k: 'cost', label: 'Cost', type: 'area' },
      { k: 'counter', label: 'Counter', type: 'area' }, { k: 'sound', label: 'Its sound', type: 'text' }, { k: 'description', label: 'Description', type: 'area', wide: true, rows: 7 }] },
    look, card,
  ];
  const kinds = { lore: ['History', 'Legend', 'Document', 'Rumour', 'Custom', 'Song'], place: ['City', 'Town', 'Region', 'Core', 'Ruin', 'Road', 'Building'],
    faction: ['House', 'Sect', 'Guild', 'Order', 'Company', 'Cult', 'Crew'] }[kind];
  const extra = { lore: [{ k: 'era', label: 'Era or date', type: 'text' }],
    place: [{ k: 'culture', label: 'Culture', type: 'select', opts: C.cultures }, { k: 'senses', label: 'Sights, sounds, smells', type: 'area', wide: true }],
    faction: [{ k: 'culture', label: 'Culture', type: 'select', opts: C.cultures }, { k: 'leader', label: 'Who leads it', type: 'text' },
      { k: 'wants', label: 'What it wants', type: 'area' }, { k: 'holdings', label: 'What it holds', type: 'area' }] }[kind];
  return [
    { id: 'concept', label: 'Concept', fields: [{ k: 'title', label: 'Name', type: 'text' }, { k: 'kindOf', label: 'Kind', type: 'select', opts: kinds }, ...extra,
      { k: 'body', label: kind === 'lore' ? 'The text' : 'Description', type: 'area', wide: true, rows: 12 }] },
    look, card,
  ];
}

// ---------- the card: markdown in the house template's shape ----------

function cardMarkdown(e) {
  const d = e.data, L = (label, v) => (v ? `**${label}** · ${v}\n` : '');
  const name = (e.title || 'Untitled').toUpperCase();
  if (e.kind === 'character') {
    const st = S.canon.stages.find((s) => s.numeral === d.stage);
    const items = (xs, f) => (xs || []).filter((x) => x.name).map(f).join(' / ');
    const techs = (e._techs || []).filter((x) => x.title).map((x) => x.title.toUpperCase());
    let md = `---\ntype: character-card\ntitle: ${e.title}\nsubtitle: ${d.epithet || ''}\nculture: ${d.culture || ''}\nrung: short\nowner: ${S.me?.name || ''}\n---\n\n# ${e.title}\n\n`;
    md += `**${e.title}** · ${[d.epithet, d.culture].filter(Boolean).join(' · ')}\n`;
    md += L('Stat line', [d.band && `Band ${d.band}`, st && `Stage ${st.numeral}, ${st.name}`, d.path && `Path ${d.path}`, d.aetherClass && `Aether Class ${d.aetherClass}`,
      d.crystalTier && `Crystal ${d.crystalTier}${d.crystalState ? ', ' + d.crystalState : ''}`].filter(Boolean).join(' · '));
    md += L('Combat grammar', d.combatGrammar) + L('Aura and sound', [d.aura && `colour: ${auraName(d.aura)}`, d.auraSound && `signature sound: ${d.auraSound}`].filter(Boolean).join(' · '));
    md += L('Releases', items(d.releases, (r) => `${r.name.toUpperCase()} (${r.kind || 'Release'})`)) + L('Bonded weapon', d.weapon);
    md += L('Traits', items(d.traits, (t) => `${t.name.toUpperCase()} (${t.kind || 'Trait'})${t.tell ? ' · tell: ' + t.tell : ''}${t.counter ? ' · counter: ' + t.counter : ''}`));
    md += L('Techniques', techs.join(' / ')) + L('Voice', [d.voiceLine && `"${d.voiceLine}"`, d.speakerType && `speaker type: ${d.speakerType}`].filter(Boolean).join(' · '));
    md += `\n---\n\n## I. Identity\n\n` + L('Full Name', e.title) + L('Pronunciation', d.pronunciation) + L('Alias / Title', d.epithet) + L('Race / Lineage', d.lineage) +
      L('Age', d.age) + L('Realm / Faction', d.faction) + L('School and sect rank', d.school) + L('Catalyst Event', d.catalyst) + L('Refusal', d.refusal) + L('Conviction', d.conviction);
    md += `\n## II. Soul Architecture\n\n` + L('Band', d.band) + L('Temperance Stage', st && `${st.numeral}, ${st.name}`) + L('Path', d.path) + L('Tier of Standing', st && `${st.standing} (Tier ${st.tier})`) +
      L('Soul Crystal Tier', d.crystalTier) + L('Crystal State', d.crystalState) + L('Aether Class', d.aetherClass) + L('Essence Typology', d.essence) + L('EU Reserve', d.reserve);
    if ((d.wellsprings || []).length) md += `\n## III. Wellspring Harmonizations\n\n` + d.wellsprings.map((w) => `**${w}**\n`).join('');
    if ((d.traits || []).some((t) => t.name)) md += `\n## VIII. Traits\n\n` + d.traits.filter((t) => t.name).map((t) => `**${t.name.toUpperCase()}${t.gloss ? ' · ' + t.gloss : ''} (${t.kind || 'Trait'})**\n${t.text || ''}\n`).join('\n');
    if (techs.length) md += `\n## X. Techniques\n\n` + techs.map((t) => `**${t}**\n`).join('');
    if (d.vows) md += `\n**Vows** · ${d.vows}\n`;
    if ((d.releases || []).some((r) => r.name)) md += '\n' + d.releases.filter((r) => r.name).map((r) => `**${r.name.toUpperCase()} (${r.kind || 'Release'})**\n${r.text || ''}\n`).join('\n');
    const phys = [d.hair, d.face, d.body, d.clothing, d.marks].filter(Boolean).join(' ');
    if (phys) md += `\n## XIII. Physical Description\n\n${phys}\n`;
    md += `\n## XIV. Psychology\n\n` + L('Core Wound', d.wound) + L('Flaw', d.flaw) + L('Desire', d.desire) + L('Speaker type', d.speakerType) + L('Sample line', d.voiceLine && `"${d.voiceLine}"`);
    if (d.lore) md += `\n---\n\n## Lore\n\n${d.lore}\n`;
    return md;
  }
  if (e.kind === 'technique') {
    return `**${name}${d.gloss ? ' · ' + d.gloss : ''} (${d.kindOf || 'Technique'})**${d.owner ? ' · ' + d.owner : ''}\n` +
      (d.entry || [d.mechanism, d.cost && 'Cost: ' + d.cost, d.limit && 'Limit: ' + d.limit, d.tell && 'Tell: ' + d.tell, d.counter && 'Counter: ' + d.counter].filter(Boolean).join(' ')) +
      `\n\n` + L('Family', d.family) + L('Wellspring', d.wellspring) + L('Sound', d.sound) + L('Phenomenon', d.phenomenon);
  }
  if (e.kind === 'item') {
    return `**${e.title}** · ${[d.kindOf, d.tier && 'Item Tier ' + d.tier, d.material, d.maker && 'made by ' + d.maker].filter(Boolean).join(' · ')}\n\n` +
      L('True name', d.trueName) + L('Carried by', d.owner) + L('Working', d.mechanism) + L('Cost', d.cost) + L('Counter', d.counter) + L('Sound', d.sound) + L('Price', d.price) + (d.description ? `\n${d.description}\n` : '');
  }
  return `# ${e.title}\n\n` + L('Kind', d.kindOf) + L('Era', d.era) + L('Culture', d.culture) + L('Leader', d.leader) + L('Wants', d.wants) + L('Holdings', d.holdings) +
    (d.body ? `\n${d.body}\n` : '') + (d.senses ? `\n${d.senses}\n` : '');
}
const auraName = (hex) => (AURAS.find((a) => a[1] === hex) || [hex])[0];

// ---------- views ----------

function nav(active) {
  $('#nav').innerHTML = S.me ? [['#/', 'Library', 'lib'], ['#/ai', 'Your AI', 'ai'], ['#/scenes', 'Scenes', 'scenes']].map(([h, l, k]) =>
    `<a href="${h}"${k === active ? ' aria-current="page"' : ''}>${l}${k === 'scenes' ? '<span class="soon">soon</span>' : ''}</a>`).join('') : '';
  $('#who').innerHTML = S.me ? `${S.me.avatar ? `<img src="${esc(S.me.avatar)}" alt="">` : `<span class="avatar">${esc(S.me.name[0] || '?')}</span>`}
    <span>${esc(S.me.name)}</span><a class="btn small" href="/auth/logout">Sign out</a>` : '';
}

async function signin() {
  nav('');
  const err = new URLSearchParams(location.hash.split('?')[1] || '').get('error');
  const status = await fetch('/api/status').then((r) => r.json()).catch(() => ({}));
  view().innerHTML = `<section class="gate">
    <div class="art"><p class="kicker">The Draw Age · a designer and a table</p>
      <h1 class="title" style="--aura:#43dcbc">Forge your <em>legend</em></h1>
      <p class="lede">Build characters, techniques, weapons and lore in your own library, with portraits and a card for each. Bring your own AI and Natalie joins you, already wired to the canon.</p></div>
    <div class="paper" style="display:flex;flex-direction:column;gap:16px">
      <h2 class="sec">Sign in</h2>
      ${err ? `<p class="msg err">${esc({ invite: 'That invite code is not valid, or it has been used.', discord: 'Discord did not let us in. Try again.', state: 'The sign-in expired. Try again.' }[err] || err)}</p>` : ''}
      <p class="msg err" id="kerr" role="alert" hidden></p>
      <div class="f"><label for="inv">Your key</label><input id="inv" type="text" autocomplete="username" spellcheck="false" placeholder="e.g. 4F2A-91C0-7B3E-0D55"></div>
      <div class="f"><label for="kname">Your name</label><input id="kname" type="text" autocomplete="nickname" placeholder="Only the first time you use a new key"></div>
      <button class="btn primary" id="enter">Enter the Workshop</button>
      <p class="hint">Isaac gives you a key. The first time you use it, it becomes yours: it signs you back in on any device, so keep it like a password.</p>
      ${status.discord ? `<div class="ruler">or</div><button class="btn discord" id="go">Continue with Discord</button>` : ''}
      ${status.dev ? `<div class="ruler">local testing</div><a class="btn" href="/auth/dev?name=Isaac">Dev sign-in</a>` : ''}
      <p class="hint">Your library is yours: nobody else sees it, and nothing in it becomes table canon on its own.</p>
    </div></section>`;
  $('#go') && ($('#go').onclick = () => { location.href = '/auth/discord?invite=' + encodeURIComponent($('#inv').value.trim()); });
  const enter = async () => {
    const r = await fetch('/auth/key', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-WOTR': '1' },
      body: JSON.stringify({ key: $('#inv').value, name: $('#kname').value }) });
    if (r.ok) { S.me = null; location.hash = '#/'; return; }
    const j = await r.json().catch(() => ({})); const e = $('#kerr'); e.hidden = false; e.textContent = j.error || 'Could not sign in.';
    if (j.need_name) $('#kname').focus();
  };
  $('#enter').onclick = enter;
  view().addEventListener('keydown', (ev) => { if (ev.key === 'Enter' && (ev.target.id === 'inv' || ev.target.id === 'kname')) enter(); });
}

async function library() {
  nav('lib');
  S.list = await api('/api/entries');
  const counts = Object.fromEntries(Object.keys(KIND).map((k) => [k, S.list.filter((e) => e.kind === k).length]));
  const shown = S.list.filter((e) => S.filter === 'all' || e.kind === S.filter);
  view().innerHTML = `
    <section class="hero"><div><p class="kicker">${esc(S.me.name)}'s workshop</p><h1 class="title">Your <em>library</em></h1>
      <p class="lede">Everything you make lives here, private to you, each with its own aura and its own card.</p></div></section>
    <div class="makers">${Object.entries(KIND).map(([k, v]) => `<button class="maker" style="--k:${v.color}" data-new="${k}"><img src="/static/art/em-${k}.webp" alt="" onerror="this.outerHTML='<span class=em-fallback>${v.glyph}</span>'"><span><b>${esc(v.label)}</b><span>${esc(v.blurb)}</span></span></button>`).join('')}</div>
    <div class="tabs" role="group" aria-label="Show">${[['all', 'Everything', S.list.length], ...Object.entries(KIND).map(([k, v]) => [k, v.label, counts[k]])].map(([k, l, n]) =>
      `<button class="tab" data-filter="${k}" aria-pressed="${S.filter === k}">${esc(l)}<small>${n}</small></button>`).join('')}</div>
    ${shown.length ? `<div class="grid">${shown.map(cardTile).join('')}</div>` :
      `<div class="paper empty"><b>Nothing forged yet</b>Start with a character: the rest of the library hangs off them.</div>`}`;
}
function cardTile(e) {
  const k = KIND[e.kind];
  const aura = e.kind === 'character' && e.aura ? e.aura : k.color;
  const sub = [e.epithet, e.kindOf, e.culture].filter(Boolean).join(' · ') || k.label;
  return `<a class="card" href="#/e/${esc(e.id)}" style="--aura:${esc(aura)};--k:${k.color}">
    <span class="seal">${esc(k.label)}</span>
    <span class="pic">${e.portrait ? `<img class="full" src="${img(e.portrait)}" alt="" loading="lazy">` : `<img class="em" src="/static/art/em-${e.kind}.webp" alt="">`}</span>
    <span class="body"><b>${esc(e.title || 'Untitled')}</b><span>${esc(sub)}</span></span></a>`;
}

async function create(kind) {
  const e = await api('/api/entries', { method: 'POST', json: { kind, title: '', data: kind === 'character' ? { aura: '#e8b04b' } : {} } });
  location.replace(`#/e/${e.id}`);
}

async function editor(id, stepId) {
  nav('lib');
  if (!S.entry || S.entry.id !== id) {
    [S.entry, S.images, S.list] = await Promise.all([api(`/api/entries/${id}`), api(`/api/entries/${id}/images`), api('/api/entries')]);
    S.chat = []; S.convo = null;
  }
  const steps = schema(S.entry.kind);
  S.step = Math.max(0, steps.findIndex((s) => s.id === stepId));
  const e = S.entry, k = KIND[e.kind];
  const aura = e.data.aura || k.color;
  const hasAI = !!(ai().provider);
  view().style.setProperty('--aura', aura);
  view().innerHTML = `
    <div class="spread"><div><p class="kicker" style="color:${k.color}">${esc(k.label)}</p>
      <h1 class="title" id="etitle">${esc(e.title || 'Untitled')}</h1>
      ${e.data.epithet ? `<p class="lede" style="margin-top:4px">${esc(e.data.epithet)}</p>` : ''}</div>
      <div class="row"><span class="hint" id="saved" role="status">Saved</span><a class="btn small" href="#/">Library</a><button class="btn small danger" id="del">Delete</button></div></div>
    <div class="ed${hasAI ? '' : ' nonat'}">
      <nav class="steps" aria-label="Sections">${steps.map((s, i) => `<button class="step" data-step="${s.id}"${i === S.step ? ' aria-current="step"' : ''}><i aria-hidden="true">${'一二三四五六七八'[i]}</i><span class="sr">${i + 1}. </span>${esc(s.label)}</button>`).join('')}
        ${hasAI ? '' : `<a class="btn draw small" href="#/ai" style="margin-top:12px">Bring Natalie in</a>`}</nav>
      <section class="sheet" id="sheet">${sheet(steps[S.step])}</section>
      ${hasAI ? natPanel() : ''}
    </div>`;
  $('#etitle').scrollIntoView?.({ block: 'nearest' });
}

function sheet(step) {
  return `<div class="paper"><h2 class="sec">${esc(step.label)}</h2>${step.intro ? `<p class="hint" style="margin-bottom:16px">${esc(step.intro)}</p>` : ''}
    <div class="fields">${step.fields.map(field).join('')}</div></div>`;
}

function field(f) {
  const d = S.entry.data, v = f.k === 'title' ? S.entry.title : d[f.k];
  const id = 'f_' + f.k, help = f.help ? `<span class="help">${esc(f.help)}</span>` : '';
  const wrap = (inner, wide) => `<div class="f${wide || f.wide ? ' wide' : ''}">${inner}${help}</div>`;
  switch (f.type) {
    case 'text': return wrap(`<label for="${id}">${esc(f.label)}</label><input id="${id}" type="text" data-k="${f.k}" value="${esc(v)}">`);
    case 'area': return wrap(`<label for="${id}">${esc(f.label)}</label><textarea id="${id}" data-k="${f.k}" rows="${f.rows || 4}">${esc(v)}</textarea>`);
    case 'select': return wrap(`<label for="${id}">${esc(f.label)}</label><select id="${id}" data-k="${f.k}"><option value=""></option>${
      [...new Set([...(f.opts || []), ...(v && !(f.opts || []).includes(v) ? [v] : [])])].map((o) => `<option${o === v ? ' selected' : ''}>${esc(o)}</option>`).join('')}</select>`);
    case 'stage': return wrap(`<span class="lbl">${esc(f.label)}</span><div class="ladder" role="group" aria-label="${esc(f.label)}">${S.canon.stages.map((s) => {
      const t = ['#9fe7c9', '#2fd1b2', '#86f4ff', '#6f9bff', '#b77bff', '#ff6a9a', '#ff6a3d', '#e8b04b', '#ffd47c'][s.tier - 1];
      return `<button class="rung" style="--t:${t}" data-set="stage" data-v="${s.numeral}" aria-pressed="${v === s.numeral}"><b>${s.numeral}</b><span>${esc(s.name)}</span><small>Tier ${s.tier} · ${esc(s.standing)}</small></button>`;
    }).join('')}</div>`, true);
    case 'springs': {
      const on = new Set(v || []);
      return wrap(`<span class="lbl">${esc(f.label)}</span><span class="help">Fixed canon: the Sixty Wellsprings by Family. Pick the ones the Crystal is harmonised with.</span>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px">${S.canon.families.map((fam) => `<div class="fam"><b>${esc(fam.name)}<small>${esc(fam.domain)}</small></b>
        <div class="chips">${fam.wellsprings.map((w) => `<button class="chip" data-toggle="wellsprings" data-v="${esc(w.name)}" aria-pressed="${on.has(w.name)}">${esc(w.name)}<small>${esc(w.gloss)}</small></button>`).join('')}</div></div>`).join('')}</div>`, true);
    }
    case 'color': return wrap(`<span class="lbl">${esc(f.label)}</span><div class="swatches" role="group" aria-label="${esc(f.label)}">${AURAS.map(([n, hex]) =>
      `<button class="sw" style="background:${hex};color:${hex}" data-set="${f.k}" data-v="${hex}" aria-label="${esc(n)}" aria-pressed="${v === hex}"></button>`).join('')}
      <label class="sr" for="${id}">Any colour</label><input id="${id}" type="color" data-k="${f.k}" value="${esc(v || '#e8b04b')}" title="Any colour"></div>`);
    case 'list': {
      const xs = v || [];
      return wrap(`<span class="lbl">${esc(f.label)}</span><div class="items">${xs.map((x, i) => `<div class="item">
        <div class="fields">${f.sub.map((s) => { const sid = `f_${f.k}_${i}_${s.k}`, sk = `${f.k}.${i}.${s.k}`, sv = x[s.k];
          if (s.type === 'select') return `<div class="f"><label for="${sid}">${esc(s.label)}</label><select id="${sid}" data-k="${sk}"><option value=""></option>${s.opts.map((o) => `<option${o === sv ? ' selected' : ''}>${esc(o)}</option>`).join('')}</select></div>`;
          if (s.type === 'area') return `<div class="f wide"><label for="${sid}">${esc(s.label)}</label><textarea id="${sid}" data-k="${sk}" rows="3">${esc(sv)}</textarea></div>`;
          return `<div class="f${s.k === 'name' ? ' name' : ''}"><label for="${sid}">${esc(s.label)}</label><input id="${sid}" type="text" data-k="${sk}" value="${esc(sv)}"></div>`; }).join('')}</div>
        <div class="row"><button class="btn small danger" data-remove="${f.k}" data-i="${i}">Remove</button></div></div>`).join('')}
        <div class="row"><button class="btn small" data-add="${f.k}">+ ${esc(f.add)}</button></div></div>`, true);
    }
    case 'linked': {
      const mineT = S.list.filter((x) => x.kind === 'technique');
      return wrap(`<span class="lbl">${esc(f.label)}</span><span class="help">Techniques are entries of their own, so each gets the full design pass. Ones whose owner is ${esc(S.entry.title || 'this character')} show here.</span>
        <div class="row" id="linked" data-count="${mineT.length}"></div><div class="row"><button class="btn small" data-new="technique">+ New technique for ${esc(S.entry.title || 'them')}</button></div>`, true);
    }
    case 'gallery': {
      const p = S.entry.portrait;
      return wrap(`<span class="lbl">${esc(f.label)}</span>
        <div style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start">
          <div class="portrait" style="flex:0 1 300px">${p ? `<img src="${img(p)}" alt="Portrait of ${esc(S.entry.title)}">` : `<span class="glyph" aria-hidden="true">${esc((S.entry.title || '?')[0])}</span>`}</div>
          <div style="flex:1 1 280px;display:flex;flex-direction:column;gap:12px;min-width:0">
            <div class="drop" id="drop">Drop images here, or <label class="btn small" style="display:inline-flex" for="upl">choose files</label><input id="upl" type="file" accept="image/png,image/jpeg,image/webp,image/gif" multiple class="sr"></div>
            <div class="f"><label for="iprompt">Portrait description</label><textarea id="iprompt" rows="3" placeholder="Left empty, it is drawn from the look fields and the aura">${esc(S.entry.data.imagePrompt)}</textarea></div>
            <div class="row"><button class="btn draw small" id="gen">Generate an image</button><span class="hint">Runs on your own image key, set in Your AI.</span></div>
            <div class="gallery">${S.images.map((im) => `<figure class="${im.id === p ? 'on' : ''}"><img src="${img(im.id)}" alt="" loading="lazy">
              <figcaption><button data-portrait="${im.id}">${im.id === p ? 'Portrait' : 'Use'}</button><button data-unimg="${im.id}" aria-label="Delete image">✕</button></figcaption></figure>`).join('')}</div>
          </div></div>`, true);
    }
    case 'card': {
      const md = cardMarkdown(S.entry), d = S.entry.data, st = S.canon.stages.find((s) => s.numeral === d.stage);
      const rows = S.entry.kind === 'character' ? [['Culture', d.culture], ['Stage', st && `${st.numeral} · ${st.name}`], ['Path', d.path], ['Aether Class', d.aetherClass],
        ['Crystal', [d.crystalTier, d.crystalState].filter(Boolean).join(', ')], ['Wellsprings', (d.wellsprings || []).join(', ')], ['Aura', [auraName(d.aura || ''), d.auraSound].filter(Boolean).join(' · ')],
        ['Traits', (d.traits || []).map((t) => t.name).filter(Boolean).join(', ')], ['Voice', d.voiceLine && `“${d.voiceLine}”`]]
        : [['Kind', d.kindOf], ['Owner', d.owner], ['Tier', d.tier], ['Wellspring', d.wellspring], ['Cost', d.cost], ['Counter', d.counter]];
      const p = S.entry.portrait;
      return wrap(`<div class="assay"><div class="seal" aria-hidden="true">GUILD<br>ASSAY</div>
        <div class="top"><div class="mini">${p ? `<img src="${img(p)}" alt="">` : `<span class="glyph" aria-hidden="true">${esc((S.entry.title || '?')[0])}</span>`}</div>
        <div style="flex:1 1 240px;min-width:0"><h3>${esc(S.entry.title || 'Untitled')}</h3>
        <p class="sub">${esc([d.epithet, d.gloss, KIND[S.entry.kind].label].filter(Boolean).join(' · '))}</p></div></div>
        <dl>${rows.filter((r) => r[1]).map(([a, b]) => `<dt>${esc(a)}</dt><dd>${esc(b)}</dd>`).join('') || '<dd class="hint">Fill the sections and the plate fills itself.</dd>'}</dl></div>
        <div class="row" style="margin-top:16px"><button class="btn primary" id="dl">Download the card (.md)</button><button class="btn" id="copy">Copy markdown</button></div>
        <details style="margin-top:12px"><summary class="hint" style="cursor:pointer;min-height:44px;display:flex;align-items:center">Show the markdown</summary><div class="md">${esc(md)}</div></details>`, true);
    }
  }
  return '';
}

// ---------- editing ----------

function setPath(obj, path, val) {
  const ks = path.split('.'); let o = obj;
  ks.slice(0, -1).forEach((k, i) => { if (o[k] == null) o[k] = /^\d+$/.test(ks[i + 1]) ? [] : {}; o = o[k]; });
  o[ks.at(-1)] = val;
}
function changed(rerender) {
  $('#saved') && ($('#saved').textContent = 'Saving…');
  clearTimeout(S.saving);
  S.saving = setTimeout(save, 600);
  if (rerender) redrawSheet();
}
async function save() {
  const e = S.entry;
  try {
    const out = await api(`/api/entries/${e.id}`, { method: 'PUT', json: { title: e.title, data: e.data, portrait: e.portrait } });
    S.entry.updated = out.updated;
    $('#saved') && ($('#saved').textContent = 'Saved');
  } catch (err) { $('#saved') && ($('#saved').textContent = 'Not saved: ' + err.message); }
}
function redrawSheet() {
  const steps = schema(S.entry.kind);
  $('#sheet').innerHTML = sheet(steps[S.step]);
  view().style.setProperty('--aura', S.entry.data.aura || KIND[S.entry.kind].color);
  $('#etitle') && ($('#etitle').textContent = S.entry.title || 'Untitled');
  fillLinked();
}
function fillLinked() {
  const box = $('#linked'); if (!box) return;
  const ts = S.list.filter((x) => x.kind === 'technique');
  Promise.all(ts.map((t) => api(`/api/entries/${t.id}`))).then((full) => {
    const mine = full.filter((t) => t.data.owner && t.data.owner === S.entry.title);
    box.innerHTML = mine.length ? mine.map((t) => `<a class="chip" href="#/e/${esc(t.id)}" style="text-decoration:none">${esc((t.title || 'Untitled').toUpperCase())}<small>${esc(t.data.kindOf || 'Technique')}</small></a>`).join('')
      : '<span class="hint">None yet.</span>';
    S.entry._techs = mine;
  });
}

document.addEventListener('input', (ev) => {
  const k = ev.target.dataset?.k; if (!k || !S.entry) return;
  if (k === 'title') { S.entry.title = ev.target.value; $('#etitle').textContent = ev.target.value || 'Untitled'; }
  else setPath(S.entry.data, k, ev.target.value);
  if (k === 'aura') view().style.setProperty('--aura', ev.target.value);
  if (ev.target.id === 'iprompt') S.entry.data.imagePrompt = ev.target.value;
  changed(false);
});
document.addEventListener('change', (ev) => { if (ev.target.id === 'iprompt') { S.entry.data.imagePrompt = ev.target.value; changed(false); } });

document.addEventListener('click', async (ev) => {
  const b = ev.target.closest('button, [data-new]'); if (!b) return;
  const ds = b.dataset;
  if (ds.new) {
    if (S.entry && ds.new === 'technique' && b.closest('#sheet')) {
      const t = await api('/api/entries', { method: 'POST', json: { kind: 'technique', title: '', data: { owner: S.entry.title } } });
      location.hash = `#/e/${t.id}`; return;
    }
    return create(ds.new);
  }
  if (ds.filter) { S.filter = ds.filter; return library(); }
  if (ds.step) { location.hash = `#/e/${S.entry.id}/${ds.step}`; return; }
  if (ds.set) { S.entry.data[ds.set] = S.entry.data[ds.set] === ds.v && ds.set === 'stage' ? '' : ds.v; return changed(true); }
  if (ds.toggle) { const xs = new Set(S.entry.data[ds.toggle] || []); xs.has(ds.v) ? xs.delete(ds.v) : xs.add(ds.v); S.entry.data[ds.toggle] = [...xs]; return changed(true); }
  if (ds.add) { (S.entry.data[ds.add] ||= []).push({}); return changed(true); }
  if (ds.remove) { S.entry.data[ds.remove].splice(+ds.i, 1); return changed(true); }
  if (ds.portrait) { S.entry.portrait = ds.portrait; return changed(true); }
  if (ds.unimg) { if (!confirm('Delete this image?')) return; await api(`/api/images/${ds.unimg}`, { method: 'DELETE' });
    S.images = S.images.filter((i) => i.id !== ds.unimg); if (S.entry.portrait === ds.unimg) S.entry.portrait = null; return redrawSheet(); }
  if (b.id === 'del') { if (!confirm(`Delete ${S.entry.title || 'this entry'} and its images? This cannot be undone.`)) return;
    await api(`/api/entries/${S.entry.id}`, { method: 'DELETE' }); S.entry = null; location.hash = '#/'; return; }
  if (b.id === 'dl') { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([cardMarkdown(S.entry)], { type: 'text/markdown' }));
    a.download = (S.entry.title || 'untitled').replace(/[^\p{L}\p{N} _-]/gu, '') + '.md'; a.click(); return; }
  if (b.id === 'copy') { await navigator.clipboard.writeText(cardMarkdown(S.entry)); return toast('Copied'); }
  if (b.id === 'gen') return generateImage(b);
  if (b.id === 'send') return natalieSend();
  if (b.id === 'aisave') return saveAI();
  if (b.id === 'aitest') return testAI(b);
});

async function upload(files) {
  for (const f of files) {
    const fd = new FormData(); fd.append('file', f);
    try { const im = await api(`/api/entries/${S.entry.id}/images`, { method: 'POST', body: fd }); S.images.push(im); if (!S.entry.portrait) S.entry.portrait = im.id; }
    catch (err) { toast(`${f.name}: ${err.message}`); }
  }
  redrawSheet();
}
document.addEventListener('change', (ev) => { if (ev.target.id === 'upl') upload(ev.target.files); });
document.addEventListener('dragover', (ev) => { const d = ev.target.closest?.('#drop'); if (d) { ev.preventDefault(); d.classList.add('over'); } });
document.addEventListener('dragleave', (ev) => ev.target.closest?.('#drop')?.classList.remove('over'));
document.addEventListener('drop', (ev) => { const d = ev.target.closest?.('#drop'); if (d) { ev.preventDefault(); upload(ev.dataTransfer.files); } });

async function generateImage(btn) {
  const c = ai();
  if (!c.imageKey) { toast('Add an image key in Your AI first'); return; }
  const d = S.entry.data;
  const prompt = (d.imagePrompt && d.imagePrompt.trim()) || [`Portrait for a dark shonen cultivation fantasy, magitech Draw Age, vivid colour and light.`,
    S.entry.title && `${S.entry.title}${d.epithet ? ', ' + d.epithet : ''}.`, d.lineage, d.culture && `${d.culture} culture.`, d.hair, d.face, d.body, d.clothing, d.marks,
    d.aura && `Aura glowing ${auraName(d.aura)} (${d.aura}).`, d.description, d.body && S.entry.kind !== 'character' ? d.body : ''].filter(Boolean).join(' ');
  btn.disabled = true; btn.textContent = 'Generating…';
  try {
    const r = await fetch((c.imageBase || 'https://api.openai.com/v1') + '/images/generations', { method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + c.imageKey },
      body: JSON.stringify({ model: c.imageModel || 'gpt-image-1', prompt, size: '1024x1536', n: 1 }) });
    const j = await r.json(); if (!r.ok) throw new Error(j.error?.message || r.statusText);
    const b64 = j.data?.[0]?.b64_json; if (!b64) throw new Error('no image came back');
    const blob = await (await fetch('data:image/png;base64,' + b64)).blob();
    await upload([new File([blob], 'generated.png', { type: 'image/png' })]);
  } catch (err) { toast('Image: ' + err.message); }
  finally { btn.disabled = false; btn.textContent = 'Generate an image'; }
}

// ---------- Your AI ----------

const PROVIDERS = {
  anthropic: { label: 'Anthropic', base: 'https://api.anthropic.com', model: 'claude-opus-5-5', key: 'sk-ant-…' },
  openai: { label: 'OpenAI', base: 'https://api.openai.com/v1', model: '', key: 'sk-…' },
  openrouter: { label: 'OpenRouter', base: 'https://openrouter.ai/api/v1', model: '', key: 'sk-or-…' },
  local: { label: 'Local AI', base: 'http://localhost:11434/v1', model: '', key: 'not needed' },
};
function aiView() {
  nav('ai');
  const c = ai(), p = c.provider || 'anthropic', P = PROVIDERS[p];
  view().innerHTML = `<p class="kicker">Bring your own</p><h1 class="title" style="--aura:#b77bff">Your <em>AI</em></h1>
    <p class="lede">Natalie runs on your own key or a model on your own machine. It is connected to the WOTR tools by itself: the rules, the Codex, the wiki and the skills. The key stays in this browser.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px;margin-top:26px">
    <section class="paper" style="display:flex;flex-direction:column;gap:14px"><h2 class="sec">Natalie</h2>
      <div class="chips" role="group" aria-label="Provider">${Object.entries(PROVIDERS).map(([k, v]) => `<button class="chip" data-prov="${k}" aria-pressed="${k === p}">${v.label}</button>`).join('')}</div>
      <div class="f"><label for="ai_base">Server address</label><input id="ai_base" type="url" value="${esc(c.base || P.base)}">
        ${p === 'local' ? `<span class="help">Ollama, LM Studio, llama.cpp or any OpenAI-compatible server. Your browser calls it directly; allow this site in its CORS setting (for Ollama, OLLAMA_ORIGINS). The model needs tool calling.</span>` : ''}</div>
      ${p === 'local' ? '' : `<div class="f"><label for="ai_key">API key</label><input id="ai_key" type="password" autocomplete="off" placeholder="${esc(P.key)}" value="${esc(c.key || '')}"></div>`}
      <div class="f"><label for="ai_model">Model</label><input id="ai_model" type="text" value="${esc(c.model || P.model)}" placeholder="${p === 'local' ? 'e.g. qwen3' : 'model id'}"></div>
      <div class="row"><button class="btn primary" id="aisave">Save</button><button class="btn draw" id="aitest">Test it</button>${c.provider ? `<button class="btn danger" id="aiforget">Forget</button>` : ''}</div>
      <p class="hint" id="aistatus" role="status"></p></section>
    <section class="paper" style="display:flex;flex-direction:column;gap:14px"><h2 class="sec">Images</h2>
      <p class="hint">Portrait generation uses an OpenAI-compatible images endpoint on your own key. Uploading your own art needs nothing.</p>
      <div class="f"><label for="im_base">Images server</label><input id="im_base" type="url" value="${esc(c.imageBase || 'https://api.openai.com/v1')}"></div>
      <div class="f"><label for="im_key">Image key</label><input id="im_key" type="password" autocomplete="off" value="${esc(c.imageKey || '')}"></div>
      <div class="f"><label for="im_model">Image model</label><input id="im_model" type="text" value="${esc(c.imageModel || 'gpt-image-1')}"></div>
      <div class="row"><button class="btn primary" id="aisave2">Save</button></div></section></div>`;
  view().querySelectorAll('[data-prov]').forEach((b) => b.onclick = () => { store('wotr.ai', { ...ai(), provider: b.dataset.prov, base: PROVIDERS[b.dataset.prov].base, model: PROVIDERS[b.dataset.prov].model, key: '' }); aiView(); });
  $('#aisave2').onclick = saveAI;
  $('#aiforget') && ($('#aiforget').onclick = () => { store('wotr.ai', {}); aiView(); toast('Forgotten'); });
}
function saveAI() {
  const v = (id) => $(id)?.value.trim() ?? '';
  const c = ai();
  store('wotr.ai', { ...c, provider: c.provider || 'anthropic', base: v('#ai_base'), key: v('#ai_key'), model: v('#ai_model'), imageBase: v('#im_base'), imageKey: v('#im_key'), imageModel: v('#im_model') });
  S.convo = null; toast('Saved on this device');
}
async function testAI(btn) {
  saveAI(); btn.disabled = true; $('#aistatus').textContent = 'Asking…';
  try { const r = await llm([{ role: 'user', content: 'Reply with the single word: ready' }], 'You are a connection test.', []); $('#aistatus').textContent = 'It answered: ' + (r.text || '(nothing)').slice(0, 80); }
  catch (err) { $('#aistatus').textContent = 'Failed: ' + err.message; }
  finally { btn.disabled = false; }
}

// ---------- Natalie: the user's model, with the WOTR tools attached ----------

const LOCAL_TOOLS = [
  { name: 'set_fields', description: 'Write values into the entry open in the Workshop editor. Pass {fields: {key: value}} using the field keys listed in the system prompt. Lists (traits, releases) take arrays of objects. Only set what the user agreed to or asked you to fill.',
    input_schema: { type: 'object', properties: { fields: { type: 'object' } }, required: ['fields'] } },
  { name: 'read_library', description: "List the user's own library: every entry's id, kind and title.", input_schema: { type: 'object', properties: {} } },
  { name: 'read_entry', description: "Read one of the user's own entries in full by id.", input_schema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } },
];

function natPanel() {
  return `<aside class="nat" aria-label="Natalie">
    <div class="who"><span class="dot" aria-hidden="true"></span><h2>Natalie</h2><span class="hint">on your ${esc(PROVIDERS[ai().provider]?.label || '')}</span></div>
    <div class="log" id="log" aria-live="polite">${S.chat.map(msgHtml).join('') || `<p class="hint">Sketch an idea and she builds it with you: "a Moto swordsman who burns his own blood for speed", "name this technique", "what would this cost". She can fill the fields; you keep what you like.</p>`}</div>
    <label class="sr" for="ask">Message Natalie</label><textarea id="ask" placeholder="Ask Natalie" ${S.busy ? 'disabled' : ''}></textarea>
    <div class="row"><button class="btn primary" id="send" ${S.busy ? 'disabled' : ''}>${S.busy ? 'Working…' : 'Send'}</button></div></aside>`;
}
const msgHtml = (m) => `<div class="msg ${m.who}">${esc(m.text)}</div>`;
function pushMsg(who, text) { S.chat.push({ who, text }); const log = $('#log'); if (log) { log.insertAdjacentHTML('beforeend', msgHtml({ who, text })); log.scrollTop = log.scrollHeight; } }

async function systemPrompt() {
  if (S.natalie == null) S.natalie = (await api('/api/tool/natalie', { method: 'POST', json: {} })).text || '';
  const keys = schema(S.entry.kind).flatMap((s) => s.fields).filter((f) => !f.k.startsWith('_'))
    .map((f) => `- ${f.k}: ${f.label}${f.opts ? ' (one of: ' + f.opts.join(', ') + ')' : ''}${f.type === 'stage' ? ' (a numeral: ' + S.canon.stages.map((s) => s.numeral + ' ' + s.name).join(', ') + ')' : ''}${f.type === 'springs' ? ' (array of Wellspring names)' : ''}${f.sub ? ' (array of {' + f.sub.map((s) => s.k).join(', ') + '})' : ''}`).join('\n');
  return `${S.natalie}\n\n---\n\n# THE WORKSHOP\n\nYou are Natalie inside the WOTR Workshop, designing with ${S.me.name} in their own library. Everything in it is theirs (characters, techniques, items, lore, places, factions); it is not Isaac's table and nothing here becomes table canon by itself. Their choices stick: you propose, they keep.\n\n` +
    `Use the WOTR tools for canon before inventing: skill("wotr-technique") to design an ability, skill("wotr-name") for a name, skill("wotr-npc") for a person, codex for Wellsprings and glyphs, wiki and character for canon people and places, load_rules for the law. The Sixty Wellsprings, the glyphs, the Stages, Families and cultures are fixed and never invented.\n\n` +
    `Answer out of character, plainly and at the length the question needs, unless asked for prose. When they agree to a design, or ask you to fill it in, write it with set_fields.\n\n` +
    `The entry open now is a ${S.entry.kind} titled "${S.entry.title || 'Untitled'}". Its current values:\n${JSON.stringify(S.entry.data, null, 1).slice(0, 12000)}\n\nField keys for set_fields:\n- title: the name\n${keys}`;
}
async function toolList() {
  S.tools ||= await api('/api/tools');
  return [...S.tools.filter((t) => t.name !== 'natalie'), ...LOCAL_TOOLS];
}
async function runTool(name, args) {
  if (name === 'set_fields') {
    const f = args?.fields || {};
    Object.entries(f).forEach(([k, v]) => { if (k === 'title') S.entry.title = String(v); else S.entry.data[k] = v; });
    changed(true); return 'Set: ' + Object.keys(f).join(', ');
  }
  if (name === 'read_library') return JSON.stringify((await api('/api/entries')).map(({ id, kind, title }) => ({ id, kind, title })));
  if (name === 'read_entry') return JSON.stringify(await api(`/api/entries/${encodeURIComponent(args.id)}`));
  return (await api(`/api/tool/${encodeURIComponent(name)}`, { method: 'POST', json: args || {} })).text;
}

// One model call. history is provider-neutral: {role, content} plus tool turns kept in provider shape.
async function llm(history, system, tools) {
  const c = ai(), p = c.provider || 'anthropic', base = (c.base || PROVIDERS[p].base).replace(/\/$/, '');
  if (p === 'anthropic') {
    const r = await fetch(base + '/v1/messages', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': c.key || '',
      'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
      body: JSON.stringify({ model: c.model || PROVIDERS.anthropic.model, max_tokens: 8000, system, messages: history,
        ...(tools.length ? { tools: tools.map((t) => ({ name: t.name, description: t.description.slice(0, 1024), input_schema: t.input_schema })) } : {}) }) });
    const j = await r.json(); if (!r.ok) throw new Error(j.error?.message || r.statusText);
    return { raw: { role: 'assistant', content: j.content }, text: j.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n'),
      calls: j.content.filter((b) => b.type === 'tool_use').map((b) => ({ id: b.id, name: b.name, args: b.input })) };
  }
  const headers = { 'content-type': 'application/json' }; if (c.key) headers.Authorization = 'Bearer ' + c.key;
  const body = { model: c.model, messages: [{ role: 'system', content: system }, ...history] };
  if (tools.length) body.tools = tools.map((t) => ({ type: 'function', function: { name: t.name, description: t.description.slice(0, 1024), parameters: t.input_schema } }));
  const r = await fetch(base + '/chat/completions', { method: 'POST', headers, body: JSON.stringify(body) });
  const j = await r.json(); if (!r.ok) throw new Error(j.error?.message || r.statusText);
  const m = j.choices[0].message;
  return { raw: m, text: m.content || '', calls: (m.tool_calls || []).map((t) => ({ id: t.id, name: t.function.name, args: JSON.parse(t.function.arguments || '{}') })) };
}
function toolResults(calls, outs) {
  return (ai().provider || 'anthropic') === 'anthropic'
    ? [{ role: 'user', content: calls.map((c, i) => ({ type: 'tool_result', tool_use_id: c.id, content: outs[i] })) }]
    : calls.map((c, i) => ({ role: 'tool', tool_call_id: c.id, content: outs[i] }));
}
async function natalieSend() {
  const box = $('#ask'), text = box.value.trim(); if (!text || S.busy) return;
  box.value = ''; pushMsg('user', text);
  S.busy = true; $('#send').disabled = true; $('#send').textContent = 'Working…';
  try {
    const [system, tools] = await Promise.all([systemPrompt(), toolList()]);
    S.convo ||= [];
    S.convo.push({ role: 'user', content: text });
    for (let round = 0; round < 14; round++) {
      const r = await llm(S.convo, system, tools);
      S.convo.push(r.raw);
      if (r.text) pushMsg('nat', r.text);
      if (!r.calls.length) break;
      const outs = [];
      for (const call of r.calls) {
        pushMsg('tool', `⚙ ${call.name}`);
        try { outs.push(String(await runTool(call.name, call.args)).slice(0, 60000)); } catch (err) { outs.push('failed: ' + err.message); }
      }
      S.convo.push(...toolResults(r.calls, outs));
    }
  } catch (err) { pushMsg('err', err.message); }
  finally { S.busy = false; const b = $('#send'); if (b) { b.disabled = false; b.textContent = 'Send'; } }
}
document.addEventListener('keydown', (ev) => { if (ev.target.id === 'ask' && ev.key === 'Enter' && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); natalieSend(); } });

// ---------- router ----------

async function route() {
  const h = location.hash.replace(/^#/, '') || '/';
  const [path] = h.split('?');
  const parts = path.split('/').filter(Boolean);
  try {
    if (!S.canon) S.canon = await fetch('/api/canon').then((r) => r.json());
    if (parts[0] === 'signin') return signin();
    if (!S.me) S.me = await api('/api/me');
    if (parts[0] === 'ai') return aiView();
    if (parts[0] === 'scenes') { nav('scenes'); view().innerHTML = `<p class="kicker">Next</p><h1 class="title">Scene <em>rooms</em></h1><p class="lede">Play with other people here instead of on Discord: your characters, their characters, Natalie on the host's AI. Being built after the designer.</p>`; return; }
    if (parts[0] === 'new' && KIND[parts[1]]) return create(parts[1]);
    if (parts[0] === 'e' && parts[1]) { await editor(parts[1], parts[2]); return fillLinked(); }
    S.entry = null;
    return library();
  } catch (err) {
    if (err.message !== 'sign in') view().innerHTML = `<div class="empty"><b>Something broke</b>${esc(err.message)}</div>`;
  }
}
window.addEventListener('hashchange', () => { route(); view().focus(); });
route();
