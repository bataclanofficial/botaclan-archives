from discord.ext import commands
import botaclan.constants
import discord
import logging

bot = commands.Bot(command_prefix=botaclan.constants.COMMAND_PREFIX)


@bot.event
async def on_ready():
    guild = discord.utils.find(
        lambda g: g.id == botaclan.constants.DISCORD_GUILD_ID, bot.guilds
    )
    logging.info(
        f"{bot.user} connected to the following guild {guild.name}({guild.id}):"
    )


bot.run(botaclan.constants.DISCORD_TOKEN)
