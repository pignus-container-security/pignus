"""Date Utilities

"""
from datetime import datetime

import arrow


def now() -> datetime:
    """Short hand to get now as UTC.
    :unit-test: TestDateUtils.test__now
    """
    return arrow.utcnow().datetime


def json_date(the_datetime: datetime) -> str:
    """Get a JSON returnable value from a datetime.
    :unit-test: TestDateUtils.test__json_date
    """
    if not the_datetime:
        return None
    return arrow.get(the_datetime).format('YYYY-MM-DD HH:mm:ss ZZ')


def human_date(the_datetime: str) -> str:
    """Get a human date from a Datetime object, such as "2 hours ago".
    :unit-test: TestDateUtils.test__human_date
    """
    if not the_datetime:
        return None
    if isinstance(the_datetime, str) and "+00:00" in the_datetime:
        the_datetime = the_datetime.replace("+00:00", "")
        the_datetime = the_datetime.strip()
    return arrow.get(the_datetime).humanize()


def get_as_utc(a_datetime: datetime):
    """Convert a datetime into a UTC Arrow object.
    :unit-test: TestDateUtils.test__get_as_utc
    """
    a_utc_time = arrow.get(a_datetime)
    return a_utc_time.to('UTC')


def get_aws_epoch(a_datetime: arrow.arrow.Arrow) -> int:
    """Get AWS epoch, which is millis since Jan 1 1970. Kinda weird.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_log_events
    :unit-test: TestDateUtils.test__get_aws_epoch
    """
    epoch_start = arrow.get(1970, 1, 1)
    diff = a_datetime - epoch_start
    diff_millis = diff.total_seconds() * 1000
    return int(round(diff_millis, 0))


def date_from_json(the_datetime: str, parse_fmt: str = None) -> datetime:
    """Convert a string into a python dative datetime object.
    :unit-test: TestDateUtils.test__date_from_json
    """
    if not the_datetime:
        return None
    if not parse_fmt:
        parse_fmt = "YYYY-MM-DD HH:mm:ss ZZ"
    try:
        ret_datetime = arrow.get(the_datetime, parse_fmt)
    except arrow.parser.ParserError:
        ret_datetime = None
    return ret_datetime


def interval_ready(last: datetime, interval_hours: int) -> bool:
    """Determine in a given datetime is older than the interval_hours.
    :unit-test: TestDateUtils.test__interval_ready
    """
    now = arrow.utcnow()
    last = arrow.get(last)
    interval_seconds = 3600 * interval_hours
    diff = (now - last).total_seconds()
    if diff > interval_seconds:
        return True
    else:
        return False


def date_hours_ago(interval_hours: int) -> datetime:
    """Determine in a given datetime is older than the interval_hours.
    :unit-test: TestDateUtils.date_hours_ago
    """
    now = arrow.utcnow()
    sync_interval = interval_hours * -1 * 3600
    the_date_then = now.shift(seconds=sync_interval)
    return the_date_then.datetime


def expire_date():
    now = arrow.utcnow()
    future = now.shift(hours=8)
    return future

# End File: pignus/src/pignus_api/utils/date_utils.py
