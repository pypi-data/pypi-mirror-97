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
import time

from .generator import Generator
from .table     import Table


class GenPy3(Generator):

    SELECT_LOCK_ARG  = '_lock4update'

    def __init__(self):
        Generator.__init__(self, ['py'])
        self.targ_type  = 'code'
        self.namespace = None

        self._field_map['bool']      = Generator.FieldMap('bool',              type_flag = 'bool',     def_value = 'False')
        self._field_map['int8']      = Generator.FieldMap('int',               type_flag = 'int',      def_value = '0')
        self._field_map['int16']     = Generator.FieldMap('int',               type_flag = 'int',      def_value = '0')
        self._field_map['int32']     = Generator.FieldMap('int',               type_flag = 'int',      def_value = '0')
        self._field_map['int64']     = Generator.FieldMap('int',               type_flag = 'int',      def_value = '0')
        self._field_map['seq32']     = Generator.FieldMap('int',               type_flag = 'int',      def_value = '0')
        self._field_map['seq64']     = Generator.FieldMap('int',               type_flag = 'int',      def_value = '0')
        self._field_map['char']      = Generator.FieldMap('str',               type_flag = 'str',      def_value = "''")
        self._field_map['string']    = Generator.FieldMap('str',               type_flag = 'str',      def_value = "''")
        self._field_map['uuid']      = Generator.FieldMap('uuid.UUID',         type_flag = 'uuid',     def_value = "None")
        self._field_map['date']      = Generator.FieldMap('datetime.date',     type_flag = 'date',     def_value = 'datetime.date.min')      # noqa
        self._field_map['time']      = Generator.FieldMap('datetime.time',     type_flag = 'date',     def_value = 'datetime.time.min')      # noqa
        self._field_map['datetime']  = Generator.FieldMap('datetime.datetime', type_flag = 'date',     def_value = 'datetime.datetime.min')  # noqa
        self._field_map['timestamp'] = Generator.FieldMap('datetime.datetime', type_flag = 'date',     def_value = 'datetime.datetime.min')  # noqa
        self._field_map['memblock']  = Generator.FieldMap('bytearray',         type_flag = 'memblock', def_value = "b''")
        self._field_map['double']    = Generator.FieldMap('float',             type_flag = 'double',   def_value = '0.0')
        self._field_map['json']      = Generator.FieldMap('dict',              type_flag = 'json',     def_value = "None")
        self._field_map['dynamic']   = Generator.FieldMap('str',               type_flag = 'str',      def_value = "''")
        self._field_map['dbrec']     = Generator.FieldMap('table',             type_flag = 'dbrec',    def_value = 'None')

        self._init_code_options()
        self._init_casing({ 'class': 'pascal', 'method': 'camel', 'member': 'camel', 'file': 'pascal' })

        self._async = {
            'await'   : '',
            'async'   : '',
            'conn'    : 'IConnect',
        }


    def name(self):
        return 'Python3'


    def initialize_generation(self, gen_info):
        Generator.initialize_generation(self, gen_info)


    def finalize_generation(self, gen_info):
        """
        Create all the __init__.py files in the namespace directories.
        """
        if gen_info['clean']:
            return

        nsdir   = self.proj_relative_path(gen_info, self.dest_dir(os.path.sep))
        ns      = self._namespace()
        fh      = None
        ns_file = os.path.join(nsdir, '__init__.py')
        fh      = open(ns_file, 'wt')

        self._add_headers(fh)
        fh.close()

        nstabledir = os.path.join(nsdir, self.get_option('dir.tables', 'tables'))

        if not os.path.exists(nstabledir):
            raise Exception('Namespace directory not found [%s]' % nstabledir)

        ns_file = os.path.join(nstabledir, '__init__.py')
        fh      = open(ns_file, 'wt')

        self._add_headers(fh)

        for gf in self._gened_files[ns]:
            fh.write('from .%s import %s\n' % (gf.fname, gf.cls))

        fh.close()

        nsdaodir = os.path.join(nsdir, self.get_dao_dir_name())

        if not os.path.exists(nsdaodir):
            raise Exception('Namespace directory not found [%s]' % nsdaodir)

        ns_file = os.path.join(nsdaodir, '__init__.py')
        fh      = open(ns_file, 'wt')

        self._add_headers(fh)

        fh.close()


    def generate_tables(self, gen_info: dict):
        self._mode      = self.TABLE
        self._target_db = 'tables'
        self._generate(gen_info)


    def generate_daos(self, gen_info: dict, target_db: str):
        self._mode      = self.DAO
        self._target_db = target_db

        if self.async_on():
            self._async['await'] = 'await '
            self._async['async'] = 'async '
            self._async['conn']  = 'IAConnect'
        else:
            self._async['await']   = ''
            self._async['async']   = ''
            self._async['conn']    = 'IConnect'

        self._generate(gen_info)


    def close_daos(self, gen_info: dict):
        if gen_info['clean']:
            return

        if self._mode == self.DAO:
            self._gen_dao_init_file()


    def _generate(self, gen_info):
        if gen_info['clean']:
            if self._mode == self.DAO:
                self.clean(gen_info, os.path.join('dao', self._target_db))
            else:
                self.clean(gen_info, self._target_db)

            return

        self._gen_info         = gen_info
        self.namespace         = self._namespace()
        self._table_id         = self._gen_info['table'].name
        self._table_class      = self._ident('class.table', self._table_id)
        self._table_key_id      = None
        self._table_key_class   = None
        self._table_key_columns = self._gen_info['table'].primary_key_columns()

        if len(self._table_key_columns) > 0:
            self._table_key_id    = '%sKey' % self._table_id
            self._table_key_class = self._ident('class.table', self._table_key_id)

        if self._mode == self.TABLE:
            self._write_data_class(self._table_key_id,
                                   self._table_key_columns,
                                   key_class = True)

            self._write_data_class(self._table_id,
                                   self._gen_info['table'].columns,
                                   main_class= True)

            self._gen_custom_procs()
        elif self._mode == self.DAO:
            self.namespacedao  = '%s.dao.%s' % (self.namespace, self._gen_info['database'].dbname)

            self._gen_dao_class()
            self._gen_standard_procs()
            self._gen_custom_procs()


    def _add_headers(self, fh):
        if self._mode == self.TABLE:
            message = '# This file was generated by mettle.genes.db.GenPy3 [ver %s] on %s\n#\n\n' % (
                self._gen_info['version'], time.asctime())
        else:
            message = '# This file was generated by mettle.genes.db.GenPy3 [ver %s] on %s\n#  Target Database = %s\n#\n' % (
                self._gen_info['version'], time.asctime(), self._gen_info['database'].dbname)

        fh.write(message)


    def _member(self, mem):
        return self._ident_member(mem)


    def _write_in_field_binding(self, fh, fields: list, sub_rec: str = '', is_insert: bool = False):
        fnd           = False
        subIdent      = sub_rec.replace('.', '_')
        has_sequences = self._check_for_sequence(fields)

        for f in fields:
            if f.type == 'dynamic':
                continue

            fnd   = True

            if is_insert and has_sequences and self._gen_info['database']._sequence_post_insert() and f.type.startswith('seq'):
                continue

            if f.type == 'dbrec':
                self._write_in_field_binding(fh, self._lookup_columns(f.lookup, ''), '%s.' % self._member(f.name))
                continue

            fmap  = self._field_map[f.type]
            bname = '"%s%s"' % (subIdent, f.name)
            iname = 'self.irec.%s%s' % (sub_rec, self._member(f.name))

            if fmap.type_flag == 'str':
                if f.type == 'char':
                    fh.write('        self._dbstmnt.bind_in(%s, %s, %s, %d)\n' % (bname, iname, fmap.name, 1))
                elif f.length > 0:
                    fh.write('        self._dbstmnt.bind_in(%s, %s, %s, %d)\n' % (bname, iname, fmap.name, f.length))
                else:
                    fh.write('        self._dbstmnt.bind_in(%s, %s, %s)\n' % (bname, iname, fmap.name))
            elif fmap.type_flag == 'int':
                fh.write('        self._dbstmnt.bind_in(%s, %s, %s, %d)\n' % (bname, iname, fmap.name, int(f.type[3:]) / 8))
            elif fmap.type_flag in ('json', 'uuid'):
                fh.write('        self._dbstmnt.bind_in(%s, %s, %s)\n' % (bname, iname, fmap.name))
            else:
                fh.write('        self._dbstmnt.bind_in(%s, %s, %s)\n' % (bname, iname, fmap.name))

        if fnd and sub_rec == '':
            fh.write('\n')


    def _write_out_field_binding(self, fh, fields: list, sub_rec: str = ''):
        fnd      = False
        subIdent = sub_rec.replace('.', '_')

        for f in fields:
            if f.type == 'dynamic':
                continue

            fnd  = True

            if f.type == 'dbrec':
                self._write_out_field_binding(fh, self._lookup_columns(f.lookup, ''), '%s.' % self._member(f.name))
                continue

            fmap  = self._field_map[f.type]
            bname = '"%s%s"' % (subIdent, f.name)

            if fmap.type_flag == 'str':
                if f.type == 'char':
                    fh.write('        self._dbstmnt.bind_out(%s, %s, 1)\n' % (bname, fmap.name))
                elif f.length > 0:
                    fh.write('        self._dbstmnt.bind_out(%s, %s, %d)\n' % (bname, fmap.name, f.length))
                else:
                    fh.write('        self._dbstmnt.bind_out(%s, %s)\n' % (bname, fmap.name))

            elif fmap.type_flag == 'int':
                fh.write('        self._dbstmnt.bind_out(%s, %s, %d)\n' % (bname, fmap.name, int(f.type[3:]) / 8))
            elif fmap.type_flag in ('json', 'uuid'):
                fh.write('        self._dbstmnt.bind_out(%s, %s)\n' % (bname, fmap.name))
            else:
                fh.write('        self._dbstmnt.bind_out(%s, %s)\n' % (bname, fmap.name))

        if fnd and sub_rec == '':
            fh.write('\n')


    def _write_get_timestamps(self, fh, fields):
        fnd = False

        for f in fields:
            if f.type != 'timestamp':
                continue

            fh.write('        self.irec.%s = %sself._dbcon.get_timestamp()\n' % (
                self._member(f.name), self._async['await']))
            fnd = True

        if fnd:
            fh.write('\n')


    def _write_get_sequences_post(self, fh, proc):
        for f in proc.in_fields:
            if f.type.startswith('seq'):
                fh.write('        self.irec.%s = %sself._dbcon.post_get_sequence(self._dbstmnt, "%s", "%s", %d)\n\n' % (
                    self._member(f.name), self._async['await'],
                    self._table_name(self._gen_info), f.name, 4 if f.type == 'seq32' else 8))


    def _write_get_sequences_pre(self, fh, proc):
        for f in proc.in_fields:
            if f.type.startswith('seq'):
                fh.write('        self.irec.%s = %sself._dbcon.pre_get_sequence(self._dbstmnt, "%s", "%s", %d)\n\n' % (
                    self._member(f.name), self._async['await'],
                    self._table_name(self._gen_info), f.name, 4 if f.type == 'seq32' else 8))


    def _write_dynamic_binding(self, fh, proc):
        fnd = False

        for f in proc.in_fields:
            if f.type != 'dynamic':
                continue

            fh.write('        self._dbstmnt.dynamic(%s self.irec.%s)\n' % ('"[%s]",' % f.name, self._member(f.name)))
            fnd = True

        if fnd:
            fh.write('\n')


    def _write_add_sql(self, fh, sql):
        fh.write('        self._dbstmnt.sql("""')
        newLine = ''

        for s in sql.splitlines() :
            if s.strip() == '':
                continue

            fh.write('%s%s' % (newLine, s))
            newLine = '\n'

        fh.write('""")\n')


    def _write_exec_deft(self, fh, cls, irec, proc, proc_ignore_tyes, iflds):
        if not irec:
            return

        self._write_py_method(fh,
                              '"%s": Self for convenience.' % cls,
                              self._ident_method('ExecDeft'),
                              iflds,
                              ignore_types = proc_ignore_tyes,
                              method_descr = 'Execute the query by setting all the inputs.',
                              can_async = True)

        self._write_copy_args(fh, 'self.irec.', iflds, '', proc_ignore_tyes, db_rec_none=False)
        fh.write('\n        return %sself.exec()\n\n' % self._async['await'])


    def _write_insert_exec(self, fh, cls, irec, proc, iflds):

        self._write_py_method(fh,
                              '"%s": Self for convenience.' % cls,
                              self._ident_method('Exec'),
                              'irec: %s = None' % irec,
                              method_descr = 'Execute the query, optionally passing in the input rec.',
                              can_async = True)

        fh.write('        if irec:\n')
        fh.write('            self.irec._copy_from(irec)\n\n')
        fh.write('        self._destroy()\n\n')
        fh.write('        self._dbstmnt = %sself._dbcon.statement("%s%s", self._dbcon.STMNT_TYPE_CUD)\n\n' % (
            self._async['await'], self._table_id, proc.name))

        if self._gen_info['database'].dbname in proc.sql and self._gen_info['database'].dbname != 'std':
            sql = proc.sql[self._gen_info['database'].dbname]
        else:
            sql = proc.sql['std']

        has_sequences = self._check_for_sequence(iflds)

        if has_sequences and self._gen_info['database']._sequence_pre_insert():
            self._write_get_sequences_pre(fh, proc)

        self._write_add_sql(fh, sql)
        fh.write('\n')
        self._write_get_timestamps(fh, iflds)
        self._write_dynamic_binding(fh, proc)
        self._write_in_field_binding(fh, iflds, is_insert=True)

        fh.write('        %sself._dbcon.execute(self._dbstmnt)\n\n' % self._async['await'])

        if has_sequences and self._gen_info['database']._sequence_post_insert():
            self._write_get_sequences_post(fh, proc)

        fh.write('        if irec:\n')
        fh.write('            irec._copy_from(self.irec)\n\n')
        fh.write('        return self\n\n')


    def _write_std_exec(self, fh, cls, irec, proc, get_timestamps, iflds, oflds):
        if irec:
            self._write_py_method(fh,
                                  '"%s": Self for convenience.' % cls,
                                  self._ident_method('Exec'),
                                  'irec: %s = None' % irec,
                                  method_descr = 'Execute the query, optionally passing in the input rec.',
                                  can_async = True)

            fh.write('        if irec:\n')
            fh.write('            self.irec._copy_from(irec)\n\n')
        else:
            self._write_py_method(fh,
                                  '"%s": Self for convenience.' % cls,
                                  self._ident_method('Exec'),
                                  None,
                                  method_descr = 'Execute the query.',
                                  can_async = True)

        fh.write('        self._destroy()\n\n')

        if oflds:
            fh.write('        self._dbstmnt = %sself._dbcon.statement("%s%s", self._dbcon.STMNT_TYPE_READ)\n\n' % (
                self._async['await'], self._table_id, proc.name))
        else:
            fh.write('        self._dbstmnt = %sself._dbcon.statement("%s%s", self._dbcon.STMNT_TYPE_CUD)\n\n' % (
                self._async['await'], self._table_id, proc.name))

        if self._gen_info['database'].dbname in proc.sql:
            sql = proc.sql[self._gen_info['database'].dbname]
        else:
            sql = proc.sql['std']

        self._write_add_sql(fh, sql)
        fh.write('\n')

        if get_timestamps:
            self._write_get_timestamps(fh, iflds)

        self._write_dynamic_binding(fh,  proc)
        self._write_in_field_binding(fh,  iflds)
        self._write_out_field_binding(fh, oflds)

        if proc.name == 'LockOne':
            fh.write('        %sself._dbcon.lock(self._dbstmnt)\n\n' % self._async['await'])

        fh.write('        %sself._dbcon.execute(self._dbstmnt)\n\n' % self._async['await'])

        if irec:
            fh.write('        if irec:\n')
            fh.write('            irec._copy_from(self.irec)\n\n')

        fh.write('        return self\n\n')


    def _write_sql_proc_dao(self, proc, proc_ignore_tyes=[], get_timestamps=False, do_insert=False):
        if self._mode != self.DAO:
            return

        idname = '%s%s' % (self._table_id, proc.name)
        cls    = self._ident('class.dao', idname )

        fh   = self.gened_file_open(self._gen_info,
                                    self._ident('file.dao', idname),
                                    extra_dir = '%s/%s' % (self.get_dao_dir_name(), self._gen_info['database'].dbname),  # noqa
                                    cls = cls,
                                    add_namespace_to_path = False)

        self._add_headers(fh)
        self._gen_headers(fh)

        irecs  = []
        orecs  = []
        iflds  = proc.in_fields
        oflds  = proc.out_fields

        if proc.is_standard:
            if len(proc.in_fields) > 0:
                if len(proc.in_fields) == 1 and proc.in_fields[0].type == 'dbrec':
                    irecs.append({
                        'cls'  : self._table_class,
                        'file' : self._ident('file.table', self._table_id),
                    })
                    iflds = self._lookup_columns(proc.in_fields[0].lookup, proc.name)
                else:
                    irecs.append({
                        'cls' : self._ident('class.qryin', '%s%s' % (self._table_id, proc.name)),
                        'file': self._ident('file.qryin', '%s%s' % (self._table_id, proc.name)),
                    })

                    for inf in proc.in_fields:
                        if inf.type == 'dbrec':
                            ltbl = self._lookup_name(inf.lookup)
                            irecs.append({
                                'cls' : self._ident('class.table', ltbl),
                                'file': self._ident('file.table', ltbl),
                            })

            if len(proc.out_fields) > 0:
                if len(proc.out_fields) == 1 and proc.out_fields[0].type == 'dbrec':
                    orecs.append({
                        'cls': self._table_class,
                        'file': self._ident('file.table', self._table_id),
                    })
                    oflds = self._lookup_columns(proc.out_fields[0].lookup, proc.name)
                else:
                    orecs.append({
                        'cls': self._ident('class.qryout', '%s%s' % (self._table_id, proc.name)),
                        'file': self._ident('file.qryout', '%s%s' % (self._table_id, proc.name)),
                    })

                    for onf in proc.out_fields:
                        if onf.type == 'dbrec':
                            ltbl = self._lookup_name(onf.lookup)
                            irecs.append({
                                'cls' : self._ident('class.table', ltbl),
                                'file': self._ident('file.table', ltbl),
                            })

        else:
            if proc.in_fields:
                irecs.append({
                    'cls': self._ident('class.table', proc.in_override_name),
                    'file': self._ident('file.table',  proc.in_override_name),
                })

            if proc.out_fields:
                orecs.append({
                    'cls': self._ident('class.table', proc.out_override_name),
                    'file': self._ident('file.table',  proc.out_override_name),
                })

        nsTableDir = os.path.join(self.namespace, self.get_option('dir.tables')).replace('/', '.')
        dups = []

        for ior in irecs + orecs:
            if ior['cls'] in dups:
                continue

            fh.write('from %s.%s import %s\n' % (nsTableDir, ior['file'], ior['cls']))
            dups.append(ior['cls'])


        fh.write('\n')
        fh.write('class %s:\n' % cls)
        fh.write('\n')
        fh.write('    def __init__(self, dbcon: mettle.db.%s):\n' % self._async['conn'])
        fh.write('        """\n')
        fh.write('        Constructor.\n\n')
        fh.write('        :param dbcon: Mettle database connection object.\n')
        fh.write('        """\n')
        fh.write('        self._dbcon   = dbcon\n')
        fh.write('        self._dbstmnt = None\n')

        if irecs:
            fh.write('        self.irec     = %s()\n' % irecs[0]['cls'])

        if orecs:
            fh.write('        self.orec     = %s()\n' % orecs[0]['cls'])

        fh.write('\n')
        fh.write('    def __del__(self):\n')
        fh.write('        """\n')
        fh.write('        Destructor.\n')
        fh.write('        """\n')
        fh.write('        del self._dbstmnt\n\n')

        fh.write('    def __enter__(self):\n')
        fh.write('        """\n')
        fh.write('        With statement enter.\n')
        fh.write('        """\n')
        fh.write('        return self\n\n')

        fh.write('    def __exit__(self, type, value, traceback):\n')
        fh.write('        """\n')
        fh.write('        With statement exit.\n')
        fh.write('        """\n')
        fh.write('        self._destroy()\n\n')

        fh.write('    def _destroy(self):\n')
        fh.write('        if self._dbstmnt == None:\n')
        fh.write('            return\n\n')
        fh.write('        del self._dbstmnt\n')
        fh.write('        self._dbstmnt = None\n\n')

        # void DAO::Exec()
        if do_insert:
            self._write_exec_deft(fh, cls, irecs[0]['cls'], proc, proc_ignore_tyes, iflds)
            self._write_insert_exec(fh, cls, irecs[0]['cls'], proc, iflds)
        else:
            if irecs:
                self._write_exec_deft(fh, cls, irecs[0]['cls'], proc, proc_ignore_tyes, iflds)
                self._write_std_exec(fh, cls, irecs[0]['cls'], proc, get_timestamps, iflds, oflds)
            else:
                self._write_std_exec(fh, cls, None, proc, get_timestamps, iflds, oflds)


        # bool DAO::Fetch()
        if orecs and len(oflds):
            self._write_py_method(fh,
                                  'bool: True if a row is retreived.',
                                  self._ident_method('Fetch'),
                                  None,
                                  method_descr = 'Fetches the next row from the executed query.',
                                  can_async = True)

            fh.write('        if not %sself._dbcon.fetch(self._dbstmnt):\n' % self._async['await'])
            fh.write('            return False\n\n')

            idx = 0

            for f in oflds:
                fname = self._member(f.name)

                if f.type == 'dbrec':
                    for dbf in self._lookup_columns(f.lookup, proc.name):
                        dbfname = self._member(dbf.name)
                        fh.write('        %s = self._dbstmnt.result[%d]\n' % ('self.orec.%s.%s' % (fname, dbfname), idx))
                        idx += 1

                else:
                    fh.write('        %s = self._dbstmnt.result[%d]\n' % ('self.orec.%s' % fname, idx))
                    idx += 1

            fh.write('\n        return True\n\n')

            self._write_py_method(fh,
                                  'int: Number of rows fetched.',
                                  self._ident_method('FetchAll'),
                                  'outList: %s.List, clearList: bool = True' % orecs[0]['cls'],
                                  method_descr = 'Fetch all the rows into the specified list and return the list count.',
                                  can_async = True)

            fh.write('        if clearList:\n')
            fh.write('            outList.clear()\n\n')
            fh.write('        while %sself.%s():\n' % (self._async['await'], self._ident_method('Fetch')))
            fh.write('            outList.append(copy.deepcopy(self.orec))\n\n')
            fh.write('        return len(outList)\n\n')

        self.gened_file_close(fh)


    def _write_data_class(self,
                          idname     : str,
                          columns    : list,
                          main_class : bool = False,
                          key_class  : bool = False,
                          out_obj    : bool = False):
        if not columns:
            return

        fileIdent = ''
        clsIdent = ''

        if main_class or key_class:
            fileIdent = 'file.table'
            clsIdent = 'class.table'
        elif out_obj:
            fileIdent = 'file.qryout'
            clsIdent = 'class.qryout'
        else:
            fileIdent = 'file.qryin'
            clsIdent = 'class.qryin'

        cls_name = self._ident(clsIdent, idname)

        fh = self.gened_file_open(self._gen_info,
                                  self._ident(fileIdent, idname),
                                  extra_dir = self.get_option('dir.tables'),
                                  cls = cls_name,
                                  add_namespace_to_path = False)

        tbl = self._gen_info['table']

        self._add_headers(fh)
        self._gen_headers(fh, main_class, key_class, len(tbl.primary_keys))

        if not main_class and not key_class:
            self._gen_table_imports(fh, cls_name, columns)

        fh.write('class %s(mettle.io.ISerializable' % cls_name)

        if main_class and len(tbl.primary_keys) > 0:
            fh.write(', mettle.db.IPrimaryKey')

        fh.write('):\n\n')

        # __init__(columns)
        self._write_py_method(fh,
                              None,
                              '__init__',
                              columns,
                              ignore_types = ['timestamp'],
                              use_default_vals = True,
                              method_descr = 'Constructor.')
        self._write_copy_args(fh, 'self.', columns, '', ['timestamp'])
        self._write_member_decleration(fh, columns, ['timestamp'])
        fh.write('\n')

        # void clear()
        self._write_py_method(fh,
                              None,
                              self._ident_method('Clear'),
                              None,
                              method_descr = 'Clears all member variables for this database record.')
        self._write_clear_fields(fh, columns)
        fh.write('\n')

        # string Table::_Name()
        self._write_py_method(fh, 'str: The name.', '_name', None, method_descr = 'Name of the record.')

        if main_class:
            fh.write("        return '%s'\n\n" % self._ident('class.table', tbl.name))
        elif key_class:
            fh.write("        return '%s'\n\n" % self._ident('class.table', '%sKey' % tbl.name))
        else:
            fh.write("        return '%s'\n\n" % (cls_name))

        # int Table::_serialize()
        self._write_py_method(fh,
                              None,
                              '_serialize',
                              '_w: mettle.io.IWriter, _oname: str = None',
                              method_descr = 'Serialize record to a stream.')

        fh.write('        if _oname == None:\n')
        fh.write('            _oname = self._name()\n\n')
        fh.write('        _w.write_start(_oname)\n')

        self._write_encapsualted_fields(fh, columns, main_class or key_class, {
            'int8'      : '        _w.write_int8("%s", self.%s)\n',
            'int16'     : '        _w.write_int16("%s", self.%s)\n',
            'int32'     : '        _w.write_int32("%s", self.%s)\n',
            'int64'     : '        _w.write_int64("%s", self.%s)\n',
            'seq32'     : '        _w.write_int32("%s", self.%s)\n',
            'seq64'     : '        _w.write_int64("%s", self.%s)\n',
            'char'      : '        _w.write_char("%s", self.%s)\n',
            'bool'      : '        _w.write_bool("%s", self.%s)\n',
            'double'    : '        _w.write_double("%s", self.%s)\n',
            'string'    : '        _w.write_string("%s", self.%s)\n',
            'json'      : '        _w.write_json("%s", self.%s)\n',
            'dynamic'   : '        _w.write_string("%s", self.%s)\n',
            'datetime'  : '        _w.write_datetime("%s", self.%s)\n',
            'timestamp' : '        _w.write_datetime("%s", self.%s)\n',
            'date'      : '        _w.write_date("%s", self.%s)\n',
            'time'      : '        _w.write_time("%s", self.%s)\n',
            'memblock'  : '        _w.write_bytearray("%s", self.%s)\n',
            'dbrec'     : '        self.%s._serialize(_w)\n',
            'uuid'      : '        _w.write_guid("%s", self.%s)\n',
        })

        fh.write('        _w.write_end(_oname)\n\n')

        # int Table::_deserialize()
        self._write_py_method(fh,
                              None,
                              '_deserialize',
                              '_r: mettle.io.IReader, _oname: str = None',
                              method_descr = 'Deserialize record from a stream.')

        fh.write('        if _oname == None:\n')
        fh.write('            _oname = self._name()\n\n')
        fh.write('        _r.read_start(_oname)\n')

        self._write_encapsualted_fields(fh, columns, main_class or key_class, {
            'int8'      : '        self.%s = _r.read_int8("%s")\n',
            'int16'     : '        self.%s = _r.read_int16("%s")\n',
            'int32'     : '        self.%s = _r.read_int32("%s")\n',
            'int64'     : '        self.%s = _r.read_int64("%s")\n',
            'seq32'     : '        self.%s = _r.read_int32("%s")\n',
            'seq64'     : '        self.%s = _r.read_int64("%s")\n',
            'char'      : '        self.%s = _r.read_char("%s")\n',
            'bool'      : '        self.%s = _r.read_bool("%s")\n',
            'double'    : '        self.%s = _r.read_double("%s")\n',
            'string'    : '        self.%s = _r.read_string("%s")\n',
            'json'      : '        self.%s = _r.read_json("%s")\n',
            'dynamic'   : '        self.%s = _r.read_string("%s")\n',
            'datetime'  : '        self.%s = _r.read_datetime("%s")\n',
            'timestamp' : '        self.%s = _r.read_datetime("%s")\n',
            'date'      : '        self.%s = _r.read_date("%s")\n',
            'time'      : '        self.%s = _r.read_time("%s")\n',
            'memblock'  : '        self.%s = _r.read_bytearray("%s")\n',
            'dbrec'     : '        self.%s._deserialize(_r)\n',
            'uuid'      : '        self.%s = _r.read_guid("%s")\n',
        })

        fh.write('        _r.read_end(_oname)\n\n')

        self._write_py_method(fh, None, '_copy_from', 'rec: "%s"' % cls_name)
        fh.write('        """\n')
        fh.write('        Copies the column from the rec into this record.\n\n')
        fh.write('        :param rec: The source record.\n')
        fh.write('        """\n')
        self._write_copy_args(fh, 'self.', columns, 'rec.', db_rec_none=False)
        fh.write('\n')

        if main_class and len(tbl.primary_keys) > 0:
            self._write_py_method(fh,
                                  None,
                                  '_write_pk',
                                  '_key: "%s"' % (cls_name),
                                  method_descr = 'Write the primary key columns to the key object.')
            fh.write('        self._write_key(_key)\n\n')

            self._write_py_method(fh,
                                  None,
                                  '_read_pk',
                                  '_key: "%s"' % (cls_name),
                                  method_descr = 'Read the primary key columns from the key object.')
            fh.write('        self._read_key(_key)\n\n')

            self._write_py_method(fh,
                                  None,
                                  '_serialize_key',
                                  '_w: mettle.io.IWriter',
                                  method_descr = 'Serialize the primary key to a stream.')
            fh.write('        _key = %sKey()\n\n' % (cls_name))
            fh.write('        self._write_key(_key)\n')
            fh.write('        _key._serialize(_w)\n\n')

            self._write_py_method(fh,
                                  None,
                                  '_deserialize_key',
                                  '_r: mettle.io.IReader',
                                  method_descr = 'Deserialize the primary key from a stream.')
            fh.write('        _key = %sKey()\n\n' % (cls_name))
            fh.write('        _key._deserialize(_r)\n')
            fh.write('        self._read_key(_key)\n\n')

        if not out_obj:
            self._write_davs(fh, cls_name, columns, main_class, key_class)

        if main_class:
            self._write_py_method(fh,
                                  None,
                                  '_write_key',
                                  '_key: %s' % self._table_key_class,
                                  method_descr = 'Write primary key columns to _key.')
            self._write_copy_args(fh, '_key.', self._table_key_columns, 'self.')
            fh.write('\n')

            self._write_py_method(fh,
                                  None,
                                  '_read_key',
                                  '_key: %s' % self._table_key_class,
                                  method_descr = 'Read the primary key columns from _key.')
            self._write_copy_args(fh, 'self.', self._table_key_columns, '_key.')
            fh.write('\n')

            self._write_couplets(fh, cls_name, columns)

        if (key_class or main_class) and len(self._table_key_columns) > 0:
            fh.write('    @staticmethod\n')
            fh.write('    def _pk_compare(x, y) -> int:\n')
            fh.write('        """\n')
            fh.write('        Compare function do primary key comparisons for list sorts and searches.\n\n')
            fh.write('        :return: zero for x == y, negative for x < y, positive for x > y\n')
            fh.write('        """\n')

            if len(self._table_key_columns) == 1:
                cname = self._member(self._table_key_columns[0].name)
                fmap  = self._field_map[self._table_key_columns[0].type]

                if fmap.type_flag in ('int', 'float'):
                    fh.write('        return x.%s - y.%s\n\n' % (cname, cname))
                else:
                    fh.write('        return (x.%s > y.%s) - (x.%s < y.%s)\n\n' % (cname, cname, cname, cname))
            else:
                for x in self._table_key_columns:
                    cname = self._member(x.name)
                    fmap  = self._field_map[x.type]

                    if fmap.type_flag in ('int', 'float'):
                        fh.write('        rc = x.%s - y.%s\n\n' % (cname, cname))
                    else:
                        fh.write('        rc = (x.%s > y.%s) - (x.%s < y.%s)\n\n' % (cname, cname, cname, cname))

                    if x == self._table_key_columns[-1]:
                        fh.write('        return rc\n\n')
                    else:
                        fh.write('        if rc != 0:\n')
                        fh.write('            return rc\n\n')

            fh.write('    def __lt__(self, other):\n')
            fh.write('        return other and self._pk_compare(self, other) < 0\n\n')
            fh.write('    def __gt__(self, other):\n')
            fh.write('        return other and self._pk_compare(self, other) > 0\n\n')
            fh.write('    def __eq__(self, other):\n')
            fh.write('        return other and self._pk_compare(self, other) == 0\n\n')
            fh.write('    def __le__(self, other):\n')
            fh.write('        return other and self._pk_compare(self, other) <= 0\n\n')
            fh.write('    def __ge__(self, other):\n')
            fh.write('        return other and self._pk_compare(self, other) >= 0\n\n')
            fh.write('    def __ne__(self, other):\n')
            fh.write('        return other == None or self._pk_compare(self, other)\n\n')

        fh.write('    def __repr__(self) -> str:\n')
        self._write_repr_method(fh, columns)
        fh.write('\n')

        fh.write('\n')
        fh.write('    class List(list, mettle.io.ISerializable):\n')
        fh.write('        """\n')
        fh.write('        List Class\n')
        fh.write('        """\n\n')

        self._write_py_method(fh,
                              'str: The name',
                              '_name',
                              None,
                              method_descr = 'Name of the list.',
                              extra_spaces = '    ')

        if main_class:
            fh.write("            return '%s.List'\n\n" % self._ident('class.table', tbl.name))
        elif key_class:
            fh.write("            return '%sKey.List'\n\n" % self._ident('class.table', tbl.name))
        else:
            fh.write("            return '%s.List'\n\n" % (cls_name))

        self._write_py_method(fh,
                              None,
                              '_serialize',
                              '_w: mettle.io.IWriter, _oname: str = None',
                              method_descr = 'Serialize the list to a stream.',
                              extra_spaces = '    ')

        fh.write('            if _oname == None:\n')
        fh.write('                _oname = self._name()\n\n')
        fh.write('            _w.write_start_list(_oname, len(self))\n\n')
        fh.write('            for _rec in self:\n')
        fh.write('                _rec._serialize(_w)\n\n')
        fh.write('            _w.write_end(_oname)\n\n')

        self._write_py_method(fh,
                              None,
                              '_deserialize',
                              '_r: mettle.io.IReader, _oname: str = None',
                              method_descr = 'Deserialize the list from a stream.',
                              extra_spaces = '    ')

        fh.write('            if _oname == None:\n')
        fh.write('                _oname = self._name()\n\n')
        fh.write('            _cnt = _r.read_start_list(_oname)\n\n')
        fh.write('            while _cnt >= 1:\n')
        fh.write('                _rec  = %s()\n' % (cls_name))
        fh.write('                _cnt -= 1\n')
        fh.write('                _rec._deserialize(_r)\n')
        fh.write('                self.append(_rec)\n\n')
        fh.write('            _r.read_end(_oname)\n\n')

        self._write_py_method(fh,
                              'str',
                              '__repr__',
                              None,
                              extra_spaces = '    ')

        fh.write("            return '<%s.List[%%d]>' %% (len(self))\n\n" % (cls_name))

        if not out_obj:
            fh.write('        def _get_davs(self, dvc=None')

            if main_class and not key_class:
                fh.write(', for_ins: bool = False, key_only: bool = False')

            fh.write('):\n')
            fh.write('            return %s._cache_davs(dvc'  % cls_name)

            if main_class and not key_class:
                fh.write(', for_ins, key_only')

            fh.write(')\n\n')

        self.gened_file_close(fh)


    def _write_col_davs(self, fh, col, main_class: bool):
        """
        Write the column davs.

        :param fh: File handle.
        :param col: Table.Column.
        :param main_class: Is this the main class.
        """
        if col.type == 'timestamp':
            return

        cdav = {}
        dset = {}
        fori = False
        spc  = ''

        if col.dav:
            cdav.update(col.dav)

        if main_class and col.type.startswith('seq'):
            fori = True
            spc  = '    '
            fh.write('        if not for_ins:\n')

        if col.type.startswith('seq'):
            if cdav is None or cdav.get('min') is None:
                fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.Min, 1))\n' % (
                    spc, col.name))
            else:
                fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.Min, %d))\n' % (
                    spc, col.name, cdav['min']))
            dset['min'] = True

        elif col.type == 'char':
            fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.Min, 1))\n' % (spc, col.name))
            fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.Max, 1))\n' % (spc, col.name))
            dset['min'] = True
            dset['max'] = True

        if col.not_null:
            fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.NotNull))\n' % (spc, col.name))
            dset['null'] = True

        if col.couplets and (not cdav or not cdav.get('in')):
            cdav['in'] = col.couplets

        if len(cdav) == 0:
            if fori:
                fh.write('\n')
            return

        for david, davval in cdav.items():
            if dset.get(david) is True:
                continue

            if david == 'null':
                if davval is False:
                    fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.NotNull))\n' % (
                        spc, col.name))
            elif david in ('min', 'max'):
                if col.type in ('date', 'datetime', 'time', 'timestamp'):
                    if col.type == 'date':
                        mask = 'datetime.date(%-Y, %-m, %-d)'
                    elif col.type in ('datetime', 'timestamp'):
                        mask = 'datetime.datetime(%-Y, %-m, %-d, %-H, %-M, %-S)'
                    else:
                        mask = 'datetime.time(%-H, %-M, %-S)'
                    fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %s))\n' % (
                        spc, col.name, self._davMap[david], davval.stftime(mask)))
                elif col.type in ('double', 'float'):
                    fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %lf))\n' % (
                        spc, col.name, self._davMap[david], davval))
                else:
                    fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %d))\n' % (
                        spc, col.name, self._davMap[david], davval))
            elif david in ('regex', 'func'):
                fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, "%s"))\n' % (
                    spc, col.name, self._davMap[david], davval))
            elif david in ('in', 'notin'):
                if col.type in ('char', 'string'):
                    opcloser = "'"
                    joiner   = "','"
                else:
                    opcloser = ""
                    joiner   = ","

                if type(davval) == dict:
                    dlist = davval.keys()
                elif type(davval) == list:
                    dlist = davval
                else:
                    raise Exception('Type [%s] not expected [davtype:%s, table:%s, col:%s]!' % (
                        str(type(davval)), david, self._table_id, col.name))

                fh.write('        %sdvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, [%s%s%s]))\n' % (
                    spc, col.name, self._davMap[david], opcloser, joiner.join(map(str, dlist)), opcloser))

        if fori:
            fh.write('\n')


    def _write_davs(self, fh, cls, columns, main_class, key_class):
        fh.write('    @staticmethod\n')
        fh.write('    def _cache_davs(dvc=None')

        if main_class:
            fh.write(', for_ins: bool = False, key_only: bool = False')

        fh.write('):\n')
        fh.write('        """\n')
        fh.write('        Cache the DAV into the dav cache (or create one) and return it.\n\n')
        fh.write('        :param dvc: (mettle.lib.DavCache), target cache, if None a new one is created and returned.\n')

        if main_class:
            fh.write('        :param for_ins: Davs for insert.\n')
            fh.write('        :param key_only: Davs by key only, ie for delete/selectone.\n')

        fh.write('        """\n')
        fh.write('        if dvc is None:\n')
        fh.write('            dvc = mettle.lib.DavCache()\n\n')

        haskeys = False

        for col in self._table_key_columns:
            self._write_col_davs(fh, col, main_class)
            haskeys = True

        if main_class and self._table_key_class and haskeys:
            fh.write('        if key_only:\n')
            fh.write('            return dvc\n\n')

        for col in columns:
            if col in self._table_key_columns:
                continue

            self._write_col_davs(fh, col, main_class)

        fh.write('\n        return dvc\n\n')

        fh.write('    def _get_davs(self, dvc=None')

        if main_class and not key_class:
            fh.write(', for_ins: bool = False, key_only: bool = False')

        fh.write('):\n')
        fh.write('        %s._cache_davs(dvc' % cls)

        if main_class and not key_class:
            fh.write(', for_ins, key_only')

        fh.write(')\n\n')


    def _write_py_method(self,
                         fh,
                         returns          : str,
                         method           : str,
                         args             : "list|str" = None,
                         ignore_types     : list = [],
                         extra_spaces     : str = '',
                         use_default_vals : bool = False,
                         method_descr     : str = None,
                         can_async        : bool = False):
        cstr  = '    %s%sdef %s(self' % (extra_spaces, self._async['async'] if can_async else '', method)
        comma = ', '

        fh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguements(fh, args, len(cstr) - 4, ignore_types, use_default_vals=use_default_vals)
            elif type(args) == str:
                fh.write('%s%s' % (comma, args))

        fh.write(')')

        if returns:
            fh.write(' -> %s' % returns.split(':')[0].strip())

        fh.write(':\n')

        if not method_descr:
            return

        fh.write('        %s"""\n' % extra_spaces)

        fh.write('        %s%s\n' % (extra_spaces, method_descr))

        if args:
            fh.write('\n')
            self._write_arguements(fh, args, len(cstr) - 4, comments = True, extra_spaces = extra_spaces)

        if returns and returns.find(':') != -1:
            if not args:
                fh.write('\n')

            fh.write('        %s:return: %s\n' % (extra_spaces, returns.split(':')[1].strip()))

        fh.write('        %s"""\n'  % extra_spaces)


    def _write_arguements(self,
                          fh,
                          args             : 'list|str',
                          spacing          : int,
                          filter_out       : list = None,
                          comments         : bool = False,
                          extra_spaces     : str  = '',
                          use_default_vals : bool = False):
        if not args:
            return

        if type(args) == str and comments:
            argi = args.split(',')

            for ai in argi:
                fh.write("        %s:param %s:\n" % (extra_spaces, ai.split(':')[0].strip()))

            return

        sep = ',\n%s%*.*s' % (extra_spaces, spacing, spacing, '')

        for a in args:
            if filter_out:
                if a.type in filter_out:
                    continue

            fmap = self._field_map[a.type]

            if a.name == self.SELECT_LOCK_ARG:
                if a.type == 'int32':
                    if comments:
                        fh.write("        %s:param %s:  The db lock object to use. \n" % (extra_spaces, self._member(a.name)))
                    else:
                        fh.write('%s%s: mettle.db.DBLock'  % (sep, a.name))
                else:
                    raise Exception('Unexpected code path')

                continue

            if comments:
                if a.type == 'dbrec':
                    param_comment = ' -> %s' % a.lookup
                else:
                    param_comment = ''

                fh.write("        %s:param %s: %s%s\n" % (extra_spaces, self._member(a.name), fmap.name, param_comment))

            else:
                if a.type == 'dbrec':
                    ltbl = self._lookup_name(a.lookup)
                    fh.write('%s%s: %s' % (sep, self._member(a.name), self._ident('class.table', ltbl)))
                else:
                    fh.write('%s%s: %s' % (sep, self._member(a.name), fmap.name))

                if a.def_val:
                    fh.write(' = %s' % a.def_val)
                elif use_default_vals:
                    fh.write(' = %s' % fmap.def_value)


    def _write_copy_args(self, fh, fromObj, args, toObj, fil=None, db_rec_none=True):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            if a.type == 'dbrec':
                if db_rec_none:
                    fh.write('        %s%s = %s()\n' % (
                        fromObj, self._member(a.name), self._ident('class.table', self._lookup_name(a.lookup))))
                    fh.write('        if %s:\n' % self._member(a.name))
                    fh.write('            %s%s._copy_from(%s%s)\n' % (
                        fromObj, self._member(a.name), toObj, self._member(a.name)))
                else:
                    fh.write('        %s%s._copy_from(%s%s)\n' % (
                        fromObj, self._member(a.name), toObj, self._member(a.name)))
            else:
                fh.write('        %s%s = %s%s\n' % (fromObj, self._member(a.name), toObj, self._member(a.name)))


    def _write_member_decleration(self, fh, members, includeOnly: list = None):
        for m in members:
            fmap = self._field_map[m.type]

            if includeOnly:

                if m.type not in includeOnly:
                    continue

            if m.type == 'dbrec':
                fh.write('        self.%s = %s()\n' % (
                    self._member(m.name)), self._ident('class.table', self._lookup_name(m.lookup)))
            else:
                fh.write('        self.%s = %s\n' % (self._member(m.name), fmap.def_value))


    def _write_encapsualted_fields(self, fh, args, tableField, type_masks):
        if not args:
            return

        for a in args:
            memName = self._member(a.name)

            if a.type in type_masks:
                if a.type == 'dbrec':
                    fh.write(type_masks[a.type] % (memName))
                else:
                    fh.write(type_masks[a.type] % (memName, memName))
            else:
                raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))


    def _write_clear_fields(self, fh, args, fil=None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            if a.type == 'dbrec':
                fh.write('        self.%s.%s()\n' % (self._member(a.name), self._ident_method('Clear')))
            else:
                fh.write('        self.%s = %s\n' % (self._member(a.name), fmap.def_value))


    def _write_repr_method(self, fh, args):
        fh.write("        return '<%s [" % self._table_id)

        delim = ''

        for a in args:
            fh.write('%s%s:'  % (delim, self._member(a.name)))
            fmap  = self._field_map[a.type]
            delim = ", "

            if fmap.type_flag in ('str', 'json', 'memblock'):
                fh.write('%.32s')
            elif fmap.type_flag in ('date'):
                fh.write('%s')
            else:
                fh.write('%r')


        fh.write("]>' % (\n")
        fh.write('            ')
        delim = ''

        for a in args:
            fmap  = self._field_map[a.type]
            fh.write('%sself.%s'  % (delim, self._member(a.name)))
            delim = ", "

        fh.write(')\n')


    def _write_couplets(self, fh, cls, columns):

        for col in columns:
            if not col.couplets:
                continue

            fmap    = self._field_map[col.type]
            valMask = '        %s = "%s"\n'
            cpCls   = self._ident('class.couplet', col.name)

            fh.write('    class %s(dict):\n' % cpCls)

            if fmap.type_flag in ('str'):
                keyMask = '        %s = "%s"\n'
            else:
                keyMask = '        %s = %s\n'

            for key, val in col.couplets.items():
                fh.write(keyMask % (self._ident_member('Key%s' % self._couplet_name(val)), str(key)))

            fh.write('\n')

            for key, val in col.couplets.items():
                fh.write(valMask % (self._ident_member('Value%s' % self._couplet_name(val)), str(val)))

            fh.write('\n')
            fh.write('        def __init__(self):\n')
            for key, val in col.couplets.items():
                cname = self._couplet_name(val)
                fh.write('            self[self.%s] = self.%s\n' % (
                    self._ident_member('Key%s' % cname), (self._ident_member('Value%s' % cname))))
            fh.write('\n')

            fh.write('        @staticmethod\n')
            fh.write('        def %s(key):\n' % (self._ident_method('GetValue')))
            for key, val in col.couplets.items():
                cname = self._couplet_name(val)
                fh.write('            if key == %s.%s.%s:\n' % (
                    self._table_class, cpCls, self._ident_member('Key%s' % cname)))
                fh.write('                return %s.%s.%s\n\n' % (
                    self._table_class, cpCls, self._ident_member('Value%s' % cname)))

            fh.write('            return ""\n\n')


    def _gen_headers(self, fh, main_class: bool = False, key_class: bool = False, pklen: int = 0, mainDao: bool = False):
        if mainDao and self.async_on:
            fh.write('import asyncio\n')

        fh.write('import copy\n')
        fh.write('import datetime\n')
        fh.write('import uuid\n')
        fh.write('import time\n')
        fh.write('import mettle.lib\n')
        fh.write('import mettle.io\n')
        fh.write('import mettle.db\n\n')

        if main_class and not key_class and pklen > 0:
            fh.write('from .%s import %s\n\n' % (self._ident('file.table', self._table_key_id), self._table_key_class))


    def _gen_table_imports(self, fh, cls, columns):
        tables = {}

        for col in columns:
            if col.type == 'dbrec':
                tables[self._lookup_name(col.lookup, 'import')] = True

        if len(tables) < 1:
            return

        for name in sorted(tables.keys()):
            cls_name = self._ident('class.table', name)
            cls_file = self._ident('file.table', name)
            fh.write('from .%s import %s\n' % (cls_file, cls_name))

        fh.write('\n')


    def _gen_dao_class(self):
        self._doa_class = self._ident('class.dao', self._table_id)
        self._std_procs = self._build_standard_procs(self._gen_info)

        fh  = self.gened_file_open(self._gen_info,
                                   self._ident('file.dao', self._table_id),
                                   extra_dir = '%s/%s' % (self.get_dao_dir_name(), self._gen_info['database'].dbname),  # noqa
                                   cls = self._doa_class,
                                   add_namespace_to_path = False)

        self._add_headers(fh)
        self._gen_headers(fh, mainDao = True)

        nstabledir = os.path.join(self.namespace, self.get_option('dir.tables')).replace('/', '.')
        fh.write('from %s.%s import %s\n' % (nstabledir, self._ident('file.table', self._table_id), self._table_class))

        if self._table_key_class:
            fh.write('from %s.%s import %s\n' % (
                nstabledir, self._ident('file.table', self._table_key_id), self._table_key_class))

        fh.write('\n')

        if 'LockOne' in self._std_procs:
            qry_name = self._ident('class.dao', '%sLockOne' % self._table_id)
            qry_file = self._ident('file.dao', '%sLockOne' % self._table_id)
            fh.write('from .%s import %s\n' % (qry_file, qry_name))

        if 'SelectOne' in self._std_procs:
            qry_name = self._ident('class.dao', '%sSelectOne' % self._table_id)
            qry_file = self._ident('file.dao', '%sSelectOne' % self._table_id)
            fh.write('from .%s import %s\n' % (qry_file, qry_name))

        if 'Update' in self._std_procs:
            qry_name = self._ident('class.dao', '%sUpdate' % self._table_id)
            qry_file = self._ident('file.dao', '%sUpdate' % self._table_id)
            fh.write('from .%s import %s\n' % (qry_file, qry_name))

        if 'Insert' in self._std_procs:
            qry_name = self._ident('class.dao', '%sInsert' % self._table_id)
            qry_file = self._ident('file.dao', '%sInsert' % self._table_id)
            fh.write('from .%s import %s\n' % (qry_file, qry_name))

        if 'DeleteOne' in self._std_procs:
            qry_name = self._ident('class.dao', '%sDeleteOne' % self._table_id)
            qry_file = self._ident('file.dao', '%sDeleteOne' % self._table_id)
            fh.write('from .%s import %s\n' % (qry_file, qry_name))

        if 'DeleteAll' in self._std_procs:
            qry_name = self._ident('class.dao', '%sDeleteAll' % self._table_id)
            qry_file = self._ident('file.dao', '%sDeleteAll' % self._table_id)
            fh.write('from .%s import %s\n' % (qry_file, qry_name))

        fh.write('\n')
        fh.write('class %s:\n\n' % self._doa_class)

        self._write_py_method(fh, None, '__init__',  'dbcon: mettle.db.%s' % (self._async['conn']))
        fh.write('        """\n')
        fh.write('        Constructor.\n\n')
        fh.write('        :param dbcon: Mettle database connection object.\n')
        fh.write('        """\n')
        fh.write('        self.rec    = %s()\n' % (self._table_class))
        fh.write('        self._dbcon = dbcon\n\n')

        fh.write('    def __enter__(self):\n')
        fh.write('        """\n')
        fh.write('        DAO enter.\n')
        fh.write('        """\n')
        fh.write('        return self\n\n')

        fh.write('    def __exit__(self, type, value, traceback):\n')
        fh.write('        """\n')
        fh.write('        DAO exit.\n')
        fh.write('        """\n')
        fh.write('        pass\n\n')

        if 'LockOne' in self._std_procs:
            qry_name = self._ident('class.dao', '%sLockOne' % self._table_id)
            lockArg = [Table.Column(True, self.SELECT_LOCK_ARG, 'int32', {'null': False})]
            expArg  = [Table.Column(True, '_expected', 'bool', {'null': False}, def_val = 'True')]

            # void DAO::lockOne()
            self._write_py_method(fh,
                                  'bool',
                                  self._ident_method('LockOne'),
                                  '%s: mettle.db.DBLock, _expected: bool = True' % (self.SELECT_LOCK_ARG),
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Lock and select the record.\n\n')
            fh.write('        :param %s: The db lock object to use.\n' % self.SELECT_LOCK_ARG)
            fh.write('        :param _expected: If set to false, will not raise if record is not found.\n')
            fh.write('        :return: True if selected, False if not found and _expected is set to False\n')
            fh.write('        """\n')
            fh.write('        _key = %s()\n\n' % (self._table_key_class))
            fh.write('        self.rec._write_key(_key)\n\n')
            fh.write('        return %sself.%s(_key, %s, _expected)\n\n' % (
                self._async['await'], self._ident_method('LockOneByKey'), self.SELECT_LOCK_ARG))

            self._write_py_method(fh,
                                  'bool',
                                  self._ident_method('LockOneWith'),
                                  '_rec: %s, %s: mettle.db.DBLock, _expected: bool = True' % (
                                      self._table_class, self.SELECT_LOCK_ARG),
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Lock and select the record using a record.\n\n')
            fh.write('        :param _rec: The table rec to select with and into.\n')
            fh.write('        :param %s: The db lock object to use.\n' % (self.SELECT_LOCK_ARG))
            fh.write('        :param _expected: If set to false, will not raise if record is not found.\n')
            fh.write('        :return: True if selected, False if not found and _expected is set to False\n')
            fh.write('        """\n')
            fh.write('        _key = %s()\n' % (self._table_key_class))
            fh.write('        _rec._write_key(_key)\n\n')
            fh.write('        %sself.%s(_key, %s, _expected)\n' % (
                self._async['await'], self._ident_method('LockOneByKey'), self.SELECT_LOCK_ARG))
            fh.write('        _rec._copy_from(self.rec)\n')
            fh.write('        return True\n\n')

            self._write_py_method(fh,
                                  'bool',
                                  self._ident_method('LockOneDeft'),
                                  self._table_key_columns + lockArg + expArg,
                                  method_descr = 'Attempt to lock and select the record by it\'s primary key columns.',
                                  can_async = True)
            fh.write('        _key = %s()\n\n' % (self._table_key_class))
            self._write_copy_args(fh, '_key.', self._table_key_columns, '')
            fh.write('\n')
            fh.write('        return %sself.%s(_key, %s, _expected)\n\n' % (
                self._async['await'], self._ident_method('LockOneByKey'), self.SELECT_LOCK_ARG))

            self._write_py_method(fh,
                                  'bool',
                                  self._ident_method('LockOneByKey'),
                                  '_key: %s, %s: mettle.db.DBLock, _expected: bool = True' % (
                                      self._table_key_class, self.SELECT_LOCK_ARG),
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Attempt to lock and select the record with it\'s primary key.\n\n')
            fh.write('        :param _key: Primary key of the table record.\n')
            fh.write('        :param %s: The db lock object to use.\n' % self.SELECT_LOCK_ARG)
            fh.write('        :param _expected: If set to false, will not raise if record is not found.\n')
            fh.write('        :return: True if selected, False if not found and _expected is set to False\n')
            fh.write('        """\n')
            fh.write('        with %s(self._dbcon) as _qry:\n' % qry_name)
            fh.write('            _dex = %s.retrys - 1 if %s.retrys > 0 else 0\n\n' % (
                self.SELECT_LOCK_ARG, self.SELECT_LOCK_ARG))
            fh.write('            while _dex >= 0:\n')
            fh.write('                try:\n')
            fh.write('                    %s_qry.exec(_key)\n' % self._async['await'])
            fh.write('                    if not %s_qry.fetch():\n' % self._async['await'])
            fh.write('                        if not _expected:\n')
            fh.write('                            return False\n\n')
            fh.write('                        raise mettle.lib.xMettle("LockOne failed to return a record (%s)")\n\n' % (
                self._doa_class))
            fh.write('                    break\n')
            fh.write('                except mettle.lib.xMettle as _x:\n')
            fh.write('                    if _x.get_error_code() != mettle.lib.xMettle.eCode.DBLockNoWaitFailed:\n')
            fh.write('                        raise _x\n\n')
            fh.write('                    if _dex == 0:\n')
            fh.write('                        raise mettle.lib.xMettle("Could not lock %s record after %s attempt(s) at %s'
                     ' mili second intervals!" %% (\n%s.retrys, %s.mili_seconds), errCode ='
                     ' mettle.lib.xMettle.eCode.DBLockNoWaitFailed)\n\n' % (
                         self._table_id, "%d", "%d", self.SELECT_LOCK_ARG, self.SELECT_LOCK_ARG))

            fh.write('                    if %s.mili_seconds > 0:\n' % self.SELECT_LOCK_ARG)
            if self._async['async']:
                fh.write('                        await asyncio.sleep(%s.mili_seconds * 0.001)\n' % self.SELECT_LOCK_ARG)
            else:
                fh.write('                        time.sleep(%s.mili_seconds * 0.001)\n' % self.SELECT_LOCK_ARG)
            fh.write('                _dex -= 1\n\n')
            fh.write('            self.rec = _qry.orec\n\n')
            fh.write('            return True\n\n')

        if 'SelectOne' in self._std_procs:
            qry_name = self._ident('class.dao', '%sSelectOne' % self._table_id)
            lockArg  = [Table.Column(True, self.SELECT_LOCK_ARG, 'int32', {'null': False})]

            # boolean DAO::trySelectOne()
            self._write_py_method(fh,
                                  'bool: True if row was selected',
                                  self._ident_method('TrySelectOne'),
                                  None,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Attempt to select the record.\n\n')
            fh.write('        :return: True if the record was found.\n')
            fh.write('        """\n')
            fh.write('        _key = %s()\n\n' % (self._table_key_class))
            fh.write('        self.rec._write_key(_key)\n\n')
            fh.write('        return %sself.%s(_key)\n\n' % (
                self._async['await'], self._ident_method('TrySelectOneByKey')))

            # boolean DAO::trySelectOneWith(Table)
            self._write_py_method(fh,
                                  'bool: True if row was selected',
                                  self._ident_method('TrySelectOneWith'),
                                  '_rec: %s' % self._table_class,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Attempt to select the record using a table rec.\n\n')
            fh.write('        :param _rec: The table rec to select with and into.\n')
            fh.write('        :return: True if the row as selectd.\n')
            fh.write('        """\n')
            fh.write('        _key = %s()\n' % (self._table_key_class))
            fh.write('        _rec._write_key(_key)\n\n')
            fh.write('        if not %sself.%s(_key):\n' % (
                self._async['await'], self._ident_method('TrySelectOneByKey')))
            fh.write('            return False\n\n')
            fh.write('        _rec._copy_from(self.rec)\n\n')
            fh.write('        return True\n\n')

            # boolean DAO::trySelectOneDeft(args)
            self._write_py_method(fh,
                                  'bool: True if the row as selectd.',
                                  self._ident_method('TrySelectOneDeft'),
                                  self._table_key_columns,
                                  method_descr = 'Attempt to select the record by it\'s primary key columns.',
                                  can_async = True)
            fh.write('        _key = %s()\n\n' % (self._table_key_class))
            self._write_copy_args(fh, '_key.', self._table_key_columns, '')
            fh.write('\n')
            fh.write('        return %sself.%s(_key)\n\n' % (
                self._async['await'], self._ident_method('TrySelectOneByKey')))

            # boolean DAO::trySelectOneByKey(TableKeyClass)
            self._write_py_method(fh,
                                  'bool',
                                  self._ident_method('TrySelectOneByKey'),
                                  '_key: %s' % self._table_key_class,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Attempt to select the record with it\'s primary key.\n\n')
            fh.write('        :param _key: Primary key of the table record.\n')
            fh.write('        :returns: True if row was selected.\n')
            fh.write('        """\n')
            fh.write('        with %s(self._dbcon) as _qry:\n' % qry_name)
            fh.write('            %s_qry.exec(_key)\n' % self._async['await'])
            fh.write('            if not %s_qry.fetch():\n' % self._async['await'])
            fh.write('                return False\n\n')
            fh.write('            self.rec = _qry.orec\n\n')
            fh.write('        return True\n\n')

            # void DAO::SelectOne()
            self._write_py_method(fh,
                                  '"%s"' % self._doa_class,
                                  self._ident_method('SelectOne'),
                                  None,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Selects the record, raises and error if it does not exist.\n\n')
            fh.write('        :return: Self for convenience.\n')
            fh.write('        """\n')
            fh.write('        if not %sself.%s():\n' % (
                self._async['await'], self._ident_method('TrySelectOne')))
            fh.write('            raise mettle.lib.xMettle("SelectOne failed to return a record (%s)")\n\n' % (self._doa_class))
            fh.write('        return self\n\n')

            # boolean DAO::selectOneWith(TableClass)
            self._write_py_method(fh,
                                  '"%s"' % self._doa_class,
                                  self._ident_method('SelectOneWith'),
                                  '_rec: %s' % self._table_class,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Attempt to select the record with the table record.\n\n')
            fh.write('        :param _rec: Table record.\n')
            fh.write('        :returns: Self for convenience.\n')
            fh.write('        """\n')
            fh.write('        if not %sself.%s(_rec):\n' % (
                self._async['await'], self._ident_method('TrySelectOneWith')))
            fh.write('            raise mettle.lib.xMettle("SelectOne failed to return a record (%s)")\n\n' % (self._doa_class))
            fh.write('        return self\n\n')

            self._write_py_method(
                fh,
                '"%s"' % self._doa_class,
                self._ident_method('SelectOneDeft'),
                self._table_key_columns,
                method_descr = 'Selects the record by its primary key columns, raises and error if it does not exist.',
                can_async = True)
            fh.write('        _key = %s()\n\n' % (self._table_key_class))
            self._write_copy_args(fh, '_key.', self._table_key_columns, '')
            fh.write('\n')
            fh.write('        if not %sself.%s(_key):\n' % (
                self._async['await'], self._ident_method('TrySelectOneByKey')))
            fh.write('            raise mettle.lib.xMettle("SelectOne failed to return a record (%s)")\n\n' % (self._doa_class))
            fh.write('        return self\n\n')

            # boolean DAO::selectOneByKey(TableKeyClass)
            self._write_py_method(fh,
                                  '"%s"' % self._doa_class,
                                  self._ident_method('SelectOneByKey'),
                                  '_key: %s' % self._table_key_class,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Attempt to select the record with it\'s primary key.\n\n')
            fh.write('        :param _key: Primary key of the table record.\n')
            fh.write('        :return: Self for convenience.\n')
            fh.write('        """\n')
            fh.write('        if not %sself.%s(_key):\n' % (
                self._async['await'], self._ident_method('TrySelectOneByKey')))
            fh.write('            raise mettle.lib.xMettle("SelectOne failed to return a record (%s)")\n\n' % (self._doa_class))
            fh.write('        return self\n\n')

        if 'Update' in self._std_procs:
            qry_name = self._ident('class.dao', '%sUpdate' % self._table_id)

            # void DAO::Update(args)
            upd_ignore_types = ['timestamp']
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('UpdateDeft'),
                                  self._gen_info['table'].columns,
                                  ignore_types = upd_ignore_types,
                                  method_descr = 'Update the record by setting all column values.',
                                  can_async = True)
            self._write_copy_args(fh, 'self.rec.', self._gen_info['table'].columns, '', upd_ignore_types)
            fh.write('\n        %sself.update()\n\n' % self._async['await'])

            # void DAO::Update()
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('update'),
                                  'irec: %s = None' % self._table_class,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Update the record in the database with the record or irec if it is not None.\n\n')
            fh.write('        :param irec: If not None use this record to update the database.\n')
            fh.write('        """\n')
            fh.write('        if irec:\n')
            fh.write('            self.rec._copy_from(irec)\n\n')
            fh.write('        with %s(self._dbcon) as _qry:\n' % (qry_name))
            fh.write('            %s_qry.exec(self.rec)\n\n' % self._async['await'])
            fh.write('        if irec:\n')
            fh.write('            irec._copy_from(self.rec)\n\n')

        if 'Insert' in self._std_procs:
            qry_name = self._ident('class.dao', '%sInsert' % self._table_id)

            # void DAO::Insert(args)
            upd_ignore_types = ['seq32', 'seq64', 'timestamp']
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('InsertDeft'),
                                  self._gen_info['table'].columns,
                                  ignore_types = upd_ignore_types,
                                  method_descr = 'Insert the record setting all column values.',
                                  can_async = True)
            self._write_copy_args(fh, 'self.rec.', self._gen_info['table'].columns, '', upd_ignore_types)
            fh.write('\n        %sself.insert()\n\n' % self._async['await'])

            # void DAO::Insert()
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('Insert'),
                                  'irec: %s = None' % self._table_class,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Insert the record in the database with the record or irec if it is not None.\n\n')
            fh.write('        :param irec: If not None use this record to insert into the database.\n')
            fh.write('        """\n')
            fh.write('        if irec:\n')
            fh.write('            self.rec._copy_from(irec)\n\n')
            fh.write('        with %s(self._dbcon) as _qry:\n' % (qry_name))
            fh.write('            %s_qry.exec(self.rec)\n\n' % self._async['await'])
            fh.write('        if irec:\n')
            fh.write('            irec._copy_from(self.rec)\n\n')

        if 'DeleteOne' in self._std_procs:
            qry_name = self._ident('class.dao', '%sDeleteOne' % self._table_id)

            # void DAO::DeleteOne(args)
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('DeleteOneDeft'),
                                  self._table_key_columns,
                                  method_descr = 'Delete one record by it\'s primary key columns.',
                                  can_async = True)
            fh.write('        _key = %s()\n\n' % (self._table_key_class))
            self._write_copy_args(fh, '_key.', self._table_key_columns, '')
            fh.write('\n        self.%s(_key)\n\n' % self._ident_method('deleteOne'))

            # void DAO::DeleteOne(*TableKeyClass = 0)
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('DeleteOne'),
                                  'irec: %s = None' % self._table_key_class,
                                  can_async = True)
            fh.write('        """\n')
            fh.write('        Delete the record by its primary key or irec if it is not None.\n\n')
            fh.write('        :param irec: If not None use this record to delete record.\n')
            fh.write('        """\n')
            fh.write('        _key = %s()\n\n' % (self._table_key_class))
            fh.write('        if irec:\n')
            fh.write('            _key._copy_from(irec)\n')
            fh.write('        else:\n')
            fh.write('            self.rec._write_key(_key)\n\n')
            fh.write('        with %s(self._dbcon) as _qry:\n' % (qry_name))
            fh.write('            %s_qry.exec(_key)\n\n' % self._async['await'])

        if 'DeleteAll' in self._std_procs:
            qry_name = self._ident('class.dao', '%sDeleteAll' % self._table_id)

            # void DAO::DeleteAll()
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('DeleteAll'),
                                  None,
                                  method_descr = 'Delete all the records in the database.',
                                  can_async = True)
            fh.write('        with %s(self._dbcon) as _qry:\n' % (qry_name))
            fh.write('            %s_qry.exec()\n\n' % self._async['await'])

        self.gened_file_close(fh)


    def _gen_standard_procs(self):
        for proc in self._std_procs:
            if proc == 'Insert':
                self._write_sql_proc_dao(self._std_procs['Insert'], [], False, True)
            elif proc == 'Update':
                self._write_sql_proc_dao(self._std_procs['Update'], ['timestamp'], True)
            else:
                self._write_sql_proc_dao(self._std_procs[proc])


    def _gen_custom_procs(self):
        for proc in self._gen_info['table'].procs:
            if self._mode == self.TABLE:
                if proc.in_fields:
                    if len(proc.in_fields) != 1 or proc.in_fields[0].type != 'dbrec':
                        self._write_data_class('%s%s' % (
                            self._table_id, proc.name), proc.in_fields)

                if proc.out_fields:
                    if len(proc.out_fields) != 1 or proc.out_fields[0].type != 'dbrec':
                        self._write_data_class('%s%s' % (self._table_id, proc.name),
                                               proc.out_fields,
                                               out_obj=True)
            elif self._mode == self.DAO:
                self._write_sql_proc_dao(proc)


    def _gen_dao_init_file(self):
        nsdir    = self.proj_relative_path(self._gen_info, self.dest_dir(os.path.sep))
        ns       = self._namespace()
        fh       = None
        nsdaodir = os.path.join(nsdir, self.get_dao_dir_name(), self._gen_info['database'].dbname)

        if not os.path.exists(nsdaodir):
            raise Exception('Namespace directory not found [%s]' % nsdaodir)

        ns_file = os.path.join(nsdaodir, '__init__.py')
        fh      = open(ns_file, 'wt')

        self._add_headers(fh)

        for gf in self._gened_files[ns]:
            fh.write('from .%s import %s\n' % (
                gf.fname, gf.cls))

        fh.close()
