"""verify.py under R78-3 and the 2026-10-17 directions (R79). Run: python build/test_r78_3.py"""
import sys; sys.path.insert(0, "build")
from pathlib import Path
import verify as v

assert v.FIGHT_ABSTRACT.search("The parry had cost him the line.")
assert v.FIGHT_ABSTRACT.search("He closed measure fast.")
assert not v.FIGHT_ABSTRACT.search("the line of his jaw") and not v.FIGHT_ABSTRACT.search("He ruled a line under it.")
fight = "He closed measure and took the line."
assert any(w.startswith("fight abstraction") for w in v.run(fight, combat=True)["warns"])
assert not any(w.startswith("fight abstraction") for w in v.run(fight)["warns"])  # R79-6: --combat only

# R79-3: no rhythm, count or length WARNs; R79-1: length is info only, in every band.
plain = " ".join(["He walked to the door and opened it."] * 12)
for band in v.BANDS:
    r = v.run(plain, band=band)
    assert not r["fails"] and not r["warns"], (band, r)
    assert any(i.startswith("length 96 words") for i in r["info"])

# R79-5: bare genre words are free; the exact clichés still FAIL. R79-7: 'her core' left the list.
assert not v.run("Killing intent filled the yard. His qi rose.")["warns"]
assert v.run("Killing intent surged through the yard.")["fails"]
assert not v.run("He touched her core of Essence.", explicit=True)["fails"]
assert v.run("He touched his member.", explicit=True)["fails"]
assert not v.run("The teenager ran. She counted 3 crows.")["warns"]

# The Weak Grade, Isaac's prose reference, passes clean.
ref = Path(__file__).resolve().parent.parent / "desktop/style-bank/references/the-weak-grade-isaac-reference.md"
assert not v.run(ref.read_text(encoding="utf-8"))["fails"], v.run(ref.read_text(encoding="utf-8"))["fails"]
print("ok")
