"""Apply blockops.json to Notion: patch_block (text, explicit rich_text, colour-only, find-by-text),
delete_blocks, append_children. Dry run unless --apply.
  bash build/py.sh ~/wotr-drafts/alchemetrica/apply_blockops.py BLOCKOPS.json [--apply]"""
import json, sys
sys.path.insert(0, "/home/oridon/wotr-rule-index/build")
from notion_export import api, paginate, rich  # noqa: E402
from notion_publish import rich_text  # noqa: E402

APPLY = "--apply" in sys.argv
ops = json.load(open(sys.argv[1]))
bad = 0


def live_text(b):
    return rich(b[b["type"]].get("rich_text", [])).strip()


def find_block(spec):
    for b in paginate("GET", f"/blocks/{spec['parent']}/children?page_size=100"):
        if b["type"] == spec["type"] and live_text(b) == spec["text"]:
            return b
    return None


for op in ops:
    tag = op.get("item", "?")
    if "patch_block" in op:
        p = op["patch_block"]
        b = api("GET", f"/blocks/{p['id']}") if p.get("id") else find_block(p["find"])
        if b is None:
            print(f"{tag:5} patch   NOT FOUND {p.get('find')}"); bad += 1; continue
        t = b["type"]
        live = live_text(b)
        colour_only = p["old"] == p["new"] and "color" in p
        if colour_only:
            done = b[t].get("color") == p["color"]
            print(f"{tag:5} colour  {'DONE' if done else 'SET ' + p['color']}  {live[:50]!r}")
            if APPLY and not done:
                api("PATCH", f"/blocks/{b['id']}", {t: {"rich_text": [{"type": r["type"], r["type"]: r[r["type"]], "annotations": r["annotations"]} for r in b[t]["rich_text"]], "color": p["color"]}})
            continue
        if live == p["new"].strip():
            print(f"{tag:5} patch   DONE"); continue
        if live != p["old"].strip():
            print(f"{tag:5} patch   MISS\n      live: {live[:160]!r}\n      old:  {p['old'][:160]!r}"); bad += 1; continue
        body = {"rich_text": p.get("rich_text") or rich_text(p["new"])}
        if "color" in p:
            body["color"] = p["color"]
        print(f"{tag:5} patch   MATCH")
        if APPLY:
            api("PATCH", f"/blocks/{b['id']}", {t: body})
    elif "delete_blocks" in op:
        for d in op["delete_blocks"]:
            b = api("GET", f"/blocks/{d['id']}")
            if b.get("archived") or b.get("in_trash"):
                print(f"{tag:5} delete  GONE {d['id'][:8]}"); continue
            live = live_text(b)
            want = d["text"].strip()
            if "..." in want:
                h, z = [x.strip() for x in want.split("...", 1)]
                ok = live.startswith(h) and live.endswith(z)
            else:
                ok = live == want or (want and live.startswith(want))
            print(f"{tag:5} delete  {'MATCH' if ok else 'MISS'} {d['id'][:8]} {live[:50]!r}")
            if not ok:
                bad += 1
            elif APPLY:
                api("DELETE", f"/blocks/{d['id']}")
    elif "append_children" in op:
        a = op["append_children"]
        kids = list(paginate("GET", f"/blocks/{a['parent']}/children?page_size=100"))
        plain = lambda k: "".join(r.get("plain_text", "") for r in k[k["type"]].get("rich_text", [])).strip()
        live_plain = [plain(k) for k in kids]
        new_plain = ["".join(r["text"]["content"] for r in rich_text(c["text"])).strip() for c in a["children"] if c["text"]]
        if new_plain and all(n in live_plain for n in new_plain):
            print(f"{tag:5} append  DONE"); continue
        after = next((k for k in kids if k["id"] == a["after"]), None)
        ok = after is not None
        print(f"{tag:5} append  {'MATCH' if ok else 'MISS'} after {a['after'][:8]} ({len(a['children'])} blocks)")
        if not ok:
            bad += 1; continue
        if APPLY:
            blocks = [{"object": "block", "type": c["type"], c["type"]: {"rich_text": rich_text(c["text"]) if c["text"] else []}}
                      for c in a["children"]]
            api("PATCH", f"/blocks/{a['parent']}/children", {"children": blocks, "after": a["after"]})
    else:
        print(f"{tag:5} ??? {list(op)}"); bad += 1
print("MISSES:", bad)
sys.exit(1 if bad else 0)
