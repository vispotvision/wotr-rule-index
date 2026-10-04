# The table questionnaire: the current law of play

Research report for the table questionnaire, 2026-10-04. It maps the law that governs how a WOTR roleplay session runs today, dimension by dimension, with rule ids and short quotes, and marks each point **Settled** (a live rule or a ruled questionnaire answer already decides it), **Open** (nothing decides it, or two live texts disagree) or **Stale text** (the law is decided but a working document still says the old thing; housekeeping, not a question).

Sources: `desktop/NATALIE.md`; `out/rules.live.full.md` (session-protocol, scene-structure, adjudication, dialogue, the R48 roleplay rows); the Style Law (R70); the Combat Law (R71, cited by questionnaire id, K5, K9 and so on, since its rows are not yet in `out/`); the skills `wotr-rp`, `wotr-ledger`, `wotr-npc`, `judger`, and `wotr-write`'s `fair-play.md` and `scene-pipeline.md`; the MCP tool docstrings in `build/mcp_server.py` (the MCP is the WOTR tool server sessions call); `table/*.yaml`; the Discord bot (`bot/PLAN.md`, `bot/config.yaml`, `bot/cogs/`). The docket is empty: no pending row touches the table.

---

## 0. Settled by R70 and R71: do not re-ask

These were answered on 2026-10-03 and 2026-10-04 and are law. The questionnaire may cite them as context; it must not put them back to Isaac.

**From the Combat Law (R71, 2026-10-04):**
- **K5, standing orders in roleplay fights.** Isaac may post conditions, and "Natalie runs them exchange by exchange until the first branch they do not cover, then stops on that threat. Table Rule 1 gains this exception." A standing order is a pre-declared conditional move ("if he closes, I cut low").
- **K9, a player's fighter on the page** (all four taken): wounds as world facts (the wound, its ATLS class, that is the trauma surgeons' blood-loss scale, and what the hand can no longer do); the tell placed, the read his ("never draws the conclusion"); felt from across the room ("It covers guest players at the Discord table too"); outward cost only, the spend kept in the Stat Ledger.
- **K7, the core promise:** "a way out, always planted": every staged fight has a findable line out (a counter, ground, flight or a yield).
- **K6:** the deciding fact shows beforehand in the read, so a sharp reader can call it.
- **CW11, how fights end:** yield on terms, flight adjudicated, a code ends it, the killing's own law. **MC10:** healing inside a fight stops the bleeding only. **WT12:** proof decides, courts fight over it, declare it or it is murder.
- Readouts in a fight: three a scene, two a turn, body first, number a line after (R70-86, R70-89), restated by R71.

**From the Style Law (R70, 2026-10-03):**
- **R70-8, one law for every job:** "All four alike", roleplay turns included, readouts included.
- **R70-12, third person only** for turns, scenes and books.
- **R70-14, Kishōtenketsu** (the four-part East Asian shape: set-up, development, twist, reconciliation, with no conflict required) for quiet, travel, downtime and interlude scenes; "roleplay turns still stop at Isaac's decision."
- **R70-17, closing modes:** a turn may stop mid-crisis on a reveal or threat; a scene may close on a notice or readout; or break off before payoff.
- **R70-90, numbers climb only for a shown cause:** "a FOW XP event on the page, or training named in a downtime turn" (FOW is Fracture of Worlds, the stat system).
- **R70-97, quests as contracts:** Guild and Crown contracts posted with terms and pay; "Hooks gain a stated reward and penalty."
- **R70-104, rivals who chose to spare:** each survival "paid for on the Ledger: a debt, a scar, a witness to the mercy."
- **R70-112, the face-slap with a bill:** every public reversal of an arrogant scion "opens a Front or a Ledger debt."
- **R70-114, grimdark warmth:** each live thread carries one standing warm bond, written openly warm.
- **R70-40:** session end "flags any rotation group untouched for six scenes."
- **R70-50:** every return of a person carries one changed body detail; "The Ledger's costs show."
- **R70-78, R70-79, R70-83:** the bearer reads his own sheet in his Crystal; practitioners feel rank; narration states only the figures the POV holds.
- **R70-130, R70-122, R70-113, R70-109:** walk-on nicknames, comic names on recurring minors and villains, comic beats for carded comic voices, proverbs by age and standing.

---

## 1. Turn shape and length

**Settled.**
- Table Rule 1 (NATALIE.md): "Answer what the PC did, move the world, stop at his next decision." Never resolve a multi-decision action in one go; stop on an NPC line, a physical action, or a thing he can now see; never on an out-of-character question. Amended by K5 for fights.
- R48-28-TURN_LENGTH: "Roleplay turns run about 3,500 words (Isaac's answer: "3500")."
- R49-30-SHORT_BEATS: "Every reply is a full turn of about 3,500 words, even to a quick line or question."
- R49-29-TURN_FILL: a turn is "about half texture and talk, half the world moving."
- R48-46-WORD_FLOOR: set pieces run 5,000 words and up.
- R49-02-TENSE: roleplay turns in present tense, written scenes and books in past.
- R48-45-CHECKS: "Full check on every roleplay turn." R48-47-NOTES: full author notes in the scene file, "chat gets a short summary."
- R48-40-NPC_THOUGHTS: roleplay turns keep one italic private thought per NPC per scene (Table Rule 10; `scene-pipeline.md` adds "not per turn").
- `wotr-rp`: match Isaac's format, prose for prose, action script for action script; Natalie's own prose stays third person.
- `build/verify.py` sets both its "conversational" and "standard" bands at 2,500 to 4,500 words.

**Stale text.** NATALIE.md still carries Table Rule 2 ("Conversational 300 to 700. Standard 700 to 1,500. Set piece 2,500 minimum") and the line "Over-delivery is the standing complaint", while its own Writing Law summary (line 287) says "turns about 3,500 words." The `wotr-rp` skill opens with "shorter turns" and then sets about 3,500. The session log of 2026-09-22 already noticed a band clash. R48-28 and R49-30 are newer and Isaac's own answer; the bands are dead text.

**Open.**
- **Out-of-character traffic.** R49-30 says "every reply" is a full turn. Nothing says whether an out-of-character question ("what does Lambert's seal look like?", "can I do X?"), a ruling, or a correction counts as a reply. R48-48-EXPLAIN says Natalie explains physics "only when asked" but not in what shape.
- **Rapid exchanges.** Fast dialogue (a bargain, an argument, a quarrel in one room) at 3,500 words a reply moves slowly. K5 solved this for fights only; there is no social or travel equivalent of standing orders.
- **Where the stop falls in talk.** Rule 1 bans resolving several decisions in one turn, but a 3,500-word turn of talk must contain several NPC lines. Nothing says which of the PC's possible answers the turn may assume (for instance, whether a turn may run past a question an NPC asks him).
- **Explicit scenes played live** get the same 3,500 words by R49-30; the intimacy questionnaire owns the content, but the pacing of a live explicit turn is a table question.
- **Author notes at the table.** R48-47 puts full notes in a scene file. In the Claude Desktop project (where NATALIE.md is read) there is no file per turn; nothing says whether notes ride at the foot of each turn, at a scene's end, or only at archive.

---

## 2. How much Natalie improvises

**Settled.**
- NATALIE.md, "What you do unprompted": pitch hooks, invent NPCs with real wants, hold ninety percent of the world under the surface, "have opinions about a beat that's drifting."
- R48-26-INVENTION: "The partner may invent NPCs, places and texture mid-scene without asking, logged; bigger things wait for Isaac."
- R48-29-PACING: "travel and waiting pass in a line when nothing is at stake; the world keeps moving."
- R48-30-SURPRISES: "Big surprises (betrayal, ambush, death) only after foreshadowing a player could have caught." R71 extends it: a third party may stop a fight only if foreshadowed.
- R57-10-NEVER_RIGGED: every engagement "a genuine challenge for the PC, never rigged in either direction."
- R48-50-PUSHBACK: a drifting beat or a rule that reads wrong gets "one plain line" and Natalie keeps writing.
- `fair-play.md`: meta knowledge informs the writer, "never an outrageous advantage"; at the table, "do not rescue a player" from what he could have looked up, nor punish him for what nobody could find.

**Open.**
- **What "bigger things" means.** R48-26 says they wait for Isaac, but no list exists. Candidates: a new faction, a new Front, killing a carded NPC, a new Wellspring site, a political event that rewrites a thread, an NPC's secret that changes canon. CLAUDE.md's "Nothing waits on Isaac" and the memory note "Isaac makes the calls" (delegated work is pre-approved) pull the other way for repo work; at the table the line is undrawn.
- **Sandbox or plot.** Nothing says whether Natalie runs a sandbox (the world reacts to the PC's choices only) or steers toward planned beats (a Front's clock is a plan). Rule 4 and the Fronts imply a moving world; nothing says how hard the world may push a thread toward a set piece.
- **Natalie's own pitches.** Nothing says whether she may seed long arcs or redirect a scene beyond R48-50's one line.
- **The world refusing the PC.** Rule 3 lets NPCs refuse. Nothing says whether the world itself may refuse an action as impossible or simply let it fail on the page.

---

## 3. NPCs: wants, refusals, lies, voices

**Settled.**
- Table Rule 3: "NPCs want things and pursue them. They lie, withhold, refuse, bargain, misjudge him. If an NPC would refuse, they refuse."
- R48-36-NPC_WITS: "veteran-clever with their abilities ... never omniscient, never dumb." R70-112 keeps a humbled scion veteran-clever afterward.
- Table Rule 8: "One thing per session an NPC tells him that is wrong and stays uncorrected until he catches it." R48-42-LIES (newer): "Frequent lies: many NPCs lie for their own reasons; the player has to catch them." R49-36-LIE_TELLS: "Every lie leaves a catchable tell."
- R48-32-NPC_VOICES: Isaac "may take over any NPC's voice anytime"; R52-12-HANDBACK: "his version sticks" and the roster voice is updated.
- R52-29, R52-31, R52-32: voices from a researched real-world speaker type, comic minors allowed, casting by ear with the swap test.
- `wotr-npc`: seven mandatory fields (want, refusal line, knows, lie, voice, body, FOW line); the roster entry is proposed and `npc_set` runs "on Isaac's word only."
- Table Rule 11, R49-28, R70-54: full inventory at first sight for majors, "minors one stroke."
- R53-18-AWE: commoners hold a ranked practitioner as "half a saint."

**Data state.** `table/NPCS.md` has entries only for the Mu-jin threads (filed under two headings, "Kwon Mu-jin" and "Mu-jin"). The Kharven and Korvaeth threads have no roster entries. NATALIE.md still says "NPC Roster per thread: not yet built"; the tool exists (`roster`, `npc_set`).

**Open.**
- **Lie density.** Rule 8 sets a floor of one per session; R48-42 says "frequent" and "many." The newer rule governs, but nothing says how many lies a session carries, whether every named NPC lies, or whether a lie may be a sincere wrong belief (the roster already records believed lies, for example Agnes Tull).
- **NPC memory and disposition.** `npc_set` stores want, refusal, knows, lied_about, last_seen and voice. There is no field for what an NPC feels about the PC, what they owe him, or a grudge. Nothing says how attitudes shift or are tracked.
- **NPC wants that move.** Nothing says how often an NPC's want changes, or whether NPCs act on their wants off-screen (which is what a Front does for factions but not for people).
- **Who may die.** R48-31 makes death possible for the PC; nothing says whether Natalie may kill a carded NPC on her own adjudication, or a named NPC Isaac is fond of, without a foreshadowed line.
- **Isaac taking an NPC.** R48-32 and R52-12 settle voice; nothing says whether the NPC's choices (not only lines) pass to Isaac while he holds the voice, or whether a guest player may take one.

---

## 4. Fronts

A Front is a threat or ambition with a want and a clock of four to six escalating consequences, borrowed from Apocalypse World tabletop design; when the clock fills the Front resolves.

**Settled.**
- Table Rule 4: "Between turns and sessions, Fronts advance." Session start step 3: "Advance one Front."
- MCP: `fronts`, `advance_front` ("At least one Front advances every session"), `add_front` (four to six consequences), `set_front_clock`. `wotr-ledger` proposes "at least one per session" and an `add_front` for any new pressure.
- R58-07-WREN_GRIEF_FRONT: a grief Front, "ticks driven by who blames whom": a Front may be emotional, not only political.
- R70-112: a public reversal opens a Front or a Ledger debt.

**Data state.** `table/fronts.yaml` holds 15 Fronts across four thread names; 14 are open. Only two have ever ticked (The Accord circle 2/5, The Class Below 2/5). The rule says one tick per session; the record shows the machinery is barely used.

**Open.**
- **Cadence.** One tick per session is the floor; nothing says whether Fronts also tick per in-world week, per downtime, or when the PC ignores them.
- **Visibility.** The bot plan lists `/fronts` for "anyone." NATALIE.md's iceberg rule holds ninety percent under the surface. Nothing says whether Isaac (or Discord players) see the clocks, see only consequences as they land, or see nothing.
- **The PC's hand on the clock.** `advance_front` records "the PC's part in it or none." Nothing says whether the PC can stop, reverse or slow a Front, and by what.
- **How many live Fronts a thread carries,** and whether one is always near firing.
- **Who opens Fronts.** R48-26's "bigger things" leaves it unclear whether Natalie may open a Front mid-session.

---

## 5. The Ledger and consequences

**Settled.**
- Table Rule 7: "Injuries, exhaustion, reserve, debts, reputation, who saw what. Persists."
- MCP: `ledger_add` (categories: the dead, injuries and reserve, debts, who knows what, reputation, canon conflicts), `due` ("Pick at least one per session"), `ledger_collect`.
- R14-7-STAT_LEDGER_CONTENTS: per named practitioner, Stage, Band, Crystal State going in, what was stressed and spent, coming out.
- Consequence law: R60-01-BRUTAL_LETHALITY ("one good cut or a ball in the gut can kill"); R60-02-REAL_HEALING_TIMES ("weeks for a cut, months for bone"); R60-03-HARD_RESERVE_CLOCK; R60-04-DEATH_IS_PERMANENT; R48-31-STAKES ("Death can happen, if earned"); R48-37-COST_SHOWN; R48-38-AFTERMATH; R53-17-THE_BILL (a working on a main raises the bill); R60-11 (trace examiners and contested jurisdiction); R70-104, R70-112, R70-50 (above).

**Data state.** `table/ledger.yaml` has 65 lines, 63 open; no narrative line has ever been collected (the two collected are canon-conflict lines). `table/sessions.yaml` logs one session (2026-09-22), so `due(sessions_old)` has almost no age to count from.

**Stale text.** Rule 7 says the Ledger "Lives on the Notion Ledger page"; the source of truth is `table/ledger.yaml`, and the Notion page is generated from it.

**Open.**
- **How fast debts are called in,** and whether every line must eventually come due or some may lapse.
- **Who-knows-what propagation.** Nothing says how fast word travels (a fire's length, a week, a season) or how many witnesses make a reputation.
- **Injury at the table between sessions.** R60-02 sets real healing; nothing says whether a wounded PC may enter the next scene's fight, or how the table handles weeks of healing (skip, downtime, play through).
- **PC death in practice.** R48-31 allows it after "clear warning." Nothing says whether the warning may be out of character (Rule 1 bans an out-of-character question at a turn's end), whether maiming, capture or ruin are preferred outcomes short of death, or what happens to the thread after a PC dies.
- **Law catching up.** R60-11 and WT12 give the machinery (proof, courts, jurisdiction); nothing says how often the law reaches the PC for a killing or an unlicensed working.

---

## 6. Adjudication

**Settled.**
- Table Rule 5: no dice; the Stage gap, the read, what was spent, what the environment allows. R14-3-STATS_DECIDE_TABLE names the stat for each (Dominion for Pressure, Dexterity for measure, Gnosis for the read, and so on). R13-8-RECONSTRUCTIBLE_ADJUDICATION: the decision must be "reconstructible from the page"; a fight that resolves "because the scene needed it to" is rewritten.
- R48-35-USES: "each side invents its own" ability uses, Isaac for his characters, the partner for NPCs.
- R47-11: one combat turn is six seconds. R71 settles the rest of fight adjudication (K4, K6, K7, CW11).
- The bot plan: dice exist only as an out-of-character toy, off by default (`ooc_dice: false`).

**Open.**
- **Adjudication outside a fight.** Every stat row in R14-3 is a combat or working row. Nothing decides a negotiation, an intimidation, a seduction, a lie the PC tells, a stealth approach, a forged paper, a chase on foot, a climb, or a long ride through a storm. Rule 3 makes social outcomes a matter of the NPC's want; nothing says whether Pressure (a Stage gap felt in the body) or a reputation line on the Ledger bends that want.
- **The PC lying to NPCs.** R49-36 gives NPC lies a catchable tell; nothing says whether NPCs read the PC's lies by Gnosis, by evidence, or by their own want.
- **Showing the sum.** R48-48: Natalie explains only when asked. Nothing says whether Isaac may ask mid-scene for the deciding row, or in which voice it comes.

---

## 7. Downtime, time and progression at the table

**Settled.**
- NATALIE.md: "Downtime. When time passes, run it in one turn."
- R48-29: travel and waiting "pass in a line when nothing is at stake."
- R70-14: downtime may run as Kishōtenketsu. R70-90: numbers move only for shown cause, including "training named in a downtime turn."
- R53-09-WEATHER: "the State of Play carries the date and season"; cold, wet and thaw change what people can do.
- The bot keeps an in-world calendar (`/date today|set|advance`) and an event list (`/event add|list|done`); the Judger sets the date.
- R53-07-PRICE_TABLE and R70-48: prices quoted from the approved table whenever money moves.

**Open.**
- **Downtime shape.** "One turn" is set; nothing says whether downtime is a menu of actions (train, heal, earn, research, craft, court, travel), a free narrative, or a list Isaac posts.
- **Training yield.** R70-90 says training may move numbers; nothing says what a week of training buys, and no number may be invented. The rate has to come from FOW XP events or a ruling.
- **The world during downtime.** Nothing says how many Front ticks a month of downtime costs, or whether Ledger lines come due inside it.
- **Upkeep and money.** The price table exists; nothing says whether the PC's living costs, wages and debts are tracked at the table or only when they matter.
- **In-world time per session,** and whether threads run on one shared calendar (the bot has one date for the whole server).

---

## 8. Scene Menu, Rumor Mill and hooks

**Settled.**
- NATALIE.md: "When Isaac opens without a beat: three hooks, one from a Front, one from the Ledger, one fresh." Rumor Mill: "Two or three pieces of world news at session start in an NPC's mouth, some wrong, one a hook."
- MCP `scene_menu(thread, culture)`: hook 1 from the Front closest to ticking, hook 2 from the oldest due Ledger line, hook 3 "yours to write" from a character the archive has barely seen plus an Inventory item; a Rumor Mill reminder line at the foot.
- R70-97: hooks state a reward and a penalty; contract boards as the Draw Age quest notice.

**Open.**
- **In-world or out.** Nothing says whether the menu is an out-of-character list or arrives in the fiction (a contract posted, a runner at the door, a letter).
- **Menu frequency and size.** Three is set; nothing says whether Isaac wants it at every session start or only when he gives no beat (the text says the latter), nor whether the Rumor Mill runs every session.
- **Tracking rumors.** A wrong rumor is a lie the world tells; nothing says whether it goes on the Ledger as "who knows what" so it can be caught later.
- **Reward and penalty for menu hooks.** R70-97 requires them for hooks; `scene_menu` does not produce them.

---

## 9. Session start and session close

**Settled.**
- NATALIE.md start protocol, eight steps: State of Play, Ledger, advance a Front, canon search, FOW line (R14-2-LOADOUT_MANDATE), Standing Inventory, rule loadout and docket, then the beat or the Scene Menu. R18-6-SESSION_START_4A inserts a Master Codex query before the FOW line. `session_start(thread, scene_type)` does steps 1 to 7 in one call.
- `wotr-rp`: the opening loadout ("Previously", "Room", "Ticking", "Consequence about to land") is assembled silently: "None of this is printed."
- Close: rewrite State of Play, append the Ledger, advance Fronts, add rulings, archive, enter new Inventory texture (NATALIE.md; R16-4-EXTEND_LEXICON; R70-40's six-scene flag). R19-9-STANDING_TASK: fold the packs, "Ask once per session."
- `session_end` drafts the close by pattern-matching and logs the session; `judger` drafts it by reading an archived scene. Both `wotr-ledger` and `judger` make every write "a proposal Isaac approves item by item."

**Open.**
- **Approval of the close.** The skills require item-by-item approval of every Ledger line, Front tick and roster entry. Isaac's standing directions point the other way for delegated work ("Isaac makes the calls"; "agents finish the job"). Nothing says whether the table close is applied by Natalie and reported, or approved line by line.
- **Session cadence.** One logged session in the record. Nothing says what a "session" is (a chat, an evening, a scene) or whether `session_end` runs at every one.
- **What Isaac sees at start.** Nothing says whether a recap ("Previously") is printed, whether the Rumor Mill is the opening, or whether the first turn simply starts in scene.
- **Which threads are live.** `session_start` knows four (Sodoku Moto, Hild Ice, Kwon Mu-jin, Ilthára Korvaeth); NATALIE.md lists three State of Play pages; the Fronts file uses four other names, two of them for the same Mu-jin material. Nothing says how many threads run at once or how play rotates among them.

---

## 10. The player's character: where Natalie stops

**Settled.**
- NATALIE.md: never "think, speak, or act for Isaac's PC," nor for the other creators' characters; R1-1-RESTRICTED_CHARACTERS_EXCLUDED; R52-10-CROSSOVER (lines and choices left open when a PC enters another thread).
- R49-01-WHOSE_HEAD: "In roleplay turns the narration may go to full depth inside Isaac's character; Isaac overrules any thought that isn't his."
- R52-08-PC_IDIOM: "his play wins" over the card. R52-09-NO_LINE: Natalie drafts his line only "in a written scene," marked as a draft.
- K9: the world owns his wound, the tell and the visible cost; he owns the read and the inside. R70-78: he reads his own sheet in his Crystal.

**Open.**
- **The depth line.** R49-01 allows full interior depth; NATALIE.md forbids thinking for him; K9 B reserves the read. Nothing says what the narration may put in his head unprompted (sensation, memory, fear) and what it must leave (a conclusion, a decision, a feeling about an NPC).
- **Involuntary reactions.** A flinch, a gag at a smell, a stumble on ice, fear from Pressure (R70-69: the room first, then bodies). Nothing says whether Natalie may write the PC's involuntary body as a world fact, as K9 A does for wounds.
- **The PC's competence.** Nothing says whether Natalie may tell Isaac what his PC would know (a Moto lord's knowledge of court law) when Isaac does not, or whether that stays his to look up (`fair-play.md`: "the fun is thinking and looking things up").

---

## 11. Multiplayer and the Discord table

**Settled.**
- The server runs location channels, a roleplay forum, Tupperbox (a bot that reposts a player's message under a character's name) and Avrae (a dice bot) in its own channel.
- The WOTR bot is "fully deterministic (no LLM)" and player-facing (Isaac's call, 2026-09-13): lookups (`/wiki`, `/define`, `/character`, `/fow`, `/recall`, `/timeline`), builders (`/name`, `/stats`, `/sheet`), `/narrate`, `/verify`, `/date`, `/event`, `/scene save`. Rule, docket and conflict commands were dropped as the Judger's desk, not the players'.
- Roles: Judger (Isaac, the Archivist role; every write), Scribe, Player, Reader. A player's `/scene save` goes to the Judger's channel; the Judger archives.
- After a save, `judger` drafts the close into `bot/queue/<slug>.judger.json`.
- No dice in canon channels: Table Rule 5 and R14-3 govern.
- K9 C: a guest player's fighter is shown only as the POV's eyes and body register him.

**Not built** (ROADMAP Phase F): F1 table state in Discord (`/fronts`, `/due`, `/ledger`, `/roster`, Judger writes, a player's `/ledger propose`); F2 forum-per-thread play (`/bind`, `/scene open|close|archive`); F3 `/adjudicate` (a card naming the Rule 5 inputs, recording "the Judger's decision; it does not make one"), `/ruling`, `/propose`. PLAN §9 leaves two of Isaac's calls open: which threads get a forum, and whether players may bind to any card or only an allowed list.

**Open.** NATALIE.md says nothing about multiplayer. Every table rule is written for one player.
- **Natalie's seat.** Whether Natalie ever runs a multiplayer scene (Isaac relaying posts into a chat, or a future LLM front end), or the Discord table stays human-run with Natalie only at the close.
- **Spotlight and turn order.** Which player's decision a turn stops on; whether a turn answers every player or one; whether 3,500 words per reply (R49-30) applies when four people post.
- **Player against player.** How a contest between two players' characters is adjudicated, since neither side may be written by the other (K9, R1-1).
- **Guest PC death and consent.** R48-31 makes death possible; nothing says whether a guest player's character may die without the player's agreement.
- **Canon from guest scenes.** Whether a guest's scene changes Isaac's threads' canon, Fronts and Ledger, or runs in a separate continuity.
- **What players see.** Fronts, the Ledger, the roster: the bot plan offers them to "anyone"; the iceberg rule hides them.
- **Standing orders for groups,** and how K5 works when two players post conditions that collide.

---

## 12. Stale text and data drift (fix, do not ask)

Beyond the stale lines flagged in sections 1, 3 and 5: NATALIE.md Table Rule 1 does not yet carry K5's standing-order exception (R71's rows are being written); Table Rule 8's "one thing per session" now reads as a floor under R48-42; `scene_menu` does not produce R70-97's reward and penalty; `npc_set` has no body or FOW-line field though `wotr-npc` makes both mandatory; the Mu-jin thread is split across two names in `table/fronts.yaml` and `table/npcs.yaml`.

---

## 13. Seeds

Every **Open** item in sections 1 to 11 is a candidate question; none re-asks R70 or R71.

## Boundaries with the other three questionnaires

- **Intimacy and explicit scenes** owns consent and refusal lines inside a scene, explicit vocabulary and aftermath; this questionnaire keeps only the pacing of a live explicit turn and the Ledger consequence.
- **Mystery, horror and intrigue** owns clue design, lie tells (R49-36) as a craft, investigation pacing and horror reveals; this questionnaire keeps lie density and how lies and rumors are tracked.
- **Techniques and characters** owns card content, ability design, progression mechanics and the NPC card's fields; this questionnaire keeps how NPCs behave at the table and how training is paced inside downtime.
