"""/verify — the manual-verification checks on a pasted scene or a linked message.
/date — the in-world calendar from "The Sky, the Hour and the Year": a fourteen-day turn of
Archon-days, two turns to a month, thirteen months of twenty-eight days, and Munahi, the
nameless day. The table's current date lives in table/calendar.yaml and is the Judger's to set.
"""
import asyncio
import re
from datetime import date

import discord
from discord import app_commands
from discord.ext import commands

import embeds as E
import wotr as W

M = W.M
T = M.T

ARCHONS = [("Urion", "Balance"), ("Uurgath", "Disruption"), ("Thalen", "Form"), ("Valen", "Time"), ("Maelor", "Memory"),
           ("Zhaeren", "Space"), ("Irath", "Dominion"), ("Veyra", "Desire"), ("Iesara", "Insight"), ("Kaetra", "Dream"),
           ("Wyther", "Motion"), ("Auren", "Death"), ("Selhar", "Harmony"), ("Elyndra", "Life")]
DAYS_IN_MONTH, MONTHS = 28, 13
YEAR = DAYS_IN_MONTH * MONTHS  # 364; Munahi sits after it, eight years in thirteen
CAL = T.TABLE / "calendar.yaml"


def describe(month: int, day: int, year: int | None = None, era: str = "") -> str:
    """Month 1–13, day 1–28 (day 0 of month 14 = Munahi)."""
    if month == 14:
        return "**Munahi**, the nameless day — no Archon, no Labour, no Work falls due, nothing can be entered, no window opens, no instrument binds."
    turn = 1 if day <= 14 else 2
    a, principle = ARCHONS[(day - 1) % 14]
    y = f" · Accord year {year}" if year else ""
    return f"**{a}'s day** ({principle}) · month {month}, {'first' if turn == 1 else 'second'} turn, day {day}{y}{(' · ' + era) if era else ''}"


def add_days(month: int, day: int, year: int, n: int) -> tuple[int, int, int]:
    """Advance through the calendar; Munahi is not modelled as a step (it is nobody's day)."""
    doy = (month - 1) * DAYS_IN_MONTH + day - 1 + n
    year += doy // YEAR
    doy %= YEAR
    return doy // DAYS_IN_MONTH + 1, doy % DAYS_IN_MONTH + 1, year


def _load() -> dict:
    import yaml
    return (yaml.safe_load(CAL.read_text(encoding="utf-8")) if CAL.exists() else None) or {}


def _save(d: dict) -> None:
    import yaml
    CAL.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")


class VerifyModal(discord.ui.Modal, title="Verify a scene"):
    text = discord.ui.TextInput(label="Scene text (markdown)", style=discord.TextStyle.paragraph, max_length=4000)

    def __init__(self, cog, combat: bool, culture: str, band: str):
        super().__init__()
        self.cog, self.combat, self.culture, self.band = cog, combat, culture, band

    async def on_submit(self, itx: discord.Interaction):
        await itx.response.defer()
        await self.cog.run_verify(itx, self.text.value, self.combat, self.culture, self.band)


class Craft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.page = int(bot.cfg.get("page_size", 3600))

    async def run_verify(self, itx: discord.Interaction, md: str, combat: bool, culture: str, band: str):
        report = await asyncio.to_thread(M.verify_scene, md, combat, culture, band)
        await E.send_pages(itx, E.pages(report, self.page, title="Verification", colour=E.C_STAT,
                                        footer_text=f"{len(md.split()):,} words · {'combat' if combat else 'standard'} · {culture or 'no culture'} · {band}"))

    @app_commands.command(name="verify", description="The manual-verification checks on a scene: paste it, or point at a message.")
    @app_commands.describe(link="A message link (right-click → Copy Message Link); leave empty to paste", combat="A duel or small action", culture="Culture the scene sits in", band="Length band")
    @app_commands.choices(band=[app_commands.Choice(name=b, value=b) for b in ("conversational", "standard", "set-piece")])
    async def verify(self, itx: discord.Interaction, link: str | None = None, combat: bool = False, culture: str = "", band: str = "standard"):
        if not link:
            return await itx.response.send_modal(VerifyModal(self, combat, culture, band))
        m = re.search(r"/channels/\d+/(\d+)/(\d+)", link)
        if not m:
            return await itx.response.send_message("That is not a message link.", ephemeral=True)
        await itx.response.defer()
        ch = self.bot.get_channel(int(m.group(1))) or await self.bot.fetch_channel(int(m.group(1)))
        msg = await ch.fetch_message(int(m.group(2)))
        text = msg.content
        for a in msg.attachments:
            if a.filename.endswith((".md", ".txt")) and a.size < 200_000:
                text += "\n" + (await a.read()).decode("utf-8", "replace")
        if len(text.split()) < 20:
            return await itx.followup.send("Fewer than twenty words there (if it is someone else's post, the bot needs the Message Content intent to read it).", ephemeral=True)
        await self.run_verify(itx, text, combat, culture, band)

    # -- the calendar --------------------------------------------------------------

    date_ = app_commands.Group(name="date", description="The in-world calendar.")

    @date_.command(name="today", description="The table's current in-world date.")
    async def today(self, itx: discord.Interaction):
        d = await asyncio.to_thread(_load)
        if not d:
            return await itx.response.send_message("No date is set on the table yet — the Judger sets it with `/date set`.", ephemeral=True)
        e = discord.Embed(title="Today", description=describe(d["month"], d["day"], d.get("year"), d.get("era", "")), colour=E.C_NAME)
        E.footer(e, f"set by {d.get('by', '?')} on {d.get('set_on', '?')} · The Sky, the Hour and the Year")
        await itx.response.send_message(embed=e)

    @date_.command(name="set", description="Judger: set the table's in-world date.")
    @app_commands.describe(month="1–13 (14 = Munahi)", day="1–28", year="Accord year", era="The Moto era name, if any")
    async def set_(self, itx: discord.Interaction, month: app_commands.Range[int, 1, 14], day: app_commands.Range[int, 1, 28] = 1, year: int | None = None, era: str = ""):
        if self.bot.table_role(itx.user) not in ("judger", "scribe"):
            return await itx.response.send_message("The Judger or a Scribe sets the date.", ephemeral=True)
        d = {"month": month, "day": 1 if month == 14 else day, "year": year, "era": era, "by": itx.user.display_name, "set_on": date.today().isoformat()}
        await asyncio.to_thread(_save, d)
        pushed = await asyncio.to_thread(M._table_commit, "Calendar set")
        await itx.response.send_message(f"Set: {describe(d['month'], d['day'], year, era)} · {pushed}")

    @date_.command(name="advance", description="Judger: move the table's date forward.")
    @app_commands.describe(days="How many days")
    async def advance(self, itx: discord.Interaction, days: app_commands.Range[int, 1, 3640]):
        if self.bot.table_role(itx.user) not in ("judger", "scribe"):
            return await itx.response.send_message("The Judger or a Scribe advances the date.", ephemeral=True)
        d = await asyncio.to_thread(_load)
        if not d or d["month"] == 14:
            return await itx.response.send_message("Set a calendar date first (`/date set`).", ephemeral=True)
        m, dd, y = add_days(d["month"], d["day"], d.get("year") or 0, days)
        d.update({"month": m, "day": dd, "year": y or None, "by": itx.user.display_name, "set_on": date.today().isoformat()})
        await asyncio.to_thread(_save, d)
        pushed = await asyncio.to_thread(M._table_commit, f"Calendar advanced {days} day(s)")
        await itx.response.send_message(f"Now: {describe(m, dd, d.get('year'), d.get('era', ''))} · {pushed}")

    @date_.command(name="name", description="Which Archon's day a given day is, and what a span of days lands on.")
    @app_commands.describe(month="1–13", day="1–28", plus="Days later (optional)")
    async def name(self, itx: discord.Interaction, month: app_commands.Range[int, 1, 13], day: app_commands.Range[int, 1, 28], plus: int = 0):
        m, dd, _ = add_days(month, day, 0, plus)
        text = describe(month, day) + (f"\n+{plus} days → " + describe(m, dd) if plus else "")
        e = discord.Embed(title="The Sky, the Hour and the Year", description=text, colour=E.C_NAME)
        e.add_field(name="The turn", value=" · ".join(f"{i + 1} {a}'s ({p})" for i, (a, p) in enumerate(ARCHONS)), inline=False)
        await itx.response.send_message(embed=e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Craft(bot))
