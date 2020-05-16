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

    @group(name="event")
    async def event_group(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(content="Event help here")

    @event_group.command(name="list", aliases=["ls"])
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

    @event_group.command(name="create", aliases=["add"])
    async def create_event(self, ctx: Context, start: str, end: str, *, summary: str):
        event = {
            "start": {"dateTime": start, "timeZone": botaclan.constants.TIMEZONE},
            "end": {"dateTime": end, "timeZone": botaclan.constants.TIMEZONE},
            "summary": summary,
        }
        cal.create_event(self.credentials, event)
        await ctx.send(content="Event created! :D")

    @event_group.command(name="delete", aliases=["del"])
    async def delete_event(self, ctx: Context, *, summary: str):
        event_id = cal.find_event_by_name(self.credentials, summary).get("id")
        if not event_id:
            return await ctx.send(content="No event was found! :s")

        cal.delete_event(self.credentials, event_id)
        await ctx.send(content="Event deleted! :(")


def setup(bot: Bot) -> None:
    """Load the Calendar cog."""
    creds = botaclan.google.auth.generate_credentials(
        botaclan.constants.GOOGLEAPI_APPLICATION_CREDENTIALS
    )
    bot.add_cog(Calendar(bot, creds))
