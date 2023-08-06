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


class ITransport:
    """
    This is the transport interface for mettle.braze.
    """

    def construct(self, settings):
        """
        Creates the transport object with all required params/settings.

        :param settings: (mettle.braze.ITransportSettings) the settings object required to construct the object.
        """
        pass


    def destruct(self):
        """
        Destructs the transport, freeing all resources.
        """
        pass


    def signature(self):
        """
        The unique signature of this transport.
        """
        pass


    def new_reader(self, stream):
        """
        Creates a reader object for this specific transport.

        :param stream: (mettle.io.IStream) the stream object that the reader object will use.

        :return: (mettle.io.IReader) the created reader object.
        """
        pass


    def new_writer(self, stream):
        """
        Creates a writer object for this specific transport.

        :param sream: (mettle.io.IStream) the stream object that the writer object will use.
        :return: (mettle.io.IWriter) the created writer object.
        """
        pass


    def newStream(self):
        """
        Creates an empty stream type that this transport uses for writing/reading.

        :return: (mettle.io.IStream) the created stream object.
        """
        pass


    def create_header(self):
        """
        Creates a header for this transport.

        :return: (mettle.io.RpcHeader) returns a standard or derrived object of mettle.io.RpcHeader for the transport.
        """
        pass


    def send(self, head, data):
        """
        Sends a header and a stream of data through the transport.

        :param header: (mettle.io.RpcHeader) a plain or derrived mettle.io.RpcHeader.
        :param data: (mettle.io.IStream) the stream of data to be written.
        """
        pass


    def send_error_message(self, head, err_msg: str):
        """
        Sends a header and error message through the transport.

        :param header: (mettle.io.RpcHeader) a plain or derrived mettle.io.RpcHeader.
        :param err_msg: The error message.
        """
        pass


    def receive_header(self, head):
        """
        Receieves a header from the transport.

        :param header: (mettle.io.RpcHeader) a plain or derrived mettle.io.RpcHeader that will be received.
        """
        pass


    def receive(self, head):
        """
        Receieves the body of a call from the transport.

        :param header: (mettle.io.RpcHeader) a plain or derrived mettle.io.RpcHeader.

        :return: (mettle.io.IStream): returns a stream that contains data received.
        """
        pass


    def receive_error_message(self, head) -> str:
        """
        Receieves an error message from the transport.

        :param header: (mettle.io.RpcHeader) a plain or derrived mettle.io.RpcHeader.
        :return: the error message that was received.
        """
        pass


    def terminate(self):
        """
        Tell the transport to terminate.
        """
        pass


    def house_keeping(self):
        """
        For server transport, perform house keeping
        """
        pass


    def wait_for_connection(self, timeOut: float) -> bool:
        """
        For server transport, the max tme to wait for a client to connect.

        :param timeOut: Time to wait in seconds for a connection.
        :return: True if a client connected, else False if time out.
        """
        pass


    def client_address(self) -> str:
        """
        For server transport, gets the address of the connecting client.

        :return: A string representation of the client address.
        """
        pass
