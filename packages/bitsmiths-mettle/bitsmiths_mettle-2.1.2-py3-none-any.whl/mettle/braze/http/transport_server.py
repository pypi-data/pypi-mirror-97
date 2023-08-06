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

from mettle.io.py_json_list_reader import PyJsonListReader
from mettle.io.py_json_list_writer import PyJsonListWriter
from mettle.io.list_stream         import ListStream

from mettle.braze.itransport import ITransport

from mettle.braze.http.http_header import HttpHeader


class TransportServer(ITransport):
    """
    This the standard http transport server.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._stream = ListStream()


    def __del__(self):
        """
        Destructor.
        """
        self.destruct()


    def get_stream_list(self) -> list:
        """
        Gets the return json data stream.

        :return: The list to be jsonlized.
        """
        return self._stream.get_list()


    def set_stream_list(self, stream_list: list):
        """
        Sets the json stream to use.

        :param stream_list: The list stream.
        """
        self._stream.eat(stream_list)


    def construct(self, settings):
        """
        Initializes the transport server, connecting it to the server.

        :param settings: (mettle.braze.http.TransportServerSettings) The settings to host with.
        """
        pass


    def destruct(self):
        """
        Destorys the tranport freeing all resources.
        """
        self._stream = None


    def signature(self) -> int:
        return int('0x08779915', 16)


    def new_reader(self, stream):
        return PyJsonListReader(stream)


    def new_writer(self, stream):
        return PyJsonListWriter(stream)


    def new_stream(self):
        return ListStream()


    def create_header(self):
        return HttpHeader()


    def send(self, header, data):
        hstream = ListStream()
        wr      = self.new_writer(hstream)

        header._serialize(wr, header._name())

        hlist = hstream.get_list()
        dlist = data.get_list()

        while len(hlist):
            dlist.insert(0, hlist.pop())

        self._stream.eat(dlist)


    def send_error_message(self, header, err_msg: str):
        self._stream.clear()

        wr = self.new_writer(self._stream)

        header._serialize(wr, header._name())

        wr.write_start("ServerException")
        wr.write_string("ErrorMessage", err_msg)
        wr.write_end("ServerException")


    def receive_header(self, header):
        rr = self.new_reader(self._stream)

        header._deserialize(rr, header._name())


    def receive(self, header):
        return self._stream


    def receive_error_message(self, header):
        pass


    def terminate(self):
        pass


    def house_keeping(self):
        pass


    def wait_for_connection(self, timeOut):
        return False


    def client_address(self):
        return '<UNKNOWN>'
