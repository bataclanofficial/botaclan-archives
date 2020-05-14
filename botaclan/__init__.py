import coloredlogs
import botaclan.constants
import logging
import sys

log_format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

root_log = logging.getLogger()
root_log.setLevel(botaclan.constants.LOG_LEVEL)
coloredlogs.install(
    logger=root_log, stream=sys.stdout, level=botaclan.constants.LOG_LEVEL
)

logging.getLogger("asyncio").setLevel(botaclan.constants.LOG_ASYNCIO_LEVEL)
logging.getLogger("discord").setLevel(botaclan.constants.LOG_DISCORD_LEVEL)
logging.getLogger("websockets").setLevel(botaclan.constants.LOG_WEBSOCKETS_LEVEL)
logging.getLogger(__name__)

botaclan.constants.log_configuration()
