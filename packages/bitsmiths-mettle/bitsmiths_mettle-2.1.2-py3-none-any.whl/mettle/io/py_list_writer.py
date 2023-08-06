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

from mettle.io.iwriter import IWriter

import datetime
import json
import uuid


class PyListWriter(IWriter):
    """
    Write a mettle object into a python list.
    """

    def __init__(self, stream):
        """
        Constructor

        :param stream: (mettle.io.IStream) The target ListStream to write to.
        """
        self._stream = stream


    def clear(self):
        self._stream.clear()


    def write_start(self, name: str):
        return None

    def write_start_list(self, name: str, list_size: int):
        self.write_int64(name, list_size)
        return None

    def write_end(self, name: str):
        return None

    def write_bool(self, field: str, v):
        self._write_field(field, v, bool)

    def write_char(self, field: str, v):
        if len(v) != 1:
            raise Exception('Cannot serialize object to list, [%s] char field has invalid length [%d].' % (field, len(v)))

        self._write_field(field, v, str)

    def write_int8(self, field: str, v):
        self._write_field(field, v, int)

    def write_int16(self, field: str, v):
        self._write_field(field, v, int)

    def write_int32(self, field: str, v):
        self._write_field(field, v, int)

    def write_int64(self, field: str, v):
        self._write_field(field, v, int)

    def write_uint8(self, field: str, v):
        self._write_field(field, v, int)

    def write_uint16(self, field: str, v):
        self._write_field(field, v, int)

    def write_uint32(self, field: str, v):
        self._write_field(field, v, int)

    def write_uint64(self, field: str, v):
        self._write_field(field, v, int)

    def write_double(self, field: str, v):
        self._write_field(field, v, float)

    def write_float(self, field: str, v):
        self._write_field(field, v, float)

    def write_string(self, field: str, v):
        self._write_field(field, v, str)

    def write_bytearray(self, field: str, v):
        self._write_field(field, v, bytes)

    def write_datetime(self, field: str, v):
        self._write_field(field, v, datetime.datetime)

    def write_date(self, field: str, v):
        self._write_field(field, v, datetime.date)

    def write_time(self, field: str, v):
        self._write_field(field, v, datetime.time)

    def write_json(self, field: str, v):
        if not v:
            self._write_field(field, '')
            return

        self._write_field(field, json.dumps(v), uuid.UUID)

    def write_guid(self, field: str, v):
        self._write_field(field, v or None, uuid.UUID)

    def _write_field(self, field: str, v, ftype: type):
        if v is None:
            if ftype == float:
                raise Exception('Cannot serialize object to list, [%s] field is None.' % (field))

        elif ftype != type(v):
            if ftype == bytes and not isinstance(v, bytearray):
                raise Exception('Cannot serialize object to list, [%s] field is the incorrect type,'
                                ' expected [%s] and got [%s].' % (field, str(ftype), str(type(v))))

        self._stream.write(v)
