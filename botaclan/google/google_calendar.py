from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import botaclan.constants


def main():
    creds = service_account.Credentials.from_service_account_file(
        botaclan.constants.GOOGLEAPI_APPLICATION_CREDENTIALS
    )
    cal = build("calendar", "v3", credentials=creds, cache_discovery=False)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    print("Getting the upcoming 10 events")
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

    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


if __name__ == "__main__":
    pass
