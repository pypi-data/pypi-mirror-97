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

from datetime import tzinfo, timedelta, datetime


class TimeZone(tzinfo):
    """
    A generic time zone class where you specify the time zone in hours/minutes.
    """
    TZ_ABR_MAP = {
        "UTC-1200" : "Y",
        "UTC-1100" : "SST",
        "UTC-1000" : "TAHT",
        "UTC-0930" : "MART",
        "UTC-0900" : "AKST",
        "UTC-0800" : "PST",
        "UTC-0700" : "MST",
        "UTC-0600" : "EAST",
        "UTC-0500" : "CIST",
        "UTC-0400" : "BOT",
        "UTC-0300" : "GFT",
        "UTC-0200" : "CVT",
        "UTC-0100" : "A",
        "UTC+0000" : "UTC",
        "UTC+0100" : "CET",
        "UTC+0200" : "SAST",
        "UTC+0300" : "TRT",
        "UTC+0400" : "SCT",
        "UTC+0500" : "TMT",
        "UTC+0530" : "IST",
        "UTC+0545" : "NPT",
        "UTC+0600" : "BST",
        "UTC+0630" : "CCT",
        "UTC+0700" : "DAVT",
        "UTC+0800" : "HKT",
        "UTC+0830" : "PYT",
        "UTC+0900" : "JST",
        "UTC+1000" : "VLAT",
        "UTC+1030" : "LHST",
        "UTC+1100" : "BST",
        "UTC+1200" : "FJT",
        "UTC+1245" : "CHAST",
        "UTC+1300" : "PHOT",
        "UTC+1400" : "WST",
    }


    def __init__(self, tzhour: int = 0, tzmin: int = 0):
        """
        Constructor.

        :param tzhour: The hours offset from utc.
        :param tzmin: The minutes offset from utc.
        """
        if tzhour < -14 or tzhour > 14:
            raise Exception("Time zone hour [%d] not valid." % tzhour)

        if tzmin < 0 or tzmin > 59:
            raise Exception("Time zone minute [%d] not valid." % tzmin)

        self.tzhour = tzhour
        self.tzmin  = tzmin
        self._tzoff = timedelta(hours=self.tzhour, minutes=self.tzmin)

        if self.tzhour >= 0:
            self._tzabr  = 'UTC+%2.2d%2.2d' % (tzhour, tzmin)
        else:
            self._tzabr  = 'UTC%2.2d%2.2d' % (tzhour, tzmin)

        abrMap = self.TZ_ABR_MAP.get(self._tzabr)

        if abrMap is not None:
            self._tzabr = abrMap


    def utcoffset(self, dt: datetime) -> int:
        """
        Implemented abstract method.
        """
        return self._tzoff


    def dst(self, dt: datetime) -> timedelta:
        """
        Implemented abstract method.
        """
        return timedelta(0)


    def tzname(self, dt: datetime) -> str:
        """
        Implemented abstract method.
        """
        return self._tzabr


    @staticmethod
    def local_tz() -> "TimeZone":
        """
        Get the local timezone.

        :return: The current timezone.
        """
        import time

        hr, mn = divmod(0 - time.timezone, 3600)

        return TimeZone(hr, mn)

    @staticmethod
    def utc_tz() -> "TimeZone":
        """
        Get the utc timezone.

        :return: The utc timezone.
        """
        return TimeZone(0, 0)
