import datetime
from typing import Optional

import pendulum


def convert_to_int(value) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return None


def convert_to_str(value) -> Optional[str]:
    try:
        return str(value)
    except ValueError:
        return None


def convert_to_bool(value) -> Optional[bool]:
    try:
        return bool(value)
    except ValueError:
        return None


def convert_to_date(value) -> Optional[datetime.date]:
    if isinstance(value, datetime.date):
        return value
    elif isinstance(value, datetime.datetime):
        return value.date()
    else:
        try:
            return datetime.datetime.fromordinal(
                pendulum.parse(value).toordinal()
            ).date()
        except ValueError:
            return None


def convert_to_datetime(value) -> Optional[datetime.datetime]:
    if isinstance(value, datetime.datetime):
        return value
    elif isinstance(value, datetime.date):
        return datetime.datetime.fromordinal(value.toordinal())
    else:
        try:
            return datetime.datetime.fromordinal(pendulum.parse(value).toordinal())
        except ValueError:
            return None
