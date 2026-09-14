#!/usr/bin/env python3
"""WOTR Bot: the players' front-end onto the rule index, the wiki mirror, the scene
archive and the table state. Plan: bot/PLAN.md.

  python bot/main.py            # run; DISCORD_TOKEN from the environment (user variable ok)
  python bot/main.py --sync     # also (re)register the slash commands with the guild, then run

Nothing here resolves a conflict, paraphrases a rule, or invents a number: every
answer is the index's own text or a refusal.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

import discord
import yaml
from discord.ext import commands

BOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BOT_DIR))

CFG = yaml.safe_load((BOT_DIR / "config.yaml").read_text(encoding="utf-8"))
COGS = ["cogs.lookup", "cogs.build", "cogs.audio", "cogs.scenes", "cogs.sheets"]

log = logging.getLogger("wotr")


def token() -> str:
    t = os.environ.get("DISCORD_TOKEN")
    if not t and sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                t = winreg.QueryValueEx(k, "DISCORD_TOKEN")[0]
        except OSError:
            pass
    if not t:
        sys.exit("DISCORD_TOKEN is not set (user environment variable).")
    return t.strip()


class WotrBot(commands.Bot):
    def __init__(self, sync: bool):
        intents = discord.Intents.default()
        intents.message_content = bool(CFG.get("intents", {}).get("message_content"))
        super().__init__(command_prefix=commands.when_mentioned, intents=intents, help_command=None)
        self.cfg = CFG
        self.guild = discord.Object(id=int(CFG["guild_id"]))
        self.do_sync = sync

    async def setup_hook(self):
        for c in COGS:
            await self.load_extension(c)
        self.tree.copy_global_to(guild=self.guild)
        if self.do_sync:
            cmds = await self.tree.sync(guild=self.guild)
            log.info("synced %d commands to guild %s: %s", len(cmds), self.guild.id, ", ".join(c.name for c in cmds))

    async def on_ready(self):
        log.info("online as %s (%s) in %s", self.user, self.user.id, ", ".join(g.name for g in self.guilds))

    def table_role(self, member: discord.abc.User) -> str:
        """judger / scribe / player / reader, from config.yaml's role map."""
        names = {r.name for r in getattr(member, "roles", [])}
        for level in ("judger", "scribe", "player"):
            if names & set(self.cfg.get("roles", {}).get(level, [])):
                return level
        return "reader"

    async def on_app_command_error(self, itx: discord.Interaction, err: Exception):
        log.exception("command %s failed", itx.command and itx.command.name, exc_info=err)
        msg = f"That failed: `{type(err).__name__}: {err}`"[:1900]
        if itx.response.is_done():
            await itx.followup.send(msg, ephemeral=True)
        else:
            await itx.response.send_message(msg, ephemeral=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sync", action="store_true", help="register slash commands with the guild on start")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    bot = WotrBot(sync=a.sync)
    bot.tree.on_error = bot.on_app_command_error
    bot.run(token(), log_handler=None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
