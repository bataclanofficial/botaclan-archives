from botaclan.bot import Botaclan
from botaclan.constants import (
    COMMAND_PREFIX,
    DISCORD_GUILD_ID,
    DISCORD_TOKEN,
    SENTRY_DSN,
    SENTRY_ENABLED,
)
import botaclan.constants
import botaclan.healthcheck.server
import discord
import logging
import sentry_sdk

log = logging.getLogger(__name__)

botaclan.constants.log_constants()

if SENTRY_ENABLED:
    sentry_sdk.init(dsn=SENTRY_DSN)

bot = Botaclan(command_prefix=COMMAND_PREFIX, case_insensitive=True)


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.id == DISCORD_GUILD_ID, bot.guilds)
    log.info(f"{bot.user} connected to the following guild {guild.name}({guild.id}):")


bot.loop.create_task(botaclan.healthcheck.server.create_server().serve())
bot.run(DISCORD_TOKEN)
