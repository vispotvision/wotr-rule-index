"""Builders for players: /name from the Naming Guide's element banks, /stats from the FOW codex."""
import asyncio
import random

import discord
from discord import app_commands
from discord.ext import commands

import embeds as E
import fow as F
import names as N

CULTURE_CHOICES = [app_commands.Choice(name=v, value=k) for k, v in N.CULTURES.items()]
BRANCH_CHOICES = [app_commands.Choice(name=b, value=b) for b in N.ELVEN_BRANCHES]
LINEAGE_CHOICES = [app_commands.Choice(name=b, value=b) for b in N.BEASTKIN_LINEAGES]
SEX_CHOICES = [app_commands.Choice(name=s, value=s) for s in ("male", "female")]


class Build(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="name", description="Compose a name from a culture's ratified element bank (the Naming Guide).")
    @app_commands.describe(culture="Which register", branch="Elven only: the branch", lineage="Beastkin only: the lineage",
                           sex="Concord / Holy Sea only: which given-name pool")
    @app_commands.choices(culture=CULTURE_CHOICES, branch=BRANCH_CHOICES, lineage=LINEAGE_CHOICES, sex=SEX_CHOICES)
    async def name(self, itx: discord.Interaction, culture: str, branch: str | None = None, lineage: str | None = None,
                   sex: str | None = None):
        label = N.CULTURES[culture]

        async def again() -> discord.Embed:
            d = await asyncio.to_thread(N.build, culture, random.randrange(1 << 30), branch=branch or "", lineage=lineage or "", sex=sex or "")
            return E.name_embed(d, label)

        await itx.response.send_message(embed=await again(), view=E.Reroll(again))

    @app_commands.command(name="name_help", description="Which registers /name can and cannot build, and why.")
    async def name_help(self, itx: discord.Interaction):
        e = discord.Embed(title="What /name can build", colour=E.C_NAME,
                          description="\n".join(f"• **{v}** — `{N.BANK[k]['rule']}`" for k, v in N.CULTURES.items()))
        e.add_field(name="Not offered (no ratified element bank — the bot will not coin one)",
                    value=E._clip("\n".join(f"• **{k.title()}** — {v}" for k, v in N.NOT_OFFERED.items()), E.FIELD_MAX), inline=False)
        await itx.response.send_message(embed=e, ephemeral=True)

    @app_commands.command(name="stats", description="A Fracture of Worlds stat block for a Level, derived from the codex. Not a card.")
    @app_commands.describe(level="1-500; the Stage follows the Band and the lean is chosen for you")
    async def stats(self, itx: discord.Interaction, level: app_commands.Range[int, 1, 500]):
        async def again() -> discord.Embed:
            lean = random.choice(F.primaries() + [None])
            d = await asyncio.to_thread(F.build, level, None, lean, random.randrange(1 << 30))
            return E.stat_embed(d)

        await itx.response.send_message(embed=await again(), view=E.Reroll(again))


async def setup(bot: commands.Bot):
    await bot.add_cog(Build(bot))
