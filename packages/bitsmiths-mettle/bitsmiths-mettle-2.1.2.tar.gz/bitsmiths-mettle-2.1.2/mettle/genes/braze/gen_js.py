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

    def __init__(self):
        Generator.__init__(self, ['js'])

        self._field_map['bool']         = Generator.FieldMap('bool',    type_flag = 'bool',        def_val = 'false')
        self._field_map['int8']         = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['int16']        = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['int32']        = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['int64']        = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['uint8']        = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['uint16']       = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['uint32']       = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['uint64']       = Generator.FieldMap('number',  type_flag = 'int',         def_val = '0')
        self._field_map['char']         = Generator.FieldMap('string',  type_flag = 'str',         def_val = "''")
        self._field_map['string']       = Generator.FieldMap('string',  type_flag = 'str',         def_val = "''")
        self._field_map['date']         = Generator.FieldMap('Date',    type_flag = 'date',        def_val = 'new Date(0)')
        self._field_map['time']         = Generator.FieldMap('Date',    type_flag = 'date',        def_val = 'new Date(0)')
        self._field_map['datetime']     = Generator.FieldMap('Date',    type_flag = 'date',        def_val = 'new Date(0)')
        self._field_map['memblock']     = Generator.FieldMap('string',  type_flag = 'memblock',    def_val = 'null')
        self._field_map['uuid']         = Generator.FieldMap('string',  type_flag = 'str',         def_val = "''")
        self._field_map['json']         = Generator.FieldMap('string',  type_flag = 'str',         def_val = "''")
        self._field_map['double']       = Generator.FieldMap('decimal', type_flag = 'double',      def_val = '0.0')
        self._field_map['dbrec']        = Generator.FieldMap('struct',  type_flag = 'dbrec',       def_val = 'null')
        self._field_map['brazerec']     = Generator.FieldMap('struct',  type_flag = 'brazerec',    def_val = 'null')

        self._init_code_options({'jsonifyFriendly': 'off'})


    def name(self) -> str:
        return 'JavaScript'


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


    def _generate(self):
        if self._gen_info['clean']:
            self.clean(self._gen_info)
            return

        self._jsonifyFriendly = self.get_option('jsonifyFriendly').lower()

        if self._mode == self.STRUCT:
            fh = self.gened_file_open(self._gen_info, '%sStructs' % self._gen_info['proj'].name.lower())
            self._add_headers(fh)
            self._package = self._gen_begin_namespaces(fh, 'Structs')
            self._gen_braze_couplets(fh)
            self._gen_braze_structs(fh)
            self._gen_end_namespaces(fh)
            self.gened_file_close(fh)
        elif self._mode == self.CLIENT:
            fh = self.gened_file_open(self._gen_info, '%sClient' % self._gen_info['proj'].name.lower())
            self._add_headers(fh)
            self._package = self._gen_begin_namespaces(fh, 'Client')
            self._gen_client_marshaler(fh)
            self._gen_end_namespaces(fh)
            self.gened_file_close(fh)


    def _member(self, mem):
        if len(mem) < 2:
            return mem.lower()

        return '%s%s' % (mem[0].lower(), mem[1:])


    def _add_headers(self, fh):
        message = '// This file was generated by mettle.genes.braze.GenJs [ver %s] on %s\n\n' % (
            self._gen_info['version'], time.asctime())
        fh.write(message)


    def _writeJSMethod(self, fh, returns, method, args = None, extra_spaces = '', use_def_vals=False):
        cstr  = '  %sthis.%s = function(' % (extra_spaces, method)
        comma = ''

        fh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguements(fh, args, len(cstr), use_def_vals=use_def_vals)
            elif type(args) == str:
                arr   = args.split(',')

                for a in arr:
                    fh.write('%s%s' % (comma, a))
                    comma = ', '

        fh.write(') {\n')

        if returns and args:
            fh.write('    %s/*\n' % extra_spaces)

            if type(args) == list:
                self._write_arguements(fh, args, len(cstr), comments = True, extra_spaces=extra_spaces)
            elif type(args) == str:
                arr   = args.split(',')
                for a in arr:
                    fh.write('    %s * :param %s: ...\n' % (extra_spaces, a))

            if returns:
                fh.write('    %s@returns %s\n' % (extra_spaces, returns))

            fh.write('    %s*/\n'  % extra_spaces)


    def _write_arguements(self, fh, args, spacing, comments = False, extra_spaces = '', use_def_vals = False):
        if not args:
            return

        comma = ''

        for a in args:
            fmap = self._field_map[a.type]

            if comments:
                if a.is_array:
                    if fmap.type_flag == 'brazerec':
                        fh.write("    %s * :param %s %s.%s array: ...\n" % (
                            extra_spaces,
                            self._member(a.name),
                            self._package,
                            self._pref_suf_name('braze.struct', a.brazestruct.struct_name())))
                    elif fmap.type_flag == 'dbrec':
                        fh.write("    %s * :param %s %s array: ...\n" % (extra_spaces,
                                                                         self._member(a.name),
                                                                         a.dbstruct.struct_name()))
                    else:
                        fh.write("    %s * :param %s %s array ...\n" % (extra_spaces,
                                                                        self._member(a.name),
                                                                        self._member(a.type).capitalize()))
                else:
                    if fmap.type_flag == 'brazerec':
                        fh.write("    %s:param %s %s.%s: ...\n" % (
                            extra_spaces,
                            self._member(a.name),
                            self._package,
                            self._pref_suf_name('braze.struct', a.brazestruct.struct_name())))
                    elif fmap.type_flag == 'dbrec':
                        fh.write("    %s * :param %s %s: ...\n" % (extra_spaces,
                                                                   self._member(a.name),
                                                                   a.dbstruct.struct_name()))
                    else:
                        fh.write("    %s * :param %s %s: ...\n" % (extra_spaces, self._member(a.name), fmap.name))

            else:
                fh.write('%s%s' % (comma, self._member(a.name)))

                if use_def_vals:
                    if a.is_array:
                        fh.write(' = null')
                    else:
                        fh.write(' = %s' % fmap.def_val)

            comma = ', '


    def _writec_opy_args(self, fh, fromObj, args, toObj = '', fil = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            if fmap.type_flag == 'date':
                fh.write('    %s%s = new Date(%s%s.valueOf());\n' % (fromObj,
                                                                     self._member(a.name),
                                                                     toObj,
                                                                     self._member(a.name)))
            else:
                fh.write('    %s%s = %s%s;\n' % (fromObj, self._member(a.name), toObj, self._member(a.name)))


    def _write_init_fields(self, fh, fromObj, args):
        if not args:
            return

        for a in args:
            fmap = self._field_map[a.type]

            if a.is_array:
                if self._jsonifyFriendly == "on":
                    if fmap.type_flag == 'brazerec':
                        fh.write('  %s%s = [];\n' % (fromObj, self._member(a.name)))
                    elif fmap.type_flag == 'dbrec':
                        fh.write('  %s%s = [];\n' % (fromObj, self._member(a.name)))
                    else:
                        fh.write('  %s%s = [];\n' % (fromObj, self._member(a.name)))
                else:
                    if fmap.type_flag == 'brazerec':
                        fh.write('  %s%s = new mettle.braze.List(%s.%s);\n' % (
                            fromObj,
                            self._member(a.name),
                            self._package,
                            self._pref_suf_name('braze.struct', a.brazestruct.struct_name())))
                    elif fmap.type_flag == 'dbrec':
                        fh.write('  %s%s = new mettle.braze.List(%s);\n' % (
                            fromObj, self._member(a.name), a.dbstruct.struct_name()))
                    else:
                        fh.write('  %s%s = new mettle.braze.List(mettle.braze.BrazeType.%s);\n' % (
                            fromObj, self._member(a.name), a.type.capitalize()))

            else:
                if fmap.type_flag == 'brazerec':
                    fh.write('  %s%s = new %s.%s();\n' % (
                        fromObj,
                        self._member(a.name),
                        self._package,
                        self._pref_suf_name('braze.struct', a.brazestruct.struct_name())))
                elif fmap.type_flag == 'dbrec':
                    fh.write('  %s%s = new %s();\n' % (fromObj, self._member(a.name), a.dbstruct.struct_name()))
                else:
                    fh.write('  %s%s = %s;\n' % (fromObj, self._member(a.name), fmap.def_val))

    def _write_clear_fields(self, fh, args, fil = None):
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


    def _write_str_print_fields(self, fh, args):
        if not args:
            return

        fh.write('    return')
        delim = '"'

        for a in args:
            fh.write(' %s%s:" + this.%s' % (delim, self._member(a.name), self._member(a.name)))
            delim = '+ ", '
            fmap   = self._field_map[a.type]

            if a.is_array:
                fh.write(".length()")
            elif fmap.type_flag == 'dbrec':
                fh.write("._name()" )
            elif fmap.type_flag == 'brazerec':
                fh.write("._name()")

        fh.write(';\n')


    def _gen_begin_namespaces(self, fh, name):
        ns = self._namespace()
        np = ns.split('.')
        ns = '%s%s' % (np[0], name)

        fh.write('var %s = {' % (ns))

        for sp in np[1:]:
            fh.write(' %s : {' % sp)

        fh.write('\n\n')

        return ns


    def _gen_end_namespaces(self, fh):
        ns = self._namespace()

        fh.write('\n\n')

        for x in ns.split('.'):
            fh.write('}')

        fh.write(';\n')


    def _gen_braze_couplets(self, fh):
        if len(self._gen_info['proj'].couplets) < 1:
            return

        pre = ''

        for x, cobj in self._gen_info['proj'].couplets.items():
            cpCls = self._pref_suf_name('braze.couplet', cobj.name)

            fmap    = self._field_map[cobj.ctype]
            keyMask = ''
            valMask = '  %-30s : "%s",\n'

            fh.write('%s%s : {\n\n' % (pre, cpCls))

            if fmap.type_flag in ['str']:
                keyMask = '  %-30s : "%s",\n'
            else:
                keyMask = '  %-30s : %s,\n'

            for key, val in cobj.couplet.items():
                fh.write(keyMask % ('key_%s' % self._couplet_name(val), str(key)))

            fh.write('\n')

            for key, val in cobj.couplet.items():
                fh.write(valMask % ('value_%s' % self._couplet_name(val), str(val)))

            fh.write('\n')
            fh.write('  getDictionary : function() {\n')
            fh.write('    var dic = {};\n\n')

            for key, val in cobj.couplet.items():
                fh.write('    dic[this.key_%s] = this.value_%s;\n' % (self._couplet_name(val), self._couplet_name(val)))

            fh.write('\n    return dic;\n')
            fh.write('  },\n\n')

            fh.write('  getValue : function(keyId) {\n')

            for key, val in cobj.couplet.items():
                fh.write('    if (keyId == this.key_%s)\n' % self._couplet_name(val))
                fh.write('      return this.value_%s;\n\n' % self._couplet_name(val))

            fh.write('    return "";\n')
            fh.write('  }\n')
            fh.write('}')
            pre = ',\n\n'


    def _gen_braze_structs(self, fh):
        pre = ''

        if len(self._gen_info['proj'].couplets) > 0:
            pre = ',\n\n'

        for s in self._gen_info['proj'].struct_order:
            sobj      = self._gen_info['proj'].structs[s]
            sname     = self._pref_suf_name('braze.struct', '%s' % (sobj.name))

            fh.write('%s%s : function() {\n\n' % (pre, sname))

            # Struct.Struct()
            self._writeJSMethod(fh, None, '_init', 'rec')
            fh.write('    /**\n')
            fh.write('     * Copy Constructor.\n')
            fh.write('     * :param rec %s: rec to copy from.\n' % sname)
            fh.write('     */\n')
            self._writec_opy_args(fh, 'this.', sobj.fields, 'rec.')
            fh.write('\n    return this;\n')
            fh.write('  }\n\n')

            # Struct.Struct()
            self._writeJSMethod(fh, None, '_initDeft', sobj.fields)
            fh.write('    /**\n')
            fh.write('     * Deft Constructor.\n')
            self._write_arguements(fh, sobj.fields, '', comments=True)
            fh.write('     */\n')
            self._writec_opy_args(fh, 'this.', sobj.fields)
            fh.write('\n    return this;\n')
            fh.write('  }\n\n')

            # void Struct.clear()
            self._writeJSMethod(fh, None, '_clear', None)
            fh.write('    /**\n')
            fh.write('     * Clear all object values.\n')
            fh.write('     */\n')
            self._write_clear_fields(fh, sobj.fields)
            fh.write('  }\n\n')

            # string Struct._name()
            self._writeJSMethod(fh, 'String', '_name', None)
            fh.write('    /**\n')
            fh.write('     * The default object name.\n')
            fh.write('     */\n')
            fh.write("    return '%s';\n  }\n\n" % sname)

            # Struct._serialize()
            self._writeJSMethod(fh, None, '_serialize', '_w, _oname')
            fh.write('    /**\n')
            fh.write('     * Serialize the object with a writer.\n')
            fh.write('     * :param _w     mettle.lib.Writer  : the writer object to use.\n')
            fh.write('     * :param _oname string             : optionally pass in a diff name for the object.\n')
            fh.write('     */\n')
            fh.write('    if (_oname == null)\n')
            fh.write('      _oname = this._name();\n\n')
            fh.write('    _w.writeStart(_oname);  if (_w._prom.broken()) return;\n\n')

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        fh.write('    this.%s._serialize(_prom, _w, "%s");' % (a.name, a.name))
                    else:
                        if a.type in ['int32', 'int64', 'int16', 'int8', 'uint32', 'uint64', 'uint16', 'uint8']:
                            fh.write('    _w.writeInt("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['string', 'uuid']:
                            fh.write('    _w.writeString("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['char']:
                            fh.write('    _w.writeChar("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['bool']:
                            fh.write('    _w.writeBool("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['double']:
                            fh.write('    _w.writeFloat("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['memblock']:
                            fh.write('     _w.writeByteArray("%s", this.%s);' % (a.name, a.name))
                        elif a.type in ['date', 'datetime', 'time']:
                            fh.write('    _w.writeDateTime("%s", this.%s);' % (a.name, a.name))
                        else:
                            raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))

                    fh.write('  if (_w._prom.broken()) return;\n')

            fh.write('\n    _w.writeEnd(_oname);  if (_w._prom.broken()) return;\n')
            fh.write('  }\n\n')

            # Struct._deserialize()
            self._writeJSMethod(fh, None, '_deserialize', '_r, _oname')
            fh.write('    /**\n')
            fh.write('     * Deserialize the object with a reader.\n')
            fh.write('     * :param _r     mettle.lib.Reader  : the reader object to use.\n')
            fh.write('     * :param _oname string             : optionally pass in a diff name for the object.\n')
            fh.write('     */\n')
            fh.write('    if (_oname == null)\n')
            fh.write('      _oname = this._name();\n\n')
            fh.write('    _r.readStart(_oname);  if (_r._prom.broken()) return;\n\n')

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        fh.write('    this.%s._deserialize(_r, "%s");' % (a.name, a.name))
                    else:
                        if a.type in ['int32', 'int64', 'int16', 'int8', 'uint32', 'uint64', 'uint16', 'uint8']:
                            fh.write('    this.%s = _r.readInt("%s");' % (a.name, a.name))
                        elif a.type in ['string', 'uuid']:
                            fh.write('    this.%s = _r.readString("%s");' % (a.name, a.name))
                        elif a.type in ['char']:
                            fh.write('    this.%s = _r.readChar("%s");' % (a.name, a.name))
                        elif a.type in ['bool']:
                            fh.write('    this.%s = _r.readBool("%s");' % (a.name, a.name))
                        elif a.type in ['double']:
                            fh.write('    this.%s = _r.readFloat("%s");' % (a.name, a.name))
                        elif a.type in ['memblock']:
                            fh.write('    this.%s = _r.readByteArray("%s");' % (a.name, a.name))
                        elif a.type in ['date', 'datetime', 'time']:
                            fh.write('    this.%s = _r.readDateTime("%s");' % (a.name, a.name))
                        else:
                            raise Exception('Unknown type [%s] for field [%s]' % (a.type, a.name))

                    fh.write('  if (_r._prom.broken()) return;\n')

            fh.write('\n    _r.readEnd(_oname);  if (_r._prom.broken()) return;\n')
            fh.write('  }\n\n')

            # string Struct.toString()
            self._writeJSMethod(fh, 'String', 'toString', None)
            self._write_str_print_fields(fh, sobj.fields)
            fh.write('  }\n\n')

            self._write_init_fields(fh, 'this.', sobj.fields)

            fh.write('}')

            pre = ',\n\n'


    def _gen_client_marshaler(self, fh):
        cls               = self._pref_suf_name('client.marshaler', self._gen_info['proj'].name)
        self._clientClass = cls

        # ?? self._gen_struct_imports(fh)

        # Class & Constrcutor
        fh.write('%s : function(client) {\n\n' % (self._clientClass))

        fh.write('  this.__init__ = function(client) {\n')
        fh.write('    /**\n')
        fh.write('     * Constructor.\n')
        fh.write('     * :param client mettle.braze.Client: braze client object.\n')
        fh.write('     */\n')
        fh.write('    this._client = client\n')
        fh.write('  }\n\n')

        fh.write('  this._name = function() {\n')
        fh.write('    /**\n')
        fh.write('     *The braze service name.\n')
        fh.write('     *:return string: the name of this braze service.\n')
        fh.write('     */\n')
        fh.write("    return '%s';\n" % self._gen_info['proj'].name)
        fh.write('  }\n\n')

        fh.write('  this._signature = function() {\n')
        fh.write('    /**\n')
        fh.write('     * Gets the client signature.\n')
        fh.write('     * :return str: the signature of this client.\n')
        fh.write('     */\n')
        fh.write('    return "%s";\n' % self._gen_info['server_sig'])
        fh.write('  }\n\n')


        for call in self._gen_info['proj'].calls:

            fh.write('  this.%s = function(_prom' % call.name)

            delim = ', '

            for f in call.fields:
                fh.write('%s%s' % (delim, f.name))

            fh.write(') {\n')

            return_type  = self._gen_return_type_str(call)
            args         = self._gen_param_str(call)

            fh.write('    /**\n')
            fh.write('     * :param _prom mettle.lib.Promise: the promise to keep or break.\n')

            for a in args:
                fh.write('     * :param %s %s: %s\n' % (a[0], a[1], a[2]))

            if return_type:
                fh.write('     * @return %s: result\n' % return_type)

            fh.write('     */\n')

            self._gen_client_declare_varibles(fh, call)
            self._gen_client_assign_input_args(fh, call)
            self._gen_client_server_call(fh, call)
            self._gen_client_assign_output_args(fh, call)

            fh.write('\n      return _prom.keep(_x);\n')
            fh.write('    });\n')
            fh.write('  }\n\n')


        fh.write('  this.__init__(client);\n')
        fh.write('}')


    def _gen_return_type_str(self, call):
        if not call.returns:
            return None

        if call.returns.is_array:

            if call.returns.type == 'brazerec':
                return '%s.%s.List ' % (
                    self._package, self._pref_suf_name('braze.struct', call.returns.brazestruct.struct_name()))

            if call.returns.type == 'dbrec':
                return '%s.List ' % call.returns.dbstruct.struct_name()

            if call.returns.type == 'memblock':
                return 'mettle.braze.MemblockList '

            return 'mettle.braze.%s%sList ' % (call.returns.type[0].upper(), call.returns.type[1:])


        if call.returns.type == 'brazerec':
            return '%s.%s' % (self._package, self._pref_suf_name('braze.struct', call.returns.brazestruct.struct_name()))

        if call.returns.type == 'dbrec':
            return '%s' % call.returns.dbstruct.struct_name()

        fmap = self._field_map[call.returns.type]

        return fmap.name


    def _gen_param_str(self, call):
        args = []

        for f in call.fields:
            param = [f.name, '', '']
            args.append(param)

            if f.io == 'i':
                param[2]  = 'input'
            elif f.io == 'o':
                param[2]  = 'output'
            else:
                param[2]  = 'input/output'

            fmap = self._field_map[f.type]

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    param[1] = '%s.%s.List' % (
                        self._package, self._pref_suf_name('braze.struct', f.brazestruct.struct_name()))
                elif fmap.type_flag == 'dbrec':
                    param[1] = '%s.List' % (f.dbstruct.struct_name())
                else:
                    if f.type == 'memblock':
                        param[1] = 'mettle.braze.MemblockList'
                    else:
                        param[1] = 'mettle.braze.%s%sList' % (f.type[0].upper(), f.type[1:])
                continue

            if fmap.type_flag == 'brazerec':
                param[1] = '%s.%s' % (self._package, self._pref_suf_name('braze.struct', f.brazestruct.struct_name()))
            elif fmap.type_flag == 'dbrec':
                param[1] = f.dbstruct.struct_name()
            else:
                param[1] = fmap.name

        return args


    def _gen_client_declare_varibles(self, fh, call):
        fh.write('    var %s = new mettle.io.ListStream(_prom);\n' % '_i')
        fh.write('    var %s = null;\n' % '_o')

        call.hasInput   = False
        call.hasOutput  = False

        for f in call.fields:
            if f.io in ['i', 'io']:
                fh.write('    var %s = null;\n' % '_w')
                call.hasInput = True
                break

        for f in call.fields:
            if f.io in ['o', 'io']:
                fh.write('    var %s = null;\n' % '_r')
                call.hasOutput = True
                break

        if call.returns and call.hasOutput:
            fh.write('    var %s = null;\n' % '_r')
            call.hasOutput = True

        fh.write('    var %s = null;\n' % '_x')
        fh.write('\n')


    def _gen_client_assign_input_args(self, fh, call):
        if not call.hasInput:
            return

        fh.write('    _w = this._client.newWriter(_prom, _i);\n')
        fh.write('    _w.writeStart("%s_IN"); if (_prom.broken()) return;\n' % (call.name))

        for f in call.fields:
            if f.io == 'o':
                continue

            fmap = self._field_map[f.type]

            if fmap.type_flag in ['brazerec', 'dbrec'] or f.is_array:
                fh.write('    %s._serialize(_w); if (_prom.broken()) return;\n' % (f.name))
                continue

            fname = f.name

            if f.type in ['int32', 'int16', 'int64', 'int8', 'uint32', 'uint16', 'uint64', 'uint8']:
                fh.write('    _w.writeInt("%s", %s);' % (f.name, fname))
            elif f.type in ['string', 'uuid']:
                fh.write('    _w.writeString("%s", %s);' % (f.name, fname))
            elif f.type in ['char']:
                fh.write('    _w.writeChar("%s", %s);' % (f.name, fname))
            elif f.type in ['bool']:
                fh.write('    _w.writeBool("%s", %s);' % (f.name, fname))
            elif f.type in ['double']:
                fh.write('    _w.writeFloat("%s", %s);' % (f.name, fname))
            elif f.type in ['memblock']:
                fh.write('    _w.writeByteArray("%s", %s);' % (f.name, fname))
            elif f.type in ['date', 'datetime', 'time']:
                fh.write('    _w.writeDateTime("%s", %s);' % (f.name, fname))
            else:
                raise Exception('Unknown type [%s] for field [%s]' % (f.type, f.name))

            fh.write("  if (_prom.broken()) return;\n")

        fh.write('    _w.writeEnd("%s_IN"); if (_prom.broken()) return;\n' % (call.name))
        fh.write('\n')


    def _gen_client_server_call(self, fh, call):
        sig = call.signature

        fh.write('    this._client.send(_prom, this, "%s", _i, function(marsh, _prom, _o) {\n'  % (sig))
        fh.write('      if (_prom.broken()) return;\n')


    def _gen_client_assign_output_args(self, fh, call):
        if not call.hasOutput:
            return

        fh.write('\n      _r = marsh._client.newReader(_prom, _o);\n')
        fh.write('      _r.readStart("%s_OUT"); if (_prom.broken()) return;\n' % call.name)
        fh.write('      _x = Object();\n')

        if call.returns:
            f     = call.returns
            fmap  = self._field_map[f.type]
            fname = "return"

            fh.write("      _x.result = ")

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    fh.write('new mettle.braze.List(%s.%s);\n' % (
                        self._package, self._pref_suf_name('braze.struct', f.brazestruct.struct_name())))
                elif fmap.type_flag == 'dbrec':
                    fh.write('new mettle.braze.List(%s);\n' % (f.dbstruct.struct_name()))
                else:
                    fh.write('new mettle.braze.List(%s);\n' % self._member(f.type).capitalize())

                fh.write("      _x.result._deserialize(_r); if (_prom.broken()) return;\n")
            else:
                if fmap.type_flag == 'brazerec':
                    fh.write('new %s.%s();\n' % (
                        self._package, self._pref_suf_name('braze.struct', f.brazestruct.struct_name())))
                    fh.write("      _x.result._deserialize(_r);")
                elif fmap.type_flag == 'dbrec':
                    fh.write('new %s();\n' % f.dbstruct.struct_name())
                    fh.write("      _x.result._deserialize(_r);")
                else:
                    if f.type in ['int32', 'int16', 'int64', 'int8', 'uint32', 'uint16', 'uint64', 'uint8']:
                        fh.write('_r.readInt("%s");' % (fname))
                    elif f.type in ['string', 'uuid']:
                        fh.write('_r.readString("%s");' % (fname))
                    elif f.type in ['char']:
                        fh.write('_r.readChar("%s");' % (fname))
                    elif f.type in ['bool']:
                        fh.write('_r.readBool("%s");' % (fname))
                    elif f.type in ['double']:
                        fh.write('_r.readFloat("%s");' % (fname))
                    elif f.type in ['memblock']:
                        fh.write('_r.readByteArray("%s");' % (fname))
                    elif f.type in ['date', 'datetime', 'time']:
                        fh.write('_r.readDateTime("%s");' % (fname))
                    else:
                        raise Exception('Unknown type [%s] for field [%s]' % (f.type, f.name))

                fh.write("  if (_prom.broken()) return;\n")


        for f in call.fields:
            if f.io == 'i':
                continue

            fmap = self._field_map[f.type]

            fh.write("      _x.%s = " % (f.name))

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    fh.write('new mettle.braze.List(%s.%s);\n' % (
                        self._package, self._pref_suf_name('braze.struct', f.brazestruct.struct_name())))
                elif fmap.type_flag == 'dbrec':
                    fh.write('new mettle.braze.List(%s);\n' % (f.dbstruct.struct_name()))
                else:
                    fh.write('new mettle.braze.List(%s);\n' % self._member(f.type).capitalize())
                fh.write("      _x.%s._deserialize(_r); if (_prom.broken()) return;\n" % (f.name))
            else:
                if fmap.type_flag == 'brazerec':
                    fh.write('new %s.%s();\n' % (
                        self._package, self._pref_suf_name('braze.struct', f.brazestruct.struct_name())))
                    fh.write("      _x.%s._deserialize(_r);" % f.name)
                elif fmap.type_flag == 'dbrec':
                    fh.write('new %s();\n' % f.dbstruct.struct_name())
                    fh.write("      _x.%s._deserialize(_r);" % f.name)
                else:
                    if f.type in ['int32', 'int16', 'int64', 'int8', 'uint32', 'uint16', 'uint64', 'uint8']:
                        fh.write('_r.readInt("%s");' % (f.name))
                    elif f.type in ['string', 'uuid']:
                        fh.write('_r.readString("%s");' % (f.name))
                    elif f.type in ['char']:
                        fh.write('_r.readChar("%s");' % (f.name))
                    elif f.type in ['bool']:
                        fh.write('_r.readBool("%s");' % (f.name))
                    elif f.type in ['double']:
                        fh.write('_r.readFloat("%s");' % (f.name))
                    elif f.type in ['memblock']:
                        fh.write('_r.readByteArray("%s");' % (f.name))
                    elif f.type in ['date', 'datetime', 'time']:
                        fh.write('_r.readDateTime("%s");' % (f.name))
                    else:
                        raise Exception('Unknown type [%s] for field [%s]' % (f.type, f.name))

                fh.write("  if (_prom.broken()) return;\n")

        fh.write('      _r.readEnd("%s_OUT"); if (_prom.broken()) return;\n' % call.name)
