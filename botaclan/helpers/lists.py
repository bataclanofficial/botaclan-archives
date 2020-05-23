from typing import List, T


def get_first_item(items: List[T]) -> T:
    return next(iter(items), None)
