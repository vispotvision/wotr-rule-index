"""F2: /scene save — a thread, a span after a message link, or a pasted block becomes an
archived scene (scenes/<slug>.md, the Notion Scene Archive, one commit); /event — an event
on the table (table/events.yaml) and a card in #event-log.

Judger and Scribe archive; a Player's /scene save posts the compiled scene and its
verification report to the Judger channel instead, for the Judger to archive.
"""
import asyncio
import re
from datetime import date

import discord
from discord import app_commands
from discord.ext import commands

import compile as C
import embeds as E
import wotr as W

M = W.M
T = M.T
LINK = re.compile(r"https://(?:\w+\.)?discord(?:app)?\.com/channels/(\d+)/(\d+)/(\d+)")


def _verify(md: str) -> str:
    return M.verify_scene(md)


def _archive(title: str, md: str, notes: str) -> str:
    return M.archive_scene(title, md, notes)


def _cast(scene_file: str, script: str) -> str:
    return M.cast_scene(scene_file, script)


class ArchiveView(discord.ui.View):
    def __init__(self, cog, title: str, md: str, script: str, notes: str, timeout: float = 1800):
        super().__init__(timeout=timeout)
        self.cog, self.title, self.md, self.script, self.notes = cog, title, md, script, notes

    @discord.ui.button(label="✔ Archive", style=discord.ButtonStyle.success)
    async def archive(self, itx: discord.Interaction, _: discord.ui.Button):
        if self.cog.bot.table_role(itx.user) not in ("judger", "scribe"):
            return await itx.response.send_message("Only the Judger or a Scribe archives.", ephemeral=True)
        self.clear_items()
        await itx.response.edit_message(view=self)
        async with self.cog.lock:
            reply = await asyncio.to_thread(_archive, self.title, self.md, self.notes)
            m = re.search(r"saved (scenes/\S+\.md)", reply)
            cast_note = ""
            if m and self.script:
                cast_note = "\n" + (await asyncio.to_thread(_cast, m.group(1).split("/")[-1], self.script))[:400]
        await itx.followup.send(f"📜 {reply}{cast_note}")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, itx: discord.Interaction, _: discord.ui.Button):
        self.clear_items()
        await itx.response.edit_message(content="Not archived.", view=self)


class PasteModal(discord.ui.Modal, title="Paste the scene"):
    text = discord.ui.TextInput(label="Scene text (markdown)", style=discord.TextStyle.paragraph, max_length=4000)

    def __init__(self, cog, title: str):
        super().__init__()
        self.cog, self.scene_title = cog, title

    async def on_submit(self, itx: discord.Interaction):
        md = f"# {self.scene_title}\n\n{self.text.value.strip()}\n"
        await self.cog.present(itx, self.scene_title, md, "", f"Pasted into Discord by {itx.user.display_name} on {date.today().isoformat()}.")


class Scenes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lock = asyncio.Lock()
        self.judger_channel = int(bot.cfg.get("channels", {}).get("judger", 0) or 0)
        self.event_log = int(bot.cfg.get("channels", {}).get("event_log", 0) or 0)

    scene = app_commands.Group(name="scene", description="Save what was written here as an archived scene.")

    async def present(self, itx: discord.Interaction, title: str, md: str, script: str, notes: str):
        """Verify, show the report, and offer the archive button (or route to the Judger)."""
        report = await asyncio.to_thread(_verify, md)
        words = len(md.split())
        role = self.bot.table_role(itx.user)
        head = discord.Embed(title=f"Scene: {title}", colour=E.C_SCENE,
                             description=E._clip(f"{words:,} words · {notes}\n\n**Verification**\n{report}", E.DESC_MAX))
        file = discord.File(fp=__import__("io").BytesIO(md.encode("utf-8")), filename=f"{W.M._slug(title)}.md")
        send = itx.followup.send if itx.response.is_done() else itx.response.send_message
        if role in ("judger", "scribe"):
            await send(embed=head, file=file, view=ArchiveView(self, title, md, script, notes))
        else:
            ch = self.bot.get_channel(self.judger_channel)
            if ch:
                await ch.send(content=f"Proposed by {itx.user.mention} from {itx.channel.mention}:", embed=head, file=file,
                              view=ArchiveView(self, title, md, script, notes + f" Proposed by {itx.user.display_name}."))
                await send("Sent to the Judger's desk with its verification report.", ephemeral=True)
            else:
                await send("No Judger channel is configured; ask the Judger to run /scene save.", ephemeral=True)

    @scene.command(name="save", description="Archive this thread, the messages after a link, or a pasted block as a scene.")
    @app_commands.describe(title="The scene's title", source="Where the text comes from", link="With source=link: the first message to include", count="With source=thread: how many recent messages (default 200)")
    @app_commands.choices(source=[app_commands.Choice(name="this thread / channel", value="thread"),
                                  app_commands.Choice(name="from a message link onward", value="link"),
                                  app_commands.Choice(name="paste a block", value="paste")])
    async def save(self, itx: discord.Interaction, title: str, source: str = "thread", link: str | None = None, count: app_commands.Range[int, 1, 500] = 200):
        if source == "paste":
            return await itx.response.send_modal(PasteModal(self, title))
        await itx.response.defer(ephemeral=False)
        after = None
        if source == "link":
            m = LINK.search(link or "")
            if not m:
                return await itx.followup.send("Give a message link (right-click a message → Copy Message Link).", ephemeral=True)
            after = discord.Object(id=int(m.group(3)) - 1)
        msgs = [m async for m in itx.channel.history(limit=count, after=after, oldest_first=True)] if after else \
               list(reversed([m async for m in itx.channel.history(limit=count)]))
        md, script, speakers = C.compile_scene(title, msgs)
        if len(md.split()) < 20:
            return await itx.followup.send("Fewer than twenty words of in-character text found here.", ephemeral=True)
        notes = f"Saved from Discord #{getattr(itx.channel, 'name', '?')} on {date.today().isoformat()} by {itx.user.display_name}; voices: {', '.join(speakers)}."
        await self.present(itx, title, md, script, notes)

    # -- events ---------------------------------------------------------------

    event = app_commands.Group(name="event", description="Events on the table.")

    @event.command(name="add", description="Record an event: what, when (in-world), where, who.")
    @app_commands.describe(title="What happens", when="In-world date or moment", where="Place (a location channel name works)", who="Who is involved", blurb="One paragraph")
    async def add(self, itx: discord.Interaction, title: str, when: str, where: str, who: str = "", blurb: str = ""):
        if self.bot.table_role(itx.user) not in ("judger", "scribe"):
            return await itx.response.send_message("Events are entered by the Judger or a Scribe.", ephemeral=True)
        await itx.response.defer()
        async with self.lock:
            def write():
                rows = T.load("events")
                eid = f"E{len(rows) + 1:03d}"
                rows.append({"id": eid, "title": title, "when": when, "where": where, "who": who, "blurb": blurb,
                             "entered": date.today().isoformat(), "by": itx.user.display_name, "status": "upcoming"})
                T.save("events", rows)
                return eid, M._table_commit(f"Event {eid}: {title}")
            eid, pushed = await asyncio.to_thread(write)
        e = discord.Embed(title=f"{eid} — {title}", colour=E.C_NAME, description=E._clip(blurb, E.DESC_MAX) or None)
        e.add_field(name="When", value=when, inline=True)
        e.add_field(name="Where", value=where, inline=True)
        if who:
            e.add_field(name="Who", value=E._clip(who, E.FIELD_MAX), inline=False)
        E.footer(e, f"table/events.yaml · {pushed}")
        ch = self.bot.get_channel(self.event_log)
        if ch and ch.id != itx.channel_id:
            await ch.send(embed=e)
        await itx.followup.send(embed=e)

    @event.command(name="list", description="Upcoming events on the table.")
    async def list_(self, itx: discord.Interaction):
        rows = [r for r in await asyncio.to_thread(T.load, "events") if r.get("status") == "upcoming"]
        if not rows:
            return await itx.response.send_message("No upcoming events on the table.", ephemeral=True)
        body = "\n\n".join(f"**{r['id']} — {r['title']}**\n{r['when']} · {r['where']}" + (f" · {r['who']}" if r.get("who") else "") for r in rows)
        await E.send_pages(itx, E.pages(body, int(self.bot.cfg.get("page_size", 3600)), title="Upcoming events", colour=E.C_NAME, footer_text="table/events.yaml"))

    @event.command(name="done", description="Mark an event as having happened.")
    @app_commands.describe(id="The event id, e.g. E003")
    async def done(self, itx: discord.Interaction, id: str):
        if self.bot.table_role(itx.user) not in ("judger", "scribe"):
            return await itx.response.send_message("Events are closed by the Judger or a Scribe.", ephemeral=True)
        await itx.response.defer()
        async with self.lock:
            def write():
                rows = T.load("events")
                for r in rows:
                    if r["id"].upper() == id.upper():
                        r["status"] = "happened"
                        T.save("events", rows)
                        return r["title"], M._table_commit(f"Event {r['id']} happened: {r['title']}")
                return None, ""
            title, pushed = await asyncio.to_thread(write)
        await itx.followup.send(f"**{id.upper()}** — {title}: happened · {pushed}" if title else f"No event {id}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Scenes(bot))
