import datetime
from warnings import warn

try:
    import pytz
except ImportError:
    warn(
        "pytz is not found and it is used in some methods inside this library",
        ImportWarning,
    )


def get_iso_week_day(date: datetime.datetime, timezone: str) -> int:
    """Function to return the iso weekday.
    :param datetime.datetime date: A date in UTC

    :param str timezone: The timezone to be applied to the date
    :rtype: int
    :return: Returns the iso weekday of the date, being:
        0 = Sunday
        1 = Monday
        2 = Tuesday
        3 = Wednesday
        4 = Thursday
        5 = Friday
        6 = Saturday

    """
    pst = pytz.timezone(timezone)
    return pst.fromutc(date).isoweekday() % 7


def datetime_with_timezone(
    *, datetime: datetime.datetime, timezone: str
) -> datetime.datetime:
    """Function to add a timezone to a specified datetime.

    :param datetime.datetime datetime: The datetime in UTC.
    :param str timezone: The timezone to be applied to the datetime.
    :rtype: datetime.datetime.
    :return: A new datetime with a timezone.

    """
    pst = pytz.timezone(timezone)
    return pst.fromutc(datetime)


def date_to_datetime(*, date: datetime.date) -> datetime.datetime:
    """Converts a date to a datetime, with time being 00:00:00.
    :param datetime.date date: The date to take as the base of the new datetime
    :rtype: datetime.datetime.
    :return: A new datetime, being the date equal to the parameter and the time to 00:00:00.

    """
    return datetime.datetime(date.year, date.month, date.day, 0, 0, 0)


def local_date_to_utc(*, date: datetime.date, timezone: str) -> datetime.datetime:
    """Function to convert a local date to UTC.
    :param date datetime.date: A normal date which is supposed to be in the local user's time.
    :param str timezone: The timezone on which the date is supposed to be.
    :rtype: datetime.datetime.
    :return: A datetime in UTC with tzinfo.

    """
    return (
        pytz.timezone(timezone)
        .localize(datetime.datetime(date.year, date.month, date.day))
        .astimezone(pytz.utc)
    )
