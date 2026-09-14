"""/narrate: render a scene to audio with the local narrator (free) or ElevenLabs (paid), and drop
the file in the channel when it is done. Judger and Scribe only: both engines cost something —
the PC's CPU or the ElevenLabs plan — and the bot asks which when the caller does not say."""
import asyncio
import re
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

import embeds as E
import wotr as W

M = W.M
POLL_S, MAX_WAIT_S = 20, 3 * 3600


def _scene(query: str) -> tuple[Path | None, list[str]]:
    return M._find_scene(query)


def _counts(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return len(text.split()), len(text)


def _job_done(job_id: str) -> str:
    for j in M._jobs():
        if j["id"] == job_id:
            return M._job_state(j)
    return "unknown"


def _job_output(job_id: str) -> Path | None:
    """The file the job wrote, read from its log's summary line."""
    for j in M._jobs():
        if j["id"] == job_id:
            tail = Path(j["log"]).read_text(encoding="utf-8", errors="replace")[-6000:]
            m = re.search(r"(?m)^\s+(\S+\.(?:mp3|wav)): [\d,]+ words", tail)
            if not m:
                return None
            hits = list(M._audio_dir().rglob(m.group(1)))
            return hits[0] if hits else None
    return None


class EnginePick(discord.ui.View):
    def __init__(self, cog, path: Path, words: int, chars: int, allow_eleven: bool, timeout: float = 300):
        super().__init__(timeout=timeout)
        self.cog, self.path = cog, path
        self.add_item(self._button(f"Local (free, ~{max(1, words // 150)} min)", "local", discord.ButtonStyle.secondary))
        if allow_eleven:
            self.add_item(self._button(f"ElevenLabs (≈ {chars:,} characters)", "elevenlabs", discord.ButtonStyle.primary))

    def _button(self, label: str, engine: str, style):
        b = discord.ui.Button(label=label, style=style)

        async def cb(itx: discord.Interaction):
            self.clear_items()
            await itx.response.edit_message(view=self)
            await self.cog.start(itx, self.path, engine)
        b.callback = cb
        return b


class Audio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def ac_scene(self, itx: discord.Interaction, current: str):
        names = [p.name for p in sorted(W.SCENES.glob("*.md")) if current.lower() in p.name.lower()
                 and p.name not in ("MANIFEST.md", "ARCS.md", "CAST.md", "TIMELINE.md")]
        return [app_commands.Choice(name=n[:100], value=n[:100]) for n in names[:25]]

    @app_commands.command(name="narrate", description="Render an archived scene to audio: local narrator (free) or ElevenLabs (paid).")
    @app_commands.describe(scene="Scene file or a unique part of its title", engine="Leave empty to be asked")
    @app_commands.choices(engine=[app_commands.Choice(name="local (free)", value="local"),
                                  app_commands.Choice(name="elevenlabs (paid)", value="elevenlabs")])
    @app_commands.autocomplete(scene=ac_scene)
    async def narrate(self, itx: discord.Interaction, scene: str, engine: str | None = None):
        role = self.bot.table_role(itx.user)
        if role not in ("judger", "scribe"):
            return await itx.response.send_message("Narration is for the Judger and Scribes — it costs CPU or ElevenLabs credit.", ephemeral=True)
        path, cands = await asyncio.to_thread(_scene, scene)
        if path is None:
            msg = ("More than one scene matches:\n" + "\n".join(f"• {c}" for c in cands[:10])) if cands else f"No scene matches **{scene}**."
            return await itx.response.send_message(msg, ephemeral=True)
        words, chars = _counts(path)
        if engine:
            await itx.response.send_message(f"Rendering **{path.stem}** on **{engine}**…")
            return await self.start(itx, path, engine)
        e = discord.Embed(title=f"Narrate {path.stem}?", colour=E.C_SCENE,
                          description=f"{words:,} words. **Local** is free and takes a few minutes on the PC; **ElevenLabs** bills about "
                                      f"{chars:,} characters to the plan and is quicker.")
        await itx.response.send_message(embed=e, view=EnginePick(self, path, words, chars, allow_eleven=role == "judger"))

    async def start(self, itx: discord.Interaction, path: Path, engine: str):
        reply = await asyncio.to_thread(M.narrate_scene, path.name, "narrator", engine)
        m = re.search(r"job (\d{8}-\d{6})", reply)
        channel = itx.channel
        if not m:
            return await channel.send(f"Could not start the render: {reply[:1500]}")
        job = m.group(1)
        await channel.send(f"🎙 {reply.split(' Output folder')[0]}")
        waited = 0
        while waited < MAX_WAIT_S:
            await asyncio.sleep(POLL_S)
            waited += POLL_S
            state = await asyncio.to_thread(_job_done, job)
            if state in ("done", "failed"):
                break
        if state != "done":
            return await channel.send(f"Render **{path.stem}** ({engine}) {state} after {waited // 60} min — see `build/.narrate-{job}.log`.")
        out = await asyncio.to_thread(_job_output, job)
        if not out:
            return await channel.send(f"Render **{path.stem}** finished but the file was not found in the audio folder.")
        limit = getattr(itx.guild, "filesize_limit", 10 * 1024 * 1024)
        if out.stat().st_size <= limit:
            await channel.send(f"**{path.stem}** — {engine}", file=discord.File(str(out)))
        else:
            await channel.send(f"**{path.stem}** — {engine}: {out.stat().st_size // 1_000_000} MB, over this server's upload limit; it is in the audio folder as `{out.name}`.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Audio(bot))
