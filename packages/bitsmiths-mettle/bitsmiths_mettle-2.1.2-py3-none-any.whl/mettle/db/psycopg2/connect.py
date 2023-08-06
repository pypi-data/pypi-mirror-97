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

import datetime
import json
import psycopg2
import psycopg2.extras
import psycopg2.errors
import uuid

from mettle.lib.xmettle import xMettle

from mettle.db import IConnect
from mettle.db import SqlVar

from .statement import Statement

"""
Initialize psycopg2 with our required extensions.
"""
psycopg2.extras.register_uuid()

DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)

BYTEA2BYTES = psycopg2.extensions.new_type(
    psycopg2.BINARY.values,
    'BYTEA2BYTES',
    lambda value, curs: psycopg2.BINARY(value, curs).tobytes() if value is not None else None)

psycopg2.extensions.register_type(DEC2FLOAT)
psycopg2.extensions.register_type(BYTEA2BYTES)


class Connect(IConnect):
    """
    Python pyscopg2 connection mettle overload.
    """

    def __init__(self):
        self._conn = None


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        self.close()


    def __del__(self):
        self.close()


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

            svar.is_null = val is None

            if svar.is_null and svar.val_type == str:
                stmnt._out_vars[idx].val = ''
                stmnt.result[idx]        = ''
            else:
                stmnt._out_vars[idx].val = val
                stmnt.result[idx]        = val

            idx += 1

        return True


    def connect_deft(self, user: str, passwd: str, db_name: str, host: str, port: int = 0, schema: str = None):
        self.close()

        conn_args = {
            'async'    : False,
            'dbname'   : db_name,
        }

        if user:
            conn_args['user'] = user

        if passwd:
            conn_args['password'] = passwd

        if host:
            conn_args['host'] = host

        if port:
            conn_args['port'] = str(port)

        self._conn = psycopg2.connect(**conn_args)
        self.transaction_mode_set(True)


    def connect(self, connection_str: str):
        """
        Assumes a standard postgres url connection string.

        eg postgresql://mettle:dev@127.0.0.1:5432/mettle
        == driver://user:password@host:port/database
        """
        user      = None
        passwd    = None
        db_name   = None
        host      = None
        port      = 0
        expected  = 'driver://user:password@host:port/database_name'
        parts     = connection_str.strip().split('//')

        if len(parts) != 2:
            raise Exception(f'Connection string not in expected format: {expected}')

        parts = parts[1].split('/')

        if len(parts) == 1:
            db_name = parts[0]
        elif len(parts) == 2:
            db_name = parts[1]
            parts   = parts[0].split('@')

            if len(parts) > 2:
                raise Exception(f'Connection string not in expected format: {expected}')

            uparts = parts[0].split(':')

            if len(uparts) > 2:
                raise Exception(f'Connection string not in expected format: {expected}')

            user = uparts[0]

            if len(uparts) == 2:
                passwd = uparts[1]

            if len(parts) == 2:
                hparts = parts[1].split(':')

                if len(hparts) > 2:
                    raise Exception(f'Connection string not in expected format: {expected}')

                host = hparts[0]

                if len(hparts) == 2:
                    if not hparts[1].isdigit():
                        raise Exception(f'Connection string not in expected format: {expected}')

                    port = int(hparts[1])
        else:
            raise Exception(f'Connection string not in expected format: {expected}')

        self.connect_deft(user, passwd, db_name, host, port)


    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


    @staticmethod
    def _psyco_repl(idx: int, name: str, var: object = None):
        return f'%({name})s'


    def execute(self, stmnt: Statement):
        in_params = self._bind_input(stmnt)

        try:
            stmnt.sql_subst(Connect._psyco_repl)
            stmnt._curr.execute(stmnt._sql, in_params)
        except psycopg2.errors.LockNotAvailable as x:
            self._handle_rollback(stmnt)
            raise xMettle('Sql Lock Error - %s' % str(x), self.name(), xMettle.eCode.DBLockNoWaitFailed)

        except psycopg2.errors.IntegrityConstraintViolation as x:
            self._handle_rollback(stmnt)
            raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBPrimaryKeyViolation)

        except psycopg2.errors.ForeignKeyViolation as x:
            self._handle_rollback(stmnt)
            raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBForeignKeyViolation)

        except psycopg2.errors.UniqueViolation as x:
            self._handle_rollback(stmnt)
            raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBUniqueKeyViolation)

        except Exception as x:
            self._handle_rollback(stmnt)
            raise xMettle('Sql Error - %s' % (str(x)), self.name(), xMettle.eCode.DBStandardError)

        return self


    def pre_get_sequence(self, stmnt, table, col, size) -> int:
        raise Exception('Sqlite databases do not allocate sequences pre-insert!')


    def post_get_sequence(self, stmnt, table: str, col: str, size: int) -> int:
        with self._conn.cursor() as cur:
            cur.execute("SELECT currval('%s_%s_seq')" % (table, col))
            res = cur.fetchone()

            if not res:
                raise xMettle('postGetSequence(table:%s, col:%s) - No rows returned' % (table, col),
                              src=self.name(),
                              errCode=xMettle.eCode.DBStandardError)

            return res[0]


    def get_timestamp(self) -> datetime.datetime:
        return datetime.datetime.now()


    def lock(self, stmnt: Statement = None):
        stmnt._curr.execute("SAVEPOINT _MX")


    def name(self) -> str:
        return 'Psycopg2 PostgreSQL'


    def date_4_sql_inject(self, srcDate: datetime.date) -> str:
        if not srcDate or srcDate == datetime.date.min or srcDate == datetime.datetime.min:
            return 'NULL'

        return "date('%s')" % srcDate.strftime('%Y-%m-%d')


    def datetime_4_sql_inject(self, srcDateTime: datetime.datetime) -> str:
        if not srcDateTime or srcDateTime == datetime.date.min or srcDateTime == datetime.datetime.min:
            return 'NULL'

        return "datetime('%s')" % srcDateTime.strftime('%Y-%m-%d %H:%M:%S')


    def statement(self, name: str, stmnt_type: int = 0) -> Statement:
        stmnt = Statement(self._conn.cursor(), name, stmnt_type)

        if self._conn.get_transaction_status() == 0:
            stmnt._curr.execute("BEGIN TRANSACTION")
            stmnt._curr.execute("SAVEPOINT _MX")

        return stmnt


    def commit(self):
        if self._conn and self._conn.get_transaction_status() != 0:
            self._conn.commit()


    def rollback(self):
        if self._conn and self._conn.get_transaction_status() != 0:
            self._conn.rollback()


    def _handle_rollback(self, stmnt: Statement):
        if self._conn.get_transaction_status() != 0:
            stmnt._curr.execute("ROLLBACK TO _MX")
            stmnt._curr.execute("SAVEPOINT _MX")


    def transaction_mode_get(self) -> bool:
        return not self._conn.auto_commit


    def transaction_mode_set(self, mode: bool):
        if self._conn.get_transaction_status() != 0:
            raise xMettle("Cannot toggle transaction mode while in a transaction, commit or rollback first.",
                          self.name(),
                          xMettle.eCode.DBStandardError)

        self._conn.set_isolation_level(1 if mode else 0)


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

            if val.val_type == dict or val.val_type == list:
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

        if not in_params:
            return None

        return in_params


    def _bind_output(self, stmnt: Statement, row: tuple) -> None:
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



    def backend_pid(self) -> int:
        return self._conn.info.backend_pid
