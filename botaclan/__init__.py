import coloredlogs
import botaclan.constants
import logging
import sys

log_format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

root_log = logging.getLogger()
root_log.setLevel(botaclan.constants.LOG_LEVEL)
coloredlogs.install(logger=root_log, stream=sys.stdout)

logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("websockets").setLevel(logging.WARNING)
logging.getLogger(__name__)

logging.debug(f"command.prefix={botaclan.constants.COMMAND_PREFIX}")
logging.debug(f"discord.guild.id={botaclan.constants.DISCORD_GUILD_ID}")
logging.debug(f"discord.token={botaclan.constants.DISCORD_TOKEN}")
logging.debug(f"feature.roulette={botaclan.constants.FEATURE_ROULETTE}")
logging.debug(f"log.level={botaclan.constants.LOG_LEVEL}")
