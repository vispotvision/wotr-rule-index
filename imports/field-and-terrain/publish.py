#!/usr/bin/env python3
"""Field and terrain: publish the derived figures to the system pages.

  bash build/py.sh imports/field-and-terrain/publish.py --dry-run
  bash build/py.sh imports/field-and-terrain/publish.py --apply
  bash build/py.sh imports/field-and-terrain/publish.py --verify

Surgical, not wholesale. Every operation is either

  * `update`      — replace the rich text of one existing paragraph, or
  * `insert`      — add new blocks immediately after a named existing block.

Nothing is deleted and no page body is replaced, so a block this script did not
write is never touched. Each operation names its anchor by a text prefix rather
than by a block id, and refuses to run if the prefix does not match exactly one
block on the page — so a page edited elsewhere stops the run instead of being
scribbled on.

Re-running is safe. `_published_blocks.json` records the ids written for each
operation key; an operation whose ids are all still present on the page is
skipped, and an `update` whose target already carries the new text is skipped.

Markdown -> blocks is `build/notion_publish.md_to_blocks`, the converter the
rest of the wiki is published with, reached through `build/notion_export`'s API
door. Nothing in `build/` is changed and nothing writes `wiki/`; the hourly sync
mirrors the pages back.

Each paragraph below is written as ONE source line. The converter's inline regex
cannot see a bold or italic span that the source wraps across a newline, and
such a span reaches Notion with its asterisks printed as characters.

The arithmetic behind every figure here is `derivation.md`, beside this file.

Needs NOTION_TOKEN (build/py.sh loads it from ~/.config/wotr/env).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api, paginate  # noqa: E402
from notion_publish import md_to_blocks  # noqa: E402

HERE = ROOT / "imports" / "field-and-terrain"
RECORD_DIR = HERE / "_published"
STATE = HERE / "_published_blocks.json"

PAGES = {
    "core-vocabulary": ("The Core Vocabulary", "3b158200-eb22-8183-817e-cc1a61adee53"),
    "eight-families": ("The Eight Families & the Sixty Wellsprings", "3b158200-eb22-814d-9056-edb0fc9827f2"),
    "part-eleven": ("III. Physical Force (Part Eleven)", "3d758200-eb22-816d-8b90-d14e1e94cfd9"),
    "counterplay": ("Counterplay: What Beats a Practitioner", "3d558200-eb22-813a-9012-d11a05c73af6"),
    "harmonic-arts": ("The Harmonic Arts", "3b158200-eb22-81db-9020-dc71b4a83e00"),
    "anima-harmonics": ("Anima Harmonics", "3d958200-eb22-8121-8dd7-e9a3f7ddb270"),
}

# ---------------------------------------------------------------------------
# 1 · The Core Vocabulary

CV_DENSITY = """**Aetheric Density** · The concentration of Aether present in a given volume, read in **EU per cubic metre**. Sets the ceiling on the AU/s output a practitioner can achieve in that location, which is why battles are fought over ground and not only over people. One EU is one megajoule, so a density in EU/m³ is an energy density, and an energy density is a pressure. **A density in EU/m³ is the same figure in megapascals.** So the ceiling is literal. No boundary can be pushed into ground at a pressure the ground does not carry. Ground wins that argument. A site yields at most a thousandth of its density per second, so the ceiling on output is that rate across the volume a practitioner's field reaches. The four conditions are laddered in numbers in *The Eight Families & the Sixty Wellsprings*."""

CV_RESIDUE = """**Aetheric Residue** · Traces left behind by an Essence working. A permanent, if often subtle, change to the location where the working occurred. Always readable by someone patient enough. Residue has a loud phase and a quiet one, and the loud phase has its own name: **Ambient Resonance** is Residue while it is still ringing."""

CV_SATURATION = """**Aetheric Saturation** · A danger state in which excessive Essence floods an area faster than it can disperse. Produces Crystal Fracture Events in everyone exposed, including the person who caused it. The threshold is a density and not a total: **ten thousand EU per cubic metre**, the stress at which a crystal lattice fails. It is reached by leaving that much in each cubic metre of a region, or by sustaining more than **a hundred AU/s through each square metre of the region's boundary**. The threshold grows with the surface while output does not. Confinement saturates. Spending does not. A kilometre of open ground swallows what a hall would not."""

CV_RESONANCE = """**Ambient Resonance** · Residue while it is still ringing, and therefore not a second quantity. It is read in the same EU per cubic metre as any density, because it is the excess a working left behind on its way out of the ground. It falls by a hundredfold in about seventy-five minutes and by a millionfold in about four hours. That is how long ground remembers a working, and how long it remembers a battle. Resonance does not lower a ceiling. It raises a floor. Every reach that depends on being heard above the ground, which is addressing, authority and anchoring, falls as the square root of the total local density. Twenty practitioners working hard over a two-hundred-metre front leave ground on which a Harmonist hears to about two fifths of his ordinary range until it quiets."""

CV_BANK = """**Banked Essence** · A working that takes an incoming load and holds it puts the load in the absorber's own Crystal, not in the room. The bank is bounded by the **rated Flux Density** rather than by the reserve, because a store held at a pressure fails at a pressure. The surplus above rating leaks at the Crystal's own bleed fraction, one minus η of itself per second. A bank therefore lives about three seconds at an η of 0.70 and about twenty at 0.95. The clock is the real limit. **A bank is tempo, not storage.** The leak leaves as heat, sound and structural bleed, so a man holding one is lit up for exactly as long as he holds it."""

CV_OVERFILL = """**Overfill** · Carrying a bank above the rated Flux Density. To **one and a half times** rating the Crystal holds and leaks and takes no lasting harm, and that margin is the whole of an absorber's working room. From one and a half to **two and a quarter times** the lattice takes a permanent set and the rating itself falls: the Crystal has gone **Overgrown**. At or past two and a quarter times it bursts. That is a **Crystal Fracture Event**, in the absorber, from energy that was aimed at him and that he chose to take. Feeding an absorber past his margin is the counter to absorption, and it is cheaper than out-hitting him."""

# ---------------------------------------------------------------------------
# 2 · The Eight Families & the Sixty Wellsprings

EF_BLOCK = """## The Density Scale in Numbers

*The condition is what a surveyor writes down. The number is what the ground will actually give.*

One EU is one megajoule, so a density in EU per cubic metre is an energy density, and an energy density is a pressure. **A density in EU/m³ is the same figure in megapascals.** That one identity is why the scale is a ceiling and not a mood. A boundary cannot be pushed into ground at a pressure the ground does not carry, and what is standing in the ground has a strength measured in the same unit.

**What a site will actually give.** A current crosses a site the size of a hall in about a thousand seconds. That is the interval in which the ground replaces what has been taken from it. So a site yields at most **a thousandth of its density, per second**. The supply rate in AU/s per cubic metre is the density in EU/m³ divided by a thousand, and the ceiling on a practitioner's output is that rate across the volume his field reaches.

| Density | EU/m³ | As pressure | Supply, AU/s per m³ | Where that sits |
|---|---|---|---|---|
| Aether-thin ground | 0.001 to 0.1 | 1 kPa to 0.1 MPa | 10⁻⁶ to 10⁻⁴ | below one atmosphere of Aetheric pressure |
| **Ambient Saturation** | 0.1 to 10 | 0.1 to 10 MPa | 10⁻⁴ to 10⁻² | sea-level air carries 0.25; a one-tesla field, 0.40 |
| **Active Concentration** | 10 to 10⁴ | 10 MPa to 10 GPa | 10⁻² to 10 | a charged cell 2,500; cast powder 6,900 |
| **Veil-Thin Nexus** | 10⁴ to 10⁸ | 10 GPa to 100 TPa | 10 to 10⁵ | the pressure inside a planet; the strongest field a forge has struck, 400,000 |
| **Wellspring Core** | 10⁸ to 7.7×10¹⁸ | 100 TPa and above | 10⁵ to 7.7×10¹⁵ | up to the field at which the void itself begins making matter |

**In a Silence the figure is zero.** That is the whole of why a Silence is not shielding. There is nothing to draw and nothing to push into, which is also why a soul held in one reports the sensation as loneliness rather than as weakness.

**Ambient Saturation is the reference.** Its midpoint, one EU per cubic metre, is the ground every laddered reach is quoted against. Denser ground does not help a practitioner. It raises the floor his own field has to stand above, and addressing range, authority radius and anchor reach all fall as the **square root** of the local density. Concentrated ground cuts all three to an **eighteenth**. A Nexus cuts them to a **thousandth**. A Core cuts them to some **five millionths**. That last figure is the arithmetic behind the sentence in the table above: inside a Core the law the Wellspring carries is the only law operating, and an S-Grade's kilometre of authority is a fifth of a millimetre wide.

**Why residence changes a body.** A person at rest dissipates about a hundred watts through about a fifteenth of a cubic metre, which is one and a half kilowatts per cubic metre. Active Concentration supplies ten to ten thousand kilowatts per cubic metre. The field is putting seven to seven thousand times the subject's own metabolic power density through them, continuously, and a body has no mechanism for declining a power density. That is why Baptism at that condition is involuntary, and why it reaches the shepherd as readily as the adept.

> **Saturation, stated once.** Saturation begins at **ten thousand EU per cubic metre**, the stress at which a crystal lattice fails. It is reached by leaving that much in each cubic metre of a region, or by sustaining more than **a hundred AU/s through each square metre of the region's boundary**. The two are one statement. The second is the first carried out at the current's own speed. The threshold grows with the surface while output does not, so **a kilometre of open ground swallows what a hall would not.** A Zenith field a kilometre across puts about a fifth of one AU/s through each square metre of its edge, a five-hundredth of threshold. The same output inside a twenty-metre hall puts five hundred and fifty through each square metre, five times over, and everyone in the hall is a casualty of it. A drawn circle is the other half of the same arithmetic. A rite bleeding sixty EU a second into two metres of floor reaches Active Concentration within the hour and stays there, which is what the Circle step is for and what an improvised one costs."""

# ---------------------------------------------------------------------------
# 3 · III. Physical Force (Part Eleven)

PE_BLOCK = """## Range Without Force

Not every reach is a strike. A practitioner also has to **name** a thing before he can set a limit on it, **hold** a limit at a distance from his own body, and keep a volume of ground under **his own law** rather than somebody else's. Those three reaches are not the range above and are not governed by it. A working that expresses no force is not bound by the coherence envelope of one that does. They have their own ladder, and it keys to Grade the same way.

**Addressing range** is the greatest distance at which a practitioner can name a thing precisely enough to impose a boundary on it. **Anchor reach** is the greatest distance between the boundary he sets and the practitioner, or the ink, blood, voice or hand that anchors him. **Authority radius** is the radius inside which his own law is the operating law: a Domain's edge, a ward's jurisdiction, a Seal's writ.

The three are one field read at three thresholds, and the thresholds differ by a hundredfold each. A boundary must stand a hundredfold **above** the background to be imposed at all. The background itself is where a law stops being the operating one. A name is narrow and coherent, so it is read a hundredfold **beneath** the background, the way a faint tone is picked out of a loud room by somebody who knows which note to listen for. Field strength falls with the square of distance, so each hundredfold step in threshold is a tenfold step in radius. **Anchor reach, authority radius and addressing range stand as one to ten to a hundred.** The middle rung is the Passive Pressure Field of the table above, which is precisely the distance at which a practitioner's field still stands above ordinary ground.

| Tier Grade | Anchor Reach | Authority Radius | Addressing Range |
|---|---|---|---|
| Hollow | Contact | None | None |
| F | 0.2 m | 2 m | 20 m |
| E | 0.5 m | 5 m | 50 m |
| D | 1 m | 10 m | 100 m |
| C | 3 m | 30 m | 300 m |
| B | 5 m | 50 m | 500 m |
| A | 20 m | 200 m | 2 km |
| S | 100 m | 1 km | 10 km |
| SS | 500 m | 5 km | 50 km |
| SSS | 5 km | 50 km | 500 km |
| X | 300 km | 3,000 km | 30,000 km |
| EX | 1,300 km | 12,700 km | 127,000 km |

**Reading the table.** Hollow has no passive field and therefore no reach past contact. Continental and planetary presence are read as a continent's span and a planet's diameter. Above EX the figures stop here, as they stop above. Every entry is stated for ordinary Ambient ground and for a target that is not working.

**Ground changes all three together.** Each falls as the **square root** of the local Aetheric Density, against the reference of ordinary Ambient ground. That is about ten times further on Aether-thin ground, an eighteenth at Active Concentration, a thousandth at a Veil-Thin Nexus, and some five millionths inside a Wellspring Core. Residue still ringing counts in the same sum, which is why fought-over ground is short ground for hours afterwards. **The ground a practitioner would choose for output is the worst ground he could choose for reach**, and every veteran knows one of those two facts.

**A working target is ten times easier to name.** Anything standing a hundredfold above the background is addressed at ten times the range, and anything performing a working at all stands there. Suppression is the same fact run backwards, and it is paid for continuously rather than once.

**Below Refraction the anchor is not the body.** A working below Stage VII needs voice, hand, ink or blood, and anchor reach is measured from the anchor rather than from the man. This is the whole commercial case for a drawn circle and an inscribed wall. They move the origin to where the boundary is needed, and a good one is worth more than a Grade.

**The crossover.** Projected force range and addressing range cross at B-Grade. Below it a practitioner can name what he cannot hit. From B upward he can hit what he cannot name, and every doctrine of scouting, spotting and signal lives in that gap.

**The failure modes, which are not gentle.** Past addressing range a name does not single its target out. Two men are one address, and the working lands on both of them or on the wrong one. Past anchor reach the boundary sets and slips. Past authority radius nothing of the practitioner's is operating at all, and a Seal sworn on authority he does not hold there closes anyway, with the difference deducted from the speaker."""

# ---------------------------------------------------------------------------
# 4 · Counterplay: What Beats a Practitioner

CP_GROUND = """**Choose the ground by Family.** Terrain is a modifier on efficiency and the modifiers are large. Caloria fails in thermal equilibrium, saturated cold, and oxygen-poor air. Fulguria fails against boiled leather, fired clay, dense fog and a shielded interior. Materia has opinions and no tools on open water. Fluxia cannot act without a medium, so a dry vault is a Fluxia prison. **The counter-Fulguria kit has been leather and ceramic for four centuries and it is not a secret; it is simply cheaper to ignore until somebody dies of it.** Limina needs a gradient, and saturated ground has none left to offer. A crowd is noise. Light him, and fill the room with people. Spatium needs a survey it can trust to say where *here* is, so unmapped ground, warp-scarred ground and ground two Domains are arguing over all leave the transform nothing to solve against. Vectoria needs something to push back. Loose sediment, scree, mud, deep water and free fall take the third law away from him. Vitalia is rate-limited chemistry. Rates roughly halve for every ten degrees you take out of the air, so **winter, bare stone and salted earth are a Vitalia sentence.**"""

CP_SATURATE = """**Saturate it.** Flood the area with Essence faster than it disperses and everyone present takes Fracture risk, **including whoever did it.** A weapon of last resort and a real one, and its practical use is the threat rather than the act. The threshold is a density and not a total: ten thousand EU in each cubic metre, or a hundred AU/s through each square metre of the region's edge. It grows with the surface while output does not, so **you cannot flood a field, only a building, and you have to be inside it.** A Zenith working a kilometre wide is a five-hundredth of threshold. The same output in a hall is five times over it."""

CP_AUTHORITY = """**Shrink his authority.** The radius in which a practitioner's own law is the operating law is his field standing above the ground's, and the ground wins on a square root. Addressing range, anchor reach and authority radius all fall as the root of the local density. Fight him on concentrated ground and all three drop to an eighteenth. At a Veil-Thin Nexus, a thousandth. Inside a Wellspring Core the strongest Domain in the register is a fraction of a millimetre wide, because there the only law operating is the one the Wellspring carries. **This is why a commander who cannot cut the main takes the fight to the vein instead.** It runs the other way too: Aether-thin ground gives him ten times the reach and almost nothing to draw, which is the whole of the Limina bargain."""

CP_OVERFILL = """**Overfill him.** A practitioner who absorbs banks the load in his own Crystal, and what bounds the bank is its rated Flux Density rather than his reserve. To half again over rating he holds it and bleeds. Past half again the lattice takes a permanent set and he is Overgrown. At two and a quarter times rating it bursts, and the Fracture is his, from energy you handed him. **Feeding an absorber is cheaper than out-hitting him.** And the bank is short. It leaks at one minus his efficiency per second, three seconds for a poor Crystal and twenty for a fine one, so a defender who declines to be hit for ten seconds has taken it off him without touching him. The bleed is the tell, and it lasts exactly as long as the bank does."""

# ---------------------------------------------------------------------------
# 5 · The Harmonic Arts

HA_BLOCK = """## The Ambient Floor

Every branch below is limited by a field quantity that is not Aetheric Density and does not behave like it. Density sets a **ceiling** on what a practitioner may draw. **Ambient Resonance sets a floor under what he can hear.** A floor is the worse constraint. No amount of Stage raises a signal already beneath the room.

Ambient Resonance is not a separate field. It is **Aetheric Residue while it is still ringing**, the excess a working left behind on its way out of the ground, and it is read in the same EU per cubic metre as any density. It falls by a hundredfold in about seventy-five minutes and by a millionfold in about four hours. **Ground remembers a working for an afternoon and a battle for an evening.**

A reading is a signal against a background, and field strength falls with the square of distance, so listening range falls as the **square root** of the total local density. Twenty practitioners working hard for five minutes over a two-hundred-metre front leave about six EU in each cubic metre on top of the ordinary one. A Harmonist standing in it hears to **two fifths** of his usual distance until the ground quiets. Indoors it is worse. The same fighting inside a building leaves Active Concentration, where the factor is eighteen rather than two and a half. **A battlefield is the worst place in the world to listen.** A Harmonist ordered to read one has been ordered to do the thing his discipline is least able to do.

> **Which is exactly what Caelmorne bought.** He could not raise the signal, so he lowered the background twice over. His own tone was dampened to near-nothing, and the session was held on a lunar Aether tide, when the site's own ring was at its quietest. A tenfold reduction in the listener's own emission triples the distance at which a fixed source can be resolved. The silence was not humility. It was instrumentation."""

# ---------------------------------------------------------------------------
# 6 · Anima Harmonics

AH_BLOCK = """**The field condition, and which way it runs.** The limit on this branch is not Aetheric Density. Density caps what a practitioner may draw. The limit here is **Ambient Resonance**, Aetheric Residue while it is still ringing, read in the same EU per cubic metre. It raises the floor instead of lowering the ceiling. The floor is the harder constraint. Listening range falls as the square root of the total local density, so a room worked in recently is a short room. A field fought over is deaf. Resonance falls a hundredfold in about seventy-five minutes and a millionfold in about four hours. On ground where twenty practitioners have just spent five minutes, a Harmonist hears to about two fifths of his ordinary distance. Caelmorne's silence and his lunar tides are one technique performed twice: lower the listener, then choose the hour at which the ground is lowest."""

# ---------------------------------------------------------------------------
# The operations, in page order.
#
# anchor: (prefix, skip) -- the block whose plain text starts with `prefix`,
# then `skip` blocks further on. `update` rewrites that block; `insert` puts
# new blocks immediately after it.
#
# marker: a phrase that appears in the new text and nowhere in the old. It is
# how the script knows an operation has already been applied, and it is what
# `--verify` looks for on the live page.

OPS = [
    # --- The Core Vocabulary
    dict(key="cv-density", marker="the same figure in megapascals", page="core-vocabulary", op="update",
         anchor=("Aetheric Density · The concentration", 0), md=CV_DENSITY),
    dict(key="cv-residue", marker="the loud phase has its own name", page="core-vocabulary", op="update",
         anchor=("Aetheric Residue · Traces left behind", 0), md=CV_RESIDUE),
    dict(key="cv-saturation", marker="ten thousand EU per cubic metre", page="core-vocabulary", op="update",
         anchor=("Aetheric Saturation · A danger state", 0), md=CV_SATURATION),
    dict(key="cv-resonance", marker="Residue while it is still ringing, and therefore not a second quantity", page="core-vocabulary", op="insert",
         anchor=("Aetheric Saturation · A danger state", 0), md=CV_RESONANCE),
    dict(key="cv-bank", marker="A bank is tempo, not storage", page="core-vocabulary", op="insert",
         anchor=("Crystal States · The three conditions", 0), md=CV_BANK + "\n\n" + CV_OVERFILL),
    # --- The Eight Families & the Sixty Wellsprings: after the Density Scale table
    dict(key="ef-numbers", marker="The Density Scale in Numbers", page="eight-families", op="insert",
         anchor=("The encounter type determines the direction", 1), md=EF_BLOCK),
    # --- Part Eleven: after the Range and Force Coherence table
    dict(key="pe-nonforce", marker="Range Without Force", page="part-eleven", op="insert",
         anchor=("Projected Force degrades according to", 1), md=PE_BLOCK),
    # --- Counterplay
    dict(key="cp-ground", marker="a Vitalia sentence", page="counterplay", op="update",
         anchor=("Choose the ground by Family.", 0), md=CP_GROUND),
    dict(key="cp-saturate", marker="you cannot flood a field, only a building", page="counterplay", op="update",
         anchor=("Saturate it. Flood the area", 0), md=CP_SATURATE),
    dict(key="cp-authority", marker="Shrink his authority.", page="counterplay", op="insert",
         anchor=("Saturate it. Flood the area", 0), md=CP_AUTHORITY),
    dict(key="cp-overfill", marker="Overfill him.", page="counterplay", op="insert",
         anchor=("Exhaustion. Below ten percent reserve", 0), md=CP_OVERFILL),
    # --- The Harmonic Arts: after the Perceptual Foundation's Temperance Gate line
    dict(key="ha-floor", marker="The Ambient Floor", page="harmonic-arts", op="insert",
         anchor=("Temperance Gate · Stage V (Splintering)", 0), md=HA_BLOCK),
    # --- Anima Harmonics: after "What it cannot do"
    dict(key="ah-floor", marker="The field condition, and which way it runs.", page="anima-harmonics", op="insert",
         anchor=("What it cannot do: tune a soul", 0), md=AH_BLOCK),
]


# ---------------------------------------------------------------------------
# Notion helpers


def plain(b: dict) -> str:
    t = b.get("type", "")
    rt = (b.get(t) or {}).get("rich_text") or []
    return "".join(r.get("plain_text", "") for r in rt)


def children(page_id: str) -> list:
    return list(paginate("GET", f"/blocks/{page_id}/children?page_size=100"))


def find_anchor(blocks: list, prefix: str, skip: int) -> dict:
    hits = [i for i, b in enumerate(blocks) if plain(b).startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"anchor {prefix!r}: expected 1 match, found {len(hits)}")
    j = hits[0] + skip
    if j >= len(blocks):
        raise SystemExit(f"anchor {prefix!r}+{skip}: past the end of the page")
    return blocks[j]


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true", help="read the live pages back and report")
    g.add_argument("--reindex", action="store_true",
                   help="recompute _published_blocks.json from the live pages")
    args = ap.parse_args()

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    cache: dict[str, list] = {}
    done = skipped = 0

    for op in OPS:
        title, pid = PAGES[op["page"]]
        if op["page"] not in cache:
            cache[op["page"]] = children(pid)
        blocks = cache[op["page"]]
        blocks_md = md_to_blocks(op["md"])
        marker = op["marker"]
        assert marker in op["md"], f"{op['key']}: marker not in its own text"
        RECORD_DIR.mkdir(parents=True, exist_ok=True)
        (RECORD_DIR / f"{op['key']}.md").write_text(op["md"] + "\n", encoding="utf-8")

        if args.verify:
            live = "\n".join(plain(b) for b in blocks)
            mark = "OK     " if marker in live else "MISSING"
            print(f"{mark} {op['key']:16s} {title}")
            continue

        anchor = find_anchor(blocks, *op["anchor"])

        if args.reindex:
            if op["op"] == "update":
                print(f"n/a   {op['key']:16s} (an update owns no block ids)")
                continue
            j = blocks.index(anchor) + 1
            got = blocks[j:j + len(blocks_md)]
            joined = "\n".join(plain(b) for b in got)
            if marker not in joined:
                raise SystemExit(f"{op['key']}: the {len(blocks_md)} blocks after the "
                                 f"anchor do not carry its marker")
            state[op["key"]] = [b["id"] for b in got]
            print(f"index {op['key']:16s} {len(got)} block(s)")
            continue

        if op["op"] == "update":
            if marker in plain(anchor):
                print(f"skip  {op['key']:16s} already carries the new text")
                skipped += 1
                continue
            if len(blocks_md) != 1 or blocks_md[0]["type"] != "paragraph":
                raise SystemExit(f"{op['key']}: an update must be exactly one paragraph")
            print(f"UPDATE {op['key']:16s} {title}: {plain(anchor)[:60]}...")
            if args.apply:
                api("PATCH", f"/blocks/{anchor['id']}",
                    {"paragraph": blocks_md[0]["paragraph"]})
                done += 1
        else:
            ids = state.get(op["key"], [])
            present = {b["id"] for b in blocks}
            if ids and all(i in present for i in ids):
                print(f"skip  {op['key']:16s} {len(ids)} block(s) already on the page")
                skipped += 1
                continue
            print(f"INSERT {op['key']:16s} {title}: {len(blocks_md)} block(s) after "
                  f"{plain(anchor)[:50]!r}")
            if args.apply:
                before = {b["id"] for b in blocks}
                res = api("PATCH", f"/blocks/{pid}/children",
                          {"children": blocks_md, "after": anchor["id"]})
                # the API answers with the page's whole child list, so the ids
                # this call added are the ones that were not there before.
                state[op["key"]] = [b["id"] for b in res.get("results", [])
                                    if b["id"] not in before]
                cache[op["page"]] = children(pid)
                done += 1

    if args.apply or args.reindex:
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    if not (args.verify or args.reindex):
        print(f"\n{done} applied, {skipped} skipped, {len(OPS)} operations, "
              f"{len(PAGES)} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
