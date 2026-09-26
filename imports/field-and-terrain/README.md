# imports/field-and-terrain

Six field-and-terrain figures the system asked for and did not have: numeric
ranges for the four Aetheric Density conditions, a saturation threshold, where
absorbed energy is banked and what bursts it, Ambient Resonance as a facet of
Aetheric Residue, failure terrain for the four Families that lacked it, and a
second Range ladder for reach that is not force.

| File | What it is |
|---|---|
| `derivation.md` | Every figure with its arithmetic, its real-physics grounding and its source by file and line. Repo-facing; the published pages carry the results and cite nothing. |
| `publish.py` | The publisher. Thirteen surgical operations across six Notion pages: three paragraph rewrites and ten insertions. Nothing is deleted, no page body is replaced, and every anchor is matched by text prefix so an edit elsewhere stops the run. |
| `_published/*.md` | The exact body of each operation, as it went up. One file per operation key. |
| `_published_blocks.json` | The block ids `publish.py` wrote, so a re-run replaces nothing and duplicates nothing. |

## Running it

```bash
bash build/py.sh imports/field-and-terrain/publish.py --dry-run
bash build/py.sh imports/field-and-terrain/publish.py --apply
bash build/py.sh imports/field-and-terrain/publish.py --verify   # read the live pages back
```

Nothing here writes `wiki/`. The hourly sync mirrors the pages back.

## The five constants everything rests on

| | |
|---|---|
| **C1** | 1 EU = 1 MJ, so 1 EU/m³ = 1 MPa. Aetheric Density is a pressure. |
| **C2** | The field relaxes at 10⁻³ s⁻¹ (a ten-metre site, a current at 10⁻² m/s). One constant sets the supply ceiling, the saturation threshold and the decay of Resonance, because a linear reservoir uses the same conductivity both ways. |
| **C3** | A crystal lattice fails at about 10 GPa, which is 10⁴ EU/m³ — the floor of the third density condition already. |
| **C4** | A 20 dB margin, and inverse square, put the three non-force reaches one decade apart and make every reach fall as the root of local density. |
| **C5** | Pressure-vessel proof 1.5× and minimum composite burst 2.25× give the overfill limit and the burst. |

## The six results in one line each

1. **Density.** Ambient Saturation 0.1–10 EU/m³, Active Concentration 10–10⁴, Veil-Thin Nexus 10⁴–10⁸, Wellspring Core 10⁸–7.7×10¹⁸, with Aether-thin ground below and zero in a Silence. Supply ceiling is density ÷ 1,000, in AU/s per m³.
2. **Saturation.** 10⁴ EU/m³, or 100 AU/s through each square metre of the region's boundary. Confining causes it; spending does not.
3. **Absorption.** The bank sits in the absorber's Crystal, bounded by rated Flux Density, leaking at 1 − η per second. Holds to 1.5× rating, Overgrown to 2.25×, Fractured at or past it.
4. **Ambient Resonance.** A facet of Residue, in the same EU/m³, down 20 dB in 75 minutes and 60 dB in about four hours; it raises a floor rather than lowering a ceiling, and reach falls as its square root.
5. **Failure terrain.** Limina wants a gradient and quiet; Spatium wants a survey; Vectoria wants a reaction; Vitalia wants warmth and substrate.
6. **Non-force reach.** Anchor reach : authority radius : addressing range = 1 : 10 : 100, the middle rung read off Part Eleven's Passive Pressure Field column. Force range and addressing range cross at B-Grade.
