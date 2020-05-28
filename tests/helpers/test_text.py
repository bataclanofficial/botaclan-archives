import botaclan.helpers.text


def test_parse_comma_list_message():
    sent = " a,b, c, D, e"
    expected = ["a", "b", "c", "D", "e"]

    assert botaclan.helpers.text.parse_comma_list_message(sent) == expected


def test_validate_email_address_existing_email():
    sent = "justin.roiland@my.heart"
    expected = True
    assert botaclan.helpers.text.validate_email_address(sent) == expected


def test_validate_email_address_non_existing_mail():
    sent = "not.working.hello.com"
    expected = False
    assert botaclan.helpers.text.validate_email_address(sent) == expected


def test_validate_url_existent():
    sent = "https://youtu.be/myrandomidhere"
    expected = True
    assert botaclan.helpers.text.validate_url(sent) == expected


def test_validate_url_inexistent():
    sent = "this should not https://work.here"
    expected = False
    assert botaclan.helpers.text.validate_url(sent) == expected
