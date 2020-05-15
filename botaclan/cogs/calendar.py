from discord.ext.commands import Cog, Bot, Context, command
import logging
import botaclan.google.google_calendar as cal

log = logging.getLogger(__name__)


class Calendar(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="calendar-test")
    async def calendar_test(self, ctx: Context):
        cal.main()
        await ctx.send(content="Testing calendar")


def setup(bot: Bot) -> None:
    """Load the Calendar cog."""
    bot.add_cog(Calendar(bot))
