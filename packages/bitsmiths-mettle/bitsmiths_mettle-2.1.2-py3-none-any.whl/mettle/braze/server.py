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

import logging
import traceback

from .iserver_marshaler import IServerMarshaler
from .itransport        import ITransport

from mettle.lib.xmettle import xMettle


class Server:
    """
    The braze server.
    """

    def __init__(self, marshaler: IServerMarshaler, trans: ITransport, log_id: str = 'brazeServer'):
        """
        The constructor.

        :param marshaler: The marshaler object this server will use.
        :param trans: The transport object this server will use.
        :param log_id: (string/logging.Logger) The log id or Logging object to use.
        """
        self._marshaler = marshaler
        self._trans     = trans

        if type(log_id) == str:
            self._log = logging.getLogger(log_id)
        elif isinstance(log_id, logging.Logger):
            self._log = log_id

        if not self._log:
            self._log = logging.getLogger()


    def __del__(self):
        """
        The destructor.
        """
        self.destruct()


    def get_marshaler(self) -> IServerMarshaler:
        """
        Gets the marshaler the server is using.

        :return: The servers marshaler object.
        """
        return self._marshaler


    def get_transport(self) -> ITransport:
        """
        Gets the transport the server is using.

        :return: The clients transport object.
        """
        return self._trans


    def logger(self):
        """
        Gets the server logger.

        :returns: The logger
        """
        return self._log


    def server_id(self) -> str:
        """
        Gets the servers identifier, this should be overwritten by the system.

        :return: (string) The servers identifier.
        """
        return "[BrazeServer] "


    def construct(self):
        """
        This virtual method is called by run before the main loop handler.
        """
        self.destruct()
        self.get_marshaler()._server_impl()._construct()


    def destruct(self):
        """
        This virtual method is called by by run when the server raises an exception or shuts down normally.
        """
        self.get_marshaler()._server_impl()._destruct()
        self._trans.terminate()


    def shutdown_server(self) -> bool:
        """
        A virtual method to indicate to the run() method whether or not the server should shutdown.

        :returns: True if the server should shut down, else false.  Default implementation always returns false.
        """
        return self.get_marshaler()._server_impl()._shutdown_server()


    def slacktime_handler(self):
        """
        A virtual method that is called every x mili seconds were x is setup by the run() 'wait_timeout' arguement.
        This is useful for house keeping routines.
        """
        self.get_marshaler()._server_impl()._slacktime_handler()


    def wait_for_connection(self, time_out: float) -> bool:
        """
        Used by the run() method to wait for a connection from a client.
        This method use the servers transport object and waits based on the input arguement 'time_out'.

        :param time_out: The time in seconds to wait for a client connection.
        :returns: True if a client has made a connection, false if not client has made a connection during the time_out.
        """
        return self._trans.wait_for_connection(time_out)


    def receive(self) -> tuple:
        """
        Used by the run() method to recieves a remote call from a client.

        Note the defaul implementation of this method should not need to be overloaded unless there is a very
        specific case that the marshaler and transport cannot handle normally.

        :returns: (tuple) A tuple of four values
            remote_sig : the rpc call unique signature to we know what call the client is trying to make.
            in_stream  : the input stream the transport object will write while reading from the client.
            err_code   : if an exception is raised, the error_code will be set for the run method, else None
            err_msg    : if an exception is raised, the err_msg will be set else None
        """
        try:
            head = self._trans.create_header()

            self._trans.receive_header(head)

            if head.server_signature != self.get_marshaler()._signature():
                raise xMettle(
                    'Server - Invalid server signature received [client:%d, server:%d]' % (
                        head.server_signature, self.get_marshaler()._signature()),
                    src = Server.__name__,
                    err_code = xMettle.eCode.ComsSignature)

            if head.transport_signature != self._trans.signature():
                raise xMettle(
                    'Server - Invalid transport signature received [client:%d, server:%d]' % (
                        head.transport_signature, self._trans._signature()),
                    src = Server.__name__,
                    err_code = xMettle.eCode.ComsSignature)

            remote_sig = head.client_signature
            in_stream  = self._trans.receive(head)

            return remote_sig, in_stream, None, None

        except xMettle as x:
            self._log.error("%sException caught in Server.receive(msg:%s)" % (self.server_id(), str(x)))

            return 0, None, x.get_error_code(), str(x)


    def send(self, remote_sig: int, out_stream, err_code: int, err_msg: str):
        """
        Used by the run() method to send a remote call result back to a client.

        Note the defaul implementation of this method should not need to be overloaded unless there is a very
        specific case that the marshaler and transport cannot handle normally.

        :param remote_sig: The rpc call unique signature we are sending back to the client.
        :param out_stream: (mettle.io.IStream) The output stream the transport object will read from
                           while writing back to the client..
        :param err_code: If an exception was raised, the error_code will be sent to the client.
        :param err_msg: If an exception was raised, the err_msg will be sent to the client.
        """
        head = self._trans.create_header()

        head.client_signature     = remote_sig
        head.server_signature     = 0 if self.get_marshaler() is None else self.get_marshaler()._signature()
        head.transport_signature  = self._trans.signature()
        head.error_code           = err_code

        if err_code != 0:
            self._trans.send_error_message(head, err_msg)
            return

        self._trans.send(head, out_stream)


    def _max_consecutive_exceptions(self) -> int:
        """
        The maximum number of consective exceptions that can occur before server is blown.

        :return: (int): The number.
        """
        return 1000


    def service_rpc(self, impl_data: dict = None) -> int:
        """
        Services a remote procedure call.

        :return: (int) xMettle.Error_code.value, zero = good
        """
        remote_sig, in_stream, err_code, err_msg = self.receive()

        if err_code:
            self.send(remote_sig, None, err_code, err_msg)
            return err_code

        out_stream, err_code, err_msg = self.get_marshaler()._serve(self, remote_sig, in_stream, impl_data)

        self.send(remote_sig, out_stream, err_code, err_msg)

        if err_code:
            return err_code

        return 0


    async def service_rpc_async(self, impl_data: dict = None) -> int:
        """
        Services a remote procedure call with async. Please note this should only be used witht he server

        :param impl_data: Any data objects required for the server impl.

        :return: (int) xMettle.Error_code.value, zero = good
        """
        remote_sig, in_stream, err_code, err_msg = self.receive()

        if err_code:
            self.send(remote_sig, None, err_code, err_msg)
            return err_code

        out_stream, err_code, err_msg = await self.get_marshaler()._serve_async(self, remote_sig, in_stream, impl_data)

        self.send(remote_sig, out_stream, err_code, err_msg)

        if err_code:
            return err_code

        return 0


    def run(self, wait_timeout: float = 1.0):
        """
        The standard run implementation.

        This method put the server in running loop and by default it sleeps wait_timeout on the transport
        object when it has nothing to to check for shut down signals and running house keeping routings.
        Ideally this method should be overloaded to suit a more custome server implementation but if you need a
        a basic and robust server handler, this will do it.

        This method loops ifinately until it recieves a shutdown signal, (until the shutdown_server() method returns true.

        Note this method is for old school servers, you will need to overload a falcon/fastapi/djanjo server to serve
        these through web stack servers.

        :param wait_timeout: The time in seconds for the handler to check for shutdown request and run house keeping routines.
        """
        except_countdown = self._max_consecutive_exceptions()

        self.construct()

        self._log.info("%sServer started" % self.server_id())

        while True:
            try:
                if not self.wait_for_connection(wait_timeout):
                    if self.shutdown_server():
                        break

                    self.slacktime_handler()
                    continue

                if 0 != self.service_rpc():
                    continue

                except_countdown = self._max_consecutive_exceptions()

            except xMettle as x:
                if self.shutdown_server():
                    self._log.error("%sException caught & shutdown signal received. Ignoring exception[msg:%s, trace:%s]" % (
                        self.server_id(), str(x), traceback.format_exc()))
                    self.destruct()
                    return

                except_countdown -= 1

                if except_countdown <= 0:
                    self._log.error("%sCountdown reached (%d), blowing server with exception[msg:%s, trace:%s]" % (
                        self.server_id(), except_countdown, str(x), traceback.format_exc()))
                    self._trans.terminate()
                    raise x

                if x.get_error_code() == xMettle.eCode.TerminalException:
                    self._log.error("%sTerminal exception encountered, blowing server with exception"
                                    "[countdown:%d, msg:%s, trace:%s]" % (
                                        self.server_id(), except_countdown, str(x), traceback.format_exc()))

                self._log.warning("%sServer exception 'Counting down [%d]' Exception[msg:%s, trace:%s]" % (
                    self.server_id, except_countdown, str(x), traceback.format_exc()))
                self._trans.terminate()

            except Exception as x:
                if self.shutdown_server():
                    self._log.error("%sException caught & shutdown signal received. Ignoring exception[msg:%s, trace:%s]" % (
                        self.server_id(), str(x), traceback.format_exc()))
                    self.destruct()
                    return

                except_countdown -= 1

                if except_countdown <= 0:
                    self._log.error("%sCountdown reached (%d), blowing server with exception[msg:%s, trace:%s]" % (
                        self.server_id(), except_countdown, str(x), traceback.format_exc()))
                    self._trans.terminate()
                    raise x

                self._log.warning("%sServer exception 'Counting down [%d]' Exception[msg:%s, trace:%s]" % (
                    self.server_id, except_countdown, str(x), traceback.format_exc()))
                self._trans.terminate()

        self._log.info("%sServer shutting down" % self.server_id())

        self.destruct()


    def auth(self, rpc_name: str, rpc_auth: str, rpc_args: dict) -> dict:
        """
        Virtual method used to authentica RPC calls against some sort token/user credentials.

        This call should raise an exception if the authentication fails.

        :param rpc_name: (string) The rpc call name.
        :param rpc_auth: (string) The rpc authentication method, sort of a factory string.
        :param rpc_args: (dict) The rpc args in a dictionary.
        :return: (dict) A auth data object for the server impl to possibly use.
        """
        pass


    async def auth_async(self, rpc_name: str, rpc_auth: str, rpc_args: dict) -> dict:
        """
        Async virtual method used to authentica RPC calls against some sort token/user credentials.

        This call should raise an exception if the authentication fails.

        :param rpc_name: (string) The rpc call name.
        :param rpc_auth: (string) The rpc authentication method, sort of a factory string.
        :param rpc_args: (dict) The rpc args in a dictionary.
        :return: (dict) A auth data object for the server impl to possibly use.
        """
        pass
