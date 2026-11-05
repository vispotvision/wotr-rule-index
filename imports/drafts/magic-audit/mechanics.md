# Magic audit: mechanics consistency

Audited 2026-11-05 against desktop/NATALIE.md, RULINGS.md, the live rules (out/rules.live.md), Fracture of Worlds.pdf and FOW_Stat_and_Magic_System_Codex.xlsx. Read-only; nothing else was changed. Findings are ordered by severity, then by how much they bite in play. Words like draw and guns were left to the other pass.

Severity: **LAW** = law disagrees with itself or a live rule. **CANON** = page breaks canon. **PAGE** = contradicts another page. **THIN** = thin or missing. **MINOR**.

Path aliases (all under `wiki/The Magic System/` unless shown):

| Alias | File |
|---|---|
| NAT | desktop/NATALIE.md |
| RL | out/rules.live.md |
| RUL | RULINGS.md |
| MS | The Magic System.md |
| HMW | First Steps/How Magic Works.md |
| MEAS | First Steps/The Measures at a Glance.md |
| ONE | First Steps/One Exchange, Annotated.md |
| VOC | First Steps/The Core Vocabulary.md |
| REL | The Soul and the Climb/Release Forms.md |
| LAD | The Soul and the Climb/The Ladder and the Draft — Temperance, Advancement and Essence Drafts.md |
| S16 | The Soul and the Climb/The Sixteen Stages.md |
| TGB | The Soul and the Climb/Tier Grade, Bands & the Aether Shell.md |
| WIN | The Soul and the Climb/Windows and the Sheet.md |
| AC | The Soul and the Climb/Aether Classes.md |
| COL | The Soul and the Climb/The Color of Essence.md |
| CONC | The Soul and the Climb/The Concordant Crystal.md |
| STK | Power in Use/Stacking and Spending.md |
| RNF | Power in Use/Reinforcement.md |
| CTR | Power in Use/Counterplay What Beats a Practitioner.md |
| RUN | Power in Use/Runes and Tags.md |
| TRD | Power in Use/The Four Crafts.md |
| BLS | Practice and Institution/Blessings and Curses.md |
| GATE | Practice and Institution/The Gate Who May Learn Magic.md |
| STD | Practice and Institution/The Standing and the Title — The Three Names.md |
| TRN | Practice and Institution/Training and Sects.md |
| LMP | Practice and Institution/Who Pays for the Lamp The Living Crafts.md |
| DRV | Practice and Institution/The Derivation of Practice — Thaumaturgic and Theurgic.md |
| TWO | The Foundations/The Physical Account Two Sets of Books.md |
| FAM | The Foundations/The Eight Families & the Sixty Wellsprings/The Eight Families & the Sixty Wellsprings.md |
| CS | The Foundations/The Descent of Parun — The Fourteen Hands/The Counted Speech — A Speaker's Grammar of Parun.md |
| LEX | Reference and Craft/The Lexicon of Magic — Master Terminology.md |
| CAT | Reference and Craft/The Magical Categories — Unified Taxonom.md |
| VOK | Reference and Craft/The Working Vocabulary — Trade Jargon and Its Metaphysical Extensions.md |
| HUB | Fracture of Worlds — The Living System/Fracture of Worlds — The Living System.md |
| F1 to F9, FX | Fracture of Worlds — The Living System/I. through IX., and X. pages |

---

## A. The law against itself and against live rules

### A1. LAW: two η ladders give one Stage different η, and "Aether Class sets η" has no class below Glory
- NAT:243 "Aether Class sets eta"
- RL:89 "η is 0.60 to 0.70 at Stage VI–VII"
- RUL:552 "Glory is Class I Muridic; Refraction is Class II"
- F7:54 "Late Refraction, Resonant Crystal. **Five to ten percent loss.**"
- F7:206 "V–VII Splintering to Refraction | 0.60–0.70"
- F7:58 "Early Master, Radiant Crystal"
- F7:207 "VIII–X Transcendence to Realization | 0.70–0.80"
- F7:50 "**Stages I through V are unclassed"
- TGB:291 "Neither has been withdrawn."

A late-Refraction Class III reads η 0.90 to 0.95 by one table and 0.60 to 0.70 by the other; Transcendence reads 1.0+ or 0.70 to 0.80. R42-2 (C-020) and R44-4 (C-037) are both live, two days apart. R44-5 (tables typical, card governs) softens it for cards and does not say which table is the rule. Stage V also got 0.60 to 0.70 by the Tier 5 rollup, though R44-4 names only VI and VII and the canon PDF gives about 0.50.

**Fix:** log a ruling under Natalie's authority: the class tier sets η from Glory up (newest word, R84-10 and NAT:243), and Part Nineteen's Tier table is relabeled the unclassed baseline for Stages I to V plus a field average above; then TGB:289-291 and MEAS:28 change to say so, because a law line outranks a typical-values table.

### A2. LAW: the AU/s formula is misworded in the law and applies η twice in the Ledger
- NAT:159 "AU/s = Flux times eta"
- RL:88 "where a card's AU/s is not Flux Density × η"
- MEAS:11 "Flux for the force a working carries"
- F9:23 "**AU/s = Flux Density × η**"
- F9:180 "| Power delivered | AU/s × η × 1 MW | watts |"
- F9:189 "Flux Density 290 EU/g, output 258.1 AU/s, η 0.89"
- F9:194 "258.1 MW spent, 229.7 MW delivered"
- F7:144 "that figure does not depend on the conversion at all"
- F7:173 "the benchmark rate is the benchmark reserve spent inside a single turn"
- F9:25 "because it determines how long the reserve lasts under continuous output"
- STK:76 "a wasteful fighter runs dry first"

Recomputed: 290 × 0.89 = 258.1, and 258.1 × 0.89 = 229.7, so delivered power in the worked example is Flux Density × η². By the formula a higher η raises AU/s and empties the reserve faster, while F7:144 says drain does not depend on conversion and F9:25 says η is what makes a reserve last. The two statements reconcile only per unit of delivered effect, and no page says so. In the law, bare "Flux" is the Ardency Sub-Stat everywhere else, so the line reads as a different formula. F9:274 does address the EU/g against EU/s units.

**Fix:** NAT:159 changes to "Flux Density" (R44-2 is Isaac's ruling); then a logged ruling states whether AU/s is rate spent or rate delivered, and F9:180 and F7:144 follow it, because the formula outranks the gloss. F9:25 and F7:136 gain "for the same delivered effect".

### A3. LAW: the two-Grade cap has three baselines, and its relation to the Stage ceiling is unstated
- NAT:251 "Boosts stack to two Grades over the Grade on the card"
- RL:274 "Boosts stack to +2 Grades"
- STK:21 "above what the practitioner's Soul Crystal"
- HMW:176 "two Grades over what a fighter can sustain"
- ONE:149 "two Grades over her sustainable B"
- F2:80 "Temperance Stage functions as a hard ceiling on every Sub-Stat"
- F2:84 "generate Crystal Fracture Events at an exponentially increasing rate"
- ONE:134 "352, A, strikes as S in that fist"
- STK:31 "It stacks freely and adds no risk to the one receiving it"

R78-10's verbatim says "two Grades above the sustainable level". For a Flux C at Stage VI, "the Grade on the card" caps at A while "what the Crystal holds safely" could read as SS. Garrick's boost carries him past his Stage VI ceiling of 400, which F2:80 calls hard, and F2:84 names "external metaphysical imposition" as a fracture cause while STK:31 says outside help is riskless.

**Fix:** the law's wording governs as newest: every page says "the Grade on the card"; F2:80 and F2:84 add that a transient boost passes the ceiling lawfully and only a lasting forced stat takes that fracture rate.

### A4. LAW: the Domain and Release ladder is circular on the lived road
Law on its own terms agrees with itself: Second from VII, it opens and powers the Domain, anyone at VIII can have one (NAT:71, NAT:249). The problem is what sits underneath.
- NAT:249 "First, Second and Third Release from Stage IV, VII and IX"
- F2:197 "First Domain seed activation, however fragile or small."
- S16:212 "first Domain seed activation, however fragile or small"
- REL:33 "VII, Refraction"
- REL:43 "The Second Release opens and powers the Domain"
- REL:63 "Far fewer earn a Second."
- S16:223 "A practitioner who cannot produce a Domain seed or pay for one does not slow down."
- F2:201 "The practitioner consolidates their Domain into a Realm capable of holding other Domains."
- REL:43 "The Third Release turns it into a Realm"
- REL:33 "IX, Invocation"
- F6:48 "Domain (a space where a soul's inner law becomes local reality) seeds become structurally stable."
- F8:129 "The first fragile, flickering territory."

To reach VII on the lived road you must fire a seed, which only a Second Release opens, which cannot exist below VII. Every lived Stage VII would then hold a Second, yet "far fewer" earn one. The same loop runs at IX: the Catalyst is a Realm, and only a Third (from IX) makes one.

**Fix:** a ruling: the Catalyst's seed is a one-time flicker of the Trait at the Threshold, and the Second Release is what later lets it be called and held; the Catalyst into IX is a first Realm-like flicker likewise. F2:197, F2:201, F6:48 and S16:212 add that sentence; the Release table stands because R78-10 and R84-17 outrank FoW's Catalyst wording.

### A5. LAW: Grade blurbs put Domains at Stages that cannot have them
- F2:58 "Domain seeds (first roots of a space where the practitioner's law overrides local law) structurally possible though not stable."
- F2:60 "Domain architecture active rather than potential."
- F2:62 "Domain live and law-bearing."
- F8:131 "The first true Domain."

Grade C is reachable at Stage III and Grade A at VI. The blurbs are in the canon PDF and the Stat Sheet, so this conflict sits in canon itself; R78-10 and R84-17 outrank them.

**Fix:** rewrite the F2 Grade blurbs to defer to the Stage (seed at VII, Domain at VIII), and soften the echo at FX:471.

### A6. LAW: older sections of the law still contradict R84 where the precedence clause has to do the work
- NAT:253 "A breakthrough meets its Catalyst by crisis, seclusion (months, guarded, slag risk) or tribulation"
- NAT:71 "Drafts and blessings can supply a Catalyst"
- RL:1243 "Breakthroughs by crisis, seclusion or tribulation"
- RL:733 "A Stage breakthrough is written from the body inside the danger that is its Catalyst"

The clause "where an older rule reads otherwise, this section wins" (NAT:63) resolves these, but the sentences stay in place and get read alone.

**Fix:** NAT:253 adds "or a Draft or blessing, see THE SHEET AND THE CLIMB", and R78-7 and R70-91 get `amends` notes; R84 wins as newest.

### A7. LAW: items on two ladders inside the law
- NAT:83 "Items carry a Grade for power and a Rarity for scarcity"
- NAT:55 "on the existing Tier ladder (R82-35)"
- NAT:255 "One item ladder decides out of sight."
- NAT:251 "items work at their own Tier"

**Fix:** NAT:55, NAT:251 and NAT:255 read Grade and Rarity, because R84-20 is newest (the wiki's Item Tiers page already follows it).

### A8. LAW: windows and live rows on what a readout may print
- NAT:65 "EU, AU/s and η stay in the notes."
- NAT:245 "they live in mouths"
- RL:2287 "A readout may mark a Level gained with the stat points it brought"

R81-3 lets EU live in mouths and notes; R84-2 says notes. R70-84 lets a window print stat points, while WIN:75 says raw values never show.

**Fix:** NAT:65 gains "and mouths", and R70-84 is amended to a bar of points to place, since R84-2 is newer.

### A9. MINOR: "no release invented on the page" against "a scene wins"
- NAT:249 "none is invented on the page outside its card"
- NAT:49 "A scene wins: whatever is on the page in an archived scene is written back to the card at scene end (R82-1)."

**Fix:** NAT:249 narrows to a new Release needing a card line first or written back at scene end, because R82-1 is newer.

### A10. MINOR: the ladder's name in the law is short
- NAT:69 "the old ladder, Muridic through Radiant, is its tier"
- MS:145 "VI Voidic, Ω Absolute"

**Fix:** NAT:69 reads "Ø Dormant through Ω Absolute".

---

## B. Pages that break canon or the law

### B1. CANON: Measures says a Third Release fractures the Crystal
- MEAS:27 "A Second Release leaves a Crystal Overgrown till morning, a Third leaves it Fractured."
- REL:79 "Overgrown for a day and a night, and an ache through the body like the end of a fever. No lasting harm"
- REL:73 "the Crystal carries it without structural damage"

R78-10: "a learned release spreads the strain so it does no structural damage inside its limit".

**Fix:** MEAS changes to Overgrown, because a live Isaac direction outranks it.

### B2. CANON: Part Eleven keys Pressure to the wrong stat and scale
- F3:198 "Governed primarily by **Harmonics**"
- F3:190 "It increases monotonically with Tier Grade and Temperance advancement"
- F3:196 "The F-Grade practitioner's knees bend."
- NAT:243 "Stage gap and Dominion for Pressure"
- NAT:247 "one Stage up bends attention; two, sweat and nausea; three or more drops people"
- NAT:247 "The unwoken take the Aura table by Grade"
- F3:194 "At **C-Grade**, measurable physical effects begin."
- F2:60 "Aura begins generating passive environmental pressure."
- F6:44 "The Aura begins generating genuine environmental effects."

Three different onsets for physical Pressure, and the Grade table is applied to practitioners when the law keeps it for the unwoken. A against F is at least five Stages, so the law drops that person rather than bending their knees.

**Fix:** F3 re-keys to Stage gap plus Dominion and labels its Grade rows as the unwoken table; F2:60 and F6:44 follow, because the law outranks these lines.

### B3. CANON: a bought Stage is given a reserve it does not have
- CTR:78 "He has the reserve and the Grades on the sheet"
- TRN:72 "A fighter who bought their Stage carries the reserve"
- TRN:90 "with the deepest reserve on the river"
- STD:34 "A Draft-bought Stage moves every figure on this line"
- LAD:46 "**Level.** The architecture sits thin"
- S16:54 "The new ceiling sits empty until danger overcome fills it"
- F9:90 "A reserve is set by **Level** and capped by **Stage**."

Recomputed by the law of reserves: an unfought heir at Level 20 holds about 4,750 EU and Wil at Level 63 about 16,900 EU, so the heir does not out-reserve him.

**Fix:** these four lines say "the ceiling, the door and the color, thin underneath", because R84-4 and R84-5 stand and the Ledger is canon.

### B4. CANON: a blessing wakes someone with a class
- BLS:63 "The whole window opens, with Essence and a class"
- AC:51 "waking opens the rest of it without yet naming her"
- RL:319 "Aether Class emerges at Glory"

R84-40's "no class until waking" is loose; R42-2 and Aether Classes are explicit.

**Fix:** BLS reads "with Essence and Stage I".

### B5. CANON: three pages say the System does not track the unwoken
- F3:228 "the System does not begin tracking a soul until the Crystal has opened"
- F2:50 "Most characters have already left it before they enter the System."
- HUB:30 "Every practitioner carries a private copy of this ledger."
- WIN:36 "**Everyone has one, the unwoken included.**"
- NAT:65 "Everyone has one, the unwoken included"

**Fix:** F3, F2 and HUB change, because R84-36 and R84-40 are newest.

### B6. CANON: Level has sources the law no longer allows, and pages say so three ways
- MEAS:19 "Moves by danger overcome, never by drill"
- TRN:25 "The only thing that raises Level"
- BLS:58 "A blessing is the one thing that can move Level without danger overcome"
- F1:58 "by long breathing and pulling at a Wellspring site or in dense Aether, and by seclusion before a Threshold, generates slower but persistent accumulation."
- F1:60 "Moderate XP"
- F1:64 "generates XP commensurate with the weight of what is risked"
- TWO:69 "A Crystal densifies when it is driven to the edge of its structural tolerance"

R84-4: Level moves by danger overcome; R84-13: a blessing can grant it.

**Fix:** F1's Gnosis Events, oath pulses and channeling are reworded as Stage pressure or tempering (or Isaac keeps them as danger of another kind), TWO:69 follows, and TRN:25 adds "barring a blessing".

### B7. CANON: Thyra Ketilsdottir holds a seed with no fight and no call
- F8:10 "from a woman who had never fought anybody in her life"
- REL:67 "A release must be found and mastered by fighting"
- F8:117 "it is called aloud, and it forms as it is named"

**Fix:** amend the story or state that a seed can flicker before any Release (this hangs on the A4 ruling).

### B8. CANON: a Domain described as not chosen, and costed by retired logic
- TGB:299 "a character does not choose to deploy a Domain the way they choose to throw a punch"
- F8:117 "A character does not choose to deploy a Domain the way they choose to throw a punch."
- NAT:249 "which is called aloud and forms as it is named"
- F8:117 "Domains are not techniques. They are consequences of sufficient Temperance, Dominion"
- NAT:71 "Anyone at Stage VIII can have a Domain"
- TGB:301 "**Anyone at Stage VIII can have one, their own concept made real,**"

TGB never mentions the Second Release at all; F8 half-reconciles by appending it.

**Fix:** both pages say the Domain is grown and then called, and TGB adds the Second Release, because R84-17 and R81-11 wording governs.

### B9. CANON: Domain clash ignores the read
- F8:159 "**First, Temperance differential.**"
- REL:45 "contest the ground by Dominion"
- HMW:178 "Dominion decides who holds the room, and a sharp read can flip it"

R78-10's verbatim: "when fields clash Dominion holds the ground and a read can flip it". FoW's first-tier overwrite at two Stages stays canon and neither source mentions the other.

**Fix:** F8:159 adds the read as a tier and REL states the overwrite at two Stages, each page carrying both, since neither Isaac's direction nor FoW withdraws the other.

### B10. CANON: Stage VII is given an S that canon refuses
- STD:68 "B* → A → S"
- F2:94 "A, allocation stops at 400; late push toward S entry"

**Fix:** STD reads "B* → A → A*", matching its own star use.

### B11. CANON: a retired or foreign name used as a Wellspring
- F3:222 "Vohrin adds thermal extraction."

Vohrin is not among the Sixty in F5 or the Caloria page; it is a Titan.

**Fix:** F3 names a real Wellspring mechanism or attributes it to a Titan source.

### B12. CANON: named crafts survive after R84-18
- VOK:131 "for *Ars Cantus* and every chanter"
- TRD:18 "No such kinds exist"
- NAT:83 "There are no named crafts"

File names "The Four Crafts.md" and "...The Living Crafts.md", and TRD's Ars register as a kinds table (TRD:109-114), also still read as categories.

**Fix:** drop or mark as guild jargon, rename the files in the wiki pass, because R84-18 is newest.

### B13. CANON: Traits described as innate only
- CAT:164 "They are woven into a soul's original Essence"
- F8:28 "Forged through trauma, revelation, sustained Wellspring"
- RUL:3743 "your body gains traits etc."

**Fix:** CAT:164 narrows to Primary and Inherited Traits; Isaac's 11-05 words stand, and "Traits are exactly as on file" keeps F8.

### B14. CANON: Path gates called a limit on the climb
- GATE:26 "decide how far a woken Crystal may climb"
- LAD:32 "there is no rung of the ladder where the law says otherwise"

Path gates cap a Sub-Stat past a Grade, and bought Stages walk past them without opening them (LAD:48).

**Fix:** GATE reads "how far a stat may rise".

### B15. CANON: Saturation doctrine computed on the wrong Stage
- FAM:243 "A Zenith field a kilometer across puts about a fifth of one AU/s through each square meter of its edge, a five-hundredth of threshold."
- CTR:32 "A Zenith working a kilometer wide is a five-hundredth of threshold."
- CTR:32 "you cannot flood a field, only a building, and you have to be inside it."
- F7:189 "2.59×10^8"
- F7:184 "710,000"

Recomputed over a sphere of radius 500 m (3.14 × 10⁶ m²): 710,000 AU/s gives 0.226 per m², the page's figure, which is the Stage VIII to X benchmark. Zenith's benchmark gives 82 per m², and the top of its band (1.12 × 10⁹) gives 357, over the threshold of 100.

**Fix:** FAM and CTR relabel to a Master and limit "you cannot flood a field" to below Archmaster, because the AU/s table is the computed side.

### B16. CANON: waking roads omit the Waking Draft
- GATE:22 "a crisis, a master's forcing or a tribulation"
- WIN:165 "A Waking Draft is very dear and often kills or warps a child"

**Fix:** GATE adds the Waking Draft and the waking blessing, because R84-37 is newest; TRD:230-232's "cannot seat in him" is scoped to ordinary Drafts.

### B17. CANON: Crystal written as separate from the soul
- GATE:17 "seals and goes on sleeping while the soul around it refines"
- VOC:146 "A Trait belongs to the soul; the Soul Crystal only arms it"
- LMP:103 "the soul's power-organ"
- GATE:15 "The Crystal is the soul"
- NAT:259 "The Soul Crystal is literally the soul"

**Fix:** these read "a sealed Crystal" or "the open Crystal", as TRAIT:42-44 already does, because the 11-05 line is Isaac's.

### B18. CANON: Retired coherence term
- CONC:12 "one eta, and one Coherence Band"

R44-6 and F2:106 retire the lettered Coherence Bands (Isaac ruled the mechanism earlier, on 09-12).

**Fix:** drop "one Coherence Band" or read it as Tier of Standing.

---

## C. Pages against each other

### C1. PAGE: showcase windows spend about twice the stat pool
Part Three is law for sheets (R39-1, R38-2); the examples below do not compute. Minimum to read each window's Grades, using the bottom of each band × 8 (× 7 for Dominion):

| Fighter | Level, Stage | Pool (levels + Thresholds) | Minimum the window needs |
|---|---|---|---|
| Wen Talley, HMW:39-41 | 47, III | 564 + 600 = 1,164 | 2,733 |
| Garrick Vane, MEAS:62-65 | 160, VI | 2,100 + 2,100 = 4,200 | 7,435 (taking Ardency at the page's 2,080) |
| Corra Vell, MS:131-134 | 196, VII | 2,640 + 2,800 = 5,440 | 10,963 |
| Mun Seo-yeon, TGB:134-138 | 170, VI | 2,250 + 2,100 = 4,350 | 10,613 |

- F1:114 "A Band II practitioner reading B with an A ceiling above him is the correct shape"
- F1:124 "If they are B-Grade, their stats are broadly B-Grade."
- MS:133 "[Vitality A · Ardency A · Gnosis C · Dexterity B]"
- TGB:137 "[Ardency B · Vitality C · Gnosis A · Dexterity A]"
- HMW:40 "[Vitality D · Ardency C · Gnosis E · Dexterity D]"
- MEAS:64 "[Vitality B · Ardency B · Gnosis D · Dexterity C]"

Race and lineage "shape base stats" (R84-9), but no page gives a base-stat figure that could fill the gap.

**Fix:** re-grade the four windows to fit, because the newest law keeps the point economy and these are illustrations; or Isaac rules a base-stat allowance and F1 adds its number.

### C2. PAGE: an aura in full Family hue below the Stage that can show one
- COL:41 "**Smoke-brown.** The first genuine clearing."
- COL:43 "**Fracture-streaked.**"
- REL:41 "At Stage IV that is a dark gray flare with the hue only hinted"
- HMW:86 "His fist glows the ember-orange of his aura"
- F9:11 "His aura went up scarlet and gold"
- F6:12 "Her aura, a modest apple green all her life"
- STK:9 "until they glowed ember-orange through her shirt"
- RNF:57 "the coat comes up arc-blue over her forearms"
- ONE:60 "with filaments of brighter blue crawling through the darker field where Splintering had cracked her"

Wen and Wu are Stage III, Ziyan IV, Sigrun and Mags V. One Exchange and the Hathersage story get it right. Law (NAT:249, R78-6) says a constant visible coat in their own color, and the Tone section wants color everywhere; COL and REL sit under that.

**Fix:** if Isaac wants color at every Stage, the Refinement Spectrum's bottom rows are the side to change (the Tone is newer than COL); otherwise recolor the five stories. Natalie's call, logged.

### C3. PAGE: Stage V's instability line
- S16:71 "B, instability above 320"
- F6:40 "instability risk above 320"
- F2:82 "276 to 350, 401 to 475, 551 to 625, 726 to 750, is the instability zone"
- F1:118 "276 to 350 is its instability zone"

320 is the PDF and Stat Sheet figure; the instability-zone ruling in RUL (line 401) replaced it.

**Fix:** S16:71, S16:173 and F6:40 change to the ruled band.

### C4. PAGE: Residual Strain meters levels the counter will not give
- F2:240 "Every fifty levels spent above a Band ceiling"
- F1:20 "The System will simply halt the level counter"

Both are in canon sources.

**Fix:** F2:240 meters by XP accrued at the halted ceiling, because the gate is called hard by F9:103.

### C5. PAGE: time to a tenth, misstated
- STK:66 "A working started at half reserve has half its time left."
- F9:178 "| Time to Starvation | 0.9 × EU reserve ÷ (AU/s) | seconds, to the ten-percent floor |"
- REL:111 "[Time: ██████░░░░ two minutes left]"
- REL:112 "[Reserve: 47%]"
- REL:103 "From a full reserve it holds about three minutes"

Recomputed: drain to the tenth from half is 0.4/0.9 = 44% of the time. Corra at 47% on a three-minute clock has (47 − 10) ÷ 30 per minute = 1.2 minutes, not two.

**Fix:** STK reads "a little under half", and REL's window reads about a minute (or a reserve near 70%).

### C6. PAGE: Overgrown has two durations
- REL:79 "until a full night's sleep"
- VOC:85 "permanent set"
- CTR:68 "Overgrown"

**Fix:** VOC:81 states that the State clears and only an overfill set stays.

### C7. PAGE: collapse with and without a shockwave
- F8:171 "Collapse produces a **Resonance Shockwave**"
- REL:105 "his field goes out like a doused lamp"

**Fix:** REL gains the shockwave or F8 scales it to nothing for a seed, because F8 is canon and its own opening story pays that bill.

### C8. PAGE: where a working's joules come from
- TWO:45 "The practitioner does not supply the joules."
- TWO:47 "The energy was in the room."
- F9:36 "Energy delivered = EU × η × 1 MJ."
- CTR:28 "he has what he walked in with"

R83-9 and the Ledger: Aether is pulled, refined, held and spent.

**Fix:** TWO changes to the refined-Essence account, with the stratum supplementing only above η 1.0 (F9:308).

### C9. PAGE: ground as an output ceiling
- FAM:228 "the ceiling on a practitioner's output i"
- VOC:42 "Sets the ceiling on the AU/s output a practitioner can achieve in that location"
- LMP:18 "Hale was holding eleven hundred threads out of a single reserve"
- F7:177 "| 452–8,380 | 1,950 |"

On ordinary ground the site's supply at the E-Grade authority radius is a few thousand times short of the Stage I benchmark, and it only closes around A (delegated recomputation, assuming the field equals the authority radius).

**Fix:** FAM and VOC call it the ceiling on sustained output and refill, with bursts spent from reserve, because the AU/s table is the computed side.

### C10. PAGE: which layer is outermost
- BLS:249 "the outermost of the Crystal's three parts"
- LAD:76 "Attraction Layer (outer layer: bonds, Domains, Wellspring ties)"
- F1:62 "the Crystal's outer layer"
- HMW:54 "the Crystal's outer skin"

**Fix:** BLS and LAD call the Attraction Layer the Fate-Plane layer, because the Shell's outer gloss is on nearly every page.

### C11. PAGE: Saturation against natural density
- FAM:243 "Saturation begins at **ten thousand EU per cubic meter**"
- VOC:46 "Produces Crystal Fracture Events in everyone exposed"

FAM:235-236 put every Nexus and Core natively above that, and the Walking page reports bleed and law replacement there, with no Fracture Events.

**Fix:** FAM and VOC count Essence left above the ground's own density.

### C12. PAGE: a rough seat caps title, though the title sits on the Stage
- S16:417 "a rough seat caps certifiable rank at Tier Four regardless of demonstrated capability"
- MEAS:22 "In a fighting guild the title sits on the Stages and measures nothing the Stage has not already measured."
- LAD:14 "a genuine Expert"
- F2:106 "Fighting guilds, adventurers' guilds included, read the title off this table"

**Fix:** S16:417 and S16:438 say a rough seat bars an appointment or certificate above the token, because R84 titles read off the Stage table.

### C13. PAGE: stat spread and brackets
- F2:28 "It does not move them between brackets."
- F1:112 "Spread evenly that is 35 a Sub-Stat, E-Grade. Concentrated into fifteen entries it is 147, C-Grade"
- F2:30 "The institutions measure the mean. The fight is decided by the peak."

**Fix:** cut the bracket sentence in F2:28 and F1:124.

### C14. PAGE: blessing as outside help goes beyond the rule's list
- STK:31 "a Grade held up by a"
- REL:85 "a blessing may count as outside help"
- BLS:59 "It is outside help"
- NAT:251 "only outside help (allies, an ally's Domain, arrays)"

R81-12 reads "allies' Domains, arrays and outside help", so this is lawful only on that last phrase, and the law's parenthesis reads as closed.

**Fix:** NAT:251 adds blessings to the list, or a ruling excludes them; the pages agree, so the law's list is the side to settle.

### C15. PAGE: an alchemist's title capped at Five
- F8:88 "up to Five"
- F2:106 "are the same in all of them"

**Fix:** F8 drops the cap on a bench alchemist unless Isaac wants it, because the nine titles run in every guild.

### C16. PAGE: Part Eleven's stat governance
- F3:134 "degrades according to"
- F3:70 "converts Essence expenditure into sustained mechanical output"
- F3:212 "Dominion Sovereignty"

F2:151 and F4:59 put range on Cascade (Spirit gate), F4:101 keeps Economy positional, and F2:175 gates Sovereignty past A behind Fate, not Attraction.

**Fix:** F3 changes to Cascade, Constitution or Yield, and Radius and Gravity.

### C17. PAGE: small named contradictions
- F6:66 "**Ardency Overflow, Ardency Overchannel and Resilience Persistence"
- F4:163 "Overflow"
- CTR:88 "A vow broken is a Shear Break"
- F8:78 "after they repeatedly deny the truth that birthed it"
- TRN:90 "Vane's father"
- GATE:59 "outer disciple, inner disciple and elder"
- TRN:43 "core"
- AC:68 "a Shell can climb on a purse"
- AC:115 "which climbs through refinement alone"

**Fix:** Overflow is Tempering's in F6; R84-26's vow breach "lands at once" and can trigger a Shear Break; TRN reads Tressilian's; GATE adds core disciple; AC:68 names one of the four roads (Forge Rites or Infusion) so a purse has a lawful way through.

---

## D. Thin or missing

### D1. THIN: what a Domain adds to the stack
- STK:31 "a Domain (a space where one soul's law outranks the world's) someone else holds"
- WIN:205 "[Ardency: two Grades up · cap reached]"
- RL:85 "The user's own Domain, releases, vows and Drafts all count toward the two-Grade cap"

STK's table has no row for the user's own Domain, and no page says how much it adds.

**Fix:** STK adds the row, with a number from a ruling, because R81-12 requires that it count.

### D2. THIN: a crossbow bolt cannot do what the law says, by the table
- NAT:255 "a crossbow bolt is the cheap thing that can kill a high-Stage fighter in a room"
- F3:99 "The active Essence field surrounding every practitioner above F-Grade"
- F3:110 "Survives arrows, sling stones and bladed weapons"

A bolt carries a few hundred joules. Surprise removes the coat, but the passive base table is unsplit, and even F survives it.

**Fix:** F3 gives Layer One its own figure or a surprise clause, because R83 is newest; "above F-Grade" also drops, since every practitioner's coat is constant (R78-6).

### D3. THIN: the boost cap is absent where boosts are sold
- F3:35 "Overchannel"
- CAT:370 "vow"

**Fix:** one line each saying these count toward two Grades. FoW's Overchannel multiplier of two to five times (TGB:93, STK:30) is also not expressed in Grades, so a window cannot print it.

### D4. THIN: low-Stage buying undefined
- FX:200 "here or on a higher rung"
- F2:183 "A Draft or a blessing can supply a Catalyst"

Catalyst Drafts start at the Elixir rung, about 46,020 EU, while S16:116 and S16:451 have house children drinking through low Stages.

**Fix:** FX states the low-Stage case.

### D5. THIN: reserve for a soul with a Level and no Essence
- WIN:62 "It holds a Level, a few trade skills and her health, with no Essence and no class"
- F9:90 "A reserve is set by **Level** and capped by **Stage**."

Level 1 reads 2,710 EU by the law; Hanne Oster at Level 6 has none and Marta Kell jumps to 23.

**Fix:** F9 adds that the law of reserves runs from waking and states what Level does in a sealed Crystal.

### D6. THIN: Zenith by purse
- S16:456 "Whether a Throne can be brought to recognize what a purse has built is the oldest open fight among Measurewrights"
- LAD:32 "there is no rung of the ladder where the law says otherwise"

**Fix:** Natalie rules it under "Nothing waits on Isaac", since R84-5 reads universal and F2:211 calls it recognition.

### D7. THIN: smaller gaps
- LEX:98 "Domain"
- F3:206 "Physical"

Lexicon's Domain entry lacks the Second Release, seed and true split, and duration. Lexicon's Aether Class (LEX:285), Field Manual and HUB:70 omit the first offer at Glory. The Stage upset limit (NAT:159) appears only on HMW-side pages, not LEX:191. F3 lists three Paths' modifiers with no Fate line. F4:55 Penetration omits worked armor (NAT:243). TRD has no line on fight Drafts (beat, refill, crash, threefold price), though STK and LAD do. "Tiers" in Stage V's Catalyst (F2:193, S16:175, LAD:60) is ambiguous now that Tier means a title.

**Fix:** add each, citing the page that holds it.

---

## E. Minor

- **MS:27** "in twenty-two Parts across eight pages": the workbook is 24 Parts across ten pages. MS:261 omits IX and X.
- **VOC:190** "anyone can level them" against **TRD:224** and **RUN:17** (a woken Crystal for all but pouring). Change VOC.
- **RUN:38** "Works anywhere" against **CTR:36** and **FAM:238**. Change RUN to "short of a Silence".
- **FAM:130** "Most mortals awaken three to five Wellsprings" against **GATE:17** (nine in ten are Class Ø). Change to "most practitioners".
- **F3:218** five-fold B-Grade Strike Force is newtons only; **F3:50** gives energy a 44-fold span. Add it.
- **F3:84-86** "Lunar" at 10¹⁶ kg and "stellar" at 10²⁶ kg do not match a Moon's or Sun's mass. Fix labels.
- **F7:136** defines η backward ("Essence spent to Essence that arrives"; repeated in F9:25, TGB:269, VOC:131). Canon wording; the math reads arrives ÷ spent.
- **F7:130** "Scales with Temperance Stage" against **F7:148** "set by Level and capped by Stage".
- **FX:39** "a hundred joules" for a bolt against **FX:648** "about 440 J".
- **CTR:34** "the strongest Domain in the register is a fraction of a millimeter wide" is the S-Grade figure from **FAM:240**. Change CTR.
- **CTR:100** costs "rarely due inside a scene" against **TRD:144** and the tell ladder.
- **F5:278** "Twenty categories" against the 26 category headings on the Categories page (delegated count). **CAT:28** "four Planes" against three.
- **HMW:60, LEX:289, CAT:190** Typology as a bias to a "phenomenon" against **F7:98** "one of the eight Families".
- **LAD:58 and F6:20**: Inner Refinement is Stages I to IV on LAD and I to VII on F6. Pick one.
- **RNF:66**: Mags at 81% says "perhaps five minutes" of a five-minute-from-full coat; about 3.9 by the drain rule, unless her Expert η buys the rest.
- **Family pages** cite retired Sub-Stats (Saturation, Cartography, Nullity, Rift, Ossification, Confluence and others); every one maps through F4's merge notes, and F5:17 says the current names are used. Rename on the Family pages.

---

## F. Live rules and tools

- **R59-12-TRANSITIONAL_MILITARY** (RL:710) is still live and names rare machine guns, against R83. The other pass should catch it; flagged because a live row contradicts the law.
- **rust/src/analysis.rs:925-945** prints "Core Progression" rows from FOW_Stat_and_Magic_System_Codex.xlsx into a tool's output. That sheet still reads 20/25/30/35/40 points per Level and a 24,100 pool, retired by R38-2, and "instability above 320". I did not run it to see which rows print. Anything built from it would cost a sheet on retired figures. sources and canon files stay untouched: the tool should cap its range or carry a note.

---

## G. Could not check

- Master Codex row by row; the Glyph Index's 136 individual rows are not on the page.
- FX Bestiary rows 101-166 and most Artifact rows were not recomputed; a delegated reader sampled the rest.
- The Stat Sheet: I read only its Core Progression, Aether Class and Domain Mechanics sheets. The Color of Essence: I read Parts One to Three, not the rest.
- These pages were read by two delegated readers working from a fact sheet I wrote, and I spot-checked their citations rather than rereading the pages: CTR, RUN, TRD, all of Practice and Institution, TWO, FAM, VOC, all of Reference and Craft, HUB, F3, F4, F5, the eight Family pages, the Glyph Index and both Parun pages. FX was grep and sampled. I read The Trait System and The Four Paths by grep plus their mechanics lines.
- Whether Fracture_of_Worlds.md differs from the PDF: I used the PDF.

---

## H. Recomputed and clean

- 1 EU = 1 MJ, 1 AU/s = 1 MW, TNT conversions, and the nine-rung table.
- Reserve law: Level 1, 100, 160, 200, 300, 355, 400, 500, and the three anchor points. "Ten every 78" is 78.05.
- Bands, working bands, benchmarks and AU/s bands (reserve ÷ 6).
- Wu Jinbao: nine seconds, 2.52 GW, 127 m. Worked scales in F9, including 4.8 × 10¹⁴ EU.
- Stat economy: 9,000 + 9,100 = 18,100; 287, 35, 147, 5,500, 87, 275. Dominion's mean over seven.
- Garrick's Ardency 2,080 ÷ 8 = 260, and his reserve line in ONE: 36 + 10 + 9 = 55% spent.
- Stage names, Tier of Standing, ceilings, Bands, gates across HMW, MEAS, F1, F2, F6, F9, TGB, S16.
- Spending tells at half, a quarter and a tenth, across HMW, STK, WIN, F7 and the law.
- Pressure at one, two and three Stages across HMW, MEAS, ONE and the law.
- Crystal States and developmental tiers, Path gates (F4's 64 Sub-Stats against F2's list), Release Stages IV, VII and IX on every page that states them, and the chain (pull, refine, Essence, Shell) on every page but TWO.
