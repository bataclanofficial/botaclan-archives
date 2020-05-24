from discord import Embed
from botaclan.constants import (
    GOOGLEAPI_APPLICATION_CREDENTIALS,
    TIMEZONE,
)
from discord.ext.commands import Cog, Bot, Context, group
from google.oauth2 import service_account
import botaclan.constants.default as default
import botaclan.google.auth
import botaclan.google.google_calendar as cal
import botaclan.helpers.date
import botaclan.helpers.lists
import dateparser.search
import logging
import re


log = logging.getLogger(__name__)


class Calendar(Cog):
    def __init__(self, bot: Bot, credentials: service_account.Credentials):
        self.bot = bot
        self.credentials = credentials

    @group(name="event")
    async def event_group(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(content="Event help here")

    @group(name="calendar")
    async def calendar_group(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(content="Calendar help here")

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
    async def create_event(self, ctx: Context, *, content: str):
        dates_found = dateparser.search.search_dates(
            content, settings={"PREFER_DATES_FROM": "future"}
        )
        log.debug(dates_found)

        if not dates_found:
            log.warn(f"{content} - Problem parsing and searching a date range")
            return await ctx.send(
                content="Your event is expected to have a start and an end date :("
            )

        required_amount_of_dates = 2
        if len(dates_found) != required_amount_of_dates:
            log.warn(f"{content} - Less than 2 dates were specified")
            return await ctx.send(
                content="Your event is expected to have a start and an end date :("
            )

        start, end = map(
            botaclan.helpers.date.create_tuple_from_dateparser_found, dates_found
        )
        if not start or not end:
            log.warn(f"{content} - Start date or end date failed to be parsed")
            return await ctx.send(
                content="Your event is expected to have a start and an end date :("
            )

        regex_datetimes = "|".join([start.content, end.content])
        content_without_datetimes = re.split(regex_datetimes, content)
        summary = botaclan.helpers.lists.get_first_item(content_without_datetimes)
        if not summary:
            log.warn(f"{content} - Event missing summary")
            return await ctx.send(content="Your event is missing a summary :(")

        event = {
            "start": {"dateTime": start.datetime.isoformat(), "timeZone": TIMEZONE},
            "end": {"dateTime": end.datetime.isoformat(), "timeZone": TIMEZONE},
            "summary": summary.strip(),
        }
        log.debug(event)
        cal.create_event(self.credentials, event)
        await ctx.send(content="Event created! :D")

    @event_group.command(name="delete", aliases=["del"])
    async def delete_event(self, ctx: Context, *, summary: str):
        event = cal.find_event_by_name(self.credentials, summary)
        if not event:
            return await ctx.send(content="No event was found! :s")
        cal.delete_event(self.credentials, event.get("id"))
        await ctx.send(content="Event deleted! :(")

    @calendar_group.command(name="subscribe", aliases=["sub"])
    async def subscribe_to_calendar(self, ctx: Context, role: str, email: str):
        if (
            role not in default.SUPPORTED_GOOGLEAPI_CALENDAR_ROLES
            or not botaclan.helpers.text.validate_email_address(email)
        ):
            return await ctx.send(content="Enter a valid email address and role :(")
        generated_rule = cal.generate_user_acl_rule(role, email)
        cal.subscribe_to_calendar(self.credentials, generated_rule)
        await ctx.send(
            content=(
                "User subscribed to the calendar. "
                "A confirmation email was sent and needs to be accepted :)"
            )
        )

    @calendar_group.command(name="unsubscribe", aliases=["unsub"])
    async def unsubscribe_to_calendar(self, ctx: Context, role: str, email: str):
        if (
            role not in default.SUPPORTED_GOOGLEAPI_CALENDAR_ROLES
            or not botaclan.helpers.text.validate_email_address(email)
        ):
            return await ctx.send(content="Enter a valid email address and role :(")
        generated_rule = cal.generate_user_acl_rule(role, email)

        rules_found = cal.find_acl_by_rule(self.credentials, generated_rule)
        if not rules_found:
            return await ctx.send(
                content="No user was found with this permission and email :s"
            )

        for rule in rules_found:
            cal.unsubscribe_to_calendar(self.credentials, rule.get("id", None))
        await ctx.send(content="User unsubscribed to the calendar :)")


def setup(bot: Bot) -> None:
    """Load the Calendar cog."""
    creds = botaclan.google.auth.generate_credentials(GOOGLEAPI_APPLICATION_CREDENTIALS)
    bot.add_cog(Calendar(bot, creds))
    log.info("Cog loaded: Calendar")
