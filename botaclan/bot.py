from discord.ext.commands import Bot
from botaclan.constants import (
    FEATURE_ROULETTE,
    FEATURE_CALENDAR,
)
import logging

log = logging.getLogger(__name__)

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
