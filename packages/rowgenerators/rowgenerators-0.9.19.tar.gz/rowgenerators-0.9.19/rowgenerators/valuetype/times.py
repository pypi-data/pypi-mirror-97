"""


Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of
the Revised BSD License, included in this distribution as LICENSE.txt

"""

from .core import *
import re
from datetime import date, time, datetime
from  dateutil.parser import parse

def cast_date(v, header_d, errors):

    if v is None or v is NoneValue or v == '':
        return None
    elif isinstance(v, FailedValue):
        pass
    elif isinstance(v, date):
        return v
    elif isinstance(v, ValueType):
        return v.__date__()
    elif isinstance(v, str):
        return parse(v).date

    errors[header_d].add(u"Failed to cast '{}' ({}) to date in '{}': {}".format(v, type(v), header_d, v.exc))
    count_errors(errors)
    return None


def cast_datetime(v, header_d, errors):

    if v is None or v is NoneValue or v == '':
        return None
    elif isinstance(v, datetime):
        return v
    elif isinstance(v, ValueType):
        return v.__datetime__()
    elif isinstance(v, str):
        return parse(v)
    elif isinstance(v, Exception):
        errors[header_d].add(u"Failed to cast '{}' ({}) to datetime in '{}': {}".format(v, type(v), header_d, v.exc))
        count_errors(errors)
    else:
        raise Exception("Unknown value! type={} value={}".format(type(v),v))

    return None


def cast_time(v, header_d, errors):
    if v is None or v is NoneValue or v == '':
        return None
    elif isinstance(v, time):
        return v
    elif isinstance(v, ValueType):
        return v.__time__()
    elif isinstance(v, str):
        return parse(v).time

    errors[header_d].add(u"Failed to cast '{}' ({}) to time in '{}': {}".format(v, type(v), header_d, v.exc))
    count_errors(errors)
    return None



class TimeVT(TimeValue, TimeMixin):
    role = ROLE.DIMENSION
    vt_code = 'dt/time'
    desc = 'Time'
    lom = LOM.ORDINAL


class DateVT(DateValue, TimeMixin):
    role = ROLE.DIMENSION
    vt_code = 'dt/date'
    desc = 'Date'
    lom = LOM.ORDINAL

    def __init__(self, v):
        super(DateVT, self).__init__(v)





class DateTimeVT(DateTimeValue, TimeMixin):
    role = ROLE.DIMENSION
    vt_code = 'dt/datetime'
    desc = 'Date and time'
    lom = LOM.ORDINAL



class YearValue(IntValue, TimeMixin):
    """Time interval of a single year"""
    role = ROLE.DIMENSION
    vt_code = 'year'
    desc = 'Single year Interval'
    lom = LOM.ORDINAL

    year_re = re.compile(r'^(\d{4})$')

    def __new__(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return NoneValue

        return IntValue.__new__(cls, v)

    @property
    def start(self):
        return int(self)

    @property
    def end(self):
        return int(self) + 1


class MonthValue(IntValue, TimeMixin):
    """A month"""
    role = ROLE.DIMENSION
    vt_code = 'month'
    desc = 'A month'
    lom = LOM.ORDINAL

class YearRangeValue(StrDimension, TimeMixin):
    """A half-open time interval between two years"""

    vt_code = 'year/range'
    desc = 'Year range interval'
    lom = LOM.ORDINAL

    y1 = None
    y2 = None

    year_range_re = re.compile(r'(\d{4})(?:\/|-|--)(\d{4})')  # / and -- make it also an ISO interval

    def __new__(cls, v):

        if v is None or (isinstance(v, str) and v.strip() == ''):
            return NoneValue

        o = StrValue.__new__(cls, v)

        if isinstance(v, (int, float)):
            o.y1 = v
            o.y2 = v + 1
            return o

        if isinstance(v, str):
            v = v.strip()

        m = YearValue.year_re.match(v)

        if m:
            o.y1 = int(m.group(1))
            o.y2 = o.y1 + 1

            return o

        m = YearRangeValue.year_range_re.match(v)

        if m:
            o.y1 = int(m.group(1))
            o.y2 = int(m.group(2))

            return o

        return FailedValue(v, ValueError("YearRangeValue failed to match year range"))

    @property
    def start(self):
        return int(self.y1)

    @property
    def end(self):
        return int(self.y2)

    def __str__(self):
        return str(self.y1) + '/' + str(self.y2)


class IntervalValue(StrDimension, TimeMixin):
    """A generic time interval. A single year, year range, or an ISO Interval"""
    vt_code = 'interval'
    desc = 'Time interval'
    lom = LOM.ORDINAL

    year_range_re = re.compile(r'(\d{4})(?:\/|-|--)(\d{4})')  # / and -- make it also an ISO interval

    def __new__(cls, v):

        if v is None or (isinstance(v, str) and v.strip() == ''):
            return NoneValue

        # P1Y1D: This is probably

        if isinstance(v, (int, float)):
            return IntervalIsoVT('{}/{}'.format(int(v), int(v) + 1))

        if isinstance(v, str):
            v = v.strip()

        m = YearValue.year_re.match(v)

        if m:
            return IntervalIsoVT('{}/{}'.format(int(m.group(1)), int(m.group(1)) + 1))

        m = cls.year_range_re.match(v)

        if m:
            return IntervalIsoVT('{}/{}'.format(m.group(1), m.group(2)))

        return IntervalIsoVT(v)


class IntervalIsoVT(StrValue, TimeMixin):
    role = ROLE.DIMENSION
    vt_code = 'duration/iso'
    desc = 'ISO FOrmat Interval'
    lom = LOM.ORDINAL

    interval = None

    def __new__(cls, *args, **kwargs):
        v = args[0]

        if v is None or (isinstance(v, str) and v.strip() == ''):
            return None

        return StrValue.__new__(cls, *args, **kwargs)

    def __init__(self, v):
        import aniso8601

        self.interval = aniso8601.parse_interval(v)

    def __str__(self):
        return str(self.interval[0]) + '/' + str(self.interval[1])

    @property
    def start(self):
        return self.interval[0]

    @property
    def end(self):
        return self.interval[1]


times_value_types = {
    'date': DateVT,
    'datetime': DateTimeVT,
    'time': TimeVT,
    'year': YearValue,
    'month': MonthValue,
    'year/range': YearRangeValue,
    "interval": IntervalValue,
    "interval/iso": IntervalIsoVT,
}
