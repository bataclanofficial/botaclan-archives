from collections import namedtuple
from typing import NamedTuple


def create_tuple_from_dateparser_found(found: tuple) -> NamedTuple:
    return namedtuple("custom_date", ["content", "datetime"])(*found)
