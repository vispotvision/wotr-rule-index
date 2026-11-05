#!/usr/bin/env python3
"""`wotr-mcp index` against build/embed_index.py, byte for byte, in scratch copies of the repo.

  bash build/py.sh rust/index_parity.py [--dir SCRATCH] [--mini]   # exit 1 on any mismatch

Two scratch roots get the same copy of wiki/, scenes/ and lore/v1/scenes/ (build/models is a
symlink to the real model cache). One builds with a copy of embed_index.py whose ROOT points at it,
the other with `WOTR_ROOT=<root> wotr-mcp index`. After every step both roots get the same edits and
both indexes are compared: chunks.json byte for byte with only the "built" timestamp blanked,
vectors.npy byte for byte, and the stats line with the root and the seconds blanked. Where vectors
differ, the largest absolute difference is printed and 50 queries go through the Rust wiki and
scene_recall tools against both indexes. The real build/index/ is never touched.

Scenarios: (a) the full corpus from scratch, (a2) a rebuild with nothing changed, (b1) one page
changed, (b) pages edited, added (one under a scene cast/ folder, one SKIP_NAMES page) and deleted,
(c) odd pages (empty, one huge paragraph, headings only, unicode, CRLF, invalid UTF-8, a BOM, an
unclosed frontmatter, odd names, duplicates, a passage over 512 tokens), (c2) an unreadable page
(both must fail and leave the index as it was), and on small roots (d) a corrupt old index, a
mismatched old index, and an empty corpus. --mini runs (c), (c2) and (d) only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BIN = REPO / "rust" / "target" / "release" / "wotr-mcp"
CORPUS = ["wiki", "scenes", "lore/v1/scenes"]
args = sys.argv[1:]
SCRATCH = Path(args[args.index("--dir") + 1]) if "--dir" in args else Path(tempfile.mkdtemp(prefix="index_parity-"))
failures: list[str] = []
timings: list[tuple[str, float, float]] = []


def make_root(name: str, corpus: bool) -> Path:
    r = SCRATCH / name
    if r.exists():
        subprocess.run(["chmod", "-R", "u+rwX", str(r)], check=False)
        shutil.rmtree(r)
    (r / "build").mkdir(parents=True)
    (r / "build" / "models").symlink_to(REPO / "build" / "models")
    if corpus:
        for c in CORPUS:
            shutil.copytree(REPO / c, r / c, symlinks=True)
    if name.startswith("py"):
        src = (REPO / "build" / "embed_index.py").read_text(encoding="utf-8")
        line = "ROOT = Path(__file__).resolve().parents[1]"
        assert line in src, "embed_index.py's ROOT line moved"
        (r / "build" / "embed_index.py").write_text(src.replace(line, f"ROOT = Path({str(r)!r})"), encoding="utf-8")
    return r


def run_py(r: Path, *extra: str) -> tuple[int, str, float]:
    t = time.time()
    p = subprocess.run([sys.executable, str(r / "build" / "embed_index.py"), *extra], cwd=r, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr, time.time() - t


def run_rs(r: Path, *extra: str) -> tuple[int, str, float]:
    t = time.time()
    p = subprocess.run([str(BIN), "index", *extra], cwd=r, capture_output=True, text=True, env={**os.environ, "WOTR_ROOT": str(r)})
    return p.returncode, p.stdout + p.stderr, time.time() - t


def blank(out: str, r: Path) -> str:
    return re.sub(r"in [0-9.]+s ->", "in Xs ->", out.replace(str(r), "ROOT"))


def files_of(r: Path) -> tuple[bytes, bytes]:
    ix = r / "build" / "index"
    meta = (ix / "chunks.json").read_bytes() if (ix / "chunks.json").exists() else b""
    vec = (ix / "vectors.npy").read_bytes() if (ix / "vectors.npy").exists() else b""
    return re.sub(rb'^\{"model": "[^"]*", "built": "[^"]*"', b'{"model": M, "built": B', meta, count=1), vec


def step(label: str, py: Path, rs: Path, *extra: str, expect_fail: bool = False):
    before = files_of(py), files_of(rs)
    (pc, pout, pt), (rc, rout, rt) = run_py(py, *extra), run_rs(rs, *extra)
    timings.append((label, pt, rt))
    ok = True
    if expect_fail:
        if pc == 0 or rc == 0:
            failures.append(f"{label}: expected both to fail, python exit {pc}, rust exit {rc}")
            ok = False
        if files_of(py) != before[0] or files_of(rs) != before[1]:
            failures.append(f"{label}: a failed build changed the index")
            ok = False
        print(f"[{'ok' if ok else 'FAIL'}] {label}: both failed (python {pc}, rust {rc}), indexes untouched; "
              f"rust said: {rout.strip().splitlines()[-1] if rout.strip() else ''}")
        return
    if pc or rc:
        failures.append(f"{label}: python exit {pc}, rust exit {rc}\n{pout[-2000:]}\n{rout[-2000:]}")
        print(f"[FAIL] {label}: exit codes {pc}/{rc}")
        return
    if blank(pout, py) != blank(rout, rs):
        failures.append(f"{label}: stdout differs\n  py: {pout!r}\n  rs: {rout!r}")
        ok = False
    (pm, pv), (rm, rv) = files_of(py), files_of(rs)
    same_m, same_v = pm == rm, pv == rv
    if not same_m:
        failures.append(f"{label}: chunks.json differs")
        diff_chunks(pm, rm)
    if not same_v:
        failures.append(f"{label}: vectors.npy differs")
        vector_report(label, py, rs)
    ok = ok and same_m and same_v
    print(f"[{'ok' if ok else 'FAIL'}] {label}: chunks.json {'identical' if same_m else 'DIFFERENT'}, "
          f"vectors.npy {'identical' if same_v else 'DIFFERENT'} ({len(pv)} bytes); python {pt:.1f}s, rust {rt:.1f}s; "
          f"{pout.strip() or '(quiet)'}".replace(str(py), "ROOT"))


def diff_chunks(pm: bytes, rm: bytes):
    a, b = json.loads(pm), json.loads(rm)
    if len(a["chunks"]) != len(b["chunks"]):
        print(f"    chunk count {len(a['chunks'])} vs {len(b['chunks'])}")
    for x, y in zip(a["chunks"], b["chunks"]):
        if x != y:
            print(f"    first differing chunk:\n      py {json.dumps(x, ensure_ascii=False)[:600]}\n      rs {json.dumps(y, ensure_ascii=False)[:600]}")
            break


def vector_report(label: str, py: Path, rs: Path):
    import numpy as np
    a, b = np.load(py / "build/index/vectors.npy"), np.load(rs / "build/index/vectors.npy")
    if a.shape != b.shape:
        print(f"    shapes {a.shape} vs {b.shape}")
        return
    d = np.abs(a.astype(np.float64) - b.astype(np.float64))
    print(f"    max abs difference {d.max():.3g}, rows differing {(d.max(axis=1) > 0).sum()} of {len(a)}")
    search_check(py, rs)


QUERIES = ["Soul Crystal", "Renard Greymane", "Emira", "Kaalabad", "Pyreveil thermal debt", "What Things Cost",
           "Kōkan Line", "Shirogane", "how does eta work", "Wellspring", "Draw Age standpipes", "Aetherion Academy",
           "Malphas", "Hild Ice", "Cozbi Mahuo", "Yoko Mishiro", "Measurewright", "Release forms", "Dominion Pressure",
           "the Veil", "Moto", "Sodoku Moto Arctic Lion", "Standing Inventory Kharven", "Glyph Index", "Archons and Titans",
           "the duel at the arena", "Amelia Greymane", "a funeral in the snow", "Yukazuri", "the ledger comes due",
           "Glass and Irons", "the king's door", "who swore the oath", "fire meets frost", "Kujo arc", "the medlar tree",
           "the empty place", "star crusher", "the stands before the bell", "a bargain in the market",
           "blood on the ice", "the academy entrance exam", "a drink with the captain", "the house of the dead",
           "an oath broken", "the first release", "the storm over the city", "the brass mains go silent",
           "a lesson that costs", "the war in the north"]


def search_check(py: Path, rs: Path):
    """The same 50 queries through the Rust wiki and scene_recall tools on both indexes."""
    diffs = 0
    for q in QUERIES:
        for tool, a in (("wiki", {"query": q}), ("scene_recall", {"query": q, "old_lore": True})):
            outs = [subprocess.run([str(BIN), "call", tool, json.dumps(a)], capture_output=True, text=True,
                                   cwd=r, env={**os.environ, "WOTR_ROOT": str(r)}).stdout for r in (py, rs)]
            if outs[0] != outs[1]:
                diffs += 1
    print(f"    search check: {diffs} of {2 * len(QUERIES)} tool results differ between the two indexes")
    if diffs:
        failures.append(f"search results differ on {diffs} calls")


# ---------------------------------------------------------------- page edits, applied to both roots
def edit(r: Path, rel: str, fn):
    p = r / rel
    p.write_bytes(fn(p.read_bytes()))


def write(r: Path, rel: str, data):
    p = r / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


def odd_pages(r: Path):
    sentence = "The draw-hum rose under the Guild seal, and Hettrun counted the brass taps — é, 漢, ✨. "
    huge = (sentence * 40) + ("x" * 2500) + " " + (sentence * 25) + ("ü" * 3000)
    pages = {
        "wiki/zz odd/empty.md": "",
        "wiki/zz odd/huge.md": "# Huge Page\n\n" + huge,
        "wiki/zz odd/headings only.md": "# Only Headings\n\n## A\n\n### B\n\n####### Seven hashes\n\n#\tTab heading\n\n##   \nbody under a blank heading\n\n#NoSpace\n\n## Trailing  \nline",
        "wiki/zz odd/unicode É.md": "﻿# Ünïcödé Pägé 漢字\n\nFirst para with   a line separator and a zero​width space.\n\xa0\nSecond after an nbsp line.\n\x1f\nThird after a unit separator line.\n\n\x1c\x1dFramed by file separators\x1e\x1f\n\n## 見出し　\n\n😀 emoji 👩‍👩‍👧 and combining é and RTL שלום\x85after NEL\n\n" + ("ñ" * 950) + "\n\n" + ("한" * 950),
        "wiki/zz odd/crlf.md": "---\r\ntitle: x\r\n---\r\n# CRLF Page\r\n\r\nPara one\r\nline two\r\n\r\nPara\rthree\r\n\r\n\r\n## Next\r\nbody\r",
        "wiki/zz odd/frontmatter open.md": "---\ntitle: never closed\n# Open Front\n\nbody text",
        "wiki/zz odd/title newline.md": "#\nThe title is on the next line\n\nbody",
        "wiki/zz odd/no title.md": "plain text with no heading at all\n\nand a second paragraph",
        "wiki/zz odd/.md": "dot md body",
        "wiki/zz odd/..md": "dot dot md body",
        "wiki/zz odd/a.b.md": "a b body",
        "wiki/zz odd/dup one.md": "# Duplicate\n\nsame body\n\n## Same\n\nrepeat\n\n## Same\n\nrepeat",
        "wiki/zz odd/dup two.md": "# Duplicate\n\nsame body",
        "wiki/zz odd/tokens.md": "# Many Tokens\n\n" + ("a-" * 890),
        "wiki/zz odd/a b/x.md": "# Sort AB\n\nspace dir",
        "wiki/zz odd/a/x.md": "# Sort A\n\nplain dir",
        "wiki/zz odd/a-b.md": "# Sort A-B\n\ndash file",
        "wiki/zz odd/a.md": "# Sort A file\n\nfile",
        "wiki/zz odd/cast/in wiki.md": "# Wiki Cast\n\nnot skipped in the wiki",
        "wiki/zz odd/INDEX.md": "# Skipped\n\nskipped by name",
        "scenes/zz_odd_cast/cast/x.md": "# Cast\n\nskipped under scenes",
    }
    for rel, t in pages.items():
        write(r, rel, t)
    write(r, "wiki/zz odd/bad utf8.md", b"# Bad \xff UTF-8\n\nbytes \xed\xa0\x80 and \xc0\xaf and \xe2\x82 and \xf0\x9f\x98 end\n\n\xe2\x80\x94 ok \xe2")


def mini_root(name: str) -> Path:
    r = make_root(name, corpus=False)
    write(r, "wiki/Start Here.md", (REPO / "wiki" / "Start Here.md").read_bytes() if (REPO / "wiki" / "Start Here.md").exists() else b"# Start\n\nhello")
    for p in sorted((REPO / "scenes").glob("*.md"))[:3]:
        write(r, f"scenes/{p.name}", p.read_bytes())
    odd_pages(r)
    return r


def main():
    if not BIN.exists():
        sys.exit(f"{BIN} missing: cargo build --release in rust/")
    print(f"scratch: {SCRATCH}")
    if "--mini" not in args:
        py, rs = make_root("py", True), make_root("rs", True)
        step("(a) full build from scratch", py, rs)
        step("(a2) rebuild, nothing changed", py, rs)
        wiki = sorted(p.relative_to(py).as_posix() for p in (py / "wiki").rglob("*.md") if p.name != "INDEX.md")
        scenes = sorted(p.relative_to(py).as_posix() for p in (py / "scenes").glob("*.md") if p.name not in ("INDEX.md", "CAST.md", "ARCS.md", "TIMELINE.md", "CONTINUITY.md"))
        for r in (py, rs):
            edit(r, wiki[len(wiki) // 2], lambda b: b + b"\n\nA new closing paragraph, added for the incremental test.\n")
        step("(b1) one page changed", py, rs)
        for r in (py, rs):
            edit(r, wiki[10], lambda b: b.replace(b"the", b"teh", 3))
            edit(r, scenes[0], lambda b: b"# A New Title\n\n" + b)
            write(r, "wiki/Parity New Page.md", "# Parity New Page\n\nA fresh page.\n\n## Its Section\n\nWith a body.")
            write(r, "scenes/parity_new_scene.md", "# The New Scene\n\nRain on the brass mains, then lamplight.")
            write(r, "scenes/cast/parity_cast.md", "# Cast\n\nSPEAKER: skipped")
            write(r, "scenes/CONTINUITY.md", "# Continuity\n\nskipped by name")
            (r / wiki[20]).unlink()
            (r / scenes[1]).unlink()
        step("(b) edits, additions and deletions", py, rs)
        for r in (py, rs):
            odd_pages(r)
        step("(c) odd pages", py, rs)
        for r in (py, rs):
            (r / "wiki/zz odd/huge.md").chmod(0)
        step("(c2) an unreadable page", py, rs, expect_fail=True)
        for r in (py, rs):
            (r / "wiki/zz odd/huge.md").chmod(0o644)
        step("(c3) quiet rebuild (-q)", py, rs, "-q")
    py, rs = mini_root("py-mini"), mini_root("rs-mini")
    step("(d0) small corpus with odd pages from scratch", py, rs)
    for r in (py, rs):
        (r / "wiki/zz odd/huge.md").chmod(0)
    step("(d0b) small corpus, unreadable page", py, rs, expect_fail=True)
    for r in (py, rs):
        (r / "wiki/zz odd/huge.md").chmod(0o644)
        (r / "build/index/chunks.json").write_text("{not json", encoding="utf-8")
    step("(d1) corrupt chunks.json: full re-embed", py, rs)
    for r in (py, rs):
        meta = json.loads((r / "build/index/chunks.json").read_text(encoding="utf-8"))
        meta["chunks"] = meta["chunks"][1:]
        (r / "build/index/chunks.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    step("(d2) old index rows != chunks: full re-embed", py, rs)
    for r in (py, rs):
        for c in CORPUS:
            shutil.rmtree(r / c, ignore_errors=True)
    step("(d3) empty corpus", py, rs)

    print("\ntimings (wall, whole process):")
    for label, pt, rt in timings:
        print(f"  {label:<48} python {pt:7.1f}s   rust {rt:7.1f}s")
    if failures:
        print("\nFAILURES:\n" + "\n".join(failures))
        sys.exit(1)
    print("\nall identical")


main()
