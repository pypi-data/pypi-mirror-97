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


class IWriter:
    """
    This is the mettle.io Writer interface for serialising objects.
    """

    def clear(self):
        """
        Clears the writer internal objects for reuse.
        """
        pass


    def write_start(self, name: str):
        """
        The first method that gets called when serialising an object.

        :param name: The name of the object, this may be left as None.
        :return: (object) If applicable the object that newly created object that is being written to else returns None.
        """
        pass


    def write_start_list(self, name: str, list_size: int):
        """
        The first method that gets called when serialising an object if the object is an array/list type.

        :param name: The name of the object, this may be left as None.
        :param list: The length/size of the list.
        """
        pass


    def write_end(self, name: str):
        """
        The last method that gets called when serialising an object.

        :param string: The name of the object, this may be left as None, must must match what was
                       passed into 'writeStart'.
        :return: (object) The object that is completed being written too, or None if that is not applicable
                 for this writer type.
        """
        pass


    def write_bool(self, field: str, v):
        """
        Writes a boolean.

        :param field: The name of the field.
        :param v: (bool) The boolean to be written.
        """
        pass


    def write_char(self, field: str, v):
        """
        Writes a char.

        :param field: The name of the field.
        :param v: (string) The string to be written, should always have a length of 1.
        """
        pass


    def write_int8(self, field: str, v):
        """
        Writes a 1 byte integer.

        :param field: The name of the field.
        :param v: (int) The byte to be written.
        """
        pass


    def write_int16(self, field: str, v):
        """
        Writes a 2 byte integer.

        :param field: The name of the field.
        :param v: (int) The int16 to be written.
        """
        pass


    def write_int32(self, field: str, v):
        """
        Writes a 4 byte integer.

        :param field: The name of the field.
        :param v: (int) The int32 to be written.
        """
        pass


    def write_int64(self, field: str, v):
        """
        Writes a 8 byte integer.

        :param field: The name of the field.
        :param v: (int) The int64 to be written.
        """
        pass


    def write_uint8(self, field: str, v):
        """
        Writes an unsigned 1 byte integer.

        :param field: The name of the field.
        :param v: (int) The unsigned byte to be written.
        """
        pass


    def write_uint16(self, field: str, v):
        """
        Writes an unsigned 2 byte integer.

        :param field: The name of the field.
        :param v: (int) The unsigned int16 to be written.
        """
        pass


    def write_uint32(self, field: str, v):
        """
        Writes an unsigned 4 byte integer.

        :param field: The name of the field.
        :param v: (int) The unsigned int32 to be written.
        """
        pass


    def write_uint64(self, field: str, v):
        """
        Writes an unsigned 8 byte integer.

        :param field: The name of the field.
        :param v: (int) The unsigned int64 to be written.
        """

        pass


    def write_double(self, field: str, v):
        """
        Writes a 8 byte float.

        :param field: The name of the field.
        :param v: (int) The double to be written.
        """
        pass


    def write_float(self, field: str, v):
        """
        Writes a 4 byte float.

        :param field: The name of the field.
        :param v: (int) The float to be written.
        """
        pass


    def write_string(self, field: str, v):
        """
        Writes a string.

        :param field: The name of the field.
        :param v: (string) The string to be written.
        """
        pass


    def write_bytearray(self, field: str, v):
        """
        Writes a byte array.

        :param field: The name of the field.
        :param v: (bytearray) The byte array to be written.
        """
        pass


    def write_datetime(self, field: str, v):
        """
        Writes a datetime.

        :param field: The name of the field.
        :param v: (datetime.datetime) The datetime to be written.
        """
        pass


    def write_date(self, field: str, v):
        """
        Writes a date.

        :param field: The name of the field.
        :param v: (datetime.date) The date to be written.
        """
        pass


    def write_time(self, field: str, v):
        """
        Writes a time.

        :param field: The name of the field.
        :param v: (datetime.time) The time to be written.
        """
        pass


    def write_json(self, field: str, v):
        """
        Writes a json string.

        :param field: The name of the field.
        :param v: (dict) The json dict to be written.
        """
        pass


    def write_guid(self, field: str, v):
        """
        Writes a uuid.

        :param field: The name of the field.
        :param v: (uuid) The guid to be written.
        """
        pass
