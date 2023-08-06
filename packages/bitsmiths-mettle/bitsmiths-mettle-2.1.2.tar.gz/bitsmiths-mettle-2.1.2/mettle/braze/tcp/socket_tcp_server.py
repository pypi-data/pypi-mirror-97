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


class SocketTcpServer(SocketTcp):
    """
    The standard socket server implementation for mettle braze.
    """

    def __init__(self, timeout: float, retrys = 5):
        """
        Constructor.

        :param timeout: The timout for all socket operations in seconds.
        :param retrys: The number of retrys for socket operations.
        """
        SocketTcp.__init__(self, timeout, retrys)

        self._socket_owner  = True
        self._addr_info     = None
        self._accepted_sock = None
        self._accepted_addr = None


    def __del__(self):
        """
        Destructor.
        """
        self.close()


    def close(self):
        """
        Closes the socket server socket and the accepted socket.
        """
        self.close_accepted()

        self._addr_info = None

        if self._sock is None:
            return

        if not self._socket_owner:
            self._sock         = None
            self._socket_owner = True
            return

        try:
            self._sock.close()
        finally:
            self._sock = None


    def close_accepted(self):
        """
        Closes the accepted remote scoket.
        """
        if not self._accepted_sock:
            return

        try:
            self._accepted_sock.close()
        finally:
            self._accepted_sock = None
            self._accepted_addr = None


    def intitialize(self, socket):
        """
        Initializes the object with an externally managed socket.

        :param socket: (object) The externally managed scoket.
        """
        self.close()

        self._sock        = socket
        self._socket_owner = False


    def open(self, service: str, backlog: int, multi_socket: bool):
        """
        Opens the server socket.

        :param service: (string) The port number of the server socket.
        :param backlog: (int) The number of backlog requests to read upon opening the socket.
        :param multi_socket: (bool) Allow multiple processes/threads to listen on this socket.
        """
        self.close()

        type_mask = socket.SOCK_STREAM

        self._socket_owner = True
        self._addr_info    = socket.getaddrinfo(None, service, proto=socket.IPPROTO_TCP)

        ipv4 = None
        ipv6 = None

        for ai in self._addr_info:
            if ai[0] == socket.AddressFamily.AF_INET and ipv4 is None:
                ipv4 = ai[4]
            elif ai[0] == socket.AddressFamily.AF_INET6 and ipv6 is None:
                ipv6 = (ai[4][0], ai[4][1])

            if ipv4 and ipv6:
                break

        if ipv4:
            self._sock = socket.socket(socket.AF_INET, type_mask)
        elif ipv6:
            self._sock = socket.socket(socket.AF_INET6, type_mask)
        else:
            raise xMettle("No IPV4 or IPV6 socket address found.",
                          src = SocketTcp.__name__,
                          errCode = xMettle.eCode.ComsStandardError)

        if hasattr(socket, 'ioctl') and hasattr(socket, 'SIO_RCVALL'):
            getattr(socket, 'ioctl')(getattr(socket, 'SIO_RCVALL'), getattr(socket, 'RCVALL_ON'))

        self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._sock.settimeout(self._timeout)
        self._sock.setblocking(True)

        if multi_socket:
            if hasattr(socket, 'SO_REUSEADDR'):
                self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            if hasattr(socket, 'SO_REUSEPORT'):
                self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        if ipv4:
            self._sock.bind(ipv4)
        else:
            self._sock.bind(ipv6)

        self._sock.listen(backlog)


    def open_managed(self, socket_fd):
        """
        Attaches the object to a socket opened by a parent process or sibling thread.
        Please note that this has not been tested on wndows yet.

        :param socket_fd: (int/obj) The socket file descriptor/windows object to attach to.
        """
        self.close()

        self._socket_owner = False
        self._sock         = socket.socket(fileno=socket_fd)
        # self._socket      = socket.fromfd(socket_fd, socket.AF_INET, socket.SOCK_STREAM)


    def wait_for_connection(self, wait_timeout: float) -> bool:
        """
        Waits for a socket connection up to the wait timeout.

        :param wait_timeout: (float) Timeout for the wait in seconds.
        """
        if not self.wait_for_read(wait_timeout):
            return False

        self.close_accepted()

        self._accepted_sock, self._accepted_addr = self._sock.accept()

        self._accepted_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        return True


    def send_size(self, data, data_size: int):
        """
        Override base method.
        """
        total_sent = 0

        while total_sent < data_size:
            sent = self._accepted_sock.send(data[total_sent:])

            if sent == 0:
                raise xMettle("Socket connection broken pipe.",
                              src = SocketTcp.__name__,
                              errCode = xMettle.eCode.ComsStandardError)

            total_sent += sent


    def read_size(self, size: int) -> bytearray:
        """
        Override base method.
        """
        res        = bytearray(size)
        total_recv = 0

        while total_recv < size:
            chunk = self._accepted_sock.recv(size - total_recv)

            if chunk == b'':
                raise xMettle("Socket connection broken pipe.",
                              src = SocketTcp.__name__,
                              errCode = xMettle.eCode.ComsStandardError)

            res[total_recv:len(chunk)] = chunk[0:]

            total_recv += len(chunk)

        return res


    def client_address(self):
        if not self._accepted_addr:
            return 'No active client connection'

        return str(self._accepted_addr[0])
