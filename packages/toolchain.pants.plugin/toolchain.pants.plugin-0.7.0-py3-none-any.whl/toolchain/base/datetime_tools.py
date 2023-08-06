# Copyright © 2019 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import datetime

UNIX_EPOCH = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
_date_fmt = "%Y/%m/%d"
_time_fmt = "%H:%M:%S"
_ms_fmt = "%f"


def utcnow() -> datetime.datetime:
    """Return a timezone aware datetime.datetime representing the current moment, in UTC.

    This is based on django.utils.timezone.now(), but without dragging django as a dependency to places that need this.
    """
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def datetime_fmt_std(dt, abbrev=False, ms=False):
    if dt is None:
        return None
    if dt == UNIX_EPOCH:
        return "-"
    dt = dt.astimezone(datetime.timezone.utc)
    if abbrev and dt.date() == utcnow().date():
        fmt = _time_fmt
    else:
        fmt = f"{_date_fmt} {_time_fmt}"
    if ms:
        fmt += f".{_ms_fmt}"
        return dt.strftime(fmt)[:-3]
    return dt.strftime(fmt)


def seconds_from_now(dt):
    now = utcnow()
    if dt is None or dt <= now:
        return 0
    else:
        return (dt - now).seconds
