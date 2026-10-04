"""F1, the read side, under R72-40-PLAYERS_CAN_LOOK_UP: /ledger and /due show a player only
the Ledger lines about characters they own (config.yaml players:), the Judger and a Scribe every
line; /roster and /npc show an NPC's public face only (name, look, voice, role). Want, lie, tell,
knows and lied_about never leave table/npcs.yaml through here. Nothing in this cog writes.
"""
import asyncio
import re

import discord
from discord import app_commands
from discord.ext import commands

import embeds as E
import wotr as W

T = W.M.T


def owned(cfg: dict, uid: int) -> list[str]:
    return [str(n) for n in {str(k): v for k, v in (cfg.get("players") or {}).items()}.get(str(uid)) or []]


def mine(r: dict, names: list[str]) -> bool:
    """The line's subject names one of them. The subject is `who` before ' about ': L053, Sodoku
    Moto about Sonzai, is what Sodoku thinks in his own head, not a line for Sonzai's player."""
    subj = re.split(r"\s+about\s+", r.get("who") or "", maxsplit=1)[0].strip(" .").lower()
    if not subj:
        return False
    for n in (x.strip().lower() for x in names):
        if n and (re.search(rf"\b{re.escape(n)}\b", subj) or re.search(rf"\b{re.escape(subj)}\b", n)):
            return True
    return False


def line(r: dict) -> str:
    terms = "; ".join(T._terms(r))
    return (f"**{r['id']}** · {r['category']} · {r.get('who') or 'no one named'}"
            + (f"\n-# {terms}" if terms else "") + (f"\n-# came due: {r['why']}" if r.get("why") else "")
            + f"\n{r['text']}\n")


def face(r: dict) -> str:
    bits = [f"{k}: {v}" for k, v in T.public_face(r).items()]
    return f"**{r['name']}**\n" + ("\n".join(bits) or "-# no public face set yet") + "\n"


class Table(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.page = int(bot.cfg.get("page_size", 3600))

    async def _lines(self, itx: discord.Interaction, come_due: bool):
        await itx.response.defer(ephemeral=True)
        everyone = self.bot.table_role(itx.user) in ("judger", "scribe")
        names = owned(self.bot.cfg, itx.user.id)
        if not everyone and not names:
            return await itx.followup.send("No characters are on file for you (bot/config.yaml, players:). Ask the Judger to add yours.", ephemeral=True)
        rows = await asyncio.to_thread(T.due) if come_due else [r for r in await asyncio.to_thread(T.load, "ledger") if r.get("status") == "open"]
        if not everyone:
            rows = [r for r in rows if mine(r, names)]
        title = "Come due" if come_due else "Ledger"
        whose = "every line (Judger's view)" if everyone else "lines about " + ", ".join(names)
        if not rows:
            return await itx.followup.send(f"{title}: nothing open in {whose}.", ephemeral=True)
        await E.send_pages(itx, E.pages("\n".join(line(r) for r in rows), self.page, title=title, colour=E.C_STAT,
                                        footer_text=f"table/ledger.yaml · {whose} · R72-40"), ephemeral=True)

    @app_commands.command(name="ledger", description="The open Ledger lines about your own characters.")
    async def ledger(self, itx: discord.Interaction):
        await self._lines(itx, come_due=False)

    @app_commands.command(name="due", description="The Ledger lines about your own characters that have come due.")
    async def due(self, itx: discord.Interaction):
        await self._lines(itx, come_due=True)

    async def _faces(self, itx: discord.Interaction, rows: list[dict], title: str, miss: str):
        if not rows:
            return await itx.response.send_message(miss, ephemeral=True)
        await E.send_pages(itx, E.pages("\n".join(face(r) for r in rows), self.page, title=title, colour=E.C_CARD,
                                        footer_text="table/npcs.yaml · public face only: name, look, voice, role · R72-40"))

    @app_commands.command(name="roster", description="The NPCs on a thread's roster, as anyone may see them.")
    @app_commands.describe(thread="The story thread, e.g. Kharven, Mu-jin (default: every thread)")
    async def roster(self, itx: discord.Interaction, thread: str | None = None):
        rows = await asyncio.to_thread(T.roster, thread)
        await self._faces(itx, rows, f"Roster · {thread}" if thread else "Roster", f"No NPC on the roster{f' for {thread}' if thread else ''}.")

    @app_commands.command(name="npc", description="One NPC's public face: look, voice, role.")
    @app_commands.describe(name="The NPC's name, or part of it")
    async def npc(self, itx: discord.Interaction, name: str):
        key = name.strip().lower()
        rows = [r for r in await asyncio.to_thread(T.roster) if key and key in r["name"].lower()]
        await self._faces(itx, rows, name, f"No NPC on the roster matches **{name}**.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Table(bot))
