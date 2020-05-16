import botaclan.helpers.date
import dateparser
import dateparser.search


def test_create_tuple_from_dateparser_found():
    sent_content = "rick e shorts on January 1st 2020 at 2PM for 1 hour"

    expected_start_content = "on January 1st 2020 at 2PM"
    expected_start_datetime = dateparser.parse("2020-01-01T14:00:00")
    expected_end_content = "1 hour"
    expected_end_datetime = dateparser.parse("2020-01-01T15:00:00")

    dates = dateparser.search.search_dates(
        sent_content, settings={"PREFER_DATES_FROM": "future"}
    )

    start, end = map(botaclan.helpers.date.create_tuple_from_dateparser_found, dates)

    assert (start.content, start.datetime, end.content, end.datetime) == (
        expected_start_content,
        expected_start_datetime,
        expected_end_content,
        expected_end_datetime,
    )
