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


class IStream:
    """
    The mettle.io.stream interface.
    """

    def clear(self):
        """
        Clears the stream for re-use, but does not necissarily free any resources.
        """
        pass


    def purge(self):
        """
        Releases all resources that the stream holds.
        """
        pass


    def read(self, size: int) -> int:
        """
        Reads bytes from the stream and returns the bytes.

        :param size: The number of bytes/objects to read from the stream.
        :return: The bytes/object count read from the stream.
        """
        pass


    def write(self, obj: object):
        """
        Writes obj to the stream.

        :param obj: The bytes/object to be written to the stream.
        """


    def size(self) -> int:
        """
        Returns the size of the stream.

        :returns: Size of the stream.
        """

        pass

    def position_start(self):
        """
        Moves the internal stream position to the start of the stream.
        """
        pass


    def position_end(self):
        """
        Moves the internal stream position to the end of the stream.
        """
        pass


    def position_move(self, offset: int):
        """
        Moves the internal stream position forward in bytes.

        :param offset: The number of bytes to move forward from the current position.
        """
        pass


    def position(self) -> int:
        """
        Gets the current position of the stream.

        :returns: The current position of the stream.
        """
        pass
