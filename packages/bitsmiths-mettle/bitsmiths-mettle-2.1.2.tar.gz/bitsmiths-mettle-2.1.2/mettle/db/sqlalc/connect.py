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

# NOTE, this connector assumes you have the following pips installed: sqlalchemy

import datetime
import json
import uuid

from mettle.db.iconnect import IConnect
from mettle.db.sqlvar   import SqlVar

from .statement import Statement


class Connect(IConnect):
    """
    Python sql alchemy conneciton mettle overload.
    """

    def __init__(self, dbs):
        self._dbs = dbs  # database sql alchmey session


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        self.close()


    def __del__(self):
        self.close()


    def fetch(self, stmnt: Statement):

        if stmnt._fetch_chunk is None or stmnt._fetch_idx >= len(stmnt._fetch_chunk):
            stmnt._fetch_chunk = stmnt._curr.fetchmany(10_000)
            stmnt._fetch_idx = 0

            if not stmnt._fetch_chunk:
                return False

            if not stmnt.columns:
                self._bind_output(stmnt, stmnt._fetch_chunk[0])

        idx = 0
        row = stmnt._fetch_chunk[stmnt._fetch_idx]

        for val in row:
            svar = stmnt._out_vars[idx]

            if svar.val_type == str:
                if val is None:
                    val = ''
            elif val is None or svar.val_type is None:
                pass
            elif svar.val_type == float:
                if type(val) != float:
                    val = float(val)
            elif svar.val_type == bytes or svar.val_type == bytearray:
                if type(val) == bytearray or type(val) != bytes:
                    val = bytes(val)

            svar.is_null             = True
            stmnt._out_vars[idx].val = val
            stmnt.result[idx]        = val

            idx += 1

        stmnt._fetch_idx += 1

        return True


    def commit(self):
        if self._dbs:
            self._dbs.commit()


    def rollback(self):
        if self._dbs:
            self._dbs.rollback()


    def connect_deft(self, user: str, passwd: str, db_name: str, host: str, port: int = 0, schema: str = None):
        raise Exception('Not supported - Use constructor for Sql Alchmey database connections')


    def connect(self, connection_str: str):
        raise Exception('Not supported - Use constructor for Sql Alchmey database connections')


    def close(self):
        if self._dbs:
            self._dbs.close()
            self._dbs = None


    def execute(self, stmnt):
        in_params = self._bind_input(stmnt)

        try:
            stmnt._sql = stmnt._sql.strip()
            stmnt._curr = self._dbs.execute(stmnt._sql, in_params)

        except Exception:
            raise
            # raise Exception('Sql Error (%s): [%s]' % (str(x), stmnt._sql))

        return self


    def pre_get_sequence(self, stmnt: Statement, table: str, col: str, size: int) -> int:
        raise Exception('Sql Alchemy connector does not allocate sequences pre-insert!')


    def post_get_sequence(self, stmnt: Statement, table: str, col: str, size: int) -> int:
        raise Exception('Sql Alchemy connector does not allocate sequences post-insert!')


    def get_timestamp(self) -> datetime.datetime:
        return datetime.datetime.now()


    def lock(stmnt: Statement = None):
        pass


    def statement(self, name: str, stmnt_type: int = 0):
        return Statement(name, stmnt_type)


    def name(self):
        return 'Sql Alchemy'


    def date_4_sql_inject(self, src_date: datetime.date):
        if not src_date or src_date == datetime.date.min or src_date == datetime.datetime.min:
            return 'NULL'

        return "date('%s')" % src_date.strftime('%Y-%m-%d')


    def datetime_4_sql_inject(self, src_datetime: datetime.datetime):
        if not src_datetime or src_datetime == datetime.date.min or src_datetime == datetime.datetime.min:
            return 'NULL'

        return "datetime('%s')" % src_datetime.strftime('%Y-%m-%d %H:%M:%S')



    def transaction_mode_get(self) -> bool:
        return self._dbs.connection().connection.get_isolation_level() == 1


    def transaction_mode_set(self, mode: bool):
        if mode:
            self._dbs.connection().connection.set_isolation_level(1)
        else:
            self._dbs.connection().connection.set_isolation_level(0)


    def _bind_input(self, stmnt: Statement) -> dict:
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
        if not stmnt._curr.keys():
            raise Exception('Statement has no output descriptor! Sql: %s' % stmnt._sql)

        if len(row) != len(stmnt._curr.keys()):
            raise Exception('Statement descriptor and return row count mismatch! Sql: %s' % stmnt._sql)

        if stmnt._out_vars:
            if len(stmnt._out_vars) != len(stmnt._curr.keys()):
                raise Exception('Predefined statement output vars length [%d] mismatch to actual cursor description'
                                ' length [%d]. Sql: %s' % (len(stmnt._out_vars), len(stmnt._curr.keys()), stmnt._sql))

            for x in stmnt._out_vars:
                stmnt.columns.append(x.name)
                stmnt.result.append(None)

            return

        for colName in stmnt._curr.keys():
            stmnt._out_vars.append(SqlVar(colName, val=None))
            stmnt.columns.append(colName)
            stmnt.result.append(None)
