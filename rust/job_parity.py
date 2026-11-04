#!/usr/bin/env python3
"""The tools that start other programs, Rust against Python, in writer_parity.py's two scratch clones:
cast_index, convert_character, cast_scene, narrate_scene, narration_status, research, ask_chatgpt,
ask_claude, research_chatgpt and chatgpt_image.

  bash build/py.sh rust/job_parity.py [scratch-dir]     # exit 1 on any difference

Nothing real runs: each clone's build/audio_export.py and build/ask_*.sh are stubs (the Rust render is
`wotr-mcp audio`, so its side gets the same stub render through WOTR_AUDIO_BIN, started as `<bin>
audio --scene ...`; rust/audio_parity.py checks the real render), and agent-reach,
agent-browser and curl are stubs first on PATH, answering from one canned table (the Python side's
urllib is pointed at the same table). HOME is a scratch folder per side, the env file an empty one.
Compared: every reply (an image reply as its blocks), the jobs file and logs, scenes/cast, CAST.md,
ARCS.md, the inbox and the saved images, with stamps and the two sides' paths normalized.
"""
import base64
import difflib
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import writer_parity as W  # noqa: E402  (reads the scratch dir from argv)

PY = sys.executable
UA = "Mozilla/5.0 (X11; Linux x86_64) WOTR-research"
API = "https://powerlisting.fandom.com/api.php?"

DRIVER = r'''
import io, json, os, sys, threading, urllib.error, urllib.request
out = os.fdopen(os.dup(1), "w", encoding="utf-8", buffering=1)
sys.stdout = sys.stderr
sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.join(os.getcwd(), "build"))
import mcp_server as M
FAKE = json.load(open(os.environ["STUB_DATA"], encoding="utf-8"))["http"]

def urlopen(req, timeout=None):
    r = FAKE.get(req.full_url)
    if req.get_header("User-agent") != %r or r is None:
        raise urllib.error.URLError(ConnectionRefusedError(111, "Connection refused"))
    if r.get("error") == "timeout":
        raise TimeoutError("timed out")
    if r["status"] >= 400:
        raise urllib.error.HTTPError(req.full_url, r["status"], r["reason"], {}, io.BytesIO(b""))
    return io.BytesIO(r["body"].encode("utf-8"))
urllib.request.urlopen = urlopen

tools = M.server._tool_manager._tools
for line in sys.stdin:
    req = json.loads(line)
    saved = dict(os.environ)
    os.environ.update(req.get("env") or {})
    pub = req.get("public") or {}
    M.PUBLIC["base"], M.PUBLIC["token"] = pub.get("base", ""), pub.get("token", "")
    try:
        res = tools[req["tool"]].fn(**req["args"])
        for t in threading.enumerate():
            if t is not threading.main_thread():
                t.join()
        if isinstance(res, list):
            res = [{"type": "text", "text": x} if isinstance(x, str) else
                   {k: v for k, v in x.to_image_content().model_dump(by_alias=True).items() if k in ("type", "data", "mimeType")} for x in res]
            res = json.dumps(res)
        resp = res
    except Exception as e:
        resp = f"<<error>> {type(e).__name__}: {e}"
    os.environ.clear()
    os.environ.update(saved)
    out.write(json.dumps({"r": resp}) + "\n")
''' % UA

REACH = r'''#!PY
import json, os, sys, time
d = json.load(open(os.environ["STUB_DATA"], encoding="utf-8"))["reach"].get(" | ".join(sys.argv[1:]))
if d is None:
    print(json.dumps({"ok": False, "error": {"code": "NO_STUB", "message": " | ".join(sys.argv[1:])}}))
    sys.exit(0)
time.sleep(d.get("sleep", 0))
sys.stdout.write(d.get("stdout", ""))
sys.stderr.write(d.get("stderr", ""))
sys.exit(d.get("code", 0))
'''

BROWSER = r'''#!PY
import json, os, sys
assert sys.argv[1:3] == ["--session", "wotr-research"], sys.argv
a = sys.argv[3:]
state = os.path.join(os.environ["STUB_STATE"], "browser_url")
pages = json.load(open(os.environ["STUB_DATA"], encoding="utf-8"))["browser"]
if a[0] == "open":
    open(state, "w").write(a[1])
    sys.exit(pages.get(a[1], {}).get("open_code", 0))
if a[0] == "close":
    sys.exit(0)
p = pages.get(open(state).read(), {})
if a == ["get", "title"]:
    print(p.get("title", ""))
else:
    print(p.get("text", "") + " exe=" + os.environ.get("AGENT_BROWSER_EXECUTABLE_PATH", "-"))
    sys.exit(p.get("text_code", 0))
'''

CURL = r'''#!PY
import json, os, sys
a = sys.argv[1:]
url = a[-1]
r = json.load(open(os.environ["STUB_DATA"], encoding="utf-8"))["http"].get(url)
if a[:-1] != ["-s", "-L", "--http1.1", "--max-time", "30", "-A", %r, "-D", "/dev/stderr"] or r is None:
    sys.exit(7)
if r.get("error") == "timeout":
    sys.exit(28)
sys.stderr.write("HTTP/1.1 301 Moved\r\nLocation: x\r\n\r\nHTTP/1.1 %%d %%s\r\nContent-Type: application/json\r\n\r\n" %% (r["status"], r["reason"]))
sys.stdout.write(r["body"] if r["status"] < 400 else "")
''' % UA

AUDIO = r'''
def main():
  import os, sys, time
  print("stub render:", " ".join(sys.argv[1:]), "PYTHONIOENCODING=" + os.environ.get("PYTHONIOENCODING", "-"), flush=True)
  if "slow" in sys.argv:
    time.sleep(3)
  if "broken" in sys.argv:
    print("Traceback (most recent call last):\n  boom")
    return 1
  print("progress\r50%\rdone")
  print("audio: 1 written to the folder")
  return 0
'''

ASK = r'''#!/usr/bin/env bash
p="$1"
case "$p" in
  *IMG:*)
    g="$HOME/.codex/generated_images/s1"; mkdir -p "$g"
    case "$p" in
      *IMG:png*) cp "$FIXTURE/a.png" "$g/one.png"; echo "$g/one.png" ;;
      *IMG:jpg*) cp "$FIXTURE/a.jpg" "$g/Two.JPG"; echo "$g/Two.JPG" ;;
      *IMG:broken*) printf 'not an image' > "$g/bad.webp"; echo "$g/bad.webp" ;;
      *IMG:fail*) echo "no can do" >&2; exit 2 ;;
      *) echo "I could not make that one." ;;
    esac ;;
  *fail*) for i in $(seq 1 80); do printf 'error line %s ' "$i" >&2; done; exit 3 ;;
  *) printf '   %s answer: %s   \n\n' "WHO" "$(printf '%s' "$p" | tail -n 1)" ;;
esac
'''


def stub(path: Path, text: str) -> None:
    path.write_text(text.replace("#!PY", "#!" + PY), encoding="utf-8")
    path.chmod(0o755)


def http_table() -> dict:
    def q(params):
        from urllib.parse import urlencode
        return API + urlencode({**params, "format": "json", "formatversion": 2})

    def ok(obj):
        return {"status": 200, "reason": "OK", "body": json.dumps(obj, ensure_ascii=False)}

    search = lambda s, hits: (q({"action": "query", "list": "search", "srsearch": s, "srlimit": 5}),  # noqa: E731
                              ok({"batchcomplete": True, "query": {"search": [{"title": h, "pageid": i} for i, h in enumerate(hits)]}}))
    parse = lambda p, body: (q({"action": "parse", "page": p, "prop": "wikitext", "redirects": 1}), body)  # noqa: E731
    wikitext = ("'''Fire Manipulation''' is the power to [[Element Manipulation|manipulate]] fire.<ref>Book, p. 3</ref>\n"
                "{{Quote|{{Nested|x}}|y}}[[File:Fire.png|thumb]][[Category:Powers]]<!-- hidden -->\n\n\n\n== Uses ==\n"
                "* Heat [[Thermal Manipulation]]\n* Plasma: 6,000 K & \"ions\" é\n") + ("long line of uses. " * 600)
    t = {}
    for k, v in [
        search("Fire Manipulation", ["Fire Manipulation", "Heat Manipulation", "Fire Generation"]),
        parse("Fire Manipulation", ok({"parse": {"title": "Fire Manipulation", "pageid": 1, "wikitext": wikitext}})),
        search("fire bending", ["Pyrokinesis Mastery", "Fire Bending (Avatar)"]),
        parse("fire bending", ok({"error": {"code": "missingtitle", "info": "The page you specified doesn't exist."}})),
        parse("Pyrokinesis Mastery", ok({"parse": {"title": "Pyrokinesis Mastery", "wikitext": "Short page about [[Fire|flames]]."}})),
        search("zzz nothing", []),
        parse("zzz nothing", ok({"error": {"code": "missingtitle"}})),
        (search("down", [])[0], {"status": 503, "reason": "Service Unavailable", "body": ""}),
        search("slow api", []),
        search("no query key", []),
        search("bad json", []),
        search("a/b & c+d? é", ["A/B"]),
        parse("a/b & c+d? é", ok({"parse": {"title": "A/B & C+D? é", "wikitext": "{{x}}Slash page"}})),
    ]:
        t[k] = v
    t[search("slow api", [])[0]] = {"error": "timeout"}
    t[search("no query key", [])[0]] = ok({"batchcomplete": True})
    t[search("bad json", [])[0]] = {"status": 200, "reason": "OK", "body": "{\"query\": {\"search\": [1,]}}"}
    return t


def reach_table() -> dict:
    j = lambda o: json.dumps(o, ensure_ascii=False)  # noqa: E731
    items = [{"title": "Thermite — Wikipedia", "url": "https://en.wikipedia.org/wiki/Thermite", "text": "Thermite is a pyrotechnic\ncomposition. " * 40},
             {"title": "", "url": "https://powerlisting.fandom.com/wiki/Fire", "text": "fandom page"},
             {"url": "https://blocked.example/page", "text": None},
             {"title": "No URL here", "text": "x"},
             {"title": "Fourth", "url": "https://fourth.example/", "text": "  spaced  "}]
    big = "Aluminium reduces iron oxide. " * 400
    return {
        "web | search | thermite | --limit | 6": {"stdout": j({"ok": True, "items": items})},
        "read | https://en.wikipedia.org/wiki/Thermite": {"stdout": "warning: cache\n" + j({"ok": True, "items": [{"title": "Thermite", "text": "  " + big + "  "}]})},
        "read | https://blocked.example/page": {"stdout": j({"ok": False, "error": {"code": "BLOCKED", "message": "403"}})},
        "read | https://fourth.example/": {"stdout": j({"ok": True, "items": []})},
        "read | https://given.example/a": {"stdout": j({"ok": True, "items": [{"text": "given page text"}]})},
        "read | https://bot.example/": {"stdout": j({"ok": False})},
        "read | https://empty.example/": {"stdout": "", "code": 2},
        "web | search | search fails | --limit | 6": {"stdout": j({"ok": False, "error": {"code": "RATE_LIMIT", "message": "slow down " * 40}})},
        "web | search | stderr junk | --limit | 6": {"stdout": j({"ok": True, "items": []}), "stderr": "a warning on stderr\n"},
        "web | search | no json | --limit | 6": {"stdout": "plain text only " * 30, "code": 1},
        "web | search | error not dict | --limit | 6": {"stdout": j({"ok": False, "error": "flat"})},
        "web | search | slow | --limit | 6": {"stdout": "{}", "sleep": 95},
        **{f"web | search | bad{i} | --limit | 6": {"stdout": s} for i, s in enumerate([
            '{"ok": true, "items": [1,]}', '{"ok": "x\ty"}', '{"ok": "\\q"}', '{"ok" true}', '{"ok": tru}', '{"ok": true,}',
            '{"ok": "\\u12"}', '{ "ok": [\n1 2]}', '{"ok": "unterminated', '{"ok": "\\ud83d\\ude00", "items": [{"title": "\\u00e9", "url": "u"}]}',
            '{"ok": true} {"second": 1}', '{', '{"ok": 1e400, "n": -0, "f": 1.5E+3}', '{"a":\n\n\n  ]'])},
    }


def browser_table() -> dict:
    return {"https://blocked.example/page": {"title": "  A Blocked Page  ", "text": "browser text " * 900},
            "https://bot.example/": {"title": "Just a moment...", "text": "cf"},
            "https://empty.example/": {"title": "Empty", "text": "", "text_code": 1},
            "https://fourth.example/": {"open_code": 1}}


def setup(a: Path, b: Path) -> dict:
    stubs = W.S / "stubs"
    stubs.mkdir()
    stub(stubs / "agent-reach", REACH)
    stub(stubs / "agent-browser", BROWSER)
    stub(stubs / "curl", CURL)
    # the Rust render is `wotr-mcp audio ARGS`: the same stub, the subcommand dropped, so the logs compare
    stub(W.S / "audio-render", "#!PY\nimport sys\nsys.argv = sys.argv[:1] + sys.argv[2:]\n" + AUDIO + "\nsys.exit(main())\n")
    fixture = W.S / "fixture"
    fixture.mkdir()
    subprocess.run(["magick", "-size", "300x200", "gradient:red-blue", str(fixture / "a.png")], check=True)
    subprocess.run(["magick", "-size", "1500x900", "plasma:fractal", "-seed", "7", str(fixture / "a.jpg")], check=True)
    data = {"http": http_table(), "reach": reach_table(), "browser": browser_table()}
    (W.S / "stubdata.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    (W.S / "empty.env").write_text("", encoding="utf-8")
    envs = {}
    for side, root in (("A", a), ("B", b)):
        # the real module (cast_scene parses with it) with a main() that renders nothing
        real = (W.REAL / "build/audio_export.py").read_text(encoding="utf-8")
        cut = real.rindex('if __name__ == "__main__":')
        (root / "build/audio_export.py").write_text(real[:cut] + AUDIO + '\nif __name__ == "__main__":\n    sys.exit(main())\n', encoding="utf-8")
        for who in ("chatgpt", "claude"):
            stub(root / f"build/ask_{who}.sh", ASK.replace("WHO", who))
        audio = root / "docs/audio"
        for rel, size in [("01 The Kharven year — Sodoku Moto/a scene.mp3", 720_000), ("solo é.mp3", 5_000), ("deep/x/y.wav", 2_880_000), ("z.mp3", 11_999_999), ("notes.txt", 10)]:
            (audio / rel).parent.mkdir(parents=True, exist_ok=True)
            (audio / rel).write_bytes(b"\0" * size)
        home = W.S / f"home{side}"
        old = home / ".codex/generated_images/old.png"
        old.parent.mkdir(parents=True)
        old.write_bytes((fixture / "a.png").read_bytes())
        os.utime(old, (time.time() - 3600, time.time() - 3600))
        (W.S / f"state{side}").mkdir()
        envs[side] = {**os.environ, "HOME": str(home), "PATH": f"{stubs}:{os.environ['PATH']}", "WOTR_ENV_FILE": str(W.S / "empty.env"),
                      "WOTR_PYTHON": PY, "STUB_DATA": str(W.S / "stubdata.json"), "STUB_STATE": str(W.S / f"state{side}"),
                      "FIXTURE": str(fixture), "WOTR_ROOT": str(root), "WOTR_AUDIO_BIN": str(W.S / "audio-render")}
        envs[side].pop("AGENT_BROWSER_EXECUTABLE_PATH", None)
        envs[side].pop("WOTR_DRIVE", None)
    return envs


def seed_jobs(root: Path) -> None:
    logs = root / "build"
    jobs = []
    for i in range(44):
        log = logs / f".narrate-seed{i}.log"
        if i % 4 == 1:
            log.write_text("render\nTraceback (most recent call last):\n  x\n", encoding="utf-8")
        elif i % 4 == 2:
            log.write_text("audio: 3 written\nlast line is long " + "y" * 300 + "\n\n", encoding="utf-8")
        elif i % 4 == 3:
            log.write_text("still going\r40%", encoding="utf-8")
        jobs.append({"id": f"seed-{i}", "scene": f"scene_{i}.md", "voice": "Ünï voice" if i == 43 else "narrator", "engine": "local",
                     "log": str(log), "started": "2026-01-01T00:00:00", "words": 1000 + i})
    (logs / ".narrate_jobs.json").write_text(json.dumps(jobs, indent=1), encoding="utf-8")


def calls(root: Path) -> list:
    sys.path.insert(0, str(root / "build"))
    import audio_export as A
    scenes = sorted(p for p in (root / "scenes").glob("*.md") if p.name not in ("MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md"))
    text = lambda p: A.plain_text(A.scene_blocks(p.read_text(encoding="utf-8", errors="replace")))  # noqa: E731
    sc = next(p for p in scenes if "[" not in text(p) and "\n---\n" in text(p))  # tags only where the script puts them
    plain = text(sc)
    paras = plain.split("\n\n")
    tagged = list(paras)
    for i in range(1, len(tagged)):
        if tagged[i].strip() != "---" and not tagged[i].startswith("# "):
            tagged[i] = "[Verinus: slow, beat] " + tagged[i] if i % 3 == 1 else ("[sigh] " + tagged[i] + " [narrator]" if i % 3 == 2 else ("[Gimbzo] " if i % 2 else "[Hild] ") + tagged[i])
    good = "\n\n".join(tagged)
    pub = {"base": "https://ultron.example.net", "token": "tok/en é"}
    S = lambda s: ("__sleep", {"s": s})  # noqa: E731
    return [
        ("cast_index", {"write": False}), ("cast_index", {}),
        ("convert_character", {"source": "x", "json_path": str(W.S / "bad.json")}),
        ("convert_character", {"source": "Sodoku", "json_path": str(W.S / "board.json")}),
        ("cast_scene", {"scene": sc.name, "script": good}),
        ("cast_scene", {"scene": sc.stem, "script": good.replace("\n", "\r\n") + "\n\n\n"}),
        ("cast_scene", {"scene": sc.name, "script": "[Bob: shouty] " + good}),
        ("cast_scene", {"scene": sc.name, "script": good.replace(" the ", " a ", 1)}),
        ("cast_scene", {"scene": sc.name, "script": good + "\n\n---\n\nextra"}),
        ("cast_scene", {"scene": sc.name, "script": good + "\n\n---"}),
        ("cast_scene", {"scene": scenes[0].name, "script": text(scenes[0])}),
        ("cast_scene", {"scene": "zzz-no-scene", "script": "x"}),
        ("cast_scene", {"scene": "the", "script": "x"}),
        ("narration_status", {}),
        ("narration_status", {"__public": pub}),
        ("narration_status", {"job": "seed-2"}),
        ("narrate_scene", {"scene": "zzz no scene"}),
        ("narrate_scene", {"scene": "it's"}),
        ("narrate_scene", {"scene": sc.name, "voice": "slow"}),
        S(1.2),
        ("narrate_scene", {"scene": scenes[1].name, "voice": "af_heart:0.6,bm_george:0.4", "engine": " Local "}),
        S(1.2),
        ("narrate_scene", {"scene": sc.name, "engine": "bogus"}),
        ("narrate_scene", {"scene": sc.name, "engine": "   "}),
        ("narrate_scene", {"scene": sc.name, "engine": "ElevenLabs", "__public": pub}),
        ("narrate_scene", {"scene": scenes[2].name, "voice": "broken", "engine": "elevenlabs", "__public": {"base": "", "token": ""}}),
        S(4),
        ("narration_status", {}),
        ("narration_status", {"__public": pub}),
        ("narration_status", {"job": "nope"}),
        ("research", {"question": "thermite", "urls": ["https://given.example/a", "https://en.wikipedia.org/wiki/Thermite", "https://bot.example/", "https://empty.example/"],
                      "power": "  Fire Manipulation  "}),
        ("research", {"question": "thermite", "read": 9, "power": "fire bending"}),
        ("research", {"question": "thermite", "read": -1, "power": "zzz nothing"}),
        ("research", {"question": "search fails", "power": "down"}),
        ("research", {"question": "stderr junk", "read": 0, "power": "slow api"}),
        ("research", {"question": "no json", "power": "no query key"}),
        ("research", {"question": "error not dict", "power": "bad json"}),
        ("research", {"question": "nothing stubbed", "urls": ["https://nowhere.example/"], "power": "a/b & c+d? é"}),
        ("research", {"question": "nothing stubbed", "power": "unknown power"}),
        ("research", {"question": "thermite", "__env": {"PATH": "/usr/bin:/bin"}}),
        *[("research", {"question": f"bad{i}", "read": 0}) for i in range(14)],
        ("ask_chatgpt", {"prompt": "first line\nsecond: what is thermite?"}),
        ("ask_claude", {"prompt": "one line é"}),
        ("ask_chatgpt", {"prompt": "please fail"}),
        ("ask_claude", {"prompt": "fail now"}),
        ("research_chatgpt", {"question": "How hot does thermite burn? " + "x" * 100, "thread": "parity-thread"}),
        ("research_chatgpt", {"question": "fail this one"}),
        ("chatgpt_image", {"prompt": "A forge at night IMG:png", "name": "Forge, at Night é!"}),
        S(1.5),
        ("chatgpt_image", {"prompt": "IMG:jpg a big plasma " + "word " * 30, "__public": pub}),
        S(1.5),
        ("chatgpt_image", {"prompt": "IMG:broken", "__public": pub}),
        S(1.5),
        ("chatgpt_image", {"prompt": "IMG:none"}),
        ("chatgpt_image", {"prompt": "IMG:fail"}),
        ("research", {"question": "slow", "read": 0}),
    ]


def run_python(root: Path, env: dict, cs: list) -> list:
    (W.S / "driver.py").write_text(DRIVER, encoding="utf-8")
    w = subprocess.Popen(["bash", str(root / "build/py.sh"), str(W.S / "driver.py")], cwd=root, env=env,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    out = []
    for tool, args in cs:
        if tool == "__sleep":
            time.sleep(args["s"])
            continue
        args = dict(args)
        req = {"tool": tool, "public": args.pop("__public", None), "env": args.pop("__env", None), "args": args}
        w.stdin.write(json.dumps(req) + "\n")
        w.stdin.flush()
        out.append(json.loads(w.stdout.readline())["r"])
    w.stdin.close()
    w.wait(30)
    return out


def run_rust(env: dict, cs: list) -> list:
    out = []
    for tool, args in cs:
        if tool == "__sleep":
            time.sleep(args["s"])
            continue
        args = dict(args)
        pub, extra = args.pop("__public", None), args.pop("__env", None)
        cmd = [str(W.BIN), "call", tool, "-"] + (["--public", pub["base"], pub["token"]] if pub else [])
        r = subprocess.run(cmd, input=json.dumps(args), capture_output=True, text=True, env={**env, **(extra or {})})
        text = r.stdout[:-1] if r.returncode == 0 else f"<<error>> {r.stderr.strip()}"
        if text.startswith('[{"type"'):  # the content list: keep the fields the Python side has
            text = json.dumps([{"type": "text", "text": b["text"]} if b["type"] == "text" else
                               {"type": "image", "data": b["data"], "mimeType": b["mimeType"]} for b in json.loads(text)])
        out.append(text)
    return out


def norm(t: str, side: str) -> str:
    t = t.replace(str(W.S / side), "<ROOT>").replace(str(W.S / f"home{side}"), "<HOME>")
    return W.norm(t)


def image_digest(t: str) -> str:
    """An image reply with its base64 data as a digest, so a difference prints short."""
    if not t.startswith('[{"type"'):
        return t
    blocks = json.loads(t)
    for b in blocks:
        if b["type"] == "image":
            b["data"] = hashlib.sha256(base64.b64decode(b["data"])).hexdigest()[:16] + f" ({len(b['data'])} b64 chars)"
    return json.dumps(blocks, ensure_ascii=False)


def tree(root: Path, home: Path, side: str) -> dict:
    files = {}
    for base in [root / "build/.narrate_jobs.json", *sorted((root / "build").glob(".narrate-*.log")), root / "scenes/cast", root / "scenes/CAST.md",
                 root / "scenes/ARCS.md", root / "inbox", home / "wotr-drafts", home / ".codex"]:
        for p in ([base] if base.is_file() else sorted(base.rglob("*")) if base.exists() else []):
            if p.is_file():
                data = p.read_bytes()
                key = norm(str(p.relative_to(home if p.is_relative_to(home) else root)), side)
                try:
                    files[key] = norm(data.decode("utf-8"), side)
                except UnicodeDecodeError:
                    files[key] = "sha256 " + hashlib.sha256(data).hexdigest()
    return files


def main() -> int:
    a, b = W.setup()
    envs = setup(a, b)
    (W.S / "bad.json").write_text('{"cards": [1,]}', encoding="utf-8")
    (W.S / "board.json").write_text(json.dumps({"lists": [{"id": "L1", "name": "Characters"}], "cards": [
        {"name": "Sodoku", "idList": "L1", "desc": "Level 40, Stage IV", "id": "c1", "labels": [{"name": "PC"}]}],
        "checklists": [{"idCard": "c1", "name": "Kit", "checkItems": [{"name": "sword"}, {"name": "η vial"}]}, {"idCard": "c2", "name": "Other"}]}), encoding="utf-8")
    bad = 0
    for rnd in range(2):
        for r in (a, b):
            seed_jobs(r) if rnd == 0 else (r / "build/.narrate_jobs.json").write_text("{not json", encoding="utf-8")
            if rnd:
                (r / "scenes/ARCS.md").unlink(missing_ok=True)
        cs = calls(a) if rnd == 0 else [("cast_index", {}), ("narration_status", {}), ("narrate_scene", {"scene": "the", "voice": "x"}),
                                        ("narrate_scene", {"scene": sorted((a / "scenes").glob("g*.md"))[0].name}), ("__sleep", {"s": 1.5}), ("narration_status", {"job": ""})]
        t0 = time.time()
        py = run_python(a, envs["A"], cs)
        t1 = time.time()
        rs = run_rust(envs["B"], cs)
        t2 = time.time()
        real = [c for c in cs if c[0] != "__sleep"]
        for (tool, args), p, r in zip(real, py, rs):
            p, r = image_digest(norm(p, "A")), image_digest(norm(r, "B"))
            if p != r:
                bad += 1
                print(f"=== reply differs: {tool} {json.dumps(args, ensure_ascii=False)[:150]}")
                print("".join(list(difflib.unified_diff(p.splitlines(True), r.splitlines(True), "python", "rust", n=1))[:30]))
        ta, tb = tree(a, W.S / "homeA", "A"), tree(b, W.S / "homeB", "B")
        for f in sorted(set(ta) | set(tb)):
            if ta.get(f) != tb.get(f):
                bad += 1
                print(f"=== file differs: {f}" + ("" if f in ta and f in tb else f" (only in {'rust' if f in tb else 'python'})"))
                print("".join(list(difflib.unified_diff(ta.get(f, "").splitlines(True), tb.get(f, "").splitlines(True), "python", "rust", n=1))[:30]))
        print(f"round {rnd + 1}: {len(real)} calls (python {t1 - t0:.0f} s, rust {t2 - t1:.0f} s), {len(ta)} files compared")
    print("ALL IDENTICAL" if not bad else f"{bad} difference(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
