"""Semantic index over the wiki mirror and the scene archive.

`python build/embed_index.py` (re)builds `build/index/`: every wiki page and
scene is cut into chunks under its nearest heading, each chunk embedded once
with bge-small (ONNX, CPU, no torch) and kept by content hash, so the hourly
sync only pays for what changed. `search()` is what the MCP's `wiki` and
`scene_recall` call: cosine over every chunk, best chunk per file, a small
bonus from the keyword ranker so exact names still win.

The model lands in build/models/fastembed (gitignored, ~130 MB) on first use.
Nothing here writes to sources/ or the wiki.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import threading
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
SCENES = ROOT / "scenes"
INDEX_DIR = ROOT / "build" / "index"
MODEL_DIR = ROOT / "build" / "models" / "fastembed"
MODEL = "BAAI/bge-small-en-v1.5"
CHUNK_CHARS = 900
SKIP_NAMES = {"INDEX.md", "MANIFEST.md"}

_model = None
_loaded: dict | None = None
_lock = threading.Lock()  # the MCP and the Discord bot both call search() from worker threads


def _embedder():
    global _model
    with _lock:
        if _model is None:
            from fastembed import TextEmbedding
            MODEL_DIR.mkdir(parents=True, exist_ok=True)
            _model = TextEmbedding(MODEL, cache_dir=str(MODEL_DIR))
        return _model


def _read(p: Path) -> str:
    t = p.read_text(encoding="utf-8", errors="replace")
    if t.startswith("---\n"):
        end = t.find("\n---\n", 4)
        if end != -1:
            t = t[end + 5:]
    return t


def _files(root: Path):
    for p in sorted(root.rglob("*.md")):
        if p.name in SKIP_NAMES:
            continue
        if root == SCENES and "cast" in p.relative_to(SCENES).parts:
            continue  # cast files repeat the scene text with speaker tags
        yield p


def chunk(text: str, title: str) -> list[tuple[str, str]]:
    """(heading, chunk text) pairs: split on headings, then on paragraphs to size."""
    out = []
    heading = title
    buf: list[str] = []

    def flush():
        body = "\n".join(buf).strip()
        if body:
            out.append((heading, body))
        buf.clear()

    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        m = re.match(r"^(#{1,6})\s+(.+)$", para.splitlines()[0])
        if m:
            flush()
            heading = m.group(2).strip()
            rest = "\n".join(para.splitlines()[1:]).strip()
            if rest:
                buf.append(rest)
            continue
        if sum(len(b) for b in buf) + len(para) > CHUNK_CHARS and buf:
            flush()
        while len(para) > CHUNK_CHARS * 2:  # a single huge paragraph
            cut = para.rfind(". ", 0, CHUNK_CHARS)
            cut = cut + 1 if cut > CHUNK_CHARS // 2 else CHUNK_CHARS
            buf.append(para[:cut].strip())
            flush()
            para = para[cut:].strip()
        buf.append(para)
    flush()
    return out


def _digest(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def build(verbose: bool = True) -> dict:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    meta_p, vec_p = INDEX_DIR / "chunks.json", INDEX_DIR / "vectors.npy"
    old_vecs: dict[str, np.ndarray] = {}
    if meta_p.exists() and vec_p.exists():
        try:
            old_meta = json.loads(meta_p.read_text(encoding="utf-8"))
            old = np.load(vec_p)
            if len(old_meta["chunks"]) == len(old):
                old_vecs = {c["hash"]: old[i] for i, c in enumerate(old_meta["chunks"])}
        except Exception:
            old_vecs = {}

    chunks: list[dict] = []
    for corpus, root in (("wiki", WIKI), ("scenes", SCENES)):
        for p in _files(root):
            text = _read(p)
            title = p.stem
            m = re.search(r"(?m)^#\s+(.+)$", text)
            if m:
                title = m.group(1).strip()
            rel = p.relative_to(ROOT).as_posix()
            for heading, body in chunk(text, title):
                passage = f"{title} — {heading}\n{body}" if heading != title else f"{title}\n{body}"
                chunks.append({"corpus": corpus, "path": rel, "title": title,
                               "heading": heading, "text": body, "hash": _digest(passage),
                               "_passage": passage})

    todo = [c for c in chunks if c["hash"] not in old_vecs]
    t0 = time.time()
    if todo:
        emb = _embedder()
        new = list(emb.embed([c["_passage"] for c in todo], batch_size=64))
        for c, v in zip(todo, new):
            old_vecs[c["hash"]] = np.asarray(v, dtype=np.float32)
    vecs = np.stack([old_vecs[c["hash"]] for c in chunks]) if chunks else np.zeros((0, 384), np.float32)
    vecs /= np.maximum(np.linalg.norm(vecs, axis=1, keepdims=True), 1e-9)
    for c in chunks:
        c.pop("_passage")
    tmp_v, tmp_m = vec_p.with_suffix(".tmp.npy"), meta_p.with_suffix(".tmp.json")
    np.save(tmp_v, vecs)
    tmp_m.write_text(json.dumps({"model": MODEL, "built": time.strftime("%Y-%m-%d %H:%M:%S"),
                                  "chunks": chunks}, ensure_ascii=False), encoding="utf-8")
    tmp_m.replace(meta_p)
    tmp_v.replace(vec_p)  # last: its mtime is the stamp readers watch
    global _loaded
    _loaded = None
    stats = {"files": len({c["path"] for c in chunks}), "chunks": len(chunks),
             "embedded": len(todo), "seconds": round(time.time() - t0, 1)}
    if verbose:
        print(f"index: {stats['files']} files, {stats['chunks']} chunks, "
              f"{stats['embedded']} newly embedded in {stats['seconds']}s -> {INDEX_DIR}")
    return stats


def available() -> bool:
    return (INDEX_DIR / "chunks.json").exists() and (INDEX_DIR / "vectors.npy").exists()


def _load() -> dict:
    # a long-lived process (the MCP, the bot) picks up an index the sync rebuilt
    global _loaded
    stamp = (INDEX_DIR / "vectors.npy").stat().st_mtime_ns
    with _lock:
        if _loaded is None or _loaded["stamp"] != stamp:
            meta = json.loads((INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
            vecs = np.load(INDEX_DIR / "vectors.npy")
            if len(meta["chunks"]) != len(vecs):
                raise RuntimeError("index is mid-rebuild; try again")
            _loaded = {"chunks": meta["chunks"], "vecs": vecs, "stamp": stamp}
        return _loaded


def search(query: str, corpus: str, limit: int = 5, per_file: int = 2) -> list[dict]:
    """Best files for a query in one corpus ('wiki' | 'scenes'). Each hit:
    {path, title, score, chunks: [(heading, text, score), ...]} — chunks are the
    passages that matched, best first, so the caller can show them as snippets."""
    if not available():
        return []
    try:
        ix = _load()
    except (RuntimeError, OSError):
        return []  # rebuild in flight: caller falls back to the keyword ranker
    q = np.asarray(next(iter(_embedder().embed([query]))), dtype=np.float32)
    q /= max(float(np.linalg.norm(q)), 1e-9)
    sims = ix["vecs"] @ q
    by_file: dict[str, dict] = {}
    for i in np.argsort(-sims):
        c = ix["chunks"][i]
        if c["corpus"] != corpus:
            continue
        h = by_file.setdefault(c["path"], {"path": c["path"], "title": c["title"],
                                            "score": float(sims[i]), "chunks": []})
        if len(h["chunks"]) < per_file:
            h["chunks"].append((c["heading"], c["text"], float(sims[i])))
        if len(by_file) > limit * 4 and all(len(h["chunks"]) >= per_file for h in by_file.values()):
            break
    hits = sorted(by_file.values(), key=lambda h: -h["score"])
    return hits[:limit]


if __name__ == "__main__":
    build(verbose="-q" not in sys.argv)
