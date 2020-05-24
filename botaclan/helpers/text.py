from typing import List
import re


def parse_comma_list_message(message: str) -> List[str]:
    return [item.strip() for item in message.split(",")]


def validate_email_address(email: str) -> bool:
    email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    return bool(re.search(email_regex, email))
