from google.oauth2 import service_account
from googleapiclient.discovery import build
import botaclan.constants
import datetime
import logging

log = logging.getLogger(__name__)


def list_events(credentials: service_account.Credentials):
    cal = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = (
        cal.events()
        .list(
            calendarId=botaclan.constants.GOOGLEAPI_CALENDAR_ID,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return events


if __name__ == "__main__":
    pass
