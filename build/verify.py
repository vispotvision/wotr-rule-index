#!/usr/bin/env python3
"""Mechanical prose checks derived from the rule index and the AI-tells guide.

  python build/verify.py draft.md [--combat] [--culture Kharven] [--band standard|set-piece|conversational]

Every check names the rule it enforces. FAIL is a rule with a hard number or an
outright ban; WARN is a pattern that needs a human read (the FID carve-out, the
whose-vocabulary test). Nothing here judges quality; it counts.
"""
import argparse
import re
import statistics
import sys
from pathlib import Path

EM_DASH = re.compile(r"[—–]|(?<!-)--(?!-)")
ANTITHESIS = [
    re.compile(r"\b(?:not|isn['’]t|wasn['’]t|is not|was not|aren['’]t|weren['’]t)\s+(?:just|merely|simply|only|so much)\b[^.!?\n]{0,80}?\b(?:but|it['’]s|it is|as|rather)\b", re.I),
    re.compile(r"\b(?:this|that|it|which|he|she)\s+(?:is|was)\s+(?:less|more)\s+(?:a |an )?\w+\s+than\s+(?:a |an |it was |it is )?\w+", re.I),
    re.compile(r"\b(?:it|this|that)\s+(?:is|was|isn['’]t|wasn['’]t)\s+not\s+(?:a |an |the )?[\w\s]{1,30}?[,;]\s*(?:but|it['’]s|it was|it is)\b", re.I),
]
FRAGMENT = re.compile(r"(?:^|(?<=[.!?]\s))(?:Not|Never|And|Only|Just)\s+\w+(?:\s+\w+)?[.!]", re.M)
LADDER = re.compile(r"\b(?:was|is|became|meant)\s+[a-z]+\s+and\s+the\s+[a-z]+\s+(?:was|is|became|meant)\b", re.I)
FACULTIES = r"(?:Cymorath|Kamigan|Shingan|Meigan|Reigan|Tengan|Ketsumy[oō]gan|Crown Eye|Seeing|Ruling Sight|Revealing Sight|Spirit Sight|Sky Sight)"
APPARATUS_SUBJECT = re.compile(r"\b(?:his|her|the|their)\s+" + FACULTIES + r"\s+(?:saw|read|mapped|noted|caught|found|registered|filed|marked|tracked|perceived|counted|watched|traced|classified|flagged|told|reported)\b")
GLOSS = re.compile(r"\b(?:which meant|which was to say|meaning that|in other words|that is to say|which is to say|what that meant was)\b", re.I)
SIGNPOST = re.compile(r"\b(?:he|she|they|[A-Z][a-z]+)\s+(?:felt|was|were)\s+(?:a\s+(?:wave|surge|flicker|pang|rush|stab)\s+of\s+)?(?:afraid|fear|angry|anger|relief|relieved|dread|terror|terrified|joy|sad|sadness|grief|ashamed|shame|guilt|guilty|nervous|anxious|anxiety|hopeful|hope|despair)\b", re.I)
SIMILE = re.compile(r"\b(?:like an?|like the|as if|as though)\b", re.I)
TIDY_CLOSE = re.compile(r"^(?:Ultimately|In the end|And so|Finally|At last|Perhaps that|Maybe that)\b", re.I)
HYPOPHORA_Q = re.compile(r"\?\s*$")
WATCHLIST = r"(?:silence|weight|arithmetic|governance|permission|distance|authority|refusal|grief|history|patience|the question|the cost|the moment|the space between them)"
REIFY_VERBS = r"(?:sat|settled|moved|handed|passed|carried|hung|lay|arrived|landed|weighed|drained|took|held|filled|stood|waited|pressed|crossed|entered|left|followed|gathered|changed hands|went|came)"
REIFICATION = re.compile(r"\b(?:the\s+)?" + WATCHLIST + r"\s+(?:\w+\s+){0,2}?" + REIFY_VERBS + r"\b", re.I)
ITALIC = re.compile(r"(?<!\*)\*(?!\*)([^*\n]{3,}?)\*(?!\*)")
HEMA = re.compile(r"\b(?:Vor|Nach|Indes|Zornhau|Absetzen|Durchwechseln|Winden|Krumphau|Zwerchhau|Schielhau|Scheitelhau|Mutieren|Duplieren|bind|measure|half-sword|halfsword|pommel|guard|ward|thrust|cut|tempo|feint|parry|riposte|void|cross|edge|flat|crossguard|quillon|point|counter-cut)\b")
ANATOMY = re.compile(r"\b(?:femoral|carotid|clavicle|radius|ulna|humerus|tibia|fibula|patella|scapula|sternum|rib|ribs|vertebra|spine|jugular|subclavian|brachial|aorta|lung|liver|kidney|spleen|diaphragm|tendon|ligament|cartilage|orbit|mandible|maxilla|skull|trachea|larynx|hypovol|haemorrh|hemorrh|shock|Class\s+(?:I|II|III|IV))\b", re.I)

KHARVEN_RECURRENCE = {
    "the woodpile / how's your stack": re.compile(r"woodpile|how['’]s your stack|your stack", re.I),
    "the night-stone": re.compile(r"night-?stone", re.I),
    "wet wood": re.compile(r"wet wood", re.I),
    "the Thin Weeks": re.compile(r"thin weeks", re.I),
    "the death-house / the Waiting": re.compile(r"death-?house|\bthe Waiting\b"),
}
BANDS = {"conversational": (300, 700), "standard": (700, 1500), "set-piece": (2500, 10**9)}


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"“‘'A-Z])", text)
    return [p.strip() for p in parts if p.strip()]


def strip_md(text: str) -> str:
    text = re.sub(r"(?m)^#{1,6}\s+.*$", "", text)
    text = re.sub(r"(?m)^---\s*$", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return text


def run(text: str, combat: bool = False, culture: str | None = None, band: str = "standard") -> dict:
    fails, warns, info = [], [], []
    raw = text
    body = strip_md(text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    prose_paras = [p for p in paragraphs if not p.startswith(">") and not p.startswith("|")]
    sentences = [s for p in prose_paras for s in split_sentences(p)]
    words = [len(s.split()) for s in sentences]
    total_words = sum(words)

    # --- bans --------------------------------------------------------------
    n = len(EM_DASH.findall(raw))
    if n:
        fails.append(f"em dashes: {n} (banned; AI-tells §1, R15-1-AI_TELL_CHECKS_SURVIVE)")
    hits = [m.group(0) for rx in ANTITHESIS for m in rx.finditer(body)]
    for h in hits[:6]:
        fails.append(f"antithesis 'not X but Y': \"{h.strip()[:90]}\" (banned; AI-tells §1)")
    if len(hits) > 6:
        fails.append(f"antithesis: {len(hits) - 6} more")
    for sen in sentences:
        lad = LADDER.findall(sen)
        if len(lad) >= 2:
            fails.append(f"Ladder, two clauses in one sentence: \"{sen[:100]}\" (R6-1-LADDER_BAN, Check 18)")
        elif lad:
            warns.append(f"possible Ladder: \"{lad[0]}\" in \"{sen[:70]}...\" (Check 18: review by reading)")

    # countdown negation: 2+ consecutive short negated sentences resolving into Just/Only
    neg = re.compile(r"\b(?:no|not|never|nothing|none|nor)\b", re.I)
    i = 0
    while i < len(sentences) - 2:
        j = i
        while j < len(sentences) and len(sentences[j].split()) <= 9 and neg.search(sentences[j]):
            j += 1
        if j - i >= 2 and j < len(sentences) and re.match(r"^(?:Just|Only)\b", sentences[j]):
            fails.append(f"countdown negation: \"{' '.join(sentences[i:j + 1])[:140]}\" (AI-tells §1)")
            i = j + 1
        else:
            i += 1
    frags = FRAGMENT.findall(body)
    if len(frags) >= 3:
        warns.append(f"manufactured fragment emphasis: {len(frags)} short Not/Never/And/Only fragments (AI-tells §1)")

    # --- warn-level patterns -----------------------------------------------
    for m in APPARATUS_SUBJECT.finditer(body):
        warns.append(f"faculty as grammatical subject: \"{m.group(0)}\" (R6-2-FACULTY_NEVER_SUBJECT, Check 19)")
    for m in GLOSS.finditer(body):
        s = body[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")
        warns.append(f"gloss watch: \"...{s.strip()}...\" (R4-13-ZERO_BUDGET, Check 15; keep only if it is the POV's own idiom)")
    for m in SIGNPOST.finditer(body):
        warns.append(f"emotional signposting: \"{m.group(0)}\" (AI-tells §4)")
    q = [s for p in prose_paras if not p.startswith("\"") for s in split_sentences(p) if HYPOPHORA_Q.search(s) and not re.search(r"[\"“”]", s)]
    for s in q[:4]:
        warns.append(f"question in narration (hypophora?): \"{s[:80]}\" (AI-tells §1)")
    for p in prose_paras:
        sm = SIMILE.findall(p)
        if len(sm) >= 2:
            warns.append(f"competing similes in one paragraph ({len(sm)}): \"{p[:70]}...\" (AI-tells §5: cut one)")
    if sentences and TIDY_CLOSE.match(sentences[-1]):
        warns.append(f"tidy summary close: \"{sentences[-1][:80]}\" (AI-tells §2; WOTR scenes end on physical action)")

    # --- reification (R4-15) -----------------------------------------------
    reif = [(i, m.group(0)) for i, p in enumerate(prose_paras) for m in REIFICATION.finditer(p)]
    if len(reif) >= 3:
        fails.append(f"reification: {len(reif)} unlicensed instances, budget is two per scene (R4-15-TWO_PER_SCENE_BUDGET, Check 17): "
                     + "; ".join(f"\"{r[1]}\"" for r in reif[:5]))
    per_para = {}
    for i, r in reif:
        per_para.setdefault(i, []).append(r)
    for i, rs in per_para.items():
        if len(rs) >= 2:
            fails.append(f"reification: two in one paragraph (R4-15-ONE_PER_PARAGRAPH): " + "; ".join(f"\"{r}\"" for r in rs))
    if 1 <= len(reif) <= 2:
        info.append(f"reification: {len(reif)} (within budget): " + "; ".join(f"\"{r[1]}\"" for r in reif))

    # --- descent / variance (R4-14, Check 16) ------------------------------
    if len(words) >= 6:
        long_chain = 0
        for w in words:
            long_chain = long_chain + 1 if w > 25 else 0
            if long_chain == 3:
                fails.append("three consecutive sentences over 25 words (R4-14-CHAIN_CEILING)")
                break
        flat_runs = 0
        for i in range(len(words) - 2):
            a, b, c = words[i:i + 3]
            lo, hi = min(a, b, c), max(a, b, c)
            if lo >= 6 and hi <= lo * 1.4:
                flat_runs += 1
        if flat_runs >= 4:
            fails.append(f"flat runs: {flat_runs} stretches of three sentences within 40% of each other (R4-14-RUN_RULE)")
        elif flat_runs:
            info.append(f"flat runs: {flat_runs} (R4-14-RUN_RULE fails at 4)")
        short_share = sum(1 for w in words if w < 8) / len(words)
        if short_share < 0.10:
            fails.append(f"sentences under 8 words: {short_share:.0%} of scene, floor is 18% (R4-14-HARD_CEILINGS)")
        elif short_share < 0.18:
            warns.append(f"sentences under 8 words: {short_share:.0%}, floor is 18% (R4-14-HARD_CEILINGS)")
        lll = 0
        for p in prose_paras:
            ws = [len(s.split()) for s in split_sentences(p)]
            if len(ws) >= 3 and all(w > 18 for w in ws[-3:]):
                lll += 1
        if lll:
            warns.append(f"paragraphs closing on three sentences over 18 words: {lll} (R4-14-HARD_CEILINGS says 0)")
        cv = statistics.pstdev(words) / statistics.mean(words)
        info.append(f"sentence length: mean {statistics.mean(words):.1f} words, CV {cv:.2f} (variance is voice; under ~0.45 reads even)")
        pl = [len(p.split()) for p in prose_paras]
        if len(pl) >= 4:
            pcv = statistics.pstdev(pl) / statistics.mean(pl)
            info.append(f"paragraph length: mean {statistics.mean(pl):.0f} words, CV {pcv:.2f}")
            if pcv < 0.35:
                warns.append("paragraphs are uniform blocks (AI-tells §2: break deliberately)")

    # --- table rules ---------------------------------------------------------
    lo, hi = BANDS.get(band, BANDS["standard"])
    if total_words < lo or total_words > hi:
        warns.append(f"length {total_words} words, outside the {band} band {lo}–{hi if hi < 10**9 else '∞'} (Table Rule 2)")
    else:
        info.append(f"length {total_words} words ({band} band)")
    italics = [m.group(1) for m in ITALIC.finditer(raw) if len(m.group(1).split()) >= 3]
    info.append(f"italic interior beats: {len(italics)} (Table Rule 10: one per named NPC per scene)")
    if prose_paras:
        info.append(f"last line: \"{prose_paras[-1][-140:]}\" (must end on physical action, an NPC line, or a thing he can now see)")

    # --- culture recurrence (R6-9) -----------------------------------------
    if culture and culture.lower() == "kharven":
        present = [k for k, rx in KHARVEN_RECURRENCE.items() if rx.search(raw)]
        if len(present) < 2:
            fails.append(f"Kharven recurrence: {len(present)} of the five signature items present ({', '.join(present) or 'none'}); minimum two per Kharven scene (R6-9-RECURRENCE_RULE)")
        else:
            info.append(f"Kharven recurrence: {', '.join(present)}")

    # --- combat density (R13-9 checks 22-23, warn) --------------------------
    if combat:
        h = len(HEMA.findall(raw)); a = len(ANATOMY.findall(raw))
        if h == 0:
            warns.append("no HEMA vocabulary found in a combat scene (R13-6-HEMA_VOCAB, check 22)")
        if a == 0:
            warns.append("no anatomical/injury vocabulary found in a combat scene (R13-6-ANATOMY_VOCAB, check 23)")
        info.append(f"combat density: {h} HEMA terms, {a} anatomy terms")

    return {"fails": fails, "warns": warns, "info": info}


def report(res: dict) -> str:
    out = []
    out.append(f"{'FAIL' if res['fails'] else 'PASS'}: {len(res['fails'])} fail, {len(res['warns'])} warn")
    for f in res["fails"]:
        out.append(f"  FAIL  {f}")
    for w in res["warns"]:
        out.append(f"  WARN  {w}")
    for i in res["info"]:
        out.append(f"  info  {i}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--combat", action="store_true")
    ap.add_argument("--culture")
    ap.add_argument("--band", default="standard", choices=list(BANDS))
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    text = Path(a.file).read_text(encoding="utf-8", errors="replace")
    res = run(text, combat=a.combat, culture=a.culture, band=a.band)
    print(report(res))
    return 1 if res["fails"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
