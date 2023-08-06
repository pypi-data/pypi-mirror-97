"""Math functions available for use in derivedfrom columns

Copyright (c) 2015 Civic Knowledge. This file is licensed under the terms of
the Revised BSD License, included in this distribution as LICENSE.txt

"""

import datetime
import dateutil.parser as dp

from .measures import IntValue, FloatValue, DateValue



class NullValue(Exception):
    """Raised from a caster to indicate that the returned value should be None"""


def transform_generator(fn):
    """A decorator that marks transform pipes that should be called to create the real transform"""
    fn.__dict__['is_transform_generator'] = True
    return fn


def is_transform_generator(fn):
    """Return true of the function has been marked with @transform_generator"""
    try:
        return fn.__dict__.get('is_transform_generator', False)
    except AttributeError:
        return False


def row_number(row_n):
    return row_n


def nullify(v):
    """Convert empty strings and strings with only spaces to None values. """

    if isinstance(v, str):
        v = v.strip()

    if v is None or v == '':
        return None
    else:
        return v


def clean_float(v):
    """Remove commas from a float"""

    if v is None or not str(v).strip():
        return None

    return float(str(v).replace(',', '').replace(' ',''))


def clean_int(v):
    """Remove commas from a float"""

    if v is None or not str(v).strip():
        return None

    return int(str(v).replace(',', '').replace(' ',''))


#
# Casters that return a default value
#
def int_d(v, default=None):
    """Cast to int, or on failure, return a default Value"""

    try:
        return int(v)
    except:
        return default


def float_d(v, default=None):
    """Cast to int, or on failure, return a default Value"""

    try:
        return float(v)
    except:
        return default


#
# Casters that return a null on failure
#

def int_n(v):
    """Cast to int, or on failure, return a default Value"""

    try:
        return int(float(v))
    except:
        return None


def float_n(v):
    """Cast to float, or on failure, return None"""

    try:
        return float(v)  # Just to be sure the code property exists
    except:
        return None


def int_e(v):
    """Cast to int, or on failure raise a NullValue exception"""

    try:
        return int(v)
    except:
        raise NullValue(v)


def parse_int(v, header_d):
    """Parse as an integer, or a subclass of Int."""
    from rowgenerators.rowpipe.exceptions import CastingError

    v = nullify(v)

    if v is None:
        return None

    try:
        # The converson to float allows converting float strings to ints.
        # The conversion int('2.134') will fail.
        return int(round(float(v), 0))
    except (TypeError, ValueError) as e:
        raise CastingError(int, header_d, v, 'Failed to cast to integer')


def parse_float(v, header_d):
    from rowgenerators.rowpipe.exceptions import CastingError

    v = nullify(v)

    if v is None:
        return None

    try:
        return float(v)
    except (TypeError, ValueError) as e:
        raise CastingError(float, header_d, v, str(e))


def parse_str(v, header_d):
    # TODO: It's so complicated while py2/py3 work because str is binary for py2, but unicode for py3.

    # This is often a no-op, but it ocassionally converts numbers into strings

    v = nullify(v)

    if v is None:
        return None

    return _parse_text(v, header_d)


def parse_bytes(v, header_d):
    return _parse_binary(v, header_d)


def parse_unicode(v, header_d):
    return _parse_text(v, header_d)


def parse_type(type_, v, header_d):
    from rowgenerators.rowpipe.exceptions import CastingError

    v = nullify(v)

    if v is None:
        return None

    try:
        return type_(v)
    except (TypeError, ValueError) as e:
        raise CastingError(type_, header_d, v, str(e))


def parse_date(v, header_d):
    from rowgenerators.rowpipe.exceptions import CastingError

    v = nullify(v)

    if v is None:
        return None

    if isinstance(v, str):
        try:
            return dp.parse(v).date()
        except (ValueError, TypeError) as e:
            raise CastingError(datetime.date, header_d, v, str(e))

    elif isinstance(v, datetime.date):
        return v
    else:
        raise CastingError(int, header_d, v, "Expected datetime.date or basestring, got '{}'".format(type(v)))


def parse_time(v, header_d):
    from rowgenerators.rowpipe.exceptions import CastingError

    v = nullify(v)

    if v is None:
        return None

    if isinstance(v, str):
        try:
            return dp.parse(v).time()
        except ValueError as e:
            raise CastingError(datetime.time, header_d, v, str(e))

    elif isinstance(v, datetime.time):
        return v
    else:
        raise CastingError(int, header_d, v, "Expected datetime.time or basestring, got '{}'".format(type(v)))


def parse_datetime(v, header_d):
    from rowgenerators.rowpipe.exceptions import CastingError

    v = nullify(v)

    if v is None:
        return None

    if isinstance(v, str):
        try:
            return dp.parse(v)
        except (ValueError, TypeError) as e:
            raise CastingError(datetime.datetim, header_d, v, str(e))

    elif isinstance(v, datetime.datetime):
        return v
    else:
        raise CastingError(int, header_d, v, "Expected datetime.time or basestring, got '{}'".format(type(v)))


class IntOrNone(IntValue):
    "An Integer value that stores values that fail to convert in the 'code' property"
    _pythontype = int

    code = None

    def __new__(cls, v):
        try:
            o = super(IntOrCode, cls).__new__(cls, v)
        except Exception as e:
            o = super(IntOrCode, cls).__new__(cls, None)
            o.code = v
        return o


class FloatOrNone(FloatValue):
    "An Float value that stores values that fail to convert in the 'code' property"
    _pythontype = float

    code = None

    def __new__(cls, v):
        try:
            o = super(FloatOrCode, cls).__new__(cls, v)
        except Exception as e:
            o = super(FloatOrCode, cls).__new__(cls, None)
            o.code = v
        return o


class IntOrCode(IntValue):
    "An Integer value that stores values that fail to convert in the 'code' property"
    _pythontype = int

    code = None

    def __new__(cls, v):
        try:
            o = super(IntOrCode, cls).__new__(cls, v)
        except Exception as e:
            o = super(IntOrCode, cls).__new__(cls, 0)
            o.code = v
        return o


class FloatOrCode(FloatValue):
    "An Float value that stores values that fail to convert in the 'code' property"
    _pythontype = float

    code = None

    def __new__(cls, v):
        try:
            o = super(FloatOrCode, cls).__new__(cls, v)
        except Exception as e:
            o = super(FloatOrCode, cls).__new__(cls, float('nan'))
            o.code = v
        return o


class DateOrCode(DateValue):
    "An Integer value that stores values that fail to convert in the 'code' property"
    _pythontype = datetime.date

    code = None

    def __new__(cls, v):
        try:
            o = super(DateOrCode, cls).__new__(cls, v)
        except Exception as e:
            o = super(DateOrCode, cls).__new__(cls, None)
            o.code = v
        return o


class ForeignKey(IntValue):
    """An Integer value represents a foreign key on another table.  The value can hold a linked row for access from other
    columns. """

    _pythontype = int

    row = None

    def __new__(cls, v):
        o = super(ForeignKey, cls).__new__(cls, v)
        return o

    def __init__(self, v):
        super(ForeignKey, self).__init__()
        self.row = None


def _parse_text(v, header_d):
    """ Parses unicode.

    Note:
        unicode types for py2 and str types for py3.

    """

    from rowgenerators.rowpipe.exceptions import CastingError

    v = nullify(v)

    if v is None:
        return None

    try:
        return str(v).strip()
    except Exception as e:
        raise CastingError(str, header_d, v, str(e))


def _parse_binary(v, header_d):
    """ Parses binary string.

    Note:
        <str> for py2 and <binary> for py3.

    """

    # This is often a no-op, but it ocassionally converts numbers into strings

    v = nullify(v)

    if v is None:
        return None

    try:
        return bytes(v, 'utf-8').strip()
    except UnicodeEncodeError:
        return str(v).strip()


def excel_dt_1900(v):
    """Convert a float that representes a date in an excel file into a datetime. The float
    is assumed to have a basis of 1900"""

    from xlrd.xldate import xldate_as_datetime
    return xldate_as_datetime(v, 0)


def excel_dt_1904(v):
    """Convert a float that representes a date in an excel file into a datetime. The float
    is assumed to have a basis of 1904"""

    from xlrd.xldate import xldate_as_datetime
    return xldate_as_datetime(v, 0)


#def date(v):
#    """Convert a date to a datetime"""
#    return v.date()
