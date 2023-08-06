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

import mettle.genes.db

from .gen_sql import GenSql


class Database:

    DAO_MODE_INLINE      = 'inline'
    DAO_MODE_STORED_PROC = 'stored-proc'

    def __init__(self):
        self.enabled     = False
        self.dao_mode    = self.DAO_MODE_INLINE
        self.sp_name     = '_sp_|'
        self.generators  = {}
        self.dbname      = self.name()

        for ge in mettle.genes.db.code_generators:
            go = ge()
            self.generators[go.name()] = go

        dbgen = self._db_generator()

        self.generators[dbgen.name()] = dbgen


    def name(self) -> str:
        return 'NONE'


    def _db_generator(self) -> GenSql:
        raise Exception('No DB Generator defined for database [%s]' % self.dbname)


    def _sequence_pre_insert(self) -> bool:
        raise Exception('Sequence pre insert rule not set for database [%s]' % self.dbname)


    def _sequence_post_insert(self) -> bool:
        raise Exception('Sequence post insert rule not set for database [%s]' % self.dbname)


    def stored_proc_support(self) -> bool:
        return False


    def initialize_generation(self, gen_info: dict):
        for g, gobj in self.generators.items():
            if not gobj.enabled:
                continue

            gobj.initialize_generation(gen_info)


    def generate(self, gen_info: dict, lang_generators: dict, for_async: bool = False, for_finalize: bool = False):
        gen_info['database'] = self

        for g, gobj in self.generators.items():
            if not gobj.enabled:
                continue

            if g in lang_generators:
                gobj.set_overrides(lang_generators[g])

            if for_async:
                if not gobj.async_enabled():
                    continue

                gobj.async_toggle(True)
            else:
                gobj.async_toggle(False)

            gen_info['db.schema'] = gobj.get_option('db.schema', blank_ok=True)

            if for_finalize:
                gobj.close_daos(gen_info)
            else:
                gobj.generate_daos(gen_info, self.dbname)


    def generate_dao_done(self, gen_info: dict, lang_generators: dict, for_async: bool = False):
        gen_info['database'] = self

        for g, gobj in self.generators.items():
            if not gobj.enabled:
                continue

            if g in lang_generators:
                gobj.set_overrides(lang_generators[g])

            if for_async:
                if not gobj.async_enabled():
                    continue

                gobj.async_toggle(True)
            else:
                gobj.async_toggle(False)

            gen_info['db.schema'] = gobj.get_option('db.schema', blank_ok=True)

            gobj.generate_daos(gen_info, self.dbname)


    def _table_name(self, gen_info: dict) -> str:
        if gen_info['db.schema'] == '':
            return gen_info['table'].name

        return '%s.%s' % (gen_info['db.schema'], gen_info['table'].name)


    def _column_name(self, cname: str) -> str:
        return cname


    def _timestamp_function(self):
        return 'CURRENT_TIMESTAMP'


    def _sql_select_one(self, gen_info: dict) -> str:
        sql = 'select'

        comma = '\n'

        for f in gen_info['table'].columns:
            sql += '%s  %s' % (comma, self._column_name(f.name))
            comma = ',\n'

        sql += '\nfrom\n  %s' % self._table_name(gen_info)
        sql += '\nwhere'

        comma = '\n'
        for f in gen_info['table'].primary_key_columns():
            sql += '%s  %s = :%s' % (comma, self._column_name(f.name), f.name)
            comma = ' and\n'

        return sql


    def _sql_lock_one(self, gen_info: dict) -> str:
        return self._sql_select_one(gen_info)


    def _sql_update(self, gen_info: dict) -> str:
        sql = 'update\n  %s\nset' % self._table_name(gen_info)

        comma = '\n'

        for f in gen_info['table'].non_primary_key_columns():
            # if f.type == 'timestamp':
            #     sql += '%s  %s = %s' % (comma, self._column_name(f.name), self._timestamp_function())
            # else:
            sql += '%s  %s = :%s' % (comma, self._column_name(f.name), f.name)
            comma = ',\n'

        sql += '\nwhere'

        comma = '\n'

        for f in gen_info['table'].primary_key_columns():
            sql += '%s  %s = :%s' % (comma, self._column_name(f.name), f.name)
            comma = ' and\n'

        return sql


    def _sql_delete_one(self, gen_info: dict) -> str:
        sql   = 'delete from\n  %s\nwhere' % self._table_name(gen_info)
        comma = '\n'

        for f in gen_info['table'].primary_key_columns():
            sql += '%s  %s = :%s' % (comma, self._column_name(f.name), f.name)
            comma = ' and\n'

        return sql


    def _sql_insert(self, gen_info: dict) -> str:
        sql   = 'insert into %s (' % self._table_name(gen_info)
        comma = '\n'

        for f in gen_info['table'].columns:
            if self._sequence_post_insert() and f.type.startswith('seq'):
                continue

            sql += '%s  %s' % (comma, self._column_name(f.name))
            comma = ',\n'

        sql   += '\n) values ('
        comma  = '\n'

        for f in gen_info['table'].columns:
            if self._sequence_post_insert() and f.type.startswith('seq'):
                continue

            # if f.type == 'timestamp':
            #     sql += '%s  %s' % (comma, self._timestamp_function())
            # else:
            sql += '%s  :%s' % (comma, f.name)
            comma = ',\n'

        sql += '\n)'

        return sql


    def _sql_delete_all(self, gen_info: dict) -> str:
        sql = 'delete from %s' % self._table_name(gen_info)
        return sql


    def _sql_select_all(self, gen_info: dict) -> str:
        sql = 'select'

        comma = '\n'

        for f in gen_info['table'].columns:
            sql += '%s  %s' % (comma, self._column_name(f.name))
            comma = ',\n'

        pkfields = gen_info['table'].primary_key_columns()

        if len(pkfields) == 0:
            sql += '\nfrom\n  %s\norder by\n  %s' % (
                self._table_name(gen_info), self._column_name(gen_info['table'].columns[0].name))
        else:
            comma = '\n'
            sql += '\nfrom\n  %s\norder by' % self._table_name(gen_info)

            for p in pkfields:
                sql += '%s  %s' % (comma, self._column_name(p.name))
                comma = ',\n'

        return sql
