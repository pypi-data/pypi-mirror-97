
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#  Top level C code generator for Python version 2.7

from __future__ import division, print_function

import os, types, inspect
from os import path
import logging

from fullofeels import codegen, ccode, pymethod, pyclass, pymember
from fullofeels.i18nstr import _T

class CModCoder(object):
    """Build outline for C/CPP/Objective-C implementation of Python module"""

    def __init__(self, options,
                    newClass=pyclass.CClass,
                    newGlobalFunc=pymethod.CFunc,
                    newClassMethod=pymethod.CClassMethod,
                    newClassProperty=pymember.CProperty):
        """Options is argparse object. Others are classes to use
           during code generation if you want to override things.
        """
        self.opts = options
        #
        self.header = None
        self.body   = None
        self.bodyExt = self.opts.ext

        # These are the classes to use for the various bits and pieces
        self.newClass = newClass
        self.newGlobalFunc = newGlobalFunc
        self.newClassMethod = newClassMethod
        self.newClassProperty = newClassProperty
        # and pass on
        pyclass.CClass.newClassMethod = self.newClassMethod
        pyclass.CClass.newClassProperty = self.newClassProperty

    def config(self, mod):
        """One time startup for given Python source module"""
        self.source = mod
        self.name   = ccode.id(mod.__name__)
        self.defs   = {}
        # Output code files
        base = os.path.abspath(self.source.__file__)
        self.basePath = os.path.dirname(base)
        self.baseName = os.path.splitext(os.path.basename(base))[0]
        self.createFiles()
        self.initCodeStyle()

    def beginModule(self):
        """Start of header and body source code"""
        self.header.write(ccode.beginHeader.format(hdrID = self.cppPrefix + self.name.upper()))
        self.genAuthorCopyright(self.header)
        if self.bodyExt != ".cpp":
            self.header.write(ccode.beginCPPGuard)
        #
        self.body.write(ccode.beginBody.format(name=self.name))
        self.genAuthorCopyright(self.body)
        doco = inspect.getdoc(self.source)
        if doco is not None:
            self.body.LF()
            self.body.code("PyDoc_VAR(__doc__) = {value}".format(value=ccode.docStringLit(doco)))

    def genDefinitions(self):
        """Code the type and method bodies"""
        self.defs = self.splitModDefinitions()
        ## Classes
        classNames = self.defs.get(type, [])
        self.modClasses = []
        for name in classNames:
            self.modClasses.append(self.newClass(self.source.__dict__[name], outerName=self.name, prefix=None))
        # Generate code in same order as original Python
        self.modClasses.sort(key=lambda cclass: cclass.line)
        for cls in self.modClasses:
            cls.genHeaderDef(self.header)
            cls.genCode(self.body)
        ## Methods
        methodNames = self.defs.get(types.FunctionType, [])
        self.modMethods = []
        for name in methodNames:
            self.modMethods.append(self.newGlobalFunc(self.source.__dict__[name], outerName=self.name))
        self.modMethods.sort(key=lambda cfunc: cfunc.line)
        for func in self.modMethods:
            func.genCode(self.body)
        # And module method table, after removing internal
        self.modMethods = [m for m in self.modMethods if m.pythonAPI]
        if len(self.modMethods) > 0:
            pymethod.genMethodTable(self.body, self.modMethods, self.name + "_methods")

    def genModuleData(self):
        """Used in Python 3"""
        pass

    def createModule(self):
        """The special call to create module object itself"""
        if len(self.modMethods) == 0:
            methodTable = "NULL"
        else:
            methodTable = self.name + "_methods"
        if inspect.getdoc(self.source) is not None:
            docStr = "__doc__"
        else:
            docStr = '""'
        self.body.code("mod = Py_InitModule3(\"{name}\", {methods}, {doc})".format(name=self.name, methods=methodTable, doc=docStr))

    def finishInit(self):
        """Finish up and return"""
        self.body.LF()
        self.body.code("if (PyErr_Occurred())", semi=False)
        self.body.indent()
        self.body.code("PyErr_Print()")
        self.body.unindent()
        self.moduleInitReturn()

    def moduleInitReturn(self):
        """Used in Python 3"""
        pass

    def genInitFunction(self):
        """The all-important init function"""
        self.header.LF()
        self.header.code(self.modInitPrototype())
        #
        self.genModuleData()
        self.body.LF()
        self.body.code(self.modInitPrototype(), semi=False)
        self.body.code("{")
        self.body.indent()
        self.body.code("PyObject * mod")
        # Create the module
        self.body.LF()
        if ccode.genPrint:
            self.body.LF()
            self.body.code('printf(\"{name}\\n\")'.format(name=ccode.id(self.modInitName())))
        self.createModule()
        # Module classes
        if len(self.modClasses) > 0:
            for cls in self.modClasses:
                cls.genModInitCode(self.body)
        # Module constants
        self.genModStrings()
        self.genModInts()
        self.genModFloats()
        # Done
        self.finishInit()
        self.body.unindent()
        self.body.code("}");

    def endModule(self):
        """Finish up"""
        if self.bodyExt != ".cpp":
            self.header.write(ccode.endCPPGuard)
        self.header.write(ccode.endHeader)
        #
        self.body.write(ccode.endBody)

    def genAuthorCopyright(self, dest):
        """Translate standard module strings into comment in C and write to dest"""
        text = []
        # These strings from the Google coding standards
        for key in ["__author__", "__copyright__", "__license__", "__version__"]:
            s = self.source.__dict__.get(key, None)
            if isinstance(s, str) and len(s) > 0:
                text.append(ccode.text(s))
            if ccode.targetVersion < (3, 0) and isinstance(s, unicode) and len(s) > 0:
                text.append(ccode.text(s))
        if len(text) > 0:
            cText = "\n".join(text)
            dest.LF()
            dest.comment(cText)

    def splitModDefinitions(self):
        """Divide module definitions into strings, methods, etc"""
        # Because Python distinguishes between built-in types and program
        # defined classes, my clever use of types as dict keys does not
        # actually work :-( Think about redoing this or dropping altogether
        reserved = self.modReservedNames()
        result = {}
        for name, value in self.source.__dict__.items():
            if name in reserved:
                continue
            # There are classes and types and metatypes... To simplify code
            # elsewhere, ignore any Python 2 old style classes.
            if inspect.isclass(value) and len(value.__bases__) > 0:
                key = type
            else:
                key = type(value)
            if key in result:
                result[key].append(name)
            else:
                result[key] = [ name ]
        return result

    def genModStrings(self):
        strList = self.defs.get(str, [])
        if ccode.targetVersion < (3, 0):
            strList += self.defs.get(unicode, [])
        if len(strList) == 0:
            return
        self.body.LF()
        for name in strList:
            value = self.source.__dict__[name]
            # Python 3 is single C call. For Python 2, more complicated
            self.modAddString(name, value)

    def genModInts(self):
        intList = self.defs.get(int, [])
        if len(intList) == 0:
            return
        self.body.LF()
        for name in intList:
            value = self.source.__dict__[name]
            self.body.code("PyModule_AddIntConstant(mod, \"{name}\", {cValue})".format(name=name, cValue=repr(value)))

    def genModFloats(self):
        floatList = self.defs.get(float, [])
        if len(floatList) == 0:
            return
        self.body.LF()
        for name in floatList:
            value = self.source.__dict__[name]
            self.body.code("PyModule_AddObject(mod, \"{name}\", PyFloat_FromDouble({cValue}))".format(name=name, cValue=repr(value)))

    def createFiles(self):
        """Open head header and body files for module"""
        headerName = os.path.join(self.basePath, self.baseName + ".h")
        bodyName = os.path.join(self.basePath, self.baseName + self.bodyExt)
        self.header = codegen.CFile(headerName, diff=self.opts.diff, backup=self.opts.backup)
        self.body   = codegen.CFile(bodyName, diff=self.opts.diff, backup=self.opts.backup)
        logging.info("Creating code files {}, {}".format(headerName, bodyName))

    def initCodeStyle(self):
        """So far just prefixes to stick on generated C names"""
        # Prefix for C types and classes specified by Python module.
        # Anything #defined gets the prefix in upper case, with underscore appended
        self.cPrefix = self.source.__dict__.get("_prefix", "")
        self.cppPrefix = self.cPrefix.rstrip("_").upper() + "_"
        #print("C names get {0} CPP names get {1}".format(self.cPrefix, self.cppPrefix))

    def modInitName(self):
        """Name of module init function, changes for Python 3"""
        return "init" + self.name

    def modInitPrototype(self):
        """Return initmodule prototype - changes in Python 3"""
        return "PyMODINIT_FUNC {name}(void)".format(name=self.modInitName())

    def modReservedNames(self):
        """Return names in module dict that should not be generated in C."""
        return [
                # Python auto generated
                "__name__" , "__doc__", "__file__",
                # Config directives
                "_prefix",
        ]

    def modAddString(self, name, value):
        """Add string constant to module. Only used in init function"""
        # Python 2 have to distinguish between ascii and unicode :-(
        try:
            asciiValue = value.encode('ascii')
            self.body.code(u"PyModule_AddStringConstant(mod, \"{name}\", {cValue})".format(name=name, cValue=ccode.strLit(asciiValue)))
        except UnicodeError:
            self.body.code(u"PyModule_AddObject(mod, \"{name}\", PyUnicode_DecodeUTF8({cValue}, {nBytes}, \"strict\"))".format(name=name,
                                    cValue=ccode.strLit(value), nBytes=len(bytearray(value, 'utf-8'))))

    def close(self):
        if self.header:
            self.header.close()
            self.header = None
        if self.body:
            self.body.close()
            self.body = None
        self.source = None
