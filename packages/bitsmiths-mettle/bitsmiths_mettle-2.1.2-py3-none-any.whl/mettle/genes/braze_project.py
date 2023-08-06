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

import os
import os.path
import logging

import mettle.genes

from mettle.genes.project import Project
from mettle.genes         import common


class BrazeProject(Project):
    """
    The mettle braze project object.
    """
    ARRAY  = True
    NORMAL = False

    IN     = 'i'
    OUT    = 'o'
    REF    = 'io'

    SIG_MODE_STRICT = 'strict'
    SIG_MODE_HASHED = 'hashed'
    SIG_MODE_NAMED  = 'named'

    class Field:
        def __init__(self,
                     name        : str,
                     datatype    : str,
                     length      : int,
                     io          : str,
                     is_array    : bool,
                     brazestruct : str,
                     dbstruct    : str,
                     descr       : str,
                     dav         : dict = None):
            self.name         = name
            self.type         = datatype
            self.length       = length
            self.io           = io
            self.is_array     = is_array
            self.brazestruct  = brazestruct
            self.dbstruct     = dbstruct
            self.descr        = descr
            self.dav          = dav


    class DBStruct:
        def __init__(self, proj: str, table: str, query: str, struct_type: str):
            self.proj        = proj
            self.table       = table
            self.query       = query
            self.struct_type = struct_type  # table, key, in, out
            self.targ_obj    = None         # gets set for generation


        def struct_name(self) -> str:
            return self.targ_obj.return_struct_name(self.table, self.query, self.struct_type)


        def struct_path(self, incl_filename: bool = False) -> str:
            return self.targ_obj.return_struct_path(self.table, self.query, self.struct_type, incl_filename)



    class BrazeCouplet:
        def __init__(self, name: str, ctype: str, couplet: dict):
            self.name    = name
            self.ctype   = ctype
            self.couplet = couplet

        def couplet_name(self) -> str:
            return self.name


    class BrazeStruct():
        def __init__(self, name: str, fields: list, meta: dict = None):
            self.name   = name
            self.fields = fields
            self.meta   = meta


        def struct_name(self) -> str:
            return self.name


        def get_descr(self) -> str:
            if self.meta:
                return self.meta.get('descr')

            return None


    class RemoteCall():
        """
        Defines a remote call (RPC) in the braze.
        """
        def __init__(self,
                     name    : str,
                     fields  : list,
                     returns : 'BrazeProject.Field',
                     auth    : str = None,
                     meta    : dict = None):
            """
            Constructor.

            :param name: Name of the rpc call.
            :param fields: List of Fileds the call takes as arguements.
            :param returns: The return type of the call.
            :param auth: Optionally give an authenticator name to be used by the server.
            :param meta: Optionally provide additional meta data to the call.
            """
            self.name       = name
            self.fields     = fields
            self.returns    = returns
            self.auth       = auth
            self.meta       = meta
            self.has_input  = False
            self.has_output = False
            self.signature  = None

        def get_descr(self) -> str:
            if self.meta:
                return self.meta.get('descr')

            return None


    def __init__(self, proj_path: str, name: str, version: str, sig_mode: str = 'strict'):
        """
        Constructor
        """
        Project.__init__(self, proj_path, name, version)

        if sig_mode != self.SIG_MODE_STRICT and\
           sig_mode != self.SIG_MODE_HASHED and\
           sig_mode != self.SIG_MODE_NAMED:
            raise Exception('Signature mode [%s] not expected.' % sig_mode)

        self._sig_mode      = sig_mode
        self.db_projs      = {}
        self.couplets      = {}
        self.structs       = {}
        self.calls         = []
        self.call_names    = []
        self.struct_order  = []


    def initialize(self):
        """
        Initialize is use be user project to initialize the braze project.
        """
        logging.info('Initializing project [%s]' % self.name)

        if self.version != self.VERSION:
            raise Exception('Project version %f is not the same as Generator version %f' % (self.version, self.VERSION))

        self._load_generators()


    def _validate_project(self):
        """
        Validate a project is empty or has invalid database projects.
        """
        logging.info('Validating Project...')

        if len(self.generators) == 0:
            raise Exception('No code generators have been initialized for project [%s]!' % self.name)

        for x, y in self.db_projs.items():
            pth = os.path.join(self.project_dir, y)

            if not os.path.exists(pth):
                raise Exception('Path [%s] for Database Project [%s] not found!' % (pth, x))


    def _load_generators(self):
        """
        Loads all the code generators.
        """
        logging.info('Loading braze code generators')
        self.generators = {}

        import mettle.genes.braze

        for gcls in mettle.genes.braze.code_generators:
            gobj = gcls()
            self.generators[gobj.name()] = gobj


    def db_project(self, name: str, proj_path: str):
        """
        Set a database project.

        :param name: Name/alias of the project.
        :param proj_path: Full path to the database mettle project file.
        """
        if name in self.db_projs.keys():
            raise Exception('Databaes project [%s] has already been defined in braze project [%s]' % (name, self.name))

        self.db_projs[name] = proj_path.replace('/', os.path.sep)


    def couplet(self, name: str, data_type: str, couplet: dict):
        if name in self.couplets:
            raise Exception('Couplet [%s] has already been defined in braze project [%s]' % (name, self.name))

        self.couplets[name] = BrazeProject.BrazeCouplet(name, data_type, couplet)


    def struct(self, name: str, fields: list, meta: dict = None):
        if name in self.struct_order:
            raise Exception('Struct [%s] has already been defined in braze project [%s]' % (name, self.name))

        if not fields:
            raise Exception('Struct [%s] has no fields, braze project [%s]' % (name, self.name))

        self.struct_order.append(name)
        self.structs[name] = BrazeProject.BrazeStruct(name,
                                                      self._init_fields_from_dicts(fields,
                                                                                   'struct',
                                                                                   name),
                                                      meta)


    def remote_call(self,
                    name     : str,
                    returns  : tuple = None,
                    args_in  : list = None,
                    args_ref : list = None,
                    args_out : list = None,
                    auth     : str = None,
                    meta     : dict = None):
        """
        Defines a remote call for a braze struct.

        :param name: The remote call name.
        :param returns: If call returns something, the data type tuple.
        :param args_in: Define input arguements with a list type of data types.
        :param args_ref: Define reference arguements with a list type of data types.
        :param args_out: Define output arguements with a list type of data types.
        :param auth: Give the authenticator name/method for this call.
        :param meta: Optionally pass in an aditional meta data.
        """
        if name in self.call_names:
            raise Exception('Remote call [%s] has already been defined in braze project [%s]' % (name, self.name))

        self.call_names.append(name)

        ret = None

        if returns:
            ret = self._init_fields_from_dicts([returns], 'return', name)[0]

        self.calls.append(BrazeProject.RemoteCall(
            name,
            self._init_fields_from_dicts(args_in,  'rpc', name, self.IN)
            + self._init_fields_from_dicts(args_ref, 'rpc', name, self.REF)    # noqa
            + self._init_fields_from_dicts(args_out, 'rpc', name, self.OUT),   # noqa
            ret,
            auth,
            meta))


    def generate(self, clean: bool = False, for_async: bool = False):
        if for_async:
            # TODO build braze async code generation
            return

        from mettle.genes import service as genes_service

        self._validate_project()

        logging.info('Generate - Started (%s)' % self.name)

        for x in self.db_projs.keys():
            pth              = os.path.join(self.project_dir, self.db_projs[x])
            logging.info('  loading db project (%s) - path: %s' % (x, pth))
            self.db_projs[x] = genes_service.mettle_obj_load(pth, 'Mettle.DB')

        gen_info               = {}
        gen_info['version']    = str(self.VERSION)
        gen_info['proj']       = self
        gen_info['clean']      = clean
        gen_info['server_sig'] = self._generate_signatures(self.name)

        for g, gobj in sorted(self.generators.items()):
            if not gobj.enabled:
                logging.info('  generator (%s) not enabled' % gobj.name())
                continue

            logging.info('  generating (%s)...' % gobj.name())

            gen_info['db_structs'] = self._init_db_structs(gobj.name())

            gobj.initialize_generation(gen_info)

            gobj.generate_structs(gen_info)

            gobj.generate_client(gen_info)

            gobj.generate_server(gen_info)

            gobj.finalize_generation(gen_info)

        logging.info('Generate - Done(%s)' % self.name)


    def _generate_signatures(self, server_name: str) -> "int|str":
        """
        Genertes a server signature.

        :param server_name: The server name.
        :return: Signature int value for strict, str for other
        """
        if self._sig_mode == self.SIG_MODE_STRICT:
            logging.info('  generating strict signatures...')

            server_sig = 0
            add        = True
            cnt        = 1
            sig_hist   = []

            for call in self.calls:
                cval = self._gen_call_signature(cnt, call, sig_hist)

                if add:
                    server_sig += cval
                    server_sig -= cnt
                    add = False
                else:
                    server_sig -= cval
                    server_sig += cnt
                    add = True

                cnt += 13

            if server_sig < 0:
                server_sig = 0 - server_sig

            return str(server_sig)

        if self._sig_mode == self.SIG_MODE_HASHED:
            logging.info('  generating hashed signatures...')

            for call in self.calls:
                self._gen_call_signature(0, call, None)

            return common.hash_str(server_name)

        if self._sig_mode == self.SIG_MODE_NAMED:
            logging.info('  generating named signatures...')

            for call in self.calls:
                self._gen_call_signature(0, call, None)

            return server_name

        raise Exception('Signature mode [%s] not expected' % self._sig_mode)


    def _gen_call_signature(self, cnt: int, call: object, sig_hist: list) -> "int|str":
        """
        Generate a call signature.

        :param cnt: The call count.
        :param call: The call object.
        :param sig_hist: The history of signatures.
        :return: The integer value of the signature, or the string value if mode is not strict.
        """
        if self._sig_mode == self.SIG_MODE_STRICT:
            sig  = 0
            prev = 7

            for c in call.name:
                sig  += ord(c) % prev
                prev  = ord(c) + cnt
                cnt  += 1

            sig *= prev
            tmp  = sig

            for f in call.fields:
                for c in f.name :
                    sig += ord(c) % prev
                    prev = ord(c) + cnt
                    cnt += 1

                for c in f.type:
                    sig += ord(c) % prev
                    prev = ord(c) + cnt
                    cnt += 1

            sig += tmp
            sig *= prev

            cval = int(str(sig)[:7])

            while cval in sig_hist:
                cval += 3

                if cval < 0:
                    cval = 0 - cval

            sig_hist.append(cval)

            call.signature = str(cval)

            return cval


        if self._sig_mode == self.SIG_MODE_HASHED:
            call.signature = common.hash_str(call.name)
            return call.signature

        if self._sig_mode == self.SIG_MODE_NAMED:
            call.signature = call.name
            return call.signature

        raise Exception('Signature mode [%s] not expected' % self._sig_mode)


    def _init_db_structs(self, targ: str):
        lst = []

        for sname, struct in self.structs.items():
            for f in struct.fields:
                if f.type == 'dbrec':
                    self._init_db_struct_field(targ, "Braze Struct", f.name, f.dbstruct)
                    lst.append(f.dbstruct)

        for call in self.calls:
            if call.returns and call.returns.type == 'dbrec':
                self._init_db_struct_field(targ, "Remote Call", 'returns', call.returns.dbstruct)
                lst.append(call.returns.dbstruct)

            for f in call.fields:
                if f.type == 'dbrec':
                    self._init_db_struct_field(targ, "Remote Call", f.name, f.dbstruct)
                    lst.append(f.dbstruct)

        logging.info('  initialized [%d] database structs' % len(lst))

        return lst


    def _init_db_struct_field(self, targ: str, src: str, name: str, dbstruct: str):
        if dbstruct.proj not in self.db_projs.keys():
            raise Exception('Database project [%s] not found for [source:%s, field:%s]'  % (dbstruct.proj, src, name))

        dbproj = self.db_projs[dbstruct.proj]

        dbstruct.targ_obj = dbproj.generators[targ]


    def _init_fields_from_dicts(self, in_dicts: list, src: str, src_name: str, in_ref_out: str = None) -> list:
        """
        Reads the data type tuple.

        The tuple should be in format (name, type, {validations})

        :param in_dicts: List of dicts.
        :param src: The source of the tuple.
        :param src_name: Source name.
        :param in_ref_out: Is the data type in/ref/out type for rpc calls.
        :returns: The list of created fields.
        """
        if not in_dicts:
            if src == 'return':
                return [None]

            if src == 'rpc':
                return []

            if src == 'struct':
                raise Exception('Struct [%s] cannot have no fields!' % (src_name))

        idx         = 0
        field_names = []
        res         = []

        for x in in_dicts:
            idx         += 1
            brazestruct  = None
            dbstruct     = None
            name         = None
            data_type    = None
            data_len     = 0
            descr        = None
            is_array     = False
            pth          = '%s:%s:' % (src, src_name)

            if in_ref_out:
                pth += '%s:' % in_ref_out

            name      = common.read_dict(x, 'name',  str, pth)
            data_type = common.read_dict(x, 'type',  str, pth)
            descr     = common.read_dict(x, 'descr', str, pth,  optional = True)
            dav       = common.read_dict(x, 'dav',   dict, pth, optional = True)

            field_names.append(name)

            if data_type.endswith('[]'):
                is_array = True
                data_type = data_type[:-2]

            if data_type.startswith('braze:'):
                brazestruct = data_type[6:]

                if brazestruct not in self.struct_order:
                    raise Exception('Struct [name:%s, field:%d, brazeStruct:%s] struct name not found.' % (
                        src_name, idx, brazestruct))

                brazestruct = self.structs[brazestruct]
                data_type    = 'brazerec'

            elif data_type.startswith('db:'):
                parts = data_type[3:].split('.')

                if len(parts) != 2 and len(parts) != 4:
                    raise Exception('Struct [name:%s, field:%d, data_type:%s] should be split in 2 or 4 parts eg:'
                                    ' "db:Proj.Table" or "db:Proj.Table.Query.out"' % (src_name, idx, data_type))

                if len(parts) == 2:
                    dbstruct = BrazeProject.DBStruct(parts[0], parts[1], '', 'table')
                else:
                    if parts[3] not in ['table', 'key', 'in', 'out']:
                        raise Exception('Struct [name:%s, field:%d, data_type:%s] type value should end in'
                                        ' [table, key, in, out]"' % (src_name, idx, data_type))

                    if len(parts[2]) < 1 and parts[3] in ['in', 'out']:
                        raise Exception('Struct [name:%s, field:%d, data_type:%s] query structs should end in [in, out]"' % (
                            src_name, idx, data_type))

                    dbstruct = BrazeProject.DBStruct(parts[0], parts[1], parts[2], parts[3])

                data_type = 'dbrec'

            if data_type not in mettle.genes.DataTypes:
                raise Exception('Struct [name:%s, field:%d, data_type:%s] is not a valid data type - see (%s)' % (
                    src_name, idx, data_type, str(mettle.genes.DataTypes)))

            if data_type in ['dynamic', 'tableRec']:
                raise Exception('Struct [name:%s, field:%d, data_type:%s] is reserved for database queries only!' % (
                    src_name, idx, data_type))

            if dav:
                for david, daval in dav.items():
                    dotplus  = david.find('+')
                    dotcol   = david.find(':')

                    if dotplus != -1 and dotcol != -1:
                        raise Exception('Dav type [%s] cannot contain both [. and +], struct'
                                        ' [name:%s, field:%d] is reserved for database queries only!' % (
                                            david, src_name, idx))

                    if (dotplus != -1 or dotcol != -1) and data_type not in ['brazerec', 'dbrec']:
                        raise Exception('Dav type [%s] cannot "subfield" for non braze/db struct types, struct'
                                        ' [name:%s, field:%d] is reserved for database queries only!' % (
                                            david, src_name, idx))

                    if dotplus != -1:
                        david = david[dotplus + 1:]
                    elif dotcol != -1:
                        david = david[dotcol + 1:]

                    if david not in ['cmds', 'in', 'notin', 'null', 'min', 'max', 'regex', 'func']:
                        raise Exception('Dav type [%s] not expected, struct [name:%s, field:%d]!' % (
                            david, src_name, idx))

                    if david == 'cmds' and daval not in ['clear', 'key', 'insert']:
                        raise Exception('Dav command [%s] not expected, struct [name:%s, field:%d, dav:%s]!' % (
                            str(daval), src_name, idx, david))

            res.append(BrazeProject.Field(name,
                                          data_type,
                                          data_len,
                                          in_ref_out,
                                          is_array,
                                          brazestruct,
                                          dbstruct,
                                          descr,
                                          dav))


        return res
