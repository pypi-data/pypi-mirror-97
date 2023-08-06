
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Generate C outline for Python classes

from __future__ import division, print_function

import os
from os import path
import types
import numbers
import collections
import inspect
import logging

from fullofeels.i18nstr import _T

from fullofeels import ccode, pymethod, builtins, pymember


class CClass(object):
    """Implement a Python class"""

    # These are the classes to use for defined methods and properties.
    # Declared as class attributes so can be overridden by assignment.
    newClassMethod = pymethod.CClassMethod
    newClassProperty = pymember.CProperty

    def __init__(self, pyClass, outerName=None, prefix=None):
        self.pyClass = pyClass
        self.name = self.pyClass.__name__
        self.src, self.line = inspect.getsourcelines(self.pyClass)
        self.buildNames(outerName, prefix)

    def getSuperClasses(self):
        """Return list of all classes we inherit from"""
        supers = inspect.getmro(self.pyClass)[1:]
        # Python 2 allows classes that don't inherit from object.
        # Kind of silly and would break other bits of code.
        if len(supers) == 0:
            return [object,]
        else:
            return list(supers)

    def buildNames(self, outerName, prefix):
        """Generate C struct names for object and type structs"""
        # Python object gets "Py" prefix to distinguish from any
        # existing C type. Standard Python types have "Object"
        # suffix, but I prefer not to do that for program types
        name = self.name[0].upper() + self.name[1:]
        self.cObjectStruct = "Py" + name
        if prefix is not None:
            self.cObjectStruct = prefix + self.cObjectStruct
        self.cClassStruct = self.cObjectStruct + "_Type"
        # Used for object attribute dict
        self.objAttribDict = None
        #self.objAttribDict = self.name.lower() + "_dict"

    def genHeaderDef(self, dest):
        """Code for .h file"""
        self.genClassHeader(dest)
        self.genObjectHeader(dest)

    def genClassHeader(self, dest):
        dest.LF()
        # Python core types should use PyAPI_DATA macro, but apparently not extensions
        #dest.code("PyAPI_DATA(PyTypeObject) {name}".format(name=self.cClassStruct))
        dest.code("extern PyTypeObject {name}".format(name=self.cClassStruct))

    def genObjectHeader(self, dest):
        dest.LF()
        dest.code("typedef struct {")
        dest.indent()
        classOrder = self.getSuperClasses()
        # Struct should declare all class fields starting with object and working
        # down the hierarchy. Without a full C parser we can't do this for all
        # classes, but should be able to handle any built in
        hdr = []
        for cls in classOrder:
            if cls is object:
                hdr.append("PyObject_HEAD")
            elif cls.__name__ in __builtins__:
                hdr.append(ccode.stdObjectStruct(cls) + " head;")
                break
            else:
                hdr.append("/* " + _T("Fields for ") + cls.__name__ + " */")
            # Check if superclass already has object attribute dict
            if cls.__dictoffset__ != 0:
                self.objAttribDict = None
        for line in reversed(hdr):
            dest.code(line, semi=False)
        # Dict for object attributes
        if self.objAttribDict:
            dest.comment("Delete this line and set tp_dictoffset to 0 to prevent object attributes")
            dest.code("PyObject * " + self.objAttribDict)
        # C fields for properties
        dest.comment(ccode.text(_T("Fields for ") + self.name))
        self.members = pymember.getProperties(self.pyClass, self.newClassProperty)
        for m in self.members:
           m.genObjectField(dest)
        #
        dest.unindent()
        dest.code("}} {name}".format(name=self.cObjectStruct))

    def genCode(self, dest):
        """Methods and class type struct implementation"""
        logging.debug("Code class {}".format(self.name))
        self.genMethods(dest)
        self.genMethodTable(dest)
        self.genProperties(dest)
        self.genSpecialBuiltins(dest)
        self.genType(dest)

    def genMethods(self, dest):
        self.classMethods = []
        for name, value in self.pyClass.__dict__.items():
            if isinstance(value, types.FunctionType):
                self.classMethods.append(self.newClassMethod(value, self, selfType=self, outerName=self.cObjectStruct))
            elif isinstance(value, classmethod):
                # Pass the original function, not the decorator
                self.classMethods.append(self.newClassMethod(value.__func__, self, selfType=type, outerName=self.cObjectStruct))
            # Special case: Python changes __new__ into a static method but still has self type
            elif isinstance(value, staticmethod) and name == "__new__":
                self.classMethods.append(self.newClassMethod(value.__func__, self, selfType=type, outerName=self.cObjectStruct))
            elif isinstance(value, staticmethod):
                self.classMethods.append(self.newClassMethod(value.__func__, self, selfType=None, outerName=self.cObjectStruct))
        self.classMethods.sort(key=lambda cfunc: cfunc.line)
        for m in self.classMethods:
            m.checkBuiltin()
        for func in self.classMethods:
            func.genCode(dest)

    def genMethodTable(self, dest):
        if self.classMethods is None or len(self.classMethods) == 0:
            self.methodTableName = "NULL"
        else:
            # Double underscore methods not included. 
            plainMethods = [m for m in self.classMethods if builtins.getMethod(self.pyClass, m.name) is None]
            if len(plainMethods) == 0:
                self.methodTableName = "NULL"
            else:
                self.methodTableName = self.cObjectStruct + "_methods"
                pymethod.genMethodTable(dest, plainMethods, self.methodTableName)

    def genProperties(self, dest):
        """Properties implemented as PyMemberDef table"""
        if self.members is None or len(self.members) == 0:
            self.memberTableName = "NULL"
        else:
            self.memberTableName = self.cObjectStruct + "_members"
            pymember.genMemberTable(dest, self.members, self.memberTableName, self)

    def genSpecialBuiltins(self, dest):
        self.asNumberName = "0"
        self.asSequenceName = "0"
        self.asMappingName = "0"
        self.asBufferName = "0"
        if issubclass(self.pyClass, numbers.Number):
            self.asNumberName = self.genSpecialTable(dest, builtins.NumberMethods, "PyNumberMethods", "asNumber")
        if issubclass(self.pyClass, collections.Mapping):
            self.asMappingName = self.genSpecialTable(dest, builtins.MappingMethods, "PyMappingMethods", "asMapping")
        if issubclass(self.pyClass, collections.Sequence):
            self.asSequenceName = self.genSpecialTable(dest, builtins.SequenceMethods, "PySequenceMethods", "asSequence")
            if ccode.targetVersion >= (3, 0):
                self.asMappingName = self.genSpecialTable(dest, builtins.Py3SequenceMappingMethods, "PyMappingMethods", "asMapping")
        if hasattr(self.pyClass, "__getbuffer__") or hasattr(self.pyClass, "__releasebuffer__"):
            self.asBufferName = self.genSpecialTable(dest, builtins.BufferMethods, "PyBufferProcs", "asBuffer")


    def genType(self, dest):
        dest.LF()
        dest.code("PyTypeObject {name} = {{".format(name=self.cClassStruct))
        dest.indent()
        dest.code("PyVarObject_HEAD_INIT(NULL, 0)", semi=False) # If has a metaclass, handled in module init
        dest.code("\"{module}.{name}\",".format(module=self.pyClass.__module__, name=self.name))
        dest.code("sizeof({name}),".format(name=self.cObjectStruct))
        dest.code("0,")
        # Special methods
        dest.code("0,\t/* tp_dealloc */", semi=False)
        self.typeSlot("{pointer},\t/* tp_print */", dest)
        self.typeSlot("{pointer},\t/* tp_getattr */", dest)
        self.typeSlot("{pointer},\t/* tp_setattr */", dest)
        # __cmp__ is obsolete in Python 3, not recommended for 2
        dest.code("0,\t/* tp_compare/tp_reserved */", semi=False)
        self.typeSlot("{pointer},\t/* tp_repr */", dest)
        # Special method suites
        #dest.code("0,\t/* tp_as_number */", semi=False)
        dest.code("{name},\t/* tp_as_number */".format(name=self.asNumberName), semi=False)
        dest.code("{name},\t/* tp_as_sequence */".format(name=self.asSequenceName), semi=False)
        dest.code("{name},\t/* tp_as_mapping */".format(name=self.asMappingName), semi=False)
        # Special methods
        self.typeSlot("{pointer},\t/* tp_hash */", dest)
        self.typeSlot("{pointer},\t/* tp_call */", dest)
        self.typeSlot("{pointer},\t/* tp_str */", dest)
        if self.memberTableName == "NULL":
            self.typeSlot("{pointer},\t/* tp_getattro */", dest)
            dest.code("0,\t/* tp_setattro */", semi=False)
        else:
            dest.code("PyObject_GenericGetAttr,\t/* tp_getattro */", semi=False)
            dest.code("PyObject_GenericSetAttr,\t/* tp_setattro */", semi=False)
        # Special method suite
        dest.code("{name},\t/* tp_as_buffer */".format(name=self.asBufferName), semi=False)
        # About this class
        flags = "Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE"
        # Not actually sure that these flags matter. Earlier tests did not
        # set these flags and dict subclass worked anyway. Can't hurt?
        for c in (list, tuple, str, dict):
            if issubclass(self.pyClass, c):
                flags += " | Py_TPFLAGS_" + c.__name__.upper() + "_SUBCLASS"
        if ccode.targetVersion < (3, 0):
            for c in (int, unicode):
                if issubclass(self.pyClass, c):
                    flags += " | Py_TPFLAGS_" + c.__name__.upper() + "_SUBCLASS"
        # This does matter in Python 2, PyObject_CheckBuffer tests it
        if self.asBufferName != "0" and ccode.targetVersion < (3, 0):
            flags += "| Py_TPFLAGS_HAVE_NEWBUFFER"
        # New style finalizer?
        if ccode.targetVersion > (3, 4) and "__del__" in self.pyClass.__dict__:
            flags += " | Py_TPFLAGS_HAVE_FINALIZE"
        dest.code(flags + ",\t/* tp_flags */", semi=False)
        docStr = inspect.getdoc(self.pyClass)
        if docStr is not None:
            docStr = ccode.docStringLit(docStr)
        else:
            docStr = "0"
        dest.code("{doc},\t/* tp_doc */".format(doc=docStr), semi=False)
        # Memory related
        dest.code("0,\t/* tp_traverse */", semi=False)
        dest.code("0,\t/* tp_clear */", semi=False)
        # Yet another special method
        self.typeSlot("{pointer},\t/* tp_richcompare */", dest)
        # More memory related
        dest.code("0,\t/* tp_weaklistoffset */", semi=False)
        # Iteration methods
        self.typeSlot("{pointer},\t/* tp_iter */", dest)
        self.typeSlot("{pointer},\t/* tp_iternext */", dest)
        # Methods, instance vars, properties, superclass
        dest.code("{name},\t/* tp_methods */".format(name=self.methodTableName), semi=False)
        dest.code("{name},\t/* tp_members */".format(name=self.memberTableName), semi=False)
        #dest.code("0,\t/* tp_members */", semi=False)
        dest.code("0,\t/* tp_getset */", semi=False)
        dest.code("0,\t/* tp_base */", semi=False)
        # Internal
        dest.code("0,\t/* tp_dict */", semi=False)
        dest.code("0,\t/* tp_descr_get */", semi=False)
        dest.code("0,\t/* tp_descr_set */", semi=False)
        # Object dict for arbitrary (non-prop) attributes?
        if self.objAttribDict:
            dest.code("offsetof({struct}, {member}),\t/* tp_dictoffset */".format(
                struct=self.cObjectStruct, member=self.objAttribDict), semi=False)
        else:
            dest.code("0,\t/* tp_dictoffset */", semi=False)
        # And even more special methods
        self.typeSlot("{pointer},\t/* tp_init */", dest)
        dest.code("0,\t/* tp_alloc */", semi=False)
        self.typeSlot("{pointer},\t/* tp_new */", dest)
        dest.code("0,\t/* tp_free */", semi=False)
        # Internals
        dest.code("0,\t/* tp_is_gc */", semi=False)
        dest.code("0,\t/* tp_bases */", semi=False)
        dest.code("0,\t/* tp_mro */", semi=False)
        dest.code("0,\t/* tp_cache */", semi=False)
        dest.code("0,\t/* tp_subclasses */", semi=False)
        dest.code("0,\t/* tp_weaklist */", semi=False)
        if ccode.targetVersion < (3, 0):
            self.typeSlot("{pointer},\t/* tp_del */", dest)
        else:
            dest.code("0,\t/* tp_del */", semi=False)
        dest.code("0,\t/* tp_version_tag */", semi=False)
        if ccode.targetVersion >= (3, 4):
            self.typeSlot("{pointer},\t/* tp_finalize */", dest)
        # And done
        dest.unindent()
        dest.code("}", semi=True)

    def typeSlot(self, structLine, dest):
        """Generate single struct line with {pointer} replaced by either
           0 or name of builtin method. Field name must be in structLine"""
        # Extract field name
        start = structLine.index("/*")
        stop = structLine.index("*/")
        field = structLine[start:stop].strip(" /*/")
        # Built in slot that this class has method for?
        target = builtins.methodForField(field)
        for m in self.classMethods:
            if m.typeMethod is target:
                dest.code(structLine.format(pointer='(' + m.typeMethod.cType + ')' + m.cName), semi=False)
                break
        else:
            dest.code(structLine.format(pointer="0"), semi=False)

    def genSpecialTable(self, dest, methodList, tableTypeName, suffix):
        """Generate number, sequence, method, or buffer special methods,
           method table, and return name for type field"""
        dest.LF()
        # First find any already defined special methods.
        ops = {}
        for special in methodList:
            # Handle changes from version 2 to 3
            if special.version is not None and special.version != ccode.targetVersion[0]:
                continue
            # Quicker to test pyClass.__dict__first, but we have to search the
            # method list anyway on a hit. Don't need high performance
            for m in self.classMethods:
                if m.name == special.name:
                    ops[special.name] = m
                    break
            else:
                ops[special.name] = None
        # Now generate method table
        tableName = self.cObjectStruct + "_" + suffix
        dest.code("{tableType} {name} = {{".format(tableType=tableTypeName, name=tableName))
        dest.indent()
        # Unlike regular method table, specials are structs with fixed order
        for special in methodList:
            if special.version is not None and special.version != ccode.targetVersion[0]:
                continue
            m = ops[special.name]
            if m is not None:
                dest.code("{pointer}, /* {entry} */".format(pointer=m.cName, entry=m.typeMethod.field), semi=False)
            else:
                dest.code("0, /* {entry} */".format(entry=special.field), semi=False)
        dest.unindent()
        dest.code("}", semi=True)
        return "&" + tableName

    def genMetaclass(self, dest):
        metaclass = self.pyClass.__class__
        if ccode.targetVersion < (3, 0):
            field = "ob_type"
        else:
            field = "ob_base.ob_base.ob_type"
        if metaclass.__module__ is self.pyClass.__module__:
            dest.code("{name}.{field} = &{meta}".format(name=self.cClassStruct, field=field, meta=ccode.classStruct(metaclass)))
        else:
            getMeta = "PyDict_GetItemString(PyModule_GetDict(PyImport_ImportModule({mod})),{cls})".format(
                            mod=ccode.strLit(metaclass.__module__),
                            cls=ccode.strLit(metaclass.__name__))
            dest.code("{name}.{field} = {meta}".format(name=self.cClassStruct, field=field, meta="(PyTypeObject *)" + getMeta))

    def genBaseClasses(self, dest):
        """Create tuple of superclasses"""
        # Multiple or non builtin inheritance. This can give odd results, for example defining
        # a subclass of collections.Mapping will actually be a subclass of _abcoll.Mapping.
        supers = list(self.pyClass.__bases__)
        # Python 3.5 added runtime check that non-heap types could not inherit from heap types
        TPFLAGS_HEAPTYPE = (1 << 9)
        for c in supers[:]:
            if (c.__flags__ & TPFLAGS_HEAPTYPE) != 0:
                logging.warning(_T("C type {} cannot inherit from superclass {} because superclass is heap allocated".format(
                    self.name, c.__name__)))
                # Probably not a great idea for non-heap to inherit from heap in Python 2,
                # but it won't actually raise an exception so leave it. You've been warned
                if ccode.targetVersion >= (3, 0):
                    supers.remove(c)
        if len(supers) > 0:
            dest.code("{name}.tp_bases = PyTuple_Pack({n},".format(name=self.cClassStruct, n=len(supers)), semi=False)
            dest.indent()
            for c in supers:
                if c.__module__ is self.pyClass.__module__:
                    line = "PyDict_GetItemString(PyModule_GetDict(mod),{cls})".format(cls=ccode.strLit(c.__name__))
                else:
                    line = "PyDict_GetItemString(PyModule_GetDict(PyImport_ImportModule({mod})),{cls})".format(mod=ccode.strLit(c.__module__),cls=ccode.strLit(c.__name__))
                if c is not supers[-1]:
                    line += ","
                dest.code(line, semi=False)
            dest.unindent()
            dest.code(")")
        elif len(self.pyClass.__bases__) > 0:
            dest.comment("{name}.tp_bases = PyTuple_Pack(0, ...)".format(name=self.cClassStruct))


    def genModInitCode(self, dest):
        """Special code within module init function"""
        dest.LF()
        # Metaclass?
        if self.pyClass.__class__ is not type:
            self.genMetaclass(dest)
        # According to Python doco, have to set up superclass in runtime code, not type struct.
        # Has to be pointer to actual C struct, so can only use Python standard types or other
        # native classes in the same module as this one.
        cSuperType = object # Just in case
        for cls in self.getSuperClasses():
            if cls.__name__ in __builtins__ or cls.__module__ is self.pyClass.__module__:
                cSuperType = cls
                break
        dest.code("{name}.tp_base = (PyTypeObject *)&{base}".format(name=self.cClassStruct, base=ccode.classStruct(cSuperType)))
        # Special case: according to the Python 2 source code, static types DON'T inherit
        # allocation if super is object, for obscure backwards compatibility reasons
        if cSuperType is object and not ("__new__" in self.pyClass.__dict__):
            dest.code("{name}.tp_new = PyType_GenericNew".format(name=self.cClassStruct))
        # More complex multiple inheritance with tuple
        self.genBaseClasses(dest)
        dest.code("PyType_Ready(&{name})".format(name=self.cClassStruct))
        dest.code("PyModule_AddObject(mod, \"{name}\", (PyObject *)&{struct})".format(name=self.name,struct=self.cClassStruct))
