from django.core.validators import URLValidator, ValidationError, EmailValidator
from typing import List


def parse_comma_list_message(message: str) -> List[str]:
    return [item.strip() for item in message.split(",")]


def validate_url(url: str) -> bool:
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError:
        return False


def validate_email_address(email: str) -> bool:
    validate = EmailValidator()
    try:
        validate(email)
        return True
    except ValidationError:
        return False
