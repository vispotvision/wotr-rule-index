"""R78-3 checks in verify.py: fight abstractions and bank density. Run: python build/test_r78_3.py"""
import sys; sys.path.insert(0, "build")
import verify as v

assert v.FIGHT_ABSTRACT.search("The parry had cost him the line.")
assert v.FIGHT_ABSTRACT.search("He closed measure fast.")
assert not v.FIGHT_ABSTRACT.search("the line of his jaw") and not v.FIGHT_ABSTRACT.search("He ruled a line under it.")
assert v.BANK.search("The rime lay hoar.") and v.BANK.search("The axe cleaved it.")
assert not v.BANK.search("He fell down.") and not v.BANK.search("He was standing.")
plain = " ".join(["He walked to the door and opened it."] * 12)
rich = " ".join(["The axe cleaved the shield and the rime lay hoar on it."] * 12)
assert any("elevated density" in w for w in v.run(plain)["warns"])
assert not any("elevated density" in w for w in v.run(rich)["warns"])
print("ok")
