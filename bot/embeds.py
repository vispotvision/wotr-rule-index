"""Renderers: search hits, a character card, a name card, a stat block, long text as
pages, and the views that turn pages or open a hit."""
import discord

DESC_MAX = 4096
FIELD_MAX = 1024
C_WIKI, C_CARD, C_SCENE, C_NAME, C_STAT, C_WARN = 0x5C6BC0, 0x8E24AA, 0x00897B, 0xD4A017, 0xC0392B, 0xE67E22


def _clip(s: str, n: int) -> str:
    s = s or ""
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def footer(e: discord.Embed, text: str) -> discord.Embed:
    e.set_footer(text=_clip(text, 2048))
    return e


# -- long text ----------------------------------------------------------------

def pages(text: str, size: int, title: str = "", colour: int = C_WIKI, url: str | None = None,
          footer_text: str = "", author: str = "") -> list[discord.Embed]:
    """Split text on line boundaries into embeds of at most `size` characters."""
    text = (text or "").strip() or "(nothing)"
    chunks, cur = [], ""
    for line in text.split("\n"):
        while len(line) > size:  # a single over-long line is cut hard
            if cur:
                chunks.append(cur)
                cur = ""
            chunks.append(line[:size])
            line = line[size:]
        if len(cur) + len(line) + 1 > size:
            chunks.append(cur)
            cur = line
        else:
            cur = f"{cur}\n{line}" if cur else line
    if cur:
        chunks.append(cur)
    out = []
    for i, ch in enumerate(chunks, 1):
        e = discord.Embed(title=_clip(title, 256) or None, description=ch, colour=colour, url=url)
        if author:
            e.set_author(name=_clip(author, 256))
        tail = f"page {i}/{len(chunks)}" if len(chunks) > 1 else ""
        footer(e, " · ".join(x for x in (footer_text, tail) if x))
        out.append(e)
    return out


class Pager(discord.ui.View):
    """◀ ▶ over a list of embeds. Anyone may turn the pages."""

    def __init__(self, embeds: list[discord.Embed], timeout: float = 900):
        super().__init__(timeout=timeout)
        self.embeds, self.i = embeds, 0
        if len(embeds) <= 1:
            self.clear_items()

    async def _show(self, itx: discord.Interaction):
        await itx.response.edit_message(embed=self.embeds[self.i], view=self)

    @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def prev(self, itx: discord.Interaction, _: discord.ui.Button):
        self.i = (self.i - 1) % len(self.embeds)
        await self._show(itx)

    @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def next(self, itx: discord.Interaction, _: discord.ui.Button):
        self.i = (self.i + 1) % len(self.embeds)
        await self._show(itx)

    async def on_timeout(self):
        self.clear_items()


async def send_pages(itx: discord.Interaction, embeds: list[discord.Embed], ephemeral: bool = False):
    view = Pager(embeds)
    if itx.response.is_done():
        await itx.followup.send(embed=embeds[0], view=view, ephemeral=ephemeral)
    else:
        await itx.response.send_message(embed=embeds[0], view=view, ephemeral=ephemeral)


# -- search hits ---------------------------------------------------------------

def hits_embed(query: str, hits: list[dict], kind: str, commit: str) -> discord.Embed:
    """One embed, one field per hit: title, where it lives, a highlighted snippet."""
    e = discord.Embed(title=_clip(f"{'Wiki' if kind == 'wiki' else 'Scenes'}: {query}", 256),
                      colour=C_WIKI if kind == "wiki" else C_SCENE)
    if not hits:
        e.description = f"Nothing matches **{query}**."
        return e
    for i, h in enumerate(hits, 1):
        where = h.get("category") or h.get("file", "")
        link = f" · [Notion]({h['url']})" if h.get("url") else ""
        e.add_field(name=_clip(f"{i}. {h['title']}", 256),
                    value=_clip(f"-# {where}{link}\n{h['snippet']}", FIELD_MAX), inline=False)
    footer(e, f"pick a number below to open it · {'wiki mirror, up to an hour behind Notion' if kind == 'wiki' else 'scene archive'} · @ {commit}")
    return e


class OpenHit(discord.ui.View):
    """A select over the hits; choosing one replaces the message with that page, paged."""

    def __init__(self, hits: list[dict], opener, timeout: float = 900):
        super().__init__(timeout=timeout)
        self.hits, self.opener = hits, opener
        sel = discord.ui.Select(placeholder="Open a result…", options=[
            discord.SelectOption(label=_clip(f"{i}. {h['title']}", 100), value=str(i - 1),
                                 description=_clip(h.get("category") or h.get("file", ""), 100) or None)
            for i, h in enumerate(hits, 1)])
        sel.callback = self.choose
        self.add_item(sel)

    async def choose(self, itx: discord.Interaction):
        h = self.hits[int(itx.data["values"][0])]
        embeds = await self.opener(h)
        pager = Pager(embeds)
        await itx.response.edit_message(embed=embeds[0], view=pager)

    async def on_timeout(self):
        self.clear_items()


# -- names ---------------------------------------------------------------------

def name_embed(d: dict, label: str) -> discord.Embed:
    e = discord.Embed(title=_clip(d["name"], 256), description=_clip(d["note"], DESC_MAX), colour=C_NAME)
    e.set_author(name=_clip(label, 256))
    for lab, txt in d["lines"]:
        e.add_field(name=_clip(lab, 256), value=_clip(txt, FIELD_MAX), inline=False)
    if d.get("flags"):
        e.add_field(name="Flags", value=_clip("\n".join(f"• {f}" for f in d["flags"]), FIELD_MAX), inline=False)
    footer(e, f"elements from {d['rule']} · Naming Guide 2026-09-12 edition · 🎲 for another")
    return e


class Reroll(discord.ui.View):
    """One button that calls `again()` and swaps the embed."""

    def __init__(self, again, timeout: float = 900):
        super().__init__(timeout=timeout)
        self.again = again

    @discord.ui.button(label="🎲 another", style=discord.ButtonStyle.primary)
    async def roll(self, itx: discord.Interaction, _: discord.ui.Button):
        await itx.response.edit_message(embed=await self.again(), view=self)

    async def on_timeout(self):
        self.clear_items()


# -- stats ---------------------------------------------------------------------

def stat_embed(d: dict) -> discord.Embed:
    st, band = d["stage"], d["band"]
    e = discord.Embed(title=f"Level {d['level']} · Stage {st['roman']} — {st['name']}", colour=C_STAT)
    e.set_author(name=f"Band {band['name']} · {st['standing']}" if st.get("standing") else f"Band {band['name']}")
    lines = [f"Max Grade **{st['max_grade']}** — a Sub-Stat holds at most **{d['grade_top']:,}** (R39-4); the Stage ceiling of {st['ceiling']:,} is the instability zone",
             f"Pool **{d['pool']:,}** ({d['lvl_pts']:,} levelling + {d['thr_pts']:,} Thresholds) · spent **{d['spent']:,}** on Sub-Stats",
             f"Leaning **{d['lean']}**"]
    if d["unheld"]:
        lines.append(f"⚠ **{d['unheld']:,}** points the Crystal cannot hold at this Stage; they sit aside")
    e.description = _clip(chr(10).join(lines), DESC_MAX)
    for r in d["rows"]:
        subs = " · ".join(f"{s} {v:,}" if v is not None else f"{s} —" for s, v in r["entries"])
        marks = (" ⚠ above the Stage's grade" if r["over"] else "") + (f" ⚠ unstable: {', '.join(r['unstable'])}" if r["unstable"] else "")
        e.add_field(name=_clip(f"{r['primary']} — {r['total']:,} · mean {r['mean']:,.0f} · {r['grade']}-Grade{marks}", 256),
                    value=_clip(subs, FIELD_MAX), inline=False)
    if d["flags"]:
        e.add_field(name="Flags", value=_clip(chr(10).join(f"• {f}" for f in d["flags"]), FIELD_MAX), inline=False)
    return e


# -- FOW line ------------------------------------------------------------------

HEADLINE = ("Level", "Level-Band", "Band", "Stage", "Temperance Stage", "Coherence Band", "Aether Class", "Soul Crystal Tier")


def fow_embed(d: dict) -> discord.Embed:
    e = discord.Embed(title=_clip(f"FOW line — {d['title']}", 256), url=d.get("url"), colour=C_STAT)
    if d.get("category"):
        e.set_author(name=_clip(d["category"], 256))
    if d["empty"]:
        e.description = "This card carries no FOW figures. Flag an estimate in a character's mouth or ask Isaac — the bot will not invent one."
        return footer(e, "from the card only")
    head = [f for f in d["facts"] if f[0] in HEADLINE]
    rest = [f for f in d["facts"] if f[0] not in HEADLINE]
    e.description = _clip("\n".join(f"**{k}** · {v}" for k, v in head), DESC_MAX) or None
    for r in d["rows"]:
        e.add_field(name=_clip(f"{r['primary']} — {r['value']} · {r['grade']}", 256), value=_clip(r["peaks"] or "—", FIELD_MAX), inline=True)
    if rest:
        e.add_field(name="Force and flow", value=_clip("\n".join(f"**{k}** · {v}" for k, v in rest[:8]), FIELD_MAX), inline=False)
    if d["notes"]:
        e.add_field(name="The card's own words", value=_clip("\n".join(f"> {n}" for n in d["notes"]), FIELD_MAX), inline=False)
    return footer(e, "from the card only; the bot never estimates a number" + (" · title links to Notion" if d.get("url") else ""))


# -- character cards -----------------------------------------------------------

def card_overview(d: dict, page: int) -> discord.Embed:
    e = discord.Embed(title=_clip(d["title"], 256), url=d.get("url"), colour=C_CARD,
                      description=_clip(d["overview"], min(page, 1800)) or None)
    if d.get("category"):
        e.set_author(name=_clip(d["category"], 256))
    for k, v in d["facts"]:
        e.add_field(name=_clip(k, 256), value=_clip(v, FIELD_MAX), inline=len(v) <= 40)
    if d["sections"]:
        e.add_field(name="Sections", value=_clip("\n".join(f"{i}. {h}" for i, (h, _) in enumerate(d["sections"], 1)), FIELD_MAX), inline=False)
    also = f" · also matched: {', '.join(d['also'])}" if d.get("also") else ""
    footer(e, ("title links to Notion" if d.get("url") else "wiki mirror") + " · jump to a section below" + also)
    return e


class CardView(discord.ui.View):
    """Overview + a section picker; ◀ ▶ page within a long section."""

    def __init__(self, d: dict, page: int, timeout: float = 900):
        super().__init__(timeout=timeout)
        self.d, self.page = d, page
        self.section, self.i = -1, 0
        self.pages: list[discord.Embed] = [card_overview(d, page)]
        opts = [discord.SelectOption(label="Overview", value="-1", emoji="🃏")]
        opts += [discord.SelectOption(label=_clip(f"{i}. {h}", 100), value=str(i - 1)) for i, (h, _) in enumerate(d["sections"][:24], 1)]
        sel = discord.ui.Select(placeholder="Jump to a section…", options=opts, row=0)
        sel.callback = self.jump
        self.add_item(sel)
        self._buttons()

    def _buttons(self):
        for item in list(self.children):
            if isinstance(item, discord.ui.Button):
                self.remove_item(item)
        if len(self.pages) > 1:
            prev = discord.ui.Button(label="◀", style=discord.ButtonStyle.secondary, row=1)
            nxt = discord.ui.Button(label="▶", style=discord.ButtonStyle.secondary, row=1)
            prev.callback, nxt.callback = self.prev, self.next
            self.add_item(prev)
            self.add_item(nxt)

    def _section_pages(self, n: int) -> list[discord.Embed]:
        h, body = self.d["sections"][n]
        return pages(body, self.page, title=f"{self.d['title']} — {h}", url=self.d.get("url"), author=self.d.get("category", ""),
                     colour=C_CARD, footer_text=f"section {n + 1}/{len(self.d['sections'])}")

    async def jump(self, itx: discord.Interaction):
        self.section = int(itx.data["values"][0])
        self.i = 0
        self.pages = [card_overview(self.d, self.page)] if self.section < 0 else self._section_pages(self.section)
        self._buttons()
        await itx.response.edit_message(embed=self.pages[0], view=self)

    async def prev(self, itx: discord.Interaction):
        self.i = (self.i - 1) % len(self.pages)
        await itx.response.edit_message(embed=self.pages[self.i], view=self)

    async def next(self, itx: discord.Interaction):
        self.i = (self.i + 1) % len(self.pages)
        await itx.response.edit_message(embed=self.pages[self.i], view=self)

    async def on_timeout(self):
        self.clear_items()
