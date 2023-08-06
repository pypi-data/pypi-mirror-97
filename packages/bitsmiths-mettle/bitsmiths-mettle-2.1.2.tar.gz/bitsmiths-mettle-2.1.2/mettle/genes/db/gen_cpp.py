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
import time

from mettle.genes.db.table import Table

from .generator import Generator


class GenCpp(Generator):

    SELECT_LOCK_ARG     = '_lock4update'

    SCHEMA_MAP = {
        'bool'      : 'Bool',
        'int8'      : 'Int8',
        'int16'     : 'Int16',
        'int32'     : 'Int32',
        'int64'     : 'Int64',
        'seq32'     : 'Seq32',
        'seq64'     : 'Seq64',
        'char'      : 'Char',
        'string'    : 'String',
        'date'      : 'Date',
        'time'      : 'Time',
        'datetime'  : 'DateTime',
        'timestamp' : 'TimeStamp',
        'double'    : 'Double',
        'memblock'  : 'MemoryBlock',
        'uuid'      : 'UUID',
        'json'      : 'String',
    }


    def __init__(self):
        Generator.__init__(self, ['h', 'cpp'])
        self.targ_type       = 'code'
        self.namespace       = None
        self._mode           = self.TABLE
        self._struct_path    = None
        self.dao_path        = None
        self.dao_header_done = False

        self._field_map['bool']      = Generator.FieldMap('bool',                     type_flag='bool',      methodpre='')
        self._field_map['int8']      = Generator.FieldMap('int8_t',                   type_flag='int',       methodpre='')
        self._field_map['int16']     = Generator.FieldMap('int16_t',                  type_flag='int',       methodpre='')
        self._field_map['int32']     = Generator.FieldMap('int32_t',                  type_flag='int',       methodpre='')
        self._field_map['int64']     = Generator.FieldMap('int64_t',                  type_flag='int',       methodpre='')
        self._field_map['seq32']     = Generator.FieldMap('int32_t',                  type_flag='int',       methodpre='')
        self._field_map['seq64']     = Generator.FieldMap('int64_t',                  type_flag='int',       methodpre='')
        self._field_map['double']    = Generator.FieldMap('double',                   type_flag='double',    methodpre='')
        self._field_map['char']      = Generator.FieldMap('char',                     type_flag='char',      methodpre='')
        self._field_map['string']    = Generator.FieldMap('Mettle::Lib::String',      type_flag='str',       methodpre='&')
        self._field_map['date']      = Generator.FieldMap('Mettle::Lib::Date',        type_flag='date',      methodpre='&')
        self._field_map['time']      = Generator.FieldMap('Mettle::Lib::Time',        type_flag='date',      methodpre='&')
        self._field_map['datetime']  = Generator.FieldMap('Mettle::Lib::DateTime',    type_flag='date',      methodpre='&')
        self._field_map['timestamp'] = Generator.FieldMap('Mettle::Lib::DateTime',    type_flag='date',      methodpre='&')
        self._field_map['memblock']  = Generator.FieldMap('Mettle::Lib::MemoryBlock', type_flag='memblock',  methodpre='&')
        self._field_map['dynamic']   = Generator.FieldMap('Mettle::Lib::String',      type_flag='str',       methodpre='&')
        self._field_map['dbrec']     = Generator.FieldMap('struct',                   type_flag='tableRec',  methodpre='*')
        self._field_map['uuid']      = Generator.FieldMap('Mettle::Lib::Guid',        type_flag='uuid',      methodpre='&')
        self._field_map['json']      = Generator.FieldMap('Mettle::Lib::String',      type_flag='json',      methodpre='&')


        self._init_code_options({ 'includepath.tables': None, 'includepath.dao': None })
        self._init_casing({
            'class'  : 'pascal',
            'method' : 'pascal',
            'member' : 'pascal',
            'file'   :  None,
        })


    def name(self):
        return 'C++'


    def _set_struct_path(self):
        if not self._struct_path:
            return

        self._struct_path = self.get_option('includepath.tables').replace('|', '/').replace('\\', '/')
        self.dao_path     = self.get_option('includepath.dao').replace('|', '/').replace('\\', '/')

        if not self._struct_path.endswith('/'):
            self._struct_path += '/'

        if not self.dao_path.endswith('/'):
            self.dao_path += '/'


    def prepare_dao(self, gen_info):
        self.dao_header_done = False


    def prepare_schema(self, gen_info):
        self._set_struct_path()

        if gen_info['clean']:
            return

        self._shfh          = None
        self._scfh          = None
        self._schema_tables = []

        self._target_db = 'tables'
        self._gen_info  = gen_info

        fname = self._ident_file(gen_info['proj'].name.replace('.', '_'))
        hFile = self.filename_and_path(self._gen_info, '_%s_dbschema' % fname, 'h',   self._target_db)
        cFile = self.filename_and_path(self._gen_info, '_%s_dbschema' % fname, 'cpp', self._target_db)

        logging.info('Gen: %s' % hFile)
        logging.info('Gen: %s' % cFile)

        self._hFile = os.path.split(hFile)[1]
        self._cFile = os.path.split(cFile)[1]

        self._shfh  = open(hFile, 'wt')
        self._scfh  = open(cFile, 'wt')

        self._add_headers(self._shfh, self._scfh)

        self._shfh.write('#ifndef __GENERATED_METTLE_DB_%s_DBSCHEMA_H_\n' % (
            self._gen_info['proj'].name.upper().replace('.', '_')))
        self._shfh.write('#define __GENERATED_METTLE_DB_%s_DBSCHEMA_H_\n\n' % (
            self._gen_info['proj'].name.upper().replace('.', '_')))

        self._shfh.write('namespace Mettle { namespace DB { \n\n')
        self._shfh.write('   class DBSchema;\n\n')
        self._shfh.write('}}\n\n')

        self._scfh.write('#include "%s%s.h"\n\n' % (self._struct_path, '_%s_dbschema' % fname))
        self._scfh.write('#include "mettle/db/dbschema.h"\n\n')


    def close_dao(self, gen_info):
        self.dao_header_done = True


    def close_schema(self, gen_info):
        if gen_info['clean']:
            return

        for s in self._schema_tables:
            x = s.split('|')
            self._scfh.write('#include "%s"\n' % x[0])

        self._scfh.write('\n')
        self._gen_begin_namespaces(self._shfh, self._scfh)

        self._shfh.write('void loadDBSchema(Mettle::DB::DBSchema* schema);\n\n')

        self._scfh.write('void loadDBSchema(Mettle::DB::DBSchema* schema)\n')
        self._scfh.write('{\n')
        self._scfh.write('   schema->_name = "%s";\n' % self._gen_info['proj'].name)
        self._scfh.write('   schema->_tables.purge();\n\n')


        for s in self._schema_tables:
            x = s.split('|')
            self._scfh.write('   %s::_loadSchema(schema);\n' % x[1])

        self._scfh.write('}\n\n')

        self._gen_end_namespaces(self._shfh, self._scfh)
        self._gen_trailers(self._shfh)

        self._shfh.close()
        self._scfh.close()

        del self._shfh
        del self._scfh
        del self._schema_tables


    def generate_tables(self, gen_info: dict):
        self._mode     = self.TABLE
        self._target_db = 'tables'
        self._generate(gen_info)


    def generate_daos(self, gen_info: dict, targetDB):
        self._mode     = self.DAO
        self._target_db = targetDB
        self._set_struct_path()
        self._generate(gen_info)


    def _generate(self, gen_info):
        if gen_info['clean']:
            self.clean(gen_info, 'tables')
            self.clean(gen_info, 'dao')
            self.clean(gen_info, 'dao/' + self._target_db)
            return

        self._gen_info = gen_info

        self._initialize()

        self._add_headers(self._hfh, self._cfh)

        self._gen_headers()
        self._gen_begin_namespaces(self._hfh, self._cfh)

        self._gen_table_key_class()
        self._gen_table_class()
        self._gen_table_schema()
        self._gen_dao_class()
        self._gen_standard_procs()
        self._gen_custom_procs()

        self._gen_end_namespaces(self._hfh, self._cfh)
        self._gen_trailers(self._hfh)

        self._destroy()


    def _initialize(self):
        fname = self._ident_file(self._gen_info['table'].name)

        if self._mode == self.TABLE:
            hFile  = self.filename_and_path(self._gen_info, fname, 'h',   self._target_db)
            cFile  = self.filename_and_path(self._gen_info, fname, 'cpp', self._target_db)
        else:
            hFile  = self.filename_and_path(self._gen_info, '%sDAO' % fname,  'h',   'dao')
            cFile  = self.filename_and_path(self._gen_info, '%sDAO' % fname,  'cpp', 'dao/' + self._target_db)

        logging.info('Gen: %s' % hFile)
        logging.info('Gen: %s' % cFile)

        self._hFile = os.path.split(hFile)[1]
        self._cFile = os.path.split(cFile)[1]

        if self._mode != self.DAO or not self.dao_header_done:
            self._hfh = open(hFile, 'wt')
        else:
            self._hfh = None

        self._cfh = open(cFile, 'wt')


    def _destroy(self):
        if self._hfh:
            self._hfh.close()
            del self._hFile
            del self._hfh

        self._cfh.close()
        del self._cFile
        del self._cfh


    def _add_headers(self, hfh, cfh):
        if self._mode == self.TABLE:
            message = '/* This file was generated by mettle.genes.db.GenCpp [ver %s] on %s */\n\n' % (
                self._gen_info['version'], time.asctime())
        else:
            message = '/* This file was generated by mettle.genes.db.GenCpp [ver %s] on %s */\n'\
                      '/* Target Database = %s*/\n\n' % (
                          self._gen_info['version'], time.asctime(), self._gen_info['database'].dbname)

        if hfh:
            hfh.write(message)

        cfh.write(message)


    def _set_short_comment(self, fh, comment: str, space: str = ''):
        fh.write('%s/*-----------------------------------\n' % space)
        fh.write('%s   %s\n' % (space, comment))
        fh.write('%s-----------------------------------*/\n' % space)


    def _set_long_comment(self, fh, comment: str):
        fh.write('/*------------------------------------------------------------------------------\n')
        fh.write('   %s\n' % comment)
        fh.write('------------------------------------------------------------------------------*/\n')


    def return_struct_name(self, table: str, qry: str, struct_type: str):
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

        if not self.namespace:
            self.namespace = '%s::' % self._namespace('::')

        return self.namespace + self._ident(key, sname)


    def _write_field_binding(self, io, rec, fields, isInsert=False):
        fnd = False

        hasSequences = self._check_for_sequence(fields)

        for f in fields:
            if f.type == 'dynamic':
                continue

            if isInsert and hasSequences and self._gen_info['database']._sequence_post_insert() and f.type.startswith('seq'):
                continue

            fnd  = True
            fmap = self._field_map[f.type]

            if fmap.type_flag in ('tableRec'):
                pass
            elif fmap.type_flag in ('str'):
                self._cfh.write('   _dbStmnt->%s->Bind(%s &%s.%s, %d);\n' % (
                    io, '"%s",' % f.name, rec, self._ident_member(f.name), f.length))
            elif fmap.type_flag in ('json'):
                self._cfh.write('   _dbStmnt->%s->BindJson(%s &%s.%s, %d);\n' % (
                    io, '"%s",' % f.name, rec, self._ident_member(f.name), f.length))
            else:
                if f.type.startswith('int') and f.not_null is False:
                    if io == 'in':
                        self._cfh.write('   _dbStmnt->%s->Bind(%s &%s.%s, %s.%s_NULL);\n' % (
                            io, '"%s",' % f.name, rec, self._ident_member(f.name), rec, self._ident_member(f.name)))
                    else:
                        self._cfh.write('   _dbStmnt->%s->Bind(%s &%s.%s, %s.%s_NULL, &%s.%s_NULL);\n' % (
                            io,
                            '"%s",' % f.name,
                            rec,
                            self._ident_member(f.name),
                            rec,
                            self._ident_member(f.name),
                            rec,
                            self._ident_member(f.name)))
                else:
                    self._cfh.write('   _dbStmnt->%s->Bind(%s &%s.%s);\n' % (
                        io, '"%s",' % f.name, rec, self._ident_member(f.name)))

        if fnd:
            self._cfh.write('\n')


    def _write_get_timestamps(self, fields):
        fnd = False

        for f in fields:
            if f.type != 'timestamp':
                continue

            fnd = True

            self._cfh.write('   _dbCon->getTimeStamp(irec.%s);\n' % self._ident_member(f.name))

        if fnd:
            self._cfh.write('\n')


    def _write_get_sequences_post(self, proc):
        for f in proc.in_fields:
            if f.type.startswith('seq'):
                self._cfh.write('   _dbCon->postGetSequence(&irec.%s, sizeof(irec.%s), _dbStmnt, "%s", "%s");\n' % (
                    self._ident_member(f.name), self._ident_member(f.name), self._table_name(self._gen_info), f.name))

        self._cfh.write('\n')


    def _write_get_sequences_pre(self, proc):

        for f in proc.in_fields:
            if f.type.startswith('seq'):
                self._cfh.write('   _dbCon->preGetSequence(&irec.%s, sizeof(irec.%s), _dbStmnt, "%s", "%s");\n' % (
                    f.name, f.name, self._table_name(self._gen_info), f.name))

        self._cfh.write('\n')


    def _write_dynamic_binding(self, proc):
        fnd = False

        for f in proc.in_fields:
            if f.type != 'dynamic':
                continue

            self._cfh.write('   _dbStmnt->sql->dynamic("[%s]", irec.%s);\n' % (f.name, self._ident_member(f.name)))
            fnd = True

        if fnd:
            self._cfh.write('\n')


    def _write_add_sql(self, sql: str, sp: str = ''):
        self._cfh.write('   %s_dbStmnt->sql->add(' % sp)

        spaces  = ''
        newLine = ''

        for s in sql.splitlines() :
            if s.strip() == '':
                continue

            self._cfh.write('%s"%s%s"' % (spaces, newLine, s))

            if not len(spaces):
                spaces  = '\n      '
                newLine = '\\n'

        self._cfh.write(');\n\n')


    def _write_insert_exec(self, cls, irec, proc, iflds):
        self._write_cpp_method('%s& ' % cls, cls, self._ident_method('Exec'), None if not irec else '%s* i=0' % irec)
        self._cfh.write('{\n')

        self._cfh.write('   if (i)\n')
        self._cfh.write('      irec = *i;\n\n')

        self._cfh.write('   %s();\n\n' % self._ident_method('Destroy'))
        self._cfh.write('   _dbStmnt = _dbCon->createStatement("%s%s", 1);\n\n' % (self._gen_info['table'].name, proc.name))

        if self._gen_info['database'].dbname in proc.sql and self._gen_info['database'].dbname != 'std':
            sql = proc.sql[self._gen_info['database'].dbname]
        else:
            sql = proc.sql['std']

        hasSequences = self._check_for_sequence(proc.in_fields)

        if hasSequences:
            if self._gen_info['database']._sequence_pre_insert():
                self._write_get_sequences_pre(proc)

        self._write_add_sql(sql)
        self._write_dynamic_binding(proc)
        self._write_get_timestamps(proc.in_fields)
        self._write_field_binding('in',  'irec', proc.in_fields, True)

        self._cfh.write('   _dbCon->execute(_dbStmnt);\n\n')

        if hasSequences:
            if self._gen_info['database']._sequence_post_insert():
                self._write_get_sequences_post(proc)

        self._cfh.write('   if (i)\n')
        self._cfh.write('      *i = irec;\n\n')
        self._cfh.write('   return *this;\n')
        self._cfh.write('}\n\n')


    def _write_std_exec(self, cls, irec, proc, get_timestamps, iflds, oflds):
        self._write_cpp_method('%s& ' % cls, cls, self._ident_method('Exec'), None if not irec else '%s* i=0' % (irec))
        self._cfh.write('{\n')

        if irec:
            self._cfh.write('   if (i)\n')
            self._cfh.write('      irec = *i;\n\n')

        self._cfh.write('   %s();\n\n' % self._ident_method('Destroy'))
        self._cfh.write('   _dbStmnt = _dbCon->createStatement("%s%s");\n\n' % (self._gen_info['table'].name, proc.name))

        if self._gen_info['database'].dbname in proc.sql:
            sql = proc.sql[self._gen_info['database'].dbname]
        else:
            sql = proc.sql['std']

        self._write_add_sql(sql)

        if proc.name == 'LockOne':
            self._cfh.write('   _dbCon->lock(_dbStmnt);\n\n')

        self._write_dynamic_binding(proc)

        if get_timestamps:
            self._write_get_timestamps(iflds)

        self._write_field_binding('in',  'irec', iflds)
        self._write_field_binding('out', 'orec', oflds)

        self._cfh.write('   _dbCon->execute(_dbStmnt);\n\n')

        if irec and get_timestamps:
            self._cfh.write('   if (i)\n')
            self._cfh.write('      *i = irec;\n\n')

        self._cfh.write('   return *this;\n')
        self._cfh.write('}\n\n')


    def _write_sql_proc_dao(self, proc, proc_ignore_types: list = [], get_timestamps: bool = False, doInsert: bool = False):
        if self._mode != self.DAO:
            return

        cls   = self._ident('class.dao', '%s%s' % (self._gen_info['table'].name, proc.name))
        irec  = None
        orec  = None
        iflds = proc.in_fields
        oflds = proc.out_fields

        if proc.is_standard:
            if len(proc.in_fields):
                if proc.in_fields[0].type == 'dbrec':
                    irec  = self._table_class
                    iflds = self._gen_info['table'].columns
                else:
                    irec = self._ident('class.qryin', '%s%s' % (self._gen_info['table'].name, proc.name))
            if len(proc.out_fields):
                if proc.out_fields[0].type == 'dbrec':
                    orec  = self._table_class
                    oflds = self._gen_info['table'].columns
                else:
                    orec = self._ident('class.qryout', '%s%s' % (self._gen_info['table'].name, proc.name))
        else:
            if len(proc.in_fields):
                irec = proc.in_override_name
            if len(proc.out_fields):
                orec = proc.out_override_name

        self._set_long_comment(self._cfh, cls)

        if self._hfh:
            self._set_short_comment(self._hfh, cls)
            self._hfh.write('class %s\n' % cls)
            self._hfh.write('{\n')
            self._hfh.write('public:\n')

        # DAO::DAO()
        self._write_cpp_method('', cls, cls, 'Mettle::DB::IConnect* dbCon')
        self._cfh.write('{\n')
        self._cfh.write('   _dbCon   = dbCon;\n')
        self._cfh.write('   _dbStmnt = 0;\n')
        self._cfh.write('}\n\n')

        # DAO::~DAO()
        self._write_cpp_method('', cls, '~%s' % cls)
        self._cfh.write('{\n')
        self._cfh.write('   %s();\n' % self._ident_method('Destroy'))
        self._cfh.write('}\n\n')

        # void DAO::destroy()
        self._write_cpp_method('void', cls, self._ident_method('Destroy'), None)
        self._cfh.write('{\n')
        self._cfh.write('   if (_dbStmnt)\n')
        self._cfh.write('   {\n')
        self._cfh.write('      delete _dbStmnt;\n')
        self._cfh.write('      _dbStmnt = 0;\n')
        self._cfh.write('   }\n')
        self._cfh.write('}\n\n')

        # DAO &DAO::Exec(args)
        if irec:
            self._write_cpp_method('%s &' % cls, cls, self._ident_method('Exec'), iflds, ignore_types=proc_ignore_types)

            self._cfh.write('{\n')
            self._write_copy_args('irec.', iflds, '', proc_ignore_types)
            self._cfh.write('\n   return %s();\n' % self._ident_method('Exec'))
            self._cfh.write('}\n\n')

            self._write_cpp_method('%s &' % cls,
                                   cls,
                                   self._ident_method('Exec'),
                                   'const %s& i' % irec,
                                   ignore_types=proc_ignore_types)

            self._cfh.write('{\n')
            self._cfh.write('   irec = i;\n\n')
            self._cfh.write('   return %s();\n' % self._ident_method('Exec'))
            self._cfh.write('}\n\n')

        # void DAO::Exec()
        if doInsert:
            self._write_insert_exec(cls, irec, proc, iflds)
        else:
            self._write_std_exec(cls, irec, proc, get_timestamps, iflds, oflds)

        # bool DAO::Fetch()
        if orec and oflds:
            self._write_cpp_method('bool', cls, self._ident_method('Fetch'), None)
            self._cfh.write('{\n')
            self._cfh.write('   return _dbCon->fetch(_dbStmnt);\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('unsigned int',
                                   cls,
                                   self._ident_method('FetchAll'),
                                   '%s::List& outList, const bool clearList=true' % orec)
            self._cfh.write('{\n')
            self._cfh.write('   if (clearList)\n')
            self._cfh.write('      outList.clear();\n\n')
            self._cfh.write('   while (%s())\n' % self._ident_method('Fetch'))
            self._cfh.write('      outList.append(new %s(orec));\n\n' % orec)
            self._cfh.write('   return outList.count();\n')
            self._cfh.write('}\n\n')

        # Members
        if self._hfh:
            if irec:
                self._hfh.write('   %s irec;\n' % irec)
            if orec:
                self._hfh.write('   %s orec;\n' % orec)
            self._hfh.write('\nprivate:\n\n')
            self._hfh.write('   Mettle::DB::IConnect* _dbCon;\n')
            self._hfh.write('   Mettle::DB::Statement* _dbStmnt;\n')
            self._hfh.write('\n};\n\n')


    def _write_assing_couplets(self):
        if self._mode != self.TABLE:
            return

        fnd = False

        for col in self._gen_info['table'].columns:
            if not col.couplets:
                continue

            cname = '%s::%s' % (self._table_class, self._ident('class.couplet', col.name))

            if not fnd:
                fnd = True
                self._set_short_comment(self._cfh, 'Couplets')

            fmap    = self._field_map[col.type]
            keyType = ''
            keyMask = ''
            const   = 'const '
            valMask = '%s %s' % ('const char*', ' %s%s = "%s";\n')
            cmpMask = 'key == %s'
            keyList = []
            valList = []

            if fmap.type_flag in ('str', 'json'):
                keyType = 'const char*'
                cmpMask = 'strcmp(key, %s) == 0'
                keyMask = '%s %s' % ('const char*', ' %s%s = "%s";\n')
                const   = ''
            elif fmap.type_flag == 'char':
                keyType = 'char'
                keyMask = '%s %s' % ('char', ' %s%s = \'%s\';\n')
            else:
                keyType = fmap.name
                keyMask = '%s %s' % (fmap.name, ' %s%s = %s;\n')

            for key, val in col.couplets.items():
                kname = self._ident_member('Key%s' % self._couplet_name(val))
                self._cfh.write(keyMask % ('%s::' % (cname), kname, str(key)))
                keyList.append('%s::%s' % (cname, kname))

            self._cfh.write('\n')

            for key, val in col.couplets.items():
                vname = self._ident_member('Value%s' % self._couplet_name(val))
                self._cfh.write(valMask % ('%s::' % (cname), vname, str(val)))
                valList.append('%s::%s' % (cname, vname))

            self._cfh.write('\n')
            self._cfh.write('%s %s%s = %s;\n' % ('unsigned int',
                                                 '%s::' % (cname),
                                                 self._ident_member('Count'),
                                                 str(len(col.couplets))))
            self._cfh.write('%s %s%s = %s;\n' % (keyType,
                                                 '%s::' % (cname),
                                                 self._ident_member('Keys[]'),
                                                 '{%s}' % ', '.join(keyList)))
            self._cfh.write('%s %s%s = %s;\n' % ('const char*',
                                                 '%s::' % (cname),
                                                 self._ident_member('Values[]'),
                                                 '{%s}' % ', '.join(valList)))

            self._cfh.write('\n')
            self._cfh.write('const char* %s::%s(%s%s key) noexcept\n' % (
                cname, self._ident_method('GetValue'), const, keyType))
            self._cfh.write('{\n')

            for i in range(len(col.couplets)):
                self._cfh.write('   if (')
                self._cfh.write(cmpMask % keyList[i])
                self._cfh.write(')\n')
                self._cfh.write('      return %s;\n\n' % valList[i])

            self._cfh.write('   return 0;\n')
            self._cfh.write('}\n')

        if fnd:
            self._cfh.write('\n')


    def _write_schema(self, cls):
        tbl = self._gen_info['table']

        self._hfh.write('   static void _loadSchema(Mettle::DB::DBSchema *schema);\n\n')

        self._cfh.write('void %s::_loadSchema(Mettle::DB::DBSchema *schema)\n' % cls)
        self._cfh.write('{\n')
        self._cfh.write('   Mettle::DB::DBSchema::Table* t;\n')

        if len(tbl.foreign_keys) > 0:
            self._cfh.write('   Mettle::DB::DBSchema::ForeignKey* fk;\n')

        if len(tbl.unique_keys) > 0:
            self._cfh.write('   Mettle::DB::DBSchema::UniqueKey* uk;\n')

        if len(tbl.indexes):
            self._cfh.write('   Mettle::DB::DBSchema::Index* idx;\n')

        self._cfh.write('\n   t = schema->_tables.append(new Mettle::DB::DBSchema::Table(schema, "%s"));\n' % (
            tbl.name.lower()))

        cnt = 1

        for col in self._gen_info['table'].columns:
            self._cfh.write('   t->_columns.append(new Mettle::DB::DBSchema::Column'
                            '(%d, "%s", Mettle::DB::DBSchema::e%s, %d, %s));\n' % (cnt,
                                                                                   col.name.lower(),
                                                                                   self.SCHEMA_MAP[col.type],
                                                                                   col.length,
                                                                                   'false' if col.not_null else 'true'))
            cnt += 1

        if len(tbl.primary_keys):
            self._cfh.write('   t->_primaryKey._table = t;\n')

            for pkCol in tbl.primary_keys:
                self._cfh.write('   t->_primaryKey._columns.append(new Mettle::Lib::String("%s"));\n' % (
                    tbl.columns[pkCol.index].name.lower()))

        cnt = 1
        for fk in tbl.foreign_keys:
            self._cfh.write('   fk = t->.foreign_keys.append(new Mettle::DB::DBSchema::ForeignKey'
                            '(t, "%s_FK%.2d", "%s"));\n' % (tbl.name, cnt, fk.ref_table.lower()))

            for field in fk.columns:
                self._cfh.write('   fk->_columns.append(new Mettle::Lib::String("%s"));\n' % (
                    tbl.columns[field].name.lower()))

            cnt += 1

        cnt = 1
        for uk in tbl.unique_keys:
            self._cfh.write('   uk = t->.unique_keys.append(new Mettle::DB::DBSchema::UniqueKey(t, "%s_UK%.2d"));\n' % (
                tbl.name, cnt))

            for field in uk.columns:
                self._cfh.write('   uk->_columns.append(new Mettle::Lib::String("%s"));\n' % (
                    tbl.columns[field].name.lower()))

            cnt += 1

        cnt = 1
        for idx in tbl.indexes:
            self._cfh.write('   idx = t->_indexes.append(new Mettle::DB::DBSchema::Index(t, "%s_IX%.2d"));\n' % (
                tbl.name, cnt))

            for field in idx.columns:
                self._cfh.write('   idx->_columns.append(new Mettle::Lib::String("%s"));\n' % (
                    tbl.columns[field].name.lower()))

            cnt += 1

        self._cfh.write('}\n\n')


    def _write_data_class(self, cls: str, columns: list, main_class: bool = False, key_class: bool = False):
        if self._mode != self.TABLE:
            return

        self._set_short_comment(self._hfh, cls)
        self._set_long_comment(self._cfh, cls)

        inherits = ['Mettle::IO::ISerializable()']
        tbl      = self._gen_info['table']

        self._hfh.write('class %s : public Mettle::IO::ISerializable' % cls)

        if main_class and len(tbl.primary_keys) > 0:
            self._hfh.write(', public Mettle::DB::IPrimaryKey')

        if key_class:
            self._hfh.write(', public Mettle::Lib::IComparable')

        self._hfh.write('\n{\n')
        self._hfh.write('public:\n')

        # Table::Table()
        self._write_cpp_method('', cls, cls, None, inherits)
        self._cfh.write('{\n')
        self._cfh.write('   clear();\n')
        self._cfh.write('}\n\n')

        # Table::Table(columns)
        self._write_cpp_method('', cls, cls, columns, inherits, ignore_types=['timestamp'])
        self._cfh.write('{\n')
        self._write_copy_args('this->', columns, '', ['timestamp'])
        self._cfh.write('}\n\n')

        # Table::Table(copy constrctor)
        self._write_cpp_method('', cls, cls, 'const %s& _copyObj' % cls, inherits)
        self._cfh.write('{\n')
        self._write_copy_args('', columns, '_copyObj.')
        self._cfh.write('}\n\n')

        # Table::~Table()
        self._write_cpp_method('', cls, '~%s' % cls, virtual=True)
        self._cfh.write('{\n')
        self._cfh.write('}\n\n')

        # void Table::Clear(void)
        self._write_cpp_method('void', cls, 'clear')
        self._cfh.write('{\n')
        self._write_clear_fields(columns)
        self._cfh.write('}\n\n')

        if key_class:
            self._write_cpp_method('int', cls, '_compare', 'const void* _obj /* %s */' % cls, const=True)
            self._cfh.write('{\n')
            if len(columns) > 1:
                self._cfh.write('   int rc;\n\n')

            for c in columns[0:-1]:
                self._cfh.write('   if ((rc = %s) != 0)\n' % self._get_compare(cls, c))
                self._cfh.write('      return rc;\n\n')

            self._cfh.write('   return %s;\n' % self._get_compare(cls, columns[-1]))
            self._cfh.write('}\n\n')

        # const char* Table::_Name()
        self._write_cpp_method('const char*', cls, '_name', None, const=True)
        self._cfh.write('{\n')

        if main_class:
            self._cfh.write('   return "%s";\n' % tbl.name)
        elif key_class:
            self._cfh.write('   return "%sKey";\n' % tbl.name)
        else:
            self._cfh.write('   return "%s";\n' % cls)

        self._cfh.write('}\n\n')

        # unsigned int Table::_serialize()
        self._write_cpp_method('unsigned int',
                               cls,
                               '_serialize',
                               'Mettle::IO::IWriter* _w, const char* _defName = 0',
                               const=True)
        self._cfh.write('{\n')
        self._cfh.write('   unsigned int _sizeWritten = 0;\n\n')
        self._cfh.write('   _sizeWritten += _w->writeStart(_defName ? _defName : _name());\n')
        self._write_encapsualted_fields(columns,
                                        '   _sizeWritten += %s._serialize(_w);\n',
                                        '   _sizeWritten += _w->write("%s", %s);\n')
        self._cfh.write('   _sizeWritten += _w->writeEnd(_defName ? _defName : _name());\n')
        self._cfh.write('\n   return _sizeWritten;\n')
        self._cfh.write('}\n\n')

        # unsigned int Table::_deserialize()
        self._write_cpp_method('unsigned int',
                               cls,
                               '_deserialize',
                               'Mettle::IO::IReader* _r, const char* _defName = 0')
        self._cfh.write('{\n')
        self._cfh.write('   unsigned int _sizeRead = 0;\n\n')
        self._cfh.write('   _sizeRead += _r->readStart(_defName ? _defName : _name());\n')
        self._write_encapsualted_fields(columns,
                                        '   _sizeRead += %s._deserialize(_r);',
                                        '   _sizeRead += _r->read("%s", %s);\n')
        self._cfh.write('   _sizeRead += _r->readEnd(_defName ? _defName : _name());\n')
        self._cfh.write('\n   return _sizeRead;\n')
        self._cfh.write('}\n\n')

        if main_class and tbl.primary_keys:
            self._write_cpp_method('void', cls, '_writePK', 'void* _key /*%sKey*/' % cls, const=True)
            self._cfh.write('{\n')
            self._cfh.write('   _writeKey(*(%sKey*) _key);\n' % cls)
            self._cfh.write('}\n\n')

            self._write_cpp_method('void', cls, '_readPK', 'const void* _key /*%sKey*/' % cls)
            self._cfh.write('{\n')
            self._cfh.write('   _readKey(*(%sKey*) _key);\n' % cls)
            self._cfh.write('}\n\n')

            self._write_cpp_method('void', cls, '_serializeKey', 'Mettle::IO::IWriter* _w', const=True)
            self._cfh.write('{\n')
            self._cfh.write('   %sKey _key;\n\n' % cls)
            self._cfh.write('   _writeKey(_key);\n')
            self._cfh.write('   _key._serialize(_w);\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('void', cls, '_deserializeKey', 'Mettle::IO::IReader* _r')
            self._cfh.write('{\n')
            self._cfh.write('   %sKey _key;\n\n' % cls)
            self._cfh.write('   _key._deserialize(_r);\n')
            self._cfh.write('   _readKey(_key);\n')
            self._cfh.write('}\n\n')


        if main_class:
            self._write_table_class_specific(cls, columns)

        # List class
        self._hfh.write('   DECLARE_SAFE_CLASS(%s);\n\n' % cls)
        self._hfh.write('   class List : public Mettle::Lib::Collection<%s>, public Mettle::IO::ISerializable\n' % cls)
        self._hfh.write('   {\n')
        self._hfh.write('   public:\n')

        self._write_cpp_method('const char*', '%s::List' % cls, '_name', const=True, spaceOffset='   ')
        self._cfh.write('{\n')

        if main_class:
            self._cfh.write('   return "%s.List";\n' % tbl.name)
        elif key_class:
            self._cfh.write('   return "%sKey.List";\n' % tbl.name)
        else:
            self._cfh.write('   return "%s.List";\n' % cls)

        self._cfh.write('}\n\n')

        self._write_cpp_method('unsigned int',
                               '%s::List' % cls,
                               '_serialize',
                               'Mettle::IO::IWriter* _w, const char* _defName=0',
                               const=True,
                               spaceOffset='   ')
        self._cfh.write('{\n')
        self._cfh.write('   unsigned int _sizeWritten = 0;\n')
        self._cfh.write('   uint32_t     _listSize    = (uint32_t) count();\n')
        self._cfh.write('   uint32_t     _idx;\n\n')
        self._cfh.write('   _sizeWritten += _w->writeStart(_defName ? _defName : _name());\n')
        self._cfh.write('   _sizeWritten += _w->write("ListSize", _listSize);\n\n')
        self._cfh.write('   for (_idx = 0; _idx < _listSize; _idx++)\n')
        self._cfh.write('      _sizeWritten += _list[_idx]->_serialize(_w);\n\n')
        self._cfh.write('   _sizeWritten += _w->writeEnd(_defName ? _defName : _name());\n')
        self._cfh.write('\n   return _sizeWritten;\n')
        self._cfh.write('}\n\n')

        self._write_cpp_method('unsigned int',
                               '%s::List' % cls,
                               '_deserialize',
                               'Mettle::IO::IReader* _r, const char* _defName=0',
                               const=False,
                               spaceOffset='   ')
        self._cfh.write('{\n')
        self._cfh.write('   unsigned int _sizeRead = 0;\n')
        self._cfh.write('   uint32_t     _listSize = 0;\n')
        self._cfh.write('   uint32_t     _idx;\n\n')
        self._cfh.write('   _sizeRead += _r->readStart(_defName ? _defName : _name());\n')
        self._cfh.write('   _sizeRead += _r->read("ListSize", _listSize);\n\n')
        self._cfh.write('   allocate(_listSize);\n\n')
        self._cfh.write('   for (_idx = 0; _idx < _listSize; _idx++)\n')
        self._cfh.write('      _sizeRead += _list[_idx]->_deserialize(_r);\n\n')
        self._cfh.write('   _sizeRead += _r->readEnd(_defName ? _defName : _name());\n')
        self._cfh.write('\n   return _sizeRead;\n')
        self._cfh.write('}\n\n')

        if main_class and tbl.primary_keys:
            self._write_cpp_method('int',
                                   '%s::List' % cls, '_compare',
                                   'const %s** x, const %s** y' % (cls, cls),
                                   spaceOffset='   ',
                                   static=True)
            self._cfh.write('{\n')
            if len(self._table_key_columns) > 1:
                self._cfh.write('   int rc;\n\n')

            for c in self._table_key_columns[0:-1]:
                self._cfh.write('   if ((rc = %s) != 0)\n' % self._get_compare_static('(*x)', '(*y)', c))
                self._cfh.write('      return rc;\n\n')

            self._cfh.write('   return %s;\n' % self._get_compare_static('(*x)', '(*y)', self._table_key_columns[-1]))
            self._cfh.write('}\n\n')

            self._write_cpp_method('void',
                                   '%s::List' % cls,
                                   'sort',
                                   spaceOffset='   ')
            self._cfh.write('{\n')
            self._cfh.write('   quickSort(_compare);\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('%s *' % cls,
                                   '%s::List' % cls,
                                   'find', 'const %s& obj' % cls,
                                   const=True,
                                   spaceOffset='   ')
            self._cfh.write('{\n')
            self._cfh.write('   return binarySearch(&obj, _compare);\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('%s *' % cls,
                                   '%s::List' % cls,
                                   'find',
                                   'const %s* obj' % cls,
                                   const=True,
                                   spaceOffset='   ')
            self._cfh.write('{\n')
            self._cfh.write('   return binarySearch(obj, _compare);\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('%s *' % cls,
                                   '%s::List' % cls,
                                   'find',
                                   'const %sKey& key' % cls,
                                   const=True,
                                   spaceOffset='   ')
            self._cfh.write('{\n')
            self._cfh.write('   %s obj;\n\n' % cls)
            self._cfh.write('   obj._readKey(key);\n\n')
            self._cfh.write('   return binarySearch(&obj, _compare);\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('%s *' % cls,
                                   '%s::List' % cls,
                                   'find',
                                   'const %sKey* key' % cls,
                                   const=True,
                                   spaceOffset='   ')
            self._cfh.write('{\n')
            self._cfh.write('   %s obj;\n\n' % cls)
            self._cfh.write('   obj._readKey(*key);\n\n')
            self._cfh.write('   return binarySearch(&obj, _compare);\n')
            self._cfh.write('}\n\n')

            self._write_cpp_method('%s *' % cls,
                                   '%s::List' % cls,
                                   'find',
                                   self._table_key_columns,
                                   const=True,
                                   spaceOffset='   ')
            self._cfh.write('{\n')
            self._cfh.write('   %sKey _key(' % cls)

            comma = ''
            for x in self._table_key_columns:
                if x.type == 'timestamp':
                    continue
                self._cfh.write('%s%s' % (comma, x.name))
                comma = ', '

            self._cfh.write(');\n\n')
            self._cfh.write('   return find(_key);\n')
            self._cfh.write('}\n\n')

        self._hfh.write('      DECLARE_SAFE_CLASS(%s::List);\n' % cls)
        self._hfh.write('   };\n\n')

        # Schema
        if main_class:
            self._write_schema(cls)

        # DeclareFields
        self._write_member_decleration(columns)
        self._hfh.write('\n')

        self._hfh.write('};\n\n')


    def _get_compare(self, cls, col):
        fmap = self._field_map[col.type]

        if fmap.type_flag == 'memblock':
            raise Exception('Cannot use a memory block to compare with.  IE, not in a primary or foreign key. (column:%s)' % (
                col.name))

        if fmap.type_flag in ('str', 'date', 'uuid', 'json'):
            return '%s._compare(&((%s*) _obj)->%s)' % (col.name, cls, col.name)

        return 'Mettle::Lib::Common::compare(%s, ((%s*) _obj)->%s)' % (col.name, cls, col.name)


    def _get_compare_static(self, x, y, col):
        fmap = self._field_map[col.type]

        if fmap.type_flag in ('str', 'date', 'uuid', 'json'):
            return '%s->%s._compare(&%s->%s)' % (x, col.name, y, col.name)

        return 'Mettle::Lib::Common::compare(%s->%s, %s->%s)' % (x, col.name, y, col.name)


    def _write_cpp_method(self,
                          returns      : str,
                          cls          : str,
                          method       : str,
                          meth_args    : list = None,
                          inherits     : str  = None,
                          virtual      : bool = False,
                          const        : str  = False,
                          ignore_types : list = [],
                          spaceOffset  : str  = '',
                          static       : bool = False):

        staticStr = ''

        if static:
            staticStr = 'static '

        if virtual:
            if len(returns):
                hstr = '   %svirtual %s %s(' % (staticStr, returns, method)
            else:
                hstr = '   %s%s %s(' % (staticStr, 'virtual', method)
        else:
            if len(returns):
                hstr = '   %s%s %s(' % (staticStr, returns, method)
            else:
                hstr = '   %s%s(' % (staticStr, method)

        cstr = '%s%s::%s(' % ('' if len(returns) == 0 else '%s ' % returns, cls, method)

        if self._hfh:
            self._hfh.write('%s%s' % (spaceOffset, hstr))
        self._cfh.write(cstr)

        if meth_args:
            if type(meth_args) == list:
                self._write_arguements(meth_args, 6 + len(spaceOffset), self._hfh, ignore_types, True)
                self._write_arguements(meth_args, 3, self._cfh, ignore_types, False)
            elif type(meth_args) == str:
                arr   = meth_args.split(',')
                nl    = '\n'
                spch  = '%*s' % (6 + len(spaceOffset), '')
                spcc  = '   '

                for a in arr:
                    if self._hfh:
                        self._hfh.write(nl)
                    self._cfh.write(nl)

                    if self._hfh:
                        if len(spch):
                            self._hfh.write(spch)
                        self._hfh.write(a.strip())

                    if len(spcc):
                        self._cfh.write(spcc)

                    self._cfh.write(a.split('=')[0].strip())
                    nl = ',\n'

        end = ')%s' % (' const' if const else '')

        if self._hfh:
            self._hfh.write('%s;\n\n' % end)
        self._cfh.write('%s\n' % end)

        if inherits:
            for h in inherits:
                self._cfh.write('   :%s\n' % h)


    def _write_arguements(self, meth_args, spacing, fh, filterOut, allowDefaults):
        if not fh:
            return

        if not meth_args:
            return

        nl      = '\n'
        nulls   = []
        spacing = '%*s' % (spacing, '')

        for a in meth_args:
            if filterOut:
                if a.type in filterOut:
                    continue

            fmap = self._field_map[a.type]

            if a.name == self.SELECT_LOCK_ARG:
                fh.write('%s%s' % (nl, spacing))

                fh.write('const %s* %s'  % ('Mettle::DB::DBLock', self._ident_member(a.name)))
                continue

            fh.write('%s%s' % (nl, spacing))

            if fmap.name == 'struct':
                fh.write('const %s%s %s' % (self._lookup_name(a.lookup, ''), fmap.methodpre, self._ident_member(a.name)))
            else:
                fh.write('const %s%s %s' % (fmap.name, fmap.methodpre, self._ident_member(a.name)))

            nl  = ',\n'

            if a.type.startswith('int') and a.not_null is False:
                nulls.append(a)


        for a in nulls:
            fh.write('%s%s' % (nl, spacing))
            if allowDefaults:
                fh.write('const %s %s' % ('bool', '%s_NULL=false' % self._ident_member(a.name)))
            else:
                fh.write('const %s %s' % ('bool', '%s_NULL' % self._ident_member(a.name)))

            nl  = ',\n'

        del nulls


    def _write_copy_args(self, fromObj, meth_args, toObj, fil = None):
        if not meth_args:
            return

        for a in meth_args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            if fmap.name == 'struct':
                self._cfh.write('   %s%s = %s%s%s;\n' % (fromObj,
                                                         self._ident_member(a.name),
                                                         '*' if toObj == '' else '',
                                                         toObj,
                                                         self._ident_member(a.name)))
            else:
                self._cfh.write('   %s%s = %s%s;\n' % (fromObj,
                                                       self._ident_member(a.name),
                                                       toObj,
                                                       self._ident_member(a.name)))

            if a.type.startswith('int') and a.not_null is False:
                self._cfh.write('   %s%s = %s%s_NULL;\n' % (fromObj,
                                                            '%s_NULL' % self._ident_member(a.name),
                                                            toObj,
                                                            self._ident_member(a.name)))


    def _write_member_decleration(self, members):
        if not self._hfh:
            return

        for m in members:
            fmap = self._field_map[m.type]

            if fmap.name == 'struct':
                self._hfh.write('   %s %s;\n' % (self._lookup_name(m.lookup, ''), self._ident_member(m.name)))
            else:
                self._hfh.write('   %s %s;\n' % (fmap.name, self._ident_member(m.name)))

            if m.type.startswith('int') and m.not_null is False:
                self._hfh.write('   %s %s_NULL;\n' % ('bool', self._ident_member(m.name)))


    def _write_encapsualted_fields(self, meth_args, maskDB, maskWithName = None):
        if not meth_args:
            return

        for a in meth_args:
            if a.type == 'dbrec':
                self._cfh.write(maskDB % self._ident_member(a.name))
            else:
                self._cfh.write(maskWithName % (self._ident_member(a.name), self._ident_member(a.name)))

            if a.type.startswith('int') and a.not_null is False:
                self._cfh.write(maskWithName % ('%s_NULL' % self._ident_member(a.name),
                                                '%s_NULL' % self._ident_member(a.name)))


    def _write_clear_fields(self, meth_args, fil = None):
        if not meth_args:
            return

        for a in meth_args:
            if fil and a.type in fil:
                continue

            fmap = self._field_map[a.type]

            if fmap.type_flag in ('str', 'memblock', 'date', 'uuid', 'tableRec', 'json'):
                self._cfh.write('   %s.clear();\n' % (self._ident_member(a.name)))
            elif fmap.type_flag == 'bool':
                self._cfh.write('   %s = false;\n' % (self._ident_member(a.name)))
            else:
                self._cfh.write('   %s = 0;\n' % (self._ident_member(a.name)))

                if a.type.startswith('int') and a.not_null is False:
                    self._cfh.write('   %s = false;\n' % ('%s_NULL' % self._ident_member(a.name)))


    def _write_read_and_write_key(self, cls, columns):
        if not self._table_key_class:
            return

        self._write_cpp_method('void', cls, '_writeKey', '%s& key' % self._table_key_class, const=True)
        self._cfh.write('{\n')
        self._write_copy_args('key.', self._table_key_columns, '')
        self._cfh.write('}\n\n')

        self._write_cpp_method('void', cls, '_readKey', 'const %s& key' % self._table_key_class)
        self._cfh.write('{\n')
        self._write_copy_args('', self._table_key_columns, 'key.')
        self._cfh.write('}\n\n')


    def _write_couplets(self, cls, columns):
        for col in columns:
            if not col.couplets:
                continue

            cname = self._ident('class.couplet', col.name)

            fmap    = self._field_map[col.type]
            keyType = ''
            keyMask = ''
            valMask = 'const char* %s;\n'
            const   = 'const '

            if fmap.type_flag == 'memblock':
                raise Exception('A memory block column (%s) cannot have any couplets.' % col.name)
            elif fmap.type_flag == 'uuid':
                raise Exception('A uuid column (%s) cannot have any couplets.' % col.name)
            elif fmap.type_flag == 'str':
                keyType = 'const char*'
                keyMask = 'const char* %s;\n'
                const   = ''
            elif fmap.type_flag == 'char':
                keyType = 'char'
                keyMask = 'char %s;\n'
            else:
                keyType = fmap.name
                keyMask = fmap.name + ' %s;\n'

            self._hfh.write('   struct %s\n' % cname)
            self._hfh.write('   {\n')

            for key, val in col.couplets.items():
                self._hfh.write('      static ')
                self._hfh.write(keyMask % ('%s' % self._ident_member('Key%s' % self._couplet_name(val))))

            self._hfh.write('\n')

            for key, val in col.couplets.items():
                self._hfh.write('      static ')
                self._hfh.write(valMask % ('%s' % self._ident_member('Value%s' % self._couplet_name(val))))

            self._hfh.write('\n')
            self._hfh.write('      static %s %s;\n' % ('unsigned int', self._ident_member('Count')))
            self._hfh.write('      static %s %s[];\n' % (keyType, self._ident_member('Keys')))
            self._hfh.write('      static %s %s[];\n' % ('const char*', self._ident_member('Values')))

            self._hfh.write('\n')
            self._hfh.write('      static const char* %s(%s%s key) noexcept;\n' % (
                self._ident_member('GetValue'), const, keyType))

            self._hfh.write('   };\n\n')


    def _write_table_class_specific(self, cls, columns):
        self._write_read_and_write_key(cls, columns)
        self._write_couplets(cls, columns)


    def _gen_headers(self):
        if self._mode == self.TABLE:

            self._hfh.write('#ifndef __GENERATED_METTLE_DB_%s_H_\n' % self._gen_info['table'].name.upper())
            self._hfh.write('#define __GENERATED_METTLE_DB_%s_H_\n\n' % self._gen_info['table'].name.upper())

            self._hfh.write('#include "mettle/lib/c99standard.h"\n')
            self._hfh.write('#include "mettle/lib/collection.h"\n')
            self._hfh.write('#include "mettle/lib/datetime.h"\n')

            if self._check_for_type(self._gen_info['table'].columns, 'uuid'):
                self._hfh.write('#include "mettle/lib/guid.h"\n')

            self._hfh.write('#include "mettle/lib/icomparable.h"\n')
            self._hfh.write('#include "mettle/lib/memoryblock.h"\n')
            self._hfh.write('#include "mettle/lib/safe.h"\n')
            self._hfh.write('#include "mettle/lib/string.h"\n')
            self._hfh.write('#include "mettle/lib/xmettle.h"\n\n')
            self._hfh.write('#include "mettle/io/iserializable.h"\n\n')
            self._hfh.write('#include "mettle/db/iprimarykey.h"\n\n')

            self._hfh.write('namespace Mettle\n')
            self._hfh.write('{\n')
            self._hfh.write('   namespace DB\n')
            self._hfh.write('   {\n')
            self._hfh.write('      class DBSchema;\n')
            self._hfh.write('   }\n\n')
            self._hfh.write('   namespace IO\n')
            self._hfh.write('   {\n')
            self._hfh.write('      class IReader;\n')
            self._hfh.write('      class IWriter;\n')
            self._hfh.write('   }\n')
            self._hfh.write('}\n\n')

            self._cfh.write('#include "%s%s.h"\n' % (self._struct_path, self._ident_file(self._gen_info['table'].name)))
            self._cfh.write('#include "mettle/db/dbschema.h"\n')
            self._cfh.write('#include "mettle/lib/common.h"\n\n')
            self._cfh.write('#include "mettle/io/ireader.h"\n')
            self._cfh.write('#include "mettle/io/iwriter.h"\n\n')

            already_incl = []

            for proc in self._gen_info['table'].procs:
                if proc.out_fields:
                    for a in proc.out_fields:
                        if a.type == 'dbrec' and a.lookup != 'table:this':
                            struct_name = self._ident_file(a.lookup[6:])
                            if struct_name not in already_incl:
                                already_incl.append(struct_name)
                                self._hfh.write('#include "%s%s.h"\n' % (self._struct_path, struct_name))

            if already_incl > 0:
                self._hfh.write('\n\n')

        else:

            if self._hfh:
                self._hfh.write('#ifndef __GENERATED_METTLE_DB_%s_DAO_H_\n' % (self._gen_info['table'].name.upper()))
                self._hfh.write('#define __GENERATED_METTLE_DB_%s_DAO_H_\n\n' % (self._gen_info['table'].name.upper()))
                self._hfh.write('#include "%s%s.h"\n\n' % (self._struct_path, self._ident_file(self._gen_info['table'].name)))
                self._hfh.write('#include "mettle/lib/string.h"\n')
                self._hfh.write('#include "mettle/lib/datetime.h"\n')
                self._hfh.write('#include "mettle/lib/memoryblock.h"\n')
                self._hfh.write('#include "mettle/lib/xmettle.h"\n\n')

            self._cfh.write('#include "mettle/lib/common.h"\n')
            self._cfh.write('#include "mettle/db/sqlbuilder.h"\n')
            self._cfh.write('#include "mettle/db/sqlparams.h"\n\n')

            if self._hfh:
                self._hfh.write('namespace Mettle\n')
                self._hfh.write('{\n')
                self._hfh.write('   namespace DB\n')
                self._hfh.write('   {\n')
                self._hfh.write('      class IConnect;\n')
                self._hfh.write('      class DBLock;\n')
                self._hfh.write('      class Statement;\n')
                self._hfh.write('   }\n')
                self._hfh.write('}\n\n')

            self._cfh.write('#include "%s%s"\n\n' % (self.dao_path, self._hFile))
            self._cfh.write('#include "mettle/db/iconnect.h"\n')
            self._cfh.write('#include "mettle/db/dblock.h"\n')
            self._cfh.write('#include "mettle/db/statement.h"\n\n')



    def _gen_trailers(self, hfh):
        if hfh:
            hfh.write('#endif\n\n')


    def _gen_begin_namespaces(self, hfh, cfh):
        ns = self._namespace(blank_ok = True)

        if not ns:
            return

        for name in ns.split('.'):
            if hfh:
                hfh.write('namespace %s { ' % name)
            cfh.write('namespace %s { ' % name)

        if hfh:
            hfh.write('\n\n')
        cfh.write('\n\n')


    def _gen_end_namespaces(self, hfh, cfh):
        ns = self._namespace(blank_ok = True)

        if not ns:
            return

        for name in ns.split('.'):
            if hfh:
                hfh.write('}')
            cfh.write('}')

        if hfh:
            hfh.write('\n\n')
        cfh.write('\n\n')


    def _gen_table_class(self):
        self._table_class = self._ident('class.table', self._gen_info['table'].name)

        self._write_assing_couplets()
        self._write_data_class(self._table_class, self._gen_info['table'].columns, main_class = True)


    def _gen_table_key_class(self):
        self._table_key_class   = None
        self._table_key_columns = self._gen_info['table'].primary_key_columns()

        if len(self._table_key_columns) < 1:
            return

        self._table_key_class = self._ident('class.table', '%sKey' % self._gen_info['table'].name)
        self._write_data_class(self._table_key_class, self._table_key_columns, key_class = True)


    def _gen_dao_class(self):
        self._doa_class = self._ident('class.dao', self._gen_info['table'].name)
        self._stdProcs = self._build_standard_procs(self._gen_info)

        if self._mode != self.DAO:
            return

        if self._hfh:
            self._set_short_comment(self._hfh, self._doa_class)

        self._set_long_comment(self._cfh, self._doa_class)

        if self._hfh:
            self._hfh.write('class %s\n' % self._doa_class)
            self._hfh.write('{\n')
            self._hfh.write('public:\n')

        # DAO::DAO()
        self._write_cpp_method('', self._doa_class, self._doa_class, 'Mettle::DB::IConnect *dbCon', '')
        self._cfh.write('{\n')
        self._cfh.write('   _dbCon = dbCon;\n')
        self._cfh.write('}\n\n')

        # DAO::~DAO()
        self._write_cpp_method('', self._doa_class, '~%s' % self._doa_class, '', virtual=True)
        self._cfh.write('{\n')
        self._cfh.write('}\n\n')

        if 'LockOne' in self._stdProcs:
            lockArg = [Table.Column(True, self.SELECT_LOCK_ARG, 'int32', {'null': False})]

            self._write_cpp_method('void', self._doa_class, self._ident_method('LockOne'), self._table_key_columns + lockArg)
            self._cfh.write('{\n')
            self._write_copy_args('rec.', self._table_key_columns, '')
            self._cfh.write('\n   %s((%s*) 0, %s);\n' % (self._ident_method('LockOne'),
                                                         self._table_key_class,
                                                         self.SELECT_LOCK_ARG))
            self._cfh.write('}\n\n')

            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('LockOne'),
                                   'const %s &irec, const Mettle::DB::DBLock* %s' % (self._table_key_class,
                                                                                     self.SELECT_LOCK_ARG))
            self._cfh.write('{\n')
            self._cfh.write('   rec._readKey(irec);\n')
            self._cfh.write('   %s((%s*) 0, %s);\n' % (self._ident_method('LockOne'),
                                                       self._table_key_class,
                                                       self.SELECT_LOCK_ARG))
            self._cfh.write('}\n\n')

            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('LockOne'),
                                   '%s* irec, const Mettle::DB::DBLock* %s' % (self._table_key_class, self.SELECT_LOCK_ARG))
            self._cfh.write('{\n')
            self._cfh.write('   %s qry(_dbCon);\n' % self._ident('class.dao', '%sLockOne' % self._gen_info['table'].name))
            self._cfh.write('   %s key;\n\n' % self._table_key_class)
            self._cfh.write('   if (irec)\n')
            self._cfh.write('      key = *irec;\n')
            self._cfh.write('   else\n')
            self._cfh.write('      rec._writeKey(key);\n\n')
            self._cfh.write('   for (int32_t _dex = %s->retrys > 0 ? %s->retrys - 1 : 0; _dex >= 0; --_dex)\n' % (
                self.SELECT_LOCK_ARG, self.SELECT_LOCK_ARG))
            self._cfh.write('   {\n')
            self._cfh.write('      try\n')
            self._cfh.write('      {\n')
            self._cfh.write('         if (!qry.%s(&key).%s())\n' % (self._ident_method('Exec'), self._ident_method('Fetch')))
            self._cfh.write('            throw Mettle::Lib::xMettle(__FILE__, __LINE__, "%s", "LockOne'
                            ' failed to return a record");\n' % (self._doa_class))
            self._cfh.write('         break;\n')
            self._cfh.write('      }\n')
            self._cfh.write('      catch (Mettle::Lib::xMettle &x)\n')
            self._cfh.write('      {\n')
            self._cfh.write('         if (x.errorCode != Mettle::Lib::xMettle::DBLockNoWaitFailed)\n')
            self._cfh.write('            throw;\n\n')
            self._cfh.write('         if (_dex == 0)\n')
            self._cfh.write('            throw Mettle::Lib::xMettle(__FILE__, __LINE__, Mettle::Lib::xMettle::'
                            'DBLockNoWaitFailed, "%s", "Could not lock (%s) record after %s attempt(s) at %s mili second'
                            ' intervals!", %s->retrys, %s->miliSeconds);\n\n' % (self._doa_class,
                                                                                 self._gen_info['table'].name,
                                                                                 "%d",
                                                                                 "%d",
                                                                                 self.SELECT_LOCK_ARG,
                                                                                 self.SELECT_LOCK_ARG))
            self._cfh.write('         if (%s->miliSeconds > 0)\n' % self.SELECT_LOCK_ARG)
            self._cfh.write('            Mettle::Lib::Common::sleepMili(%s->miliSeconds);\n' % self.SELECT_LOCK_ARG)
            self._cfh.write('      }\n')
            self._cfh.write('   }\n\n')
            self._cfh.write('   rec = qry.orec;\n')
            self._cfh.write('}\n\n')

        if 'SelectOne' in self._stdProcs:
            self._write_cpp_method('bool', self._doa_class, self._ident_method('TrySelectOne'), self._table_key_columns)
            self._cfh.write('{\n')
            self._write_copy_args('rec.', self._table_key_columns, '')
            self._cfh.write('\n   return %s();\n' % self._ident_method('TrySelectOne'))
            self._cfh.write('}\n\n')

            self._write_cpp_method('bool', self._doa_class, self._ident_method('TrySelectOne'), 'const %s &irec' % (
                self._table_key_class))
            self._cfh.write('{\n')
            self._cfh.write('   rec._readKey(irec);\n')
            self._cfh.write('\n   return %s();\n' % self._ident_method('TrySelectOne'))
            self._cfh.write('}\n\n')

            # bool DAO::trySelectOne(*TableKeyClass = 0)
            self._write_cpp_method('bool', self._doa_class, self._ident_method('TrySelectOne'), '%s *irec = 0' % (
                self._table_key_class))
            self._cfh.write('{\n')
            self._cfh.write('   %s qry(_dbCon);\n' % self._ident('class.dao', '%sSelectOne' % self._gen_info['table'].name))
            self._cfh.write('   %s key;\n\n' % self._table_key_class)
            self._cfh.write('   if (irec)\n')
            self._cfh.write('      key = *irec;\n')
            self._cfh.write('   else\n')
            self._cfh.write('      rec._writeKey(key);\n\n')
            self._cfh.write('   if (!qry.%s(&key).%s())\n' % (self._ident_method('Exec'), self._ident_member('Fetch')))
            self._cfh.write('      return false;\n\n')
            self._cfh.write('   rec = qry.orec;\n\n')
            self._cfh.write('   return true;\n')
            self._cfh.write('}\n\n')

            # void DAO::SelectOne(args)
            self._write_cpp_method('void', self._doa_class, self._ident_method('SelectOne'), self._table_key_columns)
            self._cfh.write('{\n')
            self._write_copy_args('rec.', self._table_key_columns, '')
            self._cfh.write('\n   %s();\n' % self._ident_method('SelectOne'))
            self._cfh.write('}\n\n')

            self._write_cpp_method('void', self._doa_class, self._ident_method('SelectOne'), 'const %s& irec' % (
                self._table_key_class))
            self._cfh.write('{\n')
            self._cfh.write('   rec._readKey(irec);\n')
            self._cfh.write('\n   %s();\n' % self._ident_method('SelectOne'))
            self._cfh.write('}\n\n')

            # void DAO::SelectOne(*TableKeyClass = 0)
            self._write_cpp_method('void', self._doa_class, self._ident_method('SelectOne'), '%s* irec=0' % (
                self._table_key_class))
            self._cfh.write('{\n')
            self._cfh.write('   if (!%s(irec))\n' % self._ident_method('trySelectOne'))
            self._cfh.write('      throw Mettle::Lib::xMettle(__FILE__, __LINE__, "%s", "SelectOne'
                            ' failed to return a record");\n' % (self._doa_class))
            self._cfh.write('}\n\n')


        if 'Update' in self._stdProcs:
            # void DAO::Update(args)
            upd_ignore_types = ['timestamp']
            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('Update'),
                                   self._gen_info['table'].columns,
                                   ignore_types=upd_ignore_types)
            self._cfh.write('{\n')
            self._write_copy_args('rec.', self._gen_info['table'].columns, '', upd_ignore_types)
            self._cfh.write('\n   %s();\n' % self._ident_method('Update'))
            self._cfh.write('}\n\n')

            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('Update'),
                                   'const %s& irec' % self._table_class)
            self._cfh.write('{\n')
            self._cfh.write('   rec = irec;\n\n')
            self._cfh.write('   %s();\n' % self._ident_method('Update'))
            self._cfh.write('}\n\n')

            # void DAO::Update(*TableClass = 0)
            self._write_cpp_method('void', self._doa_class, self._ident_method('Update'), '%s* irec=0' % self._table_class)
            self._cfh.write('{\n')
            self._cfh.write('   if (irec)\n')
            self._cfh.write('      rec = *irec;\n\n')
            self._cfh.write('   %s qry(_dbCon);\n\n' % self._ident('class.dao', '%sUpdate' % self._gen_info['table'].name))
            self._cfh.write('   qry.%s(&rec);\n\n' % self._ident_method('Exec'))
            self._cfh.write('   if (irec)\n')
            self._cfh.write('      *irec = rec;\n')
            self._cfh.write('}\n\n')


        if 'Insert' in self._stdProcs:
            # void DAO::Insert(args)
            upd_ignore_types = ['seq32', 'seq64', 'timestamp']
            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('Insert'),
                                   self._gen_info['table'].columns,
                                   ignore_types=upd_ignore_types)
            self._cfh.write('{\n')
            self._write_copy_args('rec.', self._gen_info['table'].columns, '', upd_ignore_types)
            self._cfh.write('\n   %s();\n' % self._ident_method('Insert'))
            self._cfh.write('}\n\n')

            # void DAO::insert(*TableClass = 0)
            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('Insert'),
                                   'const %s& irec' % self._table_class)
            self._cfh.write('{\n')
            self._cfh.write('   rec = irec;\n\n')
            self._cfh.write('   %s();\n' % self._ident_method('Insert'))
            self._cfh.write('}\n\n')

            # void DAO::insert(*TableClass = 0)
            self._write_cpp_method('void', self._doa_class, self._ident_method('Insert'), '%s* irec=0' % self._table_class)
            self._cfh.write('{\n')
            self._cfh.write('   if (irec)\n')
            self._cfh.write('      rec = *irec;\n\n')
            self._cfh.write('   %s qry(_dbCon);\n\n' % self._ident('class.dao', '%sInsert' % self._gen_info['table'].name))
            self._cfh.write('   qry.%s(&rec);\n\n' % self._ident_method('Exec'))
            self._cfh.write('   if (irec)\n')
            self._cfh.write('      *irec = rec;\n')
            self._cfh.write('}\n\n')

        if 'DeleteOne' in self._stdProcs:
            # void DAO::DeleteOne(args)
            self._write_cpp_method('void', self._doa_class, self._ident_method('DeleteOne'), self._table_key_columns)
            self._cfh.write('{\n')
            self._write_copy_args('rec.', self._table_key_columns, '')
            self._cfh.write('\n   %s();\n' % self._ident_method('DeleteOne'))
            self._cfh.write('}\n\n')

            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('DeleteOne'),
                                   'const %s& irec' % self._table_key_class)
            self._cfh.write('{\n')
            self._cfh.write('   rec._readKey(irec);\n\n')
            self._cfh.write('   %s();\n' % self._ident_method('DeleteOne'))
            self._cfh.write('}\n\n')

            # void DAO::deleteOne(*TableKeyClass = 0)
            self._write_cpp_method('void',
                                   self._doa_class,
                                   self._ident_method('DeleteOne'),
                                   '%s* irec=0' % self._table_class)
            self._cfh.write('{\n')
            self._cfh.write('   %s qry(_dbCon);\n\n' % self._ident('class.dao', '%sDeleteOne' % self._gen_info['table'].name))
            self._cfh.write('   %s key;\n\n' % self._table_key_class)
            self._cfh.write('   if (irec)\n')
            self._cfh.write('      irec->_writeKey(key);\n')
            self._cfh.write('   else\n')
            self._cfh.write('      rec._writeKey(key);\n\n')
            self._cfh.write('   qry.%s(&key);\n' % self._ident_method('Exec'))
            self._cfh.write('}\n\n')

        if 'DeleteAll' in self._stdProcs:
            # void DAO::DeleteAll()
            self._write_cpp_method('void', self._doa_class, self._ident_method('DeleteAll'), '')
            self._cfh.write('{\n')
            self._cfh.write('   %s qry(_dbCon);\n\n' % self._ident('class.dao', '%sDeleteAll' % self._gen_info['table'].name))
            self._cfh.write('   qry.%s();\n' % self._ident_method('Exec'))
            self._cfh.write('}\n\n')

        # Members
        if self._hfh:
            self._hfh.write('   %s rec;\n\n' % self._table_class)
            self._hfh.write('private:\n\n')
            self._hfh.write('   Mettle::DB::IConnect *_dbCon;\n')
            self._hfh.write('\n};\n\n')


    def _gen_standard_procs(self):
        for proc in self._stdProcs:
            if proc == 'Insert':
                self._write_sql_proc_dao(self._stdProcs['Insert'], [], False, True)
            elif proc == 'Update':
                self._write_sql_proc_dao(self._stdProcs['Update'], ['timestamp'], True)
            else:
                self._write_sql_proc_dao(self._stdProcs[proc])


    def _gen_custom_procs(self):
        for proc in self._gen_info['table'].procs:
            if proc.in_fields:
                if proc.in_fields[0].type != 'dbrec':
                    self._write_data_class(self._ident('class.qryin',
                                           '%s%s' % (self._gen_info['table'].name, proc.name)), proc.in_fields)

            if proc.out_fields:
                if proc.out_fields[0].type != 'dbrec':
                    self._write_data_class(self._ident('class.qryout',
                                           '%s%s' % (self._gen_info['table'].name, proc.name)), proc.out_fields)

            self._write_sql_proc_dao(proc)


    def _gen_table_schema(self):
        if self._mode != self.TABLE:
            return

        self._schema_tables.append('%s%s.h|%s' % (self._struct_path,
                                                  self._ident_file(self._gen_info['table'].name),
                                                  self._table_class))
