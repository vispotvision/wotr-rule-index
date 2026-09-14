"""/name: compose a name from a culture's ratified element bank (bot/namebank.yaml).

Each builder returns a dict: {"name": headline, "lines": [(label, text), ...],
"rule": id, "note": str, "flags": [str]}. A flag says where the output leans on
bot-supplied filler or where the rule left something open.
"""
import random
from pathlib import Path

import yaml

BANK = yaml.safe_load((Path(__file__).resolve().parent / "namebank.yaml").read_text(encoding="utf-8"))

CULTURES = {
    "mahuo": "Mahuo (Korean stratum)",
    "yukari": "Yukari (Japonic stratum)",
    "dawi": "Dawi (Barrel Dwarves)",
    "concord": "Concord Human (Northern stratum)",
    "holy_sea": "Holy Sea of Alabaster (Latin ordination)",
    "elven": "Elven — pick a branch",
    "beastkin": "Beastkin — pick a lineage",
    "far_northern": "Far-Northern carried name",
}
ELVEN_BRANCHES = list(BANK["elven"]["branches"])
BEASTKIN_LINEAGES = [k for k in BANK["beastkin"]["expectation"] if k != "any"]

NOT_OFFERED = {
    "moto": "Moto names are Japonic-stratum (R23-2-JAPONIC_STRATUM) and the only Moto element bank on file is the Polynesian one, struck by R21-1 and R23-1. No ratified bank; nothing to draw from.",
    "zettari": "The Zettari register is Swahili/Bantu/Arabic in flavour (R32-1) with attested names but no element bank. Nothing to draw from.",
    "chinese": "The Chinese stratum has its six slots (R23-10-CHINESE_SLOTS) but no syllable bank. Nothing to draw from.",
    "goblinoid": "R20-1-GOBLINOID_ANCHOR names the pattern, not the elements. Nothing to draw from.",
    "undaar-keth": "R20-2-UNDAAR_KETH_NAMING refers to a hobgoblin element inventory that is not in the index. Nothing to draw from.",
    "celestial": "Flagged in the amendment as pending a formal naming pass; the working names are placeholders.",
}


def _flat(groups: dict) -> list[tuple[str, str, str]]:
    return [(el, gloss, grp) for grp, els in groups.items() for el, gloss in els.items()]


def _pick2(groups: dict, rng: random.Random):
    a, b = rng.sample(_flat(groups), 2)
    return a, b


def _join(a: str, b: str) -> str:
    return a + b.lower()


def mahuo(rng: random.Random, **_) -> dict:
    b = BANK["mahuo"]
    gen, per = _pick2(b["elements"], rng)
    given = _join(gen[0], per[0]) if rng.random() < 0.5 else _join(per[0], gen[0])
    fam = rng.choice(b["families"])
    full = f"{fam} {given}" if rng.random() < 0.5 else f"{given} {fam}"
    sib = rng.choice([e for e in _flat(b["elements"]) if e[0] not in (gen[0], per[0])])
    sibling = _join(gen[0], sib[0]) if rng.random() < 0.5 else _join(sib[0], gen[0])
    return {"name": full, "rule": b["rule"], "note": b["note"], "flags": [
        "Which syllable is generational in the attested pairs is not fixed by canon; the inventory leaves it flexible."],
        "lines": [("Generation-syllable", f"**{gen[0]}** — {gen[1]} ({gen[2]})"),
                  ("Personal syllable", f"**{per[0]}** — {per[1]} ({per[2]})"),
                  ("Reads as", f"“{gen[1]}” + “{per[1]}”"),
                  ("A cohort sibling", f"{sibling} (shares **{gen[0]}**)")]}


def yukari(rng: random.Random, **_) -> dict:
    b = BANK["yukari"]
    els = _flat(b["elements"])
    child = rng.sample(els, 2)
    adult = rng.sample([e for e in els if e not in child], 2)
    post = rng.sample([e for e in els if e not in child + adult], 2)
    c, a, p = _join(child[0][0], child[1][0]), _join(adult[0][0], adult[1][0]), _join(post[0][0], post[1][0])
    return {"name": f"{a} Yukari", "rule": b["rule"], "note": b["note"], "flags": [
        "Whether a Yukari carries a second topographic surname beside “Yukari” is left open by the inventory."],
        "lines": [("Childhood name", f"**{c}** — {child[0][1]} + {child[1][1]}"),
                  ("Adult name (at the Telling)", f"**{a}** — {adult[0][1]} + {adult[1][1]}"),
                  ("Calling-name (intimates)", f"**{adult[0][0]}**"),
                  ("True name (taboo)", f"**{a} Yukari** — family, Council, a Proving, or before Senri's stone only"),
                  ("Posthumous name", f"**{p}** — {post[0][1]} + {post[1][1]}")]}


def dawi(rng: random.Random, **_) -> dict:
    b = BANK["dawi"]
    x, y = _pick2(b["elements"], rng)
    given = _join(x[0], y[0])
    fa, fb = _pick2(b["elements"], rng)
    father = _join(fa[0], fb[0])
    return {"name": f"{given} {father}sson", "rule": b["rule"], "note": b["note"], "flags": [
        "Consonant gradation at the join: named by the rule, no table given — left plain.",
        "Byname and oath-name are earned in play; the bot does not invent them. An absent oath-name is audible."],
        "lines": [("Given name", f"**{given}** — {x[0]} ({x[1]}) + {y[0]} ({y[1]})"),
                  ("Patronymic", f"**{father}sson** — son/daughter of {father} ({fa[1]}-{fb[1]})"),
                  ("Earned byname", "— (earned; e.g. *the Immovable*, for holding a doorway during a collapse)"),
                  ("Oath-name", "absent — not yet sworn")]}


def concord(rng: random.Random, sex: str = "", **_) -> dict:
    b = BANK["concord"]
    pool = b["male"] if sex == "male" else b["female"] if sex == "female" else b["male"] + b["female"]
    given = rng.choice(pool)
    father = rng.choice(b["male"])
    kind = rng.choice(["patronymic", "occupational", "locative", "descriptive"])
    flags = ["Three people in the village share this given name; the byname is the real identifier."]
    if kind == "patronymic":
        rural = rng.random() < 0.5
        byname = f"{father}sohn" if rural else father
        how = f"patronymic, {'live (rural, one generation)' if rural else 'frozen (urban, chartered)'} — father {father}"
    else:
        byname = rng.choice(b[kind]["list"])
        how = f"{kind} byname"
        flags.append(f"The {kind} list is bot-supplied plain-register filler; the guide gives that type by example only.")
    return {"name": f"{given} {byname}", "rule": b["rule"], "note": b["note"], "flags": flags,
            "lines": [("Given name", f"**{given}** — from the thirty-name pool"), ("Byname", f"**{byname}** — {how}")]}


def holy_sea(rng: random.Random, sex: str = "", **_) -> dict:
    b, c = BANK["holy_sea"], BANK["concord"]
    pool = c["male"] if sex == "male" else c["female"] if sex == "female" else c["male"] + c["female"]
    birth = f"{rng.choice(pool)} {rng.choice(c['male'])}"
    ordination = rng.choice(b["ordination"]["list"])
    title = rng.choice(b["titles"]["list"])
    return {"name": f"{ordination} {title}", "rule": b["rule"], "note": b["note"], "flags": [
        "The Latin ordination and title pools are bot-supplied filler in the attested register (Aurelian Prudentius Custos Clausorum; Verinus VII), not canon.",
        "Which name a speaker uses declares whether the conversation is secular or sacred."],
        "lines": [("Birth name (Concord Common)", f"**{birth}**"),
                  ("Ordination name (Latin, at vows)", f"**{ordination}**"),
                  ("Title / locative", f"**{title}** — add the locative of the seat, e.g. *{title} of …*")]}


def elven(rng: random.Random, branch: str = "", **_) -> dict:
    b = BANK["elven"]
    branch = branch if branch in b["branches"] else rng.choice(ELVEN_BRANCHES)
    br = b["branches"][branch]
    roots = [(k, v) for k, v in b["roots"].items() if k not in ("ma", "ur", "ie")]
    use_branch_root = rng.random() < 0.5
    root, gloss = (br["root"], br["gloss"]) if use_branch_root else rng.choice(roots)
    suffix = br["suffix"]
    name = root.capitalize() + suffix.lstrip("-")
    alt = root.capitalize() + br.get("alt_suffix", "").lstrip("-")
    byname = root.capitalize() + "ith"
    form = br["form"].format(name=name, alt=alt)
    lines = [("Branch", f"**{branch}**"),
             ("Root", f"**{root}** — {gloss}" + (" (the branch's own root)" if use_branch_root else "")),
             ("Suffix", f"**{suffix}** — {b['affixes'].get(suffix, 'none; the branch marks assent another way')}" if suffix else "none — see the form"),
             ("On the page", form),
             ("Small name / by-name", f"**{byname}** (-ith)")]
    return {"name": name, "rule": b["rule"], "note": b["note"], "flags": [
        "Roots carry a pitch contour (level/rising/falling) the text does not spell per root; not rendered here."], "lines": lines}


def beastkin(rng: random.Random, lineage: str = "", **_) -> dict:
    b = BANK["beastkin"]
    lineage = lineage if lineage in b["expectation"] and lineage != "any" else rng.choice(BEASTKIN_LINEAGES)
    circ = rng.choice(list(b["circumstance"].items()))
    own = list(b["expectation"][lineage].items())[0]
    exp = own if rng.random() < 0.75 else list(b["expectation"]["any"].items())[0]
    soul = f"{circ[0]}-{exp[0].lower()}"
    k = b["keeping"]
    return {"name": soul, "rule": b["rule"], "note": b["note"], "flags": [
        "Name-Keeping is documented for the Fox-Spirit lineage; the inventory generalises it to the others and flags that.",
        "The daily use-name is separate and ordinary — not generated here."],
        "lines": [("Lineage", f"**{lineage}**"),
                  ("Circumstance", f"**{circ[0]}** — {circ[1]}"),
                  ("Expectation", f"**{exp[0]}** — {exp[1]}"),
                  ("Soul-name", f"**{soul}** — recorded, not used daily"),
                  ("Name-Keeping", f"*“Fen {soul}, Baru”* ({k['Fen']}; {k['Baru']}) — the witness answers *“Ashe”* ({k['Ashe']})")]}


def far_northern(rng: random.Random, **_) -> dict:
    b = BANK["far_northern"]
    V, ON, CO = b["vowels"], b["onsets"], b["codas"]
    n = rng.choice([2, 2, 3])
    syl = []
    for i in range(n):
        on = rng.choice(ON) if i or rng.random() < 0.8 else ""
        v = rng.choice(V)
        co = rng.choice(CO) if i < n - 1 and rng.random() < 0.45 else ""
        syl.append((on, v, co))
    # geminate across a boundary: double the next onset when the previous syllable has no coda
    parts = []
    for i, (on, v, co) in enumerate(syl):
        if i and not syl[i - 1][2] and on and len(on) == 1 and rng.random() < 0.35:
            on = on * 2
        parts.append(on + v + co)
    name = "".join(parts)
    if rng.random() < 0.6:
        name += rng.choice(b["suffixes"]).lstrip("-")
    name = name.capitalize()
    roll = rng.choice(b["roll_names"]["list"])
    given = rng.choice(BANK["concord"]["male"] + BANK["concord"]["female"])
    return {"name": name, "rule": b["rule"], "note": b["note"], "flags": [
        "Sound-shape only: R23-11-PHONOTACTICS gives the phonology, not a morpheme list. Assign the meaning, and remember the name is a specific dead person given on.",
        "The roll-name list is bot-supplied filler (a trade or landmark, per R23-11-ROLL_NAMES_FROM_ACCORD)."],
        "lines": [("Carried name (household)", f"**{name}** — the kin-turn comes with it"),
                  ("Roll-name (the Accord's ledger)", f"**{given} {roll}** — what the muster and the tax survey use"),
                  ("Unspoken", "while the person it belonged to lies in the death-house, through the Waiting")]}


BUILDERS = {"mahuo": mahuo, "yukari": yukari, "dawi": dawi, "concord": concord, "holy_sea": holy_sea,
            "elven": elven, "beastkin": beastkin, "far_northern": far_northern}


def build(culture: str, seed: int | None = None, **kw) -> dict:
    rng = random.Random(seed)
    return BUILDERS[culture](rng, **kw)
