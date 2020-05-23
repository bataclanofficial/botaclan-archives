from botaclan.constants import (
    FEATURE_ROULETTE,
    FEATURE_CALENDAR,
)
from discord.ext.commands import Bot
import logging
import signal
import asyncio

log = logging.getLogger(__name__)

running_bot = None

COGS_AND_FEATURE_STATUS = {
    "botaclan.cogs.roulette": FEATURE_ROULETTE,
    "botaclan.cogs.calendar": FEATURE_CALENDAR,
}


class Botaclan(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_cogs()

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
