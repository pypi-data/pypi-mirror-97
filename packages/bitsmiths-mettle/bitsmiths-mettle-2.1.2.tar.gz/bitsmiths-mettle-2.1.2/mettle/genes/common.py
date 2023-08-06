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
import hashlib


def set_default(var, def_val):
    """
    Set a default value if the var is None.

    :param var: The variable to check.
    :param def_val: The default value if var is None.
    :return: var|def_val
    """
    if not var:
        return def_val

    return var


def read_dict(dic: dict, key: str, ttype: type = None, parent: str = '', req_vals: list = None, optional: bool = False):
    """
    Reads from the dictionary.

    :param dic: The dictionary to validate.
    :param key: The key to check exists.
    :param ttype: The type the key has to be, if None this is ignored.
    :param parent: Optional the parent of the dicionary to help with error logging.
    :param req_vals: An option list of values, if not None, the key value has to be one of these values.
    :param optional:  If True, the value does not have to exist, None is returned in this case.
    :return: The value of 'key'.
    """
    if not dic or type(dic) != dict:
        raise Exception('Dictionary input not a dictionary, parent [%s%s]' % (parent, key))

    if not ttype:
        if key not in dic:
            if not optional:
                raise Exception('Dictionary invalid, key [%s%s] not found' % (parent, key))

            return None

        return dic[key]

    val = dic.get(key)

    if val is None:
        if optional:
            return val

        raise Exception('Dictionary invalid, key [%s%s] not found' % (parent, key))

    if ttype and type(val) != ttype:
        try:
            val      = ttype(val)
            dic[key] = val
        except Exception:
            raise Exception('Dictionary invalid, key [%s%s] value [%s] is the incorrect type.  Expected [%s] and got [%s]' % (
                parent, key, val, str(type(val)), str(ttype) ))

    if req_vals is not None and val not in req_vals:
        raise Exception('Dictionary invalid, key [%s%s] value [%s] not valid.  Value must be one of: %s' % (
            parent, key, val, str(req_vals)))

    return val


def hash_str(val) -> str:
    """
    Hashes a single string or list of strings.

    :param val: String or list of strings to hash.
    :return: The hashed result.
    """
    m = hashlib.md5()

    if type(val) == str:
        m.update(val.encode('utf8'))
    else:
        for sval in val:
            m.update(sval.encode('utf8'))

    return m.hexdigest()


def import_dyn_pluggin(mpath: str, module_only: bool = False, raise_errors: bool = True) -> tuple:
    """
    Import a dynamic module.

    :param mpath: Fully qaualified pluging path, eg: sysX.cust_generators.firebird.Firebird
    :param module_only: If this is true, then it donly imports the module, does not expect the last path object
                          to be a attribute.
    :param raise_errors: If true, raises exceptions instead of returnning None on error.
    :return: (type, exception), if failure returns (None, Exception) else (type, None).
    """
    import importlib

    try:
        if module_only:
            obj = importlib.import_module(mpath)
        else:
            mparts = mpath.split('.')

            if len(mparts) == 1:
                raise Exception('Module path not valid, no path seperation.')

            from_list = '.'.join(mparts[0:-1])

            mod = importlib.import_module(from_list)
            obj = getattr(mod, mparts[-1])

            if type(obj) != type:
                raise Exception('Object is not a type. - Dynamic Pluggin Import [%s]' % mpath)

    except Exception as x:
        if raise_errors:
            raise

        return None, x

    return obj, None
