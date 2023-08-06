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


class GenTS(Generator):

    def __init__(self):
        Generator.__init__(self, ['ts'])
        self.targ_type  = 'code'
        self.namespace  = ''  # default to '' as we don't require a namespace for typescript we should structure with folders

        self._field_map['bool']      = Generator.FieldMap('boolean', type_flag = 'bool',     def_value = 'false')
        self._field_map['int8']      = Generator.FieldMap('number',  type_flag = 'int',      def_value = '0')
        self._field_map['int16']     = Generator.FieldMap('number',  type_flag = 'int',      def_value = '0')
        self._field_map['int32']     = Generator.FieldMap('number',  type_flag = 'int',      def_value = '0')
        self._field_map['int64']     = Generator.FieldMap('number',  type_flag = 'int',      def_value = '0')
        self._field_map['seq32']     = Generator.FieldMap('number',  type_flag = 'int',      def_value = '0')
        self._field_map['seq64']     = Generator.FieldMap('number',  type_flag = 'int',      def_value = '0')
        self._field_map['char']      = Generator.FieldMap('string',  type_flag = 'str',      def_value = "''")
        self._field_map['string']    = Generator.FieldMap('string',  type_flag = 'str',      def_value = "''")
        self._field_map['date']      = Generator.FieldMap('Date',    type_flag = 'date',     def_value = 'undefined')
        self._field_map['time']      = Generator.FieldMap('Date',    type_flag = 'date',     def_value = 'undefined')
        self._field_map['datetime']  = Generator.FieldMap('Date',    type_flag = 'date',     def_value = 'undefined')
        self._field_map['timestamp'] = Generator.FieldMap('Date',    type_flag = 'date',     def_value = 'undefined')
        self._field_map['memblock']  = Generator.FieldMap('string',  type_flag = 'memblock', def_value = 'undefined')
        self._field_map['uuid']      = Generator.FieldMap('string',  type_flag = 'str',      def_value = "''")
        self._field_map['json']      = Generator.FieldMap('string',  type_flag = 'str',      def_value = "''")
        self._field_map['double']    = Generator.FieldMap('number',  type_flag = 'double',   def_value = '0.0')
        self._field_map['dynamic']   = Generator.FieldMap('string',  type_flag = 'str',      def_value = "''")
        self._field_map['dbrec']     = Generator.FieldMap('struct',  type_flag = 'dbrec',    def_value = 'undefined')

        self._init_code_options()
        self._init_casing({ 'class': 'pascal', 'method': 'camel', 'member': 'camel', 'file': 'pascal' })


    def name(self):
        return 'TypeScript'


    def initialize_generation(self, gen_info):
        pass


    def finalize_generation(self, gen_info):
        """!
        Create the index.ts file for the generated code.
        """
        if gen_info['clean']:
            return

        nap    = gen_info['proj'].project_dir
        nsdir  = os.path.join(nap, self.dest_dir()).replace('\\', os.path.sep)\
                                                   .replace('/', os.path.sep)\
                                                   .replace('|', os.path.sep)
        ns     = self._namespace()
        fh     = None

        nstabledir = os.path.join(nsdir, 'tables')

        if not os.path.exists(nstabledir):
            print('- warning, namespace directory (%s) not found' % nstabledir)
            return

        nsFile = os.path.join(nstabledir, 'index.ts')
        fh     = open(nsFile, 'wt')

        self._add_headers(fh)

        for gf in self._gened_files[ns]:
            fh.write("export * from './%s';\n" % (gf.cls))

        fh.close()


    def generate_tables(self, gen_info):
        self._mode     = self.TABLE
        self._targetDB = 'tables'
        self._generate(gen_info)


    def generate_daos(self, gen_info, targetDB):
        pass


    def _namespace(self, speSep = None, blankOK = False, baseOnly = False):
        return self._namespace


    def _generate(self, gen_info):
        if gen_info['clean']:
            if self._mode == self.TABLE:
                self.clean(gen_info, self._targetDB)

            return

        if self._mode != self.TABLE:
            return

        self._gen_info        = gen_info
        self._table_class     = None
        self._table_key_class = None

        self._gen_table_key_class()
        self._gen_table_class()

        self._gen_custom_procs()


    def _add_headers(self, fh):
        if self._mode != self.TABLE:
            return

        fh.write('/* This file was generated by mettle.genes.db.GenTS [ver %s] on %s */\n\n' % (
            self._gen_info['version'], time.asctime()))


    def _gen_headers(self, fh, main_class: bool, key_class: bool, cls: str):
        fh.write("import { Reader }        from '@bitsmiths/mettle-io';\n")
        fh.write("import { Writer }        from '@bitsmiths/mettle-io';\n")
        fh.write("import { ISerializable } from '@bitsmiths/mettle-io';\n")

        if main_class and self._table_key_class:
            fh.write("import { IPrimaryKey }   from '@bitsmiths/mettle-db';\n")
            fh.write("\n")
            fh.write("import { %s } from './%s';\n" % (
                self._ident('class.table', '%sKey' % self._table_id),
                self._ident('file.table', '%sKey' % self._table_id)))

        fh.write('\n')

        import_set = set()

        for proc in self._gen_info['table'].procs:
            if self._mode == self.TABLE:
                for field in proc.in_fields:
                    if field.type == 'dbrec' and self._lookup_name(field.lookup, 'imports'):
                        cname = self._ident('class.table', self._lookup_name(field.lookup, 'imports'))

                        if cname == cls:
                            continue

                        import_set.add(self._lookup_name(field.lookup, 'imports'))

                for field in proc.out_fields:
                    if field.type == 'dbrec' and self._lookup_name(field.lookup, 'imports'):
                        cname = self._ident('class.table', self._lookup_name(field.lookup, 'imports'))

                        if cname == cls:
                            continue

                        import_set.add(self._lookup_name(field.lookup, 'imports'))


        for imp in import_set:
            if not imp:
                continue

            fh.write("import { %s } from './%s';\n" % (
                self._ident('class.table', imp),
                self._ident('file.table',  imp)))

        fh.write('\n')


    def _gen_trailers(self, fh):
        pass


    def _gen_table_key_class(self):
        self._table_key_class   = None
        self._table_key_columns = self._gen_info['table'].primary_key_columns()

        if len(self._table_key_columns) < 1:
            return

        self._table_id         = self._gen_info['table'].name
        self._table_key_class  = self._ident('class.table', '%sKey' % self._table_id)

        self._write_data_class(self._table_key_class,
                               self._table_key_columns,
                               self._ident('file.table', '%sKey' % self._table_id),
                               key_class = True)


    def _gen_table_class(self):
        self._table_id    = self._gen_info['table'].name
        self._table_class = self._ident('class.table', self._table_id)
        self._write_data_class(self._table_class,
                               self._gen_info['table'].columns,
                               self._ident('file.table', self._table_id),
                               main_class = True)


    def _member(self, mem):
        return self._ident_member(mem)


    def _write_data_class(self, cls: str, columns: list, file_ident: str, main_class = False, key_class = False):
        if columns is None or len(columns) < 1:
            return

        ext_dir = 'tables'

        fh  = self.gened_file_open(self._gen_info,
                                   file_ident,
                                   extra_dir = ext_dir,
                                   add_namespace_to_path=False)

        tbl = self._gen_info['table']

        self._add_headers(fh)

        self._gen_headers(fh, main_class, key_class, cls)

        fh.write('export class %s extends ISerializable%s {\n\n' % (
            cls, ' implements IPrimaryKey' if main_class and len(tbl.primary_keys) > 0 else ''))

        # member variables
        self._write_member_declaration(fh, columns)

        # constructor
        fh.write('  /**\n')
        fh.write('   * Constructor.\n')
        fh.write('   */\n')
        self._write_ts_method(fh, None, 'constructor', '')
        fh.write('   super();\n')
        fh.write('  }\n\n')

        # _init copy constructor
        fh.write('  /**\n')
        fh.write('   * Initialize with record.\n')
        fh.write('   * @param rec  The to copy from.\n')
        fh.write('   */\n')
        self._write_ts_method(fh, None, '_init', 'rec: %s' % cls)
        self._write_copy_args(fh, 'this.', columns, 'rec.')
        fh.write('  }\n\n')

        # Struct.Struct()
        fh.write('  /**\n')
        fh.write('   * Deft Initialization.\n')
        self._write_arguements(fh, columns, '', ['timestamp'], comments=True)
        fh.write('   */\n')
        self._write_ts_method(fh, cls, '_initDeft', columns, ['timestamp'])
        self._write_copy_args(fh, 'this.', columns, '', ['timestamp'])
        fh.write('\n    return this;\n')
        fh.write('  }\n\n')

        # string Table::_Name()
        self._write_ts_method(fh, 'string', '_name', None)

        if main_class:
            fh.write("    return '%s';\n  }\n\n" % tbl.name)
        elif key_class:
            fh.write("    return '%sKey';\n  }\n\n" % tbl.name)
        else:
            fh.write("    return '%s';\n  }\n\n" % cls)

        # void clear()
        self._write_ts_method(fh, None, '_clear', None,)
        self._write_clear_fields(fh, columns)
        fh.write('  }\n\n')

        fh.write('  /**\n')
        fh.write('   * Serialize the object with a writer.\n')
        fh.write('   * @param _w      The writer object to use.\n')
        fh.write('   * @param _oname  Optionally pass in a diff name for the object.\n')
        fh.write('   */\n')
        self._write_ts_method(fh, None, '_serialize', '_w: Writer, _oname?: string')
        fh.write('    if (_oname === undefined)\n')
        fh.write('      _oname = this._name();\n\n')
        fh.write('    _w.writeStart(_oname);  if (_w._prom.broken()) return;\n\n')

        for a in columns:
            if a.type in ('int32', 'int64', 'int16', 'int8', 'uint32', 'uint64', 'uint16', 'uint8', 'seq32', 'seq64'):
                fh.write('    _w.writeInt("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('string', 'dynamic', 'uuid', 'json'):
                fh.write('    _w.writeString("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('char'):
                fh.write('    _w.writeChar("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('bool'):
                fh.write('    _w.writeBool("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('double'):
                fh.write('    _w.writeFloat("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('memblock'):
                fh.write('     _w.writeByteArray("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('datetime', 'timestamp'):
                fh.write('    _w.writeDateTime("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('date'):
                fh.write('    _w.writeDate("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('time'):
                fh.write('    _w.writeTime("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('dbrec', 'this'):
                fh.write('    this.%s._serialize(_w);' % (self._member(a.name)))
            else:
                raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))

            fh.write('  if (_w._prom.broken()) return;\n')

        fh.write('\n    _w.writeEnd(_oname);  if (_w._prom.broken()) return;\n')
        fh.write('  }\n\n')

        # Struct._deserialize()
        fh.write('  /**\n')
        fh.write('   * Deserialize the object with a reader.\n')
        fh.write('   * @param _r      The reader object to use.\n')
        fh.write('   * @param _oname  Optionally pass in a diff name for the object.\n')
        fh.write('   */\n')
        self._write_ts_method(fh, None, '_deserialize', '_r: Reader, _oname?: string')
        fh.write('    if (_oname === undefined)\n')
        fh.write('      _oname = this._name();\n\n')
        fh.write('    _r.readStart(_oname);  if (_r._prom.broken()) return;\n\n')

        for a in columns:
            if a.type in ('int32', 'int64', 'int16', 'int8', 'uint32', 'uint64', 'uint16', 'uint8', 'seq32', 'seq64'):
                fh.write('    this.%s = _r.readInt("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('string', 'dynamic', 'uuid', 'json'):
                fh.write('    this.%s = _r.readString("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('char'):
                fh.write('    this.%s = _r.readChar("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('bool'):
                fh.write('    this.%s = _r.readBool("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('double'):
                fh.write('    this.%s = _r.readFloat("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('memblock'):
                fh.write('    this.%s = _r.readByteArray("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('datetime', 'timestamp'):
                fh.write('    this.%s = _r.readDateTime("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('date'):
                fh.write('    this.%s = _r.readDate("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('time'):
                fh.write('    this.%s = _r.readTime("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('dbrec', 'this'):
                fh.write('    this.%s._deserialize(_r);' % (self._member(a.name)))
            else:
                raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))

            fh.write('  if (_r._prom.broken()) return;\n')

        fh.write('\n    _r.readEnd(_oname);  if (_r._prom.broken()) return;\n')
        fh.write('  }\n\n')

        if main_class and len(tbl.primary_keys) > 0:
            self._write_ts_method(fh,
                                  None,
                                  '_writePK',
                                  'key: %sKey' % (cls),
                                  method_descr = 'Write the primary key columns to the key object.')
            fh.write('    this._writeKey(key);\n\n')
            fh.write('  }\n\n')

            self._write_ts_method(fh,
                                  None,
                                  '_readPK',
                                  'key: %sKey' % (cls),
                                  method_descr = 'Read the primary key columns from the key object.')
            fh.write('    this._readKey(key);\n')
            fh.write('  }\n\n')

            self._write_ts_method(fh,
                                  None,
                                  '_serializeKey',
                                  '_w: Writer',
                                  method_descr = 'Serialize the primary key to a stream.')
            fh.write('    let key = new %sKey();\n\n' % (cls))
            fh.write('    this._writeKey(key);\n')
            fh.write('    key._serialize(_w);\n\n')
            fh.write('  }\n\n')

            self._write_ts_method(fh,
                                  None,
                                  '_deserializeKey',
                                  '_r: Reader',
                                  method_descr = 'Deserialize the primary key from a stream.')
            fh.write('    let key = new %sKey();\n\n' % (cls))
            fh.write('    key._deserialize(_r);\n')
            fh.write('    this._readKey(key);\n\n')
            fh.write('  }\n\n')

            self._write_ts_method(fh,
                                  None,
                                  '_writeKey',
                                  'key: %s' % self._table_key_class,
                                  method_descr = 'Write primary key columns to \\p _key.')
            self._write_copy_args(fh, 'key.', self._table_key_columns, 'this.')
            fh.write('  }\n\n')

            self._write_ts_method(fh,
                                  None,
                                  '_readKey',
                                  'key: %s' % self._table_key_class,
                                  method_descr = 'Read the primary key columns from \\p _key.')
            self._write_copy_args(fh, 'this.', self._table_key_columns, 'key.')
            fh.write('  }\n\n')

        self._write_ts_method(fh, 'string', 'toString', None)
        self._write_str_print_fields(fh, columns)
        fh.write('  }\n\n')

        fh.write('}\n\n')

        if main_class:
            self._write_couplets(fh, cls, columns)

        self._gen_trailers(fh)

        self.gened_file_close(fh)


    def _gen_custom_procs(self):
        for proc in self._gen_info['table'].procs:
            if self._mode == self.TABLE:
                if proc.in_fields:
                    if len(proc.in_fields) != 1 or proc.in_fields[0].type != 'dbrec':
                        self._write_data_class(self._ident('class.qryin', '%s%s' % (self._table_id, proc.name)),
                                               proc.in_fields,
                                               self._ident('file.qryin', '%s%s' % (self._table_id, proc.name)))

                if proc.out_fields:
                    if len(proc.out_fields) != 1 or proc.out_fields[0].type != 'dbrec':
                        self._write_data_class(self._ident('class.qryout', '%s%s' % (self._table_id, proc.name)),
                                               proc.out_fields,
                                               self._ident('file.qryout', '%s%s' % (self._table_id, proc.name)))


    def _write_ts_method(self,
                         fh,
                         returnType   : str,
                         method       : str,
                         args         : 'list|str' = None,
                         ignoreTypes  : list = [],
                         extra_spaces : str = '',
                         use_def_vals : bool = False,
                         method_descr : str = ''):
        cstr  = '  %s%s(' % (extra_spaces, method)
        comma = ''

        fh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguements(fh, args, len(cstr), ignoreTypes, use_def_vals=use_def_vals)
            elif type(args) == str:
                arr = args.split(',')

                for a in arr:
                    fh.write('%s%s' % (comma, a))
                    comma = ', '

        if returnType:
            fh.write('): %s {\n' % returnType)
        else:
            fh.write(') {\n')


    def _write_arguements(self,
                          fh,
                          args         : 'list|str',
                          spacing      : int,
                          filter_out   : list = None,
                          comments     : bool = False,
                          extra_spaces : str  = '',
                          use_def_vals : bool = False):
        if args is None or len(args) < 1:
            return

        comma = ''

        for a in args:
            if filter_out:
                if a.type in filter_out:
                    continue

            fmap = self._field_map[a.type]

            if comments:
                pass
            else:
                fh.write('%s%s' % (comma, self._member(a.name)))

                if use_def_vals:
                    if a.isArray:
                        fh.write(' = undefined')
                    else:
                        fh.write(' = %s' % fmap.def_value)

                if a.type == 'dbrec':
                    fh.write(': %s' % (self._ident('class.table', self._lookup_name(a.lookup, a.name))))
                else:
                    fh.write(': %s' % fmap.name)

            comma = ', '


    def _write_copy_args(self, fh, fromObj, args, toObj, fil = None):
        if args is None or len(args) < 1:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fh.write('    %s%s = %s%s;\n' % (fromObj, self._member(a.name), toObj, self._member(a.name)))


    def _write_member_declaration(self, fh, members):
        for m in members:
            fmap = self._field_map[m.type]

            if m.type == 'dbrec':
                fh.write('  %s: %s = new %s();\n' % (self._member(m.name),
                                                     self._ident('class.table', self._lookup_name(m.lookup, m.name)),
                                                     self._ident('class.table', self._lookup_name(m.lookup, m.name))))
            else:
                fh.write('  %s: %s = %s;\n' % (self._member(m.name), fmap.name, fmap.def_value))

        fh.write('\n')


    def _write_clear_fields(self, fh, args, fil = None):
        if args is None or len(args) < 1:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            if fmap.type_flag == 'dbrec':
                fh.write('    this.%s._clear();\n' % (self._member(a.name)))
            else:
                fh.write('    this.%s = %s;\n' % (self._member(a.name), fmap.def_value))


    def _write_str_print_fields(self, fh, args):
        if args is None or len(args) < 1:
            return

        fh.write('    return')
        delim = '"'

        for a in args:
            fh.write(' %s%s:" + this.%s' % (delim, self._member(a.name), self._member(a.name)))
            delim = '+ ", '

        fh.write(';\n')


    def _write_couplets(self, fh, cls: str, columns: list):

        for col in columns:
            if col.couplets is None or len(col.couplets) < 1:
                continue

            fmap     = self._field_map[col.type]
            val_mask = '  static %-30s : %s = "%s";\n'
            cpl_cls  = self._ident('class.couplet', '%s_%s' % (self._table_id, col.name))

            fh.write('export class %s {\n' % (cpl_cls))

            if fmap.type_flag in ('str'):
                key_mask = '  static %-30s: %s = "%s";\n'
            else:
                key_mask = '  static %-30s: %s = %s;\n'

            for key, val in col.couplets.items():
                fh.write(key_mask % (self._ident_member('Key%s' % self._couplet_name(val)), fmap.name, str(key)))

            fh.write('\n')

            for key, val in col.couplets.items():
                fh.write(val_mask % (self._ident_member('Value%s' % self._couplet_name(val)), 'string', str(val)))

            fh.write('\n')

            fh.write('  static %s() : %s[] {\n' % (self._ident_method('GetKeys'), fmap.name))
            fh.write('    let res: %s[] = [];\n\n' % fmap.name)

            for key, val in col.couplets.items():
                fh.write('    res.push(%s.%s);\n' % (cpl_cls, self._ident_member('Key%s' % self._couplet_name(val))))

            fh.write('\n    return res;\n')
            fh.write('  }\n\n')

            fh.write('  static %s() : { [key: %s]: string } {\n' % (self._ident_method('GetDictionary'), fmap.name))
            fh.write('    let dic : { [key: %s]: string } = {};\n\n' % fmap.name)

            for key, val in col.couplets.items():
                fh.write('    dic[%s.%s] = %s.%s;\n' % (
                    cpl_cls,
                    self._ident_member('Key%s' % self._couplet_name(val)),
                    cpl_cls,
                    self._ident_member('Value%s' % self._couplet_name(val))))

            fh.write('\n    return dic;\n')
            fh.write('  }\n\n')

            keyid = self._ident_member('KeyId')

            fh.write('  static %s(%s: %s) : string {\n' % (self._ident_method('GetValue'), keyid, fmap.name))

            for key, val in col.couplets.items():
                fh.write('    if (%s === %s.%s)\n' % (keyid, cpl_cls, self._ident_member('Key%s' % self._couplet_name(val))))
                fh.write('      return %s.%s;\n\n' % (cpl_cls, self._ident_member('Value%s' % self._couplet_name(val))))

            fh.write('    return "";\n')
            fh.write('  }\n')
            fh.write('}\n\n')


    def return_struct_path(self, table: str, qry: str, struct_type: str, incl_fname: bool = False):
        # Override struct path method
        sname = '%s%s' % (table, qry)
        key   = ''

        if struct_type == 'table':
            key = 'file.table'
        elif struct_type == 'key':
            sname = sname + 'Key'
            key   = 'file.table'
        elif struct_type == 'in':
            key   = 'file.qryin'
        elif struct_type == 'out':
            key   = 'file.qryout'
        else:
            raise Exception('StructType expected (table/key/in/out) and got (%s)' % struct_type)

        return self._ident(key, sname)
