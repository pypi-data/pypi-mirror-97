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

        self._field_map['bool']         = Generator.FieldMap('boolean',   type_flag = 'bool',        def_val = 'false')
        self._field_map['int8']         = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['int16']        = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['int32']        = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['int64']        = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['uint8']        = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['uint16']       = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['uint32']       = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['uint64']       = Generator.FieldMap('number',    type_flag = 'int',         def_val = '0')
        self._field_map['char']         = Generator.FieldMap('string',    type_flag = 'str',         def_val = "''")
        self._field_map['string']       = Generator.FieldMap('string',    type_flag = 'str',         def_val = "''")
        self._field_map['time']         = Generator.FieldMap('Date',      type_flag = 'date',        def_val = 'undefined')
        self._field_map['date']         = Generator.FieldMap('Date',      type_flag = 'date',        def_val = 'undefined')
        self._field_map['datetime']     = Generator.FieldMap('Date',      type_flag = 'date',        def_val = 'undefined')
        self._field_map['memblock']     = Generator.FieldMap('string',    type_flag = 'memblock',    def_val = 'undefined')
        self._field_map['uuid']         = Generator.FieldMap('string',    type_flag = 'uuid',        def_val = "''")
        self._field_map['json']         = Generator.FieldMap('string',    type_flag = 'str',         def_val = "''")
        self._field_map['double']       = Generator.FieldMap('number',    type_flag = 'double',      def_val = '0.0')
        self._field_map['dbrec']        = Generator.FieldMap('struct',    type_flag = 'dbrec',       def_val = 'undefined')
        self._field_map['brazerec']     = Generator.FieldMap('struct',    type_flag = 'brazerec',    def_val = 'undefined')

        self._init_code_options({'import.dbpath': '.'})


    def name(self) -> str:
        return 'TypeScript'


    def finalize_generation(self, gen_info):
        """
        Create the index.ts for generated code.
        """
        if gen_info['clean']:
            return

        nap    = gen_info['proj'].project_dir
        nsdir  = os.path.join(nap, self.dest_dir).replace('\\', os.path.sep).replace('/', os.path.sep).replace('|', os.path.sep)
        ns     = self._namespace()
        fh     = None

        nsFile = os.path.join(nsdir, 'index.ts')
        fh     = open(nsFile, 'wt')

        self._add_headers(fh)

        for gf in self._gened_files[ns]:
            fh.write("export * from './%s';\n" % (gf.fname))

        fh.close()


    def generate_structs(self, gen_info):
        self._gen_info = gen_info
        self._mode    = self.STRUCT
        self._generate()


    def generate_client(self, gen_info):
        self._gen_info = gen_info
        self._mode    = self.CLIENT
        self._generate()


    def generate_server(self, gen_info):
        pass


    def _namespace(self, speSep = None, blank_ok = False, baseOnly = False):
        return ''


    def _generate(self):
        if self._gen_info['clean']:
            self.clean(self._gen_info)
            return

        self._proj_id         = self._gen_info['proj'].name
        self._struct_filename = self._ident('file.struct', '%sStructs' % self._proj_id)

        if self._mode == self.STRUCT:
            fh = self.gened_file_open(self._gen_info, self._struct_filename)
            self._add_headers(fh)
            self._add_struct_imports(fh)
            self._gen_braze_couplets(fh)
            self._gen_braze_structs(fh)
            self.gened_file_close(fh)
        elif self._mode == self.CLIENT:
            cls             = self._ident('client.marshaler', self._gen_info['proj'].name)
            client_filename = self._ident('file.class', cls)
            fh              = self.gened_file_open(self._gen_info, client_filename, cls=cls)

            self._add_headers(fh)
            self._add_client_imports(fh)
            self._gen_client_marshaler(fh)
            self.gened_file_close(fh)


    def _member(self, mem):
        return self._ident_member(mem)


    def _add_headers(self, fh):
        message = '/* This file was generated by mettle.genes.braze.GenTs [ver %s] on %s */\n\n' % (
            self._gen_info['version'], time.asctime())
        fh.write(message)


    def _gen_struct_imports(self, fh, db_paths: list, fields: list, import_set: set, db_only: bool):
        for f in fields:

            fmap = self._field_map[f.type]

            if fmap.type_flag == 'dbrec':
                imp_key = '%s.%s' % (f.dbstruct.proj, f.dbstruct.struct_name())

                if imp_key in import_set:
                    continue

                fh.write("import { %s } from '%s/%s';\n" % (
                    f.dbstruct.struct_name(),
                    db_paths[f.dbstruct.proj],
                    f.dbstruct.struct_path())
                )

                import_set.add('%s' % (imp_key))

                if f.is_array and "List" not in import_set:
                    fh.write("import { List } from '@bitsmiths/mettle-braze';\n")
                    import_set.add("List")

            elif fmap.type_flag == 'brazerec':
                imp_key = '%s' % (f.brazestruct.name)

                if imp_key in import_set:
                    continue

                if f.is_array and "List" not in import_set:
                    fh.write("import { List } from '@bitsmiths/mettle-braze';\n")
                    import_set.add("List")

                if not db_only:

                    fh.write("import { %s } from './%s';\n" % (
                        self._ident('braze.struct', f.brazestruct.struct_name()),
                        self._struct_filename))

                    import_set.add(imp_key)

            else:
                if f.is_array:
                    if f.type == 'uuid':
                        imp_key = 'GuidList'
                    else:
                        imp_key = '%sList' % f.type.capitalize()

                    if imp_key in import_set:
                        continue

                    fh.write("import { %s } from '@bitsmiths/mettle-braze';\n" % (imp_key))
                    import_set.add(imp_key)



    def _add_imports(self, fh, db_only=False):
        self.importDBPath = self.get_option('import.dbpath', blank_ok=True).replace('|', '/').replace('\\', '/')

        db_paths = {}

        for dbEntry in self.importDBPath.split(';'):
            if dbEntry == '':
                continue

            entry = dbEntry.split(':')
            if len(entry) != 2:
                raise Exception('Invalid setting value for [import.dbpath] in generator [TypeScript]. Expecting'
                                ' ; seperated list of databaseName:path entries.')

            db_paths[entry[0]] = entry[1]

        import_set = set()

        for k, v in self._gen_info['proj'].structs.items():
            self._gen_struct_imports(fh, db_paths, v.fields, import_set, db_only)

        for call in self._gen_info['proj'].calls:
            self._gen_struct_imports(fh, db_paths, call.fields, import_set, db_only)

            if not call.returns:
                continue

            if call.returns.type == 'dbrec':
                if call.returns.is_array and "List" not in import_set:
                    fh.write("import { List } from '@bitsmiths/mettle-braze';\n")
                    import_set.add("List")

                imp_key = '%s.%s' % (call.returns.dbstruct.proj, call.returns.dbstruct.struct_name())

                if imp_key in import_set:
                    continue

                fh.write("import { %s } from '%s/%s';\n" % (
                    call.returns.dbstruct.struct_name(),
                    db_paths[call.returns.dbstruct.proj],
                    call.returns.dbstruct.struct_path()))

                import_set.add(imp_key)

            if call.returns.type == 'brazerec' and not db_only:
                if call.returns.is_array and "List" not in import_set:
                    fh.write("import { List } from '@bitsmiths/mettle-braze';\n")
                    import_set.add("List")

                imp_key = '%s' % (call.returns.brazestruct.name)

                if imp_key in import_set:
                    continue

                fh.write("import { %s } from './%s';\n" % (
                    self._ident('braze.struct', call.returns.brazestruct.struct_name()), self._struct_filename))

                import_set.add(imp_key)


    def _add_struct_imports(self, fh):
        fh.write("import { ListStream }    from '@bitsmiths/mettle-io';\n")
        fh.write("import { Reader }        from '@bitsmiths/mettle-io';\n")
        fh.write("import { Writer }        from '@bitsmiths/mettle-io';\n")
        fh.write("import { ISerializable } from '@bitsmiths/mettle-io';\n\n")

        self._add_imports(fh, db_only=True)

        fh.write('\n')


    def _add_client_imports(self, fh):
        fh.write("import { MettlePromise } from '@bitsmiths/mettle-lib';\n")
        fh.write("import { xMettle }       from '@bitsmiths/mettle-lib';\n")
        fh.write("import { Client }        from '@bitsmiths/mettle-braze';\n")
        fh.write("import { ListStream }    from '@bitsmiths/mettle-io';\n")
        fh.write("import { Reader }        from '@bitsmiths/mettle-io';\n")
        fh.write("import { Writer }        from '@bitsmiths/mettle-io';\n\n")

        self._add_imports(fh)

        fh.write('\n')


    def _write_ts_method(self,
                         fh,
                         return_type      : str,
                         method           : str,
                         args             : "list|str" = None,
                         extra_spaces     : str = '',
                         use_default_vals : bool = False):
        cstr  = '  %s%s(' % (extra_spaces, method)
        comma = ''

        fh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguments(fh, args, len(cstr), use_default_vals=use_default_vals)
            elif type(args) == str:
                arr   = args.split(',')

                for a in arr:
                    fh.write('%s%s' % (comma, a))
                    comma = ', '

        if return_type:
            fh.write('): %s {\n' % return_type)
        else:
            fh.write(') {\n')


    def _write_arguments(self, fh, args, spacing, comments = False, extra_spaces = '', use_default_vals = False):
        if not args:
            return

        comma = ''

        for a in args:
            if a['io'] == 'output':
                continue

            if comments:

                fh.write("  %s * @param %s" % (extra_spaces, a['name']))

                if a['io']:
                    fh.write('  %s' % a['io'])

                    if a.get('descr'):
                        fh.write(' - %s' % a.get('descr'))

                elif a.get('descr'):
                    fh.write('  %s' % a.get('descr'))

                fh.write('\n')

            else:

                fh.write('%s%s: %s' % (comma, a['name'], a['type']))

                if use_default_vals:
                    fh.write(' = %s' % a['default'])

            comma = ', '


    def _write_copy_args(self, fh, from_obj: str, args: list, to_obj: str = '', fil: list = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fh.write('    %s%s = %s%s;\n' % (from_obj, self._member(a.name), to_obj, self._member(a.name)))


    def _write_init_fields(self, fh, from_obj, args):
        if not args:
            return

        for a in args:
            fh.write('  %s%s: %s = %s;\n' % (from_obj, a['name'], a['type'], a['new']))

        fh.write('\n')


    def _write_clear_fields(self, fh, args: list, fil: list = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            if a.is_array or fmap.type_flag in ['dbrec', 'brazerec']:
                fh.write('    this.%s._clear();\n' % (self._member(a.name)))
            else:
                fh.write('    this.%s = %s;\n' % (self._member(a.name), fmap.def_val))



    def _write_str_print_fields(self, fh, args: list):
        if not args:
            return

        fh.write('    return')
        delim = '"'

        for a in args:
            fh.write(' %s%s:" + this.%s' % (delim, self._member(a.name), self._member(a.name)))
            delim = '+ ", '
            fmap   = self._field_map[a.type]

            if a.is_array:
                fh.write(".length")
            elif fmap.type_flag == 'dbrec':
                fh.write("._name()" )
            elif fmap.type_flag == 'brazerec':
                fh.write("._name()")

        fh.write(';\n')


    def _gen_braze_couplets(self, fh):
        if len(self._gen_info['proj'].couplets) < 1:
            return

        for x, cobj in self._gen_info['proj'].couplets.items():
            cpl_cls  = self._ident('braze.couplet', cobj.name)
            fmap     = self._field_map[cobj.ctype]
            key_mask = ''
            val_mask = '  static %-30s: string = "%s";\n'

            fh.write('export class %s {\n\n' % cpl_cls)

            if fmap.type_flag in ['str']:
                key_mask = '  static %-30s: %s = "%s";\n'
            else:
                key_mask = '  static %-30s: %s = %s;\n'

            for key, val in cobj.couplet.items():
                fh.write(key_mask % (self._member('Key%s' % self._couplet_name(val)), fmap.name, str(key)))

            fh.write('\n')

            for key, val in cobj.couplet.items():
                fh.write(val_mask % (self._member('Value%s' % self._couplet_name(val)), str(val)))

            fh.write('\n')
            fh.write('  static %s() : %s[] {\n' % (self._ident_method('GetKeys'), fmap.name))
            fh.write('    let res: %s[] = [];\n\n' % fmap.name)

            for key, val in cobj.couplet.items():
                fh.write('    res.push(%s.%s);\n' % (cpl_cls, self._member('Key%s' % self._couplet_name(val))))

            fh.write('\n    return res;\n')
            fh.write('  }\n\n')

            fh.write('  %s() : { [key: %s]: string } {\n' % (self._ident_method('GetDictionary'), fmap.name))
            fh.write('    let dic : { [key: %s]: string } = {};\n\n' % fmap.name)

            for key, val in cobj.couplet.items():
                fh.write('    dic[%s.%s] = %s.%s;\n' % (
                    cpl_cls,
                    self._member('Key%s' % self._couplet_name(val)),
                    cpl_cls,
                    self._member('Value%s' % self._couplet_name(val))))

            fh.write('\n    return dic;\n')
            fh.write('  }\n\n')

            fh.write('  static %s(key: %s) : string {\n' % (self._ident_method('GetValue'), fmap.name))

            for key, val in cobj.couplet.items():
                fh.write('    if (key === %s.%s)\n' % (cpl_cls, self._member('Key%s' % self._couplet_name(val))))
                fh.write('      return %s.%s;\n\n' % (cpl_cls, self._member('Value%s' % self._couplet_name(val))))

            fh.write('    return "";\n')
            fh.write('  }\n')
            fh.write('}\n\n')


    def _gen_braze_structs(self, fh):

        for s in self._gen_info['proj'].struct_order:
            sobj      = self._gen_info['proj'].structs[s]
            sname     = self._ident('braze.struct', '%s' % (sobj.name))
            args      = self._gen_arg_items(sobj.fields, True)

            fh.write('export class %s extends ISerializable {\n\n' % sname)

            self._write_init_fields(fh, '', args)

            fh.write('  /**\n')
            fh.write('   * Constructor.\n')
            fh.write('   */\n')
            self._write_ts_method(fh, None, 'constructor', '')
            fh.write('    super();\n')
            fh.write('  }\n\n')

            # Struct.Struct()
            fh.write('  /**\n')
            fh.write('   * Initialize with record.\n')
            fh.write('   * @param rec  The rec to copy from.\n')
            fh.write('   */\n')
            self._write_ts_method(fh, sname, self._ident_method('_init'), 'rec: %s' % sname)
            self._write_copy_args(fh, 'this.', sobj.fields, 'rec.')
            fh.write('\n    return this;\n')
            fh.write('  }\n\n')

            # Struct.Struct()
            fh.write('  /**\n')
            fh.write('   * Initialize with all fields.\n')
            self._write_arguments(fh, args, '', comments=True)
            fh.write('   */\n')
            self._write_ts_method(fh, sname, self._ident_method('_initDeft'), args)
            self._write_copy_args(fh, 'this.', sobj.fields)
            fh.write('\n    return this;\n')
            fh.write('  }\n\n')

            # void Struct.clear()
            fh.write('  /**\n')
            fh.write('   * Clear all object values.\n')
            fh.write('   */\n')
            self._write_ts_method(fh, None, '_clear', None)
            self._write_clear_fields(fh, sobj.fields)
            fh.write('  }\n\n')

            # string Struct._name()
            fh.write('  /**\n')
            fh.write('   * The default object name.\n')
            fh.write('   */\n')
            self._write_ts_method(fh, 'string', '_name', None)
            fh.write("    return '%s';\n  }\n\n" % sname)

            # Struct._serialize()
            fh.write('  /**\n')
            fh.write('   * Serialize the object with a writer.\n')
            fh.write('   * @param _w      The writer object to use.\n')
            fh.write('   * @param _oname  Optionally pass in a diff name for the object.\n')
            fh.write('   */\n')
            self._write_ts_method(fh, None, '_serialize', '_w: Writer, _oname?: string')
            fh.write('    if (_oname === undefined)\n')
            fh.write('      _oname = this._name();\n\n')
            fh.write('    _w.writeStart(_oname);  if (_w._prom.broken()) return;\n\n')

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        if a.is_array and a.type == 'brazerec':
                            fh.write('    this.%s._serialize(_w, "%s");' % (a.name, a.name))
                        else:
                            fh.write('    this.%s._serialize(_w, "%s");' % (a.name, a.name))
                    else:
                        if a.type in ['int32', 'int64', 'int16', 'int8', 'uint32', 'uint64', 'uint16', 'uint8']:
                            fh.write('    _w.writeInt("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['string']:
                            fh.write('    _w.writeString("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['char']:
                            fh.write('    _w.writeChar("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['bool']:
                            fh.write('    _w.writeBool("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['double']:
                            fh.write('    _w.writeFloat("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['memblock']:
                            fh.write('    _w.writeByteArray("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['datetime']:
                            fh.write('    _w.writeDateTime("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['date']:
                            fh.write('    _w.writeDate("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['time']:
                            fh.write('    _w.writeTime("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['uuid']:
                            fh.write('    _w.writeGuid("%s", this.%s);' % (a.name, a.name))
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

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        fh.write('    this.%s._deserialize(_r, "%s");' % (a.name, a.name))
                    else:
                        if a.type in ['int32', 'int64', 'int16', 'int8', 'uint32', 'uint64', 'uint16', 'uint8']:
                            fh.write('    this.%s = _r.readInt("%s");' % (a.name, a.name))
                        elif a.type in ['string']:
                            fh.write('    this.%s = _r.readString("%s");' % (a.name, a.name))
                        elif a.type in ['char']:
                            fh.write('    this.%s = _r.readChar("%s");' % (a.name, a.name))
                        elif a.type in ['bool']:
                            fh.write('    this.%s = _r.readBool("%s");' % (a.name, a.name))
                        elif a.type in ['double']:
                            fh.write('    this.%s = _r.readFloat("%s");' % (a.name, a.name))
                        elif a.type in ['memblock']:
                            fh.write('    this.%s = _r.readByteArray("%s");' % (a.name, a.name))
                        elif a.type in ['datetime']:
                            fh.write('    this.%s = _r.readDateTime("%s");' % (a.name, a.name))
                        elif a.type in ['date']:
                            fh.write('    this.%s = _r.readDate("%s");' % (a.name, a.name))
                        elif a.type in ['time']:
                            fh.write('    this.%s = _r.readTime("%s");' % (a.name, a.name))
                        elif a.type in ['uuid']:
                            fh.write('    this.%s = _r.readGuid("%s");' % (a.name, a.name))
                        else:
                            raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))

                    fh.write('  if (_r._prom.broken()) return;\n')

            fh.write('\n    _r.readEnd(_oname);  if (_r._prom.broken()) return;\n')
            fh.write('  }\n\n')

            # string Struct.toString()
            self._write_ts_method(fh, 'String', 'toString', None)
            self._write_str_print_fields(fh, sobj.fields)
            fh.write('  }\n')

            fh.write('}\n\n')


    def _gen_client_marshaler(self, fh):
        cls               = self._ident('client.marshaler', self._gen_info['proj'].name)
        self._clientClass = cls

        # Class & Constrcutor
        fh.write('export class %s extends Client {\n\n' % (self._clientClass))

        fh.write('  _client: Client;\n\n')

        fh.write('  /**\n')
        fh.write('   * Constructor.\n')
        fh.write('   * @param client  The braze client object.\n')
        fh.write('   */\n')
        fh.write('  constructor(client: Client) {\n')
        fh.write('    super();\n')
        fh.write('    this._client = client;\n')
        fh.write('  }\n\n')

        fh.write('  _name(): string {\n')
        fh.write('     return "%s";\n' % self._gen_info['proj'].name)
        fh.write('  }\n\n')

        fh.write('  /**\n')
        fh.write('   * Gets the client signature.\n')
        fh.write('   * @returns  The signature of this client.\n')
        fh.write('   */\n')
        fh.write('  _signature(): string {\n')
        fh.write('    return "%s";\n' % self._gen_info['server_sig'])
        fh.write('  }\n\n')


        for call in self._gen_info['proj'].calls:

            return_type  = self._gen_return_type_str(call)
            args         = self._gen_arg_items(call.fields)

            fh.write('  /**\n')
            fh.write('   * %s\n' % (call.get_descr() or call.name))

            for a in args:
                fh.write('   * @param %s' % (a['name']))

                if a['io']:
                    fh.write('  %s' % a['io'])

                    if a.get('descr'):
                        fh.write(' - %s' % a.get('descr'))

                elif a.get('descr'):
                    fh.write('  %s' % a.get('descr'))

                fh.write('\n')


            fh.write('   */\n')

            fh.write('  %s(' % call.name)

            delim    = ''
            out_args = False

            for a in args:
                if a['io'] == 'output':
                    out_args = True
                    continue

                if a['io'] == 'input/output':
                    out_args = True

                fh.write('%s%s: %s' % (delim, a['name'], a['type']))
                delim = ', '

            res_str = ''

            if return_type == 'void' and not out_args:
                res_str = 'void'
            elif out_args:
                comma = ''
                if return_type == 'void':
                    res_str = '{'
                else:
                    res_str = '{result: %s' % return_type
                    comma = ', '

                for a in args:
                    if a['io'] == 'input':
                        continue

                    res_str += '%s%s: %s' % (comma, a['name'], a['type'])
                    comma   = ', '

                res_str += '}'
            else:
                res_str = return_type

            fh.write(') : Promise<%s> {\n' % res_str)


            fh.write('    return new Promise<%s>( (resolve, reject) => {\n' % res_str)
            fh.write('      let prom = new MettlePromise((data, httpCode) => {\n')

            if return_type == 'void' and not out_args:
                fh.write('        resolve();\n')
            elif out_args:
                fh.write('        resolve(data);\n')
            else:
                fh.write('        resolve(data.result);\n')

            fh.write('      }, (exc) => {\n')
            fh.write('        reject(exc);\n')
            fh.write('      }, (exc) => {\n')
            fh.write('        reject(exc);\n')
            fh.write('      });\n\n')

            self._gen_client_declare_varibles(fh, call)
            self._gen_client_assign_input_args(fh, call)
            self._gen_client_server_call(fh, call)
            self._gen_client_assign_output_args(fh, call, return_type)

            fh.write('\n        return prom.keep(_x);\n')
            fh.write('      });\n')
            fh.write('    });\n')
            fh.write('  }\n\n')

        fh.write('}')


    def _gen_arg_items(self, fields, is_struct: bool = False):
        args = []

        for f in fields:
            param = { 'name': self._member(f.name), 'descr': f.descr }
            args.append(param)

            if f.io == 'i':
                param['io'] = 'input'
            elif f.io == 'o':
                param['io'] = 'output'
            else:
                if is_struct:
                    param['io'] = ''
                else:
                    param['io'] = 'input/output'

            fmap = self._field_map[f.type]

            param['default'] = fmap.def_val
            param['new']     = fmap.def_val

            if f.is_array:
                sname = ''
                if fmap.type_flag == 'brazerec':
                    sname = self._ident('braze.struct', f.brazestruct.struct_name())
                    param['type'] = 'List<%s>' % sname
                elif fmap.type_flag == 'dbrec':
                    sname = f.dbstruct.struct_name()
                    param['type'] = 'List<%s>' % sname
                else:
                    if f.type == 'uuid':
                        param['type'] = 'GuidList'
                    else:
                        param['type'] = '%sList' % f.type.capitalize()

                param['new'] = 'new %s(%s)' % (param['type'], sname)
                continue

            if fmap.type_flag == 'brazerec':
                param['type'] = self._ident('braze.struct', f.brazestruct.struct_name())
                param['new']  = 'new %s()' % param['type']
            elif fmap.type_flag == 'dbrec':
                param['type'] = f.dbstruct.struct_name()
                param['new']  = 'new %s()' % param['type']
            else:
                param['type'] = fmap.name

                if is_struct:
                    continue

        return args


    def _gen_return_type_str(self, call):
        if not call.returns:
            return 'void'

        if call.returns.is_array:

            if call.returns.type == 'brazerec':
                return 'List<%s>' % (self._ident('braze.struct', call.returns.brazestruct.struct_name()))

            if call.returns.type == 'dbrec':
                return 'List<%s>' % call.returns.dbstruct.struct_name()

            if call.returns.type == 'memblock':
                return 'MemblockList'

            if call.returns.type == 'uuid':
                return 'GuidList'

            return '%s%sList' % (call.returns.type[0].upper(), call.returns.type[1:])


        if call.returns.type == 'brazerec':
            return '%s' % (self._ident('braze.struct', call.returns.brazestruct.struct_name()))

        if call.returns.type == 'dbrec':
            return '%s' % call.returns.dbstruct.struct_name()

        fmap = self._field_map[call.returns.type]

        return fmap.name


    def _gen_client_declare_varibles(self, fh, call):
        fh.write('      let %s : ListStream = new ListStream(prom);\n' % '_i')

        call.hasInput   = False
        call.hasOutput  = False

        for f in call.fields:
            if f.io in ['i', 'io']:
                fh.write('      let %s : Writer;\n' % '_w')
                call.hasInput = True
                break

        for f in call.fields:
            if f.io in ['o', 'io']:
                call.hasOutput = True
                break

        if call.returns and not call.hasOutput:
            call.hasOutput = True

        fh.write('\n')


    def _gen_client_assign_input_args(self, fh, call):
        if not call.hasInput:
            return

        fh.write('      _w = this._client.newWriter(prom, _i);\n')
        fh.write('      _w.writeStart("%s_IN"); if (prom.broken()) return;\n' % (call.name))

        for f in call.fields:
            if f.io == 'o':
                continue

            fmap   = self._field_map[f.type]

            if fmap.type_flag in ['brazerec', 'dbrec'] or f.is_array:
                fh.write('      %s._serialize(_w); if (prom.broken()) return;\n' % (f.name))
                continue

            fname = f.name

            if f.type in ['int32', 'int16', 'int64', 'int8', 'uint32', 'uint16', 'uint64', 'uint8']:
                fh.write('      _w.writeInt("%s", %s);' % (f.name, fname))
            elif f.type in ['string']:
                fh.write('      _w.writeString("%s", %s);' % (f.name, fname))
            elif f.type in ['char']:
                fh.write('      _w.writeChar("%s", %s);' % (f.name, fname))
            elif f.type in ['bool']:
                fh.write('      _w.writeBool("%s", %s);' % (f.name, fname))
            elif f.type in ['double']:
                fh.write('      _w.writeFloat("%s", %s);' % (f.name, fname))
            elif f.type in ['memblock']:
                fh.write('      _w.writeByteArray("%s", %s);' % (f.name, fname))
            elif f.type in ['datetime']:
                fh.write('      _w.writeDateTime("%s", %s);' % (f.name, f.name))
            elif f.type in ['date']:
                fh.write('      _w.writeDate("%s", %s);' % (f.name, f.name))
            elif f.type in ['time']:
                fh.write('      _w.writeTime("%s", %s);' % (f.name, f.name))
            elif f.type in ['uuid']:
                fh.write('      _w.writeGuid("%s", %s);' % (f.name, f.name))
            else:
                raise Exception('Unknown type [%s] for field [%s]' % (f.type, f.name))

            fh.write("  if (prom.broken()) return;\n")

        fh.write('      _w.writeEnd("%s_IN"); if (prom.broken()) return;\n' % (call.name))
        fh.write('\n')


    def _gen_client_server_call(self, fh, call):
        sig = call.signature

        fh.write('      this._client.send(prom, this, "%s", _i, (prom: MettlePromise, marsh: %s, sig: string'
                 ', _o: ListStream) => {\n'  % (sig, self._clientClass))
        fh.write('        if (prom.broken()) return;\n')


    def _gen_client_assign_output_args(self, fh, call, return_type):
        if not call.hasOutput:
            fh.write('\n        let %s : any;\n' % '_x')
            return

        fh.write('\n        let _r = marsh._client.newReader(prom, _o);\n')
        fh.write('        _r.readStart("%s_OUT"); if (prom.broken()) return;\n' % call.name)
        fh.write('        let _x = Object();\n')

        if call.returns:
            f     = call.returns
            fmap  = self._field_map[f.type]
            fname = "return"

            fh.write("        _x.result = ")

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    sname = self._ident('braze.struct', f.brazestruct.struct_name())
                    fh.write('new List<%s>(%s);\n' % (sname, sname))
                elif fmap.type_flag == 'dbrec':
                    sname = f.dbstruct.struct_name()
                    fh.write('new List<%s>(%s);\n' % (sname, sname))
                else:
                    if f.type == 'uuid':
                        fh.write('new GuidList();\n')
                    else:
                        fh.write('new %sList();\n' % self._member(f.type).capitalize())

                fh.write("        _x.result._deserialize(_r); if (prom.broken()) return;\n")
            else:
                if fmap.type_flag == 'brazerec':
                    fh.write('new %s();\n' % (self._ident('braze.struct', f.brazestruct.struct_name())))
                    fh.write("        _x.result._deserialize(_r);")
                elif fmap.type_flag == 'dbrec':
                    fh.write('new %s();\n' % f.dbstruct.struct_name())
                    fh.write("        _x.result._deserialize(_r);")
                else:
                    if f.type in ['int32', 'int16', 'int64', 'int8', 'uint32', 'uint16', 'uint64', 'uint8']:
                        fh.write('_r.readInt("%s");' % (fname))
                    elif f.type in ['string']:
                        fh.write('_r.readString("%s");' % (fname))
                    elif f.type in ['char']:
                        fh.write('_r.readChar("%s");' % (fname))
                    elif f.type in ['bool']:
                        fh.write('_r.readBool("%s");' % (fname))
                    elif f.type in ['double']:
                        fh.write('_r.readFloat("%s");' % (fname))
                    elif f.type in ['memblock']:
                        fh.write('_r.readByteArray("%s");' % (fname))
                    elif f.type in ['datetime']:
                        fh.write('_r.readDateTime("%s");' % (f.name))
                    elif f.type in ['date']:
                        fh.write('_r.readDate("%s");' % (f.name))
                    elif f.type in ['time']:
                        fh.write('_r.readTime("%s");' % (f.name))
                    elif f.type in ['uuid']:
                        fh.write('_r.readGuid("%s");' % (f.name))
                    else:
                        raise Exception('Unknown type [%s] for field [%s]' % (f.type, f.name))

                fh.write("    if (prom.broken()) return;\n")


        for f in call.fields:
            if f.io == 'i':
                continue

            fmap = self._field_map[f.type]

            fh.write("        _x.%s = " % (f.name))

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    sname = self._ident('braze.struct', f.brazestruct.struct_name())
                    fh.write('new List<%s>(%s);\n' % (sname, sname))
                elif fmap.type_flag == 'dbrec':
                    sname = f.dbstruct.struct_name()
                    fh.write('new List<%s>(%s);\n' % (sname, sname))
                else:
                    if f.type == 'uuid':
                        fh.write('new GuidList();\n')
                    else:
                        fh.write('new %sList();\n' % self._member(f.type).capitalize())
                fh.write("        _x.%s._deserialize(_r); if (prom.broken()) return;\n" % (f.name))
            else:
                if fmap.type_flag == 'brazerec':
                    fh.write('new %s();\n' % (self._ident('braze.struct', f.brazestruct.struct_name())))
                    fh.write("        _x.%s._deserialize(_r);" % f.name)
                elif fmap.type_flag == 'dbrec':
                    fh.write('new %s();\n' % f.dbstruct.struct_name())
                    fh.write("        _x.%s._deserialize(_r);" % f.name)
                else:
                    if f.type in ['int32', 'int16', 'int64', 'int8', 'uint32', 'uint16', 'uint64', 'uint8']:
                        fh.write('_r.readInt("%s");' % (f.name))
                    elif f.type in ['string']:
                        fh.write('_r.readString("%s");' % (f.name))
                    elif f.type in ['char']:
                        fh.write('_r.readChar("%s");' % (f.name))
                    elif f.type in ['bool']:
                        fh.write('_r.readBool("%s");' % (f.name))
                    elif f.type in ['double']:
                        fh.write('_r.readFloat("%s");' % (f.name))
                    elif f.type in ['memblock']:
                        fh.write('_r.readByteArray("%s");' % (f.name))
                    elif f.type in ['datetime']:
                        fh.write('_r.readDateTime("%s");' % (f.name))
                    elif f.type in ['date']:
                        fh.write('_r.readDate("%s");' % (f.name))
                    elif f.type in ['time']:
                        fh.write('_r.readTime("%s");' % (f.name))
                    elif f.type in ['uuid']:
                        fh.write('_r.readUuid("%s");' % (f.name))
                    else:
                        raise Exception('Unknown type [%s] for field [%s]' % (f.type, f.name))

                fh.write("    if (prom.broken()) return;\n")

        fh.write('        _r.readEnd("%s_OUT"); if (prom.broken()) return;\n' % call.name)
