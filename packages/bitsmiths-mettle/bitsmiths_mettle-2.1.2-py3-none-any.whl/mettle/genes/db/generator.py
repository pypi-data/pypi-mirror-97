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
import logging
import stringcase

from .table import Table


class Generator:
    """
    The base generator class.
    """

    TABLE            = 1
    DAO              = 2
    EXCEPTION_OBJECT = ''

    class FieldMap:
        def __init__(self,
                     name: str,
                     length: int = None,
                     type_flag: str = '',
                     methodpre: str = ' ',
                     def_value: str = ''):
            self.name      = name
            self.length    = length
            self.type_flag  = type_flag
            self.methodpre = methodpre
            self.def_value  = def_value

    class GeneratedFile:
        def __init__(self, fname: str, ext: str, path: str, namespace: str, cls: str = None):
            self.fname     = fname
            self.ext       = ext
            self.path      = path
            self.namespace = namespace
            self.cls       = cls


    def __init__(self, extensions: list):
        self.enabled            = False
        self.targ_type          = ''
        self.namespace          = ''
        self._async_on          = False
        self._options           = {}
        self._dest_dir_standard = ''
        self._dest_dir_async    = None
        self._extensions        = extensions
        self._gened_files       = {}
        self._idents            = {}

        self._table_id     = ''
        self._table_class  = ''

        self._field_map = {
            'int8'        : None,
            'int16'       : None,
            'int32'       : None,
            'int64'       : None,
            'seq32'       : None,
            'seq64'       : None,
            'string'      : None,
            'date'        : None,
            'time'        : None,
            'datetime'    : None,
            'timestamp'   : None,
            'double'      : None,
            'dynamic'     : None,
            'this'        : None,
            'dbrec'       : None,
        }

        self._davMap = {
            'min'   : 'Min',
            'max'   : 'Max',
            'null'  : 'NotNull',
            'regex' : 'Regex',
            'func'  : 'Func',
            'in'    : 'In',
            'notin' : 'NotIn',
        }


    def name(self) -> str:
        return 'Base Generator'


    def init(self,
             enabled: bool,
             opts: dict,
             dest_gen_standard: str = None,
             dest_gen_async: str = None):
        self.enabled = enabled

        if dest_gen_standard is not None:
            self._dest_dir_standard = dest_gen_standard.replace('/', '|').replace('\\', '|')

        if dest_gen_async is not None:
            self._dest_dir_async = dest_gen_async.replace('/', '|').replace('\\', '|')

        for key, val in opts.items():
            if val is None:
                self._options[key] = ''
            elif type(val) == dict:
                if not self._options.get(key):
                    self._options[key] = {}

                for subkey, subval in val.items():
                    self._options[key][subkey] = subval
            else:
                self._options[key] = val



    def dest_dir(self, sep: str = None) -> str:
        if self.async_on() and self.dest_dir_async():
            return self.dest_dir_async(sep)

        return self.dest_dir_standard(sep)


    def dest_dir_standard(self, sep: str = None) -> str:
        if sep:
            return self._dest_dir_standard.replace('|', sep)

        return self._dest_dir_standard


    def dest_dir_async(self, sep: str = None) -> str:
        if sep:
            return self._dest_dir_async.replace('|', sep)

        return self._dest_dir_async


    def standard_enabled(self) -> bool:
        if self._options.get('standard'):
            if not self._options['standard'].get('enabled'):
                return False

            return True

        if not self._options.get('async'):
            return True

        return False


    def async_enabled(self) -> bool:
        if not self._options.get('async') or not self._options['async'].get('enabled'):
            return False

        return True


    def async_on(self) -> bool:
        return self._async_on


    def async_toggle(self, val: bool):
        self._async_on = val


    def return_struct_name(self, table: str, qry: str, struct_type: str):
        # Virtual method to a struct name
        sname = '%s%s' % (table, qry)
        key   = ''

        if struct_type == 'table':
            key = 'class.table'
        elif struct_type == 'key':
            sname = sname + 'Key'
            key   = 'class.table'
        elif struct_type == 'in':
            key   = 'class.qryin'
        elif struct_type == 'out':
            key   = 'class.qryout'
        else:
            raise Exception('StructType expected (table/key/in/out) and got (%s)' % struct_type)

        return self._ident(key, sname)


    def return_struct_path(self, table: str, qry: str, struct_type: str, incl_fname: bool = False):
        # Virtual method to a struct full path.
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

        if self.namespace is None:
            self.namespace = self._namespace()

        if incl_fname:
            return '%s.tables.%s' % (self.namespace, self._ident(key, sname))

        return '%s.tables' % (self.namespace)


    def _couplet_name(self, cname):
        res  = ''

        for x in cname:
            if x.isdigit() or x.isalpha():
                res += x
            else:
                res += '_'

        return '%s%s' % (res[0].capitalize(), res[1:])


    def _init_code_options(self, extra_opts: dict = None):
        std_options = {
            'class.dao'    : None,
            'class.table'  : None,
            'class.qryin'  : None,
            'class.qryout' : None,
            'dir.tables'   : 'tables',
            'dir.dao'      : 'dao',
            'namespace'    : None,
            'db.schema'    : None,
            'async'        : None,
        }

        for key, val in std_options.items():
            x = self._options.get(key)

            if not x:
                self._options[key] = val

        if extra_opts:
            for key, val in extra_opts.items():
                x = self._options.get(key)

                if not x:
                    self._options[key] = val


    def _init_casing(self, casing: dict):
        cdict = self._options.get('casing')

        if not cdict:
            cdict = {}

        for key, val in casing.items():
            if val is not None:
                cdict[key] = val

        self._options['casing'] = cdict


    def initialize_generation(self, gen_info: dict):
        self._gened_files.clear()
        self._idents.clear()


    def finalize_generation(self, gen_info: dict):
        pass


    def generate_tables(self, gen_info: dict):
        raise Exception('GenerateTables for [%s] not implemented' % self.name())


    def generate_daos(self, gen_info: dict, target_db: str):
        raise Exception('GenerateDAOs for [%s] not implemented' % self.name())


    def close_daos(self, gen_info: dict):
        pass


    def prepare_dao(self, gen_info: dict):
        pass


    def close_dao(self, gen_info: dict):
        pass


    def prepare_schema(self, gen_info: dict):
        pass


    def close_schema(self, gen_info: dict):
        pass


    def clean(self, gen_info: dict, target_db: str):
        if not self._extensions:
            return

        for ext in self._extensions:
            delfiles = self.filename_and_path(gen_info, '*',  ext, target_db, create_if_missing=False)

            if not delfiles:
                continue

            parts = os.path.split(delfiles)

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



    def _check_for_sequence(self, fields: list) -> bool:
        """
        Checks if any of the field maps are sequence columns.

        :param fields : The list of fields to check.
        :return: True if a sequence was found else False.
        """
        for i in fields:
            if i.type.startswith('seq'):
                return True

        return False


    def _check_for_type(self, fields: list, ftype: str) -> bool:
        """
        Checks if any of the field maps are of the type.

        :param fields: The list of fields to check.
        :param ftype: The file type to check for.
        :return: True if the field type was found else False.
        """
        for i in fields:
            if i.type == ftype:
                return True

        return False


    def proj_relative_path(self, gen_info: dict, pth: str, extra_dir: str = None) -> str:
        nap = gen_info['proj'].project_dir
        res = os.path.join(nap, self.dest_dir(os.path.sep))

        if not extra_dir:
            return res

        return os.path.join(res,
                            extra_dir.lower().replace('\\', os.path.sep).replace('/', os.path.sep).replace('|', os.path.sep))


    def filename_and_path(self, gen_info: dict, name: str, ext: str, extra_dir: str = None, create_if_missing: bool = True):
        destdir = self.proj_relative_path(gen_info, self.dest_dir(os.path.sep), extra_dir)

        if not os.path.exists(destdir):
            if not create_if_missing:
                return None

            logging.info('Creating missing directory [%s]' % destdir)
            os.makedirs(destdir)
        elif not os.path.isdir(destdir):
            raise Exception('Destination dir [%s] - is not a directory' % destdir)

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

        if namespace is None:
            namespace = self._namespace()

        if ext is None:
            ext = self._extensions[0]

        destdir = self.proj_relative_path(gen_info, self.dest_dir(os.path.sep))

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


    def set_overrides(self, base_obj):
        """
        Set the default options from the language parent.  Also set the
        destination directory from the parent.

        :param base_obj: the default (base) target generation object.
        """
        self._dest_dir_standard = base_obj._dest_dir_standard
        self._dest_dir_async    = base_obj._dest_dir_async

        for key, val in base_obj._options.items():
            if val is None:
                continue

            lval = self._options.get(key)

            if lval is None:
                self._options[key] = val
                continue

            if lval is dict and val is dict:
                for skey, sval in val.items():
                    if lval.get(skey) is None:
                        lval[skey] = sval
            else:
                self._options[key] = val


    def _table_name(self, gen_info: dict):
        schema = self.get_option('db.schema', blank_ok = True)

        if schema == '':
            return gen_info['table'].name

        return '%s.%s' % (schema, gen_info['table'].name)


    def get_dao_dir_name(self) -> str:
        """
        Gets the dao directory name, and applies the async namespace ident if there is one.
        """
        dname  = self.get_option('dir.dao')
        idname = 'ns.%s' % str(self.async_on())
        ident  = self._idents.get(idname)

        if not ident:
            val = None

            if self.async_on():
                if self._options['async'].get('ns.dao'):
                    val = self._options['async'].get('ns.dao')
            else:
                if self._options.get('standard') and self._options['standard'].get('ns.dao'):
                    val = self._options['standard'].get('ns.dao')

            ident = {'mask': None, 'casing' : None }

            if val:

                ps = val.split('|')

                if len(ps) != 2:
                    logging.warning('WARNING, prefix/suffix option [ns.dao] is not valid, expected "pre|suf" format.')
                else:
                    ident['mask'] = '%s%%s%s' % (ps[0], ps[1])
            else:
                ident['mask'] = '%s'

            self._idents[idname] = ident

        return ident['mask'] % dname


    def get_option(self,
                   name        : str,
                   must_exist  : bool = True,
                   blank_ok    : bool = False,
                   from_async  : bool = False) -> str:
        """
        Gets an option/setting from the target, first checking the over loads and
        then checking the base objects options.

        :param name: The name of the option to get.
        :param must_exist: If true, raise an error if the option could not be found.
        :param blank_ok: The option is allowed to be blank.
        :param from_async: Check the async options
        :return: The option value or an empty string if not found and must_exists is set to False.
        """
        val = None
        fnd = False

        if from_async:
            if not self.async_enabled():
                raise Exception('Async not enabled')

            if name in self._options['async'].keys():
                val = self._options['async'].get(name)
                fnd = True
        else:
            if name in self._options.keys():
                val = self._options.get(name)
                fnd = True

        if not fnd:
            if must_exist:
                raise Exception('Option [%s] not found.' % name)

            print('WARNING: Option [%s] not found' % name)
            return ''

        if val is None:
            if blank_ok:
                return ''

        if type(val) == str:
            val = val.strip()

            if not val:
                if not blank_ok:
                    raise Exception('Option [%s] found, but is blank.' % name)

        return val


    def _namespace(self, spe_sep: str = None, blank_ok: bool = True):
        ns = self.get_option('namespace', blank_ok = blank_ok)

        if ns == '':
            if blank_ok:
                return ''

            return 'NO_NAMESPACE'

        if not spe_sep:
            return '%s' % ns.strip()

        return ns.strip().replace('.', spe_sep)


    def _pref_suf_name(self, key, name):
        val = self.get_option(key, blank_ok = True)

        if not val:
            return ''

        ps = val.split('|')

        if len(ps) != 2:
            logging.warning('%s: WARNING, prefix/suffix option [%s] for [%s] is not valid, expected "pre|suf" format.' % (
                self.name, key, name))
            return ''

        return '%s%s%s' % (ps[0], name, ps[1])


    def _get_string_case_method(self, key, name):
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


    def _object_ident(self, key: str, name: str):
        ident = self._idents.get(key)

        if ident:
            return ident

        ident = {'mask': None, 'casing' : None }

        if (key.startswith('class.') and key != 'class.') or\
           (key.startswith('file.') and key != 'file.'):
            val = self.get_option(key, must_exist = False, blank_ok = True)

            if val:
                ps = val.split('|')

                if len(ps) != 2:
                    logging.warning('%s: WARNING, prefix/suffix option [%s] for [%s] is not valid,'
                                    ' expected "pre|suf" format.' % (self.name, key, name))
                else:
                    ident['mask'] = '%s%%s%s' % (ps[0], ps[1])
            else:
                ident['mask'] = '%s'
        else:
            ident['mask'] = '%s'

        casing = self._options.get('casing') or {}

        if casing is not None and len(casing) != 0:
            if key.startswith('class.'):
                ident['casing'] = self._get_string_case_method('class', casing.get('class'))
            elif key.startswith('member.'):
                ident['casing'] = self._get_string_case_method('member', casing.get('member'))
            elif key.startswith('method.'):
                ident['casing'] = self._get_string_case_method('method', casing.get('method'))
            elif key.startswith('file.'):
                ident['casing'] = self._get_string_case_method('file', casing.get('file'))

        self._idents[key] = ident

        return ident


    def _ident(self, key: str, name: str) -> str:

        ident = self._object_ident(key, name)

        if ident['mask'] is None:
            return name.replace('__', '_')

        if ident['casing'] is None:
            return (ident['mask'] % name).replace('__', '_')

        return (ident['mask'] % ident['casing'](name)).replace('__', '_')


    def _ident_class(self, name) -> str:
        return self._ident('class.', name)


    def _ident_method(self, name) -> str:
        return self._ident('method.', name)


    def _ident_member(self, name) -> str:
        return self._ident('member.', name)


    def _ident_file(self, name) -> str:
        return self._ident('file.', name)


    def _build_standard_procs(self, gen_info: dict):
        flds      = gen_info['table'].primary_key_columns()
        procs     = {}

        if len(flds):
            if gen_info['table'].select_one:
                procs['SelectOne'] = self._procedure_select_one(gen_info)

            if gen_info['table'].lock_one:
                procs['LockOne'] = self._procedure_lock_one(gen_info)

            if gen_info['table'].update:
                procs['Update'] = self._procedure_update(gen_info)

            if gen_info['table'].delete_one:
                procs['DeleteOne'] = self._procedure_delete_one(gen_info)

        if gen_info['table'].insert:
            procs['Insert'] = self._procedure_insert(gen_info)

        if gen_info['table'].delete_all:
            procs['DeleteAll'] = self._procedure_delete_all(gen_info)

        if gen_info['table'].select_all:
            procs['SelectAll'] = self._procedure_select_all(gen_info)

        return procs


    def _procedure_select_one(self, gen_info: dict):
        struct_name     = gen_info['table'].name
        struct_key_name = '%sKey' % gen_info['table'].name

        p = Table.SqlProcedure(gen_info['table'], 'SelectOne')

        for x in gen_info['table'].primary_key_columns():
            p.in_field(x.name, x.type, x.dav)

        for x in gen_info['table'].columns:
            p.out_field(x.name, x.type, x.dav)

        if 'database' in gen_info:
            p.sql[gen_info['database'].dbname] = gen_info['database']._sql_select_one(gen_info)

        setattr(p, 'in_override_name',  struct_key_name)
        setattr(p, 'out_override_name', struct_name)
        p.is_standard = False

        return p

    def _procedure_lock_one(self, gen_info: dict):
        struct_name    = gen_info['table'].name
        struct_key_name = '%sKey' % gen_info['table'].name

        p = Table.SqlProcedure(gen_info['table'], 'LockOne')

        for x in gen_info['table'].primary_key_columns():
            p.in_field(x.name, x.type, x.dav)

        for x in gen_info['table'].columns:
            p.out_field(x.name, x.type, x.dav)

        if 'database' in gen_info:
            p.sql[gen_info['database'].dbname] = gen_info['database']._sql_lock_one(gen_info)

        setattr(p, 'in_override_name',  struct_key_name)
        setattr(p, 'out_override_name', struct_name)
        p.is_standard = False

        return p

    def _procedure_update(self, gen_info: dict):
        struct_name = gen_info['table'].name

        p = Table.SqlProcedure(gen_info['table'], 'Update')

        for x in gen_info['table'].columns:
            p.in_field(x.name, x.type, x.dav)

        if 'database' in gen_info:
            p.sql[gen_info['database'].dbname] = gen_info['database']._sql_update(gen_info)

        setattr(p, 'in_override_name',  struct_name)
        setattr(p, 'out_override_name', struct_name)
        p.is_standard = False

        return p


    def _procedure_delete_one(self, gen_info: dict):
        struct_key_name = '%sKey' % gen_info['table'].name

        p = Table.SqlProcedure(gen_info['table'], 'DeleteOne')

        for x in gen_info['table'].primary_key_columns():
            p.in_field(x.name, x.type, x.dav)

        if 'database' in gen_info:
            p.sql[gen_info['database'].dbname] = gen_info['database']._sql_delete_one(gen_info)

        setattr(p, 'in_override_name', struct_key_name)
        setattr(p, 'out_override_name', '')
        p.is_standard = False

        return p


    def _procedure_insert(self, gen_info: dict):
        struct_name = gen_info['table'].name

        p = Table.SqlProcedure(gen_info['table'], 'Insert')

        for x in gen_info['table'].columns:
            p.in_field(x.name, x.type, x.dav)

        if 'database' in gen_info:
            p.sql[gen_info['database'].dbname] = gen_info['database']._sql_insert(gen_info)

        setattr(p, 'in_override_name', struct_name)
        setattr(p, 'out_override_name', '')
        p.is_standard = False

        return p


    def _procedure_delete_all(self, gen_info: dict):
        p = Table.SqlProcedure(gen_info['table'], 'DeleteAll')

        if 'database' in gen_info:
            p.sql[gen_info['database'].dbname] = gen_info['database']._sql_delete_all(gen_info)

        setattr(p, 'in_override_name', '')
        setattr(p, 'out_override_name', '')
        p.is_standard = False

        return p


    def _procedure_select_all(self, gen_info: dict):
        struct_name = gen_info['table'].name

        p = Table.SqlProcedure(gen_info['table'], 'SelectAll')

        for x in gen_info['table'].columns:
            p.out_field(x.name, x.type, x.dav)

        if 'database' in gen_info:
            p.sql[gen_info['database'].dbname] = gen_info['database']._sql_select_all(gen_info)

        setattr(p, 'in_override_name', '')
        setattr(p, 'out_override_name', struct_name)
        p.is_standard = False

        return p


    def _lookup_columns(self, lookup, src):
        if not lookup or lookup == 'table:this':
            return self._gen_info['table'].columns

        if not lookup.startswith('table:'):
            raise Exception('Column lookup [%s] not expected. source [table:%s, proc:%s]' % (
                str(lookup), self._gen_info['table'].name, src))

        tbl = lookup[6:]
        dot = tbl.find('.')

        if dot != -1:
            tbl = tbl[:dot]

        if tbl not in self._gen_info['all_tables']:
            raise Exception('Table lookup [%s] not found, source [table:%s, proc:%s].' % (
                str(tbl), self._gen_info['table'].name, src))

        return self._gen_info['all_tables'][tbl].columns


    def _lookup_name(self, lookup, src: str = ''):
        if not lookup or lookup == 'table:this':
            return self._table_id

        if not lookup.startswith('table:'):
            raise Exception('Column lookup [%s] not expected. source [table:%s, proc:%s]' % (
                str(lookup), self.gen_info['table'].name, src))

        return lookup[6:]


    def _stored_proc_name(self, proc):
        pts = self._gen_info['database'].spName.split('|')

        if len(pts) != 2:
            logging.warning('%s: WARNING, prefix/suffix option [spName/sp.name] for [database:%s] is not valid,'
                            ' expected "pre|suf" format.' % (self.name, self._gen_info['database'].dbname))
            return ''

        return '%s%s%s%s' % (pts[0], self._gen_info['table'].name, proc.name, pts[1])
