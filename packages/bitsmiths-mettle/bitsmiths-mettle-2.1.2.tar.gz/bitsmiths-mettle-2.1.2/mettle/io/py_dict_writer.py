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
PyDictWriter
"""

import datetime
import uuid

from mettle.io.iwriter import IWriter


class PyDictWriter(IWriter):
    """
    Write a mettle object into a python dictionary.
    """

    def __init__(self, py_dict: dict):
        """
        Constructor

        :param py_dict: The target dictionary to write to.
        """
        self._stack = [py_dict]
        self._stlen = [0]
        self._dict  = self._stack[0]
        self._list  = None

    def clear(self):
        tmp = self._stack[0]
        tmp.clear()
        self._stack.clear()
        self._stlen.clear()
        self._stack.append(tmp)
        self._stlen.append(0)
        self._dict = self._stack[0]
        self._list = None

    def write_start(self, name: str):
        tmp = {}

        if self._dict is not None:
            self._dict[name] = tmp
            self._stack.append(tmp)
            self._stlen.append(0)
            self._dict = tmp
        else:
            idx = self._stlen[-1]
            self._stlen[-1] += 1
            self._list[idx] = tmp
            self._stack.append(tmp)
            self._stlen.append(-1)
            self._dict = tmp
            self._list = None

        return None


    def write_start_list(self, name: str, list_size: int):
        tmp = [None] * list_size

        if self._dict is not None:
            self._dict[name] = tmp
            self._stack.append(tmp)
            self._stlen.append(0)
            self._list = tmp
            self._dict = None
        else:
            idx = self._stlen[-1]
            self._stlen[-1] += 1
            self._list[idx] = tmp
            self._stack.append(tmp)
            self._stlen.append(0)
            self._list = tmp

        return None

    def write_end(self, name: str):
        self._stack.pop()
        self._stlen.pop()

        tobj = self._stack[-1]

        if isinstance(tobj, dict):
            self._list = None
            self._dict = tobj
        else:
            self._list = tobj
            self._dict = None

        return None


    def write_bool(self, field: str, v):
        self._write_field(field, v, bool)

    def write_char(self, field: str, v):
        if len(v) != 1:
            raise Exception('Cannot serialize object to dictionary, [%s] char field has invalid length [%d].' % (field, len(v)))

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

    def write_guid(self, field: str, v):
        self._write_field(field, v, uuid.UUID)

    def _write_field(self, field: str, v, ftype: type):
        if v is None:
            if ftype != uuid.UUID:
                raise Exception('Cannot serialize object to dictionary, [%s] field is None.' % (field))

        if ftype == v:
            raise Exception('Cannot serialize object to dictionary, [%s] field is the incorrect type.'
                            ' Expected [%s] and got [%s].' % (field, str(ftype), str(type(v))))

        if self._dict is not None:
            self._dict[field] = v
        else:
            idx = self._stlen[-1]

            if idx >= len(self._list):
                raise Exception('Attempted to write beyond then end of a list!')

            self._stlen[-1] += 1
            self._list[idx]  = v
