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

# NOTE, this connector assumes you have the following pips installed: sqlparse, (databases[sqlite] or databases[postgres])
# -- see reference website https://www.encode.io/databases/

import datetime
import json
import uuid

from databases.core import Connection

from mettle.lib.xmettle import xMettle

from mettle.db.iaconnect import IAConnect
from mettle.db.sqlvar   import SqlVar

from .statement import Statement


class AConnect(IAConnect):
    """
    Base mettle overload connector for encode.io/databases.
    """

    def __init__(self, conn: Connection):
        self._conn = conn  # A databases connection object, expected to already be acquired
        self._in_transaction = False
        self._tran_mode = True


    def name(self):
        return 'encode.io/databases[_base_]'


    async def fetch(self, stmnt: Statement) -> False:
        if stmnt._fres is None:
            raise xMettle('Statement [%s] has no results.' % (stmnt.name), self.name(), xMettle.eCode.DBStandardError)

        if stmnt._fidx >= len(stmnt._fres):
            return False

        idx = 0
        row = stmnt._fres[stmnt._fidx]

        for val in row.values():
            svar = stmnt._out_vars[idx]

            if svar.val_type is None or svar.val_type is None:
                pass
            elif svar.val_type == str:
                if not val:
                    val         = ''
            elif svar.val_type == float:
                if type(val) != float:
                    val = float(val)
            elif svar.val_type == dict:
                if val:
                    val = json.loads(val)
            elif svar.val_type == bytes:
                if type(val) != bytes:
                    val = bytes(val)

            svar.is_null             = val is None
            stmnt._out_vars[idx].val = val
            stmnt.result[idx]        = val

            idx += 1

        stmnt._fidx += 1

        return True


    async def commit(self):
        if self._in_transaction:
            await self._conn.execute("COMMIT")
            self._in_transaction = False


    async def rollback(self):
        if self._in_transaction:
            await self._conn.execute("ROLLBACK")
            self._in_transaction = False


    async def execute(self, stmnt):
        in_params = self._bindInput(stmnt)

        try:
            if stmnt.prepare_for_exec() == Statement.STMNT_TYPE_READ:
                stmnt._fres = await self._conn.fetch_all(stmnt._sql, in_params)

                if stmnt._fres:
                    self._bindOutput(stmnt, stmnt._fres[0])
            else:
                await self._conn.execute(stmnt._sql, in_params)

        except Exception as x:
            raise Exception('Sql Error (%s): [%s]' % (str(x), stmnt._sql))

        return self


    async def pre_get_sequence(self, stmnt, table, col, size):
        raise Exception('ecode/databases connector does not allocate sequences pre-insert!')


    async def post_get_sequence(self, stmnt, table, col, size):
        raise Exception('ecode/databases connector does not allocate sequences post-insert!')


    async def get_timestamp(self) -> datetime.datetime:
        return datetime.datetime.now()


    async def lock(self, stmnt: Statement = None):
        pass


    async def statement(self, name: str, stmnt_type: int = 0):
        return Statement(name, stmnt_type)


    def date_4_sql_inject(self, src_date: datetime.date):
        if not src_date or src_date == datetime.date.min or src_date == datetime.datetime.min:
            return 'NULL'

        return "date('%s')" % src_date.strftime('%Y-%m-%d')


    def datetime_4_sql_inject(self, src_datetime: datetime.datetime):
        if not src_datetime or src_datetime == datetime.date.min or src_datetime == datetime.datetime.min:
            return 'NULL'

        return "datetime('%s')" % src_datetime.strftime('%Y-%m-%d %H:%M:%S')


    def transactionModeGet(self) -> bool:
        return self._tran_mode


    def transactionModeSet(self, mode: bool):
        if self._tran_mode == mode:
            return

        if self._in_transaction:
            raise xMettle("Cannot toggle transaction mode while in a transaction, commit or rollback first.",
                          self.name(),
                          xMettle.eCode.DBStandardError)

        self._tran_mode = mode


    def _bind_input(self, stmnt):
        in_params = {}

        for key, val in stmnt._in_vars.items():
            if val.is_null or val.val is None:
                in_params[key] = None
                continue

            if val.val_type == int or val.val_type == float:
                in_params[key] = val.val
                continue

            if (val.val_type == str               and not val.val) or\
               (val.val_type == datetime.date     and val.val == datetime.date.min) or\
               (val.val_type == datetime.datetime and val.val == datetime.datetime.min) or\
               (val.val_type == uuid.UUID         and not val.val) or\
               (val.val_type == bytes             and not val.val):
                in_params[key] = None
                continue

            elif val.val_type == dict or val.val_type == list:
                if not val.val:
                    in_params[key] = None
                elif type(val.val) == str:
                    in_params[key] = val.val
                else:
                    in_params[key] = json.dumps(val.val)
                continue

            in_params[key] = val.val

        return in_params


    def _bind_output(self, stmnt: Statement, row):
        """
        Bind the output columns.

        :param stmnt: The statement.
        :param row: The row result.
        """
        if not row:
            raise Exception('Statement has no output! Sql: %s' % stmnt._sql)

        if stmnt._out_vars:
            if len(stmnt._out_vars) != len(row):
                raise Exception('Predefined statement output vars length [%d] mismatch to actual'
                                ' cursor description length [%d]. Sql: %s' % (len(stmnt._out_vars), len(row), stmnt._sql))

            for colName in row.keys():
                stmnt.columns.append(colName)
                stmnt.result.append(None)

            return

        for colName in row.keys():
            stmnt._out_vars.append(SqlVar(colName, val=None))
            stmnt.columns.append(colName)
            stmnt.result.append(None)
