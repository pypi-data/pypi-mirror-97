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

from mettle.io import ISerializable


class RpcHeader(ISerializable):

    def __init__(self):
        """
        Constructor, initialize the four header fields
        """
        self.client_signature    = ''
        self.server_signature    = ''
        self.transport_signature = 0
        self.error_code          = 0


    def _name(self) -> str:
        return 'RpcHeader'


    def _deserialize(self, r, oname: str):
        if not oname:
            oname = self._name()

        r.read_start(oname)
        self.transport_signature = r.read_int32("TransportSignature")
        self.error_code          = r.read_int32("ErrorCode")
        self.client_signature    = r.read_string("ClientSignature")
        self.server_signature    = r.read_string("ServerSignature")
        r.read_end(oname)


    def _serialize(self, w, oname: str):
        if not oname:
            oname = self._name()

        w.write_start(oname)
        w.write_int32("TransportSignature", self.transport_signature)
        w.write_int32("ErrorCode",          int(self.error_code))
        w.write_string("ClientSignature",   self.client_signature)
        w.write_string("ServerSignature",   self.server_signature)
        w.write_end(oname)

    def clear(self):
        self.client_signature    = ''
        self.server_signature    = ''
        self.transport_signature = 0
        self.error_code          = 0
