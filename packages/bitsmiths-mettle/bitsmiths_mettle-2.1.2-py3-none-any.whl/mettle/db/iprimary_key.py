
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


class IPrimaryKey:
    """
    Interface for a table object that has a primary key.
    """

    def _write_pk(self, _key):
        """
        Writes the primary key to the object.

        :param _key: A key object that will have the pk written to it.
        """
        pass


    def _read_pk(self, _key):
        """
        Reads the primary key from the object.

        :param _key: A key object from which the pk will be read from.
        """
        pass


    def _serialize_pk(self, _w):
        """
        Serialize the key to a writer object.

        :param _w: (mettle.io.IWriter) The writer that will seriliaze the key.
        """
        pass


    def _deserialize_pk(self, _r):
        """
        Deserialize the key from the read object.

        :param _r: (mettle.io.IReader) The read that will deseriliaze the key.
        """
        pass


    def _name(self) -> str:
        """
        Gets the name of this table.

        :return: The name of the table this object represents.
        """
        pass
