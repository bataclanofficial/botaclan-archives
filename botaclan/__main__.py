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
import asyncio
import signal

log = logging.getLogger(__name__)

botaclan.constants.log_constants()

if SENTRY_ENABLED:
    sentry_sdk.init(dsn=SENTRY_DSN)

bot = Botaclan(command_prefix=COMMAND_PREFIX, case_insensitive=True)
botaclan.bot.running_bot = bot


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.id == DISCORD_GUILD_ID, bot.guilds)
    log.info(f"{bot.user} connected to the following guild {guild.name}({guild.id}):")


async def rewrite_signal(loop):
    while True:
        loop.add_signal_handler(signal.SIGINT, bot.loop.stop)
        loop.add_signal_handler(signal.SIGTERM, bot.loop.stop)
        await asyncio.sleep(1)


server = botaclan.healthcheck.server.create_server()

bot.loop.create_task(server.serve())
bot.loop.create_task(rewrite_signal(bot.loop))
bot.run(DISCORD_TOKEN)
