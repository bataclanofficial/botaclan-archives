import botaclan.constants
import discord
import logging

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.find(
        lambda g: g.id == botaclan.constants.DISCORD_GUILD_ID, client.guilds
    )
    logging.info(
        f"{client.user} connected to the following guild {guild.name}({guild.id}):"
    )


client.run(botaclan.constants.DISCORD_TOKEN)
