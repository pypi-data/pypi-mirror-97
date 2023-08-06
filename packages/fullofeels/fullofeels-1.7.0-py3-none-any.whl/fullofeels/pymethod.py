
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#   Generate C outline for Python methods (includes global functions)

from __future__ import division, print_function

import sys
import os
from os import path
import types
import inspect
import ctypes
import logging

from fullofeels.i18nstr import _T

from fullofeels import ccode, builtins, parameter


# Methods that return self are common, so this sentinel value identifies such
Py_Self = object()


def cleanSource(origLines):
    """Strip comments, join statements over multiple lines"""
    clean = []
    for line in origLines:
        if line.find('#') > 0:
            line = line[0:line.find('#')]
        # TODO check for continuation
        clean.append(line)
    return clean

def genMethodTable(dest, methodList, cArrayName):
    """Standard Python method table for module or class"""
    dest.LF()
    dest.code("static PyMethodDef {name}[] = {{".format(name=cArrayName))
    dest.indent()
    for theMethod in methodList:
        docStr = inspect.getdoc(theMethod.callable)
        if docStr is not None:
            docStr = ccode.docStringLit(docStr)
        else:
            docStr = "NULL"
        dest.code("{{ {name}, (PyCFunction){body}, {flags}, {doco} }},".format(
                            name=ccode.strLit(theMethod.name),
                            body=theMethod.cName,
                            flags=theMethod.flags(),
                            doco=docStr),
                        semi=False)
    dest.code("{ NULL, NULL, 0, NULL },", semi=False)
    dest.unindent()
    dest.code("}", semi=True)

class CFunc(object):
    """Method common code, used for module global functions"""

    def __init__(self, callable, selfType=None, outerName=None, prefix=None):
        self.callable = callable
        self.name = self.callable.__name__
        self.selfType = selfType
        self.src, self.line = inspect.getsourcelines(self.callable)
        self.src = cleanSource(self.src)
        if sys.version_info[0] < 3:
            self.posArgs, self.varArgs, self.dictArgs, self.defaults = inspect.getargspec(self.callable)
        else:
            self.posArgs, self.varArgs, self.dictArgs, self.defaults = inspect.getfullargspec(self.callable)[:4]
        self.firstArgName = "ignore"    # Class or instance methods will change to cls or self
        self.cName = self.genName(outerName, prefix)
        self.callable.cName = self.cName    # Useful for code generation
        self.pythonAPI = True # Set to false if not added to module
        # Annotations?
        try:
            self.annotations = self.callable.__annotations__
        except AttributeError:
            self.annotations = {}   # Values can be set by parseArguments

    def genName(self, outerName=None, prefix=None):
        """Return C function name for method, optional method/class name and C prefix"""
        funcName = ccode.id(self.callable.__name__)
        # Remove double underscores because they look horrible in C. This will cause a
        # compiler error if a class has, say, __init__ and init methods. Too bad
        if funcName.startswith("__") and funcName.endswith("__"):
            funcName = funcName[2:-2]
        if outerName:
            funcName = outerName + "_" + funcName
        if prefix:
            funcName = prefix + funcName
        return funcName

    def flags(self):
        """Return method table flags, as string"""
        if len(self.posArgs) == 0 and self.varArgs is None and self.dictArgs is None:
            return "METH_NOARGS"
        result = []
        # In Python 3 METH_VARARGS has to be set, accidental bug that
        # wasn't noticed until it was too late to change existing code
        if len(self.posArgs) > 0 or self.varArgs is not None:
            result.append("METH_VARARGS")
        elif ccode.targetVersion >= (3, 0):
            result.append("METH_VARARGS")
        if len(self.posArgs) > 0 or self.dictArgs is not None:
            result.append("METH_KEYWORDS")
        return " | ".join(result)

    def returnType(self):
        """Python return type or None from source"""
        retType = self.annotations.get("return", None)
        if retType:
            return retType
        # Look for a return statement?
        srcCode = [line.strip() for line in self.src]
        srcCode.reverse()
        for line in srcCode:
            if line.startswith("return"):
                # Strip leading return
                line = line[6:]
                if line.strip() == "self":
                    return Py_Self
                what = eval(line)
                # Expect something like return int, return MyClass
                if inspect.isclass(what):
                    return what
                # But allow for return None instead of pass
                elif what is None:
                    return None
                # Or possibly return 0, return True, ...
                else:
                    return type(what)
        return None

    def cArgumentNames(self):
        """Return C argument names for arguments tuple and keywords dict.
           Defaults are args, kwArgs"""
        if len(self.posArgs) == 0 and self.varArgs is not None:
            argName = self.varArgs
        else:
            argName = "args"
        if self.dictArgs is not None:
            kwName = self.dictArgs
        else:
            kwName = "kwArgs"
        return (argName, kwName)

    def prototype(self, retType=None, selfType=None):
        """Return C prototype for Python function or method. 
           Return and self type default to standard Python object"""
        if retType:
            retStr = ccode.objectStruct(retType) + " *"
        else:
            retStr = "PyObject *"
        #
        if selfType:
            selfStr = ccode.objectStruct(selfType) + " * "
        else:
            selfStr = "PyObject * "
        argName, kwName = self.cArgumentNames()
        return retStr + '\n' + self.cName + "(" + selfStr + self.firstArgName + ", PyObject * " + argName + ", PyObject * " + kwName + ")"

    def genLocalDefs(self, dest):
        """Declare C locals for positional arguments"""
        if len(self.posArgs) == 0:
            return
        argNames = [ccode.strLit(name) for name in self.posArgs]
        dest.code("const char * keywords[] = { " + ", ".join(argNames) + ", NULL }", semi=True)
        # C declarations
        for name in self.posArgs:
            dest.code("{type} {id}".format(type=parameter.cType(name, self.annotations), id=ccode.id(name)))
        dest.LF()
        # Defaults?
        if self.defaults is not None:
            offset = len(self.posArgs) - len(self.defaults)
            for idx, val in enumerate(self.defaults):
                dest.code(ccode.id(self.posArgs[idx + offset]) + " = " + ccode.value(val))
            dest.LF()

    def genArgParsingCode(self, dest):
        """Generate any code needed for parsing arguments into C"""
        # Note: don't need to check that positional arg list is empty if no args,
        # because Python interpreter already does that if METH_NOARGS set
        if len(self.posArgs) == 0:
            # Easy, just varargs tuple and/or keyword dict.
            # However, keyword-only function must check that posArgs is non-zero
            if self.varArgs is None and self.dictArgs is not None:
                dest.code("if (! PyArg_ParseTuple(args, \"\", args))", semi=False)
                dest.indent()
                dest.code("return NULL")
                dest.unindent()
            return
        # Impossible cases: can't handle positional AND variable length,
        # or positional AND keywords dictionary, in C
        if len(self.posArgs) > 0 and self.varArgs is not None:
            dest.comment(ccode.text(_T("You will have to figure out how to decode the arguments")))
            logging.warning(_T("Don't know how to parse combined positional and variable length args in C"))
            return
        if len(self.posArgs) > 0 and self.dictArgs is not None:
            dest.comment(ccode.text(_T("You will have to figure out how to decode the arguments")))
            logging.warning(_T("Don't know how to parse combined positional and keywords dictionary in C"))
            return
        # Parse parameters
        formatStr = ""
        params = []
        if self.defaults is None:
            firstDefault = len(self.posArgs) # Never reach
        else:
            firstDefault = len(self.posArgs) - len(self.defaults)
        for idx, name in enumerate(self.posArgs):
            if idx == firstDefault:
                formatStr += "|"
            formatStr += parameter.formatStr(name, self.annotations)
            params.append(parameter.parseArgs(name, self.annotations))
        # Final call
        argName, kwName = self.cArgumentNames()
        dest.code("if (! PyArg_ParseTupleAndKeywords({args}, {kw}, \"{format}\", keywords, {params}))".format(
                    args=argName, kw=kwName, format=formatStr, params=", ".join(params)), semi=False)
        dest.indent()
        # This will generate a compiler warning for __init__ builtin functions because
        # those return int, not PyObject *. I don't think it's worth fixing
        dest.code("return NULL")
        dest.unindent()
        dest.LF()
       
    def genPrintCode(self, dest):
        """Just print out the Python arguments"""
        if ccode.targetVersion < (3, 0):
            PyToCStr = 'PyString_AsString'
        else:
            PyToCStr = 'PyUnicode_AsUTF8'
        dest.code("printf({name})".format(name=ccode.strLit(self.cName + "(")))
        for name in self.posArgs:
            dest.code("printf(\"{name} = %s \", ".format(name=name) +
                    PyToCStr + "(PyObject_Str(" + ccode.id(name) + ")))")
        argName, kwName = self.cArgumentNames()
        if self.varArgs is not None:
            dest.code("printf(\"{name} = %s \", ".format(name=argName) +
                    PyToCStr + "(PyObject_Str(" + ccode.id(argName) + ")))")
        if self.dictArgs is not None:
            dest.code("printf(\"{name} = %s \", ".format(name=kwName) +
                    PyToCStr + "(PyObject_Str(" + ccode.id(kwName) + ")))")
        dest.code("printf("+ ccode.dquote + ')\\n' + ccode.dquote + ")")
        dest.LF()

    def genCleanupCode(self, dest):
        """Need to release Py_buffer parameters"""
        for argName in self.posArgs:
            line = parameter.cleanup(argName, self.annotations)
            if line:
                dest.code(line)

    def genCode(self, dest):
        """Write C implementation for method to dest file"""
        logging.debug("Code C func {} for Python {}".format(self.cName, self.name))
        dest.LF()
        # Special case: has @argumentConverter decorator?
        if hasattr(self.callable, "_foeelsArgumentConverter"):
            parameter.genArgumentConverter(self, dest)
            return
        # Standard Python coding style seems to be always return PyObject *,
        # so return type is ignored and method body casts result
        dest.code("static " + self.prototype(selfType=self.selfType, retType=None), semi=False)
        dest.code("{")
        dest.indent()
        ret = self.returnType()
        if ret is not None and ret is not Py_Self:
            dest.code(ccode.objectStruct(ret) + " * _foeels_result")
        #
        if hasattr(self.callable, "_foeelsPosArgs") or hasattr(self.callable, "_foeelsKwArgs"):
            self.annotations = parameter.buildArgTypes(self)
        self.genLocalDefs(dest)
        self.genArgParsingCode(dest)
        if ccode.genPrint:
            self.genPrintCode(dest)
        #
        self.genCleanupCode(dest)
        if ret is None:
            dest.code("Py_RETURN_NONE")
        elif ret is Py_Self:
            dest.code("Py_INCREF(self)")
            dest.code("return (PyObject *)self")
        else:
            dest.code("return (PyObject *)_foeels_result")
        dest.unindent()
        dest.code("}")


class CClassMethod(CFunc):
    """Handle special cases for classes"""

    def __init__(self, callable, ownerClass, selfType, outerName=None, prefix=None):
        super(CClassMethod, self).__init__(callable, selfType, outerName, prefix)
        self.owner = ownerClass
        if self.selfType is not None:
            # Don't include 'self' among arguments
            self.firstArgName = self.posArgs[0]
            self.posArgs = self.posArgs[1:]
        # Built in?
        self.typeMethod = builtins.getMethod(self.owner.pyClass, self.name)

    def flags(self):
        result = super(CClassMethod, self).flags()
        if self.selfType is None:
            result += " | METH_STATIC"
        elif self.selfType is type:
            result += " | METH_CLASS"
        return result

    def checkBuiltin(self):
        if self.typeMethod is None or self.typeMethod.stdArgs:
            return
        myClass = self.selfType.pyClass
        ret = self.returnType()
        if not (ret is None or (ret is Py_Self and self.typeMethod.retType is object) or ret is self.typeMethod.retType):
            raise TypeError(str(myClass.__module__) + "." + myClass.__name__ + "." + self.name +
                        _T(" Builtin method should not specify return type"))
        if self.varArgs is not None or self.dictArgs is not None or self.defaults is not None:
            raise TypeError(str(myClass.__module__) + "." + myClass.__name__ + "." + self.name +
                        _T(" This builtin method cannot have variable length, dictionary, or default arguments"))
        if len(self.posArgs) != len(self.typeMethod.argList) - 1:
            raise TypeError(str(myClass.__module__) + "." + myClass.__name__ + "." + self.name +
                        _T(" This builtin method has wrong number of arguments: expected {orig} actual {meth}").format(orig=len(self.typeMethod.argList) - 1, meth=len(self.posArgs)))

    def genCode(self, dest):
        """Override to handle special builtin type methods"""
        if self.typeMethod is None:
            # Easy
            super(CClassMethod, self).genCode(dest)
            return
        dest.LF()
        # Prototype
        dest.code("static " + builtins.cTypeString(self.typeMethod.retType), semi=False)
        argStrings = [builtins.cTypeString(self.typeMethod.argList[0]) + " " + self.firstArgName]
        if self.typeMethod.stdArgs:
            argName, kwName = self.cArgumentNames()
            argStrings.append("PyObject * " + argName)
            argStrings.append("PyObject * " + kwName)
        else:
            for argType, argName in zip(self.typeMethod.argList[1:], self.posArgs):
                argStrings.append(builtins.cTypeString(argType) + " " + argName)
        dest.code(self.cName + "(" + ', '.join(argStrings) + ")", semi=False)
        #
        dest.code("{")
        dest.indent()
        if self.typeMethod.stdArgs:
            self.genLocalDefs(dest)
            self.genArgParsingCode(dest)
        if ccode.genPrint:
            if self.typeMethod.stdArgs:
                self.genPrintCode(dest)
            else:
                dest.code("printf({name})".format(name=ccode.strLit(self.cName + "\n")))

        #
        if self.name == "__new__":
            # Special case to make testing easier
            dest.code("return {cls}->tp_alloc({cls}, 0)".format(cls=self.firstArgName))
        elif self.returnType() is Py_Self:
            dest.code("Py_INCREF(self)")
            dest.code("return (PyObject *)self")
        elif self.typeMethod.retType is object:
            dest.code("Py_RETURN_NONE")
        elif self.typeMethod.retType is not None:
            dest.code("return 0")
        dest.unindent()
        dest.code("}")
