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
