
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Definitions for built-in type methods within Python type record

from __future__ import division, print_function

import ctypes
from ctypes import *
import collections
import numbers

from fullofeels import ccode
from fullofeels.i18nstr import _T


# Built-in methods have pointer stored directly in the type object record
# or an auxiliary method table. Need the Python double underscore name,
# the C field name, the C field type, and C prototype. Special flag for
# builtins that take 'normal' variable length, keyword argument passing

# Most argument and return types are Python just to cut down on the chance
# of typos. A few special cases are stored directly as C code string

class TypeMethod(object):
    """Single built-in Python method"""

    def __init__(self, pyName, cField, cType, retType, arguments, stdArgs=False, version=None):
        self.name = pyName
        self.field = cField
        self.cType = cType
        self.retType = retType
        self.argList = arguments
        self.stdArgs = stdArgs
        self.version = version


# Not reallly ALL object special methods, just those that have pointers in the
# type record and are visible to Python programmers. (And that I understand.)
AllObjectMethods = (
    TypeMethod("__print__", "tp_print", "printfunc", c_int, (object, "FILE *", c_int)),
    TypeMethod("__getattr__", "tp_getattr", "getattrfunc", object, (object, c_char_p)),
    TypeMethod("__setattr__", "tp_setattr", "setattrfunc", c_int, (object, c_char_p, object)), # OR __delattr__
    TypeMethod("__repr__", "tp_repr", "reprfunc", object, (object,)),
    TypeMethod("__hash__", "tp_hash", "hashfunc", c_long, (object,)),
    TypeMethod("__call__", "tp_call", "ternaryfunc", object, (object, object, object), stdArgs=True),
    TypeMethod("__str__", "tp_str", "reprfunc", object, (object,)),
    TypeMethod("__getattribute__", "tp_getattro", "getattrofunc", object, (object, object)),
    # This is not an official Python special method, but most types with C implementation
    # use a single function rather than separate methods for lt, le, etc
    TypeMethod("__compare__", "tp_richcompare", "richcmpfunc", object, (object, object, int)),

    TypeMethod("__iter__", "tp_iter", "getiterfunc", object, (object,)),
    TypeMethod("__next__", "tp_iternext", "iternextfunc", object, (object,)),
    TypeMethod("__get__", "tp_descr_get", "descrgetfunc", object, (object, object, object)),
    TypeMethod("__set__", "tp_descr_set", "descrsetfunc", c_int, (object, object, object)), # OR __delete__
    TypeMethod("__init__", "tp_init", "initproc", c_int, (object, object, object), stdArgs=True),
    TypeMethod("__new__", "tp_new", "newfunc", object, ("struct _typeobject *", object, object), stdArgs=True),
    # __del__ method moved to tp_finalize slot in Python 3.4
    TypeMethod("__del__", "tp_del", "destructor", None, (object,), version=2),
    TypeMethod("__del__", "tp_finalize", "destructor", None, (object,), version=3),
)

# The number, sequence, mapping, and buffer special methods are handled
# slightly differently, as separate structs rather than inside type struct

def unaryFunc(pyName, cField, version=None):
    return TypeMethod(pyName, cField, "unaryfunc", object, (object,), version=version)

def binaryFunc(pyName, cField, version=None):
    return TypeMethod(pyName, cField, "binaryfunc", object, (object, object), version=version)

def ssizeArgFunc(pyName, cField):
    return TypeMethod(pyName, cField, "ssizeargfunc", object, (object, "Py_ssize_t"))


NumberMethods = (
    binaryFunc("__add__", "nb_add"),
    binaryFunc("__sub__", "nb_subtract"),
    binaryFunc("__mul__", "nb_multiply"),
    binaryFunc(None, "nb_divide", version=2), # Old divide which shouldn't be used in Python 2, removed in Python 3
    binaryFunc("__mod__", "nb_remainder"),
    binaryFunc("__divmod__", "nb_divmod"),
    TypeMethod("__pow__", "nb_power", "ternaryfunc", object, (object, object, object)),
    unaryFunc("__neg__", "nb_negative"),
    unaryFunc("__pos__", "nb_positive"),
    unaryFunc("__abs__", "nb_absolute"),
    TypeMethod("__nonzero__", "nb_nonzero", "inquiry", c_int, (object,), version=2), # Renamed to __bool__ in Python 3
    TypeMethod("__bool__", "nb_bool", "inquiry", c_int, (object,), version=3),
    unaryFunc("__invert__", "nb_invert"),
    binaryFunc("__lshift__", "nb_lshift"),
    binaryFunc("__rshift__", "nb_rshift"),
    binaryFunc("__and__", "nb_and"),
    binaryFunc("__xor__", "nb_xor"),
    binaryFunc("__or__", "nb_or"),
    TypeMethod("__coerce__", "nb_coerce", "coercion", c_int, ("PyObject **", "PyObject **"), version=2), # Removed in Python 3
    unaryFunc("__int__", "nb_int"),
    unaryFunc("__long__", "nb_long", version=2),    # Ignored in Python 3
    unaryFunc(None, "nb_reserved", version=3),
    unaryFunc("__float__", "nb_float"),
    unaryFunc("__oct__", "nb_oct", version=2),  # Removed in Python 3
    unaryFunc("__hex__", "nb_hex", version=2),  # Removed in Python 3
    binaryFunc("__iadd__", "nb_inplace_add"),
    binaryFunc("__isub__", "nb_inplace_subtract"),
    binaryFunc("__imul__", "nb_inplace_multiply"),
    binaryFunc("__idiv__", "nb_inplace_divide", version=2), # Removed in Python 3
    binaryFunc("__imod__", "nb_inplace_remainder"),
    TypeMethod("__ipow__", "nb_inplace_power", "ternaryfunc", object, (object, object, object)),
    binaryFunc("__ilshift__", "nb_inplace_lshift"),
    binaryFunc("__irshift__", "nb_inplace_rshift"),
    binaryFunc("__iand__", "nb_inplace_and"),
    binaryFunc("__ixor__", "nb_inplace_xor"),
    binaryFunc("__ior__", "nb_inplace_or"),
    binaryFunc("__floordiv__", "nb_floor_divide"),
    binaryFunc("__truediv__", "nb_true_divide"),
    binaryFunc("__ifloordiv__", "nb_inplace_floor_divide"),
    binaryFunc("__itruediv__", "nb_inplace_true_divide"),
    unaryFunc("__index__", "nb_index"),
)

#

SequenceMethods = (
    TypeMethod("__len__", "sq_length", "lenfunc", c_ssize_t, (object,)),
    binaryFunc("__add__", "sq_concat"),
    ssizeArgFunc("__mul__", "sq_repeat"),
    # get and set slice are not official Python methods. The bytecode interpreter looks for
    # these slots as a shortcut, falls back to individual get/set if not found
    ssizeArgFunc("__getitem__", "sq_item"),
    TypeMethod("__getslice__", "sq_slice", "ssizessizeargfunc", object, (object, c_ssize_t, c_ssize_t), version=2),
    TypeMethod(None, "was_sq_slice", "ssizessizeargfunc", object, (object, c_ssize_t, c_ssize_t), version=3),
    TypeMethod("__setitem__", "sq_ass_item", "ssizeobjargproc", c_int, (object, c_ssize_t, object)), # __setitem__ OR __delitem__
    TypeMethod("__setslice__", "sq_ass_slice", "ssizessizeobjargproc", c_int, (object, c_ssize_t, c_ssize_t, object), version=2), # __setslice__ OR __delslice__
    TypeMethod(None, "was_sq_ass_slice", "ssizessizeobjargproc", c_int, (object, c_ssize_t, c_ssize_t, object), version=3),    
    TypeMethod("__contains__", "sq_contains", "objobjproc", c_int, (object, object)),
    binaryFunc("__iadd__", "sq_inplace_concat"),
    ssizeArgFunc("__imul__", "sq_inplace_repeat"),
)

    # For Python 3, a sequence can also have mapping methods. Len should be the same, subscript and ass_subscript implement slicing

# TODO Field names should be same as MappingMethods, but that breaks methodForField
Py3SequenceMappingMethods = (
    TypeMethod("__len__", "sqmp_length", "lenfunc", c_ssize_t, (object,)),
    binaryFunc("__getslice__", "sqmp_subscript"),
    TypeMethod("__setslice__", "sqmp_ass_subscript", "objobjargproc", c_int, (object, object, object)), # OR __delitem__
)

#

MappingMethods = (
    TypeMethod("__len__", "mp_length", "lenfunc", c_ssize_t, (object,)),
    binaryFunc("__getitem__", "mp_subscript"),
    TypeMethod("__setitem__", "mp_ass_subscript", "objobjargproc", c_int, (object, object, object)), # OR __delitem__
)

#

BufferMethods = (
    # These four were all removed in Python 3
    TypeMethod(None, "bf_getreadbuffer", "readbufferproc", "Py_ssize_t", (object, "Py_ssize_t", "void **"), version=2),
    TypeMethod(None, "bf_getwritebuffer", "writebufferproc", "Py_ssize_t", (object, "Py_ssize_t", "void **"), version=2),
    TypeMethod(None, "bf_getsegcount", "segcountproc", "Py_ssize_t", (object, "Py_ssize_t *"), version=2),
    TypeMethod(None, "bf_getcharbuffer", "charbufferproc", "Py_ssize_t", (object, "Py_ssize_t", "char **"), version=2),
    # Common for Python 2 and 3
    TypeMethod("__getbuffer__", "bf_getbuffer", "getbufferproc", c_int, (object, "Py_buffer *", c_int)),
    TypeMethod("__releasebuffer__", "bf_releasebuffer", "releasebufferproc", None, (object, "Py_buffer *"))
)


#   Map a Python special object method to C signature.
#   For no doubt excellent reasons __getitem__ has a different signature for
#   dicts than for sequences, so need to know the class as well as method

def getMethod(pyClass, pyName):
    """Return method for double underscore name or None"""
    if issubclass(pyClass, collections.Mapping):
        for m in MappingMethods:
            if m.name == pyName:
                return m
    if issubclass(pyClass, collections.Sequence):
        if ccode.targetVersion >= (3, 0):
            for m in Py3SequenceMappingMethods:
                if m.name == pyName:
                    return m
        for m in SequenceMethods:
            if m.name == pyName:
                return m
    if issubclass(pyClass, numbers.Number):
        for m in NumberMethods:
            if m.name == pyName:
                return m
    for m in BufferMethods:
        if m.name == pyName:
            return m
    for m in AllObjectMethods:
        if m.name == pyName and (m.version is None or m.version >= ccode.targetVersion[0]):
            return m
    return None


#   Map C struct field to Python special method name. Fields are unique
#   TODO not unique in Python 3. Pass class in?
#   For now just hacked around problem by renaming struct fields

methodForCName = {}
for m in AllObjectMethods + NumberMethods + SequenceMethods + MappingMethods + Py3SequenceMappingMethods + BufferMethods:
    methodForCName[m.field] = m

def methodForField(cField):
    """Return method for given C struct field"""
    global methodForCName
    #
    return methodForCName.get(cField, None)



def cTypeString(targetType):
    """Translate builtin arg or return type to actual C"""
    if isinstance(targetType, str):
        return targetType
    elif targetType is None:
        return "void"
    elif targetType in ccode.CTypesStr:
        return ccode.CTypesStr[targetType]
    else:
        return ccode.objectStruct(targetType) + " *"
