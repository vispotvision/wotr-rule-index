#!/usr/bin/env python3
"""WOTR Workshop: each player's own library (characters, techniques, items, lore, places,
factions) with images, and Natalie on the player's own AI, wired to the WOTR MCP's read tools.

  build/py.sh app/server.py                    # http://127.0.0.1:8780
  build/py.sh app/server.py invite [note]      # print a new invite code
  WOTR_APP_DEV=1 build/py.sh app/server.py     # adds /auth/dev for local testing (never behind Funnel)

Sign-in is Discord OAuth (DISCORD_CLIENT_ID / DISCORD_CLIENT_SECRET / WOTR_APP_URL in
~/.config/wotr/env); a new account needs an invite code. Data lives in WOTR_APP_DATA
(default ~/.local/share/wotr-app): app.db and images/. The AI key never reaches this server:
the browser calls the provider and comes here only for the tools (POST /api/tool/<name>).
"""
import asyncio
import json
import os
import re
import secrets
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

APP = Path(__file__).resolve().parent
ROOT = APP.parent
sys.path.insert(0, str(ROOT / "build"))

import httpx  # noqa: E402
from starlette.applications import Starlette  # noqa: E402
from starlette.requests import Request  # noqa: E402
from starlette.responses import FileResponse, JSONResponse, RedirectResponse, Response  # noqa: E402
from starlette.routing import Mount, Route  # noqa: E402
from starlette.staticfiles import StaticFiles  # noqa: E402

from common import load_env  # noqa: E402

load_env()
ENV = os.environ
DATA = Path(ENV.get("WOTR_APP_DATA", Path.home() / ".local/share/wotr-app")).expanduser()
IMAGES = DATA / "images"
DEV = ENV.get("WOTR_APP_DEV", "") == "1"
KINDS = ("character", "technique", "item", "lore", "place", "faction")
COOKIE = "wotr_session"
SESSION_DAYS = 30
MAX_IMAGE = 8 * 1024 * 1024
MAX_ENTRY = 400_000  # bytes of JSON per entry


# ---------- storage ----------

def db() -> sqlite3.Connection:
    DATA.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DATA / "app.db")
    con.row_factory = sqlite3.Row
    con.executescript("""
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, discord_id TEXT UNIQUE, name TEXT, avatar TEXT, created TEXT);
    CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id INTEGER, expires REAL);
    CREATE TABLE IF NOT EXISTS invites(code TEXT PRIMARY KEY, note TEXT, used_by INTEGER, created TEXT);
    CREATE TABLE IF NOT EXISTS entries(id TEXT PRIMARY KEY, owner INTEGER, kind TEXT, title TEXT, data TEXT,
        portrait TEXT, created TEXT, updated TEXT);
    CREATE TABLE IF NOT EXISTS images(id TEXT PRIMARY KEY, owner INTEGER, entry_id TEXT, ext TEXT, created TEXT);
    """)
    return con


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_invite(note: str = "") -> str:
    code = "-".join(secrets.token_hex(2).upper() for _ in range(3))
    with db() as con:
        con.execute("INSERT INTO invites(code, note, created) VALUES(?,?,?)", (code, note, now()))
    return code


# ---------- canon lists, read from the repo so they never drift ----------

MAGIC = ROOT / "wiki" / "The Magic System"
CULTURES = ["Kharven", "Accord", "Dawi", "Moto", "Eresse", "Expanse", "Korvaeth", "Stannvaard",
            "Nalūn", "Ketsuen", "Zettari", "Yukari"]  # NATALIE.md, Standing Inventories
ITEM_TIERS = ["Plain", "Marked", "Proofed", "Tempered", "Instrument", "Hallowed", "Storied", "Found",
              "Numinous", "Proscribed"]  # Fracture of Worlds, the item ladder


def canon() -> dict:
    stages = []
    f = MAGIC / "Fracture of Worlds — The Living System" / "VI. The Sixteen Temperance Stages (Part Sixteen).md"
    for m in re.finditer(r"^### Stage ([IVX]+) — (\S+) \(Tier (\d+) · (\w+)\)", f.read_text(encoding="utf-8"), re.M):
        stages.append({"numeral": m[1], "name": m[2], "tier": int(m[3]), "standing": m[4]})
    families = []
    for f in sorted((MAGIC / "The Foundations" / "The Eight Families & the Sixty Wellsprings").glob("* — *.md")):
        fam, domain = f.stem.split(" — ", 1)
        springs = [{"name": m[1].strip(), "gloss": m[2].strip()}
                   for m in re.finditer(r"^## (.+?) · \*(.+?)\*", f.read_text(encoding="utf-8"), re.M)]
        families.append({"name": fam, "domain": domain, "wellsprings": springs})
    tpl = (ROOT / "desktop" / "templates" / "CHARACTER_CARD_TEMPLATE.md").read_text(encoding="utf-8")

    def options(label: str) -> list[str]:
        line = re.search(r"^\*\*" + re.escape(label) + r"\*\* · <(.+?)>", tpl, re.M)[1]
        return [o.strip() for o in re.split(r" · | \| ", line)]
    return {
        "stages": stages, "families": families, "cultures": CULTURES, "item_tiers": ITEM_TIERS,
        "paths": ["Body", "Spirit", "Attraction", "Fate"],
        "aether_classes": options("Aether Class"), "crystal_tiers": options("Soul Crystal Tier"),
        "essence": options("Essence Typology"),
        "combat_grammar": ["Verdict", "Blade", "Percussion", "Expenditure"],
        "trait_kinds": ["Primary Trait", "Secondary Trait", "Inherited Trait", "Passive Trait", "Compound Trait",
                        "Higher-Imprint Trait"],
        "technique_kinds": ["Signature Technique", "School Art", "Bloodline Faculty", "Synergia", "Combined Art",
                            "First Release", "Second Release", "Third Release", "Domain"],
        "kinds": list(KINDS),
    }


# ---------- the WOTR MCP's read tools, in process ----------

_mcp = None


def mcp():
    """The MCP server object narrowed to the friends' surface: the read-only core plus skills."""
    global _mcp
    if _mcp is None:
        import mcp_server as M
        M.restrict_to_core()
        M.restrict_to_read_only()
        M.SKILL_HIDE.update(M.OPS_SKILLS)
        _mcp = M
    return _mcp


# ---------- auth ----------

def current_user(request: Request):
    token = request.cookies.get(COOKIE)
    if not token:
        return None
    with db() as con:
        row = con.execute("SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token=? AND s.expires>?",
                          (token, time.time())).fetchone()
    return dict(row) if row else None


def start_session(user_id: int, request: Request, to: str = "/") -> Response:
    token = secrets.token_urlsafe(32)
    with db() as con:
        con.execute("INSERT INTO sessions VALUES(?,?,?)", (token, user_id, time.time() + SESSION_DAYS * 86400))
    resp = RedirectResponse(to, status_code=303)
    resp.set_cookie(COOKIE, token, max_age=SESSION_DAYS * 86400, httponly=True, samesite="lax",
                    secure=request.url.scheme == "https" or ENV.get("WOTR_APP_URL", "").startswith("https"))
    return resp


def base_url(request: Request) -> str:
    return ENV.get("WOTR_APP_URL", "").rstrip("/") or str(request.base_url).rstrip("/")


def upsert_user(discord_id: str, name: str, avatar: str, invite: str | None):
    """The user's id, or None when a new account has no valid invite."""
    with db() as con:
        row = con.execute("SELECT id FROM users WHERE discord_id=?", (discord_id,)).fetchone()
        if row:
            con.execute("UPDATE users SET name=?, avatar=? WHERE id=?", (name, avatar, row["id"]))
            return row["id"]
        inv = con.execute("SELECT code FROM invites WHERE code=? AND used_by IS NULL", ((invite or "").strip().upper(),)).fetchone()
        if not inv:
            return None
        uid = con.execute("INSERT INTO users(discord_id, name, avatar, created) VALUES(?,?,?,?)",
                          (discord_id, name, avatar, now())).lastrowid
        con.execute("UPDATE invites SET used_by=? WHERE code=?", (uid, inv["code"]))
        return uid


async def auth_discord(request: Request):
    cid = ENV.get("DISCORD_CLIENT_ID")
    if not cid:
        return JSONResponse({"error": "Discord sign-in is not configured"}, status_code=503)
    state = secrets.token_urlsafe(16)
    q = urlencode({"client_id": cid, "redirect_uri": base_url(request) + "/auth/discord/callback",
                   "response_type": "code", "scope": "identify", "state": state, "prompt": "none"})
    resp = RedirectResponse("https://discord.com/oauth2/authorize?" + q)
    resp.set_cookie("wotr_oauth", json.dumps({"state": state, "invite": request.query_params.get("invite", "")}),
                    max_age=600, httponly=True, samesite="lax")
    return resp


async def auth_discord_callback(request: Request):
    try:
        saved = json.loads(request.cookies.get("wotr_oauth", "{}"))
    except ValueError:
        saved = {}
    if not saved.get("state") or not secrets.compare_digest(saved["state"], request.query_params.get("state", "")):
        return RedirectResponse("/#/signin?error=state", status_code=303)
    async with httpx.AsyncClient(timeout=15) as http:
        tok = await http.post("https://discord.com/api/oauth2/token", data={
            "client_id": ENV["DISCORD_CLIENT_ID"], "client_secret": ENV.get("DISCORD_CLIENT_SECRET", ""),
            "grant_type": "authorization_code", "code": request.query_params.get("code", ""),
            "redirect_uri": base_url(request) + "/auth/discord/callback"})
        if tok.status_code != 200:
            return RedirectResponse("/#/signin?error=discord", status_code=303)
        me = (await http.get("https://discord.com/api/users/@me",
                             headers={"Authorization": "Bearer " + tok.json()["access_token"]})).json()
    avatar = f"https://cdn.discordapp.com/avatars/{me['id']}/{me['avatar']}.png" if me.get("avatar") else ""
    uid = upsert_user(me["id"], me.get("global_name") or me["username"], avatar, saved.get("invite"))
    if uid is None:
        return RedirectResponse("/#/signin?error=invite", status_code=303)
    resp = start_session(uid, request)
    resp.delete_cookie("wotr_oauth")
    return resp


async def auth_dev(request: Request):
    if not DEV or request.client.host not in ("127.0.0.1", "::1"):
        return Response("not found", status_code=404)
    name = request.query_params.get("name", "Dev")[:40]
    with db() as con:
        row = con.execute("SELECT id FROM users WHERE discord_id=?", ("dev:" + name,)).fetchone()
        uid = row["id"] if row else con.execute("INSERT INTO users(discord_id, name, avatar, created) VALUES(?,?,?,?)",
                                                ("dev:" + name, name, "", now())).lastrowid
    return start_session(uid, request)


async def auth_logout(request: Request):
    with db() as con:
        con.execute("DELETE FROM sessions WHERE token=?", (request.cookies.get(COOKIE, ""),))
    resp = RedirectResponse("/#/signin", status_code=303)
    resp.delete_cookie(COOKIE)
    return resp


# ---------- the API ----------

def api(fn):
    """Signed-in JSON endpoint. Writes need the X-WOTR header, which a cross-site form cannot send."""
    async def wrapped(request: Request):
        user = current_user(request)
        if not user:
            return JSONResponse({"error": "sign in"}, status_code=401)
        if request.method != "GET" and request.headers.get("x-wotr") != "1":
            return JSONResponse({"error": "missing X-WOTR header"}, status_code=403)
        try:
            return await fn(request, user)
        except LookupError:
            return JSONResponse({"error": "not found"}, status_code=404)
        except ValueError as e:
            return JSONResponse({"error": str(e)}, status_code=400)
    return wrapped


def own_entry(con, user, eid: str):
    row = con.execute("SELECT * FROM entries WHERE id=? AND owner=?", (eid, user["id"])).fetchone()
    if not row:
        raise LookupError(eid)
    return row


def entry_out(row) -> dict:
    d = dict(row)
    d["data"] = json.loads(d["data"] or "{}")
    d.pop("owner", None)
    return d


@api
async def me(request, user):
    return JSONResponse({"name": user["name"], "avatar": user["avatar"], "discord": bool(ENV.get("DISCORD_CLIENT_ID"))})


async def status(request: Request):
    return JSONResponse({"discord": bool(ENV.get("DISCORD_CLIENT_ID")), "dev": DEV})


async def canon_route(request: Request):
    return JSONResponse(canon())


@api
async def entries(request, user):
    with db() as con:
        if request.method == "GET":
            rows = con.execute("SELECT id, kind, title, portrait, updated, json_extract(data,'$.epithet') AS epithet, "
                               "json_extract(data,'$.aura') AS aura, json_extract(data,'$.culture') AS culture, "
                               "json_extract(data,'$.kindOf') AS kindOf FROM entries WHERE owner=? ORDER BY updated DESC",
                               (user["id"],)).fetchall()
            return JSONResponse([dict(r) for r in rows])
        body = await request.json()
        kind = body.get("kind")
        if kind not in KINDS:
            raise ValueError("kind must be one of " + ", ".join(KINDS))
        eid = secrets.token_urlsafe(9)
        data = json.dumps(body.get("data") or {}, ensure_ascii=False)
        con.execute("INSERT INTO entries VALUES(?,?,?,?,?,?,?,?)",
                    (eid, user["id"], kind, str(body.get("title") or "")[:200], data, None, now(), now()))
        return JSONResponse(entry_out(own_entry(con, user, eid)), status_code=201)


@api
async def entry(request, user):
    eid = request.path_params["eid"]
    with db() as con:
        row = own_entry(con, user, eid)
        if request.method == "GET":
            return JSONResponse(entry_out(row))
        if request.method == "DELETE":
            for img in con.execute("SELECT id, ext FROM images WHERE entry_id=? AND owner=?", (eid, user["id"])):
                (IMAGES / f"{img['id']}.{img['ext']}").unlink(missing_ok=True)
            con.execute("DELETE FROM images WHERE entry_id=? AND owner=?", (eid, user["id"]))
            con.execute("DELETE FROM entries WHERE id=?", (eid,))
            return JSONResponse({"deleted": eid})
        body = await request.json()
        data = json.dumps(body.get("data") or {}, ensure_ascii=False)
        if len(data.encode()) > MAX_ENTRY:
            raise ValueError("entry too large")
        portrait = body.get("portrait", row["portrait"])
        if portrait and not con.execute("SELECT 1 FROM images WHERE id=? AND owner=?", (portrait, user["id"])).fetchone():
            raise ValueError("portrait must be one of your images")
        con.execute("UPDATE entries SET title=?, data=?, portrait=?, updated=? WHERE id=?",
                    (str(body.get("title", row["title"]) or "")[:200], data, portrait, now(), eid))
        return JSONResponse(entry_out(own_entry(con, user, eid)))


@api
async def entry_images(request, user):
    eid = request.path_params["eid"]
    with db() as con:
        own_entry(con, user, eid)
        if request.method == "GET":
            rows = con.execute("SELECT id, ext, created FROM images WHERE entry_id=? AND owner=? ORDER BY created",
                               (eid, user["id"])).fetchall()
            return JSONResponse([dict(r) for r in rows])
    form = await request.form(max_files=1, max_fields=2)
    up = form.get("file")
    if up is None:
        raise ValueError("no file")
    raw = await up.read(MAX_IMAGE + 1)
    if len(raw) > MAX_IMAGE:
        raise ValueError("image over 8 MB")
    from io import BytesIO
    from PIL import Image
    try:
        im = Image.open(BytesIO(raw))
        im.verify()
    except Exception:
        raise ValueError("not an image")
    ext = {"PNG": "png", "JPEG": "jpg", "WEBP": "webp", "GIF": "gif"}.get(im.format)
    if not ext:
        raise ValueError("png, jpg, webp or gif only")
    iid = secrets.token_urlsafe(12)
    IMAGES.mkdir(parents=True, exist_ok=True)
    (IMAGES / f"{iid}.{ext}").write_bytes(raw)
    with db() as con:
        con.execute("INSERT INTO images VALUES(?,?,?,?,?)", (iid, user["id"], eid, ext, now()))
        if not con.execute("SELECT portrait FROM entries WHERE id=?", (eid,)).fetchone()["portrait"]:
            con.execute("UPDATE entries SET portrait=? WHERE id=?", (iid, eid))
    return JSONResponse({"id": iid, "ext": ext}, status_code=201)


@api
async def image(request, user):
    iid = request.path_params["iid"]
    with db() as con:
        row = con.execute("SELECT * FROM images WHERE id=? AND owner=?", (iid, user["id"])).fetchone()
        if not row:
            raise LookupError(iid)
        if request.method == "DELETE":
            (IMAGES / f"{iid}.{row['ext']}").unlink(missing_ok=True)
            con.execute("DELETE FROM images WHERE id=?", (iid,))
            con.execute("UPDATE entries SET portrait=NULL WHERE portrait=?", (iid,))
            return JSONResponse({"deleted": iid})
    return FileResponse(IMAGES / f"{iid}.{row['ext']}", headers={"Cache-Control": "private, max-age=86400"})


@api
async def tools(request, user):
    listed = await mcp().server.list_tools()
    return JSONResponse([{"name": t.name, "description": t.description or "", "input_schema": t.input_schema}
                         for t in listed])


@api
async def tool(request, user):
    name = request.path_params["name"]
    args = await request.json()
    if not isinstance(args, dict):
        raise ValueError("arguments must be an object")
    try:
        res = await asyncio.wait_for(mcp().server.call_tool(name, args), timeout=120)
    except asyncio.TimeoutError:
        return JSONResponse({"text": f"{name} timed out after two minutes", "error": True})
    except Exception as e:  # unknown tool or bad arguments: the model reads the message and retries
        return JSONResponse({"text": f"{name} failed: {e}", "error": True})
    text = "\n".join(getattr(c, "text", "") for c in getattr(res, "content", []) if getattr(c, "text", None))
    return JSONResponse({"text": text, "error": bool(getattr(res, "is_error", False))})


async def index(request: Request):
    return FileResponse(APP / "static" / "index.html", headers={"Cache-Control": "no-cache"})


routes = [
    Route("/", index),
    Route("/auth/discord", auth_discord),
    Route("/auth/discord/callback", auth_discord_callback),
    Route("/auth/dev", auth_dev),
    Route("/auth/logout", auth_logout, methods=["POST", "GET"]),
    Route("/api/me", me),
    Route("/api/status", status),
    Route("/api/canon", canon_route),
    Route("/api/entries", entries, methods=["GET", "POST"]),
    Route("/api/entries/{eid}", entry, methods=["GET", "PUT", "DELETE"]),
    Route("/api/entries/{eid}/images", entry_images, methods=["GET", "POST"]),
    Route("/api/images/{iid}", image, methods=["GET", "DELETE"]),
    Route("/api/tools", tools),
    Route("/api/tool/{name}", tool, methods=["POST"]),
    Mount("/static", StaticFiles(directory=APP / "static")),
]
app = Starlette(routes=routes)


def main() -> int:
    if sys.argv[1:2] == ["invite"]:
        print(new_invite(" ".join(sys.argv[2:])))
        return 0
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8780)
    args = ap.parse_args()
    global DEV
    if DEV and ENV.get("WOTR_APP_URL", "").startswith("https"):
        # Funnel traffic arrives from 127.0.0.1 too, so a published server never offers /auth/dev
        print("WOTR_APP_DEV ignored: WOTR_APP_URL is a public https address", file=sys.stderr)
        DEV = False
    db().close()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
