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

import os.path
import logging
import time

from .generator import Generator


class GenSql(Generator):

    DAO_MODES = ('inline', 'stored-proc')

    def __init__(self):
        Generator.__init__(self, ['sql', 'drop', 'table', 'constraint', 'index'])
        self.targ_type  = 'sqldef'
        self._gen_info  = {}
        self._init_code_options({
            'db.user'     : None,
            'db.password' : None,
            'db.schema'   : None,
            'db.server'   : None
        })


    def name(self):
        return 'Sql'


    def stored_proc_support(self):
        return False


    def generate_tables(self, gen_info: dict):
        pass


    def generate_daos(self, gen_info: dict, target_db: str):
        if gen_info['clean']:
            self.clean(gen_info, target_db)

            sp_dir = self.get_option('sp.path', False, True)

            if sp_dir != '':
                self.clean(gen_info, os.path.join(target_db, sp_dir))

            return

        self._gen_info = gen_info
        self._schema  = None

        sql_file   = self.filename_and_path(gen_info, gen_info['table'].name, 'sql',        target_db)
        drop_file  = self.filename_and_path(gen_info, gen_info['table'].name, 'drop',       target_db)
        table_file = self.filename_and_path(gen_info, gen_info['table'].name, 'table',      target_db)
        cons_file  = self.filename_and_path(gen_info, gen_info['table'].name, 'constraint', target_db)
        index_file = self.filename_and_path(gen_info, gen_info['table'].name, 'index',      target_db)

        logging.info('Gen: %s' % sql_file)
        logging.info('Gen: %s' % drop_file)
        logging.info('Gen: %s' % table_file)
        logging.info('Gen: %s' % cons_file)
        logging.info('Gen: %s' % index_file)

        self._sqlfh   = open(sql_file, 'wt')
        self._dropfh  = open(drop_file, 'wt')
        self._tablefh = open(table_file, 'wt')
        self._consfh  = open(cons_file, 'wt')
        self._indexfh = open(index_file, 'wt')

        self._gen_message()
        self._gen_header()

        self._tableName = self._gen_table_name()

        self._gen_create_table()
        self._gen_sequences()
        self._gen_constraints()
        self._gen_primary_key()
        self._gen_foreign_keys()
        self._gen_unique_keys()
        self._gen_indexes()
        self._gen_stored_procs()
        self._gen_trailer()

        self._sqlfh.close()
        self._dropfh.close()
        self._tablefh.close()
        self._consfh.close()
        self._indexfh.close()

        if self.stored_proc_support() and self._gen_info['database'].stored_proc_support():
            self._generate_stored_procs(target_db)

        self._schema  = None

        del self._tableName
        del self._sqlfh
        del self._dropfh
        del self._tablefh
        del self._consfh
        del self._indexfh

        del self._gen_info


    def _all_file_handles(self) -> list:
        return [ self._sqlfh, self._dropfh, self._tablefh, self._consfh, self._indexfh ]


    def _gen_message(self):
        self._sqlfh.write('REMARK This (%s) file was generated by mettle.genes.db.GenSql on %s\n\n' % (
            self.name, time.asctime()))


    def _gen_header(self):
        pass


    def _gen_ref_table_name(self, tbl):
        if tbl.count('.') > 0:
            return tbl

        if self._schema is None:
            self._schema = self.get_option('db.schema', blank_ok = True)

        if self._schema != '':
            return '%s.%s' % (self._schema, tbl)

        return tbl

    def _gen_table_name(self):
        if not self._schema:
            self._schema = self.get_option('db.schema', blank_ok = True)

        if self._schema:
            return '%s.%s' % (self._schema, self._gen_info['table'].name)

        return self._gen_info['table'].name


    def _gen_create_table(self):
        pass


    def _gen_sequences(self):
        pass


    def _gen_constraints(self):
        pass


    def _gen_primary_key(self):
        pass


    def _gen_foreign_keys(self):
        pass


    def _gen_unique_keys(self):
        pass


    def _gen_indexes(self):
        pass


    def _gen_stored_procs(self):
        pass


    def _gen_trailer(self):
        pass

    def _generate_stored_procs(self, target_db):
        from .database  import Database

        sp_dir    = self.get_option('sp.path', False, True)

        if sp_dir == '':
            sp_dir = target_db
        else:
            sp_dir = os.path.join(target_db, sp_dir)

        if self._gen_info['database'].daoMode == Database.DAO_MODE_STORED_PROC:
            stdProcs = self._build_standard_procs(self._gen_info)

            for proc in stdProcs:
                self._write_stored_proc(target_db, sp_dir, stdProcs[proc])

        for proc in self._gen_info['table'].procs:
            if proc.daoMode == 'inline':
                continue

            if proc.daoMode != Database.DAO_MODE_STORED_PROC:
                if self._gen_info['database'] != Database.DAO_MODE_STORED_PROC or proc.daoMode != '':
                    continue

            if self._check_for_type(proc.in_fields, 'dynamic'):
                raise Exception('A query cannot be a stored procedure and also have dynamic columns'
                                '(make the dao mode "inline")! [target_db:%s, table:%s, proc:%s]' % (
                                    target_db, self._gen_info['table'].name, proc.name))

            self._write_stored_proc(target_db, sp_dir, proc)


    def _write_stored_proc(self, target_db, sp_dir, proc):
        proc_name = self._stored_proc_name(proc)
        sqlFile  = self.filename_and_path(self._gen_info, proc_name, 'sql', sp_dir)

        schema = self.get_option('db.schema', blank_ok=True)
        sql    = proc.sql.get(target_db)

        if sql:
            sql = proc.sql['std']

        fh = open(sqlFile, 'wt')

        self._add_headers(fh)
        self._add_use_schema(fh, schema)
        sql = self._native_paramatalize_sql(sql, proc)
        self._add_stored_proc(fh, schema, proc_name, proc, sql)
        self._add_footers(fh)

        fh.close()


    def _add_headers(self, fh):
        fh.write('-- This file was generated by mettle.genes.db.GenSQL [ver %s] on %s\n\n' % (
            self._gen_info['version'], time.asctime()))


    def _add_footers(self, fh):
        pass


    def _add_use_schema(self, fh, schema: str):
        pass


    def _add_stored_proc(self, fh, schema: str, proc_name: str, proc: str, sql: str):
        pass


    def _native_paramatalize_sql(self, sql, proc):
        if len(proc.in_fields) < 1:
            return sql

        return self._input_param_replace(sql, proc)


    def _input_param_subst(self, bind_idx: int, bind_name: str):
        """
        Virtual method to replace the input bind name with the db specific syntax.

        :param bind_idx: The index of the binding parameter.
        :param bind_name: The name of the binding parameter.
        """
        return ":%s" % bind_name


    def _input_param_replace(self, sql, proc):
        """
        Replaces the parameters from the source sql.

        @param sql string : The input sql to replace.
        @return    string : The replaced sql.
        """
        res             = ''
        inCommentMulti  = False
        inCommentSingle = False
        inString        = ''
        e               = 0
        bdx             = 0
        bindName        = ''
        i               = -1

        while True:
            i += 1

            if i >= len(sql):
                break

            if inCommentMulti:
                if sql[i:i + 2] == '*/':
                    inCommentMulti = False
                    i += 1

                continue

            if inCommentSingle:
                if sql[i] == '\n':
                    inCommentSingle = False

                continue

            if inString != '':
                res += sql[i]

                if sql[i] == '\\':
                    i += 1
                elif sql[i] == inString:
                    inString = ''

                continue

            if sql[i:i + 2] == '--':
                inCommentSingle = True
                i += 1
                continue

            if sql[i] == '/' and sql[i + 1] == '*':
                inCommentMulti = True
                i += 1
                continue


            if sql[i] == '\'' or sql[i] == '"':
                res      += sql[i]
                inString  = sql[i]
                continue

            if sql[i] != ':':
                res += sql[i]
                continue

            if sql[i + 1] == ':':
                res += sql[i]
                i   += 1
                res += sql[i]
                continue

            e  = i
            i += 1

            while True:
                e += 1

                if e >= len(sql):
                    break

                if not self._is_varible_char(sql[e]):
                    break

            if e == i:
                raise Exception("_inputReplace() - Missing identifier [position:%d, sql: %s]" % (i, sql))

            bindName = sql[i:i + (e - i)]
            bdx      = -1
            ldx      = -1
            fnd      = False

            while True:
                bdx += 1
                ldx += 1

                if bdx >= len(proc.in_fields):
                    break

                if proc.in_fields[bdx].type == 'dbrec':
                    for lc in self._lookup_columns(proc.in_fields[bdx].lookup, ''):
                        lcn = '%s_%s' % (proc.in_fields[bdx].name, lc.name)
                        print(lcn)

                        if lcn == bindName:
                            res += self._input_param_subst(bdx, bindName)
                            fnd  = True
                            break

                        ldx += 1

                    if fnd:
                        break

                elif proc.in_fields[bdx].name == bindName:
                    res += self._input_param_subst(ldx, bindName)
                    i = e - 1
                    break

            if bdx >= len(proc.in_fields):
                raise Exception("Unknown identifier [bindName: %s, position:%d, sql: %s]" % (bindName, i, sql))

        return res


    def _is_varible_char(self, ch: str) -> bool:
        if ch == '_' or ch == '.' or\
           (ch >= 'a' and ch <= 'z') or\
           (ch >= 'A' and ch <= 'Z') or\
           (ch >= '0' and ch <= '9'):
            return True

        return False
