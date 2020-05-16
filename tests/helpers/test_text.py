import botaclan.helpers.text


def test_parse_comma_list_message():
    sent = " a,b, c, D, e"
    parsed = ["a", "b", "c", "D", "e"]

    assert botaclan.helpers.text.parse_comma_list_message(sent) == parsed
