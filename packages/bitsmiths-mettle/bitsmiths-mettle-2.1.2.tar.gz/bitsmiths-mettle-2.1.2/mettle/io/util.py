# **************************************************************************** #
#                           This file is part of:                              #
#                                   METTLE                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/mettle.git                            #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #

import datetime
import uuid

from mettle.lib.timezone import TimeZone


class Util:
    """
    Utility helper class.
    """

    TZ_CACHE = {}

    @staticmethod
    def int_2_date(date: int) -> datetime.date:
        """
        Converts an integer represenation of a date to a datetime.date

        :param date: (int) An integer representing date value (YYYYMMDD)
        :return: The date
        """
        if date == 0:
            return datetime.date.min

        year = (int)(date * 0.0001)
        mon  = (int)((date * 0.01) - (year * 100))
        day  = (int)(date - ((year * 10000) + (mon * 100)))

        return datetime.date(year, mon, day)

    @staticmethod
    def local_tz() -> TimeZone:
        """
        Gets the local time zone.
        """
        loc = Util.TZ_CACHE.get('local')

        if loc is None:
            Util.TZ_CACHE['local'] = loc = TimeZone.local_tz()

        return loc


    @staticmethod
    def utc_tz() -> TimeZone:
        """
        Gets the local time zone.
        """
        loc = Util.TZ_CACHE.get('utc')

        if loc is None:
            Util.TZ_CACHE['utc'] = loc = TimeZone.utc_tz()

        return loc


    @staticmethod
    def int_2_time(time: int) -> datetime.time:
        """
        Converts an integer represenation of time to a datetime.date

        :param time: An integre representing time value (HHMMSS)
        :return: The time
        """
        if time == 0:
            return datetime.time.min

        hour = int(time * 0.0001)
        minu = int(((time * 0.01)) - (hour * 100))
        sec  = int(time - ((hour * 10000) + (min * 100)))

        return datetime.time(hour, minu, sec)


    @staticmethod
    def ints_2_datetime(date: int, time: int, tzhour: int, tzmin: int) -> datetime:
        """
        Converts two integers represenation of datetime to a datetime.datetime

        :param date: An integer representing date value (YYYYMMDD)
        :param time: An integer representing time value (HHMMSS)
        :param tzhour: The timezone offset in hours.
        :param tzmin: The timezone offset in minutes.
        :return: The datetime
        """
        if date == 0 and time == 0:
            return datetime.datetime.min

        if date != 0:
            year = int(date * 0.0001)
            mon  = int((date * 0.01) - (year * 100))
            day  = int(date - ((year * 10000) + (mon * 100)))
        else:
            year = datetime.date.year
            mon  = datetime.date.month
            day  = datetime.date.day

        if time != 0:
            hour = int(time * 0.0001)
            minu = int(((time * 0.01)) - (hour * 100))
            sec  = int(time - ((hour * 10000) + (minu * 100)))
        else:
            hour = 0
            minu = 0
            sec  = 0

        tzd = datetime.timedelta(hours=tzhour, minutes=tzmin)
        tz  = Util.TZ_CACHE.get(tzd)

        if tz is None:
            tz = TimeZone(tzhour, tzmin)
            Util.TZ_CACHE[tzd] = tz

        return datetime.datetime(year, mon, day, hour, minu, sec, 0, tz)


    @staticmethod
    def date_2_int(dval: "datetime.datetime|datetime.date") -> int:
        """
        Converts a datetime.date or datetime.datetime to an integer date.

        :param dval: Can also be a datetime.datetime.
        :return: An integer representation of the date
        """
        if dval is None:
            return 0

        if isinstance(dval, datetime.datetime):
            if dval == datetime.datetime.min:
                return 0
        elif isinstance(dval, datetime.date):
            if dval == datetime.date.min:
                return 0
        else:
            return 0

        return (dval.year * 10000) + (dval.month * 100) + dval.day


    @staticmethod
    def time_2_int(tval: "datetime.datetime|datetime.time") -> int:
        """
        Converts a datetime.date or datetime.time to an integer time.

        :param tval: Can also be a datetime.datetime.
        :return: An integer representation of the time.
        """
        if isinstance(tval, datetime.datetime):
            if tval == datetime.datetime.min:
                return 0
        elif isinstance(tval, datetime.time):
            if tval == datetime.time.min:
                return 0
        else:
            return 0

        return (tval.hour * 10000) + (tval.minute * 100) + tval.second


    @staticmethod
    def json_2_datetime(field: str, json_str: str, override_tz = None) -> datetime.datetime:
        """
        Converts incoming mettle format JSON string used in JSON to datetime.datetime.

        :param field: Incoming field name
        :param json_str: Incoming string to convert from mettle JSON datetime format.
        :param override_tz: (tzinfo) Servers overridden tzinfo if not not running in localtime.
        :return: The converted datetime
        """
        if str != type(json_str):
            raise Exception('Cannot de-serialize object, [%s] field is the incorrect type.'
                            ' Expected [%s/datetime.dateime] and got [%s].' % (field, str(str), str(type(json_str))))

        if len(json_str) != 24:
            raise Exception('Cannot de-serialize object from list, [%s] field is the wrong string length.'
                            ' Expected standard json date string and got [%s].' % (field, json_str))

        if json_str == '0001-01-01T00:00:00+0000':
            return datetime.datetime.min

        dt = datetime.datetime.strptime(json_str[0:24], '%Y-%m-%dT%H:%M:%S%z')

        if override_tz is None and Util.local_tz().utcoffset(None) != dt.tzinfo.utcoffset(dt):
            dt = dt - dt.tzinfo.utcoffset(dt)
            dt = dt + Util.local_tz().utcoffset(None)
        elif override_tz is not None and override_tz.utcoffset(dt) != dt.tzinfo.utcoffset(dt):
            dt = dt - dt.tzinfo.utcoffset(dt)
            dt = dt + override_tz.utcoffset(dt)

        dt = dt.replace(tzinfo=None)  # always assume we are working on the server local time.

        return dt


    @staticmethod
    def datetime_2_json(field: str, dt: datetime.datetime, override_tz = None) -> str:
        """
        Converts incoming datetime.datetime to mettle JSON string format.

        :param field: Incoming field name
        :param dt: Incoming datetime to convert to mettle JSON datetime format.
        :param override_tz: (tzinfo): Servers overridden tzinfo if not not running in localtime.

        :return: Json string version of the datetime
        """
        if dt == datetime.datetime.min:
            return '0001-01-01T00:00:00+0000'

        lz = Util.local_tz()
        if dt.tzinfo is None:
            if override_tz is None:
                dt = dt.replace(tzinfo=lz)
            else:
                dt = dt.replace(tzinfo=override_tz)

        if override_tz is None and lz.utcoffset(None) != dt.tzinfo.utcoffset(dt):
            dt = dt - dt.tzinfo.utcoffset(dt)
            dt = dt + lz.utcoffset(None)
            dt = dt.replace(tzinfo=lz)
        elif override_tz is not None and override_tz.utcoffset(dt) != dt.tzinfo.utcoffset(dt):
            dt = dt - dt.tzinfo.utcoffset(dt)
            dt = dt + override_tz.utcoffset(dt)
            dt = dt.replace(tzinfo=override_tz)

        return dt.strftime('%4Y-%m-%dT%H:%M:%S%z')


    @staticmethod
    def json_2_date(field: str, json_str: str) -> datetime.date:
        """
        Converts incoming mettle format JSON string used in JSON to datetime.date.

        :param field: Incoming field name
        :param json_str: Incoming string to convert from mettle JSON date format.
        :return: The converted date.
        """
        if str != type(json_str):
            raise Exception('Cannot de-serialize object, [%s] field is the incorrect type.'
                            ' Expected [%s/datetime.date] and got [%s].' % (field, str(str), str(type(json_str))))

        if len(json_str) != 10:
            raise Exception('Cannot de-serialize object, [%s] field is the wrong string length.'
                            ' Expected standard json date string and got [%s].' % (field, json_str))

        if json_str == '0001-01-01':
            return datetime.date.min

        return datetime.datetime.strptime(json_str[0:10], '%Y-%m-%d').date()


    @staticmethod
    def date_2_json(field: str, dt: datetime.date) -> str:
        """
        Converts incoming datetime.date to mettle JSON string format.

        :param field: Incoming field name
        :param dt: Incoming date to convert to mettle JSON date format.
        :return: Json string version of the date.
        """
        return dt.strftime('%4Y-%m-%d')


    @staticmethod
    def json_2_time(field: str, json_str: str) -> datetime.time:
        """
        Converts incoming mettle format JSON string used in JSON to datetime.time.

        :param field: (string) Incoming field name
        :param json_str: (string) Incoming string to convert from mettle JSON time format.
        :return: datetime.time
        """
        if str != type(json_str):
            raise Exception('Cannot de-serialize object from list, [%s] field is the incorrect type.'
                            ' Expected [%s/datetime.time] and got [%s].' % (field, str(str), str(type(json_str))))

        if len(json_str) != 8:
            raise Exception('Cannot de-serialize object from list, [%s] field is the wrong string length.'
                            ' Expected standard json date string and got [%s].' % (field, json_str))

        return datetime.datetime.strptime(json_str[0:8], '%H:%M:%S').time()


    @staticmethod
    def time_2_json(field: str, dt: datetime.time) -> str:
        """
        Converts incoming datetime.time to mettle JSON string format.

        :param field: Incoming field name
        :param dt: Incoming time to convert to mettle JSON time format.
        :return: Json string version of the time.
        """
        return dt.strftime('%H:%M:%S')


    def json_2_guid(field: str, json_str: str) -> uuid.UUID:
        """
        Converts incoming JSON string used in JSON to uuid.UUID.

        :param field: (string) Incoming field name
        :param json_str: (string) Incoming string to conver to uuid.UUID.
        :return: (uuid.UUID|None) None if empty, else the guid.
        """
        if str != type(json_str):
            raise Exception('Cannot de-serialize object, [%s] field is the incorrect type.'
                            ' Expected [%s/uuid] and got [%s].' % (field, str(str), str(type(json_str))))

        if len(json_str) == 0:
            return None

        if len(json_str) != 36:
            raise Exception('Cannot de-serialize object, [%s] field is the string length.'
                            ' Expected standard guid string and got [%s].' % (field, json_str))

        return uuid.UUID(json_str)


    def guid_2_json(field: str, guid: uuid.UUID) -> str:
        """
        Converts incoming JSON string used in JSON to uuid.UUID.

        :param field: (string) Incoming field name
        :param guid: (uuid.UUID|None) Incoming guid to conver to string.
        :return: The converted guid.
        """
        if guid is None:
            return ''

        return str(guid)
