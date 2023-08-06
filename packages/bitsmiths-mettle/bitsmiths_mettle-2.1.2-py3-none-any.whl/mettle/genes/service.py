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

from mettle.genes import common


def _exec_mettle_obj(obj_file: str, type_name: str = None) -> object:
    """
    Executes a mettle object file.

    :param obj_file: The full path to the object file.
    :param type_name: The type expected.
    :return: The loaded mettle object.
    """
    if not os.path.exists(obj_file):
        raise Exception('Object file [%s] not found!' % obj_file)

    fh   = open(obj_file, 'rt')
    data = fh.read()
    loc  = {}
    fh.close()

    try:
        exec(data, None, loc)
    except Exception as e:
        logging.error("Error parsing object file [%s] - Error: %s" % (obj_file, str(e)))
        raise

    if '_MettleObject' not in loc:
        raise Exception('Error loading object file [%s] - No object of type "%s" not declared' % (
            obj_file, '_MettleObject'))

    mo = loc['_MettleObject']()

    logging.debug('Mettle object [%s] loaded (name:%s/version:%s/type:%s)' % (
        (obj_file, mo._Name(), mo._Version(), mo._MettleFileType())))

    if type_name is not None and mo._MettleFileType() != type_name:
        raise Exception('Exepcted to load mettle file type [%s] but instead loaded type [%s]' % (
            type_name, mo._MettleFileType()))

    try:
        obj = mo._Object(obj_file)
    except Exception as e:
        logging.error("Error creating mettle object [%s] - Error: %s" % (obj_file, str(e)))
        raise

    return obj


def _validate_mdo_header(mdo: dict, obj_file: str, type_name: str = None):
    """
    Validate that the mdo (mettle dictionary object) header is valid.

    :param mdo: Mettle dictionary object.
    :param obj_file: The file name.
    :param type_name: The expected type, if none the not validated.
    """
    if mdo is None or type(mdo) != dict:
        raise Exception("Object file [%s] did not translate into a valid dictionary." % obj_file)

    ft   = common.read_dict(mdo, 'file-type', str)
    ver  = common.read_dict(mdo, 'version',   float)
    name = common.read_dict(mdo, 'name',      str)

    if type_name and ft != type_name:
        raise Exception('File type not valid, expected [%s] and got [%s] for object file [%s]' % (type_name, ft, obj_file))

    from mettle.genes.project   import Project

    if ver != Project.VERSION:
        raise Exception('Version not valid, expected [%.2f] and got [%.2f] for object file [%s]' % (
            Project.VERSION, ver, obj_file))

    if ft not in ('Mettle.DB.Table', 'Mettle.DB', 'Mettle.Braze', 'Mettle.Mk'):
        raise Exception('File type [%s] is not expected, for object file [%s].' % (ft, obj_file))

    if name == '':
        raise Exception('Name cannot be left blank, for object file [%s].' % (obj_file))


def _read_davs(flds: dict) -> dict:
    """
    Reads all the dav items from a dictionary.

    :param flds: The dictionary to read.
    :return: The result davs
    """
    if len(flds) <= 2:
        return None

    res = {}

    for ky, vl in flds.items():
        if ky not in ('name', 'type', 'descr'):
            res[ky] = vl

    if len(res) == 0:
        return None

    if None in res.keys():
        res['null'] = res[None]
        del res[None]

    return res


def _mettle_table(mdo: dict, obj_file: str) -> 'mettle.genes.db.Table':
    """
    Return a mettle table object from the mdo.

    :param mdo: Mettle dictionary object.
    :param obj_file: The source object file.
    :return: The mettle table object.
    """
    from mettle.genes.db.table import Table

    res       = Table(mdo['name'], mdo['version'])
    std_procs = common.read_dict(mdo, 'standard-procs', dict, '', optional=True)
    dicts     = common.read_dict(mdo, 'dicts',          dict, '', optional=True)
    columns   = common.read_dict(mdo, 'columns',        list, '', optional=False)
    tbl_pk    = common.read_dict(mdo, 'primary-key',    None, '', optional=True)
    tbl_fks   = common.read_dict(mdo, 'foreign-keys',   list, '', optional=True)
    tbl_uks   = common.read_dict(mdo, 'unique-keys',    list, '', optional=True)
    tbl_idx   = common.read_dict(mdo, 'indexes',        list, '', optional=True)
    procs     = common.read_dict(mdo, 'procs',          list, '', optional=True)

    if std_procs:
        par = 'standard-procs:'
        res.select_one  = common.read_dict(std_procs, 'select_one', bool, par)
        res.lock_one    = common.read_dict(std_procs, 'lock_one',   bool, par)
        res.select_all  = common.read_dict(std_procs, 'select_all', bool, par)
        res.update      = common.read_dict(std_procs, 'update',     bool, par)
        res.insert      = common.read_dict(std_procs, 'insert',     bool, par)
        res.delete_one  = common.read_dict(std_procs, 'delete_one', bool, par)
        res.delete_all  = common.read_dict(std_procs, 'delete_all', bool, par)

    if not columns:
        raise Exception("A table requires at least one column, src:%s" % obj_file)

    idx = 0

    for col in columns:
        par     = 'columns[%d]:' % idx
        col_name = common.read_dict(col, 'name', str, parent=par)
        col_type = common.read_dict(col, 'type', str,  req_vals=mettle.genes.DataTypes, parent=par)
        col_null = common.read_dict(col, 'null', bool, optional=True, parent=par)
        col_none = common.read_dict(col, None,   bool, optional=True, parent=par)
        col_max  = common.read_dict(col, 'max',  int,  optional=True, parent=par)
        col_min  = common.read_dict(col, 'min',  int,  optional=True, parent=par)
        col_in   = common.read_dict(col, 'in',   None, optional=True, parent=par)

        col_opts = {}

        if col_null:
            col_opts['null'] = col_null
        elif col_none:
            col_opts['null'] = col_none

        if col_max:
            col_opts['max'] = col_max

        if col_min:
            col_opts['min'] = col_min

        if col_in:
            if type(col_in) == list:
                col_opts['in'] = col_in
            elif type(col_in) == dict:
                col_opts['in'] = col_in
            elif type(col_in) == str:
                d = dicts.get(col_in)

                if d is None:
                    raise Exception('Dictionary [%s] not found for "in" [column:%s, idx:%d, src:%s]' % (
                        col_in, col_name, idx, obj_file))

                col_opts['in'] = d
            else:
                raise Exception('Invalid type [%s] for "in", expected dict, list or str [column:%s, idx:%d, src:%s]' % (
                    str(type(col_in)), col_name, idx, obj_file))

        res.column(col_name, col_type, col_opts)
        idx += 1

    if tbl_pk:
        if type(tbl_pk) == str:
            res.primary_key(tbl_pk)
        elif type(tbl_pk) == list:
            res.primary_key(*tbl_pk)
        else:
            raise Exception('Invalid type [%s] for "primary-key", exepcted str or list of strings [src:%s]' % (
                str(type(tbl_pk)), obj_file))

    if tbl_fks:
        idx = 0
        for fk in tbl_fks:
            par     = 'foreign-keys[%d]:' % idx
            fk_name  = common.read_dict(fk, 'name',    str,  parent=par)
            fk_table = common.read_dict(fk, 'table',   str,  parent=par)
            fk_cols  = common.read_dict(fk, 'columns', list, parent=par)

            res.foreign_key(fk_name, fk_table, *fk_cols)
            idx += 1

    if tbl_uks:
        idx = 0
        for uk in tbl_uks:
            par     = 'unique-keys[%d]:' % idx
            uk_name  = common.read_dict(uk, 'name',    str,  parent=par)
            uk_cols  = common.read_dict(uk, 'columns', list, parent=par)

            res.unique_key(uk_name, *uk_cols)
            idx += 1

    if tbl_idx:
        idx = 0
        for ix in tbl_idx:
            par     = 'indexes[%d]:' % idx
            ix_name  = common.read_dict(ix, 'name',    str,  parent=par)
            ix_cols  = common.read_dict(ix, 'columns', list, parent=par)

            res.index(ix_name, *ix_cols)
            idx += 1

    if procs:
        idx = 0

        for proc in procs:
            par       = 'procs[%d]:' % idx
            proc_name = common.read_dict(proc, 'name', str, parent=par)
            dao_mode  = common.read_dict(proc, 'dao-mode', str, par, ['inline', 'stored-proc'], True)
            par       = 'procs[%d, %s]:' % (idx, proc_name)
            proc_inp  = common.read_dict(proc, 'input',  list, parent=par, optional=True)
            proc_out  = common.read_dict(proc, 'output', list, parent=par, optional=True)
            pc_sql    = common.read_dict(proc, 'sql',    list, parent=par, optional=False)

            p = res.sql_proc(proc_name, '' if dao_mode is None else dao_mode)

            if proc_inp:
                sub_idx = 0

                for inf in proc_inp:
                    sub_par  = '%sinput[%d]:' % (par, sub_idx)
                    inp_name = common.read_dict(inf, 'name', str,  parent=sub_par)
                    inp_type = common.read_dict(inf, 'type', str,  parent=sub_par)
                    inp_dav  = common.read_dict(inf, 'dav',  dict, parent=sub_par, optional=True)

                    if inp_dav:
                        dav_in = inp_dav.get('in')

                        if type(dav_in) == str:
                            d = dicts.get(col_in)

                            if d is None:
                                raise Exception('Dictionary [%s] not found for "in" [proc:%s, input:%s, idx:%d, src:%s]' % (
                                    col_in, proc_name, inp_name, sub_idx, obj_file))

                            inf['in'] = d.keys()

                        if None in inp_dav.keys():
                            inp_dav['null'] = inp_dav[None]
                            del inp_dav[None]

                    p.in_field(inp_name, inp_type, inp_dav)

                    sub_idx += 1

            if proc_out:
                sub_idx = 0

                for outf in proc_out:
                    sub_par  = '%soutput[%d]:' % (par, sub_idx)
                    out_name = common.read_dict(outf, 'name', str,  parent=sub_par, optional=True)
                    out_type = common.read_dict(outf, 'type', str,  parent=sub_par)
                    out_dav  = common.read_dict(outf, 'dav',  dict, parent=sub_par, optional=True)

                    if out_dav:
                        dav_in = out_dav.get('in')

                        if type(dav_in) == str:
                            d = dicts.get(col_in)

                            if d is None:
                                raise Exception('Dictionary [%s] not found for "in" [proc:%s, input:%s, idx:%d, src:%s]' % (
                                    col_in, proc_name, out_name, sub_idx, obj_file))

                            outf['in'] = d.keys()

                        if None in out_dav.keys():
                            out_dav['null'] = out_dav[None]
                            del out_dav[None]

                    p.out_field(out_name, out_type, out_dav)


            sub_idx = 0

            for dbqry in pc_sql:
                sub_par = '%ssql[%d]:' % (par, sub_idx)

                db  = common.read_dict(dbqry, 'db', str)
                qry = common.read_dict(dbqry, 'query', str).strip()

                p.sql[db] = qry
                sub_idx += 1

            idx += 1


    return res


def _mettle_db_proj(mdo: dict, obj_file: str) -> 'mettle.genes.DatabseProject':
    """
    Return a mettle database project object from the mdo.

    :param mdo: Mettle dictionary object.
    :param obj_file: The source object file.
    :return: The mettle database project object.
    """
    res       = mettle.genes.DatabaseProject(obj_file, mdo['name'], mdo['version'])
    tbl_list  = common.read_dict(mdo, 'table-list',           list)
    lan_gens  = common.read_dict(mdo, 'language-generators',  list)
    db_gens   = common.read_dict(mdo, 'database-generators',  list)
    sql_gen   = None

    if not tbl_list:
        raise Exception("No tables have been defined for the database proejct, src:%s" % obj_file)

    for tbl in tbl_list:
        res.table_list.append(tbl)

    idx = 0

    for lg in lan_gens:
        par      = 'language-generators[%d]:' % idx
        targ     = common.read_dict(lg, 'target', str, par)

        if targ not in res.generators.keys():
            raise Exception("Language generator not expected. [target:%s, idx:%d]", (targ, idx))

        par             = 'language-generators[%d, %s]:' % (idx, targ)
        enabled         = common.read_dict(lg, 'enabled',   bool, par)
        dest_path       = common.read_dict(lg, 'dest-path', str, par)
        options         = common.read_dict(lg, 'options',   dict, par, optional=True)
        dest_path_async = None

        if lg.get('async') and lg.get('dest-path'):
            dest_path_async = lg['async']['dest-path']

        res.generators[targ].init(enabled, options, dest_path, dest_path_async)

        if targ == 'Sql':
            sql_gen = res.generators[targ]

        idx += 1

    idx = 0

    if not sql_gen or not sql_gen.enabled:
        db_gens.clear()
        return

    for dl in db_gens:
        par      = 'database-generators[%d]:' % idx
        targ     = common.read_dict(dl, 'target', str, par)

        if targ not in res.databases.keys():
            raise Exception("Database generator not expected. [target:%s, idx:%d]", (targ, idx))

        par      = 'database-generators[%d, %s]:' % (idx, targ)
        enabled  = common.read_dict(dl, 'enabled',   bool, par)
        dao_mode = common.read_dict(dl, 'dao-mode',  str,  par, ['inline', 'stored-proc'], True)
        sp_name  = common.read_dict(dl, 'sp.name',   str,  par, optional=True)
        generate = common.read_dict(dl, 'generate',  dict, par)

        if dao_mode is None:
            dao_mode = 'inline'

        dbx          = res.databases[targ]
        dbx.enabled  = enabled
        dbx.dao_mode = dao_mode

        if sp_name != '':
            dbx.sp_name = sp_name

        if not enabled:
            continue

        for lang, opts in generate.items():
            if lang not in dbx.generators.keys():
                raise Exception("Language not expected for database generator. [language:%s target:%s, idx:%d]", (
                    lang, targ, idx))

            if not opts:
                continue

            if not opts.get('enabled'):
                continue

            del opts['enabled']

            opts['dao_mode'] = dao_mode

            dbx.generators[lang].init(True,
                                      opts,
                                      sql_gen.dest_dir_standard(),
                                      sql_gen.dest_dir_async())

        idx += 1

    return res


def _mettle_braze_proj(mdo: dict, obj_file: str) -> 'mettle.genes.BrazeProject':
    """
    Return a mettle braze project object from the mdo.

    :param mdo: Mettle dictionary object.
    :param obj_file: The source object file.
    :return: The mettle braze project object.
    """
    sigMode = mdo.get('sig-mode') or 'strict'

    res      = mettle.genes.BrazeProject(obj_file, mdo['name'], mdo['version'], sigMode)
    lan_gens = common.read_dict(mdo, 'language-generators',  list)
    db_projs = common.read_dict(mdo, 'db-projects',          dict, optional=True)
    dicts    = common.read_dict(mdo, 'dicts',                dict, optional=True)
    couplets = common.read_dict(mdo, 'couplets',             list, optional=True)
    structs  = common.read_dict(mdo, 'structs',              list, optional=True)
    rpcs     = common.read_dict(mdo, 'remote-calls',         list)

    idx = 0

    for lg in lan_gens:
        par      = 'language-generators[%d]' % idx
        targ     = common.read_dict(lg, 'target', str, par)

        if targ not in res.generators.keys():
            raise Exception("Language generator not expected. [target:%s, idx:%d]", (targ, idx))

        par       = 'language-generators[%d, %s]:' % (idx, targ)
        enabled   = common.read_dict(lg, 'enabled',   bool, par)
        dest_path = common.read_dict(lg, 'dest-path', str, par)
        options   = common.read_dict(lg, 'options',   dict, par, optional=True)

        res.generators[targ].init(enabled, dest_path, options)
        idx += 1

    if dicts is None:
        dicts = {}

    if db_projs:
        for dbname, dbpath in db_projs.items():
            res.db_project(dbname, dbpath)

    if couplets:
        idx = 0

        for coupl in couplets:
            par   = 'couplets[%d]:' % idx
            cname = common.read_dict(coupl, 'name', str, par)
            ctype = common.read_dict(coupl, 'type', str, par, req_vals=mettle.genes.DataTypes)
            cvals = common.read_dict(coupl, 'vals', None, par)

            if type(cvals) == dict:
                pass
            elif type(cvals) == str:
                if cvals not in dicts.keys():
                    raise Exception("Dictionary [%d] not found, couplet [idx:%d, name:%s]" % (cvals, idx, cname))

                cvals = dicts[cvals]
            else:
                raise Exception("Vals type [%s] expected to be a dictionary or string lookup to dicts. [idx:%d, name:%s]" % (
                    str(type(cvals)),  idx, cname))

            res.couplet(cname, ctype, cvals)
            idx += 1

    if structs:
        idx = 0

        for st in structs:
            par  = 'structs[%d]:' % idx
            name = common.read_dict(st, 'name', str, par)
            par  = 'structs[%d, %s]:' % (idx, name)
            flds = common.read_dict(st, 'fields', list, par)
            meta = common.read_dict(st, 'meta', dict, par, optional = True)

            sub_idx  = 0
            fldList = []

            for fld in flds:
                sub_par  = '%sfields[%d]:' % (par, sub_idx)
                fname   = common.read_dict(fld, 'name',  str, sub_par)
                ftype   = common.read_dict(fld, 'type',  str, sub_par)
                fdescr  = common.read_dict(fld, 'descr', str, sub_par, optional = True)
                fdavs   = _read_davs(fld)

                fldList.append({ 'name': fname, 'type': ftype, 'descr': fdescr, 'dav': fdavs })
                sub_idx += 1

            res.struct(name, fldList, meta)
            idx += 1

    idx = 0

    for rpc in rpcs:
        par     = 'remote-calls[%d]' % idx
        name    = common.read_dict(rpc, 'name', str, par)
        par     = 'remote-calls[%d, %s]:' % (idx, name)
        returns = common.read_dict(rpc, 'returns', None, par, optional=True)
        meta    = common.read_dict(rpc, 'meta', dict, par, optional=True)

        if returns:
            if type(returns) == str:
                returns = { 'name' : '', 'type': returns }
            elif type(returns) == dict:
                rpar = '%s:returns:' % par
                ftype   = common.read_dict(returns, 'type',  str, rpar)
                descr   = common.read_dict(returns, 'descr', str, rpar, optional = True)
                returns = { 'name' : '', 'type': ftype, 'descr': descr }


        args_in   = []
        args_ref  = []
        args_out  = []

        for argt in ('args-in', 'args-ref', 'args-out'):
            argo = common.read_dict(rpc, argt, list, par, optional=True)

            if not argo:
                continue

            sub_idx  = 0

            for fld in argo:
                sub_par  = '%s%s[%d]:' % (par, argt, sub_idx)
                fname   = common.read_dict(fld, 'name', str, sub_par)
                ftype   = common.read_dict(fld, 'type', str, sub_par)
                fdescr  = common.read_dict(fld, 'descr', str, sub_par, optional = True)
                fdavs   = _read_davs(fld)

                if argt == 'args-in':
                    args_in.append( { 'name': fname, 'type': ftype, 'descr': fdescr, 'dav': fdavs })
                elif argt == 'args-ref':
                    args_ref.append( { 'name': fname, 'type': ftype, 'descr': fdescr, 'dav': fdavs })
                else:
                    args_out.append( { 'name': fname, 'type': ftype, 'descr': fdescr })

                sub_idx += 1

        auth = common.read_dict(rpc, 'auth', str, optional = True)

        res.remote_call(name, returns, args_in, args_ref, args_out, auth, meta)
        idx += 1

    return res


def _mettle_mk_proj(mdo: dict, obj_file: str) -> 'mettle.genes.MkProject':
    """
    Return a mettle makefile project object from the mdo.

    :param mdo: Mettle dictionary object.
    :param obj_file: The source object file.
    :return: The mettle makefile project object.
    """
    project_root = common.read_dict(mdo, 'project-root',     str)
    project_ver  = common.read_dict(mdo, 'project-version',  dict)
    gen_order    = common.read_dict(mdo, 'generation-order', list)
    res          = mettle.genes.MkProject(obj_file, mdo['name'], mdo['version'], project_root, project_ver, gen_order)

    if not os.path.exists(res.proj_root):
        raise Exception('Project root directory [%s] not found!' % (res.proj_root))

    idx = 0

    mk_gens = common.read_dict(mdo, 'generators',       list)

    for mg in mk_gens:
        par      = 'generators[%d]:' % idx
        targ     = common.read_dict(mg, 'target', str, par)

        if targ not in res.generators.keys():
            raise Exception("Makefile generator not expected. [target:%s, idx:%d]", (targ, idx))

        par        = 'generators[%d, %s]:' % (idx, targ)
        enabled    = common.read_dict(mg, 'enabled',   bool, par, optional=True)
        types      = common.read_dict(mg, 'types',     dict, par)
        compilers  = common.read_dict(mg, 'compilers', dict, par, optional=True)
        targets    = common.read_dict(mg, 'targets',   list, par)
        extern     = common.read_dict(mg, 'extern',    str,  par, optional = True)

        res.generators[targ].init(res, enabled, types, compilers, targets, extern)

    return res


def _mettle_obj_from(obj_file: str, type_name: str = None, ext: str = None) -> object:
    """
    Converts a file to a mettle object, currently either a yaml or json file.

    :param obj_file: The full path to the object file.
    :param type_name: The type expected.
    :param ext: The extension type.
    :return: The loaded mettle object.
    """
    if not ext:
        ext = os.path.splitext(obj_file)[1].lower()

    if ext == '.yml' or ext == '.yaml':
        import yaml

        with open(obj_file, 'rt') as fh:
            mdo = yaml.safe_load(fh.read())

    elif ext == 'json':
        import json

        with open(obj_file, 'rt') as fh:
            mdo = json.loads(fh.read())
    else:
        raise Exception("Object file of type [%s] not supported!" % ext)

    _validate_mdo_header(mdo, obj_file, type_name)

    if mdo['file-type'] == 'Mettle.DB.Table':
        return _mettle_table(mdo, obj_file)

    if mdo['file-type'] == 'Mettle.DB':
        return _mettle_db_proj(mdo, obj_file)

    if mdo['file-type'] == 'Mettle.Braze':
        return _mettle_braze_proj(mdo, obj_file)

    if mdo['file-type'] == 'Mettle.Mk':
        return _mettle_mk_proj(mdo, obj_file)

    raise Exception('File type [%s] not supported at this time.' % mdo['file-type'])


def mettle_obj_load(obj_file: str, req_type: str = None) -> object:
    """
    Load a mettle generation oobject.

    :param obj_file: The full path to the object file.
    :param req_type: Optionally specifiy a required type.
    :return: Mettle object.
    """
    ext = os.path.splitext(obj_file)[1].lower()

    if ext == '.yml' or ext == '.yaml' or ext == '.json':
        proj = _mettle_obj_from(obj_file, req_type, ext)
    else:
        proj = _exec_mettle_obj(obj_file, req_type)

    return proj


def proj_generate(proj_file: str, req_type=None):
    """
    Runs the genrator for the specified project file.

    :param proj_file: The full path to the project file.
    :param req_type: Optionally specifiy a required type.
    """
    proj = mettle_obj_load(proj_file, req_type)

    proj.generate()
    proj.generate(for_async = True)


def proj_clean(proj_file: str, req_type: str = None):
    """
    Runs the clean for the specified project file.

    :param proj_file: The full path to the project file.
    :param req_type: Optionally specifiy a required type.
    """
    proj = mettle_obj_load(proj_file, req_type)

    proj.generate(clean = True)
    proj.generate(clean = True, for_async = True)
