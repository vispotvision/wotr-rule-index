#!/usr/bin/env python3
"""Assemble the briefs the conversion agents read, from the wiki mirror, the FOW
workbook and the rule index. Re-run whenever the wiki or the index changes.

  python build/conversion_briefs.py      -> imports/BRIEFS/{common,character,technique,artifact,beast}.md
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
BRIEFS = ROOT / "imports" / "BRIEFS"
sys.path.insert(0, str(ROOT / "build"))
from common import load_rules  # noqa: E402
import mcp_server as M  # noqa: E402


def read(rel: str, first_lines: int | None = None) -> str:
    p = WIKI / rel
    if not p.exists():
        return f"(missing: {rel})"
    t = M._read(p)
    if first_lines:
        t = "\n".join(t.split("\n")[:first_lines])
    return t.strip()


def rules_brief(tags: list[str], limit: int = 80) -> str:
    rules, _ = M._select(tags, ["live"])
    return "\n\n".join(M._fmt(r, full=False) for r in rules[:limit]) + (f"\n\n... {len(rules) - limit} more (load_rules)" if len(rules) > limit else "")


def wellsprings() -> str:
    out = []
    for p in sorted((WIKI / "The Eight Families & the Sixty Wellsprings").glob("*.md")):
        fam = p.stem
        names = re.findall(r"(?m)^###\s+(.+?)\s*$", M._read(p))
        out.append(f"- **{fam}**: " + "; ".join(n.replace("*", "") for n in names))
    return "\n".join(out)


def aether_classes() -> str:
    try:
        import openpyxl
        wb = openpyxl.load_workbook(M.FOW_XLSX, read_only=True, data_only=True)
        ws = wb["Aether Class and Typology"]
        rows = []
        for r in list(ws.iter_rows(values_only=True))[:14]:
            cells = [str(c).strip() for c in r if c is not None and str(c).strip()]
            if cells:
                rows.append("| " + " | ".join(cells) + " |")
        return "\n".join(rows)
    except Exception as e:  # noqa: BLE001
        return f"(aether class sheet unavailable: {e})"


def categories() -> str:
    for r in load_rules():
        if r["id"] == "R10-1-CATEGORIES_AXIS":
            return r["verbatim"].strip()
    return ""


COMMON_HEAD = """# WOTR conversion brief — common to every item

You are converting an item from the old Trello board (*The Dawn of Iridescent
Sovereignty Lost*, the pre-Fracture-of-Worlds era) into current War of the Realms
canon. The world has changed since the card was written. Your output must fit the
world as it is now, in the format of the exemplar for your item type, with every
number derived from the Fracture of Worlds tables below.

## The five laws of this conversion

1. **Only the source's facts, on the current world's terms.** Keep every fact the
   card gives (who, what, history, relationships, powers) unless it contradicts
   current canon; then convert it and say so in the migration note. Do not add
   history the card does not give.
2. **Numbers come off the tables, and you commit to them.** Level, Stage, Band,
   Grades, Sub-Stats, EU, η all derive from what the card states (an old "Stage IX
   — Reflection" is converted to the FOW Stage of the same numeral; the card's power
   description places the Level within that Stage's Band; Grades follow the Tier
   Grade ranges). Where the card gives nothing to derive from, choose the most
   conservative value consistent with the card and the tables, and state the
   choice in one line of the migration note. Isaac has delegated these calls:
   never write "pending Isaac", "estimate" or "TBD" in a slot; write the number.
3. **Verify every proper noun.** Realms, factions, deities, eras, glyph systems,
   languages. Use the `wiki` tool: `wiki("Purganeth")`, `wiki("Parun glyph")`. If it
   exists in current canon, use the current form. If it does not exist, keep it
   only if the card cannot make sense without it, and flag it in the migration
   note as *unattested in current canon*. Old era names convert per the Errata
   table below. Old naming registers convert per the Moto Reversion table (Büri →
   Moto, Ajiin → Hataraki, Altan → Kōkan, Khar Ild → Kurosetsu ...).
4. **Nothing is explained by old-system vocabulary.** "Essence types", "Aether
   Class: <free text>", "Path: Body/Spirit/Judgment", "mana", "spells" as a class —
   these are converted to the current vocabulary: the seven Aether Classes, the
   Four Paths, the Eight Primaries, Wellsprings by Family, Categories, the Four
   Crafts (Chantcraft is folded into Spellcraft, ruled 2026-09-12).
5. **Every technique carries a Counter** (mandatory) and the summary card
   Effect / Cost / Limit / Counter / What nobody knows. A technique must be
   statable as "it does X to Y, which under Z produces W".

## Output

Write the finished markdown to the output path you were given. Start with the
title as `# <Name> · <Epithet>` (characters, artifacts) or `# <Name>` (techniques,
beasts), then a one-paragraph *migration note* in a blockquote stating what was
converted, what was unattested, and what is pending Isaac. Then the sections in
the exemplar's order with the exemplar's exact headings. Prose sections obey the
prose law (no em dashes, no "not X but Y", no countdown negation; you may call
`verify_scene` on a prose section). Under 16,000 characters.

Do not call `create_character` or write to Notion; a review pass runs first.

"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    BRIEFS.mkdir(parents=True, exist_ok=True)

    common = [COMMON_HEAD,
              "## What changed since the board (the lore delta)\n",
              "- **Naming.** Moto register for the Moto bloodline; the Büri/Mongolian register is dead (ruled 2026-09-12). Five naming strata: Japonic (archaic bloodlines), Korean (Mahuo), Chinese (lineage halls), Northern English and Norse (chartered families and commons), Far-Northern carried-name logic. Naming register is not ethnicity.",
              "- **The Draw Age (Pack Eleven).** Wellsprings as standing currents; a worked site is a *Core* in common speech; Cores recharge; draw is a guild-licence good (commoners burn oil); the Guild of Measurewrights measures, the Guild Accord governs; gunpowder exists and armour survives; the technology ceiling is everything invented 1800–1900 and nothing after; Wells can generate hostile entities.",
              "- **The system is Fracture of Worlds.** Sixteen Stages (FOW names: Murmuring, Welling, Ascension, Flourishing, Splintering, Glory, Refraction, Transcendence, Invocation, Realization ...), five Bands by Level, Tier Grades by stat value, eight Primaries with eight Sub-Stats each, seven Aether Classes, Coherence Band and η, the Soul Crystal (Essence Core, Aether Shell, Attraction Layer).",
              "- **Magic.** Sixty Wellsprings in eight Families, each with a Physics Domain; twenty-six Magical Categories; Four Crafts (Magicraft, Spellcraft, Runecraft, Draftcraft; Chantcraft folded into Spellcraft); the Design Chain is prose-legal; mechanism is on the page; the Origin layer is explicable (ruled 2026-09-12).",
              "- **Chronology.** The Errata below governs dates and era names; Epoch figures are myth, not arithmetic.",
              "- **Cosmology.** Omnara and the Division; the Fourteen Archons in six pairs and a dyad; the Fourteen Titans; the Three Epochs; the Celestial Host. Verify any deity or entity the card names.",
              "",
              "## Errata to the Received Registers (dates and eras)\n", read("Cosmology & Metaphysics/Errata to the Received Registers.md", 60),
              "", "## Cosmology, in brief\n", read("Cosmology/Cosmology & Metaphysics.md", 45),
              "", "## The Magic System, in brief\n", read("Magic System/The Magic System.md", 45),
              "", "## Factions, Bloodlines and Institutions, in brief\n", read("Factions/Factions, Bloodlines & Institutions.md", 40),
              "", "## Geography, in brief\n", read("Geography/Geography & the Four Quarters.md", 40),
              "", "## The Sixty Wellsprings by Family (assign harmonisations from this list only)\n", wellsprings(),
              "", "## The Magical Categories\n", categories(),
              "", "## The seven Aether Classes\n", aether_classes(),
              "", "## The FOW scale\n", M._fow_tables(),
              "", "## Moto Reversion table (old → governing)\n", "\n".join(f"- {o} → {n}" for o, n in M._reversion_map() if o not in ("Buri",)),
              "", "## Rules in force that bind every conversion (brief; `rule(id)` for full text)\n", rules_brief(["character-sheet", "stats", "naming", "codex", "magic-design"], 90),
              ]
    (BRIEFS / "common.md").write_text("\n".join(common), encoding="utf-8", newline="\n")

    char = ["# Character brief\n",
            "Format: the **Volume IV migration format** used for every card converted from this board so far. Ten sections, exact headings:",
            "`## I · Identity` (with `### Affiliation` and the Catalyst Event blockquote), `## II · Soul Architecture`, `## III · Wellspring Harmonizations`, `## IV · Primary Stats`, `## V · Sub-Stat Peaks`, `## VI · Traits`, `## VII · Artifacts`, `## VIII · Signature` (one `### <technique>` with Effect / Cost / Limit / Counter / What nobody knows), `## IX · Relationships`, `## X · Chapter Appearances`.",
            "",
            "Stat pool: Stat Pts/Level per Band × levels in each Band, plus the Threshold gates, as in the exemplar (`Pool 8,080 — 4,500 from Bands I–II, 780 from Band III, 2,800 from Thresholds I–VII. Allocated 8,013`). Grades from the Tier Grade table; the Stage's stat ceiling caps every stat. Sub-Stat peaks sit at or a little above their Primary. The card's power description decides where in the Band the Level sits; if the card gives no Stage, read one off the power description (a duellist who worries mid-Stage practitioners is Stage V–VI; a realm-scale power is IX and up) and say so in the migration note. Always fill the stat table.",
            "",
            "Gloss rights (a card field, ruled 2026-09-12) go in section I: yes / diagnostic only / unlimited / never, chosen from how the card's voice reads.",
            "",
            "## Exemplar (converted from this same board; copy its shape exactly)\n",
            read("Volume IV — Character Cards/Adalric Vladimer Valen · The Crimson Shade.md")]
    (BRIEFS / "character.md").write_text("\n".join(char), encoding="utf-8", newline="\n")

    tech = ["# Technique brief (Abilities list, and Spellcraft cards that describe a specific working)\n",
            "Format: `# <Name>`, migration note, then:",
            "`## Summary card` — **Effect**, **Cost**, **Limit**, **Counter**, **What nobody knows** (one line each).",
            "`## Codex line` — Wellspring (from the Sixty), Family, Physics Domain, Category (from the twenty-six), Craft (Magicraft / Spellcraft / Runecraft / Draftcraft), Stage floor, Grade required, Path gate.",
            "`## Design Chain` — Trigger, Function, Mechanism (the real phenomenon it runs on, named), Numerical Effect (from the FOW scale; choose and note where the card is silent), Target Response, Consequence, Limitation, Weakness, Cost, Counterplay.",
            "`## FOW line` — governing Primary and Sub-Stats, Stage floor, Grade required, Path gate, Resonant Pair if any.",
            "`## Origin` — who derived it, where, for what problem (the named inventor rule), from the card's own history.",
            "",
            "A Spellcraft card that describes a discipline or a body of theory rather than one working (e.g. a Harmonics essay) is converted instead as `# <Name>` + migration note + `## What it is` + `## Where it sits in the current system` (Family / Category / Craft it belongs to, with the current pages named) + `## Practitioners and history` + `## What it can and cannot do`, keeping the card's substance.",
            "",
            "## Exemplar technique entries (from a converted character card)\n",
            "\n".join(read("Volume I — Character Cards/Cozbi Mahuo.md").split("## X · Techniques")[1].split("## XI")[0].split("\n")[:60]) if "## X · Techniques" in read("Volume I — Character Cards/Cozbi Mahuo.md") else "",
            "", "## Exemplar signature (Volume IV format)\n",
            read("Volume IV — Character Cards/Adalric Vladimer Valen · The Crimson Shade.md").split("## VIII · Signature")[1].split("## IX")[0]]
    (BRIEFS / "technique.md").write_text("\n".join(tech), encoding="utf-8", newline="\n")

    art = ["# Artifact brief\n",
           "Format: `# <Name> · <Epithet or Type>`, migration note, then:",
           "`## What it is` (type, appearance, provenance from the card, converted eras/names), `## Physical account` (mass, length, point of balance, the armour tier it beats and fails against — R13-9-ITEM_GUIDE_WEAPON_ENTRY; proof-marks if armour; `pending Isaac` where the card gives nothing), `## Operation line` (every working the artefact performs, as a full Design Chain line: what it does to what quantity under what law — R17-5-ARTEFACT_SCOPE), `## Codex line` (Wellspring, Family, Physics Domain, Category, glyphs only if attested in the Master Glyph Index — check with `wiki`), `## Bond and cost` (soulbound? what it costs the bearer), `## Counterplay`, `## Bearers` (from the card).",
           "",
           "## Exemplar (artifact entries inside a converted card)\n",
           read("Volume IV — Character Cards/Adalric Vladimer Valen · The Crimson Shade.md").split("## VII · Artifacts")[1].split("## VIII")[0],
           "", "## Rules that bind items\n", rules_brief(["items"], 40)]
    (BRIEFS / "artifact.md").write_text("\n".join(art), encoding="utf-8", newline="\n")

    beast = ["# Beast brief\n",
             "Format: exactly the entry shape used on the Bestiary category pages: `## <Name>`, an italic-name blockquote (old-tongue names only if attested), a bold classification line (`Type · Tier, Threat · Wellspring affinity · native to`), origin paragraph, description paragraph, behaviour paragraph, an `| Abilities | Weaknesses |` table, and an attested-encounters paragraph. Tiers T0–T9 per the Material/Bestiary scale; threat wording as in the exemplar.",
             "",
             "## Exemplar\n", "\n".join(read("The Bestiary/Spirit Beasts.md").split("\n")[:26])]
    (BRIEFS / "beast.md").write_text("\n".join(beast), encoding="utf-8", newline="\n")

    for f in BRIEFS.glob("*.md"):
        print(f.name, len(f.read_text(encoding='utf-8').split()), "words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
