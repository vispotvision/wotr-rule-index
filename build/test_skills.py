"""The skills the MCP serves: listing, loading, references, and the path guard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import mcp_server as M

listing = M.skill_tool()
assert "wotr-write" in listing and "wotr-name" in listing and "judger" not in listing
assert M.skill_tool("wotr-write").startswith(M.SKILL_NOTE) and "references/rules.md" in M.skill_tool("wotr-write")
assert M.skill_tool("wotr-write", "references/rules.md").startswith("# The rule index")
for bad in ("../wotr-ops/SKILL.md", "/etc/passwd", "../../../build/.mcp_token", "references/../../../CLAUDE.md"):
    assert M.skill_tool("wotr-write", bad).startswith("no file"), bad
assert M.skill_tool("judger").startswith("no skill")
M.SKILL_HIDE.update(M.OPS_SKILLS)
assert "wotr-ops" not in M.skill_tool() and M.skill_tool("wotr-ops").startswith("no skill")
print("ok")
