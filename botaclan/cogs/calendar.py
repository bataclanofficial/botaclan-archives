from discord.ext.commands import Cog, Bot, Context, group
from discord import Embed
from google.oauth2 import service_account
import logging
import botaclan.google.google_calendar as cal
import botaclan.google.auth

log = logging.getLogger(__name__)


class Calendar(Cog):
    def __init__(self, bot: Bot, credentials: service_account.Credentials):
        self.bot = bot
        self.credentials = credentials

    @group(name="calendar", aliases=["cal"])
    async def calendar_group(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(content="Calendar help here")

    @calendar_group.command(name="list", aliases=["ls"])
    async def list_events(self, ctx: Context):
        events = cal.list_events(self.credentials)
        if not events:
            log.info("No events were found")
        embed = Embed(name="Next events")
        for event in events:
            summary = event.get("summary")
            start = event["start"].get("dateTime", event["start"].get("date"))
            embed.add_field(name=start, value=summary, inline=False)
        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Calendar cog."""
    creds = botaclan.google.auth.generate_credentials(
        botaclan.constants.GOOGLEAPI_APPLICATION_CREDENTIALS
    )
    bot.add_cog(Calendar(bot, creds))
