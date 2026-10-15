"""Mermaid charts, redrawn as the site's own art.

site_content.py hands every ```mermaid block here at build time; the vault keeps the
mermaid source (Obsidian draws it). Three shapes come back as raw HTML:

  a chain of steps   -> an illuminated road (HTML, a gilt spine of numbered medallions)
  a timeline         -> era bands on the same spine
  anything branching -> SVG plaques and gilt connectors, laid out by Graphviz (dot)
"""
import hashlib, json, math, random, re, subprocess
from html import escape

from site_art import crest, style_for

GOLD, INK, TEXT, MUTED = "#d8ab4f", "#110d09", "#f1e4c6", "#b9a583"
SERIF = "'Cormorant Garamond', Garamond, Georgia, serif"
BODY = "'Crimson Pro', Georgia, serif"

OPEN = r'(\[\[|\[\(|\(\[|\(\(|\{\{|\[|\(|\{|>)'
NODE = re.compile(r'\s*([\w-]+)\s*(?:' + OPEN + r'\s*(?:"((?:[^"\\]|\\.)*)"|([^\]\)\}"]*))\s*(?:\]\]|\)\]|\]\)|\)\)|\}\}|\]|\)|\}))?')
LINK = re.compile(r'\s*(-\.->|-\.-|==>|-->|---)\s*(?:\|"?([^|"]*)"?\|)?')


def _clean(s):
    s = re.sub(r"#quot;", '"', s or "")
    s = re.sub(r"\*\*|__|`", "", s)
    return [l.strip() for l in re.split(r"<br\s*/?>|\\n", s) if l.strip()]


def parse(src):
    lines = [l.strip() for l in src.strip().splitlines() if l.strip() and not l.strip().startswith("%%")]
    head = lines[0].split()
    if head[0] == "timeline":
        title, sections, cur = "", [], None
        for l in lines[1:]:
            if l.startswith("title "):
                title = l[6:].strip()
            elif l.startswith("section "):
                cur = [l[8:].strip(), []]; sections.append(cur)
            else:
                parts = [p.strip() for p in l.split(" : ") if p.strip()]
                if cur is None:
                    cur = ["", []]; sections.append(cur)
                cur[1].extend(parts)
        return {"kind": "timeline", "title": title, "sections": sections}
    g = {"kind": "flow", "dir": (head[1] if len(head) > 1 else "TD").upper(), "nodes": {}, "order": [], "edges": [], "groups": []}
    stack = []
    for l in lines[1:]:
        group = stack[-1] if stack else None
        if l.startswith(("classDef", "class ", "style ", "linkStyle", "click", "direction")):
            continue
        if l.startswith("subgraph"):
            m = re.match(r'subgraph\s+([\w-]+)?\s*(?:\[\s*"?([^"\]]*)"?\s*\])?\s*(.*)', l)
            sub = [(m.group(2) or m.group(3) or m.group(1) or "").strip().strip('"'), [], group]
            g["groups"].append(sub); stack.append(sub); continue
        if l == "end":
            stack and stack.pop(); continue
        pos, chain, links = 0, [], []
        while pos < len(l):
            ids = []
            while True:
                m = NODE.match(l, pos)
                if not m or not m.group(1):
                    break
                nid, label = m.group(1), m.group(3) if m.group(3) is not None else m.group(4)
                if nid not in g["nodes"]:
                    g["nodes"][nid] = _clean(label) or [nid]; g["order"].append(nid)
                elif label:
                    g["nodes"][nid] = _clean(label)
                if group is not None and nid not in group[1]:
                    group[1].append(nid)
                ids.append(nid); pos = m.end()
                a = re.match(r"\s*&", l[pos:])
                if not a:
                    break
                pos += a.end()
            if not ids:
                break
            chain.append(ids)
            m = LINK.match(l, pos)
            if not m:
                break
            links.append((m.group(1), " ".join(_clean(m.group(2) or "")))); pos = m.end()
        for (a, b), (kind, lab) in zip(zip(chain, chain[1:]), links):
            for x in a:
                for y in b:
                    g["edges"].append((x, y, lab, "dash" if "." in kind else ("none" if kind in ("---",) else "arrow")))
    return g


def is_chain(g):
    if g["groups"] or len(g["nodes"]) < 4 or len(g["edges"]) != len(g["nodes"]) - 1:
        return None
    nxt = {}
    ins = {}
    for a, b, lab, k in g["edges"]:
        if a in nxt or b in ins:
            return None
        nxt[a] = b; ins[b] = a
    start = [n for n in g["nodes"] if n not in ins]
    if len(start) != 1:
        return None
    seq, n = [], start[0]
    while n is not None and n not in seq:
        seq.append(n); n = nxt.get(n)
    return seq if len(seq) == len(g["nodes"]) else None


NUM = re.compile(r"^((?:\d+|[IVXL]+))\s*(?:·|\.|:)?\s+(.+)$")


def road(g, seq):
    out = ['<ol class="wotr-road">']
    via = {b: lab for a, b, lab, k in g["edges"] if lab}
    for i, nid in enumerate(seq, 1):
        lines = g["nodes"][nid]
        m = NUM.match(lines[0])
        num, title = (m.group(1), m.group(2)) if m else (str(i), lines[0])
        sub = "".join(f'<span class="rs">{escape(s)}</span>' for s in lines[1:])
        if nid in via:
            sub = f'<span class="rv">{escape(via[nid])}</span>' + sub
        out.append(f'<li><span class="rn">{escape(num)}</span><div class="rc"><span class="rt">{escape(title)}</span>{sub}</div></li>')
    out.append("</ol>")
    return "".join(out)


def timeline(t):
    out = ['<div class="wotr-era">']
    if t["title"]:
        out.append(f'<div class="et">{escape(t["title"])}</div>')
    out.append('<ol class="wotr-road wotr-road-era">')
    for i, (name, events) in enumerate(t["sections"], 1):
        m = re.match(r"(.*?)\s*\(([^)]*)\)\s*$", name)
        nm, span = (m.group(1), m.group(2)) if m else (name, "")
        ev = "".join(f'<span class="ev">{escape(e)}</span>' for e in events)
        out.append(f'<li><span class="rn">{i}</span><div class="rc"><span class="rt">{escape(nm)}</span>'
                   + (f'<span class="rd">{escape(span)}</span>' if span else "") + f'<span class="evs">{ev}</span></div></li>')
    out.append("</ol></div>")
    return "".join(out)


# ---------------------------------------------------------------- branching charts, drawn in SVG

def _wrap(lines, width):
    out = []
    for i, l in enumerate(lines):
        words, cur = l.split(), ""
        lim = width if i else int(width * 0.8)
        for w in words:
            if cur and len(cur) + 1 + len(w) > lim:
                out.append((i, cur)); cur = w
            else:
                cur = (cur + " " + w).strip()
        out.append((i, cur))
    return out


def _measure(lines):
    wrapped = _wrap(lines, 26)
    w = max((len(t) * (11.6 if i == 0 else 8.3)) for i, t in wrapped) + 48
    h = sum(27 if i == 0 else 23 for i, _ in wrapped) + 32
    return max(w, 120), h, wrapped


def flow_svg(g, uid, crest_key=""):
    rank = {"TD": "TB", "TB": "TB", "LR": "LR", "BT": "BT", "RL": "RL"}.get(g["dir"], "TB")
    sizes = {n: _measure(l) for n, l in g["nodes"].items()}
    ids = {n: f"n{i}" for i, n in enumerate(g["order"])}
    dot = [f'digraph G {{ rankdir={rank}; nodesep=0.45; ranksep=0.6; splines=spline; node [shape=box, fixedsize=true, label=""];',
           'edge [dir=none, fontsize=14, fontname="Georgia"];']
    def cluster(k):
        title, members, _ = g["groups"][k]
        kids = [j for j, grp in enumerate(g["groups"]) if grp[2] is g["groups"][k]]
        return (f'subgraph cluster_{k} {{ label="{title.replace(chr(34), "")}"; fontsize=18; fontname="Georgia"; margin=22; '
                + "".join(f"{ids[m]}; " for m in members) + " ".join(cluster(j) for j in kids) + " }")
    for k, grp in enumerate(g["groups"]):
        if grp[2] is None:
            dot.append(cluster(k))
    for n in g["order"]:
        w, h, _ = sizes[n]
        dot.append(f'{ids[n]} [width={w / 72:.3f}, height={h / 72:.3f}];')
    for a, b, lab, k in g["edges"]:
        l = f', label="{lab.replace(chr(34), "")}"' if lab else ""
        dot.append(f'{ids[a]} -> {ids[b]} [{l.lstrip(", ")}];')
    dot.append("}")
    lay = lambda src, eng="dot": json.loads(subprocess.run([eng, "-Tjson"], input=src, capture_output=True, text=True, check=True).stdout)
    parents = {}
    for a, b, lab, k in g["edges"]:
        parents.setdefault(b, set()).add(a)
    roots = [n for n in g["order"] if n not in parents]
    kids = lambda n: [b for a, b, l, k in g["edges"] if a == n]
    tree = all(len(v) == 1 for v in parents.values()) and len(roots) == 1 and not g["groups"]
    radial = False  # twopi spreads these too thin; kept for a later, better radial drawing
    if radial:
        src = "\n".join(dot).replace("rankdir=TB; nodesep=0.45; ranksep=0.6; splines=spline;",
                                       f"root={ids[roots[0]]}; ranksep=2.1; overlap=false; splines=curved;", 1)
        src = src.replace(f"rankdir={rank}; nodesep=0.45; ranksep=0.6; splines=spline;", f"root={ids[roots[0]]}; ranksep=2.1; overlap=false; splines=curved;", 1)
        js = lay(src, "twopi")
    else:
        js = lay("\n".join(dot))
    width = lambda j: float(j["bb"].split(",")[2])
    if not radial and rank == "TB" and width(js) > 1000:  # a wide fan reads better turned on its side
        side = lay("\n".join(dot).replace("rankdir=TB", "rankdir=LR", 1))
        if width(side) < width(js):
            js = side
    x0, y0, x1, y1 = map(float, js["bb"].split(","))
    pad = 40
    W, H = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    X = lambda x: x - x0 + pad
    Y = lambda y: (y1 - y) + pad
    r = random.Random(uid)
    o = [f'<svg class="wotr-chart" viewBox="0 0 {W:.0f} {H:.0f}" style="--mw:{min(W, 680):.0f}px" font-family="{SERIF}" role="img">',
         f'<defs><linearGradient id="pl{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1f12"/><stop offset="1" stop-color="#140f0a"/></linearGradient>'
         f'<linearGradient id="ed{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d58c"/><stop offset="1" stop-color="#b07a24"/></linearGradient>'
         f'<radialGradient id="bg{uid}" cx=".5" cy="0" r="1.1"><stop offset="0" stop-color="#2c2010"/><stop offset="1" stop-color="{INK}"/></radialGradient>'
         f'<filter id="gl{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>'
         f'<radialGradient id="halo{uid}"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W:.0f}" height="{H:.0f}" rx="16" fill="url(#bg{uid})"/>']
    for _ in range(int(W * H / 9000)):
        o.append(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" r="{r.choice((.6, .9, 1.3))}" fill="#fff4d6" opacity="{r.uniform(.1, .55):.2f}"/>')
    if crest_key:
        cs = min(W, H) * .55
        o.append(crest(crest_key, cs, W - cs * .8, H - cs * .85, GOLD, 2, .07))
    o.append(f'<rect x="7" y="7" width="{W - 14:.0f}" height="{H - 14:.0f}" rx="12" fill="none" stroke="{GOLD}" stroke-opacity=".4"/>')
    for x, y, sx, sy in ((7, 7, 1, 1), (W - 7, 7, -1, 1), (7, H - 7, 1, -1), (W - 7, H - 7, -1, -1)):
        o.append(f'<path d="M{x:.0f} {y + 22 * sy:.0f} L{x:.0f} {y:.0f} L{x + 22 * sx:.0f} {y:.0f}" fill="none" stroke="{GOLD}" stroke-width="2"/>')
    for obj in js.get("objects", []):
        if obj.get("name", "").startswith("cluster") and "bb" in obj:
            a, b, c, d = map(float, obj["bb"].split(","))
            o.append(f'<rect x="{X(a):.0f}" y="{Y(d):.0f}" width="{c - a:.0f}" height="{d - b:.0f}" rx="14" fill="{GOLD}" fill-opacity=".04" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="5 6"/>')
            lab = obj.get("label", "")
            o.append(f'<text x="{X((a + c) / 2):.0f}" y="{Y(d) + 22:.0f}" text-anchor="middle" fill="{GOLD}" font-size="16" letter-spacing="2">{escape(lab.upper())}</text>')
    name = {v: k for k, v in ids.items()}
    objs = {o_["_gvid"]: o_ for o_ in js.get("objects", [])}
    for e in js.get("edges", []):
        a, b = name[objs[e["tail"]]["name"]], name[objs[e["head"]]["name"]]
        style = next(k for x, y, l, k in g["edges"] if x == a and y == b)
        pts = [tuple(map(float, p.split(","))) for p in e["pos"].split() if not p.startswith(("e,", "s,"))]
        pts = [(X(x), Y(y)) for x, y in pts]
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f} " + " ".join(f"C{pts[i][0]:.1f} {pts[i][1]:.1f} {pts[i + 1][0]:.1f} {pts[i + 1][1]:.1f} {pts[i + 2][0]:.1f} {pts[i + 2][1]:.1f}" for i in range(1, len(pts) - 2, 3))
        dash = ' stroke-dasharray="6 6"' if style == "dash" else ""
        o.append(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="6" filter="url(#gl{uid})"/>')
        o.append(f'<path d="{d}" fill="none" stroke="url(#ed{uid})" stroke-width="2"{dash}/>')
        if style != "none":
            (ax, ay), (bx, by) = pts[-2], pts[-1]
            ang = math.degrees(math.atan2(by - ay, bx - ax))
            o.append(f'<path d="M0 0 L-11 -6 L-7 0 L-11 6 Z" transform="translate({bx:.1f} {by:.1f}) rotate({ang:.0f})" fill="#f3d58c"/>')
        if e.get("label") and "lp" in e:
            lx, ly = map(float, e["lp"].split(","))
            lw = len(e["label"]) * 8.2 + 20
            o.append(f'<rect x="{X(lx) - lw / 2:.0f}" y="{Y(ly) - 13:.0f}" width="{lw:.0f}" height="24" rx="12" fill="{INK}" stroke="{GOLD}" stroke-opacity=".5"/>')
            o.append(f'<text x="{X(lx):.0f}" y="{Y(ly) + 5:.0f}" text-anchor="middle" fill="{MUTED}" font-size="15.5" font-style="italic" font-family="{BODY}">{escape(e["label"])}</text>')
    for obj in js.get("objects", []):
        if obj.get("name") not in name:
            continue
        n = name[obj["name"]]
        cx, cy = map(float, obj["pos"].split(","))
        w, h, wrapped = sizes[n]
        x, y = X(cx) - w / 2, Y(cy) - h / 2
        if n in roots and len(g["nodes"]) > 2:  # the source of the chart wears a halo
            o.append(f'<ellipse cx="{X(cx):.1f}" cy="{Y(cy):.1f}" rx="{w * .85:.0f}" ry="{h * 1.3:.0f}" fill="url(#halo{uid})"/>')
            o.append(f'<rect x="{x - 7:.1f}" y="{y - 7:.1f}" width="{w + 14:.0f}" height="{h + 14:.0f}" rx="16" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-dasharray="2 5"/>')
        o.append(f'<rect x="{x:.1f}" y="{y + 4:.1f}" width="{w:.0f}" height="{h:.0f}" rx="11" fill="#000" opacity=".45" filter="url(#gl{uid})"/>')
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.0f}" height="{h:.0f}" rx="11" fill="url(#pl{uid})" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.4"/>')
        o.append(f'<rect x="{x + 4:.1f}" y="{y + 4:.1f}" width="{w - 8:.0f}" height="{h - 8:.0f}" rx="8" fill="none" stroke="{GOLD}" stroke-opacity=".2"/>')
        o.append(f'<polygon points="{X(cx):.1f},{y - 6:.1f} {X(cx) + 6:.1f},{y:.1f} {X(cx):.1f},{y + 6:.1f} {X(cx) - 6:.1f},{y:.1f}" fill="{GOLD}"/>')
        ty = y + 15
        for i, t in wrapped:
            ty += 27 if i == 0 else 23
            if i == 0:
                o.append(f'<text x="{X(cx):.1f}" y="{ty - 7:.1f}" text-anchor="middle" fill="{GOLD}" font-size="21" font-weight="600" letter-spacing=".5">{escape(t)}</text>')
            else:
                o.append(f'<text x="{X(cx):.1f}" y="{ty - 7:.1f}" text-anchor="middle" fill="{TEXT}" font-size="17" font-style="italic" font-family="{BODY}">{escape(t)}</text>')
    o.append("</svg>")
    return '<div class="wotr-chart-wrap">' + "".join(o) + "</div>"


def render(src, seed=""):
    """One mermaid source -> raw HTML. Falls back to the source if it cannot be read."""
    uid = hashlib.sha1((seed + src).encode()).hexdigest()[:8]
    try:
        g = parse(src)
        if g["kind"] == "timeline":
            return timeline(g)
        seq = is_chain(g)
        return road(g, seq) if seq else flow_svg(g, uid, style_for(seed)[0][0] if seed else "")
    except Exception as e:  # a chart the parser cannot read stays mermaid
        print(f"  chart left as mermaid ({e})")
        return None
