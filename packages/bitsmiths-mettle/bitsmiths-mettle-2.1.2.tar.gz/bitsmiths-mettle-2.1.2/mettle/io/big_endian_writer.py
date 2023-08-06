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
BigEndianWriter
"""

import datetime
import json
import struct

from .istream   import IStream
from .iwriter   import IWriter
from .util      import Util

from mettle.lib.timezone import TimeZone


class BigEndianWriter(IWriter):
    """
    The standard big endian writer implementation.
    """

    def __init__(self, stream: IStream, tzinfo: datetime.tzinfo = None):
        """
        Constructor

        :param stream: The stream object to write too.
        :param tzinfo: Optionally give the target timezone to convert to for datetimes.
        """
        self._stream  = stream
        self._tzinfo  = tzinfo


    def clear(self):
        self._stream.clear()


    def write_start(self, name: str):
        pass


    def write_start_list(self, name: str, list_size: int):
        self.write_int32("ListSize", list_size)
        return None


    def write_end(self, name: str):
        pass


    def write_bool(self, field: str, v):
        if v:
            ba = struct.pack(">b", 1)
        else:
            ba = struct.pack(">b", 0)

        self._stream.write(ba)


    def write_char(self, field: str, v):
        ba = struct.pack(">c", bytes(v[0], 'ascii'))
        self._stream.write(ba)


    def write_int8(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">b", v)
        self._stream.write(ba)


    def write_int16(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">h", v)
        self._stream.write(ba)


    def write_int32(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">i", v)
        self._stream.write(ba)


    def write_int64(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">l", v)
        self._stream.write(ba)


    def write_uint8(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">B", v)
        self._stream.write(ba)


    def write_uint16(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">H", v)
        self._stream.write(ba)


    def write_uint32(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">I", v)
        self._stream.write(ba)


    def write_uint64(self, field: str, v):
        if self._write_null(v):
            return

        ba = struct.pack(">L", v)
        self._stream.write(ba)


    def write_double(self, field: str, v):
        ba = struct.pack(">d", v)
        self._stream.write(ba)


    def write_float(self, field: str, v):
        ba = struct.pack(">f", v)
        self._stream.write(ba)


    def write_string(self, field: str, v):
        if v is None:
            self.write_int32(field, 0)

        ba = bytes(v, 'utf8')
        self.write_int32(field, len(ba))
        self._stream.write(ba)


    def write_bytearray(self, field: str, v):
        if v is None:
            self.write_int32(field, 0)
            return

        self.write_int32(field, len(v))
        self._stream.write(v)


    def write_datetime(self, field: str, v):
        if self._write_null(v):
            return

        lz = Util.local_tz()
        if v.tzinfo is None:
            if self._tzinfo is None:
                v = v.replace(tzinfo=lz)
            else:
                v = v.replace(tzinfo=self._tzinfo)

        if self._tzinfo is None and lz.utcoffset(None) != v.tzinfo.utcoffset(v):
            v = v - v.tzinfo.utcoffset(v)
            v = v + lz.utcoffset(None)
            v = v.replace(tzinfo=lz)
        elif self._tzinfo is not None and self._tzinfo.utcoffset(v) != v.tzinfo.utcoffset(v):
            v = v - v.tzinfo.utcoffset(v)
            v = v + self._tzinfo.utcoffset(v)
            v = v.replace(tzinfo=self._tzinfo)

        self.write_int32(field, Util.date_2_int(v))
        self.write_int32(field, Util.time_2_int(v))

        if isinstance(v.tzinfo, TimeZone):
            self.write_int8(field, v.tzinfo.tzhour)
            self.write_int8(field, v.tzinfo.tzmin)
        else:
            hr, mn = divmod(v.utcoffset(), 3600)
            self.write_int8(field, hr)
            self.write_int8(field, mn)


    def write_date(self, field: str, v):
        if self._write_null(v):
            return

        self.write_int32(field, Util.date_2_int(v))


    def write_time(self, field: str, v):
        if self._write_null(v):
            return

        self.write_int32(field, Util.time_2_int(v))


    def write_json(self, field: str, v):
        if not v:
            self.write_int32(field, 0)
            return

        ba = bytes(json.dumps(v), 'utf8')
        self.write_int32(field, 36)
        self._stream.write(ba)


    def write_guid(self, field: str, v):
        if v is None:
            self.write_int8(field, 0)
            return

        ba = bytes(str(v), 'utf8')
        self.write_int8(field, len(ba))
        self._stream.write(ba)


    def _write_null(self, v) -> bool:
        if v is None:
            self._stream.write(struct.pack(">b", 0))
            return True

        self._stream.write(struct.pack(">b", 1))
        return False
