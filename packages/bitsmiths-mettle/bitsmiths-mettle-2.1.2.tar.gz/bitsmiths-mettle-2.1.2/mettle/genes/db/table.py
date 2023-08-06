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

import mettle.genes


class Table:
    """
    Table class for the database project
    """

    VERSION  = 2.1
    NULL     = False
    NOT_NULL = True

    class Column:
        """
        Column object for the table.
        """

        def __init__(self,
                     tbl_def:  bool,
                     name:     str,
                     datatype: str,
                     dav:      dict = None,
                     def_val:  str = None):
            """
            Constructor.

            :param tbl_def: Table defintion mode or not.
            :param name: Column name.
            :param datatype: Column type.
            :param dav: Dictionary of dav validators.
            """
            self.lookup     = None
            self._resolved  = False

            if tbl_def:
                if datatype.startswith('braze:')  or\
                   datatype.startswith('table:')  or\
                   datatype.startswith('column:') or\
                   datatype.startswith('this'):
                    raise Exception('Data type [%s] not allowed [column:%s]!' % (datatype, name))
            else:
                if datatype.startswith('braze:'):
                    self.lookup = datatype
                    datatype    = 'brazerec'
                elif datatype.startswith('table:'):
                    self.lookup = datatype
                    datatype    = 'dbrec'

            self.name     = name
            self.type     = datatype
            self.length   = 0
            self.not_null = True
            self.couplets = None
            self.def_val  = def_val
            self.dav      = dav

            if self.type.startswith('this') or self.type.startswith('column:'):
                return

            if datatype not in mettle.genes.DataTypes:
                raise Exception('Data type [%s] not expected [column:%s]!' % (datatype, name))

            self._assign_dav(dav, tbl_def)
            self._resolved = True


        def _assign_dav(self, dav, tbl_def):
            if not dav:
                return

            if type(dav) != dict:
                raise Exception('DAV type [%s] is not a dictionary [column:%s]!' % (
                    str(type(dav)), self.name))

            for dkey, dval in dav.items():
                if type(dkey) != str:
                    raise Exception('Dav dictionary key type [%s] not expected [column:%s, requires:str]!' % (
                        str(type(dval)), self.name))

                if dkey == 'null':
                    if type(dval) != bool:
                        raise Exception('Dav value type [%s] not expected [column:%s, dav:%s, requires:bool]!' % (
                            str(type(dval)), self.name, dkey))

                    self.not_null = not dval
                    continue

                if dkey == 'max':
                    if type(dval) != int:
                        raise Exception('Dav value type [%s] not expected [column:%s, dav:%s, requires:int]!' % (
                            str(type(dval)), self.name, dkey))

                    if dval < 0:
                        raise Exception('Dav value [%d] cannot be less than zero [column:%s, dav:%s, requires:int]!' % (
                            dval, self.name, dkey))

                    self.length = dval
                    continue

                if dkey == 'in':
                    if type(dval) != dict:
                        if not tbl_def and type(dval) != list:
                            raise Exception('Dav value type [%s] not expected [column:%s, dav:%s, requires:dict]!' % (
                                str(type(dval)), self.name, dkey))

                    self.couplets = dval
                    continue

                if dkey in ['notin', 'func', 'regex', 'min']:
                    continue

                raise Exception('Dav type [%s] not known [column:%s]!' % (dkey, self.name))



        def _resolve(self, gen_info: dict, table_name, proc):
            """
            Resolve the column type/davs from geninfo.
            """
            if self._resolved:
                return

            if not self.type.startswith('this') and not self.type.startswith('column:'):
                raise Exception('Reolve type [%s] not expected [table:%s, proc:%s, field:%s]' % (
                    self.type, table_name, proc, self.name))

            srcTbl = None
            srcCol = None

            if self.type == 'this':
                srcTbl = table_name
                srcCol = self.name
            elif self.type.startswith('this.'):
                srcTbl = table_name
                srcCol = self.type[5:]
            else:
                if self.type.startswith("column:"):
                    srcCol = self.type[7:]
                else:
                    srcCol = self.type

                dot    = srcCol.find('.')

                if dot == -1:
                    srcTbl = table_name
                else:
                    srcTbl = srcCol[:dot]
                    srcCol = srcCol[dot + 1:]

            resTbl = gen_info['all_tables'].get(srcTbl)

            if not resTbl:
                raise Exception('Table [%s] not found resolving sql proc [table:%s, proc:%s, field:%s, type:%s]' % (
                    srcTbl, table_name, proc, self.name, self.type))

            resCol = resTbl.get_column(srcCol)

            if not resCol:
                raise Exception('Column [%s.%s] not found resolving sql proc [table:%s, proc:%s, field:%s, type:%s]' % (
                    srcTbl, srcCol, table_name, proc, self.name, self.type))

            self.type = resCol.type

            if not self.dav:
                self.dav = resCol.dav
            elif resCol.dav:
                tmp      = self.dav
                self.dav = {}
                self.dav.update(resCol.dav)
                self.dav.update(tmp)

            if self.dav:
                self._assign_dav(self.dav, False)

            self._resolved = True


    class Index:
        """
        Index object for the table.
        """
        def __init__(self, name):
            self.name    = name
            self.columns = []


    class ForeignKey:
        """
        ForeignKey object for the table.
        """
        def __init__(self, name, ref_table):
            self.name      = name
            self.ref_table = ref_table
            self.columns   = []


    class PrimaryKey:
        """
        Primary Key object for the table.
        """
        def __init__(self, column_name, index):
            self.column_name = column_name
            self.index       = index


    class SqlProcedure:
        """
        SqlProcedure object for the table.
        """
        def __init__(self, table: str, name: str, dao_mode: str = ''):
            self._table      = table
            self.name        = name
            self.dao_mode    = dao_mode
            self.in_fields   = []
            self.out_fields  = []
            self.sql         = {'std' : ''}
            self.is_standard = True

        def in_field(self, col_name: str, data_type: str, dav: dict = None):
            try:
                c = Table.Column(False, col_name, data_type, dav)
            except Exception as x:
                raise Exception('Table [%s], Proc [%s] - %s' % (self._table.name, self.name, str(x)))

            self.in_fields.append(c)

            return c

        def out_field(self, col_name: str, data_type: str, dav: dict = None):
            c = Table.Column(False, col_name, data_type, dav)

            self.out_fields.append(c)

            return c


    class UniqueKey:
        """
        UniqueKey object for the table.
        """
        def __init__(self, name: str):
            self.name    = name
            self.columns = []


    def __init__(self, name, version):
        """
        Table constructor.
        """
        self.name         = name
        self.sourcePath   = None
        self.columns      = []
        self.primary_keys = []
        self.foreign_keys = []
        self.unique_keys  = []
        self.indexes      = []
        self.procs        = []

        self.select_one   = False
        self.lock_one     = False
        self.select_all   = False
        self.update       = False
        self.insert       = False
        self.delete_one   = False
        self.delete_all   = False

        if version != self.VERSION:
            raise Exception('Table version %f is not the same as Table Generator version %f' % (version, self.VERSION))


    def column(self, col_name: str, data_type: str, dav: dict = None):
        try:
            c = Table.Column(True, col_name, data_type, dav)
        except Exception as x:
            # print 'Column [name:%s, data_type:%s] - %s' % (col_name, data_type, str(x)))
            raise x

        self.columns.append(c)

        return c


    def sql_proc(self, name: str, dao_mode: str = ''):
        p = Table.SqlProcedure(self, name, dao_mode)

        self.procs.append(p)

        return p


    def primary_key(self, *col_names) -> "PrimaryKey":
        pk = None

        for x in col_names:
            colIdx = self.get_column_index(x)

            if colIdx == -1:
                raise Exception("Could not add primary key, column '%s' is not part of table '%s'" % (x, self.name))

            pk = Table.PrimaryKey(x, colIdx)

            self.primary_keys.append(pk)

        return pk


    def foreign_key(self, name: str, ref_table: str, *col_names) -> "ForeignKey":
        if not col_names:
            raise Exception("ForeignKey '%s' for table '%s' cannot have no columns!" % (name, self.name))

        fk = Table.ForeignKey(name, ref_table)

        for x in col_names:
            colIdx = self.get_column_index(x)

            if colIdx == -1:
                raise Exception("Column '%s' not found when adding ForeignKey(%s) onto table '%s'!" % (
                    str(x), ref_table, self.name))

            fk.columns.append(colIdx)

        self.foreign_keys.append(fk)

        return fk


    def index(self, index_name: str, *col_names) -> "Index":
        if not col_names:
            raise Exception("Index '%s' for table '%s' cannot have no columns!" % (index_name, self.name))

        idx = Table.Index(index_name)

        for x in col_names:
            colIdx = self.get_column_index(x)

            if colIdx == -1:
                raise Exception("Column '%s' not found when adding Index(%s) onto table '%s'!" % (
                    str(x), index_name, self.name))

            idx.columns.append(colIdx)

        self.indexes.append(idx)

        return idx


    def unique_key(self, uk_name: str, *col_names) -> "UniqueKey":
        if not col_names:
            raise Exception("Unique Key '%s' for table '%s' cannot have no columns!" % (uk_name, self.name))

        uk = Table.UniqueKey(uk_name)

        for x in col_names:
            colIdx = self.get_column_index(x)

            if colIdx == -1:
                raise Exception("Column '%s' not found when adding Unique Key(%s) onto table '%s'!" % (
                    str(x), uk_name, self.name))

            uk.columns.append(colIdx)

        self.unique_keys.append(uk)

        return uk


    def primary_key_columns(self) -> list:
        flds = []

        for f in self.primary_keys:
            flds.append(self.columns[f.index])

        return flds


    def non_primary_key_columns(self) -> list:
        flds = []
        col  = 0

        for f in self.columns:
            add = True
            for p in self.primary_keys:
                if col == p.index:
                    add = False
                    break

            col += 1
            if add:
                flds.append(f)

        return flds


    def get_column_index(self, col_name: str) -> int:
        idx = 0

        for i in self.columns:
            if i.name == col_name:
                return idx
            idx += 1

        return -1


    def get_column(self, col_name: str) -> "Column":
        for i in self.columns:
            if i.name == col_name:
                return i

        return None
