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

from mettle.lib         import xMettle
from .iserver_marshaler import IServerMarshaler
from .server            import Server


class ServerMultiMarsh(Server):
    """
    The braze multi marshaler server.
    """

    def __init__(self, marshaler: list, trans, log_id: str = 'brazeServer'):
        """
        Constructor,

        param marshaler: List of mettle.braze.IServerMarshaler objects to use.
        param trans: (mettle.braze.ITransport) The transport object this server will use.
        param log_id: The log id or Logging object to use.
        """
        self._marsh_lookup = {}
        self._act_marsh    = None

        if type(marshaler) != list or len(marshaler) < 1:
            raise Exception('Arguement [marshaler] is not a list or is empty.')

        for marsh in marshaler:
            if not isinstance(marsh, IServerMarshaler):
                raise Exception('Arguement [marshaler] contains non IServerMarshaler objects.')

            if self._marsh_lookup.get(marsh._signature()):
                raise Exception('Duplicate marshaler signature [%d] detected.' % marsh._signature())

            self._marsh_lookup[marsh._signature()] = marsh

        Server.__init__(self, marshaler, trans, log_id)


    def __del__(self):
        pass


    def get_marshaler(self):
        return self._act_marsh


    def construct(self):
        self.destruct()

        for marsh in self._marshaler:
            marsh._server_impl()._construct()


    def destruct(self):
        for marsh in self._marshaler:
            marsh._server_impl()._destruct()

        self._trans.terminate()


    def shutdown_server(self):
        for marsh in self._marshaler:
            marsh._server_impl()._shutdownServer()


    def slacktime_handler(self):
        for marsh in self._marshaler:
            marsh._server_impl()._slackTimeHandler()


    def wait_for_connection(self, time_out: float) -> bool:
        return False


    def receive(self) -> tuple:
        try:
            self._act_marsh = None

            head = self._trans.create_header()

            self._trans.receive_header(head)

            self._act_marsh = self._marsh_lookup.get(head.server_signature)

            if not self._act_marsh:
                raise xMettle(
                    'Server - Invalid server signature received [client:%s, server:?]' % (
                        str(head.server_signature)),
                    src = Server.__name__,
                    errCode = xMettle.eCode.ComsSignature)

            if head.transport_signature != self._trans.signature():
                raise xMettle(
                    'Server - Invalid transport signature received [client:%s, server:%s]' % (
                        str(head.transport_signature), str(self._trans.signature())),
                    src = Server.__name__,
                    errCode = xMettle.eCode.ComsSignature)

            remote_sig = head.client_signature
            in_stream  = self._trans.receive(head)

            return remote_sig, in_stream, None, None

        except xMettle as x:
            self._log.error("%sException caught in ServerMultiMarsh.receive(msg:%s)" % (self.server_id(), str(x)))

            return 0, None, x.get_error_code(), str(x)
