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

from enum import IntEnum


class xMettle(Exception):
    """
    The base exception class for the mettle library.
    """


    class eCode(IntEnum):
        """
        The error code enumeration for all mettle exceptions.  These
        error codes are syncronized with the C++, C#, and Java xMettle objects.
        """
        NoError    = 0

        UnknownException   = -101
        StandardException  = -102
        TerminalException  = -103
        OutOfMemory        = -104
        SocketTimeout      = -105
        InternalException  = -106
        DavException       = -107
        CredExpired        = -108
        CredInvalid        = -109
        CredDenied         = -110
        TokenExpired       = -111
        TokenInvalid       = -112
        StandardMaxError   = -199

        ComsStandardError = -200
        ComsTimeOut       = -201
        ComsInvalidHeader = -202
        ComsServerError   = -203
        ComsReceiveError  = -204
        ComsSignature     = -205
        ComsLastError     = -299

        DBStandardError       = -300
        DBForeignKeyViolation = -301
        DBPrimaryKeyViolation = -302
        DBUniqueKeyViolation  = -303
        DBLockNoWaitFailed    = -304
        DBBokenConnection     = -305
        DBLastError           = -399


    def __init__(self, msg, src="N/A", errCode=eCode.StandardException):
        """
        Constructor.

        :param msg: The exception message.
        :param src: The source object that threw this exception.
        :param errCode: (eCode) The error code/type this exception represents.
        """
        Exception.__init__(self, msg)

        self._src     = src
        self._errCode = errCode


    def get_error_code(self) -> eCode:
        """
        Gets the error code of this exception.

        :return: The error code.
        """
        return self._errCode


    def get_source(self) -> str:
        """
        Gets the source object name that raised this exception.

        :return: The source object.
        """
        return self._src


    def is_db_exception(self) -> bool:
        """
        Check if this a database exception.

        :return: True if this is a database exception else return False.
        """
        if self._errCode <= self.eCode.DBStandardError and self._errCode >= self.eCode.DBLastError:
            return True

        return False


    def is_coms_exception(self) -> bool:
        """
        Check if this a communication(braze) exception.

        :return: True if this is a communication exception else return False.
        """
        if self._errCode <= self.eCode.ComsTimeOut and self._errCode >= self.eCode.ComsLastError:
            return True

        return False


    def is_standard_exception(self) -> bool:
        """
        Check if this a standard exception.

        :return: True if this is a standard exception else return False.
        """
        if self.isDBException() or self.isComsException():
            return False

        return True


    def is_db_broken_connection(self) -> bool:
        """
        Check if this a db lost connection exception.

        :return: True if this is a db broken connection error.
        """
        return self._errCode == self.eCode.DBBokenConnection
