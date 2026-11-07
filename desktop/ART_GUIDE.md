# WOTR Art Guide

Isaac's direction, 2026-11-07: WOTR art is **one consistent, beautiful, mystical style throughout**,
**manga and comic in its line**. Cards, panels, techniques and places read as one book. He set it from two
reference pieces, described here so the look survives without the files:

- A full-body figure in clean manhwa linework with flat cel color: an emerald cloak edged in gold over
  black, ornate embroidered coat and tall boots, a black horse behind him, a deep green forest. The
  costume carries the image.
- A back three-quarter bust in loose, rough brushwork: a white fur collar, an olive military coat with
  gold diamond ornaments and an epaulet, a hard diagonal beam of white light with a chromatic fringe
  against black. Graphic flat shapes, strong light.

What they share, and what every WOTR image keeps: bold ink line, flat cel color, a narrow jewel palette
with gold doing the shine, ornate period dress worn by elegant figures, dramatic light, and a mystical
air: soft glow, drifting motes of light, light rays. Color always (NATALIE.md, THE TONE): never gray,
never muted, never grimdark.

The images are made locally on Ultron's GPU through ComfyUI with the `comfy` tool; the `wotr-render`
skill is the how-to. This page is the what.

## The house style

One model and one tag block for everything in the house style: **NoobAI-XL 1.1** (an anime SDXL model;
it reads Danbooru tags). Every `wotr_*` workflow carries the block below and drops the subject into
its `{prompt}` slot, so a prompt names only who or what is in the picture.

```
quality:  masterpiece, best quality, newest, absurdres, highres, very aesthetic
house:    medieval fantasy, colored manga, comic, bold lineart, ink lines, cel shading, flat color,
          beautiful, ethereal, mystical, soft glow, glowing particles, light rays, dramatic lighting,
          vivid colors
negative: child, loli, shota, chibi, halo, mandala, modern, suit, necktie, cars, worst quality,
          low quality, lowres, oldest, early, 3d, realistic, photorealistic, glossy, shiny skin, moe,
          washed out, desaturated, bad anatomy, bad hands, extra fingers, watermark, signature, text,
          speech bubble, blurry, jpeg artifacts
```

Cards add `solo focus, looking at viewer, detailed clothing` and refuse panels, borders, silhouettes and
backs to the viewer. What was learned tuning it: `gold trim`, `jewel tones`, `rim light` and `sacred gold`
drown a picture in gold mandalas; `scenery` or `outdoors` in a card's block lets the background swallow
the person; `comic` alone splits a card into panels. The generator that writes the workflows is
`~/wotr-vault/comfy/gen_wotr_workflows.py`; change the block there and re-run it, never by hand in eight
files.

## The workflows

| Workflow | Size | Use |
|---|---|---|
| `wotr_card_full` | 832x1216 | a person's main card image: full body, the whole kit |
| `wotr_card_bust` | 896x1152 | head and shoulders: rosters, Discord, the voice line's face |
| `wotr_turnaround` | 1536x1024 | front, side and back views on one sheet, for later consistency |
| `wotr_release` | 832x1216 | the same person mid-Release, aura blazing |
| `wotr_technique` | 1216x832 | a working at the instant it fires |
| `wotr_panel` | 1216x832 | one manga panel of a fight beat: speed lines, impact |
| `wotr_location` | 1536x896 | a place, wide, no people |
| `wotr_clip` | from the still | an approved still set moving, 2 s (Wan 2.2), ~2 min |

All but `wotr_clip` take 15 to 25 seconds. The older plain workflows (`text_to_image` on Z-Image,
`bestiary_creature`, `heraldry_sigil`, `four_quarters_map`, `upscale_4x`, `background_remove`) stay for
work outside the house style: emblems, maps, cut-outs and upscales.

## Writing the prompt

Tags, not sentences, in this order: **who, body, gear piece by piece, the moment, the place.**

1. **Count and age, every time.** `1boy` / `1girl` / `2boys`, then `adult` and an age band: `young adult`
   reads early twenties, `adult man` thirties, `mature male` forties and lined. Every person drawn is an
   adult unless a card says otherwise, and a minor is never drawn in any sexual or suggestive frame:
   Isaac's floor, which no model setting moves. The negative already refuses `child, loli, shota`.
2. **Body.** Build, skin, hair, eyes, marks, by the card: `tall, slender, gray-violet skin, white hair`.
3. **Gear is a flex** (R85-1). Name each piece in words the model knows: `japanese armor, red armor`
   works where `red enamel lamellar` does not; `fur-trimmed cloak, gold embroidery, tall boots, longsword
   at hip`. Material and color on every piece.
4. **The moment.** Pose and expression from the card's voice: `arms crossed, smirk`, `drawing sword`.
5. **The place.** One or two tags from the culture (below).
6. **Magic.** An aura or working takes its Wellspring's hue from *The Color of Essence*
   (`wiki/The Magic System/The Soul and the Climb/The Color of Essence.md`): `crimson aura, red lightning`.
   Stage sets clarity: a low Stage's aura is clouded and smoky, a high one clean and near white.

No real person's likeness, no living artist's name: describe the style. No text in the image; it
comes out as nonsense letters.

## The peoples

Each culture's cues, from its Standing Inventory (`desktop/inventories/`). Use them as tags; read the
inventory for more.

| People | Cues |
|---|---|
| Moto | red enamel over blackened steel, lacquer, jade and iron prayer beads, ring-lined irises, a metallic sheen at brow and collarbone |
| Kharven | hide coats greased dark at the cuffs, fur hoods, felt, seal-fat lamps, frost and breath plumes, smoke over a frozen town |
| Accord | chartered officials, green, blue and gold, obsidian wax seals, silver rank tokens, brass assay posts, every street lamp its keeper's color |
| Dawi | forge-flush cheeks, untrimmed ringed beards, Soul-Runes on the arms, forge light on wet rock |
| Eresse | high elves, sacred gold and ironwood brown, sap amber, half-lit chambers below ground |
| Expanse | burnt-ochre or deep red skin with gold or bronze etchings, brass or iron eyes, iron rings in a topknot, obsidian, sulfur yellow, volcanic glass |
| Korvaeth | drow, gray-violet skin, flat white hair bound in one black cord, salt-black coats, gold for anything sworn |
| Ketsuen | raw pale timber, gray limestone, birch bark, glacial lakes |
| Marrowkin | chest-high and door-wide, shining amber-to-coal-red eyes, carved horn or ivory slit visors, ember red, rust and copper |
| Nalūn | translucent amber salt walls, the steady amber Chain Light, white rime, iron and bronze tokens |
| Stannvaard | assay stamps, forge-arrays, the great water clock, the tender's shake |
| Yukari | black hair with a silver shimmer, violet-black corona irises (crimson when taken), cedar and limestone archives |
| Zettari | another player's people: their creator's art and word govern; draw them only from what he gives |

## Keeping a person themselves

When Isaac approves an image of a person, the card gets an **art line**: the workflow, the seed and the
exact tag block for body and gear. Every later image of that person starts from that line, changing only
the moment and the place. The approved file's path goes beside it. Stronger likeness later: the
approved portrait fed back as a reference image (IP-Adapter), or a small LoRA trained per major
character; neither is installed yet.

## Where images go

Every render lands in `~/wotr-drafts/images/` as a draft. It goes on a card or wiki page only when Isaac
says so, filed the `art-drop` way. Nothing is published by default.
