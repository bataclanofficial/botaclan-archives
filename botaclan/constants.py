from vyper import v
import logging

log = logging.getLogger(__name__)


def set_env():
    v.set_env_prefix("botaclan")
    v.set_env_key_replacer(".", "_")

    v.bind_env("command.prefix")
    v.bind_env("discord.guild.id")
    v.bind_env("discord.token")
    v.bind_env("feature.roulette")
    v.bind_env("log.asyncio.level")
    v.bind_env("log.discord.level")
    v.bind_env("log.level")
    v.bind_env("log.websockets.level")


def set_env_defaults():
    v.set_default("command.prefix", "~b ")
    v.set_default("feature.roulette", True)
    v.set_default("log.asyncio.level", "warning")
    v.set_default("log.discord.level", "warning")
    v.set_default("log.level", "info")
    v.set_default("log.websockets.level", "warning")


def log_configuration():
    log.debug(f"command.prefix={COMMAND_PREFIX}")
    log.debug(f"discord.guild.id={DISCORD_GUILD_ID}")
    log.debug(f"discord.token={DISCORD_TOKEN}")
    log.debug(f"feature.roulette={FEATURE_ROULETTE}")
    log.debug(f"log.asyncio.level={LOG_LEVEL}")
    log.debug(f"log.discord.level={LOG_LEVEL}")
    log.debug(f"log.level={LOG_LEVEL}")
    log.debug(f"log.websockets.level={LOG_LEVEL}")


set_env()
set_env_defaults()

COMMAND_PREFIX = v.get_string("command.prefix")
DISCORD_GUILD_ID = v.get_int("discord.guild.id")
DISCORD_TOKEN = v.get_string("discord.token")
FEATURE_ROULETTE = v.get_bool("feature.roulette")
LOG_ASYNCIO_LEVEL = v.get_string("log.asyncio.level").upper()
LOG_DISCORD_LEVEL = v.get_string("log.discord.level").upper()
LOG_LEVEL = v.get_string("log.level").upper()
LOG_WEBSOCKETS_LEVEL = v.get_string("log.websockets.level").upper()
