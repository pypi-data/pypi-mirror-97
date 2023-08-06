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

import logging
import os.path

from .generator import Generator


class GenCpp(Generator):

    def __init__(self):
        Generator.__init__(self, ['h', 'cpp'])

        self._field_map['bool']        = Generator.FieldMap('bool')
        self._field_map['int8']        = Generator.FieldMap('int8_t')
        self._field_map['int16']       = Generator.FieldMap('int16_t')
        self._field_map['int32']       = Generator.FieldMap('int32_t')
        self._field_map['int64']       = Generator.FieldMap('int64_t')
        self._field_map['uint8']       = Generator.FieldMap('uint8_t')
        self._field_map['uint16']      = Generator.FieldMap('uint16_t')
        self._field_map['uint32']      = Generator.FieldMap('uint32_t')
        self._field_map['uint64']      = Generator.FieldMap('uint64_t')
        self._field_map['double']      = Generator.FieldMap('double')
        self._field_map['char']        = Generator.FieldMap('char',                     type_flag = 'char')
        self._field_map['string']      = Generator.FieldMap('Mettle::Lib::String',      type_flag = 'string',   methodpre = '&')
        self._field_map['date']        = Generator.FieldMap('Mettle::Lib::Date',        type_flag = 'date',     methodpre = '&')
        self._field_map['time']        = Generator.FieldMap('Mettle::Lib::Time',        type_flag = 'date',     methodpre = '&')
        self._field_map['datetime']    = Generator.FieldMap('Mettle::Lib::DateTime',    type_flag = 'date',     methodpre = '&')
        self._field_map['memblock']    = Generator.FieldMap('Mettle::Lib::MemoryBlock', type_flag = 'memblock', methodpre = '&')
        self._field_map['uuid']        = Generator.FieldMap('Mettle::Lib::String',      type_flag = 'string',   methodpre = '&')
        self._field_map['json']        = Generator.FieldMap('Mettle::Lib::String',      type_flag = 'string',   methodpre = '&')
        self._field_map['dbrec']       = Generator.FieldMap('struct',                   type_flag = 'dbrec',    methodpre = '*')
        self._field_map['brazerec']    = Generator.FieldMap('struct',                   type_flag = 'brazerec', methodpre = '*')

        self._init_code_options({
            'includepath.braze'  : None,
            'includepath.tables' : None,
        })

        self._init_casing({
            'class'  : 'pascal',
            'method' : 'pascal',
            'member' : 'pascal',
            'file'   : 'lower'
        })


    def name(self) -> str:
        return 'C++'


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

        self._initialize()

        self._add_headers()

        self._gen_headers()
        self._gen_db_struct_headers()
        self._gen_begin_namespaces()

        self._gen_braze_couplets()
        self._gen_braze_structs()

        self._gen_server_interface()
        self._gen_server_header()
        self._gen_server_code()

        self._gen_client_interface()
        self._gen_client_header()
        self._gen_client_code()

        self._gen_end_namespaces()
        self._gen_trailers()

        self._destroy()


    def _modeFileName(self, mode, interface, ext):
        return '%s%s%s.%s' % (self._gen_info['proj'].name.lower(), mode.lower(), 'interface' if interface else '',  'h')


    def _initialize(self):
        name = self._gen_info['proj'].name

        if self._mode == self.CLIENT:
            hFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident('client.marshaler', name)), 'h')
            cFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident('client.marshaler', name)), 'cpp')
            iFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident('client.interface', name)), 'h')
        elif self._mode == self.SERVER:
            hFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident('server.marshaler', name)), 'h')
            cFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident('server.marshaler', name)), 'cpp')
            iFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident('server.interface', name)), 'h')
        else:
            hFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident_class('%sStruct' % name)),  'h')
            cFile  = self.filename_and_path(self._gen_info, self._ident_file(self._ident_class('%sStruct' % name)),  'cpp')
            iFile  = None

        logging.info('Gen: %s' % hFile)
        logging.info('Gen: %s' % cFile)

        if iFile is not None:
            logging.info('Gen: %s' % iFile)

        self._hFile = os.path.split(hFile)[1]
        self._cFile = os.path.split(cFile)[1]
        self._iFile = None

        if iFile is not None:
            self._iFile = os.path.split(iFile)[1]

        self._hfh   = open(hFile, 'wt')
        self._cfh   = open(cFile, 'wt')
        self._ifh   = None

        if iFile:
            self._ifh = open(iFile, 'wt')


    def _destroy(self):
        self._hfh.close()
        self._cfh.close()

        if self._ifh:
            self._ifh.close()

        del self._hFile
        del self._cFile
        del self._iFile

        del self._hfh
        del self._cfh
        del self._ifh


    def _add_headers(self):
        import time

        message = '/* This file was generated by mettle.genes.braze.GenCpp [ver %s] on %s */\n\n' % (
            self._gen_info['version'], time.asctime())

        self._hfh.write(message)
        self._cfh.write(message)

        if self._ifh:
            self._ifh.write(message)


    def _write_cpp_method(
            self,
            returns      : str,
            cls          : str,
            method       : str,
            args         : 'str|list' = None,
            inherits     : str        = None,
            virtual      : bool       = False,
            const        : bool       = False,
            ignore_types : list       = [],
            extra_spaces : str        = ''):
        if virtual:
            if len(returns):
                hstr = '   %svirtual %s %s(' % (extra_spaces, returns, method)
            else:
                hstr = '   %s%s %s(' % (extra_spaces, 'virtual', method)
        else:
            if len(returns):
                hstr = '   %s%s %s(' % (extra_spaces, returns, method)
            else:
                hstr = '   %s%s(' % (extra_spaces, method)

        cstr = '%s%s::%s(' % ('' if len(returns) == 0 else '%s ' % returns, cls, method)

        self._hfh.write(hstr)
        self._cfh.write(cstr)

        if args:
            if type(args) == list:
                self._write_arguements(args, len(extra_spaces) + 6, self._hfh, ignore_types, True)
                self._write_arguements(args, len(extra_spaces) + 3, self._cfh, ignore_types, False)
            elif type(args) == str:
                arr   = args.split(',')
                comma = ''

                for a in arr:
                    if len(comma):
                        self._hfh.write(comma)
                        self._cfh.write(comma)

                    self._hfh.write(a.strip())
                    self._cfh.write(a.split('=')[0].strip())
                    comma = ', '

        end = ')%s' % (' const' if const else '')

        self._hfh.write('%s;\n\n' % end)
        self._cfh.write('%s\n' % end)

        if inherits:
            for h in inherits:
                self._cfh.write('   :%s\n' % h)


    def _write_arguements(self, args, spacing, fh, filter_out, allow_defaults):
        if not args:
            return

        nl    = '\n'
        spc   = spacing

        for m in args:
            if filter_out:
                if m.type in filter_out:
                    continue

            fh.write('%s%*s' % (nl, spc, ''))
            spc = spacing
            nl  = ',\n'

            fmap = self._field_map[m.type]

            if m.is_array:
                if fmap.type_flag == 'brazerec':
                    fh.write('const %s%s %s' % (
                        '%s::List' % self._ident('braze.struct', m.brazestruct.struct_name()),
                        '&',
                        self._ident_member(m.name)))

                elif fmap.type_flag == 'dbrec':
                    fh.write('const %s%s %s' % ('%s::List' % m.dbstruct.struct_name(), '&', m.name))
                else:
                    if m.type == 'memblock':
                        fh.write('const %s%s %s' % ('Mettle::Braze::MemoryBlockList', '&', m.name))
                    else:
                        fh.write('const %s%s %s' % (
                            'Mettle::Braze::%s%sList' % (m.type[0].upper(), m.type[1:]),
                            '&',
                            self._ident_member(m.name)))
                continue


            if fmap.type_flag == 'brazerec':
                fh.write('const %s%s %s' % (
                    self._ident('braze.struct', m.brazestruct.struct_name()),
                    '&',
                    self._ident_member(m.name)))
            elif fmap.type_flag == 'dbrec':
                fh.write('const %s%s %s' % (m.dbstruct.struct_name(), '&', self._ident_member(m.name)))
            else:
                fh.write('const %s%s %s' % (fmap.name, fmap.methodpre, self._ident_member(m.name)))



    def _write_copy_args(self, fromObj: str, args: list , toObj: str, fil: list = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            self._cfh.write('   %s%s = %s%s;\n' % (fromObj, self._ident_member(a.name), toObj, self._ident_member(a.name)))


    def _write_member_decleration(self, members):
        for m in members:
            fmap = self._field_map[m.type]

            if m.is_array:
                if fmap.type_flag == 'brazerec':
                    self._hfh.write('   %s %s;\n' % (
                        '%s::List' % self._ident('braze.struct', m.brazestruct.struct_name()),
                        self._ident_member(m.name)))
                elif fmap.type_flag == 'dbrec':
                    self._hfh.write('   %s %s;\n' % ('%s::List' % m.dbstruct.struct_name(), self._ident_member(m.name)))
                else:
                    if m.type == 'memblock':
                        self._hfh.write('   %s %s;\n' % ('Mettle::Braze::MemoryBlockList', self._ident_member(m.name)))
                    else:
                        self._hfh.write('   %s %s;\n' % (
                            'Mettle::Braze::%s%sList' % (m.type[0].upper(), m.type[1:]),
                            self._ident_member(m.name)))
                continue


            if fmap.type_flag == 'brazerec':
                self._hfh.write('   %s %s;\n' % (
                    self._ident('braze.struct', m.brazestruct.struct_name()),
                    self._ident_member(m.name)))
            elif fmap.type_flag == 'dbrec':
                self._hfh.write('   %s %s;\n' % (m.dbstruct.struct_name(), self._ident_member(m.name)))
            else:
                self._hfh.write('   %s %s;\n' % (fmap.name, self._ident_member(m.name)))



    def _write_clear_fields(self, args, fil = None):
        if not args:
            return

        for a in args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            if a.is_array:
                self._cfh.write('   %s.purge();\n' % (self._ident_member(a.name)))
            elif fmap.type_flag in ('dbrec', 'brazerec'):
                self._cfh.write('   %s.%s();\n' % (self._ident_member(a.name), self._ident_method('Clear')))
            elif fmap.type_flag in ('string', 'memblock', 'date'):
                self._cfh.write('   %s.clear();\n' % (self._ident_member(a.name)))
            else:
                self._cfh.write('   %s = 0;\n' % (self._ident_member(a.name)))


    def _gen_headers(self):
        self._hfh.write('#ifndef __GEN_METTLE_BRAZE_%s_%s_MARSHALER_H_\n'   % (
            self._gen_info['proj'].name.upper(), self._mode))
        self._hfh.write('#define __GEN_METTLE_BRAZE_%s_%s_MARSHALER_H_\n\n' % (
            self._gen_info['proj'].name.upper(), self._mode))

        brazePath = self.get_option('includepath.braze').replace('|', '/').replace('\\', '/')

        if len(brazePath) and not brazePath.endswith('/'):
            brazePath += '/'

        if self._ifh:
            self._ifh.write('#ifndef __GEN_METTLE_BRAZE_%s_%s_INTERFACE_H_\n'   % (
                self._gen_info['proj'].name.upper(), self._mode))
            self._ifh.write('#define __GEN_METTLE_BRAZE_%s_%s_INTERFACE_H_\n\n' % (
                self._gen_info['proj'].name.upper(), self._mode))

        self._cfh.write('#include "%s%s"\n\n' % (brazePath, self._hFile))

        if self._ifh:
            self._ifh.write('#include "%s%s"\n\n' % (brazePath, self._modeFileName(self.STRUCT, False, 'h')))
            self._ifh.write('#include "mettle/lib/c99standard.h"\n')

            if self._mode == self.STRUCT:
                self._ifh.write('#include "mettle/braze/serverinterface.h"\n')

            self._ifh.write('#include "mettle/lib/xmettle.h"\n\n')

            self._hfh.write('#include "%s%s"\n\n' % (brazePath, self._iFile))

        if self._mode == self.STRUCT:
            self._hfh.write('#include "mettle/lib/c99standard.h"\n')
            self._hfh.write('#include "mettle/lib/collection.h"\n')
            self._hfh.write('#include "mettle/lib/datetime.h"\n')
            self._hfh.write('#include "mettle/lib/memoryblock.h"\n')
            self._hfh.write('#include "mettle/lib/safe.h"\n')
            self._hfh.write('#include "mettle/lib/string.h"\n')
            self._hfh.write('#include "mettle/lib/xmettle.h"\n\n')
            self._hfh.write('#include "mettle/io/iserializable.h"\n\n')
            self._hfh.write('#include "mettle/braze/stdtypelists.h"\n\n')

            self._hfh.write('namespace Mettle\n')
            self._hfh.write('{\n')
            self._hfh.write('   namespace IO\n')
            self._hfh.write('   {\n')
            self._hfh.write('      class IReader;\n')
            self._hfh.write('      class IWriter;\n')
            self._hfh.write('   }\n')
            self._hfh.write('}\n\n')

            self._cfh.write('#include "mettle/lib/common.h"\n\n')
            self._cfh.write('#include "mettle/io/ireader.h"\n')
            self._cfh.write('#include "mettle/io/iwriter.h"\n\n')

        if self._mode == self.CLIENT:
            self._hfh.write('#include "mettle/braze/iclientmarshaler.h"\n')
            self._hfh.write('#include "mettle/braze/stdtypelists.h"\n\n')
            self._hfh.write('namespace Mettle { namespace Braze {\n')
            self._hfh.write('   class Client;\n')
            self._hfh.write('}}\n\n')

            self._cfh.write('#include "mettle/braze/client.h"\n')
            self._cfh.write('#include "mettle/braze/itransport.h"\n\n')
            self._cfh.write('#include "mettle/io/memorystream.h"\n')
            self._cfh.write('#include "mettle/io/ireader.h"\n')
            self._cfh.write('#include "mettle/io/iwriter.h"\n\n')

        if self._mode == self.SERVER:
            self._ifh.write('#include "mettle/braze/iserverinterface.h"\n\n')

            self._hfh.write('#include "mettle/braze/iservermarshaler.h"\n\n')
            self._hfh.write('#include "mettle/braze/stdtypelists.h"\n\n')
            self._hfh.write('namespace Mettle\n')
            self._hfh.write('{\n')
            self._hfh.write('   namespace Lib\n')
            self._hfh.write('   {\n')
            self._hfh.write('      class String;\n')
            self._hfh.write('   }\n\n')
            self._hfh.write('   namespace IO\n')
            self._hfh.write('   {\n')
            self._hfh.write('      class IStream;\n')
            self._hfh.write('      class MemoryStream;\n')
            self._hfh.write('   }\n\n')
            self._hfh.write('   namespace Braze\n')
            self._hfh.write('   {\n')
            self._hfh.write('      class Server;\n')
            self._hfh.write('      class ITransport;\n')
            self._hfh.write('   }\n')
            self._hfh.write('}\n\n')

            self._cfh.write('#include "mettle/lib/logger.h"\n')
            self._cfh.write('#include "mettle/lib/string.h"\n')
            self._cfh.write('#include "mettle/lib/xmettle.h"\n\n')
            self._cfh.write('#include "mettle/braze/server.h"\n')
            self._cfh.write('#include "mettle/braze/itransport.h"\n\n')
            self._cfh.write('#include "mettle/io/memorystream.h"\n')
            self._cfh.write('#include "mettle/io/ireader.h"\n')
            self._cfh.write('#include "mettle/io/iwriter.h"\n\n')


    def _gen_db_struct_headers(self):
        incss     = []

        structPath = self.get_option('includepath.tables').replace('|', '/').replace('\\', '/')

        if len(structPath) and not structPath.endswith('/'):
            structPath += '/'

        for dbs in self._gen_info['db_structs']:
            head   = '%s%s.h' % (structPath, dbs.table.lower())

            if head not in incss:
                incss.append(head)

        if not len(incss):
            return

        for i in incss:
            if self._ifh:
                self._ifh.write('#include "%s"\n' % i)

            if self._mode == self.STRUCT:
                self._hfh.write('#include "%s"\n' % i)

        if self._ifh:
            self._ifh.write('\n')

        if self._mode == self.STRUCT:
            self._hfh.write('\n')


    def _gen_trailers(self):
        self._hfh.write('#endif\n')

        if self._ifh:
            self._ifh.write('#endif\n')


    def _gen_begin_namespaces(self):
        ns = self._namespace(blank_ok = True)

        if ns == '':
            return

        for name in ns.split('.'):
            self._hfh.write('namespace %s { ' % name)
            self._cfh.write('namespace %s { ' % name)

            if self._ifh:
                self._ifh.write('namespace %s { ' % name)

        self._hfh.write('\n\n')
        self._cfh.write('\n\n')

        if self._ifh:
            self._ifh.write('\n\n')


    def _gen_end_namespaces(self):
        ns = self._namespace(blank_ok = True)

        if ns == '':
            return

        for name in ns.split('.'):
            self._hfh.write('}')
            self._cfh.write('}')

            if self._ifh:
                self._ifh.write('}')

        self._hfh.write('\n\n')
        self._cfh.write('\n\n')

        if self._ifh:
            self._ifh.write('\n\n')


    def _gen_braze_couplets(self):
        if self._mode != self.STRUCT:
            return

        if len(self._gen_info['proj'].couplets) < 1:
            return

        # Header Part
        for x, cobj in self._gen_info['proj'].couplets.items():
            cname = self._ident('braze.couplet', cobj.name)

            fmap    = self._field_map[cobj.ctype]
            keyType = ''
            keyMask = ''
            valMask = 'const char* %s;\n'
            const   = 'const '

            if fmap.type_flag == 'string':
                keyType = 'const char* '
                keyMask = 'const char* %s;\n'
                const   = ''
            elif fmap.type_flag == 'char':
                keyType = 'char'
                keyMask = 'char %s;\n'
            else:
                keyType = fmap.name
                keyMask = fmap.name + ' %s;\n'

            self._hfh.write('struct %s\n' % cname)
            self._hfh.write('{\n')

            for key, val in cobj.couplet.items():
                self._hfh.write('   static ')
                self._hfh.write(keyMask % ('%s' % self._ident_member('Key%s' % self._couplet_name(val))))

            self._hfh.write('\n')

            for key, val in cobj.couplet.items():
                self._hfh.write('   static ')
                self._hfh.write(valMask % ('%s' % self._ident_member('Value%s' % self._couplet_name(val))))

            self._hfh.write('\n')
            self._hfh.write('   static %s %s;\n' % ('unsigned int', self._ident_member('Count')))
            self._hfh.write('   static %s %s[];\n' % (keyType, self._ident_member('Keys')))
            self._hfh.write('   static %s %s[];\n' % ('const char*', self._ident_member('Values')))

            self._hfh.write('\n')
            self._hfh.write('   static const char* %s(%s%s key);\n' % (self._ident_method('GetValue'), const, keyType))

            self._hfh.write('};\n\n')


        # C File part
        for x, cobj in self._gen_info['proj'].couplets.items():
            cname = self._ident('braze.couplet', cobj.name)

            fmap    = self._field_map[cobj.ctype]
            keyType = ''
            keyMask = ''
            const   = 'const '
            valMask = '%s %s' % ('const char*', ' %s%s = "%s";\n')
            cmpMask = 'key == %s'
            keyList = []
            valList = []

            if fmap.type_flag == 'string':
                keyType = 'const char* '
                cmpMask = 'strcmp(key, %s) == 0'
                keyMask = '%s %s' % ('const char*', ' %s%s = "%s";\n')
                const   = ''
            elif fmap.type_flag == 'char':
                keyType = 'char'
                keyMask = '%s %s' % ('char', ' %s%s = \'%s\';\n')
            else:
                keyType = fmap.name
                keyMask = '%s %s' % (fmap.name, ' %s%s = %s;\n')

            for key, val in cobj.couplet.items():
                kname = self._ident_member(self._couplet_name('Key%s' % val))
                self._cfh.write(keyMask % ('%s::' % (cname), kname , str(key)))
                keyList.append('%s::%s' % (cname, kname))

            self._cfh.write('\n')

            for key, val in cobj.couplet.items():
                vname = self._ident_member(self._couplet_name('Value%s' % val))
                self._cfh.write(valMask % ('%s::' % (cname), vname, str(val)))
                valList.append('%s::%s' % (cname, vname))

            self._cfh.write('\n')
            self._cfh.write('%s %s%s = %s;\n' % (
                'unsigned int',
                '%s::' % (cname),
                self._ident_member('Count'),
                str(len(cobj.couplet))))

            self._cfh.write('%s %s%s = %s;\n' % (
                keyType,
                '%s::' % (cname),
                self._ident_member('Keys[]'),
                '{%s}' % ', '.join(keyList)))

            self._cfh.write('%s %s%s = %s;\n' % (
                'const char*',
                '%s::' % (cname),
                self._ident_member('Values[]'),
                '{%s}' % ', '.join(valList)))

            self._cfh.write('\n')
            self._cfh.write('const char* %s::%s(%s%s key)\n' % (cname, self._ident_member('getValue'), const, keyType))
            self._cfh.write('{\n')

            for i in range(len(cobj.couplet)):
                self._cfh.write('   if (')
                self._cfh.write(cmpMask % keyList[i])
                self._cfh.write(')\n')
                self._cfh.write('      return %s;\n\n' % valList[i])

            self._cfh.write('   return 0;\n')
            self._cfh.write('}\n\n')


    def _gen_braze_structs(self):
        if self._mode != self.STRUCT:
            return

        inherits = ['Mettle::IO::ISerializable()']

        for s in self._gen_info['proj'].struct_order:
            sobj  = self._gen_info['proj'].structs[s]
            sname = self._ident('braze.struct', sobj.name)

            self._hfh.write('class %s : public Mettle::IO::ISerializable\n' % sname)
            self._hfh.write('{\n')
            self._hfh.write('public:\n')

            # Struct::Struct()
            self._write_cpp_method('', sname, sname, None, inherits)
            self._cfh.write('{\n')
            self._cfh.write('   %s();\n' % self._ident_method('Clear'))
            self._cfh.write('}\n\n')

            # Struct::Struct(columns)
            self._write_cpp_method('', sname, sname, sobj.fields, inherits, ignore_types = ['timestamp'])
            self._cfh.write('{\n')
            self._write_copy_args('this->', sobj.fields, '', ['timestamp'])
            self._cfh.write('}\n\n')

            # Struct::Struct(copy constrctor)
            self._write_cpp_method('', sname, sname, 'const %s &copyObj' % sname, inherits)
            self._cfh.write('{\n')
            self._write_copy_args('', sobj.fields, 'copyObj.')
            self._cfh.write('}\n\n')

            # Struct::~Struct()
            self._write_cpp_method('', sname, '~%s' % sname, virtual=True)
            self._cfh.write('{\n')
            self._cfh.write('}\n\n')

            # void Struct::Clear(void)
            self._write_cpp_method('void', sname, self._ident_method('Clear'))
            self._cfh.write('{\n')
            self._write_clear_fields(sobj.fields)
            self._cfh.write('}\n\n')

            # unsigned int Struct::_Serialize()
            self._write_cpp_method('const char*', sname, '_name', '', const=True)
            self._cfh.write('{\n')
            self._cfh.write('   return "%s";\n' % sname)
            self._cfh.write('}\n\n')

            # unsigned int Struct::_Serialize()
            self._write_cpp_method('unsigned int',
                                   sname,
                                   '_serialize',
                                   'Mettle::IO::IWriter* _w, const char* _defName=0',
                                   const=True)
            self._cfh.write('{\n')
            self._cfh.write('   unsigned int _sizeWritten = 0;\n\n')
            self._cfh.write('   _sizeWritten += _w->writeStart(_defName ? _defName : _name());\n')

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        self._cfh.write('   _sizeWritten += %s._serialize(_w);\n' % (self._ident_member(a.name)))
                    else:
                        self._cfh.write('   _sizeWritten += _w->write("%s", %s);\n' % (a.name, self._ident_member(a.name)))


            self._cfh.write('   _sizeWritten += _w->writeEnd(_defName);\n')
            self._cfh.write('\n   return _sizeWritten;\n')
            self._cfh.write('}\n\n')

            # unsigned int Struct::_Deserialize()
            self._write_cpp_method('unsigned int', sname, '_deserialize', 'Mettle::IO::IReader* _r, const char* _defName=0')
            self._cfh.write('{\n')
            self._cfh.write('   unsigned int _sizeRead = 0;\n\n')
            self._cfh.write('   _sizeRead += _r->readStart(_defName ? _defName : _name());\n')

            if sobj.fields:
                for a in sobj.fields:
                    if a.is_array or a.type in ['dbrec', 'brazerec']:
                        self._cfh.write('   _sizeRead += %s._deserialize(_r);\n' % (self._ident_member(a.name)))
                    else:
                        self._cfh.write('   _sizeRead += _r->read("%s", %s);\n' % (a.name, self._ident_member(a.name)))

            self._cfh.write('   _sizeRead += _r->readEnd(_defName);\n')
            self._cfh.write('\n   return _sizeRead;\n')
            self._cfh.write('}\n\n')

            # List class
            self._hfh.write('   DECLARE_SAFE_CLASS(%s);\n\n' % sname)
            self._hfh.write('   class List : public Mettle::Lib::Collection<%s>, public Mettle::IO::ISerializable\n' % sname)
            self._hfh.write('   {\n')
            self._hfh.write('   public:\n')

            self._write_cpp_method('const char*', '%s::List' % sname, '_name', '', const=True, extra_spaces='   ')
            self._cfh.write('{\n')
            self._cfh.write('   return "%s.List";\n' % sname)
            self._cfh.write('}\n\n')

            self._write_cpp_method('unsigned int',
                                   '%s::List' % sname,
                                   '_serialize',
                                   'Mettle::IO::IWriter* _w, const char* _defName=0',
                                   const=True,
                                   extra_spaces = '   ')
            self._cfh.write('{\n')
            self._cfh.write('   unsigned int _sizeWritten = 0;\n')
            self._cfh.write('   uint32_t     _cnt      = (uint32_t) this->count();\n')
            self._cfh.write('   uint32_t     _idx;\n\n')
            self._cfh.write('   _sizeWritten += _w->writeStart(_defName ? _defName : _name());\n')
            self._cfh.write('   _sizeWritten += _w->write("ListSize", _cnt);\n\n')
            self._cfh.write('   for (_idx = 0; _idx < _cnt; ++_idx)\n')
            self._cfh.write('      _sizeWritten += _list[_idx]->_serialize(_w);\n\n')
            self._cfh.write('   _sizeWritten += _w->writeEnd(_defName);\n')
            self._cfh.write('\n   return _sizeWritten;\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('unsigned int',
                                   '%s::List' % sname,
                                   '_deserialize',
                                   'Mettle::IO::IReader* _r, const char* _defName = 0',
                                   extra_spaces='   ')
            self._cfh.write('{\n')
            self._cfh.write('   unsigned int _sizeRead = 0;\n')
            self._cfh.write('   uint32_t     _cnt      = 0;\n')
            self._cfh.write('   uint32_t     _idx;\n\n')
            self._cfh.write('   _sizeRead += _r->readStart(_defName ? _defName : _name());\n')
            self._cfh.write('   _sizeRead += _r->read("ListSize", _cnt);\n\n')
            self._cfh.write('   allocate(_cnt);\n\n')
            self._cfh.write('   for (_idx = 0; _idx < _cnt; ++_idx)\n')
            self._cfh.write('      _sizeRead += _list[_idx]->_deserialize(_r);\n\n')
            self._cfh.write('   _sizeRead += _r->readEnd(_defName);\n')
            self._cfh.write('\n   return _sizeRead;\n')
            self._cfh.write('}\n\n')

            self._hfh.write('      DECLARE_SAFE_CLASS(%s::List);\n\n' % sname)
            self._hfh.write('   private:\n')
            self._hfh.write('   };\n\n')

            # DeclareFields
            self._write_member_decleration(sobj.fields)
            self._hfh.write('\n')

            self._hfh.write('};\n\n')


    def _gen_server_interface(self):
        if self._mode != self.SERVER:
            return

        self._serverInterface = self._ident('server.interface', self._gen_info['proj'].name)

        self._ifh.write('class %s : public Mettle::Braze::IServerInterface\n' % self._serverInterface)
        self._ifh.write('{\n')
        self._ifh.write('protected:\n')
        self._ifh.write('   %s() {}\n\n' % self._serverInterface)
        self._ifh.write('public:\n')
        self._ifh.write('   virtual ~%s() {}\n\n' % self._serverInterface)


        for call in self._gen_info['proj'].calls:
            return_type  = self._gen_return_type_str(call)
            args         = self._gen_param_str(call)
            sep          = '\n      '
            method       = '   virtual %s%s %s(' % (
                return_type['decl'], '*' if return_type['safe'] else '', self._ident_method(call.name))

            self._ifh.write(method)

            for a in args:
                self._ifh.write('%s%s' % (sep, a))
                sep     = ',\n      '

            self._ifh.write(') = 0;\n\n')

        self._ifh.write('};\n\n')


    def _gen_client_interface(self):
        if self._mode != self.CLIENT:
            return

        self._clientInterface = self._ident('client.interface', self._gen_info['proj'].name)

        self._ifh.write('class %s\n' % self._clientInterface)
        self._ifh.write('{\n')
        self._ifh.write('protected:\n')
        self._ifh.write('   %s() {}\n\n' % self._clientInterface)
        self._ifh.write('public:\n')
        self._ifh.write('   virtual ~%s() {}\n\n' % self._clientInterface)

        for call in self._gen_info['proj'].calls:
            return_type = self._gen_return_type_str(call)
            args        = self._gen_param_str(call)
            sep         = '\n      '
            method      = '   virtual %s %s%s(' % (
                return_type['decl'], '*' if return_type['safe'] else '', self._ident_method(call.name))

            self._ifh.write(method)

            for a in args:
                self._ifh.write('%s%s' % (sep, a))
                sep     = ',\n      '

            self._ifh.write(') = 0;\n\n')

        self._ifh.write('};\n\n')


    def _gen_server_header(self):
        if self._mode != self.SERVER:
            return

        self._serverClass = self._ident('server.marshaler', self._gen_info['proj'].name)

        self._hfh.write('class %s : public Mettle::Braze::IServerMarshaler\n' % (self._serverClass))
        self._hfh.write('{\n')
        self._hfh.write('public:\n')
        self._hfh.write('            %s(%s* serverImpl);\n\n' % (self._serverClass, self._serverInterface))
        self._hfh.write('   virtual ~%s();\n\n' % self._serverClass)
        self._hfh.write('   const char* _signature();\n\n')

        self._hfh.write('   Mettle::Braze::IServerInterface* _serverImpl();\n\n')
        self._hfh.write('   int32_t  _serve(\n')
        self._hfh.write('      Mettle::Braze::Server*     __server,\n')
        self._hfh.write('      const Mettle::Lib::String& __remoteSignature,\n')
        self._hfh.write('      Mettle::IO::IStream*       __input,\n')
        self._hfh.write('      Mettle::IO::IStream*       __output,\n')
        self._hfh.write('      int32_t&                   __errorCode,\n')
        self._hfh.write('      Mettle::Lib::String*       __errMsg);\n\n')
        self._hfh.write('private:\n\n')

        for call in self._gen_info['proj'].calls:
            self._hfh.write('   void %s(' % (self._ident_method(call.name)))
            self._hfh.write('Mettle::IO::MemoryStream* _i, ')
            self._hfh.write('Mettle::IO::MemoryStream* _o);\n\n')


        self._hfh.write('   %s* _server;\n' % 'Mettle::Braze::Server')
        self._hfh.write('   %s* _simpl;\n' % self._serverInterface)
        self._hfh.write('};\n\n')


    def _gen_client_header(self):
        if self._mode != self.CLIENT:
            return

        self._clientClass = self._ident('client.marshaler', self._gen_info['proj'].name)

        self._hfh.write('class %s :\n' % (self._clientClass))
        self._hfh.write('    public Mettle::Braze::IClientMarshaler,\n')
        self._hfh.write('    public %s\n' % (self._clientInterface))
        self._hfh.write('{\n')
        self._hfh.write('public:\n')
        self._hfh.write('            %s(Mettle::Braze::Client* client);\n\n' % self._clientClass)
        self._hfh.write('   virtual ~%s();\n\n' % self._clientClass)
        self._hfh.write('   const char* _signature();\n\n')

        for call in self._gen_info['proj'].calls:
            return_type   = self._gen_return_type_str(call)
            args         = self._gen_param_str(call)

            method  = '   %s%s %s(' % (return_type['decl'], '*' if return_type['safe'] else '', self._ident_method(call.name))
            sep     = '\n      '

            self._hfh.write(method)

            for a in args:
                self._hfh.write('%s%s' % (sep, a))
                sep = ',\n      '

            self._hfh.write(');\n\n')

        self._hfh.write('private:\n\n')
        self._hfh.write('   Mettle::Braze::Client* _client;\n\n')
        self._hfh.write('};\n\n')


    def _gen_server_code(self):
        if self._mode != self.SERVER:
            return

        self._cfh.write('%s::%s(' % (self._serverClass, self._serverClass))
        self._cfh.write('   %s *serverImpl)\n' % self._serverInterface)
        self._cfh.write('   :Mettle::Braze::IServerMarshaler(serverImpl)\n')
        self._cfh.write('{\n')
        self._cfh.write('   _simpl   = serverImpl;\n')
        self._cfh.write('   _server  = 0;\n')
        self._cfh.write('}\n\n')

        self._cfh.write('%s::~%s()\n' % (self._serverClass, self._serverClass))
        self._cfh.write('{\n')
        self._cfh.write('}\n\n')

        self._cfh.write('const char* %s::_signature()\n' % self._serverClass)
        self._cfh.write('{\n')
        self._cfh.write('   return "%s";\n' % self._gen_info['server_sig'])
        self._cfh.write('}\n\n')

        self._cfh.write('Mettle::Braze::IServerInterface *%s::_serverImpl()\n' % self._serverClass)
        self._cfh.write('{\n')
        self._cfh.write('   return _simpl;\n')
        self._cfh.write('}\n\n')

        self._cfh.write('int32_t %s::_serve(\n' % self._serverClass)
        self._cfh.write('    Mettle::Braze::Server*     __server,\n')
        self._cfh.write('    const Mettle::Lib::String& __remoteSignature,\n')
        self._cfh.write('    Mettle::IO::IStream*       __input,\n')
        self._cfh.write('    Mettle::IO::IStream*       __output,\n')
        self._cfh.write('    int32_t&                   __errorCode,\n')
        self._cfh.write('    Mettle::Lib::String*       __errMsg)\n')
        self._cfh.write('{\n')
        self._cfh.write('   Mettle::IO::MemoryStream ims;\n')
        self._cfh.write('   Mettle::IO::MemoryStream oms;\n\n')
        self._cfh.write('   _server     = __server;\n')
        self._cfh.write('   __errorCode = 0;\n\n')
        self._cfh.write('   __input->poop(&ims, 0);\n\n')
        self._cfh.write('   try\n')
        self._cfh.write('   {\n')

        sep = "if"

        for call in self._gen_info['proj'].calls:
            self._cfh.write('      %s (__remoteSignature == "%s")\n' % (sep, call.signature))
            self._cfh.write('         %s(&ims, &oms);\n' % self._ident_method(call.name))
            sep = "else if"

        self._cfh.write('      else\n')
        self._cfh.write('         throw Mettle::Lib::xMettle(__FILE__, __LINE__, "%s", "_serve() - Remote Signature (%s)'
                        ' is not known!", __remoteSignature.c_str());\n' % (self._serverClass, '%s'))

        self._cfh.write('   }\n')
        self._cfh.write('   catch (Mettle::Lib::xTerminate &x)\n')
        self._cfh.write('   {\n')
        self._cfh.write('      _server->logger()->traceUnwind();\n')
        self._cfh.write('      _server->logger()->spot(__FILE__, __LINE__, x);\n')
        self._cfh.write('      Mettle::Lib::String caddr;\n')
        self._cfh.write('      _server->logger()->error("Client Address: (%s):", _server->transport()->clientAddress'
                        '(&caddr)->c_str());\n')
        self._cfh.write('      throw;\n')
        self._cfh.write('   }\n')
        self._cfh.write('   catch (Mettle::Lib::xMettle &x)\n')
        self._cfh.write('   {\n')
        self._cfh.write('      _server->logger()->traceUnwind();\n')
        self._cfh.write('      _server->logger()->spot(__FILE__, __LINE__, x);\n')
        self._cfh.write('      Mettle::Lib::String caddr;\n')
        self._cfh.write('      _server->logger()->error("Client Address: (%s):", _server->transport()->clientAddress'
                        '(&caddr)->c_str());\n')
        self._cfh.write('      __errorCode = (int32_t) x.errorCode;\n')
        self._cfh.write('      *__errMsg = x.errorMsg;\n')
        self._cfh.write('   }\n')
        self._cfh.write('   catch (std::exception &x)\n')
        self._cfh.write('   {\n')
        self._cfh.write('      _server->logger()->traceUnwind();\n')
        self._cfh.write('      _server->logger()->spot(__FILE__, __LINE__, x);\n')
        self._cfh.write('      Mettle::Lib::String caddr;\n')
        self._cfh.write('      _server->logger()->error("Client Address: (%s):", _server->transport()->clientAddress'
                        '(&caddr)->c_str());\n')
        self._cfh.write('      __errorCode = (int32_t) Mettle::Lib::xMettle::StandardException;\n')
        self._cfh.write('      *__errMsg = x.what();\n')
        self._cfh.write('   }\n')
        self._cfh.write('   catch (...)\n')
        self._cfh.write('   {\n')
        self._cfh.write('      _server->logger()->traceUnwind();\n')
        self._cfh.write('      _server->logger()->spot(__FILE__, __LINE__);\n')
        self._cfh.write('      __errorCode = 1;\n')
        self._cfh.write('      Mettle::Lib::String caddr;\n')
        self._cfh.write('      _server->logger()->error("Client Address: (%s):", _server->transport()->clientAddress'
                        '(&caddr)->c_str());\n')
        self._cfh.write('      throw Mettle::Lib::xTerminate(__FILE__, __LINE__, "%s", "_serve()'
                        ' - Unknown exception caught!");\n' % self._serverClass)
        self._cfh.write('   }\n\n')
        self._cfh.write('   if (!__errorCode)\n')
        self._cfh.write('      __output->eat(&oms);\n\n')
        self._cfh.write('   return __errorCode;\n')
        self._cfh.write('}\n\n')

        for call in self._gen_info['proj'].calls:
            return_type = self._gen_return_type_str(call)

            self._cfh.write('void %s::%s(Mettle::IO::MemoryStream* _i, Mettle::IO::MemoryStream* _o)\n' % (
                self._serverClass, self._ident_method(call.name)))
            self._cfh.write('{\n')
            self._cfh.write('   _server->logger()->traceReset();\n')
            self._cfh.write('   _server->logger()->trace(__FILE__, __LINE__)->debug("[%s - Start]");\n\n' % (
                self._ident_method(call.name)))
            self._gen_server_declare_varibles(call, return_type)
            self._gen_server_assign_input_args(call)
            self._gen_server_server_call(call, return_type)
            self._gen_server_assign_output_args(call, return_type)
            self._cfh.write('   _server->logger()->trace(__FILE__, __LINE__)->debug("[%s - Done]");\n' % (
                self._ident_method(call.name)))
            self._cfh.write('}\n\n')


    def _gen_client_code(self):
        if self._mode != self.CLIENT:
            return

        self._cfh.write('%s::%s(Mettle::Braze::Client* client)\n' % (self._clientClass, self._clientClass))
        self._cfh.write('   :Mettle::Braze::IClientMarshaler(),\n')
        self._cfh.write('    %s()\n' % self._clientInterface)
        self._cfh.write('{\n')
        self._cfh.write('   _client = client;\n')
        self._cfh.write('}\n\n')

        self._cfh.write('%s::~%s()\n' % (self._clientClass, self._clientClass))
        self._cfh.write('{\n')
        self._cfh.write('}\n\n')

        self._cfh.write('const char* %s::_signature()\n' % self._clientClass)
        self._cfh.write('{\n')
        self._cfh.write('   return "%s";\n' % self._gen_info['server_sig'])
        self._cfh.write('}\n\n')

        for call in self._gen_info['proj'].calls:
            return_type  = self._gen_return_type_str(call)
            args         = self._gen_param_str(call)
            sep          = '\n   '
            method       = '%s%s %s::%s(' % (
                return_type['decl'],
                '*' if return_type['safe'] else '',
                self._clientClass,
                self._ident_method(call.name))

            self._cfh.write(method)

            for a in args:
                self._cfh.write('%s%s' % (sep, a))
                sep     = ',\n   '

            self._cfh.write(')\n{\n')

            self._gen_client_declare_varibles(call, return_type)
            self._gen_client_assign_input_args(call)
            self._gen_client_server_call(call)
            self._gen_client_assign_output_args(call, return_type)

            self._cfh.write('}\n\n')


    def _gen_return_type_str(self, call):
        if not call.returns:
            return {'decl': 'void', 'safe': False}

        if call.returns.is_array :

            fmap = self._field_map[call.returns.type]

            if call.returns.type == 'brazerec':
                return {'decl': '%s::List' % self._ident('braze.struct', call.returns.brazestruct.struct_name()), 'safe': True}

            if call.returns.type == 'dbrec':
                return {'decl': '%s::List' % call.returns.dbstruct.struct_name(), 'safe': True}

            if call.returns.type == 'memblock':
                return {'decl': 'Mettle::Braze::MemoryBlockList', 'safe': True}

            if call.returns.type == 'uuid':
                return {'decl': 'Mettle::Braze::GuidList', 'safe': True}

            return {'decl': 'Mettle::Braze::%s%sList' % (call.returns.type[0].upper(), call.returns.type[1:]), 'safe': True}

        if call.returns.type == 'brazerec':
            return {'decl': self._ident('braze.struct', call.returns.brazestruct.struct_name()), 'safe': True}

        if call.returns.type == 'dbrec':
            return {'decl': call.returns.dbstruct.struct_name(), 'safe': True}

        fmap = self._field_map[call.returns.type]

        if fmap.type_flag in ('string', 'date', 'memblock'):
            return {'decl': fmap.name, 'safe': True}

        return {'decl': fmap.name, 'safe': False}


    def _gen_param_str(self, call):
        args = []

        for f in call.fields:
            if f.io == 'i':
                pre1 = 'const '
                pre2 = ''
                msg  = '/* i  */ '
            elif f.io == 'o':
                pre1 = ''
                pre2 = '&'
                msg  = '/* o  */ '
            else:
                pre1 = ''
                pre2 = '&'
                msg  = '/* io */ '

            fmap = self._field_map[f.type]

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    args.append('%s%s%s %s' % (
                        msg,
                        '%s%s::List' % (pre1, self._ident('braze.struct', f.brazestruct.struct_name())),
                        '&',
                        self._ident_member(f.name)))
                elif fmap.type_flag == 'dbrec':
                    args.append('%s%s%s %s' % (
                        msg,
                        '%s%s::List' % (pre1, f.dbstruct.struct_name()),
                        '&',
                        self._ident_member(f.name)))
                else:
                    if f.type == 'memblock':
                        args.append('%s%s%s %s' % (
                            msg,
                            '%sMettle::Braze::MemoryBlockList' % (pre1),
                            '&',
                            self._ident_member(f.name)))
                    elif f.type == 'uuid':
                        args.append('%s%s%s %s' % (
                            msg,
                            '%sMettle::Braze::GuidList' % (pre1),
                            '&',
                            self._ident_member(f.name)))
                    else:
                        args.append('%s%s%s %s' % (
                            msg,
                            '%sMettle::Braze::%s%sList' % (pre1, f.type[0].upper(), f.type[1:]),
                            '&',
                            self._ident_member(f.name)))
                continue

            if fmap.type_flag == 'brazerec':
                args.append('%s%s%s %s' % (
                    msg,
                    '%s%s' % (pre1, self._ident('braze.struct', f.brazestruct.struct_name())),
                    '&',
                    self._ident_member(f.name)))
            elif fmap.type_flag == 'dbrec':
                args.append('%s%s%s %s' % (
                    msg,
                    '%s%s' % (pre1, f.dbstruct.struct_name()),
                    '&',
                    self._ident_member(f.name)))
            elif fmap.type_flag in ('string', 'date', 'memblock'):
                args.append('%s%s%s %s' % (
                    msg,
                    '%s%s' % (pre1, fmap.name),
                    '&',
                    self._ident_member(f.name)))
            else:
                args.append('%s%s%s %s' % (
                    msg,
                    '%s%s' % (pre1, fmap.name),
                    pre2,
                    self._ident_member(f.name)))

        return args


    def _gen_client_declare_varibles(self, call, return_type):
        self._cfh.write('   %s _i;\n' % 'Mettle::IO::MemoryStream')
        self._cfh.write('   %s _o;\n' % 'Mettle::IO::MemoryStream')

        call.hasInput   = False
        call.hasOutput  = False

        for f in call.fields:
            if f.io in ['i', 'io']:
                self._cfh.write('   %s _w(0);\n' % 'Mettle::IO::IWriter::Safe')
                call.hasInput = True
                break

        for f in call.fields:
            if f.io in ['o', 'io']:
                self._cfh.write('   %s _r(0);\n' % 'Mettle::IO::IReader::Safe')
                call.hasOutput = True
                break

        if not call.returns:
            self._cfh.write('\n')
            return

        if not call.hasOutput:
            self._cfh.write('   %s _r(0);\n' % 'Mettle::IO::IReader::Safe')
            call.hasOutput = True

        if return_type['safe']:
            self._cfh.write('   %s _x(0);\n\n' % ('%s::Safe' % return_type['decl']))
        else:
            self._cfh.write('   %s _x;\n\n' % (return_type['decl']))


    def _gen_client_assign_input_args(self, call):
        if not call.hasInput:
            return

        self._cfh.write('   _w.remember(_client->transport()->newWriter(&_i));\n')
        self._cfh.write('   _w.obj->writeStart("%s_IN");\n' % (call.name))


        for f in call.fields:
            if f.io == 'o':
                continue

            fmap  = self._field_map[f.type]

            if fmap.type_flag in ('brazerec', 'dbrec') or f.is_array:
                self._cfh.write('   %s._serialize(_w.obj);\n' % (self._ident_member(f.name)))
            else:
                self._cfh.write('   _w.obj->write("%s", %s);\n' % (f.name, self._ident_member(f.name)))

        self._cfh.write('   _w.obj->writeEnd("%s_IN");\n\n' % (call.name))


    def _gen_client_server_call(self, call):
        sig = call.signature

        self._cfh.write('   _client->send(this,    "%s", &_i);\n' % (sig))
        self._cfh.write('   _client->receive(this, "%s", &_o);\n\n' % (sig))


    def _gen_client_assign_output_args(self, call, return_type):
        if not call.hasOutput:
            return

        self._cfh.write('   _r.remember(_client->transport()->newReader(&_o));\n')
        self._cfh.write('   _r.obj->readStart("%s_OUT");\n' % (call.name))

        if call.returns:
            if call.returns.is_array:
                self._cfh.write('   _x.remember(new %s());\n' % return_type['decl'])
                self._cfh.write('   _x.obj->_deserialize(_r.obj);\n')
            elif return_type['safe']:
                self._cfh.write('   _x.remember(new %s());\n' % return_type['decl'])

                if call.returns.type in ['date', 'string', 'memblock']:
                    self._cfh.write('   _r.obj->read("return", *_x.obj);\n')
                else:
                    self._cfh.write('   _x.obj->_deserialize(_r.obj);\n')
            else:
                self._cfh.write('   _r.obj->read("return", _x);\n')

        for f in call.fields:
            if f.io == 'i':
                continue

            fmap = self._field_map[f.type]

            if fmap.type_flag in ('brazerec', 'dbrec') or f.is_array:
                if f.io == 'io':
                    self._cfh.write('   %s.%s();\n' % (self._ident_member(f.name), self._ident_method('Clear')))

                self._cfh.write('   %s._deserialize(_r.obj);\n' % (self._ident_member(f.name)))
            else:
                self._cfh.write('   _r.obj->read("%s", %s);\n' % (f.name, self._ident_member((f.name))))

        self._cfh.write('   _r.obj->readEnd("%s_OUT");\n' % (call.name))

        if call.returns:
            if return_type['safe']:
                self._cfh.write('\n   return _x.forget();\n')
            else:
                self._cfh.write('\n   return _x;\n')


    def _gen_server_declare_varibles(self, call, return_type):
        call.hasInput   = False
        call.hasOutput  = False

        for f in call.fields:
            if f.io in ['i', 'io']:
                self._cfh.write('   %s _r(0);\n' % 'Mettle::IO::IReader::Safe')
                call.hasInput = True
                break

        for f in call.fields:
            if f.io in ['o', 'io']:
                self._cfh.write('   %s _w(0);\n' % 'Mettle::IO::IWriter::Safe')
                call.hasOutput = True
                break

        if return_type['decl'] != 'void' and not call.hasOutput:
            self._cfh.write('   %s _w(0);\n' % 'Mettle::IO::IWriter::Safe')
            call.hasOutput = True

        if return_type['decl'] != 'void':
            if return_type['safe']:
                self._cfh.write('   %s _x(0);\n' % ('%s::Safe' % return_type['decl']))
            else:
                self._cfh.write('   %s _x;\n' % (return_type['decl']))

        if not call.hasInput and not call.hasOutput:
            return

        if len(call.fields) > 0:
            self._cfh.write('\n')

        for f in call.fields:
            fmap = self._field_map[f.type]

            if f.is_array:
                if fmap.type_flag == 'brazerec':
                    self._cfh.write('   %s %s;\n' % (
                        '%s::List' % (self._ident('braze.struct', f.brazestruct.struct_name())),
                        self._ident_member(f.name)))
                elif fmap.type_flag == 'dbrec':
                    self._cfh.write('   %s %s;\n' % (
                        '%s::List' % (f.dbstruct.struct_name()),
                        self._ident_member(f.name)))
                else:
                    if f.type == 'memblock':
                        self._cfh.write('   %s %s;\n' % ('Mettle::Braze::MemoryBlockList', f.name))
                    else:
                        self._cfh.write('   %s %s;\n' % (
                            'Mettle::Braze::%s%sList' % (f.type[0].upper(), f.type[1:]),
                            self._ident_member(f.name)))
                continue

            if fmap.type_flag == 'brazerec':
                self._cfh.write('   %s %s;\n' % (
                    '%s' % (self._ident('braze.struct', f.brazestruct.struct_name())),
                    self._ident_member(f.name)))
            elif fmap.type_flag == 'dbrec':
                self._cfh.write('   %s %s;\n' % (
                    '%s' % (f.dbstruct.struct_name()),
                    self._ident_member(f.name)))
            else:
                self._cfh.write('   %s %s;\n' % ('%s' % (fmap.name), self._ident_member(f.name)))

        self._cfh.write('\n')


    def _gen_server_assign_input_args(self, call):
        if not call.hasInput:
            return

        self._cfh.write('   _r.remember(_server->transport()->newReader(_i));\n')
        self._cfh.write('   _r.obj->readStart("%s_IN");\n' % (call.name))

        for f in call.fields:
            if f.io == 'o':
                continue

            fmap  = self._field_map[f.type]

            if fmap.type_flag in ('brazerec', 'dbrec') or f.is_array:
                self._cfh.write('   %s._deserialize(_r.obj);\n' % (self._ident_member(f.name)))
            else:
                self._cfh.write('   _r.obj->read("%s", %s);\n' % (f.name, self._ident_member(f.name)))

        self._cfh.write('   _r.obj->readEnd("%s_IN");\n\n' % (call.name))


    def _gen_server_server_call(self, call, return_type):
        if return_type['decl'] == 'void':
            meth  = '   _simpl->%s(' % (self._ident_method(call.name))
        else:
            if return_type['safe']:
                meth = '   _x.remember(_simpl->%s(' % (self._ident_method(call.name))
            else:
                meth = '   _x = _simpl->%s(' % (self._ident_method(call.name))

        self._cfh.write(meth)

        if len(call.fields) <= 1:
            for f in call.fields:
                self._cfh.write(self._ident_member(f.name))
        else:
            sep = '\n      '

            for f in call.fields:
                self._cfh.write('%s%s' % (sep, self._ident_member(f.name)))
                sep = ',\n      '

        if return_type['decl'] != 'void' and return_type['safe']:
            self._cfh.write(')')

        self._cfh.write(');\n\n')


    def _gen_server_assign_output_args(self, call, return_type):
        if not call.hasOutput:
            return

        self._cfh.write('   _w.remember(_server->transport()->newWriter(_o));\n')
        self._cfh.write('   _w.obj->writeStart("%s_OUT");\n' % (call.name))

        if call.returns:
            if call.returns.is_array:
                self._cfh.write('   _x.obj->_serialize(_w.obj);\n')
            elif return_type['safe']:
                if call.returns.type in ['date', 'string', 'memblock']:
                    self._cfh.write('   _w.obj->write("return", *_x.obj);\n')
                else:
                    self._cfh.write('   _x.obj->_serialize(_w.obj);\n')
            else:
                self._cfh.write('   _w.obj->write("return", _x);\n')

        for f in call.fields:
            if f.io == 'i':
                continue

            fmap  = self._field_map[f.type]

            if fmap.type_flag in ('brazerec', 'dbrec') or f.is_array:
                self._cfh.write('   %s._serialize(_w.obj);\n' % (self._ident_member(f.name)))
            else:
                self._cfh.write('   _w.obj->write("%s", %s);\n' % (f.name, self._ident_member(f.name)))

        self._cfh.write('   _w.obj->writeEnd("%s_OUT");\n\n' % (call.name))
