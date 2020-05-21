from importlib_metadata import version
from botaclan.constants import (
    LOG_LEVEL,
    LOG_ASYNCIO_LEVEL,
    LOG_DISCORD_LEVEL,
    LOG_WEBSOCKETS_LEVEL,
)
import coloredlogs
import logging
import sys

__version__ = version(__package__)

root_log = logging.getLogger()
root_log.setLevel(LOG_LEVEL)
coloredlogs.install(logger=root_log, stream=sys.stdout, level=LOG_LEVEL)
logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logging.getLogger("asyncio").setLevel(LOG_ASYNCIO_LEVEL)
logging.getLogger("discord").setLevel(LOG_DISCORD_LEVEL)
logging.getLogger("websockets").setLevel(LOG_WEBSOCKETS_LEVEL)
logging.getLogger(__name__)
