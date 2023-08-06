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


class IServerInterface:
    """
    This is the server interface.
    """

    def _shutdown_server(self) -> bool:
        """
        Return if the server should shutdown or not.

        :return: True if the server should shutdown else False.
        """
        pass


    def _slacktime_handler(self):
        """
        A house keeping call that is called periodically while the server is not busy.
        """
        pass


    def _construct(self):
        """
        Called right after the server is created.
        """
        pass


    def _destruct(self):
        """
        Called right before the server is destroyed.
        """
        pass


    def _init_dav_cache(self, rpc_name: str, dvc):
        """
        Used to optionally init a dav cache object.

        :param rpc_name: Name of the rpc call.
        :param dvc: (mettle.lib.DavCache) The cache to set.
        """
        pass


    def _validate_rpc_token(self, tok: object) -> object:
        """
        Used to read an rpc token of some kind, validate it and potentially
        return a new one.

        :param tok: The token object.
        :return: The new/updated token object.
        """
        pass


    def _has_new_rpc_token(self) -> object:
        """
        This method should return a new rpc token if there is one
        for login session.  Typically a server would only have a new
        token if a user has succesfully logged in.

        :return : None if no new token, else the token object.
        """
        pass


    def _set_rpc_token_data(self, tdata: dict):
        """
        The result of the Server.auth method call is passed to this function so the
        server can do what it needs to with it.

        :param tdata: Token data.
        """
        pass


    def _set_impl_data(self, impl_data: dict):
        """
        Pure virtual method that can receive some kind of data object that can be used
        to service an rpc. A marshaller will call this method directly before calling
        the actual service server calls.
        """
        pass
