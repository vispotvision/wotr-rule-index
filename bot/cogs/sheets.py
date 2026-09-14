"""The sheet checker on #character-submission, and /sheet check on demand."""
import asyncio

import discord
from discord import app_commands
from discord.ext import commands

import embeds as E
import sheetcheck as S

ICON = {"fail": "❌", "warn": "⚠️", "ok": "✅"}


def report_embed(res: dict, who: str) -> discord.Embed:
    e = discord.Embed(title=f"Sheet check — {res['summary']}", colour=(0x2E7D32 if res["ok"] else 0xC62828))
    e.set_author(name=who)
    body = "\n".join(f"{ICON[l]} {t}" for l, t in res["findings"]) or "Nothing to check."
    e.description = E._clip(body, E.DESC_MAX)
    E.footer(e, "canon model R39-1 · Dominion ÷7 R39-2 · Stage I counts R39-3 · Max Grade binds R39-4 · struck names R22 · terms R14-5"
                + ("" if res["ok"] else " · fix and repost; nothing reaches the Judger until it passes"))
    return e


class Sheets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.forum = int(bot.cfg.get("channels", {}).get("character_submission", 0) or 0)

    async def _check_text(self, text: str) -> dict:
        return await asyncio.to_thread(S.check, text)

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        """A new post in the submission forum: check its opening message."""
        if not self.forum or thread.parent_id != self.forum:
            return
        await asyncio.sleep(2)  # the starter message lands just after the thread
        try:
            starter = thread.starter_message or await thread.fetch_message(thread.id)
        except discord.HTTPException:
            return
        text = starter.content + "\n" + "\n".join(a.filename for a in starter.attachments)
        for a in starter.attachments:
            if a.filename.endswith((".md", ".txt")) and a.size < 200_000:
                text += "\n" + (await a.read()).decode("utf-8", "replace")
        res = await self._check_text(text)
        await thread.send(embed=report_embed(res, starter.author.display_name))

    @app_commands.command(name="sheet", description="Check a character sheet against the canon: stat model, ceilings, pool, struck names, terms.")
    @app_commands.describe(link="A message link to the sheet (default: the first message of this thread)")
    async def sheet(self, itx: discord.Interaction, link: str | None = None):
        await itx.response.defer()
        msg = None
        if link:
            import re
            m = re.search(r"/channels/\d+/(\d+)/(\d+)", link)
            if m:
                ch = self.bot.get_channel(int(m.group(1))) or await self.bot.fetch_channel(int(m.group(1)))
                msg = await ch.fetch_message(int(m.group(2)))
        elif isinstance(itx.channel, discord.Thread):
            try:
                msg = itx.channel.starter_message or await itx.channel.fetch_message(itx.channel.id)
            except discord.HTTPException:
                msg = None
        if msg is None:
            return await itx.followup.send("Run this inside the sheet's thread, or pass a message link.", ephemeral=True)
        text = msg.content
        for a in msg.attachments:
            if a.filename.endswith((".md", ".txt")) and a.size < 200_000:
                text += "\n" + (await a.read()).decode("utf-8", "replace")
        res = await self._check_text(text)
        await itx.followup.send(embed=report_embed(res, msg.author.display_name))


async def setup(bot: commands.Bot):
    await bot.add_cog(Sheets(bot))
