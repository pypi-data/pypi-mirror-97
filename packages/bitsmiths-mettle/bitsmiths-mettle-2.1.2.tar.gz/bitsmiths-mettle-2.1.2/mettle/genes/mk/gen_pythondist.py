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


class GenPythonDist(Generator):

    PYDIST_TYPES = [
        'dist',
    ]

    TYPE_DESCR = {
        'dist'   : 'python distributal',
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
        return 'PythonDist'


    def type_descr(self, type_id: str) -> str:
        """
        Overload.
        """
        return self.TYPE_DESCR[type_id]


    def _makefile_types(self) -> list:
        """
        Overload.
        """
        return self.PYDIST_TYPES


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

        self._gen_header(gf, 'mettle.genes.mk.gen_angular')
        self._gen_std_vars(gf)
        self._gen_compiler_vars(gf)

        self._gen_usage(gf)
        self._gen_release_debug_clean(gf)

        self._makefile_close(gf)


    def _gen_compiler_vars(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the angualr specific vars.
        """
        targ  = gf.targ

        gf.fh.write('# Node Variables\n')
        gf.fh.write('PY_CC    = python\n')

        gf.fh.write('\n# Target Descriptors\n')

        gf.fh.write('TARGET_NAME  = %s\n' % targ['name'])
        gf.fh.write('PROJ_PATH    = %s\n' % self._os_sep(os.path.join(self._proj_root, targ['path'])))


    def _gen_release_debug_clean(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the release, debug, and clean targets.
        """
        tt   = gf.targ['type']
        tobj = self._types[tt]

        gf.fh.write('\n.PHONY: release\n')
        gf.fh.write('release:\n')
        gf.fh.write('\tcd $(PROJ_PATH) && $(PY_CC) -m build\n')

        if tobj.get('dest-dir'):
            gf.fh.write('\tcd $(PROJ_PATH) && $(OS_COPY) dist$(OS_DIR_SEP)/$(TARGET_NAME)-* $(COPY_PATH)$(OS_DIR_SEP)$(DEST)\n')

        gf.fh.write('\n.PHONY: debug\n')
        gf.fh.write('debug:\n')
        gf.fh.write('\tcd $(PROJ_PATH) && $(PY_CC) -m build\n')

        if tobj.get('dest-dir'):
            gf.fh.write('\tcd $(PROJ_PATH) && $(OS_COPY) dist$(OS_DIR_SEP)/$(TARGET_NAME)-* $(COPY_PATH)$(OS_DIR_SEP)$(DEST)\n')

        gf.fh.write('\n.PHONY: clean\n')
        gf.fh.write('clean:\n')
        gf.fh.write('\tcd $(PROJ_PATH) && $(OS_RMDIR) dist\n')
        gf.fh.write('\tcd $(PROJ_PATH) && $(OS_RMDIR) build\n')
        gf.fh.write('\tcd $(PROJ_PATH) && $(OS_RMDIR) *.egg-info\n')

        if tobj.get('dest-dir'):
            gf.fh.write('\tcd $(PROJ_PATH) && $(OS_DEL) $(COPY_PATH)$(OS_DIR_SEP)$(TARGET_NAME)-*\n')
