
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Conversion of Python properties into C. Used by pyclass

from __future__ import division, print_function

import ctypes
from ctypes import *
import inspect

from fullofeels import ccode
from fullofeels.i18nstr import _T

class CProperty(object):
    """Python property becomes a C member"""
    def __init__(self, name, obj):
        self.name = name
        self.getter = obj.fget
        setter = obj.fset
        self.isReadOnly = (setter is None)
        self.docString = inspect.getdoc(self.getter)
        # Can't get source for property itself
        self.src, self.lineNo = inspect.getsourcelines(self.getter)
        self.pyType = self.returnType()

    def returnType(self):
        """Very similar to pymethod.returnType"""
        try:
            retType = self.getter.__annotations__["return"]
            return retType
        except (AttributeError, KeyError):
            # Nope
            pass
        # Look for a return statement?
        srcCode = [line.strip() for line in self.src]
        srcCode.reverse()
        for line in srcCode:
            if line.startswith("return"):
                # Strip leading return
                line = line[6:]
                what = eval(line)
                # Expect something like return int, return MyClass
                if inspect.isclass(what):
                    return what
                else:
                    logging.warning(_T("return for property {} must be a type or class".format(self.name)))
        return None

    def genObjectField(self, dest):
        """C member as field in object struct"""
        dest.code("{} {}".format(_memberCType(self), self.name))


def getProperties(pyClass, newProperty=CProperty):
    """Return list of property objects, optional custom class"""
    props = []
    for name, obj in inspect.getmembers(pyClass):
        if inspect.isdatadescriptor(obj) and isinstance(obj, property):
            props.append(newProperty(name, obj))
    # Want to process in original source order
    props.sort(key=lambda prop: prop.lineNo)
    return props

def _memberCType(prop):
    """C type for property field"""
    pyType = prop.pyType
    if pyType is None:
        pyType = object
    # Actual C type?
    if pyType in ccode.CTypesStr:
        return ccode.CTypesStr[pyType]
    # Translate Python basic types into C
    if pyType is int:
        return ccode.CTypesStr[ctypes.c_int]
    elif pyType is float:
        # NOTE: if you decide to change this to double, also change _typeMacroStr below
        return ccode.CTypesStr[ctypes.c_float]
    # char * can be used for read only strings, others must be object
    elif pyType is str and prop.isReadOnly:
        return ccode.CTypesStr[ctypes.c_char_p]
    elif pyType is bool:
        return ccode.CTypesStr[ctypes.c_byte]
    # Anything else must be object pointer
    return ccode.stdObjectStruct(pyType) + " *"


_typeMacroStr = {
    c_int :     "T_INT",
    c_long :    "T_LONG",
    c_float :   "T_FLOAT",
    c_double :  "T_DOUBLE",
    c_ssize_t : "T_PYSSIZET",
    c_char_p :  "T_STRING",

    c_byte :    "T_BYTE",
    c_ubyte :   "T_UBYTE",
    c_short :   "T_SHORT",
    c_ushort :  "T_USHORT",
    c_uint :    "T_UINT",
    c_ulong :   "T_ULONG",
}

def memberTypeCode(prop):
    """Python type token for PyMemberDef entry"""
    if prop.pyType in _typeMacroStr:
        return _typeMacroStr[prop.pyType]
    elif prop.pyType is int:
        return "T_INT"
    elif prop.pyType is float:
        return "T_FLOAT"
    elif prop.pyType is str and prop.isReadOnly:
        return "T_STRING"
    elif prop.pyType is bool:
        return "T_BOOL"
    else:
        return "T_OBJECT_EX"

def genMemberTable(dest, memberList, cArrayName, ownerClass):
    """PyMemberDef array for type object"""
    dest.LF()
    dest.code("static PyMemberDef {name}[] = {{".format(name=cArrayName))
    dest.indent()
    for member in memberList:
        if member.docString is not None:
            docStr = ccode.docStringLit(member.docString)
        else:
            docStr = "NULL"
        if member.isReadOnly:
            flags = "READONLY"
        else:
            flags = "0"
        dest.code("{{ {name}, {ctype}, {offset}, {flags}, {doc} }},".format(
                            name=ccode.strLit(member.name),
                            ctype=memberTypeCode(member),
                            offset="offsetof({}, {})".format(ownerClass.cObjectStruct, member.name),
                            flags=flags,
                            doc=docStr),
                        semi=False)
    dest.code("{ NULL, 0, 0, 0, NULL },", semi=False)
    dest.unindent()
    dest.code("}", semi=True)
