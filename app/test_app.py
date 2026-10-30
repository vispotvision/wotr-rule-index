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
