from google.oauth2 import service_account
from googleapiclient.discovery import build
from botaclan.constants import GOOGLEAPI_CALENDAR_ID
import botaclan.helpers as helpers
import datetime
import logging

log = logging.getLogger(__name__)


def list_events(credentials: service_account.Credentials, max_results: int = 10):
    cal = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = (
        cal.events()
        .list(
            calendarId=GOOGLEAPI_CALENDAR_ID,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return events


def create_event(credentials: service_account.Credentials, event: dict):
    cal = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    cal.events().insert(calendarId=GOOGLEAPI_CALENDAR_ID, body=event).execute()


def delete_event(credentials: service_account.Credentials, id: str):
    cal = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    cal.events().delete(calendarId=GOOGLEAPI_CALENDAR_ID, eventId=id).execute()


def find_event_by_name(credentials: service_account.Credentials, name: str):
    cal = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = (
        cal.events()
        .list(
            calendarId=GOOGLEAPI_CALENDAR_ID,
            timeMin=now,
            maxResults=1,
            singleEvents=True,
            orderBy="startTime",
            q=name,
        )
        .execute()
    )
    events = events_result.get("items", [])
    return helpers.lists.get_first_item(events)


if __name__ == "__main__":
    pass
