
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Conversion of Python parameters into C. Used by pymethod and visible

from __future__ import division, print_function

import ctypes
import inspect
import types

from fullofeels import ccode
from fullofeels.i18nstr import _T


# NOTE: each of these functions has a very similar or identical series of if tests. Why not
# use a dict or other data structure? Because there are three different ways of converting
# a Python argument to C, and the C syntax is different for each. So it's messy.

def cType(argName, translations={}):
    """C type for declaring local argument value for parameter"""
    target = translations.get(argName, object)
    if target is object:
        return "PyObject *"
    elif target is chr:
        if ccode.targetVersion >= (3, 0):
            return "int"
        else:
            return "char"
    elif inspect.isclass(target):
        if issubclass(target, bool) and ccode.targetVersion >= (3, 3):
            return "int"
        elif issubclass(target, int):
            return "int"
        elif issubclass(target, float):
            return "double"
        elif issubclass(target, str):
            return "const char *"
        elif target is memoryview:
            return "Py_buffer"
    return "PyObject *"

def formatStr(argName, translations={}):
    """The format to use in the PyArg_ParseTuple string for given parameter"""
    target = translations.get(argName, object)
    if target is object:
        return "O"
    elif hasattr(target, "_foeelsArgumentConverter"):
        return "O&"
    elif target is chr:
        if ccode.targetVersion >= (3, 0):
            return "C"
        else:
            return "c"
    elif inspect.isclass(target):
        # Note: bool is a subclass of int so must test first
        if issubclass(target, bool) and ccode.targetVersion >= (3, 3):
            return "p"
        elif issubclass(target, int):
            return "i"
        elif issubclass(target, float):
            return "d"
        elif issubclass(target, str):
            return "z"
        elif target is memoryview:
            if ccode.targetVersion >= (3, 0):
                return "y*"
            else:
                return "s*"
        else:
            return "O!"
    else:
        raise TypeError(_T("{name} is not an Argument converter or class").format(name=target.__name__))

def parseArgs(argName, translations={}):
    """The argument(s) to pass to PyArg_ParseTuple for given parameter"""
    target = translations.get(argName, object)
    if target is object:
        return "&" + ccode.id(argName)
    elif hasattr(target, "_foeelsArgumentConverter"):
        return target.cName + ", &" + ccode.id(argName)
    elif inspect.isclass(target):
        if issubclass(target, bool) and ccode.targetVersion >= (3, 3):
            return "&" + ccode.id(argName)
        elif issubclass(target, int):
            return "&" + ccode.id(argName)
        elif issubclass(target, float):
            return "&" + ccode.id(argName)
        elif issubclass(target, str):
            return "&" + ccode.id(argName)
        elif target is memoryview:
            return "&" + ccode.id(argName)
        else:
            return "&" + ccode.classStruct(target) + ", &" + ccode.id(argName)
    else:
        # Any error will have been reported by formatStr
        return "&" + ccode.id(argName)

def cleanup(argName, translations={}):
    """Line of C code that should be generated at end of function for some arguments"""
    target = translations.get(argName, object)
    if target is memoryview:
        return "PyBuffer_Release(&{name})".format(name=ccode.id(argName))
    return None


def genArgumentConverter(pyFunc, dest):
    """Generate argument converter skeleton"""
    # Sanity check
    if hasattr(pyFunc.callable, "_foeelsPosArgs") or hasattr(pyFunc.callable, "_foeelsKwArgs"):
        raise TypeError(_T("Argument converter {name} cannot also have argument parsing decorator").format(name=str(pyFunc.name)))
    # Must have (object, address) parameters
    posArgs, varArgs, dictArgs, defaults = inspect.getargspec(pyFunc.callable)
    if len(posArgs) != 2 or varArgs is not None or dictArgs is not None or defaults is not None:
        raise TypeError(_T("Argument converter {name} must have only two positional parameters without defaults").format(name=str(pyFunc.name)))
    #
    dest.code("int", semi=False)
    dest.code("{name}(PyObject * {obj}, void * {addr})".format(name=pyFunc.cName,
                                                                obj=ccode.id(posArgs[0]),
                                                                addr=ccode.id(posArgs[1])),
                                                                semi=False)
    dest.code("{")
    dest.indent()
    docStr = inspect.getdoc(pyFunc.callable)
    if docStr is not None:
        dest.comment(docStr)
    if ccode.targetVersion >= (3, 1):
        dest.code("if ({obj} == NULL) {{".format(obj=ccode.id(posArgs[0])))
        dest.comment("Clean up any memory allocated if conversion failed")
        dest.code("}")
        dest.comment("return Py_CLEANUP_SUPPORTED if you allocate memory")
    dest.code("return 0")
    dest.unindent()
    dest.code("}")
    # Mark this function as non-Python, not part of module
    pyFunc.pythonAPI = False
    # And need to know implementation name
    pyFunc.callable._foeelsCName = pyFunc.cName


def buildArgTypes(proc):
    """Use attributes set by decorator to build dict of name : type"""
    translations = {}
    for idx, t in enumerate(proc.callable._foeelsPosArgs):
        translations[proc.posArgs[idx]] = t
    for key, t in proc.callable._foeelsKwArgs.items():
        if key in translations:
            raise RuntimeError(_T("Translation specified more than once for parameter {p} in {name}").format(p=key, name=proc.name))
        translations[key] = t
    if len(translations) != len(proc.posArgs):
        raise RuntimeError(_T("Wrong number of parameter translations for {name}").format(name=proc.name))
    return translations
