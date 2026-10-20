# Retcon brief: bringing the 19 scenes into line (2026-10-20)

You are Natalie, editing archived War of the Realms scenes in `scenes/` to Isaac's
new-lore decisions. Read, in this order:
1. `imports/drafts/new-lore-questionnaire/decisions.md` (what governs; Isaac's own words are in `answers.json`)
2. `imports/drafts/new-lore-questionnaire/digest.md` (the contradictions found)
3. `desktop/NATALIE.md`, sections PROSE STANDARDS and THE MAGIC FRAME (the prose law)

## How to edit
- Edit only the files you are assigned, and only in `scenes/`. Never touch `wiki/`: the mirrors are regenerated afterwards. Do not commit, and do not run archive_scene, session_end or any wotr MCP write tool.
- **Rewrite only what the decisions require**, plus the small slips listed for your files. Where a line breaks, rewrite the passage around it so it reads as if it had always been that way. Keep the scene's voice, POV, tense, cadence and beats. Do not shorten, summarise or tidy the scene, and leave untouched prose as it is.
- The prose law holds in every line you write: no em dashes; no "it's not X, it's Y"; no hypophora; no narrator moral after an image; no countdown negation or manufactured fragments. Match the surrounding paragraph's sentence development.
- **What characters know.** A character speaks or thinks only what they could know at that point. Muken and Yukazuri don't know their father until Kiyome tells them (not yet on the page). The north's version of the story ("Gimbzo took her") may stand in northern mouths as rumour when it is clearly framed that way, but no narration or knowing speaker may state it as fact.
- **The author notes.** Every scene ends with an author-notes block. Where it raises a question that is now settled (the retcon flags, "tell me which"), rewrite those bullets to the settled fact. Add one bullet at the top of the notes: `- **Retcon 2026-10-20 (new-lore questionnaire).** <one or two sentences on what changed in this scene>`.
- **Verify.** After editing each file, run `~/.venvs/wotr/bin/python build/verify.py scenes/<file>.md` from `/home/oridon/wotr-rule-index`. It must report 0 FAIL; fix every FAIL. Read the WARNs, and fix any your edit introduced. Pre-existing WARNs can stay.

## The settled facts you will most often need
- **The war.** One war, forty years long, ended about a month before The Uncounted Ch1. Nothing is "twenty-three years" after it. Its last four years were the worst: the Seikai turned, the Soul Plane broke, Ashura was wounded, the Zettari struck the Yukari valleys, and Shimane was fought. Gimbzo burned Hiroe and purged the Kōkan about twenty years ago, and the cellar night was about sixteen or seventeen years ago. Muken is 16 and Yukazuri 13.
- **Gimbzo Kōkan Moto** was the Kōkan king. He purged his own line, ruled forty years from the saddle and never sat the red chair. It has stood empty since the war began (forty years of dust, not a hundred). Dougou of Kushara killed him at Shimane.
- **Kasane Byakuya** was Kiyome's elder sister by twelve years. She took the Yukari name at her Telling at fourteen and was King Gimbzo's sworn guard, and she loved him. She walked out of the cellar on her own feet with the boy. Gimbzo found her once more when Muken was three, and Yukazuri is his. She came to the Halcrest Cuttings (Orrel's galleries) with the boy about sixteen years ago, under no name the clerks would take. She cut salt there, and had a token of her own that hummed (or had one once). She died of salt-throat on the morning the news of Shimane came down the galleries, about a month before Ch1. Her full name in Kiyome's mouth is "Kasane Byakuya, who took the name Yukari at her Telling". Never "Tenrai".
- **Yusif Stark** was like a big brother to Kasane, on the model of Ned Stark raising Jon Snow. He never married her: retcon every marriage, "husband" and "stepfather" line. He shielded and half-raised the children, coming once a season. He never gave them his name, because giving it would have led the hunters to them. He stopped coming when Muken was 13, because he was killed (about three years ago) by those hunting what he hid, and he kept the secret. Ulf knows how; nobody on the page has told Muken yet.
- **Tokenless.** A seal binds to a house name, and the children had none, or didn't know theirs. Their mother's token hummed. The reason is the missing name, not their blood or the mother's mark. (Later, when Muken takes his name, the Kōkan emblem goes on every seal he holds. That isn't on the page yet.)
- **The eye.** What woke at the Foot is the common Moto Shingan. The gold crack in it is the Kōkan sign, the beginning of the Kamigan, and that is what Shigure recognises.
- **Who knew a child lived.** Shigure, Sumie and a few Tenrai knew a child escaped the cellar, and buried it. Tetsugen guessed and never looked. Kiyome and the other lines didn't know until the last ten days.
- **Shigure** has stood at Gimbzo's side since the cellars or longer, never "six years". She loved him and spared his son for his face, and she still reports to Kagenori.
- **House Stark.** Torvald was Ulf's younger brother and the Stark leader of the north's rising, and he named Ulf leader before his execution. Torvald has buried two sons and every brother but Ulf.
- **Renames.** In The Verdict of Six, the kneeling Stark rider is renamed from Ulf to **Hakon**, and the Lambert prisoner from Wystan to **Osbert** (Osbert Lambert, the Hallenfeld tariff-master). Lord Ulf Stark and Lord Wystan Greymane keep their names.
- **Ages.** Kiyome and Naevra are about thirty, and Naevra is a year younger than Naiser. "The last summer before the war" becomes "the last summer before Hiroe", twenty years back.
- **Kharven** is the old name of the high north. Kharven's Seat (the Hall of Verdicts and the hold) and Kharven's Foot stand as written.
- **The Zettari belong to another player.** Never decide a Zettari choice. In Ch8 the outrider reports a Moto lady, about twenty riders without banners, and a Yukari woman walking barefoot. There is no Zettari and no sabre-toothed cat.
- **The Moto lines hold land** (villages, granaries, tenancies).

## Report back
List, per file: each change (old gist, then new gist), the verify result (FAIL and WARN counts), and anything you couldn't reconcile without a decision. Keep it under 600 words per file.
