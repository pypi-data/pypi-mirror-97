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

import sqlparse

from mettle.lib import xMettle

from .sqlvar import SqlVar


class Statement:
    """
    An abstract object that stores a SQL statements state.
    """

    STMNT_TYPE_NA   = 0
    STMNT_TYPE_READ = 1
    STMNT_TYPE_CUD  = 2  # Create, Update, Delete


    def __init__(self, name, stmnt_type = 0):
        """
        Contructor.
        """
        self.initialize()
        self.name = name
        self.stmnt_type = stmnt_type


    def __del__(self):
        self.destroy()


    def initialize(self):
        """
        Initializes the members for use.
        """
        self.name       = ''
        self.result     = []
        self.columns    = []
        self._sql       = ''
        self._in_vars   = {}
        self._out_vars  = []


    def destroy(self):
        """
        Free's all handles.
        """
        pass


    def free(self):
        """
        Same as destroy().
        """
        self.destroy()


    def bind_in(self, name: str, val, val_type = None, size: int = 0):
        """
        Bind a query input variable.

        :param name: Name of the parameter being bound.
        :param val: The object that is being bound.
        :param val_type: Optional value override type
        :param size: The size of the object, ie 4/8 for integers or string lengths.
        """
        self._in_vars[name] = SqlVar(name, val, val_type, size)


    def bind_out(self, name: str, val_type = None, size: int = 0):
        """
        Bind a query output variable.

        :param name: Name of the parameter being bound.
        :param val_type: Optional value override type
        :param size: The size of the object, ie 4/8 for integers or string lengths.
        """
        self._out_vars.append(SqlVar(name, None, val_type, size))


    def sql(self, sql_stmnt: str):
        """
        Sets the sequel statement.

        :param sql_stmnt: The sql statement.
        """
        self._sql = sql_stmnt


    def dynamic(self, dynId: str, dynVal: str):
        """
        Dyanimcally inject sql into the statement.

        :param dynId: The injection id to search replace for.
        :param dynVal: The sql to inject."""
        self._sql = self._sql.replace(dynId, dynVal)


    def get_stmnt_type(self) -> int:
        """
        Gets the expected statement type.

        :return: The statement type.
        """
        return self.stmnt_type


    def prepare_for_exec(self) -> int:
        """
        Run an cleanup checks on the sql before execution. This should also set the
        statement type if it has not been set arleady.

        :return: The statement type.
        """
        self._sql = self._sql.strip()

        if self.stmnt_type != self.STMNT_TYPE_NA:
            return self.stmnt_type

        sp = sqlparse.parse(self._sql)

        if sp:
            if sp[0].get_type() == "SELECT":
                self.stmnt_type = self.STMNT_TYPE_READ
            else:
                self.stmnt_type = self.STMNT_TYPE_CUD

        return self.stmnt_type


    def sql_subst(self, subst_func: callable) -> str:
        """
        Perform SQL parameter subsitution on the sql for different drivers or databases that
        use different syntax to the `:var` ...eg to %(var)s or %1.

        :param subst_func: The delegate function that will do the actual subsitution. Expected
                            parameters are `subst_func(idx: int, name: str, var) -> str:`.
        :returns: The substitutded string.
        """
        if not self._in_vars:
            return

        in_comment_multi  = False
        in_comment_single = False
        in_string         = False
        arg_idx           = 1
        pos               = 0
        max_len           = len(self._sql)

        while pos < max_len:
            if in_comment_multi:
                if self._sql[pos:pos + 2] == '*/':
                    in_comment_multi = False
                    pos += 2
                    continue
                pos += 1
                continue

            if in_comment_single:
                if self._sql[pos] == '\n':
                    in_comment_single = False
                pos += 1
                continue

            if in_string:
                if self._sql[pos] == '\\':
                    pos += 1
                elif self._sql[pos] == '\'':
                    in_string = False

                pos += 1
                continue

            if self._sql[pos] == "'":
                in_string = True
                pos += 1
                continue

            if self._sql[pos:pos + 2] == '--':
                in_comment_single = True
                pos += 2
                continue

            if self._sql[pos:pos + 2] == '/*':
                in_comment_multi = True
                pos += 2
                continue

            if self._sql[pos] != ':':
                pos += 1
                continue

            if self._sql[pos:pos + 2] == '::':
                pos += 2
                continue

            pos  += 1
            epos = pos + 1

            while epos <= max_len:
                if not self._sql[pos:epos].isidentifier():
                    break

                epos += 1

            epos -= 1

            if epos <= pos:
                raise xMettle('Statement.sql_subst() - Missing identifier - SQL: %s' % (self._sql))

            ident = self._sql[pos:epos]
            var   = self._in_vars.get(ident)

            if not var:
                raise xMettle('Statement.sql_subst() - Unknown identifier [%s] - SQL: %s' % (ident, self._sql))

            repl = subst_func(arg_idx, ident, var)

            self._sql = self._sql[:pos - 1] + repl + self._sql[epos:]
            pos      += len(repl)
            max_len   = len(self._sql)
            arg_idx  += 1

        return self._sql
