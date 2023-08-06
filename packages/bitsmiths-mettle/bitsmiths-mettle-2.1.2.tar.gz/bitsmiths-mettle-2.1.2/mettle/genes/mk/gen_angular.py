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

from .generator import Generator


class GenAngular(Generator):

    ANGULAR_TYPES = [
        'lib',
    ]

    TYPE_DESCR = {
        'lib'   : 'angular library',
    }


    def __init__(self):
        """
        Constructor.
        """
        Generator.__init__(self)


    def name(self) -> str:
        """
        Overload.
        """
        return 'Angular'


    def type_descr(self, type_id: str) -> str:
        """
        Overload.
        """
        return self.TYPE_DESCR[type_id]


    def _makefile_types(self) -> list:
        """
        Overload.
        """
        return self.ANGULAR_TYPES


    def generate_makefiles(self, gen_info: dict):
        """
        Overload.
        """
        Generator.generate_makefiles(self, gen_info)

        clean = gen_info.get('clean')

        for targ in self._targets:

            if clean:
                self._clean_target(targ)
                continue

            if self._skip(targ):
                continue

            self._gen_target(targ)


    def _gen_target(self, targ: dict) -> None:
        """
        Generate the target item make file.

        :param targ: The target object to generate a make file for.
        """
        gf = self._makefile_open(targ)

        if not targ.get('version'):
            raise Exception('%s has no "version": [%s]' % (gf.targ_id, str(targ)))

        if not targ.get('project-dir'):
            raise Exception('%s has no "project-dir": [%s]' % (gf.targ_id, str(targ)))

        if not targ.get('node-modules'):
            raise Exception('%s has no "node-modules": [%s]' % (gf.targ_id, str(targ)))

        targ['version'] = self._templ(targ['version'])

        self._gen_header(gf, 'mettle.genes.mk.gen_angular')
        self._gen_std_vars(gf)
        self._gen_compiler_vars(gf)

        self._gen_usage(gf)
        self._gen_release_debug_clean(gf)
        self._gen_make_targs(gf)

        self._makefile_close(gf)


    def _gen_compiler_vars(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the angualr specific vars.
        """
        tt    = gf.targ['type']
        targ  = gf.targ
        tobj  = self._types[tt]

        gf.fh.write('# Node Variables\n')
        gf.fh.write('NPM_CC       = npm\n')
        gf.fh.write('NODE_MOD_CC  = yarn\n')
        gf.fh.write('NPM_TARG     = _var_\n')
        gf.fh.write('DEST         = _var_\n')
        gf.fh.write('DEBUG_FLAG   = _var_\n')

        gf.fh.write('\n# Target Descriptors\n')

        gf.fh.write('TARGET_NAME  = %s\n' % targ['name'])
        gf.fh.write('TARGET_EXT   = .tgz\n')
        gf.fh.write('TARGET_VER   = %s\n' % targ['version'])
        gf.fh.write('PROJ_DIR     = %s\n' % os.path.join(self._proj_root, self._os_sep(self._templ(targ['project-dir']))))
        gf.fh.write('DIST_DIR     = %s\n' % os.path.join(self._proj_root, self._os_sep(targ['project-dir']), 'dist', targ['name']))  # noqa
        gf.fh.write('SHR_NM_DIR   = %s\n' % os.path.join(self._proj_root, self._os_sep(self._templ(targ['node-modules']))))

        if tobj.get('dest-dir'):
            gf.dest_dir  = os.path.join(self._proj_root, tobj['dest-dir'])
            gf.fh.write('COPY_PATH    = %s\n' % gf.dest_dir)


    def _gen_release_debug_clean(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the release, debug, and clean targets.
        """
        tt   = gf.targ['type']
        targ = gf.targ
        tobj = self._types[tt]

        gf.fh.write('\n.PHONY: release\n')
        gf.fh.write('release: DEBUG_FLAG = \n')
        gf.fh.write('release: NPM_TARG   = run build %s\n' % (targ['name']))
        gf.fh.write('release: DEST       = $(TARGET_NAME)-$(TARGET_VER)$(TARGET_EXT)\n')
        gf.fh.write('release: $(DEST)\n')

        gf.fh.write('\n.PHONY: debug\n')
        gf.fh.write('debug: DEBUG_FLAG = _debug\n')
        gf.fh.write('debug: NPM_TARG   = run build_debug %s\n' % (targ['name']))
        gf.fh.write('debug: DEST       = $(TARGET_NAME)-$(TARGET_VER)$(TARGET_EXT)\n')
        gf.fh.write('debug: $(DEST)\n')

        gf.fh.write('\n.PHONY: clean\n')
        gf.fh.write('clean:\n')
        gf.fh.write('\t$(OS_DEL) $(TARGET_NAME)-*$(TARGET_EXT)\n')
        gf.fh.write('\t$(OS_DEL) $(TARGET_NAME)_debug-*$(TARGET_EXT)\n')

        if tobj.get('dest-dir'):
            gf.fh.write('\t$(OS_DEL) $(COPY_PATH)$(OS_DIR_SEP)$(TARGET_NAME)-*$(TARGET_EXT)\n')
            gf.fh.write('\t$(OS_DEL) $(COPY_PATH)$(OS_DIR_SEP)$(TARGET_NAME)_debug-*$(TARGET_EXT)\n')


    def _gen_make_targs(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the build targets build.
        """
        tt   = gf.targ['type']
        tobj = self._types[tt]

        gf.fh.write('\n# The main build target\n')
        gf.fh.write('$(DEST): $(SHR_NM_DIR)\n')
        gf.fh.write('\tcd $(PROJ_DIR) && $(NPM_CC) $(NPM_TARG)\n')
        gf.fh.write('\tnpm pack $(DIST_DIR)\n')

        if tobj.get('dest-dir'):
            gf.fh.write('\t$(OS_COPY) $(DEST) $(COPY_PATH)$(OS_DIR_SEP)$(DEST)\n')

        gf.fh.write('\n# Install node_modules if missing\n')
        gf.fh.write('.PHONY: $(SHR_NM_DIR)\n')
        gf.fh.write('$(SHR_NM_DIR):\n')
        gf.fh.write('\tcd $(PROJ_DIR) && $(NODE_MOD_CC) install\n')
