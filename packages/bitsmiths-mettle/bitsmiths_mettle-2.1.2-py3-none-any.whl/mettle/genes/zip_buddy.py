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
import zipfile


class ZipBuddy:
    """
    A zip buddy helper class to make fancy recursive zipping easy peasy.
    """

    def __init__(self, dest_zip: str):
        """
        Constructor.

        :param dest_zip:: The dest of the zip, can use / for dir seperators.
        """
        self._raise_errors  = False
        self._dest_zip      = dest_zip.replace('/', os.path.sep)
        self._targets       = []
        self._exclude_dirs  = [ '.svn', '.git' ]
        self._exclude_paths = []
        self._pre_executes  = []
        self._post_executes = []
        self._dirs          = []
        self._text_as_files = {}


    def add_exclude_path(self, path: str) -> None:
        """
        Add an exclude path for the zip buddy, all files in this path will be ignored.

        :param path: The path to be excluded
        """
        self._exclude_paths.append(path)


    def add_exclude_dir(self, dir_name: str) -> None:
        """
        Add a directory name that will always be excluded by zipbuddy

        @param dir_name string : The dir_name to be excluded
        """
        self._exclude_dirs.append(dir_name)


    def add_files(self, dest_dir: str, src_dir: str, ext: list, recursive: bool):
        """
        Add files extensions to be ziped.

        :param dest_dir: The destination path in the zip file
        :param src_dir: The source path to search for the files
        :param ext: List of extensions for include, ie cpp, h, jar
        :param recursive: If True then do a recusive search
        """
        self._targets.append({
            'files'     : True,
            'dest_dir'  : dest_dir,
            'src_dir'   : src_dir,
            'ext'       : ext,
            'recursive' : recursive,
            'filename'  : None,
            'new_name'  : None,
        })


    def add_file(self, dest_dir: str, src_dir: str, filename: str, new_name: str = None) -> None:
        """
        Add a specific file to the zip.

        :param dest_dir: The destination path in the zip file
        :param src_dir: The source path to find the file
        :param filename: The name of the file.
        :param new_name: If not None, then the new name of the file in zip.
        """
        self._targets.append({
            'files'     : False,
            'dest_dir'  : dest_dir,
            'src_dir'   : src_dir,
            'ext'       : None,
            'recursive' : False,
            'filename'  : filename,
            'new_name'  : new_name,
        })


    def add_text_as_file(self, dest_dir, filename, txt) -> None:
        """
        Adds text as file to zip.

        :param dest_dir: The destination path in the zip file
        :param filename: The name of the file.
        :param txt: The text of the file.
        """
        self._text_as_files[os.path.join(dest_dir, filename)] = txt


    def add_pre_execute(self, cmd: str) -> None:
        """
        Add a command to run before running zipbuddy run command.

        :param cmd: The os command to be run
        """
        self._pre_executes.append(cmd)


    def add_post_execute(self, cmd: str) -> None:
        """
        Add a command to run after running zipbuddy run command.

        @param cmd string : The os command to be run
        """
        self._post_executes.append(cmd)


    def create_dir(self, pth: str) -> None:
        """
        Creates the specified directory if it does not exit.

        :param pth : The path to be created.
        """
        if os.path.exists(pth):
            return

        print('Creating directory: %s' % pth)
        os.makedirs(pth, exists_ok=True)


    def clean_dir(self, pth: str) -> None:
        """
        Cleans all items in the specified directory, recusively killing everything in it.

        :param pth:: The path to removed.
        """
        if not os.path.exists(pth):
            return

        print('Cleaning directory: %s' % pth)

        for root, dirs, files in os.walk(pth):
            for f in files:
                os.unlink(os.path.join(root, f))

        for root, dirs, files in os.walk(pth, topdown =False):
            for d in dirs:
                os.rmdir(os.path.join(root, d))


    def run(self, raise_errors: bool = True):
        """
        Runs the zipbuddy package builder.

        :param raise_errors: If true, the command raises exception if anything goes wrong, else it just prints warnings.
        """
        self._raise_errors = raise_errors

        print('Runing zipbuddy for: %s' % self._dest_zip)

        if self._exclude_paths:
            print('   Excluding paths:')
            for x in self._exclude_paths:
                print('    - %s' % x)

        if self._exclude_dirs:
            print('   Excluding directories:')
            for x in self._exclude_dirs:
                print('    - %s' % x)

        if self._pre_executes:
            print('  Running pre-run execute commands:')
            for x in self._pre_executes:
                print('    - Running: %s' % x)
                rc = os.system(x)

                if rc != 0:
                    if self._raise_errors:
                        raise Exception('Pre Command Failed (rc:%d) - %s' % (rc))

                    print('   - WARNING! Command failed! Return code: %d' % rc)
                    return False

        print('  Creating zip file:  %s' % self._dest_zip)

        cnt    = 0
        zip_fh = zipfile.ZipFile(self._dest_zip, 'w')

        for tname, txt in sorted(self._text_as_files.items()):
            zip_fh.writestr(tname, txt, zipfile.ZIP_DEFLATED)
            cnt += 1

        for x in self._targets:
            cnt += self._zip_target(zip_fh, x)

        zip_fh.close()

        print('  Total files zipped: %d' % cnt)

        if self._post_executes:
            print('  Running post-run execute commands:')
            for x in self._post_executes:
                print('    - Running: %s' % x)
                rc = os.system(x)

                if rc != 0:
                    if self._raise_errors:
                        raise Exception('Post Command Failed (rc:%d) - %s' % (rc))

                    print('   - WARNING! Command failed! Return code: %d' % rc)
                    return False

        return True


    def _zip_target(self, zip_fh, targ: dict) -> int:
        source_folder = targ['src_dir'].replace('/', os.path.sep)
        dest_folder   = targ['dest_dir'].replace('/', os.path.sep)
        include_all   = False
        ext_list      = targ['ext']
        cnt           = 0

        if not os.path.exists(source_folder):
            if self._raise_errors:
                raise Exception('Source folder not found: %s' % source_folder)

            print('   - WARNING! Source Path Not Found: %s' % source_folder)
            return cnt

        if not targ['files']:
            source  = os.path.join(source_folder, targ['filename'])
            dest    = os.path.join(dest_folder, targ['filename'] if not targ['new_name'] else targ['new_name'])

            if not os.path.exists(source):
                if self._raise_errors:
                    raise Exception('Source file not found: %s' % source)

                print('   - WARNING! Source File Not Found: %s' % source)
                return cnt

            print('   ...adding: [%s]->[%s]' % (source, dest))
            cnt += 1
            zip_fh.write(source, dest, zipfile.ZIP_DEFLATED)
            return cnt

        if ext_list and ext_list[0] == '.*':
            include_all = True

        for root, dirs, files in os.walk(source_folder):
            exchk = root.replace(os.path.sep, '/')
            chk   = exchk.split('/')
            cont  = False

            for p in self._exclude_paths:
                if exchk.startswith(p):
                    cont = True
                    break

            if cont:
                continue

            for c in chk:
                if c in self._exclude_dirs:
                    cont  = True
                    break

            if cont:
                continue

            for f in files:
                if not targ['recursive']:
                    if root != source_folder:
                        continue

                ext = os.path.splitext(f)[-1]

                if not include_all and ext not in ext_list:
                    continue

                targ_file = os.path.join(root, f)
                targ_file = targ_file[len(source_folder):]

                if targ_file[0] == os.path.sep:
                    targ_file = targ_file[1:]

                source  = os.path.join(root, f)
                dest    = os.path.join(dest_folder, targ_file)
                cnt    += 1

                print('   ...adding: [%s]->[%s]' % (source, dest))
                zip_fh.write(source, dest, zipfile.ZIP_DEFLATED)


        return cnt
