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
MemoryStream
"""

from mettle.io.istream  import IStream
from mettle.lib.xmettle import xMettle


class MemoryStream(IStream):
    """
    The standard memory/bytearray steam object.
    """

    def __init__(self):
        self._ba   = bytearray()
        self._pos  = 0


    def clear(self):
        self._ba.clear()
        self._pos = 0


    def purge(self):
        self.clear()


    def bytes(self) -> bytearray:
        """
        Returns the internal byte array object.
        """
        return self._ba


    def eat(self, ba: bytearray):
        """
        Consumes a byte array.
        """
        self._ba  = ba
        self._pos = 0


    def read(self, size: int) -> object:
        if self._pos + size > len(self._ba):
            raise xMettle("Cannot read beyond the bounds of the memorystream [position:%d, requested:%d, size:%d]." % (
                self._pos, size, len(self._ba)), src=MemoryStream.__name__)

        res = self._ba[self._pos:self._pos + size]

        self._pos += size

        return res


    def write(self, obj: object):
        if self._pos == len(self._ba):
            self._ba += obj
        elif len(self._ba) >= self._pos + len(obj):
            self._ba[self._pos:self._pos + len(obj)] = obj[0:]
        else:
            self._ba[self._pos:] = obj[0:]

        self._pos += len(obj)


    def size(self) -> int:
        return len(self._ba)


    def position_start(self):
        self._pos = 0


    def position_end(self):
        self._pos = len(self._ba)


    def position_move(self, offset: int):
        if offset + self._pos > len(self._ba):
            raise xMettle("Cannot move beyond the bounds of the memorystream [position:%d, offset:%d, size:%d]." % (
                self._pos, offset, len(self._ba)), src=MemoryStream.__name__)


    def position(self) -> int:
        return self._pos
