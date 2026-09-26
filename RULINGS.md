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

