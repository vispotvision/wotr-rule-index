# The table data, reconciled (R72-42, ME2 B)

One pass over the data on file, 4 October 2026, after the tool changes landed. Files written: `table/ledger.yaml`, `table/fronts.yaml`, `table/npcs.yaml`, and their rendered pages `table/LEDGER.md`, `FRONTS.md` and `NPCS.md`, regenerated with `build/table.py`'s own `render()`. State of Play drafts: `state-of-play/` beside this file. Nothing committed, pushed or published; no MCP tool that writes was called. Every call below is an **agent ruling** (R72-2, K2): a call Isaac may overturn, logged here once (R72-33).

## Summary

| File | Before | After | Changed |
|---|---|---|---|
| `ledger.yaml` | 65 lines, 63 open | 72 lines, 46 open | 39 open lines given a thread and a trigger or standing; 24 retired with a dated reason; 7 added (1 replacement, 2 heat, 4 bonds); 1 trigger marked fired; 2 texts updated |
| `fronts.yaml` | 15 Fronts, 14 open, no pace | 15 Fronts, 14 open, every open one paced | 15 thread names aligned; 14 paces set; 1 tick rewritten; 0 closed |
| `npcs.yaml` | 10 rows under two thread names | 10 rows under one | 40 fields set (lie, tell, doing now, stands with); thread folded |
| State of Play | 6 pages on Notion, written 6 to 28 September | 4 drafts | Kharven, Hild Ice (closed), Kwon Mu-jin / Hon-guk (folded), Kwon Mu-jin / Aetherion Academy (one page for the Mu-jin and Rovhen pages) |

`due()` now returns one line, L014, the only bill whose trigger has fired. `roster()` flags no R72-25 gap. `build/validate.py`: PASS.

## The calls that shape everything else

1. **Thread names are the State of Play page titles.** `Sodoku Moto / Kharven` (was "Kharven thread, the year after"), `Ilthára Korvaeth / The New World` (was "New World, the Korvaeth War"), `Kwon Mu-jin / Aetherion Academy` (was split between "Kwon Mu-jin" and "Mu-jin", the drift the research flagged). The tools match threads by substring, so 'Kharven', 'Sodoku Moto', 'Korvaeth', 'Mu-jin', 'Kwon Mu-jin' and 'Aetherion' all find their thread; `session_start('Sodoku Moto')` now finds the Kharven Fronts, which the old name never matched. A Rovhen session must pass 'Aetherion' or 'Mu-jin': 'Rovhen' alone matches nothing.
2. **Kharven's live date is the empire's first year, spring, after the signing, at night.** The table played this thread there on 2026-09-22 (Lambert's paper, the Accord circle to 2/5) and the paper waits on the PC's brush, so the date cannot move past it. *The Revolution of the Inner World*, archived the same morning and revised 2026-09-26, runs six years ahead; it is read as a fixed future the Fronts arrive at and never pass early (the Whitemere name, Stannvaard's annexation, Tabitha's question unanswered through the sixth year). R72-34 is written for past scenes; this reads a forward chronicle the same way.
3. **The Academy is one thread at the fourth day of term, the last hour before last bell, 715 IC.** The Mu-jin group's scenes stop on Monday (day one) and Rovhen's on day four; the thread takes the later date and the Monday lines still bind at it.
4. **No story date was invented.** No thread holds an Accord Y-M-D (there is no `table/threads.yaml`; the pages give seasons and term days, not dates), so every line got a named trigger and none a `due_date`. The first `pass_time(story_date=...)` at each thread's next session sets its date, and from then the Fronts tick by their paces.
5. **The old `due` field is cleared on every reconciled line** and its value kept: in the line's `reconciled` note ("Was due: ...") for open lines, in `collected.was_due` for retired ones. Otherwise `due()` would keep reading them by session age and `LEDGER.md` would print a dead term.
6. **Retirement uses the tools' own collected form**: `status: collected`, `collected: {session, date, how}`, with `how` beginning "retired by the R72-42 reconciliation, agent ruling". Nothing was deleted.
7. **Hon-guk folds into the Academy** (no scene is set there, no Front, Ledger line or roster row carried it), and **the Hild Ice page moves to the Scene Archive** as record (the question its 10 September page left open).

## ledger.yaml

### Kept, with a thread and a trigger (33)

| Line | Thread | Comes due when | Why kept |
|---|---|---|---|
| L006 Sodoku, sleep and Kurosetsu | Kharven | Kurosetsu is next asked to remember, or a scene runs him past another night's waking | standing exhaustion at the live date |
| L007 Bram, fingers and hip | Kharven | Bram next fights, rides hard, or is kept standing through a long sitting | healed hard at eleven months |
| L008 Brida, the stick | Kharven | the first frost comes round a year on, or she is sent on foot first | "would be for a year" |
| L010 Vresk Dokkan | Kharven | the Keth-Gorrum addresses him by his new compound (keth-gorrum tick 2) | alive and returned |
| L011 Borin's forge-work | Kharven | Borin names his price, or Sodoku next stands at Borin's forge | still unpriced; *The Drawing-Off* has Borin unpaid by "a customer upstairs" |
| L012 the Stannvaard grain | Kharven | a Stannvaard debt reaches the circle (accord-circle tick 4), or a factor comes for it | open; Stannvaard's annexation is fixed ahead |
| L014 the four hundred and six | Kharven | Lambert lays the southern registers before the king (accord-circle tick 2): **fired 2026-09-22** | the bill is on the table as Lambert's paper, an offer with terms (R72-23) |
| L015 Renard, the postern | Kharven | Renard speaks Lambert's name, or the postern is examined | backfill that still binds: his card says the claim "stands without an answer" |
| L016 Renard, the token | Kharven | the token or the packet is read | backfill that still binds: "No record says who has read the token" |
| L017 Tabitha's question | Kharven | she starts asking the factors (tabitha tick 1) | live |
| L018 Yoko's four lines | Kharven | anyone asks for her record, or the Bench demands it | unseen, and still unshown in the sixth year |
| L019 the refugee count | Kharven | anyone enters the difference, or the southern registers are re-entered under the circle's seal | live, and Lambert's paper reaches those registers |
| L020 the two-word form | Korvaeth | Aeldros works it out (the-thing-nobody-has-done tick 1) | the year-eleven scenes have not put it to her |
| L021 the blade on the sleeve | Kharven | a house, court or column that heard the depositions receives him | reputation reaches NPCs under R72-27 |
| L022 Bram's word | Kharven | the Keth-Gorrum coins the word (keth-gorrum tick 1) | the reputation rests on it |
| L023 Lambert unthanked | Kharven | Tabitha's question is put in public again (tabitha tick 3) | the Register prints it in the sixth year |
| L024 the Mad Queen | Korvaeth | a court or the archive reads the yard's ledger aloud (velthaeir tick 1) | standing at the Korvaeth date |
| L028 did Ilthára say the name | Korvaeth | the docket rules it as an agents' authorship call (RULINGS 2026-09-25, rung 7) | not ruled; this pass rules no canon conflict |
| L030 Xanelor's injuries | Academy | the tournament comes (day eight), or he draws or takes a blow on either forearm | **text updated** as *Xanelor: Dallae*'s notes say ("L030 updated"), which never reached the file; old text kept as `text_was` |
| L031 Xanelor's bow | Academy | the tournament comes, or he takes a bow from anyone | Mu-jin handed back the broken one |
| L032 who saw the arrow | Academy | the bracket is seeded, or his intake sheet is re-examined | its own condition |
| L033 who answers for the floor | Academy | Harrowgate calls for the Finding at first bell (finding tick 1) | the Finding is how the floor is answered for |
| L034 Hiromi, first-call price | Academy | Hiromi next calls anything | **text appended**: the draught closed the fresh septum bleed |
| L050 the outer town's wood | Kharven | the next Thin Weeks, or the households come to the Seat about the wood | backfill kept: nothing repays it on the page, and the Kharven keep the count |
| L053 the attribution to Sonzai | Kharven | he names Sonzai to anyone who knows who built the turning, or the Seat is asked who knew (wren tick 3) | backfill kept: nothing at the live date corrects it |
| L057 the Tuned Signature | Academy | the letter burns, changes hands or is read (tallow tick 3) | from "while the letter exists" |
| L058 the Finding owed | Academy | first bell, day five (finding tick 1) | the green-sealed note |
| L059 Sallow's bill | Academy | the Visitation files, or Sallow comes for it (finding tick 5) | from a session count |
| L060 what Rovhen holds | Academy | the evidence is shown to someone with standing (finding tick 4, tallow tick 4) | from a session count |
| L061 Imogen Pell | Academy | Class S gets into the arena or learns who filed (class-below tick 3) | from a session count |
| L062 Walter Aldery | Academy | the inquest papers are read (tallow tick 1) | a dead man whose papers carry a bill keeps the trigger |
| L063 "Lambert's lad" | Academy | someone who knew Edmund, or the struck licence, is raised before witnesses | from a session count |
| L065 the seam flicker | Academy | the draw-inspector reports on the seam, or Mu-jin looks himself | from a session count; what pulled at it is a call for the table, not this pass |

### Kept as standing (6)

L001 Hild Ice, L002 Muken Moto, L003 Freya, L004 Seiji Tenrai Moto, L005 the eleven retainers, L035 Egil Vald: the dead, thread Kharven, no trigger (the tools treat the dead as standing). L035 is backfill kept because the dead stand and Bram's roll names him, which was its own condition.

### Retired (24), each with its reason in `collected.how`

| Line | Why |
|---|---|
| L009 Renard's forearm | backfill: taken in the Thin Weeks before the muster, over a year before the live date; nothing carries it |
| L013 Renard to Brida | backfill: "a body before morning" named a morning the ninth hour overtook |
| L025 R14-A, Stage names | ruled: R20C-30-STAGE_NAMES_FROM_FOW is live; Gimbzo's numeral against name stays its own CONFLICTS row (WAR-15) |
| L026 the circle has no name | the archive names it Whitemere, Emira's word (*The Revolution of the Inner World*); in play the naming is still ahead and the Accord circle Front carries it |
| L036 Bram on foot | backfill: superseded by L007 |
| L037 Bram's three hundred | backfill: one day's state, nothing carries it |
| L038 Wren's six hundred | backfill: Wren dead; the grief Front carries the houses' want |
| L039 Wren's book | backfill: the knower is dead and the contents reached the depositions; the saddlebag lies with the body (wren tick 4) |
| L040 Seiji's four riders | backfill: the road was decided; Seiji is dead |
| L041 Lorn's reports | backfill: "Lorn Stark is dead" |
| L042 Lambert's channels | backfill: a day's silence |
| L043 Lambert's five days | backfill: long past; Lambert is at the Seat |
| L044 Lorn's arrangement | backfill: Lorn and Hild dead; the arrangement is entered at their stones |
| L045 Wren's claim | backfill: reached Bram with the depositions; his dedication answered it |
| L046 the quiet yard | backfill: superseded by L021 |
| L047 eleven officers | backfill: the narrows went onto the Reckoner's list of the dead, its own condition |
| L048 on foot | backfill: he rides the Droval at the Brine crossing |
| L049 Reigan's cost | backfill: the working's own law, recurring at every use, shown in the read, not a bill |
| L051 the gate held for him | backfill: Osric is dead |
| L052 his brother and Zuberi | backfill: the ninth hour's fight; his living brother Sonzai is back in the north by the ninth month |
| L054 the doorway order | paid: Osric put himself in the doorway and died there with Hild |
| L055 Robin's lost item | backfill: he has reported many times since |
| L056 Wren called traitor | backfill: Bram's dedication answered the word in public |
| L064 Geturo's tide | superseded: the match closed and the tide was let go; replaced by L066 |

### Added (7)

| Line | Category | Thread | Source |
|---|---|---|---|
| L066 Geturo's state after the match | injuries and reserve, trigger: he next fights, draws or reaches with the right arm | Academy | *Geturo: Gypsum* notes ("Ledger (Geturo)", never entered), *Aftermath: Hold the Wall* |
| L067 heat, level **high** | heat | Kharven | *What the Ground Was Owed* |
| L068 heat, level **warm and rising** | heat | Academy | *Rovhen: The Sort*, *Xanelor: The Arrow*, *Geturo: Gypsum*, *Wystan's Briefing* |
| L069 Sodoku and Yoko Mishiro | bonds (3 fed, 1 strained) | Kharven | *Recalescence*, *What the Ground Was Owed*; the thread's standing warm bond (R70-114) |
| L070 Sodoku and Emira | bonds (1 fed, 1 strained) | Kharven | *What the Ground Was Owed* |
| L071 Hiromi and Geturo | bonds (2 fed, 1 strained) | Academy | *Hiromi: The Bench*; the thread's openly warm bond |
| L072 Hiromi and Saeloria | bonds (3 fed) | Academy | *Hiromi: The Picnic*, *Something Special*; Saeloria is another player's and nothing of hers is written |

No heat or bond line for Korvaeth (not on this job's list of live threads), Hild Ice (closed) or Hon-guk (no play). Levels are words; no figure anywhere.

## fronts.yaml

Every Front's thread renamed as above. Paces (`pace_days`, `days_banked: 0`), each with its grounds in the Front's `reconciled` note:

| Front | Pace (story days) | Grounds |
|---|---|---|
| The Keth-Gorrum of Undaar-Keth | 56 | months have passed since Vresk's return with no compound coined: a chancery's pace |
| The Accord circle, unnamed (2/5) | 19 | the circle sits nineteen days after Lambert's drafted reading (the Front's first record of the move). Tick 3 is his brush; the calendar only reads an unanswered paper, which leaves Lambert's seal on them (R72-23). Tick 5 resolves toward the canon name Whitemere |
| Tabitha Hallenfeld | 504 | eighteen months of twenty-eight days, so tick 4 (Lambert answers) cannot fall before the sixth year's fourth month, where canon still has him silent |
| Bram Greymane | 56 | nobody wants to be the one to ask; the grief Front feeds it |
| Wren Greymane, the grief | 28 | Auren's day to Auren's day, the monthly day the dead are sat with |
| The Sunroot Regency under Ovaeren | 91 | a season; the New World keeps its own count |
| Korrindal and the Vessel road | 28 | a road held through a winter, month by month |
| Thela Ess-Vaelen | 91 | she holds the name unused and does not know what she wants |
| Velthaeir | 91 | an archive moves by the quarter |
| The Tsohanto Reach | 182 | a silence ticks by the half year |
| The thing nobody has done | 56 | the eleventh year is the live year |
| The Class Below (2/5) | 2 | tick 3 on day six, tick 4 on tournament day, tick 5 after it |
| The Finding of Cause | 1 | first bell tomorrow; tick 1 is Rovhen's answer if he gives it, and the calendar reads only an unanswered call ("stalled") |
| The Tallow Street Stair | 2 | Joan goes on a weekday morning; the letter is news that travels in days |

**Tick rewritten.** Tabitha Hallenfeld tick 3 put the dated question "in front of Hild", who is dead at the live date (the clock was written on 12 September, two days after her thread closed). It now reads: "She puts the dated question before the Bench rather than Lambert, in writing, with the two refusals attached." The old text is kept as `tick3_was`.

**Closed:** none. No open Front's question is answered at its thread's live date. The Accord circle's name is fixed ahead (Whitemere) but not yet given in play; The Tenrai was already closed.

## npcs.yaml

All ten rows folded into `Kwon Mu-jin / Aetherion Academy`; `last_updated` set to 2026-10-04. Each got a live lie with its tell (R72-25) and a doing-now and stands-with line (R72-26). Lies drawn from the record (`lied_about`) are marked so; everything else carries "(agent ruling)".

| NPC | Live lie | Tell | Stands with him |
|---|---|---|---|
| Josse Osricsson | the overdraw split the Omoro and the wood was sound (his thumb knows it dried out of true) | he calls the wood good, which he never does | unmet; the split bow between them |
| Lei Yanshu | her instructor sent her (record) | the one sentence with no figure and no "To be exact" | unmet; she holds the one number on the arrow |
| Maud Harrowgate | the ward was proofed at the quarterly (record) | her palm flat on the inspector's book she does not open | Rovhen: pressing |
| Tobin Sallow | the rest of the row is the same as number six (six plates on it are cased) | he wipes his palms down his apron one at a time | Rovhen: warm, for Edmund's sake |
| Joan Aldery | "Nail. At the counting-house door." (record) | she answers before she is asked and turns the cuff under with two fingers | Rovhen: owed |
| Imogen Pell | "Everyone says" (one person told her) | slate face down, palm flat on it, no smile | Rovhen: using him |
| Agnes Tull | says she saw it herself when it reached her as talk | she drops "they say" | Rovhen: curious |
| Wenna Crale | nobody came by the east corridor but the runner (she saw the dry flags) | she waits to be asked; her eyes go once along the floor | Rovhen: civil and watching |
| Anselm Pike | the five narrow-pen names are in order, late enrolments | says it with a finger on his own blotted entries, not looking at the five | Rovhen: neutral |
| Hob and Dunstan Pryor | there is no more to Cullen Pit than "They said the seam shifted" | Hob's thumb along the bench grain; Dunstan looks, Hob does not look back | Rovhen: warm and wary |

The public face (`roster(public=True)`) still prints only look, voice and role; none of these fields reaches it.

## State of Play drafts (not published)

- `state-of-play/sodoku-moto-kharven.md`: the live date, the paper on the table, what is owed by line id, the Fronts by sign, the bonds, heat, injuries, the one unchecked belief, and the six-year fixed future.
- `state-of-play/hild-ice-kharven-seat.md`: closed; what it hands to Kharven and what it closes.
- `state-of-play/kwon-mu-jin-hon-guk.md`: not a live thread; folded into the Academy.
- `state-of-play/kwon-mu-jin-aetherion-academy.md`: one page for the Mu-jin and Rovhen pages, each of his people by canon, who is doing what tonight, the Fronts by sign, the bonds, heat, and the beats left unplayed between Monday and day four.

Each carries a "Drafting notes" block to strip before publishing.

## Found and not done here

- **Korvaeth.** Not on this job's list of State of Play pages, so not drafted. Its page dates from 10 September and its Fronts were seeded from the yard's eleven-years-on epilogue; the year-eleven arc (Coldwater to the ridge, about twenty-five scenes) has run past it. Its roster, heat and bond lines are owed at its next session.
- **Kharven roster.** The thread has no roster rows; Lambert, Tabitha, Bram, Brida, Robin Ice, Miku and the rest are owed want, lie and tell, doing now and stands with at the next close (R72-25, R72-26).
- **Academy scenes without a close.** The Night Register run (*Wystan's Briefing*, *Shiori's Findings*, *Malphas on the Line*, *Mu-jin: The Card*, *The Old Colleague*, *The Reader's Oath*) has no Ledger line or Front; owed at the next close.
- **Canon flags, recorded and not ruled.** Emira eighteen in the third month after the ninth hour and twenty-four at the naming; Miku nine at the Brine crossing and fourteen at the signing the next spring; Rikudoku ten in the fourth year and thirteen at the Academy; Taesyn's "Uncle Mu-jin".
- **Tool note.** A thread name is matched by substring; a session for Rovhen alone should pass 'Aetherion'. The `fired` date on L014 is the table day (2026-09-22) because no story date is held, the same fallback `fire()` uses.
- **Preserved text.** Two old `due` values kept verbatim in notes (L035's in its `reconciled` note, L049's in `collected.was_due`) contain em dashes from the original data; nothing written new uses one.

## Checks run

- Every open line at HEAD is accounted for (the script refuses to save if one is left untouched): 39 kept, 24 retired.
- `bash build/py.sh` on `table.render()`: fronts 15, ledger 72, npcs 10.
- Through `build/mcp_server.py`'s own tool functions: `fronts()` and `fronts(thread)` for Kharven, Sodoku Moto, Korvaeth, Mu-jin and Aetherion (each finds its Fronts); `due()` and `due(thread)` (L014 only; nothing else has fired); `roster(public=True)` and `roster()` (no R72-25 gap); `scene_menu('Kharven')` and `scene_menu('Kwon Mu-jin')` (hooks build from the new data).
- `build/validate.py`: PASS.
