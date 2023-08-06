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
import uuid


class IReader:
    """
    This is the mettle.io Reader interface for deserialising objects.
    """

    def get_last_io_size(self) -> int:
        """
        Returns the last size read.

        :return: The size read by the reader.
        """
        return 0


    def clear(self):
        """
        Clears the reader internal objects for reuse.
        """
        pass


    def read_start(self, name: str) -> int:
        """
        The first method that gets called when deserialising an object.

        :param name: The name of the object, this may be left as None.
        :return: The size read by the reader.
        """
        pass


    def read_start_list(self, name: str) -> int:
        """
        The first method that gets called when deserialising an object.

        :param name: The name of the object, this may be left as None.
        :return: The length/size of the list.
        """
        pass


    def read_end(self, name: str) -> int:
        """
        The last method that gets called when deserialising an object.

        :param name: The name of the object, this may be left as None, must must match what was passed into 'readStart'.
        :return: The size read by the reader.
        """
        pass


    def read_bool(self, field: str) -> bool:
        """
        Reads a boolean.

        :param field: The name of the field.
        :return: The bool that was read.
        """
        pass


    def read_char(self, field: str) -> str:
        """
        Reads a character.

        :param field: The name of the field.
        :return: The char that was read, the strnig length will always be 1.
        """
        pass


    def read_int8(self, field: str) -> int:
        """
        Reads a 1 byte integer.

        :param field: The name of the field.
        :return: The byte that was read.
        """
        pass


    def read_int16(self, field: str) -> int:
        """
        Reads a 2 byte integer.

        :param field: The name of the field.
        :return: The int16 that was read.
        """
        pass


    def read_int32(self, field: str) -> int:
        """
        Reads a 4 byte integer.

        :param field: The name of the field.
        :return: The int32 that was read.
        """
        pass


    def read_int64(self, field: str) -> int:
        """
        Reads a 8 byte Integer

        :param field: The name of the field.
        :return: The int64 that was read.
        """


    def read_uint8(self, field: str) -> int:
        """
        Reads an unsigned 1 byte integer.

        :param field: The name of the field.
        :return: The byte that was read.
        """
        pass


    def read_uint16(self, field: str) -> int:
        """
        Reads an unsigned 2 byte integer.

        :param field: The name of the field.
        :return: The int16 that was read.
        """
        pass


    def read_uint32(self, field: str) -> int:
        """
        Reads an unsigned 4 byte integer.

        :param field: The name of the field.
        :return: The int32 that was read.
        """
        pass


    def read_uint64(self, field: str) -> int:
        """
        Reads an unsigned 8 byte Integer

        :param field: The name of the field.
        :return: The int64 that was read.
        """
        pass


    def read_double(self, field: str) -> float:
        """
        Reads a 8 byte float.

        :param field: The name of the field.
        :return: The double that was read.
        """
        pass


    def read_float(self, field: str) -> float:
        """
        Reads a 4 byte float.

        :param field: The name of the field.
        :return: The float that was read.
        """
        pass


    def read_string(self, field: str) -> str:
        """
        Reads a string.

        :param field: The name of the field.
        :return: (string) The string that was read.
        """
        pass


    def read_bytearray(self, field: str) -> bytearray:
        """
        Reads a byte array.

        :param field: The name of the field.
        :return: The byte array that was read.
        """
        pass


    def read_datetime(self, field: str) -> datetime.datetime:
        """
        Reads a datetime.

        :param field: The name of the field.
        :return: The datetime that was read.
        """
        pass


    def read_date(self, field: str) -> datetime.date:
        """
        Reads a date.

        :param field: The name of the field.
        :return: The date that was read.
        """
        pass


    def read_time(self, field: str) -> datetime.time:
        """
        Reads a time.

        :param field: The name of the field.
        :return: The time that was read.
        """
        pass


    def read_json(self, field: str) -> dict:
        """
        Reads a json dictionary.

        :param field: The name of the field.
        :return: The read json.
        """
        pass


    def read_guid(self, field: str) -> uuid.UUID:
        """
        Reads a uuid.

        :param field: The name of the field.
        :return: The guid that was read.
        """
        pass
