"""R78-3 check in verify.py: fight abstractions. Run: python build/test_r78_3.py"""
import sys; sys.path.insert(0, "build")
import verify as v

assert v.FIGHT_ABSTRACT.search("The parry had cost him the line.")
assert v.FIGHT_ABSTRACT.search("He closed measure fast.")
assert not v.FIGHT_ABSTRACT.search("the line of his jaw") and not v.FIGHT_ABSTRACT.search("He ruled a line under it.")
plain = " ".join(["He walked to the door and opened it."] * 12)
assert not any("elevated density" in w for w in v.run(plain)["warns"])
print("ok")
