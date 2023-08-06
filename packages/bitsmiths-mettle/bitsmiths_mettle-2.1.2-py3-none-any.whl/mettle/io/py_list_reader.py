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

from mettle.io.ireader import IReader
from mettle.io         import IStream

import datetime
import json
import uuid


class PyListReader(IReader):
    """
    Reading a mettle object from a python list.
    """

    def __init__(self, stream: IStream):
        """
        Constructor

        :param stream: The source ListStream to read from.
        """
        self._stream = stream


    def clear(self):
        self._stream.clear()


    def read_start(self, name: str):
        return None


    def read_start_list(self, name: str):
        return self.read_int64(name)


    def read_end(self, name: str):
        return None


    def read_bool(self, field: str) -> bool:
        return self._get_field(field, bool)


    def read_char(self, field: str) -> str:
        obj = self._get_field(field, str)

        if len(obj) != 1:
            raise Exception('Cannot de-serialize object from list.'
                            '[%s] char field has invalid length [%d].' % (field, len(obj)))

        return obj


    def read_int8(self, field: str) -> int:
        return self._get_field(field, int)


    def read_int16(self, field: str) -> int:
        return self._get_field(field, int)


    def read_int32(self, field: str) -> int:
        return self._get_field(field, int)


    def read_int64(self, field: str) -> int:
        return self._get_field(field, int)


    def read_uint8(self, field: str) -> int:
        return self._get_field(field, int)


    def read_uint16(self, field: str) -> int:
        return self._get_field(field, int)


    def read_uint32(self, field: str) -> int:
        return self._get_field(field, int)


    def read_uint64(self, field: str) -> int:
        return self._get_field(field, int)


    def read_double(self, field: str) -> float:
        return self._get_field(field, float)


    def read_float(self, field: str) -> float:
        return self._get_field(field, float)


    def read_string(self, field: str) -> str:
        return self._get_field(field, str)


    def read_bytearray(self, field: str) -> bytes:
        return self._get_field(field, bytes)


    def read_datetime(self, field: str) -> datetime.datetime:
        return self._get_field(field, datetime.datetime)


    def read_date(self, field: str) -> datetime.date:
        return self._get_field(field, datetime.date)


    def read_time(self, field: str) -> datetime.time:
        return self._get_field(field, datetime.time)


    def read_json(self, field: str) -> 'dict|list':
        res = self._get_field(field, str)

        if not res:
            return None

        return json.loads(res)


    def read_guid(self, field: str) -> uuid.UUID:
        return self._get_field(field, uuid.UUID)


    def _get_field(self, field: str, ftype: type):
        obj = self._stream.read(1)

        if obj is None:
            if ftype == float:
                raise Exception('Cannot de-serialize object from dictionary, [%s] field is None.' % (field))

            return None

        if ftype != type(obj):
            raise Exception('Cannot de-serialize object from list, [%s] field is the incorrect type.'
                            ' Expected [%s] and got [%s].' % (field, str(ftype), str(type(obj))))

        return obj
