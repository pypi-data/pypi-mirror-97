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


from mettle.io.istream  import IStream
from mettle.lib.xmettle import xMettle


class ListStream(IStream):
    """
    The standard list steam object.
    """

    def __init__(self):
        self._lst  = []
        self._pos  = 0


    def clear(self):
        self._lst.clear()
        self._pos = 0


    def purge(self):
        self.clear()


    def get_list(self) -> list:
        """
        Returns the actual lit object.
        """
        return self._lst


    def eat(self, lst: list):
        """
        Consumes a list.
        """
        del self._lst

        self._lst = lst
        self._pos = 0


    def read(self, size: int) -> object:
        if self._pos + size > len(self._lst):
            raise xMettle("Cannot read beyond the bounds of the liststream [position:%d, requested:%d, size:%d]." % (
                self._pos, size, len(self._lst)), src=ListStream.__name__)

        if size < 1:
            return None

        if size == 1:
            res = self._lst[self._pos]
            self._pos += 1
        else:
            res = self._lst[self._pos:self._pos + size]
            self._pos += size

        return res


    def write(self, obj):
        if self._pos == len(self._lst):
            self._lst.append(obj)
        else:
            self._lst.insert(self._pos, obj)

        self._pos += 1


    def size(self):
        return len(self._lst)


    def position_start(self):
        self._pos = 0


    def position_end(self):
        self._pos = len(self._lst)


    def position_move(self, offset: int):
        if offset + self._pos > len(self._lst):
            raise xMettle("Cannot move beyond the bounds of the liststream [position:%d, offset:%d, size:%d]." % (
                self._pos, offset, len(self._lst)), src=ListStream.__name__)


    def position(self) -> int:
        return self._pos
