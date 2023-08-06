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

from mettle.genes.project import Project


class MkProject(Project):
    """
    The mettle makefile project object.
    """
    def __init__(self, proj_path: str, name: str, version: str, proj_root: str, proj_ver: dict, gen_order: list):
        """
        Constructor
        """
        Project.__init__(self, proj_path, name, version)

        self.proj_root   = os.path.expandvars(proj_root)
        self.gen_order   = gen_order
        self.proj_ver    = proj_ver

        for item in self.proj_ver:
            self.proj_ver[item] = os.path.expandvars(str(self.proj_ver[item]))


    def initialize(self):
        """
        Initialize is use by the user project to initialize the makefile project.
        """
        logging.info('Initializing project [%s]' % self.name)

        if self.version != self.VERSION:
            raise Exception('Project version %f is not the same as Generator version %f' % (self.version, self.VERSION))

        self._load_generators()


    def generate(self, clean: bool = False, for_async: bool = False):
        if for_async:
            return

        self._validate_project()

        logging.info('Generate - Started (%s)' % self.name)

        gen_info               = {}
        gen_info['version']    = str(self.VERSION)
        gen_info['proj']       = self
        gen_info['clean']      = clean

        for gi in self.gen_order:
            gobj = self.generators.get(gi)

            if not gobj:
                raise Exception('Makefile generator [%s] not found.' % (gi))

            if not gobj.enabled:
                logging.info('  generator (%s) not enabled' % gobj.name())
                continue

            logging.info('  generating (%s)...' % gobj.name())

            gobj.initialize_generation(gen_info)

            gobj.generate_makefiles(gen_info)

            gobj.finalize_generation(gen_info)

        logging.info('Generate - Done(%s)' % self.name)


    def _validate_project(self):
        """
        Validate a project is not empty.
        """
        logging.info('Validating Project...')

        if len(self.generators) == 0:
            raise Exception('No code generators have been initialized for project [%s]!' % self.name)

        if not os.path.exists(self.proj_root):
            raise Exception('Project root path not found [%s]' % (self.proj_root))

        if not os.path.exists(self.proj_root):
            raise Exception('Project root path not found [%s]' % (self.proj_root))


    def _load_generators(self):
        """
        Loads all the code generators.
        """
        logging.info('Loading makefile generators')
        self.generators = {}

        import mettle.genes.mk

        for gcls in mettle.genes.mk.code_generators:
            gobj = gcls()
            self.generators[gobj.name()] = gobj
