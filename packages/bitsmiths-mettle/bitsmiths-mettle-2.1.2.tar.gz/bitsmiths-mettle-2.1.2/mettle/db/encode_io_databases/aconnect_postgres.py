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

# NOTE, this connector assumes you have the following pips installed: sqlparse, asyncpg, databases[postgres]

import asyncpg.exceptions

from mettle.lib.xmettle import xMettle

from .aconnect  import AConnect
from .statement import Statement


class AConnectPostgres(AConnect):
    """
    Specfic postgres overload for the the connector.
    """

    def __init__(self, conn):
        AConnect.__init__(self, conn)


    def name(self):
        return 'encode.io/databases[postgres]'


    async def execute(self, stmnt: Statement):
        in_params = self._bind_input(stmnt)

        try:
            if stmnt.prepare_for_exec() == Statement.STMNT_TYPE_READ:
                stmnt._fres = await self._conn.fetch_all(stmnt._sql, in_params)

                if stmnt._fres:
                    self._bind_output(stmnt, stmnt._fres[0])
            else:
                await self._conn.execute(stmnt._sql, in_params)

        except asyncpg.exceptions.LockNotAvailableError as x:
            await self._handle_rollback()
            raise xMettle('Sql Lock Error - %s' % str(x), self.name(), xMettle.eCode.DBLockNoWaitFailed)

        except asyncpg.exceptions.IntegrityConstraintViolationError as x:
            await self._handle_rollback()
            raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBPrimaryKeyViolation)

        except asyncpg.exceptions.ForeignKeyViolationError as x:
            await self._handle_rollback()
            raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBForeignKeyViolation)

        except asyncpg.exceptions.UniqueViolationError as x:
            await self._handle_rollback()
            raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBUniqueKeyViolation)

        except Exception as x:
            await self._handle_rollback()
            raise xMettle('Sql Error - %s' % (str(x)), self.name(), xMettle.eCode.DBStandardError)

        return self


    async def lock(self, stmnt: Statement = None):
        await self._conn.execute("SAVEPOINT _MX")


    async def statement(self, name: str, stmnt_type: int = 0) -> Statement:
        if self._tran_mode:
            if not self._in_transaction:
                await self._conn.execute("BEGIN TRANSACTION")
                await self._conn.execute("SAVEPOINT _MX")
                self._in_transaction = True

        return Statement(name, stmnt_type)


    async def post_get_sequence(self, stmnt, table: str, col: str, size: int) -> int:
        res = await self._conn.fetch_one("SELECT currval('%s_%s_seq') as val" % (table, col))

        if not res:
            raise xMettle('post_get_sequence(table:%s, col:%s) - No rows returned' % (table, col),
                          self.name(),
                          xMettle.eCode.DBStandardError)

        return res['val']


    async def _handle_rollback(self):
        if self._in_transaction:
            await self._conn.execute("ROLLBACK TO _MX")
            await self._conn.execute("SAVEPOINT _MX")
