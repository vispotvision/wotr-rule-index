"""verify.py under R78-3 and the 2026-10-17 directions (R79). Run: python build/test_r78_3.py"""
import sys; sys.path.insert(0, "build")
from pathlib import Path
import verify as v

fight = "He closed measure and took the line."
# R80-22/R80-25 (Isaac 2026-11-03): the fight-abstraction watch retired; terms are welcome beside the body.
assert not any(w.startswith("fight abstraction") for w in v.run(fight, combat=True)["warns"])
assert not any(w.startswith("fight abstraction") for w in v.run(fight)["warns"])

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
# The reference is preserved verbatim (it keeps its British spellings), so the spelling FAIL is exempt here.
_fails = [f for f in v.run(ref.read_text(encoding="utf-8"))["fails"] if not f.startswith("British spelling")]
assert not _fails, _fails
# R81-9 (Isaac 2026-11-03): only exact stock phrases FAIL; single words and canon signatures are free.
assert not v.run("The tension was palpable. A tapestry of banners. Visceral fear.")["fails"]
assert not v.run("A whisper of falling ash came off his shoulders, and the air smelled of ozone.")["fails"]
assert v.run("The coppery tang of blood filled the air.")["fails"]
assert v.run("It was a testament to his skill.")["fails"]
# En dashes in ranges are free; em dashes FAIL.
assert not v.run("Stages IV–VII.")["fails"] and v.run("He came — fast.")["fails"]
# Emotion said is free; hypophora is a question answered at once, an open question is free.
assert not v.run("She was afraid, and she said so.")["warns"]
assert any("hypophora" in w for w in v.run("Why did he stop? He was tired.")["warns"])
assert not any("hypophora" in w for w in v.run("Was the drum holding every heart on one count, and if it was, what happened to a blow that landed off the beat?")["warns"])
# Thin blows (R80-5, R81-1): a strike with no tissue or body mechanics WARNs in a fight.
assert any(w.startswith("thin blow?") for w in v.run("He hit Aksel hard.", combat=True)["warns"])
assert not any(w.startswith("thin blow?") for w in v.run("His left heel drove, the hip turned, and he hit Aksel under the jaw.", combat=True)["warns"])
print("ok")
