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

from mettle.lib.xmettle import xMettle

import struct
import select


class SocketTcp:
    """
    This an abstract socket tcp class for the mettle braze api.
    """

    def __init__(self, timeout: float, retrys: int):
        """
        Constructor.

        :param timeout: The timout for all socket operations in seconds.
        :param retrys: The number of times to retry all socket operation.
        """
        self._timeout = timeout
        self._sock    = None


    def __del__(self):
        """
        Destructor.
        """
        self.close()


    def get_timeout(self) -> float:
        """
        Gets the current timeout.

        :returns: The timeout in seconds.
        """
        return self._timeout


    def set_timeout(self, value: float):
        """
        Sets the current timeout.

        :param value: The timeout in seconds.
        """
        self._timeout = value


    def get_socket(self):
        """
        Gets the socket object in its current state.

        :return: (socket) The socket object, could be a None value.
        """
        return self._sock


    def port_from_service(self, service: str) -> int:
        """
        Gets the port from the service string.

        :param service: The port number of service string.
        :return: The port number for the service string.
        """
        if not service.isdigit():
            raise xMettle('Parsing service names not yet suppoted, please use port number. (service:%s)' % service,
                          src = SocketTcp.__name__)

        return int(service)


    def close(self):
        """
        Closes the socket if it is open.
        """
        if self._sock:
            self._sock.close()
            self._sock = None


    def send(self, data: bytes):
        """
        Send a byte array to the socket, first sends the length of the byte array to the socket.

        :param data: (bytes) The byte array to be sent.
        """
        if len(data) < 1:
            return

        data_size = struct.pack('!i', len(data))

        self.send_size(data_size, len(data_size))
        self.send_size(data,      len(data))


    def send_size(self, data: bytes, data_size: int):
        """
        Sends a byte array without first prefixing its length.

        :param data: The byte array to be sent.
        :param data_size: Size of the data.
        """
        total_sent = 0

        while total_sent < data_size:
            sent = self._sock.send(data[total_sent:])

            if sent == 0:
                raise xMettle("Socket connection broken pipe.",
                              src = SocketTcp.__name__,
                              errCode = xMettle.eCode.ComsStandardError)

            total_sent += sent


    def receive(self) -> bytearray:
        """
        Recieves data from the socket, expects a length integer, then a stream of bytes.

        :return: The data received from the socket.
        """
        recv_size = self.read_length()

        return self.read_size(recv_size)


    def read_length(self) -> int:
        """
        Expets to read an network ordered 32 bit integer from the socket.

        :return: The integer read from the socket.
        """
        size = struct.calcsize('!i')
        ba   = self.read_size(size)

        return struct.unpack('!i', ba)[0]


    def read_size(self, size: int) -> bytearray:
        """
        Reads an expected size of bytes from the socket.

        :param size: The number of bytes to read from the socket.
        :return: The bytes read from the socket.
        """
        res        = bytearray(size)
        total_recv = 0

        while total_recv < size:
            chunk = self._sock.recv(size - total_recv)

            if chunk == b'':
                raise xMettle("Socket connection broken pipe.",
                              src = SocketTcp.__name__,
                              errCode = xMettle.eCode.ComsStandardError)

            res[total_recv:len(chunk)] = chunk[0:]

            total_recv += len(chunk)

        return res


    def wait_for_read(self, time_out: float) -> bool:
        """
        Wait for the given timeout before attempting to read.

        :param time_out: Time in seconds to wait.
        :return: True if the socket is ready for eading, else False.
        """
        if time_out < 0.01:
            return True

        reade_rdy, write_rdy, except_rdy = select.select([self._sock.fileno()], [], [], time_out)

        if not reade_rdy or reade_rdy[0] != self._sock.fileno():
            return False

        return True


    def wait_for_write(self, time_out: float) -> bool:
        """
        Wait for the given time_out before attempting to write.

        :param time_out: Time in seconds to wait.
        :return: True if the socket is ready for writing, else False.
        """
        if time_out < 0.01:
            return True

        reade_rdy, write_rdy, except_rdy = select.select([], [self._sock.fileno()], [], time_out)

        if not write_rdy or write_rdy[0] != self._sock.fileno():
            return False

        return True
