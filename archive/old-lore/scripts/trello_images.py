#!/usr/bin/env python3
"""Pull the character images off the Trello board onto the Notion cards.

  python build/trello_images.py            # dry run: which Trello card -> which Notion card
  python build/trello_images.py --apply    # download to art/characters/, set each page icon

Every image on a character card (lists "[ Volume ... ]") is saved under
art/characters/<Notion title>/. The card's Trello cover (or its first image) is
shrunk to 512px and set as the Notion page's icon. Needs TRELLO_KEY, TRELLO_TOKEN
and NOTION_TOKEN in ~/.config/wotr/env (bash build/secrets.sh TRELLO_KEY TRELLO_TOKEN).
Re-runs skip cards already done (art/characters/index.json).
"""
import io
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from notion_export import NOTION_VERSION, children, slug  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art" / "characters"
INDEX = ART / "index.json"
BOARD = "6886e04c7c3c9532f2a41d49"
VOLUME_I = "3b158200-eb22-81da-b471-f9bfac2c784c"
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def env(k):
    v = os.environ.get(k)
    if not v:
        sys.exit(f"{k} is not set: bash build/secrets.sh {k}")
    return v


def trello(path, **params):
    r = requests.get(f"https://api.trello.com/1{path}", timeout=60,
                     params={"key": env("TRELLO_KEY"), "token": env("TRELLO_TOKEN"), **params})
    r.raise_for_status()
    return r.json()


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def names_of(card):
    """The character's name (the desc's first heading) and the card's quoted epithet."""
    out = []
    m = re.search(r"^#+\s*(.+)$", card["desc"] or "", re.M)
    if m:
        out.append(m.group(1))
    out += re.findall(r"[\"“]\s*([^\"”]+?)\s*[\"”]", card["name"])
    return [n for n in map(norm, out) if len(n) > 3]


def match(card, pages, by_trello):
    if card["name"] in by_trello:
        return by_trello[card["name"]]
    keys = names_of(card)
    hits = {pid for pid, title in pages.items()
            for part in re.split(r" · | — |, ", title) if norm(part) in keys}
    return hits.pop() if len(hits) == 1 else None


def images(card):
    atts = [a for a in card.get("attachments", [])
            if (a.get("mimeType") or "").startswith("image/") or a.get("name", "").lower().endswith(IMG_EXT)
            or a.get("url", "").lower().split("?")[0].endswith(IMG_EXT)]
    cover = (card.get("cover") or {}).get("idAttachment")
    atts.sort(key=lambda a: a["id"] != cover)  # the cover first: it becomes the icon
    return atts


def download(att):
    headers = {}
    if att.get("isUpload"):
        headers["Authorization"] = f'OAuth oauth_consumer_key="{env("TRELLO_KEY")}", oauth_token="{env("TRELLO_TOKEN")}"'
    r = requests.get(att["url"], headers=headers, timeout=120)
    r.raise_for_status()
    return r.content


def notion(method, path, **kw):
    r = requests.request(method, f"https://api.notion.com/v1{path}", timeout=120, **kw,
                         headers={"Authorization": f"Bearer {env('NOTION_TOKEN')}", "Notion-Version": NOTION_VERSION,
                                  **({"Content-Type": "application/json"} if "json" in kw else {})})
    if not r.ok:
        raise RuntimeError(f"{method} {path} -> {r.status_code}: {r.text[:300]}")
    return r.json()


def set_icon(page_id, raw):
    im = Image.open(io.BytesIO(raw))
    im.thumbnail((512, 512))
    buf = io.BytesIO()
    im.convert("RGBA").save(buf, "PNG")
    up = notion("POST", "/file_uploads", json={"filename": "icon.png", "content_type": "image/png"})
    notion("POST", f"/file_uploads/{up['id']}/send", files={"file": ("icon.png", buf.getvalue(), "image/png")})
    notion("PATCH", f"/pages/{page_id}", json={"icon": {"type": "file_upload", "file_upload": {"id": up["id"]}}})


def main():
    apply = "--apply" in sys.argv
    lists = {l["id"]: l["name"] for l in trello(f"/boards/{BOARD}/lists")}
    cards = [c for c in trello(f"/boards/{BOARD}/cards", attachments="true", attachment_fields="all",
                               fields="name,desc,idList,cover")
             if lists.get(c["idList"], "").startswith("[ Volume")]
    pages = {b["id"]: b["child_page"]["title"] for b in children(VOLUME_I) if b["type"] == "child_page"}
    # cards the Trello conversion already published: exact, no name matching needed
    published = json.loads((ROOT / "build/.publish_imports.json").read_text())
    by_trello = {m["name"]: published[m["file"].replace("imports/trello/", "imports/converted/")]["page_id"]
                 for m in json.loads((ROOT / "imports/MANIFEST.json").read_text())
                 if m["file"].replace("imports/trello/", "imports/converted/") in published}
    done = json.loads(INDEX.read_text()) if INDEX.exists() else {}

    unmatched, noimg = [], []
    for c in cards:
        imgs = images(c)
        if not imgs:
            noimg.append(c["name"])
            continue
        pid = match(c, pages, by_trello)
        if not pid:
            unmatched.append(c["name"])
            continue
        title = pages.get(pid, pid)
        print(f"{len(imgs)} image(s)  {c['name'][:50]:50}  ->  {title}")
        if not apply or done.get(c["id"], {}).get("icon"):
            continue
        folder = ART / slug(title)
        folder.mkdir(parents=True, exist_ok=True)
        files = []
        for i, a in enumerate(imgs, 1):
            raw = download(a)
            name = slug(a.get("name") or "image")
            if not name.lower().endswith(IMG_EXT):
                name += ".png"
            (folder / f"{i:02d}-{name}").write_bytes(raw)
            files.append(f"{i:02d}-{name}")
            if i == 1:
                set_icon(pid, raw)
        done[c["id"]] = {"trello": c["name"], "page_id": pid, "title": title, "files": files, "icon": True}
        INDEX.write_text(json.dumps(done, indent=1, ensure_ascii=False))

    print(f"\n{len(cards)} character cards; {len(noimg)} without images; {len(unmatched)} unmatched:")
    for n in unmatched:
        print("  ?", n)
    if not apply:
        print("\ndry run: nothing downloaded or changed. Re-run with --apply.")


if __name__ == "__main__":
    main()
