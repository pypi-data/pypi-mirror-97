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

from mettle.braze.tcp.socket_tcp import SocketTcp

from mettle.lib.xmettle import xMettle

import socket


class SocketTcpClient(SocketTcp):
    """
    The standard socket client implementation for mettle braze.
    """

    def __init__(self, host: str, service: str, timeout: float):
        """
        Constructor.

        :param host: The host server.
        :param service:  The service/port to connect on.
        :param timeout: The timout for all socket operations in seconds.
        """
        SocketTcp.__init__(self, timeout, 5)

        self._host      = host
        self._port      = self.port_from_service(service)
        self._addr_info = None


    def __del__(self):
        """
        Destructor.
        """
        SocketTcp.__del__(self)


    def get_host(self) -> str:
        """
        Gets the current host the client is connecting to.

        :return: the host the client is attached to.
        """
        return self._host


    def set_host(self, value: str):
        """
        Sets a new host the client must to connect to.

        :param value: The new host for the client.
        """
        self._host      = value
        self._addr_info = None


    def get_port(self) -> int:
        """
        Gets the current port the client is using.

        :return: Port the client is attached to.
        """
        return self._port


    def set_port(self, value: int):
        """
        Sets a new port the client must connect to.

        :param value: The new port for the client.
        """
        self._port      = value
        self._addr_info = None


    def open(self):
        """
        Opens a socket connection to the server.
        """
        self.close()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._sock.settimeout(self._timeout)

        if self._addr_info is None:
            self._addr_info = socket.getaddrinfo(self._host, self._port, proto=socket.IPPROTO_TCP)

        try:
            self._sock.connect((self._host, self._port))
        except OSError as ex:
            raise xMettle('Failed to connect to the server. (%s)' % str(ex),
                          src = SocketTcpClient.__name__,
                          errCode = xMettle.eCode.ComsServerError)
