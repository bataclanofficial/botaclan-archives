from botaclan.constants import GOOGLEAPI_CALENDAR_ID
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from typing import List, Dict
import botaclan.helpers.lists
import copy
import datetime
import logging

log = logging.getLogger(__name__)


def create_calendar_client(credentials: service_account.Credentials) -> Resource:
    return build("calendar", "v3", credentials=credentials, cache_discovery=False)


def generate_user_acl_rule(role: str, email: str) -> Dict:
    return {
        "scope": {"type": "user", "value": email},
        "role": role,
    }


def remove_generated_acl_fields(rule: Dict) -> Dict:
    modified_rule = copy.deepcopy(rule)
    modified_rule.pop("kind", None)
    modified_rule.pop("etag", None)
    modified_rule.pop("id", None)
    return modified_rule


def list_events(
    credentials: service_account.Credentials, max_results: int = 10
) -> List[Dict]:
    cal = create_calendar_client(credentials=credentials)
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


def create_event(credentials: service_account.Credentials, event: Dict):
    cal = create_calendar_client(credentials=credentials)
    cal.events().insert(calendarId=GOOGLEAPI_CALENDAR_ID, body=event).execute()


def delete_event(credentials: service_account.Credentials, id: str):
    cal = create_calendar_client(credentials=credentials)
    cal.events().delete(calendarId=GOOGLEAPI_CALENDAR_ID, eventId=id).execute()


def find_acl_by_rule(
    credentials: service_account.Credentials, rule: Dict, max_results: int = 100
):
    cal = create_calendar_client(credentials=credentials)
    acl_found = []
    acl_results = (
        cal.acl()
        .list(
            calendarId=GOOGLEAPI_CALENDAR_ID, showDeleted=False, maxResults=max_results,
        )
        .execute()
    )
    acl = acl_results.get("items", [])
    for found_rule in acl:
        if remove_generated_acl_fields(found_rule) == rule:
            acl_found.append(found_rule)
    return acl_found


def find_event_by_name(credentials: service_account.Credentials, name: str) -> Dict:
    cal = create_calendar_client(credentials=credentials)
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
    return botaclan.helpers.lists.get_first_item(events)


def subscribe_to_calendar(credentials: service_account.Credentials, rule: Dict):
    cal = create_calendar_client(credentials=credentials)
    cal.acl().insert(calendarId=GOOGLEAPI_CALENDAR_ID, body=rule).execute()


def unsubscribe_to_calendar(credentials: service_account.Credentials, rule_id: str):
    cal = create_calendar_client(credentials=credentials)
    cal.acl().delete(calendarId=GOOGLEAPI_CALENDAR_ID, ruleId=rule_id).execute()


if __name__ == "__main__":
    pass
