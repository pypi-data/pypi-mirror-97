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

import re


class DavCache:
    """
    A cache of active dav's and their associated objects.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._targ_cache   = {}
        self._type_cache   = {}
        self._regex_lookup = {}
        self._func_lookup  = {}


    def set_regex_lookup(self, rl: dict, reset: bool = False, plz_compile: bool = True):
        """
        Set regex lookups.

        :param rl: New regex lookups to add.
        :param reset: If true, will clear the existing lookups first,
        :param plz_compile: If true, will compile the regex expression for you.
        """
        if reset:
            self._regex_lookup.clear()

        if not plz_compile:
            self._regex_lookup.update(rl)

        for name, val in rl.items():
            if isinstance(val, str):
                self._regex_lookup[name] = re.compile(val)
            else:
                self._regex_lookup[name] = val


    def set_func_lookup(self, fl: dict, reset: bool = False):
        """
        Set regex lookups.

        :param fl: New function lookups to add.
        :param reset: If true, will clear the existing lookups first,
        """
        if reset:
            self._func_lookup.clear()

        self._func_lookup.update(fl)


    def add_targ(self, targ: str, dav):
        """
        Adds a dav to a target.

        :param targ: Target object that the dav will apply to.
        :param dav: (Dav/list) The dav or list of davs.
        """
        if not isinstance(targ, str):
            raise Exception('Can only add targets with targ type of [str]')

        tobj = self._targ_cache.get(targ)

        if tobj is None:
            tobj = []
            self._targ_cache[targ] = tobj

        if isinstance(dav, list):
            for d in dav:
                tobj.append(d)
        else:
            tobj.append(dav)


    def rem_targ(self, targ: str, davType):
        """
        Removes target davs by dav type.

        :param targ: The target objec to remove davs from.
        :param davType: (Dav.eDavType) The dav type.
        :return: Total removed.
        """
        tobj = self._targ_cache.get(targ)

        if tobj is None:
            return 0

        rmcnt = 0
        idx   = 0

        while idx < len(tobj):
            if tobj.get_type() == davType:
                del tobj[idx]
                rmcnt += 1
                continue

            idx += 1

        return rmcnt


    def add_type(self, otype: type, dav):
        """
        Adds a dav to use against all types.

        :param otype: The type the dav will apply to.
        :param dav: (Dat/list) The dav or list of davs.
        """
        if not isinstance(otype, type) and not isinstance(otype, object):
            raise Exception('Can only add types of type [type, object]')

        tobj = self._type_cache.get(otype)

        if tobj is None:
            tobj = []
            self._type_cache[otype] = tobj

        if isinstance(dav, list):
            for d in dav:
                tobj.append(d)
        else:
            tobj.append(dav)


    def rem_type(self, otype: type, davType):
        """
        Removes type davs by dav type.

        :param otype: The type to remove from.
        :param davType: (eDavType) The dav type.
        :return: Total removed.
        """
        tobj = self._type_cache.get(otype)

        if tobj is None:
            return 0

        rmcnt = 0
        idx   = 0

        while idx < len(tobj):
            if tobj.get_type() == davType:
                del tobj[idx]
                rmcnt += 1
                continue

            idx += 1

        return rmcnt


    def clear(self) -> "DavCache":
        """
        Clears the cache.

        :return: Itself.
        """
        self._targ_cache.clear()
        self._type_cache.clear()

        return self


    def clear_lookups(self) -> "DavCache":
        """
        Clears the lookups.

        :return: Itself.
        """
        self._regex_lookup.clear()
        self._func_lookup.clear()

        return self


    def validate(self, tname: str, tobj, throw_ex: bool = True, fail_fast: bool = True, quali: str = None) -> int:
        """
        Validates targent name and object against all the cached davs.

        :param tname: Name of the object.
        :param tobj: (object/list) Base type of the object or list of base types.
        :param throw_ex: (bool/list) If True raises an exception an any error else returns False on failure, if
                         type is a list, the errors are appeneded.
        :param fail_fast: If True aborts on first error encountered, else logs all the errors before aborting.
        :param quali: If not None, the qualifier name.
        :return: Number of failed validations.
        """
        fcnt = 0

        if isinstance(tobj, list):
            idx = 0
            for titem in tobj:
                tdesc = '%s[%d]' % (tname, idx) if quali is None else '%s%s[%d]' % (quali, tname, idx)
                fcnt += self.validate(tname, titem, throw_ex, fail_fast, tdesc)
                idx  += 1

                if fcnt > 0 and fail_fast:
                    return fcnt

            return fcnt

        davs = self._targ_cache.get(tname)

        if davs is not None:
            tdesc = tname if quali is None else '%s%s' % (quali, tname)
            for d in davs:
                if not d.validate(tdesc, tobj, throw_ex, self._regex_lookup, self._func_lookup):
                    if fail_fast:
                        return 1

                    fcnt += 1

        davs = self._type_cache.get(type(tobj))

        if davs is not None:
            tdesc = tname if quali is None else '%s%s' % (quali, tname)
            for d in davs:
                if not d.validate(tdesc, tobj, throw_ex, self._regex_lookup, self._func_lookup):
                    if fail_fast:
                        return 1

                    fcnt += 1

        return fcnt


    def validate_object(self, tname: str, tobj, throw_ex: bool = True, fail_fast: bool = True , quali: str = None) -> int:
        """
        Validates dictionary/object target against all the cached davs.

        :param tname: Name of the object.
        :param tobj: (dict/obj/list) A dictionary, list or dictionary of target objects to validate or an object to validate.
        :param throw_ex: (bool/list) If True raises an exception an any error else returns False on failure, if
                          type is a list, the errors are appeneded.
        :param fail_fast: If True aborts on first error encountered, else logs all the errors before aborting.
        :param quali: If not none, the qualifier of the object.
        :return: Number of failed validations.
        """
        fcnt = 0

        if isinstance(tobj, list):
            idx = 0
            for titem in tobj:
                tdesc = '%s[%d]' % (tname, idx) if quali is None else '%s%s[%d]' % (quali, tname, idx)
                fcnt += self.validate_object(tname, titem, throw_ex, fail_fast, tdesc)
                idx  += 1

                if fcnt > 0 and fail_fast:
                    return fcnt

        elif isinstance(tobj, dict):
            tdesc = '%s.' % tname if quali is None else '%s%s' % (quali, tname)
            for tin, titem in tobj.items():
                fcnt += self.validate(tin, titem, throw_ex, fail_fast, tdesc)

                if fcnt > 0 and fail_fast:
                    return fcnt
        else:
            tdesc = '%s.' % tname if quali is None else '%s%s' % (quali, tname)
            for tin, titem in tobj.__dict__.items():
                fcnt += self.validate(tin, titem, throw_ex, fail_fast, tdesc)

                if fcnt > 0 and fail_fast:
                    return fcnt

        return fcnt
