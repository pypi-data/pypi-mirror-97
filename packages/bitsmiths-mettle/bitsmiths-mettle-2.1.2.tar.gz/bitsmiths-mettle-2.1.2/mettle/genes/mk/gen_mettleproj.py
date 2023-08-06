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


class GenMettleProj(Generator):

    METTLE_TYPES = [
        'db',
        'braze',
        'mk',
    ]

    TYPE_DESCR = {
        'db'    : 'database proejct',
        'braze' : 'braze project',
        'mk'    : 'makefile project',
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
        return 'MettleProj'


    def type_descr(self, type_id: str) -> str:
        """
        Overload.
        """
        return self.TYPE_DESCR[type_id]


    def _makefile_types(self) -> list:
        """
        Overload.
        """
        return self.METTLE_TYPES


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

        if not targ.get('projects'):
            raise Exception('%s has no "projects" items : [%s]' % (gf.targ_id, str(targ)))

        self._gen_header(gf, 'mettle.genes.mk.gen_mettleproj')
        self._gen_std_vars(gf)
        self._gen_compiler_vars(gf)
        self._gen_proj_src(gf)

        self._gen_usage(gf)
        self._gen_release_debug_clean(gf)
        self._gen_make_targs(gf)

        self._makefile_close(gf)


    def _gen_compiler_vars(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the mettle proj specific vars.
        """
        if gf.targ.get('gen-cmd'):
            gen = gf.targ.get('gen-cmd')
        else:
            gen = 'mettle-genes'

        gf.fh.write('GEN_MTL       = %s\n' % gen)
        gf.fh.write('CLEAN_FLAG    = \n')


    def _gen_make_targs(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate all the project targets
        """
        idx = 1

        for pitem in gf.targ['projects']:
            p = self._os_sep(os.path.join(self._proj_root, self._templ(pitem)), '/')
            gf.fh.write('\nPROJ_%.2d: %s\n' % (idx, p))
            gf.fh.write('\t$(GEN_MTL) $(CLEAN_FLAG) $<\n')
            idx += 1

        gf.fh.write('\n')


    def _gen_release_debug_clean(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the relese, debug, and clean targets.
        """
        gf.fh.write('\n.PHONY: release\n')
        gf.fh.write('release: $(PROJECT_SOURCES)\n')

        gf.fh.write('\n.PHONY: debug\n')
        gf.fh.write('debug: $(PROJECT_SOURCES)\n')

        gf.fh.write('\n.PHONY: clean\n')
        gf.fh.write('clean: CLEAN_FLAG=--clean\n')
        gf.fh.write('clean: $(PROJECT_SOURCES)\n')


    def _gen_proj_src(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generates all the project sources.
        """
        idx = 1

        gf.fh.write('\n# Project Sources')
        gf.fh.write('\nPROJECT_SOURCES=')

        for ptiem in gf.targ['projects']:
            gf.fh.write('\\\n PROJ_%.2d' % (idx))
            idx += 1

        gf.fh.write('\n')
