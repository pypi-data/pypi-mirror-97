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
import json
import struct
import uuid

from istream  import IStream
from .ireader import IReader
from .util    import Util

from mettle.lib.xmettle import xMettle


class BigEndianReader(IReader):
    """!
    The standard big endian reader implementation.
    """

    def __init__(self, stream: IStream, tzinfo: datetime.tzinfo = None):
        """
        Constructor

        :param stream: The stream object to read from.
        :param tzinfo: Optionally give the target timezone to convert to for datetimes.
        """
        self._stream     = stream
        self._tzinfo     = tzinfo


    def clear(self):
        self._stream.clear()


    def read_start(self, name: str):
        pass


    def read_start_list(self, name: str):
        return self.read_int32("listSize")


    def read_end(self, name: str):
        pass


    def read_bool(self, field: str):
        ba = self._stream.read(struct.calcsize(">b"))

        return struct.unpack(">b", ba)[0]


    def read_char(self, field: str):
        ba = self._stream.read(struct.calcsize(">c"))
        ca = struct.unpack(">c", ba)[0]

        return ca.decode('ascii')


    def read_int8(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">b"))

        return struct.unpack(">b", ba)[0]


    def read_int16(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">h"))

        return struct.unpack(">h", ba)[0]


    def read_int32(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">i"))

        return struct.unpack(">i", ba)[0]


    def read_int64(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">l"))

        return struct.unpack(">l", ba)[0]


    def read_uint8(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">B"))

        return struct.unpack(">B", ba)[0]


    def read_uint16(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">H"))

        return struct.unpack(">H", ba)[0]


    def read_uint32(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">I"))

        return struct.unpack(">I", ba)[0]


    def read_uint64(self, field: str):
        if self._read_null(field):
            return None

        ba = self._stream.read(struct.calcsize(">L"))

        return struct.unpack(">L", ba)[0]


    def read_double(self, field: str):
        ba = self._stream.read(struct.calcsize(">d"))

        return struct.unpack(">d", ba)[0]


    def read_float(self, field: str):
        ba = self._stream.read(struct.calcsize(">f"))

        return struct.unpack(">f", ba)[0]


    def read_string(self, field: str):
        strLen = self.read_int32(field)
        ba     = self._stream.read(strLen)

        return ba.decode('utf8')


    def read_bytearray(self, field: str):
        ba_len = self.read_int32(field)

        if not ba_len:
            return None

        return self._stream.read(ba_len)


    def read_datetime(self, field: str):
        if self._read_null(field):
            return None

        dval = self.read_int32(field)
        tval = self.read_int32(field)
        hval = self.read_int8(field)
        mval = self.read_int8(field)

        dt = Util.ints_2_datetime(dval, tval, hval, mval)

        if dt == datetime.datetime.min:
            return dt

        if self._tzinfo is None and Util.local_tz().utcoffset(None) != dt.tzinfo.utcoffset(dt):
            dt = dt - dt.tzinfo.utcoffset(dt)
            dt = dt + Util.local_tz().utcoffset(None)
        elif self._tzinfo is not None and self._tzinfo.utcoffset(dt) != dt.tzinfo.utcoffset(dt):
            dt = dt - dt.tzinfo.utcoffset(dt)
            dt = dt + self._tzinfo.utcoffset(dt)

        dt = dt.replace(tzinfo=None)  # always assume we are working on the server local time.

        return dt


    def read_date(self, field: str):
        if self._read_null(field):
            return None

        dval = self.read_int32(field)

        return Util.int_2_date(dval)


    def read_time(self, field: str):
        if self._read_null(field):
            return None

        tval = self.read_int32(field)

        return Util.int_2_time(tval)


    def read_json(self, field: str):
        jz = self.read_int32(field)

        if jz == 0:
            return None

        ba = self._stream.read(jz)

        return json.loads(ba.decode('utf8'))


    def read_guid(self, field: str):
        gz = self.read_int8(field)

        if gz == 0:
            return None

        if gz != 36:
            raise xMettle("Guid length should be [36], but read size of [%d] for field [%s]" % (gz, field))

        ba = self._stream.read(36)

        return uuid.UUID(ba.decode('utf8'))


    def _read_null(self, field: str) -> bool:
        ba = self._stream.read(struct.calcsize(">b"))

        isnull = struct.unpack(">b", ba)[0]

        if isnull == 0:
            return True

        if isnull != 1:
            raise xMettle("Expected null check and got something else, field [%s]" % field)

        return False
