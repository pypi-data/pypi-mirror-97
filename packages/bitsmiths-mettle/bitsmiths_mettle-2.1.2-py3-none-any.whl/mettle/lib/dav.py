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

from enum import IntEnum

from mettle.lib.xmettle import xMettle


class Dav:
    """
    A DAV is a Data Assurance Validator.  A piece of logic or check to assure
    that a value or object is valid before proceeding.
    """

    class eDavType(IntEnum):
        """
        The list of Dav types.
        """
        NotNull    = 1  # Value cannot be null.
        Min        = 2  # Value cannot me less than min, for strings/lists this min length or list size.
        Max        = 3  # Value cannot me less than max, for strings/lists this max length or list size.
        In         = 4  # Value is inside this list.
        NotIn      = 5  # Value is inside this list.
        Regex      = 6  # Use a regex expression to pass on the str() value of object.
        Func       = 7  # Make function call lookup on the object.


    def __init__(self, dav_type: 'eDavType', val: object = None):
        """
        Constructor.

        :param dav_type: The dav type.
        :param val: (object) The object to validate.
        """
        self._dav_type = dav_type

        if dav_type in (self.eDavType.Regex, self.eDavType.Func):
            if not isinstance(val, str):
                raise Exception('Dav cannot be initialized, val is not a string! [dav_type:%s, val:%s]' % (
                    dav_type, str(type(val))))

        self._val = val


    def get_type(self) -> 'eDavType':
        """
        Get the dav type.

        :return: The eDavType
        """
        return self._dav_type


    def validate(self, src: str, obj, throw_ex: bool = True, regex_lookup: dict = None, func_lookup: dict = None) -> bool:
        """
        Do the DAV validation against the object and return False or raise and exception if the
        validation fails.

        :param  src: The name of the objecting being validated, purely for info purposes.
        :param  obj: (object) The object value to check.
        :param  throw_ex: Raise an exception if the object does not pass the validation.
        :param  regex_lookup: If regex validation, use the regex_lookup.
        :param  func_lookup: If func validation, use the func_lookup.
        :return: True/False if object passes the DAV validation.
        """
        if obj is None:
            return self._failed(throw_ex, 'Value [%s] cannot be empty.' % src)

        objt = type(obj)

        if self._dav_type == self.eDavType.NotNull:
            return self._val_not_null(src, obj, objt, throw_ex)

        if self._dav_type == self.eDavType.Min:
            return self._val_min(src, obj, objt, throw_ex)

        if self._dav_type == self.eDavType.Max:
            return self._val_max(src, obj, objt, throw_ex)

        if self._dav_type == self.eDavType.In:
            return self._val_in(src, obj, objt, throw_ex)

        if self._dav_type == self.eDavType.NotIn:
            return self._val_not_in(src, obj, objt, throw_ex)

        if self._dav_type == self.eDavType.Regex:
            return self._val_regex(src, obj, objt, throw_ex, regex_lookup)

        if self._dav_type == self.eDavType.Func:
            return self._val_func(src, obj, objt, throw_ex, func_lookup)

        return False


    def _val_not_null(self, src: str, obj: object, objt: type, throw_ex: bool) -> bool:
        """
        Ensure the object is not null.

        :param src: The source name of the object.
        :param obj: The object value to check.
        :param objt: The object type.
        :param throw_ex: Raise an exception if the object does not pass the validation.
        :return: True/False if object passes the DAV validation.
        """
        if objt == str:
            if not obj:
                return self._failed(throw_ex, 'Value [%s] cannot be null.' % src)
        elif objt == datetime.date:
            if obj == datetime.date.min:
                return self._failed(throw_ex, 'Value [%s] cannot be null.' % src)
        elif objt == datetime.datetime:
            if obj == datetime.datetime.min:
                return self._failed(throw_ex, 'Value [%s] cannot be null.' % src)
        elif objt == datetime.time:
            if obj == datetime.time.min:
                return self._failed(throw_ex, 'Value [%s] cannot be null.' % src)
        elif objt in (bytes, bytearray):
            if not obj:
                return self._failed(throw_ex, 'Value [%s] cannot be null.' % src)

        return True


    def _val_min(self, src: str, obj: object, objt: type, throw_ex: bool) -> bool:
        """
        Ensure the object is greater equal to the min.

        :param src: The source name of the object.
        :param obj: The object value to check.
        :param objt: The object type.
        :param throw_ex: Raise an exception if the object does not pass the validation.
        :return: True/False if object passes the DAV validation.
        """
        if objt == str or objt == bytes or objt == bytearray or isinstance(obj, list):
            if len(obj) < self._val:
                return self._failed(throw_ex, 'Value [%s:(%d)] below minimum length [%d].' % (src, len(obj), self._val))
        elif obj < self._val:
            return self._failed(throw_ex, 'Value [%s:%s] below minimum value [%s].' % (src, str(obj), str(self._val)))

        return True


    def _val_max(self, src: str, obj: object, objt: type, throw_ex: bool) -> bool:
        """
        Ensure the object is less than or equal to the max.

        :param src: The source name of the object.
        :param obj: The object value to check.
        :param objt: The object type.
        :param throw_ex: Raise an exception if the object does not pass the validation.
        :return: True/False if object passes the DAV validation.
        """
        if objt == str or objt == bytes or objt == bytearray or isinstance(obj, list):
            if len(obj) > self._val:
                return self._failed(throw_ex, 'Value [%s:(%d)] above maximum length [%d].' % (src, len(obj), self._val))
        elif obj > self._val:
            return self._failed(throw_ex, 'Value [%s:%s] above maximum value [%s].' % (src, str(obj), str(self._val)))

        return True


    def _val_in(self, src: str, obj: object, objt: type, throw_ex: bool) -> bool:
        """
        Ensure the object is in a list.

        :param src: The source name of the object.
        :param obj: The object value to check.
        :param objt: The object type.
        :param throw_ex: Raise an exception if the object does not pass the validation.
        :return: True/False if object passes the DAV validation.
        """
        if objt == bytes or objt == bytearray or isinstance(obj, list):
            raise xMettle('Cannot valIn a byte array!', __name__, xMettle.eCode.InternalException)

        if obj not in self._val:
            return self._failed(throw_ex, 'Value [%s:%s] not expected.' % (src, str(obj)))

        return True


    def _val_not_in(self, src: str, obj: object, objt: type, throw_ex: bool) -> bool:
        """
        Ensure the object is not in a list.

        :param src: The source name of the object.
        :param obj: The object value to check.
        :param objt: The object type.
        :param throw_ex: Raise an exception if the object does not pass the validation.
        :return: True/False if object passes the DAV validation.
        """
        if objt == bytes or objt == bytearray or isinstance(obj, list):
            raise xMettle('Cannot valOuts a byte array!', __name__, xMettle.eCode.InternalException)

        if obj in self._val:
            return self._failed(throw_ex, 'Value [%s:%s] not allowed.' % (src, str(obj)))

        return True


    def _val_regex(self, src: str, obj: object, objt: type, throw_ex: bool, regex_lookup: dict) -> bool:
        """
        Ensure the object passes the regex validation.

        :param src: The source name of the object.
        :param obj: The object value to check.
        :param objt: The object type.
        :param throw_ex: Raise an exception if the object does not pass the validation.
        :param regex_lookup: Dictionary of regex expressions.
        :return: True/False if object passes the DAV validation.
        """
        if obj is None or (objt == str and not obj):
            return True

        if regex_lookup is None:
            raise Exception('Regex lookup not set.')

        if objt in (bytes, bytearray):
            raise xMettle('Cannot regex a byte array!', __name__, xMettle.eCode.InternalException)

        regexp = regex_lookup.get(self._val)

        if regexp is None:
            raise Exception('Regex lookup [%s] not found for [src:%s, obj:%s]' % (self._val, src, str(obj)))

        if not regexp.match(str(obj)):
            return self._failed(throw_ex, 'Value [%s:%s] failed regex validation [%s].' % (src, str(obj), self._val))

        return True


    def _val_func(self, src: str, obj, objt, throw_ex: bool, func_lookup: dict) -> bool:
        """
        Call a function to see if the object passes its validation.

        :param src: The source name of the object.
        :param obj: (object) The object value to check.
        :param objt: (type) The object type.
        :param throw_ex: Raise an exception if the object does not pass the validation.
        :param func_lookup: Dictionary of functions.
        :return: True/False if object passes the DAV validation.
        """
        if func_lookup is None:
            raise Exception('Function lookup not set.')

        func = func_lookup.get(self._val)

        if func is None:
            raise Exception('Function lookup [%s] not found for [src:%s]' % (self._val, src))

        if not callable(func):
            raise Exception('Function lookup [%s] not callable for [src:%s]' % (self._val, src))

        if not func(src, obj, objt):
            if objt in (bytes, bytearray):
                return self._failed(throw_ex, 'Value [%s:(%d)] failed function validation [%s].' % (src, len(obj), self._val))

            return self._failed(throw_ex, 'Value [%s:%s] failed function validation [%s].' % (src, str(obj), self._val))

        return True


    @staticmethod
    def _failed(throw_ex, msg: str) -> bool:
        """
        Fail with either return False, or raising an exception.

        :param throw_ex: (bool/list) Throw, return, or append msg.
        :param msg: (string) The error message.
        :return: Always returns false
        """
        if isinstance(throw_ex, list):
            throw_ex.append(msg)
            return False

        if throw_ex:
            raise xMettle(msg, __name__, xMettle.eCode.DavException)

        return False
