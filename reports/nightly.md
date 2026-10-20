# Nightly — 2026-10-20 03:30

## Overnight

The big change is yesterday's new-lore batch: 19 scenes archived (The Uncounted, chapters one to eight, plus the Naiser, Muken, Keld and white-wolf/knot scenes). All 19 pass verify with 0 FAILs and a handful of WARNs (two hypophora questions in Naiser's Answer, the rest minor).
Validate passes, the docket is empty, one conflict is still open, and the 4 reconcile findings haven't moved: nothing new, nothing cleared.
Sync pushed 104 times with no failures. The backup ran Sunday 10-18 and is on schedule. Nothing on the machine needs you this morning.
What the batch left behind is names with no page. The batch leans on a cast that has no wiki pages yet. The ones that recur across many scenes are the Kōkan Line itself, Kagenori Tenrai, Kiyome Byakuya, Tetsugen Akagane, Shigure Tenrai, Hayato Amagiri, Torvald and Yusif Stark (and "the Starks"), Kessen, the Lanternless and Ridgewall.
Further down: Draycott/Hollis Draycott, Vessant, Orrel, Ironlink, Sumie, Hiroe, Shimane, Shirogane, Senri, Godfrey Greymane, Bridgemarch, Hollenmark, Fennick, Aldwin, Veyrath.
Shaka shows up five times, but he's Zettari and another player's, so he gets no page from us. Isaac, Yeah, Nonsense and Annals are false hits from the tool.
Here's what I'd do: a page pass for the recurring dozen first, starting with the Kōkan Line, since NATALIE names it as the ruling house and it still has no page of its own.
Both books are still blocked on your chapter-1 gate (kharven-year and night-watch-zombification). One `--approve 1` or `--reject 1` each unblocks them.

## Numbers

- validate PASS
- docket 0 outstanding
- conflicts open 1
- findings NEW 0 / CLEARED 0 / STILL OPEN 4

## Scenes archived since the last run

- `naiser_and_seradris_the_courtyard`
- `naisers_answer`
- `naisers_terms`
- `the_bearer_of_weight`
- `the_honest_door`
- `the_iron_fist_of_the_keld`
- `the_meeting_at_the_cedar_enclave`
- `the_truth_of_muken`
- `the_uncounted_chapter_eight_the_inheritance`
- `the_uncounted_chapter_five_kharvens_foot`
- `the_uncounted_chapter_four_three_days`
- `the_uncounted_chapter_one_the_map_at_halcrest`
- `the_uncounted_chapter_seven_crows`
- `the_uncounted_chapter_six_the_captain_of_the_foot`
- `the_uncounted_chapter_three_the_tokenless`
- `the_uncounted_chapter_two_big_bertha`
- `the_verdict_of_six`
- `the_white_knot`
- `the_white_wolf`

## The book

- **kharven-year**: 1/12 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/kharven-year/ch01/GATE.md)
- **night-watch-zombification**: 10/80 chapters written. Next: blocked — chapter 1 is written and gated; Isaac has not decided (--approve 1 / --reject 1)
  - nothing more is written until you answer: `python build/book_next.py --approve 1` or `--reject 1 --note "..."` (book/night-watch-zombification/ch01/GATE.md)

## New findings since last night

- none

## Cleared since last night

- none

## Still open: 4 (see reports/reconcile.md)

## The sync (last 26 h) and the weekly backup

- sync: 104 push(es), 0 quiet run(s), 0 push failure(s)
- backup: weekly (Sunday 03:00), last 2026-10-18 (2 day(s) ago, on schedule): wrote /home/oridon/wotr-backups/wotr-2026-10-18.zip (38.1 MB, 1579 files)
- last run of this digest: 2026-10-19T03:30:00
