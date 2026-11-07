---
name: wotr-render
description: Make War of the Realms images and short video on Isaac's own GPU through local ComfyUI, in WOTR's one house style (colored manga and comic, beautiful and mystical). Use when he says render, draw, paint, make an image, show me X, a portrait, a card image, a turnaround, a fight panel, a technique firing, a place, a clip or an animation, or wants a still upscaled, cut out or edited. Picks the workflow, builds the prompt from the card and the culture, calls the comfy tool and files the result. Also the map of the local studios (Freefield, ComfyArt, Manager) beside it.
---

# /render

Read `desktop/ART_GUIDE.md` first: the look, the house tag block, the prompt order, each people's cues.
This file is the how.

Everything runs on Ultron's RX 9070 XT (16 GB, ROCm) through `wotr-comfy.service` at
`http://127.0.0.1:8188`, loopback only. Nothing leaves the machine and nothing is billed. If a call says
ComfyUI did not answer: `systemctl --user start wotr-comfy`, wait ~20 s, call again.

## The call

`comfy(workflow, prompt, negative, image, width, height, seed, name)` on the WOTR MCP (ops surface).
No `workflow` lists them. The result comes back inline (a clip as a strip of frames) and is saved to
`~/wotr-drafts/images/`, with a public link when the call came through the funnel.

- **House workflows** (`wotr_card_full`, `wotr_card_bust`, `wotr_turnaround`, `wotr_release`,
  `wotr_technique`, `wotr_panel`, `wotr_location`, `wotr_clip`) carry the house block; `prompt` is the
  subject only, in tags. `negative` adds to the house negative.
- **`wotr_clip`** takes `image` (an approved still's path) and `prompt` (one motion and one camera move).
  Set `width`/`height` to the still's aspect, multiples of 32 (544x800 for a card). About 2 minutes.
- **Plain workflows** for work outside the house style: `upscale_4x` and `background_remove` take `image`;
  `heraldry_sigil`, `four_quarters_map`, `bestiary_creature` and `text_to_image` run on Z-Image, where
  `prompt` replaces the whole text and reads plain sentences literally (say what each noun is).
- `seed` repeats a take; keep a good one and change only the tags.

## The steps

1. **Read the person or place first:** `character` or `wiki`, and his Pinterest boards
   (`pinterest(board)`) for how they look, dress and carry themselves. Build the tags from that, never
   from memory.
2. **Write the tags** in the guide's order: count and age (always `adult` plus an age band), body, gear
   piece by piece, the moment, the place. Aura hue from *The Color of Essence*.
3. **Call, look, fix.** Read the image that comes back. Wrong age, lost gear, gray palette, a gold
   mandala or a background swallowing the person: retag and call again with the same seed.
4. **A set for a card:** `wotr_card_full`, then `wotr_card_bust` and `wotr_turnaround` on the same tags
   and seed, `wotr_release` once the card has a Release.
5. **Show Isaac** the result in the reply. When he approves a person's image, write the card's art line
   (workflow, seed, tag block, file path) with `update_character`. Placing an image on the wiki is his
   call, filed the `art-drop` way.

## The floor

Every person drawn is an adult unless a card says otherwise, and nothing sexual or suggestive involving
a minor is ever drawn: the house negative refuses `child, loli, shota`, and no prompt removes that. No
real person's likeness, no living artist's name. Explicit adult art is Isaac's call and stays local.

## The studios beside it (open in the browser pane)

- `http://127.0.0.1:8188`, ComfyUI itself, with its **Freefield** tab: about 117 Higgsfield-style one-click
  apps that fetch their own models on first use. The FLUX 3 Klein, Z-Image, upscale, cut-out, depth and
  audio apps fit the 16 GB card; LTX-2.5 apps are slow with offload; the MiniMax H3 apps are left out (US
  license exclusion, and too big).
- `http://127.0.0.1:8188/comfyart/`, **ComfyArt**: a layered design canvas (image, edit, mockups, 3D).
- **ComfyUI-Manager** (the Manager button) installs further node packs and models.
- FLUX 3 Klein and LTX-2.5 are gated on Hugging Face and need Isaac's own token: `hf auth login` in his
  terminal, never pasted into chat.
