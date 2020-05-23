import botaclan.helpers.lists


def test_get_first_item_empty_list():
    sent = []
    expected = None

    assert botaclan.helpers.lists.get_first_item(sent) == expected


def test_get_first_item_empty_one_item():
    sent = [1]
    expected = 1

    assert botaclan.helpers.lists.get_first_item(sent) == expected


def test_get_first_item_empty_n_items():
    sent = ["a", "B", {"c": "d"}]
    expected = "a"

    assert botaclan.helpers.lists.get_first_item(sent) == expected
