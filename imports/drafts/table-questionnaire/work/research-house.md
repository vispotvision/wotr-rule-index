# House research: how the WOTR table actually runs

*Table questionnaire, work file, 2026-10-04. Read-only; nothing was edited. Quotes are short, from the repo's own files, with file and line where it helps.*

## What was read

- **The table as data:** `table/` (sessions, Fronts, Ledger, NPCs; built 2026-09-12 as Phase B), and the twelve Running Pieces pages in the wiki mirror (`wiki/The Table*Running Pieces/`), which is what Natalie reads in Claude Desktop.
- **The multiplayer side:** `bot/PLAN.md`, `bot/cogs/`, and the three judger notes in `bot/queue/`.
- **Sequence A**, `WOTR_Vaeloris_Sequence.md`, *The Cabin* I to IV (lines 1368 to 1776): four consecutive Desktop roleplay turns, Natalie voicing Verinus against a player character who is never written.
- **Sequence B**, the ten `geturo_*.md` files: a two-player Discord bout, Geturo (Isaac) against Taesyn (another player).
- **Sequence C**, the five `rovhen_*.md` files: an Academy investigation, Rovhen (Isaac) among invented NPCs.
- **Scanned for counts:** the Xanelor duel, `hiromi_*`, `mu_jin_*`, the numbered set pieces `01` to `23`, `the_war_in_the_north_i` to `v`.

Counts are for prose with the author notes cut off. "Discord turns" means the 38 Academy files (Xanelor, Geturo, Hiromi, Rovhen, Mu-jin, the Night Register pieces).

## Headlines

1. **There are three tables, not one.** A Desktop table where Natalie runs NPCs against Isaac's character (the classic GM turn); a Discord table where Natalie turns Isaac's own posts for a roster of his characters into prose and never touches the other players; and an archive table, where finished set pieces and Isaac's own long texts are filed after the fact. The law is written for the first. Most recent play is the second.
2. **Turns are about half the length the law asks for.** Discord turns run a median of 1,506 words (range 683 to 3,599); only 2 of 38 reach 3,000. The Cabin turns run 2,498 to 3,111. The live rule is about 3,500 for every reply (R48-28, R49-30).
3. **The PC rule has quietly inverted.** NATALIE.md says never think, speak or act for Isaac's PC; in practice Natalie writes his characters in close POV from his beats, with his consent, and R49-01 now allows it.
4. **Fronts barely move.** 15 Fronts, one closed; in the whole history four ticks have been recorded (two on the Accord circle, two on The Class Below). Eleven open Fronts have never ticked.
5. **The Ledger fills and never empties.** 65 lines, 63 open, 2 "collected" (both canon conflicts, not costs). Nothing has ever come due and been paid at the table. `due()` returns 30 lines at once and cannot filter by thread.
6. **Session end is the step that does not happen.** `sessions.yaml` holds one session (2026-09-22). The Sodoku State of Play was last rewritten 2026-09-10; the Docket page on 2026-09-10, two days before most of its items were ruled.
7. **NPC lies and refusals are real but uneven.** The Rovhen and Mu-jin runs name "the session's lie" and give every new NPC a want, a refusal line and a lie. The duel runs mostly swap lies for misreadings.
8. **Multiplayer has no referee.** When two players' posts collide, the notes say the players settle it. Table Rule 5 adjudication (no dice: Stage gap, the read, what was spent, the environment) runs inside Isaac's own characters, never between players.
9. **The Judger's close over-delivers and under-lands.** Three judger notes made 115 proposals; 22 were applied, all of them Ledger lines. No Front tick, NPC entry or ruling from the judger has reached the table.
10. **Pending flags pile up against Isaac's own direction.** About 60 "pending ruling / Isaac's call" flags sit in the notes of 59 table scenes, and the Ledger itself carries one (L065).

## Already settled: not to be asked again

From the Style Law R70 (2026-10-03) and the Combat Law R71 (2026-10-04, `combat-law-2026-10-04`), plus the live rows both questionnaires listed as settled:

- **Turn length and fill:** about 3,500 words, every reply, half texture and talk, half the world moving; set-piece floor above that (R48-28, R49-29, R49-30, R48-46).
- **Tense and person:** present for roleplay turns and improved RP posts, past for scenes and books (R49-02); third person only (R70-12).
- **Whose head:** full depth inside Isaac's character, Isaac overrules (R49-01); his play beats his card (R52-08); his POV characters stay his in crossovers (R52-10); restricted creators' characters excluded (R1-1).
- **His dialogue:** verbatim in scene work (R19-2), improved when he asks for an RP post to be made better (the 2026-09-21 carve-out, `RULINGS.md:528`).
- **Play rows:** invent freely, logged (R48-26); skip dull stretches (R48-29); foreshadowed surprises (R48-30); death if earned (R48-31); Isaac may take any NPC's voice (R48-32); veteran-clever NPCs (R48-36); frequent lies (R48-42); one crafted speech (R48-43); full check every turn (R48-45); notes in the file (R48-47); one-line pushback (R48-50); never rigged (R57-10); death permanent (R60-04); one italic thought per NPC in roleplay turns (R48-40).
- **Fights at the table (R71):** standing orders (K5); a player's fighter as world facts, the tell placed, felt from across the room, outward cost only (K9); Aetherion bouts on posted terms, warden backstop (FT4); yield, flight, a code, the killing's law (CW11); a sign and an exit before a loss (FT17); the bill in the world (WT10); rivals paid on the Ledger (CB5).
- **Arcs (R70):** tournament, Well delve, montage and episodic jobs (R70-18); closing modes (R70-17); contract boards (LR19); changes at chapter end (LR20).

None of these says how it reaches Discord or session bookkeeping, which the questionnaire can still ask.

## Three tables, not one

**The Desktop table (Sequence A).** This is the table NATALIE.md describes. In *The Cabin*, Natalie plays Verinus VII across four exchanges with the Sovereign of the Zettari, whose lines never appear in the compilation: each turn opens on Verinus answering an unseen post ("You did that in eleven minutes," Cabin II) and ends on a thing the player can now act on. Cabin I ends on a physical action, the last poppy head set "in the middle of the twenty names"; II, III and IV end on Verinus's own line. The compilation header calls itself "Scenes and roleplay responses in narrative order" (`WOTR_Vaeloris_Sequence.md:5`). The Kharven "year after" play also happens here: the Accord circle Front ticked twice on 2026-09-22 "from the table via WOTR MCP" (commit `bc7bf80`), and I could not find the scene that tick describes anywhere in `scenes/`.

**The Discord table (Sequences B and C).** The players' server is location-based roleplay with Tupperbox (a bot that posts a player's message under a character's name and avatar) and Avrae (a dice bot, kept out of canon channels). Natalie is not in the server. The notes show the loop: another player posts, Isaac brings the post and his beat (his short prompt for what happens) to Natalie, she writes his reply, he posts it. "Isaac's RP reply to Xhem's dorm-assignment post. Isaac writes Hiromi, Xanelor, Akira, Naori and Mu-jin" (`xanelor_the_dorms.md:65`). Isaac's roster on this table runs to ten characters: Geturo, Hiromi, Xanelor, Akira, Naori, Rikudoku, Dabney, Mu-jin, Rovhen, Lance Greymane. The NPCs Natalie owns are the walk-ons around them: the warden, the infirmarian, Tam Rudd with his chalk odds, the Class S scouts, the porters.

**The archive table.** Many "table" files were never turns. The numbered Kharven set pieces are backfill of the Ashgate day, written after the State of Play had jumped a year forward. *The War in the North* I to V are "Isaac's finished text, archived verbatim" from a 49,759-word upload, in which Isaac himself writes Lambert, Lorn, Wren and Bram; Natalie is archivist and flagger there.

## Turn length and shape in practice

| Body of work | Files | Prose words per file |
|---|---|---|
| Discord turns (Academy) | 38 | median 1,506; mean 1,629; min 683; max 3,599; 17 at or under 1,500; 2 over 3,000 |
| The Cabin, Desktop roleplay | 4 turns | 2,498 / 2,862 / 2,735 / 3,111 |
| Numbered set pieces (`01` to `23`) | 34 | median 2,583; the long ones are compilations |
| Author notes on Discord turns | 33 | median 287 words, max 669 |

So the house turn sits between the old Table Rule 2 bands (conversational 300 to 700, standard 700 to 1,500, set piece 2,500 and up) and the new 3,500 rule, and closer to the old. NATALIE.md still prints both: the bands and "Over-delivery is the standing complaint" (lines 40, 47) beside "turns about 3,500 words" (line 287). The `wotr-rp` skill says "shorter turns" (line 8) and "About 3,500 words" (line 28) twenty lines apart.

**Shape.** Table Rule 1 (answer what the PC did, move the world, stop at his next decision) is mostly kept, and kept well on the endings. The Geturo files each stop where the other player has to move: "The fifth band reached Taesyn" (`geturo_ignite_tide.md`), "Geturo's elbow was at the top of its arc" (`geturo_the_elbow.md`). The duel parts stop on an NPC action or an image. Rovhen's turns stop on an NPC's line or a sensation ("a second one had begun", `rovhen_the_letter.md`).

**What a turn contains.** A Discord turn is Isaac's beat expanded, plus three layers Natalie adds: researched mechanics (the wrist-grip escape "toward the thumbs", the Shinkansen tunnel boom), the room (walk-on NPCs, odds, the warden's gauge), and his character's interior beyond the beat ("Added. Hiromi owns the loss in his father's words", `hiromi_the_bench.md`).

**Pace in a fight.** One exchange per turn. The Geturo bout took eight files and about 13,000 words of prose for one sanctioned match; one escape took 1,328 words. R71 K5 (standing orders) now answers this for fights; nothing answers it for talk or investigation.

**Tense.** Every Discord turn archived after R49-02 landed on 2026-09-26 is in past tense (the Geturo files archived 09-27, the Rovhen files 09-27, `mu_jin_the_card.md` 09-28). Either the server's own convention is past tense, or the rule has not reached the Discord posts.

## NPCs: wants, refusals, lies

**Where it works.** The Rovhen run is the model. Every new NPC arrives with the four fields: "Examiner Maud Harrowgate... Want: a finding with a name in it... Lie: the quarterly proofing. Refusal: won't open the inspector's book in front of anyone" (`rovhen_the_sort.md:223`). The lie is spoken on the page ("The ward was proofed at the quarterly," line 119) with its counter-evidence on the desk in the same scene, the cased plate struck "twice and off true". Proctor Crale's refusal is a line of dialogue: "Last bell's the last bell" (`rovhen_the_dispensary.md:31`). Joan Aldery's lie ("Nail. At the counting-house door.") stands uncorrected and is entered as Rule 8's lie (`rovhen_the_letter.md:81`). The Mu-jin run names its lies the same way: Malphas calls Velder "my secretary" while Hiromi sees hands with no ink and old splash burns (`mu_jin_the_old_colleague.md:125`).

**Where it thins.** In the duel runs the NPCs are walk-ons and nobody lies; the notes log misreadings instead ("Hiromi thinks Xanelor heard him; Mu-jin thinks the boy guessed the line", `xanelor_the_bullet_train.md`). Refusals in the Geturo run come from Isaac's own Mu-jin overruling the warden ("You're not," `geturo_the_other_side.md`), so the one refusal with weight is a player character's.

**Counts.** A rough grep of the notes in 61 table files finds a lie, misreading or uncorrected falsehood logged in 26 and a refusal in 21, concentrated in the Rovhen, Mu-jin and Kharven files. Rule 8's "one per session" is met where Natalie runs the room and missed where she is ghostwriting.

**The roster.** `npcs.yaml` holds ten NPCs, all from the two Academy threads; two of them (Josse Osricsson, Lei Yanshu) were built by agents on 2026-09-25 to drive a Front and are "Not yet on the page". No Kharven NPC is on the roster. The judger proposed six Kharven entries (Seiji, Wren, Bram, Lorn, Edward, Yoko); none was applied. NATALIE.md still says the per-thread roster is "not yet built" (line 107).

**NPC interiority.** The Cabin gives Verinus two or three italic thoughts per turn (eleven across four turns), against Rule 10's one per NPC per scene and R48-40's one per NPC in a roleplay turn. Conflict C-008 (Yoko's italic interior under a Sodoku POV lock) is the same seam in a written scene.

## Fronts in practice

A Front is an offscreen agenda run as a clock: a want, a last move, a next move and four or five ticks to resolution. The table holds 15.

| Thread | Fronts | Ticks ever recorded |
|---|---|---|
| Kharven, the year after | 6 (Tenrai closed) | 2 (the Accord circle, 2026-09-22) |
| New World, the Korvaeth War | 6 | 0 |
| Kwon Mu-jin (Academy) | 1 (The Class Below) | 2 (2026-09-22, 2026-09-28) |
| Mu-jin (Rovhen) | 2, opened 2026-09-28 | 0 |

**How they actually move.** Only when a scene happens to touch them. The Class Below is the healthy case: opened at the table on 09-22, kept warm by a silver-corded Class S girl taking notes at the tunnel mouth in several Geturo and Xanelor files, then ticked to 2/5 by five Class S names "in a narrow pen" on Rovhen's roll. It is the only Front that behaves like the law's "the world moves": Natalie seeds it in the margins of scenes about something else.

**How they stall.** The Kharven clocks were all written on 2026-09-12 and keyed to "the year after", but the scenes archived since are mostly backfill of the year before, so no scene can tick them. The judger said so of *Recalescence*: "no open Front on this thread moved (Table Rule 4 not met)" (`08_sodoku_recalescence.judger.md:69`). The Accord circle's third tick is "Whatever Sodoku does with the brush is the reading": a Front parked on a PC decision, unanswered since 09-22. The New World Fronts belong to a thread with no live play at all. The Wren Front was recast as a grief Front on 2026-09-26 (R58-07) after Isaac's own *War in the North* IV showed Wren alive and working, which the archivist flagged: "That is not step one of that clock" (`the_war_in_the_north_iv_the_blank_seal.md`, notes).

**Duplication.** The wiki mirror has two Fronts pages: "Fronts" (prose, edited 09-26) and "Fronts, as clocks" (generated, mirror dated 09-13, 12 Fronts). The prose page still says the Mu-jin thread is "Unassigned. Two to four Fronts needed."

## The Ledger in practice

The Ledger is the running bill: injuries, reserve, debts, reputation, who knows what. It holds 65 lines in six categories: who knows what 18, injuries and reserve 13, debts 13, the dead 8, reputation 8, canon conflicts 5.

**What it records well.** Injuries by structure with a condition for when they bite: L030 lists Xanelor's hairline fractures of both forearms and three fingers "cut to the bone", due "before or at the Class X Open Tournament". The Geturo run kept a running "Ledger (Geturo)" block in five consecutive files, vial by vial ("Vials 3 (cold), 7, 8 left"), and the Dallae scene carried L030 forward ("both forearms bridged with set mineral, not yet bone"). Inside a run, continuity of cost is excellent.

**What goes wrong.**
- **Nothing is ever collected.** The two lines marked collected (L027, L029) are canon conflicts. No injury has healed, no debt been paid, no secret come out at the table.
- **`due()` drowns.** With one session logged, every line with a prose condition surfaces at once: 30 of 63 open lines, and a thread filter changes nothing because rows carry no thread field (`build/table.py:190`).
- **The timeline is mixed.** L035 to L056 came from judger notes on the Ashgate day, a year before the Kharven State of Play; L043 and L041 belong to a morning the thread has passed, and L054 waits on Osric in a doorway where *Recalescence* has him dead, a death the Ledger never took.
- **It records the PC's head.** L052 and L053 record what Sodoku believes "in his own head".
- **Blocking lines go stale.** L025 (Stage names) is still blocking though NATALIE.md records it ruled 2026-09-12; L026, the Accord circle's missing name, has blocked prose since 2026-09-10.
- **"Pending Isaac" lives in the data:** L065, "Whether [Let] pulled at the seam is Isaac's call."

## State of Play, the Docket, and the session close

The State of Play is the one-page "where we are" per thread, rewritten at session end. In practice:

| Page | Last edited | State |
|---|---|---|
| Sodoku Moto / Kharven | 2026-09-10 | "What he believes that is wrong. Open. Fill at next session." |
| Hild Ice / Kharven-Seat | 2026-09-11 | closed, Hild dead, still under Running Pieces |
| Kwon Mu-jin / Hon-guk | 2026-09-22 | "Thin... Two to four needed." |
| Kwon Mu-jin / Aetherion | 2026-09-26 | Class Below shown at 1/5 (the table has 2/5) |
| Rovhen / Aetherion | 2026-09-28 | current, the best kept |
| Ilthára Korvaeth / New World | 2026-09-26 | no play |
| Open Rulings, the Docket | 2026-09-10 | lists R13-A to F, R14-B to E, R15-A, R11-A to E as open; NATALIE.md records most of them ruled 2026-09-12 |

`sessions.yaml` logs one session, n 1 on 2026-09-22, with `advanced: []` and `came_due: []` although two Fronts ticked that day. The 09-28 Rovhen session is not logged. Session ages drive `due()`, so the missing sessions are why every line looks equally due.

The Judger's assistant was built to do the close by reading: it ran on three Kharven scenes (2026-09-13 and 09-25) and produced notes of 3,900 to 5,200 words each with 41, 31 and 43 proposals (plus 26 set aside). The JSON `applied` lists show 12 applied for `01`, 10 for `04`, none for `08`, every one a `ledger_add`, each with "push failed" recorded. It has never run on a Discord scene, though that was its purpose.

## Scene Menu, Rumor Mill, downtime

The Scene Menu is three hooks offered when Isaac opens without a beat (one from a Front, one from the Ledger, one fresh); the Rumor Mill is two or three pieces of world news at session start, some wrong. Neither leaves much trace. The Rumor Mill appears once in the whole archive, in Agnes Tull's mouth with two wrong items, one texture item and one true hook (`rovhen_the_sort.md:200`). No Scene Menu is recorded in any scene or note. No downtime turn exists. Isaac nearly always arrives with a beat.

## Consequences

Cost inside a run is the table's strongest habit: wounds by structure, spent vials counted, the bow broken and owed (L031), the arena floor owed (L033), Hiromi's every draw now at "first-call price" (L034). R71's WT10 ("the bill in the world") matches what the Academy run already does with the warden, the bursar and the Visitation.

Consequence across runs is weak. The tournament seven days out is the clock every Academy injury points at, and the tournament has not been played. The Finding of Cause is "owed at first bell" and unsigned. The arena match that caused most of the debts has no recorded outcome: "Match outcome is Isaac's" (`xanelor_the_arrow.md:79`), and sessions.yaml carries "Match outcome not yet ruled". The Geturo bout ends "No winner named; the players decide it for his debrief" (`geturo_gypsum.md:103`). Two sanctioned bouts, no result on the record, and The Class Below turns on exactly that: who fought hurt or fought badly.

## Where play stalls

1. **On a name or ruling not given.** The Accord circle's name (L026), Xanelor's Wellspring, Rovhen's FOW line, Dabney's blood or wardship, Mu-jin's vial; the Rovhen State of Play lists two "pending Isaac" lines. CONTINUE.md opens with his direction ("make the calls; no 'pending' slots") and the table data has not caught up.
2. **On a PC decision held by a Front:** the Accord circle waits on the brush, the Finding of Cause on Rovhen's signature.
3. **On a contest between players** (below).
4. **On time:** the Kharven thread's live moment is a year after the scenes being written, and the table straddles both.
5. **On bookkeeping:** no session end, so the next session starts from stale pages.

## Where it over-delivers

- **Notes and flags:** a median 287 words of notes on a 1,500-word Discord turn, 600 to 1,000 on a Kharven set piece, about 60 pending flags across 59 files.
- **The close:** 115 judger proposals for three scenes, most of them notes for Isaac's hands; the notes run longer than the scenes they close.
- **A beat's expansion:** a few lines become 1,300 to 1,900 words with researched mechanics and added interior. He has asked for 3,500, so this over-delivers against NATALIE.md's text, not his latest word.
- **Talk:** Verinus's turns carry 37 to 42 lines of speech each, several paragraph-length, where R48-43 allows one crafted speech at a big moment; and two or three italic thoughts a turn.

## Multiplayer on Discord

**What it looks like.** Other players' characters in the archive: Taesyn, Zaire, Verona, Neraveth, Saeloria, Nyxeria Velthrae, and Xhem (a restricted creator's character, R1-1) whose player posts the Academy's announcements: the dorm assignment and the tournament. Another player appears to hold part of the GM role on that thread, and Natalie writes Isaac's side of it.

**How Natalie treats other players.** Strictly by R1-1 and R52-10, and consistently: "Taesyn belongs to another player. Never written: no thought, action or reaction" (`geturo_ignite_tide.md`, notes); Nyxeria "appears only as Rovhen perceives her" (`rovhen_the_dispensary.md`). This is R71 K9's "felt from across the room", already practice before it was law. She flags canon breaks in their posts without touching them: "Taesyn's post says 'Uncle Mu-jin'" (`geturo_ignite_tide.md:70`); "London, pre-Christian deities and the year 1874 are real-world references" (`rovhen_the_dispensary.md:97`).

**Contests.** When Isaac's post and another player's collide, Natalie writes only Isaac's side and leaves the collision open: "The broken fingers contest the other player's post... Players to settle canon. Known issue: the escape skips the other post's back-mount and hooks" (`geturo_the_slip.md:77`). Nobody adjudicates. Table Rule 5 and R13-8 (every outcome reconstructible from the page) run inside Isaac's roster (the Hiromi and Xanelor duel, where he wrote both fighters, is adjudicated row by row) and stop at the edge of another player's character.

**Tooling.** The bot's F1 (table state: `/fronts`, `/due`, `/ledger`, `/roster`) and F3 (`/adjudicate`) are unbuilt (`ROADMAP.md:262` to 264). Players cannot see a Front or the Ledger. `/scene save` exists but no Discord scene in `scenes/` came through it; only three cast files exist, none from Discord. Ownership marks are fragile: the 2026-09-26 clean-publishing sweep listed "Other players' (never written by Natalie)" on the Academy State of Play as a provenance line to remove (`CONTINUE.md:476`), and the current page lists Taesyn, Zaire and Neraveth in the room beside Isaac's characters with no mark of whose is whose.

## Gaps between the law and the practice

| Law | Practice | Ref |
|---|---|---|
| NATALIE.md: never think, speak or act for Isaac's PC; Isaac drives his PC (lines 34, 38) | Natalie writes his characters in close POV from beats, adds interior; Isaac asked for it ("You handed me his interiority directly") and R49-01 allows it | `04_sodoku_what_the_sky_does_not_ask.md:162` |
| One PC | A roster of ten on Discord, both sides of one duel | `xanelor_the_dorms.md:65` |
| ~3,500 words every reply (R48-28, R49-30) | Discord median 1,506; Cabin 2,500 to 3,100; NATALIE.md still prints the old bands | NATALIE.md 40, 47, 287 |
| Present tense for roleplay and improved RP posts (R49-02) | Every post-09-26 Discord turn in past tense | `geturo_the_slip.md`, `rovhen_the_letter.md` |
| Fronts advance every session (Rule 4) | 4 ticks ever; 11 open Fronts never moved | `table/fronts.yaml` |
| Ledger: at least one line comes due every session | 0 collected; `due()` returns 30; no thread filter | `build/table.py:190` |
| Session end rewrites State of Play, appends Ledger, logs the session | 1 session logged; key pages 3 weeks stale | `table/sessions.yaml` |
| One NPC lie per session (Rule 8), frequent lies (R48-42) | Kept where Natalie runs the room; thin in duels | `rovhen_the_sort.md:201` |
| One italic thought per NPC (Rule 10, R48-40) | Two or three per turn in the Cabin | Cabin I to IV |
| Every outcome reconstructible (R13-8) | Player against player outcomes left to "the players" | `geturo_gypsum.md:103` |
| Nothing waits on Isaac (CLAUDE.md, CONTINUE.md) | Pending flags in notes, State of Play pages and Ledger L065 | `table/LEDGER.md` |

## Targets for the questionnaire

Real questions the practice raises that R70, R71 and the live rows do not settle:

1. **Which tables the law governs.** Desktop GM turn, Discord ghostwritten post, archived set piece: one turn shape, length and tense for all, or one each. (Length and tense are settled; their reach to Discord posts is not.)
2. **The roster as PC.** Whether every character Isaac posts as is a PC for R49-01 and Rule 1, including two of them fighting each other, and who adjudicates that.
3. **Player against player.** Who decides a collision of posts: the players, Isaac as Judger, a Table Rule 5 card from the bot, the warden on posted terms (FT4 covers the arena only). What the losing post becomes.
4. **Results on the record.** Whether a bout or scene may close without an outcome, and how long an unruled result may hold a Front.
5. **Front cadence.** Tick every session, every scene, or when touched; ticks from backfill scenes; Fronts parked on a PC decision; how many per thread; what happens to a thread with no play.
6. **The Ledger's life cycle.** What "due" counts (sessions, story days, a condition); a thread key; how a collection reads on the page; when a line retires unpaid; whether the PC's private beliefs belong on it.
7. **Session close.** Who runs it, what is mandatory, how long it may be, whether proposals apply by default.
8. **Pending flags.** Natalie makes and logs the call in play, or flags; which kinds of thing still wait.
9. **Lies and refusals by table.** Whether Rule 8 and R48-42 bind Discord walk-ons, and whether a misreading may stand in for a lie.
10. **NPC interiority in roleplay turns.** One italic thought per NPC per turn or per scene.
11. **Scene Menu, Rumor Mill, downtime.** Keep, retrigger (say, each new in-world day), or drop.
12. **Discord ownership.** Whether pages may mark whose characters are whose, and how a canon-breaking post from another player is handled beyond a flag.
13. **What the players see.** Fronts, Ledger and roster on Discord (F1), or Judger-only.
14. **Isaac's own long texts.** When they contradict a Front or the Ledger, which moves.
15. **The time seam.** How one thread holds two moments (the Ashgate day, the year after) without the table straddling them.

Housekeeping the questionnaire need not ask about, only note: NATALIE.md's Table Rule 2 bands and "Length discipline" line, the `wotr-rp` "shorter turns" line, the 2026-09-10 Docket page, the closed Hild State of Play, the duplicate Fronts and Ledger pages, and L025 still marked blocking.
