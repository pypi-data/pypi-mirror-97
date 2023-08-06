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

import datetime
import logging
import stringcase
import os.path


class Generator:

    COUPLET          = 'COUPLET'
    STRUCT           = 'STRUCT'
    CLIENT           = 'CLIENT'
    SERVER           = 'SERVER'
    EXCEPTION_OBJECT = ''

    class FieldMap:
        def __init__(self,
                     name      : str,
                     length    : int = None,
                     type_flag : str = '',
                     methodpre : str = '',
                     def_val   : str = ''):
            self.name      = name
            self.length    = length
            self.type_flag = type_flag
            self.methodpre = methodpre
            self.def_val   = def_val


    class GeneratedFile:
        def __init__(self, fname: str, ext: str, path: str, namespace: str, cls: str = None):
            self.fname     = fname
            self.ext       = ext
            self.path      = path
            self.namespace = namespace
            self.cls       = cls


    def __init__(self, extensions: list):
        self.enabled      = False
        self.dest_dir     = ''
        self.namespace    = ''
        self._options     = {}
        self._extensions  = extensions
        self._gened_files = {}
        self._idents      = {}

        self._field_map = {
            'bool'        : None,
            'int8'        : None,
            'int16'       : None,
            'int32'       : None,
            'int64'       : None,
            'uint8'       : None,
            'uint16'      : None,
            'uint32'      : None,
            'uint64'      : None,
            'char'        : None,
            'string'      : None,
            'date'        : None,
            'time'        : None,
            'datetime'    : None,
            'double'      : None,
            'brazerec'    : None,
            'dbrec'       : None,
            'memoryBlock' : None,
        }

        self._dav_map = {
            'min'   : 'Min',
            'max'   : 'Max',
            'null'  : 'NotNull',
            'regex' : 'Regex',
            'func'  : 'Func',
            'in'    : 'In',
            'notin' : 'NotIn',
        }



    def name(self) -> str:
        return 'Base Target'


    def init(self, enabled, dest_dir = None , opts = {}):
        self.enabled = enabled

        if dest_dir:
            self.dest_dir = dest_dir

        for key, val in opts.items():
            self._options[key] = val


    def _init_code_options(self, extra_opt: dict = {}):
        std_options = {
            'braze.struct'       : None,
            'braze.couplet'      : None,
            'client.marshaler'   : None,
            'client.interface'   : None,
            'client.serverimpl'  : None,
            'server.marshaler'   : None,
            'server.interface'   : None,
            'namespace'          : None,
            'async'              : None,
        }

        for key, val in std_options.items():
            x = self._options.get(key)

            if x is None:
                self._options[key] = val


        for key, val in extra_opt.items():
            x = self._options.get(key)

            if x is None:
                self._options[key] = val


    def _init_casing(self, casing):
        cdict = self._options.get('casing')

        if cdict is None:
            cdict = {}

            self._options['casing'] = cdict

        for key, val in casing.items():
            x = cdict.get(key)

            if x is None:
                cdict[key] = val


    def _couplet_name(self, cname):
        res = ''

        for x in cname:
            if x.isdigit() or x.isalpha():
                res += x
            else:
                res += '_'

        return '%s%s' % (res[0].capitalize(), res[1:])


    def initialize_generation(self, gen_info: dict):
        self._gened_files = {}


    def finalize_generation(self, gen_info: dict):
        pass


    def generate_structs(self, gen_info: dict):
        raise Exception('GenerateStructs for "%s" not implemented' % self.name())


    def generate_client(self, gen_info: dict):
        raise Exception('GenerateClient for "%s" not implemented' % self.name())


    def generate_server(self, gen_info: dict):
        raise Exception('GenerateServer for "%s" not implemented' % self.name())


    def clean(self, gen_info: dict):
        if not self._extensions:
            return

        for ext in self._extensions:
            delfiles = self.filename_and_path(gen_info, '*',  ext)
            parts    = os.path.split(delfiles)

            if not os.path.exists(parts[0]):
                continue

            listfile = os.listdir(parts[0])
            cnt      = 0

            for x in listfile:
                if not x.endswith('%s%s' % (os.extsep, ext)):
                    continue

                os.remove(os.path.join(parts[0], x))
                cnt += 1

            logging.info('Cleaned (%d) - %s' % (cnt, delfiles))


    def filename_and_path(self, gen_info: dict, name: str, ext: str, extra_dir: str = ''):
        nap     = gen_info['proj'].project_dir
        destdir = os.path.join(nap, self.dest_dir)
        destdir = self.dest_dir.replace('|', os.path.sep).replace('\\', os.path.sep).replace('/', os.path.sep)

        if len(extra_dir):
            destdir = os.path.join(destdir, extra_dir.lower())

        destdir = os.path.join(nap, destdir)

        if not os.path.exists(destdir):
            logging.info('Creating missing target dir (%s)' % destdir)
            os.makedirs(destdir)
        elif not os.path.isdir(destdir):
            raise Exception('Destination dir (%s) - is not a directory' % destdir)

        return os.path.join(destdir, '%s.%s' % (name, ext))


    def gened_file_open(self,
                        gen_info              : dict,
                        fname                 : str,
                        ext                   : str = None,
                        namespace             : str = None,
                        cls                   : str = None,
                        extra_dir             : str = None,
                        add_namespace_to_path : bool = False):
        if not cls:
            cls = fname

        if not namespace:
            namespace = self._namespace()

        if not ext:
            ext = self._extensions[0]

        nap     = gen_info['proj'].project_dir
        destdir = os.path.join(nap, self.dest_dir).replace('\\', os.path.sep)\
                                                  .replace('/', os.path.sep)\
                                                  .replace('|', os.path.sep)\

        if add_namespace_to_path and namespace != '':
            for nsps in namespace.split('.'):
                destdir = os.path.join(destdir, nsps)

        if extra_dir:
            destdir = os.path.join(destdir, extra_dir)

        if not os.path.exists(destdir):
            logging.info('Creating missing target dir (%s)' % destdir)
            os.makedirs(destdir)
        elif not os.path.isdir(destdir):
            raise Exception('Destination dir (%s) - is not a directory' % destdir)

        fullpath = os.path.join(destdir, '%s.%s' % (fname, ext))

        fh = open(fullpath, 'wt')

        logging.info('Gen: %s' % fullpath)

        if namespace not in self._gened_files.keys():
            self._gened_files[namespace] = []

        self._gened_files[namespace].append(Generator.GeneratedFile(fname, ext, destdir, namespace, cls))

        return fh


    def gened_file_close(self, fh):
        if fh:
            fh.close()


    def get_option(self, name: str, must_exist: bool = True, blank_ok: bool = False) -> str:
        """
        Gets an option/setting from the target, first checking the over loads and
        then checking the base objects options.

        :param name: The name of the option to get.
        :param must_exist: If true, raise an error if the option could not be found.
        :param blank_ok: The option is allowed to be blank.
        :return: The option value or an empty string if not found and must_exists is set to False.
        """
        val     = None
        val_fnd = False

        if name in self._options.keys():
            val = self._options.get(name)
            val_fnd = True

        if not val_fnd:
            if must_exist:
                raise Exception('Option [%s] not found.' % name)

            print('WARNING: Option [%s] not found' % name)
            return ''

        if not val:
            val = ''
        else:
            val = val.strip()

        if val == '':
            if not blank_ok:
                raise Exception('Option [%s] found, but is blank.' % name)

        return val


    def _pref_suf_name(self, key: str, name: str) -> str:
        val = self.get_option(key, blank_ok = True)

        if val == '':
            print('%s: WARNING, could not find prefix/suffix option [%s] for [%s]' % (self.name(), key, name))
            return ''

        ps = val.split('|')

        if len(ps) != 2:
            print('%s: WARNING, prefix/suffix option [%s] for [%s] is not valid, expected "pre|suf" format.' % (
                self.name(), key, name))
            return ''

        return '%s%s%s' % (ps[0], name, ps[1])


    def _get_string_case_method(self, key: str, name: str) -> str:
        if name is None:
            return None

        func = None

        if hasattr(stringcase, '%scase' % name):
            func = getattr(stringcase, '%scase' % name)

        if func is not None and callable(func):
            return func

        caselist = []

        for caseopt in dir(stringcase):
            if caseopt.endswith('case') and not caseopt.startswith('_'):
                caselist.append(caseopt[:-4])

        raise Exception('Case type [%s] not valid for key [%s]. Please select one of the following [%s]' % (
            name, key, ', '.join(caselist)))


    def _object_ident(self, key: str, name: str) -> str:
        ident = self._idents.get(key)

        if ident:
            return ident

        ident = {'mask': None, 'casing' : None }

        if (key.startswith('client.') and key != 'client.') or\
           (key.startswith('server.') and key != 'server.') or\
           (key.startswith('braze.')  and key != 'braze.') or\
           (key.startswith('file.')   and key != 'file.'):
            val = self.get_option(key, must_exist = False, blank_ok = True)

            if val:
                ps = val.split('|')

                if len(ps) != 2:
                    logging.warning('%s: WARNING, prefix/suffix option [%s] for [%s] is not valid.'
                                    ' Expected "pre|suf" format.' % (self.name(), key, name))
                else:
                    ident['mask'] = '%s%%s%s' % (ps[0], ps[1])
            else:
                ident['mask'] = '%s'
        else:
            ident['mask'] = '%s'

        casing = self._options.get('casing')

        if casing is not None and len(casing) != 0:
            if key.startswith('client.') or key.startswith('server.') or key.startswith('braze.'):
                ident['casing'] = self._get_string_case_method('class', casing.get('class'))
            elif key.startswith('member.'):
                ident['casing'] = self._get_string_case_method('member', casing.get('member'))
            elif key.startswith('method.'):
                ident['casing'] = self._get_string_case_method('method', casing.get('method'))
            elif key.startswith('file.'):
                ident['casing'] = self._get_string_case_method('file', casing.get('file'))

        return ident


    def _ident(self, key: str, name: str) -> str:

        ident = self._object_ident(key, name)

        if ident['mask'] is None:
            return name.replace('__', '_')

        if ident['casing'] is None:
            return (ident['mask'] % name).replace('__', '_')

        return (ident['mask'] % ident['casing'](name)).replace('__', '_')


    def _ident_class(self, name: str) -> str:
        return self._ident('client.', name)


    def _ident_method(self, name: str) -> str:
        return self._ident('method.', name)


    def _ident_member(self, name: str) -> str:
        return self._ident('member.', name)


    def _ident_file(self, name: str) -> str:
        return self._ident('file.', name)


    def _namespace(self, spe_sep: str = None, blank_ok: bool = False):
        ns = self.get_option('namespace', blank_ok = blank_ok)

        if ns == '':
            if blank_ok:
                return ''

            return 'NO_NAMESPACE'

        if spe_sep is None:
            return '%s' % ns.strip()

        return ns.strip().replace('.', spe_sep)


    def _resolve_field_dav(self, sobj, field, gen_info: dict):
        """
        Resolves a field dav in various ways. IE making a lookup to a
        table column, for an 'in' check, or converting a string to a date/datetime
        for a min/max check.

        :param sobj: (Struct) The struct object.
        :param field: (Field) The field to resolve.
        :param gen_info: The generation info dict.
        """
        if not field.dav:
            return

        for david in field.dav.keys():
            if david in ['min', 'max']:
                daval = field.dav[david]

                if type(daval) == str:
                    if field.type == 'date':
                        field.dav[david] = datetime.datetime.strptime(daval, '%Y-%m-%d')
                    elif field.type == 'datetime':
                        field.dav[david] = datetime.datetime.strptime(daval, '%Y-%m-%d %H:%M:%S')
                    else:
                        field.dav[david] = datetime.datetime.strptime(daval, '%H:%M:%S')

                continue

            if david in ['in', 'notin']:
                daval = field.dav[david]

                if type(daval) == dict or type(daval) == list:
                    continue

                if type(daval) != str:
                    raise Exception('Type [%s] not expected [davtype:%s, struct:%s, field:%s]!' % (
                        str(type(daval)), david, sobj.name, field.name))

                if daval.startswith('db:'):
                    refCol = daval[3:].split('.')

                    if len(refCol) != 3:
                        raise Exception('DB reference must be in [proj.table.column] format, got [%s]'
                                        ' [davtype:%s, struct:%s, field:%s]!' % (daval, david, sobj.name, field.name))

                    dbProj = gen_info['proj'].db_projs.get(refCol[0])

                    if not dbProj:
                        raise Exception('Project [%s] not found from dav [%s] [davtype:%s, struct:%s, field:%s]!' % (
                            refCol[0], daval, david, sobj.name, field.name))

                    allTables = dbProj.load_tables(refresh=False)
                    tbl       = allTables.get(refCol[1])

                    if not tbl:
                        raise Exception('Table [%s] not found from dav [%s] [davtype:%s, struct:%s, field:%s]!' % (
                            refCol[1], daval, david, sobj.name, field.name))

                    tcol = tbl.get_column(refCol[2])

                    if not tcol:
                        raise Exception('Column [%s] not found on Table [%s] from dav [%s]'
                                        ' [davtype:%s, struct:%s, field:%s]!' % (
                                            refCol[2], refCol[1], daval, david, sobj.name, field.name))

                    if not tcol.couplets:
                        raise Exception('Column [%s] on Table [%s] has no couplets [davtype:%s, struct:%s, field:%s]!' % (
                            refCol[2], refCol[1], david, sobj.name, field.name))

                    if tcol.type != field.type:
                        raise Exception('Column [%s.%s] type [%s] does not match field type [%s]'
                                        ' [davtype:%s, struct:%s, field:%s]!' % (
                                            refCol[2], refCol[1], tcol.type, field.type, david, sobj.name, field.name))

                    field.dav[david] = tcol.couplets
                    continue

                couplets = gen_info['proj'].couplets

                if daval not in couplets:
                    raise Exception('Couplet not found in project - [ %s:%s ] from [struct:%s, field:%s]!' % (
                        david, daval, sobj.name, field.name))

                field.dav[david] = couplets[daval].couplet
