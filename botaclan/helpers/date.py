from collections import namedtuple
from datetime import datetime
from typing import Tuple

CustomDate = namedtuple("CustomDate", ["content", "datetime"])


def create_tuple_from_dateparser_found(found: Tuple[str, datetime]) -> CustomDate:
    return CustomDate(*found)
