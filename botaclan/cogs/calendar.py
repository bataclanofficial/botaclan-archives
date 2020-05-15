from discord.ext.commands import Cog, Bot, Context, command, group
import logging
import botaclan.google.google_calendar as cal

log = logging.getLogger(__name__)


class Calendar(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(name="calendar", aliases=["cal"])
    async def calendar_group(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(content="Calendar help here")

    @calendar_group.command(name="list", aliases=["ls"])
    async def list_events(self, ctx: Context):
        cal.main()
        await ctx.send(content="Testing calendar")


def setup(bot: Bot) -> None:
    """Load the Calendar cog."""
    bot.add_cog(Calendar(bot))
