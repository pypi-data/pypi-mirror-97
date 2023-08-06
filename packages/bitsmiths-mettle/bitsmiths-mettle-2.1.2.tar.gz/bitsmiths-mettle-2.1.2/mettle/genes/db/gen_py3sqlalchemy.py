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
# from .table     import Table


class GenPy3SqlAlchemy(Generator):

    SELECT_LOCK_ARG  = '_lockForUpdate'

    def __init__(self):
        Generator.__init__(self, ['py'])
        self.targ_type  = 'code'
        self.namespace = None

        self._field_map['bool']      = Generator.FieldMap('Boolean',            type_flag = 'bool',     def_value = 'False')
        self._field_map['int8']      = Generator.FieldMap('SmallInteger',       type_flag = 'int',      def_value = '0')
        self._field_map['int16']     = Generator.FieldMap('Integer',            type_flag = 'int',      def_value = '0')
        self._field_map['int32']     = Generator.FieldMap('Integer',            type_flag = 'int',      def_value = '0')
        self._field_map['int64']     = Generator.FieldMap('Integer',            type_flag = 'int',      def_value = '0')
        self._field_map['seq32']     = Generator.FieldMap('Integer',            type_flag = 'int',      def_value = '0')
        self._field_map['seq64']     = Generator.FieldMap('Integer',            type_flag = 'int',      def_value = '0')
        self._field_map['char']      = Generator.FieldMap('String(1)',          type_flag = 'str',      def_value = "''")
        self._field_map['string']    = Generator.FieldMap('String',             type_flag = 'str',      def_value = "''")
        self._field_map['uuid']      = Generator.FieldMap('UUID(as_uuid=True)', type_flag = 'uuid',     def_value = "None")
        self._field_map['date']      = Generator.FieldMap('Date',               type_flag = 'date',     def_value = '?')
        self._field_map['time']      = Generator.FieldMap('Time',               type_flag = 'date',     def_value = '?')
        self._field_map['datetime']  = Generator.FieldMap('DateTime',           type_flag = 'date',     def_value = '?')
        self._field_map['timestamp'] = Generator.FieldMap('DateTime',           type_flag = 'date',     def_value = '?')
        self._field_map['memblock']  = Generator.FieldMap('LargeBinary',        type_flag = 'memblock', def_value = "?")
        self._field_map['double']    = Generator.FieldMap('Float',              type_flag = 'double',   def_value = '0.0')
        self._field_map['json']      = Generator.FieldMap('JSON',               type_flag = 'json',     def_value = "''")
        self._field_map['dynamic']   = Generator.FieldMap('String',             type_flag = 'str',      def_value = "''")
        self._field_map['dbrec']     = Generator.FieldMap('?',                  type_flag = 'dbrec',    def_value = 'None')

        self._init_code_options()
        self._init_casing({
            'class'  : 'pascal',
            'method' : 'snake',
            'member' : 'snake',
            'file'   : 'snake',
        })


    def name(self):
        return 'Python3SqlAlchemy'


    def initialize_generation(self, gen_info):
        pass


    def finalize_generation(self, gen_info):
        """
        Create all the __init__.py files in the namespace directories.
        """
        if gen_info['clean']:
            return

        nap    = gen_info['proj'].project_dir
        nsdir  = os.path.join(nap, self.dest_dir()).replace('\\', os.path.sep)\
                                                   .replace('/', os.path.sep)\
                                                   .replace('|', os.path.sep)
        ns     = self._namespace()
        fh     = None
        nsFile = os.path.join(nsdir, '__init__.py')
        fh     = open(nsFile, 'wt')
        tbldir = self.get_option('dir.tables')

        self._add_headers(fh)
        fh.close()

        nstabledir = os.path.join(nsdir, tbldir)

        if not os.path.exists(nstabledir):
            print('- warning, namespace directory (%s) not found' % nstabledir)
            return

        nsFile = os.path.join(nstabledir, '__init__.py')
        fh     = open(nsFile, 'wt')

        self._add_headers(fh)

        for gf in self._gened_files[ns]:
            fh.write('from .%s import %s\n' % (gf.fname, gf.cls))

        fh.close()


    def _add_headers(self, fh):
        if self._mode == self.TABLE:
            message = '# This file was generated by mettle.genes.db.%s [ver %s] on %s\n\n' % (
                self.name(), self._gen_info['version'], time.asctime())
        else:
            message = '# This file was generated by mettle.genes.db.%s [ver %s] on %s\n#  Target Database = %s\n\n' % (
                self.name(), self._gen_info['version'], time.asctime(), self._gen_info['database'].dbname)

        fh.write(message)


    def _member(self, mem):
        return self._ident_member(mem)


    def generate_tables(self, gen_info):
        self._mode     = self.TABLE
        self._targetDB = 'tables'
        self._generate(gen_info)


    def generate_daos(self, gen_info, targetDB):
        self._mode     = self.DAO
        self._targetDB = targetDB
        self._generate(gen_info)


    def _generate(self, gen_info):

        if gen_info['clean']:
            if self._mode == self.DAO:
                self.clean(gen_info, os.path.join('dao', self._targetDB))
            else:
                self.clean(gen_info, self._targetDB)

            return

        self._gen_info         = gen_info
        self.namespace        = self._namespace()
        self._table_class      = self._ident('class.table', self._gen_info['table'].name)
        # self._table_key_class   = None
        self._table_key_columns = self._gen_info['table'].primary_key_columns()
        self._stdProcs        = self._build_standard_procs(self._gen_info)

        if len(self._table_key_columns) > 0:
            self._table_key_class = self._ident('class.table', '%sKey' % self._gen_info['table'].name)

        if self._mode == self.TABLE:
            self._write_model_class(self._table_class, self._gen_info['table'].columns)


    def _write_model_class(self, cls, columns):
        if not columns:
            return

        fh = self.gened_file_open(self._gen_info,
                                  self._ident('file.table', self._gen_info['table'].name),
                                  extra_dir=self.get_option('dir.tables'),
                                  cls=cls,
                                  add_namespace_to_path=False)

        self._add_headers(fh)
        self._gen_model_headers(fh, columns, self._gen_info['table'].foreign_keys)
        self._gen_model_fk_imports(fh, self._gen_info['table'].foreign_keys)

        fh.write('Base = declarative_base()\n\n')

        fh.write('class %s(Base):\n\n' % (cls))
        fh.write('    __tablename__ = "%s"\n\n' % (self._gen_info['table'].name.lower()))

        self._write_member_decleration(fh,
                                       columns,
                                       self._gen_info['table'].primary_key_columns(),
                                       self._gen_info['table'].foreign_keys)

        self._write_repr_method(fh, columns)
        self._write_couplets(fh, cls, columns)
        self._write_std_procs(fh, cls, columns)

        self.gened_file_close(fh)


    def _gen_model_headers(self, fh, columns, foreign_keys):
        has_uuid = False

        for col in columns:
            if col.type == 'uuid':
                has_uuid = True
                break

        fh.write('import sqlalchemy\n')

        if foreign_keys:
            fh.write('import sqlalchemy.orm\n')

        if has_uuid:
            fh.write('import uuid\n')

        if 'LockOne' in self._stdProcs:
            fh.write('import mettle.db\n')

        fh.write('import mettle.lib\n')


        fh.write('\n')

        for col in columns:
            if col.type == 'uuid':
                fh.write('\nfrom sqlalchemy.dialects.postgresql import UUID\n')
                break

        fh.write('from sqlalchemy.ext.declarative import declarative_base\n')


    def _gen_model_fk_imports(self, fh, foreign_keys: list):
        if not foreign_keys:
            return

        # cnt = 0

        # for fk in self._gen_info['table'].foreign_keys:
        #     if fk.refTable == self._gen_info['table'].name:
        #         continue

        #     if not cnt:
        #         fh.write('\n')

        #     cnt += 1

        #     fh.write('\nfrom %s.%s.%s import %s' % (
        #         self.namespace,
        #         self.get_option('dir.tables'),
        #         self._ident('file.table', fk.refTable),
        #         self._ident('class.table', fk.refTable)))


    def _write_member_decleration(self, fh, members, primary_keys: list, foreign_keys: list):
        if not members:
            return

        for m in members:
            fmap  = self._field_map[m.type]
            pre   = '' if m.type == 'uuid' else 'sqlalchemy.'

            fh.write("    %s = sqlalchemy.Column('%s', %s%s" % (
                self._member(m.name), m.name.lower(), pre, fmap.name))

            if m.length:
                fh.write('(%d)' % m.length)

            fh.write(', nullable=%s' % str(not m.not_null))

            for pk in primary_keys:
                if m.name in pk.name:
                    fh.write(', primary_key=True, index=True')
                    break

            if m.type == 'uuid':
                fh.write(', default=uuid.uuid4')
            elif m.type == 'timestamp':
                fh.write(', default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()')

            fh.write(')\n')

        # if foreign_keys:
        #     fh.write('\n')

        #     for fk in foreign_keys:
        #         fh.write('\n    _%s = ' % self._member('rel_%s' % fk.name))
        #         fh.write('sqlalchemy.orm.relationship("%s", foreign_keys=[' % (fk.refTable.lower()))

        #         comma = ''

        #         for colidx in fk.columns:
        #             fh.write('%s%s' % (comma, self._member(self._gen_info['table'].columns[colidx].name)))
        #             comma = ', '

        #         fh.write('])')

        fh.write('\n\n')


    def _write_repr_method(self, fh, args):
        fh.write('    def __repr__(self):\n')
        fh.write("        return '<%s [" % self._gen_info['table'].name)

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

            fh.write('\n\n    class %s(dict):\n' % cpCls)

            if fmap.type_flag in ('str', 'json'):
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
                fh.write('            self[self.%s] = self.%s\n' % (self._ident_member('Key%s' % cname),
                                                                    self._ident_member('Value%s' % cname)))
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


    def _write_std_procs(self, fh, cls, columns):

        if 'LockOne' in self._stdProcs:
            # qryName = self._ident('class.dao', '%sLockOne' % self._gen_info['table'].name)
            # fh.write('from %s.%s import %s\n' % (self.namespacedao, qryName, qryName))
            pass

        if 'SelectOne' in self._stdProcs:
            self._write_py_method(fh,
                                  None,
                                  self._ident_method('TrySelectOne'),
                                  self._table_key_columns,
                                  is_static=True,
                                  static_args='dbs')
            fh.write('        return dbs.query(%s).filter_by(' % cls)

            comma = ''

            for col in self._table_key_columns:
                mname = self._member(col.name)
                fh.write('%s%s=%s' % (comma, mname, mname))
                comma = ', '

            fh.write(').first()\n\n')

            self._write_py_method(fh,
                                  None,
                                  self._ident_method('SelectOne'),
                                  self._table_key_columns,
                                  is_static=True,
                                  static_args='dbs')
            fh.write('        res = %s.%s(dbs' % (cls, self._ident_method('TrySelectOne')))
            self._write_arguements(fh, self._table_key_columns, 0, comments=False)
            fh.write(')\n\n')
            fh.write('        if not res:\n')
            fh.write("            raise mettle.lib.xMettle('SelectOne failed to return a record <%s: %r>' % (")
            fh.write('%s.__tablename__, (' % (cls))
            self._write_arguements(fh, self._table_key_columns, 0, comments=False, comma = '')
            fh.write(')))\n\n')
            fh.write('        return res\n')


        if 'SelectAll' in self._stdProcs:
            self._write_py_method(fh, None, self._ident_method('SelectAll'), is_static=True, static_args='dbs')
            fh.write('        return dbs.query(%s).all()\n' % cls)


        if 'Update' in self._stdProcs:
            self._write_py_method(fh, None, self._ident_method('Update'), 'dbs, vals: dict')
            fh.write('        dbs.query(%s).filter('  % cls)

            comma = ''

            for col in self._table_key_columns:
                mname = self._member(col.name)
                fh.write('%s%s.%s == self.%s' % (comma, cls, mname, mname))
                comma = ', '

            fh.write(').update(vals)\n')

        if 'Insert' in self._stdProcs:
            self._write_py_method(fh, None, self._ident_method('Insert'), 'dbs', is_static=True)
            fh.write('        dbs.add(self)\n')

        if 'DeleteOne' in self._stdProcs:
            self._write_py_method(fh, None, self._ident_method('Delete'), 'dbs')
            fh.write('        dbs.delete(self)\n')

            self._write_py_method(fh,
                                  None,
                                  self._ident_method('DeleteOne'),
                                  self._table_key_columns,
                                  is_static=True,
                                  static_args='dbs')
            fh.write('        res = %s.%s(' % (cls, self._ident_method('TrySelectOne')))
            self._write_arguements(fh, self._table_key_columns, 0, comments=False, comma = '')
            fh.write(')\n\n')
            fh.write('        if res:\n')
            fh.write('            dbs.delete(res)\n')

        if 'DeleteAll' in self._stdProcs:
            self._write_py_method(fh, None, self._ident_method('DeleteAll'), is_static=True, static_args='dbs')
            fh.write('        # Delete all rows in table, returns number of rows delted\n')
            fh.write('        return dbs.query(%s).delete()\n' % cls)


        #     ,.filter(PaymentBatch.id == self.id).update(vals)

        # if with_lock:
        #     res = dbs.query(PaymentBatch).filter_by(id=batch_id).with_for_update().first()
        # else:
        #     res = dbs.query(PaymentBatch).filter_by(id=batch_id).first()

        # if must_exist and res == None:
        #     raise errors.InvalidParameterError('Payment not found [batch_id:%d]' % batch_id)

        # return res




    def _write_py_method(self,
                         fh,
                         returns,
                         method,
                         args=None,
                         ignore_types=[],
                         extra_spaces='',
                         use_default_vals=False,
                         method_descr=None,
                         is_static=False,
                         static_args=None):
        if is_static:
            fh.write('\n    %s@staticmethod' % (extra_spaces))
            cstr  = '    %sdef %s(%s' % (extra_spaces, method, static_args or '')
            comma = ', ' if static_args else ''
        else:
            cstr  = '    %sdef %s(self' % (extra_spaces, method)
            comma = ', '

        fh.write('\n')
        fh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguements(fh, args, len(cstr), ignore_types, use_default_vals=use_default_vals, comma = comma)
            elif type(args) == str:
                fh.write(comma)
                fh.write(args)

        fh.write('):\n')

        if method_descr:
            fh.write('        %s"""\n' % extra_spaces)
            fh.write('        %s%s\n' % (extra_spaces, method_descr))

            if type(args) == list:
                self._write_arguements(fh, args, len(cstr), ignore_types, comments = True, extra_spaces=extra_spaces)
            elif type(args) == str:
                arr   = args.split(',')
                for a in arr:
                    eq = a.split('=')
                    kp = eq[0].strip().split(' ')
                    fh.write('        %s:param %s: %s\n' % (extra_spaces, kp[0], kp[1]))

            if returns:
                fh.write('        %s:return: %s\n' % (extra_spaces, returns))

            fh.write('        %s"""\n'  % extra_spaces)


    def _write_arguements(self,
                          fh,
                          args,
                          spacing,
                          filter_out=None,
                          comments=False,
                          extra_spaces='',
                          use_default_vals=False,
                          comma=None):
        if not args:
            return

        nulls = []

        if comma is None:
            comma = ', '

        for a in args:
            if filter_out:
                if a.type in filter_out:
                    continue

            fmap = self._field_map[a.type]

            if a.name == self.SELECT_LOCK_ARG:
                if a.type == 'int32':
                    if comments:
                        fh.write("        %s:param %s: (%s) The db lock object to use. \n" % (
                            extra_spaces, self._member(a.name), 'mettle.db.DBLock'))
                    else:
                        fh.write('%s%s'  % (comma, a.name))
                else:
                    raise Exception('Unexpected code path')

                continue

            if comments:
                if a.type == 'dbrec':
                    paramComment = a.lookup
                else:
                    paramComment = ''

                fh.write("        %s:param %s: %s %s\n" % (extra_spaces, self._member(a.name), fmap.name, paramComment))

            else:
                fh.write('%s%s' % (comma, self._member(a.name)))

                if use_default_vals:
                    fh.write('=%s' % fmap.def_value)

                if a.type.startswith('int') and a.not_null is False:
                    nulls.append(a)

        for a in nulls:
            if comments:
                fh.write("        %s:param %s: (bool) the column value is null.\n" % (
                    extra_spaces, '%s_NULL' % self._member(a.name)))
            else:
                fh.write('%s%s' % (comma, '%s_NULL=False' % self._member(a.name)))
