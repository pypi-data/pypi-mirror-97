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
import sys

from .generator import Generator


class GenCpp(Generator):

    CPP_TYPES = [
        'lib',
        'so',
        'exe',
        'pyd',
    ]

    TYPE_DESCR = {
        'lib' : 'static library (.a, or .lib)',
        'so'  : 'shared object library (.so or .dll)',
        'pyd' : 'a python specfic shared object (.pyd or .so)',
        'exe' : 'an executable',
    }

    COMPILERS = {
        'gnu' : {
            'id'     : 'gnu',
            'descr'  : 'Gnu C++ (Linux)',
            'exts'   : { 'obj': '.o', 'lib': '.a', 'so': '.so', 'exe': '', 'pyd': '.so' },
            'c'      : 'gcc',
            'cpp'    : 'g++',
            'link'   : 'ar',
            'lindex' : 'ranlib',
            'flags'  : {
                'compile' : {
                    'cpp' : {
                        'release' : {
                            'lib'  : '-c -O2 -fPIC -std=gnu++11',
                            'so'   : '-c -O2 -std=gnu++11',
                            'exe'  : '-c -O2 -std=gnu++11',
                            'pyd'  : '-c -O2 -fPIC -std=gnu++11',
                        },
                        'debug'   : {
                            'lib' : '-c -g -fPIC -std=gnu++11',
                            'so'  : '-c -g -std=gnu++11',
                            'exe' : '-c -g',
                            'pyd' : '-c -g -fPIC -std=gnu++11',
                        },
                    },
                    'cc' : {
                        'release' : {
                            'lib'  : '-c -O2 -fPIC -std=gnu++11',
                            'so'   : '-c -O2 -std=gnu++11',
                            'exe'  : '-c -O2 -std=gnu++11',
                            'pyd'  : '-c -O2 -fPIC -std=gnu++11',
                        },
                        'debug'   : {
                            'lib' : '-c -g -fPIC -std=gnu++11',
                            'so'  : '-c -g -std=gnu++11',
                            'exe' : '-c -g',
                            'pyd' : '-c -g -fPIC -std=gnu++11',
                        },
                    },
                },
                'link' : {
                    'release' : { 'lib': '-rs $(DEST)', 'so': '', 'exe': '', 'pyd': '' },
                    'debug'   : { 'lib': '-rs $(DEST)', 'so': '', 'exe': '', 'pyd': '' },
                },
            },
        },
        'mingw' : {
            'id'     : 'mingw',
            'descr'  : 'MinGW (Windows)',
            'exts'   : { 'obj': '.o', 'lib': '.a', 'so': '.dll', 'exe': '.exe', 'pyd': '.pyd' },
            'c'      : 'gcc.exe',
            'cpp'    : 'g++.exe',
            'link'   : 'ar.exe',
            'lindex' : 'ranlib.exe',
            'flags'  : {
                'compile' : {
                    'cpp' : {
                        'release' : {
                            'lib'  : '-c -O2',
                            'so'   : '-c -O2',
                            'exe'  : '-c -O2',
                            'pyd'  : '-c -O2 -DMS_WIN64',
                        },
                        'debug'   : {
                            'lib' : '-c -g',
                            'so'  : '-c -g',
                            'exe' : '-c -g',
                            'pyd' : '-c -g -DMS_WIN64',
                        },
                    },
                    'cc' : {
                        'release' : {
                            'lib'  : '-c -O2',
                            'so'   : '-c -O2',
                            'exe'  : '-c -O2',
                            'pyd'  : '-c -O2 -DMS_WIN64',
                        },
                        'debug'   : {
                            'lib' : '-c -g',
                            'so'  : '-c -g',
                            'exe' : '-c -g',
                            'pyd' : '-c -g -DMS_WIN64',
                        },
                    },
                },
                'link' : {
                    'release' : { 'lib': '-rs $(DEST)', 'so': '', 'exe': '', 'pyd': '' },
                    'debug'   : { 'lib': '-rs $(DEST)', 'so': '', 'exe': '', 'pyd': '' },
                },
            },
        },
        'msc' : {
            'id'     : 'msc',
            'descr'  : 'Microsoft C++ (Windows)',
            'exts'   : { 'obj': '.obj', 'lib': '.lib', 'so': '.dll', 'exe': '.exe', 'pyd': '.pyd' },
            'c'      : 'cl.exe',
            'cpp'    : 'cl.exe',
            'link'   : 'lib.exe',
            'lindex' : '',
            'flags'  : {
                'compile' : {
                    'cpp' : {
                        'release' : {
                            'lib'  : '',
                            'so'   : '',
                            'exe'  : '',
                            'pyd'  : '',
                        },
                        'debug'   : {
                            'lib' : '',
                            'so'  : '',
                            'exe' : '',
                            'pyd' : '',
                        },
                    },
                    'cc' : {
                        'release' : {
                            'lib'  : '',
                            'so'   : '',
                            'exe'  : '',
                            'pyd'  : '',
                        },
                        'debug'   : {
                            'lib' : '',
                            'so'  : '',
                            'exe' : '',
                            'pyd' : '',
                        },
                    },
                },
                'link' : {
                    'release' : { 'lib': '', 'so': '', 'exe': '', 'pyd': '' },
                    'debug'   : { 'lib': '', 'so': '', 'exe': '', 'pyd': '' },
                },
            },
        },
    }


    def __init__(self):
        """
        Constructor.
        """
        Generator.__init__(self)
        self._comp = self.COMPILERS['gnu']  # The compiler being used, gnu is the default


    def name(self) -> str:
        """
        Overload.
        """
        return 'C++'


    def type_descr(self, type_id: str) -> str:
        """
        Overload.
        """
        return self.TYPE_DESCR[type_id]


    def _makefile_types(self) -> list:
        """
        Overload.
        """
        return self.CPP_TYPES


    def generate_makefiles(self, gen_info: dict):
        """
        Overload.
        """
        Generator.generate_makefiles(self, gen_info)

        clean = gen_info.get('clean')

        self._initialize()

        for targ in self._targets:
            if clean:
                self._clean_target(targ)
                continue

            if self._skip(targ):
                continue

            self._gen_target(targ)

        # self._destroy()


    def _initialize(self):
        """
        Initialize the generator.
        """
        if self._compilers:

            comp = None

            if sys.platform in self._compilers.keys():
                comp = self._compilers.get(sys.platform)
            else:
                logging.warning('Compiler operating system [%s] not found... using default [%s]' % (
                    sys.platform, self._comp['descr']))
                return

            if not comp or comp not in self.COMPILERS:
                raise Exception('Compiler [%s] not expected. Expected comilers are: %s' % (
                    self._comp, str(self.COMPILERS.keys())))

            self._comp = self.COMPILERS[comp]

        logging.info('[%s] is using %s compiler' % (self.name(), self._comp['descr']))


    def _gen_target(self, targ: dict) -> None:
        """
        Generate the target item make file.

        :param targ: The target object to generate a make file for.
        """
        gf = self._makefile_open(targ)

        if not targ.get('src-paths'):
            raise Exception('%s has no "src-paths" : [%s]' % (gf.targ_id, str(targ)))

        self._gen_header(gf, 'mettle.genes.mk.gen_cpp')
        self._gen_std_vars(gf)
        self._gen_compiler_vars(gf)

        self._gen_incl_paths(gf)
        self._gen_so_paths(gf)
        self._gen_library_paths(gf)

        src_list = self._gen_source_paths(gf)

        self._gen_usage(gf)
        self._gen_release_debug(gf)
        self._gen_clean(gf, src_list)
        self._gen_dest_targ(gf)

        self._gen_trailers(gf)
        self._makefile_close(gf)


    def _gen_compiler_vars(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Overload.
        """
        tt    = gf.targ['type']
        targ  = gf.targ
        flags = targ.get('flags')
        tobj  = self._types[tt]

        cpp_flags  = ''
        cc_flags   = ''
        link_flags = ''

        if flags:
            comp_flag = '%s|' % self._comp['id']

            for fl_id in flags:
                items = flags[fl_id]
                idx   = 0

                while idx < len(items):
                    flag = items[idx]
                    if flag.find('|') >= 0:
                        if flag.startswith(comp_flag):
                            items[idx] = items[idx][len(comp_flag):]
                        else:
                            items.pop(idx)
                            continue
                    idx += 1

            if flags.get('cpp'):
                cpp_flags = ' '.join(flags.get('cpp'))

            if flags.get('cc'):
                cc_flags = ' '.join(flags.get('cc'))

            if flags.get('link'):
                link_flags = ' '.join(flags.get('link'))

        gf.fh.write('# Compiler & Linker\n')

        gf.fh.write('CPP_CMD          = %s\n' % self._comp['cpp'])
        gf.fh.write('CC_CMD           = %s\n' % self._comp['c'])
        gf.fh.write('LINK_CMD         = %s\n' % self._comp['link'])
        gf.fh.write('LINK_INDEXER     = %s\n' % self._comp['lindex'])
        gf.fh.write('DEST             = _var_\n')
        gf.fh.write('DEBUG_FLAG       = _var_\n')
        gf.fh.write('CPP_FLAGS        = _var_\n')
        gf.fh.write('CC_FLAGS         = _var_\n')
        gf.fh.write('LINK_FLAGS       = _var_\n')
        gf.fh.write('CPP_FLAGS_EXTRA  = %s\n' % cpp_flags)
        gf.fh.write('CC_FLAGS_EXTRA   = %s\n' % cc_flags)
        gf.fh.write('LINK_FLAGS_EXTRA = %s\n\n' % link_flags)

        gf.fh.write('# Target Descriptors\n')

        gf.fh.write('ARCH_SIZE     =\n')
        gf.fh.write('TARG_EXT_LIB  = %s\n' % self._comp['exts']['lib'])
        gf.fh.write('TARG_EXT_SO   = %s\n' % self._comp['exts']['so'])
        gf.fh.write('TARG_EXT_EXE  = %s\n' % self._comp['exts']['exe'])
        gf.fh.write('TARG_EXT_PYD  = %s\n' % self._comp['exts']['pyd'])
        gf.fh.write('TARG_EXT      = $(TARG_EXT_%s)\n' % tt.upper())
        gf.fh.write('TARG_COMP     = _%s\n' % self._comp['id'])
        gf.fh.write('TARG_NAME     = %s\n' % targ['name'])

        if tobj.get('dest-dir'):
            gf.dest_dir  = os.path.join(self._proj_root, tobj['dest-dir'], self._comp['id'])
            gf.fh.write('COPY_PATH   = %s\n' % gf.dest_dir)


    def _gen_dest_targ(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the dest target build.
        """
        tt       = gf.targ['type']
        targ     = gf.targ
        tobj     = self._types[tt]
        so_str   = ''
        lib_str  = ''
        incl_str = ''

        if targ.get('depends') and self._item_list(targ['depends'].get('internal-shared-libs'), self._comp['id']):
            so_str = ' $(SO_PATHS)'

        if self._has_libs(gf.targ):
            lib_str = ' $(LIBS)'

        if targ.get('incl-paths'):
            incl_str = ' $(INCS)'

        if tt == 'lib':
            gf.fh.write('\n$(DEST): $(SOURCE_OBJS)\n')
            gf.fh.write('\t$(LINK_CMD) $(LINK_FLAGS) $(LINK_FLAGS_EXTRA) $^\n')
            gf.fh.write('\t$(LINK_INDEXER) $(DEST)\n')

        elif tt == 'exe':
            gf.fh.write('\n$(DEST): $(SOURCE_OBJS)\n')
            gf.fh.write('\t$(CPP_CMD) -o $(DEST) $(SOURCE_OBJS) $(LINK_FLAGS) $(LINK_FLAGS_EXTRA)%s%s%s\n' % (
                so_str, lib_str, incl_str))

        elif tt == 'so':
            gf.fh.write('\n$(DEST):\n')
            gf.fh.write('\t$(CPP_CMD) -shared -o $(DEST) $(SOURCE_OBJS)\n')

        elif tt == 'pyd':
            gf.fh.write('\n$(DEST): clean $(SOURCE_OBJS)\n')

            if self._windows():
                pydll = None

                if targ.get('depends'):
                    pydll = self._item_list(targ['depends'].get('python-dll'))

                if not pydll or len(pydll) != 1:
                    raise Exception('%s: property [python-dll] is required for MINGW64 windows compiles!' % (self._name))

                pythondll = pydll[0]

                realPath  = self._fixPath(os.path.join(self._proj_root, pythondll), '/')
                pydll     = os.path.split(pythondll)[1]
                pyname    = os.path.splitext(pydll)[0]
                pydef     = '%s.def' % os.path.splitext(pydll)[0]
                pylib     = 'lib%s.a' % os.path.splitext(pydll)[0]

                if pyname == '':
                    raise Exception('%s: property [python.dll] has an invalid value! (%s)' % (self._name, pythondll))

                gf.fh.write('\tgendef %s\n' % realPath)
                gf.fh.write('\tdlltool --dllname %s --def %s --output-lib %s\n' % (pydll, pydef, pylib))
                gf.fh.write('\t$(CPP_CMD) -shared -o $(DEST) $(SOURCE_OBJS)%s %s\n' % (lib_str, pylib))
            else:
                gf.fh.write('\t$(CPP_CMD) -shared -o $(DEST) $(SOURCE_OBJS)%s\n' % (lib_str))

        if tobj.get('dest-dir'):
            if self._windows():
                gf.fh.write('\t$(OS_NOT_EXISTS) $(COPY_PATH) $(OS_MKDIR) $(COPY_PATH)\n')
            else:
                gf.fh.write('\t$(OS_MKDIR) $(COPY_PATH)\n')

            gf.fh.write('\t$(OS_COPY) $(DEST) $(COPY_PATH)\n')
            gf.fh.write('\t$(OS_DEL) $(DEST)\n')

        if tt != 'so':
            if targ['src-paths'].get('cpp'):
                gf.fh.write('\n%.o: %.cpp\n')
                gf.fh.write('\t$(CPP_CMD) $(CPP_FLAGS) $(CPP_FLAGS_EXTRA)%s $< -o $@\n' % (incl_str))

            if targ['src-paths'].get('cc'):
                gf.fh.write('\n%.o: %.c\n')
                gf.fh.write('\t$(CC_CMD) $(CC_FLAGS) $(CC_FLAGS_EXTRA)%s $< -o $@\n' % (incl_str))


    def _gen_clean(self, gf: 'Generator.GeneratedFile', src_list: list) -> None:
        """
        Generate the clean.
        """
        tt = gf.targ['type']

        gf.fh.write('\n.PHONY: clean\n')
        gf.fh.write('clean:\n')

        if tt in ('exe', 'pyd'):
            gf.fh.write('\t$(OS_DEL) $(TARG_NAME)$(TARG_EXT)\n')
            gf.fh.write('\t$(OS_DEL) $(TARG_NAME)_debug$(TARG_EXT)\n')
        else:
            gf.fh.write('\t$(OS_DEL) $(TARG_NAME)$(TARG_COMP)$(ARCH_SIZE)$(TARG_EXT)\n')
            gf.fh.write('\t$(OS_DEL) $(TARG_NAME)$(TARG_COMP)$(ARCH_SIZE)_debug$(TARG_EXT)\n')

        for x in src_list:
            gf.fh.write('\t$(OS_DEL) %s%s*%s\n' % (self._os_sep(x), os.path.sep, self._comp['exts']['obj']))


    def _gen_release_debug(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the release/debug targets.
        """
        tt = gf.targ['type']

        gf.fh.write('\n.PHONY: release\n')
        gf.fh.write('release: DEBUG_FLAG =\n')

        if gf.targ['src-paths'].get('cpp'):
            gf.fh.write('release: CPP_FLAGS  = %s\n' % (self._comp['flags']['compile']['cpp']['release'][tt]))

        if gf.targ['src-paths'].get('cc'):
            gf.fh.write('release: CC_FLAGS   = %s\n' % (self._comp['flags']['compile']['cc']['release'][tt]))

        gf.fh.write('release: LINK_FLAGS = %s\n' % (self._comp['flags']['link']['release'][tt]))

        if tt in ('exe', 'pyd'):
            gf.fh.write('release: DEST       = $(TARG_NAME)$(TARG_EXT)\n')
        else:
            gf.fh.write('release: DEST       = $(TARG_NAME)$(TARG_COMP)$(ARCH_SIZE)$(TARG_EXT)\n')

        gf.fh.write('release: $(DEST)\n\n')

        gf.fh.write('.PHONY: debug\n')

        if gf.targ['src-paths'].get('cpp'):
            gf.fh.write('debug: CPP_FLAGS  = %s\n' % (self._comp['flags']['compile']['cpp']['debug'][tt]))

        if gf.targ['src-paths'].get('cc'):
            gf.fh.write('debug: CC_FLAGS   = %s\n' % (self._comp['flags']['compile']['cc']['debug'][tt]))
        gf.fh.write('debug: LINK_FLAGS = %s\n' % (self._comp['flags']['link']['debug'][tt]))

        if tt in ('exe', 'pyd'):
            gf.fh.write('debug: DEST       = $(TARG_NAME)$(DEBUG_FLAG)$(TARG_EXT)\n')
        else:
            gf.fh.write('debug: DEST       = $(TARG_NAME)$(TARG_COMP)$(ARCH_SIZE)$(DEBUG_FLAG)$(TARG_EXT)\n')
        gf.fh.write('debug: $(DEST)\n')


    def _gen_source_paths(self, gf: 'Generator.GeneratedFile') -> list:
        """
        Generate the source paths.
        """
        tt  = gf.targ['type']
        res = []

        gf.fh.write('\n# Source Objects\n')
        gf.fh.write('SOURCE_OBJS=')

        cpp_paths = gf.targ['src-paths'].get('cpp') or []
        cc_paths  = gf.targ['src-paths'].get('cc') or []

        for x in cpp_paths:
            p = self._os_sep(os.path.join(self._proj_root, self._templ(x)), '/')

            if tt == 'so':
                if p.endswith('/*'):
                    p = p[:-2]
                gf.fh.write('\\\n %s/*%s' % (p, self._comp['exts']['obj']))
                continue

            if p.endswith('*'):
                gf.fh.write('\\\n $(patsubst %%.cpp,%%%s,$(wildcard %s.cpp))' % (self._comp['exts']['obj'], p))
            else:
                gf.fh.write('\\\n %s%s' % (p, self._comp['exts']['obj']))

            if os.path.split(p)[0] not in res:
                res.append(os.path.split(p)[0])

        for x in cc_paths:
            p = self._os_sep(os.path.join(self._proj_root, self._templ(x)), '/')

            if tt == 'so':
                if p.endswith('/*'):
                    p = p[:-2]
                gf.fh.write('\\\n %s/*%s' % (p, self._comp['exts']['obj']))
                continue

            if p.endswith('*'):
                gf.fh.write('\\\n $(patsubst %%.c,%%%s,$(wildcard %s.c))' % (self._comp['exts']['obj'], p))
            else:
                gf.fh.write('\\\n %s%s' % (p, self._comp['exts']['obj']))

            if os.path.split(p)[0] not in res:
                res.append(os.path.split(p)[0])

        gf.fh.write('\n')

        return res


    def _gen_library_paths(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the external library paths.
        """
        if not self._has_libs(gf.targ):
            return

        gf.fh.write('\n# Libraries\n')
        gf.fh.write('LIBS=')

        targ = gf.targ

        for x in self._item_list(targ['depends'].get('internal-shared-libs'), self._comp['id']):
            p  = self._get_library_no_path(x)
            gf.fh.write('\\\n "-l%s$(TARG_COMP)$(ARCH_SIZE)$(DEBUG_FLAG)"' % p)

        for x in self._item_list(targ['depends'].get('internal-static-libs'), self._comp['id']):
            p  = self._get_library_path(x, False)
            gf.fh.write('\\\n "%s$(TARG_COMP)$(ARCH_SIZE)$(DEBUG_FLAG)$(TARG_EXT_LIB)"' % p)

        for x in self._item_list(targ['depends'].get('external-shared-libs'), self._comp['id']):
            gf.fh.write('\\\n "-l%s"' % x)

        for x in self._item_list(targ['depends'].get('external-static-libs'), self._comp['id']):
            p  = self._get_library_path(x, True)
            gf.fh.write('\\\n "%s"' % p)

        gf.fh.write('\n')


    def _gen_so_paths(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the paths to any internal shared object is required.
        """
        if gf.targ['type'] != 'exe' or not gf.targ.get('depends'):
            return

        so_list = self._item_list(gf.targ['depends'].get('internal-shared-libs'), self._comp['id'])

        if not so_list:
            return

        dupes = []

        gf.fh.write('\n# Internal shared object library paths\n')
        gf.fh.write('SO_PATHS =')

        for ilib in so_list:
            if ilib in dupes:
                continue

            pth  = self._get_library_path(ilib, True)
            pdir = '-L %s/%s' % ('/'.join(pth.split('/')[0:-1]), self._comp['id'])

            if pdir in dupes:
                continue

            gf.fh.write(' %s' % pdir)
            dupes.append(pdir)

        gf.fh.write('\n')


    def _gen_incl_paths(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generte all the include paths.
        """
        if not gf.targ.get('incl-paths'):
            return

        gf.fh.write('\n# Include Paths\n')
        gf.fh.write('INCS = -I.')

        comp_flag = '%s|' % self._comp['id']

        for x in gf.targ.get('incl-paths'):
            if x.find('|') >= 0:
                if x.startswith(comp_flag):
                    x = x[len(comp_flag):]
                else:
                    continue

            p  = self._os_sep(os.path.join(self._proj_root, self._templ(x)), '/')
            gf.fh.write('\\\n -I%s' % p)

        gf.fh.write('\n')


    def _get_library_no_path(self, pth: str):
        p = pth.split('/')[-1]

        return p


    def _get_library_path(self, pth: str, ext: bool):
        p = self._os_sep(self._templ(pth), '/')

        if p.startswith('/'):
            return p

        # p = self._fixPath(os.path.join(genProps['basedir'], p), '/')
        p = self._os_sep(os.path.join(self._proj_root, p), '/')

        if ext:
            return p

        x = p.split('/')


        if len(x) == 1:
            return '%s/%s' % (self._comp['id'], x)

        return '/'.join(x[0:-1] + [self._comp['id']] + [x[-1]])


    def _has_libs(self, targ: dict) -> bool:
        """
        Check if there are libraries to add.
        """
        if not targ.get('depends'):
            return False

        if self._item_list(targ['depends'].get('internal-static-libs'), self._comp['id']):
            return True

        if self._item_list(targ['depends'].get('internal-shared-libs'), self._comp['id']):
            return True

        if self._item_list(targ['depends'].get('external-static-libs'), self._comp['id']):
            return True

        if self._item_list(targ['depends'].get('external-shared-libs'), self._comp['id']):
            return True

        return False
