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
import time
import os
import os.path
import shutil  # hmm... might have to find a windows replacement if we ever use that shit OS again for some reason
import sys

from string import Template

from mettle.genes import MkProject


class Generator:

    OS_SEPERATORS = [ '/', '\\', '|' ]

    class GeneratedFile:
        def __init__(self):
            self.targ      = None
            self.targ_id   = ''
            self.fname     = ''
            self.dir       = ''
            self.full_path = ''
            self.targ_path = ''
            self.dest_dir  = None
            self.fh        = None


    def __init__(self):
        self.enabled      = True
        self._types       = {}
        self._compilers   = {}
        self._items       = []
        self._subst       = {}
        self._gened_files = []
        self._gen_info    = None


    def name(self) -> str:
        return 'Base Target'


    def type_descr(self, type_id: str) -> str:
        """
        Pure virtual method to get the type description.
        """
        raise Exception('type_descr() not implemented')


    def _makefile_types(self) -> list:
        """
        Pure virtual method that gets the list of make file types we should expect.
        """
        raise Exception('_makefile_types() not implemented')


    def init(self, proj: 'MkProject', enabled: bool, types: dict, compilers: dict, targets: list, extern: str):
        """
        Initialize the make file generator.

        :param proj_root: The makefile project
        :param enabled: If this generator is enabled or not.
        :param types: A list the type configurations, dest directorys, make file dirs and names.
        :param compilers: An optional list of which compilers targets to use of different operating systems.
        :param targets: The list of targets to generate for.
        :param extern: An optional extern folder.
        """
        self.enabled    = enabled
        self._proj_root = proj.proj_root
        self._types     = types
        self._compilers = compilers
        self._targets   = targets
        self._extern    = extern

        if self.enabled:
            self._init_target_types(self._makefile_types())

        self._subst['proj_root']   = self._proj_root
        self._subst['lang_targ']   = self.name()
        self._subst['os_name']     = os.name
        self._subst['os_platform'] = os.sys.platform
        self._subst['path']        = None

        for key, val in proj.proj_ver.items():
            self._subst['ver_%s' % key] = val

        for targ in self._targets:
            targ['path'] = self._os_sep(targ['path'])

        if extern:
            self._subst['extern'] = self._os_sep(self._templ(extern))


    def initialize_generation(self, gen_info: dict):
        pass


    def finalize_generation(self, gen_info: dict):
        pass


    def generate_makefiles(self, gen_info: dict):
        """
        Virtual method to be overloaded that generates the make files.
        """
        self._gen_info = gen_info


    def clean(self, gen_info: dict):
        """
        Clean all the make file from the system.
        """
        pass


    def _windows(self) -> bool:
        """
        Check if we are running on windows or not.
        """
        return sys.platform.startswith('win')


    def _skip(self, targ: dict) -> bool:
        """
        Check if we should skip this target for some reason.
        """
        if targ.get('skip-if!'):
            chk = self._os_sep(self._templ(targ['skip-if!']))

            if not os.path.exists(chk):
                logging.warning('Skipping target [%s] because path not found [%s]' % (targ['name'], chk))
                return True

        return False


    def _item_list(self, items: list, for_compiler: str = None) -> list:
        """
        Returns a list of the times, and also checks for a compiler specific flag if specified.

        :param items: The items to get a list for.
        :parma for_compiler: The compiler flag to check for.
        :returns: Always a list, even its empty.
        """
        if items is None:
            return []

        if not items:
            return items

        if for_compiler:

            comp_flag = '%s|' % for_compiler
            idx       = 0

            while idx < len(items):
                item = items[idx]
                if item.find('|') >= 0:
                    if item.startswith(comp_flag):
                        items[idx] = item[len(comp_flag):]
                    else:
                        items.pop(idx)
                        continue
                idx += 1

        return items


    def _clean_target(self, targ: dict) -> None:
        """
        Clean the make and its target directory.
        """
        gf = self._makefile_open(targ, False)

        if gf.dir == gf.targ_path:
            if os.path.exists(gf.full_path):
                logging.info(' - Removing makefile [%s]' % gf.full_path)
                os.remove(gf.full_path)
                return

        if os.path.exists(gf.dir):
            logging.info(' - Removing make directory [%s]' % gf.dir)
            shutil.rmtree(gf.dir)


    def _makefile_open(self, targ: dict, open_fh: bool = True) -> 'Generator.GeneratedFile':
        """
        Open the the makefile handle and the creates the needed directories as well.

        :param targ: The target object.
        :returns: The generated file object with an open file handle.
        """
        self._subst['path'] = self._templ(targ['path'])
        targ_id             = '[%s] target [%d]' % (self.name(), len(self._gened_files))

        if not targ.get('name'):
            raise Exception('%s does not specify a "name"! : [%s]' % (targ_id, str(targ)))

        if not targ.get('descr'):
            raise Exception('%s does not specify a "descr"! : [%s]' % (targ_id, str(targ)))

        if not targ.get('type'):
            raise Exception('%s does not specify a "type"! : [%s]' % (targ_id, str(targ)))

        tobj = self._types.get(targ['type'])

        if not tobj:
            raise Exception('%s specifies an unexpected type! : [%s]' % (targ_id, str(targ)))

        res = self.GeneratedFile()

        res.targ      = targ
        res.targ_id   = targ_id
        res.targ_path = os.path.join(self._proj_root, targ['path'])
        res.fname     = tobj['makefile-name']

        if not os.path.exists(res.targ_path):
            raise Exception('%s path not found [%s]! -> [%s]' % (targ_id, res.targ_path, str(targ)))

        if not os.path.isdir(res.targ_path):
            raise Exception('%s path is not a directory [%s]! -> [%s]' % (targ_id, res.targ_path, str(targ)))

        if tobj.get('makefile-dir'):
            res.dir = os.path.join(res.targ_path, tobj['makefile-dir'])
        else:
            res.dir = res.targ_path

        res.full_path = os.path.join(res.dir, res.fname)

        if open_fh:
            if not os.path.exists(res.dir):
                logging.info('%s creating make file directory [%s]' % (targ_id, res.dir))

                os.makedirs(res.dir)

            res.fh = open(res.full_path, 'wt')

            self._gened_files.append(res)

            logging.info('%s generated makefile: %s' % (targ_id, res.full_path))

        return res


    def _makefile_close(self, gf: 'Generator.GeneratedFile') -> None:
        if gf.fh is not None:
            gf.fh.close()

        self._subst['path'] = None


    def _init_target_types(self, type_list: list) -> None:
        """
        Intialize the target destintion types.

        :param type_list: List of target types to expect.
        """
        for tid in type_list:
            tobj = None

            if tid in self._types:
                tobj = self._types[tid]
                logging.warning('Makefile type [%s:%s] not defined in project!' % (self.name(), tid))

            if tobj is None:
                tobj = {}
                self._types[tid] = tobj

            if tobj.get('dest-dir'):
                tobj['dest-dir'] = self._os_sep(tobj['dest-dir'])
            else:
                tobj['dest-dir'] = None

            if not tobj.get('makefile-name'):
                tobj['makefile-name'] = 'makefile'

            if tobj.get('makefile-dir'):
                tobj['makefile-dir'] = self._os_sep(tobj['makefile-dir'])


    def _os_sep(self, pth: str, sep: str = None) -> str:
        """
        Returns the pth in the save operating style.

        :param pth: The pth to convert.
        :param sep: Optionally define the seperator
        :returns: The native os path.
        """
        for x in self.OS_SEPERATORS:
            pth = pth.replace(x, sep or os.sep)

        return pth


    def _templ(self, val: str) -> str:
        """
        Templates the value string with the subst dictionary.

        :param val: The string to tempalte.
        :returns: The result.
        """
        return Template(val).substitute(self._subst)


    def _gen_header(self, gf: 'Generator.GeneratedFile', src: str) -> None:
        """
        Generates the header message
        """
        message = '# This file was generated by %s [ver %s] on %s\n#\n\n' % (
            src, self._gen_info['version'], time.asctime())

        gf.fh.write(message)


    def _gen_trailers(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generate the trailers if there are any.
        """
        pass


    def _gen_std_vars(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Generates the standard vars all make files have.
        """
        gf.fh.write('# Common Variables\n')
        gf.fh.write('UNAME  = $(OS)\n')
        gf.fh.write('CLEAN  =\n\n')

        gf.fh.write('ifeq ($(UNAME), Windows_NT)\n')
        gf.fh.write('  MAKE          = make.exe\n')
        gf.fh.write('  LINK_CMD      = junction.exe\n')
        gf.fh.write('  UNLINK_CMD    = junction.exe -d\n')
        gf.fh.write('  RUNLNK-CMD    = $(LINK_CMD) $@ "$^"\n')
        gf.fh.write('  CLEAN-CMD     = $(UNLINK_CMD) $@\n')
        gf.fh.write('  OS_DEL        = del\n')
        gf.fh.write('  OS_COPY       = copy\n')
        gf.fh.write('  OS_CPDIR      = xcopy /E\n')
        gf.fh.write('  OS_MKDIR      = md\n')
        gf.fh.write('  OS_RMDIR      = del /s /q\n')
        gf.fh.write('  OS_NOT_EXISTS = @if not exist\n')
        gf.fh.write('  OS_DIR_SEP    = \\\\\n')
        gf.fh.write('else\n')
        gf.fh.write('  MAKE          = make\n')
        gf.fh.write('  LINK_CMD      = ln -s\n')
        gf.fh.write('  UNLINK_CMD    = rm -f\n')
        gf.fh.write('  RUNLINK-CMD   = $(LINK_CMD) "$^" $@\n')
        gf.fh.write('  CLEAN-CMD     = $(UNLINK_CMD) $@\n')
        gf.fh.write('  OS_DEL        = rm -f\n')
        gf.fh.write('  OS_COPY       = cp\n')
        gf.fh.write('  OS_CPDIR      = cp -r\n')
        gf.fh.write('  OS_MKDIR      = mkdir -p\n')
        gf.fh.write('  OS_RMDIR      = rm -f -r\n')
        gf.fh.write('  OS_NOT_EXISTS =\n')
        gf.fh.write('  OS_DIR_SEP    = /\n')
        gf.fh.write('endif\n\n')


    def _gen_compiler_vars(self, gf: 'Generator.GeneratedFile') -> None:
        """
        Virtual method to generate the compiler specific vars.
        """
        raise Exception('_gen_compiler_vars() not implemented')


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
        gf.fh.write('\t@echo "  release  : build for release"\n')
        gf.fh.write('\t@echo "  debug    : build for debug"\n')
        gf.fh.write('\t@echo "  clean    : clean all binaries"\n')
        gf.fh.write('\t@echo "  help     : this help"\n')
        gf.fh.write('\t@echo\n')
