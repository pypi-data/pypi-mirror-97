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

from .itransport import ITransport

from mettle.lib import xMettle


class Client:
    """
    The client braze client.
    """

    def __init__(self, trans):
        """
        The constructor.

        :param trans: (mettle.braze.ITransport) The transport object this client will use.
        """
        self._trans = trans


    def get_transport(self) -> ITransport:
        """
        Gets the transport the client is using.

        :return: The clients transport object.
        """
        return self._trans


    def send(self, marshaler, remote_signature, data):
        """
        Send a data stream through to the server.

        :param marshaler: (mettle.braze.IClientMarshaler) the marshaling object to use.
        :param remote_signature: (str) the signature or the remote call.
        :param data: (mettle.io.IStream) the stream of data to send to the server.
        """
        head = self._trans.create_header()

        head.client_signature     = remote_signature
        head.server_signature     = marshaler._signature()
        head.transport_signature  = self._trans.signature()

        self._trans.send(head, data)


    def receive(self, marshaler, remote_signature: int):
        """
        Receive a data response from the server.

        :param marshaler: (mettle.braze.IClientMarshaler) The marshaling object to use.
        :param remote_signature: (int) The signature or the remote call.
        :return: (mettle.io.IStream) The stream of data to returned from the server.
        """
        head = self._trans.create_header()

        self._trans.receive_header(head)

        if head.server_signature != marshaler._signature():
            raise xMettle('Client - Invalid server signature retured from server (%s)' % head.server_signature,
                          src = Client.__name__,
                          errCode = xMettle.eCode.ComsSignature)

        if head.transport_signature != self._trans.signature():
            raise xMettle('Client - Invalid transport signature retured from server (%d)' % head.transport_signature,
                          src = Client.__name__,
                          errCode = xMettle.eCode.ComsSignature)

        if head.error_code != 0:
            errMsg = self._trans.receive_error_message(head)
            raise xMettle(errMsg, src = Client.__name__, errCode = head.error_code)

        if head.client_signature != remote_signature:
            raise xMettle('Client - Invalid client signature retured from server (%s)' % head.client_signature,
                          src = Client.__name__,
                          errCode = xMettle.eCode.ComsSignature)

        return self._trans.receive(head)
