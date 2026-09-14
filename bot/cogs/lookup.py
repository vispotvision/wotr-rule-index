"""Read-only lookups: the wiki mirror, character cards, FOW lines, the scene archive."""
import asyncio

import discord
from discord import app_commands
from discord.ext import commands

import card as C
import define as D
import embeds as E
import wotr as W


class Lookup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.page = int(bot.cfg.get("page_size", 3600))

    async def ac_name(self, itx: discord.Interaction, current: str):
        names = await asyncio.to_thread(W.character_names, current)
        return [app_commands.Choice(name=n[:100], value=n[:100]) for n in names]

    # -- wiki -------------------------------------------------------------------

    async def _open_wiki(self, h: dict) -> list[discord.Embed]:
        title, text, url, cat = await asyncio.to_thread(W.wiki_page, h["rel"])
        return E.pages(text, self.page, title=title, url=url, author=cat, colour=E.C_WIKI,
                       footer_text="wiki mirror" + (" · title links to Notion" if url else ""))

    @app_commands.command(name="wiki", description="Search the lore wiki. Pick a result to read the whole page.")
    @app_commands.describe(query="What to look for, e.g. Soul Crystal, Kharven, the Accord")
    async def wiki(self, itx: discord.Interaction, query: str):
        await itx.response.defer()
        hits = await asyncio.to_thread(W.wiki_hits, query)
        e = E.hits_embed(query, hits, "wiki", W.commit_hash())
        await itx.followup.send(embed=e, view=E.OpenHit(hits, self._open_wiki) if hits else None)

    @app_commands.command(name="define", description="What a word or term means, from where the wiki defines it.")
    @app_commands.describe(term="The word or phrase, e.g. Soul Crystal, Temperance, the Waiting")
    async def define(self, itx: discord.Interaction, term: str):
        await itx.response.defer()
        hits = await asyncio.to_thread(D.lookup, term)
        e = discord.Embed(title=E._clip(term, 256), colour=E.C_WIKI)
        if hits:
            for h in hits:
                link = f" · [Notion]({h['url']})" if h["url"] else ""
                e.add_field(name=E._clip(h["page"], 256), value=E._clip(f"-# {h['category']}{link}" + chr(10) + h['text'], E.FIELD_MAX), inline=False)
            E.footer(e, "the wiki's own defining lines, verbatim · /wiki for wider search")
            return await itx.followup.send(embed=e)
        ment = await asyncio.to_thread(D.mentions, term)
        if not ment:
            return await itx.followup.send(f"The wiki neither defines nor mentions **{term}**.", ephemeral=True)
        e.description = f"No page defines **{term}** outright. Where it appears:"
        for h in ment:
            link = f" · [Notion]({h['url']})" if h["url"] else ""
            e.add_field(name=E._clip(h["title"], 256), value=E._clip(f"-# {h['category']}{link}" + chr(10) + h['snippet'], E.FIELD_MAX), inline=False)
        E.footer(e, "mentions only · /wiki to open a page")
        await itx.followup.send(embed=e)

    # -- characters --------------------------------------------------------------

    @app_commands.command(name="character", description="A character's card: overview, key facts, and every section.")
    @app_commands.describe(name="Character name")
    @app_commands.autocomplete(name=ac_name)
    async def character(self, itx: discord.Interaction, name: str):
        await itx.response.defer()
        d = await asyncio.to_thread(C.load, name)
        if not d:
            return await itx.followup.send(f"No card for **{name}** in the wiki mirror. Check Notion before writing anything numeric about them.", ephemeral=True)
        view = E.CardView(d, self.page)
        await itx.followup.send(embed=view.pages[0], view=view)

    @app_commands.command(name="fow", description="A character's Fracture of Worlds line, from their card only.")
    @app_commands.describe(name="Character name")
    @app_commands.autocomplete(name=ac_name)
    async def fow(self, itx: discord.Interaction, name: str):
        await itx.response.defer()
        d = await asyncio.to_thread(C.fow, name)
        if not d:
            return await itx.followup.send(f"No card for **{name}** in the wiki mirror.", ephemeral=True)
        await itx.followup.send(embed=E.fow_embed(d))

    # -- scenes ------------------------------------------------------------------

    async def _open_scene(self, h: dict) -> list[discord.Embed]:
        title, text = await asyncio.to_thread(W.scene_text, h["file"])
        return E.pages(text, self.page, title=title, author="scene archive", colour=E.C_SCENE, footer_text=h["file"])

    @app_commands.command(name="recall", description="Search the scene archive: who said what, what happened where.")
    @app_commands.describe(query="Words or a name")
    async def recall(self, itx: discord.Interaction, query: str):
        await itx.response.defer()
        hits = await asyncio.to_thread(W.scene_hits, query)
        e = E.hits_embed(query, hits, "scenes", W.commit_hash())
        await itx.followup.send(embed=e, view=E.OpenHit(hits, self._open_scene) if hits else None)

    @app_commands.command(name="timeline", description="Every archived scene in reading order with its in-world moment.")
    async def timeline(self, itx: discord.Interaction):
        await itx.response.defer()
        text = await asyncio.to_thread(W.timeline)
        await E.send_pages(itx, E.pages(text, self.page, title="Timeline", colour=E.C_SCENE, footer_text="scenes/TIMELINE.md"))

    # -- housekeeping ------------------------------------------------------------

    @app_commands.command(name="whoami", description="Your table role as the bot sees it.")
    async def whoami(self, itx: discord.Interaction):
        role = self.bot.table_role(itx.user)
        await itx.response.send_message(f"{itx.user.mention}: table role **{role}** · index @ `{W.commit_hash()}`", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Lookup(bot))
