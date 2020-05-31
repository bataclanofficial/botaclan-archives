from vyper import v
import argparse
import botaclan.constants.default as default
import logging


log = logging.getLogger(__name__)


def setup():
    set_default_values()
    set_environment_variables()
    if not v.is_set("disable.cli"):
        set_cli_arguments()
    set_config_file_extensions()
    if config_file := v.get("config.file"):
        read_config_file(config_file)
    else:
        find_config_file()


def read_config_file(path: str):
    try:
        with open(path, "r") as file_content:
            content = file_content.read()
    except Exception:
        log.critical("No configuration file was found with the provided path.")
        exit(1)
    v.read_config(content)


def find_config_file():
    v.set_config_name(default.CONFIG_FILENAME)
    for supported_path in default.SUPPORTED_CONFIG_PATHS:
        v.add_config_path(supported_path)
    try:
        v.read_in_config()
    except Exception:
        log.warning(
            "No configuration file was found. "
            "Some tweaks may be missing or were provided through environment variables."
        )


def set_config_file_extensions():
    for ext in default.SUPPORTED_CONFIG_EXTENSIONS:
        v.set_config_type(ext)


def set_environment_variables():
    v.set_env_prefix("botaclan")
    v.set_env_key_replacer(".", "_")
    v.automatic_env()


def set_cli_arguments():
    p = argparse.ArgumentParser(description="Bataclan's official bot")
    p.add_argument(
        "--healthcheck.host",
        help="Host used to spawn the heathcheck server",
        type=str,
        default=default.HEALTHCHECK_HOST,
        nargs="?",
    )
    p.add_argument(
        "--healthcheck.port",
        help="Port used to spawn the heathcheck server",
        type=int,
        default=default.HEALTHCHECK_PORT,
        nargs="?",
    )
    p.add_argument(
        "--log.level",
        help="Log level to be used",
        type=str,
        choices=default.SUPPORTED_LOG_LEVELS,
        default=default.LOG_LEVEL,
        nargs="?",
    )
    p.add_argument(
        "--config.file", help="Path to the YAML configuration", type=str, nargs="?",
    )
    v.bind_args(p)


def set_default_values():
    v.set_default("command.prefix", default.COMMAND_PREFIX)
    v.set_default("feature.calendar", default.FEATURE_CALENDAR)
    v.set_default("feature.musicplayer", default.FEATURE_MUSICPLAYER)
    v.set_default("feature.roulette", default.FEATURE_ROULETTE)
    v.set_default(
        "googleapi.application.credentials", default.GOOGLEAPI_APPLICATION_CREDENTIALS
    )
    v.set_default("googleapi.calendar.id", default.GOOGLEAPI_CALENDAR_ID)
    v.set_default("healthcheck.host", default.HEALTHCHECK_HOST)
    v.set_default("healthcheck.port", default.HEALTHCHECK_PORT)
    v.set_default("log.asyncio.level", default.LOG_ASYNCIO_LEVEL)
    v.set_default("log.discord.level", default.LOG_DISCORD_LEVEL)
    v.set_default("log.level", default.LOG_LEVEL)
    v.set_default("log.uvicorn.level", default.LOG_UVICORN_LEVEL)
    v.set_default("log.websockets.level", default.LOG_WEBSOCKETS_LEVEL)
    v.set_default("sentry.enabled", default.SENTRY_ENABLED)
    v.set_default("timezone", default.TIMEZONE)


def log_constants():
    log.debug(f"command.prefix={COMMAND_PREFIX}")
    log.debug(f"discord.guild.id={DISCORD_GUILD_ID}")
    log.debug(f"discord.token={DISCORD_TOKEN}")
    log.debug(f"feature.calendar={FEATURE_CALENDAR}")
    log.debug(f"feature.musicplayer={FEATURE_MUSICPLAYER}")
    log.debug(f"feature.roulette={FEATURE_ROULETTE}")
    log.debug(f"googleapi.application.credentials={GOOGLEAPI_APPLICATION_CREDENTIALS}")
    log.debug(f"googleapi.calendar.id={GOOGLEAPI_CALENDAR_ID}")
    log.debug(f"healthcheck.host={HEALTHCHECK_HOST}")
    log.debug(f"healthcheck.port={HEALTHCHECK_PORT}")
    log.debug(f"log.asyncio.level={LOG_ASYNCIO_LEVEL}")
    log.debug(f"log.discord.level={LOG_DISCORD_LEVEL}")
    log.debug(f"log.level={LOG_LEVEL}")
    log.debug(f"log.uvicorn.level={LOG_UVICORN_LEVEL}")
    log.debug(f"log.websockets.level={LOG_WEBSOCKETS_LEVEL}")
    log.debug(f"sentry.dsn={SENTRY_DSN}")
    log.debug(f"sentry.enabled={SENTRY_ENABLED}")
    log.debug(f"soundcloud.client.id={SOUNDCLOUD_CLIENT_ID}")
    log.debug(f"spotify.client.id={SPOTIFY_CLIENT_ID}")
    log.debug(f"spotify.client.secret={SPOTIFY_CLIENT_SECRET}")
    log.debug(f"timezone={TIMEZONE}")


setup()

COMMAND_PREFIX = v.get_string("command.prefix")
DISCORD_GUILD_ID = v.get_int("discord.guild.id")
DISCORD_TOKEN = v.get_string("discord.token")
FEATURE_CALENDAR = v.get_bool("feature.calendar")
FEATURE_MUSICPLAYER = v.get_bool("feature.musicplayer")
FEATURE_ROULETTE = v.get_bool("feature.roulette")
GOOGLEAPI_APPLICATION_CREDENTIALS = v.get_string("googleapi.application.credentials")
GOOGLEAPI_CALENDAR_ID = v.get_string("googleapi.calendar.id")
HEALTHCHECK_HOST = v.get_string("healthcheck.host")
HEALTHCHECK_PORT = v.get_int("healthcheck.port")
LOG_ASYNCIO_LEVEL = v.get_string("log.asyncio.level").upper()
LOG_DISCORD_LEVEL = v.get_string("log.discord.level").upper()
LOG_LEVEL = v.get_string("log.level").upper()
LOG_UVICORN_LEVEL = v.get_string("log.uvicorn.level")
LOG_WEBSOCKETS_LEVEL = v.get_string("log.websockets.level").upper()
SENTRY_DSN = v.get_string("sentry.dsn")
SENTRY_ENABLED = v.get_string("sentry.enabled")
SOUNDCLOUD_CLIENT_ID = v.get_string("soundcloud.client.id")
SPOTIFY_CLIENT_ID = v.get_string("spotify.client.id")
SPOTIFY_CLIENT_SECRET = v.get_string("spotify.client.secret")
TIMEZONE = v.get_string("timezone")
