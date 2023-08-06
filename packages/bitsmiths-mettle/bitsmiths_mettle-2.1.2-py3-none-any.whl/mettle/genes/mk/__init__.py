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

from mettle.genes import common


CODE_GENERATOR_LIST = [
    'mettle.genes.mk.gen_angular.GenAngular',
    'mettle.genes.mk.gen_cpp.GenCpp',
    'mettle.genes.mk.gen_mettleproj.GenMettleProj',
    'mettle.genes.mk.gen_mksln.GenMkSolution',
    'mettle.genes.mk.gen_pythondist.GenPythonDist',
]

code_generators = []

if os.environ.get('METTLE_MK_CUST_GENES'):
    for cgen in os.environ.get('METTLE_MKFILE_CUST_GENES').split(os.path.pathsep):
        CODE_GENERATOR_LIST.append(cgen)


for cgen in CODE_GENERATOR_LIST:
    logging.info('Importing mettlemk makefile generator [%s]' % cgen)
    plug, exc = common.import_dyn_pluggin(cgen)
    code_generators.append(plug)


__all__ = [ 'code_generators' ]
