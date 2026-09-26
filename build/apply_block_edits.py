#!/usr/bin/env python3
"""Apply substring edits to Notion blocks, keeping each character's formatting.

Input JSON: [{"block_id", "edits": [{"old", "new"}], "delete": bool}]. Replaced text takes
the annotations and link of the first character it replaces. Dry run unless --apply.

  bash build/py.sh build/apply_block_edits.py EDITS.json [--apply]
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from notion_export import api  # noqa: E402

KEYS = ("rich_text",)


def chars(rt):
    out = []
    for seg in rt:
        if seg.get("type") != "text":
            return None                      # mentions/equations: leave the block alone
        style = (json.dumps(seg.get("annotations", {}), sort_keys=True), (seg["text"].get("link") or {}).get("url"))
        out += [(c, style) for c in seg["text"]["content"]]
    return out


def rebuild(cs):
    segs = []
    for c, style in cs:
        if segs and segs[-1][1] == style:
            segs[-1][0] += c
        else:
            segs.append([c, style])
    rt = []
    for text, (ann, url) in segs:
        for i in range(0, len(text), 1900):
            t = {"content": text[i:i + 1900]}
            if url:
                t["link"] = {"url": url}
            rt.append({"type": "text", "text": t, "annotations": json.loads(ann)})
    return rt


def main():
    edits = json.loads(Path(sys.argv[1]).read_text())
    apply = "--apply" in sys.argv
    done = skipped = deleted = 0
    for e in edits:
        bid = e["block_id"]
        if e.get("delete"):
            deleted += 1
            if apply:
                api("DELETE", f"/blocks/{bid}")
            continue
        b = api("GET", f"/blocks/{bid}")
        typ = b["type"]
        rts = b[typ]["cells"] if typ == "table_row" else [b[typ].get("rich_text")]
        css = [chars(rt) if rt is not None else None for rt in rts]
        if any(cs is None for cs in css):
            print("SKIP (non-text)", bid); skipped += 1; continue
        ok = True
        for ed in sorted(e.get("edits", []), key=lambda x: -len(x["old"])):
            k = next((k for k, cs in enumerate(css) if ed["old"] in "".join(c for c, _ in cs)), None)
            if k is None:
                print("MISS", bid, repr(ed["old"][:60])); ok = False; continue
            cs = css[k]
            i = "".join(c for c, _ in cs).find(ed["old"])
            style = cs[i][1] if i < len(cs) else cs[-1][1]
            css[k] = cs[:i] + [(c, style) for c in ed["new"]] + cs[i + len(ed["old"]):]
        if not ok:
            skipped += 1
        if apply:
            body = {"cells": [rebuild(cs) for cs in css]} if typ == "table_row" else {"rich_text": rebuild(css[0])}
            api("PATCH", f"/blocks/{bid}", {typ: body})
        done += 1
    print(f"edited {done}, deleted {deleted}, skipped/missed {skipped}{'' if apply else ' (dry run)'}")


if __name__ == "__main__":
    main()
