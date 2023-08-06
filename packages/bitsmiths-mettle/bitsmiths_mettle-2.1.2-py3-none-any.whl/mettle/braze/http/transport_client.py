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

import urllib
import urllib.request
import json
import ssl

from mettle.io.py_json_list_reader import PyJsonListReader
from mettle.io.py_json_list_writer import PyJsonListWriter
from mettle.io.list_stream         import ListStream

from mettle.braze.itransport       import ITransport

from .http_header               import HttpHeader
from .transport_client_settings import TransportClientSettings


class TransportClient(ITransport):
    """
    This the standard http transport client.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._stream  = ListStream()
        self._url     = ''
        self._cookies = []
        self._tokens  = []


    def __del__(self):
        """
        Destructor.
        """
        self.destruct()


    def get_stream_list(self):
        """
        Gets the return json data stream.

        :return: The list to be jsonlized.
        """
        return self._stream.get_list()


    def set_stream_list(self, stream_list: ListStream):
        """
        Sets the json stream to use.

        :param stream_list: The list stream.
        """
        self._stream.eat(stream_list)


    def construct(self, settings: TransportClientSettings):
        """
        Initializes the transport client.

        :param settings: The settings to server the client with.
        """
        self._url     = settings.url
        self._sig_url = settings.sig_url


    def destruct(self):
        """
        Destorys the tranport freeing all resources.
        """
        self._stream = None


    def signature(self) -> int:
        return int('0x08779915', 16)


    def new_reader(self, stream: ListStream):
        return PyJsonListReader(stream)


    def new_writer(self, stream: ListStream):
        return PyJsonListWriter(stream)


    def new_stream(self) -> ListStream:
        return ListStream()


    def create_header(self) -> HttpHeader:
        return HttpHeader()


    def send(self, header: HttpHeader, data):
        hstream = ListStream()
        wr      = self.new_writer(hstream)

        header._serialize(wr, header._name())

        hlist = hstream.get_list()
        dlist = data.get_list()

        while len(hlist):
            dlist.insert(0, hlist.pop())

        self._stream.eat(dlist)

        self._do_http_call(header)


    def send_error_message(self, header: HttpHeader, err_msg: str):
        pass


    def receive_header(self, header: HttpHeader):
        rr = self.new_reader(self._stream)

        header._deserialize(rr, header._name())


    def receive(self, header: HttpHeader):
        return self._stream


    def receive_error_message(self, header: HttpHeader):
        rr = self.new_reader(self._stream)

        rr.read_start("ServerException")
        err_msg = rr.read_string("ErrorMessage")
        rr.write_end("ServerException")

        return err_msg


    def terminate(self):
        pass


    def house_keeping(self):
        pass


    def wait_for_connection(self, time_out: float) -> bool:
        return False


    def client_address(self) -> str:
        return '<UNKNOWN>'


    def _do_http_call(self, header: HttpHeader = None):
        """
        Virtual method implements defaul urllib implementation of a client
        http handler.

        :param header: Optionally pass in the header for extra info.
        """
        headers     = {}
        content_str = '' if not self._stream else json.dumps(self._stream.get_list())

        headers['Content-Type'] = 'application/json'

        for ck in self._cookies:
            headers['Cookie'] = ck

        for tok in self._tokens:
            headers['Authorization'] = tok

        ctx = ssl.create_default_context()

        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE

        if self._sig_url and header:
            url = '%s/%s/%s' % (self._url, header.server_signature, header.client_signature)
        else:
            url = self._url

        conn = urllib.request.Request(
            url,
            data=bytes(content_str, 'utf8'),
            method='POST',
            headers=headers)

        with urllib.request.urlopen(conn, timeout=5.0, context=ctx) as resp:
            data  = resp.read()

            if data is None:
                raise Exception('Rest call [%s] failed: %s' % (self._url, str(data)))

            if not data:
                return None

            reso = json.loads(str(data, 'utf8'))
            self._stream.eat(reso)

            self._cookies.clear()

            for head, val in resp.headers.items():
                if head == 'set-cookie':
                    self._cookies.append(val)
