"""Merge the five revised groups and the cross-check patch into questions.json and check it."""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
WORK = HERE / "work"

groups = [json.loads(p.read_text()) for p in sorted(WORK.glob("group-*.json"))]
patch = json.loads((WORK / "patch.json").read_text())

sections, settled = {}, []
for g in groups:
    for s in g["sections"]:
        if s["key"] in sections:
            sections[s["key"]]["questions"] += s["questions"]
        else:
            sections[s["key"]] = s
    settled += g.get("settled", [])

drop = {d["id"] for d in patch.get("drop", [])}
for s in sections.values():
    s["questions"] = [q for q in s["questions"] if q["id"] not in drop]
for add in patch.get("add", []):
    s = sections.setdefault(add["section_key"], {"key": add["section_key"], "title": add["section_key"], "intro": "", "questions": []})
    ids = [q["id"] for q in s["questions"]]
    at = ids.index(add["after_id"]) + 1 if add.get("after_id") in ids else len(ids)
    s["questions"].insert(at, add["question"])
qs = {q["id"]: q for s in sections.values() for q in s["questions"]}
for rc in patch.get("rec_changes", []):
    if rc["id"] in qs:
        qs[rc["id"]].update({k: rc[k] for k in ("recommended", "rec_reason") if k in rc})
for k, intro in patch.get("intros", {}).items():
    if k in sections:
        sections[k]["intro"] = intro
settled += patch.get("settled_extra", [])

order = [k for k in patch.get("section_order", []) if k in sections]
for new, after in (("NM", "NE"), ("VB", "RH")):
    if new in sections and new not in order and after in order:
        order.insert(order.index(after) + 1, new)
order += [k for k in sections if k not in order]
out = {"lede": patch.get("lede", ""), "sections": [sections[k] for k in order if sections[k]["questions"]], "settled": settled}

# checks
problems = []
seen = set()
for s in out["sections"]:
    for q in s["questions"]:
        if q["id"] in seen:
            problems.append(f"duplicate id {q['id']}")
        seen.add(q["id"])
        keys = {o["key"] for o in q["options"]}
        for r in re.split(r"\s*,\s*", str(q.get("recommended", ""))):
            if r and r not in keys:
                problems.append(f"{q['id']}: recommended {r} not an option")
        for d in q.get("depends_on", []):
            if d not in qs and d not in seen:
                pass
text = json.dumps(out, ensure_ascii=False)
for ch in ("—", "–"):
    if ch in text:
        problems.append(f"dash {ch!r} present {text.count(ch)}x")
dangling = sorted({d for q in qs.values() for d in q.get("depends_on", []) if d not in seen})
if dangling:
    problems.append(f"depends_on points at missing ids: {dangling}")

for s in out["sections"]:
    for q in s["questions"]:
        if len(q["options"]) > 4:
            problems.append(f"{q['id']}: {len(q['options'])} options (chat cap 4)")
(HERE / "questions.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
n = sum(len(s["questions"]) for s in out["sections"])
print(n, "questions in", len(out["sections"]), "sections;", len(settled), "settled")
print("\n".join(problems) or "checks clean")
