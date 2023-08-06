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
import multiprocessing

from .generator import Generator


class GenMkSolution(Generator):

    SLN_TYPES = {
        'sln'  : 'solution',
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
        return 'MkSolution'


    def type_descr(self, type_id: str) -> str:
        """
        Overload.
        """
        return 'solution makefile'


    def _makefile_types(self) -> list:
        """
        Overload.
        """
        return self.SLN_TYPES.keys()


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

        if not targ.get('order'):
            raise Exception('%s has no "order" items : [%s]' % (gf.targ_id, str(targ)))

        self._gen_header(gf, 'mettle.genes.mk.gen_mksln')
        self._gen_std_vars(gf)
        self._gen_compiler_vars(gf)

        targs = self._gen_target_list(gf)

        self._gen_usage(gf)
        self._gen_list(gf, targs)
        self._gen_release_targs(gf, targs)
        self._gen_debug_targs(gf, targs)
        self._gen_clean_targs(gf, targs)
        self._gen_make_targs(gf, targs)

        self._makefile_close(gf)


    def _gen_compiler_vars(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Overload.
        """
        cnt = max(1, int(multiprocessing.cpu_count() - 1))

        gf.fh.write('# Solution Variables\n')
        gf.fh.write('GMAKE_FLAG       = _na_\n')
        gf.fh.write('CONCURRENT_MAKES = %d\n' % cnt)
        gf.fh.write('MAKE_FLAG        = -j $(CONCURRENT_MAKES)\n')
        gf.fh.write('PYCMD            = python\n')
        gf.fh.write('LOG_PROG         = @echo ----------------- $(3): $(2) \\($(1)\\)\n')


    def _gen_target_list(self, gf: 'Generator.GeneratedFile') -> list:
        """
        Generates all the targets and returns the list of them by target type.
        """
        res  = []
        targ = gf.targ
        proj = self._gen_info['proj']

        for titem in targ['order']:
            gene = proj.generators.get(titem)

            if not gene:
                logging.warning('%s order item [%s] not a known generator!' % (gf.targ_id, titem))
                continue

            if not gene._gened_files:
                logging.info(' - Generator [%s] has not generated makefiles, skipping' % (gene.name()))

            idx = 1
            tt  = {
                'gene'  : gene,
                'name'  : 'TARG_%s_LIST' % gene.name(),
                'targs' : []
            }

            res.append(tt)

            gf.fh.write('\n# %s targets' % (gene.name()))
            gf.fh.write('\n%s=' % tt['name'])

            for ggf in gene._gened_files:
                targ_id = '%s_%.2d_%s_%s' % (gene.name(), idx, ggf.targ['type'].upper(), ggf.targ['name'].upper())

                gf.fh.write('\\\n %s' % (targ_id))

                tt['targs'].append({
                    'targ_id' : targ_id,
                    'path'    : ggf.full_path,
                    'fname'   : ggf.fname,
                    'idx'     : idx,
                    'descr'   : ggf.targ['descr'],
                })

                idx += 1

            gf.fh.write('\n')

        return res


    def _gen_make_targs(self, gf: 'Generator.GeneratedFile', targs: list) -> None:
        """
        Generate all the actual make file targets.
        """
        gf.fh.write('\n# -- All the make file targets --\n')

        for titem in targs:
            gf.fh.write('\n# -- %s make files --\n' % (titem['gene'].name()))

            for tt in titem['targs']:
                gf.fh.write('\n%s: %s' % (tt['targ_id'], tt['path']))
                gf.fh.write('\n\t@echo')
                gf.fh.write('\n\t$(call LOG_PROG,$(GMAKE_FLAG),Making,%s)' % tt['descr'])
                gf.fh.write('\n\t$(MAKE) -f %s -C $(<D) $(GMAKE_FLAG)\n' % tt['fname'])


    def _gen_clean_targs(self, gf: 'Generator.GeneratedFile', targs: list) -> None:
        """
        Generate all the clean targets.
        """
        gf.fh.write('\n.PHONY: clean')
        gf.fh.write('\nclean: GMAKE_FLAG:=clean')
        gf.fh.write('\nclean:')

        for tt in targs:
            gf.fh.write(' $(%s)' % (tt['name']))

        gf.fh.write('\n')

        for tt in targs:
            tid = '%s_clean' % (tt['gene'].name())
            gf.fh.write('\n.PHONY: %s' % (tid))
            gf.fh.write('\n%s: GMAKE_FLAG:=clean' % (tid))
            gf.fh.write('\n%s: $(%s)\n' % (tid, tt['name']))


    def _gen_debug_targs(self, gf: 'Generator.GeneratedFile', targs: list) -> None:
        """
        Generate all the debug targets.
        """
        gf.fh.write('\n.PHONY: debug')
        gf.fh.write('\ndebug: GMAKE_FLAG:=debug')
        gf.fh.write('\ndebug:')

        for tt in targs:
            gf.fh.write(' $(%s)' % (tt['name']))

        gf.fh.write('\n')

        for tt in targs:
            tid = '%s_debug' % (tt['gene'].name())
            gf.fh.write('\n.PHONY: %s' % (tid))
            gf.fh.write('\n%s: GMAKE_FLAG:=debug' % (tid))
            gf.fh.write('\n%s: $(%s)\n' % (tid, tt['name']))


    def _gen_release_targs(self, gf: 'Generator.GeneratedFile', targs: list) -> None:
        """
        Generate all the release targets.
        """
        gf.fh.write('\n.PHONY: release')
        gf.fh.write('\nrelease: GMAKE_FLAG:=release')
        gf.fh.write('\nrelease:')

        for tt in targs:
            gf.fh.write(' $(%s)' % (tt['name']))

        gf.fh.write('\n')

        for tt in targs:
            tid = '%s_release' % (tt['gene'].name())
            gf.fh.write('\n.PHONY: %s' % (tid))
            gf.fh.write('\n%s: GMAKE_FLAG:=release' % (tid))
            gf.fh.write('\n%s: $(%s)\n' % (tid, tt['name']))


    def _gen_list(self, gf: 'Generator.GeneratedFile', targs: list) -> None:
        """
        Gen the list target which shows all the targets!
        """
        gf.fh.write('\n.PHONY: help')
        gf.fh.write('\nlist:')

        for tt in targs:
            gf.fh.write('\n\t@echo')
            gf.fh.write('\n\t@echo %s_release' % (tt['gene'].name()))
            gf.fh.write('\n\t@echo %s_debug' % (tt['gene'].name()))
            gf.fh.write('\n\t@echo %s_clean' % (tt['gene'].name()))

            for item in tt['targs']:
                gf.fh.write('\n\t@echo    - %s' % item['targ_id'])

        gf.fh.write('\n\t@echo\n')


    def _gen_usage(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Virtual method to generate the make fiel specific usage.
        """
        td = self.type_descr(gf.targ['type'])

        gf.fh.write('\n.PHONY: help\n')
        gf.fh.write('help:\n')
        gf.fh.write('\t@echo\n')

        if td:
            gf.fh.write('\t@echo "  %s : %s"\n' % (gf.targ['descr'], td))
        else:
            gf.fh.write('\t@echo "  %s"\n' % (gf.targ['descr']))

        gf.fh.write('\t@echo\n')
        gf.fh.write('\t@echo "  Usage: make [target]"\n')
        gf.fh.write('\t@echo "  ----------------------------------------"\n')
        gf.fh.write('\t@echo "  release  : build entire solution for release"\n')
        gf.fh.write('\t@echo "  debug    : build entire solution for debug"\n')
        gf.fh.write('\t@echo "  list     : list all the language targets"\n')
        gf.fh.write('\t@echo "  clean    : clean all solution binaries"\n')
        gf.fh.write('\t@echo "  help     : this help"\n')
        gf.fh.write('\t@echo\n')
