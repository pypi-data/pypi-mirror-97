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

import getopt
import os.path

from .data_types        import DataTypes
from .braze_project     import BrazeProject
from .database_project  import DatabaseProject
from .mk_project        import MkProject
from .zip_buddy         import ZipBuddy


def _cli_show_usage():
    print()
    print('usage: mettle-genes [--clean] PROJ')
    print()
    print('required arguments:')
    print('  PROJ            The path to the project yaml file')
    print('  -c, --clean     If specified, will clean the project output instead.')
    print()
    print('optional arguments:')
    print('  -?, -h, --help  Show this help message and exit')
    print()


def _cli_read_args(args: list) -> dict:
    try:
        optlist, gargs = getopt.getopt(args, '?hc', [ 'help', 'clean' ])
    except getopt.GetoptError as err:
        print(err)
        return _cli_show_usage()

    aobj = {
        'clean' : False,
        'proj'  : None,
    }

    for o, a in optlist:
        if o in ('-?', '-h', '--help'):
            return _cli_show_usage()

        if o in ('-c', '--clean'):
            aobj['clean'] = True
            continue

        print('\n ... unrecognized arguments: %s' % o)
        return _cli_show_usage()

    if not gargs:
        print('\n ... project path not specified')
        return _cli_show_usage()

    proj = gargs[0]

    if not os.path.exists(proj):
        print('\n ... project path [%s] not found\n' % proj)
        return None

    if not os.path.isfile(proj):
        print('\n ... project path [%s] is not a file\n' % proj)
        return _cli_show_usage()

    aobj['proj'] = proj

    return aobj


def cli_run(args: list) -> int:

    aobj = _cli_read_args(args)

    if not aobj:
        return 2

    from mettle.genes import service

    if aobj.get('clean') is True:
        service.proj_clean(aobj['proj'])
    else:
        service.proj_generate(aobj['proj'])

    return 0


def _cli_show_sql_build_usage():
    """
    Prints the program usage.
    """
    print()
    print('usage: mettle-sql-build [ -s SQL | -f FILE | --clean ] OFILE ')
    print()
    print('required arguments:')
    print('  OFILE            The target output file to write to')
    print()
    print('optional arguments:')
    print('  -f, --file FILE  The input file to send to the output file')
    print('  -s, --sql SQL    The sql command to send to the output file')
    print('  -c, --clean      Cleans the file before writing to it')
    print('  -?, -h, --help   Show this help message and exit')
    print()



def _cli_read_sql_build_args(args: list) -> dict:
    """
    Reads the command line arguements for the sql builder.

    :return: The args read.
    """
    try:
        optlist, gargs = getopt.getopt(args, 'f:s:ch?', [ 'help', 'file=', 'sql=', 'clean' ])
    except getopt.GetoptError as err:
        print(err)
        _cli_show_sql_build_usage()

    res = { 'ofile': None, 'ifile': None, 'sql': None, 'open_args': 'at+' }

    for o, a in optlist:
        if o in ('-h', '--help', '-?'):
            return _cli_show_sql_build_usage()
        elif o in ('-f', '--file'):
            res['ifile'] = a
        elif o in ('-s', '--sql'):
            res['sql'] = a
        elif o in ('-c', '--clean'):
            res['open_args'] = 'wt'
        else:
            print('\n ... unrecognized arguments: %s' % o)
            return _cli_show_sql_build_usage()

    if not gargs:
        print('\n ... output file not specified')
        return _cli_show_sql_build_usage()

    res['ofile'] = gargs[0]

    return res


def cli_sql_build(args: dict) -> int:
    """
    Main
    """
    import sqlparse

    aobj = _cli_read_sql_build_args(args)

    if not aobj:
        return 2

    with open(aobj['ofile'], aobj['open_args']) as fw:

        if aobj['ifile']:
            with open(aobj['ifile'], 'rt') as fr:
                sqlfile = fr.read()
                sqlfile = sqlparse.format(sqlfile,
                                          strip_comments=True,
                                          keyword_case='upper',
                                          identifier_case='lower')

                statements = [ x.strip() for x in sqlparse.split(sqlfile) ]

                for stmnt in statements:
                    if stmnt.startswith("\\"):
                        continue
                    fw.write(stmnt)
                    fw.write('\n')

        elif aobj['sql']:
            fw.write(aobj['sql'].strip())
            fw.write('\n')

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(cli_run(_cli_read_args(sys.argv[1:])))


__all__ = [ 'DataTypes', 'BrazeProject', 'DatabaseProject', 'MkProject', 'ZipBuddy', 'cli_run', 'cli_sql_build' ]
