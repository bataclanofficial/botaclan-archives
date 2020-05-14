from discord.ext.commands import Cog, Bot, Context, command
import botaclan.helpers
import random
import logging

log = logging.getLogger(__name__)


class Roulette(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="options")
    async def options(self, ctx: Context, *, content: str):
        items = botaclan.helpers.parse_comma_list_message(content)
        chosen = random.choice(items)
        log.debug(f"Message({ctx.message.id} - options - {content}) {chosen}")
        await ctx.send(content=f"I choose {chosen}")


def setup(bot: Bot) -> None:
    """Load the Roulette cog."""
    bot.add_cog(Roulette(bot))
