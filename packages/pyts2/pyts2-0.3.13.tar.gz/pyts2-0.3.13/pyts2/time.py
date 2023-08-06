# Copyright (c) 2018 Kevin Murray <kdmfoss@gmail.com>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import calendar
import re
import os.path as op


TS_DATEFMT = "%Y_%m_%d_%H_%M_%S"
TS_DATETIME_RE = re.compile(r"(\d\d\d\d[._\- ]?\d\d[._\- ]?\d\d[._\- T]?\d\d[._\- :]?\d\d[._\- :]?\d\d)(_\w+)?")



def parse_date(datestr):
    """Parses dates in iso8601-ish formats to :class:`datetime.datetime` objects

    :param datestr: A string containing a datetime
    :type datestr: str
    :return: Datetime object representing the given string
    :rtype: :class:`datetime.datetime` object
    """
    if isinstance(datestr, datetime.datetime):
        return datestr

    valid_formats = [
        "%Y-%m-%dT%H-%M-%S%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y_%m_%d_%H_%M_%S",
        "%Y_%m_%d_%H%M%S",
        "%Y%m%d_%H%M%S",
        "%Y%m%d%H%M%S",
        "%Y-%m-%d_%H:%M:%S",
        "%Y-%m-%d_%H-%M-%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H-%M-%S",
        "%Y_%m_%d_%H_%M",
        "%Y_%m_%d_%H%M",
        "%Y%m%d_%H%M",
        "%Y%m%d%H%M",
        "%Y-%m-%d_%H:%M",
        "%Y_%m_%d_%H",
        "%Y_%m_%d",
        "%Y-%m-%d",
    ]
    for fmt in valid_formats:
        try:
            return datetime.datetime.strptime(datestr, fmt)
        except:
            pass

    # Add more things here in try-excepts if we want to accept other date
    # formats

    raise ValueError("date string '" + datestr + "' doesn't match valid date formats")


class TSInstant(object):
    """
    TSInstant: a generalised "moment in time", including both timepoint and
    optional index within a timepoint.

    >>> TSInstant(datetime.datetime(2017,  1,  2,  3,  4,  5))
    2017_01_02_03_04_05
    >>> TSInstant(datetime.datetime(2017,  1,  2,  3,  4,  5), "0011")
    2017_01_02_03_04_05_0011
    """

    def __init__(self, datetime, index=None):
        """ Initiates at a given datetime and optional index within that timepoint.

        :param datetime: A string in an ISO-8601-like format. (see :func:`~parse_date`)
        :type datetime: str
        :param index: Index number
        :type index: int or string containing a usable int, optional
        """
        self.datetime = parse_date(datetime)
        self.index = index

    @property
    def index(self):
        """ Index of timepoint.

        :setter: Converts to int, stripping underscores if needed. Sets to None if 00 or empty string.
        """
        if isinstance(self._index, int):
            return f"{self._index:04d}"
        return self._index

    @index.setter
    def index(self, val):
        if val is None or val == "_00" or val == "":
            self._index = None
            return
        if val.startswith("_00_"):
            val = val[4:]
        val = val.lstrip("_")
        try:
            self._index = int(val)
        except (TypeError, ValueError):
            self._index = val

    def __str__(self):
        idx = f"_{self.index}" if self.index is not None else ""
        return f"{self.datetime.strftime('%Y_%m_%d_%H_%M_%S')}{idx}"

    def __eq__(self, other):
        return (self.datetime, self.index) == \
               (other.datetime, other.index)

    def __lt__(self, other):
        if self.index is not None and other.index is not None:
            return (self.datetime, self.index) < \
                (other.datetime, other.index)
        else:
            return (self.datetime,) < \
                (other.datetime,)

    def __le__(self, other):
        if self.index is not None and other.index is not None:
            return (self.datetime, self.index) <= \
                (other.datetime, other.index)
        else:
            return (self.datetime,) <= \
                (other.datetime,)

    def __gt__(self, other):
        if self.index is not None and other.index is not None:
            return (self.datetime, self.index) > \
                (other.datetime, other.index)
        else:
            return (self.datetime,) > \
                (other.datetime,)

    def __ge__(self, other):
        if self.index is not None and other.index is not None:
            return (self.datetime, self.index) >= \
                (other.datetime, other.index)
        else:
            return (self.datetime,) >= \
                (other.datetime,)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def iso8601(self):
        """ Converts own datetime to a ISO-8601 string.

        :return: Datetime string in ISO-8601 format.
        :rtype: str
        """
        return self.datetime.strftime("%Y-%m-%dT%H:%M:%S")

    @classmethod
    def now(cls):
        """ Get current time.

        :return: Current timepoint
        :rtype: :class:`TSInstant`
        """
        return cls(datetime.datetime.now())

    @staticmethod
    def from_path(path):
        """Extract date and index from path to timestream image

        :param path: File path, with or without directory
        :type path: str
        :return: Datetime indicated by path
        :rtype: :class:`TSInstant`

        >>> TSInstant.from_path("2001_02_03_23_59_59_00.jpg")
        2001_02_03_23_59_59
        >>> TSInstant.from_path("2001_02_03_23_59_59_indexhere.jpg")
        2001_02_03_23_59_59_indexhere
        """
        fn = op.splitext(op.basename(path))[0]
        m = TS_DATETIME_RE.search(fn)
        if m is None:
            raise ValueError("path '" + path + "' doesn't contain a timestream date")

        dt, index = m.groups()

        datetime = parse_date(dt)

        return TSInstant(datetime, index)


def parse_partial_date(datestr, max=False):
    """ Parses date strings with implicit date format.

    :param datestr: A string that contains a date.
    :type datestr: str
    :param max: Default to maximum value within possible date range (e.g. if date only has up to hour precision, set minutes field to 59)
    :type max: bool
    :return: Date, time
    :rtype: :class:`datetime.datetime`, :class:`datetime.datetime`
    """
    m = re.search(r"_?(?P<Y>\d\d\d\d)(?:_(?P<m>\d\d)(?:_(?P<d>\d\d))?(?:_(?P<H>\d\d))?(?:_(?P<M>\d\d))?(?:_(?P<S>\d\d))?)?",
                  datestr)
    if m is None:
        raise ValueError("date string '" + datestr + "' doesn't match date formats")
    d = datetime.date.max if max else datetime.date.min
    t = None

    if m["Y"]:
        d = d.replace(year=int(m["Y"]))
    if m["m"]:
        # because not all months have the same length, we have to calculate the maximum day of this
        # month by hand
        yr, mth = int(m["Y"]), int(m["m"])
        day = calendar.monthrange(yr, mth)[1] if max else 1
        d = d.replace(month=int(m["m"]), day=day)
    if m["d"]:
        d = d.replace(day=int(m["d"]))
    if m["H"]:
        t = datetime.time.max if max else datetime.time.min
        t = t.replace(hour=int(m["H"]))
    if m["M"]:
        t = t.replace(minute=int(m["M"]))
    if m["S"]:
        t = t.replace(second=int(m["S"]))
    return d, t


class TimeFilter(object):
    """ Check datetimes fall within a given time period.
    """
    def __init__(self, startdate=None, enddate=None, starttime=None, endtime=None):
        """ Initiates with a datetime range to check against.

        :param startdate: Start of date range.
        :type startdate: ``datetime.date`` object, :class:`.TSinstant` object, or date string.
        :param enddate: End of date range Must be later than ``startdate``.
        :type enddate: ``datetime.date`` object, :class:`.TSinstant` object, or date string.
        :param startime: Start of time range per day within date range.
        :type startime: ``datetime.time`` object, :class:`.TSinstant` object, or time string.
        :param endtime: End of time range per day within date range. Must be later than ``starttime``.
        :type endtime: ``datetime.time`` object, :class:`.TSinstant` object, or time string.
        """
        def convert_date(d):
            if isinstance(d, datetime.date):
                return d
            elif isinstance(d, TSInstant):
                return d.datetime.date()
            elif isinstance(d, datetime.datetime):
                return d.date()
            elif isinstance(d, str):
                return parse_date(d).date()
            elif d is None:
                return None
            else:
                TypeError("Bad date")

        def convert_time(t):
            if isinstance(t, datetime.time):
                return t
            elif isinstance(t, TSInstant):
                return t.datetime.time()
            elif isinstance(t, datetime.datetime):
                return t.time()
            elif isinstance(t, str):
                return parse_date(t).time()
            elif t is None:
                return None
            else:
                TypeError("Bad date")

        self.startdate = convert_date(startdate)
        self.enddate = convert_date(enddate)
        if self.startdate is not None and self.enddate is not None and self.startdate > self.enddate:
            raise ValueError("Can't have startdate > enddate")

        self.starttime = convert_time(starttime)
        self.endtime = convert_time(endtime)
        if self.starttime is not None and self.endtime is not None and self.starttime > self.endtime:
            raise ValueError("Can't have starttime > endtime")

    def __call__(self, datetime):
        d = datetime.date()
        t = datetime.time()
        if self.startdate is not None and d < self.startdate:
            return False
        if self.enddate is not None and d > self.enddate:
            return False
        if self.starttime is not None and t < self.starttime:
            return False
        if self.endtime is not None and t > self.endtime:
            return False
        return True

    def partial_within(self, datestr):
        """ Checks if a given datetime is within the datetime range of the current object.

        :param datestr: String of datetime to check.
        :type datestr: str
        :return: True if within datetime range, False if not
        :rtype: bool
        """
        dmin, tmin = parse_partial_date(datestr, max=False)
        dmax, tmax = parse_partial_date(datestr, max=True)

        if self.startdate is not None and dmax < self.startdate:
            return False
        if self.enddate is not None and dmin > self.enddate:
            return False
        if self.starttime is not None and tmax is not None and tmax < self.starttime:
            return False
        if self.endtime is not None and tmin is not None and tmin > self.endtime:
            return False
        return True
