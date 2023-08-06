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

# NOTE, this connector assumes you have the following pips installed: psycopg2, sqlalchemy


import psycopg2.errors
import sqlalchemy.exc

from mettle.lib.xmettle import xMettle

from .connect   import Connect
from .statement import Statement


class ConnectPostgres(Connect):
    """
    Specfic postgres overload for the the connector.

    Note, expected db engine options are:

    options = {
        'pool_recycle' : 3600,
        'pool_size'    : 10,
        'pool_timeout' : 30,
        'max_overflow' : 30,
        'echo'         : False,
        'execution_options': {
            'autocommit'       : False,
            'autoflush'        : False,
            'expire_on_commit' : False,
            'stream_results'   : False,
        }
    }
    """

    def __init__(self, dbs):
        Connect.__init__(self, dbs)
        self._in_transaction = False


    def name(self):
        return 'Sql Alchemy [PostgreSQL]'


    def execute(self, stmnt: Statement):
        in_params = self._bind_input(stmnt)

        try:
            stmnt._sql = stmnt._sql.strip()
            stmnt._curr = self._dbs.execute(stmnt._sql, in_params)

        except sqlalchemy.exc.SQLAlchemyError as x:
            self._handle_rollback()

            if isinstance(x.orig, psycopg2.errors.LockNotAvailable):
                raise xMettle('Sql Lock Error - %s' % str(x), self.name(), xMettle.eCode.DBLockNoWaitFailed)

            if isinstance(x.orig, psycopg2.errors.IntegrityError):
                raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBPrimaryKeyViolation)

            if isinstance(x.orig, psycopg2.errors.ForeignKeyViolation):
                raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBForeignKeyViolation)

            if isinstance(x.orig, psycopg2.errors.UniqueViolation):
                raise xMettle('Sql Error - %s' % str(x), self.name(), xMettle.eCode.DBUniqueKeyViolation)

            raise xMettle('Sql Error - %s' % (str(x)), self.name(), xMettle.eCode.DBStandardError)

        except Exception as x:
            self._handle_rollback()
            raise xMettle('Sql Error - %s' % (str(x)), self.name(), xMettle.eCode.DBStandardError)

        return self


    def lock(self, stmnt: Statement = None):
        self._dbs.execute("SAVEPOINT _MX")


    def statement(self, name: str, stmnt_type: int = 0):
        if not self._in_transaction:
            self._dbs.execute("BEGIN TRANSACTION")
            self._dbs.execute("SAVEPOINT _MX")
            self._in_transaction = True

        return Statement(name, stmnt_type)


    def commit(self):
        if self._dbs and self._in_transaction:
            self._dbs.execute('COMMIT')
            self._in_transaction = False


    def rollback(self):
        if self._dbs:
            self._dbs.execute('ROLLBACK')
            self._in_transaction = False


    def post_get_sequence(self, stmnt, table: str, col: str, size: int) -> int:
        res = self._dbs.execute("SELECT currval('%s_%s_seq')" % (table, col)).fetchone()

        if not res:
            raise xMettle('postGetSequence(table:%s, col:%s) - No rows returned' % (table, col),
                          src=self.name(),
                          errCode=xMettle.eCode.DBStandardError)

        return res[0]


    def _handle_rollback(self):
        if self._in_transaction:
            self._dbs.execute("ROLLBACK TO _MX")
            self._dbs.execute("SAVEPOINT _MX")
