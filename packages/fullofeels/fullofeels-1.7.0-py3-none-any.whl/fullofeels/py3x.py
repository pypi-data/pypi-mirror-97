
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

#  Top level C code generator for Python version 3

# When I started this project I'd never written an extension module
# for Python 3, or even any serious programming in version 3. I was
# pleasantly surprised to find that there isn't much difference.

from __future__ import division, print_function

import inspect

from fullofeels import py27, ccode
from fullofeels.i18nstr import _T


class CModCoder(py27.CModCoder):
    """Changes to module top level for Python 3"""

    def modInitName(self):
        """Name of module init function, changes for Python 3"""
        return "PyInit_" + self.name

    def genModuleData(self):
        """Module name and other data now in a struct"""
        structName = self.name + "_module"
        if len(self.modMethods) == 0:
            methodTable = "NULL"
        else:
            methodTable = self.name + "_methods"
        if inspect.getdoc(self.source) is not None:
            docStr = "__doc__"
        else:
            docStr = "NULL"
        self.body.code("static struct PyModuleDef " + structName + " = {")
        self.body.indent()
        self.body.code("PyModuleDef_HEAD_INIT,")
        self.body.code(ccode.strLit(self.source.__name__) + ",")
        self.body.code(docStr + ",")
        self.body.code("-1,")
        self.body.code(methodTable + ",")
        self.body.unindent()
        self.body.code("}", semi=True)

    def createModule(self):
        """The special call to create module object itself"""
        structName = self.name + "_module"
        self.body.code("mod = PyModule_Create(&{data})".format(data=structName))

    def moduleInitReturn(self):
        """Module init function now returns the module"""
        self.body.code("return mod")
    
    def modReservedNames(self):
        """Couple of new names in Python 3"""
        return [
            "__cached__",
            "__package__"
            ] + super(CModCoder, self).modReservedNames()

    def modAddString(self, name, value):
        """Add string constant to module. Only used in init function"""
        # Python 3 accepts UTF-8 value, so easy
        self.body.code(u"PyModule_AddStringConstant(mod, \"{name}\", {cValue})".format(name=name, cValue=ccode.strLit(value)))


