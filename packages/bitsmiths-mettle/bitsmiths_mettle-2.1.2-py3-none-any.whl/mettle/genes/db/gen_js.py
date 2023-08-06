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

import time

from .generator import Generator


class GenJS(Generator):

    SELECT_LOCK_ARG  = '_lockForUpdate'

    def __init__(self):
        Generator.__init__(self, ['js'])
        self.targ_type  = 'code'
        self.namespace = None

        self._field_map['bool']      = Generator.FieldMap('bool',              type_flag = 'bool',     def_value = 'false')
        self._field_map['int8']      = Generator.FieldMap('numeric',           type_flag = 'int',      def_value = '0')
        self._field_map['int16']     = Generator.FieldMap('numeric',           type_flag = 'int',      def_value = '0')
        self._field_map['int32']     = Generator.FieldMap('numeric',           type_flag = 'int',      def_value = '0')
        self._field_map['int64']     = Generator.FieldMap('numeric',           type_flag = 'int',      def_value = '0')
        self._field_map['seq32']     = Generator.FieldMap('numeric',           type_flag = 'int',      def_value = '0')
        self._field_map['seq64']     = Generator.FieldMap('numeric',           type_flag = 'int',      def_value = '0')
        self._field_map['char']      = Generator.FieldMap('string',            type_flag = 'str',      def_value = "''")
        self._field_map['string']    = Generator.FieldMap('string',            type_flag = 'str',      def_value = "''")
        self._field_map['date']      = Generator.FieldMap('datetime.date',     type_flag = 'date',     def_value = 'new Date(0)')   # noqa
        self._field_map['time']      = Generator.FieldMap('datetime.time',     type_flag = 'date',     def_value = 'new Date(0)')   # noqa
        self._field_map['datetime']  = Generator.FieldMap('datetime.datetime', type_flag = 'date',     def_value = 'new Date(0)')   # noqa
        self._field_map['timestamp'] = Generator.FieldMap('datetime.datetime', type_flag = 'date',     def_value = 'new Date(0)')   # noqa
        self._field_map['memblock']  = Generator.FieldMap('string',            type_flag = 'memblock', def_value = 'null')
        self._field_map['uuid']      = Generator.FieldMap('string',            type_flag = 'str',      def_value = "''")
        self._field_map['json']      = Generator.FieldMap('string',            type_flag = 'str',      def_value = "''")
        self._field_map['double']    = Generator.FieldMap('decimal',           type_flag = 'double',   def_value = '0.0')
        self._field_map['dynamic']   = Generator.FieldMap('string',            type_flag = 'str',      def_value = "''")
        self._field_map['dbrec']     = Generator.FieldMap('struct',            type_flag = 'dbrec',    def_value = 'null')

        self._init_code_options()


    def name(self):
        return 'JavaScript'


    def initialize_generation(self, gen_info):
        if gen_info['clean']:
            return

        self.namespace = self._namespace()
        self._gen_info  = gen_info
        self._tblCnt   = 0
        self._fh       = self.gened_file_open(gen_info, '%s' % gen_info['proj'].name.lower())

        self._add_headers(self._fh)
        self._package = self._gen_begin_namespaces(self._fh)


    def finalize_generation(self, gen_info):
        if gen_info['clean']:
            return

        self._gen_end_namespaces(self._fh)

        if self._fh:
            self.gened_file_close(self._fh)
            self._fh = None


    def generate_tables(self, gen_info):
        self._mode     = self.TABLE
        self._target_db = 'tables'
        self._generate(gen_info)


    def generate_daos(self, gen_info, target_db):
        pass


    def _generate(self, gen_info):
        if gen_info['clean']:
            if self._mode == self.TABLE:
                self.clean(gen_info, '')

            return

        if self._mode != self.TABLE:
            return

        if self._tblCnt == 0:
            self._tblPre = ''
        else:
            self._tblPre = ',\n\n'

        fh = self._fh
        self._tblCnt  += 1


        self._gen_info         = gen_info
        self._table_class      = self._pref_suf_name('class.table', self._gen_info['table'].name)
        self._table_key_class   = None
        self._table_key_columns = self._gen_info['table'].primary_key_columns()

        if len(self._table_key_columns) > 0:
            self._table_key_class = self._pref_suf_name('class.table', '%sKey' % self._gen_info['table'].name)

        self._write_data_class(fh, self._table_key_class, self._table_key_columns,          keyClass  = True)
        self._write_data_class(fh, self._table_class,    self._gen_info['table'].columns, mainClass = True)
        self._gen_custom_procs(fh)


    def _add_headers(self, fh):

        message = '// This file was generated by mettle.genes.db.GenJS [ver %s] on %s\n\n' % (
            self._gen_info['version'], time.asctime())
        fh.write(message)


    def _gen_begin_namespaces(self, fh):
        ns = self._namespace()
        np = ns.split('.')

        fh.write('var %s = {' % np[0])

        for sp in np[1:]:
            fh.write(' %s : {' % sp)

        fh.write('\n\n')

        return np[0]


    def _gen_end_namespaces(self, fh):
        ns = self._namespace()

        fh.write('\n\n')

        for x in ns.split('.'):
            fh.write('}')

        fh.write(';\n')


    def return_struct_name(self, table, qry, structType):
        sname = '%s%s' % (table, qry)
        key   = ''

        if structType == 'table':
            key = 'class.table'
        elif structType == 'key':
            sname = sname + 'Key'
            key   = 'class.table'
        elif structType == 'in':
            key   = 'class.qryin'
        elif structType == 'out':
            key   = 'class.qryout'
        else:
            raise Exception('StructType expected (table/key/in/out) and got (%s)' % structType)

        if not self.namespace:
            self.namespace = '%s.' % self._namespace()

        return '%s%s' % (self.namespace, self._pref_suf_name(key, sname))


    def _member(self, mem):
        if len(mem) < 2:
            return mem.lower()

        return '%s%s' % (mem[0].lower(), mem[1:])


    def _write_data_class(self, fh, cls, columns, mainClass = False, keyClass = False):
        if not columns:
            return

        tbl = self._gen_info['table']

        fh.write('%s%s : function() {\n\n' % (self._tblPre, cls))

        # _init copy constructor
        self._write_js_method(fh, None, '_init', 'rec')
        fh.write('    /*\n')
        fh.write('    Copy Constructor.\n')
        fh.write('    @param rec %s: rec to copy from.\n' % cls)
        fh.write('    */\n')
        self._writec_opy_args(fh, 'this.', columns, 'rec.')
        fh.write('\n    return this;\n')
        fh.write('  }\n\n')

        # Struct.Struct()
        self._write_js_method(fh, None, '_initDeft', columns, ['timestamp'])
        fh.write('    /*\n')
        fh.write('    Deft Constructor.\n')
        self._write_arguements(fh, columns, '', ['timestamp'], comments=True)
        fh.write('    */\n')
        self._writec_opy_args(fh, 'this.', columns, '', ['timestamp'])
        fh.write('\n    return this;\n')
        fh.write('  }\n\n')

        # string Table::_Name()
        self._write_js_method(fh, 'String: returns the name.', '_name', None)

        if mainClass:
            fh.write("    return '%s';\n  }\n\n" % tbl.name)
        elif keyClass:
            fh.write("    return '%sKey';\n  }\n\n" % tbl.name)
        else:
            fh.write("    return '%s';\n  }\n\n" % cls)

        # void clear()
        self._write_js_method(fh, None, '_clear', None,)
        self._write_clear_fields(fh, columns)
        fh.write('  }\n\n')

        self._write_js_method(fh, None, '_serialize', '_w, _oname')
        fh.write('    /**\n')
        fh.write('     * Serialize the object with a writer.\n')
        fh.write('     * @param _w     mettle.lib.Writer  : the writer object to use.\n')
        fh.write('     * @param _oname string             : optionally pass in a diff name for the object.\n')
        fh.write('     */\n')
        fh.write('    if (_oname == null)\n')
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
            elif a.type in ('date', 'datetime', 'time', 'timestamp'):
                fh.write('    _w.writeDateTime("%s", this.%s);' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('dbrec', 'this'):
                fh.write('    this.%s._serialize(_w);' % (self._member(a.name)))
            else:
                raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))

            fh.write('  if (_w._prom.broken()) return;\n')

        fh.write('\n    _w.writeEnd(_oname);  if (_w._prom.broken()) return;\n')
        fh.write('  }\n\n')

        # Struct._deserialize()
        self._write_js_method(fh, None, '_deserialize', '_r, _oname')
        fh.write('    /**\n')
        fh.write('     * Deserialize the object with a reader.\n')
        fh.write('     * @param _r     mettle.lib.Reader  : the reader object to use.\n')
        fh.write('     * @param _oname string             : optionally pass in a diff name for the object.\n')
        fh.write('     */\n')
        fh.write('    if (_oname == null)\n')
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
            elif a.type in ('date', 'datetime', 'time', 'timestamp'):
                fh.write('    this.%s = _r.readDateTime("%s");' % (self._member(a.name), self._member(a.name)))
            elif a.type in ('dbrec', 'this'):
                fh.write('    this.%s._deserialize(_r);' % (self._member(a.name)))
            else:
                raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))

            fh.write('  if (_r._prom.broken()) return;\n')

        fh.write('\n    _r.readEnd(_oname);  if (_r._prom.broken()) return;\n')
        fh.write('  }\n\n')

        self._write_js_method(fh, 'String', 'toString', None)
        self._write_str_print_fields(fh, columns)
        fh.write('  }\n\n')

        self._write_member_decleration(fh, columns)

        fh.write('}')
        self._tblPre = ',\n\n'

        if mainClass:
            self._write_couplets(fh, cls, columns)


    def _gen_custom_procs(self, fh):
        for proc in self._gen_info['table'].procs:
            if self._mode == self.TABLE:
                if proc.in_fields:
                    if len(proc.in_fields) != 1 or proc.in_fields[0].type != 'dbrec':
                        self._write_data_class(
                            fh,
                            self._pref_suf_name('class.qryin', '%s%s' % (self._gen_info['table'].name, proc.name)),
                            proc.in_fields)

                if proc.out_fields:
                    if len(proc.out_fields) != 1 or proc.out_fields[0].type != 'dbrec':
                        self._write_data_class(
                            fh,
                            self._pref_suf_name('class.qryout', '%s%s' % (self._gen_info['table'].name, proc.name)),
                            proc.out_fields)


    def _write_js_method(self,
                         fh,
                         returns,
                         method,
                         args = None,
                         ignoreTypes = [],
                         extraSpaces = '',
                         useDefaultVals = False,
                         methodDescr = ''):
        cstr  = '  %sthis.%s = function(' % (extraSpaces, method)
        comma = ''

        fh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguements(fh, args, len(cstr), ignoreTypes, useDefaultVals=useDefaultVals)
            elif type(args) == str:
                arr   = args.split(',')

                for a in arr:
                    fh.write('%s%s' % (comma, a))
                    comma = ', '

        fh.write(') {\n')

        if returns and args:
            fh.write('    %s/*\n' % extraSpaces)

            if methodDescr  != '':
                fh.write('    %s\n' % methodDescr)

            if type(args) == list:
                self._write_arguements(fh, args, len(cstr), ignoreTypes, comments = True, extraSpaces=extraSpaces)
            elif type(args) == str:
                arr   = args.split(',')
                for a in arr:
                    fh.write('    %s@param %s: ...\n' % (extraSpaces, a))

            if returns:
                fh.write('    %s@returns %s\n' % (extraSpaces, returns))

            fh.write('    %s*/\n'  % extraSpaces)


    def _write_arguements(self,
                          fh,
                          args,
                          spacing,
                          filter_out: list = None,
                          comments = False,
                          extraSpaces = '',
                          useDefaultVals = False):
        if not args:
            return

        nulls = []
        comma = ''

        for a in args:
            if filter_out:
                if a.type in filter_out:
                    continue

            fmap = self._field_map[a.type]

            if comments:
                paramComment = '...'
                fh.write("    %s@param %s %s: %s\n" % (extraSpaces, fmap.name, self._member(a.name), paramComment))

            else:
                fh.write('%s%s' % (comma, self._member(a.name)))

                if useDefaultVals:
                    if a.isArray:
                        fh.write(' = null')
                    else:
                        fh.write(' = %s' % fmap.def_value)

                if a.type.startswith('int') and a.notNull is False:
                    nulls.append(a)

            comma = ', '

        for a in nulls:
            if comments:
                fh.write("    %s@param %s bool: the column value is null.\n" % (extraSpaces, '%s_NULL' % self._member(a.name)))
            else:
                fh.write('%s%s' % (comma, '%s_NULL' % self._member(a.name)))

        del nulls


    def _writec_opy_args(self, fh, fromObj, args, toObj, fil = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fh.write('    %s%s = %s%s;\n' % (fromObj, self._member(a.name), toObj, self._member(a.name)))

            if a.type.startswith('int') and a.notNull is False:
                if toObj == '':
                    fh.write("    %s%s = typeof %s%s_NULL !== 'undefined' ? %s_NULL : false;\n" % (
                        fromObj, '%s_NULL' % self._member(a.name), toObj, self._member(a.name), self._member(a.name)))
                else:
                    fh.write('    %s%s = %s%s_NULL;\n' % (
                        fromObj, '%s_NULL' % self._member(a.name), toObj, self._member(a.name)))


    def _write_member_decleration(self, fh, members):
        for m in members:
            fmap = self._field_map[m.type]

            fh.write('  this.%s = %s;\n' % (self._member(m.name), fmap.def_value))

            if m.type.startswith('int') and m.notNull is False:
                fh.write('  this.%s_NULL = false;\n' % (self._member(m.name)))


    def _write_encapsualted_fields(self, fh, args, mask, fil = None, type_masks = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            memName = self._member(a.name)

            if type_masks:
                if a.type in type_masks:
                    fh.write(type_masks[a.type] % (memName, memName))
                else:
                    fh.write(mask % (memName, memName))
            else:
                fh.write(mask % (memName, memName))

            if a.type.startswith('int') and a.notNull is False:
                memName = '%s_NULL' % memName
                atype   = 'bool'

                if type_masks:
                    if atype in type_masks:
                        fh.write(type_masks[atype] % (memName, memName))
                    else:
                        fh.write(mask % (memName, memName))
                else:
                    fh.write(mask % ('%s_NULL' % memName, '%s_NULL' % memName))


    def _write_clear_fields(self, fh, args, fil = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            fh.write('    this.%s = %s;\n' % (self._member(a.name), fmap.def_value))

            if fmap.type_flag == 'int' and a.notNull is False:
                fh.write('    this.%s = false;\n' % ('%s_NULL' % self._member(a.name)))


    def _write_str_print_fields(self, fh, args):
        if not args:
            return

        fh.write('    return')
        delim = '"'

        for a in args:
            fh.write(' %s%s:" + this.%s' % (delim, self._member(a.name), self._member(a.name)))
            delim = '+ ", '


        fh.write(';\n')


    def _write_couplets(self, fh, cls, columns):

        for col in columns:
            if not col.couplets:
                continue

            fmap    = self._field_map[col.type]
            valMask = '  %-30s : "%s",\n'
            cpCls   = self._pref_suf_name('class.couplet', '%s%s' % (cls, col.name))

            fh.write('%s%s : {\n' % (self._tblPre, cpCls))

            if fmap.type_flag in ['str']:
                keyMask = '  %-30s : "%s",\n'
            else:
                keyMask = '  %-30s : %s,\n'

            for key, val in col.couplets.items():
                fh.write(keyMask % ('key_%s' % self._couplet_name(val), str(key)))

            fh.write('\n')

            for key, val in col.couplets.items():
                fh.write(valMask % ('value_%s' % self._couplet_name(val), str(val)))

            fh.write('\n')

            fh.write('  getDictionary : function() {\n')
            fh.write('    var dic = {};\n\n')

            for key, val in col.couplets.items():
                fh.write('    dic[this.key_%s] = this.value_%s;\n' % (self._couplet_name(val), self._couplet_name(val)))

            fh.write('\n      return dic;\n')
            fh.write('  },\n\n')

            fh.write('  getValue : function(keyId) {\n')

            for key, val in col.couplets.items():
                fh.write('    if (keyId == this.key_%s)\n' % self._couplet_name(val))
                fh.write('      return this.value_%s;\n\n' % self._couplet_name(val))

            fh.write('    return "";\n')
            fh.write('  }\n')
            fh.write('}')
