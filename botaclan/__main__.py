import botaclan.constants
import discord
import logging

client = discord.Client()


@client.event
async def on_ready():
    logging.info(f"{client.user} connected.")


client.run(botaclan.constants.DISCORD_TOKEN)
