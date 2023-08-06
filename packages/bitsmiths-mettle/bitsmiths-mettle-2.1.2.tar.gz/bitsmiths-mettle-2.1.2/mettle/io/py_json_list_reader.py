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

"""
PyJsonListReader
"""

import base64
import datetime
import uuid

from .istream        import IStream
from .py_list_reader import PyListReader
from .util           import Util


class PyJsonListReader(PyListReader):
    """
    Reading a mettle object from a python list that has the dates as Json strings or datetimes.
    """

    def __init__(self, stream: IStream, tzinfo: datetime.tzinfo = None):
        """
        Constructor

        :param stream: The source ListStream to read from.
        :param tzinfo: Optionally give the target timezone to convert to for datetimes.
            """
        PyListReader.__init__(self, stream)

        self._tzinfo = tzinfo


    def _get_field(self, field: str, ftype: type):
        obj = self._stream.read(1)

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
                                'Expected [%s/float] and got [%s] which could not be converted.' % (
                                    field, str(ftype), str(type(obj))))

        if ftype == int and isinstance(obj, str):
            try:
                return int(obj)
            except ValueError:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is the incorrect type.'
                                'Expected [%s/int] and got [%s] which could not be converted.' % (
                                    field, str(ftype), str(type(obj))))

        if ftype == float and isinstance(obj, int):
            try:
                return float(obj)
            except ValueError:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is the incorrect type.'
                                'Expected [%s/float] and got [%s] which could not be converted.' % (
                                    field, str(ftype), str(type(obj))))

        if ftype == int and isinstance(obj, float):
            try:
                val = int(obj)
                return val
            except ValueError:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is the incorrect type.'
                                'Expected [%s/float] and got [%s] which could not be converted.' % (
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
            if not isinstance(obj, str):
                raise Exception('Cannot de-serialize object from list, [%s] field is the incorrect type.'
                                'Expected [%s/bytes] and got [%s].' % (
                                    field, str(str), str(type(obj))))

            return base64.b64decode(obj)

        raise Exception('Cannot de-serialize object from list, [%s] field is the incorrect type.'
                        'Expected [%s/bytes] and got [%s].' % (
                            field, str(ftype), str(type(obj))))
