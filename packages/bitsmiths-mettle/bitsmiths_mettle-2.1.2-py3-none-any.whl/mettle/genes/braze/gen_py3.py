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


class GenPy3(Generator):

    def __init__(self):
        Generator.__init__(self, ['py'])

        self._field_map['bool']      = Generator.FieldMap('bool',              type_flag = 'bool',        def_val = 'False')
        self._field_map['int8']      = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['int16']     = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['int32']     = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['int64']     = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['uint8']     = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['uint16']    = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['uint32']    = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['uint64']    = Generator.FieldMap('int',               type_flag = 'int',         def_val = '0')
        self._field_map['char']      = Generator.FieldMap('str',               type_flag = 'str',         def_val = "''")
        self._field_map['string']    = Generator.FieldMap('str',               type_flag = 'str',         def_val = "''")
        self._field_map['date']      = Generator.FieldMap('datetime.date',     type_flag = 'date',        def_val = 'datetime.date.min')      # noqa
        self._field_map['time']      = Generator.FieldMap('datetime.time',     type_flag = 'date',        def_val = 'datetime.time.min')      # noqa
        self._field_map['datetime']  = Generator.FieldMap('datetime.datetime', type_flag = 'date',        def_val = 'datetime.datetime.min')  # noqa
        self._field_map['memblock']  = Generator.FieldMap('bytearray',         type_flag = 'memblock',    def_val = "b''")
        self._field_map['uuid']      = Generator.FieldMap('uuid.UUID',         type_flag = 'uuid',        def_val = "None")
        self._field_map['json']      = Generator.FieldMap('string',            type_flag = 'str',         def_val = "''")
        self._field_map['double']    = Generator.FieldMap('float',             type_flag = 'double',      def_val = '0.0')
        self._field_map['dbrec']     = Generator.FieldMap('struct',            type_flag = 'dbrec',       def_val = 'None')
        self._field_map['brazerec']  = Generator.FieldMap('struct',            type_flag = 'brazerec',    def_val = 'None')

        self._init_code_options()

        self._async = {
            'await' : '',
            'async' : '',
            'class' : '',
        }


    def name(self) -> str:
        return 'Python3'


    def initialize_generation(self, gen_info):
        pass


    def finalize_generation(self, gen_info):
        """
        Create all the __init__.py files in the namespace directories.
        """

        if gen_info['clean']:
            return

        nap    = gen_info['proj'].project_dir
        nsdir  = os.path.join(nap, self.dest_dir).replace('\\', os.path.sep).replace('/', os.path.sep).replace('|', os.path.sep)
        ns     = self._namespace()
        fh     = None

        nsFile = os.path.join(nsdir, '__init__.py')
        fh     = open(nsFile, 'wt')

        self._add_headers(fh)

        for gf in self._gened_files[ns]:
            fh.write('from .%s import %s\n' % (gf.fname, gf.cls))

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
        self._gen_info = gen_info
        self._mode    = self.SERVER
        self._generate()


    def _generate(self):
        if self._gen_info['clean']:
            self.clean(self._gen_info)
            return

        self._package = self._namespace()
        self._async   = {
            'await' : '',
            'async' : '',
            'class' : '',
        }

        if self._mode == self.STRUCT:
            self._gen_braze_couplets()
            self._gen_braze_structs()
        elif self._mode == self.CLIENT:
            self._gen_client_interface()
            self._gen_client_marshaler()
            self._gen_client_server_impl()
        elif self._mode == self.SERVER:
            self._gen_server_interface()
            self._gen_server_marshaler()

            self._async   = {
                'await' : 'await ',
                'async' : 'async ',
                'class' : 'Async',
            }

            self._gen_server_interface()
            self._gen_server_marshaler()


    def _member(self, mem):
        return self._ident_member(mem)


    def _add_headers(self, fh):
        message = '# This file was generated by mettle.genes.braze.GenPy3 [ver %s] on %s\n#\n\n' % (
            self._gen_info['version'], time.asctime())

        fh.write(message)


    def _write_copy_args(self, fh, from_obj, args: list, to_obj, filter_args: list = None):
        if not args:
            return

        for a in args:
            if filter_args and a.type in filter_args:
                continue

            fmap = self._field_map[a.type]

            if a.is_array:
                if fmap.type_flag == 'brazerec':
                    fh.write('        %s%s = %s%s if not %s%s is None else %s.List()\n' % (
                        from_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        to_obj, self._member(a.name),
                        self._ident('braze.struct', a.brazestruct.struct_name())))
                elif fmap.type_flag == 'dbrec':
                    fh.write('        %s%s = %s%s if not %s%s is None else %s.List()\n' % (
                        from_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        a.dbstruct.struct_name()))
                elif fmap.type_flag == 'uuid':
                    fh.write('        %s%s = %s%s if not %s%s is None else mettle.braze.GuidList()\n' % (
                        from_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name)))
                else:
                    fh.write('        %s%s = %s%s if not %s%s is None else mettle.braze.%sList()\n' % (
                        from_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        self._member(a.type).capitalize()))

            else:
                if fmap.type_flag == 'brazerec':
                    fh.write('        %s%s = %s%s if not %s%s is None else %s()\n' % (
                        from_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        self._ident('braze.struct', a.brazestruct.struct_name())))
                elif fmap.type_flag == 'dbrec':
                    fh.write('        %s%s = %s%s if not %s%s is None else %s()\n' % (
                        from_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name),
                        a.dbstruct.struct_name()))
                else:
                    fh.write('        %s%s = %s%s\n' % (
                        from_obj,
                        self._member(a.name),
                        to_obj,
                        self._member(a.name)))


    def _write_clear_fields(self, fh, args: list, filter_args: list = None):
        if not args:
            return

        for a in args:
            if filter_args and a.type in filter_args:
                continue

            fmap = self._field_map[a.type]

            if a.is_array or fmap.type_flag in ['dbrec', 'brazerec']:
                fh.write('        self.%s.%s()\n' % (self._member(a.name), self._ident_method('Clear')))
            else:
                fh.write('        self.%s = %s\n' % (self._member(a.name), fmap.def_val))


    def _write_repr_method(self, fh, name: str, args: list):
        if not args:
            return

        fh.write("        return '<%s [" % name)

        delim = ''

        for a in args:
            fh.write('%s%s:'  % (delim, self._member(a.name)))
            fmap  = self._field_map[a.type]
            delim = ", "

            if a.is_array:
                fh.write('%r')
            elif fmap.type_flag in ('str', 'json', 'memblock'):
                fh.write('%.32s')
            elif fmap.type_flag in ('date'):
                fh.write('%s')
            else:
                fh.write('%r')

        fh.write("]>' % (\n")
        fh.write('            ')
        delim = ''

        for a in args:
            fh.write('%sself.%s'  % (delim, self._member(a.name)))
            delim = ", "

        fh.write(')\n')


    def _gen_imports(self, fh, fields: list = None):
        fh.write('import datetime\n')
        fh.write('import uuid\n')

        fh.write('import mettle.braze\n')
        fh.write('import mettle.lib\n\n')


    def _gen_braze_couplets(self):
        if len(self._gen_info['proj'].couplets) < 1:
            return

        for x, cobj in self._gen_info['proj'].couplets.items():
            cpCls = self._ident('braze.couplet', cobj.name)
            fh    = self.gened_file_open(self._gen_info,
                                         self._ident('file.couplet', cobj.name),
                                         cls = cpCls,
                                         add_namespace_to_path = False)

            self._add_headers(fh)

            fmap    = self._field_map[cobj.ctype]
            keyMask = ''
            valMask = '    %s = "%s"\n'

            fh.write('class %s(dict):\n\n' % cpCls)

            if fmap.type_flag in ['str']:
                keyMask = '    %s = "%s"\n'
            else:
                keyMask = '    %s = %s\n'

            for key, val in cobj.couplet.items():
                fh.write(keyMask % (self._member('Key%s' % self._couplet_name(val)), str(key)))

            fh.write('\n')

            for key, val in cobj.couplet.items():
                fh.write(valMask % (self._ident_method('Value%s' % self._couplet_name(val)), str(val)))

            fh.write('\n')
            fh.write('    def __init__(self):\n')
            for key, val in cobj.couplet.items():
                kname = self._member('Key%s' % self._couplet_name(val))
                vname = self._member('Value%s' % self._couplet_name(val))
                fh.write('        self[self.%s] = self.%s\n' % (kname, vname))
            fh.write('\n')

            fh.write('    @staticmethod\n')
            fh.write('    def %s(key):\n' % (self._ident_method('GetValue')))
            for key, val in cobj.couplet.items():
                kname = self._member('Key%s' % self._couplet_name(val))
                vname = self._member('Value%s' % self._couplet_name(val))
                fh.write('        if key == %s.%s:\n' % (cpCls, kname))
                fh.write('            return %s.%s\n\n' % (cpCls, vname))
            fh.write('        return ""\n\n')

            self.gened_file_close(fh)


    def _gen_braze_structs(self):
        for s in self._gen_info['proj'].struct_order:
            sobj      = self._gen_info['proj'].structs[s]
            sname     = self._ident('braze.struct', sobj.name)
            fh        = self.gened_file_open(self._gen_info,
                                             self._ident('file.struct', sobj.name),
                                             add_namespace_to_path = False,
                                             cls = sname)

            self._add_headers(fh)
            self._gen_imports(fh, sobj.fields)

            fh.write('from mettle.io.iserializable import ISerializable\n\n')

            if sobj.fields:
                added = []

                for a in sobj.fields:
                    fmap = self._field_map[a.type]

                    if fmap.type_flag == 'brazerec':
                        name = self._ident('braze.struct', a.brazestruct.struct_name())
                        imp  = '.%s' % (self._ident('file.struct', a.brazestruct.struct_name()))
                    elif fmap.type_flag == 'dbrec':
                        name = a.dbstruct.struct_name()
                        imp  = a.dbstruct.struct_path()
                    else:
                        continue

                    if imp in added:
                        continue

                    added.append(imp)

                    fh.write('from %s import %s\n' % (imp, name))

                if len(added) > 0:
                    fh.write('\n')


            fh.write('class %s(ISerializable):\n' % sname)

            if sobj.get_descr():
                fh.write('    """\n')
                fh.write('    %s\n' % sobj.get_descr())
                fh.write('    """\n')

            fh.write('\n')

            # Struct.Struct()
            self._write_py_method(fh,
                                  None,
                                  '__init__',
                                  self._gen_arg_items(sobj.fields, True),
                                  use_default_vals=True,
                                  method_descr = 'Constructor.')

            self._write_copy_args(fh, 'self.', sobj.fields, '')
            fh.write('\n')

            # void Struct.clear()
            self._write_py_method(fh, None, self._ident_method('Clear'), None)
            self._write_clear_fields(fh, sobj.fields)
            fh.write('\n')

            # string Struct._name()
            self._write_py_method(fh, 'str: Name of the struct', '_name', None, method_descr = 'Get the struct name.')
            fh.write("        return '%s'\n\n" % sname)

            # Struct._serialize()
            self._write_py_method(fh,
                                  None,
                                  '_serialize',
                                  '_w: mettle.io.IWriter, _oname: str = None',
                                  method_descr = 'Serialize this struct.')

            fh.write('        if not _oname:\n')
            fh.write('            _oname = self._name()\n\n')
            fh.write('        _w.write_start(_oname)\n')

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        fh.write('        self.%s._serialize(_w, "%s")\n' % (self._member(a.name), a.name))
                    else:
                        if a.type in ['int32']:
                            fh.write('        _w.write_int32("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['int64']:
                            fh.write('        _w.write_int64("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['int16']:
                            fh.write('        _w.write_int16("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['int8']:
                            fh.write('        _w.write_int8("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['uint32']:
                            fh.write('        _w.write_uint32("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['uint64']:
                            fh.write('        _w.write_uint64("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['uint16']:
                            fh.write('        _w.write_uint16("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['uint8']:
                            fh.write('        _w.write_uint8("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['string']:
                            fh.write('        _w.write_string("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['char']:
                            fh.write('        _w.write_char("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['bool']:
                            fh.write('        _w.write_bool("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['double']:
                            fh.write('        _w.write_double("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['memblock']:
                            fh.write('        _w.write_bytearray("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['date']:
                            fh.write('        _w.write_date("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['datetime']:
                            fh.write('        _w.write_datetime("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['time']:
                            fh.write('        _w.write_time("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        elif a.type in ['uuid']:
                            fh.write('        _w.write_guid("%s", self.%s)\n' % (a.name, self._member(a.name)))
                        else:
                            raise Exception('Unknown type [%s] for field [%s]' % (a.type, self._member(a.name)))

            fh.write('        _w.write_end(_oname)\n\n')

            # Struct.deserialize()
            self._write_py_method(fh,
                                  'int',
                                  '_deserialize',
                                  '_r: mettle.io.IReader, _oname: str = None',
                                  method_descr = 'Deserialize this struct.')
            fh.write('        if _oname == None:\n')
            fh.write('            _oname = self._name()\n\n')
            fh.write('        _r.read_start(_oname)\n')

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        fh.write('        self.%s._deserialize(_r, "%s")\n' % (self._member(a.name), a.name))
                    else:
                        if a.type in ['int32']:
                            fh.write('        self.%s = _r.read_int32("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['int64']:
                            fh.write('        self.%s = _r.read_int64("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['int16']:
                            fh.write('        self.%s = _r.read_int16("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['int8']:
                            fh.write('        self.%s = _r.read_int8("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['uint32']:
                            fh.write('        self.%s = _r.read_uint32("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['uint64']:
                            fh.write('        self.%s = _r.read_uint64("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['uint16']:
                            fh.write('        self.%s = _r.read_uint16("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['uint8']:
                            fh.write('        self.%s = _r.read_uint8("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['string']:
                            fh.write('        self.%s = _r.read_string("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['bool']:
                            fh.write('        self.%s = _r.read_bool("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['char']:
                            fh.write('        self.%s = _r.read_char("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['double']:
                            fh.write('        self.%s = _r.read_double("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['memblock']:
                            fh.write('        self.%s = _r.read_bytearray("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['date']:
                            fh.write('        self.%s = _r.read_date("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['datetime']:
                            fh.write('        self.%s = _r.read_datetime("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['time']:
                            fh.write('        self.%s = _r.read_time("%s")\n' % (self._member(a.name), a.name))
                        elif a.type in ['uuid']:
                            fh.write('        self.%s = _r.read_guid("%s")\n' % (self._member(a.name), a.name))
                        else:
                            raise Exception('Unknown type [%s] for field [%s]' % (a.type, self._member(a.name)))

            fh.write('        _r.read_end(_oname)\n\n')

            self._write_cache_davs(fh, sobj)
            fh.write('\n')

            self._write_py_method(fh, 'str', '__repr__', None)
            self._write_repr_method(fh, sname, sobj.fields)
            fh.write('\n')

            # List class
            fh.write('    # List class\n')
            fh.write('    class List(list, ISerializable):\n\n')

            # List._name()
            self._write_py_method(fh, 'str', '_name', None, extra_spaces = '    ', method_descr = 'Get list name')
            fh.write("            return '%s.List'\n\n" % sname)

            self._write_py_method(fh,
                                  None,
                                  '_serialize',
                                  '_w: mettle.io.IWriter, _oname: str = None',
                                  extra_spaces = '    ',
                                  method_descr = 'Serialize the list')
            fh.write('            if _oname == None:\n')
            fh.write('                _oname = self._name()\n\n')
            fh.write('            _w.write_start_list(_oname, len(self))\n\n')
            fh.write('            for _rec in self:\n')
            fh.write('                _rec._serialize(_w)\n\n')
            fh.write('            _w.write_end(_oname)\n\n')

            self._write_py_method(fh,
                                  'int',
                                  '_deserialize',
                                  '_r: mettle.io.IReader, _oname: str = None',
                                  extra_spaces = '    ',
                                  method_descr = 'Deserialize the list')
            fh.write('            if _oname == None:\n')
            fh.write('                  _oname = self._name()\n\n')
            fh.write('            _cnt = _r.read_start_list(_oname)\n\n')
            fh.write('            while _cnt >= 1:\n')
            fh.write('                _rec  = %s()\n' % (sname))
            fh.write('                _cnt -= 1\n')
            fh.write('                _rec._deserialize(_r)\n')
            fh.write('                self.append(_rec)\n\n')
            fh.write('            _r.read_end(_oname)\n\n')

            self._write_py_method(fh,
                                  'int',
                                  '_get_davs',
                                  'dvc: mettle.lib.DavCache = None',
                                  extra_spaces = '    ',
                                  method_descr = 'Cache the davs')
            fh.write('            return %s._cache_davs(dvc)\n\n' % (sname))

            self._write_py_method(fh, 'str', '__repr__', None, extra_spaces = '    ')
            fh.write("            return '<%s.List[%%d]>' %% (len(self))\n\n" % (sname))

            fh.close()


    def _gen_client_interface(self):
        cls = self._ident('client.interface', self._gen_info['proj'].name)
        fh  = self.gened_file_open(self._gen_info,
                                   self._ident('file.class', cls),
                                   add_namespace_to_path = False,
                                   cls = cls)

        self._add_headers(fh)
        self._gen_imports(fh)
        self._gen_struct_imports(fh)

        self._client_interface = cls

        fh.write('class %s:\n\n' % self._client_interface)

        for call in self._gen_info['proj'].calls:

            self._write_py_method(fh,
                                  call.returns,
                                  self._ident_method(call.name),
                                  self._gen_arg_items(call.fields),
                                  method_descr = call.get_descr() or call.name)

            fh.write('        pass\n\n')

        self.gened_file_close(fh)


    def _gen_server_interface(self):
        cls = self._ident('server.interface', '%s%s' % (self._gen_info['proj'].name, self._async['class']))
        fh  = self.gened_file_open(self._gen_info,
                                   self._ident('file.class', cls),
                                   add_namespace_to_path = False,
                                   cls = cls)

        self._add_headers(fh)
        self._gen_imports(fh)

        fh.write('from mettle.braze.iserver_interface import IServerInterface\n\n')

        self._gen_struct_imports(fh)

        self._server_interface = cls

        fh.write('class %s(IServerInterface):\n\n' % self._server_interface)

        for call in self._gen_info['proj'].calls:

            self._write_py_method(fh,
                                  call.returns,
                                  self._ident_method(call.name),
                                  self._gen_arg_items(call.fields),
                                  method_descr = call.get_descr() or call.name,
                                  can_async = True)

            fh.write('        pass\n\n')

        self.gened_file_close(fh)


    def _gen_client_server_impl(self):
        cls = self._ident('client.serverimpl', self._gen_info['proj'].name)
        si  = self._ident('server.interface',  self._gen_info['proj'].name)
        fh  = self.gened_file_open(self._gen_info,
                                   self._ident('file.class', cls),
                                   add_namespace_to_path = False,
                                   cls = cls)

        self._add_headers(fh)
        self._gen_imports(fh)

        fh.write('from .%s import %s\n'   % (self._ident('file.class', self._client_interface), self._client_interface))
        fh.write('from .%s import %s\n\n' % (self._ident('file.class', si), si))

        self._gen_struct_imports(fh)

        fh.write('class %s(%s):\n' % (cls, self._client_interface))
        fh.write('    """\n')
        fh.write('    A direct client to server client interface implementation (wrapper).\n')
        fh.write('    """\n\n')

        fh.write('    def __init__(self, serverInterface):\n')
        fh.write('        """\n')
        fh.write('        Constructor.\n\n')
        fh.write('        :param serverInterface: %s, the implemented server interface object.\n' % si)
        fh.write('        """\n')
        fh.write('        self._impl = serverInterface\n\n')

        for call in self._gen_info['proj'].calls:

            return_type  = self._gen_return_type_str(call.returns)
            args         = self._gen_arg_items(call.fields)
            comma        = ''

            self._write_py_method(fh,
                                  call.returns,
                                  self._ident_method(call.name),
                                  args,
                                  method_descr = None)

            fh.write('        ')

            if return_type:
                fh.write('return ')

            fh.write('self._impl.%s(' % self._ident_method(call.name))

            for a in args:
                fh.write('%s%s' % (comma, a['name']))
                comma = ', '

            fh.write(')\n\n')

        self.gened_file_close(fh)


    def _gen_client_marshaler(self):
        cls = self._ident('client.marshaler', self._gen_info['proj'].name)
        fh  = self.gened_file_open(self._gen_info,
                                   self._ident('file.class', cls),
                                   add_namespace_to_path = False,
                                   cls = cls)

        self._client_class = cls

        self._add_headers(fh)
        self._gen_imports(fh)

        fh.write('from mettle.braze.iclient_marshaler import IClientMarshaler\n')
        fh.write('from .%s import %s\n\n' % (self._ident('file.class', self._client_interface), self._client_interface))

        self._gen_struct_imports(fh)

        fh.write('class %s(IClientMarshaler, %s):\n\n' % (self._client_class, self._client_interface))

        fh.write('    def __init__(self, client):\n')
        fh.write('        """\n')
        fh.write('        Constructor.\n\n')
        fh.write('        :param client: braze client object.\n')
        fh.write('        """\n')
        fh.write('        self._client = client\n\n')

        fh.write('    def _signature(self) -> str:\n')
        fh.write('        """\n')
        fh.write('        Gets the client signature.\n\n')
        fh.write('        :return: the signature of this client.\n')
        fh.write('        """\n')
        fh.write("        return '%s'\n\n" % self._gen_info['server_sig'])

        for call in self._gen_info['proj'].calls:

            args = self._gen_arg_items(call.fields)

            self._write_py_method(fh,
                                  call.returns,
                                  self._ident_method(call.name),
                                  args,
                                  method_descr = None)

            self._gen_client_declare_varibles(fh, call)
            self._gen_client_assign_input_args(fh, call)
            self._gen_client_server_call(fh, call)
            self._gen_client_assign_output_args(fh, call)

        self.gened_file_close(fh)


    def _gen_server_marshaler(self):
        cls = self._ident('server.marshaler', '%s%s' % (self._gen_info['proj'].name, self._async['class']))
        fh  = self.gened_file_open(self._gen_info,
                                   self._ident('file.class', cls),
                                   add_namespace_to_path = False,
                                   cls = cls)

        self._server_class = cls

        self._add_headers(fh)
        self._gen_imports(fh)

        fh.write('import traceback\n\n')

        fh.write('from mettle.braze.iserver_interface import IServerInterface\n')
        fh.write('from mettle.braze.iserver_marshaler import IServerMarshaler\n')
        fh.write('from mettle.io.istream import IStream\n')
        fh.write('from mettle.braze.server import Server\n')
        fh.write('from mettle.lib.xmettle import xMettle\n')
        fh.write('from .%s import %s\n\n' % (self._ident('file.class', self._server_interface), self._server_interface))

        self._gen_struct_imports(fh)

        fh.write('class %s(IServerMarshaler, %s):\n\n' % (self._server_class, self._server_interface))

        fh.write('    def __init__(self, server_impl: IServerInterface):\n')
        fh.write('        """\n')
        fh.write('        Constructor.\n\n')
        fh.write('        :param server_impl: braze client object.\n')
        fh.write('        """\n')
        fh.write('        self._server   = None\n')
        fh.write('        self._simpl    = server_impl\n\n')

        fh.write('    def _signature(self) -> str:\n')
        fh.write('        """\n')
        fh.write('        Gets the server signature.\n\n')
        fh.write('        :return: the signature of this server.\n')
        fh.write('        """\n')
        fh.write("        return '%s'\n\n" % self._gen_info['server_sig'])

        fh.write('    def _server_impl(self) -> IServerInterface:\n')
        fh.write('        """\n')
        fh.write('        Gets the server implementation.\n\n')
        fh.write('        :return: the overloaded server interface/server implementation object.\n')
        fh.write('        """\n')
        fh.write('        return self._simpl\n\n')

        if self._async['class']:
            fh.write('    async def _serve_async(self, server: Server, remote_sig: "str|int", in_stream: IStream,'
                     ' impl_data: dict = None):\n')
        else:
            fh.write('    def _serve(self, server: Server, remote_sig: "str|int", in_stream: IStream,'
                     ' impl_data: dict = None):\n')

        fh.write('        """\n')
        fh.write('        The main server entry point to the marshaler.\n\n')
        fh.write('        :param server: The server object to use.\n')
        fh.write('        :param remote_sig: The client rpc signature.\n')
        fh.write('        :param in_stream:  The input stream.\n')
        fh.write('        :param impl_data: Any optional impl server data.\n')
        fh.write('        :return: a tuple of (out_stream, err_code, err_msg)\n')
        fh.write('        """\n')
        fh.write('        self._server = server\n')
        fh.write('        out_stream   = None\n\n')
        fh.write('        try:\n')
        fh.write('            self._simpl._set_impl_data(impl_data)\n\n')

        sep = ''

        for call in self._gen_info['proj'].calls:
            fh.write("            %sif remote_sig == '%s':\n" % (sep, call.signature))
            fh.write("                out_stream = %sself.%s(in_stream)\n" % (
                self._async['await'], self._ident_method(call.name)))
            sep = 'el'

        fh.write('            else:\n')
        fh.write('                raise xMettle("Remote signature not known [%s]" % remote_sig)\n')
        fh.write('        except xMettle as x:\n')
        fh.write('            self._server.logger().error("Exception caught [client_address:%s, msg:%s, trace:%s]" % (self'
                 '._server.get_transport().client_address(), str(x), traceback.format_exc()))\n\n')
        fh.write('            if x.get_error_code() == xMettle.eCode.TerminalException:\n')
        fh.write('                raise x\n\n')
        fh.write('            return out_stream, x.get_error_code(), str(x)\n\n')
        fh.write('        except Exception as x:\n')
        fh.write('            self._server.logger().error("Exception caught [client_address:%s, msg:%s, trace:%s]" % (self.'
                 '_server.get_transport().client_address(), str(x), traceback.format_exc()))\n\n')
        fh.write('            return out_stream, xMettle.eCode.UnknownException, str(x)\n\n')
        fh.write('        return out_stream, 0, None\n\n')

        for call in self._gen_info['proj'].calls:
            fh.write('    %sdef %s(self, _i):\n' % (self._async['async'], self._ident_method(call.name)))
            fh.write('        self._server.logger().debug("[%s - Start]")\n\n' % self._ident_method(call.name))
            self._gen_server_declare_varibles(fh, call)
            self._gen_server_assign_input_args(fh, call)
            self._gen_server_auth(fh, call)
            self._gen_server_dav(fh, call)
            self._gen_server_server_call(fh, call)
            self._gen_server_assign_output_args(fh, call)
            fh.write('        self._server.logger().debug("[%s - Done]")\n\n' % self._ident_method(call.name))
            fh.write('        return _o\n\n')

        self.gened_file_close(fh)


    def _gen_struct_imports(self, fh):
        incss = []
        inpss = []

        for dbs in self._gen_info['db_structs']:
            sname = dbs.struct_name()

            if sname not in incss:
                incss.append(sname)
                inpss.append(dbs.struct_path())

        if incss:
            idx = 0

            while idx < len(incss):
                fh.write('from %s import %s\n' % (inpss[idx], incss[idx]))
                idx += 1

            fh.write('\n')

        if len(self._gen_info['proj'].structs) < 1:
            return

        for s in self._gen_info['proj'].struct_order:
            sobj = self._gen_info['proj'].structs[s]
            fh.write('from .%s import %s\n' % (
                self._ident('file.struct', sobj.struct_name()),
                self._ident('braze.struct', sobj.struct_name())))

        fh.write('\n')


    def _gen_return_type_str(self, returns) -> str:
        if not returns:
            return None

        if returns.is_array:

            if returns.type == 'brazerec':
                return '%s.List' % (self._ident('braze.struct', returns.brazestruct.struct_name()))

            if returns.type == 'dbrec':
                return '%s.List' % returns.dbstruct.struct_name()

            if returns.type == 'memblock':
                return 'mettle.braze.MemblockList'

            if returns.type == 'uuid':
                return 'mettle.braze.GuidList'

            return 'mettle.braze.%s%sList' % (returns.type[0].upper(), returns.type[1:])

        if returns.type == 'brazerec':
            return self._ident('braze.struct', returns.brazestruct.struct_name())

        if returns.type == 'dbrec':
            return '%s' % returns.dbstruct.struct_name()

        fmap = self._field_map[returns.type]

        return fmap.name


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

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    param['type'] = '%s.List' % (self._ident('braze.struct', f.brazestruct.struct_name()))
                elif fmap.type_flag == 'dbrec':
                    param['type'] = '%s.List' % (f.dbstruct.struct_name())
                else:
                    if f.type == 'memblock':
                        param['type'] = 'mettle.braze.MemblockList'
                    elif f.type == 'uuid':
                        param['type'] = 'mettle.braze.GuidList'
                    else:
                        param['type'] = 'mettle.braze.%s%sList' % (f.type[0].upper(), f.type[1:])
                continue

            if fmap.type_flag == 'brazerec':
                param['type'] = self._ident('braze.struct', f.brazestruct.struct_name())
            elif fmap.type_flag == 'dbrec':
                param['type'] = f.dbstruct.struct_name()
            else:
                param['type'] = fmap.name

                if is_struct:
                    continue

                if f.io != 'i':
                    param['type']    = 'mettle.lib.Ref'
                    param['io']     += '(%s)' % fmap.name
                    param['default'] = 'None'

        return args


    def _gen_client_declare_varibles(self, fh, call):
        fh.write('        %s = self._client.get_transport().new_stream()\n' % '_i')
        fh.write('        %s = None\n' % '_o')

        call.has_input   = False
        call.has_output  = False

        for f in call.fields:
            if f.io in ['i', 'io']:
                fh.write('        %s = None\n' % '_w')
                call.has_input = True
                break

        for f in call.fields:
            if f.io in ['o', 'io']:
                fh.write('        %s = None\n' % '_r')
                call.has_output = True
                break


        if not call.returns:
            fh.write('\n')
            return

        if not call.has_output:
            fh.write('        %s = None\n' % '_r')
            call.has_output = True

        fh.write('        %s = None\n' % '_x')
        fh.write('\n')


    def _gen_client_assign_input_args(self, fh, call):
        if not call.has_input:
            return

        fh.write('        _w = self._client.get_transport().new_writer(_i)\n')
        fh.write('        _w.write_start("%s_IN")\n' % (call.name))

        for f in call.fields:
            if f.io == 'o':
                continue

            fmap  = self._field_map[f.type]
            fname = self._member(f.name)

            if fmap.type_flag in ['brazerec', 'dbrec'] or f.is_array:
                fh.write('        %s._serialize(_w, "%s")\n' % (fname, f.name))
                continue

            if f.io != 'i' and not f.is_array:
                fname = '%s.get()' % fname

            if f.type in ['int32']:
                fh.write('        _w.write_int32("%s", %s)\n' % (f.name, fname))
            elif f.type in ['int64']:
                fh.write('        _w.write_int64("%s", %s)\n' % (f.name, fname))
            elif f.type in ['int16']:
                fh.write('        _w.write_int16("%s", %s)\n' % (f.name, fname))
            elif f.type in ['int8']:
                fh.write('        _w.write_int8("%s", %s)\n' % (f.name, fname))
            elif f.type in ['uint32']:
                fh.write('        _w.write_uint32("%s", %s)\n' % (f.name, fname))
            elif f.type in ['uint64']:
                fh.write('        _w.write_uint64("%s", %s)\n' % (f.name, fname))
            elif f.type in ['uint16']:
                fh.write('        _w.write_uint16("%s", %s)\n' % (f.name, fname))
            elif f.type in ['uint8']:
                fh.write('        _w.write_uint8("%s", %s)\n' % (f.name, fname))
            elif f.type in ['string']:
                fh.write('        _w.write_string("%s", %s)\n' % (f.name, fname))
            elif f.type in ['char']:
                fh.write('        _w.write_char("%s", %s)\n' % (f.name, fname))
            elif f.type in ['bool']:
                fh.write('        _w.write_bool("%s", %s)\n' % (f.name, fname))
            elif f.type in ['double']:
                fh.write('        _w.write_double("%s", %s)\n' % (f.name, fname))
            elif f.type in ['memblock']:
                fh.write('        _w.write_bytearray("%s", %s)\n' % (f.name, fname))
            elif f.type in ['date']:
                fh.write('        _w.write_date("%s", %s)\n' % (f.name, fname))
            elif f.type in ['datetime']:
                fh.write('        _w.write_datetime("%s", %s)\n' % (f.name, fname))
            elif f.type in ['time']:
                fh.write('        _w.write_time("%s", %s)\n' % (f.name, fname))
            elif f.type in ['uuid']:
                fh.write('        _w.write_guid("%s", %s)\n' % (f.name, fname))
            else:
                fh.write('        _w.write_("%s", %s)\n' % (f.name, fname))

        fh.write('        _w.write_end("%s_IN")\n\n' % (call.name))


    def _gen_client_server_call(self, fh, call):
        sig = call.signature

        fh.write("        self._client.send(self, '%s', _i)\n" % (sig))
        fh.write("        _o = self._client.receive(self, '%s')\n\n" % (sig))


    def _gen_client_assign_output_args(self, fh, call):
        if not call.has_output:
            return

        fh.write('        _r = self._client.get_transport().new_reader(_o)\n')
        fh.write('        _r.read_start("%s_OUT")\n' % (call.name))

        if call.returns:

            fmap  = self._field_map[call.returns.type]

            if call.returns.is_array:
                if call.returns.type == 'brazerec':
                    fh.write('        _x = %s.List()\n' % (
                        self._ident('braze.struct', call.returns.brazestruct.struct_name())))
                    fh.write('        _x._deserialize(_r, None)\n')
                elif call.returns.type == 'dbrec':
                    fh.write('        _x = %s.List()\n' % (call.returns.dbstruct.struct_name()))
                    fh.write('        _x._deserialize(_r, None)\n')
                else:
                    if call.returns.type == 'memblock':
                        fh.write('        _x = mettle.braze.MemblockList()\n')
                    elif call.returns.type == 'uuid':
                        fh.write('        _x = mettle.braze.GuidList()\n')
                    else:
                        fh.write('        _x = mettle.braze.%s%sList()\n' % (
                            call.returns.type[0].upper(), call.returns.type[1:]))

                    fh.write('        _x._deserialize(_r, None)\n')

            else:
                rname = 'return'

                if call.returns.type == 'brazerec':
                    fh.write('        _x = %s()\n' % (
                        self._ident('braze.struct', call.returns.brazestruct.struct_name())))
                    fh.write('        _x._deserialize(_r, "returns")\n')
                elif call.returns.type == 'dbrec':
                    fh.write('        _x = %s()\n' % (call.returns.dbstruct.struct_name()))
                    fh.write('        _x._deserialize(_r, "returns")\n')
                elif call.returns.type in ['int32']:
                    fh.write('        _x = _r.read_int32("%s")\n' % (rname))
                elif call.returns.type in ['int64']:
                    fh.write('        _x = _r.read_int64("%s")\n' % (rname))
                elif call.returns.type in ['int16']:
                    fh.write('        _x = _r.read_int16("%s")\n' % (rname))
                elif call.returns.type in ['int8']:
                    fh.write('        _x = _r.read_int8("%s")\n' % (rname))
                elif call.returns.type in ['uint32']:
                    fh.write('        _x = _r.read_uint32("%s")\n' % (rname))
                elif call.returns.type in ['uint64']:
                    fh.write('        _x = _r.read_uint64("%s")\n' % (rname))
                elif call.returns.type in ['uint16']:
                    fh.write('        _x = _r.read_uint16("%s")\n' % (rname))
                elif call.returns.type in ['uint8']:
                    fh.write('        _x = _r.read_uint8("%s")\n' % (rname))
                elif call.returns.type in ['string']:
                    fh.write('        _x = _r.read_string("%s")\n' % (rname))
                elif call.returns.type in ['char']:
                    fh.write('        _x = _r.read_char("%s")\n' % (rname))
                elif call.returns.type in ['bool']:
                    fh.write('        _x = _r.read_bool("%s")\n' % (rname))
                elif call.returns.type in ['double']:
                    fh.write('        _x = _r.read_double("%s")\n' % (rname))
                elif call.returns.type in ['memblock']:
                    fh.write('        _x = _r.read_bytearray("%s")\n' % (rname))
                elif call.returns.type in ['date']:
                    fh.write('        _x = _r.read_date("%s")\n' % (rname))
                elif call.returns.type in ['datetime']:
                    fh.write('        _x = _r.read_datetime("%s")\n' % (rname))
                elif call.returns.type in ['time']:
                    fh.write('        _x = _r.read_time("%s")\n' % (rname))
                elif call.returns.type in ['uuid']:
                    fh.write('        _x = _r.read_guid("%s")\n' % (rname))
                else:
                    fh.write('        _x = _r.read_("%s")\n' % (rname))


        for f in call.fields:
            if f.io == 'i':
                continue

            fmap  = self._field_map[f.type]
            fname = self._member(f.name)

            if fmap.type_flag in ['brazerec', 'dbrec'] or f.is_array:
                fh.write('        %s.%s()\n' % (fname, self._ident_method('Clear')))
                fh.write('        %s._deserialize(_r, "%s")\n' % (fname, f.name))
            elif f.type in ['int32']:
                fh.write('        %s.set(_r.read_int32("%s"))\n' % (fname, f.name))
            elif f.type in ['int64']:
                fh.write('        %s.set(_r.read_int64("%s"))\n' % (fname, f.name))
            elif f.type in ['int16']:
                fh.write('        %s.set(_r.read_int16("%s"))\n' % (fname, f.name))
            elif f.type in ['int8']:
                fh.write('        %s.set(_r.read_int8("%s"))\n' % (fname, f.name))
            elif f.type in ['uint32']:
                fh.write('        %s.set(_r.read_uint32("%s"))\n' % (fname, f.name))
            elif f.type in ['uint64']:
                fh.write('        %s.set(_r.read_uint64("%s"))\n' % (fname, f.name))
            elif f.type in ['uint16']:
                fh.write('        %s.set(_r.read_uint16("%s"))\n' % (fname, f.name))
            elif f.type in ['uint8']:
                fh.write('        %s.set(_r.read_uint8("%s"))\n' % (fname, f.name))
            elif f.type in ['string']:
                fh.write('        %s.set(_r.read_string("%s"))\n' % (fname, f.name))
            elif f.type in ['char']:
                fh.write('        %s.set(_r.read_char("%s"))\n' % (fname, f.name))
            elif f.type in ['bool']:
                fh.write('        %s.set(_r.read_bool("%s"))\n' % (fname, f.name))
            elif f.type in ['double']:
                fh.write('        %s.set(_r.read_double("%s"))\n' % (fname, f.name))
            elif f.type in ['memblock']:
                fh.write('        %s.set(_r.read_bytearray("%s"))\n' % (fname, f.name))
            elif f.type in ['date']:
                fh.write('        %s.set(_r.read_date("%s"))\n' % (fname, f.name))
            elif f.type in ['datetime']:
                fh.write('        %s.set(_r.read_datetime("%s"))\n' % (fname, f.name))
            elif f.type in ['time']:
                fh.write('        %s.set(_r.read_time("%s"))\n' % (fname, f.name))
            elif f.type in ['uuid']:
                fh.write('        %s.set(_r.read_guid("%s"))\n' % (fname, f.name))
            else:
                fh.write('        %s.set(_r.read_("%s"))\n' % (fname, f.name))


        fh.write('        _r.read_end("%s_OUT")\n' % (call.name))

        if call.returns:
            fh.write('\n        return _x\n')

        fh.write('\n')


    def _gen_server_declare_varibles(self, fh, call):
        fh.write('        %s = self._server.get_transport().new_stream()\n' % '_o')

        call.has_input   = False
        call.has_output  = False

        for f in call.fields:
            if f.io in ['i', 'io']:
                fh.write('        %s = None\n' % '_r')
                call.has_input = True
                break

        for f in call.fields:
            if f.io in ['o', 'io']:
                fh.write('        %s = None\n' % '_w')
                call.has_output = True
                break

        if call.returns and not call.has_output:
            fh.write('        %s = None\n' % '_w')
            call.has_output = True

        if call.returns:
            fh.write('        %s = None\n' % '_x')

        fh.write('\n')

        if not call.has_input and not call.has_output:
            return

        writ = False

        for f in call.fields:
            fmap = self._field_map[f.type]

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    fh.write('        %s = %s.List()\n' % (
                        self._member(f.name), self._ident('braze.struct', f.brazestruct.struct_name())))
                    writ = True
                elif fmap.type_flag == 'dbrec':
                    fh.write('        %s = %s.List()\n' % (
                        self._member(f.name), f.dbstruct.struct_name()))
                    writ = True
                elif fmap.type_flag == 'uuid':
                    fh.write('        %s = mettle.braze.GuidList()\n' % (self._member(f.name)))
                    writ = True
                else:
                    fh.write('        %s = mettle.braze.%sList()\n' % (
                        self._member(f.name), self._member(f.type).capitalize()))
                    writ = True

            else:
                if fmap.type_flag == 'brazerec':
                    fh.write('        %s = %s()\n' % (
                        self._member(f.name), self._ident('braze.struct', f.brazestruct.struct_name())))
                    writ = True
                elif fmap.type_flag == 'dbrec':
                    fh.write('        %s = %s()\n' % (
                        self._member(f.name), f.dbstruct.struct_name()))
                    writ = True
                else:
                    if f.io in ['o', 'io']:
                        fh.write('        %s = mettle.lib.Ref(%s)\n' % (self._member(f.name), fmap.def_val))
                        writ = True

        if writ:
            fh.write('\n')


    def _gen_server_assign_input_args(self, fh, call):
        if not call.has_input:
            return

        fh.write('        _r = self._server.get_transport().new_reader(_i)\n')
        fh.write('        _r.read_start("%s_IN")\n' % (call.name))

        for f in call.fields:
            if f.io == 'o':
                continue

            fmap = self._field_map[f.type]

            if f.io == 'i':
                mask = '        %s = _r.%s("%s")\n'
            elif f.io == 'io':
                mask = '        %s.set(_r.%s("%s"))\n'

            if fmap.type_flag in ['brazerec', 'dbrec'] or f.is_array:
                fh.write('        %s._deserialize(_r, "%s")\n' % (self._member(f.name), f.name))
            elif f.type in ['int32']:
                fh.write(mask % (self._member(f.name), 'read_int32', f.name))
            elif f.type in ['int64']:
                fh.write(mask % (self._member(f.name), 'read_int64', f.name))
            elif f.type in ['int16']:
                fh.write(mask % (self._member(f.name), 'read_int16', f.name))
            elif f.type in ['int8']:
                fh.write(mask % (self._member(f.name), 'read_int8', f.name))
            elif f.type in ['uint32']:
                fh.write(mask % (self._member(f.name), 'read_uint32', f.name))
            elif f.type in ['uint64']:
                fh.write(mask % (self._member(f.name), 'read_uint64', f.name))
            elif f.type in ['uint16']:
                fh.write(mask % (self._member(f.name), 'read_uint16', f.name))
            elif f.type in ['uint8']:
                fh.write(mask % (self._member(f.name), 'read_uint8', f.name))
            elif f.type in ['string']:
                fh.write(mask % (self._member(f.name), 'read_string', f.name))
            elif f.type in ['char']:
                fh.write(mask % (self._member(f.name), 'read_char', f.name))
            elif f.type in ['bool']:
                fh.write(mask % (self._member(f.name), 'read_bool', f.name))
            elif f.type in ['double']:
                fh.write(mask % (self._member(f.name), 'read_double', f.name))
            elif f.type in ['memblock']:
                fh.write(mask % (self._member(f.name), 'read_bytearray', f.name))
            elif f.type in ['date']:
                fh.write(mask % (self._member(f.name), 'read_date', f.name))
            elif f.type in ['datetime']:
                fh.write(mask % (self._member(f.name), 'read_datetime', f.name))
            elif f.type in ['time']:
                fh.write(mask % (self._member(f.name), 'read_time', f.name))
            elif f.type in ['uuid']:
                fh.write(mask % (self._member(f.name), 'read_guid', f.name))
            else:
                raise Exception('Unknown type - (field:%s, type:%s)' % (f.name, f.type))

        fh.write('        _r.read_end("%s_IN")\n\n' % (call.name))


    def _gen_server_auth(self, fh, call):
        if not call.auth:
            fh.write('        self._simpl._set_rpc_token_data(None)\n\n')
            return

        if self._async['class']:
            fh.write('        tok = await self._server.auth_async("%s", "%s", {' % (call.name, call.auth))
        else:
            fh.write('        tok = self._server.auth("%s", "%s", {' % (call.name, call.auth))

        join = ''

        for f in call.fields:
            if f.io == 'o':
                continue

            fh.write('%s"%s":%s' % (join, f.name, self._member(f.name)))
            join = ', '

        fh.write('})\n')
        fh.write('        self._simpl._set_rpc_token_data(tok)\n\n')


    def _gen_server_dav(self, fh, call):
        if not call.has_input:
            return

        decl = False

        for f in call.fields:
            if f.io == 'o' or not f.dav:
                continue

            cmds = f.dav.get('cmds')

            if cmds == 'clear' and len(f.dav) == 1:
                continue

            if not decl:
                fh.write('        _dvc = mettle.lib.DavCache()\n')
                fh.write('        self._server_impl()._init_dav_cache("%s", _dvc)\n\n' % call.name)
                decl = True

            fh.write('        _dvc.clear()\n')

            cmds = f.dav.get('cmds')

            if f.type == 'brazerec':
                if cmds != 'clear':
                    fh.write('        %s._get_davs(_dvc)\n' % self._member(f.name))
            elif f.type == 'dbrec':
                if cmds != 'clear':
                    ins = '' if cmds != 'insert' else ', forIns=True'
                    key = '' if cmds != 'key' else ', keyOnly=True'
                    fh.write('        %s._get_davs(_dvc%s%s)\n'  % (self._member(f.name), ins, key))

            self._write_dav(fh, call, f)
            fh.write('\n')


    def _gen_server_server_call(self, fh, call):
        if call.returns:
            meth = '        _x = %sself._simpl.%s(' % (self._async['await'], self._ident_method(call.name))
        else:
            meth = '        %sself._simpl.%s(' % (self._async['await'], self._ident_method(call.name))

        methLen = len(meth)
        space   = ''

        fh.write(meth)

        for f in call.fields:
            fh.write('%s%s' % (space, self._member(f.name)))
            if space == '':
                space = ',\n%*s' % (methLen, '')

        fh.write(')\n\n')


    def _gen_server_assign_output_args(self, fh, call):
        if not call.has_output:
            return

        fh.write('        _w = self._server.get_transport().new_writer(_o)\n')
        fh.write('        _w.write_start("%s_OUT")\n' % (call.name))

        if call.returns:
            fmap = self._field_map[call.returns.type]
            mask = '        _w.%s("%s", _x)\n'

            if call.returns.is_array or fmap.type_flag in ['brazerec', 'dbrec']:
                fh.write('        _x._serialize(_w)\n')
            else:
                if call.returns.type in ['int32']:
                    fh.write(mask % ('write_int32', 'return'))
                elif call.returns.type in ['int64']:
                    fh.write(mask % ('write_int64', 'return'))
                elif call.returns.type in ['int16']:
                    fh.write(mask % ('write_int16', 'return'))
                elif call.returns.type in ['int8']:
                    fh.write(mask % ('write_int8', 'return'))
                elif call.returns.type in ['uint32']:
                    fh.write(mask % ('write_uint32', 'return'))
                elif call.returns.type in ['uint64']:
                    fh.write(mask % ('write_uint64', 'return'))
                elif call.returns.type in ['uint16']:
                    fh.write(mask % ('write_uint16', 'return'))
                elif call.returns.type in ['uint8']:
                    fh.write(mask % ('write_uint8', 'return'))
                elif call.returns.type in ['string']:
                    fh.write(mask % ('write_string', 'return'))
                elif call.returns.type in ['char']:
                    fh.write(mask % ('write_char', 'return'))
                elif call.returns.type in ['bool']:
                    fh.write(mask % ('write_bool', 'return'))
                elif call.returns.type in ['double']:
                    fh.write(mask % ('write_double', 'return'))
                elif call.returns.type in ['memblock']:
                    fh.write(mask % ('write_bytearray', 'return'))
                elif call.returns.type in ['date']:
                    fh.write(mask % ('write_date', 'return'))
                elif call.returns.type in ['datetime']:
                    fh.write(mask % ('write_datetime', 'return'))
                elif call.returns.type in ['time']:
                    fh.write(mask % ('write_time', 'return'))
                elif call.returns.type in ['uuid']:
                    fh.write(mask % ('write_guid', 'return'))

        mask = '        _w.%s("%s", %s.get())\n'

        for f in call.fields:
            if f.io == 'i':
                continue

            fmap  = self._field_map[f.type]
            fname = self._member(f.name)

            if fmap.type_flag in ['brazerec', 'dbrec'] or f.is_array:
                fh.write('        %s._serialize(_w)\n' % fname)
            else:
                if f.type in ['int32']:
                    fh.write(mask % ('write_int32', f.name, fname))
                elif f.type in ['int64']:
                    fh.write(mask % ('write_int64', f.name, fname))
                elif f.type in ['int16']:
                    fh.write(mask % ('write_int16', f.name, fname))
                elif f.type in ['int8']:
                    fh.write(mask % ('write_int8', f.name, fname))
                elif f.type in ['uint32']:
                    fh.write(mask % ('write_uint32', f.name, fname))
                elif f.type in ['uint64']:
                    fh.write(mask % ('write_uint64', f.name, fname))
                elif f.type in ['uint16']:
                    fh.write(mask % ('write_uint16', f.name, fname))
                elif f.type in ['uint8']:
                    fh.write(mask % ('write_uint8', f.name, fname))
                elif f.type in ['string']:
                    fh.write(mask % ('write_string', f.name, fname))
                elif f.type in ['char']:
                    fh.write(mask % ('write_char', f.name, fname))
                elif f.type in ['bool']:
                    fh.write(mask % ('write_bool', f.name, fname))
                elif f.type in ['double']:
                    fh.write(mask % ('write_double', f.name, fname))
                elif f.type in ['memblock']:
                    fh.write(mask % ('write_bytearray', f.name, fname))
                elif f.type in ['date']:
                    fh.write(mask % ('write_date', f.name, fname))
                elif f.type in ['datetime']:
                    fh.write(mask % ('write_datetime', f.name, fname))
                elif f.type in ['time']:
                    fh.write(mask % ('write_time', f.name, fname))
                elif f.type in ['uuid']:
                    fh.write(mask % ('write_guid', f.name, fname))

        fh.write('        _w.write_end("%s_OUT")\n\n' % (call.name))


    def _write_dav(self, fh, call, field):

        isobj = field.type in ['dbrec', 'brazerec']
        fname = self._member(field.name)

        self._resolve_field_dav(call, field, self._gen_info)

        for david, daval in sorted(field.dav.items(), reverse=True):

            if david == 'cmds':
                continue

            dot  = david.find(':')
            plus = david.find('+')

            if not isobj and (dot != -1 or plus != -1):
                raise Exception('No object type [%s] cannot have . or  + sub qualifier [call:%s, field:%s]' % (
                    field.type, call.name, field.name))

            if dot != -1:
                qual  = david[:dot]
                david = david[dot + 1:]
            elif plus != -1:
                qual  = david[:plus]
                david = david[plus + 1:]
            else:
                qual = fname

            if daval is None or dot != -1:
                if not isobj:
                    raise Exception('Cannot clear/None non object types. [call:%s, field:%s, dav:%s]' % (
                        call.name, field.name, str(david)))

                fh.write('        _dvc.rem_targ("%s", mettle.lib.Dav.eDavType.%s)\n' % (fname, self._dav_map[david]))

                if dot == -1:
                    continue

            if david == 'null':
                if daval is False:
                    fh.write('        _dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.NotNull))\n' % (qual))
            elif david in ['min', 'max']:
                if field.type in ['date', 'datetime', 'time']:
                    if field.type == 'date':
                        mask = 'datetime.date(%-Y, %-m, %-d)'
                    elif field.type == 'datetime':
                        mask = 'datetime.datetime(%-Y, %-m, %-d, %-H, %-M, %-S)'
                    else:
                        mask = 'datetime.time(%-H, %-M, %-S)'

                    fh.write('        _dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %s))\n' % (
                        fname, self._dav_map[david], daval.strftime(mask)))
                elif field.type in ['double', 'float']:
                    fh.write('        _dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %lf))\n' % (
                        fname, self._dav_map[david], daval))
                else:
                    fh.write('        _dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %d))\n' % (
                        qual, self._dav_map[david], daval))
            elif david in ['regex', 'func']:
                fh.write('        _dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, "%s"))\n' % (
                    qual, self._dav_map[david], daval))
            elif david in ['in', 'notin']:
                if type(daval) == dict:
                    dlist = list(daval.keys())
                elif type(daval) == list:
                    dlist = daval
                else:
                    raise Exception('Type [%s] not expected [davtype:%s, call:%s, field:%s]!' % (
                        str(type(daval)), david, call.name, fname))

                if len(dlist) == 0:
                    raise Exception('Type [%s] has no length [davtype:%s, call:%s, field:%s]!' % (
                        str(type(daval)), david, call.name, fname))

                if type(dlist[0]) == str:
                    opcloser = "'"
                    joiner   = "','"
                else:
                    opcloser = ""
                    joiner   = ","

                fh.write('        _dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, [%s%s%s]))\n' % (
                    qual, self._dav_map[david], opcloser, joiner.join(dlist), opcloser))
            else:
                raise Exception('Dav [%s] not expected [call:%s, field:%s]!' % (david, call.name, fname))

        if isobj:
            fh.write('        _dvc.validate_object("%s", %s)\n' % (fname, fname))
        else:
            fh.write('        _dvc.validate("%s", %s)\n' % (fname, fname))


    def _write_cache_field_davs(self, fh, sobj, field):
        """
        Write the column davs.

        :param fh: File handle.
        :param sobj: The struct.
        :param field: The field.
        """
        if not field.dav:
            return

        for david, daval in field.dav.items():
            if david == 'cmds' or daval is None:
                continue

            fname = self._member(field.name)

            if david == 'null':
                if daval is False:
                    fh.write('        dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.NotNull))\n' % (fname))
            elif david in ['min', 'max']:
                if field.type in ['date', 'datetime', 'time']:
                    if field.type == 'date':
                        mask = 'datetime.date(%Y, %m, %d)'
                    elif field.type == 'datetime':
                        mask = 'datetime.datetime(%Y, %m, %d, %H, %M, %S)'
                    else:
                        mask = 'datetime.time(%H, %M, %S)'

                    fh.write('        dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %s))\n' % (
                        fname, self._dav_map[david], daval.strftime(mask).replace(' 0', ' ')))
                elif field.type in ['double', 'float']:
                    fh.write('        dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %lf))\n' % (
                        fname, self._dav_map[david], daval))
                else:
                    fh.write('        dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, %d))\n' % (
                        fname, self._dav_map[david], daval))
            elif david in ['regex', 'func']:
                fh.write('        dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, "%s"))\n' % (
                    fname, self._dav_map[david], daval))
            elif david in ['in', 'notin']:
                if field.type in ['char', 'string']:
                    opcloser = "'"
                    joiner   = "','"
                else:
                    opcloser = ""
                    joiner   = ","

                if type(daval) == dict:
                    dlist = daval.keys()
                elif type(daval) == list:
                    dlist = daval
                else:
                    raise Exception('Type [%s] not expected [davtype:%s, struct:%s, field:%s]!' % (
                        str(type(daval)), david, sobj.name, field.name))

                fh.write('        dvc.add_targ("%s", mettle.lib.Dav(mettle.lib.Dav.eDavType.%s, [%s%s%s]))\n' % (
                    fname, self._dav_map[david], opcloser, joiner.join(dlist), opcloser))


    def _write_cache_davs(self, fh, sobj):
        fh.write('    @staticmethod\n')
        fh.write('    def _cache_davs(dvc: mettle.lib.DavCache = None):\n')
        fh.write('        """\n')
        fh.write('        Cache the DAV into the dav cache (or create one) and return it.\n\n')
        fh.write('        :param dvc: Target cache, if None a new one is created and returned.\n')
        fh.write('        """\n')
        fh.write('        if not dvc:\n')
        fh.write('            dvc = mettle.lib.DavCache()\n')

        added = False

        for field in sobj.fields:
            if not field.dav:
                continue

            if not added:
                fh.write('\n')
                added = True

            self._resolve_field_dav(sobj, field, self._gen_info)
            self._write_cache_field_davs(fh, sobj, field)

        fh.write('\n        return dvc\n\n')

        fh.write('    def _get_davs(self, dvc=None):\n')
        fh.write('        return self._cache_davs(dvc)\n')


    def _write_py_method(self,
                         fh,
                         returns          : "str|object",
                         method           : str,
                         args             : "list|str" = None,
                         extra_spaces     : str = '',
                         use_default_vals : bool = False,
                         method_descr     : str = None,
                         can_async        : bool = False):
        cstr  = '    %s%sdef %s(self' % (extra_spaces, self._async['async'] if can_async else '', method)
        comma = ', '

        fh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguements(fh, args, len(cstr) - 4, use_default_vals = use_default_vals)
            elif type(args) == str:
                fh.write('%s%s' % (comma, args))

        fh.write(')')

        if returns:
            if type(returns) == str:
                fh.write(' -> %s' % returns.split(':')[0].strip())
            else:
                fh.write(' -> %s' % self._gen_return_type_str(returns))

        fh.write(':\n')

        if not method_descr:
            return

        fh.write('        %s"""\n' % extra_spaces)

        fh.write('        %s%s\n' % (extra_spaces, method_descr))

        if args:
            fh.write('\n')
            self._write_arguements(fh, args, len(cstr) - 4, comments = True, extra_spaces = extra_spaces)

        if returns:
            if type(returns) == str:
                if returns.find(':') != -1:
                    if not args:
                        fh.write('\n')

                    fh.write('        %s:return: %s\n' % (extra_spaces, returns.split(':')[1].strip()))
            else:
                if not args:
                    fh.write('\n')

                fh.write('        %s:return: %s\n' % (
                    extra_spaces, returns.descr or self._gen_return_type_str(returns)))

        fh.write('        %s"""\n'  % extra_spaces)


    def _write_arguements(self,
                          fh,
                          args             : 'list|str',
                          spacing          : int,
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
            if comments:
                fh.write("        %s:param %s:" % (extra_spaces, a['name']))

                if a['io']:
                    fh.write(' %s' % a['io'])

                    if a.get('descr'):
                        fh.write(' - %s' % a.get('descr'))

                elif a.get('descr'):
                    fh.write(' %s' % a.get('descr'))

                fh.write('\n')

            else:
                fh.write('%s%s: %s' % (sep, a['name'], a['type']))

                if use_default_vals:
                    fh.write(' = %s' % a['default'])
