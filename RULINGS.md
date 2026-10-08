# Rulings awaiting application to the index

Appended by the wotr MCP server when Isaac rules at the table. Each is applied to rules/*.yaml in Claude Code, then moved to PROGRESS.md.

## 2026-09-12 — canon: Karo Venrik's parentage

Isaac, in Claude Code: "Karo Venrik is the Son of Hiromi Mahuo and the Elven Queen that got checked." Applied: Sandalphon Aestraen's card no longer names him Karo's father; Karo Venrik is the son of Hiromi Mahuo and Saeloria, Queen of Eresse. Applied to the wiki (Sandalphon's lineage flag) and to the conversion brief so the Volume V/VI conversions carry it.

## 2026-09-12, later — four rulings from an AskUserQuestion batch

- **Muken's children.** The wiki's Muken card stands: Sodoku, Sonzai, Emira,
  Tomuka and Ezo (R22-10-MUKEN_CHILDREN_CONTESTED, superseded). The original
  received text's three-heir roster (Temür, Chuluun) and Enkhtuya-as-child
  are not adopted. Note: my own first draft of this ruling misquoted the
  roster as "Tomuka, Chuluun, Ezo, Kuroyuki, Mizuyi," lifted from the base
  guides' stale Büri-era errata note rather than the live card — corrected
  in the rule row before it went anywhere else; the base guides
  (`scenes/THE_KINGDOM_OF_KHARVEN_{buri,corrected}.md`) still need their own
  "Flagged, not resolved" note updated to match.
- **Rengai Zettai's combat assignment** (R1-1-RENGAI_ASSIGNED) ratified as
  pitched, including the post-injury reading: Percussion, the Return,
  post-injury narrows to economy, answers plate by using it.
- **Black Agent's combat assignment** (R1-1-BLACK_AGENT_ASSIGNED) ratified
  as pitched: Blade, unhurried, Absetzen and Durchwechseln, does not engage
  plate.
- **The Law V gate** (R9-1-STILL_OPEN_ITEMS) confirmed at Stage VII, as
  proposed. Still open from that same row: Law III's rewrite, the
  golden-age question, the Latinate/vernacular doublet's scope — none of
  these had enough proposed substance in the sources read so far to put to
  Isaac as real options; need the actual Part Four docket text before
  asking.

## 2026-09-12, still later — seven Stages ratified; strict gates; the re-cost

- **Seven originated Temperance Stages ratified as written** after a
  read-only check of every axis against the Sixteen Stages tables, each
  re-derived by a second reader: Gorrath Bloodspine VIII, Iskaron
  Thalnaris XI (trapped, not passed through), Zarron Mahuo X, Aurevian
  Lysanthir VIII, Juno Petros Marien IX, Kaelen Raive VIII, Saruin Kye
  VIII. Done (4dd7023).
- **Two Catalyst Conditions written** — Kaelen Raive and Saruin Kye had
  the Stage's phenomenology where the Catalyst Condition belongs; each
  gets its contradiction-made-structure and first Domain from the card's
  own history, originated. Done (4dd7023).
- **Path gates are strict** (R38-1): where Part Seven gates a component
  of a merged Sub-Stat on a Path, the whole merged number is capped;
  violating values on existing sheets come down to their caps.
- **Re-cost every originated sheet to the current allotment** (R38-2):
  the Volume III/IV sheets were costed on the pre-cut 20/25/30 per Level;
  Part Three now gives 12/15/18 ("cut by two fifths"). Allocations are
  trimmed to fit, Grade letters re-derived, strict caps applied; the
  Stage ratifications stand. **Parked before running, pending Isaac.**
  The spec and target list were extracted (read-only, from the mirror):
  208 sheets carry a pool line, not ~40 — 202 are on the pre-cut rate
  (145 on Stage×100 Thresholds, 50 on a flat 400 per Threshold, 7 with
  estimated figures), 6 already on the current rate; aggregate overrun
  343,059 points; under strict gates 164 sheets carry 494 peaks above a
  Path cap (best-effort parse). The extraction found six contradictions
  in the canon arithmetic and one structural gap, logged as C-009 to
  C-014 in `CONFLICTS.md`; the gap (C-014) is the one that gates the
  sweep: 125 of the 208 cards compute "Allocated" as Σ Primary values +
  Σ listed peaks, which the Living System forbids (a Primary "is never
  purchased"), so the sweep can only scale the cards' own numbers, not
  make them canon-shaped. Proposed procedure (spec A7): scale every
  listed number by POOL_current / Pool_stated, apply the Stage ceiling
  and strict Path caps, re-derive Grade letters from the value table,
  keep each card's own identity for the verifier; ten invariants.
  Sample, Gorrath Bloodspine (L235 / VIII, Body Path only): pool 9,150 →
  6,930 (k = 0.757); Primaries 542/521/508/470/432/395/358/310 →
  410/395/385/356/327/299/271/235 (S A A A A A B B — two drop a
  bracket); peaks 550→417 … 425→322; Ardency Density 512 → 388 → capped
  to 175 (C) under the strict rule because its inscription component is
  gated on Spirit III and he has no Spirit Path; Allocated 8,899 → 6,529,
  Unspent 251 → 401. Two "at ceiling" claims on his card would need
  rewriting or re-pinning out of Unspent. Also found: Francis Alexander's
  own pool is 400 short of its stated method (Level 470 credited with a
  60-level Band V figure); two Ziyu Pip Inari pages carry the same
  numbers; 60 Primary Grade letters already disagree with the value
  table. Spec: scratchpad `recost_spec.md` / `recost_targets.json`
  (session files; regenerate from the mirror if lost).
- **Guide folds, batch two and three; the lost Item guide.** Done for
  seven guides: Scene Writing Process, Racial Voice and Dialect, Visual
  Aesthetic, Dialogue Craft Standards, AI Writing Tells, Manual
  Verification (base recovered from Downloads), Mass Combat Craft (base
  recovered from Isaac's Google Drive, export formatting normalised,
  content unchanged). Each edition sits beside its untouched base in
  WOTR True Canon with a changelog, judgment calls, flagged gaps and the
  two or three same-day review passes recorded. One tension the Scene
  Writing fold surfaced is logged as C-008 (italic thought per NPC vs.
  a locked narration distance). Drive for Desktop mirrors that folder and
  once re-created the Manual Verification edition from a stale snapshot
  mid-edit; the lost corrections were replayed from the edit log and
  verified. The Item and Equipment Writing Guide survives nowhere;
  Isaac: "you might have to create it" — reconstructed as
  `WOTR_Item_and_Equipment_Writing_Guide (2026-09-12 reconstruction).md`
  from its nine live rules, Pack Seven's description of the original
  (testimony, not law) and the artifact pages' practice, through four
  review passes; its §13 lists what the original held that nothing can
  restore. Done.

## 2026-09-12, still later — C-005 and C-006 closed; five proposals ratified

- **C-005 (Zettari vs. Zettai).** Zettari wins. "Zettai" swept to
  "Zettari" across the wiki and scenes; the three Volume I cards are
  renamed (Rashani, Rengai, Dougou Ozumu Zettari). Rule rows keep their
  verbatim quotes as the sources spell them (Zettai) and note the
  divergence. Done (commit 8d21751).
- **C-006 (the Zettari's register).** The rule gives way: the Zettari's
  established Swahili/Bantu/Arabic-flavoured vocabulary stands and the
  five-strata naming rule is carved out — the Zettari are their own
  register; "archaic bloodlines → Japonic" still governs any other archaic
  line. R32-1-ZETTARI_REGISTER_SWAHILI_BANTU_ARABIC. Done (commit 8d21751).
- **Five proposals ratified wholesale, as written:** the Zettari
  forge-culture pitch (Agano Sand and the Witnessed Temper; R33, after the
  spelling sweep); the Moto bloodline Visual Aesthetic Guide pass
  including the two flagged speculative items, the Tenrai palette and the
  Kurenai crimson/mourning-black contrast (R34-1, R34-2); the
  psychic-distance narration registers for nine POV characters, Hild Ice
  and Dabney left unassigned (R35-1, R35-2); what House Yuno declined to
  disclose to the Research Division — Yasoshima as a 200,000-year Essence
  sink worked by the Kagura branch at real cost to the officiants (R36-1);
  the four element inventories — Mahuo, Yukari, the elven branches,
  Beastkin soul-names — with their open flags kept as flags (R37-1..4).
  Each supersedes the pending row it answers. Done (commits b7c48c0,
  78e4c28).

- **Darius's seat: eleven years.** The scenes are right (the letter at
  thirty-five, Darius fifty-six now); the four wiki pages that said six
  (Sanctum Lux, Stannvaard, Aurelian's and Verinus's cards) now say eleven.
- **C-007 closed.** The psychic-distance axis is "narration distance";
  Pack Five keeps "narration register" for per-culture diction. R35 rows
  retitled.

## 2026-09-12, still later — wiki-wide docket sweep, fifth batch (the researched nine)

Nine items researched read-only first (each with verbatim flags, evidence,
options and a text-backed recommendation), then put to Isaac in three
AskUserQuestion rounds. Rulings:

- **Cymorath.** Cymorath is the Air of Ascent exactly as Fracture of Worlds
  gives it (Fulguria; freedom, motion). The frost/stasis portfolio that the
  struck Codex "Crymorath" carried is re-homed on Vohrin — the Abyssal
  Depths Titan FOW III already names for thermal extraction — Family
  Caloria, Thermodynamics, the route Cryost Ascendant, Mizuki Moto and
  Draven's card already took. Closes the follow-on left open in the first
  batch. R27-1-CYMORATH_AIR_OF_ASCENT_FROST_ON_VOHRIN (commit c86a57d).
- **Verinus's black stones.** An analogue, not Crevice Shale: a distinct
  material made when the Void was completed, which instruments cannot tell
  from Shale at a distance; Article III names Shale and not this, so
  Enforcement can hang people on a misreading (which "he gets the black
  stones wrong on purpose" already sets up). New T8 Material Index row; the
  Shale pages untouched. R28-1-BLACK_STONES_SHALE_ANALOGUE; named Voidfall Stone (commit ece4312).
- **The dawn Sacrament-bond (Verinus/Aurelian).** Anchored on Aurelian's
  soul holding Verinus's name at weight — the Rubric's own definition —
  fixed by declaration inside the rite over his refusal; Fixatio is the
  gloss for why it holds; no release valve.
  R29-1-SACRAMENT_BOND_ANCHOR_BY_DECLARATION (commit 8ee70da).
- **Darius's refusal of the Will of Judger seat.** An intentional mystery,
  codified as withheld: his reason is never given in his own voice; the
  other characters' partial readings stand; nothing pre-empted for a later
  reveal. The Stannvaard gap row stops being re-flagged. Separately noted
  for Isaac: the pages disagree on how long the seat has been refused
  (six vs. eleven years: Sanctum Lux, Stannvaard, Aurelian's and
  Verinus's cards say six; scenes 13 and 14 say eleven, and the scenes'
  arithmetic — the letter at thirty-five, Darius fifty-six now — implies
  eleven) — bookkeeping, not ruled. Done (commit 573b79f).
- **Valen Therosian's office.** High Admiral of the Praetorian March
  stands; "Envoy-Consul to the Old World Powers" was a Trello-title
  mislabel and is dropped. The Praetoria re-home-or-strike flag stays
  open. Done (commit 573b79f).
- **"Utopian Concord" / "the Fall" (Leontes Praevan).** An ordinary Accord
  audit post; "the Fall" is Leontes' private name for the institutional
  failure he watched — undated, no tie to Utopia or the Shattering. His
  note's claims that the terms recur on other sheets and that Cernan is
  "named as exiles of Utopia" were false and are struck. Done (commit
  573b79f).
- **Xanelor Rafminar, remaining §IX.** Stage IX ratified as written; the
  Spirit-Fanged Circle stays, carried unattested; the Covenant of the
  Wildbound Fang is struck (its only definition was Fenriris's followers);
  Rikudoku Moto is the figure already attested twice — Kairen Moto's
  estranged father and the Veil practitioner. Done (commit 335c91c).
- **Obrenkael, remaining §XIII.** Kwon Hae-ryu's EU Reserve is 90,000,000
  (log-linear on Level between Ara Min and Borin, confirmed by the
  Borin→Mu-jin slope), Call Cost ≈ 8,100,000 at 9%; the Codex amendment is
  taken — [Abys] Deep is attested at Oblation and Fluxia
  (R31-1-ABYS_DEEP_ATTESTED_AT_OBLATION_FLUXIA); Uncounted stays a Trait
  and names the Lattice property it alters, never a number; the Bench of
  Attribution hears the Arbitration Division's objection as a Reservation
  pending determination; the Praetoria retcon touches none of it. Done
  (commit d06bd51).
- **The "nineteen orphaned realms".** No list of nineteen ever existed;
  eight names are tagged and all eight are ruled on. The "nineteen" wording
  is retired. Altherion → Inner World, northern rim (Stannvaard's
  placement; this amends this morning's Old World ruling, whose quarter is
  now Eresse, Varūn, Iampu). Varūn → Old World. Braqth and Epprenea →
  Outer World, Southern Pan; the spelling "Epprenea"/"Epprenean" wins over
  Epphrene/Epphrenean. Anguz → Inner World, North (added to the page from
  the Material Index and coin table only). Senoth stays under "Names That
  No Longer Attach to Ground". **Mireya is struck — it does not exist;
  retconned out of all sixteen pages, no replacement place named.**
  **Vellsorea → the New World.** Done (commits 2fd4f2f, b92e887).
  Mireya's strike left six spots leaning on an unnamed place, for Isaac
  to name if he wants: Kaien Veyren's Regency posting (alias now "The
  White Bloom"); Shiran Kazuren's realm ("unstated"); the Well that
  Upanga wa Msimu Nne and Kibanda cha Mwanga wa Miti both cite; Helki's
  "Stillness at the Gate"; Auren's origin realm on The Fractured Dawn;
  the Verdant Alloy's makers.
- **The New World retcon.** Isaac, ruling on Vellsorea: "Place it in the
  New World since we are retconning most of its landmasses and moving
  Eresse to the New World and its kingdoms." Researched read-only first:
  the Korvaeth scenes already stage Eresse in the New World (the Empress
  of Eresse, the Sunroot Court, Velthaeir, the Vaelmarr terraces), so this
  is the wiki catching up to the prose. Ruled in a fourth question round:
  (1) all the elven branches move east — Eresse, Iampu, Rovann, the
  Sylvaar, the Echo Elves; the Old World quarter becomes Varūn and the
  non-elven ground; Ironwood and Glacium retag East. (2) The New World is
  two landmasses: the elven old-ground and the young arc the Accord
  chartered from nothing; the Accord's "no older law" doctrine stays true
  of the arc and is narrowed to say so; the geology page is the arc's
  ledger. (3) The arc, Caedor, Foraye, the coral coast and the Tsohanto
  Reach survive; Nevara is struck (as Valen Therosian's card already
  said). (4) Same polity, same era: Vaelmarr is Saeloria's capital, the
  seat of the Sunroot Court; the Korvaeth arc is Eresse's present; the
  State of Play's "separate calendar" is a dating convention. Cards that
  said "Eresse, Old World" retag to the New World. Scenes untouched. In
  progress (two background agents).

## 2026-09-12, still later — wiki-wide docket sweep, fourth batch

- **Fenriris.** Struck — non-canon, unattested. Xanelor Rafminar's card
  keeps every mechanical beat of the pact (the relief and what follows
  it, the Core and Shell presenting under the pact, the sense of
  something watching through the constructs); the thing he pacted with
  is now written as unnamed rather than replaced with a new name. Done
  (commit de1060c, bundled with the Concordant Crystal commit).
- **Goraku and Daigo Tenryū.** Kin — the card's own recommended reading.
  The Tenryū are a lineage whose Wellspring inheritance is metabolic
  conversion (Goraku: brew and blood-fire through the inherited Oni's
  Pact; Daigo: sweets and rhythm through Sugar Furnace). Degree of
  relation deliberately left unstated. Being written into both Volume
  IV cards.
- **Saekiro Malrake and Jindoku Malrake.** Isaac: "you should delete them
  they no longer exist," confirmed twice on direct follow-up as the two
  characters entirely, not just the Sodoku-descent claim. The "WOTR:
  Chronicles of the Exiles" chapters on Jindoku's card are a legacy
  Trello volume title the conversion pass had already flagged as
  unattested; no scene file in the repo carries either brother, so
  nothing is orphaned. Being executed: both cards, both Notion pages
  (archived, not hard-deleted), the Volume IV index, Moros Pellayne's
  "fourth to max Memorium" cross-reference, and Jindoku's converted
  import file so a future publish run cannot recreate him.
- **Obrenkael's Aperture branch.** Open to origination — no undisclosed
  plan. Kwon Hae-ryu, the Yeol-gol seat, the naming-right structure and
  the proposed generational element *Hae-* stand as written. Being
  written into the card's §XIII.

## 2026-09-12, still later — wiki-wide docket sweep, third batch

- **Obsession/Attraction gate.** Yes, Obsession Force satisfies an
  Attraction Path gate the same way clean Attraction Force does. A
  setting-wide rule, not just Sinclair Mercer's sheet — every corrupted
  practitioner in the setting gets the same treatment. Done:
  R25-1-OBSESSION_SATISFIES_ATTRACTION_GATE (commit 88e2340); Sinclair
  Mercer's three gate-contested sub-stats now read "Gate cleared".
- **Rhyse Calder's Stage.** Stage VII is right; the "S tier"/Band S
  language was aspirational, not mechanical. η corrected from 0.84 (which
  fell in the gap between bands) to 0.80, the top of Band A. Written
  directly into his Volume V card.
- **The Ossuary Choir's shared Soul Crystal.** Write the mechanism — this
  becomes a real, reusable setting-wide rule for how multiple donors can
  share one Crystal, not a one-off exception. Done: the Concordant
  Crystal, R26-1-CONCORDANT_CRYSTAL_MECHANISM, written into the Choir's
  §II (commit de1060c).
- **Aurelian's EU Reserve.** Confirmed final at 2,400,000,000 — no longer
  flagged as an estimate. Written directly into his Volume I card.

## 2026-09-12, still later — wiki-wide docket sweep, second batch

- **The two Old Worlds.** Isaac: adopt the page's own "option two" — rename
  the continent, not the quarter. The Kushara/Great-Houses material gets
  its own page named Kushara (already the material's own name for
  itself); "The Old World — The Western Wearing" stays the actual Old
  World quarter (Eresse, Varūn, Iampu, Altherion). Done — new page wiki/The Bearing and the Holding/Kushara —
  The Land That Remembers Weight.md (commit c08ce38).
- **Muken's descent.** Ratified: born in Nalūn to a Kōkan mother taken by
  a lesser noble house. The First King section gets its paragraph; the
  Origin's opening changes from "looked north" to acknowledge he had
  nowhere else to go. Done (commit f359ba8).
- **Kaalabad spelling.** "Kaalabad" wins (matches his own Volume I card
  title). "Kalaabad" swept to match across 6 locations, including two scene filenames. Done locally (commit f359ba8); the two Notion-side
  pages (the Docket, State of Play — Kwon Mu-jin) still wait on the
  integration being shared with "Information not on WIKI".
- **Raga's delivery-method question.** Spoken, not poured — nothing in
  his entry ever supported a poured mechanism. Kaalabad destroys the
  construct by killing the voice: interrupting Kwon Mu-jin's naming
  mid-word (a struck throat, a broken jaw) rather than attacking Raga
  directly, who cannot be harmed by ordinary means and doesn't need to
  be. Written directly into wiki/Summoned and Bound/Raga · The Divine
  Thunder Bear.md.

## 2026-09-12, still later — wiki-wide docket sweep, first batch

A background agent swept the whole wiki (not just rules/*.yaml) for open
questions flagged directly in page text. Four rulings from the first
batch of findings:

- **Cymorath vs. Crymorath.** One Wellspring, not two. Crymorath was the
  typo; Cymorath is canon. Swept across 16 wiki pages (commit b3967b3).
  Follow-on still open: FOW's Cymorath (Air of Ascent) and the Codex's
  old Crymorath (frost/stasis) turned out to be two unrelated portfolios
  under one name; the frost portfolio is what the Arctic Lion sheet and
  Draven's techniques are built on and is kept, pending a ruling on
  which portfolio Cymorath actually carries.
- **Tyzura / Ashura Tyurkia.** Isaac: "Tyurkia are now all Yukari so
  revert them to that." The Tyurkia lineage label is corrected to Yukari
  wherever it appears (9 files: artifacts, character cards, The Spirit
  Summoning Arts). Done (commit 45f89f8).
- **Stage-naming collisions** (Dominion/Convergence vs. Invocation/
  Realization; a Family misattribution for Psychiken/Mortalis; "Dominion"
  used as a Stage name when it's a stat). Isaac: FOW/Codex names win
  everywhere, sweep the rest. Done (commit 7173fd9).
- **Marrowchalk / phosphate-law jurisdiction.** The Holy Sea of Alabaster
  inherits the Holy See of Lurien's old jurisdiction over southern
  phosphate law, along with everything else it replaced.

## 2026-09-12, later still — backlog batch: voice guide, Sonzai, material culture, naming

- **Sonzai's card (R21-5-SONZAI_PENDING).** Isaac: "Sonzai is not my character
  so I don't need to build him." No card gets written by this project.
- **Racial Voice Guide gaps.** Yes -- draft Fleshshaper Goblin register,
  Winter Eladrin non-verbal convention, and Celestial Host voice. In
  progress (background agent).
- **Moto material culture (R21-5-MATERIAL_CULTURE_PENDING).** Yes -- write
  the Visual Aesthetic Guide pass for the Moto bloodline (crown-line
  pattern, beast-face boss, knotwork belt, fur mantle, court-vs-campaign
  split). In progress (background agent).
- **Celestial Host naming (R20-2-CELESTIAL_HOST_NAMING).** Yes -- do the
  naming pass under the proposed function + rank-suffix + Lawbell-name
  structure. In progress (background agent).

## 2026-09-12, later still — Pack Five's four Section H items ruled

- **Narration authority (R5-H-NARRATION_AUTHORITY_PENDING).** Isaac: judge
  it "based on scene, based on what scenes needed." Martin wins (already
  live via Pack Fifteen); the proposed fixed quarantine (elevated register
  only in documents/mythic strata) is replaced by a per-scene judgment call.
- **Elegiac mode (R5-H-ELEGIAC_MODE_PENDING).** Yes, standing craft law.
- **Per-culture registers (R5-H-CULTURE_REGISTERS_TIMING_PENDING).** Defer
  until a POV in that culture exists; build on demand, not ahead of need.
- **Kharven retroactive pass (R5-H-RETROACTIVE_PENDING).** Forward-only; the
  eight existing scenes stand, no rewrite pass.

## 2026-09-12, later still — Packs Sixteen through Nineteen ratified wholesale

Isaac: ratify them now, wholesale. All 72 rows across Packs Sixteen, Seventeen,
Eighteen and Nineteen moved status: proposed -> live, ratified: "Isaac,
2026-09-12, Claude Code: ratified wholesale" (both per-row and at each
pack's own header). No new live-vs-live contradictions; validate.py passes.

## 2026-09-12, later still — C-003 and C-004 closed

- **C-003.** Twelve wins everywhere, no exceptions (unlike C-001's firearms
  carve-out). R8-11-PROSE_RETAINS_PACK7 superseded.
- **C-004.** Isaac: "I want it to be a japonic island / nation and revert
  back to the Yuno document." Muken's queen's homeland is Yasoshima (House
  Yuno's own island, wiki/The Bearing and the Holding/Yasoshima — The
  Eighty Isles.md), not Wadatsumi/Vāimoana — that whole thread was a
  Polynesian re-skin of the same document. R21-1-AGAMALU_HOMELAND_RULING,
  R21-3-VAIMOANA_GOVERNANCE, R21-3-VAIMOANA_ESSENCE_STABILITY and
  R21-5-ISLAND_NAME_PENDING's "Wadatsumi" all superseded. Swept
  Wadatsumi/Vāimoana → Yasoshima across the two Kingdom of Kharven base
  guides, the Ashen Crown and Reader's Codex wiki pages (live-edited in
  Notion), and the Reader's Codex Drive source. Kept "Manono" as House
  Yuno's own ceremonial seat (the Yasoshima document's own established
  branch) distinct from Ayame's personal lineage tag, Kagura Branch, on
  her Volume I card — both stand, describing different things, rather than
  picking one and losing a real fact either source states.

## 2026-09-12 — canon: the Agamalu retcon on Muken's queen is reversed

Isaac, in Claude Code: "Ayame Yuno over Filemu Agamalu we retconned the Agamalu register." Reverses the Canon Amendment, Agamalu and Büri Origin's central claim (R21-1-QUEEN_OF_KHARVEN_RULING, R21-2-FILEMU_NAME_CORRECTION, R21-2-FILEMU_FULL_NAMING, R21-5-FILEMU_VOICE_PENDING, all marked superseded) that Muken's queen was "Filemu Agamalu" of the Agamalu house (Manono Branch, Vāimoana/Wadatsumi, the Ava-name Le Ie Tuuina Atu, matai title Tausi o le Vā Atoa, the Fusi Vā rite). She is Ayame Yuno again — Yuno Family, Kagura Branch, matai title Zenma no Mamori, Saimei Okurareta Nishiki, the rite named Saishiki — exactly as her own Volume I card (`wiki/Volume I — Character Cards/Ayame Yuno.md`, predating the Canon Amendment) already had her, untouched. Applied: swept "Filemu Agamalu"/"Filemu" back to "Ayame"/"Ayame Yuno" and "Fusi Vā" back to "Saishiki" across scenes/ and wiki/ wherever the Agamalu-register swap had been made (`scenes/THE_KINGDOM_OF_KHARVEN_buri.md`, `scenes/THE_KINGDOM_OF_KHARVEN_corrected.md`, `wiki/The Bearing and the Holding/Yasoshima — The Eighty Isles.md`, `wiki/Sodoku Moto/The Arctic Lion — Sovereign Configuration (Level 500).md`). Left open on the Docket, C-004: whether the Agamalu homeland (Vāimoana/Wadatsumi as a place, its confederation-of-aiga governance, its Essence stability) survives as unrelated worldbuilding now that its only narrative tie to Kharven (the marriage) is gone, or whether that whole thread goes with it.

## 2026-09-13 — the stat-system conflicts C-008 through C-014 closed; two proposals ratified; two pending rows superseded

Isaac, in Claude Code (a questionnaire over every open row; each answer is
his choice among stated options, quoted here as ruled). Rows R39-1 to R39-8
in `rules/doc-stat-system-rulings.yaml` carry them into the index.

- **C-014.** The canon model: points are spent on Sub-Stats only; a Primary
  is the total of its eight Sub-Stats and its Grade is read off the mean.
  The 125 sheets that buy Primaries as a second layer are wrong and are
  re-costed to this shape (the R38-2 re-cost proceeds on the canon model).
- **C-009.** Dominion's mean is the total divided by seven, the seven
  counted Sub-Stats; Throne sits outside both the total and the mean.
- **C-010.** Stage I counts as a Threshold worth 100 points: everyone
  starts with 100 Threshold points, and Part Three's worked totals stand
  exact (2,200 at Level 100 / Stage IV; 9,100 through Stage XIII).
- **C-011.** The Max Grade letter binds: a Sub-Stat may not exceed the top
  of the Stage's Max Grade bracket (Stage V 275, VII 400, IX 550, XI 725);
  the band from there up to the Stage's numeric ceiling is the flagged
  instability zone, reachable only under strain, never by allocation.
- **C-012.** Persistence's Fate gate is Stage VII, as the Four Paths page
  has it; Part Seven's Stage V is corrected to VII.
- **C-013.** The Sub-Stats that reach their true ceiling only through
  Dissonance are Overflow, Overchannel and Persistence (Part Eight and The
  Sixteen Stages agree); Part Sixteen's list is corrected to match.
- **C-008.** The narration-distance rule wins: no NPC italic thought inside
  a locked-POV scene. Pack One's "one private italic thought per named NPC"
  carve-out survives only for scenes with no POV lock (omniscient and mass
  combat).
- **R4-H1-WREN_ASSIGNED, R4-H2-EDWARD_LAMBERT_ASSIGNED.** Ratified as
  written; both go live, and the Combat Guide's pending appendix moves into
  the main assignments table at the next edition.
- **R2-OP-UNFOLDED_GUIDES, R4-OP-PASTE_IN_DIFFS.** Superseded by Isaac's
  direction of 2026-09-12 to fold the packs into dated base-guide editions
  ("yes — start folding the packs in now"); eleven guides are folded, the
  remaining six follow the same way.

Also chosen in the same sitting, not rulings: R9-1's five Four Crafts items
get concrete options drafted from Part Four's docket before he rules; the
Celestial Host naming pass (R20-2) and a Japonic Moto element bank are
drafted as proposals; Pack Twenty — The Clearance gets pack_impact before
extraction; A Reader's Codex is republished (its Notion deletion was an
accident); Darius's card is Isaac's to write in Notion.

## 2026-09-13, later — Pack Twenty extracted; R9-1 closed

Isaac, in Claude Code, on reports/pack_twenty_impact.md: **the later rulings
win, all five** — C-001 (Eleven's ban stands), the Agamalu/Vāimoana block
(reversed), the steppe items (the Northern forms), Muken's children (the card
stands), Taulagi and Afasoa (Yuno retainers). Those rows are extracted as
superseded on arrival, quoted intact (rules/pack-20-twenty.yaml). **R20C-41 to
R20C-47 are his Four Crafts rulings** — Chantcraft the fifth craft; Law V a
Stage gate at Refraction on the working; Law III dead, progression by the
sixteen Stages; Runecraft vs Spellcraft by culture; the Accord mistaken and
lying about the golden age; the doublet at the wider scope; each craft owes
the Inventory an object, an oath and a proverb — which closes
R9-1-STILL_OPEN_ITEMS. Two further collisions found at extraction and
recorded, not resolved: R20C-52 (the Host has no native register) against
R24-3 and R40-2, extracted superseded on arrival because both post-date it;
and the psychic-distance table against R35-2, logged as C-015.

## 2026-09-13, evening — C-016, the Living System pages corrected, two imports resolved

- **C-016.** Fracture of Worlds governs Cymorath's stat effect: Dexterity
  Celerity, Dexterity Burst, Gnosis Cartography. R27-1's "and Perception" was
  a slip; the ruling's own deferral to FOW decides it. Noted on the row.
- **The Living System pages.** The eight stat rulings (R38-1, R38-2, R39-1 to
  R39-6) applied to the canon Notion pages as 25 block edits
  (reports/living_system_edits.md): the canon-model sentence, Stage I as a
  Threshold, the re-cost paragraph, the Max Grade cap and instability zone in
  Part Three, Part Five's opening and its table rows V/VII/IX/XI, the strict
  component gate and Persistence's Stage VII in Part Seven, Part Eight's
  Threshold count, Dominion over seven in Parts Four and Twelve, and Part
  Sixteen's Dissonance trio and Max Grade lines. Mirror refreshed.
- **The Archmagus (Trello import).** Reconciled: her refusal of the Eressean
  crown was a handover; Karo and Asta Venrik hold with her assent. Her Level
  and η carry `derived` markers under R20C-34. Published to Volume V.
- **Precept (Trello import).** The two unattested figures (the named breaker of
  the Precept of Mercy and the lineage name) are struck; the Precept publishes
  without them to The Iridescent Archive / Spellcraft.
- **Three editions written** (WOTR True Canon): The Complete Magic System
  (R25-1, R27-1, R29-1), The Mechanism of the Sixty (R31-1 folded, R27-1
  cross-referenced), the Character Template and Examples (the nine combat
  assignments, R14-8, the R39 stat guidance quoted), each with a changelog and
  two review passes.

## 2026-09-13, late — C-015 closed: distance is two axes

Isaac: **both stand as two axes.** R35-2's narration register says whose idiom
the narration runs in (close, medium, distant/formal); Pack Twenty's
psychic-distance band (1 most distant, 5 deepest interior) says how deep
inside the POV the narration sits. They are read together, never traded off:
Cozbi runs in a distant/formal idiom AND at band 5 — the narration becomes
him, in a formal register. No row struck.

**Correction, later the same evening (C-016).** Part Twelve's Merge Ledger
retires Burst into Celerity and Cartography into Perception, so FOW's Cymorath
entry ("Celerity, Burst, Cartography") and R27-1 ("Celerity and Cartography and
Perception") describe the same two current Sub-Stats — Dexterity Celerity and
Gnosis Perception. The clash was an artefact of retired names; the ruling
"FOW governs" stands and costs nothing. Noted on R27-1 and on the C-016 row.

## 2026-09-13, late — the re-cost applied; three more Pack Twenty collisions found

- **R38-2 re-cost run** (build/recost.py, report reports/recost_2026-09-13_applied.md):
  seven cards stated a lifetime pool on the old allotment — Gorrath, Iskaron,
  Sinclair, Xanelor, Zarron, Ignatius, Karo. Each now carries the current pool
  (12/15/18/21/24 a Level plus Stage × 100, Stage I counting), every listed stat
  scaled by current ÷ stated and capped at the Stage's Max Grade top (R39-4),
  Grade letters re-derived, the pool line and the worked economy rewritten and
  marked. The two-layer shape is kept for verification. Retired Sub-Stat names
  on the cards are scaled, not renamed, and listed with their absorbing entry.
  R38-1's Path gates were not applied: the cards state no Path commitment.
  Xanelor and Ignatius list slightly more than their pool (324 and 46) — the
  sheets' own Allocated lines never counted every listed peak; the Judger's.
- **Found by the Combat Craft Guide's 2026-09-13 edition:** R20C-24, R20C-26
  and R20C-27 contradict Isaac's 2026-09-12 rulings on R13-A, R13-C and
  R13-D. Logged as C-017, C-018, C-019, open; not resolved by the extractor.
- The Combat Craft Guide's 2026-09-13 edition folds Wren and Edward into the
  main table, quotes Pack Twenty's combat rows and the R39/R41 rulings.

- **C-017, C-018, C-019.** Isaac: the later rulings win, all three, as for the
  first five collisions. R20C-24, R20C-26 and R20C-27 go superseded on arrival;
  the R13-A, R13-C and R13-D rulings of 2026-09-12 govern (Joules in anyone's
  diagnostic voice; the working stops shot, not the steel; the gap-fill pass
  may change an outcome and says so). R11-3-AMMO_TIERS reads with R13-C's
  ruling, as its note already says. The Combat Craft Guide's 2026-09-13
  edition quotes the three R20C rows; a note at each is owed in its next pass.
- **Re-cost tail.** Isaac: trim Xanelor's and Ignatius's overages. On a second
  count neither card is over its pool — the first count had double-counted a peak
  listed twice (a table and a callout). Nothing trimmed; their pool lines now
  carry the true Allocated and Unspent (Xanelor 8,082 / 288; Ignatius 13,471 /
  614). Retired Sub-Stat names stay as scaled, not renamed.

## 2026-09-18 — new

Kwon Mu-jin is 38, not 24. Isaac's ruling, 2026-09-18. His children's ages are fixed at Geturo 15, Hiromi 13, Lily 12; Geturo is the eldest and Lily the youngest, which strikes the "Hiromi and Geturo are twins" and "Lily is the older sister at 14" statements in the_great_summoners_morning.md author notes and requires the Geturo/Hiromi build comparison in that scene to be re-cut as an older-brother comparison rather than a twin one. On the card: the Catalyst Event stays at fourteen and Youngest Recorded S-Grade in Accord History survives untouched, being a claim about age at grading; the "ten years since" phrasing becomes twenty-four years. Level 430 at Stage XII now reads as two decades of work after a prodigy's start rather than a prodigy's current output.

Context: Kwon Mu-jin card gave Age 24, which conflicted with the Aetherion Academy archive (the_great_summoners_morning.md, xanelor_* scenes) establishing him as father to Hiromi, Geturo and Lily Mahuo, all Class X students. At 24 he would have fathered the eldest at nine. Surfaced at the table 2026-09-18 during the Class X dorm-assignment post.

## 2026-09-18 — new

Rikudoku Moto is the son of Sodoku Moto and Yoko Mishiro. Isaac's ruling, 2026-09-18. Closes Open Question 3 on the Rikudoku card. Consequences: Yoko goes into a parental slot on both the Rikudoku and Sodoku cards; the Scourge of Hell arc now has a child out of it, conceived when Sodoku was roughly 22, which sits inside the period Sodoku's card describes as the Yoko relationship "unnamed by him for the same reason it is unnamed by her"; Emira Moto remains Rikudoku's aunt on the paternal side; Hild Ice is his half-sister through Freya. Left open and flagged, not invented: what Rikudoku expresses of the Mishiro Fox-Spirit Beastkin line, since his only archived description (xanelor_rikudoku_and_the_address.md) is entirely Moto — Moto-dark skin, flat Moto-white hair with black tips, no beastkin feature described. Assigned to Isaac.

Context: Rikudoku Moto's card carried "Mother: unestablished" and "Who is his mother?" as Open Question 3; no archived scene named her. Raised at the table 2026-09-18.

## 2026-09-21 — R19-2-FIXED_TEXT

When Isaac asks Natalie to "make this better / improve it" on an RP post, his dialogue is in scope and gets improved automatically (voice, rhythm, realism per R19-4), keeping each line's meaning and intent and his prosodic notation (capitals, ellipses) per R19-3. R19-2 fixed-text still governs scene work where he submits dialogue to be set.

Context: 2026-09-21, Class X tournament post (Xanelor / Hiromi / Mu-jin). Isaac: "you didn't automatically fix the dialogue" after Natalie set it verbatim under R19-2.

## 2026-09-22 — new

Juggernaut's Fist (Hiromi Mahuo): any contact counts as a landed strike, including a blow that is parried or blocked. Each contact deepens a gravity well (aetheric pressure raising air pressure and local pull) on the struck body. Isaac's ruling, shown in play 2026-09-22. The technique still needs a card entry with Cost, Limit and Counter; the demonstrated counter is that the imposed weight is only force and a skilled opponent can spend it as leverage.

Context: Raised in xanelor_juggernauts_fist, where Xanelor's parry held but his forearm still grew heavier; answered by Isaac in xanelor_the_arrow, where Xanelor deliberately takes the fists on his forearms and each one adds weight.

## 2026-09-23 — the Magic System conflicts C-020 through C-029 closed; Tiers 8 and 9 renamed

Isaac, in Claude Code (a questionnaire over every open row; each answer is
his choice among stated options, quoted here as ruled). Rows R42-1 to R42-11
in `rules/doc-magic-system-rulings-2026-09-23.yaml` carry them into the index.

- **Tier names.** The Tiers of Standing are Initiate, Apprentice, Journeyman,
  Adept, Expert, Master, Grandmaster, Archmaster, Paragon; Tier 8 is no
  longer "Absolute" and Tier 9 no longer "Chosen" (the title Chosen of the
  Codex stands). Tier Grades remain lettered F through SSS, X, EX, EX+.
- **C-020.** Aether Class emerges at Stage VI, Glory. Stages I–V are
  unclassed: the coil reads no Class, and Class Ø stays the sealed
  pre-Initiate Shell. Glory is Class I Muridic; Refraction is Class II
  Harmonic early and Class III Resonant late; Class V Radiant stays at
  Transcendence; everything above is unchanged.
- **C-021.** The Awakened Crystal spans Stages I–IV, Initiate through Adept;
  the Harmonic Crystal begins at Stage V.
- **C-022.** There are three Crystal States: Fractured, Refined, Overgrown.
  Crystallized is not a State; self-as-law belongs to the Crystallized Soul
  tier alone.
- **C-023.** The Ascension Ration serves the III to IV Threshold: it is held
  at Ascension and buys Flourishing's quantitative floor.
- **C-024.** The Domain Seed Vitrifier is Class IV, reserved, like the
  Refraction Draught.
- **C-025.** There are four Paths: Body, Spirit, Attraction and Fate.
- **C-026.** Paragons exceed Level 500. At Stages XV–XVI Level keeps
  rising past 500 with no ceiling and no sixth Band; the Codex does not
  number it.
- **C-027.** Dominion's Stability is renamed Gravity; Harmonics keeps
  Stability.
- **C-028.** The Accord cannot hang a kingdom's subject, but it executes its
  own sworn members under the Codex, through the Tribunal Marshals, and in
  the New World it is the law.
- **C-029.** Closed by the existing C-013 ruling of 2026-09-13: the
  Sub-Stats that reach their true ceiling only through Dissonance are
  Overflow, Overchannel and Persistence.

## 2026-09-23, later — four follow-ups from the same questionnaire

Isaac, in Claude Code, answering the questions the card pass raised. Rows
R42-12 to R42-15 in `rules/doc-magic-system-rulings-2026-09-23.yaml`.

- **Class and Stage.** The Class ladder is the typical path, not a lock:
  a card whose Class sits above the ladder for its Stage stands, and the
  Luminous and Voidic Classes stay lateral. The 26 Stage VI–VII cards that
  disagree with the ladder are unchanged.
- **Crystal State field.** A Crystal tier word written in a card's Crystal
  State field moves to Crystal Tier, and Crystal State becomes null; a
  Stage IV card reading Harmonic is corrected to Awakened.
- **Via Fati.** Viaforma gains a fourth Via, Via Fati, for the Fate Path,
  described from The Four Paths' Fate section only.
- **Kinjiki.** Stage XIV is Tier 8, Archmaster; the card is corrected from
  Paragon.

## 2026-09-24 — new

Isaac 2026-09-24: (1) Rovhen Talvasciel is retconned. The old Volume I card 'The Prettier' (Avian Crimsoncrest surgeon villain) is superseded; Rovhen is now a human retired private magical investigator, 28, former assistant to Edmund Lambert, new instructor at Aetherion Academy teaching the observation and investigation of magical phenomena. Old card to be rewritten or archived. (2) Edmund Lambert is a separate character from Edward Lambert and a member of the Lambert family; exact relation unset. Edmund is dead; Rovhen was his assistant.

Context: Aetherion Academy thread, scene 'The Sort'. Old card 'Rovhen Talvasciel · The Prettier' (Volume I) collided with Isaac's new investigator. Canon has Edward Lambert 'The Arithmetic' (alive, Hild's right hand).

## 2026-09-24 — R12-3-DESIGN_CHAIN_RETURNS

Confirmed and extended to every document: character cards, technique and ability entries, items, lore, in-world documents and exports are fully metaphysical. Stats, Sub-Stats, Grades, Bands, Stage, EU, AU/s, eta, Crystal State, Category, the full Design Chain and mechanism explanation all print on the page. The 24 Sept brief line 'the Design Chain never appears / no mechanism explanation, no metaphysical units' is withdrawn. Never-invent-numbers still holds: empty fields stay flagged pending.

Context: Session 24 Sept 2026, building the wotr-docs skill. Isaac reversed his own brief that kept the Design Chain and mechanism off document pages.

## 2026-09-24 — new

Full-knowledge, fair-play rule. Natalie draws on everything that exists in WOTR (cards, Stat Sheet, FOW, Codex, wiki, scenes, rulings, meta and system knowledge) when writing characters and prose. Knowledge is accessible, including meta knowledge, but is never used to outrageous advantage: NPCs and opponents fight with what they could plausibly know and do, abilities stay grounded in real physics principles, and every engagement is built to be fun and a genuine challenge for the PC, never rigged in either direction.

Context: Session 24 Sept 2026. Isaac's standing direction for how Natalie writes characters and prose generally.

## 2026-09-24 — new

Mechanism and Effect are one thing. The Effect of a working is its mechanism playing out: what happens is written as how it happens (the glyph moves a boundary, the law does what it does, and that is what the target sees and feels). No Effect line that could be true of a different mechanism, and no Mechanism line that leaves the Effect to be described separately. Isaac's words: "the mechanism in the effect should be the SAME thing the Mechanism is the Effect or how it works". Applies to technique and ability entries, cards, sheets, the system accounts (WAR-3..7) and in-world documents.

Context: Session 24 Sept 2026, during the system-accounts pass (Paperclip WAR-3..7). The Technique entry format in .claude/skills/wotr-write/references/technique-design.md and 63 Technique/Spellcraft wiki pages carry separate **Effect** and **Mechanism** fields.
## 2026-09-24 — the four remaining Magic System items closed; C-030 through C-033

Isaac, in Claude Code (the WAR-2 questionnaire, one question per item; each
answer is his choice among stated options, quoted here as ruled). Rows R43-1
to R43-4 in `rules/doc-magic-system-rulings-2026-09-24.yaml` carry them into
the index.

- **C-030.** Ryuka Yukari's Crystal State becomes null and his Crystal Tier is
  Awakened Crystal; the phrase "Dormant network, awakening surface" leaves the
  card entirely.
- **C-031.** Kinjiki's η is ~1.2, the Archmaster ceiling, and his Crystal Tier
  stays Absolute Crystal, the pairing Class Ω carries.
- **C-032.** The Color of Essence's Revelation cell is restored to its own
  sentence and the block pasted inside it is lifted out as "Part Five · Prose
  Application" after Part Four, the same words re-homed; Limina's absence is
  left visible as a gap rather than papered over.
- **C-033.** The retired lettered Coherence Band is replaced, wherever it
  survives outside the Magic System pages, by the Tier of Standing for the
  page's Stage, and η is kept as written.

Context: the four items left open by the 2026-09-23 Magic System pass
(`CONTINUE.md`, that block). Evidence and options were put to Isaac as one
questionnaire; C-033's sweep was held until C-030 and C-031 were answered,
because it walks past both η figures on its way through.

## 2026-09-24 — R8-16-PHYSICAL_NUMBERS_ONLY

Superseded; mark struck in the index along with R8-12-SHEET_GETS_OPERATIONAL_ACCOUNT's clause "the Design Chain remains workbook". Grounds: R20C-39 (Pack Eight Section One superseded), R12-1-NUMBER_BAN_STRUCK, and Isaac's 24 Sept ruling that documents are fully metaphysical (logged on R12-3). The technique card on documents is R17-3's six-line card with the Design Chain below it (R12-3-CARD_PLUS_CHAIN).

Context: Found 24 Sept 2026 while checking the index for the documents ruling. R20C-39 superseded Pack Eight Section One, but these two rows are still marked live and are why the "no Design Chain / no units on documents" restriction kept resurfacing.

## 2026-09-25 — new

Isaac's rules for ruling (the precedence ladder's general rungs), answered in Claude Code on Doc Kett's WAR-61 questions. Agents apply these before the agent ladder in the wotr-conflict skill.

1. **A ruling's general sentence governs.** Where a ruling answers a narrow question but its operative sentence is written generally, the sentence applies to every case it describes (e.g. R44-5: "the card's η governs per character and the tables are typical ranges" reaches every card, not only the three Stage VI cards it was asked about).
2. **Off-ladder runs both ways.** A ruling that lets a card sit above a ladder (η above its range, Aether Class above its Stage) equally lets it sit below; the card governs (e.g. Aethryn η 0.22; Ambrose Virellith Class III at Stage VIII).
3. **Stale status notes are bookkeeping.** A line in canon that states the state of the record ("Veyran is unattested", "the efficiency conflict, unresolved") and that the record has since overtaken may be updated by any sweep, citing what overtook it; no ruling needed.
4. **A ruling's fallback for one column of a table reaches the whole table** (e.g. R44-3's Sub-Stat ranking reaches the travel-speed column of the Part Four Grade table).
5. **Figure against gloss: the bigger is intended.** Where a stated figure and its gloss on the same line disagree (e.g. "4.184 EJ … 1 Tt TNT-equivalent"), keep whichever makes the working stronger, checked against the technique's Stage band, and correct the other to match.
6. **Book against card: the card for numbers, the book for events.** Stats and mechanics follow the character's card; what happens in the story follows the book's bible and chapters.
7. **Authorship questions are the agents' to decide.** Where an item asks to confirm or flip originated material (e.g. "Did she say it … Confirm or flip", scenes/01_the_vacancy_korvaeth_arc.md:754), the agents choose the reading that best fits the rest of canon and ship it as agent-made canon, logged, which Isaac may overturn.

Context: Doc Kett's WAR-61 comment (2026-09-25): of the thirteen WAR-62 docket items, two were settled by the written text and eleven needed a rung that did not exist; these seven answers supply them. Closes on their own: WAR-39, WAR-40, WAR-43, WAR-44, WAR-47, C-038 (WAR-49), C-039, WAR-50; WAR-53/58 (authorship) go to the agents.

## 2026-09-25 — R44-1-EU_JOULE_ONE_MEGAJOULE

**C-034 — what turns EU into joules.** Isaac ruled this directly on the Paperclip board on 2026-09-25, answering the WAR-11 questionnaire card "The Essence Ledger — rulings needed". He chose option (a) of the call "C-034 — What turns EU into joules?" and wrote no words of his own, so the ruling is the option exactly as it was put to him:

> **One constant, 1 EU = 1 MJ stands; the cards that miss are the error** — The Ledger converts at 1 MJ everywhere. 137 of 165 attested figures then sit outside their Stage's band and each becomes a card correction — a follow-up issue, not this one.

Recorded as one sentence, and this sentence is what the index row quotes:

> One constant: 1 EU = 1 MJ stands. The Ledger converts at 1 MJ everywhere, and the card figures that then sit outside their Stage's band are the error; each is a card correction in its own issue, not in this ruling batch.

No card figure is changed by this ruling. `imports/essence-ledger/physics-check.md` (WAR-10) reports that this constant fails against real physics; the ruling is later than that report and is recorded as made.

Context: Logged under WAR-96 by Doc Kett, the Canon Clerk, who owns the batch; WAR-72 found that the entry the index rows quote did not exist. Isaac's answer is Paperclip interaction 364556db-a75a-4e23-ab6a-cc9541ecdbcb on WAR-11 (idempotency key war11:essence-ledger-questionnaire:v1), kind ask_user_questions, resolver policy human_only, status answered, resolved 2026-09-25T17:59:14Z; the six answers were a, a, c, a, a, a. Closes CONFLICTS.md C-034. Index row: R44-1-EU_JOULE_ONE_MEGAJOULE in rules/doc-essence-ledger-rulings-2026-09-25.yaml.

## 2026-09-25 — R44-2-AU_FORMULA_GOVERNS

**C-035 — the AU/s formula against the card figures.** Isaac ruled this directly on the Paperclip board on 2026-09-25, answering the WAR-11 questionnaire card "The Essence Ledger — rulings needed". He chose option (a) of the call "C-035 — AU/s = Flux Density x eta fails on 26 of the 29 cards that state all three. Which side gives way?" and wrote no words of his own, so the ruling is the option exactly as it was put to him:

> **The formula governs; the card AU/s figures are the error** — 26 card figures get recomputed, in a follow-up issue with its own commit. Never in this issue.

Recorded as one sentence, and this sentence is what the index row quotes:

> The formula governs: AU/s = Flux Density × η. The stated card AU/s figures are the error, and the twenty-six that miss are recomputed in their own issue, not in this ruling batch.

No card figure is changed by this ruling.

Context: Logged under WAR-96 by Doc Kett, the Canon Clerk, who owns the batch; WAR-48 found that the entry the index row quotes did not exist and withheld its sweep for that reason. Isaac's answer is Paperclip interaction 364556db-a75a-4e23-ab6a-cc9541ecdbcb on WAR-11, status answered, resolved 2026-09-25T17:59:14Z. Closes CONFLICTS.md C-035. Index row: R44-2-AU_FORMULA_GOVERNS in rules/doc-essence-ledger-rulings-2026-09-25.yaml. The card-by-card table is imports/essence-ledger/fit.json, formula_check.

## 2026-09-25 — R44-3-S_SS_GAP_RANKED_BY_SUBSTAT

**C-036 — the S/SS energy gap in the Part Four Grade table.** Isaac ruled this directly on the Paperclip board on 2026-09-25, answering the WAR-11 questionnaire card "The Essence Ledger — rulings needed". He chose option (c) of the call "C-036 — the Part Four Grade table leaves 2.42672e13 to 4.184e13 J in no Grade at all. How does it close?" and wrote no words of his own, so the ruling is the option exactly as it was put to him:

> **The gap is deliberate — grade that range by the Sub-Stat column** — The table stands exactly as written; an output between 24.3 and 41.8 TJ is ranked by Sub-Stat, not by joules.

Recorded as one sentence, and this sentence is what the index row quotes:

> The gap is deliberate. The Part Four Grade table stands exactly as written, and an attack output between 2.42672×10¹³ and 4.184×10¹³ J — 24.3 to 41.8 TJ — is ranked by the Sub-Stat column, not by joules.

No cell changes. The three tables that carry the same break — FoW II:35-36, FoW III:41-42 and Tier Grade, Bands & the Aether Shell :60-61 — all stand as written.

Context: Logged under WAR-96 by Doc Kett, the Canon Clerk, who owns the batch; WAR-72 found that the entry the index rows quote did not exist. Isaac's answer is Paperclip interaction 364556db-a75a-4e23-ab6a-cc9541ecdbcb on WAR-11, status answered, resolved 2026-09-25T17:59:14Z. Closes CONFLICTS.md C-036. Index row: R44-3-S_SS_GAP_RANKED_BY_SUBSTAT in rules/doc-essence-ledger-rulings-2026-09-25.yaml. C-038, the same shape in the travel-speed column, is not named by this ruling and stays open.

## 2026-09-25 — R44-4-ETA_PART_SEVENTEEN_GOVERNS

**C-037 — the efficiency conflict, Class I Muridic against Tier 5 Expert.** Isaac ruled this directly on the Paperclip board on 2026-09-25, answering the WAR-11 questionnaire card "The Essence Ledger — rulings needed". He chose option (a) of the call "C-037 — the eta conflict: Class I Muridic 0.60-0.70 against Tier 5 Expert 0.50-0.60. Which governs?" and wrote no words of his own, so the ruling is the option exactly as it was put to him:

> **Part Seventeen governs — eta reads 0.60-0.70 at Stage VI-VII** — Part Nineteen's Tier 5 row is corrected to match.

Recorded as one sentence, and this sentence is what the index row quotes:

> Part Seventeen governs: η reads 0.60 to 0.70 at Stage VI–VII. Part Nineteen's Tier 5 row is corrected to match.

The page edit it names is the η cell of the Tier 5 · Expert row in "VII. Aether Class, Essence Typology, Aether Flow (Parts Seventeen–Nineteen)", 0.50–0.60 to 0.60–0.70, and nothing else on that row or any other. The ruling does not name the same page's own unresolved-conflict callout at mirror line 103, so that wording is left exactly as written.

Context: Logged under WAR-96 by Doc Kett, the Canon Clerk, who owns the batch; WAR-72 found that the entry the index rows quote did not exist. Isaac's answer is Paperclip interaction 364556db-a75a-4e23-ab6a-cc9541ecdbcb on WAR-11, status answered, resolved 2026-09-25T17:59:14Z. Closes CONFLICTS.md C-037. Index row: R44-4-ETA_PART_SEVENTEEN_GOVERNS in rules/doc-essence-ledger-rulings-2026-09-25.yaml. The owed page edit is recorded in reports/essence_ledger_rulings_2026-09-25.md and goes to Notion, returning through the hourly sync.

## 2026-09-25 — R44-5-CARD_ETA_GOVERNS_PER_CHARACTER

**The Stage VI cards whose η sits above both candidate ranges.** Isaac ruled this directly on the Paperclip board on 2026-09-25, answering the WAR-11 questionnaire card "The Essence Ledger — rulings needed". He chose option (a) of the call "Not in Phase 1's rows — the Stage VI cards state eta above BOTH candidate ranges. Does the C-037 ruling reach them?" and wrote no words of his own, so the ruling is the option exactly as it was put to him:

> **The card's eta governs per character; the tables are typical ranges** — Nothing changes. An in-world-acknowledged outlier is lawful.

Recorded as one sentence, and this sentence is what the index row quotes:

> The card's η governs per character and the tables are typical ranges; an in-world-acknowledged outlier is lawful. Sodoku Moto's 0.84, Rashani Zettari's 0.81 and Naiser Yukari's figure stand as written.

The three cards are the ones the call was put on: Sodoku Moto.md:43 (0.84), Rashani Zettari.md:29 (0.81) and Naiser Yukari, all Stage VI. Nothing is edited.

Context: Logged under WAR-96 by Doc Kett, the Canon Clerk, who owns the batch; WAR-72 found that the entry the index rows quote did not exist. Isaac's answer is Paperclip interaction 364556db-a75a-4e23-ab6a-cc9541ecdbcb on WAR-11, status answered, resolved 2026-09-25T17:59:14Z. Not a CONFLICTS.md row; raised on the WAR-11 card because the three Stage VI cards state an η above both candidate ranges in C-037. Index row: R44-5-CARD_ETA_GOVERNS_PER_CHARACTER in rules/doc-essence-ledger-rulings-2026-09-25.yaml. Reads alongside R42-12, which held the Class ladder to be the typical path rather than a lock.

## 2026-09-25 — R44-6-BARE_BAND_V_IS_LEVEL_BAND

**The bare "Band V" reading.** Isaac ruled this directly on the Paperclip board on 2026-09-25, answering the WAR-11 questionnaire card "The Essence Ledger — rulings needed". He chose option (a) of the call "Not in Phase 1's rows — the 'stale Band' item. Phase 1 read Raga's 'a fifth of a Band V reserve' as the live Level Band, not the retired Coherence Band. Confirm or correct?" and wrote no words of his own, so the ruling is the option exactly as it was put to him:

> **Confirmed — Level Bands, live; nothing changes** — The brief's "stale Band" item closes with no edit.

Recorded as one sentence, and this sentence is what the index row quotes:

> Confirmed: the bare "Band V" on Raga's and Verinus VII's cards is the live Level Band, and nothing changes. The brief's "stale Band" item closes with no edit.

The two lines the item names, quoted on the WAR-11 questionnaire comment the card was posted with, are `Summoned and Bound/Raga · The Divine Thunder Bear.md:81` ("roughly a fifth of a Band V reserve") and `Volume I — Character Cards/Verinus VII · The Palatine.md:86` ("low for Band V and low deliberately"). Nothing is edited.

Context: Logged under WAR-96 by Doc Kett, the Canon Clerk, who owns the batch; WAR-72 found that the entry the index rows quote did not exist. Isaac's answer is Paperclip interaction 364556db-a75a-4e23-ab6a-cc9541ecdbcb on WAR-11, status answered, resolved 2026-09-25T17:59:14Z. Not a CONFLICTS.md row; a reading Phase 1 made and logged no conflict over, put to Isaac because it was a reading. Index row: R44-6-BARE_BAND_V_IS_LEVEL_BAND in rules/doc-essence-ledger-rulings-2026-09-25.yaml. Confirms that R43-4's sweep of the retired lettered Coherence Band does not reach these two lines.

## 2026-09-25 — WAR-70 (R44-1 corrections)

A card EU figure that R44-1 (1 EU = 1 MJ) puts outside its Stage's band is corrected by moving it to a set point in that band, so every correction is arithmetic off Part Four. The set point is the band's midpoint in decades (the geometric mean of floor and ceiling, in joules, divided by 1 MJ). Isaac chose option 1 of WAR-70 ("1"); the choice of midpoint over floor within option 1 was made by the session relaying it, on his standing direction to make the calls, and he can change it. Figures on C-040's cards (the twelve whose Strike Force does not sit in their Stage's band) are corrected the same way; C-040 itself stays as ruled.

Context: Paperclip WAR-70, filed from WAR-46's sweep (`reports/eu_band_sweep_2026-09-25.md`: 130 of 155 banded EU figures miss, 124 below, 6 above). Answered in Claude Code chat 2026-09-25, Isaac: "1".

## 2026-09-25 — C-059 (WAR-127; amends WAR-70)

WAR-70's set point applies to a card's EU reserve only. Each card whose reserve R44-1 puts outside its Stage's band is scaled by one factor: factor = (band midpoint in decades, the geometric mean of floor and ceiling joules / 1 MJ) / (the card's stated reserve). Every other EU figure on that card (technique, Form and working costs, per-use figures) is multiplied by the same factor, so each cost keeps its stated share of the reserve and distinct figures stay distinct. Flux Density, AU/s and eta stand as written. A card with no stated reserve is not scaled by this ruling and is logged. The four cards already corrected under WAR-70 are re-checked against this rule.

Context: Isaac, 2026-09-25 in Claude Code, "lets do that", accepting the proposal in answer to WAR-46's report that one midpoint per band collapsed distinct figures on ~99 misses (Dougou Ozumu Zettari's thirteen figures, 2,800 to 92,000 EU, all to 2.278e19). Worked example: Dougou's reserve to ~2.3e19 EU; a 7,400 EU Form stays ~8% of it.

## 2026-09-26 — the queue questionnaire (57 answers, Claude Code chat)

Isaac answered, in Claude Code chat, every question for him that sat in the docket queue. Each line names the issue it answers.

- **WAR-15** — Number wins: Gimbzo XII Emanation (SSS, Grandmaster); Naevra IX, Naiser VI, Niran VII take the correct names for their numbers. The four earlier 'name wins' fixes stand as they are.
- **WAR-65** — Follow Ryuka: the tier word comes off the Crystal State field; a Crystal Tier field is written from the Stage (or Aether Class where no Stage). Akira: Dormant.
- **WAR-66** — Stage decides: Aelum's Crystal Tier is Sovereign; applies to all later Class/Stage mismatches.
- **WAR-102** — Gimbzo: correct output to Flux Density x eta (8.6 million AU/s) AND scale every Work cost on his card down by the same factor so cast times stay the same.
- **WAR-102** — Dougou: leave the split output as written (3,900 AU/s external, internal immeasurable); the formula only corrects a single whole-output figure.
- **WAR-102,WAR-139** — Estimates yes, legacy no: Borin and Yoko are corrected and keep their estimate marker; Ignatius's and Karo's legacy-sheet figures stay as a record of the old sheet.
- **WAR-139** — Krothar: the reserve is the suppressed 1.6 million; the 2.8 million unsuppressed figure is scaled by the same factor.
- **WAR-102,WAR-141** — Decimals: write figures exactly as computed, with the decimal (Naori 147.9 EU, Artemis 1,663.2 AU/s, etc.).
- **WAR-102** — Keep the card's form: Elion's output becomes the range 6.768-7.332 million AU/s; Sodoku's line becomes '~772.8 base'.
- **WAR-137** — The copy follows: the Tier 5 cell on 'Tier Grade, Bands & the Aether Shell' becomes 0.60-0.70 and its stale unresolved note is updated; both pages agree.
- **WAR-138,WAR-151** — Follow the table: cards that quote the Tier table's eta read whatever the table says for their Stage (0.60-0.70 at VI-VII now); Yoko's output/flux recomputed to stay consistent.
- **WAR-140** — Leave them: the rescale applies to out-of-band reserves only; the 33 costs on cards with in-band reserves stand as written. (Note: the new job to price costs as a fraction of reserve may revisit them.)
- **WAR-142** — Unmeasured from Zenith: Stage XV keeps its EX+ Grade label, but its force is unmeasured like Zenith's; the Zenith row sits beside the Grade ladder, not on it.
- **WAR-145** — Card governs: Drakvor ~0.55 (and 'above 0.8 inside tuned bastions') and Francis 0.93 stand as their own figures.
- **WAR-155** — Re-derive from cost: each joule/newton gloss is recomputed from the scaled EU cost at Dougou's efficiency, and the Grade wording is fixed to his Stage.
- **WAR-49,WAR-62** — Card figure governs: each of the twelve Strike Force figures stands as that character's own outlier; no card changes.
- **WAR-69** — Riku is born before the book (about seven during it); Yoko is a mother on its pages; the Revolution of the Inner World birth-night scene is rewritten or redated.
- **WAR-69,WAR-50** — Yoko's card describes a later time: the cabin, Riku and the second child come after the book; the card gets a 'when' marker and the book keeps her beside Sodoku.
- **WAR-50** — Ground burial is Kharven-Seat's own city rite; the wider Four Quarters faith keeps sky burial; the faith page gains a line saying so.
- **WAR-50** — It is the Bench of Attribution with its remit unchanged; later chapters may not have it keep or compel records of signings.
- **WAR-64** — Two cuts: Tally cut his own section; Qiu Yinzhi cut and sealed the exhibit wedge herself; notes saying Tally cut the exhibit are corrected.
- **WAR-105** — They first meet at the north gate; the infancy clause in True King part 17 is cut; Hild's card row is updated to after the reunion.
- **WAR-109** — Sodoku 28, Hild 11 at the muster: Sodoku's card moves to 28; the nineteen-year lines become eleven or twelve; The Fixed End's standing-wave passage is rewritten to fit.
- **WAR-110** — Fern Stark is Hild's mother; Freya is a different woman Sodoku lost; the 18 September ruling line is corrected to Fern.
- **WAR-111** — Both: the Greymane ridge guards the west while Bram commands the southern approach; both cards say so explicitly.
- **WAR-114** — Card headers describe the character at a stated moment (e.g. 'as of the muster') and say so; Lore records later events including deaths. Applies to every card.
- **WAR-118** — Kharven's besiegers are the Iron Mandate: 'Expanse' is corrected to the Mandate across the archive, and the Kharven lorebook's cold peace is updated to the nine-year war.
- **WAR-33,WAR-34** — The prose checker stops at the author-notes heading; notes are not measured.
- **WAR-33** — Fix all: lines 13 and 479 lose 'the moment'; one short sentence is broken out of each long chain and flat run; 'A silence held past a nine-count' stays as register.
- **WAR-34** — Break the middle sentence at 'and the figure was the lowest ever entered against a Palatine's name'.
- **WAR-34** — Verinus VII's card states that his register carries set-piece speeches of this length; the scene is untouched.
- **WAR-53** — Two women: Onawa, Empress of Eresse gets her own card; Onawa Ashkewe, Queen of the Tsohanto, stands; the Tsohanto Reach's eleven-year silence becomes her people's answer to the shared name.
- **WAR-58** — The Sacrament cell stays under the Grand Church in Altherion; the scene stands.
- **WAR-58** — Conjunction stays unnamed: the Sacrament's third Wellspring stays out of the prose until decided.
- **WAR-91** — No POV without a register: Bram Greymane and Lorn Stark get registers.
- **WAR-91** — A register stays with the point of view: in another character's viewpoint Sodoku is read by that narrator's rules.
- **WAR-91** — A later scene can pay The Muster's aftermath: a named later scene covering two of the five aftermath stages discharges it.
- **WAR-91** — Stone-Blood cold latency is a rule: Stone-Blood slow (about three-quarters of a beat late) in deep cold, canon for every such fight; the paragraph stays.
- **WAR-91** — Strike the four horizontal rules and four section headings from The Muster; the prose carries place changes.
- **WAR-91** — A scene in four places with one mass-combat section is measured as a set piece.
- **WAR-91** — The viewpoint-ignorance rule counts per scene: one instance anywhere in a multi-viewpoint scene satisfies it.
- **WAR-92** — Yes: mass-combat scenes keep the one-thought-per-NPC allowance even when POV-locked; Robin Ice's italic thought stays.
- **WAR-92** — Yes: mass-combat scenes must still carry duel-level wound anatomy.
- **WAR-92** — Yes: inside a close register the faculty (Reigan) may be the grammatical subject; the three sentences stay.
- **WAR-92** — Reigan's reach is four hundred miles: the scene's figure, with its blindness and eleven-second cost, goes on Sodoku's card and the wiki is widened.
- **WAR-92** — Yes, Wren dies: Sodoku's prediction binds; Wren is dead from What the Sky Does Not Ask on, and later pages must agree.
- **WAR-92** — Draft the Moto narration register from the scene's actual prose and add it to the register list.
- **WAR-49** — Rewrite the stale callout on the Parts Seventeen-Nineteen page as one plain settled line: Part Seventeen's scale (0.60-0.70) governs.
- **WAR-98** — Both forms are real: Mahou is the line as an institution, Mahuo the surname a person bears; the Mahuo Family page states the distinction; future documents follow the Accord's usage.
- **WAR-99** — Zarron Mahuo is retconned: removed from canon. His card is struck and every page that cites him is cleaned (Mahuo Family roster, rulings references, scenes).
- **WAR-134** — Keep Mach 8: Kinjiki's Travel Speed (Mach 8 sustained, Mach 15 bursts) stands as a personal outlier at Zenith.
- **WAR-146** — Yes: a blend's Family may differ from its Wellsprings' Families; both Alchemical Index rows stand as drafted.
- **WAR-147** — Yes, and say so: a formula may invert its glyph; each of the four rows (Thundercrack Grenade, Command Brand Iron, Ashfang Venom Vial, Slag-Iron Caustic) gains a short note that it inverts or misuses its glyph.
- **WAR-148** — The highest-class ingredient sets a formula's Provenance Class: Skyfire Pulse Vial moves to Class V; Deep Grid Mortar's oath-bone ash is classed like Granite-Bone's; the page and its intro count are corrected.
- **WAR-148** — Hair from a living person is Class III, Vital Draw: Echo-Bloom moves up to Class III; Somnum Flow stands.
- **WAR-149** — Blood drawn from a living Soul Crystal bearer is Class IV, Crystal Draw: Edgetruth Whetstone Oil, Beastheart Serum and Excision Bloodletting Needles become Class IV; Dominion Brand Oil stays IV.
- **WAR-149** — Collapsed-star residue is Class VI, Archonic Residue: found matter with no locatable origin, priced at the top of the scale.

## 2026-09-26 — WAR-3 cards 1 and 2 (system accounts, 20 answers)

Recorded in full on WAR-3's comments of 2026-09-26. In short: EU-by-Stage table; AU/s ladder by Stage; an AU-to-joule rate; numeric Aetheric Density ranges; absorbed energy banks in the practitioner's Crystal; ambient Resonance is a facet of Residue; one turn = 6 seconds; a second Range ladder for non-force reach; eta above 1.0 is real, surplus drawn from the Aether stratum; failure terrain for Limina, Spatium, Vectoria, Vitalia; Path gates cap the ungated component; uncarded pages read Tier bands; unpriced pages priced per Temperance Gate; Mechanica gets a Stage floor and load-scaled cost; contested Harmonic workings resolve Attunement vs Stability; retired Bands replaced by live equivalents; mirror all 136 glyphs first; costs as a share of reserve reaching Starvation; the aftermath is the tell; a defined saturation threshold.

## 2026-09-26 — the system-accounts questionnaire (60 answers, Claude Code chat)

Answered by Isaac in Claude Code chat, deciding the calls the clean rewrites of the 76 technique and Spellcraft accounts made, and the conflicts still open. Each line names the page(s).

- **Vorynn Execution Strike (and every percentage cost)** — Every percentage cost is a share of FULL reserve (not what's left): percentage costs behave like fixed costs; Vorynn's fifth-of-reserve strike empties him in five.
- **Invert Eidolon; Oathrend; Imprinta; Celestial Harmonic Shear** — Keep shares of reserve: fixed EU prices (Invert Eidolon, Oathrend, Imprinta, Harmonic Shear) become set shares so every caster at a Stage gets the same casts before Starvation.
- **Precept** — Precept: the Stage floor rises with breadth; a small geas stays at Glory, a guild code or dynastic law needs a higher Stage.
- **Kami no Kobushi** — Kami no Kobushi (God Fist): bloodline, no Stage floor; the lineage decides who can use it; figures come off each bearer's card.
- **Kami no Kobushi** — God Fist founder's Plane-held 'cistern' is NOT exempt: rescale the reserve and the Works' costs into the Emanation band; outputs shrink by the same factor.
- **Fallacy** — Fallacy: three sizes as rewritten (local lies from Glory at 5%, Wellspring-path lies from Transcendence at 15%, Domain-god lies from Dissonance at 40%, each with upkeep).
- **Resonant Divination** — Resonant Divination floors as rewritten: Tracking at Transcendence, Fate Entanglement at Realization, Dissonance Warning at Emanation.
- **Kurotana** — Kurotana as rewritten: the rite costs 90% of reserve once, the vessel is free, every power including the crow Domain (5% a turn) is billed per use.
- **Dirge Ascension; Final Mercy; Imprinta** — Costs paid in the practitioner's own substance (Crystal mass, memory, Essence Core) are permanent and cumulative, with a hard lifetime limit; Imprinta states a cut to maximum reserve.
- **Spinal Forge Ascent** — Spinal Forge Ascent carries the Overchannel penalty: damage accumulates with use and eventually becomes permanent.
- **Obelisk of the Eclipsed Dawn** — Obelisk of the Eclipsed Dawn: healing and shielding modes cost almost no EU; the price is the emotional playback and strain.
- **Final Mercy** — Final Mercy pours the whole reserve into one strike: one verdict per fight, leaving the user near Starvation.
- **Anima Harmonics** — Anima Harmonics: listening costs reserve (0.5% a turn); long surveillance or negotiation runs the Harmonist dry.
- **Solarbound Aegoric Knight** — Solarbound Aegoric Knight: the knight's own reserve is the fuel (14-37% per release); absorbed blows are only the trigger, with a risk of overfilling.
- **Celestial Decree Aeon-Shard Mandate** — Setting-wide rule: healing and mending always cost more than breaking (Celestial Decree rebuilding 12% vs unmaking 5%, capped at the energy paid).
- **Seraphic Thread Blessing** — Seraphic Thread Blessing: 1% of reserve a cast and a lasting, readable bond with every patient; many bonds cause drift.
- **Vainglory** — Vainglory's upkeep climbs with the lie: the further the construct strays from the summoner's real self, the faster, with a stated measure of that gap.
- **The Veil** — Soul Drift gets a scale with named threshold stages; each Veil crossing adds an amount set by depth and duration.
- **Invert Eidolon** — Invert Eidolon: below Transcendence only a brief, fragile accidental construct forms, never the full thing.
- **Sovereign Parallax Lance** — Sovereign Parallax Lance keeps 400 TJ as a real blast: the Cataclysm cast is a 3 km event that engulfs the caster; the quieter cast stays contained.
- **Sovereign Parallax Lance** — Sovereign Parallax Lance keeps its 900 m reach (the reach of the flaw-reading); stepping beyond 900 m is a counter.
- **Celestial Harmonic Shear; Harmonic Null-Ascension** — Harmonic Shear and Null-Ascension: small drive; the caster supplies a driving frequency and the target's own failure does the damage (0.8-25 TJ); the Grade buys the lock; Null-Ascension's price doubles each turn held.
- **Edict Strike** — Edict Strike: a normal swing is A-Grade (10% of reserve); S only with a swing costing a third of reserve; never SS.
- **Pyrewind Breaker** — Pyrewind Breaker: small open-air shock (about 1% into the blast; 20 m holds in the open; indoors 89-400 m); fire capped at 120 GJ by the sphere's oxygen.
- **Sovereign's Reprisal** — Sovereign's Reprisal scales with what's banked: the release equals what attackers put in, boosted 2-5x from reserve; cheap against mobs, ruinous against peers.
- **Obelisk of the Eclipsed Dawn** — Obelisk SSS Fracture Cascade: state both figures; full SSS only for reserves near the Stage ceiling, A or S otherwise.
- **Transposition; Veil of Verdant Pact** — Splintering takes the 0.60-0.70 efficiency band; the whole Expert row reads 0.60-0.70.
- **Sigillum Fixatio** — Sigillum Fixatio: the held body is truly hardened and resists damage up to the working's full rating (a defensive buff), overriding the rewrite's frame-fails-first reading.
- **Winter Rend; Vorynn Execution Strike** — Cold workings (Winter Rend, Vorynn): the cold is small (~20 kJ from flesh, skin-deep frostbite, shallow nerve block, cracked armour); the yield belongs to the blow it rides, 2-4x harder because the target cannot give.
- **Bloodbind Surge** — Bloodbind Surge may go past A-Grade (top end reads S); each surge past A risks a Crystal Fracture Event.
- **Archivium Locus** — Archivium Locus: the technique page governs (a full turn to write, a 60 m redirecting lattice); the owner's card is corrected; the tell and the 'deny her the turn' counter stay.
- **Aeldoris's workings** — General rule: anyone may allocate Sub-Stats into their Stage's strain band at a stated risk; Aeldoris's Harmonics 430 and Dexterity 410 stand on that basis.
- **Invert Eidolon; Imprinta (and every sustained working)** — A working's wasted energy is radiated as heat at the caster's Shell: large sustained workings scorch their surroundings and can be seen for miles (setting-wide).
- **Crimson Dirge** — Crimson Dirge: each verse removes one nameable step from a process so the law itself produces the opposite result; Core Laws stay inviolable.
- **The Last Monolith** — The Last Monolith: the body refuses the blow; nearly all of it reflects up the attacker's weapon and the rest banks in the Crystal, which can overfill.
- **Symphonia Ascendant** — Symphonia Ascendant: the splinter outcome is a flash and blast at the attack's full energy; the arrival angle decides which of the three outcomes happens.
- **Transposition** — Transposition: unlike-for-unlike trades work because Transmutatio tunes both ends into one frame (10-15% of reserve, from Refraction); any leftover mismatch leaves a partial trade.
- **Winter Rend; Vorynn Execution Strike** — Heat pulled by cold workings goes out through the Shell into the surrounding air; a warm closed room slowly spoils the working; warm air is a tell (Vorynn's page follows Winter Rend).
- **Fluxus Intervallum; Oblivion-Step** — Fluxus Intervallum and Oblivion-Step are fast real crossings (1-60 ms / a quarter-second): an obstruction on the line stops them and fast-reflex fighters can see the streak.
- **Oblivion-Step (and every Hypnather working)** — Hypnather's Core Law becomes 'cannot be forced by ordinary means'; Oblivion-Step stays at will, each use an interrupted rest that wears the Crystal.
- **The Principle Engine** — The Principle Engine gains reserve by using the room as a heat sink (3-8% per serious contradiction, nothing in a cold still room, can overfill); deny it the gradient and it only costs.
- **Edictum** — Spellcraft whose product is a standing condition is durable (Edictum holds without upkeep); state this in the Four Crafts.
- **Thaumic Harmonics** — Thaumic Harmonics choirs: the lead singer's Crystal Fracture risk rises with each supporting voice (that is how a choir exceeds capacity).
- **Lumen Dissecans; Judgment Manifest; Oneiron Phantasm Court; and others** — 'What nobody knows' answers the rewrites stated as fact are presented as one in-world school's reading; the mystery stays open.
- **World Echelon; Dirge Ascension; Celestial Decree Aeon-Shard Mandate** — Add counters a prepared weaker side can use against World Echelon, Dirge Ascension and Celestial Decree (ground, outlasting the window, a divided crowd, detuning, Silence, Knot and Lock, the caster's body).
- **Kurotana; Saba no Rosa; Antinomy; and others** — Every working inherits the documented failures of every Wellspring it draws on; opponents can induce them.
- **Harmonic Null-Ascension; Celestial Harmonic Shear; Celestial Decree; Obelisk** — Harmonic immunity bar is Stage: anyone at the caster's Stage or higher is immune, on all four workings.
- **Archivium Locus; Coagula Dominion; Obelisk of the Eclipsed Dawn** — Area workings sort friend from foe by the caster's judgement/attention; if it slips, allies are caught (Locus, Coagula, Obelisk).
- **Imprinta** — Imprinta deposits are tethered: the page's counters work (kill the maker, break the focus, Silence); the floor rises to Glory or higher and the cost toward 75,000-150,000 EU (expressed as a share of reserve per q02).
- **Speculum Harmoniae** — Nexus Harmoniae: collapse sends a Domain-style shockwave over the whole kilometre, caster included; downing the caster hurts both armies.
- **Saba no Rosa** — Saba no Rosa: redundancy defends; broad, independent standing survives single withdrawals; narrow careers and chained holdings are vulnerable.
- **Fallacy** — Fallacy cannot be recalled: once collapse starts it runs on its own, even the author is caught; planned withdrawals fail.
- **Symphonia Ascendant** — Symphonia Ascendant's prior read is per technique: each technique must be heard separately; an opponent who varies his repertoire beats it.
- **Oblivion-Step** — Oblivion-Step: many per turn, limited by reserve (3% each, about thirty from full) and by drowsy minds in range.
- **Thaumic Harmonics** — Some workings go below hearing: those hidden by Tenebra or Luminalis are too quiet for Thaumic Harmonics to grip, a counter that can be bought.
- **Anointing** — A forced or tricked Anointing can be removed only by Scission, with its complication rate.
- **About twenty-five pages that named no glyph** — Proposed glyphs stay as printed but provisional: confirmed or reassigned once all 136 glyphs are gathered and checked.
- **Dirge Ascension** — Dirge Ascension: Francis's Sovereignty stays capped at A even while ascended (Path-gate ruling holds); the world-rewrite runs weaker.
- **Hunter's Breath; Maw of Crystalline Stasis; Bloodbind Surge; Cryost Ascendant** — Vohrin is one power at two levels, Titan and Wellspring; the four frost workings become Titan-derived, likely raising their standing and cost.
- **Symphonia Ascendant** — General rule: governing Sub-Stats belong to the practitioner, not the working's Wellsprings; Symphonia Ascendant's 5 km reach needs no third harmonisation.

## 2026-09-26 — Ability Law (R47), Claude Code chat

Isaac answered the ability-rules questionnaire in Claude Code chat: abilities are written so he can make up his own applications. Each row below is one ruling; the index pack is rules/doc-ability-law-2026-09-26.yaml.

### R47-1-NO_APPLICATIONS

An ability entry describes what the ability is, never how to use it: the mechanism, what it can act on, its costs, its limits, its tell and its counters. No tactics, combos, worked fights or lines telling the reader how to use it; the owner invents the applications.

### R47-2-FIELD_FORMAT

New abilities use the field format: the card top (Summary card, Codex line, FOW line, Origin) followed by the Physics, Metaphysics, Mechanism, Essence and Counterplay blocks, each a set of one-line **Field** · value entries. The Design Chain and the six-line card are retired as page formats.

### R47-3-COUNTERS_AS_FACTS

Tells and counters stay, written as facts only: what the ability cannot survive and what gives it away, never an instruction to an opponent. Players work out the tactic.

### R47-4-LEDGER_COSTS

A new ability's cost is a share of full reserve. Its EU and joule figures are read off the Essence Ledger's bands for its Stage, and its Grade off the joules to Grade to tier spine.

### R47-5-LADDER_RUNG

Every new item, draught, summon, Domain, Wellspring site, weapon or beast carries its Tier Ladder rung by name, read off the spine.

### R47-6-RESEARCH_STAYS

The research step stays: the real phenomenon is researched first, and the cost and the limits are derived from the mechanism.

### R47-7-NAMES_NOT_NUMBERS

Tiers of standing and ladder rungs are written by name only, never as numbers.

### R47-8-WASTE_IS_HEAT

A working's wasted energy radiates as heat at the caster's Shell; large sustained workings scorch their surroundings and can be seen for miles.

### R47-9-INHERITED_FAILURES

Every working inherits the documented failures of every Wellspring it draws on, and opponents can induce them.

### R47-10-STATS_ARE_THE_CASTERS

Governing Sub-Stats belong to the practitioner, not to the working's Wellsprings, and anyone may allocate into their Stage's strain band at a stated risk.

### R47-11-TIME_AND_ENERGY

One combat turn is six seconds. Efficiency above one draws its surplus from the Aether stratum. Healing and mending always cost more than breaking.

### R47-12-MYSTERY_STAYS_OPEN

A What nobody knows question is never answered as fact on the page; a proposed answer is one in-world school's reading and the mystery stays open.


## 2026-09-26 — the magic docket questionnaire (15 answers, Claude Code chat)

Answered by Isaac in Claude Code chat, covering every magic-system question still open on CONFLICTS.md and the docket with no answer from him. Each line names the row or issue it answers.

- **C-061, C-069** — Unquantified: the Primate's Striking Force line (:78) becomes Part Eleven's reading, an event the local physics must accommodate. The EX joule band leaves the card. 'No recorded instance' stays.
- **C-060** — Stands, outside R44-1: Stage XIV has no attack-output band to miss, so the Primate's 2,400,000,000 EU reserve is not an error and stays as written.
- **C-065** — Immeasurable: Kinjiki's Travel Speed becomes Part Six's Immeasurable Speed classification, as on the Primate's card. 'Not his instrument' stays as colour, and the Mach figures leave the card.
- **C-040** — Card governs (rung I-2, off-ladder runs both ways): the twelve cards' Strike Force figures stand, whether above or below their Stage's Max Grade band. The bands are typical ranges.
- **C-041** — Anomalies, with Strain: Sodoku (Level 320, Stage VI) and Krothar (Level 380, Stage VIII) keep their Levels as in-world outliers. Each card gains standing Residual Strain from the breach, and Krothar's Band name becomes 'IV — Mythic'.
- **C-047** — Raise the Sub-Stats: Ignatius's Ardency becomes 880 and Vitality 900 (upper SSS), so the stat table, the force lines and the yield agree. His Primaries and pool are re-totalled to carry the +482 points.
- **C-062** — The card's η ~0.55 governs (rung I-2): Draven stands 0.05 under the corrected Tier 5 band, and his seven accounts say so.
- **C-063** — Whole row, Stage V included (rung I-1): the corrected Tier 5 · Expert cell reads 0.60–0.70 for Stages V–VII. Fluxus Intervallum, Seraphic Thread Blessing, Veil of Verdant Pact and Transposition's Stage V variant reprice to 30–40% bleed. Karo and Yoko follow the table, per WAR-151.
- **C-072** — Per entity: C-059 applies one factor per person, read from wherever that person states a reserve. 'Essence Capacity' counts as a stated reserve. Dougou's card and Mugen no Hatsurugi take the same factor as The Iron Tree and Muken's card.
- **C-076 (WAR-161)** — The Level law governs: Part Nineteen's EU-by-Stage and AU/s-by-Stage tables are rebuilt from Part Twenty-Three's Level law, replacing the Grade-bracket derivation published 2026-09-26.
- **C-059 follow-up** — Re-run on the Level-law bands: the same C-059 method (one factor per entity, set point at the geometric mean of the new band) is recomputed from each card's pre-C-059 figures, so nothing compounds.
- **WAR-161, AU/s against the cards** — The ladder is typical ranges and the cards stand. The 23 misses stay listed as outliers against the rebuilt ladder.
- **WAR-161, EU floor** — Leave the fractions: no floor on the unit. Fractions of an EU are written as computed, consistent with the decimals answer (WAR-141).
- **WAR-162, the non-force ladder** — Keep the reading: the Passive Pressure Field is the authority radius at reference density, and the published ladder stands.

Context: Asked 2026-09-26 in Claude Code chat over the open magic rows. Items the queue and system-accounts questionnaires had already answered were not re-asked: C-053/C-054 (WAR-102), C-055–C-058 (WAR-146–149), C-064/C-073/C-074 (WAR-15), C-066 (WAR-139), C-067 (WAR-140), C-068 (WAR-141), C-070 (WAR-142), C-071 (WAR-151). C-038 and C-039 closed on rungs I-4 and I-5 (2026-09-25). Their CONFLICTS.md status lines are stale and are bookkeeping under rung I-3. C-062 and C-063 replace the drafts under WAR-132 and WAR-54, which were never logged. No card or page is changed by this entry; each answer is applied in its own pass.

## 2026-09-26 — Writing Law (R48), Claude Code chat

Isaac answered the 50-question writing questionnaire in Claude Code chat (beautiful prose, register, research-grounded techniques, metaphysics on the page, roleplay partnership, combat, characters and dialogue, process). Index pack: rules/doc-writing-law-2026-09-26.yaml.

### R48-01-BEAUTY

Beauty comes from exact concrete detail, images and metaphor, and what goes unsaid (not primarily rhythm/sound).

### R48-02-DENSITY

Lush throughout: every scene gets full sensory layering; slower, denser, more immersive.

### R48-03-SIMILES

Loosen similes only: a good simile is welcome when it earns its place; em dashes stay banned.

### R48-04-METAPHORS

Metaphors come from the POV's own life: trade, homeland, body; metaphor doubles as characterisation.

### R48-05-HIGH_STYLE

High mythic style is allowed freely in narration whenever the moment calls for it (not only in documents).

### R48-06-RHYTHM_LAW

Keep all rhythm rules: the hit is the shortest sentence and sits last, payoffs under 10 words, at most two long sentences in a row; the checker fails anything else.

### R48-07-WHITE_SPACE

Steady paragraphs: medium paragraphs, white space used sparingly so it still means something.

### R48-08-NEW_POVS

New or minor POVs default to close, deep interior: thoughts, sensations, the character's own idiom.

### R48-09-TECH_WORDS

Narration may use technical words freely on its own authority whenever it helps.

### R48-10-MIXING

Drop the Technical/Mystic no-mixing rule: registers mix freely by ear.

### R48-11-HUMOUR

Humour wherever it's earned: funny characters are funny often; tone flexes with the cast.

### R48-12-PROFANITY

Profanity in mouths and in close-POV narration when the POV would think it.

### R48-13-PERIOD_FEEL

Modern words in speech only: characters may talk modern; narration keeps a timeless register.

### R48-14-DEPTH

Research depth: name the real phenomenon and its fault; lighter scenes, less time per working.

### R48-15-SOURCES

Sources: encyclopedia-level, cross-checked against one better source.

### R48-16-REAL_FIGURES

Real figures appear whenever measured: anyone with an instrument or trained eye states figures as often as they would.

### R48-17-NO_CLOSURE

When real physics can't close an effect, reach for researched pseudoscience, metaphysics or another strange idea first: it's fantasy, so metaphysical and pseudoscientific mechanisms are legitimate ways to make it work. (Isaac's words: "Try to utilize pseudoscience or some other made up idea or concept that you have found or researched it's fantasy so metaphysics and other strange pseudosciencitific things can be used".)

### R48-18-INVENTION

Invention goes one clear step past textbook physics: the real law plus one pinned variable, easy for a player to reason about.

### R48-19-BANK

The Phenomenon Bank becomes a growing library: every researched phenomenon (and pseudoscientific idea) is added for future workings and players to draw from.

### R48-20-STRATA

The three-layer account (Aether, Wellspring, Essence) shows at a working's first display and at the finisher; lighter touches between.

### R48-21-NAMING

Narration names Wellsprings and glyphs freely whenever useful.

### R48-22-LENS_NAMES

Real-world names and terms for borrowed ideas (Stoic pneuma, solve et coagula) may appear anywhere they fit, scenes included.

### R48-23-LENS_COUNT

A working carries as many history-of-ideas lenses as shed light on it.

### R48-24-4_THEORIES

The Four Theories surface in scenes through characters who hold and argue them; they colour reads and mistakes.

### R48-25-AWE

Clarity everywhere: scenes explain Wellsprings, rites, oaths and the Veil as plainly as a sword exchange.

### R48-26-INVENTION

The partner may invent NPCs, places and texture mid-scene without asking, logged; bigger things wait for Isaac.

### R48-27-REAL_WORLD

Real-world material borrowed by the partner is credited in the author notes; the scene stays in-world.

### R48-28-TURN_LENGTH

Roleplay turns run about 3,500 words (Isaac's answer: "3500").

### R48-29-PACING

The partner may skip dull stretches: travel and waiting pass in a line when nothing is at stake; the world keeps moving.

### R48-30-SURPRISES

Big surprises (betrayal, ambush, death) only after foreshadowing a player could have caught.

### R48-31-STAKES

Death can happen, if earned: from real mistakes after clear warning; nothing is safe.

### R48-32-NPC_VOICES

Isaac may take over any NPC's voice anytime by saying so; the partner hands it back after.

### R48-33-CHOREOGRAPHY

Duels: every exchange traced (measure, guard and the move by its fencing name).

### R48-34-WOUNDS

Wounds: full clinical gore, anatomy named, blood loss tracked minute by minute, nothing looked away from.

### R48-35-USES

Uses in a fight: each side invents its own; Isaac for his characters, the partner for NPCs within the page's facts.

### R48-36-NPC_WITS

NPCs are veteran-clever with their abilities: use what they could know and have trained, well; never omniscient, never dumb.

### R48-37-COST_SHOWN

An ability's cost shows in the body: tremor, heat off the skin, thirst, a Crystal ache.

### R48-38-AFTERMATH

Every duel ends with a full aftermath beat: wounds dressed, what changed between people.

### R48-39-INTERIORITY

POV interiority is deep and running: thoughts, memories and reasoning flow through the narration.

### R48-40-NPC_THOUGHTS

NPC italic thoughts: roleplay turns keep the one-thought-per-NPC allowance; written scenes keep the POV lock (no NPC thoughts under a lock).

### R48-41-MAGIC_TALK

Characters talk about magic by their training: a Measurewright in gauges, a hunter in folk words, a scholar in theory.

### R48-42-LIES

Frequent lies: many NPCs lie for their own reasons; the player has to catch them.

### R48-43-SPEECHES

Dialogue stays realistic under stress, but a trained speaker may deliver one crafted, eloquent speech at a big moment.

### R48-44-NAME_USE

Narration refers to characters by POV epithets, the way the viewpoint sees them; the naming characterises.

### R48-45-CHECKS

Full check on every roleplay turn: every turn passes the full checker.

### R48-46-WORD_FLOOR

Raise the set-piece word floor above a normal ~3,500-word turn (e.g. 5,000+).

### R48-47-NOTES

Full author notes go in the scene file (rule ids, stat ledger, research, costs); chat gets a short summary.

### R48-48-EXPLAIN

The partner explains the physics and metaphysics only when asked; working it out is part of the challenge.

### R48-49-CITATIONS

Research is cited as a source list at the end of each scene's or ability's notes.

### R48-50-PUSHBACK

When the partner thinks a beat is drifting or a rule reads wrong, it says so in one plain line and keeps writing unless stopped.


## 2026-09-26 — Prose Law (R49), Claude Code chat

Isaac answered the 55-question prose questionnaire in Claude Code chat. Index pack: rules/doc-prose-law-2026-09-26.yaml.

### R49-01-WHOSE_HEAD

In roleplay turns the narration may go to full depth inside Isaac's character; Isaac overrules any thought that isn't his.

### R49-02-TENSE

Tense depends on the job: roleplay turns, and work improved for a roleplay, are written in present tense; written scenes and books are written in past tense. (Isaac: "for roleplays in specific or I am having you make something better for a roleplay it should definitely be present and past for things like writing scenes books etc".)

### R49-03-BAND_CAPS

Lift the per-character depth caps toward deep: every major POV moves closer; the old per-character notes become flavour.

### R49-04-DARIUS

Darius runs deep: band 4, fusing to 5 under violence.

### R49-05-ITALICS

Italic direct thought appears often, whenever the POV talks to himself; more voice.

### R49-06-MEMORIES

Memories may run as full flashbacks, a page or more when they matter.

### R49-07-EMOTIONS

Emotion: show it in the body first; the POV may then name it in his own word.

### R49-08-MEANING

After a beat lands the POV may reflect on what it meant in his own idiom, and may be wrong; neutral narrator summaries stay banned.

### R49-09-CUTAWAYS

A turn may close with a short, clearly marked cut to something the POV cannot see (a Front advancing, an NPC plotting).

### R49-10-EPITHETS

One epithet per character per scene: the POV's epithet changes only when the POV's view of them changes, which is itself the beat.

### R49-11-NOT_KNOWING

The not-knowing quotas (one thing the POV cannot interpret, one confident wrong inference) become optional; no per-scene minimum.

### R49-12-SHORT_FLOOR

The short-sentence floor holds scene-wide: description may run long; short sentences cluster at beats and in action so the scene clears 18%.

### R49-13-VARIANCE

Sentence-length variation targets the guide's 80% (under 50% is the strongest tell): very uneven sentences, strong contrast between fragments and long runs.

### R49-14-PARA_SHAPE

Paragraph-length spread check stays as is (guide wants 50%+, checker warns under 35%); steady paragraphs vary on purpose.

### R49-15-FRAGMENTS

Concrete noun and image fragments are free; negative and 'Only/Just' emphasis fragments stay warned at three per scene.

### R49-16-MODIFIERS

Adjective stacking is by ear: stack as the sentence wants, no limit.

### R49-17-OPENERS

The '-ing' opener and simultaneous-action construction ('Turning, he drew the blade'; 'As he stepped in, the smell hit him') is added to the AI tells and counted by the checker.

### R49-18-SIMILE_COUNT

No simile rate or ceiling: only two similes competing over the same beat get flagged.

### R49-19-EXTENDED

Extended and stacked metaphors are both allowed by ear when they come from the POV's life.

### R49-20-STOCK_PHRASE

Dead metaphors are always rebuilt from the POV's own life, even when a rough POV would think the cliche.

### R49-21-REIFICATION

Reification has no count: judge by ear; keep only 'never at the beat' and 'object first'.

### R49-22-NATURE

Avoid personifying weather and landscape: the world is described, not personified.

### R49-23-HIGH_STYLE

Anaphora and the triad come off the tell list everywhere; always legal.

### R49-24-ELEGY

High elegy allowed: at a mythic moment, loss may be sung in full cadence.

### R49-25-OPENINGS

Openings vary by scene: arrivals open on the senses; tense scenes open in motion.

### R49-26-ENDINGS

Written scenes may end on an action, a concrete image, or a line of dialogue; never a summary or a question.

### R49-27-SCENE_BREAKS

A real jump in time or place inside a turn may be marked with a blank-line break or ornament.

### R49-28-INTROS

First introductions get the full physical inventory all at first sight, in one descriptive passage.

### R49-29-TURN_FILL

A 3,500-word turn is filled balanced: about half texture and talk, half the world moving, before the stop at the next decision.

### R49-30-SHORT_BEATS

Every reply is a full turn of about 3,500 words, even to a quick line or question.

### R49-31-TAGS

Dialogue is mostly untagged: voices sort themselves; tags only when needed.

### R49-32-CUT_OFFS

Interrupted speech is shown with an ellipsis ('I didn't...') and the interrupter's line follows.

### R49-33-CALM_SPEECH

Disfluency in calm speech is by character: some people always stumble, some never do; it is set on the card.

### R49-34-STRESS

Species stress tells win: the uniform stress rule governs humans; each non-human culture keeps its own stress pattern.

### R49-35-SPEECH_CHECK

No exemption for the crafted speech: even it must pass the composure check, eloquent without balanced parallel clauses.

### R49-36-LIE_TELLS

Every lie leaves a catchable tell: a body tell, a fact that doesn't fit, or a detail changed later.

### R49-37-ACCENTS

Accents may use full dialect: heavy phonetic spelling where the culture calls for it.

### R49-38-FUNERAL_TEST

The funeral test is dropped for comic voices: characters whose humour is their voice may be openly funny.

### R49-39-TALK_SHARE

A turn's dialogue and description run balanced, about even.

### R49-40-NOT_X_Y

Not-X-but-Y: any pair where the second sentence corrects the first fails; plain negation standing alone is free.

### R49-41-QUESTIONS

Every question in narration keeps getting flagged for a read as possible hypophora.

### R49-42-FILTER_VERBS

Filter verbs (he saw, he heard, she felt) are counted by the checker, which warns above a rate.

### R49-43-EXPLAINING

Narration may explain causes anywhere, in the POV's reasoning and vocabulary; the mouth-only rules for the why of a working are struck.

### R49-44-MODERN_FLAGS

Modern words in narration are caught by a checker word list of banned modern words, checked automatically in narration.

### R49-45-SCIENCE

Real science and anatomy terms are exempt from timeless narration: they are the technical register, legal in narration and off the modern-word list.

### R49-46-CHEMISTRY

The chemistry ban is lifted for trained POVs: any POV with the training may read the world in science terms, scenery included.

### R49-47-STAT_WORDS

All free: narration may state stat names, Grades, Stages, eta, EU figures and Guild words on its own authority.

### R49-48-TECH_NAMES

Technique names and their translations are free in narration.

### R49-49-FOREIGN

Foreign in-world words appear plain, no italics; meaning comes from context.

### R49-50-OWN_BODY

A trained POV (medical or fighting training) names his own wound exactly; an untrained POV keeps his own body in plain words.

### R49-51-EXPLICIT

Explicit narration stays plain and crude: working-man anatomical words, lush in sensation, blunt in naming.

### R49-52-MEASURES

Narration measures in the POV's own units; exact minutes and figures come from a trained eye, an instrument, or the notes.

### R49-53-BUDGETS

Per-scene budgets stay per scene (not scaled to turn length): longer turns simply run tighter.

### R49-54-KHARVEN

Kharven signature items: two of the five per session instead of per turn.

### R49-55-TIC_WORDS

The repetition tic-word list stays as it is.


## 2026-09-26 — Naming Law (R50), Claude Code chat

Isaac answered the 34-question naming questionnaire in Claude Code chat. Index pack: rules/doc-naming-law-2026-09-26.yaml.

### R50-01-REAL_GRAMMAR

Borrowed real-language names must be real, correct phrases in that language, and the gloss must match what the words actually mean.

### R50-02-FIX_OLD_ONES

A published name that is wrong in its source language has its grammar and spelling corrected where the name keeps its sound; the rest stays.

### R50-03-EARTH_PLACES

A WOTR place may carry a real Earth place name unchanged, anywhere it fits the stratum.

### R50-04-POP_CULTURE

Names that echo a famous franchise (Stark, Greymane, the Night's Watch) are allowed; homage is fine and the name means what WOTR makes it mean.

### R50-05-MYTH_FIGURES

A WOTR being may carry a real god, demon or saint name as a borrowing; WOTR's being is its own, the name is a nod.

### R50-06-SACRED_TERMS

No ban on sacred or ceremonial terms from living traditions in any register; a sacred word used respectfully is allowed.

### R50-07-NEW_TONGUES

The partner may open a new real-language naming register for a new people, logged as pending.

### R50-08-GLOSS_CLASH

R49-48 governs: technique names and translations are free in narration; the older Pack Twenty clauses that kept the gloss off the page and the true name un-narrated are superseded.

### R50-09-ONE_RELEASE

No limit on release calls: an art may be called as often as the fight gives a beat; each call still costs the beat.

### R50-10-NAME_STYLE

Technique naming leans by culture: plain English names for common-tongue fighters, true names with a gloss for houses with a register.

### R50-11-LONG_NAMES

New English technique names are short: two words at most, no stacked modifiers.

### R50-12-COINED_LATIN

New Latinate names use real, correct Latin.

### R50-13-ITEM_NAMES

An item's true name depends on who tells it: each culture names it in its own tongue, and the page lists the names side by side.

### R50-14-ESCALATION

A stronger form of an art takes a suffix in the art's own language (Kurosetsu becomes Kurosetsu-Kai).

### R50-15-DIACRITICS

Macrons, apostrophes and accents stay in names wherever the register uses them.

### R50-16-HOW_EXOTIC

How hard a name is to say is decided by its register: if the register makes it hard, it is hard, and the reader learns it.

### R50-17-SHARED_NAMES

Characters may share a name or sound alike; when they meet, it becomes a beat.

### R50-18-OUTLIERS

The one-in-eight outlier-name budget is dropped: outlier names are free, no ratio, no reason needed.

### R50-19-ZETTARI_BANK

The Zettari keep a free register: names are coined in the register's sound, no element bank.

### R50-20-OTHER_BANKS

No element banks are needed for the Chinese-stratum halls or the Far-Northern peoples; their sound rules are enough.

### R50-21-THIRD_NAMES

The partner may coin a Third Name for one of Isaac's characters through an NPC in a scene; it sticks only if Isaac keeps it.

### R50-22-PLACE_STRATA

A place carries several names, one per culture that uses it; the POV picks which to use.

### R50-23-DOUBLETS

The Accord Latin / common-tongue doublet extends to everything: schools, factions and places get both, and the speaker picks.

### R50-24-SCHOOL_NAMES

A fighting or magic school takes a true name in the founding culture's own tongue, like an art.

### R50-25-WELLSPRINGS

Local folk names for a Wellspring are recorded on the Wellspring's page and usable anywhere.

### R50-26-CHANT_TONGUE

Each practitioner chants in their own language; the Latin-default chant rule is superseded.

### R50-27-NEW_NPC_NAME

A new person the partner introduces is a role (the gate-clerk) until they speak twice or matter; then they get a name.

### R50-28-NEW_WORDS

A word the partner coins mid-scene is logged with the scene, not docketed; it becomes canon only if Isaac reuses it.

### R50-29-COLLISION

When a name invented mid-scene clashes with an existing page, it becomes a beat: two people with one name, and the world notices.

### R50-30-BANK_OR_EAR

Mid-scene the partner may name by ear to keep the pace; names are checked against the banks and sound rules at the scene's end.

### R50-31-SCRIPT_SHOWN

True names are romanised only: no real script (kanji, hangul) on cards, pages or prose.

### R50-32-ITALICS

Foreign names and borrowed words are never italic in prose.

### R50-33-MISPRONOUNCE

A foreigner's bent pronunciation of a name is spelled as heard in dialogue (Gimbzo becomes 'Gimzo').

### R50-34-SAY_GUIDE

Every character card and place page carries a short pronunciation line.


## 2026-09-26 — Vocabulary Law (R51), Claude Code chat

Isaac answered the 35-question vocabulary and diction questionnaire in Claude Code chat. Index pack: rules/doc-vocabulary-law-2026-09-26.yaml.

### R51-01-TIMELESS

Timeless narration varies by culture: plain, undated English by default; some cultures' scenes (Eresse, the Moto court) may take a more antique narration.

### R51-02-CLOSE_POV_SWEARS

Profanity may bleed into close-POV narration, using timeless profanities plus swears invented deliberately for WOTR; other modern words stay out of narration. (Isaac: "Profanity is fine I think we should use timelees profanes and invent some deliberately for wotr".)

### R51-03-LIST_SLANG

Modern-word list, slang: ban only the worst in narration (okay, OK, vibe, awesome, cool); the rest by ear.

### R51-04-LIST_PSYCH

Modern-word list, psychology: ban only the obvious pop-psych jargon in narration (triggered, toxic, closure, mindset, boundaries); anxiety and stress stay.

### R51-05-LIST_TECH

Technology and office metaphors are legal only if the POV's own culture has the thing: an Accord fitter may think 'on the main', a Kharven hunter may not.

### R51-06-EARTH_WORDS

Earth-derived words (herculean, spartan, machiavellian, Achilles heel) are treated like lens names: legal wherever they fit.

### R51-07-CLOCK_WORDS

Seconds and minutes are plain English and free everywhere in narration; in-world time units add flavour.

### R51-08-CALENDAR

Earth day and month names never appear; 'week' becomes the culture's own span (a turn, a quarter-moon); all go on the list.

### R51-09-SPEECH_CAP

How modern a character's speech runs is set on their card; the default is casual, not current.

### R51-10-SLOP_WORDS

A hard-ban list separate from the repetition list: tapestry, testament, palpable, visceral, symphony of, a dance of, whisper of, orbs (eyes), ministrations, electric (touch), velvet (voice), shiver down the spine, a breath he didn't know he was holding, the coppery tang of blood, the smell of ozone; each fails the checker at first use, narration and dialogue.

### R51-11-COLLISIONS

Ordinary words that are also WOTR terms (delve, echo, numinous, sovereign, sanctum, weave, ledger) are used only in their WOTR sense; the plain adjective or verb is banned so the term stays sharp.

### R51-12-WORD_BANK

The elevated word bank (eldritch, chthonic, tenebrous, lambent, sepulchral, incarnadine, stygian, empyreal, ineffable) is used freely, by ear.

### R51-13-WORD_STOCK

Narration's word stock (Old English vs Latinate) is by ear: whatever the sentence needs.

### R51-14-NEW_TERMS

No ceiling on WOTR terms per page; readers learn by immersion.

### R51-15-FIRST_USE

New WOTR terms get meaning from context and use only; no appositive gloss (the zero gloss budget stands).

### R51-16-OLD_BANS_FALL

All older limits on stat names, Sub-Stat names, Guild words and sheet vocabulary in narration fall; they are free in narration.

### R51-17-MID_ACTION

The ban on bare jargon mid-action is lifted: mechanism terms may be bare mid-action; the reader keeps up.

### R51-18-DOUBLET

Narration uses whichever form of a craft term the POV would say: an Engraver's scene says 'the cutting', an Accord examiner's says 'Runecraft'.

### R51-19-ACCORD_LATIN

Accord Latin may appear anywhere by ear: speech, narration or documents.

### R51-20-KHARVEN_WORDS

New Kharven words may be native words, built freely on the Far-Northern sound rules; Kharven speech carries its own words.

### R51-21-MOTO_WORDS

Moto and other Japonic houses use Japanese honorifics and address forms in speech, in a feudal register, never modern casual.

### R51-22-MOTO_VOICE

The Moto narration register is drafted by the partner from The Muster's prose and put to Isaac to rule on.

### R51-23-DAWI_WORDS

Dawi drop into their own tongue freely; context carries it.

### R51-24-ELVEN_WORDS

Elves speak English plus a few Vey-Elarin loanwords for things with no English equivalent, built from the root bank.

### R51-25-BEASTKIN

Beastkin speak whatever Common their home place speaks; no special word stock.

### R51-26-CLASS

Class in diction is set by character only: no class default; each card sets the voice.

### R51-27-DIALECT

Any accent may be spelled phonetically, applied evenly including high-born speakers; the wiki's Accent page bar on eye-dialect is superseded.

### R51-28-CHANT_PAGE

A chant appears in its own language; a POV who understands it may think the meaning in his own words.

### R51-29-SWEARING

Swearing uses both: English swears are fine, and each culture has its own oaths and insults and uses those first.

### R51-30-HOLY_OATHS

Earth religious swears (God damn it, Christ, go to hell, Jesus) are replaced in-world: characters swear by their own powers ('Archons take it', 'By the Sky').

### R51-31-SENSE_BANK

Each culture's Standing Inventory gains a senses entry (smells, sounds, colours, textures); scenes draw from it first.

### R51-32-SMELL_WORDS

Technical smell words (ozone, sulphur, ammonia) are free for any POV.

### R51-33-DOC_REGISTER

In-world documents keep a house style per institution: Accord chancery formal and Latinate, the Dawi Tally terse entries, Moto records in the old register, letters in the writer's voice.

### R51-34-DOC_MODERN

The modern-word list applies to in-world documents like narration; documents are timeless and the checker runs the list on them.

### R51-35-NEW_SWEARS

A starter set of WOTR-invented swears is drafted per culture (Kharven, Moto, Dawi, Accord, Elven, Zettari) from each culture's gods, weather, work and taboos, for Isaac to approve before they are canon.


## 2026-09-26 — Voice Law (R52), Claude Code chat

Isaac answered the 32-question character-voices questionnaire in Claude Code chat. Index pack: rules/doc-voice-law-2026-09-26.yaml.

### R52-01-SAME_MAN

The quiet, controlled older man is the setting's taste: leave the archetype; the swap test catches clashes scene by scene.

### R52-02-VOICE_LEVER

A voice is mind and sound in equal measure: what they notice, want, refuse and how they reason, plus an audible layer (sentence length, contractions, a pet word, pace, dialect).

### R52-03-VOICE_BLOCK

Every major card carries a full voice block with fixed slots: notices first, sentence length, contractions, pet word, never says, stumbles or not, gloss rights, stress shift, grief shift, joy shift, one sample line.

### R52-04-CONTRACTIONS

Contractions are set per character on the card: always, sometimes or never; most sometimes, a few never on purpose.

### R52-05-COUNTING

Exact-number speech belongs to its owners: Lambert, the Measurewrights, clerks and anyone reading an instrument count; everyone else rounds, guesses or doesn't count.

### R52-06-TRIADS

Triads and parallel clauses are legal in any mouth, under duress included; the composure check drops them.

### R52-07-SWAP_CHECK

The speaker-swap measurement is for reading only: no numbers in the checker; cover the tags and sort by ear.

### R52-08-PC_IDIOM

When Isaac's play and a card disagree, his play wins: his character's thoughts sound like the man he actually plays, and the card is updated to match.

### R52-09-NO_LINE

When Isaac gives a wordless beat in a written scene, the partner writes the line in his character's voice, marked as a draft for him to keep, change or cut.

### R52-10-CROSSOVER

Isaac's POV characters are always his: when one walks into another's thread, the partner leaves their lines and choices open.

### R52-11-ILTHARA

The partner drafts a voice block for Ilthara Korvaeth from her scenes and Isaac's lines, for him to approve.

### R52-12-HANDBACK

When Isaac hands an NPC's voice back, his version sticks: the partner carries on in it and updates the NPC's roster voice.

### R52-13-SODOKU_TALK

Sodoku talks as played: full, formal sentences, no contractions, no small talk; the card changes to say so.

### R52-14-SODOKU_JOKE

Sodoku makes jokes only by accident: he never means one; sometimes a flat truth lands as a joke and he doesn't notice.

### R52-15-HILD

Hild sounds eleven because the child leaks: her syntax slips, a sentence started too big and not finished, a wrong word, a question that gets out in public.

### R52-16-LAMBERT

When Lambert is shaken he counts out loud: he falls into inventory (numbers, stores, names) where a man would say what he feels.

### R52-17-DARIUS

Darius is the one who argues: he disputes to your face in reasoned argument while the other quiet men withhold.

### R52-18-GIMBZO

Gimbzo is a loose talker: an easy, rambling old master who goes silent only on what matters; the card changes to match the scenes.

### R52-19-VERINUS

Verinus is a speech-maker: his card is rewritten to match the scenes.

### R52-20-AURELIAN

Aurelian's Sum-gol shows in the words (the dropped copula written into the line, narration marking the rising pitch), under strain and also whenever he is with Mahuo kin or anyone from Sum-gol.

### R52-21-KWON

Kwon Mu-jin never uses his rank or the old court honorifics to win an argument, even when it would work.

### R52-22-YOKO

Yoko is precise and spare at work; at home with Sodoku and family she runs long and personal.

### R52-23-MAHUO_WE

The plural 'we' under strain is a family tell: every Mahuo slips into it under strain, Aurelian included.

### R52-24-KUJO

Kujo's voice is left to his arc: no card work now; the likeness to Muken is fixed only when a scene puts them together.

### R52-25-STRESS_RULE

For named humans under stress, both apply at once: the shortening happens and the card's stress tell rides on it (Kwon over-explains in short broken bursts; Cozbi's short lines come fast).

### R52-26-GRIEF

Grief takes a voice back to its root: polish falls away and the childhood voice returns (Aurelian's Sum-gol, Verinus's coastal cadence, Hild's child).

### R52-27-JOY

Joy in a guarded voice: the speech holds; the joy shows in hands, face and breath.

### R52-28-COMPOSURE

For people trained into calm, composure is free; it costs, visibly, only when it is a real strain.

### R52-29-NPC_RECIPE

Each NPC's voice starts from a researched real-world speaker type (a customs clerk's forms, a field surgeon's triage talk, a drover's calls), credited in the notes.

### R52-30-PROVERBS

Every NPC carries one fixed saying from the Standing Inventory; the sayings are the culture's texture.

### R52-31-COMIC_NPC

The partner may invent a comic minor NPC as a comic voice from the start, with no setup-deadpan-reaction beat; the funeral test no longer binds NPC building.

### R52-32-ROOM_CAST

Room casting is by ear: the partner casts for the scene and fixes voice likeness only when the swap test fails.


## 2026-09-26 — World Texture Law (R53), Claude Code chat

Isaac answered the 32-question world-texture questionnaire in Claude Code chat. Index pack: rules/doc-world-texture-law-2026-09-26.yaml.

### R53-01-IMPERIAL_AGE_SPAN

The Imperial Age runs from the 1800s into the middle of the 1900s, and the technology of that whole span exists across it; the no-rail, no-photography, wire-only limits are superseded. (Isaac: "The imperial age goes from the 1800 into the middle part of the 1900s it should be known that due to how long it is".)

### R53-02-POOR_FIRES

A city's poor edge burns oil, tallow, peat and dung in small fires; rich districts are clean and humming; no factory chimneys.

### R53-03-FIREARM_CEILING

The firearm ceiling is up to 1900 hardware: repeating rifles, smokeless powder, even early machine guns exist, rare and state-owned.

### R53-04-ENHANCED_SHOT

Enhanced shot is standard for elites: guard companies and bounty hunters carry full pouches; ordinary infantry do not.

### R53-05-PROOF_PLATE

Narration may state the cause of any penetration outright, in gunfights as anywhere; the old firearm ban on explaining why a proofed round beats proofed plate is superseded.

### R53-06-WELL_SPAWN

Well-spawn exist: Wells breed hostile creatures, and the Bestiary gains a Well-spawn category.

### R53-07-PRICE_TABLE

A short table of everyday prices and wages is drafted from real period ratios for Isaac to approve; scenes then quote it.

### R53-08-TRAVEL_RATES

Travel uses real period rates by mode (foot about 20 miles a day, mounted 30 to 40, rail where it runs, less in snow and passes), stated by trained eyes and messengers.

### R53-09-WEATHER

Weather and season are tracked like a clock: the State of Play carries the date and season; every outdoor scene shows the actual weather, and cold, wet and thaw change what people can do.

### R53-10-MEDICINE

Medicine is era-appropriate by place: Guild cities have what their decade has (anaesthesia, antisepsis, later early antibiotics); the north and the poor get folk medicine and the barber.

### R53-11-JUSTICE

Ground-level justice borrows each culture's real-world analogue (fines and branding in Accord cities, labour-debt in Kharven, public shaming in Eresse), looked up and logged.

### R53-12-LITERACY

Literacy varies by culture: Eresse and the Accord near-universal, Kharven almost none; set on each Inventory.

### R53-13-FAITH

Faith in practice shows up where it matters: when a character wants something badly (petition is the tell); otherwise absent.

### R53-14-FOLK_KNOWLEDGE

Ordinary people know the rough ladder: there are ranks, silver tokens are feared, Pressure is felt as dread; they could not name a Stage and use folk words.

### R53-15-FOLK_BELIEFS

Each culture's Inventory gets a few named false folk beliefs about magic, some half-true; characters act on them and the narration never corrects them.

### R53-16-GUILD_WORDS

Guild words are free in any mouth: anyone may use them; the common/Guild vocabulary split no longer governs who says what.

### R53-17-THE_BILL

Money before magic holds on the page: any working indoors on a main raises the bill, the meter or the spur, and somebody notices the cost.

### R53-18-AWE

Commoners regard practitioners with awe and worship: a ranked practitioner is half a saint to ordinary people.

### R53-19-QUOTA

Every culture's signature-item quota is two per session, like Kharven's.

### R53-20-MISSING_INVENTORY

When a scene goes to a culture with no Standing Inventory, the partner drafts that Inventory from the wiki first (sourced), for Isaac's approval, then writes.

### R53-21-CANON_GATE

Texture the partner invents in play is canon once logged; Isaac can strike it later.

### R53-22-CAUSAL_TEST

The causal test for texture invented in play is by ear: plausible is enough; the causal line is optional.

### R53-23-MIXED_ROOM

A mixed room layers every culture present in roughly equal measure.

### R53-24-TEXTURE_AND_MECHANISM

The rule that texture comes from the Standing Inventory and mechanism from the Codex is retired: texture and mechanism mix freely.

### R53-25-REAL_OBJECT_NAMES

Real names for borrowed real-world objects are allowed: a yurt is a yurt and a katana a katana when the culture is clearly built on it.

### R53-26-HOW_CLOSE

Real history is taken exactly, then bent one step by the culture's own conditions (the draw, the cold, the Archons), credited in the notes.

### R53-27-MIX_SOURCES

The partner may blend real cultures freely into one WOTR culture where it serves the culture's conditions.

### R53-28-VISUAL_REFERENCE

The visual reference is Lord of the Mysteries and Victorian imperial-age fantasy; the Berserk and Vinland Saga references are retired everywhere. WOTR has its own texture, invented for the world itself, mostly drawn from real-world inspiration. (Isaac: "I want it to look like lord of mysteries or Victorian imperial aged fantasy I don't like the beast or vinland saga reference wotr has its own thing its own texture invented entirely for the world itself it mostly takes from real world inspo etc".)

### R53-29-LOOK_UP

The partner looks up every world fact (wiki, Inventory, cards) rather than inventing it; gaps are flagged, not filled.

### R53-30-TEXTURE_DENSITY

Every beat carries at least one detail that could only exist in this world; sensory layers sit around it.

### R53-31-GONE_LIST

Each culture's Standing Inventory gets a 'Gone' list of three to five named lost things the culture mourns, for elegy to reach for.

### R53-32-TECH_BY_EAR

No decade-by-decade technology page: the partner judges what is era-appropriate in the Imperial Age scene by scene.


## 2026-09-26 — questionnaire-2026-09-26-followups

The follow-up questionnaire (16 answers), Claude Code chat.

1. Hild's age at death: twelve at death. She is 11 on her card's As Of moment and turns twelve before the ninth hour; 'twelve' at her death stands everywhere.
2. Dougou: re-derive his joule figures from his restored EU costs (4.752 GJ, 7.326 GJ, 2.772 to 8.811 GJ, B-Grade); the newton figures are dropped, since no contact distance is stated.
3. Sanctum Lux becomes Sancta Lux on every page.
4. Titles are exempt from the vocabulary ban list; the checker skips the title line ('Verinus: Testament of the Sixty-Fifth' stands).
5. Approved to publish: the price table, the culture inventories (five new sheets plus Gone lists, folk beliefs and literacy for the seven existing cultures), the swears and sense banks, and the Moto, Bram Greymane and Lorn Stark narration registers.
6. Well-spawn publishes, Wells only: the spread along city mains into towns is struck.
7. Wren Greymane's Front becomes a grief Front: the aftermath of his death, Bram and the ridge carrying it, ticks driven by who blames whom.
8. Fire of the Undeserving and The Muster are re-banded as standard (2,500 to 4,500), no new prose.
9. Bara is a character: stripped from system pages like the others.
10. Part Twenty-Three (the Essence Ledger) is rebuilt from the current cards and republished.
11. Ilthara Korvaeth, Charles Lambert, Wren Greymane, Emira Moto, Dhaerin Valorin, Fern Stark and Seiji Tenrai Moto each get a short card (identity lines, Voice, Lore, Ties) carrying their voice block.
12. Every character card gets an As Of line, dated from its own Lore and Standing line.
13. Name fixes applied: Japanese long vowels (Hokai, Seijo, Joka and the Go series take macrons), Coagula Dominium, Symphonia Ascendens, Hae-jin's hanja becomes 海鎮 (Sea-Garrison), and the gloss-only fixes (Kibanda, Kafa-Karim, Hataraki no Sho glosses, Dawi 'elää').
14. Yukari eyes: crimson. The cards win; the bloodline page's silver-violet is corrected.
15. Sodoku's Standing line becomes where he stands at 28, at the muster; the Scourge travels move into Lore.
16. The wire is a Guild line; the Infrastructure page is corrected.

Context: Answers to the open decisions left after the voice, name-audit and 57-answer passes.

## 2026-09-26 — questionnaire-2026-09-26-era-apparatus

The era and apparatus questionnaire (16 answers), Claude Code chat.

1. Prime power: Essence engines. Draw-fed engines replace coal and steam outright; the main and the meter are the industrial revolution.
2. Electricity: Essence replaces it. Electricity was never discovered as a separate force; the Essence lamp and main fill its place.
3. Communication: the telegraph wire everywhere the Guild runs, plus telephones in Guild offices and rich houses in the big cities.
4. Vehicles: rail and city trams, motorcars, airships and aircraft all exist across the span, and WOTR also has vehicles and objects of its own invention.
5. Regional gradient: steep. Accord and Guild cities live in the late span, the provinces decades behind, the north (Kharven) in the early 1800s; a traveller moves through time.
6. Media: newspapers and a penny press, photography, moving pictures and recorded sound all exist (the later ones in the later span and the richer places).
7. The big city is Victorian-Edwardian: brick and stone, four to six storeys, tenements and terraces, glass arcades, Essence-lit streets, iron bridges.
8. Dress is class-layered: the rich dress late-span (Edwardian to 1920s), the middle mid-Victorian, the poor in timeless work clothes, each culture bent by its Inventory.
9. Making: clean, humming Essence works and mills; mass production exists, and the grime is in the working conditions, not the air.
10. Household: Essence cold-boxes in metered houses, a real ice trade and iceboxes, tinned food, and indoor plumbing in the rich districts; the poor salt, smoke, cellar and use privies and standpipes.
11. Materials: cheap steel and iron, rubber and gutta-percha, early plastics in the late span, and the Master Material Ledger's Essence-born materials alongside them.
12. Military: transitional. Cavalry, bright uniforms and drill in the early span; khaki, trenches and rare machine guns later; practitioners change everything anyway.
13. Time: pocket watches for the middle class up, a standard Guild time spreading along wire and rail, bells and the sun in the country.
14. Bureaucracy: heavy. Forms, permits, stamps, registers, typewriters and carbon copies; the Guild is a paper empire.
15. Leisure: theatre and music hall, sport and spectacle (racing, prize-fighting, practitioner exhibitions), cafes, clubs and reading rooms, pleasure gardens and fairs.
16. These answers are folded into The Apparatus of the Age and The Works and Days as settled text with a regional gradient section; still no decade-by-decade table.

Context: Era and material-culture questionnaire.

## 2026-09-26 — questionnaire-2026-09-26-combat-society-politics

The combat, society and politics questionnaire (21 answers), Claude Code chat.

Combat and injury
1. Lethality among ordinary fighters is brutally real: one good cut or a ball in the gut can kill, often days later from infection; most fights end in the first seconds; a wounded man is out of the fight.
2. Healing runs on real timelines (weeks for a cut, months for bone). Vitalia healing can shorten it, but it costs the healer EU and the patient's body pays something (scar tissue, fever, hunger).
3. Essence and stamina run on a hard clock by the Ledger's numbers; long fights are won by whoever manages the reserve; Starvation hits mid-fight on overspend.
4. Death is almost always permanent; the only exceptions are liches, the undead and their kind.

Empire and commerce (it is the Imperial Age: imperialisation, commercialisation and the industrial revolution are happening now)
5. Crowns and chartered houses expand together: the company takes the ground, then the crown claims it.
6. The scramble is for the commercialisation of monster-hunting (hired hunting parties; guild systems spread rapidly, before the full creation of the Guild Accord, which is a communion of guilds), and for Wells and draw, materials, markets and labour, and routes.
7. Commerce shows on the page as branded goods and advertising, chartered share-holding companies with exchanges, speculation and crashes, arcades and department stores, and consumer Essence goods sold as products.
8. The cost of the industrial revolution falls on displaced trades, works labour, the colonised, and unions and unrest.

Magic in society
9. The Guild Accord is forming now, in the story's present.
10. Anyone may practise privately, but taking pay for workings or hunts needs a guild licence; unlicensed hunters are cheap and common.
11. A crime done with a working is proved by trace examiners reading its traces as evidence, and guild courts and crown courts fight over jurisdiction.
12. Practitioners work as hired hunters, works inscribers, company soldiers, and in private practice.
13. Few people lack a Soul Crystal, commoners included, but knowledge of magic is gatekept by administration: the Imperial Age is when nations lock down which kinds of people may use which magics.
14. A common person's Crystal is dormant for life unless someone trains them.
15. Who may learn which magic is decided by natural ability (people are recruited to magical academies and sought out by the guilds), class and birth, nation and loyalty, licence and exam, and bloodline.
16. The lockdown is enforced by controlled texts, Crystal registration, inspectors and trace examiners, the Inquisition, and by the guilds, which locally hunt down those who do wrong.
17. Those who learn anyway: black-market teaching, self-derived workings, the guild loophole (hunting guilds train their own outside the state's gate), and harsh penalties for unlicensed high magic.

Politics and power
18. The Guild Accord's pages read as forming in circles: the Articles and Commission framework bind where a circle has signed and not yet elsewhere.
19. Day-to-day rule is layered: a crown or house holds the land, a chartered company the trade, the guilds the hunters and local policing of magic; each fights the others over jurisdiction, and which layer wins differs by place.
20. The powers fight by proxy and company wars, open war, economic war and intrigue; WOTR needs distinct conflicting factions with different interests written out.
21. Succession follows each culture's own law, set on its Inventory.

Context: Combat, magic-in-society and politics questionnaire.

## 2026-09-26 — night-watch-and-the-mother

The Night Watch and Malphas's organization (Claude Code chat).

1. The Night Watch is a pre-Guild-Accord investigation unit on illegal magic and phenomena. It is a crown office: it works alongside the guilds but answers to the state.
2. Malphas runs an organization called The Mother, after the mother of vinegar, the living culture that sours everything it is added to. Its cells are cultures; recruits are inoculated. The Greyshaft Nine coldhouse cell is one of them.
3. The Mother is a cult.
4. Malphas wants from it: to obtain the unattainable; to feed his backlog (he cannot convert what he holds fast enough); to break the Gate (the state lockdown on who may learn magic); and profit and power.

Context: Faction questions after the combat, society and politics questionnaire.

## 2026-09-26 — C-087

The Night Watch Society is one body with the Night Watch: a crown-chartered society. It holds a crown charter and warrant, is organised as chapters (the Timberline among them) with walkers on fixed walks and a bulletin office, answers to the crown, and keeps the Night Register, which takes up what the Lattice Classification Bureau (a separate office) closes. 'The Society's warrant, not the Bureau's' is the crown's warrant as the Society holds it.

Context: Settles C-087; follows 'night-watch-and-the-mother' item 1.

## 2026-09-27 — ruling-audit-2026-09-27

Corrections from the ruling audit: every answer Isaac gave by questionnaire (510, all sessions) was checked against its record. These rules now state exactly what he chose; the last three were chosen but never recorded.

- R54-8-UNMEASURED_FROM_ZENITH: Unmeasured from Zenith: Stage XV keeps its EX+ Grade label, but its force is unmeasured like Zenith's.
- R47-2-FIELD_FORMAT: New abilities use the field format, in the same look as the card top (Summary card, Codex line, FOW line, Origin): plain headings, short one-line **Field** · value entries in the Physics, Metaphysics, Mechanism, Essence and Counterplay blocks, a table for the numbers, and very little prose. The Design Chain and the six-line card are retired as page formats.
- R57-25-UNCARDED_PAGES_READ_TIER_BANDS: Unpriced Spellcraft discipline pages are priced in EU per gate: each branch at its own Temperance Gates, from the EU-by-Stage table.
- R49-14-PARA_SHAPE: Paragraph-length spread check stays as is (guide wants 50%+, checker warns under 35%); steady, medium paragraphs keep drawing the warning.
- R50-10-NAME_STYLE: Technique naming leans by culture: plain English names for common-tongue fighters, true names for houses with a register.
- R51-02-CLOSE_POV_SWEARS: Profanity may bleed into close-POV narration, using timeless profanities plus swears invented deliberately for WOTR. (Isaac: "Profanity is fine I think we should use timelees profanes and invent some deliberately for wotr".)
- R51-12-WORD_BANK: The elevated word bank (eldritch, numinous, chthonic, tenebrous, lambent, sepulchral, incarnadine, stygian, empyreal, ineffable) is used freely, by ear.
- R52-03-VOICE_BLOCK: Every major card carries a full voice block with fixed slots: notices first, sentence length, contractions, pet word, never says, stumbles or not, stress shift, grief shift, joy shift, one sample line.
- R59-02-NO_ELECTRICITY: Electricity: Essence replaces it. Electricity was never discovered as a separate force; the Essence lamp and main fill its place. Fulguria practitioners are the closest thing.
- R59-04-VEHICLES: Vehicles: railways where they run and trams in the big cities; Essence- or engine-driven motorcars for the rich and the state in the later span; dirigibles for the Guild, the state or luxury travel; early fixed-wing aircraft in the latest part of the span, military and rare; and other WOTR-created objects and things of its own invention.
- R59-06-MEDIA: Media: daily papers and a penny press in the cities, broadsheets reaching the provinces late; photography (studio portraits, Guild identity plates, evidence); early cinema or an Essence equivalent in the latest span; phonographs or Essence sound-plates for the rich.
- R60-09-ACCORD_FORMING_NOW: The Guild Accord is forming now: the communion is being negotiated during the story, and the guilds are still competing hunting companies.
- R60-10-LICENSED_FOR_HIRE: Anyone may practise privately, but taking pay for workings or hunts needs a guild licence; unlicensed hunters are cheap, common and illegal-ish.
- R60-17-LEARNING_ANYWAY: Those who learn anyway: black-market teaching (hedge-schools, stolen manuals, back-room masters; a whole criminal economy); self-derived workings, the mark of the outlaw and the genius; the guild loophole (hunting guilds train their own outside the state's gate, part of why the states want the Accord); and unlicensed high magic is punished like treason: branding, Crystal sealing, death.
- R60-24-THE_MOTHER_IS_A_CULT: The Mother is a cult: a religious following of the Becoming; members seek Malphas's path to undeath and worship the rot.
- R49-35-SPEECH_CHECK: No exemption for the crafted speech: even it must pass the composure check; triads and parallel clauses are legal in it, by the later Voices answer (R52-06).
- R57-26-USAGE_STRIPPED_NUMBERS_KEPT (new): The 76 published technique and Spellcraft write-ups are stripped of usage lines (tactics and fight-count phrasing such as 'three verdicts per fight', 'cheap against mobs'); their numbers stay: costs stay as shares of reserve, and a plain 'reserve covers N uses' stays only where it is a number, not advice.
- R57-27-PATH_GATE_BINDS_ITS_COMPONENT (new): A Path gate binds only the component it names: where a working relies on a Sub-Stat component its declared Path does not open, that component runs capped or absent (Florwyn's Canticle heals but doesn't reinforce); no Path changes.
- R57-28-OWN_FIELD_COUNTS_TO_SATURATION (new): A working's own Essence field counts toward saturation: a threshold is defined in volume and rate, in the new density units, and a working past it triggers the saturation consequence (Crystal Fracture Event for everyone present) like any other field.

Context: Audit of RULINGS.md and rules/ against the AskUserQuestion answers in every session transcript.

## 2026-09-27 — C-089-C-090-C-091

The three conflicts questionnaire (C-089, C-090, C-091), Claude Code chat.

1. C-089: A Path gate caps only the component it names; the rest of the Sub-Stat runs at full. A healer without Body Path heals fully but cannot reinforce. This supersedes R38-1-COMPONENT_GATES_BIND_WHOLE_SUBSTAT.
2. C-090: 'Ozone' is free as a word for any POV; only the stock phrase 'the smell of ozone' stays on the hard-ban list.
3. C-091: 'Numinous' keeps only its WOTR sense and comes out of the elevated word bank, which is eldritch, chthonic, tenebrous, lambent, sepulchral, incarnadine, stygian, empyreal and ineffable, used freely, by ear. This supersedes R51-12-WORD_BANK.

Context: Conflicts recorded by the ruling audit.

## 2026-09-27 — open-conflicts-2026-09-27

The open-conflicts questionnaire (11 answers), Claude Code chat.

1. C-080: Ayame Yuno died later, by her own hand, after the corridor night; she is not among the dead of the corridor night.
2. C-081: Muken's sons who died on the corridor night are Tomuka and Ezo.
3. C-082: The Tenrai dubbed Mizuki the heir, because Mizuki was a child Muken had with a woman before Ayame; but the story clearly sets Sodoku up as the heir of Kharven, and Muken never agreed to make Mizuki his heir despite the pressure.
4. C-083: Ignatius is alive and his whereabouts are known; there was no real report of his death.
5. C-084: Year Zero of the Concordance of Ages is the sealing of the Codex, 715 years ago; the Guild Accord as a communion of guilds is what is forming now.
6. C-085: The Holy Inquisition holds legal standing where the crowns and churches that back it rule, and is outlawed where the Accord's circles have signed; it enforces the Gate in its own territory.
7. C-086: A very few people are born with no Soul Crystal at all; it is rare and remarked on. A Class Ø soul keeps its sealed Shell.
8. C-088: The Night Register is the Night Watch Society's own desk, not the Guild Accord's Arbitration Division's.
9. C-052: Hobgoblin formations signal by Silent Sign-Glyphs as the norm; in deep cold or broken ground a formation falls back to a horn count, which is why the fight at the breach is unusual.
10. C-078: Checks 34 and 35 (defined on the six-line card's Operation line) are retired; the Counterplay block and the fair-play rules cover them.
11. C-079: Reification has no count anywhere, procedural and ledger scenes included.

Context: The eleven open rows in CONFLICTS.md.

## 2026-09-28 — alchemy-conversion-2026-09-28

The alchemy conversion questionnaire (131 answers), Claude Code chat.

Standing decision before the questionnaire: Kwon Mu-jin wrote the Alftian Codex (Volumes I to III, replacing the narrator Vis Trismegistus); Malphas wrote the Necrocursica (replacing Noxinus Ren); a new invented author writes the Papers (replacing Oren Corrant). Each line names its questionnaire id; the questions, options and the audit behind them are in imports/drafts/alchemy-conversion/.

1. K1 (Which era the texts are dated in): The five texts are stamped in the early years of the Imperial Age, and the story's present is itself the early Imperial Age (see the calendar answer at the end).
2. K2 (Is the Heresiology written after the texts?): After: a recent Accord manual drawn from these events. The five cases stand word for word; the meta page and Malphas's card stay true. The texts' events close some years before its issue, in Mu-jin's past. Case II's author 'pulled by access and manipulated through need' must fit Malphas (the Necrocursica items).
3. K3 (When in his life each volume falls): Vols I–II on the road; Vol III after the Ashgate road. Vols I–II fall between fourteen and about nineteen; the eleven months in Urbis become his convalescence on one lung, before the Academy. The Correction answers Rimward. 'Final Testimonies' and 'life's work' go, and Vol III must mention Frithia and infant children.
4. K4 (Texts' doctrine: system canon or one school's reading): System canon: the residues, the Volitional Trace and impression-bodies all become fact. The Crossing, the Lexicon and the Magical Categories gain entries, and the Heresiology agrees with them. (Isaac: "All system canon".)
5. K5 (Sublimatio or Sublimare: which one is sublimation): The physics register wins. Sublimatio is sublimation, Sublimare is distillation. Alchemetrica's operation table, R18-5's list and Kytheris's card are corrected, and Distillation mirrors Sublimare. The Necrocursica's Sublimatio line stands; its separating cleanse becomes Sublimare-aligned.
6. K6 (Calcination and Distillation: Wellsprings or bench operations): Calcination and Distillation are not Wellsprings; they are bench operations only. R18-5's list of Wellsprings that are also operations is amended, Alchemetrica's table drops them, and the cards that call them Wellsprings (Kwon Mu-jin's and about ten others) are fixed. (Isaac: "Fix the cards they aren't right".)
7. K7 (Which residue list the texts use): Both lists on two clocks, hinged on The Crossing's nine days. The Necrocursica's four are the forensic reading inside the nine days; the Codex's three (place, bond, glyph-trace) are what stays after, which the two-year-old commission draws on. The Necrocursica gains a short after-window section, so the Codex and Papers cite it truly.
8. K8 (Which seven keeps 'Seven Cacodaemonic Corruptions'): Heresiology keeps it; the Necrocursica's become the Seven Unmoorings. The Necrocursica's title, chapter 3 heading and Appendix II are renamed from the text's own verb ('it unmoors them', chapter 4), and each failure may name the Heresiology inversion that drives it. Grade III and the God Hand page's 'two sevens' stay true.
9. K9 (Base text: full Word files or wiki): Word files as base; wiki condensations regenerated afterwards. Every contradiction is visible and decided here. The converted texts are first person throughout, and the wiki's Codex pages are rewritten afterwards as condensations of the new text, keeping their chapter subheads and residue table.
10. K10 (How deep the rewrite goes): Full rebuild: structure, events and cast are rethought around the new authors, and the old texts become source notes.
11. ST1 (Real historical names in the texts): Rename historical people; keep gods and idea-names. Furveus loses 'Paracelsus'; Jabir, Gillus and Thom get in-world names; Trismegistus and Asclepius stay under R50-05; Tat is renamed unless he becomes Doyun; the Tablet's wording and the Tria Prima stay, credited in author notes (R48-27).
12. ST2 (When Thom's fourth-residue paper was written): Old paper on the residue; completion method after the commission. The twelve-year paper and crude activations stay; the completion method and the drift date from the commission, and Volume III line 122 reads as the completion step only. Papers line 75 is reworded, or it puts the Necrocursica's first edition about 24 years back.
13. ST3 (Credit for the Volitional Trace and commission): Layered credit, and Mu-jin names it. Madeleine found it and designed the commission; Thom found it independently; Gillus framed the theory and built the mechanism; Mu-jin coined the name. Edit Volume III lines 66, 340 and overview line 63; Necrocursica line 93 credits Mu-jin as namer, not co-builder.
14. ST4 (One letter from Gillus or two): Two letters. Volume II's letter was received and transcribed; a second was intercepted, held in the case file, hand-delivered by the investigator, unopened four months, then answered. Papers line 23 and Volume III line 78 say 'second'; the Necrocursica's note stays as an echo.
15. ST5 (Eleven days or fourteen): Eleven days in all. Line 139 becomes 'Before the eleventh day was out'. Lines 133 and 135 and Volume III line 276 stay true; the change, the request and the ending fall on the last day.
16. ST6 (What happens to Paracelsus (Furveus)): Keep as a new person named Furveus. A roster entry (a short minor-NPC record) with a FOW (Fracture of Worlds, the stat system) line pricing the commission; 'called Paracelsus' follows ST1. Through the Necrocursica he is Malphas's colleague too, a tie Malphas's card must carry.
17. ST7 (What happens to Gillus De Raits): New person with a full character card. A full card with a FOW (Fracture of Worlds) loadout, costs, counters and a Voice block; name per ST1. Mu-jin's and Malphas's cards both gain him in Ties.
18. ST8 (What happens to Vaughaus Thom): Keep as a new person. A roster entry (a short NPC record) with a FOW stat line (Anamnesis, crude impression-bodies, twelve years' activation); name per ST1. Malphas stays the theorist whose architecture Thom scaled, so his card's tell becomes a line he lives into later.
19. ST9 (What happens to Neros): Keep as a new person. A roster entry (a short NPC record) and a voice note; the railway conversation, the stabilised drift and the case-file readings stay. Where he met Mu-jin follows the origin question.
20. ST10 (What happens to Jabir): Keep as a new person. A roster entry (a short NPC record); his name, and Volume III's 'ibn Hayyan', follow ST1. His homeland follows the setting question on the Shaneni empire, a polity canon lacks.
21. ST11 (What happens to Tat): He is Doyun, met as a boy. Tat's scenes move from the Monastery to Mu-jin's room at Sum-gol, when Doyun is about 13 to 15 (Mu-jin 22 to 24). Doyun gains the cat, the Third Corruption question and the address; his boyhood becomes canon.
22. ST12 (What happens to Madeleine Ault): New person with a roster entry and stat line. A short NPC record (dead of lung-sickness; Anamnesis-adjacent scholar; her Stage) with a FOW (Fracture of Worlds) stat line that prices her Trace and the eleven days. Case III stays unnamed.
23. ST13 (What happens to Cassian Ault): Roster NPC through the NPC build. A record with a want, a refusal line, a lie (what the document said) and a voice, so the Papers' interview has a person behind it and a later scene can use him.
24. ST14 (What happens to Halveth): New person, quiet director of the Urbis office. A roster entry (a short NPC record); the twist stays regional, and 'the Research Division' in the Papers and Volume III means its Urbis branch. No Division head changes.
25. ST15 (What happens to the king): Unnamed ruler, a role. No card; he and his wife stay roles, as R50-27 allows for a man with no lines. Case I and Volume II's use of him stay.
26. ST16 (What happens to Asclepius): Keep as a new person. A roster entry (a short NPC record); her name follows ST1. Her atheism follows the setting ruling on God-Essence.
27. ST17 (What happens to Dessa Mael): Keep as a new person. A short NPC record (want, refusal, voice); the Genesio archive scene stays as written.
28. ST18 (What happens to the plagiarising lecturer): He is Doryun, recut as quiet theft. The scene moves to the court: Doryun patiently signs his pupil's later work as his own, with no brawl, and Paracelsus's sternum strike goes. Doryun's card gains the act behind 'estranged', kept separate from the credited correction at fourteen.
29. ST19 (What happens to the Prior and dragon-claw monk): Name the dragon-claw monk; the Prior stays a role. The monk gets a name and a short NPC record (want, voice, his father's death); the Prior stays a role. The father's death 'on Tempus-bred quarry' follows the setting ruling on Tempus.
30. ST20 (Are the three friends canon's three dead?): Leave the line unassigned. No change; the friends' later fates stay open and the three dead can be anyone a later scene needs.
31. ST21 (Correcting Nospheric, Anamnetic and Necrocursica): Fix only the plain misspelling. 'Nospheric' becomes 'Noospheric' in the Necrocursica (13 uses) and on the Sub-Stats page; Anamnetic, Necrocursica and Urbis stay as published.
32. ST22 (A Sum-gol title for Mu-jin's book): Add a Sum-gol title beside The Alftian Codex. A correct Korean-stratum title, his own name for the book, heads Volume I and the overview's name list; 'The Alftian Codex' stays the archive title everywhere else.
33. MJ1 (When Sum-gol emptied, against Mu-jin's boyhood): Before his birth: the Primate's card governs. He is born to the remnant of a house whose valley had already thinned; the school and the sixty roofs are what remained. Ara's 'Sum-gol went' reads as the last of the house going, as her scene already hints. No scene line changes.
34. MJ2 (What Chapter the First becomes): A Mahuo boyhood near the mountain, the house named once. The frost and the mountain come from his card, the fields from Sum-gol's river-valley farming; the sky-watching is new. He names the house once and the Ledger-Prince title (the court epithet he resents) never. 'No men of learning' goes.
35. MJ3 (Whose Trace waits for him, and whose tomb): His own earlier life: 'Vis' was the soul called Geuk-hon. The coffin keeps 'Vis, Alchemical Astronomer' as an Elfin earlier life of the soul Kaalabad names; that soul's four hundred years hold more than one life. Pays off Kaalabad and the Soul Kingdom thread, and makes the author note canon.
36. MJ4 (Where Ara appears in the Codex): Healer in the illness chapter and Vol III's addressee. She treats the friends' illness beside him, and her 'ending as a passage' seeds the Monastery's 'Death is not the opposite of life'. Vol III is written to her, keeping the Rimward promise and replacing 'at the request of no one'.
37. MJ5 (Which corruption Mu-jin finds in himself): Separation turned inward: he corrects everyone but himself. He confronts Paracelsus and Gillus plainly; what he files away is his own matter, the Trace aimed at his signature. Vol II's confession survives nearly word for word, the café walk-out goes, and Vol III becomes the Heresiology's cure, a decision under witness.
38. MJ6 (How much of the Codex's ironic voice survives): A written voice built on his habits, changing by volume. Vol I apologises for explaining; by Vol III he has stopped. He notices the flaw, then the child. Lacquered jokes are cut back to dry self-correction. Length and texture stay, the man is recognisable, and the change shows his growth.
39. MJ7 (What happens to 'Trismegistus' and the Sage titles): An epithet others gave him, which he refuses. After the king's hall the Monastery calls him 'the Thrice-Great'; he writes 'That is not my name', the line he later gives Kaalabad. The word stays in-world and rhymes with the Ledger-Prince; the frame's Sage titles go.
40. MJ8 (Why a living man's journals sit sealed): He filed them openly; the Accord sealed them. He deposits each volume under his teaching vow for common use; the Accord classifies them Mortalis-adjacent. 'Recovered' becomes 'withdrawn under seal'. His open book made restricted doctrine without asking him is the Ledger-Prince wound again.
41. MJ9 (Whose hand wrote the unsigned margin note): Malphas wrote the unsigned margin note that is Volume III's epigraph, in Mu-jin's own copy of Volume II.
42. MJ10 (His Accord standing inside the Codex): The Accord appears only from Vol III, after the rank. Vols I–II show him outside any institution; Vol III's letter and title page carry the Division and the vow. Simpler, but it hides the assessments that sent him everywhere.
43. MJ11 (His part in Category Three and failing seals): Detector only: he feels seals fail, never performs Category Three. He is the Codex's witness of failing seals: the passive sense is free and reaches streets away, a full lens-off read costs its migraine. He diagnoses and warns but cannot perform; Genesio completes through his Anamnesis, never his authority.
44. MJ12 (Whether and how Rimward enters the Codex): Named as his question; what answered stays unnamed. Vol III opens on Rimward as the question the Trace answers: he writes the wall, the eye and the law of response, never who responded. Keeps the promise to Ara and his refusal to invent a shape.
45. MJ13 (His credit in the residue theory): Mu-jin is the witness and namer: he named the Volitional Trace; Gillus De Raits and Vaughaus Thom built the method (follows ST3).
46. ML1 (When in his life he writes it): At Invocation: the compulsion is when he stopped working alone. The preface stays close to as written. The months past the brief are Invocation's relief; the 'worse' a year or two later is The Mother. The warnings read as sincere and tragic, written in the Codex I years.
47. ML2 (Is he the Heresiology's Compelled Author?): Yes: Submission first, then Fermentation Perverted. Case II and Codex II's example stand with the name changed. The preface adds the bargain, sealed Genesio stacks for his pen, beside the coercion. His card's Lore gains a first corruption: the perverted form of his own primary Wellspring.
48. ML3 (Who the titled second compeller is): Gillus plus Zeraphine Drowl, then the Academy's tactician. The Academy gets its first face, her canon betrayal starts at his confinement, and the hand mark is hers. Her card's Lore gains the meeting, fixing her as an Academy officer at the date ML1 sets.
49. ML4 (The name on the title page): Malphas signs the Necrocursica in his own name, Malphas.
50. ML5 (The office on his title page): A sentence title his compellers imposed, which he mocks. Something like 'Scribe to the Genesio Archivum, by order'. Keeps the page's rhythm, shows Submission on its face, and stays card-safe: a leash is not a house he answers to.
51. ML6 (How Malphas and Mu-jin know each other): Malphas and Mu-jin were friends. Mu-jin knows his old friend as Malphas the alchemist and never learns that his friend founds The Mother; the lich and the cult work under other names.
52. ML7 (One Necrocursica or two editions): Two editions: an early manuscript, then a sealed edition. Codex I and II read the first (three categories, the footnote), written in the Codex I years. The extant text is the later sealed edition, with a short edition note. The Papers' 'twelve years' (lines 75, 101) are re-dated to K1's timeline.
53. ML8 (The warning footnote and whose hand): He writes it; the sealed edition drops it; Mu-jin restores it. The first edition has it, as Codex II quotes. The sealed edition cuts it, and Mu-jin's note in the Archivum copy carries it back. 'Survived' becomes literal, and the cut shows his descent on the page.
54. ML9 (How openly the margins foreshadow his fall): Sealed-edition margins show his drift. Short notes by the older, living Malphas against the Third, Fifth and Sixth Corruptions and Category Three, each a step over his own line. The core warnings stay sincere; the document reads in two voices.
55. ML10 (Whether The Mother uses the Necrocursica): A working text he teaches from memory. Each culture's methods trace to its protocols, so anyone who has read it can recognise the cult's work: a counter someone can find. The Mother's page gains one line; the Arena speech becomes that recognition.
56. ML11 (Full resurrection: impossible or only forbidden): Full resurrection is forbidden on paper in the Necrocursica, and secretly Malphas's own path.
57. ML12 (Does the treatise discuss lichdom?): One sealed-edition margin line he refuses to expand. Names liches as the one exception he will not treat, and stops. Honest with canon, no false doctrine, no future-dated layer; the reader sees the gap he is walking toward.
58. ML13 (Whose voice governs his writing): Two registers, one man. The block sets command as his default and the Necrocursica's candour as his grief and joy shifts, the man before The Mother; contractions never. Trim the chatty tics, keep the confessions, so his fall shows in his voice.
59. ML14 (His part in the Genesio activations): Silent partner: his protocol under Thom's hand and signature. His first Fermentation Perverted work runs through another man's signature, The Mother's method before The Mother. The texts stay unchanged on the surface; one sealed-edition margin line hints it; Case IV becomes his unnamed case.
60. ML15 (Is it the Arena's forbidden source material?): Yes: the sealed Necrocursica sits beside the Zettari notes. The speech gains a buried confession: Mu-jin read his friend's book and now describes its use without naming its author. No scene edit.
61. PA1 (What record the new author gets): Full character card. Fracture of Worlds loadout (the stat sheet), voice block, pronunciation line, dated header, voice fingerprint and casting entry. Most work; the investigator becomes a playable NPC with counters, and the Papers and Codex III share one fixed voice.
62. PA2 (The new author's office): The new Papers author is a Night Watch Society investigator on the crown's warrant. Halveth stays with the Research and Archives Division as head of its Urbis office; the case is joint: she opened it, hands the investigator the file and annotates the notes, and her order 'not a report' is a condition of access.
63. PA3 (The new author's culture and naming): Concord human: small name pool, byname surname. An Urbis native named in the Oren Corrant mould, so the filing needs no flattening and name, office and chancery frame agree. Contrasts with Mu-jin's Mahuo name.
64. PA4 (The new author's Stage, or none): No Stage: unwoken, reading by instrument. Class Ø (a Crystal never woken). Every reading comes from instruments and other people's senses; the Gillus meeting is real risk; a Mother culture finds no signature of theirs to follow. The card needs no Wellsprings.
65. PA5 (House style of the Papers): Two layers: the frame (header, classification, cross-references, closing note) in the Night Watch's own office style, and the entries in the author's own voice.
66. PA6 (Citing a sealed text without clearance): Through the Codex: add 'as the Codex reports'. Two phrase edits. The author knows the sealed book only second-hand, which fits the header's 'unverified' Volitional Trace and keeps knowledge limited.
67. WS1 (Which current each Great Work stage draws on): Six stages mapped by physics; Conjunction stays Attraction-driven. Calcination to Cinerion (pyrolytic char), Dissolution to Dissolution, Separation to Judicium (discernment), Fermentation to Rebirthine (breakdown pays for growth), Distillation to Sublimare (if K5 keeps the physics), Coagulation to Coagulatio. Conjunction's Corruption injures Attraction itself. Alchemetrica gains a stage table; Mu-jin's card follows.
68. WS2 (The Genesio site's rung, and why it pushed): Riptide, turned to Obsession Force by Thom's draw. Clean, it needs A-grade output; while Thom draws it reads Whirlpool, so standing there needs S to SS, and 'time wrong' and the Tempus drift (correspondence, not energy) last only while it takes. Completing the oldest Trace drops it a rung.
69. WS3 (Mortalis: river of the dead, or gate): Gate, recast to the physics. Mortalis is Auren's Still Gate; the river becomes Sylorin's soulstream, a Pantheon image, not a current. The 'loan' becomes a current borrowed and stepped out of, as Malphas's card says. The sealed vessel holds the impression-body. Rewrites Codex II's Mortalis passages and Corrant 189.
70. WS4 (Anamnesis: keeper of the past, or its reader): Instrument: records live in the ground; Anamnesis reads them. Genesio's Traces are the hollow's Mnemata, and Anamnesis reads and wakes them. Thom's harm is erasure by coarse reading plus the site's corruption. Vol I's 'nothing is erased' stands as the young author's error that Vol III corrects; the Vol III title follows.
71. WS5 (What becomes of the 'Anamnetic fabric'): Recast to canon and drop the term. Records are the Mnemata of places the dead touched; the world-ledger is Maelor's. The Necrocursica's account of death follows the Crossing's three destinations. About 25 lines change; 'Anamnetic activation' becomes 'waking a Trace' or similar.
72. DE1 (Which Soul Crystal layer each residue comes from): Use the map; split the Nospheric Echo. Every residue lands on a layer and a Crossing product. The Nospheric Echo narrows to the held Echo (voice, habit, possession); its place-imprint half moves to the Harmonic Imprint. K4 decides whether the Crossing page gains the map.
73. DE2 (What a practitioner's body holds after nine days): Only Trait tissue: passive Class IV carry, no active residue. Stage stretches the nine days by days, not years. The Crossing's 'meat' reads as 'no Temperance left', and the ledger stands. Malphas's decades-old bones survive as passive Trait carry: old graves are Class IV stock, but nothing in them is still diffusing.
74. DE3 (Where an unfinished decision goes at death): A commitment laid into the place, read by Anamnesis. An Attraction Layer commitment settles into the ground where the person was bound, as Mnemata (a place's memory imprint). It lasts where ground holds records well (an Anamnesis site like Genesio) and fades elsewhere; Anamnesis reads and wakes it. No canon page changes.
75. DE4 (Which summoning layers make an impression-body): A Greater Summons: vessel, Animatria and Vocatia together. Canon's Tier III (Stage IX to XI, 'ancestral echoes'): Arts vessel, the maker's Core as identity, Vocatia contact with the Trace. The Aphorism turns literal; the Trace explains what he did not foresee. Eleven days outruns 'minutes to hours', so vessel and Binding carry it.
76. DE5 (Is the impression-body's vessel a graded Draft): Graded Draft; Class IV only when rendered remains go in. The vessel carries Class, Fidelity, Carry and a price. Ordinary commissions use Class I to III stock; Thom's regional scaling uses Class IV, where the Bench's blind spot on source and the black market bite.
77. DE6 (Whether a revenant happens without a necromancer): A Crossing that stalls on its own. A revenant is a body that spends its nine days where the Wellspring cannot take the residue: sealed ground, saturated battlefields. It fades when diffusion completes; moving or grounding the body (Stillgate Ash) is the counter. Malphas's 'not supernatural' becomes the Crossing's own account.
78. DE7 (Whether 'necromancy' stays the texts' word): Keep it as the scholars' loose word, with one legal note. Both authors use 'necromantic' as the period term, and the Necrocursica adds a line that the Accord's legal sense is narrower. Matches the Heresiology's own loose usage; least rewriting.
79. GW1 (Great Work stages against the Temperance ladder): The double seven, with a grain clause for Class Ø. Stages I-VII walk the seven once, VIII-XIV again (the Codex's own 'spiral'): Splintering V is Fermentation, Invocation IX Dissolution, Dissonance XI Conjunction, Zenith XIV Coagulation. For Class Ø the maker side is read on grain. A ruling and one line on the Temperance page.
80. GW2 (Where Fermentation sits against the Rot): Fermentation begins in the Rot and completes at the Feeding. Fermentation spans two Turnings: the Rot kills, the Feeding (cibation, measured increments after the Wedding) grows it back. The doctrine counts the stage where it completes, so both orders agree. Same concordance table; nothing reordered.
81. GW3 (Where Distillation sits at the bench): The Whitening: purification inside the sealed vessel, read by colour. Distillation runs as circulation in the Returner (condensate fed back for weeks unopened) and is read as the Whitening. Blacking, Whitening, Reddening then track Fermentation, Distillation, Coagulation. The concordance pins it to a colour, not a Turning.
82. GW4 (What Sulphur, Salt and Mercury map to): Crystal layers by plane: Sulphur Core, Salt Shell, Mercury Attraction. Spagyria becomes layer-by-layer medicine; Separate-Purify-Recombine runs the Parting, Distillation and the Wedding, so it carries Conjunction's Rupture risk. The Necrocursica's Aetheric Shell residue joins Salt; its residue triad stays Malphas's openly 'modified' reading.
83. GW5 (Naming corruptions, and Malphas's charge against Mu-jin): Names, not numbers; Appendix II names it, keeps Malphas's charge. Every ordinal becomes a name. Appendix II first calls the Codex's corruption Separation Perverted, then keeps the Nomenclature charge and the 'general scholarly Corruption' paragraph as Malphas's opinion of Mu-jin, not a correction of canon.
84. GW6 (The four corruptions Volume II promised): Volume III closes the promise in one paragraph, no case studies. The four by their Heresiology epithets (Instrumental Union, Catastrophic Germination, Sanitized Truth, Tyrannous Finality) and Mu-jin's reason for stopping: he teaches only what he has seen in himself. The promise is kept; the Heresiology stays the finished book.
85. GW7 (Reading a corruption on the character sheet): As C, plus an eighth vow Mu-jin writes. Volume III closes the gap with his vow against his own corruption (in the spirit of 'I will not document what I will not obstruct'), and the Heresiology lists it eighth. Every corruption gets a named, findable counter; grain stays unread.
86. GW8 (Where the Codex's Correction sits among theories): Mu-jin's eastern merger of Correspondence and Debt. The answer comes late because it is given on credit and settled out of sight. Still a contested position; the Physical Account gains one line naming it, joining the Aphorism's debt reading and the Tempus drift.
87. GW9 (Origin of the Aphorism of Mortalis): Old debt doctrine, with Mu-jin's gloss as his own. Volume II stands as written. Volume III's line becomes 'my gloss of the Aphorism', the Papers' author credits Mu-jin's gloss, and the overview prints doctrine and gloss apart. The debt reading stays for the alchemy-cost rewrite.
88. GL1 (Which glyph names Mu-jin and Malphas write): Index names in chains; Mu-jin glosses his teachers' names in prose. 'Ie, Perception; I was taught Insight', once per glyph he explains. The Book of Summons' glyph lines move to Index names; the phoneme table stays, labelled an older teaching register that drifted. Malphas writes Index names only.
89. GL2 (The Category One seal ending on Fixatio): 'Flx (Flux), sealed by Tp (Topology) on a Fixatio chain'. Names the checkable glyph and the law it runs under in one clause. Topology 'freezes a local outcome grid for a brief window', which suits a field meant to fade cleanly.
90. GL3 (The last glyph of the Category Three seal): Vor (Return), written as a closing condition. 'The Mortalis seal', closing on Vor: it ends when the Trace's decision is delivered, opened with 'ena' if spelled out. Explains why the Papers' echo ended 'in one breath' after eleven days.
91. GL4 (Which Craft Mu-jin and Malphas practise): Both Draftcraft. Both cards gain a Craft line. Mu-jin's summons are a spoken call over Draft ground; Malphas pours. Their texts write in price, vessel, seal and ledger, and their work is traceable through provenance.
92. GL5 (How Category Three is made and fails): Poured body, Mortalis seal written or cut (Runecraft). The failed seal is an unsealed rune: an open wound that ambient pressure completes into a haunting, misfiring until found and broken. Maker's mark and cutter's hand both trace De Raits, who needs both crafts.
93. GL6 (Where the practitioner's will enters Category Three): Authorization: the Continuum reads the practitioner into the working. One clause moves. The Mirror Trace gets a canon cause at the moment of inscription, and its cure (a third party separating the practitioner's Attraction Layer) stands unchanged.
94. GL7 (Gravemark Ink for the Category Three seal): Yes: the lawful formula names Gravemark Ink. Malphas's formula ties to a priced, scarce reagent that suits a written seal. Short or diluted ink becomes a material cause of the Incomplete Sealing, and the supply gap explains where Vaughaus Thom found enough to scale.
95. GL8 (Mechanica in the Aetheric Bleed): Real Mechanica: Extraction from a dead donor, filed at Grade V. Drop 'legitimate'. The practitioner can be treated over months; the worked ground never heals. The one Mortalis failure that crosses into civilizational breach.
96. GL9 (Whose Mortalis work is lawfully authorized): Paracelsus and Gillus harmonized; Thom outruns his at scale. The commission is lawful work done well. Thom's regional scaling tips into Mechanica, giving the Aetheric Bleed its example and the Papers a concrete breach at Genesio.
97. GL10 (What the Parunic Echo is): Keep the name; it is the Essence Signature in the Residue. 'Parunic Echo' stays as the trade's word for a practitioner's Essence Signature carried in Aetheric Residue, legible from Stage IV. 'Glyph-trace' goes. Logged as a naming-only extension.
98. GL11 (What is written on Jabir's amulet): Very old Old High Runic, readable but undatable. The overview's 'decipher' becomes 'date'. Jabir's recited words are his gloss of the working cut in the copper. Mu-jin reads it at once and cannot place its age.
99. GL12 (De Raits's mark on the wax seal): His registered craft mark, the one struck on his work. 'Glyph' becomes 'mark': a maker's mark if he pours, an Engraver's mark if he cuts. The same mark sits on his impression-bodies, so the investigator can match the seal to the bodies.
100. EC1 (What pays for alchemical work): Drafts from stock and vein; standing works also cost reserve once. Drafts stay reserve-free. A Crystal-bearer's standing work (a seal, Jabir's amulet, an impression-body) costs a once-only share of reserve on the arms-ladder model; a pure alchemist's needs a Crystal-bearer's seal. Alchemetrica gains one line; Category Three gains a real price.
101. EC2 (Can a Draft refill a reserve): R2-6 governs: no Draft refills a reserve. Paracelsus's medicines heal bodies and steady Shells; nothing he brews refuels. The Drafts ladder's 'banked' and 'overfill' sentences and Mnemonis Solution's sizing are corrected. 'Alchemical treatment' reads as speeding Wellspring recovery, not supplying EU.
102. EC3 (Ranking and capping the Crystal-less alchemist): Alchemetrica governs: bench-certified Tiers up to Expert cap their work. Pure alchemists hold Tiers of Standing up to Five (Expert) by bench certification, and that Tier caps what they make. The Tiered Path page and Part Twenty gain one carve-out line: bench Tiers are certified, not read off the Crystal.
103. EC4 (Sub-Stats that govern alchemy and Mortalis work): A Draft profile built from existing Sub-Stats, filed for ratification. Core to Tempering Coherence and Maturity, Shell to Tempering Clarity, Attraction Layer to Harmonics Attunement; Gnosis Analysis and Fluency for reading and chain; Vitality Filtration for exposure. Mortalis work adds Persistence and Cognition. Filed through propose_rule.
104. EC5 (The missing Real Alchemy page): Proceed, and write The Real Alchemy from the conversion's research. As B, and the research gathered (Paracelsus's dosing, spagyric separation, luting, long calcinations) becomes The Real Alchemy page for ratification, so every later alchemy task has R18-5's third source.
105. EC6 (Paracelsus's arsenic and mercury): Real names; the dose is the point; he carries the cost. The medicine heals at a dose and poisons past it. Paracelsus shows early crucible palsy and Draft-mark, which Mu-jin reads on sight. Dose and mechanism are checked by research before print.
106. EC7 (How access and clearance are written): Bench reservation for operations; sealed treatise; Lyssara-style clearance for files. Categories are Bench-reserved by named Tier (EC10 sets which). The Necrocursica is 'sealed' everywhere, as its title page says. The Papers' header and Appendix I read like Lyssara's card ('Tier IV Restricted'). Every Level line changes.
107. EC8 (Where Mortalis costs, floors and counters live): Both: pieces in the prose, a field-format entry per Category. The texts carry law, cost and tell in each author's voice. Categories One to Three each get an R47-2 entry and a Spell Index row with a Stage floor; Category Four gets a refusal entry. Every counter can be looked up.
108. EC9 (What a Mortalis or Anamnesis working costs): The full stack, and a Trace can be used once. Reserve share, site depletion, waste heat, a Drift Scale tick for Category Two and up, and every Anamnesis read erasing what it takes. The Genesio activation gets a hard limit and a visible scar.
109. EC10 (Stage floor for each Mortalis Category): Flourishing, Glory, then Refraction with individual review. Categories One and Two sit on precedent rows; Category Three sits where the Necrocursica says Trace-compulsion begins. Gillus stands at the floor, lawful by rank and unlawful only by review. Reservations read Adept, Expert, Expert with review.
110. EC11 (The impression-body's tells and counters): As B, plus Stillgate Ash as the material counter. A ring of Stillgate Ash (Journeyman gate) grounds the body's residual charge and lets it complete its passage. Living Essence at the ring bleeds too, so the counter costs whoever uses it.
111. EC12 (What kind of commission Paracelsus took): Private, unentered and paid: he sold what he could only hold. The patron broke no law, so the Papers' line stands as said to him; Paracelsus carries the breach and a Master of the Circle's personal liability (the rank that seals). The Codex names the fee; the Papers author has a case.
112. EC13 (How many figures the prose carries): Each author states figures as their instruments give them. Mu-jin reads EU, η and site density whenever he removes his spectacles; Malphas prices each Category as a share of reserve by Stage; the investigator logs readings at scenes. The impression-body's cost, Genesio's density and the drift's scale are derived.
113. EC14 (How much procedure the Necrocursica gives): The Accord's redacted copy: completion struck, Appendix I printed. The sealed original stays complete, so Case II holds. The reader's copy has Category Three's completion steps struck under 'preservable under redaction', and the stabilisation protocol, the defensive counter to a failing seal, printed in full.
114. EC15 (Naming the Castlefall circle's ink): Gravetide Ink, named when the Genesio analysis returns. Keeps the caution beat. A later entry names it from the sample, giving the reader a findable piece and tying the circle to the Boundary role. The circle is the Boundary (Gravetide Ink); the Category Three seal is the Sealing (Gravemark Ink, GL7): two glyph roles on one site.
115. SE1 (Where the Trans-Alftian region sits): Inner World: Ketsuen's valleys and Uplands, toward the Concord heartland. The terraces become Ketsuen's limestone valleys, Genesio sits among the Uplands' dense seeps, Castlefall is a valley rail town and Urbis a heartland city. Invented names survive, including Heresiology Case IV. One geography note on the Ketsuen page.
116. SE2 (Where Jabir's Shaneni empire lies): The New World border where Eresse's old-ground meets the chartered arc. No new polity. 'The Shaneni empire's borders' becomes that border, where two incompatible orders share ground, which explains his synthesis. One line reworded; nothing added to Eresse's page.
117. SE3 (What Genesio is, and how far): One mountain territory: rail to a railhead, then the passes. A day by rail to the Genesio waystation, then two days mounted up the passes: both figures hold. Its archive-town holds the Archivum. Volume I's tanner's flat moves to Castlefall, where Volume II and the Papers already put it.
118. SE4 (One or two Archivums; where the Monastery stands): Two Archivums; the Monastery at Urbis houses the Urbis Archivum. Genesio's is the older outlying house with its own sealed stacks; Urbis's sits in the Monastery's lower floors, so Volume II's two lines already agree. Only the Necrocursica's 'Genesio Monastery' changes.
119. SE5 (What the Heralds are): An order grown from Maelor's lineage of heralds. One Factions page and a line on Maelor's page. The Archivums, the Silent Archivists and the Genesio Anamnesis site gain a patron whose office is memory; Asclepius's scorn for 'God-Essence' becomes a quarrel with the order's theology.
120. SE6 (What Urbis is): A new Inner World heartland city with a regional Division office. The Archives Eternal stays at the Citadel; the Papers' address is a regional desk. One line of geography; rail and trams suit a heartland city.
121. SE7 (Naln: Nalūn or somewhere else): Nalūn: Vaultmere's archivists transcribe; the Measurewrights verify the drift. Two orphans tie to canon, and Vaultmere's pending archivist profile goes into use and needs ratifying. The 'observation post at Naln' becomes the Measurewrights' instrument chair, since Deepvein measures contracts, not skies.
122. SE8 (What Tempus is in the canon sky): The Hermetic name for the Weight, the 29-year wanderer. Fits five wanderers: Tempus means time and the Weight counts generations, so its drift is a public shock. The daylight-eye image goes; Case V keeps its name.
123. SE9 (What moved Tempus, and its course): A sequence; Volume II's cause is Mu-jin's first wrong guess. The commission's nudge settles, then the drift resumes and accelerates with Thom's activations, and reverses once the old Trace completes. Volume III gains one sentence naming the earlier error. Matches Case V and his card's limits.
124. SE10 (What physically moved Tempus): Correspondence: no energy moves it. The drift is the delayed answer the Codex argues for. Its price is booked as debt on the site and the operators, not as an EU figure.
125. SE11 (God-Essence: force or belief-word): A belief-word: Wellspring Essence treated as divine. No new metaphysics. Volume I's 'structural law' becomes the Heralds' reading; the humming bridges are ordinary inscribed arrays. If the Heralds serve Maelor, it names Essence as his gift. Sirel's leakage stays a separate folk name.
126. SE12 (What 'the Eressean era' points to): An Antediluvian site, worked before that Calendar closed. Genesio becomes one of the Guild's surveyed sources, its old hall built on the Wellspring. The unpublished finding on what those sites 'are now doing' becomes the texts' reason Genesio pushes back when drawn.
127. ME1 (Wiki pages for the Necrocursica and Papers): Publish both under The Alftian Codex section. Five pages sit together; Volume III's references and the Halveth line resolve; the INDEX section grows from three pages to five. 'Sealed' and 'Level VI' become in-world labels on public pages.
128. ME2 (Card write-back and the renames registry): Write back and register. Both cards gain the events, checked by the lore-writing pass; the registry gains Vis Trismegistus to Kwon Mu-jin (full name only), Oren Corrant to the new author, Noxinus Ren to Malphas if Noxinus goes, and ST1's renames; casting entries follow.
129. ME3 (Order of work, one document per commit): Composition order: Volumes I, II, Papers, Volume III, Necrocursica. Each document is converted after everything it quotes, so no conversion cites an unconverted source; the Necrocursica's revised edition comes last and cites the finished four.
130. ME4 (Where the converted texts go): Notion pages plus fresh docx files beside the originals. Pages are published in-session and mirrored by the sync; new docx files, such as 'The Alftian Codex (Mu-jin edition)', are saved next to his originals, which stay untouched.
131. Calendar (C-084 follow-up): The count stands: it runs 715 years from the sealing of the Codex (C-084). 'The Imperial Age' names only the age of empire and industry now beginning, so the present is Year 715 of the count and the early years of the Imperial Age. The Concordance's Voyager Era, Long Reckoning and Withering Era become the count's earlier ages under new names, and the 1800s-to-1900s span (R53-01) starts recently. The texts carry Imperial-Age years.

Context: Asked 2026-09-28 in Claude Code chat after a nine-seam audit of the five texts against canon, each finding checked by a second agent. Canon self-conflicts the audit found are recorded in CONFLICTS.md (C-092 onward); those these answers settle are marked ruled there.

## 2026-09-28 — open-conflicts-2026-09-28

The alchemy conversion's open conflicts (9 answers), Claude Code chat.

1. C-106: Kwon Mu-jin was 24 on the Ashgate road and is 38 now, at the Academy. R57-01's 38 is his age at the Academy; the card dated before the Ashgate road keeps Age 24 and its 'ten years since'; the Academy pages stand; the 'forty years' lines in two scenes are recut.
2. C-100: Malphas's card carries two dated loadouts: it keeps its Greyshaft Nine coldhouse date with a living loadout derived from his Stage then, and the lich's figures move to a second, later-dated section.
3. C-101: The Mother begins as a cult of Malphas's rot-method under the living Malphas and becomes a religion of the Becoming after it; R60-24 describes the later cult, and The Mother page gains the turn.
4. C-102: The Materia Wellspring is spelled Monolithion; the Master Codex's 'Monlithion' rows are corrected.
5. C-103: The coal paragraphs are cut; R59-01 governs, and The Bearing and the Holding and The Four Ceilings lose the coal-boiler paragraph and the repeated Logistics Division sentence.
6. C-107: Aetheric Residue thins to a floor: the loud phase fades in hours; the quiet residue thins on a schedule set by local density toward a floor it never passes, so it stays readable by the patient. Mechanica residue does not thin at all. The Core Vocabulary and the Mechanica page each gain a line.
7. C-108: Both laws are true in their own domains: Vocatia gets nothing when the summoner lacks the standing he claims; a Parun Warrant that overstates standing seals and takes the gap from the speaker's body. Rimward fits neither: something outside both laws answered, and the eye was its price.
8. C-111: Parun carries the warrant: the spoken Latin gives the order over the Parun Authorization, canon's normal layering, and the Open Crucible's word 'authorization' for the Latin is corrected.
9. C-095: Mu-jin's card header reads 'of the house at Sum-gol, Ketsuen', matching his Lore, Ara's card and the Ketsuen page; there is no Eastern Concord.

Context: The nine rows the alchemy-conversion answers left open (CONFLICTS.md C-092 to C-112), asked the same day.

## 2026-09-28 — calendar-2026-09-28

The calendar follow-up (3 answers), Claude Code chat.

1. The count keeps its label: IC means 'In Concordance', years counted from the sealing of the Concord Codex. Pages keep their IC dates; only the Concordance and the lines that call the count 'the Imperial Age' change.
2. The Imperial Age began in Year 690 IC. Its technology span (R53-01), rail included, begins then; the present, Year 715 IC, is its twenty-fifth year.
3. The count's three eras keep their names: the Voyager Era (000 to 070 IC), the Long Reckoning (070 to 645 IC) and the Withering Era (645 IC to now). The Withering Era runs on as the present era, and the Imperial Age rises inside it from 690 IC as an overlapping age.

Context: Settles how C-112 (alchemy-conversion answer 131) is applied to the Concordance of Ages and the IC-dated pages.

## 2026-09-28 — alftian-vol1-2026-09-28

Isaac approved the rebuilt Alftian Codex, Volume the First, with no changes. Ratified with it:
1. The Alftian Codex, Volume the First, is Kwon Mu-jin's memoir, deposited in 696 IC, and stands as published. What he states from a read is canon; what he states in error (that nothing that has been is erased) stays his error.
2. Mu-jin's own title for the book is Gameung-nok, glossed on the page only as his house's word for correspondence.
3. Mu-jin crosses into Refraction, Stage VII, in the king's hall, and the first seed of his Domain works as nucleation under Coagulatio.
4. Volume I's physical descriptions of Malphas living, Furveus, Neros, Penn, Venur, Draycott, Strom, Asclepius and the king are canon.
5. Venur's amulet is a Charm cut in Old High Runic, chained [Ma] Recall, [Ir] Continuum, [Lei] Binding; its maker paid once and the wearer pays nothing.
6. Castlefall's ground reads Rill. The hall under Genesio is a Spirit-type site on the Riptide rung.
7. Weight-bred is a drake-hunters' folk belief: a drake hatched the year the Weight returns to its station is the worst of its kind. Penn Ralfsohn's father Ralf hunted drakes under a guild licence and did not come back from one.
8. Maelor's edict, "Nothing is lost, only waiting to be remembered", is cut over the door of the Genesio Archivum.

Context: Isaac said 'go' in Claude Code chat on 2026-09-28 after reading the Volume I draft and its list of invented items; no swaps.

## 2026-09-28 — malphas-living-2026-09-28

Agent ruling under Isaac's direction ("do the Malphas living figures"), applying C-100's two dated loadouts. Malphas's living loadout, on his card as "IV · Stats · The Living Man, at Greyshaft Nine":
1. Greyshaft Nine is dated 706 IC (the present less the night-watch book's nine years). Malphas was born 667 IC and is 39 there.
2. At Greyshaft Nine he stands at Stage X, Realization, Level 350, Level Band IV, Tier of Standing 6 Master, Grade ceiling 725; η about 0.72, an estimate inside the Master band.
3. Pool 11,050 (5,550 levelling and 5,500 Thresholds through Stage X), allocated 11,000 across the Sub-Stats as the card prints them; Depth 725 at ceiling is his widest figure and Dexterity his lowest.
4. His living Crystal State is Refined, going Overgrown only at a Stage transition; Path Spirit dominant, Fate secondary, no Body Path; his Attraction Layer runs under Obsession Force.
5. Reserve 80,241,677.6 EU by the Level law; output 165,000 AU/s at full, placed at the floor of Stage X's band.
Grounds: Part Three and Part Twenty-Three as currently applied, the card's canon lines, the night-watch book and scene, and the published Alftian Codex Volume I; derived and checked three ways (law, canon, design).

Context: Isaac, Claude Code chat 2026-09-28: 'do the Malphas living figures while you wait'. Isaac may overturn any item.

## 2026-09-28 — alftian-vol2-2026-09-28

Isaac approved the rebuilt Alftian Codex, Volume the Second, with no changes. Ratified with it:
1. Volume the Second is Kwon Mu-jin's memoir of his nineteenth to twenty-third years, 696 to 700 IC, deposited in 700 IC, the tenth year of the Imperial Age. What he states from a read is canon; what he states in error stays his error.
2. The commission's vessel is a Class II Field Substrate Draft, fidelity Sound, Carry Marked, shipped to the eastern lowlands at the turn of 697 IC; the fee was three hundred gold marks, half before the pour and half after.
3. Draycott's registered craft mark is a ring crossed by three spokes, the lowest longest, with registry letters beneath, pressed in grey wax.
4. The footnote to the Necrocursica stands in the wording Volume II quotes, and the Necrocursica's conversion matches it.
5. Malphas's left hand healed into a small repeating lattice, pressed and held by a maker nobody names.
6. Neros measured the Weight standing out of its place some turns after the pour, always to the same side, and still by the summer of 697 IC.
7. Mu-jin crosses into Transcendence, Stage VIII, on the Heralds' bridge in late 697 IC, into Invocation, Stage IX, in the summer of 698 IC, and into Realization, Stage X, in the Sum-gol schoolroom in the winter of 699 to 700 IC, where the room keeps his set.
8. The school at Sum-gol is taught under the valley's standing, without fee; the schoolmaster is a woman of the house who came back from the court and trained Mu-jin in the house art from the winter of 697 IC.
9. Doyun is Seok Doyun, thirteen when he enters the east room in the spring of 699 IC as its ninth pupil; his cats are both called Nabi.
10. The fourth residue is the Volitional Trace: the finding is Draycott's, the name and its boundary are Mu-jin's.
11. Ara, at twenty, walks the Sum-gol circuit with Mu-jin, wearing a ring that warms when a wound nearby can still be saved.
12. Volume the Second names three of the Seven Cacodaemonic Corruptions (Conviction, Submission, Non-Commitment) and leaves the other four to the third volume.
The rest of the draft's list of new material, as its author notes set it out, is ratified with the volume.

Context: Isaac said 'go' in Claude Code chat on 2026-09-28 after reading the Volume II draft and its list of 44 invented items; no swaps.

## 2026-09-28 — alftian-vol3-direction-2026-09-28

Isaac's direction for The Alftian Codex, Volume the Third:
1. Volume III is about Kwon Mu-jin becoming a teacher: he teaches the children of Sum-gol, and then goes from one place to another teaching people.
2. In Volume III Mu-jin meets Frithia, his wife, whom he met in Vaeloris.

Context: Isaac, Claude Code chat 2026-09-28, after Volume II was published: 'I do like the idea of the volume three be about he becomes a teacher and teaches sum-gol children and goes from one place to the other teaching people, + him meeting his wife frithia... frithia is someone he met in Vaeloris'.

## 2026-09-28 — alftian-vol2-credit-correction-2026-09-28

Agent ruling correcting item 10 of alftian-vol2-2026-09-28 (R65-10), which overstated Volume II. Volume II's Appendix says the finding came to Mu-jin in Draycott's letter; it does not make Draycott the finder. The credit for the Volitional Trace stands as ST3 (R61-13) gives it: Madeleine Ault found it and designed the commission, Ivor Strom found it independently, Gisli Draycott framed the theory and built the mechanism, and Kwon Mu-jin named it and set its boundary.

Context: Found while filing the Papers' owed conflict rows (C-126): the lead's summary of Isaac's 'go' on Volume II had reworded Volume II's 'The finding came to me in Draycott's letter' as 'the finding is Draycott's'. Grounds: R61-13 (Isaac's ST3 answer) and the published Volume II text. Isaac may overturn.

## 2026-09-28 — frithia-timeline-2026-09-28

Isaac's answers on Frithia and the Mahuo children, setting the frame for The Alftian Codex, Volume the Third:
1. Geturo is Frithia's son, born in 700 IC. Mu-jin and Frithia had one winter together, 699 to 700 IC; she refused marriage and asked not to be written down, which is why Volume II never names her.
2. They met in 699 IC, when Mu-jin was twenty-two, on the night he answered a Legion-class working: she watched him do it. Volume III tells the meeting looking back.
3. The Legion night was at the Carver's Seat of Vaeloris, the Valorin house's research academy in Ketsuen, which Kujo destroys in the late summer of 701 IC.
4. The kiss Frithia takes at Mu-jin's bedside in 701 IC, telling him she will never tell him, is her way back to him after refusing him.
5. Frithia's body is the Academy's: tall, taller than Mu-jin, angular, with brown hair, the bones Lily inherited. The rest of the manuscript's Frithia stays: she is from the ice country, speaks her own tongue before Accord common, wears the ringed-seal hat she made, carries the chin tattoos (three at fourteen, a fourth she added at twenty-two) and the walrus scar.
6. Eight of the nine pupils in Mu-jin's room at Sum-gol died by 701 IC, leaving Doyun, and Volume III tells how.
7. Mu-jin and Frithia marry in 702 IC, after his months in Urbis.

Context: Isaac, Claude Code chat 2026-09-28, answering the Frithia timeline questions (map in /tmp/wotr-drafts/frithia/timeline.md; Option A with the Academy's body).

## 2026-09-28 — farrant-papers-2026-09-28

Isaac approved The Farrant Papers and their author's card with no changes. Ratified with them:
1. The Papers are the field notes of Orin Farrant (OR-in FARR-unt), a woman, born 659 IC in Urbis, Searcher of the Night Watch Society's Urbis chapter on the crown's warrant, with its chapter house in the Ropewalk; she files as "Farrant, O.". They replace the Corrant Papers and run from the autumn of 700 IC to the late autumn of 701 IC.
2. Farrant is Class Ø, unwoken: screened at seven with nothing stirring, entered Class Ø by the chapter bench. She reads only by instrument or through a named reader, and leaves no signature to follow.
3. The case is joint: Halveth, K., head of the Research and Archives Division's Urbis office, opened it, set field notes under the Division's seal as the condition of access, and annotates in the margins.
4. The crown's warrant runs in the crown's land only; in Ketsuen a Searcher can ask and cannot compel.
5. The Castlefall circle is drawn in Gravetide Ink and the drop by the old bench is Gravemark Ink, as the Genesio Archivum's assay names them, Dessa Mael of record.
6. The likeness at the Ault house held eleven days and ended in one breath, having asked for the key to Madeleine's workroom; Draycott's registered mark is on the vessel's lute and on her sealed paper.
7. The Strom Submission has sat below the gate at Genesio about twelve years; the ground at the passage stair climbs through the seasons where drawn ground should fall.
8. Malphas answered Farrant in writing and is filed by his title, Scribe to the Genesio Archivum, by order.
9. At the Castlefall platform in late summer 701 IC Draycott's hold on his weight slipped once when Farrant asked after the treatise's author, and he handed her a packet filed as Volitional Trace, Genesio, active.
10. Farrant carried Draycott's held letter, Exhibit C, by hand to Kwon Mu-jin's lodging in Urbis in late autumn 701 IC; he set it down unopened.
11. Orin Farrant's character card stands as published, and her casting entry is as filed.
The rest of the Papers' and the card's lists of new material, as their notes set them out, are ratified with them.

Context: Isaac said 'Go' in Claude Code chat on 2026-09-28 after reading The Farrant Papers and Orin Farrant's card with their ratify lists; no swaps.

## 2026-09-28 — necrocursica-calls-2026-09-28

Isaac's answers on the Necrocursica's sealed edition:
1. No document names who drew the Mortalis Categories or first numbered them. The Necrocursica states the Categories as binding wherever a circle has signed and never says who drew them, and Volume III does not number them.
2. Clearance runs upward: a higher Tier numeral is more restricted. The treatise is Tier VI and the Codex Tier IV.
3. The Necrocursica's seven failure-cases are the Seven Unmoorings: the Mirror Trace, the Worn Habit, the Incomplete Sealing, the Open Shell (formerly the Aetheric Bleed), the Averted Regard, the Misnaming and the False Vocation. The earlier rulings that use the old names stay true through the renames registry.
4. The first manuscript of 695 to 696 IC carried the warnings and confessions that the sealed edition's margins later step over; the sealed edition keeps them under new heads and cuts the footnote.

Context: Isaac, Claude Code chat 2026-09-28, answering the four calls the Necrocursica groundwork's critic left for him (/tmp/wotr-drafts/necro-brief.md, Critic D).

## 2026-09-28 — alftian-vol3-2026-09-28

Isaac approved the rebuilt Alftian Codex, Volume the Third, with no changes. Ratified with it:
1. Volume the Third is Kwon Mu-jin's memoir of 699 to 702 IC, written to Ara in Urbis from late autumn 701 IC, its last chapter at Sum-gol, deposited at the start of winter 702 IC, the twelfth year of the Imperial Age. What he states from a read is canon; what he states in error stays his error.
2. The Legion night: the Carver's Seat was testing a Legion-class working for the kingdom's standard when the summoner's hold broke; Mu-jin, there to deliver a correction to the entering grammar, laid a chalk circle and called as what he was, and the hosts stood down one at a time. Frithia watched from the hall door, thirty-four, come south to teach the Seat's wardens.
3. Geturo was born at the end of the summer of 700 IC, Ara delivering him; Hiromi was born at Sum-gol in the summer of 702 IC while Mu-jin was in Urbis.
4. After the Legion night the Division of Alchemetrica entered Mu-jin as a Registered Natural and reassessed him four times; the fourth gave him the rank of Archmagus, which he took as a licence to certify teachers and enter pupils for the kingdom's examination in the Draft trade.
5. The Division posted him to teach: a draw-town's meter house, a settlement past the last warded station, and a river-town infirmary. At the Zettari camp he swore the Dawn Guard's teaching vow at the quench, before the camp's Stone Witness.
6. The eight pupils he entered for the examination died when the Carver's Seat fell in the late summer of 701 IC: the Hong boy, the Baek boy, the Tak twins, the potter Ahn's two girls, the Yang boy and the Hwang girl. Doyun was with him at the camp and lived.
7. At Sum-gol, after the orchard, five of the valley died and every child on the terraces was dug out alive by the line Frithia had drilled.
8. Three fingers of Mu-jin's left hand were cut in Urbis where the line drew itself, with Furveus naming the place.
9. At Genesio the Trace in the first coffin, laid by an Elfin astronomer two hundred and sixty years dead and aimed at Mu-jin's signature, completed into him through Anamnesis. He reads it as a correction: correspondence is a law of response. The hall fell from Whirlpool back to Riptide, the lamps pulse again, and nothing left in the stone can be woken.
10. Strom's completions have stopped; he is held under review by the Research and Archives Division's Urbis office on an unheard charge of extraction. Draycott holds no appointment and no rank from any of it. His old paper is titled On a Residue of the Dead That Keeps an Intent.
11. Frithia asked Mu-jin to marry her in the east room at Sum-gol in the autumn of 702 IC, and they married there before the turn was out; she struck two sentences from the book.
12. Mu-jin swore a vow of his own in the east room before Doyun and Frithia, over a vessel he poured: "I will not write down what I have decided not to stop." It is entered on the room's roll beneath the eight names.
The rest of the draft's list of new material, as its author notes set it out, is ratified with the volume.

Context: Isaac said 'go' in Claude Code chat on 2026-09-28 after reading the Volume III draft and its list of invented items; no swaps.

## 2026-09-28 — necrocursica-2026-09-28

Isaac approved the Necrocursica's sealed edition. Ratified with it:
1. The extant Necrocursica is Malphas's sealed edition, written by order at Genesio in 703 IC and sealed below the gate at the thaw of 704 IC at Tier VI, signed Malphas, Scribe to the Genesio Archivum, by order; its first manuscript was begun in the winter of 694 to 695 IC and finished in the spring of 696 IC, and lies sealed beside it.
2. Its copies are the sealed original at Genesio, a second sealed copy in the Zettari archives, and the Accord's copy for the Research and Archives Division's Urbis office, with the completion steps of Category Three struck under redaction.
3. It reads four residues inside the nine days (the Corporeal Residue, the Aetheric Shell, the Noospheric Echo and the Volitional Trace), in that order of reading, and three after them (the Harmonic Imprint, the Sympathetic Bond Trace and the Parunic Echo); a Trace laid in ground that keeps records stays past the nine days.
4. For the dead it maps the Tria Prima as Sulphur to the Volitional Trace, Salt to the Corporeal Residue with the Shell, and Mercury to the Noospheric Echo; a revenant is a stalled Crossing, grounded by Stillgate Ash or by moving the body.
5. The Mortalis Categories bind wherever a circle has signed, each with a floor, a reservation, a cost, a tell and a counter: One at Flourishing and the Adept gate, Two at Glory and the Expert gate, Three at Refraction and the Expert gate with individual review; Category Four has no floor and no gate, and an application is entered against the one who makes it.
6. The Seven Unmoorings, with their drivers: the Mirror Trace (Submission), the Worn Habit (none), the Incomplete Sealing (Non-Commitment), the Open Shell (Instrumental Union), the Averted Regard (Catastrophic Germination), the Misnaming (Conviction) and the False Vocation (Tyrannous Finality).
7. The sealed edition cuts the first manuscript's footnote, and Kwon Mu-jin's note in the Archivum copy restores it in its own words.
8. Five margins in Malphas's later hand step over his own lines, one of them naming the lich as the one dead thing that stays itself, and refusing to treat it.
9. Appendix I is Furveus's stabilisation protocol as Malphas modified it for Mortalis work, with its doses of white arsenic and calomel; Appendix II answers the third volume of Kwon Mu-jin's Codex.
10. Malphas's fixed saying is "A melted coin does not testify."
The rest of the draft's list of new material, as its author notes set it out, is ratified with it.

Context: Isaac said 'go' in Claude Code chat on 2026-09-28 after reading the Necrocursica sealed edition and its ratify list; no swaps.

## 2026-10-03 — style-law-2026-10-03

The style questionnaire (138 answers), Claude Code chat.

Isaac's direction, in his words: "let's change the style for WOTR and do a questionaire, on the way it's written since I wanna focus it being more a mixture of western and eastern writing styles etc descriptions should cover a wide variety of things"; "I want WOTR to be written like a LitRPG etc"; "I think another thing is we should do names and a lot of them should be funny puns or other stuff just fantasy names like Borin and Snorin it be funny"; "we should also do something particularly for vocab". Each line names its questionnaire id; the questions, options, sample passages and the research behind them are in imports/drafts/style-questionnaire/. Prose questions were answered in a picker with samples; housekeeping ones were taken as section digests (the recommendation accepted). The rule rows are rules/doc-style-law-2026-10-03.yaml (R70), whose id numerals are the numbers here.

1. K1 (The blend model): Fused, tilted by culture. One house style draws on all three strands in every scene, and the POV's culture tilts the mix: a Moto room leans further East, an Accord counting-house further West. R5-A, R5-E and R11-1 are rewritten.
2. K2 (How LitRPG WOTR becomes): Full LitRPG, screens. Practitioners see their own readouts: a screen at a reading, a notice at a level, a breakthrough or a cost. Where the screens come from in the world is LR22's call; every figure traces to the sheet (R12-5).
3. K3 (Which strand leads which layer): Eastern voice leads. Eastern leads narration, interiority and structure; Western leads combat, injury and dialogue; LitRPG leads progression. The narrator itself changes most.
4. K4 (Western models): Yes to: Tolkien (Elegy, high style, routes, songs and many-named places stay named under Tolkien; his moral voice stays barred (R5-E). Unticked, the same register stays legal under R48-05 without his name); Dickens and the Victorians (Joins the list: the city as one organism, money and institutions on the page, the serial hook. Fits the Draw Age's Victorian look (R53-28); the narrator's moral verdicts stay out); Guy Gavriel Kay (Joins the list: Western craft carried into Chinese-history settings, an elegiac storyteller who looks ahead to what the years will do, courts run on poetry and rank. A ready bridge for the Chinese-register halls and Korean courts). Not taken: Martin and Abercrombie. (Dickens/Victorians, Guy Gavriel Kay, Tolkien kept; Martin and Abercrombie unticked (dropped as named models). Added in his words: 'Other Eastern Writers like Creator of Naruto and Bleach and other animes litRPG light novel etc like unbound and beginning after the end'.)
5. K5 (Eastern models): Yes to: Jin Yong, chapter novels (The Chinese-register halls gain a model: named forms traced to a lineage and a manual, sect politics run like a state's, the chapter novel's storyteller and couplet chapter titles); The Heike and war tales (The Moto and Shirogane gain their tradition: the name-declaration before combat, armour catalogued piece by piece, impermanence felt at the fall of a house); Kawabata and Tanizaki (Japanese restraint gains a named model: the scene that breaks off before its point, the season in one exact detail, rooms described by how they hold light and shadow); Pansori and sijo (Ketsuen, Hon-guk and the Mahuo gain a literary voice: tempo matched to feeling, comedy inside tragedy, han (grief held for years, never released), and sijo, three-line verse that turns in its last line).
6. K6 (LitRPG and progression models): Yes to: Cradle (Ranks everyone in a room can sense, breakthroughs written as set pieces, little need for screens. Matches how Pressure already works in WOTR); Reverend Insanity (A Chinese cultivation novel run as a ledger: every gain bought, every resource counted, a cold calculating mind at the centre. The grimdark end of cultivation fiction, close to WOTR's cost law); Solo Leveling (The Korean System novel: the reassessment that overturns a registered rank, quests with stated penalties, the daily drill as a contract. Its escalation and onlooker shock run into the R5-B tells); The Wandering Inn (The level-up as a quiet verdict on who a person became that day, arriving in sleep; bracketed class and skill names inside ordinary sentences).
7. K7 (How far to move): New pack, old hygiene. A new style pack supersedes Pack Five's flesh sections and R11-1 and re-rules the R5-B and R5-G tells one by one; the anti-machine checks carry over unchanged.
8. K8 (Which jobs the style governs): All four alike. One style law; every job takes the blend in full, readouts included. Documents keep their institution's house style inside it.
9. K9 (The Technical and Mystic registers): Strands mapped to registers. R12-2 is rewritten: the Technical register draws on LitRPG and wuxia (numbers, named forms, the read); the Mystic on Japanese and Chinese literary craft and the gothic (law, the half-seen). R48-10's free mixing stays.
10. VO1 (The narrator's stance): Storyteller at thresholds. In a chapter's opening and closing lines the narrator may address the reader, foreshadow or set down a maxim; the body of the scene stays POV-locked. R5-C1 gains a threshold exception.
11. VO2 (The wide view): Sweep with marked dips. Battles and crowds may run a marked roll call: one line inside each of several heads, then the lock resumes. R1-3's name-three rule exempts roll-call lines, and R39-7 gains rules for them.
12. VO3 (First person): Third person only. Third person becomes law for turns, scenes and books; first person stays in documents. Rotating POVs and the lock stay easy.
13. VO4 (Epithets in narration): Rank and trade tags. An epithet may be a rank or trade tag (the Flourishing envoy, the Measurewright) whenever the POV can read rank; still one per scene, changing when the reading changes.
14. SP1 (Kishōtenketsu): Kishōtenketsu for quiet scenes. Quiet, travel, downtime and interlude scenes may run set-up, development, twist, reconciliation with no conflict; fights, councils and set pieces keep the turn. Scene briefs name the shape; roleplay turns still stop at Isaac's decision.
15. SP2 (Tempo and stillness): Jo-ha-kyū tempo. Set pieces and long scenes run slow, breaking, swift at scene and paragraph scale; R49-25's motion opening becomes one option among others, and the hit still lands short and last (R48-06).
16. SP3 (Opening modes): Yes to: Far to near (Arrivals may open on a long view that moves in, plane by plane, to the person, as Chinese landscape painting does. Feeds the archive's thin landscape); Season word (An opening may fix time and mood with one culture's season word (Ward-Lighting, the Thin Weeks, Ice-out) instead of a mood statement; each Inventory's Time field becomes a season list); A reading or document (A scene may open on a register entry, readout or document that the scene then tests (R12-4's threshold voice), as Lord of the Mysteries and LitRPG chapters do). Not taken: Image linked by mood.
17. SP4 (Closing modes): Yes to: Mid-crisis cliffhanger (Chapters, and turns at the next decision, may stop mid-crisis on a reveal or a threat, web-serial style; R49-26 gains the hook R5-F already wants); A notice or readout (A scene may close on a notice or readout set off from the prose: what the scene cost or earned, in figures traced to the sheet (R12-5)); Break off before payoff (A scene may stop a breath before its emotional point and leave the payoff to the reader or the next scene, as Kawabata does; the next scene owes what was withheld). Not taken: Storyteller's next chapter.
18. SP5 (Arc shapes): Yes to: Tournament and examination (Tournaments and examinations become a licensed arc: rounds, brackets, scouts' odds, a ranking at the close. The Aetherion Academy arc already runs this way; ticking it names the shape); The Well delve (A Well may be worked as an arc, deeper ground and worse spawn at each stage, each stage closed on its cost; Well-spawn (R53-06) supply the threat); The training montage (Weeks of drill may pass in one compressed passage that ends on a reading of what changed; R48-29's skip gains a form for growth); Episodic jobs (A chapter or session may be one self-contained job, opened and closed in itself, inside the longer arc, as light novels and The Wandering Inn run).
19. RH1 (Paired and cumulative sentences): Both, in set pieces. Both licences, in set pieces only; ordinary turns keep the full rhythm law.
20. RH2 (Paragraph shape): One-liners at peaks. Medium paragraphs stay the norm; reveals, verdicts, notices and a fight's last beats may run as one-line paragraphs in a cluster. R48-07 is amended; R49-14's shape check stays.
21. RH3 (Cadence by culture): POV's culture sets it. The POV's culture sets cadence, and each narration register states it. A Hallenfeld man stays Hallenfeld in a Moto house, and the gap between his rhythm and the house's is the texture.
22. RH4 (Sound words): Each culture's own words. Each culture may carry a few native sound and state words in speech and close narration, entered in its Inventory and never italic (R49-49). Moto and Korean-register houses gain most.
23. RH5 (Chapter heads): Yes to: Couplet title (A book chapter may be headed by a matched couplet naming its two main events; the table of contents reads as a poem and a promise); In-world epigraph (A chapter may open on a short in-world document (case-book, register, proverb, letter) in its institution's house style (R51-33), which the chapter then tests (R12-4)); Verse header (A chapter may open on a short verse in a culture's own form (a Kharven riding-song, a Korean sijo), and verify checks it as verse, outside the rhythm statistics).
24. VB1 (Eastern concept words in narration): Felt word, measured word. The loanword names what the body feels; the WOTR noun names what a gauge or the Guild measures, in the same POV's narration. The Eastern inside and the LitRPG outside sit side by side.
25. VB2 (Foreign words on the page): Context plus a glossary. Prose as in A, plus a glossary at the back of each book and a terms page on the wiki. The page stays clean, and LitRPG readers get the reference they expect. (Option A there reads: Plain, context only. Current law. No italics and no explaining phrase; the scene carries the meaning. Immersive and quick, and now and then a reader guesses wrong for a page.)
26. VB3 (Learned tongues beside Latin): A learned tongue each. Hanmun tags for Korean-stratum scholars, kanbun readings in Moto records, wenyan in the lineage halls, Latin for the Accord, each real and romanised (R50-01, R50-31). Every learned culture gets weight; every tag needs checking.
27. VB4 (How antique the narration runs): A dial per culture. Each Standing Inventory sets plain, period or archaic as law, amending R20C-58, and narration follows the POV's culture. The sample is a Moto-court steward under an archaic dial; a Kharven POV stays plain.
28. VB5 (Trade and science words): As now, mixed. Narration names apparatus and workings exactly by ear; an untrained POV's own body and his reading of the scene stay plain. Check 30's floor holds.
29. VB6 (Units of measure): The POV's own units. Current law. A Kharven guard counts in bowshots and a pot's boil, a Measurewright in yards, pounds and joules. Units characterise, and the exact figure stays with trained eyes.
30. VB7 (Numbers: words or digits): Small in words, big digits. Words up to one hundred and for round numbers; digits for exact large counts and every system figure (Level, EU, AU/s). Sourced figures stand out as data.
31. VB8 (Capitals for system terms): Canonical terms capitalised. The archive's habit fixed as a list: Stage, Band, Grade, Level, Wellspring, Essence, Aether, Pressure and Sub-Stat names capitalised; reserve and the draw lower case. Plain senses (a band of riders) need care.
32. VB9 (New words: what kind, how many): All three, by owner. English compounds for common things, a culture's native word where that culture owns the thing, capitalised labels for system and instrument things; no cap, all logged (R50-28). The blend in one rule.
33. VB10 (A word bank per culture): A Words entry everywhere. Every Inventory gains a Words entry: native words, trade terms, slang and address forms, each with meaning and who says it. Scenes draw from it first; a checker can spell-check against it.
34. VB11 (Real-language swears in narration): The POV's own tongue. A Japonic, Korean or Chinese-stratum POV may think his own language's swears, romanised, correct and never italic (R50-01, R50-32), beside English and WOTR ones.
35. VB12 (The hard-ban list): Yes to: Cultivation-translation stock (Bans 'qi surged', 'a cold glint flashed', 'sucked in a cold breath' and 'killing intent surged' in narration. The Eastern feel comes from method, never from translated filler); Western fantasy stock (Bans 'the steel sang', 'a grim smile', 'his blood ran cold', 'every fibre of his being' and 'darkness gathered'. Grimdark's own worn phrasing goes out with the imported kind); LitRPG stock (Bans 'power surged through him', 'stronger than ever', 'a wave of power' and 'his stats soared'. Growth shows in the body and on the instrument); Trim the false hits (Narrows three items to their stock sense: a will called a testament passes, 'visceral' passes in anatomy (the visceral pleura, R49-45), 'orbs' passes for lamps and regalia. The stock senses still fail).
36. VB13 (What the checker enforces): Yes to: Word-bank spelling check (Native words are matched against the culture banks (VB10); a near-miss FAILs as a misspelt Wellspring does (R14-5-NEAR_MISS_FAIL); unknown words are listed for the scene log (R50-28)); Canonical term list (wotr_terms.txt is built from Fracture of Worlds, the glossary and the Codex; Stage, Band, Wellspring and Family names are checked for spelling and capitals (VB8), and a near-miss FAILs (R14-5-NEAR_MISS_FAIL, Check 37)); New ban families FAIL (The families chosen in VB12 FAIL at first use in narration, as R51-10 does; looser variants of a banned phrase WARN for a read); Style-sheet warnings (WARNs for the house style set here: an italicised loanword (VB2), a digit where words are due (VB7), an archaic word outside its culture's dial (VB4). Holds the style without blocking a reply).
37. IN1 (Modern idiom in thought): Thought as he speaks. Italic thought may use whatever the POV would say aloud, modern words included; plain narration stays timeless. verify drops italic thought from the modern-word check.
38. IN2 (How reasoning shows): Yes to: Stepwise lists (A reasoning POV may set thinking out as numbered steps, risk lists or tests in italic thought; R16-8-CHECK33's cap on technical terms in italics eases); The unsaid (Thought may stop short of its conclusion and leave an action or an image to carry it, as Kawabata does; deep interiority becomes one mode of two, chosen per register); Reasoning from figures (A POV who can read rank or price may reason from readings and figures as evidence, as LitRPG heroes do; every figure still traces to a source (R12-5)).
39. IN3 (Carrying feeling): Held image, never named. In chosen scenes the feeling is never named and one held, concrete image carries it, as mono no aware and han do; R49-07 gains a register-level exception, and the image obeys R5-C2.
40. DS1 (How wide description must range): Lead plus two, thread-checked. Each scene brief names one lead subject group and two supporting ones, the lead rotating scene to scene; session end flags any rotation group untouched for six scenes.
41. DS2 (The land and what lives on it): Yes to: Land, water and sky (Terrain and ground underfoot, rivers, sea and shore, the long view, and the night sky (Shiro, the five wanderers, the Nail, the aurora) join the rotation); Seasons and weather (Thaw, rain, heat, fog and each culture's signs of the turning year join the rotation, beyond R53-09's actual weather in every outdoor scene); Plants and animals (Trees, crops, herbs, blossom, birds, insects, working beasts, and Well-spawn looked at as creatures join the rotation). Not taken: History in layers.
42. DS3 (The public world): Yes to: Architecture as style (Buildings are described for style and ornament as well as use and wear; the Moto 'one thing made that serves no function' finally gets looked at); Dress and adornment (Cloth, cut, colour by rank, wear and repair, jewellery, cosmetics and worn scent join the rotation, past the first-sight inventory); Streets, markets, crowds (Squares, alleys, hawkers, stalls and haggling, arcades and branded goods (R60-07), and the crowd as one body join the rotation); Power on show (Processions and entrances, seating by precedence, courts and punishments (R53-11), Guild halls and academy grounds as displays of standing, and ranking boards join the rotation).
43. DS4 (Home, table, rite and play): Yes to: Households, young and old (Servants and the order of a house, the rich at home as well as the poor, the child's games and chores, and old age at the fire join the rotation); Food and taste (Ingredients, cooking, street food, drink, hunger and rationing, and taste in the mouth join the rotation. How a meal is written is DS8); Rites and festivals (Rites performed on the page, household observance, funerals and mourning, festivals, and folk taboos acted on join the rotation); Music, art and play (Instruments and songs, carving and painting, theatre and storytellers, games of chance and skill, sport and toys join the rotation).
44. DS5 (Culture-keyed noticing): Place supplies, viewer judges. The place's Inventory sets what is in the room; the POV's culture sets what he makes of it, misreadings included. Each Inventory gains a 'Notices first' line for both jobs.
45. DS6 (New Standing Inventory fields): Yes to: Land, sky, living things (Each Inventory gains terrain and climate, the sky by its own names, seasons and their signs, and what grows, is kept, hunted and feared; Temperature joins the senses entry); Building, dress, the street (Each Inventory gains architecture and ornament, the house plan, dress by rank (cloth, cut, colour, adornment, worn scent), and its market and street); Music, play, festivals (Each Inventory gains instruments and songs, games and toys, and one or two festivals written as performed: who does what, and in what order); Law, succession, roads (Each Inventory gains law and punishment (R53-11), succession (R60-21), and roads, vehicles and inns).
46. DS7 (Craft and labour on the page): Process and its beauty. Process as in B, and the finished thing is looked at for its quality: what good work looks like in that craft, through the POV's eye. (Option B there reads: Shown as process. Whenever a craft is on the page, at least one stretch runs as process: tool, material and steps in order, with the worker's body doing them.)
47. DS8 (The table): Order and taste both. The order of serving and the taste in the mouth are both on the page whenever a meal is.
48. DS12 (Money, price and provenance): Yes to: Price whenever money moves (Every purchase, wage, fee and bribe on the page names its sum in the culture's money, quoted from the approved price table; north of the arrays, payment in kind is named as exactly); Its life and lineage (A notable object is described through who made, carried, mended and died with it, the way a famous tea bowl keeps its line of owners; Tier and price stay off unless asked). Not taken: Appraisal by a trained eye.
49. DS9 (Landscape and sky): One wide view outdoors. Every outdoor scene gets one wide view built far, middle and near, with the people small in it, and the sky in it after dark.
50. DS10 (Bodies after first sight): One changed detail each time. Every return of a person carries one detail of what the body has changed since: a new wound, weight, fatigue, cold damage, a missed shave. The Ledger's costs show.
51. DS11 (Repetition against novelty): Recur, and add one. R53-19's two signature items stay; R6-9's 'Novelty is its enemy' is rewritten so every scene also adds one subject the thread has not described, logged as canon (R53-21).
52. DD1 (Overall density): Lush throughout (current). R48-02 stands: full sensory layering in every scene, slower and denser. The blend widens what is described and keeps the amount.
53. DD2 (Where description sits): Woven, pooling in lulls. Texture stays woven through every beat; the longer passages are held for pauses, silences and aftermaths, so the news lands bare and the room is seen in the quiet after.
54. DD3 (Who gets the full inventory): Places full, minors one stroke. Major people, places, rooms, creatures and significant objects get the full inventory; minor people get one exact stroke.
55. DD4 (The order of a first inventory): The POV's order. The inventory stays one passage at first sight but runs in the order this POV would look: a clerk prices first, a surgeon reads wounds first, a rider looks at hands.
56. DD5 (Catalogue or telling detail): Catalogue at set occasions. Arming, feasts, markets, musters, treasuries and loot may run as full catalogues; elsewhere description stays woven. The chain ceiling (R4-14) still holds, so short sentences flank a long list.
57. DD6 (Description inside a fight): Held instant, then outcome. Exchanges run traced and lean; at the deciding moment the page holds still for a passage of setting before the outcome lands.
58. DD7 (Checking the range): Census as a WARN. The census WARNs when a scene touches too few groups or one group takes over half, and the signature-item count extends from Kharven to every Inventory.
59. DT1 (Where comparisons come from): Culture image bank, always. Each Standing Inventory gains eight to twelve set images that any POV of that culture may use whole, unglossed. POV-life comparisons stay the default; R49-20 relaxes for the listed images.
60. DT2 (Colour as symbol, per culture): A colour code per culture. Each Inventory gains a colour field: what white, red, black and two or three local colours mean there, and the chartered Northern houses read heraldry. Narration uses it unglossed; two cultures may read one colour two ways.
61. DT3 (What a season word does): Season words carry mood. As B, and each logged word carries a settled feeling, as kigo do: sap-stop means endings. The scene leans on that feeling and never names it. (Option B there reads: Season words mark time. Each culture's season words may stand in narration and speech, placing the time and weather in one word. Any feeling still comes from the scene itself.)
62. DT4 (Weather and land as persons): Personify at high moments. R49-22 relaxes at mythic moments (R48-05), in verse and documents, and in close POV for cultures whose speech already gives the sky a will. Everyday narration stays plain.
63. DT5 (Wear and age as beauty): Beauty, keyed by culture. Each Inventory states what its people prize in age and what they despise. A Moto or Ketsuen POV may see the mend as beautiful while a Kharven guest sees a cracked bowl.
64. DT6 (Verse inside the prose): Plus a closing poem. As B, and a scene or chapter may close on a short poem set apart, haibun-style. R49-26's legal endings gain the poem. (Option B there reads: In mouths and documents. Verse appears when a character sings, recites or writes it, or inside an in-world document, set as a quoted block the rhythm checks skip.)
65. DT7 (Set idioms in narration): Four-beat idioms, told once. Each Inventory gains six to ten four-beat idioms, each a compressed in-world story. An elder tells the story once on the page; after that the idiom is used bare, in narration or speech.
66. DT8 (Named devices to add): Yes to: Tanizaki light and shadow (Rooms and objects may be described by how they hold low light: lacquer, gold in the dark, oil and paper. Moto shadow and Accord draw-light become a standing contrast); The epic simile (Once per set piece, a held instant may carry a long comparison that grows into its own small scene, and it may reach beyond the POV's life, an exception to R48-04 and R49-19); Ekphrasis, the made object (A made object (a painted screen, a banner, an engraved gorget) may be described at length until it opens onto history or myth, carrying what the narration may not say).
67. DT9 (Forms for in-world documents): Yes to: Lists and loose notebooks (A document may be a list or loose notebook in the Pillow Book manner, a culture's eye compressed into entries; it moves no plot and packs world-only detail. Suits the Moto and Eresse courts); Records of the strange (A document may set down a strange event as plain witness and close on the recorder's own comment, the zhiguai form; folk belief stays uncorrected (R53-15). Suits Guild archives, Well reports and the lineage halls); Court annals and memorials (A day-record by a court recorder the ruler may not read, as Joseon Korea kept its annals, or a memorial (a set-form petition to the throne). Suits the Mahuo houses and the Moto court); Game-reference entries (Bestiary entries, registry sheets and item ledgers in a Guild hand, LitRPG's reference pages made institutional, each figure traced to canon (R12-5, R57-07). Suits the Guild, the wardens and the proof-houses).
68. MY1 (Inside practice): The Crystal as inner map. Practice is written as a walk through the Soul Crystal in Codex nouns, layer by layer, as cultivation maps meridians: where the draw enters, where it pools, where it snags.
69. MY2 (Pressure and aura): Through the room first. Pressure shows first in the room: smoke, frost, lamp flames, the draw-hum, animals; bodies follow. NATALIE's 'a Band gap changes weather' becomes the lead for every gap.
70. MY3 (Intent felt in the body): Intent as aimed Pressure. Killing intent becomes Pressure narrowed onto one man through Dominion, felt as cold, sweat and the pull to step back, and answered by suppression. It needs a ruled mechanism before first use.
71. MY4 (Explaining a working mid-fight): Rules shown beforehand. A working's rules are planted earlier (training, a document, talk), so the fight's explaining is mostly recall and the reader does the sum with the fighter. Self-derived techniques are still read live (R12-3).
72. MY5 (The watching crowd at a power reveal): Spoken chorus, in hearing. At a reveal the crowd may speak in waves inside the POV's hearing: the breath, the name passed along, an elder's verdict. R5-G's reaction-shot tell is struck for crowds.
73. MY6 (How many display beats per scene): One per practitioner. Each named practitioner may take one display beat per scene, so a duel can carry two and a battle several. R9-3-SCOPE's list of triggers stays.
74. MY9 (How a technique's name looks): Yes to: Numbered forms by school (A school's art may run as numbered forms (First Form, Second Form), each named, called and counted; mastery reads as forms held, a ladder inside the art at R8-23's form level); Long names for the halls (Lineage-hall and Korean-stratum arts may carry a four-syllable true name in correct Chinese or Korean, glossed literally (R8-22); R50-11's two-word cap binds new English names only). Not taken: Brackets inside sentences.
75. MY7 (A rite on the page): Numbered rite, set apart. The rite appears as an in-world form in the Guild's house style (R51-33), numbered and set apart; the scene then performs it, and something departs from it.
76. MY8 (How much of the world's magic is shown): Law stated, reasons kept. R12-2 governs what the world does and R48-25 narrows to what people do: rules in the imperative, prices as prices, taboos unexplained. People's workings keep full mechanism.
77. LR1 (What an instrument can show): Printing instruments. Assay coils stamp a paper tape or punch a card, as a ticker or tabulator does, so a set-off block on the page is that tape, in the instrument's own type.
78. LR22 (Where a screen comes from): Read in the Crystal. The bearer reads his own Soul Crystal as plain, voiceless lines at thresholds: his own sheet only, exact, and blind to wounds and to others. Small new canon; instruments still read everyone else.
79. LR2 (Who can read whom): Practitioners feel rank. Any practitioner feels his own Grades and Stage, and another's Band and rough Stage, with Gnosis setting how close. Another's exact figures need an instrument; commoners keep their folk words and their awe.
80. LR3 (How a readout sits on the page): Inline, blocks at milestones. Figures inline by default; a set-off block only at a re-assay that moves something, a breakthrough or an arc's end. Blocks become events, rare enough to land.
81. LR4 (The voice of a readout): Clinical, wit in margins. The instrument stays clinical, and any wit lives in the clerk's or Measurewright's note beside it. Humour stays in a person, never in the readout, and R5-D stands.
82. LR5 (Numerals for the ladder's rungs): Numeral beside name. 'Stage V, Splintering' and 'Band II, Awakened', as FOW writes them. Tiers of Standing and item Tiers keep their names alone. R47-7 is amended.
83. LR6 (Figures in plain narration): What the POV knows. Narration states the figures the POV holds: his own last reading, the card he has seen, what he was told. R49-52 governs R49-47; R14-4-SUBSTAT retires; NATALIE.md is rewritten.
84. LR7 (Growth moments that earn a readout): Yes to: Level gained (A short readout when a Level lands, with the stat points it brought. The genre's heartbeat, and the most frequent of the four); Stage breakthrough (A readout naming the new Stage and its Tier of Standing when the Catalyst completes. The cultivation novel's big moment); New Trait (A readout naming the Trait when it registers. Rare, and each one changes what a character can do); Wellspring contact (A readout at first contact with a new Wellspring current (FOW's Resonant Surge) and at a harmonisation. Growth tied to a place).
85. LR8 (In-scene moments that earn a readout): Yes to: Appraisal (Reading a person, beast or item: the Measurewright at the rail, the coil at the counter, a faculty. The genre's appraisal in WOTR's hands); A wound (A diagnostic line in a surgeon's terms: the structure struck, the ATLS class, the minutes left. Brida's 'third bowl' as a readout); Essence spent (A reserve line after a working: what was drawn and what is left. R60-03's hard reserve clock made visible). Not taken: Pressure.
86. LR9 (How many readouts a scene carries): Display, finisher, aftermath. Up to three per scene, on R48-20's rhythm; a roleplay turn carries two at most, never two in one exchange.
87. LR10 (Readouts and the two-voice cap): Outside the cap. A readout states figures and explains nothing, so it never counts; two voices still do the explaining, and the reader checks the call against the figures.
88. LR11 (Numbers inside a fight): Grades at the read. The POV's read names Grades and gaps before or between exchanges, as estimates in her own terms; no running figures. The genre's sizing-up without a log.
89. LR12 (Body first or number first): Body, then number. The body first and the readout in the same beat, a line after. Both on the page together, with the body always ahead.
90. LR13 (How fast the numbers climb): Event-bound. Numbers move only for a cause the reader was shown: a FOW XP event on the page, or training named in a downtime turn.
91. LR23 (A breakthrough on the page): In the crisis, line after. It happens inside the danger that is its Catalyst, written from the body; the line lands as the danger breaks and the Catalyst completes, never mid-exchange (LR11). R9-3's splash beat goes to the crisis.
92. LR14 (Confirming a new Stage): A public re-assay. The re-assay is a rite before witnesses, read aloud and entered on the Reckoner's roll: the sect's ranking ceremony, in WOTR's institutions.
93. LR15 (Build talk in dialogue): Ranked practitioners too. Any ranked practitioner talks his own and others' numbers exactly and argues builds, as in Unbound; commoners still round. R52-05 widens.
94. LR16 (Gamer slang): Speech, by ear. Current law: gamer slang in a mouth whose voice would carry it; narration stays timeless. verify_scene adds these words to its narration watch-list.
95. LR17 (Item cards): Item card, once. A set-off card at purchase or appraisal: Tier, Latin form, Grade band, maker, stamp, price, one line of lore. Once per item, never reprinted.
96. LR18 (Titles and achievements): Guild commendations. The Guild may also enter a commendation on a registration and strike its mark on the token: legal and social weight, no stat effect. Third Names carry on as now.
97. LR19 (Quests and contracts): Contract boards. Guild and Crown contracts posted with terms, pay and the clearance register: the quest board as a Draw Age notice. Hooks gain a stated reward and penalty.
98. LR20 (Sheets at chapter and arc ends): Changes at chapter end. Each chapter closes with a short block of what moved and why, above the notes; roleplay turns keep it in the notes.
99. LR21 (A number not yet in canon): Print the estimate, marked. The readout prints the figure with the instrument's own hedge (a range, 'uncertain past the third place'), and the notes log it as estimate.
100. CB1 (Which martial vocabulary names the moves): By the POV's own school. Narration names every move in the POV's own training (a Moto POV calls a diagonal cut kesa-giri, a Greymane POV a Zornhau); a foreign school's word arrives in a mouth. verify takes per-school lists.
101. CB2 (Declaring name and line before a duel): Full declaration, with a price. Full declarations are legal but count as the scene's crafted speech under R48-43, and the world does not wait: an opponent may close measure, or shoot, while the recital runs.
102. CB3 (Stillness, traced passes, or the long fight): Shape follows the grammar. A rule ties duel shape to the four combat grammars: Verdict still then one cut, Blade traced passes, Percussion and Expenditure by attrition; practitioners escalate while reserve lasts. R60-01 holds for the unranked.
103. CB4 (Memory inside a fight): Full flashback, POV only. The POV may take a full flashback, a page or more, frozen inside one turning exchange, once per fight. The POV lock holds; the opponent's past reaches the page only through what the POV knows.
104. CB5 (The rival bond): Rivals who chose to spare. A rival may recur, but each survival is a choice someone made and paid for on the Ledger: a debt, a scar, a witness to the mercy. R48-31 stands.
105. CB6 (What joins the wound when a fight ends): Rites and image, by culture. Both, keyed to culture: Japonic, Korean and Chinese killers carry the rites; the elegiac image belongs to any POV whose culture mourns that way. The clinical floor holds everywhere.
106. CB7 (How a battle is told): Hill and ditch, cut. A battle cuts between the commander's hill and one man in the press at marked breaks, each section POV-locked; the breaks stand in for the guide's rule to 'pass through Line'. R1-3's three heads cover both.
107. DL1 (Speech levels and address for the Korean and Chinese strata): Native words and level shifts. Native address words as in B, and level shifts written as events as in C. R23-10-CHINESE_PHONOTACTICS still bars stacked honorifics inside names. (Option B there reads: Native address words. R51-21 extends: Korean speakers use their own address words (-ssi, polite; -nim, honoured; sunbae), Chinese theirs (shifu, shixiong, qianbei, an elder of another school), romanised and never italic.) (Option C there reads: Levels carried in English. No foreign address words beyond the Japonic houses; speech levels live in English grammar (bare orders against full courteous forms), and a shift of level is written as an event the room hears.)
108. DL2 (How Eastern-register speech sounds in English): Translated forms for ceremony. Natural English in daily talk; the translated forms (self-reference, set formulas, idioms word for word) come out at ceremony, challenge, oath, court and insult, where the shift into them is itself a beat.
109. DL3 (Proverbs in speech): Duels, by age and standing. B, keyed to standing: elders, headmen and court speakers argue in sayings; the young speak plain, and a youth who quotes above his years is put down for it. (Option B there reads: Proverb duels. NPCs carry several fixed sayings and may argue in them at bargain, quarrel and council, a saying answered by a saying. R52-30's 'one' becomes 'several'.)
110. DL4 (Verse exchanged in talk): Each culture its own contest. B, plus the north's own form: Northern English and Norse-register speakers may answer in alliterative insult verse (flyting). Each culture's verse form is entered in its Inventory. (Option B there reads: Courtly cultures trade verse. The Moto court, Eresse, the Mahuo houses and the lineage halls may offer and answer verse at rites and in court; a weak answer, or a plain one, costs face.)
111. DL5 (Long formal speech and the clipped line): Long speech at court. Court cultures (the Moto court, the Accord chancery, the Mahuo houses, the lineage halls) argue in long formal speeches as their normal register; Kharven, saga and soldier speech stay short. R48-43's cap holds outside court.
112. DL6 (Face, and the face-slap): The face-slap, with a bill. C, with a bill: every public reversal opens a Front or a Ledger debt (a vengeful house, a witness, a feud), and the humbled man stays veteran-clever afterward. (Option C there reads: The face-slap licensed. The face-slap becomes a legal payoff: an arrogant scion underestimates, the reversal is public, the room reassesses. R5-C1-WELL_REASONED_WRONG_CONCLUSION and R48-36 relax for the arrogant, who may misjudge badly.)
113. HU1 (The double act and the comic beat): Full beats for comic voices. Full comic beats, retort and reaction included, belong to comic voices and double acts named on their cards; everyone else stays under R5-D.
114. HU2 (Grimdark and warmth): Warmth as counterweight. Each live thread carries at least one standing warm bond (found family, master and disciple, sworn kin) written openly warm, and joy may get scenes of its own. Losses still cost.
115. HU3 (Tears and sentiment): Break at a small thing. A rule adds the delayed break: restraint holds through the big moment and gives way, fully and openly, at a small unexpected thing. Once per character per arc.
116. HU4 (Comedy beside danger): Comedy hard against dread. Comedy and dread may be set hard against each other by design (domestic farce, then the thing in the dark), each played straight; jokes inside the danger stay gallows wit.
117. NE1 (Sobriquets and hall titles): Sobriquets and title ladders. B and C together: sobriquets spread by use, and the halls stack their titles in formal address. R23-10 holds for given names only. (Option B there reads: Sobriquets in common use. Criers, crowds, ballads and enemies may hang lesser names on any notable fighter; most fade, and the one that sticks becomes the Third Name. Your characters' names still stick only if you keep them.) (Option C there reads: Hall title ladders. The lineage halls run a full title ladder (Hall Master, Elder, Senior Brother, first disciple) that may stack in formal address; R23-10's bans lift for titles and hold for given names.)
118. NE2 (Honorifics in narration): The POV's own honorific. A close POV from a culture with honorifics carries them into narration (Kaname-sama, Seo-nim) as he would think them, never italic; a Western POV in the same room uses plain names.
119. NM1 (How much of the pool is comic): Most commons and soldiers. Comic bynames and nicknames become the norm in musters, crews, taverns and markets. Above the commons they thin out, and NM4 sets how high they reach.
120. NM2 (Built comic names): Yes to: Rhyming and alliterating sets (Kin, crews and sworn pairs share a name-part and change the sound, Borin and Snorin style, inside each culture's own sound rules. A set meeting is a beat (R50-17)); Dickensian talking surnames (Surnames that tell a trade or a nature one notch past believable, as Gradgrind did: the Victorian imperial register R53-28 already sets, for Northern and Accord families); Plausible puns, Pratchett-style (Surnames that pass for real ones, with the pun underneath or turned against the bearer. Built from words the Draw Age owns, so no brand, celebrity or modern-world reference). Not taken: Phrase and sentence names.
121. NM3 (Grown comic names): Yes to: Soldiers' nicknames (Deed and body bynames from comrades, literal or ironic, the way Abercrombie's Logen Ninefingers counts his missing finger. Peers coin them, so the joke belongs to the characters); Mangled names (A name or phrase bent by a foreign mouth and written as heard, a real mishearing every time (R20-4). Canon already does it: the Dawi say Porin, and Common mouths make it Borin); Sound comedy (Names funny for their noise: hard k sounds, doubled syllables, a goblin mouth's extra consonants. Built inside each people's own sound rules, and most at home among the goblinoids); Protective ugly names (A child given a cheap or ugly name so death passes it over, as Chinese and Korean families did; R23-5 already allows a name given 'as an insult or a shield'. Comic to outsiders, grim at home).
122. NM4 (Who may carry one): Plus villains. B, plus villains and rivals, in the Jonson and Dickens line (Volpone the fox, Uriah Heep): a comic name on a dangerous person. Major NPCs keep strict names. (Option B there reads: Plus recurring NPCs. Recurring minor NPCs (the innkeeper, the sergeant, the Guild clerk) may keep comic names across scenes. Villains and major NPCs stay strict.)
123. NM5 (Whose ear hears the joke): English puns with a bridge. An English pun is legal where the world supplies a bridge: a Common mouth, a byname rendered in English, or a Common ear mishearing. Reader-only puns hidden in a foreign name stay out.
124. NM6 (Which peoples: West and North): Yes to: The Dawi (Rhyming sets on a shared bank element, deed bynames rendered in English, and outsiders' mangling. Given names stay bank-built; the joke lives in sets, bynames and other people's mouths); Kharven and Far-Northern (Bynames from the Kharven stock of scarcity insults, protective cheap names, and roll-names (surnames an Accord clerk assigned). No joke on the name of the recently dead (R23-11)); Accord and Northern commons (The richest home: talking and phrase surnames, rhyming pet names (Hob and Dob), soldiers' bynames, and Accord jokes in correct Latin (R50-12)); Goblinoid peoples (Sound comedy, and bynames whose cause nobody remembers, so a dreaded name can arrive with no story behind it).
125. NM7 (Which peoples: the Eastern strata): Yes to: Retainers and household staff (Retainers and servants of the Japonic houses take calling-names from real Japanese trait-words, and sound puns on real words, glossed once by a character); Bloodline cadets, bynames only (Servants and rival Lines coin comic bynames for new cadets of the archaic houses, behind their backs; given names stay under R40-1. No carded Moto is touched, Sodoku least of all, and no Büri form returns); The Mahuo (Korean-register names chime through the generation syllable (one syllable every cousin of a generation shares) and can land on a real Korean word; children may carry ugly milk-names. Real Korean only (R50-01)); The Chinese lineage halls (Self-awarded studio names (a scholar's chosen art-name, which other houses mock), insulting posthumous names, cheap child-names and spoken homophone puns. Nothing that needs a written character to land).
126. NM8 (Borin Ironheart's rhyming kin): Brothers, Snorin included. Natalie invents Borin's brothers on the shared Rin, one called Snorin by every Common mouth, and adds them to his card's kin line once you approve the names.
127. NM9 (A comic name, a grim end): The name turns to grief. Someone says the comic name at the death and the joke becomes the wound. Among the Kharven the name then goes unspoken until it is given on (R23-11).
128. NM10 (Places, inns, ships and gear): Yes to: Inns, taverns and shops (Signboards and their regulars' nicknames carry the joke, in every culture's towns); Streets and places (The commons' names for streets, fords and districts sit beside the official ones, one per culture (R50-22). The Accord's Latin name stays grave); Ships, sledges and engines (Crews' names for vessels, sledge-teams, draw-engines and gun-carriages, beside whatever the registry wrote); Weapons and items (Weapons and gear take soldiers' folk names beside their true names (R50-13): the true name in the maker's tongue stays grave, and the folk name may joke. Technique names keep R50-11 and R8-22).
129. NM11 (Who notices the joke): Close POV may notice. The POV's own head may register the joke in his own idiom, as he would think it. The narrator outside him never remarks, so R5-C1 stands.
130. NM12 (Walk-ons with comic names): Nickname in a mouth. A walk-on may be named at once only by a nickname in someone else's mouth; the narration keeps the role until R50-27 is met. A walk-on named for a joke does not die in that scene.
131. NM13 (How comic names get made): Yes to: A comic bank per culture (Each Standing Inventory (the per-culture texture file) gains a comic-name list of bynames, nicknames, rhyming sets and signboards, built in that culture's sound rules); By ear, sound-checked (Natalie coins comic names live; the scene-end check passes each as an outlier (R50-18) so long as it keeps its culture's sound rules, and flags any that break them). Not taken: A floor per crowd scene, A pitch list per session.
132. NM14 (How far the naming law bends): Banks gain comic slots. B, plus each culture's naming rows gain a comic-names clause pointing to that culture's comic bank in its Standing Inventory, so load_rules serves the bank with the law. (Option B there reads: Narrow amendments. Only the rows your answers above bend are amended, each in one line naming its answer: R50-30 for the sound check, R50-27 only if NM12 opens walk-ons. Banks and sound rules stand.)
133. XS1 (Eastern techniques beside clinical specificity): Yes to: Season and nature imagery (An explicit scene may set a season or nature image beside the anatomy (frost, snow, blossom, the brazier), carrying mood without replacing the plain words); Held detail at the peak (At chosen moments, usually the peak, one held physical detail may carry the beat; plain specificity governs the rest, and the aftermath is still written); The poem after (An explicit scene may close on a written or spoken exchange (a morning poem, a note, a line answered) as part of its aftermath beat); Mimetic words (Mimetic words for texture and state (the Japanese gitaigo habit, and each culture's own) join table rule 9's onomatopoeia, romanised and never italic).
134. XS2 (Keyed to culture or free): Keyed to the POV. The POV's culture decides: a Moto POV writes with image and the held detail, a Kharven POV blunt, whoever the lover is; the lover's culture shows in what they do and say.
135. ME1 (Where the new law lives): A, plus new guide editions. A, then new editions of the Master Style Directive, Combat Craft Guide, Dialogue Craft Standards and Scene Writing Process Guide, so no companion document still teaches the old law. (Option A there reads: Rule doc and NATALIE rewrite. One dated Style Law doc logged through log_ruling; NATALIE.md's models line and Prose Standards rewritten to it; R5-A-FLESH_CHANGES, R5-E-MARTIN_WINS_RULING and R11-1 superseded or amended as K1 decides.)
136. ME2 (New checks in verify_scene): Yes to: Combat words by school (verify --combat takes a school (blade, japanese, chinese, korean, percussion) or reads the culture tag, and warns only when a fight carries none of that school's terms); A verse marker (A marked verse block (a poem, a lament, a declaration in lines) is left out of the rhythm statistics and word count; the dash and hard-ban checks still read it); Stock-formula watch (A WARN on translated web-novel formulas (you court death, this junior, this old man, lose face) in narration, and an info line in speech, so the flavour stays where DL2 puts it). Not taken: Address check.
137. ME3 (The archived scenes): Leave them, tag the edition. The archive stays untouched, and scenes/MANIFEST.md gains a law-edition column so the drafting tools and scene_recall stop treating old style as precedent.
138. ME4 (Proof and the order of work): Law, test scene, then bank. The law is logged live; one test scene in a live thread follows; anything that reads wrong becomes a dated amendment; then a sample bank for Kharven, Moto, Accord, the Mahuo and the lineage halls.

Context: Isaac answered all 138 questions in Claude Code chat on 2026-10-03 and said 'go'; the rows are applied as R70 (rules/doc-style-law-2026-10-03.yaml) in the same session.

## 2026-10-04 — combat-law-2026-10-04

The combat and alchemy questionnaire (105 answers), Claude Code chat.

Isaac's direction, in his words: "Let's do a questionnaire for magical combat and combat in general and how it's written etc along with applications of alchemy and different wotr things and some research on different styles of combat writing etc". Each line names its questionnaire id; the questions, options, sample passages and the research behind them are in imports/drafts/combat-questionnaire/. Prose questions were answered in a picker with samples; the rest were taken as section digests (the recommendation accepted). The rule rows are rules/doc-combat-law-2026-10-04.yaml (R71), whose id numerals are the numbers here. WT4 rules CONFLICTS C-001.

1. K1 (Where the line falls in a fight): Western body, Eastern read. The exchange, the wound and the cost stay Western and clinical; the read, the stillness before the cut and a rule's reveal run Eastern, long and deductive, the Naruto and Bleach way. The next Combat Guide writes it in.
2. K2 (Eastern combat models): Yes to: Togashi, Hunter x Hunter (Fights as logic: the opponent's rules inferred from evidence, tested and exploited, and the winner is whoever knows his own limits best. Its vows that trade a limit for power wait for MC6); Gu Long, the one cut (The duel is the wait: the long read and a single exchange, the floor paid on the body. Becomes the named model for Verdict grammar (read, rank, commit); FT16 asks whether the cut itself is seen); Inoue and Yoshikawa, Musashi (Inoue's manga Vagabond and Yoshikawa's novel Musashi: the deciding event happens inside the fighter (fear, the fixed mind, no-mind), with pages of breath and footing. A model for Japonic POVs); Akutami, Jujutsu Kaisen (Domain clashes decided in a stated order, with the burnout after a Domain as the counter-window. FOW Part Twenty-Two already sets the order; burnout and the sure-hit (a Domain that cannot miss) would be new canon).
3. K3 (Western combat models): Yes to: Cornwell, Sharpe (Volley drill, powder smoke, the stormed breach, tactics explained in the action by a sergeant's read. The only model for the gunpowder battle the archive has never written); Sanderson, hard magic (Rules planted before, physics as choreography, costs and counters findable, so the reader does the sum. Already close to R70-71's rules shown beforehand); HEMA novelists (Christian Cameron and Sebastien de Castell: armoured fights from inside the steel, the phrase (one unbroken attack and answer), joints, the visor slot, the ground. The Western school's model). Not taken: O'Brian, Aubrey-Maturin.
4. K4 (How far from the floor): Floor by grammar. Rescaled as in A, and each grammar pays the floor its own way: Verdict states the read before and the mechanics after, on the body; Blade pass by pass; Percussion and Expenditure carry the cost every exchange. (Option A there reads: Rescale, same ratios. R13-4-DENSITY_BUDGET is rewritten for today's lengths: full floor at first display and finisher, items 1 to 4 at every exchange that turns the fight, item 8 at a turn's close. Every item stated where it happens.)
5. K5 (Roleplay turns against written fights): Standing orders honoured. You may post conditions ('if he closes, I cut low'). Natalie runs them exchange by exchange until the first branch they do not cover, then stops on that threat. Table Rule 1 gains this exception.
6. K9 (A player's fighter on the page): Yes to: Wounds as world facts (Once your stated move resolves, the hit, the wound by structure, its ATLS class (the trauma surgeons' blood-loss scale) and what the hand can no longer do are written as world facts; how he bears it stays yours); The tell placed, the read his (Natalie puts the evidence in the room (the heel, the smell, the needle) and never draws the conclusion; the deduction, floor item 3, is your post, as CW14's D already leaves the reading to you); Felt from across the room (From an NPC's POV a player's fighter is only what that NPC's eyes, body and room register, the Geturo model; his reasons and his Crystal stay dark. It covers guest players at the Discord table too); Outward cost only (Natalie shows what his working costs where others could see it (heat off the skin, thaw at his boots, R48-37) and keeps the spend in the Stat Ledger (the running figures in the notes); the inside is yours).
7. K6 (When the reader sees the call): Deciding fact in the read. The fact that decides an exchange shows beforehand in the POV's read or a second's mouth, as behaviour or a Grade estimate, so a sharp reader can call it. The notes still name the row.
8. K7 (The core promise): A way out, always planted. The world stays honest, and every fight Natalie stages has at least one findable line out (a counter, ground, flight or a yield), planted where you could catch it. The guide opens: fair, computable, costly.
9. K8 (LitRPG combat models): Yes to: nobody103, Mother of Learning (The prepared fight: scout, learn the enemy's tools, then a short, legible final attempt the reader can check. Its time loop stays out, since death is permanent; R70-71 and R12-3's study counter are its home); Dinniman, Dungeon Crawler Carl (The room as the counter: a gas, a drop, a cut main beats the boss; bosses that change their rule mid-fight; grief arriving cold after the jokes. Comic beats stay with carded comic voices (R70-113)); Zogarth, The Primal Hunter (The bench wins the fight: poisons and coated shot prepared days before, the dose counted toward its effect, the dying long. Its time-stopping sense would need a ruled mechanism and stays out); SenescentSoul, Delve (Drain-rate tension: the reserve clock worked out so the reader knows when a fighter will cross into Starvation (below a tenth of his reserve). The figures stay between exchanges and in the notes, under R70-88's no running figures).
10. CW1 (Counting back the small exchanges): Count back the minor ones. R48-33 is amended: exchanges that change nothing may be counted back in one sentence, each named by its move; any exchange that lands, shifts measure or reveals something is traced with the floor.
11. CW2 (Running fast): A staccato run, once. Once per fight, in its swift stretch, one short paragraph of short, even sentences is exempt from the run rule, and the notes mark it. R4-14 is partly amended for fights.
12. CW3 (Keeping space trackable): Fixed at the deciders. A scramble (a crowd, the dark, a fall) may blur position while it lasts; every exchange that decides something re-fixes both bodies before it lands. Chaos is legal, the deciding geometry always clear.
13. CW4 (Superhuman speed): Yes to: The effect arrives first (Speed shown through its physics: the pressure front, the crack after, the wound that opens once the swordsman has passed. Held to FOW's speed rows for the Grade on the card); Felt time, by Reflex (A POV whose Reflex Grade outruns the threat gets stretched time on the page, held to FOW's Reaction Speed row for that Grade; a slower POV gets only the gap. Sits beside R70-57's one held instant); The gap in the frame (The body is simply elsewhere, nothing drawn between two poses; any after-image is disturbed snow, dust or frost, never a glowing double (R9-3 keeps 'it glowed' banned)). Not taken: The witness who misses it.
14. CW5 (Impact and momentum): Momentum accounted for. At display and finisher the page says where the momentum went: what anchored the striker, whether the target was thrown or broken, what the ground took. The physics audit checks it; stock images move to a bank per culture.
15. CW6 (Fighting on through a wound): An Essence splint, priced. A practitioner may hold a broken structure shut with a working: Tempering for how long, a reserve cost per turn, ending at Starvation; the wound is worse afterward. Needs a ruled mechanism before first use.
16. CW7 (How long the page stays on a wound): Length by scene type. Exchanges stay precise; a finisher, an execution and a battle's one full-detail body get the lingering passage; roleplay turns keep it short unless the death is the turn's point.
17. CW8 (Fear in the body): Owed for the untrained. An untrained POV's fights carry at least two fear effects in the body, traced to adrenaline; trained fighters keep composure free (R52-28) and show it only under real strain or Pressure.
18. CW9 (What a fight sounds like): The native word at impact. In fights the POV culture's own sound words (R70-22) carry the impacts, entered in its Inventory first; comparisons are kept for the held instant. Each culture's bank gains a few fight words.
19. CW10 (Ground and weather in the fight): Yes to: An environment row (The adjudication table gains a row: footing, light, cold, wet and Aetheric Density bend named stats, and the author notes say which. Weather stops being texture only); Ground chosen before contact (Every planned duel opens with the fighters reading or choosing ground (Counterplay's 'Pick before contact'), and the ground decides at least one exchange). Not taken: New ground, by rotation, Texture only, as now.
20. CW11 (How fights end): Yes to: Yield on terms (Surrender is legal and binds by the culture's custom (a Kharven word before witnesses, an Accord form under seal); the terms go on the Ledger as R70-104's debt); Flight, adjudicated (Breaking off and running is always a choice; pursuit is decided on Dexterity (Celerity), the reserve and the ground (FT12 shapes the chase), and a fled fight leaves a witness and a debt); A code ends it (Formal duels run under the culture's code, with seconds and a stated end (first blood, a disarm, a yield); the code's stop binds both men, and breaking it is a Ledger debt); The killing's own law (Every killing carries its culture's legal aftermath (a declaration, a blood-price or labour-debt, outlawry) on the page, opened as a Front or a Ledger line).
21. CW12 (The aftermath on the page): Procedure as craft. The dressing is written as process: the period kit for the place, the healer's hands, the bleeding clock closing, what this place's medicine cannot do. R70-46's craft-as-process reaches the infirmary.
22. CW13 (Talk inside the fight): Talk as a weapon. Taunts, lies and accusations are moves: each line aims to break the read or the temper, and the page shows what it bought or cost in tempo. Gallows wit stays the only joke.
23. CW14 (The tell and the read): Shown twice, then read. The tell is shown plainly at its first and second appearance and read at length at the third, matching NATALIE's two or three exchanges of evidence. When the POV is your PC, the reading is yours.
24. CW15 (When the rows come out level): Rule 5's order, step by step. The read decides first, then what each has left to spend, then the ground; the notes name the step that broke the tie, as a Domain clash names its step. Every level exchange reconstructs.
25. CW16 (Wounds carried into the next fight): The anatomy, not the stat. No Grade moves. The wound's structure decides what the body can do (a stitched forearm cannot hold a hard bind, a cracked rib cannot take a deep breath), checked by the gap-fill body audit and named in the notes.
26. CW17 (Counting rounds, vials and charges): Counted as the POV counts. A trained hand keeps his count and the page keeps it with him; a panicked or untrained man loses count and the reader with him. Objects only: stats and the reserve stay under R70-88.
27. MC1 (A spoken working in the exchange): Cut into the exchange. The chain is printed in pieces between the opponent's moves, so each clause costs a step he takes. The Combat Guide gains the rule; the reader watches the race and can count its price.
28. MC2 (What decides casting speed): Row now, cards override. The Alacrity row decides every race today; where you fill a card's Readiness, that figure governs. Nothing waits on figures, and precision grows as cards are filled.
29. MC3 (How often an art is released): As often as beats allow. R50-09 governs and R8-26 is marked superseded. Every call costs its beat and buys its output, so a fighter may call his art again whenever he can afford the beat.
30. MC4 (The held-back reveal): Shown before, told at reveal. This reopens R70-71 for held reveals: the rule may act earlier, unexplained, as evidence a reader could catch, and a voice tells it at the reveal. The notes list each planted sign.
31. MC5 (Counters at duel scale): Soft Family chart. A chart derived from Codex physics says which conditions and Families make each Family's working cost more and deliver less; the card's Counter field stays the hard answer. You ratify the chart.
32. MC6 (Vows and limits): Narrowing buys output. A vow that narrows a technique raises its output through Attraction Force, by a figure you set on that card; breaking it is a Shear Break. The vow's terms are its findable counter.
33. MC7 (How the drain shows): Yes to: The body, by threshold (A bank of body signs keyed to the Ledger's lines, committed spending and Starvation: cold hands, tin on the teeth, the slow grip. Logged by culture, so the nosebleed stops carrying everything); The waste grows (As η (eta, efficiency) falls, the same work sheds more heat, so the room shows the drain: the thawed ring widens, the air shakes harder. Canon's own law, written as a rule of the page); The opponent reads it (The drain is shown through the other fighter's read and his choice to make the spender spend. The Counterplay doctrine, on the page). Not taken: By Family.
34. MC8 (Overchannel on the page): Felt now, measured after. The crack is felt in the exchange, inner map and body symptom; its size comes later from a surgeon or an instrument, and the Ledger enters it when measured.
35. MC9 (The second wind): Decides, if planted. It may land at the deciding exchange only when its trigger was set up earlier on the page where a reader could catch it, and its price goes on the Ledger. Rare by rule.
36. MC10 (Healing inside a fight): Stop the bleeding only. Mid-fight Vitalia may close a vessel or seal a bleed, at full price; the wound itself stays open until the fight ends. §7.1 gains the row.
37. MC11 (Traits when they fire): Named at first fire. Narration names the Trait the first time it fires in a scene, then shows it working. The reader holds the name the way he holds a technique's.
38. MC12 (A Resonant Pair under strain): For the crisis only. Where a Sub-Stat sits at its Stage's cap, strain may lift it level with its partner, and the Pair runs for the crisis, then goes. The notes name the strain.
39. MC13 (Allies working together): Drilled forms, carded. Allies chain by default; a fusion exists only as a carded Synergia technique the pair learned together, with its own cost split and counter. No improvised fusion.
40. MC14 (The mechanism of aimed Pressure): The field narrowed. Dominion draws the Passive Pressure Field onto one man; what he takes, the room loses, so the room eases as he suffers. The trade's figures come from Dominion, set by you.
41. MC15 (Pressure on the unwoken): The Aura table, by Grade. Practitioner against practitioner keeps the Stage ladder; the unwoken take Part Eleven's Grade table: dread from F to D, weight in the room from C, knees bending from A. No new figures.
42. MC16 (Two Pressures in one room): A contest for the room. Meeting Pressures fight for the room by Dominion before steel; the room shows the border moving, bystanders take both, and the loser begins the fight already paying. §7 gains the row.
43. MC17 (Suppression on the page): Yes to: The cost in his body (Holding it in tires him in named places, jaw, collar, temper, and the cost grows with the approach. The Combat Guide gains a bank of signs by culture); Small leaks in the room (R70-69 at its faintest: the draw-hum dips and a dog lies down as he passes. A sharp-eyed reader, or a POV with good Gnosis, can catch a suppressed man); Instruments catch it (A gauge or coil reads what eyes miss; the Board's clerks and the Measurewrights can find a suppressed man by the sag he leaves on a needle).
44. MC18 (A faculty read on a man): Exact unless warded. A faculty prints exact figures where the reader's Gnosis Perception outranks the target's Resilience Ward by Grade, and a hedged range where it does not. §7 gains the row; Ward is the counter.
45. MC19 (Raising a Domain in a duel): Attention, then held in. Below Stage XI it rises by attention as in A. From Stage XI, where canon has it leak, suppression holds it in and the holder lets it go in a beat. Originated; you rule it. (Option A there reads: Raised by attention. Part Twenty-Two read plainly: the holder concentrates and the Domain comes up over turns, unnamed, at a cost the notes track. Its rising joins R9-3-SCOPE's triggers as his display beat.)
46. MC20 (A Domain clash on the page): The moving border. The seam between two laws shows in the room and moves; one voice names the deciding step once. Reconstructible, and paced like an exchange.
47. MC21 (Showing the scale): Yes to: One street beat (At a marked break, one commoner in the street gets a short dip inside her head, then the lock resumes. Scale seen from the ditch, by R70-11's device); The aftermath walk (The scale is shown after, walking the ground (R57-24). The fight stays tight; the ruin tells the size); The claims come in (Lives and property go on the Ledger as claims, settled in a later scene at the Accord's schedule, as R54-15 lets a later scene pay an aftermath. WT10 asks the fighter's own bill). Not taken: A report sizes it.
48. MC22 (Waste light, outside a display): Incandescent, by physics. Waste light is written by the smith's colour scale, dull red to orange to white, and by what it lights; brightness tracks η, so masters work darker. The word glow stays banned.
49. MC23 (A summon's display beat): Native summons earn one. A Native summon, with its own Crystal, takes its own display beat; Donated and Analog forms share the summoner's. Provenance decides, as the Register's doctrine says.
50. MC24 (Shot meets a worked cuirass): By inscription, read on plate. Each inscription stops shot its own way and leaves its own mark from §4.6, so the shooter can read which working he faces and which round to bring next.
51. FT1 (The skirmish of three to ten): Duel floor, mass compression. Amends R1-4: the POV's own exchanges carry the duel floor, and everyone else's fighting is compressed by the Mass Guide's rules. Her count of who still stands stays in her head, never as figures.
52. FT2 (Ambush and the named round): Both, split by a break. A marked break splits the wait from the shot, each half POV-locked. In roleplay the shooter's half is one turn's closing cutaway (R49-09), and the shot lands in the next turn.
53. FT3 (Brawls and folk schools): Folk schools, by culture. Each Standing Inventory's Words entry gains its wrestling and fist words, entered and logged; a POV raised in them names moves in them, and verify gains a list per culture.
54. FT4 (Bouts at Aetherion): Posted terms, warden backstop. Each bout's terms are chalked before it (yield, ring-out, a wound by class). Fighters may push right up to them, and the warden's gauge stops only what the terms never priced.
55. FT5 (Duels to first blood): Terms hold, the body doesn't. The duel stops at first blood, but the wound is tracked like any other: where the point lands decides whether it is a nick or a death, and the Ledger keeps what follows.
56. FT6 (The shape of a monster fight): Yes to: The hunt as procedure (The fight is won at the shaft head: reading the draw, choosing the entry's counter, laying out the kit. The kill is short and the work is the scene); Phases at the tie (A beast's fight turns (a boss phase: the monster changing form mid-fight) only at a lever canon gives it: its tie cut, its Wellspring's failure induced. The rung drops on the page; an untraceable phase fails R13-8). Not taken: A duel with a beast.
57. FT7 (Appraising a beast): Both, and the gap. The tape prints rung and Commission tier together, and where they disagree a voice names the gap, because canon puts the hunter's answer there. It counts as one of the scene's three readouts (R70-86).
58. FT8 (One shot at a practitioner): Each shot traced. A shot is traced like an exchange: range, the ball's speed (R45-1's reference figure) against the Speed Grade the POV reads, the result, the cause stated under R53-05. Rounds left are counted as CW17 rules.
59. FT9 (Practitioners as artillery): Battery with a spotter. An ordinary commander directs the practitioner like a gun; a Measurewright spotter in the line reads the effect on her gauge. R3-9 stays whole, and each section stays POV-locked across marked breaks.
60. FT10 (Volley, smoke and the drilled line): Yes to: Drill and smoke (A section on loading by numbered motions, smoke that blinds after the first volley, fire by platoons down a line, and squares against horse; the ditch sees smoke and hears the count); Spread against a practitioner (A section on Counterplay's doctrine: men drilled to spread, make him choose and keep a line of fire open, so numbers correctly used beat a practitioner at a stated cost in men); Enhanced-shot companies (A section on elite guard and bounty companies with full pouches of enhanced shot (R53-04): each round priced, made and findable, fired only at practitioners and only on a named order). Not taken: Guns and the late gun.
61. FT11 (A siege with practitioners in it): Ward breach as a break. Amends R3-8: a ward failing joins sortie, mine and storm as a Close Register break, sudden, from a POV on the wall, and over fast; the Line Register resumes after.
62. FT12 (Chases and pursuits): Yes to: The reserve race (The chase is the reserve clock: every burst of speed is spent, both bodies pay, and whoever runs dry first loses. The running total stays in the notes (R70-88)); The quarry's route (The chase is the quarry's route read against the pursuer's: ground chosen beforehand, a cut street, a standpipe yard, a rail cutting. The reserve still runs, but the map decides). Not taken: The crowd and the law.
63. FT13 (Beastkin senses and fox-fire): Yes to: Scent as the read (For a scenting POV, the floor's named read may be a smell stated as evidence: what was smelled, where, and what it means. Tempo words follow the nose); Tells the enemy reads (Ears and tail move before the fighter decides, and an opponent who knows it may read them: an involuntary tell written as a fair, findable counter, in the opponent's eyes or mouth); Fox-fire as plain light (A canon Trait that makes light is named as light, by colour, size and what it shows; R9-3's glow ban stays on Essence discharge only). Not taken: Lineage on the appraisal.
64. FT14 (Fighting on the main): Yes to: The cut mid-fight (A district can be cut from outside during a fight: the hum dies, the room's density falls, every draw costs more, and the page names who ordered it, even unseen); The burst main (A working that splits a culvert or standpipe spikes the room's density: output up, reach down, by FOW's square-root law. The page shows the effect; any figure prints as a marked estimate (R70-99)); Short ground after (Ground fought on stays short for hours: reach falls, gauges read the residue, and a second fight there pays for the first. FOW's law decides it, and no figure prints without a source). Not taken: Rail and the tram slot.
65. FT15 (River and sea fights): River law of its own. A river gets its own rows: banks close the horizon and open a rout and an ambush, the current is the motion channel, sound carries far over cold water, and the cold drowns.
66. FT16 (The fight that is mostly a read): Read before, body after. The read pays the first four items (measure, tempo, read, fault) before the cut; the body pays the last four (the hit, the injury, the Essence, what he cannot do) after it. The cut is one line between.
67. FT17 (Clear warning before a loss): A sign and an exit. As B, plus a way out shown before the killing exchange (ground, a door, a yield, a price). A death means the exit was missed or refused, and the notes cite both sign and exit. (Option B there reads: One plain sign first. At least one plain sign the fight is lost (a gap read, a wound, a second's shout, a readout) lands an exchange or more before the killing one, and the notes cite it. Ambushes follow R48-30.)
68. FT18 (When two grammars meet): The clash is the shape. Both shapes run at once: the POV's grammar on the surface, the opponent's underneath in the cost, and the fight turns at the moment one overruns the other.
69. FT19 (A grammar for gun, bench and field): The four suffice. A marksman reads, ranks and commits, so he fights in Verdict; the alchemist and the field caster make the other man spend, so they fight in Expenditure. Each card names its grammar; no fifth.
70. AL1 (Bench work on the page): Guild form, then performed. The scene's main brew appears first as the house's numbered form, set apart (R70-75 extended to the bench), then is performed, and something departs from it. Minor bench work keeps A's single stretch.
71. AL2 (Heat at the Draw Age bench): Fuel by purse. Heat follows money: houses on trade supply heat from the main and pay the meter, poor houses burn charcoal and dung (R53-02), the north burns charcoal, and a bench's fire names its owner's class. The Bed stays everywhere.
72. AL3 (The alchemist's voice): Yes to: Reads the body first (On the menu: notices mouths, hands, sclera and tremor before faces, and reads a dose, a career or a lie in them. A card that takes it gains a 'reads first' line in its voice block); Price, vessel, seal, ledger (On the menu: weighs a thing by its cost, its vessel, whose mark closes it and where it is entered, pricing before praising. Extends R61-91 from the two texts to any alchemist who takes it); Bench words for everything (On the menu: the operations as all-purpose idiom (a plan still in the Rot, a recruit fed too fast), the Fleshshaper model (R24-1) applied to the trade, a few logged per card). Not taken: Quiet at the work.
73. AL4 (Prepared or live in a fight): Made before, ground live. Canon read straight: every Draft left a bench before the fight; mid-fight the alchemist spends the bandolier or lays Draft ground, costing turns with hands busy and eyes down. A bench scene plants each vial.
74. AL5 (A Draft in the six-second turn): A drink costs the turn. Drinking or smearing takes a whole turn and opens the drinker inside measure; throwing or smashing is one action within an exchange. The hand going to the bandolier becomes a readable tell.
75. AL6 (Who carries it onto a field): Gates, bought by purse. As B, and a company's purse decides how many certified hands it retains, at the price table's retainers (forty gold a month and up for an Adept), so rich companies field far more alchemy. (Option B there reads: Issue by gate. Drafts reach a field by their rank gate: low-gate lots to the line, Adept munitions to drilled details, Expert charges only to Expert hands. The gate becomes the field's ration logic.)
76. AL7 (The formula's own failure): Every use shows it. The precaution each formula demands (the gloved off hand, the chalked hour, the edge kept wide of the body) shows at every use, a standing tell a reading opponent can exploit. The counter stays on the page.
77. AL8 (Poison and the duel): By culture, on the Inventory. Each Standing Inventory gains a line on coated weapons and poison, taken from the culture's real analogue; the Accord's munitions class is the first entry. An Accord duel and a Moto duel may differ.
78. AL9 (A Draft's readout): Card once, body at use. R70-95's card carries the Draft's own marks (gate, rung, Class, Fidelity, Carry, maker, price, lore) once, at purchase or appraisal. At use only the body shows, plus a surgeon's inline wound line if a wound earns one.
79. AL10 (Medicine by place and purse): Both, by place and purse. The surgeon uses Drafts beside carbolic and chloroform for those who pay; the Legion gets Bone-Grey by issue; the north and the poor get the barber and Cutwater. Every wound scene names which.
80. AL11 (Proving a poison): Real tests, by place. The mirror test, the copper test and the iron antidote come into WOTR where R59-05's gradient puts them: Guild cities have them, the north does not. The coil still reads worked poisons.
81. AL12 (A forensic reading on the page): Protocol as action. The pair, the stands and the withdrawal play as action, and figures enter in a mouth, read aloud at every stand, outside R70-86's cap. The contradiction between the instruments is the scene's turn.
82. AL13 (Corruption shown on the body): Yes to: Signs in the body (The Heresiology's bodily signs become standing tells, planted before any reveal, so a reader can catch a corrupt master before the plot names him. One sign a scene at most, across A to C); Signs in the work (The bench betrays him first: vessels crack under his hands alone, inscriptions darken on their own, residue gathers in shapes. The workshop shows the corruption before the man does); Signs in technique (A corrupted practitioner's workings run their corrupted versions (the Open Crucible's model, where Honest Fire strips structure it finds inconvenient), so the tell lives in how he works and fights); The break as an event (When the vow finally fails, the Shear Break is written as its own event, the fall shown whole in the body and the work, so the slow signs pay off on the page).
83. AL14 (Accidents and fumes): Late drowning, and rest. As B, plus a findable counter: men kept lying still and watched through the night fare better than men who walk home, as real toxicology keeps such patients at rest. A knowing hand's orders save some. (Option B there reads: The late drowning. The Real Alchemy's reading: the room doses in order of nearness and the dying comes hours later, after the men have walked out. A surgeon's wound line can name it (R70-85); the grief arrives by morning.)
84. AL15 (The trade's paper in a scene): Yes to: Price counted at use (Beyond R70-48's price at purchase, a fighter or worker counts what a Draft cost when he spends it, in his own money, the sum taken from the table or the Index. Money before magic, in the hand); The mark checked (Every lawful vessel carries its maker's registered mark, and anyone handling one looks at it the way a soldier reads a proof-dent (R11-3). The mark becomes standing texture and a trail); Provenance as plot (Lots can be forged, adulterated, stale or unentered, and a scene may turn on a bad lot; the forgery is always findable by mark, assay or the Index's own failure. A fair counter and a plot engine).
85. AL16 (A Draft against a working): Two parts, two answers. A Draft splits: its plain physics (blast, heat, acid, smoke) meets Durability like any force, while its worked part answers its maker's ceiling and fails against anyone above it. Both stay traceable (R13-8).
86. AL17 (A revenant in a fight): Levers still rule. A body on habit: anatomy stops the motion (a cut hamstring drops it) while the habit keeps trying; only ash, removal or the ninth day ends it. The floor applies by structure, with no blood-loss class.
87. AL18 (The impression-body's voice): A seam the reader catches. As A, plus one planted habit of the maker leaks through the likeness, findable by an attentive reader before any trained reader names it: the maker's Core as identity, made visible. (Option A there reads: Seamless to the mourner. The likeness is written exactly as the living man, through the mourner's eyes; only the room (the dim lamp, the ink) hints. The horror is what the reader knows and she does not.)
88. AL19 (Explosives beside the Index): Plain chemistry, powder law. They exist as plain chemistry with no Essence and no rank gate, licensed under ordinary powder law. The coil reads nothing in them, and a quarryman's stick of dynamite holds about what a Thundercrack does.
89. WT1 (The item card in a fight): Tier named, card after. Mid-fight a trained eye names the Tier inline, by name alone (R70-82). The full card waits for the counter or the aftermath. No set-off block between exchanges; verify_scene warns on one.
90. WT2 (Weapon names in a fight): The POV's own name. Narration uses whatever the POV calls it: a Kharven rider's folk name, a Moto retainer's true name. It matches R70-100's rule for moves. Other names wait for a card or the aftermath.
91. WT3 (Armour sums on the page): The read names the sum. A trained POV names both Tiers in her read before the exchange (R70-88), then the steel shows the sum. Untrained POVs fall back to A. The reader checks every penetration against R46-3.
92. WT13 (Armour's kind against its Tier): Kind if plain, Tier if worked. Unworked armour fights by its physics (mail turns the cut, not the thrust); once armour carries a working, R46-3's Tier decides and the kind is only the shape the working wears, as R13-C has it for shot.
93. WT4 (Proofed shot against proofed plate): Out-coupling counts one Tier. Against worked armour a proofed round strikes as one Tier higher: proofed shot breaks proofed plate, a round two over passes, and the named round is simply two over. One ladder, R13-C kept.
94. WT5 (The stale pouch): Fails on a planted tell. A stale round may fail mid-fight only if the page showed its date earlier: the stamp on the pouch, a Harmonist's word, a re-read put off. The failure is then the fight's fair surprise.
95. WT6 (A ward breaking): By who is looking. A POV inside the craft names the layer as it goes; any other POV gets only what stops, and hears the layer named in a mouth. Keyed to the POV, as R70-100's school words are.
96. WT7 (The Well as ground): Yes to: Reach written to rung (Before contact a gauge or a practitioner's feel names the density rung (Ambient Saturation through Core), and every reach in the fight is written to it. Adds reach beside §7's draw-cost row); The unawakened in it (Porters, lamp-men and timber crews are in every Well fight as people who can win it: no Shell (the layer a working fires through) to fire, no reserve to drain. Each gets a want and a line). Not taken: The register stays tidy.
97. WT8 (Contract fights): Yes to: The posting as document (The posting is set on the page at the hook in the Guild's house style (terms, pay, register, penalty), a document voice that plants the rules before the fight (R70-71)); A clause binds the fight (Every contract carries at least one clause limiting how it may be won (alive, intact, unwitnessed, before the thaw), with a penalty. The cheapest counter often breaks the clause); Proof at the counter (The job closes at the clerk's counter: the proof the contract asks for, the clerk's dispute, the pay named from the price table. A failed proof is a Ledger debt).
98. WT9 (Who hears the rail): Called aloud to all. She says the reading as she takes it: both fighters and the benches hear it, the readout reaches a fighter's own page, and a suppressed Stage is exposed in public, with R70-112's bill.
99. WT10 (The bill after a fight): The bill in the world. Each cost arrives as a person or a paper in the aftermath: the fee named from the price table or exactly in kind, the debt spoken, the witnesses counted. The formal Ledger stays in the notes.
100. WT11 (The roll after a public fight): Entered, may earn a mark. B, and a notable win may earn a Guild commendation struck on the token (R70-96): the genre's achievement in WOTR's institutions, with legal weight and no stat effect. (Option B there reads: Entered as a record. A fight before witnesses is entered: who, where, by what, the outcome, read aloud as written. A public record that can be read back and contested at the next quarrel.)
101. WT12 (What the law turns on): Yes to: Proof decides (Law moves only on a witness or a reading inside the residue clocks (R61-7); R60-11's trace proof reaches blade killings too. An unread killing sits on the Ledger as a risk); Courts fight over it (Every practitioner's killing opens a jurisdiction contest between crown, company and guild (R60-19) as a Front, and the killer's fate turns on which layer wins it); Declare it, or murder (A killer who does not declare before witnesses by the next dawn is a murderer in every culture that keeps witnesses, Kharven and Korvaeth first. The declaration is its own short scene). Not taken: Standing buys terms.
102. ME1 (Where the combat law lands): Rule doc, three guides. A, plus new editions of the Combat Craft, Mass Combat Craft and Item and Equipment Writing guides, and NATALIE.md's stale combat lines rewritten, so nothing still teaches dead law. (Option A there reads: Rule doc only. One dated Combat Law doc through log_ruling, served by load_rules. The guides and NATALIE.md stay as they are until a later pass, stale lines included.)
103. ME2 (Combat checks in verify_scene): Yes to: Truer school lists (Percussion gets a hammer-and-haft list, boxing becomes its own school, and firearms and Kharven lists are added, so a gunfight or a hall fight is checked in its own words); Readout and beat counts (WARN past three readout lines a scene or two a turn, on two in one exchange, and on a figure carried from one exchange to the next (R70-86, R70-88)); Stale-device watch (WARN past one a scene on the archive's tired fight devices: the default 'eleven', the knock-back furrow, the overdraw nosebleed, 'without deciding to' and 'the particular X of Y'). Not taken: Checks 24 to 26.
104. ME3 (The combat sample bank): Both. A and B: culture passages where Natalie already loads them, and the fight types the archive has never written.
105. ME4 (Proof and the order of work): Law and checks, then test. Log the law and build the new checks; run the test fight against them; amend; then the guide editions and the bank, written once against proved law.

Context: Isaac answered all 105 questions in Claude Code chat on 2026-10-04 and said 'Go'; the rows are applied as R71 (rules/doc-combat-law-2026-10-04.yaml) in the same session.

## 2026-10-04 — table-law-2026-10-04

The table questionnaire (43 answers), Claude Code chat.

Isaac's direction, in his words: "Anything else do you think we should do a questionaire about?". Each line names its questionnaire id; the questions, options, sample passages and the research behind them are in imports/drafts/table-questionnaire/. Prose questions and the big calls were answered in a picker with samples; the rest were taken as a digest (the recommendation accepted). The rule rows are rules/doc-table-law-2026-10-04.yaml (R72), whose id numerals are the numbers here. He picked four from Natalie's offer; this one is "The table itself": how a roleplay session runs. K2 differs from the recommendation (Natalie makes every call herself); WD14's recommendation moved to match it.

1. K1 (What a session promises): Spine and payoff. B and C together: each thread works toward its next set piece, and every session on the way puts one earnable payoff in reach beside a fresh cost.
2. K2 (Improvise or ask): Natalie decides everything. "Bigger things wait" is struck. Natalie makes every call, even a carded NPC's death or a new faction, and logs each as an agent ruling (a call you may overturn) under the turn.
3. K3 (Which replies run long): Desktop fiction only. This reopens R49-30 for Discord: Desktop turns run about 3,500 and OOC answers are plain; a Discord post runs about 1,500 words, the house median, unless your beat asks for more.
4. K4 (Where a turn stops): The first pressure. The turn runs past pauses he would let pass and stops when something presses him: a question to him, an offer, a threat, a clock. A line aimed at him always stops it.
5. K5 (Standing orders outside fights): Every scene type. Post conditions anywhere ("if she names the stair, I ask for the daybook"). Natalie runs them to the first branch they miss, and any line your PC speaks is only your posted words.
6. K6 (What the world writes on him): Yes to: Reflexes as world facts (Involuntary responses (sweat and nausea under Pressure, a startle at a shot, cold shakes, a drug taking hold) land on his body as facts, as wounds do under R71-6; what he does next stays yours); Evidence, never the conclusion (In talk and investigation too, Natalie lays the tells in the room and never draws his conclusion; the deduction is your post, R71-6's "the read his" carried outside fights); What he would know (What your PC knows and you might not (a custom, a Guild form, a law of his own court) comes as plain recall from his card and canon only, never a new memory).
7. K7 (What a cutaway shows): The act, reason kept. The cut shows who acts and what they do, and keeps the reason, as R70-76 does for the world's magic. You see the move; your PC still has to read the why.
8. TU1 (Opening a turn): One clause, then answer. Your move gets one clause that fixes where it landed ("with the Finding face down between them"), then the world answers. The archive stays readable and the turn spends itself on what you did not write.
9. TU2 (Several NPCs in one turn): The room talks. NPCs talk to each other, interrupt and score points, and your PC overhears what they would never tell him; the turn stops when the room turns to him.
10. TU3 (Routine talk in summary): Summary, then the line. Routine exchange (prices, directions, greetings, haggling) is told in a sentence or two; any line that carries a want, a lie, a refusal or a tell is quoted in full.
11. TU4 (When the world interrupts): Actions cut, speech whole. A chain of actions stops at the first point the world pushes back, and the later actions never happen; every line he speaks is said in full, though NPCs may react while he speaks.
12. TU5 (Table talk and notes): Foot now, file at archive. Prose first; below a divider line, a short foot of OOC lines. The full notes are written once, when archive_scene (the tool that files a finished scene) saves it.
13. TU6 (What the foot carries): Yes to: Calls made (One line per call Natalie made this turn (a new NPC, a fact, an estimate), each marked as an agent ruling you may overturn); What it cost (The Ledger lines and Front ticks the turn caused, one line each, so nothing is lost before the session close); Rules and the deciding row (Two to four rule ids that bound the turn and, for any adjudicated outcome, the stat row that decided it (R14-3, R71-7)).
14. TU7 (The "previously" line): Header and "previously". The header, then two or three plain OOC lines: what happened last, what is owed, what is ticking that your PC knows of. Then the prose.
15. TU8 (Who carries the Rumor Mill): Yes to: A gossip's mouth (One NPC who wants to know things first tells it and gets some of it wrong. NATALIE.md's form, and the teller becomes a standing face); Print and notice (Where the Inventory gives literacy, news arrives as a Board notice, a broadsheet or a porter's slate, and print can be wrong too. Never in the north); Overheard (Your PC passes people talking among themselves and catches the news in pieces, mixed in with their own business).
16. TU9 (When the Rumor Mill runs): Yes to: Session start (Two or three items as each session opens, as now); Each new place (On first arrival at a town, hall, camp or market, that place's own talk).
17. TU10 (The Scene Menu): OOC list, then in-world. Three OOC lines, each with its source, reward and penalty; you pick in a word, and the turn opens on that hook in the world.
18. TU11 (A turn sent back): Unwound whole. A sent-back turn never happened: the prose is replaced and every table write it made (Ledger line, Front tick, roster entry) is reversed. Name any part to keep it.
19. TU12 (New lines in his posts): Drafted, marked. R52-09 reaches the posts: Natalie drafts the line in his voice, marked as a draft for you to keep, change or cut before you post.
20. WD1 (What moves a Front): By the calendar. Each Front gets a pace in story days. When in-world time passes, every Front whose days are spent ticks offscreen, played or not; his acts can speed, slow or stop it. Rule 4 is rewritten to this.
21. WD2 (What he sees of a Front): Signs in the world. Every tick puts one sign into a scene of that thread the same session (a seal, a stranger, a price gone up) or a marked cutaway. Clocks are never printed in play; the files stay yours to open.
22. WD3 (When the bill comes): A date or a trigger. Each line gains a thread and either a story date off the State of Play calendar or a named trigger (he returns to the Seat, the thaw comes). The close marks what fired; due() returns only those.
23. WD4 (The bill on the page): An offer with terms. The creditor or the consequence arrives with terms and the turn stops on them; his answer is the move. An offer refused or ignored is collected outright the next time.
24. WD5 (New lines on the Ledger): Yes to: Bonds, by name (Each thread's warm bonds go on the Ledger by name, with what has fed them and what has strained them, so a loss lands on a named line); Heat per thread (A standing heat line per thread: the attention crown, company and Guild are paying him. Public acts and unread killings raise it; only the right office, paid, cools it).
25. WD6 (How many lies): A lie for every want. Every roster NPC with a want carries at least one live lie, told when it serves them and logged with its tell. Rule 8 folds into this and is retired.
26. WD7 (NPCs off the page): Wants move offscreen. At each close every named NPC in the thread gets a 'doing now' line and a 'stands with him' line (owed, slighted, warm, afraid); when he meets them again, both show.
27. WD13 (What sways an NPC): Yes to: Rank bends it (A Stage gap felt as Pressure (R70-69) and a commoner's awe of a ranked practitioner (R53-18) can make an NPC yield what its want alone would refuse; a ranked NPC weighs them less); His name goes before him (Ledger lines for reputation and who saw what reach the NPC: it answers what your PC did in public, for good or ill, and the notes name the line that weighed); His lies caught on evidence (An NPC catches your PC's lie only on what it can check: a tell in his body, a fact it holds, or a read its Gnosis earns (R14-3's read row). Otherwise the lie holds).
28. WD8 (Time off): B, with project clocks. As B, and long work (a commissioned bench piece, a licence, a house) runs on a clock of four to eight that fills across spans, kept on the Ledger.
29. WD9 (The road): The road as a clock. The journey gets a clock of four to six (weather, horses, food), ticked by miles and calendar, each tick a beat on the page; if it fills first, the road takes a horse, a hand or the season.
30. WD10 (What a win pays): Yes to: Favours owed him (A debt in his favour becomes a Ledger line he can call in later, on terms, the way his own debts are called); Access and licence (A draw allotment, a Guild licence, a key, a seat at a table: rights on paper that open doors and can be revoked); Spoils with a history (Things taken or given (a dead man's blade, a horse, a proofed rifle) arrive with their lineage (R70-48), and the Ledger keeps who wants them back).
31. WD11 (The last warning): Plain only when unreadable. As A, plus the OOC line only when the danger is one his character could not read: Pressure (the felt weight of a higher Stage) from far above him, or a Well's own law.
32. WD12 (After his death): The world goes on. The thread goes on and your next character enters it. The dead man's debts fall on kin or partners, his Fronts keep their clocks, and a grief Front may open (R58-07).
33. WD14 (Who writes the close): Applied, then listed. At your wrap and whenever a scene is archived, Natalie applies the close herself and lists each write once as an agent ruling (a call you may overturn); nothing waits.
34. WD15 (Scenes set in the past): Only what still binds. A past scene adds canon and precedent, and writes a Ledger line or Front history only for what still binds at the thread's live date, which the close checks.
35. MP1 (Natalie's seat on Discord): The Judger's desk. Natalie also drafts world and NPC posts, rulings and closes for you to post as narrator. Every word that reaches the server passes through your hands, and the bot stays model-free.
36. MP2 (Who posts when): Order when it matters. Free posting in talk and travel; in fights and contests a fixed round order with a reply window the Judger sets, after which the round moves on and standing orders (R71-5) play for the absent.
37. MP3 (Player against player): Terms first, then Judger. Before contact both players post terms (what counts as a loss, what is off the table), R71-54 widened to every contest; inside those terms the Judger rules by card, as in B.
38. MP4 (A guest's own lines): Yes to: Lines and veils (Each guest lists lines and veils on their character's card; the Judger and Natalie honour them in that player's scenes, and the Floor binds everyone); Mortal or not (Each guest marks their character mortal or not. One marked not mortal can be maimed, captured or ruined, never killed; this narrows R48-31 for that character only); Explicit scenes opt in (Explicit scenes run only in age-restricted channels with only players who opted in present; anyone else's character sees a door close).
39. MP5 (What guest scenes become): The Judger rules breaks. On archive the Judger marks each break struck or accepted as a new fact and tells the player which; pages mark every character's owner.
40. MP6 (What players can look up): Yes to: Their own Ledger lines (/due and /ledger show a player only the lines about their own characters); Public faces on the roster (/roster and /npc show what is public: name, look, voice, role. Wants, lies and what they know stay with the Judger); Adjudication cards (Each ruling's card is posted in the scene's thread, so any player can see which stat rows decided it).
41. ME1 (Where the table law lands): C, plus the tools. C, plus MCP changes: a thread and a date or trigger on Ledger rows, a pace on Fronts, new roster fields, reward and penalty in scene_menu, and the bot's table commands per MP6.
42. ME2 (The data already on file): One reconciliation pass. Every open row gets a thread and a date or trigger under the new law; dead and stale lines retire with a note; Fronts get a pace; State of Play pages are rewritten.
43. ME3 (The test session): Law and tools, two tests. Log the law, change the tools and reconcile the data; run one Desktop session start to close and one Discord scene through the full loop; amend; then the skills.

## 2026-10-04 — intimacy-law-2026-10-04

The intimacy questionnaire (43 answers), Claude Code chat.

Isaac's direction, in his words: "Anything else do you think we should do a questionaire about?". Each line names its questionnaire id; the questions, options, sample passages and the research behind them are in imports/drafts/intimacy-questionnaire/. Prose questions and the big calls were answered in a picker with samples; the rest were taken as a digest (the recommendation accepted). The rule rows are rules/doc-intimacy-law-2026-10-04.yaml (R73), whose id numerals are the numbers here. He picked four from Natalie's offer; this one is "Intimacy and explicit scenes": relationships and courtship by culture, desire and refusal lines, dubcon handling, aftermath, how bonds grow, the new style in bed. Every sample was between adults. K2, K5 and SC1 differ from the recommendation.

1. K1 (What an explicit scene earns): B, and joy may stand. B by default, and a settled pair may have a night that is only pleasure and warmth, its consequence small: a habit, a mark, a witness.
2. K2 (On the page or cut): Always on the page. Any sex that happens inside a scene is written explicitly, start to finish, with no cut and no fade; the aftermath follows on the page.
3. K3 (When the first time comes): When the people would. No pacing rule: NPCs act on their wants and refusal lines, so sex may come first and the bond after, or never. Table Rule 3 decides.
4. K4 (The lover's desire and refusal): Desire, refusal, and the hinge. As B, plus a third field: what would change their mind, either way. Rule 9's change of mind then has a planted cause a player can find.
5. K5 (What the Ledger keeps): Yes to: Debts and promises (Whatever was promised, owed, bargained or betrayed in bed is entered and comes due like any other debt); Witnesses and reputation (Who heard, who saw, who will talk: gossip, scandal and a rival's leverage, entered as who-saw-what, and able to open a Front); Marks on the body (Bites, bruises, beard-burn, a strained hip, another's scent on the skin: entered and carried on real healing times (R60-02), visible to whoever looks); What was learned (A secret told, a scar seen, a weakness found in bed is entered as knowledge the other now holds, and may use).
6. SC1 (The words, by culture): Crude English, native in mouths. Narration keeps one crude English; each culture's own words for the body arrive in speech and italic thought, as its swears do.
7. SC2 (How long it runs): By weight. A first time, a turning point or a dark scene runs as a set piece; a returning pair's night inside a chapter runs on that chapter's length, the aftermath always written.
8. SC3 (Tracking the bodies): Fixed at each new pose. Each new arrangement is fixed in one clear sentence as it forms; between poses, sensation leads and the geometry may blur. This settles the two skills' wording.
9. SC4 (Which sense leads): The POV's own order. The POV's body and trade decide: a beastkin nose first, a Moto eye first, a sealer's hands first. Rule 9's scents still appear in every scene.
10. SC5 (Talk in bed): Full voice, talk as play. Each partner talks in bed the way their card talks out of it, crude, teasing, bargaining or tender, and the talk is part of the act.
11. SC6 (Power games, framed): By each culture's form. The Accord seals terms on paper, the Moto enter a word in form, Kharven takes a word before witnesses; the stop-word carries that culture's weight, and breaking it is answered under that culture's own law (R53-11).
12. SC7 (Consent on the page): Both, read together. Words and body both carry it. A refusal in either channel is a refusal; where the two disagree the scene has become dubcon (dubious consent) and is written as dubcon (SC9).
13. SC15 (Reading a lover): Senses free, workings by leave. What cannot shut, a beastkin nose or ears, reads freely; a worked read, by Gnosis or a Moto's eyes, needs leave, and one taken unasked is B's trespass, with B's tell, counter and debt.
14. SC8 (Workings on desire): Desire, with tell and counter. An Obsession or Attraction working, a charm or a Draft may make someone want; it shows a tell, has a findable counter, costs its user, and the aftermath knows it was made.
15. SC16 (Bedchamber arts): Given or drawn, fully priced. A bedchamber art is a technique: a Codex line, a cost in both bodies, a tell, a counter, no figure until canon holds one. One drawing unasked is a Claim, and the scene dubcon or non-con (SC8).
16. SC9 (The body under coercion): Shown, known as reflex. Arousal may be written, and the POV knows it for the body's reflex, apart from her will; she carries that knowledge into the aftermath.
17. SC10 (Carrying it forward): Yes to: In the body and habit (The survivor's later scenes carry it physically (the startle, sleep that will not come, the seat with its back to the wall) until the thread resolves it); The bill reaches the world (The act opens or advances a Front: feud, blood-debt, pregnancy, scandal or a case at law; the perpetrator's own account is a lie in his mouth (Rule 8)).
18. SC11 (The aftermath beat): Procedure, meaning unsaid. The aftermath is the small work after (washing, the fire fed, clothes found, the door), and neither partner says what it meant; the change shows in how they do it.
19. SC12 (Your character in the bed): Contact as world fact. Once your post sets the act, contact, position and what the partner does to him are world facts; his arousal, pleasure, pain and climax, and how he bears them, stay yours.
20. SC13 (The explicit roleplay turn): Standing orders in bed. You may post the course of the encounter, a pace, a limit or a stop for your character, and Natalie runs it to the first branch it does not cover, then stops there.
21. SC14 (An NPC who would force him): Threat placed, his post decides. Natalie sets the threat in the room (the grip, the bargain, the Draft in the cup) and stops; the act reaches the page only through your post.
22. CO1 (Where courtship custom lives): Courtship field, plus mores. A, plus a Mores field: what the culture holds shameful and what it boasts of, nakedness and bathing, the pleasure trade (CO18), and what its law does to adultery and to rape, written beside R70-45's law field.
23. CO2 (Kharven courtship): Yes to: The stack proves him (A suitor splits for her household's woodpile unasked, labour-debt run in reverse; the asking comes when the stack is full and her kin say so. Entered in the Kharven field); The skin answers (Her household answers at the hearth: she drinks from the sealskin and passes it across the fire, and he drinks after her before everyone. A withheld skin is the no, said without a word); Ridden off, priced after (On the nameless day a man may ride off with a woman, and her kin name a price on the first named morning. Whether she went willing is hers to tell; the custom never asks).
24. CO3 (Moto courtship): Yes to: Asked in form, entered (A match is asked in form at the hinge of the day and is real only when the register holds it in the house's own hand; an unentered lover is nobody to the house); The eyes offered (A suitor outside the line courts by lifting his eyes to a Moto and leaving them there, offering himself to be read; whether she reads him, and how far, is her answer).
25. CO4 (Accord courtship): Yes to: Terms under seal (A match is a settlement drawn by an advocate, pledged 'Ita spondeo' and entered in ink, with what stays in her name written in. Courtship is the negotiation, and love shows in the clauses); Breach of promise sued (A broken engagement is actionable at the Assize: the letters are read aloud in open court and the Bench prices the jilt. Every love letter in the Accord is also evidence).
26. CO5 (Mahuo courtship): Yes to: A sijo owed a sijo (Courtship is a verse exchange: the suitor's three lines are answered with three, and the last clause turns. A plain answer costs standing, as R70-110 rules at court); The speech level drops (The proposal is a change of speech: one of them drops from the high forms to the plain speech kept for kin and spouses, and the other answering in kind is the yes).
27. CO6 (Courtship in the lineage halls): Yes to: Entered in the book (A marriage is real when the husband's hall enters her in its book as 'of' her father's hall; a secondary wife is entered lower, and an unentered woman has no standing in the hall); Bought for the book (A hall marries for a skill it lacks, and the bride-gifts come with a schedule of what her children will be taught. Love is a clause, and the halls say so).
28. CO7 (Dawi courtship): Yes to: Entered, never promised (A Dawi match is made backward: the acts already done for each other are entered in the Tally in metre, and the entry is the marriage. There is no betrothal); Kurlo, the refusal unsaid (Courtship is 'Kurlo' said alone between two people, with the 'Ei kurme' that would end a bargain left off: a thing unbegun and not refused, the nearest the tongue comes to hope).
29. CO8 (Consorts, concubines, widows): Yes to: Entered lower, in book (The lineage halls and the Moto enter a secondary wife or consort below the wife in the book or register; her children's standing is written there, and an unentered child is 'written in the wrong hand'); Accord: off the books (One spouse in Accord law. A kept woman or kept man lives on an allowance quoted from the price table, a scandal with a sum on it, and their children are sine sigillo); Kharven: the brother's widow (A Kharven widow and her stack may pass to her dead man's brother, wife or no wife, if she takes the skin from him, so no hearth goes cold; refusing is her right, and her hunger); Dawi: one entry only (The Tally holds one marriage entry. A second partner is an act nobody will stand behind, 'kurnur', unentered, and carries that swear in the hold).
30. CO18 (The pleasure trade): Each culture's own form. The Accord licenses houses under seal and inspection, Eastern courts keep ranked quarters or verse-trained entertainers, the north keeps no house and trades in kind; entered in CO1's Mores field, fees as price-table rows on your word.
31. CO9 (Marriage as politics): A Front with a clock. A political match in play runs as a Front: betrothal, settlement, wedding and first heir are its ticks. A broken match fires the Front, and someone pays.
32. CO10 (Jealousy and rivals): Yes to: A feud with a bill (Jealousy acts: slander, theft, a duel, poison. Each act lands on the Ledger as a debt or a witness, and a love rival who recurs is paid for as R70-104 rules); The road to Obsession (Fed long enough, jealousy turns to Obsession Force: Breadth collapses and Empathy runs one way. An instrument or a good Gnosis read can find it, which is its fair counter).
33. CO11 (Conception and the pox): Ruled openly, every time. Each bed between partners who could conceive records its precaution (sheath, sponge, timing, a Draft, or none) in the notes; Natalie rules conception and the pox by period medicine, names what decided, and a pregnancy opens a Front.
34. CO12 (Love across a Stage gap): Yes to: He holds it, and pays (The higher partner suppresses at home every waking hour; his jaw, collar and temper carry it, and the household learns to read the bill); Drawn off by an art (A partner who holds a draining art, as Yorime does, may take the Pressure off by touch at that art's own price, traced to Fracture of Worlds before first use; love alone draws nothing).
35. CO13 (Pressure in bed): Let go, by leave. A, plus: a lover may ask him to stop holding it in. Letting go is the most intimate thing a practitioner can give, and she pays in sweat and nausea she chose.
36. CO14 (Lovers and the warm bond): Never the only one. Lovers count, but each thread also keeps a warm bond that is not romantic, so a romance that dies, sours or turns to Obsession leaves warmth standing.
37. CO15 (How a bond grows): Yes to: Tokens and maintenance (A bond grows by what is mended, fed and carried: the coat, the comb, the bowl. Each scene adds one, and the reader counts them); Jeong through hardship (A bond grows from shared cost, chosen or not: a night in a collapsed gallery, a winter of short rations. Enemies can accrue it, and it binds them anyway); Crystal fact, no figure (The breakthrough readout R70-84 already owes at Flourishing also names its Catalyst, the first Spirit Axis, with no figure (R12-5); no other bond prints, and nothing says whether she loves him).
38. CO16 (Love mourned or lived): Lived first, then cost. A bond gets scenes of its own joy before a loss may land on it; a love that dies before the reader has seen it lived is a fault to fix.
39. CO17 (A bond after death): Clean or a cage. A, plus the turn: grief fed long enough tips the bond into Obsession, which an instrument or a good Gnosis read can find, and a Crystal grown dependent on the dead risks FOW's fracture events.
40. ME1 (Where the intimacy law lands): B, plus the Inventories. B, plus the courtship and mores fields drafted for the six cultures from these answers and entered on your word, and an intimacy section in the Dialogue Craft Standards and Scene Writing Process Guide.
41. ME2 (Intimacy checks in verify_scene): Yes to: An explicit mode (verify --explicit WARNs on a scene with no smell word, no sound or mimetic word, an italic mimetic word, or notes without a consequence line, and stops counting 'cock' as gun vocabulary); A floor guard (FAIL when an explicit scene names anyone whose card or roster gives an age under eighteen; WARN when a named partner has no age on file. The body's age counts, never a soul's); Euphemism bans (Bed euphemisms that dodge R49-51 (his member, her sex, manhood, her core) FAIL in narration like the hard-ban words; in a mouth they pass, since a character may be coy); Stale-touch watch (WARN past one a scene on the archive's repeated touches: the hand on the arm, the jaw held, the kiss on the hair, as R71-103 does for fight devices).
42. ME3 (The intimacy sample bank): Both. A and B: culture beats where Natalie already loads them, and the kinds the archive lacks; this questionnaire's samples become their first drafts.
43. ME4 (Proof and the test scene): Law, checks, NPC test. Log the law and build ME2's checks; write one explicit scene between adult NPCs on your thread's Kharven ground, a Kharven half and a Moto half split by a break mark (R49-27); amend; then guides, Inventories and bank.

## 2026-10-04 — mystery-law-2026-10-04

The mystery, horror and intrigue questionnaire (46 answers), Claude Code chat.

Isaac's direction, in his words: "Anything else do you think we should do a questionaire about?". Each line names its questionnaire id; the questions, options, sample passages and the research behind them are in imports/drafts/mystery-questionnaire/. Prose questions and the big calls were answered in a picker with samples; the rest were taken as a digest (the recommendation accepted). The rule rows are rules/doc-mystery-law-2026-10-04.yaml (R74), whose id numerals are the numbers here. He picked four from Natalie's offer; this one is "Mystery, horror and intrigue": the Lord of the Mysteries register and the Night Watch, fair clues, how secrets surface, horror pacing, court and faction intrigue, lies that stay uncorrected. K2 adds the challenge mark to the recommendation. MY15 rules CONFLICTS C-125.

1. K1 (How much the reader may solve): Each book declares. Each book or thread bible names its mode: inverted, fair puzzle, or the split (the reader knows who, never how or why). Undeclared work defaults to inverted, the house mode.
2. K2 (The fair-play terms): Yes to: Nothing unseen (The solution rests only on what the reader or player was shown. A clue the investigator held and the page withheld voids the solution; the notes list every clue used); Codex-backed solutions (Any working in a solution has a Codex line and its rule acted on the page first. No working is invented to solve a case; one that falsifies perception is planted (R71-30) or barred); Sealed solution (The truth (who, how, why) is written in the notes before the first clue is placed and never moves to fit a guess: R57-10's ban on rigging made a procedure); A challenge mark (Ellery Queen's device: a book marks the point where every clue is on the page, as a chapter-head line or a set-off notice, before the solution).
3. K3 (When secrets pay): Caught or clocked. A secret pays when his PC catches it or its Front (a faction's clock of moves) resolves, never on a timer. A few are marked 'kept' and never pay on the page, as the one-word letter.
4. K4 (What knowing costs): Records that act. B, plus a few records act on whoever touches them through canon mechanism (Mnemata, records held in objects, R61-70), priced by Resilience with the counter named in the notes. No invented figure.
5. K5 (What catching a lie is): His PC acts on it. Caught when his PC acts on the truth or names the lie in play. Isaac spotting it in chat changes nothing in the world until his PC moves.
6. K6 (Finding clues at the table): Core found, extras earned. Each conclusion's core clue comes to any sensible look; the further clues that sharpen it, speed it or name the purse (who paid) come only to the right question or instrument.
7. K7 (Cutting away inside a case): Cut to the hand. A turn may close on a short marked cut to the other side moving (a hand, a room, a deed) that may carry a clue, never a face, a name or the answer.
8. MY1 (Clues per conclusion): Three, by three roads. At least three clues per conclusion: one in the room, one in a mouth, one on paper or an instrument, so no single kind of looking is required. The notes list all three.
9. MY2 (Where the truth is kept): Yes to: A sealed truth file (One entry per open mystery under table/: who, how, why, what each NPC knows, what stays kept. Natalie reads it each session; play never quotes it. One file with any sealed Front file); Clue list in the notes (Every scene's author notes list each clue planted, found or missed, and the conclusion it serves, so fairness can be audited after).
10. MY3 (Red herrings): True facts, refutable. A herring is built from true facts that point the wrong way, is refutable on the page, and is listed as a herring in the notes.
11. MY4 (When the clues are missed): Both, at a price. The Front ticks and a costlier road opens: each miss spends something (a witness, a Trace read once, a life), so the case stays solvable and the delay shows on the Ledger.
12. MY5 (The rest of a Watch search): Protocol, closed on filing. As A, and the search closes on its docket line set off from the prose: the Register's flat record against the long hour, the Lord of the Mysteries document turned to a close.
13. MY6 (The interrogation): A duel of tells. R71-22's accounting extends past fights: each question aims at a tell, and the page shows what it bought or cost.
14. MY16 (True words that deceive): The fact is the tell. No body tell, since the speaker tells the truth; the deceit lives in what the sentence leaves out, and the page carries a fact that turns its meaning where a careful player can line it up. The notes name that fact.
15. MY7 (Clue objects): By culture. Each Standing Inventory gains a 'Clue beds' line beside 'Notices first': Kharven counts and the woodpile, Accord meters and wax, Moto seals and court verse. A case draws its clues from its culture.
16. MY8 (The investigator's head): Facts shown, conclusion held. Every fact she notices reaches the page plainly; the conclusion waits, carried by her next act, as Holmes keeps his. Numbered steps stay legal at the solution.
17. MY9 (How witnesses err): Both, logged apart. Errors come by either road, and the roster gains an 'errs about' field beside 'lied about', so an honest error never owes a liar's tell.
18. MY10 (The lie never caught): It comes due. The first time his PC acts on it, the lie opens a Ledger line; the truth arrives as that line's cost when it bites, the tell already behind him to find.
19. MY17 (The thing left unexplained): When a scene has one. R49-11 carried to the table: no count; an unexplained notice comes when a scene has one worth leaving, marked texture or seed in the notes as in C.
20. MY11 (What instruments prove): Never lies, may miss. A sound instrument prints true. A case lives in what one was not built to read: below its floor, behind a ward, or asked the wrong question. The notes say which.
21. MY12 (The solution scene): Yes to: The hearing (A court, inquest or Register hearing, turned where a statement meets the exhibit that breaks it; each culture keeps its own justice (R53-11)); The procedure (A test or instrument proves it on the page as action (R71-81), and the result is the verdict); The document (The case closes as a filing, a docket or a set-off notice (R70-67, R70-17), its last line the verdict).
22. MY13 (The reveal): Cold, in a cluster. The answer lands as a short cluster of one-line paragraphs at the moment of proof; the explanation comes later or never.
23. MY14 (The Watch at the table): Both, by where. Patron where the crown's warrant runs and his PC is neither the hand (who did it) nor the purse (who paid); rival where he is either. In Ketsuen it can only ask.
24. MY18 (A rival on the case): A rival on his own clock. B, and an NPC on the same case runs it as a Front and may close it first, right or wrong, from clues the page has shown; a wrong close can hang an innocent, a right one takes the credit and the fee.
25. MY15 (Naming Malphas in a file): Title only, everywhere. No Watch file names him; he is filed by his title at his own written request, and named volumes are read at the desk, never copied in. The Papers stand.
26. HO1 (Dread pacing): Long build, one hard shock. The build stays long; the swift beat is one sudden sight set as a cluster of one-line paragraphs (R70-20), then the scene moves. One shock per horror scene at most.
27. HO2 (The thing seen): Half-seen, then full. R9-3 extends to horrors: effects and outline first, through the room and the bodies (R70-69's order); the full inventory lands when the thing is understood, appraised or fought.
28. HO3 (Fear in Isaac's PC): Caused signs, his read. Where a field, Pressure, a working, the cold or a sudden shock acts on his body (the Pike's weight, the Lamp-drinker's chill, a startle), its signs are world facts; what he feels about them and does stays his.
29. HO4 (What horror leaves): Marks that compound. B, and a mark struck again before it fades deepens to a standing condition with a named counter (rest, a person, a rite): fraying by stages, still no meter and no number.
30. HO5 (The dead and the folk belief): Half true, by mechanism. Events show where a belief holds and where it fails, both traced in the notes to canon mechanism; the people keep their reading, and the narration still corrects nothing.
31. HO6 (The Veil and his own grief): His, from canon only. What he carried may condense too, shaped only from grief or rage his archived scenes and card already show; the beast has no mind to voice, and his response stays his.
32. HO7 (Cosmic scale on the page): In frame at a peak. Effects carry it by default; at an arc's peak one may stand in frame in full, as stated law with reasons kept (R70-76), changing no plot (R7-2).
33. HO8 (Body horror outside a fight): Full and clinical. R48-34 extends to horror: anatomy named, colour, texture and the absent smell, nothing looked away from, in the POV's flat, exact eye. Documents may carry it too.
34. HO9 (The witness's face): One witness, horror only. In a horror beat, one witness's face may come before the thing, once a scene; the reaction shot used as characterisation stays a tell everywhere else.
35. IN1 (What turns a council): The dated fact. The turn is arithmetic or paper: a date that does not fit, a column, a seal, found on the page where a player could find it first. Speech and reads colour it.
36. IN2 (Feints within feints): Any depth, each planted. Schemes nest as deep as the faction can afford, and every layer leaves at least one sign a player could catch before that layer turns.
37. IN3 (Betrayal by the trusted): The warm bond is safe. The thread's standing warm bond never betrays by choice; anyone else may, with the signs shown twice before the turn (R71-23's rhythm).
38. IN4 (Leverage and blackmail): Held, it marks the holder. As B, and every held secret is also a Ledger risk against its holder, on the same line as K4's B: someone wants the secret, or the man who holds it, gone.
39. IN5 (Spies and the information trade): Yes to: The press as intelligence (Inserts, bulletins and the penny press carry public intelligence both ways: whoever reads them learns something, and is learned about by whoever filed them); Letters as exhibits (Intercepted letters, wires and dockets appear in full as documents Isaac can read (R70-67), with seal, hand and paper described as clues); Tradecraft per service (Each service (the Watch, the Mother's cultures, the Moto court, the Mahuo houses) gets working words for agents, drops and watchers in its Inventory's Words entry (R70-33)).
40. IN8 (One man, two faces): Either road; masks leak. A or B, at least one link planted before the unmasking; a face held by a working has its Codex line and leaks a seam, as an impression-body (a dead man's likeness worked from his Trace) does under R71-87.
41. IN6 (How much of a Front Isaac sees): Clock shown, contents sealed. For mystery and intrigue Fronts only, the clock and its ticks show; the Want and Next move live in a sealed file Natalie reads, opened to Isaac when the Front resolves or he asks.
42. IN7 (When the process is bought): Bought, with a trail. Courts and files can be bought, lost or sealed, and every corruption leaves a findable trail (a payment, a hand, a gap in a numbered series), as R71-84 makes forgeries; finding it reopens the case.
43. ME1 (Where the law lands): Doc, NATALIE, a guide. B, plus a new Mystery, Horror and Intrigue Craft Guide in desktop/, so Natalie has one document to read before a dark or scheming scene.
44. ME2 (What the table keeps on paper): Yes to: Faction sheets (Every faction with a Front gets a sheet on the Powers page model: wants, holds, fights by, set against, fears, its method, and its seam); What NPCs know of him (The roster's knows line gains a running entry, updated at session end, of what each NPC in an intrigue knows or believes about the PC).
45. ME3 (Checks in verify_scene): Yes to: Cosmic stock words ('Unnameable', 'eldritch', 'indescribable', 'unspeakable' and 'nameless dread' join the hard-ban list as a fourth stock family, FAIL in narration; the Nameless day stays legal); Stale not-knowing lines (WARN past one a scene on 'could make nothing of it', 'did not know what that meant' and their kin, as the combat stale-device watch does for fights); Planted signs for turns (A scene whose notes mark a reveal, a betrayal or a case's solution FAILs unless the notes list an earlier planted sign (R48-30, R71-30)).
46. ME4 (The sample bank): Both. B as the new bank, and each culture file gains one dark scene so the voice and the type meet.

## 2026-10-04 — techniques-law-2026-10-04

The techniques and characters questionnaire (47 answers), Claude Code chat.

Isaac's direction, in his words: "Anything else do you think we should do a questionaire about?". Each line names its questionnaire id; the questions, options, sample passages and the research behind them are in imports/drafts/techniques-questionnaire/. Prose questions and the big calls were answered in a picker with samples; the rest were taken as a digest (the recommendation accepted). The rule rows are rules/doc-techniques-law-2026-10-04.yaml (R75), whose id numerals are the numbers here. He picked four from Natalie's offer; this one is "Techniques and characters": building abilities and people under the new law, technique cards with readouts, vows and Traits, naming forms, how a character or NPC card is made, progression arcs. K5 adds a counter at each phase to the recommendation.

1. K1 (Where a technique is written): Signatures own, arts shared. A signature, or any art one person derived alone, gets its own page priced at its owner's exact reserve; a school art lives once on its school's page, priced by Stage band. The card's rows link to either.
2. K2 (Designed first or found in play): Core first, rest found. Before first fire the card holds mechanism, cost, limit, tell and counter. Name, forms, Readiness (its casting-time figure), evolutions and What nobody knows fill in from what play showed.
3. K3 (Your sketch to a card): Whole card, yours to keep. Natalie returns the full R47-2 entry at once, a proposed true name in your character's tongue included; every choice on it (name, call, vow) sticks only when you keep it.
4. K7 (Your price against the law): Your price, new mechanism. The cost and limit you named stand; Natalie reworks the mechanism until they fall out of it, so R17-4 holds. If no lawful mechanism yields them, she says so in one line and offers the nearest.
5. K4 (Techniques on the Crystal): Signatures print once. Adds a fifth growth moment to R70-84: the first time a Trait-permitted signature holds, one inline Crystal line names it, its Trait and its Grade. School arts never print.
6. K5 (The fairness test): Yes to: Same Stage can answer (The written counter is within reach of a prepared practitioner of the technique's own Stage; a counter that needs a higher Stage or a rare Wellspring fails the card); Counter on known law (The counter rests on law someone already knows (a Wellspring's recorded failure, a school's teaching, a Family's weakness), so a player can study toward it before he meets the technique); A counter at each phase (The card names a counter before, during and after contact; 'none once contact is made' fails and the card is rebuilt).
7. K6 (What opens a new technique): Numbers plus a cause. The FOW line must be met, and the technique arrives only with a cause on the page: a teacher named, a book studied, or the problem it answers met in a fight.
8. TE1 (How long a ladder of forms): By the school's culture. Western and Kharven schools run short ladders like Liechtenauer's; the lineage halls and the Korean-stratum houses keep long catalogues. Each school's page sets its count.
9. TE2 (Cutting a chant short): Clip it, lose output. A chant's length sets its output: each line dropped costs a share of output and buys Readiness (casting time), both figures set on the card.
10. TE3 (Does a technique grow on its own): Grows to its Grade. Output rises with the reserve until it reaches the top of the Grade it was designed in; past that it needs an escalated form, with its suffix and a shown cause.
11. TE4 (Drill and mastery): Mastery marks on the card. Three named marks, Held, Drilled and Mastered; each lowers Readiness and cost share by figures set on that card, each crossing a shown cause entered in the chapter-end block.
12. TE5 (What a vow is worth): A great vow, one Grade. As A, and a great vow, one that stakes life, a limb's use or Crystal mass, may lift output one full Grade; nothing lifts it further. A release call stacks on top.
13. TE6 (What else a vow may be): Yes to: A stake beyond Shear Break (A vow may stake life, a limb's use or Crystal mass; broken, the stake is paid at once and for good (R55-1). Under TE5's B, only a staked vow reaches a full Grade); A vow between two (Two people bind each other; each card carries the terms, and whoever breaks them takes the Shear Break).
14. TE7 (How a vow is sworn): Aloud, any witness. A vow binds when spoken before any living witness, the opponent included; it earns oath experience only at a stone. Somebody always heard, so the counter can be found by asking.
15. TE8 (When a new Trait forms): Canon's four, on the page. A new Trait forms only at one of the four events, written as its own scene; no count cap, the scale of the event is the limit.
16. TE9 (Who writes your character's Trait): Natalie writes, you keep. At the event Natalie writes name, Reflection (its kind) and Lattice property; it sticks only when you keep it, as a Third Name does.
17. TE10 (What a Trait entry carries): Yes to: Founding sentence (The statement the Continuum accepted, in the bearer's words, yours to write for your characters as in TE11. Denying it is the Shear Break, so every Trait carries a findable counter); Rigidity line (What the bearer cannot safely contradict, as a fact. NPCs play it on the page; for your characters it stays a fact for you to play); Offices held (Which of Bias, Permission, Nucleation and Ceiling it serves; a Permission line lists the signatures it allows).
18. TE11 (How a Trait evolves): The bearer's sentence. The evolved law takes the shape of the sentence the bearer holds in the crisis; for your characters you write that sentence, and the Crystal prints the result.
19. TE12 (New Resonant Pairs): New, by R18-2's test. R18-2 extends to Pairs: a new one may be proposed when a build reaches a combination the ten lack, with real mechanism, Grade and effect; it binds once ratified.
20. TE13 (Carding a Synergia): Drilled, one shared page. One technique page carries both partners, the drill that made it, the cost split and the counter; both cards link to it; no vow.
21. TE14 (Naming a two-tongue art): Each calls his own. The card carries both names, each glossed; in a fight each partner calls it in his own tongue, two calls in one beat.
22. TE15 (One man's techniques combined): A carded composite art. Two of his techniques may be derived into a third, carded art with its own cost, counter and new name; it costs at least the sum of its parts. Chaining stays free.
23. TE16 (What a school keeps back): The last form withheld. A school writes its lower forms and teaches its last form mouth to ear; outside the school that form counts as self-derived and is read live.
24. TE17 (Learning by watching): Re-derived after watching. A witnessed technique may be re-derived in downtime if the watcher holds its Wellsprings and meets its FOW line; it runs at his stats and becomes his own, with his own name.
25. CH1 (One card shape): A table head, then sections. A one-screen head above the seventeen: header, stat line, combat grammar (Verdict, Blade, Percussion or Expenditure), Traits and techniques by name with tell and counter, the voice sample line. Natalie fights from the head.
26. CH2 (The rungs of a person): Three rungs. Roster entry; a short card (header, FOW line, Traits by name, one signature technique with tell and counter, voice block, Lore); a full card. Today's compact cards become short cards.
27. CH3 (What lifts a person a rung): Yes to: Stats decide a scene (The first time his stats must decide an outcome on the page, he gets at least a short card before that scene is written); Becomes a rival (A rival under R70-104, spared and returning, gets a full card, since his growth and his debts must be traced); Holds a POV (Anyone whose head a scene sits in gets a full card first, since his readouts come from his own sheet).
28. CH4 (How much of the sheet): Sixty-four on full cards. Full cards carry all sixty-four and the Pool, unset ones spent inside the re-costed totals along the Path and logged, your characters' as CH5 decides; short cards carry Primary totals and the peaks a scene will stress.
29. CH5 (Who spends a Level's points): He builds his own. You spend your characters' points at each Level, build talk welcome; Natalie spends each NPC's where the Level was earned (a Level won by the sword feeds the sword), logged in the changes block.
30. CH6 (Four cards past the gate): Outliers with Strain. R56-4 extended: each keeps his Level with standing Residual Strain, priced by Part Ten (XP five percent lower, Overchannel and Backlash risk two percent higher, per fifty Levels past). Lorn and Heisuke owe one step now.
31. CH7 (Marking an estimate): Tag it inline. One mark, '(est.)', after the figure and nothing more; the six styles collapse into one.
32. CH8 (New voice block slots): Yes to: Speaker type (The researched real-world model (a customs clerk, a field surgeon, a drover) moves from the notes onto the card, so every return starts from the same voice); Chant tongue (The tongue his chants and release calls run in (his own under R50-26, or a learned one under R70-26, as Kwon's Accord Latin), so Borin's Latin forge-liturgy is caught and fixed); Lying tell (What his body does when he lies or withholds, the body kind of R49-36's three tells, so the frequent lies of R48-42 can be caught by a player who reads bodies).
33. CH9 (Lore and the length cap): The seventeen only. The cap binds Identity through Fracture Log; Lore runs free below it. The eight cards over without Lore are trimmed in the sweep.
34. CH10 (Story fields on the card): Yes to: Refusal line (The thing he will not do whatever is offered, as the roster already carries; Table Rule 3's refusals read straight off the card); Conviction (The belief that costs him, named; the Trait System's 'Belief, once survived, becomes law' gets the belief it grows from, and a Shear Break has a truth to break against); Arc kind (Positive, flat, negative or corruption, after K. M. Weiland's arc types: set when the card is made, revised at each arc's end).
35. CH18 (Skills on the card): Skills section, with marks. As A, and each skill carries TE4's three marks (Held, Drilled, Mastered), each crossing a shown cause entered in the chapter-end block. The Crystal never prints them.
36. CH11 (A comic name on the card): Byname with its making. Byname, who coined it and when, its bank or sound rule, and the given name under it, so a grief beat and the Kharven giving-on have both names to work with.
37. CH12 (A rival between meetings): His own clock, shown. A rival's growth runs on a Front (a world clock that ticks between sessions); each tick names its cause, and his return shows it in the room and in what the POV was told.
38. CH13 (An old feat too big): Keep it, explain it. The feat stays and the card names how (an Overchannel spike, a Domain, a site's Wellspring) and the cost it charged, logged on the Ledger.
39. CH14 (XP as arithmetic): Sums for the carded. Arithmetic for your characters and full cards, the scale for everyone else.
40. CH15 (What training pays): Edge, or a sworn drill. A, and a drill sworn as an oath before a Witness Stone pays Part Two's oath XP on swearing and on fulfilment; a broken drill is a strain event. Solo Leveling's contract in FOW's terms.
41. CH16 (The record of a climb): Yes to: XP bar (XP held and XP to the next Level, from CH14's tally where the card keeps one, so a reader of the card knows how near the next readout is); Level log (Each Level with its cause and the scene it happened in, fed from the chapter-end changes blocks); Stage ledger (Each Stage with its Catalyst, re-assay, witnesses and date, one line of story each, set above the prose Temperance Record, which stays).
42. CH17 (The next gate): Next gate, every card. A line names the next Stage, its FOW Catalyst and any Band gate ahead. NPC cards add the crisis the Fronts are building; your characters' cards name only FOW's Catalyst.
43. ME1 (Where the law lands): Doc, tools and guides. A, plus the sixth edition of the Ability and Technique Design Guide, the wotr-npc, wotr-stat-line and wotr-write references rewritten, and NATALIE.md's character-sheet line updated, all in this pass.
44. ME2 (What joins the card sweep): Yes to: One estimate mark (CH7's answer applied to every card, and flags the Level law has since made exact (Borin's, Yoko's reserves) dropped); Lore against body (Each Lore read against its card body; name drift is fixed, and any other contradiction goes to CONFLICTS.md for the docket); Dashes out (Em and en dashes taken out of card bodies and Lore, carrying the prose ban from the page to the sheet).
45. ME3 (Which cards first): The Kharven room first. Lambert, Bram, Brida, Tabitha Hallenfeld and the rest of the room at Kharven-Seat get their cards first, then the other live threads, then the archive by appearances.
46. ME5 (Old entries that fail the law): Each card an agent ruling. As A, and each card's changed lines go through log_ruling as one agent ruling that quotes them and names its grounds, so you read them in CONTINUE.md and may overturn any.
47. ME4 (Proof and the order of work): Law and tools, then test. Log the law and rebuild the converter and skeleton; make the three test cards through them; play a scene where one decides a fight; amend; then sweep and rebuilds.

## 2026-10-05 — R75-17-TRAIT_ENTRY_CARRIES

Isaac's ruling: a Trait is written as one simple one-word name plus "(Primary Trait)" or its Reflection, then ONE plain paragraph. The founding sentence, rigidity line, offices held (Bias, Permission, Nucleation), Lattice property, tell, counter and cost are all still required, but they are woven into that effect paragraph as prose, never as separate field lines, tables or headers. Model: his Ferment entry for Malphas. Also amends R47-2-FIELD_FORMAT for Traits.

Context: 2026-10-05, writing the Primary Trait CLENCH: "all that other stuff should be tied into the effect" after finding the field layout hard to read.

## 2026-10-05 — R75-17-TRAIT_ENTRY_CARRIES

Isaac's ruling (ability-format questionnaire, replaces the earlier 2026-10-05 ruling on this row): EVERY ability (Traits, techniques, signatures, school arts, bloodline faculties) is written as one simple name in caps, with a short gloss after it for characters with a naming register (e.g. KUSARI · the Rot), then its kind in brackets, then ONE paragraph of any length. The paragraph carries full LitRPG figures inline (EU, % of reserve, Grade, m/s, joules; estimates marked (est.)). Belief/founding sentence is left implied, not quoted. Cost, limit and counter are always in the paragraph; offices, Lattice property and nucleation only where they read naturally. The paragraph IS the Notion page and the card entry: nothing else on it. Old field-format entries are converted when next edited or used. Amends R75-17, R47-2-FIELD_FORMAT, R17-5-TRAIT_SCOPE (Lattice property now optional on the page) and the technique-entry format in the Ability Technique Design Guide.

Context: 2026-10-05 ability-format questionnaire, answers at imports/drafts/ability-format-questionnaire/answers.json. Model entry: his FERMENT (Primary Trait) for Malphas.

## 2026-10-06 — R76-2-FIGURES_INLINE

Isaac's ruling: no figure carries an (est.) mark anywhere, on an ability write-up or on a card. Ability write-ups carry full LitRPG figures inline (EU, % of reserve, Grade, m/s, joules), every figure written plainly with no estimate mark. An estimate is still canon on use and a source value still beats it on contact; which figures are estimates is kept in the author notes, never on the page. Supersedes R76-2-FIGURES_INLINE and R75-31-MARKING_ESTIMATE.

Context: 2026-10-06, Geturo's OPUS (Primary Trait): "get rid of the est" then "yea lets get rid of that rule est is annoying".

## 2026-10-06 — R48-45-CHECKS

Isaac's direction (2026-10-06): every scene, and every piece Isaac asks to have improved, extended or made better, gets a cross-read by the other model before it is posted. Claude drafts, then asks ChatGPT (ask_chatgpt); ChatGPT drafts, then asks Claude (ask_claude). Order: verify_scene clean, then the cross-read with the line-editor brief, then revise (every beat Isaac wrote kept), then verify_scene again. One round for a turn or an improvement, two for a set piece. The foot says what was kept and declined. If the other model fails or takes over five minutes, post without it and say so in one line. This widens R48-45's full check; it does not replace verify_scene.

Context: Asked in the Claude Code session that built ask_chatgpt / ask_claude; supersedes the earlier default where quick table turns skipped the cross-read.

## 2026-10-08 — R48-45-CHECKS

Isaac's direction (2026-10-08): the cross-read runs only when Isaac asks for it ("cross-read", "cross-check", "ask ChatGPT", "ask Claude", "second opinion"). Nothing goes to the other model by default, on any surface; when he asks, the 10-06 procedure applies unchanged (verify_scene, line-editor brief, revise keeping every beat, verify again; one round, two for a set piece; foot line only when it ran). Supersedes the 2026-10-06 every-time ruling.

Context: Asked in a Claude Code session: "set it up to only do the cross check if I ask". Applied to desktop/NATALIE.md, desktop/CHATGPT_INSTRUCTIONS.md, desktop/chatgpt-skills/wotr-ask-claude, and the wotr-chatgpt, wotr-write and wotr-rp skills.

## 2026-10-08 — R70-100-MARTIAL_VOCABULARY_NAMES_MOVES

Isaac, 2026-10-08: no HEMA or European fencing-manual terms in WOTR prose, for every character, post, scene and book (Vor, Nach, Indes, Zufechten, Krieg, Vom Tag, Ochs, Pflug, Alber, Zornhau, Winden, Absetzen, Durchwechseln and the like). Every guard, cut, tempo and measure is described as the body doing it: where the weight sits, where the blade is held, who moves first, how far apart they stand. This supersedes R70-100's requirement to name moves in the POV's school vocabulary for European schools. It also amends the rows that require or reward that vocabulary: R13-6-HEMA_VOCAB, R13-4-COMBAT_FLOOR (tempo is still stated, but in plain words, not Vor/Nach/Indes), R13-9-VERIFY_CHECKS_22_26 (check 22, HEMA density, should stop counting these terms as a virtue and should instead WARN when they appear), and the term lists in R1-1-BLADE_GRAMMAR and R1-1-YOKO_ASSIGNED. The mechanics of those grammars (the bind, the read, the measure) still apply; only the jargon goes.

Context: Ruled while improving Dabney's tournament posts (Aetherion Class X Open Tournament, the first exchange vs Taesyn, "Where They Meet"). Isaac: "don't use the words hema words instead describe them in actions", then "I want to make sure that its like that for everything now". Open: whether Eastern school terms in narration (kesa-giri etc. for Moto POVs) fall under the same ruling. Asked, not yet answered.

## 2026-10-08 — R13-4-COMBAT_FLOOR

Isaac's direction (2026-10-08): combat roleplay never hands the opponent the how. In any roleplay fight (Desktop turn, Discord post, and above all an improvement of Isaac's combat post) the page shows what the move does and the tells a sharp opponent could read (sound, light, frost, smell, breath, stance, what repeats, what it costs the body), never the full mechanism, the figures or why it works; those stay in the author notes, the card and the Stat Ledger. In roleplay the floor (R13-4, R71-4, R12-2, R12-3, and R70-76's "full mechanism") is paid on the body and in the notes, the read and the fault shown as behaviour; a voice explains only what it has earned by reading the tells (R71-23). Applies to his PC and NPCs alike. Written set pieces and books keep the full floor.

Context: Isaac in a Claude Code session: "CRP is [not] supposed to give your opponent exactly what you're doing, how you're doing it, especially when it's improving combat; you're supposed to have some tells of how a thing works in the writing." Scope to roleplay (not written set pieces) is Claude's reading; he may widen it. Written into desktop/NATALIE.md Table Rule 6 and the wotr-rp and wotr-write skills.

## 2026-10-08 — new

Isaac's direction (2026-10-08): Natalie knows every named character's kit before writing them. She reads the card (character, fow_line) for each practitioner in the scene and has them use their Traits, techniques and skills unprompted, in fights and out of them, inventing fresh applications, combinations and tricks from what each mechanism can lawfully do, inside its cost, limit and counter. A new use that holds is canon on use and is noted for the card. His PC's kit moves only as his post moves it; in an improvement of his post, his abilities may be built out inside the beats he wrote. Pairs with the same day's combat-roleplay ruling on R13-4: the inventive use shows on the page through its tells, and its how goes to the notes.

Context: Isaac in a Claude Code session: he doesn't see the AI writing abilities, techniques and cool ideas from a character's known skill set; characters should act inside what they can do and make things from it. Written into desktop/NATALIE.md ("What you do unprompted"), scene_brief field 9a in build/mcp_server.py, and the wotr-rp and wotr-write skills.
