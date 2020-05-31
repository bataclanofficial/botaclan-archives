from botaclan.constants import (
    DISCORD_GUILD_ID,
    FEATURE_CALENDAR,
    FEATURE_MUSICPLAYER,
    FEATURE_ROULETTE,
)
from discord.ext.commands import Bot
import asyncio
import discord.utils
import logging
import signal


log = logging.getLogger(__name__)

running_bot = None

COGS_AND_FEATURE_STATUS = {
    "botaclan.cogs.calendar": FEATURE_CALENDAR,
    "botaclan.cogs.musicplayer": FEATURE_MUSICPLAYER,
    "botaclan.cogs.roulette": FEATURE_ROULETTE,
}


class Botaclan(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_cogs()

    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.id == DISCORD_GUILD_ID, self.guilds)
        log.info(
            f"{self.user} connected to the following guild {guild.name}({guild.id}):"
        )

    def load_cogs(self):
        for cog, status in COGS_AND_FEATURE_STATUS.items():
            if status:
                log.debug(f"Loading cog - {cog}")
                self.load_extension(cog)

    async def rewrite_signal(self):
        while True:
            self.loop.add_signal_handler(signal.SIGINT, self.loop.stop)
            self.loop.add_signal_handler(signal.SIGTERM, self.loop.stop)
            await asyncio.sleep(1)
