import botaclan.google.google_calendar as cal


def test_remove_generated_acl_fields():
    sent = {
        "kind": "calendar#aclRule",
        "etag": '"00000000000000000000"',
        "id": "user:john.mayer@blues.org",
        "scope": {"type": "user", "value": "john.mayer@blues.org"},
        "role": "owner",
    }
    expected = {
        "scope": {"type": "user", "value": "john.mayer@blues.org"},
        "role": "owner",
    }

    assert cal.remove_generated_acl_fields(sent) == expected


def test_generate_user_acl_rule():
    sent = ("writer", "john.mayer@blues.org")
    expected = {
        "scope": {"type": "user", "value": "john.mayer@blues.org"},
        "role": "writer",
    }

    assert cal.generate_user_acl_rule(*sent) == expected
