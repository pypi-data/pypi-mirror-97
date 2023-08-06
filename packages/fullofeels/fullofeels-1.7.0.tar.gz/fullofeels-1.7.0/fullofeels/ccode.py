
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Handy C utility code and constants

from __future__ import division, print_function

import sys, types, string
import ctypes
from ctypes import *

from fullofeels.codegen import indentStr
from fullofeels.i18nstr import _T


## Lower level code generation options

# Tracing print code in stubs?
genPrint = False

# Target Python version?
targetVersion = (2, 7)

# My C compiler is crap and can't handle UTF-8?
asciiStrings = False

def setOptions(opts):
    global genPrint, targetVersion, asciiStrings, beginHeader, endHeader
    #
    genPrint = opts.printf
    asciiStrings = opts.ascii
    if opts.hdrIfDef:
        beginHeader = OLD_beginHeader
        endHeader = OLD_endHeader
    # Used to be command line option, decided not to bother
    targetVersion = sys.version_info


# Fiddly to type and read
dquote = '"'

def cstrEncode(s):
    """Python string as C literal, assuming compiler can handle UTF-8.
       Does NOT add the surrounding quotes"""
    # Interesting thing I wish I'd never had to learn: in Python \x escapes are
    # always 2 hex digits. In C, it's as many hex digits as the compiler feels
    # like scanning. So chars that are also hex digits can't follow \x
    result = ""
    prevHex = False
    for c in s:
        if c == '\n':
            result += '\\n'
            prevHex = False
        elif c == '\r':
            result += '\\r'
            prevHex = False
        elif c == '\t':
            result += '\\t'
            prevHex = False
        elif c == '\\':
            result += '\\\\'
            prevHex = False
        elif c == dquote:
            result += '\\"'
            prevHex = False
        elif ord(c) < 32 or ord(c) == 127:
            result += "\\x{0:02x}".format(ord(c))
            prevHex = True
        elif prevHex and c in string.hexdigits:
            # All the hex digits are ASCII
            result += "\\x{0:02x}".format(ord(c))
            prevHex = True
        else:
            result += c
            prevHex = False
    return result

def byteEncode(s):
    """Non-ASCII string for C compiler that doesn't handle UTF-8"""
    # Want exact UTF-8 byte sequence because that's what Python C API requires.
    # Encoding everything as \x bytes works, and if you're unlucky enough to be
    # doing i18n with an ASCII-only C compiler, you have other problems anyway
    result = ""
    for b in bytearray(s, 'utf-8'):
        result += "\\x{0:02x}".format(b)
    return result


def cStrRepr(s):
    """Convert single Python string into acceptable C literal"""
    if asciiStrings:
        # Anglo-Saxon string?
        try:
            asAscii = s.encode('ascii').decode('ascii')
            return cstrEncode(asAscii)
        except UnicodeError:
            return byteEncode(s)
    else:
        return cstrEncode(s)

def strLit(s):
    """Return string as C constant. Can be multiline"""
    lines = [cStrRepr(chunk) for chunk in s.splitlines(1)] # Don't strip whitespace or LF
    if len(lines) == 1:
        return dquote + lines[0] + dquote
    else:
        # C compiler will concatenate string literals. Indent after the first
        glue = dquote + '\n' + indentStr + dquote
        return dquote + glue.join(lines) + dquote

def docStringLit(s):
    """Wrap string literal in macro that Python internals use"""
    return "PyDoc_STR(" + strLit(s) + ")"


def id(s):
    """Convert Python name into C compiler acceptable name.
       NOP for Python 2, but 3 allows Unicode identifiers"""
    # This is how PEP 489 says module names are converted
    try:
        coded = s.encode("ascii")
    except UnicodeEncodeError:
        coded = s.encode("punycode").replace(b'-', b'_')
    return coded.decode("ascii")

def value(pyVal):
    """Try to translate (simple) Python value into C equivalent"""
    if pyVal is None:
        return "NULL"
    elif isinstance(pyVal, bool):
        # C99 has true and false if you include <stdbool.h>, but
        # that doesn't work with Visual Studio. (Maybe 2015?)
        # 0 and 1 will always work
        if pyVal:
            return "1"
        else:
            return "0"
    elif isinstance(pyVal, int) or isinstance(pyVal, float):
        return str(pyVal)
    elif isinstance(pyVal, str):
        return strLit(pyVal)
    else:
        logging.warning(_T("Don't know how to represent C value of ") + str(pyVal))
        return "/* TODO " + strLit(str(pyVal)) + " */"

def text(txt):
    """Translate comment or similar into pure ASCII if necessary"""
    if asciiStrings:
        # This is used for comments, not code. Replacing Unicode with ? would
        # make it impossible to recover original text, so use web coding
        return txt.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    else:
        return txt


##      Translating Python types into C

# List of built in types with C struct name that doesn't fit the normal pattern
_SpecialNames = {
    bytearray                   : "PyByteArrayObject",
    frozenset                   : "PySetObject",
    memoryview                  : "PyMemoryViewObject",
    types.BuiltinFunctionType   : "PyCFunctionObject",
    types.FunctionType          : "PyFunctionObject",
    types.MethodType            : "PyMethodObject",
}

# ctypes and C equiv. Would be easier if these were attributes of ctypes...
CTypesStr = {
    c_int :     "int",
    c_long :    "long",
    c_float :   "float",
    c_double :  "double",
    c_ssize_t : "Py_ssize_t",
    c_char_p :  "char *",
    c_void_p :  "void *",

    c_byte :    "signed char",
    c_ubyte :   "unsigned char",
    c_short :   "short",
    c_ushort :  "unsigned short",
    c_uint :    "unsigned int",
    c_ulong :   "unsigned long",

    # 8/16/32/64 bit int/unsigned int types REMOVED because one of them
    # will overwrite the c_int value. This in turn changes builtin methods
    # from 'int' to 'int32_t' or whatever
}



def stdObjectStruct(pyClass):
    """Return C struct type for Python object. Does not include *"""
    # Special case?
    if pyClass is int and targetVersion >= (3, 0):
        return "PyLongObject"
    elif pyClass is str and targetVersion >= (3, 0):
        return "PyUnicodeObject"
    elif pyClass is str and targetVersion < (3, 0):
        return "PyStringObject"
    elif pyClass in _SpecialNames:
        return _SpecialNames[pyClass]
    # Default is that Spam (or spam) becomes PySpamObject
    name = id(pyClass.__name__)
    name = name[0].upper() + name[1:]
    # Don't want ObjectObject
    if name.endswith("Object") or name.endswith("object"):
        name = name[:-6]
    return "Py" + name + "Object"

def objectStruct(pyClass):
    # Already set?
    try:
        return pyClass.cObjectStruct
    except AttributeError:
        pass
    return stdObjectStruct(pyClass)

def classStruct(pyClass):
    # Already set?
    try:
        return pyClass.cClassStruct
    except AttributeError:
        pass
    # Special case
    if pyClass is object:
        return "PyBaseObject_Type"
    else:
        instType = stdObjectStruct(pyClass)
        return instType.replace("Object", "_Type")


##  Code used at start and end of each generated .h file

# It's the 21st century, so default to modern compiler
beginHeader = """\
#pragma once
"""

endHeader = """
"""

# Old style header guard
OLD_beginHeader = """\
#ifndef {hdrID}_H
#define {hdrID}_H
"""

OLD_endHeader = """
#endif
"""

beginCPPGuard = """
#ifdef __cplusplus
extern "C" {
#endif
"""

endCPPGuard = """
#ifdef __cplusplus
}
#endif
"""

##  Code used at start, end of .c files (.cpp, .m, whatever)

beginBody = """
/* Recommended for Python 3 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "{name}.h"

"""

endBody = """
/* End generated code */
"""