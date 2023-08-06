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

from mettle.braze.itransport_settings import ITransportSettings


class TransportServerSettings(ITransportSettings):
    """
    Contains all the settings requirerd by the TransportServer
    """

    def __init__(self,
                 service: str,
                 timeout: float,
                 retrys: int = 5,
                 managed: bool = False,
                 socket_fd = None):
        """
        Constructor takes all the settings required for a socket server transport.

        :param service: The port number of the server to connect on.
        :param timeout: The timeout in seconds to wait before raising an exception.
        :param retrys: The number of retrys to perform on a failed socket read/write operation.
        :param managed:  The port is managed and opened by parent process.
        :param socket_fd: (int/obj) The socket file descriptor/windows obj to use if the socket is managed.
        """
        self.service   = service
        self.timeout   = timeout
        self.retrys    = retrys
        self.managed   = managed
        self.socket_fd = socket_fd
