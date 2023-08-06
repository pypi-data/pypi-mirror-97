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

import sqlite3
import datetime
import json
import uuid

from mettle.db import IConnect
from mettle.db import SqlVar

from .statement import Statement


class Connect(IConnect):
    """
    Python sqlite3 conneciton mettle overload.
    """

    def __init__(self):
        self._conn = None


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        self.close()


    def __del__(self):
        self.close()


    def commit(self):
        if self._conn.in_transaction:
            self._conn.commit()


    def rollback(self):
        if self._conn.in_transaction:
            self._conn.rollback()


    def fetch(self, stmnt: Statement) -> bool:
        row = stmnt._curr.fetchone()

        if not row:
            return False

        if len(stmnt.columns) == 0:
            self._bind_output(stmnt, row)

        idx    = 0
        outLen = len(row)

        while idx < outLen:
            val  = row[idx]
            svar = stmnt._out_vars[idx]

            if svar.val_type == str:
                if val is None:
                    val = ''
            elif val is None or svar.val_type is None:
                pass
            elif svar.val_type == datetime.datetime:
                if val and len(val) == 19:
                    val = datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                else:
                    val = None
            elif svar.val_type == datetime.date:
                if val and len(val) == 10:
                    val = datetime.datetime.strptime(val, '%Y-%m-%d').date()
                else:
                    val = None
            elif svar.val_type == datetime.time:
                if val and len(val) == 8:
                    val = datetime.datetime.strptime(val, '%H:%M:%S').time()
                else:
                    val = None
            elif svar.val_type == bool:
                val = bool(val)
            elif svar.val_type == dict:
                val = json.loads(val)
            elif svar.val_type == uuid.UUID:
                val = uuid.UUID(val)

            svar.is_null             = val is None
            stmnt._out_vars[idx].val = val
            stmnt.result[idx]        = val

            idx += 1

        return True


    def connect_deft(self, user: str, passwd: str, db_name: str, host: str, port: int = 0, schema: str = None):
        self.connect(db_name)


    def connect(self, connection_str: str):
        self.close()
        self._conn = sqlite3.connect(connection_str)


    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


    def execute(self, stmnt) -> "Connect":
        in_tuple = self._bind_input(stmnt)

        try:
            stmnt._sql = stmnt._sql.strip()
            stmnt._curr.execute(stmnt._sql, in_tuple)
        except sqlite3.OperationalError as x:
            raise Exception('Sql Error (%s): [%s]' % (str(x), stmnt._sql))

        return self


    def pre_get_sequence(self, stmnt, table, col, size) -> int:
        raise Exception('Sqlite databases do not allocate sequences pre-insert!')


    def post_get_sequence(self, stmnt, table, col, size) -> int:
        return stmnt._curr.lastrowid


    def get_timestamp(self) -> datetime.datetime:
        return datetime.datetime.now()


    def lock(self, stmnt: Statement = None):
        pass  # note, sqlite never requires locks because only one connection is active at a time.


    def statement(self, name: str, stmnt_type: int = 0) -> Statement:
        return Statement(name, self._conn.cursor(), stmnt_type)


    def name(self) -> str:
        return 'SQLite3 (Python Native)'


    def date_4_sql_inject(self, srcDate: datetime.date) -> str:
        if not srcDate or srcDate == datetime.date.min or srcDate == datetime.datetime.min:
            return 'NULL'

        return "date('%s')" % srcDate.strftime('%Y-%m-%d')


    def datetime_4_sql_inject(self, srcDateTime: datetime.datetime) -> str:
        if not srcDateTime or srcDateTime == datetime.date.min or srcDateTime == datetime.datetime.min:
            return 'NULL'

        return "datetime('%s')" % srcDateTime.strftime('%Y-%m-%d %H:%M:%S')


    def transaction_mode_get(self) -> bool:
        return False


    def transaction_mode_set(self, mode: bool):
        pass


    def _bind_input(self, stmnt) -> dict:
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

            if val.val_type == datetime.date and (type(val.val) == datetime.date or type(val.val) == datetime.datetime):
                in_params[key] = val.val.strftime('%Y-%m-%d')
                continue

            if val.val_type == datetime.datetime and (type(val.val) == datetime.datetime or type(val.val) == datetime.date):
                in_params[key] = val.val.strftime('%Y-%m-%d %H:%M:%S')
                continue

            if val.val_type == datetime.time and (type(val.val) == datetime.time or type(val.val) == datetime.datetime):
                in_params[key] = val.val.strftime('%H:%M:%S')
                continue

            if val.val_type == dict:
                if not val.val:
                    in_params[key] = None
                elif type(val.val) == str:
                    in_params[key] = val.val
                else:
                    in_params[key] = json.dumps(val.val)
                continue

            if val.val_type == uuid.UUID:
                in_params[key] = str(val.val)
                continue

            in_params[key] = val.val

        return in_params


    def _bind_output(self, stmnt, row):
        if not stmnt._curr.description:
            raise Exception('Statement has no output descriptor! Sql: %s' % stmnt._sql)

        if len(row) != len(stmnt._curr.description):
            raise Exception('Statement descriptor and return row count mismatch! Sql: %s' % stmnt._sql)

        if stmnt._out_vars:
            if len(stmnt._out_vars) != len(stmnt._curr.description):
                raise Exception('Pre-defined statement output vars length [%d] mismatch to actual cursor'
                                ' description length [%d]. Sql: %s' % (
                                    len(stmnt._out_vars), len(stmnt._curr.description), stmnt._sql))

            for x in stmnt._out_vars:
                stmnt.columns.append(x.name)
                stmnt.result.append(None)

            return

        for idx in range(len(stmnt._curr.description)):
            x = stmnt._curr.description[idx]
            stmnt._out_vars.append(SqlVar(x[0], val=None, val_type=type(row[idx])))
            stmnt.columns.append(x[0])
            stmnt.result.append(None)
