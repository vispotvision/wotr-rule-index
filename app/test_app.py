"""The Workshop's trust boundaries: sign-in required, write header required, each user sees only
their own entries and images, uploads must be real images, dev sign-in only when enabled.
Run: build/py.sh app/test_app.py"""
import io
import os
import sys
import tempfile
from pathlib import Path

os.environ["WOTR_APP_DATA"] = tempfile.mkdtemp()
os.environ["WOTR_APP_DEV"] = "1"
sys.path.insert(0, str(Path(__file__).parent))
import server as S  # noqa: E402
from starlette.testclient import TestClient  # noqa: E402

W = {"X-WOTR": "1"}


def client(name):
    c = TestClient(S.app, base_url="http://127.0.0.1", client=("127.0.0.1", 5000))
    assert c.get(f"/auth/dev?name={name}", follow_redirects=False).status_code == 303
    return c


anon = TestClient(S.app, client=("127.0.0.1", 5000))
assert anon.get("/api/entries").status_code == 401
assert anon.get("/api/canon").json()["stages"][0]["name"] == "Murmuring"

a, b = client("A"), client("B")
assert a.post("/api/entries", json={"kind": "character"}).status_code == 403          # no X-WOTR header
assert a.post("/api/entries", json={"kind": "spell"}, headers=W).status_code == 400   # unknown kind
e = a.post("/api/entries", json={"kind": "character", "title": "Naiser", "data": {"aura": "#e8b04b"}}, headers=W).json()
assert a.put(f"/api/entries/{e['id']}", json={"title": "Naiser", "data": {"stage": "IV"}}, headers=W).json()["data"] == {"stage": "IV"}
assert b.get(f"/api/entries/{e['id']}").status_code == 404                            # not B's
assert b.put(f"/api/entries/{e['id']}", json={"data": {}}, headers=W).status_code == 404
assert b.get("/api/entries").json() == []

png = io.BytesIO()
from PIL import Image  # noqa: E402
Image.new("RGB", (8, 8), "red").save(png, "PNG")
up = a.post(f"/api/entries/{e['id']}/images", files={"file": ("x.png", png.getvalue(), "image/png")}, headers=W)
assert up.status_code == 201, up.text
iid = up.json()["id"]
assert a.get(f"/api/entries/{e['id']}").json()["portrait"] == iid
assert a.get(f"/api/images/{iid}").status_code == 200 and b.get(f"/api/images/{iid}").status_code == 404
bad = a.post(f"/api/entries/{e['id']}/images", files={"file": ("x.png", b"<script>", "image/png")}, headers=W)
assert bad.status_code == 400
f = b.post("/api/entries", json={"kind": "item"}, headers=W).json()
assert b.put(f"/api/entries/{f['id']}", json={"data": {}, "portrait": iid}, headers=W).status_code == 400  # A's image

assert a.post("/api/tool/skill", json={"name": "wotr-name"}, headers=W).json()["text"].startswith(S.mcp().SKILL_NOTE)
assert a.post("/api/tool/archive_scene", json={}, headers=W).json()["error"]          # writers are not exposed
assert a.delete(f"/api/entries/{e['id']}", headers=W).status_code == 200
assert not list(S.IMAGES.glob(f"{iid}.*"))

S.DEV = False
assert anon.get("/auth/dev?name=X").status_code == 404
print("ok")

# key sign-in: an invite becomes the holder's key; the same key signs back in; junk is refused
k = S.new_invite("test")
c = TestClient(S.app, client=("127.0.0.1", 5000))
assert c.post("/auth/key", json={"key": k}, headers=W).json().get("need_name")
assert c.post("/auth/key", json={"key": k, "name": "Kei"}, headers=W).status_code == 200
assert c.get("/api/me").json()["name"] == "Kei"
c2 = TestClient(S.app, client=("127.0.0.1", 5000))
assert c2.post("/auth/key", json={"key": k.lower()}, headers=W).status_code == 200 and c2.get("/api/me").json()["name"] == "Kei"
assert c2.post("/auth/key", json={"key": "0000-0000-0000-0000"}, headers=W).status_code == 401
assert c2.post("/auth/key", json={"key": k}).status_code == 403
print("ok keys")

# sharing: a link shows the entry and only its images to anyone; a copy lands in the viewer's own
# library with its own images; turning sharing off kills the link
S.DEV = True
a = client("SharerA")
e = a.post("/api/entries", json={"kind": "character", "title": "Ka<b>ito", "data": {"epithet": "the Ember"}}, headers=W).json()
png = io.BytesIO(); Image.new("RGB", (8, 8), "blue").save(png, "PNG")
iid = a.post(f"/api/entries/{e['id']}/images", files={"file": ("x.png", png.getvalue(), "image/png")}, headers=W).json()["id"]
other = a.post("/api/entries", json={"kind": "lore", "title": "secret"}, headers=W).json()
png2 = io.BytesIO(); Image.new("RGB", (8, 8), "green").save(png2, "PNG")
secret_img = a.post(f"/api/entries/{other['id']}/images", files={"file": ("y.png", png2.getvalue(), "image/png")}, headers=W).json()["id"]
assert anon.get("/api/shared/nope").status_code == 404
tok = a.put(f"/api/entries/{e['id']}/share", json={"on": True}, headers=W).json()["share"]
assert a.put(f"/api/entries/{e['id']}/share", json={"on": True}, headers=W).json()["share"] == tok   # stable
assert b.put(f"/api/entries/{e['id']}/share", json={"on": True}, headers=W).status_code == 404      # not B's
pub = anon.get(f"/api/shared/{tok}").json()
assert pub["title"] == "Ka<b>ito" and pub["owner"] == "SharerA" and pub["images"] == [iid] and "owner" not in pub["data"]
assert anon.get(f"/s/{tok}/img/{iid}").status_code == 200
assert anon.get(f"/s/{tok}/img/{secret_img}").status_code == 404                                   # not this entry's
page = anon.get(f"/s/{tok}").text
assert 'og:title" content="Ka&lt;b&gt;ito · WOTR Workshop"' in page and "og:image" in page and "<b>ito" not in page
assert anon.post(f"/api/shared/{tok}/copy", headers=W).status_code == 401
cid = b.post(f"/api/shared/{tok}/copy", headers=W).json()["id"]
mine = b.get(f"/api/entries/{cid}").json()
assert mine["title"] == "Ka<b>ito" and mine["portrait"] and mine["portrait"] != iid and mine["share"] is None
assert b.get(f"/api/images/{mine['portrait']}").status_code == 200
assert a.put(f"/api/entries/{e['id']}/share", json={"on": False}, headers=W).json()["share"] is None
assert anon.get(f"/api/shared/{tok}").status_code == 404 and anon.get(f"/s/{tok}/img/{iid}").status_code == 404
assert anon.get(f"/s/{tok}").status_code == 404
print("ok sharing")
