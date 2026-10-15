"""The site's artwork, all SVG: section crests, a plate for every page, the system diagrams.

  python build/site_art.py      # rewrite wiki/Assets/Diagrams/*.svg (the vault embeds them)

site_content.py imports plate() and banner() and lays them over each public page at build
time, so the vault stays plain markdown.
"""
import hashlib, math, random
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIAGRAMS = ROOT / "wiki" / "Assets" / "Diagrams"
SERIF = "'Cormorant Garamond', 'EB Garamond', Garamond, Georgia, serif"
BODY = "'Crimson Pro', Georgia, serif"
GOLD, INK, TEXT, MUTED = "#d8ab4f", "#110d09", "#f1e4c6", "#a8957a"

# section -> (key, hue, deep, painted art or None, tagline)
SECTIONS = {
    "The Magic System": ("magic", "#8a5cf0", "#1a0f2e", "magic", "Sixteen Stages, sixty Wellsprings, and the bill for every working."),
    "Races & Peoples": ("peoples", "#e0a24a", "#24170a", "peoples", "The peoples of the realms: their tongues, their blood, their ways."),
    "Factions, Bloodlines & Institutions": ("factions", "#d0453a", "#2a0c0b", "factions", "Crowns, guilds, orders and the old blood that owns them."),
    "Geography & the Four Quarters": ("geography", "#3fb59a", "#08201b", "geography", "Four Quarters, two worlds, and the roads and coin between them."),
    "Cosmology & Metaphysics": ("cosmology", "#5b8ff0", "#0a1430", "cosmology", "Titans, Archons, the Veil and the ages of the world."),
    "The Bestiary": ("bestiary", "#c43a5a", "#250a12", "bestiary", "What hunts the dark, and what the Wells spawn into it."),
    "Lore & History": ("lore", "#d8ab4f", "#21180a", "lore", "The chronicles, the codices, and what the record keeps."),
    "Materials, Alchemy & Trade": ("materials", "#46c27a", "#0a2014", "alchemy", "Ores, Drafts, prepared tags and the price of everything."),
    "The War Cycle": ("war", "#e2603a", "#2a0f06", None, "How a war is paid for, marched, fought, survived and buried."),
}
DEFAULT = ("crown", "#d8ab4f", "#1c140b", "hero", "")

# Crests, drawn on a 200x200 box centred at (100,100); stroke-only, painted with currentColor.
CRESTS = {
    "magic": """
      <circle cx="100" cy="100" r="86"/><circle cx="100" cy="100" r="74" stroke-dasharray="2 5"/>
      <polygon points="100,22 167,139 33,139"/><polygon points="100,178 33,61 167,61"/>
      <circle cx="100" cy="100" r="30"/><polygon points="100,78 119,100 100,122 81,100" fill="currentColor" fill-opacity=".35"/>
      <circle cx="100" cy="22" r="5"/><circle cx="167" cy="139" r="5"/><circle cx="33" cy="139" r="5"/>""",
    "peoples": """
      <circle cx="78" cy="84" r="44"/><circle cx="122" cy="84" r="44"/><circle cx="100" cy="122" r="44"/>
      <circle cx="100" cy="97" r="8" fill="currentColor" fill-opacity=".45"/>
      <path d="M30 172 Q100 150 170 172" stroke-dasharray="3 5"/>""",
    "factions": """
      <path d="M100 26 L160 46 L160 104 Q160 150 100 178 Q40 150 40 104 L40 46 Z"/>
      <path d="M100 38 L150 54 L150 104 Q150 142 100 166 Q50 142 50 104 L50 54 Z" stroke-opacity=".5"/>
      <path d="M58 118 L100 82 L142 118"/><path d="M58 136 L100 100 L142 136"/>
      <path d="M78 14 L84 26 L92 16 L100 26 L108 16 L116 26 L122 14" />""",
    "geography": """
      <circle cx="100" cy="100" r="80"/><circle cx="100" cy="100" r="62" stroke-dasharray="1 4"/>
      <polygon points="100,12 110,90 100,100 90,90" fill="currentColor" fill-opacity=".55"/>
      <polygon points="100,188 110,110 100,100 90,110"/>
      <polygon points="12,100 90,90 100,100 90,110"/><polygon points="188,100 110,110 100,100 110,90" fill="currentColor" fill-opacity=".55"/>
      <polygon points="40,40 96,94 100,100 94,96" /><polygon points="160,160 104,106 100,100 106,104"/>
      <polygon points="160,40 106,96 100,100 104,94"/><polygon points="40,160 94,104 100,100 96,106"/>""",
    "cosmology": """
      <circle cx="100" cy="100" r="16" fill="currentColor" fill-opacity=".45"/>
      <ellipse cx="100" cy="100" rx="84" ry="30" transform="rotate(-24 100 100)"/>
      <ellipse cx="100" cy="100" rx="84" ry="30" transform="rotate(36 100 100)"/>
      <ellipse cx="100" cy="100" rx="56" ry="56" stroke-dasharray="2 6"/>
      <circle cx="176" cy="66" r="6" fill="currentColor"/><circle cx="34" cy="62" r="4" fill="currentColor"/>
      <circle cx="129" cy="149" r="5" fill="currentColor"/>""",
    "bestiary": """
      <path d="M100 18 L182 100 L100 182 L18 100 Z"/>
      <path d="M40 100 Q100 44 160 100 Q100 156 40 100 Z"/>
      <ellipse cx="100" cy="100" rx="9" ry="30" fill="currentColor" fill-opacity=".6"/>
      <path d="M58 30 Q70 60 62 86"/><path d="M76 22 Q88 54 80 82"/><path d="M142 170 Q130 140 138 114"/><path d="M124 178 Q112 146 120 118"/>""",
    "lore": """
      <path d="M100 150 Q70 128 26 134 L26 58 Q70 52 100 74 Q130 52 174 58 L174 134 Q130 128 100 150 Z"/>
      <path d="M100 74 L100 150"/><path d="M40 76 Q66 72 88 84"/><path d="M40 92 Q66 88 88 100"/><path d="M40 108 Q66 104 88 116"/>
      <path d="M160 76 Q134 72 112 84"/><path d="M160 92 Q134 88 112 100"/><path d="M160 108 Q134 104 112 116"/>
      <path d="M100 58 L100 20"/><path d="M78 56 L60 26"/><path d="M122 56 L140 26"/><path d="M58 64 L28 44"/><path d="M142 64 L172 44"/>""",
    "materials": """
      <circle cx="100" cy="130" r="48"/><path d="M86 84 L86 30 L114 30 L114 84"/><path d="M78 30 L122 30"/>
      <path d="M58 140 Q100 120 142 140" stroke-opacity=".6"/>
      <polygon points="100,108 120,144 80,144" fill="currentColor" fill-opacity=".35"/>
      <circle cx="132" cy="56" r="5"/><circle cx="146" cy="40" r="3"/><circle cx="66" cy="60" r="4"/>""",
    "war": """
      <path d="M40 40 L150 150"/><path d="M160 40 L50 150"/>
      <path d="M32 32 L44 36 L40 48"/><path d="M168 32 L156 36 L160 48"/>
      <path d="M138 162 L162 138"/><path d="M38 138 L62 162"/>
      <polygon points="100,62 116,84 140,84 128,106 136,130 100,118 64,130 72,106 60,84 84,84" fill="currentColor" fill-opacity=".25"/>
      <circle cx="100" cy="100" r="14"/>""",
    "crown": """
      <path d="M38 140 L30 66 L68 100 L100 46 L132 100 L170 66 L162 140 Z"/>
      <path d="M38 156 L162 156"/><circle cx="100" cy="46" r="7" fill="currentColor"/><circle cx="30" cy="66" r="5"/><circle cx="170" cy="66" r="5"/>
      <polygon points="100,104 112,120 100,136 88,120" fill="currentColor" fill-opacity=".45"/>""",
}


def style_for(rel: str):
    top = rel.split("/")[0]
    return SECTIONS.get(top, DEFAULT), top if top in SECTIONS else ""


def crest(key, size=200, x=0, y=0, color=GOLD, width=3, opacity=1.0):
    s = size / 200
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" fill="none" stroke="{color}" color="{color}" '
            f'stroke-width="{width / s:.2f}" stroke-linejoin="round" stroke-linecap="round" opacity="{opacity}">{CRESTS[key]}</g>')


def _rng(seed):
    return random.Random(int(hashlib.sha1(seed.encode()).hexdigest()[:12], 16))


def plate_svg(title, key, hue, deep, uid):
    """The art behind a page's title: a starfield, a rune wheel and the section crest."""
    r = _rng(title)
    cx, cy = 980 + r.randint(-40, 40), 120
    o = [f'<svg class="wotr-plate-art" viewBox="0 0 1200 240" preserveAspectRatio="xMaxYMid slice" aria-hidden="true">',
         f'<defs><linearGradient id="pg{uid}" x1="0" x2="1"><stop offset="0" stop-color="{INK}"/><stop offset=".55" stop-color="{deep}"/><stop offset="1" stop-color="{INK}"/></linearGradient>',
         f'<radialGradient id="pr{uid}" cx="{cx / 1200:.3f}" cy=".5" r=".45"><stop offset="0" stop-color="{hue}" stop-opacity=".55"/><stop offset="1" stop-color="{hue}" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="1200" height="240" fill="url(#pg{uid})"/><rect width="1200" height="240" fill="url(#pr{uid})"/>']
    stars = [(r.uniform(0, 1200), r.uniform(0, 240)) for _ in range(70)]
    for x, y in stars:
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice((0.6, 0.9, 1.2, 1.7))}" fill="#fff4d6" opacity="{r.uniform(.15, .8):.2f}"/>')
    pick = r.sample(stars[:40], 6)
    pick.sort()
    o.append('<polyline points="' + " ".join(f"{x:.0f},{y:.0f}" for x, y in pick) + f'" fill="none" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1"/>')
    # rune wheel
    step = r.choice((5, 6, 8, 10, 12))
    for rad, op in ((150, .22), (118, .35), (96, .18)):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1.2"/>')
    for a in range(0, 360, step):
        t = math.radians(a + r.random() * 0.5)
        l = 10 if a % (step * 3) == 0 else 5
        o.append(f'<line x1="{cx + 118 * math.cos(t):.1f}" y1="{cy + 118 * math.sin(t):.1f}" x2="{cx + (118 + l) * math.cos(t):.1f}" y2="{cy + (118 + l) * math.sin(t):.1f}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1.2"/>')
    for _ in range(r.randint(9, 15)):  # glyph marks between the rings
        t = r.uniform(0, 2 * math.pi)
        x, y = cx + 134 * math.cos(t), cy + 134 * math.sin(t)
        g = r.choice(("M-5 -5 L5 5 M-5 5 L0 0", "M0 -6 L0 6 M-4 -2 L4 -2", "M-5 4 L0 -6 L5 4", "M-4 -4 L4 -4 L-4 4 L4 4", "M0 -6 A6 6 0 0 1 0 6"))
        o.append(f'<path d="{g}" transform="translate({x:.1f} {y:.1f}) rotate({math.degrees(t) + 90:.0f})" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.3"/>')
    o.append(crest(key, 150, cx - 75, cy - 75, GOLD, 2.4, .9))
    o.append(f'<rect x="10" y="10" width="1180" height="220" rx="6" fill="none" stroke="{GOLD}" stroke-opacity=".28"/>')
    for x, y, sx, sy in ((10, 10, 1, 1), (1190, 10, -1, 1), (10, 230, 1, -1), (1190, 230, -1, -1)):
        o.append(f'<path d="M{x} {y + 26 * sy} L{x} {y} L{x + 26 * sx} {y} M{x + 6 * sx} {y + 6 * sy} L{x + 14 * sx} {y + 6 * sy}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-opacity=".75"/>')
    o.append("</svg>")
    return "".join(o)


def _attr(s):
    return escape(s, quote=True)


def _words(kicker, title, tag=""):
    """Empty spans whose words CSS draws from data-t, so they stay out of search and previews."""
    spans = [("wk", kicker), ("wt", title)] + ([("wg", tag)] if tag else [])
    return '<div class="wotr-words">' + "".join(f'<span class="{c}" data-t="{_attr(v)}"></span>' for c, v in spans) + "</div>"


def plate(rel, title):
    """Raw HTML set at the head of an ordinary page. Title and kicker ride on data
    attributes (CSS draws them), so search previews and descriptions stay clean."""
    (key, hue, deep, _, _), top = style_for(rel)
    parts = rel.split("/")[:-1]
    kicker = " · ".join(p for p in parts if p != title) or "War of the Realms"
    uid = hashlib.sha1(rel.encode()).hexdigest()[:8]
    return (f'<div class="wotr-plate wotr-s-{key}">{plate_svg(title, key, hue, deep, uid)}'
            f'{_words(kicker, title)}</div>\n\n')


def banner(rel, title, base):
    """A section front page: the painted art (or the crest alone), the title and the tagline."""
    (key, hue, deep, art, tag), top = style_for(rel)
    if top and top != title:  # a sub-folder's front page inside a section
        tag = ""
        kicker = " · ".join(rel.split("/")[:-2])
    else:
        kicker = "War of the Realms"
    img = f'background-image:url({base}/assets/{art}.webp);' if art else ""
    uid = hashlib.sha1(rel.encode()).hexdigest()[:8]
    art_svg = "" if art else plate_svg(title, key, hue, deep, uid)
    return (f'<div class="wotr-banner wotr-s-{key}" style="{img}--hue:{hue}">{art_svg}'
            f'<svg class="wotr-banner-crest" viewBox="0 0 200 200" aria-hidden="true">{crest(key, 200, 0, 0, GOLD, 3)}</svg>'
            f'{_words(kicker, title, tag)}</div>\n\n')


# ---------------------------------------------------------------- diagrams

def _frame(w, h, title, sub=""):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{SERIF}">',
            f'<defs><radialGradient id="glow" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#3a2a12"/><stop offset="1" stop-color="{INK}"/></radialGradient></defs>',
            f'<rect width="{w}" height="{h}" rx="14" fill="url(#glow)"/>',
            f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="10" fill="none" stroke="{GOLD}" stroke-opacity=".45"/>',
            f'<text x="{w / 2}" y="58" text-anchor="middle" fill="{GOLD}" font-size="34" font-weight="600" letter-spacing="3">{escape(title.upper())}</text>',
            (f'<text x="{w / 2}" y="88" text-anchor="middle" fill="{MUTED}" font-size="19" font-style="italic" font-family="{BODY}">{escape(sub)}</text>' if sub else ""),
            f'<path d="M{w / 2 - 120} 100 L{w / 2 - 12} 100 M{w / 2 + 12} 100 L{w / 2 + 120} 100" stroke="{GOLD}" stroke-opacity=".5"/>',
            f'<polygon points="{w / 2},94 {w / 2 + 6},100 {w / 2},106 {w / 2 - 6},100" fill="{GOLD}"/>']


def t(x, y, s, size=18, fill=TEXT, anchor="start", weight="normal", italic=False, font=None, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"'
            + (' font-style="italic"' if italic else "") + (f' font-family="{font}"' if font else "") + f' {extra}>{escape(s)}</text>')


STAGES = [  # numeral, name, tier, colour, street name
    ("I", "Murmuring", "1 · Initiate", "#16120e", "carrying a bee"),
    ("II", "Welling", "2 · Apprentice", "#2b211a", "the spilling year"),
    ("III", "Ascension", "3 · Journeyman", "#4d3b2b", "coming into the road"),
    ("IV", "Flourishing", "4 · Adept", "#4a4643", "taking root"),
    ("V", "Splintering", "5 · Expert", "url(#splinter)", "the cracking"),
    ("VI", "Glory", "5 · Expert", "#7b7672", "being lit"),
    ("VII", "Refraction", "5 · Expert", "url(#refract)", "the double sight"),
    ("VIII", "Transcendence", "6 · Master", "#bdb3a2", ""),
    ("IX", "Invocation", "6 · Master", "url(#invoke)", ""),
    ("X", "Realization", "6 · Master", "#e6d7ae", ""),
    ("XI", "Dissonance", "7 · Grandmaster", "#f3dc8e", ""),
    ("XII", "Emanation", "7 · Grandmaster", "#f6ecd0", ""),
    ("XIII", "Principality", "8 · Archmaster", "#faf5e6", ""),
    ("XIV", "Zenith", "8 · Archmaster", "#fdfaf0", ""),
    ("XV", "Revelation", "9 · Paragon", "url(#reveal)", ""),
    ("XVI", "Apex", "9 · Paragon", "#ffffff", ""),
]
BANDS = [("I", "Mortal Foundation", 0, 4), ("II", "Awakened", 4, 7), ("III", "Sovereign", 7, 10),
         ("IV", "Mythic", 10, 12), ("V", "Absolute", 12, 14), ("", "The Apotheosis Approach", 14, 16)]
MARKS = {3: "First Release", 6: "Second Release · Domain", 8: "Third Release"}
GATES = {4: "Level 100 gate", 7: "Level 200 gate", 10: "Level 300 gate", 12: "Level 400 gate"}


def stage_ladder():
    W, top, rh = 1000, 140, 46
    H = top + rh * 16 + 70
    o = _frame(W, H, "The Sixteen Stages", "The climb, top to foot; each swatch is the Essence's colour at that Stage")
    o.insert(1, f'<defs><linearGradient id="splinter" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b3735"/><stop offset=".48" stop-color="#3b3735"/><stop offset=".5" stop-color="{GOLD}"/><stop offset=".53" stop-color="#3b3735"/><stop offset="1" stop-color="#3b3735"/></linearGradient>'
                f'<linearGradient id="refract" x1="0" x2="1"><stop offset=".5" stop-color="#8a8580"/><stop offset=".5" stop-color="{GOLD}"/></linearGradient>'
                f'<linearGradient id="invoke" x1="0" x2="1"><stop offset="0" stop-color="#5bb0ff"/><stop offset=".22" stop-color="#e9dcb4"/><stop offset=".78" stop-color="#e9dcb4"/><stop offset="1" stop-color="#5bb0ff"/></linearGradient>'
                f'<linearGradient id="reveal" x1="0" x2="1"><stop offset="0" stop-color="#ffd9d9"/><stop offset=".33" stop-color="#fff9d9"/><stop offset=".66" stop-color="#d9fff1"/><stop offset="1" stop-color="#e3dcff"/></linearGradient></defs>')
    o.append(t(150, top - 12, "STAGE", 14, MUTED, extra='letter-spacing="2"'))
    o.append(t(585, top - 12, "TIER OF STANDING", 14, MUTED, extra='letter-spacing="2"'))
    o.append(t(742, top - 12, "WHAT OPENS", 14, MUTED, extra='letter-spacing="2"'))
    for b, (num, name, a, z) in enumerate(BANDS):
        y0, y1 = top + a * rh, top + z * rh
        o.append(f'<rect x="30" y="{y0 + 3}" width="92" height="{y1 - y0 - 6}" rx="6" fill="{GOLD}" fill-opacity="{.05 + .03 * b:.2f}" stroke="{GOLD}" stroke-opacity=".35"/>')
        cy = (y0 + y1) / 2
        label = f"Band {num}" if num else "Beyond"
        o.append(t(76, cy - 4, label, 15, GOLD, "middle", "600"))
        words = name.split()
        for i, wd in enumerate(words[:3]):
            o.append(t(76, cy + 14 + i * 15, wd, 12, MUTED, "middle", italic=True, font=BODY))
    for i, (num, name, tier, col, street) in enumerate(STAGES):
        y = top + i * rh
        if i % 2:
            o.append(f'<rect x="130" y="{y}" width="{W - 160}" height="{rh}" fill="#ffffff" fill-opacity=".025"/>')
        cy = y + rh / 2
        o.append(t(178, cy + 7, num, 20, GOLD, "end", "600"))
        o.append(f'<polygon points="208,{cy - 15} 222,{cy} 208,{cy + 15} 194,{cy}" fill="{col}" stroke="{GOLD}" stroke-width="1.4"/>')
        o.append(t(240, cy + 7, name, 22, TEXT, weight="600"))
        if street:
            o.append(t(400, cy + 6, f"“{street}”", 15, MUTED, italic=True, font=BODY))
        o.append(t(585, cy + 6, tier, 17, TEXT, font=BODY))
        if i in MARKS:
            o.append(f'<rect x="742" y="{cy - 14}" width="{22 + 7.4 * len(MARKS[i]):.0f}" height="28" rx="14" fill="{GOLD}" fill-opacity=".16" stroke="{GOLD}" stroke-opacity=".7"/>')
            o.append(t(753, cy + 5, MARKS[i], 15, GOLD, weight="600"))
    for i, g in GATES.items():
        y = top + i * rh
        o.append(f'<line x1="130" y1="{y}" x2="{W - 30}" y2="{y}" stroke="#e2603a" stroke-width="1.6" stroke-dasharray="7 5" stroke-opacity=".85"/>')
        o.append(f'<rect x="{W - 172}" y="{y - 11}" width="140" height="22" rx="4" fill="{INK}"/>')
        o.append(t(W - 36, y + 5, g, 14, "#f0906a", "end", "600"))
    o.append(t(W / 2, H - 30, "Pressure: one Stage up bends attention · two brings sweat and nausea · three drops people", 16, MUTED, "middle", italic=True, font=BODY))
    o.append("</svg>")
    return "".join(o)


def crystal_layers():
    W, H = 1000, 620
    o = _frame(W, H, "The Soul Crystal", "Three layers, one for each plane; every working crosses all three")
    o.insert(1, f'<defs><radialGradient id="core" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#fff2c4"/><stop offset=".35" stop-color="{GOLD}"/><stop offset="1" stop-color="#6b3f10"/></radialGradient>'
                f'<linearGradient id="shell" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9fd6ff" stop-opacity=".35"/><stop offset="1" stop-color="#3a5a9a" stop-opacity=".12"/></linearGradient></defs>')
    cx, cy = 290, 360
    for k in range(9):  # fate threads
        a = math.radians(k * 40 + 12)
        x1, y1 = cx + 150 * math.cos(a), cy + 150 * math.sin(a)
        x2, y2 = cx + 228 * math.cos(a + .25), cy + 210 * math.sin(a + .25)
        o.append(f'<path d="M{x1:.0f} {y1:.0f} Q{cx + 205 * math.cos(a):.0f} {cy + 190 * math.sin(a):.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="#c89bff" stroke-opacity=".55" stroke-width="1.3"/>')
        o.append(f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="4.5" fill="#c89bff" fill-opacity=".8"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="160" fill="none" stroke="#c89bff" stroke-opacity=".7" stroke-width="2" stroke-dasharray="3 7"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="178" fill="none" stroke="#c89bff" stroke-opacity=".25"/>')
    pts = [(cx, cy - 128), (cx + 92, cy - 52), (cx + 76, cy + 74), (cx, cy + 128), (cx - 76, cy + 74), (cx - 92, cy - 52)]
    o.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in pts) + f'" fill="url(#shell)" stroke="#9fd6ff" stroke-width="2.4"/>')
    for x, y in pts:
        o.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#9fd6ff" stroke-opacity=".22"/>')
    o.append(f'<polygon points="{cx},{cy - 54} {cx + 38},{cy - 8} {cx + 24},{cy + 40} {cx},{cy + 56} {cx - 24},{cy + 40} {cx - 38},{cy - 8}" fill="url(#core)" stroke="#fff2c4" stroke-width="1.5"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="{GOLD}" fill-opacity=".08"/>')
    rows = [
        (180, "#c89bff", "Attraction Layer", "Plane of Fate", "Bonds, Domains, harmonisations: what a soul is tied to.", (cx + 160, cy - 20)),
        (330, "#9fd6ff", "Aether Shell", "Material Plane", "The skin power passes through on the way out. Its clarity is the Aether Class, which sets η.", (cx + 92, cy - 52)),
        (480, GOLD, "Essence Core", "Soul Plane", "Identity, memory and Traits: the soul’s own standing law.", (cx + 30, cy + 10)),
    ]
    for y, col, name, plane, what, (px, py) in rows:
        o.append(f'<path d="M{px} {py} L540 {y + 18} L560 {y + 18}" fill="none" stroke="{col}" stroke-opacity=".6"/>')
        o.append(f'<circle cx="{px}" cy="{py}" r="4" fill="{col}"/>')
        o.append(f'<rect x="560" y="{y - 22}" width="400" height="104" rx="10" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".55"/>')
        o.append(t(582, y + 8, name, 26, col, weight="600"))
        o.append(t(940, y + 8, plane, 16, MUTED, "end", italic=True, font=BODY))
        words, line, ly = what.split(), "", y + 38
        for wd in words:
            if len(line) + len(wd) > 46:
                o.append(t(582, ly, line.strip(), 17, TEXT, font=BODY)); line, ly = "", ly + 22
            line += wd + " "
        o.append(t(582, ly, line.strip(), 17, TEXT, font=BODY))
    o.append("</svg>")
    return "".join(o)


FAMILIES = [("Caloria", "Thermodynamics", "#e0702a", "ember-orange"), ("Fulguria", "Electromagnetism", "#4aa8ff", "arc-discharge blue"),
            ("Vectoria", "Mechanics", "#7d848b", "iron to gunmetal"), ("Spatium", "Spatial Geometry", "#7a4cf0", "deep violet"),
            ("Materia", "Material Science", "#c8892f", "ochre to amber"), ("Vitalia", "Biochemistry", "#c0283a", "arterial red"),
            ("Fluxia", "Fluid Dynamics", "#14918c", "deep teal"), ("Limina", "Entropy, Void and Mind", "#4a2466", "black-violet")]


def families_wheel():
    W, H = 1000, 960
    o = _frame(W, H, "The Eight Families", "Sixty Wellsprings, each a law of nature, gathered by the science they condition")
    cx, cy, R, r0 = 500, 540, 270, 110
    for i, (name, dom, col, hue) in enumerate(FAMILIES):
        a0, a1 = math.radians(i * 45 - 112.5), math.radians(i * 45 - 67.5)
        p = lambda rr, a: (cx + rr * math.cos(a), cy + rr * math.sin(a))
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p(R, a0), p(R, a1), p(r0, a1), p(r0, a0)
        o.append(f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 1 {x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} A{r0} {r0} 0 0 0 {x3:.1f} {y3:.1f} Z" fill="{col}" fill-opacity=".82" stroke="{INK}" stroke-width="4"/>')
        am = (a0 + a1) / 2
        ix, iy = p((R + r0) / 2, am)
        o.append(crest_family(i, ix, iy))
        lx, ly = p(R + 70, am)
        anchor = "middle" if abs(math.cos(am)) < .3 else ("start" if math.cos(am) > 0 else "end")
        lx += 0 if anchor == "middle" else (-30 if anchor == "start" else 30)
        o.append(t(lx, ly - 4, name, 28, col if name != "Limina" else "#b38ad6", anchor, "600"))
        o.append(t(lx, ly + 20, dom, 17, TEXT, anchor, font=BODY))
        o.append(t(lx, ly + 40, hue, 15, MUTED, anchor, italic=True, font=BODY))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r0 - 6}" fill="{INK}" stroke="{GOLD}" stroke-width="2"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 10}" fill="none" stroke="{GOLD}" stroke-opacity=".5"/>')
    o.append(t(cx, cy - 8, "SIXTY", 30, GOLD, "middle", "700", extra='letter-spacing="3"'))
    o.append(t(cx, cy + 22, "Wellsprings", 22, TEXT, "middle", italic=True))
    o.append("</svg>")
    return "".join(o)


def crest_family(i, x, y):
    """A small mark for each Family, white on its wedge."""
    m = ["M0 -16 Q10 -4 4 6 Q12 2 10 -6 Q18 8 0 18 Q-18 8 -10 -6 Q-12 2 -4 6 Q-10 -4 0 -16 Z",  # flame
         "M4 -18 L-8 2 L2 2 L-4 18 L10 -4 L0 -4 Z",  # bolt
         "M-16 0 L10 0 M4 -7 L12 0 L4 7 M-16 -10 L-6 -10 M-16 10 L-6 10",  # vector
         "M-14 -14 L14 -14 L14 14 L-14 14 Z M-14 -14 L0 -4 L14 -14 M0 -4 L0 14",  # folded space
         "M-16 8 L0 -14 L16 8 Z M-8 8 L0 -3 L8 8",  # stone
         "M0 -16 C14 -4 12 10 0 16 C-12 10 -14 -4 0 -16 Z M0 -4 L0 10",  # drop of blood / seed
         "M-18 -4 Q-9 -12 0 -4 Q9 4 18 -4 M-18 8 Q-9 0 0 8 Q9 16 18 8",  # waves
         "M0 -16 A16 16 0 1 0 0 16 A10 10 0 1 1 0 -16 Z"]  # eclipse
    return f'<path d="{m[i]}" transform="translate({x:.1f} {y:.1f}) scale(1.5)" fill="none" stroke="#fff8ea" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" opacity=".92"/>'


GRADES = [("Hollow", "1–10"), ("F", "11–25"), ("E", "26–50"), ("D", "51–100"), ("C", "101–175"), ("B", "176–275"),
          ("A", "276–400"), ("S", "401–550"), ("SS", "551–725"), ("SSS", "726–950"), ("X", "951–1,200"), ("EX", "1,201–1,500"), ("EX+", "1,501 and up")]


def grade_ladder():
    W, top, rh = 1000, 130, 38
    H = top + rh * 13 + 120
    o = _frame(W, H, "Grades", "The letter on a Sub-Stat’s number: how much that one ability delivers")
    for i, (g, rng) in enumerate(GRADES):
        y = top + i * rh
        up = int(rng.replace(",", "").split("–")[-1].split()[0]) if "–" in rng else 1800
        frac = math.log10(up) / math.log10(1800)
        col = f"hsl({30 + i * 2}, {55 + i * 3}%, {28 + i * 4.2}%)"
        o.append(t(120, y + 26, g, 22, GOLD, "end", "700"))
        o.append(f'<rect x="140" y="{y + 7}" width="{frac * 620:.0f}" height="{rh - 12}" rx="5" fill="{col}" stroke="{GOLD}" stroke-opacity=".45"/>')
        o.append(t(150 + frac * 620, y + 25, rng, 17, TEXT, font=BODY))
    y = top + 13 * rh + 26
    for k, (head, body) in enumerate((("One Grade up", "wins the exchange outright"), ("Two Grades", "is one-sided"), ("Three Grades", "is an event the lower side survives"))):
        x = 70 + k * 300
        o.append(f'<rect x="{x}" y="{y}" width="270" height="62" rx="8" fill="{GOLD}" fill-opacity=".08" stroke="{GOLD}" stroke-opacity=".5"/>')
        o.append(t(x + 135, y + 26, head, 20, GOLD, "middle", "600"))
        o.append(t(x + 135, y + 48, body, 16, TEXT, "middle", font=BODY))
    o.append("</svg>")
    return "".join(o)


def reserve_tells():
    W, H = 1000, 520
    o = _frame(W, H, "Reading the Reserve", "The body tells on the reserve, and the ladder is the same for everyone")
    o.insert(1, f'<defs><linearGradient id="res" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}"/><stop offset=".55" stop-color="#b3742a"/><stop offset=".85" stop-color="#7a3a1e"/><stop offset="1" stop-color="#3a1712"/></linearGradient></defs>')
    x0, x1, y = 70, 930, 150
    o.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="26" rx="13" fill="url(#res)" stroke="{GOLD}" stroke-opacity=".7"/>')
    steps = [(0, "Full", "The aura bright in its own colour; breath easy.", 1.0),
             (.5, "Half", "Breath shortens and stays short. The aura dims, as if a hand cupped the lamp.", .7),
             (.75, "A quarter", "A tremor in the hands and knees. The colour thins toward grey; the edges fray.", .45),
             (.9, "A tenth", "The aura flickers like a lamp on a failing main. Traits stutter: late, half, or not at all.", .25),
             (1.0, "Starvation", "The coat fails and the base stats sag. The Shell degrades.", .08)]
    cols = [70, 250, 430, 610, 790]
    for (f, head, body, glow), cx in zip(steps, cols):
        mx = x0 + f * (x1 - x0)
        o.append(f'<line x1="{mx}" y1="{y - 10}" x2="{mx}" y2="{y + 36}" stroke="{TEXT}" stroke-width="2"/>')
        o.append(f'<path d="M{mx} {y + 36} L{cx + 85} 232" stroke="{GOLD}" stroke-opacity=".35" fill="none"/>')
        dash = 'stroke-dasharray="4 4"' if f >= .9 else ""
        o.append(f'<circle cx="{cx + 85}" cy="262" r="26" fill="{GOLD}" fill-opacity="{glow * .5:.2f}" stroke="{GOLD}" stroke-opacity="{glow:.2f}" stroke-width="3" {dash}/>')
        o.append(f'<circle cx="{cx + 85}" cy="262" r="9" fill="#fff2c4" fill-opacity="{glow:.2f}"/>')
        o.append(t(cx + 85, 320, head, 22, GOLD, "middle", "600"))
        words, line, ly = body.split(), "", 348
        for wd in words:
            if len(line) + len(wd) > 21:
                o.append(t(cx + 85, ly, line.strip(), 15, TEXT, "middle", font=BODY)); line, ly = "", ly + 20
            line += wd + " "
        o.append(t(cx + 85, ly, line.strip(), 15, TEXT, "middle", font=BODY))
    o.append(t(W / 2, H - 28, "Maxing out shows heat first, then blood, then a cracking aura. Waste is loud and hot; mastery is quiet.", 16, MUTED, "middle", italic=True, font=BODY))
    o.append("</svg>")
    return "".join(o)


def release_forms():
    W, H = 1000, 660
    o = _frame(W, H, "The Three Releases", "The soul’s standing law let off its limit, in a learned shape")
    cols = [("First Release", "From Stage IV · Flourishing", "The body", "One signature change to the body or the weapon.",
             "The Trait strikes at the top of its Grade.", "Spent and shaking; the pain arrives.", 1),
            ("Second Release", "From Stage VII · Refraction", "The field", "The change spreads into the ground around them; the Domain opens.",
             "Inside the field, one full Grade higher.", "The Crystal runs Overgrown until a full night’s sleep.", 2),
            ("Third Release", "From Stage IX · Invocation", "The law", "A field that can hold other fields inside it.",
             "The Trait’s effect becomes local law, two Grades over base.", "Held past the limit, the Trait itself may fail.", 3)]
    for i, (name, when, reach, look, power, after, n) in enumerate(cols):
        x = 50 + i * 310
        lift = (2 - i) * 40
        o.append(f'<rect x="{x}" y="{130 + lift}" width="280" height="{490 - lift}" rx="12" fill="{GOLD}" fill-opacity="{.05 + i * .04:.2f}" stroke="{GOLD}" stroke-opacity=".55"/>')
        cx, cy = x + 140, 210 + lift
        for k in range(n):
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{18 + k * 18}" fill="none" stroke="{GOLD}" stroke-opacity="{.85 - k * .22:.2f}" stroke-width="{2.4 - k * .5:.1f}"/>')
        o.append(f'<polygon points="{cx},{cy - 11} {cx + 8},{cy} {cx},{cy + 11} {cx - 8},{cy}" fill="#fff2c4"/>')
        y = 300 + lift
        o.append(t(cx, y, name, 26, GOLD, "middle", "600"))
        o.append(t(cx, y + 24, when, 15, MUTED, "middle", italic=True, font=BODY))
        o.append(t(cx, y + 52, reach.upper(), 14, TEXT, "middle", "600", extra='letter-spacing="3"'))
        ly = y + 78
        for txt, col in ((look, TEXT), (power, "#f0d48a"), (after, MUTED)):
            words, line = txt.split(), ""
            for wd in words:
                if len(line) + len(wd) > 30:
                    o.append(t(cx, ly, line.strip(), 15, col, "middle", font=BODY)); line, ly = "", ly + 19
                line += wd + " "
            o.append(t(cx, ly, line.strip(), 15, col, "middle", font=BODY)); ly += 28
    o.append("</svg>")
    return "".join(o)


def stack_cap():
    W, H = 1000, 660
    o = _frame(W, H, "Stacking", "Every boost of one’s own counts toward a single cap: two Grades over sustainable")
    layers = [("Base stats", "the body’s passive floor, always on", "#5a4630"),
              ("The coat", "active reinforcement, bought with reserve", "#7a5a30"),
              ("Focus", "the coat gathered to one place: +1 Grade there", "#94702f"),
              ("A vow", "to the top of the band; a great vow, one Grade", "#b0852f"),
              ("A release", "First to the top, Second +1, Third +2 for one effect", "#c99a3a"),
              ("A Draft or an overchannel", "as graded; overchannel always damages", "#e0b04f")]
    x, w, y, h = 90, 520, 520, 58
    for i, (name, what, col) in enumerate(layers):
        yy = y - i * (h + 6)
        o.append(f'<rect x="{x + i * 10}" y="{yy}" width="{w - i * 20}" height="{h}" rx="8" fill="{col}" fill-opacity=".85" stroke="{GOLD}" stroke-opacity=".5"/>')
        o.append(t(x + 24 + i * 10, yy + 26, name, 21, "#fff6e0", weight="600"))
        o.append(t(x + 24 + i * 10, yy + 47, what, 15, "#fbecd0", font=BODY))
    capy = y - 6 * (h + 6) + h - 4
    o.append(f'<line x1="60" y1="{capy}" x2="{x + w + 30}" y2="{capy}" stroke="#e2603a" stroke-width="2.5" stroke-dasharray="9 6"/>')
    o.append(t(64, capy - 10, "THE CAP · +2 GRADES OVER SUSTAINABLE", 15, "#f0906a", weight="700", extra='letter-spacing="2"'))
    o.append(f'<rect x="680" y="200" width="270" height="250" rx="12" fill="#14918c" fill-opacity=".14" stroke="#3fd0c0" stroke-opacity=".7"/>')
    o.append(t(815, 236, "Help from outside", 24, "#7fe6da", "middle", "600"))
    for k, line in enumerate(("An ally’s working, a standing", "array, a Domain someone", "else holds.", "", "Stacks freely, above the cap,", "and adds no risk to the", "one receiving it.")):
        o.append(t(815, 270 + k * 24, line, 17, TEXT, "middle", font=BODY))
    o.append(t(W / 2, H - 22, "Each layer stacked at once raises the risk of a Crystal Fracture Event. Two is a gamble veterans take.", 16, MUTED, "middle", italic=True, font=BODY))
    o.append("</svg>")
    return "".join(o)


DIAGRAM_FILES = {
    "stage-ladder.svg": stage_ladder, "soul-crystal.svg": crystal_layers, "eight-families.svg": families_wheel,
    "grades.svg": grade_ladder, "reserve-tells.svg": reserve_tells, "release-forms.svg": release_forms,
    "stacking.svg": stack_cap,
}

if __name__ == "__main__":
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAM_FILES.items():
        (DIAGRAMS / name).write_text(fn(), encoding="utf-8")
        print("wrote", DIAGRAMS / name)
