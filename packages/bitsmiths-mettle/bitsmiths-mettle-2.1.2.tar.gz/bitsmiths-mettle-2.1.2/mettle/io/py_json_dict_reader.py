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

import base64
import datetime
import uuid

from mettle.io.py_dict_reader import PyDictReader
from mettle.io.util           import Util


class PyJsonDictReader(PyDictReader):
    """
    Reading a mettle object from a python dictionary.  This reader is forgiving
    in that it accepts floats as integers, visa versa, reads strings as dates and so on.
    """

    def __init__(self, py_dict: dict, tzinfo=None):
        """
        Constructor

        :param py_dict: The source dictionary to read from.
        :param tzinfo: (datetime.tzinfo) Optionally give the target timezone to convert to for datetimes.
        """
        PyDictReader.__init__(self, py_dict)

        self._tzinfo = tzinfo


    def _get_field(self, field: str, ftype: type):
        if self._dict is not None:
            obj = self._dict.get(field)
        else:
            idx = self._stLen[-1]

            if idx >= len(self._list):
                raise Exception('Attempted to read beyond then end of a list!')

            self._stLen[-1] += 1
            obj              = self._list[idx]

        if obj is None:
            if ftype == float:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is None.' % (field))

            return None

        if ftype == type(obj):
            return obj

        if ftype == float and isinstance(obj, str):
            try:
                return float(obj)
            except ValueError:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is the incorrect type.'
                                'expected [%s/float] and got [%s] which could not be converted.' % (
                                    field, str(ftype), str(type(obj))))

        if ftype == int and isinstance(obj, str):
            try:
                return int(obj)
            except ValueError:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is the incorrect type.'
                                'expected [%s/int] and got [%s] which could not be converted.' % (
                                    field, str(ftype), str(type(obj))))

        if ftype == float and isinstance(obj, int):
            try:
                return float(obj)
            except ValueError:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is the incorrect type.'
                                'expected [%s/float] and got [%s] which could not be converted.' % (
                                    field, str(ftype), str(type(obj))))

        if ftype == int and isinstance(obj, float):
            try:
                return int(obj)
            except ValueError:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is the incorrect type.'
                                'expected [%s/int] and got [%s] which could not be converted.' % (
                                    field, str(ftype), str(type(obj))))

        if ftype == datetime.datetime:
            return Util.json_2_datetime(field, obj, self._tzinfo)

        if ftype == datetime.date:
            return Util.json_2_date(field, obj)

        if ftype == datetime.time:
            return Util.json_2_time(field, obj)

        if ftype == uuid.UUID:
            return Util.json_2_guid(field, obj)

        if ftype == bytes:
            if str != type(obj):
                raise Exception('Cannot de-serialize object from list, [%s] field is the incorrect type.'
                                'Expected [%s/bytes] and got [%s].' % (field, str(str), str(type(obj))))

            return base64.b64decode(obj)

        raise Exception('Cannot de-serialize object from list, [%s] field is the incorrect type.'
                        ' Expected [%s/bytes] and got [%s].' % (field, str(ftype), str(type(obj))))
