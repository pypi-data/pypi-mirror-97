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


class Project:
    """
    Base project class
    """
    VERSION = 2.1

    def __init__(self, proj_path, name, version):
        """
        Constructor
        """
        self.name          = name
        self.version       = version
        self.proj_path     = proj_path
        self.project_file  = None
        self.project_dir   = None

        self.set_proj(proj_path)
        self.initialize()


    def initialize(self):
        """
        Initialize is use be user project to initialize the database project.
        """
        pass


    def set_proj(self, proj_path):
        """
        Set the project and project path
        """
        if not os.path.exists(proj_path):
            raise Exception('Project path [%s] not found!' % proj_path)

        self.proj_path    = proj_path.replace('/', os.path.sep)
        self.project_dir  = os.path.split(self.proj_path)[0]
        self.project_file = os.path.split(self.proj_path)[1]


    def generate(self, clean = False):
        """
        Runs the project generator.
        """
        pass
